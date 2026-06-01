# LDA-1B: 通过通用具身数据摄入扩展潜在动力学动作模型

## 元数据

- 作者：Jiangran Lyu, Kai Liu, Xuheng Zhang, Haoran Liao, Yusen Feng, Wenxuan Zhu, Tingrui Shen, Jiayi Chen, Jiazhao Zhang, Yifei Dong, Wenbo Cui, Senmao Qi, Shuo Wang, Yixin Zheng, Mi Yan, Xuesong Shi, Haoran Li, Dongbin Zhao, Ming-Yu Liu, Zhizheng Zhang, Li Yi, Yizhou Wang, He Wang
- 来源：https://arxiv.org/pdf/2602.12215
- arXiv：2602.12215v1，2026-02-12
- 本地 PDF：[../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.pdf](../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.pdf)
- 转换 Markdown：[../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.md](../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.md)
- 项目页：https://pku-epic.github.io/LDA

## 研究问题

这篇论文关注机器人基础模型如何突破“只在高质量专家示教上做行为克隆”的限制。核心观点是：异构具身数据里包含可迁移的物理动力学知识，即使是低质量轨迹和没有动作标注的人类视频，只要分配合适的训练目标，也能帮助机器人学习。

## 核心方法

LDA-1B 是一个约 1.6B 参数的 unified world model，通过 universal embodied data ingestion 训练。它同时学习 policy prediction、forward dynamics、inverse dynamics 和 visual forecasting。模型不直接预测未来像素，而是在结构化 DINO latent space 中预测未来视觉特征，从而减少对背景、光照和纹理等无关外观细节的建模负担。

架构上，LDA-1B 使用 multi-modal diffusion transformer，同时 denoise 动作块和未来视觉 latent，并通过 VLM token、扩散时间步和任务 embedding 进行条件控制。

论文还构建了 EI-30K 数据集，包含 3 万小时以上的具身交互数据：真实机器人数据、仿真机器人数据、带动作的人类示教，以及没有动作标注的人类视频。高质量轨迹用于 policy 和 dynamics；低质量轨迹用于 dynamics 和 visual forecasting；无动作视频用于 visual forecasting。

## 关键创新

- 按数据角色训练：不同质量的数据服务不同目标，而不是简单过滤低质量数据。
- DINO latent dynamics：在语义 latent 空间预测未来状态，而不是像素或 VAE latent。
- 多任务 unified training：一个模型同时学习策略、正向动力学、逆动力学和视觉预测。
- 手部中心动作空间：对齐机器人和人类的末端执行器、夹爪或灵巧手表示。

## 实际解决的问题

LDA-1B 解决的是机器人基础模型的数据利用瓶颈。传统行为克隆主要依赖干净的专家动作示教，而这篇论文展示了如何利用不完美轨迹和无动作视频来学习可迁移的物理动力学。

它尤其针对接触丰富、灵巧操作和长时序任务。这类任务需要模型理解动作后果、接触持续性和时间一致性，而不只是识别当前图像。

## 实验证据

在 RoboCasa-GR1 上，LDA-1B 成功率为 55.4%，高于 GR00T-N1.6 的 47.6%、StarVLA 的 47.8% 和 GR00T-EI30k 的 51.3%。从 VAE latent 换成 DINO latent 是关键因素：使用 VAE latent 的 UWM 变体只有 14.2% 到 20.0%。

论文报告相对 π0.5，在接触丰富任务上最多提升 21%，灵巧操作任务上最多提升 48%，长时序任务上最多提升 23%。在混合质量微调中，加入 30% 低质量轨迹让 LDA-1B 提升 10%，而 π0.5 反而下降。

## 局限性

该方法训练成本很高：论文报告使用 48 张 H800、训练 400k iterations，总计 4,608 GPU hours。模型依赖固定 DINO 视觉特征，并主要使用头戴式第一视角图像，这可能限制它迁移到新的相机布局或多模态传感器。当前转换出的 Markdown 是文本版，精确表格和图示仍应以原 PDF 为准。

## 应用到我的机器人

如果我的机器人数据质量参差不齐，这篇论文很有价值。不要只保留最干净的成功示教，可以把失败、停顿、绕路和低效率轨迹用于动力学或未来 latent 预测，把高质量数据用于 policy 学习。

实际落地路径：

- 把所有机器人示教转换成统一的 LeRobot 风格格式；
- 统一末端执行器 delta、夹爪宽度或灵巧手关键点表示；
- 给轨迹打质量标签，而不是直接删除低质量轨迹；
- 用高质量 episode 训练策略目标；
- 用更大范围的混合质量数据训练 dynamics 和 future-latent prediction；
- 评估 DINO-latent 预测是否改善恢复能力、接触处理和长时序一致性。

对我的机器人来说，最直接的应用是建立一个按数据用途分类的数据摄入流程：哪些数据适合学动作，哪些数据适合学物理变化。这样可以降低示教采集成本，并让不完美遥操作日志也产生价值。

## 实施建议

不要一开始复现 1B 规模模型。先在本地操作数据上做小实验：在原有策略训练之外加入 DINO latent 未来预测损失，观察成功率、失败恢复和接触稳定性是否提升。工程重点是数据规范化，包括相机时间戳、动作频率、末端坐标系、夹爪或手部表示，以及轨迹质量标签。
