# Bill of materials

Everything you need to build one BubbleLink pack with two gun channels. Commodity parts were sourced from AliExpress; the search links below are generic, so pick any seller whose listing matches the spec column. Where a spec matters (pump voltage, BMS chemistry, connector type), it is called out in **bold**.

Printed parts are listed in the [print guide](../hardware/printed/README.md). The controller board has its own machine-readable BOMs in the [PCB release](../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/).

## Power

| Qty | Part | Spec | Notes | Find it |
|---:|---|---|---|---|
| 10 | Samsung INR18650-25R | 18650 Li-ion, 2500 mAh, 20 A | Matched set for the 2S5P pack (7.2 V, 12.5 Ah, 90 Wh) | [search](https://www.google.com/search?q=Samsung+INR18650-25R) |
| 1 | 2S BMS | **2S 8.4 V 40 A Li-ion** with balance leads | Confirm it is the Li-ion version, not LiFePO₄ | [search](https://www.aliexpress.us/w/wholesale-2S-8.4V-40A-BMS-balance.html) |
| 1 | USB-C 2S boost charger | USB-C in, **8.4 V 2S, 4 A** variant | Charges battery-side, upstream of the power key | [search](https://www.aliexpress.us/w/wholesale-type-c-2S-8.4V-boost-charger.html) |
| 1 | Manual-reset breaker | **30 A**, 12–48 V DC, M6 studs ("Type B-30A") | The only main protection; + line only | [search](https://www.aliexpress.us/w/wholesale-30A-manual-reset-circuit-breaker-12V.html) |
| 1 | ACS758 current-sensor module | **ACS758LCB-050B**, 5 V, 40 mV/A, ±50 A | Measures combined gun current for the controller | [search](https://www.aliexpress.us/w/wholesale-ACS758LCB-050B-module.html) |
| 2 | 5 V USB buck module | 6–20 V in, 5 V USB out | Buck A feeds the PCB and pump (keep it under 5.25 V); Buck B feeds the LED backpack. Upgrade path for Buck A: Pololu S13V30F5 | [search](https://www.aliexpress.us/w/wholesale-6-20V-to-5V-USB-buck-module.html) |
| 1 | Round LED voltmeter | DC 4–100 V, two-wire, ~29 mm | The battery gauge on the cap | [search](https://www.aliexpress.us/w/wholesale-DC-4-100V-round-two-wire-voltmeter.html) |
| 30 | Cell tabs | **Nickel-plated steel**, 2.6 cm | Five parallel series bridges | [search](https://www.aliexpress.us/w/wholesale-18650-nickel-plated-steel-tab.html) |
| 10 | Fish-paper insulator rings | 18650 | One per cell, positive end | [search](https://www.aliexpress.us/w/wholesale-18650-insulator-ring-fish-paper.html) |
| 3 m + 3 m | Silicone wire, 12 AWG | Red / black, tinned | Battery and main path | [search](https://www.aliexpress.us/w/wholesale-12AWG-silicone-wire.html) |
| 5 m + 5 m | Silicone wire, 16 AWG | Red / black, tinned | Gun branches and umbilicals | [search](https://www.aliexpress.us/w/wholesale-16AWG-silicone-wire.html) |
| 1 set | SC10-6 copper ring lugs | M6 hole | Only if your breaker has studs instead of wire clamps; solder-fill the barrel | [search](https://www.aliexpress.us/w/wholesale-SC10-6-copper-lug.html) |
| 2 pairs | XT60H connectors | Male + female with sheath | Power key and its inline disconnect | [search](https://www.aliexpress.us/w/wholesale-XT60H-connector.html) |
| 5 pairs | Amass XT30U connectors | **XT30U** (not MR30) | One pair per umbilical end plus the pack wells | [search](https://www.aliexpress.us/w/wholesale-Amass-XT30U.html) |
| 1 kit | JST-XH 2.54 mm kit | Pre-crimped leads, 2/3-pin housings | PCB and internal harness | [search](https://www.aliexpress.us/w/wholesale-JST-XH-2.54-kit-pre-crimped.html) |

## Fluid

| Qty | Part | Spec | Notes | Find it |
|---:|---|---|---|---|
| 1 | Peristaltic pump, GROTHEN G528 | **6 V**, 3 × 5 mm tube, 150 mL/min | Seller art often says 12 V; check the motor marking | [search](https://www.aliexpress.us/w/wholesale-G528-6V-peristaltic-pump.html) |
| 1 | Hydration bladder | 1 L, with detachable drinking tube | The bubble reservoir | [search](https://www.aliexpress.us/w/wholesale-1L-hydration-bladder.html) |
| 5 m | Silicone tube | Food-grade, **3.5 mm ID × 5.5 mm OD** | The only system tubing | [search](https://www.aliexpress.us/w/wholesale-silicone-tube-3.5mm-5.5mm.html) |
| 1 set | Nylon hose-connector assortment | Straight unions, tees, reducers | Use the 1/8" unions (#68401) and 5/32" tees (#68409) | [search](https://www.aliexpress.us/w/wholesale-car-hose-connector-assortment-reducer-T-piece.html) |
| 1 | Inline check valve | **4 mm** barb, ~0.003 MPa cracking, liquid-rated | Bypass loop, arrow toward the pump inlet | [search](https://www.aliexpress.us/w/wholesale-4mm-plastic-check-valve-one-way.html) |
| 1 | Bubble concentrate | Commercial machine concentrate | Start here before mixing your own | [search](https://www.google.com/search?q=bubble+machine+solution+concentrate) |
| optional | Liquid Germall Plus | Preservative | Only if solution is stored | [search](https://www.google.com/search?q=Liquid+Germall+Plus) |

## Umbilicals, carrier and guns

| Qty | Part | Spec | Notes | Find it |
|---:|---|---|---|---|
| 15 m | 550 paracord | 7-strand, 4 mm | The load-bearing tether in each umbilical | [search](https://www.aliexpress.us/w/wholesale-550-paracord-7-strand.html) |
| 5 m | Braided PET sleeving | 10 mm | Bundles power, hose and cord | [search](https://www.aliexpress.us/w/wholesale-10mm-braided-PET-sleeving.html) |
| 1 | LED pixel backpack | Bluetooth pixel-panel backpack ("M Style" size) | Any bag that fits the 100 × 78 × 220 mm stick next to a 1 L bladder works | [search](https://www.aliexpress.us/w/wholesale-LED-pixel-backpack-bluetooth.html) |
| 4 | Donor bubble-gun heads | Blower-head mechanisms from toy bubble guns | Match current draw; measured ~1.39 A per head at 2S | any toy store |
| 2 | Gardner Bender GSW-21 | Push-on/push-off SPST, 8 A | Duo gun trigger switch | [spec sheet](https://www.gardnerbender.com/-/media/inriver/GSW-21_SPEC.pdf) |
| optional | 6 × 3 mm magnets | Neodymium | Holds a Duo pair together | — |

## Hardware and consumables

| Qty | Part | Notes |
|---:|---|---|
| 2 | M3 × 10 DIN 912 socket-head screw, stainless | Cap, each with a flat washer over the TPU washer |
| 4 | M3 × 12 DIN 912 socket-head screw, stainless | Cup, each with a split lock washer |
| 6 | M3 hex nut | Glued into printed pockets |
| — | Narrow zip ties, CA, hot glue, neutral-cure silicone, clear hot glue or UV resin | Assembly |
| — | ASA and TPU filament | Rigid parts in ASA, seals and cushions in TPU |

## Controller PCB (BubbleLink CTRL v1.2)

Fab and SMT assembly from the release package: upload [`BubbleLink_CTRL_v1_2_Gerbers.zip`](../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/fabrication/BubbleLink_CTRL_v1_2_Gerbers.zip) with [`PCBWAY_SMT_BOM.csv`](../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/PCBWAY_SMT_BOM.csv) and [`PCBWAY_SMT_CPL.csv`](../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/PCBWAY_SMT_CPL.csv). 41 top-side placements; J4 and R22 are DNP.

Key SMT parts: TI **TLV1822QDRQ1** comparator (no substitute), TI TLV803EA43DBZR supervisor, AO3400A pump switch, DMP2065UQ-7 ×2, Vishay B340A flyback diode, Littelfuse 1812L150/16DR PTC.

Through-hole parts you solder yourself ([`USER_THT_BOM.csv`](../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/assembly/USER_THT_BOM.csv)):

| Ref | Qty | MPN | Description |
|---|---:|---|---|
| J1, J3 | 2 | JST B2B-XH-A(LF)(SN) | 2-pin vertical XH header |
| J2 | 1 | JST B3B-XH-A(LF)(SN) | 3-pin vertical XH header |
| C1 | 1 | Rubycon 16ZLH100MEFC5X11 | 100 µF 16 V low-ESR electrolytic |
| RV1 | 1 | Bourns 3296W-1-202LF | 2 kΩ 25-turn trimmer (threshold) |
| RV2 | 1 | Bourns 3296W-1-104LF | 100 kΩ 25-turn trimmer (off-delay) |
| SW1 | 1 | Omron B3F-1000 | 6 × 6 mm tactile switch (PRIME) |
| LED1–3 | 3 | Kingbright L-934GD / YD / ID | 3 mm green / yellow / red |

## Tools

Spot welder or a big-tip soldering iron with flux for the cell tabs, multimeter, an oscilloscope (helpful for tuning the off-delay), wire strippers, a 2.5 mm hex key, and two printers: one with a tall build volume for the 159 mm tube (the reference build used a Creality K2 Plus) and one for TPU and small parts (a Bambu Lab A1).
