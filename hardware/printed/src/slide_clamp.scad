// Slide clamp for the 3.5 x 5.5 mm silicone tube. Print three:
//   1x bypass restrictor (pump outlet tee -> clamp -> check valve)
//   2x channel shutoff (one per gun channel)
//
// The tube lies in a channel whose floor ramps up. A slider rides on dovetail
// rails over the channel; a rounded ridge under it squeezes the tube against
// the floor. Slide toward the tunnel end to close.
//   x = -8 .. 4    gap 6.0 mm   tube fully open (load the slider here)
//   x =  4 .. 12   gap 6.0 -> 2.4 (coarse)
//   x = 12 .. 34   gap 2.4 -> 0.6 (fine: 1 mm of travel = ~0.08 mm of gap)
//   x = 34 .. 44   gap 0.6     tube sealed (1.0 with the dovetail's play)
// Stop blocks on the wall tops halt the slider with the ridge at x = 35, in
// the sealed zone. The tube stays at the sealed-floor height to the end of
// the body, so it is never kinked. The shallow ramp is self-locking, so the
// slider stays where it is put; no screw needed.
//
// part = "body"   print upright, base on the bed
// part = "slider" print upside down, flat top on the bed
// part = "both"   plated together for one print job
// Both PETG, no supports. Tie the tube down through the tail slots.

include <params.scad>

part = "both";

wc = tube_flat_w + 0.4;    // channel width: room for the tube flattened
t  = 2.4;                  // wall thickness
H  = 9.5;                  // wall top / slider underside
nose_z = 6.0;              // lowest point of the ridge above the floor datum
lip = 1.2;                 // dovetail lip
c  = slide_clear;
yw = wc / 2 + t;           // wall outer face
base = 2.0;                // base plate thickness below the floor datum
x0 = -8; x_stop = 37; x1 = 44;   // body start, end of ramp, body end
tail = 9;

// floor height along x
fl = [[x0, 0], [4, 0], [12, 3.6], [34, 5.4], [x1, 5.4]];

module body() {
    difference() {
        union() {
            // base plate including the tie-down tails
            translate([x0 - tail, -yw, -base]) cube([x1 - x0 + 2 * tail, 2 * yw, base]);
            // walls
            for (s = [-1, 1]) translate([x0, s > 0 ? wc / 2 : -yw, -base])
                cube([x1 - x0, t, H + base]);
            // dovetail lips with a 45-degree underside
            for (s = [-1, 1]) mirror([0, s > 0 ? 0 : 1, 0])
                translate([x0, 0, 0]) rotate([90, 0, 90])
                    linear_extrude(x1 - x0)
                        polygon([[yw - 0.01, H - 3], [yw + lip, H - 3 + lip],
                                 [yw + lip, H], [yw - 0.01, H]]);
            // ramp floor
            rotate([90, 0, 0]) translate([0, 0, -wc / 2 - 0.01])
                linear_extrude(wc + 0.02)
                    polygon(concat([[x0, -0.01]], fl, [[x1, -0.01]]));
            // exit ramp on the tail, so the tube eases back down to the
            // tie-down level instead of kinking over the end of the floor
            rotate([90, 0, 0]) translate([0, 0, -wc / 2 + 0.6])
                linear_extrude(wc - 1.2)
                    polygon([[x1 - 0.01, -0.01], [x1 - 0.01, 5.4], [x1 + tail - 1, 0.6], [x1 + tail - 1, -0.01]]);
            // stop blocks on the wall tops: the slider plate hits them with
            // its ridge at x = 35, inside the sealed zone
            for (s = [-1, 1]) translate([x_stop + sl_len / 2 - 2, s > 0 ? wc / 2 : -yw, H - 0.01])
                cube([x1 - (x_stop + sl_len / 2 - 2), t, 3]);
        }
        // tie-down slots in the tails, either side of the tube
        for (x = [x0 - tail / 2, x1 + tail / 2], s = [-1, 1])
            translate([x, s * (tube_od / 2 + 2.2), 0])
                cube([ziptie_w, ziptie_t, 3 * base + 2], center = true);
        // arrow on the wall top pointing toward "closed"
        translate([x_stop - 12, yw - t / 2, H - 0.6])
            linear_extrude(1) polygon([[0, -0.8], [6, -0.8], [6, -1.1], [9, 0], [6, 1.1], [6, 0.8], [0, 0.8]] * 0.9);
    }
}

sl_len = 14;
sk = 2.0;                  // skirt thickness
yo = yw + lip + c + sk;    // slider outer half-width

module slider() {
    // modelled in its working position, ridge centre at x = 0
    union() {
        difference() {
            translate([-sl_len / 2, -yo - 0.4, H + c]) cube([sl_len, 2 * yo + 0.8, 3]);
            // thumb grip grooves
            for (x = [-4.5 : 3 : 4.5]) translate([x, 0, H + c + 3])
                rotate([90, 0, 0]) cylinder(d = 1.4, h = 2 * yo + 2, center = true, $fn = 16);
        }
        for (s = [-1, 1]) mirror([0, s > 0 ? 0 : 1, 0])
            translate([-sl_len / 2, 0, 0]) rotate([90, 0, 90]) linear_extrude(sl_len)
                polygon([
                    [yw + lip + c,      H + c + 0.5],
                    [yw + lip + c,      H - 1.8 - c],          // under the lip
                    [yw + c,            H - 3 - c],
                    [yw + c,            H - 3 - c - 1.6],
                    [yo,                H - 3 - c - 1.6],
                    [yo,                H + c + 0.5]]);
        // ridge: rounded nose, flat back up to the plate
        hull() {
            translate([0, 0, nose_z + 2]) rotate([90, 0, 0])
                cylinder(r = 2, h = wc - 2 * c - 0.4, center = true);
            translate([-2, -(wc - 2 * c - 0.4) / 2, H + c]) cube([4, wc - 2 * c - 0.4, 0.01]);
        }
    }
}

if (part == "body") translate([0, 0, base]) body();
else if (part == "slider") translate([0, 0, H + c + 3]) rotate([180, 0, 0]) slider();
else {
    translate([0, 0, base]) body();
    translate([0, 2 * yo + 8, H + c + 3]) rotate([180, 0, 0]) slider();
}
