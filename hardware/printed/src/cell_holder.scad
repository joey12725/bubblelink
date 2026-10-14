// Cell holder (upper/lower spacer) for the 2S5P pack, 10x Samsung 25R.
//
// Two offset rows of five. Row A is one parallel group, row B is the other.
// Print one of each:
//   part = "mid"   the end where the groups join in series (midpoint bus;
//                  every tab on this face is at the same potential)
//   part = "term"  the other end, carrying the separate pack + and - buses.
//                  It is a mirror image of "mid", because the offset pattern
//                  does not line up with itself when flipped over.
//
// The lip face (z = 0) faces outward on the finished pack. Print lip-side
// down, no supports. PETG.

include <params.scad>

part = "mid";

p = cell_pitch;
row_dy = p * sin(60);
r_out = cell_bore / 2 + holder_wall;
span_x = 2.25 * p + r_out;        // half-length of the cell group outline

m = part == "mid" ? 1 : -1;       // x mirror for the "term" holder

// Row A has cells at x = -2.25p .. 1.75p, row B at -1.75p .. 2.25p.
function cell_xy(i) = i < 5 ? [m * (i - 2.25) * p, -row_dy / 2]
                            : [m * (i - 5 - 1.75) * p, row_dy / 2];

// No ears: the dry core's battery bay fence locates the block and ribs on
// the lid hold it down.
module outline() {
    hull() for (i = [0:9]) translate(cell_xy(i)) circle(r = r_out);
}

// Engraved on the lip face; mirrored so it reads correctly from outside.
module label(xy, s, size = 4, rot = 0) {
    translate([xy[0], xy[1], -0.01]) rotate(rot) mirror([1, 0, 0])
        linear_extrude(0.6)
            text(s, size = size, halign = "center", valign = "center",
                 font = "Liberation Sans:style=Bold");
}

difference() {
    linear_extrude(holder_t) outline();
    for (i = [0:9]) translate(cell_xy(i)) {
        translate([0, 0, holder_lip]) cylinder(d = cell_bore, h = holder_t);
        translate([0, 0, -1]) cylinder(d = cap_window, h = holder_t);
    }
    // row letters in the land between the first two cells of each row
    label([m * -1.75 * p, -row_dy / 2], "A");
    label([m *  1.75 * p,  row_dy / 2], "B");
    label([m * -0.75 * p, -row_dy / 2], part == "mid" ? "M" : "T");
}
