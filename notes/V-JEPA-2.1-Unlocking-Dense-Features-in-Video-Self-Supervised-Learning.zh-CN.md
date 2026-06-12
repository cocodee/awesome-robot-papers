# V-JEPA 2.1：解锁视频自监督学习中的 Dense Features

## 元数据

- 作者：Lorenzo Mur-Labadia, Matthew Muckley, Amir Bar, Mido Assran, Koustuv Sinha, Mike Rabbat, Yann LeCun, Nicolas Ballas, Adrien Bardes
- 会议/年份：arXiv，2026
- 来源：https://arxiv.org/pdf/2603.14482
- arXiv：2603.14482v2，2026-03-17
- 本地 PDF：[../papers/V-JEPA-2.1-Unlocking-Dense-Features-in-Video-Self-Supervised-Learning.pdf](../papers/V-JEPA-2.1-Unlocking-Dense-Features-in-Video-Self-Supervised-Learning.pdf)
- 本地 Markdown：[../papers/V-JEPA-2.1-Unlocking-Dense-Features-in-Video-Self-Supervised-Learning.md](../papers/V-JEPA-2.1-Unlocking-Dense-Features-in-Video-Self-Supervised-Learning.md)
- 代码：https://github.com/facebookresearch/vjepa2

## 研究问题

V-JEPA 2 能学习强的全局视频表示，但 patch feature 不一定适合深度估计、分割、跟踪、抓取和导航这类 dense spatial tasks。本文要回答的问题是：如何保留 JEPA 的预测式世界模型优势，同时让视频特征具备空间 grounding、时间一致性，并能用于机器人 dense perception。

## 核心方法

V-JEPA 2.1 从四个方面修改自监督训练 recipe：

- dense predictive loss 同时监督 masked tokens 和 visible context tokens；
- distance-weighted context loss 防止可见 token 只作为全局聚合器，鼓励局部空间 grounding；
- deep self-supervision 在多个中间 encoder 层施加自监督目标；
- modality-specific tokenizers 支持图像和视频在同一个共享 encoder 中统一训练。

模型还通过更大、更丰富的图像视频数据进行 scaling。论文发布了较大的 ViT-g/G 模型，也发布了蒸馏后的 ViT-B/L 变体，因此既可以作为研究规模 backbone，也可以作为较小下游系统的候选感知模块。

## 关键创新

本文的关键创新是指出 V-JEPA feature 对 dense tasks 较弱的原因：如果 loss 只施加在 masked 区域，可见 context token 可能会压缩全局信息，而不保留精确局部结构。V-JEPA 2.1 让所有 token 都参与预测目标，并通过多层监督把局部信息保留到更深层。

对机器人来说，这一点很重要，因为很多视觉规划失败并不是高层语义错误，而是几何、深度、物体边界和夹爪相对位置细节错误。

## 实际解决的问题

V-JEPA 2.1 解决的是全局视频理解和机器人所需 dense perception 之间的缺口。一个模型可以很好地识别动作，但仍然无法稳定定位物体局部、从单目图像推断深度或规划精细夹爪动作。本文在保留全局运动理解能力的同时，提高 dense representation 质量。

机器人收益很直接：更好的 dense features 改进真实机器人抓取，也让 latent navigation planning 更快、更准确。

## 实验证据

论文报告 Ego4D short-term object-interaction anticipation 为 7.71 mAP，EPIC-KITCHENS action anticipation 为 40.8 Recall@5。它还报告 Something-Something-V2 为 77.7，NYUv2 linear probe 深度估计为 0.307 RMSE，并在语义分割和目标跟踪上给出强结果。

在操作任务中，V-JEPA 2.1 使用与 V-JEPA 2 类似的 action-conditioned predictor，在 DROID 上训练后零样本部署到 Franka Panda。与 V-JEPA 2 相比，V-JEPA 2.1 改进 grasp 成功率：在同样 800 samples、10 次 CEM iteration、horizon 1 下，reach 仍为 100%，grasp 从 60% 提升到 70%，pick-and-place 保持 80%。当 horizon 增加到 8、samples 降到 300 时，grasp 达到 80%，规划时间约 14 秒。

在导航任务中，基于 V-JEPA 2.1 表示的 latent world model 从图像目标规划 2 秒轨迹。论文报告规划时间 10.6 秒，而 NWM 基线为 103.2 秒；ViT-G 的平均 ATE/RTE 约为 2.990/0.688，并在 TartanDrive 上达到 5.687 ATE。

## 局限性

V-JEPA 2.1 改善了 dense features，但没有消除 latent planning 的主要部署约束。操作规划仍然需要数秒级每动作，失败仍集中在夹爪动作时序，例如过早闭合、没有夹稳物体或搬运过程中打开。

真实机器人实验仍然较窄：Franka 桌面任务、目标图像条件、有限物体类别。论文提升了空间理解，但还没有解决长时域任务规划、语言目标、接触丰富装配或带安全约束的在线控制。

## 对机器人研究的影响

如果机器人需要一个同时支持高层视频理解和局部几何的感知 backbone，这篇论文很有价值。对操作来说，dense features 可以改进抓取点定位和对深度敏感的接近动作。对导航来说，时间一致的 dense features 可以支持图像目标规划，而不必重建逼真的像素视频。

它也给出了一个模型选择标准：不要只用动作识别或 VQA 来判断视频 backbone。对机器人来说，还要评估 frozen dense features 在深度、分割、跟踪和目标条件控制上的表现，因为这些更接近真实执行中的失败来源。

## 应用到我的机器人

如果任务需要精确空间推理，例如抓杯沿、对齐小物体、在杂乱环境中视觉伺服或根据图像目标导航，V-JEPA 2.1 比 V-JEPA 2 更适合作为默认 backbone。可以先把 encoder 作为 frozen feature extractor，再训练深度、物体 mask 或 action-conditioned latent prediction 的任务头。

所需输入包括 RGB 视频、用于世界模型训练的动作和末端执行器日志，以及用于小型验证 probe 的深度或分割标签。计算需求取决于模型大小：ViT-G 适合离线训练和评估，蒸馏后的 ViT-B/L 更适合 onboard 实验。预期收益是更好的深度敏感性、更干净的物体局部特征，以及更少的空间规划失败。主要风险是延迟仍高、夹爪控制错误，以及公开视频预训练数据与机器人相机视角不匹配。

## 实施建议

实际采用时，可以先在机器人自己的相机画面上并排评估 V-JEPA 2 和 V-JEPA 2.1。第一步用 frozen features 做简单 linear probe，对比深度或分割。第二步在同一小型操作数据集上对比 action-conditioned latent planning。如果 V-JEPA 2.1 只提升 dense probe 但没有提升控制，应先检查夹爪动作标签和 planner horizon，再考虑更换 backbone。
