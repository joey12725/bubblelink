#!/usr/bin/env python3
"""Fail-hard structural/manufacturing validator for BubbleLink CTRL v1.1.

The validator intentionally uses only the Python standard library.  It validates
the checked circuit JSON independently from the TypeScript source, then validates
Gerber/Excellon, KiCad PCB, PCBWay BOM/CPL, DRC, and SHA-256 artifacts when they
are supplied or uniquely auto-discovered.

Exit codes:
    0: every required check passed
    1: at least one check failed
    2: no failure, but at least one export/DRC check remains pending
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR_VERSION = "1.0.0"
DEFAULT_RELEASE_ROOT = SCRIPT_DIR.parent
DEFAULT_CIRCUIT = SCRIPT_DIR.parents[1] / "postroute" / "BubbleLink_CTRL_v1_1_FINAL.circuit.json"
DEFAULT_SOURCE = SCRIPT_DIR.parents[1] / "tscircuit" / "circuit.tsx"
EPS = 1e-6


class ValidationError(RuntimeError):
    """Raised for a malformed input that cannot be safely interpreted."""


class Report:
    def __init__(self, phase: str) -> None:
        self.phase = phase
        self.checks: list[dict[str, Any]] = []

    def add(
        self,
        check_id: str,
        section: str,
        status: str,
        message: str,
        evidence: Any | None = None,
    ) -> None:
        if status not in {"PASS", "FAIL", "PENDING"}:
            raise ValueError(f"invalid check status: {status}")
        item: dict[str, Any] = {
            "id": check_id,
            "section": section,
            "status": status,
            "message": message,
        }
        if evidence is not None:
            item["evidence"] = evidence
        self.checks.append(item)

    def passed(self, check_id: str, section: str, message: str, evidence: Any | None = None) -> None:
        self.add(check_id, section, "PASS", message, evidence)

    def failed(self, check_id: str, section: str, message: str, evidence: Any | None = None) -> None:
        self.add(check_id, section, "FAIL", message, evidence)

    def external_missing(self, check_id: str, section: str, message: str) -> None:
        status = "FAIL" if self.phase == "release" else "PENDING"
        self.add(check_id, section, status, message)

    def summary(self) -> dict[str, int]:
        counts = Counter(item["status"] for item in self.checks)
        return {key: counts.get(key, 0) for key in ("PASS", "FAIL", "PENDING")}

    def exit_code(self) -> int:
        summary = self.summary()
        if summary["FAIL"]:
            return 1
        if summary["PENDING"]:
            return 2
        return 0

    def as_dict(self, inputs: dict[str, str | None]) -> dict[str, Any]:
        code = self.exit_code()
        disposition = {0: "PASS", 1: "FAIL", 2: "PENDING"}[code]
        return {
            "schema_version": 1,
            "validator": "BubbleLink manufacturing structural QA",
            "validator_version": VALIDATOR_VERSION,
            "phase": self.phase,
            "disposition": disposition,
            "exit_code": code,
            "summary": self.summary(),
            "inputs": inputs,
            "checks": self.checks,
        }


def close(a: Any, b: Any, tol: float = EPS) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=tol)
    except (TypeError, ValueError):
        return False


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot parse JSON {path}: {exc}") from exc


def normalize_pin_hint(value: Any) -> str | None:
    text = str(value).strip().lower()
    match = re.fullmatch(r"pin[_ -]?(\d+)", text)
    if match:
        return str(int(match.group(1)))
    if re.fullmatch(r"\d+", text):
        return str(int(text))
    return None


def point_in_polygon(point: tuple[float, float], vertices: Sequence[dict[str, Any]]) -> bool:
    x, y = point
    inside = False
    if len(vertices) < 3:
        return False
    j = len(vertices) - 1
    for i, vertex in enumerate(vertices):
        xi, yi = float(vertex["x"]), float(vertex["y"])
        xj, yj = float(vertices[j]["x"]), float(vertices[j]["y"])
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-300) + xi
        ):
            inside = not inside
        j = i
    return inside


def copper_pour_contains(pour: dict[str, Any], point: tuple[float, float]) -> bool:
    shape = pour.get("brep_shape", {})
    outer = shape.get("outer_ring", {}).get("vertices", [])
    if not point_in_polygon(point, outer):
        return False
    return not any(
        point_in_polygon(point, ring.get("vertices", []))
        for ring in shape.get("inner_rings", [])
    )


def distance_point_segment(
    point: tuple[float, float], start: tuple[float, float], end: tuple[float, float]
) -> float:
    px, py = point
    ax, ay = start
    bx, by = end
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def polygon_edges(vertices: Sequence[tuple[float, float]]) -> Iterator[tuple[tuple[float, float], tuple[float, float]]]:
    for index, vertex in enumerate(vertices):
        yield vertex, vertices[(index + 1) % len(vertices)]


def cross_product(
    first: tuple[float, float], second: tuple[float, float], third: tuple[float, float]
) -> float:
    return (second[0] - first[0]) * (third[1] - first[1]) - (second[1] - first[1]) * (third[0] - first[0])


def point_on_segment(
    point: tuple[float, float], start: tuple[float, float], end: tuple[float, float]
) -> bool:
    return (
        abs(cross_product(start, end, point)) <= EPS
        and min(start[0], end[0]) - EPS <= point[0] <= max(start[0], end[0]) + EPS
        and min(start[1], end[1]) - EPS <= point[1] <= max(start[1], end[1]) + EPS
    )


def segments_intersect(
    first_start: tuple[float, float],
    first_end: tuple[float, float],
    second_start: tuple[float, float],
    second_end: tuple[float, float],
) -> bool:
    orientations = (
        cross_product(first_start, first_end, second_start),
        cross_product(first_start, first_end, second_end),
        cross_product(second_start, second_end, first_start),
        cross_product(second_start, second_end, first_end),
    )
    if (
        ((orientations[0] > EPS and orientations[1] < -EPS) or (orientations[0] < -EPS and orientations[1] > EPS))
        and ((orientations[2] > EPS and orientations[3] < -EPS) or (orientations[2] < -EPS and orientations[3] > EPS))
    ):
        return True
    return any(
        abs(orientation) <= EPS and point_on_segment(point, start, end)
        for orientation, point, start, end in (
            (orientations[0], second_start, first_start, first_end),
            (orientations[1], second_end, first_start, first_end),
            (orientations[2], first_start, second_start, second_end),
            (orientations[3], first_end, second_start, second_end),
        )
    )


def point_in_polygon_xy(point: tuple[float, float], vertices: Sequence[tuple[float, float]]) -> bool:
    if len(vertices) < 3:
        return False
    if any(point_on_segment(point, start, end) for start, end in polygon_edges(vertices)):
        return True
    x, y = point
    inside = False
    for start, end in polygon_edges(vertices):
        if ((start[1] > y) != (end[1] > y)) and (
            x < (end[0] - start[0]) * (y - start[1]) / ((end[1] - start[1]) or 1e-300) + start[0]
        ):
            inside = not inside
    return inside


def polygons_overlap(
    first: Sequence[tuple[float, float]], second: Sequence[tuple[float, float]]
) -> bool:
    if any(
        segments_intersect(first_start, first_end, second_start, second_end)
        for first_start, first_end in polygon_edges(first)
        for second_start, second_end in polygon_edges(second)
    ):
        return True
    return point_in_polygon_xy(first[0], second) or point_in_polygon_xy(second[0], first)


def polygon_clearance(
    first: Sequence[tuple[float, float]], second: Sequence[tuple[float, float]]
) -> float:
    if polygons_overlap(first, second):
        return 0.0
    return min(
        [distance_point_segment(point, start, end) for point in first for start, end in polygon_edges(second)]
        + [distance_point_segment(point, start, end) for point in second for start, end in polygon_edges(first)]
    )


def courtyard_polygon(item: dict[str, Any]) -> list[tuple[float, float]]:
    if item.get("type") == "pcb_courtyard_rect":
        center = item.get("center", {})
        half_width = float(item["width"]) / 2
        half_height = float(item["height"]) / 2
        angle = math.radians(float(item.get("ccw_rotation", 0)))
        cosine, sine = math.cos(angle), math.sin(angle)
        return [
            (
                float(center["x"]) + local_x * cosine - local_y * sine,
                float(center["y"]) + local_x * sine + local_y * cosine,
            )
            for local_x, local_y in (
                (-half_width, -half_height),
                (half_width, -half_height),
                (half_width, half_height),
                (-half_width, half_height),
            )
        ]
    if item.get("type") == "pcb_courtyard_outline":
        vertices = [(float(point["x"]), float(point["y"])) for point in item.get("outline", [])]
        cleaned: list[tuple[float, float]] = []
        for vertex in vertices:
            if not cleaned or vertex != cleaned[-1]:
                cleaned.append(vertex)
        if len(cleaned) > 1 and cleaned[0] == cleaned[-1]:
            cleaned.pop()
        return cleaned
    return []


def distance_to_ring(point: tuple[float, float], vertices: Sequence[dict[str, Any]]) -> float:
    if not vertices:
        return 0.0
    distances = []
    for index, vertex in enumerate(vertices):
        nxt = vertices[(index + 1) % len(vertices)]
        distances.append(
            distance_point_segment(
                point,
                (float(vertex["x"]), float(vertex["y"])),
                (float(nxt["x"]), float(nxt["y"])),
            )
        )
    return min(distances)


def copper_radius(item: dict[str, Any]) -> float:
    """Conservative radial extent for a pad/via copper shape."""
    if item.get("radius") is not None:
        return float(item["radius"])
    diameter_fields = ("outer_diameter", "diameter", "pad_diameter")
    diameters = [float(item[field]) for field in diameter_fields if item.get(field) is not None]
    width_fields = ("width", "rect_pad_width", "pad_width")
    height_fields = ("height", "rect_pad_height", "pad_height")
    widths = [float(item[field]) for field in width_fields if item.get(field) is not None]
    heights = [float(item[field]) for field in height_fields if item.get(field) is not None]
    if widths or heights:
        half_width = max(widths, default=max(heights, default=0.0)) / 2
        half_height = max(heights, default=max(widths, default=0.0)) / 2
        return math.hypot(half_width, half_height)
    if diameters:
        return max(diameters) / 2
    if item.get("hole_diameter") is not None:
        return float(item["hole_diameter"]) / 2
    return 0.0


def trace_via_inventory(
    routed_traces: Sequence[dict[str, Any]], pcb_vias: Sequence[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return unique layer transitions owned by one or more routed traces."""
    inventory: dict[tuple[float, float], dict[str, Any]] = {}
    routed_ids = {str(trace.get("pcb_trace_id")) for trace in routed_traces}
    for trace in routed_traces:
        for route_point in trace.get("route", []):
            if route_point.get("route_type") != "via":
                continue
            key = (round(float(route_point["x"]), 6), round(float(route_point["y"]), 6))
            inventory[key] = {
                "x": float(route_point["x"]),
                "y": float(route_point["y"]),
                "from_layer": route_point.get("from_layer"),
                "to_layer": route_point.get("to_layer"),
            }
    for via in pcb_vias:
        if str(via.get("pcb_trace_id")) not in routed_ids:
            continue
        key = (round(float(via["x"]), 6), round(float(via["y"]), 6))
        inventory[key] = {
            "x": float(via["x"]),
            "y": float(via["y"]),
            "drill_mm": via.get("hole_diameter", via.get("drill_diameter")),
            "diameter_mm": via.get("outer_diameter", via.get("diameter")),
        }
    return [inventory[key] for key in sorted(inventory)]


def element_count(elements: Sequence[dict[str, Any]], kind: str) -> int:
    return sum(1 for item in elements if item.get("type") == kind)


def validate_circuit(path: Path, manifest: dict[str, Any], report: Report) -> dict[str, Any] | None:
    section = "circuit_json"
    if not path.is_file():
        report.failed("CIR-001", section, f"required circuit JSON is missing: {path}")
        return None
    try:
        elements = safe_json(path)
    except ValidationError as exc:
        report.failed("CIR-001", section, str(exc))
        return None
    if not isinstance(elements, list) or not all(isinstance(item, dict) for item in elements):
        report.failed("CIR-001", section, "circuit JSON must be a top-level list of objects")
        return None
    report.passed("CIR-001", section, "circuit JSON parsed", {"elements": len(elements)})

    u1src = next((e for e in elements if e.get("type") == "source_component" and e.get("name") == "U1"), {})
    u1comp = next((e for e in elements if e.get("type") == "pcb_component" and e.get("source_component_id") == u1src.get("source_component_id")), {})
    u1pads = [e for e in elements if e.get("type") == "pcb_smtpad" and e.get("pcb_component_id") == u1comp.get("pcb_component_id")]
    correct = len(u1pads) == 8
    for p in u1pads:
        try:
            n = int(p["port_hints"][0])
            x = -10.905 + (n-1)*1.27 if n <= 4 else -7.095 - (n-5)*1.27
            y = -1.2 if n <= 4 else 4.2
            correct = correct and 1 <= n <= 8 and all(abs(u-v)<1e-6 for u,v in [(p["x"],x),(p["y"],y),(p["width"],0.6),(p["height"],1.55),(p.get("soldermask_margin",0),0.075)])
        except (KeyError,ValueError,TypeError):
            correct = False
    if correct:
        report.passed("U1-001", section, "U1 matches TI D0008A: 1.27 mm pitch, 5.40 mm rows, 1.55 x 0.60 mm pads, 0.075 mm mask expansion")
    else:
        report.failed("U1-001", section, "U1 manufacturer land-pattern assertion failed", u1pads)

    counts = Counter(item.get("type") for item in elements)
    expected_counts = manifest["circuit_counts"]
    count_failures: dict[str, dict[str, int]] = {}
    for kind, expected in expected_counts.items():
        if kind == "unowned_pcb_smtpad":
            actual = sum(
                1
                for item in elements
                if item.get("type") == "pcb_smtpad" and item.get("pcb_component_id") is None
            )
        else:
            actual = counts.get(kind, 0)
        if actual != expected:
            count_failures[kind] = {"expected": expected, "actual": actual}
    if count_failures:
        report.failed("CIR-002", section, "frozen structural counts differ", count_failures)
    else:
        report.passed("CIR-002", section, "all frozen structural counts match", expected_counts)

    errors = [item for item in elements if str(item.get("type", "")).endswith("_error")]
    if errors:
        report.failed(
            "CIR-003",
            section,
            f"circuit contains {len(errors)} explicit PCB errors",
            [{"type": item.get("type"), "message": item.get("message")} for item in errors],
        )
    else:
        report.passed("CIR-003", section, "zero explicit circuit/PCB errors")

    ignored = [item for item in elements if item.get("type") == "source_property_ignored_warning"]
    if ignored:
        report.failed(
            "CIR-004",
            section,
            "one or more requested source properties were ignored",
            [item.get("message") for item in ignored],
        )
    else:
        report.passed("CIR-004", section, "no source properties were ignored")

    source_components = [item for item in elements if item.get("type") == "source_component"]
    source_by_ref: dict[str, dict[str, Any]] = {}
    duplicate_refs: list[str] = []
    for item in source_components:
        ref = str(item.get("name", ""))
        if ref in source_by_ref:
            duplicate_refs.append(ref)
        source_by_ref[ref] = item
    expected_components = manifest["components"]
    actual_refs = set(source_by_ref)
    expected_refs = set(expected_components)
    if duplicate_refs or actual_refs != expected_refs:
        report.failed(
            "CMP-001",
            section,
            "component designator set is not frozen set",
            {
                "duplicates": sorted(set(duplicate_refs)),
                "missing": sorted(expected_refs - actual_refs),
                "unexpected": sorted(actual_refs - expected_refs),
            },
        )
    else:
        report.passed("CMP-001", section, f"exact frozen component set present ({len(expected_refs)} refs)")

    pcb_components = [item for item in elements if item.get("type") == "pcb_component"]
    pcb_by_source = {item.get("source_component_id"): item for item in pcb_components}
    pads_by_component: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in elements:
        if item.get("type") in {"pcb_smtpad", "pcb_plated_hole"} and item.get("pcb_component_id"):
            pads_by_component[str(item["pcb_component_id"])].append(item)

    component_mismatches: list[dict[str, Any]] = []
    mount_mismatches: list[dict[str, Any]] = []
    dnp_mismatches: list[dict[str, Any]] = []
    for ref in sorted(expected_refs & actual_refs):
        expected = expected_components[ref]
        actual = source_by_ref[ref]
        for field in ("ftype",):
            if actual.get(field) != expected[field]:
                component_mismatches.append(
                    {"ref": ref, "field": field, "expected": expected[field], "actual": actual.get(field)}
                )
        value_field = expected["value_field"]
        expected_value = expected["value"]
        actual_value = actual.get(value_field)
        same_value = close(actual_value, expected_value) if isinstance(expected_value, (int, float)) else actual_value == expected_value
        if not same_value:
            component_mismatches.append(
                {"ref": ref, "field": value_field, "expected": expected_value, "actual": actual_value}
            )
        if actual.get("manufacturer_part_number") != expected["mpn"]:
            component_mismatches.append(
                {
                    "ref": ref,
                    "field": "manufacturer_part_number",
                    "expected": expected["mpn"],
                    "actual": actual.get("manufacturer_part_number"),
                }
            )
        pcb = pcb_by_source.get(actual.get("source_component_id"))
        if pcb is None:
            mount_mismatches.append({"ref": ref, "error": "missing pcb_component"})
            continue
        pads = pads_by_component.get(str(pcb.get("pcb_component_id")), [])
        kinds = {pad.get("type") for pad in pads}
        actual_mount = "SMT" if kinds == {"pcb_smtpad"} else "THT" if kinds == {"pcb_plated_hole"} else "MIXED_OR_EMPTY"
        if actual_mount != expected["mount"]:
            mount_mismatches.append({"ref": ref, "expected": expected["mount"], "actual": actual_mount})
        if bool(pcb.get("do_not_place", False)) != bool(expected["dnp"]):
            dnp_mismatches.append(
                {"ref": ref, "expected": expected["dnp"], "actual": bool(pcb.get("do_not_place", False))}
            )
    if component_mismatches:
        report.failed("CMP-002", section, "component value/MPN/type mismatches", component_mismatches)
    else:
        report.passed("CMP-002", section, "all component types, values, and MPNs match frozen design")
    if mount_mismatches:
        report.failed("CMP-003", section, "SMT/THT physical implementation mismatches", mount_mismatches)
    else:
        report.passed("CMP-003", section, "every component has the expected SMT/THT pad technology")
    if dnp_mismatches:
        report.failed("CMP-004", section, "DNP flags differ from frozen design", dnp_mismatches)
    else:
        report.passed("CMP-004", section, "exact DNP flags are present")

    source_ports = [item for item in elements if item.get("type") == "source_port"]
    ports_by_source_component: dict[str, list[dict[str, Any]]] = defaultdict(list)
    port_by_endpoint: dict[str, dict[str, Any]] = {}
    source_ref_by_id = {item["source_component_id"]: item["name"] for item in source_components}
    for port in source_ports:
        component_id = str(port.get("source_component_id"))
        ports_by_source_component[component_id].append(port)
        ref = source_ref_by_id.get(component_id)
        if ref is not None and port.get("pin_number") is not None:
            port_by_endpoint[f"{ref}.{int(port['pin_number'])}"] = port

    pin_label_failures: list[dict[str, Any]] = []
    for ref, expected_pins in manifest["critical_pin_labels"].items():
        component = source_by_ref.get(ref)
        if not component:
            continue
        actual = {
            str(int(port["pin_number"])): str(port.get("name"))
            for port in ports_by_source_component.get(component["source_component_id"], [])
            if port.get("pin_number") is not None
        }
        if actual != expected_pins:
            pin_label_failures.append({"ref": ref, "expected": expected_pins, "actual": actual})
    if pin_label_failures:
        report.failed("PIN-001", section, "critical source pin labels/numbers differ", pin_label_failures)
    else:
        report.passed("PIN-001", section, "critical IC/transistor/diode/connector pin maps match")

    pad_mapping_failures: list[dict[str, Any]] = []
    for ref, component in source_by_ref.items():
        pcb = pcb_by_source.get(component.get("source_component_id"))
        if pcb is None:
            continue
        physical_pins: set[str] = set()
        for pad in pads_by_component.get(str(pcb.get("pcb_component_id")), []):
            physical_pins.update(
                pin
                for pin in (normalize_pin_hint(hint) for hint in pad.get("port_hints", []))
                if pin is not None
            )
        logical_pins = {
            str(int(port["pin_number"]))
            for port in ports_by_source_component.get(component["source_component_id"], [])
            if port.get("pin_number") is not None
        }
        if logical_pins != physical_pins:
            pad_mapping_failures.append(
                {
                    "ref": ref,
                    "logical_pins": sorted(logical_pins, key=int),
                    "physical_pad_hints": sorted(physical_pins, key=int),
                    "missing_on_physical_pads": sorted(logical_pins - physical_pins, key=int),
                    "unexpected_physical_pins": sorted(physical_pins - logical_pins, key=int),
                }
            )
    if pad_mapping_failures:
        report.failed(
            "PIN-002",
            section,
            "logical pins are not fully mapped to numbered physical pads",
            pad_mapping_failures,
        )
    else:
        report.passed("PIN-002", section, "every logical pin maps to exactly the expected physical pin set")

    net_names_by_key = {
        item.get("subcircuit_connectivity_map_key"): item.get("name")
        for item in elements
        if item.get("type") == "source_net"
    }
    endpoints_by_key: dict[str, set[str]] = defaultdict(set)
    for endpoint, port in port_by_endpoint.items():
        key = port.get("subcircuit_connectivity_map_key")
        if key is not None:
            endpoints_by_key[str(key)].add(endpoint)
    topology_failures: list[dict[str, Any]] = []
    group_to_key: dict[str, str] = {}
    named_topologies = set(net_names_by_key.values())
    for group, expected_endpoints_list in manifest["topology"].items():
        expected_endpoints = set(expected_endpoints_list)
        missing = sorted(expected_endpoints - set(port_by_endpoint))
        if missing:
            topology_failures.append({"group": group, "missing_endpoints": missing})
            continue
        keys = {str(port_by_endpoint[endpoint].get("subcircuit_connectivity_map_key")) for endpoint in expected_endpoints}
        if len(keys) != 1:
            topology_failures.append({"group": group, "error": "endpoints split across nets", "keys": sorted(keys)})
            continue
        key = next(iter(keys))
        group_to_key[group] = key
        actual_endpoints = endpoints_by_key.get(key, set())
        if actual_endpoints != expected_endpoints:
            topology_failures.append(
                {
                    "group": group,
                    "missing": sorted(expected_endpoints - actual_endpoints),
                    "unexpected": sorted(actual_endpoints - expected_endpoints),
                }
            )
        if group in named_topologies and net_names_by_key.get(key) != group:
            topology_failures.append(
                {"group": group, "error": "named net mismatch", "actual_net_name": net_names_by_key.get(key)}
            )
    if topology_failures:
        report.failed("NET-001", section, "frozen topology differs", topology_failures)
    else:
        report.passed("NET-001", section, f"all {len(manifest['topology'])} frozen connectivity groups match exactly")

    endpoint_by_port_id = {
        str(port.get("source_port_id")): endpoint for endpoint, port in port_by_endpoint.items()
    }
    actual_internal_connections: set[frozenset[str]] = set()
    malformed_internal: list[dict[str, Any]] = []
    for connection in (item for item in elements if item.get("type") == "source_component_internal_connection"):
        endpoints = [endpoint_by_port_id.get(str(port_id)) for port_id in connection.get("source_port_ids", [])]
        if len(endpoints) != 2 or any(endpoint is None for endpoint in endpoints):
            malformed_internal.append({"connection": connection.get("source_component_internal_connection_id"), "endpoints": endpoints})
        else:
            actual_internal_connections.add(frozenset(str(endpoint) for endpoint in endpoints))
    expected_internal_connections = {
        frozenset(str(endpoint) for endpoint in connection)
        for connection in manifest.get("internal_connections", [])
    }
    if malformed_internal or actual_internal_connections != expected_internal_connections:
        report.failed(
            "NET-002",
            section,
            "component-internal switch connections differ",
            {
                "malformed": malformed_internal,
                "expected": sorted(sorted(connection) for connection in expected_internal_connections),
                "actual": sorted(sorted(connection) for connection in actual_internal_connections),
            },
        )
    else:
        report.passed("NET-002", section, "PRIME switch internal pole pairs are exactly 1-2 and 3-4")

    source_traces = [item for item in elements if item.get("type") == "source_trace"]
    trace_endpoints_by_id: dict[str, frozenset[str]] = {}
    traces_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    trace_tree_failures: list[dict[str, Any]] = []
    for trace in source_traces:
        trace_id = str(trace.get("source_trace_id"))
        endpoints = [endpoint_by_port_id.get(str(port_id)) for port_id in trace.get("connected_source_port_ids", [])]
        if len(endpoints) != 2 or any(endpoint is None for endpoint in endpoints) or len(set(endpoints)) != 2:
            trace_tree_failures.append({"trace": trace_id, "error": "trace is not one valid two-terminal edge", "endpoints": endpoints})
            continue
        edge = frozenset(str(endpoint) for endpoint in endpoints)
        trace_endpoints_by_id[trace_id] = edge
        traces_by_key[str(trace.get("subcircuit_connectivity_map_key"))].append(trace)
    expected_source_trace_count = sum(len(endpoints) - 1 for endpoints in manifest["topology"].values())
    if len(source_traces) != expected_source_trace_count:
        trace_tree_failures.append(
            {"error": "N-1 tree total differs", "expected_source_traces": expected_source_trace_count, "actual_source_traces": len(source_traces)}
        )
    expected_keys = set(group_to_key.values())
    unexpected_trace_keys = sorted(set(traces_by_key) - expected_keys)
    if unexpected_trace_keys:
        trace_tree_failures.append({"error": "traces use connectivity keys outside frozen groups", "keys": unexpected_trace_keys})
    for group, expected_list in manifest["topology"].items():
        expected_endpoints = set(expected_list)
        key = group_to_key.get(group)
        if key is None:
            trace_tree_failures.append({"group": group, "error": "no unique connectivity key"})
            continue
        traces = traces_by_key.get(key, [])
        edges = [trace_endpoints_by_id.get(str(trace.get("source_trace_id")), frozenset()) for trace in traces]
        bad_edges = [sorted(edge) for edge in edges if len(edge) != 2 or not set(edge).issubset(expected_endpoints)]
        duplicate_edges = len(edges) != len(set(edges))
        adjacency: dict[str, set[str]] = defaultdict(set)
        for edge in edges:
            if len(edge) != 2:
                continue
            first, second = tuple(edge)
            adjacency[first].add(second)
            adjacency[second].add(first)
        visited: set[str] = set()
        if expected_endpoints:
            stack = [next(iter(expected_endpoints))]
            while stack:
                endpoint = stack.pop()
                if endpoint in visited:
                    continue
                visited.add(endpoint)
                stack.extend(adjacency.get(endpoint, set()) - visited)
        if len(edges) != len(expected_endpoints) - 1 or bad_edges or duplicate_edges or visited != expected_endpoints:
            trace_tree_failures.append(
                {
                    "group": group,
                    "expected_edges": len(expected_endpoints) - 1,
                    "actual_edges": len(edges),
                    "bad_edges": bad_edges,
                    "duplicate_edges": duplicate_edges,
                    "unreached_endpoints": sorted(expected_endpoints - visited),
                }
            )
    if trace_tree_failures:
        report.failed("NET-003", section, "source traces are not exact cycle-free N-1 connectivity trees", trace_tree_failures)
    else:
        report.passed(
            "NET-003",
            section,
            f"all {len(manifest['topology'])} groups are explicit two-terminal N-1 trees ({expected_source_trace_count} edges)",
        )

    traces_by_edge: dict[frozenset[str], list[dict[str, Any]]] = defaultdict(list)
    for trace in source_traces:
        edge = trace_endpoints_by_id.get(str(trace.get("source_trace_id")))
        if edge:
            traces_by_edge[edge].append(trace)
    critical_trace_records: dict[frozenset[str], dict[str, Any]] = {}
    source_width_failures: list[dict[str, Any]] = []
    for specification in manifest["critical_source_edges"]:
        edge = frozenset(str(endpoint) for endpoint in specification["endpoints"])
        expected_width = float(specification["width_mm"])
        matching = traces_by_edge.get(edge, [])
        trace = matching[0] if len(matching) == 1 else None
        actual = None if trace is None else trace.get("min_trace_thickness")
        if trace is None or not close(actual, expected_width):
            source_width_failures.append(
                {"edge": sorted(edge), "matches": len(matching), "expected_mm": expected_width, "actual_mm": actual}
            )
        else:
            critical_trace_records[edge] = trace
    if source_width_failures:
        report.failed("TRC-001", section, "critical source trace-width constraints differ", source_width_failures)
    else:
        report.passed("TRC-001", section, "all pump/high-current source trace-width constraints match")

    boards = [item for item in elements if item.get("type") == "pcb_board"]
    board = boards[0] if len(boards) == 1 else None
    board_failures: list[dict[str, Any]] = []
    expected_board = manifest["board"]
    board_fields = {
        "width": expected_board["width_mm"],
        "height": expected_board["height_mm"],
        "thickness": expected_board["thickness_mm"],
        "num_layers": expected_board["copper_layers"],
        "material": expected_board["material"],
    }
    if board is None:
        board_failures.append({"error": f"expected one pcb_board, found {len(boards)}"})
    else:
        for field, expected in board_fields.items():
            actual = board.get(field)
            same = close(actual, expected) if isinstance(expected, (int, float)) else str(actual).lower() == str(expected).lower()
            if not same:
                board_failures.append({"field": field, "expected": expected, "actual": actual})
        minimums = {
            "min_trace_width": expected_board["min_trace_width_mm"],
            "min_via_hole_diameter": expected_board["min_via_drill_mm"],
            "min_via_pad_diameter": expected_board["min_via_diameter_mm"],
            "min_via_hole_edge_to_via_hole_edge_clearance": expected_board["min_via_drill_edge_clearance_mm"],
            "min_board_edge_clearance": expected_board["min_board_edge_clearance_mm"],
        }
        for field, minimum in minimums.items():
            actual = board.get(field)
            if actual is None or float(actual) + EPS < minimum:
                board_failures.append({"field": field, "minimum": minimum, "actual": actual})
    if board_failures:
        report.failed("BRD-001", section, "board stack/dimensions/design-rule floor differ", board_failures)
    else:
        report.passed("BRD-001", section, "board is exactly 50 x 40 x 1.6 mm, two-layer FR-4 with frozen rule floors")

    holes = [item for item in elements if item.get("type") == "pcb_hole"]
    unmatched_holes = list(holes)
    hole_failures: list[dict[str, Any]] = []
    for expected in expected_board["mounting_holes"]:
        candidates = [
            hole
            for hole in unmatched_holes
            if close(hole.get("x"), expected["x"])
            and close(hole.get("y"), expected["y"])
            and close(hole.get("hole_diameter"), expected["diameter"])
            and hole.get("hole_shape") == "circle"
        ]
        if len(candidates) != 1:
            hole_failures.append({"expected": expected, "matches": len(candidates)})
        else:
            unmatched_holes.remove(candidates[0])
    if unmatched_holes:
        hole_failures.append({"unexpected_holes": unmatched_holes})
    if hole_failures:
        report.failed("BRD-002", section, "mounting holes differ from frozen 3.2 mm NPTH pattern", hole_failures)
    else:
        report.passed("BRD-002", section, "four 3.2 mm mounting holes match the 43 x 33 mm pattern")

    keepouts = [item for item in elements if item.get("type") == "pcb_keepout"]
    keepout_failures: list[dict[str, Any]] = []
    for expected in expected_board["mounting_holes"]:
        matches = [
            keepout
            for keepout in keepouts
            if close(keepout.get("center", {}).get("x"), expected["x"])
            and close(keepout.get("center", {}).get("y"), expected["y"])
        ]
        if len(matches) != 1:
            keepout_failures.append({"hole": expected, "matching_keepouts": len(matches)})
            continue
        keepout = matches[0]
        if keepout.get("shape") != "circle" or not close(keepout.get("radius"), expected_board["keepout_radius_mm"]):
            keepout_failures.append({"hole": expected, "shape": keepout.get("shape"), "radius": keepout.get("radius")})
        layers = {str(layer).lower() for layer in keepout.get("layers", [])}
        required_layers = {str(layer).lower() for layer in expected_board["keepout_layers"]}
        if not required_layers.issubset(layers):
            keepout_failures.append(
                {"hole": expected, "required_layers": sorted(required_layers), "actual_layers": sorted(layers)}
            )
    if keepout_failures:
        report.failed("BRD-003", section, "mounting-hole keepouts do not protect both copper layers", keepout_failures)
    else:
        report.passed("BRD-003", section, "3.0 mm-radius keepouts protect every mounting hole on both layers")

    pcb_traces = [item for item in elements if item.get("type") == "pcb_trace"]
    if not pcb_traces:
        report.failed("TRC-002", section, "zero routed pcb_trace elements; fabrication cannot proceed")
    else:
        report.passed("TRC-002", section, f"routed PCB trace objects present ({len(pcb_traces)})")
    route_width_failures: list[dict[str, Any]] = []
    min_route_width = math.inf
    for trace in pcb_traces:
        for point in trace.get("route", []):
            if point.get("route_type") == "wire" and point.get("width") is not None:
                width = float(point["width"])
                min_route_width = min(min_route_width, width)
                if width + EPS < expected_board["min_trace_width_mm"]:
                    route_width_failures.append({"pcb_trace_id": trace.get("pcb_trace_id"), "width_mm": width})
    if route_width_failures:
        report.failed("TRC-003", section, "one or more routed wires are below 0.20 mm", route_width_failures)
    elif pcb_traces:
        report.passed("TRC-003", section, "all routed wire widths meet the 0.20 mm floor", {"minimum_mm": min_route_width})
    else:
        report.failed("TRC-003", section, "trace-width check cannot pass without routed traces")

    trace_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for trace in pcb_traces:
        if trace.get("source_trace_id"):
            trace_by_source[str(trace["source_trace_id"])].append(trace)
    critical_route_failures: list[dict[str, Any]] = []
    for specification in manifest["critical_source_edges"]:
        edge = frozenset(str(endpoint) for endpoint in specification["endpoints"])
        minimum = float(specification["width_mm"])
        source_trace = critical_trace_records.get(edge)
        routed = [] if source_trace is None else trace_by_source.get(str(source_trace.get("source_trace_id")), [])
        widths = [
            float(point["width"])
            for trace in routed
            for point in trace.get("route", [])
            if point.get("route_type") == "wire" and point.get("width") is not None
        ]
        if not widths or min(widths) + EPS < minimum:
            critical_route_failures.append(
                {"edge": sorted(edge), "minimum_mm": minimum, "actual_minimum_mm": min(widths) if widths else None}
            )
    if critical_route_failures:
        report.failed("TRC-004", section, "high-current nets are absent or routed below their frozen widths", critical_route_failures)
    else:
        report.passed("TRC-004", section, "all high-current routes meet their 1.0/1.2 mm constraints")

    pcb_vias = [item for item in elements if item.get("type") == "pcb_via"]
    critical_via_failures: list[dict[str, Any]] = []
    for specification in manifest["critical_source_edges"]:
        edge = frozenset(str(endpoint) for endpoint in specification["endpoints"])
        source_trace = critical_trace_records.get(edge)
        routed = [] if source_trace is None else trace_by_source.get(str(source_trace.get("source_trace_id")), [])
        if not routed:
            critical_via_failures.append({"edge": sorted(edge), "error": "critical edge has no routed PCB trace"})
            continue
        vias_for_edge = trace_via_inventory(routed, pcb_vias)
        policy = specification.get("via_policy", {"mode": "via_free"})
        mode = policy.get("mode")
        if mode == "via_free" and vias_for_edge:
            critical_via_failures.append(
                {
                    "edge": sorted(edge),
                    "width_mm": specification["width_mm"],
                    "error": "critical current path changes layers through series vias",
                    "via_count": len(vias_for_edge),
                    "vias": vias_for_edge,
                }
            )
        elif mode == "parallel_bank_bottom_ground_pour":
            source_key = str(source_trace.get("subcircuit_connectivity_map_key"))
            frozen_gnd_key = group_to_key.get("GND")
            if frozen_gnd_key is None or source_key != frozen_gnd_key:
                critical_via_failures.append({"edge": sorted(edge), "error": "parallel-bank exception is allowed only on GND"})
                continue
            tolerance = float(policy.get("coordinate_tolerance_mm", 0.0))
            minimum_bank = int(policy.get("minimum_vias_per_transition", 3))
            minimum_pad_edge = float(policy.get("minimum_pad_edge_clearance_mm", -1.0))
            expected_bottom_points = int(policy.get("expected_distinct_bottom_route_points", -1))
            try:
                expected_via_points = [
                    (float(point[0]), float(point[1])) for point in policy["expected_via_coordinates"]
                ]
                expected_transition_points = [
                    (float(point[0]), float(point[1])) for point in policy["expected_transition_coordinates"]
                ]
            except (KeyError, TypeError, ValueError, IndexError):
                expected_via_points = []
                expected_transition_points = []
            if (
                tolerance <= 0
                or minimum_bank < 3
                or len(expected_via_points) != minimum_bank
                or not expected_transition_points
                or minimum_pad_edge < 0
                or expected_bottom_points < 1
            ):
                critical_via_failures.append({"edge": sorted(edge), "error": "invalid bank policy parameters", "policy": policy})
                continue

            # A route point records the logical layer transition; the other frozen
            # vias are explicit parallel copper paths.  Check each set separately
            # and exactly, rather than treating nearby unrelated GND vias as bank
            # members.
            actual_transition_points = sorted(
                {
                    (round(float(point["x"]), 6), round(float(point["y"]), 6))
                    for trace in routed
                    for point in trace.get("route", [])
                    if point.get("route_type") == "via"
                }
            )

            def coordinate_sets_match(
                actual: Sequence[tuple[float, float]], expected: Sequence[tuple[float, float]]
            ) -> bool:
                if len(actual) != len(expected):
                    return False
                unmatched = list(actual)
                for target in expected:
                    matches = [
                        candidate
                        for candidate in unmatched
                        if math.hypot(candidate[0] - target[0], candidate[1] - target[1]) <= tolerance + EPS
                    ]
                    if len(matches) != 1:
                        return False
                    unmatched.remove(matches[0])
                return not unmatched

            if not coordinate_sets_match(actual_transition_points, expected_transition_points):
                critical_via_failures.append(
                    {
                        "edge": sorted(edge),
                        "error": "logical layer-transition coordinates differ from the frozen exception",
                        "expected": expected_transition_points,
                        "actual": actual_transition_points,
                        "tolerance_mm": tolerance,
                    }
                )

            flat_bank_vias: list[dict[str, Any]] = []
            matched_ids: set[str] = set()
            for expected_point in expected_via_points:
                candidates = [
                    via
                    for via in pcb_vias
                    if str(via.get("subcircuit_connectivity_map_key")) == source_key
                    and math.hypot(float(via["x"]) - expected_point[0], float(via["y"]) - expected_point[1])
                    <= tolerance + EPS
                ]
                if len(candidates) != 1:
                    critical_via_failures.append(
                        {
                            "edge": sorted(edge),
                            "expected_coordinate": expected_point,
                            "error": "frozen bank coordinate does not resolve to exactly one GND via",
                            "matches": [via.get("pcb_via_id") for via in candidates],
                        }
                    )
                    continue
                via_id = str(candidates[0].get("pcb_via_id"))
                if via_id in matched_ids:
                    critical_via_failures.append(
                        {"edge": sorted(edge), "error": "one physical via satisfies multiple frozen bank coordinates", "via": via_id}
                    )
                    continue
                matched_ids.add(via_id)
                flat_bank_vias.append(candidates[0])
            if len(flat_bank_vias) != minimum_bank:
                critical_via_failures.append(
                    {
                        "edge": sorted(edge),
                        "error": "parallel via bank is not the exact frozen size",
                        "expected": minimum_bank,
                        "actual": len(flat_bank_vias),
                    }
                )
            for via in flat_bank_vias:
                drill = via.get("hole_diameter", via.get("drill_diameter"))
                diameter = via.get("outer_diameter", via.get("diameter"))
                if drill is None or float(drill) + EPS < expected_board["min_via_drill_mm"] or diameter is None or float(diameter) + EPS < expected_board["min_via_diameter_mm"]:
                    critical_via_failures.append({"edge": sorted(edge), "error": "bank via geometry is undersized", "via": via})
            for first_index, first in enumerate(flat_bank_vias):
                for second in flat_bank_vias[first_index + 1 :]:
                    center_distance = math.hypot(float(first["x"]) - float(second["x"]), float(first["y"]) - float(second["y"]))
                    drill_first = float(first.get("hole_diameter", first.get("drill_diameter", 0)))
                    drill_second = float(second.get("hole_diameter", second.get("drill_diameter", 0)))
                    diameter_first = float(first.get("outer_diameter", first.get("diameter", 0)))
                    diameter_second = float(second.get("outer_diameter", second.get("diameter", 0)))
                    drill_edge = center_distance - (drill_first + drill_second) / 2
                    pad_edge = center_distance - (diameter_first + diameter_second) / 2
                    if drill_edge + EPS < expected_board["min_via_drill_edge_clearance_mm"]:
                        critical_via_failures.append(
                            {"edge": sorted(edge), "error": "bank drill-to-drill edge clearance is too small", "actual_mm": drill_edge}
                        )
                    if pad_edge + EPS < minimum_pad_edge:
                        critical_via_failures.append(
                            {
                                "edge": sorted(edge),
                                "error": "bank pad-to-pad edge clearance is below the frozen minimum",
                                "minimum_mm": minimum_pad_edge,
                                "actual_mm": pad_edge,
                            }
                        )
            top_segments: list[tuple[tuple[float, float], tuple[float, float], float]] = []
            bottom_points: list[tuple[float, float]] = []
            for trace in routed:
                route = trace.get("route", [])
                bottom_points.extend(
                    (float(point["x"]), float(point["y"]))
                    for point in route
                    if point.get("route_type") == "wire" and point.get("layer") == "bottom"
                )
                for first, second in zip(route, route[1:]):
                    if first.get("route_type") == "wire" and second.get("route_type") == "wire" and first.get("layer") == second.get("layer") == "top":
                        top_segments.append(
                            (
                                (float(first["x"]), float(first["y"])),
                                (float(second["x"]), float(second["y"])),
                                min(float(first.get("width", 0)), float(second.get("width", 0))),
                            )
                        )
            distinct_bottom_points = sorted({(round(point[0], 6), round(point[1], 6)) for point in bottom_points})
            if len(distinct_bottom_points) != expected_bottom_points:
                critical_via_failures.append(
                    {
                        "edge": sorted(edge),
                        "error": "distinct bottom-route point count differs from the frozen geometry",
                        "expected": expected_bottom_points,
                        "actual": len(distinct_bottom_points),
                        "points": distinct_bottom_points,
                    }
                )
            for via in flat_bank_vias:
                center = (float(via["x"]), float(via["y"]))
                pad_radius = float(via.get("outer_diameter", via.get("diameter", 0))) / 2
                if not any(distance_point_segment(center, first, second) <= width / 2 + pad_radius + EPS for first, second, width in top_segments):
                    critical_via_failures.append({"edge": sorted(edge), "error": "bank via does not overlap continuous top-route copper", "via": via.get("pcb_via_id")})
            bottom_gnd_pours = [
                pour
                for pour in elements
                if pour.get("type") == "pcb_copper_pour"
                and str(pour.get("layer")).lower() == "bottom"
                and str(pour.get("subcircuit_connectivity_map_key")) == frozen_gnd_key
            ]
            if len(bottom_gnd_pours) != 1:
                critical_via_failures.append(
                    {
                        "edge": sorted(edge),
                        "error": "frozen bank requires exactly one bottom GND copper-pour BREP",
                        "actual": len(bottom_gnd_pours),
                    }
                )
            required_pour_points = distinct_bottom_points + [(float(via["x"]), float(via["y"])) for via in flat_bank_vias]
            continuous_pours = [
                pour for pour in bottom_gnd_pours if required_pour_points and all(copper_pour_contains(pour, point) for point in required_pour_points)
            ]
            if not continuous_pours:
                critical_via_failures.append(
                    {
                        "edge": sorted(edge),
                        "error": "no single connected bottom GND-pour BREP contains all bottom-route and bank-via points",
                        "bottom_route_points": len(bottom_points),
                        "bank_vias": len(flat_bank_vias),
                    }
                )
        elif mode == "unrestricted_non_load":
            if specification.get("classification") != "non_load_test_branch":
                critical_via_failures.append(
                    {"edge": sorted(edge), "error": "unrestricted via policy requires explicit non-load test-branch classification"}
                )
        elif mode not in {"via_free", "parallel_bank_bottom_ground_pour", "unrestricted_non_load"}:
            critical_via_failures.append({"edge": sorted(edge), "error": "unknown via policy", "policy": policy})
    if critical_via_failures:
        report.failed(
            "TRC-005",
            section,
            "frozen via policy failed; load paths must be via-free unless an exact GND bank+continuous-pour exception is frozen",
            critical_via_failures,
        )
    else:
        report.passed("TRC-005", section, "all load-current paths satisfy their frozen via policy; non-load test branches are explicitly classified")

    via_failures: list[dict[str, Any]] = []
    for via in pcb_vias:
        drill = via.get("hole_diameter", via.get("drill_diameter"))
        diameter = via.get("outer_diameter", via.get("diameter"))
        if drill is None or float(drill) + EPS < expected_board["min_via_drill_mm"]:
            via_failures.append({"via": via.get("pcb_via_id"), "field": "drill", "actual": drill})
        if diameter is None or float(diameter) + EPS < expected_board["min_via_diameter_mm"]:
            via_failures.append({"via": via.get("pcb_via_id"), "field": "diameter", "actual": diameter})
    if len(pcb_vias) > 300:
        via_failures.append({"error": "implausible via count", "count": len(pcb_vias), "maximum": 300})
    if via_failures:
        report.failed("VIA-001", section, "via geometry/count violates frozen limits", via_failures)
    else:
        report.passed("VIA-001", section, "via geometry/count is within frozen limits", {"count": len(pcb_vias)})

    copper_clearance_failures: list[dict[str, Any]] = []
    required_clearance = expected_board["min_copper_to_hole_edge_mm"]
    for hole in holes:
        center = (float(hole["x"]), float(hole["y"]))
        required_radius = float(hole["hole_diameter"]) / 2 + required_clearance
        for pour in (item for item in elements if item.get("type") == "pcb_copper_pour"):
            shape = pour.get("brep_shape", {})
            outer = shape.get("outer_ring", {}).get("vertices", [])
            if not point_in_polygon(center, outer):
                continue
            enclosing_voids = [
                ring.get("vertices", [])
                for ring in shape.get("inner_rings", [])
                if point_in_polygon(center, ring.get("vertices", []))
            ]
            if not enclosing_voids:
                copper_clearance_failures.append(
                    {"hole": center, "layer": pour.get("layer"), "error": "copper pour has no enclosing void"}
                )
            else:
                clearance_radius = max(distance_to_ring(center, vertices) for vertices in enclosing_voids)
                if clearance_radius + EPS < required_radius:
                    copper_clearance_failures.append(
                        {
                            "hole": center,
                            "layer": pour.get("layer"),
                            "required_copper_free_radius_mm": required_radius,
                            "actual_copper_free_radius_mm": round(clearance_radius, 6),
                        }
                    )
        for trace in pcb_traces:
            wires = [point for point in trace.get("route", []) if point.get("route_type") == "wire"]
            for first, second in zip(wires, wires[1:]):
                width = max(float(first.get("width", 0)), float(second.get("width", 0)))
                distance = distance_point_segment(
                    center,
                    (float(first["x"]), float(first["y"])),
                    (float(second["x"]), float(second["y"])),
                ) - width / 2
                if distance + EPS < required_radius:
                    copper_clearance_failures.append(
                        {"hole": center, "pcb_trace_id": trace.get("pcb_trace_id"), "edge_distance_mm": round(distance, 6)}
                    )
                    break
        for copper in (
            item
            for item in elements
            if item.get("type") in {"pcb_smtpad", "pcb_plated_hole", "pcb_via"}
            and item.get("x") is not None
            and item.get("y") is not None
        ):
            edge_distance = math.hypot(float(copper["x"]) - center[0], float(copper["y"]) - center[1]) - copper_radius(copper)
            if edge_distance + EPS < required_radius:
                copper_clearance_failures.append(
                    {
                        "hole": center,
                        "copper_type": copper.get("type"),
                        "copper_id": next((value for key, value in copper.items() if key.endswith("_id") and key.startswith("pcb_")), None),
                        "edge_distance_mm": round(edge_distance, 6),
                    }
                )
    if copper_clearance_failures:
        report.failed(
            "BRD-004",
            section,
            "copper is closer than 1.0 mm to a mounting-hole edge",
            copper_clearance_failures,
        )
    else:
        report.passed("BRD-004", section, "circuit geometry preserves 1.0 mm copper-to-mounting-hole-edge clearance")

    edge_failures: list[dict[str, Any]] = []
    if board is not None:
        half_w, half_h = float(board["width"]) / 2, float(board["height"]) / 2
        edge_clearance = expected_board["min_board_edge_clearance_mm"]
        for pour in (item for item in elements if item.get("type") == "pcb_copper_pour"):
            for vertex in pour.get("brep_shape", {}).get("outer_ring", {}).get("vertices", []):
                if abs(float(vertex["x"])) > half_w - edge_clearance + EPS or abs(float(vertex["y"])) > half_h - edge_clearance + EPS:
                    edge_failures.append({"type": "pour", "id": pour.get("pcb_copper_pour_id"), "vertex": vertex})
                    break
        for trace in pcb_traces:
            for point in trace.get("route", []):
                if point.get("route_type") != "wire":
                    continue
                radius = float(point.get("width", 0)) / 2
                if abs(float(point["x"])) + radius > half_w - edge_clearance + EPS or abs(float(point["y"])) + radius > half_h - edge_clearance + EPS:
                    edge_failures.append({"type": "trace", "id": trace.get("pcb_trace_id"), "point": point})
                    break
        for copper in (
            item
            for item in elements
            if item.get("type") in {"pcb_smtpad", "pcb_plated_hole", "pcb_via"}
            and item.get("x") is not None
            and item.get("y") is not None
        ):
            radius = copper_radius(copper)
            if abs(float(copper["x"])) + radius > half_w - edge_clearance + EPS or abs(float(copper["y"])) + radius > half_h - edge_clearance + EPS:
                edge_failures.append(
                    {
                        "type": copper.get("type"),
                        "id": next((value for key, value in copper.items() if key.endswith("_id") and key.startswith("pcb_")), None),
                        "x": copper.get("x"),
                        "y": copper.get("y"),
                        "conservative_radius_mm": round(radius, 6),
                    }
                )
    if edge_failures:
        report.failed("BRD-005", section, "copper violates the 0.5 mm board-edge clearance", edge_failures)
    else:
        report.passed("BRD-005", section, "checked traces, pours, pads, holes, and vias respect 0.5 mm board-edge clearance")

    courtyard_items = [
        item
        for item in elements
        if item.get("type") in {"pcb_courtyard_rect", "pcb_courtyard_outline"}
    ]
    ref_by_pcb_component_id = {
        str(pcb.get("pcb_component_id")): ref
        for ref, source in source_by_ref.items()
        for pcb in [pcb_by_source.get(source.get("source_component_id"))]
        if pcb is not None
    }
    courtyard_failures: list[dict[str, Any]] = []
    courtyard_records: list[dict[str, Any]] = []
    courtyard_ref_counts: Counter[str] = Counter()
    for item in courtyard_items:
        component_id = str(item.get("pcb_component_id"))
        ref = ref_by_pcb_component_id.get(component_id)
        layer = str(item.get("layer", "")).lower()
        try:
            polygon = courtyard_polygon(item)
        except (KeyError, TypeError, ValueError) as exc:
            polygon = []
            courtyard_failures.append(
                {"courtyard": next((value for key, value in item.items() if key.startswith("pcb_courtyard") and key.endswith("_id")), None), "error": f"malformed geometry: {exc}"}
            )
        if ref is None:
            courtyard_failures.append({"pcb_component_id": component_id, "error": "courtyard has no frozen component owner"})
            continue
        courtyard_ref_counts[ref] += 1
        if layer not in {"top", "bottom"}:
            courtyard_failures.append({"ref": ref, "error": "courtyard has unsupported layer", "layer": layer})
        if len(polygon) < 3 or abs(sum(first[0] * second[1] - second[0] * first[1] for first, second in polygon_edges(polygon))) <= EPS:
            courtyard_failures.append({"ref": ref, "error": "courtyard polygon is empty or degenerate"})
            continue
        courtyard_records.append({"ref": ref, "layer": layer, "polygon": polygon})

    actual_courtyard_refs = set(courtyard_ref_counts)
    expected_courtyard_refs = set(manifest["courtyard_refs"])
    if actual_courtyard_refs != expected_courtyard_refs or any(count != 1 for count in courtyard_ref_counts.values()):
        courtyard_failures.append(
            {
                "error": "courtyard ownership set/count differs",
                "missing": sorted(expected_courtyard_refs - actual_courtyard_refs),
                "unexpected": sorted(actual_courtyard_refs - expected_courtyard_refs),
                "non_singleton": {ref: count for ref, count in sorted(courtyard_ref_counts.items()) if count != 1},
            }
        )

    pair_clearances: dict[frozenset[str], float] = {}
    closest_pair: tuple[str, str] | None = None
    closest_clearance = math.inf
    for first_index, first in enumerate(courtyard_records):
        for second in courtyard_records[first_index + 1 :]:
            if first["layer"] != second["layer"] or first["ref"] == second["ref"]:
                continue
            clearance = polygon_clearance(first["polygon"], second["polygon"])
            pair_clearances[frozenset((first["ref"], second["ref"]))] = clearance
            if clearance < closest_clearance:
                closest_clearance = clearance
                closest_pair = (first["ref"], second["ref"])
            if polygons_overlap(first["polygon"], second["polygon"]):
                courtyard_failures.append(
                    {"refs": [first["ref"], second["ref"]], "layer": first["layer"], "error": "courtyards overlap or touch"}
                )

    reviewed_evidence: list[dict[str, Any]] = []
    for requirement in manifest.get("reviewed_courtyard_clearances", []):
        refs = frozenset(str(ref) for ref in requirement["refs"])
        minimum = float(requirement["minimum_mm"])
        actual = pair_clearances.get(refs)
        reviewed_evidence.append({"refs": sorted(refs), "minimum_mm": minimum, "actual_mm": actual})
        if actual is None or actual + EPS < minimum:
            courtyard_failures.append(
                {"refs": sorted(refs), "error": "reviewed courtyard clearance regressed", "minimum_mm": minimum, "actual_mm": actual}
            )

    if courtyard_failures:
        report.failed(
            "PLC-001",
            section,
            "serialized component courtyards overlap, are malformed, or differ from the frozen placement review",
            courtyard_failures,
        )
    else:
        report.passed(
            "PLC-001",
            section,
            "all 40 frozen courtyards are pairwise disjoint and reviewed placement clearances pass",
            {
                "closest_pair": list(closest_pair) if closest_pair else None,
                "closest_clearance_mm": round(closest_clearance, 6) if math.isfinite(closest_clearance) else None,
                "reviewed": reviewed_evidence,
            },
        )

    warning_counts = {
        kind: count
        for kind, count in sorted(counts.items())
        if isinstance(kind, str) and kind.endswith("_warning")
    }
    report.passed("CIR-005", section, "non-fatal warning inventory recorded", warning_counts)

    positions: dict[str, dict[str, Any]] = {}
    for ref, component in source_by_ref.items():
        pcb = pcb_by_source.get(component.get("source_component_id"))
        if pcb:
            positions[ref] = {
                "x": pcb.get("center", {}).get("x"),
                "y": pcb.get("center", {}).get("y"),
                "rotation": pcb.get("rotation", 0),
                "layer": pcb.get("layer", "top"),
            }
    return {
        "elements": elements,
        "counts": counts,
        "positions": positions,
        "components": source_by_ref,
    }


class FileBundle:
    """Read-only abstraction over a zip archive or a directory."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._zip: zipfile.ZipFile | None = None
        self._directory: Path | None = None
        if path.is_dir():
            self._directory = path
            self.names = sorted(
                candidate.relative_to(path).as_posix()
                for candidate in path.rglob("*")
                if candidate.is_file()
            )
        elif path.is_file() and zipfile.is_zipfile(path):
            self._zip = zipfile.ZipFile(path)
            infos = self._zip.infolist()
            self.names = sorted(info.filename for info in infos if not info.is_dir())
            unsafe = [
                name
                for name in self.names
                if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts
            ]
            duplicates = [name for name, count in Counter(self.names).items() if count > 1]
            if unsafe or duplicates:
                self.close()
                raise ValidationError(
                    f"unsafe/ambiguous archive members: unsafe={unsafe}, duplicates={duplicates}"
                )
        elif path.is_file():
            self._directory = path.parent
            self.names = [path.name]
        else:
            raise ValidationError(f"artifact does not exist: {path}")

    def close(self) -> None:
        if self._zip is not None:
            self._zip.close()

    def __enter__(self) -> "FileBundle":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def read_bytes(self, name: str) -> bytes:
        if self._zip is not None:
            return self._zip.read(name)
        assert self._directory is not None
        if len(self.names) == 1 and (self._directory / name).resolve() != self.path.resolve() and self.path.is_file():
            return self.path.read_bytes()
        return (self._directory / PurePosixPath(name)).read_bytes()

    def read_text(self, name: str) -> str:
        data = self.read_bytes(name)
        if b"\x00" in data[:4096]:
            raise ValidationError(f"binary/NUL data in text artifact {name}")
        return data.decode("utf-8-sig", errors="strict")


def artifact_role(name: str, text: str | None = None) -> str | None:
    base = PurePosixPath(name).name.lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", base).strip("_")
    if text:
        file_function = re.search(r"TF\.FileFunction,([^*%]+)", text, flags=re.I)
        if file_function:
            function = file_function.group(1).lower()
            if "copper,l1" in function or ("copper" in function and "top" in function):
                return "f_cu"
            if "copper,l2" in function or ("copper" in function and ("bot" in function or "bottom" in function)):
                return "b_cu"
            if "soldermask" in function and "top" in function:
                return "f_mask"
            if "soldermask" in function and ("bot" in function or "bottom" in function):
                return "b_mask"
            if "paste" in function and "top" in function:
                return "f_paste"
            if "paste" in function and ("bot" in function or "bottom" in function):
                return "b_paste"
            if "legend" in function and "top" in function:
                return "f_silk"
            if "legend" in function and ("bot" in function or "bottom" in function):
                return "b_silk"
            if "profile" in function:
                return "edge"
    suffix_roles = {
        ".gtl": "f_cu",
        ".gbl": "b_cu",
        ".gts": "f_mask",
        ".gbs": "b_mask",
        ".gtp": "f_paste",
        ".gto": "f_silk",
        ".gm1": "edge",
        ".gko": "edge",
    }
    suffix = Path(base).suffix
    if suffix in suffix_roles:
        return suffix_roles[suffix]
    patterns = [
        ("f_cu", ("f_cu", "top_copper")),
        ("b_cu", ("b_cu", "bottom_copper")),
        ("f_mask", ("f_mask", "top_mask")),
        ("b_mask", ("b_mask", "bottom_mask")),
        ("f_paste", ("f_paste", "top_paste")),
        ("b_paste", ("b_paste", "bottom_paste")),
        ("f_silk", ("f_silk", "f_silkscreen", "top_silk")),
        ("b_silk", ("b_silk", "b_silkscreen", "bottom_silk")),
        ("edge", ("edge_cuts", "outline", "board_profile")),
    ]
    for role, needles in patterns:
        if any(needle in normalized for needle in needles):
            return role
    if suffix in {".drl", ".xln", ".txt"}:
        if "npth" in normalized or "non_plated" in normalized or "nonplated" in normalized:
            return "drill_npth"
        if "drill" in normalized or suffix in {".drl", ".xln"}:
            return "drill_pth"
    if suffix == ".csv":
        if "bom" in normalized:
            return "bom"
        if any(word in normalized for word in ("cpl", "pick_and_place", "pick_place", "centroid", "position")):
            return "cpl"
    return None


def classify_bundle(bundle: FileBundle) -> tuple[dict[str, str], list[str]]:
    roles: dict[str, str] = {}
    duplicates: list[str] = []
    for name in bundle.names:
        text = None
        if Path(name).suffix.lower() in {".gbr", ".ger", ".gtl", ".gbl", ".gts", ".gbs", ".gtp", ".gto", ".gm1", ".gko"}:
            try:
                text = bundle.read_text(name)
            except (OSError, UnicodeError, ValidationError):
                text = None
        role = artifact_role(name, text)
        if role:
            if role in roles:
                duplicates.append(role)
            else:
                roles[role] = name
    return roles, duplicates


def decode_gerber_number(raw: str, decimals: int, unit_scale: float) -> float:
    if "." in raw:
        return float(raw) * unit_scale
    sign = -1 if raw.startswith("-") else 1
    digits = raw.lstrip("+-")
    return sign * int(digits or "0") / (10**decimals) * unit_scale


def gerber_bbox(text: str) -> tuple[float, float, float, float]:
    fs_match = re.search(r"%FS[LT]A?X(\d)(\d)Y(\d)(\d)\*%", text, flags=re.I)
    if not fs_match:
        raise ValidationError("Gerber lacks a supported FS coordinate-format statement")
    x_decimals, y_decimals = int(fs_match.group(2)), int(fs_match.group(4))
    unit_scale = 25.4 if re.search(r"%MOIN\*%", text, flags=re.I) else 1.0
    xs: list[float] = []
    ys: list[float] = []
    current_x: float | None = None
    current_y: float | None = None
    for line in text.splitlines():
        x_match = re.search(r"X([+-]?[0-9.]+)", line, flags=re.I)
        y_match = re.search(r"Y([+-]?[0-9.]+)", line, flags=re.I)
        if x_match:
            current_x = decode_gerber_number(x_match.group(1), x_decimals, unit_scale)
        if y_match:
            current_y = decode_gerber_number(y_match.group(1), y_decimals, unit_scale)
        if (x_match or y_match) and current_x is not None and current_y is not None:
            xs.append(current_x)
            ys.append(current_y)
    if not xs or not ys:
        raise ValidationError("Gerber contains no decodable XY coordinates")
    return min(xs), min(ys), max(xs), max(ys)


def minimum_draw_aperture(text: str) -> float | None:
    unit_scale = 25.4 if re.search(r"%MOIN\*%", text, flags=re.I) else 1.0
    apertures: dict[int, float] = {}
    for match in re.finditer(r"%ADD(\d+)([CRO]),([^*%]+)\*%", text, flags=re.I):
        code = int(match.group(1))
        dimensions = [float(value) for value in re.findall(r"[0-9]+(?:\.[0-9]+)?", match.group(3))]
        if dimensions:
            apertures[code] = min(dimensions) * unit_scale
    selected: int | None = None
    region = False
    used: list[float] = []
    for line in text.splitlines():
        upper = line.upper()
        if "G36" in upper:
            region = True
        if "G37" in upper:
            region = False
        for match in re.finditer(r"(?:^|[^0-9])D(\d{2,})\*", upper):
            code = int(match.group(1))
            if code >= 10:
                selected = code
        if "D01" in upper and not region and selected in apertures:
            used.append(apertures[selected])
    return min(used) if used else None


def gerber_flash_inventory(text: str) -> list[dict[str, Any]]:
    """Decode standard circle/rectangle D03 flashes with their exact geometry."""
    fs_match = re.search(r"%FS[LT]A?X(\d)(\d)Y(\d)(\d)\*%", text, flags=re.I)
    if not fs_match:
        raise ValidationError("Gerber lacks a supported FS coordinate-format statement")
    x_decimals, y_decimals = int(fs_match.group(2)), int(fs_match.group(4))
    unit_scale = 25.4 if re.search(r"%MOIN\*%", text, flags=re.I) else 1.0
    apertures: dict[int, dict[str, Any]] = {}
    for match in re.finditer(r"%ADD(\d+)([A-Z][A-Z0-9_]*),?([^*%]*)\*%", text, flags=re.I):
        code = int(match.group(1))
        kind = match.group(2).upper()
        modifiers = [part for part in re.split(r"[Xx]", match.group(3)) if part]
        try:
            values = [float(value) * unit_scale for value in modifiers]
        except ValueError as exc:
            raise ValidationError(f"invalid aperture modifier for D{code}") from exc
        if kind == "C" and values:
            apertures[code] = {"shape": "circle", "diameter": values[0]}
        elif kind == "R" and len(values) >= 2:
            apertures[code] = {"shape": "rect", "width": values[0], "height": values[1]}
        else:
            apertures[code] = {"shape": f"unsupported:{kind}", "modifiers": values}

    selected: int | None = None
    current_x: float | None = None
    current_y: float | None = None
    flashes: list[dict[str, Any]] = []
    for line in text.splitlines():
        upper = line.strip().upper()
        for match in re.finditer(r"(?:^|[^0-9])D(\d+)\*", upper):
            code = int(match.group(1))
            if code >= 10:
                selected = code
        x_match = re.search(r"X([+-]?[0-9.]+)", upper)
        y_match = re.search(r"Y([+-]?[0-9.]+)", upper)
        if x_match:
            current_x = decode_gerber_number(x_match.group(1), x_decimals, unit_scale)
        if y_match:
            current_y = decode_gerber_number(y_match.group(1), y_decimals, unit_scale)
        if "D03" not in upper:
            continue
        if selected is None or selected not in apertures:
            raise ValidationError(f"Gerber flash uses undefined aperture D{selected}")
        if current_x is None or current_y is None:
            raise ValidationError("Gerber flash lacks a complete modal coordinate")
        flashes.append({"x": current_x, "y": current_y, "aperture": selected, **apertures[selected]})
    return flashes


def paste_signature(item: dict[str, Any]) -> tuple[Any, ...]:
    base: tuple[Any, ...] = (round(float(item["x"]), 6), round(float(item["y"]), 6), str(item.get("shape")))
    if item.get("shape") == "rect":
        return base + (round(float(item["width"]), 6), round(float(item["height"]), 6))
    if item.get("shape") == "circle":
        diameter = item.get("diameter")
        if diameter is None and item.get("radius") is not None:
            diameter = 2 * float(item["radius"])
        return base + (round(float(diameter), 6),)
    return base


def parse_excellon(text: str) -> list[dict[str, float]]:
    unit_scale = 25.4 if re.search(r"\bINCH\b", text, flags=re.I) else 1.0
    decimal_mode = "decimal" in text.lower() or any("." in token for token in re.findall(r"[XY][+-]?([0-9.]+)", text))
    format_match = re.search(r"FILE_FORMAT\s*=\s*(\d+)\s*:\s*(\d+)", text, flags=re.I)
    decimals = int(format_match.group(2)) if format_match else 4
    tools: dict[int, float] = {}
    active_tool: int | None = None
    hits: list[dict[str, float]] = []
    current_x: float | None = None
    current_y: float | None = None

    def decode(raw: str) -> float:
        if decimal_mode or "." in raw:
            return float(raw) * unit_scale
        sign = -1 if raw.startswith("-") else 1
        return sign * int(raw.lstrip("+-")) / (10**decimals) * unit_scale

    for line in text.splitlines():
        stripped = line.strip().upper()
        definition = re.fullmatch(r"T(\d+)C([0-9.]+)(?:.*)?", stripped)
        if definition:
            tools[int(definition.group(1))] = float(definition.group(2)) * unit_scale
            continue
        selection = re.fullmatch(r"T(\d+)", stripped)
        if selection:
            active_tool = int(selection.group(1))
            continue
        x_match = re.search(r"X([+-]?[0-9.]+)", stripped)
        y_match = re.search(r"Y([+-]?[0-9.]+)", stripped)
        if x_match:
            current_x = decode(x_match.group(1))
        if y_match:
            current_y = decode(y_match.group(1))
        if (x_match or y_match) and active_tool is not None and current_x is not None and current_y is not None:
            if active_tool not in tools:
                raise ValidationError(f"Excellon uses undefined tool T{active_tool}")
            hits.append({"x": current_x, "y": current_y, "diameter": tools[active_tool]})
    return hits


def relative_hole_pattern(hits: Sequence[dict[str, float]]) -> list[tuple[float, float, float]]:
    if not hits:
        return []
    cx = sum(hit["x"] for hit in hits) / len(hits)
    cy = sum(hit["y"] for hit in hits) / len(hits)
    return sorted((round(hit["x"] - cx, 4), round(hit["y"] - cy, 4), round(hit["diameter"], 4)) for hit in hits)


def validate_gerbers(
    path: Path | None,
    manifest: dict[str, Any],
    circuit_context: dict[str, Any] | None,
    report: Report,
) -> tuple[FileBundle | None, dict[str, str]]:
    section = "gerber_excellon"
    if path is None:
        report.external_missing("GBR-001", section, "final Gerber/Excellon archive not supplied or uniquely discovered")
        return None, {}
    try:
        bundle = FileBundle(path)
        roles, duplicates = classify_bundle(bundle)
    except (OSError, UnicodeError, zipfile.BadZipFile, ValidationError) as exc:
        report.failed("GBR-001", section, f"cannot open final Gerber bundle: {exc}")
        return None, {}
    policy = manifest["gerber_policy"]
    required_roles = set(policy["required_roles"])
    forbidden_roles = set(policy["forbidden_roles"])
    missing_roles = sorted(required_roles - set(roles))
    manufacturing_suffixes = {".gbr", ".ger", ".gtl", ".gbl", ".gts", ".gbs", ".gtp", ".gbp", ".gto", ".gbo", ".gm1", ".gko", ".drl", ".xln"}
    manufacturing_members = [name for name in bundle.names if Path(name).suffix.lower() in manufacturing_suffixes]
    unclassified = [name for name in manufacturing_members if artifact_role(name, bundle.read_text(name)) is None]
    layer_set_failures: dict[str, Any] = {}
    if duplicates:
        layer_set_failures["duplicate_roles"] = sorted(duplicates)
    if missing_roles:
        layer_set_failures["missing_roles"] = missing_roles
    present_forbidden = sorted(forbidden_roles & set(roles))
    if present_forbidden:
        layer_set_failures["forbidden_roles"] = present_forbidden
    if unclassified:
        layer_set_failures["unclassified_manufacturing_files"] = unclassified
    expected_file_count = int(policy["exact_manufacturing_file_count"])
    if len(manufacturing_members) != expected_file_count:
        layer_set_failures["manufacturing_file_count"] = {"expected": expected_file_count, "actual": len(manufacturing_members)}
    if layer_set_failures:
        layer_set_failures["members"] = bundle.names
        report.failed("GBR-001", section, "Gerber/Excellon layer set is not the exact frozen top-assembly set", layer_set_failures)
    else:
        report.passed("GBR-001", section, "exact nine-file top-assembly Gerber/Excellon set present", roles)

    syntax_failures: list[dict[str, Any]] = []
    for role in sorted(required_roles & set(roles)):
        name = roles[role]
        try:
            text = bundle.read_text(name)
        except (OSError, UnicodeError, ValidationError) as exc:
            syntax_failures.append({"role": role, "error": str(exc)})
            continue
        if not text.strip():
            syntax_failures.append({"role": role, "error": "empty file"})
        elif role.startswith("drill"):
            if "M48" not in text.upper() or "M30" not in text.upper():
                syntax_failures.append({"role": role, "error": "missing M48/M30 Excellon framing"})
        else:
            if not re.search(r"%FS[LT]A?X\d\dY\d\d\*%", text, flags=re.I) or "M02" not in text.upper():
                syntax_failures.append({"role": role, "error": "missing Gerber FS/M02 framing"})
    if syntax_failures:
        report.failed("GBR-002", section, "one or more Gerber/Excellon files are malformed or empty", syntax_failures)
    elif required_roles.issubset(roles):
        report.passed("GBR-002", section, "all required manufacturing layers have valid text framing")

    if "edge" in roles:
        try:
            bbox = gerber_bbox(bundle.read_text(roles["edge"]))
            width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if close(width, manifest["board"]["width_mm"], 0.01) and close(height, manifest["board"]["height_mm"], 0.01):
                report.passed("GBR-003", section, "Gerber profile is exactly 50 x 40 mm", {"bbox_mm": bbox})
            else:
                report.failed("GBR-003", section, "Gerber profile dimensions differ", {"bbox_mm": bbox, "width_mm": width, "height_mm": height})
        except (ValidationError, OSError, UnicodeError) as exc:
            report.failed("GBR-003", section, f"cannot decode Gerber board profile: {exc}")

    copper_width_failures: list[dict[str, Any]] = []
    copper_widths: dict[str, float | None] = {}
    for role in ("f_cu", "b_cu"):
        if role not in roles:
            continue
        try:
            minimum = minimum_draw_aperture(bundle.read_text(roles[role]))
        except (OSError, UnicodeError, ValidationError) as exc:
            copper_width_failures.append({"role": role, "error": str(exc)})
            continue
        copper_widths[role] = minimum
        if minimum is not None and minimum + EPS < manifest["board"]["min_trace_width_mm"]:
            copper_width_failures.append({"role": role, "minimum_draw_aperture_mm": minimum})
    if copper_width_failures:
        report.failed("GBR-004", section, "Gerber drawn copper includes a feature below 0.20 mm", copper_width_failures)
    elif {"f_cu", "b_cu"}.issubset(roles):
        report.passed("GBR-004", section, "Gerber copper draw apertures meet the 0.20 mm floor", copper_widths)

    if "drill_npth" in roles:
        try:
            npth_hits = parse_excellon(bundle.read_text(roles["drill_npth"]))
            expected_hits = [
                {"x": hole["x"], "y": hole["y"], "diameter": hole["diameter"]}
                for hole in manifest["board"]["mounting_holes"]
            ]
            if relative_hole_pattern(npth_hits) == relative_hole_pattern(expected_hits):
                report.passed("GBR-005", section, "NPTH drill has exactly the frozen four-hole pattern", npth_hits)
            else:
                report.failed(
                    "GBR-005",
                    section,
                    "NPTH drill pattern/count/diameter differs",
                    {"expected_relative": relative_hole_pattern(expected_hits), "actual_relative": relative_hole_pattern(npth_hits)},
                )
        except (ValidationError, OSError, UnicodeError) as exc:
            report.failed("GBR-005", section, f"cannot parse NPTH drill: {exc}")
    if "drill_pth" in roles:
        try:
            pth_hits = parse_excellon(bundle.read_text(roles["drill_pth"]))
            # The plated drill file contains both component PTH pads and vias.
            expected_count = (
                manifest["circuit_counts"]["pcb_plated_hole"]
                + manifest["circuit_counts"]["pcb_via"]
            )
            if len(pth_hits) == expected_count:
                report.passed(
                    "GBR-006",
                    section,
                    f"PTH drill hit count matches {manifest['circuit_counts']['pcb_plated_hole']} component holes + {manifest['circuit_counts']['pcb_via']} vias ({expected_count})",
                )
            else:
                report.failed("GBR-006", section, "PTH drill hit count differs", {"expected": expected_count, "actual": len(pth_hits)})
        except (ValidationError, OSError, UnicodeError) as exc:
            report.failed("GBR-006", section, f"cannot parse PTH drill: {exc}")

    if "f_paste" not in roles:
        report.failed("GBR-007", section, "cannot verify top paste without F.Paste Gerber")
    elif circuit_context is None:
        report.failed("GBR-007", section, "cannot cross-check top paste because circuit JSON did not parse")
    else:
        try:
            paste_text = bundle.read_text(roles["f_paste"])
            flashes = gerber_flash_inventory(paste_text)
            if re.search(r"D01\*|G36\*", paste_text, flags=re.I):
                raise ValidationError("F.Paste contains drawn/region copper instead of flash-only apertures")
            circuit_elements = circuit_context["elements"]
            source_ref_by_id = {
                str(item["source_component_id"]): str(item["name"])
                for item in circuit_elements
                if item.get("type") == "source_component"
            }
            pcb_ref_by_id = {
                str(item["pcb_component_id"]): source_ref_by_id.get(str(item.get("source_component_id")), "")
                for item in circuit_elements
                if item.get("type") == "pcb_component"
            }
            populated_refs = set(manifest["assembly"]["smt_refs"])
            dnp_refs = set(manifest["assembly"]["dnp_refs"])
            component_pads = [
                item
                for item in circuit_elements
                if item.get("type") == "pcb_smtpad"
                and item.get("layer") == "top"
                and item.get("pcb_component_id") is not None
            ]
            populated_pads = [
                pad for pad in component_pads if pcb_ref_by_id.get(str(pad.get("pcb_component_id"))) in populated_refs
            ]
            dnp_pads = [
                pad for pad in component_pads if pcb_ref_by_id.get(str(pad.get("pcb_component_id"))) in dnp_refs
            ]
            unexpected_owner_pads = [
                str(pad.get("pcb_smtpad_id"))
                for pad in component_pads
                if pcb_ref_by_id.get(str(pad.get("pcb_component_id"))) not in populated_refs | dnp_refs
            ]
            expected_count = int(policy["top_paste_populated_flash_count"])
            scale = float(policy["top_paste_scale_to_copper_pad"])

            def scaled_pad_signature(pad: dict[str, Any]) -> tuple[Any, ...]:
                scaled = dict(pad)
                if pad.get("shape") == "rect":
                    scaled["width"] = float(pad["width"]) * scale
                    scaled["height"] = float(pad["height"]) * scale
                elif pad.get("shape") == "circle":
                    scaled["radius"] = float(pad["radius"]) * scale
                return paste_signature(scaled)

            expected_inventory = Counter(scaled_pad_signature(item) for item in populated_pads)
            actual_inventory = Counter(paste_signature(item) for item in flashes)
            dnp_inventory = Counter(scaled_pad_signature(item) for item in dnp_pads)
            missing = list((expected_inventory - actual_inventory).elements())
            extra = list((actual_inventory - expected_inventory).elements())
            dnp_flashes = list((actual_inventory & dnp_inventory).elements())
            failures: dict[str, Any] = {}
            if len(populated_pads) != expected_count or len(dnp_pads) != 2 or unexpected_owner_pads or not close(scale, 1.0):
                failures["circuit_population_pad_mapping"] = {
                    "expected_populated_pad_count": expected_count,
                    "populated_pad_count": len(populated_pads),
                    "dnp_pad_count": len(dnp_pads),
                    "unexpected_owner_pad_ids": unexpected_owner_pads,
                    "required_scale_to_copper_pad": 1.0,
                    "configured_scale": scale,
                }
            if len(flashes) != expected_count:
                failures["flash_count"] = {"expected": expected_count, "actual": len(flashes)}
            if missing:
                failures["missing_populated_pad_apertures"] = missing
            if extra:
                failures["unexpected_paste_apertures"] = extra
            if dnp_flashes:
                failures["dnp_r22_apertures"] = dnp_flashes
            if any(flash.get("shape") != "rect" for flash in flashes):
                failures["non_rectangular_flashes"] = [flash for flash in flashes if flash.get("shape") != "rect"]
            if failures:
                report.failed(
                    "GBR-007",
                    section,
                    "F.Paste is not an exact one-to-one 1.00x center/dimension match to the 92 populated top SMT pads",
                    failures,
                )
            else:
                report.passed(
                    "GBR-007",
                    section,
                    "F.Paste has exactly 92 full-size populated top-SMT flashes; R22 DNP, PTH, fiducial, and bottom apertures are absent",
                )
        except (KeyError, TypeError, ValueError, ValidationError, OSError, UnicodeError) as exc:
            report.failed("GBR-007", section, f"cannot independently verify F.Paste flash inventory: {exc}")
    return bundle, roles


def tokenize_sexpr(text: str) -> list[str]:
    token_re = re.compile(r'\s*(\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+)')
    tokens = []
    position = 0
    while position < len(text):
        match = token_re.match(text, position)
        if not match:
            if text[position:].strip():
                raise ValidationError(f"unparseable S-expression near byte {position}")
            break
        token = match.group(1)
        position = match.end()
        if token.startswith('"'):
            try:
                token = json.loads(token)
            except json.JSONDecodeError as exc:
                raise ValidationError(f"invalid quoted S-expression token near byte {position}: {exc}") from exc
        tokens.append(token)
    return tokens


def parse_sexpr(text: str) -> list[Any]:
    stack: list[list[Any]] = []
    roots: list[Any] = []
    for token in tokenize_sexpr(text):
        if token == "(":
            node: list[Any] = []
            if stack:
                stack[-1].append(node)
            else:
                roots.append(node)
            stack.append(node)
        elif token == ")":
            if not stack:
                raise ValidationError("unexpected closing parenthesis")
            stack.pop()
        else:
            if not stack:
                raise ValidationError("atom outside root S-expression")
            stack[-1].append(token)
    if stack:
        raise ValidationError("unterminated S-expression")
    if len(roots) != 1 or not isinstance(roots[0], list):
        raise ValidationError(f"expected one S-expression root, found {len(roots)}")
    return roots[0]


def sexpr_nodes(node: Any, head: str) -> Iterator[list[Any]]:
    if not isinstance(node, list):
        return
    if node and node[0] == head:
        yield node
    for child in node:
        if isinstance(child, list):
            yield from sexpr_nodes(child, head)


def direct_child(node: Sequence[Any], head: str) -> list[Any] | None:
    for child in node[1:]:
        if isinstance(child, list) and child and child[0] == head:
            return child
    return None


def node_xy(node: Sequence[Any], head: str) -> tuple[float, float] | None:
    child = direct_child(node, head)
    if child is None or len(child) < 3:
        return None
    try:
        return float(child[1]), float(child[2])
    except (TypeError, ValueError):
        return None


def footprint_local_to_board(
    footprint: Sequence[Any], local: tuple[float, float]
) -> tuple[float, float] | None:
    """Transform a footprint-local coordinate into KiCad board coordinates."""
    at = direct_child(footprint, "at")
    if at is None or len(at) < 3:
        return None
    try:
        origin_x, origin_y = float(at[1]), float(at[2])
        angle = math.radians(float(at[3])) if len(at) >= 4 else 0.0
    except (TypeError, ValueError):
        return None
    local_x, local_y = local
    return (
        origin_x + local_x * math.cos(angle) - local_y * math.sin(angle),
        origin_y + local_x * math.sin(angle) + local_y * math.cos(angle),
    )


def node_number(node: Sequence[Any], head: str) -> float | None:
    child = direct_child(node, head)
    if child is None or len(child) < 2:
        return None
    for value in child[1:]:
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return None


def node_layer(node: Sequence[Any]) -> str | None:
    child = direct_child(node, "layer")
    return str(child[1]) if child is not None and len(child) > 1 else None


def footprint_reference(footprint: Sequence[Any]) -> str | None:
    for child in footprint[1:]:
        if isinstance(child, list) and len(child) >= 3:
            if child[0] == "property" and child[1] == "Reference":
                return str(child[2])
            if child[0] == "fp_text" and child[1] == "reference":
                return str(child[2])
    return None


def validate_kicad(
    path: Path | None,
    manifest: dict[str, Any],
    circuit_context: dict[str, Any] | None,
    report: Report,
) -> None:
    section = "kicad_pcb"
    if path is None:
        report.external_missing("KIC-001", section, "final KiCad PCB/source archive not supplied or uniquely discovered")
        return
    try:
        with FileBundle(path) as bundle:
            candidates = [name for name in bundle.names if name.lower().endswith(".kicad_pcb")]
            if len(candidates) != 1:
                report.failed(
                    "KIC-001",
                    section,
                    "KiCad artifact must contain exactly one .kicad_pcb",
                    {"candidates": candidates, "members": bundle.names},
                )
                return
            pcb_name = candidates[0]
            text = bundle.read_text(pcb_name)
    except (OSError, UnicodeError, zipfile.BadZipFile, ValidationError) as exc:
        report.failed("KIC-001", section, f"cannot open KiCad PCB artifact: {exc}")
        return
    try:
        root = parse_sexpr(text)
    except ValidationError as exc:
        report.failed("KIC-001", section, f"cannot parse KiCad PCB S-expression: {exc}")
        return
    if not root or root[0] != "kicad_pcb":
        report.failed("KIC-001", section, "artifact root is not kicad_pcb")
        return
    report.passed("KIC-001", section, "KiCad PCB parsed", {"member": pcb_name, "bytes": len(text.encode('utf-8'))})

    expected_board = manifest["board"]
    geometry_failures: list[dict[str, Any]] = []
    general = direct_child(root, "general")
    thickness = node_number(general, "thickness") if general else None
    if thickness is None or not close(thickness, expected_board["thickness_mm"]):
        geometry_failures.append({"field": "thickness_mm", "expected": expected_board["thickness_mm"], "actual": thickness})
    layers_node = direct_child(root, "layers")
    copper_layers = []
    if layers_node:
        for layer in layers_node[1:]:
            if isinstance(layer, list) and len(layer) >= 2 and str(layer[1]).endswith(".Cu"):
                copper_layers.append(str(layer[1]))
    if len(copper_layers) != expected_board["copper_layers"] or set(copper_layers) != {"F.Cu", "B.Cu"}:
        geometry_failures.append({"field": "copper_layers", "expected": ["F.Cu", "B.Cu"], "actual": copper_layers})

    edge_points: list[tuple[float, float]] = []
    for kind in ("gr_line", "gr_rect", "gr_arc"):
        for graphic in sexpr_nodes(root, kind):
            if node_layer(graphic) != "Edge.Cuts":
                continue
            for head in ("start", "end", "mid", "center"):
                point = node_xy(graphic, head)
                if point is not None:
                    edge_points.append(point)
    if edge_points:
        xs = [point[0] for point in edge_points]
        ys = [point[1] for point in edge_points]
        bbox = (min(xs), min(ys), max(xs), max(ys))
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if not close(width, expected_board["width_mm"], 0.01) or not close(height, expected_board["height_mm"], 0.01):
            geometry_failures.append({"field": "edge_bbox_mm", "expected": [50.0, 40.0], "actual": [width, height], "bbox": bbox})
    else:
        geometry_failures.append({"field": "Edge.Cuts", "error": "no supported board-profile graphics"})
    if geometry_failures:
        report.failed("KIC-002", section, "KiCad board stack/profile differs", geometry_failures)
    else:
        report.passed("KIC-002", section, "KiCad PCB is 50 x 40 x 1.6 mm with two copper layers")

    segments = list(sexpr_nodes(root, "segment"))
    vias = list(sexpr_nodes(root, "via"))
    route_failures: list[dict[str, Any]] = []
    segment_widths = []
    for index, segment in enumerate(segments):
        width = node_number(segment, "width")
        if width is None:
            route_failures.append({"segment_index": index, "error": "missing width"})
        else:
            segment_widths.append(width)
            if width + EPS < expected_board["min_trace_width_mm"]:
                route_failures.append({"segment_index": index, "width_mm": width})
    if not segments:
        route_failures.append({"error": "zero routed segments"})
    for index, via in enumerate(vias):
        size = node_number(via, "size")
        drill = node_number(via, "drill")
        if size is None or size + EPS < expected_board["min_via_diameter_mm"]:
            route_failures.append({"via_index": index, "field": "size", "actual": size})
        if drill is None or drill + EPS < expected_board["min_via_drill_mm"]:
            route_failures.append({"via_index": index, "field": "drill", "actual": drill})
    if len(vias) > 300:
        route_failures.append({"error": "implausible via count", "actual": len(vias), "maximum": 300})
    if route_failures:
        report.failed("KIC-003", section, "KiCad trace/via geometry violates frozen floors", route_failures)
    else:
        report.passed(
            "KIC-003",
            section,
            "KiCad traces/vias meet width/diameter floors",
            {"segments": len(segments), "vias": len(vias), "minimum_segment_width_mm": min(segment_widths)},
        )

    footprints = list(sexpr_nodes(root, "footprint"))
    footprint_by_ref: dict[str, list[Any]] = {}
    duplicates: list[str] = []
    for footprint in footprints:
        ref = footprint_reference(footprint)
        if not ref:
            continue
        if ref in footprint_by_ref:
            duplicates.append(ref)
        footprint_by_ref[ref] = footprint
    expected_refs = set(manifest["components"])
    actual_refs = set(footprint_by_ref)
    if duplicates or expected_refs != actual_refs:
        report.failed(
            "KIC-004",
            section,
            "KiCad footprint designator set differs",
            {"duplicates": sorted(set(duplicates)), "missing": sorted(expected_refs - actual_refs), "unexpected": sorted(actual_refs - expected_refs)},
        )
    else:
        report.passed("KIC-004", section, f"KiCad has exact {len(expected_refs)}-footprint designator set")

    endpoint_net: dict[str, str] = {}
    pad_pin_failures: list[dict[str, Any]] = []
    for ref, footprint in footprint_by_ref.items():
        actual_pins: set[str] = set()
        for pad in (child for child in footprint[1:] if isinstance(child, list) and child and child[0] == "pad"):
            if len(pad) < 2:
                continue
            pin = normalize_pin_hint(pad[1])
            if pin is None:
                continue
            actual_pins.add(pin)
            net = direct_child(pad, "net")
            if net is not None and len(net) >= 3:
                endpoint_net[f"{ref}.{pin}"] = str(net[2])
        expected_pins = set(manifest.get("critical_pin_labels", {}).get(ref, {})) or {
            endpoint.split(".", 1)[1]
            for endpoints in manifest["topology"].values()
            for endpoint in endpoints
            if endpoint.startswith(f"{ref}.")
        }
        if expected_pins and actual_pins != expected_pins:
            pad_pin_failures.append({"ref": ref, "expected_pins": sorted(expected_pins, key=int), "actual_pins": sorted(actual_pins, key=int)})
    if pad_pin_failures:
        report.failed("KIC-005", section, "KiCad physical pad-number sets differ", pad_pin_failures)
    else:
        report.passed("KIC-005", section, "KiCad footprint pad-number sets match the frozen topology")

    topology_failures: list[dict[str, Any]] = []
    all_expected_endpoints = {endpoint for endpoints in manifest["topology"].values() for endpoint in endpoints}
    for group, endpoints in manifest["topology"].items():
        missing = [endpoint for endpoint in endpoints if endpoint not in endpoint_net]
        if missing:
            topology_failures.append({"group": group, "missing_pad_nets": missing})
            continue
        nets = {endpoint_net[endpoint] for endpoint in endpoints}
        if len(nets) != 1:
            topology_failures.append({"group": group, "error": "split nets", "nets": sorted(nets)})
            continue
        net = next(iter(nets))
        actual_endpoints = {endpoint for endpoint, actual_net in endpoint_net.items() if actual_net == net and endpoint in all_expected_endpoints}
        if actual_endpoints != set(endpoints):
            topology_failures.append({"group": group, "net": net, "missing": sorted(set(endpoints) - actual_endpoints), "unexpected": sorted(actual_endpoints - set(endpoints))})
    if topology_failures:
        report.failed("KIC-006", section, "KiCad pad-to-net topology differs", topology_failures)
    else:
        report.passed("KIC-006", section, "KiCad pad-to-net topology matches all frozen groups")

    npth_hits: list[dict[str, float]] = []
    for footprint in footprints:
        for pad in (
            child
            for child in footprint[1:]
            if isinstance(child, list) and child and child[0] == "pad"
        ):
            if len(pad) < 3 or str(pad[2]) != "np_thru_hole":
                continue
            local = node_xy(pad, "at")
            drill = node_number(pad, "drill")
            board_at = footprint_local_to_board(footprint, local) if local is not None else None
            if board_at is not None and drill is not None:
                npth_hits.append({"x": board_at[0], "y": board_at[1], "diameter": drill})
    expected_hits = [
        {"x": hole["x"], "y": hole["y"], "diameter": hole["diameter"]}
        for hole in manifest["board"]["mounting_holes"]
    ]
    if relative_hole_pattern(npth_hits) == relative_hole_pattern(expected_hits):
        report.passed("KIC-007", section, "KiCad NPTH mounting-hole pattern matches")
    else:
        report.failed(
            "KIC-007",
            section,
            "KiCad NPTH mounting-hole pattern differs",
            {"expected_relative": relative_hole_pattern(expected_hits), "actual_relative": relative_hole_pattern(npth_hits)},
        )

    if circuit_context is None:
        report.failed("KIC-008", section, "cannot cross-check KiCad trace/via counts because circuit JSON did not parse")
    else:
        circuit_elements = circuit_context["elements"]
        expected_vias = sum(item.get("type") == "pcb_via" for item in circuit_elements)
        expected_segments = 0
        for trace in (item for item in circuit_elements if item.get("type") == "pcb_trace"):
            route = trace.get("route", [])
            expected_segments += sum(
                1
                for first, second in zip(route, route[1:])
                if first.get("route_type") == "wire"
                and second.get("route_type") == "wire"
                and first.get("layer") == second.get("layer")
            )
        if len(vias) != expected_vias or len(segments) != expected_segments:
            report.failed(
                "KIC-008",
                section,
                "KiCad routed segment/via counts do not match circuit JSON",
                {
                    "circuit_segments": expected_segments,
                    "kicad_segments": len(segments),
                    "circuit_vias": expected_vias,
                    "kicad_vias": len(vias),
                },
            )
        else:
            report.passed(
                "KIC-008",
                section,
                "KiCad routed segment/via counts exactly match circuit JSON",
                {"segments": len(segments), "vias": len(vias)},
            )


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.strip().lower())


def find_column(headers: Sequence[str], aliases: Sequence[str]) -> str | None:
    normalized = {normalize_header(header): header for header in headers}
    for alias in aliases:
        if normalize_header(alias) in normalized:
            return normalized[normalize_header(alias)]
    return None


def read_csv_text(text: str) -> tuple[list[dict[str, str]], list[str]]:
    sample = text[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    if reader.fieldnames is None:
        raise ValidationError("CSV has no header")
    headers = [str(header).strip() for header in reader.fieldnames if header is not None]
    if len(headers) != len(set(headers)):
        raise ValidationError("CSV contains duplicate header names")
    rows = []
    for raw in reader:
        row = {str(key).strip(): str(value or "").strip() for key, value in raw.items() if key is not None}
        if any(row.values()):
            rows.append(row)
    return rows, headers


def expand_designators(text: str) -> list[str]:
    refs: list[str] = []
    tokens = re.findall(r"[A-Za-z]+\d+(?:\s*-\s*(?:[A-Za-z]+)?\d+)?", text.upper())
    for token in tokens:
        compact = re.sub(r"\s+", "", token)
        if "-" not in compact:
            refs.append(compact)
            continue
        first, last = compact.split("-", 1)
        first_match = re.fullmatch(r"([A-Z]+)(\d+)", first)
        last_match = re.fullmatch(r"([A-Z]*)(\d+)", last)
        if not first_match or not last_match:
            raise ValidationError(f"cannot expand designator range: {token}")
        prefix = first_match.group(1)
        if last_match.group(1) and last_match.group(1) != prefix:
            raise ValidationError(f"cross-prefix designator range is forbidden: {token}")
        start, end = int(first_match.group(2)), int(last_match.group(2))
        if end < start or end - start > 1000:
            raise ValidationError(f"invalid designator range: {token}")
        refs.extend(f"{prefix}{index}" for index in range(start, end + 1))
    return refs


def parse_engineering_value(text: str, kind: str) -> float | None:
    value = text.strip().replace("Ω", "ohm").replace("µ", "u").lower()
    if kind == "capacitance":
        descriptive = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([pnum]?)\s*f(?:\b|$)", value)
        if descriptive:
            return float(descriptive.group(1)) * {"": 1.0, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3}[descriptive.group(2)]
    else:
        descriptive = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([rkm]?)\s*(?:ohm)(?:\b|$)", value)
        if descriptive:
            return float(descriptive.group(1)) * {"": 1.0, "r": 1.0, "k": 1e3, "m": 1e6}[descriptive.group(2)]
    value = re.sub(r"\s+", "", value)
    value = value.replace("ohms", "").replace("ohm", "")
    if kind == "capacitance":
        value = value.rstrip("f")
        multipliers = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3}
    else:
        multipliers = {"r": 1.0, "k": 1e3, "m": 1e6}
    embedded = re.fullmatch(r"([0-9]+)([a-z])([0-9]+)", value)
    if embedded and embedded.group(2) in multipliers:
        number = float(f"{embedded.group(1)}.{embedded.group(3)}")
        return number * multipliers[embedded.group(2)]
    suffix = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?(?:e[+-]?\d+)?)([a-z]?)", value)
    if suffix:
        multiplier = multipliers.get(suffix.group(2), 1.0 if suffix.group(2) == "" else None)
        if multiplier is not None:
            return float(suffix.group(1)) * multiplier
    return None


def natural_ref_key(ref: str) -> tuple[str, int, str]:
    match = re.fullmatch(r"([A-Za-z]+)(\d+)", ref)
    return (match.group(1), int(match.group(2)), "") if match else (ref, -1, ref)


def load_csv_source(
    explicit_path: Path | None,
    gerber_bundle: FileBundle | None,
    gerber_roles: dict[str, str],
    role: str,
) -> tuple[str, str] | None:
    if explicit_path is not None:
        try:
            return explicit_path.read_text(encoding="utf-8-sig"), str(explicit_path)
        except (OSError, UnicodeError) as exc:
            raise ValidationError(f"cannot read {role} CSV {explicit_path}: {exc}") from exc
    if gerber_bundle is not None and role in gerber_roles:
        try:
            return gerber_bundle.read_text(gerber_roles[role]), f"{gerber_bundle.path}!{gerber_roles[role]}"
        except (OSError, UnicodeError, ValidationError) as exc:
            raise ValidationError(f"cannot read embedded {role} CSV: {exc}") from exc
    return None


def bom_value_matches(row_value: str, expected: dict[str, Any]) -> bool:
    field = expected["value_field"]
    target = expected["value"]
    if field in {"resistance", "capacitance"}:
        parsed = parse_engineering_value(row_value, field)
        return parsed is not None and close(parsed, target, max(abs(float(target)) * 1e-9, 1e-15))
    if isinstance(target, (int, float)):
        parsed = re.search(r"[0-9]+(?:\.[0-9]+)?", row_value)
        return parsed is not None and close(float(parsed.group(0)), target, 1e-9)
    return bool(row_value.strip())


def validate_bom(
    source: tuple[str, str] | None,
    manifest: dict[str, Any],
    report: Report,
) -> set[str] | None:
    section = "pcbway_bom"
    if source is None:
        report.external_missing("BOM-001", section, "final PCBWay SMT BOM not supplied or embedded in Gerber archive")
        return None
    text, label = source
    try:
        rows, headers = read_csv_text(text)
    except ValidationError as exc:
        report.failed("BOM-001", section, f"cannot parse BOM: {exc}")
        return None
    ref_col = find_column(headers, ["Designator", "Designators", "Reference Designator", "Reference Designators", "Reference", "References", "RefDes"])
    qty_col = find_column(headers, ["Qty", "Quantity"])
    mpn_col = find_column(
        headers,
        ["Manufacturer Part Number", "Manufacturer Part #", "Manufacturer PN", "MPN", "Part Number"],
    )
    value_col = find_column(headers, ["Value", "Comment", "Component Value", "Description"])
    side_col = find_column(headers, ["Layer", "Side"])
    missing_columns = [name for name, column in (("designator", ref_col), ("quantity", qty_col), ("MPN", mpn_col), ("value", value_col)) if column is None]
    if missing_columns:
        report.failed("BOM-001", section, "BOM lacks required PCBWay columns", {"missing": missing_columns, "headers": headers})
        return None
    assert ref_col and qty_col and mpn_col and value_col
    report.passed("BOM-001", section, "PCBWay BOM parsed with required columns", {"source": label, "rows": len(rows)})

    by_ref: dict[str, dict[str, str]] = {}
    row_failures: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        try:
            refs = expand_designators(row[ref_col])
        except ValidationError as exc:
            row_failures.append({"row": index, "error": str(exc)})
            continue
        if not refs:
            row_failures.append({"row": index, "error": "no parseable designators"})
            continue
        try:
            quantity = int(float(row[qty_col]))
        except ValueError:
            row_failures.append({"row": index, "error": "quantity is not an integer", "value": row[qty_col]})
            quantity = -1
        if quantity != len(refs):
            row_failures.append({"row": index, "error": "quantity/designator count mismatch", "quantity": quantity, "refs": refs})
        for ref in refs:
            if ref in by_ref:
                row_failures.append({"row": index, "error": "duplicate designator", "ref": ref})
            by_ref[ref] = row
        if side_col is not None and row[side_col].strip().lower() not in {"top", "front", "f", "f.cu"}:
            row_failures.append({"row": index, "field": "side", "expected": "top", "actual": row[side_col]})
    expected_refs = set(manifest["assembly"]["smt_refs"])
    actual_refs = set(by_ref)
    forbidden = set(manifest["assembly"]["dnp_refs"]) | set(manifest["assembly"]["tht_refs"])
    if actual_refs != expected_refs or actual_refs & forbidden:
        row_failures.append(
            {
                "error": "BOM designator set differs",
                "missing": sorted(expected_refs - actual_refs, key=natural_ref_key),
                "unexpected": sorted(actual_refs - expected_refs, key=natural_ref_key),
                "forbidden_dnp_or_tht": sorted(actual_refs & forbidden, key=natural_ref_key),
            }
        )
    for ref in sorted(expected_refs & actual_refs, key=natural_ref_key):
        row = by_ref[ref]
        expected = manifest["components"][ref]
        if row[mpn_col].strip() != expected["mpn"]:
            row_failures.append({"ref": ref, "field": "MPN", "expected": expected["mpn"], "actual": row[mpn_col]})
        if not bom_value_matches(row[value_col], expected):
            row_failures.append({"ref": ref, "field": "value", "expected": expected["value"], "actual": row[value_col]})
    if row_failures:
        report.failed("BOM-002", section, "BOM quantities/designators/values/MPNs are inconsistent", row_failures)
    else:
        report.passed("BOM-002", section, "BOM is exact 41-part top-SMT population; DNP/THT excluded")
    return actual_refs


def parse_finite(value: str, field: str, ref: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise ValidationError(f"{ref} {field} is not numeric: {value!r}") from exc
    if not math.isfinite(number):
        raise ValidationError(f"{ref} {field} is not finite: {value!r}")
    return number


def validate_cpl(
    source: tuple[str, str] | None,
    manifest: dict[str, Any],
    circuit_context: dict[str, Any] | None,
    bom_refs: set[str] | None,
    report: Report,
) -> set[str] | None:
    section = "pcbway_cpl"
    if source is None:
        report.external_missing("CPL-001", section, "final PCBWay SMT CPL not supplied or embedded in Gerber archive")
        return None
    text, label = source
    try:
        rows, headers = read_csv_text(text)
    except ValidationError as exc:
        report.failed("CPL-001", section, f"cannot parse CPL: {exc}")
        return None
    ref_col = find_column(headers, ["Designator", "Reference", "RefDes"])
    x_col = find_column(headers, ["Mid X", "Center X", "PosX", "X"])
    y_col = find_column(headers, ["Mid Y", "Center Y", "PosY", "Y"])
    side_col = find_column(headers, ["Layer", "Side"])
    rotation_col = find_column(headers, ["Rotation", "Rot"])
    missing = [name for name, column in (("designator", ref_col), ("X", x_col), ("Y", y_col), ("side", side_col), ("rotation", rotation_col)) if column is None]
    if missing:
        report.failed("CPL-001", section, "CPL lacks required PCBWay columns", {"missing": missing, "headers": headers})
        return None
    assert ref_col and x_col and y_col and side_col and rotation_col
    report.passed("CPL-001", section, "PCBWay CPL parsed with required columns", {"source": label, "rows": len(rows)})

    by_ref: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        refs = expand_designators(row[ref_col])
        if len(refs) != 1:
            failures.append({"row": index, "error": "CPL row must contain one designator", "value": row[ref_col]})
            continue
        ref = refs[0]
        if ref in by_ref:
            failures.append({"row": index, "error": "duplicate designator", "ref": ref})
            continue
        try:
            by_ref[ref] = {
                "x": parse_finite(row[x_col], "X", ref),
                "y": parse_finite(row[y_col], "Y", ref),
                "rotation": parse_finite(row[rotation_col], "rotation", ref) % 360,
                "side": row[side_col].strip().lower(),
            }
        except ValidationError as exc:
            failures.append({"row": index, "error": str(exc)})
    expected_refs = set(manifest["assembly"]["smt_refs"])
    actual_refs = set(by_ref)
    forbidden = set(manifest["assembly"]["dnp_refs"]) | set(manifest["assembly"]["tht_refs"])
    if actual_refs != expected_refs or actual_refs & forbidden:
        failures.append(
            {
                "error": "CPL designator set differs",
                "missing": sorted(expected_refs - actual_refs, key=natural_ref_key),
                "unexpected": sorted(actual_refs - expected_refs, key=natural_ref_key),
                "forbidden_dnp_or_tht": sorted(actual_refs & forbidden, key=natural_ref_key),
            }
        )
    for ref, placement in by_ref.items():
        if placement["side"] not in {"top", "front", "f", "f.cu"}:
            failures.append({"ref": ref, "field": "side", "expected": "top", "actual": placement["side"]})
    if bom_refs is not None and actual_refs != bom_refs:
        failures.append({"error": "BOM/CPL designator mismatch", "bom_only": sorted(bom_refs - actual_refs), "cpl_only": sorted(actual_refs - bom_refs)})

    if circuit_context is None:
        failures.append({"error": "cannot cross-check CPL coordinates/rotation because circuit JSON did not parse"})
    else:
        positions = circuit_context["positions"]
        comparable = sorted(expected_refs & actual_refs & set(positions), key=natural_ref_key)
        translations = [
            (by_ref[ref]["x"] - float(positions[ref]["x"]), by_ref[ref]["y"] - float(positions[ref]["y"]))
            for ref in comparable
        ]
        if translations:
            dx = sum(item[0] for item in translations) / len(translations)
            dy = sum(item[1] for item in translations) / len(translations)
            for ref in comparable:
                expected_x = float(positions[ref]["x"]) + dx
                expected_y = float(positions[ref]["y"]) + dy
                if not close(by_ref[ref]["x"], expected_x, 0.02) or not close(by_ref[ref]["y"], expected_y, 0.02):
                    failures.append(
                        {
                            "ref": ref,
                            "field": "centroid",
                            "expected_after_global_translation": [round(expected_x, 5), round(expected_y, 5)],
                            "actual": [by_ref[ref]["x"], by_ref[ref]["y"]],
                        }
                    )
                expected_rotation = float(positions[ref].get("rotation", 0)) % 360
                delta = abs(((by_ref[ref]["rotation"] - expected_rotation + 180) % 360) - 180)
                if delta > 0.1:
                    failures.append({"ref": ref, "field": "rotation", "expected": expected_rotation, "actual": by_ref[ref]["rotation"]})
            if abs(dx) > 1000 or abs(dy) > 1000:
                failures.append({"error": "implausible CPL origin translation", "dx": dx, "dy": dy})
        else:
            failures.append({"error": "no comparable CPL/circuit placements"})
    if failures:
        report.failed("CPL-002", section, "CPL population/side/coordinates/rotation is inconsistent", failures)
    else:
        report.passed("CPL-002", section, "CPL exactly matches circuit placements and BOM; DNP/THT excluded")
    return actual_refs


def validate_drc(
    path: Path | None,
    report: Report,
    expected_circuit_sha256: str | None = None,
    required_audit_categories: Sequence[str] = (),
) -> None:
    section = "drc"
    if path is None:
        report.external_missing("DRC-001", section, "final KiCad DRC/unconnected report not supplied or uniquely discovered")
        return
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        report.failed("DRC-001", section, f"cannot read DRC report: {exc}")
        return
    if not text.strip():
        report.failed("DRC-001", section, "DRC report is empty")
        return

    counts: dict[str, int] = {}
    audit_counts: dict[str, int] = {}
    metadata_failures: list[dict[str, Any]] = []
    if path.suffix.lower() == ".json" or text.lstrip().startswith(("{", "[")):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            report.failed("DRC-001", section, f"DRC JSON cannot be parsed: {exc}")
            return

        if isinstance(data, dict) and str(data.get("schema", "")).startswith("BubbleLink"):
            reported_hash = data.get("circuit_json_sha256")
            if expected_circuit_sha256 is None or reported_hash != expected_circuit_sha256:
                metadata_failures.append(
                    {
                        "field": "circuit_json_sha256",
                        "expected": expected_circuit_sha256,
                        "actual": reported_hash,
                    }
                )
            raw_audit_counts = data.get("check_counts")
            if not isinstance(raw_audit_counts, dict) or not raw_audit_counts:
                metadata_failures.append({"field": "check_counts", "error": "missing or empty"})
            else:
                for key, value in raw_audit_counts.items():
                    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                        metadata_failures.append(
                            {"field": f"check_counts.{key}", "error": "must be a nonnegative integer", "actual": value}
                        )
                    else:
                        audit_counts[str(key)] = value
                if required_audit_categories:
                    missing_categories = sorted(set(required_audit_categories) - set(raw_audit_counts))
                    unexpected_categories = sorted(set(raw_audit_counts) - set(required_audit_categories))
                    if missing_categories or unexpected_categories:
                        metadata_failures.append(
                            {
                                "field": "check_counts",
                                "missing_categories": missing_categories,
                                "unexpected_categories": unexpected_categories,
                            }
                        )

        def collect(node: Any, parent: str = "") -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    normalized = normalize_header(str(key))
                    if normalized in {"violations", "errors", "unconnected", "unconnecteditems", "drcviolations"}:
                        if isinstance(value, list):
                            counts[normalized] = len(value)
                        elif isinstance(value, int):
                            counts[normalized] = value
                    collect(value, normalized)
            elif isinstance(node, list):
                for child in node:
                    collect(child, parent)

        collect(data)
    else:
        patterns = {
            "violations": [
                r"found\s+(\d+)\s+(?:drc\s+)?violations?",
                r"(?:drc\s+)?violations?\s*[:=]\s*(\d+)",
            ],
            "unconnected": [
                r"found\s+(\d+)\s+unconnected(?:\s+(?:pads?|items?))?",
                r"unconnected(?:\s+(?:pads?|items?))?\s*[:=]\s*(\d+)",
            ],
            "errors": [r"errors?\s*[:=]\s*(\d+)", r"found\s+(\d+)\s+errors?"],
        }
        for key, expressions in patterns.items():
            for expression in expressions:
                match = re.search(expression, text, flags=re.I)
                if match:
                    counts[key] = int(match.group(1))
                    break
    if not counts or not any(key in counts for key in ("violations", "drcviolations", "errors")) or not any(
        key in counts for key in ("unconnected", "unconnecteditems")
    ):
        report.failed(
            "DRC-001",
            section,
            "DRC report does not provide independently parseable violation and unconnected counts",
            {"parsed_counts": counts},
        )
        return
    nonzero = {key: value for key, value in counts.items() if value != 0}
    nonzero_audits = {key: value for key, value in audit_counts.items() if value != 0}
    if metadata_failures or nonzero or nonzero_audits:
        report.failed(
            "DRC-001",
            section,
            "DRC/unconnected report is not clean or is not bound to the frozen circuit",
            {
                "metadata_failures": metadata_failures,
                "nonzero_summary_counts": nonzero,
                "nonzero_audit_counts": nonzero_audits,
            },
        )
    else:
        evidence: dict[str, Any] = dict(counts)
        if audit_counts:
            evidence["zero_audit_categories"] = len(audit_counts)
            evidence["circuit_json_sha256"] = expected_circuit_sha256
        report.passed(
            "DRC-001",
            section,
            "DRC report is hash-bound to the circuit and states zero violations, unconnected items, and audit-category findings",
            evidence,
        )


def parse_hash_manifest(path: Path) -> dict[Path, str]:
    entries: dict[Path, str] = {}
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64})\s+[* ]?(.+)", line)
        if not match:
            raise ValidationError(f"invalid SHA-256 manifest line {line_number}: {raw!r}")
        candidate = Path(match.group(2))
        resolved = (path.parent / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
        if resolved in entries:
            raise ValidationError(f"duplicate SHA-256 manifest path on line {line_number}: {candidate}")
        entries[resolved] = match.group(1).lower()
    if not entries:
        raise ValidationError("SHA-256 manifest contains no entries")
    return entries


def expand_files(paths: Iterable[Path | None]) -> set[Path]:
    files: set[Path] = set()
    for path in paths:
        if path is None:
            continue
        if path.is_dir():
            files.update(candidate.resolve() for candidate in path.rglob("*") if candidate.is_file())
        elif path.is_file():
            files.add(path.resolve())
    return files


def validate_hashes(
    manifest_path: Path,
    required_paths: Iterable[Path | None],
    report: Report,
) -> None:
    section = "integrity"
    if not manifest_path.is_file():
        report.failed("HASH-001", section, f"SHA-256 manifest is missing: {manifest_path}")
        return
    try:
        entries = parse_hash_manifest(manifest_path)
    except (OSError, UnicodeError, ValidationError) as exc:
        report.failed("HASH-001", section, f"cannot parse SHA-256 manifest: {exc}")
        return
    missing_files = sorted(str(path) for path in entries if not path.is_file())
    mismatches = []
    for path, expected in entries.items():
        if not path.is_file():
            continue
        actual = sha256_file(path)
        if actual != expected:
            mismatches.append({"path": str(path), "expected": expected, "actual": actual})
    if missing_files or mismatches:
        report.failed(
            "HASH-001",
            section,
            "one or more manifest entries are missing or changed",
            {"missing_files": missing_files, "hash_mismatches": mismatches},
        )
    else:
        report.passed("HASH-001", section, f"all {len(entries)} SHA-256 entries match")

    required_files = expand_files(required_paths)
    untracked = sorted(str(path) for path in required_files - set(entries))
    if untracked:
        report.failed("HASH-002", section, "release inputs/artifacts are not covered by SHA-256 manifest", untracked)
    else:
        report.passed("HASH-002", section, "every supplied release input/artifact is hash-covered")


def freeze_hashes(manifest_path: Path, paths: Iterable[Path | None]) -> None:
    files = sorted(expand_files(paths), key=lambda path: str(path))
    if not files:
        raise ValidationError("no files supplied for hash freeze")
    lines = []
    for path in files:
        try:
            relative = os.path.relpath(path, manifest_path.parent)
        except ValueError:
            relative = str(path)
        lines.append(f"{sha256_file(path)}  {Path(relative).as_posix()}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def discover_candidates(release_root: Path, kind: str) -> list[Path]:
    if not release_root.is_dir():
        return []
    candidates: list[Path] = []
    for path in release_root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(release_root).parts
        if any(part in {"manufacturing_qa", "verification", "system_docs"} for part in relative_parts[:-1]):
            continue
        name = path.name.lower()
        suffix = path.suffix.lower()
        if kind == "gerbers" and suffix == ".zip" and "gerber" in name:
            candidates.append(path)
        elif kind == "kicad" and (suffix == ".kicad_pcb" or (suffix == ".zip" and "kicad" in name)):
            candidates.append(path)
        elif kind == "bom" and suffix == ".csv" and "bom" in name:
            candidates.append(path)
        elif kind == "cpl" and suffix == ".csv" and "template" not in name and any(token in name for token in ("cpl", "pick_and_place", "centroid")):
            candidates.append(path)
        elif kind == "drc" and suffix in {".rpt", ".txt", ".json"} and "drc" in name:
            candidates.append(path)
    return sorted(set(path.resolve() for path in candidates))


def resolve_optional(explicit: str | None, release_root: Path, kind: str, report: Report) -> Path | None:
    if explicit:
        return Path(explicit).expanduser().resolve()
    candidates = discover_candidates(release_root, kind)
    preferred_names = {
        "bom": {"pcbway_smt_bom.csv"},
        "cpl": {"pcbway_smt_cpl.csv", "pcbway_pick_and_place.csv"},
    }
    preferred = [path for path in candidates if path.name.lower() in preferred_names.get(kind, set())]
    if len(preferred) == 1:
        return preferred[0]
    if len(preferred) > 1:
        candidates = preferred
    if len(candidates) > 1:
        digests = {sha256_file(path) for path in candidates}
        if len(digests) == 1:
            return sorted(
                candidates,
                key=lambda path: (
                    0 if "assembly" in {part.lower() for part in path.parts} else 1,
                    len(path.parts),
                    str(path),
                ),
            )[0]
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        report.failed(
            f"INP-{kind.upper()}",
            "inputs",
            f"multiple {kind} candidates found; pass --{kind} explicitly",
            [str(path) for path in candidates],
        )
    return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("preexport", "release"), default="preexport")
    parser.add_argument("--release-root", default=str(DEFAULT_RELEASE_ROOT))
    parser.add_argument("--manifest", default=str(SCRIPT_DIR / "frozen_design.json"))
    parser.add_argument("--hash-manifest", default=str(SCRIPT_DIR / "release_hashes.sha256"))
    parser.add_argument("--circuit-json", default=str(DEFAULT_CIRCUIT))
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--gerbers", help="final Gerber zip or directory")
    parser.add_argument("--kicad", help="final KiCad zip or .kicad_pcb")
    parser.add_argument("--bom", help="final PCBWay BOM CSV (otherwise use CSV embedded in Gerber zip)")
    parser.add_argument("--cpl", help="final PCBWay CPL CSV (otherwise use CSV embedded in Gerber zip)")
    parser.add_argument("--drc", help="final machine-readable/text DRC report (native KiCad or disclosed independent engine)")
    parser.add_argument("--output", help="also write deterministic JSON report to this path")
    parser.add_argument(
        "--freeze-hashes",
        action="store_true",
        help="explicitly replace the hash manifest with hashes of every supplied/discovered release input",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = Report(args.phase)
    release_root = Path(args.release_root).expanduser().resolve()
    manifest_path = Path(args.manifest).expanduser().resolve()
    hash_manifest_path = Path(args.hash_manifest).expanduser().resolve()
    circuit_path = Path(args.circuit_json).expanduser().resolve()
    source_path = Path(args.source).expanduser().resolve()

    try:
        manifest = safe_json(manifest_path)
    except ValidationError as exc:
        report.failed("CFG-001", "configuration", str(exc))
        payload = report.as_dict({"manifest": str(manifest_path)})
        print(json.dumps(payload, indent=2, sort_keys=True))
        return report.exit_code()
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        report.failed("CFG-001", "configuration", "unsupported/malformed frozen design manifest")
        payload = report.as_dict({"manifest": str(manifest_path)})
        print(json.dumps(payload, indent=2, sort_keys=True))
        return report.exit_code()
    else:
        report.passed("CFG-001", "configuration", "frozen design manifest parsed", {"design": manifest.get("design")})

    gerbers_path = resolve_optional(args.gerbers, release_root, "gerbers", report)
    kicad_path = resolve_optional(args.kicad, release_root, "kicad", report)
    bom_path = resolve_optional(args.bom, release_root, "bom", report)
    cpl_path = resolve_optional(args.cpl, release_root, "cpl", report)
    drc_path = resolve_optional(args.drc, release_root, "drc", report)

    core_tool_paths = [manifest_path, Path(__file__).resolve()]
    all_artifact_paths = [
        source_path,
        circuit_path,
        *core_tool_paths,
        gerbers_path,
        kicad_path,
        bom_path,
        cpl_path,
        drc_path,
    ]
    if args.freeze_hashes:
        freeze_missing_roles = []
        if gerbers_path is None:
            freeze_missing_roles.append("gerbers")
        if kicad_path is None:
            freeze_missing_roles.append("kicad")
        if drc_path is None:
            freeze_missing_roles.append("drc")
        embedded_roles: set[str] = set()
        if gerbers_path is not None and gerbers_path.exists():
            try:
                with FileBundle(gerbers_path) as freeze_bundle:
                    embedded_roles = set(classify_bundle(freeze_bundle)[0])
            except (OSError, UnicodeError, zipfile.BadZipFile, ValidationError):
                pass
        if bom_path is None and "bom" not in embedded_roles:
            freeze_missing_roles.append("bom")
        if cpl_path is None and "cpl" not in embedded_roles:
            freeze_missing_roles.append("cpl")
        if freeze_missing_roles:
            raise SystemExit(
                "refusing incomplete release hash freeze; missing final roles: "
                + ", ".join(sorted(freeze_missing_roles))
            )
        missing = [str(path) for path in all_artifact_paths if path is not None and not path.exists()]
        if missing:
            raise SystemExit(f"refusing to freeze hashes; inputs missing: {missing}")
        try:
            freeze_hashes(hash_manifest_path, all_artifact_paths)
        except (OSError, ValidationError) as exc:
            raise SystemExit(f"cannot freeze hashes: {exc}") from exc
        print(f"wrote {hash_manifest_path}")
        return 0

    circuit_context = validate_circuit(circuit_path, manifest, report)
    gerber_bundle, gerber_roles = validate_gerbers(gerbers_path, manifest, circuit_context, report)
    validate_kicad(kicad_path, manifest, circuit_context, report)
    try:
        bom_source = load_csv_source(bom_path, gerber_bundle, gerber_roles, "bom")
        cpl_source = load_csv_source(cpl_path, gerber_bundle, gerber_roles, "cpl")
    except ValidationError as exc:
        report.failed("CSV-001", "assembly", str(exc))
        bom_source = None
        cpl_source = None
    bom_refs = validate_bom(bom_source, manifest, report)
    validate_cpl(cpl_source, manifest, circuit_context, bom_refs, report)
    validate_drc(
        drc_path,
        report,
        sha256_file(circuit_path) if circuit_path.is_file() else None,
        manifest.get("drc_required_audit_categories", []),
    )
    if gerber_bundle is not None:
        gerber_bundle.close()

    validate_hashes(hash_manifest_path, all_artifact_paths, report)

    inputs = {
        "manifest": str(manifest_path),
        "hash_manifest": str(hash_manifest_path),
        "source": str(source_path),
        "circuit_json": str(circuit_path),
        "gerbers": str(gerbers_path) if gerbers_path else None,
        "kicad": str(kicad_path) if kicad_path else None,
        "bom": str(bom_path) if bom_path else ("embedded" if bom_source else None),
        "cpl": str(cpl_path) if cpl_path else ("embedded" if cpl_source else None),
        "drc": str(drc_path) if drc_path else None,
    }
    payload = report.as_dict(inputs)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
