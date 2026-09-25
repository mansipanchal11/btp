Claude can create and edit CST projects, but not by writing the `.cst` file directly. A `.cst` file is a proprietary binary format, and CST has to be running to build or change one. What Claude can do is write scripts that control CST, and CST then creates, edits, simulates and saves the project itself.

## How it works

CST can be driven entirely by code, in two ways:

1. **VBA macros / History List.** Your `model.mod` is already one of these. Claude can write or change this code, and you paste it into **Home → History List → Edit** and click Update, or run it as a macro. That's what the tutorial's appendix does.
2. **The CST Python API (2020 and newer).** This is the more powerful option. A Python script can:
   - start CST and create a new project, or open an existing `.cst` file
   - build the geometry, materials, ports and solver settings
   - change parameters (for example `r_sphere = 4.8`) and rebuild the model
   - run the solver and save the project
   - pull S11 and S21 out of the results into a CSV file, which Claude can then analyse and plot
   - run parameter sweeps or small optimisation loops

## The workflow

Claude can't run CST here, because CST is Windows software that needs your licence. So the loop goes through your PC:

1. Claude writes the script, for example `build_sphere_dr.py`.
2. You run it on your PC with CST's own Python. It's bundled with CST, usually at `C:\Program Files\CST Studio Suite <year>\AMD64\python\python.exe`.
3. The script produces `sphere_DR.cst` plus a results CSV.
4. You share the CSV (or screenshots) back, and Claude analyses the results and suggests the next change.

If you install **Claude Code** on the same PC as CST, Claude can do steps 2–4 itself: run the script, read the results and adjust. That makes the whole design loop hands-off.

## What a script looks like

This is a short sketch based on CST's Python API. I haven't tested it, and method names differ slightly between CST versions:

```python
import cst.interface, cst.results

de  = cst.interface.DesignEnvironment()        # starts CST
prj = de.new_mws()                              # new Microwave Studio project
m   = prj.model3d

m.add_to_history("define sphere", '''
With Sphere
  .Reset
  .Name "solid2"
  .Component "component1"
  .Material "Alumina (99.5%) (lossy)"
  .Axis "z"
  .CenterRadius "r_sphere"
  .Center "0", "0", "r_sphere"
  .Create
End With''')
# ... substrate, feeds, ports, solver: same VBA blocks as model.mod

prj.save(r"D:\BTP\CST\sphere_DR.cst")
m.run_solver()

# read S21 out of the finished project
res = cst.results.ProjectFile(r"D:\BTP\CST\sphere_DR.cst").get_3d()
s21 = res.get_result_item(r"1D Results\S-Parameters\S2,1")
freq, vals = s21.get_xdata(), s21.get_ydata()   # complex S21 vs frequency
```

Right now I can:

- write the full Python build script, which recreates your whole model in one run
- write a sweep script over `r_sphere`, `s_mic` and `ss_mic` that saves all the S-parameters to CSV
- edit `model.mod` or a macro as text, for example to switch Zmax to open or widen the lines to 1.25 mm

For your BTP, the full build script plus the sweep script would save you the most manual clicking. Want me to write those, and add a "Scripting CST with Python" section to the tutorial?
