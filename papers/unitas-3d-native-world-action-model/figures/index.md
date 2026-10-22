# 图表索引

来源 `paper.pdf`（27 页）：图 11 张、表 13 张。全部裁剪拼在 `figures/_contact.png`，一次看完。

> 讲到哪张图就把那个 PNG 发给用户；讲之前自己先看一眼——caption 不会告诉你图是怎么排的。
> 裁得不对：`crop.py paper.pdf --page P --grid` 看带刻度的整页，再 `crop.py paper.pdf --page P x0 y0 x1 y1 -o figures/fig-NN.png` 重裁（坐标是页面比例 0–1）。

## 图 1 · 第 2 页 · `figures/fig-01.png`
**caption**：Figure 1: UNITAS is a 3D-native world action model. Observations, action flow, and scene flow share a metric frame within each prediction window, with a common representation across embod- iments. With 1.7B parameters, UNITAS achieves leading manipulation results among the compared methods and predicts action-conditioned scene trajectories.
· label `fig:physwam_overview` · paper.tex L98 · 源文件 `figures/unitas_overview.pdf` · 正文引用：§1 Introduction (L73)

## 图 2 · 第 4 页 · `figures/fig-02.png`
**caption**：Figure 2: UNITAS architecture and attention masks. Left: The point dynamics expert models both action and scene flows, while the action expert generates the end-effector action chunk. Scene flow generation is conditioned on clean demonstrated action flow during training and generated or supplied action flow at inference. Right: Colored/white cells indicate allowed/blocked attention. Policy-only inference omits both future action-flow and scene-flow tokens.
· label `fig:architecture, fig:attention_mask` · paper.tex L205 · 源文件 `figures/architecture.pdf` · 正文引用：§3 Methodology (L222)；§3.5 Model Architecture (L501)

## 图 3 · 第 6 页 · `figures/fig-03.png`
**caption**：Figure 3: Shared point-flow representations across data sources. Left: gripper/hand trajectories (purple) and scene trajectories (yellow–blue), with RGB insets. Right: RoboTwin end-effector XYZ error (mm). Thick curves show exponential moving averages (EMA) of the thin curves.
· label `fig:experiments:mixed_dataset_training` · paper.tex L458 · 源文件 `figures/mixed_dataset_training.pdf` · 正文引用：§4.2 Simulation Benchmarks (L668)

## 图 4 · 第 8 页 · `figures/fig-04.png`
**caption**：Figure 4: Qualitative real-robot rollouts on Organize Books and Pack the Ball. Numbered keyframes show task progression through precise placement and sequential manipulation.

## 图 5 · 第 9 页 · `figures/fig-05.png`
**caption**：Figure 5: Action-conditioned scene-flow predictions. Top: observed RGB images. Middle: ini- tial point clouds. Bottom: predicted endpoint point clouds and scene trajectories (color gradient), conditioned on recorded gripper trajectories (purple). Translucent robot meshes indicate the corre- sponding poses.
· label `fig:experiments:scene_flow_qualitative` · paper.tex L846 · 源文件 `figures/scene_flow_qualitative.pdf` · 正文引用：§5 Action-Conditioned World Modeling (L897)；§G.1 Scene Prediction in Simulation (L1554)

## 图 6 · 第 16 页 · `figures/fig-06.png`
**caption**：Figure 6: Representative observations and aligned geometry from pretraining data. Robot panels show RGB, depth where available, and scene points with robot overlays. VITRA shows egocentric RGB and hand landmarks.
· label `fig:app:dataset_visualization` · paper.tex L953 · 源文件 `figures/pretraining_datasets.pdf` · 正文引用：§A.1 Data Mixture and Temporal Sampling (L950)

## 图 7 · 第 23 页 · `figures/fig-07.png`
**caption**：Figure 7: Additional scene-flow visualizations (1/4): insertion, extraction, bimanual lifting, and block stacking.

## 图 8 · 第 24 页 · `figures/fig-08.png`
**caption**：Figure 8: Additional scene-flow visualizations (2/4): bowl and mug placement, articulated motion, and gravity-driven motion after object release.

## 图 9 · 第 25 页 · `figures/fig-09.png`
**caption**：Figure 9: Additional scene-flow visualizations (3/4): book, bottle, block, and bowl manipulation across LIBERO and RoboTwin.

## 图 10 · 第 26 页 · `figures/fig-10.png`
**caption**：Figure 10: Additional scene-flow visualizations (4/4): object placement, drawer opening and clos- ing, and microwave opening.

## 图 11 · 第 27 页 · `figures/fig-11.png`
**caption**：Figure 11: Zero-shot scene-flow predictions on real-world observations. The first four rows are from DROID and the last is from RH20T. Columns show observed RGB, initial points, and predicted midpoint and endpoint point clouds with scene trajectories (orange to purple) and ground-truth grip- per trajectories used for conditioning (magenta). No scene-trajectory ground truth is shown.

## 表 1 · 第 7 页 · `figures/tab-01.png`
**caption**：Table 1: Policy performance (%, ↑). Our 1.7B model is evaluated with and without mixed-dataset pretraining. Bold and underlined scores denote the best and second-best results, respectively. LIBERO-Plus ranks use one-decimal precision. Dashes denote unavailable results.
· label `tab:experiments:simulation` · paper.tex L585 · 正文引用：§4.2 Simulation Benchmarks (L647)；§4.2 Simulation Benchmarks (L659)；§C Detailed LIBERO-Plus Results (L1266)；§E Detailed RoboTwin Results (L1362)

## 表 2 · 第 8 页 · `figures/tab-02.png`
**caption**：Table 2: Quantitative comparison results of real-robot experiments (20 trials per task).
· label `fig:experiments:real_world, tab:experiments:real_world` · paper.tex L688 · 源文件 `figures/real_world_keyframes.pdf` · 正文引用：§4.3 Real-world Evaluation (L686)；§4.3 Real-world Evaluation (L683)

## 表 3 · 第 8 页 · `figures/tab-03.png`
**caption**：Table 3: LIBERO-Plus ablations without mixed-dataset pretraining. Checkmarks indicate enabled components. Success rates (%) are reported for each perturbation; Overall pools all 10,030 evalua- tion episodes.
· label `tab:experiments:libero_plus_ablation` · paper.tex L732 · 正文引用：§4.4 Ablation Study (L802)；§B.1 Evaluation without Depth Input (L1216)

## 表 4 · 第 9 页 · `figures/tab-04.png`
**caption**：Table 4: Action-conditioned scene prediction on RoboTwin. Errors are in cm (↓); Acc@1cm is in % (↑). DA3 and STv2 denote Depth Anything 3 and SpatialTrackerV2, respectively.
· label `tab:experiments:world_model` · paper.tex L860 · 正文引用：§5 Action-Conditioned World Modeling (L894)；§F.1 Action-Conditioned Scene Prediction (L1452)

## 表 5 · 第 17 页 · `figures/tab-05.png`
**caption**：Table 5: Pretraining trajectory sampling configuration. H and Hhist count future and historical intervals; duration is H/f in seconds. H + 1 includes the current anchor.
· label `tab:app:temporal` · paper.tex L985 · 正文引用：§A.1 Data Mixture and Temporal Sampling (L973)

## 表 6 · 第 18 页 · `figures/tab-06.png`
**caption**：Table 6: Held-out trajectory reconstruction errors of the frozen tokenizer (mm). Dashes indicate unavailable scene-flow ground truth.

## 表 7 · 第 18 页 · `figures/tab-07.png`
**caption**：Table 7: Model architecture. Parameter counts include the frozen tokenizer. Component Configuration Params. (M)

## 表 8 · 第 19 页 · `figures/tab-08.png`
**caption**：Table 8: Inference efficiency on an RTX 5090 D. Latency is measured per prediction chunk; Ns denotes the number of scene queries.
· label `tab:app:inference_efficiency` · paper.tex L1173 · 正文引用：§A.4 Inference Efficiency (L1159)

## 表 9 · 第 19 页 · `figures/tab-09.png`
**caption**：Table 9: Spatial grounding without depth input on LIBERO-Plus. Success rates (%, ↑) over 10,030 episodes. Routed PE and ground-truth depth PE use the same checkpoint.
· label `tab:app:missing_depth` · paper.tex L1219 · 正文引用：§B.1 Evaluation without Depth Input (L1214)

## 表 10 · 第 20 页 · `figures/tab-10.png`
**caption**：Table 10: LIBERO-Plus success rates (%, ↑) across seven perturbation types. Robot denotes initial- state perturbations.
· label `tab:experiments:libero_plus` · paper.tex L1270 · 正文引用：§C Detailed LIBERO-Plus Results (L1264)

## 表 11 · 第 20 页 · `figures/tab-11.png`
**caption**：Table 11: Detailed VLABench results (%). SR, PS, and IS denote success rate, progress score, and intention score, respectively (all ↑).

## 表 12 · 第 21 页 · `figures/tab-12.png`
**caption**：Table 12: Detailed RoboTwin 2.0 success rates (%, ↑). Clean and Rand. denote demo clean and demo randomized. All methods are evaluated over 100 episodes per task in each setting.

## 表 13 · 第 22 页 · `figures/tab-13.png`
**caption**：Table 13: Closed-loop action–scene consistency on RoboTwin. Predictions are compared with the scene evolution produced by executing the same model’s generated actions. Errors are in cm; Moving Acc@1cm is in %.
