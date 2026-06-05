# Tuna-2：像素嵌入在多模态理解与生成中超过视觉编码器

## 元数据

- 作者：Zhiheng Liu, Weiming Ren, Xiaoke Huang, Shoufa Chen, Tianhong Li, Mengzhao Chen, Yatai Ji, Sen He, Jonas Schult, Belinda Zeng, Tao Xiang, Wenhu Chen, Ping Luo, Luke Zettlemoyer, Yuren Cong
- 会议/年份：arXiv，2026
- 来源：https://arxiv.org/pdf/2604.24763
- arXiv：2604.24763v2，最后修订于 2026-05-18
- 项目页：https://tuna-ai.org/tuna-2/
- 代码：https://github.com/facebookresearch/tuna-2
- 本地 PDF：[../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.pdf](../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.pdf)
- 转换 Markdown：[../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.md](../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.md)

## 研究问题

Tuna-2 研究的是：统一多模态模型是否真的需要预训练视觉编码器或 VAE latent？论文试图验证，视觉理解、文生图和图像编辑能否在一个端到端系统里直接基于 pixel embeddings 学出来。

从机器人角度看，对应的问题是：如果不继承固定视觉编码器的分辨率限制和语义偏置，模型能否学到对细粒度视觉细节更敏感的表示？

## 核心方法

Tuna-2 从之前的 Tuna 架构出发，逐步移除视觉编码模块。Tuna-R 先移除 VAE，但保留 SigLIP 2 representation encoder。Tuna-2 进一步移除 representation encoder，只用简单 patch embedding layer 把原始图像像素转成 token，再交给 Qwen2.5-7B-Instruct decoder 处理。

图像生成方面，Tuna-2 不使用 latent diffusion，而是在像素空间做 rectified flow。模型使用 x-prediction 和 v-loss，从带噪像素输入中预测干净图像，条件可以是文本，也可以是图像加编辑指令。视觉理解则通过同一个模型的 language modeling head 完成。

训练分两阶段。第一阶段是 full-model pretraining，用 image captioning 和 text-to-image generation 数据联合训练，其中包括 550M 内部图文对和 text-only 数据。第二阶段是 SFT，用图像指令跟随、图像编辑和高质量生成数据微调。Tuna-2 还在预训练后期加入 masking-based visual feature learning：随机遮住一部分图像 patch，用 learnable mask token 替换，让生成任务更难，也迫使理解任务在部分视觉信息缺失时仍能推理。

## 关键创新

- Encoder-free unified multimodal model：原始图像 patch 直接进入 decoder，不再依赖预训练视觉编码器。
- VAE-free pixel-space generation：文生图和图像编辑直接在像素空间用 flow matching 完成。
- 用 Tuna-R 做受控对比，清楚拆分 representation encoder 和 pixel embeddings 的影响。
- masking-based feature learning 同时正则化理解和生成任务。
- 证明在足够大规模预训练后，encoder-free pixel-space 训练可以在细粒度视觉理解上超过 encoder-based 方案。

## 实际解决的问题

Tuna-2 主要解决统一多模态模型里的表示不一致问题。很多系统理解用一种视觉表示，生成用另一种表示，或者依赖预训练 encoder 的固定先验。Tuna-2 把这些压缩成一个像素空间表示和一条端到端训练路径。

它还针对细粒度感知问题。固定视觉编码器可能压缩掉小物体、文字细节、局部几何、异常视觉线索或接触边界。Tuna-2 的 pixel embeddings 给模型保留了更直接的细节访问能力，因此在 pixel-centric benchmark 和 attention 可视化中表现更好。

## 实验

多模态理解方面，Tuna-2 在 7B 级 native unified multimodal model 中有很强表现。论文报告 GQA 65.0、RealWorldQA 67.7、MMVet 51.7、MMMU 50.7、MMVP 77.3、OCRBench 79.7、V* 59.2、CountBench 81.7、VisuLogic 28.8。关键不是单个分数，而是趋势：在足够预训练后，Tuna-2 通常超过 Tuna-R，尤其是在依赖细粒度视觉感知的任务上。

图像生成方面，Tuna-2 有竞争力，但 Tuna-R 往往略强。Tuna-2 的 GenEval overall 为 0.87，DPG-Bench overall 为 86.54。这说明 representation encoder 的语义先验对生成仍然有帮助，不过随着 scale 和 SFT 增加，差距会缩小。

图像编辑方面，Tuna-2 超过 OmniGen、BAGEL、UniWorld、OmniGen2 等早期 unified baseline，但仍落后于 Tuna 和 Tuna-R。重建实验显示，Tuna-2 作为 unified tokenizer 在 ImageNet 上表现很强，512 分辨率下 rFID 为 0.15、PSNR 为 32.80、SSIM 为 0.93。

消融实验很有实践价值。生成与理解数据比例中，7:3 是较好的 tradeoff。masking 对 Tuna-R 和 Tuna-2 都有提升，而且 Tuna-2 受益更明显。训练曲线显示，Tuna-R 因为有预训练 encoder，早期学得更快；但 Tuna-2 随着数据规模增加会追上并在理解任务上超过它。

## 局限性

Tuna-2 的训练成本非常高。论文中的 7B 设置使用 550M 内部图文对、64 个节点、300k 预训练 step、每 GPU 16k sequence length，然后还要 50k step SFT。这不是小型机器人项目可以直接复现的训练方案。

论文的主要验证对象是图像，不是真实机器人视频、3D 状态、时间一致性、动作预测或闭环控制。因此对机器人来说，Tuna-2 更像是一个感知和生成表示方向，而不是可直接部署的机器人策略。

encoder-free 设计在大规模下提升理解，但并不是所有任务都赢。Tuna-R 在不少生成和编辑指标上仍略强，说明预训练视觉先验依然有价值。官方代码已经公开，但项目页说明完整生产训练权重因政策限制暂不释放，只计划发布移除少量层的基础 checkpoint。

## 机器人实践影响

Tuna-2 对机器人有价值，是因为很多机器人失败都来自细节感知不足：小物体姿态变化、细把手、电缆几何、透明物体、标签文字、工具尖端、接触边界和遮挡区域。像素空间表示可能保留通用 VLM encoder 会压缩掉的信号。

它也给机器人世界模型一个方向。与其用 VAE latent 生成未来帧并损失接触细节，不如在窄任务里尝试 pixel-space flow matching，做短时未来图像预测或图像条件编辑，再和 value model 或 action model 结合。

## 应用到我的机器人

对我的机器人，不建议从零训练 Tuna-2。更现实的做法是复用它的设计思想：

- 对夹爪、物体接触区、标签、小目标部件等关键区域使用 raw-patch 或高分辨率 crop token；
- 保留一个 VLM encoder 做全局场景理解，同时增加 pixel-space 分支处理局部细节；
- 在机器人相机帧上做 masked visual prediction，让模型学习遮挡下的稳健局部特征；
- 对接触细节重要的短 horizon，使用 pixel-space future prediction；
- 用机器人自己的感知任务评估，例如小物体计数、标签读取、把手定位、夹爪是否真实接触物体、near-failure 状态识别。

需要的传感器主要是 RGB 相机，最好同时有腕部相机和外部固定相机。Tuna-2 本身不需要深度，但真实机器人上我会保留深度或触觉作为独立监督，因为像素空间图像建模并不保证物理正确。

预期收益是更好的细粒度视觉感知，以及在接触丰富任务中更保真的视觉想象。主要风险是计算成本高、像素空间训练不稳定、逐帧使用时缺少时间一致性，以及视觉细节变好但动作选择不一定变好。

## 实施建议

第一步可以做一个小型 masked pixel-prediction 模型，只针对腕部相机 crop。训练它重建 masked patch，并在 action-conditioned observation 下预测短时未来 crop。先把这些特征和标准 VLM encoder 在接触状态分类、小目标定位任务上对比，再考虑接入策略模型。
