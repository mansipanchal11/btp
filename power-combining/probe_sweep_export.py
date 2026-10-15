"""Read every parametric run of probe_sweep.cst and write the summary and curve CSVs."""

import cmath
import csv
import os

import cst.results

PROJECT_DIR = r"C:\Users\asus\btp\btp\power-combining"
PROJECT = os.path.join(PROJECT_DIR, "probe_sweep.cst")
S11_PATH = r"1D Results\S-Parameters\S1,1"

res = cst.results.ProjectFile(PROJECT, allow_interactive=True).get_3d()
run_ids = res.get_run_ids(S11_PATH, skip_nonparametric=True)

summary = []
with open(os.path.join(PROJECT_DIR, "probe_sweep_s11.csv"), "w", newline="") as fc:
    wc = csv.writer(fc)
    wc.writerow(["run_id", "r_f_mm", "h_p_mm", "freq_GHz", "S11_dB"])
    for rid in run_ids:
        params = res.get_parameter_combination(rid)
        r_f, h_p = float(params["r_f"]), float(params["h_p"])
        item = res.get_result_item(S11_PATH, run_id=rid)
        curve = [(f, 20 * cmath.log10(abs(v) + 1e-30).real) for f, v in zip(item.get_xdata(), item.get_ydata())]
        for f, db in curve:
            wc.writerow([rid, r_f, h_p, f, db])
        f_min, s_min = min(curve, key=lambda t: t[1])
        band = [f for f, db in curve if db <= -10]
        summary.append([rid, r_f, h_p, round(f_min, 3), round(s_min, 2),
                        f"{min(band):.3f}-{max(band):.3f}" if band else ""])

summary.sort(key=lambda r: (r[1], r[2]))
with open(os.path.join(PROJECT_DIR, "probe_sweep_summary.csv"), "w", newline="") as fs:
    ws = csv.writer(fs)
    ws.writerow(["run_id", "r_f_mm", "h_p_mm", "f_min_GHz", "S11_min_dB", "minus10dB_band_GHz"])
    ws.writerows(summary)

for row in summary:
    print(row)
