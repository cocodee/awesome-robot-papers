# AlphaNIST：从二元任务奖励涌现装配技能

## 元数据

- 作者：Octi Zhang、Iretiayo Akinola、Rosario Scalise、Mateo Guaman Castro 等 15 人
- 机构：NVIDIA、University of Washington
- 发表：arXiv:2610.13354v1，2026；arXiv 备注“ICRA”，尚未据此认定录用
- 来源：[论文](https://arxiv.org/abs/2610.13354) · [项目页及演示](https://alpha-nist.github.io/)
- 本地：[PDF](../papers/alphanist-emergent-assembly-skills/paper.pdf) · [转换 Markdown](../papers/alphanist-emergent-assembly-skills/paper.md) · [精读笔记](../papers/alphanist-emergent-assembly-skills/精读笔记.md) · [详解教程](alphanist-emergent-assembly-skills-tutorial.md)
- 代码状态：项目页截至 2026-10-14 标注待发布；本分析不声称已核对代码。

## 研究问题

精密装配通常依赖示教、手写技能序列、易起步姿态或“靠近—对齐”的稠密奖励。AlphaNIST 研究：能否从大范围初始状态出发，用一个共享策略和完成/失败信号学会 NIST Assembly Task Board #1 的 20 个不同装配对，并涌现重抓、借助环境调整姿态及多件顺序协调？[论文 §I–III](../papers/alphanist-emergent-assembly-skills/paper.tex)

## 方法与关键创新

方法结合三件事：覆盖未抓、在手、近装配和部分装配的 `(任务, 状态)` reset bank；按 `εq+√[p̂(1−p̂)]` 为每个起点分配练习概率的 success-guided beta sampling；20 项任务共用的完整装配成功条件。所有任务使用一套 PPO actor/critic、奖励和训练参数。策略由点云、本体状态和上一动作输出 7 维关节增量与 1 维夹爪命令，25 Hz 控制。[图 3](../papers/alphanist-emergent-assembly-skills/figures/fig-03.png)、[图 4](../papers/alphanist-emergent-assembly-skills/figures/fig-04.png)、[论文 §IV](../papers/alphanist-emergent-assembly-skills/paper.tex)

创新点是把异构任务视作共享装配经验，而不是为每种几何先训专家；reset bank 解决“永远见不到完成”的冷启动，动态采样集中计算于当前成功率中等的起点。论文不提供抓取、重定位、插入或装配顺序的技能脚本。

## 训练与数据

一次训练条目是 `(装配对身份 eᵢ, 可复位状态 s̄ᵢ)`，不是人类演示。仿真在线生成点云观察、动作、奖励和转移。输入含工件/配合几何/机器人表面点云 `3×npts`，加位姿 7、twist 6、关节 9、上一动作 8；论文未给固定 `npts`。策略输出 `a=[Δq₁:₇,夹爪]`。单件完成阈值是装配误差 `<1 mm`，成功只奖励一次；总奖励另扣动作幅度、关节速度和力矩平方的共同控制成本。十件任务只在全部完成时给成功奖励。[论文 §IV-B–D](../papers/alphanist-emergent-assembly-skills/paper.tex)

每轮 PPO 在每个并行环境采 32 步，更新 5 epoch、每 epoch 4 minibatch。实验覆盖 1K–256K 并行环境，跨 GPU 平均梯度；64K 环境、25K 迭代的共享策略约用 410 GPU-hours。[论文 §IV-E、§V](../papers/alphanist-emergent-assembly-skills/paper.tex)

## 实验

| 实验 | 结果 | 解读边界 |
| --- | ---: | --- |
| 64K 环境、25K 迭代的 20 项单件共享稀疏策略 | 98.2% 训练成功 | 20 个独立稀疏策略平均 81.4%；图 5。 |
| 相同设置加入 reach/align 稠密项 | 共享策略 17.8% | 独立稠密策略平均 78.3%；只测试这两种塑形项，不能说全部稠密奖励都会失败。 |
| 256K 环境的采样消融 | beta 97.4%，uniform 84.3% | 同一 reset bank，固定 25K 迭代评测；图 7。 |
| 单回合完成 10 对 | 84% | 为多对设置单独训练策略，全部完成后才给成功奖励；表 I。 |

图 8 展示放下重抓、环境接触转向、轻敲螺母等行为；图 9 展示先把 USB-A 移近，完成 8 mm 杆后返回的顺序协调。[图 8](../papers/alphanist-emergent-assembly-skills/figures/fig-08.png)、[图 9](../papers/alphanist-emergent-assembly-skills/figures/fig-09.png)

## 局限性

全部实验在仿真中；匹配硬件速度和力矩限制，仍不能证明真实视觉噪声、摩擦、接触模型与延迟下的成功率。98.2% 是 64K 设置的训练成功率，与 256K 设置的 97.4% 评测数值不同。论文只展示十对同回合完成，未展示单回合完成板上全部 20 对。所谓“二元奖励”是二元**任务成功**信号，总奖励并非严格只有 0/1，因为含连续控制成本。当前无官方代码可逐行复核 PPO/点云实现。[论文 §V–VI](../papers/alphanist-emergent-assembly-skills/paper.tex)

## 应用到我的机器人

**集成思路：**先选一个插销或齿轮装配对，在仿真中建立有效的散落、在手、接近配合和部分装配 reset bank；以最终成功为主要任务信号，比较均匀抽样与动态 beta 抽样，记录每类起点的完成率。扩展到多任务时保持相同奖励定义和控制配置，用点云让策略识别几何。

**所需传感器与算力：**真机需要深度/点云、关节状态、夹爪反馈、可靠的完成检测及速度/力矩限位；训练需要高吞吐、接触准确的并行仿真和 GPU。论文的 64K 设置约 410 GPU-hours，不是普通工作站即刻可复现的成本。

**预期收益与风险：**可减少手写抓取/插入阶段和装配顺序，学到环境辅助重定位与失败恢复；风险在于 reset bank 构造、接触仿真偏差、真实点云遮挡、奖励阈值错误和大规模探索成本。部署前应先对单件装配做低速、限幅的真实验证。
