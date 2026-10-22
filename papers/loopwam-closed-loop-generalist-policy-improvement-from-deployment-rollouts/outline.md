# 大纲 · LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L14 摘要
- L29–74 1 Introduction
- L75–95 2 Related Work
- L96–242 3 Method
  - L115–159 3.1 Joint World--Action Modeling
  - L160–224 3.2 Quality-Aware Learning from Mixed Trajectories
  - L225–242 3.3 Closed-Loop Self-Improvement
- L243–460 4 Experiments
  - L246–255 4.1 Implementation Details
  - L256–374 4.2 Benchmark Experimental Setup
  - L375–393 4.3 Benchmark Results
  - L394–425 4.4 Closed-Loop Improvement from Deployment
  - L426–460 4.5 Ablation Study
- L461–476 5 Conclusion
- L472 —— 附录 ——
- L477–637 A Training and Data Processing Details
  - L480–514 A.1 Trajectory-Quality Annotations
  - L515–543 A.2 Training Details
  - L544–578 A.3 Table30-V2 Subtask Segmentation
  - L579–637 A.4 Subtask Switching Examples
- L638–649 B RoboChallenge Table30-V2 Leaderboard
- L650–680 C Failure Recovery and Iterative Execution
- L681–715 D Qualitative Future Observation Prediction
- L716–818 E Representative Robot Platforms and Tasks

## 公式（8 个，按出现顺序；L 后面是所在小节）

- L122 §3.1 Joint World--Action Modeling `eq:quality_joint`：p_\theta(A_t,Z_t\mid o_t,s_t,\ell,q),
- L132 §3.1 Joint World--Action Modeling `eq:flow_path`：X_m^{\sigma_m}=(1-\sigma_m)X_m+\sigma_m\epsilon_m, \qquad \epsilon_m\sim\mathcal N(0,I),\quad m\in\{v,a\}.
- L143 §3.1 Joint World--Action Modeling `eq:joint_mask`：M_{(O,V,A)}= \begin{pmatrix} 1 & 0 & 0\\ 1 & 1 & 1\\ 1 & 1 & 1 \end{pmatrix},
- L174 §3.2 Quality-Aware Learning from Mixed Trajec `eq:source_noise`：\begin{aligned} d=E:&\quad \sigma_v\sim\operatorname{Beta}(7,1), &&\sigma_a\sim\mathcal P_0,\\ d=R:&\quad \sig…
- L205 §3.2 Quality-Aware Learning from Mixed Trajec `eq:modality_loss`：\ell_{m,i}=\omega(\sigma_{m,i}) \left\|v_{\theta,i}^{m}-(\epsilon_{m,i}-X_{m,i})\right\|_{\mathrm{valid}}^2,
- L213 §3.2 Quality-Aware Learning from Mixed Trajec `eq:quality_loss`：\mathcal L_{\mathrm{LoopWAM}} =\underbrace{\frac{1}{B}\sum_{i=1}^{B}\ell_{v,i}}_{\text{world supervision}} +\u…
- L229 §3.3 Closed-Loop Self-Improvement `eq:steered_policy`：\pi_\theta(A_t\mid o_t,s_t,\ell;q^\star) =\int p_\theta(A_t,Z_t\mid o_t,s_t,\ell,q^\star)\,\mathrm d Z_t.
- L530 §A.2 Training Details：\begin{aligned} g(\sigma)&=\exp\!\left[-2(\sigma-\tfrac12)^2\right]-e^{-1/2},\\ \omega(\sigma)&=\frac{g(\sigma…

图表的页码、caption、在哪节被引用：见 `figures-auto/index.md`。
