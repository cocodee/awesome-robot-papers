# Xiaomi-Robotics-1: Scaling Vision-Language-Action Models with over 100K Hours of Real-World Trajectories

## Metadata

- Authors: Xiaomi Robotics Team, Jun Guo, Piaopiao Jin, Jason Li, Peiyan Li, Yingyan Li, Futeng Liu, Wanli Peng, Optimus Qin, Yifei Su, Nan Sun, Qiao Sun, Runze Suo, Heyun Wang, Yunhong Wang, Rujie Wu, Caoyu Xia, Lina Zhang, Jack Zhao, Guoliang Chen, et al.
- Venue/year: arXiv, 2026
- Source: https://arxiv.org/pdf/2607.15330
- arXiv: 2607.15330v2, 22 Jul 2026
- Local PDF: [../papers/Xiaomi-Robotics-1-Scaling-Vision-Language-Action-Models-with-over-100K-Hours-of-Real-World-Trajectories.pdf](../papers/Xiaomi-Robotics-1-Scaling-Vision-Language-Action-Models-with-over-100K-Hours-of-Real-World-Trajectories.pdf)
- Converted Markdown: [../papers/Xiaomi-Robotics-1-Scaling-Vision-Language-Action-Models-with-over-100K-Hours-of-Real-World-Trajectories.md](../papers/Xiaomi-Robotics-1-Scaling-Vision-Language-Action-Models-with-over-100K-Hours-of-Real-World-Trajectories.md)
- Project page: https://robotics.xiaomi.com/xiaomi-robotics-1.html

## Research Question

Can a VLA model obtain broad manipulation capability by scaling diverse real-world data, and do the resulting pre-training gains transfer to unseen robot environments and low-data downstream adaptation?

The paper treats robotics data scale as the main bottleneck. UMI handheld grippers make it possible to collect data across many environments without tying every trajectory to one robot embodiment, but the resulting clips do not naturally contain imperative robot instructions. Xiaomi-Robotics-1 addresses this with a two-stage recipe: broad action pre-training followed by embodiment and instruction alignment.

## Core Method

Xiaomi-Robotics-1 uses a Mixture-of-Transformers architecture that couples a Qwen3-VL vision-language model with a diffusion transformer (DiT). The VLM encodes images and language, while the DiT generates an action chunk conditioned on robot proprioception and the VLM observation/language KV cache. Actions are generated with flow matching and five Euler inference steps. The model has 2.6B, 5.1B, and 10.5B total-parameter variants.

The VLM also predicts K candidate action chunks using Choice Policies. A winner-takes-all L1 action loss and candidate-score loss provide direct action supervision to the VLM and help the DiT converge. Action-related tokens are excluded from the DiT attention computation; this prevents a shortcut where the DiT copies the VLM's candidate actions instead of grounding its prediction in visual and language context.

Pre-training uses more than 100,000 hours of real-world UMI trajectories from household, commercial, industrial, office, and outdoor environments. The trajectories are split into fixed-length clips and automatically captioned by Qwen3.5-27B with descriptions of gripper and object state transitions. A producer-consumer pipeline labels the full corpus in about two weeks. The pre-training objective combines flow-matching loss, Choice Policy regression, and next-token prediction, with vision-language data and UMI data sampled at a 1:9 ratio.

Post-training uses about 10,000 hours of cross-embodiment data: more than 7,200 hours of in-house mobile-manipulator and dual-arm robot data, over 1,000 hours of instruction-labeled UMI data, and open datasets such as Bridge V2, RT-1, and DROID. This stage maps UMI-gripper action generation to robot action spaces and changes state-transition descriptions into imperative instructions. Relative end-effector pose deltas, base velocity, and waist deltas are packed into a unified masked action vector.

## Key Innovation

- Scaling with UMI data: a hardware-light data-collection interface expands environment and task diversity beyond conventional teleoperation.
- State-transition auto-labeling: descriptive labels turn unlabeled or weakly labeled clips into precise action-conditioning targets.
- Explicit two-stage alignment: pre-training learns general action generation, while post-training handles embodiment and instruction gaps.
- Complementary scaling axes: both data volume and model capacity improve out-of-distribution performance, with data appearing to be the stronger current bottleneck.
- Shortcut control in the MoT architecture: separating action-query tokens from DiT attention preserves visual and textual grounding.

## Problems Solved

The work targets three practical problems in robot foundation models: expensive and hardware-bound data collection, weak language labels for large trajectory corpora, and poor transfer from a general policy to a specific robot. It also targets the high data cost of learning new contact-rich, dexterous, deformable-object, and mobile-manipulation tasks.

The important conceptual shift is that a large pre-training corpus need not be collected in the final robot's action space. The post-training stage can align a general UMI action prior with multiple robot embodiments, provided the action frames and semantics are normalized carefully.

## Evidence

- In pre-training, validation action error decreases as UMI data scales from 12.5% to 100% of a 20k-hour subset. Small-data settings overfit, while 50% and 100% continue improving. Larger 2B, 5B, and 10B models also improve, although the model-size gaps are smaller than the data-scale gaps.
- In real-robot out-of-the-box evaluation on four tasks and unseen environments, scaling pre-training data raises overall success from 26% with no action pre-training to 75% with the full pre-training setting. Scaling model size raises success from 61% for 2B to 75% for 5B and 79% for 10B.
- For four held-out downstream tasks, the low-data setting uses 36 hours total, less than 10 hours per task on average. Xiaomi-Robotics-1 reaches 75% average success and 90% average progress, versus 40% and 66% for π0.5.
- Simulation results are state of the art in the reported comparisons: 74.5% on RoboCasa, 57.4% average success on RoboCasa365, the latter exceeding the previous 46.6% result; it also leads the reported VLABench aggregate and RoboDojo results, with an average RoboDojo score of 20.07 versus 13.07 for the prior best.
- RoboCasa365 is especially informative: the model reaches 32.1% on unseen composite tasks, suggesting that the gain is not limited to memorizing atomic skills.

The paper has a small internal reporting inconsistency: the abstract and RoboCasa365 table report 57.4%, while one introduction sentence says 57.6%. This note uses the table/abstract value of 57.4%.

## Limitations

The paper does not provide a detailed public breakdown of the 100k-hour corpus, so it is difficult to independently assess duplication, task balance, failure trajectories, or geographic and environmental bias. UMI data also uses egocentric cameras and a gripper-centric interface; transfer to robots with very different sensing, kinematics, or dexterous hands may require substantial post-training.

The strongest real-robot claims are evaluated on tasks that are represented in post-training, although object instances and environments are held out. This is meaningful generalization, but weaker than a fully task-disjoint test. The model also does not use observation history in RoboDojo, and the authors note a lower memory score than a model explicitly designed for memory.

Finally, the training and auto-labeling pipeline is expensive and operationally complex. Simulation benchmark gains do not by themselves establish safety, recovery under severe perception failure, or long-term robustness in uncontrolled homes.

## Application to My Robot

The most practical lesson is to separate data collection from final embodiment. If my robot project has limited successful demonstrations, I can collect broader egocentric manipulation data or use a common end-effector interface, then reserve robot-specific data for alignment and instruction following.

A staged implementation would be:

- normalize cameras, timestamps, action frequency, end-effector frames, and proprioception;
- represent arm actions as relative end-effector deltas and mask unavailable dimensions for heterogeneous robots;
- automatically segment clips and caption object/scene state transitions;
- pre-train or adapt a smaller VLA on state-transition prompts;
- post-train with a smaller set of imperative instructions on my robot;
- evaluate data scaling, unseen-object generalization, and fine-tuning efficiency separately.

For a smaller project, the key experiment is not immediately reproducing 100k hours. It is comparing a policy trained only on robot-specific demonstrations against one initialized with diverse UMI-style or human egocentric data. Contact-rich tasks such as opening appliances, packing, inserting deformable items, and mobile manipulation are good tests because they expose whether the broad action prior is useful.

Required hardware includes synchronized RGB observation and robot state; mobile tasks additionally need base and waist state. Risks include frame-convention mistakes, language captions that describe effects incorrectly, unsafe action chunks during early deployment, and a domain gap between UMI grippers and the target robot. Use action limits, collision checks, and a human stop mechanism during transfer.
