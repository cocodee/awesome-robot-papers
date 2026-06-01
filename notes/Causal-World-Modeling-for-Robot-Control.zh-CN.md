# Causal World Modeling for Robot Control

## 元数据

- 作者：Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, Yinghao Xu
- 来源：https://arxiv.org/pdf/2601.21998
- arXiv：2601.21998v2，2026-03-22
- 本地 PDF：[../papers/Causal-World-Modeling-for-Robot-Control.pdf](../papers/Causal-World-Modeling-for-Robot-Control.pdf)
- 转换 Markdown：[../papers/Causal-World-Modeling-for-Robot-Control.md](../papers/Causal-World-Modeling-for-Robot-Control.md)
- 网站：https://technology.robbyant.com/lingbot-va
- GitHub：https://github.com/robbyant/lingbot-va

## 研究问题

这篇论文研究如何把视频世界模型用于机器人闭环控制，同时避免开放环节漂移、长期记忆不足和视频生成延迟过高的问题。论文认为真实物理交互是因果和自回归的：当前状态只能依赖过去，机器人执行时也必须不断接收真实环境反馈。

## 核心方法

论文提出 LingBot-VA，一个自回归 diffusion video-action 框架。它把视频 latent token 和 action token 交错成一个因果序列，在每个自回归步骤中预测未来视觉 latent，并用 inverse dynamics 解码对应动作。

架构上，它使用 Mixture-of-Transformers：视频流由 Wan2.2-5B 初始化，动作流更窄更轻量。因果 attention 和 KV cache 用于保留长时序历史。Noisy History Augmentation 让动作解码器能从部分 denoise 的视频 latent 中预测动作，从而减少推理时的视频 denoise 开销。异步推理管线把当前动作执行和下一段视频-动作预测并行化，并用 forward dynamics grounding 避免模型依赖过期的想象画面。

## 关键创新

- 用因果自回归 video-action 建模替代双向 chunk 生成。
- 把视频和动作 token 交错到同一个序列，并用 KV cache 保留长期记忆。
- Noisy History Augmentation 允许从半去噪视觉 latent 中预测动作。
- 异步闭环执行在机器人运动时并行预测下一段动作。
- 重点解决长时序、精细操作、柔性物体和双臂操作任务。

## 实际解决的问题

LingBot-VA 解决了之前机器人世界模型策略的三个问题。第一，开放式未来视频生成不能及时吸收真实观测，容易漂移。第二，chunk 策略缺少完整历史记忆，长任务中容易忘记已经完成的步骤。第三，完整未来视频 denoise 太慢，不适合实时控制。

它通过因果建模、持久记忆和面向部署的异步执行，把视频世界模型从“离线想象未来”推进到更接近真实闭环控制。

## 实验证据

在 RoboTwin 2.0 上，LingBot-VA 在 50 个任务中达到 Easy 92.93%、Hard 91.55% 成功率，超过 X-VLA、pi0、pi0.5 和 Motus。长时序任务提升更明显，在 horizon 3 上相对第二名提升 Easy +8.2%、Hard +9.1%。

在 LIBERO 上，平均成功率为 98.5%，其中 LIBERO-Long 为 98.5%，LIBERO-Object 为 99.6%。

真实机器人实验包含六个任务：Make Breakfast、Pick Screws、Insert Tubes、Unpack Delivery、Fold Clothes 和 Fold Pants。论文报告在 success rate 和 progress score 上超过 pi0.5，并且只用 50 条示教进行适配，在困难任务上有超过 20% 的提升。少样本实验也显示，在 5、10、25、50 条示教下都优于 pi0.5。

## 局限性

LingBot-VA 仍依赖大型视频 diffusion backbone 和迭代 denoise，因此即使有部分 denoise 和异步执行，部署工程复杂度仍然较高。异步管线比直接 VLA 策略复杂，要求观测、动作执行和缓存更新的时序可靠。论文结果很强，但在硬件延迟、相机异常、安全关键接触失败等场景下，仍需要针对具体机器人验证。

## 应用到我的机器人

如果我的机器人要做长时序闭环操作，这篇论文非常相关，例如做饭、拆包、工具使用、插入、折叠柔性物体，或者需要记住已完成步骤的任务。

实际适配路线：

- 采集同步相机观测、机器人状态和动作；
- 训练或微调带因果历史输入的动作策略，而不是只看单帧；
- 部署时维护类似 KV cache 的历史记忆；
- 把未来状态预测作为内部规划信号；
- 如果推理延迟高，就把策略推理和动作执行并行化；
- 用真实观测校正预测未来，避免模型一直沿着错误想象滚动。

对我的机器人来说，最值得先尝试的不是完整视频生成，而是“因果记忆 + 反馈校正的未来预测”。可以先做一个小模型：用视觉 latent 预测短期未来，再让动作解码器根据历史和预测 latent 输出动作，测试它是否提升长任务成功率和扰动恢复能力。

## 实施建议

先做简化实验：在同一长时序数据集上比较普通 action-chunk policy 和 causal-history policy。指标看 success rate、progress score，以及受到扰动后的恢复能力。如果历史模型有效，再加入部分 future-latent prediction 和异步执行；不要一开始就复现完整 LingBot-VA。

## 问题分析

### LingBot-VA 是怎么实现训练或微调带因果历史输入的动作策略，而不是只看单帧？

LingBot-VA 不是把当前单帧 `o_t` 直接映射到动作 `a_t`，而是把历史观测和历史动作都作为因果上下文：

```text
a_t:t+K-1 ~ g(predicted future z_t+1:t+K, z_<=t, a_<t)
```

也就是：动作预测依赖过去视觉历史 `z_<=t`、过去动作历史 `a_<t`，以及预测出来的未来视觉 latent。

它的关键实现是把视频 latent 和动作 token 交错成一个时间序列：

```text
z0, a0,1, a0,2, ..., z1, a1,1, a1,2, ..., z2, ...
```

视频会降采样，动作频率更高，所以每个视频帧对应多个动作 token。这样模型训练时看到的是“过去发生了什么”和“机器人之前执行了什么”，而不是单张图像。

训练时使用 teacher forcing：输入真实历史 token，让模型预测后续 token。为了保证因果性，每个 token 只能通过 causal attention mask 访问时间上更早的 token，不能看到未来 token。因此它学习的是：

```text
next_token = f(all_past_video_tokens, all_past_action_tokens, language)
```

而不是普通 VLA 的：

```text
action = f(current_image, language)
```

训练目标包括两个 flow-matching loss：

- `Ldyn`：根据历史 `z_<=t, a_<t` 预测未来视觉 latent。
- `Linv`：根据历史、当前/未来视觉 latent，预测动作。

因此动作模型学到的是“什么动作会导致期望的视觉变化”，而不只是模仿当前图像对应的动作。

微调时也沿用同样的数据结构。新机器人数据需要组织成完整 episode：

```text
language instruction
image sequence: o0, o1, o2, ...
action sequence: a0, a1, a2, ...
```

然后转成交错序列：

```text
z0, a0, a1, ..., z1, a2, a3, ..., z2 ...
```

继续用 causal mask 训练模型预测后续视觉 latent 和动作。部署时，LingBot-VA 使用 KV cache 保存过去的观测和动作，每次加入新的真实观测和已执行动作，再预测下一段 future latent 和 action chunk。这就是它能做长时序记忆的原因，例如记住盘子擦了几次、盒子是否已经打开过。

对自己的机器人，最小可实现版本是：

1. 收集长时序 demonstration：图像、动作、任务文本。
2. 用视觉 encoder 把图像变成 `z_t`。
3. 把动作投影成 action token。
4. 拼成 video/action 交错序列。
5. 用 causal mask 训练 Transformer。
6. 同时预测 future latent 和 action。
7. 部署时缓存历史 token，而不是每步只看当前图像。

关键点：不是简单给 policy 多塞几帧图像，而是把历史观测和历史动作作为因果序列建模，并让动作预测依赖“过去发生了什么”和“预测接下来会发生什么”。
