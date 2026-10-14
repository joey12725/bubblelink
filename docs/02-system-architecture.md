# System Architecture

BubbleLink is a modular bubble-gun system for festivals and raves, built around a 2S5P 18650 lithium-ion battery, a single transfer pump controlled by gun-current detection, dual XT30U gun channels, and a one-liter bubble-solution reservoir. This document describes the complete system architecture, power distribution, fluid paths, control logic, and mechanical layout.

## Table of Contents

1. [Overview](#overview)
2. [Power System](#power-system)
3. [Fluid System](#fluid-system)
4. [Control System](#control-system)
5. [Electrical Architecture](#electrical-architecture)
6. [Umbilicals and Connectors](#umbilicals-and-connectors)
7. [Physical Layout](#physical-layout)
8. [Subsystems Reference](#subsystems-reference)

---

## Overview

The BubbleLink system integrates five major subsystems:

- **Battery & Power Distribution:** 2S5P Samsung 25R cells with BMS, 30 A manual breaker, two regulated 5 V rails, and battery voltage display.
- **Fluid Delivery:** 1 L hydration bladder, GROTHEN G528 6 V pump, low-pressure recirculation loop, two gun channels with four-foot hoses.
- **Control Electronics:** BubbleLink CTRL v1.2 PCB (50 × 40 mm), ACS758 external current sensor, three status LEDs, adjustable pump delay.
- **Gun Outputs:** Two XT30U power connectors on independent 16 AWG branches, supporting dual bubble-gun heads simultaneously.
- **Mechanical Integration:** One printed upright "stick" (about 99 × 78 × 207 mm) beside the bladder inside the MAX LED backpack: a control-head cap over a sealed dry tube (battery and electronics on a slide-out sled) over a draining wet cup (pump and fittings). Printed umbilical bricks give strain relief at both ends of each umbilical. See [09-printed-parts.md](09-printed-parts.md).

---

## Power System

### Battery Architecture

**Configuration:** 2S5P (two series × five parallel)
- **Cells:** 10× Samsung INR18650-25R (3.6 V nominal, 2500 mAh each)
- **Nominal voltage:** 7.2 V; **Charged:** 8.4 V (4.2 V per cell)
- **Capacity:** 90 Wh (12.5 Ah)
- **Current rating:** 40 A BMS (peak); continuous operation <1.1 A total system
- **Configuration:** Thin 2S5P slab (5 parallel columns × 2 series rows) with distributed nickel-plated-steel bridges (minimum 0.15 mm thick)
- **Protection:** 2S 40 A Li-ion BMS with balance charging; stands on edge in a slot along the stick's back wall, next to the battery's TERM face
- **Cell holders:** printed MID and TERM, two offset rows of five at 19.9 mm pitch; the two rows face opposite directions
- **Thermal observation:** Cells reach 45–55°C during sustained high-current use; within safe Samsung 25R operating range

### Primary Breaker and Distribution

```
2S5P Battery (7.2–8.4 V)
    │
    ├─ BMS (40 A, 2S, Li-ion)
    │
    └─ XT60H connector (30 A rated, 12 AWG main wire)
           │
           ├─ [30 A manual-reset breaker, waterproof car-rated (Type B)]
           │
           └─ Distribution point (12 AWG copper bus)
                  │
                  ├─ Buck A converter (→ 5 V for pump + PCB logic) [ACS758 supply]
                  │
                  └─ Parallel split to two XT30U channels
                         │
                         ├─ Gun Channel 1 (XT30U, 16 AWG, 15 A max)
                         │
                         └─ Gun Channel 2 (XT30U, 16 AWG, 15 A max)
```

**Breaker Specifications:**
- Type: 12V–48V DC manual-reset, waterproof
- Rating: 30 A (6 mm / M6 threaded studs)
- Form: inline type, studs at both ends; a square plate in the middle carries a red reset lever and a red push-to-trip button
- Size (measured 2026-10-14): 1⅝ in square plate, 4 in (102 mm) long, 1⅝ in thick, plate holes 1¼ in apart (the listing's 72 × 48 × 44 mm was wrong: it's longer but slimmer)
- Mounting: Stands upright behind the sled's cross panel with its controls facing the right wall, 2 mm behind a 34 × 40 mm window covered by a glued TPU membrane, so you can trip or reset it through the wall. It hangs by zip ties through its two plate holes and slots in the spine
- OFF switch: pressing the trip button through the membrane turns off everything downstream (bucks, PCB, voltmeter, guns). The XT60H loop below the stick is the full battery disconnect, for storage; the BMS stays on the battery either way
- Installation: In the + line only. Two M6 ring terminals (12 AWG, tinned copper) soldered to 12 AWG main harness, clamped beneath nuts

### Regulated 5 V Rails

**Buck A (Primary):** Pump supply + PCB logic + ACS758 sensor
- Input: Unregulated 6.4–8.4 V from battery (through 30 A breaker)
- Output: 5.0 V ±0.25 V (qualified 4.75–5.25 V)
- Load: ~0.5 A peak (0.3 A pump + 0.2 A PCB/sensor logic)
- Module: Adjustable step-down converter (set to 5.0 V before deployment)
- Filtering: 100 nF input bypass capacitor

**Buck B (Secondary):** LED backpack USB power (isolated)
- Input: Unregulated 6.4–8.4 V from battery
- Output: 5.0 V for LED display backpack, soldered directly to a cut USB cable (no room for USB plugs inside the stick; Buck A's output is likewise soldered straight to the J1 lead)
- Load: ~0.5 A (LED pixel matrix)
- Module: Separate step-down converter (dedicated, no cross-load coupling)
- Rationale: Isolates LED and pump load transients from PCB logic supply

**Battery Voltage Display:** External 4–100 V digital voltmeter
- Input: 2S battery voltage (7.2–8.4 V nominal), wired after the breaker so tripping the breaker turns it off
- Connector: Two-wire. Idle draw not measured (small LED meters typically draw tens of mA); check it once with a multimeter, and unplug the XT60H loop for storage
- Display: Glued into a 29.2 mm hole in the top of the stick's cap (about 1 in deep or a bit more; the cap allows 30 mm)
- Accuracy: Sufficient for field battery estimation; accounts for voltage sag under load

---

## Fluid System

### Reservoir and Prime Path

```
1 L Hydration Bladder (TPU food-grade, removable)
    │
    ├─ 101 cm factory detachable outlet hose (cut to ~20 cm inside pack)
    │
    └─ [Reducer: bladder hose → 3.5 mm ID]
           │
           └─ 3.5 × 5.5 mm silicone tubing (5 m spool available)
                  │
                  └─ Pump inlet tee (nylon barb, 3.5 mm side)
```

**Reservoir Specifications:**
- Capacity: 1 L (exactly; no oversized bag)
- Material: TPU, food-grade, BPA-free
- Removable: Yes; clean after every event
- Valve: Bite-valve (auto-sealing, leak-proof during transport)
- Prime time: ~7–12 seconds (GROTHEN G528 at 6 V filling four-foot hose)

### Pump and Transfer Circuit

**GROTHEN G528 Peristaltic Pump:**
- Rated voltage: 6 V DC (4–6 V operating range)
- Actual supply: 5.0 V regulated from Buck A (confirmed compatible; flowrate slightly reduced but within design margin)
- Flow rate: ~150 mL/min on water; ~100–120 mL/min with bubble solution at 5–6 V
- Current draw: 0.25–0.30 A nominal at 5 V; <0.60 A preferred, <1.10 A worst-case hot limit
- Pump tubing: 3 × 5 mm BPT (supplied with pump); connects to 3.5 mm barb union via reducer
- Protection: F1 PPTC 1.5 A fuse on pump positive branch (temperature-derated: 1.10 A hold at 50°C)
- Operation: Continuous whenever armed and gun current detected; prime time negligible compared to recirculation settling

### Recirculation Loop (Low-Pressure Bypass)

**Purpose:** Maintains four-foot hoses primed and ready; allows pump to run faster than gun demand without overpressurizing

```
Outlet tee 1 (pump outlet)
    │
    ├─ [1] To outlet tee 2 → gun 1 / gun 2 (primary path)
    │
    └─ [2] Side branch: bypass restrictor (printed slide clamp, adjustable)
           │
           └─ Check valve (0.003 MPa opening pressure; 4 mm barb, plastic PP body)
                  │
                  └─ Pump inlet tee (closes circuit)
```

Three tees in total: the inlet tee and outlet tees 1 and 2. All of them, the check valve and the bypass slide clamp are strapped to the right-hand strip of the stick's wet cup.

**Flow Regulation:**
- Restrictor: Printed slide clamp (the same design as the two channel shutoffs). Slide toward the arrow to close: the first ~8 mm takes the gap from 6.0 mm to 2.4 mm, the next 22 mm is fine adjustment, and it seals at 0.6 mm. The shallow ramp self-locks; no screw. Set during build; wet-test that it holds
- Check valve: 4 mm plastic one-way valve (BigBigBear model); opening pressure 0.003 MPa (≈0.44 psi), low enough for peristaltic operation
- Orientation: Check valve arrow points toward pump inlet/reservoir side (critical for direction)
- Expected bypass flow: 5–15 mL/min at nominal pump output, balancing hydrostatic lift and line friction

### Gun Channel Hoses

**Dual independent channels (symmetrical):**

```
Outlet tee 2
    │
    ├─ Left channel:  3.5 × 5.5 mm silicone hose
    │                 └─ Four-foot length → XT30U connector → paracord umbilical
    │                     └─ Donor gun inlet (4 mm barb, donor-pump inlet side)
    │
    └─ Right channel: 3.5 × 5.5 mm silicone hose
                      └─ Four-foot length → XT30U connector → paracord umbilical
                          └─ Donor gun inlet (4 mm barb, donor-pump inlet side)
```

**Specifications:**
- Hose ID: 3.5 mm; OD: 5.5 mm; food-grade silicone
- Shutoff: one printed slide clamp on each gun line
- Length: Four feet per channel (measured inside pack to gun adapter)
- Fittings: Nylon barbs from automotive hose assortment (#68409, 5/32-inch ≈4 mm tees; #68401 straight unions for reducers)
- Pressure rating: Low (<1 psi during normal operation; dynamic hose suitable)
- Fastening: Narrow (2.5 mm) zip ties at manifold, pump outlet, and bladder reducer only; avoid over-clamping soft silicone
- Hose volume: Four-foot 3.5 mm-ID hose holds ~25 mL (priming time ~2–3 seconds at pump flow)

---

## Control System

### Current Sensing and Detection

**ACS758LCB-050B Hall-Effect Module (External):**
- Type: 50 A bidirectional; 40 mV/A sensitivity; 5 V supply
- Connection: Three-wire JST-XH (GND, +5V, analog OUTPUT)
- Zero-current output: ~2.5 V nominal
- Operating range: 0–5 V output (0–50 A primary measurement range)
- Accuracy: ±4 mV over temperature; noise floor ~±10 mV
- Location: Compartment on the front of the sled's cross panel, above Buck A, held with a zip tie (mounting holes not used); signal wire routed separately to J2 connector
- Purpose: Detects combined current from both XT30U gun channels; triggers pump-on when threshold exceeded

**Current Sensing Path:**
- Measured signal: Combined gun current (both XT30U channels in parallel upstream of ACS758)
- Signal does NOT include pump current or LED backpack current (isolated upstream of sensor)
- Filtering: R1/C5 (10 ms RC low-pass) removes PWM ripple and brush noise
- Comparator threshold: RV1 adjustable 2.21–2.80 V (user-tuned during calibration)
- Hysteresis: ~4.4 mV (typical), preventing false triggers from sensor noise

### BubbleLink CTRL v1.2 PCB

**Function:** Automatic transfer-pump controller with manual override

**Key Components:**
- **U1 (TLV1822QDRQ1):** Dual comparator (rail-to-rail, 2.4–40 V range, open-drain outputs)
  - Channel A: Gun-current detector (ACS_FILTER vs. RV1 threshold)
  - Channel B: Timer for pump off-delay (HOLD vs. VDELAY)
- **U2 (TLV803EA43DBZR):** 4.38 V / 200 ms brownout supervisor (fail-off safety)
- **Q2 (AO3400A):** N-channel MOSFET pump driver (logic-level, SOT-23)
- **D1 (B340A-E3/61T):** 2–3 A Schottky flyback diode (pump back-EMF suppression)
- **F1 (1812L150/16DR):** 1.5 A PPTC fuse (pump branch protection, temperature-derated)
- **RV1 (Bourns 3296W-1-202LF):** 2 kΩ 25-turn trimmer (gun-detection sensitivity)
- **RV2 (Bourns 3296W-1-104LF):** 100 kΩ 25-turn trimmer (pump shutoff delay, ~350 ms nominal)
- **LEDs:** POWER (always on), GUN ACTIVE (detection), PUMP (pump running); they show through 0.6 mm skin windows in the cap
- **SW1 (PRIME button):** Momentary switch for manual pump trigger (testing, priming); pressed through a plunger under a TPU boot in the cap

In the stick, the PCB hangs component-side up under the cap, heat-staked onto four printed pins. RV1 and RV2 adjust through two small tape-covered windows in the cap.

**Board Specifications:**
- Size: 50 × 40 mm, two-layer FR-4, 1 oz copper, lead-free HASL
- Mounting: Four 3.2 mm NPTH corner holes (43 × 33 mm spacing rectangle)
- SMT assembly: 41 top-side placements; 10 through-hole positions (user-installed connectors, potentiometers, LEDs)
- Power input (J1): JST-XH, 5.0 V ±0.25 V regulated from Buck A
- Sensor input (J2): JST-XH, ACS758 module interface (3-pin)
- Pump output (J3): JST-XH, pump positive and switched negative
- Optional force-on (J4): User-installable override (short to force pump ON)

### Detection and Timing Logic

**Pump activation sequence:**
1. Gun trigger closes; gun motor draws current
2. ACS758 analog output rises (40 mV per amp of gun current)
3. Filtered sensor signal (TP5, ACS_FILTER) reaches comparator threshold (RV1 set point, TP6)
4. U1A comparator pulls DET_N low (open-drain, ~0 V asserted)
5. DET_N triggers Q1 (P-channel), charging HOLD capacitor from buffered half-supply (VMID, TP8)
6. While HOLD > timer threshold (VDELAY, TP10), U1B keeps TIMER_N low
7. Low TIMER_N gates Q3 (P-channel) ON, sourcing Q2 gate voltage
8. Q2 turns on (gate high), pump negative switch closes → pump runs

**Pump shutdown sequence:**
1. Gun trigger released; gun current drops below comparator hysteresis
2. U1A releases DET_N (open-drain, pulled high by R12)
3. Q1 turns off; C7 (HOLD capacitor) begins discharging through R9/RV2/R21
4. After adjustable delay (~350 ms nominal, tuned via RV2), HOLD voltage crosses VDELAY threshold
5. U1B comparator releases TIMER_N (open-drain, pulled high by R12)
6. Q3 turns off; Q2 gate pulls down through R15 (10 kΩ)
7. Q2 turns off; pump stops
8. Residual system pressure maintains hose priming for next trigger

**Manual Prime (PRIME button):**
- Short DET_N directly to ground via momentary switch
- Activates same gate-charge path as gun detection
- Pump runs continuously while button held
- Used for field priming before first use or system refill

**Force-on Fallback (J4 optional, currently DNP):**
- Two-pin header (solder lands present, unpopulated by default)
- If installed and jumpered, directly gates Q2 ON (independent of comparator)
- Fallback workaround if the ACS758 cannot detect very low-current or internally PWM-slowed gun heads (below sensor noise floor)
- Override entirely replaces comparator logic (no automatic shutoff; manual control required)

### Sensor Threshold Calibration

**RV1 Adjustment Range:** 2.21–2.80 V (approximately)
- **Clockwise turn:** Raises threshold, decreases pump sensitivity
- **Counter-clockwise turn:** Lowers threshold, increases sensitivity
- **Typical setting:** ~2.4–2.5 V for one three-head gun (gun current ~10–15 mV rise on sensor output)
- **Calibration procedure:** Set RV1 so pump starts immediately when any gun trigger closes; back off slightly to avoid false triggers from sensor noise

**RV2 (Shutoff Delay) Adjustment:**
- **Nominal range:** 34–574 ms (worst-case modeled 23–737 ms depending on component tolerances)
- **Target setting:** ~350 ms (pump stays on ~350 ms after gun trigger released; prevents rapid on-off cycling from brief trigger releases)
- **Clockwise turn:** Increases delay (slower shutdown)
- **Counter-clockwise turn:** Decreases delay (faster shutdown)
- **Field tuning:** If hoses drain too quickly and bubble flow stops between trigger pulses, increase RV2; if pump overstays after gun release, decrease RV2

---

## Electrical Architecture

### High-Current Power Path (Battery to Guns)

```
2S5P Battery (8.4 V)
    │
    ├─ XT60H connector
    │
    └─ 30 A manual breaker
           │
           └─ 12 AWG silicone wire (main bus)
                  │
                  ├─ [ACS758 sensor input; measures combined gun current]
                  │
                  └─ 12 AWG star harness splits to two 16 AWG XT30U branches
                         │
                         ├─ XT30U Channel 1 → Gun 1 (15 A max per XT30U rating)
                         │
                         └─ XT30U Channel 2 → Gun 2 (15 A max per XT30U rating)
```

**Current Distribution:**
- Main 12 AWG path: Entire system current (pump + both guns) up to 30 A breaker limit
- Per-gun branch 16 AWG: Each gun channel carries up to 15 A (XT30U rated limit)
- Six-head configuration (3 heads per gun): ~17 mA per head at 8.4 V (~3 V per head), combined ~51 mV per gun on ACS758 output (above 10 mV noise floor)
- Dual-gun simultaneous firing: Both channels active, total system current flows through ACS758 and main 12 AWG

### Low-Current PCB Logic and Signal Paths

```
5 V Logic Rail (from Buck A)
    │
    ├─ U1, U2 comparators & supervisor (quiescent ~0.7 mA)
    │
    ├─ ACS758 sensor module (13.5 mA max)
    │
    ├─ RV1, RV2 potentiometers (low current)
    │
    ├─ LED drivers (LED1 POWER ~10 mA; LED2/LED3 conditional)
    │
    └─ Q1, Q3 gate drives (~1 µA quiescent; transient ~100 µA when gating)

Pump Output (Q2 driver)
    │
    ├─ F1 PPTC fuse (1.5 A hold @ 20°C; 1.10 A @ 50°C)
    │
    └─ Q2 N-channel MOSFET
           │
           ├─ [D1 Schottky flyback diode on motor back-EMF]
           │
           └─ J3 pump connector to GROTHEN G528 pump
                  │
                  └─ Pump motor (~0.3 A nominal, <1.1 A peak)
```

### Test Points (Accessible on PCB for field troubleshooting)

| Test Point | Signal | Nominal Range | Purpose |
|---|---|---|---|
| TP1 | +5V_PUMP | 4.95–5.05 V | Pump rail; ripple measurement |
| TP2 | +5V_LOGIC | 4.95–5.05 V | Logic rail; ripple |
| TP5 | ACS_FILTER | 0–5 V | Filtered sensor input |
| TP6 | VTH | 2.21–2.80 V | Comparator threshold (RV1 wiper) |
| TP8 | VMID | 2.40–2.60 V | Buffered half-supply reference |
| TP9 | HOLD | 0–VDELAY | Gate-charge storage node |
| TP10 | VDELAY | 0.98–1.06 V | Timer threshold |
| TP11 | PUMP_GATE | <0.05 V idle; ~4.5 V when pump on | Q2 pump driver gate signal |
| TP12 | PUMP_SW_NEG | ~0 V when pump on; near +5V_PUMP when off | Pump negative leg (Q2 source) |
| TP14 | TIMER_N | 0 V (on) / >4.5 V (off) | Timer comparator output |

---

## Umbilicals and Connectors

### Standard Umbilical Assembly (per gun channel)

Each gun receives a four-foot "umbilical" bundle containing:

```
[Pack side] ←──── Four-foot bundle ────→ [Gun side]
    │                    │                      │
    ├─ XT30U connector    ├─ 16 AWG power pair  ├─ Gun motor
    │ (pack mating)       │ (two conductors)    │
    │                     │                      │
    ├─ Fluid hose barb    ├─ 3.5×5.5 mm         ├─ Gun pump
    │ (3.5 mm barb)       │ silicone tube       │ inlet
    │                     │ (~4 feet)           │
    ├─ Paracord anchor    ├─ 550-cord           ├─ Cable restraint
    │ (load-bearing)      │ (tether, 4 mm)      │ (short loop)
    │                     │                      │
    └─ Umbilical brick    └─ Braided sleeve     └─ Umbilical brick
      (XT30U + tube + tether)  (10 mm PET, protective)  (strain relief)
```

**Specifications:**
- **Power:** Two 16 AWG silicone conductors (black/red); stranded, tinned copper; 5 m spools sufficient for two umbilicals
- **Fluid:** 3.5 × 5.5 mm silicone hose; three barbed nylon unions (one pack-side reducer, two gun adapters)
- **Tether:** 550 paracord (4 mm, 7-strand), listing states 150 kg load-bearing capacity; load-bearing for gun weight and hose strain relief
- **Protective sheathing:** 10 mm braided PET cable sleeving; black; functional, not cosmetic
- **Connectors:** 
  - Pack side: XT30U (female/recessed), strapped with a zip tie into the open-top pocket of the pack-end umbilical brick
  - Gun side: XT30U (male) soldered to 16 AWG pair, strapped into the gun-end umbilical brick
  - Bricks: printed, one at each end of each umbilical (×4). The 16 AWG pair and the tube run in grooves under narrow zip ties; the paracord ties through the outer hole, and the inner hole ties to the stick or the gun
  - Hose side: Barbed nylon unions (pack reducer, gun adapter); secured with narrow zip ties
- **Redundancy:** Two identical umbilicals per system; spare materials are available for additional umbilicals if needed

### Connector Hierarchy

| Connection | Connector Type | Rating | Wire Gauge | Quantity | Location |
|---|---|---|---|---|---|
| Battery → Breaker | XT60H | 30 A | 12 AWG | 1 pair | Disconnect loop below the stick |
| Breaker → Gun channels | XT30U | 15 A | 16 AWG | 2 pairs | Pack core |
| ACS758 input | JST-XH | 2 A | 22 AWG | 1× 3-pin | PCB J2 |
| Pump output | JST-XH | 0.3 A | 22 AWG | 1× 2-pin | PCB J3 |
| Power input | JST-XH | 5 A | 22 AWG | 1× 2-pin | PCB J1 |
| Battery display | Two-wire | 0.1 A | 22 AWG | 1 pair | Voltmeter in the cap, wired after the breaker |

**Design Rationale:**
- XT60H for main battery: 30 A rating exceeds worst-case 25 A system draw; larger connector accommodates thick 12 AWG lugs
- XT30U for gun channels: 15 A rating per gun sufficient (max 17 A per XT30U at full six-head draw, below continuous limit)
- JST-XH for PCB and sensor: Low-current logic signals; keyed connectors prevent reversal
- All connectors female/recessed on live (power source) side for safety during connection/disconnection

---

## Physical Layout

### Pack Interior Geometry

**Container:** MAX LED "M Style" Bluetooth LED pixel backpack (internal geometry to be measured)
- The printed stick and the 1 L reservoir stand side by side inside

**Layout (the stick, about 99 × 78 × 207 mm, standing upright beside the bladder):**
- **Back:** The stick's back goes against the wearer's back
- **Battery:** Left of the sled's spine at the top of the dry side, the highest and driest spot, so the heavy part rides high
- **Electronics:** On the sled beside the battery; PCB hung under the cap
- **Bulkhead:** The tube's floor is the wet/dry divider
- **Pump and fluid manifold:** In the wet cup at the bottom, which drains through its floor
- **Exits:** Both umbilicals, the bladder feed, the LED-backpack USB and the XT60H disconnect loop leave through the cup's floor
- **OFF switch and master disconnect:** Everyday OFF is the breaker's trip button, pressed through the TPU membrane in the right wall. The XT60H loop below the stick is the full battery disconnect (open the bag to pull it); unplug it for storage

**Weight distribution (festival configuration with 1 L solution):**
- 1 L bubble solution: 1.0 kg
- 2S5P battery + printed stick: 0.55–0.65 kg
- Pump, tubing, electronics: 0.3–0.5 kg
- MAX LED backpack carrier: 0.3–0.5 kg
- **Total (rough estimate, not weighed):** ~2.2–2.7 kg. The platform-spec target for the standard rig is 4.6–5.5 lb (~2.1–2.5 kg). Weigh the real build.

### Internal Assembly (Pack Interior)

Everything except the bladder is one printed upright stick. CAD is in `hardware/printed/` ([print guide](../hardware/printed/README.md)); nothing has been printed or test-fitted yet.

**Internal sub-assemblies:**

1. **Cap (control head)**
   - CTRL v1.2 PCB hangs under it, component side up, heat-staked onto four pins
   - LEDs show through 0.6 mm skin windows; PRIME is a plunger under a TPU boot; RV1/RV2 adjust through two tape-covered windows
   - Voltmeter (29.2 mm hole) and USB-C charge port (charger glued under the CHG window) on top
   - A TPU ring seals radially against the tube; 2× M3×10 screws with TPU washers keep it on

2. **Tube and sled (dry section)**
   - The sled slides out of the top. The 2S5P block stands beside a central spine, cell axes front to back, TERM face toward the back
   - Breaker stands upright behind a cross panel, hung by zip ties through its plate holes and spine slots, its trip button and reset lever 2 mm behind the TPU-membrane window in the right wall; BMS stands on edge in a slot along the back wall
   - Buck A, Buck B and the ACS758 sit in open compartments on the front of the panel, each held with a zip tie (no mounting holes used)
   - The cap's ribs press the cell holders and pin the sled onto the bulkhead

3. **Bulkhead**
   - The tube's floor and the wet/dry divider
   - Cables pass through a two-piece TPU grommet with knife-cut slits: a splash baffle, not watertight. Once the wiring is final, seal its top face with a thin bead of neutral-cure silicone (it peels off for service); give cables drip loops below the cup

4. **Cup (wet chamber)**
   - Pump in a 52 × 46 mm pocket, strapped down; three tees, the 4 mm check valve and the bypass slide clamp strapped to the floor slots
   - Bolts on from below with 4× M3×12 into nuts glued into the bulkhead
   - Drains through its floor

5. **Umbilical Management (printed umbilical bricks)**
   - Two four-foot umbilical bundles leave through two 13 mm holes in the cup's floor
   - A brick at each end of each umbilical (×4) gives strain relief, holds the XT30U, and anchors the paracord

### Hose Routing

```
Stick (side by side with the bladder in the MAX LED backpack):

   ┌──── cap ────┐   voltmeter, USB-C, LEDs, PRIME; PCB hangs under it
   │ BATT │ BRK  │
   │ 2S5P │ BMS  │   ← sled slides out of the top
   │      │bucks │
   ╞══ bulkhead ═╡   cables pass through a slit TPU grommet
   │  pump cup   │   pump, tees, check valve, bypass clamp; drains
   └──┬───────┬──┘
     L        R      umbilicals, bladder feed, service cables out the floor

    Umbilicals:  Outlet tee 2 → left 4 ft hose → Gun 1 umbilical
                 Outlet tee 2 → right 4 ft hose → Gun 2 umbilical
```

### Wet/Dry Separation and Condensation Control

- **Dry section:** The tube, closed by the cap's TPU ring at the top and the bulkhead at the bottom. Battery, breaker, BMS, bucks, ACS758, charger and PCB
- **Wet section:** The cup: pump, tees, check valve, slide clamp. The bladder sits outside the stick
- **Bulkhead grommet:** Splash baffle, not watertight. Seal its top face with a thin bead of neutral-cure silicone once the wiring is final (it peels off for service); give every cable a drip loop below the cup
- **Drain path:** The cup drains through its floor
- **Disconnects in the wet zone:** The XT60H pair and the LED-backpack USB plug end up below the stick; wrap them in a bag or heat-shrink
- **Not verified:** The cap seal (wet-test it), pressure relief if a cell fails (the tube only breathes incidentally, through the grommet slits and the cap ring), and charger/BMS temperatures inside the closed tube

---

## Subsystems Reference

The following documents detail each subsystem:

| Subsystem | Document | Scope |
|---|---|---|
| Power System | [04-power-system.md](04-power-system.md) | Battery pack design, BMS configuration, breaker specifications, buck converter tuning, voltage display |
| Fluid System | [05-fluid-system.md](05-fluid-system.md) | Pump selection and tuning, hose sizing, manifold/tee design, recirculation loop calibration, fluid mixing and storage |
| Guns and Heads | [06-guns-heads-and-umbilicals.md](06-guns-heads-and-umbilicals.md) | Donor gun qualification, umbilical assembly, adapter designs, umbilical bricks |
| PCB Design | [07-pcb/overview.md](07-pcb/overview.md) | BubbleLink CTRL v1.2 schematic, BOM, layout, fabrication history, bringup procedures |
| PCB Connectors & Pinout | [07-pcb/connectors-and-pinout.md](07-pcb/connectors-and-pinout.md) | JST-XH pin assignments, test points, connector mechanical drawings |
| PCB BOM and Parts | [07-pcb/bom-and-parts.md](07-pcb/bom-and-parts.md) | Component sourcing, part numbers, equivalents, through-hole user assembly |
| PCB Fabrication | [07-pcb/fabrication-and-assembly.md](07-pcb/fabrication-and-assembly.md) | PCBWay order, Gerber files, SMT assembly, manual soldering guide |
| PCB Bringup & Test | [07-pcb/bringup-and-acceptance-test.md](07-pcb/bringup-and-acceptance-test.md) | Power-on checklist, calibration procedures, acceptance criteria, troubleshooting |
| Printed Parts | [09-printed-parts.md](09-printed-parts.md) | The upright stick (cap, tube, sled, bulkhead grommet, cup), cell holders, slide clamps, umbilical bricks; CAD in `hardware/printed/` |
| Build Guide | [10-build-guide.md](10-build-guide.md) | Step-by-step assembly sequence, hand-solder procedures, fluid system priming, harness routing, first-time setup |
| Parts Order Ledger | [parts/ORDER_LEDGER.md](parts/ORDER_LEDGER.md) | Complete AliExpress and PCBWay orders, delivery status, part variants, pricing |

---

## Electrical Isolation and Safety

The design maintains strict isolation between high-current gun channels and low-current logic:

- **Pump and USB LED backpack current do NOT pass through the ACS758 sensor**, preventing false pump triggers from power-supply transients
- **Gun-current measurement is common** (both XT30U channels combined), enabling single-comparator automatic detection
- **Brownout supervisor (U2) monitors battery voltage** and forces pump OFF during low-battery condition, preventing unpredictable behavior
- **Manual PRIME button provides override** if sensor fails or gun current falls below detection threshold
- **Force-on fallback (J4)** available as a no-respin workaround if the ACS758 cannot detect very low-current gun heads (currently DNP)

---

## Thermal Management

- **Battery cells:** Reach 45–55°C during sustained high-current operation (within Samsung 25R safe operating range of 0–60°C continuous)
- **PCB and components:** Expected <20°C rise above ambient during typical festival use (0.3 A pump + sensor logic)
- **Pump motor:** 6 V peristaltic motor runs cool under low-flow conditions; <60°C expected at maximum continuous output
- **F1 PPTC fuse:** Rated for temperature-dependent hold current; 1.10 A limit at 50°C ambient ensures safe margin below pump stall current
- **Enclosed dry tube:** No active cooling. The tube only breathes incidentally (grommet slits, cap ring). Charger and BMS temperatures inside the closed tube haven't been measured; at 4 A the charger alone may give off around 3–4 W. Charge with the cap off until the first enclosed charge has been checked

---

## Charging and Storage

- **Charging:** 2S USB-C 4 A charger (external module, glued under the cap's CHG window with its receptacle on top; output to BMS P+/P− through an XT30 pair so the cap stays removable); 8–10 hour charge time from empty on typical USB-C PD supply (≥3 A at 5 V). Charge with the cap off until the first enclosed charge has been checked
- **Battery management:** 2S 40 A BMS with cell balancing; stands on edge beside the battery's TERM face in the sled
- **Pre-event:** Charge to 8.4 V minimum; voltage display shows ~4.2 V per cell when ready
- **Storage:** Store charged to 3.7 V per cell (~7.4 V system) for maximum cell lifespan; recharge monthly if unused >2 weeks
- **Travel:** 90 Wh battery within FAA 0–100 Wh limit; no airline approval required (confirmed 2S5P = 90 Wh exact)

---

## Summary

BubbleLink combines a simple, robust power system with straightforward fluid delivery and automatic pump control. The architecture emphasizes field serviceability: all major assemblies (battery, PCB, pump, umbilicals) are user-replaceable; the stick's dry tube over a draining wet cup keeps electronics away from the fluid; and the two-stage calibration (RV1 gun detection, RV2 pump delay) provides tuning flexibility for varying gun types and event conditions. The dual XT30U channels support simultaneous dual-gun operation without manual switching, while the recirculation bypass keeps hoses primed during brief trigger releases, ensuring consistent bubble output across a full festival session.
