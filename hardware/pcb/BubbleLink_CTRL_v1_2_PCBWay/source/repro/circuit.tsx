import { createKiCadRoutingToolsAutorouter } from "@tscircuit/krt-wasm"

/*
 * BubbleLink CTRL v1.1
 *
 * Circuit authoring reference. Routed release authority is the FINAL circuit JSON;
 * use rebuild.sh for the exact revised manufacturing export.  The circuit intentionally
 * uses explicit physical pad numbers for every polarity-sensitive or unusual
 * footprint.  In particular, the Bourns 3296W lead order is 1-3-2.
 */

const u1TiD0008AFootprint = (
  <footprint>
    <smtpad name="pin1" portHints={["pin1"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={-2.700} pcbY={1.905} />
    <smtpad name="pin2" portHints={["pin2"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={-2.700} pcbY={0.635} />
    <smtpad name="pin3" portHints={["pin3"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={-2.700} pcbY={-0.635} />
    <smtpad name="pin4" portHints={["pin4"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={-2.700} pcbY={-1.905} />
    <smtpad name="pin5" portHints={["pin5"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={2.700} pcbY={-1.905} />
    <smtpad name="pin6" portHints={["pin6"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={2.700} pcbY={-0.635} />
    <smtpad name="pin7" portHints={["pin7"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={2.700} pcbY={0.635} />
    <smtpad name="pin8" portHints={["pin8"]} shape="rect" width="1.55mm" height="0.60mm" solderMaskMargin="0.075mm" layer="top" pcbX={2.700} pcbY={1.905} />
  </footprint>
)

const jstXh2Footprint = (
  <footprint insertionDirection="from_above">
    <platedhole name="pin1" portHints={["pin1"]} shape="circular_hole_with_rect_pad" holeDiameter="1mm" rectPadWidth="1.8mm" rectPadHeight="1.8mm" pcbX={-1.25} pcbY={0} />
    <platedhole name="pin2" portHints={["pin2"]} shape="circle" holeDiameter="1mm" outerDiameter="1.8mm" pcbX={1.25} pcbY={0} />
    <silkscreenrect width="7.5mm" height="5.75mm" pcbY={0.75} filled={false} strokeWidth="0.15mm" />
    <silkscreentext text="1" pcbX={-1.25} pcbY={-1.8} fontSize="0.8mm" />
  </footprint>
)

const jstXh3Footprint = (
  <footprint insertionDirection="from_above">
    <platedhole name="pin1" portHints={["pin1"]} shape="circular_hole_with_rect_pad" holeDiameter="1mm" rectPadWidth="1.8mm" rectPadHeight="1.8mm" pcbX={-2.5} pcbY={0} />
    <platedhole name="pin2" portHints={["pin2"]} shape="circle" holeDiameter="1mm" outerDiameter="1.8mm" pcbX={0} pcbY={0} />
    <platedhole name="pin3" portHints={["pin3"]} shape="circle" holeDiameter="1mm" outerDiameter="1.8mm" pcbX={2.5} pcbY={0} />
    <silkscreenrect width="10mm" height="5.75mm" pcbY={0.75} filled={false} strokeWidth="0.15mm" />
    <silkscreentext text="1" pcbX={-2.5} pcbY={-1.8} fontSize="0.8mm" />
  </footprint>
)

const padsOnly2Footprint = (
  <footprint insertionDirection="from_above">
    <platedhole name="pin1" portHints={["pin1"]} shape="circular_hole_with_rect_pad" holeDiameter="1mm" rectPadWidth="1.8mm" rectPadHeight="1.8mm" pcbX={0} pcbY={1.25} />
    <platedhole name="pin2" portHints={["pin2"]} shape="circle" holeDiameter="1mm" outerDiameter="1.8mm" pcbX={0} pcbY={-1.25} />
    <silkscreenrect width="2.3mm" height="4.4mm" filled={false} strokeWidth="0.15mm" />
    <silkscreentext text="1" pcbX={-0.8} pcbY={1.25} fontSize="0.7mm" />
  </footprint>
)

const trimmer3296wFootprint = (clockwiseLabel: string) => (
  <footprint insertionDirection="from_above">
    {/* Bourns 3296W, top view: physical left-to-right order is 1, 3, 2. */}
    <platedhole name="pin1" portHints={["pin1"]} shape="circular_hole_with_rect_pad" holeDiameter="0.9mm" rectPadWidth="1.7mm" rectPadHeight="1.7mm" pcbX={-2.54} pcbY={0} />
    <platedhole name="pin3" portHints={["pin3"]} shape="circle" holeDiameter="0.9mm" outerDiameter="1.7mm" pcbX={0} pcbY={0} />
    <platedhole name="pin2" portHints={["pin2"]} shape="circle" holeDiameter="0.9mm" outerDiameter="1.7mm" pcbX={2.54} pcbY={0} />
    <silkscreenrect width="10.2mm" height="5.5mm" pcbY={0.25} filled={false} strokeWidth="0.15mm" />
    <silkscreentext text="1" pcbX={-3.8} pcbY={-1.8} fontSize="0.75mm" />
    <silkscreentext text={clockwiseLabel} pcbX={0.6} pcbY={2.2} fontSize="0.65mm" />
  </footprint>
)

const switchB3fFootprint = (
  <footprint insertionDirection="from_above">
    <platedhole name="pin1" portHints={["pin1"]} shape="circular_hole_with_rect_pad" holeDiameter="1mm" rectPadWidth="1.8mm" rectPadHeight="1.8mm" pcbX={-3.25} pcbY={-2.25} />
    <platedhole name="pin2" portHints={["pin2"]} shape="circle" holeDiameter="1mm" outerDiameter="1.8mm" pcbX={-3.25} pcbY={2.25} />
    <platedhole name="pin3" portHints={["pin3"]} shape="circle" holeDiameter="1mm" outerDiameter="1.8mm" pcbX={3.25} pcbY={-2.25} />
    <platedhole name="pin4" portHints={["pin4"]} shape="circle" holeDiameter="1mm" outerDiameter="1.8mm" pcbX={3.25} pcbY={2.25} />
    <silkscreenrect width="6.4mm" height="6.4mm" filled={false} strokeWidth="0.15mm" />
  </footprint>
)

const led3mmFootprint = (
  <footprint insertionDirection="from_above">
    <platedhole name="pin1" portHints={["pin1"]} shape="circular_hole_with_rect_pad" holeDiameter="0.9mm" rectPadWidth="1.7mm" rectPadHeight="1.7mm" pcbX={-1.27} pcbY={0} />
    <platedhole name="pin2" portHints={["pin2"]} shape="circle" holeDiameter="0.9mm" outerDiameter="1.7mm" pcbX={1.27} pcbY={0} />
    <silkscreencircle radius="1.7mm" isOutline={true} strokeWidth="0.15mm" />
    <silkscreentext text="K" pcbX={-1.7} pcbY={-1.8} fontSize="0.7mm" />
  </footprint>
)

const radialCap5mmFootprint = (
  <footprint insertionDirection="from_above">
    <platedhole name="pin1" portHints={["pin1"]} shape="circular_hole_with_rect_pad" holeDiameter="0.8mm" rectPadWidth="1.7mm" rectPadHeight="1.7mm" pcbX={-1} pcbY={0} />
    <platedhole name="pin2" portHints={["pin2"]} shape="circle" holeDiameter="0.8mm" outerDiameter="1.7mm" pcbX={1} pcbY={0} />
    <silkscreencircle radius="2.75mm" isOutline={true} strokeWidth="0.15mm" />
    <silkscreentext text="+" pcbX={-1.8} pcbY={-1.8} fontSize="1mm" />
  </footprint>
)

const smaDiodeFootprint = (
  <footprint>
    {/* KiCad/IPC diode convention: pad 1 is cathode. */}
    {/* Vishay document 88896 SMA mounting pattern: 5.28 mm overall,
        1.52 mm inner gap, 1.88 x 1.68 mm pads. */}
    <smtpad name="pin1" portHints={["pin1"]} shape="rect" width="1.88mm" height="1.68mm" layer="top" pcbX={-1.70} pcbY={0} />
    <smtpad name="pin2" portHints={["pin2"]} shape="rect" width="1.88mm" height="1.68mm" layer="top" pcbX={1.70} pcbY={0} />
    {/* Horizontal body bars avoid crossing the terminal lands. */}
    <silkscreenline x1="-2.45mm" y1="-1.45mm" x2="2.45mm" y2="-1.45mm" strokeWidth="0.15mm" />
    <silkscreenline x1="-2.45mm" y1="1.45mm" x2="2.45mm" y2="1.45mm" strokeWidth="0.15mm" />
    <silkscreentext text="K" pcbX={-2.25} pcbY={-1.8} fontSize="0.8mm" />
  </footprint>
)

const ptc1812Footprint = (
  <footprint>
    {/* Littelfuse 1812L recommended pad layout: 3.45 mm inner gap,
        1.78 x 3.15 mm pads (7.01 mm overall). */}
    <smtpad name="pin1" portHints={["pin1"]} shape="rect" width="1.78mm" height="3.15mm" layer="top" pcbX={-2.615} pcbY={0} />
    <smtpad name="pin2" portHints={["pin2"]} shape="rect" width="1.78mm" height="3.15mm" layer="top" pcbX={2.615} pcbY={0} />
    {/* Horizontal body bars avoid crossing the wide 1812 terminal lands. */}
    <silkscreenline x1="-2.35mm" y1="-1.85mm" x2="2.35mm" y2="-1.85mm" strokeWidth="0.15mm" />
    <silkscreenline x1="-2.35mm" y1="1.85mm" x2="2.35mm" y2="1.85mm" strokeWidth="0.15mm" />
  </footprint>
)

/*
 * Deterministic two-terminal routing trees.  These replace the implicit
 * multi-terminal `net.*` source traces, which the local KRT router cannot
 * reliably decompose on this dense board.  Every tree has N-1 edges, touches
 * every pad exactly as the named net did, and uses nearby real pads as branch
 * nodes.  The high-current trees retain their released trace widths.
 */
const routingTrees = [
  { name: "PLUS_5V_PUMP", edges: [
    /* Keep the entire 1.5 A feed on top copper.  The explicit lower-edge
       corridor avoids C1 and removes the autorouter's two 0.30 mm drill
       bottlenecks from this 1.2 mm power path.  Coordinates are J1-local. */
    [".J1 > .pin1", ".F1 > .pin1", "1.2mm", false,
      [{ x: -1.25, y: -2.9 }, { x: 18.885, y: -2.9 }]],
    [".J1 > .pin1", ".C1 > .pin1", "1mm"],
    [".J1 > .pin1", ".FB1 > .pin1"],
    [".J1 > .pin1", ".TP1 > .pin1", "1mm", false, [{ x: -3.5, y: 0 }, { x: -3.9, y: 1 }]],
  ]},
  { name: "GND", edges: [
    [".J1 > .pin2", ".Q2 > .pin2", "1.2mm"],
    [".J1 > .pin2", ".C1 > .pin2", "1mm"],
    [".U1 > .pin4", ".R8 > .pin2"],
    [".R11 > .pin2", ".C8 > .pin2"],
    [".R18 > .pin2", ".C12 > .pin2"],
    [".C8 > .pin2", ".C10 > .pin2"],
    [".C8 > .pin2", ".U2 > .pin1"],
    [".U2 > .pin1", ".C11 > .pin2"],
    [".C2 > .pin2", ".C3 > .pin2"],
    [".C7 > .pin2", ".R21 > .pin2"],
    [".J2 > .pin2", ".C12 > .pin2"],
    [".C11 > .pin2", ".TP13 > .pin1"],
    [".R15 > .pin2", ".C10 > .pin2"],
    [".R3 > .pin2", ".RV2 > .pin1"],
    [".R8 > .pin2", ".C6 > .pin2"],
    [".R21 > .pin2", ".RV2 > .pin1"],
    [".C1 > .pin2", ".C3 > .pin2"],
    [".SW1 > .pin3", ".TP13 > .pin1"],
    [".J2 > .pin2", ".C5 > .pin2"],
    [".C7 > .pin2", ".U2 > .pin1"],
    [".C10 > .pin2", ".Q2 > .pin2"],
    [".U1 > .pin4", ".C4 > .pin2"],
    [".C6 > .pin2", ".C7 > .pin2"],
    [".J4 > .pin2", ".TP13 > .pin1"],
    [".LED1 > .pin1", ".R3 > .pin2"],
    [".LED1 > .pin1", ".J2 > .pin2"],
    /* Drop the low-current TP3 branch to bottom copper at a deliberate via,
       then approach the plated test point from the lower-left.  This keeps
       it clear of the fixed +5 V feed and the dense FB1/C1 top-copper fanout. */
    [".J1 > .pin2", ".TP3 > .pin1", "0.25mm", false,
      [{ x: 2.3, y: 0 },
       { x: 2.8, y: -1.5 },
       { x: 2.8, y: -1.5, via: true, fromLayer: "top", toLayer: "bottom" },
       { x: 2.8, y: -1.5 },
       { x: 4.3, y: 3.5 },
       { x: -5.2, y: 5.0 }]],
  ]},
  { name: "PLUS_5V_LOGIC", edges: [
    [".FB1 > .pin2", ".C2 > .pin1"],
    [".FB1 > .pin2", ".TP2 > .pin1"],
    [".C2 > .pin1", ".C3 > .pin1"],
    [".C3 > .pin1", ".Q3 > .pin2"],
    [".Q3 > .pin2", ".R12 > .pin1"],
    [".R12 > .pin1", ".R10 > .pin1"],
    [".R10 > .pin1", ".U2 > .pin3"],
    [".U2 > .pin3", ".C11 > .pin1"],
    [".R12 > .pin1", ".R7 > .pin1"],
    [".R7 > .pin1", ".U1 > .pin8"],
    [".U1 > .pin8", ".R4 > .pin1"],
    [".U1 > .pin8", ".C4 > .pin1"],
    [".R4 > .pin1", ".R2 > .pin1"],
    [".R2 > .pin1", ".R17 > .pin1"],
    [".R17 > .pin1", ".R6 > .pin1"],
    [".R2 > .pin1", ".J2 > .pin1"],
    [".R6 > .pin1", ".R16 > .pin1"],
    [".J2 > .pin1", ".C12 > .pin1"],
  ]},
  { name: "ACS_OUT", edges: [
    [".J2 > .pin3", ".R18 > .pin1"],
    [".R18 > .pin1", ".R1 > .pin1"],
    [".R18 > .pin1", ".TP4 > .pin1"],
  ]},
  { name: "ACS_FILTER", edges: [
    [".R1 > .pin2", ".C5 > .pin1"],
    [".R1 > .pin2", ".TP5 > .pin1"],
    [".C5 > .pin1", ".U1 > .pin2"],
  ]},
  { name: "VTH", edges: [
    [".RV1 > .pin2", ".R19 > .pin1"],
    [".R19 > .pin1", ".TP6 > .pin1"],
    [".TP6 > .pin1", ".R5 > .pin2"],
    [".R5 > .pin2", ".R22 > .pin2"],
    [".R5 > .pin2", ".U1 > .pin3"],
  ]},
  { name: "DET_N", edges: [
    [".U1 > .pin1", ".R5 > .pin1"],
    [".R5 > .pin1", ".R22 > .pin1"],
    [".R22 > .pin1", ".TP7 > .pin1"],
    [".R5 > .pin1", ".R4 > .pin2"],
    [".U1 > .pin1", ".Q1 > .pin1"],
    [".Q1 > .pin1", ".LED2 > .pin1"],
    [".LED2 > .pin1", ".SW1 > .pin1"],
    [".SW1 > .pin1", ".J4 > .pin1"],
  ]},
  { name: "VDELAY", edges: [
    [".U1 > .pin5", ".R13 > .pin2"],
    [".R13 > .pin2", ".R10 > .pin2"],
    [".R10 > .pin2", ".R11 > .pin1"],
    [".R11 > .pin1", ".C8 > .pin1"],
    [".C8 > .pin1", ".TP10 > .pin1"],
  ]},
  { name: "HOLD", edges: [
    [".U1 > .pin6", ".R20 > .pin2"],
    [".R20 > .pin2", ".TP9 > .pin1"],
    [".R20 > .pin2", ".C7 > .pin1"],
    [".R20 > .pin2", ".R21 > .pin1"],
    [".R21 > .pin1", ".R9 > .pin1"],
    [".R9 > .pin1", ".R23 > .pin2"],
  ]},
  { name: "TIMER_N", edges: [
    [".U1 > .pin7", ".R13 > .pin1"],
    [".R13 > .pin1", ".R12 > .pin2"],
    [".R12 > .pin2", ".Q3 > .pin1"],
    [".Q3 > .pin1", ".TP14 > .pin1"],
    [".U1 > .pin7", ".LED3 > .pin1"],
  ]},
  { name: "VMID", edges: [
    [".R7 > .pin2", ".C6 > .pin1"],
    [".C6 > .pin1", ".R8 > .pin1"],
    [".R8 > .pin1", ".TP8 > .pin1"],
    [".C6 > .pin1", ".Q1 > .pin2"],
  ]},
  { name: "PUMP_GATE", edges: [
    [".R14 > .pin2", ".R15 > .pin1"],
    [".R15 > .pin1", ".C10 > .pin1"],
    [".C10 > .pin1", ".TP11 > .pin1"],
    [".TP11 > .pin1", ".Q2 > .pin1"],
  ]},
  { name: "PUMP_SW_NEG", edges: [
    [".Q2 > .pin3", ".J3 > .pin2", "1.2mm"],
    [".Q2 > .pin3", ".D1 > .pin2", "1mm"],
    [".D1 > .pin2", ".C9 > .pin2"],
    [".D1 > .pin2", ".TP12 > .pin1", "1mm"],
  ]},
  { name: "PUMP_PLUS", edges: [
    [".F1 > .pin2", ".J3 > .pin1", "1.2mm"],
    [".J3 > .pin1", ".D1 > .pin1", "1mm"],
    [".D1 > .pin1", ".C9 > .pin1"],
    [".F1 > .pin2", ".TP15 > .pin1", "1mm"],
  ]},
] as const

export default () => (
  <board
    name="BubbleLink_CTRL_v1_1"
    width="50mm"
    height="40mm"
    thickness="1.6mm"
    layers={2}
    autorouter={{
      algorithmFn: createKiCadRoutingToolsAutorouter({
        gridStep: 0.1,
        clearance: 0.2,
        maxIterations: 300_000,
      }),
    }}
    autorouterEffortLevel="1x"
    minTraceWidth="0.20mm"
    nominalTraceWidth="0.25mm"
    minTraceToPadEdgeClearance="0.20mm"
    minPadEdgeToPadEdgeClearance="0.20mm"
    minBoardEdgeClearance="0.50mm"
    minViaHoleDiameter="0.30mm"
    minViaPadDiameter="0.60mm"
    pcbStyle={{ viaHoleDiameter: "0.30mm", viaPadDiameter: "0.60mm" }}
  >
    {/* Mechanical datum: board center is (0,0), 50 x 40 mm. */}
    <hole name="H1" diameter="3.2mm" pcbX={-21.5} pcbY={-16.5} />
    <hole name="H2" diameter="3.2mm" pcbX={21.5} pcbY={-16.5} />
    <hole name="H3" diameter="3.2mm" pcbX={-21.5} pcbY={16.5} />
    <hole name="H4" diameter="3.2mm" pcbX={21.5} pcbY={16.5} />
    <keepout shape="circle" radius="3mm" layers={["top", "bottom"]} pcbX={-21.5} pcbY={-16.5} />
    <keepout shape="circle" radius="3mm" layers={["top", "bottom"]} pcbX={21.5} pcbY={-16.5} />
    <keepout shape="circle" radius="3mm" layers={["top", "bottom"]} pcbX={-21.5} pcbY={16.5} />
    <keepout shape="circle" radius="3mm" layers={["top", "bottom"]} pcbX={21.5} pcbY={16.5} />

    <fiducial name="FID1" padDiameter="1mm" soldermaskPullback="0.5mm" pcbX={-20} pcbY={-10.5} />
    <fiducial name="FID2" padDiameter="1mm" soldermaskPullback="0.5mm" pcbX={20} pcbY={-10.5} />
    <fiducial name="FID3" padDiameter="1mm" soldermaskPullback="0.5mm" pcbX={18.5} pcbY={9} />

    {/* External interfaces. */}
    <chip name="J1" displayName="POWER 5V" manufacturerPartNumber="B2B-XH-A(LF)(SN)" mfn="JST" footprint={jstXh2Footprint}
      pinLabels={{ pin1: "PLUS_5V_PUMP", pin2: "GND" }} schPinArrangement={{ leftSide: ["pin1", "pin2"] }} pcbX={-14.3} pcbY={-15.5} pcbRotation={0} />
    <chip name="J2" displayName="ACS758" manufacturerPartNumber="B3B-XH-A(LF)(SN)" mfn="JST" footprint={jstXh3Footprint}
      pinLabels={{ pin1: "PLUS_5V_LOGIC", pin2: "GND", pin3: "ACS_OUT" }} schPinArrangement={{ leftSide: ["pin1", "pin2", "pin3"] }} pcbX={-13.8} pcbY={15.3} pcbRotation={180} />
    <chip name="J3" displayName="PUMP" manufacturerPartNumber="B2B-XH-A(LF)(SN)" mfn="JST" footprint={jstXh2Footprint}
      pinLabels={{ pin1: "PUMP_PLUS", pin2: "PUMP_SW_NEG" }} schPinArrangement={{ rightSide: ["pin1", "pin2"] }} pcbX={14.3} pcbY={-15.5} pcbRotation={0} />
    <chip name="J4" displayName="EXT PRIME DNP" doNotPlace={true} footprint={padsOnly2Footprint}
      pinLabels={{ pin1: "DET_N", pin2: "GND" }} schPinArrangement={{ rightSide: ["pin1", "pin2"] }} pcbX={22} pcbY={4.5} />

    {/* Power filtering and indication. */}
    <chip name="C1" displayName="100uF 16V" manufacturerPartNumber="16ZLH100MEFC5X11" mfn="Rubycon" footprint={radialCap5mmFootprint}
      pinLabels={{ pin1: "POS", pin2: "NEG" }} schPinArrangement={{ leftSide: ["pin1"], rightSide: ["pin2"] }} pcbX={-7} pcbY={-15.2} />
    <chip name="FB1" displayName="220R@100MHz" manufacturerPartNumber="BLM21PG221SN1D" mfn="Murata" footprint="0805"
      pinLabels={{ pin1: "PUMP_RAIL", pin2: "LOGIC_RAIL" }} schPinArrangement={{ leftSide: ["pin1"], rightSide: ["pin2"] }} pcbX={-14.5} pcbY={-10.2} />
    <capacitor name="C2" capacitance="10uF" footprint="1206" manufacturerPartNumber="GRM31CR71C106KA12L" mfn="Murata" pcbX={-10} pcbY={-10} />
    <capacitor name="C3" capacitance="100nF" footprint="0805" manufacturerPartNumber="GRM21BR71H104KA01L" mfn="Murata" pcbX={-5.7} pcbY={-10} />
    <chip name="LED1" displayName="POWER GREEN" manufacturerPartNumber="L-934GD" mfn="Kingbright" footprint={led3mmFootprint}
      pinLabels={{ pin1: "K", pin2: "A" }} schPinArrangement={{ leftSide: ["pin2"], rightSide: ["pin1"] }} pcbX={-5.2} pcbY={16.7} />
    <resistor name="R17" resistance="2.2k" footprint="0805" manufacturerPartNumber="RC0805FR-072K2L" mfn="Yageo" pcbX={-6.7} pcbY={13.5} pcbRotation={90} />

    {/* External sensor filtering and threshold. */}
    <resistor name="R18" resistance="100k" footprint="0805" manufacturerPartNumber="RC0805FR-07100KL" mfn="Yageo" pcbX={-18.5} pcbY={10.5} pcbRotation={90} />
    <resistor name="R1" resistance="10k" footprint="0805" manufacturerPartNumber="RC0805FR-0710KL" mfn="Yageo" pcbX={-15.7} pcbY={8.8} />
    <capacitor name="C5" capacitance="1uF" footprint="0805" manufacturerPartNumber="GRM21BR71C105KA01L" mfn="Murata" pcbX={-12.3} pcbY={9} pcbRotation={90} />
    <capacitor name="C12" capacitance="100nF" footprint="0805" manufacturerPartNumber="GRM21BR71H104KA01L" mfn="Murata" pcbX={-18} pcbY={13.3} />
    <resistor name="R2" resistance="7.5k" footprint="0805" manufacturerPartNumber="RC0805FR-077K5L" mfn="Yageo" pcbX={-9.5} pcbY={11.5} pcbRotation={90} />
    <chip name="RV1" displayName="THRESH 2k" manufacturerPartNumber="3296W-1-202LF" mfn="Bourns" footprint={trimmer3296wFootprint("CW MORE→3")}
      pinLabels={{ pin1: "LOW", pin2: "WIPER", pin3: "HIGH" }} schPinArrangement={{ leftSide: ["pin1"], rightSide: ["pin3"], bottomSide: ["pin2"] }} pcbX={-5.2} pcbY={10.1} />
    <resistor name="R3" resistance="7.5k" footprint="0805" manufacturerPartNumber="RC0805FR-077K5L" mfn="Yageo" pcbX={-0.8} pcbY={13.4} />
    <resistor name="R19" resistance="220k" footprint="0805" manufacturerPartNumber="RC0805FR-07220KL" mfn="Yageo" pcbX={-4} pcbY={6.6} />

    {/* Dual comparator and detector output. */}
    <chip name="U1" displayName="TLV1822-Q1" manufacturerPartNumber="TLV1822QDRQ1" mfn="Texas Instruments" footprint={u1TiD0008AFootprint}
      pinLabels={{ pin1: "DET_N", pin2: "ACS_FILTER", pin3: "VTH", pin4: "GND", pin5: "VDELAY", pin6: "HOLD", pin7: "TIMER_N", pin8: "PLUS_5V_LOGIC" }}
      schPinArrangement={{ leftSide: ["pin3", "pin2", "pin5", "pin6"], rightSide: ["pin1", "pin7"], topSide: ["pin8"], bottomSide: ["pin4"] }}
      pcbX={-9} pcbY={1.5} pcbRotation={90} />
    <capacitor name="C4" capacitance="100nF" footprint="0805" manufacturerPartNumber="GRM21BR71H104KA01L" mfn="Murata" pcbX={-13} pcbY={-1} pcbRotation={90} />
    <resistor name="R4" resistance="10k" footprint="0805" manufacturerPartNumber="RC0805FR-0710KL" mfn="Yageo" pcbX={-14} pcbY={6.2} />
    <resistor name="R5" resistance="4.7M" footprint="0805" manufacturerPartNumber="RC0805FR-074M7L" mfn="Yageo" pcbX={-13.5} pcbY={3.2} pcbRotation={90} />
    <resistor name="R22" resistance="4.7M" footprint="0805" manufacturerPartNumber="RC0805FR-074M7L" mfn="Yageo" doNotPlace={true} pcbX={-16} pcbY={3.2} pcbRotation={90} />
    <resistor name="R6" resistance="2.2k" footprint="0805" manufacturerPartNumber="RC0805FR-072K2L" mfn="Yageo" pcbX={-3.5} pcbY={13.3} pcbRotation={90} />
    <chip name="LED2" displayName="GUN YELLOW" manufacturerPartNumber="L-934YD" mfn="Kingbright" footprint={led3mmFootprint}
      pinLabels={{ pin1: "K", pin2: "A" }} schPinArrangement={{ leftSide: ["pin2"], rightSide: ["pin1"] }} pcbX={0} pcbY={16.7} />

    {/* VMID and HOLD fast-charge stage. */}
    <resistor name="R7" resistance="4.7k" footprint="0805" manufacturerPartNumber="RC0805FR-074K7L" mfn="Yageo" pcbX={-5} pcbY={3} pcbRotation={90} />
    <resistor name="R8" resistance="4.7k" footprint="0805" manufacturerPartNumber="RC0805FR-074K7L" mfn="Yageo" pcbX={-5} pcbY={-1.2} pcbRotation={90} />
    <capacitor name="C6" capacitance="22uF" footprint="1210" manufacturerPartNumber="C3225X7R1E226M250AB" mfn="TDK" pcbX={-1.5} pcbY={0.5} />
    <chip name="Q1" displayName="DMP2065UQ P-MOS" manufacturerPartNumber="DMP2065UQ-7" mfn="Diodes Incorporated" footprint="sot23"
      pinLabels={{ pin1: "GATE", pin2: "SOURCE", pin3: "DRAIN" }} schPinArrangement={{ leftSide: ["pin1"], topSide: ["pin2"], rightSide: ["pin3"] }} pcbX={-1.5} pcbY={4.5} pcbRotation={90} />
    <resistor name="R20" resistance="2.2k" footprint="0805" manufacturerPartNumber="RC0805FR-072K2L" mfn="Yageo" pcbX={2} pcbY={4.5} />

    {/* Timer, true Schmitt feedback, and fail-safe decay. */}
    <capacitor name="C7" capacitance="6.8uF" footprint="1206" manufacturerPartNumber="CGA5L1X7R1E685K160AC" mfn="TDK" pcbX={5.3} pcbY={2.2} pcbRotation={90} />
    <resistor name="R21" resistance="1M" footprint="0805" manufacturerPartNumber="RC0805FR-071ML" mfn="Yageo" pcbX={7.5} pcbY={5.8} pcbRotation={90} />
    <resistor name="R9" resistance="10k" footprint="0805" manufacturerPartNumber="RC0805FR-0710KL" mfn="Yageo" pcbX={10.5} pcbY={7.5} />
    <chip name="RV2" displayName="DELAY 100k" manufacturerPartNumber="3296W-1-104LF" mfn="Bourns" footprint={trimmer3296wFootprint("CW LONGER→3")}
      pinLabels={{ pin1: "LOW", pin2: "WIPER", pin3: "HIGH" }} schPinArrangement={{ leftSide: ["pin1"], rightSide: ["pin3"], bottomSide: ["pin2"] }} pcbX={6.2} pcbY={10.1} />
    <resistor name="R10" resistance="39k" footprint="0805" manufacturerPartNumber="RC0805FR-0739KL" mfn="Yageo" pcbX={2.5} pcbY={-2.5} />
    <resistor name="R11" resistance="10k" footprint="0805" manufacturerPartNumber="RC0805FR-0710KL" mfn="Yageo" pcbX={5.5} pcbY={-3.5} pcbRotation={90} />
    <capacitor name="C8" capacitance="100nF" footprint="0805" manufacturerPartNumber="GRM21BR71H104KA01L" mfn="Murata" pcbX={7.7} pcbY={-3.5} pcbRotation={90} />
    <resistor name="R12" resistance="10k" footprint="0805" manufacturerPartNumber="RC0805FR-0710KL" mfn="Yageo" pcbX={-1.8} pcbY={-4.3} />
    <resistor name="R13" resistance="4.7M" footprint="0805" manufacturerPartNumber="RC0805FR-074M7L" mfn="Yageo" pcbX={-1} pcbY={-2.3} />

    {/* Supply supervisor: holds HOLD below VDELAY until 5 V is valid. */}
    <chip name="U2" displayName="4.38V / 200ms RESET" manufacturerPartNumber="TLV803EA43DBZR" mfn="Texas Instruments" footprint="sot23"
      pinLabels={{ pin1: "GND", pin2: "RESET_N", pin3: "PLUS_5V_LOGIC" }} schPinArrangement={{ leftSide: ["pin3"], rightSide: ["pin2"], bottomSide: ["pin1"] }} pcbX={8.5} pcbY={1} pcbRotation={180} />
    <capacitor name="C11" capacitance="100nF" footprint="0805" manufacturerPartNumber="GRM21BR71H104KA01L" mfn="Murata" pcbX={12.5} pcbY={1} pcbRotation={90} />
    <resistor name="R23" resistance="560" footprint="0805" manufacturerPartNumber="RC0805FR-07560RL" mfn="Yageo" pcbX={10.5} pcbY={4.8} />

    {/* Fail-off gate source and low-side pump switch. */}
    <chip name="Q3" displayName="DMP2065UQ P-MOS" manufacturerPartNumber="DMP2065UQ-7" mfn="Diodes Incorporated" footprint="sot23"
      pinLabels={{ pin1: "GATE", pin2: "SOURCE", pin3: "DRAIN" }} schPinArrangement={{ leftSide: ["pin1"], topSide: ["pin2"], rightSide: ["pin3"] }} pcbX={0} pcbY={-7} pcbRotation={0} />
    <resistor name="R14" resistance="100" footprint="0805" manufacturerPartNumber="RC0805FR-07100RL" mfn="Yageo" pcbX={3.8} pcbY={-7} />
    <resistor name="R15" resistance="10k" footprint="0805" manufacturerPartNumber="RC0805FR-0710KL" mfn="Yageo" pcbX={6.7} pcbY={-8} pcbRotation={90} />
    <capacitor name="C10" capacitance="100nF" footprint="0805" manufacturerPartNumber="GRM21BR71H104KA01L" mfn="Murata" pcbX={10} pcbY={-5} pcbRotation={90} />
    <chip name="Q2" displayName="AO3400A N-MOS" manufacturerPartNumber="AO3400A" mfn="Alpha & Omega Semiconductor" footprint="sot23"
      pinLabels={{ pin1: "GATE", pin2: "SOURCE", pin3: "DRAIN" }} schPinArrangement={{ leftSide: ["pin1"], bottomSide: ["pin2"], rightSide: ["pin3"] }} pcbX={11.8} pcbY={-10} pcbRotation={180} />
    <chip name="D1" displayName="3A 40V SMA" manufacturerPartNumber="B340A-E3/61T" mfn="Vishay" footprint={smaDiodeFootprint}
      pinLabels={{ pin1: "CATHODE", pin2: "ANODE" }} schPinArrangement={{ leftSide: ["pin2"], rightSide: ["pin1"] }} pcbX={15.5} pcbY={-10.5} pcbRotation={90} />
    <capacitor name="C9" capacitance="100nF" footprint="0805" manufacturerPartNumber="GRM21BR71H104KA01L" mfn="Murata" pcbX={18} pcbY={-10} pcbRotation={90} />
    <fuse name="F1" displayName="1.5A PTC" currentRating="1.5A" manufacturerPartNumber="1812L150/16DR" mfn="Littelfuse" footprint={ptc1812Footprint} pcbX={7.2} pcbY={-15.2} />
    <resistor name="R16" resistance="2.2k" footprint="0805" manufacturerPartNumber="RC0805FR-072K2L" mfn="Yageo" pcbX={3} pcbY={13.3} pcbRotation={90} />
    <chip name="LED3" displayName="PUMP RED" manufacturerPartNumber="L-934ID" mfn="Kingbright" footprint={led3mmFootprint}
      pinLabels={{ pin1: "K", pin2: "A" }} schPinArrangement={{ leftSide: ["pin2"], rightSide: ["pin1"] }} pcbX={5.2} pcbY={16.7} />

    {/* PRIME: physical left pair (1,2) and right pair (3,4) are common. */}
    <chip name="SW1" displayName="PRIME" manufacturerPartNumber="B3F-1000" mfn="Omron" footprint={switchB3fFootprint}
      pinLabels={{ pin1: "A1", pin2: "A2", pin3: "B1", pin4: "B2" }} internallyConnectedPins={[["pin1", "pin2"], ["pin3", "pin4"]]}
      schPinArrangement={{ leftSide: ["pin1", "pin2"], rightSide: ["pin3", "pin4"] }} pcbX={14.7} pcbY={12.4} />

    {/* Through-hole probe loops / mini-grabber points. */}
    <testpoint name="TP1" displayName="+5V_PUMP" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-18.2} pcbY={-13} />
    <testpoint name="TP2" displayName="+5V_LOGIC" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-15.8} pcbY={-8.2} />
    <testpoint name="TP3" displayName="GND" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-18.2} pcbY={-8.2} />
    <testpoint name="TP4" displayName="ACS_OUT" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-20} pcbY={7.6} />
    <testpoint name="TP5" displayName="ACS_FILTER" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-16.8} pcbY={6.3} />
    <testpoint name="TP6" displayName="VTH" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-8.5} pcbY={7.2} />
    <testpoint name="TP7" displayName="DET_N" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-19} pcbY={1} />
    <testpoint name="TP8" displayName="VMID" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-5} pcbY={-4.8} />
    <testpoint name="TP9" displayName="HOLD" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={3.5} pcbY={7.2} />
    <testpoint name="TP10" displayName="VDELAY" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={14} pcbY={-2.5} />
    <testpoint name="TP11" displayName="PUMP_GATE" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={12.5} pcbY={-5.5} />
    <testpoint name="TP12" displayName="PUMP_SW_NEG" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={18.5} pcbY={-6.8} />
    <testpoint name="TP13" displayName="GND" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={15} pcbY={5.5} />
    <testpoint name="TP14" displayName="TIMER_N" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={-5.5} pcbY={-7.2} />
    <testpoint name="TP15" displayName="PUMP_PLUS" footprintVariant="through_hole" holeDiameter="1mm" padDiameter="2mm" pcbX={11.8} pcbY={-12.7} />

    {/* Equivalent explicit net trees for deterministic KRT routing. */}
    {routingTrees.flatMap(({ name, edges }) =>
      edges.map(([from, to, thickness, pcbStraightLine, pcbPath], index) => (
        <trace key={`${name}_${index}`} name={`T_${name}_${index}`} from={from} to={to} thickness={thickness}
          pcbStraightLine={pcbStraightLine} pcbPath={pcbPath} />
      )),
    )}

    {/* Two-terminal nodes that are not members of a named tree. */}
    <trace name="T_R17_LED1" from=".R17 > .pin2" to=".LED1 > .pin2" />
    <trace name="T_R2_RV1" from=".R2 > .pin2" to=".RV1 > .pin3" />
    <trace name="T_RV1_LOW" from=".RV1 > .pin1" to=".R3 > .pin1" />
    <trace name="T_R19_H" from=".R19 > .pin2" to=".RV1 > .pin3" />
    <trace name="T_R6_LED2" from=".R6 > .pin2" to=".LED2 > .pin2" />
    <trace name="T_Q1_D" from=".Q1 > .pin3" to=".R20 > .pin1" />
    <trace name="T_R9_RV2" from=".R9 > .pin2" to=".RV2 > .pin3" />
    <trace name="T_RV2_W3" from=".RV2 > .pin2" to=".RV2 > .pin3" />
    <trace name="T_U2_R" from=".U2 > .pin2" to=".R23 > .pin1" />
    <trace name="T_Q3_D" from=".Q3 > .pin3" to=".R14 > .pin1" />
    <trace name="T_R16_LED3" from=".R16 > .pin2" to=".LED3 > .pin2" />

    {/* Archived implicit-net representation, retained only as an audit aid. */}
    {false ? <>
    <trace name="T_J1_PUMP" from=".J1 > .pin1" to="net.PLUS_5V_PUMP" thickness="1.2mm" />
    <trace name="T_J1_GND" from=".J1 > .pin2" to="net.GND" thickness="1.2mm" />
    <trace name="T_C1_POS" from=".C1 > .pin1" to="net.PLUS_5V_PUMP" thickness="1mm" />
    <trace name="T_C1_NEG" from=".C1 > .pin2" to="net.GND" thickness="1mm" />
    <trace name="T_FB1_IN" from=".FB1 > .pin1" to="net.PLUS_5V_PUMP" />
    <trace name="T_FB1_OUT" from=".FB1 > .pin2" to="net.PLUS_5V_LOGIC" />
    <trace name="T_C2_P" from=".C2 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_C2_G" from=".C2 > .pin2" to="net.GND" />
    <trace name="T_C3_P" from=".C3 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_C3_G" from=".C3 > .pin2" to="net.GND" />
    <trace name="T_R17_P" from=".R17 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R17_LED1" from=".R17 > .pin2" to=".LED1 > .pin2" />
    <trace name="T_LED1_G" from=".LED1 > .pin1" to="net.GND" />

    <trace name="T_J2_V" from=".J2 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_J2_G" from=".J2 > .pin2" to="net.GND" />
    <trace name="T_J2_O" from=".J2 > .pin3" to="net.ACS_OUT" />
    <trace name="T_R18_O" from=".R18 > .pin1" to="net.ACS_OUT" />
    <trace name="T_R18_G" from=".R18 > .pin2" to="net.GND" />
    <trace name="T_R1_O" from=".R1 > .pin1" to="net.ACS_OUT" />
    <trace name="T_R1_F" from=".R1 > .pin2" to="net.ACS_FILTER" />
    <trace name="T_C5_F" from=".C5 > .pin1" to="net.ACS_FILTER" />
    <trace name="T_C5_G" from=".C5 > .pin2" to="net.GND" />
    <trace name="T_C12_V" from=".C12 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_C12_G" from=".C12 > .pin2" to="net.GND" />

    <trace name="T_R2_V" from=".R2 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R2_RV1" from=".R2 > .pin2" to=".RV1 > .pin3" />
    <trace name="T_RV1_LOW" from=".RV1 > .pin1" to=".R3 > .pin1" />
    <trace name="T_R3_G" from=".R3 > .pin2" to="net.GND" />
    <trace name="T_RV1_W" from=".RV1 > .pin2" to="net.VTH" />
    <trace name="T_R19_W" from=".R19 > .pin1" to="net.VTH" />
    <trace name="T_R19_H" from=".R19 > .pin2" to=".RV1 > .pin3" />

    <trace name="T_U1_1" from=".U1 > .pin1" to="net.DET_N" />
    <trace name="T_U1_2" from=".U1 > .pin2" to="net.ACS_FILTER" />
    <trace name="T_U1_3" from=".U1 > .pin3" to="net.VTH" />
    <trace name="T_U1_4" from=".U1 > .pin4" to="net.GND" />
    <trace name="T_U1_5" from=".U1 > .pin5" to="net.VDELAY" />
    <trace name="T_U1_6" from=".U1 > .pin6" to="net.HOLD" />
    <trace name="T_U1_7" from=".U1 > .pin7" to="net.TIMER_N" />
    <trace name="T_U1_8" from=".U1 > .pin8" to="net.PLUS_5V_LOGIC" />
    <trace name="T_C4_V" from=".C4 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_C4_G" from=".C4 > .pin2" to="net.GND" />
    <trace name="T_R4_V" from=".R4 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R4_D" from=".R4 > .pin2" to="net.DET_N" />
    <trace name="T_R5_D" from=".R5 > .pin1" to="net.DET_N" />
    <trace name="T_R5_T" from=".R5 > .pin2" to="net.VTH" />
    <trace name="T_R22_D" from=".R22 > .pin1" to="net.DET_N" />
    <trace name="T_R22_T" from=".R22 > .pin2" to="net.VTH" />
    <trace name="T_R6_V" from=".R6 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R6_LED2" from=".R6 > .pin2" to=".LED2 > .pin2" />
    <trace name="T_LED2_D" from=".LED2 > .pin1" to="net.DET_N" />

    <trace name="T_R7_V" from=".R7 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R7_M" from=".R7 > .pin2" to="net.VMID" />
    <trace name="T_R8_M" from=".R8 > .pin1" to="net.VMID" />
    <trace name="T_R8_G" from=".R8 > .pin2" to="net.GND" />
    <trace name="T_C6_M" from=".C6 > .pin1" to="net.VMID" />
    <trace name="T_C6_G" from=".C6 > .pin2" to="net.GND" />
    <trace name="T_Q1_G" from=".Q1 > .pin1" to="net.DET_N" />
    <trace name="T_Q1_S" from=".Q1 > .pin2" to="net.VMID" />
    <trace name="T_Q1_D" from=".Q1 > .pin3" to=".R20 > .pin1" />
    <trace name="T_R20_H" from=".R20 > .pin2" to="net.HOLD" />

    <trace name="T_C7_H" from=".C7 > .pin1" to="net.HOLD" />
    <trace name="T_C7_G" from=".C7 > .pin2" to="net.GND" />
    <trace name="T_R21_H" from=".R21 > .pin1" to="net.HOLD" />
    <trace name="T_R21_G" from=".R21 > .pin2" to="net.GND" />
    <trace name="T_R9_H" from=".R9 > .pin1" to="net.HOLD" />
    <trace name="T_R9_RV2" from=".R9 > .pin2" to=".RV2 > .pin3" />
    <trace name="T_RV2_W3" from=".RV2 > .pin2" to=".RV2 > .pin3" />
    <trace name="T_RV2_G" from=".RV2 > .pin1" to="net.GND" />
    <trace name="T_R10_V" from=".R10 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R10_D" from=".R10 > .pin2" to="net.VDELAY" />
    <trace name="T_R11_D" from=".R11 > .pin1" to="net.VDELAY" />
    <trace name="T_R11_G" from=".R11 > .pin2" to="net.GND" />
    <trace name="T_C8_D" from=".C8 > .pin1" to="net.VDELAY" />
    <trace name="T_C8_G" from=".C8 > .pin2" to="net.GND" />
    <trace name="T_R12_V" from=".R12 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R12_T" from=".R12 > .pin2" to="net.TIMER_N" />
    <trace name="T_R13_T" from=".R13 > .pin1" to="net.TIMER_N" />
    <trace name="T_R13_D" from=".R13 > .pin2" to="net.VDELAY" />

    <trace name="T_U2_G" from=".U2 > .pin1" to="net.GND" />
    <trace name="T_U2_R" from=".U2 > .pin2" to=".R23 > .pin1" />
    <trace name="T_U2_V" from=".U2 > .pin3" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R23_H" from=".R23 > .pin2" to="net.HOLD" />
    <trace name="T_C11_V" from=".C11 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_C11_G" from=".C11 > .pin2" to="net.GND" />

    <trace name="T_Q3_G" from=".Q3 > .pin1" to="net.TIMER_N" />
    <trace name="T_Q3_S" from=".Q3 > .pin2" to="net.PLUS_5V_LOGIC" />
    <trace name="T_Q3_D" from=".Q3 > .pin3" to=".R14 > .pin1" />
    <trace name="T_R14_GATE" from=".R14 > .pin2" to="net.PUMP_GATE" />
    <trace name="T_R15_GATE" from=".R15 > .pin1" to="net.PUMP_GATE" />
    <trace name="T_R15_G" from=".R15 > .pin2" to="net.GND" />
    <trace name="T_C10_GATE" from=".C10 > .pin1" to="net.PUMP_GATE" />
    <trace name="T_C10_G" from=".C10 > .pin2" to="net.GND" />
    <trace name="T_Q2_G" from=".Q2 > .pin1" to="net.PUMP_GATE" />
    <trace name="T_Q2_S" from=".Q2 > .pin2" to="net.GND" thickness="1.2mm" />
    <trace name="T_Q2_D" from=".Q2 > .pin3" to="net.PUMP_SW_NEG" thickness="1.2mm" />
    <trace name="T_F1_IN" from=".F1 > .pin1" to="net.PLUS_5V_PUMP" thickness="1.2mm" />
    <trace name="T_F1_OUT" from=".F1 > .pin2" to="net.PUMP_PLUS" thickness="1.2mm" />
    <trace name="T_J3_P" from=".J3 > .pin1" to="net.PUMP_PLUS" thickness="1.2mm" />
    <trace name="T_J3_N" from=".J3 > .pin2" to="net.PUMP_SW_NEG" thickness="1.2mm" />
    <trace name="T_D1_K" from=".D1 > .pin1" to="net.PUMP_PLUS" thickness="1mm" />
    <trace name="T_D1_A" from=".D1 > .pin2" to="net.PUMP_SW_NEG" thickness="1mm" />
    <trace name="T_C9_P" from=".C9 > .pin1" to="net.PUMP_PLUS" />
    <trace name="T_C9_N" from=".C9 > .pin2" to="net.PUMP_SW_NEG" />
    <trace name="T_R16_P" from=".R16 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_R16_LED3" from=".R16 > .pin2" to=".LED3 > .pin2" />
    <trace name="T_LED3_N" from=".LED3 > .pin1" to="net.TIMER_N" />

    <trace name="T_SW_A" from=".SW1 > .pin1" to="net.DET_N" />
    <trace name="T_SW_B" from=".SW1 > .pin3" to="net.GND" />
    <trace name="T_J4_D" from=".J4 > .pin1" to="net.DET_N" />
    <trace name="T_J4_G" from=".J4 > .pin2" to="net.GND" />
    <trace name="T_TP1" from=".TP1 > .pin1" to="net.PLUS_5V_PUMP" thickness="1mm" />
    <trace name="T_TP2" from=".TP2 > .pin1" to="net.PLUS_5V_LOGIC" />
    <trace name="T_TP3" from=".TP3 > .pin1" to="net.GND" />
    <trace name="T_TP4" from=".TP4 > .pin1" to="net.ACS_OUT" />
    <trace name="T_TP5" from=".TP5 > .pin1" to="net.ACS_FILTER" />
    <trace name="T_TP6" from=".TP6 > .pin1" to="net.VTH" />
    <trace name="T_TP7" from=".TP7 > .pin1" to="net.DET_N" />
    <trace name="T_TP8" from=".TP8 > .pin1" to="net.VMID" />
    <trace name="T_TP9" from=".TP9 > .pin1" to="net.HOLD" />
    <trace name="T_TP10" from=".TP10 > .pin1" to="net.VDELAY" />
    <trace name="T_TP11" from=".TP11 > .pin1" to="net.PUMP_GATE" />
    <trace name="T_TP12" from=".TP12 > .pin1" to="net.PUMP_SW_NEG" thickness="1mm" />
    <trace name="T_TP13" from=".TP13 > .pin1" to="net.GND" />
    <trace name="T_TP14" from=".TP14 > .pin1" to="net.TIMER_N" />
    <trace name="T_TP15" from=".TP15 > .pin1" to="net.PUMP_PLUS" thickness="1mm" />

    {/* Ground planes are intentionally kept off the top quiet-node region. */}
    <copperpour name="GND_BOTTOM" connectsTo="net.GND" layer="bottom" clearance="0.25mm" boardEdgeMargin="0.50mm" />
    <copperpour name="GND_TOP_QUIET" connectsTo="net.GND" layer="top" clearance="0.25mm" boardEdgeMargin="0.50mm"
      outline={[{x:-19,y:-9},{x:7.5,y:-9},{x:7.5,y:8},{x:-19,y:8}]} />
    </> : null}

    {/* Human-facing fabrication marks. */}
    <silkscreentext text="BubbleLink CTRL v1.1" pcbX={0} pcbY={-18.6} fontSize="1.1mm" />
    <silkscreentext text="DATE 2026-08-07" pcbX={0} pcbY={-17.1} fontSize="0.7mm" />
    <silkscreentext text="5 V ONLY" pcbX={-13.8} pcbY={-12.4} fontSize="1mm" />
    <silkscreentext text="POWER" pcbX={-5.2} pcbY={18.7} fontSize="0.8mm" />
    <silkscreentext text="GUN" pcbX={0} pcbY={18.7} fontSize="0.8mm" />
    <silkscreentext text="PUMP" pcbX={5.2} pcbY={18.7} fontSize="0.8mm" />
    <silkscreentext text="THRESH" pcbX={-5.2} pcbY={6.8} fontSize="0.8mm" />
    <silkscreentext text="DELAY" pcbX={6.2} pcbY={6.8} fontSize="0.8mm" />
    <silkscreentext text="PRIME" pcbX={14.7} pcbY={8.5} fontSize="0.9mm" />
    <silkscreentext text="J1 +5 G" pcbX={-14.3} pcbY={-18.2} fontSize="0.8mm" />
    <silkscreentext text="J2 OUT G +5" pcbX={-13.8} pcbY={11.8} fontSize="0.75mm" />
    <silkscreentext text="J3 +  -SW" pcbX={14.3} pcbY={-18.2} fontSize="0.8mm" />
    <silkscreentext text="F1 PUMP PTC" pcbX={7.2} pcbY={-12.7} fontSize="0.75mm" />
    <silkscreentext text="D1 K→PUMP+" pcbX={15.5} pcbY={-6.8} fontSize="0.75mm" />
  </board>
)
