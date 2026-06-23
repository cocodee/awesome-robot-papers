# Qwen-RobotManip 技术报告：Alignment 解锁机器人操作基础模型的规模化

## 元数据

- 作者：Haoqi Yuan, Zhixuan Liang, Anzhe Chen, Ye Wang, Haoyang Li, Pei Lin,
  Yiyang Huang, Zixing Lei, Tong Zhang, Jiazhao Zhang, Jie Zhang, Jingyang Fan,
  Gengze Zhou, Qihang Peng, Chenxu Lv, Xiaoyue Chen, An Yang, Fei Huang,
  Junyang Lin, Dayiheng Liu, Jingren Zhou, Chenfei Wu, Xiong-Hui Chen
- 会议/年份：arXiv，2026
- 来源：[arXiv PDF](https://arxiv.org/pdf/2606.17846)
- arXiv：2606.17846v2，2026-06-17
- 本地 PDF：
  [../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.pdf](../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.pdf)
- 转换 Markdown：
  [../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.md](../papers/Qwen-RobotManip-Technical-Report-Alignment-Unlocks-Scale-for-Robotic-Manipulation-Foundation-Models.md)
- 项目页：[Qwen-RobotManip](https://qwen.ai/blog?id=qwen-robotmanip)
- 代码：[QwenLM/Qwen-RobotManip](https://github.com/QwenLM/Qwen-RobotManip)

## 研究问题

Qwen-RobotManip 研究的是：语言模型和多模态模型里的规模化训练规律，能否迁移到机器人操作基础模型。难点在于机器人数据天然异构：不同机器人有不同状态维度、动作空间、坐标系、相机、夹爪、控制频率和采集流程。如果不先对齐，简单扩大数据量会制造冲突，而不是产生可迁移能力。

论文的核心结论是：先 alignment，再 scale。它用统一跨本体状态动作表示、camera-frame 末端执行器动作、in-context policy adaptation，以及 VL/VLA 联合训练，把开源机器人数据、第一视角人类视频、合成人到机器人数据和视觉语言数据放进同一个训练体系。

## 核心方法

Qwen-RobotManip 使用 Qwen3.5-4B 作为视觉语言 backbone，并接一个 flow-matching Diffusion Transformer action expert。backbone 处理多视角图像、语言指令、结构化 embodiment prompt 和历史上下文；action expert 用连续 flow matching 预测动作块，推理时使用 4 步 Euler integration。

状态和动作接口是一个 80 维 canonical vector。它包含两个 29 维手臂 block 和 22 个保留维度。每个手臂 block 包含关节位置、9D 末端位姿、夹爪状态和可选灵巧手关节。不存在的维度填 0，并用 binary mask 从 loss 中排除，因此单臂、双臂、灵巧手、移动机器人和类人机器人可以共享同一个模板。

动作对齐的关键是 camera-frame delta EEF。模型不直接预测某台机器人的关节动作，也不使用机器人 base frame 下的绝对位姿，而是把相对末端执行器运动表达在选定相机坐标系中。Camera positional encoding 把相机内外参注入 action expert。这样，视觉上相似的动作在数值动作空间里也更接近，有利于跨机器人迁移。

模型还使用结构化 embodiment prompt，包括机器人名称、任务指令、速度、FPS 和相机视角方向。Context 版本进一步输入同一 episode 中最近的 observation-state-action chunk，让策略从刚刚执行过的行为里推断机器人的运动学特征，无需参数更新。

数据层由机器人示教、第一视角人类操作视频、Human-to-Robot 合成轨迹和视觉语言数据组成。操作数据总量约 38,100 小时：单臂机器人 3,808 小时，双臂机器人 6,744 小时，移动/类人机器人 868 小时，人类第一视角视频 1,933 小时，Human-to-Robot 合成数据 24,808 小时。H2R pipeline 会把人手轨迹 retarget 成夹爪轨迹，移除视频中的人手，搜索可达机器人底座，使用 MuJoCo IK 求解，再把渲染出的机器人手臂按深度合成进第一视角场景，覆盖 15 种双臂平台。

## 关键创新

- 把跨机器人 alignment 作为规模化训练的前提，而不是后处理技巧。
- 用 80 维 canonical state-action vector 和 binary mask 统一异构本体。
- 用 camera-frame delta EEF 让动作空间贴近视觉观测空间，降低坐标系冲突。
- 将第一视角人类视频合成为 15 平台机器人轨迹，得到 24,808 小时合成机器人数据。
- 数据清洗覆盖状态/动作突变、时序错位、极值、FK 一致性、base frame 对齐、指令一致性、视频状态一致性和坏帧过滤。
- 通过约 28M 视觉语言样本做 dual-stream co-training，保留 VLM 的视觉、语言和空间推理能力。
- 提出或采用更强 OOD 评测，包括 RoboTwin-IF 指令跟随和 RoboTwin-XE 零样本跨本体迁移。

## 实际解决的问题

论文解决的核心问题是：多机器人数据不等于可规模化训练。相同物理动作如果在不同机器人和数据集中用不兼容坐标表达，模型会把容量浪费在调和冲突上。canonical vector 和 camera-frame EEF 让数据在结构和几何上更一致。

它还缓解了机器人数据稀缺。作者没有依赖私有大规模 teleoperation，而是把开源机器人数据和第一视角人类视频通过合成与清洗变成约 38,100 小时训练语料。

最后，论文指出常规 in-domain benchmark 不足以验证基础模型能力。真正有价值的指标是 OOD 场景、未见物体、语言指令变化、机器人初始状态扰动、跨本体迁移和真实机器人部署。

## 实验结果

在 in-distribution benchmark 上，Qwen-RobotManip 在 LIBERO 达到 99.1%，在 RoboTwin-Easy/Hard 达到 93.4%/92.5%。Context 版本达到 99.2%、93.7% 和 94.0%。论文认为这些结果只是基础验证，不足以说明泛化。

在 LIBERO-Plus 上，Qwen-RobotManip 总成功率为 89.0%，Context 版本为 91.4%，高于 pi0.5 的 84.4%。在 RoboTwin-Clean2Rand 上，Context 模型在 Hard joint-control 设置达到 69.4%，高于 pi0.5 的 47.9% 和 GR00T-N1.7 的 20.7%。

在 RoboCasa365 上，Qwen-RobotManip 总成功率 35.9%，高于 RLDX-1 的 33.2%、GR00T-N1.5 的 23.9% 和 pi0.5 的 16.9%。在最难的 Composite-Unseen 上，它达到 14.9%，而下一个最好结果是 5.4%。

在 EBench 上，Qwen-RobotManip 总成功率 45.6%，composite score 60；pi0.5 为 27.1% 和 41。dexterous tabletop split 上差距很大，Qwen-RobotManip 达到 50.0% 和 score 70，pi0.5 只有 12.9% 和 score 32。

在 RoboTwin-IF 指令跟随 benchmark 上，Qwen-RobotManip 平均成功率 72.2%，pi0.5 为 49.6%。这类任务同一场景中存在多个可行动作，必须真正理解语言指令，不能只靠视觉 shortcut。

在 RoboTwin-XE 零样本跨本体迁移上，EEF 版本在 ARX-X5、UR5-WSG 和 Franka 上平均 23.9%，高于 pi0.5 EEF 的 7.5% 和 Qwen-RobotManip joint-action 版本的 14.5%。这验证了 camera-frame EEF 的价值，但绝对成功率仍说明跨本体迁移远未解决。

真实 CobotMagic ALOHA 上，7 个 in-domain 任务平均成功率 88.6%，pi0.5 为 42.9%，StarVLA 为 20.0%。4 个 OOD 任务包含杂乱背景、未见物体、空间关系和动态光照，Qwen-RobotManip 平均 87.5%，pi0.5 为 37.5%，StarVLA 为 0.0%。

在 ARX ALOHA few-shot adaptation 中，所有方法只用 130 条示教。Qwen-RobotManip 在 Put Blocks、Fold Towel 和 Unscrew Cap 上优于 pi0.5，但 Insert Screw 的完整插入仍无人成功。跨本体 skill transfer 中，ARX 目标任务没有示教，完整模型平均 55.0%，去掉 UnifiedEEF 为 12.5%，去掉 UnifiedSpace 为 7.5%。

在 RoboChallenge Table30-v1 generalist track 上，Qwen-RobotManip 平均成功率 40%，高于 pi0.5 的 21.2%、DM0 的 16.2%、GR00T-MULTI 的 7.5% 和 pi0 的 7.5%。

## 消融实验

动作空间 scaling 消融是论文最关键证据。使用对齐表示时，随着跨本体预训练数据从 1% 增加到 100%，validation MSE 基本呈 log-linear 下降。没有 UnifiedSpace 时，尤其是末端执行器预测，曲线不稳定。下游 RoboTwin-C2R Hard 也显示完整 camera-frame 表示规模化最好，满量预训练时 joint 为 50.2%，EEF 为 56.6%。

In-context adaptation 消融显示，结构化 prompt 有小幅收益，但历史执行上下文在 denoising steps 足够时收益更大。10 步 denoising 时，context 版本在该 RoboTwin-Clean2Rand 设置平均达到 70.9，比结构化 prompt baseline 高约 5 点。

Human-to-Robot 数据比原始 ego 数据更有效。在 RoboTwin-Clean2Rand Hard 上，robot-only 为 54.7%，+ego 为 55.0%，+H2R 为 58.7%。在 LIBERO-Plus 上，总分从 87.1% 到 88.4% 再到 89.0%。

VL co-training 对难 OOD 很重要。预训练阶段去掉 VL 数据后，RoboTwin-Clean2Rand Hard 从 62.6% 降到 54.4%，RoboTwin-IF 从 71.6% 降到 64.6%。在 post-training 阶段加入 VL 数据还能继续提升 LIBERO-Plus 和 RoboTwin-IF。

## 局限性

论文明确指出，Human-to-Robot 合成虽然可扩展，但会引入 retargeting 近似误差和 inpainting artifact，合成数据质量受这些环节限制。主要 OOD 评测仍以仿真为主，尽管论文包含了真实机器人验证。

跨本体迁移仍未解决。RoboTwin-XE 的 EEF 平均只有 23.9%，Franka 只有 5.9%。这说明 camera-frame EEF 明显有帮助，但不能消除机器人形态、可达空间、控制器和校准误差带来的差距。

Context 版本在 episode 开头可能犹豫，因为历史输入是 zero-padded，占位历史会让模型倾向于等待。因此作者同时发布 context 和 non-context 版本。固定 action chunk 长度和当前推理延迟也限制了需要亚秒级反应的任务。

工程依赖也很重：camera-frame EEF 需要可靠相机标定，部署需要稳定 IK/controller，训练前必须做严格数据清洗。即使数据源是开源的，完整复现仍需要大量工程投入。

## 应用到我的机器人

对我的机器人，最值得迁移的是动作接口和数据对齐流程。不要先追求 38,100 小时数据规模，而是先定义固定 state/action schema，并尽量把末端执行器 delta 表达在相机坐标系或任务坐标系中，让不同机械臂、夹爪和相机配置的数据可以复用。

可落地路线：

- 定义固定状态/动作向量，用 mask 标记不存在的维度；
- 把 joint、EEF、gripper、可选 hand/base 字段放到稳定语义槽位；
- 对希望跨机器人迁移的操作技能，优先使用 camera-frame 或 task-frame relative EEF action；
- 严格记录相机标定、proprioception、动作和时间戳；
- 增加数据清洗：动作突变、state-action 延迟、FK 不一致、指令视频不一致和坏帧过滤；
- 第一视角人类视频只能作为 retarget 和视觉合成后的辅助数据，不应直接当机器人动作监督；
- 评测要覆盖 OOD 场景、未见物体、初始位姿扰动和指令跟随，而不只看 in-domain success。

预期收益是更好地利用小规模异构数据、更强语言条件控制，以及从一台机器人迁移到另一台机器人的可能性。主要风险是相机标定误差、IK 不可达、合成数据 artifact、推理速度和过拟合仿真 benchmark。

## 实施建议

先做小规模验证。选择两个机器人本体或两个相机配置，比较三种动作表示：原始关节动作、base-frame EEF delta、camera-frame EEF delta。在未见初始位姿和未见物体布局上评测。如果 camera-frame 表示显著提升 OOD 成功率，再扩大混合数据规模。

对真实机器人项目来说，最高杠杆不是模型参数量，而是数据 alignment 工程。应优先做标定检查、FK 一致性检查、state-action latency 检查和指令/视频一致性检查，然后再投入更多数据采集。
