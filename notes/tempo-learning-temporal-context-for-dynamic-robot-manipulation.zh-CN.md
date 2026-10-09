# TEMPO：为动态机器人操作学习时间上下文

- 作者：Zhenyang Feng、Jimin Heo、Erik B. Sudderth、Unnat Jain；University of California, Irvine。
- 会议/年份：CoRL 2026；arXiv:2609.16864v1。
- 来源：https://arxiv.org/abs/2609.16864
- 项目页：https://tempo-robot.github.io/
- 代码：https://github.com/tempo-robot/TEMPO
- **公开基准：** [TEMPO-Bench](https://github.com/tempo-robot/TempoBench)。
- **本地材料：** [PDF](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/paper.pdf) · [转换 Markdown](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/paper.md) · [逐站精读](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/精读笔记.md)。

## 研究问题与实际问题

单帧 VLA 做动态操作时有两种不同的信息缺口：同一位置的物体可能朝不同方向移动（运动歧义）；相似画面可能分别处于伸手抓取、释放撤回等阶段（状态别名）。接住路过的人递来的瓶子必须估计未来截取位置，倒珠子后撤回则必须记得机器人已经倒完。仅缩短推理延迟仍不能从单张图中恢复运动与阶段（论文 §1–3）。

## 方法与关键创新

TEMPO 在预训练 π0.5 / VLASH 策略上提供两类历史。**TEMPO-MOT** 使用冻结的 SAM 2.1 Tiny 和短时视觉记忆提取场景运动；**TEMPO-ACT** 将过去 10 秒、30 Hz 的 300 条原始控制聚成 10 桶，每桶均值作为动作历史。两者进入 VLM 前缀，动作历史还通过 AdaRMS 残差影响 action expert。论文称新增约 2M 参数（0.08%），原有动作 flow-matching 损失不变（§4）。[图 3](../assets/tempo/figure-3.png)展示连接。

官方配置更具体：每路相机取含当前帧的 3 帧、间隔约 0.333 秒；head 相机的 SAM2 特征为 `64×256`，融合进当前视觉 token，而不是代码里另加独立 motion token。双臂动作与状态各 14 维（每臂 6 关节+夹爪），输出 16 步动作块；模型内部 pad 到 32 维并采样 10 步后切回本体维度。默认动作目标把关节目标转成相对当前状态的增量、夹爪保持绝对；动作历史保留原始值（官方 `training/config.py`、`policies/yam_dual_policy.py`、`models_pytorch/pi0_pytorch.py`）。

## 训练、数据与可复核样本

训练仍预测从带噪动作到真实动作的 flow 速度。官方代码写作 `xₛ=sε+(1−s)a*`、目标 `ε−a*`、逐元素 MSE。底座参考配置 10,000 步，TEMPO 增量参考配置 5,000 步；batch 128、AdamW 峰值学习率 `5e−5`。论文附录报告每策略约 2 小时、8 张 RTX PRO 6000 Blackwell。

[公开基准 TEMPO-Bench](https://github.com/tempo-robot/TempoBench)含 257 段、97,265 帧，其中 55,482 帧有可见物体定位。其双臂接瓶第 0 段第 60 帧的**真实标注**为：时间 2.000 秒，瓶中心 `(237.095,200.553)` 像素，速度 `(487.380,−56.580)` 像素/秒；`observation.state` 与原始 `action` 均为 14 维。此前 60 条真实控制在 10 桶历史窗口中只填满最后两桶，前 8 桶为 pad。基准规模不能代替论文未明确给出的策略训练演示规模；策略权重与训练数据在[官方仓库](https://github.com/tempo-robot/TEMPO)仍标为待发布。

## 实验与证据

| 设置                             | 结果                                            | 解读                                   |
| -------------------------------- | ----------------------------------------------- | -------------------------------------- |
| 真机 Bottle Handover             | VLASH 38%、RTC 44%、TEMPO 74%，各 50 次         | 加历史显著改善截取移动瓶子（表 4）。   |
| 真机 Drop Catch                  | RTC 80%、TEMPO 66%                              | 反应时序主导时，TEMPO 未领先（表 4）。 |
| 原始完整 Flick Catch / Wine Pour | 异步基线均 0%，TEMPO 68% / 97.6%                | 动作历史帮助区分抓取与撤回（表 1）。   |
| Bottle Handover 消融             | 仅 ACT 52%、仅 MOT 56%、两者 74%                | 两种历史互补（表 6）。                 |
| 运动 probe                       | Flick Catch 的速度 `R²`：VLASH 0.03、TEMPO 0.57 | 时间信息进入可读出的表示（表 7）。     |

表 4 的 Flick Catch 和 Wine Pour 使用**裁剪掉释放撤回阶段**的任务；完整任务另见表 1。Wine Pour 的百分数是容器保留的珠子质量比例，不是二值成功率。TEMPO+UVT 的平均 87.2% 还包含更换输出目标，不能归为 TEMPO 输入独自造成的提升。

## 局限与代码核对

- 论文用四项真实双臂任务验证，尚不足以说明跨机器人本体或开放环境的稳定泛化。
- SAM2 虽冻结，部署仍需要实时编码及缓存；35.3 ms 中位策略前向时间略高于 30 Hz 帧间隔 33.3 ms，实际控制依赖异步流水线。
- 论文图示把运动编码当作额外 token，代码则在 SigLIP 内加入时间注意力、再将 SAM2 特征融入现有视觉 token；“不改 backbone”需要按实现限定理解。
- 代码的 SAM2 融合与 AdaRMS 残差可零初始化，但 10 个动作历史前缀 token 会改变注意力序列；官方配置注释明确说明初始化不完全等于原策略。
- 公开 TEMPO-Bench 可复核运动标注，但训练好的策略权重、训练演示仍待发布，暂不能独立重现真机成功率。

## 问题分析

本次按 kelip-paper-reading 依次核对动机、架构、训练、真实样本、信息流、两次接瓶观测与实验口径。逐步计算、图像和代码路径见[精读笔记](../papers/tempo-learning-temporal-context-for-dynamic-robot-manipulation/精读笔记.md)。后续关于本文的具体问题追加在此。

## 应用到我的机器人

- **集成思路：** 先记录相机时间戳、当前状态、发出的控制和动作完成时刻。保留现有 VLA，先加 10 桶历史动作条件，再加流式视觉运动编码；分别做单信号消融，并按“物体运动方向错”和“任务阶段错”标注失败。
- **传感器与算力：** 至少一台同步 RGB 相机、关节与夹爪状态、30 Hz 左右的控制日志；多视角和双臂可参照论文设置。需要运行冻结视频编码器和原 VLA 的 GPU；论文完整训练使用 8 张 RTX PRO 6000 Blackwell。
- **预期收益：** 改善对移动目标的预判，并减少抓取、释放、撤回阶段的犹豫和反向动作。
- **风险：** 运动特征可能受遮挡、跟踪错误和相机延迟影响；粗时间桶会抹掉快速动作细节；换本体后动作历史维度与单位必须重新定义。先用公开基准验证运动特征，再在自有安全任务中做闭环消融。
