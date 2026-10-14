// Dry core: one closed box holding the battery and all the electronics.
// It replaces the battery cartridge, electronics tray, wet/dry divider, PCB
// bracket, breaker bracket, both buck mounts, the ACS758 mount, the
// voltmeter mount, and the control faceplate.
//
// Worn orientation: the back plate rests against the wearer's back, +y is
// up, the lid faces outward. The wet bay (pump module, bladder) sits below.
// Every cable leaves through the BOTTOM wall, so drips can't run in.
//
//   Battery bay (top)   2S5P block in its two cell holders, held by a fence
//                       and pressed down by ribs on the lid
//   BMS zone (top right)
//   Breaker fence (bottom left), reset reached through a lid port
//   Electronics field   ACS758, Buck A, Buck B on a grid of zip-tie slots;
//                       the USB-C charger glues behind a port in the right wall
//   CTRL PCB            hangs from the LID, component side up: the LEDs show
//                       through light tunnels, RV1/RV2 adjust through slots,
//                       and PRIME is a flexure button in the lid
//
// The parts whose size is not yet measured (BMS, charger, bucks, ACS758,
// breaker) are held with zip ties through the slot grid, not tight pockets,
// so the box doesn't depend on their exact dimensions. The three
// unmeasured panel features (voltmeter, breaker reset, USB-C) are separate
// 15-minute port inserts (port_insert.scad), so a wrong guess costs one small
// reprint, not the box.
//
// No screws: the PCB heat-stakes onto the lid pins (soldering iron), the lid
// laces to the box with zip ties or paracord through the four ears.
//
// part = "box"       print back-plate down on the K2 Plus, no supports
// part = "lid"       print outer face down, no supports
// part = "assembly"  preview with ghost components, for checking fit

include <params.scad>

part = "assembly";

// ------------------------------------------------------------ main sizes
W  = 152;    // inner width  (x)
H  = 166;    // inner height (y, up when worn)
D  = 47;     // inner depth  (z): 44 mm breaker + 3 mm
t  = 2.4;    // wall
tb = 2.4;    // back plate
tl = 2.4;    // lid plate
rc = 4;      // outer corner radius

// ------------------------------------------------------------ battery bay
blk_x = 2 * (2.25 * cell_pitch + cell_bore / 2 + holder_wall);  // holder length
blk_z = cell_pitch * sin(60) + cell_bore + 2 * holder_wall;     // holder width
blk_y = cell_h + 2 * holder_lip + 1;                            // incl. tabs
bay = [2, 88, blk_x + 2.4, H - 2 - 88];   // x, y, w, h (fence inner)
fence_t = 2; fence_h = 16;
blk_y0 = bay[1] + (bay[3] - blk_y) / 2;    // battery block placed centred

// ------------------------------------------------------------ breaker
brk = [2, 2, 75, 51];                      // fence inner: 72 x 48 + clearance
brk_h = 44;                                // [LISTING]

// ------------------------------------------------------------ PCB (on lid)
pcb_c = [W - 2 - pcb_w / 2 - 1, 60];       // board centre
pcb_top_z = D - 22;                        // component face; 22 mm under lid
post_d = 4.5;                              // clears J2's 9.9 mm body by 0.5 mm

// PCB features, mm from board centre (BubbleLink CTRL v1.2 release files)
led_xy = [[-5.2, 16.7], [0, 16.7], [5.2, 16.7]];
rv_xy  = [[-5.2, 10.1], [6.2, 10.1]];
sw_xy  = [14.7, 12.4];
holes  = [for (sx = [-1, 1], sy = [-1, 1]) [sx * pcb_hole_dx / 2, sy * pcb_hole_dy / 2]];
led_h = 5.3;          // 3 mm LED body above board
sw_h  = 4.3;          // B3F-1000 actuator above board

// ------------------------------------------------------------ ports
port = 36;            // square opening for a port insert
vm_c  = [64, 70];     // voltmeter port (lid)
brk_c = [40, 28];     // breaker reset port (lid), over the breaker
usb_c = [20, 20];     // USB-C port in the right wall: [y, z]. The insert's
                      // window sits 10 mm below the port centre (10 mm off
                      // the floor) so the charger can be zip-tied down.
// Bottom-wall cable slots: gun ch1, gun ch2, pump + Buck B USB, and the
// battery disconnect loop (the XT60H pair hangs just outside the box, so it
// can be unplugged without unlacing the lid).
cable_x = [88, 106, 124, 142];
cable_w = 14; cable_hz = 10; cable_z = 30;

ears_y = [62, H - 24];   // clear of the USB-C port flange on the right wall

// ============================================================ helpers
// Wall-port outline, (horizontal, up): 36 mm square, top corners chamfered
// so the remaining bridge is 14 mm. Shared with port_insert.scad.
module port_profile(s = port, ch = 11) {
    polygon([[-s / 2, -s / 2], [s / 2, -s / 2], [s / 2, s / 2 - ch],
             [s / 2 - ch, s / 2], [-s / 2 + ch, s / 2], [-s / 2, s / 2 - ch]]);
}

module rrect(w, h, r) {
    translate([r, r]) offset(r) square([w - 2 * r, h - 2 * r]);
}

module cross_slot(h) {
    translate([0, 0, h / 2]) {
        cube([ziptie_w, ziptie_t, h + 2], center = true);
        cube([ziptie_t, ziptie_w, h + 2], center = true);
    }
}

module grid(x0, y0, x1, y1, pitch = 12) {
    for (x = [x0 : pitch : x1], y = [y0 : pitch : y1])
        translate([x, y, -tb - 0.5]) cross_slot(tb);
}

module ear(y, side) {   // side -1 = left wall, +1 = right wall
    xw = side < 0 ? -t : W + t;
    translate([xw, y, 0]) difference() {
        union() {
            translate([side < 0 ? -9 : -0.5, -6, D - 6]) cube([9.5, 12, 6]);
            // 45-degree gusset under the ear
            hull() {
                translate([side < 0 ? -9 : -0.5, -6, D - 6]) cube([9.5, 12, 0.01]);
                translate([side < 0 ? -0.5 : -0.5, -6, D - 15]) cube([1, 12, 0.01]);
            }
        }
        translate([side * 4.5, 0, D - 20]) cylinder(d = 5, h = 30);
    }
}

// ============================================================ box
module box() {
    difference() {
        union() {
            // shell
            translate([-t, -t, -tb]) linear_extrude(D + tb)
                rrect(W + 2 * t, H + 2 * t, rc);
            for (y = ears_y, s = [-1, 1]) ear(y, s);
        }
        // cavity
        linear_extrude(D + 1) square([W, H]);
        // slot grids: breaker, electronics field, BMS zone
        grid(brk[0] + 6, brk[1] + 6, brk[0] + brk[2] - 4, brk[1] + brk[3] - 4);
        grid(84, 8, W - 6, 80);
        grid(8, 62, 78, 80);
        grid(bay[0] + bay[2] + fence_t + 5, bay[1] + 6, W - 5, H - 6);
        // cable slots, bottom wall
        for (x = cable_x) translate([x - cable_w / 2, -t - 1, cable_z])
            cube([cable_w, t + 2, cable_hz]);
        // weep holes at the bottom of the bottom wall
        for (x = [86, 104, 122, 140]) translate([x, 1, 1.6]) rotate([90, 0, 0])
            cylinder(d = 3, h = t + 4);
        // USB-C port, right wall
        // the top corners are chamfered 45 degrees so the opening prints
        // without a 36 mm bridge; the insert has the same shape, so it can
        // only go in one way
        translate([W - 1, usb_c[0], usb_c[1]]) rotate([90, 0, 90])
            linear_extrude(t + 2) port_profile();
    }
    // battery bay fence, with notches for the 12 AWG leads
    difference() {
        translate([bay[0] - fence_t, bay[1] - fence_t, 0])
            cube([bay[2] + 2 * fence_t, bay[3] + 2 * fence_t, fence_h]);
        translate([bay[0], bay[1], -1]) cube([bay[2], bay[3], fence_h + 2]);
        for (y = [bay[1] + 4, bay[1] + bay[3] - 14])
            translate([bay[0] + bay[2] - 1, y, 6]) cube([fence_t + 2, 10, fence_h]);
        translate([bay[0] + bay[2] / 2 - 5, bay[1] - fence_t - 1, 6]) cube([10, fence_t + 2, fence_h]);
    }
    // breaker fence (low, so the ring-lug wiring clears it)
    difference() {
        translate([brk[0] - fence_t, brk[1] - fence_t, 0])
            cube([brk[2] + 2 * fence_t, brk[3] + 2 * fence_t, 12]);
        translate([brk[0], brk[1], -1]) cube([brk[2], brk[3], 14]);
    }
}

// ============================================================ lid
// Modelled in its closed position (assembled coordinates).
tongue = [4, 25];     // PRIME flexure: width, length (root toward +y); ~2-3 N to press
tongue_dx = 0.5;      // tongue sits 0.5 mm right of SW1, clear of the wider RV2 slot

module lid() {
    pc = [pcb_c[0], pcb_c[1]];
    sw = pc + sw_xy;
    difference() {
        union() {
            translate([-t, -t, D]) linear_extrude(tl) rrect(W + 2 * t, H + 2 * t, rc);
            // locating skirt inside the walls
            translate([0, 0, D - 5]) linear_extrude(5) difference() {
                translate([0.3, 0.3]) square([W - 0.6, H - 0.6]);
                translate([2, 2]) square([W - 4, H - 4]);
            }
            // ears
            for (y = ears_y, s = [-1, 1])
                translate([s < 0 ? -t - 9 : W + t - 0.5, y - 6, D]) cube([9.5, 12, tl]);
            // ribs pressing on the two cell holders
            for (y = [blk_y0 + holder_t / 2, blk_y0 + blk_y - holder_t / 2])
                translate([bay[0] + 10, y - 1.5, blk_z + 0.6]) cube([bay[2] - 20, 3, D - blk_z - 0.6]);
            // PCB posts with heat-stake pins
            for (h = holes) translate([pc[0] + h[0], pc[1] + h[1], 0]) {
                translate([0, 0, pcb_top_z]) cylinder(d = post_d, h = D - pcb_top_z);
                translate([0, 0, pcb_top_z - 1.6 - 1.6]) cylinder(d = pcb_hole_d - 0.25, h = 3.3);
            }
            // light-tunnel block over the three LEDs
            translate([pc[0] - 8.2, pc[1] + 16.7 - 2.8, pcb_top_z + led_h + 1])
                cube([16.4, 5.6, D - pcb_top_z - led_h - 1]);
            // PRIME nub hangs from the tongue
            translate([sw[0] + 0.25, sw[1], pcb_top_z + sw_h + 0.4])
                cylinder(d = 3.4, h = D - pcb_top_z - sw_h - 0.4 + 0.01);
        }
        // ports
        for (c = [vm_c, brk_c]) translate([c[0], c[1], D - 6])
            linear_extrude(tl + 7) square(port, center = true);
        // LED windows
        for (l = led_xy) translate([pc[0] + l[0], pc[1] + l[1], pcb_top_z])
            cylinder(d = 3.6, h = 40);
        // trimmer access slots
        for (r = rv_xy) translate([pc[0] + r[0], pc[1] + r[1], D - 1])
            // The 3296W screw sits ~3.5 mm from the centre, at the pin-1 end
            // (KiCad Bourns footprint); 9 mm covers either end in case a
            // trimmer goes in reversed.
            linear_extrude(tl + 2) square([9, 4.6], center = true);
        // PRIME flexure: U-shaped cut, free end just below the switch, root
        // toward +y (clear of the H4 post and the RV2 slot)
        translate([sw[0] + tongue_dx, sw[1] - 3, D - 1]) linear_extrude(tl + 2) difference() {
            translate([-tongue[0] / 2 - 1, -1]) square([tongue[0] + 2, tongue[1] + 1]);
            translate([-tongue[0] / 2, 0]) square([tongue[0], tongue[1] + 0.1]);
        }
        // ear holes
        for (y = ears_y, s = [-1, 1])
            translate([s < 0 ? -t - 4.5 : W + t + 4.5, y, D - 1]) cylinder(d = 5, h = tl + 2);
        // labels on the outer face
        translate([0, 0, D + tl - 0.6]) linear_extrude(1) {
            for (i = [0:2]) translate([pc[0] + led_xy[i][0], pc[1] + 19.5]) rotate(90)
                text(["PWR", "GUN", "PUMP"][i], size = 2.8, valign = "center",
                     font = "Liberation Sans:style=Bold");
            translate([pc[0] + rv_xy[0][0], pc[1] + rv_xy[0][1] - 5.5])
                text("THR", size = 3, halign = "center", font = "Liberation Sans:style=Bold");
            translate([pc[0] + rv_xy[1][0], pc[1] + rv_xy[1][1] - 5.5])
                text("DLY", size = 3, halign = "center", font = "Liberation Sans:style=Bold");
            translate([sw[0], sw[1] + 24])
                text("PRIME", size = 3, halign = "center", font = "Liberation Sans:style=Bold");
            translate([brk_c[0], brk_c[1] - port / 2 - 6])
                text("BREAKER", size = 4, halign = "center", font = "Liberation Sans:style=Bold");
            translate([W / 2, H - 22])
                text("BubbleLink", size = 9, halign = "center", font = "Liberation Sans:style=Bold");
            translate([W / 2, H - 34])
                text("2S5P 25R  7.2V  12.5Ah  90Wh", size = 4.5, halign = "center",
                     font = "Liberation Sans:style=Bold");
        }
    }
}

// ============================================================ ghosts
module ghost(i) {
    if (i == 0) color("orange", 0.5) translate([bay[0] + (bay[2] - blk_x) / 2, blk_y0, 0]) cube([blk_x, blk_y, blk_z]);
    if (i == 1) color("red", 0.5) translate([brk[0] + 1.5, brk[1] + 1.5, 0]) cube([72, 48, brk_h]);
    if (i == 2) color("green", 0.6) translate([pcb_c[0] - pcb_w / 2, pcb_c[1] - pcb_h / 2, pcb_top_z - 1.6 - 2])
        cube([pcb_w, pcb_h, 1.6 + 2]);   // board + 2 mm of THT leads under it
    if (i == 3) color("gray", 0.5) translate([vm_c[0], vm_c[1], D - 18]) cylinder(d = 33.8, h = 18);
    if (i == 4) color("blue", 0.4) for (p = [[86, 10], [86, 40]]) translate([p[0], p[1], 0]) cube([30, 25, 15]);
    if (i == 5) color("purple", 0.4) translate([10, 62, 0]) cube([37, 18, 15]);
}

module ghosts() {
    // battery block
    color("orange", 0.5) translate([bay[0] + (bay[2] - blk_x) / 2, blk_y0, 0]) cube([blk_x, blk_y, blk_z]);
    // breaker
    color("red", 0.5) translate([brk[0] + 1.5, brk[1] + 1.5, 0]) cube([72, 48, brk_h]);
    // PCB and its tallest parts
    color("green", 0.6) translate([pcb_c[0] - pcb_w / 2, pcb_c[1] - pcb_h / 2, pcb_top_z - 1.6])
        cube([pcb_w, pcb_h, 1.6]);
    color("black", 0.6) translate([pcb_c[0] - 7, pcb_c[1] - 15.2, pcb_top_z]) cylinder(d = 5, h = 11);
    // voltmeter body behind the lid
    color("gray", 0.5) translate([vm_c[0], vm_c[1], D - 18]) cylinder(d = 33.8, h = 18);
    // bucks and ACS758 (sizes are guesses)
    color("blue", 0.4) for (p = [[86, 10], [86, 40]]) translate([p[0], p[1], 0]) cube([30, 25, 15]);
    color("purple", 0.4) translate([10, 62, 0]) cube([37, 18, 15]);
}

if (part == "box") translate([0, 0, tb]) box();
else if (part == "lid") translate([0, 0, D + tl]) rotate([180, 0, 0]) lid();
else { box(); %lid(); ghosts(); }
