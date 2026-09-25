# Power Combining — Phase 1 Design Plan

Scope: the **multi-feed-line power-combining** half of the BTP (Prof. Utpal Dey), from
`Spherical DRA Power Combining & CP — Study Roadmap.pdf`, Parts D/F/G/H. Circular
polarization (Roadmap Part E, sequential-rotation phasing) is deliberately deferred to a
later `circular-polarization/` phase — everything here uses **equal-amplitude, equal-phase**
feeds only.

This folder holds planning only (no CST files, no code yet). Once the plan below is agreed,
build scripts and `.cst` projects for this phase will live alongside these files.

## Files

- [01-design-overview.md](01-design-overview.md) — objective, scope boundary, what carries
  over from the roadmap and from the CST tutorial baseline already built
- [02-parameters-and-materials.md](02-parameters-and-materials.md) — draft parameter table,
  materials, what's fixed vs. still open
- [03-cst-workflow.md](03-cst-workflow.md) — phased CST build/solve plan (eigenmode →
  single probe → N=4 equal-phase), solver choice, mesh/memory strategy
- [04-evaluation-metrics.md](04-evaluation-metrics.md) — what "success" means for this
  phase and how each metric is computed
- [05-open-questions.md](05-open-questions.md) — decisions needed before CST work starts
- [06-step1-eigenmode-results.md](06-step1-eigenmode-results.md) — Step 1 results: bare
  and seated sphere eigenmodes, done

## Relationship to prior work

The two-port coupled-resonator model built and solved in the project root
(`sphere_DR.cst`, `sphere_DR_sparams.csv`, and the "Spherical DRA — Design and Behaviour
Analysis" doc) was a **CST-scripting practice exercise** at a different scale (10 mm alumina
sphere, X/Ku-band ~10-13.5 GHz) — not the BTP target design. It's kept as a reference for
CST Python-API workflow, mesh/accuracy lessons, and this machine's memory behaviour,
all of which carry forward into Section 3 here. The actual BTP target is Ka-band
(~28-40 GHz) with a much smaller sphere, per the roadmap.
