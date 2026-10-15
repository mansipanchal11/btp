# Phase 3 Results — First-Stage Four-Probe Power-Combining Model

**Answer first.** The first-stage model of the proposed idea (one sphere, four probes)
is built and solved. The roadmap's planned first scheme, **equal-phase feeding, does not
work**: it excites the wrong mode and puts a null at broadside. Driving the probes with a
**90° phase progression (sequential rotation)** does combine power into a broadside beam.
After retuning the probes for the multi-port environment: **combining efficiency 0.975**,
**9.13 dBi** realized gain on boresight, and **+7.6 dB more EIRP than one source** (ideal
combining alone gives +6.02 dB; the rest comes from a more directive beam). That is
**+5.2 dB more EIRP than the stripline-fed paper's single-source antenna**. Bandwidth
(1.4%) is the main remaining weakness.

Files (this folder): `four_probe.cst` / `four_probe_model.py` (first-stage model),
`combine_excitations.py` (combining analysis), `four_probe_sweep.cst` /
`four_probe_sweep.py` (retuning sweep), `four_probe_tuned.cst` / `four_probe_tuned.py`
(retuned design). Data: `four_probe_*.csv`, `four_probe_tuned_*.csv`,
`four_probe_sweep_*.csv`.

## 1. Model

Same sphere, substrate and ground as Phase 2. Four copper probes (radius 0.15 mm) at 0°,
90°, 180° and 270° on a feed circle, each fed by a 50 Ω discrete port. Every port was
excited in turn (full 4 × 4 S-matrix, per-port farfields); combined excitations were then
formed in CST by superposition with set amplitudes and phases.

Three schemes, all equal amplitude:

| Scheme | Port phases | Mode it drives | Expected beam |
| --- | --- | --- | --- |
| Equal phase (roadmap Phase 3) | 0, 0, 0, 0 | Azimuthally symmetric (m = 0) | Null at broadside |
| Sequential rotation | 0, 90, 180, 270 | Rotating dipole (m = +1) | Broadside, circular polarization |
| Push-pull pairs | 0, 0, 180, 180 | Two crossed dipoles in phase (m = ±1) | Broadside, slant-linear polarization |

The reason equal phase fails is symmetry. Each probe on its own radiates broadside with
its field pointing along its own azimuth. Opposite probes (0° and 180°) therefore produce
opposite fields at boresight, and in-phase feeding cancels them.

## 2. First-stage results (matched single-probe geometry reused: r_f 1.70 mm, h_p 1.80 mm)

**Coupling between probes is strong.** At 33.1 GHz: adjacent probes −10.6 dB, opposite
probe −14.4 dB. With its neighbours present (and terminated), a probe that was matched to
−22.7 dB on its own now sees only −5.6 dB.

Combined results at 33.1 GHz (single-probe reference: 96.6% total efficiency, 7.58 dBi):

| Scheme | Power accepted | Total efficiency | Combining efficiency | Peak realized gain | Boresight gain | Beam | EIRP vs 1 source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Equal phase | 5.1% | 4.1% | 0.04 | −7.8 dBi | −47.8 dBi | Toward horizon | −9.3 dB |
| Sequential rotation | 87.9% | 85.2% | 0.88 | 7.79 dBi | 7.79 dBi | Broadside, 65° wide | +6.23 dB |
| Push-pull pairs | 87.9% | 85.3% | 0.88 | 7.79 dBi | 7.79 dBi | Broadside, 65° wide | +6.24 dB |

- **Equal phase** is matched only near 36.0 GHz (active −20 dB, 35.5–36.7 GHz), which is
  the m = 0 mode, and even there symmetry forces a broadside null.
- **Sequential rotation and push-pull** accept the same power (both are m = 1 drives;
  they differ only in polarization). Peak gain lands exactly at boresight.
- **The catch:** the active match under sequential rotation peaks at only **−9.1 dB at
  33.27 GHz**, with no −10 dB bandwidth at all. Combining efficiency falls to 0.55 and
  0.73 just 0.6 GHz either side.

## 3. Gaps and shortcomings of the first-stage model

| # | Gap | Evidence | Consequence |
| --- | --- | --- | --- |
| G1 | The roadmap's equal-phase scheme drives the wrong mode | Boresight −47.8 dBi; 4% combining efficiency at 33.1 GHz | Phase 3 must use an m = 1 drive, not equal phase |
| G2 | Mutual coupling detunes each probe | Adjacent −10.6 dB; embedded S11 −5.6 dB vs. −22.7 dB isolated | Active match −9.1 dB; 12% of power reflected |
| G3 | Very narrow combining bandwidth | No −10 dB active band; efficiency 0.55 at ±0.6 GHz | Sensitive to fabrication tolerance and sphere εr |
| G4 | Element gain below the reference paper | 7.8 dBi vs. ~10 dBi | Paper's metal package adds ~3 dB directivity; this model has none |
| G5 | Feed network not modelled | Ideal discrete ports | A real 4-way divider plus phase lines will add loss (roughly 0.5–1 dB at Ka-band, not yet simulated) |
| G6 | Infinite ground plane | Zmin electric boundary | No ground-edge diffraction or back radiation |

## 4. Improvement ideas

| Idea | Targets | Effort | Status |
| --- | --- | --- | --- |
| Drive the m = 1 mode (sequential rotation or push-pull) instead of equal phase | G1 | None (change of phases) | **Done** — Section 2 |
| Retune probe radius and height for the *active* impedance under m = 1 drive | G2, G3 | Low | **Done** — Section 5: −9.1 → −15.9 dB, combining efficiency 0.88 → 0.975 |
| Use sequential rotation in the feed network: reflections from the four probes return with 0°/180°/360°/540° round-trip phase and cancel at the common input | Input match, G3 | Medium (feed-network design, Phase 5) | Idea |
| Metal cavity or shield around the sphere, as in the stripline-fed paper | G4 | Medium | Idea |
| Use the lower, low-Q m = 1 resonance near 22.8 GHz (active −11.3 dB, 0.9 GHz band, 4%) for a wider band, or a lower-εr sphere | G3 | Medium; moves off the Ka-band target | Idea, needs a pattern check |
| Decoupling: parasitic posts between probes, or N = 2 (one push-pull pair) | G2 | Medium | Idea |
| Model the 4-way Wilkinson divider and phase lines | G5 | Medium (Phase 5) | Planned |

## 5. Improvement implemented: retuning for the active impedance

The single-probe geometry was optimized for one probe on its own, but in the 4-probe
model each probe sees its neighbours. Under m = 1 drive, the 4-fold symmetry makes the
active reflection at every port equal to **Γ = S11 − S13**, so it can be computed from
one excitation. A 12-point sweep of feed radius and probe height:

| Feed radius r_f | h_p = 1.60 | 1.80 | 2.00 | 2.20 mm |
| --- | --- | --- | --- | --- |
| 1.70 mm | −7.6 dB | −9.4 | −10.4 (0.14 GHz) | −10.9 (0.23 GHz) |
| 1.85 mm | −5.1 | −8.7 | −13.4 (0.41 GHz) | −20.1 (0.47 GHz) |
| 2.00 mm | −4.2 | −7.9 | −16.3 (0.50 GHz) | **−21.5** (0.45 GHz) |

(best active reflection in 28–38 GHz; −10 dB active bandwidth in brackets)

In the array, moving the probes **farther out and taller** helps — the opposite of the
single-probe trend — because the extra distance weakens neighbour coupling while the extra
height restores coupling to the sphere. r_f = 2.00 mm, h_p = 2.00 mm gives the widest
band and was verified with a full 4-port solve:

Passive coupling after retuning: adjacent −11.4 dB, opposite −19.1 dB at 33.72 GHz.
Under sequential-rotation drive the active match is **−15.9 dB at 33.70 GHz**, with a
−10 dB active band of **33.50–33.99 GHz (1.4%)**.

| Sequential rotation (push-pull identical) | 33.52 GHz | 33.72 GHz | 34.02 GHz |
| --- | --- | --- | --- |
| Power accepted | 92.1% | 97.4% | 89.2% |
| Radiation efficiency | 95.8% | 96.7% | 97.7% |
| Total efficiency | 88.2% | 94.2% | 87.1% |
| Combining efficiency | 0.91 | **0.975** | 0.90 |
| Realized gain (boresight = peak) | 8.92 dBi | **9.13 dBi** | 8.49 dBi |
| 3 dB beamwidth | 63° | 64° | 66° |
| EIRP vs. 1 source | +7.4 dB | **+7.6 dB** | +6.9 dB |
| EIRP vs. stripline-fed paper | +4.9 dB | **+5.2 dB** | +4.5 dB |

Against the first stage (Section 2) at its best frequency:

| | First stage | Retuned | Change |
| --- | --- | --- | --- |
| Active match | −9.1 dB | −15.9 dB | 6.8 dB better |
| −10 dB active bandwidth | none | 0.49 GHz (1.4%) | now usable |
| Combining efficiency | 0.88 | 0.975 | +0.10 |
| Realized gain | 7.79 dBi | 9.13 dBi | +1.3 dB |
| EIRP vs. 1 source | +6.2 dB | +7.6 dB | +1.3 dB |

Why EIRP beats the "ideal" +6.02 dB: combining is nearly lossless (0.975), and the four
taller probes make the beam about 1.5 dB more directive than the single matched probe
(directivity ≈ 9.4 dBi vs. 7.7 dBi). That is a property of this structure, not extra
power.

Equal phase is still unusable after retuning: its m = 0 resonance moves to 34.8 GHz and
accepts power, but boresight gain stays near −41 dBi.

## 6. Comparison with the reference paper

Neither reference paper combines power: both feed one sphere from one port. The fair
comparison is radiated power density on boresight (EIRP) for the same per-source power.

| | Stripline-fed paper (1 source) | This work, 1 source | This work, 4 sources (first stage) | This work, 4 sources (retuned) |
| --- | --- | --- | --- | --- |
| Frequency | 34.5 GHz (sim) | 33.11 GHz | 33.27 GHz | 33.72 GHz |
| Peak realized gain | ~10 dBi | 7.58 dBi | 7.79 dBi | 9.13 dBi |
| Total efficiency | ~74% (sim, radiation) | 96.6% | 85.2% | 94.2% |
| −10 dB bandwidth | ~3% | 2.2% | none (active) | 1.4% (active, 33.50–33.99 GHz) |
| EIRP vs. one source of this work | — | 0 dB | +6.23 dB | +7.6 dB |
| EIRP vs. the paper | 0 dB | −2.4 dB | +3.8 dB | +5.2 dB |

**Is our method better?**

- **Delivered power on boresight: yes.** Four sources combined in one sphere beat the
  paper's single-source antenna by +5.2 dB of EIRP. That is the capability the
  project set out to add, and neither reference paper has it.
- **Antenna gain: close, not better.** 9.1 dBi combined vs. ~10 dBi, with no metal
  package (the paper's package adds ~3 dB, so a shield should push this past 10 dBi).
- **Bandwidth: no.** 1.4% active vs. ~3%.
- **Efficiency:** better on paper, but not comparable yet. This model has ideal ports and
  no feed network, while the paper's figure includes a real transition.

## 7. Next steps

1. Re-scope roadmap Phase 3 from "equal phase" to "m = 1 drive" (sequential rotation),
   which is also Phase 4's CP architecture, so Phases 3 and 4 merge.
2. Compute axial ratio for the sequential-rotation excitation (Phase 4 metric) from the
   saved farfields.
3. Bandwidth: try the metal cavity/shield and the feed-network reflection cancellation.
4. Model the 4-way divider and phase lines so efficiency includes feed losses.
