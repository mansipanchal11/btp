"""
Step 2 of power-combining/03-cst-workflow.md: single discrete-probe-fed 3 mm
alumina sphere on the 0.14 mm RO3003 supportive layer, ground plane below.
Uses the default probe geometry from 02-parameters-and-materials.md (0.3 mm
probe diameter, 0.14 mm insertion depth, ~0.6 mm feed-circle radius) - flagged
there as the plan's least-confident numbers since neither reference paper
demonstrates an actual probe feed.

Benchmarks against the stripline-fed paper's reported single-element numbers
(S11 dip ~34.5/35.0 GHz, ~3% BW, ~10 dBi gain, ~74% efficiency) as a sanity
check on the CST setup, even though our target frequency differs (~28-30 GHz).
"""

import os
import cst.interface

PROJECT_DIR = r"C:\Users\asus\btp\btp\power-combining"
TARGET_PROJECT = os.path.join(PROJECT_DIR, "single_probe_baseline.cst")

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
ChangeSolverType "HF Frequency Domain"
''',
)

block(
    "define materials",
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
''',
)

block(
    "define substrate",
    '''
Component.New "component1"
With Brick
     .Reset
     .Name "solid1"
     .Component "component1"
     .Material "Rogers RO3003"
     .Xrange "-3", "3"
     .Yrange "-3", "3"
     .Zrange "0", "0.14"
     .Create
End With
''',
)

block(
    "define seating hole",
    '''
With Cylinder
     .Reset
     .Name "solid3"
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
Solid.Subtract "component1:solid1", "component1:solid3"
''',
)

block(
    "define sphere",
    '''
With Sphere
     .Reset
     .Name "solid2"
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
     .Zmin "electric"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .OpenAddSpaceFactor "0.5"
End With
''',
)

block(
    "define probe pin",
    '''
With Cylinder
     .Reset
     .Name "solid4"
     .Component "component1"
     .Material "Copper (annealed)"
     .OuterRadius "0.15"
     .InnerRadius "0.0"
     .Axis "z"
     .Zrange "0.02", "0.45"
     .Xcenter "1.0"
     .Ycenter "0"
     .Segments "0"
     .Create
End With
''',
)

block(
    "define discrete port",
    '''
With DiscretePort
     .Reset
     .Portnumber "1"
     .Voltage "1"
     .Current "1"
     .Type "Sparameter"
     .Point1 "1.0", "0", "0"
     .Point2 "1.0", "0", "0.02"
     .Impedance "50"
     .UsePickedPoints False
     .Monitor False
     .Create
End With
''',
)

block(
    "define frequency + solver",
    '''
Solver.FrequencyRange "25", "40"
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

block(
    "define farfield monitors",
    '''
With Monitor
     .Reset
     .Name "farfield (f=27)"
     .FieldType "Farfield"
     .Frequency "27"
     .Create
End With
With Monitor
     .Reset
     .Name "farfield (f=28.5)"
     .FieldType "Farfield"
     .Frequency "28.5"
     .Create
End With
With Monitor
     .Reset
     .Name "farfield (f=30)"
     .FieldType "Farfield"
     .Frequency "30"
     .Create
End With
With Monitor
     .Reset
     .Name "farfield (f=33)"
     .FieldType "Farfield"
     .Frequency "33"
     .Create
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

    print("Running Frequency Domain solver ...")
    try:
        m.run_solver()
    except Exception as e:
        print(f"run_solver() raised: {e}")
        print("Checking message log (solver may have completed underneath) ...")

    prj.save()

    msgs = prj.get_messages()
    print("--- last 20 messages ---")
    if msgs:
        for msg in msgs[-20:]:
            print(msg)

    print("Done. Run export_sparams.py next to pull S11 and farfield results.")


if __name__ == "__main__":
    main()
