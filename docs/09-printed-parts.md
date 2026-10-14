# 3D-Printed Parts

**Status (2026-10-14):** CAD exists for every functional part. Sources, STLs and the full print guide are in [`hardware/printed/`](../hardware/printed/README.md). **Nothing has been printed or test-fitted yet.**

## Design: the stick

The whole pack, apart from the bladder, is one upright **stick**: about **99 × 78 × 207 mm** (3.9 × 3.06 × 8.15 in). It stands beside the 1 L bladder in the bag. Two umbilicals (hose + XT30U cable + paracord each) leave from its bottom, so it can move to a different bag easily.

| Section | What's in it |
|---|---|
| **Cap** (control head) | CTRL v1.2 PCB hung underneath. LEDs show through 0.6 mm skin windows. PRIME is a plunger under a TPU boot. RV1 and RV2 adjust through two tape-covered windows. Voltmeter and USB-C charge port on top. A TPU ring seals radially against the tube; two M3 screws with TPU washers keep it on. |
| **Tube** (dry) | Plain shell; its floor is the bulkhead. |
| **Sled** (slides out of the top) | The 2S5P block stands beside a central spine. Breaker and BMS sit behind a cross panel; Buck A, Buck B and the ACS758 sit in front of it. |
| **Bulkhead** | Cables cross through a two-piece TPU grommet. |
| **Cup** (wet) | Pump, three tees, check valve and bypass slide clamp. Bolts on from below with 4 M3 screws, and drains through its floor. |

**History:** Joey approved combining parts on 2026-10-14. The first combined design was a wide box (about 157 × 171 × 52 mm). It was replaced the same day because it couldn't sit beside the bladder. Its sources (`dry_core.scad`, `pump_module.scad`, `port_insert.scad`) are kept for reference only.

**Superseded (don't design or print):** the separate battery cartridge, the wet/dry divider and electronics tray, the PCB mount bracket, buck pads, the breaker bracket, the voltmeter and control-panel faceplates, the pump cradle, the pump/hose/tether block, the Cults3D spacer remix (replaced by original 5×2 offset cell holders, MID and TERM, 19.9 mm pitch), and the intermediate "dry core" wide box.

**Hardware:** 6 M3 screws (2× M3×10 for the cap, 4× M3×12 for the cup) with 6 nuts glued in, zip ties, glue, 1 mm foam and tape. Earlier "no screws" statements are superseded.

**Still in use from earlier:** the fit coupon, the two cell holders, the slide clamps (×3) and the umbilical bricks (×4). The Tracer cosplay shells (L1, L2, L3, L6, R1–R6) were printed 2026-08-06 and are a separate project.

**Not designed yet:** mounts for the two dual-head guns. They need the teardown measurements.

## Measured parts

Joey measured the breaker, BMS, bucks, ACS758, charger, voltmeter and pump with a tape measure on 2026-10-14. The stick is sized around those numbers, and every board sits in an open compartment held with a zip tie. The breaker is an inline type with a push-to-trip button and a reset lever. Both are reached through a TPU membrane window in the right wall, which also makes the breaker the stick's OFF switch. The voltmeter is about 1 in deep, and the cap allows 30 mm. Still unknown: the bucks' width (17 mm assumed). See the [print guide](../hardware/printed/README.md).

## Known risks (not yet verified)

- **Cap seal:** a printed TPU ring is a starting geometry, not a proven seal. Wet-test it.
- **Grommet:** a splash baffle, not watertight.
- **Pressure and heat:** there's no verified pressure relief if a cell fails, and charger and BMS temperatures inside the closed tube haven't been measured. Charge with the cap off until the first enclosed charge has been checked.
