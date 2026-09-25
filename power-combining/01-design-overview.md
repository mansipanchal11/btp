# Design Overview — Multi-Feed Power Combining

> **Naming note:** "Paper 1" and "Paper 2" below follow the roadmap's own numbering
> (Paper 1 = stripline-fed DRA with assembly features, not yet attached; Paper 2 = the
> attached fundamental-modes/mode-characterization paper). Values now resolved from
> Paper 2 are recorded in [02-parameters-and-materials.md](02-parameters-and-materials.md)
> and [05-open-questions.md](05-open-questions.md).

## Objective

Validate that N microstrip/coax probe feeds, arranged symmetrically around one spherical
dielectric resonator (DR) and driven with **equal amplitude and equal phase**, combine
coherently into a single TE1q1-mode radiating structure — before any CP phasing is
introduced. This is Roadmap Phase 2→3 (Part I timeline): single-probe baseline, then
extend to N=4.

Success here is the prerequisite for Part 2 (circular polarization): sequential rotation
only makes sense once plain equal-phase combining is shown to work and is understood
quantitatively.

## Scope boundary — what's in and out

**In scope (this phase):**
- Bare-sphere eigenmode characterization (confirm TE1q1 lands in the target band)
- A single-probe-fed baseline, benchmarked against Paper 1's reported numbers
- Extension to N=4 probes, **equal amplitude, equal phase**
- Power-combining gain vs. a single-element baseline (Part D metric)
- Mode-purity check (does the fed structure still look like natural TE1q1, or has it
  drifted into an uncontrolled hybrid mode)

**Out of scope (deferred to `circular-polarization/`):**
- Sequential-rotation phase stepping (360°/N per feed)
- Axial ratio, RHCP/LHCP sense
- The N-way phase-shifting network (only the equal-phase N-way divider tree is needed here)
- Aperture/stripline-iris feed variant (documented as a later comparison, per Roadmap
  Part F table — probe feeds are the primary path here per the stated preference)

## Design choices carried over from the roadmap

| Decision | Choice | Source |
| --- | --- | --- |
| Feed style | Direct coax/probe feed | Roadmap Part F, stated preference: faster CST iteration, fewer coupled effects |
| Starting N | 4 | Roadmap Part F/I: standard sequential-rotation starting point, 90° steps, manageable feed network |
| Target band | Ka-band, ~28-40 GHz | Both reference papers; sphere's TE1q1 resonance |
| Sphere | Alumina, small diameter (see Section 2) | Papers 1 & 2 |
| Substrate | Rogers RO3003 | Same as both papers; same material already validated in the CST tutorial baseline |

## Why eigenmode-first

Both reference papers, and the roadmap's own CST workflow (Part G), insist on
characterizing the bare sphere's TE1q1 frequency with **no ports and no feed structure**
before adding anything. This avoids debugging a fed, lossy, multi-port structure while
still unsure whether the sphere itself resonates where expected. It mirrors Paper 2's
parallel-plate PMC-symmetry validation method.

It also mirrors a lesson from the CST tutorial baseline: resonant frequency is sensitive
to mesh order/adaptive refinement (a coarse mesh shifted results by up to 3.4% in that
build). Locking down the bare-sphere eigenfrequency first, at full mesh accuracy, gives a
trusted reference point to detect when a *fed* structure's frequency shift is a real
loading effect vs. a meshing artifact.
