# Video Prediction Policy 2: Predict Better, Act Better

## Metadata

- Authors: Yanjiang Guo, Haodong Yan, Zhide Zhong, Zhongru Zhang, Qingyuan Yang, and 13 others
- Affiliations: Robotera, Tsinghua University, HKUST (GZ), UC Berkeley, Shanghai Jiao Tong University
- Venue/year: arXiv:2610.10270v2, revised October 8, 2026; preprint
- Source: [arXiv](https://arxiv.org/abs/2610.10270) · [project](https://robert-gyj.github.io/video-prediction-policy-2) · [official code](https://github.com/roboterax/video-prediction-policy-2)
- Local: [PDF](../papers/video-prediction-policy-2/paper.pdf) · [converted Markdown](../papers/video-prediction-policy-2/paper.md) · [close-reading notes](../papers/video-prediction-policy-2/精读笔记.md) · [detailed Chinese tutorial](video-prediction-policy-2-tutorial.md)

## Research Question

Can a world action model retain broad manipulation video priors while producing instruction-faithful future motion and useful robot actions? Generic video generators may invent incorrect motion, while naive action training may damage video generalization. See paper §§1–3 in the [local LaTeX text](../papers/video-prediction-policy-2/paper.tex).

## Method and Key Innovation

VPP2 continues training Wan2.1-I2V-14B on complete 1–12 second manipulation events with captions that identify the acting end effector, target object, motion, and viewpoint. It then trains on fixed-duration video chunks and applies consistency distillation for one-step video representation generation. A separate action DiT joins the video DiT through mixture-of-transformers attention and uses cached video features to denoise an action chunk. During early action training, the video backbone is frozen and adapted through LoRA. Cross-dataset workspace and end-effector transforms align action coordinates. See [Figure 2](../papers/video-prediction-policy-2/figures/fig-02.png), [Figure 4](../papers/video-prediction-policy-2/figures/fig-04.png), and paper §§2–3.

The useful idea is the **semantic and temporal alignment**: first align a detailed instruction with the full visual evolution of one subtask, then convert that prior to a fixed-duration representation suitable for short action chunks. This may avoid learning short-horizon correlations between ambiguous captions and actions.

## Data and Training

Data sources span single-arm, bimanual, mobile/humanoid, human-hand, and filtered general videos; the paper reports more than 20 robot embodiments and says bimanual/egocentric data account for over 80% of the total. It does not report a verifiable total number of hours or clips, nor full source mixture proportions. [Table 1](../papers/video-prediction-policy-2/figures/tab-01.png) lists the sources.

Stage 1 uses video flow matching at 49 frames and 416×240 resolution for 30,000 steps, batch size 1,024. Stage 2 predicts fixed horizons of two seconds for human hands and eight seconds for robots, then distills the video model to one forward pass. Stage 3 adds an approximately 0.9B action expert in the paper's generic configuration. Public LIBERO evaluation instead uses a 32×7 action chunk, ten Euler steps, and executes ten actions; RoboDojo uses 32×16, ten steps, and executes 24. These are benchmark-specific recipes, not interchangeable global settings. See paper §3 and the official [LIBERO](https://github.com/roboterax/video-prediction-policy-2/blob/main/docs/libero.md) and [RoboDojo](https://github.com/roboterax/video-prediction-policy-2/blob/main/docs/robodojo.md) guides.

## Experiments

| Evaluation | VPP2 | Relevant comparison and scope |
| --- | ---: | --- |
| Video instruction following, human / robot | 0.80 / 0.90 | Cosmos3-64B: 0.70 / 0.78; 50 image–instruction pairs in each group, primarily model-judged. Paper Table 2. |
| Real ALOHA unseen tasks | 58.5% mean success | π0.5: 40.0%; Fast-WAM: 20.5%. The robot embodiment was seen in training. Paper Figure 8. |
| LIBERO-ID / Pro / OOD | 98.8% / 45.0% / 63.9% | All are after standard-suite post-training; Table 3. |
| RoboDojo simulation | 39.26 score / 32.26% success | Benchmark-specific training; baseline values from the September 2026 leaderboard. Table 4. |

The abstract's 11.0 percentage point gain is the mean of the human and robot video comparisons (0.85 versus 0.74); the 18.5 point gain is the ALOHA mean versus π0.5 (58.5 versus 40.0).

## Limitations

The 100-case video instruction evaluation is relatively small and uses a model judge for the main metric. The reported gains cannot isolate event segmentation from caption detail, source mixture, and post-training. The paper does not disclose total video hours, full mixture weights, or a complete public recipe for event-level pretraining. Released benchmark configurations differ from the generic paper latency/path: the paper reports five action denoising steps and roughly 0.22 seconds per chunk, while released LIBERO/RoboDojo evaluations use ten steps and different action experts. Video representations used by action inference need not be decoded into full RGB video on every control call.

## Application to My Robot

Start with a table-top task containing lookalike targets and collect synchronized main/wrist RGB, robot state, calibrated end-effector poses, actions, and explicit subtask captions. Compare broad captions and fixed clips with detailed captions and complete events on target identity, contact timing, and task success. If prediction improves, attach an action expert while initially freezing the video backbone; keep an action-only baseline and execute chunks with closed-loop replanning. Expected benefit is less target confusion and improved generalization to new object/layout combinations. Key risks are wrong visual priors, incorrect coordinate alignment, expensive annotation and GPU requirements, and inference latency exceeding the control budget.
