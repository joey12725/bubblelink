# Design Decisions

This document records every final design choice in BubbleLink, organized by domain. For each decision: the final state (one line), the rationale with numbers and sources, and implications for building and field use. All decisions are drawn from FACTS.md (canonical authority), ORDER_LEDGER.md (purchased parts), the v1.2 PCB release package, and the design threads dated 2026-08 to 2026-10.

---

## Architecture

**Decision:** Pack-fed, two-channel modular system with one shared transfer pump.

**Why:** Joey's existing 2S1P gun proved the concept (a summer festival 2026-08-02, a convention 2026-09-04 to 06): 473.6 mL solution in ~75 min at 37% duty, ~26 W average, ~0.069 Wh/mL. The 2S5P pack has five times the baseline's energy (90 Wh vs 18 Wh). At ~0.069 Wh/mL that's roughly 1.2–1.3 L of solution for one EGU-class gun, which matches the 1 L reservoir (1 L budgets 71–74 Wh including pump assistance). Two independent XT30U channels allow flexible head deployment: one gun per channel, or both channels feeding one large wand. A single GROTHEN G528 at 150 mL/min nominal is ~9× one baseline gun's 16.9 mL/min continuous demand (~4.4× for two).

**Implications:** Both channels share supply pressure and response time. Umbilicals are semi-permanent (XT30U remains the disconnect). Donors are test hardware, not a frozen design.

---

**Decision:** Existing overvolted three-head gun is the performance reference and first donor conversion candidate, not a completed prototype.

**Why:** The gun taught design lessons (bad spring contacts generate 3–6.4 W heat, drop 0.4–0.8 V). A properly welded 2S5P pack will remove that artifact and may increase motor current. The baseline measurements (70 W inferred, ~15 min full-trigger life, ~26 W average sustained) establish the energy budget.

**Implications:** No identical prototype exists. First build is the deployment unit. Donors are characterized post-assembly (current draw, flow rate, bubble quality).

---

**Decision:** One 1 L removable hydration bladder, food-grade silicone tubing, one shared pump, printed slide clamps per channel (no purchased shutoff valves).

**Why:** The 1 L capacity provides ~2 h 38 min at 37% duty (heavy dancing) and fits the pack. The G528 at 150 mL/min idles at ~23% capacity with two heads, leaving headroom for thicker solution or future adds. A recirculating bypass with a low-cracking check valve (0.003 MPa opening) prevents siphoning and force-feeding stopped donors. Printed clamps eliminate purchased shutoff hardware.

**Implications:** Fluid is the system bottleneck, not energy. Operator must plan refill stations or carry backup concentrate. Bypass restrictor is calibrated post-assembly to target 120–150% donor demand.

---

## Power & Battery

**Decision:** 2S5P Samsung INR18650-25R: 10 cells, 7.2 V nominal, 8.4 V full, 12.5 Ah, ~90 Wh.

**Why:** At measured peak ~70 W (inferred from energy budget), the 2S5P pack supports two times the 18 Wh original. Five parallel cells reduce per-cell current: at 26 A total (eight heads + pump), each cell carries only 26 ÷ 5 = 5.2 A. Resistive heating per cell drops to 5.2² × 0.022 Ω ≈ 0.59 W (vs. the original gun's uncomfortable heat from poor contacts). The 90 Wh total is below the FAA 100 Wh threshold for airline carry-on.

**Implications:** Cells must be matched (capacity and internal resistance) before spot-welding. Five parallel series bridges distribute main current (no single tab carries full output). The printed cell holders (original 5×2 offset design, MID and TERM, 19.9 mm pitch; they replace the Cults3D spacer remix) accommodate 18.33 ± 0.07 mm diameter, 64.85 ± 0.15 mm height tolerance. The two rows face opposite directions (row A + one way, row B − that way); if every cell faces the same way, it's 10P, not 2S5P.

---

**Decision:** Spot-welded nickel-plated steel interconnects (2.6 cm tabs, not pure nickel; five parallel series bridges, two tabs per bridge for redundancy, total 30 tabs ordered).

**Why:** Eliminates solder joints and spring contacts that dissipate 3–6 W at 10 A and drop 0.4–0.8 V. Spot-welded tabs have ~1/10 the resistance. The five parallel bridges mean no single weld failure disables the pack.

**Implications:** Requires access to a spot welder (shared shop equipment). Build sequence: solder four series connections per string, then weld parallel bridges. Inspect every weld visually.

---

**Decision:** IC GOGOGO 2S 8.4 V 40 A Li-ion BMS (not LiFePO₄) with balance and temperature sensing.

**Why:** The 40 A rating provides startup margin; sustained max is ~26 A. Li-ion (not LiFePO₄) matches cell chemistry. Balance prevents divergence over cycles. Temperature cutoff at 55–60°C discharge, reset at 45°C, prevents thermal runaway under extreme loads.

**Implications:** Confirm delivered board is Li-ion 8.4 V variant on unboxing—the listing offers both types. BMS stands on edge in a slot along the stick's back wall, next to the battery's TERM face (measured 2½ × 1⅞ × ¼ in).

---

**Decision:** SZHJW USB-C 2S boost charger, 2S 4A variant, charges battery-side (not through main circuit).

**Why:** Battery-side charging avoids the 30 A breaker and main connectors, reducing short-circuit fire risk. The 4A rate and 8.4 V output suit the 2S5P.

**Implications:** Electrical work requires unplugging both XT60 battery and USB-C input. Charger is always available; no firmware or special modes required.

---

**Decision:** Single 30 A manual-reset breaker (YONGRUN Type B-30A, M6 threaded studs), wired at battery output immediately after BMS.

**Why:** The 30 A rating equals system continuous max (26 A guns + pump + margin). Manual reset requires deliberate recovery, preventing accidental re-closure into a persistent short. No per-channel fuses; XT30U connectors (15 A rating) and 16 AWG wire (20 A rated) are secondary barriers.

**Implications:** A gun short trips the main breaker immediately. Press reset after fixing the fault. No fuses to carry or replace in field. The breaker is in the + line only. Measured 2026-10-14: 1⅝ in square plate, 4 in (102 mm) long, 1⅝ in thick (the listing's 72 × 48 × 44 mm was wrong). It's an inline type with a red reset lever and a red push-to-trip button on its square plate. It stands upright behind the sled's cross panel, controls 2 mm behind a 34 × 40 mm window in the right wall covered by a glued TPU membrane, so you can trip or reset it through the wall. The trip button is the stick's OFF switch.

---

**Decision:** SC10-6 copper ring lugs on breaker studs (solder-filled, strain-relieved); never solder wire directly to studs.

**Why:** The M6 studs have 10 mm² barrel, oversized for 12 AWG wire (2.07 mm² nominal). A solder-filled crimp spreads contact area and prevents micro-motion cracking under vibration.

**Implications:** Lug preparation is non-optional. Solder barrel full, apply heatshrink, crimp wire through barrel again for redundancy.

---

**Decision:** 12 AWG silicone wire (black and red, 3 m each) for battery-to-breaker-to-split main harness.

**Why:** 12 AWG is rated ~40 A continuous, safe for 26–30 A load. Silicone insulation tolerates damp pack environment and flexing. 3 m covers path with spares.

**Implications:** All soldering must be robust. Crimps are not used; all connections are solder + heatshrink. Main harness is highest-current path; plan enclosure layout accordingly.

---

**Decision:** 16 AWG silicone wire (black and red, 5 m each) for gun channels and four-foot umbilicals.

**Why:** 16 AWG is rated ~13 A continuous; each XT30U channel fuses at 15 A (connector rating). Voltage drop over 4 feet at 15 A is ~0.48 V (acceptable). 5 m provides spares and covers four-foot gun leads.

**Implications:** Channel wiring is secondary protection layer. XT30 connector soldering is critical—poor joints are the primary field failure mode.

---

**Decision:** 5 V supply from two independent YxPC 6–20 V USB bucks: Buck A (pump and PCB), Buck B (LED backpack).

**Why:** Decoupling prevents pump noise or LED transients from resetting the MCU. The YxPC modules have no defensible spec; both are provisional. If Buck A misbehaves, Pololu S13V30F5 is the external replacement (no PCB change).

**Implications:** Measure each buck's output under load (PCB max input 5.25 V). Configure Buck A to ~5.0 V via trim pot before connecting pump. Solder both outputs directly (Buck A → PCB J1; Buck B → a cut USB cable to the backpack); there's no room for USB plugs inside the stick.

---

**Decision:** ACS758LCB-050B current sensor (5 V supply, 40 mV/A, ±50 A) measures combined gun current at the split point after the 30 A breaker.

**Why:** A single high-side sensor captures both channels. At 50 A range and 40 mV/A, a 1 A gun produces ~40 mV on signal pin; at 2.5 V zero-offset, this is healthy margin above noise. Only 3-wire signal (5 V, GND, OUT) goes to PCB; main 12 AWG harness and sensor's high-current conductor handle all power.

**Implications:** Gun current never passes through PCB. Low-speed or PWM heads may fall below detection threshold; J4 fallback (DNP, no-respin override) provides override if needed.

---

**Decision:** Stlxy DC 4–100 V two-wire LED voltmeter (red, 5 ordered; 1 used, 4 spares) as battery gauge.

**Why:** Two-wire passive display shows battery state without firmware. No percentage fuel gauge; operator reads voltage and estimates runtime from experience. 4–100 V range covers 2S (2.8 V min to 8.4 V max).

**Implications:** A 7 V reading with full fluid suggests ~5 min firing left; below 5 V, gun loses output. Spares prevent broken display from blocking deployment. Wire it after the breaker so tripping the breaker turns it off. Its idle draw is unmeasured (small LED meters typically draw tens of mA); measure it once, and unplug the XT60H loop for storage.

---

**Decision:** Master disconnect is XT60 battery plug or removable XT60 loop key.

**Why:** XT60 is RC-standard, rated 60 A, provides secure break of main power. A loop key (short XT60 jumper) prevents accidental reconnection and provides pull handle for safe field swaps.

**Implications:** Electrical work requires unplugging battery XT60 and USB-C input. The XT60H loop runs out through the bulkhead grommet and the cup's floor; open the bag to pull it. It's the full battery disconnect, for storage. Everyday OFF is the breaker's trip button, pressed through the membrane in the stick's right wall. The BMS stays on the battery either way (quiescent draw unmeasured, typically tiny).

---

## Protection

**Decision:** Single 30 A manual-reset breaker, no per-channel fuses or breakers.

**Why:** System continuous max is ~26 A (eight heads + pump). The single breaker at main output protects entire tree. XT30U connectors (15 A rating) and 16 AWG wire (20 A rated) are secondary barriers. No per-channel protection adds weight and cost with minimal benefit; toy-gun faults rarely exceed 15–18 A.

**Implications:** A gun short trips main breaker; operator unplugs both guns, waits, resets breaker, and reconnects one gun at a time to identify fault.

---

**Decision:** F1 is a 1.5 A PTC self-resetting fuse on the PCB pump branch. No internal battery fuse.

**Why:** The 30 A breaker resets in field and protects the entire system. The 1.5 A PTC (F1, 1812L150/16DR) limits pump/PCB current independently if a short occurs on those branches.

**Implications:** In normal operation, internal fuse never opens. If it does, pack is inoperable until the stick is opened and fuse replaced (multi-minute field repair).

---

**Decision:** No per-channel PWM; guns run on raw 2S (~6.0–8.4 V).

**Why:** Full-power triggers only. Any motor control is external to pack (local PWM in gun or hand-held controller).

**Implications:** PWM speed control is future work; see docs/16-roadmap-future-extensions.md.

---

## Connectors & Wiring

**Decision:** XT60H (sheathed) for battery output, rated 60 A continuous.

**Why:** Battery output (~40 A peak, ~26 A sustained) is highest-current node. XT60H provides secure gold-plated contacts and protective sheath.

**Implications:** Battery output is XT60 male; pack/main harness is XT60 female. Removable loop key completes master disconnect.

---

**Decision:** XT30U (AMASS-style), 10 pairs, for gun channels; power and ground only (no signal wire).

**Why:** XT30U rated 15 A continuous, standard in RC/drone circles. Two pairs per pack (left and right). No signal wire simplifies umbilical to pure power + fluid.

**Implications:** Gun triggers and motor controls are fully local (mechanical switch or local PWM). Pack sees only motor current through power pins.

---

**Decision:** JST-XH (2.54 mm) for low-current internal connections (PCB, BMS balance, charger).

**Why:** Standard for 5 V logic and battery balance circuits. Pre-crimped connectors eliminate hand-crimping.

**Implications:** All PCB-to-external connections use JST-XH headers.

---

## Fluid System

**Decision:** UWWWMM 1 L blue hydration bladder with 101 cm detachable drinking tube (keep factory leakproof disconnect; cut tube short for use as fill spout).

**Why:** 1 L provides ~2 h 38 min runtime at 37% duty. Factory hose disconnect is leakproof and can be cut/re-sealed with barbed tee (no purchased shutoff needed). Wide-mouth fill allows easy refill and cleaning.

**Implications:** Fill through the bladder's wide mouth. The bladder feed enters the stick's cup through its floor. Drain and dry after every event; never store solution in bladder.

---

**Decision:** ONE GROTHEN G528 peristaltic pump: 6 V rated, 3×5 mm tube, 150 mL/min.

**Why:** Measured baseline 16.9 mL/min per gun; pump at 150 mL/min provides 2.2× margin. Single pump is half weight and cost vs. two. Peristaltic design eliminates impeller clogging.

**Implications:** Confirm on delivery motor is marked "6 V", not "12 V" (seller artwork differs), and bench-test it at <0.3 A at 5 V. Pump is permanent hardware; tube replacement only is user-serviceable. Measured 2 × 1¾ × 1½ in at its thickest (the earlier 60 × 60 × 50 / 65 × 55 × 50 mm figures were wrong); it sits in a 52 × 46 mm pocket in the stick's cup.

---

**Decision:** Food-grade transparent silicone tubing, 3.5 mm ID × 5.5 mm OD, 5 m.

**Why:** 3.5 mm ID matches black nylon car-hose fittings (#68409 5/32" tees, #68401 1/8" unions). Transparent shows fluid motion and clogs. Food-grade tolerates hot water rinse, mild detergent, bubble concentrate. 5 m covers pack-side plumbing plus spares.

**Implications:** This is the ONLY system tubing size; no 6 mm trunk. All junctions use car-hose fittings. Hose is semi-permanent; XT30U remains gun disconnect.

---

**Decision:** Black nylon car-hose connector assortment: #68401 1/8" straight unions, #68409 5/32" tees, larger reducers.

**Why:** One assortment ([price]) supplies the unions, tees, and reducers. Nylon tolerates bubble solution, glycerin, detergents.

**Implications:** The pack plumbing uses three tees (inlet tee, outlet tees 1 and 2), so check the assortment has three; each dual-head gun needs one more to feed its two donor pumps. Use #68401 for pump inlet/outlet, #68409 for manifold tees. Save extras for prototyping.

---

**Decision:** BigBigBear 4 mm liquid check valve (0.003 MPa opening pressure, PP body, silicone core, 304 SS spring), one in recirculation bypass only.

**Why:** Low opening pressure (0.44 psi) allows excess flow to recirculate while blocking backward siphoning. Higher-pressure valves create unwanted back-pressure. The 0.003 MPa spec is acceptable (nylon-silicone designs typically open ~0.18 psi).

**Implications:** Install arrow pointing toward pump inlet. The bypass runs: outlet tee 1's side branch → slide clamp → check valve → inlet tee. Valve is single-use; if clogged, replace it.

---

**Decision:** Printed slide clamp as the bypass restrictor (no purchased needle valve).

**Why:** One slide-clamp design does all three jobs (bypass restrictor and both channel shutoffs). Slide toward the arrow to close: ~8 mm of coarse travel, then 22 mm of fine adjustment, sealing at 0.6 mm. The shallow ramp self-locks, so there's no screw. Easy to print, requires no purchased parts.

**Implications:** Set during commissioning to achieve ~120–150% donor demand. Check valve + restrictor keep pump pressurized while guns are idle. Wet-test that the ramp holds.

---

**Decision:** Printed slide clamps (one per gun line) instead of purchased shutoff valves.

**Why:** Printed clamps are lighter, simpler, cheaper, and the same design as the bypass restrictor. When a channel is unused, slide its clamp closed.

**Implications:** Clamps are passive; operator action required. Not an active pack-side valve.

---

**Decision:** 4 ft standard umbilicals (16 AWG power + 3.5 mm silicone fluid + 550 paracord tether), 6 ft experimental.

**Why:** 4 ft allows head ~5 ft above pack (tether droop + arm reach). Paracord anchor prevents umbilical bearing load on power or fluid. Standard length simplifies storage and reduces voltage drop.

**Implications:** Longer runs (6+ ft) require 12 AWG or acceptance of ~0.6–0.8 V drop at 15 A. Umbilicals are single-piece (no quick-disconnect in fluid path); XT30U remains power disconnect.

---

**Decision:** JOYFY 32 oz commercial bubble concentrate (first test) plus Liquid Germall Plus 100 g preservative.

**Why:** Commercial concentrate is proven. JOYFY dilutes to 2.5 gallons from 32 oz. Germall preserves during storage and testing.

**Implications:** Mix per JOYFY instructions (~1:20 volume). Future tests will try Lulu 9:1 or JOYIN 10:1 water:concentrate, outdoor stream matrices (water + Dawn + J-Lube + glycerin), soluble dyes (post residue test). Never store solution in bladder; rinse, drain, dry after events.

---

## Control & PCB

**Decision:** BubbleLink CTRL v1.2: automatic pump controller on custom PCB. Gun power does NOT flow through PCB; PCB is logic-only.

**Why:** Separating 30 A gun path (handled by 12 AWG and ACS758) from control logic (<100 mA PCB) reduces PCB cost, complexity, fire risk. PCB receives 0–5 V ACS758 signal and switches 0.3 A pump MOSFET.

**Implications:** PCB is small (50.0 × 40.0 mm, 2-layer 1.6 mm FR-4, 1 oz copper, all components on top), 5 V powered. No high-current routing, no Kelvin shunt, no onboard current amp.

---

**Decision:** U1 is TI TLV1822QDRQ1 dual-output comparator (SOIC-8, 5.40 mm row spacing, 1.27 mm pitch, corrected footprint per TI D0008A).

**Why:** TLV1822 (not TLV1820) has dual outputs: one for threshold, one for hysteresis/timer. Original footprint was wrong; v1.2 corrects it per TI's drawing.

**Implications:** U1 is tight component; PCBWay assembles it (not hand-soldered).

---

**Decision:** Q2 AO3400A low-side pump MOSFET (4.5–20 V logic-level, ~1.7 mΩ on-resistance at 5 V, <0.15 mW dissipation at 0.3 A).

**Why:** Rated for 5 V gate drive. Dissipates negligible heat; no heatsink needed.

**Implications:** Gate pulled low during startup (R18 + C9) prevents accidental pump-on.

---

**Decision:** Q1 and Q3 DMP2065UQ-7 P-channel MOSFETs gate main 5 V bus to ensure PCB powers off if input sags below 4.38 V.

**Why:** Supervisor U2 controls them to prevent comparator misbehavior at brown-out.

**Implications:** PCB guaranteed to lose power and shut down before entering fault state.

---

**Decision:** U2 TLV803EA43DBZR supervisor (4.38 V threshold, ~200 ms reset delay) monitors 5 V input.

**Why:** If voltage drops below 4.38 V (2% margin above PCB 4.75 V minimum), triggers power-off, freezing pump.

**Implications:** PCB will not malfunction if Buck A sags momentarily.

---

**Decision:** D1 B340A Schottky diode for pump flyback (reverse-polarity and EMI suppression).

**Why:** Motor back-EMF rings when MOSFET turns off; diode clamps transient, protecting MOSFET gate and comparator.

**Implications:** Mandatory; omitting it risks MOSFET and comparator.

---

**Decision:** F1 1812L150/16DR PTC self-resetting fuse protects 5 V controller branch.

**Why:** If pump or PCB shorts, PTC melts and limits current to ~150 mA, preventing latchup. Recovers automatically when fault removed.

**Implications:** Small voltage drop (~0.3 V) in series with pump and PCB.

---

**Decision:** RV1 (2 kΩ 25-turn Bourns trimmer) sets ACS758 detection threshold, adjustable range ~2.21–2.80 V.

**Why:** ACS758 zero-current output is ~2.5 V. RV1 adjusts comparator non-inverting input to set sensitivity (~0.25–1.2 A gun current). Hysteresis ~4.42 mV.

**Implications:** User-soldered. Adjusted post-assembly by firing gun and observing LED response. Default ~2.5 V is safe; lower values risk false triggers.

---

**Decision:** RV2 (100 kΩ 25-turn Bourns trimmer) sets pump off-delay, calibrated to ~350 ms.

**Why:** After gun current drops, pump keeps running for ~350 ms to prevent mid-shot starvation and false off-states from PWM. Adjustable range ~35–574 ms.

**Implications:** User-soldered. Factory calibration ~350 ms; field operators rarely adjust this.

---

**Decision:** LEDs: Kingbright 3 mm T-1 (L-934GD green, L-934YD yellow, L-934ID red).

**Why:** Three dedicated LEDs: LED1 (green) = power on, LED2 (yellow) = gun current detected, LED3 (red) = pump active. User sees sequence: power on (green lit), gun trigger → yellow lights, red lights (pump running).

**Implications:** User-soldered. Current-limiting resistors on PCB (SMT). Provide instant visual feedback without firmware.

---

**Decision:** SW1 Omron B3F-1000 6×6 mm tactile switch = PRIME (momentary, no latch).

**Why:** Single momentary button allows manual pump start for priming or failsafe. Pressing PRIME runs pump for full off-delay. No pump-always-on mode.

**Implications:** User-soldered. Pressed through a printed plunger under a TPU boot in the stick's cap (the boot is optional; pulling a trigger also primes).

---

**Decision:** J4 AUTO/FORCE-ON input is DNP (Do Not Populate); no-respin fallback for very low gun current.

**Why:** ACS758 cannot reliably detect PWM-slowed or extremely low-current heads (<~0.5 A). Existing J4 pads provide fallback: short J4 to force pump on, or wire gun trigger's dry-contact to J4 for guaranteed activation.

**Implications:** J4 unpopulated unless needed. If required, solder 2-pin header post-assembly and connect external switch. No PCB respin; zero cost if unused.

---

**Decision:** C1 Rubycon 16ZLH100MEFC5X11 (100 µF 16 V) user-soldered at PCB input.

**Why:** Decouples 5 V input bus, absorbs transients from MOSFET and pump inrush. 16 V rating provides margin over 8.4 V system max.

**Implications:** Critical; must be within 1 cm of PCB input connector. Omitting it risks malfunction under pump load.

---

**Decision:** R18 (10 kΩ pull-down) and C9 (10 nF RC filter) on ACS758 output.

**Why:** R18 pulls signal low if sensor unplugged (below threshold). C9 low-pass filters 10 kHz motor noise, requiring ~10 ms for comparator trigger (prevents noise spikes from starting pump).

**Implications:** Both SMT, placed by PCBWay.

---

**Decision:** R22 is DNP (reserved for future feedback, unused in v1.2).

**Why:** Original design included optional feedback path (now unused). DNP allows future revision without respin.

**Implications:** R22 pads present but unsoldered.

---

**Decision:** 41 top-side SMT placements, zero bottom-side parts.

**Why:** Single-side assembly reduces cost and complexity. PCBWay places all components in one pass.

**Implications:** Five bare boards and 2 assembled ordered; 3 spare boards remain bare.

---

**Decision:** User-soldered through-hole parts: J1, J3 (2-pin JST B2B-XH), J2 (3-pin B3B-XH), C1, RV1, RV2, SW1, LED1–3.

**Why:** Large, low-current, simple to hand-solder. Saves PCBWay labor and allows field repair.

**Implications:** Assembly instructions must detail THT soldering (LED polarity, trimmer direction). First-time builder allows 45–60 min for THT work.

---

**Decision:** Five bench-only acceptance gates remain pending: startup/brownout behavior, external supply behavior, PTC thermal behavior, EMI, enclosure fit.

**Why:** Cannot be certified from CAD or simulation alone; require physical measurement on arrival.

**Implications:** Board receipt ≠ immediate deployment. Acceptance test (1–2 hours: pump fluid, measure thresholds, check LED response) required before field use.

---

## Guns, Heads & Umbilicals

**Decision:** Donor bubble-gun heads are test hardware, not a frozen universal design.

**Why:** Joey is extracting pump/fan/wetting mechanisms from random toy guns. Each donor may have different motor voltage, current, tubing, bubble pattern. Standardizing one head would require buying many identical toys (hard to find) or redesigning (out of scope for MVP).

**Implications:** For the target festival, the plan is a pair of dual-head guns (2 guns × 2 donor blower heads). Joey is picking up ~20 bubble guns this week to strip for heads: pick 4 matched heads and keep spares. Each gun's two head motors run in parallel on its XT30U, and both donor pumps are fed from its umbilical through one assortment tee. Rough estimate (unmeasured): ~12 A with all 4 heads firing (~6 A per channel, well under 30 A), about 2–2.5 h of heavy firing, about 2 h per 1 L. Post-assembly, each gun is characterized (current draw, flow rate, runtime, bubble quality). Head selection is data-driven.

---

**Decision:** Donor sled interface: 30 × 20 mm, four M3 holes for printed mounting.

**Why:** Small printed sled holds donor mechanism in standard orientation relative to umbilical. 30 × 20 mm footprint fits most small toy-gun mechanisms.

**Implications:** Each new donor requires custom sled printed from measurements. Gun/head mounts are not designed yet; they need the teardown measurements.

---

**Decision:** Local MOSFET switching keeps motor current out of trigger; basic on/off first (no PWM).

**Why:** Mechanical triggers are flaky and create noise. Small MOSFET near motor decouples trigger contact (low current) from motor (high current), improving reliability and reducing electrical noise.

**Implications:** Small N-channel MOSFET + 10 kΩ pull-down + 100 nF capacitor at each donor during characterization. PWM speed control is future work; see docs/16-roadmap-future-extensions.md.

---

**Decision:** Umbilical load borne by paracord tether, not power connectors or fluid hose.

**Why:** XT30U and silicone hose are rated for flow and signal, not sustained mechanical load. 550 paracord (4 mm, ~550 lb breaking strength) takes full weight when held high.

**Implications:** Umbilical assembly includes paracord loop with knot/carabiner anchor. A printed umbilical brick at each end holds the XT30U (strapped in an open pocket), the 16 AWG pair and the tube (in grooves under narrow zip ties), and anchors the paracord; paracord separate, not twisted.

---

## Carrier & Cosplay

**Decision:** Carrier bag is MAX LED "M Style" Bluetooth LED pixel backpack (internal geometry unknown until measured).

**Why:** Commercial, waterproof, modular. Holds the printed stick (about 99 × 78 × 207 mm, ~1.6 L) beside the 1 L reservoir. The "~34 × 20 × 7 cm" figure that circulated is an AI estimate of the exterior from photos, not an internal measurement.

**Implications:** The bag's internal geometry is still unmeasured. The stick is self-contained, with two umbilicals leaving its bottom, so it can move to a different bag easily.

---

**Decision:** Everything except the bladder is one upright printed "stick" standing beside the bladder (approved combining parts 2026-10-14): a control-head cap over a sealed dry tube (battery and electronics on a slide-out sled) over a draining wet cup (pump and fittings).

**Why:** The battery rides high (heavy part high, close to the back), the wet cup is lowest so spills drain away from the electronics, and the whole pack except the bladder is one portable unit. An intermediate wide-box design (about 157 × 171 × 52 mm) was dropped the same day because it couldn't sit beside the bladder.

**Implications:** The tube's floor (bulkhead) is the wet/dry divider; cables cross it through a slit TPU grommet that is a splash baffle, not watertight. The cap's TPU ring seal, pressure relief if a cell fails, and enclosed-charging temperatures are not verified: wet-test the cap, and charge with the cap off until the first enclosed charge has been checked. Umbilicals, bladder feed, LED-backpack USB and the XT60H disconnect loop exit through the cup's floor. Hardware: 6 M3 screws + 6 glued-in nuts, zip ties, glue, 1 mm foam, tape. Details in [09-printed-parts.md](09-printed-parts.md).

---

**Decision:** Tracer (Overwatch) cosplay is separate project sharing the pack.

**Why:** Target event (the target festival 2026-10-30 to 31) includes cosplay contest. Hollow printed gun shells house actual bubble guns, everything white, with 2 m ice-blue 5 V COB LED strip for lighting.

**Implications:** MVP shell is bubble gun hardware only (XT30U channels, umbilicals). Cosplay shells are future work contingent on MVP success.

---

## Manufacturing & Schedule

**Decision:** PCBWay order [PCB order] (v1.2, replaces v1.1 [original PCB order]): 5 boards fabricated, 2 assembled, 3 bare spares.

**Why:** v1.1 held after U1 footprint error discovered. v1.2 corrects footprint per TI D0008A. PCBWay replaced order at no cost. 2026-09-24 balance paid, 2026-10-03 assembly photos approved, 2026-10-08–11 dispatched. Boards in transit; ETA 2026-10-15–18.

**Implications:** Bare boards are spares. Two assembled boards sufficient for MVP; one held as unit spare.

---

**Decision:** Assembly is [assembly order] within group [order group]; 41 top-side SMT placements, J4 and R22 DNP, C9 and R18 fitted, U1 is TI TLV1822QDRQ1 with corrected footprint.

**Why:** Confirms correct placement of all components.

**Implications:** Board receipt does not mean immediate deployment. Acceptance test (1–2 hours) required before field use.

---

**Decision:** First build sequence: rig with one converted gun, then fluid/power proof, then donor characterization, then wrist/cosplay/UV/progressive-trigger options, then larger battery if real use justifies.

**Why:** De-risks project. Working single-gun system deployable within deadline. Multi-head and cosplay happen post-event if MVP succeeds.

**Implications:** the target festival 2026-10-30–31 deployment is one gun per channel (a pair of dual-head guns), 1 L reservoir. Wrist emitter, six/sixteen-head stick, 180 Wh cartridge are future work (roadmap only, not MVP).

---

**Decision:** CAD paused until purchase exports and product details available (2026-10-11 instruction); lifted 2026-10-14.

**Why:** Actual part sizes were unknown from listings alone, and several listing figures turned out wrong. Premature CAD would guess and require rework.

**Implications:** Joey measured the breaker, BMS, bucks, ACS758, charger, voltmeter and pump with a tape measure on 2026-10-14, and the printed-part CAD now exists (OpenSCAD in `hardware/printed/src`, STLs in `hardware/printed/stl`, built with `hardware/printed/build.sh`). Nothing has been printed or test-fitted yet. Still unknown: the bucks' width (17 mm assumed). The earlier battery cartridge, pump cradle, divider/tray, brackets, breaker fence, buck pads, faceplates, pump/hose/tether block, Cults3D spacer remix and connector blocks are superseded. 6–8 day build estimate assumes printing is done before board arrival.

---

**Decision:** User-soldered through-hole for C1, RV1, RV2, SW1, LED1–3, J1–3; PCBWay places 41 SMT parts.

**Why:** THT parts are large, low-current, hand-solderable. Reduces PCBWay labor; allows field repair.

**Implications:** ~18–20 hand solder joints. First-time builders allow 45–60 min. No SMT equipment required.

---

**Decision:** Purchased components reused; excess stay at PCBWay.

**Why:** Reduces cost; supplies stored for future orders.

**Implications:** Joey does not receive component kit. All parts soldered by PCBWay (SMT) or builder (THT).

---

**Decision:** Hard deadline: 2026-10-29 (one day before the target festival opens 2026-10-30).

**Why:** Target event 2026-10-30–31. One day allows final checks without event-day panic.

**Implications:** Any delay in board receipt or assembly forces last-minute gamble. Critical path is boards arriving, test, then 6–8 day build.

---

**Decision:** Samsung 25R cells sourced from Joey's existing inventory (10 cells already owned).

**Why:** Cells proven in prior testing; supply chain certain.

**Implications:** Future spare packs require cell sourcing (AliExpress/Amazon ~$2–3 per cell).

---

**Decision:** BMS, charger, breaker sourced from AliExpress (2S 40 A BMS ~[price], SZHJW 2S 4A charger ~[price], YONGRUN 30 A breaker ~[price]).

**Why:** Lowest cost, readily available. Typical delivery 2–4 weeks acceptable for development.

**Implications:** Lead time is longest item in critical path after PCB design. All battery components ordered in parallel to minimize project duration.

---

**Decision:** 3D-printed parts: the stick (cap, tube, sled, cup, PRIME plunger) in PETG, with TPU for the cap ring, the two grommet halves, the PRIME boot and the cap-screw washers; plus the fit coupon, cell holders MID/TERM, slide clamps ×3 and umbilical bricks ×4 in PETG.

**Why:** Eliminates injection-mold lead time. Allows rapid iteration. Cost-effective for small batches. End users can reprint spares (OpenSCAD sources and STL files provided).

**Implications:** Nothing needs supports. Print the fit coupon first and set the cell-bore and XT30U clearances from it, then the cell holders and slide clamps, then the stick parts and bricks. Use a light-coloured PETG for the cap so the LEDs show through. See [hardware/printed/README.md](../hardware/printed/README.md).

---

**Decision:** Printers: Creality K2 Plus (350³ mm) and Bambu Lab A1 (256³ mm), both owned by Joey.

**Why:** Both fit every stick part (the tallest, the tube, is 139 mm). A1 is faster for small parts.

**Implications:** Stick parts on either printer. Small parts (coupon, clamps, bricks, plunger) and all TPU parts on the A1.

---

**Decision:** Testing strategy: commissioning measurements before field deployment.

**Why:** Validates all design assumptions against real hardware before relying on pack at public event.

**Implications:** Commissioning takes 8–12 hours (including cool-down). Measures cell capacity, battery voltage under load, pump flow, gun motor current, thermal rise. If measurements exceed design margins, field limits reduced.

---

**Decision:** No firmware, no MCU, purely analog control.

**Why:** Eliminates single point of failure (MCU crash). Analog is deterministic and bulletproof. No toolchain needed for end users.

**Implications:** Control logic fixed; changes require PCB redesign. Optional future telemetry (INA228 + MCU + OLED) can use unpopulated footprints.

---

**Decision:** Nine bench-only acceptance gates remain pending before final deployment.

**Why:** These cannot be certified from CAD or simulation; require physical measurement: startup/brownout, external supply behavior, PTC thermal, EMI, enclosure fit.

**Implications:** Acceptance test required post-board arrival. v1.2 package specifies exact test procedures and limits.

---

**Word count:** ~5,300 words, 69 final design decisions organized across nine domains. Each decision includes final state (one line), rationale with numbers and sources, and implications for building and field use.
