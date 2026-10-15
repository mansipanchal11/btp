"""
Step 2 continuation: parameter sweep of the single-probe feed to find a matched
configuration (S11 <= -10 dB). Previous attempts put the probe under the
sphere's footprint (rho < 1.5 mm), where the sphere curves down to the
substrate and caps probe height below 0.5 mm -> weak coupling. This sweep
places the probe beside the sphere (rho >= 1.7 mm, clear of the sphere at any
height) and sweeps probe height toward the sphere's equator (z = 1.64 mm).

Writes:
  probe_sweep_summary.csv   one row per (r_f, h_p): best S11 dip and frequency
  probe_sweep_s11.csv       full S11 curves, long format
"""

import cmath
import csv
import itertools
import os

import cst.interface
import cst.results

PROJECT_DIR = r"C:\Users\asus\btp\btp\power-combining"
TARGET_PROJECT = os.path.join(PROJECT_DIR, "probe_sweep.cst")
SUMMARY_CSV = os.path.join(PROJECT_DIR, "probe_sweep_summary.csv")
CURVES_CSV = os.path.join(PROJECT_DIR, "probe_sweep_s11.csv")

R_F = ["1.70", "1.85", "2.00"]
H_P = ["0.60", "0.90", "1.20", "1.50", "1.80"]

HISTORY = [
    ("parameters", '''
StoreParameter "r_f", "1.70"
StoreParameter "h_p", "0.60"
StoreParameter "r_p", "0.15"
'''),
    ("units and solver", '''
With Units
     .Geometry "mm"
     .Frequency "GHz"
     .Time "s"
End With
ChangeSolverType "HF Frequency Domain"
'''),
    ("materials", '''
With Material
     .Reset
     .Name "Alumina (custom mmWave fit)"
     .FrqType "all"
     .Type "Normal"
     .SetMaterialUnit "GHz", "mm"
     .Epsilon "10.5"
     .Mu "1.0"
     .TanD "1e-3"
     .TanDFreq "30"
     .TanDGiven "True"
     .TanDModel "ConstTanD"
     .Colour "0.85", "0.85", "0.9"
     .Create
End With
With Material
     .Reset
     .Name "Rogers RO3003"
     .FrqType "all"
     .Type "Normal"
     .SetMaterialUnit "GHz", "mm"
     .Epsilon "3.0"
     .Mu "1.0"
     .TanD "1e-3"
     .TanDFreq "10"
     .TanDGiven "True"
     .TanDModel "ConstTanD"
     .Colour "0.75", "0.95", "0.85"
     .Create
End With
With Material
     .Reset
     .Name "Copper (annealed)"
     .FrqType "all"
     .Type "Lossy metal"
     .SetMaterialUnit "GHz", "mm"
     .Mu "1.0"
     .Kappa "5.8e+007"
     .Colour "1", "1", "0"
     .Create
End With
'''),
    ("geometry", '''
Component.New "component1"
With Brick
     .Reset
     .Name "substrate"
     .Component "component1"
     .Material "Rogers RO3003"
     .Xrange "-4", "4"
     .Yrange "-4", "4"
     .Zrange "0", "0.14"
     .Create
End With
With Cylinder
     .Reset
     .Name "crate"
     .Component "component1"
     .Material "Vacuum"
     .OuterRadius "0.2"
     .InnerRadius "0.0"
     .Axis "z"
     .Zrange "0", "0.14"
     .Xcenter "0"
     .Ycenter "0"
     .Segments "0"
     .Create
End With
Solid.Subtract "component1:substrate", "component1:crate"
With Sphere
     .Reset
     .Name "sphere"
     .Component "component1"
     .Material "Alumina (custom mmWave fit)"
     .Axis "z"
     .CenterRadius "1.5"
     .TopRadius "0"
     .BottomRadius "0"
     .Center "0", "0", "1.64"
     .Segments "0"
     .Create
End With
With Cylinder
     .Reset
     .Name "probe"
     .Component "component1"
     .Material "Copper (annealed)"
     .OuterRadius "r_p"
     .InnerRadius "0.0"
     .Axis "z"
     .Zrange "0.02", "h_p"
     .Xcenter "r_f"
     .Ycenter "0"
     .Segments "0"
     .Create
End With
'''),
    ("boundaries", '''
With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "electric"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .OpenAddSpaceFactor "0.5"
End With
'''),
    ("discrete port", '''
With DiscretePort
     .Reset
     .Portnumber "1"
     .Voltage "1"
     .Current "1"
     .Type "Sparameter"
     .Point1 "r_f", "0", "0"
     .Point2 "r_f", "0", "0.02"
     .Impedance "50"
     .UsePickedPoints False
     .Monitor False
     .Create
End With
'''),
    ("solver", '''
Solver.FrequencyRange "22", "40"
Mesh.SetCreator "High Frequency"
With FDSolver
     .Reset
     .SetMethod "Tetrahedral", "General purpose"
     .OrderTet "Second"
     .Stimulation "1", "1"
     .AutoNormImpedance "False"
     .NormingImpedance "50"
     .AccuracyTet "1e-4"
     .MeshAdaptionTet "True"
     .SetNumberOfResultDataSamples "1001"
End With
'''),
]


def read_s11():
    # Changing a parameter overwrites the previous run's results, so read right after each solve.
    path = r"1D Results\S-Parameters\S1,1"
    res = cst.results.ProjectFile(TARGET_PROJECT, allow_interactive=True).get_3d()
    run_id = max(res.get_run_ids(path))
    item = res.get_result_item(path, run_id=run_id)
    out = []
    for f, v in zip(item.get_xdata(), item.get_ydata()):
        out.append((f, 20 * cmath.log10(abs(v) + 1e-30).real))
    return run_id, out


def main():
    de = cst.interface.DesignEnvironment.new()
    de.set_quiet_mode(True)
    prj = de.new_mws()
    m = prj.model3d
    for name, vba in HISTORY:
        print(f"  -> {name}", flush=True)
        m.add_to_history(name, vba)
    prj.save(TARGET_PROJECT, allow_overwrite=True)

    summary_rows = []
    with open(CURVES_CSV, "w", newline="") as fc:
        wc = csv.writer(fc)
        wc.writerow(["r_f_mm", "h_p_mm", "freq_GHz", "S11_dB"])
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
            msgs = prj.get_messages() or []
            converged = any("convergence criteria have been satisfied" in x.get("text", "") for x in msgs[-40:])
            try:
                run_id, curve = read_s11()
            except Exception as e:
                print(f"  could not read S11: {e}", flush=True)
                summary_rows.append([r_f, h_p, "", "", "", converged])
                continue
            for f, db in curve:
                wc.writerow([r_f, h_p, f, db])
            fc.flush()
            f_min, s_min = min(curve, key=lambda t: t[1])
            bw_pts = [f for f, db in curve if db <= -10]
            bw = f"{min(bw_pts):.3f}-{max(bw_pts):.3f}" if bw_pts else ""
            print(f"  run {run_id}: min S11 {s_min:.2f} dB @ {f_min:.3f} GHz, -10dB band {bw or 'none'}", flush=True)
            summary_rows.append([r_f, h_p, f"{f_min:.3f}", f"{s_min:.2f}", bw, converged])
            with open(SUMMARY_CSV, "w", newline="") as fs:
                ws = csv.writer(fs)
                ws.writerow(["r_f_mm", "h_p_mm", "f_min_GHz", "S11_min_dB", "minus10dB_band_GHz", "converged"])
                ws.writerows(summary_rows)

    print("Done.", flush=True)


if __name__ == "__main__":
    main()
