# StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing

## Metadata

- Authors: StarVLA Community
- Source: https://arxiv.org/pdf/2604.05014
- arXiv: 2604.05014v1, 6 Apr 2026
- Local PDF: [../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.pdf](../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.pdf)
- Converted Markdown: [../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.md](../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.md)
- Project: https://starvla.github.io
- Code: https://github.com/starVLA/starVLA

## Research Question

StarVLA asks how VLA research can become reproducible and comparable when current methods use incompatible model architectures, data loaders, training scripts, and evaluation protocols.

## Core Method

StarVLA is an open-source modular framework for VLA development. It decomposes policies into a vision-language backbone and a pluggable action head. The framework supports VLM backbones such as Qwen3-VL and world-model backbones such as Cosmos-Predict2, while keeping the same data interface, training loop, and deployment API.

It implements four representative action paradigms: StarVLA-FAST for autoregressive action-token generation, StarVLA-OFT for parallel continuous regression, StarVLA-pi for flow-matching action denoising, and StarVLA-GR00T for dual-system reasoning. It also provides supervised robot learning, multimodal co-training, cross-embodiment robot data mixtures, and a server-client evaluation interface.

## Key Innovation

- A backbone/action-head abstraction that makes VLA components interchangeable.
- Unified data and inference contracts across direct VLA, VLM-based VLA, and world-model-based VLA.
- Benchmark adapters for LIBERO, SimplerEnv, RoboTwin 2.0, RoboCasa-GR1, BEHAVIOR-1K, and related environments.
- Same policy server interface for simulation benchmarks and real-robot deployment.
- Reproducible single-benchmark recipes that avoid hidden data engineering.

## Problems Solved

The paper addresses the fragmentation problem in VLA research. Without shared abstractions, it is hard to tell whether performance differences come from model design, data preprocessing, training recipe, or benchmark implementation. StarVLA isolates these factors so researchers can swap one component while holding the rest fixed.

## Evidence

On LIBERO, StarVLA variants trained for 30K steps achieve strong results: StarVLA-OFT with Qwen3-VL reaches 96.6% average, StarVLA-GR00T reaches 96.5%, and Cosmos-Predict2 variants stay above 95.2%. These results are competitive with OpenVLA-OFT at 97.1% despite using far fewer steps.

On SimplerEnv WidowX Visual Matching, StarVLA-GR00T with Qwen3-VL reaches 65.3% average and StarVLA-OFT reaches 64.6%, competitive with or above strong published baselines.

## Limitations

This is primarily a framework and benchmark paper, not a new policy architecture. Its value depends on code maintenance, adapter quality, and whether future methods fit the abstraction. RL fine-tuning is described as planned or ongoing rather than fully central to the public code at the time of the report.

## Application to My Robot

StarVLA is useful as an engineering base for testing different VLA policy heads on the same robot data. For my robot, the main value is not one specific model but a clean experimental harness:

- keep robot observation/action formatting stable;
- compare OFT, FAST, flow-matching, and GR00T-style heads under the same data;
- reuse the policy-server interface for simulation and hardware;
- add a robot-specific adapter for action unnormalization, gripper logic, and safety filtering.

This can prevent misleading comparisons when testing new robot-policy ideas.

## Implementation Notes

Start by implementing a local dataset adapter and a policy-client adapter for the robot. Then run a small baseline with StarVLA-OFT because it is the simplest head. Once the data path works, compare flow-matching or GR00T-style action heads without changing the evaluation loop.
