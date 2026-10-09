# OpenWAM: An Open Framework for Composable World-Action Models

- **Authors:** Heng Yu, David D. Yuan, Juze Zhang, Changan Chen, Yao Feng, Michelle Baldonado, Steve Cousins, Li Fei-Fei, Jiajun Wu, Ehsan Adeli.
- **Venue/year:** arXiv:2610.07922v1, 2026 (preprint).
- **Institution:** Stanford University.
- **Sources:** [paper](https://arxiv.org/abs/2610.07922), [project](https://openwam.stanford.edu/), [official code](https://github.com/OpenWAM/OpenWAM).
- **Local paper:** [PDF](../papers/openwam/paper.pdf), [converted Markdown](../papers/openwam/paper.md), [LaTeX source](../papers/openwam/source/main.tex), [Figure 1](../assets/openwam/figure-1.png).

## Research Question and Solved Problem

How should predicted future video and robot actions interact, and can a separately trained dynamics model be reused when the visual predictor changes? Existing world-action models change backbones, data, objectives, and inference procedures at once, making architecture comparisons difficult. Successful demonstrations also cover only a narrow range of action outcomes. OpenWAM supplies a common experimental framework and additional counterfactual transitions to study both questions (paper §§1, 3).

## Method and Key Innovation

1. Initialize from Wan2.2-5B and train a chunk-causal video predictor on 14.64k hours of source video without action labels. Future chunks see past chunks, while tokens within a chunk are denoised together (paper §3.2, Appendix B).
2. Add a 2B action expert through a Mixture-of-Transformers (MoT). Both streams have their own layers and exchange information through attention. With the same backbone and objective, compare **video then action (VTA)**, **action then video (ATV)**, **joint**, and **decoupled** generation (paper §3.3, Figures 1–3).
3. Train independent local inverse dynamics (IDM: current image/state + supplied future video → actions) and forward dynamics (FDM: current image/state + supplied actions → future video). These components receive no task instruction or pre-start history. Their common trajectory interface allows a task-adapted video predictor to use a frozen IDM (paper §3.4).
4. Restore LIBERO simulator states and execute alternative action sequences, including unsuccessful ones, to build 32,000 counterfactual segments. Train IDM/FDM on demonstration-only, counterfactual-only, or 60% counterfactual + 40% demonstration transitions. The loss treats each branch as an individual sample; it does not explicitly contrast branches (paper §4.1, Appendix C).

The policy uses a 16-step action chunk aligned to four latent video frames. In LIBERO each action has 7 dimensions: end-effector position (3), axis-angle rotation (3), and gripper (1). The proprioceptive input has 8 dimensions. At inference, the policy executes the full chunk and then replans (Appendix A). The method uses latent flow matching for both video and action targets (paper §3.3).

## Experiments and Evidence

| Experiment | Result | What it supports |
| --- | --- | --- |
| Four LIBERO suites | VTA mean success 98.6%; LIBERO-Long 97.8% | The framework yields a strong closed-loop policy (Table 3). |
| Video initialization ablation | VTA LIBERO-Long: original Wan2.2 68.4%, robot-video-pretrained 97.8% | Robot-video training **and causal adaptation together** provide a 29.4-point gain; their individual effects were not isolated (Table 12). |
| Real bimanual FR3 | VTA mean 92.1% over toast, Rubik's cube, and cup sorting | Shows native policy control beyond simulation, on three tasks (Table 4). |
| Frozen IDM transfer to four LIBERO-90 tasks | Local IDM: demo-only 21.5%, mixed 84.0%; full-context mixed 47.0% | Broader transition data and a local input boundary improve component reuse in this setup (Table 5). |
| Counterfactual FDM test | Correct outcome among 16 alternatives: demo-only 21.1%, counterfactual-only 71.3% | Alternative actions improve action-conditioned future discrimination (Table 7). |

For the transfer experiment, each target-task video predictor was adapted with target demonstrations **including action labels**. The 84.0% figure measures reuse of a frozen IDM, not zero-shot transfer of the entire system (paper §4.3).

## Limitations

- The composability evidence is primarily from LIBERO simulation; equivalent frozen-component transfer on physical robots remains open (paper §5).
- The counterfactual data depends on simulator state restoration. A physical robot needs a different way to collect diverse safe transitions (paper §3.4, Appendix C).
- The FDM evaluation is local and short-horizon; it does not establish long-horizon planning performance (paper §5).
- The [official release](https://github.com/OpenWAM/OpenWAM) currently provides framework code and video-pretrained weights. Policy checkpoints and OpenWAM datasets are described as being prepared for release, limiting immediate reproduction of the paper's full policy results.
- Four program comparisons share the main setup, but the best program can depend on task and compute budget; success rates alone do not measure inference latency.

## Practical Robotics Impact

The most reusable idea is a clean boundary between *deciding what should happen* (video prediction) and *turning a proposed visual future into motor commands* (local IDM). A second useful practice is collecting failed and perturbed action outcomes for dynamics training, instead of discarding all non-successful episodes. The paper also provides a controlled way to test whether explicit future prediction benefits a specific robot task over a decoupled action stream.

## Question Analysis

### Continue: ② Architecture

In [Figure 2](../assets/openwam/figure-2.png), the roughly 5B video expert starts from Wan2.2-5B and robot-video pretraining; the roughly 2B action expert starts from width-adapted video layers. Each stream keeps its own normalization, QKV projections, and FFN. Masked packed attention exchanges allowed information, while separate text cross-attention conditions both streams. Both experts are updated in downstream training (paper §3.3, Appendix A.1–A.2).

For LIBERO, two 128×128 RGB views and an 8D proprioceptive state condition four future video latent frames and a 16×7 action chunk. One latent frame aligns with four action steps. The entire chunk is executed before replanning; video and action sampling each use 20 denoising steps (Appendix A.1, A.4). [Figure 3](../assets/openwam/figure-3.png) distinguishes VTA (video then action), ATV (reverse order), Joint (mutual noisy-future attention), and Decoupled (no future cross-modal attention). Its IDM/FDM rows are separately trained local dynamics programs without task language or pre-start history. The real bimanual setup uses a separate 20D action interface (Appendix A.5).

### Continue: ③–⑦ Training, Data, Information Flow, Example, and Results

The [detailed reading notes](../papers/openwam/精读笔记.md) walk through every stage. Video and action use flow matching with `Zτ=(1−τ)ε+τZ*`, target velocity `Z*−ε`, and equal loss weights. The code uses the equivalent reversed convention `σ=1−τ` and target `ε−Z*`. VTA trains its second stage with recorded future video and conditions on generated video at inference. Downstream optimization uses AdamW, a 1e−5 learning rate, effective batch 10, and 10,000 steps. The video pretraining stage uses 32 B200 GPUs for 14 days (paper Appendices A–B; official `flow_schedule.py` and `packed_training.py`).

A LIBERO sample comprises a task instruction, two 128×128 RGB views, an 8D current robot state, a future 16×7 delta-OSC action chunk, and four aligned future VAE video latent frames. Each view encodes to 8×8×48 per frame; concatenation yields 8×16×48. Four actions align with each latent frame, and the action chunk spans 0.8 seconds at 20 Hz. LIBERO-Long-CF adds 32,000 simulator-executed alternative-action segments, each with 128 controls and 129 synchronized observations (paper Appendices A, C). The official dataset has not yet been released; sample values in the detailed notes are explicitly illustrative.

At inference, VTA follows `new observation/state/instruction → 20 video denoising steps → four future VAE latent frames → 20 action denoising steps → execute 16 actions → observe again`. Video uses CFG 5; action uses no CFG. The history window retains at most 15 chunks. The next call uses the newly measured image, rather than treating the earlier imagined future as observed. A frozen IDM accepts generated VAE video latents, not video-transformer hidden state or KV cache. The reported 84.0% transfer still uses a target video predictor adapted with target demonstrations that include action labels (paper Table 5, Appendix A).

## Application to My Robot

- **Integration idea:** Start with a fixed camera and robot state interface. Train or adapt a task-conditioned video predictor for one manipulation skill, then train a local IDM on `(current image, proprioception, future images, executed actions)` transitions. Compare demonstration-only training with additional perturbed or failed transitions before considering a full OpenWAM policy.
- **Required sensors and compute:** Synchronized RGB views, end-effector pose, gripper state, action logs, and a GPU for latent video modeling. The paper's full backbone pretraining used 32 B200 GPUs for 14 days (Appendix B); a small local prototype should reuse available weights and avoid that stage.
- **Expected benefit:** Better reuse of an action component when the desired visual outcome changes, and better coverage of recovery motions than successful demonstrations alone.
- **Risks:** Imagined video may be physically inconsistent; a frozen IDM may fail under a new embodiment or camera geometry; unfiltered perturbations can be unsafe on hardware. Evaluate in simulation first and log action-conditioned outcomes before real-robot deployment.
