# Kairos: A Regret-Aware Native World-Action Model Stack for Physical AI

## Metadata

- Authors: Kairos Team
- Venue/year: arXiv, 2026
- Source: https://arxiv.org/abs/2606.16533
- arXiv: 2606.16533v3, 3 Jul 2026
- Local PDF: [../papers/Kairos-Regret-Aware-Native-World-Action-Model-Stack-for-Physical-AI.pdf](../papers/Kairos-Regret-Aware-Native-World-Action-Model-Stack-for-Physical-AI.pdf)
- Converted Markdown: [../papers/Kairos-Regret-Aware-Native-World-Action-Model-Stack-for-Physical-AI.md](../papers/Kairos-Regret-Aware-Native-World-Action-Model-Stack-for-Physical-AI.md)
- Code: https://github.com/kairos-agi/kairos
- Model: https://huggingface.co/kairos-agi
- ModelScope: https://modelscope.cn/collections/kairos-team/kairos30

## Research Question

How should a world model for Physical AI represent, maintain, and deploy the information that matters for control over long horizons? The report argues that visual plausibility alone is insufficient: a useful model must preserve object state, contact, task progress, action consequences, failure boundaries, recoverability, and deployment uncertainty.

Kairos frames this goal through regret: learn a compressed state that retains information useful for reducing future physical cost. The report is careful, however, that its current experiments provide proxy evidence for regret-relevant capabilities rather than direct proof of lower real-robot regret.

## Core Method

Kairos is a native world-action stack with three coupled functions:

- World Understanding constructs a control-sufficient shared state from observations and language.
- World Generation predicts future visual tokens, providing physical and temporal regularization through object permanence, scene consistency, and future imagination.
- World Prediction jointly models future visual states and robot action tokens. A Video DiT and an Action DiT are coupled through mixed attention, so actions are modeled as part of future world evolution rather than as an unrelated policy head.

The architecture uses Hybrid Linear Temporal Attention. Sliding-window attention captures local motion, contact transitions, slip, and fast corrections; dilated sliding-window attention captures mid-range subtask and object-tool dependencies; gated linear attention provides persistent global causal memory for object permanence, task progress, delayed effects, and failure history. This factorization aims to support multi-timescale state maintenance with better efficiency than full quadratic attention.

Training follows a Cross-Embodiment Data Curriculum (CEDC):

1. Stage I, physical pretraining, learns passive physical evolution from open-world videos.
2. Stage II, embodied pretraining, uses first- and third-person human behavior plus robot-centric video to learn intentional, task-structured, instruction-aware dynamics before robot action grounding.
3. Stage III, regret-aware world-action training, uses temporally aligned robot video and action trajectories. It mines failures, recoveries, unsafe contacts, boundary cases, and prediction-versus-execution mismatches to form execution preference pairs, then combines DPO-style regret alignment with joint video/action flow-matching training.

The joint objective is described as `L_joint = L_video + λ L_action`. A shared state can therefore support counterfactual queries: from the same observation, different candidate actions should lead to different predicted outcomes.

Inference is treated as part of the model design. The stack includes proxy rollout–evaluation–refinement, prompt self-alignment, timestep distillation, token streaming, quantization, hardware-aware kernels, and operator-level parallelism. The intention is to make a world model capable of participating in an observation–action–feedback loop.

## Key Innovation

- Control-sufficient state: optimize the information needed for action and failure reasoning, rather than reconstructing every future pixel.
- Intervention-strength curriculum: organize passive video, intentional human behavior, and robot interaction as `D_obs → D_human → D_robot` instead of mixing them as flat data.
- Native world-action coupling: future video and future actions share a representation and are jointly trained.
- Hybrid temporal memory: combine local, mid-range, and persistent global pathways for long-horizon control state.
- Regret-aware preference data: failures and recoveries are useful contrastive evidence about safety margins, contact stability, recoverability, and physical cost.
- Deployment-aware co-design: latency, memory, hardware compatibility, and inference parallelism are treated as first-order modeling constraints.

## Problems Solved

Kairos addresses fragmentation between video world models, abstract latent models, and robot policies. A video model may generate plausible futures but fail to preserve task state or action consequences; a direct VLA may predict actions without explicitly modeling how the world changes; and a long-context model may still lack persistent, efficient memory.

The proposed stack also addresses the data problem. Human videos supply scalable task structure and intentional behavior, while robot data supplies embodiment, actuation limits, proprioception, execution errors, and action grounding. The curriculum is meant to reduce the amount of robot data needed to learn broad physical and task priors without claiming that human data alone solves robot control.

## Evidence

- On RoboTwin 2.0, Kairos reports 96.9 on Clean, 95.2 on Randomized, and 96.1 average, leading the average comparison in the table. MotuBrain is slightly higher on Randomized at 96.1.
- On LIBERO-Plus, Kairos reaches 89.0 average, while the jointly denoised `Kairos-joint` variant reaches 90.8. The joint variant is especially strong under language and background shifts.
- On DreamGen Bench, the 4B model reports 0.538 average physical adherence, 0.698 instruction following, and 0.618 average score, ahead of the listed baselines on average score despite being smaller than most of them.
- On PAI-Bench-Robot, Kairos-4B reports 88.59 Domain Score and 82.57 Overall Score, the best among the listed sub-10B models and close to the 16B Cosmos3-Nano result of 82.62.
- On 15-second PAI-Bench generation, Kairos reports 79.9 overall versus 77.8 for Wan2.2-5B and 77.2/76.2 for Cosmos-Predict2.5 2B/14B.
- The report gives a deployment proxy of 23.5 GB memory, 2.3 PFLOPs, and about 43 seconds on one GPU or 9 seconds on four GPUs for 720P, 5-second TI2V inference. This is substantially more practical than the larger baselines, but still not real-time robot control.
- Ablations support both human-centric pretraining and joint generation-prediction training: WorldModelBench-Robot total score rises from 9.08 to 9.25 with scaled human data and to 9.30 with a stronger VLM; removing generation supervision degrades LIBERO-Plus action performance.

## Limitations

The central claim—lower realized regret in a real closed loop—is not directly tested. The report explicitly lists missing validation for imagined-to-real rollout correlation, counterfactual action closure, failure prediction, safety filtering, recovery learning, policy improvement from imagined experience, and uncertainty calibration.

Most evidence comes from generated-video metrics, human preference evaluation, simulated WAM benchmarks, and efficiency proxies. These are useful component tests, but they do not establish that Kairos can safely rank actions or reduce collisions, slips, recovery effort, or human intervention on a physical robot.

The report is also a large technical stack with many interacting design choices. Improvements may depend on training data composition, caption quality, benchmark fine-tuning, and implementation optimizations rather than only on regret-aware state design. The 15-second long-horizon evaluation does not demonstrate stability over the much longer horizons of household tasks. Human-centric data remains morphologically different from robot execution, and the authors acknowledge that it cannot replace robot grounding.

The report has a date distinction worth recording: the arXiv record identifies v3 as 3 July 2026, while the PDF cover says “Date: July 7, 2026.”

## Application to My Robot

The most transferable idea is to build a control-information data pipeline before attempting a large world model. Keep failure, recovery, near-collision, slip, unstable grasp, and human-intervention segments instead of filtering them out. Tag them by contact, task progress, action consequence, safety margin, and recovery outcome so they can be sampled deliberately.

A practical small-scale adaptation is:

- train a video or latent dynamics model on passive robot and human first-person clips;
- add task and instruction captions that describe intended state transitions;
- introduce robot action chunks only after the visual dynamics representation is stable;
- train video prediction and action prediction jointly on synchronized robot trajectories;
- use matched success/failure or stable/unstable execution pairs for a small preference objective;
- evaluate predicted-versus-real rollouts, failure anticipation, recovery success, and action ranking before allowing imagined rollouts to influence control.

For my robot, the first useful experiment would be a LIBERO-like manipulation suite with deliberate perturbations: camera changes, object-layout changes, contact slips, and interrupted tasks. Compare a direct policy with a policy conditioned on a persistent hybrid temporal state. The required sensors are synchronized RGB or multi-view video, proprioception, action logs, and ideally force/torque or contact proxies. Deployment risks include hallucinated futures, overconfident counterfactuals, latency spikes, and unsafe action ranking; use conservative action limits, collision checking, uncertainty thresholds, and a human stop path.
