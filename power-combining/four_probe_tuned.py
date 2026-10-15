"""
Full 4-port solve of a retuned geometry chosen from four_probe_sweep.

Usage: python four_probe_tuned.py <r_f_mm> <h_p_mm> <f1,f2,f3 GHz for farfields>
Writes four_probe_tuned.cst; analyse with
    python combine_excitations.py four_probe_tuned.cst <f1,f2,f3>
"""

import os
import sys

import cst.interface

import four_probe_sweep as sw

r_f, h_p = sys.argv[1], sys.argv[2]
ff_freqs = sys.argv[3].split(",")
PROJECT = os.path.join(sw.fp.PROJECT_DIR, "four_probe_tuned.cst")

history = []
for name, vba in sw.HISTORY:
    if name == "parameters":
        vba = f'StoreParameter "r_f", "{r_f}"\nStoreParameter "h_p", "{h_p}"\nStoreParameter "r_p", "0.15"\n'
    if name == "solver":
        vba = vba.replace('.Stimulation "1", "1"', '.Stimulation "All", "All"')
    history.append((name, vba))
history.append(("farfield monitors", "".join(f'''
With Monitor
     .Reset
     .Name "farfield (f={f})"
     .FieldType "Farfield"
     .Frequency "{f}"
     .Create
End With
''' for f in ff_freqs)))

de = cst.interface.DesignEnvironment.connect_to_any_or_new()
de.set_quiet_mode(True)
prj = de.new_mws()
m = prj.model3d
for name, vba in history:
    print(f"  -> {name}", flush=True)
    m.add_to_history(name, vba)
prj.save(PROJECT, allow_overwrite=True)
try:
    m.run_solver()
except Exception as e:
    print(f"run_solver raised (checking log): {str(e).splitlines()[0]}", flush=True)
prj.save()
for msg in (prj.get_messages() or [])[-6:]:
    print(msg, flush=True)
print("Done.", flush=True)
