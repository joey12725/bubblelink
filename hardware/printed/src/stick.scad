// BubbleLink stick (dry core v2): the whole pack except the bladder, in one
// upright column that stands beside the bladder in any bag. Supersedes
// dry_core.scad, pump_module.scad and port_insert.scad.
//
// Worn orientation: +z up, y = 0 against the wearer's back, x across.
//
//   CAP     control head. The CTRL PCB hangs under it. LEDs show through
//           glue-filled through-holes, PRIME is a TPU plunger under a TPU
//           boot clamped by a guard bezel, and the voltmeter and USB-C
//           charge port are on top. A printed TPU
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
//           underneath, and drains through its floor and walls. Nothing exits
//           underneath: see PORTS.
//   PORTS   cap top (dry): USB-C charge, XT60H power KEY, PRIME, LEDs, THR/DLY,
//           voltmeter. Tube outer wall (dry): LED 5V, Buck B's own USB-A port
//           behind a window. Cup outer wall (wet): two gun clusters, each an
//           XT30U well (pack side female), a hose pigtail and a paracord
//           tunnel. Cup front wall: bladder IN pigtail.
//   Cables cross the bulkhead through a two-piece TPU grommet with knife-cut
//   slits, so the sled can still be pulled. It's a splash baffle, not a
//   watertight feedthrough.
//   Venting/thermal: incidental breathing only (grommet slits, cap ring).
//   Cell-fault pressure relief and enclosed-charging temperatures are NOT
//   verified; measure charger/BMS temperature on the first enclosed charge.
//
// Hardware: 6x M3 screws (2x 10 mm for the cap, 4x 12 mm for the cup),
// 6x M3 nuts glued into pockets, zip ties, glue. TPU: seal ring, two
// grommet halves, PRIME boot and plunger, two screw washers, two battery
// pads, a pump mat and a shim set. Rigid parts are ASA (PETG also works): includes the
// PRIME guard bezel, grommet drip skirt and the power-key grip. TPU plugs and caps close
// the trimmer windows (one plug for both), USB-C, LED 5V, unused gun ports and the key
// socket.
//
// part = tube | cap | sled | cup | plunger | pcbspacer | ring | boot | grommet_lo | grommet_hi |
//        skirt | bezel | washer | batpad | pumpmat | shim | trimplug | usbplug | usbAplug |
//        gunportcap | powerkey | keyblank | keygasket | coupon_rim | coupon_skirt |
//        coupon_nut | coupon_ports | assembly

include <params.scad>

part = "assembly";

// ------------------------------------------------------------ envelope
Wi = 94;      // inner width (x): battery + spine + 42 mm breaker bay
Di = 73;      // inner depth (y): 69.85 mm battery + clearance
ri = 1.0;     // inner corner radius (the battery block fills the corners)
t  = 2.4;     // wall
tb = 3;       // bulkhead (tube floor)
Zt = 156;     // tube rim, measured from the bulkhead's top face (room for the 38 mm upright
              // charger and the ~30 mm voltmeter above the battery)
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
cap_sz = Zt - 5.2;        // 3.5 mm of tube wall above the hole

// ------------------------------------------------------------ fasteners
m3_clear = 3.4;
nut_d = 5.5 / cos(30) + 0.4;   // hex pocket, across corners
nut_h = 2.8;
cup_screw = 12;                // M3 x 12 into the bulkhead nuts
lw_t = 0.8;                    // M3 split lock washer under each cup screw head
cs = [[5, 5], [Wi - 5, 5], [5, Di - 5], [Wi - 5, Di - 5]];

// ------------------------------------------------------------ ports (every way in or out of the stick)
// [ESTIMATE] connector sizes: check them with 00_stick_coupon_ports before printing the cup/cap/tube.
xt30_well = [10.8, 6.2];   // well for the umbilical's XT30U male shroud (AMASS envelope ~10.2 x 5.6, +0.3 per side)
xt30_len  = 24;            // well + potted female, along its 45-degree axis
xt60_body = [17.0, 9.8];   // XT60H male (the key socket) body in the cap (AMASS envelope 16.4 x 9.2, +0.3 per side)
xt60_dep  = 22;            // sleeve depth under the cap plate (room for the zip-tie keeper behind the body)
key_xy    = [42, 52.0];    // power-key socket on the cap (long side along y)
gun_y     = [22, 48];      // gun port clusters on the cup's outer wall (y centres)
sock_z    = 30;            // XT30U well mouth centre (cup coordinates)
hose_z    = 18;            // hose pigtail exit
hose_hole = 6.0;           // 3.5 x 5.5 silicone pigtail (5.4 was too tight in ASA; coupon, 2026-10-15)
in_xz     = [76, 18];      // bladder IN pigtail on the cup's front wall (x, z)
usbA_win  = [14.0, 6.6];   // LED 5 V window: takes Buck B's USB-A receptacle shell (13.1 x 5.7) and any plug
usbA_cb   = [17, 9];       // outside counterbore for the plug's overmold, leaves a 0.8 web
bb_sz     = [25.4, 8, 17]; // Buck B: length (x, port end toward the wall), thickness (y), width (z)
bb_z0     = 42;            // Buck B bottom edge on its shelf (tube coordinates)
bb_x0     = Wi - 25.4;     // Buck B input end: the board is pushed up to the outer wall (receptacle into the window)
bb_yb     = Di - 2;        // Buck B's PCB back face, 2 mm off the front wall

// ------------------------------------------------------------ TPU cushions (replace foam)
bp_t    = 3.8;    // battery pad cushion thickness (free, uncompressed)
bp_wall = 1.2;    // pad wall around the rib end
bp_deep = 6;      // how far the pad pocket wraps up the rib
bp_ov   = 0.6;    // pad compression against the cell holders (working range 0.1-1.2 mm)
rib_w   = 3;
mp_t    = 2;      // pump mat thickness
emb_h   = 0.8;    // BubbleLink emboss height
emb_size = 12;

// ------------------------------------------------------------ battery
blk_l = 2 * (2.25 * cell_pitch + cell_bore / 2 + holder_wall);   // 113.15, along z
blk_w = cell_pitch * sin(60) + cell_bore + 2 * holder_wall;      // 40.83, along x
blk_d = cell_h + 2 * holder_lip + 1;                              // 67.45, along y (holders + cells + fish paper)
base_t = 2.5;
bat = [0.5, Di - blk_d - 2.0, base_t];   // MID face 2 mm off the front wall, TERM face 3.55 mm off the back:
                                         // room for the tabs and solder on both faces
bat_top = bat[2] + blk_l;
bp_y = [bat[1] + holder_t / 2, bat[1] + blk_d - holder_t / 2];   // rib / pad centre lines (y)
rib_z0 = bat_top - bp_ov + bp_t;                                  // rib bottom = pad pocket floor

// ------------------------------------------------------------ measured parts
// Joey's tape-measure readings, 2026-10-14, rounded up.
brk_sz  = [42, 42, 102];   // breaker: 1-5/8 in square plate, 4 in long, stands upright.
                           // Inline type: studs at both ends, reset lever and push-to-trip
                           // button on the plate face. There is no wall window: the walls stay
                           // solid, so resetting it means cap off and sled out. The power
                           // KEY on the cap is the OFF switch.
brk_hole = 31.75;          // plate mounting holes, 1-1/4 in apart (zip ties go through them)
bms_sz  = [48, 6.4, 63.5]; // BMS card: 1-7/8 x 1/4 x 2-1/2 in, stands against the back wall
buck_sz = [17, 8, 25.4];   // Buck A/B: 1 in along the port, 5/16 in thick; width NOT measured
acs_sz  = [19, 4, 38.1];   // ACS758 module: 3/4 x 1/8 x 1-1/2 in
chg_sz  = [17.5, 9.5, 38.1]; // USB-C charger: 1-1/2 in along the plug (vertical: port faces up), 11/16 x 3/8 in
pump_sz = [50.8, 44.5, 38.1]; // G528: 2 x 1-3/4 x 1-1/2 in (thickest)

// ------------------------------------------------------------ sled
sx0 = bat[0] + blk_w + 0.5;   // spine
ts = 2.5;
spine_h = 112;
bms_y = [1.3, 8.3];           // BMS slot between two low lips at the back
brk_y0 = 9.9;                 // breaker's back edge
brk_x0 = Wi - 2 - brk_sz[0];   // 2 mm from the outer wall; the gap to the spine is a wire channel
brk_z0 = 4;                   // hangs 1.5 mm above the base (room for the bottom lug)
brk_c = [brk_y0 + brk_sz[1] / 2, brk_z0 + brk_sz[2] / 2];   // plate centre (y, z)
py0 = brk_y0 + brk_sz[1] + 1; // cross panel (breaker behind, bucks and ACS in front)
panel_t = 3;
panel_h = 100;

// ------------------------------------------------------------ bulkhead grommet
gs = [47, 58.3, 34, 10];      // x, y, w, h

// ------------------------------------------------------------ PCB (hangs from the cap, rotated 90 deg)
pcb_cxy = [70, 36.5];
pcb_post_z = Zt - 22;         // end of the cap's PCB posts, as printed
// The LEDs came out taller than led_h and hit the light tunnel (Joey, 2026-10-20). Four ASA
// spacers (part 27) slip over the posts' stake pins and drop the board by one board thickness
// plus one stake pin plus 1 mm. The cap doesn't change; the PRIME plunger grows to match.
pcb_drop = 1.6 + 3.2 + 1;     // 5.8
pcb_top_z = pcb_post_z - pcb_drop;   // component face
function pxy(p) = [pcb_cxy[0] - p[1], pcb_cxy[1] + p[0]];   // board (x,y) -> stick (x,y)
led_xy = [[-5.2, 16.7], [0, 16.7], [5.2, 16.7]];
rv_xy  = [[-5.2, 10.1], [6.2, 10.1]];
sw_xy  = [14.7, 12.4];
holes  = [for (sx = [-1, 1], sy = [-1, 1]) [sx * pcb_hole_dx / 2, sy * pcb_hole_dy / 2]];
led_h = 5.3; sw_h = 4.3;

// ------------------------------------------------------------ cap panel features
vm_xy  = [21, 28];   vm_hole = 31.2;   // 29.2 printed 1-2 mm too small in ASA (Joey, 2026-10-16): +2 mm
usb_xy = [23, 55];
usbc_port_t = 3.3;            // [ESTIMATE] thickness of the charger's USB-C receptacle
chg_slot_t  = 1.25 * usbc_port_t;   // charger slot thickness: snug round the board's thin top
                              // end; its thick part (output pads, big parts) hangs below the slot
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
            emboss();
            // Buck B shelf on the front wall (45-degree underside): the board stands on it, PCB
            // toward the wall, and slides along it until its USB-A receptacle sits in the outer
            // wall's window; a lip stops it tipping in, and a zip tie through the two slots
            // goes over its top edge
            let(L = bb_yb - bb_sz[1] - 2) difference() {   // L: lip face, 2 mm in front of the board
                translate([bb_x0 - 0.2, 0, 0]) rotate([90, 0, 90]) linear_extrude(Wi - bb_x0 + 0.21)
                    polygon([[L - 1.2, bb_z0 + 4], [L - 1.2, bb_z0], [Di + 0.01, bb_z0 - (Di - L + 1.2)],
                             [Di + 0.01, bb_z0], [L, bb_z0], [L, bb_z0 + 4]]);
                for (x = [bb_x0 + 5, Wi - 6], y = [L + 1, Di - 1])
                    translate([x, y, bb_z0 - 6]) cube([ziptie_w, ziptie_t, 20], center = true);
            }
            // drip hood over the LED 5 V window (45-degree underside)
            translate([Wi + t - 0.01, bb_port[0] - 8, bb_port[1] + usbA_cb[0] / 2 + 2]) rotate([90, 0, 0])
                translate([0, 0, -(Di - 1 - (bb_port[0] - 8))]) linear_extrude(Di - 1 - (bb_port[0] - 8))
                    polygon([[0, -2.5], [2.5, 0], [2.5, 1.2], [0, 1.2]]);   // stops before the corner radius
            // corner bosses on the dry side, so the nut holes stay blind
            for (p = cs) translate([p[0], p[1], 0]) cylinder(r = 4.5, h = base_t - 0.1);
        }
        // cup screw nuts drop in from the DRY side and get glued: 1.4 mm of
        // bulkhead sits under each nut, so the screw clamps the cup to the
        // bulkhead (a pocket open on the cup side would let the screw pull
        // the nut straight out). Dab silicone over each nut once tightened.
        for (p = cs) translate([p[0], p[1], 0]) {
            translate([0, 0, -tb - 0.01]) cylinder(d = m3_clear, h = tb + 3);
            translate([0, 0, -tb + 1.4]) cylinder(d = nut_d, h = 10, $fn = 6);
        }
        // LED 5 V: window to Buck B's USB-A port (0.8 mm web) and an outside counterbore
        // for the plug's overmold; label below
        translate([Wi - 1, bb_port[0], bb_port[1]]) rotate([0, 90, 0]) linear_extrude(t + 2)
            offset(0.5) square([usbA_win[0] - 1, usbA_win[1] - 1], center = true);
        translate([Wi + 0.8, bb_port[0], bb_port[1]]) rotate([0, 90, 0]) linear_extrude(t)
            offset(1.5) square([usbA_cb[0] - 3, usbA_cb[1] - 3], center = true);
        translate([Wi + t - 0.6, bb_port[0], bb_port[1] - usbA_cb[0] / 2 - 4]) rotate([90, 0, 90])
            linear_extrude(1) text("LED 5V", size = 3.5, halign = "center", valign = "center",
                                   font = "Liberation Sans:style=Bold");
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
            // ribs pressing the two cell holders through TPU pads that slip
            // over their ends (pad free thickness bp_t, squeezed bp_ov)
            for (y = bp_y)
                translate([bat[0] + 3, y - rib_w / 2, rib_z0]) difference() {
                    union() {   // 0.5 mm chamfer on the tip so the sharp edge can't shave the pad's bead
                        hull() {
                            translate([0, 0.5, 0]) cube([blk_w - 6, rib_w - 1, 0.01]);
                            translate([0, 0, 0.5]) cube([blk_w - 6, rib_w, 0.01]);
                        }
                        translate([0, 0, 0.5]) cube([blk_w - 6, rib_w, Zt - rib_z0 - 0.4]);
                    }
                    // snap groove for the pad's retaining bead (both faces)
                    for (f = [0, 1]) translate([-1, f * (rib_w - 0.5) - (f == 0 ? 0.01 : -0.01), bp_deep - 2.8 - 0.7]) cube([blk_w - 4, 0.51, 1.4]);
                }
            // PCB posts with heat-stake pins
            for (h = holes) let(p = pxy(h)) translate([p[0], p[1], 0]) {
                translate([0, 0, pcb_post_z]) cylinder(d = 4.5, h = Zt - pcb_post_z + 0.01);
                translate([0, 0, pcb_post_z - 3.2]) cylinder(d = pcb_hole_d - 0.25, h = 3.3);
            }
            // light-tunnel block over LED1-3
            let(c = pxy([0, 16.7]))
                translate([c[0] - 2.8, c[1] - 8.2, pcb_post_z + led_h + 1])
                    cube([5.6, 16.4, Zt - pcb_post_z - led_h - 1 + 0.01]);
            // charger slot: the board's thin top end (PCB + USB-C receptacle) slides up
            // into a slot only 1.25x the receptacle's thickness, receptacle against the
            // window, so the board can't wobble. The thick part of the board (output pads,
            // big components) hangs below the slot. Receptacle centred on the 17.5 mm
            // side (Joey, 2026-10-15); a dab of glue at the slot mouth.
            translate([usb_xy[0], usb_xy[1], Zt - 30]) difference() {
                translate([-(chg_sz[0] / 2 + 1.6), -(chg_slot_t / 2 + 1.2), 0])
                    cube([chg_sz[0] + 3.2, chg_slot_t + 2.4, 30.01]);
                translate([-(chg_sz[0] / 2 + 0.4), -chg_slot_t / 2, -1])
                    cube([chg_sz[0] + 0.8, chg_slot_t, 31]);
            }
            // PRIME plunger sleeve
            let(c = pxy(sw_xy)) translate([c[0], c[1], Zt - 8]) cylinder(d = 8.2, h = 8.01);
            // power-key socket sleeve (XT60H male, potted from below)
            translate([key_xy[0] - xt60_body[1] / 2 - 1.2, key_xy[1] - xt60_body[0] / 2 - 1.2, Zt - xt60_dep])
                cube([xt60_body[1] + 2.4, xt60_body[0] + 2.4, xt60_dep + 0.01]);
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
        // LED windows: punched through. Fill each from the top with clear
        // hot glue or UV resin; that seals it and passes the light.
        for (l = led_xy) let(p = pxy(l)) translate([p[0], p[1], pcb_post_z])
            cylinder(d = 3.6, h = Zt + tp - pcb_post_z + 1);
        // trimmer windows over each 3296W screw. Per the KiCad Bourns
        // footprint the screw sits 0.955 mm beyond pin 1 (the square pad),
        // i.e. 3.5 mm from the trimmer centre on the side away from SW1.
        // Solder RV1/RV2 with pin 1 on the square pad. One TPU plug (part 39)
        // closes both windows afterwards.
        for (r = rv_xy) let(p = pxy(r + [-3.495, 0])) translate([p[0], p[1], Zt - 1])
            linear_extrude(tp + 2) square([5.6, 5], center = true);
        // power-key socket: the male's shroud sits under a 0.8 mm lip (the lip stops it being
        // pulled up; hot glue under it stops it being pushed down); the key's female plug
        // enters through the window
        translate([key_xy[0] - xt60_body[1] / 2, key_xy[1] - xt60_body[0] / 2, Zt - xt60_dep - 1])
            cube([xt60_body[1], xt60_body[0], xt60_dep + 1 + tp - 0.8]);
        translate([key_xy[0], key_xy[1], Zt - 1]) linear_extrude(tp + 2)
            offset(0.8) square([xt60_body[1] - 1.0 - 1.6, xt60_body[0] - 1.0 - 1.6], center = true);
        // rear keeper: a zip tie threaded across through these two slots, between the
        // solder cups and pushed up against the back of the connector body before it is
        // cinched round the sleeve; it stops the key's insertion force pushing the socket in
        translate([key_xy[0] - xt60_body[1] / 2 - 2, key_xy[1] - 1.8, Zt + tp - 0.8 - 23])
            cube([xt60_body[1] + 4, 3.6, 7]);
        // PRIME bore
        let(c = pxy(sw_xy)) translate([c[0], c[1], Zt - 9]) cylinder(d = 6.4, h = 20);
        // voltmeter
        translate([vm_xy[0], vm_xy[1], Zt - 1]) cylinder(d = vm_hole, h = tp + 2, $fn = 128);
        // USB-C: window plus counterbore from the top
        translate([usb_xy[0], usb_xy[1], Zt - 1]) linear_extrude(tp + 2)
            offset(1.6) square(usb_win - [3.2, 3.2], center = true);
        translate([usb_xy[0], usb_xy[1], Zt + usb_web]) linear_extrude(tp)
            offset(2.5) square(usb_cbore - [5, 5], center = true);
        // labels (engraved 0.6 mm), all reading correctly from the FRONT
        translate([0, 0, Zt + tp - 0.6]) linear_extrude(1) cap_labels();
    }
}

// engraved cap labels (2D). Rotated 180 so they read from the front.
module cap_labels() {
            for (i = [0:2]) let(p = pxy(led_xy[i])) translate([p[0] - 3.4, p[1]]) rotate(180)
                text(["PWR", "GUN", "PUMP"][i], size = 3, halign = "left", valign = "center",
                     font = "Liberation Sans:style=Bold");
            for (i = [0:1]) let(p = pxy(rv_xy[i] + [-3.495, 0])) translate([p[0] + 6.0, p[1]]) rotate(180)
                text(["THR", "DLY"][i], size = 3, halign = "right", valign = "center",
                     font = "Liberation Sans:style=Bold");
            let(c = pxy(sw_xy)) translate([c[0], c[1] + 14]) rotate(180)
                text("PRIME", size = 3.5, halign = "center", valign = "center",
                     font = "Liberation Sans:style=Bold");
            translate([usb_xy[0], usb_xy[1] + 7.5]) rotate(180)
                text("CHG", size = 3.5, halign = "center", valign = "center",
                     font = "Liberation Sans:style=Bold");
            translate([key_xy[0], key_xy[1] + xt60_body[0] / 2 + 4]) rotate(180)
                text("KEY", size = 3.5, halign = "center", valign = "center",
                     font = "Liberation Sans:style=Bold");
            translate([70, 12]) rotate(180)
                text("BubbleLink", size = 4.5, halign = "center", valign = "center",
                     font = "Liberation Sans:style=Bold");
        }

// ============================================================ sled
// Front compartment: two side rails and a ledge on the panel's front face,
// each with a 45-degree underside so the standing sled prints without
// supports. A board drops in from the top; a zip tie through the panel
// slots holds it.
pf = py0 + panel_t;      // panel front face
bb_port = [bb_yb - 1.6 - 2.85, bb_z0 + bb_sz[2] / 2];   // Buck B receptacle centre (y, z): PCB back toward the front wall
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
      [bay_x + 1.2, acs_sz[0] + 1, 40, 40 + acs_sz[2] + 2]];             // ACS758
// Buck B (LED backpack 5 V) is NOT on the sled: it sits on a shelf on the tube's front wall
// (see tube()), its USB-A receptacle in a window in the outer wall, so the sled lifts out
// past it. Its two input wires reach the sled through a JST-XH plug.

module sled() {
    difference() {
        union() {
            linear_extrude(base_t) difference() {
                in2d(-0.5);
                // corner notches: each hugs its boss (0.3 mm) and opens out to the corner
                for (p = cs) hull() {
                    translate(p) circle(r = 4.8);
                    translate([p[0] < Wi / 2 ? -2 : Wi - 3, p[1] < Di / 2 ? -2 : Di - 3]) square(5);
                }
                translate([gs[0] - 2.2, gs[1] - 2.2]) square([gs[2] + 4.4, gs[3] + 4.4]);
                // notch for the Buck B shelf on the tube's front wall (the base slides down past it)
                translate([bb_x0 - 0.2 - 0.6, bb_yb - bb_sz[1] - 2 - 1.2 - 0.6]) square([Wi, Di]);
            }
            // two stops behind the battery's back face (y < 2.65) so a hard jump can't drive it into the leads;
            // the holder's sawtooth outline reaches only one side of the base, so each stop is 5 mm wide
            for (x = [12, 31]) translate([x, 0.6, base_t - 0.01]) cube([5, bat[1] - 0.6 - 0.3, 2]);   // 2 mm tall: they meet the holder's flat bottom strip, below every cell and tab   // 5 mm wide: the cell holder's rounded end only reaches one of them
            // spine stops 6 mm short of both walls: lead channels front and back
            translate([sx0, 6, 0]) cube([ts, Di - 12, spine_h]);
            // cross panel
            translate([bay_x - 0.01, py0, 0]) cube([Wi - 0.5 - bay_x, panel_t, panel_h]);
            // BMS slot: a 12 mm back lip and a 25 mm front fence (the breaker's back face is
            // 0.4 mm beyond it), so the card can't rock; a TPU shim behind its top takes up
            // the last 1-2 mm against the tube wall
            translate([bay_x - 0.01, bms_y[0] - 0.8, 0]) cube([Wi - 0.5 - bay_x, 0.8, base_t + 12]);
            translate([bay_x - 0.01, bms_y[1], 0]) cube([Wi - 0.5 - bay_x, 1.2, base_t + 25]);
            // compartments for Buck A and the ACS758
            for (p = pk) pocket(p[0], p[1], p[2], p[3]);
        }
        // clear the bulkhead's corner bosses
        // the four bulkhead bosses (r 4.5) locate the sled: 0.3 mm clearance all round
        for (p = cs) translate([p[0], p[1], -1]) cylinder(r = 4.85, h = base_t + 1.5);
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
tie_z = tf + 5.5;   // paracord tie-off tunnels, one beside each gun port, low on the outer wall

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
            for (k = [0, 1]) gun_port_solid(gun_y[k]);
            // IN pigtail boss (45-degree underside)
            intersection() {
                translate([in_xz[0], Di + t, in_xz[1]]) rotate([-45, 0, 0]) rotate([-90, 0, 0])
                    translate([0, 0, -11]) cylinder(d = 9, h = 11);
                translate([0, 0, tf]) linear_extrude(Hw) in2d(0.1);
            }
        }
        // M3 x 12 goes up from below through a deep counterbore
        for (p = cs) translate([p[0], p[1], 0]) {
            // 0.8 mm extra depth for an M3 split lock washer under the head: with it the M3x12
            // still reaches 0.7 mm past the nut (without it, 1.5 mm past: also fine)
            translate([0, 0, -1]) cylinder(d = 6.6, h = tf + Hw - (cup_screw - 4.5 - lw_t) + 1);
            cylinder(d = m3_clear, h = tf + Hw + 1);
        }
        // gun port clusters (outer wall): XT30U well, hose pigtail, paracord tunnel
        for (k = [0, 1]) gun_port_cuts(gun_y[k], k + 1);
        // bladder IN pigtail (front wall, 45 degrees down)
        translate([in_xz[0], Di + t, in_xz[1]]) rotate([-45, 0, 0]) rotate([-90, 0, 0])
            translate([0, 0, -12]) cylinder(d = hose_hole, h = 20);
        translate([in_xz[0], Di + t - 0.6, in_xz[1] + 12]) rotate([90, 0, 180]) linear_extrude(1)
            text("IN", size = 5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        // side drains, flush with the floor: front and back walls at the same x; the left wall
        // and the outer wall in the gaps between the corner columns and the port bosses
        for (x = [Wi / 2 - 25, Wi / 2 + 25], y = [-t - 1, Di - 1]) translate([x, y, tf + 2])
            rotate([-90, 0, 0]) cylinder(d = 4, h = t + 2);
        for (y = side_drain_y, x = [-t - 1, Wi - 1]) translate([x, y, tf + 2])
            rotate([0, 90, 0]) cylinder(d = 4, h = t + 2);
        // drains under the pump: a row down the middle, plus the four pocket corners
        for (x = [20 : 10 : 55]) translate([x, Di / 2, -1]) cylinder(d = 4, h = tf + 2);
        for (x = [16, 56], y = [pp[1] + 6, pp[1] + pp[3] - 6]) translate([x, y, -1]) cylinder(d = 4, h = tf + 2);
        // notches at floor level through the pocket fence, so it can't hold water as a tray
        // when the pack lies on its side
        for (yy = [pp[1] - 2, pp[1] + pp[3] - 0.2]) translate([pp[0] + pp[2] / 2 - 3, yy, tf]) cube([6, 2.2, 1.5]);
        for (xx = [pp[0] - 2, pp[0] + pp[2] - 0.2]) translate([xx, pp[1] + pp[3] / 2 - 3, tf]) cube([2.2, 6, 1.5]);
        // tie slots: straps over the pump, and the fittings strip
        for (x = [22, 36, 50], y = [pp[1] - 4, pp[1] + pp[3] + 4])
            translate([x, y, tf / 2]) cross_slot(tf + 2);
        for (p = [[74, 16], [74, 40], [66, 52], [80, 52]])
            translate([p[0], p[1], tf / 2]) cross_slot(tf + 2);
    }
}

// ------------------------------------------------------------ gun port cluster (cup's outer wall)
// From the top: a drip hood, an XT30U well pointing 45 degrees down and out, a hose pigtail
// exit (also 45 degrees down), and a paracord tunnel that enters and leaves the outer face.
//  - XT30U: the pack side is the FEMALE (sockets), so live pins are never exposed. It sits
//    in a well sized for the umbilical's MALE shroud; the shroud slides in around it. Fit it
//    with a spare male plugged in as a jig: push the pair in from inside the cup until the
//    male's rim is flush with the outer face, then fill the well behind the female with hot
//    glue (it pots the solder cups too). Pointing down, the well drains.
//  - Hose pigtail: 60-80 mm of the 3.5 x 5.5 silicone tube pokes out; join the umbilical
//    hose to it with a straight barbed connector from the assortment.
//  - Paracord: in one opening, round the U-tunnel inside the boss, out the other; knot it.
//    The cord is shorter than the wires and hose, so it takes a dropped gun's pull.
sock_axis = [-cos(45), 0, sin(45)];          // from the mouth, inward and up
module sock_frame(yc, z) translate([Wi + t, yc, z]) rotate([0, 45, 0]) children();
module gun_port_solid(yc) {
    // well sleeve (1.2 walls), trimmed at the outer face
    intersection() {
        sock_frame(yc, sock_z) translate([-xt30_len, -(xt30_well[0] / 2 + 1.2), -(xt30_well[1] / 2 + 1.2)])
            cube([xt30_len + 6, xt30_well[0] + 2.4, xt30_well[1] + 2.4]);
        translate([-1, -10, tf]) cube([Wi + t + 0.99 - 0.02, Di + 20, Hw]);
    }
    // hose boss
    intersection() {
        sock_frame(yc, hose_z) rotate([0, -90, 0]) translate([0, 0, -3]) cylinder(d = 9, h = 14);
        translate([-1, -10, tf]) cube([Wi + t + 0.99 - 0.02, Di + 20, Hw]);
    }
    // paracord tunnel boss, standing on the floor
    translate([Wi - 8.5, yc - 9, 0]) cube([8.6, 18, tie_z + 5.5]);
    // drip hood over the well (45-degree underside)
    translate([Wi + t - 0.01, yc - 8, sock_z + 6]) rotate([90, 0, 0]) translate([0, 0, -16])
        linear_extrude(16) polygon([[0, -2.5], [2.5, 0], [2.5, 1.2], [0, 1.2]]);
}
module gun_port_cuts(yc, n) {
    sock_frame(yc, sock_z) translate([-xt30_len - 1, -xt30_well[0] / 2, -xt30_well[1] / 2])
        cube([xt30_len + 10, xt30_well[0], xt30_well[1]]);
    // rear keeper: a zip tie across the sleeve between the female's solder cups, pushed
    // against the back of its body (reach it with the cup off); stops the 12-34 N
    // unplugging force pulling the socket out, so the hot glue only seals
    sock_frame(yc, sock_z) translate([-23, -1.8, -(xt30_well[1] / 2 + 2)]) cube([8, 3.6, xt30_well[1] + 4]);
    sock_frame(yc, hose_z) rotate([0, -90, 0]) translate([0, 0, -5]) cylinder(d = hose_hole, h = 25);
    // U-tunnel: half torus inside the boss, both ends open on the outer face, chamfered
    translate([Wi + t, yc, tie_z]) {
        rotate([0, 0, 90]) rotate_extrude(angle = 180) translate([5.5, 0]) circle(d = 5.2);
        for (s = [-1, 1]) translate([0.01, s * 5.5, 0]) rotate([0, -90, 0]) {
            cylinder(d = 5.2, h = 2);
            cylinder(d1 = 7.2, d2 = 5.2, h = 1);
        }
    }
    // number above the hood
    translate([Wi + t - 0.6, yc, sock_z + 13]) rotate([90, 0, 90]) linear_extrude(1)
        text(str(n), size = 6, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
}
side_drain_y = [11, (gun_y[0] + gun_y[1]) / 2, 61.5];   // gaps: column | port 1 | port 2 | column

// ============================================================ small parts
// PRIME button: TPU boot + ASA guard bezel + TPU plunger.
//  - The boot's flange is clamped under the bezel, which is glued to the cap
//    (ASA to ASA, a strong CA or acetone joint), so nothing relies on glue holding
//    TPU. Silicone under the flange seals it.
//  - The bezel's rim stands 1 mm above the boot, so you need a fingertip to
//    press it; a bump or a strap can't.
//  - Hard stop: the plunger head bottoms on the cap plate after 0.75 mm.
//    The switch clicks at ~0.55 mm; the soft TPU plunger takes up the rest,
//    so even a hard press puts only ~10-15 N on the PCB.
//  - D-shaped flange and bezel: the flat side faces -y, clear of LED3 and
//    the RV2 window.
pr_flat = 7.4;   // distance from the SW1 axis to the flat side (0.3 mm clear of LED3)
module dshape(r) intersection() { circle(r = r); translate([-r - 1, -pr_flat]) square([2 * r + 2, 2 * r + 2]); }
bt_r0 = 5.2;     // inner radius of the boot's straight section
pr_stroke = 0.75;
bt_head_z = pr_stroke + 1.2;          // plunger head top at rest
bt_h0 = bt_head_z - (bt_r0 - 4.5);    // straight section height
bt_top = bt_h0 + 3;
module boot() {
    difference() {
        union() {
            linear_extrude(0.8) dshape(9);
            cylinder(r = 6, h = bt_h0);
            translate([0, 0, bt_h0 - 0.01]) cylinder(r1 = 6, r2 = 3, h = 3);
        }
        translate([0, 0, -0.01]) cylinder(r = bt_r0, h = bt_h0 + 0.02);
        translate([0, 0, bt_h0]) cylinder(r1 = bt_r0, r2 = bt_r0 - 2, h = 2);
    }
}
// guard bezel, modelled in its installed position (sits on the cap top)
module bezel() {
    difference() {
        linear_extrude(bt_top + 1) dshape(10.5);
        translate([0, 0, -1]) cylinder(r = 6.5, h = 20);
        translate([0, 0, -0.01]) linear_extrude(0.6) offset(0.3) dshape(9);   // clamps the 0.8 mm flange
    }
}
// TPU plunger: head under the boot's cone, tip 0.3 mm above SW1 at rest
pl_len = Zt + tp + pr_stroke - (pcb_top_z + sw_h + 0.3);
module plunger() {
    cylinder(d = 9, h = 1.2);
    cylinder(d = 5.8, h = 1.2 + pl_len);
}
// ASA PCB spacer (part 27): one per cap post, so the board hangs pcb_drop lower. Its socket
// slips over the post's stake pin (CA it there); its own pin goes through the board hole and
// gets heat-staked like the original. 5 mm OD because H3 sits 2.75 mm from J2's body.
// Modelled with its top face at z = pcb_drop, pin down.
sp_od = 5.0;
sp_sock = pcb_hole_d - 0.25 + 2 * 0.15;   // 3.25 bore on the 2.95 stake pin
module pcb_spacer() {
    difference() {
        cylinder(d = sp_od, h = pcb_drop);
        translate([0, 0, pcb_drop - 3.5]) cylinder(d = sp_sock, h = 3.6);
        // mouth chamfer: it prints on the bed, so this eats the elephant's foot
        translate([0, 0, pcb_drop - 0.4]) cylinder(d1 = sp_sock, d2 = sp_sock + 0.8, h = 0.41);
    }
    translate([0, 0, -3.2]) cylinder(d = pcb_hole_d - 0.25, h = 3.3);
}
// TPU battery pad: a compliant cap that slips over the end of a cap rib. Printed
// opening-up. The pocket is 0.1 mm tight per side and two 0.4 mm beads on its long
// walls click into grooves cut in the rib, so retention is mechanical (a dab of hot
// glue is only a backup). In the assembly it is modelled with its floor at the cell
// holder and the rib end sitting on the pocket floor.
bp_len = blk_w - 6;
module batpad() {
    // Compliant floor: 0.8 mm bottom skin, 0.8 mm top plate (the rib seat) and six
    // 0.8 mm cross-fins between them, 1.6 mm wide, 6.4 mm apart (so the plate only
    // bridges 6.4 mm). Spring rate ~150-250 N/mm per pad instead of a solid block's
    // kN/mm, so the pad, not the cap plate, takes up the stack tolerance.
    L = bp_len + 2 * bp_wall - 0.4;  W = rib_w + 2 * bp_wall - 0.3;
    n = 6; fw = 0.8; pitch = (L - fw) / (n - 1);
    difference() {
        translate([-bp_wall, -bp_wall, 0]) union() {
            cube([L, W, 0.8]);
            for (k = [0 : n - 1]) translate([k * pitch, (W - 1.6) / 2, 0.79]) cube([fw, 1.6, bp_t - 1.58]);
            translate([0, 0, bp_t - 0.8]) cube([L, W, 0.8 + bp_deep]);
        }
        translate([0.1, -0.1, bp_t]) cube([bp_len - 0.6, rib_w - 0.1, bp_deep + 1]);   // pocket 2.9 mm wide, centred (1.3 mm walls)
    }
    // retaining beads on the two long pocket walls; they click into the rib's grooves
    for (f = [0, 1]) translate([0.3, f == 0 ? -0.1 : rib_w - 0.2, bp_t + bp_deep - 2.8 - 0.7])
        rotate([90, 0, 90]) linear_extrude(bp_len - 1.0)
            polygon(f == 0 ? [[0, 0], [0.4, 0.35], [0.4, 1.05], [0, 1.4]] : [[0, 0], [-0.4, 0.35], [-0.4, 1.05], [0, 1.4]]);
}
// TPU pump mat: sits in the pump pocket under the G528, drain holes line up
// with the cup's floor drains.
module pumpmat() {
    difference() {
        linear_extrude(mp_t) rr(pp[2] - 0.4, pp[3] - 0.4, 2);
        for (x = [20 : 10 : 55]) translate([x - pp[0] - 0.2, Di / 2 - pp[1] - 0.2, -1]) cylinder(d = 6, h = mp_t + 2);
        for (x = [16, 56], y = [pp[1] + 6, pp[1] + pp[3] - 6]) translate([x - pp[0] - 0.2, y - pp[1] - 0.2, -1]) cylinder(d = 6, h = mp_t + 2);
        // perimeter groove ties the grooves together
        translate([-1, -0.01 - 0.4, -0.01]) cube([pp[2] + 2, 1.9, 0.81]);
        translate([-1, pp[3] - 0.4 - 1.5, -0.01]) cube([pp[2] + 2, 1.9, 0.81]);
        translate([-0.4, -1, -0.01]) cube([1.9, pp[3] + 2, 0.81]);
        translate([pp[2] - 0.4 - 1.5, -1, -0.01]) cube([1.9, pp[3] + 2, 0.81]);
        // underside drain grooves (1.5 x 0.8 mm) from the holes to the mat edge, so a flat
        // pump bottom can't seal them shut
        translate([-1, Di / 2 - pp[1] - 0.2 - 0.75, -0.01]) cube([pp[2] + 2, 1.5, 0.81]);
        for (x = [22, 37, 52]) translate([x - pp[0] - 0.2 - 0.75, -1, -0.01]) cube([1.5, pp[3] + 2, 0.81]);
    }
}
// TPU shim set: six flat 5 x 30 mm strips (2x 0.6, 2x 1.0, 2x 1.5 mm thick);
// cut to length and tuck into any pocket where a board rattles. The BMS slot
// has only ~0.6 mm of slack, the buck / ACS758 pockets ~1 mm of width.
module shim() for (i = [0 : 5]) translate([0, i * 6.5, 0]) cube([30, 5, [0.6, 0.6, 1.0, 1.0, 1.5, 1.5][i]]);
module emb_text() text("BubbleLink", size = emb_size, halign = "center", valign = "center",
                       font = "Liberation Sans:style=Bold");
// raised BubbleLink on the tube's outer (+x) wall, reading upward
module emboss() {
    translate([Wi + t - 0.01, Di / 2, Zt / 2 + 6]) rotate([90, 0, 90]) rotate(90)
        union() {   // stepped bevel: the top half is inset 0.3 mm so the letter edges print without a flat overhang
            linear_extrude(emb_h / 2 + 0.01) emb_text();
            translate([0, 0, emb_h / 2]) linear_extrude(emb_h / 2 + 0.01) offset(delta = -0.3) emb_text();
        }
}

// TPU trimmer plug: ONE plug closes both the RV1 (THR) and RV2 (DLY) windows. A 1.2 mm
// plate sits on the cap top with two square plugs (0.1 mm interference per side) pushed
// 2.6 mm into the windows, and a pull tab toward the BubbleLink label. Printed plate-down.
// Modelled with its origin at the cap's top surface, centred between the two windows.
rv_win = [5.6, 5];
rv_c = [for (r = rv_xy) pxy(r + [-3.495, 0])];             // window centres (stick x, y)
rv_mid = (rv_c[0] + rv_c[1]) / 2;
rv_span = abs(rv_c[1][1] - rv_c[0][1]);                    // 11.4 mm, along stick y
module trimplug() {
    w = rv_win[0] + 2;  l = rv_span + rv_win[1] + 2;
    linear_extrude(1.2) hull() {
        translate([-w / 2, -l / 2]) rr(w, l, 1.5);
        translate([0, -l / 2 - 3]) circle(r = 2.2);          // pull tab (toward -y)
    }
    for (sy = [-1, 1]) translate([0, sy * rv_span / 2, 0]) mirror([0, 0, 1]) hull() {
        translate([0, 0, -0.01]) linear_extrude(2.2) square(rv_win + [0.2, 0.2], center = true);
        linear_extrude(2.6) square(rv_win - [0.6, 0.6], center = true);   // lead-in
    }
}
// TPU USB-C plug: fills the CHG counterbore and the window through the 0.8 mm web, so grit
// and spray stay out of the port when you're not charging. Nothing enters the receptacle
// itself (its centre tongue sits right behind the mouth). Pull tab
// toward -y (away from the CHG label). Origin at the cap's top surface.
module usbplug() {
    cb = usb_cbore + [0.2, 0.2];                             // 0.1 mm interference per side
    translate([0, 0, 0]) linear_extrude(1.0) hull() {
        offset(2.6) square(cb - [5.2, 5.2], center = true);
        translate([0, -cb[1] / 2 - 3.5]) circle(r = 2.2);
    }
    mirror([0, 0, 1]) {
        linear_extrude(tp - usb_web) offset(2.6) square(cb - [5.2, 5.2], center = true);
        translate([0, 0, tp - usb_web - 0.01]) linear_extrude(usb_web + 0.01)
            offset(1.6) square(usb_win - [3.2, 3.2], center = true);          // through the web
    }
}

// Power key: an XT60H FEMALE with its two solder cups bridged by a short 12 AWG U-loop,
// hot-glued into this ASA grip. In = ON, out = OFF (and the full battery disconnect for
// storage; the charger still works with the key out). Lanyard hole so it can't get lost.
module powerkey() {
    w = xt60_body[0] + 3.4;  d = xt60_body[1] + 3.4;  h = 22;
    difference() {
        hull() for (sx = [-1, 1], sy = [-1, 1]) translate([sx * (w / 2 - 2), sy * (d / 2 - 2), 0]) cylinder(r = 2, h = h);
        translate([-(xt60_body[0] - 0.4) / 2, -(xt60_body[1] - 0.4) / 2, -1]) cube([xt60_body[0] - 0.4, xt60_body[1] - 0.4, 15]);
        translate([0, 0, h - 4.5]) rotate([90, 0, 0]) cylinder(d = 4, h = d + 2, center = true);   // lanyard
        for (z = [4 : 3 : 13]) for (sx = [-1, 1]) translate([sx * w / 2, 0, z]) cube([1, d + 2, 1.2], center = true);   // grip ribs
    }
}
// TPU USB-A plug for the LED 5 V port: fills the counterbore and the window, pull tab down
module usbAplug() {
    cb = usbA_cb + [0.2, 0.2];
    linear_extrude(1.0) hull() {
        offset(1.6) square(cb - [3.2, 3.2], center = true);
        translate([-cb[0] / 2 - 3.5, 0]) circle(r = 2.2);
    }
    mirror([0, 0, 1]) linear_extrude(t - 0.8) offset(1.6) square(cb - [3.2, 3.2], center = true);
}
// TPU gun-port cap: closes an unplugged XT30U well (an unused channel, or while the
// umbilical is off). Water sitting across the two live sockets would leak current and
// corrode them. A sleeve presses into the well around the female's nose; pull tab.
module gunportcap() {
    linear_extrude(1.0) hull() {
        offset(1.2) square(xt30_well + [0.1, 0.1], center = true);
        translate([xt30_well[0] / 2 + 4, 0]) circle(r = 2.2);
    }
    mirror([0, 0, 1]) difference() {
        linear_extrude(5) offset(0.5) square(xt30_well + [0.1, 0.1] - [1, 1], center = true);
        translate([0, 0, -0.01]) linear_extrude(6) square(xt30_well - [2.4, 2.4], center = true);
    }
}
// TPU key blank: closes the key socket while the key is out (storage). One side of the
// socket stays live with the key out, so keep water out of it. Lanyard hole: tie it to
// the key's lanyard so one is always in the socket.
module keyblank() {
    win = [xt60_body[1] - 1.0, xt60_body[0] - 1.0];
    linear_extrude(1.0) hull() {
        offset(1.2) square(win, center = true);
        translate([0, win[1] / 2 + 5]) circle(r = 3);
    }
    mirror([0, 0, 1]) {
        linear_extrude(0.8) offset(0.1) square(win, center = true);
        translate([0, 0, 0.79]) linear_extrude(1.5) offset(-0.3) square(win, center = true);
    }
}
module keyblank_print() difference() {
    translate([0, 0, 1.0]) rotate([180, 0, 0]) keyblank();
    translate([0, -(xt60_body[0] - 1.0) / 2 - 5, -1]) cylinder(d = 2.5, h = 5);
}
// TPU key gasket: glue it under the key grip; it presses on the cap top round the socket
// when the key is home (sand the grip or add a shim strip to get 0.2-0.3 mm squeeze).
module keygasket() difference() {
    hull() for (sx = [-1, 1], sy = [-1, 1])
        translate([sx * ((xt60_body[0] + 3.4) / 2 - 2), sy * ((xt60_body[1] + 3.4) / 2 - 2), 0]) cylinder(r = 2, h = 1.5);
    translate([0, 0, -1]) linear_extrude(4) square([xt60_body[0] - 0.4, xt60_body[1] - 0.4], center = true);
}
// Port fit coupon: a 2.4 mm wall with each port, so the real connectors can be checked
// before the cup, cap and tube are printed. Left to right: XT30U well (with a 10 mm
// sleeve), hose pigtail hole, USB-A window + counterbore, XT60H key socket with its lip.
module coupon_ports() {
    difference() {
        union() {
            cube([84, 26, t]);
            translate([13 - xt30_well[0] / 2 - 1.2, 13 - xt30_well[1] / 2 - 1.2, 0]) cube([xt30_well[0] + 2.4, xt30_well[1] + 2.4, 10]);
            translate([70 - xt60_body[0] / 2 - 1.2, 13 - xt60_body[1] / 2 - 1.2, 0]) cube([xt60_body[0] + 2.4, xt60_body[1] + 2.4, 10]);
        }
        translate([13 - xt30_well[0] / 2, 13 - xt30_well[1] / 2, -1]) cube([xt30_well[0], xt30_well[1], 12]);
        translate([28, 13, -1]) cylinder(d = hose_hole, h = t + 2);
        translate([45, 13, -1]) linear_extrude(t + 2) offset(0.5) square([usbA_win[0] - 1, usbA_win[1] - 1], center = true);
        translate([45, 13, 0.8]) linear_extrude(t) offset(1.5) square([usbA_cb[0] - 3, usbA_cb[1] - 3], center = true);
        translate([70 - xt60_body[0] / 2, 13 - xt60_body[1] / 2, 0.8]) cube([xt60_body[0], xt60_body[1], 12]);
        translate([70, 13, -1]) linear_extrude(3) offset(0.8) square([xt60_body[0] - 2.6, xt60_body[1] - 2.6], center = true);
    }
}

// TPU seal ring: stretches over the skirt into the groove
module ring() {
    linear_extrude(ring_h) difference() { in2d(ring_sq); in2d(-sk_c - gr_d); }
}
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
    [5, 2.7, awg16_od - 0.2], [9, 2.7, awg16_od - 0.2],        // gun 1 pair
    [14.5, 2.7, awg16_od - 0.2], [18.5, 2.7, awg16_od - 0.2],  // gun 2 pair
    [25, 2.7, pump_od - 0.2], [28, 2.7, pump_od - 0.2]];       // pump leads
// (the XT60H key and the LED-backpack USB no longer cross the bulkhead)
gm_f = 2.0;   // grommet flange width
sk_lip = 0.8; sk_wall = 1.0; sk_drop = 8;   // drip skirt under the bulkhead
// extra = extra neck length (the lower half also passes the skirt's lip)
module grommet_half(extra = 0) {
    w = gs[2]; h = gs[3]; f = gm_f; ft = 1.2;
    difference() {
        union() {
            linear_extrude(ft) offset(f) rr(w, h, 2);
            translate([0, 0, ft - 0.01]) linear_extrude(tb / 2 + extra + 0.01) offset(-0.1) rr(w, h, 2);
        }
        for (c = gm_holes) translate([c[0], c[1], -1]) cylinder(d = c[2], h = 10, $fn = 24);
    }
}

// ASA drip skirt on the cup side of the grommet: its lip is clamped
// between the bulkhead and the lower grommet flange, and its 8 mm wall hangs
// down around the cable exit. Water running along the underside of the
// bulkhead drips off its edge, and spray from a leaking fitting can't hit
// the grommet directly. Print lip-down.
module skirt() {
    w = gs[2]; h = gs[3];
    linear_extrude(sk_lip) difference() { offset(gm_f + 0.2 + sk_wall) rr(w, h, 2); rr(w, h, 2); }
    linear_extrude(sk_lip + sk_drop) difference() {
        offset(gm_f + 0.2 + sk_wall) rr(w, h, 2); offset(gm_f + 0.2) rr(w, h, 2);
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
    if (i == 6) color("cyan", 0.4) {                                                              // bucks + ACS758
        for (k = [0:1]) let(p = pk[k], b = k < 1 ? buck_sz : acs_sz) translate([p[0] + 0.5, pf + 0.2, p[2]]) cube(b);
        translate([bb_x0, bb_yb - bb_sz[1], bb_z0]) cube([bb_sz[0], bb_sz[1], bb_sz[2]]);         // Buck B (tube shelf)
    }
    if (i == 7) color("tan", 0.4) translate([pp[0] + 0.6, pp[1] + 0.75, -tb - Hw + mp_t]) cube(pump_sz);  // pump
}

if (part == "tube")      translate([0, 0, tb]) tube();
else if (part == "cap")  translate([0, 0, Zt + tp]) rotate([180, 0, 0]) cap();
else if (part == "sled") sled();
else if (part == "cup")  cup();
else if (part == "plunger") plunger();
// four spacers plus two spares, socket down so the pin prints upright
else if (part == "pcbspacer") for (k = [0:5]) translate([k * 9, 0, pcb_drop]) rotate([180, 0, 0]) pcb_spacer();
else if (part == "ring") ring();
else if (part == "grommet_lo") grommet_half(sk_lip);
else if (part == "skirt") skirt();
else if (part == "bezel") translate([0, 0, bt_top + 1]) rotate([180, 0, 0]) bezel();
else if (part == "grommet_hi") translate([0, gs[3], 0]) mirror([0, 1, 0]) grommet_half();
else if (part == "boot") boot();
else if (part == "washer") washer();
else if (part == "batpad") batpad();
else if (part == "pumpmat") pumpmat();
else if (part == "shim") shim();
else if (part == "trimplug") translate([0, 0, 1.2]) rotate([180, 0, 0]) trimplug();
else if (part == "usbplug") translate([0, 0, 1.0]) rotate([180, 0, 0]) usbplug();
else if (part == "usbAplug") translate([0, 0, 1.0]) rotate([180, 0, 0]) usbAplug();
else if (part == "powerkey") powerkey();
else if (part == "keyblank") keyblank_print();
else if (part == "keygasket") keygasket();
else if (part == "gunportcap") for (k = [0, 1]) translate([k * 22, 0, 1.0]) rotate([180, 0, 0]) gunportcap();
else if (part == "coupon_ports") coupon_ports();
// The part of the cap with the voltmeter hole and the charger slot, plate down: check
// both with the real voltmeter and charger before printing a whole lid.
else if (part == "coupon_cap")
    translate([0, Di, Zt + tp]) rotate([180, 0, 0]) intersection() {
        cap();
        translate([3.5, 11, Zt - 31]) cube([34, 53.5, 40]);
    }
else if (part == "none") {}
// Fit coupons for the stick in the real filament (ASA shrinks more than PETG): a 19 mm slice of the
// tube rim (16 mm below the rim + the bulkhead offset), the matching slice of the cap skirt (groove, ring land, screw slot), and a bulkhead corner
// with a cup-screw nut pocket. Print these first; the cap slice must drop into the rim slice with the
// TPU ring on it, and an M3 nut must press into the hex pockets.
else if (part == "coupon_rim")
    translate([0, 0, -(Zt - 16)]) intersection() {
        translate([0, 0, tb]) tube();
        translate([-10, -10, Zt - 16]) cube([Wi + 20, Di + 20, 20]);
    }
else if (part == "coupon_skirt")
    translate([0, Di, Zt + 1.5]) rotate([180, 0, 0]) intersection() {
        cap();
        translate([0, 0, Zt - sk_h - 2]) linear_extrude(sk_h + 3.5)
            difference() { in2d(1); in2d(-sk_c - sk_t - 10); }
    }
else if (part == "coupon_nut")
    intersection() {
        translate([0, 0, tb]) tube();
        translate([-3, -3, 0]) cube([19, 19, tb + base_t + 3]);
    }
else {
    tube(); %cap(); sled();
    translate([0, 0, -tb - Hw - tf]) cup();
    for (i = [0:7]) ghost(i);
    for (h = holes) let(p = pxy(h)) color("#6f9fbd") translate([p[0], p[1], pcb_top_z]) pcb_spacer();
    installed_tpu();
}

// TPU parts in their installed positions (assembly preview and checks)
module installed_tpu() {
    color("black") {
        translate([0, 0, gr_z + 0.4]) ring();
        // lower grommet half: flange under the skirt lip, neck up into the slot
        translate([gs[0], gs[1], -tb - sk_lip - 1.2]) grommet_half(sk_lip);
        // upper half: flange on the bulkhead's top face, neck down into the slot
        translate([gs[0], gs[1], 1.2]) mirror([0, 0, 1]) grommet_half();
        let(c = pxy(sw_xy)) translate([c[0], c[1], Zt + tp]) boot();
    }
    color("#6f9fbd") {
        let(c = pxy(sw_xy)) translate([c[0], c[1], Zt + tp]) bezel();
        translate([gs[0], gs[1], -tb]) mirror([0, 0, 1]) skirt();
        for (y = [-t - 1, Di + t]) translate([cap_sx, y, cap_sz]) rotate([-90, 0, 0]) washer();
    }
    color("black") {
        for (y = bp_y) translate([bat[0] + 3 + 0.2, y - 1.35, bat_top - bp_ov]) batpad();
        translate([pp[0] + 0.2, pp[1] + 0.2, -tb - Hw]) pumpmat();
        translate([rv_mid[0], rv_mid[1], Zt + tp]) trimplug();
        translate([usb_xy[0], usb_xy[1], Zt + tp]) usbplug();
        translate([Wi + t, bb_port[0], bb_port[1]]) rotate([0, 90, 0]) rotate([0, 0, 90]) usbAplug();
    }
}
