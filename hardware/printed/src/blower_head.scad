// Donor bubble-blower head: reference model + first test mount.
//
// The head is the 7-wand wheel unit Joey stripped from the ~20 toy guns (2026-10-28).
// v2 (same day): rebuilt from a pixel-measured pass over the 16 photos. Each value below
// names the photo it came from (IMG_35xx). Scales: the Stanley tape (403 px/in on the
// face in 3547) and the cm labels on the Cricut mat (80-85 px/cm), with the mat shots
// corrected for camera height using ring A as the known size. Expect +-1 mm on ring A,
// +-2 mm on the rest, +-3 mm on the gearbox/pump interior.
//
// Coordinates (all parts): head axis = Z, front (bubble) face at z = 0, +z toward the
// back. Looking at the face from the front: +X is LEFT (gearbox column and yellow wheel
// gear), +Y is UP, -Y is the LED side, -X is the hose-barb side.
//
// part = "head"     reference model (for designing guns around; don't print)
//        "collar"   the test mount: C-collar over the front 9 mm of ring A, front lip on
//                   the stationary rim, crush ribs, a gap for the gear housing, a notch
//                   for the hose barb, and a flat pad with two zip-tie tunnels.
//        "gauge"    five 4 mm C-rings, ID 48.5-51.5 (1-5 bumps). Print these first: the
//                   smallest one that goes on without its gap spreading is ring A.
//        "assembly" head + collar
// Units: millimetres.

part = "collar";

// ================= head: measured =================
// Ring A (front wheel housing)
ringA_d   = 49.5;  // 3547: 780 px across at 403 px/in = 49.2; 3542 mat 49.5; 3543 side 49.5
ringA_h   = 15.0;  // 3543: face to the A/B step = 140 px at 9.5 px/mm (14.7); 3554: 15
rim_w     = 3.0;   // 3547: stationary rim band 48 px
wheel_r   = 20.6;  // 3547: outer edge of the wheel ring 327 px from centre
wheel_dep = 1.0;   // wheel face below the rim (3543/3545: the face ellipse sits in a lip)
well_dep  = 6.0;   // depth of the wheel well (the wheel turns in it)
loop_n    = 7;     // 7 toothed teardrop wands (3547, 3548)
loop_rc   = 13.5;  // wand centre radius
loop_len  = 10.5;  // tip-to-end
loop_wid  = 7.5;
hub_d     = 6.0;   // 3548: hub ~60 px at 305 px/in

// Ring B (fan housing)
ringB_d   = 47.5;  // 3543: 1 mm step each side from ring A (left edges 1140 vs 1150 px)
ringB_h   = 13.5;  // 3543: 750 -> 875 px = 13.2; 3553: 13.5
fan_r     = 18.5;  // fan visible through ring B's open back (3540, 3542)

// Gear housing alongside ring A at +X (3547 left bump, 3543 right tab)
gh_y0 = -7.0; gh_y1 = 7.0;     // 3547 read 11.4 wide; part 51 fit test (2026-10-28) showed the
                               // gear section wider than its 15 mm gap on both sides, so ~14 centred
gh_r1 = 30.0;                  // 3543: tab to 1660 px -> 30.0 from the axis
gh_z0 = 1.5;                   // 3543: 620 px (face at 605)
// yellow spur gear that drives the wheel (3553 edge-on, 3547/3548 at the rim)
yg_x = 26.0; yg_y = 2.0; yg_z = 32.5; yg_d = 12.0; yg_t = 3.5;

// Hose barb on ring A at -X (3554: tube lies along ring A, barb tip 6.8 mm from the face,
// held in a U-bracket; 3547: bracket shows at the right edge, Y ~ 0)
barb_ang  = 180;
barb_z0   = 5.0;   // bracket front edge
barb_z1   = 11.5;  // bracket back edge / barb root
brk_w     = 6.5;   // bracket width (tangential)
brk_h     = 3.8;   // bracket height above ring A
tube_od   = 5.0;   // silicone, 3554/3551
tube_id   = 3.0;

// LED + "+" light window on ring B at -Y (3553)
led_ang   = 262;   // 3553: LED centre ~3.5 mm toward -X from the -Y line
led_r     = 20.0;
led_z     = 29.0;  // dome against ring B's back edge, body to the rear
cross_ang = 260;   // 3553: "+" boss on ring B, 3 mm in front of the B step...
cross_z   = 18.0;
// rectangular snap loops ring B -> motor cradle (3553 above/below the LED; 3540 rear)
loopB_angs = [245, 279, 85, 165];

// Motor (FA-130 class: 20.1 can, 15.1 across flats, 25 long) on the axis (3550, 3552)
mot_d = 20.1; mot_flat = 15.1; mot_z0 = 12.5; mot_z1 = 37.0;
term_x = 7.0;      // 3543: tabs 150 px apart at 9.5 px/mm -> +-7.9; 3542: +-6.8
term_y = 9.0;      // tabs on the +Y side (3542 rear: Y +10.5 incl. solder)
// motor cradle box behind ring B (3543: 1230-1490 px -> X -15..+12)
cr_x0 = -14; cr_x1 = 13; cr_y0 = -12; cr_y1 = 11; cr_z1 = 38.5;

// Gearbox / pump block behind the cradle (3543, 3552, 3540-3542)
gb_x0 = -10; gb_x1 = 31.0;     // 3543 plate 1290-1660 px; 3553 top edge 455 px -> X 31
gb_y0 = -9;  gb_y1 = 8;
gb_z0 = 36;  gb_z1 = 53.0;     // 3543: plate bottom 1100 px; 3553 rear ~52-55
gbu_x0 = 13; gbu_z0 = 29;      // 3553: the upper (+X) part starts right behind ring B
// gearbox column: links the wheel-gear housing back to the gearbox (3543 right side)
col_x0 = 19.5; col_x1 = 31.0; col_y0 = -6; col_y1 = 7;
// pump rotor cover on the -Y face (3553): ~16 dia, centre pin
pump_x = 18; pump_z = 44; pump_d = 17; pump_t = 4;
// bosses on the +Y face (3552, 3543)
bosses = [[8, 46, 7, 3], [-3, 44, 5.5, 0], [24, 46, 6, 2.5]];   // [x, z, d, pin d]

$fn = 96;
e = 0.01;

// ================= collar / gauge =================
clr       = 0.3;     // radial clearance to ring A (ribs take up the rest)
wall      = 2.4;
coll_h    = 9;       // grips the front 9 of ring A's 15
lip_t     = 1.6;     // front lip
lip_w     = 2.0;     // reach over the 3 mm rim, stays clear of the wheel
gap_clr   = 5.0;     // each side of the gear housing tab; v1 (1.8 off a photo guess) was too tight
gap_w     = gh_y1 - gh_y0 + 2*gap_clr;   // 24
rib_n     = 8;
rib_h     = 0.5;
rib_w     = 1.6;
notch_w   = brk_w + 2.5;
pad_ang   = 90;      // +Y: clear of the LED (-Y), barb (-X) and gear (+X)
pad_w     = 30;
pad_t     = 6;
pad_len   = 26;      // stops short of the ring B loop at 85 deg (z ~ 24-31)
tie_w     = 5.5;
tie_t     = 2.2;
gauge_ids = [48.5, 49.25, 50.0, 50.75, 51.5];

R_in  = ringA_d/2 + clr;
R_out = R_in + wall;
RA = ringA_d/2; RB = ringB_d/2;

// ================= helpers =================
module polar(a, r, z) { rotate([0,0,a]) translate([r,0,z]) children(); }
module rbox(p0, p1, r = 1.5) {      // rounded box between two corners
  hull() for (x = [p0[0]+r, p1[0]-r], y = [p0[1]+r, p1[1]-r], z = [p0[2]+r, p1[2]-r])
    translate([x,y,z]) sphere(r, $fn = 16);
}
module tube_path(pts, od = tube_od) {
  for (i = [0:len(pts)-2]) hull() { translate(pts[i]) sphere(d = od, $fn = 20); translate(pts[i+1]) sphere(d = od, $fn = 20); }
}

// ================= head parts =================
module wand(len, wid) {             // toothed teardrop loop, lying in XY, tip at origin -> +X
  t = 0.9;
  difference() {
    hull() { translate([len - wid/2, 0]) circle(d = wid); circle(d = 1.6); }
    offset(-t) hull() { translate([len - wid/2, 0]) circle(d = wid); circle(d = 1.6); }
  }
  // teeth round the outer end
  for (a = [-150:12:150]) translate([len - wid/2, 0]) rotate(a) translate([wid/2, 0]) square([1.2, 0.6], center = true);
}

module wheel() {
  color("white") translate([0,0,wheel_dep]) {
    difference() { cylinder(r = wheel_r, h = 1.2); translate([0,0,-1]) cylinder(r = wheel_r - 1.2, h = 4); }
    cylinder(d = hub_d, h = 2.5);
    for (i = [0:loop_n-1]) rotate(360/loop_n*i) {
      translate([loop_rc - loop_len/2, 0, 0]) linear_extrude(1.2) wand(loop_len, loop_wid);
      rotate(180/loop_n) translate([hub_d/2 - 0.5, -0.6, 0]) cube([wheel_r - hub_d/2, 1.2, 1.0]);   // spoke
      translate([hub_d/2 - 0.5, -0.5, 0]) cube([loop_rc - loop_len/2 - hub_d/2 + 1, 1.0, 1.0]);      // stem
    }
  }
}

module ringA() {
  color("ivory") difference() {
    union() {
      cylinder(r = RA, h = ringA_h);
    }
    translate([0,0,-e]) cylinder(r = RA - rim_w, h = well_dep + e);        // wheel well
    translate([0,0,-e]) difference() {                                   // front edge chamfer (outer edge only;
      cylinder(r = RA + 1, h = 1.0); cylinder(r1 = RA - 0.4, r2 = RA + 0.6, h = 1.0); }  // it used to remove the whole face)
    translate([0,0,-1]) difference() { cylinder(r = RA + 1, h = 1.0 + 0.4); cylinder(r = RA - 0.4, h = 3); }
  }
}

module ringB() {
  color("ivory") difference() {
    translate([0,0,ringA_h - e]) cylinder(r = RB, h = ringB_h + e);
    translate([0,0,ringA_h]) cylinder(r = RB - 1.5, h = ringB_h - 1.5);
    // open back with 4 cradle arms
    difference() {
      translate([0,0,ringA_h + ringB_h - 3]) cylinder(r = fan_r, h = 5);
      for (a = [45:90:315]) rotate(a) translate([0,-2,ringA_h + ringB_h - 4]) cube([fan_r + 1, 4, 6]);
    }
  }
  // fan behind the open back
  color("lightgrey") translate([0,0,ringA_h + 2]) {
    cylinder(d = 8, h = 8);
    for (a = [0:72:359]) rotate(a) translate([3.5,-0.5,1]) rotate([25,0,0]) cube([fan_r - 4, 1, 7]);
  }
}

module gear_housing() {             // the bump beside ring A at +X, with the yellow gear
  color("ivory") {
    // tab alongside ring A
    translate([RA - 3, gh_y0, gh_z0]) cube([gh_r1 - RA + 3, gh_y1 - gh_y0, ringA_h + ringB_h - gh_z0]);
    // column back to the gearbox
    translate([col_x0, col_y0, ringA_h]) cube([col_x1 - col_x0, col_y1 - col_y0, gb_z0 - ringA_h + 1]);
  }
  color("gold") translate([yg_x, yg_y, yg_z - yg_t/2]) difference() {
    union() {
      cylinder(d = yg_d - 1.4, h = yg_t);
      for (a = [0:15:359]) rotate(a) translate([yg_d/2 - 0.8, -0.5, 0]) cube([0.8, 1.0, yg_t]);
    }
    translate([0,0,-1]) cylinder(d = 2, h = yg_t + 2, $fn = 16);
  }
}

module motor_and_cradle() {
  // cradle box with a window on +Y for the terminals
  color("ivory") difference() {
    rbox([cr_x0, cr_y0, ringA_h + ringB_h - 1], [cr_x1, cr_y1, cr_z1], 1.5);
    translate([-term_x - 2.5, cr_y1 - 4, mot_z1 - 3]) cube([2*term_x + 5, 6, 10]);
  }
  // motor can (flats facing +-Y) and end cap
  color("silver") intersection() {
    translate([0,0,mot_z0]) cylinder(d = mot_d, h = mot_z1 - mot_z0);
    translate([-15, -mot_flat/2, 0]) cube([30, mot_flat, 60]);
  }
  // terminals + 104 capacitor
  color("silver") for (s = [-1, 1]) translate([s*term_x - 1, term_y - 1.5, mot_z1 - 2]) cube([2, 3.5, 3]);
  color("sienna") translate([0, term_y + 1.5, mot_z1 + 3]) rotate([90,0,0]) cylinder(d = 5, h = 2, $fn = 24);
  // long snap fingers from the cradle up onto ring B's back (3550)
  color("ivory") for (s = [-1, 1]) translate([s*6 - 0.8, cr_y1 - 2, ringA_h + ringB_h - 6]) cube([1.6, 2, 8]);
}

module gearbox() {
  color("ivory") {
    rbox([gb_x0, gb_y0, gb_z0], [gb_x1, gb_y1, gb_z1], 2.5);
    rbox([gbu_x0, gb_y0, gbu_z0], [gb_x1, gb_y1, gb_z1], 2.5);
  }
  // bosses with pins on +Y
  color("ivory") for (b = bosses) translate([b[0], gb_y1 - e, b[1]]) rotate([-90,0,0]) {
    cylinder(d = b[2], h = 2.5);
    if (b[3] > 0) cylinder(d = b[3], h = 4.5, $fn = 24);
  }
  // pump rotor cover + centre pin on -Y, purple drive gear peeking out below it
  color("ivory") translate([pump_x, gb_y0 + e, pump_z]) rotate([90,0,0]) {
    cylinder(d = pump_d, h = pump_t);
    cylinder(d = 3.5, h = pump_t + 2, $fn = 24);
  }
  color("mediumpurple") translate([pump_x - 6, gb_y0 - 1.5, pump_z - 6]) rotate([90,0,0]) cylinder(d = 8, h = 1.5, $fn = 24);
}

module hose(inlet = true) {
  // U-bracket + barb on ring A at -X; tube runs back along ring A/B to the pump outlet
  rotate([0,0,barb_ang]) {
    color("ivory") difference() {
      translate([RA - 1, -brk_w/2, barb_z0]) cube([brk_h + 1, brk_w, barb_z1 - barb_z0]);
      translate([RA + tube_od/2 - 0.2, 0, barb_z0 - 1]) cylinder(d = tube_od + 0.2, h = 20, $fn = 24);
    }
    color("ivory") translate([RA + tube_od/2 - 0.2, 0, barb_z0 + 1]) cylinder(d = tube_id + 0.6, h = barb_z1 - barb_z0 + 1, $fn = 20);
  }
  rt = RA + tube_od/2 - 0.2;
  color("white", 0.55) {
    // outlet: barb -> back along the housing -> round the -Y side -> pump outlet
    tube_path([[-rt, 0, barb_z0 + 2], [-rt, 0, 24], [-RB - 2, -6, 31], [-16, -16, 40],
               [-2, -15, 47], [pump_x - 8, gb_y0 - 3, pump_z + 4]]);
    // inlet: pump -> off the head toward -X (illustrative; a gun shell supplies its own hose)
    if (inlet) tube_path([[pump_x - 9, gb_y0 - 3, pump_z + 7], [-6, -13, 52], [-24, -13, 56], [-45, -13, 60]]);
  }
}

module led_parts() {
  // 5 mm LED lying along the axis, dome forward against ring B's back edge, in a 2-prong holder
  polar(led_ang, led_r, led_z) {
    color("white", 0.6) { cylinder(d = 5, h = 5.5, $fn = 32); translate([0,0,0]) sphere(d = 5, $fn = 32); }
    color("ivory") for (s = [-1, 1]) translate([-1.5, s*3.4 - 0.7, 0.5]) cube([3.5, 1.4, 4.5]);
  }
  // "+" window boss on ring B
  color("ivory") polar(cross_ang, RB - 0.2, cross_z) rotate([0,90,0]) {
    translate([-1.6,-0.5,0]) cube([3.2,1,1]); translate([-0.5,-1.6,0]) cube([1,3.2,1]);
  }
  // rectangular snap loops from ring B onto the cradle
  color("ivory") for (a = loopB_angs) polar(a, RB - 0.3, ringA_h + ringB_h - 5) difference() {
    translate([0, -3, 0]) cube([1.2, 6, 9]);
    translate([-1, -1.7, 1.6]) cube([3.2, 3.4, 5]);
  }
}

module head(inlet = true) {
  ringA(); wheel(); ringB();
  gear_housing(); motor_and_cradle(); gearbox(); hose(inlet); led_parts();
}

// ================= collar =================
module c_cut(h) { translate([0, gh_y0 - gap_clr, -50]) cube([R_out + 50, gap_w, h + 100]); }

module collar() {
  difference() {
    union() {
      translate([0,0,-lip_t]) cylinder(r = R_out, h = lip_t + coll_h, $fn = 160);
      rotate([0,0,pad_ang]) translate([R_out - 1.5, -pad_w/2, -lip_t]) cube([pad_t + 1.5, pad_w, pad_len]);
    }
    cylinder(r = R_in, h = 200, $fn = 160);
    translate([0,0,-lip_t - 1]) cylinder(d = ringA_d - 2*lip_w, h = lip_t + 2, $fn = 160);
    translate([0,0,coll_h - e]) cylinder(r = R_out - 0.3, h = 200, $fn = 160);
    c_cut(coll_h);
    // barb + bracket notch, open at the back edge so the head slides in face-first
    rotate([0,0,barb_ang]) translate([R_in - 1, -notch_w/2, barb_z0 - 0.8]) cube([wall + 10, notch_w, 50]);
    rotate([0,0,pad_ang]) for (z = [3, pad_len - lip_t - 8])
      translate([R_out + (pad_t - tie_t)/2, pad_w, z]) rotate([90,0,0])   // 45-degree peaked roof: no bridge
        linear_extrude(2*pad_w) polygon([[0,0], [tie_t,0], [tie_t,tie_w], [tie_t/2, tie_w + tie_t/2], [0,tie_w]]);
  }
  for (i = [0:rib_n-1]) let(a = 360/rib_n*i + 360/rib_n/2)
    if (abs(a) > 25 && abs(a - 180) > 25 && abs(a - 360) > 25)
      rotate([0,0,a]) translate([R_in - rib_h, -rib_w/2, 0]) cube([rib_h + 0.2, rib_w, coll_h]);
}

// ================= gauge =================
module gauge_ring(id, n) {
  r_in = id/2; r_out = r_in + 2;
  difference() {
    cylinder(r = r_out, h = 4, $fn = 160);
    translate([0,0,-1]) cylinder(r = r_in, h = 7, $fn = 160);
    translate([0, gh_y0 - gap_clr, -1]) cube([r_out + 1, gap_w, 7]);
  }
  for (k = [0:n-1]) rotate([0,0,90 + (k - (n-1)/2)*9]) translate([r_out - 0.5, 0, 0]) cylinder(d = 2.4, h = 4, $fn = 24);
}
module gauge() { for (i = [0:4]) translate([(i % 3)*60, floor(i / 3)*60, 0]) gauge_ring(gauge_ids[i], i + 1); }

// ================= for gun shells (`use <blower_head.scad>`) =================
// [ring A dia, ring A length, ring B dia, stationary rim width]
function head_rings() = [ringA_d, ringA_h, ringB_d, rim_w];
// gear-housing tab beside ring A, in the head frame: a box from x = ringA_d/2 - 3 to gh_r1,
// y = gh_y0 .. gh_y1, z = gh_z0 .. the back of ring B. Grown by c on every side.
module head_gear_tab(c = 0) translate([ringA_d / 2 - 3, gh_y0 - c, gh_z0 - c])
  cube([gh_r1 - ringA_d / 2 + 3 + c, gh_y1 - gh_y0 + 2 * c, ringA_h + ringB_h - gh_z0 + c]);

// ================= dispatch =================
if (part == "head")          head();
else if (part == "collar")   translate([0,0,lip_t]) collar();
else if (part == "gauge")    gauge();
else if (part == "assembly") { head(); color("orange", 0.85) collar(); }
