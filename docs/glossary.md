# BubbleLink Glossary

All terms, acronyms, part nicknames, and technical shorthand used across the BubbleLink project.

---

## Battery & Power

**2S5P**  
Two cells in series, five cells in parallel. BubbleLink uses 10× Samsung INR18650-25R cells (2 rows of 5 each) for nominal 7.4 V and 12.5 Ah total capacity.

**2S nominal**  
7.4 V nominal (3.7 V per cell, two cells in series). Fully charged is 8.4 V (4.2 V per cell); discharge floor is 6.0 V (3.0 V per cell).

**BMS**  
Battery Management System. 40 A lithium BMS with cell balancing and temperature cutoff (~55–60°C discharge stop). Ordered variant: IC GOGOGO Store, 2S 8.4V 40A, Li-ion (not LiFePO₄). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 2.

**Buck A**  
First (primary) voltage regulator module. Converts battery 2S voltage (6–8.4 V) down to regulated 5 V for the PCB and pump. Generic YxPC Store 5V USB buck module (2 units ordered, [price] each; the second is **Buck B**, for the LED backpack). Both outputs are soldered directly (Buck A to PCB J1, Buck B to a cut USB cable); there's no room for USB plugs inside the stick. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 4. Design ceiling: 5.25 V maximum (PCB spec). Backup upgrade: Pololu S13V30F5 (not ordered).

**USB-C charger (2S boost)**  
USB Power Delivery input module (SZHJW Technology Store, 2S 4A boost converter, order ref [order ref removed]). Steps up USB-C input to 8.4 V for battery charging. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 3.

**Circuit breaker (main)**  
30 A manual-reset breaker (Type B-30A, YONGRUN Store, 12–48 V DC, M6 terminal studs). Inline type: studs at both ends, a 1⅝ in square plate in the middle with a red reset lever and a red push-to-trip button; 4 in (102 mm) long (measured 2026-10-14). Mounted immediately after BMS, in the + line only, for catastrophic overcurrent protection on the main 12 AWG power rails. In the stick the walls are solid, so its controls are only reachable with the cap off and the sled out; the **XT60H loop** is the OFF switch. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 5.

**Ring lug (SC10-6)**  
M6 closed-ring terminal, 10 mm² barrel (~8 AWG), 10 pcs ordered. Connects 12 AWG main power wire to circuit breaker M6 studs. Barrel is oversized; requires solder-fill and strain relief. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 6.

**Voltmeter (battery gauge)**  
DC 4–100V circular two-wire LED voltmeter display (Stlxy Store, red, 5 pcs). One in use, four spares. Shows battery voltage on top of the stick's cap. Wired after the breaker, so tripping the breaker turns it off; idle draw not yet measured. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 12.

---

## Electrical Components & PCB

**TLV1822QDRQ1 (U1, dual comparator)**  
Texas Instruments dual open-drain comparator, SOIC-8 D0008A footprint (5.4 mm row spacing; v1.1 had incorrect 4.3 mm spacing, corrected in v1.2). One channel (U1A) detects gun current from the ACS758 sensor signal against the RV1 threshold; the other (U1B) implements the pump off-delay timer by comparing the HOLD capacitor voltage to VDELAY. Both outputs are open-drain, requiring pull-up resistors.

**TLV803EA43DBZR (U2, supervisor)**  
Texas Instruments supply supervisor with open-drain RESET_N output, SOT-23-3 package. Monitors the 5 V logic rail; when voltage falls below 4.38 V threshold (~200 ms response), clamps the HOLD capacitor and pump gate low via Q1/Q3 to ensure pump stays OFF during brownout or startup.

**AO3400A (Q2, pump driver)**  
Alpha & Omega N-channel logic-level MOSFET, SOT-23 package. Gate-driven by the output of U1B (timer comparator) via Q3 and RC filtering. Switches pump negative lead; sources ~0.25–0.3 A pump current at 5 V (drain to G528 pump negative). R15 pull-down ensures gate remains low during startup/brownout.

**DMP2065UQ-7 (Q1, Q3, gate-drive MOSFETs)**  
Diodes Incorporated P-channel logic-level MOSFETs, SOT-23 package (two units). Q1 charges the HOLD capacitor when DET_N is pulled low (gun current detected). Q3 sources the gate of Q2 during the delay-timer phase (when HOLD > VDELAY). Both are fed from a mid-supply bias node to support proper gate drive.

**B340A-E3/61T (D1, Schottky diode)**  
Vishay 3 A 40 V Schottky diode, SMA DO-214AC package. Reverse-biased (anode to Q2 drain, cathode to 5 V rail). Suppresses pump motor back-EMF transients during Q2 shutoff, clamping to the 5 V supply rail.

**ACS758 (current sensor)**  
Hall-effect current-sense module (Great IT Electronic Components Store, ACS758LCB-050B variant). 5 V supply, 40 mV/A output, ±50 A bidirectional. Detects combined gun current draw on main high-current path; output signal feeds U1A (gun-current comparator) non-inverting input via R1/C5 sensor filter. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 21.

**RV1 (2 kΩ, 25-turn trimmer, gun-detection threshold)**  
Bourns 3296W potentiometer. Sets the threshold voltage for U1A comparator (inverting input), controlling the ACS758 gun-current detection point. Typical range ~2.21–2.80 V; final calibration TBD during field commissioning. R19 (220 kΩ) biases threshold toward the safe (high) direction if RV1 wiper opens.

**RV2 (100 kΩ, 25-turn trimmer, pump off-delay)**  
Bourns 3296W potentiometer. Controls the discharge resistor for the HOLD capacitor after gun current stops, setting the pump shutoff delay. Target 350 ms nominal; range ~35–574 ms adjustable via RV2. Calibrated during commissioning. R21 (1 MΩ) provides a safe discharge path if RV2 wiper opens.

Both Bourns 3296W trimmers are hand-soldered THT components; horizontal orientation preferred. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), PCB THT BOM.

**R18 (ACS pulldown, 100 kΩ)**  
Yageo RC0805FR-07100KL, 1% tolerance, 0805 package, SMT. Must be fitted. Pulls the ACS_OUT signal low if the ACS758 module is unplugged, forcing the system into a safe (pump off) state. Specified in PCBWAY_SMT_BOM with "MUST BE FITTED" requirement.

**FB1 (ferrite bead, logic filtering)**  
Murata BLM21PG221SN1D, 220 Ω @ 100 MHz, 0805 package. Series ferrite bead on the logic / sensor 5 V rail to reduce high-frequency noise coupling from the pump driver branch. Part of the separation between pump power (high current, switching transients) and comparator / sensor signals.

**DET_N (gun-detection signal net)**  
Active-low signal generated by U1A comparator output, pulled down when ACS758 gun-current input exceeds the RV1 threshold. Triggers Q1 to charge HOLD and illuminates LED2 (gun-active indicator). PRIME button grounds DET_N directly for manual activation.

**HOLD (gate-charge storage capacitor)**  
Capacitor voltage on the gate-drive timing network, charged by Q1 when DET_N is asserted and discharged by RV2/R21 after gun current stops. U1B compares HOLD to VDELAY to control the pump off-delay timer (target ~350 ms).

**VDELAY (timer threshold voltage)**  
Mid-supply buffered reference voltage (~1.0–1.03 V typical) generated by a resistive divider and Schmitt feedback network. U1B compares HOLD against VDELAY; when HOLD falls below VDELAY, the timer comparator signals pump shutoff after the RV2-set delay interval.

**VMID (mid-supply reference)**  
Buffered 2.5 V rail (nominal) derived from the 5 V supply via resistor divider, used as the bias node for the Q1/Q3 P-channel gate drivers and as the upper reference node for the VDELAY Schmitt network.

**1812L150/16DR (F1, PTC thermal-cutoff fuse)**  
Littelfuse resettable PTC (positive temperature coefficient) fuse, 1812 package, 1.5 A hold current at 16 V. Series-connected in the pump-drain path to protect Q2 and pump against overcurrent fault conditions. Self-resets once overcurrent is removed and device cools.

**Pump driver (Q2 + D1 + F1 + gate filtering)**  
Functional unit: Q2 MOSFET gate driven by U1B (timer) output through Q3 buffer and RC filter → Q2 sources pump current from 5 V → flyback diode D1 (clamping inductive transients) + PTC fuse F1 (in series for fault protection) → pump-negative return to ground. Pump sees ~5 V − (Q2 RDS(on) + F1 drop) ≈ 4.7–4.9 V under full load.

**LEDs (power, status indicators)**

- **LED1 (green, L-934GD):** POWER indicator. Always on when 5 V supply present.
- **LED2 (yellow, L-934YD):** GUN ACTIVE indicator. Illuminated when U1A (gun-current comparator) output goes low and pulls DET_N down (ACS758 detects gun current above RV1 threshold).
- **LED3 (red, L-934ID):** PUMP ACTIVE indicator. Illuminated when Q2 MOSFET gate is high (pump running).

All 3 mm through-hole, current-limited via series resistors (typical 1–2 kΩ for 5 V, 10–20 mA per LED). Kingbright OEM. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), PCB THT BOM.

**PRIME button (SW1, momentary manual pump trigger)**  
Omron B3F-1000, 6×6 mm tactile switch. Momentary pushbutton; grounds the DET_N signal when pressed, forcing Q1 to charge the HOLD capacitor and Q2 to turn on the pump (same delay-timer logic as normal gun detection). Released → comparator resumes control based on ACS758. Manual pump-start function for reservoir priming, line clearing, or override. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), PCB THT BOM.

**J4 (AUTO/FORCE-ON jumper)**  
2-pin, 2.50 mm-pitch position, DNP. No-respin fallback if the ACS758 can't detect a low-current head. Open = automatic sensing; shorted = pump forced on through the normal protected timer/driver path. Wire it to a maintained `AUTO / FORCE ON` switch, or to dry-contact trigger poles in parallel. Never connect a motor lead or PWM node directly.

**Connectors (power)**

- **XT60H (10 pairs):** High-current DC connector (60 A rated), gold-plated. Used for the battery-to-breaker interface: the **XT60H loop** runs out below the stick and is the full battery disconnect (unplug it for storage). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 9.
- **XT30U (gun channels):** 30 A rated connector pair for XT30 (upgrade variant U for improved contact). Connects main PCB / power distribution to individual gun heads. 10 pair ordered. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 23.
- **JST-XH 2.54 mm:** Connector family for low-power signal and power distribution. Used for PCB interfaces:
  - **J1:** 2-pin JST-XH header, 5V and GND from Buck A.
  - **J2:** 3-pin JST-XH header, ACS758 interface (GND, Vcc 5V, signal output).
  - **J3:** 2-pin JST-XH header, pump output (PUMP+, PUMP_SW_NEG).
  - See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 10.

**C1 (electrolytic capacitor, through-hole)**  
Rubycon 100 µF, 16 V, low-ESR, radial D5 P2.0 footprint. Smoothing / bulk capacitance on 5 V Buck A output (handles pump start transient current).

**C6, C7 (high-value ceramics)**  
Timing and filtering capacitors for comparator and gate-drive networks. Tight placement (C7/U2 spacing 0.02 mm) requires high manufacturing tolerance; flagged in manufacturing QA.

**Nickel-plated steel tabs (battery interconnect)**  
Welding tabs for 18650 cell interconnection in 2S5P pack. 2.6 cm tabs, 10 pcs per unit, 3 units ordered (30 total, allowing 5 distributed bridges per cell in each series string). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 11.

**Fish-paper insulators (18650 cell gaskets)**  
Barley-paper insulation rings for isolating 18650 cells in pack. Prevent accidental shorts and manage current distribution. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 24.

**PCB dimensions**  
50 × 40 mm, two-layer, 1.6 mm thick, 1 oz copper, green solder mask, white silkscreen, lead-free HASL finish.

**SMT (Surface Mount Technology)**  
Components placed and soldered by PCBWay on top side of PCB. 41 placements in standard v1.2 assembly.

**THT (Through-Hole Technology)**  
Components soldered by Joey (hand-soldering) after PCBWay delivery. Includes JST headers, trimmers (RV1, RV2), tactile button (SW1), LEDs, and electrolytic capacitor (C1).

**DNP (Do Not Place)**  
Components designated DNP are not populated by factory; left as bare pads. Includes J4 (AUTO/FORCE-ON jumper, reserved for field fallback) and R22 (unused pull-up resistor in design).

**PCBWay**  
Vendor for custom PCB fabrication and SMT assembly. Orders:
- **Original:** [original PCB order] (v1.1, defective U1 footprint, fabricated but not assembled).
- **Replacement:** [PCB order] (v1.2, corrected U1 footprint, 5 boards; 2 assembled, 3 bare).
- **Group order:** [order group] (consolidates all components and stencil).
- **Assembly reference:** [assembly order] (group assembly tag).

**Gerber**  
Industry-standard format for PCB fabrication artwork. Contains layers: F_Cu (top copper), B_Cu (bottom copper), F_Mask (top solder mask), F_Paste (paste-layer for SMT stencil), F_SilkScreen (legend), Edge_Cuts (board outline). Delivered to PCBWay as compressed ZIP archive.

**BOM (Bill of Materials)**  
PCBWAY_SMT_BOM.csv: 41 lines, one per SMT component, with part number, value, footprint, quantity, reference designator.

**CPL (Component Placement List)**  
PCBWAY_SMT_CPL.csv: 41 lines with X/Y centroid coordinates (mm), rotation angle (degrees), component reference designator. Used by PCBWay pick-and-place machine.

**Stencil**  
Metal frame with apertures matching paste-layer (F_Paste.gbr), used to apply solder paste to PCB before component placement. Standard thickness 0.15 mm; stencil cost ~$25 per design per fab run.

---

## Fluid System & Pump

**Peristaltic pump (G528)**  
GROTHEN G528, 6 V DC nominal, 150 mL/min flow, 3×5 mm tubing (pump inlet/outlet barb sizes). Self-priming, low-shear design suitable for bubble solution without foaming. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 1.

**G528 transfer pump**  
Alternative name for GROTHEN G528 (emphasis on "transfer" role: moves bubble solution from reservoir through gun heads).

**Bubble concentrate**  
Commercial concentrate (JOYFY 32 OZ, US Store, order ref [order ref removed]) diluted per manufacturer instructions for bubble solution. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 16. Also called "bubble solution" when mixed.

**Hydration bladder (1 L)**  
Food-grade TPU flexible water reservoir, 1 L capacity, with detachable 101 cm factory hose and auto-sealing bite valve. UWWWMM Official Store, blue color. Repurposed as BubbleLink bubble-solution reservoir. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 15.

**Silicone tube (3.5 × 5.5 mm)**  
Transparent food-grade tubing, ID 3.5 mm, OD 5.5 mm, 5 meters per spool. Used throughout fluid path (pump inlet, outlet, distribution to guns, recirculation bypass). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 13.

**Hose fitting assortment (nylon barbs, tees, reducers)**  
Assortment of plastic barbed connectors for coupling silicone tubing. Includes tees (Y-splitters), reducers (ID steps), and straight connectors. The pack plumbing uses three tees (inlet tee, outlet tee 1, outlet tee 2), and each dual-head gun uses one more. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 14.

**Check valve (4 mm)**  
One-way plastic valve, 4 mm barb ID, manual opening pressure 0.003 MPa. Installed in recirculation bypass line to prevent reverse flow from gun outlet back toward pump. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 22.

**Recirculation loop (bypass)**  
Tubing path: outlet tee 1's side branch → printed slide clamp (restrictor) → check valve (arrow toward the inlet) → inlet tee → pump inlet. The main flow continues from outlet tee 1 to outlet tee 2 and the two gun channels. Maintains constant low-pressure circulation when guns are not firing (primes lines, keeps pump cool). Target bypass pressure 0.2–0.5 psi (opens when gun outlet backs up).

**Cracking / opening pressure**  
Pressure threshold at which recirculation check valve opens and allows fluid bypass. Typically 0.003–0.01 MPa for low-pressure systems.

**Umbilical (gun umbilical, umbilical tether)**  
Bundled cable assembly connecting PCB/pack to each bubble-gun head. Contains:
- Two 16 AWG silicone power conductors (red positive, black negative).
- One 3.5 × 5.5 mm silicone fluid hose.
- One 550 paracord (load-bearing tether; carries drop load, not electrical current).
- All four bundled in 8–10 mm braided PET sleeve.
- Connectors: XT30U + fluid barb, with a printed umbilical brick at each end.

Four-foot umbilical is standard (~9.8 mL priming volume). Six-foot variant experimental (~14.5 mL priming volume).

**Umbilical brick (printed)**  
ASA (or PETG) block at each end of each umbilical (×4 in all). Strain relief: the XT30U drops into an open-top pocket and is strapped with a zip tie, the 16 AWG pair and the tube run in grooves under narrow zip ties, and the paracord ties through the outer hole (the inner hole ties to the stick or the gun). It replaces the earlier "connector block" / pump/hose/tether block and TPU strain-relief boots.

**ASA**  
The rigid printing material for the stick (tube, cap, sled, cup, bezel, skirt); older parts can be ASA or PETG. Prints best on the enclosed K2 Plus; shrinks about 0.5-0.7%, so re-run the fit coupon in ASA. See the print guide.

**TPU cushions (parts 36-38)**  
Replace the 1 mm foam: two compliant battery pads that click onto the cap's ribs, a 2 mm pump mat with eight drain holes, and a set of six flat 5 × 30 mm shim strips (0.6, 1.0 and 1.5 mm thick) cut to fit where a board rattles.

**Slide clamp (printed)**  
ASA (or PETG) tube clamp, ×3. One design serves as the bypass restrictor and both channel shutoffs. Slide toward the arrow to close: ~8 mm of coarse travel, then 22 mm of fine adjustment, sealing at 0.6 mm. The shallow ramp self-locks (no screw); wet-test that it holds. Replaces the earlier "pinch clamp" wording.

**Bladder outlet**  
1 L hydration bladder's fluid-discharge port. Factory hose (101 cm, detachable) is cut short inside pack and reduced to 3.5 × 5.5 mm silicone tubing via assortment reducer fitting.

**Germall Plus**  
Liquid antimicrobial preservative (100 g bottle, Shop1105380267 Store, order ref [order ref removed]). Prevents mold/algae growth in stored bubble solution (dosage TBD, estimated 0.1–0.2% by weight). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 17.

---

## Wearable Pack & Integration

**Hydration pack (MAX LED M Style backpack)**  
MAX LED Official Store "M Style" LED pixel backpack (48.16 USD). Carries the BubbleLink system: the printed **stick** (battery, electronics and pump) standing upright beside the 1 L reservoir. Interior geometry not yet measured (the "~34 × 20 × 7 cm" figure is an AI estimate of the exterior). Exterior LED matrix programmable via Bluetooth (secondary feature; not part of core bubble functionality). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 20.

**LED pixel backpack (M Style)**  
Alternative name for the MAX LED M Style backpack. "Pixel" refers to individually-addressable LED array on exterior.

**Stick (printed pack unit)**  
The whole pack apart from the bladder, as one upright printed column about 99.6 × 79.8 × 220 mm (3.9 × 3.1 × 8.7 in), standing beside the bladder. CAD in `hardware/printed/` (designed 2026-10-14; not yet printed or test-fitted). Two umbilicals leave from its bottom. Sections, top to bottom:
- **Cap:** the control head. The CTRL PCB hangs underneath; LEDs shine through glue-filled 3.6 mm through-holes; PRIME is a TPU plunger under a TPU boot, guarded by an ASA bezel and hard-stopped after 0.75 mm; RV1/RV2 adjust through tape-covered windows; the voltmeter and USB-C charge port are on top. A TPU ring seals radially against the tube (not yet wet-tested); 2× M3×10 screws with TPU washers (nuts in slots behind the skirt) keep it on; two compliant TPU battery pads on its ribs press the cell holders.
- **Tube:** the dry section, with raised BubbleLink lettering on its right-hand wall (98.8 mm wide, 99.6 with the lettering). Its floor is the **bulkhead**, the wet/dry divider.
- **Sled:** slides out of the top. The 2S5P block stands beside a central spine; the breaker stands behind a cross panel, 2 mm from the outer wall (reset it with the sled out), the BMS on edge along the back wall, and Buck A, Buck B and the ACS758 in compartments on the front of the panel.
- **Bulkhead grommet:** two-piece TPU grommet with knife-cut slits that the cables pass through, with an ASA drip skirt below it. A splash baffle on its own; fill its top face with neutral-cure silicone once the wiring is final.
- **Tether anchors:** two pairs of 5 mm holes low in the cup's outer wall. The pack-end umbilical brick ties to one pair with a short paracord loop, so a dropped gun pulls on the cup, not the hose or wires.
- **Cup:** the wet chamber (pump on a TPU mat, three tees, check valve, bypass slide clamp). Bolts on from below with 4× M3×12 into nuts in the bulkhead; drains through its floor.

**Cell holders (MID and TERM)**  
Printed 5×2 offset cell holders for the 2S5P block, 19.9 mm pitch, with flat end faces so the cap's pads bear across the full width. MID caps the series end; TERM carries the pack + and − buses. Replaces the earlier Cults3D spacer remix. Printed after the **fit coupon**, which sets the cell-bore and XT30U-pocket clearances.

**OFF switch**  
Unplugging the **XT60H loop** below the stick (open the bag to reach it). It turns off the bucks, PCB, voltmeter and guns, and it's also the full battery disconnect for storage; the BMS stays on the battery either way. The breaker's controls are only reachable with the sled out.

**Tracer cosplay**  
Reference to Overwatch character Tracer armor shell + integrated bubble guns (aesthetic context for the LED integration and gun cosplay skins).

**Braided PET sleeving (umbilical sleeve)**  
Insulation wrap for umbilical bundles. 5 meters, 10 mm width, black color. Protects power and fluid lines from abrasion. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 18.

**550 paracord (load-bearing tether)**  
Mil-spec nylon cord, 7-strand, 4 mm diameter (550 lb tensile strength nominal; "550" is the spec number). 15 meters ordered. Each gun umbilical includes one 4-foot section (mechanical tether, load-bearing). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 19.

**Donor head (bubble gun head)**  
Bubble-producing mechanism extracted from donated children's toy bubble guns. Typically contains a motor-driven wand or rotor. Variable current draw (estimated 3–6 A peak) depending on design, speed, and bubble concentration.

**PWM (Pulse Width Modulation)**  
Variable-speed control of gun motors via duty-cycle switching (not implemented in v1.2 PCB; guns run at fixed voltage only, no speed control). Historically considered but removed from MVP scope.

---

## Measurement & Characterization

**Overvolting (overvolted operation)**  
Running 6V-nominal pump or guns at higher voltage (e.g., 7.2–8.4 V from 2S battery directly) to increase flow rate or speed. Increases current draw and thermal load; acceptable for short festival bursts but requires thermal qualification.

**Lowest gun PWM**  
One of the nine pending bench gates: confirm the ACS758 detects the slowest/lowest-current head Joey will actually run. If it can't, use J4 FORCE-ON.

**Bench gate**  
Manual acceptance criterion that cannot be verified by simulation and requires physical measurement or field testing. Examples: thermal rise, EMI immunity, brownout waveforms, vibration tolerance. Nine bench gates remain pending. Joey couldn't run them before ordering because parts hadn't arrived; they're done during bring-up.

**FORCE-ON (manual override)**  
The pump is forced on regardless of sensed gun current by shorting J4 (via a maintained switch or dry-contact trigger poles). This is separate from PRIME, which is a momentary button.

**Threshold (detector threshold, gun-detection threshold)**  
Voltage level (set via RV1 trimmer potentiometer) at which U1A comparator switches DET_N from HIGH to LOW, triggering pump activation. Must be set slightly above ACS758 zero-current output voltage (~2.5 V nominal); design hysteresis ~4.42 mV.

**Hysteresis (comparator hysteresis)**  
Voltage deadband between U1A LOW-to-HIGH and HIGH-to-LOW switching points (typically 4–10 mV on comparators; TLV1822 nominal package hysteresis ~4.42 mV). Prevents rapid chattering due to noise and glitches on the ACS758 output.

**Pump delay (shutoff delay, off-delay)**  
Time (40–450 ms, nominal 350 ms) that pump continues running after gun current drops below ACS758 threshold. Implemented via RC timing network with RV2 potentiometer feedback resistor (corrected from 2.2 MΩ to 10 MΩ in v1.2 to avoid tolerance-dependent error at maximum delay). Prevents pump chatter on brief trigger taps.

**Dual-gun concurrent operation**  
Simultaneous firing of both XT30U gun channels from a single ACS758 current sensor (parallel gun load on main 12 AWG path). Comparator threshold must detect combined current; no separate left/right channel signal routing implemented.

**Soft-start (startup behavior)**  
Gradual voltage ramp on 5 V supply (from buck module) to prevent inrush damage to PCB components. Design must avoid spurious pump activation during startup (supervisory cutoff TLV803 addresses this).

**Brownout (brownout condition, brownout clamp)**  
Momentary battery voltage collapse (e.g., from inrush load or loose contact). TLV803 supervisor monitors 4.38 V threshold; below this, pump is clamped OFF and comparator output disabled. Margin 180 mV nominal (168–196 mV modeled).

**EMI (electromagnetic interference)**  
Spurious signals from external sources (Wi-Fi, cellular towers, motor noise) that could falsely trigger comparator or cause false pump activation. Filtered via RC networks on comparator input; bench gate B-006 requires 10,000-cycle EMI immunity test.

**Motor EMI / flyback (motor back-EMF)**  
Transient voltage spike generated when pump motor switches off (inductive kick). Suppressed by B340A Schottky diode (D1) reverse-biased across Q2 drain, clamping to 5 V rail. "Flyback" refers to back-EMF energy path through diode.

**Thermal rise**  
Temperature increase above ambient during continuous operation. Design target: <20°C thermal rise on Q2 MOSFET and F1 PTC at continuous 0.3 A, 50°C ambient.

**Vibration testing**  
Physical shake test to confirm connector/harness mechanical integrity under festival dance-floor vibration. Deferred to field commissioning (bench gate B-009).

---

## Acronyms & Abbreviations

| Acronym | Definition |
|---------|-----------|
| 2S5P | 2 cells in series, 5 parallel (10 total 18650 cells) |
| AWG | American Wire Gauge (wire thickness) |
| BMS | Battery Management System |
| BOM | Bill of Materials |
| CAD | Computer-Aided Design |
| CPL | Component Placement List (centroid file for PCBWay) |
| DFM | Design for Manufacturability (factory review) |
| DRC | Design Rule Check (KiCad validation) |
| DNP | Do Not Place (component reserved for field commissioning) |
| EQ | Engineering Query (PCBWay design-review question) |
| ESR | Equivalent Series Resistance (capacitor spec) |
| FAA | Federal Aviation Administration (battery transport compliance) |
| GND | Ground (0 V reference) |
| HAL | Hall-effect (ACS758 sensor principle) |
| ID | Inner Diameter (tubing spec) |
| LED | Light-Emitting Diode |
| Liter (L) | Volume unit (1 L = 1000 mL) |
| LSI | Large-Scale Integration (IC package category) |
| MHz | Megahertz (frequency) |
| MPN | Manufacturer Part Number |
| mV | Millivolt (1/1000 volt) |
| MVΩ | Megaohm (1 million ohms) |
| OD | Outer Diameter (tubing spec) |
| OEM | Original Equipment Manufacturer |
| PCB | Printed Circuit Board |
| PD | Power Delivery (USB USB-C standard) |
| PTC | Positive Temperature Coefficient (self-resetting thermal fuse) |
| PWM | Pulse Width Modulation (variable-speed control) |
| RDS(on) | Drain-Source On-resistance (MOSFET spec) |
| RF | Radio Frequency (EMI context) |
| SOIC-8 | Small-Outline Integrated Circuit, 8-pin package |
| SOD-123 | Small-Outline Diode package |
| SOT-23 | Small-Outline Transistor, 3-pin (MOSFET/BJT standard) |
| STL | Stereolithography (3D-print model file format) |
| THT | Through-Hole Technology (hand-soldered components) |
| TI | Texas Instruments (semiconductor manufacturer) |
| USB-C | Universal Serial Bus Type C (connector/power standard) |
| Vcc | Supply voltage (positive rail) |
| Vs | Versus (comparison) |
| Ω | Ohm (unit of electrical resistance) |
| µF | Microfarad (capacitance unit, 1/1,000,000 farad) |

---

## Wire & Cable Nomenclature

**12 AWG silicone wire (main power bus)**  
Red and black silicone-insulated copper conductor, 12 AWG gauge (2.08 mm diameter nominal), 3 meters each color. High-temperature rated for pump/gun current. See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 7.

**16 AWG silicone wire (gun branch)**  
Red and black silicone-insulated, 16 AWG gauge, 5 meters each color. Used for umbilical branches (smaller gauge than main 12 AWG for weight savings; each gun XT30U rated 15 A continuous, 16 AWG adequate). See [ORDER_LEDGER](parts/ORDER_LEDGER.md), item 8.

**M6 stud (circuit breaker terminal)**  
6 mm metric threaded post (male) protruding from circuit breaker terminal block. Ring lugs (SC10-6) bolt onto these studs with washers and nuts.

**Pigtail (motor harness suppression)**  
Short length of wire or twisted pair connecting a component directly to another; used when off-board connection needed (e.g., ACS758 module wiring, motor suppression capacitor/diode leads at pump terminals).

---

## Design Versions & Release History

**v1.1 (initial release, superseded)**  
First PCB release by PCBWay (order [original PCB order]). Defective U1 footprint (4.3 mm row spacing vs. required 5.4 mm); fabricated 5 boards but assembly held pending correction. Frozen 2026-08-18.

**v1.2 (current, corrected)**  
Replacement PCB release (order [PCB order]) with corrected U1 footprint (TI D0008A, 5.4 mm row spacing). Rerouted nearby traces, regenerated ground pour. All functionality unchanged vs. v1.1. Frozen 2026-09-09. Ordered 5 boards; 2 assembled by PCBWay, 3 bare (waiting for 2026-10-29 deadline).

**Release package (v1.2 complete)**  
`BubbleLink_CTRL_v1_2_PCBWay_Complete.zip` (or `BubbleLink_CTRL_v1_2_PCBWay_RELEASE`): complete design handoff with Gerbers, BOM, CPL, assembly notes, verification reports, and source files. SHA-256 `3c64f97583e2ebbbbe63c5a76e57f49cb4ee16553018ccf1ec2cc02d671e801c`. 66 files, 50 automated QA checks PASS.

**Manufacturing gates**  
Verification checkpoints:
- 49 checks (v1.1) → 50 checks (v1.2) automated pass.
- 9 bench-only manual gates (B-001 through B-009) deferred to field commissioning.

---

## Related Documentation

- **[ORDER_LEDGER.md](parts/ORDER_LEDGER.md):** Authoritative list of all 25 purchased items, part numbers, sellers, quantities, prices.
- **[07-pcb/overview.md](07-pcb/overview.md):** Functional circuit topology, power flow, current sensing, control behavior.
- **[07-pcb/bringup-and-acceptance-test.md](07-pcb/bringup-and-acceptance-test.md):** Step-by-step bring-up procedure and 9 bench-gate specifications.

---

## Word Count

~4,300
