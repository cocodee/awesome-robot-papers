# LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts

## Metadata

- Authors: Wenxuan Guo, Yingping Liang, Zhaoguo Wang, Ziyuan Li, Angyuan Ma, Zhenyu Wu, Chengkun Wang, Bingyao Yu, Ze Chen, Borui Zhang, Xiuwei Xu, Meng Zhang, Erjin Zhou, Jiwen Lu
- Institutions: Tsinghua University, Dexmal, Loopeva
- Venue/year: arXiv preprint, 2026; arXiv:2610.18873v2, revised 15 October 2026
- Source: https://arxiv.org/abs/2610.18873
- Project: https://loop-wam.github.io/
- Code: https://github.com/loop-wam/LoopWAM
- Local PDF: [../papers/loopwam-closed-loop-generalist-policy-improvement-from-deployment-rollouts/paper.pdf](../papers/loopwam-closed-loop-generalist-policy-improvement-from-deployment-rollouts/paper.pdf)
- Converted Markdown (from the official arXiv HTML for readable text and tables): [../papers/loopwam-closed-loop-generalist-policy-improvement-from-deployment-rollouts/paper.md](../papers/loopwam-closed-loop-generalist-policy-improvement-from-deployment-rollouts/paper.md)

## Research Question

How can a generalist manipulation policy improve after deployment using successful, suboptimal, and failed robot rollouts? Imitating every rollout teaches bad actions; keeping only successes throws away observations of what bad actions physically caused. LoopWAM tries to retain the latter information while controlling the former.

## Method and Key Innovation

LoopWAM jointly models an action chunk and future video latents, conditioned on the current image, robot state, task instruction, and a numeric trajectory-quality score. Its video stream starts from Wan2.2-TI2V-5B; a separate action DiT has hidden dimension 1024. Video and action tokens exchange information through bidirectional attention during the same denoising process. The current observation stays fixed. At deployment, both future video and actions are sampled together, but the robot executes the actions. This is joint future generation, not an explicit search over candidate actions with a separate world-model evaluator (§3.1–3.3).

Three training choices make mixed-quality data usable (§3.2, Eq. 4–6):

1. **Source-dependent noise:** expert samples use strongly corrupted video (video noise from Beta(7,1)) and a base action-noise distribution. Rollout samples use low action noise (Beta(1,7)) and base video noise. In the latter case, the recorded action remains legible while the model learns its observed video consequence.
2. **Quality steering:** a numeric score is appended to the task instruction as `Quality: q`. Experts receive a score above all rollout scores; inference always requests that expert score. Scores can be assigned per episode or more coarsely per policy checkpoint, with failures given the minimum.
3. **Quality-weighted action loss:** all trajectories keep their video loss. Expert actions get full weight, suboptimal actions get reduced weight, and failed actions get zero direct imitation loss. A failed sample can still affect shared representations through video prediction and joint attention; zero action weight does not mean zero training influence.

The loop begins with an expert-trained model, deploys it, grades complete trajectories, retrains on demonstrations plus all accumulated rollouts, and repeats. The same objective can ingest rollouts from other policies. This is supervised flow matching over graded experience, not online reinforcement learning with a learned reward (§3.3).

The released RoboTwin model config maps quality scores 1–5 to action-loss weights `0, 0, 0.3, 0.6, 1.0` (`configs/model/fastwam_joint_mixed_quality_weighted.yaml`). Its model implementation samples separate video and action timesteps and masks first-frame-to-action attention (`src/fastwam/models/wan22/fastwam_joint_mixed_quality_weighted.py` and `fastwam_joint_mixed.py`). These are implementation details of the released configuration; the paper states the general weighting rule.

## Data and Training Details

- Each training segment contains 64 actions and nine RGB frames: the present frame plus one future frame every eight control steps. Multiple camera views are stitched into a single image. Robot state and actions use statistics from expert data (§4.1, Appendix A.2).
- On Table30-V2, joint targets are relative to the joint state at the start of the chunk, while gripper commands remain absolute. Padded targets are excluded from both losses (Appendix A.2).
- Table30-V2 covers 30 real tasks on ALOHA, DOS-W1, ARX5, and UR5, with one multitask model per embodiment. Each of three rounds collects about 100 trajectories per task; earlier rollouts remain in training (§4.2).
- RoboTwin 2.0 uses 27,500 expert demonstrations and 22,500 rollouts across 50 tasks, collected from expert-trained LoopWAM, X-VLA, and π0.5. Collection and evaluation use different random seeds (§4.2).
- For real tasks, human episode scores are on a 1–10 rollout scale, failures are set to 1, and experts to 12. In RoboTwin, successful rollouts get a checkpoint-level score of 3 or 4, failures 1, and experts 5 (Appendix A.1).

## Experiments

| Evaluation                                          | Reported result                                                                                              | What it supports                                                                           |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| RoboChallenge Table30-V2, real robots               | Overall success 23.67% → 28.00% → 37.67% → 43.33% over three deployment/retraining rounds; final score 56.80 | Repeated improvement on the same four embodiments and 30 tasks (§4.4, Fig. 3)              |
| Shirt folding, real DOS-W1 after task post-training | 13.20% → 32.54% → 55.56% over two rounds                                                                     | Improvement in a deformable-object task, after a task-specific expert stage (§4.4, Fig. 3) |
| RoboTwin 2.0, simulation                            | 94.5% average success versus 92.8% for AHA-WAM and 93.6% for LingBot-VA 2.0                                  | Strong mixed-data multitask benchmark performance (Table 2)                                |
| RoboCasa365, simulation                             | 49.5% overall versus 46.6% for ABot-M0.6; 14.9% on held-out composite tasks                                  | Some transfer, with substantial headroom on unseen compositions (Table 3)                  |

The RoboTwin ablation is especially informative: without quality steering and weighted rollout action loss, average success is 72.3%; coarse steering alone reaches 92.7%, and adding weighted action supervision reaches 94.5% (Table 4). This directly supports the value of identifying data quality. The paper does not provide an equally direct ablation isolating every component of the joint video-action architecture or the source-dependent noise scheme.

## Limitations and Interpretation

- Real-world improvements are measured on the same benchmark tasks used to collect rollouts. They show iterative adaptation, not adaptation to entirely unseen real tasks.
- The best RoboCasa Composite-Unseen result is 14.9%; broad task-composition transfer remains difficult (Table 3).
- Whole-trajectory quality scores cannot distinguish a good recovery action inside an ultimately failed episode. Giving every failed action zero direct imitation loss may discard useful recovery behavior; this is an inference from the weighting rule, not an ablation result.
- Strong benchmark results are not a clean attribution to world modeling alone: the quality-steering ablation is large, while component-specific evidence for bidirectional consequence feedback is limited (Table 4).
- The method depends on paired, synchronized actions and future video, quality labels, and a large video generator. The official implementation uses Wan2.2-TI2V-5B and its released RoboTwin evaluation describes eight A100 GPUs, so direct replication is expensive. The paper does not give enough evidence to assume low-latency control on a small on-board computer.

## Application to My Robot

**Integration idea:** begin with a single tabletop manipulation task and a working imitation policy. Record every deployment episode with synchronized camera frames, joint state, commanded actions, instruction, and final outcome. Score complete episodes; keep failures for action-conditioned future prediction, but prevent failed actions from becoming direct action targets. Compare an expert-only baseline, quality-conditioned action imitation, and joint action/future-video learning under identical data and evaluation trials.

**Sensors and compute:** at least one calibrated RGB view, joint/gripper telemetry, reliable timestamps, episode reset/outcome logging, and a GPU for model training. Multiple camera views help when contact or grasp points are occluded. A full LoopWAM replica requires much more compute than a small task-specific latent or image predictor.

**Expected benefit:** more useful learning from failed deployments and potentially better recovery after off-demonstration states. **Risks:** incorrect quality labels, weak action–video alignment, video-model hallucination, high sampling latency, and imitation of suboptimal actions if the action weights are miscalibrated. Pilot with a small fixed evaluation set and measure success, recovery rate, and end-to-end action latency before adopting a joint generator.
