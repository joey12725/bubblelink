# Bring-up and Acceptance Test

Complete step-by-step electrical commissioning and acceptance procedure for the assembled BubbleLink CTRL board after PCBWay hand-solders through-hole components. All bench gates required for full qualification are documented, including measurements, acceptance criteria, and pass/fail thresholds.

## Scope and prerequisites

**When to run:** After SMT assembly (PCBWay) is complete, all through-hole parts are soldered, and the board has passed unpowered visual inspection.

**Personnel:** Engineer with oscilloscope, multimeter, current-limited bench supply (5 V, 1–2 A adjustable), and access to a simulated sensor source (0–5 V adjustable, <1 kΩ impedance).

**Safety:** Use a current-limited supply throughout to avoid damage from accidental shorts. Do not power the board beyond 5.25 V or 2 A continuous.

---

## 1. Unpowered inspection

Before applying power, verify physical assembly and polarity.

### Checklist

- [ ] Board revision: confirm "v1.2" marking (not v1.1)
- [ ] Dimensions: 50 × 40 × 1.6 mm ✓
- [ ] Four 3.2 mm mounting holes present and clear ✓
- [ ] U1 (TLV1822QDRQ1) pin 1 (lower-left pad after rotation) correctly soldered; inspect pad geometry against assembly PDF
- [ ] U2 (TLV803EA43DBZR) SOT-23-3 pinout correct (pin 1 GND, pin 2 RESET_N, pin 3 VDD); do NOT accept RDBZ/VDBZ variant
- [ ] Q1, Q3 (DMP2065UQ-7, P-channel) gate orientation; Q2 (AO3400A, N-channel) gate orientation
- [ ] D1 (B340A-E3/61T) band faces PUMP+ (pad 1); verify band location matches silkscreen
- [ ] F1 (1812L150/16DR) polarity not applicable (non-polar PTC); check solder coverage
- [ ] C1 (100 µF electrolytic) positive lead to square pad (pad 1) and + silkscreen mark
- [ ] C6 (22 µF 1210) and C7 (6.8 µF 1206) correct sizes (not swapped)
- [ ] All THT headers (J1, J2, J3) soldered with pin 1 to square pads; connector opening outlines match assembly drawing
- [ ] RV1/RV2 (Bourns trimmers) physical lead order 1–3–2 (NOT 1–2–3), all three leads soldered
- [ ] SW1 (Omron B3F-1000) seated flush; pins 1/2 and 3/4 not shorted
- [ ] LED1–3 cathodes (short leads, flat sides) to pad 1 and K marks; anodes to pad 2
- [ ] **Unpopulated:** R22 (DNP) pads empty; J4 (DNP) holes empty ✓
- [ ] **Populated:** C9 and R18 fitted (both are SMT parts required for operation) ✓
- [ ] **THT assembly complete:** All 10 THT components present and soldered; no missing or reversed parts ✓

### Electrical continuity check (unpowered)

Use a multimeter set to resistance (Ω) or continuity mode.

| Test | Measurement | Acceptance |
|---|---|---|
| J1 pin 1 to GND (J1 pin 2) | ~0 Ω | Short or low resistance (capacitive discharge okay) |
| J3 pin 2 to GND | ~0 Ω | Unpowered trace resistance; should be low |
| J3 pin 1 to GND (unpowered) | High Ω (>1 MΩ) | No shorts; Q2 off-leakage only |
| J2 pins unpowered | No DC path to GND or +5V | All three pins isolated until powered |

If any unexpected shorts are found, do not proceed. Inspect solder bridges and rework as needed.

---

## 2. Logic-only bring-up (no sensor or pump)

Test the control logic in isolation: power supply, supervisor, comparators, and LEDs.

### Setup

- Leave **J2 (ACS sensor)** disconnected
- Leave **J3 (pump)** disconnected
- Set **J1 input to 5.00 V** nominal, 100 mA current limit on bench supply
- Prepare oscilloscope for multi-channel monitoring
- Allow board to settle for >10 seconds after power-on

### Measurements (record actual values)

| Signal | Test point | Expected range | Pass/Fail |
|--------|-----------|---|---|
| **Supply current** | J1 | No limiting, <50 mA, no heating or odor | PASS if <50 mA and no thermal issues |
| **+5V_PUMP rail** | TP1 | 4.95–5.05 V @ 5.00 V input | PASS if within range |
| **+5V_LOGIC rail** | TP2 | Within 50 mV of TP1 (4.95–5.05 V) | PASS if ripple <50 mV peak-to-peak |
| **VMID (buffered half-supply)** | TP8 | 2.40–2.60 V after >1 s settling | PASS if within range |
| **VDELAY (timer reference)** | TP10 | 0.98–1.06 V | PASS if within range |
| **HOLD (charge node)** | TP9 | <0.10 V idle | PASS if <0.10 V after power-up and settling |
| **TIMER_N (active-low output)** | TP14 | >4.5 V (open-drain released) | PASS if >4.5 V |
| **PUMP_GATE (Q2 gate)** | TP11 | <0.05 V idle | **CRITICAL: STOP if >0.05 V. Pump must be off at idle.** |

### LED status (unpowered J2, J3)

| LED | Expected state | Notes |
|---|---|---|
| **POWER (LED1, green)** | ON | Always on when J1 powered; indicates +5V_LOGIC present |
| **GUN (LED2, yellow)** | OFF | No sensor; DET_N released (high) |
| **PUMP (LED3, red)** | OFF | PUMP_GATE low; Q2 off; pump relay off |

### Acceptance

- All rail voltages within specification
- All LED states correct
- **PUMP_GATE <0.05 V (pump safe off at idle)**
- No excessive supply current (<50 mA logic-only)

---

## 3. Controlled startup and brownout gate

Test power-on sequencing and supervisor clamp operation. This is a **critical bench gate (PWR-000 through PWR-004).**

### Setup and test sequence

**Equipment:** Oscilloscope (4-channel minimum: TP2, RESET_N side of R23, TP9, TP14, TP11); current-limited 5 V supply with voltage ramp capability.

**Monitor all five signals simultaneously:**
1. **TP2** (logic rail)
2. **U2 RESET_N / R23 junction** (supervisor output clamp)
3. **TP9** (HOLD charge node)
4. **TP14** (TIMER_N active-low)
5. **TP11** (PUMP_GATE, must remain low)

### Test 1: Hard connect/disconnect (10 cycles)

Quickly connect and disconnect 5.00 V supply to J1 ten times.

| Parameter | Acceptance |
|---|---|
| Pump-gate voltage during invalid supply | <0.65 V (no spurious pulse above logic threshold) |
| PUMP_GATE falltime after RESET_N asserts | <15 ms to below 0.20 V |
| Worst-case waveform | Record and save for later reference |

**FAIL criterion:** Any PUMP_GATE pulse above 0.65 V during power-up or power-down.

### Test 2: Slow ramps (0→5 V and 5→0 V at 0.1, 1, 10, 100 V/s)

Perform four ramp rates in each direction (up and down). Board must not initiate pump motion.

| Ramp rate | Up / Down | PUMP_GATE threshold | Acceptance |
|---|---|---|---|
| 0.1 V/s | 0→5 V and 5→0 V | <0.20 V throughout | No spurious pulse |
| 1 V/s | 0→5 V and 5→0 V | <0.20 V throughout | No spurious pulse |
| 10 V/s | 0→5 V and 5→0 V | <0.20 V throughout | No spurious pulse |
| 100 V/s | 0→5 V and 5→0 V | <0.20 V throughout | No spurious pulse |

**FAIL criterion:** Any transient PUMP_GATE >0.20 V during any ramp.

### Test 3: Brownout dips (supply dips through 4.2–4.6 V nominal)

Apply shallow supply dropouts at four dwell times: 1 ms, 10 ms, 100 ms, 1 s.

| Dwell time | Supply range | PUMP_GATE during dip | After recovery |
|---|---|---|---|
| 1 ms | Dip to ~4.3 V, hold, recover to 5.0 V | <0.20 V | <0.05 V within 15 ms |
| 10 ms | Dip to ~4.3 V, hold, recover to 5.0 V | <0.20 V | <0.05 V within 15 ms |
| 100 ms | Dip to ~4.3 V, hold, recover to 5.0 V | <0.20 V | <0.05 V within 15 ms |
| 1 s | Dip to ~4.3 V, hold, recover to 5.0 V | <0.20 V | <0.05 V within 15 ms |

**FAIL criterion:** Any spurious pump motion or gate rise above 0.65 V.

### Acceptance

- All 10 hard power cycles: no PUMP_GATE pulse >0.65 V
- All eight ramp cases (four rates × two directions): PUMP_GATE <0.20 V throughout
- All four brownout dips: PUMP_GATE <0.20 V during dip, <0.05 V within 15 ms after recovery
- Gate recovery time <15 ms in all cases

---

## 4. Simulated sensor calibration and detection

Test the detector circuit using a precision voltage source (0–5 V, <1 kΩ source impedance).

### Setup

- **J2 connected via 1 kΩ series resistor** from 0–5 V adjustable voltage source (ground-referenced)
- **J3 disconnected** (no pump load)
- **J1 at 5.00 V**
- **Oscilloscope monitoring:** TP5 (ACS_FILTER), TP6 (VTH, RV1 wiper), DET_N (U1 pin 1 output), TP9 (HOLD)

### Test 4a: RV1 threshold range

Manually adjust RV1 (2 kΩ trimmer) through its full range while observing TP6.

| Check | Expected | Acceptance |
|---|---|---|
| RV1 full clockwise (CW) | TP6 ≈ 2.80 V (high/safe, pump off) | PASS if ≥2.75 V |
| RV1 full counterclockwise (CCW) | TP6 ≈ 2.21 V (low/active, pump on) | PASS if ≤2.25 V |
| Clockwise motion | TP6 increases with CW rotation | PASS if increasing |
| Range span | TP6 sweeps 2.21–2.80 V (~0.59 V) | PASS if >0.50 V span |

**Trimmer lead order reminder:** RV1 physical pad order is 1–3–2 (wiper is pin 2). Verify leads are in correct order before soldering.

### Test 4b: Detection threshold and hysteresis

Slowly increase ACS_OUT voltage from 0 V while monitoring DET_N.

| Step | Action | Observation | Acceptance |
|---|---|---|---|
| 1 | Increase ACS_OUT from 0 V slowly | Record DET_N assertion voltage at TP5 and TP6 | Release threshold (lower) |
| 2 | Decrease ACS_OUT slowly from high voltage | Record DET_N release voltage at TP5 and TP6 | Turn-on threshold (higher) |
| 3 | Calculate hysteresis | Hysteresis = turn-on − release | PASS if 3–7 mV; expected ~4 mV |

**Setup hint:** At 5.00 V rail, a 2.50 V divider point (VMID) combined with RV1 creates the threshold. Hysteresis comes from R5 (4.7 MΩ) feedback from DET_N.

### Test 4c: Detection speed

Step the source from idle (below threshold) to at least 20 mV above threshold.

| Parameter | Expected | Acceptance |
|---|---|---|
| DET_N assertion latency | <25 ms (typically ~7 ms) | PASS if <25 ms |
| Q1 gate rise (charging HOLD) | Visible rise at TP9 within 10 ms | PASS if continuous rise, no glitches |
| Signal stability | No chatter or multiple transitions | PASS if clean single transition |

### Test 4d: Adjustable delay (RV2 and timer)

Manually adjust RV2 (100 kΩ trimmer) while observing HOLD discharge and TIMER_N behavior.

| Check | Action | Expected | Acceptance |
|---|---|---|---|
| Clockwise motion | Rotate RV2 CW | TIMER_N stays low longer (longer delay) | PASS if delay increases |
| 350 ms target | Adjust RV2 until delay ≈ 350 ms | RV2 position ≈ 0.564 fraction | PASS if 350 ± 50 ms reachable |
| Range | Sweep RV2 full range | Delay varies from ~35 ms (CCW) to ~574 ms (CW) | PASS if min 25 ms, max 750 ms |

**Procedure:** Trigger with PRIME; release; time DET_N release to TIMER_N rising (pump off). Repeat at different RV2 positions and record.

### Test 4e: PRIME button (manual trigger)

Hold SW1 (PRIME button) and release while observing all signals.

| Check | Expected | Acceptance |
|---|---|---|
| PRIME held | DET_N pulled low; GUN LED on; HOLD rises; TIMER_N low; PUMP_GATE rises | PASS if all signals respond |
| PRIME released | Normal delay countdown triggered (same as sensor release) | PASS if pump-off delay obeys RV2 setting |
| Rapid presses | 10 press/release cycles | No missed or hung transitions | PASS if all cycles complete normally |

### Test 4f: Sensor disconnect (J2 open)

With the board running normally, disconnect J2 (pull the connector).

| Check | Expected | Acceptance |
|---|---|---|
| Immediate response | DET_N released within 1 s | PASS if pump off within max 1 s |
| HOLD discharge | TP9 decays through (R9+RV2) ∥ R21 | PASS if decay visible |
| Pump-off delay | Respects calibrated RV2 delay from disconnect moment | PASS if standard delay applies |

### Acceptance

- RV1 threshold range: 2.21–2.80 V (or user-measured endpoint)
- Detection hysteresis: 3–7 mV without chatter
- Detection latency: <25 ms
- RV2 delay range: at least 25–750 ms, with 350 ms reachable ±50 ms
- PRIME button: 1,000 cycles without missed transitions
- Sensor disconnect: pump off within 1 s

---

## 5. Dummy-load output test

Test pump-gate driver with a resistive load (no real pump yet).

### Setup

- **J1:** 5.00 V supply, current limit raised to 500 mA
- **J2:** Simulated sensor (0–5 V source as in Section 4)
- **J3:** 100–300 Ω resistive load (5 V, 50–100 mA); example: two 200 Ω resistors in parallel = 100 Ω
- **Oscilloscope:** TP2 (logic rail), TP5 (sensor), TP6 (threshold), TP11 (PUMP_GATE), TP12 (Q2 drain / load voltage)

### Test sequence

1. **Trigger PRIME:** Hold SW1
   - TP11 (PUMP_GATE) should rise to ~4.5 V (Q2 on)
   - TP12 should drop to near ground (load powered)
   - TP2 should remain stable (no dip)

2. **Release PRIME:** Let SW1 go
   - PUMP_GATE falls over ~1 ms RC time
   - Load voltage rises back to rail
   - Delay countdown (RV2) should activate; pump off after configured delay

3. **Trigger with simulated sensor:** Use simulated ACS (Section 4 setup)
   - Assert above threshold
   - PUMP_GATE rises; load powered
   - Release (drop below threshold)
   - PUMP_GATE falls after RV2 delay

### Acceptance

| Parameter | Acceptance |
|---|---|
| PUMP_GATE high | ~4.5 V when on; <0.05 V when off |
| Load current | ~50–100 mA at 5 V (100 Ω dummy load) |
| TP2 stability | <50 mV ripple during load switch |
| TP5, TP6 noise | No visible movement or glitches during load switching |
| Delay control | RV2 setting respected; no timing anomalies |

---

## 6. External hardware release tests

These tests require real components: the actual ACS758 sensor module, the GROTHEN G528 pump, and the full harness with motor-end suppression. **These are the final bench gates before field deployment (B-003 through B-010).**

### Prerequisites

- Assemble the motor-end suppression: diode and capacitor across motor, twisted-pair harness, strain relief
- Verify diode polarity with a multimeter before connecting the motor
- Mount sensor and pump in a test rig (not in the final enclosure yet)
- Prepare an oven or thermal chamber for temperature testing (optional but recommended)

### 6a: ACS758 sensor and gun qualification

Record the ACS758 output voltage range at idle and when the gun fires. This determines the RV1 calibration threshold.

| Condition | Temperature | Measured ACS_OUT | Expected margin |
|---|---|---|---|
| **Gun idle** (no motor running) | 0°C | Record V_idle_0 | Noise floor typically 10–50 mV |
| **Gun idle** | 25°C | Record V_idle_25 | |
| **Gun idle** | 50°C | Record V_idle_50 | |
| **Gun active** (minimum current head) | 0°C | Record V_active_0 | Target ≥30 mV above idle; preferred ≥50 mV |
| **Gun active** | 25°C | Record V_active_25 | |
| **Gun active** | 50°C | Record V_active_50 | |

**Acceptance:** At each temperature, V_active − V_idle ≥ 30 mV (preferably ≥50 mV).

**RV1 calibration:** Once margins are confirmed, adjust RV1 so:
- TP6 (VTH) sits at least 10 mV above V_idle (safe margin for noise)
- TP6 at least 10 mV below V_active (safe margin for detection)
- Example: if V_idle = 0.5 V and V_active = 0.8 V, set VTH ≈ 0.60–0.70 V

**Field qualification:** Run ten start-and-release cycles at each temperature (0°C, 25°C, 50°C) with the calibrated RV1. Require zero misses and zero false triggers.

### 6b: Pump, buck converter, and PTC current limits

Measure pump operating current under steady state and transient load.

| Condition | Current | Temperature | Acceptance |
|---|---|---|---|
| **Steady run** | Pump on, no mechanical load | 25°C ambient | <0.60 A preferred |
| **Steady run (worst case)** | Pump on, filter blocked or high back-pressure | 50°C enclosure equivalent | <1.10 A (F1 hold-current limit derated) |
| **Startup transient** | First 100 ms after DET_N asserted | 25°C | Allow brief peak >0.60 A, but <1.5 A |
| **Brief stall** (do NOT sustain) | Motor mechanically constrained for <1 s | 25°C | Measure current rise; confirm <2.0 A |

**Thermal acceptance:**
- After 10 minutes continuous run at 50°C:
  - F1 temperature rise: <20°C above ambient
  - Q2 (MOSFET) temperature rise: <20°C above ambient
  - Connector J3 temperature rise: <20°C above ambient
  - D1 (diode) temperature rise: <20°C above ambient

**Rails acceptance:**
- TP1 (pump rail) and TP2 (logic rail) remain within 4.75–5.25 V during startup and continuous operation
- No brownout pulses on RESET_N

### 6c: EMI and motion (100-cycle pump test)

Run the pump 100 times (start and stop cycles) while monitoring logic and sensor integrity.

| Signal | Equipment | Scope requirement |
|---|---|---|
| **TP2** (+5V_LOGIC) | 4-channel oscilloscope | Monitor rail ripple; should stay >4.75 V, ripple <100 mVpp |
| **TP5** (ACS_FILTER) | | Monitor noise from motor switching; should not exceed ±0.2 V transients |
| **DET_N** | | Look for false assertions or release glitches during motor on/off |
| **RESET_N** (U2 side) | | Should not assert or dip spuriously |
| **TP11** (PUMP_GATE) | | Should transition cleanly; no ringing or chatter |

**Mechanical checks:**
- Shake the entire assembled system (bag + board + harness)
- Flex only the strain-relieved harness sections (not the board)
- Run another 100 pump cycles while shaking

**Acceptance:**
- Zero false detection starts or missed starts
- Zero unexpected RESET_N assertions (brownout)
- Zero stuck or intermittent pump operation
- No connector loosening or wire chafing
- No visible board fractures or solder joint cracks

---

## 7. Final calibration and field acceptance

Once all tests pass, the board is ready for integration into the final enclosure.

### RV1 calibration (final)

Set RV1 based on measured ACS758 data from Section 6a, **not guessed trimmer turns.**

1. Record V_idle and V_active at the temperature where the gun will operate most (typically 25°C)
2. Calculate target threshold: VTH_mid = (V_idle + V_active) / 2
3. Adjust RV1 so TP6 ≈ VTH_mid (using the adjustable voltage source from Section 4)
4. Confirm 10 mV safety margin on each side:
   - TP6 ≥ V_idle + 10 mV
   - TP6 ≤ V_active − 10 mV
5. Record final RV1 position (trimmer dial or distance estimate) for documentation

### RV2 calibration (final)

Set RV2 to 350 ms ±50 ms (or an alternate qualified value if required by fluid system design).

1. Configure a simulated sensor source to assert above threshold
2. Measure time from DET_N release to TIMER_N rising edge (pump off) using the oscilloscope
3. Adjust RV2 until delay ≈ 350 ms
4. Verify clockwise increases delay; counterclockwise decreases delay
5. Record final RV2 position for documentation

### Full system test (final)

With calibrated RV1 and RV2, perform the following tests:

| Test | Duration | Acceptance |
|---|---|---|
| **One gun (single head)** | 50 rapid trigger taps | Zero misses; zero false starts |
| **Dual gun or multi-head** | 50 cycles (if supported) | Both channels operate independently; no crosstalk |
| **Rapid trigger taps** | 100 press/release cycles at 5 Hz | No chatter; clean on/off |
| **PRIME button** | 100 cycles | Manual override works; delay countdown normal |
| **Sensor unplug** | Full/VOUT disconnect | Pump off within 1 s; board stable |
| **Pump unplug** | Motor harness disconnect | Board unharmed; no electrical transient |
| **Hard power cycle** | Connect/disconnect 10 times | No spurious pump motion; startup clean |
| **Breaker shutdown** | Activate upstream circuit breaker | Pump off cleanly; board remains safe |

### Conformal coating (optional)

Only apply after calibration and all tests pass.

- Mask connectors (J1, J2, J3), trimmer pots (RV1/RV2), tactile switch (SW1), LED optics, and all test points (TP1–15)
- Use a process compatible with high-impedance nodes; do not apply unqualified material
- Allow proper cure time per coating datasheet
- Retest all critical signals (rail voltages, thresholds, timings) after coating cure
- Confirm no coating seeped into connector contacts or switch mechanism

### Field acceptance test (in enclosure)

After the board is mounted in the final wearable pack:

1. Retest at the worst expected ambient temperature (typically 0°C or 50°C depending on season/venue)
2. Run 100 pump cycles to verify thermal stability in enclosure
3. Test all user controls (trigger, PRIME button) with gloved hand if applicable
4. Verify no fluid leaks from any joint
5. Confirm vibration tolerance (shake the pack; confirm no intermittent faults)
6. Document final configuration: RV1 position, RV2 position, pump model, gun head used, fluid reservoir capacity

---

## Bench gates and verification status

### Analog circuit model validation

The design was validated with a Monte Carlo model (20,000 samples) covering resistor tolerances, capacitor effective values, transistor thresholds/leakage, and supervisor specifications. Full results: `hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/verification/analog_model/verification_results.json`

**Model verdict:** MODEL_PASS; 20 vector tests pass or marked for bench confirmation. **Nine bench gates remain pending physical measurement:**

| Gate ID | Test / Requirement | Scope | This procedure section |
|---------|-------------------|-------|---|
| **START-002** | Q1 drive corner (model proxy pass; corner operation) | Temperature and load transient Q1 current | Section 6a |
| **PWR-000** | POR fail-off coverage (TLV1822 Hi-Z + R15 gate pulldown below 0.7 V supervisor range) | Below-0.7-V startup and power loss observation | Section 3 |
| **PWR-001** | Supervisor startup ramp (envelope: hard plug, 0.1/1/10/100 V/s) | Scoped hard ramps; zero pump motion at idle | Section 3, Test 2 |
| **PWR-002** | Supervisor clamp sweep (HOLD below active timer threshold 3.0–5.25 V with Q1 on) | Clamp voltage, steady-state sink current | Section 3, Test 3 |
| **PWR-003** | Supervisor brownout shutdown (reset sink current, gate decay, total pump-off time) | Shallow brownout waveforms; gate/drain ring-down | Section 3, Test 3 |
| **PTC-001** | F1 (1812L150/16DR) hold current derated at 50°C (1.10 A) | Production pump continuous current <1.10 A at 50°C including blocked-filter case | Section 6b |
| **ENV-001** | Sensor environmental window (0–50°C idle vs. active separation on RV1 fixed setting) | Real gun current profiles; actual ACS output range | Section 6a |
| **PWR-004** | Physical power transients (hard plug, slow ramp, shallow brownout, reconnect) | Full scope of startup transients; no spurious pump motion | Section 3 (all tests) |
| **EMI-001** | Pump inductive switching (10,000-cycle drain/logic integrity, G528 noise envelope) | Flyback peak, logic rail ripple, false detector transitions | Section 6c (100 cycles shown; extend to 10,000 if time permits) |

### Supporting bench gates (B-001 through B-010)

All sections of this procedure address these gates:

| Gate ID | Tests Covered | Sections |
|---------|---|---|
| **B-001** | All rails/functions at nominal and corner voltages | Sections 2, 3 |
| **B-002** | Idle state: Q2 gate <0.02 V, no spurious brownout pulses | Sections 2, 3 |
| **B-003** | Real gun detection with ACS758 calibration and noise margins | Section 6a |
| **B-004** | Timer delay range, RV2 adjustment, R21 fail-safe | Sections 4d, 7 |
| **B-005** | Thermal, load, trigger latency, Q1/Q2 drive adequacy | Sections 5, 6b |
| **B-006** | PRIME button: 1,000 cycles with delay | Sections 4e, 7 |
| **B-007** | Sensor disconnect: full/VOUT open, J2 pin faults | Section 4f, 6a |
| **B-008** | Environmental: cold/hot, vibration, humidity | Section 6a, 6c, 7 |
| **B-009** | CAD audit: ERC/DRC, BOM/CPL, U1/U2/Q1/Q3/C6/C7/F1 pinouts | Pre-assembly (Section 1) |
| **B-010** | PTC and temperature testing | Section 6b, 7 |

### Manufacturing QA summary

All 50 manufacturing QA checks passed (release run 2026-10-14):
- **Configuration & Integrity:** 2/2 PASS
- **Circuit JSON Validation:** 8/8 PASS
- **Pin & Net Topology:** 6/6 PASS
- **Trace & Route Validation:** 7/7 PASS (including freeze on 56 vias)
- **Board Layout & Clearance:** 6/6 PASS (including U1 footprint and via positioning)
- **Gerber & Excellon Export:** 7/7 PASS (9-file set complete)
- **KiCad PCB File Validation:** 5/5 PASS
- **BOM & CPL Reconciliation:** 4/4 PASS
- **DRC & Audit:** 1/1 PASS (zero violations)
- **U1 Footprint Verification:** 1/1 PASS (TI D0008A exact)

**Disposition:** PASS (50/50 checks, 0 FAIL, 0 PENDING)

---

## Troubleshooting and remediation

### Common failures and recovery

| Symptom | Probable cause | Recovery |
|---|---|---|
| **PUMP_GATE high at idle (>0.65 V)** | U1 open-drain stuck; Q3 or Q2 leakage; R15 pull-down missing | STOP. Do not proceed. Inspect U1 solder, Q2/Q3 orientation, R15 continuity. |
| **No detection response to simulated sensor** | RV1 threshold out of range; R5 or R19 cold joint; U1A output stuck | Check RV1 range at TP6 (should be 2.21–2.80 V span). Verify DET_N continuity to Q1. Reflow U1 pins. |
| **Excessive noise on DET_N** | Inadequate sensor filtering (R1/C5); motor EMI coupling | Confirm R1/C5 values; check C5 for visible cracks. Shield sensor harness away from pump wire. Run Section 6c (100 cycles with scope). |
| **RV2 delay not adjustable** | Trimmer wiper open; R21 discharge open; C7 leakage | Verify RV2 can vary TP10 voltage (connected to VDELAY). Test R21 continuity. Measure C7 capacitance with a capacitance meter (should be 6.8 µF ±10%). |
| **Unexpected brownout resets** | Supervisor threshold too high; supply ripple >100 mVpp; U2 pinout wrong | Measure TP2 ripple in Section 6b. Confirm U2 pinout (pin 1 GND, pin 2 RESET_N, pin 3 VDD). Verify F1 is rated PTC (not a resistor). |
| **Motor current exceeds 1.10 A at 50°C** | Pump drawing excessive current; blocked filter; incorrect pump model | Verify GROTHEN G528 6 V motor is genuine. Check fluid viscosity and back-pressure. Consider blocked filter or high-friction head assembly. |

### Rework checklist

If failures occur during bring-up:

1. **Power off immediately** and allow board to cool
2. **Document the failure** with oscilloscope captures and measured values
3. **Inspect the suspect component(s)** visually under magnification
4. **Reflow suspect solder joints** if cold or insufficient coverage
5. **Measure continuity** of suspected open circuits (remove power first)
6. **Replace** failed or incorrect components (order exact part numbers from ORDER_LEDGER)
7. **Repeat the relevant test section** from this procedure
8. **Do not proceed to field integration** until all bench gates pass

---

## Documentation and sign-off

### Test log template

Record all measurements and pass/fail status for each section:

```
Date: _______________
Tester: _______________
Board S/N: _______________

Section 1 (Unpowered): ☐ PASS  ☐ FAIL
Section 2 (Logic-only): ☐ PASS  ☐ FAIL
Section 3 (Startup/brownout): ☐ PASS  ☐ FAIL
Section 4 (Sensor calibration): ☐ PASS  ☐ FAIL
Section 5 (Dummy load): ☐ PASS  ☐ FAIL
Section 6a (ACS/gun): ☐ PASS  ☐ FAIL
Section 6b (Pump/PTC): ☐ PASS  ☐ FAIL
Section 6c (EMI/motion): ☐ PASS  ☐ FAIL
Section 7 (Final calibration): ☐ PASS  ☐ FAIL

RV1 final setting: ___ (trimmer dial position or voltage @ TP6)
RV2 final setting: ___ (trimmer dial position or delay in ms)

Bench gates passed: ___ / 19 (PWR-000–004, START-002, PTC-001, ENV-001, EMI-001, B-001–B-010)

Signature: _____________________
```

### Field deployment readiness

The board may be integrated into the final wearable pack once:
- All sections of this procedure show **PASS**
- All nine analog-model bench gates (PWR-*, START-002, PTC-001, ENV-001, EMI-001) pass physical measurement
- All 10 supporting bench gates (B-001–B-010) pass
- RV1 and RV2 are calibrated and documented
- Conformal coating (if used) has cured and been retested
- Final enclosure test (Section 7) passes at expected ambient temperature

---

## Related documentation

- **BOM and parts:** `docs/07-pcb/bom-and-parts.md`
- **Fabrication and assembly:** `docs/07-pcb/fabrication-and-assembly.md`
- **Connector pinout:** `docs/07-pcb/connectors-and-pinout.md`
- **Motor harness suppression:** `hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/customer/MOTOR_HARNESS_SUPPRESSION.md`
- **Analog model results:** `hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/verification/analog_model/verification_results.json`
- **Manufacturing QA:** `hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/verification/manufacturing_qa/manufacturing_qa_results.json`
