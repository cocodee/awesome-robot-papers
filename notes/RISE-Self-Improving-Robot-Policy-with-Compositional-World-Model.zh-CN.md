# RISE：基于组合式世界模型的机器人策略自我提升

## 元数据

- 作者：Jiazhi Yang, Kunyang Lin, Jinwei Li, Wencong Zhang, Tianwei Lin, Longyan Wu, Zhizhong Su, Hao Zhao, Ya-Qin Zhang, Li Chen, Ping Luo, Xiangyu Yue, Hongyang Li
- 会议/年份：arXiv，2026
- 来源：https://arxiv.org/pdf/2602.11075
- arXiv：2602.11075v2，最后修订于 2026-04-28
- 项目页：https://opendrivelab.com/RISE
- 代码：https://github.com/OpenDriveLab/RISE
- 本地 PDF：[../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.pdf](../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.pdf)
- 转换后的 Markdown：[../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.md](../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.md)

## 研究问题

本文关注的问题是：如何让 VLA 机器人策略在接触丰富、动态、长时程操作任务中自我提升，同时避免直接在真实机器人上做昂贵且有风险的在线强化学习？

核心矛盾是，模仿学习训练出来的 VLA 策略能复现示教，但一旦执行轨迹偏离专家分布，就容易出现误差累积，缺少恢复能力。真实世界 RL 理论上可以通过成功和失败提升鲁棒性，但真实机器人交互慢、串行、需要重置，还有安全和硬件成本。RISE 的目标是把在线 RL 的交互过程搬到一个学出来的“想象空间”里。

## 核心方法

RISE 构建了一个组合式世界模型，由两个相互独立的模块组成：

- 可控 dynamics model：根据历史多视角观测和候选动作块，预测未来多视角图像；
- progress value model：给想象出来的状态打分，并把进度差转换成策略改进所需的 advantage。

dynamics model 从 Genie Envisioner 初始化，再适配机器人动作条件输入。它接收顶视相机和腕部相机等多视角 RGB 观测，预测短时未来。作者还提出 task-centric batching，让每个训练 batch 更强调同一类任务场景下的动作多样性，从而提升动作可控性，而不只是提升画面真实感。

value model 从预训练 VLA backbone 初始化，并结合两个训练目标。progress regression 提供稠密的时间进度信号，Temporal-Difference learning 利用成功和失败轨迹，让 value 对细微接触失败更敏感。动作块的 advantage 被定义为当前观测和想象未来观测之间的平均 value 提升。

策略训练分两阶段。第一阶段是 warm-up：在真实离线数据上微调 VLA，包括专家示教、策略 rollout、失败轨迹和人工纠正数据，同时加入 advantage conditioning。第二阶段是 self-improving loop：从离线状态开始，让 rollout policy 提出高 advantage 动作，用世界模型想象未来状态，用 value model 评估这些未来，再用得到的动作和 advantage 样本训练策略。世界模型只在训练阶段使用，因此部署时不会增加策略推理开销。

## 关键创新

本文的关键创新是把学出来的视觉世界模型作为真实机器人 foundation policy 的在线 RL 环境，同时把世界模型拆成 dynamics 和 value 两个模块，而不是要求单一模型同时完成仿真和奖励判断。

这个拆分很务实。dynamics model 专注于快速、动作可控的多视角未来预测；value model 专注于任务进度和失败敏感性。两者组合后，可以直接产生动作块级别的 advantage，不需要把整个任务想象到终止状态再判断成败。这对长时程任务很重要，因为视频生成模型在长 rollout 中会累积误差。

## 实际解决的问题

RISE 主要解决三个实际瓶颈：

- 减少真实机器人上高风险 trial-and-error RL 的需求；
- 让 VLA 策略获得超出纯模仿学习的恢复能力和鲁棒性；
- 为长时程操作提供比稀疏终止奖励更密集的学习信号。

这些能力特别适合小接触错误会持续放大的任务，例如抓取移动物体、操作软物体、拉拉链、关盒子、插入和双臂协作。

## 实验

论文在真实双臂平台上评估了三个任务：

- Dynamic Brick Sorting：从运动传送带上抓取彩色积木，并放入对应颜色的盒子；
- Backpack Packing：打开背包、放入衣物、提起并拉上拉链；
- Box Closing：放入杯子、折叠盒盖，并用双臂精确地把卡扣塞入盒中。

主要真实实验结果显示，RISE 相比模仿学习和 RL baseline 有明显提升：

- Dynamic Brick Sorting：RISE 成功率 85%，微调后的 π0.5 为 35%，RECAP 为 50%；
- Backpack Packing：RISE 成功率 85%，π0.5 为 30%，RECAP 为 40%；
- Box Closing：RISE 成功率 95%，π0.5 为 35%，RECAP 为 60%。

消融实验很关键。在 Dynamic Brick Sorting 上，只加入 online action 会把完成率从 35% 提到 40%；同时加入 online action 和想象出来的 online state 后，完成率提升到 70%。去掉 dynamics pretraining 后完成率降到 15%，去掉 task-centric batching 降到 40%，去掉 progress loss 降到 50%，去掉 TD learning 降到 35%。这说明 dynamics model 和 value model 的设计都不是可有可无的。

在 dynamics 质量上，RISE 相比 Cosmos 和 Genie Envisioner 在动作可控性和视觉质量上更好。在作者的真实任务中，RISE 的 PSNR、LPIPS、SSIM 和 EPE 指标整体优于对比模型，其中 EPE 从 Cosmos 的 1.21、GE 的 1.05 改善到 RISE 的 0.54。

## 局限性

RISE 仍然受限于学到的世界模型的准确性和覆盖范围。对于罕见状态、数据中不足的失败模式或特殊接触情况，世界模型仍可能生成物理上不合理的转移，从而给策略提供错误 advantage。

该方法也仍然需要不少真实机器人数据来锚定学习过程。论文的结果表明，真实离线数据和想象在线数据的混合比例非常重要；真实数据太少会导致策略崩溃，真实数据太多又会限制策略改进。

最后，RISE 把成本从真实交互转移到了计算。论文中 dynamics 预训练使用 16 张 H100 约 7 天，任务特定 dynamics 微调用 8 张 H100 约 3 天，value 和 policy 训练也依赖多 GPU。对于小型机器人项目，更现实的路线是使用更轻量的世界模型、蒸馏模型，或只做窄任务版本。

## 应用到我的机器人

如果我的机器人已经有一个 VLA、diffusion policy 或 flow policy，能够完成示教中的动作，但在小偏差后容易失败，那么 RISE 的思路很值得借鉴。与其直接在真实机器人上做高风险在线 RL，不如先用想象 rollout 给策略提供改进信号。

一个实际适配方案是：

- 收集同步多视角视频、动作块、语言或任务标签、成功轨迹、失败轨迹和人工纠正数据；
- 训练一个任务特定、动作条件的短时未来预测模型，不要一开始就追求完整任务级仿真；
- 训练一个能评估任务进度并惩罚失败状态的 value model；
- 用短时想象未来计算 advantage；
- 在固定混入真实离线数据的前提下，用 advantage conditioning 微调策略。

所需硬件和数据包括至少一个全局相机，最好有腕部相机，准确同步的机器人动作，足够的示教和失败 rollout，以及用于视频模型微调的 GPU。对于较小的机器人，第一步不应复现完整 RISE，而应尝试短时 latent dynamics 或图像特征预测，对比“只做动作微调”和“加入 advantage-conditioned 微调”是否能提升偏离示教后的恢复能力。

预期收益是更高鲁棒性、更强恢复能力、更低真实探索风险，以及从失败中获得更有用的训练信号。主要风险是世界模型幻觉、value model 打分错误、算力成本高，以及想象图像状态和真实相机观测之间的分布偏移。

## 实施建议

最现实的起点是一个窄任务，例如分拣、插入、关抽屉、关盒子或软物体放置。不要一开始就做通用机器人模拟器。最小可行版本是：

- 先用示教训练当前策略；
- 收集成功、失败和人工纠正 rollout；
- 从这些轨迹中学习 progress/value scorer；
- 在学到的视觉或 latent dynamics model 中生成短候选动作 rollout；
- 训练策略偏向高 advantage 动作块，同时每个 batch 保持固定比例的真实离线数据。

论文的离线数据比例消融说明，这个混合比例不是细节。在他们的设置中，离线数据比例约 0.6 时效果最好；本地实现时应把这个比例作为关键超参数调试，而不是假设想象数据可以完全替代真实数据。
