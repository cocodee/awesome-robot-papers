# HoloBrain-0 Technical Report

## 元数据

- 作者：Xuewu Lin, Tianwei Lin, Yun Du, Hongyu Xie, Yiwei Jin, Jiawei Li, Shijie Wu, Qingze Wang, Mengdi Li, Mengao Zhao, Ziang Li, Chaodong Huang, Hongzhe Bi, Lichao Huang, Zhizhong Su
- 会议/年份：arXiv，2026
- 来源：https://arxiv.org/pdf/2602.12062
- arXiv：2602.12062v1，2026-02-12
- 本地 PDF：[../papers/HoloBrain-0-Technical-Report.pdf](../papers/HoloBrain-0-Technical-Report.pdf)
- 本地 Markdown：[../papers/HoloBrain-0-Technical-Report.md](../papers/HoloBrain-0-Technical-Report.md)
- 项目页：https://horizonrobotics.github.io/robot_lab/holobrain
- 代码：https://github.com/HorizonRobotics/RoboOrchardLab

## 研究问题

HoloBrain-0 关注的问题是：如何把 VLA 基础模型研究真正落到可靠的真实机器人部署。论文同时处理三个难点：跨机器人本体泛化、高质量数据低成本采集，以及真实机器人上的低延迟控制。

本文的核心判断是，VLA 不应该把机器人硬件差异当成隐含噪声去拟合，而应该显式使用相机标定、深度和机器人运动学结构，让模型知道自己在控制什么身体、从什么视角看世界。

## 核心方法

HoloBrain-0 是一个完整 VLA 系统栈，主要包括三部分。

第一部分是 VLM 语义骨干，用来处理视觉和语言。论文报告了两个版本：HoloBrain-0-GD 使用 GroundingDINO Tiny，总参数约 0.2B；HoloBrain-0-QW 使用裁剪后的 Qwen2.5-VL-3B，总参数约 1.1B。

第二部分是 perspective-aware Spatial Enhancer，用来注入几何信息。它利用多视角 RGB-D、相机内参和外参，把视觉特征投影到统一 3D 坐标系中。论文还把投影参考系从各机器人底座改成中心固定相机坐标系，这样更容易混合不同机器人和人类第一视角数据。

第三部分是 embodiment-aware Action Expert，用来建模机器人运动学链。它用每个关节的 6D 位姿表示机器人状态，屏蔽大多数原始关节角，避免不同 URDF 和零位定义带来的歧义；输出则是混合相对动作空间，同时预测每个关节的关节残差和笛卡尔位姿变化。Action Expert 使用 joint-graph attention，并以扩散式动作生成和 x-prediction 训练。

部署方面，论文提出 SimpleRTC 和 teacher-forcing 训练来支持异步推理，目标是避免机器人执行完一个动作块后停下来等待下一次模型推理。

## 关键创新

最重要的创新是把机器人本体显式放进 VLA 架构里。很多 VLA 方法依赖文本 prompt、异构 encoder 或共享动作格式来处理多机器人数据；HoloBrain-0 则直接引入物理结构：相机标定、深度、URDF 运动学链、关节位姿和相对 SE(3) 动作。

第二个关键点是 test-driven data strategy。它不是简单增加完整示教，而是反复部署模型、统计失败、聚类失败模式，然后针对性采集恢复片段或状态扩展数据。对长程、柔性物体和双臂任务来说，这比盲目扩大数据集更高效。

第三个贡献是 RoboOrchard 工具链。论文开源了覆盖数据采集、验证、训练、模型打包和部署的基础设施，包括 MCAP 日志、Arrow 训练数据、包含部署上下文的模型 artifact，以及同步/异步推理接口。

## 实际解决的问题

HoloBrain-0 通过把相机几何和运动学结构作为一等输入，缓解跨机器人训练中的表示不一致问题。这对混合多种机械臂、双臂平台、移动/类人平台、仿真数据和人类示教数据尤其重要。

它也降低了部署难度。HoloBrain-0-GD 总参数 183.70M，可训练参数 74.81M；HoloBrain-0-QW 总参数 1080.86M，可训练参数 412.17M。论文认为这种小 Action Expert 的设计比许多大型 VLA 基线更适合边缘端或低延迟部署。

数据方面，预训练语料超过 1.56 亿帧、3500 多小时，覆盖 7 种本体；但真实任务 post-training 强调用更有针对性的数据获得性能，例如每个长程任务约 30 小时数据。

## 实验证据

真实双臂 Piper 机器人 10 个任务上，HoloBrain-0-QW 平均成功率 77.18%，高于 pi0.5 的 69.16% 和 pi0 的 45.39%；HoloBrain-0-GD 平均成功率 74.81%。长程任务上提升明显：HoloBrain-0-QW 在 Fold Clothes 上成功率 75.00%，在 Fold Paper Box 上成功率 95.00%。

RoboTwin 2.0 的 50 个任务上，HoloBrain-0-GD 在 clean/randomized 设置下分别达到 91.30%/90.80%；HoloBrain-0-QW 达到 91.90%/92.30%。按论文表格，平均 randomized 成功率超过 pi0.5、X-VLA、Lingbot-VLA 和 Motus。

标准 LIBERO 上，HoloBrain-0-QW 平均成功率 97.4%，接近表中最好方法。zero-shot LIBERO-Plus 上，HoloBrain-0-GD 平均 74.0%，高于 OpenVLA-OFT 的 69.6% 和 X-VLA 的 69.7%。

GenieSim 2.2 上，HoloBrain-0-QW 总进度分 4.685，略高于 X-VLA 的 4.541。

消融实验显示，七个基础任务与 Grasp Anything 共同训练后，平均成功率从 72.40% 提升到 75.00%。SimpleRTC 与 teacher-forcing 的分析表明，异步推理可以减少动作停顿，并提升布料折叠这类需要平滑控制的任务表现。

## 局限性

这个方法非常依赖标定和运动学元数据质量。如果相机外参、深度、URDF 或关节位姿投影不准，显式几何先验会把系统性错误直接注入模型。

论文是一个大系统技术报告，性能提升来自架构、数据规模、数据清洗、post-training 和基础设施的组合。虽然有消融实验，但仍然不容易完全拆分每个组件的独立贡献。

论文也把严格指令跟随列为未来工作，尤其是容易混淆的指令。目前主要是 imitation learning，作者计划下一步加入 off-policy RL，这说明现阶段策略在恢复能力和长尾失败上仍可能受限于示教分布。

## 应用到我的机器人

如果我的机器人有多相机、明确运动学链，并且任务强依赖空间几何，HoloBrain-0 的思路很值得借鉴。实际落地路径可以是：

- 保持每个相机视角的内参和外参准确；
- 维护干净的 URDF 或等价运动学描述；
- 同步记录 RGB-D、机器人本体状态、语言或任务标签、动作轨迹；
- 增加数据验证器，把关节或连杆位姿反投影到图像中，自动发现标定错误和标签错误；
- 训练时不要只喂平面图像和关节数组，而是引入 3D-aware 视觉特征和 joint-centric 状态表示；
- post-training 采用目标驱动数据采集：先部署测试，归类失败，再采集短恢复片段和状态扩展示教。

对我的机器人来说，第一步不建议直接复现完整 HoloBrain-0。更合理的最小实验是在同一数据集上比较普通模仿学习策略和 embodiment-aware 策略，重点评估相机扰动、物体位姿扰动和背景变化下的成功率，而不是只看原始示教分布。

需要的传感器和计算包括多视角 RGB-D、准确相机位姿、机器人关节状态、URDF，以及能训练或微调紧凑 VLA/action expert 的 GPU。预期收益是更好的空间精度、更平滑的长程动作执行，以及更好的跨相机或跨机器人变体迁移。主要风险是标定维护成本、计算成本、异步执行时的控制安全，以及隐藏的数据质量问题。

## 实施建议

优先做数据层，再做模型层。最高收益的基础设施是一个自包含 episode 格式，里面同时有 RGB-D 帧、相机参数、机器人状态、动作和语言指令。先加自动检查：缺帧、时间戳漂移、相机标定不一致、关节或连杆投影不可能等。

策略训练时，可以把 HoloBrain-0 作为设计目标：标定多视角感知、显式运动学、joint-centric 动作解码器。如果机器人已经使用 ROS 2，可以直接评估 RoboOrchardLab，因为它就是论文发布的配套栈。
