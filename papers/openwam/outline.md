# 大纲 · OpenWAM: An Open Framework for Composable World-Action Models

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L31–77 1 Introduction
- L78–199 2 Related Work
  - L81–110 2.1 Visuomotor Policies and Predictive Control
  - L111–167 2.2 Video Foundations and World--Action Architectures
  - L168–199 2.3 Dynamics Learning Beyond Successful Demonstrations
- L200–596 3 Methodology
  - L218–274 3.1 World--Action Modeling Formulation
  - L275–301 3.2 An Open Causal Robot-Video Backbone
  - L302–432 3.3 Configurable Video--Action Interaction Programs
  - L433–596 3.4 Counterfactual Learning of Local-Context Dynamics Interfaces
- L597–1024 4 Experiments
  - L607–949 4.1 Experimental Setup
  - L950–975 4.2 Native Policy Performance
  - L976–1008 4.3 Component Composability
  - L1009–1024 4.4 Action-Conditioned Forward Dynamics
- L1025–1079 5 Discussion and Conclusion
- L1073 —— 附录 ——
- L1080–1294 A Implementation Details
  - L1085–1103 A.1 Model Architecture and Representation
  - L1104–1155 A.2 Downstream Training
  - L1156–1187 A.3 Video--Action Interaction Programs
  - L1188–1218 A.4 Inference and Closed-Loop Evaluation
  - L1219–1294 A.5 Real Robot Setup
- L1295–1339 B Robot-Video Pretraining
  - L1304–1317 B.1 Pretraining Corpus
  - L1318–1332 B.2 Causal Adaptation
  - L1333–1339 B.3 Training Compute
- L1340–1497 C LIBERO-Long-CF: Counterfactual Dynamics Data
  - L1356–1438 C.1 Scale and Intervention Coverage
  - L1439–1479 C.2 State and Interaction Coverage
  - L1480–1497 C.3 Representation for Local Dynamics Learning
- L1498–1691 D Ablations
  - L1499–1678 D.1 Effect of Video-Backbone Initialization
  - L1679–1691 D.2 Effect of the Mixture-of-Transformers Architecture
- L1692–1735 E External Dynamics Comparison
  - L1707–1717 E.1 Independent Dynamics Components
  - L1718–1735 E.2 Unified Policy and Dynamics Modeling

## 公式（14 个，按出现顺序；L 后面是所在小节）

- L222 §3.1 World--Action Modeling Formulation：\begin{aligned} O_t^- &= (o_{t-K_o}, \ldots, o_{t-1}), \\ A_t^- &= (a_{t-K_a}, \ldots, a_{t-1}), \\ O_t^0 &= o…
- L231 §3.1 World--Action Modeling Formulation：A_t^+ = (a_t, \ldots, a_{t+H-1}), \quad O_t^+ = (o_{t+1}, \ldots, o_{t+H}).
- L236 §3.1 World--Action Modeling Formulation：\mathcal C_t=(O_t^-,O_t^0,A_t^-,q_t,\ell).
- L244 §3.1 World--Action Modeling Formulation `eq:wam-factorizations`：\begin{aligned} p_{\mathrm{WAM}} ( O_t^+, A_t^+\mid\mathcal C_t) &= \underbrace{p( O_t^+\mid\mathcal C_t)}_{\m…
- L400 §3.3 Configurable Video--Action Interaction P `eq:flow-path`：Z_{P,\tau}=(1-\tau)\epsilon_P+\tau Z_P^\star,\quad u_P=Z_P^\star-\epsilon_P.
- L406 §3.3 Configurable Video--Action Interaction P `eq:shared-flow-objective`：\mathcal L_P = \mathbb E\!\left[ \left\| v_{\theta,P} \!\left( Z_{P,\tau}\mid c_P,\tau \right) -u_P \right\|_2…
- L445 §3.4 Counterfactual Learning of Local-Context `eq:strict-modeling-roles`：\begin{aligned} p_{\mathrm{IDM}}^{\mathrm{local}} &:= p( A_t^+ \mid O_t^+, O_t^0,q_t ),\\ p_{\mathrm{FDM}}^{\m…
- L506 §3.4 Counterfactual Learning of Local-Context `eq:dynamics-training-distribution`：\mathcal D_{\mathrm{dyn}} = (1-\eta)\mathcal D_{\mathrm{task}}^{\mathrm{loc}} + \eta\mathcal D_{\mathrm{cf}}, …
- L526 §3.4 Counterfactual Learning of Local-Context `eq:strict-dynamics-objectives`：\begin{aligned} \mathcal L_{\mathrm{LC\text{-}IDM}} &= \mathbb E\!\left[ \left\| v_{\theta_{\mathrm{ID}}} ( Z_…
- L570 §3.4 Counterfactual Learning of Local-Context `eq:strict-vta-composition`：\hat{O}_t^+ \sim p_\phi^{\mathrm{CVP}}(\cdot\mid\mathcal C_t), \quad \hat{A}_t^+ \sim p_{\theta_{\mathrm{ID}}}…
- L582 §3.4 Counterfactual Learning of Local-Context `eq:strict-atv-composition`：\hat{A}_t^+ \sim p_\psi^{\mathrm{VLA}}(\cdot\mid\mathcal C_t), \quad \hat{O}_t^+ \sim p_{\theta_{\mathrm{FD}}}…
- L1122 §A.2 Downstream Training：S_s(\sigma) = \frac{s\sigma}{1+(s-1)\sigma}, \qquad s_V=5.0,\quad s_A=1.0,
- L1132 §A.2 Downstream Training：w_P(\sigma) \propto \exp\!\left[-2\left(\sigma-\tfrac{1}{2}\right)^2\right] - e^{-1/2},
- L1148 §A.2 Downstream Training：\mathcal{L} = \mathcal{L}_{V} + \mathcal{L}_{A}.

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
