# LDA-1B: Scaling Latent Dynamics Action Model via Universal Embodied Data Ingestion

## Metadata

- Authors: Jiangran Lyu, Kai Liu, Xuheng Zhang, Haoran Liao, Yusen Feng, Wenxuan Zhu, Tingrui Shen, Jiayi Chen, Jiazhao Zhang, Yifei Dong, Wenbo Cui, Senmao Qi, Shuo Wang, Yixin Zheng, Mi Yan, Xuesong Shi, Haoran Li, Dongbin Zhao, Ming-Yu Liu, Zhizheng Zhang, Li Yi, Yizhou Wang, He Wang
- Source: https://arxiv.org/pdf/2602.12215
- arXiv: 2602.12215v1, 12 Feb 2026
- Local PDF: [../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.pdf](../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.pdf)
- Converted Markdown: [../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.md](../papers/LDA-1B-Scaling-Latent-Dynamics-Action-Model-via-Universal-Embodied-Data-Ingestion.md)
- Project page: https://pku-epic.github.io/LDA

## Research Question

The paper asks how robot foundation models can scale beyond behavior cloning on clean expert demonstrations. Its central claim is that heterogeneous embodied data, including noisy robot trajectories and actionless human videos, contains useful dynamics knowledge if each data type is assigned the right training role.

## Core Method

LDA-1B is a 1.6B-parameter unified world model trained with universal embodied data ingestion. It jointly learns policy prediction, forward dynamics, inverse dynamics, and visual forecasting. Instead of predicting future pixels, it predicts structured DINO latent features, reducing wasted capacity on appearance details. A multi-modal diffusion transformer jointly denoises action chunks and future visual latents while conditioning on VLM tokens, diffusion timestep, and task embeddings.

The authors also build EI-30K, a 30k+ hour embodied interaction dataset with real robot data, simulated robot data, human demonstrations with actions, and actionless human videos. High-quality trajectories supervise both policy and dynamics; low-quality trajectories supervise dynamics and forecasting; actionless videos supervise visual forecasting.

## Key Innovation

- Role-aware data ingestion: different data qualities are used for different objectives rather than filtered away.
- DINO latent dynamics: future visual states are represented in semantic latent space instead of pixel or VAE space.
- Unified multi-task training: policy, forward dynamics, inverse dynamics, and visual forecasting are trained in one model.
- Aligned hand-centric action space across robots and humans, supporting grippers and dexterous hands.

## Problems Solved

LDA-1B addresses the data bottleneck of robot foundation models. Behavior cloning mainly benefits from expert action-labeled demonstrations, while this approach can use imperfect and actionless embodied data to learn transferable physical dynamics.

It also improves robustness for contact-rich, dexterous, and long-horizon manipulation, where action consequences and temporal consistency matter more than static visual recognition.

## Evidence

On RoboCasa-GR1, LDA-1B reaches 55.4% success, outperforming GR00T-N1.6 at 47.6%, StarVLA at 47.8%, and GR00T-EI30k at 51.3%. Replacing VAE-style visual targets with DINO latents is a major factor: UWM variants using VAE latents remain near 14.2% to 20.0%.

The paper reports gains over π0.5 of up to 21% on contact-rich tasks, 48% on dexterous tasks, and 23% on long-horizon tasks. In mixed-quality finetuning, adding 30% low-quality trajectories improves LDA-1B by 10%, while π0.5 degrades.

## Limitations

The model requires large-scale data and heavy pretraining: 48 H800 GPUs, 400k iterations, and 4,608 GPU hours are reported. It depends on fixed DINO visual features and mostly egocentric camera viewpoints, which may limit transfer to new camera layouts or richer sensory inputs. The converted Markdown is text-only, so figures and tables should be checked against the original PDF when exact details matter.

## Application to My Robot

This paper is useful if my robot data is mixed-quality rather than perfectly curated. Instead of discarding failed or inefficient demonstrations, I can use them for dynamics or visual forecasting while reserving high-quality data for policy learning.

A practical adaptation path:

- convert all robot demonstrations into a unified LeRobot-style format;
- align action representation around end-effector deltas, gripper width, or hand keypoints;
- label data quality instead of deleting noisy trajectories;
- train a policy objective on high-quality episodes;
- train dynamics and future-latent prediction on broader mixed-quality data;
- evaluate whether DINO-latent prediction improves recovery, contact handling, and long-horizon consistency.

For my robot, the most immediate application is building a data ingestion pipeline that separates policy-quality data from dynamics-useful data. This should reduce data collection cost and make imperfect teleoperation logs valuable.

## Implementation Notes

Start small: test whether adding a DINO-latent future prediction loss improves a local manipulation policy before attempting a full 1B-scale model. The key engineering work is data normalization: camera timestamps, action frequency, end-effector coordinate frames, gripper or hand representation, and quality labels must be consistent.
