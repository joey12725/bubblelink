# BubbleLink CTRL v1.2 engineering change

Order **[assembly order]**. Issued **2026-09-09**.

## Decision and rationale

Retain **TI TLV1822QDRQ1** and replace the incorrect U1 land pattern. This is the most supportable correction with the available design, photos and manufacturer documents. No electrically and mechanically validated BOM-only substitute has been identified. A same-function comparator in another package is not a drop-in, and the standard SOIC versions need the wider footprint too. An adapter or hand-wired rework could be a separately engineered salvage option, but is not supplied or approved here; for the small existing order, a proper remake avoids introducing an unqualified mechanical assembly.

The comparator's rail-to-rail inputs, low input bias, open-drain outputs and defined startup behavior are part of the existing circuit assumptions. Keeping the part avoids changing those assumptions. This conclusion is based on fit and circuit behavior, not merely the old packet's substitution prohibition. [TI TLV1822-Q1](https://www.ti.com/lit/ds/symlink/tlv1822-q1.pdf)

## Correction to the earlier memo

The **5.40 mm dimension is spacing between opposite pad-row centers**, not the lead pitch. Lead pitch is **1.27 mm**.

The earlier disposition's claim that the manufactured pads had their dimensions transposed is not supported by the released Gerbers. The original top-copper flashes are **0.60 mm along the row x 1.00 mm across the package**. Reading KiCad pad size without its absolute pad angle and footprint-coordinate transform produced the erroneous description. The original copper outer span is **5.30 mm**, not 4.90 mm; its inner gap is **3.30 mm**, not 3.70 mm. This correction does not change the need for a new land pattern.

| U1 geometry | Original v1.1 Gerber | Revised v1.2 |
|---|---:|---:|
| Same-row lead pitch | 1.27 mm | 1.27 mm |
| Opposite-row center distance | 4.30 mm | 5.40 mm |
| Copper length across package | 1.00 mm | 1.55 mm |
| Copper width along row | 0.60 mm | 0.60 mm |
| Inner copper gap | 3.30 mm | 3.85 mm |
| Outer copper span | 5.30 mm | 6.95 mm |
| U1 mask expansion per side | nominal zero | 0.075 mm |

The revised geometry follows TI's D0008A example board and stencil patterns. The package drawing permits process-dependent alternatives; PCBWay should confirm the stencil process and mask registration. [TI D0008A drawing](https://www.ti.com/lit/ml/msoi002k/msoi002k.pdf)

## Exact engineering changes

- U1's eight copper pads and ports move outward by 0.55 mm per row and become 1.55 x 0.60 mm lands. U1 centroid and 90-degree CPL rotation stay unchanged.
- U1 mask apertures become 1.70 x 0.75 mm, providing 0.075 mm expansion per side. U1 paste follows the full copper size.
- U1 courtyard expands to cover the corrected land envelope with 0.25 mm margin.
- Attached endpoints and nearby ground/signal routing are adjusted to clear the expanded lands.
- Three signal vias move (coordinates below use the original centered CAD datum, not the lower-left CPL datum). No via is added or removed.
- Bottom GND pour is regenerated against the revised routing and via positions.
- Visible board revision text changes to v1.2. Net identifiers containing v1_1 are intentionally retained internal identities, not stale geometry.
- New assembly PDF and pad-1 coordinate CSV identify actual numbered pads. The generic exporter's corner triangles are not reliable orientation references for rotated components; its assembly thumbnail is deliberately not shipped.
- All logical source records, MPNs, values, component centroids and CPL angles remain unchanged. All board dimensions, mounting holes, through-hole locations and the current-carrying return bank remain unchanged.

| Signal via | Original CAD X,Y | Revised CAD X,Y | Reason |
|---|---|---|---|
| pcb_via_search_19 | -10.70, 5.00 | -10.40, 5.55 | Clearance from expanded U1 pin 8 and nearby routing |
| pcb_via_search_48 | -9.00, 4.90 | -9.00, 5.45 | Via-to-pad clearance from expanded U1 pin 6 |
| pcb_via_search_24 | -17.70, 10.30 | -17.40, 10.35 | Existing ~0.112 mm via-to-R18 pad clearance below the 0.20 mm rule |

The full Gerber/drill set must be replaced, including the plated drill program and bottom copper. Old stencil and drill files cannot be reused just because the component centroids and hole count are unchanged.

## Verification and its limits

- Legacy routing/placement/connectivity engine: **zero violations, zero unconnected items**, all 18 categories clean.
- Independent Shapely geometry check: different-net copper separation at least **0.200 mm top**, **0.207 mm bottom**, including SMT/PTH pads, traces, vias and the regenerated pour. Distances include the permanently connected physical PRIME switch pin pairs.
- Actual Gerbers, decoded independently with Gerbonara, match the complete intended copper geometry on both layers within 0.002 mm geometric tolerance. No extra or missing copper beyond that tolerance.
- U1 copper, paste and mask flashes are separately checked for eight exact pad positions/dimensions.
- All component SMT pad positions, sizes and absolute orientations in KiCad are reconciled against serialized geometry; no mismatch.
- The old U1 footprint is intentionally fed to the new geometry assertion and rejected.
- Automated structural release QA: **50 PASS, 0 FAIL, 0 pending**. It adds a manufacturer U1 geometry gate to the existing checks. See the freshly generated JSON result and checksum manifest; do not reuse the old v1.1 result as evidence.
- The unchanged electrical model was rerun with **20,000 samples**, seed **20260807**: `model_passed=true`, no analytic failures. Nine bench-only gates remain pending; no physical measurements are claimed.

The added geometric checks caught a pre-existing R18 clearance problem as well as a U1 via clearance that the old routing suite missed. A generic DRC pass or matching checksum is not proof of manufacturer package fit.

**KiCad-native CLI DRC was not available.** The checks supplied here are serialized-circuit DRC, independently decoded export geometry and KiCad pad reconciliation. PCBWay must still complete its own CAM/assembly review. Electrical startup, brownout, timing calibration, sensor noise, external pump/buck behavior and thermal/EMI performance require the existing bench procedure after assembly; this footprint ECO is not physical product qualification.

## Other likely assembly issues reviewed / flagged

| Item | Finding and handoff action |
|---|---|
| U2, TLV803EA43DBZR | Exact DBZ pinout is 1 GND, 2 RESET, 3 VDD. Do not accept RDBZ/VDBZ variants. Existing SOT-23 pad pattern retained; ask PCBWay to confirm its process fit. |
| Q1/Q3 DMP2065UQ-7; Q2 AO3400A | Same numerical G/S/D pin map, different channel polarity. Actual SOT-23 bodies and lead spans differ between vendors; package identity alone is insufficient. Existing pads retained after dimension review; factory to verify actual procured-part overlap and solder fillets. |
| D1 B340A-E3/61T | Custom SMA lands retained: 1.88 x 1.68 mm, 3.40 mm centers. Pad 1 is cathode; explicit coordinate and band instruction supplied. |
| F1 1812L150/16DR | Custom PTC lands retained: 1.78 x 3.15 mm, 5.23 mm centers. Do not replace with a generic 1812 resistor footprint or generic 1.5 A fuse. |
| Passive packages | 0805 lands are 1.025 x 1.40 mm with 1.825 mm centers; 1206 lands 1.125 x 1.75 mm with 2.925 mm centers; 1210 lands 1.125 x 2.65 mm with 2.925 mm centers. Size classes are consistent with the BOM. This is not a full vendor-by-vendor solder-process qualification. |
| C2/C6/C7 | Preserve exact values, voltage, dielectric and MPN. Confirm purchased stock and body size before remake; especially C6 1210 versus C7 1206. Avoid a distributor's automatic smaller-package replacement. |
| Placement clearances | Existing courtyards are disjoint, but C7/U2 have only 0.02 mm courtyard separation. Ask PCBWay to verify actual body/tolerance fit; do not infer body collision solely from that courtyard gap. |
| Population / stencil | Exactly 41 SMT placements and 92 paste apertures; R22 and J4 DNP; C9 and R18 fitted. No THT/fiducial/bottom paste. |
| Flux / calibration | High-value 4.7 Mohm nodes need clean assembly. Do not add an unqualified coating before calibration. |
| THT / external hardware | User installs exact THT parts and tests the harness. Existing AUTO/FORCE ON input and weak-current sensing limitations remain; no new external part purchase is required by this ECO. |

Manufacturer references: [TI TLV803E](https://www.ti.com/lit/ds/symlink/tlv803e.pdf), [Diodes DMP2065UQ](https://www.diodes.com/datasheet/download/DMP2065UQ.pdf), [AOS AO3400A](https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf), [AOS SOT23 mechanical drawing](https://www.aosmd.com/sites/default/files/res/package/SOT23.pdf), [Vishay B340A](https://www.vishay.com/doc/?88896=), [Littelfuse 1812L](https://www.littelfuse.com/assetdocs/resettable-ptcs-1812l-datasheet?assetguid=ca5c80cb-504e-4a8a-8e74-0107520a1717), [TDK C6 product detail](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R1E226M250AB).

## Factory response requested

Confirm v1.2 receipt, fabrication/assembly status, remake/stencil cost, revised schedule, exact-part availability and a single consolidated DFM response. Obtain updated placement preview and first-article photos. This package does not itself authorize additional charges or a part substitution.
