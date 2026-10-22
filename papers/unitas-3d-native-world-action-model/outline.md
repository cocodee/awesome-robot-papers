# 大纲 · UNITAS: A 3D-Native World Action Model for Embodied Manipulation

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L9 摘要
- L23–150 1 Introduction
- L151–200 2 Related Work
- L201–544 3 Methodology
  - L225–256 3.1 Revisiting Video World Action Models
  - L257–293 3.2 3D-Native World Action Formulation
  - L294–396 3.3 World-Aligned Observations
  - L397–471 3.4 Physical-Time Point-Flow Representation
  - L472–544 3.5 Model Architecture
- L545–825 4 Policy Evaluation
  - L557–580 4.1 Experimental Setup
  - L581–674 4.2 Simulation Benchmarks
  - L675–794 4.3 Real-world Evaluation
  - L795–825 4.4 Ablation Study
- L826–910 5 Action-Conditioned World Modeling
- L911–935 6 Conclusion
  - L928–935 AI use statement
- L932 —— 附录 ——
- L936–1197 A Implementation and Training Details
  - L940–1011 A.1 Data Mixture and Temporal Sampling
  - L1012–1092 A.2 Physical-Time Trajectory Tokenizer
  - L1093–1154 A.3 Architecture and Optimization
  - L1155–1197 A.4 Inference Efficiency
- L1198–1255 B Spatial Grounding without Depth Input
  - L1209–1255 B.1 Evaluation without Depth Input
- L1256–1301 C Detailed LIBERO-Plus Results
- L1302–1357 D Detailed VLABench Results
- L1358–1444 E Detailed RoboTwin Results
- L1445–1546 F World Model Evaluation Details
  - L1448–1480 F.1 Action-Conditioned Scene Prediction
  - L1481–1546 F.2 Closed-Loop Action--Scene Consistency
- L1547–1631 G Additional Action-Conditioned Scene Predictions
  - L1550–1606 G.1 Scene Prediction in Simulation
  - L1607–1631 G.2 Transfer to Real-World Observations

## 公式（10 个，按出现顺序；L 后面是所在小节）

- L234 §3.1 Revisiting Video World Action Models `eq:video_wam`：p(a_{1:H}\mid o,\ell) =\int p(v_{1:T}\mid o,\ell)\, p(a_{1:H}\mid o,\ell,v_{1:T})\,dv_{1:T}.
- L243 §3.1 Revisiting Video World Action Models `eq:fastwam`：p_{\theta}(a_{1:H}\mid o,\ell) =p_{\theta}\!\left(a_{1:H}\mid z(o,\ell)\right), \qquad \mathcal L =\mathcal L_…
- L276 §3.2 3D-Native World Action Formulation `eq:physwam_factorization`：p_{\theta}(\mathbf A,\mathbf u,\mathbf S\mid\mathcal C,\mathbf q_0) = p_{\theta}(\mathbf A\mid\mathcal C)\, p_…
- L314 §3.3 World-Aligned Observations `eq:world_coordinate_map`：\mathbf P_{\mathrm{camera},i}(u,v) =\mathbf D_{t,i}(u,v)\,\mathbf K_i^{-1}[u,v,1]^\top, \qquad \begin{bmatrix}…
- L332 §3.3 World-Aligned Observations `eq:depth_position_embedding`：\mathbf E_{\mathrm{pos},t,i} =\operatorname{Enc}_{\mathrm{3D}}(\mathbf P_{\mathrm{world},i}), \qquad \widetild…
- L348 §3.3 World-Aligned Observations `eq:frustum_routing`：\begin{aligned} \alpha_m &=\operatorname{softmax}_{m} \left( \frac{(\mathbf W_q\mathbf f)^\top \mathbf W_k\bol…
- L375 §3.3 World-Aligned Observations `eq:position_distillation`：\mathcal L_{\mathrm{PE}} =\sum_{i=1}^{N_v} \mathbb E_{\mathcal R\in\mathcal V_i} \left\| \sum_{m=1}^{M}\alpha_…
- L434 §3.4 Physical-Time Point-Flow Representation `eq:physical_time_flowchunk`：\begin{aligned} \mathbf z_n &=\frac{1}{\sqrt H}\sum_{k=1}^{H} \left[(\mathbf 1+\mathbf a^{\mathrm{enc}}_k)\odo…
- L516 §3.5 Model Architecture `eq:training_objective`：\mathcal L =\lambda_{\mathrm A}\mathcal L_{\mathrm A} +\lambda_{\mathrm s}\mathcal L_{\mathrm{scene}} +\lambda…
- L1019 §A.2 Physical-Time Trajectory Tokenizer `eq:tokenizer_time_basis`：[\boldsymbol\phi_{\mathrm{time}}(\tau)]_j =\operatorname{sgn}(\tau)\, \sin\!\left[\frac{\pi}{2} \left|\frac{\t…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
