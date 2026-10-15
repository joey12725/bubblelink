# Bubble-Gun Heads, Umbilicals, and Wands

This document covers the selection, qualification, and integration of donor bubble-gun heads into the BubbleLink system; the electrical umbilical design connecting pack to gun; multi-head wand configurations; and the integration of gun heads into Tracer cosplay prop shells.

## Contents

- [Donor bubble-gun heads](#donor-bubble-gun-heads)
- [Current and voltage characteristics](#current-and-voltage-characteristics)
- [Overvolting findings](#overvolting-findings)
- [Gun-side wiring and contacts](#gun-side-wiring-and-contacts)
- [Trigger control](#trigger-control)
- [Umbilical design](#umbilical-design)
- [Multi-head wands](#multi-head-wands)
- [Head capacity limits](#head-capacity-limits)
- [Gun teardown and qualification](#gun-teardown-and-qualification)
- [Tracer cosplay integration](#tracer-cosplay-integration)

---

## Donor bubble-gun heads

BubbleLink uses donor bubble-gun heads stripped from retail toy guns rather than custom-fabricated heads. This approach retains the original pump (which is already optimized for the head geometry and solution delivery) and avoids the cost, MOQ, and engineering complexity of custom gearbox orders from industrial suppliers. Joey rips heads out of random toy guns, typically selecting models from AliExpress or retail stores that offer:

- Multiple bubbling heads (2–4 per gun is common)
- Brushed-motor drive with integrated pump
- Electrical accessibility for power and ground
- Stable mounting points inside the gun plastic housing

An existing three-head gun has been used for all benchmarking and performance reference. This gun remains the only one "actually proven to survive [Joey's] usage," though its original solder contacts were creating unintended voltage drop and current limiting.

### the target festival plan: a pair of dual-head guns

- **Two guns × two donor blower heads.** Joey is picking up ~20 bubble guns this week to strip for heads. Pick 4 matched heads and keep the spares.
- **Wiring:** each gun's two head motors run in parallel on that gun's XT30U.
- **Fluid:** both donor pumps in a gun are fed from its umbilical through one assortment tee.
- **Rough estimates (not measured):** ~12 A with all 4 heads firing (~6 A per channel, well under the 30 A breaker); about 2–2.5 h of heavy firing; about 2 h per 1 L of fluid.
- **Mounts:** gun/head mounts are not designed yet. They need the teardown measurements.

---

## Current and voltage characteristics

### Baseline performance

Measured with Joey's existing three-head gun:

- **Voltage draw:** 3.2 V to 4.2 V (full discharge of 2S at rest to nominal full charge)
- **Power draw:** ~70 W (inferred from energy and runtime)
- **Runtime on 2S 18650 pair:** ~15 minutes continuous at full throttle
- **Battery test:** Two Samsung INR18650-25R cells (2,500 mAh each, 2S1P configuration, ~18 Wh) discharged from 4.2 V to 3.2 V during continuous full-power operation

### Current variability and fixed full-power operation

Donor heads exhibit highly variable starting and running current depending on:

- Motor speed (determined by applied voltage)
- Pump load (affected by solution viscosity, hose restriction, and pressure head)
- Physical binding or obstruction in the motor or drive train

The MVP design uses **fixed full-power triggers** on each gun channel: when pulled, the trigger connects the gun's motor supply directly to the pack voltage (raw, unregulated 2S, ~6.0–8.4 V) without current-limiting resistors or PWM. This approach is simple and reliable for field operation.

**Progressive triggers (future):** A future version may integrate a potentiometer-based voltage control into the gun wand, allowing Joey to adjust output from minimal (low power, long runtime) to maximum (high visual impact) during a performance. Potentiometer control is deferred to the roadmap. When implemented, a potentiometer would be preferred over a series resistor because a resistor would dissipate excess power as heat (~2.7 W at 0.5 A over 5 V drop) and create thermal risk.

### Current sensing and low-current floor

The ACS758LCB-050B Hall-effect current sensor (40 mV/A sensitivity) detects gun activity to trigger the pack's transfer pump. The sensor has a **reliable detection floor of approximately 0.1 A**. For the MVP's fixed full-power triggers, this threshold is not a practical concern; however, the limitation exists to support future progressive trigger designs (potentiometer or PWM control at very low voltages).

**Fallback:** If a gun fails to activate the ACS758 above its detection limit—relevant when progressive low-speed operation is enabled—the J4 FORCE-ON jumper on the PCB provides a manual override to enable the pump regardless of sensed current. This fallback is a no-respin design safety feature and is valuable for troubleshooting.

---

## Overvolting findings

Joey has experimentally overvolted prototype guns to improve performance and understand the limits.

### 2S operation and motor heating

Overvolting to 8.4 V (2S Li-ion full charge) from the design nominal ~4.2 V produces significant heating:

- **Stall heating scaling:** Approximately **4× winding heating at stall** compared to 4.2 V operation
- **Copper heating mechanism:** Winding heating rises approximately with current squared; stall current roughly doubles at 8.4 V, so heating quadruples
- **Motor lifespan:** Sustained operation at 8.4 V on small toy motors causes brush sparking, visible gear noise, and internal winding temperature rise approaching or exceeding motor design limits
- **Initial transient improvement:** Motor speed increases ~21% and airflow improves noticeably at first, but continued high-voltage operation degrades the motor
- **Flow demand:** Motors overvolted to 8.4 V draw significantly higher current at startup (~54% more than at 3.7 V baseline), which can collapse bench supplies with insufficient current limit

### Recommended operating envelope

The MVP operates at **raw 2S pack voltage** (6.0–8.4 V depending on battery charge state), with no on-gun voltage regulation. Based on Joey's field experience with the existing three-head gun:

- **Sustained operation:** 6.0–7.2 V (nominal pack voltage, minimal motor stress). Running continuously at 8.4 V causes brush sparking and accelerated wear.
- **Short bursts / peak effect:** up to 8.4 V for maximum visual impact, but monitor brush noise and motor temperature; limit duration to a few seconds.
- **Heat management:** If progressive voltage control is added in the future, a practical sweet spot for extended performance would be 3.7–5.5 V per motor, balancing visual impact with motor longevity.

**Note:** With fixed full-power MVP triggers, the gun operates at whatever the pack provides. Voltage varies naturally with battery state. Performance will degrade slightly from 8.4 V (full) down to 6.0 V (depleted) but remains usable across the entire discharge range.

### Pack voltage to the gun channels

The pack supplies **raw, unregulated 2S pack voltage** (~6.0–8.4 V depending on battery state) directly to each XT30U connector, with no per-gun PWM, regulator, or voltage-limiting circuit. This approach keeps the pack's architecture simple: the pack is a power and fluid source. Gun voltage varies naturally with battery discharge (8.4 V at full charge down to 6.0 V near depletion).

**MVP behavior:** With fixed full-power triggers, the gun operates at whatever voltage the pack provides at that moment. Performance scales with battery state but remains simple and field-reliable.

**Progressive control (future):** A future design revision may add potentiometer-based or PWM voltage control integrated into the gun wand, allowing Joey to:

- Adjust output during a performance without battery-state dependency
- Vary power smoothly (e.g., ramp up toward a beat drop)
- Extend runtime by reducing voltage when full power is not needed

See [docs/16-roadmap-future-extensions.md](16-roadmap-future-extensions.md) for long-term trigger plans.

---

## Gun-side wiring and contacts

### Bad spring contacts—solder instead

Joey's original three-head gun has "flimsy thin springs and the positive end of a battery in contact directly with solder." This bad contact design exhibits:

- **Contact resistance:** ~0.05 Ω (measured)
- **Power dissipation:** 0.05 Ω × 8 A² = 3.2 W at full current
- **Voltage drop:** 0.05 Ω × 8 A = 0.4 V (significant for low-voltage systems)
- **Heat generation:** Contacts become too hot to touch during extended use, creating thermal stress on the battery and control circuitry

**Corrected approach:** Replace all gun-side battery and motor connections with **soldered XT30U connectors and high-gauge wire**. This eliminates the spring-contact bottleneck and ensures the motor receives full pack voltage.

### Donor gun structure

Typical donor guns contain:

- **Battery input:** Two to four small motors (fans, wand drives, bubble-head drivers)
- **Motor wiring:** Usually thin 18–24 AWG wire soldered or spot-welded to a small internal PCB
- **Pump connection:** Built-in peristaltic or gear pump, already integrated into the gun's plastic body
- **Fluid input:** Wetting manifold or open nozzles that the hose connects to via barb fittings

The external BubbleLink system connects:

1. Power via XT30U connectors to the gun's motor supply (replacing or augmenting the original internal battery)
2. Fluid via a barbed silicone hose to the existing wetting manifold
3. Trigger switch (on/off only; MVP uses direct motor connection with no voltage regulation)

---

## Trigger control

### MVP: Fixed full-power triggers

The BubbleLink MVP design uses **fixed full-power triggers** on each gun channel: when pulled, the trigger connects the gun's motor supply directly to the pack voltage without current-limiting resistors, PWM, or potentiometer control. This approach is simple, reliable, and proven in field use on Joey's existing three-head gun.

**Performance variation:** Gun output varies naturally with battery state (8.4 V at full charge down to 6.0 V near depletion). For sustained MVP operation with minimal motor stress, keep the pack in the 6.0–7.2 V nominal range. Running continuously at 8.4 V causes motor stress (see [Overvolting findings](#overvolting-findings) for thermal limits).

**Progressive control (future):** Future iterations may add potentiometer-based or PWM voltage control integrated into the gun wand or backpack, allowing real-time adjustment during a performance. When implemented, progressive triggers would allow:
- Continuous voltage selection from 3 V (minimal power, extended runtime) to 8.4 V (peak aggression)
- Dynamic power adjustment during a performance without battery-state dependency
- Optional dual-gang potentiometer for coordinated multi-head wands

See [docs/16-roadmap-future-extensions.md](16-roadmap-future-extensions.md) for long-term control architecture.

---

## Umbilical design

The electrical and fluid "umbilical" connects the pack to each gun head. It is a single bundle combining power, tether, and fluid in a compact, strain-relieved assembly.

### Components per umbilical

| Item | Specification | Source |
|---|---|---|
| **Electrical power connectors** | XT30U male/female pair (15 A rated, 1 per channel) | AliExpress order ref [order ref removed] |
| **Hose (fluid)** | ID 3.5 mm, OD 5.5 mm silicone tube, food-grade | 5 m spool; order ref [order ref removed] |
| **Tether (mechanical load-bearing)** | 550 paracord, 7-strand, 4 mm diameter, black | 15 m spool; order ref [order ref removed] |
| **Wire protection** | 10 mm braided PET sleeving | 5 m spool; order ref [order ref removed] |
| **Umbilical bricks** | Printed ASA (or PETG), one at the gun end of each umbilical (×2 total; no brick at the pack end) | `hardware/printed/` (`10_umbilical_brick_x2`) |

### Hose length—default 4 feet

The **default umbilical length is 4 feet (approximately 1.2 m)**, which provides:

- **Hose volume:** ~9.8 mL (fast priming, low solution waste)
- **Ease of handling:** Compact, light, easy to coil in pack or belt
- **Typical use case:** Wrist-mounted gun, short-distance spray, standard festival dancing

**Extended umbilical option:** **6 feet (approximately 1.8 m)** is available for special cases (e.g., longboard-mounted gun, unusual routing through costume). This adds only ~4.7 mL extra hose volume (14.5 mL total) but can complicate pack routing. Custom longer umbilicals can be assembled using the same components.

### Assembly procedure

1. **Hose:** Cut silicone tube to desired length (4 or 6 feet default) from the 5 m spool; flush with water to remove dust; allow to dry
2. **Paracord tether:** Cut paracord to match hose length; seal cut ends with a lighter to prevent fraying
3. **Braided sleeving:** Pre-stretch 10 mm braided PET to length; slide onto the hose + paracord bundle
4. **Power connector(s):** Solder the 16 AWG wire pair to an XT30U **male** at the pack end and an XT30U **female** at the gun end (power always comes from a female, so no live pins are exposed); use adhesive heat shrink to cover each solder joint
5. **Gun-end brick:** At the gun end, drop the XT30U into the brick's open-top pocket and strap it with a zip tie through the slots beside the pocket. Run the 16 AWG pair and the tube in their grooves under narrow zip ties. Tie the paracord through the outer hole
6. **Pack-side termination:** The pack end has no brick: it is an XT30U male on the 16 AWG pair, the hose end and a paracord loop. Push the male into the pack-side XT30U female in the cup's port well (proof-test each port with a ~70 N pull, paracord slack) (the male's shroud slides into the well around it). Join the umbilical hose to the port's hose pigtail with a straight barbed connector from the assortment, and tie the paracord through the port's U-tunnel boss (thread it with a leader, a stiff wire or a zip tie taped to the cord's tip; cord in one opening, out the other, knot, melt the ends). Port 1 takes umbilical 1 and port 2 takes umbilical 2. Keep the cord shorter than the hose and wires, so it takes any pull first. Close an unplugged well with a TPU port cap
7. **Gun-side termination:** Fit an XT30U **male** to the gun's motor input (the umbilical's gun-end female plugs onto it); barb the hose to the gun's wetting manifold (through one assortment tee to both donor pumps on a dual-head gun) and tie the brick's inner hole to the gun body or wand

### Strain relief and routing

- **Paracord as load-bearing tether:** The 550 paracord **is the primary load path** for the umbilical. All tension (including accidental tugging, falls, or costume weight) goes through the paracord, not the hose or electrical connectors
- **Braided sleeving:** Provides protection from abrasion and UV; also visually integrates the umbilical bundle
- **Pack-side anchor:** Both umbilicals plug into port clusters on the cup's outer wall (one per gun), each with an XT30U well, a hose pigtail and a paracord U-tunnel. The load path is gun, gun-end brick, paracord, U-tunnel boss on the cup, and the cup's four M3 screws into the bulkhead nuts. Nothing in the umbilical joins inside the wet cup
- **Umbilical brick:** A **printed ASA (or PETG) brick** at the gun end of each umbilical prevents sharp bends, holds the XT30U, and anchors the paracord loop mechanically
- **Drip loop:** A loose loop in the hose 6–12 inches from the gun prevents solution from running back into the pack connectors if the gun is held above pack height

---

## Multi-head wands

### Dual-gun configuration

The standard pack supports **two independent gun channels**, each with its own XT30U connector. This allows:

- **Two single-head guns** (one per channel) for dual-wielding
- **Two multi-head guns** (up to 3 heads each) for coordinated spray
- **One multi-head gun** and one backup / spare gun on a shared channel

Each channel supports up to **15 A continuous** (XT30U rating); shared channel operation is not recommended at full power.

### Umbilical brick (printed)

Each umbilical has a **3D-printed ASA (or PETG) brick** at the gun end (two in all). It is the only printed umbilical part; the pack end plugs into the cup's port cluster. The earlier combined-wand connector block and pump/hose/tether block are superseded.

| Feature | Detail |
|---|---|
| **Electrical** | XT30U dropped into an open-top pocket and strapped with a zip tie through the slots beside it |
| **Fluid** | The tube runs in a groove, held by a narrow zip tie |
| **Mechanical** | The 16 AWG pair runs in its own groove; the paracord tether ties through the outer hole and runs back to the U-tunnel boss on the cup; the inner hole ties to the gun |
| **Material** | ASA or PETG, printed on the A1 (with ASA: brim and draft shield) |

### Wand configuration options

For the target festival the plan is option 2 below, with each gun a dual-head gun.

1. **Single wand + two heads (3 + 3 split):** One print-molded wand body holds two XT30U sockets and connects to two parallel three-head gun blocks. Total: 6 heads, each channel at ~10.9 A at 6.4 V (typical), leaving margin below 15 A limit.
2. **Dual handheld guns:** Joey wields one gun per hand, each connected to a single XT30U umbilical. Simplest configuration; no wand block needed.
3. **Extended wand (future):** A long stick-mounted wand supporting 4–8 heads in a row. This requires XT60H (20 A) connectors on pack channels; not supported with current XT30U connectors without redesign.

---

## Head capacity limits

### Per-channel limits

Each XT30U connector is rated for **15 A continuous**. At the nominal pack voltage under load (~6.4 V), this provides:

- **Power ceiling per channel:** 15 A × 6.4 V = 96 W
- **Typical three-head gun power:** ~35 W at full voltage (varies widely depending on motor condition and solution viscosity)
- **Headroom:** Supports 2–3 standard heads per channel with margin

### System-wide limits

The pack has a **30 A manual-reset main breaker** protecting the entire system. Under sustained full power across both channels:

- **Combined current:** up to 25 A (typical; some headroom below 30 A limit)
- **Combined power:** 25 A × 6.4 V ≈ 160 W (within budget for 2S5P battery under moderate load)
- **Supported configuration:** 6 standard heads (3 + 3 split) at full power
- **the target festival estimate:** ~12 A with all 4 heads of the two dual-head guns firing (~6 A per channel); not measured

### Expansion ceiling

Future expansion to 8 heads or higher power is documented in [docs/16-roadmap-future-extensions.md](16-roadmap-future-extensions.md).

### Practical head limits

In practice, Joey's current builds support:

- **1–2 heads per gun:** Standard wrist or handheld mount; simple to balance and control
- **3 heads per gun:** Original test gun; maximum recommended for a single handheld wand without feeling unbalanced
- **6 heads total (3 + 3):** Dual-wand or dual-gun configuration; maximum current-limited support at 6.4 V nominal
- **Future totem (16+ heads):** Explicitly deferred; would require a separate pack with higher voltage/current capacity and its own independent BMS

---

## Gun teardown and qualification

For the target festival, strip the ~20 bubble guns Joey is picking up this week, pick 4 matched heads, and keep the spares. Record the teardown measurements: the gun/head mounts aren't designed yet and are drawn from them.

Before integrating a donor gun into the system, it must be qualified for:

1. **Electrical integrity:** Verify all motor connections are clean; solder any bad contacts; test at 5 V and at 8.4 V for 30 seconds and verify no burning smell or excessive heat
2. **Fluid path:** Pressurize the internal pump to ~1.6 psi (simulating a three-foot hose elevation) and leave off for 10 minutes—it must not drip from any joint (confirms the donor's internal check valve is functional)
3. **Mechanical function:** Spin the wand/bubble-maker by hand to verify smooth rotation; listen for grinding or binding
4. **Hose attachment:** Test the fluid connection point for compatible barb size (typically 6–8 mm barb for ID 3.5 mm hose); ensure no leaks under 2 psi

### Disassembly for modification

If the donor gun requires internal rewiring (bad contacts, additional bracing, or pump disconnection for custom operation):

1. Remove the toy's outer plastic shell (typically glued or screwed)
2. Note the original wiring layout with photos
3. Desolder or cut old battery contacts and replace with soldered XT30U pigtails
4. Verify all motor and pump wiring is secure; add solder bridges to any flaky connections
5. Reassemble with clear epoxy or plastic-safe adhesive in place of original glue
6. Retest at the electrical/fluid specifications above before field use

---

## Tracer cosplay integration

Joey is integrating bubble-gun heads into 3D-printed hollow shells for a Tracer (Overwatch) cosplay prop. This represents a special-case gun configuration that combines cosmetic integration with functional operation.

### Cosplay shells—white 3D-printed

| Spec | Detail |
|---|---|
| **Printers** | Creality K2 Plus (350 × 350 × 350 mm) and Bambu Lab A1 (256 × 256 × 256 mm) for large parts |
| **Material** | Standard FDM resin or FDM PLA; printed in white for visibility and paint prep |
| **Shell files** | L1, L2, L3, L6, R1–R6 (10 armor/gun shell components, all printed and complete as of 2026-08-06) |
| **Status** | All shells printed; awaiting bubble-gun head installation |
| **Finishing** | Paint, weather, and integrate LED accents (2 m COB light blue LED strip, integrated into gun shells for visual effect during performance) |

### Head integration inside shells

The Tracer gun shells are hollow with an internal cavity designed to accept:

- **One or two bubble-gun donor heads** (exact count TBD based on shell size and wand geometry)
- **Wetting manifold and hose exit** toward the cosplay front (not visible when worn)
- **XT30U electrical connector** on the back or side (hidden by costume, leads to pack-mounted wand)
- **Strain relief and mechanical anchoring** to prevent the head from shifting inside the shell during dancing or falls

### Assembly procedure

1. **Test-fit the head:** Insert the donor gun head into the shell cavity and verify fit and wand alignment
2. **Locate barb fittings:** Mark the internal fluid entry point (where the hose will barb onto the wetting manifold)
3. **Drill/resize holes:** Add holes for the XT30U connector exit (back/side) and fluid hose exit (front or wetting point)
4. **Mount the head:** Use print-in-place clips or epoxy to secure the head inside the shell; ensure the wetting manifold can reach the hose connection point
5. **Route hose and power:** Feed the umbilical through the back of the prop into the pack
6. **Cosmetic finish:** Paint and detail the outside of the shell; integrate LED strips along edges for visual effect
7. **Field-test:** Fire the gun briefly to verify fluid and electrical connections under load. The gun operates at raw 2S pack voltage (6.0–8.4 V); start with a short burst to confirm no fluid leaks at the new joints

### Performance considerations

- **Weight and balance:** Tracer shells plus integrated guns are heavier than handheld wands; use the cosplay backpack for stable mounting, not a belt
- **Spray direction:** The gun heads inside shells will spray outward perpendicular to Joey's body; verify spray doesn't hit the wearer's face or costume
- **Solution management:** Prevent solution from pooling inside the hollow shells; add drainage holes or sealed internal drip trays
- **LED coordination:** The COB blue LED strips provide visual effect synchronized with the spray (LEDs + bubble spray = enhanced performance photography)

---

## Open items

- **Exact donor gun models:** Joey is picking up ~20 bubble guns this week to strip; the 4 matched heads for the two dual-head guns are chosen at teardown
- **Gun/head mounts:** Not designed yet; they need the teardown measurements
- **Motor current by head type:** Individual motor current draw for various common donor heads has not been systematically measured; field measurements during commissioning will establish accurate per-head budgets
- **Tracer shell final integration:** Exact hose routing, LED placement, and drainage design for the Tracer cosplay guns will be confirmed during build-out in October 2026

---

## Related docs

- [docs/01-overview-and-requirements.md](01-overview-and-requirements.md) — System goals and performance targets
- [docs/04-power-system.md](04-power-system.md) — Battery, BMS, breaker, and 2S pack voltage specifications
- [docs/05-fluid-system.md](05-fluid-system.md) — Pump, hose, and reservoir design
- [docs/07-pcb/overview.md](07-pcb/overview.md) — ACS758 current sensing and pump trigger logic
- [docs/parts/ORDER_LEDGER.md](parts/ORDER_LEDGER.md) — XT30U connectors, paracord, hose, and sleeving part references
