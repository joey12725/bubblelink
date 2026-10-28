"""Printability check for STLs in stl/: watertight, body count, and support-free overhangs.

    python check_stl.py                 every STL
    python check_stl.py 6 51            only files whose names start with these prefixes

Assumes each STL is exported in its print orientation (bed at the lowest Z). Flags any
downward-facing surface steeper than 45 degrees that isn't on the bed. A flagged
ceiling has to become a 45-degree roof or a teardrop. Short bridges (slots, nut pockets)
and ring-shaped ledges get flagged too: read the printed location before acting on one.
Needs trimesh + numpy.
"""
import glob, os, sys
import numpy as np
import trimesh

LIMIT = 46          # degrees from vertical; designed 45-degree faces pass with a little slack
here = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(here, "stl", "*.stl")))
if len(sys.argv) > 1:
    files = [f for f in files if os.path.basename(f).startswith(tuple(sys.argv[1:]))]

bad_files = 0
for f in files:
    m = trimesh.load_mesh(f)
    n = m.face_normals
    off_bed = m.triangles[:, :, 2].min(1) > m.bounds[0][2] + 0.05
    over = (n[:, 2] < -np.sin(np.radians(LIMIT))) & off_bed
    area = m.area_faces[over].sum()
    ok = m.is_watertight and area < 0.01
    bad_files += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {os.path.basename(f):32s} watertight={m.is_watertight} "
          f"bodies={len(m.split(only_watertight=False))} overhang>{LIMIT - 1}deg={area:.2f} mm2")
    if area >= 0.01:
        for p in m.submesh([np.where(over)[0]], append=True).split(only_watertight=False):
            lo, hi = p.bounds
            print(f"       at x {lo[0]:.1f}..{hi[0]:.1f}  y {lo[1]:.1f}..{hi[1]:.1f}  z {lo[2]:.2f}  ({p.area:.2f} mm2)")
sys.exit(1 if bad_files else 0)
