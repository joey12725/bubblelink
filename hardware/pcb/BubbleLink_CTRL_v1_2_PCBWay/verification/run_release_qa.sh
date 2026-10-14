#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 verification/manufacturing_qa/validate_release.py \
 --phase release \
 --manifest verification/manufacturing_qa/frozen_design.json \
 --hash-manifest verification/manufacturing_qa/release_hashes.portable.sha256 \
 --source source/repro/circuit.tsx \
 --circuit-json source/BubbleLink_CTRL_v1_2_FINAL.circuit.json \
 --gerbers fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip \
 --kicad source/BubbleLink_CTRL_v1_2_KiCad_Source.zip \
 --bom assembly/PCBWAY_SMT_BOM.csv \
 --cpl assembly/PCBWAY_SMT_CPL.csv \
 --drc verification/BubbleLink_CTRL_v1_2_DRC.json \
 --output verification/manufacturing_qa/manufacturing_qa_results.json
