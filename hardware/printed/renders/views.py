import sys
import render as R
from render import box_edges

Wi, Di, t, Zt, tp = 94, 73, 2.4, 156, 3
TOP = Zt + tp
PCBZ = Zt - 22                      # PCB component face
TUBE, CAP, SLED, CUP, TPU = '"#c5d3de"', '"#6f9fbd"', '"#e3a453"', '"#9aa7b2"', '"#2b2b2b"'
C = (47, 36.5, 52)
GROM = f'color({TPU}) translate([47, 58.5, -4.2]) cube([34, 11, 1.2]);'


def cam(center, d=(350, 445, 276)):
    return [center[0] + d[0], center[1] + d[1], center[2] + d[2], *center]


def pxy(p):  # PCB board coords -> stick coords (board rotated 90 deg)
    return (70 - p[1], 36.5 + p[0])


only = sys.argv[1:]
want = lambda n: not only or n in only
DOT = "·"
INK = f'color("#16212b") translate([0, 0, {TOP} - 0.6]) linear_extrude(0.59) cap_labels();'

if want("1"):
    R.view("1_assembled",
           f'color({TUBE}) tube(); color("#6e8aa0") emboss(); color({CAP}) cap(); color({CUP}) translate([0,0,-56]) cup(); color({TPU}) installed_tpu(); ' + INK,
           cam(C),
           [("L", (Wi + t + 0.8, 36.5, 110), "Raised BubbleLink lettering", "0.8 mm tall, on the outer wall, reads upward"),
            ("L", (Wi + t, 62, 40), "Solid side wall (no openings)", "the breaker sits just behind it; reset = cap off, sled out"),
            ("L", (Wi + t, 20, 112), "Dry tube", "battery + electronics on a slide-out sled"),
            ("L", (Wi + t, 4, -4), "Cup-to-tube joint", "4x M3x12, driven up from underneath"),
            ("L", (Wi + t, 20, -30), "Wet cup", "pump, 3 tees, check valve, bypass clamp"),
            ("L", (Wi + t, 13, -39), "Paracord tie-offs 1 and 2", "a hole pair per umbilical; the cord takes a dropped gun's pull (view 9)"),
            ("R", (75, 60, TOP), "Control head (cap)", "voltmeter, USB-C, LEDs, PRIME: see view 2"),
            ("R", (49, Di + t + 1, Zt - 5.2), "Cap screw (front + back)", "M3x10 socket head, steel flat washer over a TPU washer"),
            ("R", (60, Di + t, -56), "Underneath: everything exits here", "2 umbilicals, bladder feed, backpack USB, and the XT60H loop (unplug it = OFF)")],
           f"1 {DOT} Fully assembled",
           "Body about 100 x 78 x 220 mm (3.9 x 3.1 x 8.7 in); 87 mm deep across the two cap screw heads. Stands upright beside the bladder; the hidden back faces your back.")

if want("2"):
    R.view("2_cap_top",
           f'color({CAP}) cap(); color({TPU}) translate([{pxy((14.7, 12.4))[0]}, {pxy((14.7, 12.4))[1]}, {Zt + tp}]) boot(); color({CAP}) translate([{pxy((14.7, 12.4))[0]}, {pxy((14.7, 12.4))[1]}, {Zt + tp}]) bezel(); color({TPU}) translate([59.9, 33.505, {Zt + tp}]) trimplug(); color({TPU}) translate([23, 55, {Zt + tp}]) usbplug(); ' + INK,
           [47, 36.5 + 60, TOP + 350, 47, 36.5, TOP],
           [("L", (21, 28, TOP), "Voltmeter (29 mm hole)", "battery voltage; the body hangs ~1 in below"),
            ("L", (23, 55, TOP + 1), "USB-C port with its TPU plug", "pull the tab to charge; the charger sits in a pocket underneath"),
            ("L", (47, Di + t, TOP), "FRONT edge", "faces away from you"),
            ("L", (47, -t, TOP), "BACK edge", "against your back"),
            ("R", pxy((0, 16.7)) + (TOP,), "Status LED windows: PWR / GUN / PUMP", "through-holes; fill with clear hot glue or UV resin"),
            ("R", pxy((14.7, 12.4)) + (TOP + 4,), "PRIME button (guarded)", "the rim sits 1 mm above the boot; press with a fingertip (view 8)"),
            ("R", (59.9, 27.8, TOP + 1.2), "THR + DLY plug (one TPU piece)", "closes both trimmer windows; pull the tab to reach RV1 (threshold) and RV2 (delay)")],
           f"2 {DOT} Cap top (the control panel)",
           "Looking down from the front. Engraved labels drawn paint-filled (rub in acrylic or a paint pen). The PCB hangs under the LED/PRIME area.")

if want("3"):
    cut = (f'difference() {{ tube(); translate([{Wi - 0.6}, -20, 0.01]) cube([30, 140, 200]); '
           f'translate([-20, {Di - 0.6}, 0.01]) cube([150, 30, 200]); }}')
    R.view("3_cap_off_front_cutaway",
           f'color({TUBE}) {cut}; color({SLED}) sled(); color({CUP}) translate([0,0,-56]) cup(); {GROM}',
           cam(C),
           [("L", (20, 40, 115.65), "What holds the sled down", "the cap's TPU pads press the battery, which clamps the sled base onto the bulkhead"),
            ("L", (43, 66.9, 108), "Spine", "zip-tie slots; lead channels at both ends"),
            ("L", (5, 63.2, 1.0), "Corner bosses (x4) locate the sled", "the base hugs each boss with 0.3 mm clearance, so it can't slide or twist"),
            ("L", (64, 64, 0), "Bulkhead cable grommet", "every cable drops into the cup through here"),
            ("L", (30, 72, -30), "Wet cup (drains)", ""),
            ("R", (20, 72.5, 60), "Battery bay (2S5P block stands here)", "cells front-to-back, TERM face to the back"),
            ("R", (70, 55.9, 96), "Cross panel", "breaker + BMS behind it (view 4)"),
            ("R", (55.5, 59.9, 62), "ACS758 compartment", "current sensor"),
            ("R", (54.5, 59.9, 21), "Buck A compartment", "5 V to the PCB (J1)"),
            ("R", (74.7, 59.9, 21), "Buck B compartment", "5 V to the LED backpack"),
            ("R", (89.5, 55.9, 30), "Wire pass", "to the breaker / BMS side")],
           f"3 {DOT} Cap off: front of the sled (front and side walls cut away)",
           "The sled lifts straight out of the top. It takes no screws: bosses stop it sliding, the cap clamps it down. Dashed blue = battery.",
           outlines=[box_edges((0.5, 2.65, 2.5), (41.33, 72.5, 115.65))])

if want("4"):
    cut = (f'difference() {{ tube(); translate([{Wi - 0.6}, -20, 0.01]) cube([30, 140, 200]); '
           f'translate([-20, -30, 0.01]) cube([150, 30.6, 200]); }}')
    R.view("4_cap_off_back_cutaway",
           f'color({TUBE}) {cut}; color({SLED}) sled(); color({CUP}) translate([0,0,-56]) cup();',
           cam((47, 36.5, 60), (370, -470, 290)),
           [("L", (44.4, 46.8, 55), "Breaker tie slots (x2)", "one zip tie through each plate hole"),
            ("L", (43, 25, 104), "Spine wire pass-throughs", ""),
            ("L", (43, 3, 60), "Lead channel behind the spine", "battery leads straight into the BMS"),
            ("R", (80, 9.9, 92), "Breaker hangs here", "upright; reset it with the cap off and the sled out"),
            ("R", (70, 52.9, 80), "Cross panel (back face)", ""),
            ("R", (89.5, 52.9, 25), "Wire pass to the front", ""),
            ("R", (70, 4.8, 40), "BMS slot", "card stands on edge between two lips, against the back wall")],
           f"4 {DOT} Cap off: back of the sled (back and side walls cut away)",
           "Dashed blue = where the breaker and BMS sit, behind the cross panel. Both are held with zip ties, not screws.",
           outlines=[box_edges((50, 9.9, 4), (92, 51.9, 106)), box_edges((45, 1.6, 2.5), (93, 8.0, 66))])

if want("5"):
    f = lambda p: (p[0], Di - p[1], Zt + tp - p[2])     # flipped cap coordinates
    capb = f'translate([0, {Di}, {Zt + tp}]) rotate([180, 0, 0])'
    R.view("5_cap_underside",
           f'color({CAP}) {capb} cap(); color({TPU}) {capb} translate([0,0,{Zt - 12 + 2 + 0.4}]) ring(); color({TPU}) {capb} for (y = [7.65, 67.5]) translate([3.7, y - 1.35, 115.05]) batpad();',
           cam((47, 36.5, 14), (170, 215, 230)),
           [("L", f((20, 67.5, 118)), "Battery hold-down ribs (x2)", "a TPU pad slips over each rib end"),
            ("L", f(pxy((21.5, 16.5)) + (PCBZ,)), "PCB posts (x4)", "the CTRL board heat-stakes onto the pins"),
            ("L", f((50, 36.5, PCBZ)), "CTRL PCB hangs here (dashed)", "component side toward the plate"),
            ("L", f((21, 28, Zt)), "Voltmeter drops in here", "glue around the bezel on top"),
            ("L", f((23, 55 + 6.4, Zt - 15)), "USB-C charger pocket", "board slides in, receptacle up against the CHG window"),
            ("R", f(pxy((0, 16.7)) + (PCBZ + 6.3,)), "LED light tunnels", "open through the cap; no extra lights needed"),
            ("R", f(pxy((14.7, 12.4)) + (Zt - 8,)), "PRIME plunger sleeve", ""),
            ("R", f((Wi + 0.25, 40, Zt - 8.7)), "TPU seal ring in its groove", "seals against the inside of the tube"),
            ("R", f((49, 7, Zt - 12)), "Nut slots (front + back)", "M3 nuts glued in")],
           f"5 {DOT} Cap underside (flipped over)",
           "The PCB, voltmeter and charger all hang from the cap, so they lift out with it. Leave slack in their wires.",
           outlines=[[(f(a), f(b)) for a, b in box_edges((50, 11.5, PCBZ - 1.6), (90, 61.5, PCBZ))]])

if want("6"):
    z = -53
    R.view("6_cup_interior",
           f'color({CUP}) translate([0,0,-56]) cup(); color({TPU}) translate([10.2, 13.7, -53]) pumpmat();',
           cam((47, 36.5, -35), (-110, 150, 430)),
           [("L", (56, 52, z + 2), "Pump pocket (52 x 46 mm)", "the G528 sits on a 2 mm TPU mat"),
            ("L", (22, 9.5, z), "Pump strap slots", "zip ties over the pump"),
            ("L", (40, 36.5, z + 2), "Floor drains (8, under the pump)", "plus the same 2 flush-with-floor holes centred on every wall"),
            ("L", (89, 5, -3), "Screw columns (x4)", "M3x12 driven up from below"),
            ("R", (72, 12, z), "Umbilical exit 1 (13 mm)", ""),
            ("R", (72, 32, z), "Umbilical exit 2 (13 mm)", ""),
            ("R", (79, 56, z), "Service hole (20 mm)", "bladder feed, backpack USB, XT60H loop"),
            ("R", (88, 32, z), "Fittings strip + tie slots", "3 tees, check valve, bypass clamp"),
            ("R", (Wi, 31, z + 14), "Paracord tie-offs 1 and 2", "the pack-end brick's cord loops through a pair (view 9)")],
           f"6 {DOT} Cup off: inside the wet chamber",
           "Everything wet lives here. It drains through the floor, and the cup comes off from below.")

if want("7"):
    R.view("7_bulkhead_underside",
           f'color({TUBE}) tube(); color({TPU}) translate([47, 58.3, -3 - 0.8 - 1.2]) grommet_half(0.8); color({CAP}) translate([47, 58.3, -3]) mirror([0,0,1]) skirt();',
           [47 + 300, 36.5 + 380, -3 - 380, 47, 36.5, 60],
           [("L", (47 + 19.6, 58.3, -11.8), "Drip skirt (ASA) around the grommet", "water dripping along the bulkhead falls off its edge"),
            ("L", (5, 68, -3), "Cup screw holes (x4)", "the M3 nuts sit above, glued in from the dry side"),
            ("R", (60, 30, -3), "Bulkhead", "the dry/wet divider; floor of the tube"),
            ("R", (52, 58.3, -5.0), "Cable grommet (2-piece TPU)", "slit it; fill the top with silicone once wired")],
           f"7 {DOT} Bulkhead from below (cup removed)",
           "The only path between dry and wet is the cable grommet. The side walls are solid.")

if want("8"):
    sx, sy = pxy((14.7, 12.4))
    body = (f'intersection() {{ union() {{ color({CAP}) cap(); '
            f'color({TPU}) translate([{sx}, {sy}, {Zt + tp}]) boot(); '
            f'color({CAP}) translate([{sx}, {sy}, {Zt + tp}]) bezel(); '
            f'color("#d9534f") translate([{sx}, {sy}, {Zt + tp + 0.75 + 1.2}]) mirror([0,0,1]) plunger(); '
            f'color("green") translate([{sx - 14}, {sy - 22}, {PCBZ - 1.6}]) cube([28, 30, 1.6]); '
            f'color("#444") translate([{sx - 3}, {sy - 3}, {PCBZ}]) cube([6, 6, 3.5]); '
            f'color("#444") translate([{sx}, {sy}, {PCBZ}]) cylinder(d = 3.5, h = 4.3); }} '
            f'translate([-50, -50, 0]) cube([{sx} + 50, 200, 300]); }}')
    R.view("8_prime_section",
           body,
           [sx + 160, sy - 25, 150, sx, sy - 2, 146],
           [("L", (sx, sy, Zt + tp + 4.2), "TPU boot", "its flange is clamped under the bezel, not just glued"),
            ("L", (sx, sy + 9.5, Zt + tp + 4), "ASA guard bezel", "glued to the cap (ASA to ASA); rim 1 mm above the boot"),
            ("L", (sx, sy, Zt + tp + 1.2), "Hard stop", "the plunger head bottoms on the cap after 0.75 mm"),
            ("R", (sx, sy, Zt - 4), "TPU plunger in its sleeve", "soft, so a hard press can't load the PCB much"),
            ("R", (sx, sy, PCBZ + 4.3), "SW1 (PRIME switch)", "clicks after ~0.55 mm of travel"),
            ("R", (sx, sy - 15, PCBZ - 0.8), "CTRL PCB", "component side up, hanging from the cap"),
            ("R", (sx, sy + 6.6, Zt + 1.5), "Cap plate", "")],
           f"8 {DOT} PRIME button, cut in half",
           "Section through the button. The switch and board are simple placeholders.")

if want("9"):
    cutT = (f'difference() {{ tube(); translate([{Wi - 0.6}, -20, 0.01]) cube([30, 140, 200]); '
            f'translate([-20, {Di - 0.6}, 0.01]) cube([150, 30, 200]); translate([-20, -20, 92]) cube([150, 150, 100]); }}')
    cutC = f'difference() {{ translate([0,0,-56]) cup(); translate([-20, {Di - 0.6}, -60]) cube([150, 30, 70]); }}'
    tz = -56 + 3 + 14                  # paracord tie-off height (cup tf + 14)
    RED, ORA, YEL = (214, 40, 40), (240, 140, 20), (215, 180, 0)
    xo = Wi + t + 1.5
    g1 = [(53, 58, 40), (54, 61, 30), (54, 61, 3), (54, 61, -8), (70, 16, -44), (72, 12, -56), (72, 12, -80)]
    g2 = [(60, 58, 40), (63.5, 61, 30), (63.5, 61, 3), (63.5, 61, -8), (71, 34, -44), (72, 32, -56), (72, 32, -80)]
    c1 = [(80, 9, -80), (xo, 13, tz - 3), (xo, 13, tz), (xo, 25, tz), (xo, 25, tz - 3), (80, 15, -80)]
    c2 = [(80, 29, -80), (xo, 31, tz - 3), (xo, 31, tz), (xo, 43, tz), (xo, 43, tz - 3), (80, 35, -80)]
    R.view("9_gun_power_and_paracord",
           f'color({TUBE}) {cutT}; color({SLED}) sled(); color({CUP}) {cutC}; {GROM} '
           f'color("cyan", 0.5) ghost(6);',
           cam((58, 36.5, -8), (300, 380, 236)),
           [("L", (57, 58, 60), "ACS758 (current sensor)", "battery + > breaker > ACS758, then it splits into the two gun channels"),
            ("L", (60, 61, 1), "Cable grommet", "both 16 AWG gun pairs cross the bulkhead here"),
            ("L", (70, 16, -44), "Gun 1 power (red), gun 2 power (orange)", "16 AWG pairs: + from the ACS758 split, - from BMS P-. Gun current never touches the PCB"),
            ("L", (72, 32, -56), "Exits 1 and 2 (13 mm)", "numbers engraved on the underside"),
            ("L", (72, 30, -85), "Pack-end umbilical bricks", "XT30U disconnect strapped in each; hose, 16 AWG pair and cord go on to the gun"),
            ("R", (xo, 19, tz), "Paracord tie-off 1 (yellow)", "in one hole, out the other, around the 7 mm web; knot and melt the ends"),
            ("R", (xo, 37, tz), "Paracord tie-off 2", "the same, beside exit 2; '1' and '2' are engraved above the pairs")],
           f"9 {DOT} Gun power and paracord routing",
           "Front and outer walls cut away, top of the tube hidden. Lines show routes; hoses not drawn. The cord goes tight before the wires or hose.",
           outlines=[box_edges((64, 4, -92), (82, 18, -80)), box_edges((64, 26, -92), (82, 40, -80))],
           paths=[(RED, g1), (ORA, g2), (YEL, c1), (YEL, c2)])
