# Cosmos World Foundation Model Platform for Physical AI

## Metadata

- **Source:** <https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf>
- **Local PDF:** [papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.pdf](../papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.pdf)
- **Converted Markdown:** [papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.md](../papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.md)
- **Type:** NVIDIA technical report, 2026

## Research Question

Can a single foundation model platform unify the capabilities normally split across VLMs, video generators, forward dynamics models, inverse dynamics models, and robot policies for Physical AI?

## Method

Cosmos 3 is an omnimodal world model family for language, image, video, audio, and action. It uses modality-specific encoders, a unified token layout, and a Mixture-of-Transformers architecture. Autoregressive tokens handle reasoning and understanding, while diffusion tokens generate images, videos, audio, and actions through denoising.

For robotics, action is treated as a first-class modality. The report maps heterogeneous controls into relative pose and grasp-state components, then uses domain-aware projections for different embodiments. The same model supports forward dynamics, inverse dynamics, and policy mode by changing which video/action tokens are clean conditions and which are noisy generation targets.

## Key Innovation

The main innovation is not one isolated robot policy trick. It is a unified Physical AI platform where perception, simulation, action inference, and action generation share a model backbone and training curriculum.

Important design points:

- Action tokens are integrated with language, video, image, and audio instead of being a separate policy head only.
- Forward dynamics, inverse dynamics, and policy learning are represented as different token-conditioning patterns.
- Mid-training introduces action and video-transfer data after broad multimodal pre-training.
- Specialized models, such as `Cosmos3-Nano-Policy-DROID`, are obtained by post-training without changing the core architecture.
- Synthetic data generation, policy learning, and benchmark infrastructure are treated as one platform loop.

## Experiments

The report evaluates Cosmos 3 across reasoning, image/video/audio generation, transfer generation, forward/inverse dynamics, and robot policy.

Key robotics results:

- Action mid-training uses 8.4M episodes and 61.3K hours across egocentric motion, robotics, autonomous vehicles, and camera motion.
- Robotics data contributes 5.4K hours from sources including AgiBot, Franka Panda, Google Robot, WidowX, UMI, and UR datasets.
- On DROID forward dynamics, Cosmos3-Super with mid-training reaches 26.04 PSNR, above Ctrl-World at 22.99.
- `Cosmos3-Nano-Policy-DROID` reaches 39.7% RoboLab success under specific instructions, ahead of pi0.5 at 28.1% and DreamZero at 25.2%.
- On LIBERO-10 adaptation, mid-trained initialization reaches 24.6% success at 500 iterations and 97.4% at 2000 iterations, while pre-trained initialization starts at 0.0% at 500 iterations.

## Limitations

The report is platform-scale and depends on very large data and compute. Mid-training used 1024 to 2048 NVIDIA GB200 GPUs, which is not directly reproducible for a small lab. The DROID policy pilot is centered on Franka-style tabletop manipulation, so transfer to mobile manipulation or humanoids still requires embodiment-specific post-training. Some evaluation claims are leaderboard-based and may change as more submissions arrive.

## Practical Robotics Impact

Cosmos 3 is useful as a blueprint for building a robot learning stack:

- Train or fine-tune a policy from a world-action prior rather than only behavior cloning from robot demonstrations.
- Use forward dynamics as a video-based evaluator before executing risky action chunks.
- Use inverse dynamics to mine actions or pseudo-actions from passive videos.
- Use synthetic and transfer generation to cover long-tail scenes, camera views, and object configurations.
- Keep action representation geometric and embodiment-aware, instead of tying learning to low-level controller internals.

## Application to My Robot

For my robot, the most practical path is not to reproduce full Cosmos 3 training. Instead:

- Represent actions as relative end-effector pose deltas plus gripper state, and include proprioception.
- Collect multi-view robot demonstrations with language instructions and save both successful and failed rollouts.
- Fine-tune an available VLA or world-action model using a DROID-like format.
- Add an auxiliary future-video prediction loss so the policy learns expected consequences, not only actions.
- Use the predicted video rollout as a safety/debug signal before executing action chunks.

Required sensors and compute: wrist camera, one or two external RGB cameras, robot proprioception, gripper state, and at least one strong GPU for fine-tuning or inference. Expected benefit is better generalization across objects and instructions. Main risks are latency, action calibration errors, and false confidence from visually plausible but physically wrong predicted futures.
