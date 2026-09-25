# Open Questions — Status

Originally five gaps blocking the start of CST work (Step 1 of the workflow). Four are now
resolved or defaulted per the fundamental-modes paper and stated defaults; one stays a
genuinely unvalidated estimate worth an early parameter sweep.

## 1. Which alumina epsilon_r/tan-delta to use — RESOLVED

epsilon_r = 10.5, tan-delta ~ 1e-3, fitted from the fundamental-modes paper's WR-28
waveguide transmission test (a direct measurement fit, more trustworthy than a catalog
figure). Re-check against a physical sphere's measured value once one is sourced, per the
roadmap's own note that dielectric parameters are "catalog/literature approximations"
needing reconciliation later (Part H) - not a Phase 1 blocker.

## 2. Final N — DEFAULTED to 4

4 is the standard sequential-rotation starting point (90 deg steps, manageable feed
network) and is fixed for Phase 1. The roadmap's suggested "back-of-envelope link-budget
pass" (PCB area, feed-network loss, desired combining gain) is still worth doing before
fabrication, but doesn't block the CST build/solve work in
[03-cst-workflow.md](03-cst-workflow.md), none of which depends on N being final.

## 3. Feed circle radius and probe depth/diameter — DEFAULTED, LOWEST CONFIDENCE

Neither reference paper documents an actual probe/coax feed - both use microstrip or
stripline fringing coupling instead. The fundamental-modes paper's real dimensions
(0.4 mm seating-crate diameter, 1.5 mm fringing gap, 0.125 mm line width, 0.14 mm
substrate) informed the defaults in
[02-parameters-and-materials.md](02-parameters-and-materials.md) (probe diameter 0.3 mm,
insertion depth 0.14 mm, feed circle radius ~0.6 mm), but none of the three is
paper-sourced. **This is the first thing to parameter-sweep once single-probe geometry
exists in CST** (Step 5 of the workflow) - treat the default as a starting point to get a
model running, not a validated value.

## 4. Supportive-layer (air-cavity) thickness — RESOLVED

0.14 mm, taken directly from the fundamental-modes paper's on-chip parallel-plate
prototype. This substrate thickness serves double duty as both the RF substrate and the
sphere's supportive/alignment layer, matching how the paper itself builds it.

## 5. Discrete port vs. coax waveguide port — DEFAULTED to discrete port

Starting with a discrete port at each probe for CST iteration speed, per the original
plan. Revisit only if connector effects need modelling later - the roadmap flags
"connector mechanical contact quality" as a real sim-vs-measurement gap in both papers,
but that's a fabrication/measurement-stage concern, not a Phase 1 simulation blocker.

## Not a Phase 1 question (parking here for visibility)

Everything about the phase-shifting network, sequential-rotation phase values, axial
ratio targets, and probe-fed vs. aperture-coupled comparison stays parked for the
`circular-polarization/` phase and is intentionally not answered here.

## Still worth doing before Phase 1 is "done" (not blockers)

- Link-budget pass to confirm N=4 vs. a higher count (Question 2).
- Parameter sweep on probe diameter/depth/feed-circle radius once the single-probe
  baseline is running in CST (Question 3).
- If Paper 1 (stripline-fed DRA with assembly features - the one with the fuller
  layer-stack, iris, and Wheeler-cap efficiency methodology) becomes available, re-check
  the supportive-layer and shielding assumptions against it directly.
