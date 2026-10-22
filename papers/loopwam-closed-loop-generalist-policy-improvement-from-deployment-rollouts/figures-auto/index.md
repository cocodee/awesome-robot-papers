# 图表索引

来源 `paper.pdf`（24 页）：图 14 张、表 5 张。全部裁剪拼在 `figures-auto/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures-auto/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 2 页 · `figures-auto/fig-01.png`
**caption**：Figure 1: LoopWAM learns from deployment. Mixed-quality rollouts return to training through quality steer- ing, source-dependent noise sampling, and quality-weighted supervision. Center: closed-loop self-improvement on RoboChallenge Table30-V2, where three rounds of deployment and retraining increase overall success from 23.67% to 43.33%. Bottom: benchmark comparisons.
· label `fig:teaser` · paper.tex L50 · 源文件 `figures/teaser.pdf`

## 图 2 · 第 4 页 · `figures-auto/fig-02.png`
**caption**：Figure 2: Overview of LoopWAM. LoopWAM is structured as a Mixture-of-Transformer (MoT) architecture, where bidirectional attention enables feature interaction between the video and action branches. Training combines quality-conditioned instructions, source-dependent noise sampling, and quality-weighted action supervision. Expert trajectories supervise both modalities, while lower-quality rollouts retain full world supervision and contribute to action imitation according to their quality. The trained model is deployed using the expert score 𝑞⋆, and recorded experience returns to the next training round.
· label `fig:method` · paper.tex L104 · 源文件 `figures/LoopWAM_method0926.pdf` · 正文引用：§3 Method (L101)

## 图 3 · 第 10 页 · `figures-auto/fig-03.png`
**caption**：Figure 3: Closed-loop improvement from real-robot deployment. Top: three deployment-and-training iterations on RoboChallenge Table30-V2, covering 30 tasks across four robot embodiments. Bottom: two deployment- and-training iterations on shirt folding after task-specific expert post-training of the DOS-W1 model. Each plot reports success rate and score over successive improvement rounds.
· label `fig:closed_loop_improvement` · paper.tex L397 · 源文件 `figures/closed_loop_improvement.pdf` · 正文引用：§4.4 Closed-Loop Improvement from Deployment (L407)

## 图 4 · 第 16 页 · `figures-auto/fig-04.png`
**caption**：Figure 4: Button pressing (ARX5). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.
· label `fig:subtask_press_the_button` · paper.tex L585 · 源文件 `figures/table30_subtask_keyframes_train/press_the_button/init.png`、`figures/table30_subtask_keyframes_train/press_the_button/01_press_2.png`、`figures/table30_subtask_keyframes_train/press_the_button/02_press_3.png`、`figures/table30_subtask_keyframes_train/press_the_button/03_press_4.png` · 正文引用：§A.4 Subtask Switching Examples (L581)

## 图 5 · 第 17 页 · `figures-auto/fig-05.png`
**caption**：Figure 5: Plant watering (ARX5). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.
· label `fig:subtask_water_the_flowers` · paper.tex L602 · 源文件 `figures/table30_subtask_keyframes_train/water_the_flowers/init.png`、`figures/table30_subtask_keyframes_train/water_the_flowers/01_place.png`

## 图 6 · 第 17 页 · `figures-auto/fig-06.png`
**caption**：Figure 6: Paper shredding (UR5). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.
· label `fig:subtask_shred_paper` · paper.tex L613 · 源文件 `figures/table30_subtask_keyframes_train/shred_paper/init.png`、`figures/table30_subtask_keyframes_train/shred_paper/01_retract.png`

## 图 7 · 第 18 页 · `figures-auto/fig-07.png`
**caption**：Figure 7: Stamp positioning (ALOHA). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.
· label `fig:subtask_stamp_positioning` · paper.tex L624 · 源文件 `figures/table30_subtask_keyframes_train/stamp_positioning/init.png`、`figures/table30_subtask_keyframes_train/stamp_positioning/01_dip.png`、`figures/table30_subtask_keyframes_train/stamp_positioning/02_stamp.png` · 正文引用：§A.4 Subtask Switching Examples (L581)

## 图 8 · 第 20 页 · `figures-auto/fig-08.png`
**caption**：Figure 8: RoboChallenge Table30-V2 leaderboard. LoopWAM ranks first with an overall score of 56.80 and a success rate of 43.33%, using a multi-task policy for each embodiment.
· label `fig:table30_leaderboard` · paper.tex L643 · 源文件 `figures/table30v2-leaderboard.png` · 正文引用：§B RoboChallenge Table30-V2 Leaderboard (L640)

## 图 9 · 第 21 页 · `figures-auto/fig-09.png`
**caption**：Figure 9: Qualitative examples of iterative execution and failure recovery. The first attempt may fail due to execution uncertainty, incomplete interaction, or object displacement. Subsequent attempts generate corrective behaviors and achieve successful task completion.
· label `fig:retry_success` · paper.tex L666 · 源文件 `figures/lyp/retry-sucess.pdf` · 正文引用：§C Failure Recovery and Iterative Execution (L658)

## 图 10 · 第 22 页 · `figures-auto/fig-10.png`（整页，需要时手动裁）
**caption**：Figure 10: Qualitative comparison between predicted future observations from LoopWAM and ground-truth robot executions. The model captures the temporal evolution of robot-object interactions and predicts plausible future visual states.
· label `fig:video_prediction` · paper.tex L698 · 源文件 `figures/lyp/video-pred-1.pdf`、`figures/lyp/video-pred-2.pdf` · 正文引用：§D Qualitative Future Observation Predictio (L689)

## 图 11 · 第 23 页 · `figures-auto/fig-11.png`
**caption**：Figure 11: Representative tasks on the ARX robot platform. The examples illustrate diverse manipulation scenarios used for evaluating LoopWAM across different robot embodiments.
· label `fig:arx_tasks` · paper.tex L735 · 源文件 `figures/lyp/arx-01.png`、`figures/lyp/arx-02.png` · 正文引用：§E Representative Robot Platforms and Tasks (L727)

## 图 12 · 第 23 页 · `figures-auto/fig-12.png`
**caption**：Figure 12: Representative tasks on the ALOHA robot platform. The examples include coordinated manipulation and object interaction requiring temporally consistent control.
· label `fig:aloha_tasks` · paper.tex L752 · 源文件 `figures/lyp/aloha-01.png`、`figures/lyp/aloha-02.png`、`figures/lyp/aloha-03.png`、`figures/lyp/aloha-04.png` · 正文引用：§E Representative Robot Platforms and Tasks (L728)

## 图 13 · 第 24 页 · `figures-auto/fig-13.png`
**caption**：Figure 13: Representative tasks on the UR5 robot platform. The examples demonstrate single-arm manipulation in structured environments.
· label `fig:ur5_tasks` · paper.tex L777 · 源文件 `figures/lyp/ur5-01.png`、`figures/lyp/ur5-02.png` · 正文引用：§E Representative Robot Platforms and Tasks (L730)

## 图 14 · 第 24 页 · `figures-auto/fig-14.png`
**caption**：Figure 14: Representative long-horizon tasks on the W1 robot platform. The examples demonstrate sequential manipulation behaviors in complex environments.
· label `fig:w1_tasks` · paper.tex L794 · 源文件 `figures/lyp/w1-01.png`、`figures/lyp/w1-02.png`、`figures/lyp/w1-03.png`、`figures/lyp/w1-04.png` · 正文引用：§E Representative Robot Platforms and Tasks (L732)

## 表 1 · 第 8 页 · `figures-auto/tab-01.png`
**caption**：Table 1: Performance on RoboChallenge Table30-V2. We report per-embodiment success rates (SR, %) and overall performance across four robot embodiments. Baselines are sorted by overall SR. Bold denotes the best performance, while blue and light blue highlight LoopWAM and the runner-up, respectively.
· label `tab:robochallenge_results` · paper.tex L281 · 正文引用：§1 Introduction (L69)；§4.3 Benchmark Results (L379)

## 表 2 · 第 9 页 · `figures-auto/tab-02.png`
**caption**：Table 2: Performance on RoboTwin 2.0. We report success rates (SR, %) under clean and randomized evaluation settings. Embodied PT. denotes additional embodied-data pretraining before benchmark training. LoopWAM is trained with the mixed expert–rollout corpus described in Section 4.2. Blue and light blue highlight LoopWAM and the runner-up, respectively.
· label `tab:robotwin_results` · paper.tex L312 · 正文引用：§1 Introduction (L70)；§4.2 Benchmark Experimental Setup (L342)；§4.3 Benchmark Results (L385)

## 表 3 · 第 9 页 · `figures-auto/tab-03.png`
**caption**：Table 3: Performance on RoboCasa365. We report success rates (SR, %) across three evaluation splits. Baseline results are obtained from the official leaderboard. Embodied PT. follows the definition in Table 2. Blue and light blue highlight LoopWAM and the runner-up, respectively.
· label `tab:robocasa_results` · paper.tex L340 · 正文引用：§1 Introduction (L70)；§4.3 Benchmark Results (L390)

## 表 4 · 第 10 页 · `figures-auto/tab-04.png`
**caption**：Table 4: Ablation study on RoboTwin 2.0. We evaluate quality steering with different annotation schemes and assess the effect of quality-weighted rollout action supervision (Act.).
· label `tab:robotwin_ablation` · paper.tex L431 · 正文引用：§4.5 Ablation Study (L453)

## 表 5 · 第 15 页 · `figures-auto/tab-05.png`
**caption**：Table 5: Table30-V2 subtask instructions, listed in execution order.
· label `tab:table30_subtasks` · paper.tex L551 · 正文引用：§A.3 Table30-V2 Subtask Segmentation (L548)
