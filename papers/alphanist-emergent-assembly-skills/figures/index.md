# 图表索引

来源 `paper.pdf`（8 页）：图 9 张、表 1 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 1 页 · `figures/fig-01.png`
**caption**：Fig. 1. Emergent multi-component assembly with a single policy. Trained with a binary task reward, AlphaNIST learns to select, grasp, reorient, and assemble diverse components, while autonomously sequencing multiple assemblies within a single episode. Shown are snapshots from a ten-component assembly sequence.

## 图 2 · 第 2 页 · `figures/fig-02.png`
**caption**：Fig. 2. The complete NIST Assembly Task Board #1 in simulation. Yellow indicates the 20 movable parts in their fully-assembled states.
· label `fig:nistboard-overview` · paper.tex L61 · 源文件 `figures/overview/nistboard_fully_assembled.png` · 正文引用：§1 Introduction (L72)

## 图 3 · 第 4 页 · `figures/fig-03.png`
**caption**：Fig. 3. Policy architecture. Actor and critic have the same architecture with separate parameters. Inputs are drawn once; each network contains two consecutive residual blocks. RN: running normalization; LN: layer normalization; SW: Swish activation; npts: number of input points.
· label `fig:policy-architecture` · paper.tex L214 · 正文引用：§4.4 Shared Policy and Robot Control (L571)

## 图 4 · 第 4 页 · `figures/fig-04.png`
**caption**：Fig. 4. Diverse assembly reset states. Examples of resets across tasks, ranging from random object poses to in-hand grasps and partial assemblies.
· label `fig:reset-coverage` · paper.tex L406 · 源文件 `figures/method/reset_coverage.png` · 正文引用：§4.2 Reset Coverage and Experience Allocation (L401)

## 图 5 · 第 5 页 · `figures/fig-05.png`
**caption**：Fig. 5. Training across heterogeneous assembly pairs substantially improves learning from a sparse binary task reward. At 64K environments across 25k iterations: (a) compares 20-task success rates for one shared policy versus 20 separately trained policies. The shared policy (first row) achieved above 98% success rate across all tasks, including three precision assemblies that corresponding specialists rarely solve. Dense shaping does not exhibit the same benefit. Panel (b) shows overall success, note that the separate-policy success rate is average across all 20 per-task policies; Asset notation: N, G, R, and P denote nuts, gears, rods, and pegs, respectively; numeric suffixes indicate nominal diameters in millimeters, while s, m, and l indicate gear size. "Sparse reward" denotes Eq. (6); "dense reward" additionally includes the shaping terms in Eq. (7).
· label `fig:heterogeneity-ablation` · paper.tex L469 · 源文件 `figures/results/heterogeneity.pdf` · 正文引用：§2.1 Scalable Learning for Contact-Rich Assem (L120)；§5.1 Assembly-Pair Heterogeneity Enables Lear (L701)

## 图 6 · 第 5 页 · `figures/fig-06.png`
**caption**：Fig. 6. Joint sparse training converges faster than separate policies. Curves compare one shared policy trained on all 20 tasks with the mean of 20 policies trained separately, one per task.
· label `fig:heterogeneity-dynamics` · paper.tex L486 · 源文件 `figures/results/heterogeneity_dynamics.pdf` · 正文引用：§5.1 Assembly-Pair Heterogeneity Enables Lear (L708)

## 图 7 · 第 5 页 · `figures/fig-07.png`
**caption**：Fig. 7. Sparse task rewards benefit strongly from parallel experience. Mean success ± standard deviation over 5 evaluation seeds for 25k-iteration checkpoints, with 32 trials per task per seed across 20 assemblies. Color denotes reward; solid and dashed lines denote beta and uniform training- reset sampling.
· label `fig:parallel-scaling` · paper.tex L495 · 源文件 `figures/results/scaling.pdf` · 正文引用：§5.2 Sparse Binary Task Rewards Benefit from  (L712)

## 图 8 · 第 6 页 · `figures/fig-08.png`
**caption**：Fig. 8. One shared policy discovers diverse contact strategies from a sparse binary task reward. Each panel proceeds from left to right. (a) Waterproof connector: board contact helps reorient the part before insertion. (b) D-sub connector: the part is set down and regrasped for alignment with its socket. (c) 8 mm peg: the part is dropped from a center grasp and regrasped near one end, leaving its remaining length free for insertion. (d) Medium gear: the part pivots from a side grasp into a horizontal pose over its mounting post. (e) M12 nut: the nut is rolled from its edge onto a flat face before placement on the bolt. (f) M4 nut: repeated one-sided taps advance the nut along the thread. (g) 8 mm rod: the fingertip shovels the rod to a position where it is easier to lift. (h) M16 nut: the gripper moves around the nut, using fingertip contact to turn it along the bolt.
· label `fig:emergent-assembly-strategies` · paper.tex L507 · 源文件 `figures/qualitative/waterproof_strategy.png`、`figures/qualitative/dsub_strategy.png`、`figures/qualitative/peg_insert_8mm_strategy.png`、`figures/qualitative/gear_mesh_medium_strategy.png` · 正文引用：§5.3 Emergent Strategies over Short Horizons (L722)

## 图 9 · 第 7 页 · `figures/fig-09.png`
**caption**：Fig. 9. Emergent coordination in multi-pair assembly. (a) The policy brings the USB-A connector from a distant corner to a nearby working position, leaves it there while assembling the 8 mm rod, then returns to insert the connector. (b) During M12 nut threading, the end effector makes small turns to avoid touching the neighboring RJ45 connector. Each sequence proceeds from left to right.
· label `fig:long-horizon-multi-asset` · paper.tex L543 · 源文件 `figures/qualitative/bring_close_deferred_assembly.png`、`figures/qualitative/small_turns.png` · 正文引用：§5.4 Emergent Strategies over Long Horizons (L735)

## 表 I · 第 7 页 · `figures/tab-I.png`
**caption**：TABLE I SUCCESS RATE FOR MULTI-PAIR ASSEMBLY EACH POLICY IS TRAINED AND EVALUATED ON THE SAME NUMBER OF ACTIVE ASSEMBLY PAIRS, FROM 1–10. ALPHANIST SOLVES THESE TASKS WITHOUT A PRESCRIBED ORDER OR EXPLICIT TASK DECOMPOSITION. FOR EXAMPLE, WHEN THERE ARE 10 ACTIVE PAIRS, THE POLICY RECEIVES A SUCCESS REWARD ONLY WHEN ALL 10 ARE IN THEIR ASSIGNED BOARD SLOTS.
· label `tab:seq-success` · paper.tex L670 · 正文引用：§5.4 Emergent Strategies over Long Horizons (L734)
