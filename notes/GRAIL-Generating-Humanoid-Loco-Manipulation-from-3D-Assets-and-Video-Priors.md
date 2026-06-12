# GRAIL: Generating Humanoid Loco-Manipulation from 3D Assets and Video Priors

## Metadata

- Authors: Tianyi Xie, Haotian Zhang, Jinhyung Park, Zi Wang, Bowen Wen, Jiefeng Li, Xueting Li, Qingwei Ben, Haoyang Weng, Yufei Ye, David Minor, Tingwu Wang, Chenfanfu Jiang, Sanja Fidler, Jan Kautz, Linxi Fan, Yuke Zhu, Zhengyi Luo, Umar Iqbal, Ye Yuan
- Venue/Year: arXiv, 2026
- Source: [arXiv PDF](https://arxiv.org/pdf/2606.05160)
- arXiv: 2606.05160v1, 3 June 2026
- Local PDF: [../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.pdf](../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.pdf)
- Converted Markdown: [../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.md](../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.md)
- Project page: [GRAIL](https://research.nvidia.com/labs/dair/grail/)
- Code: [NVlabs/GRAIL](https://github.com/NVlabs/GRAIL)
- Dataset: [nvidia/PhysicalAI-Robotics-Locomanipulation-GRAIL](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Locomanipulation-GRAIL)

## Research Question

GRAIL asks how to scale humanoid loco-manipulation data without teleoperating the robot, rebuilding physical scenes, or collecting motion capture for every object and terrain. The paper's answer is to keep the whole data-generation process virtual until deployment.

The key hypothesis is that video foundation models are useful as human interaction priors, but only if their outputs are anchored by known 3D assets, camera parameters, metric scale, scene depth, and a character already fitted to the target humanoid.

## Core Method

GRAIL starts from a 3D object asset and a simulator-ready scene. It uses Infinigen and Blender to place the object in a known 3D configuration, renders the first frame, asks a VLM to generate an interaction prompt, and then uses a video foundation model such as Kling 2.5 Turbo Pro to synthesize a human-object interaction video.

Unlike methods that reconstruct uncontrolled internet videos, GRAIL knows the camera intrinsics, camera extrinsics, object mesh, object texture, metric scale, scene depth, and robot-proportioned human character before video generation. This privileged setup makes later 4D reconstruction less ambiguous.

The reconstruction stack estimates human motion with GENMO, refines hands with WiLoR, tracks the object with FoundationPose, aligns depth with MoGe-2 and rendered scene depth, segments with SAM2, and then jointly optimizes human and object trajectories using keypoint, projection, depth, contact, foot-contact, velocity, and smoothing losses.

The recovered human-object interaction is retargeted to the Unitree G1. GRAIL then trains task-general tracking policies on top of SONIC, a pretrained whole-body controller. For manipulation, it uses an object-aware latent adaptor that injects latent residuals and hand open/close primitives while keeping the base controller frozen. For terrain traversal and sitting, it fine-tunes a scene-aware tracker with a local height-map encoder.

Finally, the tracking policies are distilled into egocentric RGB visual policies and deployed on a real Unitree G1 through a sim-to-real pipeline with visual domain randomization and camera alignment.

## Key Innovation

- Fully digital data generation for humanoid loco-manipulation, from 3D assets and video priors to robot deployment.
- Asset-conditioned video generation: the VFM generates behavior while geometry, scale, camera, and morphology are known.
- Interaction-aware 4D HOI reconstruction that uses the known 3D configuration to reduce depth ambiguity and contact errors.
- Task-general trackers instead of one policy per sequence or object.
- Complementary controller adaptation: object-aware latent adaptation for manipulation and scene-aware height-map conditioning for terrain.
- End-to-end validation on a real Unitree G1 using only GRAIL-generated data.

## Problems Solved

GRAIL addresses a major data bottleneck for humanoids. Teleoperation and motion capture are hard to scale because every object, scene, and terrain layout needs physical setup and human effort. Pure video reconstruction is broad but underconstrained, especially for camera, scale, object geometry, contact, and world-space motion.

GRAIL combines the strengths of both: video generation supplies diverse interaction priors, while known 3D assets and scene geometry make the result reconstructable and simulator-ready.

## Experiments

The generated dataset contains more than 20,000 sequences for Unitree G1. It spans pick-up, whole-body manipulation, sitting, and terrain traversal, using 1,000 object assets and 1,000 procedurally generated terrain configurations.

For 4D HOI generation, GRAIL is compared with HOIDiff, CHOIS, and DAViD on 20 everyday objects. It achieves the best or near-best geometric quality, the highest interaction score, the smoothest object motion, and the highest physical tracking success. The tracking success rate is 88.9%, compared with 24.0% for DAViD, 15.8% for HOIDiff, and 10.5% for CHOIS.

For task-general loco-manipulation tracking, GRAIL is evaluated on 124 motions across 43 objects. The full method reaches 81.4% success, outperforming HDMI at 48.5% and ResMimic at 49.2%. Ablations show that removing SONIC, removing the object-aware adaptor, or replacing relative object observations with absolute ones all degrade success.

For real-world deployment, GRAIL trains egocentric visual policies using only generated data. On a real Unitree G1, it reports 90% success for stair climbing. For object pick-up, it trains on cube, apple, tea box, carrot, and wet wipes, achieving 84% average success on seen objects and 80% average success on unseen objects such as spray can, lint roller, peach, flashlight, and medicine bottle.

## Ablations

The reconstruction-loss ablation shows that projection, depth, and contact losses each matter. Removing any one reduces downstream tracking success from 81.4% to the 41.6-53.3% range. This is important: reconstruction metrics alone do not tell the full story; the full loss gives the best robot-tracking result even if it is not best on every proxy metric.

The controller ablation shows that accurate body imitation alone is not enough for manipulation. Vanilla SONIC tracks the body well but performs poorly on object success. The object-aware adaptor and relative object observations are key for turning human-object references into robot-executable manipulation.

## Limitations

GRAIL assumes access to usable 3D object assets, simulator-ready scenes, and a video foundation model that follows the requested interaction. If the VFM changes object appearance, produces fast motion, or creates heavy occlusion, tracking quality degrades and the filtering step discards those sequences.

The pipeline is computationally heavy. The appendix reports about 14 minutes to generate one 5-second, 121-frame 4D HOI sequence on a single A100, dominated by joint optimization. Tracker training uses 64 NVIDIA L40 GPUs with 1,024 environments per GPU for 30,000 PPO iterations, about 30 hours per full task-family run.

The task-general trackers amortize learning within related motion families, but substantial task-family changes still require training or fine-tuning. The real-world validation is strong but focused on Unitree G1, pick-up, and stair climbing, so broader cross-hardware evidence is still needed.

Licensing also matters for practical use. The released GitHub project uses an NVIDIA non-commercial license, so production or commercial reuse needs separate legal review.

## Application to My Robot

GRAIL is useful if my robot project needs diverse humanoid or whole-body behaviors but robot teleoperation data is too expensive. The practical idea is to generate training references digitally, then validate them in simulation before any real-world deployment.

For my robot, the reusable design is:

- collect or generate accurate 3D assets for objects and environments;
- render known 3D scene configurations instead of relying on uncontrolled videos;
- use a VFM to propose human-like interaction motion;
- reconstruct 4D HOI with metric depth, object geometry, and contact constraints;
- retarget to my robot's kinematic skeleton;
- train a physics tracker before training a visual policy;
- use real deployment only as the final validation stage.

If my robot is not a Unitree G1, the main extra work is robot-specific retargeting, a whole-body controller or tracking policy, and action-space adaptation. The GRAIL data philosophy still transfers: make generation creative, but make reconstruction and policy training geometry-grounded.

## Implementation Notes

A minimal replication should start with one object class and one behavior, such as pick up a box from a table. The first milestone is not real deployment; it is a simulated robot that can track one reconstructed 4D HOI trajectory without object drift or contact failure.

The highest-risk modules are VFM consistency, object pose tracking, contact alignment, and retargeting. Each stage needs visual diagnostics. If the generated object changes shape across frames or FoundationPose loses the object, training a policy on that sequence will likely teach the wrong behavior.

For smaller labs, the full GRAIL compute budget is large. A pragmatic path is to use the released dataset where possible, fine-tune only a narrow task-family tracker, and reserve new video generation for objects or scenes that are missing from the dataset.
