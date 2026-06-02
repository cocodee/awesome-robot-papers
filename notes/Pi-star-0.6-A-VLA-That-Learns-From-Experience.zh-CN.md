# Pi-star-0.6: A VLA That Learns From Experience

## 元数据

- 标题：$\pi^{*}_{0.6}$: a VLA That Learns From Experience
- 作者：Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachy Groom, Hunter Hancock, Karol Hausman, Gashon Hussein, Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim Jones, Ben Katz, Liyiming Ke, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow, James Tanner, Marcel Torne, Quan Vuong, Anna Walling, Haohuan Wang, Blake Williams, Sukwon Yoo, Lili Yu, Ury Zhilinsky, Zhiyuan Zhou
- 会议/年份：arXiv, 2025
- arXiv：2511.14759v2，2025-11-19
- 来源：https://arxiv.org/pdf/2511.14759
- 项目页：https://pi.website/blog/pistar06
- 本地 PDF：[../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.pdf](../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.pdf)
- 转换 Markdown：[../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.md](../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.md)

## 研究问题

这篇论文研究大型 vision-language-action 模型如何在真实部署之后继续变强，而不是停留在“模仿示教”的水平。目标任务都是长时序、真实、难以密集打分的机器人操作，例如叠不同衣物、组装纸箱、用专业咖啡机制作 espresso。

核心问题不是普通泛化，而是：如何把真实机器人执行经验、稀疏成功/失败标签，以及少量人工接管修正，稳定地转化成适合大 VLA 和连续动作 flow-matching head 的强化学习信号。

## 核心方法

论文提出 RECAP：RL with Experience and Corrections via Advantage-conditioned Policies。训练流程分三步。

第一步，收集任务数据。数据来源包括人工示教、机器人自主执行、以及自主执行过程中专家的远程接管修正。每个 episode 通常只标注最终成功或失败。

第二步，训练语言条件的 distributional value function。这个 value function 预测距离成功还剩多少步，归一化到大致 `(-1, 0)`，其中 `0` 表示成功完成。失败 episode 在终点给一个很大的负惩罚。value 模型由较小的 VLM backbone 初始化，并在累计数据上训练。

第三步，用 value function 为每个动作估计 advantage，并转成二值 improvement indicator。策略训练不是直接对完整 VLA 做 PPO 或 REINFORCE，而是在类似监督学习的 action loss 中加入文本条件，例如 `Advantage: positive` 或 `Advantage: negative`。人工修正段默认强制标为正 advantage。

最终模型 $\pi^{*}_{0.6}$ 是在 $\pi_{0.6}$ 基础上加入 advantage conditioning。基础策略使用 Gemma 3 4B VLM backbone、860M 参数的 flow-matching action expert、多相机和本体状态观测、50 Hz action chunk，并预测高层子任务文本。

## 关键创新

- 把大 VLA 的真实机器人 RL 简化成 advantage-conditioned supervised training。
- 同时利用示教、成功/失败自主执行、旧策略数据和专家修正，而不是只筛选“好数据”。
- 避免直接计算 flow-matching action head 的精确 likelihood，因此比直接 policy-gradient 更容易扩展到大模型。
- 在多机器人数据上预训练 advantage conditioning，再用真实机器人经验做任务专门化。
- 优化真实部署更关心的 throughput，而不只看单次成功率。

## 实验

实验使用静态双臂机器人：两个 6 DoF 机械臂、平行夹爪、三路相机、关节和夹爪状态观测。主要任务包括：

- 叠 T-shirt 和 shorts：200 秒内完成。
- 多样衣物折叠：包含 11 类衣物，定量评估集中在 button-up shirt，500 秒内完成。
- 定向失败模式移除：从对抗性初始状态开始，严格要求衣领朝上。
- Cafe double-shot espresso：拿 portafilter、磨豆、压粉、锁入咖啡机、拿杯、萃取并端上，200 秒内完成。
- 纸箱组装：从扁平纸板开始折箱、贴标签、放入 crate，600 秒内完成。

对比方法包括预训练 $\pi_{0.5}$、监督训练 $\pi_{0.6}$、只做 RL 预训练但未用任务经验的 $\pi^{*}_{0.6}$、offline RL + SFT、AWR，以及 PPO 风格的 diffusion policy optimization。

主要结果：

- 在困难的多样衣物折叠和 espresso 任务上，加入 RECAP 的真实机器人经验后，每小时成功完成次数超过翻倍。
- 困难任务失败率大约降低一半。
- 除多样衣物任务外，最终模型在多数任务上达到 90% 以上成功率。
- 迭代实验中，T-shirt/shorts 折叠两轮 RECAP 后 throughput 提升约 50%；纸箱组装在第二轮后 throughput 约提升 2 倍。
- 在定向衣物失败模式实验中，两轮 RECAP、每轮 600 条轨迹，在没有额外示教或人工接管数据的情况下达到 97% 成功率。
- 在叠衣对比中，RECAP 的策略抽取效果明显好于 AWR 和 PPO 风格方法，尤其是 throughput。

## 局限性

系统并不是完全自主的。它仍需要人工标注 reward、提供接管修正，以及重置 episode。探索策略也比较朴素，主要依赖策略随机性和人工干预；因此它更适合初始 imitation policy 已经能做出部分合理行为的任务。

RECAP 采用 batch 式迭代 offline 更新：先收集一批数据，再重新训练模型，再部署下一版策略。这个流程工程上实用，但不是机器人运行时实时更新的 fully online RL。

对于小团队，复现完整系统的成本很高：需要大 VLA、value model、多相机双臂硬件、大量真实机器人 trial，以及稳定标注流程。迁移到自己的机器人时，动作接口、安全约束、自动 reset、任务标签质量都会显著影响效果。

## 实际机器人影响

这篇论文的重要点在于：它把 VLA 看作一个可以通过部署经验持续改进的机器人技能，而不是一次训练完就固定的 imitation policy。它直接对应真实机器人中的三个常见问题：

- 示教无法覆盖部署时的所有错误。
- 人工遥操作有用，但慢且质量不稳定。
- 对大规模连续动作 VLA 直接做在线 policy-gradient RL 很难稳定。

最可复用的思想是 advantage-conditioned policy interface。机器人团队可以保留原来的监督式 VLA 训练流程，只额外加入一个 value-based 标签，告诉策略哪些动作更可能改善当前行为。

## 应用到我的机器人

对我的机器人来说，最有价值的应用场景是：初始策略已经偶尔能成功，但长时序任务还不够稳定或太慢。适合任务包括叠布料、分类装箱、工具使用、操作家电、装配和清理收纳。

可执行集成路线：

- 先为一个任务训练示教策略。
- 记录每次 rollout：相机帧、机器人状态、动作、语言指令、时间戳、成功/失败标签。
- 训练一个简单 value model，预测当前观测下的剩余进度或成功概率。
- 用 value 差分把动作片段转成二值 improvement indicator。
- 用普通 behavior cloning loss 加 advantage-conditioned action loss 微调策略。
- 人工 rescue 或 correction 段标成 positive advantage，但失败的自主执行片段也保留在数据集中。
- 每轮迭代都记录 throughput、成功率、超时次数和常见失败模式。

第一版不应该直接复现完整 $\pi^{*}_{0.6}$。更现实的做法是把 RECAP 当作训练范式：在现有视觉策略上训练 critic，标出高 advantage 的 action chunk，给策略增加一个文本 token 或 learned binary token，然后测试正向条件是否提升速度和可靠性。

预期收益：机器人可以从自己的部署失败中学习，减少对新示教的依赖，并逐步提高执行速度。

主要风险：稀疏标签可能有噪声，value model 可能学到投机捷径，人工修正质量不稳定，多轮 fine-tuning 如果不保留旧数据可能发生 drift。自主采集前需要安全保护和可回滚 checkpoint。

## 实施建议

先把 RECAP 当成实验管理流程来做：

1. 定义严格的任务成功条件和超时时间。
2. 收集 baseline SFT rollout。
3. 标注成功/失败和主要失败类别。
4. 用日志 episode 训练 value model。
5. 用 positive/negative advantage conditioning 微调策略。
6. 限量部署新策略收集下一批 trial。
7. 在同一任务分布上与上一版 checkpoint 对比。

低成本原型可以用 frozen visual encoder 加小型 temporal head 替代大 value model，用当前策略自己的 action loss 替代 flow matching。核心验证问题只有一个：相比普通 behavior cloning，条件化到 high-advantage behavior 是否能提升真实部署 throughput。
