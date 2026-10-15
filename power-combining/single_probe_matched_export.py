"""Pull mode-identification probes, efficiencies, losses and farfield metrics from single_probe_matched.cst."""

import cmath
import csv
import math
import os

import cst.interface
import cst.results

PROJECT_DIR = r"C:\Users\asus\btp\btp\power-combining"
PROJECT = os.path.join(PROJECT_DIR, "single_probe_matched.cst")
ETA0 = 376.73
FREQS = [25.1, 33.106]


def curve(res, path):
    item = res.get_result_item(path)
    return list(zip(item.get_xdata(), item.get_ydata()))


def at(c, f):
    return min(c, key=lambda t: abs(t[0] - f))[1]


def mag(v):
    return abs(v) if isinstance(v, complex) else abs(float(v))


res = cst.results.ProjectFile(PROJECT, allow_interactive=True).get_3d()

e = {k: curve(res, rf"1D Results\Probes\E-Field\E-Field (0 0 1.64)({k}) [1]") for k in ("Abs", "X", "Y", "Z")}
h = {k: curve(res, rf"1D Results\Probes\H-Field\H-Field (0 0 1.64)({k}) [1]") for k in ("Abs", "X", "Y", "Z")}
s11 = curve(res, r"1D Results\S-Parameters\S1,1")
rad = curve(res, r"1D Results\Efficiencies\Rad. Efficiency [1]")
tot = curve(res, r"1D Results\Efficiencies\Tot. Efficiency [1]")
p_acc = curve(res, r"1D Results\Power\Excitation [1]\Power Accepted")
loss = {
    "copper": curve(res, r"1D Results\Power\Excitation [1]\Loss per Material\Metal loss in Copper (annealed)"),
    "alumina": curve(res, r"1D Results\Power\Excitation [1]\Loss per Material\Volume loss in Alumina (custom mmWave fit)"),
    "RO3003": curve(res, r"1D Results\Power\Excitation [1]\Loss per Material\Volume loss in Rogers RO3003"),
}

with open(os.path.join(PROJECT_DIR, "single_probe_matched_mode_ratio.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["freq_GHz", "S11_dB", "eta0_H_over_E_centre", "rad_eff", "tot_eff"])
    for (f, ea), (_, ha) in zip(e["Abs"], h["Abs"]):
        w.writerow([f, 20 * math.log10(mag(at(s11, f)) + 1e-30), ETA0 * mag(ha) / (mag(ea) + 1e-30),
                    mag(at(rad, f)), mag(at(tot, f))])

print("raw efficiency samples (to see units):", rad[len(rad) // 2], tot[len(tot) // 2])
for f in FREQS:
    ratio = ETA0 * mag(at(h["Abs"], f)) / (mag(at(e["Abs"], f)) + 1e-30)
    ecomp = {k: round(mag(at(e[k], f)), 3) for k in "XYZ"}
    hcomp = {k: round(mag(at(h[k], f)), 5) for k in "XYZ"}
    pa = mag(at(p_acc, f))
    print(f"\n=== f = {f} GHz ===")
    print(f"S11 = {20 * math.log10(mag(at(s11, f))):.2f} dB")
    print(f"eta0*|H|/|E| at sphere centre = {ratio:.2f}  (>>1 magnetic-dipole/TE-like, <<1 electric-dipole/TM-like)")
    print(f"E components at centre: {ecomp}")
    print(f"H components at centre: {hcomp}")
    print(f"rad eff = {mag(at(rad, f))}, tot eff = {mag(at(tot, f))}")
    print("loss share of accepted power: " + ", ".join(f"{k} {100 * mag(at(v, f)) / pa:.2f}%" for k, v in loss.items()))

# Farfield metrics through the open CST session.
de = cst.interface.DesignEnvironment.connect_to_any()
prj = de.get_open_project(PROJECT)
m = prj.model3d
ff = m.FarfieldPlot
for f in FREQS:
    m.SelectTreeItem(f"Farfields\\farfield (f={f}) [1]")
    out = {}
    for mode in ("directivity", "realized gain"):
        ff.Reset()
        ff.Plottype("3D")
        ff.SetPlotMode(mode)
        ff.Plot()
        out[mode] = ff.GetMax()
    try:
        out["main_lobe_dir"] = ff.GetMainLobeDirection()
    except Exception as ex:
        out["main_lobe_dir"] = f"n/a ({str(ex).splitlines()[0]})"
    out["rad_eff_ff"] = ff.GetRadiationEfficiency()
    out["tot_eff_ff"] = ff.GetTotalEfficiency()
    print(f"\nfarfield {f} GHz: {out}")

# Elevation cut phi=0 and phi=90 for pattern shape at the matched frequency.
m.SelectTreeItem(f"Farfields\\farfield (f={FREQS[1]}) [1]")
for phi in (0, 90):
    ff.Reset()
    ff.Plottype("polar")
    ff.Vary("angle1")
    ff.Phi(phi)
    ff.SetPlotMode("realized gain")
    ff.Plot()
    print(f"\ncut phi={phi}: max {ff.GetMax()}, main lobe {ff.GetMainLobeDirection()}, "
          f"3dB width {ff.GetAngularWidthXdB(3)}")
