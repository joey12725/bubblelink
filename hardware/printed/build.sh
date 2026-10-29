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
# donor blower heads (2026-10-28): print the gauge first, set ringA_d, then the collar
render 50_head_gauge_x5.stl           blower_head.scad    -D 'part="gauge"'
render 51_head_collar_test.stl        blower_head.scad    -D 'part="collar"'
render REF_blower_head.stl            blower_head.scad    -D 'part="head"'     # reference only, don't print
# gun docks (2026-10-28): the standard umbilical panel for every gun shell. Coupon first, then
# set out_peak in gun_dock.scad if 3.0 isn't the size that fits the head hose
render 60_dock_barb_coupon.stl        gun_dock.scad       -D 'part="coupon"'
render 61_gun_dock_1head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=1
render 62_gun_dock_2head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=2
render 63_gun_dock_3head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=3
render 64_gun_dock_4head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=4
render 65_gun_dock_5head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=5
render 66_gun_dock_6head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=6
render 67_gun_dock_7head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=7
render 68_gun_dock_8head.stl         gun_dock.scad       -D 'part="dock"' -D n_out=8
render 69_dock_mount_plate.stl        gun_dock.scad       -D 'part="plate"'
# Superseded by the stick, kept for reference (not built):
#   dry_core.scad, pump_module.scad, port_insert.scad
# Duo (2026-10-28): compact two-head gun, made as a left/right pair (R = mirror of L). All purple.
# Per gun: main half (with the grip), cover half, trigger (74), dock 62.
# print the two test pieces first: the trigger housing region of each half (switch fit, nut
# stack, trigger, stop, button bottom-out). Hold them together with rubber bands.
render 00_duo_test_main.stl           duo_gun.scad        -D 'part="test_main"'
render 00_duo_test_cover.stl          duo_gun.scad        -D 'part="test_cover"'
render 70_duo_main_L.stl              duo_gun.scad        -D 'part="main"'        -D 'hand="L"'
render 71_duo_cover_L.stl             duo_gun.scad        -D 'part="cover"'       -D 'hand="L"'
render 72_duo_main_R.stl              duo_gun.scad        -D 'part="main"'        -D 'hand="R"'
render 73_duo_cover_R.stl             duo_gun.scad        -D 'part="cover"'       -D 'hand="R"'
render 74_duo_trigger.stl             duo_gun.scad        -D 'part="trigger"'     # 1 per gun
# the Duo shells' unions leave a few stray zero-area triangles; drop them (needs python + trimesh)
python clean_stl.py stl/7[0-4]_duo_*.stl stl/00_duo_test_*.stl
