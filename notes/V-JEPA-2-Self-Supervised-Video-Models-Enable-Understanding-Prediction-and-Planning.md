# V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

## Metadata

- Authors: Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba Komeili, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, Nicolas Ballas
- Venue/Year: arXiv, 2025
- Source: https://arxiv.org/pdf/2506.09985
- arXiv: 2506.09985v1, 11 Jun 2025
- Local PDF: [../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.pdf](../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.pdf)
- Local Markdown: [../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.md](../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.md)
- Code: https://github.com/facebookresearch/vjepa2
- Blog: https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks

## Research Question

Can a robot-useful world model be learned mostly from observation, rather than from dense task-specific robot interaction and reward labels? V-JEPA 2 asks whether internet-scale self-supervised video pretraining can produce representations that support understanding, prediction, and real robot planning after only a small amount of robot post-training.

## Core Method

The system uses a two-stage pipeline. First, V-JEPA 2 is pretrained on more than 1 million hours of internet video plus images with a JEPA-style mask-denoising objective in latent representation space. The model predicts missing video patch representations rather than reconstructing pixels, which lets it focus on predictable scene structure and motion.

Second, the pretrained video encoder is frozen and a 300M-parameter action-conditioned predictor, V-JEPA 2-AC, is trained on less than 62 hours of unlabeled DROID robot video. The predictor receives current frame features, end-effector state, and actions, then autoregressively predicts future latent frame features using teacher-forcing and short rollout losses.

For control, the robot receives a goal image. At each step, model-predictive control samples candidate action sequences with the Cross-Entropy Method, rolls them forward in the latent world model, chooses the action sequence whose predicted latent state is closest to the goal latent state, executes the first action, and replans.

## Key Innovation

The main innovation is using a large action-free video JEPA as the representation backbone for a robot action-conditioned latent world model. Instead of planning through slow pixel-space video generation, V-JEPA 2-AC plans in representation space. This makes model-based robot control feasible with a small amount of robot data and no task reward.

The paper also shows that a video encoder pretrained without language supervision can be aligned with an LLM for video QA, suggesting that physical and temporal understanding can be learned before language alignment rather than only through captioned data.

## Problems Solved

V-JEPA 2 addresses three practical bottlenecks:

- large robot datasets are expensive, while unlabeled internet video is abundant;
- pixel video generation is costly for closed-loop planning;
- task-specific reward design and in-environment robot data collection slow down deployment.

For robotics, the important result is zero-shot transfer to Franka arms in two labs not present in the DROID data, using only an uncalibrated low-resolution monocular RGB camera and visual goal images.

## Experiments

For video understanding, V-JEPA 2 reports 77.3 top-1 accuracy on Something-Something v2. For human action anticipation, it reports 39.7 Recall@5 on EPIC-KITCHENS-100. After LLM alignment at the 8B scale, it reports results such as 84.0 on PerceptionTest and 76.9 on TempCompass.

For robot control, V-JEPA 2-AC is trained on about 23k DROID trajectories, under 62 hours of video. In zero-shot robot manipulation, it achieves 100% average reach success, 65% cup grasp, 25% box grasp, 75% cup reach-with-object, 75% box reach-with-object, 80% cup pick-and-place, and 65% box pick-and-place across the reported lab evaluations. Compared with a Cosmos action-conditioned video generation baseline on Lab 2, V-JEPA 2-AC uses 16 seconds per planned action versus 4 minutes for Cosmos and performs better on object interaction tasks.

## Limitations

The robot planner is still slow for real-time manipulation: 16 seconds per action is useful for research but not acceptable for fast closed-loop control. The robot tasks are also relatively short-horizon and often depend on image sub-goals; long-horizon plans without intermediate visual goals remain difficult because autoregressive latent prediction accumulates error and action search grows quickly.

The model is sensitive to camera placement because it must infer robot action coordinates from monocular RGB without explicit calibration. The experiments are limited to Franka tabletop manipulation, so transfer to mobile manipulation, bimanual work, deformable objects, and cluttered contact-rich settings is still unproven.

## Practical Robotics Impact

The paper is useful as a blueprint for goal-image visual servoing with a learned latent dynamics model. It is especially relevant when the robot has limited demonstrations for the target lab, but can reuse a strong video representation and a modest amount of broad robot trajectory data.

The key engineering lesson is to separate representation learning from action-conditioned dynamics learning: pretrain or reuse a broad video encoder, freeze it, then train a smaller dynamics head from robot data. This reduces the robot data burden and gives a practical way to test whether latent planning works before investing in a full VLA policy.

## Application to My Robot

For my robot, start with a constrained tabletop manipulation setup: one calibrated or consistently mounted RGB camera, end-effector Cartesian actions, gripper state, and goal images. Train an action-conditioned latent predictor on local demonstrations or public DROID-style data, then evaluate model-predictive control on reach, grasp, and simple pick-and-place.

Required sensors and compute are an RGB camera, robot end-effector state, gripper state, a GPU for latent planning, and a low-level controller that can execute small Cartesian deltas safely. Expected benefits are better data efficiency, goal-image conditioning without reward engineering, and a reusable world-model component for later policy learning. Main risks are slow planning, camera-view sensitivity, poor gripper timing, and compounding prediction errors on long tasks.

## Implementation Notes

The smallest useful experiment is not to reproduce the full 1B-parameter V-JEPA 2 pretraining. Reuse available V-JEPA 2 weights, freeze the encoder, and train a small action-conditioned predictor on a narrow robot dataset. Compare it against behavior cloning with the same goal images. If latent planning improves recovery from off-nominal states but is too slow, use the world model to generate training targets or initialize a faster policy.
