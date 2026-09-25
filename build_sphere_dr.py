"""
Recreates the spherical DRA two-port coupled-resonator model described in
"Spherical DRA in CST: Build-from-Scratch Tutorial.pdf", using CST's Python API.

Every History List block below is taken verbatim from the tutorial's Appendix
(macro block B), which is itself a trimmed copy of the original model.mod.
Run with CST's bundled Python:

    "C:\\Program Files (x86)\\CST Studio Suite 2025\\AMD64\\python\\python.bat" build_sphere_dr.py
"""

import os
import sys

import cst.interface
import cst.results

PROJECT_DIR = r"C:\Users\asus\btp\btp"
SOURCE_PROJECT = os.path.join(PROJECT_DIR, "start (1).cst")
TARGET_PROJECT = os.path.join(PROJECT_DIR, "sphere_DR.cst")

RUN_SOLVER = True
EXPORT_CSV = os.path.join(PROJECT_DIR, "sphere_DR_sparams.csv")
EXPORT_S2P = os.path.join(PROJECT_DIR, "sphere_DR.s2p")

MONITOR_FREQS = ["9.957", "10.34", "13.45", "13.6"]

HISTORY_BLOCKS = []


def block(name, vba):
    HISTORY_BLOCKS.append((name, vba))


# ---------------------------------------------------------------------------
# Parameters (tutorial Appendix A, run as a "define parameters" history step)
# ---------------------------------------------------------------------------
block(
    "define parameters",
    '''
StoreParameter "l_sub", "50"
StoreParameter "w_sub", "30"
StoreParameter "t_sub", "0.5"
StoreParameter "r_sphere", "5"
StoreParameter "w_inset", "(r_sphere^2-(r_sphere-t_sub)^2)^0.5"
StoreParameter "s_mic", "1"
StoreParameter "w_mic", "1"
StoreParameter "ss_mic", "3"
StoreParameter "t_metal", "0.018"
StoreParameter "f_min", "9"
StoreParameter "f_max", "14"
''',
)

# ---------------------------------------------------------------------------
# Solver and units
# ---------------------------------------------------------------------------
block(
    "solver and units",
    '''
ChangeSolverType "HF Frequency Domain"
With Units
     .Geometry "mm"
     .Frequency "GHz"
     .Time "s"
End With
''',
)

# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
block(
    "define material: Rogers RO3003 (loss free)",
    '''
With Material
     .Reset
     .Name "Rogers RO3003 (loss free)"
     .FrqType "all"
     .Type "Normal"
     .SetMaterialUnit "GHz", "mm"
     .Epsilon "3"
     .Mu "1.0"
     .TanD "0.0"
     .Colour "0.75", "0.95", "0.85"
     .Create
End With
''',
)

block(
    "define material: Alumina (99.5%) (lossy)",
    '''
With Material
     .Reset
     .Name "Alumina (99.5%) (lossy)"
     .FrqType "all"
     .Type "Normal"
     .SetMaterialUnit "MHz", "mm"
     .Epsilon "9.9"
     .Mu "1.0"
     .TanD "0.0001"
     .TanDFreq "1.0"
     .TanDGiven "True"
     .TanDModel "ConstTanD"
     .Colour "0.94", "0.82", "0.76"
     .Create
End With
''',
)

block(
    "define material: Copper (annealed)",
    '''
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
''',
)

# ---------------------------------------------------------------------------
# Substrate
# ---------------------------------------------------------------------------
block(
    "define substrate",
    '''
Component.New "component1"
With Brick
     .Reset
     .Name "solid1"
     .Component "component1"
     .Material "Rogers RO3003 (loss free)"
     .Xrange "-l_sub/2", "l_sub/2"
     .Yrange "-w_sub/2", "w_sub/2"
     .Zrange "0", "t_sub"
     .Create
End With
''',
)

# ---------------------------------------------------------------------------
# Sphere
# ---------------------------------------------------------------------------
block(
    "define sphere",
    '''
With Sphere
     .Reset
     .Name "solid2"
     .Component "component1"
     .Material "Alumina (99.5%) (lossy)"
     .Axis "z"
     .CenterRadius "r_sphere"
     .TopRadius "0"
     .BottomRadius "0"
     .Center "0", "0", "r_sphere"
     .Segments "0"
     .Create
End With
''',
)

# ---------------------------------------------------------------------------
# Seating hole (cylinder, then subtract from substrate)
# ---------------------------------------------------------------------------
block(
    "define seating hole",
    '''
With Cylinder
     .Reset
     .Name "solid3"
     .Component "component1"
     .Material "Vacuum"
     .OuterRadius "w_inset"
     .InnerRadius "0.0"
     .Axis "z"
     .Zrange "0", "t_sub"
     .Xcenter "0"
     .Ycenter "0"
     .Segments "0"
     .Create
End With
Solid.Subtract "component1:solid1", "component1:solid3"
''',
)

# ---------------------------------------------------------------------------
# Feed line 1 + two mirrors -> feed line 2
# ---------------------------------------------------------------------------
block(
    "define feed line 1 + two mirrors",
    '''
With Brick
     .Reset
     .Name "solid4"
     .Component "component1"
     .Material "Copper (annealed)"
     .Xrange "-w_inset-s_mic", "-l_sub/2"
     .Yrange "-w_mic/2-ss_mic", "w_mic/2-ss_mic"
     .Zrange "t_sub", "t_metal+t_sub"
     .Create
End With
With Transform
     .Reset
     .Name "component1:solid4"
     .Origin "Free"
     .Center "0", "0", "0"
     .PlaneNormal "0", "1", "0"
     .MultipleObjects "True"
     .GroupObjects "False"
     .Repetitions "1"
     .MultipleSelection "False"
     .Transform "Shape", "Mirror"
End With
With Transform
     .Reset
     .Name "component1:solid4_1"
     .Origin "Free"
     .Center "0", "0", "0"
     .PlaneNormal "1", "0", "0"
     .MultipleObjects "False"
     .GroupObjects "False"
     .Repetitions "1"
     .MultipleSelection "False"
     .Transform "Shape", "Mirror"
End With
''',
)

# ---------------------------------------------------------------------------
# Boundaries - exact replica of the original model (Zmax electric)
# ---------------------------------------------------------------------------
block(
    "define boundaries",
    '''
With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "electric"
     .Zmax "electric"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .OpenAddSpaceFactor "0.5"
End With
''',
)

# ---------------------------------------------------------------------------
# Ports
# ---------------------------------------------------------------------------
block(
    "define ports",
    '''
Pick.PickFaceFromId "component1:solid4", "4"
With Port
     .Reset
     .PortNumber "1"
     .NumberOfModes "1"
     .Coordinates "Picks"
     .Orientation "positive"
     .PortOnBound "True"
     .ClipPickedPortToBound "False"
     .XrangeAdd "0.0", "0.0"
     .YrangeAdd "2.5*w_mic", "2.5*w_mic"
     .ZrangeAdd "t_sub", "2.5*w_mic"
     .Create
End With
Pick.PickFaceFromId "component1:solid4_1", "4"
With Port
     .Reset
     .PortNumber "2"
     .NumberOfModes "1"
     .Coordinates "Picks"
     .Orientation "positive"
     .PortOnBound "True"
     .ClipPickedPortToBound "False"
     .XrangeAdd "0.0", "0.0"
     .YrangeAdd "2.5*w_mic", "2.5*w_mic"
     .ZrangeAdd "t_sub", "2.5*w_mic"
     .Create
End With
''',
)

# ---------------------------------------------------------------------------
# Frequency range + solver
# ---------------------------------------------------------------------------
block(
    "define frequency + solver",
    '''
Solver.FrequencyRange "f_min", "f_max"
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
''',
)

# ---------------------------------------------------------------------------
# Field monitors: E-field + H-field at each candidate resonance
# ---------------------------------------------------------------------------
monitor_vba = ""
for f in MONITOR_FREQS:
    monitor_vba += f'''
With Monitor
     .Reset
     .Name "e-field (f={f})"
     .Dimension "Volume"
     .Domain "Frequency"
     .FieldType "Efield"
     .MonitorValue "{f}"
     .Create
End With
With Monitor
     .Reset
     .Name "h-field (f={f})"
     .Dimension "Volume"
     .Domain "Frequency"
     .FieldType "Hfield"
     .MonitorValue "{f}"
     .Create
End With
'''
block("define field monitors", monitor_vba)


def main():
    print(f"Opening {SOURCE_PROJECT} ...")
    de = cst.interface.DesignEnvironment.new()
    prj = de.open_project(SOURCE_PROJECT)
    m = prj.model3d

    for name, vba in HISTORY_BLOCKS:
        print(f"  -> {name}")
        m.add_to_history(name, vba)

    print(f"Saving as {TARGET_PROJECT} ...")
    prj.save(TARGET_PROJECT, allow_overwrite=True)

    if RUN_SOLVER:
        print("Running Frequency Domain solver ...")
        m.run_solver()
        prj.save()
        print("Solver finished, exporting S-parameters ...")
        export_results()

    print("Done.")


def export_results():
    res = cst.results.ProjectFile(TARGET_PROJECT, allow_interactive=True).get_3d()
    s11 = res.get_result_item(r"1D Results\S-Parameters\S1,1")
    s21 = res.get_result_item(r"1D Results\S-Parameters\S2,1")

    freq = s11.get_xdata()
    s11_vals = s11.get_ydata()
    s21_vals = s21.get_ydata()

    import csv
    import cmath

    with open(EXPORT_CSV, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["freq_GHz", "S11_dB", "S21_dB"])
        for f, a, b in zip(freq, s11_vals, s21_vals):
            s11_db = 20 * cmath.log10(abs(a) + 1e-30).real
            s21_db = 20 * cmath.log10(abs(b) + 1e-30).real
            writer.writerow([f, s11_db, s21_db])

    print(f"Wrote {EXPORT_CSV}")


if __name__ == "__main__":
    main()
