// Pump module: one plate that carries the whole wet-side manifold. It
// replaces the separate pump cradle, the restrictor mount, and the tee and
// check-valve holders.
//
//   - G528 motor rests in two 90-degree V-blocks, strapped down with zip
//     ties. A V seats any motor from ~20 to ~40 mm diameter, so the cradle
//     doesn't depend on unmeasured pump dimensions. The pump head overhangs
//     the -x end of the plate; push its back face against the stop wall.
//   - Manifold field: pairs of zip-tie slots sized for three assortment
//     tees, the 4 mm check valve, and one slide clamp (the bypass restrictor):
//         inlet tee -> pump -> outlet tee 1 -> outlet tee 2 -> gun 1 / gun 2
//                                  \-> slide clamp -> check valve -> inlet tee
//   - Four 5 mm holes for paracord or zip ties into the bag.
//   - Drain holes so nothing pools on the plate.
// A strip of foam under the motor (between the V-blocks) damps vibration.
//
// Print flat, PETG, no supports.

include <params.scad>

motor_d_max = 40;     // largest motor the V-blocks accept
motor_len   = 28;     // [ESTIMATE] motor can length; sets V-block spacing.
                      // Third-party spec: whole pump ~60 x 60 x 50 mm, 69 g.

Lp = 166; Wp = 66; Tp = 3;
v_w = 8;                            // V-block thickness along x
v_x = [0, motor_len - v_w];         // first block doubles as the head stop
v_h = motor_d_max / 2 + 2;          // V-block height above the plate
mot_y = 27;                         // motor axis y

module vblock(x) {
    translate([x, mot_y, 0]) difference() {
        translate([0, -(motor_d_max / 2 + 6), 0]) cube([v_w, motor_d_max + 12, v_h + Tp]);
        // 90-degree V, apex 3 mm above the plate; local (u,v,w) -> (y,z,x)
        translate([-1, 0, Tp + 3]) rotate([90, 0, 90]) linear_extrude(v_w + 2)
            polygon([[0, 0], [60, 60], [-60, 60]]);
    }
}

module tie_pair(x, y, span) {
    // two slots either side of a fitting; the strap passes over it
    for (s = [-1, 1]) translate([x, y + s * span / 2, Tp / 2])
        cube([ziptie_w, ziptie_t, Tp + 2], center = true);
}

mx = v_x[1] + v_w + 12;   // start of the manifold field
lane_a = 12;              // tees and check valve
lane_b = 52;              // slide clamp (bypass restrictor)

difference() {
    union() {
        hull() for (sx = [0, 1], sy = [0, 1])
            translate([4 + sx * (Lp - 8), 4 + sy * (Wp - 8), 0]) cylinder(r = 4, h = Tp);
        for (x = v_x) vblock(x);
    }
    // straps over the motor, between the V-blocks
    tie_pair(v_x[0] + v_w + 2.5, mot_y, motor_d_max + 8);
    tie_pair(v_x[1] - 2.5, mot_y, motor_d_max + 8);   // stays on a short can
    // lane A: inlet tee, two outlet tees, check valve. The outlet side has
    // four connections (pump, bypass, gun 1, gun 2), so it takes two tees in
    // series: pump -> tee 1 (bypass branch) -> tee 2 (gun 1 / gun 2).
    for (x = [mx, mx + 14])           tie_pair(x, lane_a, tube_od + 9);   // inlet tee
    for (x = [mx + 30, mx + 44])      tie_pair(x, lane_a, tube_od + 9);   // outlet tee 1 (bypass)
    for (x = [mx + 60, mx + 74])      tie_pair(x, lane_a, tube_od + 9);   // outlet tee 2 (guns)
    for (x = [mx + 90, mx + 106])     tie_pair(x, lane_a, tube_od + 8);   // check valve
    // lane B: slide clamp, matching the slots in its tails (61 mm apart)
    for (x = [mx + 6, mx + 67])       tie_pair(x, lane_b, tube_od + 4.4);
    // anchor holes (the near-left corner is taken by the V-block)
    for (p = [[7, Wp - 7], [34, Wp - 6], [Lp - 7, 7], [Lp - 7, Wp - 7]])
        translate([p[0], p[1], -1]) cylinder(d = 5, h = Tp + 2);
    // drain holes between the lanes
    for (x = [mx + 4 : 16 : Lp - 10]) translate([x, 32, -1]) cylinder(d = 4, h = Tp + 2);
}
