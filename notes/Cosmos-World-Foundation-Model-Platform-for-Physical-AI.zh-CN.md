# Cosmos World Foundation Model Platform for Physical AI

## 元数据

- **来源:** <https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf>
- **本地 PDF:** [papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.pdf](../papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.pdf)
- **转换 Markdown:** [papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.md](../papers/Cosmos-World-Foundation-Model-Platform-for-Physical-AI.md)
- **类型:** NVIDIA 技术报告，2026

## 研究问题

能不能用一个统一的基础模型平台，把 VLM、视频生成器、前向动力学模型、逆动力学模型和机器人策略这些原本分散的模块统一起来，用于 Physical AI？

## 方法

Cosmos 3 是一个面向语言、图像、视频、音频和动作的 omnimodal world model。它使用各模态专用编码器、统一 token 排列方式，以及 Mixture-of-Transformers 架构。自回归 token 负责理解和推理，扩散 token 负责通过去噪生成图像、视频、音频和动作。

对机器人来说，关键是它把 action 当成核心模态。报告把不同本体的控制量映射为相对位姿和抓取状态，再通过 domain-aware projection 适配不同机器人或运动域。同一个模型通过改变哪些 video/action token 是条件、哪些是生成目标，支持前向动力学、逆动力学和 policy 三种模式。

## 关键创新

这篇报告的创新不只是某个机器人策略技巧，而是一个统一的 Physical AI 平台：感知、仿真、动作反推和动作生成共享同一个模型骨干和训练流程。

关键点：

- action token 和语言、图像、视频、音频一起建模，而不是只在末尾加一个策略头。
- 前向动力学、逆动力学和策略学习被表示成不同的 token 条件模式。
- 在大规模多模态预训练之后，mid-training 阶段加入 action 和 video transfer 数据。
- `Cosmos3-Nano-Policy-DROID` 这类专用模型通过 post-training 获得，不需要改核心架构。
- 合成数据生成、机器人策略学习和 benchmark 基础设施被放进同一个平台闭环。

## 实验

报告评估了 Cosmos 3 的推理、图像/视频/音频生成、transfer generation、前向/逆动力学和机器人策略能力。

机器人相关结果：

- action mid-training 使用 8.4M episodes 和 61.3K hours，覆盖 egocentric motion、robotics、autonomous vehicles 和 camera motion。
- robotics 数据占 5.4K hours，来自 AgiBot、Franka Panda、Google Robot、WidowX、UMI、UR 等数据源。
- DROID 前向动力学上，Cosmos3-Super mid-training 初始化达到 26.04 PSNR，高于 Ctrl-World 的 22.99。
- `Cosmos3-Nano-Policy-DROID` 在 RoboLab specific instruction 下达到 39.7% 成功率，高于 pi0.5 的 28.1% 和 DreamZero 的 25.2%。
- LIBERO-10 新本体适配中，mid-trained 初始化在 500 iterations 达到 24.6%，2000 iterations 达到 97.4%；而普通 pre-trained 初始化在 500 iterations 仍是 0.0%。

## 局限

这是平台级技术报告，依赖非常大的数据和算力。mid-training 使用 1024 到 2048 张 NVIDIA GB200 GPU，小实验室基本无法完整复现。DROID policy pilot 主要是 Franka 风格桌面操作，迁移到移动操作或人形机器人还需要针对本体做 post-training。部分结果来自 leaderboard，后续排名可能变化。

## 对机器人研究的实际影响

Cosmos 3 更适合作为机器人学习系统设计蓝图：

- 不只用行为克隆训练策略，而是从 world-action prior 上继续微调。
- 用前向动力学预测视频结果，在真实执行前评估动作 chunk 的风险。
- 用逆动力学从被动视频中挖掘动作或 pseudo-action。
- 用合成和 transfer generation 扩展长尾场景、相机视角和物体组合。
- action 表示应保持几何化和本体感知，不要直接绑定到底层控制器细节。

## 应用到我的机器人

对我的机器人，最可行的路线不是复现完整 Cosmos 3，而是借鉴它的训练结构：

- 把动作表示为末端相对位姿增量加夹爪状态，并加入 proprioception。
- 采集多视角机器人示教，配语言指令，同时保留成功和失败轨迹。
- 用 DROID-like 数据格式微调现成 VLA 或 world-action model。
- 增加未来视频预测辅助损失，让策略学习动作后果，而不只是模仿动作。
- 把预测视频 rollout 作为执行前的安全检查和调试信号。

需要的传感器和算力：腕部相机、一到两个外部 RGB 相机、机器人 proprioception、夹爪状态，以及至少一张较强 GPU 做微调或推理。预期收益是对新物体和新指令更泛化。主要风险是推理延迟、动作标定误差，以及模型生成“看起来合理但物理上错误”的未来视频。
