"""
Step 1a of power-combining/03-cst-workflow.md: bare 3 mm alumina sphere in free
space, Eigenmode Solver, no ports/feed structure. Confirms TE1q1 lands near the
target band (~28.5-33 GHz) before anything else gets built.
"""

import os
import cst.interface

PROJECT_DIR = r"C:\Users\asus\btp\btp\power-combining"
TARGET_PROJECT = os.path.join(PROJECT_DIR, "eigenmode_bare_sphere.cst")

HISTORY_BLOCKS = []


def block(name, vba):
    HISTORY_BLOCKS.append((name, vba))


block(
    "units and solver",
    '''
With Units
     .Geometry "mm"
     .Frequency "GHz"
     .Time "s"
End With
ChangeSolverType "HF Eigenmode"
''',
)

block(
    "define material: Alumina (custom mmWave fit)",
    '''
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
''',
)

block(
    "define sphere",
    '''
Component.New "component1"
With Sphere
     .Reset
     .Name "solid1"
     .Component "component1"
     .Material "Alumina (custom mmWave fit)"
     .Axis "z"
     .CenterRadius "1.5"
     .TopRadius "0"
     .BottomRadius "0"
     .Center "0", "0", "0"
     .Segments "0"
     .Create
End With
''',
)

block(
    "define boundaries",
    '''
With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .OpenAddSpaceFactor "0.5"
End With
''',
)

block(
    "define eigenmode solver",
    '''
Solver.FrequencyRange "20", "45"
With EigenmodeSolver
     .Reset
     .SetMethodType "General (Lossy)", "Tet"
     .SetMeshType "Tetrahedral Mesh"
     .SetNumberOfModes "4"
End With
''',
)


def main():
    print("Starting new CST MWS project ...")
    de = cst.interface.DesignEnvironment.new()
    prj = de.new_mws()
    m = prj.model3d

    for name, vba in HISTORY_BLOCKS:
        print(f"  -> {name}")
        m.add_to_history(name, vba)

    print(f"Saving as {TARGET_PROJECT} ...")
    prj.save(TARGET_PROJECT, allow_overwrite=True)

    print("Running Eigenmode solver ...")
    try:
        m.run_solver()
    except Exception as e:
        print(f"run_solver() raised: {e}")
        print("Checking message log ...")

    prj.save()

    msgs = prj.get_messages()
    print("--- last 20 messages ---")
    for msg in msgs[-20:]:
        print(msg)

    es = m.EigenmodeSolver
    n = es.GetNumberOfModesCalculated()
    print(f"\nModes calculated: {n}")
    for i in range(1, n + 1):
        f_hz = es.GetModeFrequencyInHz(i)
        q = es.GetModeQFactor(i)
        print(f"  Mode {i}: f = {f_hz/1e9:.4f} GHz, Q = {q}")

    print("Done.")


if __name__ == "__main__":
    main()
