# Fast-WAM: World Action Models 是否需要在测试时想象未来？

## 元数据

- 作者：Tianyuan Yuan, Zibin Dong, Yicheng Liu, Hang Zhao
- 来源：https://arxiv.org/pdf/2603.16666
- arXiv：2603.16666v2，2026-03-23
- 本地 PDF：[../papers/Fast-WAM-Do-World-Action-Models-Need-Test-time-Future-Imagination.pdf](../papers/Fast-WAM-Do-World-Action-Models-Need-Test-time-Future-Imagination.pdf)
- 项目页：https://yuantianyuan01.github.io/FastWAM/

## 研究问题

World Action Models 通常会先生成未来视频帧，再根据这些“想象出来的未来”预测机器人动作。本文要回答的问题是：测试时显式生成未来画面是否真的必要，还是说 WAM 的主要收益其实来自训练阶段的视频预测任务？

## 核心方法

Fast-WAM 在训练时保留视频 co-training，但在推理时去掉未来视频生成。模型使用 Wan2.2-5B 的视频 Diffusion Transformer 作为骨干，并复用文本编码器和视频 VAE，同时加入一个 action expert DiT 来生成动作块。训练时，模型同时优化动作生成和未来视频 latent 预测的 flow-matching 目标；推理时，模型只对当前观测和语言指令做一次编码，然后直接从学到的 latent world representation 预测动作块。

## 关键创新

本文的关键创新不是提出更复杂的未来视频生成器，而是把 WAM 中常常混在一起的两个因素拆开比较：

- 训练阶段的视频 co-training；
- 推理阶段的显式未来视频生成。

实验表明，训练时的视频建模目标比运行时生成未来帧更重要。这样可以把 WAM 的表征学习优势保留下来，同时让部署接口接近实时直接策略。

## 实际解决的问题

Fast-WAM 主要解决 imagine-then-execute WAM 的高推理延迟问题。已有方法通常需要迭代 denoise 未来视频，然后才能输出动作。Fast-WAM 在推理时移除未来视频分支，论文报告延迟为 190 ms，比文中较慢的 imagine-then-execute 变体快 4 倍以上。

它还提升了数据效率。Fast-WAM 在 RoboTwin 和 LIBERO 上不使用 embodied pretraining 也能保持有竞争力的结果，说明视频 co-training 能提供有用的物理动态和时间结构先验。

## 实验证据

在 RoboTwin 上，Fast-WAM 成功率为 91.8%，接近 Fast-WAM-IDM 的 91.3% 和 Fast-WAM-Joint 的 90.6%。去掉视频 co-training 后，成功率降到 83.8%。

在 LIBERO 上，Fast-WAM 平均成功率为 97.6%，接近 Fast-WAM-Joint 的 98.5% 和 Fast-WAM-IDM 的 98.0%。去掉视频 co-training 后降到 93.5%。

在真实毛巾折叠任务中，去掉视频 co-training 会明显降低成功率；而 Fast-WAM 在保持较低延迟的同时，仍然有较强的真实任务表现。

## 局限性

该方法仍依赖大型视频骨干和约 6B 参数模型，实际部署可能需要高端 GPU、模型蒸馏或更小模型复现。真实世界实验主要集中在毛巾折叠，还需要更多任务验证，例如移动操作、双臂协作、工具使用和接触丰富的装配任务。论文也把更大规模预训练数据和模型 scaling 留作未来工作。

## 应用到我的机器人

如果机器人需要快速闭环操作，但不能承受测试时生成未来视频的延迟，这篇论文的思路很值得采用。一个实际适配方案是：

- 收集观测、语言或任务标签、动作轨迹和短未来图像序列；
- 训练时加入未来帧 latent 预测损失；
- 部署时关闭未来帧生成；
- 让策略直接根据当前相机观测和任务指令输出动作块。

对我的机器人来说，这个方向适合实时操作任务，例如折叠、分拣、抓取放置、双臂交接和视觉伺服。所需输入包括同步相机图像、语言指令或任务标签、机器人动作轨迹，以及覆盖目标任务分布的示教数据。主要风险包括 GPU 延迟、动作安全、训练相机配置与真实部署不一致，以及接触丰富场景中的数据不足。

## 实施建议

不要一开始就复现完整 6B 模型。更合理的最小实验是：在同一机器人数据集上比较两个策略，一个只训练动作预测，另一个额外加入未来帧 latent 预测损失。如果带视频 co-training 的策略在成功率、恢复能力或泛化上更好，同时推理延迟没有明显增加，就说明 Fast-WAM 的原则值得继续投入。
