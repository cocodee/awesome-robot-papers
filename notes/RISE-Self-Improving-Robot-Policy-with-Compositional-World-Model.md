# RISE: Self-Improving Robot Policy with Compositional World Model

## Metadata

- Authors: Jiazhi Yang, Kunyang Lin, Jinwei Li, Wencong Zhang, Tianwei Lin, Longyan Wu, Zhizhong Su, Hao Zhao, Ya-Qin Zhang, Li Chen, Ping Luo, Xiangyu Yue, Hongyang Li
- Venue/Year: arXiv, 2026
- Source: https://arxiv.org/pdf/2602.11075
- arXiv: 2602.11075v2, last revised 28 Apr 2026
- Project page: https://opendrivelab.com/RISE
- Code: https://github.com/OpenDriveLab/RISE
- Local PDF: [../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.pdf](../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.pdf)
- Converted Markdown: [../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.md](../papers/RISE-Self-Improving-Robot-Policy-with-Compositional-World-Model.md)

## Research Question

The paper asks how a VLA robot policy can improve itself on contact-rich, dynamic, long-horizon manipulation tasks without doing expensive and risky on-policy reinforcement learning directly on real hardware.

The core problem is that imitation-learned VLA policies can follow demonstrations but remain brittle when execution drifts off the expert trajectory. Real-world RL can, in principle, teach recovery and robustness, but physical interaction is slow, serial, unsafe, and requires repeated resets. RISE tries to move the online RL loop into an imagined environment learned from robot data.

## Core Method

RISE builds a compositional world model with two separate modules:

- a controllable dynamics model that predicts future multi-view observations from recent visual history and a candidate action chunk;
- a progress value model that scores imagined observations and converts progress differences into an advantage signal for policy improvement.

The dynamics model is initialized from Genie Envisioner and adapted to robot action conditioning. It predicts multi-view RGB futures from top and wrist cameras. The authors introduce task-centric batching so each optimization batch emphasizes action diversity within related task scenes, improving controllability instead of only visual realism.

The value model is initialized from a pretrained VLA backbone and trained with two objectives. A progress regression objective gives dense temporal structure, while temporal-difference learning on success and failure data makes the value estimate more sensitive to subtle contact failures. The advantage for an action chunk is computed as the average value improvement between the current observation and the imagined future observations.

Policy learning has two stages. First, a warm-up stage fine-tunes the VLA on offline real-world data, including expert demonstrations, policy rollouts, failures, and human corrections, while adding advantage conditioning. Second, a self-improving loop samples offline states, prompts the rollout policy to propose high-advantage actions, uses the world model to imagine future observations, evaluates those futures with the value model, and trains the policy on the resulting action-advantage samples. The world model is used only during training, so it adds no inference overhead to the deployed policy.

## Key Innovation

The key innovation is treating a learned visual world model as the online RL environment for a real robot foundation policy, but decomposing the world model into dynamics and value modules instead of asking one model to both simulate and reward everything.

This decomposition is practical. The dynamics model can focus on fast, action-controllable multi-view future prediction. The value model can focus on task progress and failure sensitivity. Together they produce chunk-level advantages without needing to simulate a full episode until terminal success or failure, which is important because long-horizon video rollouts accumulate errors.

## Problems Solved

RISE addresses three practical bottlenecks:

- reducing dependence on risky real-world trial-and-error for RL;
- giving VLA policies recovery and robustness beyond pure imitation learning;
- producing denser learning signals than sparse terminal rewards for long-horizon manipulation.

This is especially relevant for tasks where small contact errors compound, such as grasping moving objects, manipulating deformable items, zipping, closing boxes, and bimanual coordination.

## Experiments

The paper evaluates RISE on a dual-arm real-world setup with three challenging tasks:

- Dynamic Brick Sorting: pick colored bricks from a moving conveyor and sort them into matching bins.
- Backpack Packing: open a backpack, insert clothes, lift, and zip it.
- Box Closing: place a cup, fold the flap, and tuck the tab with bimanual precision.

Main real-world results report large gains over imitation and RL baselines:

- Dynamic Brick Sorting: RISE reaches 85% success, compared with 35% for the fine-tuned π0.5 policy and 50% for RECAP.
- Backpack Packing: RISE reaches 85% success, compared with 30% for π0.5 and 40% for RECAP.
- Box Closing: RISE reaches 95% success, compared with 35% for π0.5 and 60% for RECAP.

The ablations are important. On Dynamic Brick Sorting, using online actions alone improves completion from 35% to 40%, but using both online actions and imagined online states raises completion to 70%. Removing dynamics pretraining drops completion to 15%, removing task-centric batching drops it to 40%, removing progress loss drops it to 50%, and removing TD learning drops it to 35%. This supports the claim that both the dynamics model and the value model design matter.

For dynamics quality, RISE improves action controllability and visual fidelity over Cosmos and Genie Envisioner baselines. On the authors' real-world tasks, RISE reports better PSNR, LPIPS, SSIM, and EPE than the compared world models, with EPE improving from 1.21 for Cosmos and 1.05 for GE to 0.54 for RISE.

## Limitations

RISE is still constrained by the accuracy and coverage of the learned world model. Rare states, underrepresented failures, or unusual contacts can lead to physically implausible imagined transitions, which may produce misleading advantages.

The method also still needs a non-trivial amount of real robot data to anchor learning. The paper finds that mixing offline real data with imagined online data is essential; too little offline data causes collapse, while too much constrains improvement.

Finally, the approach shifts cost from physical interaction to computation. The reported dynamics pretraining uses 16 H100 GPUs for about seven days, task-specific dynamics fine-tuning uses 8 H100 GPUs for about three days, and value/policy training also uses multi-GPU runs. A small lab robot project would need a lighter world model, distillation, or a narrower task-specific version.

## Application to My Robot

RISE is most useful if my robot already has a VLA or diffusion/flow policy that works in demonstrations but fails after small execution errors. Instead of running unsafe online RL on the robot, I can use the RISE idea to learn from imagined rollouts.

A practical adaptation would be:

- collect synchronized multi-view video, action chunks, language or task labels, success episodes, failure episodes, and human correction data;
- train a task-specific action-conditioned future predictor for short horizons, not full-episode simulation;
- train a value model that scores task progress and penalizes failure states;
- compute advantages from short imagined futures;
- fine-tune the policy with advantage conditioning while mixing real offline data to prevent drift.

Required hardware and data are at least one global camera, preferably wrist cameras, calibrated robot actions, enough demonstrations and failure rollouts, and GPU capacity for video-model fine-tuning. For a smaller robot, the first experiment should avoid full RISE scaling: use a short-horizon latent dynamics model or image-feature predictor, compare action-only fine-tuning against advantage-conditioned fine-tuning, and test whether the robot recovers better from off-nominal states.

Expected benefits are higher robustness, better recovery behavior, less real-world exploration risk, and more useful training signal from failures. Main risks are world-model hallucination, value-model mis-scoring, compute cost, and distribution shift between imagined visual states and real camera observations.

## Implementation Notes

The most realistic starting point is a narrow task such as sorting, insertion, drawer closing, or deformable-object placement. Avoid trying to build a general simulator first. The minimum viable version is:

- train the current policy from demonstrations;
- collect success, failure, and correction rollouts;
- learn a progress/value scorer from those trajectories;
- generate short candidate action rollouts in a learned visual or latent dynamics model;
- train the policy to prefer high-advantage action chunks while keeping a fixed ratio of real offline data in every batch.

The paper's offline-data-ratio ablation suggests this mixing ratio is not a detail. In their setting, performance peaks around a 0.6 offline data ratio; a local implementation should tune this instead of assuming imagined data can replace real data.
