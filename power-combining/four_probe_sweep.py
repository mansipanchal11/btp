"""
Retune the 4-probe geometry for its ACTIVE match under sequential-rotation
(m = 1, broadside) drive, instead of the isolated single-probe match.

By the 4-fold symmetry S12 = S14, so for phases 0/90/180/270 deg the active
reflection at every port is  Gamma_SR = S11 - S13,  and for equal phase it is
Gamma_EQ = S11 + 2*S12 + S13. Exciting port 1 alone gives S11, S21, S31, S41,
so each run needs one stimulation instead of four.
"""

import cmath
import csv
import itertools
import math
import os

import cst.interface
import cst.results

import four_probe_model as fp

PROJECT = os.path.join(fp.PROJECT_DIR, "four_probe_sweep.cst")
SUMMARY = os.path.join(fp.PROJECT_DIR, "four_probe_sweep_summary.csv")
CURVES = os.path.join(fp.PROJECT_DIR, "four_probe_sweep_active.csv")
R_F = ["1.70", "1.85", "2.00"]
H_P = ["1.60", "1.80", "2.00", "2.20"]

POS = [("r_f", "0"), ("0", "r_f"), ("-r_f", "0"), ("0", "-r_f")]


def parametric(block):
    for i, (x, y) in enumerate(POS):
        old = [(f"{v:.1f}" if abs(v) > 1e-9 else "0.0") for v in
               (fp.R_F * math.cos(math.radians(fp.ANGLES[i])), fp.R_F * math.sin(math.radians(fp.ANGLES[i])))]
        block = block.replace(f'"{old[0]}", "{old[1]}"', f'"{x}", "{y}"')
        block = block.replace(f'.Xcenter "{old[0]}"\n     .Ycenter "{old[1]}"', f'.Xcenter "{x}"\n     .Ycenter "{y}"')
    return block


HISTORY = []
for name, vba in fp.HISTORY:
    if name in ("geometry: four probes", "discrete ports"):
        vba = parametric(vba)
    if name == "solver":
        vba = vba.replace('.Stimulation "All", "All"', '.Stimulation "1", "1"')
    if name == "farfield monitors":
        continue
    HISTORY.append((name, vba))


def read_row1():
    res = cst.results.ProjectFile(PROJECT, allow_interactive=True).get_3d()
    out = {}
    for j in (1, 2, 3):
        path = rf"1D Results\S-Parameters\S{j},1"
        item = res.get_result_item(path, run_id=max(res.get_run_ids(path)))
        out[j] = (item.get_xdata(), item.get_ydata())
    return out


def db(z):
    return 20 * math.log10(abs(z) + 1e-30)


def main():
    for name, vba in HISTORY:
        if name in ("geometry: four probes", "discrete ports") and "r_f" not in vba:
            raise SystemExit(f"parametrisation failed for {name}")
    de = cst.interface.DesignEnvironment.connect_to_any_or_new()
    de.set_quiet_mode(True)
    prj = de.new_mws()
    m = prj.model3d
    for name, vba in HISTORY:
        m.add_to_history(name, vba)
    prj.save(PROJECT, allow_overwrite=True)

    rows = []
    with open(CURVES, "w", newline="") as fc:
        wc = csv.writer(fc)
        wc.writerow(["r_f_mm", "h_p_mm", "freq_GHz", "S11_dB", "S21_dB", "S31_dB", "active_SR_dB", "active_EQ_dB"])
        for r_f, h_p in itertools.product(R_F, H_P):
            print(f"Run r_f={r_f} h_p={h_p}", flush=True)
            m.StoreParameter("r_f", r_f)
            m.StoreParameter("h_p", h_p)
            m.Rebuild()
            try:
                m.run_solver()
            except Exception as e:
                print(f"  run_solver raised (checking log): {str(e).splitlines()[0]}", flush=True)
            prj.save()
            try:
                s = read_row1()
            except Exception as e:
                print(f"  could not read results: {e}", flush=True)
                continue
            f = s[1][0]
            sr = [s[1][1][k] - s[3][1][k] for k in range(len(f))]
            eq = [s[1][1][k] + 2 * s[2][1][k] + s[3][1][k] for k in range(len(f))]
            for k in range(len(f)):
                wc.writerow([r_f, h_p, f[k], db(s[1][1][k]), db(s[2][1][k]), db(s[3][1][k]), db(sr[k]), db(eq[k])])
            fc.flush()
            win = [k for k in range(len(f)) if 28 <= f[k] <= 38]
            kb = min(win, key=lambda k: abs(sr[k]))
            band = [f[k] for k in win if db(sr[k]) <= -10]
            rows.append([r_f, h_p, round(f[kb], 3), round(db(sr[kb]), 2),
                         f"{min(band):.3f}-{max(band):.3f}" if band else "",
                         round(max(band) - min(band), 3) if band else 0.0,
                         round(db(s[2][1][kb]), 1), round(db(s[3][1][kb]), 1)])
            print(f"  SR active best {rows[-1][3]} dB @ {rows[-1][2]} GHz, -10 dB band {rows[-1][4] or 'none'}", flush=True)
            with open(SUMMARY, "w", newline="") as fs:
                ws = csv.writer(fs)
                ws.writerow(["r_f_mm", "h_p_mm", "f_best_GHz", "active_SR_best_dB", "minus10dB_band_GHz",
                             "bandwidth_GHz", "S21_dB_at_best", "S31_dB_at_best"])
                ws.writerows(rows)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
