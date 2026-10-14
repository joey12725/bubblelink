# BubbleLink CTRL v1.1 — design description

## Functional chain

1. J1 receives regulated 5 V. The pump rail feeds the pump branch directly; FB1 and local capacitors create a quieter logic/sensor rail.
2. The external ACS758 module reports combined gun current on J2 pin 3. R18 defines an unplugged sensor as off; R1/C5 filter PWM and brush noise.
3. U1A compares the filtered sensor voltage to RV1’s adjustable threshold. Detection pulls `DET_N` low and lights the GUN LED.
4. Low `DET_N` turns on Q1, charging `HOLD` from the buffered half-supply node through R20. PRIME grounds `DET_N` and exercises this same path.
5. U1B compares `HOLD` with `VDELAY`. While HOLD is high, its open-drain `TIMER_N` output is low. Q3 then sources Q2’s gate. R13 supplies true Schmitt feedback to VDELAY.
6. Q2 switches the pump’s negative lead. F1 protects the positive branch, D1 clamps board-side flyback, C9 shunts high-frequency noise, and the motor harness adds suppression directly at the source.
7. After the guns stop, Q1 turns off and C7 discharges through R9/RV2/R21. The pump stops when HOLD crosses the lower timer threshold.
8. R15 makes the MOSFET gate default low. U2 clamps HOLD through startup/brownout. An absent/open U1B output, Q3, or supply therefore does not pull the pump gate high.

## Key nominal values

| Quantity | Nominal |
|---|---:|
| Input rail | 5.0 V; qualified range 4.75–5.25 V |
| VMID | 2.5 V |
| Sensor filter time constant | 10 ms |
| RV1 threshold range | about 2.21–2.80 V |
| Detector hysteresis | about 4.42 mV |
| VDELAY falling/rising threshold | about 1.019 / 1.027 V |
| Calibrated delay target | 350 ms |
| Nominal delay endpoints | about 35–574 ms |
| Q2 gate turnoff RC | about 1 ms |
| Supervisor threshold/delay option | 4.38 V / nominal 200 ms |

The stored Monte Carlo model includes resistor tolerances, effective-capacitance bands, device thresholds/leakage bounds, rail limits, and supervisor limits. Its worst modeled delay range is wider than the nominal values and is reported in `verification/verification_results.json`; RV2 remains able to calibrate 350 ms in all accepted samples.

## Fail-safe behavior

| Fault/state | Intended outcome |
|---|---|
| U1 unpowered, in POR, or output open | Q3 off; R15 pulls Q2 gate low; pump off |
| Logic rail below U2 threshold | RESET_N clamps HOLD below VDELAY; pump turns off |
| Sensor unplugged | R18 pulls ACS_OUT low; detection releases; normal delay then off |
| RV2 wiper opens | Physical end tie plus R21 provide a finite discharge path |
| RV1 wiper opens | R19 biases threshold toward the high/safe direction |
| Pump unplugged | Driver remains unloaded and safe |
| Pump branch overload | F1 heats/trips; upstream buck/current limit and main breaker remain required |
| Q2 fails short | External breaker remains the system-level shutdown; no board can guarantee otherwise |

## Physical architecture

All user-installed and SMT components are on top. Pump power occupies the lower-right region; sensor/filter and comparator occupy the upper-left/center. The bottom layer is primarily routing/ground. Four corner holes and independent harness strain relief support a moving festival-bag environment. Sensitive nets (`ACS_FILTER`, `VTH`, `VMID`, `HOLD`, and `VDELAY`) are kept away from the pump drain and connectors.

