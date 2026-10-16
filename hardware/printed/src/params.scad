// BubbleLink printed parts: shared measurements and fit settings.
//
// Every model in this folder includes this file. Edit a value here, re-run
// build.sh, and every affected STL is regenerated.
//
// Each value is tagged with where it came from:
//   [VERIFIED]  datasheet, PCB release package, or canonical-facts.md
//   [LISTING]   seller listing claim; plausible but not measured
//   [ESTIMATE]  nobody has measured it; MEASURE THE PART before a long print
//
// All dimensions in mm.

$fn = 64;

// ---------------------------------------------------------------- printing
fit_clear   = 0.20;   // clearance per side for a part dropping into a pocket; +0.2 held the XT30U snugly on the fit coupon (2026-10-15)
slide_clear = 0.20;   // clearance per side for the slide-clamp dovetail
ziptie_w    = 3.2;    // slot width for the narrow zip ties on hand
ziptie_t    = 1.8;    // slot thickness

// ---------------------------------------------------------------- 18650 cells
cell_d      = 18.33;  // [VERIFIED] Samsung INR18650-25R, +/-0.07
cell_h      = 64.85;  // [VERIFIED] +/-0.15
cell_bore   = 18.65;  // pocket diameter; fit_coupon says 18.65 for Joey's 25R cells in ASA (2026-10-15)
cell_pitch  = 19.90;  // centre-to-centre. Gives a ~1.6 mm wrapper gap and a
                      // printable 1.1 mm rib. Keep <= 21 so the 26 mm nickel
                      // tabs still reach both cell centres.
holder_t    = 10.0;   // spacer thickness along the cell axis
holder_lip  = 2.0;    // retaining lip under each cell end
holder_wall = 2.4;    // outer wall around the cell group
cap_window  = 12.5;   // opening in the lip for spot-welding the tabs

// ---------------------------------------------------------------- tubing
tube_od     = 5.5;    // [VERIFIED order] 3.5 ID x 5.5 OD silicone
tube_wall   = 1.0;
tube_flat_w = 8.8;    // width of the tube when pinched flat (pi*OD/2 + margin)

// ---------------------------------------------------------------- connectors
// AMASS XT30U / XT60H housings. Datasheet-nominal; tune with fit_coupon.
xt30_w      = 10.2;   // [ESTIMATE] across the housing
xt30_h      =  5.3;   // [ESTIMATE]
xt60_w      = 16.0;   // [ESTIMATE] XT60H with sheath
xt60_h      =  8.4;   // [ESTIMATE]

// ---------------------------------------------------------------- umbilical
awg16_od    = 3.2;    // [ESTIMATE] 16 AWG silicone insulation OD
awg12_od    = 4.0;    // [ESTIMATE] 12 AWG silicone insulation OD
usb_od      = 4.0;    // [ESTIMATE] LED-backpack USB cable OD
pump_od     = 2.0;    // [ESTIMATE] G528 motor lead insulation OD
paracord_d  = 4.0;    // [LISTING] 550 cord, 4 mm

// ---------------------------------------------------------------- PCB
// [VERIFIED] BubbleLink CTRL v1.2: 50 x 40 x 1.6 mm, NPTH H1-H4 3.2 mm at
// (+/-21.5, +/-16.5) from board centre.
pcb_w       = 50.0;
pcb_h       = 40.0;
pcb_hole_dx = 43.0;
pcb_hole_dy = 33.0;
pcb_hole_d  = 3.2;
pcb_standoff = 6.0;   // board underside height above the tray
