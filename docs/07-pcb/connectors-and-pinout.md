# BubbleLink CTRL v1.2 — connectors and pinout

The BubbleLink CTRL v1.2 has three active connectors (J1, J2, J3) for power input, sensor signal, and pump output, plus an unpopulated J4 AUTO/FORCE-ON input. J1–J3 are JST XH headers (2.50 mm pitch; the purchased kit is listed as "2.54 mm", which is the same XH system), which are standard in small electronics and easy to hand-crimp.

## J1 — 5 V power input (2-pin)

Receives regulated 5 V from the backpack's buck converter. Polarity is critical.

| Pin | Signal | Voltage | Notes |
|-----|--------|---------|-------|
| 1 | +5V | +5.0 V (4.75–5.25 V qualified) | Red; **marked + on housing** |
| 2 | GND | Ground | Black; marked GND on housing |

**Mating connector:** JST B2B-XH-A(LF)(SN) (two-position vertical header)  
**Cable assembly:** Two wires (red for +5V, black for GND) crimped into female contacts from the JST-XH kit and mated into the housing.

**Acceptance:** Before soldering, verify polarity with a multimeter. Reverse polarity will damage the board.

---

## J2 — ACS758 current sensor input (3-pin)

Connects the external Hall-effect current-sensor module. The sensor board must be powered from J2 pin 1; its analog output (typically 2.5 V at zero current) connects to J2 pin 3.

| Pin | Signal | Voltage | Notes |
|-----|--------|---------|-------|
| 1 | ACS_VCC | +5.0 V output from board | Red; power for external sensor module |
| 2 | ACS_GND | Ground | Black; sensor ground return |
| 3 | ACS_OUT | 0–5 V analog signal | Brown or yellow; sensor output to comparator |

**Mating connector:** JST B3B-XH-A(LF)(SN) (three-position vertical header)  
**Cable assembly:** Three wires (red for power, black for ground, brown/yellow for signal) crimped into female contacts from the JST-XH kit and housed as above.

**Sensor details:** The ACS758LCB-050B is a bidirectional Hall-effect sensor rated 50 A (±50 A), with output sensitivity of approximately 40 mV per ampere and a zero-current offset of 2.5 V.

**Unplugged condition:** If J2 pin 3 is not connected, R18 (10 kΩ pull-down) defines the condition as "no detection," and the pump will not run.

---

## J3 — pump motor output (2-pin)

Supplies power and switched negative to the external bubble-transfer pump. The pump sits at a distance of several meters from the controller, connected via the umbilical harness.

| Pin | Signal | Voltage | Notes |
|-----|--------|---------|-------|
| 1 | PUMP+ | +5 V (steady) | Red; motor positive terminal |
| 2 | PUMP_SW_NEG | GND (switched by Q2) | Black; switched motor negative (Q2 source) |

**Mating connector:** JST B2B-XH-A(LF)(SN) (two-position vertical header)  
**Cable assembly:** Two wires (red and black), twisted together, crimped into female contacts from the JST-XH kit and housed.

**Harness suppression at the motor (critical):**

The pump motor is an inductive load and generates flyback transients when switched off. Suppression at the motor terminals is mandatory:

- One 100 nF ceramic capacitor (X7R, ≥25 V) connected directly across the motor tabs (as close as practicable).
- One flyback diode across the motor tabs: cathode to motor positive (PUMP+), anode to motor negative (PUMP_SW_NEG). Use a 2–3 A, 20 V or higher Schottky diode with verified polarity.
- Twisted pair from J3 to the motor to minimize loop area.
- Strain relief on the umbilical harness that does not load J3 connector pins (load transfer to the enclosure or gaff-tape anchor).

Board-side protection (D1, C9) alone is insufficient because cable inductance makes the motor-terminal loop the effective noise source.

---

## J4: AUTO / FORCE-ON input (unpopulated)

**J4** is a 2-pin, 2.50 mm-pitch through-hole position, DNP. PCBWay leaves the holes empty, and it isn't in the THT BOM. It's the no-respin fallback for heads the ACS758 can't detect reliably, such as very low-current or slowed toy heads.

- **J4 open:** normal automatic current sensing.
- **J4 shorted:** the pump is forced on through the normal protected timer/driver path.
- To use it, solder a header or wires to J4 and fit a maintained panel switch labeled `AUTO / FORCE ON`. For fully automatic low-speed operation, give each gun trigger an independent dry-contact pole and wire those contacts in parallel to J4.
- **Never** connect a powered motor lead or a PWM node directly to J4. Use a second trigger pole, an isolated microswitch, a relay contact, or an optocoupler.

---

## Polarity and connector orientation

All three connectors are mounted **vertically** on the top of the PCB, with the opening facing upward (toward the user/enclosure). Pin 1 of each housing is marked with a small **square pad** on the PCB silkscreen, and the plastic connector housing has a **beveled corner or key** indicating pin-1 orientation.

**Before crimping wires:**

1. Identify the pin-1 mark on the JST housing you are using (usually a notch or raised boss on one corner).
2. The square pad on the PCB must align with this pin-1 marker.
3. Red (+5V or PUMP+) wires go to pin 1 of J1 and J3, and pin 1 of J2 (sensor power).
4. Black (GND or switched negative) wires go to pin 2.
5. Brown/yellow (sensor signal) on J2 goes to pin 3.

---

## Wire and connector specifications

| Item | Specification | Qty/board | Source |
|------|---------------|-----------|--------|
| **JST XH headers (male, vertical)** | | | |
| J1, J3 | JST B2B-XH-A(LF)(SN), 2-pin | 2 | User-installed |
| J2 | JST B3B-XH-A(LF)(SN), 3-pin | 1 | User-installed |
| **Harness wire** | | | |
| J1/J2/J3 connections | Silicone-insulated wire (black & red) from JST-XH kit | As needed | Pre-crimped leads supplied in JST-XH kit |
| **Connectors (battery/main power; not on PCB)** | | | |
| Main power in | XT60H (10 pairs) | 1 pair | Backpack main distribution |
| Gun channel power | XT30U (10 pairs) | per gun channel | Distributed to gun amplifier boards |

---

## Test point access

Fifteen test points (TP1–TP15) are 1.0 mm plated holes on the top of the PCB, each with a 2.0 mm solder pad. These are suitable for direct oscilloscope probes or tweezer-tip multimeter leads.

| Test point | Signal | Location/function | Typical probe setup |
|---|---|---|---|
| TP1, TP2 | +5V_PUMP, +5V_LOGIC | Power supply quality | DC voltmeter, 0–6 V range |
| TP5, TP6 | ACS_FILTER, VTH | Sensor threshold check | Oscilloscope 0–5 V, 1 µs/div |
| TP8, TP9, TP10 | VMID, HOLD, VDELAY | Reference and timing nodes | Oscilloscope 0–3 V, 10 ms/div (during calibration) |
| TP11, TP12, TP14 | PUMP_GATE, PUMP_SW_NEG, TIMER_N | Gate drive and motor control | Oscilloscope 0–5 V, 10 µs/div (during pump switching) |

See [overview.md](overview.md#test-points) for detailed signal descriptions and acceptance ranges.

---

## Related documentation

- **Board overview and functional blocks:** [overview.md](overview.md)
- **Through-hole component installation:** [fabrication-and-assembly.md](fabrication-and-assembly.md#user-installed-through-hole-parts)
- **Bring-up and sensor calibration:** [bringup-and-acceptance-test.md](bringup-and-acceptance-test.md)
- **Motor harness suppression (detailed):** ../../hardware/pcb/BubbleLink_CTRL_v1_2_PCBWay/customer/MOTOR_HARNESS_SUPPRESSION.md
