// Duo: a compact, rounded two-head BubbleLink gun, made as a left/right pair.
//
// Two donor blower heads (blower_head.scad) stacked one above the other behind round front
// windows, the umbilical dock built into the back (the standard gun dock's three
// connections: XT30U, hose inlet, carabiner bar), and a Gardner Bender GSW-21
// push-on/push-off button pressed by a printed trigger. All purple, R 10 rounds everywhere.
//
// THREE PRINTED PIECES per gun, nothing else:
//   - main half:  one side of the body with the grip (solid, flush with this face), the
//                 umbilical dock, the switch bulkhead, half the trigger housing and one
//                 pivot peg, the head sleeves with their crush ribs, the glue-pad pegs.
//                 Build everything into it.
//   - cover half: the other side of the body, half the trigger housing and the other pivot
//                 peg. Glued on last.
//   - trigger.
// The halves split on the centre plane through both head axes. The switch, its bores and
// the trigger slot sit on that plane too, so every hole is open at the seam and both halves
// print outer face down with no supports. The trigger housing is a short full-width block
// under the body, ahead of the grip. Two glue pads (plates that meet face to face at the
// seam, each on a post fused to the nearest wall) add area to the rim; a 4 mm peg on each
// main-half pad drops into a hole in the matching cover pad.
//
// Heads: ring A's face sits against the front wall's 2 mm lip. The main half's sleeves
// carry crush ribs that just touch the ring; the cover half's sleeves are ~0.8 mm clear with
// no ribs, so the cover always closes even if a ring is a little bigger than modelled.
// Hot glue the heads in their sleeves.
//
// SWITCH: Gardner Bender GSW-21 (UPC 0 32076 89021 6), push-on / push-off maintained SPST,
// 6" 18 AWG leads, rated 8 A 125 VDC. Sizes from the GB spec sheet (GSW-21_SPEC.pdf),
// checked against Joey's photo on the cm mat (bushing 11.9, knurl nut ~15, cap ~10):
//   body 15.6 deep (along the axis) x 24.9 x 15.3; leads leave one 24.9-end, the 2 x 1
//   keyway in the bushing is at the other. Bushing 15/32-32, 14.4 long; button cap dia 10.3,
//   10.3 past the bushing (tip 40.3 from the back of the body, released). Panel hole 12.2
//   (+0.2) with a 1.2 mm key tab. 1 hex nut + 1 knurled nut. Travel to latch: 5 mm (Joey
//   measured it).
// It hangs on a bulkhead 45 degrees down and forward, its button just behind the trigger.
// Stack along the button axis (s, from the back of the body): body 0..15.6 | hex nut
// 15.6..18.2 | bulkhead 18.2..21.2 (keyed hole) | knurled nut 21.2..24.0 | bushing end 30 |
// button tip 40.3. FITTING: run the hex nut all the way down to the body and the knurled
// nut on loosely, lay the switch in the main half with the bulkhead between the nuts (key
// tab in the keyway), then spin the knurled nut snug. That puts the button tip on the
// trigger's nub. If the trigger then sits pushed forward off the button, back the hex nut
// off (0.8 mm per turn) and re-snug. The cover's half of the bulkhead is 0.25 mm thinner
// each side round the hole, so it slides in between the nuts already snugged on the main
// half. (If the real keyway isn't where the key tab is, trim the tab off: the body's
// pocket stops the switch turning anyway.)
//
// TRIGGER: hangs in a slot on the seam and pivots on two 5 mm pegs printed into the slot
// walls (no pin): drop it onto the main half's peg; the cover's peg goes into a looser
// hole, so the main peg alone locates it. Its nub rests on the button's tip; a pull pushes
// the button along its axis (pivot 18 mm off the axis and 3 mm ahead of the nub; the nub
// drifts up to 3.2 mm off the axis, on the 10.3 cap face). The switch's own spring pushes
// it back. The hard stop is a boss on the grip's front strap that the back of the blade
// meets at full pull (tr_push of button travel), down at finger height, so a hard squeeze
// goes straight into the grip, not through the pivot pegs. A 1 mm moat round the slot and
// the button bore at the seam catches glue squeeze-out: keep glue 5 mm clear of them, and
// try the trigger (halves held with rubber bands) before gluing.
//
// One hand, two guns. The left gun's grip is on its right, the right gun's on its left; the
// right gun is the mirror image of the left one (the heads sit the same way up in both).
// The switches latch, so switch both on, then hold the guns grip to grip: the grips make
// one 56 mm handle. Optional 6 x 3 mm magnets in each grip-side face hold the pair together
// (left gun north out, right gun south out).
//
// Coordinates (mm): +x forward (bubbles go +x), +z up, +y to the left. y = 0 is the left
// gun's grip-side face (it faces right), y = T its cover face, y = T/2 the seam. Front
// face at x = 0.
//
// part = "main" | "cover" | "trigger"   print parts (halves outer face down, trigger flat)
//        "test_main" | "test_cover"     the trigger housing region of each half, to print first
//        "assembly" | "open" | "pair"   renders
// hand  = "L" (main half at y = 0) or "R" (its mirror image).
// Units: millimetres. No supports: every downward face is 45 degrees or shallower.

include <params.scad>
use <blower_head.scad>
use <gun_dock.scad>

part = "assembly";
hand = "L";
e = 0.01;

// ---------------------------------------------------------------- donor heads
HR   = head_rings();          // [ring A dia, ring A length, ring B dia, rim]
RA   = HR[0] / 2;             // 24.75
A_h  = HR[1];                 // 15
roll = 20;                    // each head turned 20 deg about its axis (gear tab up, toward +y):
                              // keeps it within +-24.8 across the gun, and lets the two nest
pitch = 57;                   // head axis spacing: the lower head's gear tab (14 wide since the
                              // part 51 fit test) clears the upper ring A by 1.5 mm
lip_w = 2.0;                  // front wall laps over the 3 mm stationary rim (= part 51)
h_clr = 1.05;                 // ring A to sleeve and walls, radial: 0.4 into the side walls,
                              // so the cut never grazes a wall face
rib_h = h_clr;                // crush ribs (main half only): their tips just touch the modelled ring
rib_w = 1.6;

// ---------------------------------------------------------------- shell
w   = 2.4;                    // wall (= dock_wall, so the standard dock hole fits)
fw  = 3.4;                    // front wall: 1 mm thicker than the rest, so the wall in front of
                              // the gear-tab clearance stays thick enough at the front-top corner
R   = 10;                     // edge round into the flat side faces
Rc  = 5.6;                    // inside corner round (smaller than R - w: the heads come close)
T   = 55.6;                   // thickness: heads +-24.8 + 0.6 clearance + walls
L   = 88;                     // front face to back face
zb  = -31;                    // bottom (lower head barb 27.9 below its axis)
zt  = 92.5;                   // top: upper head's gearbox 31.5 above its axis, plus 1.6 clearance
r_ft = 8;  r_fb = 6;          // front corners: the tab and the ring A rim come close here
r_rt = 24; r_rb = 10;         // back corners
mid = T / 2;

// ---------------------------------------------------------------- grip: raked, half the gun thick, flush with y = 0
g_front = -48;                // front strap at the body's underside
g_back  = -86;                // back strap there (38 deep)
g_len   = 76;                 // below the body
g_rake  = 12;
g_fil   = 6;                  // fillet where the grip meets the body
gy      = mid - 0.05;         // grip: y 0 .. gy
function strap_x(z) = g_front + (z - zb) * tan(g_rake);

// ---------------------------------------------------------------- switch (GB GSW-21)
sw_body  = [15.6, 24.9, 15.3];   // along axis, y, z
sw_bush  = 14.4;                 // thread length past the body
sw_thd   = 11.9;                 // 15/32-32
sw_cap_d = 10.3;
sw_tip   = 40.3;                 // button tip, released
sw_hex_t = 2.6;  sw_hex_af = 14.3;    // hex nut: estimate (9/16" AF); its pocket also takes 5/8"
sw_knurl_t = 2.8;  sw_knurl_d = 15.2; // knurled nut, from the photo (~15 x 2.8)
sw_hole  = 12.2 + 0.2;           // spec 12.2 +0.2/-0; printed holes shrink, so top of the band
sw_key_w = 1.4;  sw_key_h = 1.1; // spec tab 1.5 wide, 1.2 deep: a hair under, so it slides in
s_hex  = sw_body[0];             // 15.6
s_bulk = s_hex + sw_hex_t;       // 18.2 bulkhead back face
bulk_t = 3.0;
s_knurl = s_bulk + bulk_t;       // 21.2
s_bush_end = sw_body[0] + sw_bush;   // 30.0
hex_r    = 9.6;                  // hex nut pocket (dia 19.2: clears the corners of a 5/8" AF nut too)
knurl_r  = 8.8;                  // knurled nut pocket (dia 17.6)
knurl_l  = sw_knurl_t + 2.2;     // ...5 long: lay the switch in with the nut 2 mm loose, then spin it snug
back_clr = 1.5;                  // behind the body: room to back the hex nut off ~2 turns
cap_r    = 6.4;                  // clearance round the 10.3 cap (dia 12.8)
btn_z    = -41.5;                // where the button axis meets the front strap
sw_tilt  = 45;                   // button axis: 45 degrees down and forward
P_btn    = [strap_x(btn_z), btn_z];
U        = [cos(sw_tilt), -sin(sw_tilt)];      // along the button axis, toward the tip
V        = [sin(sw_tilt), cos(sw_tilt)];       // perpendicular to it, up and forward
P0       = P_btn - 40.75 * U;    // back of the switch body (x, z): sits in the body, clear of the dock

// ---------------------------------------------------------------- trigger
T_c    = P0 + sw_tip * U;        // button tip, released
nub_r  = 2.5;
N_c    = T_c + nub_r * U;        // nub centre, touching the tip
P_t    = N_c + 18 * V + 3 * U;   // trigger pivot (x, z)
r_nub  = norm(N_c - P_t);        // 18.25
tr_push = 7.0;                   // button travel at the stop: latches at 5 (measured), 6.5 wanted,
                                 // +0.5 in case the switch sits a little further back
tr_pull = asin((tr_push + 3) / r_nub) - atan2(3, 18);   // degrees (23.8): push = 18 sin a + 3 cos a - 3
tr_t   = 12;                     // trigger thickness (y)
slot_hw = tr_t / 2 + 0.6;        // half width of the slot
peg_t_d = 5.0;  peg_t_in = 3.5;  // pivot pegs: dia, and how far into the trigger
peg_t_clr = 0.3;                 // radial, in the trigger's hole on the main side
peg_t_clr2 = 0.6;                // ...on the cover side: the main peg alone locates the trigger
hub_r  = 5.75;

// ---------------------------------------------------------------- umbilical dock, built into the main half
// The standard gun dock's connections (gun_dock.scad: same XT30U window, inlet barb, outlet
// barbs and carabiner bar), laid out down the back face of the main half. The main half
// prints with the gun's y axis up, so: the XT30U pocket stands on edge with a 45-degree
// peak; the carabiner bar is an upright post under a 45-degree roof; the hose inlet points
// 45 degrees toward the outer side (a barb straight back would stick out sideways with
// nothing under it), so the umbilical hose comes in from behind and a little from the
// outer side; the two outlets point up out of the open half (+y), so the head hoses push
// on from above.
dk_lip = 0.8;  dk_lipw = 0.6;            // XT30U front lip: depth, and on the long sides
xt_pw = xt30_w + 2 * fit_clear;          // 10.6: XT30U pocket (gun y)
xt_ph = xt30_h + 2 * fit_clear;          //  5.7               (gun z)
xt_z = 43;  xt_y0 = 11;  xt_d = 16;      // window centre height, pocket bottom (y), pocket depth behind the lip
hs_z = 55;  hs_y = 18;                   // hose socket centre on the back face (12 above the XT30U, as on the dock)
hs_sock = 7.6;  hs_tip_in = 2;  hs_len = 10;   // socket dia; barb tip 2 mm in from the face; barb length
hs_j = 18;                               // inlet bore runs 18 mm down the socket axis to the manifold
out_z = 65;  out_x = [-80.5, -72];  out_y = 12;   // outlets: barbs point +y from a block top at out_y
cb_rod = 8;  bar_w = 7;  bar_t = 6;      // carabiner wire; bar width (z), depth (x): as gun_dock.scad
cb_open = cb_rod + 5;  cb_w = cb_rod + 2.5;  cb_tun = bar_t + cb_rod + 1.5;
cb_len = 2 * cb_open + bar_w;            // 33
cb_y0 = 8;  cb_z0 = 0;                   // pocket floor (y) and bottom end (z)

// ---------------------------------------------------------------- glue pads + pegs (closing the shell)
// (x, z) of the pad, and the wall point its post is fused to
pads   = [[-72, 78, [-79, 86]],     // behind the upper head: post into the top back corner
          [-46, -23, [-46, -31]]];  // under the lower head's back: post down into the floor
pad_r  = 4.5;                 // post across the seam
pad_sq = 13;                  // square glue plate at the seam, in each half
pad_sq2 = [10, 10];           // ...the lower one 10 x 10, between the lower head and the switch
pad_t  = 1.6;                 // plate thickness
pad_fl = 6;                   // 45-degree flare from the post up to the plate
peg_pd = 4;  peg_h = 4;  peg_clr = 0.2;

// ---------------------------------------------------------------- magnets (optional: hold a pair together)
mag_d = 6.0;  mag_h = 3.0;    // 6 x 3 mm neodymium discs (set to yours)
mag_clr = 0.15;
pair_mags = [[-15, pitch / 2], [-74, cb_z0 + cb_len / 2], [-72, -52], [-82, -93]];   // grip-side face (x, z); one under the carabiner pocket

$fn = 64;
kfn = 48;

// ================================================================ helpers
// 2D drawn in (x, z), extruded across y0..y1
module side_extrude(y0, y1) translate([0, y1, 0]) rotate([90, 0, 0]) linear_extrude(y1 - y0) children();
// rounding tool: sphere with 45-degree cones at both poles (along y): a round on a face that
// prints on the bed turns into a 45-degree chamfer, so nothing overhangs
module kround(r) rotate([90, 0, 0]) hull() {
    sphere(r, $fn = kfn);
    for (s = [-1, 1]) translate([0, 0, s * (r - e)]) cylinder(r = r * (sqrt(2) - 1), h = 2 * e, center = true, $fn = kfn);
}
// head frame -> gun: head axis (z) points back along -x, face at x = -fw
module at_head(i) translate([-fw, mid, i * pitch]) rotate([0, -90, 0]) rotate([0, 0, roll]) children();
module mirror_seam() { children(); translate([0, T, 0]) mirror([0, 1, 0]) children(); }
// switch frame: +x along the button axis (toward the button), origin at the centre of the
// back face of the body, +z = the body's 15.3 direction, y = its 24.9 direction (leads
// toward +y, keyway toward -y), centred on the seam
module sframe() translate([P0[0], mid, P0[1]]) rotate([0, sw_tilt, 0]) children();
function on_axis(s) = P0 + s * U;

// ================================================================ outline
module core_2d() hull() {                 // the body box
    translate([-r_ft, zt - r_ft]) circle(r_ft);
    translate([-r_fb, zb + r_fb]) circle(r_fb);
    translate([-L + r_rt, zt - r_rt]) circle(r_rt);
    translate([-L + r_rb, zb + r_rb]) circle(r_rb);
}
// trigger housing: a short block under the body round the switch's nuts and cap, out to
// the trigger's pivot. Full width (the switch sits on the seam), solid apart from the
// switch's bores and the trigger slot.
module block_2d() hull() {
    translate(on_axis(s_hex + sw_hex_t / 2)) circle(r = hex_r + 2.8, $fn = 48);
    translate(on_axis(s_knurl + knurl_l)) circle(r = knurl_r + 2.8, $fn = 48);
    translate(T_c) circle(r = 9, $fn = 48);
    translate(P_t) circle(r = 9, $fn = 48);
    translate([-66, zb + 2]) square([40, 8]);
}
module body_2d() offset(r = -4) offset(delta = 4) { core_2d(); block_2d(); }
module grip_base_2d() let(t = tan(g_rake))
    offset(r = 11) offset(delta = -11)
        polygon([[g_back + 30 * t, zb + 30], [g_front + 30 * t, zb + 30],
                 [g_front - g_len * t, zb - g_len], [g_back - g_len * t, zb - g_len]]);
module gun_2d() offset(r = -g_fil) offset(delta = g_fil) { body_2d(); grip_base_2d(); }

// ================================================================ trigger
module trigger_2d() difference() {
    union() {
        translate(P_t) circle(r = hub_r, $fn = 48);                                        // hub
        hull() { translate(P_t) circle(r = 3.5, $fn = 32); translate(N_c) circle(r = nub_r, $fn = 32); }   // arm + nub
        hull() {                                                                           // finger blade, leaning forward
            translate(P_t) circle(r = 4.5, $fn = 32);
            translate(P_t + [0, -15]) circle(r = 4.6, $fn = 32);
            translate(P_t + [1.5, -26]) circle(r = 5, $fn = 40);
        }
    }
    translate(P_t + [8.3, -20]) circle(r = 5.0, $fn = 48);                                 // finger curve
}
// pivot hole: snug on the main side (y < mid), looser on the cover side; 0.8 x 45-degree
// countersink at both ends (clears the pegs' root fillets, leads the cover's peg in)
module pivot_hole() translate([P_t[0], 0, P_t[1]]) rotate([-90, 0, 0]) {     // local z = gun y
    r1 = peg_t_d / 2 + peg_t_clr; r2 = peg_t_d / 2 + peg_t_clr2;
    translate([0, 0, mid - tr_t / 2 - 1]) cylinder(r = r1, h = tr_t / 2 + 1 + e, $fn = 40);   // main side
    translate([0, 0, mid]) cylinder(r = r2, h = tr_t / 2 + 1, $fn = 40);                     // cover side
    translate([0, 0, mid - tr_t / 2 - e]) cylinder(r1 = r1 + 0.8, r2 = r1, h = 0.8 + e, $fn = 40);
    translate([0, 0, mid + tr_t / 2 - 0.8]) cylinder(r1 = r2, r2 = r2 + 0.8, h = 0.8 + e, $fn = 40);
}
module trigger_at(a = 0) translate([P_t[0], 0, P_t[1]]) rotate([0, a, 0]) translate([-P_t[0], 0, -P_t[1]]) difference() {
    side_extrude(mid - tr_t / 2, mid + tr_t / 2) offset(r = 0.8) offset(delta = -0.8) trigger_2d();
    pivot_hole();
}
module trigger_print() rotate([90, 0, 0]) translate([0, tr_t / 2 - mid, 0]) trigger_at(0);
// the room the trigger swings through (+0.5 all round): from 1.5 degrees forward of rest to
// exactly tr_pull, where the slot's end stops it (~1.5 deg later, through the 0.5). One 2D
// union, extruded once. The hub pokes 1.8 mm up through the floor into the body; being
// round, it plugs its own opening (0.5 mm gap round it, 1 mm each side), so wires can't
// drop into the slot.
pull_steps = concat([for (a = [-1.5 : 1.5 : tr_pull]) a], [tr_pull]);
module trigger_sweep_2d() for (a = pull_steps) translate(P_t) rotate(-a) translate(-P_t) offset(r = 0.5) trigger_2d();
module trigger_sweep() side_extrude(mid - slot_hw, mid + slot_hw) trigger_sweep_2d();
// the two pivot pegs, standing out of the slot walls (each prints standing up): 0.5 x 45
// root fillet, 0.8 mm tip chamfer
module trigger_pegs() for (h = [-1, 1])
    translate([P_t[0], mid + h * (slot_hw + e), P_t[1]]) rotate([h < 0 ? -90 : 90, 0, 0]) let(l = slot_hw - tr_t / 2 + peg_t_in + e) {
        cylinder(d = peg_t_d, h = l - 0.8, $fn = 40);
        translate([0, 0, l - 0.8 - e]) cylinder(d1 = peg_t_d, d2 = peg_t_d - 1.6, h = 0.8 + e, $fn = 40);
        cylinder(d1 = peg_t_d + 1.0, d2 = peg_t_d, h = 0.5, $fn = 40);
    }
// the stop: a boss on the grip's front strap that the back of the blade meets at tr_pull.
// Its underside (the -y end, facing down as printed) is a 45-degree slope back to the strap.
function rot_t(p, a) = let(r = p - P_t) P_t + [r[0] * cos(a) + r[1] * sin(a), -r[0] * sin(a) + r[1] * cos(a)];
blade_c1 = P_t + [0, -15];  blade_c2 = P_t + [1.5, -26];       // blade circles (r 4.6, 5)
blade_nb = let(d = (blade_c2 - blade_c1) / norm(blade_c2 - blade_c1)) [d[1], -d[0]];   // back normal (-x)
stop_q1 = rot_t(blade_c1 + 4.8 * blade_nb + 0.5 * (blade_c2 - blade_c1), tr_pull);          // halfway down the blade
stop_q2 = rot_t(blade_c2 + 5.0 * blade_nb, tr_pull);
module stop_2d() polygon([stop_q1, stop_q2, [strap_x(stop_q2[1]) - 1.5, stop_q2[1]], [strap_x(stop_q1[1]) - 1.5, stop_q1[1]]]);
module stop_boss() hull() {
    side_extrude(22, gy) stop_2d();
    side_extrude(13, gy) polygon([[strap_x(stop_q2[1]) - 1.5, stop_q2[1]], [strap_x(stop_q2[1]) - 1.2, stop_q2[1]],
                                  [strap_x(stop_q1[1]) - 1.2, stop_q1[1]], [strap_x(stop_q1[1]) - 1.5, stop_q1[1]]]);
}
// where the button bore passes the floor it would leave knife edges: a low hump across the
// floor wraps it in 1.6 mm of wall instead
module bore_hump() side_extrude(w, T - w) intersection() {
    hull() for (s0 = [24, 34]) translate(on_axis(s0)) circle(r = cap_r + 1.6, $fn = 48);
    translate([-200, zb]) square([400, 40]);
}
// glue moat: 1 mm round the slot and the button bore, 1 mm deep each side of the seam
module glue_moat() {
    side_extrude(mid - 1, mid + 1) offset(r = 1) trigger_sweep_2d();
    intersection() {
        sframe() translate([36, 0, 0]) rotate([0, 90, 0]) cylinder(r = cap_r + 1, h = s_knurl + 30 - 36, $fn = 64);   // round the button tip and nub
        translate([-200, mid - 1, -200]) cube([400, 2, 400]);
    }
}

// ================================================================ switch: model, cuts, bulkhead
module gsw21(pressed = 0) {
    color("#1d1d22") translate([0, -sw_body[1] / 2, -sw_body[2] / 2]) cube(sw_body);
    color("silver") {
        translate([sw_body[0], 0, 0]) rotate([0, 90, 0]) difference() {
            cylinder(d = sw_thd, h = sw_bush, $fn = 48);
            translate([-1, -sw_thd / 2 - 1, -1]) cube([2, 2, sw_bush + 2]);         // keyway toward -y
        }
        translate([s_hex, 0, 0]) rotate([0, 90, 0]) cylinder(d = sw_hex_af / cos(30), h = sw_hex_t, $fn = 6);
        translate([s_knurl, 0, 0]) rotate([0, 90, 0]) cylinder(d = sw_knurl_d, h = sw_knurl_t, $fn = 60);
    }
    color("#111") translate([s_bush_end - pressed, 0, 0]) rotate([0, 90, 0]) cylinder(d = sw_cap_d, h = sw_tip - s_bush_end, $fn = 40);
    // leads: only where they leave the body (18 AWG, flexible: they bend toward the XT30U)
    color("#222") for (dz = [-3, 3]) translate([4, sw_body[1] / 2, dz]) rotate([-90, 0, 0]) cylinder(d = 2.6, h = 8, $fn = 12);
}
// what the case must leave clear (switch frame): the body (+0.6, +1.5 behind) and its leads
// (+y), the hex nut, the bushing through the bulkhead, the knurled nut, and the bushing +
// cap out to the trigger
module sw_keepout() {
    c = 0.6;
    translate([-back_clr, -sw_body[1] / 2 - c, -sw_body[2] / 2 - c]) cube(sw_body + [back_clr, 2 * c, 2 * c]);
    translate([-back_clr, sw_body[1] / 2 - 1, -sw_body[2] / 2 - c]) cube([sw_body[0] + back_clr, 9, sw_body[2] + 2 * c]);   // leads: 8 mm to start their bend
    translate([s_hex - 0.2, 0, 0]) rotate([0, 90, 0]) cylinder(r = hex_r, h = sw_hex_t + 0.2 + e, $fn = 64);
    // bushing through the bulkhead (bigger than its keyed hole, so the surfaces never coincide)
    translate([s_bulk - 1, 0, 0]) rotate([0, 90, 0]) cylinder(d = sw_hole + 0.6, h = bulk_t + 2, $fn = 64);
    translate([s_knurl - e, 0, 0]) rotate([0, 90, 0]) {
        cylinder(r = knurl_r, h = knurl_l, $fn = 64);
        cylinder(r = cap_r, h = 30, $fn = 64);              // bushing + cap, out to the trigger
    }
}
// the bulkhead plate, with the keyed hole: key tab toward -y, in the main half
module sw_bulkhead(w_y, h_z) difference() {
    translate([s_bulk, -w_y / 2, -h_z / 2]) cube([bulk_t, w_y, h_z]);
    translate([s_bulk - 1, 0, 0]) rotate([0, 90, 0]) linear_extrude(bulk_t + 2) difference() {
        circle(d = sw_hole, $fn = 64);
        translate([-sw_key_w / 2, -sw_hole / 2 - 1]) square([sw_key_w, sw_key_h + 1]);
    }
}

// ================================================================ solids
module outer() minkowski() {      // one minkowski, so the body and grip surfaces never coincide
    union() {
        side_extrude(R, T - R) offset(delta = -R) body_2d();
        // grip: grip-side half only; overlaps the body core by 2 mm so no boundaries are shared
        side_extrude(R, gy - R) intersection() {
            difference() { offset(delta = -R) gun_2d(); offset(delta = -R - 2) body_2d(); }
            translate([-200, zb - 200]) square([400, 200 + 2 * g_fil + R]);
        }
    }
    kround(R);
}
module cavity() minkowski() { side_extrude(w + Rc, T - w - Rc) offset(delta = -w - Rc) core_2d(); kround(Rc); }

module front_windows() for (i = [0, 1]) translate([0, mid, i * pitch]) rotate([0, 90, 0]) {
    translate([0, 0, -w - 1]) cylinder(r = RA - lip_w, h = w + 2, $fn = 128);
    translate([0, 0, -1.2 + e]) cylinder(r1 = RA - lip_w, r2 = RA - lip_w + 1.2 + 0.6, h = 1.2 + 0.6, $fn = 128);  // 45-deg bevel
}

// half-sleeves round ring A: the side wedges only (41-140 deg from the top, both sides),
// leaving the top for the gear tab and the bottom for the hose barb and the gear tab of
// the head below
module sleeve_wedges() {
    module wedge() polygon(concat([[0, 0]], [for (a = [41 : 6 : 137]) 60 * [sin(a), cos(a)]], [[60 * sin(140), 60 * cos(140)]]));
    translate([-fw - A_h, 0, 0]) rotate([90, 0, 90]) linear_extrude(A_h + e) { wedge(); mirror([1, 0]) wedge(); }
}
module sleeves() for (i = [0, 1]) intersection() {
    outer();
    translate([0, mid, i * pitch]) difference() {
        sleeve_wedges();
        translate([-fw - A_h - 1, 0, 0]) rotate([0, 90, 0]) cylinder(r = RA + h_clr, h = A_h + 1 + e, $fn = 128);
    }
}
// crush ribs: main half only (rotating by +a puts them on the -y side)
module ribs() for (i = [0, 1]) translate([0, mid, i * pitch]) for (a = [62, 95, 128])
    rotate([a, 0, 0]) translate([-fw - A_h, -rib_w / 2, RA + h_clr - rib_h]) cube([A_h, rib_w, rib_h + 0.5]);

// glue pad: a post across the seam, fused to its wall, flaring at 45 degrees into a square
// plate on each side of the seam; the seam cuts it into two pads that meet face to face
module glue_pad(p, sq = [pad_sq, pad_sq]) {
    side_extrude(w, T - w) hull() { translate([p[0], p[1]]) circle(r = pad_r); translate(p[2]) circle(r = pad_r); }
    translate([p[0], 0, p[1]]) rotate([-90, 0, 0]) hull() {   // local z = gun y
        translate([0, 0, mid - pad_fl]) cylinder(r = pad_r, h = 2 * pad_fl);
        translate([0, 0, mid - pad_t]) linear_extrude(2 * pad_t) offset(r = 2) square([sq[0] - 4, sq[1] - 4], center = true);
    }
}
// peg on the main half's pad (stands up from the seam as printed), hole in the cover's
module seam_peg(p) translate([p[0], mid - e, p[1]]) rotate([-90, 0, 0]) {
    cylinder(d = peg_pd, h = peg_h - 0.6 + e);
    translate([0, 0, peg_h - 0.6]) cylinder(d1 = peg_pd, d2 = peg_pd - 1.2, h = 0.6);   // lead-in
}
module seam_hole(p) translate([p[0], mid - e, p[1]]) rotate([-90, 0, 0]) {
    cylinder(d = peg_pd + 2 * peg_clr, h = peg_h + 0.6);
    cylinder(d1 = peg_pd + 2 * peg_clr + 1, d2 = peg_pd + 2 * peg_clr, h = 0.5);           // mouth chamfer
}
// pair magnets: pocket from the grip-side face with a 45-degree cone roof (prints face down)
module pair_boss(p) translate([p[0], 0, p[1]]) rotate([-90, 0, 0]) cylinder(d = mag_d + 4, h = mag_h + 3.6);
module pair_pocket(p) let(r = mag_d / 2 + mag_clr, h = mag_h + 0.2)
    translate([p[0], 0, p[1]]) rotate([-90, 0, 0]) rotate_extrude($fn = 32) polygon([[0, -1], [r, -1], [r, h], [0, h + r]]);

// switch bulkhead: full width, square to the button axis, rising from the floor and both
// side walls; the seam splits it and its keyed hole
module bulkhead() intersection() { sframe() sw_bulkhead(T - 2, 26); outer(); }

// ================================================================ the built-in umbilical dock
// hose socket frame: local z along the socket axis into the gun (45 degrees: back face ->
// toward y = 0), origin where the axis meets the back face, local x = gun z
module at_hose() let(c = cos(45))
    multmatrix([[0, -c, c, -L], [0, -c, -c, hs_y], [1, 0, 0, hs_z], [0, 0, 0, 1]]) children();
function hose_pt(t) = [-L + t * cos(45), hs_y - t * cos(45)];   // (x, y) at t along the axis
hs_J = hose_pt(hs_j);                                           // manifold junction (x, y)
module house_2d(wd, ht) polygon([[-wd / 2, 0], [wd / 2, 0], [wd / 2, ht], [0, ht + wd / 2], [-wd / 2, ht]]);   // 45-degree peak
module tdrop_y(d) { circle(d = d, $fn = 24); rotate(45) square(d / 2); }   // teardrop, point +2D y
// solid blocks, inside the back wall (intersected with outer())
module dock_blocks() {
    // XT30U pocket boss
    translate([-L, w - 1, xt_z - xt_ph / 2 - 2]) cube([dk_lip + xt_d, xt_y0 + xt_pw + xt_ph / 2 + 1.6 - (w - 1), xt_ph + 4]);
    // hose socket + manifold: the socket's 1.6 mm wall, hulled down to the side wall, and a
    // block under the outlets
    hull() {
        at_hose() translate([0, 0, -10]) cylinder(r = hs_sock / 2 + 1.6, h = 10 + hs_tip_in + hs_len + 6, $fn = 48);
        translate([0, w - 1, 0]) scale([1, 0.001, 1]) at_hose() translate([0, 0, -10]) cylinder(r = hs_sock / 2 + 1.6, h = 10 + hs_tip_in + hs_len + 6, $fn = 48);
    }
    translate([-L, w - 1, hs_z - 3]) cube([out_x[1] + 3.5 + L, out_y - (w - 1), out_z + 4 - (hs_z - 3)]);
    // carabiner block: from the side wall up to the seam
    translate([-L, w - 1, cb_z0 - 2.5]) cube([cb_tun + 1.6, gy - (w - 1), cb_len + 5]);
}
module bar_2d() let(z0 = cb_z0 + cb_open) hull() {   // (x, z): face edges chamfered 0.8, back edges r 1.5
    translate([-L - 1, z0 + 0.8]) square([1.01, bar_w - 1.6]);
    translate([-L + 0.8, z0]) square([0.01, bar_w]);
    for (dz = [1.5, bar_w - 1.5]) translate([-L + bar_t - 1.5, z0 + dz]) circle(r = 1.5, $fn = 32);
}
module dock_cuts() {
    // XT30U: the male goes in from inside until its shroud stops on the lip; the window lets
    // the umbilical's female in. Both on edge, with 45-degree peaks
    translate([-L + dk_lip, 0, xt_z]) rotate([0, 90, 0]) linear_extrude(xt_d + 1) translate([0, xt_y0]) house_2d(xt_ph, xt_pw);
    translate([-L - 1, 0, xt_z]) rotate([0, 90, 0]) linear_extrude(1 + dk_lip + e) translate([0, xt_y0]) house_2d(xt_ph - 2 * dk_lipw, xt_pw);
    // hose socket: bore, 45-degree ceiling ending inside the barb root (runs out past the face)
    at_hose() let(rr = 4.0 / 2 - 0.3, ze = hs_tip_in + hs_len)
        rotate_extrude($fn = 48) polygon([[0, -12], [hs_sock / 2, -12], [hs_sock / 2, ze],
                                          [rr, ze + hs_sock / 2 - rr], [0, ze + hs_sock / 2 - rr]]);
    // carabiner pocket: two openings either side of the bar, a tunnel behind it, a
    // 45-degree roof over the tunnel, a 1 mm chamfer round the mouth (bottom and ends)
    difference() {
        union() {
            translate([0, 0, cb_z0]) linear_extrude(cb_len) polygon([
                [-L - 1, cb_y0], [-L + cb_tun, cb_y0], [-L + cb_tun, cb_y0 + cb_w],
                [-L + cb_tun / 2, cb_y0 + cb_w + cb_tun / 2], [-L, cb_y0 + cb_w], [-L - 1, cb_y0 + cb_w]]);
            hull() {   // (not along the top edge: the roof already slopes away from it)
                translate([-L - 1, cb_y0 - 1, cb_z0 - 1]) cube([1, cb_w, cb_len + 2]);
                translate([-L - 1, cb_y0, cb_z0]) cube([2, cb_w, cb_len]);
            }
        }
        side_extrude(cb_y0 - 3, mid + 1) bar_2d();
    }
}
// the barbs: added after the cuts
module dock_barbs() {
    at_hose() translate([0, 0, hs_tip_in]) barb(in_profile());
    for (ox = out_x) translate([ox, out_y, out_z]) rotate([-90, 0, 0]) barb(out_profile());
}
// fluid path: inlet bore down the socket axis to the junction, a teardrop channel up (z) to
// the outlets' level, one along x under both outlets, and a bore up each outlet
module dock_flow() {
    at_hose() translate([0, 0, -1]) cylinder(d = 1.8, h = 1 + hs_j + 0.9, $fn = 24);
    translate([hs_J[0], hs_J[1], hs_z]) linear_extrude(out_z - hs_z) tdrop_y(2.4);
    translate([out_x[0], hs_J[1], out_z]) rotate([0, 90, 0]) linear_extrude(out_x[1] - out_x[0]) tdrop_y(2.4);
    for (ox = out_x) translate([ox, hs_J[1], out_z]) rotate([-90, 0, 0]) cylinder(d = 1.2, h = out_y - hs_J[1] + 12, $fn = 16);
}

// ================================================================ the shell
module shell_solid() difference() {
    union() {
        shell_body();
        intersection() { ribs(); outer(); }
        bulkhead();
        trigger_pegs();
        stop_boss();
        dock_barbs();
    }
    dock_flow();
}
module shell_body() difference() {
    union() {
        difference() {
            outer(); cavity();
            // ring A clearance through the inner corner rounds, plus a 0.4 mm rim recess in the front wall
            for (i = [0, 1]) translate([-fw - A_h - 0.5, mid, i * pitch]) rotate([0, 90, 0]) cylinder(r = RA + h_clr, h = A_h + 0.9, $fn = 128);
            // 1 mm all round each gear tab (photo-measured, already grew once) and its mirror
            // image, so one shell fits both guns. Run out to the seam, so it prints open-topped;
            // it thins the inside of the front-top corner a little
            mirror_seam() for (i = [0, 1]) hull() {
                at_head(i) head_gear_tab(1);
                translate([0, mid - 1, 0]) scale([1, 0.001, 1]) translate([0, -mid, 0]) at_head(i) head_gear_tab(1);   // 1 past the seam
            }
        }
        intersection() { outer(); translate([-fw, -500, -500]) cube([fw, 1000, 1000]); }   // front wall: fw thick
        sleeves();
        for (i = [0 : len(pads) - 1]) intersection() { glue_pad(pads[i], i == 0 ? [pad_sq, pad_sq] : pad_sq2); outer(); }
        for (p = pair_mags) intersection() { pair_boss(p); outer(); }
        bore_hump();
        intersection() { dock_blocks(); outer(); translate([-200, -1, -200]) cube([400, gy + 1, 400]); }
    }
    front_windows();
    dock_cuts();
    for (p = pads) seam_hole(p);
    for (p = pair_mags) pair_pocket(p);
    sframe() sw_keepout();
    trigger_sweep();
    glue_moat();
}
module main_half() union() {
    intersection() { shell_solid(); translate([-200, -1, -200]) cube([400, mid + 1, 400]); }
    for (p = pads) seam_peg(p);
}
module cover_half() difference() {
    intersection() { shell_solid(); translate([-200, mid, -200]) cube([400, mid + 1, 400]); }
    // the cover's half of the bulkhead: 0.25 mm thinner each side round the hole
    sframe() for (s0 = [s_bulk - 1, s_knurl - 0.25]) translate([s0, 0, 0]) rotate([0, 90, 0]) cylinder(r = 9, h = 1.25, $fn = 64);
}
// test piece: the trigger housing region of each half (switch, nuts, pegs, stop), to print
// first and check the switch fit, the nut stack, the trigger and the button's bottom-out
test_box = [[-92, -20], [-66, -6]];   // x, z
module test_cut() translate([test_box[0][0], -1, test_box[1][0]]) cube([test_box[0][1] - test_box[0][0], T + 2, test_box[1][1] - test_box[1][0]]);

// assembled helpers (for check_duo_fit.py and renders)
module switch_asm(pressed = 0) sframe() gsw21(pressed);
module trigger_asm(a = 0) trigger_at(a);

// ================================================================ reference parts
module heads() for (i = [0, 1]) at_head(i) head(inlet = false);
// the head hoses pushed onto the outlets: 5.5 OD, 20 mm straight up before they bend (reference)
module head_hose_stubs() for (ox = out_x) translate([ox, out_y + 1.7, out_z]) rotate([-90, 0, 0]) difference() { cylinder(d = 5.5, h = 20); translate([0, 0, -1]) cylinder(d = 3.2, h = 22); }
// the XT30U male in its pocket (reference: AMASS envelope)
module xt30_male() color("#e8c840") translate([-L + dk_lip, xt_y0 + fit_clear, xt_z - xt30_h / 2]) cube([16, xt30_w, xt30_h]);

PURPLE = "#cdb4f0"; COVER = "#d9c6f6"; TRIG = "#a98ae0";   // all printed purple; shades only tell the parts apart in renders

// a = trigger angle; the button is pushed by the nub's travel along its axis
function push_at(a) = let(r = N_c - P_t, n = P_t + [r[0] * cos(a) + r[1] * sin(a), -r[0] * sin(a) + r[1] * cos(a)])
    max(0, -(n - N_c) * U);
module gun(h = hand, open = false, a = 0) {
    module m() if (h == "R") translate([0, T, 0]) mirror([0, 1, 0]) children(); else children();
    m() color(PURPLE) main_half();
    if (!open) m() color(COVER) cover_half();
    m() color(TRIG) trigger_asm(a);
    m() switch_asm(push_at(a));
    heads();
    m() xt30_male();
}

// ================================================================ output
// print orientation: outer face down; R = mirror image of L
module print_hand() if (hand == "R") mirror([1, 0, 0]) children(); else children();
module main_print() print_hand() rotate([90, 0, 0]) children();
module cover_print() print_hand() translate([0, 0, T]) rotate([-90, 0, 0]) children();
if (part == "main")             main_print() main_half();
else if (part == "cover")       cover_print() cover_half();
else if (part == "trigger")     trigger_print();
else if (part == "test_main")   main_print() intersection() { main_half(); test_cut(); }
else if (part == "test_cover")  cover_print() intersection() { cover_half(); test_cut(); }
else if (part == "assembly")    gun(hand, false);
else if (part == "open")        gun(hand, true);
else if (part == "pair")        { gun("L"); translate([0, -T - 0.2, 0]) gun("R"); }
