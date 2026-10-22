# UNITAS: A 3D-Native World Action Model for Embodied Manipulation

## Paper record

- **Authors:** Ruixiang Wang, Yongyi Su, et al. (17 authors)
- **Venue/year:** arXiv:2610.12099v1, 2026-10-08; under review, not an accepted conference paper
- **Source:** [arXiv](https://arxiv.org/abs/2610.12099) · [local PDF](../papers/unitas-3d-native-world-action-model/paper.pdf) · [converted Markdown](../papers/unitas-3d-native-world-action-model/paper.md) · [official repository](https://github.com/DexForce/UNITAS) · [close-reading note](../papers/unitas-3d-native-world-action-model/精读笔记.md) · [detailed Chinese tutorial](unitas-3d-native-world-action-model-tutorial.md)

## Research question

Robotic control and contact require metric 3D reasoning, while video-based world action models usually predict view-dependent pixels or visual latents. Can one representation connect observations, executable actions, and action-conditioned scene change across camera views and embodiments?

## Method and key innovation

UNITAS fixes a metric frame within each interaction window. Calibrated RGB-D is back-projected into that frame for visual positional embeddings. When depth is unavailable, a learned router weights 64 candidate depths between 0.1 and 2.0 m along each calibrated ray; camera calibration is still required. Each robot gripper contributes 20 URDF-defined tracked surface points per arm, and each human hand contributes 21 MANO landmarks. A physical-time tokenizer encodes the displacement trajectory of one point into one 256-dimensional latent, using elapsed seconds rather than source frame indices.

Florence-2-large supplies visual/language features. A point dynamics expert predicts gripper/hand action flow and action-conditioned scene flow; a smaller action expert predicts executable end-effector command chunks. The model factorizes `p(A,u,S|C,q₀)=p(A|C)p(u|C,q₀)p(S|A,C)`, so the command `u` and action-point trajectory `A` can be sampled together, while scene trajectory `S` needs an action trajectory. Scene prediction also needs current 3D query coordinates. The tokenizer is reconstruction-pretrained and frozen; the main model uses rectified-flow velocity MSE for action flow, scene flow, and commands, plus spatial-position distillation at weight 0.1. Missing targets are masked. [Paper §3](../papers/unitas-3d-native-world-action-model/paper.tex)

## Data and experiments

Pretraining mixes nine sources: RoboTwin, LIBERO, VLABench, DROID, AgiBot, RoboMIND, RH20T, VITRA, and in-house W1. The paper reports 200K pretraining steps, batch size 1,024, and 64 BW1000_H accelerators with 64 GiB each. Sampling rates and horizons vary: LIBERO uses 20 Hz and 20 future intervals (1 s); RoboTwin uses 15 Hz and 20 intervals (1.33 s). Scene-flow labels are not present for all real-world sources. Exact full-dataset counts and mixture proportions are not supplied. [Appendix A](../papers/unitas-3d-native-world-action-model/paper.tex)

| Evaluation | UNITAS | Reading condition |
| --- | ---: | --- |
| LIBERO average | 99.8% | Benchmark fine-tuning after mixed pretraining; not zero-shot. Without mixed pretraining: 99.5%. |
| LIBERO-Plus | 89.1% | Benchmark perturbations; without mixed pretraining: 86.5%. |
| RoboTwin 2.0 clean/random | 92.94% / 93.04% | Benchmark-specific evaluation. |
| Real books / ball-and-zipper tasks | 18/20 / 16/20 | 90% / 80%; mean 85%. |
| Action-conditioned RoboTwin scene prediction | Moving ADE 0.427 cm; static ADE 0.043 cm | Conditioned on recorded gripper motion; PointWorld: 0.656 / 0.084 cm. |

The introduction says 65% for Pack the Ball, but §4.3/Table 2 report 16/20 = 80%, consistent with the abstract's 85% two-task mean. Use the trial counts. In a LIBERO-Plus ablation without mixed pretraining, scene supervision raises overall success only from 85.74% to 86.47% (+0.73 percentage points); removing 3D visual PE, action-flow supervision, or history lowers it to 81.35%, 78.89%, or 75.92%. The depth-free policy test reaches 84.43% versus 84.68% with ground-truth-depth PE using the same checkpoint, while calibration and robot state remain available. [Tables 1–4, 9](../papers/unitas-3d-native-world-action-model/paper.tex)

## Limitations and reproducibility

The official repository releases checkpoints and inference/evaluation code but marks training code and datasets as forthcoming. Moreover, the paper's proposed action-only inference omits future point flows, whereas the current public `decoder.sample(decode_target="eef")` still denoises and decodes gripper action flow; it only skips scene flow. The published 55.77 ms action-only latency on an RTX 5090 D should therefore not be assumed for that public path without measurement. Real-world scene forecasts are largely qualitative and condition on observed gripper trajectories. Calibration error, occlusion, point correspondence, and sparse real scene-flow labels limit transfer. [Official README](https://github.com/DexForce/UNITAS), [public decoder](https://github.com/DexForce/UNITAS/blob/main/src/unitas/models/decoder.py)

## Application to My Robot

**Integration idea:** Start with world-aligned visual position embeddings and 20 tracked gripper-surface points in an existing policy; compare RGB-only, 3D grounding, and an auxiliary action-flow objective on an insertion or ball-in-bag task before adding scene prediction. **Required sensors/compute:** Synchronized multiview RGB-D, calibrated camera intrinsics/extrinsics, URDF, joint/end-effector state, and timestamped controls. Measure released-checkpoint VRAM and per-chunk latency on target hardware; world prediction needs 3D scene queries. Full reported pretraining used 64 large accelerators. **Expected benefit:** More stable metric alignment under viewpoint changes and optional action-conditioned scene forecasts. **Risks:** Hand-eye calibration drift, occluded or mismatched points, absent real scene-flow ground truth, and deployment latency that differs from the paper's optimized action-only measurement.

## Question Analysis

The current request asks for a full analysis in the previous close-reading style. The [close-reading note](../papers/unitas-3d-native-world-action-model/精读笔记.md) and [detailed tutorial](unitas-3d-native-world-action-model-tutorial.md) contain the six-stage walkthrough, two-step example, and paper/code discrepancy. Append later paper-specific questions here.
