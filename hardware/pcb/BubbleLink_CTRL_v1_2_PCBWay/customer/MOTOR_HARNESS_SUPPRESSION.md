# Pump harness and motor suppression

Board D1 and C9 protect the controller end of the cable. They do not replace suppression at a brushed motor because cable inductance makes the motor-terminal loop the effective noise source.

## Required motor-end parts

- One 100 nF ceramic capacitor, at least 25 V, X7R or C0G, connected directly across the motor tabs with leads kept as short as practicable.
- One flyback diode across the motor tabs, cathode to motor positive and anode to motor negative. Use a 2–3 A, 20 V or higher Schottky part with verified polarity. If motor reversal is ever introduced, this diode arrangement must be redesigned; the present system is one-direction only.
- Twisted positive/negative pump pair from J3 to the motor.
- Strain relief that transfers pull force to the enclosure, not J3 or the motor tabs.

## Harness pinout

| J3 pin | Label | Connects to |
|---:|---|---|
| 1 | PUMP+ | Motor positive; diode cathode |
| 2 | PUMP_SW_NEG | Motor negative; diode anode |

## Inspection and acceptance

1. Power off and verify diode polarity with a meter before connecting the motor.
2. Confirm no short exists across J3.
3. Start on a current-limited 5 V supply.
4. Scope J3 pin 2, +5V_LOGIC, DET_N, and RESET_N during at least 100 rapid cycles.
5. Reject any build showing false detection, rail reset, unexpected pump pulses, or excessive diode/MOSFET temperature.

Never place a fluid joint above the controller. Keep pump wiring physically separated from J2 and the ACS signal harness.

