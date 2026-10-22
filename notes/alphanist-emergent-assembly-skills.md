# AlphaNIST: Emergent Assembly Skills from Binary Task Rewards

## Metadata

- Authors: Octi Zhang, Iretiayo Akinola, Rosario Scalise, Mateo Guaman Castro, and 11 others
- Affiliations: NVIDIA and University of Washington
- Venue/year: arXiv:2610.13354v1, 2026; the arXiv comment says “ICRA,” without an acceptance claim
- Source: [arXiv](https://arxiv.org/abs/2610.13354) · [official project and videos](https://alpha-nist.github.io/)
- Local: [PDF](../papers/alphanist-emergent-assembly-skills/paper.pdf) · [converted Markdown](../papers/alphanist-emergent-assembly-skills/paper.md) · [close-reading notes](../papers/alphanist-emergent-assembly-skills/精读笔记.md) · [detailed Chinese tutorial](alphanist-emergent-assembly-skills-tutorial.md)
- Code: the official project said “Code Release soon” when checked on October 14, 2026.

## Research Question

Can one reinforcement-learning policy discover precision assembly and multi-part coordination from complete-task success alone, rather than demonstrations, predefined skills, task decomposition, or dense progress rewards? The benchmark has 20 heterogeneous assembly pairs on NIST Assembly Task Board #1, including tight-fit pegs, gears, threaded nuts, and connectors. See paper §§I–III in the [local source](../papers/alphanist-emergent-assembly-skills/paper.tex).

## Method and Key Innovation

AlphaNIST combines a cached bank of `(assembly identity, reset state)` pairs covering loose, in-hand, near-mating, and partially assembled configurations; success-guided sampling with weight `εq + √[p̂ᵢ(1−p̂ᵢ)]`; and standard shared PPO with one actor and one critic across all 20 tasks. The reset bank expands the states from which sparse reward can be discovered, while the sampler concentrates practice near each entry's current capability frontier. It does not prescribe a sequence of skills or provide action demonstrations. [Figure 4](../papers/alphanist-emergent-assembly-skills/figures/fig-04.png) and paper §IV-B.

The policy receives surface point clouds of the movable part, mating geometry, and robot, plus 30 proprioceptive/last-action values (pose 7, twist 6, joints 9, previous action 8). Separate actor and critic SimBa networks share the architecture but not parameters. The actor produces an 8D Gaussian action: seven relative joint position targets and one gripper command, at 25 Hz. There is no explicit discrete task ID; the geometry itself conveys task information. [Figure 3](../papers/alphanist-emergent-assembly-skills/figures/fig-03.png), paper §IV-D.

## Training Data and Objective

Experience is generated online in Isaac Lab, not collected from human demonstrations. A reset entry contains an assembly identity and full simulator state. One rollout step has an observation, 8D action, next observation, reward, and termination outcome; the paper does not publish a complete sample schema or a fixed point count. Each single-pair success occurs when assembly error is under 1 mm, with the success reward issued once. The actual per-step reward also subtracts a shared control cost proportional to squared action, joint velocity, and torque. Thus “binary task reward” describes the **task-completion signal**, not a strictly binary total reward. Multi-pair episodes award task success only when all active pairs are complete. [Paper §IV-C](../papers/alphanist-emergent-assembly-skills/paper.tex).

Each PPO iteration collects 32 steps per environment and trains for five epochs with four minibatches each. Experiments scale from 1K to 256K environments. The 64K-environment, 25K-iteration shared run consumed about 410 GPU-hours. See paper §IV-E and §V.

## Experiments

| Setting | Result | Scope |
| --- | ---: | --- |
| Shared sparse policy, 20 single-pair tasks, 64K environments/25K iterations | 98.2% training success | Separate sparse specialists averaged 81.4%. Figure 5. |
| Shared policy with reach and align dense shaping | 17.8% | Separate dense specialists averaged 78.3%; this tests two shaping terms at specified coefficients. Figure 5. |
| Sparse beta versus uniform reset sampling at 256K environments | 97.4% versus 84.3% | Same reset bank, evaluated on mixed resets after 25K iterations. Figure 7. |
| Ten active pairs in one episode | 84% success | Separately trained ten-pair policy; no per-pair task success reward. Table I. |

Qualitative examples include releasing and regrasping a peg near its tip, turning parts against board geometry, tapping a nut to thread it, and preparing a USB connector before completing another assembly. [Figures 8–9](../papers/alphanist-emergent-assembly-skills/figures/fig-08.png).

## Limitations

All results are in simulation. Matched robot speed and torque limits do not establish robustness to real perception noise, contact-model error, or latency. The paper demonstrates up to ten active pairs in one episode, not all twenty at once. The 98.2% training result and 97.4% scaling evaluation use different settings and should not be conflated. Official code had not been released by October 14, 2026, so architectural and optimizer details cannot be cross-checked against an implementation. See paper §VI.

## Application to My Robot

Start with one part-and-mate assembly in a high-throughput contact simulator. Build valid reset states from loose part to partial insertion, use complete assembly as the task signal plus hardware-relevant control costs, and compare uniform and success-guided reset sampling while tracking success by reset family. A physical test needs a depth sensor or reliable point cloud, joint and gripper sensing, completion detection, and enforced speed/torque limits. The expected benefit is fewer scripted stages and more adaptive contact handling. Main risks are costly reset construction and GPU simulation, inaccurate contact physics, occluded point clouds, and sim-to-real failure. Validate a single assembly on hardware before moving to multi-pair sequencing.
