#!/usr/bin/env bash
# Regenerate every STL in stl/ from src/.
#   ./build.sh                      uses `openscad` on PATH or $OPENSCAD
#   ./build.sh /path/to/openscad    explicit binary
# Needs an OpenSCAD build with the manifold backend (2024+ snapshot).
set -euo pipefail
cd "$(dirname "$0")"
OPENSCAD="${1:-${OPENSCAD:-openscad}}"
mkdir -p stl
render() {  # render <out.stl> <src.scad> [-D var=value ...]
  local out="$1" src="$2"; shift 2
  echo "== $out"
  "$OPENSCAD" --backend=manifold -o "stl/$out" "$@" "src/$src" 2>&1 \
    | grep -iE 'warning|error' | grep -v Fontconfig || true
}
# Numbered in print order. "xN" = print N copies.
render 00_fit_coupon.stl              fit_coupon.scad
render 01_cell_holder_MID.stl         cell_holder.scad    -D 'part="mid"'
render 02_cell_holder_TERM.stl        cell_holder.scad    -D 'part="term"'
render 09_slide_clamp_x3.stl          slide_clamp.scad    -D 'part="both"'
render 10_umbilical_brick_x2.stl      umbilical_brick.scad
render 11_hose_adapter_8.5mm.stl      hose_adapter.scad   -D big_peak=8.5   # bladder tube -> 3.5 mm silicone
render 11_hose_adapter_8.0mm.stl      hose_adapter.scad   -D big_peak=8.0   # alternate, looser
render 11_hose_adapter_9.0mm.stl      hose_adapter.scad   -D big_peak=9.0   # alternate, tighter
# the stick (dry core v2): print the three fit coupons first, in the real filament
render 00_stick_coupon_rim.stl        stick.scad          -D 'part="coupon_rim"'
render 00_stick_coupon_skirt.stl      stick.scad          -D 'part="coupon_skirt"'
render 00_stick_coupon_nut.stl        stick.scad          -D 'part="coupon_nut"'
render 00_stick_coupon_ports.stl      stick.scad          -D 'part="coupon_ports"'
render 00_stick_coupon_cap.stl        stick.scad          -D 'part="coupon_cap"'
render 20_stick_tube.stl              stick.scad          -D 'part="tube"'
render 21_stick_cap.stl               stick.scad          -D 'part="cap"'
render 22_stick_sled.stl              stick.scad          -D 'part="sled"'
render 23_stick_cup.stl               stick.scad          -D 'part="cup"'
render 24_stick_prime_bezel.stl       stick.scad          -D 'part="bezel"'
render 25_stick_grommet_skirt.stl     stick.scad          -D 'part="skirt"'
render 26_stick_power_key.stl         stick.scad          -D 'part="powerkey"'
render 27_stick_pcb_spacer_x6.stl     stick.scad          -D 'part="pcbspacer"'   # 4 + 2 spares in one file
render 30_TPU_cap_ring.stl            stick.scad          -D 'part="ring"'
render 31_TPU_grommet_lower.stl       stick.scad          -D 'part="grommet_lo"'
render 32_TPU_grommet_upper.stl       stick.scad          -D 'part="grommet_hi"'
render 33_TPU_prime_boot.stl          stick.scad          -D 'part="boot"'
render 34_TPU_screw_washer_x2.stl     stick.scad          -D 'part="washer"'
render 35_TPU_prime_plunger.stl       stick.scad          -D 'part="plunger"'
render 36_TPU_battery_pad_x2.stl      stick.scad          -D 'part="batpad"'
render 37_TPU_pump_mat.stl            stick.scad          -D 'part="pumpmat"'
render 38_TPU_shim_strip_set.stl      stick.scad          -D 'part="shim"'
render 39_TPU_trimmer_plug.stl        stick.scad          -D 'part="trimplug"'
render 40_TPU_usbc_plug.stl           stick.scad          -D 'part="usbplug"'
render 41_TPU_usbA_plug.stl           stick.scad          -D 'part="usbAplug"'
render 42_TPU_gun_port_cap_x2.stl     stick.scad          -D 'part="gunportcap"'
render 43_TPU_key_blank.stl           stick.scad          -D 'part="keyblank"'
render 44_TPU_key_gasket.stl          stick.scad          -D 'part="keygasket"'
# Superseded by the stick, kept for reference (not built):
#   dry_core.scad, pump_module.scad, port_insert.scad
