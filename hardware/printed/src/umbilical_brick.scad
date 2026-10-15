// Umbilical brick: strain-relief anchor where an umbilical meets a GUN. Print 2
// (one per umbilical). The pack end needs no brick: it plugs into a gun port
// cluster on the stick's cup (XT30U well, hose pigtail, paracord tunnel).
//
// Layout, looking down (+x points toward the umbilical):
//   y = +10  open groove for the 3.5 x 5.5 fluid tube (passes straight through)
//   y =  -2  open groove for the 16 AWG red/black pair
//            with an open-top XT30U pocket at the -x end (drop the housing
//            in, strap it with a zip tie, glue optional; its mating face
//            points away from the umbilical)
//   y = -13  two 5 mm vertical holes for 550 paracord: the umbilical tether
//            ties to the +x hole, the gun ties to the -x hole
// Narrow zip ties through the vertical slots hold the tube and wires down.
// The fluid hose is semi-permanent (canonical facts); the XT30U is the
// disconnect.
//
// Print flat (base on the bed), ASA or PETG, no supports.

include <params.scad>

with_xt30 = true;

L = 44; W = 35; Hb = 14;
tube_y = 10; wire_y = -2; cord_y = -13;
tube_floor = Hb - tube_od + 0.5;   // tube stands 0.5 proud so the tie grips it
wire_floor = 11.0;                 // wires stand 0.2 proud so the ties grip
pocket_z = Hb - xt30_h - 2 * fit_clear + 0.3;   // housing stands 0.3 proud
tube_g = tube_od + 0.4;
wire_g = 2 * awg16_od + 0.6;
pocket_d = 11;
pw = xt30_w + 2 * fit_clear;
ph = xt30_h + 2 * fit_clear;

module slot(x, y) {
    translate([x, y, Hb / 2]) cube([ziptie_w, ziptie_t, Hb + 2], center = true);
}

difference() {
    // rounded block
    hull() for (sx = [-1, 1], sy = [-1, 1])
        translate([sx * (L / 2 - 3), sy * (W / 2 - 3), 0]) cylinder(r = 3, h = Hb);

    // tube groove with a flared exit on the umbilical side
    translate([-L / 2 - 1, tube_y - tube_g / 2, tube_floor]) cube([L + 2, tube_g, Hb]);
    translate([L / 2, tube_y, tube_floor + tube_g / 2]) rotate([0, 90, 0])
        cylinder(d1 = tube_g, d2 = tube_g + 3, h = 3, center = true);
    // wire groove
    translate([-L / 2 - 1, wire_y - wire_g / 2, wire_floor]) cube([L + 2, wire_g, Hb]);
    // XT30U pocket, open on top. The housing stands 0.3 mm proud so a zip
    // tie through the slots either side straps it down: unplugging pulls on
    // the tie and the pocket's back wall, not on glue or the solder joints.
    if (with_xt30) {
        translate([-L / 2 - 1, wire_y - pw / 2, pocket_z]) cube([pocket_d + 1, pw, Hb]);
        for (s = [-1, 1]) slot(-L / 2 + 5, wire_y + s * (pw / 2 + 1.9));
    }
    // paracord holes, chamfered both sides so the cord doesn't chafe
    for (x = [-9, L / 2 - 7]) translate([x, cord_y, -1]) {   // -x hole clears the XT30U tie slot
        cylinder(d = paracord_d + 1, h = Hb + 2);
        cylinder(d1 = paracord_d + 4, d2 = paracord_d + 1, h = 2.5);
        translate([0, 0, Hb + 2 - 2.5]) cylinder(d1 = paracord_d + 1, d2 = paracord_d + 4, h = 2.5);
    }
    // zip-tie slots straddling each groove
    for (x = [-12, 4, 16], s = [-1, 1]) slot(x, tube_y + s * (tube_g / 2 + 1.9));
    for (x = [-4, 12], s = [-1, 1]) slot(x, wire_y + s * (wire_g / 2 + 1.9));
}
