# Pi-star-0.6: A VLA That Learns From Experience

## Metadata

- Title: $\pi^{*}_{0.6}$: a VLA That Learns From Experience
- Authors: Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan Goryachev, Lachy Groom, Hunter Hancock, Karol Hausman, Gashon Hussein, Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim Jones, Ben Katz, Liyiming Ke, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow, James Tanner, Marcel Torne, Quan Vuong, Anna Walling, Haohuan Wang, Blake Williams, Sukwon Yoo, Lili Yu, Ury Zhilinsky, Zhiyuan Zhou
- Venue/Year: arXiv, 2025
- arXiv: 2511.14759v2, 19 Nov 2025
- Source: https://arxiv.org/pdf/2511.14759
- Project page: https://pi.website/blog/pistar06
- Local PDF: [../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.pdf](../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.pdf)
- Converted Markdown: [../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.md](../papers/Pi-star-0.6-A-VLA-That-Learns-From-Experience.md)

## Research Question

The paper asks how a large vision-language-action model can keep improving after deployment, rather than being limited by imitation learning from demonstrations. The target setting is real robot manipulation where tasks are long, messy, and hard to score densely: folding diverse laundry, assembling cardboard boxes, and making espresso drinks with a professional machine.

The key problem is not just task generalization. It is how to turn real execution experience, sparse success labels, and occasional human corrections into a stable reinforcement-learning signal for a high-capacity VLA with continuous flow-matching actions.

## Method

The paper proposes RECAP: RL with Experience and Corrections via Advantage-conditioned Policies. The training loop has three main stages.

First, the system collects task episodes from demonstrations, autonomous robot rollouts, and optional expert teleoperation interventions during autonomous execution. Each episode receives a sparse outcome label, usually success or failure.

Second, it trains a language-conditioned distributional value function. The value function predicts normalized remaining steps to success, using values in roughly `(-1, 0)` where `0` means successful completion. Failed episodes receive a large negative terminal penalty. This value model is initialized from a smaller VLM backbone and trained on the accumulated dataset.

Third, it uses the value model to compute an advantage indicator for each action. Instead of applying PPO or REINFORCE directly to the full VLA, the policy is trained with supervised-style losses while conditioning the action prediction on a binary text prefix such as `Advantage: positive` or `Advantage: negative`. Human corrective actions are forced to positive advantage.

The final model, $\pi^{*}_{0.6}$, extends $\pi_{0.6}$ with this advantage-conditioning path. The base policy uses a Gemma 3 4B VLM backbone, an 860M-parameter flow-matching action expert, robot observations from multiple cameras and proprioception, action chunks at 50 Hz, and high-level subtask text prediction.

## Key Innovation

- It makes real-world RL practical for a large VLA by turning policy improvement into advantage-conditioned supervised training.
- It uses all heterogeneous data: demonstrations, successful and failed autonomous trials, prior-policy data, and expert corrections.
- It avoids needing exact action likelihoods for the flow-matching action head, which makes it easier to scale than direct policy-gradient training.
- It pre-trains advantage conditioning on broad multi-robot data, then specializes with on-robot experience.
- It optimizes practical robot throughput, not only per-episode success.

## Experiments

The evaluation uses a static bimanual robot setup with two 6-DoF arms, parallel-jaw grippers, three cameras, and joint/gripper observations. The main tasks are:

- Laundry folding: T-shirts and shorts within 200 seconds.
- Diverse laundry: 11 item types, with quantitative evaluation focused on button-up shirts within 500 seconds.
- Targeted laundry failure removal: a strict collar-facing-up criterion from an adversarial initial condition.
- Cafe double-shot espresso: pick up portafilter, grind, tamp, lock into machine, bring cup, extract, and serve within 200 seconds.
- Box assembly: fold a flattened cardboard sheet, attach a label, and place it in a crate within 600 seconds.

Baselines include pre-trained $\pi_{0.5}$, supervised $\pi_{0.6}$, RL-pretrained $\pi^{*}_{0.6}$ before task experience, offline RL plus SFT, AWR, and a PPO-style diffusion policy optimization baseline.

Main reported findings:

- On difficult diverse laundry and espresso tasks, adding on-robot RECAP experience more than doubles successful task completions per hour.
- Failure rates are reduced by about a factor of two on the hardest tasks.
- On most tasks except diverse laundry, final success rates are in the 90%+ range.
- In iterative experiments, T-shirt/shorts folding improves about 50% in throughput over two RECAP iterations, while box assembly reaches roughly 2x throughput improvement after the second iteration.
- For a targeted laundry failure mode, two RECAP iterations with 600 trajectories each produce 97% success without extra demonstrations or intervention data.
- RECAP outperforms AWR and PPO-style extraction on the laundry comparison, especially in throughput.

## Limitations

The system is not fully autonomous. It still needs human effort for reward labels, expert interventions, and episode resets. The exploration strategy is also simple: it mostly relies on policy stochasticity and human interventions, so it is best suited when the initial imitation policy already performs reasonable partial behavior.

RECAP also uses batch-style iterated offline updates rather than fully online RL. Data is collected, models are retrained, and then the next policy is deployed. This is practical, but it means the system does not update continuously while the robot is running.

For smaller labs, the compute and data requirements are substantial: a large VLA, value model, multi-camera bimanual hardware, many real robot trials, and consistent annotation infrastructure. The paper demonstrates strong real-world performance, but transfer to a new robot will depend heavily on action interface compatibility, safety handling, task reset automation, and label quality.

## Practical Robotics Impact

The paper is important because it treats a VLA as a robot skill that should improve from deployment experience, not as a fixed imitation policy. For real robots, this directly addresses three common blockers:

- Demonstrations are not enough to cover deployment mistakes.
- Human teleoperation is useful but slow and inconsistent.
- Online policy-gradient RL is hard to stabilize for large continuous-action VLAs.

The most practical idea is the advantage-conditioned policy interface. A robot team can keep the normal supervised VLA training path while adding value-based labels that tell the model which actions are likely to improve over the current behavior.

## Application to My Robot

For my robot, the most valuable application is long-horizon manipulation improvement after an initial policy already works sometimes. Good candidate tasks include folding cloth, sorting and packing objects, tool-use sequences, appliance operation, assembly, and cleanup routines.

A realistic integration plan:

- Start with a demonstration-trained policy for one task.
- Log every rollout with synchronized camera frames, robot state, actions, language command, timing, and success/failure label.
- Add a simple value model that predicts remaining progress or success likelihood from observation and language.
- Convert value differences into a binary improvement indicator for each action or action chunk.
- Fine-tune the policy with both normal behavior cloning and an advantage-conditioned action loss.
- Mark human rescue or correction segments as positive advantage, but still keep failed autonomous segments in the dataset.
- Track throughput, success rate, timeout frequency, and common failure modes across iterations.

The first implementation should not try to reproduce the full $\pi^{*}_{0.6}$ stack. A smaller version can use the same idea with an existing visual policy: train a critic over episodes, label high-advantage chunks, add a text or learned binary conditioning token to the policy, and test whether conditioning on the positive token improves speed and reliability.

Expected benefit: the robot should learn from its own deployment failures and become faster without requiring a new full demonstration set.

Main risks: sparse labels may be noisy, the value model may reward shortcuts, human corrections may be inconsistent, and repeated fine-tuning can drift if old data is not retained. Safety guards and rollback checkpoints are required before running autonomous collection.

## Implementation Notes

Use RECAP first as an experiment-management pattern:

1. Define strict task success criteria and timeout.
2. Collect baseline SFT rollouts.
3. Label success/failure and annotate major failure categories.
4. Train a value model from logged episodes.
5. Fine-tune the policy with positive/negative advantage conditioning.
6. Deploy the new policy for a limited batch of trials.
7. Compare against the previous checkpoint on the same task distribution.

For a low-cost prototype, replace the large VLA value model with a frozen visual encoder plus small temporal head, and replace flow matching with the current robot policy's action loss. The core test is whether "condition on high-advantage behavior" improves deployment throughput over plain behavior cloning.
