# LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts

Wenxuan Guo

Yingping Liang

Zhaoguo Wang

Ziyuan Li

Angyuan Ma

Zhenyu Wu

Chengkun Wang

Bingyao Yu

Ze Chen

Borui Zhang

Xiuwei Xu

Meng Zhang

Erjin Zhou

Jiwen Lu

Tsinghua University  Dexmal  Loopeva

\* Core Contributors   Corresponding Authors

###### Abstract

Scaling expert demonstrations alone does not enable generalist robot policies to improve from deployment.
Real-world rollouts contain successes, suboptimal behavior, and failures: imitating every recorded action can reinforce poor behavior, while filtering out failures discards evidence of physical interactions and their consequences.
We introduce LoopWAM, a closed-loop world-action model that learns directly from this full quality spectrum, using rollouts from both itself and other deployed policies.
Source-dependent noise sampling unifies behavior learning and action-conditioned world modeling, while quality steering and quality-weighted supervision retain full video supervision across qualities and regulate action imitation.
Video and action tokens interact throughout parallel denoising, allowing learned consequences to inform action generation directly.
On RoboChallenge Table30-V2, three deployment-and-training rounds raise success from 23.67% to 43.33%, a 19.7-percentage-point gain, with a final score of 56.80.
LoopWAM also achieves 94.5% average success on RoboTwin 2.0 and 49.5% overall success on RoboCasa365 without additional embodied pretraining, obtaining the best overall results among the compared methods across all three benchmarks.
On challenging shirt folding task, two rounds of deployment-driven improvement after single-task post-training raise success from 13.20% to 55.56%.
These results demonstrate closed-loop improvement from mixed-quality experience under both multi-task learning and single-task post-training.
[Project Page](https://loop-wam.github.io/)

\abscontent

## 1 Introduction

Scaling human-collected robot data has expanded the capabilities of generalist manipulation policies ([O’Neill et al., 2024](#bib.bib20)), but demonstration scaling alone does not close the loop between deployment and continual improvement.
Deployment exposes states, interactions, and failure modes beyond curated demonstrations, providing new experience for an embodied data flywheel.
Real-world reinforcement learning (RL) ([Xu et al., 2026](#bib.bib23)) can improve policy performance during deployment, but may narrow the model’s predictive distribution and often struggles to learn multi-task generalist policies.
Although distilling a generalist policy from multiple RL specialists ([Xiao et al., 2025](#bib.bib22)) can address this issue, the generalist’s supervision comes from curated successful rollouts rather than the full interaction history.
Therefore, we aim to study direct generalist improvement from the full mixture of successful, suboptimal, and failed deployment rollouts.
The challenge is to use this experience productively: imitating every recorded action risks absorbing undesirable behavior, while retaining only high-quality trajectories discards informative interactions and their outcomes.

Recent VLA and world-action models address important pieces of this problem.
On the VLA side, π0.6\pi\_{0.6} ([Physical Intelligence, 2025](#bib.bib3)) uses advantage-conditioned learning to incorporate autonomous experience and interventions, while π0.7\pi\_{0.7} ([Physical Intelligence, 2026](#bib.bib4)) uses quality, speed, and mistake metadata to absorb mixed-quality data and distill specialist capabilities into a generalist.
These VLA methods use steering during training to model behavior distributions across data qualities and specify a desirable mode at inference for smooth execution, but rely on VLM-based language–vision–action representations without an explicit objective for learning the physical dynamics reflected in action–video transitions.
Consequently, suboptimal and failed rollouts provide behavior targets but do not directly supervise learning of their physical consequences.
World modeling offers a more elegant solution: WAMs ([Pai et al., 2025](#bib.bib21); [Ye et al., 2026b](#bib.bib33); [Li et al., 2026](#bib.bib15)) couple predictive visual representations with action generation, while action-conditioned world models (ACWMs) ([Guo et al., 2025](#bib.bib10); [Gao et al., 2026](#bib.bib9)) predict future observations conditioned on actions.
Combining the two allows ACWM to learn action consequences from data of different qualities, while WAM learns appropriate actions from expert demonstrations.
τ0\tau\_{0}-WM ([Zhou et al., 2026](#bib.bib25)) trains separate WAM and ACWM, routing failure and recovery data to ACWM training and use ACWM as selector for policy improvement.
FACT ([Peng et al., 2026](#bib.bib24)) implements the two roles within a shared model, but retains sequential action–consequence generation. It only supports success/failure supervision split, with failure consequences influencing the policy implicitly through shared representations.
These approaches expose a remaining design challenge in learning from mixed-quality deployment experience: VLA steering lacks natural action–video dependency modeling, while consequence-aware WAMs still exploit rollout data indirectly through an ACWM interface—a simulator for action selection or a subsequent consequence-prediction stage that influences the policy through shared representations.
Can a single WAM directly learn from mixed-quality deployment rollouts, with all qualities supervising the model and learned consequences participating directly in action generation?

![Refer to caption](figures/figure-1.png)

Figure 1: LoopWAM learns from deployment.
Mixed-quality rollouts return to training through quality steering, source-dependent noise sampling, and quality-weighted supervision.
Center: closed-loop self-improvement on RoboChallenge Table30-V2, where three rounds of deployment and retraining increase overall success from 23.67% to 43.33%.
Bottom: benchmark comparisons.

We introduce LoopWAM, a closed-loop World-Action Model that updates a generalist directly from mixed-quality deployment rollouts.
Our core idea is to let one WAM directly absorb rollouts across the full quality spectrum and learn from each.
To achieve this, we first use *source-dependent noise sampling* to unify WAM behavior learning and ACWM consequence learning within a single model and generation stage.
Video and action noise levels are sampled independently, allowing low-noise rollout actions to guide prediction of their observed consequences.
Within this unified model, *quality steering* represents behaviors of different qualities and selects the highest-quality condition at deployment.
To control how strongly each behavior is imitated, we further apply *quality-weighted supervision*, reducing imitation of suboptimal actions and masking failed-action targets while retaining video supervision across all qualities.
Together, these mechanisms let every trajectory supervise the joint model according to its behavioral quality and observed transitions.
Video and action tokens interact bidirectionally throughout one parallel denoising process, allowing learned future representations to participate in action formation without a separate consequence-evaluation stage.
We close the loop by repeatedly collecting rollouts and retraining the generalist on demonstrations and accumulated experience before redeployment.
On RoboChallenge Table30-V2 ([RoboChallenge Dexmal Team, 2026](#bib.bib28)), three rounds raise overall success from 23.67% to 28.00%, 37.67%, and 43.33%, a 19.7-percentage-point improvement, with a final score of 56.80, ranking first in both success and score among the compared entries (Table [1](#S4.T1 "Table 1 ‣ RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).
LoopWAM achieves 94.5% average success on RoboTwin 2.0 ([Chen et al., 2025](#bib.bib6)), exceeding the reported 87.5% of FACT and 93.6% of LingBot-VA 2.0, and 49.5% on the 50-task RoboCasa365 evaluation ([Nasiriany et al., 2026](#bib.bib18)), above ABot-M0.6’s 46.6% (Tables [2](#S4.T2 "Table 2 ‣ RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")–[3](#S4.T3 "Table 3 ‣ RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).
We further evaluate deployment-driven self-improvement after single-task post-training on challenging shirt folding, which involves deformable objects and multiple coordinated steps.
Two deployment-and-training rounds raise success from 13.20% to 55.56% (Section [4.4](#S4.SS4 "4.4 Closed-Loop Improvement from Deployment ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).
These results establish that directly learning from mixed-quality rollouts with parallel world–action denoising can deliver leading benchmark performance and repeated deployment improvement in both multi-task and single-task settings.

## 2 Related Work

Robot Manipulation Policies.
Robot manipulation policies increasingly combine scalable imitation learning with pretrained representations.
ACT ([Zhao et al., 2023](#bib.bib37)) and Diffusion Policy ([Chi et al., 2025](#bib.bib8)) learn action sequences from demonstrations, while RT-2 ([Zitkovich et al., 2023](#bib.bib40)) and OpenVLA ([Kim et al., 2024](#bib.bib13)) transfer vision-language priors to language-conditioned control.
Flow-based policies such as π0\pi\_{0} ([Black et al., 2024](#bib.bib2)) and π0.5\pi\_{0.5} ([Physical Intelligence et al., 2025](#bib.bib26)) further scale continuous action generation and generalization.
Open X-Embodiment ([O’Neill et al., 2024](#bib.bib20)) and DROID ([Khazatsky et al., 2024](#bib.bib12)) expand training coverage across embodiments and environments.
Beyond offline demonstrations, DAgger ([Ross et al., 2011](#bib.bib29)) addresses policy-induced distribution shift by collecting expert labels on visited states.
LoopWAM studies learning from the recorded observations and actions of deployment rollouts, using trajectory quality to guide policy updates while retaining world supervision from unsuccessful interactions.

World Action Models.
Video-based robot policies use predictive visual representations to support control.
mimic-video ([Pai et al., 2025](#bib.bib21)) conditions an action decoder on representations from a pretrained video model.
DreamZero ([Ye et al., 2026b](#bib.bib33)) jointly generates video and actions, while LingBot-VA ([Li et al., 2026](#bib.bib15)) organizes visual prediction and action decoding within a causal autoregressive framework.
LingBot-VA 2.0 ([Zhang et al., 2026a](#bib.bib35)) further develops native video-action pretraining with a control-oriented tokenizer.
Efficiency-oriented designs include Fast-WAM ([Yuan et al., 2026](#bib.bib34)), which retains video co-training but removes future-video generation at inference, and GigaWorld-Policy ([Ye et al., 2026a](#bib.bib32)), which learns action-conditioned visual dynamics while allowing action-only inference.
Being-H0.7 ([Luo et al., 2026](#bib.bib17)) instead uses future observations to supervise latent representations.
These studies establish several ways for predictive supervision to support action learning.
LoopWAM focuses on closing the deployment–training loop: mixed-quality rollouts broaden world-model training, while joint video–action modeling, quality steering, and weighted action supervision connect consequence awareness with high-quality behavior.

## 3 Method

LoopWAM learns a world–action model that can be updated with experience collected during deployment.
The framework couples video and action generation within a shared denoising process, then uses trajectory quality to distinguish how deployment data supervise world modeling and control.
Figure [2](#S3.F2 "Figure 2 ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") summarizes the architecture and training procedure.
We first introduce joint world–action modeling, followed by quality-aware learning from mixed trajectories and the deployment–learning loop.

![Refer to caption](figures/figure-2.png)

Figure 2: Overview of LoopWAM.
LoopWAM is structured as a Mixture-of-Transformer (MoT) architecture, where bidirectional attention enables feature interaction between the video and action branches.
Training combines quality-conditioned instructions, source-dependent noise sampling, and quality-weighted action supervision.
Expert trajectories supervise both modalities, while lower-quality rollouts retain full world supervision and contribute to action imitation according to their quality.
The trained model is deployed using the expert score q⋆q^{\star}, and recorded experience returns to the next training round.

### 3.1 Joint World–Action Modeling

We consider language-conditioned manipulation with visual observation oto\_{t}, robot state sts\_{t}, and instruction ℓ\ell.
The prediction targets are an action chunk At=(at,…,at+H−1)A\_{t}=(a\_{t},\ldots,a\_{t+H-1}) and the corresponding future observations VtV\_{t}, sampled over the same horizon.
A pretrained video VAE maps (ot,Vt)(o\_{t},V\_{t}) to an observation latent zoz\_{o} and future latents ZtZ\_{t}.
LoopWAM models their joint distribution

|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ(At,Zt∣ot,st,ℓ,q),p\_{\theta}(A\_{t},Z\_{t}\mid o\_{t},s\_{t},\ell,q), |  | (1) |

where qq is a numerical score of trajectory quality, as detailed in Section [3.2](#S3.SS2 "3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
This unified formulation enables a single model to learn action generation and visual dynamics from paired action–observation sequences ([Zhu et al., 2025](#bib.bib39)).

We instantiate this formulation with a dual-stream diffusion transformer whose video backbone is initialized from Wan2.2-TI2V-5B ([Wan et al., 2025](#bib.bib30)).
The video and action streams have separate token projections, transformer parameters, and prediction heads, with joint attention connecting the streams at every layer.
To train them with flow matching ([Lipman et al., 2023](#bib.bib16)), we independently perturb each target XmX\_{m}, where Xv=ZtX\_{v}=Z\_{t} and Xa=AtX\_{a}=A\_{t}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | Xmσm=(1−σm)​Xm+σm​ϵm,ϵm∼𝒩⁡(0,I),m∈{v,a}.X\_{m}^{\sigma\_{m}}=(1-\sigma\_{m})X\_{m}+\sigma\_{m}\epsilon\_{m},\qquad\epsilon\_{m}\sim\mathcal{N}(0,I),\quad m\in\{v,a\}. |  | (2) |

The joint network predicts velocity fields (vθv,vθa)(v\_{\theta}^{v},v\_{\theta}^{a}) with targets um=ϵm−Xmu\_{m}=\epsilon\_{m}-X\_{m}.
Each stream receives noise level σm\sigma\_{m}, with 00 denoting clean data and 11 pure noise; the observation latent zoz\_{o} remains clean.

The attention structure couples the two predictions throughout denoising.
Denote observation, future-video, and action tokens by OO, VV, and AA, respectively.
Their block mask, with queries indexing rows and keys indexing columns, is

|  |  |  |  |
| --- | --- | --- | --- |
|  | M(O,V,A)=(100111111),M\_{(O,V,A)}=\begin{pmatrix}1&0&0\\ 1&1&1\\ 1&1&1\end{pmatrix}, |  | (3) |

where 11 permits attention.
Observation tokens attend only within the initial frame.
Both streams cross-attend to the quality-conditioned instruction; robot-state tokens additionally condition the action stream.
Together with the training scheme in Section [3.2](#S3.SS2 "3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"), this architecture supports learning both embodied world representations and awareness of action consequences.
Dense video supervision on expert and mixed-quality rollouts broadens the interactions from which these representations are learned.
Through bidirectional attention, the world-prediction loss also trains features used for action generation.
This training couples learning how tasks can be completed with learning how particular actions affect their outcomes, encouraging consistency between video and action generation.

### 3.2 Quality-Aware Learning from Mixed Trajectories

Our training corpus combines expert demonstrations 𝒟E\mathcal{D}\_{E} with rollout data 𝒟R\mathcal{D}\_{R} of arbitrary quality, including successful, suboptimal, and failed executions.
These rollouts substantially broaden the state–action–outcome distribution beyond expert paths, providing world-model supervision even when their actions are undesirable imitation targets.
Each trajectory is assigned a source indicator d∈{E,R}d\in\{E,R\}; every training segment extracted from that trajectory uses the same indicator.
We combine source-dependent noise sampling, quality conditioning, and selective action supervision to learn from this broader experience while favoring high-quality behavior.

Source-dependent noise sampling.
Jointly predicting video and actions in a WAM does not by itself ensure that the predicted futures reflect the consequences of the generated actions.
To improve consistency between video and action generation and make world predictions more useful for control, we aim to strengthen action-conditioned world modeling (ACWM) within the same unified model.
We therefore use source-dependent noise sampling to make recorded rollout actions accessible when predicting their observed consequences, while retaining joint video–action generation in a single training stage.
Specifically, we select different noise distributions for expert and rollout segments, while drawing video and action noise levels independently within each segment:

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  | d=E:\displaystyle d=E: | σv∼Beta⁡(7,1),\displaystyle\sigma\_{v}\sim\operatorname{Beta}(7,1), |  | σa∼𝒫0,\displaystyle\sigma\_{a}\sim\mathcal{P}\_{0}, |  | (4) |
|  | d=R:\displaystyle d=R: | σv∼𝒫0,\displaystyle\sigma\_{v}\sim\mathcal{P}\_{0}, |  | σa∼Beta⁡(1,7).\displaystyle\sigma\_{a}\sim\operatorname{Beta}(1,7). |  |

Here 𝒫0\mathcal{P}\_{0} is the base noise distribution obtained by sampling u∼𝒰⁡(0,1)u\sim\mathcal{U}(0,1) and setting σ=ϕκ​(u)=κ​u/[1+(κ−1)​u]\sigma=\phi\_{\kappa}(u)=\kappa u/[1+(\kappa-1)u], with κ=5\kappa=5.
The Beta distributions ([Johnson et al., 1995](#bib.bib11)) are applied directly to σ\sigma.
For expert data, high video noise emphasizes recovering expert futures from strongly corrupted inputs, alongside action generation over the base noise distribution.
For rollouts, low action noise preserves much of the recorded motion while the video stream predicts its visual consequences.
Training across these executions broadens the action–outcome distribution seen by the world model, including transitions in which the task remains incomplete or an interaction fails.
Joint attention then connects this consequence-learning signal to the representations used for action generation.

Quality steering.
Within this unified training scheme, each trajectory is assigned a numerical quality score qq, which is shared by all training segments extracted from it.
We encode quality as a suffix to the instruction, ℓq=[ℓ;Quality:q]\ell\_{q}=[\ell;\texttt{Quality:}\ q], and use its text embeddings to condition both video and action streams.
We support two trajectory annotation schemes: (1) *Episode-level annotation*, where human annotators or a vision-language model (VLM) score each trajectory individually for fine-grained quality estimation; and (2) *coarse-level annotation*, where a single human-provided score is assigned to all rollouts from a policy checkpoint based on its overall success rate and motion smoothness.
Under coarse annotation, successful trajectories receive the checkpoint score while failed trajectories receive the minimum score, requiring only one annotation per checkpoint.
Both schemes represent rollout quality using numerical scores.
For expert demonstrations, we assign an expert score q⋆q^{\star} that is higher than the maximum rollout quality score.
The quality-conditioned instruction allows different behaviors under the same task instruction to be represented within one model.
During deployment, we condition on q=q⋆q=q^{\star} to steer sampling toward expert-quality behavior.

Quality-weighted supervision.
Given these noise levels and quality scores, we retain video prediction on all trajectory qualities and modulate action supervision with a nondecreasing weight λ⁡(q)∈[0,1]\lambda(q)\in[0,1].
Expert trajectories receive full action supervision with λ⁡(q⋆)=1\lambda(q^{\star})=1, while failed trajectories use λ⁡(q)=0\lambda(q)=0 and receive no action supervision.
For sample ii and modality mm, define the denoising loss

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℓm,i=ω⁡(σm,i)​‖vθ,im−(ϵm,i−Xm,i)‖valid2,\ell\_{m,i}=\omega(\sigma\_{m,i})\left\|v\_{\theta,i}^{m}-(\epsilon\_{m,i}-X\_{m,i})\right\|\_{\mathrm{valid}}^{2}, |  | (5) |

where the norm denotes mean squared error over valid target elements and ω\omega is the common timestep weighting function.
The clean observation latent is excluded from video supervision, and padded targets are masked in both modalities.
For a minibatch of BB segments, the complete objective is

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒLoopWAM=1B​∑i=1Bℓv,i⏟world supervision+∑i=1Bλ⁡(qi)​ℓa,imax⁡(1,∑i=1Bλ⁡(qi))⏟quality-weighted action supervision.\mathcal{L}\_{\mathrm{LoopWAM}}=\underbrace{\frac{1}{B}\sum\_{i=1}^{B}\ell\_{v,i}}\_{\text{world supervision}}+\underbrace{\frac{\sum\_{i=1}^{B}\lambda(q\_{i})\ell\_{a,i}}{\max\!\left(1,\sum\_{i=1}^{B}\lambda(q\_{i})\right)}}\_{\text{quality-weighted action supervision}}. |  | (6) |

The source indicator determines corruption, whereas quality controls the behavior condition and action weight.
In particular, λ⁡(q)=0\lambda(q)=0 removes direct imitation of a trajectory’s actions while preserving world-model gradients through the jointly attended video and action representations.
Quality steering and weighted supervision thus allow broader transition learning while concentrating action imitation on more desirable behavior.
The data preprocessing are specified in Appendix [A](#A1 "Appendix A Training and Data Processing Details ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").

### 3.3 Closed-Loop Self-Improvement

The deployed policy uses the high-quality action marginal of the joint model:

|  |  |  |  |
| --- | --- | --- | --- |
|  | πθ(At∣ot,st,ℓ;q⋆)=∫pθ(At,Zt∣ot,st,ℓ,q⋆)dZt.\pi\_{\theta}(A\_{t}\mid o\_{t},s\_{t},\ell;q^{\star})=\int p\_{\theta}(A\_{t},Z\_{t}\mid o\_{t},s\_{t},\ell,q^{\star})\,\mathrm{d}Z\_{t}. |  | (7) |

In practice, we sample this marginal by jointly denoising video and actions from Gaussian noise, holding the current observation latent fixed.
Starting from an expert-trained model, we collect and score deployment rollouts, then update the model on expert demonstrations and all accumulated rollouts using Equation [6](#S3.E6 "In 3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
Each updated model is redeployed with the expert score q⋆q^{\star} to continue the deployment–learning loop.

More broadly, LoopWAM’s self-improvement updates can use rollouts from arbitrary deployed policies, even poorly performing ones.
The joint architecture and quality-aware objective accommodate their varying trajectory qualities, so each trajectory contributes according to its observed transitions and behavioral quality.
This extends self-improvement to learning from deployment experience collected by other policies as well as LoopWAM itself.
We validate this broader setting on RoboTwin 2.0 and RoboCasa365 (Section [4.3](#S4.SS3 "4.3 Benchmark Results ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).

## 4 Experiments

### 4.1 Implementation Details

We initialize the video backbone, text encoder, and video VAE from Wan2.2-TI2V-5B ([Wan et al., 2025](#bib.bib30)), and use an action DiT with a hidden dimension of 1024.
Each training segment pairs a 64-step action chunk with nine RGB frames sampled at intervals of eight control steps, including the initial observation.
Multi-camera views are stitched into a single image, and actions and robot states are normalized using expert-data statistics.
Training follows the quality-conditioned joint objective in Section [3.2](#S3.SS2 "3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"), and deployment uses the expert score q⋆q^{\star}.
Table30-V2 uses relative joint targets and absolute gripper commands.
Additional training, preprocessing, and subtask-segmentation details are provided in Appendix [A](#A1 "Appendix A Training and Data Processing Details ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").

### 4.2 Benchmark Experimental Setup

We evaluate LoopWAM on the real-robot benchmark RoboChallenge Table30-V2 and two simulation benchmarks, RoboTwin 2.0 and RoboCasa365.
RoboChallenge evaluates closed-loop self-improvement using LoopWAM’s own real-robot deployments.
The two simulation benchmarks additionally test learning from different deployed policies by augmenting expert demonstrations with rollouts from both expert-trained LoopWAM and others.
Across these settings, successful, suboptimal, and failed rollouts expand the state–action–outcome distribution beyond expert demonstrations.

#### RoboChallenge Table30-V2.

RoboChallenge Table30-V2 ([RoboChallenge Dexmal Team, 2026](#bib.bib28)) is a standardized real-robot benchmark comprising 30 tabletop manipulation tasks across four embodiments: ALOHA, DOS-W1, ARX5, and UR5.
Its tasks test capabilities including tool use, precise manipulation, and coordinated bimanual control.
We follow the official multi-task evaluation protocol and report overall performance across embodiments.
Starting from one expert-trained multi-task LoopWAM per embodiment, we conduct three successive rounds of closed-loop self-improvement.
In each deployment round, we run each model on its assigned tasks and collect about 100 rollout trajectories per task.
These trajectories are quality-annotated and combined with expert demonstrations and rollout trajectories from all previous deployment rounds for further training.

#### RoboTwin 2.0.

RoboTwin 2.0 ([Chen et al., 2025](#bib.bib6)) comprises 50 bimanual manipulation tasks evaluated in clean and domain-randomized scenes.
Following the multi-task setup of LingBot-VA ([Li et al., 2026](#bib.bib15)), we use 2,500 expert demonstrations from clean scenes and 25,000 from heavily randomized scenes.
We augment these demonstrations with rollouts generated by expert-trained LoopWAM, X-VLA ([Zheng et al., 2025](#bib.bib38)), and π0.5\pi\_{0.5} ([Physical Intelligence et al., 2025](#bib.bib26)).
For each task, each policy contributes 20 clean and 130 randomized rollouts, yielding 22,500 trajectories across all 50 tasks and the three policies.
The combined rollout corpus has approximately the same total duration as the expert corpus.
Rollout collection and evaluation use different random seeds to avoid data leakage.
Rollout quality is annotated using the coarse-level numerical scores in Section [3.2](#S3.SS2 "3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").

Table 1: Performance on RoboChallenge Table30-V2. We report per-embodiment success rates (SR, %) and overall performance across four robot embodiments. Baselines are sorted by overall SR. Bold denotes the best performance, while blue and light blue highlight LoopWAM and the runner-up, respectively.

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | ALOHA | | DOS-W1 | | ARX5 | | UR5 | | Overall | |
|  | Score | SR | Score | SR | Score | SR | Score | SR | Score | SR |
| debuggers\_vla | 5.40 | 0.00 | 5.15 | 2.00 | 53.21 | 34.29 | 27.83 | 23.33 | 18.72 | 11.00 |
| W0 | 12.25 | 2.00 | 4.40 | 0.00 | 48.64 | 30.00 | 49.50 | 43.33 | 21.85 | 12.00 |
| test\_01 | 6.25 | 1.00 | 8.95 | 3.00 | 49.50 | 28.57 | 61.17 | 43.33 | 22.73 | 12.33 |
| holobrain | 11.75 | 3.00 | 13.30 | 6.00 | 53.64 | 30.00 | 70.67 | 43.33 | 27.93 | 14.33 |
| Baseline Model | 21.55 | 6.00 | 17.35 | 6.00 | 60.14 | 32.86 | 44.83 | 26.67 | 31.48 | 14.33 |
| MagicBot | 4.70 | 0.00 | 6.85 | 5.00 | 47.57 | 32.86 | 58.67 | 53.33 | 20.82 | 14.67 |
| mc | 10.60 | 7.00 | 2.00 | 0.00 | 73.64 | 47.14 | 22.50 | 20.00 | 23.63 | 15.33 |
| JV0 | 12.70 | 5.00 | 17.80 | 16.00 | 49.64 | 20.00 | 58.33 | 43.33 | 27.58 | 16.00 |
| my16 | 18.95 | 13.00 | 36.60 | 27.00 | 73.29 | 54.29 | 56.50 | 46.67 | 41.27 | 30.67 |
| VLA-DM0.5 | 26.50 | 18.00 | 55.45 | 42.00 | 79.07 | 58.57 | 86.50 | 70.00 | 54.42 | 40.67 |
| LoopWAM (expert-trained) | 23.05 | 8.00 | 46.35 | 38.00 | 37.00 | 24.29 | 43.33 | 26.67 | 36.10 | 23.67 |
| LoopWAM | 38.65 | 26.00 | 54.90 | 42.00 | 76.21 | 55.71 | 78.33 | 76.67 | 56.80 | 43.33 |

Table 2: Performance on RoboTwin 2.0. We report success rates (SR, %) under clean and randomized evaluation settings. Embodied PT. denotes additional embodied-data pretraining before benchmark training. LoopWAM is trained with the mixed expert–rollout corpus described in Section [4.2](#S4.SS2 "4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"). Blue and light blue highlight LoopWAM and the runner-up, respectively.

| Method | Embodied PT. | Clean | Rand. | Average |
| --- | --- | --- | --- | --- |
| π0\pi\_{0} ([Black et al., 2024](#bib.bib2)) | ✓ | 65.9 | 58.4 | 62.2 |
| X-VLA ([Zheng et al., 2025](#bib.bib38)) | ✓ | 72.9 | 72.8 | 72.9 |
| π0.5\pi\_{0.5} ([Physical Intelligence et al., 2025](#bib.bib26)) | ✓ | 82.7 | 76.8 | 79.8 |
| ABot-M0 ([Yang et al., 2026](#bib.bib31)) | ✓ | 81.2 | 80.4 | 80.8 |
| Motus (from Wan2.2) ([Bi et al., 2025](#bib.bib1)) | ✗ | 77.6 | 77.0 | 77.3 |
| Motus ([Bi et al., 2025](#bib.bib1)) | ✓ | 88.7 | 87.0 | 87.8 |
| LingBot-VA ([Li et al., 2026](#bib.bib15)) | ✓ | 92.9 | 91.5 | 92.2 |
| Fast-WAM ([Yuan et al., 2026](#bib.bib34)) | ✗ | 91.9 | 91.8 | 91.8 |
| AHA-WAM ([Cai et al., 2026](#bib.bib5)) | ✗ | 93.4 | 92.2 | 92.8 |
| LingBot-VA 2.0 ([Zhang et al., 2026a](#bib.bib35)) | ✓ | 93.8 | 93.4 | 93.6 |
| LoopWAM | ✗ | 94.6 | 94.4 | 94.5 |

Table 3: Performance on RoboCasa365. We report success rates (SR, %) across three evaluation splits. Baseline results are obtained from the official leaderboard. Embodied PT. follows the definition in Table [2](#S4.T2 "Table 2 ‣ RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"). Blue and light blue highlight LoopWAM and the runner-up, respectively.

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | |  | | --- | | Embodied PT. | | |  | | --- | | Atomic Seen | | |  | | --- | | Composite Seen | | |  | | --- | | Composite Unseen | | Overall |
| Diffusion Policy ([Chi et al., 2025](#bib.bib8)) | ✗ | 15.7 | 0.2 | 1.3 | 6.1 |
| π0\pi\_{0} ([Black et al., 2024](#bib.bib2)) | ✓ | 34.6 | 6.1 | 1.1 | 14.8 |
| π0.5\pi\_{0.5} ([Physical Intelligence et al., 2025](#bib.bib26)) | ✓ | 39.6 | 7.1 | 1.2 | 16.9 |
| GigaWorld-Policy 0.1 ([Ye et al., 2026a](#bib.bib32)) | ✓ | 44.4 | 11.8 | 2.9 | 20.7 |
| GR00T N1.6 ([NVIDIA et al., 2025](#bib.bib19)) | ✓ | 51.1 | 9.4 | 1.7 | 21.9 |
| GR00T N1.5 ([NVIDIA et al., 2025](#bib.bib19)) | ✓ | 50.7 | 14.8 | 2.7 | 23.9 |
| RLDX-1 ([Kim et al., 2026](#bib.bib14)) | ✓ | 67.6 | 27.9 | 8.5 | 36.0 |
| PRTS ([Zhang et al., 2026b](#bib.bib36)) | ✓ | 66.3 | 30.3 | 18.8 | 39.6 |
| ABot-M0.5 ([Chen et al., 2026](#bib.bib7)) | ✓ | 75.6 | 37.7 | 3.3 | 40.3 |
| ABot-M0.6 ([Yang et al., 2026](#bib.bib31)) | ✓ | 79.4 | 48.3 | 7.9 | 46.6 |
| LoopWAM | ✗ | 79.7 | 50.3 | 14.9 | 49.5 |

#### RoboCasa365.

RoboCasa365 ([Nasiriany et al., 2026](#bib.bib18)) is a large-scale simulation framework for household manipulation in diverse kitchen environments.
We evaluate on its 50-task benchmark, which includes atomic and composite manipulation tasks.
Training combines expert demonstrations with rollouts generated by expert-trained LoopWAM and RLDX-1 ([Kim et al., 2026](#bib.bib14)), with the combined rollout duration approximately matching that of the expert data.
Both expert and rollout data follow the Human300 training split: the 16 Composite-Unseen tasks are excluded from training and evaluated zero-shot.
As in RoboTwin 2.0, training and evaluation data use different random seeds.

### 4.3 Benchmark Results

#### RoboChallenge Table30-V2.

Table [1](#S4.T1 "Table 1 ‣ RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") compares expert-trained and final LoopWAM with leading entries from the official leaderboard ([RoboChallenge, 2026](#bib.bib27)).
After three deployment-and-training rounds, LoopWAM attains an overall score of 56.80 and 43.33% success, exceeding VLA-DM0.5 by 2.38 score points and 2.67% in success, and ranking first on both metrics among the compared methods.
Appendix [B](#A2 "Appendix B RoboChallenge Table30-V2 Leaderboard ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") includes a leaderboard snapshot.
Section [4.4](#S4.SS4 "4.4 Closed-Loop Improvement from Deployment ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") analyzes the successive deployment updates that produce this improvement over expert-only training.

#### RoboTwin 2.0.

LoopWAM achieves 94.58% success in clean scenes and 94.42% under domain randomization, averaging 94.50% (Table [2](#S4.T2 "Table 2 ‣ RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).
Without additional embodied pretraining, it improves over AHA-WAM by 1.70 percentage points and surpasses the pretrained LingBot-VA 2.0 by 0.90 points on average.
Together, these results show that joint learning from expert demonstrations and diverse deployment rollouts yields a competitive multi-task policy under both evaluation settings.

#### RoboCasa365.

LoopWAM achieves 79.7%, 50.3%, and 14.9% success on Atomic-Seen, Composite-Seen, and Composite-Unseen, respectively, yielding 49.5% overall success across the 50 tasks (Table [3](#S4.T3 "Table 3 ‣ RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).
It exceeds ABot-M0.6 by 2.9 percentage points overall without additional embodied pretraining.
The improvement extends to held-out composite tasks, demonstrating transfer to task compositions absent from both expert and rollout training data.

### 4.4 Closed-Loop Improvement from Deployment

![Refer to caption](figures-auto/fig-03.png)

Figure 3: Closed-loop improvement from real-robot deployment.
Top: three deployment-and-training iterations on RoboChallenge Table30-V2, covering 30 tasks across four robot embodiments.
Bottom: two deployment-and-training iterations on shirt folding after task-specific expert post-training of the DOS-W1 model.
Each plot reports success rate and score over successive improvement rounds.

We examine deployment-driven improvement in two real-robot settings: multi-task learning and single-task post-training (Figure [3](#S4.F3 "Figure 3 ‣ 4.4 Closed-Loop Improvement from Deployment ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).
Both follow the update procedure in Section [3.3](#S3.SS3 "3.3 Closed-Loop Self-Improvement ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"): At each iteration, we deploy the current policy and assign quality scores to the collected rollouts, then update the model through quality-aware joint training on expert demonstrations and all rollouts collected so far.

Multi-task deployment.
As in Section [4.2](#S4.SS2 "4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"), we train multi-task models for ALOHA, DOS-W1, ARX5, and UR5, covering the 30 Table30-V2 tasks.
Starting from expert-trained checkpoints, each model undergoes three rounds of deployment and training using experience from its assigned tasks.
Overall success increases from 23.67% to 28.00%, 37.67%, and 43.33%, while the scores rise from 36.10 to 42.63, 51.65, and 56.80.
Both aggregate metrics improve at every iteration, yielding a 19.7-percentage-point success gain over the initial deployment.
This demonstrates that LoopWAM can use its own deployment experience to improve policies trained across multiple tasks.

Single-task post-training.
We further evaluate shirt folding, a challenging deformable-object manipulation task with diverse and disordered initial configurations.
A shirt is casually tossed into the robot’s workspace, creating varied and messy initial states in which its corners may be hidden.
The robot must identify suitable grasp points and progressively unfold the shirt until its corners are exposed, then grasp these corners to complete the subsequent folds.
We initialize from the DOS-W1 multi-task model trained on Table30-V2 and post-train it on newly collected expert demonstrations of shirt folding.
The resulting task-specific expert-trained checkpoint serves as the starting point for two rounds of deployment and self-improvement.
Success rises from 13.20% to 32.54% and 55.56%, while the scores increase from 14.44 to 38.89 and 67.78.
These gains show that deployment feedback remains effective after adapting a multi-task model to a challenging individual task, supporting closed-loop improvement under both training regimes.

### 4.5 Ablation Study

We use the RoboTwin 2.0 setup in Section [4.2](#S4.SS2 "4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"), varying only quality steering and rollout action supervision; expert action supervision and video supervision remain unchanged.

Table 4: Ablation study on RoboTwin 2.0. We evaluate quality steering with different annotation schemes and assess the effect of quality-weighted rollout action supervision (Act.).

| Quality Steering | Quality-weighted Act. | Clean | Rand. | Average |
| --- | --- | --- | --- | --- |
| None | ✗ | 73.5 | 71.1 | 72.3 |
| Extra-coarse | ✗ | 92.2 | 93.3 | 92.8 |
| Extra-coarse | ✓ | 93.9 | 93.3 | 93.6 |
| Coarse | ✗ | 93.2 | 92.2 | 92.7 |
| Coarse (ours) | ✓ | 94.6 | 94.4 | 94.5 |

Table [4](#S4.T4 "Table 4 ‣ 4.5 Ablation Study ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") compares no steering, extra-coarse annotation, and our coarse-level annotation (Section [3.2](#S3.SS2 "3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")).
Extra-coarse annotation distinguishes rollouts from all policies solely by success or failure: all failed rollouts are assigned Quality: low, all successful rollouts are assigned Quality: medium, and expert demonstrations are assigned Quality: high.
In our coarse-level scheme, successful rollouts from the same policy are assigned a shared numerical score, which can differ across policies according to their overall success rates across tasks and manually assessed motion smoothness.
Failed rollouts are assigned the minimum score, while expert demonstrations are assigned q⋆q^{\star}, above the rollout score range. The ablation results reveal three key findings:
(1) Quality steering is key to learning from mixed-quality deployment rollouts, enabling the model to distinguish trajectories of different quality.
(2) Even extra-coarse labels remain effective, demonstrating that fine-grained annotation is not required to benefit from steering.
(3) Quality-aware rollout action supervision further improves overall performance under both annotation schemes.

## 5 Conclusion

We presented LoopWAM for improving generalist world-action policies directly from deployment experience.
The key is to learn physical consequences from trajectories across the quality spectrum while controlling how their actions supervise behavior.
Source-dependent noise sampling, quality steering, and quality-weighted supervision implement this distinction within joint video–action denoising, allowing consequence representations to participate directly in action generation.
The same formulation accepts rollouts from both LoopWAM and other deployed policies. Experiments show the best overall results: a score of 56.80 and 43.33% success on RoboChallenge Table30-V2, 94.5% average success on RoboTwin 2.0, and 49.5% overall success on RoboCasa365.
Repeated real-robot deployment raises Table30-V2 success by 19.7 percentage points over three rounds and improves shirt-folding success from 13.20% to 55.56% over two rounds after single-task post-training.
These findings support using mixed-quality interaction history as a training resource for continued improvement of both multi-task policies and policies adapted to individual tasks.

## References

* Bi et al. (2025)
  H. Bi, H. Tan, S. Xie, Z. Wang, S. Huang, H. Liu, R. Zhao, Y. Feng, C. Xiang, Y. Rong, et al.
  Motus: A Unified Latent Action World Model.
  arXiv preprint arXiv:2512.13030.
  Cited by: [Table 2](#S4.T2.2.6.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 2](#S4.T2.2.7.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Black et al. (2024)
  K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al.
  π0\pi\_{0}: A Vision-Language-Action Flow Model for General Robot Control.
  arXiv preprint arXiv:2410.24164.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 2](#S4.T2.2.2.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 3](#S4.T3.2.3.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Cai et al. (2026)
  J. Cai, L. Ling, S. Chu, Z. Liu, J. Kang, Z. Liang, W. Xu, Y. Mao, W. Zhang, X. Yang, R. Ying, R. Zheng, and Y. Mu
  AHA-WAM: Asynchronous Horizon-Adaptive World-Action Modeling with Observation-Guided Context Routing.
  arXiv preprint arXiv:2606.09811.
  Cited by: [Table 2](#S4.T2.2.10.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Chen et al. (2026)
  R. Chen, Y. Yang, Z. Tang, D. Huo, T. Lin, H. Wu, H. Liu, Y. Chen, L. Zheng, B. Yuan, et al.
  ABot-M0.5: Unified Mobility-and-Manipulation World Action Model.
  arXiv preprint arXiv:2607.00678.
  Cited by: [Table 3](#S4.T3.2.10.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Chen et al. (2025)
  T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu, et al.
  RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation.
  arXiv preprint arXiv:2506.18088.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§4.2](#S4.SS2.SSS0.Px2.p1.1 "RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Chi et al. (2025)
  C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song
  Diffusion Policy: Visuomotor Policy Learning via Action Diffusion.
  IJRR.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 3](#S4.T3.2.2.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Gao et al. (2026)
  S. Gao, W. Liang, K. Zheng, A. Malik, S. Ye, S. Yu, W. Tseng, Y. Dong, K. Mo, C. Lin, et al.
  DreamDojo: a generalist robot world model from large-scale human videos.
  arXiv preprint arXiv:2602.06949.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Guo et al. (2025)
  Y. Guo, L. X. Shi, J. Chen, and C. Finn
  Ctrl-world: a controllable generative world model for robot manipulation.
  arXiv preprint arXiv:2510.10125.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Johnson et al. (1995)
  N. L. Johnson, S. Kotz, and N. Balakrishnan
  Continuous univariate distributions.
  2nd edition, Vol. 2, John Wiley & Sons.
  External Links: ISBN 9780471584940
  Cited by: [§3.2](#S3.SS2.p2.3 "3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Khazatsky et al. (2024)
  A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al.
  DROID: A Large-Scale In-the-Wild Robot Manipulation Dataset.
  arXiv preprint arXiv:2403.12945.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Kim et al. (2026)
  D. Kim, H. Jang, M. Koo, S. Jang, T. Kim, B. Kim, B. Yoon, C. Jang, D. Choi, D. Han, et al.
  RLDX-1 Technical Report.
  arXiv preprint arXiv:2605.03269.
  External Links: [Link](https://arxiv.org/abs/2605.03269)
  Cited by: [§4.2](#S4.SS2.SSS0.Px3.p1.1 "RoboCasa365. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 3](#S4.T3.2.8.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Kim et al. (2024)
  M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al.
  OpenVLA: An Open-Source Vision-Language-Action Model.
  arXiv preprint arXiv:2406.09246.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Li et al. (2026)
  L. Li, Q. Zhang, Y. Luo, S. Yang, R. Wang, F. Han, M. Yu, Z. Gao, N. Xue, X. Zhu, et al.
  Causal world modeling for robot control.
  arXiv preprint arXiv:2601.21998.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§2](#S2.p2.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§4.2](#S4.SS2.SSS0.Px2.p1.1 "RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 2](#S4.T2.2.8.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Lipman et al. (2023)
  Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le
  Flow Matching for Generative Modeling.
  In International Conference on Learning Representations,
  External Links: [Link](https://arxiv.org/abs/2210.02747)
  Cited by: [§3.1](#S3.SS1.p2.1 "3.1 Joint World–Action Modeling ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Luo et al. (2026)
  H. Luo, W. Zhang, Y. Feng, S. Zheng, H. Xu, C. Xu, Z. Xi, Y. Fu, and Z. Lu
  Being-H0.7: A Latent World-Action Model from Egocentric Videos.
  arXiv preprint arXiv:2605.00078.
  External Links: [Link](https://arxiv.org/abs/2605.00078)
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Nasiriany et al. (2026)
  S. Nasiriany, S. Nasiriany, A. Maddukuri, and Y. Zhu
  RoboCasa365: A Large-Scale Simulation Framework for Training and Benchmarking Generalist Robots.
  arXiv preprint arXiv:2603.04356.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§4.2](#S4.SS2.SSS0.Px3.p1.1 "RoboCasa365. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* NVIDIA et al. (2025)
  NVIDIA, J. Bjorck, F. Castañeda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, et al.
  GR00T N1: An Open Foundation Model for Generalist Humanoid Robots.
  arXiv preprint arXiv:2503.14734.
  Cited by: [Table 3](#S4.T3.2.6.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 3](#S4.T3.2.7.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* O’Neill et al. (2024)
  A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, et al.
  Open X-Embodiment: Robotic Learning Datasets and RT-X Models.
  In 2024 IEEE International Conference on Robotics and Automation (ICRA),
  pp. 6892–6903.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Pai et al. (2025)
  J. Pai, L. Achenbach, V. Montesinos, B. Forrai, O. Mees, and E. Nava
  mimic-video: Video-Action Models for Generalizable Robot Control Beyond VLAs.
  arXiv preprint arXiv:2512.15692.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§2](#S2.p2.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Peng et al. (2026)
  Q. Peng, Y. Liang, R. Yan, N. Hansen, and X. Wang
  FACT: Failure-Aware Causal Training for World-Action Models.
  arXiv preprint arXiv:2608.10232.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Physical Intelligence et al. (2025)
  Physical Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al.
  π0.5\pi\_{0.5}: A Vision-Language-Action Model with Open-World Generalization.
  arXiv preprint arXiv:2504.16054.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§4.2](#S4.SS2.SSS0.Px2.p1.1 "RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 2](#S4.T2.2.4.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 3](#S4.T3.2.4.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Physical Intelligence (2025)
  Physical Intelligence
  π0.6\pi\_{0.6}: A VLA That Learns From Experience.
  arXiv preprint arXiv:2511.14759.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Physical Intelligence (2026)
  Physical Intelligence
  π0.7\pi\_{0.7}: A Steerable Generalist Robotic Foundation Model with Emergent Capabilities.
  arXiv preprint arXiv:2604.15483.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* RoboChallenge Dexmal Team (2026)
  RoboChallenge Dexmal Team
  Table30 V2: Evaluating Generalized Models by Real Robots at Scale.
  Technical report
   Dexmal.
  External Links: [Link](https://robochallenge.ai/robochallenge_techreport_V2.pdf)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§4.2](#S4.SS2.SSS0.Px1.p1.1 "RoboChallenge Table30-V2. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* RoboChallenge (2026)
  RoboChallenge
  RoboChallenge Table30-V2 Leaderboard.
  Note: Accessed September 22, 2026
  External Links: [Link](https://robochallenge.cn/leaderboard?selectBenchmark=table30_v2&currentPage=1&pageSize=30)
  Cited by: [§4.3](#S4.SS3.SSS0.Px1.p1.1 "RoboChallenge Table30-V2. ‣ 4.3 Benchmark Results ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Ross et al. (2011)
  S. Ross, G. Gordon, and D. Bagnell
  A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning.
  In Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics,
  Vol. 15, pp. 627–635.
  External Links: [Link](https://proceedings.mlr.press/v15/ross11a.html)
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Wan et al. (2025)
  T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C. Xie, D. Chen, F. Yu, H. Zhao, J. Yang, et al.
  Wan: open and advanced large-scale video generative models.
  arXiv preprint arXiv:2503.20314.
  Cited by: [§3.1](#S3.SS1.p2.1 "3.1 Joint World–Action Modeling ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§4.1](#S4.SS1.p1.1 "4.1 Implementation Details ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Xiao et al. (2025)
  W. Xiao, H. Lin, A. Peng, H. Xue, T. He, Y. Xie, F. Hu, J. Wu, Z. Luo, L. Fan, G. Shi, and Y. Zhu
  Self-Improving Vision-Language-Action Models with Data Generation via Residual RL.
  arXiv preprint arXiv:2511.00091.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Xu et al. (2026)
  C. Xu, J. T. Springenberg, M. Equi, A. Amin, A. Esmail, S. Levine, and L. Ke
  RL Token: Bootstrapping Online RL with Vision-Language-Action Models.
  arXiv preprint arXiv:2604.23073.
  External Links: [Link](https://arxiv.org/abs/2604.23073)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Yang et al. (2026)
  Y. Yang, S. Zeng, T. Lin, X. Chang, D. Qi, J. Xiao, H. Liu, R. Chen, Y. Chen, D. Huo, et al.
  ABot-M0: VLA Foundation Model for Robotic Manipulation with Action Manifold Learning.
  arXiv preprint arXiv:2602.11236.
  Cited by: [Table 2](#S4.T2.2.5.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 3](#S4.T3.2.11.1.2 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Ye et al. (2026a)
  A. Ye, B. Wang, C. Ni, G. Huang, G. Zhao, H. Li, H. Li, J. Li, J. Lv, J. Liu, et al.
  GigaWorld-Policy: An Efficient Action-Centered World–Action Model.
  arXiv preprint arXiv:2603.17240.
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 3](#S4.T3.2.5.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Ye et al. (2026b)
  S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang, et al.
  World action models are zero-shot policies.
  arXiv preprint arXiv:2602.15922.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [§2](#S2.p2.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Yuan et al. (2026)
  T. Yuan, Z. Dong, Y. Liu, and H. Zhao
  Fast-WAM: Do World Action Models Need Test-time Future Imagination?.
  arXiv preprint arXiv:2603.16666.
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 2](#S4.T2.2.9.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Zhang et al. (2026a)
  Q. Zhang, L. Li, L. Zhang, S. Yang, Y. Luo, S. Li, R. Wang, J. Wang, J. Shao, G. Xu, et al.
  Native Video-Action Pretraining for Generalizable Robot Control.
  arXiv preprint arXiv:2607.08639.
  External Links: [Link](https://arxiv.org/abs/2607.08639)
  Cited by: [§2](#S2.p2.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 2](#S4.T2.2.11.1.2 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Zhang et al. (2026b)
  Y. Zhang, J. Zhao, C. Fan, F. Yan, T. Li, H. Tang, S. Fu, X. Wu, Q. Weng, W. Zhang, X. Li, C. Zhang, C. Bai, and X. Li
  PRTS: A Primitive Reasoning and Tasking System via Contrastive Representations.
  arXiv preprint arXiv:2604.27472.
  Cited by: [Table 3](#S4.T3.2.9.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Zhao et al. (2023)
  T. Z. Zhao, V. Kumar, S. Levine, and C. Finn
  Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware.
  arXiv preprint arXiv:2304.13705.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Zheng et al. (2025)
  J. Zheng, J. Li, Z. Wang, D. Liu, X. Kang, Y. Feng, Y. Zheng, J. Zou, Y. Chen, J. Zeng, et al.
  X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model.
  arXiv preprint arXiv:2510.10274.
  Cited by: [§4.2](#S4.SS2.SSS0.Px2.p1.1 "RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"),
  [Table 2](#S4.T2.2.3.1.1 "In RoboTwin 2.0. ‣ 4.2 Benchmark Experimental Setup ‣ 4 Experiments ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Zhou et al. (2026)
  P. Zhou, S. Chen, D. Chen, J. Wang, R. Jin, B. Zhu, Y. Pan, S. Gu, K. Wang, S. Nan, X. Qiu, C. Qiu, P. Yang, Y. Cai, J. Gao, Y. Li, Y. Fu, X. Yue, Z. Chen, and J. Luo
  τ0\tau\_{0}-WM: A Unified Video-Action World Model for Robotic Manipulation.
  arXiv preprint arXiv:2606.01027.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Zhu et al. (2025)
  C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta
  Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets.
  External Links: 2504.02792,
  [Link](https://arxiv.org/abs/2504.02792)
  Cited by: [§3.1](#S3.SS1.p1.2 "3.1 Joint World–Action Modeling ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").
* Zitkovich et al. (2023)
  B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al.
  RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control.
  In Conference on Robot Learning,
  pp. 2165–2183.
  Cited by: [§2](#S2.p1.1 "2 Related Work ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts").

## Appendix A Training and Data Processing Details

### A.1 Trajectory-Quality Annotations

We use two numerical quality scales according to annotation granularity.
*Episode-level annotation* uses a 1–12 scale, with rollout scores in [1,10][1,10] and expert demonstrations assigned q⋆=12q^{\star}=12.
*Coarse-level annotation* uses a 1–5 scale, with rollout scores in {1,2,3,4}\{1,2,3,4\} and expert demonstrations assigned q⋆=5q^{\star}=5.
In all settings, every failed trajectory receives q=1q=1.
Expert demonstrations are treated as optimal reference trajectories and assigned scores above the rollout range; the same expert score is used at deployment.
Each score is assigned to a complete trajectory and inherited by all training segments extracted from it.

RoboChallenge Table30-V2.
We use human episode-level annotations from the official RoboChallenge platform.
Platform operators already rate each rollout on a 1–10 scale according to task completion, with successful trajectories typically receiving scores of at least 8.5.
We directly use these platform ratings as rollout quality scores, except that all failed trajectories are assigned q=1q=1.
Expert demonstrations receive q⋆=12q^{\star}=12.

Single-task shirt-folding post-training.
We likewise use human episode-level annotation.
After each rollout, the data collector assesses task completion before resetting the scene and assigns a score on a 1–10 scale, following the same completion-based scoring approach as RoboChallenge.
Failed trajectories receive q=1q=1, and task-specific expert demonstrations receive q⋆=12q^{\star}=12.

RoboTwin 2.0.
We apply coarse-level annotation separately to rollouts from expert-trained LoopWAM, X-VLA, and π0.5\pi\_{0.5}.
For each policy, we compute its overall rollout success rate across all tasks and manually inspect approximately 0.7% of its trajectories for motion smoothness and action accuracy.
These two assessments determine a single shared score for all successful trajectories from that policy across tasks; every failed trajectory receives q=1q=1.
Expert-trained LoopWAM achieves approximately 90% success during rollout collection and produces relatively smooth trajectories, so its successful rollouts receive q=4q=4.
X-VLA and π0.5\pi\_{0.5} each achieve less than 50% success and produce less smooth trajectories, so their successful rollouts receive q=3q=3.
Expert demonstrations receive q⋆=5q^{\star}=5.

RoboCasa365.
We use the same coarse-level protocol, assessing each source policy through its overall rollout success rate across tasks and manual inspection of approximately 0.7% of its trajectories for motion smoothness and action accuracy.
We obtain two expert-trained LoopWAM policies using 64-step and 32-step action chunks, denoted Policy 1 and Policy 2, respectively, and also collect rollouts from RLDX-1.
Following the same scoring criteria as RoboTwin, all successful rollouts from Policy 1 share q=3q=3, those from Policy 2 share q=4q=4, and those from RLDX-1 share q=2q=2.
All failed rollouts receive q=1q=1, and expert demonstrations receive q⋆=5q^{\star}=5.

### A.2 Training Details

Temporal alignment and robot representations.
The training configurations use an action horizon of H=64H=64 and a visual stride of eight control steps, yielding nine RGB frames including the initial observation.
Camera views are stitched into a single image, and robot states and actions are normalized using expert-data statistics.
For Table30-V2, joint targets are represented relative to the joint state at the beginning of each action chunk, whereas gripper commands remain absolute.
Only the joint components are converted back to absolute targets at execution; the gripper components are not differenced.
To reduce redundant stationary data, the real-world pipeline checks unnormalized state sequences with an absolute tolerance of 10−310^{-3} and resamples nearly static windows up to three times.
Windows starting within the final 20 seconds of expert episodes are exempt from this filtering to retain terminal behavior.
Padding is excluded from the denoising losses.

Noise schedules and loss weighting.
The base noise sampler uses ϕ5​(u)=5​u/(1+4​u)\phi\_{5}(u)=5u/(1+4u) for u∼𝒰⁡(0,1)u\sim\mathcal{U}(0,1).
Samples drawn from the Beta distributions in Equation [4](#S3.E4 "In 3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") are clipped to [10−4,1−10−4][10^{-4},1-10^{-4}] without a further time shift.
Both modalities use the same scheduler weighting function in Equation [5](#S3.E5 "In 3.2 Quality-Aware Learning from Mixed Trajectories ‣ 3 Method ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts"):

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | g⁡(σ)\displaystyle g(\sigma) | =exp[−2(σ−12)2]−e−1/2,\displaystyle=\exp\!\left[-2(\sigma-\tfrac{1}{2})^{2}\right]-e^{-1/2}, |  | (8) |
|  | ω⁡(σ)\displaystyle\omega(\sigma) | =g⁡(σ)C+10−10,C=1T∑j=0T−1g(ϕ5(1−j/T)),T=1000.\displaystyle=\frac{g(\sigma)}{C+10^{-10}},\qquad C=\frac{1}{T}\sum\_{j=0}^{T-1}g\!\left(\phi\_{5}(1-j/T)\right),\quad T=1000. |  |

This normalization is shared by expert and rollout samples.
For KK inference steps, the schedule is σk=ϕ5​(1−k/K)\sigma\_{k}=\phi\_{5}(1-k/K), k=0,…,Kk=0,\ldots,K.
Each modality follows the Euler update
Xmk+1=Xmk+(σk+1−σk)​vθmX\_{m}^{k+1}=X\_{m}^{k}+(\sigma\_{k+1}-\sigma\_{k})v\_{\theta}^{m},
with the vector fields evaluated jointly and the initial observation latent fixed throughout sampling.

### A.3 Table30-V2 Subtask Segmentation

We use Qwen2.5-VL-7B for subtask segmentation, switching between stage-specific language instructions during online robot execution.
Table [5](#A1.T5 "Table 5 ‣ A.3 Table30-V2 Subtask Segmentation ‣ Appendix A Training and Data Processing Details ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") lists the resulting ordered prompts.
The four illustrated tasks are button pressing, plant watering, paper shredding, and stamp positioning. The remaining tasks retain their original full-task instructions.

Table 5: Table30-V2 subtask instructions, listed in execution order.

| Task | Robot | Ordered subtask instructions |
| --- | --- | --- |
| Press the button | ARX5 | 1. Press the pink button.  2. Press the blue button.  3. Press the green button.  4. Press the yellow button, then retract the gripper. |
| Water the flowers | ARX5 | 1. Pick up the watering can and water the potted plant.  2. The watering is finished, put the watering can down. |
| Shred paper | UR5 | 1. Put the paper into the shredder.  2. Retract gripper. |
| Stamp positioning | ALOHA | 1. Pick up the stamp.  2. Dip into the ink.  3. Stamp the signature area and return. |

### A.4 Subtask Switching Examples

Figures [4](#A1.F4 "Figure 4 ‣ A.4 Subtask Switching Examples ‣ Appendix A Training and Data Processing Details ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts")–[7](#A1.F7 "Figure 7 ‣ A.4 Subtask Switching Examples ‣ Appendix A Training and Data Processing Details ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") show one trajectory for each of the four tasks.
The first image is the stitched policy input at the start of execution; each subsequent image is captured when the active subtask prompt changes.
The associated text gives the instruction used for the new stage.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/press_the_button/init.png)

Stage 1. Press the pink button.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/press_the_button/01_press_2.png)

Stage 2. Press the blue button.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/press_the_button/02_press_3.png)

Stage 3. Press the green button.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/press_the_button/03_press_4.png)

Stage 4. Press the yellow button, then retract the gripper.

Figure 4: Button pressing (ARX5). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/water_the_flowers/init.png)

Stage 1. Pick up the watering can and water the potted plant.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/water_the_flowers/01_place.png)

Stage 2. The watering is finished, put the watering can down.

Figure 5: Plant watering (ARX5). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/shred_paper/init.png)

Stage 1. Put the paper into the shredder.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/shred_paper/01_retract.png)

Stage 2. Retract gripper.

Figure 6: Paper shredding (UR5). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/stamp_positioning/init.png)

Stage 1. Pick up the stamp.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/stamp_positioning/01_dip.png)

Stage 2. Dip into the ink.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30_subtask_keyframes_train/stamp_positioning/02_stamp.png)

Stage 3. Stamp the signature area and return.

Figure 7: Stamp positioning (ALOHA). Subtask segmentation example. The initial observation (Stage 1) and subsequent stage observations are shown in order, each paired with its subtask instruction.

## Appendix B RoboChallenge Table30-V2 Leaderboard

Figure [8](#A2.F8 "Figure 8 ‣ Appendix B RoboChallenge Table30-V2 Leaderboard ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") presents the official RoboChallenge Table30-V2 leaderboard at the time of evaluation.
LoopWAM ranks first, achieving an overall score of 56.80 and a success rate of 43.33%.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/table30v2-leaderboard.png)

Figure 8: RoboChallenge Table30-V2 leaderboard. LoopWAM ranks first with an overall score of 56.80 and a success rate of 43.33%, using a multi-task policy for each embodiment.

## Appendix C Failure Recovery and Iterative Execution

Real-world robot manipulation often involves uncertainty caused by
imperfect perception, inaccurate execution, and complex object
interaction dynamics.

To analyze the ability of LoopWAM to support iterative execution,
Figure [9](#A3.F9 "Figure 9 ‣ Appendix C Failure Recovery and Iterative Execution ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") presents qualitative examples where an
initial attempt does not complete the desired task.

After observing the resulting environment state, the model generates
subsequent corrective behaviors that improve the execution outcome.
These examples highlight the importance of modeling future states and
environment transitions beyond predicting isolated actions.

![Refer to caption](https://arxiv.org/html/2610.18873v2/retry-sucess.png)

Figure 9:
Qualitative examples of iterative execution and failure recovery.
The first attempt may fail due to execution uncertainty,
incomplete interaction, or object displacement.
Subsequent attempts generate corrective behaviors and achieve
successful task completion.

## Appendix D Qualitative Future Observation Prediction

As a learned robot world model, LoopWAM predicts future visual
observations conditioned on the current robot state and interaction
history.

To further examine the learned visual dynamics,
Figure [10](#A4.F10 "Figure 10 ‣ Appendix D Qualitative Future Observation Prediction ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") compares predicted future frames with
ground-truth observations from robot executions.

The predictions capture major aspects of scene evolution, including
robot motion, object movement, and manipulation progress.
Although generated observations may differ from the ground-truth images
in fine visual details, they preserve the temporal structure of the
interaction process.

![Refer to caption](https://arxiv.org/html/2610.18873v2/video-pred-1.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/video-pred-2.png)

Figure 10:
Qualitative comparison between predicted future observations from
LoopWAM and ground-truth robot executions.
The model captures the temporal evolution of robot-object
interactions and predicts plausible future visual states.

## Appendix E Representative Robot Platforms and Tasks

LoopWAM is evaluated across multiple robot platforms with different
embodiments, sensing configurations, and manipulation spaces.

To demonstrate the diversity of learned robot behaviors, we provide
additional qualitative examples from ARX, ALOHA, UR5, and W1 platforms.
The examples cover object manipulation, coordinated control,
fine-grained interaction, and long-horizon tasks.

Figure [11](#A5.F11 "Figure 11 ‣ Appendix E Representative Robot Platforms and Tasks ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") shows representative tasks on the ARX platform.
Figure [12](#A5.F12 "Figure 12 ‣ Appendix E Representative Robot Platforms and Tasks ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") presents examples from the ALOHA platform,
which includes coordinated manipulation behaviors.
Figure [13](#A5.F13 "Figure 13 ‣ Appendix E Representative Robot Platforms and Tasks ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") demonstrates single-arm manipulation tasks on
the UR5 platform.
Finally, Figure [14](#A5.F14 "Figure 14 ‣ Appendix E Representative Robot Platforms and Tasks ‣ LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts") presents representative long-horizon
tasks from the W1 platform.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/arx-01.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/arx-02.png)

Figure 11:
Representative tasks on the ARX robot platform.
The examples illustrate diverse manipulation scenarios used for
evaluating LoopWAM across different robot embodiments.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/aloha-01.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/aloha-02.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/aloha-03.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/aloha-04.png)

Figure 12:
Representative tasks on the ALOHA robot platform.
The examples include coordinated manipulation and object
interaction requiring temporally consistent control.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/ur5-01.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/ur5-02.png)

Figure 13:
Representative tasks on the UR5 robot platform.
The examples demonstrate single-arm manipulation in structured
environments.

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/w1-01.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/w1-02.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/w1-03.png)

![Refer to caption](https://arxiv.org/html/2610.18873v2/figures/lyp/w1-04.png)

Figure 14:
Representative long-horizon tasks on the W1 robot platform.
The examples demonstrate sequential manipulation behaviors in
complex environments.