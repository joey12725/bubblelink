"""Drop stray zero-area triangles from STLs, in place.

    python clean_stl.py stl/70_*.stl ...

OpenSCAD's manifold backend sometimes leaves a few isolated zero-area triangles where
coplanar faces of a union meet (the Duo shells' flat side faces). They hold no geometry but
make the mesh read as "not watertight" and slicers report them as errors. This removes those
stray pieces (nothing else) and refuses to write a file whose remaining mesh isn't watertight.
Needs trimesh + numpy.
"""
import sys
import numpy as np
import trimesh

bad = 0
for f in sys.argv[1:]:
    m = trimesh.load_mesh(f)
    n0 = len(m.faces)
    # drop only stray pieces with no area; zero-height needles inside the real surface stay
    comps = trimesh.graph.connected_components(m.face_adjacency, nodes=np.arange(n0), min_len=1)
    stray = [c for c in comps if m.area_faces[list(c)].sum() < 1e-6]
    if stray:
        keep = np.ones(n0, bool)
        for c in stray: keep[list(c)] = False
        m.update_faces(keep)
        m.remove_unreferenced_vertices()
    if not m.is_watertight:
        print(f"FAIL {f}: not watertight after dropping {n0 - len(m.faces)} faces (left unchanged)")
        bad += 1
        continue
    if len(m.faces) != n0:
        m.export(f, file_type="stl_ascii")   # full precision, like OpenSCAD's (float32 would merge needle edges)
        print(f"     {f}: dropped {n0 - len(m.faces)} zero-area faces")
sys.exit(1 if bad else 0)
