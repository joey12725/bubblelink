# PCB Bill of Materials and Components

Complete inventory of all electronics ordered for the BubbleLink CTRL v1.2 board: 41 top-side surface-mounted parts (fabricated and assembled by PCBWay), 11 through-hole parts (installed by hand post-assembly), 2 do-not-place parts (reserved for future tuning), and 15 test points.

## Surface-mounted components (PCBWay assembly, 41 parts)

These parts are placed and soldered by PCBWay on the top layer only. All centroids and rotation angles are frozen from v1.1 and remain unchanged in v1.2; the U1 footprint correction affects only pad geometry and nearby routing, not placement coordinates.

| Item | Reference Designator | Qty | Manufacturer | MPN | Description | Package | Substitution |
|------|----------------------|-----|--------------|-----|-------------|---------|---|
| 1 | U1 | 1 | Texas Instruments | TLV1822QDRQ1 | Dual open-drain comparator, rail-to-rail | SOIC-8 D0008A | NO SUBSTITUTE |
| 2 | U2 | 1 | Texas Instruments | TLV803EA43DBZR | 4.38 V supervisor, 200 ms delay; DBZ pinout only | SOT-23-3 DBZ | NO SUBSTITUTE |
| 3 | Q1, Q3 | 2 | Diodes Incorporated | DMP2065UQ-7 | P-channel MOSFET | SOT-23 | NO SUBSTITUTE WITHOUT WRITTEN APPROVAL |
| 4 | Q2 | 1 | Alpha & Omega Semiconductor | AO3400A | N-channel MOSFET | SOT-23 | NO SUBSTITUTE WITHOUT WRITTEN APPROVAL |
| 5 | D1 | 1 | Vishay | B340A-E3/61T | 3 A 40 V Schottky diode, flyback clamp | SMA DO-214AC custom | NO SUBSTITUTE |
| 6 | F1 | 1 | Littelfuse | 1812L150/16DR | 1.50 A hold, 16 V resettable PTC fuse | 1812 custom | NO SUBSTITUTE |
| 7 | FB1 | 1 | Murata | BLM21PG221SN1D | 220 Ω ferrite bead at 100 MHz | 0805 | NO SUBSTITUTE WITHOUT WRITTEN APPROVAL |
| 8 | C2 | 1 | Murata | GRM31CR71C106KA12L | 10 µF 16 V X7R 10% | 1206 | NO SUBSTITUTE WITHOUT WRITTEN APPROVAL |
| 9 | C3, C4, C8, C9, C10, C11, C12 | 7 | Murata | GRM21BR71H104KA01L | 100 nF 50 V X7R 10% | 0805 | EQUIVALENT ALLOWED |
| 10 | C5 | 1 | Murata | GRM21BR71C105KA01L | 1 µF 16 V X7R 10% | 0805 | EQUIVALENT ALLOWED |
| 11 | C6 | 1 | TDK | C3225X7R1E226M250AB | 22 µF 25 V X7R 20% | 1210 | NO SUBSTITUTE WITHOUT WRITTEN APPROVAL |
| 12 | C7 | 1 | TDK | CGA5L1X7R1E685K160AC | 6.8 µF 25 V X7R 10% | 1206 | NO SUBSTITUTE WITHOUT WRITTEN APPROVAL |
| 13 | R14 | 1 | Yageo | RC0805FR-07100RL | 100 Ω 1% | 0805 | EQUIVALENT ALLOWED |
| 14 | R23 | 1 | Yageo | RC0805FR-07560RL | 560 Ω 1% | 0805 | EQUIVALENT ALLOWED |
| 15 | R6, R16, R17, R20 | 4 | Yageo | RC0805FR-072K2L | 2.2 kΩ 1% | 0805 | EQUIVALENT ALLOWED |
| 16 | R7, R8 | 2 | Yageo | RC0805FR-074K7L | 4.7 kΩ 1% | 0805 | EQUIVALENT ALLOWED |
| 17 | R2, R3 | 2 | Yageo | RC0805FR-077K5L | 7.5 kΩ 1% | 0805 | EQUIVALENT ALLOWED |
| 18 | R1, R4, R9, R11, R12, R15 | 6 | Yageo | RC0805FR-0710KL | 10 kΩ 1% | 0805 | EQUIVALENT ALLOWED |
| 19 | R10 | 1 | Yageo | RC0805FR-0739KL | 39 kΩ 1% | 0805 | EQUIVALENT ALLOWED |
| 20 | R18 | 1 | Yageo | RC0805FR-07100KL | 100 kΩ 1% ACS pulldown (MUST BE FITTED) | 0805 | EQUIVALENT ALLOWED BUT MUST BE FITTED |
| 21 | R19 | 1 | Yageo | RC0805FR-07220KL | 220 kΩ 1% | 0805 | EQUIVALENT ALLOWED |
| 22 | R21 | 1 | Yageo | RC0805FR-071ML | 1 MΩ 1% fail-safe | 0805 | EQUIVALENT ALLOWED |
| 23 | R5, R13 | 2 | Yageo | RC0805FR-074M7L | 4.7 MΩ 1% | 0805 | EQUIVALENT ALLOWED |

**Summary:** 41 parts across 23 line items. Zero equivalent substitutions in final design. Solder paste: exactly 92 full-size populated apertures on top; DNP (R22), through-hole, fiducial, and bottom apertures are excluded.

**Critical parts (no substitution allowed):**
- **U1 (TLV1822QDRQ1):** Dual comparator with open-drain outputs and rail-to-rail input; the specific part avoids changing circuit assumptions. Footprint corrected to exact TI D0008A pad geometry: 1.55 × 0.60 mm pads, 5.40 mm opposite-row spacing, 3.85 mm inner gap.
- **U2 (TLV803EA43DBZR, DBZ pinout only):** Voltage supervisor with 4.38 V threshold, 200 ms delay. Do not accept RDBZ or VDBZ variants (different pinouts).
- **Q1/Q3 (DMP2065UQ-7, P-channel)** and **Q2 (AO3400A, N-channel):** Gate drivers with specific threshold and leakage requirements for startup/fail-off logic.
- **D1 (B340A-E3/61T):** Schottky flyback diode rated 3 A, 40 V; cathode to PUMP+.
- **F1 (1812L150/16DR):** Resettable PTC fuse with 1.50 A hold at 20°C, 1.10 A at 50°C; protects pump positive.
- **C6 (C3225X7R1E226M250AB, 22 µF, 1210):** Exact size and dielectric (not C7 footprint).
- **C7 (CGA5L1X7R1E685K160AC, 6.8 µF, 1206):** Exact size and dielectric (not C6 footprint); timer capacitor.

---

## Through-hole parts (customer installation)

These 10 parts (9 BOM lines) are soldered by hand after SMT assembly and must be installed before electrical testing. All are orientation-sensitive; pad 1 is marked with a square pad and/or silkscreen label.

| Item | Reference Designator | Qty | Manufacturer | MPN | Description | Footprint | Polarity |
|------|----------------------|-----|--------------|-----|-------------|-----------|----------|
| 1 | J1, J3 | 2 | JST | B2B-XH-A(LF)(SN) | 2-position vertical XH header, 2.50 mm pitch | Custom THT | Pin 1 to square pad; connector opening must match assembly drawing |
| 2 | J2 | 1 | JST | B3B-XH-A(LF)(SN) | 3-position vertical XH header, 2.50 mm pitch | Custom THT | Pin 1 to square pad; connector opening must match assembly drawing |
| 3 | C1 | 1 | Rubycon | 16ZLH100MEFC5X11 | 100 µF 16 V low-ESR electrolytic | Radial D5 mm P2.0 mm | Positive lead to square pad (pad 1) and + silkscreen mark |
| 4 | RV1 | 1 | Bourns | 3296W-1-202LF | 2 kΩ 25-turn top-adjust trimmer | Bourns 3296W 1-3-2 | **Top view left-to-right pad order 1-3-2; pin 2 is wiper** |
| 5 | RV2 | 1 | Bourns | 3296W-1-104LF | 100 kΩ 25-turn top-adjust trimmer | Bourns 3296W 1-3-2 | **Top view left-to-right pad order 1-3-2; pin 2 is wiper** |
| 6 | SW1 | 1 | Omron | B3F-1000 | 6 × 6 mm momentary tactile switch | Custom 4-pin B3F | Pins 1/2 are one side, 3/4 the other; seat flush to PCB |
| 7 | LED1 | 1 | Kingbright | L-934GD | 3 mm green LED | Radial P2.54 mm | Cathode (short lead, flat side) to pad 1 and K mark |
| 8 | LED2 | 1 | Kingbright | L-934YD | 3 mm yellow LED | Radial P2.54 mm | Cathode (short lead, flat side) to pad 1 and K mark |
| 9 | LED3 | 1 | Kingbright | L-934ID | 3 mm red LED | Radial P2.54 mm | Cathode (short lead, flat side) to pad 1 and K mark |

**Trimmer pad order (critical):** The Bourns 3296W has a non-standard 1-3-2 physical lead layout when viewed from above. Pads must be soldered in physical order 1-3-2, not the standard 1-2-3. Pin 2 is the wiper and must be connected to TP6 (RV1) or VDELAY (RV2).

---

## Do-not-place parts and mechanical features

| Reference | Status | Value or Function | Footprint | Instruction | Reason |
|-----------|--------|-------------------|-----------|-------------|--------|
| R22 | DNP | 4.7 MΩ optional hysteresis resistor | 0805 | LEAVE PADS EMPTY | Reserved for future tuning option; not in PCBWay BOM or CPL. Pads preserved for field modification if needed. |
| J4 | DNP | Optional external prime input | Custom 2-pin 2.50 mm THT | LEAVE HOLES EMPTY | Pads-only fallback; not in customer THT BOM. Allows future AUTO/FORCE-ON override if low-current gun qualification fails. |
| TP1–TP15 | NO COMPONENT | Plated probe-loop test holes | 1.0 mm PTH in 2.0 mm pad | DO NOT PLACE | Fabricated copper features only; labeled test points for commissioning. Not component designators. |
| H1–H4 | NO COMPONENT | Mounting holes | 3.2 mm NPTH | DO NOT PLACE | Mechanical holes (M3 compatible). Four holes form a 43.0 × 33.0 mm rectangle pattern. |
| FID1–FID3 | NO COMPONENT | Local fiducials | 1.0 mm copper, 0.5 mm mask pullback | DO NOT PLACE | Optical assembly alignment features. Not component designators. |

---

## Critical pad-1 coordinates (reference for assembly orientation)

Used to verify correct component placement and orientation during SMT assembly. Coordinates are in millimeters from board lower-left datum (−25, −20 in absolute KiCad; board origin 0,0 at lower-left in manufacturing datum).

| Component | Pad 1 Function | X (mm) | Y (mm) | Use Case |
|-----------|----------------|--------|--------|----------|
| U1 | OUT1 (first output) | 14.0950 | 18.8000 | Verify SOIC-8 lower-left pad placement; required for correct pin 1 orientation on rotated 90° component |
| U2 | GND (pin 1) | 34.6375 | 20.0500 | Confirm DBZ pinout: pin 1 GND, pin 2 RESET_N, pin 3 VDD |
| Q1 | Gate (pin 1) | 22.5500 | 23.3625 | P-channel source charge; verify SOT-23 gate connection |
| Q2 | Gate (pin 1) | 36.1375 | 9.0500 | N-channel pump driver; verify gate drive path |
| Q3 | Gate (pin 1) | 23.8625 | 13.9500 | P-channel Q2 gate source; verify same polarity as Q1 |
| D1 | Cathode / band | 40.5000 | 7.8000 | Flyback protection; verify band faces pad 1 (PUMP+) |

---

## Component Placement List (CPL summary)

Full placement coordinates and rotation angles: [`../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/PCBWAY_SMT_CPL.csv`](../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/PCBWAY_SMT_CPL.csv)

**Summary:** 41 placed components on top layer; all centroids and angles frozen from v1.1. Datum origin is board lower-left corner (−25, −20 mm in absolute KiCad coordinates; 0,0 in manufacturing datum).

---

## External modules and hardware dependencies

The board operates in a system with components not soldered to the PCB. These must be specified and verified before use.

### ACS758 Hall-effect current sensor module

From `docs/parts/ORDER_LEDGER.md`:
- **MPN:** ACS758LCB-050B (AliExpress order 2026-08-06)
- **Rating:** ±50 A bidirectional, 5 V supply
- **Sensitivity:** 40 mV/A nominal (model assumes 39.4–41.0 mV/A)
- **Supply:** J2 pin 1 (+5V_LOGIC); return J2 pin 2 (GND)
- **Output:** J2 pin 3 (ACS_OUT) — filtered by R1/C5 (10 ms time constant)
- **Critical note:** The detector threshold (RV1) is adjusted during commissioning to account for actual module sensitivity and the gun's idle/active current window. Sensor disconnect (J2 unplugged) is safe: R18 (100 kΩ pulldown) defines open ACS_OUT as zero current (pump off).

### GROTHEN G528 6 V peristaltic pump

From `docs/parts/ORDER_LEDGER.md`:
- **MPN:** GROTHEN G528 (AliExpress order 2026-08-06, order ref [order ref removed])
- **Specification:** 6 V nominal, 3 × 5 mm tube, 150 ml/min at rated voltage
- **Electrical:** Single DC motor, brushed; requires external suppression at motor terminals (see `customer/MOTOR_HARNESS_SUPPRESSION.md`)
- **Connection:** J3 (PUMP+, PUMP_SW_NEG) via twisted-pair harness with motor-end diode and capacitor
- **Current envelope:** Model and test gates assume <1.10 A steady at 50°C; actual pump current is highly dependent on fluid viscosity, back pressure, and head assembly

### Buck converter (5 V USB output, external)

From `docs/parts/ORDER_LEDGER.md`:
- **MPN:** YxPC DC 6-20V to 5V USB Step-Down Module (AliExpress order 2026-08-06, order ref [order ref removed])
- **Quantity ordered:** 2 units (one in use, one spare)
- **Purpose:** Powers the external ACS758 module and any additional logic rail if main 5 V supply is limited
- **Specification caveat:** The listing provides no defensible current, tolerance, or ripple spec. PCB +5V_LOGIC ceiling is 5.25 V.
- **Upgrade option:** If this buck converter fails or output is unstable, substitute with Pololu S13V30F5 (critical "Buck A" upgrade). External module — no board change needed.

### Circuit breaker (manual reset, system level)

From `docs/parts/ORDER_LEDGER.md`:
- **MPN:** YONGRUN Type B-30A (AliExpress order 2026-08-06, order ref [order ref removed])
- **Purpose:** Upstream protection for entire system; independent of board-level F1 (PTC)
- **Activation:** Manual reset after trip; not automatic rearm

---

## Board dimensions and layer structure

| Parameter | Value | Notes |
|-----------|-------|-------|
| Dimensions | 50.0 × 40.0 × 1.6 mm | FR-4 material |
| Copper layers | 2 (top and bottom) | 1 oz copper weight |
| Solder mask | Green, standard coverage | White legend top side |
| Surface finish | Lead-free HASL | RoHS-compliant |
| **Component side** | Top (F.Cu) | 41 SMT, 15 test points |
| **Back side** | Bottom (B.Cu) | GND pour only; no components |
| Mounting holes | 4 × 3.2 mm NPTH | M3 compatible; 43.0 × 33.0 mm pattern |
| Minimum trace width | 0.25 mm routed (0.20 mm floor) | Pump traces 1.0–1.2 mm for high current |
| Minimum clearance | 0.20 mm (all nets) | Via-to-trace, pad-to-pad, same/different nets |
| Via specification | 56 total; 0.30 mm drill, 0.60 mm diameter | Plated through-holes |

---

## Manufacturing QA and design verification status

All 50 manufacturing QA checks pass (certification as of 2026-10-14, release run). See `verification/manufacturing_qa/manufacturing_qa_results.json` in the PCBWay package for full details.

**Critical checks:**
- **U1 footprint:** Matches TI D0008A exactly (1.27 mm pitch, 5.40 mm row spacing, 1.55 × 0.60 mm pads, 3.85 mm inner gap).
- **DRC:** Zero violations; all traces, vias, pads meet minimum geometry rules.
- **BOM/CPL reconciliation:** 41 parts, 92 paste apertures; R22 and J4 DNP as specified.
- **Gerber/Excellon export:** Nine-file set complete and validated (F.Cu, B.Cu, F.Mask, B.Mask, F.Paste, F.SilkScreen, Edge_Cuts, drill_pth, drill_npth).

**Bench gates pending:** Nine bench-level tests remain (START-002, PWR-000–004, PTC-001, ENV-001, EMI-001) pending physical hardware commissioning. See `docs/07-pcb/bringup-and-acceptance-test.md` for procedure.

---

## Related documentation

- **Fabrication and assembly:** `docs/07-pcb/fabrication-and-assembly.md`
- **Bringup and acceptance test:** `docs/07-pcb/bringup-and-acceptance-test.md`
- **Connector pinout:** `docs/07-pcb/connectors-and-pinout.md`
- **Order ledger:** `docs/parts/ORDER_LEDGER.md`
- **v1.2 PCBWay release package:** `hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/`
