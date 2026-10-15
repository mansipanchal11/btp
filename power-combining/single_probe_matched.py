"""
Characterize the matched single-probe design from probe_sweep (r_f = 1.70 mm,
h_p = 1.80 mm): which sphere mode is excited, plus radiation results.

Mode identification: E and H field probes at the sphere centre. A magnetic-
dipole (TE-type) mode has strong H and near-zero E at the centre; an electric-
dipole (TM-type) mode is the reverse. eta0*|H|/|E| >> 1 -> TE-like, << 1 -> TM-like.
"""

import csv
import os

import cst.interface
import cst.results

import probe_sweep as base

PROJECT_DIR = base.PROJECT_DIR
TARGET_PROJECT = os.path.join(PROJECT_DIR, "single_probe_matched.cst")
F_LOW, F_MATCH = "25.1", "33.106"

EXTRA = [
    ("set matched geometry", '''
StoreParameter "r_f", "1.70"
StoreParameter "h_p", "1.80"
'''),
    ("monitors and probes", f'''
With Monitor
     .Reset
     .Name "e-field (f={F_MATCH})"
     .Dimension "Volume"
     .Domain "Frequency"
     .FieldType "Efield"
     .MonitorValue "{F_MATCH}"
     .Create
End With
With Monitor
     .Reset
     .Name "h-field (f={F_MATCH})"
     .Dimension "Volume"
     .Domain "Frequency"
     .FieldType "Hfield"
     .MonitorValue "{F_MATCH}"
     .Create
End With
With Monitor
     .Reset
     .Name "farfield (f={F_MATCH})"
     .FieldType "Farfield"
     .Frequency "{F_MATCH}"
     .Create
End With
With Monitor
     .Reset
     .Name "farfield (f={F_LOW})"
     .FieldType "Farfield"
     .Frequency "{F_LOW}"
     .Create
End With
With Probe
     .Reset
     .Name "E_centre"
     .Field "Efield"
     .Orientation "All"
     .Xpos "0"
     .Ypos "0"
     .Zpos "1.64"
     .Create
End With
With Probe
     .Reset
     .Name "H_centre"
     .Field "Hfield"
     .Orientation "All"
     .Xpos "0"
     .Ypos "0"
     .Zpos "1.64"
     .Create
End With
'''),
]


def main():
    de = cst.interface.DesignEnvironment.new()
    de.set_quiet_mode(True)
    prj = de.new_mws()
    m = prj.model3d
    for name, vba in base.HISTORY + EXTRA:
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

    items = m.get_tree_items()
    print("--- result tree (filtered) ---", flush=True)
    for it in items:
        if any(k in it for k in ("Probe", "Efficien", "Farfield", "Power", "S-Parameters")):
            print(it, flush=True)

    print("--- FarfieldPlot API ---", flush=True)
    print([x for x in dir(m.FarfieldPlot) if not x.startswith("_")], flush=True)


if __name__ == "__main__":
    main()
