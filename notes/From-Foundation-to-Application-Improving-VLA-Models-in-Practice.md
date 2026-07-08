# From Foundation to Application: Improving VLA Models in Practice

## Metadata

- Authors: Wei Wu, Fangjing Wang, Fan Lu, He Sun, Shi Liu, Yunnan Wang, Yibin Yan, Yong Wang, Shuailei Ma, Xinyang Wang, Yibin Liu, Shuai Yang, Tianxiang Zhou, Kejia Zhang, Lei Zhou, Cheng Su, Nan Xue, Bin Tan, Han Zhang, Youchao Zhang, Fei Liao, Xing Zhu, Yujun Shen, Kecheng Zheng
- Venue/Year: arXiv, 2026
- Source: https://arxiv.org/pdf/2607.06403
- arXiv: 2607.06403v1, 2026-07-07
- Local PDF: [../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.pdf](../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.pdf)
- Local Markdown: [../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.md](../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.md)
- Project page: https://technology.robbyant.com/lingbot-vla-v2
- Code: https://github.com/robbyant/lingbot-vla-v2
- Checkpoints: https://huggingface.co/collections/robbyant/lingbot-vla-v2

## Research Question

The paper asks how a VLA foundation model can be made more useful in real robot deployment, where the robot must handle heterogeneous embodiments, richer whole-body action spaces, and dynamic long-horizon scenes rather than only clean laboratory dual-arm tasks.

## Core Method

LingBot-VLA 2.0 improves the previous LingBot-VLA system in three practical areas.

First, it scales and cleans pretraining data. The authors collect about 90,000 hours of robot data from 20 embodiments and filter it to 50,000 hours of higher-quality robot trajectories. They also build a 20,000-hour egocentric human video pool and keep about 10,000 hours after VLM filtering, reconstruction, standardization, and motion-quality checks.

Second, it uses a 55-dimensional canonical state/action vector covering arm joints, end-effector poses, grippers, dexterous hands, waist, head, and mobile-base signals. Missing body parts are padded, so single-arm robots, dual-arm robots, half-humanoids, humanoids, mobile manipulators, and egocentric hand trajectories can share one representation.

Third, the action expert uses sparse MoE layers, and the perception side adds dual-query distillation. A current query learns current geometry and temporal features, while a future query learns to predict representations at the action-chunk horizon. LingBot-Depth supplies geometric depth supervision, and DINO-Video supplies causal video features for temporal supervision.

## Key Innovation

The useful idea is not a single new module, but the system-level alignment between pretraining and deployment:

- data is filtered for robot-state/video alignment and motion smoothness;
- action representation includes whole-body degrees of freedom, not just arm or end-effector commands;
- MoE capacity is placed inside the action expert for multi-embodiment action modeling;
- future prediction is trained as a representation objective rather than requiring explicit future video generation at runtime.

This makes the paper relevant for teams trying to turn VLA models into deployable robot stacks.

## Problems Solved

LingBot-VLA 2.0 targets three practical problems:

- cross-embodiment generalization when training data comes from robots with different kinematics, cameras, hands, and policy frequencies;
- control of richer robot bodies, including head, waist, mobile base, and dexterous hands;
- temporal reasoning for long-horizon manipulation, where the model must anticipate future scene state and action consequences.

It also gives concrete engineering signals for dataset curation: reject episodes with excessive jerk, abnormal velocity or acceleration Z-scores, mostly static signals, video blur, dropped frames, multi-view misalignment, and robot-state/video mismatch.

## Experiments

On nine GM-100 bimanual tasks in a generalist mixed-training setting, LingBot-VLA 2.0 reports the best overall progress score. On Agilex Cobot Magic, it reaches 66.2% progress and 34.4% success, compared with 58.2% / 30.0% for LingBot-VLA 1.0 and 59.1% / 32.2% for pi0.5. On Galaxea R1 Pro, it reaches 34.6% / 15.6%, compared with 32.7% / 15.6% for LingBot-VLA 1.0 and 27.4% / 8.9% for pi0.5.

For long-horizon mobile manipulation, the paper evaluates Astribot S1 on sorting objects into a refrigerator and Cobot Magic-ARX X5 on stove cleaning, with 15 trials per task-setting pair. LingBot-VLA 2.0 outperforms pi0.5 in both in-domain and OOD settings. For refrigerator sorting, it reports 77.1% / 60.0% in-domain and 37.0% / 13.3% OOD. For stove cleaning, it reports 84.3% / 66.7% in-domain and 67.5% / 40.0% OOD.

The ablations are especially actionable. Relative joint targets outperform absolute joint targets, improving average success from 33.7% to 55.0%. MeanStd normalization outperforms MinMax and Q01-Q99 in the reported setup. L2 loss outperforms L1 on average, although L1 is better on a contact-rich ketchup-squeezing task.

## Limitations

The evaluation still shows a large gap between progress and full success, meaning the model often reaches partial completion but fails on final placement, release, or precise completion steps. Performance also varies strongly by embodiment: Agilex Cobot Magic performs much better than Galaxea R1 Pro, so camera viewpoint, kinematics, and action-space alignment remain difficult.

The data and infrastructure requirements are high: tens of thousands of hours of robot and egocentric data, multi-stage filtering, VLM annotation, SLAM and hand-pose reconstruction, large-scale pretraining, and teacher models for depth and video distillation. The paper does not remove the need for real robot evaluation, safety layers, or task-specific calibration.

## Practical Robotics Impact

For a real robot project, the strongest takeaway is that VLA deployment quality depends as much on data/action engineering as on model architecture. A smaller lab can adopt the principles without reproducing the full scale:

- standardize all robot data into a canonical state/action schema;
- prefer relative action targets for joint-space policies;
- use MeanStd normalization as a strong default, then verify per task;
- add future representation prediction as an auxiliary objective;
- build automatic filters for motion smoothness and video-state alignment;
- score long-horizon tasks by progress as well as binary success.

## Application to My Robot

For my robot, this paper is most useful if the platform has more than a simple arm: mobile base, waist, head camera, dual arms, dexterous hands, or multiple end-effectors. The integration idea is to define a padded canonical action vector for all controllable body parts, train a VLA policy on synchronized camera, robot state, language instruction, and action chunks, and add a future-feature prediction head during training.

Required sensors and compute include calibrated RGB cameras, robot joint and base state, synchronized action logs, enough storage for video trajectories, a GPU training setup, and preferably depth or video teacher models for distillation. The expected benefit is better transfer across tasks and robot configurations, especially for long-horizon mobile manipulation. The main risks are poor data alignment, inconsistent action conventions across embodiments, latency from an oversized model, and unsafe whole-body actions without a lower-level safety controller.

## Implementation Notes

A realistic first experiment is not to train LingBot-VLA 2.0 from scratch. Start by converting existing demonstrations into a canonical action schema and comparing:

- absolute versus relative joint targets;
- joint versus end-effector action space for each task type;
- MinMax, Q01-Q99, and MeanStd normalization;
- action-only training versus action training with future visual-feature prediction.

If relative targets plus future-feature supervision improve progress score without increasing deployment latency, then the LingBot-VLA 2.0 design direction is worth scaling.
