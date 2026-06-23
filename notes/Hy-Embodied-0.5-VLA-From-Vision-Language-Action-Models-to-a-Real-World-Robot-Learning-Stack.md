# Hy-Embodied-0.5-VLA: From Vision-Language-Action Models to a Real-World Robot Learning Stack

## Metadata

- Authors: He Zhang, Lingzhu Xiang, Haitao Lin, Zeyu Huang, Minghui Wang, Dingyan Zhong, Yubo Dong, Yihao Wu, Yongming Rao, Dongsheng Zhang, Wanjia He, Ling Chen, Kai Huang, Jiahao Chen, Sichang Su, Xumin Yu, Ziyi Wang, Chengwei Zhu, Xiao Teng, Yuchun Guo, Yufeng Zhang, Yuandong Liu, Rui Wang, Zisheng Lu, Han Hu, Zhengyou Zhang
- Venue/Year: arXiv, 2026
- Source: [arXiv PDF](https://arxiv.org/pdf/2606.14409)
- arXiv: 2606.14409v1, 12 June 2026
- Local PDF: [../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.pdf](../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.pdf)
- Converted Markdown: [../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.md](../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.md)
- Project page: [Hy-Embodied-0.5-VLA](https://tairos.tencent.com/openSourceModels/hy-embodied-0.5-vla)
- Code: [Tencent-Hunyuan/Hy-Embodied-0.5-VLA](https://github.com/Tencent-Hunyuan/Hy-Embodied-0.5-VLA)
- Model: [tencent/Hy-Embodied-0.5-VLA-UMI](https://huggingface.co/tencent/Hy-Embodied-0.5-VLA-UMI)
- Dataset: [tencent/Hy-Embodied-0.5-VLA-Data](https://huggingface.co/datasets/tencent/Hy-Embodied-0.5-VLA-Data)

## Research Question

This report asks how to turn a VLA policy into a deployable robot learning stack rather than a standalone model. The target problem is real-world bimanual manipulation across different embodiments, where success depends on precise data collection, continuous control, adaptation, failure correction, and low-latency execution.

The paper's core claim is that generalist robot behavior needs the whole pipeline to be co-designed: high-fidelity human demonstrations, an embodied VLM backbone, continuous flow-matching actions, cross-embodiment action representation, preference-based post-training, and asynchronous deployment.

## Core Method

HyVLA-0.5 starts from the Hy-Embodied-0.5-MoT backbone, a 4B Mixture-of-Transformers embodied VLM. It adds a 370M-parameter flow-matching action expert that predicts continuous action chunks instead of discrete action tokens. Visual, language, state, and noisy-action streams are routed through separate modality-specific computation while sharing attention for grounding.

The action interface is a relative end-effector delta chunk. For each arm, it predicts 3D translation, 6D rotation, and gripper command in the end-effector frame. This keeps the learned policy less tied to a particular robot's joint space; deployment code maps the relative end-effector targets through forward kinematics and inverse kinematics for each platform.

The data layer is Hy-UMI-10K, over 10,000 hours and more than 1M episodes of fingertip UMI demonstrations across 70 tasks. The custom grippers use optical motion capture for sub-millimeter 6-DoF labels, fingertip actuation for human haptic feedback, RGB-D capture, gripper encoders, and optional force/torque sensing. Current HyVLA-0.5 training uses RGB, while depth remains available for future work.

Training has three stages. First, pre-train on the full UMI corpus for 200K steps with 3 camera views at 224x320 and horizon 50 at 10 Hz. Second, run supervised fine-tuning with a compact memory encoder using the current frame plus five historical frames. Track A fine-tunes and evaluates on the same real robot; Track B fine-tunes only on task-specific UMI demonstrations and deploys to different robots without target-robot teleoperation. Third, FlowPRO post-training collects paired failure/correction trajectories through intervention-and-rollback and trains with RPRO, a reward-free and critic-free preference objective adapted to flow-matching policies.

Deployment uses an asynchronous producer-consumer runtime: inference produces action chunks while the robot keeps executing buffered commands. A latency-aware cubic Bezier stitcher discards stale prefixes and reconnects chunks with smooth position, orientation, and gripper transitions.

## Key Innovation

- Treats VLA deployment as a full robot learning stack, not only as model architecture.
- Scales high-precision UMI data collection with fingertip grippers, optical tracking, and optional force sensing.
- Uses a relative end-effector delta-chunk representation for cross-embodiment transfer.
- Adds compact visual memory without increasing the visual token count passed to the VLM.
- Uses FlowPRO/RPRO to turn real failure cases into offline preference updates without reward or value models.
- Makes high-capacity VLA inference usable on hardware through asynchronous execution and Bezier chunk stitching.

## Problems Solved

The system targets four practical bottlenecks. First, teleoperation is expensive and embodiment-specific, while raw human video lacks precise action labels. Hy-UMI-10K tries to preserve human manipulation diversity while recording robot-usable 6-DoF trajectories.

Second, discrete action token VLAs can be too coarse or slow for precise manipulation. HyVLA-0.5 uses continuous flow matching and action chunks to support high-frequency control.

Third, small supervised datasets often fail at last-mile dexterity. FlowPRO uses failures as contrastive negative examples and corrective interventions as positives, which gives the policy a direct push away from repeated failure modes.

Fourth, model inference latency can break closed-loop control. The asynchronous buffer and chunk stitcher keep the robot moving while new VLA chunks are computed.

## Experiments

On RoboTwin 2.0, HyVLA-0.5 reports 90.9% success in the Clean setting and 90.1% in Randomized, averaged over 100 runs per task on 50 tasks. It slightly exceeds JoyAI-RA at 90.5% and 89.3%, and is ahead of Qwen-VLA, starVLA, Motus, LingBot-VLA, pi0, and pi0.5 under the reported protocol.

Ablations show that removing compact memory reduces RoboTwin success to 88.8% / 88.6%. Removing both compact memory and UMI pre-training further reduces it to 88.1% / 87.9%. The simulation gain from UMI pre-training is modest, which the authors attribute to the domain gap between egocentric real UMI data and synthetic RoboTwin renderings.

Real-world SFT uses Track A on Dobot X-Trainer for Insert Bottles, Fold and Store Glasses, Set the Table, and Zip Up the Pen Case. Track B uses only UMI fine-tuning data for cross-embodiment deployment on JAKA K1 and Astribot S1. The paper reports clear gains from Hy-UMI-10K pre-training, especially at precision bottlenecks such as folding eyeglasses, pinching a zipper slider, placing a small hair tie, and cleaning a table with a humanoid.

For force-modality validation, the authors augment the action expert with lightweight TCN encoders for a 50-step force/torque window per hand. On Unitree G1, the policy selects the lighter box after sequential grasps, showing that fingertip force signals can become useful non-visual policy input.

For FlowPRO post-training on Dobot X-Trainer, all methods run 3 post-training rounds with the same data budget. RPRO reaches 99+/-0.6% success and 16 s completion on Bottle, 99+/-0.7% and 21 s on Cap, 98+/-0.9% and 22 s on USB, and 94+/-1.1% and 37 s on Zip. It outperforms DAgger and the pi0.6\* advantage-conditioned regression baseline on both success rate and completion time.

## Limitations

HyVLA-0.5 is still a large and complex stack. It depends on a 4B VLM backbone, a large action expert, a 10K-hour private data-collection effort, optical motion-capture infrastructure, and careful real-robot execution engineering. Smaller teams may be able to reuse released checkpoints or data, but reproducing the full pipeline is expensive.

The strongest real-world claims are task-specific post-training and cross-embodiment transfer after UMI fine-tuning, not broad zero-shot generalization. The authors explicitly leave emergent zero-shot embodied intelligence as an open direction.

The UMI setup prioritizes label precision over in-the-wild convenience. Optical tracking improves action labels but constrains collection environments. The paper also notes that egocentric UMI cameras differ from robot-mounted deployment cameras, leaving room for systematic visual augmentation.

Only RGB is consumed in the current model despite RGB-D data collection. Force is validated on one qualitative task with an added module, so force-aware general manipulation is still early.

## Application to My Robot

For my robot, the most useful idea is not to copy the whole 4B stack immediately. The practical takeaway is to standardize a robot-agnostic end-effector action interface and build the data, policy, correction, and deployment loops around it.

A realistic adaptation path:

- record demonstrations as relative end-effector deltas plus gripper state, not only joint targets;
- keep camera, proprioception, action, and language timestamps tightly synchronized;
- add short visual history for contact-rich manipulation;
- train an action-chunk policy with continuous regression or flow matching;
- deploy with an asynchronous action buffer and smooth chunk stitching;
- collect failure/correction pairs during real rollouts and use them as preference or contrastive post-training data.

Required hardware depends on ambition. The minimal version needs synchronized RGB cameras, end-effector pose estimates, gripper state, and enough compute for a chunked policy. A stronger version benefits from wrist cameras, head camera, force/torque sensing, and a reliable IK/controller layer.

Expected benefit is better precision at manipulation bottlenecks and faster iteration from failures. Main risks are dataset scale, camera-domain mismatch, IK failures under relative end-effector commands, action latency, and unsafe exploration during correction collection.

## Implementation Notes

Start with one bimanual or single-arm task that has clear failure modes, such as inserting, zipping, folding, or placing a small object. Implement the delta end-effector representation and asynchronous chunk execution first, because those pieces can improve deployment even before training a foundation-scale VLA.

For a small lab, the first experiment should compare an action-only chunk policy against the same policy with visual history and UMI-style relative end-effector targets. If that improves the precision-critical sub-steps, then add failure/correction preference data. Full FlowPRO is useful only after the base SFT policy is already competent enough to produce meaningful near-miss failures.
