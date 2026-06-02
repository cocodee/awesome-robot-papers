# Qwen-VLA: 统一任务、环境和机器人本体的视觉-语言-动作建模

## 元数据

- 作者：Qwen Team
- 来源：https://arxiv.org/pdf/2605.30280
- arXiv：2605.30280v1，2026-05-28
- 本地 PDF：[../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.pdf](../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.pdf)
- 转换 Markdown：[../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.md](../papers/Qwen-VLA-Unifying-Vision-Language-Action-Modeling-across-Tasks-Environments-and-Robot-Embodiments.md)
- 博客：https://qwen.ai/blog?id=qwenvla
- 代码：https://github.com/QwenLM/Qwen-VLA

## 研究问题

Qwen-VLA 研究的是：操作、导航、轨迹预测和第一视角具身动作建模，是否可以统一到一个 VLA 模型里，而不是为每类任务或每种机器人单独训练系统。

## 核心方法

Qwen-VLA 基于 Qwen3.5-4B vision-language backbone，并加入一个约 1.15B 参数的 DiT-style flow-matching action expert。模型根据视觉观测、语言指令、任务标识和 embodiment-aware prompt，预测连续动作或轨迹 chunk。

embodiment prompt 会描述机器人平台、手臂配置、控制频率、控制约定和预测 horizon。Qwen-VLA 不强行把所有机器人动作转换成同一种物理语义，而是保留各数据集原生动作定义，用统一 padded tensor 和 mask 来训练一个共享 action expert。

训练分四阶段：T2A text-to-action 预训练先让 decoder 在没有图像的情况下学习语言条件动作先验；CPT continued pretraining 把动作先验 grounding 到视觉观测；SFT 对目标任务和真实机器人数据对齐；RL 在仿真中用任务成功奖励进一步优化，得到 Qwen-VLA-Instruct。

## 关键创新

- 用统一 action-and-trajectory prediction 覆盖操作、导航、轨迹预测和人类第一视角动作。
- 用 embodiment-aware prompt 表达机器人控制语义。
- 用 shared padded action tensor + validity mask 避免为每个机器人单独设计输出头。
- 渐进训练 recipe：T2A、CPT、SFT、RL。
- 联合使用机器人轨迹、人类第一视角示教、合成仿真、VLN、空间 grounding、自动驾驶 VQA 和通用 VL 数据。

## 实际解决的问题

Qwen-VLA 解决的是任务和本体碎片化问题。一个模型可以通过 prompt 适配不同机器人平台，并输出不同格式的连续控制信号，减少维护多个操作、导航和轨迹模型的成本。

它也解决了 VLM backbone 已经预训练、action decoder 随机初始化时训练不稳定的问题。T2A 阶段先给 action decoder 建立结构化动作先验，再进入视觉 grounding。

## 实验证据

作为单一 generalist policy，Qwen-VLA-Instruct 在 LIBERO 达到 97.9%，RoboCasa-GR1 达到 56.7%，Simpler-WidowX 达到 73.7%，RoboTwin Easy/Hard 达到 86.1%/87.2%，在多个 benchmark 上超过多数 specialist baseline。

在真实 ALOHA 任务上，从 Qwen-VLA-Base 微调得到 83.6% 平均 in-domain 成功率，而从零训练只有 48.5%。在 OOD ALOHA 测试上，预训练版本平均成功率 76.9%，明显高于 pi0.5 的 41.5%。

导航任务中，Qwen-VLA-Instruct 在 R2R Val-Unseen 上 SR 为 57.5，在 RxR Val-Unseen 上 SR 为 59.6，在多数指标上领先开源 baseline。

## 局限性

模型很大：Qwen3.5-4B 加上 1.15B action expert。统一 tensor 和 mask 能处理不同动作维度，但不能完全消除不同本体之间的语义差异。真实机器人结果主要在 ALOHA 上展示，还需要更多硬件验证。RL 阶段在仿真中完成，迁移到真实机器人时可能受平台影响。

## 应用到我的机器人

如果我的机器人需要同时做操作和导航，或者希望一个模型支持多个机器人配置，Qwen-VLA 的设计很有参考价值。实际路线是：

- 写 embodiment prompt，明确机器人类型、手臂、底盘、FPS 和 action horizon；
- 把我的机器人控制命令映射到固定 action tensor 的前若干通道；
- 对不用的通道 mask，并按数据集归一化；
- 保留本机器人原生控制约定，不强行套用别的机器人动作语义；
- 如果有命令日志但图像质量不足，可以先做 T2A-style action pretraining；
- 最后从预训练 checkpoint 微调到真实硬件。

对我的机器人最直接可复用的是 embodiment-aware prompt 和 masked action tensor。

## 实施建议

训练前先定义 action schema 和 prompt 模板。第一步可以只做操作任务：固定 `K` 个动作通道和 mask，跑通后再加入底盘或导航 waypoint。加入多任务数据前，必须先验证动作归一化和 mask 是否正确。
