# HoloBrain-0 Technical Report

## Metadata

- Authors: Xuewu Lin, Tianwei Lin, Yun Du, Hongyu Xie, Yiwei Jin, Jiawei Li, Shijie Wu, Qingze Wang, Mengdi Li, Mengao Zhao, Ziang Li, Chaodong Huang, Hongzhe Bi, Lichao Huang, Zhizhong Su
- Venue/Year: arXiv, 2026
- Source: https://arxiv.org/pdf/2602.12062
- arXiv: 2602.12062v1, 12 Feb 2026
- Local PDF: [../papers/HoloBrain-0-Technical-Report.pdf](../papers/HoloBrain-0-Technical-Report.pdf)
- Local Markdown: [../papers/HoloBrain-0-Technical-Report.md](../papers/HoloBrain-0-Technical-Report.md)
- Project page: https://horizonrobotics.github.io/robot_lab/holobrain
- Code: https://github.com/HorizonRobotics/RoboOrchardLab

## Research Question

HoloBrain-0 asks how to turn VLA foundation-model research into a deployable robot manipulation system. The paper targets three connected problems: cross-embodiment generalization, high-quality data collection under realistic budgets, and low-latency deployment on real robots.

The main claim is that a VLA policy should not treat robot hardware as an implicit nuisance variable. Instead, the model should directly use camera calibration, depth, and robot kinematics as structural priors.

## Core Method

HoloBrain-0 is a full VLA stack with three main pieces.

First, the model uses a VLM backbone for visual and language semantics. The paper reports two variants: HoloBrain-0-GD with GroundingDINO Tiny, about 0.2B total parameters, and HoloBrain-0-QW with Qwen2.5-VL-3B trimmed to about 1.1B total parameters.

Second, a perspective-aware Spatial Enhancer injects geometry. It uses multi-view RGB-D observations, camera intrinsics, and camera extrinsics to project visual features into a shared 3D coordinate system. The paper shifts the projection reference to a central fixed camera frame rather than each robot base frame, which makes mixed robot and egocentric human data easier to align.

Third, an embodiment-aware Action Expert models the robot kinematic chain. It represents each joint with 6D pose information, masks most raw joint angles to avoid embodiment-specific conventions, and predicts a hybrid relative action space: joint residuals plus Cartesian pose displacement for each joint. The Action Expert uses joint-graph attention and diffusion-style action generation with x-prediction.

For deployment, the paper introduces SimpleRTC and teacher-forcing training to support asynchronous inference. This is meant to avoid the pause-and-go behavior that appears when a robot waits for an entire new action chunk before continuing motion.

## Key Innovation

The strongest idea is explicit embodiment modeling inside the VLA pipeline. Many VLA systems learn from mixed robot data by relying on text prompts, heterogeneous encoders, or a shared action format. HoloBrain-0 instead exposes the physical structure: calibrated cameras, depth, URDF-style kinematic chains, joint poses, and relative SE(3) actions.

The second important contribution is the test-driven data strategy. Rather than only collecting more full demonstrations, the team repeatedly evaluates the deployed policy, clusters failures, and collects targeted recovery or state-expansion data. This is especially relevant for long-horizon deformable-object tasks where random extra demonstrations can be expensive and low yield.

The third contribution is RoboOrchard, the released infrastructure for data acquisition, validation, training, packaging, and deployment. The paper emphasizes MCAP logging, Arrow-based training data, model artifacts that contain deployment context, and synchronous/asynchronous inference modes.

## Problems Solved

HoloBrain-0 addresses cross-robot training by making camera geometry and kinematic structure first-class inputs. This is useful when training data comes from multiple manipulators, dual-arm systems, mobile/humanoid platforms, simulation, and human demonstrations.

It reduces deployment friction by keeping the action expert small. HoloBrain-0-GD has 183.70M total parameters and 74.81M trainable parameters; HoloBrain-0-QW has 1080.86M total parameters and 412.17M trainable parameters. The paper argues this makes edge deployment more practical than larger VLA baselines.

It also tackles data inefficiency. The pretraining corpus contains more than 156M frames and over 3,500 hours across seven embodiments, but the real-world post-training protocol is designed to get strong task performance from targeted data such as about 30 hours per long-horizon task.

## Evidence

On real dual-arm Piper robot tasks, HoloBrain-0-QW reaches 77.18% average success over 10 tasks, compared with 69.16% for pi0.5 and 45.39% for pi0. HoloBrain-0-GD reaches 74.81% average success. The largest gains are on long-horizon tasks: HoloBrain-0-QW reports 75.00% success on fold clothes and 95.00% on fold paper box.

On RoboTwin 2.0 across 50 tasks, HoloBrain-0-GD reports 91.30% clean and 90.80% randomized success. HoloBrain-0-QW reports 91.90% clean and 92.30% randomized success, outperforming listed baselines including pi0.5, X-VLA, Lingbot-VLA, and Motus on average randomized success.

On standard LIBERO, HoloBrain-0-QW reports 97.4% average success, near top listed methods. On zero-shot LIBERO-Plus, HoloBrain-0-GD reports 74.0% average, higher than OpenVLA-OFT at 69.6% and X-VLA at 69.7% in the paper's table.

On GenieSim 2.2, HoloBrain-0-QW reports a total progress score of 4.685, slightly above X-VLA at 4.541.

The ablations show that co-training seven basic tasks with Grasp Anything raises average success from 72.40% to 75.00%. The SimpleRTC and teacher-forcing analysis indicates that asynchronous inference can reduce pauses and improve cloth-folding performance.

## Limitations

The method depends on good calibration and kinematic metadata. If camera extrinsics, depth, URDFs, or joint-pose projections are wrong, the same explicit priors that help generalization can inject systematic error.

The paper is a technical report for a large system, so some improvements combine architecture, data scale, data cleaning, post-training, and infrastructure. It is hard to isolate how much each component contributes beyond the reported ablations.

Instruction following is still listed as future work, especially for easily confused commands. The paper also focuses on imitation learning and proposes off-policy reinforcement learning as a next step, which suggests current policies may still struggle with recovery and long-tail failures outside the collected demonstrations.

## Application to My Robot

HoloBrain-0 is most useful if my robot has multiple cameras, a known kinematic chain, and manipulation tasks where geometry matters. The practical adaptation path is:

- keep accurate camera intrinsics and extrinsics for every view;
- maintain a clean URDF or equivalent kinematic description;
- log RGB-D, proprioception, language/task labels, and action trajectories together;
- add a data validator that reprojects joint/link poses into camera images to catch bad calibration or bad labels;
- train a policy that consumes 3D-aware visual features and joint-centric robot state rather than only flat images and joint arrays;
- use targeted post-training data collection: evaluate the robot, group failures, then collect short recovery and state-expansion demonstrations.

For my robot, the most realistic first experiment is not to reproduce the full HoloBrain-0 stack. A smaller experiment would compare a baseline imitation policy against an embodiment-aware policy on the same dataset. The key measurement should be success under camera/object perturbations, not just success on the original demonstration distribution.

Required sensors and compute are at least multi-view RGB-D cameras, calibrated camera poses, robot joint states, a URDF, and a GPU capable of training or fine-tuning a compact VLA/action expert. Expected benefits are better spatial precision, smoother long-horizon action execution, and better transfer across camera poses or robot variants. Main risks are calibration maintenance, compute cost, control safety during asynchronous execution, and hidden data-quality problems.

## Implementation Notes

Start by implementing the data layer before the model layer. The highest-leverage component is a self-contained episode format with RGB-D frames, camera parameters, robot state, actions, and instructions. Add automatic checks for missing frames, timestamp drift, camera calibration mismatch, and impossible joint/link projections.

For policy training, use the HoloBrain-0 idea as a design target: calibrated multi-view perception, explicit kinematics, and a joint-centric action decoder. If the robot already uses ROS 2, RoboOrchardLab is worth evaluating directly because it is the paper's released stack.
