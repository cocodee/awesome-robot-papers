# HumanEgo：从数分钟人类第一视角视频中零样本学习机器人策略

## 元数据

- 作者：Zhi Wang, Botao He, Kelin Yu, Seungjae Lee, Ruohan Gao, Furong Huang, Yiannis Aloimonos
- 会议/年份：arXiv，2026
- 来源：[arXiv PDF](https://arxiv.org/pdf/2605.24934)
- arXiv：2605.24934v2，2026-05-28
- 本地 PDF：[../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.pdf](../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.pdf)
- 转换 Markdown：[../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.md](../papers/HumanEgo-Zero-Shot-Robot-Learning-from-Minutes-of-Human-Egocentric-Videos.md)
- 项目页：[HumanEgo](https://humanego-ai.github.io/)
- 代码：[TX-Leo/HumanEgo](https://github.com/TX-Leo/HumanEgo)

## 研究问题

HumanEgo 研究的是：机器人能否只用几分钟人类第一视角操作视频，直接学到可部署的真实机器人操作策略，而不需要机器人示教、不需要互联网规模预训练，也不需要在目标机器人上后训练。

核心难点是 embodiment gap。人手和机器人夹爪在外观、运动学和控制方式上都不同，但真正可迁移的是手与物体之间的任务相关交互几何。

## 核心方法

HumanEgo 把人类第一视角视频转成双臂机器人策略，流程分四步。

第一步，人类佩戴 Aria Gen1 眼镜采集任务示教。Aria 管线提供同步第一视角 RGB、SLAM 位姿和带真实尺度的 3D 手部跟踪。

第二步，做视觉观测预处理，降低视觉 embodiment gap。系统用 SAM2 分割人手和手臂，用 LaMa inpainting 去除它们，再把虚拟夹爪和物体关键点渲染回图像。

第三步，构建 Interaction-Centric Tokens（ICT）。系统把左右手和每个物体都当作 entity。每个 entity 的 token 包含 entity 类型、参考坐标系下的位姿、左手相对该 entity 的位姿、右手相对该 entity 的位姿，以及抓取状态。这样模型学习的是接近、抓取、搬运、释放这些手-物关系，而不是模仿人手本身。

第四步，训练 flow matching policy 来预测双臂动作 chunk。策略网络使用共享 context encoder 和动作 decoder，并加入三个 dense auxiliary objectives：未来物体 6D 运动、未来 2D entity 轨迹、未来 ICT latent state。这些辅助目标让 encoder 在 3D 物理空间、2D 视觉空间和 latent 空间中学习前向动力学。

## 关键创新

- 从人类第一视角视频中学习真实机器人操作策略，不需要机器人数据。
- 用 ICT 显式编码可迁移的手-物关系，而不是模仿人手几何。
- 用视觉预处理去掉人类外观，同时保留任务相关视觉提示。
- 用 flow matching 生成多模态动作，比多步 diffusion sampling 更适合快速推理。
- 用 dense auxiliary supervision 从短示教中压榨更多训练信号。
- 在不同相机、机器人手臂、环境、物体位置和视觉条件下零样本迁移。

## 实际解决的问题

这篇论文解决的是机器人任务示教数据昂贵、采集麻烦的问题。传统做法需要用户在同一台机器人、同一套环境里 teleop；HumanEgo 则让人自然完成任务，用可穿戴相机记录即可。

它也解决了很多人类视频方法的表示不足问题。只表示点、只表示物体运动、或者只预测 goal-conditioned tracks，都会丢失操作真正依赖的手-物交互结构。HumanEgo 把手和物体的相对关系作为主状态。

## 实验结果

主实验包含四个真实机器人任务：Serve Bread、Downstack Cups、Water Flowers 和 Adjust Table，覆盖 pick-and-place、长时序堆叠、接触丰富的双臂协作，以及持续旋转控制。

每个任务使用 30 分钟人类视频时，HumanEgo 在四个任务上的平均成功率为 92.5%。只用 15 分钟时，平均成功率为 75.0%。同等时间机器人 teleoperation 训练的 ACT 为 51.2%，所以主文报告 HumanEgo 相比机器人示教高 41 个百分点。

与五个从人类第一视角视频学习的零样本 baseline 相比，HumanEgo 在每个任务上都是最好。这些 baseline 包括 point-based、goal-conditioned 和 object-centric 方法，但在需要精确手-物几何和双臂时序协调的任务上明显掉队。

Serve Bread 的数据效率实验显示，HumanEgo 大约用 7 分钟人类示教就达到 50% 成功率，30 分钟达到 95%。在 8 分钟时，用人类数据训练的 HumanEgo 已经超过用 30 分钟机器人数据训练的 ACT。

鲁棒性实验显示，HumanEgo 可以在新背景、新光照、新视角、干扰物、新物体实例、新相机、不同桌面高度和不同机器人本体上零样本迁移，包括 Trossen、Franka 和 UR10。

## 消融实验

表示消融是最关键证据。raw human RGB 只有 7.5%，加关键点渲染和手臂 inpainting 为 20%，直接用 robot RGB 为 32.5%，raw human RGB 加 ICT 达到 85%，完整系统达到 95%。这说明真正打通迁移的不是视觉逼真度，而是显式空间交互 token。

辅助损失消融在 15 分钟数据下进行。object motion 单独贡献最大，其次是 latent consistency 和 2D trace；三者一起比无辅助损失 baseline 高 25 个百分点。

附录里的手部跟踪实验很有实操价值。在 Serve Bread 上，Aria-MPS 达到 95%，WiLoR 降到 45%，HaMeR 降到 32.5%，MediaPipe 为 0%。这说明方法强依赖平滑、稳定、有真实尺度的 3D 手部轨迹。

## 局限性

HumanEgo 依赖 Aria 的 stereo hand tracking。单目替代方案会引入深度歧义、抖动、漏检和明显的下游成功率下降。

整个感知链路由多个现成模块串起来，包括 SAM2、LaMa、Grounding DINO、CoTracker3、Orient-Anything、SLAM 和手部跟踪。检测、分割、姿态估计或跟踪的错误都会传递到策略。

物体处理还不是完整的在线鲁棒跟踪。手中操作、严重遮挡、快速运动和动态场景可能需要更强的实时 occlusion-robust tracker。

论文展示了很强的零样本效果，但任务仍主要是桌面操作。亚厘米级接触控制很可能仍需要 RL refinement、仿真微调或真实机器人反馈。

复现时还要注意一个数据口径细节：主文反复强调每任务 30 分钟人类视频，而附录超参数表写的是每任务 60 条示教、总人类视频 40 分钟。实际复现应明确使用哪些片段、如何裁剪、训练和测试如何划分。

## 应用到我的机器人

如果我的机器人项目希望快速学习新操作任务，又不想先搭建 teleoperation 数据集，HumanEgo 很值得参考。可落地路线是：

- 用能提供真实尺度手部位姿的设备采集第一视角任务视频；
- 把人手轨迹转换为虚拟夹爪动作标签；
- 跟踪被操作物体和关键点；
- 为每只手和每个物体构建 ICT-style token；
- 训练带未来预测辅助损失的 flow matching 动作策略；
- 部署时通过我的机器人 IK 和夹爪控制器执行动作。

对我的机器人来说，最可复用的不是完整大模型结构，而是数据接口：把操作表示成相对手-物变换。这个设计可以先在小模型和单任务上验证。

## 实施建议

第一优先级是感知前端。如果没有 Aria 这类 stereo hand tracking，应考虑使用标定多相机、深度相机或其他能输出稳定真实尺度手部轨迹的方案，否则性能可能大幅下降。

建议先从一个简单 pick-and-place 任务开始。记录 RGB、相机位姿、物体 mask、物体关键点、手部位姿和推导出的夹爪位姿。训练前先把 ICT 轨迹可视化检查一遍；坏的 tracker 最后会表现成坏的 policy。

部署时要保留每周期位置和旋转变化限幅、动作 chunk 平滑和夹爪 latch 逻辑，并单独测试安全边界。HumanEgo 的动作流仍然需要正常的机器人安全工程。
