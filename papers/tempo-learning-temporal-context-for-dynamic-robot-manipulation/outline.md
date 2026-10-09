# 大纲 · TEMPO: Learning Temporal Context for Dynamic Robot Manipulation

行号指 `paper.tex`。读某一节：`sed -n '起,止p' paper.tex`（或用 Read 的 offset/limit）。

- L16 摘要
- L26–56 1 Introduction
- L57–68 2 Related Work
- L69–107 3 Motion Ambiguity and State Aliasing
- L108–193 4 \methodname
  - L122–150 4.1 TEMPO\textsubscriptMOT: Captures Object and Scene Dynamics
  - L151–164 4.2 TEMPO\textsubscriptACT: Resolves State Aliasing
  - L165–173 4.3 Plug-and-Play Temporal Integration
  - L174–193 4.4 Real-Time Deployment via Parallel Encoding
- L194–288 5 Experiments
  - L220–246 5.1 Experimental Setup
  - L247–288 5.2 Experimental Results
- L289–342 6 Analysis and Ablations
- L343–358 7 Conclusion
- L352 —— 附录 ——
- L359–370 Appendix
- L371–386 A Additional Failure Mode Analysis
- L387–408 B Experimental Setup Details
  - L392–396 B.1 Hardware Platform
  - L397–404 B.2 Evaluation Protocol
  - L405–408 B.3 Training Details
- L409–440 C Per-Task Failure Mode Breakdown
- L441–446 D Input Ablation
- L447–495 E Motion Encoder Selection

## 公式（2 个，按出现顺序；L 后面是所在小节）

- L124 §4.1 TEMPO\textsubscriptMOT: Captures Object  `eq:tempomot`：\mathbf{m}_t \;=\; \phi(o_{t-W+1:t}) \;=\; \operatorname{CrossAttn}\bigl(\mathbf{f}_t,\; \mathcal{F}_t\bigr),
- L155 §4.2 TEMPO\textsubscriptACT: Resolves State A `eq:joint-compaction`：\mathbf{c}_t=\bigl(\bar q^{(1)}_t,\dots,\bar q^{(K)}_t\bigr),\qquad \bar q^{(k)}_t=\frac{1}{L}\sum_{\tau\in B_…

图表的页码、caption、在哪节被引用：见 `figures/index.md`。
