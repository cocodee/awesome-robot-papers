# Psi-0: 面向通用类人机器人移动操作的开放基础模型

## 元数据

- 作者：Songlin Wei, Hongyi Jing, Boqian Li, Zhenyu Zhao, Jiageng Mao, Zhenhao Ni, Sicheng He, Jie Liu, Xiawei Liu, Kaidi Kang, Sheng Zang, Weiduo Yuan, Marco Pavone, Di Huang, Yue Wang
- 来源：https://arxiv.org/pdf/2603.12263
- arXiv：2603.12263v1，2026-03-12
- 本地 PDF：[../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.pdf](../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.pdf)
- 转换 Markdown：[../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.md](../papers/Psi-0-An-Open-Foundation-Model-Towards-Universal-Humanoid-Loco-Manipulation.md)
- 项目页：https://psi-lab.ai/Psi0

## 研究问题

这篇论文研究如何训练一个能做长时序类人移动操作的基础模型，同时不依赖海量类人机器人遥操作数据。作者的核心观点是：直接把人类视频动作和类人机器人动作混在一起 co-training 并不理想，因为两者在运动学、动力学、动作频率和自由度上都有明显差异。

## 核心方法

Psi-0 使用分阶段训练。第一阶段，在 EgoDex 第一视角人类视频上预训练 Qwen3-VL-2B，让 VLM 预测下一步 task-space action token，从而学习任务语义、视觉表征和人类-物体交互先验。第二阶段，冻结 VLM，用真实类人机器人数据训练一个约 500M 参数的 flow-based MM-DiT action expert，让它直接预测 joint-space whole-body action chunk。第三阶段，对每个下游真实任务，只微调 action expert。

部署时系统分成三层：VLM backbone、action expert、RL lower-body controller。动作空间包含灵巧手关节、手臂关节、躯干姿态、底盘高度、平面速度、yaw 速度和目标 yaw。下半身控制器负责把高层 lower-body command 转成稳定的腿部和腰部关节动作。

## 关键创新

- 不做单一大模型的混合 human-robot co-training，而是分阶段学习。
- 人类视频用于学习视觉和任务级先验，真实类人机器人数据用于学习精确 joint control。
- MM-DiT action expert 比 naive DiT head 更好地融合视觉语言特征和动作 token。
- training-time real-time chunking 缓解大模型推理延迟导致的动作抖动。
- 构建了面向类人移动操作的单人遥操作系统：VR 头显、腕部 tracker、MANUS 手套、腰部 tracker 和脚部 tracker。

## 实际解决的问题

Psi-0 解决的是类人机器人 loco-manipulation 问题：机器人既要走动和转身，又要控制躯干、双臂和灵巧手完成长时序任务。论文主要针对三个瓶颈：类人遥操作数据昂贵、人类视频直接迁移到机器人控制不稳定、大模型推理延迟会造成 action chunk 之间的停顿和抖动。

## 实验证据

论文在 Unitree G1 + Dex3-1 灵巧手上评估了 8 个真实长时序任务，涉及抓取、放置、推动、擦拭、倒入、旋转、下蹲、行走和双臂搬运。作者报告平均整体成功率比第二名 GR00T N1.6 至少高 40%，同时只使用约 800 小时第一视角人类视频和 30 小时真实机器人数据。

消融实验显示分阶段训练很关键。在一个三阶段双臂任务上，不做预训练和 post-training 的 naive DiT action head 整体成功率为 0/10；换成 MM-DiT 为 2/10；加入 EgoDex 预训练为 6/10；再加入 Humanoid Everyday post-training 为 8/10；加入 real-time chunking 后为 9/10。

## 局限性

实验虽然是真实机器人，但主要集中在 Unitree G1 和 Dex3-1 手这一平台。作者也指出，由于算力和时间限制，没有进一步扩大人类视频和机器人数据规模。硬件载荷能力也限制了更复杂操作行为。工程上，该方法仍需要较重基础设施：64 张 A100 做 VLM 预训练，32 张 A100 做 action expert post-training，并依赖定制遥操作系统。

## 应用到我的机器人

如果我的机器人是类人机器人，或者是移动操作平台，需要同时处理移动、躯干姿态、手臂和末端执行器控制，这篇论文很有价值。最重要的启发是：不要太早把人类视频动作和机器人 joint control 强行塞进同一个策略分布。

实际适配路线：

- 用第一视角人类视频或遥操作视频学习任务级视觉先验；
- 保持高层 VLM 和低层 robot action expert 分离；
- action expert 直接在我的机器人 joint space 或控制器 command space 中训练；
- 对底盘或下半身使用稳定控制器，不要求 VLA 完全输出所有低层关节；
- 实现 real-time chunking 或异步 action buffer，避免推理时停顿导致机器人抖动。

对我的机器人来说，最强的工程经验是分阶段解耦：从可扩展视频中学习感知和任务意图，再用少量高质量机器人数据学习精确执行。

## 实施建议

先定义清楚机器人动作接口，再训练模型。对于轮式或腿式移动操作机器人，建议把动作拆成手/臂命令和底盘/下半身命令。先采集一个小但稳定的遥操作数据集，测试 frozen VLM + flow/diffusion action head 是否能模仿 joint-space action chunks。真实部署时必须把推理延迟计入测试，因为动作平滑性问题通常只会在硬件上暴露。
