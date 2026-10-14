"""Analytic models for the frozen BubbleLink CTRL v1.1 circuit.

The model uses only the Python standard library.  It solves the passive
networks exactly and uses first-order or exact two-node RC equations.  It is
not a transistor-level SPICE model and does not turn bench-only properties
into simulated passes.

Frozen safety/timer topology represented here:

* U1 is TLV1822QDRQ1, an open-drain dual comparator with high-impedance POR.
* U1B non-inverting input is VDELAY and inverting input is HOLD.
* R13 = 4.7 Mohm from TIMER_N to VDELAY creates true hysteresis.
* Q1 and Q3 are DMP2065UQ-7; Q1 charges HOLD through R20 = 2.2 kohm.
* R9 = 10 kohm, RV2 = 100 kohm, R21 = 1 Mohm, C7 = 6.8 uF nominal.
* U2 is TLV803EA43DBZR, standard DBZ pinout (1 GND, 2 RESET_N,
  3 VDD), clamping HOLD through R23 = 560 ohm during reset.
* Q2 gate defaults off through R15 = 10 kohm and C10 = 100 nF.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
from typing import Dict, Iterable, Sequence, Tuple


@dataclass(frozen=True)
class ControllerParameters:
    # Supply and ACS current detector.
    vcc: float = 5.0
    r1: float = 10_000.0
    c5: float = 1.0e-6
    r18: float = 100_000.0
    r2: float = 7_500.0
    r3: float = 7_500.0
    rv1: float = 2_000.0
    r19: float = 220_000.0
    r4: float = 10_000.0
    r5: float = 4_700_000.0
    detector_vol: float = 0.10
    detector_vos: float = 0.0
    sensor_sensitivity: float = 0.040

    # VMID and Q1 HOLD charge path.
    r7: float = 4_700.0
    r8: float = 4_700.0
    c6_effective: float = 22.0e-6
    r20: float = 2_200.0
    q1_on_resistance: float = 0.15

    # Timer and true hysteresis.
    r9: float = 10_000.0
    rv2: float = 100_000.0
    r21: float = 1_000_000.0
    c7_effective: float = 6.8e-6
    c7_insulation_resistance: float = 73_000_000.0
    r10: float = 39_000.0
    r11: float = 10_000.0
    r12: float = 10_000.0
    r13: float = 4_700_000.0
    timer_vol: float = 0.10
    timer_vos: float = 0.0

    # TLV803EA43 supervisor and TLV1822 POR bounds.
    r23: float = 560.0
    supervisor_falling_threshold: float = 4.38
    supervisor_hysteresis_fraction: float = 0.012
    supervisor_release_delay: float = 0.200
    supervisor_assert_delay: float = 30.0e-6
    supervisor_vol: float = 0.10
    supervisor_off_leakage: float = 0.0
    supervisor_por_voltage: float = 0.70
    supervisor_recommended_current: float = 5.0e-3
    supervisor_absolute_current: float = 20.0e-3
    comparator_min_supply: float = 2.4
    comparator_por_delay: float = 200.0e-6
    comparator_propagation_delay: float = 0.9e-6

    # Fail-off pump-gate network.
    r14: float = 100.0
    r15: float = 10_000.0
    c10: float = 100.0e-9
    q3_on_resistance: float = 0.15
    q3_off_leakage: float = 1.0e-6
    q2_vgs_threshold_min: float = 0.65

    # Pump branch protection: 1812L150/16DR datasheet anchors.
    ptc_hold_0c: float = 1.68
    ptc_hold_20c: float = 1.50
    ptc_hold_40c: float = 1.25
    ptc_hold_50c: float = 1.10
    ptc_trip_20c: float = 2.80
    ptc_resistance_typ: float = 0.040
    ptc_resistance_post_reflow_max: float = 0.110


def parallel(*resistances: float) -> float:
    """Return the parallel combination of positive finite resistances."""
    conductance = 0.0
    for resistance in resistances:
        if resistance <= 0.0:
            raise ValueError("resistance must be positive")
        conductance += 1.0 / resistance
    return 1.0 / conductance


def _solve_linear(matrix: Iterable[Iterable[float]], rhs: Iterable[float]) -> Tuple[float, ...]:
    """Small Gaussian-elimination solver with partial pivoting."""
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(a)
    if n == 0 or any(len(row) != n + 1 for row in a):
        raise ValueError("matrix must be square")
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(a[row][column]))
        if abs(a[pivot][column]) < 1.0e-30:
            raise ValueError("singular matrix")
        a[column], a[pivot] = a[pivot], a[column]
        scale = a[column][column]
        a[column] = [value / scale for value in a[column]]
        for row in range(n):
            if row == column:
                continue
            factor = a[row][column]
            if factor == 0.0:
                continue
            a[row] = [left - factor * right for left, right in zip(a[row], a[column])]
    return tuple(a[row][-1] for row in range(n))


def _pot_segments(total: float, position: float) -> Tuple[float, float]:
    if not 0.0 <= position <= 1.0:
        raise ValueError("pot position must be between zero and one")
    tiny = 1.0e-9
    return max((1.0 - position) * total, tiny), max(position * total, tiny)


def _detector_vth_low(params: ControllerParameters, pot_position: float, det_voltage: float) -> float:
    """VTH with DET_N actively low, including R19 and R5."""
    r_top, r_bottom = _pot_segments(params.rv1, pot_position)
    g2 = 1.0 / params.r2
    g3 = 1.0 / params.r3
    gt = 1.0 / r_top + 1.0 / params.r19
    gb = 1.0 / r_bottom
    gf = 1.0 / params.r5
    matrix = (
        (g2 + gt, -gt, 0.0),
        (-gt, gt + gb + gf, -gb),
        (0.0, -gb, gb + g3),
    )
    rhs = (params.vcc * g2, det_voltage * gf, 0.0)
    _, vth, _ = _solve_linear(matrix, rhs)
    return vth


def _detector_vth_high(params: ControllerParameters, pot_position: float) -> Tuple[float, float]:
    """VTH and DET_N with the open-drain output released."""
    r_top, r_bottom = _pot_segments(params.rv1, pot_position)
    g2 = 1.0 / params.r2
    g3 = 1.0 / params.r3
    gt = 1.0 / r_top + 1.0 / params.r19
    gb = 1.0 / r_bottom
    gf = 1.0 / params.r5
    g4 = 1.0 / params.r4
    matrix = (
        (g2 + gt, -gt, 0.0, 0.0),
        (-gt, gt + gb + gf, -gb, -gf),
        (0.0, -gb, gb + g3, 0.0),
        (0.0, -gf, 0.0, gf + g4),
    )
    rhs = (params.vcc * g2, 0.0, 0.0, params.vcc * g4)
    _, vth, _, det = _solve_linear(matrix, rhs)
    return vth, det


def detector_thresholds(params: ControllerParameters, pot_position: float) -> Dict[str, float]:
    """Return U1A turn-on/release thresholds and external hysteresis."""
    turn_on, det_high = _detector_vth_high(params, pot_position)
    release = _detector_vth_low(params, pot_position, params.detector_vol)
    turn_on += params.detector_vos
    release += params.detector_vos
    return {
        "det_high_v": det_high,
        "turn_on_v": turn_on,
        "release_v": release,
        "hysteresis_v": turn_on - release,
    }


def detector_step_latency(initial_v: float, final_v: float, threshold_v: float, tau_s: float) -> float:
    """First-order rising or falling threshold-crossing time."""
    if tau_s <= 0.0:
        raise ValueError("tau_s must be positive")
    if final_v > initial_v:
        if threshold_v <= initial_v:
            return 0.0
        if threshold_v >= final_v:
            return math.inf
    elif final_v < initial_v:
        if threshold_v >= initial_v:
            return 0.0
        if threshold_v <= final_v:
            return math.inf
    else:
        return 0.0 if threshold_v == initial_v else math.inf
    ratio = (threshold_v - final_v) / (initial_v - final_v)
    return -tau_s * math.log(ratio)


def sensor_step_latency(params: ControllerParameters, current_a: float, margin_v: float) -> float:
    idle = 0.5 * params.vcc
    final = idle + params.sensor_sensitivity * current_a
    return detector_step_latency(idle, final, idle + margin_v, params.r1 * params.c5)


def pwm_filter_steady_state(
    params: ControllerParameters,
    peak_current_a: float,
    frequency_hz: float,
    duty_cycle: float,
) -> Dict[str, float]:
    """Steady-state C5 extrema for a rectangular current-PWM profile."""
    if frequency_hz <= 0.0:
        raise ValueError("frequency_hz must be positive")
    if not 0.0 < duty_cycle < 1.0:
        raise ValueError("duty cycle must be strictly between zero and one")
    amplitude = params.sensor_sensitivity * peak_current_a
    period = 1.0 / frequency_hz
    tau = params.r1 * params.c5
    on_decay = math.exp(-duty_cycle * period / tau)
    off_decay = math.exp(-(1.0 - duty_cycle) * period / tau)
    low = amplitude * off_decay * (1.0 - on_decay) / (1.0 - on_decay * off_decay)
    high = amplitude + (low - amplitude) * on_decay
    return {
        "low_increment_v": low,
        "high_increment_v": high,
        "average_increment_v": amplitude * duty_cycle,
    }


def vmid_thevenin(params: ControllerParameters) -> Tuple[float, float]:
    return params.vcc * params.r8 / (params.r7 + params.r8), parallel(params.r7, params.r8)


def q1_charge_resistance(params: ControllerParameters) -> float:
    return params.r20 + params.q1_on_resistance


def timer_discharge_resistance(params: ControllerParameters, delay_position: float) -> float:
    if not 0.0 <= delay_position <= 1.0:
        raise ValueError("delay position must be between zero and one")
    return parallel(params.r9 + params.rv2 * delay_position, params.r21)


def timer_total_decay_resistance(params: ControllerParameters, delay_position: float) -> float:
    return parallel(
        timer_discharge_resistance(params, delay_position),
        params.c7_insulation_resistance,
    )


def timer_thresholds(params: ControllerParameters) -> Dict[str, float]:
    """Solve VDELAY for TIMER_N released and actively low states."""
    g12 = 1.0 / params.r12
    g13 = 1.0 / params.r13
    g10 = 1.0 / params.r10
    g11 = 1.0 / params.r11
    matrix = (
        (g12 + g13, -g13),
        (-g13, g10 + g11 + g13),
    )
    rhs = (params.vcc * g12, params.vcc * g10)
    timer_high, vdelay_off = _solve_linear(matrix, rhs)
    vdelay_on = (params.vcc * g10 + params.timer_vol * g13) / (g10 + g11 + g13)
    return {
        "timer_high_v": timer_high,
        "timer_low_v": params.timer_vol,
        "rising_hold_threshold_v": vdelay_off + params.timer_vos,
        "falling_hold_threshold_v": vdelay_on + params.timer_vos,
        "hysteresis_v": vdelay_off - vdelay_on,
    }


def active_hold_voltage(params: ControllerParameters, delay_position: float) -> float:
    """Steady HOLD while Q1 is on and U2 RESET_N is released."""
    vmid, rmid = vmid_thevenin(params)
    source_r = rmid + q1_charge_resistance(params)
    decay_r = timer_total_decay_resistance(params, delay_position)
    numerator = vmid / source_r - params.supervisor_off_leakage
    return max(0.0, numerator / (1.0 / source_r + 1.0 / decay_r))


def timer_delay(params: ControllerParameters, delay_position: float) -> float:
    """Off-delay after Q1 opens, including C7 leakage and U2 off leakage."""
    hold_start = active_hold_voltage(params, delay_position)
    threshold = timer_thresholds(params)["falling_hold_threshold_v"]
    decay_r = timer_total_decay_resistance(params, delay_position)
    leakage_shift = params.supervisor_off_leakage * decay_r
    if hold_start <= threshold or threshold + leakage_shift <= 0.0:
        return math.inf
    return decay_r * params.c7_effective * math.log(
        (hold_start + leakage_shift) / (threshold + leakage_shift)
    )


def timer_delay_with_adjustable_branch_open(params: ControllerParameters) -> float:
    """Fail-safe delay with R9/RV2 open; R21 still guarantees decay."""
    vmid, rmid = vmid_thevenin(params)
    source_r = rmid + q1_charge_resistance(params)
    decay_r = parallel(params.r21, params.c7_insulation_resistance)
    hold_start = max(
        0.0,
        (vmid / source_r - params.supervisor_off_leakage)
        / (1.0 / source_r + 1.0 / decay_r),
    )
    threshold = timer_thresholds(params)["falling_hold_threshold_v"]
    shift = params.supervisor_off_leakage * decay_r
    if hold_start <= threshold:
        return math.inf
    return decay_r * params.c7_effective * math.log((hold_start + shift) / (threshold + shift))


def solve_delay_position(params: ControllerParameters, target_s: float) -> Tuple[float, float]:
    low_delay = timer_delay(params, 0.0)
    high_delay = timer_delay(params, 1.0)
    if not low_delay <= target_s <= high_delay:
        return math.nan, math.nan
    lo = 0.0
    hi = 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if timer_delay(params, mid) < target_s:
            lo = mid
        else:
            hi = mid
    position = 0.5 * (lo + hi)
    return position, timer_delay(params, position)


def _two_node_hold_coefficients(
    params: ControllerParameters,
    delay_position: float,
) -> Tuple[float, float, float, float, float]:
    """Return Hinf, lambda1, lambda2, exp coefficients a and b.

    Initial conditions are VMID at its unloaded divider value and HOLD = 0.
    The exact response is H(t) = Hinf + a*exp(lambda1*t) +
    b*exp(lambda2*t).  Supervisor off leakage is omitted during the first
    millivolts of startup because its direction at RESET_N = 0 V is not
    specified; it remains included in the steady timer bounds.
    """
    vmid, rmid = vmid_thevenin(params)
    charge_r = q1_charge_resistance(params)
    decay_r = timer_total_decay_resistance(params, delay_position)
    c6 = params.c6_effective
    c7 = params.c7_effective

    a11 = -(1.0 / rmid + 1.0 / charge_r) / c6
    a12 = (1.0 / charge_r) / c6
    a21 = (1.0 / charge_r) / c7
    a22 = -(1.0 / charge_r + 1.0 / decay_r) / c7
    trace = a11 + a22
    discriminant = math.sqrt((a11 - a22) ** 2 + 4.0 * a12 * a21)
    lambda1 = 0.5 * (trace + discriminant)
    lambda2 = 0.5 * (trace - discriminant)

    source_r = rmid + charge_r
    h_inf = vmid * decay_r / (source_r + decay_r)
    dh0 = vmid / (charge_r * c7)
    total = -h_inf
    a = (dh0 - lambda2 * total) / (lambda1 - lambda2)
    b = total - a
    return h_inf, lambda1, lambda2, a, b


def q1_start_latency(params: ControllerParameters, delay_position: float) -> Dict[str, float]:
    """Exact two-node VMID/C6-to-HOLD/C7 charge latency through R20."""
    threshold = timer_thresholds(params)["rising_hold_threshold_v"]
    h_inf, lambda1, lambda2, a, b = _two_node_hold_coefficients(params, delay_position)

    def hold_at(time_s: float) -> float:
        return h_inf + a * math.exp(lambda1 * time_s) + b * math.exp(lambda2 * time_s)

    if h_inf <= threshold:
        latency = math.inf
    else:
        lo = 0.0
        hi = 1.0e-6
        while hold_at(hi) < threshold and hi < 10.0:
            hi *= 2.0
        if hi >= 10.0 and hold_at(hi) < threshold:
            latency = math.inf
        else:
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                if hold_at(mid) < threshold:
                    lo = mid
                else:
                    hi = mid
            latency = 0.5 * (lo + hi)
    return {
        "initial_hold_v": 0.0,
        "final_active_v": h_inf,
        "rising_threshold_v": threshold,
        "latency_s": latency,
    }


def q1_drive_corner(params: ControllerParameters, delay_position: float) -> Dict[str, float]:
    """Q1 steady drain current and source-referenced gate overdrive."""
    vmid, rmid = vmid_thevenin(params)
    hold = active_hold_voltage(params, delay_position)
    decay_r = timer_total_decay_resistance(params, delay_position)
    load_current = hold / decay_r + params.supervisor_off_leakage
    source_voltage = vmid - load_current * rmid
    vgs_magnitude = max(0.0, source_voltage - params.detector_vol)
    return {
        "active_hold_v": hold,
        "q1_source_v": source_voltage,
        "required_drain_current_a": load_current,
        "final_vgs_magnitude_v": vgs_magnitude,
        "threshold_test_current_a": 250.0e-6,
        "vgs_threshold_max_v": 0.90,
    }


def pump_gate_on_voltage(params: ControllerParameters) -> float:
    source_r = params.r14 + params.q3_on_resistance
    return params.vcc * params.r15 / (source_r + params.r15)


def fail_off_gate_voltage(params: ControllerParameters) -> Dict[str, float]:
    gate = params.q3_off_leakage * params.r15
    return {
        "q2_gate_v": gate,
        "q2_vgs_threshold_min_v": params.q2_vgs_threshold_min,
        "off_margin_v": params.q2_vgs_threshold_min - gate,
        "gate_rc_time_constant_s": params.r15 * params.c10,
    }


def pump_gate_decay_time(params: ControllerParameters, initial_gate_v: float | None = None) -> float:
    """Time after Q3 opens until Q2 gate crosses its minimum threshold."""
    initial = pump_gate_on_voltage(params) if initial_gate_v is None else initial_gate_v
    final = params.q3_off_leakage * params.r15
    threshold = params.q2_vgs_threshold_min
    if initial <= threshold:
        return 0.0
    if final >= threshold:
        return math.inf
    return params.r15 * params.c10 * math.log((initial - final) / (threshold - final))


def supervisor_thresholds(params: ControllerParameters) -> Dict[str, float]:
    falling = params.supervisor_falling_threshold
    rising = falling * (1.0 + params.supervisor_hysteresis_fraction)
    return {
        "falling_threshold_v": falling,
        "rising_threshold_v": rising,
        "hysteresis_v": rising - falling,
    }


def supervisor_clamped_hold(
    params: ControllerParameters,
    delay_position: float,
    reset_low_v: float | None = None,
) -> Dict[str, float]:
    """Steady HOLD with Q1 on and U2 RESET_N asserted through R23."""
    reset_v = params.supervisor_vol if reset_low_v is None else reset_low_v
    vmid, rmid = vmid_thevenin(params)
    source_r = rmid + q1_charge_resistance(params)
    decay_r = timer_total_decay_resistance(params, delay_position)
    conductance = 1.0 / source_r + 1.0 / decay_r + 1.0 / params.r23
    hold = (vmid / source_r + reset_v / params.r23) / conductance
    threshold = timer_thresholds(params)["falling_hold_threshold_v"]
    return {
        "clamped_hold_v": hold,
        "falling_timer_threshold_v": threshold,
        "off_margin_v": threshold - hold,
        "steady_reset_sink_current_a": max(0.0, (hold - reset_v) / params.r23),
    }


def supervisor_clamp_sweep(
    params: ControllerParameters,
    supplies_v: Sequence[float],
    reset_low_v: float,
) -> Dict[str, object]:
    """Sweep asserted-reset HOLD clamp across supply and RV2 endpoints."""
    points = []
    for supply in supplies_v:
        for position in (0.0, 1.0):
            point_params = replace(params, vcc=float(supply))
            values = supervisor_clamped_hold(point_params, position, reset_low_v)
            points.append({"supply_v": supply, "delay_position": position, **values})
    worst = min(points, key=lambda item: float(item["off_margin_v"]))
    max_current = max(float(item["steady_reset_sink_current_a"]) for item in points)
    return {
        "points": points,
        "minimum_off_margin_v": float(worst["off_margin_v"]),
        "worst_supply_v": float(worst["supply_v"]),
        "worst_delay_position": float(worst["delay_position"]),
        "maximum_steady_reset_sink_current_a": max_current,
    }


def supervisor_startup_ramp(
    params: ControllerParameters,
    ramp_rates_v_per_s: Sequence[float],
    final_supply_v: float,
) -> Dict[str, object]:
    """Bound release timing for linear ramps and a hard-plug step.

    A rate of infinity represents a hard step to final_supply_v.
    """
    thresholds = supervisor_thresholds(params)
    rising = thresholds["rising_threshold_v"]
    cases = []
    for rate in ramp_rates_v_per_s:
        if math.isinf(rate):
            crossing_time = 0.0
            release_supply = final_supply_v
        else:
            crossing_time = rising / rate
            release_supply = min(final_supply_v, rising + rate * params.supervisor_release_delay)
        release_time = crossing_time + params.supervisor_release_delay
        cases.append(
            {
                "ramp_rate_v_per_s": "hard_step" if math.isinf(rate) else rate,
                "threshold_crossing_s": crossing_time,
                "release_time_s": release_time,
                "release_supply_v": release_supply,
            }
        )
    minimum_release_supply = min(float(case["release_supply_v"]) for case in cases)
    return {
        **thresholds,
        "release_delay_s": params.supervisor_release_delay,
        "comparator_por_delay_s": params.comparator_por_delay,
        "por_guard_margin_s": params.supervisor_release_delay - params.comparator_por_delay,
        "minimum_release_supply_v": minimum_release_supply,
        "comparator_min_supply_v": params.comparator_min_supply,
        "cases": cases,
    }


def supervisor_brownout_shutdown(
    params: ControllerParameters,
    delay_position: float,
    reset_v_for_current: float = 0.0,
    reset_v_for_timing: float = 0.30,
) -> Dict[str, float]:
    """Worst active-HOLD discharge when U2 asserts on brownout.

    The initial current uses the lowest possible RESET_N voltage; shutdown
    timing separately uses the maximum bounded 0.30 V reset-low level.
    """
    initial_hold = active_hold_voltage(params, delay_position)
    initial_current = max(0.0, (initial_hold - reset_v_for_current) / params.r23)

    vmid, rmid = vmid_thevenin(params)
    source_r = rmid + q1_charge_resistance(params)
    decay_r = timer_total_decay_resistance(params, delay_position)
    total_g = 1.0 / source_r + 1.0 / decay_r + 1.0 / params.r23
    final_hold = (
        vmid / source_r + reset_v_for_timing / params.r23
    ) / total_g
    tau = params.c7_effective / total_g
    threshold = timer_thresholds(params)["falling_hold_threshold_v"]
    if initial_hold <= threshold:
        hold_crossing = 0.0
    elif final_hold >= threshold:
        hold_crossing = math.inf
    else:
        hold_crossing = tau * math.log(
            (initial_hold - final_hold) / (threshold - final_hold)
        )
    gate_decay = pump_gate_decay_time(params)
    total = (
        params.supervisor_assert_delay
        + hold_crossing
        + params.comparator_propagation_delay
        + gate_decay
    )
    return {
        "initial_hold_v": initial_hold,
        "initial_reset_sink_current_a": initial_current,
        "recommended_reset_current_a": params.supervisor_recommended_current,
        "absolute_reset_current_a": params.supervisor_absolute_current,
        "timing_reset_low_v": reset_v_for_timing,
        "final_clamped_hold_v": final_hold,
        "falling_timer_threshold_v": threshold,
        "hold_crossing_s": hold_crossing,
        "gate_decay_s": gate_decay,
        "total_pump_off_s": total,
    }


def sensor_disconnect_release_time(
    params: ControllerParameters,
    starting_sensor_v: float,
    detector_release_v: float,
) -> float:
    tau = (params.r1 + params.r18) * params.c5
    return detector_step_latency(starting_sensor_v, 0.0, detector_release_v, tau)


def ptc_hold_current(params: ControllerParameters, temperature_c: float) -> float:
    """Linear interpolation of official 1812L150/16 hold-current anchors."""
    anchors = (
        (0.0, params.ptc_hold_0c),
        (20.0, params.ptc_hold_20c),
        (40.0, params.ptc_hold_40c),
        (50.0, params.ptc_hold_50c),
    )
    if not anchors[0][0] <= temperature_c <= anchors[-1][0]:
        raise ValueError("PTC interpolation is bounded to 0..50 C")
    for (t0, i0), (t1, i1) in zip(anchors, anchors[1:]):
        if t0 <= temperature_c <= t1:
            fraction = (temperature_c - t0) / (t1 - t0)
            return i0 + fraction * (i1 - i0)
    raise AssertionError("unreachable")


def with_supply(params: ControllerParameters, vcc: float) -> ControllerParameters:
    return replace(params, vcc=vcc)
