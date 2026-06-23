# Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models

## Metadata

- Authors: Haoqi Yuan, Zhixuan Liang, Anzhe Chen, Ye Wang, Haoyang Li,
  Pei Lin, Yiyang Huang, Zixing Lei, Tong Zhang, Jiazhao Zhang, Jie Zhang,
  Jingyang Fan, Gengze Zhou, Qihang Peng, Chenxu Lv, Xiaoyue Chen, An Yang,
  Fei Huang, Junyang Lin, Dayiheng Liu, Jingren Zhou, Chenfei Wu,
  Xiong-Hui Chen
- Venue/Year: arXiv, 2026
- Source: [arXiv PDF](https://arxiv.org/pdf/2606.17846)
- arXiv: 2606.17846v2, 17 June 2026
- Local PDF:
  [../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.pdf](../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.pdf)
- Converted Markdown:
  [../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.md](../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.md)
- Project page: [Qwen-RobotManip](https://qwen.ai/blog?id=qwen-robotmanip)
- Code: [QwenLM/Qwen-RobotManip](https://github.com/QwenLM/Qwen-RobotManip)

## Research Question

Qwen-RobotManip asks whether the scaling recipe that works for language and
multimodal foundation models can work for robotic manipulation. The core
problem is that robot data is heterogeneous: different embodiments use different
state layouts, action spaces, coordinate frames, sensors, cameras, and control
conventions. Without alignment, adding more data can create interference rather
than transferable skill.

The paper's answer is "alignment first, then scale." It proposes a unified
cross-embodiment representation, camera-frame end-effector actions, in-context
policy adaptation, and VL/VLA co-training so that open robot datasets, egocentric
human video, synthetic human-to-robot demonstrations, and vision-language data
can train one manipulation foundation model.

## Core Method

Qwen-RobotManip is built on Qwen3.5-4B as the vision-language backbone and a
flow-matching Diffusion Transformer action expert. The backbone processes
multi-view images, language instruction, structured embodiment prompts, and
history context. The action expert predicts continuous action chunks with 4
Euler integration steps at inference.

The state and action interface is an 80-dimensional canonical vector. It uses
two 29-dimensional per-arm blocks plus 22 reserved dimensions. Each arm block
contains joint positions, 9D end-effector pose, gripper state, and optional
dexterous hand joints. Missing dimensions are zero-padded and masked from the
loss, so single-arm, dual-arm, dexterous, mobile, and humanoid data can share one
template.

The key motion-alignment design is camera-frame delta end-effector control.
Instead of predicting robot-specific joint actions or base-frame poses, the
model expresses relative end-effector motion in a selected camera coordinate
frame. Camera positional encoding injects calibrated intrinsics and extrinsics
into the action expert. This makes visually similar motions numerically similar
across robots, which is crucial for cross-embodiment transfer.

The model also uses structured embodiment prompts with fields such as
embodiment, instruction, speed, fps, and camera-view direction. The context
variant adds recent observation-state-action chunks from the same episode, so
the policy can infer kinematic behavior from what the robot just did without
updating parameters.

The data pipeline combines robot demonstrations, egocentric human manipulation
videos, human-to-robot synthesized trajectories, and vision-language data. The
manipulation corpus totals about 38,100 hours: 3,808 hours single-arm robot
data, 6,744 hours dual-arm robot data, 868 hours mobile/humanoid robot data,
1,933 hours human egocentric video, and 24,808 hours synthesized human-to-robot
data. The Human-to-Robot pipeline retargets hands to grippers, removes human
hands from video, searches feasible robot bases, solves IK in MuJoCo, and
composites rendered robot arms into egocentric scenes across 15 dual-arm
platforms.

## Key Innovation

- Treats cross-embodiment alignment as the prerequisite for scaling robot data.
- Uses an 80D canonical state-action vector with binary masks for heterogeneous
  embodiments.
- Grounds end-effector actions in camera-frame delta poses rather than
  robot-specific joint or base frames.
- Converts egocentric human videos into robot trajectories across 15 platforms,
  producing 24,808 hours of synthetic robot demonstrations.
- Uses a rigorous curation pipeline: state/action outlier filtering, temporal
  trend alignment, FK consistency, base-frame alignment, instruction consistency,
  video-state consistency, and video quality filtering.
- Preserves VLM capabilities through dual-stream co-training with about 28M
  vision-language samples, including embodied chain-of-thought, egocentric video
  understanding, and 2D trajectory prediction.
- Introduces stronger OOD evaluation settings, including RoboTwin-IF for
  instruction following and RoboTwin-XE for zero-shot cross-embodiment transfer.

## Problems Solved

The paper attacks the main reason multi-robot pretraining often underdelivers:
heterogeneous data is not automatically useful. If two robots describe the same
physical motion in incompatible coordinates, scaling can dilute the signal. The
canonical vector and camera-frame EEF representation make diverse data more
coherent.

It also addresses the scarcity of robot data. Instead of collecting proprietary
teleoperation at huge scale, the system expands open egocentric human
demonstrations into robot-form demonstrations. This is imperfect, but it gives
the model broad visual, task, and embodiment diversity.

Finally, the paper challenges common benchmark practice. It argues that
in-domain LIBERO/RoboTwin numbers can hide whether pretraining actually helps,
so it emphasizes OOD perturbations, instruction following, cross-embodiment
transfer, and real-robot validation.

## Experiments

On in-distribution benchmarks, Qwen-RobotManip reaches 99.1% on LIBERO, 93.4%
on RoboTwin-Easy, and 92.5% on RoboTwin-Hard. The context variant reaches 99.2%,
93.7%, and 94.0%. The paper treats these as necessary but insufficient evidence.

On LIBERO-Plus, Qwen-RobotManip reaches 89.0% total success and the context
variant reaches 91.4%, compared with 84.4% for pi0.5. On RoboTwin-Clean2Rand,
the context model reaches 69.4% on the Hard joint-control setting, compared with
47.9% for pi0.5 and 20.7% for GR00T-N1.7.

On RoboCasa365, Qwen-RobotManip reaches 35.9% total success, above RLDX-1 at
33.2%, GR00T-N1.5 at 23.9%, and pi0.5 at 16.9%. Its strongest gain is on
Composite-Unseen, 14.9% versus 5.4% for the next-best baseline.

On EBench, Qwen-RobotManip reaches 45.6% overall success and a composite score
of 60, compared with pi0.5 at 27.1% and 41. It performs especially well on the
dexterous tabletop split: 50.0% success and score 70, compared with pi0.5 at
12.9% and score 32.

On RoboTwin-IF, the instruction-following benchmark, Qwen-RobotManip reaches
72.2% average success versus 49.6% for pi0.5. This is important because the
scenes contain multiple plausible actions, so the policy must actually follow
language rather than rely on visual shortcuts.

On RoboTwin-XE zero-shot cross-embodiment transfer, the EEF version reaches
23.9% average across ARX-X5, UR5-WSG, and Franka, compared with 7.5% for pi0.5
EEF and 14.5% for the Qwen-RobotManip joint-action variant. This validates the
camera-frame EEF action representation, although absolute success remains far
from solved.

Real-world ALOHA evaluation is strong. On seven in-domain CobotMagic ALOHA
tasks, Qwen-RobotManip averages 88.6% success, compared with 42.9% for pi0.5 and
20.0% for StarVLA. On four OOD ALOHA tasks with clutter, unseen objects,
spatial references, and lighting disturbance, it averages 87.5%, compared with
37.5% for pi0.5 and 0.0% for StarVLA.

For few-shot ARX ALOHA adaptation with 130 demonstrations, it improves over pi0.5
on Put Blocks, Fold Towel, and Unscrew Cap, while Insert Screw remains unsolved
at full-task level. In cross-embodiment skill transfer to ARX with no
target-task demonstrations, the full model reaches 55.0%, compared with 12.5%
without UnifiedEEF and 7.5% without UnifiedSpace.

On RoboChallenge Table30-v1 generalist track, the model reports 40% average
success, ahead of pi0.5 at 21.2%, DM0 at 16.2%, GR00T-MULTI at 7.5%, and pi0 at
7.5%.

## Ablations

The action-space scaling ablation is central. With aligned representations,
validation MSE decreases roughly log-linearly as cross-embodiment data grows
from 1% to 100%. Without UnifiedSpace, scaling is unstable, especially on
end-effector prediction. Downstream RoboTwin-C2R Hard also shows that the full
camera-frame representation scales best, reaching 50.2% joint and 56.6% EEF at
full pretraining scale.

The in-context adaptation ablation shows that structured prompts help modestly,
but execution history gives a larger gain when the action expert uses enough
denoising steps. With 10 denoising steps, the context variant reaches 70.9
average on the tested RoboTwin-Clean2Rand setting, about 5 points above the
structured prompt baseline.

Human-to-Robot data helps more than raw ego data. On RoboTwin-Clean2Rand Hard,
robot-only pretraining reaches 54.7%, +ego reaches 55.0%, and +H2R reaches
58.7%. On LIBERO-Plus, totals improve from 87.1% to 88.4% to 89.0%.

Vision-language co-training matters under harder OOD conditions. Removing VL
data from pretraining drops RoboTwin-Clean2Rand Hard from 62.6% to 54.4% and
RoboTwin-IF from 71.6% to 64.6%. Adding VL data during post-training improves
LIBERO-Plus and RoboTwin-IF further.

## Limitations

The paper is unusually broad, but several limits are explicit. Human-to-Robot
synthesis introduces retargeting approximations and visual inpainting artifacts,
so synthetic data quality is bounded by these stages. The strongest OOD
evaluation suite is still mostly simulation-based, even though the paper includes
real-robot checks.

Cross-embodiment transfer is promising but not solved. RoboTwin-XE EEF averages
23.9%, and Franka remains only 5.9%, showing that camera-frame EEF helps but
does not remove morphology, reachability, and calibration gaps.

The context model can hesitate at the beginning of an episode because its
history is zero-padded; the authors release both context and non-context
variants for this reason. The current fixed action chunk length and inference
latency also constrain tasks that need reactive sub-second control.

The system depends on calibrated cameras for camera-frame EEF actions, reliable
IK/controller mappings, and careful data curation. Reproducing the full pipeline
requires substantial engineering even if the underlying data sources are open.

## Application to My Robot

For my robot, the most transferable idea is the action interface. Use a canonical
state-action schema and express end-effector deltas in a camera or task-centric
frame whenever possible. This makes data from different arms, grippers, and
camera setups more reusable.

A practical adaptation path:

- define a fixed state/action vector with masked inactive dimensions;
- normalize joint, end-effector, gripper, and optional hand/base fields into
  stable semantic slots;
- prefer camera-frame or task-frame relative EEF actions for manipulation skills
  that should transfer across robots;
- log camera calibration, proprioception, actions, and timestamps carefully;
- add a data curation pipeline for sudden jumps, state-action lag, FK mismatch,
  instruction mismatch, and bad video frames;
- use egocentric human videos as an auxiliary source only after retargeting and
  visual alignment, not as raw action supervision;
- evaluate on OOD scenes, unseen objects, altered initial robot states, and
  instruction-following tests, not only in-domain success.

Expected benefits are better use of small heterogeneous datasets, stronger
language-conditioned control, and more robust transfer from one robot to another.
Main risks are camera calibration errors, IK infeasibility, synthetic-data
artifacts, slow inference, and overfitting to benchmark-specific simulation
distributions.

## Implementation Notes

Start smaller than Qwen-RobotManip. The minimum useful experiment is to train a
policy on two robot embodiments or two camera setups with three action
representations: raw joint actions, base-frame EEF deltas, and camera-frame EEF
deltas. Evaluate on an unseen initial pose and an unseen object layout. If the
camera-frame representation improves OOD success, then it is worth investing in
larger-scale mixed data.

For a real robot project, the highest leverage engineering task is not model
scale; it is data alignment. Build calibration checks, FK consistency checks,
state-action latency checks, and instruction/video consistency checks before
collecting more data.
