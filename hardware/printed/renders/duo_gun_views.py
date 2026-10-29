"""Renders of the Duo gun (src/duo_gun.scad), all purple; OpenSCAD --render + Pillow.

    python duo_gun_views.py          writes renders/15_duo_gun_*.png + 15_duo_gun_overview.png
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

OS = r"/path/to/openscad"
D = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
SRC = D.rsplit("/", 1)[0] + "/src/duo_gun.scad"
TMP = os.environ.get("TEMP", D).replace("\\", "/")
FONTB = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 30)
FONT = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 23)


def render(name, body, eye, center, size=(1100, 900), ortho=False):
    scene = f"{TMP}/_duo_{name}.scad"
    with open(scene, "w") as f:
        f.write(f"use <{SRC}>\n{body}\n")
    out = f"{D}/15_duo_gun_{name}.png"
    cmd = [OS, "--backend=manifold", "--render", "-o", out, f"--imgsize={size[0]},{size[1]}",
           "--colorscheme=Tomorrow", "--projection=" + ("ortho" if ortho else "perspective"),
           "--camera=" + ",".join(str(v) for v in (*eye, *center)), scene]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(out):
        print(r.stderr); raise SystemExit(f"render {name} failed")
    print("wrote", out)
    return out


C = (-50, 27.8, -8)          # middle of the whole gun, grip included


def eye(dx, dy, dz, dist=640, c=C):
    n = (dx * dx + dy * dy + dz * dz) ** 0.5
    return tuple(c[i] + v / n * dist for i, v in enumerate((dx, dy, dz)))


TC = (-55, 27.8, -35)        # trigger close-ups: open gun, true side view from the seam side
views = [
    ("hero", 'gun("R");', eye(0.55, -1, 0.4), C, "The right gun, outer side",
     "All purple, R 10 rounds; the trigger sits in a short housing ahead of the grip"),
    ("front", 'gun("L");', eye(1, 0.35, 0.25), C, "Front: the two head windows",
     "Front wall laps 2 mm over each head's stationary rim; 45-degree bevel"),
    ("grip_side", 'gun("L");', eye(0.45, -1, 0.3), C, "Left gun, inner side (faces the right gun)",
     "Grip flush with this face; magnet pockets hold the pair together"),
    ("trigger", 'gun("L", open = true);', (TC[0], 400, TC[2]), TC,
     "Trigger at rest (cover off)", "Its nub rests on the GSW-21's button; it pivots on two 5 mm pegs printed into the halves", True),
    ("pulled", 'gun("L", open = true, a = 23.77);', (TC[0], 400, TC[2]), TC,
     "Trigger at full pull", "Pushes the button 7.0 mm (it latches at 5), then lands on the stop boss on the grip", True),
    ("open", 'gun("L", open = true);', eye(0.25, 1, 0.35, 600), C, "Cover off: the build",
     "Heads in half-sleeves with crush ribs, dock outlets pointing up, switch on its bulkhead, grip built in"),
    ("pair", 'gun("L"); translate([0, -55.8, 0]) gun("R");', eye(0.8, -0.35, -0.5, 720, (-50, 0, -8)), (-50, 0, -8),
     "A pair in one hand", "Switch both on, then hold them grip to grip: one 56 mm handle"),
    ("rear", 'gun("L");', eye(-1, -0.55, 0.15, 520), (-80, 20, 25), "Back: the umbilical dock, built into the main half",
     "Hose socket (angled 45 deg), XT30U window, carabiner bar between two openings"),
]

shots = []
for v in views:
    name, body, cam, center, title, sub = v[:6]
    shots.append((render(name, body, cam, center, ortho=len(v) > 6), title, sub))

# print layout: one left gun, three parts, halves outer face down
layout = ('color("#cdb4f0") main_print() main_half();'
          ' translate([0, 215, 0]) color("#d9c6f6") cover_print() cover_half();'
          ' color("#cdb4f0") translate([110, 40, 0]) trigger_print();')
shots.append((render("print", layout, (0, -330, 760), (0, 105, 0)), "Print layout (one gun): three parts",
              "Main half with the grip, cover half, trigger. Outer faces down, no supports"))


def sheet(shots, out):
    W1, H1 = 1100, 900
    cols, pad, head = 2, 16, 92
    rows = (len(shots) + cols - 1) // cols
    img = Image.new("RGB", (cols * W1 + (cols + 1) * pad, rows * (H1 + head) + (rows + 1) * pad), "white")
    dr = ImageDraw.Draw(img)
    for i, (path, title, sub) in enumerate(shots):
        r, c = divmod(i, cols)
        x = pad + c * (W1 + pad); y = pad + r * (H1 + head + pad)
        dr.text((x + 6, y + 2), title, font=FONTB, fill=(60, 40, 90))
        dr.text((x + 6, y + 46), sub, font=FONT, fill=(90, 90, 105))
        img.paste(Image.open(path).convert("RGB"), (x, y + head))
    img.save(out)
    print("wrote", out)


sheet(shots, f"{D}/15_duo_gun_overview.png")
