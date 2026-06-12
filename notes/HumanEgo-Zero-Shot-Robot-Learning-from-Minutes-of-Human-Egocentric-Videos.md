# HumanEgo: Zero-Shot Robot Learning from Minutes of Human Egocentric Videos

## Metadata

- Authors: Zhi Wang, Botao He, Kelin Yu, Seungjae Lee, Ruohan Gao, Furong Huang, Yiannis Aloimonos
- Venue/Year: arXiv, 2026
- Source: [arXiv PDF](https://arxiv.org/pdf/2605.24934)
- arXiv: 2605.24934v2, 28 May 2026
- Local PDF: [../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.pdf](../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.pdf)
- Converted Markdown: [../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.md](../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.md)
- Project page: [HumanEgo](https://humanego-ai.github.io/)
- Code: [TX-Leo/HumanEgo](https://github.com/TX-Leo/HumanEgo)

## Research Question

HumanEgo asks whether a robot can learn deployable manipulation policies directly from a few minutes of human first-person video, without collecting robot demonstrations, without large-scale pretraining, and without post-training on the target robot.

The core problem is the embodiment gap. Human hands and robot grippers differ visually and kinematically, but the task-relevant hand-object interaction geometry should transfer across bodies.

## Core Method

HumanEgo turns egocentric human demonstrations into a bimanual robot policy through four stages.

First, a human records task demonstrations with Aria Gen1 glasses. The Aria pipeline provides synchronized egocentric RGB, SLAM poses, and metric 3D hand tracking.

Second, HumanEgo preprocesses visual observations to reduce the visual embodiment gap. It segments the human arm and hand with SAM2, removes them with LaMa inpainting, and renders a virtual gripper plus object keypoints back into the image.

Third, it constructs Interaction-Centric Tokens (ICT). Each hand and object is treated as an entity. For every entity, the token stores entity type, pose in a reference frame, left-hand pose relative to that entity, right-hand pose relative to that entity, and grasp state. This explicitly represents approaching, grasping, transporting, and releasing as relationships between hands and objects rather than as human-body motion.

Fourth, it trains a flow matching policy that predicts bimanual action chunks. The policy uses a transformer-style context encoder and action decoder, and adds three dense auxiliary objectives: future object motion, future 2D entity traces, and future latent ICT state. These objectives force the encoder to learn forward dynamics in 3D physical, 2D visual, and latent spaces.

## Key Innovation

- Robot-data-free learning from human egocentric video for real robot manipulation.
- Interaction-Centric Tokens that encode transferable hand-object relations instead of imitating human hand geometry.
- Visual preprocessing that removes human appearance while keeping task-relevant visual cues.
- Flow matching action generation for multimodal actions with faster inference than iterative diffusion-style sampling.
- Dense auxiliary supervision that extracts more learning signal from each short demonstration.
- Zero-shot transfer across cameras, robot arms, environments, object placements, and visual conditions.

## Problems Solved

The paper targets the cost and friction of collecting task-specific robot teleoperation data. Instead of asking the user to teleoperate the exact robot in the exact setup, it lets a person perform the task naturally with a wearable camera.

It also addresses a limitation of prior human-video methods: representing only points, only object motion, or only goal-conditioned tracks loses the interaction structure that actually defines manipulation. HumanEgo makes the hand-object relation the primary state.

## Experiments

The main evaluation uses four real-world tasks: Serve Bread, Downstack Cups, Water Flowers, and Adjust Table. These include pick-and-place, long-horizon stacking, contact-rich bimanual coordination, and sustained rotational control.

With 30 minutes of human video per task, HumanEgo reports 92.5% average success across the four tasks. With 15 minutes, it reports 75.0%. The matched-time robot teleoperation baseline ACT reaches 51.2%, so HumanEgo is reported as 41 percentage points better than robot teleoperation under the main comparison.

Against five zero-shot human-video baselines, HumanEgo is strongest on every task. The baselines span point-based methods, goal-conditioned methods, and object-centric methods, but they fail more often on tasks needing precise hand-object geometry and bimanual sequencing.

The data-efficiency study on Serve Bread shows that HumanEgo reaches 50% success with about 7 minutes of human demonstrations and 95% at 30 minutes. At 8 minutes, HumanEgo trained on human data already surpasses ACT trained on 30 minutes of robot data.

The robustness study reports strong zero-shot transfer under new backgrounds, lighting, viewpoints, distractors, object instances, camera setups, table heights, and robot embodiments including Trossen, Franka, and UR10.

## Ablations

The representation ablation is the strongest evidence. Raw human RGB reaches 7.5%, keypoint rendering with arm inpainting reaches 20%, robot RGB reaches 32.5%, raw human RGB plus ICT reaches 85%, and the full system reaches 95%. This supports the claim that explicit spatial interaction tokens matter more than visual realism alone.

The auxiliary-loss ablation at 15 minutes shows that object motion gives the largest individual gain, followed by latent consistency and 2D trace. Combining all three gives a 25 percentage point gain over the no-auxiliary baseline.

The hand-tracking appendix is practically important. Replacing Aria stereo hand tracking with monocular trackers causes success to fall sharply: Aria-MPS reaches 95%, WiLoR 45%, HaMeR 32.5%, and MediaPipe 0% on Serve Bread. The method depends heavily on smooth, metric 3D hand trajectories.

## Limitations

HumanEgo relies on Aria's stereo hand tracking. Monocular substitutes introduce depth ambiguity, jitter, missing detections, and lower downstream success.

The perception stack is chained from several off-the-shelf modules: SAM2, LaMa, Grounding DINO, CoTracker3, Orient-Anything, SLAM, and hand tracking. Errors in detection, segmentation, pose estimation, or tracking can cascade into the policy.

Object handling is not yet a full online tracker. In-hand manipulation, heavy occlusion, fast motion, and dynamic scenes may require more robust real-time tracking.

The paper reports strong zero-shot results, but the tasks are still tabletop manipulation tasks. Sub-centimeter contact-rich control likely needs RL refinement, simulation fine-tuning, or real robot feedback.

One reproducibility detail to check carefully: the main paper emphasizes 30 minutes of human video per task, while the appendix hyperparameter table lists 60 demonstrations and 40 minutes of total human-video time per task. Reproduction should define the exact included clips, trimming rule, and train/test split.

## Application to My Robot

HumanEgo is most useful if my robot project needs quick task learning without building a teleoperation dataset first. The practical route is:

- collect first-person task videos with a device that can provide metric hand pose or reliable depth;
- convert the hand into a virtual gripper action label;
- track manipulated objects and keypoints;
- build ICT-style tokens for each hand and object;
- train a flow matching action policy with auxiliary future-prediction losses;
- deploy the policy through my robot's inverse kinematics and gripper controller.

For my robot, the most reusable idea is not the exact model architecture but the data interface: represent manipulation as relative hand-object transforms. This can be implemented before building a large VLA stack.

## Implementation Notes

The first engineering priority is the perception frontend. If I do not have Aria-style stereo hand tracking, I should either add calibrated multi-camera tracking, use depth sensors, or expect a large performance drop.

Start with one simple pick-and-place task. Log RGB, camera pose, object masks, object keypoints, hand pose, and the derived gripper pose. Validate the ICT trajectories visually before training. A bad tracker will look like a bad policy later.

For deployment, keep conservative safety limits on per-cycle position and rotation changes, smooth action chunks, and test the gripper latch logic separately. HumanEgo's action stream still needs normal robot safety engineering.
