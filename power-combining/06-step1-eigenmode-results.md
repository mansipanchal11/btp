# Step 1 Results — Bare and Seated Sphere Eigenmodes

CST projects: `eigenmode_bare_sphere.cst`, `eigenmode_seated_sphere.cst` (this folder).
Both solved with CST's Eigenmode Solver (General/Lossy, tetrahedral mesh, 4 modes
requested, 20-45 GHz search window). Scripts: `eigenmode_bare_sphere.py`,
`eigenmode_seated_sphere.py`.

## Bare sphere (free space)

3 mm alumina sphere (epsilon_r = 10.5, tan-delta = 1e-3), all boundaries expanded open,
no substrate, no ground.

| Mode | Frequency | Q |
| --- | --- | --- |
| 1 | 29.373 GHz | 10.77 |
| 2 | 29.373 GHz | 10.77 |
| 3 | 29.373 GHz | 10.77 |
| 4 | 37.206 GHz | 1.97 |

Modes 1-3 are a **3-fold degenerate triplet** at the same frequency - exactly what's
expected for a TE1q1 magnetic-dipole mode on a spherically symmetric structure (the three
orthogonal dipole orientations, m = -1, 0, +1, are indistinguishable in free space). This
confirms TE1q1 at **29.37 GHz**, comfortably inside the 28.5-33 GHz target band from the
fundamental-modes paper. Q~10.8 is low because nothing suppresses radiation - the sphere
is fully exposed to free space.

## Seated on the 0.14 mm RO3003 supportive layer + ground plane

Same sphere, resting on a 6x6x0.14 mm RO3003 patch (placeholder footprint), Zmin =
electric (ground), sides/top expanded open.

| Mode | Frequency | Q |
| --- | --- | --- |
| 1 | 24.788 GHz | 1.76 |
| 2 | 27.816 GHz | 4.16 |
| 3 | 27.816 GHz | 4.16 |
| 4 | 30.257 GHz | 28.2 |

The ground plane breaks the free-space triplet's degeneracy: modes 2-3 remain a
degenerate **pair** (the two dipole orientations parallel to the ground plane, m = +-1),
while mode 1 (and possibly mode 4) reflect the dipole orientation perpendicular to the
ground (m = 0), which interacts differently with its own image in the ground plane. This
is standard image-theory behaviour for a dipole near a conducting plane, not a modelling
error - it's the same splitting effect that motivates probe orientation/placement choices
in ground-mounted DRA designs generally.

**Net effect:** the bare sphere's single 29.37 GHz triplet spreads into a family spanning
roughly **24.8-30.3 GHz** once seated. Part of that spread (mode 4, 30.26 GHz) sits
comfortably inside the target band; part (mode 1, 24.79 GHz) sits noticeably below it.

## What this means for Step 2

Which of these split components an actual probe feed couples to depends on the probe's
position and orientation relative to the sphere - a probe near the sphere's equator
predominantly drives the ground-parallel pair (modes 2-3, ~27.8 GHz), while a probe
positioned to couple to the vertical field component would drive mode 1/4 instead. This
is worth checking directly via field monitors once the single-probe-fed baseline (Step 2)
exists, rather than assumed - it directly affects which frequency the fed design actually
resonates at, and how close that lands to the 28.5-33 GHz target.

## Caveats

- Substrate footprint (6x6 mm) is an arbitrary placeholder (open question tracked
  in [05-open-questions.md](05-open-questions.md)) - not expected to change the *symmetry-
  breaking* result qualitatively, but could shift exact frequencies somewhat; worth
  re-checking once a real footprint (driven by the N=4 feed layout) is known.
- Only 4 modes were requested per run; higher-order modes above ~37 GHz weren't explored
  and aren't relevant to this project's TE1q1 scope.
