# Step 2 Results — Matched Single-Probe Baseline

A vertical probe beside the sphere, 1.80 mm tall at a 1.70 mm feed-circle radius, matches
at **33.11 GHz (S11 = −22.7 dB)** with **97% radiation efficiency** and **7.6 dBi realized
gain** at broadside. The excited mode is a **hybrid** with strong magnetic-dipole content,
not a pure TE1q1 eigenmode — see Section 4 before relying on it as "the TE1q1 antenna".

Projects and scripts (this folder): `probe_sweep.cst` / `probe_sweep.py` (sweep),
`single_probe_matched.cst` / `single_probe_matched.py` (characterization),
`single_probe_matched_export.py`, `single_probe_matched_cuts.py` (post-processing).
Data: `probe_sweep_summary.csv`, `probe_sweep_s11.csv`, `single_probe_matched_mode_ratio.csv`.

## 1. Why the earlier attempts failed

Both earlier placements put the probe under the sphere's footprint (feed-circle radius
0.6 mm and 1.0 mm). There the sphere curves down to within 0.1–0.5 mm of the substrate,
so the probe could not be taller than ~0.5 mm without touching it. Best result: −1 dB.

The sweep instead puts the probe **beside** the sphere, at radii ≥ 1.70 mm, where a probe
of radius 0.15 mm clears the 1.5 mm sphere at any height.

## 2. Sweep

Model: 3 mm alumina sphere (εr 10.5, tanδ 1e-3) on 0.14 mm RO3003 (8 × 8 mm), ground plane
(Zmin electric), open elsewhere; copper probe radius 0.15 mm from z = 0.02 mm to h_p; 50 Ω
discrete port across the 0.02 mm gap to ground. Frequency Domain solver, 2nd-order
adaptive tetrahedral mesh, 22–40 GHz. All 15 runs converged.

Best S11 per run (−10 dB band shown where it exists):

| Feed radius r_f | h_p = 0.60 | 0.90 | 1.20 | 1.50 | 1.80 mm |
| --- | --- | --- | --- | --- | --- |
| 1.70 mm | −0.1 dB | −0.5 | −2.2 | −6.1 @ 34.0 GHz | **−22.7 @ 33.11 GHz** (32.78–33.50) |
| 1.85 mm | −0.1 | −0.4 | −1.6 | −4.5 @ 39.5 | −12.8 @ 33.83 (33.57–34.22) |
| 2.00 mm | −0.1 | −0.4 | −1.4 | −4.1 @ 39.7 | −10.2 @ 34.15 (34.04–34.29) |

- Coupling only becomes useful once the probe reaches **above the sphere's equator**
  (z = 1.64 mm). Below h_p ≈ 1.2 mm the only feature is the probe's own rising
  response at the top of the band.
- Moving the probe closer to the sphere strengthens coupling and lowers the resonance
  (34.15 → 33.83 → 33.11 GHz).
- The best point sits on the edge of the grid (closest radius, tallest probe), so a
  better optimum may exist at h_p > 1.8 mm. r_f cannot go much below 1.70 mm without
  the probe touching the sphere.

A second, broad and shallow dip appears near **25.1 GHz** (−5.4 dB at the matched
geometry). It lines up with the low-Q (Q ≈ 1.8) seated eigenmode at 24.79 GHz.

## 3. Matched design: radiation performance

| Quantity | 33.11 GHz (matched) | 25.1 GHz (secondary dip) |
| --- | --- | --- |
| S11 | −22.7 dB | −5.4 dB |
| −10 dB bandwidth | 32.78–33.50 GHz (0.72 GHz, 2.2%) | — |
| Radiation efficiency | 97.1% (−0.13 dB) | 99.3% |
| Total efficiency (incl. mismatch) | 96.6% (−0.15 dB) | 70.7% |
| Directivity | 7.74 dBi | 6.18 dBi |
| Realized gain | 7.58 dBi | 4.68 dBi |
| Main lobe | θ = 0° (broadside) | — |
| 3 dB beamwidth | 60° (φ = 0° cut), 80° (φ = 90° cut) | — |

Loss breakdown at 33.11 GHz, as a share of accepted power: alumina 2.28%, copper 0.45%,
RO3003 0.17%. The alumina's tanδ dominates the (small) loss.

In the φ = 0° cut (the plane containing the probe) CST reports a secondary lobe within
1 dB of the main lobe; the φ = 90° cut has none. This probe-side asymmetry is expected
from a single off-axis feed but should be checked visually in the 3D pattern.

## 4. Which mode is excited

E and H field probes at the sphere centre (0, 0, 1.64 mm):

| | 25.1 GHz | 33.11 GHz |
| --- | --- | --- |
| E (V/m), x / y / z | 2504 / 1 / 1169 | 9272 / 3 / 3889 |
| H (A/m), x / y / z | 0.002 / 39.9 / 0.001 | 0.015 / 144.7 / 0.026 |
| η0·H/E (magnitudes) | 5.9 | 5.5 |

How to read this: a pure magnetic-dipole (TE1q1) mode has H at the centre and **zero**
E there; a pure electric-dipole (TM1q1) mode is the reverse. For reference, a plane wave
inside the alumina gives η0·|H|/|E| = √10.5 ≈ 3.2.

- **H is entirely along y.** That is a magnetic dipole oriented along y — the horizontal
  TE1q1 component that Step 1 predicted a probe on the x axis would drive, and the
  orientation that radiates well above a ground plane.
- **E at the centre is large too** (mainly along x, with a z part). A pure TE1q1 mode
  would have none, so an electric-dipole contribution is also present.
- The broadside main lobe agrees: a vertical probe radiating on its own would put a
  null at θ = 0°. The radiation comes from horizontal dipoles in the sphere (y-directed
  magnetic, x-directed electric), not from the probe wire.

**Conclusion:** at 33.11 GHz the probe excites a **hybrid mode** combining the y-directed
magnetic dipole (TE1q1-type) with an x-directed electric dipole. Its frequency is above
the seated TE1q1 eigenmodes (24.8 / 27.8 / 30.3 GHz) and close to the fundamental-modes
paper's TM1q1 value (33.1 GHz). This mirrors the stripline-fed paper, whose authors also
report that their feed excites a hybrid rather than a pure Mie mode.

This matters for the project's stated scope (TE1q1). Options for the supervisor
discussion are in Section 7.

## 5. Benchmark against the stripline-fed paper

Figures for the stripline-fed paper come from the roadmap's summary; the full paper is
not yet in the repo.

| Quantity | This design (simulated) | Stripline-fed paper |
| --- | --- | --- |
| Feed | Vertical probe beside sphere | Stripline + rectangular iris |
| Resonance | 33.11 GHz | 34.5 GHz sim / 35.0 GHz meas |
| −10 dB bandwidth | 2.2% | ~3% |
| Directivity | 7.7 dBi | 11 dB |
| Peak gain | 7.6 dBi (realized) | ~10 dBi |
| Radiation efficiency | 97% | ~74% (sim) |
| Excited mode | Hybrid, magnetic + electric dipole | Hybrid, TM101-like |

The two are not like-for-like. The paper's metal package raises directivity by about
3 dB and its stripline-to-microstrip transition costs ~1 dB; this model has neither, and
its idealized discrete port has no connector loss. The comparison shows the simulation
lands in a credible range; it does not show this feed is better.

## 6. Limitations

- **Idealized feed:** a 50 Ω discrete port across a 0.02 mm gap stands in for a coaxial
  launch. A real coax pin and connector will shift the match.
- **Infinite ground:** the Zmin electric boundary acts as an infinite ground plane, so
  there is no back radiation or ground-edge diffraction.
- **No shield or package**, unlike the stripline-fed paper.
- **Grid edge:** the optimum may lie at h_p > 1.8 mm.
- **Mode identification uses two points of field data.** A full field-plot inspection or
  projection onto the Step 1 eigenmode fields would make it rigorous. The E/H field
  monitors at 33.11 GHz are saved in `single_probe_matched.cst` for this.

## 7. Implications for Phase 3 and decisions needed

- **Geometry for N = 4 is feasible.** Four probes at 1.70 mm radius, 90° apart, 1.80 mm
  tall, clear the sphere and each other. Because each probe stands close to the sphere,
  port-to-port coupling may be strong; the 4 × 4 S-matrix in Phase 3 will show it.
- **Phase 3 reference:** use this design's 7.58 dBi realized gain and 97% radiation
  efficiency as the single-element baseline for the combining-efficiency calculation.
- **Decision for the supervisor:** the project is scoped to TE1q1, but a vertical probe
  excites a hybrid mode. Options:
  1. Accept the hybrid (as the stripline-fed paper did) and continue to Phase 3.
  2. Look for a feed that isolates the horizontal magnetic dipole, e.g. a horizontal
     current element or slot under the sphere, which couples to magnetic fields rather
     than vertical E.
  3. Run both, and compare combining efficiency and polarization purity.
