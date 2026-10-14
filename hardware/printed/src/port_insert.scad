// Port inserts for the dry core's 36 mm square ports. Each one is a quick
// print, so a wrong guess about an unmeasured part costs one small reprint,
// not the box or lid. Push in from outside and glue (CA or hot glue).
//
//   type = "voltmeter"  round hole for the Stlxy voltmeter (lid)
//   type = "breaker"    finger hole over the breaker's reset (lid)
//   type = "usbc"       USB-C window, offset 10 mm toward the floor. Its plug
//                       has chamfered top corners like the wall port, so it
//                       only fits one way (arrow toward the back plate). Seat the receptacle
//                       in the window, set the charger on a spacer, and
//                       zip-tie it to the floor grid; glue alone won't hold
//                       against plugging in (right wall)
//   type = "blank"      closes an unused port
//
// Print flange-down, PETG, no supports.

include <params.scad>

type = "voltmeter";

port = 36;           // must match dry_core.scad
wall = 2.4;          // lid / wall thickness
flange = 1.6;

vm_hole   = 29.0;    // [ESTIMATE] MEASURE the voltmeter body behind its
                     // 33.8 mm bezel and set this 0.4 mm larger
brk_hole  = 30.0;    // [ESTIMATE] big enough for a fingertip on the reset
usb_win   = [9.8, 4.0];    // through-window for the plug's metal shell
usb_cbore = [13.5, 7.5];   // outside counterbore for the plug overmold
usb_web   = 0.8;           // material left at the window, so the plug seats
usb_dz    = -10;           // window offset toward the floor (see the arrow)

module rsq(s, r) { offset(r) square([s[0] - 2 * r, s[1] - 2 * r], center = true); }

// must match port_profile() in dry_core.scad
module port_profile(s = port, ch = 11) {
    polygon([[-s / 2, -s / 2], [s / 2, -s / 2], [s / 2, s / 2 - ch],
             [s / 2 - ch, s / 2], [-s / 2 + ch, s / 2], [-s / 2, s / 2 - ch]]);
}

difference() {
    union() {
        linear_extrude(flange) rsq([port + 6, port + 6], 3);
        if (type == "usbc")   // wall port: chamfered top, same as the box
            linear_extrude(flange + wall) offset(-0.2) port_profile();
        else
            linear_extrude(flange + wall) rsq([port - 0.4, port - 0.4], 1.5);
    }
    if (type == "voltmeter")
        translate([0, 0, -1]) cylinder(d = vm_hole, h = 10, $fn = 128);
    if (type == "breaker")
        translate([0, 0, -1]) cylinder(d = brk_hole, h = 10, $fn = 128);
    if (type == "usbc") translate([0, usb_dz, 0]) {
        translate([0, 0, -1]) linear_extrude(10) rsq(usb_win, 1.6);
        translate([0, 0, -1]) linear_extrude(flange + wall - usb_web + 1) rsq(usb_cbore, 2.5);
    }
    // arrow on the outside face: point it at the floor (toward the back plate)
    if (type == "usbc")
        translate([0, 9, -0.01]) mirror([1, 0, 0]) linear_extrude(0.6)
            polygon([[-1, 8], [1, 8], [1, 3], [3, 3], [0, 0], [-3, 3], [-1, 3]]);
}
