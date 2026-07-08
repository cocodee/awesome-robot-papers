# Qwen-RobotWorld 技术报告：通过语言条件视频生成统一具身世界建模

## 元数据

- 作者：Qwen Team
- 会议/年份：arXiv，2026
- 来源：https://arxiv.org/pdf/2606.17030
- arXiv：2606.17030v3，2026-06-17
- 本地 PDF：[../papers/Qwen-RobotWorld-Technical-Report-Unifying-Embodied-World-Modeling-through-Language-Conditioned-Video-Generation.pdf](../papers/Qwen-RobotWorld-Technical-Report-Unifying-Embodied-World-Modeling-through-Language-Conditioned-Video-Generation.pdf)
- 本地 Markdown：[../papers/Qwen-RobotWorld-Technical-Report-Unifying-Embodied-World-Modeling-through-Language-Conditioned-Video-Generation.md](../papers/Qwen-RobotWorld-Technical-Report-Unifying-Embodied-World-Modeling-through-Language-Conditioned-Video-Generation.md)
- 项目页：https://qwen.ai/blog?id=qwen-robotworld

## 研究问题

论文要解决的问题是：如何构建一个统一的具身视频 world model，让它能在机器人操作、自动驾驶、室内导航和人到机器人迁移中，根据当前观测和动作条件预测未来视觉轨迹。核心假设是：自然语言可以作为统一动作接口，避免每类机器人都需要自己的 joint action、waypoint、steering command 或 navigation vector。

## 核心方法

Qwen-RobotWorld 是一个 language-conditioned video world model。输入当前观测和语言动作后，模型生成符合该动作意图的未来视觉轨迹。

系统由三部分组成：

- Double-Stream MMDiT with MLLM Action Encoding：60 层双流 diffusion transformer，通过每层 joint attention 把冻结 Qwen2.5-VL 的语义特征和 video VAE latent 结合起来。
- Embodied World Knowledge 数据集：约 8.6M video-text pairs，超过 200M 帧，覆盖机器人操作、自动驾驶、室内导航、人到机器人迁移和通用视频。
- General+Expert Progressive Curriculum：先用 T2I、T2V、TI2V 学通用视觉先验，再在 SFT 阶段逐步注入具身数据，同时保留一部分通用数据。

模型使用 Wan-VAE 表示视频 latent，冻结 Qwen2.5-VL 作为语言/动作编码器，并使用 20B 参数的 MMDiT 作为状态转移模型。它还使用非对称 3D RoPE 和多视角拼接训练来增强同步相机生成的一致性。

## 关键创新

关键创新不只是模型规模，而是把异构具身动作统一表示为自然语言。这样，机械臂视频、驾驶场景、导航轨迹和人类示范都可以变成同一种条件视频生成任务。

EWK 数据管线也很重要。它把 20+ 机器人本体和 500+ 动作类别映射到语言，加入 task-aware temporal segmentation，并使用五层视角感知标注：任务目标、动作细节、物理反馈、完整描述和简短描述。

最直接和机器人相关的是 Scene2Robot。它用 masked human demonstration、simulated robot reference trajectory 和 language action 作为条件，生成 photorealistic robot execution video。这使模型可以用于人类示范到机器人视频的迁移和合成数据生成。

## 实际解决的问题

Qwen-RobotWorld 主要面向三个实际问题：

- 具身数据稀缺：生成合成机器人视频，增强策略训练数据。
- 策略评估成本高：提供可扩展的视频 world model，作为虚拟环境或评估器。
- 规划信号不足：用语言条件未来视频作为下游机器人控制的视觉子目标或规划提示。

它也缓解了动作接口碎片化问题。现有具身 world model 往往需要场景专用控制量，例如机器人关节动作、驾驶 waypoint 或导航 heading。Qwen-RobotWorld 把这些统一成语言动作接口，更容易跨数据集、跨本体扩展。

## 实验证据

报告在四个主要 benchmark 上评估：

- EWMBench：总分 4.60，排名第一，高于 LVP 的 4.05；scene consistency 和 motion fidelity 表现突出。
- DreamGen Bench：总分 4.952，排名第一，覆盖 GR1 的环境、物体和行为泛化子集。
- PBench：总分 0.804，在论文比较中超过所有开源模型；domain understanding 为 0.857。
- WorldModelBench：总分 8.99，总体第三，仅低于闭源 Wan2.6 和 Veo3，在开源模型中第一。

论文还在 RoboTwin-IF 上做了 qualitative 和 zero-shot 分析。和 LVP、Cosmos2.5-14B 相比，Qwen-RobotWorld 在若干 Unitree G1 任务中展示出更好的指令对齐和多视角一致性。跨域示例包括人到机器人迁移、自动驾驶场景生成和室内导航生成。

## 局限性

这个系统本质上仍然是视频 world model，不是已经部署好的闭环机器人策略。它能预测视觉未来，但机器人仍然需要 action decoder、planner、controller 或数据生成管线，才能把生成的未来转成可执行控制。

系统规模很大：冻结 Qwen2.5-VL、Wan-VAE 和 20B MMDiT。没有蒸馏、缓存、稀疏调用或离线生成，很难直接放进机器人控制环路。

自然语言动作接口可扩展，但也有信息损失。语言可以描述意图和高层运动，但无法完整指定力、接触时序、关节限制、抓取稳定性和安全约束。对于接触丰富操作，语言条件视频更适合作为规划或数据生成信号，不能当作直接控制保证。

部分评估依赖视频指标或 VLM judge。这些指标适合筛选模型，但不能替代真实机器人成功率、接触失败分析和闭环恢复测试。

## 机器人实践影响

对机器人项目来说，Qwen-RobotWorld 更适合作为上游 world model 和数据引擎，而不是实时控制器。它的实际价值在于，在真实机器人数据昂贵时，用语言指令生成或评估候选未来。

适合的应用包括：

- 用语言条件未来视频增强机器人操作数据集；
- 为稀有物体、视角或本体组合生成合成 rollout；
- 把人类示范转换成机器人风格视频，再用于策略训练；
- 为下游 VLA、diffusion policy 或 MPC planner 生成视觉子目标；
- 通过生成合理的未来场景变化来压力测试策略。

最适合的任务是视觉进展容易判断的任务，例如抓取放置、倒水、折叠、交接、导航 waypoint 进展和多视角操作监控。最不适合的是高力接触、紧配合插入、滑移敏感灵巧操作，以及任何强依赖隐藏力觉和触觉状态的任务。

## 应用到我的机器人

对我的机器人，我不会把完整模型直接放进控制环。更合理的集成方式是离线或异步使用：

- 从当前相机观测生成语言条件未来视频或关键帧；
- 用几何、碰撞和任务成功检测过滤生成未来；
- 训练小模型模仿成功生成轨迹，或执行到生成视觉子目标；
- 运行时仍使用快速 VLA、diffusion policy 或 action-chunk controller；
- 只有在机器人不确定或需要长时规划时，才调用 world model。

需要的输入包括 RGB 或 RGB-D 观测、语言任务标签、机器人示范视频，最好还有多视角相机数据。做人到机器人迁移时，还需要仿真器或 retargeting pipeline，提供类似论文 Scene2Robot 的机器人参考运动。

预期收益是更好的数据覆盖、更强语言 grounding，以及更容易的跨本体迁移。主要风险是生成视频伪影、物理不可执行未来、生成视觉计划和真实机器人动力学不匹配，以及算力成本过高。

## 实施建议

最小复现不要从 20B 模型开始。可以先做小规模实验：

- 收集短机器人视频，并配简短动作 caption；
- 微调一个较小的 first-frame + language conditioned 图像/视频续写模型；
- 只生成短时未来关键帧，而不是长视频；
- 用 inverse dynamics model 或 goal-conditioned policy 执行到生成未来；
- 比较有无合成未来数据时的策略训练效果。

最重要的验证不是视频好不好看，而是生成数据是否提升真实或仿真任务成功率，是否保持物体身份和接触顺序，以及下游控制器在生成未来略有错误时能否恢复。
