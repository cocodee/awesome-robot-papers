# 图表索引

来源 `paper.pdf`（21 页）：图 10 张、表 8 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 1 页 · `figures/fig-01.png`
**caption**：Figure 1: A typical robot policy maps a simple instruction and an observation into a short action chunk. As datasets scale, this mapping becomes increasingly multimodal and uncertain, leading models to learn spurious short-horizon correlations. VPP2 first establishes consistent semantic-to- trajectory mappings via next event video prediction with detailed captions, then post-trains and distills the model to generate short action chunks.
· label `fig:fig1` · paper.tex L14 · 源文件 `figures/fig1_0926_scientific_colors_checked.pdf` · 正文引用：§1 Introduction (L30)

## 图 2 · 第 3 页 · `figures/fig-02.png`
**caption**：Figure 2: An example of our data processing pipeline. The central objective is to reduce uncertainty in future prediction, thereby encouraging the model to learn a consistent mapping from conditioning information to sub-task trajectories. To this end, each caption includes detailed task descriptions, explicit end-effector identification, a description of the visible target object, and camera-view changes.
· label `fig:fig2` · paper.tex L79 · 源文件 `figures/fig2_2.pdf` · 正文引用：§2 Data Processing Pipeline (L77)；§2 Data Processing Pipeline (L122)

## 图 3 · 第 3 页 · `figures/fig-03.png`
**caption**：Figure 3: (a) Bounding boxes show the aligned workspaces of different datasets. (b) Aligned end-effector coordinate frames.
· label `fig:coordinate_alignment` · paper.tex L87 · 源文件 `figures/fig3_2.pdf`

## 图 4 · 第 5 页 · `figures/fig-04.png`
**caption**：Figure 4: The VPP2 training pipeline is designed to maximize generalization. Stage 1 uses large- scale, event-level video pretraining to learn a generalizable video model for manipulation. Stage 2 post-trains and distills this model to predict long-horizon video chunks spanning 8 seconds in a single forward pass, taking approximately 0.1 seconds. Finally, Stage 3 trains an action expert to generate 2-second action chunks conditioned on the one-step video latents.
· label `fig:fig4` · paper.tex L188 · 源文件 `figures/fig4_3.pdf` · 正文引用：§3 VPP2: A Generalist Policy with Zero-shot (L127)

## 图 5 · 第 6 页 · `figures/fig-05.png`
**caption**：Figure 5: VPP2 video predictions for human-hand and robot manipulation. Trained on large-scale, diverse manipulation datasets, VPP2 generalizes across human hands and a wide range of robot embodiments. For robot manipulation, VPP2 jointly predicts one to three camera views arranged in a T-shaped composite. Due to space constraints, single-step video predictions after distillation are shown in Figure 10 in the appendix.
· label `fig:fig6` · paper.tex L271 · 源文件 `figures/fig6.pdf`、`figures/fig7.pdf` · 正文引用：§4.1 Video Prediction Quality Analysis (L289)；§4.1 Video Prediction Quality Analysis (L290)

## 图 6 · 第 7 页 · `figures/fig-06.png`（整页，需要时手动裁）
**caption**：Figure 6: Win rates of the pretrained VPP2 model against different baselines on video prediction tasks.
· label `table:video_quality, fig:fig8` · paper.tex L297 · 源文件 `figures/fig8_2_0921.pdf` · 正文引用：§4.1 Video Prediction Quality Analysis (L295)

## 图 7 · 第 7 页 · `figures/fig-07.png`
**caption**：Figure 7: Comparison of instruction-following capabilities among VPP2, Wan-14B, and Cosmos3- 64B. VPP2 demonstrates better instruction following on complex tasks requiring spatial understand- ing.
· label `fig:fig5` · paper.tex L337 · 源文件 `figures/fig5_2.pdf` · 正文引用：§4.1 Video Prediction Quality Analysis (L295)

## 图 8 · 第 8 页 · `figures/fig-08.png`
**caption**：Figure 8: Zero-shot success rates on the real-world ALOHA across 10 randomly selected task categories. For a fair comparison, we finetune π0.5 and FastWAM on all ALOHA datasets exposed in VPP2’s training data and use the 14B variant of FastWAM.
· label `fig:fig9` · paper.tex L351 · 源文件 `figures/fig10.pdf` · 正文引用：§4.2 Policy Performance Analysis (L349)

## 图 9 · 第 9 页 · `figures/fig-09.png`
**caption**：Figure 9: Success rates with and without VLM-based subtask planning (50 trials per task). Average is the five-task mean; the baseline checkpoint matches Table 4.
· label `fig:subtask_planning` · paper.tex L488 · 源文件 `figures/subtask_planning.pdf` · 正文引用：§4.2 Policy Performance Analysis (L486)

## 图 10 · 第 19 页 · `figures/fig-10.png`
**caption**：Figure 10: Additional video prediction results on open-ended tasks. We compare single-step video predictions before and after distillation. Distillation enables high-quality video prediction with just one sampling step.
· label `fig:video_app` · paper.tex L603 · 源文件 `figures/video_comparison_8groups_updated.pdf` · 正文引用：§3.3 VLM for High-level Planning. (L275)

## 表 1 · 第 3 页 · `figures/tab-01.png`
**caption**：Table 1: Overview of training data sources. Full dataset references are provided in Appendix A, Table 5.
· label `table:video_source` · paper.tex L42 · 正文引用：§2 Data Processing Pipeline (L40)；§A Dataset Process Details (L526)

## 表 2 · 第 7 页 · `figures/tab-02.png`
**caption**：Table 2: Instruction following success rates.
· label `table:video_quality` · paper.tex L322 · 正文引用：§4.1 Video Prediction Quality Analysis (L295)

## 表 3 · 第 8 页 · `figures/tab-03.png`
**caption**：Table 3: Post-training on LIBERO-ID, LIBERO-Pro, and LIBERO-OOD benchmarks. All models are trained exclusively on the four standard LIBERO suites (Liu et al., 2023) and are evaluated under three complementary settings.
· label `tab:libero_generalization` · paper.tex L359 · 正文引用：§4.2 Policy Performance Analysis (L476)；§C.1 Detailed LIBERO Results (L613)

## 表 4 · 第 9 页 · `figures/tab-04.png`
**caption**：Table 4: Post-training results on the RoboDojo simulation benchmark. Average score captures partial task progress, and success rate measures binary task completion; both are averaged over the five capability dimensions. Baseline results are taken from the official leaderboard.
· label `tab:robodojo` · paper.tex L456 · 正文引用：§4.2 Policy Performance Analysis (L481)；§4.2 Policy Performance Analysis (L484)；§4.2 Policy Performance Analysis (L492)；§C.2 Detailed RoboDojo Results (L643)

## 表 5 · 第 18 页 · `figures/tab-05.png`
**caption**：Table 5: Training data sources with references to the original datasets. Self-collected datasets are collected as part of this work.
· label `table:video_source_full` · paper.tex L528 · 正文引用：§2 Data Processing Pipeline (L69)；§A Dataset Process Details (L526)

## 表 6 · 第 20 页 · `figures/tab-06.png`
**caption**：Table 6: Per-suite success rates (%) on the standard LIBERO benchmark. Best results in each column are in bold.
· label `tab:app_libero` · paper.tex L615 · 正文引用：§C.1 Detailed LIBERO Results (L613)

## 表 7 · 第 20 页 · `figures/tab-07.png`
**caption**：Table 7: Per-dimension average score on the RoboDojo simulation benchmark. Generalization is evaluated under standard (Std.) and randomized (Rand.) settings. Avg. is the mean over the five capability dimensions, where the generalization score is the mean of the Std. and Rand. settings. For VPP2, we report the generalization result pooled over both settings (25 episodes each, following the official protocol), which equals their mean. Baseline results are taken from the official leaderboard.
· label `tab:app_robodojo_score` · paper.tex L645 · 正文引用：§C.2 Detailed RoboDojo Results (L643)；§C.2 Detailed RoboDojo Results (L691)

## 表 8 · 第 21 页 · `figures/tab-08.png`
**caption**：Table 8: Per-dimension success rate (%) on the RoboDojo simulation benchmark, computed in the same way as Table 7.
· label `tab:app_robodojo_sr` · paper.tex L670 · 正文引用：§C.2 Detailed RoboDojo Results (L643)
