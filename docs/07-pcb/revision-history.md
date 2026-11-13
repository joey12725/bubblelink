# BubbleLink CTRL PCB — revision history

This document records the release and revision status of the BubbleLink CTRL printed circuit board. The focus is on the final design state and the engineering decisions that led to v1.2, the current fabrication release.

---

## v1.1 Release (August 2026)

**BubbleLink CTRL v1.1** was the initial design-ready release of the automatic pump controller, submitted to PCBWay for fabrication on **August 6, 2026**. The design is a dual-comparator architecture for gun-current detection and timed pump control, with brownout supervision and fail-safe logic ensuring the pump does not run if the controller loses power or the gun is unplugged.

v1.1 included:

- Dual open-drain comparator (U1: TI TLV1822QDRQ1) for sensor threshold comparison and timer logic
- 4.38 V supply supervisor (U2: TLV803E) with 200 ms delay for controlled shutdown during brownout
- Adjustable detection threshold (RV1, 2 kΩ, 25-turn 3296W trimmer) tunable to each gun's noise floor
- Adjustable pump-delay timer (RV2, 100 kΩ, 25-turn 3296W trimmer), target 350 ms ±50 ms
- 1.5 A polyswitch fuse (F1) on the pump branch, protection against sustained overload
- Schottky flyback diode (D1) and 100 nF capacitor (C9) at the pump connector
- Three status LEDs (power, detection, pump)
- Manual PRIME button for testing and priming the pump
- Four M3 mounting holes (3.2 mm NPTH) on a 43 × 33 mm pattern
- 50.0 × 40.0 mm board, 1.6 mm FR-4, 2-layer, 1 oz copper, lead-free HASL

---

## Engineering Hold: U1 Footprint Discovery (September 2026)

After submitting v1.1 to PCBWay, the manufacturer flagged a critical mismatch: the PCB's SOIC-8 footprint for U1 had 4.30 mm spacing between opposite pad rows, while the TI TLV1822QDRQ1 datasheet (D0008A land pattern) specifies 5.40 mm.

**Root cause:** The footprint was generated from a generic `soic8` template that did not match TI's specific land pattern for this device.

**Why substitution was not an option:**

The TLV1822-Q1 was selected for specific electrical properties integral to the design:

- Rail-to-rail input operation (measures 0–5 V sensor signal without a scaling amplifier)
- Very low input bias current (avoids large offset errors in the ~100 kΩ threshold network)
- Open-drain outputs (allow direct, low-impedance HOLD charge/discharge and Schmitt feedback)
- Industrial/automotive temperature range and defined high-impedance power-on-reset behavior
- Compatibility with the TLV803 supervisor's fail-off startup design

These properties were essential and could not be compromised in the 4.30 mm footprint without requiring circuit re-qualification.

---

## v1.2 Engineering Change (September 9, 2026)

**BubbleLink CTRL v1.2** incorporates the corrected U1 footprint and supporting layout repairs. The decision was made to keep the TLV1822QDRQ1 unchanged and regenerate the PCB with exact TI D0008A land geometry.

### U1 footprint correction

The v1.2 PCB replaces the generic SOIC-8 pads with the exact TI D0008A specification:

| Parameter | v1.1 Gerber | v1.2 Revised | Change |
|-----------|----------|----------|--------|
| Opposite-row center distance | 4.30 mm | 5.40 mm | +1.10 mm |
| Copper length across package | 1.00 mm | 1.55 mm | +0.55 mm |
| Copper width along row | 0.60 mm | 0.60 mm | — |
| Inner copper gap | 3.30 mm | 3.85 mm | +0.55 mm |
| Outer copper span | 5.30 mm | 6.95 mm | +1.65 mm |
| Mask expansion per side | nominal zero | 0.075 mm | +0.075 mm |
| Same-row lead pitch | 1.27 mm | 1.27 mm | — |

U1's component centroid, CPL rotation angle (90°), and all electrical signals remain unchanged.

### Supporting routing and via adjustments

Three signal vias relocated to maintain 0.200 mm minimum clearance from the expanded U1 pads:

| Via | Original position | Revised position | Reason |
|-----|--|--|---|
| pcb_via_search_19 | (-10.70, 5.00) | (-10.40, 5.55) | Clearance from expanded U1 pin 8 |
| pcb_via_search_48 | (-9.00, 4.90) | (-9.00, 5.45) | Clearance from expanded U1 pin 6 |
| pcb_via_search_24 | (-17.70, 10.30) | (-17.40, 10.35) | Via-to-R18 pad clearance correction |

The bottom copper ground pour was regenerated against the revised routing and via positions.

### Manufacturing implications

The complete Gerber, drill, paste, and assembly files were regenerated and re-verified:

- **Gerber changes:** All nine CAM files updated (top/bottom copper, masks, paste, silkscreen, edge cuts, PTH drill, NPTH drill)
- **Paste changes:** All 92 populated SMT apertures remain full-size; U1's eight paste openings now match the corrected copper pads
- **Stencil:** Must be remade from the updated Gerber files; old stencil cannot be reused
- **Drill:** Complete plated and non-plated drill programs must be regenerated; three via locations changed
- **Assembly process:** U1 pin 1 and exact pad coordinates verified in the updated assembly drawing and coordinate CSV

### Verification and frozen release

v1.2 was subjected to automated structural release QA:

- **50 manufacturing checks:** all PASS (configuration, circuit integrity, component topology, trace routing, DRC, manufacture-specific U1 geometry assertion)
- **Electrical model rerun:** 20,000-sample analog circuit simulation with component tolerances, seed 20260807; `model_passed=true`; no analytic failures
- **Geometry regression:** Independent Shapely-based copper separation check confirms ≥0.200 mm top-layer and ≥0.207 mm bottom-layer clearance between different nets
- **Gerber reconciliation:** Actual CAM files decoded with Gerbonara match intended geometry within 0.002 mm
- **Frozen file integrity:** SHA-256 hashes bind all artifacts (Gerbers, BOM, CPL, schematics, design source, assembly notes, test procedures)

---

## Current Status: v1.2 is the Fabrication Release

**v1.2 is the current and only authorized fabrication release.** The design was finalized on September 9, 2026; the replacement PCB order was submitted September 20, 2026, and supersedes v1.1 completely. The first run was 5 boards: 2 assembled by PCBWay and 3 bare spares. The v1.1 bare PCBs are scrap.

### Manufacturing order specifics

| Aspect | Detail |
|--------|--------|
| **Quantity** | 5 boards fabricated; 2 assembled by PCBWay, 3 bare |
| **Order status** | Fabricated, assembled and shipped October 2026 |
| **U1 component** | TI TLV1822QDRQ1 (SOIC-8, confirmed no substitutes) |
| **Exact parts** | C6 (1210), C7 (1206), D1 (custom SMA), F1 (custom 1812 PTC), all critical; no distributor substitutions without written approval |
| **Assembly notes** | C9 (100 nF) and R18 (100 kΩ) must be fitted; J4 and R22 DNP; R22 reserved for future hysteresis tuning |
| **Quality gates** | Bare-board electrical test included; first-article photos approved 2026-10-03 and DFM sign-off completed |

### Build path for users

1. Wait for PCBWay v1.2 delivery (assembled and bare boards).
2. Hand-solder the through-hole components (J1, J2, J3, C1, RV1, RV2, SW1, LED1–LED3) following [fabrication-and-assembly.md](fabrication-and-assembly.md).
3. Perform unpowered inspection, logic-only bring-up, and calibration per [bringup-and-acceptance-test.md](bringup-and-acceptance-test.md).
4. Hang it under the cap of the printed stick (component side up, pushed onto the four printed pins through its mounting holes and heat-staked; see [../09-printed-parts.md](../09-printed-parts.md)), then connect to the ACS758 sensor, pump, and 5 V buck converter.
5. Calibrate RV1 and RV2 to the actual gun and fluid system.
6. Perform full system acceptance test under load.

---

## Design decisions (still valid in v1.2)

- **One pump, always:** The bubble system uses a single GROTHEN G528 peristaltic pump, powered from a 5 V supply provided by Buck A (the YxPC 5 V module).
- **Hall-effect sensor only:** Current detection via ACS758 module, external to the board, measuring combined gun current.
- **Closed-loop detection:** Active gun current detection from the sensor module, not a timer-only fallback. J4 (AUTO/FORCE-ON) is unpopulated (DNP). It's the no-respin fallback if the ACS758 can't reliably detect a very low-current head. Donor heads vary widely, and Joey may put a potentiometer in front of a head to slow it, so some heads may draw too little current to detect.
- **Timed pump cutoff:** The pump runs for a fixed delay after detection stops (default 350 ms), not on demand from a manual valve. This delay allows the last bubble shot to complete before fluid returns to the reservoir.
- **Fail-safe shutdown:** Multiple independent paths ensure the pump stops: U1B timer, U2 brownout supervisor, R15 gate pull-down, R21 charge-dump resistor.

---

## Related documentation

- **Board overview and functional description:** [overview.md](overview.md)
- **Connectors and pinout:** [connectors-and-pinout.md](connectors-and-pinout.md)
- **Bill of materials:** [bom-and-parts.md](bom-and-parts.md)
- **Fabrication and assembly (PCBWay and user THT):** [fabrication-and-assembly.md](fabrication-and-assembly.md)
- **Bring-up and acceptance test:** [bringup-and-acceptance-test.md](bringup-and-acceptance-test.md)
- **Engineering disposition memo (U1 decision):** ../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/ENGINEERING_CHANGE_AND_REVIEW.md
- **Design description (electrical):** ../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/customer/DESIGN_DESCRIPTION.md
