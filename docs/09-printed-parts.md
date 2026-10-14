# 3D-Printed Parts Catalog

BubbleLink system requires thirteen 3D-printed components: battery cartridge assembly (upper and lower cell spacers, enclosure), fluid-system manifold (pump cradle, recirculation restrictor, wet/dry bag divider), connector harness structure (four connector blocks), control mounts, donor sled interface, and cosmetic shells for the Tracer cosplay integration. Tracer shells (ten parts: L1, L2, L3, L6, R1–R6) are already completed. All parts are printed in-house on Creality K2 Plus (350³ mm) or Bambu Lab A1 (256³ mm). Print start priority is immediately upon receipt of PCBs (ETA Oct 15–18); completion is required by **2026-10-19** to allow ten days of assembly integration and testing before the hard **2026-10-29** deadline.

## Printed Parts by Subsystem

### Battery Assembly (3 parts)

| Part | Purpose | Material | Printer | Size | Print Priority | Status | Notes |
|------|---------|----------|---------|------|-----------------|--------|-------|
| **Upper cell spacer** | Mechanical separator between 5×2 cell rows; positions cells at 0.5–1 mm air gap; integrated screw/tie features; rigid two-row ten-cell holder for Samsung 25R cells (18.33 ± 0.07 mm dia., 64.85 ± 0.15 mm H) | PETG or ASA | Creality K2 Plus | ~105 × 50 × 10 mm | **1—Critical path** | Download & remix from Cults3D [18650 Offset Spacer](https://cults3d.com/en/3d-model/tool/18650-offset-spacer); original 8-cell model, requires remix to ten-position (5×2) configuration. FreeCAD source included in download. | Verify remix geometry against printed test-fit with actual 10× Samsung 25R cells. Fish-paper insulator rings separate top/bottom rows (inter-row isolation). |
| **Lower cell spacer** | Identical to upper; provides bottom closure and tie anchor for 2S5P cartridge | PETG or ASA | Creality K2 Plus | ~105 × 50 × 10 mm | **1—Critical path** | Download & remix from Cults3D (same source as upper) | Same remix as upper. Two-piece sandwich holds 10 cells in 2S5P stack. Spot-welded nickel-plated steel tabs bridge series connections (five parallel bridges, no single tab carries full pack current). |
| **Rigid battery cartridge** | Enclosure for 2S5P pack (10× Samsung 25R), BMS, XT60 connector, and USB-C charging input; rigid wall prevents crush and abrasion; internal label area for Sharpie: "2S5P Samsung 25R / 7.2 V nominal / 12.5 Ah / 90 Wh / [build date]" | PETG or ASA | Creality K2 Plus or Bambu Lab A1 (if cartridge >256 mm in any dimension) | ~110 × 80 × 50 mm (external, enclosing 105×75×43 mm internal assembly) | **2—Early** | Needs design | Must fit inside LED pixel backpack (MAX M Style, ~34×20×7 cm internal). Connector pass-through holes for XT60H outlet (unregulated 2S battery) and USB-C inlet (2S 4A charger). Four M3 mounting holes on bottom surface for 5–7 mm standoffs; holes align with PCB bracket pattern (43 × 33 mm spacing per BubbleLink CTRL v1.2 NPTH H1–H4). Lid attachment (snap or screw) TBD. |

### Fluid System (3 parts)

| Part | Purpose | Material | Printer | Size | Print Priority | Status | Notes |
|------|---------|----------|---------|------|-----------------|--------|-------|
| **Pump cradle** | Rigid mount for GROTHEN G528 peristaltic pump (6 V, 150 mL/min, 60×60×50 mm, 69 g); secures pump to pack frame; provides strain relief for inlet/outlet tubing and motor leads | PETG or ASA | Creality K2 Plus | ~70 × 70 × 60 mm | **3—Early** | Needs design | Delivers 5 V from Buck A (via PCB J1) to pump motor (per CTRL v1.2 circuit). Two or three attachment points (M3 screw bosses or snap tabs) to carrier frame. Inlet/outlet barb orientation to align with tubing path (gravity feed from bladder inlet tee). Cable strain relief and routing for motor leads. Test fit with actual delivered pump. |
| **Wet/dry bag divider + electronics tray** | Sandwich layer separating 1 L fluid bladder (above) from electronics compartment (below); provides horizontal support and water barrier; integral tray for PCB, BMS, 5 V bucks (A & B), 30 A breaker, and voltmeter mounts | PETG or ASA | Creality K2 Plus or Bambu A1 | ~100 × 80 × 15 mm base + boss posts | **4—Concurrent with PCB arrival** | Needs design | Three integrated sections: (a) barrier floor with small drainage/vent holes, (b) PCB support posts (four 3.2 mm NPTH holes at ±21.5, ±16.5 mm from center for BubbleLink CTRL v1.2 mounting, matching PCB H1–H4 pattern), (c) component pocket map for IC GOGOGO 2S 40 A BMS, two YxPC 5 V USB bucks, 30 A Type B breaker (72×48×44 mm, M6 studs), and Stlxy DC 4–100 V voltmeter head. Thickness 3–5 mm; water-tolerant PETG recommended. |
| **Pump inlet check valve restriction clamp** (adjustable pinch restrictor) | Screw-type tube clamp on recirculation inlet tee (after 4 mm check valve); permits field calibration of bypass flow (target 5–10 mL/min excess capacity); enables smooth donor activation without force-feeding | TPU or flexible PETG | Bambu Lab A1 | ~30 × 20 × 15 mm (screw-handle clamp) | **3—Concurrent with pump** | Needs design | Adjustable screw restricts 3.5 mm ID silicone tubing; range 0–fully-closed (must not permanently restrict pump outlet). Field-tunable; after final flow measurement, may be replaced with fixed-capillary restrictor. Test with actual G528 pump to confirm bypass behavior. |

### Harness & Connectors (4 parts)

| Part | Purpose | Material | Printer | Size | Print Priority | Status | Notes |
|------|---------|----------|---------|------|-----------------|--------|-------|
| **Pack-side pump/hose/tether connector block** (×1) | Three-way junction at pump inlet; integrates: 4 mm hose barb (inlet from bladder tee, outlet toward gun tee), pump motor 5 V lead anchor, and paracord anchor (to umbilical load tether). Hub between pump cradle and fluid path. | TPU or flexible PETG | Bambu Lab A1 | ~40 × 35 × 30 mm | **4—Concurrent with pump cradle** | Needs design | Hose barb 4 mm (pump outlet is 3×5 mm; use automotive reducer 3→4 mm or rebarb). Pump motor 5 V leads pass through to PCB J1 (via Buck A); cable strain relief. Paracord anchor for load-bearing tether (4 mm 550-type paracord rated ~150 kg). Test fit with actual pump and tubing. |
| **Pack-side gun-channel connector block** (×2, one per gun channel) | Two-way junction integrating: one XT30U power connector (raw 2S bus, unregulated 6.0–8.4 V per channel), one 4 mm hose barb for donor pump inlet feed (from pump outlet Y-splitter tee). One unit per left/right umbilical. | TPU or PETG | Bambu Lab A1 | ~35 × 25 × 20 mm each | **5—Late (after harness layout)** | Needs design | One per gun channel (left and right). XT30U female mating socket (mates to PCB XT30U male outputs, one per channel, fused internally at 15 A nominal per channel per PCB). Hose barb 4 mm for 3.5 mm ID tubing (donor pump intake line). Cable strain relief; umbilical routing anchor. Verify actual gun current profile to confirm XT30U rating adequacy. |
| **Gun-side connector block** (×2, one per donor head) | End-of-umbilical junction block; integrates: XT30U male connector (mating to pack female XT30U), 4 mm hose barb (mating to donor pump inlet line), and mechanical anchor for sled mounting (zip-tie slot or friction snap). | TPU or PETG | Bambu Lab A1 | ~40 × 30 × 30 mm each | **5—Late (after donor selection)** | Needs design | Two identical units, one per donor gun (left/right channels). XT30U male connector for power return to pack. Hose barb 4 mm for 3.5 mm tubing (donor intake line). Mechanical strain-relief clamping for paracord load-bearing tether (anchors to sled). Hose entry strain boot optional (TPU overmold or printed flexible lip). |
| **Pinch clamp for unused-channel shutoff** (×2, one per gun outlet if both channels used) | Screw-type tube clamp on each gun-channel outlet hose line; enables manual per-channel shutoff without purchased valves; field-operator can restrict or stop flow to unused or dormant head during performance | TPU or flexible PETG | Bambu Lab A1 | ~25 × 20 × 15 mm each | **5—Late (after harness layout)** | Needs design | Two units, one per gun channel outlet (post-tee, before gun entry). Screw handle pinches 3.5 mm tubing; range 0–fully-closed. If only one gun is active, the other channel outlet remains clamped closed. Alternative: may be replaced with fixed-capillary restrictor or needle valve after field testing; printed clamp is MVP for manual control. Test with actual tubing and donor pump back-pressure. |

### Control & Mounts (6 parts)

| Part | Purpose | Material | Printer | Size | Print Priority | Status | Notes |
|------|---------|----------|---------|------|-----------------|--------|-------|
| **BubbleLink CTRL PCB mount bracket** | Four-corner standoff frame; secures 50×40×1.6 mm PCB at 5–7 mm above wet/dry divider tray; mounting holes match PCB NPTH pattern (H1–H4 at ±21.5, ±16.5 mm from center = 43 × 33 mm spacing). Rigid PETG. | PETG | Creality K2 Plus or Bambu A1 | ~60 × 50 × 8 mm (including corner bosses) | **4—Concurrent with divider** | Needs design | Four 3.2 mm NPTH holes at exact ±21.5, ±16.5 mm spacing per BubbleLink CTRL v1.2 mounting-hole pattern (from PCBWay package, verified 2026-10-14). Mount height sets PCB clearance for J1/J2/J3 connector access below. M3 screws + standoffs (user-supplied, ~5–7 mm height). Test-fit with actual PCB. |
| **Mounting pad for 5V buck converter (Buck A, pump supply)** | YxPC 6–20V to 5V USB buck module mounted on L-bracket or pad anchor near PCB and pump cradle. Output feeds PCB J1 (5 V/GND), which powers logic and the pump branch. | PETG | Bambu Lab A1 | ~40 × 25 × 15 mm | **4—Concurrent with PCB** | Needs design | L-bracket or snap-fit pad; allow airflow around converter for thermal dissipation. Input ~6–8.4 V from raw battery (via main breaker, 12 AWG line). Screw or snap attachment to tray. Verify delivered buck output voltage <5.25 V (PCB ceiling). |
| **Mounting pad for 5V buck converter (Buck B, LED backpack supply)** | Identical L-bracket or pad anchor for second YxPC 6–20V to 5V USB buck (isolation stage); powers LED pixel backpack display (~2–3 W average, 4 W ceiling per FACTS.md) separately from pump rail | PETG | Bambu Lab A1 | ~40 × 25 × 15 mm | **4—Concurrent with PCB** | Needs design | Identical design to Buck A or side-by-side/stacked layout if space permits. Input same ~6–8.4 V source (post-breaker, parallel connection). Output to USB-A socket or USB-C cable (target 5 V, ~1 A). Verify delivered buck output <5.25 V. Thermally space from Buck A if stacked. |
| **Digital voltmeter mount** | Circular faceplate bracket for Stlxy DC 4–100V LED voltmeter head (red, ~38 mm dia.); exterior-facing display on pack side or back panel; two-wire signal anchor | PETG | Bambu Lab A1 | ~50 × 50 × 20 mm (faceplate + bracket) | **5—Late (after tray layout)** | Needs design | Faceplate with circular window cutout matching voltmeter head OD. Signal wires (two-wire direct from battery XT60H outlet) routed through bracket channel/strain relief. Display face outward-facing for real-time battery voltage visibility. Protective bezel lip prevents water intrusion. Test-fit with actual delivered voltmeter head. |
| **Breaker (30A Type B-30A) mechanical mount** | Clip or pad bracket for YONGRUN Type B-30A manual-reset circuit breaker (12–48V, 72×48×44 mm, M6 threaded studs); secures breaker in accessible location within electronics compartment for user reset capability | PETG | Creality K2 Plus or Bambu Lab A1 | ~80 × 55 × 30 mm (bracket + retention pad) | **4—Concurrent with divider** | Needs design | Breaker input/output via SC10-6 copper ring lugs (10 mm² barrel, M6 hole, solder-filled per FACTS.md). Print bracket anchors breaker body without restricting manual reset button. Thermal spacing if stacked with bucks. Input from main 12 AWG line (from battery via BMS). Output to XT30U distribution or high-current nodes. Test-fit with actual breaker (user-supplied). |
| **Donor sled interface** (×2, one per gun) | Flat adapter plate (30 × 20 mm, four M3 holes at corners) that bridges donor gun body to umbilical connector block; provides mechanical load-path anchor for paracord tether and structural support for donor mounting and field sled swapping | PETG | Bambu Lab A1 | 30 × 20 × 5 mm (flat plate with four corner M3 bosses) | **5—Late (after donor selection)** | Needs design | Standard interface per Rev 2.4 platform spec: 30 × 20 mm footprint, four M3 holes for mechanical fastening (M3 screws, 6–8 mm length). Mounts to gun-side connector block and receives paracord load-bearing tether anchor loop. Two identical units, one per left/right gun. Verify actual gun body geometry to confirm mounting hole positions after donor is selected. |

### Cosmetic & Enclosure (10 parts: Tracer shells)

| Part | Purpose | Material | Printer | Size | Print Priority | Status | Notes |
|------|---------|----------|---------|------|-----------------|--------|-------|
| **Tracer cosplay bubble-gun shells (×10 parts: L1, L2, L3, L6, R1–R6)** | 3D-printed hollow bodies for Overwatch Tracer gunplay cosplay prop; bubble-gun donor heads mount internally; 2 m COB light-blue 5V LED strip integration (cosmetic only, not part of bubble system); non-functional cosmetic details (armor plating, scope, details) | White PETG (durable for repeated handling and display; not ABS) | Creality K2 Plus (350 mm capacity primary) | Individual part sizes: ~80–150 mm per file | **0—Already complete** | Printed & completed (as of 2026-08-06) | Ten files (L1, L2, L3, L6, R1–R6) already printed on Creality K2 Plus in white per Codex notes (2026-08-06). L1/L2/L3/L6 are helmet left-side armor pieces; R1–R6 are right-arm gun shells. Assembly pending: donor bubble-gun heads mount inside gun shells (R1–R3 or subset thereof); 2 m COB ice-blue 5V LED strip adheres to interior. Separate project; not part of core BubbleLink pump/battery/controller system. |
| **Control panel / LCD faceplate** (optional, non-critical) | Printed bracket or cover for optional display/control panel (voltmeter, status LEDs, prime button interface) on pack exterior if separate control interface desired | PETG | Bambu Lab A1 | ~80 × 60 × 10 mm (faceplate) | **6—Optional** | Needs design (deferred if basic manual controls sufficient) | Non-critical for MVP; primary control via manual gun triggers + pump prime button on PCB. If separate status display desired, faceplate integrates LED window cutouts (POWER, GUN ACTIVE, PUMP ACTIVE) and prime-button pass-through. Voltmeter already integrated in dedicated mount (part above). |

---

## Print Sequence & Timeline

### Status: CAD paused 2026-10-11; ready to resume

As of **2026-10-11**, all BubbleLink CAD design work was paused pending purchase details. This document and the ORDER_LEDGER now provide those details. CAD can resume now, at Joey's call. Most parts don't depend on the boards; only the PCB mount needs a physical board check, and its hole pattern is already known (43.0 × 33.0 mm, 3.2 mm holes). Boards are due **Oct 15–18**.

### Critical Path (Oct 15–19: PCBs arrive through print deadline)

**Printer: Creality K2 Plus (primary, 350×350×350 mm capacity)**

Upon PCB receipt (Oct 15–18), print in this order:

1. **Upper & lower cell spacers (2×, ~4 hours total)**
   - Download & remix Cults3D 18650 Offset Spacer to 5×2 ten-cell configuration
   - FreeCAD source included; remix must preserve mounting hole spacing
   - Test-fit immediately against actual 10× Samsung 25R cells upon completion

2. **Rigid battery cartridge (1×, ~6–8 hours)**
   - Awaits cell-spacer test fit before finalizing height/wall thickness
   - Dimensions verified against MAX LED pixel backpack internal geometry (~34×20×7 cm)
   - Connector pass-throughs: XT60H outlet (unregulated 2S), USB-C inlet (charger)

3. **PCB mount bracket (1×, ~2–3 hours)**
   - Four M3 NPTH holes at ±21.5, ±16.5 mm spacing (43 × 33 mm pattern per BubbleLink CTRL v1.2)
   - Measure delivered PCB holes before printing for confirmation

4. **Pump cradle (1×, ~4 hours)**
   - Test-fit with delivered GROTHEN G528 pump
   - Motor lead routing to PCB J1 (5 V supply via Buck A)
   - Inlet/outlet barb alignment with tee network

5. **Wet/dry divider + electronics tray (1×, ~5–6 hours)**
   - Four M3 support posts matching PCB bracket mounting pattern
   - Component pocket layout for BMS, buck A/B, breaker, voltmeter
   - Await PCB + BMS arrival for final internal geometry confirmation

6. **Pinch restrictor clamp (1×, ~2 hours; tuning variant)**
   - Screw-type restrictor on inlet tee recirculation line
   - Test with actual pump and tubing; field-adjustable

### Secondary Path (Oct 17–19: Bambu Lab A1 parallel printing)

**Printer: Bambu Lab A1 (256×256×256 mm capacity) — parallel to K2**

7. **Pack-side pump/hose/tether block (1×, ~3 hours)**
8. **Pack-side gun-channel connector blocks (2×, ~4 hours total)**
9. **Gun-side connector blocks (2×, ~4 hours total)**
10. **Unused-channel blocks (2×, ~2 hours total)** if second gun channel unused
11. **Pinch clamps for gun outlets (2×, ~2 hours total)**
12. **Buck converter mounts A & B (2×, ~3 hours total)**
13. **Voltmeter circular faceplate (1×, ~2 hours)**
14. **Breaker mechanical bracket (1×, ~2 hours)**
15. **Donor sled interface (2×, ~2 hours total)**
16. **Control panel faceplate (optional, 1×, ~2 hours)** — defer if MVP manual controls sufficient

### Print Completion Deadline: Oct 19, 2026 (10 days before project hard deadline)

All functional printed parts (except optional control panel) must be complete, fit-tested against delivered hardware, and ready for assembly integration by **Oct 19, 2026**. This allows **10 days** (Oct 19–29) for:
- Hand-soldering THT components to PCBs (J1–J3, C1, RV1/RV2, SW1, LED1–3)
- Attaching M3 standoffs and brackets to printed parts
- Integrating battery cartridge, BMS, pump cradle, wet/dry tray, and PCB assembly
- Testing fluid path continuity and electrical function
- Cosmetic assembly (Tracer armor shells, LED strip integration)
- Final commissioning and field checkout

**If a critical part fails printing after Oct 18:** hand-fabrication fallback (milled acrylic, service print, glued PVC/TPU) may be required to meet the Oct 29 deadline.

---

## Material & Printer Selection Guidelines

### Material Choice

- **PETG:** Default for structural parts (cell spacers, battery cartridge, pump cradle, electronics tray, mounts). Good strength, temperature tolerance (up to ~80 °C), low moisture absorption. Recommended for parts exposed to ambient humidity or minor heat from electronics.
- **ASA:** Alternative for battery cartridge and cell spacers if UV resistance desired (outdoor festival use, cosplay display). Higher temperature tolerance (~100 °C). Slightly more brittle than PETG; adequate for compression-loaded spacers.
- **TPU (flexible):** Restrictor clamp, unused-channel clamp, hose connector blocks (strain-relief junctions). Flexibility prevents hose shearing at bends; durability for repeated use.
- **White ABS/PETG/Nylon:** Tracer shells already completed; no change recommended.

### Printer Selection

- **Creality K2 Plus (350³ mm):** Primary. Battery cartridge, cell spacers, pump cradle, wet/dry divider, PCB mount bracket, pinch restrictor. Better for large/tall prints and long duration runs (8+ hours).
- **Bambu Lab A1 (256³ mm):** Secondary/parallel. Smaller connector blocks, buck mounts, voltmeter/breaker mounts. Faster peel cycles; good for quick iterations (pinch restrictor calibration). Parts requiring TPU flex printing.

### Quality & Fit Checkpoints

**Immediate upon print completion (same day):**

1. **Cell spacers:** Insert into actual Samsung 25R cell pack; verify 0.5–1 mm air gap, screw/tie features seated, no cell wrapper abrasion.
2. **Battery cartridge:** Fit cell pack assembly inside, verify lid closure, connector pass-through alignment (XT60 outlet, USB-C inlet), standoff boss clearance for M3 screws.
3. **PCB bracket:** Measure NPTH distances against PCB release package (±21.5, ±16.5 mm, ±0.3 mm tolerance); test M3 mounting hardware.
4. **Pump cradle:** Fit GROTHEN G528 pump (60×60×50 mm, 69 g); verify cable routing and inlet/outlet port accessibility.
5. **Wet/dry divider:** Fit PCB bracket and tray into main carrier frame; verify compartment volumes (estimate ~3–3.5 L usable space for 1 L fluid bladder + 2 L electronics/battery).

**Within 24 hours if fit issues:**

- Re-slice and re-print failed parts (tolerance issues, dimensional errors).
- Modify CAD and iterate (design revisions per fit feedback).

---

## Design Status & Dependencies

### Requires Download & Remix (Not Custom CAD)

1. **Upper & lower cell spacers** — Download Cults3D [18650 Offset Spacer](https://cults3d.com/en/3d-model/tool/18650-offset-spacer); FreeCAD source available. Remix from 8-cell to 5×2 ten-cell configuration (nominal dimensions ~105 × 50 × 10 mm per spacer). Test-fit against actual Samsung 25R cells (18.33 ± 0.07 mm dia., 64.85 ± 0.15 mm H).

### Already Completed (No Further Work)

1. **Tracer cosplay shells (×10: L1, L2, L3, L6, R1–R6)** — Printed 2026-08-06 on Creality K2 Plus in white. Assembly pending: donor bubble-gun heads + 2 m COB ice-blue 5V LED strip integration inside gun shells.

### Needs design

1. **Rigid battery cartridge** — Enclosure: 2S5P pack (10× Samsung 25R) + IC GOGOGO 2S 40 A BMS + XT60H outlet + USB-C inlet; lid attachment TBD (snap or screw); mounting holes for battery-cartridge M3 studs; fit within MAX LED pixel backpack (~34×20×7 cm internal)
2. **Wet/dry divider + electronics tray** — Barrier floor with vent holes; four M3 posts at ±21.5, ±16.5 mm spacing; component layout for BMS, Buck A/B, breaker (72×48×44 mm, M6 studs), voltmeter head
3. **Pump cradle** — GROTHEN G528 motor mount, 5 V lead anchor, inlet/outlet tee barb routing, cable strain relief
4. **Pack-side pump/hose/tether block** — Hose barb (3×5 mm pump outlet → 4 mm junction), pump motor lead anchor, paracord tether loop (4 mm 550-type)
5. **Pack-side gun-channel connector blocks (×2, left/right)** — XT30U female socket (PCB output), 4 mm hose barb (to donor pump inlet), cable strain relief
6. **Gun-side connector blocks (×2, left/right)** — XT30U male (mating to pack female), 4 mm hose barb (to donor intake), sled attachment anchor
7. **Unused-channel connector blocks (×2)** — XT30U male, 4 mm hose barb, paracord tether anchor (if second gun channel used; otherwise may be omitted)
8. **Pinch clamp for inlet restrictor** — Screw-type 3.5 mm tube clamp on recirculation tee inlet; field-adjustable (0–fully-closed); test with G528 pump and tubing
9. **Pinch clamps for gun-channel outlets (×2)** — Screw-type clamps for manual per-channel shutoff (alternative to purchased valves)
10. **Buck converter mounts (A & B)** — L-brackets for YxPC 6–20V to 5V USB bucks; thermal spacing; output routing (A → PCB J1, B → backpack USB)
11. **Voltmeter circular faceplate** — Stlxy DC 4–100V LED head mount; circular window cutout; two-wire signal anchor; bezel lip for water protection
12. **Breaker mechanical bracket** — YONGRUN Type B-30A mount; M6 stud access (ring-lug crimped 12 AWG); reset-button clearance; thermal spacing from bucks
13. **PCB mount bracket** — Four-corner standoff frame; 3.2 mm NPTH at ±21.5, ±16.5 mm (43 × 33 mm spacing per BubbleLink CTRL v1.2 NPTH H1–H4)
14. **Donor sled interface (×2)** — 30 × 20 mm flat plate, four M3 corner holes; tether anchor loop; one per left/right gun
15. **Control panel faceplate (optional)** — Status LED window cutouts (POWER/GUN/PUMP), prime-button pass-through; defer if MVP manual controls sufficient

### Critical Measurements (Delivered Hardware)

Verify immediately upon receipt:

1. **Samsung 25R cells:** Wrapper diameter (nominal 18.3 mm; measure cold state) and height (nominal 64.85 mm)
2. **Battery cartridge:** Assembled pack dimensions with spacers + BMS + XT60H connector; XT60H external envelope (polarity marker height, lead solder-pad offset)
3. **GROTHEN G528 pump:** Delivered motor voltage marking (confirm **6 V**, not 12 V per seller artwork); motor footprint and screw-hole pattern; inlet/outlet barb type and size
4. **IC GOGOGO BMS:** Delivered board type (confirm **2S 8.4 V Li-ion**, not LiFePO₄); dimensions; terminal locations and wire gauges
5. **YxPC 5V bucks (×2):** Delivered output voltage under nominal load; verify <5.25 V (PCB ceiling)
6. **YONGRUN 30A breaker:** M6 stud thread pitch and height; manual reset button height and throw; internal switching current rating
7. **Stlxy voltmeter head:** Actual diameter and depth; two-wire connector gauge; display window placement
8. **PCB NPTH holes (H1–H4):** Measure delivered board against mounting-hole pattern (±21.5, ±16.5 mm from origin = 43 × 33 mm spacing); verify 3.2 mm diameter
9. **Silicone tubing 3.5×5.5 mm:** Delivered OD true size (confirm 5.5 mm nominal for 4 mm barb compatibility)
10. **XT30U connectors:** Delivered housing width/height; mating surface geometry for printed block integration

---

## Print Failure & Rework Contingency

- **Estimated total print time:** ~55–70 hours (single printer sequential)
- **Parallel printing (K2 + A1, Oct 15–19):** ~35–40 hours wall time for 13 functional parts
- **Contingency buffer:** 10% re-print allowance (5–7 hours) for failed/misfit parts
- **Last-start deadline for critical-path re-print:** **Oct 17, 2026** (48 hours to Oct 19 print deadline)
- **Last-start deadline for secondary-path re-print:** **Oct 18, 2026** (24 hours to Oct 19 deadline)

**Optional parts (control panel faceplate) may be deferred** without jeopardizing build completion if print queue fills.

If a critical battery/pump/PCB-related part fails after **Oct 17**, hand-fabrication fallback (milled acrylic, third-party 3D print service, glued PVC/TPU) may be required to meet the **Oct 19 print deadline** and maintain the Oct 29 final-build target.

---

## References & CAD Sources

- **Cults3D 18650 Offset Spacer:** https://cults3d.com/en/3d-model/tool/18650-offset-spacer (FreeCAD source included; remix to 10-cell configuration required)
- **BubbleLink CTRL v1.2 PCB v1.2 Package:** `bubblelink/hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/` (mounting-hole pattern H1–H4 at ±21.5, ±16.5 mm from origin; PCB 50 × 40 × 1.6 mm)
- **Tracer Cosplay Shell Models (Iván Ruiz Peón Armor Kit):** `<cosplay-armor-kit>/` (10 STL files: L1–L6, R1–R6; already printed Aug 2026)

