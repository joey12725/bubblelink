"""Duo fit check (src/duo_gun.scad): interference between the two halves, heads, dock,
GSW-21 switch and trigger; the trigger's travel and stops; the switch mount's adjustment
room; and the clearances that matter.

    python check_duo_fit.py        add -v for where each overlap is

Expected: every overlap 0 except "head hoses" (~1 mm3: the hose model brushing the barbs'
bases) and the lines marked
"(should hit)", which prove the stops and the push are real (-v: the full-pull hit should
be the stop boss on the front strap, z about -50..-55, not up at the pivot). The crush ribs just touch
the modelled ring (gap 0); the cover half's sleeves are ~0.8 mm clear. Rerun after any
change to the head model (e.g. gh_y0/gh_y1 in blower_head.scad) or to the switch /
trigger numbers in duo_gun.scad.
Needs trimesh + manifold3d and the portable OpenSCAD below.
"""
import math, os, subprocess, sys
import numpy as np, trimesh, manifold3d as m3

OS = r"/path/to/openscad"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
SRC = HERE + "/src/duo_gun.scad"
BH = HERE + "/src/blower_head.scad"
T = os.environ.get("TEMP", ".").replace("\\", "/")
PUSH = 6.5            # button travel to support (GSW-21 latches at 5 mm, measured)
fw = 3.4              # front wall
mid = 55.6 / 2


def stl(name, body):
    f = f"{T}/_duo_{name}.scad"
    open(f, "w").write(f"use <{SRC}>\nuse <{BH}>\n{body}\n")
    out = f"{T}/_duo_{name}.stl"
    r = subprocess.run([OS, "--backend=manifold", "-o", out, f], capture_output=True, text=True)
    if not os.path.exists(out) or "WARNING: Ignoring unknown" in r.stderr:
        print(r.stderr); raise SystemExit(f"render {name} failed")
    m = trimesh.load(out)
    return m3.Manifold(m3.Mesh(vert_properties=np.asarray(m.vertices, np.float32),
                               tri_verts=np.asarray(m.faces, np.uint32)))


def echo(expr):
    """value of an expression in duo_gun.scad"""
    f = f"{T}/_duo_echo.scad"
    open(f, "w").write(f'include <{SRC}>\necho(v = {expr});\n')
    out = f"{T}/_duo_echo.echo"
    subprocess.run([OS, "-D", 'part="none"', "-o", out, f], capture_output=True, text=True)
    return eval(open(out).read().split("v = ")[1].split("\n")[0])


def box(x0, x1, y0, y1, z0, z1):
    return m3.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def line(n, v, unit="mm"):
    print(f"{n:46s} {v:8.2f} {unit}")


# ---------------------------------------------------------------- trigger kinematics (2D, gun x-z)
P_t, N_c, T_c = (np.array(echo(k)) for k in ("P_t", "N_c", "T_c"))
tr_pull, r_nub = echo("tr_pull"), echo("r_nub")
U = np.array([math.cos(math.radians(45)), -math.sin(math.radians(45))])
V = np.array([math.sin(math.radians(45)), math.cos(math.radians(45))])


def nub(a):
    a = math.radians(a); r = N_c - P_t
    return P_t + np.array([r[0] * math.cos(a) + r[1] * math.sin(a), -r[0] * math.sin(a) + r[1] * math.cos(a)])


def push(a):
    return -(nub(a) - N_c) @ U


a_push = next(a / 100 for a in range(0, 4000) if push(a / 100) >= PUSH)
a_latch = next(a / 100 for a in range(0, 4000) if push(a / 100) >= 5.0)
full = push(tr_pull)
lat = max(abs((nub(a / 10) - T_c) @ V) for a in range(0, int(tr_pull * 10) + 1))
finger = math.radians(tr_pull) * math.hypot(3.3, -20)         # where the finger sits on the blade
print("TRIGGER")
line("pivot to nub (lever, pivot side)", r_nub)
line("full pull (blade meets the stop boss)", tr_pull, "deg")
line("button push at full pull", full)
line("  latch (5 mm) reached at", a_latch, "deg")
line(f"  {PUSH} mm reached at", a_push, "deg")
line("  push left if the switch sits 1 mm further back", full - 1)
line("nub off the button axis, max (cap radius 5.15)", lat)
line("finger travel at the finger curve, about", finger)

A, B = stl("A", "main_half();"), stl("B", "cover_half();")
shell = A + B
sw0, swp, swf = stl("sw0", "switch_asm(0);"), stl("swp", f"switch_asm({PUSH});"), stl("swf", f"switch_asm({full:.3f});")
tr0, trp, trf = stl("tr0", "trigger_asm(0);"), stl("trp", f"trigger_asm({a_push});"), stl("trf", f"trigger_asm({tr_pull});")
trx, trb = stl("trx", f"trigger_asm({tr_pull + 0.5});"), stl("trb", "trigger_asm(-6);")
h0, h1 = stl("h0", "at_head(0) head(inlet = false);"), stl("h1", "at_head(1) head(inlet = false);")
heads = h0 + h1
hm = stl("headsM", "translate([0, 55.6, 0]) mirror([0,1,0]) heads();")   # right gun's heads in the left gun's frame
xt = stl("xt", "xt30_male();")
# head hoses pushed onto the two outlets (5.5 OD, 20 mm straight up before they bend)
hoses = stl("hoses", "head_hose_stubs();")
# switch mount: body backed off (hex nut thicker / backed off), a 5/8" hex nut, the knurled nut 2 mm loose
swback = stl("swback", "sframe() translate([-1.4, -12.45, -7.65]) cube([15.6, 24.9, 15.3]);")
hex58 = stl("hex58", "for (r = [0, 15]) sframe() translate([15.6, 0, 0]) rotate([0, 90, 0]) rotate(r) cylinder(d = 15.875 / cos(30), h = 2.6, $fn = 6);")
knloose = stl("knloose", "sframe() translate([21.2 + 2, 0, 0]) rotate([0, 90, 0]) cylinder(d = 15.2, h = 2.8);")

pairs = [(A, B, "halves (pegs)"),
         (shell, heads, "shell x heads (ribs just touch)"), (shell, hm, "shell x heads (right gun)"),
         (shell, xt, "case x XT30U male in its pocket"), (shell, hoses, "case x head hoses on the outlets"),
         (heads, hoses, "heads x head hoses"), (sw0, xt, "switch x XT30U"),
         (shell, sw0, "case x switch"), (shell, swf, "case x switch (pushed full)"),
         (shell, swback, "case x switch body 1.4 mm further back"),
         (shell, hex58, "case x 5/8\" hex nut (any angle)"), (shell, knloose, "case x knurled nut 2 mm loose"),
         (heads, sw0, "heads x switch"),
         (shell, tr0, "case x trigger (rest)"), (shell, trp, f"case x trigger ({PUSH} mm)"),
         (shell, trf, "case x trigger (full pull)"),
         (shell, trx, "case x trigger 0.5 deg past full (should hit)"),
         (shell, trb, "case x trigger 6 deg forward (should hit)"),
         (sw0, tr0, "switch x trigger (rest)"),
         (swp, trp, f"switch {PUSH} x trigger at {PUSH} (touching)"),
         (sw0, trf, "released switch x full pull (should hit)"),
         (heads, trf, "heads x trigger")]
print("\nINTERFERENCE")
for a, b, n in pairs:
    print(f"{n:46s} {(a ^ b).volume():8.3f} mm3")

print("\nCLEARANCES")
behind = box(-200, -fw - 0.3, -200, 200, -200, 200)      # leave out the front lip the rings rest on
line("head to head", h0.min_gap(h1, 10))
line("heads to main half (0 = ribs touch)", heads.min_gap(A ^ behind, 10))
line("heads to cover half", heads.min_gap(B ^ behind, 10))
line("XT30U male to its pocket", xt.min_gap(shell, 10))
line("head hoses to heads", hoses.min_gap(heads, 10))
line("switch to heads", sw0.min_gap(heads, 10))
line("trigger (rest) to button", tr0.min_gap(sw0, 10))
line("trigger (rest) to case", tr0.min_gap(shell, 10))
line("trigger (full pull) to case", trf.min_gap(shell, 10))
line("trigger (any) to heads", tr0.min_gap(heads, 10))
# the blade's tip at full pull to the grip's front strap below the stop boss (grip beside
# the slot; trigger moved sideways onto it)
g = shell ^ box(-200, 0, 0, mid - 8, -200, -58)
line("blade tip to front strap at full pull", trf.translate([0, -11, 0]).min_gap(g, 30))
# walls left round the switch's pockets (body, nuts; not the cap bore, which runs out to the slot)
pk = stl("pk", "intersection() { sframe() sw_keepout(); sframe() translate([-50, -50, -50]) cube([50 + 26, 100, 100]); }")
out = stl("out", "difference() { translate([-300, -300, -300]) cube(600); outer(); }")
line("thinnest wall round the switch pockets", pk.min_gap(out, 10))
gt = stl("gt", "mirror_seam() for (i = [0, 1]) at_head(i) head_gear_tab(1);")
line("thinnest wall at the gear-tab pockets", gt.min_gap(out, 10))

if "-v" in sys.argv:
    for a, b, n in pairs:
        for p in (a ^ b).decompose():
            if p.volume() < 0.05: continue
            lo, hi = p.bounding_box()[:3], p.bounding_box()[3:]
            print(f"  {n.split(' (')[0]}: vol {p.volume():7.2f}  x {lo[0]:6.1f}..{hi[0]:6.1f}  y {lo[1]:5.1f}..{hi[1]:5.1f}  z {lo[2]:6.1f}..{hi[2]:6.1f}")
