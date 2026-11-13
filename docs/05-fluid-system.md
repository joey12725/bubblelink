# Fluid System

Complete hydraulic design and operation of BubbleLink's bubble-solution delivery system: 1 L reservoir, peristaltic transfer pump, low-pressure recirculation loop, distribution tubing and manifolds, donor-head metering, four-foot umbilicals, and concentrate preparation. All components are ordered and specified; the system is designed for festival/rave use with multiple three-to-six-head configurations.

## Table of Contents

1. [Overview](#overview)
2. [Reservoir and Pump](#reservoir-and-pump)
3. [Hydraulic Design](#hydraulic-design)
4. [Tubing and Fittings](#tubing-and-fittings)
5. [Umbilicals](#umbilicals)
6. [Flow Control and Calibration](#flow-control-and-calibration)
7. [Bubble Solution Concentrate](#bubble-solution-concentrate)
8. [Assembly and Testing](#assembly-and-testing)
9. [Open Items](#open-items)

---

## Overview

The fluid system transfers bubble solution from a 1 L reservoir to donor gun heads via a peristaltic transfer pump and low-pressure recirculation loop. The transfer pump maintains adequate hydrostatic pressure to prime four-foot hose runs and overcome elevation changes. Each gun head provides its own metering via internal pump; the pack pump supplies 120–150% of demand, with excess flowing through a recirculation restrictor (a printed slide clamp) back to the pump inlet. This architecture allows a single pump to supply two independent gun channels without the complexity of per-channel metering or the oversizing that would result from series feeding to a splitter.

**Key design intent**: Pack pump eliminates suction-lift problems over four-foot hose runs; donor pumps retain responsibility for output control via trigger and internal mechanics. Recirculation prevents fighting between pack and donor pumps. System operates continuously when armed; gun triggers control donor pump current draw, which pack controller detects to begin energy accumulation.

---

## Reservoir and Pump

### 1 L Hydration Bladder

**Part**: Water Bladder for Hydration Pack (1 L), Blue, UWWWMM Official Store  

| Specification | Value |
|---|---|
| Capacity | 1 L (1000 mL) |
| Material | TPU food-grade, BPA-free |
| Dimensions | 30 cm × 17 cm × 4 cm |
| Weight | 130 g |
| Tube length | 101 cm detachable silicone tube |
| Tube ID/OD | ~0.5 in / ~0.75 in (12.7 mm / 19 mm nominal) |
| Valves | Shutoff bite valve on outlet; double-seal seams |
| Pressure rated | Leak-proof, designed for hiking use |

**Installation note**: The bladder stands beside the printed stick in the bag. The factory 101 cm (40 in) tube should be cut short and enters the stick's wet cup through a hose pigtail on the cup's front wall (labelled IN, 45 degrees down), joined to the bladder tube with a reducer. The bladder outlet connects through a car-hose reducer fitting to the 3.5×5.5 mm system tubing feeding the pump inlet.

### GROTHEN G528 6 V Peristaltic Transfer Pump

**Part**: 6V Low Voltage Peristaltic Pump 150 mL/min DIY Dosing Head, GROTHEN Official Store  

| Specification | Value |
|---|---|
| Voltage rated | 6 V DC (do NOT use 12 V; confirm delivered motor is marked 6 V before connecting) |
| Flow rate nominal | 150 mL/min (with supplied 3×5 mm BPT tube at rated voltage; actual performance depends on solution viscosity and tubing selection) |
| Tube type supplied | 3×5 mm replaceable BPT (silicone/fluoropolymer blend, part of peristaltic drive) |
| Tube alternatives | 2×4 mm (65 mL/min) or 1×3 mm (23 mL/min) available; **do not substitute** without recalibrating flow controller and system pressure |
| Electrical current | Approximately 0.25–0.30 A at rated voltage under load |
| Pressure output | Low-pressure, non-positive-displacement pump (no pressure relief; reliant on external recirculation restrictor for pressure capping) |
| Self-priming | Yes; capable of pumping air for initial hose fill |
| Mounting orientation | Horizontal preferred; vertical mounting with motor below outlet acceptable |
| Size (measured 2026-10-14) | 2 × 1¾ × 1½ in at its thickest (the earlier 60 × 60 × 50 / 65 × 55 × 50 mm figures were wrong) |
| Mounting in the stick | 52 × 46 mm pocket on the left of the wet cup's floor, strapped down with zip ties through the slots either side; drains under it |
| Life expectancy | Peristaltic tube degrades over ~500–1000 hours of operation; replacements available from vendor |

**Calibration note**: Bench-test the delivered pump before installing it: the motor must be marked 6 V, and it should draw <0.3 A at 5 V. This pump, driven at 5 V from Buck A through the PCB's MOSFET (no PWM), delivers approximately 100–120 mL/min with finished bubble solution (thicker than water) through the standard 3×5 tube. Measured three-head gun consumes ~17 mL/min at full blast; eight-head configuration consumes ~45 mL/min, providing a 2.2–2.7× safety margin against starvation. Do not operate pump dry; always fill reservoir before starting.

---

## Hydraulic Design

### System Architecture

```
1 L Reservoir (factory 101 cm tube, cut short)
    │
    ├─ reservoir outlet → car-hose reducer
    │
    ▼
3.5×5.5 mm system tubing
    │
    ├─ inlet to pump
    │
    ▼
GROTHEN G528 pump (motor: 6 V DC, 3×5 mm tube)
    │
    ├─ pump outlet
    │
    ▼
Outlet tee 1 (3.5×5.5 mm / car-hose fitting)
    │
    ├─ (main outlet) → outlet tee 2 → gun 1 / gun 2
    │
    └─ (side branch: bypass slide clamp → check valve → pump inlet tee)
```

Three tees in total: the inlet tee, outlet tee 1 and outlet tee 2 (the outlet side has four connections). Check the assortment has three. The tees, check valve and bypass slide clamp are strapped to the right-hand strip of the stick's wet cup.

### Low-Pressure Recirculation Loop

The recirculation loop allows the pack pump to run continuously without dumping solution into inactive gun heads. Plumbing:

1. Outlet tee 1: main outlet feeds outlet tee 2 and the guns; the side branch is the recirculation return
2. Printed slide clamp on the return leg throttles flow (initial setting: ~0.2–0.3 psi pressure when all outlets blocked)
3. Plastic one-way check valve (4 mm, 0.003 MPa opening pressure, arrow toward the inlet) prevents reverse flow into pump outlet
4. Check valve outlet returns to pump inlet tee (merges with fresh inlet from reservoir)

**Design benefit**: Excess pump flow recirculates at low pressure rather than forcing solution through idle gun heads. Pump runs at one calibrated speed (~6 V); excess capacity is "wasted" internally. This is simpler than PWM speed control and eliminates need for per-channel pump metering.

**NOT a bypass**: The recirculation loop does NOT provide an alternate path around the donor head pumps. Solution still passes through each gun's internal pump when that gun fires; pack pump merely supplies the header at low pressure to prime hoses and overcome static lift.

### Design Pressures and Flow Rates

**Measured gun consumption**:
- Single three-head gun: ~17 mL/min at full blast (overvolted at 8.4 V nominal)
- Two three-head guns (six heads total): ~34 mL/min
- Eight-head configuration (two four-head channels): ~45 mL/min

**Pack pump specification**:
- Nominal 150 mL/min @ 6 V with 3×5 tube
- Actual operation with finished solution: 100–120 mL/min
- Required margin for six-head design: ≥2× (i.e., pump ≥34 mL/min guaranteed)
- Actual margin for six-head design: 2.9–3.5×
- Required margin for eight-head design: ≥1.5× (pump ≥68 mL/min)
- Actual margin for eight-head design: 1.5–1.8×

**Header pressure target** (pump outlet, all channels flowing):
- **Nominal design target**: 0.2–0.3 psi (1.4–2.1 kPa) for priming and maintaining low-pressure header
- At blocked-outlet (recirculation restrictor fully open, no gun flow): ~0–0.1 psi to avoid wasting energy
- Safety cap (restrictor fully closed, no recirculation): ~0.5–1.0 psi maximum, to avoid damaging check valve or overpressurizing donor pump inlet
- **Note**: 0.2–0.5 psi blocked-outlet target is a proposed calibration approach; final performance to be confirmed during prototype testing and field trials.

**Hose friction** (four-foot, 3.5 mm ID, 33.8 mL/min two-gun flow, 10 cP solution):
- Horizontal run: ~0.4 psi
- Four-foot vertical rise: additional 1.73 psi (static lift only)
- Total four-foot vertical: ~2.1 psi (well within donor pump inlet pressure tolerance of 0–2 psi)

### Four-Foot vs. Six-Foot Hose Length

**Standard four-foot hose** (per gun):
- Volume: 9.8 mL
- Friction loss: 0.4 psi (horizontal), 2.1 psi (vertical four feet at 33.8 mL/min)
- Dry priming time: ~6–7.5 seconds at 100+ mL/min pump
- Voltage drop (16 AWG copper, 10 A): 0.24–0.32 V
- Recommended use: typical festival setup, dancer height 5–7 feet, gun at chest/shoulder level

**Six-foot hose** (extended use only):
- Volume: 14.5 mL
- Friction loss: higher than four-foot
- Dry priming time: ~12–15 seconds at 100+ mL/min pump
- Voltage drop: 0.48 V (double four-foot)
- Recommended use: unusual routing (e.g., longboard towing, arm extension), not standard

**Decision**: Four feet is standard. Six feet available as optional extension for rare cases. Do not use six feet as default.

---

## Tubing and Fittings

### System Tubing and Fittings

**3.5 mm ID × 5.5 mm OD food-grade silicone tubing** (entire system):
- Material: Food-grade transparent silicone gel, BPA-free
- Diameter: 3.5 mm nominal ID, 5.5 mm OD
- Sections: from bladder reducer through pump inlet, pump outlet, all channel feeds, and recirculation loop
- Advantages: low friction, flexible, transparent for visual inspection, standard sizing for car-hose assortment fittings
- Source: Ordered as 5 m roll (part Shop1105214603, 3.5×5.5 mm Transparent Flexible Silicone Tube)
- **NOTE**: This is the ONLY system tubing; there is no 6 mm trunk line

**Car-hose fitting assortment**:
- **Part**: Plastic car-hose connector set, Shop1103411025 Store
- **Includes**: reducers (1/4" to 3/8" to mate bladder's large factory hose to 3.5×5.5 mm silicone), tees, Y-splitters, straight connectors
- **Material**: Polypropylene (plastic), rated <850 kPa (124 psi)
- **Exact contents**: Assortment may vary; select pieces as needed for manifold construction

**Manifold and fluid path**:
1. Pump outlet → outlet tee 1 (connects to: main distribution path and recirculation return leg)
2. Main distribution → outlet tee 2 → 3.5×5.5 mm tubing to gun 1 and gun 2, each through its own slide-clamp shutoff
3. Recirculation leg (tee 1's side branch) → bypass slide clamp → 4 mm check valve (0.003 MPa cracking) → return to pump inlet tee
4. Pump inlet tee merges fresh inlet from the reservoir with the recirculation return (there is no filter)

### Gun Channel Hoses (Four-Foot Standard)

**3.5 mm ID × 5.5 mm OD food-grade silicone tubing**:
- **Part**: Transparent Flexible Silicone Tube, Shop1105214603 Store
- Material: Food-grade silicone gel, transparent
- Flexibility: excellent; easy to bundle in umbilical sleeve
- Temperature rated: -20°C to +60°C storage, -20°C to +45°C operation
- Pressure rated: suitable for 0–2 psi operation (peristaltic pump outlet)
- One 5 m roll provides four 4-foot (1.22 m) channel hoses plus spares

**Hose routing**:
- Outlet tee 2 → slide clamp → 3.5×5.5 mm hose (one per gun channel, 4 feet), leaving through a 6.0 mm hose pigtail at 45 degrees on the cup's outer wall (60-80 mm of tube; the umbilical hose joins it with a straight barbed connector)
- Field termination: nylon barb from car-hose assortment (pressed onto hose end, secured with narrow zip tie)
- Gun-side termination: nylon barb from car-hose assortment; the tube runs in a groove of the gun-end umbilical brick

### Check Valve (Recirculation Loop)

**4 mm one-way plastic check valve**:
- **Part**: Plastic Check Valve One-Way Pagoda Inline, BigBigBear Tech Store

| Specification | Value |
|---|---|
| Valve type | One-way check (pilot-operated, low-cracking pressure) |
| Cracking pressure | 0.003 MPa (0.04 psi, ~1 inch water column) |
| Port size | 4 mm (barb connection) |
| Body material | Polypropylene (PP) |
| Internal core | Food-grade silicone |
| Spring | 304 stainless steel |
| Temperature range | -20°C to +130°C (rated; operating envelope -20°C to +60°C sufficient) |
| Forward direction | Opens above 0.003 MPa, passes recirculation flow ~freely |
| Reverse direction | Blocks backflow; zero leakage under normal 0–0.5 psi pressure cycling |

**Installation**: Bypass slide clamp outlet → 4 mm hose ~6 inches → check valve 4 mm inlet barb → 4 mm hose ~12 inches → inlet tee 4 mm inlet. Arrow on valve body points downstream (toward pump inlet tee).

---

### Slide Clamp (Recirculation Bypass Adjustment)

**Printed slide clamp** (one of three identical clamps; the other two are the channel shutoffs):
- Outlet tee 1 side branch → slide clamp → check valve → pump inlet tee
- Assembly: lay the tube in the channel and slide the slider on from the open end, ridge down. The 70 mm clamp runs front to back in the cup
- Operation: slide toward the arrow to close. The first ~8 mm goes from fully open (6.0 mm gap) to 2.4 mm; the next 22 mm is fine adjustment (about 0.08 mm per mm); it seals at 0.6 mm against the stop blocks
- Initial setting: fully open (minimum back-pressure)
- Commissioning adjustment: slowly slide the clamp closed until pump outlet pressure (measured at temporary test port) reaches 0.2–0.3 psi with all downstream outlets blocked
- Lock-down: the shallow ramp self-locks (no screw); wet-test that it holds. Once calibrated, do NOT adjust further during operation

---

## Umbilicals

### Four-Foot Standard Umbilical

Each gun receives one four-foot umbilical containing:
- Two 16 AWG silicone-insulated copper wires (red and black)
- One 3.5 mm ID × 5.5 mm OD silicone fluid tube
- One 4 mm 550 paracord (load-bearing tether; **this cord carries the gun weight if dropped**, not the electrical wire)

**Assembly**:
1. Cut lengths to exact 4 feet (48 inches / 1.22 m): two 16 AWG, one 3.5 mm tube, one paracord
2. Gather into one 8–10 mm braided PET expandable sleeve
3. Solder XT30 connectors to wire leads
4. Fit a printed umbilical brick (ASA or PETG) at the gun end: drop the XT30U into the open-top pocket and strap it with a zip tie through the slots beside it; run the 16 AWG pair and the fluid tube in their grooves under narrow zip ties; tie the paracord through the outer hole, and tie the inner hole to the gun. At the pack end, the male XT30U plugs into the cup's port well, the hose joins the port's pigtail, and the paracord ties through the port's U-tunnel
5. Press nylon barb from car-hose assortment onto fluid tube; secure with narrow zip tie
6. Test for continuity (XT30 wires), fluid leak (at barb), and mechanical strength (paracord under load)

### Six-Foot Extended Umbilical (Optional)

Identical to four-foot except:
- Lengths cut to exact 6 feet (72 inches / 1.83 m)
- Higher voltage drop (0.48 V per 10 A) acceptable only for rare use cases
- Reserved for unusual routing or extreme arm extension

---

## Flow Control and Calibration

### System Priming (Initial Fill and Dry-Start)

1. Fill 1 L reservoir with prepared bubble solution (see [Bubble Solution Concentrate](#bubble-solution-concentrate) section)
2. Close or unplug both gun XT30 connectors (no current draw; pump starts only on PRIME button or gun trigger)
3. Apply power (close main XT60 battery connector)
4. **LED indication**: POWER LED (green) lights; GUN ACTIVE (yellow) and PUMP (red) LEDs off
5. Press the momentary PRIME button (SW1) through the boot in the stick's cap (a deliberate fingertip press inside the guard bezel) to run the pump manually for priming
6. Hold PRIME button; observe hose outlets for solution flow
7. Once solution reaches both outlet fittings, release PRIME button
8. Connect both gun XT30 connectors
9. Gently squeeze each gun trigger; solution should flow immediately from the head metering pump (no delay or spitting expected once hose is primed)

**Note**: Dry-run time depends on hose volume (9.8 mL for four feet). At 100+ mL/min pump, expect 6–7 seconds to fill. If hose does not prime within 20 seconds, check for:
- Air locks in pump inlet line (bleed by tapping inlet tee)
- Reservoir empty or low (refill)
- Pump electrical failure (check PUMP LED; verify 6 V at pump motor leads)

### Pressure Calibration (Restrictor Setting)

1. After priming, install temporary pressure test port on pump outlet tee (use a 0–5 psi water-column gauge with 1/8" barb fitting)
2. Close both gun channel slide clamps to simulate zero gun flow
3. Apply power and press the momentary PRIME button (SW1) to run the pump
4. Observe gauge reading; should settle to ~0.1–0.2 psi within 5 seconds
5. If pressure exceeds 0.3 psi, slowly slide the bypass slide clamp back toward open until pressure drops to 0.2–0.3 psi
6. If pressure drops below 0.1 psi, slide the clamp slightly further closed
7. Once calibrated, mark the slider position (e.g., sharpie line on the clamp body) and do NOT adjust further during operation
8. Remove test gauge; cap or plug the test port
9. Unblock gun hoses and proceed to normal operation

**Why 0.2–0.3 psi?** This pressure is sufficient to prime hoses and provide positive inlet pressure to donor head pumps (which typically tolerate 0–2 psi inlet pressure). Higher pressure wastes pump energy and increases wear; lower pressure risks cavitation or incomplete priming on cold solution.

### Donor Head Qualification (Per-Gun Acceptance Test)

Before integrating a new donor gun head into the system:

1. Mount donor head on test sled with standard XT30 connector and 4-foot hose
2. Connect to bench power supply (adjustable 0–8.4 V DC) and flow-measurement container
3. Pressurize inlet to ~0.3 psi (e.g., using small hand pump or by connecting to pack pump via tee)
4. Measure solution consumption (mL/min) at various trigger positions and voltages:
   - Full voltage (8.4 V), full trigger: record peak flow (should be 17 mL/min for single-head, 34 mL/min for two-head equivalent)
   - Minimum usable voltage (e.g., 5 V): record minimum flow and whether pump runs smoothly
   - Halfway trigger: record intermediate flow
5. Measure electrical current draw (A) at each setting
6. Check off-state leakage: close trigger, wait 10 minutes, measure any drip (should be zero or <1 drip/min)
7. Repeat with finished bubble solution (not water) to verify performance in thicker medium
8. **Label donor**: Attach waterproof label with qualified voltage range, peak current, flow rate, and acceptance date (e.g., "D1 — 5.0–8.4 V — 11 A peak — 17 mL/min — accepted 2026-10-14")

---

## Bubble Solution Concentrate

### JOYFY Concentrate Mixing

**Product**: JOYFY 32 oz (946 mL) concentrated bubble solution, JOYFY US Store  

**Mixing ratio** (from JOYFY label):
- Concentrate: 1 part
- Water: 9 parts (1 part concentrate + 9 parts water)
- Total yield: 10 parts (32 oz concentrate makes up to 2.5 gallons / 320 oz finished solution from one 946 mL bottle)
- **Alternative recipes**: See [`docs/16-roadmap-future-extensions.md`](16-roadmap-future-extensions.md) for other tested formulations (Lulu, JOYIN, outdoor stream matrix)

**Preparation procedure**:
1. Pour concentrate into large clean container (gallon-sized pitcher or jug)
2. Add water (distilled or fountain water; tap water acceptable if soft/low mineral content)
3. Stir gently for 1–2 minutes until fully mixed; avoid creating foam
4. Let stand 5–10 minutes; foam will settle
5. Pour into smaller 100–200 mL bottles for field transport and reservoir filling (use funnel to avoid spills)

**Storage**:
- Finished solution: refrigerate if not used within 1 week (preserves bubble quality; prevents algae/bacterial growth without preservative)
- Concentrate: store cool and out of direct sunlight (shelf life ~6 months unopened)
- Avoid metal containers; use glass or food-grade plastic only

### Germall Plus Preservative (Optional, Not Included)

**Status**: Optional (Liquid Germall Plus, 100 g); use is conditional.

**Germall Plus** (sodium methylisothiazolinone + sodium methylchloroisothiazolinone blend):
- **Purpose**: Biocide preservative for mixed bubble solutions to prevent mold and bacterial growth in stored solution
- Typical concentration in finished solution: 0.1% (1 mL per liter)
- **Dosage**: To be decided based on storage duration and field testing

**Recommendation**: 
- **NOT REQUIRED** for festival use lasting 1–4 hours (solution consumed in single day)
- **OPTIONAL** if planning extended storage (>1 week) or if operating in warm/humid conditions where algae might grow
- If used, add 0.1% concentration (e.g., 0.1 mL per 100 mL finished solution) and test with donor head before field deployment (some preservatives can affect bubble quality)
- Verify compatibility with local toy-product and food-contact regulations before any public performance or sale (bubble guns are often classified as toys)

---

## Assembly and Testing

### Manifold and Return Loop Assembly

1. **Lay out parts on workbench**:
   - Three car-hose tees from the assortment (inlet tee, outlet tee 1, outlet tee 2), sized for 3.5×5.5 mm / 1/8" connections
   - Three printed slide clamps: one bypass restrictor, two channel shutoffs
   - Check valve (4 mm one-way) for recirculation return
   - 3.5×5.5 mm hose lengths (pre-cut from 5 m roll) for:
     - Inlet from bladder to pump inlet (via car-hose reducer from factory tube)
     - Outlet from outlet tee 1 to outlet tee 2, and from tee 2 to the gun channels
     - Recirculation loop: tee 1 side branch → slide clamp → check valve → inlet tee
   - Car-hose reducers (1/4" to 3/8") to adapt bladder factory hose to 3.5×5.5 mm

2. **Connect pump inlet path**:
   - Bladder factory tube (cut short) → car-hose reducer → 3.5×5.5 mm hose → inlet tee → pump inlet. The bladder feed enters the cup through its IN pigtail on the front wall
   - Pump inlet tee merges fresh inlet with recirculation return flow

3. **Connect pump outlet path**:
   - Pump outlet (3×5 mm tube) → outlet tee 1 → two 3.5×5.5 mm outputs:
     - Main outlet: 3.5×5.5 mm hose to outlet tee 2
     - Side branch: 3.5×5.5 mm hose to the bypass slide clamp

4. **Connect recirculation loop**:
   - Bypass slide clamp output → 4 mm hose (~6 inches) → check valve inlet barb
   - Check valve outlet → 4 mm hose (~12 inches) → pump inlet tee inlet
   - Ensure check valve arrow points downstream (toward pump inlet)

5. **Gun channel connections**:
   - From outlet tee 2: one slide clamp and one 3.5×5.5 mm hose (4 feet) per gun channel, out through the hose pigtails on the cup's outer wall (gun 1 and gun 2 ports)
   - Each hose terminates in nylon barb from car-hose assortment (pressed on and secured with narrow zip tie)
   - Run the tube through the gun-end umbilical brick

6. **Strap down** the pump in its 52 × 46 mm pocket and the tees, check valve and bypass clamp to the four tie slots on the cup's right-hand strip

7. **Secure all connections**:
   - Use narrow zip ties at each barb connection; warm silicone tubing in hot water to stretch before assembly
   - Verify no leaks with dry-run (no solution yet); apply gentle hand pressure to inputs and look for squirts at fittings
   - Tighten any weeping connections by adjusting zip tie or reseating barb

### Leak Testing Under Pressure

1. Fill reservoir with water (not solution; easier cleanup)
2. Prime hoses as per [System Priming](#system-priming) section
3. Once primed, run pump with both channel slide clamps closed for 2 minutes
4. Inspect all manifold connections, barb fittings, and zip ties for weeping or dripping
5. Pay special attention to pump inlet tee (high flow path under pressure)
6. If leaks observed, adjust zip tie or reseat barb by removing hose, cleaning barb tip, and reinserting firmly with mallet tap
7. Repeat test until zero leaks observed over 5 minutes of continuous pump operation

### Field Readiness Checklist

Before field deployment (festival event):

- [ ] Reservoir filled with finished bubble solution
- [ ] Pump outlet hoses primed (solution reaches both gun outlets of outlet tee 2)
- [ ] Bypass slide clamp set to 0.2–0.3 psi (checked with test gauge) and holding
- [ ] All gun XT30 connectors seated and locked
- [ ] All gun umbilical fluid barbs drip-tested (no solution leaking from unused channels)
- [ ] Donor head electrical contacts clean (no corrosion on XT30 pins)
- [ ] System power-on verified (POWER LED green; pump ready to start on gun trigger or PRIME button)
- [ ] Battery fully charged (8.4 V nominal at XT60 connector)
- [ ] Gun triggers tested at low, medium, and high positions (solution flows smoothly)
- [ ] Backup concentrate bottle and mixing pitcher packed in backpack side pocket
- [ ] Cleanup supplies: small funnel, paper towels, squeeze bottle with fountain water for rinsing hands

### Post-Event Cleanup and Storage

1. **In field** (end of event):
   - Unplug gun XT30 connectors
   - Pump remaining solution into waste container
   - Spray hoses with fountain water to flush residual concentrate (prevents sticky buildup)

2. **At home**:
   - Disconnect all umbilicals from pack
   - Rinse all hoses, fittings, and bladder interior with clean water (use rinsing syringe or funnel)
   - For bubble machines prone to residue: prepare ~0.5 L fresh water, run pump for 10–15 seconds with hoses submerged in water to flush pump internal path
   - Dry hose interiors by blowing air or hanging vertically overnight
   - Store in sealed bag or box to prevent dust accumulation

3. **Pump storage**:
   - Leave pump dry (no fluid inside motor or tube for >1 week)
   - If extended storage (>2 weeks), run pump for 5 seconds with water only once per month to prevent seal drying

---

## Open Items

1. **Pump replacement tube availability**: GROTHEN official store lists multiple tube configurations. Confirm whether spare 3×5 BPT tubing is available directly from vendor or whether entire pump unit must be replaced if primary tube degrades.

2. **Concentrate alternative**: JOYFY is the commercial concentrate in the current design. If JOYFY becomes unavailable, test alternative concentrates for compatibility with donor pump suction and final bubble quality.

3. **Slide clamp hold**: The clamp's self-locking ramp is printed, not proven. Wet-test that the bypass and channel clamps hold their setting under pump pressure.

4. **Check valve backward-flow threshold**: BigBigBear 4 mm valve is rated 0.003 MPa cracking pressure. Confirm that static pressure in blocked-outlet condition does not cause creep-back into recirculation path over extended operation (e.g., 2+ hour festival).

