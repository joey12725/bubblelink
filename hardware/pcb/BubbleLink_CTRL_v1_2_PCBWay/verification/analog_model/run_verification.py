#!/usr/bin/env python3
"""Run deterministic analytic verification for BubbleLink CTRL v1.1.

Exit status is non-zero only for an analytic/model failure.  Bench-required
items remain pending even when their analytic prerequisite passes.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import replace
import io
import json
import math
from pathlib import Path
import random
import statistics
import sys
from typing import Any, Dict, List, Sequence

sys.dont_write_bytecode = True

from controller_model import (
    ControllerParameters,
    detector_thresholds,
    fail_off_gate_voltage,
    ptc_hold_current,
    pump_gate_decay_time,
    pwm_filter_steady_state,
    q1_drive_corner,
    q1_start_latency,
    sensor_disconnect_release_time,
    sensor_step_latency,
    solve_delay_position,
    supervisor_brownout_shutdown,
    supervisor_clamp_sweep,
    supervisor_startup_ramp,
    timer_delay,
    timer_delay_with_adjustable_branch_open,
    timer_thresholds,
)


SUITE_VERSION = "1.1.1"
DEFAULT_SEED = 20_260_807
DEFAULT_SAMPLES = 20_000


def _between(value: float, bounds: Sequence[float]) -> bool:
    return float(bounds[0]) <= value <= float(bounds[1])


def _finite(value: float) -> bool:
    return math.isfinite(value)


def _result(
    vector: Dict[str, Any],
    passed: bool | None,
    measurements: Dict[str, Any],
    note: str = "",
) -> Dict[str, Any]:
    bench = bool(vector.get("bench_required", False))
    if passed is None:
        status = "BENCH_REQUIRED"
    elif passed and bench:
        status = "MODEL_PASS_BENCH_REQUIRED"
    else:
        status = "PASS" if passed else "FAIL"
    return {
        "id": vector["id"],
        "test": vector["test"],
        "status": status,
        "bench_required": bench,
        "measurements": measurements,
        "note": note,
    }


def evaluate_vector(vector: Dict[str, Any], base: ControllerParameters) -> Dict[str, Any]:
    test = vector["test"]
    inputs = vector.get("inputs", {})
    acceptance = vector.get("acceptance", {})

    if test == "detector_hysteresis":
        params = replace(
            base,
            vcc=float(inputs["vcc_v"]),
            detector_vol=float(inputs["detector_vol_v"]),
        )
        values = detector_thresholds(params, float(inputs["rv1_position"]))
        hysteresis_mv = values["hysteresis_v"] * 1e3
        passed = acceptance["hysteresis_min_mv"] <= hysteresis_mv <= acceptance["hysteresis_max_mv"]
        return _result(vector, passed, {**values, "hysteresis_mv": hysteresis_mv})

    if test == "detector_adjustment_span":
        params = replace(base, vcc=float(inputs["vcc_v"]))
        low = detector_thresholds(params, 0.0)["turn_on_v"]
        high = detector_thresholds(params, 1.0)["turn_on_v"]
        passed = _between(low, acceptance["minimum_turn_on_v"]) and _between(
            high, acceptance["maximum_turn_on_v"]
        )
        return _result(vector, passed, {"minimum_turn_on_v": low, "maximum_turn_on_v": high})

    if test == "sensor_step_latency":
        latency = sensor_step_latency(
            base,
            float(inputs["current_a"]),
            float(inputs["threshold_margin_mv"]) * 1e-3,
        )
        latency_ms = latency * 1e3
        passed = _finite(latency) and latency_ms <= acceptance["maximum_latency_ms"]
        return _result(vector, passed, {"latency_ms": latency_ms})

    if test == "pwm_detection":
        pwm = pwm_filter_steady_state(
            base,
            float(inputs["peak_current_a"]),
            float(inputs["frequency_hz"]),
            float(inputs["duty_cycle"]),
        )
        detected = pwm["high_increment_v"] >= float(inputs["threshold_margin_mv"]) * 1e-3
        passed = detected is bool(acceptance["expected_detected"])
        return _result(vector, passed, {**pwm, "detected": detected})

    if test == "timer_true_hysteresis":
        params = replace(
            base,
            vcc=float(inputs["vcc_v"]),
            timer_vol=float(inputs["timer_vol_v"]),
        )
        values = timer_thresholds(params)
        hysteresis_mv = values["hysteresis_v"] * 1e3
        passed = acceptance["hysteresis_min_mv"] <= hysteresis_mv <= acceptance["hysteresis_max_mv"]
        return _result(vector, passed, {**values, "hysteresis_mv": hysteresis_mv})

    if test == "timer_delay_range":
        params = replace(base, vcc=float(inputs["vcc_v"]))
        low_ms = timer_delay(params, 0.0) * 1e3
        high_ms = timer_delay(params, 1.0) * 1e3
        passed = _between(low_ms, acceptance["minimum_delay_ms"]) and _between(
            high_ms, acceptance["maximum_delay_ms"]
        )
        return _result(vector, passed, {"minimum_delay_ms": low_ms, "maximum_delay_ms": high_ms})

    if test == "timer_target_solution":
        target_s = float(inputs["target_delay_ms"]) * 1e-3
        position, achieved = solve_delay_position(base, target_s)
        error_ms = abs(achieved - target_s) * 1e3 if _finite(achieved) else math.inf
        passed = (
            _finite(position)
            and acceptance["position_min"] <= position <= acceptance["position_max"]
            and error_ms <= acceptance["error_max_ms"]
        )
        return _result(
            vector,
            passed,
            {"rv2_position": position, "achieved_delay_ms": achieved * 1e3, "error_ms": error_ms},
        )

    if test == "timer_adjustable_branch_open":
        delay = timer_delay_with_adjustable_branch_open(base)
        passed = _finite(delay) and delay <= acceptance["maximum_delay_s"]
        return _result(vector, passed, {"fail_safe_delay_s": delay})

    if test == "q1_start_latency":
        params = replace(
            base,
            vcc=float(inputs["vcc_v"]),
            c6_effective=float(inputs["c6_effective_uf"]) * 1e-6,
            c7_effective=float(inputs["c7_effective_uf"]) * 1e-6,
            r20=float(inputs["r20_ohm"]),
            detector_vol=float(inputs["detector_vol_v"]),
        )
        values = q1_start_latency(params, float(inputs["delay_position"]))
        latency_ms = values["latency_s"] * 1e3
        passed = _finite(values["latency_s"]) and latency_ms <= acceptance["maximum_latency_ms"]
        return _result(vector, passed, {**values, "latency_ms": latency_ms})

    if test == "q1_drive_corner":
        params = replace(
            base,
            vcc=float(inputs["vcc_v"]),
            r20=float(inputs["r20_ohm"]),
            detector_vol=float(inputs["detector_vol_v"]),
        )
        values = q1_drive_corner(params, float(inputs["delay_position"]))
        current_ua = values["required_drain_current_a"] * 1e6
        overdrive = values["final_vgs_magnitude_v"] - values["vgs_threshold_max_v"]
        passed = (
            current_ua <= acceptance["maximum_required_current_ua"]
            and overdrive >= acceptance["minimum_vgs_overdrive_v"]
        )
        return _result(
            vector,
            passed,
            {**values, "required_drain_current_ua": current_ua, "vgs_overdrive_v": overdrive},
            "Static low-current proxy passes; production Q1 operation remains temperature bench-gated.",
        )

    if test == "q3_fail_off":
        params = replace(
            base,
            vcc=float(inputs["vcc_v"]),
            q3_off_leakage=float(inputs["q3_off_leakage_ua"]) * 1e-6,
        )
        values = fail_off_gate_voltage(params)
        passed = (
            values["q2_gate_v"] <= acceptance["maximum_q2_gate_v"]
            and values["off_margin_v"] >= acceptance["minimum_off_margin_v"]
        )
        return _result(vector, passed, values)

    if test == "por_fail_off_coverage":
        gate = fail_off_gate_voltage(base)
        coverage = base.comparator_min_supply - base.supervisor_por_voltage
        values = {
            "supervisor_controlled_output_from_v": base.supervisor_por_voltage,
            "comparator_guaranteed_operating_from_v": base.comparator_min_supply,
            "controlled_coverage_margin_v": coverage,
            "tlv1822_por_output_state": "high_impedance",
            "q3_por_vgs_v": 0.0,
            "q2_gate_from_q3_leakage_v": gate["q2_gate_v"],
        }
        passed = (
            coverage >= acceptance["minimum_coverage_margin_v"]
            and gate["q2_gate_v"] <= acceptance["maximum_q2_gate_v"]
        )
        return _result(
            vector,
            passed,
            values,
            "Below 0.7 V U2 is undefined, but TLV1822 open-drain POR is Hi-Z and R12/R15 make Q3/Q2 fail off; observe this on hardware.",
        )

    if test == "supervisor_startup_ramp":
        params = replace(
            base,
            supervisor_falling_threshold=float(inputs["falling_threshold_v"]),
            supervisor_hysteresis_fraction=float(inputs["hysteresis_fraction"]),
            supervisor_release_delay=float(inputs["release_delay_ms"]) * 1e-3,
        )
        rates = [float(value) for value in inputs["ramp_rates_v_per_s"]]
        if inputs.get("include_hard_step", False):
            rates.append(math.inf)
        values = supervisor_startup_ramp(params, rates, float(inputs["final_supply_v"]))
        passed = (
            values["minimum_release_supply_v"] >= acceptance["minimum_release_supply_v"]
            and values["por_guard_margin_s"] * 1e3 >= acceptance["minimum_por_guard_ms"]
        )
        return _result(
            vector,
            passed,
            values,
            "The supervisor timing envelope passes analytically; zero pump motion still requires scoped hardware ramps.",
        )

    if test == "supervisor_clamp_sweep":
        params = replace(
            base,
            r20=float(inputs["r20_ohm"]),
            r23=float(inputs["r23_ohm"]),
        )
        values = supervisor_clamp_sweep(
            params,
            [float(value) for value in inputs["supplies_v"]],
            float(inputs["reset_low_v"]),
        )
        passed = (
            values["minimum_off_margin_v"] >= acceptance["minimum_off_margin_v"]
            and values["maximum_steady_reset_sink_current_a"] * 1e3
            <= acceptance["maximum_steady_sink_current_ma"]
        )
        return _result(vector, passed, values)

    if test == "supervisor_brownout_shutdown":
        params = replace(
            base,
            vcc=float(inputs["pre_brownout_vcc_v"]),
            r20=float(inputs["r20_ohm"]),
            r23=float(inputs["r23_ohm"]),
            c7_effective=float(inputs["c7_effective_uf"]) * 1e-6,
            supervisor_assert_delay=float(inputs["assert_delay_us"]) * 1e-6,
            c10=float(inputs["c10_nf"]) * 1e-9,
        )
        values = supervisor_brownout_shutdown(
            params,
            float(inputs["delay_position"]),
            float(inputs["reset_v_for_current"]),
            float(inputs["reset_v_for_timing"]),
        )
        current_ma = values["initial_reset_sink_current_a"] * 1e3
        total_ms = values["total_pump_off_s"] * 1e3
        passed = (
            current_ma <= acceptance["maximum_initial_sink_current_ma"]
            and total_ms <= acceptance["maximum_total_pump_off_ms"]
            and values["final_clamped_hold_v"] < values["falling_timer_threshold_v"]
        )
        return _result(
            vector,
            passed,
            {**values, "initial_reset_sink_current_ma": current_ma, "total_pump_off_ms": total_ms},
            "Bounded RC model passes; shallow brownout propagation and real gate/drain waveforms remain bench-gated.",
        )

    if test == "sensor_disconnect":
        release = sensor_disconnect_release_time(
            base,
            float(inputs["starting_sensor_v"]),
            float(inputs["detector_release_v"]),
        )
        delay = timer_delay(base, float(inputs["delay_position"]))
        total = release + delay
        passed = _finite(total) and total <= acceptance["maximum_total_off_time_s"]
        return _result(
            vector,
            passed,
            {"detector_release_s": release, "timer_delay_s": delay, "total_off_time_s": total},
        )

    if test == "ptc_derating":
        values = {
            "hold_current_0c_a": ptc_hold_current(base, 0.0),
            "hold_current_20c_a": ptc_hold_current(base, 20.0),
            "hold_current_40c_a": ptc_hold_current(base, 40.0),
            "hold_current_50c_a": ptc_hold_current(base, 50.0),
            "trip_current_20c_a": base.ptc_trip_20c,
            "post_reflow_resistance_max_ohm": base.ptc_resistance_post_reflow_max,
            "required_measured_pump_current_below_a": float(inputs["maximum_continuous_pump_current_50c_a"]),
        }
        return _result(
            vector,
            None,
            values,
            "The known 50 C PTC limit is 1.10 A; the real pump current is unknown until measured.",
        )

    if test in {
        "sensor_environmental_window",
        "physical_power_transients",
        "pump_inductive_switching",
    }:
        return _result(
            vector,
            None,
            {},
            "No component-level analytic model can replace the specified delivered-hardware measurement.",
        )

    raise ValueError(f"unknown test dispatcher: {test}")


def _vary(rng: random.Random, nominal: float, fraction: float = 0.01) -> float:
    return nominal * rng.uniform(1.0 - fraction, 1.0 + fraction)


def _percentile(sorted_values: Sequence[float], fraction: float) -> float:
    if not sorted_values:
        raise ValueError("metric must contain at least one value")
    location = fraction * (len(sorted_values) - 1)
    lower = int(math.floor(location))
    upper = int(math.ceil(location))
    if lower == upper:
        return sorted_values[lower]
    weight = location - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def _metric(values: List[float], unit: str = "") -> Dict[str, Any]:
    ordered = sorted(values)
    return {
        "unit": unit,
        "minimum": ordered[0],
        "p01": _percentile(ordered, 0.01),
        "median": statistics.median(ordered),
        "p99": _percentile(ordered, 0.99),
        "maximum": ordered[-1],
    }


def monte_carlo(samples: int, seed: int, base: ControllerParameters) -> Dict[str, Any]:
    rng = random.Random(seed)
    metrics: Dict[str, List[float]] = {
        "detector_hysteresis_mv": [],
        "timer_hysteresis_mv": [],
        "timer_minimum_delay_ms": [],
        "timer_maximum_delay_ms": [],
        "target_350_position": [],
        "q1_start_latency_ms": [],
        "q1_required_current_ua": [],
        "q1_vgs_overdrive_v": [],
        "q2_fail_off_gate_v": [],
        "r21_fail_safe_delay_s": [],
        "supervisor_clamp_margin_v": [],
        "supervisor_initial_sink_current_ma": [],
        "supervisor_brownout_off_ms": [],
        "supervisor_minimum_release_supply_v": [],
        "supervisor_por_guard_ms": [],
        "pump_gate_decay_ms": [],
    }
    failure_names = (
        "detector_hysteresis",
        "timer_hysteresis",
        "timer_range",
        "target_350",
        "q1_start",
        "q1_drive",
        "q3_fail_off",
        "r21_fail_safe",
        "supervisor_clamp",
        "supervisor_current",
        "supervisor_brownout_time",
        "supervisor_startup_guard",
    )
    failures = {key: 0 for key in failure_names}

    resistor_fields = (
        "r1", "r2", "r3", "rv1", "r19", "r4", "r5", "r7", "r8",
        "r20", "r9", "rv2", "r21", "r10", "r11", "r12", "r13",
        "r14", "r15", "r23",
    )
    clamp_supplies = (3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25)
    ramp_rates = (0.1, 1.0, 10.0, 100.0, math.inf)

    for _ in range(samples):
        updates = {field: _vary(rng, getattr(base, field)) for field in resistor_fields}
        updates.update(
            vcc=rng.uniform(4.75, 5.25),
            c5=_vary(rng, base.c5, 0.20),
            c6_effective=rng.uniform(13.5e-6, 30.4e-6),
            c7_effective=rng.uniform(4.68e-6, 8.60e-6),
            c7_insulation_resistance=rng.uniform(73.0e6, 500.0e6),
            detector_vol=rng.uniform(0.02, 0.25),
            timer_vol=rng.uniform(0.02, 0.25),
            detector_vos=rng.uniform(-0.004, 0.004),
            timer_vos=rng.uniform(-0.004, 0.004),
            sensor_sensitivity=rng.uniform(0.0394, 0.0410),
            supervisor_falling_threshold=4.38 * rng.uniform(0.98, 1.02),
            supervisor_hysteresis_fraction=rng.uniform(0.009, 0.015),
            supervisor_release_delay=rng.uniform(0.130, 0.270),
            supervisor_assert_delay=rng.uniform(0.0, 50.0e-6),
            supervisor_vol=rng.uniform(0.0, 0.30),
            supervisor_off_leakage=rng.uniform(0.0, 350.0e-9),
            q3_off_leakage=rng.uniform(0.0, 1.0e-6),
            c10=_vary(rng, base.c10, 0.10),
        )
        params = replace(base, **updates)

        det_hys = detector_thresholds(params, 0.5)["hysteresis_v"] * 1e3
        timer_hys = timer_thresholds(params)["hysteresis_v"] * 1e3
        delay_min = timer_delay(params, 0.0) * 1e3
        delay_max = timer_delay(params, 1.0) * 1e3
        target_position, target_delay = solve_delay_position(params, 0.350)
        target_metric = target_position if _finite(target_position) else -1.0
        q1_start = q1_start_latency(params, 0.0)["latency_s"] * 1e3
        q1_drive = q1_drive_corner(params, 0.0)
        q1_current = q1_drive["required_drain_current_a"] * 1e6
        q1_overdrive = q1_drive["final_vgs_magnitude_v"] - q1_drive["vgs_threshold_max_v"]
        gate = fail_off_gate_voltage(params)
        r21_delay = timer_delay_with_adjustable_branch_open(params)
        clamp = supervisor_clamp_sweep(params, clamp_supplies, 0.30)
        brownout = supervisor_brownout_shutdown(params, 1.0, 0.0, 0.30)
        startup = supervisor_startup_ramp(params, ramp_rates, 4.75)
        gate_decay_ms = pump_gate_decay_time(params) * 1e3

        metrics["detector_hysteresis_mv"].append(det_hys)
        metrics["timer_hysteresis_mv"].append(timer_hys)
        metrics["timer_minimum_delay_ms"].append(delay_min)
        metrics["timer_maximum_delay_ms"].append(delay_max)
        metrics["target_350_position"].append(target_metric)
        metrics["q1_start_latency_ms"].append(q1_start)
        metrics["q1_required_current_ua"].append(q1_current)
        metrics["q1_vgs_overdrive_v"].append(q1_overdrive)
        metrics["q2_fail_off_gate_v"].append(gate["q2_gate_v"])
        metrics["r21_fail_safe_delay_s"].append(r21_delay)
        metrics["supervisor_clamp_margin_v"].append(float(clamp["minimum_off_margin_v"]))
        metrics["supervisor_initial_sink_current_ma"].append(
            brownout["initial_reset_sink_current_a"] * 1e3
        )
        metrics["supervisor_brownout_off_ms"].append(brownout["total_pump_off_s"] * 1e3)
        metrics["supervisor_minimum_release_supply_v"].append(
            float(startup["minimum_release_supply_v"])
        )
        metrics["supervisor_por_guard_ms"].append(float(startup["por_guard_margin_s"]) * 1e3)
        metrics["pump_gate_decay_ms"].append(gate_decay_ms)

        failures["detector_hysteresis"] += not (3.0 <= det_hys <= 7.0)
        failures["timer_hysteresis"] += not (5.0 <= timer_hys <= 12.0)
        failures["timer_range"] += not (20.0 <= delay_min <= 80.0 and 350.0 <= delay_max <= 850.0)
        failures["target_350"] += not (
            _finite(target_position)
            and 0.0 <= target_position <= 1.0
            and abs(target_delay - 0.350) <= 1e-6
        )
        failures["q1_start"] += not (_finite(q1_start) and q1_start <= 40.0)
        failures["q1_drive"] += not (q1_current <= 250.0 and q1_overdrive >= 0.25)
        failures["q3_fail_off"] += not (gate["q2_gate_v"] <= 0.02 and gate["off_margin_v"] >= 0.60)
        failures["r21_fail_safe"] += not (_finite(r21_delay) and r21_delay <= 10.0)
        failures["supervisor_clamp"] += not (float(clamp["minimum_off_margin_v"]) >= 0.10)
        failures["supervisor_current"] += not (
            brownout["initial_reset_sink_current_a"] <= params.supervisor_recommended_current
        )
        failures["supervisor_brownout_time"] += not (
            _finite(brownout["total_pump_off_s"])
            and brownout["total_pump_off_s"] <= 0.015
        )
        failures["supervisor_startup_guard"] += not (
            float(startup["minimum_release_supply_v"]) >= 4.20
            and float(startup["por_guard_margin_s"]) >= 0.129
        )

    units = {
        "detector_hysteresis_mv": "mV",
        "timer_hysteresis_mv": "mV",
        "timer_minimum_delay_ms": "ms",
        "timer_maximum_delay_ms": "ms",
        "target_350_position": "fraction",
        "q1_start_latency_ms": "ms",
        "q1_required_current_ua": "uA",
        "q1_vgs_overdrive_v": "V",
        "q2_fail_off_gate_v": "V",
        "r21_fail_safe_delay_s": "s",
        "supervisor_clamp_margin_v": "V",
        "supervisor_initial_sink_current_ma": "mA",
        "supervisor_brownout_off_ms": "ms",
        "supervisor_minimum_release_supply_v": "V",
        "supervisor_por_guard_ms": "ms",
        "pump_gate_decay_ms": "ms",
    }
    summary = {name: _metric(values, units[name]) for name, values in metrics.items()}
    return {
        "seed": seed,
        "samples": samples,
        "assumptions": {
            "resistors": "independent uniform +/-1%",
            "C5_effective": "uniform +/-20%",
            "C6_effective": "uniform 13.5 to 30.4 uF engineering envelope; verify assembled value",
            "C7_effective": "uniform 4.68 to 8.60 uF tolerance/temperature/DC-bias envelope; verify assembled value",
            "TLV1822_input_offset": "independent uniform +/-4 mV",
            "TLV1822_output_low": "independent uniform 0.02 to 0.25 V",
            "TLV803_falling_threshold": "nominal 4.38 V with uniform +/-2% accuracy",
            "TLV803_hysteresis": "uniform 0.9% to 1.5%",
            "TLV803_release_delay": "uniform 130 to 270 ms",
            "TLV803_assert_delay": "uniform 0 to 50 us",
            "TLV803_reset_low": "uniform 0 to 0.30 V",
            "TLV803_open_drain_leakage": "uniform 0 to 350 nA",
            "ACS_sensitivity": "uniform 39.4 to 41.0 mV/A",
            "Q3_off_leakage": "uniform 0 to 1 uA",
            "C10": "uniform +/-10%",
        },
        "metrics": summary,
        "failure_counts": failures,
        "passed": all(count == 0 for count in failures.values()),
    }


def run_suite(vectors_path: Path, samples: int, seed: int) -> Dict[str, Any]:
    payload = json.loads(vectors_path.read_text(encoding="utf-8"))
    base = ControllerParameters()
    vector_results = [evaluate_vector(vector, base) for vector in payload["vectors"]]
    mc = monte_carlo(samples, seed, base)
    analytic_failures = [item["id"] for item in vector_results if item["status"] == "FAIL"]
    bench_pending = [item["id"] for item in vector_results if item["bench_required"]]
    model_passed = not analytic_failures and mc["passed"]
    return {
        "schema_version": "1.1",
        "suite_version": SUITE_VERSION,
        "design": payload["design"],
        "model_passed": model_passed,
        "release_disposition": "MODEL_PASS_BENCH_GATES_PENDING" if model_passed else "MODEL_FAIL",
        "analytic_failure_ids": analytic_failures,
        "bench_pending_ids": bench_pending,
        "vector_results": vector_results,
        "monte_carlo": mc,
        "limitations": [
            "This is a bounded passive-network/first-order model, not transistor-level SPICE.",
            "Effective C6/C7 values under assembled bias and temperature require measurement.",
            "TLV803 behavior below its 0.7 V controlled-output limit is covered by TLV1822 Hi-Z POR plus R15, but still requires hardware observation.",
            "The real ACS module offset/noise, pump current, PTC heating, flyback, brush noise, buck behavior and PCB parasitics require bench testing.",
            "A model pass is not authorization to skip any BENCH_REQUIRED traceability row.",
        ],
    }


def print_human(results: Dict[str, Any]) -> None:
    print(f"BubbleLink verification suite {results['suite_version']}")
    print(f"Disposition: {results['release_disposition']}")
    for item in results["vector_results"]:
        print(f"{item['id']:10s} {item['status']}")
    mc = results["monte_carlo"]
    print(f"Monte Carlo: {'PASS' if mc['passed'] else 'FAIL'} ({mc['samples']} samples, seed {mc['seed']})")
    for name, count in mc["failure_counts"].items():
        print(f"  {name:28s} failures={count}")
    print("Bench pending: " + ", ".join(results["bench_pending_ids"]))


def print_csv(results: Dict[str, Any]) -> None:
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("metric", "unit", "minimum", "p01", "median", "p99", "maximum"))
    for name, values in results["monte_carlo"]["metrics"].items():
        writer.writerow(
            (
                name,
                values["unit"],
                f"{values['minimum']:.12g}",
                f"{values['p01']:.12g}",
                f"{values['median']:.12g}",
                f"{values['p99']:.12g}",
                f"{values['maximum']:.12g}",
            )
        )
    sys.stdout.write(output.getvalue())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--vectors",
        type=Path,
        default=Path(__file__).with_name("test_vectors.json"),
        help="path to machine-readable test vectors",
    )
    parser.add_argument("--samples", type=int, default=DEFAULT_SAMPLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    mode.add_argument("--csv", action="store_true", help="emit Monte Carlo metrics as CSV")
    args = parser.parse_args(argv)
    if args.samples <= 0:
        parser.error("--samples must be positive")
    results = run_suite(args.vectors, args.samples, args.seed)
    if args.json:
        json.dump(results, sys.stdout, indent=2, sort_keys=True, allow_nan=False)
        sys.stdout.write("\n")
    elif args.csv:
        print_csv(results)
    else:
        print_human(results)
    return 0 if results["model_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
