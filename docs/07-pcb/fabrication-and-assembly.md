# Fabrication and Assembly

Complete fabrication specifications for PCBWay, SMT assembly parameters, hand-soldering instructions for through-hole parts, motor harness assembly, and procedures to rebuild or reproduce the design.

## PCBWay fabrication parameters

Revision v1.2, issued 2026-09-09 (replaces v1.1). This is the final specification; use the complete v1.2 Gerber and drill set.

### Board specifications

| Parameter | Specification |
|-----------|---|
| **Dimensions** | 50.0 × 40.0 mm |
| **Thickness** | 1.6 mm FR-4 |
| **Copper weight** | 1 oz (both layers) |
| **Solder mask** | Green epoxy, standard coverage |
| **Silkscreen** | White, top side only |
| **Surface finish** | Lead-free HASL (RoHS) |
| **Mounting holes** | 4 × 3.2 mm NPTH; 43.0 × 33.0 mm pattern (M3 compatible) |
| **Via specification** | 56 total plated holes; 0.30 mm drill, 0.60 mm finished diameter (0.15 mm annulus per side) |
| **Plated hole specification** | 42 component holes (through-hole THT footprints) + 56 signal vias = 98 total drills |
| **Minimum trace width** | 0.25 mm routed (0.20 mm floor enforced) |
| **Minimum clearance** | 0.20 mm (pad-pad, pad-trace, via-trace, same/different nets) |
| **Board-edge clearance** | 0.50 mm minimum copper setback on both layers |
| **Copper-to-mounting-hole** | 1.0 mm keepout on both layers (3.0 mm radius per hole) |

### Copper layers

- **Top (F.Cu):** 41 SMT component placements, 15 labeled test point pads (TP1–TP15), 3 alignment fiducials (FID1–FID3), signal and ground traces, 56 plated via holes.
- **Bottom (B.Cu):** Ground plane with routed return paths and 56 plated via holes. No bottom components, no bottom copper features for fill or pour beyond signal routing and ground connectivity.
- **Gerber export floor:** All copper apertures ≥0.20 mm; measured minimum 0.25 mm on both layers. Compliant with floor tolerance.

### Solder mask and paste

| Layer | Specification | Apertures |
|-------|---|---|
| **F.Mask** (top) | ±0.10 mm registration; 0.075 mm per-side U1 expansion | Standard coverage over all copper except specified pads |
| **B.Mask** (bottom) | Standard | Standard coverage; no custom apertures |
| **F.Paste** (top) | Full-size 1× scale | 92 apertures for 41 SMT parts; no DNP/THT/fiducial/bottom apertures |
| **Bottom paste** | Absent | No bottom-side assembly |

**Paste aperture detail:** 92 full-size top-side SMT apertures; R22 (DNP) pads intentionally masked off; J4, J1, J2, J3, C1, RV1, RV2, SW1, LED1–3 (THT) excluded; test points TP1–15 and fiducials FID1–3 excluded.

### Stencil and assembly

**Stencil thickness:** TI's D0008A reference suggests 0.125 mm. Confirm the complete-board stencil process and notify design before use if aperture changes are required.

**U1 special instruction:** U1 (TLV1822QDRQ1) footprint corrected in v1.2. Pads are now 1.55 mm across package × 0.60 mm along row (from v1.1 incorrect 4.30 mm opposite-row spacing to correct 5.40 mm). Mask apertures 1.70 × 0.75 mm with 0.075 mm per-side expansion. Paste includes all eight full-size U1 apertures.

---

## Files to upload to PCBWay

**Upload only the v1.2 files from:**
```
hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip
```

This archive contains exactly nine files required for fabrication and assembly:

1. `BubbleLink_CTRL_v1_2-F.Cu.gbr` — Top copper layer
2. `BubbleLink_CTRL_v1_2-B.Cu.gbr` — Bottom copper layer
3. `BubbleLink_CTRL_v1_2-F.Mask.gbr` — Top solder mask
4. `BubbleLink_CTRL_v1_2-B.Mask.gbr` — Bottom solder mask
5. `BubbleLink_CTRL_v1_2-F.Paste.gbr` — Top solder paste (92 apertures)
6. `BubbleLink_CTRL_v1_2-F.SilkScreen.gbr` — Top silkscreen
7. `BubbleLink_CTRL_v1_2-Edge_Cuts.gbr` — Board outline
8. `BubbleLink_CTRL_v1_2-PTH.xln` — Plated hole drill program (98 hits)
9. `BubbleLink_CTRL_v1_2-NPTH.xln` — Non-plated hole drill program (4 mounting holes)

**Do NOT use v1.1 files.** The v1.1 board has an incorrect U1 land pattern. The v1.2 design corrects it and requires new drill files (three signal vias have relocated). Uploading v1.1 gerbers or drill files will produce an unusable board.

**Do NOT patch or substitute.** The complete v1.2 set must be used as-is. Do not attempt to reuse the v1.1 stencil, drill program, or partial layer files.

---

## SMT Assembly parameters

PCBWay top-side assembly only (no bottom-side SMT).

| Parameter | Value |
|-----------|-------|
| **Assembly type** | Top-side SMT (41 placements) |
| **Component count** | 41 parts across 23 line items |
| **Paste aperture count** | 92 (full-size, 1× scale, top only) |
| **Stencil type** | 0.125 mm thickness recommended |
| **Reflow profile** | Standard lead-free (RoHS) |
| **Population rule** | Exactly 41 placements per PCBWAY_SMT_BOM.csv and PCBWAY_SMT_CPL.csv; R22 and J4 DNP |
| **Fitted parts (must be populated)** | C9 and R18 (both required despite being in the SMT BOM) |
| **Placement accuracy** | ±0.1 mm (XY) per component centroid; rotation ±1° |
| **Via filling** | Not required for this design (all vias are signal/return, not component pads) |
| **Cleaning** | Flux residue must be removed, especially near high-impedance nodes (R5/R13 4.7 MΩ, RV1/RV2 trimmers, timing nodes). Use process compatible with fitted parts; do not apply unqualified conformal coat before field calibration. |

### BOM and CPL files

- **SMT BOM:** `../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/PCBWAY_SMT_BOM.csv` (41 parts, 23 lines, no THT/DNP rows)
- **SMT CPL:** `../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/PCBWAY_SMT_CPL.csv` (41 placements, XY in mm, lower-left datum, top view, +X right +Y up)
- **Board datum:** Lower-left corner; CPL coordinates do NOT include the absolute KiCad offset (−25, −20 mm).
- **Do not mirror:** Component centroids and rotation angles are for top-view assembly.

### Critical U1 placement

U1 (TLV1822QDRQ1) SOIC-8 with TI D0008A footprint:
- **Centroid:** X=16.0000 mm, Y=21.5000 mm (mid-device), rotation 90.0°
- **Pad 1 (OUT1):** X=14.0950 mm, Y=18.8000 mm (lower-left corner of chip as viewed from above after 90° rotation)
- **Copper pads:** 1.55 mm across × 0.60 mm along row
- **Paste apertures:** Full-size (no reduction); eight apertures, all included
- **Assembly verification:** Compare procured TI TLV1822QDRQ1 package dimensions and pin numbering against the supplied assembly PDF and critical-coordinates CSV. The generic CAD exporter's corner triangle symbols are not reliable orientation references for rotated parts; use the numbered pad list instead.

---

## Assembly notes and quality checks

Provided to PCBWay with the order. Reference file: `../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/ASSEMBLY_NOTES_FOR_PCBWAY.txt`

### Pre-assembly review (PCBWay CAM)

- Confirm v1.2 receipt and release status
- Compare every procured MPN's actual package, pinout and terminal orientation with final copper and paste
- Check U2/Q1–Q3 SOT-23 lands, D1 SMA, F1 custom PTC lands, C2/C6/C7 MLCC sizes
- Verify stencil process suitability, actual package overlap, and solder fillets
- Report all remaining DFM/assembly issues in **one consolidated response** (do not issue multiple RFQ cycles)
- Confirm part availability now, especially exact C2 MPN and C6/C7 sizes (1210 vs 1206), before starting a remake; no replacement part is pre-authorized
- Provide top-side placement CAM preview using updated assembly PDF and pad-1 CSV

### First-article inspection

- Provide clear first-article photograph (top and bottom) before remaining assembly run
- Check BOM vs CPL vs actual packages
- Verify U1 pin 1 (lower-left pad after rotation), U2 pinout (GND–RESET–VDD), MOSFET polarity (G/S/D pins), D1 band orientation (cathode at PUMP+)
- Verify all 41 solder joints for completeness, coverage, and bridging
- Confirm exactly 41-part population with no extras or omissions
- Check mask dams and clip silkscreen from mask openings while retaining readable reference/polarity identification
- Verify stencil fits large F1 (custom PTC lands 1.78 × 3.15 mm) and small SOT-23 lands without bridging or inadequate paste release

### Electrical and cleanliness

- Perform top-side placement/assembly only
- Leave J1, J2, J3, C1, RV1/RV2, SW1, LED1–LED3 holes **open for customer THT installation**
- **Do NOT populate J4 (DNP)** and **do NOT populate R22 (DNP)**
- **DO populate C9 and R18** (both on SMT BOM and fitted)
- No paste on DNP R22, THT pads, test holes (TP1–15), or fiducials
- Clean flux residue thoroughly, especially near 4.7 MΩ resistors (R5, R13) and timing/threshold nodes (VDELAY, HOLD, VMID)
- Use a process compatible with high-impedance nodes; do not apply unqualified conformal coat before field calibration
- Bare-board electrical test: confirm no shorts at J1 pin 1 to GND, no open circuits at test points
- Plated drill program verification required (revised via drilling in v1.2)

---

## Hand-soldering through-hole components

These 10 parts must be soldered **after** SMT assembly is complete and cleaned. Do not proceed to electrical testing until all THT parts are installed.

### Parts to install (10 total)

| Designator | Qty | Part | Installation notes |
|---|---:|---|---|
| **J1** | 1 | JST B2B-XH-A 2-pin header | Input power (5 V, GND); pin 1 to square pad |
| **J2** | 1 | JST B3B-XH-A 3-pin header | ACS sensor input; pin 1 to square pad |
| **J3** | 1 | JST B2B-XH-A 2-pin header | Pump motor output; pin 1 to square pad |
| **C1** | 1 | Rubycon 16ZLH100MEFC5X11 100 µF 16 V | Electrolytic; positive lead to square pad (pad 1) |
| **RV1** | 1 | Bourns 3296W-1-202LF 2 kΩ trimmer | **Lead order 1–3–2** (not 1–2–3); wiper (pin 2) to TP6 |
| **RV2** | 1 | Bourns 3296W-1-104LF 100 kΩ trimmer | **Lead order 1–3–2** (not 1–2–3); wiper (pin 2) to VDELAY |
| **SW1** | 1 | Omron B3F-1000 6×6 mm switch | Momentary tactile; pins 1/2 one pole, 3/4 other; seat flush |
| **LED1** | 1 | Kingbright L-934GD 3 mm green | Cathode (short lead) to pad 1 and K mark |
| **LED2** | 1 | Kingbright L-934YD 3 mm yellow | Cathode (short lead) to pad 1 and K mark |
| **LED3** | 1 | Kingbright L-934ID 3 mm red | Cathode (short lead) to pad 1 and K mark |

### Soldering procedure

1. **Inspect through-hole pattern before soldering.** Confirm all holes are open and lead diameters fit (0.5–1.0 mm leads standard for these parts). Test-fit J1, J2, J3 connectors to ensure alignment.

2. **Solder connectors (J1, J2, J3):**
   - Heat both pad and lead together for 3–5 seconds
   - Apply solder and fill each hole; use minimal solder to avoid bridges to adjacent pins
   - Pin 1 identification: square pad on both sides of connector; verify alignment with silkscreen outline
   - Allow to cool; do not disturb while solidifying

3. **Solder capacitor C1 (electrolytic):**
   - **Polarity critical:** Positive lead (longer leg, + mark on can) goes to square pad (pad 1)
   - Negative lead to the other pad
   - Heat both pads; apply solder; cool
   - If mechanical orientation is tight, solder one lead first, verify polarity, then solder the other

4. **Solder potentiometers (RV1, RV2):**
   - **Non-standard lead order:** Physical leads left-to-right when viewed from above are 1–3–2 (NOT 1–2–3)
   - Pad 1 (left) and pad 3 (right) are the voltage divider; pad 2 (center) is the wiper
   - RV1 wiper (pad 2) must connect to TP6 (threshold voltage)
   - RV2 wiper (pad 2) must connect to VDELAY node (timer)
   - Solder all three leads; verify no bridges between wiper and end terminals
   - Do not assume a standard 3-lead potentiometer pinout

5. **Solder switch (SW1):**
   - Omron B3F-1000 has four leads: pins 1/2 form one pole (one side of switch when viewed from above); pins 3/4 form the other pole (other side)
   - Seat the switch flush to the PCB (do not leave gap; plunger should move freely without binding)
   - Solder all four leads; verify no shorts between the two poles

6. **Solder LEDs (LED1, LED2, LED3):**
   - **Polarity critical:** Cathode (short lead, flat side of lens) goes to pad 1 (square pad, K mark on silkscreen)
   - Anode (longer lead) to the other pad
   - Solder both leads; cool
   - Do not bend leads excessively after insertion; use needle-nose pliers to hold near the board if needed
   - LEDs do not tolerate reverse polarity; verify before powering up

### Post-soldering inspection

- Visually inspect all solder joints for continuity and no bridges
- Check no leads are floating or cold-soldered
- Verify J1, J2, J3 pins are fully seated and aligned
- Confirm trimmer leads are not bent or folded (no mechanical stress)
- Test continuity: J1.1 to GND, J1.2 to GND (should be zero ohms); J3.1 to J3.2 through the board (should show low resistance of traces/vias)

---

## Motor harness assembly and suppression

The GROTHEN G528 pump is a brushed DC motor with commutator noise. Without motor-end suppression, transients can couple into the logic rails and cause false triggers.

See `../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/customer/MOTOR_HARNESS_SUPPRESSION.md` for full instructions.

### Motor-end components (NOT on PCB)

| Component | Specification | Purpose |
|---|---|---|
| **Flyback diode** | Schottky, 2–3 A, 20 V minimum; cathode to motor positive, anode to motor negative | Clamps inductive spike when motor current switches off |
| **Capacitor** | 100 nF ceramic, 25 V minimum, X7R or C0G, mounted directly across motor tabs | Shunts high-frequency motor switching noise |
| **Twisted pair** | Positive and negative pump leads from J3 to motor; keep leads as short and close as possible | Reduces loop inductance and EMI coupling |
| **Strain relief** | Transfers mechanical load to enclosure/bag structure, NOT to J3 connector or motor tabs | Prevents connector wear and wire fatigue |

### Harness pinout

| J3 pin | Label | Connects to |
|---:|---|---|
| 1 | PUMP+ | Motor positive; diode cathode |
| 2 | PUMP_SW_NEG | Motor negative; diode anode |

### Assembly sequence

1. **Prepare the harness at motor end** before connecting to the board
2. **Install flyback diode** (Schottky, 2–3 A, 20 V+) across motor terminals with correct polarity:
   - Cathode (band marked on diode) connects to motor positive
   - Anode connects to motor negative
   - Test polarity with a multimeter in diode mode before soldering
3. **Install bypass capacitor** (100 nF ceramic, 25 V+) directly across motor terminals with leads kept as short as practicable (<10 mm total)
4. **Twist positive and negative pump wires** tightly together from J3 to the motor (aim for 5–10 twists per inch)
5. **Solder or crimp the harness to J3 connectors:**
   - Verify J3 polarity matches motor wiring (positive to pin 1, negative to pin 2)
   - Ensure no shorts across J3
6. **Install strain relief** at the enclosure/bag, not at J3 or the motor. Transfer all mechanical pull force to the structure.

### Inspection and acceptance

- Power off and verify diode polarity with a multimeter before connecting the motor
- Confirm no short across J3 (should read high impedance unpowered)
- Start on a current-limited 5 V supply (100–300 mA budget)
- Scope J3 pin 2, +5V_LOGIC, DET_N, and RESET_N during at least 100 rapid pump cycles
- Reject any build showing false detection, unexpected rail resets, unexpected pump pulses, or excessive diode/MOSFET temperature rise
- **Never place a fluid joint above the controller.** Keep pump wiring physically separated from J2 (sensor) and the ACS signal harness.

---

## Reproduction and rebuild procedure

The v1.2 design can be reproduced from deterministic scripts if the v1.1 baseline is available.

### Source location

`../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/source/repro/`

**Files:**
- `circuit.tsx` — TypeScript circuit definition (reference authoring, not the manufacturing entry point)
- `correct_u1.py` — Python script applying explicit U1 footprint, mask, courtyard, routing, via, and revision-text changes
- `repour.mjs` — Node.js script regenerating bottom GND copper pour only
- `export_final.mjs` — Exports Gerbers (copper, mask, paste, drill), KiCad, and drawings
- `make_drawings.py` — Builds assembly PDF from numbered pads (avoids generic corner markers)
- `rebuild.sh` — Orchestration script
- `package-lock.json` — Pinned npm dependencies
- `v1_1_baseline.circuit.json` — Input circuit (v1.1, unchanged in v1.2 logic)

### Dependencies

- Node.js (npm)
- Python 3 with: `gerbonara`, `shapely`, `reportlab`
- DejaVu Sans fonts (Linux/macOS standard; Windows may require manual install)

### Build steps

```bash
cd source/repro/
npm ci                  # Install pinned dependencies
bash rebuild.sh        # Apply ECO and export
```

**Output:**
- `../BubbleLink_CTRL_v1_2_FINAL.circuit.json` — Routed circuit with U1 correction
- Gerber, drill, KiCad, and PDF files in parent directory

### Verification after rebuild

- Regenerated files have new export timestamps and ZIP metadata. **Do not silently accept hash changes.**
- Review the regenerated data (Gerber previews, copper geometry, drill counts)
- Rerun verification checks: `manufacturing_qa_results.json` must show all 50 PASS
- Intentionally freeze a new release if any design changes are made
- The supplied checksums in `SHA256SUMS.txt` bind the released files; deviations must be reviewed and re-signed

### Important limitations

- `circuit.tsx` is an authoring reference for documentation and review; it is **not** the exact manufacturing entry point
- The manufacturing baseline is `v1_1_baseline.circuit.json` plus deterministic ECO scripts
- **Do not hand-edit** intermediate files between `correct_u1.py` and final export
- Internal v1_1 net identifiers are intentionally retained as internal-only identities (not stale geometry references)

---

## Related documentation

- **BOM and parts:** `docs/07-pcb/bom-and-parts.md`
- **Bringup and acceptance test:** `docs/07-pcb/bringup-and-acceptance-test.md`
- **Engineering change detail:** `hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/ENGINEERING_CHANGE_AND_REVIEW.md`
