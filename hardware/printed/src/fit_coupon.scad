// Fit coupon. Print this first (about 30 min on either printer, same
// filament and settings you'll use for the real parts), then copy the sizes
// that fit into params.scad before printing anything big.
//
//   Row 1: cell rings, bore 18.65 / 18.80 / 18.95. Pick the tightest one a
//          25R cell slides into by hand without forcing. -> cell_bore
//   Row 2: XT30U pockets at +0.2 / +0.3 / +0.4 per side. Pick the one that
//          holds the housing snugly. -> xt30_w/xt30_h stay, set fit_clear
//   Row 3: XT60H pockets, same three clearances (battery disconnect).
//
// Numbers are engraved next to each feature.

include <params.scad>

plate = 2;

module tag(s, at) {
    translate([at[0], at[1], plate - 0.6]) linear_extrude(1)
        text(s, size = 3.2, halign = "center", valign = "center",
             font = "Liberation Sans:style=Bold");
}

module slot_block(w, h, cl, at) {
    translate(at) difference() {
        translate([-(w + 2 * cl) / 2 - 2, -6, 0]) cube([w + 2 * cl + 4, 12, h + 2 * cl + 2 + plate]);
        translate([-(w + 2 * cl) / 2, -7, plate]) cube([w + 2 * cl, 14, h + 2 * cl]);
    }
}

difference() {
    union() {
        translate([0, 0, 0]) cube([90, 78, plate]);
        // row 1: cell rings
        for (i = [0:2]) translate([16 + i * 29, 62, 0]) difference() {
            cylinder(d = 18.65 + i * 0.15 + 3.2, h = 8);
            translate([0, 0, -1]) cylinder(d = 18.65 + i * 0.15, h = 10);
        }
        // row 2: XT30U
        for (i = [0:2]) slot_block(xt30_w, xt30_h, 0.2 + i * 0.1, [16 + i * 29, 35, 0]);
        // row 3: XT60H
        for (i = [0:2]) slot_block(xt60_w, xt60_h, 0.2 + i * 0.1, [16 + i * 29, 12, 0]);
    }
    for (i = [0:2]) {
        tag(str(".", 65 + i * 15), [16 + i * 29, 47.5]);
        tag(str("+.", 2 + i), [16 + i * 29, 26]);
        tag(str("+.", 2 + i), [16 + i * 29, 3]);
    }
}
