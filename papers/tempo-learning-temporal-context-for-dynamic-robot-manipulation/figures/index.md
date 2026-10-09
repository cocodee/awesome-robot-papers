# 图表索引

来源 `paper.pdf`（17 页）：图 10 张、表 7 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 2 页 · `figures/fig-01.png`
**caption**：Figure 1: TEMPO makes a pretrained VLA motion-aware. Four dynamic tasks (left) in which the target object is in motion throughout the episode. A standard VLA, conditioned on a single observation, cannot determine how the scene is evolving (center, red; “? m/s”) and cannot disam- biguate perceptually identical observations that arise at different phases of the same task, producing failed grasps and mistimed actions. TEMPO resolves both failure modes by augmenting the policy with two compact signals: TEMPOMOT, a motion representation from a frozen video foundation model, and TEMPOACT, a compact proprioceptive history providing subtask context. Together they enable reliable task completion across all four tasks (right, green).
· label `fig:teaser` · paper.tex L34 · 源文件 `2026-corl-unveil-template/figures/teaser.pdf` · 正文引用：§1 Introduction (L28)；§1 Introduction (L32)

## 图 2 · 第 3 页 · `figures/fig-02.png`
**caption**：Figure 2: Robot joint action (blue) does not track the human hand (red). Side-by-side compar- ison of a Drop Catch rollout from the baseline (VLASH, left) and TEMPO (right). The baseline oscillates left-to-right continuously while the human hand moves in a single direction, whereas TEMPO closely tracks the hand.
· label `fig:jittery` · paper.tex L74 · 源文件 `2026-corl-unveil-template/figures/jittery.pdf` · 正文引用：§1 Introduction (L53)；§3 Motion Ambiguity and State Aliasing (L83)

## 图 3 · 第 5 页 · `figures/fig-03.png`
**caption**：Figure 3: TEMPO architecture. TEMPO augments a pretrained VLM-based policy with two temporal inputs. TEMPOMOT cross-attends the current frame’s patch features ft against a streaming cache Ft of features from the preceding W −1 frames, producing a motion code mt that encodes scene dynamics. TEMPOACT mean pools the robot’s recent proprioceptive command history into K fixed-size buckets, yielding a compact summary ct. Both signals attach to the pretrained backbone with near-zero overhead: mt and ct are projected to the VLM’s token dimension and appended to its prefix, and ct additionally conditions the action expert via an AdaRMS residual.
· label `fig:method` · paper.tex L111 · 源文件 `2026-corl-unveil-template/figures/tempo_main.pdf` · 正文引用：§4 \methodname (L119)；§4.1 TEMPO\textsubscriptMOT: Captures Object  (L123)；§4.3 Plug-and-Play Temporal Integration (L166)

## 图 4 · 第 7 页 · `figures/fig-04.png`
**caption**：Figure 4: Task Setup. We benchmark all models across four comprehensive dynamic tasks.
· label `fig:tasks` · paper.tex L224 · 源文件 `2026-corl-unveil-template/figures/handover.pdf`、`2026-corl-unveil-template/figures/drop.pdf`、`2026-corl-unveil-template/figures/flick.pdf`、`2026-corl-unveil-template/figures/pour.pdf`

## 图 5 · 第 8 页 · `figures/fig-05.png`
**caption**：Figure 5: Failure-mode breakdown on Bottle Handover, we categorized and visually examined each episode in deployment rollouts and attributed each model’s failure to different categories.
· label `fig:failure_modes` · paper.tex L250 · 源文件 `2026-corl-unveil-template/figures/failure_modes.pdf` · 正文引用：§5.2 Experimental Results (L264)；§7 Conclusion (L346)；Appendix (L366)；§C Per-Task Failure Mode Breakdown (L412)

## 图 A1 · 第 14 页 · `figures/fig-A1.png`
**caption**：Figure A1: VLASH rollout on the untrimmed Flick Catch task. The task is to grip the velcro plate and follow the human hand. VLASH’s gripper hovers near the plate without committing to grasp or retract, because a single-frame observation cannot differentiate reaching for the plate from releasing it. RTC exhibits the same failure (see project page).
· label `fig:ambiguity` · paper.tex L376 · 源文件 `2026-corl-unveil-template/figures/state_alias.pdf` · 正文引用：§4.2 TEMPO\textsubscriptACT: Resolves State A (L152)；Appendix (L364)；§A Additional Failure Mode Analysis (L374)

## 图 A2 · 第 15 页 · `figures/fig-A2.png`
**caption**：Figure A2: Failure-mode breakdown on Flick Catch. Each of the 50 rollouts is decomposed into success plus three failure modes corresponding to the three task stages (grab plate, track hand, catch ball). VLASH’s failures concentrate in hand-tracking and RTC struggles most at tracking the ball’s trajectory (see project page); TEMPO cuts both failure modes.
· label `fig:flick_failure` · paper.tex L414 · 源文件 `2026-corl-unveil-template/figures/failure_modes_flick.pdf` · 正文引用：Appendix (L366)；§C Per-Task Failure Mode Breakdown (L421)

## 图 A3 · 第 15 页 · `figures/fig-A3.png`
**caption**：Figure A3: Failure-mode breakdown on Drop Catch. RTC scores highest as Drop Catch is dom- inated by reactive timing rather than motion or state ambiguity. VLASH’s dominant failure is pre- mature movement before the human’s hand begins to move; TEMPO cuts this failure by nearly 4×.
· label `fig:drop_failure` · paper.tex L424 · 源文件 `2026-corl-unveil-template/figures/failure_modes_drop.pdf` · 正文引用：Appendix (L366)；§C Per-Task Failure Mode Breakdown (L431)

## 图 A4 · 第 16 页 · `figures/fig-A4.png`
**caption**：Figure A4: Both TEMPOMOT and TEMPOACT are necessary. Per-frame action MSE for the full TEMPO model (blue) vs. the two single-signal ablations, evaluated on the Flick Catch task. Freezing TEMPOMOT to its first-frame value (green) hurts most at 2.7 s, the beginning of the task where human hand starts to move. Freezing TEMPOACT (red) hurts most at 5.3 s, the middle of the task where the finger sweeps horizontally across the balls before picking one and flicking it. Thus, each signal plays an important role at a different moment in the task.
· label `fig:attention_mse` · paper.tex L434 · 源文件 `2026-corl-unveil-template/figures/ablation_mse.pdf` · 正文引用：Appendix (L367)；§D Input Ablation (L445)

## 图 A5 · 第 16 页 · `figures/fig-A5.png`（整页，需要时手动裁）
**caption**：Figure A5: Linear probe of candidate initializations for TEMPOMOT. Top: one example frame per task showing the object of interest (red dot) and its recent trajectory (yellow line); the pixel-space velocity of this object is the regression target the linear probe must predict. Bottom: per-task velocity R2 for each candidate initialization, along with the average. Higher is better; the raw object-position baseline (R2 = 0.08 on average) cannot recover velocity from a single position, while every learned motion encoder does so substantially better.
· label `fig:ball_velocity_probe` · paper.tex L450 · 源文件 `2026-corl-unveil-template/figures/velocity_handover.png`、`2026-corl-unveil-template/figures/velocity_drop.png`、`2026-corl-unveil-template/figures/velocity_flick.png`、`2026-corl-unveil-template/figures/velocity_pour.png` · 正文引用：§4.1 TEMPO\textsubscriptMOT: Captures Object  (L148)；Appendix (L368)；§E Motion Encoder Selection (L494)

## 表 1 · 第 4 页 · `figures/tab-01.png`
**caption**：Table 1: Success on the untrimmed Flick Catch and Wine Pour, where each episode retains the release-and-retract phase that pro- duces state aliasing. Both asynchronous baselines fail every rollout; TEMPO com- pletes the task by using TEMPOACT to dis- ambiguate phases the current frame cannot.
· label `tab:state_alias` · paper.tex L85 · 正文引用：§3 Motion Ambiguity and State Aliasing (L103)；§7 Conclusion (L346)；Appendix (L364)；§A Additional Failure Mode Analysis (L385)

## 表 2 · 第 4 页 · `figures/tab-02.png`
**caption**：Table 2: Swapping the motion encoder ϕ keeps Bottle Handover success comfort- ably above the VLASH baseline (38%).
· label `tab:encoder_swap` · paper.tex L130 · 正文引用：§4.1 TEMPO\textsubscriptMOT: Captures Object  (L148)

## 表 3 · 第 6 页 · `figures/tab-03.png`
**caption**：Table 3: Inference latency comparison across methods.
· label `tab:latency_comparison` · paper.tex L175 · 正文引用：§4.1 TEMPO\textsubscriptMOT: Captures Object  (L148)；§4.4 Real-Time Deployment via Parallel Encodi (L192)；§E Motion Encoder Selection (L494)

## 表 4 · 第 6 页 · `figures/tab-04.png`
**caption**：Table 4: Success rates across the four dynamic tasks. Each entry is the percentage of 50 real-world rollouts in which the policy completes the task, evaluated under varied object speeds, appearances, and approach directions. For Wine Pour task, instead of recording binary success or failure, we measure the percentage of the ”wine” mass retained in the pot at the end of the pour.
· label `tab:success_rates` · paper.tex L196 · 正文引用：§3 Motion Ambiguity and State Aliasing (L103)；§5.1 Experimental Setup (L234)；§5.2 Experimental Results (L259)；§5.2 Experimental Results (L287)；Appendix (L364)；§A Additional Failure Mode Analysis (L374)

## 表 5 · 第 8 页 · `figures/tab-05.png`
**caption**：Table 5: TEMPO is plug-and-play across VLA backbones. Adding TEMPOMOT and TEMPOACT improves Bottle Handover on all backbones, in- cluding the non-asynchronous π0.5.
· label `tab:backbone_integration` · paper.tex L266 · 正文引用：§5.2 Experimental Results (L284)

## 表 6 · 第 9 页 · `figures/tab-06.png`
**caption**：Table 6: Both temporal signals con- tribute to the task. Removing either TEMPOMOT or TEMPOACT reduces Bottle Handover success; the two to- gether outperform either alone.
· label `tab:input_ablation` · paper.tex L294 · 正文引用：§6 Analysis and Ablations (L312)

## 表 7 · 第 9 页 · `figures/tab-07.png`
**caption**：Table 7: Motion probing of the trained VLA hidden state. MLP probe on object velocity across our dynamic tasks (R2). On Flick Catch and Wine Pour, where motion is the only usable cue, the asynchronous baselines’ representations collapse to near zero while TEMPO’s remains informative.
· label `tab:motion_probe` · paper.tex L320 · 正文引用：§3 Motion Ambiguity and State Aliasing (L83)；§6 Analysis and Ablations (L316)；§6 Analysis and Ablations (L318)
