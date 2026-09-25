# Evaluation Metrics — Phase 1

CP-specific metrics (axial ratio, RHCP/LHCP sense) are explicitly excluded here - see
`circular-polarization/` once that phase starts. Everything below is checked against the
single-probe baseline from Step 2 of the workflow, then again after the N=4 extension.

## 1. Impedance match

- S11 (and, once N=4 is built, every cross-port S_nm for isolation) below -10 dB across
  the target band.
- Report the -10 dB bandwidth as a percentage of center frequency - same convention as
  both reference papers, so results are directly comparable (Paper 1: ~3% BW).

## 2. Power-combining efficiency (the core Phase 1 metric)

Compare total radiated power (or peak realized gain) of the N=4-fed sphere against N
times the single-element baseline from Step 2:

```latex
\eta_{combine} = \frac{P_{rad}(N\ \text{feeds})}{N \cdot P_{rad}(\text{1 feed})}
```

- A ratio near 1 (equivalently, a gain increase near +10.log10(N) dB = +6.02 dB for N=4)
  indicates near-ideal coherent combining.
- Any shortfall quantifies combining loss - at this phase (equal amplitude/phase, no
  sequential rotation), the main expected loss sources are port-to-port coupling
  (imperfect isolation) and any asymmetry in probe placement, not phase/amplitude error
  from a phase network (that's a Part 2 concern).

## 3. Mode purity

Confirm via eigenmode + field monitor plots that the excited field in the N=4-fed
structure still resembles the natural TE1q1 pattern from Step 1 (near-linear H-field,
circumferential non-radial E-field - Roadmap Part B) and has not drifted into an
uncontrolled hybrid mode from feed/shield perturbation. Both reference papers flag this
as a real risk once a bare mode is loaded by feed structure.

## 4. Radiation pattern quality

E-plane and H-plane cuts, checked for symmetry and for ripples/spurious lobes. Paper 1
flagged E-plane ripples from its feed-transition leakage with a single stripline+iris
feed; watch for whether N=4 probes introduce a comparable or different pattern
disturbance.

## 5. Gain / directivity / efficiency

Peak realized gain along boresight and simulated radiation efficiency, reported the same
way as Paper 1 (~10 dBi gain, ~74% simulated efficiency, ≈ -1 dB, for their single-feed
TM-mode design) so the single-probe baseline (Step 2) is a like-for-like sanity check
before layering on the N=4 extension.

## Definition of "Phase 1 done"

All of the above measured and recorded for both the single-probe baseline and the N=4
equal-phase design, with the combining efficiency (Metric 2) and mode purity (Metric 3)
specifically called out as the two results that justify moving on to Part 2 (sequential
rotation / CP).
