# CST Workflow — Phase 1 (Power Combining Only)

Scoped from Roadmap Part G, filtered to exclude anything CP-specific (axial ratio,
phase-stepped excitation, LHCP/RHCP farfield monitors - those move to
`circular-polarization/`).

## Step sequence

1. **Bare-sphere eigenmode run.** No ports, no feed structure. 3 mm alumina sphere
   (epsilon_r = 10.5, tan-delta ~1e-3) in free space first, then seated on the actual
   0.14 mm RO3003 supportive layer, to confirm TE1q1 lands near the target band
   (~28.5-33 GHz - see [02-parameters-and-materials.md](02-parameters-and-materials.md))
   before anything else is built. Mirrors Paper 2's parallel-plate PMC-symmetry approach;
   a PMC symmetry plane can halve/quarter solve time here since the bare, unfed structure
   is symmetric.

2. **Single-probe-fed baseline.** Add one discrete port/probe using the default geometry
   in [02-parameters-and-materials.md](02-parameters-and-materials.md) (0.3 mm probe
   diameter, 0.14 mm insertion depth) - flagged there as the least-confident numbers in
   the plan, since neither reference paper demonstrates an actual probe feed. Build
   layer-by-layer per Paper 1's stack (supportive layer with alignment hole -> feed layer
   -> shield). Solve
   with the Time Domain solver for broadband S11 and farfield in one run; cross-check the
   TE1q1 resonance itself with the Frequency Domain solver, since it's a high-Q,
   narrowband feature a transient solver's mesh/timestep can under-resolve (this exact
   failure mode - coarse mesh shifting a high-Q resonance by several percent - showed up
   in the CST tutorial baseline and is why the eigenmode + frequency-domain cross-check
   is worth the extra runs). Benchmark S11, gain, bandwidth against Paper 1's reported
   numbers (S11 dip 34.5/35.0 GHz, ~3% BW, ~10 dBi gain, ~74% efficiency) as a sanity
   check on the CST setup itself, even though the target frequency differs.

3. **Extend to N=4 probes, equal amplitude, equal phase.** Add three more identical
   probes at 90 deg spacing on the feed circle (default radius ~0.6 mm - the plan's
   least-confident number, so treat Step 4's mesh convergence check and any early result
   here as provisional until it's been swept). All four ports driven with the same
   amplitude and phase (no sequential rotation yet). CST computes the full 4x4 S-matrix
   in one run - use this to check port-to-port isolation (S_nm) alongside S11.

4. **Mesh convergence check.** Increase mesh density (refine near the sphere-substrate
   contact point and each probe-to-sphere gap - these small features drive convergence,
   per Part G) until S11 and gain stabilize, before trusting any of the above results.

5. **Post-process and compare against Section 4's metrics** (power-combining efficiency,
   mode purity, impedance bandwidth).

## Solver choice per step

| Step | Solver | Why |
| --- | --- | --- |
| 1. Bare-sphere eigenmode | Eigenmode Solver | No ports; finds natural resonant frequencies directly |
| 2-3. Fed structure, broadband | Time Domain (Transient) | Handles multiple ports well; full S-matrix + farfield in one wideband run |
| 2-3. Cross-check near TE1q1 | Frequency Domain | High-accuracy narrowband check on the high-Q resonance transient solvers can under-resolve |

## Mesh and memory strategy (lessons carried from the CST tutorial baseline)

The tutorial baseline build on this machine (16 GB RAM) repeatedly hit
`"not enough memory"` errors from CST's Frequency Domain solver (2nd-order tetrahedral +
adaptive refinement) whenever free RAM dropped below ~5 GB - and, separately, discovered
that CST's Python `run_solver()` call can report that error as a fatal `RuntimeError`
**even when the solver actually completes successfully underneath**. Two things to plan
for as this N-port model gets more mesh-hungry than the 2-port baseline:

- **Prefer the Time Domain solver for the full N-port radiating runs** (per the solver
  table above) - it's the roadmap's own recommendation for multi-port broadband work and
  is generally lighter on memory than a 2nd-order adaptive tetrahedral frequency-domain
  solve of the same structure. Reserve Frequency Domain for the smaller single-element/
  eigenmode cross-checks where the accuracy payoff matters most.
- **When scripting solves via the CST Python API, always verify completion from
  `project.get_messages()`**, not from whether `run_solver()` raised an exception - this
  was a repeated false negative in the tutorial baseline. Treat a `RuntimeError` from
  `run_solver()` as "check the message log," not "the run failed."
- **Close other CST windows/heavy apps before a solve** if free RAM is under ~5 GB;
  confirm with a quick memory check before kicking off a long run.

## Parameter sweeps (once the N=4 equal-phase baseline works)

Per Roadmap Part G, use CST's built-in parameter sweep against:
- Probe position/depth (coupling strength)
- Feed circle radius
- N itself, if the link-budget pass in [05-open-questions.md](05-open-questions.md)
  suggests testing more than one value

Sequential-rotation phase steps are a Part 2 sweep variable, not Phase 1.
