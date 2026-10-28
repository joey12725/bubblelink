# 04. Power System

Everything electrical outside the PCB: battery, charging, protection, distribution, current sensing, and voltage regulation. See [docs/parts/ORDER_LEDGER.md](parts/ORDER_LEDGER.md) for purchased components and [docs/parts/listings/](parts/listings/) for detailed part specs.

## Table of Contents

1. [Battery Pack](#battery-pack)
2. [Charging & Protection](#charging--protection)
3. [Main Distribution Harness](#main-distribution-harness)
4. [Current Sensing](#current-sensing)
5. [Gun Channels](#gun-channels)
6. [5V Regulation](#5v-regulation)
7. [Voltage Readout](#voltage-readout)
8. [Runtime & Power Budget](#runtime--power-budget)
9. [Thermal & Safety Notes](#thermal--safety-notes)
10. [Complete Wiring Table](#complete-wiring-table)

---

## Battery Pack

The 2S5P block stands on the base of the printed stick's sled, beside the central spine; it is not a separate cartridge. See [09-printed-parts.md](09-printed-parts.md).

**Configuration:** 2S5P (two series × five parallel)  
**Cells:** 10× Samsung INR18650-25R, 3.6 V nominal, 2500 mAh each  
**Nominal voltage:** 7.2 V (two cells @ 3.6 V nominal)  
**Fully charged:** 8.4 V (4.2 V per cell)  
**Cutoff voltage:** ~6.0 V under load (protected by BMS)  
**Total capacity:** 12.5 Ah (2.5 Ah × 5 parallel)  
**Energy:** 90 Wh nominal (7.2 V × 12.5 Ah)  
**Cell dimensions:** 18.33 ± 0.07 mm × 64.85 ± 0.15 mm per cell; two offset rows of five at 19.9 mm pitch in the printed cell holders  
**Mass:** ~450 g cells alone; ~500–600 g with cell holders, BMS, and connectors

### Cell Layout & Interconnect

Arrange as two five-cell parallel groups in two offset rows of five. **The two rows face opposite directions**: row A has + toward one end and row B has − toward that end. If every cell faces the same way, it's 10P, not 2S5P. In the stick, the cell axes run front to back and the TERM face (pack + and −) faces the back.

**Cell insulation & spacing:**
- Fish-paper positive-terminal rings on all ten cell positive ends (prevents shorts)
- ~1.6 mm wrapper gap at the holders' 19.9 mm pitch
- Printed 5×2 offset cell holders (original design, replacing the Cults3D spacer remix): **MID** caps the series end (every tab on that face is the midpoint); **TERM** carries the separate pack + and − buses. Keep the two rows' strips on the TERM face apart, with fish paper between them. The holders are mirror images; if the A/B letters don't line up, rotate MID 180°

**Interconnect method:** Spot-welded nickel-plated steel tabs, 2.6 cm long (3 × 10 pcs), not pure nickel. The 26 mm tabs reach both cell centres at the 19.9 mm pitch.

**Series path:** Five independent nickel-plated steel bridges connect the two cell groups:
- Five series links each rated for ~6 A at maximum 30 A pack current
- Doubled or tripled tabs in high-current concentration zones (where 12 AWG leads attach)
- Approximately 17–21 total tab pieces required (including spares and reinforcements)

**Parallel path per group:** Four additional tabs each (one per cell-to-cell connection within each five-cell group), or single wide tab per group if width permits. Design for minimum resistance (<20 mV drop per series link at 30 A).

**Test before assembly:** 
- Capacity-match all ten cells by voltage and internal resistance before welding
- Load-test assembled pack at 15 A sustained; measure tab/weld temperature with IR camera or thermocouples
- No localized heating above 50°C

### BMS (Battery Management System)

**Part:** 2S 40 A lithium-ion (NMC/LiCoO₂) BMS module, not LiFePO₄  
**Voltage rating:** 2S (7.2 V nominal, 8.4 V fully charged)  
**Protection:** 40 A continuous, automatic short-circuit protection with recovery after load removal  
**Balancing:** Passive cell-voltage balancing, NTC temperature sensor, cutoff ~55–60°C, reset ~45°C  
**Connections:**
- **B−:** Battery group 1 negative
- **BM/B1:** Midpoint (group 1 positive / group 2 negative)
- **B+:** Battery group 2 positive
- **P−:** System negative (to main load)
- **P+:** System positive (to main load / USB-C charger)

**Size (measured 2026-10-14):** 2½ × 1⅞ × ¼ in (mounting holes not used).

Stands on edge in a 7 mm slot along the stick's back wall, next to the battery's TERM face; the TERM-face leads reach it through the channel behind the spine. Solder 12 AWG leads from parallel-series bus to BMS inputs with low-resistance solder joints and mechanical strain relief. Attach JST-XH three-pin balance connector for future cell monitoring (optional).

---

## Charging & Protection

### USB-C Charger

**Part:** SZHJW Type-C USB-PD → 2S 8.4 V boost charger, **2S 4A** variant  
**Specifications:**
- Input: USB-C Power Delivery (5 V / 3 A typical input from wall supply)
- Output: 8.4 V CC/CV for 2S lithium-ion, up to 4 A rated (actual charge current limited by USB supply and BMS)
- Charge time: 8–10 hours from full discharge at ≤4 A delivered to cells
- Wiring: USB-C input to 30 W or greater USB-PD wall charger; BAT− to BMS P−; BAT+ to BMS P+

**Size (measured 2026-10-14):** 1½ in (plug direction) × 11/16 × ⅜ in.

**Installation:** Glued under the CHG window in the stick's cap, receptacle up. Connect its output to the BMS load terminals (P− and P+) through an XT30 pair so the cap stays removable; do not connect directly to battery slab, which bypasses BMS protection.

**Charging procedure:**
1. Disconnect pack from backpack if possible. **Take the cap off** until the first enclosed charge has been checked: charger and BMS temperatures inside the closed tube haven't been measured (at 4 A the charger alone may give off around 3–4 W), and pressure relief if a cell fails isn't verified
2. Place on flat, non-flammable surface
3. Visually inspect battery for swelling or damage
4. Connect USB-C charger to 30 W+ USB-PD wall supply
5. Monitor BMS temperature during first 10 minutes (should not exceed 45°C)
6. Charge overnight (8–10 hours for full cycle)
7. Disconnect charger after cycle complete

**Safety:** BMS will cut off charging if temperature exceeds 60°C or if pack voltage reaches 8.7 V. Do not force discharge through power draw while charger is connected; the charger is not isolated and may be damaged by back-feeding current.

### Main Protection

**Type B-30A Manual-Reset Circuit Breaker**  
**Part:** Waterproof DC automotive breaker, 30 A rating, Type B (manual reset only)  
**Voltage:** 12–48 V DC (suitable for 2S 8.4 V)  
**Terminals:** M6 threaded studs (6 mm hole), not solder terminals  
**Dimensions (measured 2026-10-14):** 1⅝ in square plate, 4 in (102 mm) long, 1⅝ in thick, plate holes 1¼ in apart. The listing's 72 × 48 × 44 mm was wrong: it's longer (102 vs 72 mm) but slimmer.  
**Form:** Inline type: studs at both ends, and a square plate in the middle carrying a red reset lever and a red push-to-trip button.  
**Location:** Stands upright behind the sled's cross panel, 2 mm from the outer wall, with a wire channel between it and the spine. It hangs by zip ties through its two plate holes and tall slots in the spine. The tube walls are solid, so its controls are only reachable with the sled out.  
**OFF switch:** Pull the power key out of the KEY socket on the cap top. That turns off everything downstream (breaker, ACS758, bucks, PCB, voltmeter and guns): all loads off; the battery stays connected to the BMS, the charger and one pin of the key socket. The charger connects to BMS P+/P− upstream of the key, so it still works with the key out. For storage or transport, key out and key blank in. Wiring: socket pin A is BMS P+, pin B is the breaker input (12 AWG, soldered, slack for lifting the cap).

**Wiring:** The breaker is in the **+ line only**. No negative wire goes to it.
- Battery positive from BMS P+ → M6 stud via 12 AWG red silicone wire fitted with M6 closed-ring terminal
- Other M6 stud → main positive distribution
- Return path: all negative to BMS P− (shared return)

**Ring terminals:** Use **SC10-6** copper ring lugs (10 mm² barrel, M6 hole, specified for 12 AWG wire). **Solder-fill the barrel** to eliminate crimp-only failures and improve current distribution. **Do NOT** solder wire directly to breaker studs—excessive heat risks damaging breaker internals and causes fatigue failures under load cycling. Procedure: solder 12 AWG wire into the ring barrel (away from the stud connection), allow solder to cool, then bolt the filled ring under breaker nut with strain relief.

**Reset procedure:** A trip means a real fault (a short, a jammed motor), so find the cause first. Take the cap off (2 screws), lift the sled out (leave enough wiring slack for that) and work the red reset lever. Press firmly until click is heard. If breaker trips repeatedly, disconnect one gun at a time and test to isolate fault.

---

## Main Distribution Harness

**Battery path:** BMS P+ → breaker → 12 AWG red silicone wire → distribution point

**From distribution point, split into:**
1. **Gun channel bus:** 12 AWG (red) to ACS758 high-current sense terminals
2. **Pump & controller supply:** 12 AWG (red) to YxPC Buck A 5V converter (pump + PCB)
3. **LED backpack supply:** 12 AWG (red) to YxPC Buck B 5V converter (backpack only)
4. **Return:** All negatives → 12 AWG black → BMS P−

**Wire gauge justification:**
- 12 AWG rated for 30 A continuous (intentionally oversized to avoid voltage drop in the ~2–4 ft runs inside pack)
- At 30 A over 4 feet: ~0.048 V drop (acceptable for battery system with regulated 5 V downstream)
- Temperature rise during 30 A sustained: <10°C above ambient in air; lower in thermally managed pack

**Harness assembly method:** Soldered star configuration from breaker/BMS outputs, staggered point-to-point with adhesive heat shrink on each tap, no distribution block required (single 30 A main breaker eliminates per-channel isolation).

---

## Current Sensing

**ACS758LCB-050B Hall-effect bidirectional current sensor**  
**Specifications:**
- Measurement range: ±50 A (gun current only)
- Sensitivity: 40 mV/A (linear)
- Supply voltage: 5 V DC
- Zero-current output: ~2.5 V (nominal; to be verified upon hardware arrival)
- Bandwidth: >100 kHz (fast enough for pump control switching)
- Package: DIP-8 module on breakout board

**Placement:** Separate from the PCB (external high-current sensors prevent PCB layout noise and heat). The module (measured 1½ × ~¾ × ⅛ in) drops into a compartment on the front of the sled's cross panel, above Buck A, and is held with a zip tie; its mounting holes aren't used.

**Wiring (high-current path):**
- **Conductor in:** 12 AWG red from breaker through sensor terminals (both terminals carry full gun current)
- **Conductor out:** 12 AWG red to XT30U channel split
- Must use module's screw terminals or solder-pad connectors, not pin headers (high current)

**Sensing output (signal path):**
- Three wires from ACS758 module to PCB via JST-XH connector:
  - **GND:** sensor ground (connect to system return / BMS P−)
  - **Vcc (5V):** from Buck A 5V rail
  - **Signal out:** to PCB comparator input (TI TLV1822QDRQ1; delivers 2.5 V at zero current, ±40 mV per A)

**Purpose:** Detects when either bubble gun draws current (threshold >~0.3–0.5 A), triggers automatic pump start via onboard comparator logic. Pump stays on ~300–750 ms after gun current drops below threshold.

**Note:** Do NOT route pump or USB-backpack-LED current through ACS758 conductor; sensor must measure gun-channel current only. Otherwise pump starts, load-current from pump increases ACS758 signal, causing false positive feedback loop.

---

## Gun Channels

**Configuration:** Two independent XT30U power channels, 16 AWG each, four feet long

**Per channel:**
- **Wire:** 16 AWG silicone (red and black pair, tinned copper strands)
- **Connector (pack end):** XT30U female receptacle (recessed, live power) potted in a well on the cup's outer wall; the umbilical's pack end is the XT30U male
- **Connector (gun end):** XT30U **female** on the umbilical (power always comes from a female); it plugs onto the gun's XT30U male input
- **Rated current:** 15 A continuous per XT30U (sufficient for one 3-head gun at full power, or two guns sharing a channel if total <15 A)

**Umbilical construction (per four-foot channel):**
- Two 16 AWG wires (red +, black −) arranged as twisted pair
- Three additional mechanical elements bundled inside 8–10 mm PET braided sleeve:
  - One 3.5 mm ID × 5.5 mm OD silicone tube (fluid line to gun nozzles)
  - One 4 mm paracord or Dyneema cord (load-bearing tether, rated for gun drop)
  - A printed umbilical brick at the gun end (ASA or PETG); the pack end is an XT30U male, the hose end and a paracord loop

**Strain relief:** XT30 connectors soldered with generous heat-shrink wrap. At the gun end the connector is strapped with a zip tie into the open-top pocket of the umbilical brick; the paracord ties through the brick, so the load path transfers mechanical stress to paracord, not wire (wire carries power only). At the pack end the cord ties through a U-tunnel boss on the cup. Tether prevents damage if gun is dropped during event.

**Termination:** Wires soldered to XT30 pins from rear (solder from back of connector, not from pin directly, to avoid cold-solder joints). Verify mechanical fit before final enclosure assembly.

**Voltage at gun:** Unregulated 2S battery voltage (~7.2–8.4 V). Gun donor mechanism has its own built-in pump and trigger; each gun controls its own motor current independently via internal trigger potentiometer or Hall switch (no separate PWM regulation from pack).

---

## 5V Regulation

**Two independent buck converters** (isolation for noise/stability):

### Buck A: Pump & Controller Supply

**Part:** YxPC 6–20V to 5V USB buck converter (adjustable variant, <1 A typical rating)  
**Configuration:**
- Input: 2S battery voltage (~6–8.4 V unregulated)
- Output: 5.0 V (adjusted via onboard potentiometer before installation)
- Load: G528 peristaltic pump (~250–300 mA running, 0.3 A nominal) + PCB logic/LEDs (<50 mA)
- Total: ~350 mA steady-state

**Size (measured 2026-10-14):** 1 in along the port, 5/16 in thick; width not measured (17 mm assumed). Same for Buck B.

**Installation:**
- Drops into a compartment on the front of the sled's cross panel and gets a zip tie
- **Solder the output directly to the PCB J1 lead.**
- **Verify output with multimeter before connecting any load.** Bench-test it under load before installing: it must stay below 5.25 V. Target output is 5.0 V; PCB accepts 4.75–5.25 V. Use onboard potentiometer to adjust; do not assume factory default.
- Do not exceed 1 A total load on module (pump ~0.3 A + PCB <0.05 A)
- Connect input to 12 AWG main red wire (post-breaker)
- Output feeds PCB power input (JST-XH J1, 2-pin) and G528 pump (+5V, −GND)

**Alternative (if module fails during testing):** Pololu S13V30F5 buck converter (30 A rated, more stable but costs ~$8 vs. [price]). This can be swapped in without board redesign; module mounts external to PCB.

### Buck B: LED Backpack Supply

**Part:** Second identical YxPC 6–20V to 5V USB buck  
**Configuration:**
- Input: 2S battery (post-breaker)
- Output: 5.0 V
- Load: LED backpack. Measured 2026-10-27: 66 mA at the battery with a simple design (~10% of pixels lit); scaling with lit pixels, up to ~0.66 A at the battery fully lit

**Installation:** Stands on a shelf printed on the tube's front wall, in the corner by the outer wall, with its PCB facing the front wall (2 mm gap). It slides along the shelf until its USB-A receptacle sits in (or right behind) the outer wall's 14.0 × 6.6 mm window (LED 5V), then gets a zip tie over its top edge. The backpack cable plugs straight into the buck: no extension cable and no USB plug inside. The sled lifts out past it untouched; its two input wires (main + after the breaker, and P−) run from the sled with a 2-pin JST-XH plug. Unplug the backpack cable before lifting the sled. Measure the buck (width and where its USB-A sits) before printing the tube; the shelf assumes 25.4 × 17 × 8 mm with the receptacle centred on the 17 mm side. Separate from Buck A to prevent pump current transients (0.3 A inrush) from resetting backpack logic or causing brief display flicker.

**Setting:** Same as Buck A—verify 5.0 V output with multimeter before connecting LED backpack.

---

## Voltage Readout

**Digital voltmeter, 4–100V DC range**  
**Specifications:**
- Display: Red LED 0.56-inch digits
- Input: Two wires (positive, negative)
- Supply current: Not measured on its own. It's under 50 mA: the whole system idles at 50 mA with the backpack unplugged (2026-10-27), voltmeter included
- Accuracy: ±1 V typical across range
- Protection: Reverse-polarity protected

**Wiring:**
- Positive (red): to the main positive **after the breaker**, so tripping the breaker turns the voltmeter off
- Negative (black): to BMS P− (system ground)
- It draws current whenever the breaker is closed; there's no push-button or standby mode. Left on with the backpack unplugged, the whole system (voltmeter included) drains the pack in about 10 days, so overnight doesn't matter, but take the power key out (blank in) for storage

**Display reference:**
- 8.4 V: Fully charged, ready for operation
- 7.2 V: Half capacity (nominal)
- 6.0 V: Minimum safe voltage (BMS cutoff threshold); if reached, stop operating and recharge
- Below 6.0 V: Do not fire; BMS is actively protecting cells

**Location:** Top of the stick's cap: the body drops through a 31.2 mm hole (29.2 mm printed 1-2 mm too small in ASA) and is glued around its bezel. Measured 2026-10-14: bezel about 1 5/16 in, body a hair over 1⅛ in, about 1 in deep or a bit more (the cap allows 30 mm above the battery).

---

## Runtime & Power Budget

### Measured System Current (Joey, 2026-10-27)

Whole-system current from the battery, on the built BubbleLink:

| State | Current |
|-------|--------:|
| Idle, LED backpack showing a simple design (~10% of pixels lit) | 116 mA |
| Idle, LED backpack unplugged | 50 mA |
| One head firing at full power (pump, PCB and backpack included) | 1.51 A |

What that breaks down to:
- **Base idle (50 mA):** bucks, PCB, ACS758 and voltmeter together. The voltmeter is in this figure, so on its own it draws less than 50 mA.
- **LED backpack:** 66 mA at ~10% of pixels. Assuming it scales with lit pixels, that's about 66 mA per 10% lit, so up to ~0.66 A fully lit. That's an upper bound, since part of the 66 mA is the backpack's controller and doesn't scale.
- **Each head firing:** 1.51 − 0.116 ≈ **1.39 A**. The budget counts this per head, which is conservative: the 1.39 A includes the pump, and one pump serves every head. Heads ≈ 1.39 A × N, so four heads ≈ 5.7 A (~2.8 A per channel) and eight heads ≈ 11.3 A, all well under the 15 A XT30U and 30 A breaker ratings.

**Usable capacity:** 12.0 Ah from full charge (8.4 V) to the BMS cutoff, taken as ~96% of the 12.5 Ah rating. The BMS's exact over-discharge voltage isn't on record; Li-ion 2S boards usually cut at 2.5–3.0 V per cell, and 25R cells have very little capacity left below 3.0 V.

**Idle runtime (key in, not firing):**
- Simple design on the backpack: 12.0 Ah ÷ 0.116 A ≈ **103 h (~4.3 days)**
- Backpack unplugged: 12.0 Ah ÷ 0.050 A ≈ **240 h (~10 days)**

So idle barely matters: each hour of a festival day costs ~1% of the pack.

**Nonstop firing from full charge:**

| Heads | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------|--:|--:|--:|--:|--:|--:|--:|--:|
| System current | 1.51 A | 2.90 A | 4.30 A | 5.69 A | 7.09 A | 8.48 A | 9.87 A | 11.27 A |
| Time to BMS cutoff | 7:57 | 4:08 | 2:48 | 2:06 | 1:42 | 1:25 | 1:13 | 1:04 |

**Festival day: total trigger-on time.** The pack is on (key in, backpack showing a simple design) for the whole day; the table gives how many hours and minutes of full-power firing the battery covers, in total over the day. "All day" means it can fire nonstop for the whole day.

| Day length | 1 head | 2 heads | 3 heads | 4 heads | 5 heads | 6 heads | 7 heads | 8 heads |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 h | all day | all day | all day | all day | 1:41 | 1:24 | 1:12 | 1:03 |
| 3 h | all day | all day | 2:47 | 2:05 | 1:40 | 1:24 | 1:12 | 1:03 |
| 4 h | all day | all day | 2:46 | 2:04 | 1:39 | 1:23 | 1:11 | 1:02 |
| 5 h | all day | 4:06 | 2:44 | 2:03 | 1:38 | 1:22 | 1:10 | 1:01 |
| 6 h | all day | 4:03 | 2:42 | 2:02 | 1:37 | 1:21 | 1:10 | 1:01 |
| 7 h | all day | 4:01 | 2:41 | 2:00 | 1:36 | 1:20 | 1:09 | 1:00 |
| 8 h | 7:57 | 3:58 | 2:39 | 1:59 | 1:35 | 1:19 | 1:08 | 1:00 |

Formula: firing hours = (12.0 Ah − 0.116 A × day hours) ÷ (1.39 A × heads). For a brighter backpack design, add ~66 mA to the idle figure for every extra 10% of pixels lit.

Caveats:
- The pump isn't counted as shared, so multi-head times are slightly low (by roughly 10–15% at 8 heads, if the pump is ~0.2 A of the 1.39 A).
- The buck loads draw a little more current as the battery sags, and the heads (straight on the battery) draw a little less. Those roughly cancel.
- **Fluid probably runs out first.** The 1 L bladder at the baseline gun's ~5.6 mL/min per head (16.9 mL/min for three heads) lasts ~3 h on one head and ~22 min on eight. The donor heads' own flow hasn't been measured yet.

### Measured Baseline (2S1P Test)

**Test data:** One 2S1P Samsung 25R pair (18 Wh nominal), tested at the target festival event
- Event duration: ~75 minutes with heavy dancing; actual gun firing ≈28 minutes (37% duty)
- Solution consumed: 473.6 mL in that 75-minute event period
- Average power during event: ~26 W (including pump + gun + losses)
- Voltage drop under load: 4.2 V → 3.6 V per cell
- **Energy per liter: ~69 Wh/L** (0.069 Wh/mL, measured across both continuous full-fire and event scenarios)

### 2S5P Extrapolation

These estimates scale the old baseline gun (~70 W firing). The donor heads measured on 2026-10-27 draw far less per head (~1.39 A, roughly 10 W), so use [Measured System Current](#measured-system-current-joey-2026-10-27) for battery runtime. The per-liter figures still need the donor heads' flow measured.

**Pack energy:** 90 Wh nominal (5× parallel = 5× energy of 2S1P)

**Estimated solution capacity before cutoff (3.6 V):**
- 90 Wh ÷ 69 Wh/L ≈ **1.3 L** at 3.6 V per cell
- Practical commitment with 1 L reservoir: **1 L per fully charged pack**, with ~300 mL safety margin remaining
- Two fully charged packs support **~2.6 L total** (one reload during event)
- Note: Individual donor gun efficiency varies widely (3–8 V nominal, varying motor design); calibrate against measured flow at typical event voltage (7.2 V nominal)

**Practical scenario (1 L reservoir):**
- One fully charged 2S5P pack supports ~1.0 L fluid delivery before reaching BMS cutoff (6.0 V)
- Estimated runtime at 37% average duty (typical event use): 2–3 hours per pack
- With pump and gun system running, solution consumption is ~0.069 Wh per mL at average load
- Multiple packs and reservoir refills extend event duration; carry one fully charged spare

### Power Budget (Instantaneous)

**Typical load composition at full power** (measured 2026-10-27, see [Measured System Current](#measured-system-current-joey-2026-10-27)):
- Each donor head firing: ~1.39 A at the battery (pump share included)
- Two dual-head guns (4 heads): ~5.7 A total system current
- Base idle (bucks, PCB, ACS758, voltmeter): 50 mA
- LED backpack: 66 mA at ~10% of pixels lit
- **Total continuous:** 1.5 A (one head) to 11.3 A (eight heads)

**Peak (startup + motor inrush):** Up to 15–20 A briefly; 30 A breaker protects against sustained faults.

**Overvolting effect:** 6V-nominal donor guns overvolted to 8.4 V will draw more current and consume more solution. To mitigate, consider PWM control on gun side (future enhancement, not in MVP). For v1, fire at full voltage to get maximum bubble output; control duty cycle via trigger (tap trigger rather than sustained hold).

### Thermal & Cell Heating

**Battery cell self-heating at 10 A continuous:**
- Internal resistance: ~22 mΩ per Samsung 25R
- Power dissipated per cell: I² × R = 10² × 0.022 = 2.2 W
- Five cells in parallel: 2.2 W ÷ 5 = 0.44 W per cell (much lower than 2S1P alone)
- Temperature rise: ~2–5°C above ambient in still air

**2S5P advantage:** Parallel configuration distributes current five ways, reducing per-cell heating to ~28% of 2S1P equivalent. Cells should remain comfortable to hold even after 30+ minute sustained firing.

**Packed thermal environment:** Cells inside the stick's closed dry tube, in a soft hydration pack, with no active cooling. The tube only breathes incidentally (grommet slits, cap ring); pressure relief if a cell fails is not verified. Monitor pack surface temperature during testing; if enclosure is too hot to touch, stop operation and allow 10 minutes cool-down before resuming.

---

## Thermal & Safety Notes

### Cell Temperature Monitoring

- **Samsung 25R safe limit:** 60°C absolute maximum (per datasheet)
- **Recommended ceiling:** 50°C during operation (NTC sensor cutoff at 55–60°C, reset at ~45°C)
- **Comfortable-to-hold range:** <45°C
- If cells feel hot enough to cause discomfort, stop firing immediately

### Contact Resistance Risk

The old 2S1P test used hand-soldered connections that developed significant contact resistance (~30–50 mΩ), causing localized heating even at moderate currents (3.2 W per bad connection at 10 A). The 2S5P design uses **spot-welded nickel-plated steel tabs** to eliminate this; verify welds are solid and distribute current across five series links.

### Connector Integrity

- **XT30U connectors:** Rated for 15 A sustained. If gun is hot to the touch after extended firing, suspect bad connector contact. Disconnect, clean gold pins with dry cloth, reinsert firmly.
- **Ring terminals on breaker:** Crimped terminals are more reliable than solder under thermal cycling. Do not rely on solder alone; use proper crimping tool or accept solder-fill as secondary retention only.

### Charging Safety

- Charge with the stick's cap off until the first enclosed charge has been checked (charger and BMS temperatures inside the closed tube are unverified).
- Charge on flat, non-flammable surface (wood table, concrete, not carpet or paper).
- If BMS cuts off charging (thermal or voltage cutoff), allow pack to cool to room temperature before resuming. Do not force discharge through parallel load.
- Damaged or swollen cells: **do not attempt to recharge or discharge**; replace immediately.

### Storage

- Take the power key out, and put the key blank in, for storage and transport (all loads off; the battery stays connected to the BMS, the charger and one pin of the key socket). The BMS stays on the battery either way; its quiescent draw hasn't been measured but is typically tiny
- Store fully charged packs at room temperature (~20°C) in dry location
- For storage >1 month, discharge to 50% (7.2 V nominal) to reduce stress on BMS balancing circuit
- Do not store in extreme heat (>35°C) or moisture (>85% RH)

---

## Complete Wiring Table

| From | To | Wire Gauge | Connector | Polarity | Notes |
|------|----|-----------:|-----------|----------|-------|
| BMS P+ | Power key socket pin A | 12 AWG red | Soldered; slack to lift the cap | + | Key bridges A to B (key in = ON); the charger stays on BMS P+/P- upstream |
| Power key socket pin B | 30A Breaker stud | 12 AWG red | Soldered at the socket; M6 ring terminal at the stud | + | High-current; use crimped ring, not solder to stud |
| Breaker stud | Distribution point | 12 AWG red | Solder + heat-shrink | + | Short run (~6 inches), strain relief only |
| Distribution | ACS758 in (conductor) | 12 AWG red | Sensor screw terminals | + | High-current sense path |
| ACS758 out | XT30U split junction | 12 AWG red | Solder + heat-shrink | + | Exits high-current sensor |
| Junction | XT30U gun channel A | 16 AWG red | XT30U female connector | + | Four-foot umbilical |
| Junction | XT30U gun channel B | 16 AWG red | XT30U female connector | + | Four-foot umbilical |
| BMS P− | System ground (bus) | 12 AWG black | Solder | − | Return path for all circuits |
| Ground bus | ACS758 GND (J2 pin 1) | Small wire | JST-XH 3-pin | − | Signal return; low-current |
| Ground bus | Gun channels (both) | 16 AWG black | XT30U (within connectors) | − | Return in umbilical pairs |
| Ground bus | G528 pump (−) | Small wire | JST-XH (J3) | − | Pump return |
| Ground bus | PCB GND (J1 pin 2) | Small wire | JST-XH 2-pin | − | Logic ground |
| Main red | Buck A input (Hi) | 12 AWG red | Solder | + | Pump + controller supply |
| Buck A output | PCB +5V (J1) | Small wire | Soldered at buck; JST-XH 2-pin at PCB | + | Logic supply, TLV1822 comparator, LEDs |
| Buck A output | G528 pump (+) | Small wire | JST-XH (J3) | + | Pump power @ 5V |
| Main red (after the breaker) | Buck B input (Hi) | 12 AWG red | Soldered; 2-pin JST-XH plug at the sled so it can come out | + | LED backpack supply (Buck B is on the tube's front wall shelf) |
| Buck B output | LED backpack +5V | Backpack's own USB cable | Buck B's USB-A receptacle, in a window in the tube wall | + | Backpack power |
| Main red (after breaker) | Voltmeter (+) | Small wire | Connector | + | Battery voltage display; off when the breaker is tripped |
| BMS P− | Voltmeter (−) | Small wire | Connector | − | Voltmeter return |
| ACS758 (5V out) | PCB Vcc (J2 pin 2) | Small wire | JST-XH 3-pin | + | Sensor supply; low-current |
| ACS758 signal out | PCB input (J2 pin 3) | Small wire | JST-XH 3-pin | Variable | 2.5V zero, ±40 mV/A |
| PCB pump output | G528 (J3 pins 1–2) | Small wire | JST-XH 2-pin | Variable | MOSFET gate to pump |

**Notes on wire selection:**
- 12 AWG silicone-insulated, tinned copper preferred for all main paths (flexible, heat-resistant, handles temperature swings)
- 16 AWG for four-foot umbilicals (lower current per gun, standard practice for RC/hobby projects)
- Small wire (22–24 AWG) for logic, sensor, and signal lines (<100 mA)
- All connectors JST-XH for logic; XT30U for gun power; M6 ring terminals for breaker; direct solder on pump and sensors

---

**Source:** Joey's bench measurements, component datasheets from [docs/parts/listings/](parts/listings/), and v1.2 design handoff. Wiring verified against assembled boards post-build; thermal testing on 2S5P baseline at 15 A sustained (target <50°C after 30 min).

