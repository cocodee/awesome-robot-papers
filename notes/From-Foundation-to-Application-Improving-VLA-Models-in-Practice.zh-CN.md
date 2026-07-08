# From Foundation to Application：在实践中改进 VLA 模型

## 元数据

- 作者：Wei Wu, Fangjing Wang, Fan Lu, He Sun, Shi Liu, Yunnan Wang, Yibin Yan, Yong Wang, Shuailei Ma, Xinyang Wang, Yibin Liu, Shuai Yang, Tianxiang Zhou, Kejia Zhang, Lei Zhou, Cheng Su, Nan Xue, Bin Tan, Han Zhang, Youchao Zhang, Fei Liao, Xing Zhu, Yujun Shen, Kecheng Zheng
- 会议/年份：arXiv，2026
- 来源：https://arxiv.org/pdf/2607.06403
- arXiv：2607.06403v1，2026-07-07
- 本地 PDF：[../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.pdf](../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.pdf)
- 本地 Markdown：[../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.md](../papers/From-Foundation-to-Application-Improving-VLA-Models-in-Practice.md)
- 项目页：https://technology.robbyant.com/lingbot-vla-v2
- 代码：https://github.com/robbyant/lingbot-vla-v2
- Checkpoints：https://huggingface.co/collections/robbyant/lingbot-vla-v2

## 研究问题

本文要回答的问题是：VLA 基础模型如何从实验室基准走向真实机器人应用？真实部署中，机器人不仅要完成干净的双臂操作任务，还要面对不同本体、全身动作空间、移动操作、灵巧手、动态场景和长程任务。

## 核心方法

LingBot-VLA 2.0 在三个实践维度上改进上一代 LingBot-VLA。

第一，扩大并清洗预训练数据。作者从 20 种机器人本体收集约 90,000 小时机器人数据，经过过滤后保留 50,000 小时高质量轨迹；同时构建约 20,000 小时人类第一视角视频池，经过 VLM 过滤、重建、标准化和运动质量检查后保留约 10,000 小时。

第二，使用 55 维 canonical state/action 表示，覆盖手臂关节、末端位姿、夹爪、灵巧手、腰部、头部和移动底盘信号。不存在的身体部件用 padding 处理，因此单臂、双臂、半身人形、全尺寸人形、移动操作机器人和人类第一视角手部轨迹可以进入同一训练接口。

第三，action expert 使用 sparse MoE 层，感知侧加入 dual-query distillation。current query 学当前几何和时序特征，future query 学 action chunk horizon 处的未来表示。LingBot-Depth 提供深度几何监督，DINO-Video 提供 causal video 特征作为时序监督。

## 关键创新

这篇论文最有价值的点不是某个单独模块，而是把预训练方式和真实部署需求对齐：

- 数据过滤关注 robot state 与视频是否对齐，以及动作是否平滑；
- 动作表示覆盖全身自由度，而不只控制机械臂或末端；
- MoE 容量放在 action expert 中，用于多本体动作建模；
- 未来预测作为训练时的表征目标，而不是部署时必须显式生成未来视频。

因此它更像一份面向真实机器人 VLA 系统的工程路线图。

## 实际解决的问题

LingBot-VLA 2.0 主要解决三个实践问题：

- 多本体泛化：训练数据来自不同运动学、相机、手部机构和控制频率的机器人；
- 更丰富的控制空间：支持头部、腰部、移动底盘和灵巧手，而不仅是双臂；
- 长程操作中的时序推理：模型需要预判未来场景状态和动作后果，而不只是响应当前图像。

论文还给出了具体的数据工程信号：过滤 jerk 过大、速度或加速度 Z-score 异常、几乎全程静止、视频模糊、掉帧、多视角不同步、机器人状态与视频不匹配的样本。

## 实验

在 GM-100 的 9 个双臂任务上，论文采用 generalist mixed-training 设置，即单个策略同时训练多个任务。LingBot-VLA 2.0 在总体 progress score 上最好。在 Agilex Cobot Magic 上，它达到 66.2% progress / 34.4% success，高于 LingBot-VLA 1.0 的 58.2% / 30.0%，也高于 pi0.5 的 59.1% / 32.2%。在 Galaxea R1 Pro 上，它达到 34.6% / 15.6%，高于 LingBot-VLA 1.0 的 32.7% / 15.6% 和 pi0.5 的 27.4% / 8.9%。

在长程移动操作上，论文测试了 Astribot S1 的“把物体放进冰箱”和 Cobot Magic-ARX X5 的“清洁灶台”，每个任务设置 15 次试验。LingBot-VLA 2.0 在 in-domain 和 OOD 设置下都优于 pi0.5。冰箱整理任务中，它达到 77.1% / 60.0% in-domain 和 37.0% / 13.3% OOD；灶台清洁任务中，它达到 84.3% / 66.7% in-domain 和 67.5% / 40.0% OOD。

消融实验对落地很有参考价值。relative joint action 明显优于 absolute joint action，平均成功率从 33.7% 提升到 55.0%。在论文设置中，MeanStd normalization 优于 MinMax 和 Q01-Q99。L2 loss 的平均表现优于 L1，不过在挤番茄酱这类接触丰富任务上 L1 更好。

## 局限性

实验中 progress score 和 success rate 之间仍有明显差距，说明模型经常能完成一部分流程，但会在最终摆放、释放或精确完成阶段失败。不同机器人本体之间差异也很大：Agilex Cobot Magic 的结果显著好于 Galaxea R1 Pro，说明相机视角、运动学、动作空间对齐仍然是难点。

该方法的数据和基础设施门槛也很高：需要数万小时机器人和第一视角数据、多阶段过滤、VLM 标注、SLAM 与手部姿态重建、大规模预训练，以及深度和视频 teacher 模型。论文并没有消除真实机器人评测、安全控制层和任务级校准的需求。

## 对机器人实践的影响

对真实机器人项目来说，最重要的结论是：VLA 的部署效果不只取决于模型结构，也强烈依赖数据和动作接口工程。即使不复现完整规模，也可以吸收这些原则：

- 把所有机器人数据标准化到统一 state/action schema；
- joint-space 策略优先尝试 relative action target；
- 默认先尝试 MeanStd normalization，再按任务验证；
- 训练时加入未来视觉特征预测作为辅助目标；
- 建立动作平滑性和视频状态对齐的自动过滤；
- 长程任务同时记录 progress score 和 binary success。

## 应用到我的机器人

如果我的机器人不只是简单机械臂，而是包含移动底盘、腰部、头部相机、双臂、灵巧手或多种末端执行器，这篇论文很值得参考。可行集成方案是：为所有可控身体部件定义 padded canonical action vector，用同步相机、机器人状态、语言指令和 action chunks 训练 VLA 策略，并在训练时加入未来特征预测头。

所需传感器和算力包括标定好的 RGB 相机、机器人关节与底盘状态、同步动作日志、足够的视频轨迹存储、GPU 训练环境，以及最好有深度或视频 teacher 模型用于蒸馏。预期收益是更好的跨任务和跨本体迁移，尤其是长程移动操作。主要风险是数据对齐差、不同本体动作约定不一致、模型过大导致延迟，以及没有底层安全控制器时全身动作不安全。

## 实施建议

不要从一开始就复现完整 LingBot-VLA 2.0。更现实的第一步是在已有示教数据上做 canonical action schema，然后比较：

- absolute joint target 与 relative joint target；
- 不同任务中的 joint action 与 end-effector action；
- MinMax、Q01-Q99、MeanStd normalization；
- 只训练动作预测，与加入未来视觉特征预测的动作训练。

如果 relative target 加 future-feature supervision 能提高 progress score，并且不增加部署延迟，就说明 LingBot-VLA 2.0 的路线值得继续扩大规模。
