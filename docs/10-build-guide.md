# BubbleLink Build Guide

Complete step-by-step assembly procedure from parts-on-the-bench to festival-ready bubble-gun system. This guide covers incoming inspection, battery assembly, electrical harness construction, PCB and controller setup, fluid system assembly, donor gun integration, LED backpack assembly, and final testing. The entire build requires 25–40 hours of hands-on work over approximately **two weeks** (compression from the original four-week estimate due to the 2026-10-29 hard deadline). **Status as of 2026-10-14:** AliExpress parts on hand; PCBs shipped ETA **Oct 15–18**. Printed-part CAD is done (the upright "stick", see [09-printed-parts.md](09-printed-parts.md) and [hardware/printed/README.md](../hardware/printed/README.md)); nothing has been printed or test-fitted yet. Prep work (cell matching, 3D printing, harness prep) can start immediately. PCB assembly begins after board arrival. **Target completion: 2026-10-29** (the target festival 2026-10-30 to 31).

## Quick Reference

**Required tools/consumables per step:**
- Spot welder or nickel-tab soldering rig
- Multimeter (voltage, current, continuity)
- Oscilloscope (recommended for PCB calibration)
- Soldering iron + solder and solder wick
- Wire strippers, crimpers (for ring terminals)
- Hot-water bath or heat gun (for hose warm-stretching)
- Narrow 2.5 mm zip ties
- Electrical tape, electrical shrink tubing
- 3D printer (Creality K2 Plus for the tall ASA parts, Bambu A1 for small parts and TPU), ASA and TPU filament (PETG also works for the older cell holders, clamps and bricks); see *Printing in ASA* in the [print guide](../hardware/printed/README.md)
- Printed-part hardware: 6× M3 stainless socket-head screws from the HVAKHVA kit (2× M3×10 each with an M3 flat washer over its TPU washer; 4× M3×12 each with an M3 split lock washer) + 6 M3 nuts (4 in the bulkhead's hex pockets, 2 in the cap's slots) glued in, a 2.5 mm hex key long enough to reach about 46 mm up the cup columns (no anaerobic threadlocker near ASA; a drop of CA on the screw tip is safe), glue (CA/hot glue/neutral-cure silicone; acetone for ASA-to-ASA joints), clear hot glue or UV resin for the LED windows, scissors for the TPU shim strips, and a small screwdriver for the trimmers

**Build order to 2026-10-29:**
1. **Now:** check or buy the PCB THT parts (no purchase record). Get written the target festival approval. Bench-test Buck A (<5.25 V under load) and the pump (marked 6 V, <0.3 A at 5 V). Incoming inspection and cell matching.
2. **Print:** the fit coupon, cell holders and slide clamps, then the stick parts and umbilical bricks.
3. **Build the battery.**
4. **Boards arrive (est. Oct 15–18):** PCB THT soldering and bring-up.
5. **Tear down the guns** (pick 4 matched heads).
6. **Electronics into the sled.**
7. **Fluid and umbilicals.**
8. **First fire and tuning.**
9. **Bench gates** and system tests.
10. **Done Oct 29.**

---

## 1. Incoming Inspection

### Verify all AliExpress parts against ../parts/ORDER_LEDGER.md

**Battery subsystem (critical variants):**
1. **2S 40A BMS** (IC GOGOGO Store, [price])
   - Verify label reads **Li-ion 8.4V 40A**, NOT LiFePO₄ 3.2V
   - If unmarked, check voltage: should output ~8.4 V when fully charged 2S pack connected
   - Common-port design: B− (group 1 −), BM/B1 (group 1 +/ group 2 −), B+ (group 2 +), P− (load −), P+ (load +)

2. **6V GROTHEN G528 pump** (GROTHEN Official Store, [price])
   - Verify motor housing marked **6V** (NOT 12V; artwork on some units misleads)
   - Measure DC resistance of motor coil: should read ~10–15 Ω
   - Included tubing: **3 mm ID × 5 mm OD** (kept as pump connection reference)
   - Bench test: should draw **<0.3 A at 5 V**
   - Measured 2026-10-14: 2 × 1¾ × 1½ in at its thickest; it fits the cup's 52 × 46 mm pocket (measure your own before printing the cup)

3. **2S 4A USB-C boost charger** (SZHJW Technology Store, [price])
   - Verify input USB-C connector and output spade terminals
   - Test with a 5V supply: should output ~8.4 V when connected to 2S BMS P+/P− ports

4. **5V USB buck converters** (YxPC Store, qty 2, [price] each)
   - No datasheet: assume 6–20 V input, 5V adjustable output, ~1–2 A capacity
   - **CRITICAL:** before use, dial pot to exactly **5.0 V** and verify with multimeter
   - **Buck A** powers the controller PCB and pump motor (~5.0–5.1 V; PCB qualified input 4.75–5.25 V)
   - **Buck B** powers the LED backpack's USB input
   - Bench-test Buck A under load: must stay **below 5.25 V**
   - Measured 2026-10-14: 1 in along the port, 5/16 in thick. **Width not measured** (17 mm assumed); measure it
   - Buck A's output is soldered straight to the J1 lead; Buck B has no wiring on its output side (the backpack plugs into its own USB-A port through the tube wall)

**Electrical subsystem (critical variants):**
5. **ACS758LCB-050B current sensor** (Great IT Electronic, [price])
   - Verify label/silkscreen shows **050B** (±50A, 40 mV/A), NOT 100B
   - Module connector: should be JST or screw terminals; verify 5V, GND, signal pins
   - Measure output voltage at zero current: should read ~2.5V (typical resting point)

6. **30A manual-reset circuit breaker** (YONGRUN Store, [price])
   - Verify **Type B-30A** rating and 12–48 V DC compliance
   - Confirm terminal studs are **M6** (6 mm diameter) for ring-terminal fit
   - Measured 2026-10-14: 1⅝ in square plate, 4 in (102 mm) long, 1⅝ in thick (the listing's 72 × 48 × 44 mm was wrong), plate holes 1¼ in apart. Inline type: studs at both ends, red reset lever and red push-to-trip button on the square plate
   - Do NOT apply power until ring terminals are crimped

7. **M6 ring terminals** (SC10-6, solder-filled, match for 12 AWG wire)
   - Verify **10 mm² barrel** (oversized for 12 AWG; solder-fill the barrel and strain-relieve rather than relying on crimp alone)
   - Confirm hole diameter matches M6 studs (6.0–6.5 mm)

**Fluid subsystem (critical variants):**
8. **1L water bladder** (UWWWMM Official Store, [price])
   - Verify **1L** capacity (not 2L unless intended)
   - Confirm included **detachable 101 cm hose** with bite-valve shutoff
   - Test hose end for ID/OD: should accept 4 mm hose-fitting connectors or require a reducer

9. **4mm plastic check valve** (BigBigBear Tech Store, [price])
   - Verify **opening pressure 0.003 MPa** (0.435 psi) from manual
   - Arrow on valve body points toward inlet (pump inlet return); critical for orientation
   - Test by applying gentle air pressure from the inlet side; should barely open under thumb pressure

10. **3.5 × 5.5 mm silicone tubing** (Shop1105214603, [price])
    - Measure actual ID/OD; should match 3.5 × 5.5 mm nominal
    - Inspect for cracks, discoloration, or brittleness

11. **Automotive hose-fitting assortment** (Shop1103411025, [price])
    - Identify **#68401** straight 1/8" unions and **#68409** 5/32" tees in compartment
    - Confirm black nylon material and barb sizes
    - Count the tees: the pack plumbing needs **three**, plus one per dual-head gun

**Connectors & wiring (critical variants):**
12. **XT60H battery connectors** (Shop911130012, [price])
    - Confirm **XT60H** (upgraded version), NOT standard XT60
    - Count: should have 2 pairs (male + female per pair) minimum; confirm 10 pairs shipped

13. **XT30U gun-channel connectors** (Xing Yiao Store, [price])
    - Verify **XT30U** or **XT30** (NOT MR30)
    - Count pairs; intended qty 10 but "5 pairs plenty" per design note

14. **12 AWG silicone wire** (AuHo DIY Store, [price])
    - Verify gauge and color: **Black and Red, 3 m each** (or 5–10 m total)
    - Tinned copper, stranded; should be flexible

15. **16 AWG silicone wire** (AuHo DIY Store, [price])
    - Verify color and gauge: **Black and Red, 5 m each**
    - For gun-channel harnesses

16. **550 paracord 4 mm, 15 m** (FFlyBG Store, [price])
    - Load-bearing tether for umbilical support; black color

17. **JST-XH 2.54 mm connector kit** (Daevkaema Global Tools, [price])
    - Verify kit includes pre-crimped male/female pairs in multiple pin counts
    - Should have 2-pin, 3-pin, and 4-pin housings

18. **Braided PET sleeving 10 mm, 5 m** (XIDA Electric Store, [price])
    - For strain relief on solder joints

**PCB and controllers (critical components):**
19. **PCBWay BubbleLink CTRL v1.2 board** (2 assembled + 3 bare, v1.2 revision)
    - Verify board revision **v1.2** (footprint correction for U1 from v1.1)
    - Check SMT assembly: U1 (TLV1822QDRQ1), U2 (TLV803E), MOSFETs (Q1/Q3 DMP2065UQ, Q2 AO3400A), diode D1 (B340A), fuse F1 (1812L150)
    - Confirm C9 and R18 are **fitted** (populated), NOT DNP
    - Confirm J4 and R22 are **DNP** (not populated)
    - Through-hole parts (RV1, RV2, LEDs, J1–J3, SW1, C1) user-installed. **There's no purchase record for them: check or buy them now**

20. **Nickel-plated steel battery tabs** (AllThingsHome, qty 3 packs = 30 total, [price] each)
    - Verify **2.6 cm length, 0.15 mm thick minimum** by caliper
    - Count: should have 30 total (10 per pack)

21. **Fish-paper insulation gaskets** (IC GOGOGO CHANGELIN, [price])
    - 18650 positive-terminal rings; qty ~10

**Consumables & safety:**
22. **JOYFY 32 oz bubble concentrate** (JOYFY US Store, [price])
    - Verify bottle intact, label clear
    - Mix 1 part concentrate + 9–10 parts water per 1 L fill

23. **Liquid Germall Plus preservative** (Shop1105380267, [price])
    - 100 g bottle; add ~1% to bubble solution for long-term storage

24. **COB LED strip 5V 2 m ice-blue** (KISUFU Lighting, [price]) [OPTIONAL]
    - For Tracer cosplay side panel; NOT part of bubble system

**Other measured parts (2026-10-14):** BMS 2½ × 1⅞ × ¼ in; ACS758 module 1½ × ~¾ × ⅛ in; USB-C charger 1½ in (plug direction) × 11/16 × ⅜ in, receptacle centred on the 17.5 mm short side (confirmed by Joey, 2026-10-15); voltmeter bezel about 1 5/16 in, body a hair over 1⅛ in, about 1 in deep or a bit more (the cap allows 30 mm). **Measure the voltmeter's idle current once** with a multimeter on the mA range (unmeasured; small LED meters typically draw tens of mA).

**Mark any missing or incorrect variants in an "Incoming Issues" list; do NOT proceed with assembly until verified.**

### Printed parts (start now)

Follow the print order in [hardware/printed/README.md](../hardware/printed/README.md):

1. Print the five **fit coupons** first, in ASA: `00_fit_coupon` plus the stick's rim, skirt, nut and ports coupons. Pick the tightest cell ring a 25R slides into by hand and the snug XT30U pocket, and check that the skirt slice drops into the rim slice with the TPU ring on that an M3 nut presses into both hex pockets, and, on the ports coupon, that the umbilical's XT30U male shroud slides into the well, the silicone tube pushes snugly through the hose hole, a USB-A plug seats fully through the window, and the XT60H male drops into its sleeve and stops under the lip. Set `cell_bore`, `fit_clear` or `sk_c` in `src/params.scad` (or use about 100.5% slicer shrink compensation on the K2 Plus) and rebuild the STLs with `build.sh`.
2. Print the **tube**, **sled**, **cell holders** (MID and TERM; they now have flat ends, so reprint any older ones) and the **slide clamps** (×3). Then **measure** the tube rim height (156 mm above the bulkhead plus 3 mm) and the assembled battery block (113.15 mm nominal): the coupons don't capture Z shrink. If the stack is off by more than 0.2 mm, edit `bp_ov` and rebuild only the cap and pads. Print the cap and battery pads after measuring.
3. Print the **stick parts** (tube, cap, sled, cup, PRIME guard bezel, grommet drip skirt, power key) in ASA (tall parts on the K2 Plus; run the fit coupon in ASA first) and the TPU parts (cap ring, grommet halves, PRIME boot, PRIME plunger, two screw washers, two compliant battery pads, the pump mat, the shim strip set, trimmer plug, USB-C plug, USB-A plug, two gun port caps, key blank, key gasket), then the **umbilical bricks** (×2, gun end only). The LED windows are through-holes, so any cap colour works. Nothing needs supports.

None of these parts has been test-fitted yet, so check fits as you go.

---

## 2. Battery Assembly (Days 1–3)

### 2.1 Cell matching and preparation

**Cells:** 10 × Samsung INR18650-25R (already owned; 2500 mAh, 3.6 V nominal, 10 A continuous)

1. **Measure each cell's voltage** with multimeter (open-circuit, no load):
   - Record all ten readings; should be within ±0.05 V of each other
   - If spread >0.1 V, charge all cells to 4.2 V via a hobby LiPo charger before proceeding
   - Goal: matched cells ensure balanced 2S5P operation and minimize BMS balancing current demand

2. **Test cell integrity:**
   - Inspect wrapper for tears, burns, or swelling; reject any compromised cells
   - Measure DC resistance (ESR) by discharging 1 A through the cell for ~10 ms and measuring voltage drop; should be <100 mΩ (high ESR indicates wear)

3. **Arrange cells in 2S5P configuration:**
   - Two rows of five cells each (2 series × 5 parallel)
   - Row 1: cells 1–5 (all at same voltage before welding)
   - Row 2: cells 6–10 (all at same voltage before welding)
   - Label rows with tape to avoid mixing during welding
   - **Orient the two rows in opposite directions:** row 1 (A) goes + toward one end and row 2 (B) goes − toward that end. If every cell faces the same way, it's 10P, not 2S5P

### 2.2 Spot-weld battery tabs

**Setup:**
- Printed cell holders, MID and TERM (original 5×2 offset design, 19.9 mm pitch, ~1.6 mm wrapper gap)
- **MID** caps the series end (every tab on that face is the midpoint); **TERM** carries the separate pack + and − buses. Keep the two rows' strips on TERM apart, with fish paper between them. The holders are mirror images; if the A/B letters don't line up, rotate MID 180°
- Nickel-plated steel tabs, 2.6 cm (qty 30 total); they reach both cell centres at the 19.9 mm pitch
  - Five independent series links connecting the two rows (positive of row 1 to negative of row 2)
  - Four links joining cells 1–5 in parallel (row 1)
  - Four links joining cells 6–10 in parallel (row 2)
  - Spares for rework

**Tab layout.** The rows face opposite ways, so each holder face carries one end of every cell:
- **MID face:** row A's + ends and row B's − ends. This face is the series midpoint: join **all ten** terminals on it into one mesh. Every neighbour, in-row and across rows, is 19.9 mm centre to centre, so each 26 mm tab spans one pair. Use at least 13 tabs: the 4 in-row links in each row plus 5 cross-row links, so each row-A cell connects straight to the row-B cell it sits next to. The BMS balance wire (BM/B1) goes here.
- **TERM face:** row A's − ends and row B's + ends. Join row A's five − ends with 4 tabs (pack −, BMS B−), and row B's five + ends with 4 tabs (pack +, BMS B+). **Keep these two buses apart:** no tab crosses between the rows on this face, and a strip of fish paper goes between them.
- That's 21 tabs of the 30; double up the in-row links nearest the BMS leads if you have spares.

**Order:**
1. Fit the fish-paper rings on the + ends, put the cells in the holders (check every row's direction twice), then fit the other holder.
2. TERM face first: the pack − bus (row A), then the pack + bus (row B). Check with a meter that the two buses read about 3.6-4.2 V apart and that no tab bridges them.
3. MID face: the full mesh. The TERM buses should now read about 7.2-8.4 V apart.

4. **Weld current:** ~80–100 A for 10–15 ms per spot (adjust for your welder calibration). If you solder instead of welding: use flux, an iron of 80 W or more with a large tip, pre-tin the tab, and keep each joint on the cell under 3 s; let the cell cool between joints. Weld if you can: hot, slow joints damage cells

5. **Post-weld inspection:**
   - No visible cracks or discoloration around welds
   - Tab contact resistance <5 mΩ per weld (measure with multimeter @ 10 A test)
   - No cell heating after 1 A load test for 30 seconds

### 2.3 BMS and power key connection

**BMS wiring (common-port design):**
- **B−:** Row 1 negative terminal (cell 1 −)
- **BM/B1:** Row 1 positive + Row 2 negative midpoint (junction between series links)
- **B+:** Row 2 positive terminal (cell 10 +)
- **P−:** System load negative (main harness return; it does not go to the breaker)
- **P+:** System load positive (to pin A of the power key socket; the charger also connects to P+/P−, upstream of the key)

**Wire the power key socket (XT60H male, in the cap):**
1. Wire the socket in line with the + feed (it switches the + line only):
   - Pin A: 12 AWG red to BMS P+ (row 2 +)
   - Pin B: 12 AWG red to the breaker input
   - The key (an XT60H female with a short 12 AWG U-loop across its two cups, hot-glued into the printed grip, part 26) bridges A and B. Key in is ON; key out is OFF (all loads off; the battery stays connected to the BMS, the charger and one pin of the key socket). Solder with slack to lift the cap; fit the rear zip-tie keeper behind the connector body, and put the TPU key blank (part 43) in the socket for storage
   - Black (return) goes from P− (row 1 −) to the return split, not to the socket
   - Insulate solder joints with heat-shrink or electrical tape
   - **CRITICAL:** verify polarity with multimeter before connecting ANY load

2. Insulate the battery terminals:
   - Wrap Row 1 − and Row 2 + with fish-paper rings or electrical tape to prevent short circuits
   - Cover all nickel tabs with electrical tape (except the connections to BMS terminals)

### 2.4 Label the battery

**Use permanent Sharpie on the cell holders:**
- "2S5P Samsung 25R"
- "7.2 V nominal, 12.5 Ah, 90 Wh"
- "Build date: [DATE]"
- "XT60 polarity: Red = +, Black = −"

On the bench, hold the block together with tape or a rubber band; in the stick, the tube walls hold it in.

---

## 3. Electrical Harness Assembly (Days 3–5)

### 3.1 Main distribution harness (12 AWG)

**Components:**
- 30A manual-reset circuit breaker with M6 studs
- 2× M6 ring terminals, 12 AWG size
- 12 AWG red and black silicone wire (~1–2 m total)
- Electrical tape, heat-shrink tubing

**Assembly:**

1. **Ring terminals for breaker studs:**
   - Strip ~5 mm of insulation from each 12 AWG lead
   - Crimp ring terminal onto stripped wire (or solder inside barrel after crimping for extra strength)
   - Verify hole diameter matches M6 studs (should be 6.2–6.5 mm)

2. **Connect to breaker (+ line only):**
   - Red wire from BMS P+ (via the power key): crimp and bolt to one M6 stud with stainless nut (torque: hand-tight + 1/8 turn)
   - Red wire to the distribution point: crimp and bolt to the other M6 stud the same way
   - The breaker is in the **+ line only**. No black (−) wire goes to the breaker; the return runs straight to BMS P−
   - **CRITICAL:** do NOT solder directly to breaker studs; thermal stress damages internal contacts

3. **Main harness cable:**
   - From the breaker's output stud, run **12 AWG red** to the distribution point, and **12 AWG black** from BMS P− (inside the stick)
   - Keep pairs twisted to minimize noise induction
   - Total length: ~1 m (adjust for pack layout)

### 3.2 XT30U gun-channel splits (16 AWG)

**Setup:** Two independent channels (guns can be powered separately or together)

1. **Pack side, each channel (gun port 1 and gun port 2):**
   - **+:** a 16 AWG red lead from the ACS758's output stud (the + split after the breaker), through the bulkhead grommet, across the cup, to the **+ socket of the pack-side XT30U female** potted in that channel's well
   - **−:** a 16 AWG black lead from the BMS P− bus, along the same route, to the − socket of the same female
   - The two pairs cross the bulkhead in the grommet's four 16 AWG holes; heat-shrink every joint and fit the well's zip-tie keeper before the hot glue (see the print guide, Inputs and outputs)

2. **Umbilical (one per gun, ~1.2 m):**
   - Pack end: an XT30U **male** on the 16 AWG pair, plugged into the well
   - Gun end: an XT30U **female** (power always comes from a female), in the gun-end brick
   - The hose and paracord run with the pair; the cord is the shortest, so it takes any pull

3. **Gun side:** an XT30U **male** on the gun's motor input (both heads of a dual-head gun in parallel)

4. **Strain relief:**
   - Braided PET sleeving over all soldered joints
   - Heat-shrink tubing over each XT30U connector neck
   - No sharp kinks in the hose or cable bundles

5. **Voltmeter:** wire its + lead to the main positive **after the breaker** (− to BMS P−), so the meter goes off with the bucks, PCB and guns whenever the breaker trips or the key is pulled. Pulling the power key on the cap top is the OFF switch (all loads off; for storage, key out and key blank in)

### 3.3 ACS758 external mounting

**Current sensor module placement (sled, front of the cross panel):**

1. Drop the ACS758 module into its compartment on the front of the sled's cross panel, above Buck A, and hold it with a zip tie (not on PCB; mounting holes not used; high-current terminals kept clear)
2. **High-current path:**
   - Breaker positive → ACS758 positive terminal (screw or connector)
   - ACS758 negative terminal → split to XT30U Channel 1 and Channel 2 males
   - Ensure connections are rated for 30+ A (proper wire gauges, terminals, not PCB traces)

3. **Signal connection to PCB (J2):**
   - 3-wire JST-XH or twisted pair: 5V, GND, signal (ACS_OUT)
   - Route away from pump current paths to minimize noise coupling

---

## 4. Power Supply Regulation (Buck Converters)

### 4.1 Pump regulation (5V for motor)

**YxPC USB buck converter (Buck A):**

1. **Input:** 2S battery voltage (unregulated, ~6.0–8.4 V)
2. **Output:** **Dial to exactly 5.0 V** before connecting pump
   - Use multimeter on 5.00 V setting to verify
   - This is CRITICAL; pump rated 4–6 V, and 8.4 V unregulated will overstress it

3. **Load:** GROTHEN G528 pump at 5V draws ~250–300 mA
   - Verify buck can supply 1+ A continuous

4. **Connections:**
   - Buck input: battery 2S pack (via breaker)
   - Buck output: **solder directly** to the lead for PCB J1 ; the PCB drives the pump through J3
   - Bench test under load before installing: output must stay **below 5.25 V**

### 4.2 LED backpack regulation (5V for display, Buck B)

**YxPC USB buck converter (Buck B):**

1. **Input:** 2S battery voltage
2. **Output:** **Dial to exactly 5.0 V**
3. **Load:** LED backpack USB input (variable, ~100–500 mA depending on display mode)
4. **Connection:** no wiring on the output side. Buck B lies on its ledge with its own USB-A port 1.3 mm behind the LED 5V window in the tube's outer wall; plug the backpack's USB cable straight into it from outside (unplug it before lifting the sled). Buck B sits 0.5 mm from the wall (put a 1.0 mm TPU shim at its input end, against the ACS758 rail); the plug must cross a 0.8 mm web and a 0.5 mm gap, so it needs at least about 10.3 mm of exposed shell (standard plugs have about 12 mm), and the backpack cable's overmold must fit the 17 × 9 mm counterbore. **Measure Buck B before printing the tube**: the window assumes 25.4 × 17 × 8 mm with the receptacle centred on the 17 mm side

---

## 5. PCB Assembly and Bring-Up (Days 3–7)

### 5.1 Through-hole component installation (on v1.2 SMT-pre-assembled boards)

**User-installed components (PCBWay shipped SMT side complete; THT user responsibility):**

| Ref | Component | Value | Package | Notes |
|---|---|---|---|---|
| J1 | JST-XH connector | 2-pin (JST B2B-XH-A) | THT | Power input (5V, GND); verify polarity mark |
| J2 | JST-XH connector | 3-pin (JST B3B-XH-A) | THT | ACS758 input (GND, Vcc, signal); verify polarity |
| J3 | JST-XH connector | 2-pin (JST B2B-XH-A) | THT | Pump output (PUMP+, PUMP_SW_NEG); verify polarity |
| J4 | AUTO/FORCE-ON input | 2-pin, 2.50 mm | DNP | Leave empty unless a head can't be detected; see [connectors](07-pcb/connectors-and-pinout.md) |
| RV1 | 3296W-1-202LF | 2 kΩ 25-turn | THT | Gun-detection threshold trimmer; Bourns 3296W lead order 1–3–2 |
| RV2 | 3296W-1-104LF | 100 kΩ 25-turn | THT | Pump-delay trimmer; Bourns 3296W lead order 1–3–2 |
| SW1 | Omron B3F-1000 | Momentary | THT | PRIME button (6×6 mm tactile switch) |
| LED1 | 3–5 mm green (Kingbright L-934GD) | LED | THT | POWER indicator (always on when J1 powered) |
| LED2 | 3–5 mm yellow (Kingbright L-934YD) | LED | THT | GUN indicator (on when current detected) |
| LED3 | 3–5 mm red (Kingbright L-934ID) | LED | THT | PUMP indicator (on when pump active) |
| C1 | Rubycon 16ZLH100MEFC5X11 | 100 µF 16 V | THT | Input bypass on J1; user-installed |
| R22 | — | — | THT | Do NOT populate (future use) |

**Installation order:**

1. **Connectors (J1–J3):** Solder JST-XH 2-pin (B2B-XH-A) and 3-pin (B3B-XH-A) headers; confirm polarity marks face outward
2. **Trimmers (RV1, RV2):** Solder 25-turn 3296W potentiometers; leads are 1–3–2 (NOT 1–2–3). **Pin 1 goes on the square pad.** The cap's adjustment windows sit over each trimmer's screw at the pin-1 end; if one goes in reversed, its screw ends up under the PRIME boot
3. **LEDs:** Install with cathodes toward GND; verify colors (red, green, yellow)
4. **PRIME switch (SW1):** Solder tactile switch; confirm closure resistance <10 Ω
5. **Capacitor C1:** 100 µF 16 V electrolytic on J1 input bypass (positive lead to square pad, + mark)
6. **Verify no missing or backward components before power-up**

### 5.2 Power-up and logic-only bring-up

**Setup:** 5V bench supply at 100 mA limit, no J2 or J3 connected yet

1. **Inspect before power:**
   - Check J1 pin 1 to GND for shorts (should read >1 MΩ)
   - Verify J3 pin 2 NOT shorted to GND unpowered
   - Confirm no solder bridges between pads

2. **Apply 5V, measure acceptance criteria (from ../07-pcb/bringup-and-acceptance-test.md § 2. Logic-only bring-up):**

| Test Point | Expected | Measurement |
|---|---|---|
| TP1 +5V_PUMP | 4.95–5.05 V | ___ |
| TP2 +5V_LOGIC | Within 50 mV of TP1 | ___ |
| TP8 VMID | 2.40–2.60 V (after settling ~1 s) | ___ |
| TP10 VDELAY | 0.98–1.06 V | ___ |
| TP9 HOLD idle | <0.10 V | ___ |
| TP14 TIMER_N idle | >4.5 V | ___ |
| TP11 PUMP_GATE idle | <0.05 V | ___ |
| LED1 (POWER) | ON | ___ |
| LED2 (GUN) | OFF | ___ |
| LED3 (PUMP) | OFF | ___ |

3. **STOP immediately if TP11 PUMP_GATE is HIGH at idle** (indicates Q2/gate-drive failure)

4. **Current consumption:** Record steady-state current at J1; should be <20 mA with no sensor/pump connected

### 5.3 Controlled startup and brownout gate

**Use oscilloscope to monitor TP2, U2 RESET_N, TP9, TP14, TP11:**

1. **Hard connect/disconnect 5V** ten times, observe:
   - TP11 PUMP_GATE remains <0.65 V during brownout
   - After RESET_N asserts, TP11 falls below 0.20 V within 15 ms

2. **Ramp supply voltage** 0→5V and 5→0V at rates: 0.1, 1, 10, 100 V/s
   - No pump-gate pulses above 0.65 V during invalid supply

3. **Supply dips** through 4.2–4.6 V range with 1 ms, 10 ms, 100 ms, and 1 s dwell times:
   - Pump gate must release within 15 ms of RESET_N assertion

4. **Record worst-case waveform** for field reference

### 5.4 Simulated sensor calibration

**Use function generator or 0–5V source with 1 kΩ series resistor on J2 pin 3 (ACS_OUT):**

1. **Verify RV1 threshold range:**
   - Measure TP6 (RV1 wiper) voltage; should span ~2.20–2.80 V as RV1 is rotated
   - Clockwise = higher threshold; counter-clockwise = lower threshold

2. **Detection assertion:**
   - Slowly increase J2 pin 3 voltage from 0 to 3.5 V (simulating gun current)
   - Record TP5 (filtered) and TP6 (threshold) voltages when DET_N asserts (GUN LED on)
   - Hysteresis should be only a few millivolts

3. **Detection release:**
   - Slowly decrease J2 pin 3; record release point
   - Expect minimal hysteresis (~4 mV nominal)

4. **Fast step response:**
   - Step J2 pin 3 from 0 to 20 mV above threshold
   - Confirm DET_N assertion and Q2 gate (TP11) rise within 25 ms
   - GUN LED should light instantly

5. **Pump delay tuning:**
   - With J2 held at ~3V (simulated gun active), set RV2 and release J2
   - Measure time from J2 release until TP11 (PUMP_GATE) falls below 0.20 V
   - Record RV2 dial position for **target 350 ms delay**
   - Verify clockwise increases delay; range should span 35–575 ms

6. **PRIME button:**
   - Press SW1; confirm GUN LED and TP11 (PUMP_GATE) go high immediately
   - Release SW1; confirm timed shutdown per RV2 setting

7. **Sensor disconnect:**
   - Unplug J2 (simulate unplugged ACS758 module)
   - Pump must release after max delay; R18 pull-down ensures safe OFF state

### 5.5 Dummy-load output test (simulated pump)

**Use 5V, 100–300 mA resistive load (e.g., 20–50 Ω power resistor) at J3:**

1. **Verify J3 polarity** before connection (red/positive pin orientation)
2. **Trigger pump control:**
   - Use PRIME switch or simulated ACS input on J2
   - Confirm TP12 (PUMP_SW_NEG) falls close to GND when pump is "on"
   - Confirm TP11 (PUMP_GATE) remains near logic rail (~3.5 V) when on
3. **Verify signal integrity:**
   - No material noise on TP2 (power rail), TP5 (sensor), TP6 (threshold) as pump load switches
   - Indicates proper filtering and ground distribution

---

## 6. Fluid System Assembly (Days 5–8)

### 6.1 Prepare 1L water bladder

1. **Inspect bladder** for leaks (fill with water, squeeze gently, check for weeps around seams)
2. **Measure outlet hose ID/OD:**
   - Typical: 6 mm ID × 8 mm OD or 4 mm ID × 6 mm OD
   - Determine reducer size needed (e.g., 6→4 mm reducer if hose is larger than 3.5 mm ID)

3. **Install reducer:**
   - From automotive hose assortment, select appropriate barbed union (e.g., 1/4" or 3/8" to 1/8")
   - Warm 3.5 × 5.5 mm silicone tube in hot water (~60°C) to soften
   - Push tubing over reducer barb until fully seated (~10 mm deep)
   - Secure with narrow 2.5 mm zip tie; do NOT overtighten

4. **Hydration bladder setup inside pack:**
   - Stand the bladder beside the stick in the LED backpack
   - Cut factory hose short; it enters the stick's wet cup through the IN hose pigtail on the front wall (45 degrees down); join the two with a reducer from the assortment
   - Factory hose feeds to reducer → 3.5 mm silicone tube → pump inlet tee

### 6.2 Assemble pump manifold

**Components:**
- GROTHEN G528 pump (6V at ~5V regulated supply)
- 1L bladder (pre-configured above)
- 3.5 × 5.5 mm silicone tubing, 5 m spool
- 4 mm plastic check valve (opening pressure 0.003 MPa)
- Automotive hose-fitting assortment: **three tees** (inlet tee, outlet tee 1, outlet tee 2), unions, reducers
- Printed slide clamps ×3 (bypass restrictor + both channel shutoffs)
- The stick's wet cup (no inlet filter; the system has none)

**Plumbing path (functional diagram):**

```
Bladder (1 L)
    ↓
Factory hose (cut short)
    ↓
Reducer (e.g., 6→4 mm barb)
    ↓
3.5 × 5.5 mm silicone inlet line
    ↓
INLET TEE
    ├─ Pump inlet
    │   GROTHEN G528
    │   (6V, 250–300 mA at 5V)
    ├─ Bypass return (from bypass slide clamp via check valve)
    │
Pump outlet
    ↓
OUTLET TEE 1
    ├─ Side branch → BYPASS SLIDE CLAMP → Check valve (arrow toward inlet) → Inlet tee
    ↓
OUTLET TEE 2
    ├─ Left gun channel → LEFT SLIDE CLAMP (shutoff) → 4-foot hose → Gun 1 inlet
    └─ Right gun channel → RIGHT SLIDE CLAMP (shutoff) → 4-foot hose → Gun 2 inlet
```

**Assembly steps:**

1. **Strap the pump into the cup:** it sits in the 52 × 46 mm pocket on the left of the cup floor, held with zip ties through the slots either side. Drains are under it. The tees, check valve and bypass slide clamp strap to the six floor slots on the right-hand strip (the 70 mm clamp runs front to back)

2. **Pump inlet tubing:**
   - Cut 3.5 mm silicone hose to ~1 m from bladder reducer to pump inlet
   - Barb at inlet tee (1/8" or 5/32" diameter from assortment)
   - Secure inlet with 2.5 mm zip tie (do NOT overtighten into soft silicone)

3. **Pump outlet tees:**
   - Install 1/8" or 5/32" outlet tee 1 at the pump outlet, then outlet tee 2 after it
   - Tee 1's side branch is the bypass return; tee 2 splits to the left and right gun channels (the outlet side has four connections)

4. **Gun outlet channels (2× four-foot hoses):**
   - Left channel: outlet tee 2 → left slide clamp → 4-foot 3.5 mm hose → left gun barb
   - Right channel: outlet tee 2 → right slide clamp → 4-foot 3.5 mm hose → right gun barb
   - Each hose leaves through the hose pigtail of its gun port on the cup's outer wall (60-80 mm of tube, 5.4 mm hole, zip-tied inside against its boss); join the umbilical hose to it with a straight barbed connector; outer hose sheathed in braided PET sleeving for durability

5. **Bypass/recirculation loop:**
   - Outlet tee 1 side branch → bypass slide clamp → 4 mm check valve → pump inlet tee
   - Allows pump to "unload" when guns are closed, reducing cavitation and noise
   - Restrictor tuned to ~5–10 mL/min bypass flow during normal operation (calibrate by observation)

6. **Check valve orientation (CRITICAL):**
   - Arrow on valve body must point toward pump inlet (reservoir return side)
   - Prevents siphoning from guns back into reservoir when pump stops

7. **Pressure test (bench, no guns):**
   - Fill bladder with water (not solution yet, to avoid mess)
   - Prime pump via PRIME button for 5 seconds
   - Verify no leaks at barbs, tees, or unions (all hoses secured with narrow zip ties)
   - Apply gentle air pressure to outlet hose (slide clamp open); check valve should barely crack open

8. **Close the cup:** bolt it on from below with 4× M3×12 screws through the corner columns into the 4 nuts in the bulkhead's hex pockets (fitted from the dry side before the sled went in; you need a long, narrow screwdriver)

---

## 7. Donor Gun Teardown and Rewiring (Days 6–8)

### 7.1 Identify and prepare donor guns

**the target festival plan:** a pair of dual-head guns (2 guns × 2 donor blower heads). Joey is picking up ~20 bubble guns this week: strip them, pick **4 matched heads**, and keep the spares. Record the teardown measurements; the gun/head mounts aren't designed yet and need them. Rough estimate (unmeasured): ~12 A with all 4 heads firing (~6 A per channel), about 2–2.5 h of heavy firing, about 2 h per 1 L.

**Earlier design note:** Four-AA 10-hole rocket-style gun
- Compact mechanical head
- 10 apertures, high bubble count
- 4.5V nominal (AA batteries × 4), or 6V variant if available
- Overvoltage tolerance: 40% at 8.4V (6V nominal)

**Verification steps:**

1. **Open donor gun carefully** (pry apart plastic halves without breaking clips)
2. **Identify motor inlet tubing:**
   - Trace pump inlet to locate tubing ID (typically 3–4 mm ID)
   - If <3.5 mm, a 4→3 mm reducer may be needed from assortment
   - Measure actual ID with digital caliper

3. **Disconnect factory motor wiring** (typically two solder tabs or push connectors)
   - Do NOT damage the internal brushes or commutator
   - Take a photo for reference during reassembly

4. **Check check valve inside gun** (if present):
   - Some guns have internal one-way valves on pump inlet; confirm direction (arrow toward motor chamber)
   - If present, do NOT replace; leave in place

### 7.2 Umbilical harness assembly

**One umbilical per gun (two total for dual-channel system):**

**Components per umbilical:**
- 16 AWG red and black silicone wire, 4–5 meters (accounts for 4-foot gun hose bundling)
- XT30U male connector (pack end) and XT30U female connector (gun end; power always comes from a female)
- 3.5 mm silicone tubing, 4 feet (fluid inlet)
- Two printed umbilical bricks (one at the gun end of each umbilical)
- 550 paracord 4 mm, ~2 meters (load-bearing tether)
- Heat-shrink and braided PET sleeving

**Harness construction:**

1. **Electrical leads (16 AWG):**
   - Bundle red and black wires together (twist lightly)
   - Length: 4–5 m to account for gun hose routing and pack entry
   - Soldered to the XT30U pins at each end (male at the pack end, female at the gun end; + red, − black)
   - Insulate solder joints with heat-shrink

2. **Fluid line (3.5 mm tubing):**
   - 4-foot length from the cup's hose pigtail to the gun-side inlet barb
   - Bundle alongside power leads with zip ties at ~1 m intervals
   - Do NOT kink or bind tightly (allows liquid flow)

3. **Load-bearing paracord:**
   - 2 m length, 4 mm 550 paracord in black
   - Bundles power and fluid together as primary support member
   - Ties to the gun-end brick at one end and through the U-tunnel boss on the cup at the other
   - Carries mechanical load; electrical leads and fluid line are passengers

4. **Umbilical bricks (printed, gun end only):**
   - Drop the XT30U into the open-top pocket and strap it with a zip tie through the slots beside the pocket
   - Run the 16 AWG pair and the fluid tube in their grooves, held by narrow zip ties
   - Tie the paracord through the outer hole; the inner hole ties to the gun. The other end of the cord goes through the U-tunnel boss at the cup's port (port 1 for umbilical 1, port 2 for umbilical 2): in one opening, out the other, knot, melt the ends
   - Leave the hose and wires a little longer than the cord, so a dropped gun loads the cord, never the hose or the solder joints
   - No screws; the bricks are the strain relief (there are no separate TPU boots)

### 7.3 Gun motor rewiring

1. **Solder 16 AWG leads** from the gun's XT30U **male** input connector (it mates with the umbilical's gun-end female):
   - Red wire to motor positive terminal (usually marked or color-coded)
   - Black wire to motor negative terminal
   - On a dual-head gun, wire both head motors **in parallel** on the gun's XT30U
   - Use electrical tape or heat-shrink to insulate solder joints

2. **Pump tubing connection:**
   - Warm 3.5 mm tubing in hot water
   - On a dual-head gun, split the umbilical's tube with **one assortment tee** to feed both donor pumps
   - Push over motor inlet barb until fully seated
   - Secure with 2.5 mm zip tie (or barb clip if included)

3. **Reassemble gun body:**
   - Reinsert rewired motor assembly
   - Check that tubing inlet is accessible and not pinched
   - Close plastic halves; verify trigger mechanism moves freely

4. **Test (bench, no solution):**
   - Connect umbilical to 5–6V bench supply
   - Trigger gun; motor should spin smoothly
   - Disconnect immediately if motor stalls (indicates blocked inlet or incorrect wiring)

---

## 8. LED Backpack Integration (Days 7–9)

### 8.1 Measure LED backpack interior

**Goal:** Confirm the stick and the bladder fit side by side inside the M-Style LED pixel backpack

1. **Empty the backpack** (remove factory bladder and internal pads)
2. **Measure internal dimensions.** Nobody has measured them yet. The "~34 × 20 × 7 cm" figure that has circulated is an AI estimate of the bag's **exterior** from photos, not an internal measurement

3. **Mock up with cardboard:** Cut cardboard templates for:
   - The stick: about 99.6 × 77.8 × 220 mm, standing upright
   - Fluid reservoir: 1 L + ~20% bladder material volume

4. **Fit test:** Place templates inside backpack; confirm no binding or excessive gaps

### 8.2 Internal organization (electronics into the sled)

Everything except the bladder goes into the stick. Full part notes are in [hardware/printed/README.md](../hardware/printed/README.md).

1. **Sled (slides out of the top of the tube):**
   - Battery: stands left of the spine on the base, cell axes front to back, **TERM face (pack + and −) toward the back**
   - Breaker: stands upright right of the spine, behind the cross panel, 2 mm from the outer wall. Run one zip tie through each plate hole and the tall slot in the spine behind it. Leave about 1.5 mm under the bottom stud for its lug. The gap between the spine and the breaker is a wire channel. The tube walls are solid, so the reset lever is only reachable with the sled out: leave enough wiring slack to lift the sled out
   - BMS: stands on edge in the slot along the back wall; the TERM-face leads reach it through the channel behind the spine. Two small posts on the base (x = 12–17 and 31–36) stop the battery sliding into the leads: route the leads clear of them; the TERM-bus leads must run above z = 10.5 mm, since the posts fill the bottom 8 mm of the lead channel
   - Buck A, Buck B, ACS758: drop into the three compartments on the front of the panel and get a zip tie each. Wires to the breaker/BMS side go through the 8 × 30 mm pass at the panel's right end

2. **Cap (control head):**
   - PCB: hangs under the cap, component side up. Push it onto the four pins and heat-stake the tips (heads under 5 mm, because J2 sits 2.7 mm from H3)
   - PRIME: TPU plunger in its sleeve, head up. Put a thin ring of silicone around the bore, lay the boot's D-shaped flange on it (flat side toward the LEDs), then glue the ASA bezel down over the flange (acetone slurry, or CA)
   - LEDs: once the PCB is staked, fill each 3.6 mm LED hole from the top with clear hot glue or UV resin
   - Voltmeter: body through the 29 mm hole, glued around its bezel
   - USB-C charger: presses by hand, with firm pressure, up into its pocket under the CHG window (four crush ribs grip it), receptacle against the window, plus a dab of glue; its output runs to BMS P+/P− through an XT30 pair so the cap stays removable
   - J1, J2, J3 are XH plugs; leave enough slack to lift the cap and set it beside the stick

3. **Bulkhead and cup:**
   - **Pack end of each umbilical:** an XT30U male on the 16 AWG pair, the hose end and a paracord loop. No brick. Close an unplugged port well with a TPU port cap (part 42) and its fluid side with the slide clamp inside the cup (the cap only covers the electrical well)
   - **Before the sled goes in:** drop the 4 M3 nuts into the hex pockets in the bulkhead floor from the dry side and lock each with a dab of CA or silicone. The M3×12 cup screws (each with an M3 split lock washer under the head) then go up from below through the cup columns and thread fully through these nuts
   - Cut a slit with a knife from each grommet hole to the nearest long edge and lay the cables in: both 16 AWG gun pairs and both pump leads (the XT60H loop and the backpack USB no longer cross the bulkhead). Hold the ASA drip skirt's lip against the bulkhead's underside, push the lower half up through it from the cup side, and the upper half down from the dry side
   - Once the wiring is final, fill the grommet's whole top face with neutral-cure silicone, worked around each cable (it peels off when you need to pull the sled)
   - Gun ports (cup outer wall): fit each pack-side XT30U **female** with a spare male plugged in as a jig. Push the pair in from inside until the male's rim is flush with the outer face, then fill the well behind the female with hot glue (it pots the solder cups too). Fit a rear zip-tie keeper across the sleeve between the female's solder cups, pushed against the back of its body (cup off the stick); it carries the 12-34 N unplugging force, so the glue only seals and centres. Proof-test each port by pulling the plugged umbilical at about 70 N with the paracord slack. Add a short heat-shrink boot over the umbilical's male and wires if you expect rain (the mated pair is recessed under a drip hood, not waterproof). Push the 60-80 mm hose pigtail out through its 5.4 mm hole and zip-tie it inside against its boss. Tie each umbilical's paracord through the U-tunnel beside its port (cord in one opening, out the other, knot, melt the ends); keep the cord shorter than the hose and wires; thread the cord through the tunnel with a leader (a stiff wire or a zip tie taped to the cord's tip) and test the tunnel with a hard pull on the cup
   - Jostle-proofing: hot glue on the J1–J3 XH plugs after a final test, tape or a zip tie around each mated XT30/XT60, a zip tie within 2–3 cm of every solder joint, the TPU pump mat under the pump (strapped down with zip ties across the pocket), and a slack loop on each hose in the cup
   - Give every cable a drip loop below the cup, so water runs off the low point rather than up the cable
   - Nothing exits underneath: the umbilicals use the two gun ports, the bladder uses the IN pigtail on the front wall, and the LED backpack plugs into the USB-A window in the tube wall
   - The two gun XT30U wells and the IN pigtail are on the wet side; close unplugged wells with the TPU port caps

4. **Close the stick:**
   - Click a TPU battery pad onto the end of each of the cap's two ribs (its bead snaps into the rib's groove; a dab of hot glue is only a backup). If the cap closes with the pads loose, put a 0.6 mm shim strip under a pad; the ribs press the cell holders and pin the sled onto the bulkhead. Tuck TPU shim strips into any pocket where a board rattles (0.6 and 1.0 mm for the BMS slot and buck/ACS758 pockets), against a component-free board edge, and keep the zip tie
   - Stretch the TPU ring into the cap skirt's groove. Fit the cap, then 2× M3×10 screws through the front and back walls, **each with a TPU washer under the head**, into the M3 nuts glued into the slots behind the cap's skirt. Snug is enough; ASA cracks if over-torqued. Use the M3 flat washer on top of the TPU washer. Press the cap down while tightening so the screw holes' slack doesn't eat the pad preload
   - To get the cap off, lever it up with a flat screwdriver in the notch on the left edge

5. **In the bag:**
   - Stand the stick upright beside the bladder, its back (y = 0) against your back
   - No pressure on fluid bladder or PCB
   - Total loaded weight ~3.1–3.5 kg (within performance envelope for festival wear)

### 8.3 Electrical integration inside backpack

1. **5V power distribution:**
   - **Buck A** (YxPC, set to 5.0V): input from 2S battery (through breaker), output supplies PCB J1, ACS758 module power, and pump motor control via Q2 on the PCB
   - **Buck B** (YxPC, set to 5.0V): input from 2S battery, output to its own USB-A port behind the LED 5V window (the backpack cable plugs in there)

2. **Connector routing:**
   - J1 (PCB power): JST-XH cable soldered directly to Buck A's output
   - J2 (ACS758 sensor): 3-wire JST-XH from external ACS758 module (receives 5V and GND from PCB J1)
   - J3 (pump output): cable down through the bulkhead grommet to the pump motor (2-pin JST-XH, controlled by PCB MOSFET Q2)
   - LED backpack USB: plugs into Buck B's own USB-A port through the tube wall (no cut cable)

3. **Test before final packing:**
   - Apply 5V to system; verify all test points nominal per PCB bring-up section
   - Confirm no shorts when fully integrated
   - RV1 and RV2 (3296W, 25-turn) adjust through the cap's two small windows with a small screwdriver, with the TPU trimmer plug (part 39) pulled; push the plug back in afterwards. The plugs go in last: the trimmer plug when RV1/RV2 are set, and the USB-C plug (part 40) after charging
   - **Charge with the cap off** until the first enclosed charge has been checked (see [test plan](13-test-plan.md))

---

## 9. First Integrated Firing Test (Days 10–11)

### 9.1 Pre-fire checklist

- [ ] Battery charged to 8.4 V (use USB-C charger for ~8 hours from empty)
- [ ] BMS balancing complete (voltage <0.1 V spread across cells)
- [ ] All solder joints cold and solid (no joint movement with probe)
- [ ] Pump inlet and outlet NOT kinked or occluded
- [ ] XT30U connectors fully seated and latched
- [ ] Breaker armed (reset lever ON, checked with the sled out before closing the stick); the power key on the cap top is the OFF switch
- [ ] PRIME works with a deliberate fingertip press inside the bezel, and a flat palm or a strap across the cap doesn't trigger it
- [ ] Donor guns verified for motor movement and tubing inlet patency
- [ ] Fluid solution mixed (1 part JOYFY concentrate + 9 parts water in 1L container)

### 9.2 Prime pump (bench, no guns)

1. **Fill 1L bladder** with mixed solution (10 mL concentrate + 90 mL water for test)
2. **Insert the power key** (the battery is connected through the KEY socket)
   - Voltmeter reading should jump to ~8.4 V (battery full)
   - LEDs should light (POWER on, others off if no sensor/pump connected)

3. **Connect J2 (ACS758 sensor)** to PCB
   - POWER LED should remain on
   - GUN and PUMP LEDs off (no current detected)

4. **Connect J1 (5V supply)** to PCB
   - All three LEDs on briefly during startup, then POWER remains on

5. **Connect pump to J3:**
   - PRIME switch activation → PUMP LED on
   - Pump motor audible; fluid flows from pump outlet into tee
   - Hold PRIME for 10 seconds (primes all lines with solution)
   - Release PRIME → PUMP LED off after ~350 ms delay

6. **Verify output:**
   - Fluid should flow from pump outlet tee into left and right gun channels
   - No leaks at barbs, tees, or unions (all connections secured with narrow zip ties)

### 9.3 Gun firing (first test, single gun)

1. **Connect Left Gun** (Umbilical 1): plug its pack-end male into the port 1 well female, and its gun-end female onto the gun's male input:
   - Confirm snug fit and latch clicks
   - Motor should spin freely (dry run, no solution in tubing yet)

2. **Trigger gun with PRIME:**
   - PUMP LED lights; solution flows into gun inlet
   - Release gun; pump stops after ~350 ms delay (solution in gun nozzle)
   - Repeat 3–4 times to verify consistent behavior

3. **Connect Right Gun** (Umbilical 2) to Right Channel:
   - Repeat PRIME trigger test
   - Verify pump activation works independently per gun

4. **Dual-gun firing:**
   - Connect both XT30U umbilicals to pack channels
   - Trigger Left gun → GUN LED on, PUMP LED on, solution flows left
   - Trigger Right gun (while Left held) → solution flows right; pump remains on (supplying both)
   - Release both guns → PUMP stays on for 350 ms delay, then off
   - Repeat 5–10 times; verify no chatter or false starts on either gun

5. **ACS758 threshold tuning** (if gun current varies):
   - Measure combined gun current at 5V (multimeter in series on gun return)
   - Adjust RV1 (gun detection threshold) so trigger is reliable but no false positives during idle
   - Typical threshold: ~0.5 A (adjust per actual gun current)

---

## 10. Leak Test (Days 11–12)

### 10.1 Pressurized soap bubble test

1. **Fill bladder** with 1L of water + soap (1 mL dish soap per liter for visibility)
2. **Apply gentle air pressure** to pump outlet line via hand pump or low-pressure air compressor (~0.5 psi):
   - Observe all joints, barbs, tees, and check valve
   - Listen for hissing; watch for bubbles
   - Verify zip ties are not cutting into the silicone hose
3. **Mark any leaks** with tape; note location and severity
4. **Common leak points:**
   - Zip ties overtightened (cutting into soft silicone): loosen and reposition, or replace hose section
   - Check valve cracking too easily: reduce air pressure or confirm arrow orientation
   - Barb mismatch: replace with correct size or add reducer

### 10.2 Dynamic leak test (during pump operation)

1. **Prime pump for 30 seconds** with guns closed (channel slide clamps fully shut)
   - Observe bypass slide clamp and check valve (should hear quiet gurgle if flow is ~5–10 mL/min)
   - Watch for weeps at all connections; confirm the slide clamps hold their settings

2. **Open one channel slide clamp** and trigger PRIME for 10 seconds:
   - Solution flows to that gun; no leaks at barb connections (zip ties tight but not crushing silicone)

3. **Repeat with both guns open**:
   - Pump supplies both channels simultaneously
   - No dripping or weeping anywhere

### 10.3 Stick wet checks (not yet verified)

1. **Cap seal:** the TPU ring is a starting geometry, not a proven seal. Wet-test the closed stick before trusting it ([test plan](13-test-plan.md))
2. **Cup drain:** pour a little water into the cup and confirm it drains through the floor
3. **Grommet:** splash only; it isn't watertight, so keep fluid joints below it

---

## 11. Shake and Dance Test (Days 12–13)

**Goal:** Verify mechanical security and connector integrity during movement

1. **Physical shake test (30 seconds):**
   - Hold backpack at chest level and shake vigorously (simulating dance)
   - No loose components rattling
   - No zip ties slipping or coming loose
   - No connector wiggle or disconnection

2. **Dance simulation:**
   - Wear backpack and move for 2–3 minutes (jumping, turning, arm swinging)
   - Monitor for vibration/noise from internal components
   - No rattle from the sled inside the tube (the cap's TPU-padded ribs should pin it)
   - No cable strain at the umbilical bricks
   - Tug each gun hard: the paracord goes taut while the hose and wires stay slack

3. **Hose head-height test (if applicable):**
   - Raise gun intake barb 5 feet above reservoir surface
   - Prime pump; solution should flow upward without cavitation
   - If flow stops, check for air locks in hose or inadequate pump pressure

---

## 12. One-Liter Endurance Test (Day 13)

**Goal:** Measure actual battery runtime and power consumption

1. **Charge battery to 8.4 V** via USB-C charger
2. **Fill 1L bladder** with mixed bubble solution
3. **Connect guns and start firing continuously:**
   - Both gun channels open (slide clamps fully open)
   - Continuous trigger (PRIME held or gun triggers held)
   - Measure time until solution depleted (bladder empty, no more bubbles)

4. **Record:**
   - Start time and start battery voltage (should be ~8.4 V)
   - End time and end battery voltage (should be ~6.0 V, BMS cutoff threshold)
   - Total runtime in minutes
   - Solution consumption (should be approximately 100 mL/min for dual-gun operation, yielding ~10 minute runtime for 1L)

5. **Thermal monitoring:**
   - Check battery temperature after endurance test
   - Should be warm but NOT hot to touch (aim <50°C)
   - Check PCB temperature at U1 and Q2 (should be <60°C)
   - Pump and motor temperature rise acceptable if <20°C above ambient

---

## 13. Electrical System Verification (Day 14)

### 13.1 Battery voltage and protection

- [ ] Open-circuit voltage: 8.4 V (fully charged)
- [ ] Nominal voltage under 5A load: 7.4 V (acceptable)
- [ ] BMS cutoff threshold triggered: 6.0 V (gun current should stop flowing)
- [ ] BMS balance current: <10 mA at 8.4 V rest (low balancing demand)

### 13.2 Charger integration

- [ ] USB-C charger accepts 5V/3A input
- [ ] Battery charges from 6.0 V (depleted) to 8.4 V in <10 hours
- [ ] Voltmeter reads 8.4 V when charger is done
- [ ] No overheating of charger or battery during charging
- [ ] First enclosed charge (cap on): charger and BMS temperatures checked. Until this passes, charge with the cap off

### 13.3 Controller stability

- [ ] PCB logic remains stable over 10+ pump cycles
- [ ] RV1 and RV2 calibration stable (no drift after 100 cycles)
- [ ] LEDs bright and responsive
- [ ] No false pump starts or dropouts during operation

---

## 14. Pre-Event Checklist (Day 14–15, before 2026-10-29 deadline)

**Final systems review before festival deployment:**

- [ ] Battery charged to 8.4 V and rested >30 minutes (voltage stable)
- [ ] All connectors (XT60H, XT30U, JST-XH, J1–J3) securely latched
- [ ] Fluid solution mixed and bladder filled (1 part concentrate to 9 parts water)
- [ ] Pump primed (no air locks in tubing)
- [ ] Both guns tested for motor spin and inlet patency
- [ ] PCB calibrated (RV1 = detection threshold, RV2 = ~350 ms delay)
- [ ] Voltmeter readable on top of the stick's cap
- [ ] Cap seal wet-tested; TPU trimmer plug (39) and USB-C plug (40) fitted
- [ ] LED backpack powered and responsive (if used)
- [ ] Backpack weight balanced and comfortable (tested for 5+ minutes wear)
- [ ] Umbilical connectors accessible for quick gun swap in field
- [ ] Spare bubble solution concentrate on hand (1× 32 oz bottle supports ~10 refills)
- [ ] Power key pulled with the stick closed: the bucks, PCB, voltmeter and guns all go off (it's the OFF switch)
- [ ] Voltmeter idle current measured once with a multimeter; power key pulled whenever the pack is stored
- [ ] Conformal coating applied (optional; skip if field repair access needed)
- [ ] Documentation (this build guide, test results, calibration notes) stored digitally or on paper

---

## Final Assembly Statistics

- **Total build time:** 25–40 hours hands-on
- **Critical path:** PCB bring-up (6+ hours) + fluid system assembly (4+ hours) + donor gun integration (3+ hours)
- **Estimated completion:** 2026-10-29 (see the build order at the top)
- **Loaded weight:** 3.1–3.5 kg (with 1L fluid, festival configuration)
- **Runtime:** 8–12 minutes continuous firing (1L solution at dual-gun operation)
- **Estimated bubble output:** 500–1000 bubbles/minute per gun (subject to head design and solution quality)
