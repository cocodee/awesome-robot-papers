<!-- markdownlint-disable MD013 -->

# MolmoAct2：面向真实部署的 Action Reasoning Models

## 元数据

- 作者：Haoquan Fang, Jiafei Duan, Donovan Clay, Sam Wang, Shuo Liu, Weikai Huang, Xiang Fan, Wei-Chuan Tsai, Shirui Chen, Yi Ru Wang, Shanli Xing, Jaemin Cho, Jae Sung Park, Ainaz Eftekhar, Peter Sushko, Karen Farley, Angad Wadhwa, Cole Harrison, Winson Han, Ying-Chun Lee, Eli VanderBilt, Rose Hendrix, Suveen Ellawela, Lucas Ngoo, Joyce Chai, Zhongzheng Ren, Ali Farhadi, Dieter Fox, Ranjay Krishna
- 会议/年份：arXiv，2026
- 来源：[arXiv PDF](https://arxiv.org/pdf/2605.02881)
- arXiv：2605.02881v2，2026-05-08
- 本地 PDF：[../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.pdf](../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.pdf)
- 转换 Markdown：[../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.md](../papers/MolmoAct2-Action-Reasoning-Models-for-Real-world-Deployment.md)
- 项目页：[MolmoAct2 project page](https://allenai.org/blog/molmoact2)
- 代码：[allenai/molmoact2](https://github.com/allenai/molmoact2)

## 研究问题

开放 VLA 模型能否真正面向真实机器人部署：既能闭环控制、又能高成功率微调，还要开放权重、数据和训练方法，并且可以落到低到中等成本的机器人平台上？

论文认为当前 VLA 系统通常至少卡在一个问题上：前沿模型闭源，开放模型常绑定特定昂贵平台，带 reasoning 的策略推理延迟太高，微调后的成功率也还不足以支撑可靠部署。

## 核心方法

MolmoAct2 是一个三阶段 VLA 训练流程，核心是空间 reasoning VLM backbone 加连续动作专家。

第一步训练 Molmo2-ER。它基于 Molmo2，面向 embodied reasoning 做专门训练，使用 3.3M 样本的 embodied reasoning 数据，覆盖空间问答、指点、检测、视频 embodied QA、多图像 ego-exo 推理和抽象空间推理。训练采用 specialize-then-rehearse：先强化具身能力，再混合通用数据复习，减少通用视觉语言能力遗忘。

第二步训练 MolmoAct2-Pretrain，把 Molmo2-ER 变成离散自回归机器人策略。机器人状态被离散成 state tokens；未来 1 秒的连续动作块由 MolmoAct2-FAST 转成 action tokens。MolmoAct2-FAST 是开放权重、开放数据的动作 tokenizer，训练在一百万条动作序列上，覆盖 YAM、SO-100/101、DROID Franka、Google Robot 和 WidowX 风格数据。

第三步 post-training 加入 DiT 风格的 flow-matching action expert，用来输出连续控制。action expert 与 VLM 一样有 36 层。它不是只看 VLM 最后一层 hidden state，而是在每一层 cross-attend 到对应 VLM 层的 keys 和 values。这个 per-layer KV conditioning 让连续控制器直接使用 VLM 的视觉语言注意力状态。

MolmoAct2-Think 进一步加入自适应深度 token reasoning。它预测一个 10 x 10 的深度 token 网格，但对静态区域复用缓存，只重新生成 RGB patch 发生变化的格子。目标是在保留几何 grounding 的同时，降低每个控制步的 reasoning 延迟。

## 关键创新

这篇论文的贡献不是单个模块，而是一个面向部署的开放 VLA 栈：

- Molmo2-ER：先增强空间和具身 reasoning 的 VLM backbone；
- MolmoAct2-BimanualYAM：720 小时、34.5K 条双臂 YAM 示教，同时提供过滤后的 DROID 和 SO-100/101 数据；
- MolmoAct2-FAST：把多种机器人连续动作转为离散 action tokens 的开放 tokenizer；
- per-layer KV conditioning：把离散 token VLM 与连续 flow-matching 动作专家连接起来；
- MolmoAct2-Think：只更新变化区域的自适应深度 reasoning。

这套组合同时针对可复现性、多 embodiment 覆盖、推理延迟和连续控制接口。

## 实际解决的问题

MolmoAct2 主要解决开放机器人 foundation model 的部署缺口。它不仅给 checkpoint，还给数据、tokenizer、训练方法和代码，使研究者可以检查、复现和迁移。

它也解决了 VLM token prediction 与真实机器人连续控制之间的不匹配。离散 action tokens 适合大规模预训练，但真实机器人需要平滑连续轨迹。flow-matching action expert 可以直接生成连续动作块，同时仍然利用 VLM 的视觉语言 grounding。

对于 reasoning 延迟，MolmoAct2-Think 避免在相邻控制步重复生成几乎不变的 dense geometric tokens。这对桌面操作尤其有用，因为背景和很多物体在连续帧中基本静止。

## 实验证据

在 embodied reasoning 上，Molmo2-ER 在 13 个 benchmark 的平均分为 63.8%，超过论文中对比的强开源模型和闭源模型；相对 Molmo2 起点提升 17 个点。

在 DROID 风格的 out-of-the-box 部署中，MolmoAct2-DROID 在 MolmoSpaces 上平均成功率 37.7%，高于 pi-0.5-DROID 的 34.5%。在真实 DROID 风格任务中，面对新场景、随机相机位姿和新物体，MolmoAct2-DROID 平均成功率 87.1%，高于 MolmoBot 的 48.4% 和 pi-0.5-DROID 的 45.2%。

在 SO-100 真实任务上，MolmoAct2-SO 平均成功率 56.7%，高于论文中 SO-100/101 版 pi-0 的 45.3%，也明显高于 SmolVLA 的 2.3%。

微调后，MolmoAct2 在 LIBERO 上平均成功率 97.2%，MolmoAct2-Think 提升到 98.1%。在 RoboEval 上，MolmoAct2 成功率 44.3%，比 pi-0.5 高 3.8 个点。在 8 个真实双臂 YAM 任务上，MolmoAct2 平均成功率 50.1%，比第二名 OpenVLA-OFT 高 15 个点。

在扰动鲁棒性上，MolmoAct2-Think 在空间、光照、语言改写和干扰物扰动上的平均成功率为 50.69%，高于 OpenVLA-OFT 的 39.89%。

## 局限性

训练成本很高。pretraining 使用 64 张 H100 约 5,760 GPU 小时，post-training 约 2,304 GPU 小时，大规模 fine-tuning 也需要 32 到 64 张 H100。多数实验室更现实的做法是使用发布 checkpoint，而不是完整复现训练。

真实世界成功率虽然有进步，但并非所有任务都达到可放心部署的水平。双臂 YAM 微调平均成功率为 50.1%，意味着真实任务仍有大量失败。空间扰动也是短板，MolmoAct2-Think 在 spatial variation 下只有 26.25%。

论文覆盖多个 embodiment，但每个部署 checkpoint 仍然经过 embodiment-specific fine-tuning。不能假设它能零样本迁移到任意新机器人；必须处理动作空间映射、相机配置、归一化和安全验证。

MolmoAct2-Think 依赖单目深度估计和深度 token 缓存。在反光、透明、低纹理或场景剧烈变化时，错误深度可能给 action expert 引入误导。

## 应用到我的机器人

对我的机器人来说，最有价值的思路是把有 reasoning 能力的 VLM backbone 与连续 action expert 分开。一个实际适配路径是：

- 采集同步多相机图像、机器人 proprioceptive state、语言指令和动作轨迹；
- 把动作归一化到固定宽度表示，并按控制频率选择 1 秒 action chunk；
- 优先从发布的 MolmoAct2 checkpoint 开始，而不是从头训练完整栈；
- 微调时保持部署时相同的 setup/control 描述和相机顺序；
- 先评估标准 MolmoAct2 风格策略，只有当主要失败来自空间理解时，再加入深度 token reasoning。

如果是低成本机械臂或移动操作平台，SO-100/101 路线最接近。若是双臂机器人，YAM 数据更有参考价值，因为它包含家庭、实验室和服务场景中的双臂协作任务。若是 Franka 或类似机器人，过滤后的 DROID 路线最自然。

## 所需传感器和算力

最低可行配置：

- 一个腕部相机加一个外部相机，最好时间同步；
- 机器人关节状态和夹爪状态；
- 每条轨迹的语言任务标签或指令；
- 覆盖目标任务分布的示教数据；
- 能进行 VLA 微调的 GPU，或至少能低延迟运行发布 checkpoint 的推理 GPU。

MolmoAct2-Think 还需要较稳定的相机几何和可靠的深度估计。如果相机剧烈运动或整个场景频繁变化，自适应深度缓存的延迟收益会下降。

## 预期收益

相较纯 behavior cloning，MolmoAct2 可能带来更好的空间 grounding；相较只输出离散 action tokens 的 VLA，它能输出更平滑的连续动作。开放 tokenizer、数据配方和代码也让动作表示问题更容易排查。

最合适的短期实验不是完整复现，而是在自己的机器人少量示教上微调发布 checkpoint，并与 diffusion policy 或 OpenVLA 风格 baseline 对比。重点记录成功率、物体位置变化后的恢复能力、每个 action chunk 的延迟，以及相机和物体分布变化下的失败模式。

## 风险

主要风险是算力成本、动作空间不匹配、相机布局不匹配和安全性。用一种相机顺序、控制模式或动作归一化训练出的策略，换到另一种部署设置时可能严重失败。真实机器人测试应从低速执行、工作空间限制、碰撞检查和人工急停开始。
