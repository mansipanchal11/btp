"""
Phase 3 analysis of four_probe.cst: S-matrix, active matching, and combined
farfields for several excitation schemes.

Metrics (per scheme, at each farfield frequency):
  eta_acc      accepted / incident power, from the 4x4 S-matrix (active reflection)
  eta_tot      total efficiency of the combined farfield (radiated / incident)
  eta_combine  eta_tot / eta_tot of the isolated single-probe design (ideal 1.0)
  G_real       peak realized gain, main-lobe direction, boresight realized gain
  dEIRP_1      EIRP gain over ONE source driving the single-probe design:
               10log10(4) + G_real(combined) - G_real(single)   (ideal +6.02 dB)
  dEIRP_paper  same, against the stripline-fed paper's ~10 dBi single-source antenna
"""

import cmath
import csv
import math
import os
import sys

import cst.interface
import cst.results

PROJECT_DIR = r"C:\Users\asus\btp\btp\power-combining"
PROJECT = os.path.join(PROJECT_DIR, sys.argv[1] if len(sys.argv) > 1 else "four_probe.cst")
FF_FREQS = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [32.5, 33.1, 33.7]
TAG = os.path.splitext(os.path.basename(PROJECT))[0]
N = 4

SINGLE = {"G_real": 7.58, "eta_tot": 0.966}  # single_probe_matched.cst at 33.11 GHz
PAPER_GAIN_DBI = 10.0  # stripline-fed paper, roadmap summary

SCHEMES = {
    "equal phase": [0, 0, 0, 0],
    "sequential rotation": [0, 90, 180, 270],
    "push-pull pairs": [0, 0, 180, 180],
}


def db(x):
    return 10 * math.log10(max(x, 1e-30))


res = cst.results.ProjectFile(PROJECT, allow_interactive=True).get_3d()


def sparam(i, j):
    item = res.get_result_item(rf"1D Results\S-Parameters\S{i},{j}")
    return item.get_xdata(), item.get_ydata()


freqs, _ = sparam(1, 1)
S = [[sparam(i, j)[1] for j in range(1, N + 1)] for i in range(1, N + 1)]

with open(os.path.join(PROJECT_DIR, f"{TAG}_sparams.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["freq_GHz"] + [f"S{i}{j}_dB" for i in range(1, N + 1) for j in range(1, N + 1)])
    for k, f in enumerate(freqs):
        w.writerow([f] + [20 * math.log10(abs(S[i][j][k]) + 1e-30) for i in range(N) for j in range(N)])


def active(phases, k):
    a = [cmath.exp(1j * math.radians(p)) for p in phases]
    b = [sum(S[i][j][k] * a[j] for j in range(N)) for i in range(N)]
    gam = [b[i] / a[i] for i in range(N)]
    eta_acc = 1 - sum(abs(x) ** 2 for x in b) / N
    return gam, eta_acc


def idx(f):
    return min(range(len(freqs)), key=lambda k: abs(freqs[k] - f))


# Passive behaviour around the resonance.
k_min = min(range(len(freqs)), key=lambda k: abs(S[0][0][k]))
print(f"S11 min {20 * math.log10(abs(S[0][0][k_min])):.2f} dB at {freqs[k_min]:.3f} GHz (embedded, other ports matched)")
for f in FF_FREQS:
    k = idx(f)
    row = ", ".join(f"S1{j + 1} {20 * math.log10(abs(S[0][j][k])):.1f} dB" for j in range(N))
    print(f"{f} GHz: {row}")

# Active match per scheme across the band.
with open(os.path.join(PROJECT_DIR, f"{TAG}_active.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["freq_GHz"] + [f"{s}: worst active S dB" for s in SCHEMES] + [f"{s}: accepted fraction" for s in SCHEMES])
    for k, f in enumerate(freqs):
        worst, acc = [], []
        for ph in SCHEMES.values():
            gam, eta = active(ph, k)
            worst.append(max(20 * math.log10(abs(g) + 1e-30) for g in gam))
            acc.append(eta)
        w.writerow([f] + worst + acc)

for name, ph in SCHEMES.items():
    best = max(range(len(freqs)), key=lambda k: active(ph, k)[1])
    gam, eta = active(ph, best)
    band = [freqs[k] for k in range(len(freqs)) if max(abs(g) for g in active(ph, k)[0]) <= 10 ** (-10 / 20)]
    bw = f"{min(band):.3f}-{max(band):.3f} GHz" if band else "none"
    print(f"[{name}] best accepted fraction {eta:.3f} at {freqs[best]:.3f} GHz; "
          f"active S at that freq {[round(20 * math.log10(abs(g)), 1) for g in gam]} dB; -10 dB active band {bw}")

# Combined farfields.
de = cst.interface.DesignEnvironment.connect_to_any()
m = de.get_open_project(PROJECT).model3d
cr, ff = m.CombineResults, m.FarfieldPlot
labels = {}
for name, ph in SCHEMES.items():
    label = name.replace(" ", "_").replace("-", "_")
    cr.Reset()
    cr.SetMonitorType("frequency")
    cr.EnableAutomaticLabeling(False)
    cr.SetLabel(label)
    cr.SetNone()
    cr.ClearFilters()
    cr.AddFilter(":farfield:")
    cr.OnlyAtFrequency(-1)
    for port, p in enumerate(ph, start=1):
        cr.SetPortModeValues(port, 1, 1.0, float(p))
    cr.Run()
    labels[name] = label

tree = [t for t in m.get_tree_items() if t.startswith("Farfields\\")]
print("farfield tree:", tree)


def cut(phi):
    ff.Reset()
    ff.Plottype("polar")
    ff.Vary("angle1")
    ff.Phi(phi)
    ff.SetPlotMode("realized gain")
    ff.Plot()
    return ff.GetMax(), ff.GetMainLobeDirection(), ff.GetAngularWidthXdB()


rows = []
for f in FF_FREQS:
    k = idx(f)
    for name, label in [("single port 1 (embedded)", "1")] + [(n, l) for n, l in labels.items()]:
        item = next((t for t in tree if f"(f={f})" in t and t.endswith(f"[{label}]")), None)
        if item is None:
            print(f"missing farfield for {name} at {f}")
            continue
        m.SelectTreeItem(item)
        ff.Reset()
        ff.Plottype("3D")
        ff.SetPlotMode("realized gain")
        ff.Plot()
        g_max = ff.GetMax()
        eta_tot = 10 ** (ff.GetTotalEfficiency() / 10)
        eta_rad = 10 ** (ff.GetRadiationEfficiency() / 10)
        try:
            g_bore = ff.CalculatePoint(0.0, 0.0, "abs", item.split("\\")[-1])
        except Exception as ex:
            g_bore = f"n/a ({str(ex).splitlines()[0][:60]})"
        g0, lobe0, bw0 = cut(0)
        g90, lobe90, bw90 = cut(90)
        if name.startswith("single"):
            eta_acc = 1 - sum(abs(S[i][0][k]) ** 2 for i in range(N))
            n_src = 1
        else:
            eta_acc = active(SCHEMES[name], k)[1]
            n_src = N
        d_eirp_1 = db(n_src) + g_max - SINGLE["G_real"]
        d_eirp_paper = db(n_src) + g_max - PAPER_GAIN_DBI
        row = {
            "freq_GHz": f, "scheme": name, "eta_acc": round(eta_acc, 3), "eta_rad": round(eta_rad, 3),
            "eta_tot": round(eta_tot, 3), "eta_combine": round(eta_tot / SINGLE["eta_tot"], 3),
            "G_real_max_dBi": round(g_max, 2), "G_real_boresight": g_bore if isinstance(g_bore, str) else round(g_bore, 2),
            "lobe_theta_phi0": lobe0, "lobe_theta_phi90": lobe90, "bw3dB_phi0": round(bw0, 1), "bw3dB_phi90": round(bw90, 1),
            "dEIRP_vs_single_dB": round(d_eirp_1, 2), "dEIRP_vs_paper_dB": round(d_eirp_paper, 2),
        }
        rows.append(row)
        print(row, flush=True)

with open(os.path.join(PROJECT_DIR, f"{TAG}_combining.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print("Done.")
