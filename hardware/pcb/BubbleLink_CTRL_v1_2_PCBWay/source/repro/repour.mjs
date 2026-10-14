import fs from "node:fs"
import {
  CopperPourPipelineSolver,
  convertCircuitJsonToInputProblem,
  initializeManifoldGeometry,
} from "@tscircuit/copper-pour-solver"

const [inputPath, outputPath] = process.argv.slice(2)
if (!inputPath || !outputPath) throw new Error("usage: add_bottom_ground_pour.mjs <input> <output>")
let circuit = JSON.parse(fs.readFileSync(inputPath, "utf8"))
circuit = circuit.filter((e) => e.type !== "pcb_copper_pour")

const gndTrace = circuit.find((e) => e.type === "source_trace" && e.name === "T_GND_0")
if (!gndTrace?.subcircuit_connectivity_map_key) throw new Error("GND connectivity key missing")

await initializeManifoldGeometry()
const options = {
  layer: "bottom",
  subcircuit_id: gndTrace.subcircuit_id,
  subcircuit_connectivity_map_key: gndTrace.subcircuit_connectivity_map_key,
  pad_margin: 0.25,
  trace_margin: 0.25,
  board_edge_margin: 0.5,
  // The board declares a 3.00 mm radius copper keepout around each 3.20 mm
  // NPTH mounting hole. A 1.60 mm solver margin creates a nominal 3.20 mm
  // cutout and remains >3.00 mm after polygonal approximation.
  cutout_margin: 1.60,
}
const problem = convertCircuitJsonToInputProblem(circuit, options)
const { brep_shapes: shapes } = new CopperPourPipelineSolver(problem).getOutput()

function pointInRing(point, vertices) {
  let inside = false
  for (let i = 0, j = vertices.length - 1; i < vertices.length; j = i++) {
    const a = vertices[i], b = vertices[j]
    if ((a.y > point.y) !== (b.y > point.y) &&
        point.x < ((b.x - a.x) * (point.y - a.y)) / (b.y - a.y) + a.x) inside = !inside
  }
  return inside
}
function pointInShape(point, shape) {
  return pointInRing(point, shape.outer_ring.vertices) &&
    !shape.inner_rings.some((ring) => pointInRing(point, ring.vertices))
}

const gndPcbTrace = circuit.find((e) => e.type === "pcb_trace" && e.source_trace_id === gndTrace.source_trace_id)
if (!gndPcbTrace) throw new Error("GND PCB trace missing")
const requiredBottomPoints = gndPcbTrace.route
  .filter((p) => p.route_type === "wire" && p.layer === "bottom")
  .map(({ x, y }) => ({ x, y }))
const connectedShape = shapes.find((shape) => requiredBottomPoints.every((point) => pointInShape(point, shape)))
if (!connectedShape) throw new Error("no single bottom GND pour contains the complete high-current return")

const pours = [connectedShape].map((brep_shape, index) => ({
  type: "pcb_copper_pour",
  shape: "brep",
  pcb_copper_pour_id: `pcb_copper_pour_gnd_bottom_${index}`,
  layer: "bottom",
  subcircuit_id: gndTrace.subcircuit_id,
  subcircuit_connectivity_map_key: gndTrace.subcircuit_connectivity_map_key,
  brep_shape,
  covered_with_solder_mask: true,
}))

fs.writeFileSync(outputPath, `${JSON.stringify([...circuit, ...pours], null, 2)}\n`)
console.log(JSON.stringify({
  gnd_key: gndTrace.subcircuit_connectivity_map_key,
  solver_shapes: shapes.length,
  emitted_shapes: pours.length,
  vertices: connectedShape.outer_ring.vertices.length,
  holes: connectedShape.inner_rings.length,
  required_bottom_points: requiredBottomPoints.length,
  options,
}, null, 2))
