# SmoothRL: Online Reinforcement Learning During Asynchronous Execution

## Metadata

- Authors: Astribot Team (Contributors: Guang Gao, Yuxuan Nong, Baifu Huang; Project Lead: Jianan Wang)
- Venue/year: arXiv, 2026
- Source: https://arxiv.org/pdf/2608.29768
- arXiv: 2608.29768v1 [cs.RO], 30 Aug 2026
- Local PDF: [../papers/SmoothRL-Online-Reinforcement-Learning-During-Asynchronous-Execution.pdf](../papers/SmoothRL-Online-Reinforcement-Learning-During-Asynchronous-Execution.pdf)
- Converted Markdown: [../papers/SmoothRL-Online-Reinforcement-Learning-During-Asynchronous-Execution.md](../papers/SmoothRL-Online-Reinforcement-Learning-During-Asynchronous-Execution.md)
- Project page: https://www.astribot.com/research/SmoothRL

## Research Question

How can online reinforcement learning fine-tuning be integrated into an asynchronous deployment loop, so that a pretrained policy is optimized under the same execution semantics it will actually encounter at test time?

The paper frames real-world deployment as two complementary requirements — reliability (high task success) and smooth real-time execution — that are usually studied in isolation. Pretrained generalist policies (VLA and WAM) need sample-efficient online RL to reach the precision required for contact-rich tasks, while their growing inference latency forces modern systems to overlap inference with execution through action chunking and asynchronous scheduling. Existing online RL assumes synchronous execution, so the policy is optimized under dynamics that differ from deployment. SmoothRL closes this gap by "reinforcing in deployment".

## Core Method

SmoothRL follows the value-gradient paradigm: the gradient of the action-value function with respect to the policy's actions ∇_a Q is backpropagated through the deterministic policy into its parameters. The central difficulty is that, under asynchronous execution, a generated action chunk is only partially executed before the next chunk supersedes it. SmoothRL therefore partitions each horizon-H chunk by frame index into three regions, made deterministic by a fixed latency budget n:

- Committed region [0, n): frames that elapse during this chunk's own inference latency, supplied by the previous chunk. They can never affect the environment through the current chunk.
- Execution region [n, 2n): newly generated frames actually issued to and executed by the robot; the only part of the chunk that directly determines the trajectory.
- Discarded region [2n, H): frames superseded by the next inference cycle, never reaching the environment.

The two key contributions formalize the training implications:

- Gradient truncation to the execution region. ∇_a Q is computed only with respect to a[n,2n), so policy updates depend exclusively on actions whose consequences are observed. The critic, however, still consumes the full chunk: the committed region must be part of its input for the chunk-skip Bellman backup to stay unbiased, and the in-flight action serves as state augmentation for the concurrent-decision process.
- Asynchronous execution embedded in the training loop. The asynchronous inference loop — inference overlapping execution — runs during training rollouts, not only at deployment. Replay transitions therefore record the actions the robot actually executed under the same timing the objective is defined against.

Operating in the raw action space also lets human intervention serve directly as a BC regression target and a value-labeled transition, with no latent inversion.

Instantiation. The implementation follows the RLT skeleton: a frozen base policy (π0.5, fine-tuned per task) emits a reference action chunk and a compressed RL token from its internal representation; a lightweight TD3-style attached actor-critic predicts a bounded residual correction added to the reference chunk. The actor loss is

L_actor = −Q(z, s, sg[ã[0,n)], a[n,2n)) + w_bc · ‖a − a_target‖² + w_smooth · Σ_k w_k · ‖Δ^k a‖²,

where sg[·] is a stop-gradient over the committed region, and the smoothness term penalizes velocity (k=1), acceleration (k=2), and jerk (k=3) to instantiate the executable-set constraint instead of chunk stitching or trajectory blending. The critic is an MLP with LayerNorm and a REDQ-style ensemble of N critics. The replay buffer is seeded by rolling out the frozen base policy alone, and updates are paced by rollout throughput (G=5 critic iterations per trajectory, actor delay D=5).

## Key Innovation

- Reinforce in deployment: online value-gradient RL is performed inside the exact asynchronous loop used at deployment, eliminating the train/deploy dynamics mismatch.
- Chunk-role partitioning with a latency budget: fixing the boundaries (d = c = n) turns stochastic execution status into a function of frame index alone, making the objective well-defined.
- Gradient truncation: only the executed region receives ∇_a Q, while the critic stays conditioned on the full chunk to preserve the unbiased chunk-skip bootstrap and model concurrency.
- Human intervention in raw action space: absolute (VR teleop) and residual (hand-controller delta) modes both record the issued action directly as a BC target and RL transition, without latent inversion.
- Smoothness via constrained optimization: a velocity/acceleration/jerk penalty replaces post-hoc boundary blending, keeping the executed action identical to the policy output.

## Problems Solved

The paper targets a specific failure mode: value-gradient online RL breaks under asynchronous execution because ∇_a Q would otherwise backpropagate through generated actions that never reached the environment, contaminating the parameter update. It also addresses the deployment-side problem that synchronous execution pauses the robot at every chunk boundary, which is fatal for tasks requiring continuous motion (e.g., building release velocity through a swing).

The conceptual contribution is reframing "which segment is actually executed" as a known constraint imposed by deployment, and eliminating gradient contamination in the objective itself rather than in the execution schedule. The same truncation principle is shown to extend naturally to trajectory blending, where every contributing chunk is differentiated exactly once over its disjoint executed segment.

## Evidence

- Real-robot tasks on Astribot S1 (25-DoF mobile bimanual robot), with π0.5 fine-tuned per task as the frozen base policy. Inference at 5 Hz (n=6 frames at 30 Hz control, H=32 frames per chunk).
- After 250 rollout episodes, all three tasks substantially beat the frozen base policy: dynamic tossing 39% → 94%, pen capping 8% → 83%, box opening 30% → 90%.
- Learning dynamics differ by task: tossing and pen capping improve monotonically (largest gains in the first 150 episodes), while box opening drops transiently to 20% before recovering to 90%, attributed to exploration.
- Residual intervention (≈80%) markedly outperforms absolute VR teleoperation (≈30%) on the hardest far-bin tossing configurations, motivating residual mode for dynamic tasks.
- The paper argues qualitatively — via "closing the last millimeter" failure analysis — that remaining errors shrink from systematic, visible biases to small spreads (1–2 mm) around the correct pose, which is precisely the precision regime that separates success from failure.

## Limitations

- Inference latency constraint: the framework assumes a fixed inference frequency where every chunk completes within its budget. If latency fluctuates beyond n, scheduled handover cannot be guaranteed and the timing alignment destabilizes the loop.
- Output expressiveness bounded by the base policy: the RL branch is conditioned on VLA internal features (perception bounded by the base policy's embedding richness) and only produces bounded residual corrections in a fixed local neighborhood. Systematic biases of the base policy that exceed this radius cannot be corrected.
- Evaluation is single-seed per task (one RL run), with only ~10–18 evaluation configurations per checkpoint, and checkpoints use the same configurations as training, so generalization to unseen configurations is not measured.
- Success rewards are sparse and human-labeled via a gamepad/VR interface, so results depend on operator judgment and are not trivially reproducible at scale.

## Application to My Robot

The most practical lesson is that online RL should run inside my real deployment loop, not in a simplified synchronous simulator loop. If my robot already uses action chunking with asynchronous inference to hide latency, I can add a small trainable residual module on top of a frozen policy and fine-tune it with value gradients truncated to the actually-executed frames.

A staged implementation would be:

- fix a latency budget n and enforce a scheduled handover so chunk boundaries are deterministic;
- freeze my existing policy (VLA or WAM) and extract a compressed feature token plus a reference action chunk per forward pass;
- attach a small actor-critic (MLP) that predicts a bounded residual correction in raw action space, with a TD3+BC-style actor loss and a smoothness penalty over velocity/acceleration/jerk;
- seed the replay buffer with base-policy rollouts, then run the asynchronous loop for data collection while a concurrent process performs critic/actor updates;
- record human interventions (absolute and residual) in raw action space as both BC targets and Q-labeled transitions.

For a smaller project, the key experiment is not reproducing 250-episode fine-tuning at full scale; it is verifying that (a) gradient truncation to the execution region prevents the value-gradient update from being contaminated by superseded frames, and (b) the smoothness penalty substitutes for chunk stitching on tasks where motion continuity matters. High-precision insertion (pen capping, box seam cutting) and dynamic release (tossing) are the best probe tasks because they expose the last-few-millimeters gap and the continuity requirement respectively.

Required hardware includes a policy inference latency that is roughly stable (or an upper bound you can budget), synchronized RGB and proprioception, and a teleoperation device that emits commands in the same action space as the policy. Risks include latency spikes breaking the fixed-budget assumption, residual corrections that are too small to fix systematic base-policy bias, and over-reliance on human-labeled sparse rewards. Use a conservative correction bound, monitor chunk-handover timing, and keep a human stop switch during transfer.
