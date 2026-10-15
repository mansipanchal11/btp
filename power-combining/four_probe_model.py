"""
Phase 3 first-stage model: one 3 mm alumina sphere fed by four identical probes
at 90 deg spacing (the matched single-probe geometry from Step 2: feed-circle
radius 1.70 mm, probe height 1.80 mm, probe radius 0.15 mm).

Every port is stimulated in turn, giving the full 4x4 S-matrix and per-port
farfields. Combined excitations (equal phase, sequential rotation, push-pull)
are formed afterwards by superposition in combine_excitations.py.
"""

import math
import os

import cst.interface

import probe_sweep as base

PROJECT_DIR = base.PROJECT_DIR
TARGET_PROJECT = os.path.join(PROJECT_DIR, "four_probe.cst")
FF_FREQS = ["32.5", "33.1", "33.7"]
ANGLES = [0, 90, 180, 270]

common = {name: vba for name, vba in base.HISTORY}

probes = ""
ports = ""
R_F = 1.70
for i, ang in enumerate(ANGLES, start=1):
    x = f"{round(R_F * math.cos(math.radians(ang)), 6) + 0.0}"
    y = f"{round(R_F * math.sin(math.radians(ang)), 6) + 0.0}"
    probes += f'''
With Cylinder
     .Reset
     .Name "probe{i}"
     .Component "component1"
     .Material "Copper (annealed)"
     .OuterRadius "r_p"
     .InnerRadius "0.0"
     .Axis "z"
     .Zrange "0.02", "h_p"
     .Xcenter "{x}"
     .Ycenter "{y}"
     .Segments "0"
     .Create
End With
'''
    ports += f'''
With DiscretePort
     .Reset
     .Portnumber "{i}"
     .Voltage "1"
     .Current "1"
     .Type "Sparameter"
     .Point1 "{x}", "{y}", "0"
     .Point2 "{x}", "{y}", "0.02"
     .Impedance "50"
     .UsePickedPoints False
     .Monitor False
     .Create
End With
'''

geometry = common["geometry"].split("With Cylinder\n     .Reset\n     .Name \"probe\"")[0]

farfields = "".join(f'''
With Monitor
     .Reset
     .Name "farfield (f={f})"
     .FieldType "Farfield"
     .Frequency "{f}"
     .Create
End With
''' for f in FF_FREQS)

solver = common["solver"].replace('.Stimulation "1", "1"', '.Stimulation "All", "All"')

HISTORY = [
    ("parameters", '''
StoreParameter "r_f", "1.70"
StoreParameter "h_p", "1.80"
StoreParameter "r_p", "0.15"
'''),
    ("units and solver", common["units and solver"]),
    ("materials", common["materials"]),
    ("geometry: substrate, crate, sphere", geometry),
    ("geometry: four probes", probes),
    ("boundaries", common["boundaries"]),
    ("discrete ports", ports),
    ("solver", solver),
    ("farfield monitors", farfields),
]


def main():
    de = cst.interface.DesignEnvironment.connect_to_any_or_new()
    de.set_quiet_mode(True)
    prj = de.new_mws()
    m = prj.model3d
    for name, vba in HISTORY:
        print(f"  -> {name}", flush=True)
        m.add_to_history(name, vba)
    prj.save(TARGET_PROJECT, allow_overwrite=True)
    try:
        m.run_solver()
    except Exception as e:
        print(f"run_solver raised (checking log): {str(e).splitlines()[0]}", flush=True)
    prj.save()
    for msg in (prj.get_messages() or [])[-8:]:
        print(msg, flush=True)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
