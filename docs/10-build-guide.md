# BubbleLink Build Guide

Complete step-by-step assembly procedure from parts-on-the-bench to festival-ready bubble-gun system. This guide covers incoming inspection, battery assembly, electrical harness construction, PCB and controller setup, fluid system assembly, donor gun integration, LED backpack assembly, and final testing. The entire build requires 25–40 hours of hands-on work over approximately **two weeks** (compression from the original four-week estimate due to the 2026-10-29 hard deadline). **Status as of 2026-10-14:** AliExpress parts on hand; PCBs shipped ETA **Oct 15–18**. Prep work (cell matching, 3D printing, harness prep) can start immediately. PCB assembly begins after board arrival. **Target completion: 2026-10-29** (the target festival 2026-10-30 to 31).

## Quick Reference

**Required tools/consumables per step:**
- Spot welder or nickel-tab soldering rig
- Multimeter (voltage, current, continuity)
- Oscilloscope (recommended for PCB calibration)
- Soldering iron + solder and solder wick
- Wire strippers, crimpers (for ring terminals)
- Hot-water bath or heat gun (for hose warm-stretching)
- Narrow 2.5 mm zip ties
- Electrical tape, electrical shrink tubing
- 3D printer (Creality K2/Bambu A1)

**Build schedule by week:**
- **Week 1 (Oct 14–20; prep before PCB arrival):** Incoming inspection of non-PCB parts, battery cell matching and voltage testing, 3D-printed part production (battery spacers, pump cradle, connector blocks, pinch clamps)
- **Week 2 (Oct 21–27; PCB assembly and integration):** Battery cartridge soldering and testing, electrical harness construction, PCB THT component soldering and bring-up, pump assembly and plumbing, fluid system integration
- **Week 3 (Oct 28–29; testing and final prep):** Donor gun integration and calibration, LED backpack setup, first firing tests, leak test, endurance test, final electrical verification

---

## 1. Incoming Inspection

### Verify all AliExpress parts against ../parts/ORDER_LEDGER.md

**Battery subsystem (critical variants):**
1. **2S 40A BMS** (IC GOGOGO Store, [price])
   - Verify label reads **Li-ion 8.4V 40A**, NOT LiFePO₄ 3.2V
   - If unmarked, check voltage: should output ~8.4 V when fully charged 2S pack connected
   - Common-port design: B− (group 1 −), BM/B1 (group 1 +/ group 2 −), B+ (group 2 +), P− (load −), P+ (load +)

2. **6V GROTHEN G528 pump** (GROTHEN Official Store, [price])
   - Verify motor housing marked **6V** (NOT 12V; artwork on some units misleads)
   - Measure DC resistance of motor coil: should read ~10–15 Ω
   - Included tubing: **3 mm ID × 5 mm OD** (kept as pump connection reference)

3. **2S 4A USB-C boost charger** (SZHJW Technology Store, [price])
   - Verify input USB-C connector and output spade terminals
   - Test with a 5V supply: should output ~8.4 V when connected to 2S BMS P+/P− ports

4. **5V USB buck converters** (YxPC Store, qty 2, [price] each)
   - No datasheet: assume 6–20 V input, 5V adjustable output, ~1–2 A capacity
   - **CRITICAL:** before use, dial pot to exactly **5.0 V** and verify with multimeter
   - **Buck A** powers the controller PCB and pump motor (~5.0–5.1 V; PCB qualified input 4.75–5.25 V)
   - **Buck B** powers the LED backpack's USB input

**Electrical subsystem (critical variants):**
5. **ACS758LCB-050B current sensor** (Great IT Electronic, [price])
   - Verify label/silkscreen shows **050B** (±50A, 40 mV/A), NOT 100B
   - Module connector: should be JST or screw terminals; verify 5V, GND, signal pins
   - Measure output voltage at zero current: should read ~2.5V (typical resting point)

6. **30A manual-reset circuit breaker** (YONGRUN Store, [price])
   - Verify **Type B-30A** rating and 12–48 V DC compliance
   - Confirm terminal studs are **M6** (6 mm diameter) for ring-terminal fit
   - Do NOT apply power until ring terminals are crimped

7. **M6 ring terminals** (SC10-6, solder-filled, match for 12 AWG wire)
   - Verify **10 mm² barrel** (oversized for 12 AWG; solder-fill the barrel and strain-relieve rather than relying on crimp alone)
   - Confirm hole diameter matches M6 studs (6.0–6.5 mm)

**Fluid subsystem (critical variants):**
8. **1L water bladder** (UWWWMM Official Store, [price])
   - Verify **1L** capacity (not 2L unless intended)
   - Confirm included **detachable 101 cm hose** with bite-valve shutoff
   - Test hose end for ID/OD: should accept 4 mm hose-fitting connectors or require a reducer

9. **4mm plastic check valve** (BigBigBear Tech Store, [price])
   - Verify **opening pressure 0.003 MPa** (0.435 psi) from manual
   - Arrow on valve body points toward inlet (pump inlet return); critical for orientation
   - Test by applying gentle air pressure from the inlet side; should barely open under thumb pressure

10. **3.5 × 5.5 mm silicone tubing** (Shop1105214603, [price])
    - Measure actual ID/OD; should match 3.5 × 5.5 mm nominal
    - Inspect for cracks, discoloration, or brittleness

11. **Automotive hose-fitting assortment** (Shop1103411025, [price])
    - Identify **#68401** straight 1/8" unions and **#68409** 5/32" tees in compartment
    - Confirm black nylon material and barb sizes

**Connectors & wiring (critical variants):**
12. **XT60H battery connectors** (Shop911130012, [price])
    - Confirm **XT60H** (upgraded version), NOT standard XT60
    - Count: should have 2 pairs (male + female per pair) minimum; confirm 10 pairs shipped

13. **XT30U gun-channel connectors** (Xing Yiao Store, [price])
    - Verify **XT30U** or **XT30** (NOT MR30)
    - Count pairs; intended qty 10 but "5 pairs plenty" per design note

14. **12 AWG silicone wire** (AuHo DIY Store, [price])
    - Verify gauge and color: **Black and Red, 3 m each** (or 5–10 m total)
    - Tinned copper, stranded; should be flexible

15. **16 AWG silicone wire** (AuHo DIY Store, [price])
    - Verify color and gauge: **Black and Red, 5 m each**
    - For gun-channel harnesses

16. **550 paracord 4 mm, 15 m** (FFlyBG Store, [price])
    - Load-bearing tether for umbilical support; black color

17. **JST-XH 2.54 mm connector kit** (Daevkaema Global Tools, [price])
    - Verify kit includes pre-crimped male/female pairs in multiple pin counts
    - Should have 2-pin, 3-pin, and 4-pin housings

18. **Braided PET sleeving 10 mm, 5 m** (XIDA Electric Store, [price])
    - For strain relief on solder joints

**PCB and controllers (critical components):**
19. **PCBWay BubbleLink CTRL v1.2 board** (2 assembled + 3 bare, v1.2 revision)
    - Verify board revision **v1.2** (footprint correction for U1 from v1.1)
    - Check SMT assembly: U1 (TLV1822QDRQ1), U2 (TLV803E), MOSFETs (Q1/Q3 DMP2065UQ, Q2 AO3400A), diode D1 (B340A), fuse F1 (1812L150)
    - Confirm C9 and R18 are **fitted** (populated), NOT DNP
    - Confirm J4 and R22 are **DNP** (not populated)
    - Through-hole parts (RV1, RV2, LEDs, J1–J3, SW1, C1) user-installed

20. **Nickel-plated steel battery tabs** (AllThingsHome, qty 3 packs = 30 total, [price] each)
    - Verify **2.6 cm length, 0.15 mm thick minimum** by caliper
    - Count: should have 30 total (10 per pack)

21. **Fish-paper insulation gaskets** (IC GOGOGO CHANGELIN, [price])
    - 18650 positive-terminal rings; qty ~10

**Consumables & safety:**
22. **JOYFY 32 oz bubble concentrate** (JOYFY US Store, [price])
    - Verify bottle intact, label clear
    - Mix 1 part concentrate + 9–10 parts water per 1 L fill

23. **Liquid Germall Plus preservative** (Shop1105380267, [price])
    - 100 g bottle; add ~1% to bubble solution for long-term storage

24. **COB LED strip 5V 2 m ice-blue** (KISUFU Lighting, [price]) [OPTIONAL]
    - For Tracer cosplay side panel; NOT part of bubble system

**Mark any missing or incorrect variants in an "Incoming Issues" list; do NOT proceed with assembly until verified.**

---

## 2. Battery Assembly (Days 1–3)

### 2.1 Cell matching and preparation

**Cells:** 10 × Samsung INR18650-25R (already owned; 2500 mAh, 3.6 V nominal, 10 A continuous)

1. **Measure each cell's voltage** with multimeter (open-circuit, no load):
   - Record all ten readings; should be within ±0.05 V of each other
   - If spread >0.1 V, charge all cells to 4.2 V via a hobby LiPo charger before proceeding
   - Goal: matched cells ensure balanced 2S5P operation and minimize BMS balancing current demand

2. **Test cell integrity:**
   - Inspect wrapper for tears, burns, or swelling; reject any compromised cells
   - Measure DC resistance (ESR) by discharging 1 A through the cell for ~10 ms and measuring voltage drop; should be <100 mΩ (high ESR indicates wear)

3. **Arrange cells in 2S5P configuration:**
   - Two rows of five cells each (2 series × 5 parallel)
   - Row 1: cells 1–5 (all at same voltage before welding)
   - Row 2: cells 6–10 (all at same voltage before welding)
   - Label rows with tape to avoid mixing during welding

### 2.2 Spot-weld battery tabs

**Setup:**
- Printed cell spacers (5×2 offset layout, 0.5–1 mm air gap between wrappers)
- One spacer at each end of the cartridge
- Nickel-plated steel tabs (qty 30 total)
  - Five independent series links connecting the two rows (positive of row 1 to negative of row 2)
  - Four links joining cells 1–5 in parallel (row 1)
  - Four links joining cells 6–10 in parallel (row 2)
  - Spares for rework

**Weld sequence (5 distributive series links, 4 per row parallel):**

1. **Row 1 parallel bus:** Weld four 2.6 cm tabs connecting the five positive terminals of cells 1–5 in a staggered pattern (avoid single point-of-failure bottleneck)
   - Link 1: cells 1 + to 2 +
   - Link 2: cells 2 + to 3 +
   - Link 3: cells 4 + to 5 +
   - Link 4: doubler or stagger to distribute current

2. **Row 2 parallel bus:** Weld four tabs connecting the five positive terminals of cells 6–10 the same way

3. **Series connections (two rows):** Weld five separate single-cell-to-cell links connecting row 1 (+) to row 2 (−) at distributed points:
   - Link A: cell 1 + to cell 6 −
   - Link B: cell 2 + to cell 7 −
   - Link C: cell 3 + to cell 8 −
   - Link D: cell 4 + to cell 9 −
   - Link E: cell 5 + to cell 10 −

4. **Weld current:** ~80–100 A for 10–15 ms per spot (adjust for your welder calibration)

5. **Post-weld inspection:**
   - No visible cracks or discoloration around welds
   - Tab contact resistance <5 mΩ per weld (measure with multimeter @ 10 A test)
   - No cell heating after 1 A load test for 30 seconds

### 2.3 BMS and XT60H connection

**BMS wiring (common-port design):**
- **B−:** Row 1 negative terminal (cell 1 −)
- **BM/B1:** Row 1 positive + Row 2 negative midpoint (junction between series links)
- **B+:** Row 2 positive terminal (cell 10 +)
- **P−:** System load negative (main harness to breaker)
- **P+:** System load positive (main harness from XT60H)

**Solder XT60H to battery terminals:**
1. Solder **XT60H female (recessed, safer on live pack)** to BMS P+/P− output:
   - Red wire to P+ (row 2 +)
   - Black wire to P− (row 1 −)
   - Insulate solder joints with heat-shrink or electrical tape
   - **CRITICAL:** verify polarity with multimeter before connecting ANY load

2. Insulate the battery terminals:
   - Wrap Row 1 − and Row 2 + with fish-paper rings or electrical tape to prevent short circuits
   - Cover all nickel tabs with electrical tape (except the connections to BMS terminals)

### 2.4 Label the battery cartridge

**Use permanent Sharpie to label the rigid enclosure:**
- "2S5P Samsung 25R"
- "7.2 V nominal, 12.5 Ah, 90 Wh"
- "Build date: [DATE]"
- "XT60 polarity: Red = +, Black = −"
- Diagrams of cell orientation if enclosure is clear/translucent

---

## 3. Electrical Harness Assembly (Days 3–5)

### 3.1 Main distribution harness (12 AWG)

**Components:**
- 30A manual-reset circuit breaker with M6 studs
- 2× M6 ring terminals, 12 AWG size
- 12 AWG red and black silicone wire (~1–2 m total)
- Electrical tape, heat-shrink tubing

**Assembly:**

1. **Ring terminals for breaker studs:**
   - Strip ~5 mm of insulation from each 12 AWG lead
   - Crimp ring terminal onto stripped wire (or solder inside barrel after crimping for extra strength)
   - Verify hole diameter matches M6 studs (should be 6.2–6.5 mm)

2. **Connect to breaker:**
   - Red wire (+): crimp and bolt to one M6 stud with stainless nut (torque: hand-tight + 1/8 turn)
   - Black wire (−): crimp and bolt to opposite M6 stud the same way
   - **CRITICAL:** do NOT solder directly to breaker studs; thermal stress damages internal contacts

3. **Main harness cable:**
   - From breaker output studs, run **12 AWG red and black** to the distribution point (inside pack)
   - Keep pairs twisted to minimize noise induction
   - Total length: ~1 m (adjust for pack layout)

### 3.2 XT30U gun-channel splits (16 AWG)

**Setup:** Two independent channels (guns can be powered separately or together)

1. **Channel 1 (left gun):**
   - Strip 12 AWG red from main harness and solder to one XT30U male connector (positive pin)
   - 16 AWG red wire (~2 m) to gun 1 input
   - XT30U female (recessed) on gun 1 side

2. **Channel 2 (right gun):**
   - Strip 12 AWG red from main harness (or split before main entry) and solder to second XT30U male
   - 16 AWG red wire (~2 m) to gun 2 input
   - XT30U female (recessed) on gun 2 side

3. **Return paths (GND):**
   - 12 AWG black from breaker to ACS758 high-current terminal (both guns in parallel on return)
   - 16 AWG black from ACS758 return to each gun 1 and gun 2 return terminals

4. **Strain relief:**
   - Braided PET sleeving over all soldered joints
   - Heat-shrink tubing over each XT30U connector neck
   - No sharp kinks in the hose or cable bundles

### 3.3 ACS758 external mounting

**Current sensor module placement (beside PCB in enclosure):**

1. Mount ACS758 module on its own standoff or bracket (not on PCB; high-current terminals kept clear)
2. **High-current path:**
   - Breaker positive → ACS758 positive terminal (screw or connector)
   - ACS758 negative terminal → split to XT30U Channel 1 and Channel 2 males
   - Ensure connections are rated for 30+ A (proper wire gauges, terminals, not PCB traces)

3. **Signal connection to PCB (J2):**
   - 3-wire JST-XH or twisted pair: 5V, GND, signal (ACS_OUT)
   - Route away from pump current paths to minimize noise coupling

---

## 4. Power Supply Regulation (Buck Converters)

### 4.1 Pump regulation (5V for motor)

**YxPC USB buck converter (Buck A):**

1. **Input:** 2S battery voltage (unregulated, ~6.0–8.4 V)
2. **Output:** **Dial to exactly 5.0 V** before connecting pump
   - Use multimeter on 5.00 V setting to verify
   - This is CRITICAL; pump rated 4–6 V, and 8.4 V unregulated will overstress it

3. **Load:** GROTHEN G528 pump at 5V draws ~250–300 mA
   - Verify buck can supply 1+ A continuous

4. **Connections:**
   - Buck input: battery 2S pack (via breaker)
   - Buck output: to pump inlet via flyback-protected circuit (see Pump driver section)

### 4.2 LED backpack regulation (5V for display, Buck B)

**YxPC USB buck converter (Buck B):**

1. **Input:** 2S battery voltage
2. **Output:** **Dial to exactly 5.0 V**
3. **Load:** LED backpack USB input (variable, ~100–500 mA depending on display mode)

---

## 5. PCB Assembly and Bring-Up (Days 3–7)

### 5.1 Through-hole component installation (on v1.2 SMT-pre-assembled boards)

**User-installed components (PCBWay shipped SMT side complete; THT user responsibility):**

| Ref | Component | Value | Package | Notes |
|---|---|---|---|---|
| J1 | JST-XH connector | 2-pin (JST B2B-XH-A) | THT | Power input (5V, GND); verify polarity mark |
| J2 | JST-XH connector | 3-pin (JST B3B-XH-A) | THT | ACS758 input (GND, Vcc, signal); verify polarity |
| J3 | JST-XH connector | 2-pin (JST B2B-XH-A) | THT | Pump output (PUMP+, PUMP_SW_NEG); verify polarity |
| J4 | AUTO/FORCE-ON input | 2-pin, 2.50 mm | DNP | Leave empty unless a head can't be detected; see [connectors](07-pcb/connectors-and-pinout.md) |
| RV1 | 3296W-1-202LF | 2 kΩ 25-turn | THT | Gun-detection threshold trimmer; Bourns 3296W lead order 1–3–2 |
| RV2 | 3296W-1-104LF | 100 kΩ 25-turn | THT | Pump-delay trimmer; Bourns 3296W lead order 1–3–2 |
| SW1 | Omron B3F-1000 | Momentary | THT | PRIME button (6×6 mm tactile switch) |
| LED1 | 3–5 mm green (Kingbright L-934GD) | LED | THT | POWER indicator (always on when J1 powered) |
| LED2 | 3–5 mm yellow (Kingbright L-934YD) | LED | THT | GUN indicator (on when current detected) |
| LED3 | 3–5 mm red (Kingbright L-934ID) | LED | THT | PUMP indicator (on when pump active) |
| C1 | Rubycon 16ZLH100MEFC5X11 | 100 µF 16 V | THT | Input bypass on J1; user-installed |
| R22 | — | — | THT | Do NOT populate (future use) |

**Installation order:**

1. **Connectors (J1–J3):** Solder JST-XH 2-pin (B2B-XH-A) and 3-pin (B3B-XH-A) headers; confirm polarity marks face outward
2. **Trimmers (RV1, RV2):** Solder 10-turn potentiometers; leads are 1–3–2 (NOT 1–2–3)
3. **LEDs:** Install with cathodes toward GND; verify colors (red, green, yellow)
4. **PRIME switch (SW1):** Solder tactile switch; confirm closure resistance <10 Ω
5. **Capacitor C1:** 100 µF 16 V electrolytic on J1 input bypass (positive lead to square pad, + mark)
6. **Verify no missing or backward components before power-up**

### 5.2 Power-up and logic-only bring-up

**Setup:** 5V bench supply at 100 mA limit, no J2 or J3 connected yet

1. **Inspect before power:**
   - Check J1 pin 1 to GND for shorts (should read >1 MΩ)
   - Verify J3 pin 2 NOT shorted to GND unpowered
   - Confirm no solder bridges between pads

2. **Apply 5V, measure acceptance criteria (from ../07-pcb/bringup-and-acceptance-test.md § 2. Logic-only bring-up):**

| Test Point | Expected | Measurement |
|---|---|---|
| TP1 +5V_PUMP | 4.95–5.05 V | ___ |
| TP2 +5V_LOGIC | Within 50 mV of TP1 | ___ |
| TP8 VMID | 2.40–2.60 V (after settling ~1 s) | ___ |
| TP10 VDELAY | 0.98–1.06 V | ___ |
| TP9 HOLD idle | <0.10 V | ___ |
| TP14 TIMER_N idle | >4.5 V | ___ |
| TP11 PUMP_GATE idle | <0.05 V | ___ |
| LED1 (POWER) | ON | ___ |
| LED2 (GUN) | OFF | ___ |
| LED3 (PUMP) | OFF | ___ |

3. **STOP immediately if TP11 PUMP_GATE is HIGH at idle** (indicates Q2/gate-drive failure)

4. **Current consumption:** Record steady-state current at J1; should be <20 mA with no sensor/pump connected

### 5.3 Controlled startup and brownout gate

**Use oscilloscope to monitor TP2, U2 RESET_N, TP9, TP14, TP11:**

1. **Hard connect/disconnect 5V** ten times, observe:
   - TP11 PUMP_GATE remains <0.65 V during brownout
   - After RESET_N asserts, TP11 falls below 0.20 V within 15 ms

2. **Ramp supply voltage** 0→5V and 5→0V at rates: 0.1, 1, 10, 100 V/s
   - No pump-gate pulses above 0.65 V during invalid supply

3. **Supply dips** through 4.2–4.6 V range with 1 ms, 10 ms, 100 ms, and 1 s dwell times:
   - Pump gate must release within 15 ms of RESET_N assertion

4. **Record worst-case waveform** for field reference

### 5.4 Simulated sensor calibration

**Use function generator or 0–5V source with 1 kΩ series resistor on J2 pin 3 (ACS_OUT):**

1. **Verify RV1 threshold range:**
   - Measure TP6 (RV1 wiper) voltage; should span ~2.20–2.80 V as RV1 is rotated
   - Clockwise = higher threshold; counter-clockwise = lower threshold

2. **Detection assertion:**
   - Slowly increase J2 pin 3 voltage from 0 to 3.5 V (simulating gun current)
   - Record TP5 (filtered) and TP6 (threshold) voltages when DET_N asserts (GUN LED on)
   - Hysteresis should be only a few millivolts

3. **Detection release:**
   - Slowly decrease J2 pin 3; record release point
   - Expect minimal hysteresis (~4 mV nominal)

4. **Fast step response:**
   - Step J2 pin 3 from 0 to 20 mV above threshold
   - Confirm DET_N assertion and Q2 gate (TP11) rise within 25 ms
   - GUN LED should light instantly

5. **Pump delay tuning:**
   - With J2 held at ~3V (simulated gun active), set RV2 and release J2
   - Measure time from J2 release until TP11 (PUMP_GATE) falls below 0.20 V
   - Record RV2 dial position for **target 350 ms delay**
   - Verify clockwise increases delay; range should span 35–575 ms

6. **PRIME button:**
   - Press SW1; confirm GUN LED and TP11 (PUMP_GATE) go high immediately
   - Release SW1; confirm timed shutdown per RV2 setting

7. **Sensor disconnect:**
   - Unplug J2 (simulate unplugged ACS758 module)
   - Pump must release after max delay; R18 pull-down ensures safe OFF state

### 5.5 Dummy-load output test (simulated pump)

**Use 5V, 100–300 mA resistive load (e.g., 20–50 Ω power resistor) at J3:**

1. **Verify J3 polarity** before connection (red/positive pin orientation)
2. **Trigger pump control:**
   - Use PRIME switch or simulated ACS input on J2
   - Confirm TP12 (PUMP_SW_NEG) falls close to GND when pump is "on"
   - Confirm TP11 (PUMP_GATE) remains near logic rail (~3.5 V) when on
3. **Verify signal integrity:**
   - No material noise on TP2 (power rail), TP5 (sensor), TP6 (threshold) as pump load switches
   - Indicates proper filtering and ground distribution

---

## 6. Fluid System Assembly (Days 5–8)

### 6.1 Prepare 1L water bladder

1. **Inspect bladder** for leaks (fill with water, squeeze gently, check for weeps around seams)
2. **Measure outlet hose ID/OD:**
   - Typical: 6 mm ID × 8 mm OD or 4 mm ID × 6 mm OD
   - Determine reducer size needed (e.g., 6→4 mm reducer if hose is larger than 3.5 mm ID)

3. **Install reducer:**
   - From automotive hose assortment, select appropriate barbed union (e.g., 1/4" or 3/8" to 1/8")
   - Warm 3.5 × 5.5 mm silicone tube in hot water (~60°C) to soften
   - Push tubing over reducer barb until fully seated (~10 mm deep)
   - Secure with narrow 2.5 mm zip tie; do NOT overtighten

4. **Hydration bladder setup inside pack:**
   - Place bladder in rear compartment of LED backpack or hydration pack
   - Cut factory hose to ~30 cm length (retain inside pack; loop back to pump inlet)
   - Factory hose feeds to reducer → 3.5 mm silicone tube → pump inlet tee

### 6.2 Assemble pump manifold

**Components:**
- GROTHEN G528 pump (6V at ~5V regulated supply)
- 1L bladder (pre-configured above)
- 3.5 × 5.5 mm silicone tubing, 5 m spool
- 4 mm plastic check valve (opening pressure 0.003 MPa)
- Automotive hose-fitting assortment (tees, unions, reducers)
- Printed pinch clamp (recirculation restrictor, or fixed-tube bypass)
- Pump inlet filter (optional; typically not needed for clean solution)

**Plumbing path (functional diagram):**

```
Bladder (1 L)
    ↓
Factory hose (cut short, ~30 cm)
    ↓
Reducer (e.g., 6→4 mm barb)
    ↓
3.5 × 5.5 mm silicone inlet line
    ↓
INLET TEE (3-way tee fitting)
    ├─ Pump inlet (top of tee)
    │   GROTHEN G528
    │   (6V, 250–300 mA at 5V)
    ├─ Bypass return (from printed pinch clamp via check valve)
    │   Loop back from pump outlet
    │
Pump outlet
    ↓
OUTLET SPLITTER TEE (2 to 3 branch tee)
    ├─ Left gun channel → LEFT PINCH CLAMP (shutoff) → 4-foot hose → Gun 1 inlet
    ├─ Right gun channel → RIGHT PINCH CLAMP (shutoff) → 4-foot hose → Gun 2 inlet
    └─ Bypass return → Printed restrictor → Check valve → Pump inlet tee
```

**Assembly steps:**

1. **Mount pump inside pack** on printed cradle (small foam pad underneath to isolate vibration)

2. **Pump inlet tubing:**
   - Cut 3.5 mm silicone hose to ~1 m from bladder reducer to pump inlet
   - Barb at inlet tee (1/8" or 5/32" diameter from assortment)
   - Secure inlet with 2.5 mm zip tie (do NOT overtighten into soft silicone)

3. **Pump outlet splitter:**
   - Install 1/8" or 5/32" 2-to-3 tee at pump outlet
   - Three branches: left-gun channel, right-gun channel, bypass return
   - Pump outlet tubing: cut ~30 cm section to tee

4. **Gun outlet channels (2× four-foot hoses):**
   - Left channel: pump outlet tee → left pinch clamp → 4-foot 3.5 mm hose → left gun barb
   - Right channel: pump outlet tee → right pinch clamp → 4-foot 3.5 mm hose → right gun barb
   - Each hose secured at pack exit with zip tie; outer hose sheathed in braided PET sleeving for durability

5. **Bypass/recirculation loop:**
   - Pump outlet tee → printed pinch clamp restrictor → 4 mm check valve → pump inlet tee
   - Allows pump to "unload" when guns are closed, reducing cavitation and noise
   - Restrictor tuned to ~5–10 mL/min bypass flow during normal operation (calibrate by observation)

6. **Check valve orientation (CRITICAL):**
   - Arrow on valve body must point toward pump inlet (reservoir return side)
   - Prevents siphoning from guns back into reservoir when pump stops

7. **Pressure test (bench, no guns):**
   - Fill bladder with water (not solution yet, to avoid mess)
   - Prime pump via PRIME button for 5 seconds
   - Verify no leaks at barbs, tees, or unions (all hoses secured with narrow zip ties)
   - Apply gentle air pressure to outlet hose (pinch clamp open); check valve should barely crack open

---

## 7. Donor Gun Teardown and Rewiring (Days 6–8)

### 7.1 Identify and prepare donor guns

**Recommended:** Four-AA 10-hole rocket-style gun (Joey's design note)
- Compact mechanical head
- 10 apertures, high bubble count
- 4.5V nominal (AA batteries × 4), or 6V variant if available
- Overvoltage tolerance: 40% at 8.4V (6V nominal)

**Verification steps:**

1. **Open donor gun carefully** (pry apart plastic halves without breaking clips)
2. **Identify motor inlet tubing:**
   - Trace pump inlet to locate tubing ID (typically 3–4 mm ID)
   - If <3.5 mm, a 4→3 mm reducer may be needed from assortment
   - Measure actual ID with digital caliper

3. **Disconnect factory motor wiring** (typically two solder tabs or push connectors)
   - Do NOT damage the internal brushes or commutator
   - Take a photo for reference during reassembly

4. **Check check valve inside gun** (if present):
   - Some guns have internal one-way valves on pump inlet; confirm direction (arrow toward motor chamber)
   - If present, do NOT replace; leave in place

### 7.2 Umbilical harness assembly

**One umbilical per gun (two total for dual-channel system):**

**Components per umbilical:**
- 16 AWG red and black silicone wire, 4–5 meters (accounts for 4-foot gun hose bundling)
- XT30U male connector (power inlet, gun-side)
- 3.5 mm silicone tubing, 4 feet (fluid inlet)
- Printed connector block (pack end) with XT30U female socket and fluid barb
- Printed connector block (gun end) with XT30U male receptacle and fluid inlet barb
- 550 paracord 4 mm, ~2 meters (load-bearing tether)
- Heat-shrink and braided PET sleeving (strain relief)

**Harness construction:**

1. **Electrical leads (16 AWG):**
   - Bundle red and black wires together (twist lightly)
   - Length: 4–5 m to account for gun hose routing and pack entry
   - Soldered to XT30U male connector pins (+ red, − black)
   - Insulate solder joints with heat-shrink

2. **Fluid line (3.5 mm tubing):**
   - 4-foot length from pack-side connector block to gun-side inlet barb
   - Bundle alongside power leads with zip ties at ~1 m intervals
   - Do NOT kink or bind tightly (allows liquid flow)

3. **Load-bearing paracord:**
   - 2 m length, 4 mm 550 paracord in black
   - Bundles power and fluid together as primary support member
   - Attached to printed strain-relief boots at pack and gun ends
   - Carries mechanical load; electrical leads and fluid line are passengers

4. **Connector blocks (printed):**
   - Pack-end: XT30U female socket (recessed), 1/8" or 5/32" barb for 3.5 mm hose, paracord anchor
   - Gun-end: XT30U male receptacle, barbed inlet for motor pump, paracord anchor
   - Assembled with M3 screws or snap clips (design per CAD)

5. **Strain relief (printed TPU boots):**
   - At pack entry: curved boot transitions paracord load to bag stitching and structure
   - At gun end: boot anchors paracord to gun body, isolates tubing/wires from pinch stress

### 7.3 Gun motor rewiring

1. **Solder 16 AWG leads** from umbilical XT30U male connector:
   - Red wire to motor positive terminal (usually marked or color-coded)
   - Black wire to motor negative terminal
   - Use electrical tape or heat-shrink to insulate solder joints

2. **Pump tubing connection:**
   - Warm 3.5 mm tubing in hot water
   - Push over motor inlet barb until fully seated
   - Secure with 2.5 mm zip tie (or barb clip if included)

3. **Reassemble gun body:**
   - Reinsert rewired motor assembly
   - Check that tubing inlet is accessible and not pinched
   - Close plastic halves; verify trigger mechanism moves freely

4. **Test (bench, no solution):**
   - Connect umbilical to 5–6V bench supply
   - Trigger gun; motor should spin smoothly
   - Disconnect immediately if motor stalls (indicates blocked inlet or incorrect wiring)

---

## 8. LED Backpack Integration (Days 7–9)

### 8.1 Measure LED backpack interior

**Goal:** Determine if battery, pump, controller, and fluid fit inside the M-Style LED pixel backpack

1. **Empty the backpack** (remove factory bladder and internal pads)
2. **Measure internal dimensions:**
   - Length (back pocket depth): typically 34–36 cm
   - Width: typically 20–22 cm
   - Depth (front to back): typically 6.5–7.5 cm
   - Usable volume after LED panel/controller removed: ~2.5–3.5 L (vs. advertised 5 L nominal)

3. **Mock up with cardboard:** Cut cardboard templates for:
   - Battery cartridge: ~105 × 75 × 43 mm
   - Pump cradle: ~65 × 55 × 50 mm
   - Controller/charger/breaker tray: ~140 × 80 × 25–35 mm
   - Fluid reservoir: 1 L + ~20% bladder material volume

4. **Fit test:** Place templates inside backpack; confirm no binding or excessive gaps

### 8.2 Internal organization

1. **Rear compartment (water-proof divider optional):**
   - Battery cartridge (bottom, closest to back)
   - 1L fluid reservoir (bladder in protective mesh bag)
   - Pump on foam cradle (damping vibration)

2. **Front compartment:**
   - Controller PCB on small tray (~100 × 60 mm)
   - USB-C charger (cable routed externally to shoulder strap opening)
   - 30A breaker and 5V buck converters on same tray
   - XT60H battery connector (accessible for field swap)
   - JST-XH sensor and pump connectors (accessible for testing)

3. **Cable management:**
   - All harnesses and umbilicals routed through side exit points (shoulder strap channels)
   - No pressure on fluid bladder or PCB
   - Zip ties at strategic points to prevent movement during dance/shake

4. **Weight distribution:**
   - Battery (~500 g) centered
   - Pump (~70 g) on pad to isolate vibration
   - Electronics tray balanced on front
   - Total loaded weight ~3.1–3.5 kg (within performance envelope for festival wear)

### 8.3 Electrical integration inside backpack

1. **5V power distribution:**
   - **Buck A** (YxPC, set to 5.0V): input from 2S battery (through breaker), output supplies PCB J1, ACS758 module power, and pump motor control via Q2 on the PCB
   - **Buck B** (YxPC, set to 5.0V): input from 2S battery, output to LED backpack USB input

2. **Connector routing:**
   - J1 (PCB power): short JST-XH cable from Buck A output
   - J2 (ACS758 sensor): 3-wire JST-XH from external ACS758 module (receives 5V and GND from PCB J1)
   - J3 (pump output): short cable to pump motor (2-pin JST-XH, controlled by PCB MOSFET Q2)
   - LED backpack USB: 5V from Buck B output

3. **Test before final packing:**
   - Apply 5V to system; verify all test points nominal per PCB bring-up section
   - Confirm no shorts when fully integrated
   - Verify connectors are accessible for field calibration (RV1, RV2 must be visible/reachable)

---

## 9. First Integrated Firing Test (Days 10–11)

### 9.1 Pre-fire checklist

- [ ] Battery charged to 8.4 V (use USB-C charger for ~8 hours from empty)
- [ ] BMS balancing complete (voltage <0.1 V spread across cells)
- [ ] All solder joints cold and solid (no joint movement with probe)
- [ ] Pump inlet and outlet NOT kinked or occluded
- [ ] XT30U connectors fully seated and latched
- [ ] Breaker reset lever DOWN (armed)
- [ ] PRIME button accessible for priming
- [ ] Donor guns verified for motor movement and tubing inlet patency
- [ ] Fluid solution mixed (1 part JOYFY concentrate + 9 parts water in 1L container)

### 9.2 Prime pump (bench, no guns)

1. **Fill 1L bladder** with mixed solution (10 mL concentrate + 90 mL water for test)
2. **Connect battery to XT60H** connector (red wire to +, black to −)
   - Voltmeter reading should jump to ~8.4 V (battery full)
   - LEDs should light (POWER on, others off if no sensor/pump connected)

3. **Connect J2 (ACS758 sensor)** to PCB
   - POWER LED should remain on
   - GUN and PUMP LEDs off (no current detected)

4. **Connect J1 (5V supply)** to PCB
   - All three LEDs on briefly during startup, then POWER remains on

5. **Connect pump to J3:**
   - PRIME switch activation → PUMP LED on
   - Pump motor audible; fluid flows from pump outlet into tee
   - Hold PRIME for 10 seconds (primes all lines with solution)
   - Release PRIME → PUMP LED off after ~350 ms delay

6. **Verify output:**
   - Fluid should flow from pump outlet tee into left and right gun channels
   - No leaks at barbs, tees, or unions (all connections secured with narrow zip ties)

### 9.3 Gun firing (first test, single gun)

1. **Connect Left Gun** (Umbilical 1) XT30U to Left Channel XT30U female:
   - Confirm snug fit and latch clicks
   - Motor should spin freely (dry run, no solution in tubing yet)

2. **Trigger gun with PRIME:**
   - PUMP LED lights; solution flows into gun inlet
   - Release gun; pump stops after ~350 ms delay (solution in gun nozzle)
   - Repeat 3–4 times to verify consistent behavior

3. **Connect Right Gun** (Umbilical 2) to Right Channel:
   - Repeat PRIME trigger test
   - Verify pump activation works independently per gun

4. **Dual-gun firing:**
   - Connect both XT30U umbilicals to pack channels
   - Trigger Left gun → GUN LED on, PUMP LED on, solution flows left
   - Trigger Right gun (while Left held) → solution flows right; pump remains on (supplying both)
   - Release both guns → PUMP stays on for 350 ms delay, then off
   - Repeat 5–10 times; verify no chatter or false starts on either gun

5. **ACS758 threshold tuning** (if gun current varies):
   - Measure combined gun current at 5V (multimeter in series on gun return)
   - Adjust RV1 (gun detection threshold) so trigger is reliable but no false positives during idle
   - Typical threshold: ~0.5 A (adjust per actual gun current)

---

## 10. Leak Test (Days 11–12)

### 10.1 Pressurized soap bubble test

1. **Fill bladder** with 1L of water + soap (1 mL dish soap per liter for visibility)
2. **Apply gentle air pressure** to pump outlet line via hand pump or low-pressure air compressor (~0.5 psi):
   - Observe all joints, barbs, tees, and check valve
   - Listen for hissing; watch for bubbles
   - Verify zip ties are not cutting into the silicone hose
3. **Mark any leaks** with tape; note location and severity
4. **Common leak points:**
   - Zip ties overtightened (cutting into soft silicone): loosen and reposition, or replace hose section
   - Check valve cracking too easily: reduce air pressure or confirm arrow orientation
   - Barb mismatch: replace with correct size or add reducer

### 10.2 Dynamic leak test (during pump operation)

1. **Prime pump for 30 seconds** with guns closed (pinch clamps fully shut)
   - Observe bypass restrictor and check valve (should hear quiet gurgle if flow is ~5–10 mL/min)
   - Watch for weeps at all connections

2. **Open one pinch clamp** and trigger PRIME for 10 seconds:
   - Solution flows to that gun; no leaks at barb connections (zip ties tight but not crushing silicone)

3. **Repeat with both guns open**:
   - Pump supplies both channels simultaneously
   - No dripping or weeping anywhere

---

## 11. Shake and Dance Test (Days 12–13)

**Goal:** Verify mechanical security and connector integrity during movement

1. **Physical shake test (30 seconds):**
   - Hold backpack at chest level and shake vigorously (simulating dance)
   - No loose components rattling
   - No zip ties slipping or coming loose
   - No connector wiggle or disconnection

2. **Dance simulation:**
   - Wear backpack and move for 2–3 minutes (jumping, turning, arm swinging)
   - Monitor for vibration/noise from internal components
   - Verify no battery tab fractures visible through enclosure window (if clear)
   - No cable strain at pack exit points

3. **Hose head-height test (if applicable):**
   - Raise gun intake barb 5 feet above reservoir surface
   - Prime pump; solution should flow upward without cavitation
   - If flow stops, check for air locks in hose or inadequate pump pressure

---

## 12. One-Liter Endurance Test (Day 13)

**Goal:** Measure actual battery runtime and power consumption

1. **Charge battery to 8.4 V** via USB-C charger
2. **Fill 1L bladder** with mixed bubble solution
3. **Connect guns and start firing continuously:**
   - Both gun channels open (pinch clamps fully open)
   - Continuous trigger (PRIME held or gun triggers held)
   - Measure time until solution depleted (bladder empty, no more bubbles)

4. **Record:**
   - Start time and start battery voltage (should be ~8.4 V)
   - End time and end battery voltage (should be ~6.0 V, BMS cutoff threshold)
   - Total runtime in minutes
   - Solution consumption (should be approximately 100 mL/min for dual-gun operation, yielding ~10 minute runtime for 1L)

5. **Thermal monitoring:**
   - Check battery cartridge temperature after endurance test
   - Should be warm but NOT hot to touch (aim <50°C)
   - Check PCB temperature at U1 and Q2 (should be <60°C)
   - Pump and motor temperature rise acceptable if <20°C above ambient

---

## 13. Electrical System Verification (Day 14)

### 13.1 Battery voltage and protection

- [ ] Open-circuit voltage: 8.4 V (fully charged)
- [ ] Nominal voltage under 5A load: 7.4 V (acceptable)
- [ ] BMS cutoff threshold triggered: 6.0 V (gun current should stop flowing)
- [ ] BMS balance current: <10 mA at 8.4 V rest (low balancing demand)

### 13.2 Charger integration

- [ ] USB-C charger accepts 5V/3A input
- [ ] Battery charges from 6.0 V (depleted) to 8.4 V in <10 hours
- [ ] Voltmeter reads 8.4 V when charger is done
- [ ] No overheating of charger or battery during charging

### 13.3 Controller stability

- [ ] PCB logic remains stable over 10+ pump cycles
- [ ] RV1 and RV2 calibration stable (no drift after 100 cycles)
- [ ] LEDs bright and responsive
- [ ] No false pump starts or dropouts during operation

---

## 14. Pre-Event Checklist (Day 14–15, before 2026-10-29 deadline)

**Final systems review before festival deployment:**

- [ ] Battery charged to 8.4 V and rested >30 minutes (voltage stable)
- [ ] All connectors (XT60H, XT30U, JST-XH, J1–J3) securely latched
- [ ] Fluid solution mixed and bladder filled (1 part concentrate to 9 parts water)
- [ ] Pump primed (no air locks in tubing)
- [ ] Both guns tested for motor spin and inlet patency
- [ ] PCB calibrated (RV1 = detection threshold, RV2 = ~350 ms delay)
- [ ] Voltmeter visible and readable on front of backpack
- [ ] LED backpack powered and responsive (if used)
- [ ] Backpack weight balanced and comfortable (tested for 5+ minutes wear)
- [ ] Umbilical connectors accessible for quick gun swap in field
- [ ] Spare bubble solution concentrate on hand (1× 32 oz bottle supports ~10 refills)
- [ ] Spare fuses/breaker reset mechanism tested
- [ ] Conformal coating applied (optional; skip if field repair access needed)
- [ ] Documentation (this build guide, test results, calibration notes) stored digitally or on paper

---

## Final Assembly Statistics

- **Total build time:** 25–40 hours hands-on
- **Critical path:** PCB bring-up (6+ hours) + fluid system assembly (4+ hours) + donor gun integration (3+ hours)
- **Estimated completion:** 2026-10-20 to 2026-10-25 (allowing 4–9 days for final testing and calibration before 2026-10-29 deadline)
- **Loaded weight:** 3.1–3.5 kg (with 1L fluid, festival configuration)
- **Runtime:** 8–12 minutes continuous firing (1L solution at dual-gun operation)
- **Estimated bubble output:** 500–1000 bubbles/minute per gun (subject to head design and solution quality)
