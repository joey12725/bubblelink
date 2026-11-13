# BubbleLink: Overview and Requirements

BubbleLink is Joey's custom bubble-gun backpack system, designed for sustained bubble production at music festivals and raves. The core platform consists of a 2S5P (90 Wh) battery, one-liter solution reservoir, automatic transfer pump, two independent gun channels, and a pump-controller PCB with USB-C charging—all integrated inside a MAX LED "M Style" LED pixel backpack, where everything except the bladder lives in one printed upright "stick" standing beside the bladder. The system supports multiple concurrent bubble guns (donor mechanisms from uncharacterized children's toy guns) with dual-channel operation, fixed full-power output, and festival-compliant form factors.

---

## Table of Contents

- [Who It's For and How Joey Uses It](#who-its-for-and-how-joey-uses-it)
- [Functional Requirements and Targets](#functional-requirements-and-targets)
- [System Constraints](#system-constraints)
- [MVP Scope](#mvp-scope)
- [Future Extensions](#future-extensions)
- [Design Philosophy](#design-philosophy)

---

## Who It's For and How Joey Uses It

Joey uses bubble guns at music festivals (multi-hour events) and raves, dancing continuously with the pack as a wearable system. Key usage patterns:

- **Festival runtime:** 10 pm to 3:30 am (~5 hour block) with light-to-moderate bubble production, punctuated by high-intensity dance peaks during drop moments.
- **Consumption baseline (measured):** Three-head gun at ~70 W draws approximately 16.9 mL/min of bubble solution (measured under overvolted operation).
- **Actual field consumption:** Approximately 37% duty cycle (37 minutes of firing per 100 minutes elapsed) during "very dance heavy" usage; lower 12–20% duty during typical nights.
- **Portability:** Worn as a backpack while dancing. Must fit within typical venue bag rules (hydration packs are usually allowed; large rigid backpacks often are not). Battery, pump, and electronics live in one printed upright stick (about 99.6 × 77.8 × 220 mm) beside the bladder; two umbilicals plug into ports on the cup's outer wall (nothing exits underneath), so it can move to a different bag easily.
- **Weight sensitivity:** Loaded festival config (1 L solution + 1 L drinking water + battery + pump + electronics + bag) targets 6.8–7.7 lb (3.1–3.5 kg); without added drinking water ~4.4–5.3 lb (2.0–2.4 kg).
- **Camelback experience:** Joey previously used hydration bladders; BubbleLink is a hybrid system allowing both bubble solution and drinking water (optionally) in same pack.

---

## Functional Requirements and Targets

### Power System

- **Battery topology:** 2S5P Samsung INR18650-25R (10 cells total)
  - Nominal voltage: 7.2 V (2S serial, 5 parallel per column)
  - Nominal capacity: 12.5 Ah
  - Nominal energy: **90 Wh** (FAA compliant for air travel with no special approval)
  - Fully charged: 8.4 V (4.2 V per cell)
  - Discharge floor: 6 V nominal (3 V per cell)
  - Cells per-row: 5 cells, two offset rows in printed MID/TERM cell holders (19.9 mm pitch); the two rows face opposite directions

- **BMS:** 40 A automatic-recovery 2S lithium battery management system with cell balancing and temperature cutoff (~55–60°C discharge stop, ~45°C reset)

- **Charging:** SZHJW USB-C boost charger module (2S 4A variant) → BMS → cells
  - Input: USB-C, accepts any standard USB-C power adapter
  - Charge time: 7–8 hours nominal for 90 Wh at ~2 A rate
  - Charge-only path, isolated from gun and accessory power

- **Main protection:** 40 A BMS + one 30 A manual-reset circuit breaker (Type B, YONGRUN, M6 studs) mounted immediately after BMS, in the + line only. Ring lugs (SC10-6, solder-filled) connect the 12 AWG main wire; never solder wire directly to breaker studs. Its reset lever is reached only with the cap off and the sled out. The power key on the cap top (an XT60H socket and key) is the OFF switch (all loads off; the battery stays connected to the BMS, the charger and one pin of the key socket; for storage, key out and key blank in)

- **Battery voltage display:** Two-wire DC 4–100 V round LED voltmeter in the top of the stick's cap, reading battery voltage, wired after the breaker so tripping it turns the meter off; printed reference label showing 8.4 V (full) and 6 V (cutoff) thresholds

- **Accessory USB output:** 5 V regulated via Buck B converter (external, YxPC 6–20 V → 5 V module) providing power for LED backpack display and future accessory panels; Buck B stands on a shelf on the tube's front wall with its own USB-A receptacle in (or right behind) a window in the tube's outer wall (labelled LED 5V), so the backpack cable plugs straight in (no extension cable, no USB plug inside the stick). Its input runs from the sled with a 2-pin JST-XH plug

### Fluid System

- **Reservoir capacity:** Exactly 1 L removable TPU bladder with wide opening and existing outlet hose reusable for first few inches
  - Runtime at measured consumption: 2 L guaranteed with reserve; ~2.7–3.0 L probable with full discharge; 4 L not promised
  - Reservoir removable for refill and inspection without disassembling pack

- **Bubble solution:** Commercial 9:1 concentrate (Lulu Home or FoamDaddy recommended for initial testing) diluted per manufacturer instructions; DIY recipes (Dawn/glycerin/J-Lube) deferred to post-MVP optimization

- **Pump:** One shared peristaltic transfer pump, permanent installation in pack
  - Nominal voltage: 6 V DC (overvolt-capable in 2S 7.2–8.4 V context)
  - Flow rate: ≥70 mL/min at 6.0 V with recirculation closed; baseline ~100 mL/min typical
  - Current draw: <1 A
  - Self-priming, replaceable 3×5 mm tube (3 mm ID × 5 mm OD)
  - Suction/lift: ≥5 m claim

- **Tubing standard:** 3.5 mm ID × 5.5 mm OD food-grade transparent silicone throughout—pump inlet, outlet, recirculation loop, and both four-foot gun channels
  - Four-foot umbilical (standard per gun): approximately 9.8 mL priming volume; dries primes in 12–17 seconds
  - Six-foot umbilical (experimental): approximately 14.5 mL priming volume; used only for unusual routing (e.g., mounted on longboard)
  - Tubing secured only at reservoir adapter, pump inlet, pump outlet, and Y-splitter with narrow 2.5 mm zip ties (correctly matched silicone + barbs hold at low pressure)

- **Hydraulic architecture:** Bladder → inlet tee → pump → outlet tee 1 → outlet tee 2 → two four-foot branches (one per XT30 gun channel). Outlet tee 1's side branch returns through a printed slide clamp (restrictor) and the 4 mm check valve (arrow toward the inlet) to the inlet tee (recirculation loop). Three tees in total. Target bypass pressure: 0.2–0.5 psi.

- **Priming:** Automatic via gun trigger hold. Holding either gun trigger starts the transfer pump; dry line primes and gun fires immediately on release. The PCB's PRIME button (SW1), pressed through a TPU plunger under a TPU boot, guarded by a bezel, in the stick's cap, also runs the pump. The bezel's rim sits above the boot, so it takes a deliberate fingertip press.

### Electrical Architecture

- **Gun channels:** Two independent XT30 power outputs (16 AWG branches from 12 AWG main star harness)
  - Per channel: 15 A continuous rated per XT30 datasheet
  - Concurrent dual-gun operation supported
  - Combined multi-head wand (consuming both channels simultaneously) supported with shared four-head-per-channel configuration

- **Umbilical specification (per gun):**
  - Two 16 AWG silicone conductors (red/black power)
  - One 3.5 mm ID × 5.5 mm OD silicone fluid hose
  - One 4 mm load-bearing paracord (mechanical tether; cord carries gun drop load, not electrical wire)
  - All four elements bundled in 8–10 mm braided PET sleeve
  - Connectors: a printed umbilical brick at each end (strain relief, XT30U strapped in an open pocket, paracord anchors) + fluid barb

- **Gun-side electronics:** Fixed full-power triggers on both channels. No per-gun driver PCBs or signal wires in umbilical.

- **Pump activation:** Pack-side current detection via ACS758LCB-050B Hall-effect current-sense module (measures combined gun channels) → analog comparator threshold + off-delay timer → pump MOSFET gate driver. Pump runs whenever combined gun current exceeds calibrated threshold (~5–10 A); ~350 ms off-delay after trigger release allows the gun's internal pump (if any) to finish priming.

- **Main controller PCB:** Custom design (BubbleLink CTRL v1.2) by PCBWay, includes:
  - Analog comparator and ~350 ms off-delay timer for pump trigger logic
  - Pump MOSFET and flyback diode protection
  - 5 V buck regulator supply for pump and controller logic
  - Power/gun-active/pump-active indicator LEDs
  - Adjustable threshold (RV1) and off-delay (RV2) trimmers for field calibration
  - PRIME momentary button for manual pump activation
  - Connectors for ACS758 current sensor input (3 wires), pump motor output (2 wires), and 5 V supply
  - No MCU or firmware required; purely analog control

- **Voltage control strategy:** Fixed full-power operation via momentary trigger. Raw 2S bus voltage (~6.0–8.4 V) applied directly to gun channels; no PWM modulation or potentiometer control in MVP scope. Donor head can run at any voltage from ~3 V to 8.4 V, with field power determined by pack discharge state and dual-gun loading.

### Bubble Gun Heads

- **Donor strategy:** Retail toy-gun heads extracted from random available toys and mounted on sleds connected to BubbleLink channels. Donor motors are uncharacterized and may have unknown original voltage ratings, but tolerance is permissive post-measurement.
- **Baseline hardware (not a finished BubbleLink):** Joey's existing three-head overvolted bubble gun (2S1P 18 Wh, ~70 W firing power, ~16.9 mL/min continuous flow) serves as the performance reference and is the intended first donor head for one channel. See the baseline gun section of [canonical facts](canonical-facts.md) for existing gun details.
- **Future variants:** Additional donor heads will be selected post-measurement based on bubbles-per-watt, throw distance, reliability, size, and thermal behavior
- **Head output rating:** Each head is powered at raw 2S bus voltage (~6.0–8.4 V depending on discharge and dual-gun loading). No per-gun PWM or voltage regulation in MVP; voltage floor and ceiling are determined by battery discharge state and total system load.

### System Integration

- **Heads per channel:** 1–4 heads per gun
  - Measured (2026-10-27): each donor head firing at full power adds ~1.39 A (1.51 A whole system with one head)
  - Two-head gun: ~2.8 A; four-head gun: ~5.6 A
  - Three-head gun (Joey's baseline, a different, overvolted gun): ~10–14 A nominal draw
  - Per-channel ceiling: 15 A (XT30U)

- **Dual-channel loading:** Two guns simultaneously. With the measured heads, eight heads (four per channel) draw ~11.3 A whole system (~5.6 A per channel); the design still allows ≤26 A continuous and ≤40 A brief motor-start surge for hungrier heads. Battery runtime per head count: [04-power-system.md](04-power-system.md#measured-system-current-joey-2026-10-27).

- **Power distribution:** Single 30 A main breaker (all gun channels + pump + accessories); no individual channel breakers initially installed (retrofit space available if commissioning tests exceed 18–20 A sustained single-channel fault current)

### Carrier and Enclosure

- **Pack model:** MAX LED "M Style" Bluetooth LED pixel backpack—a hydration-pack-form-factor carrier with built-in display capability (status unknown until measured). Holds the printed stick (battery, pump, controller PCB) and the fluid reservoir.
  - Display is dual-use: serves as Tracer cosplay component and may provide BubbleLink status feedback
  - Required fit: room for the stick (about 99.6 × 77.8 × 220 mm) standing upright beside the 1 L bladder. Two umbilicals plug into ports on the cup's outer wall. The bag's internal geometry is unknown until measured

- **Internal organization:** Everything except the bladder is one upright printed stick: a control-head cap (PCB hung underneath, voltmeter and USB-C charge port on top) over a dry tube holding a slide-out sled (battery, breaker, BMS, Buck A, ACS758; Buck B stands on a shelf on the tube wall). The tube's floor is the bulkhead (wet/dry divider); cables cross it through a slit TPU grommet. Below it, a wet cup holds the pump and fittings and drains through its floor. See [docs/09-printed-parts.md](09-printed-parts.md).

- **Printed components** (OpenSCAD sources and STLs in `hardware/printed/`):
  - The stick: cap, tube, sled, cup, PRIME guard bezel and grommet drip skirt (ASA), plus TPU cap ring, grommet halves, PRIME boot, PRIME plunger, screw washers, battery pads, pump mat, shim strips, the trimmer, USB-C and USB-A plugs, gun port caps, key blank and gasket, and the power key (32 STLs in all with the four stick fit coupons)
  - Cell holders MID and TERM (original 5×2 offset design, 19.9 mm pitch)
  - Slide clamps ×3 (bypass restrictor and both channel shutoffs)
  - Umbilical bricks ×2 (one at the gun end of each umbilical)
  - A fit coupon, printed first to set cell-bore and connector clearances

- **Hydraulic zoning:** Pump and fittings in the wet cup at the bottom of the stick, which drains through its floor. Battery and electronics in the dry tube above the bulkhead, sealed at the top by the cap's TPU ring (not yet wet-tested). The grommet is a splash baffle, not watertight.

- **Moisture tolerance:** Pack is a hydration-pack-form-factor system; intended for dance use in humid/wet venues. Objective is preventing liquid pooling around electrical hardware, not keeping entire pack pristine.

### Hydration During Events

- The 1 L BubbleLink solution reservoir is a UWWWMM hydration bladder with a 101 cm detachable drinking tube included. This tube remains part of the bladder assembly but is unused for bubble solution (the system has its own outlet fitting for solution transfer). Joey may elect to carry a separate external drinking bladder if they choose to drink during longer events. Not mandatory for MVP.

---

## System Constraints

- **Budget sensitivity:** Acknowledged; component substitutions preferred over premium solutions (e.g., cheap plastic check valve ~$1–3 instead of specialized $15+ part; printed umbilical bricks instead of cable glands; fish paper + electrical tape instead of Kapton + heat shrink)
- **Component untestedness:** Donor toy guns sourced second-hand; pump flow and motor specs measured post-receipt only. Tolerances permissive to accommodate variance.
- **Single consolidated order:** All purchased parts ordered at once from AliExpress (~2026-08-06) plus PCBWay controller order (timing critical for manufacturing; 3–5 days PCBWay production + shipping)
- **Festival clearance:** Bubble solution (soap/detergent) is prohibited at some venues. System form factor must remain hydration-pack-like for security. Explicit venue approval required before event (a festival approval pending).
- **TSA/airline compliance:** 90 Wh battery remains under 100 Wh FAA threshold, permitting carry-on transport with protected terminals (no airline approval required). Spare packs and 2S6P or larger modules deferred (would exceed 100 Wh, requiring approval).
- **Manufacturing constraints:** No access to production spot-welders on-site; cells pre-assembled with nickel-plated steel tabs + solder joints. 3D printers available (Creality K2 Plus 350³ mm, Bambu Lab A1 256³ mm); enclosures and sleds designed to fit.

---

## MVP Scope

The minimum viable product completes and validates the core BubbleLink platform.

### Includes

- One-liter removable bubble-solution reservoir
- 2S5P (90 Wh) battery with BMS and USB-C charging
- Battery voltage display (4–100 V two-wire LED voltmeter in the stick's cap)
- One shared automatic peristaltic transfer pump
- Two independent gun channels via XT30 power connectors
- Concurrent dual-gun operation (each gun independent; wand option consuming both channels)
- Printed umbilical bricks (×2) at the gun end of each umbilical: strain relief, XT30U in an open pocket, paracord anchors; the pack end plugs into a port cluster on the cup's outer wall
- Fixed full-power gun triggers (momentary trigger on each channel, raw 2S bus voltage with no PWM modulation)
- Four-foot standard hose lengths per gun
- Six-foot experimental hose option (optional extended routing)
- Recirculating hydraulic bypass (pump supplies excess, slide-clamp restrictor routes back to inlet; prevents flooding)
- LED backpack power (5 V via Buck B, out of its own USB-A port through the tube's outer wall)
- One printed upright stick (battery, electronics, pump) beside the bladder in the MAX LED "M Style" LED pixel backpack
- Donor gun integration: a pair of dual-head guns (2 guns × 2 donor heads, 4 matched heads stripped from ~20 bubble guns); gun/head mounts not designed yet

### Does Not Include

- **Piston-style variable-power triggers:** Future extension; requires donor-side potentiometer linkage and PWM control (not in v1.2 controller scope)
- **Per-gun PWM electronics or signal conditioning:** Future extension; current design applies fixed full-power triggers via raw 2S bus
- **UV/blacklight torch:** Belongs to cosplay subsystem; initially use complete USB-powered UV flashlight/module with own driver
- **Wrist-mounted gun enclosure:** Future extension for cosplay builds
- **Cosplay-prop enclosure:** Future extension; not blocking core platform
- **True non-spill fluid quick-disconnect:** Premium CPC dry-break fittings deferred; baseline uses low-cost nylon barbs and silicone tubing semi-permanently installed

---

## Future Extensions

Once MVP validation confirms reliability and runtime, Joey intends to pursue (in sequence, not blocking release):

- **Piston-operated variable-power trigger:** Allows smooth modulation from low-idle (minimum solution consumption) to full-power show mode; requires potentiometer-linked mechanical trigger on donor gun and PWM control on main PCB
- **Wrist-mounted gun:** Invisible/discrete form factor for dancing; independent enclosure and mounting hardware
- **Cosplay-prop bubble gun:** Integrated into existing costume prop (Tracer-inspired); separate electrical enclosure and hose routing
- **Blacklight UV torch variant:** Dedicated UV LED (395–405 nm, 3 W) with independent on/off switch and focusing reflector; separate from pump trigger, custom gun adapter
- **16-head bubble totem:** Large multi-gun wand with its own antechamber and fluid pump (separate subsystem from core pack); uses both XT30 channels simultaneously
- **LED display integration:** Removable/detachable 64×64 RGB panel on backpack exterior; USB-powered via 5 V output; separate from bubble core; can be unmounted for venues that restrict electronic display
- **Decorative/rave accessories:** RGB lighting, music-reactive control, sound-triggered bubble firing (all future add-ons; not part of core platform)
- **2S6P high-capacity cartridge:** Extended endurance variant (108 Wh, ground travel only; exceeds airline limits) as drop-in replacement for 2S5P cartridge; uses same connector/interface

---

## Design Philosophy

**"Simple and clean beats messy and expensive."**

The platform prioritizes:

1. **Minimal component count:** Eliminated distribution blocks, redundant fuses, specialized connectors, cable glands, premium heat-sink hardware, and pre-made hardware where 3D printing or existing stock suffices
2. **Off-the-shelf solutions:** SZHJW USB-C boost charger module as a proven, replaceable design rather than integrating into controller PCB; peristaltic pump as single shared unit rather than per-head modules
3. **Over-specification in final design:** Once a part is chosen, it is fully documented (model number, voltage, current, pinout, mounting); no ambiguity at build time
4. **Modularity without hypotheticals:** Design for measured requirements (two guns, 1 L solution, 90 Wh battery, four-foot hoses) and proven components only; defer UV lighting, decorative LEDs, and 16-head wands until after MVP validation
5. **Field recoverability:** Single main breaker allows unplug-and-reset recovery if one gun shorts; no specialized tools required beyond standard electronics tools (soldering iron, wire cutters, voltmeter)
6. **Permissive tolerances:** Donor guns are uncharacterized toys; controllers and enclosures designed to adapt post-measurement, not predict CAD from vendor photos

---

## Commissioning Checklist

The measurements and checks that turn a fresh build into a tuned one:

1. **PCB acceptance:** Run the bring-up procedure on each assembled BubbleLink CTRL v1.2 board before it goes into the sled.
2. **Inline wattmeter test (high priority):** Measure exact Wh/L figure for one complete 118.4 mL canister firing with the existing three-head baseline gun at 2S 7.2–8.4 V. This will confirm whether 2.7–3.0 L or better is achievable.
3. **Bladder outlet adapter sourcing:** Measure actual outlet hose ID and barb OD on the delivered 1 L UWWWMM hydration bladder. Buy or 3D-print one reducer adapting bladder hose to the 3.5×5.5 mm system tubing.
4. **MAX LED backpack physical fit verification:** Measure the bag's interior. Confirm the stick (about 99.6 × 77.8 × 220 mm) stands beside the 1 L bladder.
5. **Donor gun selection:** Strip a batch of toy bubble guns for heads. Pick 4 matched heads for the two dual-head guns and keep spares. Measure current draw and bubble output, and take the teardown measurements the gun/head mounts need.
6. **Recirculation restrictor calibration:** After system assembly, set the bypass slide clamp to the 0.2–0.5 psi target and wet-test that its self-locking ramp holds.
7. **Printed parts:** Print the fit coupon, cell holders and slide clamps, then the stick and umbilical bricks. Wet-test the cap seal, and check charger and BMS temperatures on the first enclosed charge (charge with the cap off until then).
8. **Field trial plan:** Establish a baseline performance run with the two dual-head guns in the completed 2S5P BubbleLink pack before the first event (the existing three-head gun remains the performance reference). Measure runtime, solution consumption, pump on-time, and thermal behavior at the target duty cycle (~37% event usage).

---

**Document revision:** 2026-10-14  
**Authoritative source:** [docs/bom.md](bom.md) and the BubbleLink CTRL v1.2 release package.
