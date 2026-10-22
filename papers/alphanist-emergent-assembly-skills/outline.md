# 大纲 · AlphaNIST: Emergent Assembly Skills from Binary Task Rewards

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L9 摘要
- L24–92 1 Introduction
- L93–178 2 Related Work
  - L95–121 2.1 Scalable Learning for Contact-Rich Assembly
  - L122–146 2.2 Multi-Task Reinforcement Learning
  - L147–178 2.3 Learning-Based Robot Assembly
- L179–209 3 Problem Formulation
  - L181–209 3.1 Task Definition and MDP
- L210–628 4 Method
  - L212–385 4.1 AlphaNIST Training Framework
  - L386–431 4.2 Reset Coverage and Experience Allocation
  - L432–559 4.3 Binary Full-Assembly Objective
  - L560–618 4.4 Shared Policy and Robot Control
  - L619–628 4.5 Distributed Training and Scale
- L629–740 5 Experiments
  - L688–710 5.1 Assembly-Pair Heterogeneity Enables Learning
  - L711–718 5.2 Sparse Binary Task Rewards Benefit from Scale
  - L719–729 5.3 Emergent Strategies over Short Horizons
  - L730–740 5.4 Emergent Strategies over Long Horizons
- L741–750 6 Limitations
- L751–761 7 Conclusion

## 公式（8 个，按出现顺序；L 后面是所在小节）

- L190 §3.1 Task Definition and MDP：\mathcal{M}=(\mathcal{S},\mathcal{A},p,r,\gamma,T,\rho),
- L198 §3.1 Task Definition and MDP `eq:objective`：J(\theta) = \mathbb{E}_{\rho,p,\pi_\theta} \left[ \sum_{t=0}^{T-1}\gamma^t r_t \right].
- L377 §4.1 AlphaNIST Training Framework：\begin{array}{r@{\quad}l} \textbf{Reset bank:} & \textit{Which states are available?}\\ \textbf{Beta sampling:…
- L391 §4.2 Reset Coverage and Experience Allocation：\mathcal{D}_{\mathrm{reset}} =\{(e_i,\bar{s}_i)\}_{i=1}^{M}.
- L418 §4.2 Reset Coverage and Experience Allocation `eq:beta-sampling`：q_i\propto \varepsilon_q+ \sqrt{\hat{p}_i(1-\hat{p}_i)},\qquad i=1,\ldots,M,
- L440 §4.3 Binary Full-Assembly Objective `eq:sparse-reward`：r_t^{\mathrm{succ}} = \begin{cases} 1, & d_{\mathrm{asm}}^e(s_{t+1})<\epsilon,\\ 0, & \text{otherwise}. \end{c…
- L455 §4.3 Binary Full-Assembly Objective `eq:full-reward`：r_t = \underbrace{r_t^{\mathrm{succ}}}_{\text{binary task reward}} - \underbrace{c\left(\lVert a_t\rVert_2^2 +…
- L656 §5 Experiments `eq:reward-ablation`：r_t^{\mathrm{dense}} = r_t + c_2 r_t^{\mathrm{reach}} + c_3 r_t^{\mathrm{align}}, \qquad c_2,c_3 \geq 0,

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
