# Rebuild the v1.2 engineering change

Run `bash rebuild.sh` from this directory. Dependencies: Node/npm; Python 3 with gerbonara, shapely and reportlab; DejaVu Sans fonts for the PDF. The included package lock pins the export/check/pour tools. `npm ci` fetches dependencies.

The exact routed input is `v1_1_baseline.circuit.json`. `correct_u1.py` applies the explicit pad, mask, courtyard, route, via and revision-text changes. `repour.mjs` regenerates only the ground pour. The electrical source records remain unchanged. The output is `../BubbleLink_CTRL_v1_2_FINAL.circuit.json`.

`circuit.tsx` is an authoring reference with U1's explicit footprint replacing the generic soic8. It is not the exact routed manufacturing build entry point; use the baseline plus deterministic ECO script. Internal v1_1 net identities are intentionally preserved.

`export_final.mjs` exports copper, mask, paste, drills and KiCad. It supplies 92 full-size top SMT paste apertures and omits DNP/THT/fiducial/bottom paste. `make_drawings.py` builds the authoritative assembly PDF from numbered pads, avoiding generic corner markers that can misidentify pin 1 on rotated parts.

Gerber previews were generated with Gerbonara from the final copper files. The bottom copper preview uses the same top-view coordinate system as the top copper preview; it is not a bottom-side mirrored assembly view.

Rebuilding changes export timestamps and ZIP metadata. Do not silently accept hash changes. Review the regenerated data, rerun verification, and intentionally freeze a new release if modified. The supplied checksums bind the shipped files.
