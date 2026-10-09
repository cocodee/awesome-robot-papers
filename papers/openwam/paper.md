# OpenWAM: An Open Framework for Composable World-Action Models

> Markdown conversion of the [arXiv HTML version](https://arxiv.org/html/2610.07922v1) of the same paper. See [PDF](paper.pdf) and [LaTeX source](source/main.tex) for authoritative figures, tables, and equations.

Heng Yu

David D. Yuan

Juze Zhang

Changan Chen

Yao Feng

Michelle Baldonado

Steve Cousins

Li Fei-Fei

Jiajun Wu

Ehsan Adeli
Affiliation: Stanford University

###### Abstract

World–action models (WAMs) couple future prediction with robot control, yet
existing systems often vary the video backbone, interaction structure,
supervision, and inference procedure simultaneously, making their design
choices difficult to compare. We introduce OpenWAM, an open
world–action modeling framework built around a common causal robot-video
foundation and configurable video–action interaction.
Starting from Wan2.2-5B, we perform causal robot-video pretraining on over 10,000 hours of video, then integrate an action expert through a shared Mixture-of-Transformers architecture that supports joint, video-then-action, action-then-video, and decoupled generation.
OpenWAM achieves high success rates on four LIBERO suites and real-world bimanual tasks; robot-video training with causal adaptation improves VTA success on LIBERO-Long from 68.4% to 97.8%.
The same configurable architecture naturally extends to inverse and forward
dynamics, allowing us to study how counterfactual transitions improve
independently trained dynamics models beyond demonstrations alone.
When only the video predictor is adapted to a new task, a frozen local-context
inverse dynamics model trained on counterfactual data and demonstrations achieves 84.0% mean success across four held-out
LIBERO-90 tasks, compared with 47.0% for a full-context inverse model and
21.5% for a local-context model trained only on demonstrations.
For forward dynamics, counterfactual supervision reduces RGB prediction error by
34.5% and raises outcome identification from 21.1% to 71.3% among 16
same-state outcomes.
OpenWAM provides a common testbed for comparing WAM interaction designs and for studying dynamics learning from video data beyond successful demonstrations.

## 1 Introduction

World-action models (WAMs) integrate future-observation prediction with robot control. Recent systems such as DreamZero [[90](#bib.bib21)], DVA [[71](#bib.bib67)] and LingBot-VA [[43](#bib.bib29), [97](#bib.bib60)] use pretrained video models to couple future-observation prediction with robot action generation. However, differences in their backbones, training data, objectives, and inference procedures make it difficult to isolate the effect of video–action interaction.

![Refer to caption](../../assets/openwam/figure-1.png)

Figure 1:
Overview of OpenWAM.
Left: Starting from Wan2.2 [[75](#bib.bib19)], causal pretraining on robot and
human-interaction video builds a predictive backbone without action labels,
followed by video–action training on simulated and real-robot demonstrations.
Top right: A shared Mixture-of-Transformers couples temporally
aligned video and action streams through joint attention while retaining
modality-specific experts.
Middle right: Configurable cross-modal attention and generation
order support joint, video-then-action, action-then-video, and decoupled
prediction within the same architecture.
Bottom right: Local-context inverse and forward dynamics models
are trained independently using demonstrations and counterfactual
transitions. A frozen IDM translates predictions from compatible
task-adapted video models into actions, while an FDM predicts the visual
consequences of candidate actions.

Two challenges arise when studying these systems systematically. First, video–action interaction spans multiple choices: video and actions can be generated jointly, sequentially, or through restricted cross-modal connections. A shared architecture and evaluation protocol would allow these interaction patterns and generation orders to be compared under controlled conditions.
Second, successful demonstrations cover only a limited subset of possible action–outcome relationships. Other interactions, including failures, exploratory behavior, and counterfactual rollouts, can provide additional supervision about local dynamics. However, it remains unclear whether such data can improve the reuse of an action-grounding component when the visual predictor is adapted to a new task. We study this question by independently training local-context dynamics models and evaluating their transfer across adapted video predictors.

To this end, we introduce OpenWAM, an open framework and model series for controlled world–action modeling, summarized in Figure [1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models"). Starting from a pretrained general-purpose video model, we adapt its visual prior through causal robot-video training without action labels, then introduce an action branch through a Mixture-of-Transformers (MoT) architecture [[49](#bib.bib51)]. The resulting model supports joint, sequential, and restricted video–action interaction. These configurations share the video initialization, representations, and evaluation pipeline, allowing us to compare how their interaction patterns affect the control performance.

Furthermore, OpenWAM trains local-context inverse and forward models independently. The inverse model predicts actions from the current observation and a future visual trajectory, while the forward model predicts that trajectory from supplied actions.
In simulation, we broaden their training data by executing alternative action sequences from the same initial state.
This local-transition formulation is also compatible with failed and exploratory interactions, because it does not require a successful task outcome or a success label.
Each recorded transition supplies dynamics supervision regardless of whether it completes the task. At inference, a video predictor can propose a visual trajectory and a separately trained inverse model can translate it into executable actions.

We evaluate robot-video pretraining, closed-loop policy success across
video–action interaction modes and dynamics-component reuse. In transfer experiments, task-adapted video predictors are paired with frozen inverse models to compare demonstration-only with counterfactual-augmented supervision and local-context with full-context conditioning. We additionally evaluate forward prediction under alternative actions from the same initial state.

This work makes three contributions:

* •

  A controlled WAM framework. OpenWAM combines a causal video backbone with configurable video–action models under shared training and evaluation protocols.
* •

  Local-context dynamics interfaces. We independently train inverse- and forward-dynamics models from demonstrations and broader local transitions and evaluate their composition with separately trained predictors.
* •

  Controlled empirical analysis. We measure the effects of robot-video pretraining, interaction design, transition coverage, and conditioning context on policy performance and component reuse.

## 2 Related Work

### 2.1 Visuomotor Policies and Predictive Control

Behavior cloning provides the standard supervised formulation for visuomotor
policy learning, mapping observations and task context directly to demonstrated
actions. Action chunking and generative action prediction have become effective
control primitives [[101](#bib.bib9), [12](#bib.bib10)], while large-scale
vision–language–action models extend this paradigm through language
conditioning, pretraining, and cross-task or cross-embodiment learning
[[8](#bib.bib1), [7](#bib.bib2), [38](#bib.bib5), [6](#bib.bib7), [33](#bib.bib8), [58](#bib.bib3), [70](#bib.bib4)].

Predictive control introduces an additional interface by explicitly modeling
future observations or latent states. Early visual-foresight methods combined
action-conditioned video prediction with model-predictive control for robotic
manipulation [[17](#bib.bib99), [16](#bib.bib100)]. Subsequent work learns latent
or visual dynamics to support policy learning, planning, and imagined rollouts
[[24](#bib.bib12), [25](#bib.bib13), [82](#bib.bib14), [80](#bib.bib16), [11](#bib.bib17), [107](#bib.bib18)]. Predictive rollouts have also been used to evaluate policy behavior [[47](#bib.bib30), [22](#bib.bib31)].

Action-conditioned world models provide a complementary perspective by
predicting how an environment evolves under supplied or candidate actions.
Recent methods use such predictions for simulation, candidate evaluation,
proposal refinement, and self-verifying planning
[[31](#bib.bib24), [106](#bib.bib37), [61](#bib.bib98), [95](#bib.bib38)]. Together, these lines show that predictive models can
support action generation, simulation, planning, and evaluation. However,
action-conditioned prediction and video–action policy generation are often
developed as separate components, leaving open how explicit
prediction–action interfaces affect component reuse across tasks.

### 2.2 Video Foundations and World–Action Architectures

Recent world–action models connect predictive video representations with
robot control through several forms of video–action coupling. Joint
generation models predict future visual content and actions together
[[90](#bib.bib21), [1](#bib.bib68), [66](#bib.bib34), [21](#bib.bib75)], while
causal video-first formulations generate or represent visual futures before
action prediction [[43](#bib.bib29), [71](#bib.bib67)]. Other architectures use
specialized video and action pathways with explicit cross-modal exchange
[[87](#bib.bib76), [96](#bib.bib77)], or leverage egocentric and large-scale
video priors for robot grounding and generalization
[[41](#bib.bib35), [105](#bib.bib49), [85](#bib.bib50), [62](#bib.bib78)].

A closely related line studies the interface between predictive visual
information and executable actions. Predicted visual states or representations
can condition inverse dynamics [[72](#bib.bib61), [26](#bib.bib62), [46](#bib.bib108)], while
other approaches translate generated futures through dense correspondence,
pseudo-action labeling, intermediate denoising features, or latent
representation alignment
[[39](#bib.bib63), [34](#bib.bib64), [55](#bib.bib79), [74](#bib.bib80)]. These methods differ in where and how predictive visual
information enters the action-generation pathway.

Unified formulations instead expose multiple predictive and control modes
within a shared system. UWM and UVA [[108](#bib.bib65), [45](#bib.bib20)]
support combinations of policy, inverse-dynamics, forward-dynamics, and video
prediction objectives, while related systems combine action generation with
world prediction, simulation, planning, or evaluation
[[10](#bib.bib26), [37](#bib.bib81), [68](#bib.bib44), [4](#bib.bib45), [20](#bib.bib28)].

Recent work further isolates particular choices in the WAM design space.
Predictive computation can be reduced, sparsified, reordered, or scheduled
asynchronously
[[94](#bib.bib22), [69](#bib.bib39), [77](#bib.bib40), [89](#bib.bib82), [48](#bib.bib83), [29](#bib.bib84), [28](#bib.bib85), [59](#bib.bib36)]. Alternative work studies the
representation through which world prediction interacts with control
[[53](#bib.bib23), [76](#bib.bib25), [63](#bib.bib86), [99](#bib.bib87), [67](#bib.bib88), [92](#bib.bib89), [35](#bib.bib90)], or augments
world–action learning with structural, geometric, and tactile supervision
[[104](#bib.bib41), [18](#bib.bib42), [56](#bib.bib43)]. Temporal
abstraction, data and model scaling, humanoid control, and long-horizon memory
provide additional design axes
[[44](#bib.bib91), [52](#bib.bib92), [103](#bib.bib93), [100](#bib.bib94)];
recent surveys summarize the rapidly expanding landscape
[[78](#bib.bib95), [54](#bib.bib96)].

Concurrent work, also named OpenWAM [[79](#bib.bib97)], develops a modular
framework for systematic WAM pretraining and design studies. Our focus is
complementary: OpenWAM fixes a common causal robot-video foundation and training
interface while explicitly varying generation order and future cross-modal
visibility, enabling joint, video-then-action, action-then-video, and decoupled
interaction to be compared under a shared evaluation protocol. We further study
the reuse of independently trained inverse- and forward-dynamics components
through explicit trajectory interfaces.

### 2.3 Dynamics Learning Beyond Successful Demonstrations

Successful demonstrations provide valid transitions, but they cover only the
action–outcome relationships selected by the demonstrating policy. A
complementary analysis shows that observational demonstrations alone may not
identify the consequences of unsupported actions [[93](#bib.bib48)].
Classical imitation-learning methods address the resulting distribution shift
by collecting supervision on learner-visited states, perturbing expert
trajectories, or soliciting corrective interventions
[[65](#bib.bib69), [40](#bib.bib66), [57](#bib.bib70), [27](#bib.bib71), [32](#bib.bib72)]. These approaches broaden state coverage beyond clean
expert rollouts and improve robustness to execution errors.

More recent work expands supervision through synthetic failures,
counterfactual augmentation, autonomous experience, and other non-successful
interactions
[[2](#bib.bib101), [15](#bib.bib73), [42](#bib.bib74), [98](#bib.bib102), [91](#bib.bib33), [60](#bib.bib46), [4](#bib.bib45), [88](#bib.bib47)].
Such data have been used for recovery, policy improvement, failure
understanding, and predictive modeling. Particularly related to our setting,
Fail2Progress [[30](#bib.bib103)] targets data collection toward
observed failures to improve skill-effect models, while
UniPi [[14](#bib.bib15)] decouples video planning from inverse dynamics and
allows the inverse model to learn from a separate, potentially suboptimal
dataset.

OpenWAM focuses on a different question: how transition coverage and conditioning
scope affect the reuse of independently trained dynamics components after
visual task adaptation. We branch alternative action continuations from
task-relevant simulator states and use the resulting state–action–outcome
transitions as local dynamics supervision.

## 3 Methodology

We develop OpenWAM as an open framework for composing world prediction and
action generation. It combines three ingredients: a causal video backbone
pretrained on robot video without action labels, a common video–action
architecture whose cross-modal interaction can be reconfigured, and
separately trained inverse and forward dynamics components operating through
local trajectory interfaces.

The design supports two forms of composition. At the *architectural*
level, we vary how future observation and action streams interact while
retaining a common backbone and objective family. At the
*component* level, we connect independently trained predictors through
explicit future-observation and action-trajectory interfaces. The latter
motivates local-context dynamics models that do not require the language and
nonlocal history used by a task-conditioned generator.

### 3.1 World–Action Modeling Formulation

Let ot∈𝒪o\_{t}\in\mathcal{O}, at∈𝒜a\_{t}\in\mathcal{A}, qt∈𝒬q\_{t}\in\mathcal{Q}, and ℓ∈ℒ\ell\in\mathcal{L} denote the visual observation, action, proprioceptive state, and language instruction at time tt. For fixed observation- and action-history lengths Ko∈ℕK\_{o}\in\mathbb{N} and Ka∈ℕK\_{a}\in\mathbb{N}, respectively, we define

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Ot−\displaystyle O\_{t}^{-} | =(ot−Ko,…,ot−1),\displaystyle=(o\_{t-K\_{o}},\ldots,o\_{t-1}), |  | (1) |
|  | At−\displaystyle A\_{t}^{-} | =(at−Ka,…,at−1),\displaystyle=(a\_{t-K\_{a}},\ldots,a\_{t-1}), |  |
|  | Ot0\displaystyle O\_{t}^{0} | =ot.\displaystyle=o\_{t}. |  |

Let H∈ℕ>0H\in\mathbb{N}\_{>0} denote the prediction horizon. The future action and observation trajectories are defined as

|  |  |  |  |
| --- | --- | --- | --- |
|  | At+=(at,…,at+H−1),Ot+=(ot+1,…,ot+H).A\_{t}^{+}=(a\_{t},\ldots,a\_{t+H-1}),\quad O\_{t}^{+}=(o\_{t+1},\ldots,o\_{t+H}). |  | (2) |

We collect the information available before predicting the future into the task context

|  |  |  |
| --- | --- | --- |
|  | 𝒞t=(Ot−,Ot0,At−,qt,ℓ).\mathcal{C}\_{t}=(O\_{t}^{-},O\_{t}^{0},A\_{t}^{-},q\_{t},\ell). |  |

Recorded future trajectories are denoted without hats, whereas generated trajectories are denoted by O^t+\hat{O}\_{t}^{+} and A^t+\hat{A}\_{t}^{+}. We omit the time index tt when it is unambiguous.

OpenWAM models future observations and actions jointly. For a reference
joint distribution, the two chain-rule factorizations are

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | pWAM​(Ot+,At+∣𝒞t)\displaystyle p\_{\mathrm{WAM}}(O\_{t}^{+},A\_{t}^{+}\mid\mathcal{C}\_{t}) | =p⁡(Ot+∣𝒞t)⏟CVP​p⁡(At+∣Ot+,𝒞t)⏟IDM\displaystyle=\underbrace{p(O\_{t}^{+}\mid\mathcal{C}\_{t})}\_{\mathrm{CVP}}\underbrace{p(A\_{t}^{+}\mid O\_{t}^{+},\mathcal{C}\_{t})}\_{\mathrm{IDM}} |  | (3) |
|  |  | =p⁡(At+∣𝒞t)⏟VLA​p⁡(Ot+∣At+,𝒞t)⏟FDM.\displaystyle=\underbrace{p(A\_{t}^{+}\mid\mathcal{C}\_{t})}\_{\mathrm{VLA}}\underbrace{p(O\_{t}^{+}\mid A\_{t}^{+},\mathcal{C}\_{t})}\_{\mathrm{FDM}}. |  |

Causal video prediction (CVP) proposes future observations, a direct
vision–language–action (VLA) policy proposes actions, inverse dynamics
(IDM) grounds a supplied visual transition into actions, and forward
dynamics (FDM) predicts the visual consequence of supplied actions.

These roles give three primary generation routes.
*Joint generation* produces future observations and actions
concurrently. *Video-then-action (VTA)* first generates a visual
future and then conditions action generation on that trajectory.
*Action-then-video (ATV)* first proposes actions and then predicts
their visual consequences. These factorizations specify modeling
interfaces; they do not require all factors to share one trained
parameterization or final checkpoint.

### 3.2 An Open Causal Robot-Video Backbone

We initialize the video backbone from Wan2.2-5B [[75](#bib.bib19)] and
continue pretraining it on heterogeneous robot-manipulation and interaction
videos without action supervision. This stage adapts a general-purpose video
prior to robot-centric motion and interaction while preserving a standalone
video-prediction interface. The resulting checkpoint is shared across all
downstream OpenWAM variants, allowing different video–action interaction
strategies to be compared under a common visual initialization. Dataset
composition and optimization details are summarized in
Sec. [4.1](#S4.SS1 "4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").

Because the original video model is not temporally causal, we introduce
chunk-causal prediction during robot-video pretraining. A future chunk may
attend to the current and preceding observations and previously generated
chunks, but not to later chunks; tokens within a chunk are processed
jointly. This provides the temporal direction needed for sequential
prediction while retaining within-chunk denoising.

Temporal causality and cross-modal interaction are separate design
dimensions. Chunk causality determines which times are visible, while the
interaction programs in Sec. [3.3](#S3.SS3 "3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models") determine which
observation and action streams communicate. The pretrained causal backbone
can therefore be used directly as a video predictor or coupled to an action
branch without changing its basic predictive interface.

### 3.3 Configurable Video–Action Interaction Programs

#### Shared architecture.

We couple the pretrained video backbone to a separate action
transformer using a Mixture-of-Transformers (MoT) architecture [[49](#bib.bib51)]. Video and
action trajectories are encoded into temporally aligned streams and
processed by modality-specific transformer branches. Interleaved
cross-modal attention determines how information flows between them. The
backbone, tokenization, and objective family are shared across
configurations; future cross-modal visibility and generation order are the
principal variables. Figure [2](#S3.F2 "Figure 2 ‣ Shared architecture. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models") summarizes the
architecture, and Figure [3](#S3.F3 "Figure 3 ‣ Interaction programs. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models") the attention masks of four
interaction programs together with the two local-context dynamics programs.

Figure 2:
Shared MoT architecture. Two modality-specific branches keep their own
normalization, projection and feed-forward parameters and meet in a single
attention over the packed video and action tokens; a separate
cross-attention consumes the task text. Noisy future tokens enter at the
bottom and the preceding chunks sit behind as history context.

#### Interaction programs.

We study four video–action interaction programs under a shared
Mixture-of-Transformers backbone. *Joint* denoises future video and
action streams concurrently, with bidirectional attention between their
noisy future tokens. *VTA* first predicts future video without access
to future actions, then predicts the action conditioned on the
completed visual trajectory. *ATV* reverses this order: it first
predicts the action, then conditions video prediction on the
completed action trajectory. *Decoupled* predicts both modalities
without future cross-modal attention. All four programs use the same backbone, tokenization, and
training objective; they differ only in generation order and future
cross-modal attention.

Figure 3:
Attention masks the shared architecture exposes: four interaction programs
(A–D) and the two local-context dynamics programs (E–F). Columns are the
streams a row may condition on, cell colour gives what it attends to there,
and the numeral marks the generation pass. E and F carry one row each
because each predicts a single stream: the inverse model produces actions, the forward model observations.

Table 1: LIBERO-90 targets used for component-transfer evaluation.

| Task | Target behavior | Transfer challenge |
| --- | --- | --- |
| 64 | Stack bowls; place stack in tray | Novel skill composition |
| 74 | Book into caddy’s left compartment | Retarget familiar manipulation |
| 21 | Turn on stove; place frying pan on it | Object and grasp change |
| 45 | Same objective as Task 21 | Additional scene and layout shift |

![Refer to caption](../../assets/openwam/figure-4.png)

Figure 4: Evaluation tasks. Left: the three real-world bimanual
tasks of Table [2](#S4.T2 "Table 2 ‣ Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models"), each shown as frames sampled
along one successful rollout. Right: the four LIBERO-90 targets of Table [1](#S3.T1 "Table 1 ‣ Interaction programs. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models") used for component transfer, which lie
outside the LIBERO-Long source-task set.

#### Shared flow-matching objective.

All programs use the same latent flow-matching [[50](#bib.bib105)] construction. For target
modality P∈{O,A}P\in\{\mathrm{O},\mathrm{A}\}, let ZP⋆Z\_{P}^{\star} be its clean target
latent. With τ∼𝒰⁡[0,1]\tau\sim\mathcal{U}[0,1] and
ϵP∼𝒩⁡(0,I)\epsilon\_{P}\sim\mathcal{N}(0,I),

|  |  |  |  |
| --- | --- | --- | --- |
|  | ZP,τ=(1−τ)​ϵP+τ​ZP⋆,uP=ZP⋆−ϵP.Z\_{P,\tau}=(1-\tau)\epsilon\_{P}+\tau Z\_{P}^{\star},\quad u\_{P}=Z\_{P}^{\star}-\epsilon\_{P}. |  | (4) |

An active prediction stage minimizes

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒP=𝔼⁡[‖vθ,P​(ZP,τ∣cP,τ)−uP‖22],\mathcal{L}\_{P}=\mathbb{E}\!\left[\left\|v\_{\theta,P}\!\left(Z\_{P,\tau}\mid c\_{P},\tau\right)-u\_{P}\right\|\_{2}^{2}\right], |  | (5) |

where cPc\_{P} denotes the history, side information, and cross-modal
trajectory made visible by the interaction program. Programs with
multiple targets sum the corresponding losses. Observation and
action trajectories used as conditioning are processed through their
respective modality encoders.

During training, a sequential program uses teacher forcing: the second
generation pass conditions on the recorded cross-modal trajectory rather than
on an output sampled by the first pass. At inference, it conditions on the
completed trajectory generated by the first pass. The same interaction program
and temporal alignment are used during training and inference; the source of the conditioning trajectory changes
from recorded to generated.

### 3.4 Counterfactual Learning of Local-Context Dynamics Interfaces

#### Local-context dynamics interfaces.

Architectural composition controls communication within a model, but
reusing a separately trained component requires an explicit conditioning
boundary. A task-conditioned generator may use language and nonlocal
history to specify behavior; a reusable local dynamics component instead
relates a supplied transition to its actions, or supplied actions to their
consequences.

We therefore define

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | pIDMlocal\displaystyle p\_{\mathrm{IDM}}^{\mathrm{local}} | :=p⁡(At+∣Ot+,Ot0,qt),\displaystyle:=p(A\_{t}^{+}\mid O\_{t}^{+},O\_{t}^{0},q\_{t}), |  | (6) |
|  | pFDMlocal\displaystyle p\_{\mathrm{FDM}}^{\mathrm{local}} | :=p⁡(Ot+∣At+,Ot0,qt).\displaystyle:=p(O\_{t}^{+}\mid A\_{t}^{+},O\_{t}^{0},q\_{t}). |  |

Local-context IDM grounds a supplied visual trajectory into an action sequence,
while local-context FDM predicts the visual consequence of a supplied action
sequence. Neither receives language, past actions, or observations
preceding tt.

Importantly, conditioning scope and transition supervision are separate
design choices. The local-context restriction specifies which variables the dynamics component
may consume; it does not determine which transitions are used for learning.
Conversely, broader transition supervision can also be applied to a
full-context dynamics model. Sec. [4.3](#S4.SS3 "4.3 Component Composability ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models")
therefore compares full-context and local-context IDMs under matched
demonstration-only and mixed supervision.

Local-context conditioning restricts the variables available to the dynamics
component; it does not assume universal local sufficiency. Its adequacy
depends on whether the information needed for local action–outcome inference
is observable from the current observation, proprioceptive state, and supplied
transition. We evaluate this interface through local prediction and composed
control.

#### Broader local-transition supervision.

A task trajectory induces a local transition
z=(Ot0,qt,At+,Ot+)z=(O\_{t}^{0},q\_{t},A\_{t}^{+},O\_{t}^{+}).
Let 𝒟taskloc\mathcal{D}\_{\mathrm{task}}^{\mathrm{loc}} denote the distribution of
such transitions obtained from demonstrations. Demonstrations provide valid
transitions but contain only the action continuations selected by the
policy.

To broaden local supervision, we restore selected simulator states and
execute alternative future action sequences. For branch bb, this produces
z(b)=(Ot0,qt,At+,(b),Ot+,(b))z^{(b)}=(O\_{t}^{0},q\_{t},A\_{t}^{+,(b)},O\_{t}^{+,(b)}), where the initial condition is shared and each
future observation trajectory results from executing its corresponding
action sequence. These alternatives include interactions outside the
demonstrated continuation and need not complete the task. The simulator
state is used only to control data collection and is not provided to the
model.

The paired collection protocol controls the starting state, while the
learning objective operates on individual transition records rather than
using an explicit paired-branch loss. Let 𝒟cf\mathcal{D}\_{\mathrm{cf}} denote
the resulting counterfactual transitions. Dynamics models are trained from

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒟dyn=(1−η)​𝒟taskloc+η​𝒟cf,η∈[0,1].\mathcal{D}\_{\mathrm{dyn}}=(1-\eta)\mathcal{D}\_{\mathrm{task}}^{\mathrm{loc}}+\eta\mathcal{D}\_{\mathrm{cf}},\qquad\eta\in[0,1]. |  | (7) |

This supports demonstration-only, counterfactual-only, and mixed
supervision without changing the conditioning interface. The experimental
mixture and collection details are given in Sec. [4.1](#S4.SS1 "4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
The same interface can be applied to failed or exploratory physical-robot transitions when such data are collected.

#### Local dynamics learning.

Using the flow construction in Eq. [4](#S3.E4 "Equation 4 ‣ Shared flow-matching objective. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models"), local-context IDM denoises
the action target while conditioning on the observed future, whereas local-context
FDM denoises the future observation target while conditioning on the
executed action sequence:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | ℒLC​-​IDM\displaystyle\mathcal{L}\_{\mathrm{LC\text{-}IDM}} | =𝔼⁡[‖vθID​(ZA,τ∣O0,qt,O+,τ)−uA‖22],\displaystyle=\mathbb{E}\!\left[\left\|v\_{\theta\_{\mathrm{ID}}}(Z\_{\mathrm{A},\tau}\mid O^{0},q\_{t},O^{+},\tau)-u\_{\mathrm{A}}\right\|\_{2}^{2}\right], |  | (8) |
|  | ℒLC​-​FDM\displaystyle\mathcal{L}\_{\mathrm{LC\text{-}FDM}} | =𝔼⁡[‖vθFD​(ZO,τ∣O0,qt,A+,τ)−uO‖22].\displaystyle=\mathbb{E}\!\left[\left\|v\_{\theta\_{\mathrm{FD}}}(Z\_{\mathrm{O},\tau}\mid O^{0},q\_{t},A^{+},\tau)-u\_{\mathrm{O}}\right\|\_{2}^{2}\right]. |  |

Ground-truth future observations condition IDM training but are not video
denoising targets; analogously, executed actions condition FDM training.

#### Inference and component composition.

For video-to-action composition, the video predictor passes future
variational autoencoder (VAE) video latents to the receiving IDM;
transformer hidden states and caches are not transferred across components.
The receiving IDM processes the transferred latents through the same
modality-conditioning pathway used for recorded conditioning.

At inference, a task-conditioned visual predictor can be paired with an
independently trained local-context IDM:

|  |  |  |  |
| --- | --- | --- | --- |
|  | O^t+∼pϕCVP(⋅∣𝒞t),A^t+∼pθIDLC​-​IDM(⋅∣O^t+,Ot0,qt).\hat{O}\_{t}^{+}\sim p\_{\phi}^{\mathrm{CVP}}(\cdot\mid\mathcal{C}\_{t}),\quad\hat{A}\_{t}^{+}\sim p\_{\theta\_{\mathrm{ID}}}^{\mathrm{LC\text{-}IDM}}(\cdot\mid\hat{O}\_{t}^{+},O\_{t}^{0},q\_{t}). |  | (9) |

Task context determines the desired future through the visual predictor,
while the receiving IDM receives only the generated future trajectory and the
current local inputs.

The complementary composition pairs an action generator with local-context FDM:

|  |  |  |  |
| --- | --- | --- | --- |
|  | A^t+∼pψVLA(⋅∣𝒞t),O^t+∼pθFDLC​-​FDM(⋅∣A^t+,Ot0,qt).\hat{A}\_{t}^{+}\sim p\_{\psi}^{\mathrm{VLA}}(\cdot\mid\mathcal{C}\_{t}),\quad\hat{O}\_{t}^{+}\sim p\_{\theta\_{\mathrm{FD}}}^{\mathrm{LC\text{-}FDM}}(\cdot\mid\hat{A}\_{t}^{+},O\_{t}^{0},q\_{t}). |  | (10) |

The action sequence may equivalently be supplied by an external policy.
These are learned compositions: separately trained components need not
recover factors of one identical learned joint distribution. Their common
trajectory interfaces instead make the components explicitly replaceable,
and Sec. [4.3](#S4.SS3 "4.3 Component Composability ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models") evaluates when such replacement
succeeds.

## 4 Experiments

We evaluate OpenWAM along three dimensions: *native policy performance*,
*component composability*, and *local dynamics modeling*. We test
whether the shared robot-video foundation supports different video–action
interaction programs, whether independently trained action components remain
useful when paired with adapted visual predictors, and whether local-context forward
dynamics models action-dependent visual outcomes.

### 4.1 Experimental Setup

#### Robot-video pretraining and simulation.

We initialize the visual backbone from Wan2.2-5B [[75](#bib.bib19)] and further
pretrain it without action supervision on heterogeneous robot and
human-interaction video, including UMI/MV-UMI [[13](#bib.bib11), [64](#bib.bib57)],
AgiBot World [[9](#bib.bib52)], RoboMIND [[81](#bib.bib53)],
InternData-A1 [[73](#bib.bib54)], RoboCOIN [[84](#bib.bib55)],
FastUMI [[102](#bib.bib56)], Ego-Exo4D [[19](#bib.bib58)],
and Open X-Embodiment [[58](#bib.bib3)].
Unless otherwise stated, downstream OpenWAM variants use this
common initialization.

The four interaction programs share the same dual-stream
MoT backbone and downstream training recipe; they
differ in generation order and future cross-modal attention. Video is
processed in four-frame latent chunks, each predicting a 16-step action
chunk, with proprioception provided as a per-chunk conditioning signal.
Actions consist of end-effector position, axis-angle rotation, and a
gripper command. We use a two-stage training procedure: causal
robot-video pretraining followed by joint video–action training on the
target suite.

We evaluate Joint, VTA, ATV, and Decoupled on LIBERO-Object, LIBERO-Goal,
LIBERO-Spatial, and LIBERO-Long [[51](#bib.bib32)].
Component transfer uses LIBERO-Long as the downstream source
distribution and four LIBERO-90 targets (Table [1](#S3.T1 "Table 1 ‣ Interaction programs. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models")) chosen to represent qualitatively different forms of transfer. These targets are outside the LIBERO-Long
source-task set; robot-video pretraining is treated as a separate stage.

Table 2: Real-world bimanual manipulation tasks.

| Task | Objective | Main challenge |
| --- | --- | --- |
| Toast Bread | Insert bread and activate toaster | Deformability and precise insertion |
| Rubik’s Cube | Restore final layer of 2×22\times 2 cube | Contact-rich push and rotation |
| Sort Cups | Sort cups according to color | Variable ordering and sequencing |

#### Real-world tasks.

We evaluate on a bimanual platform comprising two Franka Research 3 arms
with parallel-jaw grippers and three RGB views: two wrist-mounted cameras
and one centered third-person camera. The three task definitions
are listed in Table [2](#S4.T2 "Table 2 ‣ Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models"). Figure [4](#S3.F4 "Figure 4 ‣ Interaction programs. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models") shows the
real-world tasks and the LIBERO-90 transfer targets.

#### Dynamics supervision.

Native task models are trained from task demonstrations. For local dynamics,
we additionally construct LIBERO-Long-CF by executing alternative
action continuations from states encountered in LIBERO-Long demonstrations.
Branches sharing an initial state remain in the same train, validation, or
test partition.
IDM and FDM experiments use demonstration-only, counterfactual-only
(CF-only), or mixed supervision. Mixed supervision samples 60% of
transitions from 𝒟cf\mathcal{D}\_{\mathrm{cf}} and 40% from
𝒟taskloc\mathcal{D}\_{\mathrm{task}}^{\mathrm{loc}}, corresponding to η=0.6\eta=0.6
in Eq. [7](#S3.E7 "Equation 7 ‣ Broader local-transition supervision. ‣ 3.4 Counterfactual Learning of Local-Context Dynamics Interfaces ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models").

#### Evaluation.

Closed-loop task success is the primary policy and composition metric.
For forward dynamics, we report visual prediction error and outcome
identification accuracy. Given KK realized futures from the same state,
the metric tests whether the prediction is closest in RGB MSE to its
matching outcome. We report both pairwise identification (K=2K=2) and
identification among all 16 action branches (K=16K=16).

Table 3: Closed-loop success (%) on four LIBERO suites.
Baselines are previously reported results.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Method | Object | Goal | Spatial | Long | Mean |
| OpenVLA [[38](#bib.bib5)] | 88.4 | 79.2 | 84.7 | 53.7 | 76.5 |
| OpenVLA-OFT [[36](#bib.bib6)] | 98.4 | 97.9 | 97.6 | 94.5 | 97.1 |
| π0\pi\_{0} [[6](#bib.bib7)] | 98.8 | 95.8 | 96.8 | 85.2 | 94.1 |
| π0.5\pi\_{0.5} [[33](#bib.bib8)] | 98.2 | 98.0 | 98.8 | 92.4 | 96.9 |
| GR00T-N1 [[5](#bib.bib59)] | 97.6 | 93.0 | 94.4 | 90.6 | 93.9 |
| Motus [[3](#bib.bib27)] | 99.8 | 96.6 | 96.8 | 97.6 | 97.7 |
| Fast-WAM [[94](#bib.bib22)] | 100.0 | 97.0 | 98.2 | 95.2 | 97.6 |
| LingBot-VA [[43](#bib.bib29)] | 99.6 | 97.2 | 98.5 | 98.5 | 98.5 |
| OpenWAM-VTA | 99.4±0.3\text{99.4}\_{\pm\text{0.3}} | 98.4±0.5\text{98.4}\_{\pm\text{0.5}} | 98.6±0.2\text{98.6}\_{\pm\text{0.2}} | 97.8±0.4\text{97.8}\_{\pm\text{0.4}} | 98.6 |
| OpenWAM-ATV | 98.0±0.4\text{98.0}\_{\pm\text{0.4}} | 97.2±0.2\text{97.2}\_{\pm\text{0.2}} | 96.6±0.6\text{96.6}\_{\pm\text{0.6}} | 95.4±0.3\text{95.4}\_{\pm\text{0.3}} | 96.8 |
| OpenWAM-Joint | 98.2±0.2\text{98.2}\_{\pm\text{0.2}} | 97.8±0.4\text{97.8}\_{\pm\text{0.4}} | 97.6±0.3\text{97.6}\_{\pm\text{0.3}} | 96.6±0.5\text{96.6}\_{\pm\text{0.5}} | 97.6 |
| OpenWAM-Decoupled | 99.0±0.3\text{99.0}\_{\pm\text{0.3}} | 98.0±0.2\text{98.0}\_{\pm\text{0.2}} | 97.8±0.5\text{97.8}\_{\pm\text{0.5}} | 97.0±0.4\text{97.0}\_{\pm\text{0.4}} | 98.0 |

Table 4:
Closed-loop success (%) on real-world bimanual manipulation tasks.

| Method | Toast | Cube | Cups | Mean |
| --- | --- | --- | --- | --- |
| OpenWAM-VTA | 92.0 | 90.0 | 94.4 | 92.1 |
| OpenWAM-Joint | 90.0 | 94.0 | 91.7 | 91.9 |

Table 5:
Frozen inverse dynamics transfer to four LIBERO-90 targets.
Target rows use task-tuned video predictors while source-trained IDMs
remain frozen. Mean is averaged over the four target tasks.

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Video / policy | Action component (frozen) | 64 Composition | 74 Retarget | 21 Object/grasp | 45 Scene shift | Transfer mean |
| Task-tuned VTA (finetuned policy reference) | | 94% | 86% | 92% | 100% | 93.0% |
| Task-tuned video | Full-context IDM, demo-only | 88% | 90% | 0% | 0% | 44.5% |
| Task-tuned video | Full-context IDM, mixed | 54% | 92% | 4% | 38% | 47.0% |
| Task-tuned video | Local-context IDM, demo-only | 36% | 50% | 0% | 0% | 21.5% |
| Task-tuned video | Local-context IDM, CF-only | 80% | 92% | 90% | 76% | 84.5% |
| Task-tuned video | Local-context IDM, mixed | 74% | 86% | 88% | 88% | 84.0% |
| Original VTA (unadapted policy reference) | | 42% | 0% | 0% | 0% | 10.5% |

Table 6:
Source-task composition on LIBERO-Long, all action components evaluated with LIBERO-Long video
predictor.

|  |  |  |
| --- | --- | --- |
| Action component | Supervision | Success (%) |
| Full-context IDM | Demo-only (Native VTA) | 97.8 |
| Full-context IDM | Mixed | 92.2 |
| Local-context IDM | Demo-only | 25.8 |
| Local-context IDM | CF-only | 90.6 |
| Local-context IDM | Mixed | 94.4 |

Table 7:
Local-context FDM prediction on counterfactual transitions.
MSE values are reported in units of 10−310^{-3}.
Outcome accuracy measures identification of the matching realized future
by RGB MSE among KK same-state outcomes.

| Supervision | RGB MSE ↓\downarrow | Acc. K=2K{=}2 ↑\uparrow | Acc. K=16K{=}16 ↑\uparrow |
| --- | --- | --- | --- |
| Demo-only | 14.35 | 68.3 | 21.1 |
| CF-only | 9.40 | 93.6 | 71.3 |
| Mixed | 9.62 | 91.8 | 67.7 |

### 4.2 Native Policy Performance

#### Broad LIBERO evaluation.

We compare the four interaction programs across the LIBERO suites and
report the average success rate over three random seeds in
Table [3](#S4.T3 "Table 3 ‣ Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
The principal OpenWAM configurations achieve strong performance across all
four suites, establishing that the shared foundation supports multiple
world–action generation orders.

#### Backbone initialization ablation.

Holding the VTA architecture, task supervision, and downstream training
procedure fixed, the original Wan2.2-5B initialization reaches 68.4%
success on LIBERO-Long, while our robot-video-pretrained causal backbone
reaches 97.8% (+29.4 points). This comparison measures the combined effect
of robot-video pretraining and causal adaptation, rather than attributing the
gain to either factor individually.

#### Real-world native policies.

Table [4](#S4.T4 "Table 4 ‣ Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models") reports closed-loop success for VTA and
Joint on the three bimanual tasks of Table [2](#S4.T2 "Table 2 ‣ Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models"), which
test the same framework under multi-view, deformable, contact-rich,
and multi-object manipulation.

### 4.3 Component Composability

We next study whether action-grounding components remain useful when the visual predictor changes. Full-context and local-context IDMs are evaluated under transition-supervision regimes, separating the effects of broader local-transition data from the restriction of task-level context.

#### Frozen action-component reuse.

For each LIBERO-90 target, the visual producer is taken from a task-tuned
VTA model while source-trained action components remain frozen. Thus, the
experiment measures reuse of an action component after visual-task
adaptation, rather than target-task learning without action supervision.
All reused executors are evaluated with the same target predictor and
rollout protocol. Table [6](#S4.T6 "Table 6 ‣ Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models") reports source-task
composition on LIBERO-Long.

Conditioning scope and supervision interact strongly
(Tables [6](#S4.T6 "Table 6 ‣ Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models") and [5](#S4.T5 "Table 5 ‣ Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models")).
Mixed supervision raises mean target success from 21.5% to 84.0%
for local-context IDMs, compared with 44.5% to 47.0% for
full-context IDMs. Under matched mixed supervision, local conditioning
improves target success by 37.0 percentage points while retaining
94.4% source-task success.
Counterfactual-only and mixed supervision both substantially improve
local-context IDM transfer, achieving comparable mean success of 84.5%
and 84.0%, respectively, across the four LIBERO-90 targets. These
results show that broader transition coverage supports the reuse of
local-context dynamics components after visual task adaptation.

The per-task results also reveal uneven transfer. The demonstration-only
full-context IDM performs well on Tasks 64 and 74 but obtains 0%
success on Tasks 21 and 45, whereas CF-only and mixed local-context
IDMs remain effective across all four targets. This contrast highlights
their more consistent reuse across the evaluated task changes.

### 4.4 Action-Conditioned Forward Dynamics

We evaluate local-context FDMs on 2,560 counterfactual futures from
160 contexts across ten LIBERO tasks, with 16 action branches per context.
Models share the same initial observations, actions, and realized futures.
In addition to RGB prediction error, we measure whether the predicted future
preserves the identity of its conditioning action through outcome
identification at K=2K=2 and K=16K=16.

As shown in Table [7](#S4.T7 "Table 7 ‣ Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models"), CF-only and mixed supervision reduce RGB MSE
by 34.5% and 33.0%, respectively, relative to demonstration-only training.
CF-only supervision raises outcome accuracy from 68.3% to 93.6% for
K=2K=2, and from 21.1% to 71.3% for K=16K=16. Mixed supervision shows a
similar improvement, reaching 91.8% and 67.7%, respectively. These results
show that broader transition supervision improves both visual prediction
accuracy and the ability to distinguish action-dependent futures.

## 5 Discussion and Conclusion

We presented OpenWAM, an open framework and pretrained foundation spanning
video prediction, robot control, and local dynamics modeling. Its shared
causal backbone supports joint, sequential, and decoupled video–action
generation within a common training and evaluation stack. Strong performance
across four LIBERO suites and real-world bimanual tasks demonstrates the
framework’s control capabilities, while the initialization ablation
establishes the substantial benefit of robot-video pretraining. OpenWAM thus supports multiple effective modeling configurations rather than a
single specialized policy.

Beyond native control, the framework supports independently trained
inverse and forward dynamics components. In the transfer study,
counterfactual-only and mixed supervision both substantially improve the
reuse of local-context IDMs after visual task adaptation, while retaining
strong source-task performance. Counterfactual FDM supervision also improves both visual prediction accuracy and
identification of action-dependent outcomes.

Several questions remain open. Composability is established primarily in
simulation; demonstrating comparable reuse on real robots will require more
data-efficient physical dynamics supervision. Our target-task experiments
adapt the video predictor and therefore do not establish zero-shot transfer of
the complete video–action model. Appendix E shows that policy, IDM, and FDM
objectives can be trained jointly in one checkpoint, but we have not yet shown
that a single multi-objective model can match the strongest specialized
OpenWAM variants across all modes. The present FDM study also focuses on local,
short-horizon prediction, leaving long-horizon planning and physical deployment
as natural extensions.

OpenWAM brings these capabilities into one open foundation: strong
policies, configurable prediction–action interaction, and independently
reusable dynamics. It provides both capable world–action models and a
common basis for building, comparing, and composing the next generation.

## References

* [1]
  N. Agarwal, A. Ali, J. Allen, M. Antolini, A. Aubame, A. Azzolini, J. Bai, M. Bala, Y. Balaji, J. Bapst, et al. (2026)
  Cosmos 3: omnimodal world models for physical ai.
  arXiv preprint arXiv:2606.02800.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [2]
  E. Ameperosa, J. A. Collins, M. Jain, and A. Garg (2025)
  Rocoda: counterfactual data augmentation for data-efficient robot learning from demonstrations.
  In 2025 IEEE International Conference on Robotics and Automation (ICRA),
  pp. 13250–13256.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [3]
  H. Bi, H. Tan, S. Xie, Z. Wang, S. Huang, H. Liu, R. Zhao, Y. Feng, C. Xiang, Y. Rong, et al. (2026)
  Motus: a unified latent action world model.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
  pp. 35101–35113.
  Cited by: [Table 3](#S4.T3.5.7.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [4]
  H. Bi, Z. Zhou, Y. Tang, J. Pang, S. Huang, H. Liu, R. Wang, S. Huang, Y. Wang, Y. Cheng, et al. (2026)
  Motus2: a self-evolving general world model for dexterous manipulation.
  arXiv preprint arXiv:2608.30237.
  Cited by: [§2.2](#S2.SS2.p3.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [5]
  J. Bjorck, F. Castañeda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. (2025)
  Gr00t n1: an open foundation model for generalist humanoid robots.
  arXiv preprint arXiv:2503.14734.
  Cited by: [Table 3](#S4.T3.5.6.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [6]
  K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. (2024)
  π0\pi\_{0}: a vision-language-action flow model for general robot control.
  arXiv preprint arXiv:2410.24164.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [Table 3](#S4.T3.5.4.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [7]
  A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, et al. (2023)
  Rt-2: vision-language-action models transfer web knowledge to robotic control.
  arXiv preprint arXiv:2307.15818.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [8]
  A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. (2022)
  Rt-1: robotics transformer for real-world control at scale.
  arXiv preprint arXiv:2212.06817.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [9]
  Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang, et al. (2025)
  Agibot world colosseo: a large-scale manipulation platform for scalable and intelligent embodied systems.
  arXiv preprint arXiv:2503.06669.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [10]
  J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang, et al. (2025)
  Worldvla: towards autoregressive action world model.
  arXiv preprint arXiv:2506.21539.
  Cited by: [§2.2](#S2.SS2.p3.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [11]
  C. Cheang, G. Chen, Y. Jing, T. Kong, H. Li, Y. Li, Y. Liu, H. Wu, J. Xu, Y. Yang, et al. (2024)
  Gr-2: a generative video-language-action model with web-scale knowledge for robot manipulation.
  arXiv preprint arXiv:2410.06158.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [12]
  C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song (2025)
  Diffusion policy: visuomotor policy learning via action diffusion.
  The International Journal of Robotics Research 44 (10-11), pp. 1684–1704.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [13]
  C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song (2024)
  Universal manipulation interface: in-the-wild robot teaching without in-the-wild robots.
  arXiv preprint arXiv:2402.10329.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [14]
  Y. Du, S. Yang, B. Dai, H. Dai, O. Nachum, J. Tenenbaum, D. Schuurmans, and P. Abbeel (2023)
  Learning universal policies via text-guided video generation.
  Advances in neural information processing systems 36, pp. 9156–9172.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [15]
  J. Duan, W. Pumacay, N. Kumar, Y. R. Wang, S. Tian, W. Yuan, R. Krishna, D. Fox, A. Mandlekar, and Y. Guo (2024)
  Aha: a vision-language-model for detecting and reasoning over failures in robotic manipulation.
  arXiv preprint arXiv:2410.00371.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [16]
  F. Ebert, C. Finn, S. Dasari, A. Xie, A. Lee, and S. Levine (2018)
  Visual foresight: model-based deep reinforcement learning for vision-based robotic control.
  arXiv preprint arXiv:1812.00568.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [17]
  C. Finn and S. Levine (2017)
  Deep visual foresight for planning robot motion.
  In 2017 IEEE international conference on robotics and automation (ICRA),
  pp. 2786–2793.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [18]
  J. A. L. Gonzalez, P. Pacaud, and C. Schmid (2026)
  Spatially aware world action model via geometric latent diffusion.
  arXiv preprint arXiv:2609.02531.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [19]
  K. Grauman, A. Westbury, L. Torresani, K. Kitani, J. Malik, T. Afouras, K. Ashutosh, V. Baiyya, S. Bansal, B. Boote, et al. (2024)
  Ego-exo4d: understanding skilled human activity from first-and third-person perspectives.
  In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
  pp. 19383–19400.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [20]
  J. Guo, Q. Li, P. Li, Z. Chen, N. Sun, Y. Su, H. Wang, Y. Zhang, X. Li, and H. Liu (2026)
  Unified 4d world action modeling from video priors with asynchronous denoising.
  arXiv preprint arXiv:2604.26694.
  Cited by: [§2.2](#S2.SS2.p3.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [21]
  Y. Guo, Y. Hu, J. Zhang, Y. Wang, X. Chen, C. Lu, and J. Chen (2024)
  Prediction with action: visual policy learning via joint denoising process.
  Advances in Neural Information Processing Systems 37, pp. 112386–112410.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [22]
  Y. Guo, L. Shi, J. Chen, and C. Finn (2026)
  Ctrl-world: a controllable generative world model for robot manipulation.
  In International Conference on Learning Representations,
  Vol. 2026, pp. 6121–6138.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [23]
  H. Ha, Y. Gao, Z. Fu, J. Tan, and S. Song (2024)
  UMI on legs: making manipulation policies mobile with manipulation-centric whole-body controllers.
  In Proceedings of the 2024 Conference on Robot Learning,
  Cited by: [§B.1](#A2.SS1.p1.1 "B.1 Pretraining Corpus ‣ Appendix B Robot-Video Pretraining ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [24]
  D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi (2019)
  Dream to control: learning behaviors by latent imagination.
  arXiv preprint arXiv:1912.01603.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [25]
  D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap (2023)
  Mastering diverse domains through world models.
  arXiv preprint arXiv:2301.04104.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [26]
  Y. Hu, Y. Guo, P. Wang, X. Chen, Y. Wang, J. Zhang, K. Sreenath, C. Lu, and J. Chen (2024)
  Video prediction policy: a generalist robot policy with predictive visual representations.
  arXiv preprint arXiv:2412.14803.
  Cited by: [§2.2](#S2.SS2.p2.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [27]
  Z. Hu, R. Wu, N. Enock, J. Li, R. Kadakia, Z. Erickson, and A. Kumar (2026)
  Rac: robot learning for long-horizon tasks by scaling recovery and correction.
  IEEE Transactions on Robotics.
  Cited by: [§2.3](#S2.SS3.p1.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [28]
  W. Huang, H. Sun, Y. Guo, Y. Ma, H. Li, J. Long, Z. Mo, Z. Guan, Y. Guo, S. Di, et al. (2026)
  NoiseGate: learning per-latent timestep schedules as information gating in world action models.
  arXiv preprint arXiv:2605.07794.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [29]
  X. Huang, Y. Wang, Z. Ye, B. Zhao, C. Yu, H. Wen, and Z. Deng (2026)
  Streaming-wam: action-conditioned world-action model for asynchronous robot manipulation.
  arXiv preprint arXiv:2609.28927.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [30]
  Y. Huang, N. Alvina, M. D. Shanthi, and T. Hermans (2025)
  Fail2progress: learning from real-world robot failures with stein variational inference.
  arXiv preprint arXiv:2509.01746.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [31]
  Z. Huang, J. Zhang, H. Liu, C. Zhang, R. Cheng, and L. Zhang (2026)
  Learning transferable dynamics priors from action to world modeling.
  arXiv preprint arXiv:2606.29501.
  Cited by: [§2.1](#S2.SS1.p3.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [32]
  P. Intelligence, A. Amin, R. Aniceto, A. Balakrishna, K. Black, K. Conley, G. Connors, J. Darpinian, K. Dhabalia, J. DiCarlo, et al. (2025)
  π0.6∗\pi^{\*}\_{0.6}: a vla that learns from experience.
  arXiv preprint arXiv:2511.14759.
  Cited by: [§2.3](#S2.SS3.p1.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [33]
  P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, et al. (2025)
  π0.5\pi\_{0.5}: a vision-language-action model with open-world generalization.
  arXiv preprint arXiv:2504.16054.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [Table 3](#S4.T3.5.5.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [34]
  J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y. Lin, et al. (2025)
  Dreamgen: unlocking generalization in robot learning through video world models.
  arXiv preprint arXiv:2505.12705.
  Cited by: [§2.2](#S2.SS2.p2.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [35]
  H. Jiang, L. Liu, X. Wang, Z. Sun, Z. Chen, S. Wang, X. Wang, X. Chen, J. Yao, W. Zhao, et al. (2026)
  Rethinking representations for world-action modeling.
  arXiv preprint arXiv:2609.38163.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [36]
  M. J. Kim, C. Finn, and P. Liang (2025)
  Fine-tuning vision-language-action models: optimizing speed and success.
  arXiv preprint arXiv:2502.19645.
  Cited by: [Table 3](#S4.T3.5.3.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [37]
  M. J. Kim, Y. Gao, T. Lin, Y. Lin, Y. Ge, G. Lam, P. Liang, S. Song, M. Liu, C. Finn, et al. (2026)
  Cosmos policy: fine-tuning video models for visuomotor control and planning.
  arXiv preprint arXiv:2601.16163.
  Cited by: [§2.2](#S2.SS2.p3.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [38]
  M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. (2024)
  Openvla: an open-source vision-language-action model.
  arXiv preprint arXiv:2406.09246.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [Table 3](#S4.T3.5.2.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [39]
  P. Ko, J. Mao, Y. Du, S. Sun, and J. B. Tenenbaum (2024)
  Learning to act from actionless videos through dense correspondences.
  In International Conference on Learning Representations,
  Vol. 2024, pp. 40938–40958.
  Cited by: [§2.2](#S2.SS2.p2.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [40]
  M. Laskey, J. Lee, R. Fox, A. Dragan, and K. Goldberg (2017)
  Dart: noise injection for robust imitation learning.
  In Conference on robot learning,
  pp. 143–156.
  Cited by: [§2.3](#S2.SS3.p1.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [41]
  B. Li, X. Yin, M. Lin, Y. Zhang, and D. Xu (2026)
  EgoWAM: world action models beyond pixels with in-the-wild egocentric human data.
  In Robot World Models,
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [42]
  D. Li, J. Lei, H. Wang, L. Liu, Y. Yang, Z. Wang, B. Liu, M. Zheng, and Z. Fan (2026)
  Learning actionable manipulation recovery via counterfactual failure synthesis.
  arXiv preprint arXiv:2603.13528.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [43]
  L. Li, Q. Zhang, Y. Luo, S. Yang, R. Wang, F. Han, M. Yu, Z. Gao, N. Xue, X. Zhu, et al. (2026)
  Causal world modeling for robot control.
  arXiv preprint arXiv:2601.21998.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [Table 3](#S4.T3.5.9.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [44]
  S. Li, V. Yao, C. Yang, T. Qu, R. Cheng, R. Yu, H. Lu, N. Von, V. Chen, Y. Tang, et al. (2026)
  WALL-wm: carving world action modeling at the event joints.
  arXiv preprint arXiv:2606.01955.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [45]
  S. Li, Y. Gao, D. Sadigh, and S. Song
  Unified video action model, 2025.
  arXiv preprint arXiv:2503.00200.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E External Dynamics Comparison ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§2.2](#S2.SS2.p3.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [46]
  S. L. Li, E. Kim, X. Bai, T. Zhao, T. Pang, M. Simchowitz, and V. Sitzmann (2026)
  Turning video models into generalist robot policies.
  External Links: 2605.27817,
  [Link](https://arxiv.org/abs/2605.27817)
  Cited by: [§2.2](#S2.SS2.p2.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [47]
  Y. Li, Y. Zhu, J. Wen, C. Shen, and Y. Xu (2025)
  Worldeval: world model as real-world robot policies evaluator.
  arXiv preprint arXiv:2505.19017.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [48]
  Z. Li, D. Cheng, Y. Wang, S. Wang, X. Xu, L. Weng, J. Wang, and J. Wang (2026)
  Light-wam: efficient world action models with state-fusion action decoding.
  arXiv preprint arXiv:2606.08242.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [49]
  W. Liang, L. Yu, L. Luo, S. Iyer, N. Dong, C. Zhou, G. Ghosh, M. Lewis, W. Yih, L. Zettlemoyer, et al. (2024)
  Mixture-of-transformers: a sparse and scalable architecture for multi-modal foundation models.
  arXiv preprint arXiv:2411.04996.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§3.3](#S3.SS3.SSS0.Px1.p1.1 "Shared architecture. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [50]
  Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le (2022)
  Flow matching for generative modeling.
  arXiv preprint arXiv:2210.02747.
  Cited by: [§3.3](#S3.SS3.SSS0.Px3.p1.1 "Shared flow-matching objective. ‣ 3.3 Configurable Video–Action Interaction Programs ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [51]
  B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone (2023)
  Libero: benchmarking knowledge transfer for lifelong robot learning.
  Advances in Neural Information Processing Systems 36, pp. 44776–44791.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p3.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [52]
  R. Liu, W. Zhao, Z. Yang, L. Chen, P. Zhou, S. Chen, G. Ren, Y. Peng, R. Jin, N. Wang, et al. (2026)
  GE-act 2.0: pretraining and scaling a world-action model for robotic manipulation.
  arXiv preprint arXiv:2609.05588.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [53]
  Y. Liu, P. Sun, S. Li, Y. Xie, L. Zhang, X. Chao, S. Dong, F. Chen, X. Zhang, and W. Ding (2026)
  Oa-wam: object-addressable world action model for robust robot manipulation.
  arXiv preprint arXiv:2605.06481.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [54]
  Z. Lu, H. Zhai, G. Wang, H. Zeng, J. Yang, J. Liu, L. Cheng, Y. Zhang, Y. Qiu, Z. Cheng, et al. (2026)
  World-action models for robot learning and control: a survey.
  arXiv preprint arXiv:2609.16074.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [55]
  T. Ma, J. Zheng, Z. Wang, C. Jiang, A. Cui, J. Liang, and S. Yang (2026)
  Dit4dit: jointly modeling video dynamics and actions for generalizable robot control.
  arXiv preprint arXiv:2603.10448.
  Cited by: [§2.2](#S2.SS2.p2.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [56]
  Z. Ma, X. Wei, J. Jiang, S. Lu, and L. Zhang (2026)
  TacPAC: tactile prediction and real-time action correction in world-action models for contact-rich manipulation.
  arXiv preprint arXiv:2609.05266.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [57]
  A. Mandlekar, D. Xu, R. Martín-Martín, Y. Zhu, L. Fei-Fei, and S. Savarese (2020)
  Human-in-the-loop imitation learning using remote teleoperation.
  arXiv preprint arXiv:2012.06733.
  Cited by: [§2.3](#S2.SS3.p1.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [58]
  A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, et al. (2024)
  Open x-embodiment: robotic learning datasets and rt-x models: open x-embodiment collaboration 0.
  In 2024 IEEE International Conference on Robotics and Automation (ICRA),
  pp. 6892–6903.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [59]
  B. Pan, F. Liu, H. Lu, J. Wang, and Y. Shi (2026)
  SelfWAM: a self-grounded unified world action model for fast robot control.
  arXiv preprint arXiv:2608.00725.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [60]
  Q. Peng, Y. Liang, R. Yan, N. Hansen, and X. Wang (2026)
  FACT: failure-aware causal training for world-action models.
  arXiv preprint arXiv:2608.10232.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [61]
  H. Qi, H. Yin, A. Zhu, Y. Du, and H. Yang (2026)
  Inference-time enhancement of generative robot policies via predictive world modeling.
  IEEE Robotics and Automation Letters.
  Cited by: [§2.1](#S2.SS1.p3.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [62]
  C. Qiu, R. Wang, R. Zhao, S. Lin, S. Gu, S. Nan, G. Liu, K. Jia, Y. Fu, and S. Wu (2026)
  Vid2WAM: distilling video diffusion priors into world action models.
  arXiv preprint arXiv:2608.08558.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [63]
  L. Qiu, Y. Li, Y. Chen, Y. Ge, Y. Ge, and X. Liu (2026)
  Making foresight actionable: repurposing representation alignment in world action models.
  arXiv preprint arXiv:2606.12217.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [64]
  O. Rayyan, J. Abanes, M. Hafez, A. Tzes, and F. Abu-Dakka (2026)
  Mv-umi: a scalable multi-view interface for cross-embodiment learning.
  IEEE Access.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [65]
  S. Ross, G. Gordon, and D. Bagnell (2011)
  A reduction of imitation learning and structured prediction to no-regret online learning.
  In Proceedings of the fourteenth international conference on artificial intelligence and statistics,
  pp. 627–635.
  Cited by: [§2.3](#S2.SS3.p1.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [66]
  Y. Shen, F. Wei, Z. Du, Y. Liang, Y. Lu, J. Yang, N. Zheng, and B. Guo (2026)
  Videovla: video generators can be generalizable robot manipulators.
  Advances in neural information processing systems 38, pp. 95597–95621.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [67]
  Z. Shen, J. Liang, J. Lu, F. Jiang, Y. Wang, C. Wei, J. Liu, J. Yang, Q. Yu, J. You, et al. (2026)
  LD4WAM: learning latent dynamics from human videos for world action models.
  arXiv preprint arXiv:2608.22403.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [68]
  H. Sun, J. Pei, F. Kang, Z. Liu, Y. Li, B. Jiang, H. Xue, C. Zhou, W. Li, Y. Wei, et al. (2026)
  Riemann-1.0: an embodied world action model for physical ai.
  arXiv preprint arXiv:2608.27033.
  Cited by: [§2.2](#S2.SS2.p3.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [69]
  Q. Tang, B. Zhuang, B. Yuan, X. Yu, L. Guo, and J. Feng (2026)
  World tokens: enhancing embodied policies with training-time world modeling.
  arXiv preprint arXiv:2608.09730.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [70]
  O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. (2024)
  Octo: an open-source generalist robot policy.
  arXiv preprint arXiv:2405.12213.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [71]
  R. A. Team (2026)
  Causal video models are data-efficient robot policy learners.
  Rhoda AI Blog.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [72]
  Y. Tian, S. Yang, J. Zeng, P. Wang, D. Lin, H. Dong, and J. Pang (2025)
  Predictive inverse dynamics models are scalable learners for robotic manipulation.
  In International Conference on Learning Representations,
  Vol. 2025, pp. 92033–92052.
  Cited by: [§2.2](#S2.SS2.p2.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [73]
  Y. Tian, Y. Yang, Y. Xie, Z. Cai, X. Shi, N. Gao, H. Liu, X. Jiang, Z. Qiu, F. Yuan, et al. (2026)
  Interndata-a1: pioneering high-fidelity synthetic data for pre-training generalist policy.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
  pp. 976–985.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [74]
  A. D. Vuong, T. Van Vo, A. Sohail, H. Ding, L. Ma, X. Liang, A. Duan, I. Laptev, and I. Reid (2026)
  World2Act: latent action post-training from world model dynamics.
  arXiv preprint arXiv:2603.10422.
  Cited by: [§2.2](#S2.SS2.p2.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [75]
  T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C. Xie, D. Chen, F. Yu, H. Zhao, J. Yang, et al. (2025)
  Wan: open and advanced large-scale video generative models.
  arXiv preprint arXiv:2503.20314.
  Cited by: [Figure 1](#S1.F1 "In 1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [Figure 1](#S1.F1.9 "In 1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§3.2](#S3.SS2.p1.1 "3.2 An Open Causal Robot-Video Backbone ‣ 3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [76]
  J. Wang, Q. Zhang, S. Yang, Y. Luo, Y. Shen, Z. Wu, Y. Jiang, and Y. Xu (2026)
  RepWAM: world action modeling with representation visual-action tokenizers.
  arXiv preprint arXiv:2606.13674.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [77]
  L. Wang, Z. An, M. Zhang, C. Dai, Y. Xu, C. Cui, Z. Yang, Y. Chen, L. Zhou, and C. Lu (2026)
  GlanceWAM: sparse test-time imagination for world-action models.
  arXiv preprint arXiv:2608.23927.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [78]
  S. Wang, J. Shi, Z. Fu, X. He, F. Liu, C. Yang, Y. Zhou, Z. Fei, J. Gong, J. Fu, et al. (2026)
  World action models: the next frontier in embodied ai.
  arXiv preprint arXiv:2605.12090.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [79]
  Y. Wang, S. Huang, M. Li, C. Zhang, J. Liang, W. Jin, Y. Chen, X. Chi, D. Zhou, Q. Yu, et al. (2026)
  Openwam: an open, modular exploration towards systematic world-action model pretraining.
  arXiv preprint arXiv:2609.07398.
  Cited by: [§2.2](#S2.SS2.p5.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [80]
  H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong (2024)
  Unleashing large-scale video generative pre-training for visual robot manipulation.
  In International Conference on Learning Representations,
  Vol. 2024, pp. 10641–10662.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [81]
  K. Wu, C. Hou, J. Liu, Z. Che, X. Ju, Z. Yang, M. Li, Y. Zhao, Z. Xu, G. Yang, et al. (2024)
  Robomind: benchmark on multi-embodiment intelligence normative data for robot manipulation.
  arXiv preprint arXiv:2412.13877.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [82]
  P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg (2023)
  Daydreamer: world models for physical robot learning.
  In Conference on robot learning,
  pp. 2226–2240.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [83]
  P. Wu, Y. Shentu, Z. Yi, X. Lin, and P. Abbeel (2024)
  Gello: a general, low-cost, and intuitive teleoperation framework for robot manipulators.
  In 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS),
  pp. 12156–12163.
  Cited by: [Figure 5](#A1.F5 "In A.5 Real Robot Setup ‣ Appendix A Implementation Details ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [Figure 5](#A1.F5.4 "In A.5 Real Robot Setup ‣ Appendix A Implementation Details ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [84]
  S. Wu, X. Liu, S. Xie, P. Wang, X. Li, B. Yang, Z. Li, K. Zhu, H. Wu, Y. Liu, et al. (2025)
  Robocoin: an open-sourced bimanual robotic data collection for integrated manipulation.
  arXiv preprint arXiv:2511.17441.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [85]
  X. Wu, Y. Yang, S. Zhou, H. Sun, J. Liu, S. Yu, J. Zhang, W. Li, B. Wang, G. Ma, et al. (2026)
  ZimaBlue: evolving generalizable world action models through scalable video pre-training.
  arXiv preprint arXiv:2609.00188.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [86]
  M. Xu, H. Zhang, Y. Hou, Z. Xu, L. Fan, M. Veloso, and S. Song (2025)
  DexUMI: using human hand as the universal manipulation interface for dexterous manipulation.
  In Conference on Robot Learning,
  pp. 437–459.
  Cited by: [§B.1](#A2.SS1.p1.1 "B.1 Pretraining Corpus ‣ Appendix B Robot-Video Pretraining ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [87]
  L. Yang, Y. Bai, G. Eskandar, F. Shen, M. Altillawi, D. Chen, Z. Liu, and A. Valada (2026)
  Covar: co-generation of video and action for robotic manipulation via multi-modal diffusion.
  In 2026 IEEE International Conference on Robotics and Automation (ICRA),
  pp. 17785–17792.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [88]
  L. Yang, Z. Jiang, C. Sheng, and Z. Tang (2026)
  WAM-opd: on-policy distillation for world action models.
  arXiv preprint arXiv:2608.22364.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [89]
  A. Ye, B. Wang, C. Ni, G. Huang, G. Zhao, H. Li, H. Li, J. Li, J. Lv, J. Liu, et al.
  Gigaworld-policy: an efficient action-centered world–action model, 2026.
  URL https://arxiv. org/abs/2603.17240.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [90]
  S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang, et al. (2026)
  World action models are zero-shot policies.
  arXiv preprint arXiv:2602.15922.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [91]
  T. Yin, Z. Mei, Z. Zheng, M. Yamane, D. Wang, J. Sceats, S. M. Bateman, L. Zha, A. Badithela, O. Shorinwa, et al. (2026)
  Playworld: learning robot world models from autonomous play.
  arXiv preprint arXiv:2603.09030.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [92]
  J. You, Q. Yu, Y. Chen, M. Cai, Z. Zhong, Y. Wang, B. Ping, J. Liang, Z. Shen, H. Yan, et al. (2026)
  AffordanceWAM: affordance-aware joint world-action modeling for robot manipulation.
  arXiv preprint arXiv:2609.22332.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [93]
  Y. Yu (2026)
  On the capability separation between world-model policy learning and imitated world-action models.
  arXiv preprint arXiv:2608.22197.
  Cited by: [§2.3](#S2.SS3.p1.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [94]
  T. Yuan, Z. Dong, Y. Liu, and H. Zhao (2026)
  Fast-wam: do world action models need test-time future imagination?.
  arXiv preprint arXiv:2603.16666.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models"),
  [Table 3](#S4.T3.5.8.1.1 "In Evaluation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [95]
  C. Zhang, S. Ito, K. Hoshino, S. Ikehata, and I. Sato (2026)
  World-coherent decoding: self-verifying test-time planning for world action models.
  arXiv preprint arXiv:2609.02159.
  Cited by: [§2.1](#S2.SS1.p3.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [96]
  M. Zhang, S. Khose, S. Kareer, Y. Song, U. Jain, and J. Hoffman (2026)
  DeVA: decoupled video-action model with physical guidance for robot policy learning.
  arXiv preprint arXiv:2607.24159.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [97]
  Q. Zhang, L. Li, L. Zhang, S. Yang, Y. Luo, S. Li, R. Wang, J. Wang, J. Shao, G. Xu, et al. (2026)
  Native video-action pretraining for generalizable robot control.
  arXiv preprint arXiv:2607.08639.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [98]
  G. Zhao, Z. Tang, X. Chen, Z. Kuang, Y. Tian, and G. Li (2026)
  FLARE: a failure-aware framework for autonomous correction and recovery in visual-language robotic manipulation.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
  pp. 22391–22401.
  Cited by: [§2.3](#S2.SS3.p2.1 "2.3 Dynamics Learning Beyond Successful Demonstrations ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [99]
  R. Zhao, Z. Zhang, Y. Su, W. Wang, J. Li, Z. Yang, F. E. Tay, M. H. Ang Jr, and H. Zhu (2026)
  SG-wam: self-guided world modeling in geometry-aware policy space.
  arXiv preprint arXiv:2608.01397.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [100]
  S. Zhao, H. Xie, W. Zhao, C. Zhang, H. Wang, C. Wang, Q. Liu, and S. Zhang (2026)
  Memory as plans: world-action modeling with memory-grounded planning.
  arXiv preprint arXiv:2609.11561.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [101]
  T. Z. Zhao, V. Kumar, S. Levine, and C. Finn (2023)
  Learning fine-grained bimanual manipulation with low-cost hardware.
  arXiv preprint arXiv:2304.13705.
  Cited by: [§2.1](#S2.SS1.p1.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [102]
  Z. Zhaxizhuoma, K. Liu, C. Guan, Z. Jia, Z. Wu, X. Liu, T. Wang, S. Liang, P. Chen, P. Zhang, et al. (2025)
  Fastumi: a scalable and hardware-independent universal manipulation interface with dataset.
  In Conference on Robot Learning,
  pp. 3069–3093.
  Cited by: [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Robot-video pretraining and simulation. ‣ 4.1 Experimental Setup ‣ 4 Experiments ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [103]
  J. Zheng, T. Ma, Y. Fan, Z. Wang, S. Yang, and J. Liang (2026)
  MotionWAM: towards foundation world action models for real-time humanoid loco-manipulation.
  arXiv preprint arXiv:2606.09215.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [104]
  Y. Zheng, X. Li, S. Gu, Y. Zheng, S. Tian, W. Li, L. Wang, C. Li, Q. Zhang, H. Li, et al. (2026)
  GIFT: guided intermediate feature training via action-oriented structural supervision for robotic manipulation.
  arXiv preprint arXiv:2609.04193.
  Cited by: [§2.2](#S2.SS2.p4.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [105]
  J. Zhou, Q. Zhang, G. Xu, C. Fan, Y. Zhao, R. Wang, Y. Luo, S. Yang, X. Zhu, Y. Shen, et al. (2026)
  Zero-wam: in-context world-action modeling from human videos for open-ended task generalization.
  arXiv preprint arXiv:2608.26103.
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [106]
  P. Zhou, S. Chen, D. Chen, J. Wang, R. Jin, B. Zhu, Y. Pan, S. Gu, K. Wang, S. Nan, et al. (2026)
  τ0\tau\_{0}-WM: a unified video-action world model for robotic manipulation.
  arXiv preprint arXiv:2606.01027.
  Cited by: [§2.1](#S2.SS1.p3.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [107]
  S. Zhou, Y. Du, J. Chen, Y. Li, D. Yeung, and C. Gan (2024)
  Robodreamer: learning compositional world models for robot imagination.
  arXiv preprint arXiv:2404.12377.
  Cited by: [§2.1](#S2.SS1.p2.1 "2.1 Visuomotor Policies and Predictive Control ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").
* [108]
  C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta (2025)
  Unified world models: coupling video and action diffusion for pretraining on large robotic datasets.
  arXiv preprint arXiv:2504.02792.
  Cited by: [§2.2](#S2.SS2.p3.1 "2.2 Video Foundations and World–Action Architectures ‣ 2 Related Work ‣ OpenWAM: An Open Framework for Composable World-Action Models").

Appendix

## Appendix A Implementation Details

This section provides implementation and evaluation details for the four video–action interaction programs studied in the main paper, including model architecture, downstream training, generation, and closed-loop evaluation.

### A.1 Model Architecture and Representation

#### Dual-stream backbone.

We use a 30-layer dual-stream Mixture-of-Transformers (MoT) architecture with modality-specific video and action experts.
The video expert has a hidden dimension of 3072, 24 attention heads with a head dimension of 128, and an FFN dimension of 14336. The action expert has a hidden dimension of 2048 and an FFN dimension of 8192, while retaining the same attention configuration of 24 heads with a head dimension of 128. Consequently, its query, key, and value projections each map the 2048-dimensional hidden state to 3072 dimensions, and the attention output is projected back to 2048 dimensions.
Cross-modal information exchange is controlled by the future cross-modal attention pattern associated with each interaction program.
Task text conditions both streams through a separate cross-attention layer.

#### Visual observations.

Each observation contains an agent-view image and a wrist-camera
image, both at 128×128128\times 128 resolution.
The two views are encoded independently into 8×8×488\times 8\times 48 VAE latents and concatenated along the spatial width dimension to form an 8×16×488\times 16\times 48 latent canvas.
Using a 1×2×21\times 2\times 2 temporal-spatial patch size, each latent frame contains 32 video tokens.
The video VAE temporally compresses every four environment steps into one latent video frame. Each generation chunk spans four future latent frames, corresponding to 16 environment steps.

#### Actions and proprioception.

The policy predicts a 16-step action chunk aligned with the same temporal horizon, with four action steps corresponding to each latent video frame. Each action has seven dimensions: three for end-effector position, three for axis-angle rotation, and one for the gripper command. Each chunk is conditioned on an eight-dimensional proprioceptive state comprising the 3D end-effector position, a 3D axis-angle orientation converted from the simulator quaternion, and two gripper joint positions. The proprioceptive state is projected to the corresponding hidden dimension of each stream and added to its hidden representation rather than appended as a sequence token.

### A.2 Downstream Training

The four interaction programs start from the same robot-video-pretrained causal backbone. The action expert is initialized from width-adapted copies of the corresponding pretrained video-expert layers, while action-specific input/output and conditioning layers are initialized separately. The video and action experts are then jointly optimized during downstream training. All programs use the same data, optimization settings, and flow-matching objective; they differ only in generation order and future cross-modal attention.

For the downstream runs examined here, training uses AdamW with
β1=0.9\beta\_{1}=0.9, β2=0.95\beta\_{2}=0.95, weight decay 0.1, a learning rate of
10−510^{-5}, with 10 warmup steps followed by a constant learning-rate schedule.
We use a per-device batch size of 1 and accumulate gradients over 10 steps, yielding an effective batch size of 10. Gradient norms
are clipped at 2.0, and training uses bf16 mixed precision.
We train all downstream models for 10,000 optimization steps.

#### Flow-matching objective.

Both streams are trained with the rectified-flow objective in
Eq. (4). For implementation, we parameterize the noise level as
σ=1−τ\sigma=1-\tau, such that σ=0\sigma=0 denotes clean data and
σ=1\sigma=1 denotes pure noise. We uniformly sample from a
1,000-level base noise grid and apply the modality-specific shift

|  |  |  |  |
| --- | --- | --- | --- |
|  | Ss​(σ)=s​σ1+(s−1)​σ,sV=5.0,sA=1.0,S\_{s}(\sigma)=\frac{s\sigma}{1+(s-1)\sigma},\qquad s\_{V}=5.0,\quad s\_{A}=1.0, |  | (11) |

for video and action, respectively.

We additionally apply timestep-dependent loss weighting,

|  |  |  |  |
| --- | --- | --- | --- |
|  | wP(σ)∝exp[−2(σ−12)2]−e−1/2,w\_{P}(\sigma)\propto\exp\!\left[-2\left(\sigma-\tfrac{1}{2}\right)^{2}\right]-e^{-1/2}, |  | (12) |

where the weights are normalized to have unit mean over the
corresponding timestep grid. This emphasizes intermediate noise
levels while assigning zero weight to the pure-noise endpoint.

The flow-matching loss is applied only to predicted future video
latents and valid action entries. Video losses are normalized over
the supervised latent elements, while action losses are averaged
over the action horizon after masking invalid action dimensions.
The two modality losses are combined with equal weight,

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒ=ℒV+ℒA.\mathcal{L}=\mathcal{L}\_{V}+\mathcal{L}\_{A}. |  | (13) |

### A.3 Video–Action Interaction Programs

The four programs differ in how predicted video and action
trajectories interact within a generation chunk. Each program
also receives the observed history and task instruction.

#### Joint.

Video and action trajectories are denoised concurrently. During
generation, each stream can attend to the other stream’s evolving
prediction, allowing bidirectional interaction before either
trajectory is complete.

#### Video-to-action (VTA).

The model first generates the future video trajectory without
conditioning on future actions. It then generates the action
trajectory conditioned on the generated video trajectory.

#### Action-to-video (ATV).

The model first generates the future action trajectory without
conditioning on future video. It then generates the video trajectory
conditioned on the generated action trajectory.

#### Decoupled.

Video and action trajectories are generated concurrently, without
cross-modal interaction between their future predictions. Both
streams can still use the observed history and task instruction.

During training, the second stage of VTA and ATV conditions on the ground-truth trajectory of the first modality.
At inference time, this ground-truth trajectory is replaced by the trajectory generated in the first stage.
Joint and Decoupled jointly denoise both modalities in a single generation stage, whereas VTA and ATV use two sequential generation stages.

### A.4 Inference and Closed-Loop Evaluation

#### Sampling.

We use 20 denoising steps for each modality, with the same
modality-specific timestep schedules as in training. Video generation
uses classifier-free guidance with scale 5.0, while no classifier-free
guidance is applied to actions. Key–value caching is enabled during
inference. The history window spans 15 generation chunks, corresponding
to 60 latent video frames and the temporally aligned action history.

#### Action execution.

After resetting to the episode’s initial state, the simulator is advanced for
five zero-action steps to settle, and the policy is initialized from the final
observation. The first generation chunk conditions on this single observation;
the same startup convention is used during training, so no additional history
frames are required before the first prediction. The policy executes each
16-step action chunk before replanning. Episodes terminate upon task success,
after 800 environment steps (including the five initialization steps), or after
50 action chunks, whichever comes first.

#### Evaluation protocol.

For each interaction program, we evaluate three independently trained
seeds. Each checkpoint is evaluated on 10 tasks with 50 closed-loop
episodes per task, for 500 episodes per seed. Within each task, all
interaction programs use the same 50 environment seeds and therefore
share the same set of initial conditions. An episode is counted as
successful if the simulator’s task-success predicate is satisfied at
any environment step, at which point the rollout terminates. We report
the mean and standard deviation of the success rate across the three seeds.

### A.5 Real Robot Setup

![Refer to caption](../../assets/openwam/figure-5.png)

Figure 5: Real-world bimanual setup with two Franka FR3 arms, Flexiv Grav grippers, bimanual GELLO teleoperation [[83](#bib.bib104)], two wrist-mounted RealSense D405 cameras, and a central Orbbec Femto Mega camera.

The real-robot setup, as shown in Figure [5](#A1.F5 "Figure 5 ‣ A.5 Real Robot Setup ‣ Appendix A Implementation Details ‣ OpenWAM: An Open Framework for Composable World-Action Models"), consists of two Franka FR3 arms with Flexiv Grav grippers. We collect demonstrations through bimanual GELLO teleoperation. Two wrist-mounted RealSense D405 cameras record at 1280 × 720 pixels, and a central Orbbec Femto Mega records at 1920 × 1080 pixels, all at 30 fps. Joint positions, end-effector poses, gripper widths, and control commands are recorded with timestamps at 30 Hz. In the chunk-relative formulation, each arm’s target poses are expressed relative to its observed pose at the start of the chunk, while gripper widths remain absolute. Each action contains 20 values: three position coordinates, six values representing orientation, and one gripper width for each arm.

For the real-robot experiments, we collect 200 demonstrations each for
Toast Bread and Rubik’s Cube, and 180 demonstrations for Sort Cups.
Each demonstration is 30 s long. We evaluate the learned
policies over 50 closed-loop episodes for Toast Bread and Rubik’s Cube,
and 36 episodes for Sort Cups.

Table 8:
Data used for causal robot-video pretraining.

| Dataset | Trajectories / takes | Hours | Source type |
| --- | --- | --- | --- |
| Open X-Embodiment (49 manipulation datasets) | 1,300,749 | 1,911.29 | Multi-embodiment robot data |
| AgiBot World Beta | 1,003,672 | 2,976.4 | Real robot manipulation |
| Ego-Exo4D v2 | 5,035 | 221.26 | Human interaction |
| InternData-A1 | 637,498 | 7,433.91 | Synthetic robot manipulation |
| RoboCOIN | 183,157 | 1,306.83 | Real bimanual manipulation |
| RoboMIND | 107,877 | 305.5 | Multi-embodiment robot data |
| FastUMI-100K | 92,823 | 461.77 | Human-guided manipulation |
| UMI family | 5,430 | 24.60 | Human-guided manipulation |

## Appendix B Robot-Video Pretraining

We adapt the Wan2.2-5B video backbone to robot-centric motion and physical
interaction before introducing action prediction. The pretraining corpus
combines robot demonstrations, human manipulation video, and synthetic robot
trajectories across a broad range of embodiments, viewpoints, objects, and
interaction patterns. No action labels are used during this stage.

### B.1 Pretraining Corpus

Our robot-video pretraining corpus combines large-scale real-robot manipulation,
human interaction video, and synthetic robot trajectories. Table [8](#A1.T8 "Table 8 ‣ A.5 Real Robot Setup ‣ Appendix A Implementation Details ‣ OpenWAM: An Open Framework for Composable World-Action Models")
summarizes the source data before training-window sampling. The UMI-family entry
aggregates UMI, DexUMI [[86](#bib.bib106)], UMI on Legs [[23](#bib.bib107)], and MV-UMI.

The corpus contains approximately 3.34 million trajectory or take units and
14.64k nominal hours, spanning heterogeneous robot embodiments, collection
interfaces, viewpoints, human-object interactions, and synthetic manipulation
at scale, providing the visual and interaction prior used by all downstream
OpenWAM models.

### B.2 Causal Adaptation

Pretraining starts from the Wan2.2-5B checkpoint. We retain the pretrained
video representation and optimize the model on the corpus above using the
chunk-causal prediction objective described in Sec. [3](#S3 "3 Methodology ‣ OpenWAM: An Open Framework for Composable World-Action Models"). Future
chunks may attend to the current observation, preceding observations, and
previously generated chunks, but not to later chunks. Tokens within each
chunk are denoised jointly.

This stage uses video alone. Robot actions, proprioception, and task-specific
policy targets are not supplied to the model. The resulting checkpoint serves
both as a standalone causal video predictor and as the common visual
initialization for the downstream OpenWAM interaction programs.

### B.3 Training Compute

Causal robot-video pretraining is performed on 32 NVIDIA B200 GPUs for
14 days. All downstream OpenWAM variants in the main experiments start from
the resulting checkpoint unless otherwise specified.

## Appendix C LIBERO-Long-CF: Counterfactual Dynamics Data

LIBERO demonstrations contain task-directed behavior and cover only a small
fraction of the local state–action–outcome distribution. From each visited
state, they provide essentially one successful action continuation. This is
well suited to imitation learning but provides limited supervision for inverse
and forward dynamics, which must model how alternative actions correspond to
alternative physical outcomes.

We construct LIBERO-Long-CF by branching from task-relevant states in
the ten LIBERO-Long tasks and executing modified future action sequences.
The dataset contains 32,000 counterfactual segments, balanced across tasks.
Each segment contains 128 future controls and 129 synchronized two-view
observations. The original tasks, assets, and simulator physics are preserved.

### C.1 Scale and Intervention Coverage

LIBERO-Long-CF contains 4.10 million control records, compared with 138,090
controls in the 500 source demonstrations, increasing local transition
supervision by approximately 29.7×29.7\times. At 20 Hz, these correspond to
56.9 and 1.92 control-equivalent hours, respectively.

Table 9:
Scale of LIBERO-Long-CF and the source LIBERO-Long demonstration corpus.

|  |  |  |
| --- | --- | --- |
| Quantity | Demonstrations | LIBERO-Long-CF |
| Tasks | 10 | 10 |
| Stored sequences | 500 | 32,000 |
| Sequences / task | 50 | 3,200 |
| Controls / sequence | 276.2 mean | 128 |
| Total controls | 138,090 | 4,096,000 |
| Duration | 1.92 h | 56.9 h |

The branch generator modifies motion magnitude, direction, temporal structure,
individual action axes, stochastic arm motion, and gripper behavior.
Table [10](#A3.T10 "Table 10 ‣ C.1 Scale and Intervention Coverage ‣ Appendix C LIBERO-Long-CF: Counterfactual Dynamics Data ‣ OpenWAM: An Open Framework for Composable World-Action Models") summarizes the intervention distribution.

Table 10:
Intervention composition of LIBERO-Long-CF. Categories denote generation
recipes and may induce overlapping physical effects.

| Intervention family | Fraction (%) |
| --- | --- |
| Stop / rescale arm motion | 9.4 |
| Reverse / redirect translation | 6.3 |
| Axis biases and pulses | 12.5 |
| Dedicated yaw perturbation | 3.1 |
| Noise / randomized arm controls | 12.5 |
| Dedicated gripper interventions | 31.3 |
| Random-duration arm / gripper interventions | 25.0 |

Interventions include stopped and rescaled motion, reversed or redirected
translation, translational and rotational pulses, structured control noise,
piecewise-random commands, and changes to gripper state and timing. All
commands are within LIBERO’s normalized controller range.

### C.2 State and Interaction Coverage

Within the dataset, 75% of segments begin from demonstration-prefix states.
The remaining 25% begin after an additional executed perturbation, extending
the starting-state distribution beyond the demonstrated trajectories.

Among characterized perturbed starts, the end-effector state is on average
3.34 cm from the nearest point on the corresponding demonstrated path
(median 1.90 cm). Under thresholds of 1 cm translation, 5∘5^{\circ} rotation,
or 5% articulated-joint travel, 61.6% also contain object configurations
outside the corresponding demonstrated configurations.

The corpus contains substantial physical interaction. As shown in
Table [11](#A3.T11 "Table 11 ‣ C.2 State and Interaction Coverage ‣ Appendix C LIBERO-Long-CF: Counterfactual Dynamics Data ‣ OpenWAM: An Open Framework for Composable World-Action Models"), 90.4% of characterized segments contain
gripper contact with an object or fixture, 50.0% contain a detected grasp,
and 72.3% alter object configuration relative to the same-start reference
continuation.

Table 11:
Physical interaction statistics for LIBERO-Long-CF. Categories overlap.

| Measured interaction | Rate (%) |
| --- | --- |
| Gripper–object / fixture contact | 90.4 |
| Detected grasp | 50.0 |
| Object-configuration effect | 72.3 |

### C.3 Representation for Local Dynamics Learning

Each segment contains two synchronized 128×128128\times 128 RGB streams,
128 seven-dimensional delta-OSC controls, and 129 proprioceptive states.
Actions contain three translation channels, three rotation channels, and one
gripper command.

Both camera streams are encoded with the OpenWAM video VAE. The encoded
sequence contains one boundary observation and 32 future latent frames, with
four controls aligned to each future latent frame.

Local-context IDM conditions on the boundary observation, proprioception, and
future visual trajectory to predict the action sequence. Local-context FDM
conditions on the boundary observation, proprioception, and action sequence to
predict the future visual trajectory. Both objectives exclude task language
and pre-start history.

## Appendix D Ablations

### D.1 Effect of Video-Backbone Initialization

We further examine whether the benefit of robot-video pretraining is specific to
VTA or persists across interaction programs. Under otherwise matched downstream
training, we initialize the video backbone either randomly, from the original
Wan2.2 checkpoint, or from our robot-video-pretrained causal checkpoint.
Table [12](#A4.T12 "Table 12 ‣ D.1 Effect of Video-Backbone Initialization ‣ Appendix D Ablations ‣ OpenWAM: An Open Framework for Composable World-Action Models") shows a consistent ordering for both VTA
and Joint. Relative to Wan2.2 initialization, robot-video pretraining improves
success by 29.4 percentage points for VTA and 34.4 points for Joint, reaching
97.8% and 96.6%, respectively. Random initialization performs substantially
worse for both programs. These results indicate that the benefit of the
robot-video-pretrained backbone transfers across distinct video–action interaction
structures.

Table 12:
Effect of video-backbone initialization on closed-loop LIBERO-Long success.
Downstream architecture and training are held fixed within each interaction
program.

| Video initialization | VTA (%) | Joint (%) |
| --- | --- | --- |
| Random initialization | 20.0 | 27.2 |
| Original Wan2.2 | 68.4 | 62.2 |
| Robot-video pretrained | 97.8 | 96.6 |

Table 13:
Effect of the Mixture-of-Transformers architecture on closed-loop
LIBERO-Long success. All variants use robot-video-pretrained
initialization.

| Architecture | VTA (%) | Joint (%) |
| --- | --- | --- |
| Non-MoT | 92.8 | 93.6 |
| MoT | 97.8 | 96.6 |

Table 14:
Policy and dynamics accuracy on LIBERO-Long.
LC-IDM and LC-FDM are independently trained specialist checkpoints;
the multi-objective model trains policy, IDM, and FDM within a single
checkpoint.
Lower is better for MSE and IDM error; higher is better for success and SSIM.

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Policy | Real demonstrations | | | | Counterfactual transitions | | | |
| Model | Succ. (%) | FDM MSE ↓\downarrow | FDM SSIM ↑\uparrow | IDM pos. (cm) ↓\downarrow | IDM rot. (∘) ↓\downarrow | FDM MSE ↓\downarrow | FDM SSIM ↑\uparrow | IDM pos. (cm) ↓\downarrow | IDM rot. (∘) ↓\downarrow |
| OpenWAM, LC-IDM, CF-only | – | – | – | 1.76 | 2.39 | – | – | 1.17 | 3.60 |
| OpenWAM, LC-IDM, mixed | – | – | – | 0.44 | 1.21 | – | – | 1.22 | 3.68 |
| OpenWAM, LC-FDM, CF-only | – | 0.00734 | 0.9126 | – | – | 0.00940 | 0.8889 | – | – |
| OpenWAM, LC-FDM, mixed | – | 0.00186 | 0.9776 | – | – | 0.00962 | 0.8859 | – | – |
| OpenWAM, multi-objective | 92.8 | 0.00058 | 0.9934 | 0.43 | 1.10 | 0.01416 | 0.8398 | 1.73 | 3.55 |
| UVA | 88.0 | 0.00279 | 0.9645 | 2.03 | 1.60 | 0.01514 | 0.8134 | 3.57 | 12.99 |

### D.2 Effect of the Mixture-of-Transformers Architecture

We isolate the effect of the Mixture-of-Transformers (MoT) parameterization
while keeping the pretrained visual foundation fixed. Both variants start
from the same robot-video-pretrained video checkpoint and use the same
downstream data and training procedure. In the non-MoT variant, video and
action tokens are processed by the same pretrained DiT; the MoT variant retains the pretrained video expert and introduces a separate action expert initialized from width-adapted copies of the corresponding video-expert layers. As shown in Table [13](#A4.T13 "Table 13 ‣ D.1 Effect of Video-Backbone Initialization ‣ Appendix D Ablations ‣ OpenWAM: An Open Framework for Composable World-Action Models"), the
shared-DiT model already achieves strong performance, reaching 92.8% for
VTA and 93.6% for Joint. MoT further improves success to 97.8% and
96.6%, corresponding to gains of 5.0 and 3.0 percentage points,
respectively.

## Appendix E External Dynamics Comparison

We compare OpenWAM with UVA [[45](#bib.bib20)], the closest released
LIBERO system in our related work that exposes policy, inverse-dynamics,
and forward-dynamics objectives within one model. Table [14](#A4.T14 "Table 14 ‣ D.1 Effect of Video-Backbone Initialization ‣ Appendix D Ablations ‣ OpenWAM: An Open Framework for Composable World-Action Models")
covers two settings: independently trained local-context dynamics components
and a single multi-objective checkpoint trained jointly across policy, IDM,
and FDM objectives.

For FDM, we report RGB prediction error in a common agent-view image space.
For IDM, the two systems use different action parameterizations, so we compare
the resulting end-effector trajectory error after executing the predicted
actions from the same simulator state.

### E.1 Independent Dynamics Components

The LC-IDM and LC-FDM specialists are trained either on counterfactual
transitions only or on a 60/40 mixture of counterfactual and demonstration
transitions. CF-only specialists are strongest on the held-out
counterfactual distribution, while mixed supervision substantially improves
fidelity on real demonstrations. Both remain well ahead of UVA on the
counterfactual dynamics metrics.

### E.2 Unified Policy and Dynamics Modeling

UVA trains policy generation, inverse dynamics, and forward dynamics within a
single model. We therefore also evaluate one OpenWAM checkpoint trained with
60% real joint video–action supervision, 20% local-context IDM supervision,
and 20% local-context FDM supervision; the IDM and FDM portions are each split
equally between demonstration and counterfactual transitions.

The unified OpenWAM checkpoint outperforms UVA on policy success and on the
evaluated IDM and FDM metrics. Its counterfactual dynamics accuracy is weaker
than that of the dedicated specialists, showing the expected tradeoff between
multi-objective training and specialization. The unified OpenWAM checkpoint also gives the lowest IDM and FDM errors on real
demonstrations. These numbers measure fit to the demonstration distribution,
not held-out generalization, because some of the same demonstrations may also
be seen by the policy objective during training. Its policy score is also lower
than the policy-specialized OpenWAM models as only 60% of training updates
optimize the policy objective.
