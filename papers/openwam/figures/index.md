# 图表索引

来源 `paper.pdf`（18 页）：图 5 张、表 14 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 2 页 · `figures/fig-01.png`
**caption**：Figure 1. Overview of OPENWAM. Left: Starting from Wan2.2 [75], causal pretraining on robot and human-interaction video builds a predictive backbone without action labels, followed by video–action training on simulated and real-robot demonstrations. Top right: A shared Mixture-of-Transformers couples temporally aligned video and action streams through joint attention while retaining modality- specific experts. Middle right: Configurable cross-modal attention and generation order support joint, video-then-action, action-then-video, and decoupled prediction within the same architecture. Bottom right: Local-context inverse and forward dynamics models are trained independently using demonstrations and counterfactual transitions. A frozen IDM translates predictions from compatible task-adapted video models into actions, while an FDM predicts the visual consequences of candidate actions.
· label `fig:openwam-teaser` · paper.tex L35 · 源文件 `sec/images/openwam-fig1-combined-v4.pdf` · 正文引用：§1 Introduction (L61)

## 图 2 · 第 5 页 · `figures/fig-02.png`
**caption**：Figure 2. Shared MoT architecture. Two modality-specific branches keep their own normalization, projection and feed-forward parameters and meet in a single attention over the packed video and action tokens; a separate cross-attention consumes the task text. Noisy future tokens enter at the bottom and the preceding chunks sit behind as history context.
· label `fig:openwam-mot-programs` · paper.tex L318 · 源文件 `sec/images/openwam-fig2-arch-v1.pdf` · 正文引用：§3.3 Configurable Video--Action Interaction P (L314)

## 图 3 · 第 5 页 · `figures/fig-03.png`
**caption**：Figure 3. Attention masks the shared architecture exposes: four interaction programs (A–D) and the two local-context dynamics programs (E–F). Columns are the streams a row may condition on, cell colour gives what it attends to there, and the numeral marks the generation pass. E and F carry one row each because each predicts a single stream: the inverse model produces actions, the forward model observations.
· label `fig:openwam-masks` · paper.tex L344 · 源文件 `sec/images/openwam-fig3-masks-v1.pdf` · 正文引用：§3.3 Configurable Video--Action Interaction P (L315)

## 图 4 · 第 6 页 · `figures/fig-04.png`
**caption**：Figure 4. Evaluation tasks. Left: the three real-world bimanual tasks of Table 2, each shown as frames sampled along one successful rollout. Right: the four LIBERO-90 targets of Table 1 used for component transfer, which lie outside the LIBERO-Long source-task set.
· label `fig:tasks` · paper.tex L385 · 源文件 `sec/images/openwam-fig3-tasks-v1.pdf` · 正文引用：§4.1 Experimental Setup (L666)

## 图 5 · 第 15 页 · `figures/fig-05.png`
**caption**：Figure 5. Real-world bimanual setup with two Franka FR3 arms, Flexiv Grav grippers, bimanual GELLO teleoperation [83], two wrist-mounted RealSense D405 cameras, and a central Orbbec Femto Mega camera.
· label `fig:real_robot_setup` · paper.tex L1221 · 源文件 `sec/images/openwam-real-setup.png` · 正文引用：§A.5 Real Robot Setup (L1228)

## 表 1 · 第 5 页 · `figures/tab-01.png`
**caption**：Table 1. LIBERO-90 targets used for component-transfer evalua- tion.
· label `tab:transfer-tasks` · paper.tex L357 · 正文引用：§3.3 Configurable Video--Action Interaction P (L390)；§4.1 Experimental Setup (L634)

## 表 2 · 第 7 页 · `figures/tab-02.png`
**caption**：Table 2. Real-world bimanual manipulation tasks.
· label `tab:real-world-tasks` · paper.tex L637 · 正文引用：§3.3 Configurable Video--Action Interaction P (L389)；§4.1 Experimental Setup (L666)；§4.2 Native Policy Performance (L972)

## 表 3 · 第 8 页 · `figures/tab-03.png`
**caption**：Table 3. Closed-loop success (%) on four LIBERO suites. Baselines are previously reported results.
· label `tab:libero-broad` · paper.tex L689 · 正文引用：§4.2 Native Policy Performance (L956)

## 表 4 · 第 8 页 · `figures/tab-04.png`
**caption**：Table 4. Closed-loop success (%) on real-world bimanual manipu- lation tasks.
· label `tab:real-world-native` · paper.tex L761 · 正文引用：§4.2 Native Policy Performance (L971)

## 表 5 · 第 9 页 · `figures/tab-05.png`
**caption**：Table 5. Frozen inverse dynamics transfer to four LIBERO-90 targets. Target rows use task-tuned video predictors while source-trained IDMs remain frozen. Mean is averaged over the four target tasks.
· label `tab:component-transfer` · paper.tex L785 · 正文引用：§4.3 Component Composability (L991)

## 表 6 · 第 9 页 · `figures/tab-06.png`
**caption**：Table 6. Source-task composition on LIBERO-Long, all action components evaluated with LIBERO-Long video predictor.
· label `tab:component-source` · paper.tex L875 · 正文引用：§4.3 Component Composability (L987)；§4.3 Component Composability (L991)

## 表 7 · 第 9 页 · `figures/tab-07.png`
**caption**：Table 7. Local-context FDM prediction on counterfactual transi- tions. MSE values are reported in units of 10−3. Outcome accuracy measures identification of the matching realized future by RGB MSE among K same-state outcomes.
· label `tab:fdm` · paper.tex L916 · 正文引用：§4.4 Action-Conditioned Forward Dynamics (L1018)

## 表 8 · 第 16 页 · `figures/tab-08.png`
**caption**：Table 8. Data used for causal robot-video pretraining.
· label `tab:pretraining-corpus` · paper.tex L1236 · 正文引用：§B.1 Pretraining Corpus (L1308)

## 表 9 · 第 16 页 · `figures/tab-09.png`
**caption**：Table 9. Scale of LIBERO-Long-CF and the source LIBERO-Long demonstration corpus.
· label `tab:libero-cf-scale` · paper.tex L1364

## 表 10 · 第 17 页 · `figures/tab-10.png`
**caption**：Table 10. Intervention composition of LIBERO-Long-CF. Cat- egories denote generation recipes and may induce overlapping physical effects.
· label `tab:libero-cf-composition` · paper.tex L1403 · 正文引用：§C.1 Scale and Intervention Coverage (L1401)

## 表 11 · 第 17 页 · `figures/tab-11.png`
**caption**：Table 11. Physical interaction statistics for LIBERO-Long-CF. Categories overlap.
· label `tab:libero-cf-interaction` · paper.tex L1458 · 正文引用：§C.2 State and Interaction Coverage (L1453)

## 表 12 · 第 17 页 · `figures/tab-12.png`
**caption**：Table 12. Effect of video-backbone initialization on closed-loop LIBERO-Long success. Downstream architecture and training are held fixed within each interaction program.
· label `tab:init-program-ablation` · paper.tex L1513 · 正文引用：§D.1 Effect of Video-Backbone Initialization (L1505)

## 表 13 · 第 17 页 · `figures/tab-13.png`
**caption**：Table 13. Effect of the Mixture-of-Transformers architecture on closed-loop LIBERO-Long success. All variants use robot-video- pretrained initialization.
· label `tab:mot-ablation` · paper.tex L1541 · 正文引用：§D.2 Effect of the Mixture-of-Transformers Ar (L1686)

## 表 14 · 第 18 页 · `figures/tab-14.png`
**caption**：Table 14. Policy and dynamics accuracy on LIBERO-Long. LC-IDM and LC-FDM are independently trained specialist checkpoints; the multi-objective model trains policy, IDM, and FDM within a single checkpoint. Lower is better for MSE and IDM error; higher is better for success and SSIM.
· label `tab:external-dynamics` · paper.tex L1566 · 正文引用：§E External Dynamics Comparison (L1697)
