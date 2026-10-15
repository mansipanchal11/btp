# Parameters and Materials

Values marked **(open)** are not yet fixed — see [05-open-questions.md](05-open-questions.md).

> **Naming note:** the "fundamental modes of a spherical DR at mmWave" paper (the one
> referred to as "Paper 1" when this file was last updated) is what the roadmap calls
> **Paper 2** — it's mode-characterization only, with a single microstrip-fringing feed,
> not a probe. The roadmap's **Paper 1** (stripline-fed DRA with assembly features,
> the iris/via-fence/Wheeler-cap design) is not attached yet. Values below are cited by
> content, not by number, to avoid repeating that mix-up.

## Materials

| Component | Material | epsilon_r | Loss | Source |
| --- | --- | --- | --- | --- |
| Sphere | Alumina | 10.5 | tan-delta ~1e-3 | Fitted from the fundamental-modes paper's WR-28 waveguide transmission test - the most trustworthy of the two papers' values since it's a direct measurement fit, not a catalog figure |
| Substrate + supportive layer | Rogers RO3003 | 3.0 | tan-delta = 0.001 | Fundamental-modes paper; matches the material already loaded/validated in the CST tutorial baseline |
| Feed metallization | Copper | - | sigma ~5.8e7 S/m | Standard annealed copper, matching the tutorial baseline's material |
| Shield/package | Metal (copper or aluminium) | - | Use real conductivity, not PEC, if conductor-loss/efficiency numbers matter | Roadmap Part G |

CST already has "Rogers RO3003 (loss free)" and "Copper (annealed)" in its library from
the tutorial baseline - reuse those definitions. Alumina will need a **custom** material
entry, since the library's "Alumina (99.5%) (lossy)" (epsilon_r = 9.9, tan-delta = 1e-4,
used in the baseline) does not match the fitted Ka-band value (10.5, ~1e-3) closely
enough to skip re-defining it.

## Sphere and target frequency

| Parameter | Value | Meaning |
| --- | --- | --- |
| Sphere diameter | 3 mm (radius 1.5 mm) | Proven, commercially available size (Goodfellow Cambridge Ltd.) |
| Target TE1q1 frequency | ~28-33 GHz | Fundamental-modes paper: TE1q1 zero at 28.5 GHz (WR-28 waveguide test), 33.02 GHz (on-chip parallel-plate prototype, Q~2352); TM1q1 companion at 33.1 GHz (waveguide) / 34.47 GHz (parallel-plate, Q~1363) |
| Size parameter x = 2.pi.r/lambda | ~0.95 at TE1q1 resonance | Governs which Mie mode dominates (Roadmap Part B) |

## Feed geometry

> **Update 2026-10-15:** the probe defaults below never matched. The swept, matched
> values are probe radius 0.15 mm, feed-circle radius **1.70 mm** (beside the sphere,
> not under it), probe height **1.80 mm** — see
> [07-probe-sweep-results.md](07-probe-sweep-results.md).

The fundamental-modes paper's on-chip prototype gives real dimensions for its single
**microstrip-fringing** feed - useful as scale references even though it isn't a probe.
Nothing in either reference paper documents an actual probe feed, so probe-specific
values below are engineering defaults, not paper data - flagged accordingly.

| Parameter | Value | Source |
| --- | --- | --- |
| Substrate/supportive-layer thickness | 0.14 mm | Fundamental-modes paper's on-chip prototype - this layer does double duty as both the RF substrate and the sphere's supportive/alignment layer |
| Seating crate (alignment hole) diameter | 0.4 mm | Fundamental-modes paper - notably smaller than our tutorial baseline's full-cross-section seating-hole formula would give, since it reads as a small locating dimple rather than a hole sized to the sphere's contact circle |
| Reference feed-to-crate gap (microstrip fringing) | 1.5 mm | Fundamental-modes paper's single feedline - the coupling gap for *fringing* excitation; a direct probe would couple much closer, so this is an upper bound, not a probe default |
| Reference feed line width (50 ohm on 0.14 mm RO3003) | 0.125 mm | Fundamental-modes paper |
| N (feed count) | 4 (starting point) | Roadmap's standard sequential-rotation starting point; trade off vs. PCB area and feed-network loss left for a later link-budget pass |
| Azimuthal spacing | 360/N = 90 deg for N=4 | Fixed once N is fixed |
| **Probe diameter** | **0.3 mm (default estimate)** | No paper precedent (both references use fringing feeds, not probes); scaled to sit between the paper's 0.125 mm line width and 0.4 mm crate diameter, roughly a small mmWave connector pin size - needs validation via parameter sweep |
| **Probe insertion depth** | **0.14 mm (default estimate, = substrate/supportive-layer thickness)** | No paper precedent; starting point is a probe reaching from the ground plane through the supportive layer to just beneath the sphere - sweep from here |
| **Feed circle radius** | **~0.6 mm (default estimate = crate radius 0.2 mm + ~0.4 mm coupling gap)** | No paper precedent; gap chosen smaller than the paper's 1.5 mm fringing gap since a probe couples more directly - this is the least-confident number in this table and the first candidate for a parameter sweep once geometry is in CST |

## Simulation parameters (to define in CST once geometry is fixed)

| Parameter | Draft value | Notes |
| --- | --- | --- |
| Frequency sweep | 25-40 GHz | Wide enough to see impedance bandwidth with margin, per roadmap Part G step notes |
| Units | mm, GHz, s | Same convention as the tutorial baseline |
| Port type | Discrete port per probe (start here) | Simpler and faster than modelling the physical coax connector; revisit if connector effects matter later |

## What's fixed vs. still a default — summary

**Fixed (paper- or tutorial-sourced):** substrate material and thickness (0.14 mm RO3003),
alumina epsilon_r/tan-delta (10.5 / ~1e-3), sphere diameter (3 mm), target band (Ka-band),
seating-crate diameter (0.4 mm), feed metallization.

**Default, not yet validated:** N (4), probe diameter (0.3 mm), probe insertion depth
(0.14 mm), feed circle radius (~0.6 mm), port type (discrete). All four of the probe/feed-
circle defaults are first-pass estimates specifically because neither reference paper uses
a probe feed - see [05-open-questions.md](05-open-questions.md) for what to re-check once
CST geometry exists.
