# StarVLA: 面向 VLA 模型开发的乐高式代码库

## 元数据

- 作者：StarVLA Community
- 来源：https://arxiv.org/pdf/2604.05014
- arXiv：2604.05014v1，2026-04-06
- 本地 PDF：[../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.pdf](../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.pdf)
- 转换 Markdown：[../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.md](../papers/StarVLA-A-Lego-like-Codebase-for-Vision-Language-Action-Model-Developing.md)
- 项目页：https://starvla.github.io
- 代码：https://github.com/starVLA/starVLA

## 研究问题

这篇论文关注 VLA 研究中的工程碎片化问题：不同方法使用不同代码库、数据格式、训练脚本和评估协议，导致复现困难，也很难公平比较模型设计。

## 核心方法

StarVLA 是一个开源 VLA 开发框架。它把策略拆成 vision-language backbone 和可插拔 action head。backbone 可以是 Qwen3-VL 这类 VLM，也可以是 Cosmos-Predict2 这类 world-model backbone；action head 可以独立替换，而数据接口、训练循环和部署 API 保持一致。

框架实现了四类代表性动作解码方式：FAST 自回归动作 token、OFT 并行连续动作回归、pi 风格 flow-matching 动作去噪，以及 GR00T 风格双系统推理。它还支持监督学习、多模态 co-training、跨本体机器人数据混合训练，以及统一 server-client 评估。

## 关键创新

- backbone/action-head 解耦，让 VLA 组件可以像积木一样替换。
- 用统一接口覆盖 direct VLA、VLM-based VLA 和 world-model-based VLA。
- 集成 LIBERO、SimplerEnv、RoboTwin 2.0、RoboCasa-GR1、BEHAVIOR-1K 等 benchmark。
- 仿真和真实机器人使用同一 policy server 接口。
- 提供可复现实验 recipe，减少隐藏的数据工程差异。

## 实际解决的问题

StarVLA 解决的是 VLA 实验不可比的问题。没有统一框架时，性能差异可能来自模型、数据预处理、训练 recipe 或评估脚本，很难定位。StarVLA 让研究者可以固定大部分系统，只替换一个模块做对照实验。

## 实验证据

在 LIBERO 上，StarVLA 多个变体只训练 30K steps 就达到较强结果：Qwen3-VL backbone 下 StarVLA-OFT 平均 96.6%，StarVLA-GR00T 平均 96.5%；Cosmos-Predict2 backbone 的多个变体也超过 95.2%。这些结果接近 OpenVLA-OFT 的 97.1%，但训练步数少很多。

在 SimplerEnv WidowX Visual Matching 上，Qwen3-VL backbone 下 StarVLA-GR00T 达到 65.3%，StarVLA-OFT 达到 64.6%，与强 baseline 竞争。

## 局限性

这篇论文主要贡献是框架和基准，不是新的策略架构。它的价值取决于代码维护、benchmark adapter 质量，以及未来方法是否能自然纳入这个抽象。RL fine-tuning 在文中更多是规划或集成方向，不是当前核心结果。

## 应用到我的机器人

对我的机器人来说，StarVLA 最有价值的是实验工程底座，而不是某个单独模型。可以用它来：

- 固定机器人数据格式和评估流程；
- 在同一数据上比较 OFT、FAST、flow-matching、GR00T-style action head；
- 用统一 policy server 连接仿真和真实机器人；
- 写一个机器人 adapter 处理动作反归一化、夹爪逻辑和安全过滤。

这样可以避免因为数据管线不同而误判模型优劣。

## 实施建议

先实现本地数据 adapter 和机器人 policy-client adapter。第一版用最简单的 StarVLA-OFT 跑通数据闭环；确认训练和执行流程稳定后，再替换成 flow-matching 或 GR00T-style action head 做公平比较。
