# BubbleLink CTRL v1.1 — bring-up and acceptance test

Use an oscilloscope where requested. Record actual values; do not mark a measurement PASS from visual behavior alone.

## 1. Unpowered inspection

- Confirm board revision, dimensions, and four 3.2 mm NPTH holes.
- Inspect U1/U2 pin 1, Q1/Q2/Q3 orientation, D1 cathode at PUMP+, F1, C1 polarity, LED cathodes, and JST pin-1 marks.
- Confirm RV1=`3296W-1-202LF`, RV2=`3296W-1-104LF`; their physical lead order is 1–3–2.
- Confirm J4 and R22 are unpopulated; C9 and R18 are populated.
- Measure J1 pin 1 to GND for a short. Verify J3 pin 2 is not shorted to GND unpowered.

## 2. Logic-only bring-up

Leave J2 and J3 disconnected. Set a 5.00 V bench supply to a 100 mA current limit and power J1.

| Check | Acceptance |
|---|---|
| Supply current | No current limiting, heating, or odor; record value |
| TP1 +5V_PUMP | 4.95–5.05 V at a 5.00 V input |
| TP2 +5V_LOGIC | Within 50 mV of TP1 with no external sensor |
| TP8 VMID | 2.40–2.60 V after settling |
| TP10 VDELAY | 0.98–1.06 V |
| TP9 HOLD after supervisor release | <0.10 V idle |
| TP14 TIMER_N idle | >4.5 V |
| TP11 PUMP_GATE idle | <0.05 V |
| LEDs | POWER on; GUN and PUMP off |

Stop immediately if PUMP_GATE is high at idle.

## 3. Controlled startup/brownout gate

Monitor TP2, U2 RESET_N side of R23, TP9, TP14, and TP11.

- Hard-connect and disconnect 5 V ten times.
- Ramp 0→5 V and 5→0 V at 0.1, 1, 10, and 100 V/s.
- Apply dips through roughly 4.2–4.6 V with 1 ms, 10 ms, 100 ms, and 1 s dwell.

Acceptance: no pump-gate pulse above 0.65 V while supply is invalid; after RESET_N asserts, TP11 falls below 0.20 V within 15 ms. Record the worst waveform.

## 4. Simulated sensor calibration

Drive J2 pin 3 from a ground-referenced 0–5 V source through 1 kΩ.

1. Verify RV1 spans approximately 2.20–2.80 V at TP6 and clockwise raises the threshold.
2. Increase ACS_OUT slowly and record TP5/TP6 at DET_N assertion.
3. Decrease slowly and record release. Expect only a few millivolts hysteresis.
4. Step the source from idle to at least 20 mV above threshold. Confirm DET_N assertion and Q2-gate rise within 25 ms.
5. Remove the step and sweep RV2. Confirm clockwise increases delay and the target 350 ms is reachable.
6. Hold PRIME. Confirm GUN and PUMP commands assert through the same path. Release it and confirm timed shutdown.
7. Disconnect J2. Pump must release after the normal maximum calibrated delay.

## 5. Dummy-load output test

Use a 5 V, 100–300 mA resistive load at J3. Raise supply current limit appropriately.

- Verify J3 polarity before connection.
- Trigger with PRIME and simulated ACS.
- Confirm TP12 falls close to ground when on and TP11 remains about the logic rail.
- Confirm no material movement on TP2, TP5, or TP6 as the load switches.

## 6. External-hardware release tests

### ACS/gun

At stabilized 0, 25, and 50 °C, record maximum idle/noise voltage and minimum active voltage for the weakest intended gun mode. Require ≥30 mV separation, preferably ≥50 mV. Set RV1 so at least 10 mV remains on each side. Run ten starts and releases at each temperature with no misses or chatter.

### Pump/buck/PTC

- Fit the motor-end diode/capacitor and twisted pair first.
- Measure steady, startup, and brief mechanically constrained current without sustaining a stall.
- At 50 °C enclosure-equivalent ambient, require steady pump current <1.10 A; preferred <0.60 A.
- Require TP1/TP2 within 4.75–5.25 V during startup and operation.
- Run 10 minutes; reject connector, F1, Q2, D1, or copper temperature rise >20 °C above ambient.

### EMI and motion

Cycle the actual pump 100 times while scoping TP2, TP5, DET_N, RESET_N, and TP11. Shake the assembled bag and flex only the strain-relieved harness sections. Require no false starts, missed starts, resets, or intermittent connections.

## 7. Final calibration and field acceptance

- Set RV1 from measured data, never by guessed trimmer turns.
- Set RV2 to 350 ms ±50 ms unless the fluid system requires another qualified value.
- Confirm one gun, either channel, both together, rapid trigger taps, PRIME, sensor unplug, pump unplug, hard power cycle, and breaker shutdown.
- Apply conformal coating only after calibration; mask connectors, RV1/RV2, switch, LED optics, and test points needed for service.
- Retest after the enclosure is closed and at its worst expected temperature.

