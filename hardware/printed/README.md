# BubbleLink printed parts

Parametric OpenSCAD sources are in `src/`; ready-to-slice STLs are in `stl/`. Rigid stick parts are **ASA** (see *Printing in ASA* below); the older cell holders, clamps and bricks can be ASA or PETG. The seals, the PRIME boot and plunger, and the cushions are TPU. Nothing needs supports.

All STLs + this guide are also zipped at (link removed) (STLs split into `stl/ASA/` and `stl/TPU/`). Those zips hold only what's still to print (the coupons already printed and checked are left out). Just the two 18.65 cell holders + the battery build steps are at (link removed)

The whole pack, apart from the bladder, is one upright **stick**: outside about **99.6 × 77.8 × 220 mm** (3.9 × 3.1 × 8.7 in) for the body including the cup and the PRIME guard bezel (the tube, cap and cup alone are 215 mm tall; the bezel adds about 5 mm on top). Across the two cap screw heads it is about **87 mm deep**: each screw stands 4.5 mm proud of the front or back wall (5.5 mm DIN 912 head, 3 mm tall, plus a 0.5 mm steel flat washer and a 1 mm TPU washer), at the very top of the walls, 5.2 mm below the rim. The tube is 98.8 mm wide, plus 0.8 mm for the raised BubbleLink lettering on its right-hand wall; the cap is 98.8 mm wide. It stands beside the bladder in the bag. Two umbilicals (hose + XT30U cable + paracord each) plug into ports on the cup's outer wall, and nothing exits underneath: the stick stands on its floor. That makes it easy to move into a different bag. The drip hoods stand 2.5 mm off the outer wall, so the stick is **101.3 mm (4.0 in) wide across the hoods**, and plugged connectors stick out further. Every model is designed around the parts in `docs/parts/ORDER_LEDGER.md` and the BubbleLink CTRL v1.2 board on order.

```
   ┌──── cap ────┐   control head: voltmeter, USB-C (CHG), power key (KEY), LEDs, PRIME; PCB hangs under it
   │ BATT │ BRK  │   TPU ring seals against the tube wall; 2× M3 keep it on
   │ 2S5P │ BMS  │   ← the sled slides out of the top
   │      │bucks │   LED 5V: USB-A port through the tube's outer wall
   ╞══ bulkhead ═╡   gun pairs and pump leads pass through a slit TPU grommet, silicone on top, drip skirt below
   │  pump cup   │   wet side: pump, tees, check valve, bypass clamp; drains
   └─────────────┘   4× M3 from underneath; gun 1 and 2 ports and paracord tie-offs on the outer wall, IN on the front wall
```

**Renders:** `renders/` has 10 views: 1 every way in and out (the port map), 2 cap top, 3 and 4 cap-off cutaways (front, back), 5 cap underside, 6 cup interior, 7 bulkhead underside, 8 PRIME section, 9 gun power and hoses (`9_gun_power_and_paracord.png`: red is gun 1, orange gun 2, yellow paracord) and 10 gun port close-up (`10_gun_ports_closeup.png`).

**Hardware** (all of it from the HVAKHVA 304 stainless DIN 912 hex socket-head kit: M3 × 6/8/10/12 screws, 130 M3 nuts, M3 flat and lock washers; none of the M4/M5/M6 parts are needed):
- **2× M3 × 10 socket head** (cap retention), each with an M3 **flat** washer on top of the TPU washer (part 34) under the head. The steel washer spreads the head load so the TPU isn't cut.
- **4× M3 × 12 socket head** (cup), each with an M3 **split lock** washer under the head, as vibration protection for the jumping.
- **6× M3 nuts:** 4 in hex pockets in the bulkhead floor, dropped in from the dry side, and 2 in slots in the cap's nut blocks, open on the underside. The nuts carry the threads (nothing self-taps into plastic; all clearance holes are 3.4 mm), so glue each one in.
- **No anaerobic threadlocker** (Loctite 242/243 and similar) near ASA: it can crack ASA and ABS. If you want something on the threads, a tiny drop of CA on the screw tip is the plastic-safe option.
- **Tool:** a 2.5 mm hex key (M3 DIN 912), long enough to reach about 46 mm up the cup columns.
- For the power key: one XT60H male and one XT60H female from the XT60H pairs on hand (plus one more pair inline on the key leads, so the cap comes off; see the cap-to-sled harness), a short length of 12 AWG, hot glue, and narrow zip ties for the connector keepers (key socket and each XT30U well). For soldering the battery tabs: a big chisel tip, flux paste, fine sandpaper and isopropyl alcohol (see *Cell holders*). Also zip ties, glue (CA/hot glue/neutral-cure silicone), clear hot glue or UV resin for the LED windows, electrical tape, and a soldering iron for heat-staking the PCB. There is no foam in this build; the TPU cushions (parts 36-38) replace it, and TPU plugs (39, 40, 41) close the trimmer windows, the USB-C port and the LED 5 V port; two TPU port caps (42) close unused gun ports, and the key blank and gasket (43, 44) seal the KEY socket. Optional: a paint pen or acrylic to fill the engraved cap labels.
- Spares: the kit has plenty (30 of each screw length, 130 nuts, about 300 washers).

## Print order

**Sequence:** the five coupons (00) first, then the tube (20), sled (22) and cell holders (01, 02). **Measure** the tube rim height (Zt = 156 mm above the bulkhead's top face, plus the 3 mm bulkhead) and the assembled battery block height (113.0 mm nominal with the 18.65 bore). The coupons only capture XY shrink; Z shrink on a 156 mm tall ASA tube is about 0.3-0.5 mm and they don't see it. Only then print the cap (21) and the battery pads (36). If the measured stack differs from nominal by more than 0.2 mm, edit `bp_ov` (nominal 0.6) in `stick.scad` and rebuild only the cap and pad. The rest can be printed in any order.

| # | STL | Copies | Material | Printer | Notes |
|---|---|---|---|---|---|
| 00 | `00_fit_coupon` | 1 | ASA | K2 (or A1 with draft shield) | **Print first**, in ASA. Sets the cell-bore and connector clearances. |
| 00 | `00_stick_coupon_rim` | 1 | ASA | K2 Plus | **Print first.** 19 mm slice of the tube rim with a cap-screw hole. |
| 00 | `00_stick_coupon_skirt` | 1 | ASA | K2 Plus | **Print first.** Matching slice of the cap skirt: seal-ring groove, nut slot and screw hole. Flipped plate-up for printing. |
| 00 | `00_stick_coupon_nut` | 1 | ASA | K2 Plus | **Print first.** Bulkhead corner with a cup-screw hex nut pocket. |
| 00 | `00_stick_coupon_ports` | 1 | ASA | K2 Plus | **Print first.** A 2.4 mm wall with an XT30U well, a hose hole, a USB-A window with counterbore, and an XT60H key socket with its lip. |
| 00 | `00_stick_coupon_cap` | 1 | ASA | K2 Plus | **Optional.** The part of the cap with the voltmeter hole and the charger slot, plate down (about 34 × 54 × 33 mm). Check the real voltmeter and charger in it before printing a whole new lid. |
| 01 | `01_cell_holder_MID` | 1 | ASA or PETG | K2 | |
| 02 | `02_cell_holder_TERM` | 1 | ASA or PETG | K2 | |
| 09 | `09_slide_clamp_x3` | 3 | ASA or PETG | A1 (brim, draft shield if ASA) | Bypass restrictor and both channel shutoffs |
| 10 | `10_umbilical_brick_x2` | 2 | ASA or PETG | A1 (brim, draft shield if ASA) | Strain relief at the gun end of each umbilical (no brick at the pack end) |
| 11 | `11_hose_adapter_8.5mm` | 1 | ASA or PETG | A1 or K2 (brim) | Straight barbed reducer: bladder drinking tube (8.5 mm barb) to the 3.5 × 5.5 mm IN pigtail (4.8 mm barb). Big barb down, 100% infill, zip-tie both ends. `_8.0mm` and `_9.0mm` are looser/tighter alternates; collar notches mark the size (1 = 8.0, 2 = 8.5, 3 = 9.0). 3MF copies carry explicit mm units. |
| 20 | `20_stick_tube` | 1 | ASA | K2 Plus (159 mm tall) | Bulkhead on the bed. 99.6 mm wide with the raised lettering. |
| 21 | `21_stick_cap` | 1 | ASA | K2 Plus | Plate on the bed |
| 22 | `22_stick_sled` | 1 | ASA | K2 Plus | Base on the bed. **Check the breaker's lug clearance first** (below). The base has a notch at the front-right corner so it slides down past the Buck B shelf; **a sled printed before 2026-10-16 needs that corner cut off** (Joey used wire cutters). |
| 23 | `23_stick_cup` | 1 | ASA | K2 Plus | Floor on the bed. **Measure the pump first.** |
| 24 | `24_stick_prime_bezel` | 1 | ASA | A1 (brim, draft shield) | Guard ring around the PRIME boot; exported top-down |
| 25 | `25_stick_grommet_skirt` | 1 | ASA | A1 (brim, draft shield) | Drip skirt under the bulkhead grommet; lip on the bed |
| 26 | `26_stick_power_key` | 1 | ASA | A1 (brim, draft shield) | The power key's grip, with a lanyard hole. The XT60H female and its U-loop are hot-glued into it. |
| 27 | `27_stick_pcb_spacer_x6` | 4 (+2 spares) | ASA | K2 Plus or A1 (brim) | Drops the PCB 5.8 mm so the LEDs clear the light tunnel. Socket on the bed, pin up. Each one slips over a cap post's stake pin (CA it there); the board goes on the spacers' pins and gets heat-staked as before. |
| 30 | `30_TPU_cap_ring` | 1 | TPU | A1 | The cap seal. Flat, slow. |
| 31 | `31_TPU_grommet_lower` | 1 | TPU | A1 | Bulkhead grommet, cup side |
| 32 | `32_TPU_grommet_upper` | 1 | TPU | A1 | Bulkhead grommet, dry side (a mirror image of the lower half) |
| 33 | `33_TPU_prime_boot` | 1 | TPU | A1 | Seals the PRIME bore; its flange is clamped under the bezel |
| 34 | `34_TPU_screw_washer_x2` | 2 | TPU | A1 | Seals the two cap screw holes |
| 35 | `35_TPU_prime_plunger` | 1 | TPU | A1 | Head on the bed. TPU so a hard press can't load the PCB. 5.8 mm longer since the PCB spacers (2026-10-20): **reprint one printed before then**, or PRIME won't reach SW1. |
| 36 | `36_TPU_battery_pad_x2` | 2 | TPU | A1 | Compliant pad over the end of each of the cap's two battery ribs. Print slow, opening up. |
| 37 | `37_TPU_pump_mat` | 1 | TPU | A1 | 2 mm mat under the pump, 8 drain holes, drain grooves on the underside |
| 38 | `38_TPU_shim_strip_set` | 1 | TPU | A1 | One STL with six 5 × 30 mm strips: 2× 0.6, 2× 1.0 and 2× 1.5 mm thick. Cut to length and tuck where a board rattles. |
| 39 | `39_TPU_trimmer_plug` | 1 | TPU | A1 | One plug closes both trimmer windows. Plate down. |
| 40 | `40_TPU_usbc_plug` | 1 | TPU | A1 | Fills the CHG window; pull it to charge. Flange down. |
| 41 | `41_TPU_usbA_plug` | 1 | TPU | A1 | Fills the LED 5V counterbore and window; pull tab down. Flange down. |
| 42 | `42_TPU_gun_port_cap_x2` | 2 | TPU | A1 | Closes an unplugged XT30U well. Flange down. |
| 43 | `43_TPU_key_blank` | 1 | TPU | A1 | Closes the KEY socket when the key is out. Tie it to the key's lanyard. |
| 44 | `44_TPU_key_gasket` | 1 | TPU | A1 | Glued under the key grip; presses on the cap top round the socket when the key is home. |
| 50 | `50_head_gauge_x5` | 1 | ASA or PETG | any | Five 4 mm C-rings, ID 48.5 / 49.25 / 50.0 / 50.75 / 51.5 mm (1-5 bumps), for the donor blower head's front wheel ring (photo estimate 49.5). Slip each over the face; the smallest one that goes on without its gap spreading is ring A's size. Set `ringA_d` in `src/blower_head.scad` and rebuild part 51. |
| 51 | `51_head_collar_test` | 1 | ASA or PETG | any | Test mount for a donor blower head: a C-collar over the front 9 mm of ring A, a 2 mm lip on the stationary rim, crush ribs, a 24 mm gap for the yellow-gear housing (widened after the first print, which only fitted upside down), a notch for the hose-barb bracket, and a flat pad with two zip-tie tunnels. Lip on the bed, no supports. `REF_blower_head.stl` is the head reference model (not for printing); `renders/13_blower_head_photo_vs_model.png` compares it with the photos. |
| 60 | `60_dock_barb_coupon` | 1 | ASA | any | **Print before any dock.** Four head-hose barbs: 2.8 / 2.9 / 3.0 / 3.2 mm (1-4 dots), each with a 0.25 mm ridge step. Push the head hose onto each; pick the biggest one that still goes on by hand and set `out_peak` in `src/gun_dock.scad` (default 3.0) before printing docks. |
| 61-68 | `6N_gun_dock_Nhead` | 1 per gun | ASA, 100% infill (or 6 walls) | K2 Plus | The standard umbilical panel for a gun shell; N = heads fed (61 = 1 head ... 68 = 8). **Face on the bed, no supports.** Outside: XT30U window, recessed 4.8 mm hose barb, carabiner bar. Inside: N × 3.0 mm barbs. Clear the 1.2 mm outlet bores with a 1.2 mm drill or a guitar string if they print shut. See *Gun dock* below. |
| 69 | `69_dock_mount_plate` | as needed | ASA | any | A 2.4 mm "shell wall" with the standard dock hole and four M3 holes. Use it to test-fit a dock, or to mount one on a gun that has no printed shell yet. Outer face on the bed. |
| 00 | `00_duo_test_main`, `00_duo_test_cover` | 1 each | ASA (purple) | any | **Print first.** The Duo's trigger housing region from each half: check the switch fit, the nut stack, the trigger and its stop, and where the button bottoms out. Hold them together with rubber bands. |
| 70, 72 | `70_duo_main_L`, `72_duo_main_R` | 1 per gun | ASA (purple) | A1 or K2 Plus | **Duo** main half with the grip and the umbilical dock built in (see *Duo* below). L = left gun, R = its mirror image; a pair is one of each. Grip-side face down, no supports. |
| 71, 73 | `71_duo_cover_L`, `73_duo_cover_R` | 1 per gun | ASA (purple) | A1 or K2 Plus | Duo cover half. Outer face down. |
| 74 | `74_duo_trigger` | 1 per gun | ASA (purple) | any | Duo trigger. Lies flat. |

That is 32 STLs: 5 older parts (the brick file is now x2), 5 stick coupons (one optional), 7 rigid stick parts and 15 TPU parts (each file counts as one STL, whatever the copy count). On top of those: the three hose adapters (11), the two donor-head test parts (50-51), the ten gun-dock files (60-69), and the Duo files (70-74). `REF_blower_head.stl` is a reference model, not a print.

The older wide-box design (`dry_core.scad`, `pump_module.scad`, `port_insert.scad`) is superseded and no longer built. **Don't print those.**

## Gun dock

Every gun shell gets the same dock (`src/gun_dock.scad`), so any umbilical fits any gun. **No supports anywhere:** every face of parts 50, 51 and 60-69 that isn't on the bed is 45° or shallower, with no bridges (the socket ceiling, the carabiner tunnel roof, the collar and the zip-tie tunnels are all 45°, and the manifold channels are teardrops). `python check_stl.py 5 6` re-checks them after a rebuild. Outside, it is a flat strip **65.5 × 20 mm**, flush with the shell. It reaches **24 mm** into the gun, plus 7 mm of barbs. Keep the space in `gun_dock_envelope()` clear inside the shell.

- **Docking a gun:** clip the carabiner onto the bar and lock it, plug the umbilical's XT30U female into the window, then push the hose into the socket until it bottoms on the barb. To undock, do the same in reverse; nothing gets tied. The carabiner lives on the umbilical: tie a fixed loop in the paracord's gun end (figure-8 on a bight) once, and leave the carabiner on it. **Keep that loop shorter than the hose and wire tails**, so a dropped or yanked gun pulls on the bar, never the XT30U or the hose.
- **Power:** solder the gun's XT30U **male** first, then push it in from the back until its shroud stops on the 0.8 mm lip at the face. Pot it with hot glue from behind. The lip carries the unplugging pull; the glue only stops it being pushed in.
- **Fluid:** one 4.8 mm inlet barb (the size that fits the 3.5 × 5.5 umbilical silicone), with a long 3.2 mm lead-in. It sits recessed in a socket so a drop can't snap it off. It feeds N 3.0 mm outlet barbs inside: 1 = straight, 2 = Y, 3-8 = manifold. Dots on the back face count the heads.
- **Carabiner:** the pocket fits a carabiner rod up to **8 mm** thick; the bar is 7 × 6 mm, so the gate has to open more than 7 mm. For a bigger carabiner, set `cb_rod` (and `bar_w`/`bar_t` if the gate is small) and rebuild. The bar is good for roughly 1 kN in ASA.
- **In a shell:** design the wall at the dock **2.4 mm** thick and subtract `gun_dock_hole()`. That is the face outline plus 0.2 mm, with a 45° × 1.5 mm chamfer on the inside edge. The dock goes in from inside, and its 45° collar seats in the chamfer, so an outward pull presses the collar into the wall (compression, not glue or screws). Acetone-weld it (both ASA) or run hot glue round the collar. Or `use <gun_dock.scad>` and union `gun_dock(n)` straight into a shell model. Coordinates: face at z = 0, +z into the gun, XT30U at the origin, hose at x = 12 (the same spacing as the umbilical brick).

## Duo (compact two-head gun)

`src/duo_gun.scad`, parts 70-74. Renders `renders/15_duo_gun_*.png` (rebuild with `python renders/duo_gun_views.py`). 3D parts viewer: (link removed) A small, rounded gun for two donor heads, made as a **left/right pair**. **Three printed pieces per gun, all purple, nothing else:** main half (with the grip and the umbilical dock built in), cover half, trigger.

- **Size:** body **88 long × 123.5 tall × 55.6 mm thick**; about 102 × 200 mm with the grip. The heads sit one above the other behind round windows, axes 57 mm apart, each turned 20° about its axis.
- **Shell:** split on the centre plane through both head axes and **glued shut**. The **main half** (70/72) carries everything: the grip (solid, half the gun thick, flush with its face), the umbilical dock, the switch bulkhead, half the trigger housing and one pivot peg, the head sleeves with crush ribs, and the pegs. The **cover half** (71/73) is the other side, with the other pivot peg. The switch, its bores and the trigger slot sit on the seam plane, so both halves print outer face down with no supports. Two glue pads (plates that meet face to face, on posts fused to the walls) add area to the rim, and a 4 mm peg on each main-half pad drops into a hole in the cover's pad.
- **Heads:** ring A's face sits on the 2 mm lip of a 3.4 mm front wall. The main half's sleeves have three crush ribs per head whose tips just touch the modelled ring. The cover half's sleeves have no ribs and **0.8 mm of clearance**, so the cover closes even if a ring is a little bigger than modelled. Hot-glue the heads in. Each gear tab gets a 1 mm clearance pocket.
- **Switch:** a **Gardner Bender GSW-21** push-on/push-off maintained SPST (rated 8 A at 125 V DC; spec sheet: https://www.gardnerbender.com/-/media/inriver/GSW-21_SPEC.pdf). All sizes are from the spec sheet and checked against the photo: body 24.9 × 15.3 × 15.6, 15/32-32 bushing, 12.2 mm keyed panel hole, 10.3 mm button. It hangs on a full-width bulkhead inside the body, 45° down and forward, its button in a short housing just ahead of the grip. The nut pockets are generous: the hex nut pocket also takes a 5/8" nut, the knurled nut has 2 mm of room, and the switch body can sit 1.4 mm further back.
- **Fitting the switch:**
  1. Run the hex nut all the way down to the switch body, and the knurled nut on loosely.
  2. Lay the switch in the main half, with the bulkhead half-plate between the nuts, the key tab in the keyway and the leads toward the open side.
  3. Spin the knurled nut snug.
  4. Drop the trigger on its peg. Its nub should just touch the button tip. If the trigger sits pushed forward off the button instead, back the hex nut off a turn (0.8 mm) and re-snug.

  The cover's half of the bulkhead is 0.25 mm thinner each side round the hole, so it slides in between the nuts. If the real keyway isn't where the key tab is, trim the tab off: the body's pocket stops the switch turning anyway. Measure your hex nut: the design assumes 2.6 mm, and a thicker one costs push travel (see below).
- **Umbilical dock (built into the main half):** the standard gun dock's connections, down the back face. All of them stay in the main half and print without supports with the half lying on its outer face.
  - **XT30U window:** the male goes in from inside and stops on a 0.8 mm lip; the umbilical's female plugs in from behind. The pocket stands on edge with a 45° peak.
  - **Hose inlet:** a 4.8 mm barb, recessed in its socket. It points **45° toward the outer side**, so the umbilical hose comes in from behind and a little from the outside. A barb pointing straight back would stick out sideways, with nothing under it, as the half prints.
  - **Carabiner bar:** two openings with the bar between, and a tunnel behind it. The bar prints as an upright post, anchored at both ends, under a 45° roof.
  - **Outlets:** inside, two 3.0 mm outlet barbs point up out of the open half. Push the head hoses on from above before closing.
  - Same sizes as `gun_dock.scad`, so any umbilical fits. No part 62 needed.
- **Wiring:** XT30U + → switch → both motor + (parallel); XT30U − → both motor −. The 18 AWG leads leave the switch toward the cover side and bend toward the dock. The switch is rated 8 A, so fuse each gun at 8 A or less.
- **Trigger (74):** hangs in a slot on the seam and pivots on two **5 mm pegs**, one printed into each half (no pin), with root fillets and chamfered tips.
  - **Fit:** the main-side hole is 5.6 mm and locates the trigger. The cover-side hole is 6.2 mm, and both ends are countersunk, so the cover's peg finds its way in blind.
  - **Action:** its nub pushes the button cap directly, and the switch's spring pushes it back. A full pull (23.8°, about 8.4 mm at the finger) pushes the button **7.0 mm**. It latches at 5 mm (measured), reached at 16.5°, and 6.5 mm is reached at 22°.
  - **Stop:** at full pull, the back of the blade lands on a **stop boss** on the grip's front strap. The stop sits at finger height, so a hard squeeze goes into the grip, not through the pivot pegs.
  - **Margin:** if the switch ends up 0.5 mm further back (a thicker hex nut), it still pushes 6.5 mm.
  - **Glue:** a 1 mm moat round the slot and the button tip at the seam catches squeeze-out. Keep glue 5 mm clear of them, and try the trigger with the halves held by rubber bands before gluing.
  - **Loose when on:** with the switch on, the button stays partway in, so the trigger hangs loose until the next press.
  - **Floor:** the hub pokes 1.8 mm up through the floor. Being round, it plugs its own opening, so wires can't drop into the slot. A low hump on the floor wraps the button bore where it passes under.
- **Test pieces (00):** the trigger housing region of each half (switch, nuts, bulkhead, pegs, stop boss). Print these first in the real filament. They confirm the switch fits, the nuts tighten, the trigger swings and stops, and the button latches before it bottoms out.
- **One hand, two guns:** the left gun's grip is on its right, the right gun's on its left. The buttons latch, so switch both on, then hold the guns grip to grip: the grips make one 56 mm handle. Optional 6 × 3 mm magnets in the grip-side faces (two in the body, two in the grip) hold the pair together: **left gun north out, right gun south out.**
- **Checks:**
  - `python check_stl.py 7 00_duo`: watertight, one body, nothing over 45°.
  - `python check_duo_fit.py`: trigger kinematics, plus interference with manifold3d between the halves, heads (both hands), the XT30U male in its pocket, the head hoses on the outlets, switch (released, pushed and set back), nuts (5/8" hex, knurled nut loose), and the trigger at rest, at 6.5 mm and at full pull. It confirms both stops (`-v` shows the full-pull stop is the boss on the strap), and reports clearances and the thinnest walls (1.6 mm round the switch pockets). Everything is 0 except the head-hose model brushing the outlet barbs' bases (about 1 mm³).
  - `build.sh` runs `clean_stl.py` to drop a few stray zero-area triangles the shells' unions leave.
  - The head model is photo-measured: check the part 50/51 results before printing a full shell.

## Inputs and outputs

Every way in or out of the stick. Nothing exits underneath any more.

| Port | Direction | Where | Wet/dry | Connector | Protection | Label |
|---|---|---|---|---|---|---|
| Charge in | in | Cap top | dry | USB-C: the charger board's own receptacle, under a 0.8 mm web | TPU plug (part 40) | CHG |
| Power key | switch (in line with the + feed) | Cap top | dry | XT60H **male** potted in a 17.0 × 9.8 mm sleeve, 22 mm deep, under a 0.8 mm lip, with a rear zip-tie keeper; the key is an XT60H **female** with a short 12 AWG U-loop across its two cups, hot-glued into an ASA grip (part 26, lanyard hole) | Lip stops pull-out; keeper stops push-in; TPU key blank (43) closes the socket when the key is out; TPU gasket (44) under the grip when it is home | KEY |
| Controls and status | in / out | Cap top | dry | PRIME button (guarded), LEDs PWR / GUN / PUMP, voltmeter, trimmers RV1 / RV2 | Guard bezel and boot on PRIME; trimmer plug (part 39) | PRIME, PWR, GUN, PUMP, THR, DLY |
| LED 5 V out | out | Tube outer wall, mid-height (window centre y = 66.55, close to the front corner) | dry | USB-A: Buck B's own port, on a shelf on the tube's front wall, in (or right behind) a 14.0 × 6.6 mm window | 0.8 mm web, outside counterbore (17 × 9 mm) for the plug's overmold, drip hood above, TPU plug (part 41) in the counterbore | LED 5V |
| Gun 1, Gun 2 | out | Cup outer (+x, right) wall, one cluster each | wet | XT30U well (10.8 × 6.2 mm, pack side **female**), hose pigtail and paracord tie-off (details below) | Drip hood; TPU port cap (part 42) when unplugged; slide clamp closes the fluid side | 1, 2 |
| Bladder IN | in | Cup front wall | wet | Hose pigtail, 45 degrees down, joined to the bladder's factory tube with a reducer | None needed (it is a hose) | IN |
| Drains | out | Cup floor and walls | wet | 4 mm holes | None | none |
| Bulkhead grommet | internal | Tube floor | dry / wet divider | Two 16 AWG gun pairs and the two pump leads only | TPU grommet, silicone on top, drip skirt below | none |

**Gone:** the XT60H loop below the stick, the backpack USB cable out of the floor, the 20 mm service hole and the 13 mm umbilical exits. The stick stands on its floor.

**Power key**
- The panel side is an XT60H **male** in a 17.0 × 9.8 mm sleeve under the cap plate (the AMASS XT60H envelope is 16.4 × 9.2 mm, plus 0.3 mm per side), 22 mm deep, with the socket at `key_xy` [42, 52.0]. A 0.8 mm lip over its shroud stops it being pulled out.
- **Rear keeper:** thread a zip tie across the sleeve through its two slots, between the solder cups, push it up against the back of the connector body, then cinch it round the sleeve. It stops the key's insertion force from pushing the socket in. Hot glue only seals.
- Wiring: socket pin A is BMS P+ and pin B is the breaker input, so the key switches the + line only. The key's female bridges the two with its 12 AWG U-loop.
- Key in is ON. Key out is OFF: **all loads off; the battery stays connected to the BMS, the charger and one pin of the key socket.** Everything downstream (breaker, ACS758, both bucks, PCB, voltmeter, pump, guns) is off. For storage or transport, take the key out **and** put the key blank (part 43) in.
- The charger connects to BMS P+/P− **upstream** of the key, so charging works with the key out.
- **Key blank, part 43:** a TPU plug that closes the socket when the key is out. Tie it to the key's lanyard, so one of the two is always in.
- **Key gasket, part 44:** glue it under the key grip. It presses on the cap top round the socket when the key is home. Sand the grip or add a shim strip for 0.2-0.3 mm of squeeze.
- Water sitting in an open key socket only bridges P+ to the switched + (it can't short the battery), but keep the key or the blank in.
- Leave enough slack on the socket wires (12 AWG, soldered) to lift the cap and set it beside the stick.

**LED 5 V (USB-A)**
- Buck B stands on a shelf printed on the tube's front wall, in the corner by the outer wall (shelf top at z = 42, 45-degree underside, a lip 2 mm in front of the board, and two zip-tie slots so a tie goes over the board's top edge). Its PCB faces the front wall with a 2 mm gap, and it slides along the shelf until its USB-A receptacle sits in (or right behind) the outer wall's window, then gets the zip tie. The sled lifts out past it untouched.
- The window is 14.0 × 6.6 mm. It takes Buck B's USB-A receptacle shell (13.1 × 5.7 mm) and any plug. There is a 0.8 mm web, an outside counterbore (17 × 9 mm) for the plug's overmold, a drip hood above, and the label LED 5V below. The window centre is at y = 66.55 on the outer wall. **Check that the backpack cable's overmold fits the 17 × 9 mm counterbore.**
- Its two input wires (main + after the breaker, and P−) run from the sled to the tube with a 2-pin JST-XH plug, so the sled can come out. **Buck B is on the tube, not on the cap or the sled.**
- The backpack cable plugs straight into the buck's own port: no extension cable and no USB plug inside the stick. **Unplug the cable before lifting the sled.**
- The TPU USB-A plug (part 41) only fills the outside counterbore. It doesn't enter the window, because the receptacle may sit in it.
- **Measure Buck B (width and where its USB-A sits) before printing the tube.** The shelf assumes 25.4 × 17 × 8 mm with the receptacle centred on the 17 mm side.

**Gun 1 and Gun 2** (a cluster on the cup's outer wall each, with a drip hood and the engraved number 1 or 2 above it):
- **XT30U well** (10.8 × 6.2 mm: the AMASS envelope of about 10.2 × 5.6 mm plus 0.3 mm per side). It points 45 degrees down and out so it drains. Power always comes from a **female** so no live pins are exposed: the pack well holds the XT30U **female** (sockets); the umbilical's pack end is the **male**, whose shroud slides into the well around the female; the umbilical's gun end is a **female**, and the gun's input is the **male**.
  - To fit it, plug a spare male in as a jig, push the pair in from inside until the male's rim is flush with the outer face, then fill the well behind the female with hot glue (it pots the solder cups and centres the body).
  - **Rear keeper:** a zip tie across the sleeve between the female's solder cups, through two slots, pushed against the back of its body (do this with the cup off the stick). It carries the 12-34 N unplugging force, so the hot glue only seals and centres.
  - **Proof-test each port** by pulling the plugged umbilical at about 70 N (7 kg), with the paracord slack, before trusting it.
  - The mated XT30 pair is recessed in the well under a drip hood but is **not waterproof**. If you expect rain, add a short heat-shrink boot over the umbilical's male and wires.
- **Hose pigtail.** 60-80 mm of 3.5 × 5.5 mm silicone leaves through a 6.0 mm hole at 45 degrees (5.4 mm was too tight in ASA, on the coupon, 2026-10-15). The pigtail is held by a zip tie inside against the end of its boss and a dab of silicone, not by squeeze. Join the umbilical hose to it with a straight barbed connector from the assortment.
- **Paracord.** A U-tunnel in a boss standing on the floor, with both openings on the outer face, so you never reach inside the cup. Thread the cord with a leader (a stiff wire, or a zip tie taped to the cord's melted tip), knot it and melt the ends. The cord is shorter than the hose and wires. **Test the tunnel with a hard pull on the cup before relying on it.**
- **Unplugged port:** push a TPU port cap (part 42) into the well. Standing water across live sockets leaks current and corrodes them. The cap only covers the electrical well: **close an unused channel's fluid side with its slide clamp inside the cup**. Its pigtail can also be capped with a barbed plug or coupler from the assortment, folded over, or just left with the slide clamp closed.

**Bladder IN.** A hose pigtail out the front wall (6.0 mm hole, same zip tie and silicone dab), 45 degrees down, joined to the bladder's factory tube with a reducer from the assortment. Labelled IN.

**Drains.** Eight 4 mm floor drains under the pump (four in a centre row and four at the pocket corners), plus a pair of floor-flush 4 mm holes in every wall: front and back walls at x = 22 and 72; left and outer walls at y = 11, 35 and 61.5, the gaps between the corner columns and the port bosses.

### Cap-to-sled harness

The cap carries the PCB, the voltmeter, the USB-C charger and the power-key socket, so these wires run between the cap and the sled. Give the bundle about 15 cm of service loop, zip-tie it to the spine at the front lead channel, and put a disconnect in every run so the cap comes right off:

| Run | Wires | From (sled) | To (cap) | Disconnect |
|---|---|---|---|---|
| Power key | 2 × 12 AWG | BMS P+ and the breaker's input stud | Key socket pins A and B | Inline XT60H pair (a spare from the 10) |
| Charger | 2 × 16–18 AWG (up to 4 A) | BMS P+ and P− | Charger output | XT30 pair |
| Voltmeter | 2 × thin | Main + after the breaker, BMS P− | Voltmeter | 2-pin JST-XH, inline |
| PCB power (J1) | 2 × thin | Buck A output | PCB J1 | JST-XH at the PCB |
| Current sense (J2) | 3 × thin | ACS758: GND, 5 V, signal | PCB J2 | JST-XH at the PCB |
| Pump (J3) | 2 × thin | carried on to the pump, through the bulkhead grommet into the cup | PCB J3 | JST-XH at the PCB |

That's 13 conductors in six runs. The two key wires carry the full gun current, so they are the only heavy ones. Nothing in the cap connects to the guns, the LED 5V port or the bladder: those all stay on the sled and the cup.

## Measured parts (Joey, tape measure, 2026-10-14)

The stick is built around these measurements, with clearance added. Every board sits in an open compartment and is held with a zip tie; none of the mounting holes are used.

| Part | Measured | Where it goes |
|---|---|---|
| Breaker | Inline type: studs at both ends; a 1⅝ in square plate in the middle with a reset lever and a push-to-trip button; 4 in long, 1⅝ in thick; plate holes 1¼ in apart | Stands upright behind the cross panel, 2 mm from the outer wall (the walls are solid; its controls are reached with the sled out). Hangs by two zip ties through its plate holes and the spine. Its top is at 106 mm, well under the hung PCB. |
| BMS | 2½ × 1⅞ × ¼ in | Stands on edge in the slot along the back wall, next to the battery's TERM face: a 12 mm back lip and a 25 mm front fence (1.2 mm thick, 0.4 mm from the breaker's back face) stop the 63.5 mm card rocking |
| Buck A, Buck B | 1 in along the port, 5/16 in thick | Buck A in a compartment on the front of the cross panel. Buck B stands on a shelf on the tube's front wall, by the outer wall, with its USB-A receptacle in (or behind) the outer wall's window. **Width not measured; assumed 17 mm (⅝ in).** |
| ACS758 | 1½ × ¾ × ⅛ in | Compartment on the front of the cross panel, above Buck A |
| USB-C charger | 1½ × 11/16 × ⅜ in; the receptacle is centred on the 17.5 mm short side (confirmed by Joey, 2026-10-15) and sits toward one face of the 9.5 mm board thickness | In a slot under the cap's CHG window, receptacle up, thin top end in the slot |
| Voltmeter | bezel about 1 5/16 in, body a hair over 1⅛ in, about 1 in deep or a bit more | 31.2 mm hole in the cap (29.2 mm printed 1-2 mm too small in ASA), with 30 mm of depth allowed above the battery |
| G528 pump | 2 × 1¾ × 1½ in at its thickest | 52 × 46 mm pocket in the cup, strapped down across it |

**Not verified until fitted:** the breaker hangs 1.5 mm above the base. Check that the bottom stud's lug clears the base before printing the sled.

**Still unknown:** the bucks' width (17 mm is assumed). **Measure Buck B before printing the tube**: width, length (assumed 25.4 mm) and where its USB-A sits.

**Buck A's output is soldered straight to the J1 lead.** Buck B has no wiring on its output side: the backpack plugs into its own USB-A port through the tube wall. Buck B's input runs from the sled with a 2-pin JST-XH plug.

## Fit settings (`src/params.scad`)

- **Print all five fit coupons first, in ASA** (see *Printing in ASA*).
- **Cell rings:** measured 2026-10-15: the .65 ring (18.65 mm) fits Joey's 25R cells in ASA, so `cell_bore` = 18.65 in `params.scad`. The default holders (01, 02) are the 18.65 set (the block is now 113.0 × 40.68 × 10 mm).
- **XT30U pockets (+.2 / +.3 / +.4):** lay an XT30U housing in each of the three pockets on `00_fit_coupon` and note which holds it snugly. That sets `fit_clear` for the gun-end umbilical brick's XT30U pocket. **Joey's result (2026-10-15): +0.2 holds it snugly, so `fit_clear` = 0.20** and the brick is rebuilt.

Then rebuild with `./build.sh /path/to/openscad`. It regenerates every STL in a few seconds.

## Part notes

### The stick
- **Orientation:** standing upright beside the bladder.
  - The back (y = 0) goes against your back.
  - The battery is on the left, at the top of the dry side. That's the highest and driest spot, and the heavy part rides high.
  - Nothing exits underneath: the stick stands on its floor. The umbilicals, the bladder hose and the LED 5 V cable all use ports on the walls (see *Inputs and outputs*).
- **Sled:** a central spine with a cross panel.
  - **Battery:** stands left of the spine, on the base, with the **TERM face (pack + and −) toward the back**. The block is **113.0 × 40.68 × 67.45 mm** (67.45 along the cell axis). It sits 2.0 mm off the front wall (the MID face: room for tabs and solder) and 3.55 mm off the back wall (the TERM face: tabs, solder, and the B+/B− leads leaving at the right-hand edge into the space behind the spine's end). The tube walls hold it in once it's inside, so on the bench, hold it to the spine with tape or a rubber band.
  - **Wire routes:** the spine stops 6 mm short of the front and back walls, leaving vertical lead channels. The cross panel has an 8 × 30 mm wire pass at its right end, low down, from the breaker/BMS bay to the bucks/ACS758 in front.
  - **Breaker:** stands upright right of the spine, behind the panel, 2 mm from the outer wall. Run one zip tie through each plate hole and the tall slot in the spine behind it. Leave about 1.5 mm under the bottom stud for its lug. The gap between the spine and the breaker is a wire channel.
  - **BMS:** stands on edge in the slot along the back wall. A 12 mm lip behind it and a 25 mm front fence (1.2 mm thick, 0.4 mm from the breaker's back face) stop the 63.5 mm card from rocking; put a 1.0 or 1.5 mm TPU shim strip (part 38) behind its top, against the tube wall. The battery's TERM-face leads reach it directly through the channel behind the spine.
  - **Buck A and ACS758:** drop into their compartments on the front of the panel and get a zip tie each. **Buck B is not on the sled:** it stands on a shelf on the tube's front wall (see *LED 5 V*), so the sled lifts out past it. Its input wires have a 2-pin JST-XH plug at the sled. Wires to the breaker/BMS side go through the pass at the panel's right end.
  - **Slots:** the spine and panel have cross-shaped zip-tie slots, plus two wire pass holes for the battery leads.
  - **Front-right corner notch:** the base has a notch there (x from about 67.6 mm, y from about 59.2 mm to the walls), so the sled slides down past the Buck B shelf on the tube's front wall. A sled printed before 2026-10-16 filled the whole footprint and hit the shelf: cut that corner off.
  - **How the sled is held (no screws):**
    1. *Sideways and twist:* the base hugs the four bulkhead corner bosses (radius 4.5 mm) with 0.3 mm clearance, and sits 0.5 mm inside the tube walls.
    2. *Up and down:* the cap's TPU pads press the battery, and the battery presses the sled base onto the bulkhead (about 75-125 N per pad).
    3. *Swaying:* the tall spine and panel can't sway. The clamped battery block sits 0.5 mm beside the spine, and the panel runs to within 0.5 mm of the outer wall.
    4. *The right (breaker) half of the base* is tied to the clamped left half by the spine and the 100 mm cross panel, so it can't lift.
  - **Battery stops:** two small ASA posts (5 × 1.75 × 2 mm) stand on the sled base at x = 12–17 and 31–36, in the lead channel behind the battery's back face. They are now only 2 mm tall: they meet the holder's flat bottom strip, below every cell and tab, so a hard jump can't drive the block into the leads. An already-printed sled with the old 8 mm posts still works with the new holders (0.2 mm clear of the TERM tabs), or trim the posts to 2 mm. Route the B+/B− leads out at the right-hand edge of the TERM face.
  - **Holding it down:** the cap's two ribs press the cell holders through a compliant TPU battery pad (part 36) that clicks onto each rib end, which pins the sled onto the bulkhead. The sled itself takes no screws.
- **Tube:** plain shell, 94 × 73 mm inside, 2.4 mm walls, 3 mm bulkhead floor, 156 mm of inside height above the bulkhead. **BubbleLink** is raised 0.8 mm on the outer right-hand (+x) wall, reading upward, so the tube is 99.6 mm wide instead of 98.8. The top half of each letter is inset 0.3 mm (a stepped bevel) so the lettering prints without a flat overhang; it is fine detail only. Print with the bulkhead on the bed; the lettering is on a vertical wall and needs no supports. The outer wall also carries the **LED 5V** USB-A window (a 0.8 mm web, an outside counterbore for the plug's overmold, a drip hood above and the label below), at mid-height beside Buck B.
- **Cap (control head):**
  - **Outline:** 98.8 mm wide; the lettering is on the tube only.
  - **PCB:** hangs under the cap, component side up, on four ASA spacers (part 27) that put it 27.8 mm below the plate (5.8 mm lower than the posts alone, because the LEDs hit the light tunnel). CA a spacer onto each post's stake pin, push the board onto the spacers' pins and heat-stake the tips (heads under 5 mm, because J2 sits 2.7 mm from H3).
  - **LEDs:** LED1–3 shine up 3.6 mm holes that go all the way through the cap, inside a light-tunnel block that stops one LED bleeding into the next. With the PCB fitted, fill each hole from the top with clear hot glue or UV resin; that seals it and passes the light. Any cap colour works.
  - **PRIME (guarded, hard-stopped):** a TPU plunger in a sleeve, under a TPU boot.
    - The boot's D-shaped flange sits on the cap and is clamped under the ASA **guard bezel**, which is glued to the cap (ASA to ASA: acetone slurry is best, CA works). Put a thin ring of silicone under the flange first. Nothing relies on glue holding TPU.
    - The bezel's rim stands 1 mm above the boot, so it takes a deliberate fingertip press. A strap, an elbow or the bag can't press it.
    - The plunger head bottoms on the cap after 0.75 mm. SW1 clicks at about 0.55 mm, and the soft TPU plunger takes up the rest, so even a hard press can't push the PCB off its posts.
    - At rest the plunger tip is 0.3 mm above SW1. See view 8 in `renders/`.
  - **RV1 and RV2:** RV1 (THR) sets the gun-detect threshold and RV2 (DLY) the pump off-delay. Pull the TPU trimmer plug (part 39), adjust the 3296W trimmers (25-turn) through the two small windows with a small screwdriver, then push the plug back in. One plug closes both windows: a 1.2 mm plate on the cap top with two square plugs (5.8 × 5.2 mm, 0.1 mm interference per side) pushed 2.6 mm into the 5.6 × 5 mm windows, with a lead-in chamfer and a pull tab toward the BubbleLink label. Print plate down. Plugs go in last, once the trimmers are set. The THR and DLY labels are 1.4 mm further out so the plug doesn't cover them.
    - Each window sits over its 3296W adjusting screw, which is at the pin-1 end.
    - **Solder both trimmers with pin 1 on the square pad.** If one goes in reversed, its screw ends up under the PRIME boot.
  - **Voltmeter:** the body drops through the 31.2 mm hole and gets glued around its bezel. (The first 29.2 mm hole printed 1-2 mm too small in ASA, so `vm_hole` is now 31.2 mm.)
  - **Power key socket (KEY):** an XT60H male sits in a 17.0 × 9.8 mm, 22 mm deep sleeve under the cap plate, its shroud under a 0.8 mm lip, with a rear zip-tie keeper (see *Inputs and outputs*). Wire pin A to BMS P+ and pin B to the breaker input. The key (part 26) is an XT60H female with a 12 AWG U-loop across its two cups, hot-glued into the grip. Key in is ON; key out is OFF (all loads off; the BMS, the charger and one pin of the key socket stay live), and the key blank (43) goes in for storage.
  - **USB-C charger:** the board's receptacle sits toward one face of its 9.5 mm thickness, with the thick part (output pads, big components) lower down the board. The old 9.5 mm pocket let it wobble, so the cap now has a slot only 1.25 × the USB-C receptacle's thickness (`usbc_port_t` = 3.3 mm, an estimate, so the slot is about 4.1 mm), 30 mm deep and 18.3 mm wide. The board's thin top end (PCB plus receptacle) slides up into it, receptacle against the CHG window; the thick part hangs below the slot. There are no crush ribs any more. Add a dab of glue at the slot mouth. **If the board's top end is thicker than about 4.1 mm** (for example the receptacle sits on top of the PCB rather than through it), measure PCB plus receptacle and set `usbc_port_t` so 1.25× it clears, then rebuild. A USB-C plug pushes about 20 N, so charging with the cap on is fine once the board is seated. Between charges, the TPU USB-C plug (part 40) fills the CHG counterbore (13.5 × 7.5 mm stadium, 0.1 mm interference per side) and the window through the 0.8 mm web. Nothing enters the receptacle (its centre tongue is right behind the mouth). The pull tab points toward the voltmeter; pull it to charge. Print flange down. **Charge indication:** the charger's LEDs are hidden under the cap. Charge with the key IN to watch the voltmeter reach 8.4 V (the bucks and PCB draw about 20 mA meanwhile), or with the cap off. The receptacle is centred on the board's 17.5 mm short side (confirmed by Joey, 2026-10-15). Run its output to the BMS P+/P− through an XT30 pair, so the cap stays removable.
  - **Labels:** engraved 0.6 mm deep, reading from the front. Rub in acrylic or a paint pen if you want them to stand out.
  - **Wires to the cap:** J1, J2 and J3 are XH plugs. Leave enough slack to lift the cap and set it beside the stick. (Buck B is on the tube, not the cap or the sled; its input is a tube-to-sled run with its own 2-pin JST-XH disconnect.)
- **Seal:** stretch the TPU ring into the cap skirt's groove (about 80% fill, 13% squeeze). The tube's rim has a 1 mm lead-in so the ring doesn't catch on the way in.
  - Two M3 × 10 screws go through the front and back walls, **each with a TPU washer and an M3 flat washer under the head**, into M3 nuts glued into the slots behind the cap's skirt (the slots open on the underside of the nut blocks). Each also has an M3 flat steel washer on top of the TPU washer, under the head. The screws only keep the cap on; the washers keep water from following the screw holes past the ring.
  - To get the cap off, lever it up with a flat screwdriver in the notch on the left edge.
  - **Wet-test the cap** before trusting it. This is a starting geometry for a TPU seal, not a proven one.
- **Bulkhead grommet:** two TPU halves plus an ASA drip skirt. Each half has its own hole per conductor, sized 0.2 mm under the wire OD.
  - Holes: both 16 AWG gun pairs and both pump leads. The XT60H loop and the backpack USB no longer cross the bulkhead.
  - **Cut a slit with a knife** from each hole to the nearest long edge, so the cables lay in.
  - Put the skirt's lip against the bulkhead's underside, then push the lower half up through it from the cup side, and the upper half down from the dry side. They meet inside the slot, and the lower flange clamps the skirt's lip.
  - **Seal the top:** once the wiring is final, fill the whole top face of the upper half with neutral-cure silicone, covering the slits and working it around each cable. The silicone peels off when you need to pull the sled.
  - **Skirt:** its 8 mm wall hangs down around the cable exit. Water running along the underside of the bulkhead drips off its edge, and spray from a leaking fitting can't hit the grommet directly.
  - **On its side:** the cup has drains in its floor and the same pair of 4 mm drains in every wall, so whichever face is down, water runs out instead of pooling up to the grommet. Upside down is the one orientation where water sits on the grommet, which is why the top is sealed with silicone. Turn it upright and let it drain.
  - Give every cable a drip loop below the cup, so water runs off the low point rather than up the cable.
- **Venting and heat (not verified):**
  - The tube only breathes incidentally, through the grommet slits and the cap ring.
  - I haven't verified pressure relief if a cell fails, or charging temperatures inside the closed tube. At 4 A the charger alone may give off around 3–4 W.
  - Check charger and BMS temperatures on the first enclosed charge. Until then, charge with the cap off.
- **Turning it off:**
  - **Power key (OFF switch):** pull the key out of the KEY socket on the cap top. That turns off everything downstream of it (breaker, ACS758, both bucks, PCB, voltmeter, pump and guns): all loads off, but the battery stays connected to the BMS, the charger and one pin of the key socket. The charger connects upstream of the key, so it still works with the key out. For storage or transport, key out and key blank (part 43) in.
  - **Voltmeter:** wire it after the breaker (and so after the key), so it goes off with everything else when the breaker trips or the key is pulled.
  - **Resetting the breaker:** there's no window, so take the cap off (2 screws), lift the sled out and reset the lever. Leave enough wiring slack to lift the sled out. A trip means a real fault (a short, a jammed motor), so find the cause before resetting.
  - **Idle drain:** pull the key, and put the blank in, for storage.
    - The BMS stays on the battery either way. Its quiescent draw is typically tiny, but I haven't measured this one.
    - The voltmeter's idle draw isn't measured either. Small LED meters like this typically draw tens of mA. At 20 mA, the 12.5 Ah pack would take weeks to drain, so overnight it doesn't matter.
    - Check it once with a multimeter on the mA range.
- **Cup:**
  - **Pump:** sits on a 2 mm TPU pump mat (part 37) in a 52 × 46 mm pocket on the left of the floor, strapped down with zip ties through the slots on either side. Eight 4 mm drains are under it (four in the centre row, four at the pocket corners); the mat's eight 6 mm holes sit over them, and its underside grooves keep a flat pump bottom from sealing them. Four 6 × 1.5 mm notches through the pocket fence at floor level stop the pocket holding water when the pack lies on its side.
  - **Fittings:** the right-hand strip (x 64–94) holds three tees, the check valve and the bypass slide clamp, strapped to the four tie slots. The 70 mm clamp runs front to back.
  - **Ports:** the two gun clusters (XT30U well, hose pigtail, paracord tunnel, drip hood, number) are on the outer wall, and the bladder IN pigtail is on the front wall. There is no service hole and no hole in the floor except the drains. See *Inputs and outputs*.
  - **Drains:** eight 4 mm floor drains under the pump (four in a centre row and four at the pocket corners; offset because the pump pocket sits left of the fittings strip). Every wall also has floor-flush 4 mm drains: front and back walls at x = 22 and 72; left and outer walls at y = 11, 35 and 61.5, the gaps between the corner columns and the port bosses.
  - **Paracord tie-offs** (also called tether anchors): one U-tunnel in a floor-standing boss beside each gun port on the outer wall, with both openings on the outer face (no reaching inside the cup). The number 1 or 2 is engraved above each port, so tunnel 1 belongs to gun 1. See *Built for jostling* below.
  - **Mounting:** four M3 × 12 screws go up from underneath through the corner columns into the bulkhead nuts. **Fit the 4 nuts before the sled goes in:** drop each one into its hex pocket in the bulkhead floor from the dry side (there's 1.4 mm of floor under it) and lock it with a dab of CA or silicone. Each screw, with its lock washer, runs through the 3.4 mm hole in its column, past a 6.6 mm counterbore for the head and washer, and threads fully through its nut. Pulling on the cup pulls the nuts down onto that floor, not out of their pockets.
- **Plumbing:** `bladder → inlet tee → pump → outlet tee 1 → outlet tee 2 → gun 1 / gun 2`. From tee 1's side branch: `→ slide clamp → check valve (arrow toward inlet) → inlet tee`. That's three tees in total, so check the assortment has three.

### Built for jostling (hours of jumping, dancing and walking)

**Where the umbilical joins.** At the cup's outer wall, in one of two port clusters. Nothing joins inside the wet cup. Each umbilical's pack end is an XT30U **male** on the 16 AWG pair, the hose end and a paracord loop; there is no brick at the pack end. Its gun end is an XT30U **female** (power always comes from a female), which plugs onto the gun's male input. The male plugs into the pack-side female in the XT30U well, the hose joins the hose pigtail with a straight barbed connector, and the paracord ties through the cluster's U-tunnel. From the pack to the gun it's one bundle, ending in a **gun-end umbilical brick** (hose, 16 AWG pair and paracord).

**Gun power route.** The 16 AWG gun pairs do not come from the PCB. Battery + goes to the BMS, then the power key, then the 30 A breaker, then the ACS758, where it splits into two 16 AWG + leads. The − leads come from the BMS P− bus. Each pair runs down the front compartment, through the bulkhead grommet, across the cup and to its port's XT30U female, numbered 1 or 2. View 9 in `renders/` (`9_gun_power_and_paracord.png`) shows it with the hoses: red is gun 1, orange is gun 2 and yellow is the paracord.

**Load path for a dropped gun.**
1. The gun pulls the gun-end brick (its inner hole is tied to the gun).
2. The brick pulls the **paracord**, which runs from the gun end to the cup.
3. The cord is tied through the **U-tunnel boss** at that gun's port (cord in one opening, out the other, knot it, then melt the ends). It is shorter than the hose and wires.
4. The U-tunnel boss carries the load into the cup, and the cup into the bulkhead through its four M3 screws and the captured nuts.

The hose and wires between the port and the gun-end brick, and between the gun-end brick and the gun, are **left longer than the cord**, with a visible slack loop. If a gun drops, the cord goes tight first and the hose and solder joints never see the load. Check this by pulling on the gun with everything assembled: the cord should go taut while the hose and wires stay slack.

**Vibration measures** (built in or done at assembly):
- **Nothing rattles in a pocket:** TPU battery pads on the cap's two ribs (part 36) and TPU shim strips (part 38; thicknesses 0.6, 1.0 and 1.5 mm) anywhere a board has play in its compartment. Every board gets a zip tie through its compartment slots.
- **Breaker:** two zip ties through its plate holes into the spine slots, so it can't swing on its studs.
- **Connectors:** a dab of hot glue on every JST-XH plug (J1–J3) after a final test, and a zip tie or tape around each mated XT30/XT60 pair. The XT30U well, the key socket and the USB-A window are potted or glued as described under *Inputs and outputs*.
- **Solder joints:** heat-shrink over every joint, and a zip tie to the sled within 2–3 cm of each joint, so the wire flexes there instead of at the solder.
- **Charger:** held by its slot, not only its glue.
- **Pump:** the TPU pump mat (part 37) under it in the pocket, strapped down across the top with zip ties.
- **Hoses:** a slack loop on every hose inside the cup, so pump vibration doesn't work the barbs loose.
- **Sled:** takes no screws; it is located by the corner bosses and pinned by the pads (see *How the sled is held* above).
- **Cap:** the radial TPU ring takes no clamping force, so the two screws can't shake it loose. The seal doesn't depend on screw torque.
- **Nuts:** all six are captured in hex pockets and glued, so nothing turns when a screw is driven or the stick is shaken.

### Cell holders (MID and TERM)
- Ten cells in two offset rows of five, at 19.9 mm pitch. That leaves a 1.6 mm wrapper gap and keeps the 26 mm nickel tabs reaching both cell centres.
- **Orient the rows in opposite directions.** Row A goes + toward one end and row B − toward it. If every cell faces the same way, it's 10P, not 2S5P.
- **MID** caps the series end: every tab on that face is the midpoint.
- **TERM** carries the separate pack + and − buses. Keep the two rows' strips apart, with fish paper between them.
- **0.8 mm lip (reprint both holders, 01 and 02):** `holder_lip` went from 2.0 to 0.8 mm. With the 2.0 mm lip the cell ends sat about 2 mm below the holder face (plus the fish paper), so every tab had to bend down into its window and arch over the plastic, the tabs wouldn't lie flat, and the finished block (with tabs and solder) was too long to slide into the stick. The block is now 113.0 × 40.68 × 67.45 mm (it was 69.85 along the cell axis). Any holders printed with the 2 mm lip must be reprinted.
- **Flat ends:** both holders have flat end faces (the outline includes a full-width rectangle at each long end), so the pack's top and bottom are flat across the full 40.68 mm width rather than a rounded sawtooth crest. The cap's TPU pads would otherwise bear on a single crest about 7 mm wide. The bounding box (113.0 × 40.68 × 10 mm with the 18.65 bore) is unchanged by the flat ends, and cells and tabs are unaffected. **Anyone who already printed the old flat-less holders must reprint them,** or sand a flat end, or accept a stiffer or looser pad contact.
- The holders are mirror images. If the A/B letters don't line up, rotate MID 180°.
- **In the stick**, the cell axes run front to back. The holder faces with the tabs press against the tube's front and back walls through fish paper (2.0 mm off the front wall, 3.55 mm off the back wall).
- **Soldering the tabs:**
  - Amber residue means the rosin flux burned off before the solder wet: not enough heat is getting in. Use the biggest chisel tip, clean and freshly tinned, at 400-450 C, with a small blob of solder on the tip as a heat bridge, pressed firmly.
  - Scuff both the tab and the cell terminal with fine sandpaper and wipe with isopropyl alcohol. Use flux **paste**; rosin core alone is not enough on nickel-plated steel.
  - **Pre-tin the tabs off the battery.** Tin each cell terminal with a 1-2 s touch, then join by reflowing through the tab. Still at most about 3 s per contact; alternate cells.
  - **Never use hot glue (or tape) as the electrical connection.** Each joint carries up to about 5 A, a glue contact heats, the glue softens at about 60-80 C, and the joint opens or arcs. Hot glue is fine over a good solder joint as strain relief and insulation.
  - If soldering keeps fighting, a handheld 18650 spot welder makes these joints in seconds (an optional tool, not a part change).

### Slide clamp (×3)
- **Assembly:** lay the tube in the channel and slide the slider on from the open end, ridge down.
- **Operation:** slide toward the arrow to close.
  - The first ~8 mm goes from fully open (6.0 mm gap) to 2.4 mm.
  - The next 22 mm is fine adjustment (about 0.08 mm per mm).
  - It seals at 0.6 mm against the stop blocks.
  - The shallow ramp self-locks; wet-test that it holds.
- **Roles:** one is the bypass restrictor; two are channel shutoffs, one on each gun line.

### Umbilical brick (×2)
- One at the **gun end** of each umbilical. There is no brick at the pack end any more: that end is an XT30U male, the hose end and a paracord loop that plug into the cup's port cluster.
- **XT30U (female):** drop it into the open-top pocket and strap it with a zip tie through the slots beside the pocket.
- **Wires and tube:** the 16 AWG pair and the fluid tube run in their grooves, held by narrow zip ties.
- **Paracord:** the tether ties through the outer hole and runs back to the cup's U-tunnel. The inner hole ties to the gun.

## M3 hardware (checked against `stick.scad`, 2026-10-15)

No screw cuts its own thread in plastic. Every clearance hole is 3.4 mm and every thread is in a nut.

| | Cap screws | Cup screws |
|---|---|---|
| Count and size | 2 × M3 × 10 socket head | 4 × M3 × 12 socket head |
| Where | Front and back tube walls, 5.2 mm below the rim (a 3.5 mm land above the hole), centred at x = 49 | Four corner columns of the cup, up from below |
| Nut | Slot opening on the underside of the cap's nut block. The slot is 5.9 mm wide and 3.0 mm deep (nut_h 2.8 + 0.2). | Hex pocket in the bulkhead, dropped in from the dry side. 6.75 mm across corners (5.5 / cos 30° + 0.4). The pocket starts 1.4 mm above the bulkhead's underside, so 1.4 mm of floor sits under the nut. |
| Under the head | M3 flat washer (0.5 mm) on top of the TPU washer (part 34, 1 mm) | M3 split lock washer (0.8 mm); the 6.6 mm counterbore fits the 5.5 mm head and the washer |
| Stack-up | flat 0.5 + TPU 1 + wall 2.4 + gap 0.3 + skirt 2.6 to the nut seat = 6.8 mm | head underside to nut seat = 8.9 mm (0.8 lock washer + 6.7 mm from the counterbore floor to the bulkhead's underside + the 1.4 mm floor) |
| Thread past the nut seat | 10 - 6.8 = 3.2 mm | 12 - 8.9 = 3.1 mm |
| Through the nut | A full M3 nut is 2.4 mm, so the screw is through it with 0.8 mm showing | Through the nut with 0.7 mm showing |
| Engaged | The whole nut (about 5 turns at 0.5 mm pitch) | The whole nut (about 5 turns) |

The cup counterbore is 0.8 mm deeper than a bare screw needs. With the lock washer the screw still reaches 0.7 mm past the nut; without it, it shows 1.5 mm. Without the extra depth, the lock washer would leave the tip 0.1 mm short of the nut top (still fully engaged, but with no margin).

The nut pockets (the cap slot and the bulkhead hex) were confirmed correct as printed on the coupons (2026-10-15). Both lengths work, so **don't use shorter screws**. Don't over-torque: ASA is a bit more brittle than PETG, and the cup's nuts are only held by the 1.4 mm floor and glue. Snug is enough; the cap seal doesn't depend on screw torque.

Totals: 6 M3 socket-head screws (2 × 10, 4 × 12), 6 M3 nuts (4 bulkhead, 2 cap), 2 TPU washers, 2 flat washers, 4 lock washers. No anaerobic threadlocker near ASA.

## TPU cushions (replacing foam)

The build no longer uses foam. Three TPU parts do its jobs. All print on the A1 with no supports.

- **Battery pads, part 36 (x2).** A compliant cap that clicks over the end of each of the cap's two battery hold-down ribs. It is not a solid block: a 0.8 mm bottom skin, a 0.8 mm top plate (the rib seat) and six 0.8 mm fins, each 1.6 mm wide, between them, leaving a 2.2 mm fin gap and a 3.8 mm floor overall. A solid 3 mm TPU block is far stiffer than the cap plate, so it would not take up any tolerance; the fins let the pad do that. The pocket is 2.9 mm wide with centred 1.3 mm walls and 6 mm deep, and a 0.4 mm retaining bead on each long pocket wall clicks into a matching 0.5 mm deep groove in the rib, so the grip is mechanical. The rib tip has a 0.5 mm chamfer so insertion doesn't shave the bead. A dab of hot glue is only a backup.
  - Compression is 0.6 mm nominal (working range 0.1 to 1.2 mm). The spring rate is roughly 70-140 N/mm per pad.
  - **Preload ceiling:** both cap screws bear on a 3.5 mm land (the screw hole is 5.2 mm below the rim), so keep the total preload under about 100-140 N. If the cap needs hard pressing to close, the stack is too tall: trim with a thinner pad or sand the pad floor. Press the cap down while tightening the two screws so the 3.4 mm holes' slack doesn't eat the preload.
  - Print slow, in TPU, opening up. The top plate bridges 6.4 mm gaps between fins and droops a little, so print three pads and keep the best two.
  - **Tolerance:** ASA shrinkage in XY can shorten the battery stack by 0.3-0.8 mm. If the cap closes with the pads loose or rattles, put a 0.6 mm shim strip (part 38) under a pad, between the pad and the cell holder. If the cap won't seat, trim the shims or sand the pad floor. Measure the real stack before printing the cap (see *Print order*).
- **Pump mat, part 37.** A 2 mm mat that sits in the cup's pump pocket under the G528. It has eight 6 mm holes (four in the centre row and four near the pocket corners, centred at x = 16 and 56 and 6 mm in from the pocket edge, so the mat doesn't tear at its corners) over matching 4 mm floor drains in the cup, and 1.5 × 0.8 mm drain grooves on its underside (a perimeter groove plus a cross grid), so a flat pump bottom can't seal the holes. The cup also has four 6 × 1.5 mm notches at floor level through the pump-pocket fence, so the pocket can't hold water like a tray when the pack lies on its side. The pump is still strapped down with zip ties across the pocket fence.
- **Shim strips, part 38.** One STL with six 5 × 30 mm strips: two 0.6 mm, two 1.0 mm and two 1.5 mm thick. Cut with scissors and tuck into any pocket where a board rattles. The BMS slot has only about 0.6 mm of slack and the buck and ACS758 pockets about 1 mm of width, so use the 0.6 and 1.0 mm strips there. Place a strip against a component-free board edge and keep the zip tie.

Check the pads on the first dry fit: with the cap on, the sled should not move when you shake the stick.

## TPU plugs (no tape)

TPU plugs close the cap's and tube's openings, so nothing is taped over. Print them on the A1.

- **Trimmer plug, part 39.** One plug closes both trimmer windows (RV1 = THR, RV2 = DLY). A 1.2 mm plate sits on the cap top with two square plugs (5.8 × 5.2 mm, 0.1 mm interference per side) pushed 2.6 mm into the 5.6 × 5 mm windows. It has a lead-in chamfer and a pull tab toward the BubbleLink label. Pull it to adjust the trimmers, push it back in. Print plate down.
- **USB-C plug, part 40.** Fills the CHG counterbore (13.5 × 7.5 mm stadium, 0.1 mm interference per side) and the window through the 0.8 mm web. Nothing enters the receptacle, because its centre tongue is right behind the mouth. The pull tab points toward the voltmeter. Pull it to charge. Print flange down.
- **USB-A plug, part 41.** Fills the outside LED5V counterbore only (17 × 9 mm); it doesn't enter the window, since Buck B's receptacle may sit in it. The pull tab points down. Print flange down.
- **Gun port cap, part 42 (x2).** Closes an unplugged XT30U well, so standing water doesn't sit across live sockets. A sleeve presses into the well around the female's nose; it has a pull tab. Print flange down.
- **Key blank, part 43.** Closes the KEY socket when the key is out; tie it to the key's lanyard so one is always in.
- **Key gasket, part 44.** Glued under the key grip; presses on the cap top round the socket when the key is home (sand the grip or add a shim strip for 0.2-0.3 mm of squeeze).
- The THR and DLY labels were moved 1.4 mm further out so the trimmer plug doesn't cover them.

## Printing in ASA

The rigid stick parts are ASA, not PETG. It is tougher in the heat (about 100 C against about 80 C), which is a plus in a hot bag or in sun. It is also fussier to print.

- **Printer:** print the tall parts (tube, cap, sled, cup, and the cell holders) on the enclosed K2 Plus. The A1 is open-frame, and Bambu lists ASA as not recommended on it: ASA warps and can crack on tall parts there. Use the A1 for TPU and for the small ASA parts only (bezel, skirt, clamps, bricks), and then only with a draft shield and a brim.
- **Settings:** brim on the tube, cup and cap. Warm the chamber. No part-cooling fan, or a very low one. Nothing here needs supports.
- **Ventilate.** ASA gives off styrene fumes. Print in a ventilated room or with the printer's filter.
- **What `00_fit_coupon` is.** A flat plate with three rows of rectangles. **Row 1 (top):** the three cell rings (18.65, 18.80, 18.95 mm). **Row 2:** three open-top XT30U pockets at +0.2 / +0.3 / +0.4 mm per side. Lay an XT30U housing in each and note which holds it snugly; that sets `fit_clear` for the gun-end umbilical brick's XT30U pocket (Joey's result: +0.2, now set). **Row 3:** three XT60H pockets, same idea. They were for the old XT60H loop holder and **no part uses them any more** (the key socket is tested on the ports coupon instead), so ignore row 3.
- **Print the fit coupons first, in ASA, before any real part.** ASA shrinks about 0.5-0.7%, against about 0.3% for PETG. Print the five coupons: `00_fit_coupon` plus the four stick coupons.
  - `00_stick_coupon_rim`: a 19 mm slice of the tube rim, including a cap-screw hole.
  - `00_stick_coupon_skirt`: the matching slice of the cap skirt, with the seal-ring groove, a nut slot and a screw hole. It is flipped plate-up for printing.
  - `00_stick_coupon_nut`: a bulkhead corner with a cup-screw hex nut pocket.
  - `00_stick_coupon_cap` (optional): the part of the cap with the voltmeter hole and the charger slot, plate down (about 34 × 54 × 33 mm). Check the real voltmeter and charger in it.
  - `00_stick_coupon_ports`: a 2.4 mm wall with an XT30U well, a 6.0 mm hose hole, a 14.0 × 6.6 mm USB-A window with its counterbore, and an XT60H key socket with its lip.
- **Procedure:**
  1. The skirt slice should drop into the rim slice with the TPU ring (part 30) stretched on. The ring squeezes about 0.25 mm against the wall.
  2. An M3 nut should press into both hex pockets (the cap's slot and the bulkhead's hex).
  3. The cell bore in `00_fit_coupon` should take a 25R cell. **Result (2026-10-15): the .65 ring fits; `cell_bore` = 18.65 is set.**
  4. If anything is tight or loose by more than about 0.2 mm, use slicer shrink compensation (about 100.5% on the K2 Plus for ASA), or edit `cell_bore` or `sk_c` in the params and rebuild.
  5. The voltmeter hole is now 31.2 mm (29.2 mm printed 1-2 mm too small in ASA). Check the real voltmeter and the charger in the cap coupon before printing a whole new lid.
  6. On the ports coupon: the umbilical's male XT30U shroud slides into the well (10.8 × 6.2 mm), the silicone tube goes through the hose hole, a USB-A plug seats through the window, and the XT60H male drops into its sleeve (17.0 × 9.8 mm) and stops under the lip. **Results (2026-10-15): the XT30U well is a good fit and the XT60H key socket is "a great fit" (verified, no longer estimates). The M3 nut pockets are correct as printed. The 5.4 mm hose hole was too tight and is now 6.0 mm. The USB-A window was too small for Buck B's receptacle and is now 14.0 × 6.6 mm.**
- **Gluing:** acetone can weld ASA to ASA (bezel to cap), brushed on or as a slurry of ASA scrap dissolved in acetone, and bonds better than CA. Don't use it on grooves, bores or pockets: it changes their edges. CA joints should be tested on scrap first. The nut pockets still get CA or silicone.
- **Heat-staking the PCB pins:** still works. The pins are about 2.95 mm tall and leave about 1.6 mm above the board. Melt them down to heads of about 4.2 mm with a 250-280 C iron (ASA softens around 100 C), touching briefly, and don't pull on the board.
- **Brittleness:** ASA is somewhat more brittle than PETG. Don't over-torque the M3 screws into the nuts, and don't pry hard at the cap's notch.
- **TPU is unaffected.** Print the TPU parts as you would have before.

## Checks done on these files (2026-10-14, updated 2026-10-15)

- All 32 STLs rebuilt watertight. Every STL is watertight. All are single bodies except the clamp (a body and a slider) and the shim set (38), which is six separate strips on purpose. All sit at z = 0.
- `stick.scad` `part="assembly"` has placeholder blocks for the battery, breaker, PCB, voltmeter, charger, BMS zone, bucks/ACS zone and pump envelope.
  - Pairwise intersection checks, including the TPU parts in their installed positions, found no overlaps. The exceptions are intended: the heat-stake pins pass through the PCB holes, and the seal ring presses 0.25 mm into the tube wall.
  - With the measured sizes, the pump fits its pocket with 0.6–0.75 mm of side clearance and 12 mm above it.
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
- A final GPT-6 Astra verification pass (2026-10-14) confirmed the earlier fixes and caught one last collision: the USB-C charger stands upright (its 1½ in runs along the plug), so it would have hit the battery. The cap was raised 8 mm and the stick is now 215 mm tall. It also flagged the breaker caveat above.
- **Jostle pass (2026-10-14):**
  - The bulkhead nut pockets opened on the cup side, so tightening the screws would have pulled the nuts out. Fixed: they now drop in from the dry side.
  - Added the paracord tie-offs (tether anchors), the grommet drip skirt, wall drains for lying on its side, the charger pocket, through-hole LED windows, and the guarded, hard-stopped PRIME button.
  - The PRIME plunger is now TPU and part 24 is the bezel; the old rigid plunger STL is gone. Labels were enlarged and turned to read from the front.
  - All 17 STLs rebuilt watertight; the interference sweep is still clear.
- **TPU-cushion pass, 2026-10-15:**
  - Foam is gone. Added parts 36 (battery pads), 37 (pump mat) and 38 (shim strips); the tube gained raised BubbleLink lettering on its right-hand wall (now 99.6 mm wide); the USB-C receptacle position was confirmed; rigid parts move from PETG to ASA.
  - Two further independent reviews (Astra and Fable) led to: the compliant battery pad with snap beads, an 8-hole pump mat with drain grooves and cup corner drains and fence notches, a shim set in three thicknesses, charger crush ribs, battery y-stops on the sled, a stepped bevel on the tube lettering, and three stick fit coupons.
  - Round-2 reviews: flat end faces on both cell holders (reprint old ones); pad redesigned (3.8 mm floor, 0.6 mm compression, 70-140 N/mm); cap screw holes 0.7 mm lower (5.2 mm below the rim, 3.5 mm land); pump mat and cup corner drains moved 2 mm inward; print order now measures the real stack before the cap and pads.
  - Hardware and plugs pass: the kit's DIN 912 socket heads with flat washers (cap) and lock washers (cup, counterbore 0.8 mm deeper); TPU trimmer and USB-C plugs (39, 40) replace the tape; cup drains made identical on every wall; paracord tie-offs moved up and numbered; sled base now hugs the corner bosses; gun power routing wording fixed; render view 9 added.
  - Lid and sled pass (2026-10-16): voltmeter hole 29.2 to 31.2 mm; charger pocket replaced by a thin slot (no crush ribs); optional cap coupon; sled corner notch for the Buck B shelf. Joey needs a new lid (part 21); the sled fix only matters for a reprint.
  - Battery build pass (2026-10-16): `holder_lip` 2.0 to 0.8 mm (reprint both holders; block 113.0 × 40.68 × 67.45 mm); the block now sits 2.0 mm off the front wall and 3.55 mm off the back; pad centres at y 8.55 and 66.0 (the new cap, part 21, includes this); sled stop posts now 2 mm tall; soldering guidance added.
  - Coupon results (2026-10-15): `cell_bore` = 18.65 (holders 113.0 × 40.68 × 10 mm); nut pockets, XT30U well and XT60H key socket verified; hose hole 5.4 to 6.0 mm; USB-A window 14.0 × 6.6 mm, with Buck B moved from the sled to a shelf on the tube's front wall.
  - Review pass (Astra): connector genders fixed (power always from a female; pack well female, umbilical pack end male, gun end female, gun input male); the key no longer fully disconnects the battery (key blank for storage); keepers for the key socket and XT30U wells; XT30U well 10.8 × 6.2 mm; key sleeve 17.0 × 9.8 × 22 mm; LED 5V window 13.2 × 5.7 mm with Buck B 0.5 mm from the wall; parts 43 and 44 added.
  - Ports pass: every way in or out is now a labelled port (CHG, KEY, LED 5V, gun 1 and 2, IN) and nothing exits underneath. The power key (part 26) replaces the XT60H loop, Buck B plugs straight into a USB-A window, gun ports sit on the cup's outer wall, and the pack-end brick is gone (`10_umbilical_brick_x2`). Added the ports coupon and parts 26, 41 and 42; the BMS slot got a 12 mm lip and a 25 mm fence.
  - All 32 STLs rebuilt watertight.
  - The M3 thread and nut stack-ups were re-checked against `stick.scad` (see *M3 hardware* below).
- **None of these parts has been printed or test-fitted.**
