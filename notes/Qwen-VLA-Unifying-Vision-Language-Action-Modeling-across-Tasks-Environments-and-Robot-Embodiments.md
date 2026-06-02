# Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments

## Metadata

- Authors: Qwen Team
- Source: https://arxiv.org/pdf/2605.30280
- arXiv: 2605.30280v1, 28 May 2026
- Local PDF: [../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.pdf](../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.pdf)
- Converted Markdown: [../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.md](../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.md)
- Blog: https://qwen.ai/blog?id=qwenvla
- Code: https://github.com/QwenLM/Qwen-VLA

## Research Question

Qwen-VLA asks whether manipulation, navigation, trajectory prediction, and egocentric embodied action modeling can be unified in one VLA model rather than handled by separate task- or embodiment-specific systems.

## Core Method

Qwen-VLA builds on a Qwen3.5-4B vision-language backbone and adds a 1.15B-parameter DiT-style flow-matching action expert. The model predicts continuous action or trajectory chunks from visual observations, language instructions, task identifiers, and an embodiment-aware prompt.

The embodiment prompt describes the robot platform, arm configuration, control frequency, control convention, and prediction horizon. Qwen-VLA keeps each dataset's native action semantics instead of forcing every robot into one physical action space. It uses a shared padded tensor and mask so one action expert can train across manipulation actions, navigation waypoints, and human motion trajectories.

Training is staged: text-to-action DiT pretraining teaches the decoder a language-conditioned action prior without images; continued pretraining grounds this prior in visual observations across heterogeneous data; SFT aligns the model to target tasks and real robot data; RL further optimizes task success in simulation to produce Qwen-VLA-Instruct.

## Key Innovation

- Unified action-and-trajectory prediction across manipulation, navigation, driving-style trajectories, and egocentric motion.
- Embodiment-aware prompt conditioning as the main interface for robot-specific control semantics.
- Shared padded action tensor plus validity mask, avoiding separate output heads per embodiment.
- Progressive training recipe: T2A, CPT, SFT, and RL.
- Joint training over robot trajectories, human egocentric demonstrations, synthetic simulation, VLN, spatial grounding, driving VQA, and general VL data.

## Problems Solved

Qwen-VLA addresses fragmentation across task families and robot embodiments. A single model can be prompted to operate different platforms and output different continuous control formats. This reduces the need to maintain separate manipulation, navigation, and trajectory models.

It also addresses training instability when a pretrained VLM is paired with a randomly initialized action decoder. T2A pretraining gives the action decoder a structured prior before visual grounding.

## Evidence

As a single generalist policy, Qwen-VLA-Instruct reports 97.9% on LIBERO, 56.7% on RoboCasa-GR1, 73.7% on Simpler-WidowX, and 86.1%/87.2% on RoboTwin Easy/Hard. It outperforms most specialist baselines on several benchmarks.

On real-world ALOHA tasks, fine-tuning from Qwen-VLA-Base achieves 83.6% average in-domain success versus 48.5% when training from scratch. On OOD ALOHA tests, pretraining gives 76.9% average success, outperforming pi0.5 at 41.5%.

For navigation, Qwen-VLA-Instruct achieves 57.5 SR on R2R Val-Unseen and 59.6 SR on RxR Val-Unseen, leading open-source baselines on most reported metrics.

## Limitations

The model is large: Qwen3.5-4B plus a 1.15B action expert. The unified representation masks over heterogeneous action spaces but does not remove all semantic mismatch between embodiments. Real-world results are shown on ALOHA, so broader hardware validation is still needed. RL refinement is performed in simulation, and transfer of that optimization may vary across robots.

## Application to My Robot

Qwen-VLA is useful if my robot needs both manipulation and navigation, or if I want one model to support multiple robot configurations. The practical idea is to describe the robot in text and keep a stable action tensor contract:

- write an embodiment prompt specifying robot type, arms, base, FPS, and action horizon;
- map my robot commands into leading channels of a fixed action tensor;
- mask unused channels and normalize per dataset;
- keep the native control convention instead of forcing another robot's action semantics;
- use T2A-style action pretraining if I have command logs without reliable images;
- fine-tune from a pretrained checkpoint for real hardware.

For my robot, embodiment-aware prompting and masked action tensors are the most directly reusable design.

## Implementation Notes

Before training, define the action schema and prompt template. A good first experiment is one manipulation-only model with fixed `K` action channels and a mask, then add base or navigation waypoints later. Validate that action normalization and masks are correct before adding multi-task data.
