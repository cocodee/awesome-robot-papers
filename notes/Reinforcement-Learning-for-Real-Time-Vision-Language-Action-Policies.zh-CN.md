# Real-Time EXPO-FT 精讲教程：面向实时机器人的 VLA 强化学习微调

> 论文：Perry Dong, Kuo-Han Hung, Dorsa Sadigh, Chelsea Finn, “Reinforcement Learning for Real-Time Vision-Language-Action Policies”，arXiv:2609.18207v1，2026-09-16。\
> 原文：[arXiv 摘要页](https://arxiv.org/abs/2609.18207)，[PDF](../papers/Reinforcement-Learning-for-Real-Time-Vision-Language-Action-Policies.pdf)，[正文提取稿](../papers/Reinforcement-Learning-for-Real-Time-Vision-Language-Action-Policies.md)。

这篇论文提出 Real-Time EXPO-FT：大型 VLA 异步地产生候选 action chunk，小型 Edit Policy 在执行前用最新观测做快速修正，Critic 再从原始/修正候选中选出价值最高的 chunk。它解决的核心不是“如何把 VLA 每次推理做得更快”，而是“在 VLA 很慢且环境继续运动时，如何仍然进行有效的 RL 微调和实时控制”。

## 1. 课程导入

### 1.1 论文研究背景

VLA 把图像、语言和机器人动作统一在一个生成策略中，擅长利用大规模预训练得到的行为先验。但模型越大，视觉编码、语言条件和 flow/diffusion action 生成越慢。机器人却以固定控制频率运行，环境不会等待神经网络完成推理。于是，模型看到的是旧状态，真正执行动作时状态已经改变。

论文关注的是在已有 VLA/SFT 能力之上进行少量在线 RL 微调，使系统在动态、随机、对时间敏感的任务上可靠工作。实验不是从零训练 VLA，而是从预训练/监督微调策略出发。

### 1.2 这篇论文试图解决什么问题

若 VLA 在 (s_t) 开始推理，经过 (d) 个控制步才输出动作，那么该动作实际要在 (s_{t+d}) 执行。朴素系统执行的是

\[
a_{t+d}=\pi_{VLA}(s_t),
\]

而不是理想的 \(\pi(s_{t+d})\)。在动态任务中，这会造成观测—动作分布错位、抓取时机错过、平衡误差累积和 RL credit assignment 偏差。

### 1.3 为什么 VLA 的推理延迟会影响机器人控制

控制频率 30 Hz 时，一个控制步约 33 ms。论文真实机器人 VLA 推理约 67 ms；在三个任务中又人为加入 100 ms，合计约 167 ms，对应约 5 个控制步。167 ms 内，物体、机械臂、球或防守者都可能显著移动。延迟不是简单的“动作晚一点”，而是使动作基于错误的状态生成。

### 1.4 本课程的核心学习目标

- 分清 action chunk、推理延迟、实时执行和状态滞后的关系。
- 理解 EXPO-FT 的 base VLA + bounded edit + Q-function 结构。
- 理解 RTC 只保证连续执行，Real-Time EXPO-FT 进一步补偿延迟期间的状态变化。
- 能把该架构映射到动态抓取、双臂协作和移动机器人系统。

## 2. 从实时控制问题开始理解论文

### 2.1 机器人控制频率与 VLA 推理速度的矛盾

设控制频率为 (f) Hz，VLA 推理耗时为 (T) 秒，则离散延迟近似为

\[
d=\lfloor Tf\rfloor+1.
\]

VLA 通常一次预测长度为 (H) 的动作块，每轮执行 (C\le H) 步。论文假设 (1\le d\le C)：推理延迟不超过一轮 chunk 的执行长度。系统需要在当前 chunk 尚未结束时就启动下一次 VLA 推理。

### 2.2 状态滞后：为什么动作生成完成时世界已经变了

动态抓取中，VLA 看到目标位于 50 cm 处并开始生成动作；等动作完成时目标已到 55 cm。如果仍执行未修改的接近轨迹，末端会落后 5 cm。更糟的是，chunk 中后半段动作也会建立在错误的速度、姿态和接触时机上。

### 2.3 静态任务与动态任务的本质区别

静态任务中，(s_t\approx s_{t+d})，延迟主要降低效率。动态任务中，状态转移量 \(\|s_{t+d}-s_t\|\) 与任务容错范围同量级，延迟直接降低成功率。平衡、接球、动态抓取和踢球都要求“在正确的时间采取正确的动作”。

### 2.4 State-Action Temporal Mismatch

State-Action Temporal Mismatch 指动作由旧状态生成，却在新状态执行。标准 MDP 里通常假设 \(a_t\sim\pi(\cdot|s_t)\)；存在延迟时，实际是 \(a_t\sim\pi(\cdot|s_{t-d})\)。只把延迟当成实现细节，会让 critic 把收益错误归因给旧状态，破坏 Markov 性和 credit assignment。Real-Time EXPO-FT 让最终执行的 edit policy 显式条件于最新状态，从而使“修正后策略”重新接近当前状态上的 Markov 决策。

## 3. EXPO-FT 基础方法

### 3.1 EXPO-FT 的总体框架

EXPO 使用两个策略：表达能力强但昂贵的 base flow policy，以及小而快的 edit policy。EXPO-FT 把它用于预训练 VLA 的 RL 微调。VLA 给出接近专家分布的动作，edit policy 学习把动作推向高 Q 值区域。

### 3.2 Base VLA：生成候选动作

给定状态和动作噪声 \(\epsilon_i\)，VLA 产生多个候选 chunk：

\[
a^i_{t:t+H}=\pi_{VLA}(s_t,a^{prev}_{t:t+d},\epsilon_i).
\]

RTC prefix 中前 (d) 步是推理窗口内已经承诺执行的动作，因此真正保留的是 \(a^i_{t+d:t+d+C}\)。多噪声采样提供行为多样性，但每个候选都可能带有旧观测造成的误差。

### 3.3 Edit Policy：对 VLA 动作进行局部修正

Edit Policy 输入状态和 base action，输出有界残差：

\[
\hat a\sim\pi_{edit}(\cdot|s,a),\qquad \tilde a=a+\hat a.
\]

它不是重新规划整段行为，而是利用小网络快速把已有 chunk 推向更可靠的局部动作。Real-Time EXPO-FT 中，(s) 使用动作真正要执行前的最新观测 (s_{t+d})。

### 3.4 Critic / Q-function：评价并选择动作

Critic 估计 chunk 在状态下的价值。候选集合包含原始动作和修正动作，执行最高价值者：

\[
\tilde a^*=\arg\max_{a\in\{a_i,\tilde a_i\}}Q_\phi(s,a).
\]

论文采用 chunk-level Q，而非单步 Q；真实机器人部分使用轻量 ResNet-50 风格视觉编码器、proprioception 和展平后的动作块。

### 3.5 为什么要限制 Edit Policy 的修正幅度

论文把 \(\hat a\) 限制在 \([ -\beta,\beta]\)（实现中为 tanh 输出乘 task-specific edit scale）。限制有三层作用：保留 VLA 的行为先验、避免 critic 梯度反向推动大型 VLA 脱离已学分布、降低 edit policy 产生灾难性动作的风险。它表达的是“在 base action 附近做可靠改进”，不是“从零替换 base policy”。

### 3.6 EXPO-FT 的强化学习思想

Edit policy 通过最大化编辑后动作的 Q 值训练，同时保留熵正则；critic 通过 TD 学习。训练/执行时可用 on-the-fly policy 在原始与修正动作中选高值者。这样 RL 主要承担可靠性提升，VLA 继续承担复杂任务行为生成。

## 4. EXPO-FT 在实时动态场景中的局限

### 4.1 EXPO-FT 隐含的时间同步假设

普通 EXPO-FT 的关键计算容易写成“在状态 (s_t) 生成动作，再在同一时刻评价/执行”。大型 VLA 的现实延迟破坏了这个假设：候选动作生成时看到的是旧图像，编辑与评价若仍使用旧状态，整个 RL 闭环仍然是滞后的。

### 4.2 VLA 推理延迟带来的旧观测问题

延迟期间机器人继续执行已排队 chunk。状态从 (s_t) 变到 (s_{t+d})，但候选 action 仍由 (s_t) 产生。RTC 的 prefix conditioning 能让新 chunk 接上旧 chunk，却不会自动知道目标在延迟窗口内移动了多少。

### 4.3 为什么“修正旧动作”仍然可能失败

若 edit policy 也接收 (s_t)，它只能修正“当时看来合理”的动作；目标已经偏移时，修正方向本身就是错的。解决方式不是让旧状态下的修正更激进，而是把修正时刻推迟到动作执行前，并输入 (s_{t+d})。

### 4.4 动态抓取示例：目标从 50 cm 移动到 55 cm

VLA 在 50 cm 生成朝向 50 cm 的 chunk；推理期间目标到 55 cm。Real-Time EXPO-FT 保留该 chunk 作为 proposal，在最新观测中由 edit policy 学习一个约 5 cm 的末端位置/速度补偿，再由 critic 判断“原始 chunk”还是“补偿 chunk”更可能成功。补偿范围有限时仍可能失败，因此基础 VLA 必须先具备基本抓取能力。

## 5. Real-Time EXPO-FT 的核心思想

### 5.1 从 EXPO-FT 到 Real-Time EXPO-FT

改动可以概括为：让 VLA 负责慢而有表达力的候选生成，让 edit policy 负责快而依赖最新状态的反应控制，让 critic 在最新状态下重新选择。论文称其为两个时间尺度的解耦。

### 5.2 Slow Asynchronous Generation

当当前 action queue 还剩 (d) 步时，后台启动 VLA。它基于当时状态和 RTC prefix 采样 (N) 个候选，推理期间机器人不停止。候选生成可以慢，因为它不在关键的同步执行路径上。

### 5.3 Fast Synchronous Editing

到达新 chunk 切换点时，读取最新 (s_{t+d})，用轻量 edit policy 对所有保留候选做修正。这个路径只需小网络前向和 critic 评估，目标是足够快地跟上固定控制频率。

### 5.4 Proposal from Old State + Correction from Current State

这是全文最重要的工程抽象：

\[
\underbrace{a^i=\pi_{VLA}(s_t,\epsilon_i)}_{\text{旧状态下的强先验}}
\quad\rightarrow\quad
\underbrace{\tilde a^i=a^i+\pi_{edit}(s_{t+d},a^i)}_{\text{最新状态下的快速反应}}.
\]

旧状态并不等于无用状态：它提供完整的任务意图和长时行为结构；最新状态则负责弥补延迟造成的局部变化。

### 5.5 为什么不需要让大型 VLA 本身达到高频控制速度

大型模型只需在流水线启动时生成下一批候选，昂贵计算与执行并行。高频反应交给小网络。这样既保留 VLA 的多任务泛化和动作先验，也避免在有限硬件上强行把全部视觉—语言—动作推理压缩到每个控制周期。

## 6. Real-Time EXPO-FT 的时间轴

### 6.1 VLA 在 (s_t) 时刻开始推理

当前 chunk 还剩 (d) 步时，系统记录 (s_t)，将已承诺 prefix 输入 VLA，异步采样多个候选。

### 6.2 推理期间机器人继续执行动作

机器人执行 queue 中的 prefix；控制线程不能阻塞等待 VLA。这保证动作流连续，也避免因推理停顿造成轨迹断裂。

### 6.3 状态从 (s_t) 演化到 (s_{t+d})

机器人和环境经过 (d) 个动作后产生新图像和本体状态。目标位姿、速度、接触关系和可见性都可能变化。

### 6.4 Edit Policy 使用最新状态 (s_{t+d})

对每个候选的剩余执行段计算 \(\hat a^i_{t+d:t+d+C}\sim\pi_{edit}(\cdot|s_{t+d},a^i)\)。注意它编辑的是将要执行的剩余 chunk，不是已执行 prefix。

### 6.5 Critic 在最新状态下重新评价动作

计算 (Q_\phi(s_{t+d},a^i)) 与 (Q_\phi(s_{t+d},\tilde a^i))，保留最高价值动作。这一步让动作选择也对齐最新状态，而不是只让 edit policy 对齐。

### 6.6 新 Action Chunk 的执行

执行选出的 (C) 步，再在接近队列尾部时启动下一轮 VLA。整个系统像流水线：生成、编辑、评价、执行持续重叠。

## 7. RTC：为什么机器人不能停下来等 VLA

### 7.1 什么是 Real-Time Chunking

RTC 是一种异步 action chunking 方法：当前 chunk 执行时，后台预测下一个 chunk；切换时直接接上，不让机器人因等待推理而停顿。

### 7.2 Committed Action Prefix

推理窗口内必然会执行旧 chunk 的一段动作，这段已承诺动作就是 prefix。新策略不能重新改写它，只能把它作为条件，生成 prefix 之后的 postfix。

### 7.3 Action Prefix Conditioning

训练时把 ground-truth chunk 划为 (d) 步 prefix 和剩余 postfix；prefix 使用干净动作、flow timestep 设为 1，仅对 postfix 计算 flow-matching loss。部署时同理把在途动作 inpaint 到新 chunk 的前端。

### 7.4 VLA 如何预测已提交动作之后的未来动作

形式上：

\[
a_{t+d:t+d+H}\sim\pi(\cdot|s_t,a^{prev}_{t:t+d}).
\]

它学习的是“给定已经会执行的动作，如何产生连贯的后续”。因此不会发生动作 chunk 的硬切换或明显不连续。

### 7.5 RTC 解决的是“执行连续性”，而不是“观测过时”

RTC 能消除等待造成的停顿，但如果整个新 chunk 仍由旧观测决定，目标快速移动时仍会失败。Real-Time EXPO-FT 的新增点正是：最新状态下的 edit + critic。

## 8. EXPO-FT、EXPO-FT + RTC 与 Real-Time EXPO-FT

### 8.1 三种方法的演化关系

```text
EXPO-FT                 : RL 编辑提升动作质量
EXPO-FT + RTC           : 再用 prefix conditioning 消除等待停顿
Real-Time EXPO-FT       : 再把最新状态用于编辑和选择，补偿延迟期间变化
```

### 8.2 EXPO-FT：提升动作质量

它学习 bounded residual，让 VLA 动作向高价值区域移动；适合已有任务能力、但需要可靠性提升的场景。

### 8.3 EXPO-FT + RTC：消除等待推理造成的停顿

RTC 使策略能在固定频率持续输出，但 base VLA 和编辑逻辑仍可能面对 stale observation。

### 8.4 Real-Time EXPO-FT：补偿推理期间的环境变化

它把快速编辑和 Q 选择放到 (s_{t+d}) 下；论文实验显示，即使 base flow policy 仍有 4/5 步延迟，整体性能也能超过零延迟的轻量 RLPD 基线。

### 8.5 三种方法的结构与能力对比

| 方法              | 大型 VLA      | 连续执行 | 最新状态修正      | 主要解决的问题   |
| ----------------- | ------------- | -------- | ----------------- | ---------------- |
| EXPO-FT           | 同步候选/编辑 | 否或有限 | 不充分            | 动作质量、可靠性 |
| EXPO-FT + RTC     | 异步并行      | 是       | 主要仍是旧状态    | 等待停顿         |
| Real-Time EXPO-FT | 异步候选      | 是       | 是，edit + critic | 停顿与状态滞后   |

## 9. Edit Policy 深入解析

### 9.1 Edit Policy 的输入与输出

输入是最新视觉/本体状态和 base action chunk；输出是与动作块同维度的有界残差。真实实验中 action chunk 为 (C\times7)（末端位置、姿态、夹爪等 7 维），(C=8) 时 edit 输出维度为 56。

### 9.2 动作修正公式

\[
\hat a_{t+d:t+d+C}\sim\pi_{edit}(\cdot|s_{t+d},a_{t+d:t+d+C}),
\quad
\tilde a=a+\hat a.
\]

### 9.3 RL Action Refinement

EXPO-FT 的原始目标是让 edit 后动作获得更高 Q：

\[
\mathcal L_{edit}=-\mathbb E[Q_\phi(s,a+\hat a)-\alpha\log\pi_{edit}(\hat a|s,a)].
\]

它通过 reward/critic 学到“哪些局部偏移有益”，而不是依赖人工写出每个目标速度或抓取提前量。

### 9.4 Latency Compensation

在论文方法中，latency compensation 并不是显式预测一个 5 cm 位移，而是让 edit policy 从最新观测中学习这种补偿。环境运动规律、视觉变化和任务成功反馈共同塑造残差。

### 9.5 为什么 Edit Policy 不是用来取代 VLA

单独用小策略需要大量数据覆盖任务和初始状态，也缺乏 VLA 的多步行为先验。Edit policy 的局部有界结构限制它承担的责任：VLA 负责“做什么和大致怎么做”，edit 负责“现在需要怎样微调”。

### 9.6 “最新观测”究竟指哪个时刻的观测

不是 VLA 启动时的 (s_t)，而是候选动作即将接管执行时的 (s_{t+d})。如果系统有图像采集、传输和预处理额外延迟，应将时间戳和有效状态延迟纳入工程定义；论文公式中的最新状态是算法语义，不等于传感器绝对零延迟。

## 10. Edit Policy 是否每个控制周期都执行

### 10.1 论文中的 Chunk-Level Editing

论文明确以 chunk 为基本决策单元。VLA 候选的剩余 (C) 步在切换点被 edit 一次，随后执行这一段；不是对每个图像帧都重新编辑。

### 10.2 动作块切换时的反馈修正

每轮切换时重新读取状态、编辑候选并由 critic 选择。这样编辑频率约为 chunk 频率，控制器仍可在 30 Hz 发送动作，但 edit 不一定 30 次/秒。

### 10.3 与每帧视觉闭环控制的区别

每帧闭环需要高频视觉编码、动作重规划和稳定的时间同步；论文则把高频执行和较低频决策分开，以获得更低计算成本和更平滑的 chunk。

### 10.4 如果每帧都运行 Edit Policy 会发生什么

可能提高反应速度，但也可能产生动作抖动、残差叠加、critic 误差放大、动作块内部不一致和训练分布改变。特别是 56 维 chunk 每帧都被重写，会使原有动作先验难以保持。

### 10.5 Learned MPC / Receding-Horizon 扩展方案

可以把 edit policy 看作学习型局部 MPC：每个短周期读取最新状态，生成一段有界修正，仅执行前若干步，再滚动更新。若采用该扩展，应重新设计 overlap、一致性损失、速度/加速度约束和 critic 的时间尺度。

### 10.6 高频修正带来的动作抖动与训练问题

需要加入残差平滑、动作变化率惩罚、末端速度/加速度限制和安全层；训练数据也要包含连续修正后的真实执行轨迹，否则 off-policy critic 会高估频繁 edit 的收益。

## 11. Critic 与 Chunk-Level 强化学习

### 11.1 为什么不能只评价单步动作

抓取是否成功、球是否保持在盘中心、是否踢进球门，都取决于连续动作的时序效果。单步动作可能暂时偏离目标，但对后续轨迹有益；chunk-level Q 能评价整段动作的结果。

### 11.2 Action Chunk 级 Q-function

把一段 (C) 步动作视为宏动作：

\[
Q_\phi(s_t,a_{t:t+C}).
\]

它接收当前视觉、本体状态和展平后的 action chunk，输出一个价值。

### 11.3 Chunk-Level Temporal-Difference Backup

论文使用跨越完整执行窗口的 TD：

\[
\mathcal L_Q=\mathbb E[(r_t+\gamma Q'_{\phi}(s_{t+C},\tilde a^*_{t+C:t+2C})-Q_\phi(s_t,a_{t:t+C}))^2].
\]

### 11.4 从 (s_t) 到 (s_{t+C}) 的价值传播

当前 chunk 执行完才到 (s_{t+C})，下一个 chunk 的最佳原始/编辑候选作为 bootstrap。这样价值会传播到“这一段动作是否把系统带入更好状态”，比单步 reward 更贴近实际任务成功。

### 11.5 Critic 如何比较原始动作和 Edited Action

对每个候选同时评估 (Q(s,a)) 和 (Q(s,a+\hat a))，不强制 edit 必须生效；如果最新状态表明 base action 已经足够好，critic 可以选择不编辑的原始候选。这是安全的保守机制。

## 12. Real-Time EXPO-FT 完整执行流程

1. 执行当前 action chunk。
2. 当队列剩余 (d) 步时异步启动大型 VLA。
3. 机器人持续运动，不等待 VLA。
4. VLA 生成 (N) 个候选 chunk，并利用 RTC prefix 保证衔接。
5. 到达切换点，获取最新观测 (s_{t+d})。
6. Edit Policy 对每个候选的剩余段做有界修正。
7. Critic 在最新状态下比较原始和修正候选。
8. 执行最优 chunk，进入下一轮流水线。

训练时还有三条线：VLA 用带随机延迟的 training-time RTC 行为克隆损失微调；edit policy 最大化 Q；critic 用 chunk-level TD 更新。可选的 noise-level Q filter 先在噪声空间筛掉候选，再只解码一个候选，以降低 Bellman backup 计算量。

## 13. 论文实验设计

### 13.1 仿真实验设置

Kinetix 10 个动态环境：Car Launch、Cartpole Thrust、Catapult、Catcher、H17 Unicycle、Hard Lunar Lander、Half-Cheetah、Trampoline、Chain Lander、Grasp。预训练 flow policy 使用 (H=8)，RL 在线训练 100k environment steps，延迟 4 步。

### 13.2 真实机器人实验平台

单臂 DROID setup，30 Hz，侧视和腕视两路 224×224 RGB，输入末端位置/姿态本体状态，控制为空间笛卡尔和夹爪速度。VLA 约 67 ms；Ball Balancing、Object Passing、Soccer Kicking 加 100 ms，总延迟约 167 ms、(d=5)；Dynamic Picking 使用约 67 ms、(d=3)。

### 13.3 Dynamic Picking

物体放在旋转盘上，目标速度和轨迹变化，机器人必须快速接近并抓住。增加延迟会直接导致闭合时机错过，是验证 stale observation 的代表任务。

### 13.4 Ball Balancing

控制盘子让乒乓球持续位于中心。任务连续、随机、对小误差敏感，尤其考验最新观测下的平滑快速反应。

### 13.5 Object Passing

另一机械臂随机运动并传来物体，接收臂要预测并跟随物体位置。随机性使离线动作先验不足，要求实时根据对方运动修正。

### 13.6 Soccer Kicking

将球踢入小球门，同时避开移动防守者。策略必须同时决定踢的位置和时刻，是空间精度与时间精度的结合。

### 13.7 为什么这些任务适合验证实时控制能力

四个任务分别覆盖抓取、连续平衡、随机交互和时机决策；它们共同具有快速状态变化、随机未来和紧时间窗口，能把“无停顿”和“无 stale observation”区分开。

## 14. 实验结果如何解读

### 14.1 SFT 的表现

四个真实任务分别为 19/30、8/30、10/30、13/30，平均 12.5/30（约 42%）。说明监督学习策略具备先验，但不足以应对动态分布。

### 14.2 SFT + RTC 的提升

平均 18/30。连续执行消除了等待造成的停顿，但性能仍受 stale observation 限制。

### 14.3 EXPO-FT 的表现

平均 18.8/30；RL 能改善任务可靠性，但没有 RTC 时高频执行会出现 chunk 间暂停。

### 14.4 EXPO-FT + RTC 的意义

平均 25/30。它同时改善了动作质量和执行连续性，但面对更快环境仍可能退化，因为候选与修正的状态时刻仍不充分对齐。

### 14.5 Real-Time EXPO-FT 的最终提升

Dynamic Picking 30/30，Ball Balancing 28/30，Object Passing 30/30，Soccer Kicking 28/30，平均 29/30（97%）。仿真延迟设置下平均 96.2%，超过零延迟 RLPD 的 81.4%。

### 14.6 为什么结果说明“只解决异步执行还不够”

RTC 主要保证机器人不停；Real-Time EXPO-FT 还要在切换时读取最新状态、执行快速 edit 并让 critic 重新选择。延迟/速度实验中，Real-Time EXPO-FT 对延迟和目标速度更稳定，而 RTC 和普通 EXPO-FT 更明显下降。

## 15. 为什么少量在线 RL 数据也能有效

### 15.1 预训练 VLA 提供的行为先验

VLA 已经知道视觉语义、动作格式和基本任务步骤，RL 不需要探索整个动作空间。

### 15.2 SFT 提供初始任务能力

论文先收集专家演示或脚本演示，做监督微调，直到具备基础成功率，再进入在线 RL。真实实验不是随机策略冷启动。

### 15.3 Online RL 负责局部适应与优化

在线数据主要揭示动态速度、接触时机、延迟补偿和随机扰动下的失败模式，edit policy 用这些反馈学习局部改正。

### 15.4 为什么“10 分钟训练”不能理解为从零训练 VLA

10 分钟是每个任务的在线机器人交互上限，不包括预训练、已有模型和演示数据。正确理解是“少量真实数据做后训练适配”。

### 15.5 少量真实数据适配的真正意义

把高成本的真实交互集中用于解决仿真/演示无法准确覆盖的延迟、摩擦、传感器噪声、目标速度和机器人动力学差异。

## 16. 与经典机器人控制架构的关系

### 16.1 高层规划器、局部控制器与底层伺服

VLA 类似高层语义/行为规划器；Edit Policy 类似学习型局部规划器或残差控制器；Cartesian controller、IK 和 joint servo 负责确定性执行与安全约束。

### 16.2 Large Slow Model + Small Fast Controller

论文把“大模型慢但懂任务”和“小模型快但只做局部反应”组合起来。这是现代机器人很实用的系统分工。

### 16.3 多时间尺度控制架构

示意划分：VLA 以 chunk/几十到几百毫秒运行；edit/critic 在 chunk 切换点运行；笛卡尔速度控制以 30 Hz 或更高运行；关节伺服/力矩环在更高频率运行。

### 16.4 VLA、Edit Policy、Cartesian Controller 和 Joint Servo 的频率划分

VLA 负责目标与动作序列，edit 负责延迟补偿，Cartesian controller 负责速度/轨迹跟踪，IK/servo 负责可执行性、关节限位和电机级稳定。不能让 RL 直接绕过底层安全约束。

### 16.5 Real-Time EXPO-FT 与 MPC 的联系和区别

共同点是滚动时域、使用当前状态、只执行短期动作并重新规划。区别是 Real-Time EXPO-FT 的候选由生成式 VLA 给出、局部修正由学习策略完成，critic 是 learned value；经典 MPC 通常依赖显式动力学模型和在线优化。它可以被视为一种 learned proposal + learned local selection 的 MPC-like 架构。

## 17. 面向双臂移动机器人的扩展

### 17.1 双臂动作空间建模

将两臂末端位姿、速度、夹爪和底盘速度拼成联合动作；应明确左右臂坐标系、时间戳和 chunk 内同步约束。

### 17.2 左右臂联合 Action Chunk

联合 chunk 使两臂能共享同一时间基准，但动作维度变高、critic 学习更难。可先采用共享视觉编码器、双臂分支，再用协同头预测相对动作。

### 17.3 双臂 Edit Policy

Edit policy 输出左右臂残差，并加入相对距离、相对姿态、闭链和碰撞特征。残差最好分组限幅，避免一只臂的修正破坏另一只臂的协作。

### 17.4 相对位姿与协同抓取约束

除世界坐标误差外，应显式关注两末端相对位姿、物体两接触点、夹持力和同步到达时间。critic 可输入这些几何量，reward 同时包含成功、碰撞和约束违背信号。

### 17.5 底盘、双臂和夹爪联合控制

建议让 VLA 生成全身 coarse chunk，edit policy 先在任务空间补偿；底盘速度与双臂动作需要共享速度/加速度预算，否则局部修正可能使底盘或某一臂不可达。

### 17.6 Safety Layer、IK 与轨迹控制器

最终动作必须经过碰撞检测、关节限位、速度/加速度限幅、IK 可行性检查和 emergency stop。RL 只应输出受约束的参考动作，不能替代安全控制器。

## 18. 动态轮胎抓取案例分析

### 18.1 传送带动态目标场景

轮胎在传送带上移动，目标不仅平移，还可能滚动、遮挡或发生姿态变化。双臂移动机器人还要处理底盘相对目标的运动。

### 18.2 VLA 的低频粗规划

VLA 根据任务语言、全局视觉和物体语义提出“靠近—对准—双臂包络—闭合—抬升”的候选 chunk，并利用 RTC 保证在途动作连续。

### 18.3 Edit Policy 的实时位置与姿态补偿

最新观测输入应包含轮胎中心、法向/滚转姿态、速度估计和两末端状态。Edit Policy 学习对 approach 点、夹爪方向、闭合时刻和底盘速度做小幅修正。

### 18.4 双臂抓取时机修正

若左臂已接近而右臂滞后，修正应保持相对抓取几何，不是独立追踪目标中心。critic 评价整段双臂 chunk 是否在同步窗口内形成稳定夹持。

### 18.5 目标速度、位姿和视觉状态的输入设计

视觉输入提供目标检测/分割、姿态和遮挡信息；本体输入提供两臂与底盘状态；可选的 tracking filter 提供速度。要记录测量时间戳，并将传感器延迟作为训练随机化变量。

### 18.6 从 Real-Time EXPO-FT 到工业动态抓取系统

工程流水线可以是：VLA 生成候选 → 最新状态 edit → critic 选择 → IK/碰撞/力控安全层 → 30–100 Hz 轨迹控制。部署前应验证不同带速、照明、负载、轮胎姿态和网络延迟，而不是只测试平均速度。

## 19. 方法局限与开放问题

### 19.1 单臂实验向双臂系统扩展的难点

论文真实实验是单臂 DROID setup；双臂会引入更高维动作、更强耦合、碰撞和闭链约束，不能直接把 7 维 action 替换为 14 维就认为问题解决。

### 19.2 Chunk-Level Editing 的反馈频率限制

论文编辑发生在 chunk 切换点，不是每帧视觉闭环；极高速目标可能在 chunk 内仍发生不可补偿的变化。

### 19.3 Reward Design 问题

论文使用任务级稀疏二值成功检测，需为每个任务设计 detector。工业系统可能需要安全、抓取质量、能耗和时间等多目标 reward，reward 错误会直接误导 critic。

### 19.4 基础 VLA 初始能力不足时的困难

有界 edit 不能从错误行为中凭空创造完整技能；若 VLA 不会抓取、姿态理解错误或动作空间不匹配，应先改进演示、SFT 或任务接口。

### 19.5 安全控制不能完全依赖强化学习

Q 值是估计，不是安全证明。碰撞、夹伤、超速、通信丢包和传感器失效必须由确定性 safety layer、监控器和急停处理。

### 19.6 高频 Edit Policy 是否值得进一步研究

值得研究，但应同时解决 chunk 内一致性、残差平滑、critic 过估计、计算预算、实时调度和训练—部署频率差异。一个可能方向是带动作变化率约束的 learned MPC。

## 20. 课程总结

### 20.1 EXPO-FT 的核心思想

保留大型 VLA 的动作先验，用小型 bounded edit policy 在 Q 值指导下做局部 RL refinement。

### 20.2 Real-Time EXPO-FT 的核心改进

把慢的 VLA 候选生成放到异步后台，把最新状态下的快速编辑和 critic 选择放到同步执行路径，显式处理 inference latency。

### 20.3 RTC、Edit Policy 与 Critic 的职责分工

RTC 负责“不断流、接得上”；Edit Policy 负责“根据最新状态改多少”；Critic 负责“原始和修正候选哪个更值得执行”；VLA 负责“提供复杂行为候选”。

### 20.4 论文最值得记住的系统架构

```text
旧状态 s_t ──慢 VLA──> 多个候选 action chunks
                                  │
最新状态 s_(t+d) ──快 Edit───────┤
                                  ▼
                         Critic 选择最高价值 chunk
                                  │
                             安全/控制层执行
```

### 20.5 对真实机器人 VLA 系统的工程启示

不要把实时性简化为“让大模型每帧跑完”。更稳妥的系统是多时间尺度流水线：大模型提供语义和行为先验，小模型补偿最新状态，价值模型选择，传统控制器保证可执行性与安全。论文的 10 分钟结果说明这种架构能高效利用少量真实数据，但也提醒我们：高成功率依赖良好的基础策略、可靠的 reward detector、合理的延迟建模和完整的安全层。

## 参考与核对

- Dong et al., _Reinforcement Learning for Real-Time Vision-Language-Action Policies_, arXiv:2609.18207v1, 2026。
- 关键公式：论文 Eq. (4)–(11)，分别对应异步候选、最新状态编辑、chunk-level critic、noise-space filtering 和训练目标。
- 论文真实任务结果：SFT 12.5/30，SFT+RTC 18/30，EXPO-FT 18.8/30，EXPO-FT+RTC 25/30，Real-Time EXPO-FT 29/30。
