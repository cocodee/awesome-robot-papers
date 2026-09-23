# Reinforcement Learning for Real-Time Vision-Language-Action Policies

> Perry Dong, Kuo-Han Hung, Dorsa Sadigh, Chelsea Finn. arXiv:2609.18207v1, 2026-09-16.

This note accompanies the full Chinese tutorial: [中文精讲教程](Reinforcement-Learning-for-Real-Time-Vision-Language-Action-Policies.zh-CN.md). The paper proposes Real-Time EXPO-FT, an RL fine-tuning framework for VLA policies under inference latency.

## Core idea

Large VLAs provide strong behavior priors but are too slow for highly dynamic control. If inference starts at (s_t) and finishes (d) control steps later, a naive system executes an action generated from (s_t) at (s_{t+d}). This State-Action Temporal Mismatch breaks the usual Markov assumption and can severely reduce reliability.

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

The critic uses a chunk-level TD target spanning the execution horizon (C):

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
