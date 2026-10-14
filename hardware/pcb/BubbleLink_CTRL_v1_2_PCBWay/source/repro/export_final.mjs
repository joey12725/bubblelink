#!/usr/bin/env node
import fs from "node:fs/promises"
import path from "node:path"
import crypto from "node:crypto"
import {
  convertSoupToExcellonDrillCommandLayers,
  convertSoupToGerberCommands,
  stringifyExcellonDrill,
  stringifyGerberCommandLayers,
} from "circuit-json-to-gerber"
import {
  CircuitJsonToKicadPcbConverter,
  CircuitJsonToKicadProConverter,
  CircuitJsonToKicadSchConverter,
} from "circuit-json-to-kicad"
import {
  convertCircuitJsonToAssemblySvg,
  convertCircuitJsonToPcbSvg,
  convertCircuitJsonToSchematicSvg,
} from "circuit-to-svg"

const [inputPath, outputRoot] = process.argv.slice(2)
if (!inputPath || !outputRoot) throw new Error("usage: export_final.mjs <final.circuit.json> <output-root>")
const circuit = JSON.parse(await fs.readFile(inputPath, "utf8"))
const gerberDir = path.join(outputRoot, "fabrication", "gerber_unpacked")
const sourceDir = path.join(outputRoot, "source")
const drawingsDir = path.join(outputRoot, "drawings")
// Start clean so removed layers cannot survive as stale files in a later ZIP.
await fs.rm(gerberDir, { recursive: true, force: true })
await Promise.all([gerberDir, sourceDir, drawingsDir].map((dir) => fs.mkdir(dir, { recursive: true })))

const gerberCommands = convertSoupToGerberCommands(circuit)
const drillCommands = convertSoupToExcellonDrillCommandLayers({ circuitJson: circuit })
const gerbers = stringifyGerberCommandLayers(gerberCommands)
const drills = Object.fromEntries(Object.entries(drillCommands).map(([name, commands]) => [name, stringifyExcellonDrill(commands)]))

// circuit-json-to-gerber 0.0.89 emits circular PTH annuli as paste flashes and
// scales every real SMT aperture to 70% in each axis. Regenerate F.Paste from
// the copper-pad geometry so the Gerber agrees with the KiCad source: 1:1 pad
// dimensions, top side only, and no aperture for the explicit DNP R22.
const sourceById = new Map(
  circuit
    .filter((e) => e.type === "source_component")
    .map((e) => [e.source_component_id, e]),
)
const dnpNames = new Set(["R22", "J4"])
const dnpPcbComponentIds = new Set(
  circuit
    .filter((e) => e.type === "pcb_component")
    .filter((e) => dnpNames.has(sourceById.get(e.source_component_id)?.name))
    .map((e) => e.pcb_component_id),
)
const intendedPastePads = circuit
  .filter(
    (e) =>
      e.type === "pcb_smtpad" &&
      e.layer === "top" &&
      e.pcb_component_id != null &&
      !dnpPcbComponentIds.has(e.pcb_component_id),
  )
  .sort((a, b) => a.y - b.y || a.x - b.x || a.width - b.width || a.height - b.height)

if (intendedPastePads.length !== 92) {
  throw new Error(`expected 92 populated top SMT pads, found ${intendedPastePads.length}`)
}
if (intendedPastePads.some((pad) => pad.shape !== "rect" || !(pad.width > 0) || !(pad.height > 0))) {
  throw new Error("top paste generator currently requires positive rectangular pad geometry")
}

const apertureKeys = [...new Set(intendedPastePads.map((pad) => `${pad.width.toFixed(6)}X${pad.height.toFixed(6)}`))]
  .sort()
const dCodeByAperture = new Map(apertureKeys.map((key, index) => [key, index + 10]))
const formatCoord = (value) => `${Math.round(Number(value) * 1e6)}`
const generatedTopPaste = [
  "%TF.GenerationSoftware,Codex,BubbleLink-paste-generator,1.0*%",
  `%TF.CreationDate,${new Date().toISOString()}*%`,
  "%TF.SameCoordinates,Original*%",
  "%TF.FileFunction,Paste,Top*%",
  "%TF.FilePolarity,Positive*%",
  "%FSLAX46Y46*%",
  "%MOMM*%",
  "G04 BubbleLink top-only 1:1 SMT paste; DNP and PTH excluded*",
  "G01*",
  "%LPD*%",
  ...apertureKeys.map((key) => `%ADD${dCodeByAperture.get(key)}R,${key}*%`),
  ...intendedPastePads.flatMap((pad) => {
    const key = `${pad.width.toFixed(6)}X${pad.height.toFixed(6)}`
    return [`D${dCodeByAperture.get(key)}*`, `X${formatCoord(pad.x)}Y${formatCoord(pad.y)}D03*`]
  }),
  "M02*",
  "",
].join("\n")

const releaseGerbers = { ...gerbers, F_Paste: generatedTopPaste }
delete releaseGerbers.B_Paste
delete releaseGerbers.B_SilkScreen

for (const [name, content] of Object.entries(releaseGerbers)) await fs.writeFile(path.join(gerberDir, `${name}.gbr`), content)
for (const [name, content] of Object.entries(drills)) await fs.writeFile(path.join(gerberDir, name), content)

const projectName = "BubbleLink_CTRL_v1_2"
const pcb = new CircuitJsonToKicadPcbConverter(circuit, { projectName })
pcb.runUntilFinished()
const sch = new CircuitJsonToKicadSchConverter(circuit, { projectName })
sch.runUntilFinished()
const pro = new CircuitJsonToKicadProConverter(circuit, {
  projectName,
  schematicFilename: `${projectName}.kicad_sch`,
  pcbFilename: `${projectName}.kicad_pcb`,
})
pro.runUntilFinished()
await fs.writeFile(path.join(sourceDir, `${projectName}.kicad_pcb`), pcb.getOutputString())
await fs.writeFile(path.join(sourceDir, `${projectName}.kicad_sch`), sch.getOutputString())
await fs.writeFile(path.join(sourceDir, `${projectName}.kicad_pro`), pro.getOutputString())

await fs.writeFile(path.join(drawingsDir, `${projectName}_PCB.svg`), convertCircuitJsonToPcbSvg(circuit, { showErrorsInTextOverlay: false }))
// Assembly orientation is issued by make_drawings.py from numbered physical pads. Generic corner marks are omitted.
await fs.writeFile(path.join(drawingsDir, `${projectName}_Schematic.svg`), convertCircuitJsonToSchematicSvg(circuit))

const sha256 = (text) => crypto.createHash("sha256").update(text).digest("hex")
const allGerberFiles = [...Object.keys(releaseGerbers).map((name) => `${name}.gbr`), ...Object.keys(drills)]
const report = {
  input: path.resolve(inputPath),
  input_sha256: sha256(await fs.readFile(inputPath)),
  generated_at_utc: new Date().toISOString(),
  gerber_files: allGerberFiles.sort(),
  gerber_layer_count: Object.keys(releaseGerbers).length,
  drill_file_count: Object.keys(drills).length,
  assembly_side: "top-only",
  top_paste_pad_count: intendedPastePads.length,
  top_paste_scale_to_copper: 1,
  omitted_dnp_paste_pads: 2,
  rejected_generator_pth_paste_flashes: 31,
  omitted_layers: ["B_Paste.gbr", "B_SilkScreen.gbr"],
  pcb_trace_count: circuit.filter((e) => e.type === "pcb_trace").length,
  pcb_via_count: circuit.filter((e) => e.type === "pcb_via").length,
  pcb_copper_pour_count: circuit.filter((e) => e.type === "pcb_copper_pour").length,
  kicad_files: [`${projectName}.kicad_pcb`, `${projectName}.kicad_sch`, `${projectName}.kicad_pro`],
  drawing_files: [`${projectName}_PCB.svg`, `${projectName}_Schematic.svg`],
}
await fs.writeFile(path.join(outputRoot, "export_report.json"), `${JSON.stringify(report, null, 2)}\n`)
console.log(JSON.stringify(report, null, 2))
