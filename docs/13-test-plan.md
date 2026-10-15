# BubbleLink System-Level Test Plan

Complete acceptance test procedures for BubbleLink bubble-gun system. This plan covers functional verification of battery, power delivery, controller, fluid system, current sensing, pump operation, mechanical reliability, and endurance. All tests are field-executable and do not require lab equipment beyond a multimeter and oscilloscope (for controller calibration). Build on foundation of [docs/07-pcb/bringup-and-acceptance-test.md](07-pcb/bringup-and-acceptance-test.md) for PCB-level tests.

## Overview

| Test Phase | Tests | Acceptance | Equipment |
|---|---|---|---|
| **Battery & Power** | Capacity, charging, voltage protection | 8.4 V charged, 6.0 V cutoff, <10 hr charge | Multimeter, USB-C supply |
| **Controller Logic** | Startup, threshold tuning, delay calibration | LEDs nominal, thresholds stable, delay 350 ms ±50 | Oscilloscope, trimmers |
| **Current Sensing** | ACS758 module characterization | Threshold reached at gun current, ~4 mV hysteresis | Multimeter, simulated load |
| **Pump Control** | Manual (PRIME) and automatic activation | Pump ON <25 ms after gun current; OFF after delay | Visual, acoustic |
| **Fluid System** | No leaks, no siphoning, bypass restrictor tuning | Dry benchtop, <0.5 psi soap bubble test, 5–10 mL/min bypass | Soap, air pump |
| **Thermal** | Battery and controller temperature under load | Suggested starting criterion (not from a source spec): <20 °C rise above ambient; stop if a cell is uncomfortable to touch | Thermometer, 10 min run |
| **Mechanical** | Shake, vibration, hose security, connector latch | No disconnects, no component wiggle, no liquid weeps | Visual, dance motion |
| **Endurance** | 1L continuous runtime, solution consumption | ≥8 min runtime, ≤6 V final voltage | Timer, empty bladder |
| **Integration** | Dual-gun operation, rapid cycling, field conditions | Both guns independent, no crosstalk, reliable at all temperatures | Both guns, repeated fire |
| **Pre-Event** | Final checklist before festival deployment | All systems green, spare parts on hand, calibration locked | Venue-equivalent temperature |

---

## 1. Battery Capacity and Runtime Test

### Test 1.1: Open-Circuit Voltage Check

**Objective:** Verify 2S5P pack delivers expected nominal voltage without load.

**Procedure:**
1. Fully charge battery via USB-C charger (8–10 hours from empty 6.0 V)
2. Allow 30 minutes rest (let internal resistance stabilize)
3. Measure voltage at XT60H battery connector with multimeter set to DC voltage (highest range)
4. Record: **Expected 8.40 ± 0.10 V** (fully charged 2S nominal, 4.2 V per cell)

**Acceptance criteria:**
- [ ] Voltage ≥8.30 V (indicates all cells charged)
- [ ] Voltage ≤8.50 V (normal fully-charged range)
- [ ] No significant droop over 5 minutes idle (should remain stable ±0.05 V)

**Pass/Fail:** ____

---

### Test 1.2: Battery Cutoff Voltage (BMS Protection)

**Objective:** Verify BMS cuts power at the configured protection threshold (prevents over-discharge damage). Standard Li-ion protection threshold: ~6.0 V for 2S (3.0 V per cell).

**Procedure:**
1. **Load the battery:** Connect a 5V dummy load (~1A resistive load) to XT30U gun channels via a dummy connector
2. **Monitor voltage** with multimeter in continuous mode; record time
3. **Continue until BMS cutoff:** Gun current should stop flowing when pack voltage drops to BMS protection threshold
4. **Record final voltage** and time elapsed

**Acceptance criteria:**
- [ ] Cutoff voltage measured: standard Li-ion 2S threshold (measure actual; ~5.95–6.05 V expected for 3.0 V/cell cutoff)
- [ ] No supply voltage below 5.8 V before cutoff (sharp protection, not gradual fade)
- [ ] Cutoff is clean and repeatable (test twice; both within 0.05 V of first cutoff)

**Note:** This test depletes the battery completely. Recharge immediately after for next tests.

**Pass/Fail:** ____

---

### Test 1.3: One-Liter Continuous Runtime (Dual-Gun Operation)

**Objective:** Measure actual runtime with both guns firing continuously at nominal 5V pump supply.

**Procedure:**
1. **Setup:**
   - Charge battery to 8.4 V and rest 30 minutes
   - Fill 1L bladder with mixed bubble solution (100 mL JOYFY concentrate + 900 mL water)
   - Connect both XT30U gun channels with donor guns installed
   - Open both channel slide clamps (gun outlet shutoffs fully open)

2. **Fire continuously:**
   - Activate PRIME button (or gun triggers held in) for continuous pump operation
   - Do NOT release; maintain steady flow to both guns
   - Record **start time** and **initial battery voltage** (should be 8.4 V)
   - Observe bubble production; should be steady and abundant (>100 bubbles/sec combined)

3. **Monitor during test:**
   - Record battery voltage every 2 minutes (note: voltage will decline from 8.4 V toward 6.0 V over ~10 minutes)
   - Listen for pump noise change (may become slightly quieter as voltage drops)
   - Watch solution level in bladder; record depletion rate during test
   - Note any leaks, hose kinks, or motor stalling

4. **End test:**
   - **Test ends when:** Either bladder is empty (no more solution) OR battery reaches 6.0 V (BMS cuts off)
   - Record **end time**, **final battery voltage**, and **final solution volume**
   - Time elapsed = Runtime; solution consumed = drain rate

**Acceptance criteria:**
- [ ] Runtime ≥8 minutes (measure actual consumption; 1 L at estimated 50–80 mL/min dual-gun system draw gives 12–20 min as reference)
- [ ] Final battery voltage ≥5.95 V and ≤6.05 V (BMS cutoff reached, not error discharge)
- [ ] Solution consumption rate stable; record actual rate for baseline (dual-gun demand depends on donor motor specs and voltage)
- [ ] No thermal issues: battery case warm but not hot to touch after test
- [ ] No mechanical failures: pump, hoses, connectors all functional

**Data logged:**
- Start voltage: ____ V
- End voltage: ____ V
- Runtime: ____ min
- Solution consumed: ____ mL
- Drain rate: ____ mL/min
- Observations: __________________________

**Pass/Fail:** ____

---

## 2. Charging Test

### Test 2.1: USB-C Charger Functionality and Charge Time

**Objective:** Verify charger accepts 5V input and charges 2S pack to 8.4 V within expected time window.

**Procedure:**
1. **Discharge battery** to ~6.0 V (via Test 1.2 or extended operation). **Take the stick's cap off** for this test; enclosed charging is checked separately in Test 2.2
2. **Prepare charger:**
   - Use a 5V/2A USB-C power supply (wall adapter or lab supply)
   - Connect USB-C input to charger module
   - Connect charger output to BMS P− (black) and P+ (red) (in the stick, through the cap's XT30 pair)
   - Verify polarity with multimeter before applying power (should read 0V at start)

3. **Apply 5V input:**
   - Charger should begin charging (may hum quietly or show LED indicator, depending on design)
   - Monitor pack voltage with multimeter; should climb from 6.0 V toward 8.4 V

4. **Log voltage and time:**
   - Record voltage every 30 minutes
   - Expected progression: 6.0 V → 7.4 V (60 min) → 8.0 V (90 min) → 8.4 V (120–150 min)

5. **End charge:**
   - Charging complete when voltage plateaus at 8.4 V (usually indicated by charger going quiet or LED changing state)
   - Record **total charge time**

**Acceptance criteria:**
- [ ] Charging initiates immediately (no delay >5 seconds)
- [ ] Voltage rises monotonically toward 8.4 V (no reversals or oscillations)
- [ ] Final voltage: 8.35–8.45 V (target 8.4 V, ±2% acceptable)
- [ ] Charge time: ≤10 hours from 6.0 V to 8.4 V (acceptable for overnight charging)
- [ ] No excessive heat: Charger module warm but not hot after 2 hours continuous charge

**Charge time log:**
- Time 0:00 — 6.0 V
- Time 0:30 — ___ V
- Time 1:00 — ___ V
- Time 1:30 — ___ V
- Time 2:00 — 8.4 V (complete)
- **Total charge time: ____ hours**

**Pass/Fail:** ____

---

### Test 2.2: First Enclosed Charge (Cap On)

**Objective:** Check charger and BMS temperatures when charging inside the closed stick. This hasn't been verified: the tube only breathes incidentally (grommet slits, cap ring), and at 4 A the charger alone may give off around 3–4 W. **Until this test passes, charge with the cap off.**

**Procedure:**
1. Run Test 2.1 first (cap off) and note the charger and BMS temperatures there
2. Close the stick (cap on, both cap screws in) and charge from the top USB-C port
3. Stay with it. Check the charger and BMS temperatures during the first 10 minutes and then periodically (open the cap briefly, or use a thermocouple lead or thermal camera)
4. If either gets hot, stop charging and take the cap off

**Acceptance criteria:**
- [ ] BMS stays below the 45 °C first-charge limit in [04-power-system.md](04-power-system.md)
- [ ] Charger and BMS temperatures are not much higher than in the cap-off charge of Test 2.1
- [ ] Charge completes normally (8.35–8.45 V)

**Data logged:**
- Cap-off temperatures (Test 2.1): charger ____ °C, BMS ____ °C
- Cap-on temperatures: charger ____ °C, BMS ____ °C

**Pass/Fail:** ____

---

## 3. Circuit Breaker and Main Power Path Test

### Test 3.1: Breaker Current Rating Verification

**Objective:** Confirm 30A manual-reset breaker trips at design current and resets cleanly.

**Procedure:**
1. **Setup:**
   - Open the breaker by pressing its red push-to-trip button (OFF)
   - Use adjustable lab power supply set to 8.4 V DC with 5A current limit
   - Connect positive to breaker positive terminal (via ring terminal)
   - Connect negative to a 10 Ω load resistor to ground

2. **Test breaker pickup:**
   - Slowly increase current limit until breaker trips (reset lever pops)
   - Record trip current (should be slightly above 30A, typically 32–35A due to thermal lag)
   - Breaker should trip cleanly and stop current flow within <100 ms

3. **Test breaker reset:**
   - Work the red reset lever back to ON
   - Power should return; voltage should reappear across load
   - Breaker should hold at nominal current with no chatter or oscillation

4. **Thermal test:**
   - Run at 30A (near rated) for 2 minutes
   - Check breaker housing temperature; should be warm but <60°C

**Acceptance criteria:**
- [ ] Breaker trips at 30–35A (within ±15% of 30A nominal)
- [ ] Reset is smooth with no bounce or delayed restart
- [ ] Breaker holds >10 A continuous without nuisance trips
- [ ] No excessive heat build-up

**Test results:**
- Trip current: ____ A
- Reset lever response: ____ ms
- Temperature after 2 min @ 30A: ____ °C

**Pass/Fail:** ____

---

### Test 3.2: Power Key (XT60H) and Ring Terminal Security

**Objective:** Verify battery connector and ring terminals are secure and carry full system current without heating.

**Procedure:**
1. **Visual inspection:**
   - Confirm the XT60H male socket (17.0 × 9.8 mm sleeve) is potted in the cap, with its rear zip-tie keeper in place, (shroud under its 0.8 mm lip; pin A = BMS P+, pin B = breaker input) and the key is an XT60H female with its U-loop hot-glued into the grip
   - Check that the lip stops the male being pulled up and the glue below it stops it being pushed down
   - Confirm both M6 ring terminals are fully seated on breaker studs with nuts snug (hand-tight + 1/8 turn)

2. **Electrical test:**
   - Apply 8.4 V from battery through the power key to the main harness
   - Measure voltage at breaker output (should be ≥8.35 V, <0.05 V drop)
   - Load with 15A continuous; measure again (should remain ≥8.30 V)
   - Record voltage drop: _____ mV

3. **Thermal test:**
   - Run at 15A continuous for 5 minutes
   - Check XT60H connector and ring terminal temperature
   - Should be warm but <40°C above ambient

4. **Mechanical test:**
   - Attempt to pull XT60H connector apart with moderate force; should require deliberate unlatching
   - Twist connection by 10–15°; no lateral movement of ring terminals on studs

**Acceptance criteria:**
- [ ] Voltage drop ≤0.05 V at 15A (clean connection)
- [ ] XT60H latches securely and requires intentional press to separate
- [ ] Ring terminals do NOT slip on breaker studs under 15A load
- [ ] Temperature rise ≤15°C above ambient at 15A × 5 min

**Measurements:**
- Voltage drop @ 15A: ____ mV
- XT60H latch resistance: FIRM / LOOSE / DAMAGED
- Ring terminal slip: NO / YES (if YES, tighten nuts)
- Temperature rise: ____ °C

**Pass/Fail:** ____

---

### Test 3.3: OFF via the Power Key, and Idle Draw

**Objective:** Confirm that pulling the power key on the cap top works as the OFF switch (and that the charger still works with the key out; with the key out, the voltmeter, bucks and PCB must be off), and measure the voltmeter's idle current (not yet measured). The breaker has no wall window; its controls are only reachable with the sled out.

**Procedure:**
1. With the stick closed, the breaker armed and the key in, confirm the voltmeter, the PCB's POWER LED and the LED backpack are on
2. Pull the power key out of the KEY socket on the cap top
3. Confirm everything downstream goes off: the voltmeter goes dark, the PCB's POWER LED goes out (Buck A off), the LED backpack goes off (Buck B off), and the guns don't fire. The battery stays connected to the BMS, the charger and one pin of the key socket (it is not a full disconnect); for storage, key out and key blank in
4. Put the key back in and confirm everything comes back
5. **Voltmeter idle current:** with a multimeter on the mA range in series with the voltmeter's + lead, read its draw. Small LED meters typically draw tens of mA

**Acceptance criteria:**
- [ ] Pulling the power key with the stick closed turns off the bucks, PCB, voltmeter and guns
- [ ] Everything comes back when the key is put back in
- [ ] Voltmeter idle current recorded

**Data logged:**
- Voltmeter idle current: ____ mA

**Pass/Fail:** ____

---

## 4. Current Sensing Threshold Test

### Test 4.1: ACS758 Module Output Characterization

**Objective:** Verify ACS758 sensor output voltage at zero and nominal gun current; confirm threshold window adequate for detection.

**Procedure:**
1. **Setup:**
   - Disconnect J2 (ACS758 input) from PCB temporarily
   - Apply 5V regulated supply to ACS758 module Vcc and GND
   - Measure sensor output voltage (signal pin) with high-impedance multimeter
   - Record **zero-current output voltage** (should be ~2.5 V for ±50 A bidirectional sensor)

2. **Load test:**
   - Connect adjustable current source to ACS758 high-current terminals (or use lab supply + load resistor)
   - Draw 1A through sensor; measure output voltage
   - Expected: 2.5 V + (1 A × 40 mV/A) = 2.54 V
   - Draw 5A through sensor; expected 2.7 V
   - Draw 10A through sensor; expected 2.9 V
   - Record all three points

3. **Sensitivity check:**
   - Calculate actual sensitivity: (V_5A − V_1A) / (5A − 1A)
   - Should be ~40 mV/A (typical for ACS758-050B)
   - If <39 mV/A or >41 mV/A, note as out-of-spec

**Acceptance criteria:**
- [ ] Zero-current output: 2.40–2.60 V (nominal 2.5 V ±4%)
- [ ] Sensitivity: 39–41 mV/A (nominal 40 mV/A)
- [ ] Signal clean: <20 mV ripple at fixed current

**Data:**
- V @ 0 A: ____ V (zero offset)
- V @ 1 A: ____ V
- V @ 5 A: ____ V
- V @ 10 A: ____ V
- Calculated sensitivity: ____ mV/A
- Signal ripple: ____ mV peak-to-peak

**Pass/Fail:** ____

---

### Test 4.2: Gun Current Detection Threshold (RV1 Calibration)

**Objective:** Tune RV1 potentiometer so pump activates reliably when either gun draws current, with adequate margin against noise.

**Procedure:**
1. **Bench setup with simulated gun:**
   - Connect J2 back to PCB
   - Use function generator or adjustable 0–5V source to simulate ACS758 output
   - Drive J2 pin 3 through 1 kΩ resistor (impedance matching)
   - Start at 2.5 V (zero current), simulating idle sensor

2. **Measure threshold and hysteresis:**
   - Slowly increase source voltage from 2.5 V → 3.0 V (simulating ~10 A gun current)
   - Watch for GUN LED to light and DET_N to go low
   - Record voltage at which detection occurs: **______ V**
   - Expected range: 2.6–2.8 V (corresponding to ~2.5–12 A gun current with 40 mV/A sensitivity)
   - Slowly decrease voltage; record release point: **______ V**
   - Hysteresis should be <10 mV

3. **Adjust RV1 for target threshold:**
   - Current gun current at 5V nominal pump supply: **measured ____ A**
   - Expected ACS758 output at this current: 2.5 V + (gun_current × 0.040) = **_____ V**
   - Adjust RV1 (clockwise = higher threshold) so detection occurs ~50 mV above zero-current output (2.55 V target)
   - This provides margin against sensor noise (typically <20 mV) and prevents false positives from boot transients

4. **Field test:**
   - Connect actual gun to XT30U channel 1
   - PRIME button → GUN LED should light immediately; pump activates within 25 ms
   - Trigger gun directly → same behavior
   - Release gun → GUN LED goes out within <100 ms; PUMP LED off after ~350 ms (RV2 delay)

**Acceptance criteria:**
- [ ] GUN LED lights when either gun is triggered
- [ ] GUN LED does NOT light during idle or when pump only (isolated sensor from pump current)
- [ ] Pump activation delay <25 ms after gun current detected
- [ ] No false positives during startup transients or BMS balancing

**RV1 Calibration log:**
- Measured gun current: ____ A
- ACS758 output at that current: ____ V
- RV1 dial position for detection: **____ turns clockwise from minimum**
- Threshold voltage (TP6 reading): ____ V
- Hysteresis: ____ mV
- Field test result: GUN LED YES / NO; Pump YES / NO

**Pass/Fail:** ____

---

## 5. Pump Control and Automatic Start/Stop Timing

### Test 5.1: Manual PRIME Button

**Objective:** Verify PRIME switch activates pump immediately and timed shutdown works.

**Procedure:**
1. **Unpressurized bench test:**
   - No guns connected, pump outlet open to air
   - Press PRIME switch; both GUN and PUMP LEDs should light immediately
   - Listen for pump motor sound (high-pitched buzz at 6V; ~300 rpm)
   - Hold PRIME for 10 seconds (pump runs continuously)

2. **Measure on time:**
   - Release PRIME switch at t=0
   - Observe PUMP LED: should remain ON for ~350 ms, then OFF
   - Measure time using oscilloscope on TP11 (PUMP_GATE) or visual LED timing
   - Record: **off-delay = ____ ms**

3. **Repeat 5 times:**
   - Confirm delay is consistent (should be within ±50 ms of 350 ms nominal due to RV2 setting)

**Acceptance criteria:**
- [ ] PRIME activates pump immediately (<5 ms)
- [ ] Pump motor audible and sustained while PRIME held
- [ ] PUMP LED delay from release: 300–400 ms (typical 350 ±50)
- [ ] Consistent timing across 5 trials (std dev <20 ms)

**PRIME test data:**
- Trial 1 delay: ____ ms
- Trial 2 delay: ____ ms
- Trial 3 delay: ____ ms
- Trial 4 delay: ____ ms
- Trial 5 delay: ____ ms
- Average: ____ ms
- Std dev: ____ ms

**Pass/Fail:** ____

---

### Test 5.2: Automatic Activation (Gun Current Detection)

**Objective:** Verify pump activates when gun is triggered and shuts down on timed schedule independent of PRIME.

**Procedure:**
1. **Setup:**
   - Connect one donor gun to XT30U channel 1
   - Fill 1L bladder with water (or dilute solution for safety)
   - Priming: Use PRIME button to fill all hoses with water

2. **Trigger gun:**
   - Press gun trigger (activates motor, draws current through ACS758)
   - Observe GUN LED → should light immediately
   - Observe PUMP LED → should light within 25 ms
   - Water should flow into gun outlet within ~1 second (accounting for line fill)

3. **Hold trigger for 5 seconds:**
   - GUN and PUMP LEDs remain on continuously
   - Water flows steadily
   - Release trigger

4. **Measure pump off-delay:**
   - After releasing gun trigger, GUN LED goes out immediately
   - PUMP LED remains on for ~350 ms (from RV2 calibration)
   - At 350 ms mark, PUMP LED goes out
   - Pump motor should stop spinning (no more water flow)

5. **Repeat with both guns:**
   - Connect channel 2 gun as well
   - Trigger channel 1 alone → pump activates for channel 1 only; continues for 350 ms after release
   - Trigger channel 2 alone → same behavior
   - Trigger both simultaneously → pump runs; continues for 350 ms after BOTH released
   - Trigger channel 1, then channel 2 while channel 1 held → pump supplies both; timer resets each time current detected

**Acceptance criteria:**
- [ ] Pump activates <25 ms after gun current detected
- [ ] Pump continues running while gun is triggered
- [ ] Pump continues for 300–400 ms after all triggers released
- [ ] No pump activation during idle
- [ ] Behavior consistent across 10 trigger cycles per gun

**Gun activation test data:**
- Channel 1 activation delay: ____ ms
- Channel 1 off-delay: ____ ms
- Channel 2 activation delay: ____ ms
- Channel 2 off-delay: ____ ms
- Dual-gun behavior: PASS / FAIL (notes: _____________)

**Pass/Fail:** ____

---

### Test 5.3: Pump Off-Delay Tuning (RV2 Calibration)

**Objective:** Set RV2 potentiometer for 350 ms pump shutoff delay (prevents cavitation and solution dripping when guns are released).

**Procedure:**
1. **Bench setup (with oscilloscope):**
   - Monitor TP11 (PUMP_GATE) or pump current with oscilloscope
   - Simulate gun trigger via simulated ACS input (J2 pin 3 set to ~2.6 V for 1 A gun current)
   - Apply step signal: 0 → 2.6 V (gun on) for 1 second, then return to 2.5 V (gun off)
   - Scope trigger on rising edge of ACS_OUT step

2. **Measure response:**
   - Q2 gate (TP11) should rise within 25 ms of ACS step
   - Q2 gate should fall to <0.20 V at time = ~350 ms after ACS_OUT step ends
   - Measure exact time: **off-delay = ____ ms**

3. **Adjust RV2:**
   - If off-delay <300 ms: turn RV2 **clockwise** (increase capacitor discharge time)
   - If off-delay >400 ms: turn RV2 **counter-clockwise** (decrease capacitor discharge time)
   - Repeat step 2 until off-delay = 350 ±50 ms

4. **Lock RV2 setting:**
   - Mark trimmer dial position with permanent marker (for field reference)
   - Record rotations and final position

**Acceptance criteria:**
- [ ] RV2 calibrated to 350 ±50 ms delay
- [ ] Delay repeatable within ±20 ms across 10 cycles
- [ ] Final position marked for future reference
- [ ] Clockwise = longer delay (physically verified)

**RV2 Calibration log:**
- Initial delay estimate: ____ ms
- Adjustment direction: CW / CCW
- Final delay measured: ____ ms
- Final RV2 dial position: ______ (rotations or angle from minimum)
- Position marked for field reference: YES / NO

**Pass/Fail:** ____

---

## 6. Bypass and Recirculation Behavior

### Test 6.1: Check Valve and Bypass Restrictor Function

**Objective:** Verify recirculation bypass prevents siphoning when pump stops and restrictor tuning allows 5–10 mL/min flow.

**Procedure:**
1. **Check valve orientation:**
   - Inspect valve body; arrow should point toward pump inlet (reservoir return direction)
   - If arrow points wrong way, physically reverse valve before reassembly

2. **Bench test without guns:**
   - Fill 1L bladder with water (not solution, for safety)
   - Prime pump for 5 seconds via PRIME button
   - Observe outlet tee 2; water should flow only to the two gun channels (or be shut off by their slide clamps)
   - Outlet tee 1's bypass branch should have quiet recirculation (listen for gurgling; restrictor tuning target is to keep flow steady, not excessive)

3. **Stop pump (release PRIME):**
   - Pump stops after ~350 ms
   - Check valve should hold pressure; water should NOT siphon back into pump (no backflow sound)
   - Gun channels should NOT drip significantly (allow <1 mL/min drip due to residual pressure)

4. **Restrict bypass flow:**
   - If bypass gurgling is loud or splashing (indicating high flow), slide the bypass slide clamp further toward the arrow to restrict flow
   - The shallow ramp self-locks (no screw); confirm it holds its setting under pump pressure
   - Retest; target is quiet, steady recirculation without splashing or backpressure buildup (system design targets 0.2–0.5 psi exit pressure)

5. **Hold gun outlet high:**
   - Raise gun outlet hose 5 feet above reservoir surface
   - Prime pump; water should flow upward to hose end
   - Release pump; water should NOT flow back down (check valve prevents siphoning)

**Acceptance criteria:**
- [ ] Check valve arrow points toward inlet
- [ ] No siphoning when pump stops (gun channels do not drip >1 mL/min)
- [ ] Bypass flow 5–10 mL/min (audible but not loud)
- [ ] Gun hose at +5 ft elevation does not drain when pump off

**Bypass test data:**
- Check valve arrow direction: CORRECT / REVERSED
- Drip rate after pump stop (at 1 ft height): ____ mL/min
- Bypass flow rate: ____ mL/min (estimated by timing container fill; record for baseline; no specific limit, observe for excessive splashing/pressure)
- 5-ft elevation drain test: NO DRAIN / DRAIN (if drain, recheck check valve)

**Pass/Fail:** ____

---

## 7. Leak Test

### Test 7.1: Pressurized Soap Bubble Test (Benchtop)

**Objective:** Identify leaks at all fluid connections under simulated operating pressure.

**Procedure:**
1. **Prepare test fluid:**
   - Mix 1L water + 1 mL dish soap (for bubble visibility)

2. **Fill and prime:**
   - Fill 1L bladder with soapy water
   - Prime pump for 10 seconds via PRIME button (all lines filled)
   - Shut off PRIME; allow system to rest for 1 minute

3. **Apply gentle air pressure:**
   - Connect low-pressure air pump or hand-operated pump to gun outlet (open one channel slide clamp)
   - Apply ~0.5 psi air pressure gradually
   - Observe all connections with eye and ear:
     - Pump inlet/outlet barbs
     - Tee fittings (all three: inlet tee, outlet tee 1, outlet tee 2)
     - Check valve inlet/outlet
     - Gun outlet hoses at barb connections
     - Zip ties (if foam visible on hose, tie is cutting into silicone)

4. **Mark any leaks:**
   - Use tape or dry-erase marker to identify location
   - Record severity: hairline weep, steady drip, or stream
   - Typical causes and fixes:
     - Hose slips off barb: remove hose, warm in hot water, re-seat firmly, use zip tie
     - Barb mismatch (hose ID vs. barb OD): replace barb with correct size
     - Overtightened zip tie (cutting into hose): loosen tie, reposition or replace hose section
     - Defective tee or union: replace component

5. **Retest after repairs:**
   - Reapply 0.5 psi pressure
   - Confirm all previously identified leaks are resolved
   - Continue pressure test for 5 minutes; no new leaks should appear

**Acceptance criteria:**
- [ ] Zero visible leaks at 0.5 psi
- [ ] All barbs fully seated (hose depth >10 mm on barb)
- [ ] All zip ties snug but NOT cutting into silicone (should take ~5–10 N force to slide hose)
- [ ] No foam or deformation visible at clamp points

**Leak test log:**
- Leaks found: NONE / YES (list locations: _______________)
- Repairs made: (list all)
- Retest result: NO LEAKS FOUND / PASS

**Pass/Fail:** ____

---

### Test 7.2: Dynamic Leak Test (Pump Operating)

**Objective:** Verify no leaks during actual pump operation with solution flow.

**Procedure:**
1. **Setup:**
   - Drain soapy water from previous test; replace with 1L mixed bubble solution (100 mL JOYFY concentrate + 900 mL water)
   - Connect both donor guns; open both channel slide clamps fully

2. **Run pump for 30 seconds:**
   - Use PRIME button or gun triggers to keep pump running continuously
   - Observe all hose connections, tees, check valve, and gun outlets for weeps or drips
   - Audible cues: hissing = leak, gurgling = normal bypass

3. **Check gun channels:**
   - Ensure solution flows steadily to both gun inlets (should see liquid moving through tubing)
   - No leaking at barb connections (zip ties snug but not crushing hose)

4. **Record observations:**
   - Any new leaks? If yes, mark and repair (same procedure as Test 7.1)
   - Solution color/clarity maintained? (indicates no contamination from materials)

**Acceptance criteria:**
- [ ] No new leaks at operating pressure
- [ ] Solution flows steadily to gun channels
- [ ] Gun outlet hoses NOT weeping or dripping (allow <0.5 mL/min total drip from both)

**Dynamic test result:**
- Leaks observed: NO / YES (locations: _______________)
- Gun flow: NORMAL / WEAK (if weak, check for air locks)
- Drip rate (both guns combined): ____ mL/min
- Result: PASS / FAIL

**Pass/Fail:** ____

---

### Test 7.3: Stick Cap Seal Wet Test and Cup Drain

**Objective:** Check that the stick's dry tube stays dry. The cap's TPU ring is a starting geometry for a seal, not a proven one, and the bulkhead grommet is only a splash baffle.

**Procedure:**
1. Close the stick: TPU ring in the cap skirt's groove, cap fitted, both M3×10 cap screws in with their TPU and flat washers (each screw should pass fully through its nut; snug, not over-torqued). The RV1/RV2 windows are closed with the TPU trimmer plug, the USB-C port with its plug, the LED holes are filled with clear glue, and the PRIME boot is clamped under its glued bezel
2. Splash and spray water over the cap and the outside of the tube, as rain or spilled solution would in use (no submersion)
3. Pour a little water into the cup and confirm it drains through the cup floor
4. Open the cap and check the dry side (cap underside, PCB, sled, top of the grommet) for any water

**Acceptance criteria:**
- [ ] No water inside the dry tube
- [ ] Cup drains through its floor and wall drains; no standing water around the fittings
- [ ] Grommet top face filled with neutral-cure silicone once the wiring is final; drip skirt fitted; every cable has a drip loop below the cup
- [ ] Lay the closed, wet stick on each of its four sides for 5 minutes: water runs out of the down-facing wall's drains, and the dry side stays dry

**Pass/Fail:** ____

---

## 8. Shake, Vibration, and Mechanical Stability Test

### Test 8.1: Component Wiggle Test

**Objective:** Ensure no loose components or mechanical failures from assembly stress.

**Procedure:**
1. **Backpack assembly (fully integrated):**
   - Battery and electronics on the sled inside the stick's tube, cap screwed on (the cap's TPU-padded ribs pin the sled)
   - PCB hung under the cap on its heat-staked pins
   - Pump strapped into its pocket in the cup
   - All hoses in place, clipped at ~1 m intervals
   - Both umbilical harnesses connected to pack channels

2. **Shake test (30 seconds):**
   - Hold backpack at chest level with both hands
   - Shake vigorously side-to-side and up-and-down (simulating dance motion)
   - Listen and feel for:
     - Rattling or clicking from loose battery tabs, or the sled moving in the tube
     - Pump bouncing in its pocket
     - PCB shifting on its pins
     - Connectors becoming loose or partially unlatched

3. **Document findings:**
   - Any loose components?
   - Any mechanical noise?
   - Any connector movement?

4. **Connector latch verification:**
   - Attempt to manually pull apart XT30U and XT60H connectors while system is vibrating
   - Should require intentional unlatching; no accidental disconnection

**Acceptance criteria:**
- [ ] No rattling or loose component noise
- [ ] No PCB movement on its pins
- [ ] No battery tab shifting or cracking sounds; no sled rattle
- [ ] No pump bouncing excessively (zip ties hold it in its pocket)
- [ ] XT30U/XT60H connectors remain latched and secure

**Shake test results:**
- Loose component noise: NO / YES (describe: _______________)
- Connector security: FIRM / LOOSE (any failed latches: _______________)
- Mechanical stability: GOOD / POOR
- Result: PASS / FAIL

**Pass/Fail:** ____

---

### Test 8.2: Zip Tie and Strain Relief Integrity

**Objective:** Verify zip ties are secure and NOT cutting into soft silicone tubing.

**Procedure:**
1. **Visual inspection of all zip ties:**
   - Locate every zip tie securing barbs on the system
   - Check for foam or deformation of silicone underneath tie (indicates overtightening)
   - Try to slide hose past tie with finger; should require ~5–10 N force (moderate grip, not trivial but not excessive)

2. **Repair overtightened ties:**
   - If hose is deformed, cut and remove tie
   - Inspect hose for cutting/scoring; if minor, trim ~1 cm and re-seat on barb
   - If significant damage, replace hose section
   - Reinstall tie with less force (should NOT visibly compress silicone)

3. **Strain relief assessment:**
   - Examine umbilical harnesses where they leave the cup floor
   - The printed umbilical bricks at each end should transfer load to the paracord (not sharp bends); XT30U strapped in its pocket, wires and tube held in their grooves
   - Flex hose gently by hand; should not cause pinching at exit points

**Acceptance criteria:**
- [ ] No foam/deformation visible at any zip tie point
- [ ] Hose can be slid 5–10 mm with moderate force (not stuck, not loose)
- [ ] Umbilical bricks intact and not cracked
- [ ] No sharp kinks in hoses exiting pack

**Zip tie inspection log:**
- Zip ties checked: ____ total
- Deformations found: NONE / YES (locations: _______________)
- Repairs needed: (list)
- Strain relief condition: GOOD / CRACKED (location: _______________)
- Result: PASS / FAIL

**Pass/Fail:** ____

---

## 9. Thermal Performance

### Test 9.1: Battery and Controller Temperature Under Load

**Objective:** Verify thermal performance during continuous operation; ensure no over-temperature conditions.

**Procedure:**
1. **Setup:**
   - Place backpack in 50°C environment (or summer room at ambient 25°C; results adjusted by +25°C offset)
   - Charge battery to 8.4 V; allow to rest 1 hour to reach ambient temperature

2. **Run continuous operation for 10 minutes:**
   - Both guns firing continuously (PRIME held or gun triggers held)
   - Pump running full-time, motors spinning
   - Record temperature at 2 min, 5 min, and 10 min intervals using thermometer

3. **Measure component temperatures:**
   - **Battery:** Contact thermometer on the cells or cell holders with the cap off, or on the tube wall beside the battery (or thermal imaging if available)
   - **PCB (U1 area and Q2 MOSFET):** Contact thermometer on top of board near components
   - **Pump housing:** Contact on plastic exterior
   - **XT30U connectors:** Contact on connector body

4. **Record ambient temperature** at test location

**Acceptance criteria (for 50°C ambient test):**
- [ ] Battery temperature rise: <20 °C above ambient (suggested criterion, not a sourced spec; Joey has felt cells get nearly too hot to touch on the 2S1P gun)
- [ ] PCB temperature rise: <20 °C above ambient (suggested criterion)
- [ ] Pump temperature rise: <15°C above ambient (target <65°C)
- [ ] XT30U connectors: <10°C rise (target <60°C)

**If test is at lower ambient (e.g., 25°C):**
- Add 25°C offset to ambient for 50°C worst-case estimate
- E.g., if rise is 10°C at 25°C ambient, estimate 10°C rise at 50°C (confirm if possible)

**Thermal test data (at ambient ____ °C):**
- Time 0 min: Battery __°C, PCB __°C, Pump __°C
- Time 2 min: Battery __°C, PCB __°C, Pump __°C
- Time 5 min: Battery __°C, PCB __°C, Pump __°C
- Time 10 min: Battery __°C, PCB __°C, Pump __°C
- **Temperature rise:** Battery __°C, PCB __°C, Pump __°C
- **Estimated at 50°C ambient:** Battery __°C, PCB __°C, Pump __°C

**Pass/Fail:** ____

---

## 10. Hose Head-Height Test (Pump Suction Capability)

### Test 10.1: Raise Gun Inlet 5 Feet Above Reservoir

**Objective:** Verify pump can lift solution 5 feet vertically without cavitation or failure.

**Procedure:**
1. **Setup:**
   - Mount gun inlet barb on a stand or clamp ~5 feet (1.5 m) above the 1L bladder surface
   - Hose runs vertically from bladder → pump → up to gun inlet barb
   - Fill bladder with water (clear so you can watch solution level)

2. **Prime pump:**
   - Activate PRIME button for 10 seconds
   - Solution should flow upward through hose
   - Record time for solution to reach gun inlet barb (should be <10 seconds for 5-foot run)

3. **Release pump:**
   - Stop PRIME; solution should remain in elevated hose (check valve prevents siphoning)
   - Hose should NOT drain back into bladder (indicates check valve working)

4. **Verify no cavitation:**
   - Listen for hissing or grinding sounds during upward flow (indicates cavitation)
   - If cavitation heard, problem likely: wrong check valve orientation, blocked inlet, or pump inadequacy
   - Verify check valve arrow points toward reservoir (toward pump inlet)

**Acceptance criteria:**
- [ ] Solution reaches 5-foot elevation within 10 seconds
- [ ] No hissing or cavitation sounds during prime
- [ ] Hose does NOT drain after pump stops (check valve holding)
- [ ] Solution can be dispensed from elevated gun inlet (no air locks)

**Head-height test data:**
- Elevation: 5 feet / ____ feet
- Prime time to reach inlet: ____ seconds
- Cavitation sounds: NO / YES
- Siphoning when pump stops: NO / YES (if yes, check valve failure)
- Result: PASS / FAIL

**Pass/Fail:** ____

---

## 11. LED Backpack Power and Display

### Test 11.1: LED Backpack Powered Operation (Optional Feature)

**Objective:** Verify LED backpack receives sufficient 5V power and operates without voltage sag.

**Procedure:**
1. **Backpack LED power supply:**
   - Connected via second 5V buck converter (separate from pump regulation)
   - Input: 2S battery (via breaker)
   - Output: 5V into backpack LED controller (USB or DC barrel connector)

2. **Power-up test:**
   - Apply battery power (XT60H connected)
   - Backpack LED panel should display (color pattern, text, or animation per LED design)
   - Monitor 5V output with multimeter: should be 4.95–5.05 V at idle

3. **Load test:**
   - Run pump and guns simultaneously (load backpack LEDs heavily if they support brightness adjustment)
   - Voltage should remain ≥4.85 V during peak load (pump + backpack LEDs)
   - If voltage sags <4.8 V, check:
     - Buck converter output regulation under load
     - Wire size/length in backpack power harness
     - LED controller power consumption

4. **Field observation:**
   - LED display should be visible in daylight (venue lighting)
   - Colors should be vibrant (not dimmed or washed out)

**Acceptance criteria:**
- [ ] Backpack LED controller powers up without errors
- [ ] 5V supply remains 4.85–5.05 V under full load (pump + LEDs)
- [ ] LED display visible and operational at intended brightness
- [ ] No flicker or dropout during 10-minute continuous run

**LED backpack test data:**
- Idle voltage (no pump/LEDs): ____ V
- Peak load voltage (pump + LEDs): ____ V
- LED display brightness: GOOD / DIM / NOT VISIBLE
- Flicker observed: NO / YES (frequency: ____ Hz if yes)
- Result: PASS / FAIL / NOT APPLICABLE (if LED backpack not used)

**Pass/Fail:** ____

---

## 12. Controller Stability and Noise Rejection

### Test 12.1: False Start Prevention (Electrical Noise Immunity)

**Objective:** Confirm controller does NOT activate pump during startup transients, BMS balancing, or motor noise.

**Procedure:**
1. **Power-up sequence:**
   - Disconnect J2 (ACS758) temporarily
   - Apply 5V to PCB (J1)
   - Monitor TP11 (PUMP_GATE) for any glitches or pulses
   - Expected: TP11 remains <0.05 V for entire startup sequence (~500 ms)

2. **BMS balancing test:**
   - Charge battery to 8.4 V; allow BMS to balance (may run for 1 hour quietly)
   - Monitor GUN and PUMP LEDs; should remain off during balancing
   - No false pump starts should occur

3. **Motor noise immunity:**
   - Reconnect J2 (ACS758 sensor)
   - Run pump alone (without gun current) for 30 seconds via PRIME button
   - GUN LED should remain OFF (pump current NOT detected on gun side)
   - PUMP LED controlled only by PRIME switch, not by motor noise coupling

4. **Oscilloscope observation (optional):**
   - Scope TP5 (ACS_FILTER) during pump operation
   - Should see clean ~2.5 V reference with <20 mV ripple (motor noise filtered)

**Acceptance criteria:**
- [ ] No PUMP_GATE glitches during power-up
- [ ] GUN LED remains off during pump-only operation
- [ ] No false activations during BMS balancing
- [ ] TP5 noise <20 mV peak-to-peak (filtered signal clean)

**Noise immunity test results:**
- TP11 glitches during startup: NO / YES (max duration: ____ ms)
- False pump starts: 0 / ____ (count)
- Motor noise on TP5: ____ mV peak-to-peak
- Result: PASS / FAIL

**Pass/Fail:** ____

---

## 13. Integration Test: Dual-Gun System Behavior

### Test 13.1: Concurrent Dual-Gun Operation

**Objective:** Verify both guns can fire simultaneously, each independently triggerable, with no crosstalk or control conflicts.

**Procedure:**
1. **Setup:**
   - Both donor guns connected to XT30U channels (Channel 1 and Channel 2)
   - 1L bladder filled with mixed bubble solution
   - System primed via PRIME button (30 sec run, all hoses filled)

2. **Test sequence:**

   **A) Single gun (Left):**
   - Trigger Left gun; GUN and PUMP LEDs on
   - Bubble production steady; Right gun silent (its slide clamp closed or disconnected)
   - Release Left gun; pump off after 350 ms delay
   - Repeat 3 times; timing consistent

   **B) Single gun (Right):**
   - Repeat with Right gun only; timing and behavior identical to Left

   **C) Dual-gun simultaneous:**
   - Both guns connected with both channel slide clamps fully open
   - Trigger both simultaneously
   - GUN LED on immediately; PUMP LED on within 25 ms
   - Bubble production from both gun heads (total output roughly doubled vs. single gun)
   - Solution flow balanced (both gun outlets flowing at similar rate)
   - Release both guns; pump off after 350 ms

   **D) Sequential triggering:**
   - Trigger Left gun; pump activates
   - 2 seconds later, trigger Right gun (while Left still held)
   - Pump continues (already running); no on/off cycle
   - Right gun inlet receives solution within ~500 ms (delay for solution to reach inlet)
   - Release Left while Right held; PUMP continues (Right still drawing current)
   - Release Right; PUMP off after 350 ms

   **E) Rapid tapping:**
   - Rapid trigger taps (<100 ms each) on Left gun 5 times
   - PUMP should activate/deactivate for each tap
   - No missed activations or false starts

3. **Crosstalk verification:**
   - Connect both guns and close the Right slide clamp (block flow to Right channel)
   - Trigger Left gun; solution should flow only to Left
   - Measure pressure in Right hose (by feel or manometer); should be <0.1 psi (open line, no pump pressure)
   - Right pump channel isolated by its slide clamp; no solution leakage

**Acceptance criteria:**
- [ ] Left gun fires consistently (3/3 trials successful)
- [ ] Right gun fires consistently (3/3 trials successful)
- [ ] Dual-gun firing: both output simultaneously, combined bubble rate >200 bubbles/sec
- [ ] Sequential triggering: second gun activates within 500 ms; PUMP continues without restart
- [ ] Rapid tapping: all 5 activations successful (no missed or delayed starts)
- [ ] No crosstalk: Right channel isolated when closed; no pressure observed

**Dual-gun test results:**
- Left-only success rate: ____ / 3
- Right-only success rate: ____ / 3
- Dual simultaneous: PASS / FAIL
- Sequential test: PASS / FAIL (right gun activation time: ____ ms)
- Rapid-tap success: ____ / 5
- Crosstalk test: PASS (isolated) / FAIL (pressure observed)
- Result: PASS / FAIL

**Pass/Fail:** ____

---

## 14. Pre-Event Final Checklist (the target festival 2026-10-30/31)

**To be completed 1 day before festival departure (2026-10-29):**

### Electrical Systems
- [ ] Battery fully charged: 8.40 ± 0.10 V open-circuit
- [ ] BMS balanced: voltage spread <0.05 V (cells matched)
- [ ] Breaker reset lever ON (armed), checked with the sled out before the stick was closed
- [ ] Power key pulled and replaced with the stick closed: everything goes off and comes back (Test 3.3)
- [ ] All connectors (XT60H, XT30U, JST-XH) latched firmly; test by gentle pull
- [ ] Controller (PCB) powered on; all three LEDs respond to PRIME
- [ ] RV1 and RV2 calibration locked: dial positions marked

### Fluid System
- [ ] Bladder filled: 1 L mixed solution (100 mL JOYFY + 900 mL water)
- [ ] Pump primed: all hoses filled, no air locks; test via PRIME (30 sec run)
- [ ] Check valve arrow points toward inlet (toward reservoir)
- [ ] Gun channels: both channel slide clamps accessible, responsive, and holding their setting
- [ ] No leaks observed at any hose connection during 2-minute bench test

### Guns & Umbilicals
- [ ] Both donor guns connected and motors spin freely
- [ ] XT30U connectors latched and secure (intentional unlatching required)
- [ ] Umbilical harnesses bundled and protected (no kinks, no sharp bends)
- [ ] Paracord load-bearing tethers intact (no fraying, no cuts)
- [ ] Umbilical bricks fitted at both ends of each umbilical (XT30U strapped in, paracord tied through)

### Backpack Integration
- [ ] Sled pinned in the tube by the cap's compliant TPU battery pads (no rattle, no movement during shake; shim strips in any pocket where a board moves; the cap seats fully)
- [ ] Pump strapped into its 52 × 46 mm pocket in the cup
- [ ] PCB hung under the cap, heat-staked on its pins (secure, no flexing); RV1/RV2 windows closed with the TPU trimmer plug; USB-C plug fitted when not charging
- [ ] All internal hoses clipped at 1 m intervals (no dangling loops)
- [ ] Loaded weight felt comfortable (wear for 2 minutes; feedback: ___________)
- [ ] Umbilicals plug into the gun ports on the cup's outer wall with drip loops below; no interference with arm movement
- [ ] USB-C charge port on top of the cap reachable; charge with the cap off until Test 2.2 has passed
- [ ] Unplugged gun port wells closed with TPU port caps; USB-A plug fitted when the backpack is not connected; power key stored on its lanyard

### Testing & Documentation
- [ ] All test results logged (Sections 1–13): PASS / FAIL status per test
- [ ] Any repairs or rework documented: (list: _______________)
- [ ] Field calibration notes: RV1 position, RV2 position, measured gun current
- [ ] Spare parts on hand: 1× JOYFY 32 oz concentrate, 1× backup bubble solution (1 L pre-mixed)
- [ ] Charging supplies: USB-C power adapter (for venue charging between sessions)
- [ ] Tool kit: multimeter, flashlight, zip ties, electrical tape, spare hoses/barbs

### Venue & Environmental
- [ ] Backpack size verified against venue bag restrictions (if applicable)
- [ ] Water/moisture protection: cap seal wet-tested (Test 7.3); no exposed solder joints, connectors covered when not in use
- [ ] Temperature range: system tested or rated for expected venue temperature (if festival is <0°C or >40°C, note any thermal derating)
- [ ] System readiness: perform final 5-minute test fire at venue (or pre-event location) within 1 hour of performance

### Contingency
- [ ] Known issues documented: (list: _______________)
- [ ] Workarounds prepared: (list: _______________)
- [ ] Service contact or backup power source: (if applicable)
- [ ] Backup guns or umbilical harnesses: (if spares available)

**Final checklist status:**
- All systems: **READY / NOT READY** (describe any blockers: _______________)
- Last test fire: ______ (time), Result: SUCCESSFUL / ISSUES OBSERVED (describe: _______________)
- Deployment confidence: **HIGH / MEDIUM / LOW** (explain: _______________)

---

## End of Test Plan

All tests completed: __________ (date)
Tester name: ____________________________
Festival/event: **the target festival**
Festival dates: **2026-10-30 to 10-31**
Completion deadline: **2026-10-29** (day before event)
