# Video Prediction Policy 2：先预测对，再动得对

## 元数据

- 标题：Video Prediction Policy 2: Predict Better, Act Better
- 作者：Yanjiang Guo、Haodong Yan、Zhide Zhong、Zhongru Zhang、Qingyuan Yang 等 18 人
- 机构：Robotera、清华大学、香港科技大学（广州）、UC Berkeley、上海交通大学
- 发表：arXiv:2610.10270v2，2026-10-08 修订；预印本
- 来源：[arXiv](https://arxiv.org/abs/2610.10270) · [项目页](https://robert-gyj.github.io/video-prediction-policy-2) · [官方代码](https://github.com/roboterax/video-prediction-policy-2)
- 本地：[PDF](../papers/video-prediction-policy-2/paper.pdf) · [转换 Markdown](../papers/video-prediction-policy-2/paper.md) · [精读笔记](../papers/video-prediction-policy-2/精读笔记.md) · [详解教程](video-prediction-policy-2-tutorial.md)

## 研究问题

世界动作模型将视频预测先验用于机器人策略，但通用视频模型可能生成视觉合理、运动目标错误的未来；直接用动作损失改造视频主干又可能损伤泛化。本文研究如何同时提高开放任务的视频指令遵循和动作成功率。[论文 §1](../papers/video-prediction-policy-2/paper.tex)

## 方法与关键创新

VPP2 从 Wan2.1-I2V-14B 出发，先在跨机器人、人手、通用操作视频上进行**事件级视频续训**：把示教剪成 1–12 秒的完整子任务，并以明确末端、目标物和视角的 caption 监督。随后改为固定时域视频块预测，并用 consistency distillation 得到单步视频表示。最后通过 MoT 加入动作 DiT，利用视频侧缓存条件化动作去噪；动作训练早期冻结视频主干，仅 LoRA 适配。[图 2](../papers/video-prediction-policy-2/figures/fig-02.png)、[图 4](../papers/video-prediction-policy-2/figures/fig-04.png)、[§3](../papers/video-prediction-policy-2/paper.tex)

核心创新在于把**完整事件语义对齐**放在动作学习之前，并以固定时域及蒸馏弥合“完整事件视频”与“短动作块”的时间尺度差异。跨数据集还用 `T̃_d=A_d T_d B_d` 对齐世界坐标和末端坐标，避免同一视觉运动对应相反动作方向。[论文 §2、附录 A.2](../papers/video-prediction-policy-2/paper.tex)

## 训练与数据

阶段 1 的视频目标是 flow matching：`xₛ=(1−s)ε+sx₁`，预测速度 `x₁−ε`；论文给出 49 帧、416×240、30,000 步、batch 1,024。阶段 2 预测固定窗：人手 2 秒、机器人 8 秒；蒸馏后 17 帧视频一次前向。阶段 3 训练约 0.9B 的通用动作专家；论文描述动作 5 次去噪。[论文 §3](../papers/video-prediction-policy-2/paper.tex)

数据覆盖 20 余种机器人 embodiment；双臂/第一视角类数据占 80% 以上。论文列出 OXE、DROID、AgiBot、Ego4D、OpenVid 等来源，但未明确总小时数、总片段数或各源比例。官方仓库发布部分视频与基准权重、基准代码，但事件级大规模预训练所需完整数据与配方未公开。[表 1](../papers/video-prediction-policy-2/figures/tab-01.png)、[代码 README](https://github.com/roboterax/video-prediction-policy-2)

## 实验

| 评测 | VPP2 | 对照与条件 |
| --- | ---: | --- |
| 视频指令遵循：人手 / 机器人 | 0.80 / 0.90 | Cosmos3-64B：0.70 / 0.78；每类 50 个图像–指令对，GPT 类评估器打分，另有人类成对比较。表 2。 |
| ALOHA 真机未见任务平均成功率 | 58.5% | π0.5：40.0%，Fast-WAM：20.5%；本体已见、任务未微调，比较模型用相同 ALOHA 训练数据。图 8。 |
| LIBERO-ID / Pro / OOD | 98.8% / 45.0% / 63.9% | 标准四套 LIBERO 训练后的泛化评估；表 3。 |
| RoboDojo-Sim | score 39.26；成功率 32.26% | 基准专门训练；比较基线取自截至 2026-09 的排行榜。表 4。 |

摘要中的 11.0 个百分点是人手/机器人两类平均 `0.85−0.74`；18.5 个百分点是 ALOHA 上 `58.5−40.0`。不能把它们理解成所有子任务都有同幅提升。[表 2](../papers/video-prediction-policy-2/figures/tab-02.png)、[图 8](../papers/video-prediction-policy-2/figures/fig-08.png)

## 局限性与复现边界

- 视频指标的测试集只有 100 个图像–指令对，主要指令遵循分数由模型评估器给出；需要更大、独立且含真实接触结果的评测来确认普适性。
- ALOHA “zero-shot”指已见本体上的未见任务；LIBERO/RoboDojo 则经过基准专门训练，不能混为同一种零样本能力。
- 视频与动作的因果联系仍受数据组成、caption 质量、后训练方式影响；图 1 的解释是合理动机，不是独立因素的严格证明。
- 公开配置和通用论文设置不完全一致：LIBERO/RoboDojo 评测使用 10 次动作 Euler 步，而论文报告 5 步；RoboDojo 发布配置是 Action2B。按具体基准配置复现。[LIBERO 指南](https://github.com/roboterax/video-prediction-policy-2/blob/main/docs/libero.md)、[RoboDojo 指南](https://github.com/roboterax/video-prediction-policy-2/blob/main/docs/robodojo.md)

## 应用到我的机器人

**集成思路：**从存在多个相似目标的桌面双臂任务开始，按完整事件切示教、写清目标与左右手，先比较视频目标定位和接触时刻，再把固定窗视频表示接到现有动作策略或轻量动作专家。

**传感器与算力：**至少同步主视角 RGB、机器人状态、末端位姿、动作和标定；腕部相机有助于接触判断。完整 14B 视频主干需要高显存 GPU，资源有限时先验证事件切分与详细 caption 是否改善视频预测。

**预期收益：**减少左右手和相似目标混淆，提高未见任务组合时的动作选择。**风险：**视频预测错误会传给动作、坐标对齐错误会反转动作语义、详细 caption 成本高、推理延迟可能超出控制预算。部署前应与纯动作基线比较，并用闭环重规划与动作限幅保护执行。
