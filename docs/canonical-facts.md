# Canonical facts

This is the one-page verified summary of BubbleLink's final design and status. Every other doc in this repo was checked against it. **If any doc disagrees with this page, this page wins.** Then fix the other doc.

Verified against the primary sources: the v1.2 release package, the AliExpress order history (2026-08-06), the final cart and decisions in the design thread, the v1.1 Release thread, the PCBWay emails, and the 2026-10-14 design review.

## Identity and status
- BubbleLink is Joey's **pack-fed, two-channel modular bubble system**. A backpack holds the battery, the 1 L bubble reservoir, one shared transfer pump, and an automatic pump controller PCB. Hand-held bubble heads (donor toy-gun mechanisms) plug in through umbilicals.
- **Joey's existing overvolted three-head bubble gun** (2S1P Samsung 25R, ~18 Wh) is real, working baseline hardware, called the "Equivalent Gun Unit" (EGU). It is NOT a completed BubbleLink prototype. It's the performance reference and the intended first head for one channel.
- **Target event:** the target festival, **2026-10-30 to 31**. Project must be complete by **2026-10-29**.
- **As of 2026-10-14:** the AliExpress parts are on hand (Joey, 2026-08-21: all bubble parts on hand except the PCB). The PCBs shipped and are in transit: 4PX **[tracking removed]**, SpeedX **[tracking removed]**, customs cleared 10-12, ETA **Oct 15–18**. Board receipt and acceptance are not yet confirmed. Joey's estimate: 6–8 days of build after the boards arrive, if prep is done first.
- **2026-10-11 instruction:** BubbleLink CAD is paused until purchase details are available. This repo now provides them (docs/parts/), so the pause can be lifted at Joey's call. Don't claim CAD exists.
- No complete 90 Wh cartridge, print pack, integrated plumbing, or field trial of BubbleLink exists yet.

## Baseline measurements (existing gun, 2S1P 25R)
- 2,500 mAh cells. ~15 min full-trigger life. ~70 W firing power (inferred). Continuous fluid use 118.4 mL / 7 min ≈ 16.9 mL/min. Heavy event 473.6 mL in ~75 min, giving ~37% duty, ~26 W average, ~0.069 Wh/mL.
- Joey's batteries get warm, once nearly too hot to touch, under heavy use. The gun's spring contacts are poor ("hot garbage"), so solder the connections.
- Field history: a summer festival 2026-08-02 (five canisters in 80–90 min); a convention 2026-09-04 to 06 (venue staff refused the gun at Friday's EDM event despite earlier approval).

## Power (final)
- **Battery cartridge: 2S5P**, 10× Samsung INR18650-25R (owned; match and qualify first). 7.2 V nominal, 8.4 V full, 12.5 Ah, **90 Wh**. Cells 18.33 ± 0.07 mm × 64.85 ± 0.15 mm. Printed 5×2 upper/lower spacers, fish-paper insulator rings, **nickel-plated steel tabs** (3 × 10 pcs, 2.6 cm), with **five parallel series bridges** so no single strip carries full pack current. Spot welded.
- **BMS:** IC GOGOGO 2S **8.4 V 40 A** Li-ion with balance.
- **Charger:** SZHJW USB-C → 2S 8.4 V boost charger, **2S 4A** variant. Charging is battery-side.
- **Main protection:** ONE **30 A manual-reset breaker** (YONGRUN Type B-30A, 12–48 V DC, 72×48×44 mm, **M6 threaded studs**). Wire to the studs with **SC10-6 copper ring lugs**, solder-filled and strain-relieved (the 10 mm² barrel is oversized for 12 AWG). Never solder to the studs. There are no per-channel fuses.
- **Wire:** **12 AWG** silicone (black/red, 3 m each) for the battery/main path; **16 AWG** (black/red, 5 m each) for gun branches/umbilicals.
- **Connectors:** **XT60H** for the battery cartridge; **XT30U** (AMASS-style, 10 pairs) per gun channel, power + and − only, with no signal wire to the guns; **JST-XH** kit for low-current/PCB/balance.
- **High-current path:** `battery → BMS → XT60H → 30 A breaker → ACS758 high-current terminals → split → two XT30U gun channels`. Gun current never passes through the PCB.
- **Current sensor:** ACS758LCB-**050B** module, 5 V supply, **40 mV/A**, ~2.5 V at zero current, ±50 A. It measures **combined** gun current, not per-channel.
- **Gun bus:** raw, unregulated 2S (~6.0–8.4 V). Fixed full-power triggers. No per-gun PWM.
- **5 V rails:** two YxPC 6–20 V → 5 V USB bucks. **Buck A** powers the controller PCB and pump (~5.0–5.1 V; the PCB's qualified input is 4.75–5.25 V). **Buck B** powers the LED backpack's USB. The listing has no defensible current spec. If Buck A misbehaves, the recommended external upgrade is a **Pololu S13V30F5** (no PCB change).
- **Voltmeter:** Stlxy DC 4–100 V two-wire round LED voltmeter, red, 5 bought (1 used, 4 spares). It's the battery gauge; there's no percentage fuel gauge.
- Master disconnect intent: an XT60 loop key or unplugging the battery XT60. Electrical work requires disconnecting the battery and the USB-C input.

## Fluid (final)
- **Reservoir:** UWWWMM **1 L** blue hydration bladder with a **101 cm detachable drinking tube** (keep its leakproof disconnect; cut the tube short).
- **Pump:** ONE **GROTHEN G528** peristaltic, **6 V, 3×5 mm tube, 150 mL/min** variant (4–6 V rated, ~0.25–0.30 A). It runs from Buck A's 5 V through the PCB's MOSFET. Check that the delivered motor is marked 6 V (the seller art says 12 V). It's shared by both channels.
- **Tubing:** food-grade transparent silicone, **3.5 mm ID × 5.5 mm OD, 5 m**. This is the ONLY system tubing; there's no 6 mm trunk. The pump's own tube is 3×5 mm.
- **Fittings:** the black nylon **car-hose connector assortment** (set) supplies the unions, tees, and reducers. Use `#68401` 1/8" straight unions for the pump and connector bricks, and `#68409` 5/32" (≈4 mm) tees (or `#68408` 1/8") for the manifold. The 1/4" and 3/8" reducers mate the bladder's factory hose to the 3.5 mm silicone. Secure barbs with narrow zip ties; warm silicone in hot water to stretch it.
- **Check valve:** BigBigBear **4 mm** one-way, **0.003 MPa (0.435 psi) opening pressure**, PP body, silicone core, 304 SS spring, liquid-rated, hose barb. One only (the listing is limited to 1 per shopper).
- **Recirculating bypass:** `pump outlet → printed adjustable pinch restrictor → check valve → pump-inlet tee`, valve arrow toward the inlet/reservoir side. Excess flow recirculates instead of force-feeding a stopped donor pump, and the reservoir can't siphon past the stopped pump.
- **Path:** `1 L bladder → factory tube (cut short) → assortment reducer → 3.5×5.5 silicone → inlet tee (bypass return) → G528 → outlet tee → left channel / right channel / bypass`.
- Unused channels are closed with **printed pinch clamps** (no purchased shutoff valves). The fluid hose is **semi-permanent** for the MVP; the XT30U remains the disconnect.
- Donor pumps stay in place as the final metering stage. Donor-side reducers get chosen only after measuring each donor's tubing.
- **Umbilical length:** 4 ft standard, 6 ft experimental. Head may be ~5 ft above the pack.
- **Solution:** JOYFY 32 oz concentrate ("up to 2.5 gallons"), commercial concentrate first. Liquid Germall Plus 100 g was also bought as a preservative. Rinse/flush, drain, and dry after every event; never store solution in the bladder.
- Future fluid profiles to test (intentions only): Lulu 9:1 or JOYIN 10:1 water:concentrate; outdoor stream matrix of 1,000 mL water + 50–70 mL Dawn Professional + 0–0.20 g J-Lube + 0–10 mL glycerin; soluble fluorescent dye only after residue tests.

## Controller PCB: BubbleLink CTRL v1.2 (final)
- Purpose: an **automatic transfer-pump controller**. When either gun draws current, the pump runs; when the guns stop, the pump keeps running for a calibrated **~350 ms** off-delay (range ~35–574 ms), then stops.
- U1 **TI TLV1822QDRQ1** dual comparator (SOIC-8; v1.2 land pattern per TI D0008A, 5.40 mm row centers, 1.27 mm pitch). Q2 **AO3400A** low-side pump switch. Q1/Q3 **DMP2065UQ-7**. D1 **B340A** flyback. F1 **1812L150/16DR** PTC. U2 **TLV803EA43DBZR** supervisor (4.38 V, ~200 ms). FB1 ferrite, logic-rail filtering. R18 pulls ACS_OUT low (unplugged sensor = off). R1/C5 10 ms sensor filter.
- RV1 (2 kΩ 3296W) sets the detection threshold, ~2.21–2.80 V; hysteresis ~4.42 mV. RV2 (100 kΩ 3296W) sets the off-delay, calibrated to 350 ms.
- LEDs: LED1 green = power, LED2 yellow = gun active, LED3 red = pump active (Kingbright L-934GD/YD/ID). SW1 Omron B3F-1000 = **PRIME** (momentary).
- **J4 AUTO/FORCE-ON input** is DNP: a no-respin fallback if the ACS758 can't detect a very low-current or PWM-slowed head. **R22 DNP. C9 and R18 fitted.**
- 41 top-side SMT placements, 92 paste apertures, no bottom-side parts. User-soldered THT: J1, J3 (B2B-XH), J2 (B3B-XH), C1 (Rubycon 16ZLH100MEFC5X11 100 µF 16 V), RV1, RV2, SW1, LED1–3.
- External connections only: 5 V + GND from Buck A; 3 wires to the ACS758; 2 wires to the pump.
- The PCB does NOT do charging, BMS, main overcurrent, gun regulation/PWM, per-channel control, fuel gauge, voltmeter, backpack power, or firmware.
- Release QA: 50 PASS / 0 FAIL. Electrical Monte Carlo of 20,000 samples passed. **Nine bench-only gates remain pending** (no physical measurements claimed).

## PCBWay (final)
- Original order **[original PCB order]** (v1.1) was held after the U1 footprint problem was found. Its old boards are not assembled and not shipped.
- Replacement order **[PCB order]** (v1.2, marked "replace [original PCB order]"). Assembly **[assembly order]**, group **[order group]**. **5 boards fabricated, 2 assembled.** New stencil. U1 stays TLV1822QDRQ1, with no substitution. Purchased components reused; excess components stay at PCBWay.
- 2026-09-24: remaining balance (~$40) paid. 2026-10-03: assembly photos approved. 2026-10-08 to 11: dispatched. Now in transit (tracking above).

## Carrier and cosplay (final)
- The bag is the MAX LED **"M Style" Bluetooth LED pixel backpack**. Its internal geometry is unknown until measured. Buck B powers its display (target 2–3 W average, 4 W ceiling).
- Layout intent: battery high and close to the spine; dry electronics above an open-bottom, draining wet bay; connectors at lower left and right; the master disconnect reachable.
- **Tracer (Overwatch) cosplay** is a separate project that can share the pack. Hollow printed gun shells with bubble guns installed, everything printed in white, a 2 m ice-blue 5 V COB LED strip (not waterproof, not UV). Printers: Creality K2 Plus (350³ mm) and Bambu Lab A1 (256³ mm).

## Not part of the final system

These came up during design and were dropped, swapped out, or never ordered. They're listed only so nobody reintroduces them by accident.
Kamoer NKP pumps, two pumps, a 12 V pump, a 6 mm trunk, Luer fittings, CPC couplings, a stopcock, aquarium tee packs, pneumatic push-fittings, purchased inline shutoff valves, a filter, INA180/shunt sensing, LM393/BSS84/SS34 (pre-design concept parts), per-channel fuses, HUSB238/TP5100 charging, Hobbywing UBEC, MP1584, Arduino/Nano fallback kit, D4184 modules, PWM motor controllers, Heltec/Enerkey BMS, a 40 A breaker, a running vest/CamelBak carrier, a separate drinking bladder, and the June standalone blower-and-handle housing. Future extensions (2S10P 180 Wh cartridge, wrist emitter, UV torch, progressive Hall trigger, six-head stick, 16-head totem, Bubble Miku) are covered only in [16-roadmap-future-extensions.md](16-roadmap-future-extensions.md).

## More things that are not part of the system
- No "removable cassette" or QD cassette. The pack has a printed wet/dry divider and an electronics tray inside the MAX LED backpack.
- No 7 L festival pack or "club bag" migration. No an earlier festival bag rules (an older event; they don't apply to the target festival).
- No pump mode switch / OFF-AUTO-ON switch. The PCB has only the momentary **PRIME** button (SW1) and the DNP **J4 AUTO/FORCE-ON** input.
- No 40 A backup/one-shot fuse. Protection is the single 30 A breaker, plus F1 (1.5 A PTC, 1812L150/16DR) on the PCB pump branch.
- The PCB comparator is the TLV1822QDRQ1, NOT an LM393. The flyback diode is the B340A, NOT an SS34. Q1/Q3 are DMP2065UQ-7 P-channel parts, NOT BSS84. PRIME grounds DET_N and runs the same delay path; it doesn't drive Q2 directly.
- Fluid terminations use nylon barbs from the car-hose assortment with narrow zip ties, NOT Luer-lock barbs or hose clamps.
- C1 is 100 µF 16 V (Rubycon 16ZLH100MEFC5X11), NOT 470 µF.

