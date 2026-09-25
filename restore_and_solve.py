import csv
import cmath
import os

import cst.interface
import cst.results

PROJECT_DIR = r"C:\Users\asus\btp\btp"
TARGET_PROJECT = os.path.join(PROJECT_DIR, "sphere_DR.cst")
EXPORT_CSV = os.path.join(PROJECT_DIR, "sphere_DR_sparams.csv")

de = cst.interface.DesignEnvironment.connect(28280)
prj = de.get_open_project(TARGET_PROJECT)
m = prj.model3d

print("Restoring original tutorial solver settings (2nd order, adaptive) ...")
m.add_to_history(
    "restore original solver settings",
    '''
With FDSolver
     .OrderTet "Second"
     .MeshAdaptionTet "True"
End With
''',
)
prj.save()

print("Running Frequency Domain solver ...")
try:
    m.run_solver()
except Exception as e:
    print(f"run_solver() raised: {e}")
    print("Checking whether it actually completed underneath ...")

prj.save()

msgs = prj.get_messages()
tail = msgs[-15:]
print("--- last 15 messages ---")
for msg in tail:
    print(msg)

res = cst.results.ProjectFile(TARGET_PROJECT, allow_interactive=True).get_3d()
s11 = res.get_result_item(r"1D Results\S-Parameters\S1,1")
s21 = res.get_result_item(r"1D Results\S-Parameters\S2,1")

freq = s11.get_xdata()
s11_vals = s11.get_ydata()
s21_vals = s21.get_ydata()

with open(EXPORT_CSV, "w", newline="") as fh:
    writer = csv.writer(fh)
    writer.writerow(["freq_GHz", "S11_dB", "S21_dB"])
    for f, a, b in zip(freq, s11_vals, s21_vals):
        s11_db = 20 * cmath.log10(abs(a) + 1e-30).real
        s21_db = 20 * cmath.log10(abs(b) + 1e-30).real
        writer.writerow([f, s11_db, s21_db])

print(f"Wrote {EXPORT_CSV}, {len(freq)} points")
print("Done.")
