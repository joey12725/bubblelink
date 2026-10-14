#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
npm ci --ignore-scripts --no-audit --no-fund
python3 correct_u1.py
node repour.mjs ../BubbleLink_CTRL_v1_2_FINAL.circuit.json ../BubbleLink_CTRL_v1_2_FINAL.circuit.json
node run_final_drc.mjs ../BubbleLink_CTRL_v1_2_FINAL.circuit.json ../../verification/BubbleLink_CTRL_v1_2_DRC.json
node export_final.mjs ../BubbleLink_CTRL_v1_2_FINAL.circuit.json ../..
python3 make_drawings.py
python3 ../../verification/verify_eco.py
python3 - <<'PY'
import zipfile
from pathlib import Path
r=Path('../..')
with zipfile.ZipFile(r/'fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((r/'fabrication/gerber_unpacked').iterdir()):z.write(p,p.name)
with zipfile.ZipFile(r/'source/BubbleLink_CTRL_v1_2_KiCad_Source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((r/'source').glob('*.kicad_*')):z.write(p,p.name)
PY
printf '%s\n' 'Geometry rebuilt. Timestamps may change export hashes; re-review before freezing a new release.'
