# Project Progress and Context

BTP (B.Tech Project) under Prof. Utpal Dey: a millimeter-wave spherical dielectric
resonator antenna (DRA) that combines power from multiple feeds and targets circular
polarization (CP), building on two of his group's MAPCON papers. Full plan:
`Spherical DRA Power Combining & CP — Study Roadmap (1).pdf`.

CST Studio Suite 2025 is installed locally on this machine, and is driven end-to-end via
its Python API (`cst.interface`, `cst.results`) rather than the GUI - see `context.md` for
how that workflow works and what it can do.

## Repo map

- `context.md` - how Claude drives CST via its Python API on this machine
- `PROGRESS.md` - this file
- `Spherical DRA in CST Build-from-Scratch Tutorial (1).pdf` - tutorial used for the
  CST-scripting practice build (below)
- `Spherical DRA Power Combining & CP — Study Roadmap (1).pdf` - the actual BTP plan
- `On_the_study_of_fundamental_modes_of_spherical_dielectric_resonator_at_millimeter-wave_frequency.pdf`
  - reference paper (the roadmap's "Paper 2": mode characterization, no feed design)
- `start (1).cst`, `sphere_DR.cst`, `sphere_DR_sparams.csv`, `build_sphere_dr.py`,
  `run_sphere_dr.py`, `retry_*.py`, `export_only.py`, `restore_and_solve.py`, `*_log.txt`
  - the CST-scripting practice build (below), not part of the BTP target design
- `power-combining/` - the actual BTP Phase 1 work (multi-feed power combining, CP
  deferred) - plan docs, build scripts, and `.cst` projects

## Work completed

### 1. CST-scripting practice build (repo root)

Recreated the tutorial's two-port coupled-resonator spherical DRA (10 mm alumina sphere,
X/Ku-band, ~10-13.5 GHz, two microstrip feed lines, shielded/non-radiating) entirely via
the CST Python API, as a first exercise in scripting CST from this machine. Not the BTP
target design (different scale/band), but the CST automation lessons carried forward
directly into the real work:

- Three of four reference resonances reproduced within 0.25% (9.957, 10.34, 13.6 GHz);
  the fourth (13.45 GHz, TM101) landed 2.3% low, traced to mesh sensitivity around the
  18 um copper feed lines.
- **CST's Python `run_solver()` can raise a "not enough memory" `RuntimeError` even when
  the solver completes successfully underneath.** Always verify via
  `project.get_messages()` before concluding a run failed - this happened repeatedly and
  cost real time until identified.
- This machine (16 GB RAM) needs ~5 GB+ free for a 2nd-order adaptive tetrahedral solve;
  close other CST windows/heavy apps before a solve.
- Full write-up with charts and mode analysis: a "Spherical DRA — Design and Behaviour
  Analysis" Claude Docs report (not stored in this repo; ask if you need the link again).

### 2. Power-combining Phase 1 plan (`power-combining/`)

Scoped to the multi-feed/power-combining half of the BTP only - circular polarization
(sequential-rotation phasing) is deliberately deferred to a later phase. See
`power-combining/README.md` for the full doc index. Key resolved values (from the
fundamental-modes paper): alumina epsilon_r = 10.5, tan-delta ~1e-3; 3 mm sphere diameter;
0.14 mm RO3003 supportive layer. Probe feed geometry (diameter, depth, feed-circle radius)
has **no literature precedent** in either reference paper - both papers use
microstrip/stripline fringing feeds, not probes - so those values are engineering defaults
flagged for a parameter sweep, not paper-sourced facts (see
`power-combining/05-open-questions.md`).

### 3. Step 1 - bare and seated sphere eigenmodes: DONE

`power-combining/06-step1-eigenmode-results.md` has the full write-up. Headline: bare
sphere TE1q1 is a 3-fold degenerate triplet at 29.37 GHz (Q~10.8), inside the 28.5-33 GHz
target band. Seating it on the real substrate + ground plane splits that degeneracy into a
family spanning ~24.8-30.3 GHz (expected image-theory effect of the ground plane) - which
split component a real probe couples to depends on probe position/orientation, to be
checked once a fed model exists.

Also resolved during this step: the exact CST 2025 VBA syntax for `ChangeSolverType "HF
Eigenmode"` and `EigenmodeSolver.SetNumberOfModes "N"` (neither obvious from CST's Python
API introspection - found by grepping CST's own installed macro library and wizard
templates under `Library/`, and by testing candidate property names directly against a
live CST session).

### 4. Step 2 - single-probe-fed baseline: DONE (hybrid-mode caveat)

`power-combining/single_probe_baseline.py` / `.cst`. Built a discrete-port-fed probe next
to the sphere, on the seated structure from Step 1. First attempt (probe confined to the
0.14 mm substrate only, per the plan's original default) showed **essentially no
coupling** - S11 flat at ~0 dB across the whole 25-40 GHz band - because the sphere's
surface curves down close to the substrate near the feed circle, leaving almost no room
for the probe to reach the sphere's near field. A revised attempt (taller probe, larger
feed-circle radius, reaching up alongside the sphere without touching it) improved this to
a shallow, unresolved dip (~-1 dB near 34.7 GHz) - real frequency dependence now, but
nowhere near a matched resonance (need <= -10 dB).

**Resolved (2026-10-15) by a 15-point sweep with the probe beside the sphere** instead of
under it (`power-combining/07-probe-sweep-results.md`): feed-circle radius 1.70 mm, probe
height 1.80 mm → **S11 = −22.7 dB at 33.11 GHz**, 2.2% −10 dB bandwidth, 97% radiation
efficiency, 7.7 dBi directivity, 7.6 dBi realized gain, broadside main lobe. Centre-point
E/H probes show the excited mode is a **hybrid** (y-directed magnetic dipole plus
x-directed electric dipole), not a pure TE1q1 eigenmode — a scope decision for the
supervisor before Phase 3.

Also learned: changing CST parameters with `StoreParameter` + `Rebuild` overwrites the
previous run's results, so sweep scripts must read results after every solve. Quiet mode
(`DesignEnvironment.set_quiet_mode(True)`) stopped the blocking dialogs.

### 5. Phase 3 - four-probe power combining: FIRST STAGE DONE

`power-combining/08-four-probe-combining-results.md`. Four probes around one sphere,
full 4×4 S-matrix, combined excitations by superposition.

- **Equal-phase feeding (the roadmap's Phase 3 scheme) fails by symmetry:** it drives
  the m = 0 mode, putting a null at broadside (−48 dBi; combining efficiency 0.04).
- **Sequential rotation (0/90/180/270°) works** and is also the CP architecture. With
  the single-probe geometry reused, neighbour coupling (−10.6 dB) limited the active
  match to −9.1 dB (combining efficiency 0.88).
- **Retuned for active impedance** (feed radius 2.00 mm, probe height 2.00 mm):
  active −15.9 dB at 33.70 GHz, combining efficiency 0.975, 9.13 dBi realized gain on
  boresight, +7.6 dB EIRP over one source, +5.2 dB over the stripline-fed paper's
  antenna. Remaining weakness: 1.4% active bandwidth (paper ~3%).

## Research phases

`RESEARCH_PHASES.md` frames the project as research questions, phases and milestones
M0–M7. Status: M0, M1, M2 and M3 met; M4 onward not started.

## Next steps

1. Supervisor decisions: accept the hybrid mode; confirm re-scoping Phase 3 from equal
   phase to sequential rotation.
2. Axial ratio of the sequential-rotation excitation (Phase 4), from the saved farfields.
3. Widen the 1.4% bandwidth: metal cavity/shield, feed-network reflection cancellation.
4. Model the 4-way divider and phase lines so efficiency includes feed losses.
5. Obtain the stripline-fed paper itself to firm up the benchmark.
