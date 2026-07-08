# World Action Models 综述：少做梦，多行动

## 元数据

- 作者：Qiuhong Shen, Shihua Zhang, Yue Liao, Qi Li, Zhenxiong Tan, Shizun Wang, Shuicheng Yan, Xinchao Wang
- 会议/年份：arXiv，2026
- 来源：https://arxiv.org/pdf/2606.20781
- arXiv：2606.20781v1，2026-06-18
- 本地 PDF：[../papers/World-Action-Models-A-Survey.pdf](../papers/World-Action-Models-A-Survey.pdf)
- 本地 Markdown：[../papers/World-Action-Models-A-Survey.md](../papers/World-Action-Models-A-Survey.md)
- 项目页：https://world-action-models.github.io/

## 研究问题

这篇综述要回答的是：什么样的模型才算 World Action Model，而不是普通 VLA、普通 world model，或者只是加了 action head 的视频生成模型？更实际的问题是，机器人策略到底应该如何使用“预测出来的未来”：是完整渲染未来视频，保留 latent future，还是完全不走视频生成路径、只保留对动作有用的预测结构？

## 核心方法

论文给 WAM 建立了一套统一词汇和设计框架。它把 WAM 定义为一种 predictive-action model：模型预测的未来必须留在动作路径中，可以是先预测未来再解码动作，也可以是用预测后果评估候选动作，还可以是在同一个模型中联合训练未来预测和动作生成。

论文用两个互补视角组织已有工作：

- 设计哲学：Render-and-Decode、Latent-Only、Video-Generation-Free。
- 组件解剖：predictive substrate、architectural backbone、action coupling、deployment regime。

随后，论文用五个控制环路属性评价 WAM：可交互性、因果性、持久性、物理合理性和泛化能力。

## 关键创新

最有价值的贡献是把“模型生成什么未来”和“动作如何使用这个未来”拆开。很多近两年的论文都叫 WAM 或接近 WAM，但实现细节和工程权衡差异很大；这篇综述提供了一个能放到同一坐标系里比较的框架。

三类设计哲学是：

- Render-and-Decode：生成像素级或可解码成像素的未来，再从未来中恢复动作。
- Latent-Only：保留视频模型带来的动态先验，但推理时停在 pixel rendering 之前，用 latent、feature、flow、mask 或 value map 来生成动作。
- Video-Generation-Free：不使用视频生成骨干，在语言、VLM、JEPA、特征、几何、affordance、音频或 latent action 空间中预测对动作有用的未来。

四轴组件解剖更适合工程选型：

- Predictive substrate：像素、特征、几何、affordance/map。
- Backbone：diffusion、autoregressive、JEPA、hybrid、LLM 或 VLM。
- Action coupling：action-conditioned rollout、joint generation、post-prediction action head。
- Deployment regime：open-loop rollout、chunked closed-loop、single-step closed-loop 或 interactive simulator。

## 实际解决的问题

这篇综述首先解决概念混乱。WAM 不是所有视频生成模型，不是所有 VLA，也不是所有 world model。只有当预测出来的未来真正参与动作生成、动作评估或动作路径训练时，它才是 WAM。

它也给机器人项目提供了一个实用选型工具。如果部署延迟最重要，Latent-Only 或 Video-Generation-Free 往往比完整渲染未来视频更现实。如果需要可解释规划，关键帧、flow、mask 或 affordance map 可能值得额外计算。如果是接触丰富的操作任务，触觉、力、proprioception 和运动学一致性通常比 photorealistic video 更重要。

## 综述证据

论文覆盖了大量近年 WAM 相关方法，应用范围包括机械臂操作、灵巧手、自动驾驶、空中操作、触觉交互和仿真评估。它用表格把代表性系统归入 Render-and-Decode、Latent-Only 和 Video-Generation-Free 三类。

这篇论文的证据主要是横向比较和分析，而不是新 benchmark。它的核心判断是：领域正在从“dream more”转向“act more”。很多强方法仍然保留未来预测训练信号，但在推理时减少或跳过完整未来视频生成。

文中反复出现的代表性例子包括：

- 早期 rendered-future 路线：UniPi、VLP、AVDC、GR-1、GR-2；
- latent shortcut 路线：VPP、Genie Envisioner、UWM、Fast-WAM、S-VAM；
- generation-free 路线：FLARE、PointWorld、PALM、DUST、ALAM、LDA-1B。

## 局限性

因为这是综述，论文没有做统一实证 benchmark。分类框架很有帮助，但真实系统可能跨多个 substrate，或者训练和推理阶段模式不同，所以具体归类仍可能有争议。

论文也指出当前评估还不成熟。视觉质量指标便宜，但和机器人任务成功率关联弱；闭环仿真更相关，但依赖仿真器或 learned model 的保真度；真实机器人评估最有效，但昂贵且难规模化。物理合理性、接触行为、长时记忆、延迟和峰值显存等指标还没有被稳定报告。

## 机器人实践影响

最强的实践结论是：选择能约束动作的最便宜未来表示。完整渲染未来视频并不总是闭环操作所需要的。对很多机器人项目，更合理的起点是训练时加入未来预测监督，部署时让直接策略消费紧凑特征、flow、mask、affordance map 或 proprioceptive/tactile prediction。

用于系统设计时，可以按这个清单判断：

- 明确目标泛化：新物体、新场景、新相机、新本体，还是新接触状态。
- 选择匹配的 substrate：像素适合语义先验，flow 适合物体运动，mask 适合任务几何，feature 适合大规模预训练，触觉和力适合接触。
- 按延迟选择 coupling：post-prediction head 更模块化，action-conditioned rollout 适合规划，joint generation 更强调未来和动作一致性。
- 评估时同时报告成功率、延迟、持续任务长度、显存和失败类型，而不是只报平均成功率。

## 应用到我的机器人

对我的机器人来说，这篇综述更适合作为架构决策指南，而不是复现某一个单独模型。一个务实的第一阶段实验是做 Latent-Only 或 Video-Generation-Free WAM：

- 采集同步相机观测、机器人状态、动作，以及可选的语言或任务标签；
- 加入未来 DINO/V-JEPA 类特征、object flow、mask 或 affordance map 的预测目标；
- 训练一个 action chunk decoder，让它消费紧凑未来表示；
- 部署时使用 chunked closed loop，每个动作块执行后用真实观测替换想象状态；
- 同时评估任务成功率、延迟、显存和接触相关失败。

传感器取决于任务。普通桌面操作至少需要 RGB-D 和 proprioception。插入、折叠、擦拭、灵巧手操作等接触丰富任务，最好把触觉或力矩传感加入 predictive substrate，而不是只作为后处理安全检查。

主要风险包括表示不匹配、训练中未来信息泄漏、推理太慢，以及 action decoder 无法把抽象未来转成可执行控制。更稳妥的路径是先做短时闭环任务，对比 action-only VLA 训练和带未来监督的 WAM 训练；只有当紧凑 substrate 不够用时，再考虑加入 rendered imagination。

## 实施建议

不要一开始复现大规模 rendered-video WAM。先做一个小型对比矩阵：

- baseline：直接行为克隆或 VLA-style policy；
- feature WAM：未来特征预测加 action head；
- geometry WAM：flow、mask 或 affordance 预测加 action head；
- 可选 rendered WAM：如果需要可解释规划，再加入 sparse keyframe prediction。

每个版本都报告同一组指标：成功率、策略频率、动作延迟、GPU 显存、扰动恢复能力，以及由接触、遮挡或视角变化导致的失败。这样才能把综述中的 taxonomy 变成可执行的工程测试。
