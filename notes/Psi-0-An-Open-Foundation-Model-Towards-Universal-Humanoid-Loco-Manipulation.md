# Psi-0: An Open Foundation Model Towards Universal Humanoid Loco-Manipulation

## Metadata

- Authors: Songlin Wei, Hongyi Jing, Boqian Li, Zhenyu Zhao, Jiageng Mao, Zhenhao Ni, Sicheng He, Jie Liu, Xiawei Liu, Kaidi Kang, Sheng Zang, Weiduo Yuan, Marco Pavone, Di Huang, Yue Wang
- Source: https://arxiv.org/pdf/2603.12263
- arXiv: 2603.12263v1, 12 Mar 2026
- Local PDF: [../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.pdf](../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.pdf)
- Converted Markdown: [../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.md](../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.md)
- Project page: https://psi-lab.ai/Psi0

## Research Question

The paper asks how to train a humanoid foundation model for long-horizon loco-manipulation without requiring massive humanoid teleoperation datasets. Its core argument is that simply co-training human and humanoid robot actions is inefficient because the two domains have different kinematics, dynamics, action frequencies, and degrees of freedom.

## Core Method

Psi-0 uses a staged training recipe. First, it pre-trains a Qwen3-VL-2B backbone on egocentric human video from EgoDex to predict next-step task-space action tokens. This stage teaches task semantics, visual representations, and human-object interaction priors. Second, it freezes the VLM and post-trains a 500M-parameter flow-based MM-DiT action expert on real humanoid data, predicting joint-space whole-body action chunks. Third, it fine-tunes only the action expert on in-domain teleoperation data for each downstream task.

The deployed system has three levels: a VLM backbone, an action expert, and an RL lower-body controller. The action space includes dexterous hand joints, arm joints, torso pose, base height, planar velocity, yaw velocity, and target yaw. The lower-body controller maps high-level lower-body commands to stable leg and waist joints.

## Key Innovation

- Staged learning rather than monolithic human-robot co-training.
- Human video is used to train visual and task-level priors, while real humanoid data trains precise joint control.
- MM-DiT action expert fuses vision-language features with action tokens more effectively than a naive DiT head.
- Training-time real-time chunking reduces jitter caused by inference latency.
- A practical teleoperation pipeline uses VR headset, wrist trackers, MANUS gloves, waist tracker, and foot tracker for single-operator whole-body data collection.

## Problems Solved

Psi-0 targets humanoid loco-manipulation, where the robot must combine locomotion, torso motion, dexterous hands, and long-horizon task execution. The work addresses three practical bottlenecks: expensive humanoid teleoperation data, unstable direct transfer from human videos, and action discontinuities caused by large-model inference latency.

## Evidence

The paper reports strong real-world performance on eight long-horizon Unitree G1 tasks involving grasping, placing, pushing, wiping, pouring, rotating, squatting, walking, and dual-arm carrying. It claims an average overall success rate at least 40% higher than the second-best baseline, GR00T N1.6, while using about 800 hours of human egocentric video and 30 hours of robot data.

Ablations show the staged recipe matters. On a three-stage dual-arm task, a naive DiT action head without pretraining or post-training gets 0/10 overall success; adding MM-DiT improves to 2/10; EgoDex pretraining improves to 6/10; adding Humanoid Everyday post-training improves to 8/10; adding real-time chunking improves to 9/10.

## Limitations

The results are real-world but limited to one humanoid platform, Unitree G1, with Dex3-1 hands. The authors note that compute and time prevented scaling to larger human-video and robot datasets. Hardware payload limits also restrict possible manipulation behaviors. The method still requires substantial infrastructure: 64 A100s for VLM pretraining, 32 A100s for action-expert post-training, and a custom teleoperation stack.

## Application to My Robot

This paper is most relevant if my robot is humanoid or mobile-manipulator-like and must combine movement, torso posture, arm motion, and hand control. The practical takeaway is to avoid forcing human video and robot joint control into one shared policy too early.

A useful adaptation path:

- use egocentric human or teleoperation videos to learn task-level visual priors;
- keep the high-level VLM separate from the low-level robot action expert;
- train the action expert directly in my robot's joint or controller command space;
- use a stable lower-body or base controller instead of expecting the VLA to output every low-level joint perfectly;
- implement real-time chunking or asynchronous action buffering to avoid stop-and-think jitter.

For my robot, the strongest engineering lesson is the staged separation: learn perception and task intent from scalable video, then learn precise robot actuation from smaller high-quality robot data.

## Implementation Notes

Start by defining the robot action interface before model training. For a wheeled or legged mobile manipulator, split action into hand/arm commands and base or lower-body commands. Collect a small but stable teleoperation dataset and test whether a frozen VLM plus flow/diffusion action head can imitate joint-space chunks. Real-time execution should be evaluated with latency included, because smoothness failures may only appear on hardware.
