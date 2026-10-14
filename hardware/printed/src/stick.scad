// BubbleLink stick (dry core v2): the whole pack except the bladder, in one
// upright column that stands beside the bladder in any bag. Supersedes
// dry_core.scad, pump_module.scad and port_insert.scad.
//
// Worn orientation: +z up, y = 0 against the wearer's back, x across.
//
//   CAP     control head. The CTRL PCB hangs under it. LEDs show through
//           0.6 mm skin windows, PRIME is a plunger under a TPU boot, and
//           the voltmeter and USB-C charge port are on top. A printed TPU
//           ring on its skirt seals against the inside of the tube, so the
//           seal needs no clamping force; two M3 screws (front/back) only
//           keep the cap on.
//   TUBE    plain shell; its floor is the bulkhead between dry and wet.
//   SLED    slides out of the top. The 2S5P block stands left of a central
//           spine; the BMS and breaker sit right of it behind a cross
//           panel; the bucks and ACS758 sit in front of the panel. The cap
//           presses the battery, which pins the sled to the bulkhead.
//   CUP     the wet chamber: pump, tees, check valve, bypass clamp. Bolts
//           to the bulkhead from below with 4 M3 screws reached from
//           underneath, and drains through its floor. Umbilicals, the
//           bladder feed and the service cables all leave through the floor.
//   Cables cross the bulkhead through a two-piece TPU grommet with knife-cut
//   slits, so the sled can still be pulled. It's a splash baffle, not a
//   watertight feedthrough.
//   Venting/thermal: incidental breathing only (grommet slits, cap ring).
//   Cell-fault pressure relief and enclosed-charging temperatures are NOT
//   verified; measure charger/BMS temperature on the first enclosed charge.
//
// Hardware: 6x M3 screws (2x 10 mm for the cap, 4x 12 mm for the cup),
// 6x M3 nuts glued into pockets, zip ties, glue. TPU: seal ring, two
// grommet halves, PRIME boot, two screw washers. Tape over the trimmer
// slots.
//
// part = tube | cap | sled | cup | plunger | ring | grommet | boot |
//        grommet_lo | grommet_hi | washer | membrane | assembly

include <params.scad>

part = "assembly";

// ------------------------------------------------------------ envelope
Wi = 94;      // inner width (x): battery + spine + 42 mm breaker bay
Di = 73;      // inner depth (y): 69.85 mm battery + clearance
ri = 1.0;     // inner corner radius (the battery block fills the corners)
t  = 2.4;     // wall
tb = 3;       // bulkhead (tube floor)
Zt = 148;     // tube rim, measured from the bulkhead's top face (room for a ~30 mm deep voltmeter)
tp = 3;       // cap plate
Hw = 50;      // cup inner height: pump 38-45 mm + hose barbs
tf = 3;       // cup floor

// ------------------------------------------------------------ cap skirt and seal
sk_h = 12;    // skirt depth into the tube
sk_t = 2.8;
sk_c = 0.3;   // skirt-to-tube clearance per side
gr_z = Zt - sk_h + 2;     // groove bottom (2 mm land below it)
gr_h = 2.6;
gr_d = 1.4;   // groove depth
ring_sq = 0.25;           // ring squeeze against the tube wall (~13%)
ring_h = 1.8;             // ring height in the 2.6 mm groove (~80% fill)
cap_sx = 49;              // cap retention screws, front and back walls
cap_sz = Zt - 4.5;        // 2.8 mm of tube wall above the hole

// ------------------------------------------------------------ fasteners
m3_clear = 3.4;
nut_d = 5.5 / cos(30) + 0.4;   // hex pocket, across corners
nut_h = 2.8;
cup_screw = 12;                // M3 x 12 into the bulkhead nuts
cs = [[5, 5], [Wi - 5, 5], [5, Di - 5], [Wi - 5, Di - 5]];

// ------------------------------------------------------------ battery
blk_l = 2 * (2.25 * cell_pitch + cell_bore / 2 + holder_wall);   // 113.15, along z
blk_w = cell_pitch * sin(60) + cell_bore + 2 * holder_wall;      // 40.83, along x
blk_d = cell_h + 2 * holder_lip + 1;                              // 69.85, along y
base_t = 2.5;
bat = [0.5, Di - blk_d - 0.5, base_t];   // TERM face toward the back: 2.65 mm gap for the leads
bat_top = bat[2] + blk_l;

// ------------------------------------------------------------ measured parts
// Joey's tape-measure readings, 2026-10-14, rounded up.
brk_sz  = [42, 42, 102];   // breaker: 1-5/8 in square plate, 4 in long, stands upright.
                           // Inline type: studs at both ends, reset lever and push-to-trip
                           // button on the plate face. The face points at the right wall.
brk_hole = 31.75;          // plate mounting holes, 1-1/4 in apart (zip ties go through them)
bms_sz  = [48, 6.4, 63.5]; // BMS card: 1-7/8 x 1/4 x 2-1/2 in, stands against the back wall
buck_sz = [17, 8, 25.4];   // Buck A/B: 1 in along the port, 5/16 in thick; width NOT measured
acs_sz  = [19, 4, 38.1];   // ACS758 module: 3/4 x 1/8 x 1-1/2 in
chg_sz  = [38.1, 17.5, 9.5]; // USB-C charger: 1-1/2 in along the plug, 11/16 x 3/8 in
pump_sz = [50.8, 44.5, 38.1]; // G528: 2 x 1-3/4 x 1-1/2 in (thickest)

// ------------------------------------------------------------ sled
sx0 = bat[0] + blk_w + 0.5;   // spine
ts = 2.5;
spine_h = 112;
bms_y = [1.3, 8.3];           // BMS slot between two low lips at the back
brk_y0 = 9.9;                 // breaker's back edge
brk_x0 = Wi - 2 - brk_sz[0];   // controls 2 mm from the right wall, behind the window
brk_z0 = 4;                   // hangs 1.5 mm above the base (room for the bottom lug)
brk_c = [brk_y0 + brk_sz[1] / 2, brk_z0 + brk_sz[2] / 2];   // plate centre (y, z)
brk_win = [34, 40];           // right-wall window over the reset lever and trip button
py0 = brk_y0 + brk_sz[1] + 1; // cross panel (breaker behind, bucks and ACS in front)
panel_t = 3;
panel_h = 100;

// ------------------------------------------------------------ bulkhead grommet
gs = [47, 58.5, 34, 11];      // x, y, w, h

// ------------------------------------------------------------ PCB (hangs from the cap, rotated 90 deg)
pcb_cxy = [70, 36.5];
pcb_top_z = Zt - 22;          // component face
function pxy(p) = [pcb_cxy[0] - p[1], pcb_cxy[1] + p[0]];   // board (x,y) -> stick (x,y)
led_xy = [[-5.2, 16.7], [0, 16.7], [5.2, 16.7]];
rv_xy  = [[-5.2, 10.1], [6.2, 10.1]];
sw_xy  = [14.7, 12.4];
holes  = [for (sx = [-1, 1], sy = [-1, 1]) [sx * pcb_hole_dx / 2, sy * pcb_hole_dy / 2]];
led_h = 5.3; sw_h = 4.3;

// ------------------------------------------------------------ cap panel features
vm_xy  = [21, 28];   vm_hole = 29.2;   // body just over 1-1/8 in (~28.8 mm), bezel ~1-5/16 in
usb_xy = [23, 55];
usb_win = [9.8, 4.0]; usb_cbore = [13.5, 7.5]; usb_web = 0.8;

// ============================================================ 2D helpers
module rr(w, d, r) { translate([r, r]) offset(r) square([w - 2 * r, d - 2 * r]); }
// inner outline grown by o (negative shrinks)
module in2d(o = 0) translate([-o, -o]) rr(Wi + 2 * o, Di + 2 * o, max(0.2, ri + o));
module out2d() in2d(t);

module cross_slot(h) {
    cube([ziptie_w, ziptie_t, h], center = true);
    cube([ziptie_t, ziptie_w, h], center = true);
}

// breaker window outline (horizontal = y, vertical = z), top corners
// chamfered so the wall prints without a long bridge
module win_profile(o = 0) {
    w = brk_win[0] / 2 + o; h = brk_win[1] / 2 + o; c = 12;
    polygon([[-w, -h], [w, -h], [w, h - c], [w - c, h], [-w + c, h], [-w, h - c]]);
}

// ============================================================ tube
module tube() {
    difference() {
        union() {
            difference() {
                translate([0, 0, -tb]) linear_extrude(Zt + tb) out2d();
                linear_extrude(Zt + 1) in2d();
                // 1 mm lead-in so the seal ring doesn't catch on the rim
                hull() {
                    translate([0, 0, Zt - 1]) linear_extrude(0.01) in2d();
                    translate([0, 0, Zt]) linear_extrude(0.01) in2d(1);
                }
                translate([gs[0], gs[1], -tb - 1]) linear_extrude(tb + 2) rr(gs[2], gs[3], 2);
            }
            // corner bosses on the dry side, so the nut holes stay blind
            for (p = cs) translate([p[0], p[1], 0]) cylinder(r = 4.5, h = base_t - 0.1);
        }
        // cup screw nuts, glued in from below
        for (p = cs) translate([p[0], p[1], -tb - 0.01]) {
            cylinder(d = nut_d, h = nut_h, $fn = 6);
            cylinder(d = m3_clear, h = nut_h + 1.4);   // blind: 1.2 mm skin on top
        }
        // breaker window, right wall: covered by a glued TPU membrane, so the
        // trip button (OFF) and reset lever work through the wall
        translate([Wi - 1, brk_c[0], brk_c[1]]) rotate([90, 0, 90]) linear_extrude(t + 2)
            win_profile();
        // cap retention screws (above the seal ring)
        for (y = [-t - 1, Di - 1]) translate([cap_sx, y, cap_sz]) rotate([-90, 0, 0])
            cylinder(d = m3_clear, h = t + 2);
    }
}

// ============================================================ cap (assembled position)
module cap() {
    difference() {
        union() {
            // plate, top edge chamfered
            hull() {
                translate([0, 0, Zt]) linear_extrude(tp - 1.2) out2d();
                translate([0, 0, Zt]) linear_extrude(tp) offset(-1.2) out2d();
            }
            // skirt
            translate([0, 0, Zt - sk_h]) linear_extrude(sk_h + 0.01)
                difference() { in2d(-sk_c); in2d(-sk_c - sk_t); }
            // nut blocks for the two retention screws
            for (s = [0, 1]) {
                y0 = s == 0 ? sk_c + sk_t - 0.01 : Di - sk_c - sk_t - 8 + 0.01;
                translate([cap_sx - 4, y0, Zt - sk_h]) cube([8, 8, sk_h + 0.01]);
            }
            // ribs pressing the two cell holders (add 1 mm foam)
            for (y = [bat[1] + holder_t / 2, bat[1] + blk_d - holder_t / 2])
                translate([bat[0] + 3, y - 1.5, bat_top + 0.6]) cube([blk_w - 6, 3, Zt - bat_top - 0.5]);
            // PCB posts with heat-stake pins
            for (h = holes) let(p = pxy(h)) translate([p[0], p[1], 0]) {
                translate([0, 0, pcb_top_z]) cylinder(d = 4.5, h = Zt - pcb_top_z + 0.01);
                translate([0, 0, pcb_top_z - 3.2]) cylinder(d = pcb_hole_d - 0.25, h = 3.3);
            }
            // light-tunnel block over LED1-3
            let(c = pxy([0, 16.7]))
                translate([c[0] - 2.8, c[1] - 8.2, pcb_top_z + led_h + 1])
                    cube([5.6, 16.4, Zt - pcb_top_z - led_h - 1 + 0.01]);
            // PRIME plunger sleeve
            let(c = pxy(sw_xy)) translate([c[0], c[1], Zt - 8]) cylinder(d = 8.2, h = 8.01);
        }
        // seal groove: square upper flank, 45-degree lower flank so the land
        // below it prints without an overhang
        translate([0, 0, gr_z]) linear_extrude(gr_h)
            difference() { in2d(1); in2d(-sk_c - gr_d); }
        for (k = [0.2 : 0.2 : gr_d - 0.2]) translate([0, 0, gr_z - k])
            linear_extrude(0.21) difference() { in2d(1); in2d(-sk_c - gr_d + k); }
        // pry notch on the left edge, for a flat screwdriver
        translate([-t - 1, Di / 2 - 5, Zt - 0.01]) cube([t + 1.5, 10, 1.2]);
        // retention screw holes (M3 x 10 with a TPU washer under the head,
        // which seals the hole); each nut drops into a slot that opens at
        // the bottom of its block, right behind the skirt
        for (s = [0, 1]) mirror([0, s, 0]) translate([0, -s * Di, 0]) {
            translate([cap_sx, -1, cap_sz]) rotate([-90, 0, 0])
                cylinder(d = m3_clear, h = sk_c + sk_t + 9);
            translate([cap_sx - 5.9 / 2, sk_c + sk_t - 0.2, Zt - sk_h - 1])
                cube([5.9, nut_h + 0.2, cap_sz - (Zt - sk_h - 1) + 3.3]);
        }
        // LED skin windows (0.6 mm left on the outer face)
        for (l = led_xy) let(p = pxy(l)) translate([p[0], p[1], pcb_top_z])
            cylinder(d = 3.6, h = Zt + tp - 0.6 - pcb_top_z);
        // trimmer windows over each 3296W screw. Per the KiCad Bourns
        // footprint the screw sits 0.955 mm beyond pin 1 (the square pad),
        // i.e. 3.5 mm from the trimmer centre on the side away from SW1.
        // Solder RV1/RV2 with pin 1 on the square pad. Tape over afterwards.
        for (r = rv_xy) let(p = pxy(r + [-3.495, 0])) translate([p[0], p[1], Zt - 1])
            linear_extrude(tp + 2) square([5.6, 5], center = true);
        // PRIME bore
        let(c = pxy(sw_xy)) translate([c[0], c[1], Zt - 9]) cylinder(d = 6.4, h = 20);
        // voltmeter
        translate([vm_xy[0], vm_xy[1], Zt - 1]) cylinder(d = vm_hole, h = tp + 2, $fn = 128);
        // USB-C: window plus counterbore from the top
        translate([usb_xy[0], usb_xy[1], Zt - 1]) linear_extrude(tp + 2)
            offset(1.6) square(usb_win - [3.2, 3.2], center = true);
        translate([usb_xy[0], usb_xy[1], Zt + usb_web]) linear_extrude(tp)
            offset(2.5) square(usb_cbore - [5, 5], center = true);
        // labels
        translate([0, 0, Zt + tp - 0.6]) linear_extrude(1) {
            for (i = [0:2]) let(p = pxy(led_xy[i]))
                translate([p[0] - 5, p[1]]) text(["PWR", "GUN", "PMP"][i], size = 2,
                    halign = "right", valign = "center", font = "Liberation Sans:style=Bold");
            let(c = pxy(sw_xy)) translate([c[0] + 13, c[1]])
                text("PRIME", size = 3, halign = "center", valign = "center",
                     font = "Liberation Sans:style=Bold");
            translate([usb_xy[0], usb_xy[1] + 8]) text("CHG", size = 3, halign = "center",
                font = "Liberation Sans:style=Bold");
            translate([82, 6]) text("BubbleLink", size = 4, halign = "center",
                font = "Liberation Sans:style=Bold");
        }
    }
}

// ============================================================ sled
// Front compartment: two side rails and a ledge on the panel's front face,
// each with a 45-degree underside so the standing sled prints without
// supports. A board drops in from the top; a zip tie through the panel
// slots holds it.
pf = py0 + panel_t;      // panel front face
module pocket(x0, w, z0, z1, d = 4) {
    // local profile (u = y, v = z), extruded along x
    module prof(top) polygon([[pf - 0.01, z0 - d], [pf + d, z0], [pf + d, top], [pf - 0.01, top]]);
    for (x = [x0 - 1.6, x0 + w]) translate([x, 0, 0]) rotate([90, 0, 90])
        linear_extrude(1.6) prof(z1);
    translate([x0 - 0.01, 0, 0]) rotate([90, 0, 90]) linear_extrude(w + 0.02)
        polygon([[pf - 0.01, z0 - d], [pf + d, z0], [pf - 0.01, z0]]);
}
bay_x = sx0 + ts;        // breaker bay left edge
pk = [[bay_x + 1.2, buck_sz[0] + 1, 8, 8 + buck_sz[2] + 2],             // Buck A
      [bay_x + 3.4 + buck_sz[0] + 1, buck_sz[0] + 1, 8, 8 + buck_sz[2] + 2], // Buck B
      [bay_x + 1.2, acs_sz[0] + 1, 40, 40 + acs_sz[2] + 2]];             // ACS758

module sled() {
    difference() {
        union() {
            linear_extrude(base_t) difference() {
                in2d(-0.5);
                for (p = cs) translate(p - [6, 6]) square(12);   // clear the bulkhead bosses
                translate([gs[0] - 2.2, gs[1] - 2.2]) square([gs[2] + 4.4, gs[3] + 4.4]);
            }
            // spine stops 6 mm short of both walls: lead channels front and back
            translate([sx0, 6, 0]) cube([ts, Di - 12, spine_h]);
            // cross panel
            translate([bay_x - 0.01, py0, 0]) cube([Wi - 0.5 - bay_x, panel_t, panel_h]);
            // BMS slot: low lips front and back
            translate([bay_x - 0.01, bms_y[0] - 0.8, 0]) cube([Wi - 0.5 - bay_x, 0.8, base_t + 5]);
            translate([bay_x - 0.01, bms_y[1], 0]) cube([Wi - 0.5 - bay_x, 0.8, base_t + 5]);
            // compartments for Buck A, Buck B and the ACS758
            for (p = pk) pocket(p[0], p[1], p[2], p[3]);
        }
        // clear the bulkhead's corner bosses
        for (p = cs) translate([p[0], p[1], -1]) cylinder(r = 5.5, h = base_t + 1.5);
        // zip-tie slots: spine (through x) and panel (through y)
        for (y = [13 : 12 : Di - 12], z = [9 : 13 : spine_h - 6])
            translate([sx0 + ts / 2, y, z]) rotate([0, 90, 0]) cross_slot(ts + 2);
        for (x = [bay_x + 6 : 11 : Wi - 5], z = [14 : 11 : panel_h - 6])
            translate([x, py0 + panel_t / 2, z]) rotate([90, 0, 0]) cross_slot(panel_t + 2);
        // breaker: one zip tie through each plate hole and through these
        // spine slots (tall, so the hole spacing can be approximate)
        for (s = [-1, 1]) translate([sx0 - 1, brk_c[0] + s * brk_hole / 2 - 1.7, brk_c[1] - 7])
            cube([ts + 2, 3.4, 14]);
        // wire pass through the panel's right end (breaker / BMS to the
        // bucks and ACS758 in front)
        translate([Wi - 8.5, py0 - 1, 4]) cube([8.01, panel_t + 2, 30]);
        // wire pass holes through the spine (battery leads)
        for (z = [24, 104]) translate([sx0 - 1, 25, z]) rotate([0, 90, 0])
            linear_extrude(ts + 2) offset(2) square([6, 12], center = true);
    }
}

// ============================================================ cup (local: floor bottom at z = 0)
pp = [10, 13.5, pump_sz[0] + 1.2, pump_sz[1] + 1.5];   // pump pocket: x, y, w, d
umb = [[72, 12], [72, 32]];  svc = [79, 56];

module cup() {
    difference() {
        union() {
            difference() {
                hull() {
                    translate([0, 0, 1.2]) linear_extrude(tf + Hw - 1.2) out2d();
                    linear_extrude(tf + Hw) offset(-1.2) out2d();
                }
                translate([0, 0, tf]) linear_extrude(Hw + 1) in2d();
            }
            // screw columns
            for (p = cs) translate([p[0], p[1], 0]) cylinder(d = 9, h = tf + Hw);
            // pump pocket fence (6 mm tall); strap the pump down across it
            translate([pp[0] - 1.6, pp[1] - 1.6, 0]) difference() {
                cube([pp[2] + 3.2, pp[3] + 3.2, tf + 6]);
                translate([1.6, 1.6, tf]) cube([pp[2], pp[3], 10]);
            }
        }
        // M3 x 12 goes up from below through a deep counterbore
        for (p = cs) translate([p[0], p[1], 0]) {
            translate([0, 0, -1]) cylinder(d = 6.6, h = tf + Hw - (cup_screw - 3) + 1);
            cylinder(d = m3_clear, h = tf + Hw + 1);
        }
        // umbilical exits and service hole (bladder feed, LED-backpack USB,
        // XT60H disconnect loop), with 1 mm chamfers so hoses don't rub
        for (p = concat(umb, [svc])) let(d = p == svc ? 20 : 13) translate([p[0], p[1], 0]) {
            translate([0, 0, -1]) cylinder(d = d, h = tf + 2);
            translate([0, 0, -0.01]) cylinder(d1 = d + 2, d2 = d, h = 1);
            translate([0, 0, tf - 0.99]) cylinder(d1 = d, d2 = d + 2, h = 1);
        }
        // drains under the pump
        for (x = [20 : 10 : 55]) translate([x, Di / 2, -1]) cylinder(d = 4, h = tf + 2);
        // tie slots: straps over the pump, and the fittings strip
        for (x = [22, 36, 50], y = [pp[1] - 4, pp[1] + pp[3] + 4])
            translate([x, y, tf / 2]) cross_slot(tf + 2);
        for (p = [[88, 14], [88, 32], [68, 48], [90, 48]])
            translate([p[0], p[1], tf / 2]) cross_slot(tf + 2);
    }
}

// ============================================================ small parts
// TPU boot glued over the PRIME bore. 45-degree cone, so it prints without
// supports (6.4 mm roof bridge).
bt_r0 = 5.2;     // inner radius of the boot's straight section
bt_h0 = 2.2;     // height of the straight section
bt_head_z = bt_h0 + (bt_r0 - 4.5);   // where the 9 mm plunger head meets the cone
module boot() {
    difference() {
        union() {
            cylinder(d = 16, h = 0.8);
            cylinder(r = 6, h = bt_h0);
            translate([0, 0, bt_h0 - 0.01]) cylinder(r1 = 6, r2 = 3, h = 3);
        }
        translate([0, 0, -0.01]) cylinder(r = bt_r0, h = bt_h0 + 0.02);
        translate([0, 0, bt_h0]) cylinder(r1 = bt_r0, r2 = bt_r0 - 2, h = 2);
    }
}
// PRIME plunger: the head floats under the boot's cone, 1.7 mm above the
// plate (that's the stroke); the tip stops 0.3 mm above SW1.
pl_len = Zt + tp + (bt_head_z - 1.2) - (pcb_top_z + sw_h + 0.3);
module plunger() {
    cylinder(d = 9, h = 1.2);
    cylinder(d = 5.8, h = 1.2 + pl_len);
}
// TPU seal ring: stretches over the skirt into the groove
module ring() {
    linear_extrude(ring_h) difference() { in2d(ring_sq); in2d(-sk_c - gr_d); }
}
// TPU membrane glued over the breaker window (outside face of the right wall)
module membrane() { linear_extrude(0.8) win_profile(4); }
// TPU washer under each cap screw head
module washer() {
    difference() { cylinder(d = 7, h = 1); translate([0, 0, -1]) cylinder(d = 2.8, h = 3); }
}
// Two-piece TPU grommet: each half is a flange plus half the neck, printed
// flange-down. The lower half pushes up from the cup side, the upper half
// down from the dry side, and they meet inside the bulkhead slot. Holes are
// sized per conductor (0.2 mm under OD); cut a slit from each hole to the
// nearest long edge with a knife so cables can be laid in.
gm_holes = [   // [x, y, d] in slot coordinates (slot is gs[2] x gs[3])
    [5, 3.0, awg16_od - 0.2], [9, 3.0, awg16_od - 0.2],        // gun 1 pair
    [14.5, 3.0, awg16_od - 0.2], [18.5, 3.0, awg16_od - 0.2],  // gun 2 pair
    [25, 3.0, pump_od - 0.2], [28, 3.0, pump_od - 0.2],        // pump leads
    [6, 7.9, awg12_od - 0.2], [11.5, 7.9, awg12_od - 0.2],     // XT60H loop
    [19, 7.9, usb_od - 0.2]];                                  // backpack USB
module grommet_half() {
    w = gs[2]; h = gs[3]; f = 2.0; ft = 1.2;
    difference() {
        union() {
            linear_extrude(ft) offset(f) rr(w, h, 2);
            translate([0, 0, ft - 0.01]) linear_extrude(tb / 2 + 0.01) offset(-0.1) rr(w, h, 2);
        }
        for (c = gm_holes) translate([c[0], c[1], -1]) cylinder(d = c[2], h = 10, $fn = 24);
    }
}

// ============================================================ ghosts
module ghost(i) {
    if (i == 0) color("orange", 0.5) translate(bat) cube([blk_w, blk_d, blk_l]);                  // battery
    if (i == 1) color("red", 0.5) translate([brk_x0, brk_y0, brk_z0]) cube(brk_sz);              // breaker
    if (i == 2) color("green", 0.6) let(c = pxy([0, 0]))                                           // PCB + leads
        translate([c[0] - 20, c[1] - 25, pcb_top_z - 1.6 - 2]) cube([40, 50, 3.6]);
    if (i == 3) color("gray", 0.5) translate([vm_xy[0], vm_xy[1], Zt - 30]) cylinder(d = 28.8, h = 30);  // voltmeter body, ~1 in+ deep
    if (i == 4) color("blue", 0.4) translate([usb_xy[0] - chg_sz[0] / 2, usb_xy[1] - chg_sz[1] / 2, Zt - chg_sz[2]]) cube(chg_sz);  // charger
    if (i == 5) color("purple", 0.4) translate([bay_x + 0.7, bms_y[0] + 0.3, base_t]) cube(bms_sz);  // BMS
    if (i == 6) color("cyan", 0.4) for (k = [0:2]) let(p = pk[k], b = k < 2 ? buck_sz : acs_sz)   // bucks + ACS758
        translate([p[0] + 0.5, pf + 0.2, p[2]]) cube(b);
    if (i == 7) color("tan", 0.4) translate([pp[0] + 0.6, pp[1] + 0.75, -tb - Hw]) cube(pump_sz);  // pump
}

if (part == "tube")      translate([0, 0, tb]) tube();
else if (part == "cap")  translate([0, 0, Zt + tp]) rotate([180, 0, 0]) cap();
else if (part == "sled") sled();
else if (part == "cup")  cup();
else if (part == "plunger") plunger();
else if (part == "ring") ring();
else if (part == "grommet_lo") grommet_half();
else if (part == "grommet_hi") translate([0, gs[3], 0]) mirror([0, 1, 0]) grommet_half();
else if (part == "boot") boot();
else if (part == "washer") washer();
else if (part == "membrane") membrane();
else {
    tube(); %cap(); sled();
    translate([0, 0, -tb - Hw - tf]) cup();
    for (i = [0:7]) ghost(i);
    installed_tpu();
}

// TPU parts in their installed positions (assembly preview and checks)
module installed_tpu() {
    color("black") {
        translate([0, 0, gr_z + 0.4]) ring();
        // lower grommet half: flange under the bulkhead, neck up into the slot
        translate([gs[0], gs[1], -tb - 1.2]) grommet_half();
        // upper half: flange on the bulkhead's top face, neck down into the slot
        translate([gs[0], gs[1], 1.2]) mirror([0, 0, 1]) grommet_half();
        let(c = pxy(sw_xy)) translate([c[0], c[1], Zt + tp]) boot();
        for (y = [-t - 1, Di + t]) translate([cap_sx, y, cap_sz]) rotate([-90, 0, 0]) washer();
        translate([Wi + t, brk_c[0], brk_c[1]]) rotate([90, 0, 90]) membrane();
    }
}
