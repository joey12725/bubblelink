"""Printability check for STLs in stl/: watertight, body count, and support-free overhangs.

    python check_stl.py                 every STL
    python check_stl.py 6 51            only files whose names start with these prefixes

Assumes each STL is exported in its print orientation (bed at the lowest Z). Flags any
downward-facing surface steeper than 45 degrees that isn't on the bed. A flagged
ceiling has to become a 45-degree roof or a teardrop. Short bridges (slots, nut pockets)
and ring-shaped ledges get flagged too: read the printed location before acting on one.
Multi-colour parts: an inlay file named <part>__<colour>.stl is merged (boolean union) with
<part>.stl before the check, since they print as one object (flagged patches under 0.1 mm2
on such a merge are boolean seams and are ignored).
Needs trimesh + numpy (+ manifold3d for the merge).
"""
import glob, os, sys
import numpy as np
import trimesh

LIMIT = 46          # degrees from vertical; designed 45-degree faces pass with a little slack
here = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(os.path.join(here, "stl", "*.stl")))
if len(sys.argv) > 1:
    files = [f for f in files if os.path.basename(f).startswith(tuple(sys.argv[1:]))]

def merged(f):
    """the part plus any <part>__<colour>.stl inlays, as one solid"""
    base = f[:-4]
    inlays = sorted(glob.glob(base + "__*.stl"))
    m = trimesh.load_mesh(f)
    if not inlays:
        return m, ""
    import manifold3d as m3
    def man(t):
        return m3.Manifold(m3.Mesh(vert_properties=np.asarray(t.vertices, np.float32),
                                   tri_verts=np.asarray(t.faces, np.uint32)))
    u = man(m)
    for g in inlays:
        u = u + man(trimesh.load_mesh(g))
    o = u.to_mesh()
    return (trimesh.Trimesh(vertices=np.asarray(o.vert_properties)[:, :3], faces=np.asarray(o.tri_verts)),
            " + " + ", ".join(os.path.basename(g)[len(os.path.basename(base)) + 2:-4] for g in inlays))


files = [f for f in files if "__" not in os.path.basename(f)]
bad_files = 0
for f in files:
    m, tag = merged(f)
    n = m.face_normals
    off_bed = m.triangles[:, :, 2].min(1) > m.bounds[0][2] + 0.05
    over = (n[:, 2] < -np.sin(np.radians(LIMIT))) & off_bed
    if tag and over.any():
        # merged inlays: the boolean seam where an inlay meets its pocket leaves sub-0.1 mm2
        # slivers with arbitrary normals; drop flagged patches that small (real ledges are bigger)
        keep = np.zeros(len(over), bool)
        idx = np.where(over)[0]
        for comp in trimesh.graph.connected_components(m.face_adjacency, nodes=idx):
            comp = np.asarray(list(comp))
            if m.area_faces[comp].sum() >= 0.1: keep[comp] = True
        over = keep
    area = m.area_faces[over].sum()
    ok = m.is_watertight and area < 0.01
    bad_files += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {os.path.basename(f) + tag:32s} watertight={m.is_watertight} "
          f"bodies={len(m.split(only_watertight=False))} overhang>{LIMIT - 1}deg={area:.2f} mm2")
    if area >= 0.01:
        for p in m.submesh([np.where(over)[0]], append=True).split(only_watertight=False):
            lo, hi = p.bounds
            print(f"       at x {lo[0]:.1f}..{hi[0]:.1f}  y {lo[1]:.1f}..{hi[1]:.1f}  z {lo[2]:.2f}  ({p.area:.2f} mm2)")
sys.exit(1 if bad_files else 0)
