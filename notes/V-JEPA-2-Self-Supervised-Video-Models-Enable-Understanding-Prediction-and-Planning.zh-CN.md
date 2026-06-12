# V-JEPA 2：自监督视频模型实现理解、预测与规划

## 元数据

- 作者：Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba Komeili, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, Nicolas Ballas
- 会议/年份：arXiv，2025
- 来源：https://arxiv.org/pdf/2506.09985
- arXiv：2506.09985v1，2025-06-11
- 本地 PDF：[../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.pdf](../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.pdf)
- 本地 Markdown：[../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.md](../papers/V-JEPA-2-Self-Supervised-Video-Models-Enable-Understanding-Prediction-and-Planning.md)
- 代码：https://github.com/facebookresearch/vjepa2
- 博客：https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks

## 研究问题

机器人可用的世界模型能否主要从观察中学到，而不是依赖大量任务特定的机器人交互数据和奖励标注？V-JEPA 2 关注的问题是：互联网规模的自监督视频预训练，是否能学出支持理解、预测和真实机器人规划的表示，并且只需要少量机器人数据进行后训练。

## 核心方法

系统分两阶段。第一阶段，V-JEPA 2 在超过 100 万小时互联网视频和图像上做 JEPA 风格的自监督预训练。训练目标是在 latent 表示空间中预测被 mask 掉的视频 patch 表示，而不是重建像素，因此模型更关注可预测的场景结构和运动。

第二阶段，冻结预训练视频编码器，在少于 62 小时的 DROID 无标注机器人视频上训练一个约 300M 参数的 action-conditioned predictor，称为 V-JEPA 2-AC。该 predictor 输入当前图像特征、末端执行器状态和动作，自回归预测未来帧的 latent 表示，并同时使用 teacher-forcing loss 和短 rollout loss。

控制时，机器人接收一张目标图像。每个控制周期中，系统用 Cross-Entropy Method 采样候选动作序列，在 latent 世界模型中向前 rollout，选择预测 latent 状态最接近目标 latent 状态的动作序列，只执行第一个动作，然后重新观测和规划。

## 关键创新

核心创新是把大规模 action-free 视频 JEPA 作为机器人 action-conditioned latent world model 的表示基础。它不是通过慢速像素级视频生成来规划，而是在表示空间中规划。这样可以用少量机器人数据和无奖励设置，实现真实机器人的模型预测控制。

论文还表明，没有语言监督的视频编码器也可以后续对齐到 LLM，并在视频问答上取得强结果。这说明物理和时间理解可以先从视频观察中学到，再进行语言对齐，而不必完全依赖图文字幕数据。

## 实际解决的问题

V-JEPA 2 主要解决三个工程瓶颈：

- 大规模机器人数据昂贵，而无标注互联网视频丰富；
- 像素级视频生成用于闭环规划时计算代价高；
- 任务特定奖励设计和目标环境采集会拖慢部署。

对机器人来说，最重要的是它能零样本迁移到两个实验室中的 Franka 机械臂，这些环境没有出现在 DROID 数据里；输入只需要未标定的低分辨率单目 RGB 相机和目标图像。

## 实验证据

在视频理解上，V-JEPA 2 在 Something-Something v2 上报告 77.3 top-1 accuracy。在人类动作预测上，它在 EPIC-KITCHENS-100 上报告 39.7 Recall@5。对齐 8B LLM 后，它在视频问答任务上报告了例如 PerceptionTest 84.0、TempCompass 76.9 的结果。

在机器人控制上，V-JEPA 2-AC 使用约 23k 条 DROID 轨迹、少于 62 小时视频训练。零样本操作实验中，它报告平均 reach 成功率 100%，cup grasp 65%，box grasp 25%，cup reach-with-object 75%，box reach-with-object 75%，cup pick-and-place 80%，box pick-and-place 65%。与 Cosmos action-conditioned 视频生成基线相比，在 Lab 2 上 V-JEPA 2-AC 每个动作规划约 16 秒，而 Cosmos 需要约 4 分钟，并且 V-JEPA 2-AC 在物体交互任务上表现更好。

## 局限性

规划速度仍然偏慢：16 秒一个动作适合研究验证，但不适合快速闭环操作。机器人任务也偏短时域，pick-and-place 依赖中间图像子目标；如果没有子目标，长时域规划会受到自回归 latent 预测误差累积和动作搜索空间膨胀的限制。

模型对相机位置敏感，因为它要在没有显式标定的情况下，从单目 RGB 中隐式推断机器人动作坐标轴。实验主要是 Franka 桌面操作，尚未证明能稳定迁移到移动操作、双臂、柔性物体或更复杂的接触丰富场景。

## 对机器人研究的影响

这篇论文给出了一个实用蓝图：用 learned latent dynamics model 做目标图像条件的视觉伺服。它特别适合目标实验室示教数据有限，但可以复用强视频表示和少量通用机器人轨迹数据的情况。

关键工程启发是把表示学习和 action-conditioned dynamics learning 分开：先预训练或复用通用视频编码器，冻结后再用机器人数据训练小一些的 dynamics head。这样能降低机器人数据需求，并在投入完整 VLA 策略之前，先验证 latent planning 是否对当前机器人有效。

## 应用到我的机器人

对我的机器人，建议先从受限桌面操作开始：固定或标定好的 RGB 相机、末端笛卡尔动作、夹爪状态和目标图像。用本地示教或 DROID 风格数据训练 action-conditioned latent predictor，然后在 reach、grasp 和简单 pick-and-place 上测试模型预测控制。

所需传感器和计算包括 RGB 相机、末端执行器状态、夹爪状态、用于 latent planning 的 GPU，以及能安全执行小幅笛卡尔 delta 的底层控制器。预期收益是更高数据效率、无需奖励工程的目标图像条件控制，以及一个可复用到后续策略学习的世界模型组件。主要风险是规划慢、相机视角敏感、夹爪时序不准，以及长任务上的预测误差累积。

## 实施建议

最小可行实验不应从复现完整 1B 参数 V-JEPA 2 预训练开始。更合理的是复用公开 V-JEPA 2 权重，冻结编码器，在窄域机器人数据上训练小型 action-conditioned predictor。然后用同样目标图像条件与 behavior cloning 对比。如果 latent planning 在偏离示教状态后的恢复能力更好但速度太慢，可以把世界模型用于生成训练目标或初始化一个更快的前馈策略。
