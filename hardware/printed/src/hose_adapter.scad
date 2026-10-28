// Straight barbed reducer: bladder drinking tube -> 3.5 x 5.5 mm silicone (the IN pigtail).
//
// Big barb: the UWWWMM bladder's 101 cm TPU drinking tube. Its ID wasn't listed; Joey's
// test fits (2026-10-27) with the car-hose assortment: a 6.3 mm barb just touches the
// walls (leaks), a 9.5 mm barb goes on but is too tight. So the tube ID is about 6.3-6.5
// and big_peak defaults to 8.5 (about 1/3 stretch). 8.0 and 9.0 builds are alternates.
// Small barb: the ordered 3.5 ID x 5.5 OD silicone. 4.8 mm peak, the same as the
// assortment's 3/16" barbs that Joey found fit it.
//
// Printed upright, big barb's tip on the bed (use a brim: the footprint is a 6 mm ring).
// The big ridges' sharp steps face up and the small ridges have 45-degree backs, so
// nothing overhangs past 45 degrees. Notches on the collar edge mark the size:
// 1 = 8.0, 2 = 8.5, 3 = 9.0. Zip-tie both ends. ASA or PETG, 100% infill.
// Units: millimetres (STL and 3MF).

big_peak   = 8.5;                     // big barb ridge OD
big_tip    = 6.0;                     // lead-in, under the tube ID
big_valley = min(7.0, big_peak - 1.2);
big_bore   = 4.5;
big_ridge  = 3.5;                     // cone length per ridge
big_n      = 3;
big_shank  = 1.5;                     // plain length below the collar (zip tie sits on a ridge valley)

sm_peak    = 4.8;
sm_tip     = 3.4;                     // under the 3.5 ID
sm_valley  = 4.0;
sm_bore    = 2.2;
sm_ridge   = 2.5;
sm_n       = 3;
sm_shank   = 1.0;

collar_d   = 12;
collar_h   = 2.0;                     // straight part, above a 45-degree chamfer from the big shank

$fn = 96;

notches = big_peak < 8.25 ? 1 : big_peak < 8.75 ? 2 : 3;

// outer profile, bottom (big tip) to top (small tip), as [r, z]
function outer() = let(
    zb  = big_n * big_ridge,
    big = [for (i = [0 : big_n - 1]) each [
              [(i == 0 ? big_tip : big_valley) / 2, i * big_ridge],
              [big_peak / 2, (i + 1) * big_ridge]]],
    zc0 = zb + big_shank,
    ch  = (collar_d - big_valley) / 2,
    zc1 = zc0 + ch + collar_h,
    zs  = zc1 + sm_shank,
    bk  = (sm_peak - sm_valley) / 2,          // 45-degree back of each small ridge
    sm  = [for (i = [0 : sm_n - 1]) let(z0 = zs + i * (bk + sm_ridge)) each [
              [sm_valley / 2, z0],
              [sm_peak / 2, z0 + bk],
              [(i == sm_n - 1 ? sm_tip : sm_valley) / 2, z0 + bk + sm_ridge]]])
    concat(big,
           [[big_valley / 2, zb], [big_valley / 2, zc0],
            [collar_d / 2, zc0 + ch], [collar_d / 2, zc1], [sm_valley / 2, zc1]],
           sm);

function height() = let(o = outer()) o[len(o) - 1][1];

module adapter() {
    o = outer();
    H = height();
    zc0 = big_n * big_ridge + big_shank;
    difference() {
        rotate_extrude() polygon(concat([[0, 0]], o, [[0, H]]));
        // bore: big, 45-degree neck at the collar, small
        rotate_extrude() polygon([
            [0, -1], [big_bore / 2, -1], [big_bore / 2, zc0],
            [sm_bore / 2, zc0 + (big_bore - sm_bore) / 2], [sm_bore / 2, H + 1], [0, H + 1]]);
        // size notches in the collar rim
        for (i = [0 : notches - 1]) rotate(i * 25)
            translate([collar_d / 2, 0, zc0]) cylinder(h = 20, d = 1.6, $fn = 4);
    }
}

adapter();
