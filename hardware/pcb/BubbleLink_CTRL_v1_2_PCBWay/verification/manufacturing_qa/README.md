# BubbleLink v1.2 manufacturing QA

This is the v1.1 structural validator plus an explicit U1 manufacturer-geometry gate. The electronic manifest is unchanged except its revision title. Exact topology, population, current-path rules, courtyards and board dimensions remain required.

Run from the outer handoff directory:

```sh
python3 verification/verify_eco.py
bash verification/run_release_qa.sh
```

`verify_eco.py` independently decodes the actual copper with Gerbonara, reconciles copper shapes with the circuit, checks all different-net copper separations with Shapely (including pad/via and pour clearances), checks U1 copper/paste/mask, rejects the old U1 footprint, and reconciles all component SMT pad coordinates/sizes/angles with the KiCad export. It requires Python gerbonara and shapely.

The release validator separately reconciles the board, nets, holes, source, BOM, CPL, DRC, export counts and frozen file hashes. The U1 assertion is intentionally specific to this release's centroid, orientation, pad numbering and manufacturer land pattern.

This is not KiCad-native CLI DRC or physical bench qualification. No paid remake is implied by a software pass; PCBWay must review the actual CAM/assembly data and provide revised cost/schedule for customer acceptance.
