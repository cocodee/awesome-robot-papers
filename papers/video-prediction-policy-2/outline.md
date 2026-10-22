# 大纲 · Video Prediction Policy 2: Predict Better, Act Better

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L8 摘要
- L23–34 1 Introduction
- L35–123 2 Data Processing Pipeline
- L124–279 3 VPP2: A Generalist Policy with Zero-shot Capability
  - L129–257 3.1 Video Prediction Model Training Pipeline
  - L258–264 3.2 Action Modeling
  - L265–279 3.3 VLM for High-level Planning.
- L280–496 4 Experiments
  - L286–345 4.1 Video Prediction Quality Analysis
  - L346–496 4.2 Policy Performance Analysis
- L497–505 5 Related Works
- L506–511 6 Conclusion
- L512–514 Acknowledgments
- L515–517 AI Use Statement
- L518–523 Reproducibility Statement
- L522 —— 附录 ——
- L524–600 A Dataset Process Details
  - L559–573 A.1 Video Captioning.
  - L574–600 A.2 Unified Action Space
- L601–610 B More Video Prediction Results
- L611–694 C Detailed Benchmark Results
  - L612–639 C.1 Detailed LIBERO Results
  - L640–694 C.2 Detailed RoboDojo Results

## 公式（6 个，按出现顺序；L 后面是所在小节）

- L140 §3.1 Video Prediction Model Training Pipeline：\mathbf{y}_{\mathrm{event}} = \left( o_0, o_{\lfloor T/N \rfloor}, o_{\lfloor 2T/N \rfloor}, \ldots, o_T \righ…
- L156 §3.1 Video Prediction Model Training Pipeline：\mathbf{x}_s = (1-s)\boldsymbol{\epsilon} + s\mathbf{x}_1, \qquad \boldsymbol{\epsilon} \sim \mathcal{N}(\math…
- L167 §3.1 Video Prediction Model Training Pipeline `eq:video_fm`：\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{(\mathbf{x}_1,c),\,\boldsymbol{\epsilon},\,s} \left[ \left\| v…
- L211 §3.1 Video Prediction Model Training Pipeline：\mathbf{y}_{\mathrm{chunk}}^{(t)} = \left( o_t, o_{t+\lfloor \delta \rfloor}, o_{t+\lfloor 2\delta \rfloor}, \…
- L232 §3.1 Video Prediction Model Training Pipeline：\mathcal{L}_{\mathrm{CD}} = \mathbb{E} \left[ \lambda(s,s') \left\| F_\theta(\mathbf{x}_s,s,c) - \operatorname…
- L596 §A.2 Unified Action Space `eq:coordinate_alignment`：\widetilde{T}_d = A_d T_d B_d,

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
