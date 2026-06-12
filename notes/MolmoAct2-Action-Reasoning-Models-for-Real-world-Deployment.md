<!-- markdownlint-disable MD013 -->

# MolmoAct2: Action Reasoning Models for Real-world Deployment

## Metadata

- Authors: Haoquan Fang, Jiafei Duan, Donovan Clay, Sam Wang, Shuo Liu, Weikai Huang, Xiang Fan, Wei-Chuan Tsai, Shirui Chen, Yi Ru Wang, Shanli Xing, Jaemin Cho, Jae Sung Park, Ainaz Eftekhar, Peter Sushko, Karen Farley, Angad Wadhwa, Cole Harrison, Winson Han, Ying-Chun Lee, Eli VanderBilt, Rose Hendrix, Suveen Ellawela, Lucas Ngoo, Joyce Chai, Zhongzheng Ren, Ali Farhadi, Dieter Fox, Ranjay Krishna
- Venue/Year: arXiv, 2026
- Source: [arXiv PDF](https://arxiv.org/pdf/2605.02881)
- arXiv: 2605.02881v2, 8 May 2026
- Local PDF: [../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.pdf](../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.pdf)
- Converted Markdown: [../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.md](../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.md)
- Project page: [MolmoAct2 project page](https://allenai.org/blog/molmoact2)
- Code: [allenai/molmoact2](https://github.com/allenai/molmoact2)

## Research Question

Can an open VLA model be practical enough for real-world deployment: fast enough for closed-loop control, strong enough after fine-tuning, reproducible from open data and code, and deployable on low-to-medium cost robots rather than only on expensive closed platforms?

The paper argues that current VLA systems fail on at least one of these constraints. Closed frontier models are not reproducible, open alternatives often depend on narrow robot platforms, reasoning-based policies add too much latency, and fine-tuned success rates are not yet reliable enough for everyday use.

## Core Method

MolmoAct2 is a three-stage VLA training pipeline built around a spatially specialized VLM backbone and a continuous action expert.

First, the authors train Molmo2-ER, a Molmo2-derived VLM specialized for embodied reasoning. It is trained on a 3.3M-sample embodied reasoning corpus covering spatial QA, pointing, detection, video embodied QA, multi-image ego-exo reasoning, and abstract spatial reasoning, using a specialize-then-rehearse recipe to avoid losing general VLM capability.

Second, MolmoAct2-Pretrain turns Molmo2-ER into a discrete autoregressive robot policy. Robot states are discretized into tokens, and one-second continuous action chunks are converted into action tokens by MolmoAct2-FAST, an open action tokenizer trained on one million action sequences across YAM, SO-100/101, DROID Franka, Google Robot, and WidowX-style data.

Third, post-training attaches a DiT-style flow-matching action expert for continuous control. The action expert has the same 36-layer depth as the VLM. Instead of conditioning only on final hidden states, each action-expert layer cross-attends to the corresponding VLM layer's projected keys and values. This per-layer KV conditioning gives the controller direct access to visual-language attention state while preserving the VLM backbone.

MolmoAct2-Think adds adaptive depth-token reasoning. It predicts a 10 x 10 grid of depth tokens, but reuses cached tokens for static regions and only regenerates cells whose RGB patches changed. The goal is to preserve geometric grounding without paying the full reasoning-token latency at every control step.

## Key Innovation

The main contribution is not a single trick; it is an open deployment-oriented VLA stack:

- Molmo2-ER: an embodied-reasoning VLM backbone that improves spatial and robotic reasoning before action learning.
- MolmoAct2-BimanualYAM: 720 hours and 34.5K demonstrations on a bimanual YAM setup, plus filtered DROID and SO-100/101 datasets.
- MolmoAct2-FAST: an open-weight, open-data tokenizer for mapping heterogeneous continuous robot actions into discrete tokens.
- Per-layer KV conditioning: a cleaner bridge from a discrete-token VLM to a continuous flow-matching action expert.
- MolmoAct2-Think: adaptive depth reasoning that updates only changed spatial cells over time.

This combination matters because it targets reproducibility, embodiment coverage, latency, and continuous control at the same time.

## Problems Solved

MolmoAct2 addresses the deployment gap in current open robotics foundation models. It gives researchers a model family, data, tokenizer, and training recipe that can be inspected and extended rather than just a checkpoint.

It also addresses the mismatch between VLM token prediction and robot control. Discrete action tokens are useful for large-scale pretraining, but real robots need smooth continuous trajectories. The flow-matching action expert provides continuous action chunks while still using the VLM's visual-language grounding.

For reasoning latency, MolmoAct2-Think avoids regenerating dense geometric tokens for unchanged scene regions. This is especially relevant for tabletop manipulation, where much of the background remains static across adjacent control steps.

## Evidence

On embodied reasoning benchmarks, Molmo2-ER reaches 63.8% overall average across 13 benchmarks, outperforming strong open-weight models and reported proprietary baselines in the paper. The authors report a 17-point improvement over the Molmo2 starting point.

For out-of-the-box DROID-style deployment, MolmoAct2-DROID reports 37.7% average success on MolmoSpaces versus 34.5% for pi-0.5-DROID. In real-world DROID-style tasks with novel scenes and randomized camera poses, it reports 87.1% average success, above MolmoBot at 48.4% and pi-0.5-DROID at 45.2%.

On SO-100 real-world tasks, MolmoAct2-SO reports 56.7% average success, above the paper's pi-0 implementation on SO-100/101 at 45.3% and SmolVLA at 2.3%.

After fine-tuning, MolmoAct2 reports 97.2% average success on LIBERO, while MolmoAct2-Think improves to 98.1%. On RoboEval, MolmoAct2 reports 44.3% success, 3.8 points above pi-0.5. On eight real-world bimanual YAM tasks, it reports 50.1% average success, 15 points above the runner-up OpenVLA-OFT.

For robustness under perturbations, MolmoAct2-Think reports 50.69% average success across spatial, lighting, language, and distractor shifts, versus 39.89% for OpenVLA-OFT.

## Limitations

The method is expensive to train. Pretraining uses 64 H100 GPUs for about 5,760 GPU hours; post-training uses about 2,304 GPU hours; major fine-tunes also use 32-64 H100s. For most labs, direct reproduction is unrealistic without relying on released checkpoints.

The reported real-world success rates are promising but still not deployment-grade for all settings. The bimanual YAM fine-tuning average of 50.1% means many real tasks still fail. Spatial perturbation is also a weak point, with MolmoAct2-Think at 26.25% under spatial variation.

The paper evaluates several embodiments, but each deployed checkpoint is still embodiment-specific after fine-tuning. A user should not assume zero-shot transfer to a new robot without calibration, action-space mapping, and safety testing.

MolmoAct2-Think depends on monocular depth estimation and depth-token caching. Errors in reflective, transparent, low-texture, or strongly changing scenes could inject misleading geometric context into the action expert.

## Application to My Robot

For my robot, the most useful idea is the separation between a reasoning-capable VLM backbone and a continuous action expert. A practical adaptation would be:

- collect synchronized multi-camera observations, proprioceptive state, language instructions, and action trajectories;
- normalize actions into a fixed-width representation and choose a one-second action chunk matching the robot control rate;
- start from the released MolmoAct2 checkpoint if available rather than training the full stack;
- fine-tune on the target robot with the same setup/control descriptors and camera ordering used at deployment;
- evaluate a standard MolmoAct2-style policy first, then add depth-token reasoning only if spatial failures dominate.

For a low-cost arm or mobile manipulator, SO-100/101 is the closest reference path. For a bimanual robot, the YAM dataset is more relevant because it covers coordinated household, lab, and service tasks. For a Franka-like robot, the filtered DROID setup is the most natural starting point.

## Required Sensors or Compute

Minimum practical setup:

- one wrist camera plus one external camera, preferably synchronized;
- robot joint state and gripper state;
- a language task label or instruction per trajectory;
- enough demonstrations for the target task distribution;
- a GPU suitable for VLA fine-tuning or at least low-latency inference from a released checkpoint.

MolmoAct2-Think also benefits from stable camera geometry and depth-estimation quality. If the robot camera moves aggressively or the scene changes globally, adaptive depth caching may provide less latency benefit.

## Expected Benefit

The likely benefit is better spatial grounding than a pure behavior-cloning policy and smoother continuous action output than a token-only VLA. The open tokenizer, data recipe, and code also make it easier to debug action representation problems than with closed VLA systems.

The most attractive short experiment is not full reproduction. Fine-tune a released MolmoAct2 checkpoint on a small set of robot demonstrations and compare against a simpler diffusion policy or OpenVLA-style baseline on the same tasks. Track success rate, recovery from object displacement, latency per action chunk, and failure modes under camera and object shifts.

## Risks

The main risks are compute cost, action-space mismatch, camera-layout mismatch, and safety. A policy trained with one camera order, control mode, or action normalization can fail badly when deployed with another. Any real robot test should start with low-speed execution, workspace limits, collision checks, and a human stop mechanism.
