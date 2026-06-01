# Fast-WAM: Do World Action Models Need Test-time Future Imagination?

## Metadata

- Authors: Tianyuan Yuan, Zibin Dong, Yicheng Liu, Hang Zhao
- Source: https://arxiv.org/pdf/2603.16666
- arXiv: 2603.16666v2, 23 Mar 2026
- Local PDF: [../papers/Fast-WAM-Do-World-Action-Models-Need-Test-time-Future-Imagination.pdf](../papers/Fast-WAM-Do-World-Action-Models-Need-Test-time-Future-Imagination.pdf)
- Project page: https://yuantianyuan01.github.io/FastWAM/

## Research Question

World Action Models often generate future video frames before predicting robot actions. This paper asks whether that explicit test-time future imagination is actually needed, or whether the real value comes from video prediction as a training signal.

## Core Method

Fast-WAM keeps video co-training during training but removes future-video generation during inference. The model uses a pretrained video Diffusion Transformer backbone from Wan2.2-5B, a text encoder, a video VAE, and a separate action expert DiT. During training, it jointly optimizes action generation and future-video latent prediction with a flow-matching objective. During inference, it only encodes the current observation and language instruction once, then predicts an action chunk directly from the learned latent world representation.

## Key Innovation

The key innovation is the controlled separation of two usually entangled WAM factors:

- video co-training during training;
- explicit future video generation during inference.

Fast-WAM shows that the training-time video objective is more important than generating future frames at runtime. This turns WAM-style learning into a real-time direct policy interface.

## Problems Solved

Fast-WAM addresses high inference latency in imagine-then-execute WAMs. Existing systems often spend substantial time iteratively denoising future videos before actions can be produced. Fast-WAM removes that branch at inference and reports 190 ms latency, over 4x faster than slower imagine-then-execute variants in the paper.

It also improves data efficiency. On RoboTwin and LIBERO, Fast-WAM remains competitive without embodied pretraining, suggesting video co-training can provide useful physical and temporal structure even when large robot pretraining data is unavailable.

## Evidence

On RoboTwin, Fast-WAM reports 91.8% success, close to Fast-WAM-IDM at 91.3% and Fast-WAM-Joint at 90.6%. Removing video co-training drops performance to 83.8%.

On LIBERO, Fast-WAM reports 97.6% average success, close to Fast-WAM-Joint at 98.5% and Fast-WAM-IDM at 98.0%. Without video co-training, performance drops to 93.5%.

On a real-world towel-folding task, removing video co-training causes a major success-rate drop, while Fast-WAM keeps much lower latency than variants that generate future video.

## Limitations

The method still depends on a large video backbone and a 6B-parameter model, so deployment may require a high-end GPU or distillation. The real-world evaluation is focused on towel folding, so more tasks are needed to prove robustness across mobile manipulation, locomotion, tool use, and contact-rich assembly. The paper also leaves large-scale pretraining and model scaling as future work.

## Application to My Robot

Use this idea if the robot needs fast closed-loop manipulation but cannot afford slow future-video generation at runtime. A practical adaptation would be:

- train or fine-tune with paired observation, language, action, and short future-frame sequences;
- keep the future-frame prediction loss during training;
- remove future-frame generation during deployment;
- run the policy as a direct action-chunk predictor from current camera observations and command text.

For my robot, this is most relevant to real-time manipulation tasks such as folding, sorting, pick-and-place, bimanual handoff, and visual servoing. Required inputs are synchronized camera images, language or task labels, robot action trajectories, and enough demonstrations to learn the task distribution. Main risks are GPU latency, action safety, mismatch between training camera setup and real deployment, and insufficient data for contact-rich edge cases.

## Implementation Notes

Start with a smaller experimental version before attempting a full 6B model. The minimum useful experiment is to compare two policies on the same robot dataset: one with action-only training and one with an added future-frame latent prediction loss. If the video-co-trained policy improves success or recovery behavior without increasing runtime much, then Fast-WAM's principle is worth adopting.
