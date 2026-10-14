# BubbleLink printed parts

Parametric OpenSCAD sources are in `src/`; ready-to-slice STLs are in `stl/`. Rigid parts are PETG and the four seals and boots are TPU. Nothing needs supports.

The whole pack, apart from the bladder, is one upright **stick**: outside about **99 × 78 × 207 mm** (3.9 × 3.06 × 8.15 in). It stands beside the bladder in the bag. Two umbilicals (hose + XT30U cable + paracord each) leave from the bottom. That makes it easy to move into a different bag. Every model is designed around the parts in `docs/parts/ORDER_LEDGER.md` and the BubbleLink CTRL v1.2 board on order.

```
   ┌──── cap ────┐   control head: voltmeter, USB-C, LEDs, PRIME; PCB hangs under it
   │ BATT │ BRK  │   TPU ring seals against the tube wall; 2× M3 keep it on
   │ 2S5P │ BMS  │   ← the sled slides out of the top
   │      │bucks │
   ╞══ bulkhead ═╡   cables pass through a slit TPU grommet
   │  pump cup   │   wet side: pump, tees, check valve, bypass clamp; drains
   └──┬───────┬──┘   4× M3 from underneath
     L        R      umbilicals, bladder feed, service cables out the floor
```

**Hardware:** 6× M3 screws (2× **10 mm** for the cap, 4× **12 mm** for the cup) with 6 nuts glued into printed pockets. Also zip ties, glue (CA/hot glue/silicone), a strip of 1 mm foam, electrical tape, and a soldering iron for heat-staking the PCB. The cup screws sit about 55 mm up their columns, so you need a long, narrow screwdriver.

## Print order

| # | STL | Copies | Material | Printer | Notes |
|---|---|---|---|---|---|
| 00 | `00_fit_coupon` | 1 | PETG | A1 | Print first. Sets the cell-bore and connector clearances. |
| 01 | `01_cell_holder_MID` | 1 | PETG | either | |
| 02 | `02_cell_holder_TERM` | 1 | PETG | either | |
| 09 | `09_slide_clamp_x3` | 3 | PETG | A1 | Bypass restrictor and both channel shutoffs |
| 10 | `10_umbilical_brick_x4` | 4 | PETG | A1 | Strain relief at both ends of each umbilical |
| 20 | `20_stick_tube` | 1 | PETG | either (139 mm tall) | Bulkhead on the bed. **Measure the breaker first** (below). |
| 21 | `21_stick_cap` | 1 | PETG | either | Plate on the bed |
| 22 | `22_stick_sled` | 1 | PETG | either | Base on the bed |
| 23 | `23_stick_cup` | 1 | PETG | either | Floor on the bed. **Measure the pump first.** |
| 24 | `24_stick_prime_plunger` | 1 | PETG | A1 | Head on the bed |
| 30 | `30_TPU_cap_ring` | 1 | TPU | A1 | The cap seal. Flat, slow. |
| 31 | `31_TPU_grommet_lower` | 1 | TPU | A1 | Bulkhead grommet, cup side |
| 32 | `32_TPU_grommet_upper` | 1 | TPU | A1 | Bulkhead grommet, dry side (a mirror image of the lower half) |
| 33 | `33_TPU_prime_boot` | 1 | TPU | A1 | Optional: you can also prime by pulling a trigger |
| 34 | `34_TPU_screw_washer_x2` | 2 | TPU | A1 | Seals the two cap screw holes |
| 35 | `35_TPU_breaker_membrane` | 1 | TPU | A1 | Glued over the breaker window, so you can trip and reset it through the wall |

The older wide-box design (`dry_core.scad`, `pump_module.scad`, `port_insert.scad`) is superseded and no longer built. **Don't print those.**

**Not designed yet:** mounts for the dual-head guns. They need the teardown measurements.

## Measured parts (Joey, tape measure, 2026-10-14)

The stick is built around these measurements, with clearance added. Every board sits in an open compartment and is held with a zip tie; none of the mounting holes are used.

| Part | Measured | Where it goes |
|---|---|---|
| Breaker | Inline type: studs at both ends; a 1⅝ in square plate in the middle with a reset lever and a push-to-trip button; 4 in long, 1⅝ in thick; plate holes 1¼ in apart | Stands upright behind the cross panel with its controls facing the right wall, 2 mm behind a window. Hangs by two zip ties through its plate holes and the spine. Its top is at 106 mm, well under the hung PCB. |
| BMS | 2½ × 1⅞ × ¼ in | Stands on edge in a 7 mm slot along the back wall, next to the battery's TERM face |
| Buck A, Buck B | 1 in along the port, 5/16 in thick | Compartments on the front of the cross panel. **Width not measured; assumed 17 mm (⅝ in).** |
| ACS758 | 1½ × ¾ × ⅛ in | Compartment on the front of the cross panel, above Buck A |
| USB-C charger | 1½ × 11/16 × ⅜ in | Under the cap's CHG window, receptacle up |
| Voltmeter | bezel about 1 5/16 in, body a hair over 1⅛ in, about 1 in deep or a bit more | 29.2 mm hole in the cap, with 30 mm of depth allowed above the battery |
| G528 pump | 2 × 1¾ × 1½ in at its thickest | 52 × 46 mm pocket in the cup, strapped down across it |

**Still unknown:** the bucks' width (17 mm is assumed) and exactly where the breaker's controls sit on its plate. The window is 34 × 40 mm, centred on the plate.

**Solder the bucks' outputs directly** (Buck A to J1; Buck B to a cut USB cable for the backpack). There's no room for USB plugs inside.

## Fit settings (`src/params.scad`)

- **Cell rings (.65 / .80 / .95):** pick the tightest ring a 25R cell slides into by hand and set `cell_bore` to 18.65, 18.80 or 18.95.
- **XT30U pockets (+.2 / +.3 / +.4):** pick the snug one and set `fit_clear`.

Then rebuild with `./build.sh /path/to/openscad`. It regenerates every STL in a few seconds.

## Part notes

### The stick
- **Orientation:** standing upright beside the bladder.
  - The back (y = 0) goes against your back.
  - The battery is on the left, at the top of the dry side. That's the highest and driest spot, and the heavy part rides high.
  - Every cable leaves through the bottom.
- **Sled:** a central spine with a cross panel.
  - **Battery:** stands left of the spine, on the base, with the **TERM face (pack + and −) toward the back**. That gives the 12 AWG leads a 2.65 mm gap, plus the holder's 2 mm window recess. The tube walls hold it in once it's inside, so on the bench, hold it to the spine with tape or a rubber band.
  - **Wire routes:** the spine stops 6 mm short of the front and back walls, leaving vertical lead channels. The cross panel has a 10 × 30 mm wire pass at its right end, low down, from the breaker/BMS bay to the bucks/ACS758 in front.
  - **Breaker:** stands upright right of the spine, behind the panel. Its reset lever and trip button face the right wall, 2 mm behind the window. Run one zip tie through each plate hole and the tall slot in the spine behind it. Leave about 1.5 mm under the bottom stud for its lug. The gap between the spine and the breaker is a wire channel.
  - **BMS:** stands on edge in the slot along the back wall. The battery's TERM-face leads reach it directly through the channel behind the spine.
  - **Buck A, Buck B, ACS758:** drop into the three compartments on the front of the panel and get a zip tie each. Wires to the breaker/BMS side go through the pass at the panel's right end.
  - **Slots:** the spine and panel have cross-shaped zip-tie slots, plus two wire pass holes for the battery leads.
  - **Holding it down:** the cap's two ribs press the cell holders (add 1 mm foam to the ribs), which pins the sled onto the bulkhead. No screws.
- **Cap (control head):**
  - **PCB:** hangs under the cap, component side up, 22 mm below the plate. Push it onto the four pins and heat-stake the tips (heads under 5 mm, because J2 sits 2.7 mm from H3).
  - **LEDs:** LED1–3 show through 0.6 mm skin windows: no holes, so it stays sealed. Use a light-coloured PETG for the cap. Black won't pass the light.
  - **PRIME:** a plunger in a sleeve. Its head floats under the TPU boot with 1.7 mm of travel, and the tip stops 0.3 mm above SW1. Glue the boot down around the bore.
  - **RV1 and RV2:** adjust through two small windows with a 2 mm screwdriver. Cover the windows with electrical tape afterwards.
    - Each window sits over its 3296W adjusting screw, which is at the pin-1 end.
    - **Solder both trimmers with pin 1 on the square pad.** If one goes in reversed, its screw ends up under the PRIME boot.
  - **Voltmeter:** the body drops through the 29 mm hole and gets glued around its bezel.
  - **USB-C charger:** glued under the CHG window, receptacle up. Run its output to the BMS P+/P− through an XT30 pair, so the cap stays removable.
  - **Wires to the cap:** J1, J2 and J3 are XH plugs. Leave enough slack to lift the cap and set it beside the stick.
- **Seal:** stretch the TPU ring into the cap skirt's groove (about 80% fill, 13% squeeze). The tube's rim has a 0.6 mm lead-in so the ring doesn't catch on the way in.
  - Two M3 × 10 screws go through the front and back walls, **each with a TPU washer under the head**, into nuts glued in the cap's slots. The screws only keep the cap on; the washers keep water from following the screw holes past the ring.
  - To get the cap off, lever it up with a flat screwdriver in the notch on the left edge.
  - **Wet-test the cap** before trusting it. This is a starting geometry for a TPU seal, not a proven one.
- **Bulkhead grommet:** two TPU halves. Each has its own hole per conductor, sized 0.2 mm under the wire OD.
  - Holes: both 16 AWG gun pairs, both pump leads, both 12 AWG XT60H loop wires, and the LED-backpack USB cable.
  - **Cut a slit with a knife** from each hole to the nearest long edge, so the cables lay in.
  - Push the lower half up from the cup side and the upper half down from the dry side; they meet inside the slot.
  - It's a splash baffle, not a watertight feedthrough. Once the wiring is final, run a thin bead of neutral-cure silicone over its top face. The silicone peels off when you need to pull the sled.
  - Give every cable a drip loop below the cup, so water runs off the low point rather than up the cable.
- **Venting and heat (not verified):**
  - The tube only breathes incidentally, through the grommet slits and the cap ring.
  - I haven't verified pressure relief if a cell fails, or charging temperatures inside the closed tube. At 4 A the charger alone may give off around 3–4 W.
  - Check charger and BMS temperatures on the first enclosed charge. Until then, charge with the cap off.
- **Turning it off:**
  - **Breaker trip button (OFF switch):** press it through the membrane on the right wall. Wire the voltmeter after the breaker, so tripping it turns off everything except the BMS: bucks, PCB, voltmeter and guns.
  - **XT60H loop (full disconnect):** it runs out through the grommet and the cup's service hole. Pulling it isolates the battery completely. Wrap the XT60H pair and the USB plug, because they sit in the wet zone below the stick.
  - **Idle drain:** unplug the loop for storage.
    - The BMS stays on the battery either way. Its quiescent draw is typically tiny, but I haven't measured this one.
    - The voltmeter's idle draw isn't measured either. Small LED meters like this typically draw tens of mA. At 20 mA, the 12.5 Ah pack would take weeks to drain, so overnight it doesn't matter.
    - Check it once with a multimeter on the mA range.
- **Cup:**
  - **Pump:** sits in a 52 × 46 mm pocket on the left of the floor, strapped down with zip ties through the slots on either side. Drains are under it.
  - **Fittings:** the right-hand strip (x 64–94) holds three tees, the check valve and the bypass slide clamp, strapped to the six floor slots. The 70 mm clamp runs front to back.
  - **Holes:** umbilicals leave through the two 13 mm holes, and the bladder feed, LED-backpack USB and XT60 loop use the 20 mm service hole. All have chamfered edges so the hoses don't rub.
  - **Mounting:** four M3 × 12 screws go up from underneath through the corner columns into nuts glued into the bulkhead's underside.
- **Plumbing:** `bladder → inlet tee → pump → outlet tee 1 → outlet tee 2 → gun 1 / gun 2`. From tee 1's side branch: `→ slide clamp → check valve (arrow toward inlet) → inlet tee`. That's three tees in total, so check the assortment has three.

### Cell holders (MID and TERM)
- Ten cells in two offset rows of five, at 19.9 mm pitch. That leaves a 1.6 mm wrapper gap and keeps the 26 mm nickel tabs reaching both cell centres.
- **Orient the rows in opposite directions.** Row A goes + toward one end and row B − toward it. If every cell faces the same way, it's 10P, not 2S5P.
- **MID** caps the series end: every tab on that face is the midpoint.
- **TERM** carries the separate pack + and − buses. Keep the two rows' strips apart, with fish paper between them.
- The holders are mirror images. If the A/B letters don't line up, rotate MID 180°.
- **In the stick**, the cell axes run front to back. The holder faces with the tabs press against the tube's front and back walls through fish paper.

### Slide clamp (×3)
- **Assembly:** lay the tube in the channel and slide the slider on from the open end, ridge down.
- **Operation:** slide toward the arrow to close.
  - The first ~8 mm goes from fully open (6.0 mm gap) to 2.4 mm.
  - The next 22 mm is fine adjustment (about 0.08 mm per mm).
  - It seals at 0.6 mm against the stop blocks.
  - The shallow ramp self-locks; wet-test that it holds.
- **Roles:** one is the bypass restrictor; two are channel shutoffs, one on each gun line.

### Umbilical brick (×4)
- One at each end of both umbilicals.
- **XT30U:** drop it into the open-top pocket and strap it with a zip tie through the slots beside the pocket.
- **Wires and tube:** the 16 AWG pair and the fluid tube run in their grooves, held by narrow zip ties.
- **Paracord:** the tether ties through the outer hole. The inner hole ties to the stick or the gun.

## Checks done on these files (2026-10-14)

- Every STL is watertight. All are single bodies except the clamp, which plates a body and a slider together. All sit at z = 0.
- `stick.scad` `part="assembly"` has placeholder blocks for the battery, breaker, PCB, voltmeter, charger, BMS zone, bucks/ACS zone and pump envelope.
  - Pairwise intersection checks, including the TPU parts in their installed positions, found no overlaps. The exceptions are intended: the heat-stake pins pass through the PCB holes, and the seal ring presses 0.25 mm into the tube wall.
  - The pump placeholder box overlaps the V-blocks and the two left screw columns. The real pump shape decides whether that's a real clash.
- Two independent reviews of the stick (2026-10-14, Claude and GPT-6 Astra) found real problems, now fixed:
  - the PRIME plunger had no travel,
  - the seal ring overfilled its groove,
  - the cap screw holes bypassed the seal and left only 0.7 mm of wall,
  - the trimmer openings and PRIME boot overlapped,
  - the cup screw had 0.19 mm of bottoming clearance,
  - the TPU grommet had an unsupported flange,
  - the battery leads had no route between bays,
  - the pump V-blocks left 6 mm for the pump head.
- I also took out a claim that the grommet vents a failing cell.
- The PCB feature positions come from the KiCad source.
- **None of these parts has been printed or test-fitted.**
