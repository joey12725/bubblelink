# BubbleLink CTRL v1.1 verification suite

This directory verifies the frozen supervised fail-off circuit in
`work/tscircuit/circuit.tsx`.  It deliberately separates:

- **model-passed** — passive-network equations, bounded data-sheet corners,
  deterministic vectors, and Monte Carlo assertions passed;
- **bench-required** — the result depends on the assembled capacitors,
  delivered ACS module, real pump/PTC, supply source, PCB parasitics,
  temperature, or switching noise and cannot honestly be certified in code.

Canonical disposition:

`MODEL_PASS_BENCH_GATES_PENDING`

This is not a production-release waiver.  All rows marked `BENCH_REQUIRED`
in `requirements_traceability.csv` remain release gates.

## Frozen circuit represented

| Function | Frozen implementation |
|---|---|
| Dual comparator | U1 `TLV1822QDRQ1`, open-drain, POR output Hi-Z |
| Timer polarity | U1B `+ = VDELAY`, `- = HOLD`, output `TIMER_N` |
| Timer hysteresis | R13 = 4.7 MΩ, `TIMER_N` to `VDELAY` |
| HOLD charge | Q1 `DMP2065UQ-7`, R20 = 2.2 kΩ |
| VMID storage | C6 `C3225X7R1E226M250AB`, 22 µF, 25 V, X7R |
| Timer storage | C7 `CGA5L1X7R1E685K160AC`, 6.8 µF, 25 V, ±10%, X7R |
| HOLD decay | R9 = 10 kΩ, RV2 = 100 kΩ, R21 = 1 MΩ |
| Supervisor | U2 `TLV803EA43DBZR`, standard DBZ: 1 GND, 2 RESET_N, 3 VDD |
| Supervisor clamp | R23 = 560 Ω, RESET_N to HOLD; C11 = 100 nF on VDD |
| Pump gate source | Q3 `DMP2065UQ-7`, R14 = 100 Ω |
| Pump gate fail-off | R15 = 10 kΩ, C10 = 100 nF |
| Pump protection | F1 `1812L150/16DR` PPTC; D1 `B340A-E3/61T` flyback |

The detector model also includes frozen R19 = 220 kΩ across the RV1
high-to-wiper segment and solves DET_N's released voltage through R4/R5 rather
than assuming an ideal 5 V output.

## Files

| File | Purpose |
|---|---|
| `controller_model.py` | Standard-library detector, timer, two-node startup, supervisor, gate, disconnect, and PTC models |
| `run_verification.py` | Deterministic vector runner and Monte Carlo driver |
| `test_vectors.json` | Machine-readable inputs and acceptance limits |
| `verification_results.json` | Saved compact summary from the canonical run |
| `monte_carlo_results.csv` | Saved 20,000-sample distribution results |
| `requirements_traceability.csv` | Source requirement → frozen implementation → automated/manual gate |

## Run locally

From this directory:

```bash
python3 -B run_verification.py
```

Machine-readable output:

```bash
python3 -B run_verification.py --json
python3 -B run_verification.py --csv
```

Canonical invocation:

```text
python3 -B run_verification.py --samples 20000 --seed 20260807
```

The suite requires Python 3.10 or newer and no third-party packages.  A fixed
seed and sample count reproduce the same result.  Exit code zero means only
that the analytic assertions and Monte Carlo bounds passed.

## Canonical results

All 20,000 deterministic Monte Carlo samples passed all 12 encoded model
assertion groups.  No bench-only item is reported as `PASS`.

| Metric | Minimum | Median | Maximum |
|---|---:|---:|---:|
| Detector hysteresis | 4.010 mV | 4.387 mV | 4.764 mV |
| Timer true hysteresis | 7.491 mV | 8.207 mV | 8.930 mV |
| Minimum-delay endpoint | 23.002 ms | 34.100 ms | 45.949 ms |
| Maximum-delay endpoint | 378.364 ms | 555.233 ms | 736.645 ms |
| RV2 fraction for 350 ms | 0.420 | 0.584 | 0.913 |
| Q1 startup latency | 6.146 ms | 9.488 ms | 14.615 ms |
| Q1 required current | 162.439 µA | 173.079 µA | 184.552 µA |
| Q1 `VGS` overdrive above 0.9 V | 0.830 V | 1.058 V | 1.291 V |
| Q2 gate from bounded Q3 leakage | 0.00000015 V | 0.005034 V | 0.010085 V |
| R21-only fail-safe release | 3.351 s | 5.325 s | 7.831 s |
| U2 asserted-clamp timer margin | 0.168 V | 0.182 V | 0.196 V |
| U2 initial brownout sink current | 3.984 mA | 4.266 mA | 4.552 mA |
| Modeled brownout-to-Q2-off time | 4.941 ms | 6.518 ms | 8.207 ms |
| Minimum startup release supply | 4.345 V | 4.453 V | 4.560 V |
| U2 delay beyond U1 POR | 129.801 ms | 200.394 ms | 269.800 ms |
| Q2 gate decay to 0.65 V | 1.777 ms | 2.037 ms | 2.314 ms |

Nominal or explicit-corner vectors produced:

- detector turn-on span 2.2118–2.7969 V at 5.0 V;
- detector hysteresis 4.4209 mV;
- 0.5 A step with 10 mV margin: 6.931 ms detector latency;
- timer thresholds: 1.0271 V rising and 1.0189 V falling;
- nominal timer delay range: 34.967–573.808 ms;
- 350 ms at RV2 fraction 0.56424;
- R9/RV2 open: R21 releases in 5.990 s nominal;
- explicit startup passive corner: 14.247 ms to cross the timer threshold;
- explicit brownout corner: 4.5277 mA initial U2 sink and 7.968 ms
  until the Q2 gate crosses 0.65 V;
- complete/VOUT sensor disconnect: modeled pump-off in 608.7 ms at
  maximum nominal delay;
- `1812L150/16DR` data-sheet hold current: 1.10 A at 50 °C.

The worst Monte Carlo U2 current is 4.552 mA, retaining about 0.448 mA of
headroom below the 5 mA recommended-current limit even though the current
check deliberately assumes RESET_N instantaneously reaches 0 V.  The
separate timing check uses the bounded 0.30 V low level.  `PWR-003` remains an
essential bench gate because actual shallow-brownout propagation and PCB
waveforms are not captured by this passive model.

## Bounded-random model assumptions

Every sample independently randomizes:

- supply from 4.75 to 5.25 V;
- modeled resistors uniformly over ±1%;
- C5 effective value over ±20%;
- C6 effective value from 13.5 to 30.4 µF;
- C7 effective value from 4.68 to 8.60 µF;
- C7 insulation resistance from 73 to 500 MΩ;
- each TLV1822 input offset over ±4 mV;
- each TLV1822 output-low voltage from 0.02 to 0.25 V;
- TLV803 falling threshold at 4.38 V ±2%;
- TLV803 hysteresis from 0.9% to 1.5%;
- TLV803 release delay from 130 to 270 ms;
- TLV803 assertion delay from 0 to 50 µs;
- TLV803 reset-low level from 0 to 0.30 V and released leakage from 0 to
  350 nA;
- ACS sensitivity from 39.4 to 41.0 mV/A;
- Q3 off leakage from 0 to 1 µA;
- C10 over ±10%.

C6 and C7 ranges are engineering envelopes combining nominal tolerance,
temperature behavior, and a conservative allowance for DC bias.  They are
not manufacturer-guaranteed probability distributions.  Measure effective
capacitance on the assembled board at its operating bias before relying on a
trim setting.

Uniform sampling is a reproducible corner exercise, not a claim about actual
manufacturing statistics or field failure probability.

## Supervisor analysis

### Low-voltage startup phases

1. Below the TLV803 controlled-output limit of 0.7 V, its RESET_N state is
   undefined.  The TLV1822 open-drain POR output is Hi-Z, R12 pulls TIMER_N to
   the local rail, Q3 has approximately zero `VGS`, and R15 holds Q2 off.
2. From 0.7 V upward, TLV803 RESET_N is controlled low while the supply is
   below its threshold.
3. TLV1822 is guaranteed over its 2.4–40 V supply range and keeps its
   open-drain output Hi-Z during POR for up to 200 µs.
4. TLV803 does not release until the supply exceeds its rising threshold and
   remains there for 130–270 ms.  Thus its minimum delay exceeds the U1 POR
   bound by 129.8 ms.

The explicit worst-threshold 0.1 V/s ramp releases at 4.344 V; faster ramps
reach the 4.75 V final rail before or during the delay.  This proves the
nominal timing relationship, not the absence of a real-board pulse.

### Asserted HOLD clamp

The code solves Q1-on HOLD equilibrium through the VMID Thevenin resistance,
R20, the timer discharge network, R23, and a 0.30 V RESET_N low.  Both RV2
endpoints are swept at 0.25 V supply increments from 3.0 to 5.25 V.  The
explicit worst vector retains 180.3 mV below the active timer threshold; the
20,000-sample minimum is 168.1 mV.

### Brownout

Brownout is split into two conservative calculations:

- instantaneous current uses charged HOLD and RESET_N = 0 V;
- shutdown time uses RESET_N = 0.30 V, maximum C7/C10 vectors, 50 µs U2
  assertion delay, TLV1822 propagation, and R15/C10 gate decay.

This model does not cover an arbitrarily shallow or noisy rail crossing, the
source impedance of the buck converter, or PCB inductance.  Test those cases
with an oscilloscope.

## Bench release gates

Record board serial number, ambient temperature, supply/current limit,
instrument models, raw captures, and signed pass/fail disposition for every
gate.

### B-001 — rails and references

1. Test 4.75, 5.00, and 5.25 V at J1 with a current-limited supply.
2. Record +5V_PUMP, +5V_LOGIC, VMID, VDELAY thresholds, RV1 endpoints, and
   idle current.
3. Pass if every automatic and PRIME operation works at all three voltages,
   no part heats unexpectedly, and references remain within the encoded
   bounds.

### B-002 / PWR-000…PWR-004 — startup and brownout

1. Scope +5V_LOGIC, RESET_N, HOLD, VDELAY, TIMER_N, PUMP_GATE, and
   PUMP_SW_NEG simultaneously or in correlated captures.
2. Test hard plug and 0.1/1/10/100 V/s ramps.  Repeat at least 100 times each
   with sensor idle and pump connected.
3. Sweep downward through the U2 threshold slowly and with steps.  Add
   0.1/1/10/100 ms interruptions and shallow dips above, at, and below the
   threshold.
4. Exercise both idle and active-HOLD states.  Derive U2 current as
   `(HOLD - RESET_N) / measured R23` during assertion.
5. Pass only if there is zero unintended pump motion at idle, asserted HOLD
   remains at least 100 mV below the active VDELAY threshold, derived U2
   current never exceeds 5 mA, and PUMP_GATE crosses below 0.65 V within
   15 ms after a qualified brownout.
6. Capture the sub-0.7 V interval; do not replace the observation with a
   statement that U2 is guaranteed there.

### B-003 / ENV-001 — actual ACS window

1. Warm the actual ACS module for one minute.  Record zero-current output,
   RMS noise, peak-to-peak noise, polarity, and sensitivity at 0/25/50 °C and
   4.75/5.25 V.
2. Record minimum steady and PWM current profiles for every intended gun
   mode over the same matrix.
3. Choose one fixed RV1 setting.
4. Pass only if the threshold is at least `15 mV + 3 × filtered RMS noise`
   above maximum idle and equally below minimum active output everywhere.

### B-004 — C6/C7 and timer acceptance

1. Measure effective C6 and C7 in circuit or characterize identical parts at
   their operating DC bias and 0/25/50 °C.
2. Measure RV2 endpoint delays for 100 cycles at 4.75/5.00/5.25 V and
   0/25/50 °C.
3. Set 350 ms and record 100 cycles; verify clockwise means longer.
4. On a development board, open the adjustable branch and verify R21 always
   releases within 10 s.
5. Pass if 350 ms ±25 ms is reachable, jitter is below 5 ms, and every
   release terminates.

### B-005 / START-002 — Q1, Q2, and load thermal

1. At 4.75 V and 0 °C with RV2 minimum, verify every qualified detection
   crosses the rising HOLD threshold.
2. Test Q2 and pump copper at 0.3 A for 60 minutes, 1.0 A for 30 minutes,
   1.5 A for 10 minutes, and measured startup-current pulses.  This is a
   board/driver test; bypass or separately account for F1 if needed.
3. Pass if Q1 always starts, Q2 `VDS(on)` stays below 100 mV at 1.5 A, and no
   board or connector part rises more than 20 °C above ambient.

### B-006 — PRIME and sequencing

Run 1,000 press/release and rapid gun-trigger sequences, including switch
bounce, 5/10/20/50 ms pulses, overlapping triggers, and both gun channels.
There must be no missed qualified command, timer double edge, or abnormal
delay after PRIME release.

### B-007 — disconnect and recovery

Test complete J2 disconnect, individual VCC/GND/VOUT opens, and current-
limited VOUT shorts to ground and +5 V.  Full/VOUT disconnect must command
off within 1 s.  Ground-open behavior must be recorded, not claimed fail-off
without evidence.

### EMI-001 — pump inductive and brush switching

Use the production pump and harness for 10,000 starts/stops across supply
extremes, long harness routing, stall-current pulses, and rapid triggers.
Scope Q2 drain, logic rail, ACS_FILTER, VTH, HOLD, VDELAY, RESET_N, TIMER_N,
and PUMP_GATE.  Pass only if drain stays below 12 V, logic ripple below
50 mV peak-to-peak, and there are zero false transitions.

### B-008 — physical environment

Run cold/hot operation, one-hour powered vibration/wear simulation,
connector tugging, post-cleaning humidity exposure, and conformal-coating
recheck.  No moisture-related state change, intermittent connection, or
calibration movement is acceptable.

### B-009 — CAD and manufacturing release

Independently verify ERC/DRC, connector pin order, Bourns 3296W physical
1-3-2 lead order, exact U1/U2/Q1/Q2/Q3/D1 pad mapping, U2 standard DBZ
orientation, C6/C7/F1 production MPNs, copper widths, test-point access,
BOM/CPL rotations, Gerber layers, drill files, and NPTH status.

### B-010 / PTC-001 — production-pump PTC acceptance

1. Measure continuous pump current at 4.75 and 5.25 V, 0/25/40/50 °C, with
   normal fluid flow and the worst credible restricted-flow condition.
2. Measure startup/stall pulses and F1 surface temperature.
3. The production pump must remain below 1.10 A continuously at 50 °C and
   must not nuisance-trip during any valid startup sequence.
4. If it does not pass, select a higher-temperature hold-current PTC; the
   `1.5 A` marking is a 20 °C rating and is not a 50 °C guarantee.

## Data-sheet facts encoded

- TI TLV181x-Q1/TLV182x-Q1 data sheet: 2.4 V minimum operating supply,
  ±4 mV full-temperature input offset, 250 mV maximum VOL at 4 mA,
  open-drain POR Hi-Z, and up to 200 µs POR time.
- TI TLV803E data sheet: A43 = 4.38 V falling threshold, ±2% accuracy,
  0.9–1.5% hysteresis, A delay = 130/200/270 ms, controlled reset down to
  0.7 V, 0.30 V VOL test limits, 350 nA open-drain leakage, and ±5 mA
  recommended RESET current.
- TDK C3225 page: 22 µF ±20%, 25 V, X7R, 22 MΩ minimum insulation.
- TDK CGA5 page: 6.8 µF ±10%, 25 V, X7R, 73 MΩ minimum insulation.
- Littelfuse 1812L series data sheet: `1812L150/16` hold current 1.68/1.50/
  1.25/1.10 A at 0/20/40/50 °C, 2.8 A trip current at 20 °C, and 0.11 Ω
  maximum post-reflow resistance.

Official source pages:

- <https://www.ti.com/lit/ds/symlink/tlv1812-q1.pdf>
- <https://www.ti.com/lit/ds/symlink/tlv803e.pdf>
- <https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3225X7R1E226M250AB>
- <https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CGA5L1X7R1E685K160AC>
- <https://www.littelfuse.com/assetdocs/resettable-ptcs-1812l-datasheet>

## Model boundary

The suite does not invent values for the actual ACS module, G528 winding
resistance/inductance and brush spectrum, supply-source startup/current
limiting, PCB contamination/parasitics, connector heating, PPTC enclosure
temperature, or assembly defects.  Those omissions are exactly why the
bench gates remain mandatory after a clean model run.
