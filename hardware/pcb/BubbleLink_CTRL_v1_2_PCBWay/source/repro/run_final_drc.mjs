#!/usr/bin/env node
import fs from "node:fs"
import crypto from "node:crypto"
import {
  checkDifferentNetViaSpacing,
  checkEachPcbPortConnectedToPcbTraces,
  checkEachPcbTraceNonOverlapping,
  checkPadPadClearance,
  checkPadTraceClearance,
  checkPcbComponentOverlap,
  checkPcbComponentsOutOfBoard,
  checkPcbTracesOutOfBoard,
  checkSameNetViaSpacing,
  checkSourceTracesHavePcbTraces,
  checkTracesAreContiguous,
  checkViaTraceClearance,
  checkViasInPads,
  checkViasOffBoard,
  runAllPlacementChecks,
  runAllRoutingChecks,
} from "@tscircuit/checks"

const [inputPath, outputPath] = process.argv.slice(2)
if (!inputPath || !outputPath) throw new Error("usage: run_final_drc.mjs <final.circuit.json> <report.json>")
const raw = fs.readFileSync(inputPath)
const circuit = JSON.parse(raw)
const clearance = { minClearance: 0.2 }
const checks = {
  source_traces_have_pcb_traces: checkSourceTracesHavePcbTraces(circuit),
  pcb_ports_connected: checkEachPcbPortConnectedToPcbTraces(circuit),
  trace_routes_contiguous: checkTracesAreContiguous(circuit),
  trace_overlap_clearance_0_20mm: checkEachPcbTraceNonOverlapping(circuit, clearance),
  pad_trace_clearance_0_20mm: checkPadTraceClearance(circuit, clearance),
  pad_pad_clearance_0_20mm: checkPadPadClearance(circuit, clearance),
  via_trace_clearance_0_20mm: checkViaTraceClearance(circuit, clearance),
  same_net_via_spacing_0_20mm: checkSameNetViaSpacing(circuit, clearance),
  different_net_via_spacing_0_20mm: checkDifferentNetViaSpacing(circuit, clearance),
  vias_in_smt_pads: checkViasInPads(circuit),
  footprint_overlap: checkPcbComponentOverlap(circuit),
  components_out_of_board: checkPcbComponentsOutOfBoard(circuit),
  traces_out_of_board: checkPcbTracesOutOfBoard(circuit),
  vias_out_of_board: checkViasOffBoard(circuit),
  aggregate_placement_including_courtyard_and_access: await runAllPlacementChecks(circuit),
  aggregate_routing: await runAllRoutingChecks(circuit),
}

const sourceById = new Map(circuit.filter((e) => e.type === "source_trace").map((e) => [e.source_trace_id, e]))
const widthViolations = []
for (const trace of circuit.filter((e) => e.type === "pcb_trace")) {
  const source = sourceById.get(trace.source_trace_id)
  const minimum = Number(source?.min_trace_thickness ?? 0)
  for (const point of trace.route ?? []) {
    if (point.route_type === "wire" && Number(point.width) + 1e-9 < minimum) {
      widthViolations.push({
        message: `${source?.name ?? trace.source_trace_id} width ${point.width}mm is below ${minimum}mm`,
        pcb_trace_id: trace.pcb_trace_id,
        source_trace_id: trace.source_trace_id,
      })
    }
  }
}
checks.per_source_trace_minimum_width = widthViolations
checks.embedded_circuit_error_records = circuit.filter((e) => String(e.type ?? "").endsWith("_error"))

const unconnectedCheckNames = new Set(["source_traces_have_pcb_traces", "pcb_ports_connected", "trace_routes_contiguous"])
const violations = []
const unconnected = []
for (const [check, errors] of Object.entries(checks)) {
  for (const error of errors) {
    const row = { check, message: error.message ?? error.error_type ?? error.type ?? "check failed", raw: error }
    ;(unconnectedCheckNames.has(check) ? unconnected : violations).push(row)
  }
}
const report = {
  schema: "BubbleLink final independent geometry/connectivity DRC v1",
  engine: "@tscircuit/checks plus explicit per-source width audit",
  note: "KiCad CLI is not installed in this environment; this is not represented as a KiCad-native DRC run. KiCad export reconciliation is performed separately by manufacturing_qa.",
  input_file: inputPath,
  circuit_json_sha256: crypto.createHash("sha256").update(raw).digest("hex"),
  minimum_clearance_mm: 0.2,
  violations,
  unconnected,
  check_counts: Object.fromEntries(Object.entries(checks).map(([name, errors]) => [name, errors.length])),
}
fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`)
console.log(JSON.stringify({ violations: violations.length, unconnected: unconnected.length, check_counts: report.check_counts }, null, 2))
if (violations.length || unconnected.length) process.exit(1)
