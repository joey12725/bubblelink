# 3D-Printed Parts

**Status (2026-10-15):** CAD exists for every functional part. Sources, STLs and the full print guide are in [`hardware/printed/`](../hardware/printed/README.md). **Nothing has been printed or test-fitted yet.**

## Design: the stick

The whole pack, apart from the bladder, is one upright **stick**: about **99.6 × 77.8 × 220 mm** (3.9 × 3.1 × 8.7 in) including the PRIME bezel, the cap screw heads and the cup. It stands beside the 1 L bladder in the bag. Two umbilicals (hose + XT30U cable + paracord each) plug into ports on the cup's outer wall, and nothing exits underneath, so it can move to a different bag easily. The drip hoods stand 2.5 mm off the outer wall, so it is 101.3 mm (4.0 in) wide across them. The tube is 98.8 mm wide plus 0.8 mm of raised BubbleLink lettering on its right-hand wall; the cap is 98.8 mm wide. The rigid parts are printed in ASA; the seals and cushions are TPU (see *Printing in ASA* in the [print guide](../hardware/printed/README.md)).

| Section | What's in it |
|---|---|
| **Cap** (control head) | CTRL v1.2 PCB hung underneath. LEDs shine through glue-filled through-holes. PRIME is a TPU plunger under a TPU boot, inside a glued ASA guard bezel, with a hard stop. The USB-C charger's thin top end slides into a slot about 4.1 mm thick under the CHG window (with a dab of glue), and a TPU plug closes the CHG port between charges. The voltmeter hole is 31.2 mm. RV1 and RV2 adjust through two windows closed by one TPU plug. Voltmeter, USB-C charge port and the power key socket (KEY, an XT60H male) on top. A TPU ring seals radially against the tube; two M3 × 10 screws, each with a TPU washer and a steel flat washer, keep it on. Two TPU battery pads on its ribs press the cell holders. |
| **Tube** (dry) | Plain shell, 94 × 73 mm inside, 2.4 mm walls; its 3 mm floor is the bulkhead. Raised 0.8 mm BubbleLink lettering on the outer right-hand wall. A shelf on the front wall holds Buck B, and a 14.0 × 6.6 mm USB-A window (LED 5V) with a drip hood and a TPU plug lets the LED backpack plug into it. |
| **Sled** (slides out of the top) | The 2S5P block stands beside a central spine. Breaker and BMS sit behind a cross panel; Buck A and the ACS758 sit in front of it (Buck B is on the tube wall, so the sled lifts out past it). The BMS slot has a 12 mm lip and a 25 mm fence. |
| **Bulkhead** | Only the two 16 AWG gun pairs and the two pump leads cross, through a two-piece TPU grommet with an ASA drip skirt below it. The cup's 4 nuts sit in hex pockets, fitted from the dry side. |
| **Cup** (wet) | Pump (on a TPU mat), three tees, check valve and bypass slide clamp. Bolts on from below with 4 M3 × 12 screws. Drains through its floor and through the same pair of 4 mm holes in every wall. On the outer wall, two numbered port clusters (1 and 2) each have an XT30U female well, a hose pigtail, a paracord U-tunnel and a drip hood; the bladder IN pigtail is on the front wall. |

**History:** Joey approved combining parts on 2026-10-14. The first combined design was a wide box (about 157 × 171 × 52 mm). It was replaced the same day because it couldn't sit beside the bladder. Its sources (`dry_core.scad`, `pump_module.scad`, `port_insert.scad`) are kept for reference only.

**Superseded (don't design or print):** the separate battery cartridge, the wet/dry divider and electronics tray, the PCB mount bracket, buck pads, the breaker bracket, the voltmeter and control-panel faceplates, the pump cradle, the pump/hose/tether block, the Cults3D spacer remix (replaced by original 5×2 offset cell holders, MID and TERM, 19.9 mm pitch), and the intermediate "dry core" wide box.

**Hardware:** 6 M3 stainless DIN 912 socket-head screws from Joey's HVAKHVA kit (2× M3×10 for the cap, each with an M3 flat washer on top of the TPU washer under the head; 4× M3×12 for the cup, each with an M3 split lock washer), 6 M3 nuts captured in the printed pockets and glued (4 in hex pockets dropped into the bulkhead from the dry side, 2 in slots in the cap's nut blocks), 2 TPU washers, zip ties, glue, clear hot glue or UV resin for the LED windows, and tape. No self-tapping: the nuts carry the threads and the clearance holes are 3.4 mm. Both screw lengths pass fully through their nuts (the M3×12 shows 0.7 mm past the nut with its lock washer, the M3×10 shows 0.8 mm). No anaerobic threadlocker (Loctite 242/243) near ASA, since it can crack it; a tiny drop of CA on the screw tip is the plastic-safe alternative. Tool: a 2.5 mm hex key, long enough to reach about 46 mm up the cup columns. None of the kit's M4/M5/M6 parts are needed. Earlier "no screws" statements are superseded.

**Foam is gone.** Three TPU parts replace it: two compliant battery pads that click onto the cap's ribs (36; about 0.6 mm of compression, roughly 70-140 N/mm per pad), a 2 mm pump mat with eight drain holes (37), and a set of six 5 × 30 mm shim strips (0.6, 1.0 and 1.5 mm thick, two of each) to cut and tuck where a board rattles (38).

**PCB spacers (2026-10-20):** `27_stick_pcb_spacer_x6` (ASA, four plus two spares) drops the CTRL board 5.8 mm below the cap's posts, because the LEDs hit the light tunnel. The cap doesn't change. The PRIME plunger (35) is 5.8 mm longer to match, so reprint it if yours is older.

**New parts this round:** `00_stick_coupon_ports`, `26_stick_power_key` (ASA), and `41_TPU_usbA_plug`, `42_TPU_gun_port_cap_x2`, `43_TPU_key_blank` and `44_TPU_key_gasket` (TPU).

**TPU parts (15 STLs, 23 pieces; the shim set is one STL):** cap ring (30), grommet lower and upper halves (31, 32), PRIME boot (33), screw washers ×2 (34), PRIME plunger (35), battery pads ×2 (36), pump mat (37), shim strip set (38), trimmer plug (39), USB-C plug (40), USB-A plug (41), gun port caps ×2 (42), key blank (43), key gasket (44).

**Fit coupons (print first, in ASA):** `00_fit_coupon` plus five stick coupons (the cap coupon is optional): tube rim, cap skirt (with seal-ring groove, nut slot and screw hole), bulkhead nut corner, ports (XT30U well, hose hole, USB-A window, XT60H key socket in a 2.4 mm wall), and the optional cap coupon (voltmeter hole and charger slot, about 34 × 54 × 33 mm). The skirt slice must drop into the rim slice with the TPU ring on, and an M3 nut must press into both hex pockets. Total: 33 STLs.

**Still in use from earlier:** the fit coupon, the two cell holders (reprinted with a 0.8 mm lip and flat ends; block 113.0 × 40.68 × 67.45 mm), the slide clamps (×3) and the umbilical bricks (×2, gun end only). The Tracer cosplay shells (L1, L2, L3, L6, R1–R6) were printed 2026-08-06 and are a separate project.

**Not designed yet:** mounts for the two dual-head guns. They need the teardown measurements.

## Measured parts

Joey measured the breaker, BMS, bucks, ACS758, charger, voltmeter and pump with a tape measure on 2026-10-14. The stick is sized around those numbers, and every board sits in an open compartment held with a zip tie. The breaker is an inline type with a push-to-trip button and a reset lever. The tube walls are solid (there's no breaker window), so both are reached only with the cap off and the sled out. The power key on the cap top is the OFF switch (all loads off; the BMS, the charger and one key-socket pin stay live). The voltmeter is about 1 in deep, and the cap allows 30 mm. Still unknown: the bucks' width (17 mm assumed). The USB-C receptacle is centred on the charger's 17.5 mm short side (confirmed by Joey, 2026-10-15). See the [print guide](../hardware/printed/README.md).

## Known risks (not yet verified)

- **Cap seal:** a printed TPU ring is a starting geometry, not a proven seal. Wet-test it.
- **Grommet:** a splash baffle on its own; the silicone-filled top is what seals it. Lying on any side, the cup drains before water reaches it. Upside down, only the silicone keeps water out, so turn it upright and let it drain.
- **Jostling:** designed for hours of jumping (captured nuts, a charger slot, a breaker held by two zip ties, paracord tie-offs, a hard-stopped PRIME, lock washers on the cup screws, and a sled held by the corner bosses and the cap's pads), but not yet shaken for real. See *Built for jostling* in the [print guide](../hardware/printed/README.md).
- **Pressure and heat:** there's no verified pressure relief if a cell fails, and charger and BMS temperatures inside the closed tube haven't been measured. Charge with the cap off until the first enclosed charge has been checked.
