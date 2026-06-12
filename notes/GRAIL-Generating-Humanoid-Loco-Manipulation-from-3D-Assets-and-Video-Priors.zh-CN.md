# GRAIL：从 3D 资产和视频先验生成类人机器人移动操作

## 元数据

- 作者：Tianyi Xie, Haotian Zhang, Jinhyung Park, Zi Wang, Bowen Wen, Jiefeng Li, Xueting Li, Qingwei Ben, Haoyang Weng, Yufei Ye, David Minor, Tingwu Wang, Chenfanfu Jiang, Sanja Fidler, Jan Kautz, Linxi Fan, Yuke Zhu, Zhengyi Luo, Umar Iqbal, Ye Yuan
- 会议/年份：arXiv，2026
- 来源：[arXiv PDF](https://arxiv.org/pdf/2606.05160)
- arXiv：2606.05160v1，2026-06-03
- 本地 PDF：[../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.pdf](../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.pdf)
- 转换 Markdown：[../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.md](../papers/GRAIL-Generating-Humanoid-Loco-Manipulation-from-3D-Assets-and-Video-Priors.md)
- 项目页：[GRAIL](https://research.nvidia.com/labs/dair/grail/)
- 代码：[NVlabs/GRAIL](https://github.com/NVlabs/GRAIL)
- 数据集：[nvidia/PhysicalAI-Robotics-Locomanipulation-GRAIL](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Locomanipulation-GRAIL)

## 研究问题

GRAIL 研究的是如何规模化生成类人机器人的移动操作数据，而不需要对每个物体、每个场景和每种地形都做机器人 teleoperation、物理场景搭建或动捕采集。论文的答案是：在真实部署前，整个数据生成流程都保持数字化。

核心假设是：视频基础模型适合作为人类交互行为先验，但不能直接把生成视频当机器人数据。必须先固定 3D 资产、相机参数、真实尺度、环境深度和已经适配目标机器人的人体形态，再让视频模型补充交互动态。

## 核心方法

GRAIL 从一个 3D 物体资产和 simulator-ready 场景开始。系统用 Infinigen 和 Blender 把物体放进已知 3D 配置，渲染第一帧，再让 VLM 生成交互 prompt，最后用 Kling 2.5 Turbo Pro 这类视频基础模型生成一段人-物交互视频。

与重建非受控互联网视频的方法不同，GRAIL 在生成视频前就知道相机内参、外参、物体 mesh、物体纹理、真实尺度、场景深度和按目标机器人比例预拟合的人体角色。这种 privileged setup 显著降低后续 4D 重建里的深度、尺度和形态歧义。

重建阶段先用 GENMO 估计人体运动，用 WiLoR 细化双手，用 FoundationPose 跟踪物体，用 MoGe-2 和渲染场景深度对齐尺度，用 SAM2 做分割，然后通过 keypoint、projection、depth、contact、foot-contact、velocity 和 smoothness loss 联合优化人和物体轨迹。

恢复出的 human-object interaction 会被 retarget 到 Unitree G1。之后 GRAIL 在预训练全身控制器 SONIC 之上训练 task-general tracking policies。对操作任务，它使用 object-aware latent adaptor，在冻结基础控制器的同时注入 latent residual，并输出双手开合 primitive。对地形穿越和坐下任务，它使用 scene-aware tracker，加上局部 height-map encoder 并微调整个控制器。

最后，系统把 tracking policy 蒸馏成第一视角 RGB visual policy，通过视觉 domain randomization 和相机对齐做 sim-to-real，并部署到真实 Unitree G1。

## 关键创新

- 从 3D 资产和视频先验到真实机器人部署的全数字化类人机器人移动操作数据生成。
- Asset-conditioned video generation：视频模型负责生成行为，但几何、尺度、相机和形态由系统预先固定。
- Interaction-aware 4D HOI reconstruction：利用已知 3D 配置降低深度歧义和接触错误。
- 训练 task-general tracker，而不是每条轨迹或每个物体训练一个专用策略。
- 两类互补控制器适配：操作用 object-aware latent adaptation，地形任务用 scene-aware height-map conditioning。
- 只用 GRAIL 生成数据，在真实 Unitree G1 上完成端到端验证。

## 实际解决的问题

GRAIL 解决的是类人机器人数据瓶颈。Teleoperation 和动捕质量高，但每个物体、场景和地形都要真实搭建，成本高且难扩展。纯视频重建覆盖面广，但相机、尺度、物体几何、接触和世界坐标运动都欠约束。

GRAIL 把两者结合起来：视频生成提供多样交互先验，已知 3D 资产和场景几何保证结果可以重建、可仿真、可用于机器人训练。

## 实验结果

GRAIL 生成的数据集包含 2 万多条 Unitree G1 序列，覆盖 pick-up、whole-body manipulation、sitting 和 terrain traversal。数据来自 1000 个物体资产和 1000 个程序生成地形配置。

在 4D HOI 生成评测中，GRAIL 与 HOIDiff、CHOIS 和 DAViD 在 20 个日常物体上比较。GRAIL 在几何质量、interaction score、物体运动平滑度和物理可执行性上整体最好。物理 tracking success rate 为 88.9%，相比之下 DAViD 为 24.0%，HOIDiff 为 15.8%，CHOIS 为 10.5%。

在 task-general loco-manipulation tracking 中，GRAIL 在 43 个物体、124 条运动上评测。完整方法成功率为 81.4%，高于 HDMI 的 48.5% 和 ResMimic 的 49.2%。消融显示，去掉 SONIC、去掉 object-aware adaptor，或者把相对物体观测换成绝对观测，都会降低成功率。

真实机器人部署中，GRAIL 只用生成数据训练第一视角 visual policy。在真实 Unitree G1 上，爬楼成功率为 90%。物体拾取任务在 cube、apple、tea box、carrot 和 wet wipes 上训练，seen objects 平均成功率 84%；在 spray can、lint roller、peach、flashlight 和 medicine bottle 等 unseen objects 上平均成功率 80%。

## 消融实验

重建损失消融表明 projection、depth 和 contact loss 都重要。去掉任意一个，后续 tracking success 会从 81.4% 降到 41.6-53.3%。这说明单独看重建 proxy 指标不够，最终应以机器人可跟踪、可执行为准。

控制器消融说明，仅仅模仿人体动作并不足以完成操作。Vanilla SONIC 的身体跟踪可以很好，但物体操作成功率很低。object-aware adaptor 和相对物体观测是把人-物参考轨迹转成机器人可执行操作的关键。

## 局限性

GRAIL 假设有可用的 3D 物体资产、可仿真的场景和能按要求生成交互的视频基础模型。如果视频模型改变物体外观、产生快速运动或严重遮挡，跟踪质量会下降，失败过滤会丢弃不少序列。

计算成本很高。附录报告，单条 5 秒、121 帧 4D HOI 序列在单张 A100 上约需 14 分钟，主要耗在 joint optimization。Tracker 训练使用 64 张 NVIDIA L40，每张 1024 个并行环境，PPO 训练 30000 次迭代，完整 task-family run 约 30 小时。

Task-general tracker 可以在相关 motion family 内分摊训练成本，但当任务族变化较大时仍需要重新训练或微调。真实机器人验证很强，但主要集中在 Unitree G1、物体拾取和爬楼，跨硬件泛化还需要更多证据。

实际使用还要注意许可。GitHub 项目采用 NVIDIA 非商业许可证，生产或商业使用需要单独做法律确认。

## 应用到我的机器人

如果我的机器人项目需要大量类人或全身操作行为，而机器人 teleoperation 数据太贵，GRAIL 的路线很有价值：先数字化生成训练参考，再在仿真里筛选和验证，最后再上真实机器人。

对我的机器人，可复用的设计是：

- 收集或生成准确的 3D 物体和环境资产；
- 渲染已知 3D 场景配置，而不是依赖非受控视频；
- 用视频基础模型提出人类式交互运动；
- 用真实尺度、物体几何和接触约束重建 4D HOI；
- retarget 到我的机器人运动学骨架；
- 先训练 physics tracker，再训练 visual policy；
- 真实部署只作为最后验证阶段。

如果我的机器人不是 Unitree G1，主要额外工作是机器人专属 retargeting、全身控制器或 tracking policy，以及动作空间适配。GRAIL 的数据思想仍然可迁移：生成阶段可以有创造性，但重建和策略训练必须被几何约束住。

## 实施建议

最小复现可以从一个物体类别和一个行为开始，例如从桌上拿起盒子。第一目标不是直接真实部署，而是在仿真中让机器人稳定跟踪一条重建的 4D HOI 轨迹，并且物体不漂移、接触不崩。

最高风险模块是视频模型一致性、物体姿态跟踪、接触对齐和 retargeting。每一阶段都要做可视化诊断。如果生成视频里的物体跨帧变形，或者 FoundationPose 丢失物体，后面训练出的策略很可能学习到错误行为。

对算力较小的团队，更现实的路线是优先使用作者发布的数据集，只微调窄任务族 tracker；只有在数据集中缺少目标物体或场景时，再额外生成新视频。
