# BubbleLink

BubbleLink is a wearable, pack-fed bubble system for festivals. A backpack carries a 90 Wh 2S5P battery cartridge, a 1 L bubble-solution bladder, one shared peristaltic transfer pump, and the **BubbleLink CTRL** board, a small analog PCB that runs the pump automatically whenever a gun draws current. Hand-held bubble heads (mechanisms pulled from toy bubble guns, starting with Joey's existing overvolted three-head gun) plug into two channels through umbilicals that each carry XT30U power, a silicone fluid line, and a paracord tether.

This repo is the single source of truth for the project. It records the final design, the parts actually bought, the PCB release, and the build and test plan. It covers only what was chosen. Alternatives that were considered and dropped are left out on purpose.

**Status (2026-10-14):** parts on hand, controller PCBs in transit (ETA Oct 15–18), build not started. Target event: the target festival, Oct 30–31. → [Project status](docs/00-project-status.md)

## Start here

| If you want to… | Read |
|---|---|
| Get the whole design on one page | [docs/canonical-facts.md](docs/canonical-facts.md) |
| See what's done and what's next | [docs/00-project-status.md](docs/00-project-status.md) · [docs/11-open-items.md](docs/11-open-items.md) |
| Understand the project and its requirements | [docs/01-overview-and-requirements.md](docs/01-overview-and-requirements.md) |
| See how it all fits together | [docs/02-system-architecture.md](docs/02-system-architecture.md) |
| Know why something is the way it is | [docs/03-design-decisions.md](docs/03-design-decisions.md) |
| Look up a part you bought | [docs/parts/ORDER_LEDGER.md](docs/parts/ORDER_LEDGER.md) · [docs/parts/listings/](docs/parts/listings/) |
| Build it | [docs/10-build-guide.md](docs/10-build-guide.md) · [docs/09-printed-parts.md](docs/09-printed-parts.md) |
| Test it | [docs/13-test-plan.md](docs/13-test-plan.md) · [docs/07-pcb/bringup-and-acceptance-test.md](docs/07-pcb/bringup-and-acceptance-test.md) |

## Documentation map

**System**
- [Canonical facts](docs/canonical-facts.md): one-page verified summary; wins any conflict
- [00 Project status](docs/00-project-status.md): current state, PCB tracking, critical path
- [01 Overview and requirements](docs/01-overview-and-requirements.md): goals, use, requirements, MVP scope
- [02 System architecture](docs/02-system-architecture.md): power, fluid, and control paths; pack layout
- [03 Design decisions](docs/03-design-decisions.md): every final decision with its rationale

**Subsystems**
- [04 Power system](docs/04-power-system.md): 2S5P cartridge, BMS, USB-C charging, 30 A breaker, harness, 5 V bucks, voltmeter
- [05 Fluid system](docs/05-fluid-system.md): bladder, G528 pump, recirculating bypass, check valve, fittings, solution
- [06 Guns, heads and umbilicals](docs/06-guns-heads-and-umbilicals.md): donor heads, overvolting, umbilicals, connector bricks
- [07 Controller PCB (BubbleLink CTRL v1.2)](docs/07-pcb/overview.md)
  - [Connectors and pinout](docs/07-pcb/connectors-and-pinout.md)
  - [BOM and parts](docs/07-pcb/bom-and-parts.md)
  - [Fabrication and assembly](docs/07-pcb/fabrication-and-assembly.md)
  - [Bring-up and acceptance test](docs/07-pcb/bringup-and-acceptance-test.md)
  - [Revision history](docs/07-pcb/revision-history.md)
- [12 Wearable pack and cosplay](docs/12-wearable-pack-and-cosplay.md): LED pixel backpack, layout, Tracer cosplay

**Making it**
- [08 PCBWay order history](docs/08-manufacturing/pcbway-order-history.md)
- [09 Printed parts](docs/09-printed-parts.md)
- [10 Build guide](docs/10-build-guide.md)
- [13 Test plan](docs/13-test-plan.md)
- [14 Budget](docs/14-budget.md)

**Context**
- [15 Baseline gun and field history](docs/15-baseline-gun-and-field-history.md): the existing three-head gun, measurements, events
- [16 Roadmap / future extensions](docs/16-roadmap-future-extensions.md): what comes after the MVP (not built, not ordered)
- [11 Open items](docs/11-open-items.md)
- [Glossary](docs/glossary.md)

## Hardware files

| Path | Contents |
|---|---|
| [`hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/`](hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/) | The complete v1.2 release, unpacked: KiCad source, Gerbers, BOM/CPL, drawings, verification, reproduction scripts |
| [`hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay_Complete.zip`](hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay_Complete.zip) | The same release as the original ZIP |
| [`hardware/pcb/…/fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip`](hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip) | **The file to upload to a fab.** Upload this, not the outer package |
| [`hardware/pcb/pcbway-replacement-order/`](hardware/pcb/pcbway-replacement-order/) | Replacement-order review: checked BOM/CPL, QA JSON, assembly-review images, status |

## Archive

[`_archive/`](_archive/) holds the raw transcripts of the original ChatGPT and Codex threads and the older source documents. It's there as a safety net for searching, and it is **not authoritative**. The threads contain many ideas that were later dropped. Where the archive and `docs/` disagree, `docs/` wins.
