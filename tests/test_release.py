"""Release checks for the BubbleLink hardware files.

Run from the repo root:  python -m pytest -q
Needs: pytest, numpy, trimesh.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware" / "pcb" / "BubbleLink_CTRL_v1_2_PCBWay"
STL_DIR = ROOT / "hardware" / "printed" / "stl"


def test_pcb_release_checksums_match():
    """Every file listed in SHA256SUMS.txt exists and is unchanged."""
    lines = (PCB / "SHA256SUMS.txt").read_text().splitlines()
    assert len(lines) > 50
    for line in lines:
        digest, name = line.split(None, 1)
        data = (PCB / name.strip()).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest, name


def test_manufacturing_qa_passes(tmp_path):
    """The structural release validator reports 50 PASS / 0 FAIL."""
    out = tmp_path / "qa.json"
    qa = PCB / "verification" / "manufacturing_qa"
    cmd = [
        sys.executable, str(qa / "validate_release.py"),
        "--phase", "release",
        "--manifest", str(qa / "frozen_design.json"),
        "--hash-manifest", str(qa / "release_hashes.portable.sha256"),
        "--source", str(PCB / "source/repro/circuit.tsx"),
        "--circuit-json", str(PCB / "source/BubbleLink_CTRL_v1_2_FINAL.circuit.json"),
        "--gerbers", str(PCB / "fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip"),
        "--kicad", str(PCB / "source/BubbleLink_CTRL_v1_2_KiCad_Source.zip"),
        "--bom", str(PCB / "assembly/PCBWAY_SMT_BOM.csv"),
        "--cpl", str(PCB / "assembly/PCBWAY_SMT_CPL.csv"),
        "--drc", str(PCB / "verification/BubbleLink_CTRL_v1_2_DRC.json"),
        "--output", str(out),
    ]
    subprocess.run(cmd, check=True, cwd=PCB, capture_output=True)
    summary = json.loads(out.read_text())["summary"]
    assert summary["FAIL"] == 0
    assert summary["PASS"] >= 50


def test_analog_model_monte_carlo_passes():
    """Circuit equations, test vectors and a Monte Carlo sweep all pass."""
    model = PCB / "verification" / "analog_model"
    res = subprocess.run(
        [sys.executable, "run_verification.py", "--samples", "2000", "--json"],
        cwd=model, capture_output=True, text=True, check=True,
    )
    report = json.loads(res.stdout)
    assert report["model_passed"] is True
    assert report["analytic_failure_ids"] == []
    assert report["monte_carlo"]["passed"] is True


@pytest.mark.parametrize("stl", sorted(STL_DIR.glob("*.stl")), ids=lambda p: p.name)
def test_stl_is_watertight(stl):
    trimesh = pytest.importorskip("trimesh")
    mesh = trimesh.load_mesh(stl)
    assert mesh.is_watertight
    assert mesh.volume > 0
