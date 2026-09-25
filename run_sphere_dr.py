"""
start (1).cst already contains the complete spherical DRA model (geometry,
materials, ports, monitors) described in the tutorial - it just hasn't been
solved yet. This script opens a clean copy, saves it as sphere_DR.cst, runs
the Frequency Domain solver, and exports S11/S21 to CSV.

Run with CST's bundled Python:
    "C:\\Program Files (x86)\\CST Studio Suite 2025\\AMD64\\python\\python.bat" run_sphere_dr.py
"""

import csv
import cmath
import os

import cst.interface
import cst.results

PROJECT_DIR = r"C:\Users\asus\btp\btp"
SOURCE_PROJECT = os.path.join(PROJECT_DIR, "start (1).cst")
TARGET_PROJECT = os.path.join(PROJECT_DIR, "sphere_DR.cst")
EXPORT_CSV = os.path.join(PROJECT_DIR, "sphere_DR_sparams.csv")


def main():
    print(f"Opening {SOURCE_PROJECT} ...")
    de = cst.interface.DesignEnvironment.new()
    prj = de.open_project(SOURCE_PROJECT)
    m = prj.model3d

    print(f"Saving a working copy as {TARGET_PROJECT} ...")
    prj.save(TARGET_PROJECT, allow_overwrite=True)

    print("Running Frequency Domain solver (this can take a few minutes) ...")
    m.run_solver()
    prj.save()
    print("Solver finished. Exporting S-parameters ...")

    export_results()
    print("Done.")


def export_results():
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

    print(f"Wrote {EXPORT_CSV}")


if __name__ == "__main__":
    main()
