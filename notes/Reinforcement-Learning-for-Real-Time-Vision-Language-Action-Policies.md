# Reinforcement Learning for Real-Time Vision-Language-Action Policies

> Perry Dong, Kuo-Han Hung, Dorsa Sadigh, Chelsea Finn. arXiv:2609.18207v1, 2026-09-16.

This note accompanies the full Chinese tutorial: [中文精讲教程](Reinforcement-Learning-for-Real-Time-Vision-Language-Action-Policies.zh-CN.md). The paper proposes Real-Time EXPO-FT, an RL fine-tuning framework for VLA policies under inference latency.

## Core idea

Large VLAs provide strong behavior priors but are too slow for highly dynamic control. If inference starts at $$s_t$$ and finishes $$d$$ control steps later, a naive system executes an action generated from $$s_t$$ at $$s_{t+d}$$. This State-Action Temporal Mismatch breaks the usual Markov assumption and can severely reduce reliability.

Real-Time EXPO-FT separates two time scales:

1. A large VLA asynchronously samples candidate action chunks using the old state and RTC-style committed-action prefix conditioning.
2. A lightweight edit policy synchronously adds a bounded residual using the latest observation.
3. A chunk-level critic evaluates original and edited candidates at the latest state and selects the highest-value chunk.

The central computation is:

$$
a^i=\pi_{VLA}(s_t,a^{prev}_{t:t+d},\epsilon_i),
\quad
\tilde a^i=a^i+\hat a^i,
\quad
\hat a^i\sim\pi_{edit}(\cdot|s_{t+d},a^i).
$$

The critic uses a chunk-level TD target spanning the execution horizon $$C$$:

$$
Q(s_t,a_{t:t+C})\leftarrow r_t+\gamma Q(s_{t+C},a^*_{t+C:t+2C}).
$$

## Main lessons

- RTC prevents pauses while the VLA is computing, but does not by itself correct stale observations.
- Real-Time EXPO-FT retains the VLA's long-horizon prior while using a fast policy for local state correction.
- Bounded edits protect the base policy and keep RL focused on refinement rather than replacing the VLA.
- Chunk-level value estimation is appropriate for tasks whose outcomes depend on temporally extended action segments.
- The method is a multi-timescale control stack, not a replacement for IK, servo control, collision checking, or emergency stops.

## Experimental headline

On four real-world dynamic tasks, with online robot data capped at ten minutes per task, success improved from 12.5/30 for SFT (about 42%) to 29/30 for Real-Time EXPO-FT (about 97%). The tasks were Dynamic Picking, Ball Balancing, Object Passing, and Soccer Kicking. On ten Kinetix simulation environments, the delayed method achieved a 96.2% average success rate.

## Engineering interpretation

For a dynamic dual-arm or mobile-manipulation system, VLA should generate coarse synchronized proposals, while a fast edit policy uses the latest target pose, velocity, relative-arm geometry, and proprioception to compensate for motion during VLA inference. The resulting actions should still pass through IK, collision, velocity/acceleration, force, and emergency-stop layers.

## Source files

- [Paper PDF](../papers/Reinforcement-Learning-for-Real-Time-Vision-Language-Action-Policies.pdf)
- [Extracted paper text](../papers/Reinforcement-Learning-for-Real-Time-Vision-Language-Action-Policies.md)
- [arXiv page](https://arxiv.org/abs/2609.18207)

## Question Analysis

### Critic design, training, and inference

The paper uses a chunk-level Q-function rather than a single-step action-value function:

$$
Q_\phi(s_t,a_{t:t+C}).
$$

The critic receives multi-view images, proprioception, and a flattened action chunk. In the real-robot setting, images are encoded into a 512-dimensional embedding, proprioception into a 64-dimensional embedding, and the result is combined with the action chunk before entering a three-layer, 256-wide Q network. The critic is a REDQ-style ensemble of 10 Q networks. For target estimation, two target networks are subsampled and their minimum is used to reduce Q overestimation.

The critic is trained from offline demonstrations and online replay data with a chunk-level TD target:

$$
y_t=r_t+\gamma Q_{\phi'}(s_{t+C},\tilde a^*_{t+C:t+2C}).
$$

$$
\mathcal L_Q=\mathbb E\left[\left(y_t-Q_\phi(s_t,a_{t:t+C})\right)^2\right].
$$

The next chunk $$\tilde a^*_{t+C:t+2C}$$ is selected by the target critic. Real-robot rewards are mainly sparse binary success rewards; terminal transitions do not bootstrap. The target critic is updated with Polyak averaging using $$\tau_Q=5\times10^{-3}$$. The reported real-robot settings use Adam with learning rate $$3\times10^{-4}$$, batch size 64, and an update-to-data ratio of 20.

The edit policy uses the critic as its optimization signal. It samples a bounded residual:

$$
\hat a\sim\pi_{edit}(\cdot|s,a),\qquad \tilde a=a+\hat a,
$$

and is trained to increase the value of the edited chunk:

$$
\mathcal L_{edit}=-\mathbb E\left[Q_\phi(s,a+\hat a)-\alpha\log\pi_{edit}(\hat a|s,a)\right].
$$

At inference, the VLA asynchronously proposes $$N$$ chunks from the old state $$s_t$$. At the execution boundary, the edit policy uses the latest state $$s_{t+d}$$ to produce edited candidates. The critic scores both original and edited candidates:

$$
\tilde a^*=\arg\max_{a\in\{a^i,\tilde a^i\}}Q_\phi(s_{t+d},a).
$$

The real-robot experiments typically evaluate 32 base candidates and 32 edited candidates, select deterministically using the minimum of two subsampled target-Q values, and do not apply a softmax. The original action can therefore win if its Q value is higher than the edited version.

The paper also describes an optional noise-level filter critic, $$Q^{dn}_\psi(s',\epsilon)$$, which scores VLA noise seeds before full denoising during Bellman backups. It is a two-network ensemble trained by MSE regression to the outer target critic with stop-gradient targets. It reduces training compute only and does not replace the main critic during rollout action selection.

In short, the VLA proposes behavior, the edit policy makes a fast latest-state correction, and the critic chooses which complete action chunk is most valuable to execute.
