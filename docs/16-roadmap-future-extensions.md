# BubbleLink v1 roadmap: Future extensions and planned directions

This document describes the intended future directions beyond the current MVP build—clearly labeled as not built, not ordered, and not scheduled for completion before the target festival 2026-10-30. The roadmap follows the established v1 architecture and design philosophy but reserves complexity for later iterations.

## Build sequence and phase structure

The v1 MVP follows a measured development path:

1. **Phase 1: Basic rig.** Single existing three-head gun, pack control, one umbilical, 1 L reservoir + 90 Wh battery, no fancy extras.
2. **Phase 2: Fluid and power proof.** Verify GROTHEN G528 pump performance at actual solution viscosity. Measure battery thermal behavior under sustained eight-head equivalent load. Establish pump pressure setpoint and recirculation restrictor calibration.
3. **Phase 3: Donor characterization.** Test retail donor cohort (rocket-style 10-hole, windmill, large-bubble) against selection criteria. Measure bubbles-per-watt, throw in still air, reliability over 10+ consecutive bursts, motor noise, internal temperature, fluid tolerance (thick vs. thin solution).
4. **Phase 4: Add-on options.** Build wrist emitter, UV torch, or cosplay integration as side projects without redesigning the core pack.
5. **Phase 5 (future): Larger battery if justified.** Field experience at the target festival and other events will determine whether the 180 Wh cartridge justifies the extra weight for normal use.

---

## Extended battery cartridge (2S10P, 180 Wh)

**Intended purpose:** Ground-travel-only long-day events with midday solution refill.

**Specifications:**
- Configuration: 2S10P (20 cells, two ten-cell parallel groups)
- Cells: Samsung INR18650-25R, 2,500 mAh each (same qualification as 90 Wh)
- Nominal: 7.2 V, 25 Ah, 180 Wh
- Voltage range: 6.0 V (discharge cutoff) to 8.4 V (full charge)
- Discharge capacity: ≈2.37 L solution at measured baseline (2× the standard cartridge)
- Charge current: 2 A (0.2 A per cell), safe for Samsung 25R standard 1.25 A charging spec
- Charge time: ~14–16 hours from cutoff at 2 A
- Connector: Identical XT60H output as 90 Wh (same rail, no redesign needed)
- BMS: Identical 2S 30–40 A balancing model as 90 Wh (reusable charger circuit)
- Balance/service connector: JST-XH 3-pin, identical interface
- Mechanical mounting: Same slide-rail and latch datum as 90 Wh (swap, don't parallel)

**Usage intent:** One liter in afternoon → water-station refill (100 mL concentrate + 900 mL water) → second liter through evening. Never paralleled with 90 Wh cartridge in operation; installed one-at-a-time.

**Field carry:** 100 mL of 9:1 concentrate in HDPE pod, refillable from venue water station or personal hydration supply. No separate battery combiner or dual-pack hardware; cartridge is swapped at workshop, not in field.

**Travel restriction:** Exceeds 100 Wh FAA limit; ground transport only. Do not bring on aircraft as checked or carry-on baggage without explicit airline pre-approval.

---

## Enclosed swappable battery cartridge (XT60 output interface)

**Intended refinement:** Permanent labeled case around the 90 Wh and 180 Wh cell stacks.

**Specifications:**
- Output connector: XT60H-rated 30 A continuous (female receptacle, energized pack side)
- Balance/service: JST-XH 3-pin keyed connector, protected by cap when not charging
- Labels: Permanently marked with (a) BubbleLink version ID, (b) cell count and configuration (2S5P/90 Wh or 2S10P/180 Wh), (c) nominal voltage, (d) capacity in Ah and Wh, (e) manufacture date, (f) weight with case
- Rigidity: 3D-printed PETG outer shell, interior film-insulated cell groups; no loose internal motion
- Mounting: Slide-rail interface on running vest; quick-swap without plumbing or electrical disconnect of umbilicals or fluid lines (battery cartridge slides in/out independently)
- Service access: Two cells in series can be bypassed individually if one fails (via JST-XH jumper-pair swaps at workshop only)

**Purpose:** Allows swapping cartridges in the field for longer events without opening the cell assembly or risking exposed 18650 cells. Labeled case prevents accidental mixing of 90 Wh and 180 Wh packs and enforces travel-only compliance for the 180 Wh unit.

---

## Master disconnect (XT60 loop key with pull handle)

**Intended purpose:** Emergency power cutoff, safely accessible under pack straps while wearable.

**Specifications:**
- Type: XT60H shorted connector plug on 1–2 cm solid handle (3D-printed TPU or cast resin)
- Placement: Mounted on side-accessible location of pack, reachable by touch without removing pack
- Function: Breaks all power to gun channels, pump, and USB output; does NOT affect charging circuit (allows battery-side charging even with key removed)
- Polarity: Keyed as XT60H female receptacle → shorted XT60H male plug

**Operation:** Pull handle vertically to break circuit; reinsert to restore. No tools required. Provides mechanical emergency stop without relying on digital control or thermal breaker response time.

---

## Invisible wrist emitter

**Intended purpose:** One-head continuous-operation bubble wand worn on wrist, independent from pack orientation.

**Specifications:**
- Donor mechanism: <100 g single-head retail pump-gun (wind-up, small rocket, or compact fan)
- Wrist mounting: Elastic strap or silicone cuff, neoprene or silicone TPU liner to prevent chafing
- Fluid line: Routed under sleeve, small-diameter (2–3 mm ID) silicone tube, tethered to pack via main umbilical
- Control: Palm or thumb-accessible trigger on gun handle; local momentary switch (no pack signal required)
- Electrical: Direct XT30 connection to pack channel (either independently or via second-gun XT30 pair)
- MOSFET/flyback: Local gate driver if PWM control desired; on/off-only acceptable for v1
- Fan guard: Printed shroud over intake to prevent hair/lint occlusion
- Power budget: ≤10 W continuous; uses dedicated XT30 channel

**Development path:** Start with existing small retail donor + armband. Measure current draw and solution consumption. Iterate shroud geometry and strap comfort without redesigning core pack.

---

## Cosplay cartridge (removable sled, no reservoir)

**Intended purpose:** Integrate bubbles into Tracer (Overwatch) or similar prop costume without adding bulk pack to the prop itself.

**Specifications:**
- Donor mounting: Removable 30 × 20 mm M3 sled, mechanically identical to standard pack-side sleds (allows quick swap between bubble-on and bubble-off costumes)
- Intake: Unobstructed pump inlet port on sled face (no tubing routed through costume interior)
- Service access: Removable side panel or hatch for pump priming, nozzle cleaning, or manual solution feed
- Drainage: Slotted lower edge or small drain grommet to expel residual liquid after event
- Reservoir: None (solution supplied via umbilical from pack; costume receives primed line only)
- Weight: Mounted sled + local pump/motor only (~50–80 g); no bladder or battery in costume
- Example: Tracer's dual-gun hand mounts become simple hollow printed shells with pump inlets routed back to pack

**Expected build:** Two hollow printed gun/turret shells, sled mounting brackets, local wetting manifolds matching donor pump geometry. No changes to core pack or 90 Wh cartridge; costume is a head variant only.

---

## Blacklight torch or wand

**Intended purpose:** Independent 395–405 nm UV emitter for complementary visual effect alongside bubble output, deployable as handheld wand or fixed accessory.

**Specifications:**
- LED: 395–405 nm (purple-appearing blacklight), 3 W power nominal on aluminum substrate or star mount
- Driver: 700 mA constant-current PWM-capable driver (PT4115-class or equivalent)
- Power supply: Dedicated regulated 5 V from pack USB rail (independent of gun channels)
- Switch: Separate on/off toggle or momentary button (NOT modulated with bubble gun trigger)
- Heat management: Aluminum heat spreader (25 × 25 mm minimum), thermally bonded to LED backside; passive convection adequate for <5 second bursts, active cooling (fan or gel) optional for sustained use
- Mounting: 30 × 20 mm sled interface (reuses standard donor sled pattern) or hand-held wand body
- Waveform: Verified to excite common fluorescent dye (fluorescein, optical brightener, etc.) without UV-C skin hazard

**Development notes:** Start with 3 W fixed-brightness mounted on sled. Measure actual output with lux meter and UV radiometer. Test with various fluorescent dyes in bubble solution to optimize visual effect. Limit to 4–5 W system budget to avoid draining 90 Wh pack faster than primary bubbles.

---

## Progressive trigger (Hall-effect plunger with PWM output)

**Intended purpose:** Variable-power bubble output responsive to trigger plunger travel, enabling real-time control without on/off chatter.

**Specifications:**
- Mechanical: Spring-return plunger bore (18–25 mm diameter, 18–25 mm travel), hardened PETG or nylon housing
- Sensor: Neodymium magnet (5 × 3 mm) embedded in plunger; SS49E-class analog Hall sensor affixed beside bore bore (linear output 0–5 V proportional to magnet distance)
- Electrical: Hall sensor output → voltage divider → analog input to PWM controller (either remote potentiometer board or microcontroller)
- PWM generation: Local to gun, 15–20 kHz switching frequency, gate-driven MOSFET (no direct microcontroller pin drive)
- Gate driver: TC4420A-class high-current gate driver if MOSFET switching frequency >4 kHz
- Minimum duty: Configured floor to prevent stalling at low trigger position; calibrated per donor pump (typically 20–40%)
- Maximum duty: Hard-capped ceiling to prevent thermal runaway; typically 100% for initial testing, derated based on measured junction temperature
- Startup kick: Optional 100–200 ms pulse at configured minimum duty if donor stalls without initial boost; configurable or switchable off if not needed

**Development path:** Build with commercial remote potentiometer PWM controller (6–30 V, 15 A) and linear slide pot on workbench first. Measure actual plunger displacement vs. output wattage and bubbles-per-second. Once geometry proven, redesign into final Hall-effect plunger and gate-driver PCB.

---

## Six-head stick expansion (two three-head cartridges)

**Intended purpose:** Unidirectional bubble output from a single handheld wand, useful for large static scenes (backstage, stage prop, stationary installation).

**Specifications:**
- Architecture: Two independent three-head donor cartridges, one per existing pack channel
- Mounting: Printed aluminum or PETG stick frame, ~0.5–1 m total length, cartridges angled or aligned as desired
- Power: Dual XT30 connectors (Channel A and B from pack) feeding split umbilical into each cartridge's fluid/electrical manifold
- Fluid: Single 1 L reservoir at pack can supply both cartridges via Y splitter (total demand ~34 mL/min at full three-head equivalent per channel)
- Redundancy: Cartridge A failure does not disable Cartridge B (independent fuses at 15 A each)
- Runtime: ~1.47 hours at heavy 37% duty with single liter (split between two channels)

**Expected hardware:**
- Printed sled interface adapters (two copies of standard 30 × 20 mm M3)
- Printed alignment frame or aluminum tubing jig
- Extended 6–8 foot umbilicals to accommodate stick length
- Two parallel donation cartridges (existing guns or new builds)

**Not part of v1:** Design is future-only; v1 focuses on dual-channel handheld guns operated independently. Six-head stick becomes viable once field experience confirms donor reliability and baseline performance is locked.

---

## Bubble Miku costume (passive or fallback option)

**Intended purpose:** Wearable costume prop fallback if fluid system fails during event; allows full costume performance without active bubble output.

**Specifications:**
- Base costume: 3D-printed components or fabric bodysuit matching Vocaloid Miku aesthetic
- Passive operation: Costume operates as-is without bubble emission; LED accents and movement provide visual spectacle independent of fluid
- Bubble mounts: Optional threaded or quick-mount points for cosmetic bubble-head shells (non-functional but visually realistic; can be retrofitted with actual pumps later)
- Fallback scenario: If pack fails, costume remains wearable and photogenic without needing rapid repair
- Integration: Not integrated into wearable pack system; completely separate costume project

**Status:** Mentioned as future possibility; not actively designed or scheduled.

---

## Sixteen-head totem (separate power, surge chamber, larger pump)

**Intended purpose:** Permanent or semi-permanent installation (stage, installation art, large venue) with unified control and distributed bubble output.

**Specifications:**
- Power: Separate 2S or 3S battery (not tethered to wearable pack); 4S possible for higher voltage head tolerance
- Pump: Kamoer KPK200 or TOPSFLO TF30B-A (much higher flow capacity than NKP; 150–200 mL/min or greater) to supply 16 heads simultaneously
- Surge chamber: 50–100 mL silicone bulb on pump outlet to dampen pressure spikes and reduce on/off cycling
- Manifold: Large-bore distribution tree (6–8 mm trunk splitting to 16 independent 3.2 mm output lines)
- Head arrangement: Four columns of four heads each, mounted in printed radial or grid array on vertical post or frame
- Firmware: Optional ESP32-class microcontroller with network-synchronized output (BPM detection, music-reactive patterns, or simple timer-based cycles) if visual coordination desired
- Fluid: High-flow bubble concentrate (commercial machine mix or custom formulation) at 1–2 W per head, ~16 W total for heads + pump overhead
- Electrical control: Simple momentary on/off or fully programmable triggering

**Not part of v1:** Requires separate battery, pump upgrade, and enclosure design. Reserved as future expansion after core pack platform proven. No PCB changes to wearable pack; totem is a standalone system that can be tested independently.

---

## Optional LED display module (64×64 P3.75)

**Intended purpose:** Removable backpack-mounted RGB pixel display for visual coordination with bubble output or independent light show.

**Specifications:**
- Resolution: 64 × 64 pixels, 3.75 mm pitch (P3.75)
- Size: 25 × 25 cm face
- Power: 5 V digital logic, estimated 2–3 W average (4 W absolute ceiling with 90 Wh pack)
- Input: Bluetooth app-based control (no firmware required; vendor provides Android/iOS app)
- Programs: Text, animations, GIFs, still images via app
- Mounting: Removable outer skin on pack using laser-cut polycarbonate backing + TPU isolation tabs, hook-and-loop attachment
- Ventilation: 10–15 mm air gap between display and pack fabric to prevent thermal issues
- Removal: Takes <2 minutes; allows display-off operation for daytime events or venue compliance

**Development notes:** Panel is optional luxury add-on. Do NOT design display integration into core pack architecture. Mount as independent module that can be swapped on/off without affecting bubble system. Requires separate USB power bank initially; integration with main pack USB rail feasible after v1 field-proven and power budget verified.

---

## True non-spill fluid quick-disconnect (CPC NS1 upgrade)

**Intended purpose:** Premium dry-break fluid coupling to eliminate spillage and minimize fluid loss during head swaps in field.

**Specifications:**
- Type: CPC NS1D170212 valved body + NS1D220212 valved insert (or equivalent dual check-valve design)
- Ratings: Vacuum-rated (allows siphon-proof closed system); 15 psi working pressure (safe for 0.2–0.5 psi pack header)
- Tubing: 1/8-inch (3.2 mm) barbed or push-to-connect
- Operation: Mate two bodies → dual check valves open simultaneously; separate one → both check valves close automatically → minimal drip
- Cost: ~$40–60 per pair; optional upgrade after v1 baseline with nylon car-hose connectors

**Development path:** v1 uses the black nylon car-hose connector assortment (tees, unions, reducers) with field-acceptable spillage tolerance. If later field use proves frequent head swaps or solution spillage is problematic, retrofit both pack output tees with CPC NS1 couplers. Fluid lines and pump interface remain unchanged; only swap the tee connector bodies.

---

## Coulomb-counting fuel gauge with OLED display (future power monitoring)

**Intended purpose:** Accurate battery state-of-charge readout accounting for discharge curve and temperature effects.

**Specifications:**
- Hardware: TI INA228 or BQ34Z100-R2 fuel gauge IC (coulomb accumulation + voltage model)
- Display: 128×64 monochrome OLED, I²C interface, mounted on pack face
- Inputs: Battery voltage, pack current (via existing 5 mΩ shunt), battery temperature (NTC on cell body)
- Output: % state-of-charge, mAh remaining, estimated runtime to 3.0 V per cell (cutoff), accumulated Wh consumed
- Microcontroller: ATtiny or XIAO-class, runs independently from pack main control
- Refresh: Update every 1–2 seconds or on-demand (momentary button if power-saving preferred)

**Not part of v1:** Requires battery characterization curve and firmware development. Simple voltmeter (0–30 V digital panel display) sufficient for MVP. Fuel gauge added only after v1 proves 90 Wh capacity in real-world field use; enables long-day planning with higher confidence.

---

## Fluid-recipe experimental matrix

**Intended purpose:** Characterize solution performance vs. donor pump efficiency and reliability.

**Test matrix:**

| Recipe | Water | Concentrate | J-Lube (g) | Glycerin (mL) | Notes |
|---|---|---|---|---|---|
| Commercial baseline | 900 mL | 100 mL (9:1 Lulu) | 0 | 0 | Reference; proven in bubble machines; low viscosity |
| Commercial alt | 900 mL | 100 mL (10:1 JOYIN) | 0 | 0 | Verify consistency with existing concentrate |
| Stream pool 1 | 1000 mL | 50–70 mL Dawn Professional | 0 | 0 | Outdoor base without polymer |
| Stream pool 2 | 1000 mL | 50–70 mL Dawn Professional | 0.05 g | 0 | Low-polymer variant |
| Stream pool 3 | 1000 mL | 50–70 mL Dawn Professional | 0.10 g | 0 | Medium polymer (PEO thickening) |
| Stream pool 4 | 1000 mL | 50–70 mL Dawn Professional | 0.20 g | 0 | High polymer (larger bubbles, slower fail) |
| Stream pool 5 | 1000 mL | 50–70 mL Dawn Professional | 0.10 g | 5 mL | Polymer + light glycerin |
| Stream pool 6 | 1000 mL | 50–70 mL Dawn Professional | 0.10 g | 10 mL | Polymer + moderate glycerin |

**Measurement per recipe:**
- Pump current draw at pack header
- Flow rate (mL/min at pack-side outlet, no gun attached)
- Bubble count in still air (slow-motion video, 1-second sample)
- Failed film count (% of wetting cycles that don't produce bubble)
- Throw distance (horizontal in calm indoor space)
- Residue on pump tubing (visual inspection post-test, 24 hour soak in distilled water)
- Cleanup time (time to rinse tubing, manifold, reservoir until clear)

**Schedule:** Baseline commercial reference in field use at the target festival. Stream matrix testing during winter off-season (January–March 2027) with data review for summer event planning.

---

## Donor test cohort and selection criteria

**Intended purpose:** Establish measured baseline of available retail donor mechanisms rather than settling on first option.

**Test cohort:**
- Rocket-style 10-hole automatic (high-sales reference model, ~$2–5 retail)
- Rocket-style 10-hole from alternate seller (verify cross-vendor consistency)
- Windmill or fairy-wand compact generator (low weight, unknown flow)
- Large-bubble 3-AA donor (visual variety, lower frequency, possible lower efficiency)

**Measurement per donor:**
- Operating voltage range (minimum/nominal/maximum without stall)
- Peak motor current at nominal voltage
- Minimum usable motor current (below which performance drops)
- Solution consumption rate (mL/min at various throttle settings or fixed voltage)
- Bubble production (count per second from video)
- Throw distance (still air)
- Noise level (dB @ 50 cm)
- Internal temperature after 5-minute continuous operation
- Pump type (gear, screw, peristaltic, other)
- Wetting ring or nozzle geometry (critical for bubble size/count)

**A/B experiment:** If feasible, compare stock 5015 blower with converging shroud retrofit vs. standard fountain-style pump. Measure if shroud improves bubble output or reliability.

**Acceptance criteria:**
- Donor must exceed stock baseline (existing three-head gun at 16.9 mL/min fluid, 70 W equivalent power) OR
- Donor must sustain stock peak power for 50% longer duration OR
- Donor must exhibit repeatable turbo across 10+ consecutive trigger bursts (no intermittent failure, no current/temperature drift)

**Ownership:** After testing, select two primary donors for field use (one per channel in standard pack). Mark with profile cards identifying class, voltage ceiling, PWM range, measured flow and current. Keep remaining test units as spares.

---

## Up-to-eight-head system expansion (post-v1 investigation)

**Intended purpose:** Explore technical feasibility of four heads per channel instead of three.

**Specifications:**
- Channel architecture: Dual 12 A continuous per channel (two XT30 in parallel or single XT60 rated 30 A total)
- Per-head power budget: 12 A / 4 heads = 3 A per head at 8.4 V nominal → ~25 W per head
- Pump flow: ~48–64 mL/min total (8 heads × ~6–8 mL/min per head); Kamoer NKP adequate at lower margin
- Feasibility unknowns: (a) Whether individual toy pumps can operate reliably in series-parallel combination; (b) Wetting manifold design for eight independent hole sets; (c) Bubble count consistency across all eight heads at same time

**Development path:** Not pursued for v1. After field experience with six-head (two three-head cartridges), measure actual per-head power draw and reliability. If reliability proven and power budget allows, design eight-head stick cartridge with custom printed manifold distributing from single pack header line.

---

## Optional potentiometer speed control (handheld trigger variant)

**Intended purpose:** Continuous variable motor voltage control via handheld trigger potentiometer without digital PWM complexity.

**Specifications:**
- Potentiometer: Linear slide pot or rotary dial (10–100 kΩ), ±10% linearity acceptable
- Control circuit: Simple Zener + pass-MOSFET or linear LDO regulator (no PWM, no microcontroller)
- Output range: 0–100% of supply voltage via voltage divider / feedback network
- Mounting: Hand-accessible on trigger guard or wrist cuff
- Power budget: <1 W continuous (dissipated in pass device or regulator)

**Status:** Not part of v1. Explored as optional enhancement for future handheld designs. Current v1 uses fixed-current or PWM per channel; potentiometer adds mechanical complexity without clear v1 gain.

---

## LED and UV lighting accessories (secondary integration)

**Intended purpose:** Coordinate lighting effects with bubble output for visual spectacle.

**Options explored (not active):**
- Body-wide RGB LEDs (e.g., APA102 strips on pack or costume)
- Fixed 365 nm or 395 nm UV accent lights (complementary to blacklight torch)
- Strobe or chase patterns triggered by bubble volume detection

**Status:** Deferred to v2+. v1 focuses on core bubble system. LED panel (optional 64×64 RGB) can be retrofitted independently; no pack redesign required.

---

## Explicitly out of scope for v1

The following features are **not** designed into v1 and will not be pursued before the target festival 2026-10-30:

- **Body-wide RGB lighting** controlled by pack firmware or music synchronization
- **BPM detection** and music-reactive bubble output modulation
- **Music-reactive firmware** with beat detection and synchronized pump/head control
- **Completed 16-head totem** ready for field deployment (concept only; development reserved for 2027)
- **Proprietary hybrid connectors** combining electrical and fluid (power, complexity, non-repair; standard parts acceptable instead)
- **Guaranteed universal donor compatibility** across unmeasured donor designs (test cohort approach instead; document per-donor limits on profile cards)
- **Integrated fuel gauge** with OLED display and coulomb counting (panel voltmeter sufficient for MVP)
- **Premium CPC NS1 dry-break couplings** on first build (nylon car-hose connectors acceptable; upgrade path available)

---

## Summary and completion timeline

**Completed/in progress (by 2026-10-29):**
- v1 MVP: two-channel 90 Wh wearable pack with GROTHEN G528 pump, 1 L bladder, existing three-head donor, two standard umbilicals
- Initial donor characterization (test cohort measured vs. selection criteria)
- Basic progressive trigger (potentiometer + PWM controller prototype)

**Planned after the target festival (winter 2026–2027):**
- 2S10P 180 Wh cartridge build and field validation
- Enclosed swappable battery cartridge with XT60 interface
- Master disconnect loop key integration
- Wrist emitter and UV torch builds (parallel side projects)
- Cosplay cartridge variant (Tracer costume integration)
- Progressive Hall-effect trigger redesign and bench testing
- Fluid recipe experimental matrix (stream solutions)
- Donor test cohort expansion and A/B blower experiment

**Deferred to 2027 or later:**
- Six-head stick cartridge
- Sixteen-head totem with optional firmware
- Bubble Miku costume
- Coulomb-counting fuel gauge with OLED
- CPC NS1 premium coupler retrofit
- Eight-head channel upgrade feasibility study
- Body-wide RGB and music-reactive control systems

All extensions maintain v1 core architecture (two-channel 2S raw bus, nylon car-hose fitting field interface, 30 × 20 mm sled standard, pack-side current detection). No redesigns to wearable core required for any listed future item.
