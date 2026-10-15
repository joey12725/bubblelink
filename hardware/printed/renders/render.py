"""Annotated OpenSCAD renders of the BubbleLink stick.

Each view: an OpenSCAD preview render with a fixed orthographic camera, an
affine 3D->pixel map fitted from marker renders with the same camera, and
labels + arrows drawn with Pillow in side margins.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OS = r"/path/to/openscad"
D = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
SRC = "bubblelink/hardware/printed/src/stick.scad"
OUT = os.environ.get("REND_OUT", D)
W, H = 1300, 1450          # OpenSCAD render size
MARGIN = 540               # label margin each side
FONT = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 25)
FONTB = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 25)
TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 40)
SUB = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 26)


def run_scad(body, cam, out):
    path = f"{D}/_scene.scad"
    with open(path, "w") as f:
        f.write(f'use <{SRC}>\n$fn = 48;\n{body}\n')
    cmd = [OS, "--camera=" + ",".join(str(c) for c in cam), "--projection=ortho",
           f"--imgsize={W},{H}", "--colorscheme=Tomorrow", "-o", out, path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(out):
        print(r.stderr); raise SystemExit("render failed")


def calibrate(cam):
    """Fit pixel = A @ [x, y, z, 1] from marker renders around the view centre."""
    c = cam[3:6]
    k = 0.065 * float(np.linalg.norm(np.array(cam[:3]) - np.array(c))) / 40   # keep markers on screen
    pts = [(c[0] + a * k, c[1] + b * k, c[2] + e * k) for a, b, e in
           [(0, 0, 0), (40, 0, 0), (0, 40, 0), (0, 0, 40), (-25, 15, -30)]]
    px = []
    for i, p in enumerate(pts):
        f = f"{D}/_m{i}.png"
        run_scad(f'color("black") translate([{p[0]},{p[1]},{p[2]}]) sphere(r = {max(0.6, 2.5 * k)});', cam, f)
        a = np.asarray(Image.open(f).convert("L"), dtype=float)
        ys, xs = np.nonzero(a < 90)
        px.append((xs.mean(), ys.mean()))
    P = np.array([list(p) + [1] for p in pts], dtype=float)
    A, _res, *_ = np.linalg.lstsq(P, np.array(px), rcond=None)
    err = np.abs(P @ A - np.array(px)).max()
    assert err < 2.0, f"calibration error {err:.2f} px"
    return lambda q: tuple((np.array(list(q) + [1.0]) @ A).tolist())


def arrow(dr, a, b, color):
    dr.line([a, b], fill=color, width=3)
    v = np.array(b) - np.array(a); n = np.linalg.norm(v)
    if n < 1: return
    v /= n; w = np.array([-v[1], v[0]])
    tip = np.array(b)
    dr.polygon([tuple(tip), tuple(tip - 16 * v + 7 * w), tuple(tip - 16 * v - 7 * w)], fill=color)
    dr.ellipse([b[0] - 1, b[1] - 1, b[0] + 1, b[1] + 1], fill=color)


BOXW = MARGIN - 54 - 24


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width: cur = trial
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def place(labels, proj, top, bottom):
    """labels: (side, 3d anchor, title, detail). Returns layout per side."""
    out = []
    for side in ("L", "R"):
        items = []
        for s_, a, t, d in labels:
            p = proj(a)
            auto = "L" if p[0] < MARGIN + W / 2 else "R"
            if auto != side: continue
            tl = wrap(t, FONTB, BOXW); dl = wrap(d, FONT, BOXW) if d else []
            items.append((p[1], p, tl, dl))
        items.sort(key=lambda it: it[0])
        hs = [12 + 31 * (len(tl) + len(dl)) for _, _, tl, dl in items]
        ys, y = [], top
        for (ay, *_), h in zip(items, hs):
            y = max(y, ay - h / 2); ys.append(y); y += h + 14
        if y - 14 > bottom:
            for i in range(len(ys) - 1, -1, -1):
                ys[i] = min(ys[i], bottom - sum(hs[i:]) - 14 * (len(hs) - 1 - i))
        for (ay, p, tl, dl), y, h in zip(items, ys, hs):
            out.append((side, p, tl, dl, y, h))
    return out


def dashed(dr, a, b, color, on=11, off=7):
    a = np.array(a, float); b = np.array(b, float); n = np.linalg.norm(b - a)
    if n < 1: return
    v = (b - a) / n; s = 0.0
    while s < n:
        e = min(s + on, n)
        dr.line([tuple(a + v * s), tuple(a + v * e)], fill=color, width=3)
        s = e + off


def box_edges(lo, hi):
    xs, ys, zs = (lo[0], hi[0]), (lo[1], hi[1]), (lo[2], hi[2])
    pts = [(x, y, z) for x in xs for y in ys for z in zs]
    return [(p, q) for i, p in enumerate(pts) for q in pts[i + 1:]
            if sum(1 for k in range(3) if p[k] != q[k]) == 1]


def view(name, body, cam, labels, title, subtitle, outlines=()):
    img = f"{D}/_{name}.png"
    run_scad(body, cam, img)
    proj = calibrate(cam)
    base = Image.open(img).convert("RGB")
    cw = W + 2 * MARGIN
    canvas = Image.new("RGB", (cw, H + 110), "white")
    canvas.paste(base, (MARGIN, 110))
    dr = ImageDraw.Draw(canvas)
    dr.text((30, 18), title, font=TITLE, fill=(25, 35, 50))
    dr.text((30, 66), subtitle, font=SUB, fill=(90, 100, 115))
    sproj = lambda q: (lambda p: (p[0] + MARGIN, p[1] + 110))(proj(q))
    col = (200, 60, 30)
    for edges in outlines:
        for a, b in edges: dashed(dr, sproj(a), sproj(b), (40, 95, 210))
    for side, p, tl, dl, y, h in place(labels, sproj, 130, H + 90):
        bx0 = 24 if side == "L" else cw - MARGIN + 30
        bx1 = MARGIN - 30 if side == "L" else cw - 24
        dr.rounded_rectangle([bx0, y, bx1, y + h], radius=8, fill=(255, 248, 240), outline=col, width=2)
        ty = y + 5
        for ln in tl: dr.text((bx0 + 12, ty), ln, font=FONTB, fill=(30, 30, 30)); ty += 31
        for ln in dl: dr.text((bx0 + 12, ty), ln, font=FONT, fill=(70, 70, 70)); ty += 31
        start = (bx1, y + h / 2) if side == "L" else (bx0, y + h / 2)
        arrow(dr, start, p, col)
    canvas.save(f"{OUT}/{name}.png")
    print("wrote", f"{OUT}/{name}.png")
    return proj
