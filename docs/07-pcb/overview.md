# BubbleLink CTRL v1.2 — board overview

The BubbleLink CTRL v1.2 is an automatic transfer-pump controller for bubble guns, hung under the cap of the printed stick in the backpack, above the battery and power distribution on the sled. It detects when a gun is in use by measuring current through an external Hall-effect sensor (ACS758), and automatically activates a peristaltic pump to feed the bubble reservoir through a distributing manifold. The controller cuts pump power after detection ends, with a calibrated delay to allow the last shot to complete.

## Functional blocks

### Power input and distribution

**J1** receives regulated 5 V from the backpack's buck converter. The input rail is qualified to operate in the range 4.75–5.25 V.

- **Pump rail (+5V_PUMP, TP1):** Feeds the pump MOSFET driver. Ferrite bead **FB1** and bulk capacitor isolate it from the logic rail.
- **Logic/sensor rail (+5V_LOGIC, TP2):** Powered through FB1, supplies U1, U2, and sensor interface. Expected within 50 mV of the pump rail when idle.

### Sensor interface and current detection

**J2** connects the external ACS758 current-sensor module, which outputs a 0–5 V analog signal proportional to gun current. Typical sensitivity is 40 mV per ampere (±50 A range).

| J2 pin | Signal | Source |
|--------|--------|--------|
| 1 | ACS_VCC | Sensor +5 V supply |
| 2 | ACS_GND | Sensor ground |
| 3 | ACS_OUT | Sensor analog output (0–5 V) |

An unplugged sensor (J2 pin 3 open) is pulled low by **R18** (10 kΩ), which defines that condition as no detection.

**R1** and **C5** form a 10 ms low-pass filter on the sensor signal path, attenuating PWM and brush noise from the gun motors (R1/C5, 10 ms). Filtered voltage appears at **TP5** (ACS_FILTER).

### Detection logic and threshold calibration

**U1A** (top half of the dual comparator) receives the filtered sensor signal at its non-inverting input (TP5) and compares it to an adjustable threshold voltage at **TP6** (VTH), set by the **RV1** potentiometer.

- **RV1 range:** approximately 2.21–2.80 V (clockwise = higher threshold)
- **Hysteresis:** approximately 4.42 mV (prevents chatter near the threshold)
- **Detection output (DET_N):** Open-drain, pulled low when ACS_FILTER exceeds VTH

When DET_N asserts (gun detected):

- **LED2** (green GUN LED) lights
- **Q1** (P-channel MOSFET) turns on
- **HOLD** capacitor (TP9) begins charging from the buffered half-supply **VMID** through **R20** (2.2 kΩ)

The PRIME button (**SW1**) also pulls DET_N low directly, exercising the same charge path.

### Buffered reference and gate-charge accumulation

**VMID** (**TP8**) is the buffered midpoint of the 5 V rail, providing a stable ~2.5 V reference for the timing circuit. It settles to 2.40–2.60 V after power-up.

**Q1** charges the **HOLD** node from VMID; this charge accumulates while the gun is active (DET_N low). When the gun stops, DET_N rises and Q1 turns off. The accumulated HOLD voltage then determines how long the pump stays on.

### Timer comparator and pump gate drive

**U1B** (bottom half) compares the HOLD voltage with a threshold voltage **VDELAY** (**TP10**), which is set at approximately 0.98–1.06 V.

- While HOLD > VDELAY, the open-drain output **TIMER_N** (**TP14**) is held low.
- While TIMER_N is low, **Q3** (P-channel) is on, sourcing current through **R14** (100 Ω) to the gate of **Q2** (N-channel pump driver).
- **Q2** gate (**TP11**) is thus pulled high, turning on the pump.

As HOLD slowly discharges through **R9** (10 kΩ) and **RV2** (100 kΩ trimmer), HOLD falls below VDELAY. TIMER_N then rises, Q3 turns off, and Q2 gate falls, stopping the pump.

The delay time is determined by the RC time constant of the discharge path and is adjustable via **RV2**:

- **RV2 range:** clockwise = longer delay
- **Target calibrated delay:** 350 ms ±50 ms (tuned from the delay endpoints ~35–574 ms nominal)
- **Worst-case modeled range:** 23–737 ms (includes component tolerances and rail limits)

**R13** (4.7 MΩ) provides Schmitt feedback from TIMER_N back to VDELAY, ensuring clean threshold crossing. **R21** (1 MΩ) provides a weak fail-safe discharge path so the pump releases even if RV2 opens mechanically (~3.4–7.8 s worst case).

### Pump switching and protection

**Q2** (N-channel MOSFET) switches the pump's negative lead (PUMP_SW_NEG, **TP12**) to ground when Q2 gate is high.

- **Pump rail polarity:** +5V_PUMP on **J3 pin 1** (PUMP+), switched negative on **J3 pin 2** (PUMP_SW_NEG)
- **Steady-state pump current limit:** 0.60 A preferred; 1.10 A hard absolute at 50 °C
- **F1** (1.5 A polyswitch/PPTC resettable fuse) protects the positive branch against overload
- **D1** (Schottky diode, B340A) clamps board-side flyback, with its cathode to PUMP+ and anode to PUMP_SW_NEG
- **C9** (100 nF ceramic) shunts high-frequency motor noise at J3

The pump motor harness also includes a diode and capacitor at the motor itself to suppress noise at the source, preventing false triggering and protecting the MOSFET driver.

### Supervisor and brownout protection

**U2** (TLV803E supervisor, 4.38 V threshold) monitors the logic rail. If +5V_LOGIC falls below 4.38 V (with ~0.9–1.5% hysteresis and 200 ms delay), RESET_N pulls low. During RESET_N assertion, **R23** (560 Ω) allows HOLD to discharge quickly through the supervisor's current sink, ensuring the pump turns off before the logic supply becomes too weak.

| Fault/condition | Outcome |
|---|---|
| U1 unpowered or output open | Q3 off; R15 pulls Q2 gate low; pump off |
| Logic rail < 4.38 V | RESET_N clamps HOLD; pump stops |
| Sensor unplugged (J2 pin 3 open) | R18 pulls ACS_OUT low; detection stops; normal delay then off |
| RV2 wiper opens | R21 provides finite discharge path; pump releases in ~3.4–7.8 s |
| RV1 wiper opens | R19 biases threshold toward high (safe) direction |
| Pump unplugged or stalled | Driver remains unloaded and safe; F1 and circuit limits protect rails |
| Q2 shorts to ground | External 30 A breaker in the main power line remains the system-level shutdown |

**R15** (10 kΩ) pulls Q2 gate low by default, ensuring the pump cannot turn on if the U1B output or Q3 source is absent.

### Status LEDs

| LED | Color | Signal | Meaning |
|-----|-------|--------|---------|
| LED1 | Green (POWER) | +5V_LOGIC via current-limiting resistor | Always on when J1 powered; indicates controller alive |
| LED2 | Yellow (GUN) | DET_N asserted | Gun detected; sensor active and above threshold |
| LED3 | Red (PUMP) | Q2 gate high | Pump actively running |

All LED cathodes connect to ground; anodes are current-limited from the logic rail.

## Board specifications

| Parameter | Value |
|-----------|-------|
| **Dimensions** | 50.0 × 40.0 mm |
| **Thickness** | 1.6 mm FR-4 |
| **Layers** | 2 (signal and ground) |
| **Copper weight** | 1 oz per side |
| **Solder mask** | Green (top and bottom) |
| **Silkscreen legend** | White (top only) |
| **Surface finish** | Lead-free HASL |
| **SMT placements (PCBWay)** | 41 components, top-side only |
| **User-installed (THT)** | 10 components (3 connectors, 1 capacitor, 2 trimmers, 1 switch, 3 LEDs) |
| **Mounting holes (NPTH)** | 4 × M3, 3.2 mm diameter, centers at (±21.5, ±16.5) mm |
| **Test points** | 15 (TP1–TP15), 1.0 mm plated holes with 2.0 mm pads |

## Setting the calibration trimmers

### RV1 (2 kΩ, sensor threshold)

**RV1** controls the current-detection threshold. Set it after measuring the actual gun's idle and active current with the ACS758 module.

1. Power up the controller and confirm the pump is off.
2. Measure the gun's idle-condition voltage at J2 pin 3 (ACS_OUT) using a bench multimeter.
3. Measure the gun's active-condition voltage with the gun running.
4. Calculate the threshold voltage needed: typically midway between idle and active, but with at least 10 mV margin on each side.
5. Adjust RV1 (clockwise = higher threshold) until **TP6** (VTH) reads the target voltage.
6. Verify with the actual gun that detection works reliably and does not chatter.
7. At 0, 25, and 50 °C, require at least 30 mV separation between idle and active, preferably 50 mV.

### RV2 (100 kΩ, pump delay)

**RV2** controls the pump-off delay after detection stops.

1. Set RV2 to a mid-position (approximately half-turn from either end).
2. With the gun running, press the PRIME button to trigger pump start.
3. Release PRIME and measure the time from release until the pump stops.
4. Adjust RV2 clockwise (increases delay) or counterclockwise (decreases delay) toward the target of **350 ms ±50 ms**.
5. Repeat 5–10 times and record the actual delay at each setting. RV2 can reliably calibrate 350 ms even at the worst-case component-tolerance endpoints.
6. Once calibrated, do not adjust RV2 unless the fluid system (pump speed, manifold pressure loss) changes.

## Test points

All test points are 1.0 mm plated holes suitable for oscilloscope probes or a bench multimeter.

| TP | Signal | Nominal/range | Purpose |
|----|--------|----------------|---------|
| TP1 | +5V_PUMP | 4.95–5.05 V (at 5.00 V input) | Pump rail voltage check |
| TP2 | +5V_LOGIC | Within 50 mV of TP1 idle | Logic supply quality |
| TP5 | ACS_FILTER | 0–5 V | Filtered sensor signal (scope) |
| TP6 | VTH (RV1 wiper) | 2.21–2.80 V range | Detection threshold; set by RV1 |
| TP8 | VMID | 2.40–2.60 V | Buffered half-supply reference |
| TP9 | HOLD | <0.10 V idle; ≥0.18 V during pump on | Gate-charge accumulation; timer input |
| TP10 | VDELAY | 0.98–1.06 V | Timer threshold node |
| TP11 | PUMP_GATE (Q2 gate) | <0.05 V idle; ~4.5 V when pump on | Q2 driver signal |
| TP12 | PUMP_SW_NEG | ~0 V when pump on; near +5V_PUMP when off | Pump negative leg (Q2 source) |
| TP14 | TIMER_N (U1B output) | >4.5 V idle; <0.1 V when pump on | Timer comparator output |

TP3, TP4, TP7, TP13, TP15 are reserved for future use or internal test sequencing and are not normally scoped.

## Related documentation

- **Connectors and pinout:** [connectors-and-pinout.md](connectors-and-pinout.md)
- **Revision history:** [revision-history.md](revision-history.md)
- **Bill of materials and parts:** [bom-and-parts.md](bom-and-parts.md)
- **Fabrication and assembly:** [fabrication-and-assembly.md](fabrication-and-assembly.md)
- **Bring-up and acceptance test:** [bringup-and-acceptance-test.md](bringup-and-acceptance-test.md)
- **Electrical power system:** [../04-power-system.md](../04-power-system.md)
