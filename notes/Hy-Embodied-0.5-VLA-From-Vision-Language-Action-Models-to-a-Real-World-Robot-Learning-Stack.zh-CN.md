# Hy-Embodied-0.5-VLA：从视觉-语言-动作模型到真实机器人学习栈

## 元数据

- 作者：He Zhang, Lingzhu Xiang, Haitao Lin, Zeyu Huang, Minghui Wang, Dingyan Zhong, Yubo Dong, Yihao Wu, Yongming Rao, Dongsheng Zhang, Wanjia He, Ling Chen, Kai Huang, Jiahao Chen, Sichang Su, Xumin Yu, Ziyi Wang, Chengwei Zhu, Xiao Teng, Yuchun Guo, Yufeng Zhang, Yuandong Liu, Rui Wang, Zisheng Lu, Han Hu, Zhengyou Zhang
- 会议/年份：arXiv，2026
- 来源：[arXiv PDF](https://arxiv.org/pdf/2606.14409)
- arXiv：2606.14409v1，2026-06-12
- 本地 PDF：[../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.pdf](../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.pdf)
- 转换 Markdown：[../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.md](../papers/Hy-Embodied-0.5-VLA-From-Vision-Language-Action-Models-to-a-Real-World-Robot-Learning-Stack.md)
- 项目页：[Hy-Embodied-0.5-VLA](https://tairos.tencent.com/openSourceModels/hy-embodied-0.5-vla)
- 代码：[Tencent-Hunyuan/Hy-Embodied-0.5-VLA](https://github.com/Tencent-Hunyuan/Hy-Embodied-0.5-VLA)
- 模型：[tencent/Hy-Embodied-0.5-VLA-UMI](https://huggingface.co/tencent/Hy-Embodied-0.5-VLA-UMI)
- 数据集：[tencent/Hy-Embodied-0.5-VLA-Data](https://huggingface.co/datasets/tencent/Hy-Embodied-0.5-VLA-Data)

## 研究问题

这篇报告研究的是：怎样把 VLA 策略从一个模型，变成可以真实部署的机器人学习栈。目标场景是真实双臂操作和跨本体迁移，难点不只在模型能力，还在高质量数据、连续控制、任务适配、失败修正和低延迟执行。

论文的核心判断是：通用机器人不能只靠一个更大的 VLA。数据采集、模型结构、动作表示、监督微调、偏好式后训练和部署运行时必须一起设计。

## 核心方法

HyVLA-0.5 基于 Hy-Embodied-0.5-MoT，一个 4B 参数的 Mixture-of-Transformers 具身 VLM。论文在其上加入约 370M 参数的 flow-matching action expert，用连续动作块替代离散动作 token。视觉、语言、机器人状态和 noisy action 使用不同的模态计算路径，同时通过共享 attention 做跨模态 grounding。

动作接口采用相对末端执行器 delta chunk。每个手臂预测 3D 平移、6D 旋转和夹爪命令，坐标系是末端执行器坐标系。这让策略尽量不绑定某台机器人的关节空间；部署时再通过平台映射、正运动学和 IK 转成目标机器人的控制命令。

数据层是 Hy-UMI-10K：超过 1 万小时、100 多万 episode、70 个任务的 fingertip UMI 示教。自研手持夹爪使用光学动捕提供亚毫米级 6-DoF 标签，用手指绑定式结构保留人的触觉反馈，同时记录 RGB-D、夹爪编码器和可选力/力矩信号。当前 HyVLA-0.5 只使用 RGB 训练，深度数据留作未来扩展。

训练分三步。第一步，用完整 10K 小时 UMI 数据做预训练，训练 200K steps，输入 3 路 224x320 相机，预测 10 Hz、长度 50 的未来动作块。第二步，做监督微调，并启用 compact memory encoder，使用当前帧加 5 帧历史。Track A 在同一真实机器人上采集、微调和评测；Track B 只用任务相关 UMI 数据微调，然后部署到形态不同的 JAKA K1 和 Astribot S1，不使用目标机器人 teleoperation。第三步，用 FlowPRO 做后训练：通过 intervention-and-rollback 收集失败轨迹和修正轨迹，再用适配 flow-matching 的 RPRO 目标做无 reward、无 critic 的偏好优化。

部署层使用异步 producer-consumer 运行时：推理线程持续产出动作块，执行线程按控制频率消费 buffer 中的命令。新的动作块到来后，系统丢弃过期前缀，并用 latency-aware cubic Bezier stitcher 平滑拼接位置、姿态和夹爪命令。

## 关键创新

- 把 VLA 做成完整机器人学习栈，而不是只提出一个策略网络。
- 用 fingertip gripper、光学动捕和可选力传感扩展高精度 UMI 数据采集。
- 用相对末端执行器 delta chunk 降低跨机器人本体迁移难度。
- compact memory encoder 引入短时视觉历史，同时不增加传给 VLM 的视觉 token 数。
- FlowPRO/RPRO 把真实失败案例变成离线偏好训练信号，不需要 reward model 或 value model。
- 用异步执行和 Bezier 动作块拼接解决大 VLA 在真实硬件上的延迟问题。

## 实际解决的问题

第一个问题是数据。传统 teleoperation 成本高且绑定机器人本体；普通人类视频又缺少精确动作标签。Hy-UMI-10K 试图保留人类操作的多样性，同时记录可训练机器人的 6-DoF 轨迹。

第二个问题是动作精度。离散动作 token VLA 在精细操作上容易受限。HyVLA-0.5 用连续 flow matching 和动作块预测支持高频控制。

第三个问题是最后一段灵巧性。纯 SFT 常在接触、插入、拉链、折叠等关键局部步骤失败。FlowPRO 直接利用失败轨迹作为 negative，修正轨迹作为 positive，把策略从常见失败模式推开。

第四个问题是部署延迟。异步 buffer 和 chunk stitching 让机器人在等待下一次 VLA 推理时仍能连续运动，减少同步推理造成的停顿。

## 实验结果

在 RoboTwin 2.0 上，HyVLA-0.5 在 50 个任务上评测，每个任务 100 次随机 rollout。Clean 成功率为 90.9%，Randomized 成功率为 90.1%。它略高于 JoyAI-RA 的 90.5% / 89.3%，也高于 Qwen-VLA、starVLA、Motus、LingBot-VLA、pi0 和 pi0.5 等对比方法。

消融结果显示，去掉 compact memory encoder 后成功率降到 88.8% / 88.6%；同时去掉 compact memory 和 UMI pre-training 后降到 88.1% / 87.9%。UMI 预训练在仿真里的增益不大，作者认为原因是 egocentric 真实 UMI 数据与 RoboTwin 合成渲染之间存在明显 domain gap。

真实机器人 SFT 包含两条线。Track A 在 Dobot X-Trainer 上做 Insert Bottles、Fold and Store Glasses、Set the Table 和 Zip Up the Pen Case。Track B 只用 UMI 数据微调，然后迁移到 JAKA K1 的 Put Away the Accessory 和 Astribot S1 的 Clean Up the Table。论文报告 Hy-UMI-10K 预训练对高精度瓶颈步骤特别有帮助，例如折眼镜、防滑、捏住拉链头、放置小发圈和类人机器人清桌面。

力觉验证在 Unitree G1 上进行。作者给 action expert 增加轻量 TCN 编码器，输入每只手 50 步 force/torque 窗口。机器人连续抓取两个盒子并把更轻的盒子放入篮子，说明 fingertip force 信号可以成为可用的非视觉策略输入。

FlowPRO 后训练在 Dobot X-Trainer 上评测四个双臂任务，所有方法使用相同数据预算并迭代 3 轮。RPRO 在 Bottle 上达到 99+/-0.6% 和 16 秒，在 Cap 上达到 99+/-0.7% 和 21 秒，在 USB 上达到 98+/-0.9% 和 22 秒，在 Zip 上达到 94+/-1.1% 和 37 秒。相比 DAgger 和 pi0.6\* advantage-conditioned regression，RPRO 同时提升成功率并缩短完成时间。

## 局限性

HyVLA-0.5 是一个很重的系统。它依赖 4B VLM backbone、大 action expert、1 万小时私有数据采集、光学动捕设备，以及细致的真实机器人部署工程。小团队更现实的路线是复用发布的模型或数据，而不是完整复刻。

论文最强的真实机器人证据是任务后训练和 UMI 微调后的跨本体迁移，不是广义 zero-shot 泛化。作者也明确把涌现式 zero-shot 具身智能留作未来问题。

UMI 采集设置偏向标签精度，不偏向野外便利性。光学动捕提升动作标签质量，但限制采集环境。论文还指出 UMI 的第一视角相机和机器人部署相机存在差异，需要系统化视觉增强研究。

虽然采集了 RGB-D，但当前模型只用 RGB。力觉只在一个定性任务上通过额外模块验证，距离通用 force-aware manipulation 还有距离。

## 应用到我的机器人

对我的机器人来说，最值得先借鉴的不是完整 4B 模型，而是统一动作接口和闭环迭代流程：用机器人无关的末端执行器相对动作表示，把数据、策略、修正和部署都围绕这个接口组织起来。

可落地的改造路线：

- 示教数据记录相对末端执行器 delta 和夹爪状态，而不只记录关节目标；
- 保证相机、proprioception、动作和语言指令严格同步；
- 对接触丰富任务加入短时视觉历史；
- 训练连续动作块策略，可以先用回归，再尝试 flow matching；
- 部署时使用异步动作 buffer 和平滑 chunk stitching；
- 在真实 rollout 中收集失败/修正配对数据，用作偏好或对比式后训练。

硬件需求取决于目标规模。最小版本需要同步 RGB 相机、末端位姿估计、夹爪状态和能运行 chunk policy 的计算资源。更强版本可以加入腕部相机、头部相机、力/力矩传感器和稳定 IK/controller。

预期收益是提高精细操作关键步骤的成功率，并让真实失败快速转化成下一轮训练数据。主要风险是数据规模不足、相机 domain gap、相对末端命令导致 IK 不可达、动作延迟，以及采集修正数据时的安全问题。

## 实施建议

先选一个失败模式清楚的任务，例如插入、拉拉链、折叠或小物体精确放置。第一步先实现 delta end-effector 表示和异步 chunk 执行，因为这些部署组件即使不训练基础大模型，也可能改善机器人运行稳定性。

小团队的第一组实验应该比较两个策略：普通 action chunk policy，以及加入短时视觉历史和 UMI 风格相对末端目标的策略。如果后者能改善关键精度步骤，再引入失败/修正偏好数据。完整 FlowPRO 更适合在基础 SFT 策略已经有一定成功率、能产生有意义 near-miss failure 之后再做。
