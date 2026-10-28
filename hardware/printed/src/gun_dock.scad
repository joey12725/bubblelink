// Gun dock: the standard umbilical connection panel for every BubbleLink gun shell.
//
// One part per gun: it sits in a hole in the shell wall, flush with the outside. From the
// outside you see a flat strip (65.5 x 20 mm) with three openings:
//   - XT30U window: the gun's MALE sits behind a 0.8 mm lip; the umbilical's gun-end
//     FEMALE plugs into it (power always comes from a female).
//   - Hose socket: a 4.8 mm barb (the size that fits the 3.5 x 5.5 umbilical silicone),
//     recessed in a socket so a dropped gun can't snap it off. Long 3.2 mm lead-in, so the
//     hose starts easily. Push the umbilical hose in; pull it straight out to undock.
//   - Carabiner bar: a recessed bar flush with the face. A locking carabiner that lives on
//     the umbilical's paracord loop clips round it. This bar takes the pull from a dropped
//     or yanked gun. Keep the paracord loop shorter than the hose and wire tails, so
//     neither the XT30U nor the hose is ever loaded.
// Inside the gun, n_out 3.0 mm barbs point straight back, one per head: n_out = 1 is a
// straight adapter, 2 a Y, 3-8 a manifold (two rows on an 8 mm pitch).
//
// Mounting in a shell. The face is flush with the shell's outer surface. The dock goes
// in from INSIDE the shell, through a hole whose inner edge has a 45-degree x 1.5 mm
// chamfer. The dock's 45-degree collar seats in that chamfer, so an outward pull (the
// carabiner) pushes the collar into the shell wall: the wall carries it in compression,
// not glue or screws. Glue (acetone weld if both are ASA, or hot glue round the collar
// inside) only has to stop it being pushed in, which docking does (~30 N).
// Shell rules: wall = dock_wall (2.4) at the dock, hole = gun_dock_hole(), keep the
// space in gun_dock_envelope() clear. Or union gun_dock() straight into a shell model.
//
// Coordinates: face at z = 0 (on the bed when printing), +z into the gun. XT30U window
// centre at the origin, wide axis along X; hose socket at x = 12 (the same spacing as on
// the umbilical brick, part 10); carabiner pocket along +X beyond it.
//
// part = "dock"     the dock with n_out outlets. Face down, no supports, ASA, 100% infill
//                   (or 6 walls): the bar and barbs are the strong bits.
//        "coupon"   four output barbs, 2.8 / 2.9 / 3.0 / 3.2 mm (1-4 dots). Print first and
//                   try the head hose on each; set out_peak to the one that grips and
//                   still pushes on by hand.
//        "plate"    a 2.4 mm wall with the standard hole and chamfer, and four M3 holes:
//                   a fit test for the dock, or a mounting plate for a gun that has no
//                   printed shell (zip-tie, screw or glue it on).
//        "envelope" keep-out volume for shell design (reference, don't print)
//        "assembly" dock in a plate, for renders
// Units: millimetres.

include <params.scad>

part  = "dock";
n_out = 2;          // heads fed by this dock, 1-8

// ---------------------------------------------------------------- shell interface
dock_wall = 2.4;    // shell wall thickness at the dock
dock_cham = 1.5;    // 45-degree chamfer on the hole's inner edge; the collar seats in it
hole_clr  = 0.2;    // per side, dock to hole
collar_x  = 2.5;    // collar overhang past the face outline (1.5 in the chamfer, 1 behind the wall)
collar_h  = 1.6;    // straight band above the cone (glue land)

// ---------------------------------------------------------------- XT30U (gun side = male)
xt_pw  = xt30_w + 2 * fit_clear;   // 10.6
xt_ph  = xt30_h + 2 * fit_clear;   //  5.7
xt_lip_t = 0.8;                    // front lip: the male's shroud rim stops on it (unplugging)
xt_lip_w = 0.6;                    // lip on the two long sides only; window 10.6 x 4.5 lets the female in

// ---------------------------------------------------------------- inlet: umbilical hose
in_x      = 12;     // socket centre
in_peak   = 4.8;    // = the 3/16" assortment barbs Joey found fit the 3.5 x 5.5 silicone
in_valley = 4.0;
in_tip    = 3.2;    // lead-in, under the 3.5 ID
in_lead   = 4.0;    // tip -> first peak, a long gentle taper
in_ridge  = 3.0;    // second ridge
in_bore   = 1.8;
sock_d    = 10;     // socket depth = barb length (tip flush with the face)
sock_dia  = 7.6;    // hose is ~6.4 OD stretched on the barb
sock_mouth = 1.2;   // 45-degree mouth chamfer

// ---------------------------------------------------------------- outlets: head hoses
out_peak   = 3.0;   // Joey: a 3.17 barb fits the head hose, just a touch big (coupon has 2.8-3.2)
out_flare  = 0.5;   // valley = peak - flare: a 0.25 mm step each side, so the ridges bite
out_valley = out_peak - out_flare;
out_tip    = out_peak - 0.8;        // lead-in, well under the hose ID
out_bore   = 1.2;   // clear with a 1.2 mm drill or a guitar string if it prints shut
out_lead   = 3.0;
out_ridge  = 2.0;
out_boss_d = 5.0;   // hose stop under each barb
out_boss_h = 1.2;
out_pitch  = 8;     // along X
out_row    = 4.5;   // rows at y = +-out_row
chan_d     = 2.4;   // manifold channels (teardrop, no bridging)

// ---------------------------------------------------------------- carabiner tie point
// Measure your carabiner: cb_rod = the thickest part of its wire where it wraps the bar;
// the gate has to open wider than the bar (bar_w x bar_t). Defaults suit mini lockers.
cb_rod  = 8;
bar_w   = 7;        // along X
bar_t   = 6;        // into the shell (Z); the face side is flush
cb_open = cb_rod + 5;              // each opening, along X
cb_w    = cb_rod + 2.5;            // pocket width (Y)
cb_tun  = bar_t + cb_rod + 1.5;    // tunnel ceiling behind the bar, before the 45-degree roof
px0     = in_x + sock_dia / 2 + sock_mouth + 3;   // pocket start (20)
p_len   = 2 * cb_open + bar_w;                    // 33

// ---------------------------------------------------------------- outline and depth
x0 = -(xt_pw / 2 + 3.7);           // -9
x1 = px0 + p_len + 3.5;            // 56.5
W  = 20;
cr = 3;                            // corner radius
chan_z = cb_tun + (cb_w / 2 - (out_row - chan_d / 2)) + 1.6 + chan_d / 2;   // clears the roof under the rows
Hb = ceil(chan_z + chan_d / 2 * 1.42 + 1.6);                                // back face (24)

$fn = 64;

function outlets(n) = n == 1 ? [[in_x, 0]]
    : [for (k = [0 : n - 1]) [in_x + floor(k / 2) * out_pitch, (k % 2 == 0 ? -1 : 1) * out_row]];

module outline(grow = 0) {
    offset(r = cr + grow) offset(delta = -cr)
        translate([x0, -W / 2]) square([x1 - x0, W]);
}

// ---------------------------------------------------------------- barbs (profiles as [r, z])
// inlet: tip at z = 0, root at sock_d; ridges taper up from the tip, sharp step on the root
// side (holds the hose). Printed tip-down, so every step narrows going up.
function in_profile() = [
    [in_tip / 2, 0], [in_peak / 2, in_lead], [in_valley / 2, in_lead],
    [in_peak / 2, in_lead + in_ridge], [in_valley / 2, in_lead + in_ridge],
    [in_valley / 2, sock_d + 2]];

// outlet: root at z = 0 (on the back face), tip up. 45-degree backs so nothing overhangs.
function out_profile(peak = out_peak, valley = out_valley, tip = out_tip) = let(
    bk = (peak - valley) / 2,
    z1 = out_boss_h + 0.8,
    z2 = z1 + bk + out_ridge,
    z3 = z2 + bk + out_lead)
  [[out_boss_d / 2, -1], [out_boss_d / 2, out_boss_h], [valley / 2, out_boss_h + 0.6],
   [valley / 2, z1], [peak / 2, z1 + bk], [valley / 2, z2],
   [peak / 2, z2 + bk], [tip / 2, z3]];

function out_height() = let(p = out_profile()) p[len(p) - 1][1];

module barb(profile) {
    rotate_extrude($fn = 48) polygon(concat([[0, profile[0][1]]], profile,
                                            [[0, profile[len(profile) - 1][1]]]));
}

module tdrop(d) { circle(d = d, $fn = 24); rotate(45) square(d / 2); }   // point toward 2D +y
module chan_x(xa, xb, y, z) translate([xa, y, z]) rotate([90, 0, 90]) linear_extrude(xb - xa) tdrop(chan_d);
module chan_y(ya, yb, x, z) translate([x, yb, z]) rotate([90, 0, 0]) linear_extrude(yb - ya) tdrop(chan_d);

// ---------------------------------------------------------------- the dock
module dock_solid() {
    z_c0 = dock_wall - dock_cham;
    // face plug with a 0.5 mm edge chamfer (shadow line round the panel)
    hull() {
        linear_extrude(0.01) outline(-0.5);
        translate([0, 0, 0.5]) linear_extrude(z_c0 - 0.5) outline();
    }
    // 45-degree seating collar + glue band
    hull() {
        translate([0, 0, z_c0]) linear_extrude(0.01) outline();
        translate([0, 0, z_c0 + collar_x]) linear_extrude(collar_h) outline(collar_x);
    }
    linear_extrude(Hb) outline();
}

module dock_cuts(n) {
    // XT30U: male goes in from the back until its shroud stops on the lip
    translate([-xt_pw / 2, -xt_ph / 2, xt_lip_t]) cube([xt_pw, xt_ph, Hb]);
    hull() {
        translate([-xt_pw / 2, -(xt_ph / 2 - xt_lip_w), -1]) cube([xt_pw, xt_ph - 2 * xt_lip_w, 1 + xt_lip_t]);
        translate([-xt_pw / 2 - 0.4, -(xt_ph / 2 - xt_lip_w) - 0.4, -1]) cube([xt_pw + 0.8, xt_ph - 2 * xt_lip_w + 0.8, 1]);
    }

    // hose socket round the inlet barb: flared mouth, 45-degree ceiling
    translate([in_x, 0, 0]) {
        translate([0, 0, -1]) cylinder(d = sock_dia, h = sock_d + 1);
        translate([0, 0, -0.01]) cylinder(d1 = sock_dia + 2 * sock_mouth, d2 = sock_dia, h = sock_mouth);
        translate([0, 0, sock_d - 0.01]) cylinder(d1 = sock_dia, d2 = in_valley, h = (sock_dia - in_valley) / 2);
    }

    // carabiner pocket: two openings, a tunnel behind the bar, 45-degree gable roof
    difference() {
        union() {
            translate([px0, -cb_w / 2, -1]) cube([p_len, cb_w, cb_tun + 1]);
            translate([px0, 0, cb_tun]) rotate([90, 0, 90]) linear_extrude(p_len)
                polygon([[-cb_w / 2, 0], [cb_w / 2, 0], [0, cb_w / 2]]);
            // 1 mm entry chamfer round the pocket mouth
            hull() {
                translate([px0 - 1, -cb_w / 2 - 1, -1]) cube([p_len + 2, cb_w + 2, 1]);
                translate([px0, -cb_w / 2, -1]) cube([p_len, cb_w, 2]);
            }
        }
        // the bar: square face edges chamfered 0.8, back edges rounded r 1.5 for the carabiner
        translate([px0 + cb_open, cb_w / 2 + 2, 0]) rotate([90, 0, 0]) linear_extrude(cb_w + 4)
            hull() {
                translate([0.8, -1]) square([bar_w - 1.6, 1.01]);
                translate([0, 0.8]) square([bar_w, 0.01]);
                translate([1.5, bar_t - 1.5]) circle(r = 1.5, $fn = 32);
                translate([bar_w - 1.5, bar_t - 1.5]) circle(r = 1.5, $fn = 32);
            }
    }
}

module dock_flow(n) {
    o = outlets(n);
    // inlet bore, up to the manifold
    translate([in_x, 0, -1]) cylinder(d = in_bore, h = chan_z + 1, $fn = 24);
    if (n > 1) {
        chan_y(-out_row, out_row, in_x, chan_z);
        last = max([for (p = o) p[0]]);
        if (last > in_x) for (s = [-1, 1]) chan_x(in_x, last, s * out_row, chan_z);
    }
    for (p = o) translate([p[0], p[1], chan_z - 0.5]) cylinder(d = out_bore, h = Hb + 20, $fn = 16);
}

module gun_dock(n = n_out) {
    difference() {
        union() {
            difference() { dock_solid(); dock_cuts(n); }
            translate([in_x, 0, 0]) barb(in_profile());
            for (p = outlets(n)) translate([p[0], p[1], Hb]) barb(out_profile());
        }
        dock_flow(n);
        // head count, engraved on the back face beside the XT30U
        for (k = [0 : n - 1]) translate([x0 + 2.2, -W / 2 + 2.5 + k * 1.95, Hb - 0.6]) cylinder(d = 1.1, h = 1, $fn = 12);
    }
}

// ---------------------------------------------------------------- for shell design
// Subtract from a wall of thickness dock_wall (outer surface at z = 0, +z inward).
module gun_dock_hole() {
    translate([0, 0, -1]) linear_extrude(dock_wall + 2) outline(hole_clr);
    // 45 degrees, offset so the collar seats with the face flush
    hull() {
        translate([0, 0, dock_wall - dock_cham + hole_clr]) linear_extrude(0.01) outline(hole_clr);
        translate([0, 0, dock_wall + 0.5]) linear_extrude(0.01) outline(dock_cham + 0.5);
    }
}

// Keep this clear inside the shell: body, collar, barbs + 15 mm of hose bend room behind
// them, and the XT30U wires.
module gun_dock_envelope(n = n_out) {
    translate([0, 0, dock_wall]) linear_extrude(Hb - dock_wall + out_height() + 15) outline(collar_x + 0.5);
}

// ---------------------------------------------------------------- coupon + plate
module barb_coupon() {
    peaks = [2.8, 2.9, 3.0, 3.2];
    difference() {
        union() {
            translate([-5, -5, 0]) cube([4 * 9 + 1, 12, 3]);
            for (i = [0 : 3]) translate([i * 9, 0, 3])
                barb(out_profile(peaks[i], peaks[i] - out_flare, peaks[i] - 0.8));
        }
        for (i = [0 : 3]) {
            translate([i * 9, 0, -1]) cylinder(d = out_bore, h = 30, $fn = 16);
            for (k = [0 : i]) translate([i * 9 - 2.4 + k * 1.6, 4.6, 2.4]) cylinder(d = 1, h = 1, $fn = 12);
        }
    }
}

module mount_plate() {
    m = 9;
    difference() {
        linear_extrude(dock_wall)
            offset(r = 4) offset(delta = -4) translate([x0 - m, -W / 2 - m]) square([x1 - x0 + 2 * m, W + 2 * m]);
        gun_dock_hole();
        for (x = [x0 - m / 2, x1 + m / 2], y = [-1, 1]) translate([x, y * (W / 2 + m / 2), -1]) cylinder(d = 3.4, h = 10);
    }
}

// ---------------------------------------------------------------- output
if (part == "dock") gun_dock(n_out);
else if (part == "coupon") barb_coupon();
else if (part == "plate") mount_plate();   // outer face on the bed, chamfer up
else if (part == "envelope") gun_dock_envelope(n_out);
else if (part == "assembly") {
    color("dimgray") gun_dock(n_out);
    color("tan", 0.6) mount_plate();
}
