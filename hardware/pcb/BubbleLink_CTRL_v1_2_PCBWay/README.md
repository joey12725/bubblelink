# BubbleLink CTRL v1.2: release package

The complete fabrication release for the BubbleLink pump controller: a 50 × 40 mm, two-layer, all-analog board that runs the pack's transfer pump whenever a gun draws current, then holds it on for a tunable off-delay.

## Ordering boards

Upload these to any PCB fab that does top-side SMT assembly:

| File | Use |
|---|---|
| `fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip` | Gerbers and drills. Upload this ZIP, not the whole folder |
| `assembly/PCBWAY_SMT_BOM.csv` | SMT BOM (41 placements, top side only) |
| `assembly/PCBWAY_SMT_CPL.csv` | Pick-and-place, mm, lower-left datum, top view |
| `assembly/ASSEMBLY_NOTES_FOR_PCBWAY.txt` | Polarity, DNP and substitution rules |
| `drawings/BubbleLink_CTRL_v1_2_Assembly_and_U1_Detail.pdf` | Assembly drawing; its numbered pads and pin-1 table control orientation |
| `assembly/CRITICAL_PAD1_COORDINATES.csv` | Pin-1 coordinates for U1, U2, Q1–Q3, D1 |

J4 and R22 are DNP. C9 and R18 must be fitted. U1 is TI TLV1822QDRQ1 with no substitute. The through-hole parts (`assembly/USER_THT_BOM.csv`) are hand-soldered after delivery; see the [hand-solder guide](../hand_solder_guide/).

## What else is here

- `source/`: KiCad project (`.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, also zipped), the serialized tscircuit design, and `repro/`, the deterministic engineering-change scripts that turn the v1.1 baseline into v1.2.
- `drawings/`: schematic and PCB SVGs and independently parsed Gerber previews.
- `customer/`: design description, bring-up and acceptance test, motor harness suppression.
- `verification/`: the analog model with Monte Carlo, the manufacturing QA validator, DRC results and geometry regression.
- `ENGINEERING_CHANGE_AND_REVIEW.md`: why v1.2 exists (the corrected U1 land pattern, per TI D0008A) and what changed.
- `SHA256SUMS.txt`: checksums for every file in this folder.

## Re-running the checks

```sh
python3 verification/manufacturing_qa/validate_release.py --help   # or:
bash verification/run_release_qa.sh                                  # 50 structural checks
python3 verification/analog_model/run_verification.py               # model + 20,000-sample Monte Carlo
python3 verification/verify_eco.py                                   # needs gerbonara + shapely
```

The automated checks cover structure, geometry and the circuit model. Startup, brownout, timing calibration, sensor noise and thermal behaviour are covered by the bench procedure in `customer/BRINGUP_AND_ACCEPTANCE_TEST.md`.
