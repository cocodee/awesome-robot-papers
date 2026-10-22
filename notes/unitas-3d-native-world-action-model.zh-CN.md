# UNITAS：三维原生世界动作模型

## 论文信息

- **标题：**UNITAS: A 3D-Native World Action Model for Embodied Manipulation
- **作者：**Ruixiang Wang、Yongyi Su 等 17 人
- **发表状态：**arXiv:2610.12099v1，2026-10-08；预印本、审稿中
- **来源：**[arXiv](https://arxiv.org/abs/2610.12099) · [本地 PDF](../papers/unitas-3d-native-world-action-model/paper.pdf) · [转换 Markdown](../papers/unitas-3d-native-world-action-model/paper.md) · [官方代码](https://github.com/DexForce/UNITAS) · [精读笔记](../papers/unitas-3d-native-world-action-model/精读笔记.md) · [详解教程](unitas-3d-native-world-action-model-tutorial.md)

## 研究问题

机器人执行与接触发生在米制三维空间，视频世界模型却通常在视角相关的像素/视觉 latent 里预测未来。如何同时预测可执行动作和动作导致的场景变化，并让多视角、不同机器人和人手数据共享一个几何接口？

## 方法与关键创新

UNITAS 在每个交互窗口内固定度量坐标系，把视觉位置、机器人/人手动作点轨迹、场景点位移都放入该帧。深度可用时用相机标定反投影视觉 token；没有深度时沿标定射线抽取 64 个 0.1–2.0m 候选深度并学习加权。每只夹爪取 20 个 URDF 点，人手用 21 个 MANO 关键点；以秒为时间轴的 tokenizer 把一个点的整个轨迹编码为一个 token。Florence-2-large 与点动力学 DiT 处理视觉/文字及未来点运动，较小的动作 DiT 预测末端控制块。世界预测以动作点轨迹为条件；缺少当前三维查询点时不能直接输出点级场景轨迹。[论文 §3](../papers/unitas-3d-native-world-action-model/paper.tex)

核心联合分解为 `p(A,u,S|C,q₀)=p(A|C)p(u|C,q₀)p(S|A,C)`：`A` 是夹爪/人手点流，`u` 是可执行动作，`S` 是场景点流。轨迹 tokenizer 先重建预训并冻结；随后用 rectified flow 的速度回归学习三个输出，附加权重 0.1 的位置编码蒸馏损失。训练场景流用示教干净动作流，推理用生成或外部给定动作流。[图 2](../papers/unitas-3d-native-world-action-model/figures/fig-02.png)

## 数据与实验

混合预训有 RoboTwin、LIBERO、VLABench、DROID、AgiBot、RoboMIND、RH20T、VITRA、自采 W1 九源；场景流仅在有有效点对应时监督。论文报告 200K 步、batch 1024、64 张 64GiB DCU。LIBERO 20Hz×20 间隔＝1 秒动作窗；RoboTwin 15Hz×20 间隔≈1.33 秒；并非所有来源一个频率。[图 6](../papers/unitas-3d-native-world-action-model/figures/fig-06.png)、[附录表 5](../papers/unitas-3d-native-world-action-model/figures/tab-05.png)

| 设置 | 结果 | 条件 |
| --- | ---: | --- |
| LIBERO 平均 | 99.8% | 混合预训后基准微调，非 zero-shot；无混合预训版 99.5% |
| LIBERO-Plus | 89.1% | 扰动鲁棒性；无混合预训版 86.5% |
| RoboTwin 2.0 clean/random | 92.94% / 93.04% | 各自基准设置 |
| 真机整理书 / 装球拉链 | 18/20 / 16/20 | 即 90% / 80%，等权平均 85% |
| RoboTwin 动作条件场景预测 | 移动 ADE 0.427cm、静态 ADE 0.043cm | 给定录制夹爪轨迹；PointWorld 0.656/0.084cm |

论文引言把装球任务写为 65%，与正文表 2 的 16/20＝80% 及摘要平均 85% 矛盾，笔记采用表 2 的试次数。LIBERO-Plus 消融中，加场景损失只把 85.74% 提到 86.47%（+0.73 点）；对策略性能的直接增益小于去掉 3D 位置编码、动作流监督或历史 token 引起的下降。无深度策略用射线路由为 84.43%，用真实深度 PE 为 84.68%，前提是相机标定仍可用。[论文表 1–4、附录 B](../papers/unitas-3d-native-world-action-model/paper.tex)

## 局限与复现状态

官方发布权重、推理/评测代码，训练代码和训练数据仍标为待发布。论文称策略仅输出动作时可跳过未来点流；当前公开 `decoder.sample(decode_target="eef")` 仍计算夹爪点流，只跳过场景流，因此论文的 55.77ms action-only 延迟不可直接套给这一公开路径。真实观测上的场景预测多为给定真实夹爪轨迹的定性展示，软物体/接触后的真实点级误差还需验证。大规模训练依赖精确手眼标定、点对应和多源动作定义。[官方 README](https://github.com/DexForce/UNITAS)、[公开 decoder](https://github.com/DexForce/UNITAS/blob/main/src/unitas/models/decoder.py)

## 应用到我的机器人

**集成想法：**在现有夹爪策略上先增加三维世界位置编码与 20 点夹爪轨迹辅助监督；用球入袋、插入或抓放任务比较 RGB 基线、几何编码、动作流损失。**传感器/算力：**同步多视角 RGB-D、相机内外参、URDF、关节/末端状态、动作时间戳；部署权重须实测显存与延迟，场景预测另需深度或外部三维几何，完整论文预训需大规模多卡。**预期收益：**相机换位和精细放置时更稳定的米制对齐，可额外预测给定动作的场景点变化。**风险：**标定/同步漂移、遮挡、点对应错误、真实场景流监督不足，以及公开推理路径延迟与论文表 8 不一致。

## Question Analysis / 问题分析

本次问题是按此前方式分析整篇论文；[精读笔记](../papers/unitas-3d-native-world-action-model/精读笔记.md)和[详解教程](unitas-3d-native-world-action-model-tutorial.md)给出六站路线、具体两轮示例及论文/代码差异。后续特定问题可追加在本节。
