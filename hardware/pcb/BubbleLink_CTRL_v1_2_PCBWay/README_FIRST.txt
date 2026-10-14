BUBBLELINK CTRL v1.2 - COMPLETE PCBWAY ENGINEERING-CHANGE HANDOFF
Order [assembly order] | 2026-09-09

Send this complete ZIP with the reply in EMAIL_TO_PCBWAY.txt.
Do not upload the outer handoff ZIP as a Gerber ZIP. PCBWay should unpack it
and use fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip for PCB fabrication.

REQUIRED FABRICATION / ASSEMBLY INPUTS
fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip
assembly/PCBWAY_SMT_BOM.csv
assembly/PCBWAY_SMT_CPL.csv
assembly/ASSEMBLY_NOTES_FOR_PCBWAY.txt
drawings/BubbleLink_CTRL_v1_2_Assembly_and_U1_Detail.pdf
assembly/CRITICAL_PAD1_COORDINATES.csv

SUPPORTING RECORDS
references/TI_D0008A_SOIC8_Land_Pattern.pdf
ENGINEERING_CHANGE_AND_REVIEW.md
source/ - revised KiCad files, serialized design, deterministic ECO source
verification/ - actual rerun results, geometry regression and original circuit model
drawings/Gerber_top.png and Gerber_bottom.png - independently parsed CAM previews
customer/ - unmodified electrical bring-up and harness instructions, still applicable
SHA256SUMS.txt - exact final packaged file checksums

U1 footprint is corrected, with supporting routing and via clearance repairs.
All electronic parts, logical connections, component centroids and CPL angles
are unchanged. The reused BOM/CPL data is intentional, not a stale-file error.
Use the ENTIRE v1.2 fabrication set: three signal vias have moved, so even
nominally unchanged mechanical drill counts do not permit old drill reuse.
Old v1.1 boards, stencil and generic assembly thumbnail are superseded.
The PDF's numbered pads and pin-1 coordinate table control orientation.

Automated geometry/reconciliation results are not bench measurements or a
PCBWay CAM approval. Obtain the revised quote/schedule and consolidated
factory DFM review. Complete electrical commissioning after THT installation.
