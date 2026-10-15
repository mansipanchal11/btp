# Research Phases and Milestones

**Project:** Multi-feed spherical dielectric resonator antenna (DRA) at Ka-band for spatial
power combining and circular polarization
**Supervisor:** Prof. Utpal Dey
**Basis:** `Spherical DRA Power Combining & CP — Study Roadmap (1).pdf` (Parts C, F, I)

## 1. Research problem

The two reference works from the supervisor's group establish a single-feed spherical DRA:
one demonstrates a stripline+iris-fed antenna with self-aligned assembly (MAPCON 2023), the
other characterizes the sphere's fundamental TE1q1/TM1q1 modes at mm-wave (MAPCON 2022).
Neither excites one sphere from several ports at once, neither builds a radiating antenna
on the high-Q TE1q1 mode, and neither addresses polarization control.

**Research gap:** no published work excites a spherical DR from multiple ports
simultaneously to (a) combine the power of several sources in the resonator itself and
(b) synthesize circular polarization from a single TE1q1-mode sphere.

## 2. Research questions

| ID | Question | Answered in |
| --- | --- | --- |
| RQ1 | Where does the TE1q1 mode of a 3 mm alumina sphere sit at Ka-band, and how does a grounded substrate perturb it? | Phase 1 |
| RQ2 | Can a vertical probe feed excite that mode with a usable impedance match (S11 <= -10 dB)? | Phase 2 |
| RQ3 | Do N equal-phase probes combine coherently in the sphere (combining efficiency near 1, gain increase near +10 log10 N dB)? | Phase 3 |
| RQ4 | Does sequential-rotation phasing of the same N probes give circular polarization (AR < 3 dB) without losing combining efficiency? | Phase 4 |
| RQ5 | How sensitive is the design to fabrication tolerances, and can a physical feed network realize the required phases? | Phase 5 |
| RQ6 | Do measurements of a fabricated prototype agree with simulation? | Phases 6-7 |

## 3. Phases

Each phase lists its objective, method, milestone (the evidence that closes it), and
current status. Durations are suggested working weeks, not calendar dates.

### Phase 0 — Literature review and simulation methodology (≈2 weeks) — COMPLETE

- **Objective:** understand Mie-mode theory, the two reference papers, and establish a
  reliable, reproducible simulation workflow.
- **Method:** study roadmap Parts A–C; set up scripted CST Studio Suite 2025 control via
  its Python API; validate the workflow by reproducing a published tutorial model.
- **Milestone M0 (met):** tutorial two-port spherical DR model reproduced by script; 3 of 4
  reference resonances matched within 0.25% (9.957, 10.34, 13.6 GHz), the fourth within
  2.3%. Establishes that the simulation pipeline gives trustworthy resonant frequencies.
- **Methodology findings carried forward:** resonance accuracy needs 2nd-order adaptive
  tetrahedral meshing (coarse mesh shifted modes up to 3.4%); solver error reports must be
  checked against the solver log (false "out of memory" failures on this workstation).

### Phase 1 — Modal characterization (≈2 weeks) — COMPLETE

- **Objective:** answer RQ1 before any feed is designed.
- **Method:** CST eigenmode analysis of (a) the bare sphere in free space and (b) the sphere
  seated on the 0.14 mm RO3003 supportive layer over a ground plane.
- **Milestone M1 (met):**
  - Bare sphere: TE1q1 is a three-fold degenerate mode at **29.37 GHz** (Q ≈ 10.8), inside
    the 28.5–33 GHz target band.
  - Seated sphere: the ground plane splits the degeneracy into modes at **24.79, 27.82 (×2)
    and 30.26 GHz**, consistent with image theory for a dipole above a ground plane.
- **Output:** `power-combining/06-step1-eigenmode-results.md`.

### Phase 2 — Single-element excitation (≈3 weeks) — SUBSTANTIALLY COMPLETE

- **Objective:** answer RQ2 and produce the single-element reference for Phase 3.
- **Method:** discrete-port probe feed beside the seated sphere; parametric sweep of probe
  height and feed-circle radius; field monitors to confirm which mode is excited; farfield
  for gain, directivity and radiation efficiency.
- **Milestone M2:** S11 <= -10 dB at the TE1q1-family resonance, field plot confirming the
  excited mode, and gain/efficiency/bandwidth reported against the stripline-fed paper's
  figures (~10 dBi, ~74% efficiency, ~3% bandwidth).
- **Status (M2 met, with one caveat):** probes under the sphere coupled weakly (best
  −1 dB). A 15-point sweep with the probe beside the sphere found a match: feed-circle
  radius 1.70 mm, probe height 1.80 mm → **S11 = −22.7 dB at 33.11 GHz**, 2.2% −10 dB
  bandwidth, 97% radiation efficiency, 7.7 dBi directivity, 7.6 dBi realized gain,
  broadside beam. **Caveat:** centre-point field probes show a hybrid mode (y-directed
  magnetic dipole plus x-directed electric dipole), not a pure TE1q1 eigenmode — a scope
  decision for the supervisor. Details: `power-combining/07-probe-sweep-results.md`.
- **Natural checkpoint:** mid-term evaluation (single-element antenna characterized).

### Phase 3 — Multi-port power combining (≈3 weeks) — FIRST STAGE COMPLETE

- **Objective:** answer RQ3.
- **Method:** four identical probes at 90° spacing; full 4×4 S-matrix; combined
  excitations by superposition; combining efficiency against the M2 single element.
- **Re-scoped from the roadmap:** equal-phase feeding was tested and fails by symmetry —
  it drives the m = 0 mode, with a broadside null (−48 dBi at boresight, combining
  efficiency 0.04). Phase 3 now uses an m = 1 drive (sequential rotation, or push-pull for
  linear polarization), which is also the Phase 4 CP architecture.
- **Milestone M3 (met):** after retuning the probes for their active impedance
  (feed radius 2.00 mm, height 2.00 mm), sequential-rotation drive gives **combining
  efficiency 0.975**, active match −15.9 dB, 9.13 dBi realized gain at boresight, and
  **+7.6 dB EIRP over one source** (+5.2 dB over the stripline-fed paper's antenna). Open
  issue: −10 dB active bandwidth only 1.4%. Details:
  `power-combining/08-four-probe-combining-results.md`.

### Phase 4 — Circular polarization by sequential rotation (≈3 weeks) — NOT STARTED

- **Objective:** answer RQ4.
- **Method:** same four probes with 0°/90°/180°/270° excitation phases; axial ratio vs.
  frequency at boresight; sense of rotation; re-check impedance and combining efficiency.
- **Milestone M4:** AR < 3 dB bandwidth reported alongside impedance bandwidth, with CP
  sense matching the phase progression.

### Phase 5 — Tolerance study and feed-network design (≈3 weeks) — NOT STARTED

- **Objective:** answer RQ5.
- **Method:** parametric sweeps of amplitude/phase imbalance and sphere placement error;
  design a 4-way Wilkinson divider with phase-offset lines on RO3003.
- **Milestone M5:** sensitivity curves (AR and combining efficiency vs. imbalance) and a
  simulated feed network meeting the required phases.

### Phase 6 — Fabrication and measurement (time-permitting) — NOT STARTED

- **Objective:** experimental answer to RQ6.
- **Method:** fabricate on RO3003, self-aligned sphere assembly, VNA S-parameters,
  Wheeler-cap efficiency, anechoic pattern and AR measurement.
- **Milestone M6:** measured S-parameters, efficiency, pattern and AR.

### Phase 7 — Analysis and dissemination (≈2 weeks) — NOT STARTED

- **Objective:** reconcile simulation with measurement (or with the reference papers if
  Phase 6 is not reached) and report.
- **Milestone M7:** final thesis; a conference-paper draft (MAPCON-style) if results
  support it.

## 4. Milestone summary

| Milestone | Evidence | Status |
| --- | --- | --- |
| M0 Simulation methodology validated | Tutorial model reproduced within 0.25% (3 of 4 modes) | Met |
| M1 TE1q1 mode located and its ground-plane splitting explained | Eigenmode results, bare and seated | Met |
| M2 Matched single-probe antenna characterized | S11 −22.7 dB @ 33.11 GHz, 97% rad. eff., 7.6 dBi; hybrid mode identified | Met (mode is hybrid, not pure TE1q1) |
| M3 4-port combining demonstrated | Combining efficiency 0.975, +7.6 dB EIRP, 9.13 dBi (sequential rotation; equal phase shown to fail) | Met (bandwidth 1.4%) |
| M4 Circular polarization demonstrated | AR < 3 dB bandwidth, CP sense | Not started |
| M5 Tolerance study and feed network | Sensitivity curves, divider design | Not started |
| M6 Prototype measured | Measured S11, efficiency, pattern, AR | Not started (time-permitting) |
| M7 Thesis and paper draft | Written report | Not started |

## 5. Risks

| Risk | Affects | Mitigation |
| --- | --- | --- |
| Probe feeds have no precedent in either reference paper | M2 | Resolved: sweep found a matched probe geometry |
| A vertical probe excites a hybrid mode rather than pure TE1q1 | RQ2 framing, M3–M4 | Supervisor decision: accept hybrid, or try a feed that couples to magnetic field (horizontal current / slot) |
| Narrow combining bandwidth (1.4%) | M3–M5 | Metal cavity/shield; sequential-rotation feed network cancels port reflections at its input; lower-Q mode near 22.8 GHz |
| The ground plane splits TE1q1, so different feeds may excite different split modes | M2–M4 | Identify the excited mode with field monitors at each milestone |
| Workstation memory (16 GB) limits mesh density | All simulation phases | Small models, one CST session at a time, verify runs from solver logs |
| Stripline-fed reference paper not yet in hand | M2 benchmark | Obtain the full paper; until then use the roadmap's summary figures |
| Fabrication access and timeline | M6 | Phase 6 is time-permitting; M7 can close on simulation plus reference-paper comparison |
