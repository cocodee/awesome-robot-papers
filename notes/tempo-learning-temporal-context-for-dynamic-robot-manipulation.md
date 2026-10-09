# TEMPO: Learning Temporal Context for Dynamic Robot Manipulation

- **Authors:** Zhenyang Feng, Jimin Heo, Erik B. Sudderth, Unnat Jain (University of California, Irvine).
- **Venue/year:** CoRL 2026; arXiv:2609.16864v1.
- **Sources:** [paper](https://arxiv.org/abs/2609.16864), [project](https://tempo-robot.github.io/), [official code](https://github.com/tempo-robot/TEMPO), [TEMPO-Bench](https://github.com/tempo-robot/TempoBench).
- **Local material:** [PDF](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/paper.pdf), [converted Markdown](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/paper.md), [detailed reading notes](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/精读笔记.md).

## Research Question and Practical Problem

What temporal context does a pretrained single-frame VLA need for dynamic manipulation? The paper separates **motion ambiguity** (a snapshot gives position but not velocity) from **state aliasing** (visually similar grasp and release phases demand different actions). Catching a bottle carried by a walking person requires the first; retracting after a pour requires the second. Faster inference alone does not reconstruct either missing signal (paper §§1–3).

## Method and Key Innovation

TEMPO adds two inputs to a π0.5/VLASH policy. **TEMPO-MOT** supplies recent visual motion through a frozen SAM 2.1 Tiny encoder and short visual memory. **TEMPO-ACT** averages the previous 300 raw controls at 30 Hz into ten chronological buckets. The bucket vectors become VLM prefix tokens and an AdaRMS conditioning residual for the action expert. The paper reports roughly 2M added trainable parameters (0.08%) and keeps the action flow-matching objective (paper §4; [Figure 3](../assets/tempo/figure-3.png)).

The reference code loads three frames per camera, spaced about 0.333 seconds apart, and fuses a `64×256` SAM2 feature into the current head-camera visual tokens. A dual-arm record has a 14D state and 14D raw action (six joints plus a gripper per arm); the model predicts 16 actions, internally padded to 32 dimensions, and samples with ten denoising steps. The default data transform converts joint targets to deltas relative to current state while leaving gripper targets absolute. The action-history condition uses raw, unnormalized recorded targets (`training/config.py`, `policies/yam_dual_policy.py`, `models_pytorch/pi0_pytorch.py`).

## Training and Data

The code constructs `xₛ=sε+(1−s)a*`, regresses velocity `ε−a*` by elementwise MSE, and integrates from noise to actions. Reference configurations specify 10,000 base steps and 5,000 TEMPO steps, batch 128, and AdamW with a `5e−5` peak learning rate. Appendix B.3 reports about two hours per policy on eight RTX PRO 6000 Blackwell GPUs.

The public [TEMPO-Bench](https://github.com/tempo-robot/TempoBench) contains 257 episodes and 97,265 frames; 55,482 frames have a visible tracked object. In the actual `dynamic_handover` episode 0, frame 60 (2.000 s), the tracked bottle is at `(237.095, 200.553)` head-camera pixels with labeled velocity `(487.380, −56.580)` pixels/s. State and raw action each have 14 values. This benchmark is a useful concrete record, but its size is **not** the policy training-set size, which the paper does not fully report. The official policy repository still lists training data and trained checkpoints as pending release.

## Experiments and Evidence

| Setting                                 | Result                                     | Interpretation                                                             |
| --------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------- |
| Real Bottle Handover, 50 trials         | VLASH 38%, RTC 44%, TEMPO 74%              | Temporal inputs improve moving-object interception (Table 4).              |
| Real Drop Catch                         | RTC 80%, TEMPO 66%                         | TEMPO does not lead when reactive timing dominates (Table 4).              |
| Full, untrimmed Flick Catch / Wine Pour | Both async baselines 0%; TEMPO 68% / 97.6% | Action history helps distinguish grasp from release and retract (Table 1). |
| Handover ablation                       | ACT only 52%, MOT only 56%, both 74%       | The two temporal inputs provide complementary information (Table 6).       |
| Flick Catch velocity probe              | VLASH `R²=0.03`, TEMPO `R²=0.57`           | Motion is more decodable from the trained representation (Table 7).        |

Table 4 uses **trimmed** Flick Catch and Wine Pour tasks with the release-and-retract phase removed; Table 1 reports the full-task results. Wine Pour's percentage measures bead mass retained in the pot, not binary success. TEMPO+UVT's 87.2% four-task average also changes the output target and should not be attributed to TEMPO's inputs alone.

## Limitations and Paper–Code Differences

- Four real dual-arm tasks do not establish stable transfer across embodiments or open environments.
- Frozen SAM2 still requires online encoding. The reported 35.3 ms median policy forward time slightly exceeds a 30 Hz frame period, so real-time control depends on asynchronous execution.
- The paper depicts a separate motion token, while the released implementation adds temporal attention inside SigLIP and fuses SAM2 features into existing current visual tokens. “No backbone modification” should therefore be interpreted with care.
- The SAM2 fusion and AdaRMS residual are initially no-ops; adding ten action-history prefix positions changes attention even at initialization, as the official configuration comments state.
- TEMPO-Bench is public, but policy checkpoints and training demonstrations remain listed as forthcoming; the real-robot rates cannot yet be independently reproduced from released artifacts.

## Question Analysis

This reading covers motivation, architecture, training, a real benchmark record, information flow, two successive handover observations, and evaluation details. The [detailed notes](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/精读笔记.md) contain the worked example, figures, and code locations. Append later paper-specific questions here.

## Application to My Robot

- **Integration idea:** Log synchronized camera frames, robot state, issued controls, and execution timestamps. Add bucketed action history to an existing VLA, then a streaming visual motion cue. Compare each signal alone and together, categorizing failures by motion direction versus task-phase confusion.
- **Required sensors and compute:** At least one synchronized RGB camera, joint and gripper readings, and roughly 30 Hz control logs; the paper uses multiple views and two arms. Deployment needs compute for a frozen video encoder plus the VLA. Full reported training used eight RTX PRO 6000 Blackwell GPUs.
- **Expected benefit:** Better interception of moving objects and fewer hesitant or reversed actions across grasp, release, and retract phases.
- **Risks:** Occlusion, tracking errors, and camera latency can corrupt motion features; coarse buckets can hide fast control changes; a new embodiment needs a redefined action-history layout. Probe motion on public data first, then run closed-loop ablations on a safe local task.
