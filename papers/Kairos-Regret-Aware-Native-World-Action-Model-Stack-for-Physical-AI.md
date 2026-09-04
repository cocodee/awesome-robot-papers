Kairos: A Regret-Aware Native World-Action Model
Stack for Physical AI
Learning, Maintaining, and Deploying Control-Sufficient World States
Kairos Team
Abstract
World models are becoming a central substrate for Physical AI, yet their current development
is differentiating across representational, generative, interactive, and unified understanding–
generation–prediction world models. While these paradigms have advanced abstract world
reasoning, high-fidelity visual generation, interactive simulation, and embodied world-action
modeling, none alone provides the deployable, long-horizon, control-sufficient state required
by embodied agents. We introduce Kairos, a regret-aware native world-action model stack
for Physical AI. Kairos is motivated by the view that a physical world model should not
aim to fully simulate all future pixels, but should learn and maintain the information most
relevant to embodiment control: object state, spatial relations, contact conditions, task
progress, action consequences, failure boundaries, and deployment uncertainty.
Kairos establishes three model-side prerequisites toward this goal. First, it learns control-
relevant information through a Cross-Embodiment Data Curriculum, which organizes
open-world videos, human behavioral data, and robot interactions into an intervention-
strength progression from passive physical observation to intentional behavior and embodied
action grounding. Second, it maintains control-sufficient states through a unified under-
standing, generation, and prediction architecture equipped with Hybrid Linear
Temporal Attention, where local, mid-range, and global temporal pathways support
multi-timescale state maintenance under efficient inference. Third, it deploys these states
through a Deployment-Aware System Co-Design, treating latency, memory footprint,
and hardware compatibility as first-order constraints for future observation, action, and
feedback loops.
Experiments on embodied world-model benchmarks, world-action benchmarks, long-horizon
generation,andinference-efficiencyevaluationshowthatKairosachievessuperiorperformance
while offering a favorable efficiency to capability trade-off. These results provide proxy
evidence for regret-relevant capabilities, including physical plausibility, instruction grounding,
joint world-action prediction, long-horizon consistency, and deployment readiness. Direct
validation of real-robot closed-loop regret reduction, including rollout correlation, failure
prediction, safety filtering, recovery learning, and measurable policy improvement from
imagined experience, remains an important direction for future Kairos development.
Date: July 7, 2026
Code: https://github.com/kairos-agi/kairos
Hugging Face: https://huggingface.co/kairos-agi
ModelScope: https://modelscope.cn/collections/kairos-team/kairos30
1
6202
luJ
3
]IA.sc[
3v33561.6062:viXra

Contents
1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
2 Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
2.1 Native Architecture with Unified Understanding, Generation, and Prediction . . . . 13
2.1.1 World Understanding: Control-Sufficient State Construction . . . . . . . . . . 14
2.1.2 World Generation: Control-State Regularization . . . . . . . . . . . . . . . . 15
2.1.3 World Prediction: Joint World-Action Modeling . . . . . . . . . . . . . . . . . 17
2.2 Efficient Diffusion Transformer with Hybrid Linear Attention . . . . . . . . . . . . . 19
2.2.1 Global Pathway: Gated Linear Attention as Persistent Causal Memory . . . . 20
2.2.2 Local and Mid-Range Pathways: Sliding-Window and Dilated Sliding-Window
Attention . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
2.3 Theoretical Scope and Analysis of Hybrid Multi-Scale Temporal Memory . . . . . . . 23
2.3.1 Necessity of Persistent Internal States . . . . . . . . . . . . . . . . . . . . . . 23
2.3.2 Approximate Sufficiency of Hybrid Multi-Scale Temporal Memory . . . . . . 24
2.3.3 Interpretation for Kairos . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
2.3.4 From Theoretical State Maintenance to Regret-Aware Physical AI . . . . . . 25
3 Native Pretraining Paradigm for Physical AI . . . . . . . . . . . . . . . . . . . . . . . . . 26
3.1 Native Pretraining with Cross-Embodiment Data Curriculum . . . . . . . . . . . . . 27
3.2 Stage I: Physical Pretraining . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
3.3 Stage II: Embodied Pretraining with Human-centric Data . . . . . . . . . . . . . . . 33
3.4 Stage III: Regret-Aware World-Action Training . . . . . . . . . . . . . . . . . . . . . 34
3.4.1 Regret Alignment Training . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36
3.4.2 Joint World-Action Training . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36
3.5 Training Infrastructure for Control-Sufficient Pretraining . . . . . . . . . . . . . . . . 37
3.6 Summary: From Flat Data Scaling to a Staged Cross-Embodiment Curriculum . . . 38
4 Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
4.1 Data Collection: Multi-Source Experience Acquisition . . . . . . . . . . . . . . . . . 40
4.2 Data Curation: From Quality Filtering to Control-Relevant Filtering . . . . . . . . . 41
4.3 Tagging: Structured Indexing for Control-Relevant Sampling. . . . . . . . . . . . . . 44
4.4 Captioning: From Visual Description to Control-State Supervision . . . . . . . . . . 45
4.5 Enhanced Text with Control-Oriented Chain of Thought . . . . . . . . . . . . . . . . 47
4.6 Data Engineering Infrastructure for Scalable Control-Information Processing . . . . . 48
4.7 Limitations and Future Data Directions . . . . . . . . . . . . . . . . . . . . . . . . . 49
4.8 Summary: A Data Engine for Control-Sufficient World Modeling . . . . . . . . . . . 50
5 Inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50
5.1 Toward Self-Evolution: Proxy Rollout–Evaluation–Refinement . . . . . . . . . . . . . 51
5.2 Prompt Self-Alignment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52
5.3 Inference Efficiency . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53
5.3.1 Timestep Distillation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53
5.3.2 Hardware-Aware Inference Optimization . . . . . . . . . . . . . . . . . . . . . 56
5.3.3 Efficiency Comparison . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 58
5.4 Inference Modes for Kairos . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59
5.5 Summary: From Fast Generation to Deployment-Aware World-Action Operation . . 60
2

6 Evaluation Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 61
6.1 Evaluation Scope and Proxy-Evidence Framing . . . . . . . . . . . . . . . . . . . . . 61
6.2 Embodied World Model Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . . 61
6.2.1 WorldModelBench-Robot . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 61
6.2.2 DreamGen Bench . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62
6.2.3 PAI-Bench-Robot . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 64
6.2.4 Human Evaluation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 65
6.2.5 Ablation Studies: Human-Centric Scaling and VLM Selection . . . . . . . . . 66
6.3 World Action Model Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
6.3.1 RoboTwin 2.0 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
6.3.2 LIBERO-Plus . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 68
6.3.3 Ablation Studies: Human-Centric Pretraining and Joint World-Action Training 69
6.4 General World Model Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . . . 70
6.4.1 PAI-Bench . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 70
6.4.2 WorldModelBench . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 71
6.4.3 VideoPhy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 73
6.5 Long-Horizon Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 74
6.6 Efficiency–Capability Trade-off as Deployment Proxy . . . . . . . . . . . . . . . . . . 76
6.7 Regret-Relevant Cases . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76
6.8 Current Evaluation Limitations and Future Closed-Loop Validation . . . . . . . . . . 77
6.9 Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 78
7 Related Work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 79
7.1 Video Generation Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 79
7.2 World Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 80
7.3 World Action Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 81
7.4 Efficient Attention Mechanisms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 82
8 Conclusion and Future Works . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 82
8.1 Future Works . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 84
8.1.1 Direct Evaluation of Control-Sufficient States . . . . . . . . . . . . . . . . . . 84
8.1.2 Counterfactual Action Validation . . . . . . . . . . . . . . . . . . . . . . . . . 85
8.1.3 Interventional Generalization Across Observation, Human Intervention, and
Robot Intervention . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 86
8.1.4 Multi-Timescale Memory Beyond 15-Second Generation . . . . . . . . . . . . 87
8.1.5 Control-Information-Density Data Engine . . . . . . . . . . . . . . . . . . . . 87
8.2 Outlook . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89
Appendix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 104
A Contributors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 104
B Theoretical Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 105
B.1 Problem Setup and Theoretical Scope . . . . . . . . . . . . . . . . . . . . . . . . . . 105
B.2 Necessity of Persistent Internal States . . . . . . . . . . . . . . . . . . . . . . . . . . 107
B.3 Approximate Sufficiency of a Hybrid Multi-Scale Temporal Memory. . . . . . . . . . 111
3

1 Introduction
World models [1] are rapidly emerging as a central substrate for Physical AI. They are no longer
expected to be merely generative models that render visually plausible futures; they are increasingly
expected to support physical understanding, temporal prediction, embodied interaction, action-
conditioned reasoning, deployment-time decision support, and eventually continual adaptation in
real environments. In this broader view, a useful world model is an internal predictive system that
acquires, organizes, maintains, and operationalizes knowledge about how the world evolves under
time, uncertainty, and action. Recent advances across video generation [2–19], latent dynamics
modeling [20–27], model-based reinforcement learning [22, 28–30], embodied AI, and interactive
simulation [31–50] all point toward the same direction: world models are moving from offline
demonstrations toward operational infrastructure for embodied and physical intelligence.
To understand this shift, recent advancements in world models can be broadly viewed through four
industry-oriented directions. The first direction focuses on generative world models, or generative
pixel-level rendering, which primarily encompasses video generation and the synthesis of high-fidelity
visual futures. Models in thiscategory aim toproduce temporally coherent continuations of theworld
directly in pixel space. A prominent example is NVIDIA’s Cosmos [3], which leverages generative
video foundation models as digital twins and essential infrastructure for Physical AI.
The second direction shifts the focus toward representational world models, emphasizing
predictive latent embedding and abstract world reasoning. Rather than rendering pixels, this
approach explicitly frames world models as systems that learn physically meaningful predictive
structures entirely within abstract representation spaces. Meta’s JEPA family (e.g., V-JEPA 2 [25],
V-JEPA 2.1 [26], and DINO-world [27]) exemplifies this trajectory. By internally anticipating
outcomes in a latent form, these models inherently support downstream tasks such as physical
understanding, zero-shot planning, and robot control. The core premise here is that a world model’s
utility for decision-making relies on its capacity to anticipate the future abstractly, bypassing the
immense computational overhead of pixel-level rendering. Recent evidence that semantic latent
spaces can be more useful for robotic policy evaluation and planning than reconstruction-aligned
latents further supports this emphasis on action-relevant structure over pixel fidelity [51].
The third direction advances interactive world models, emphasizing the creation of persistent
simulations and interactive arenas. This encompasses both static spatial worlds and dynamic
interactive environments. For instance, models focusing on static spatial intelligence, such as World
Labs’ Marble [31] and TeleWorld [32], excel at building explorable 3D worlds that agents can
perceive and navigate, emphasizing geometric consistency and "worldness." Extending into dynamic
interaction, environment generators like DeepMind’s Genie 3 [33], HY-World 1.5 [34], and LingBot-
World [35] instantiate fully manipulable worlds from simple prompts. Furthermore, frameworks like
Dreamer 4 [29] utilize these models as internal simulators where agents can recursively optimize
long-horizon behaviors through imagination. In this paradigm, models are judged by their capability
to act as comprehensive engines for spatial exploration, interaction, and self-evolution.
The fourth direction is emerging around unified understanding–generation–prediction world-
action models. This direction does not treat understanding, generation, prediction, and action as
separate downstream modules. Instead, it aims to unify semantic and physical understanding, multi-
modal future imagination, future-state prediction, embodied action modeling, and deployment-time
decision support within a shared world-action substrate. Recent systems such as Cosmos 3 [52] and
MotuBrain [53] reflect this broader movement by integrating multimodal understanding, generation,
and world-action modeling within a unified Physical AI backbone. Taken together, these advances
4

show that the field is no longer converging on a single definition of world models as “video gener-
ators.” For industrial deployment, this fourth direction is the most closely aligned with Physical
AI, because its purpose is not merely to abstract the world, reproduce the world, or simulate an
interactive scene, but to connect generation, physics, cognition, and action so that an embodied
agent can preserve control-relevant information, evaluate action consequences, and run inside real
observation–action–feedback loops. Kairos is our systematic, full-stack exploration along this fourth
class of embodied world models.
Operationalizing this direction for Physical AI requires a first principle: a world model should not be
understood as a full simulator of the world. The real world contains far more information than any
robot can observe, compute, store, or act upon. A robot picking up a cup does not need to predict
every future pixel of the table texture, the shape of clouds outside the window, or the motion of
irrelevant background objects. What matters is whether the robot can preserve the information
required for embodied control: the cup position, mass, friction, grasp affordance, contact condition,
hand pose, task progress, failure risk, and the consequences of alternative actions. Therefore, the
objective of an embodied world model is not to reproduce all future sensory information, but to
learn a compact internal state that is sufficient for predicting task-relevant future variables. We refer
to this internal representation as a control-sufficient state.
The challenge becomes sharper in robotics. Physical agents operate under partial observability,
embodiment-specific constraints, contact-rich dynamics, discontinuous state transitions, limited
real-world trial-and-error, and safety-sensitive deployment conditions. In manipulation, a small
changeincontact, friction, grasppose, forcedistribution, orobjectgeometrycandeterminewhethera
task succeeds or fails. In navigation, local observations must be integrated into persistent spatial and
semantic memory. In long-horizon operation, delayed effects and accumulated errors can determine
downstream outcomes. In real deployment, the model must produce useful predictions within the
time budget of the control loop. Therefore, the central missing link is not another visual simulator,
but a deployable, long-horizon, control-sufficient state.
Formally, given the observation–action history H , task goal g, and candidate future action sequence
t
a , an embodied world model should maintain an internal state Z that preserves the informa-
t:t+H−1 t
tion needed to predict task-relevant future states, failure events, task progress, physical cost, and
the discrepancy between imagined and real outcomes. State Z is not merely a visual representation,
t
but a control-sufficient state: a compressed representation that retains the variables necessary for
action selection, risk assessment, failure anticipation, and recovery planning. A model that generates
realistic videos but cannot predict failures, distinguish the consequences of different actions, or
assess policy risk remains an incomplete embodied world model. Conversely, a model that does
not synthesize every pixel but can reliably predict the consequences of different actions and failure
boundaries is closer to the type of embodied world model required by Physical AI.
This perspective changes how embodied world models should be evaluated. In conventional genera-
tive modeling, success is often measured by visual realism, temporal smoothness and consistency,
instruction following, or reconstruction quality. These criteria remain useful, but they are insufficient
for Physical AI. A robot does not pay a cost when its predicted pixels are slightly blurry; it pays a
cost when a cup slips, a collision occurs, a task fails, a human must intervene, or a safety boundary
is crossed. For embodied intelligence, regret is not an abstract learning-theoretic quantity alone;
it corresponds to real-world costs such as collision, damage, wasted time, recovery effort, unsafe
contact, and failed task completion. In this report, we therefore use regret reduction as the guiding
principle for embodied world-model design. Kairos is designed as a regret-aware world-action model
stack that establishes several model-side prerequisites for future regret-minimizing Physical AI:
5

control-relevant information acquisition, control-sufficient state compression, joint world-action
prediction, multi-timescale state maintenance, and deployment-ready inference.
To make this evaluation principle precise, we formalize the value of an internal world state by the
excess physical cost it induces for future action selection. The key question is not whether the state
reconstructs all observations, but whether it preserves the information needed for low-cost decisions
under a task goal. Let denote the observation–action history up to time t, the task goal,
|     |     |     | H   |     |     |     |     | g ∈ | G   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
t
and Z = f(H ) ∈ Z a compact state representation derived from H via a compression function
| t   |     | t   |     |     |     |     | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
f : H → Z. For a future horizon H, let A denote the action space and let AH denote the space of
| length-H | future | action | sequences. | We use |           |         |     |     |     |
| -------- | ------ | ------ | ---------- | ------ | --------- | ------- | --- | --- | --- |
|          |        |        |            |        | J (a      | | H ,g) |     |     |     |
|          |        |        |            |        | H t:t+H−1 | t       |     |     |     |
to denote the conditional expected physical cost of executing a candidate future action sequence
a ∈ AH under the current history H and goal g. This cost captures deployment-level physical
| t:t+H−1 |     |     |     |     | t   |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and operational consequences, such as task failure, collision, unsafe contact, recovery effort, and
downstream costs caused by discrepancies between imagined and real outcomes.
Since is obtained by compressing , it may discard information that is relevant for planning
| Z   |     |     |     | H   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | t   |     |     |     | t   |     |     |     |     |
low-cost actions under J . To quantify this potential loss, we compare planners that act on Z with
|          |      |             | H      |              |     |       |     |     | t   |
| -------- | ---- | ----------- | ------ | ------------ | --- | ----- | --- | --- | --- |
| planners | that | have access | to the | full history | H   | . Let |     |     |     |
t
|     |     |     |     |     | π : | Z ×G → AH |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- |
Z
denote a horizon-level planner that maps the compressed state and goal to a length-H future action
| sequence. | Similarly, | let |     |     |     |          |     |     |     |
| --------- | ---------- | --- | --- | --- | --- | -------- | --- | --- | --- |
|           |            |     |     |     | π : | H×G → AH |     |     |     |
H
denote a planner with access to the full history and goal. Thus, the two planners differ only in the
| information | available |                        | for planning. |        |     |      |     |     |     |
| ----------- | --------- | ---------------------- | ------------- | ------ | --- | ---- | --- | --- | --- |
| We define   | the       | representation-induced |               | regret | of  | f as |     |     |     |
Reg (f;g) = infE[J (π (Z ,g) | H ,g)]−infE[J (π (H ,g) | H ,g)],
|     |     | H   |     | H Z | t   | t   | H H t | t   |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
|     |     |     | πZ  |     |     | πH  |       |     |     |
where the outer expectation is taken over the distribution of histories . The first term is the best
H t
achievable expected physical cost when planning from the compressed state Z , while the second
t
term is the best achievable expected physical cost when planning from the full history H . Because
t
is derived from , any planner based on can be emulated by a planner based on . Therefore,
| Z   |     | H   |     |     | Z   |     |     |     | H   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t   |     | t   |     |     |     | t   |     |     | t   |
under the same admissible planner class, this regret is nonnegative and measures the excess physical
| cost induced |     | by compressing | H   | into Z | .   |     |     |     |     |
| ------------ | --- | -------------- | --- | ------ | --- | --- | --- | --- | --- |
|              |     |                |     | t t    |     |     |     |     |     |
A regret-aware world-action model should therefore learn a compact state representation that makes
small. Such a state should discard irrelevant visual detail while retaining information
Reg (f;g)
H
about action consequences, failure boundaries, safety risks, recovery costs, and imagined–real gaps.
Under the above formulation, an embodied world model for Physical AI must satisfy several
requirements. The first is regret-aware information compression. Its value lies not in maximizing the
number of future pixels it can generate, but in preserving the information that reduces Reg (f;g)
H
per unit of internal state, computation, latency, memory, and risk. A large model that generates
visually impressive rollouts but cannot run before action execution may be less useful for robotics
thana smaller modelthatmaintainstherightcontrolvariableswithlowlatency. Foraphysicalagent,
6

information is valuable when it reduces uncertainty about action consequences, failure boundaries,
contact dynamics, recovery strategies, and safety risks. This principle explains why world modeling,
representation learning, data selection, temporal memory, and system efficiency should not be treated
as separate engineering concerns: they are all part of the same question—what information should
be preserved so that future costly mistakes can be reduced?
A second requirement is counterfactual closure. A passive video model can answer the question: what
is likely to happen next? A robot needs to answer a more difficult question: what will happen if I act
now, and how would the future change if I chose a different action? In terms of J , counterfactual
H
closure is needed because the model must compare the physical costs of alternative action sequences
from the same state. A world model that can only continue the natural evolution of a training video
remains a spectator of the world. An embodied world model must support multiple action branches
from the same internal state. Given the same Z , it should represent how different candidate actions
t
lead to different future states, different risks, and different task outcomes. In Physical AI, future
actions should not be treated as an external policy output attached after world modeling; they
should be part of the modeled physical evolution of the world under embodied intervention.
A third requirement is interventional generalization. Classical supervised learning typically assumes
that training and testing data are drawn from the same distribution. Robotic deployment violates
this assumption. Once a robot acts, it changes the future data distribution. The agent does not
merelyobservetheworld; itintervenesinit. Thiscreatesaninterventionaldistributionshift: training
data may contain observation–action correlations, but deployment requires action–outcome causation.
A model trained primarily on passive videos may learn broad visual and physical regularities but
fail to predict how robot actions change the environment. A model trained only on narrow robot
data may acquire action grounding but lack general physical and semantic priors. An embodied
world model must therefore learn across a hierarchy of intervention strengths, moving from passive
observation toward intentional behavior and finally embodied action grounding.
A fourth requirement is multi-timescale control-state maintenance. Long-horizon world modeling
should not be reduced to longer context modeling. For embodied agents, the key is not to store all
historical tokens, but to maintain the state variables that remain relevant for future control. These
variables naturally live on different timescales. Millisecond-to-second dynamics include contact, slip,
collision, hand–eye correction, and short-term motion continuity. Second-to-minute dynamics include
subtask status, object locations, tool use, and local interaction history. Minute-to-hour dynamics
include task plans, environmental changes, user preferences, and accumulated scene context. Hour-
to-day dynamics include repeated failure patterns, scene regularities, and individualized experience.
A single memory mechanism is unlikely to serve all of these requirements. A deployable world model
needs a structured temporal architecture that allocates fast feedback, mid-range event continuity,
and long-range causal memory to different but interacting pathways.
A fifth requirement is control information density. Data value in Physical AI should not be measured
onlybyrawscale. Ashortsegmentcontainingafailure,recovery,contacttransition,orboundary-case
behaviormaybemorevaluablethanhoursofordinarysuccessfulvideo, becauseitreducesuncertainty
about the variables that matter for control. Under the regret formulation, high-value data are those
that reduce uncertainty about the variables that determine future physical cost, especially failures,
contact transitions, recoveries, and boundary cases. Failure data reveals when and why the policy
breaks. Contact-rich data reveals friction, force, deformation, slip, and grasp stability. Recovery
data reveals how the system can return from an error state. Boundary-case data reveals the margin
between success and failure. Ordinary successful trajectories remain useful, but they often contain
less information about failure boundaries. Ordinary open-world videos provide broad physical priors,
7

but usually lack action grounding. Thus, data engineering for Physical AI should not only increase
the volume of training data; it should increase the density of control-relevant information.
These five requirements expose a set of in current world models:
|            |     |                |     | coupled    | bottlenecks |           |     |              |                      |     |
| ---------- | --- | -------------- | --- | ---------- | ----------- | --------- | --- | ------------ | -------------------- | --- |
| 1.         |     |                |     |            | World       | knowledge |     | is scattered | across heterogeneous |     |
| Fragmented |     | interventional |     | knowledge. |             |           |     |              |                      |     |
experience sources. Open-world videos provide broad physical priors, human behavior provides
intentional task structure, and robot data provides action grounding, but these sources are
| often | mixed                 | without | a principled | progression.        |     |          |                 |     |                |        |
| ----- | --------------------- | ------- | ------------ | ------------------- | --- | -------- | --------------- | --- | -------------- | ------ |
| 2.    |                       |         |              |                     |     | Existing | representations |     | often preserve | visual |
| Lack  | of control-sufficient |         |              | state preservation. |     |          |                 |     |                |        |
detail while discarding contact, task progress, or failure risk—the very variables that matter
| for | embodied | control. |     |     |     |     |     |     |     |     |
| --- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
3. Insufficient counterfactual action closure. Many models predict plausible futures but cannot
| reliably | compare | alternative |     | action outcomes |     | from | the same | state. |     |     |
| -------- | ------- | ----------- | --- | --------------- | --- | ---- | -------- | ------ | --- | --- |
4. Fragile multi-timescale state maintenance. Local visual continuation does not guarantee
| persistent |            | state maintenance |     | over long        | horizons. |            |                                       |     |     |     |
| ---------- | ---------- | ----------------- | --- | ---------------- | --------- | ---------- | ------------------------------------- | --- | --- | --- |
| 5.         |            |                   |     |                  |           |            | Modelsthatachievestrongofflinemetrics |     |     |     |
| Offline    | capability | without           |     | deployment-ready |           | inference. |                                       |     |     |     |
often miss latency, memory, or hardware constraints required by real systems, leaving them
| unable | to  | participate | in observation–action–feedback |     |     |     | loops. |     |     |     |
| ------ | --- | ----------- | ------------------------------ | --- | --- | --- | ------ | --- | --- | --- |
Addressing these bottlenecks separately risks producing systems that are strong along one dimension
but fundamentally incomplete as substrates for physical intelligence. Figure 1 visualizes this gap-to-
design logic, showing how Kairos connects existing world-model capabilities to the requirements of
| Physical | AI through | a regret-aware |     | world-action |     | stack. |     |     |     |     |
| -------- | ---------- | -------------- | --- | ------------ | --- | ------ | --- | --- | --- | --- |
Kairos is designed around this bottleneck structure (Figure 2). Rather than stopping at representa-
tional abstraction, pixel-level generation, or interactive simulation, Kairos systematically explores
the fourth class of unified understanding–generation–prediction world-action models through a native
world-action model stack for Physical AI. Its central objective is to learn, maintain, and deploy
a control-sufficient state Z . This state is not intended to simulate the full world; it is intended
t
to preserve the variables needed for joint world-action prediction, long-horizon consistency, failure
anticipation, and future closed-loop evaluation. In this sense, Kairos should be understood as a
regret-aware step toward control-sufficient Physical AI: it aims to learn, maintain, and deploy a
compressed state Z = f(H ) that preserves information relevant to reducing Reg (f;g), while
|     |     | t   | t   |     |     |     |     |     | H   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
direct validation of reduced Reg in real closed-loop systems remains future work.
H
The first pillar of Kairos is a Cross-Embodiment Data Curriculum for interventional control-
information acquisition. Instead of treating open-world videos, human demonstrations, and robot
data as a flat mixture, Kairos organizes them into a progression over intervention strength. Open-
world videos provide passive physical observation: they expose broad environmental dynamics, object
motion, scene evolution, and physical regularities without direct robot intervention. Human behav-
ioral data provides intentional intervention: it reveals task organization, goal-directed interaction,
object manipulation strategies, and structured behavior patterns. Robot interaction data provides
embodied intervention: it grounds perception–action alignment, embodiment-specific constraints,
actuationlimits, executionerrors, proprioception, andmotoraffordances. Thiscurriculumisdesigned
to move the model from observation–action correlation toward action–outcome causation.
ThesecondpillarofKairosisaNativeUnifiedArchitectureforcontrol-sufficientstatecompression
and counterfactual world-action prediction. Kairos does not simply connect separate modules for
8

Figure 1 Motivation of Kairos. Existing world models have advanced along representational, generative,
interactive, and unified world-action directions, providing useful capabilities such as abstract reasoning,
high-fidelity future generation, simulation-based interaction, and embodied world-action modeling. However,
Physical AI requires more than visually plausible future simulation: it needs control-sufficient states,
counterfactual action closure, multi-timescale state maintenance, and deployment-ready inference. Kairos
addresses these gaps through a cross-embodiment data curriculum, a unified world-action architecture with
hybrid temporal memory, and deployment-aware co-design, forming a regret-aware world-action stack for
learning, maintaining, and deploying control-sufficient states.
understanding, generation, and prediction. Instead, it aims to maintain semantic understanding,
visual generation, physical prediction, and action prediction within a shared world-action state Z .
t
World Understanding extracts control-relevant semantic and physical variables from heterogeneous
observations. WorldGenerationservesasanauxiliaryinterfaceforlearningphysicallyplausiblefuture
evolution and regularizing the shared latent state through visual consistency, object permanence,
and physical coherence. World Prediction provides the world-action interface, jointly modeling
environmental dynamics and future robot actions. By using Video DiT for future visual tokens,
Action DiT for future action tokens, and mixed attention to couple video and action streams, Kairos
treats future actions as part of the physical evolution of the world rather than as an external policy
head.
The third pillar of Kairos is Hybrid Linear Temporal Attention for multi-timescale control-state
maintenance. Long-horizon Physical AI requires more than extending context length. Kairos
decomposes temporal modeling into complementary pathways. Sliding-Window Attention captures
local dynamics, including short-term motion continuity, contact transitions, slip, collision, and fast
hand–eye correction. Dilated Sliding-Window Attention captures mid-range dependencies, including
subtask transitions, object–tool interaction histories, and delayed but still localized causal effects.
Gated Linear Attention [54] acts as persistent global causal memory, maintaining object permanence,
task progress, long-range dependencies, delayed physical effects, and failure history under efficient
9

Figure 2 FrameworkofKairos. WorldUnderstandingextractsacontrol-sufficientstateZ t ; WorldGeneration
regularizes physical consistency of Z through future imagination; World Prediction uses Z for future
|     |     | t   |     |     | t   |
| --- | --- | --- | --- | --- | --- |
state-action sequences; Deployment-Aware System Co-Design runs Z under latency/memory constraints.
t
The Proxy Rollout–Evaluation–Refinement loop establishes inference-side prerequisites for future closed-loop
self-evolution.
inference. This temporal factorization should be interpreted not merely as an efficiency mechanism,
but as a structured approach to maintaining control-relevant state across multiple timescales. The
theoretical analysis in this report studies this design under stated assumptions and provides bounds
that support its role in mitigating long-horizon error accumulation, rather than claiming universal
| real-world | guarantees.      |                  |                  |                 |            |
| ---------- | ---------------- | ---------------- | ---------------- | --------------- | ---------- |
| The fourth | pillar of Kairos | is a             |                  | for closed-loop | readiness. |
|            |                  | Deployment-Aware | System Co-Design |                 |            |
For Physical AI, efficiency is not a post-hoc acceleration problem; it is part of the modeling objective.
The world model must run within the latency, memory, communication, and hardware constraints of
real systems. Kairos therefore treats inference efficiency as a first-order design principle. Hardware-
aware kernels, quantization, token streaming, timestep distillation, and runtime optimization are not
only engineering improvements; they determine whether the model can participate in observation–
action–feedback loops. Efficient deployment increases the amount of control-relevant information
that can be processed before action execution, making future regret-aware evaluation and policy
| improvement | more practical. |                 |             |                 |                |
| ----------- | --------------- | --------------- | ----------- | --------------- | -------------- |
| The fifth   | pillar is a     |                 |             | density. Kairos | already builds |
|             | data-centric    | view of control | information |                 |                |
a large-scale data pipeline for data collection, filtering, tagging, captioning, and long-horizon task
annotation. Under the control-sufficient perspective, the goal of this pipeline is not only to process
more videos, but to identify and structure experience that most reduces uncertainty about action
consequences, failure boundaries, contact dynamics, recovery strategies, and safety risks. This
suggests a clear data priority for future Physical AI world modeling: near-boundary failure and
recovery data, near-boundary successful data, contact-rich data, ordinary successful trajectories,
and ordinary observation videos, in descending order of expected control information density. This
principle prioritizes diagnostically useful boundary-region experience rather than treating all failures
10

|     |     |     | RoboTwin 2.0 |     |     |     |     |     |     | LIBERO-plus |     |     |     |
| --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- |
97
92
96.1
|     |     |     | 96.0 |     |     |     |     | 90.8 |     |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
96
90
95
|     | erocS |     | 94.4 |     |     |     |     | erocS |     |     | 88.0 |     |     |
| --- | ----- | --- | ---- | --- | --- | --- | --- | ----- | --- | --- | ---- | --- | --- |
88
94
93.2
|     |     |     |     |     | 93.1 | 93.0 |     |     |     |     |     |      |     |
| --- | --- | --- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | ---- | --- |
|     | 93  |     |     |     |      |      |     | 86  |     |     |     | 85.7 |     |
85.5
84.8
92.2
92
84
Kairos MotuBrain SANTS G0.5 AIM TBot-SA1 LingBot-VA Kairos Being-H0.7 ProGAL-VLA ACoT-VLA Pi-0.5
|     |     | (a) | Performance           |     | comparison | across | world | action | model | benchmarks. |     |     |     |
| --- | --- | --- | --------------------- | --- | ---------- | ------ | ----- | ------ | ----- | ----------- | --- | --- | --- |
|     |     |     | WorldModelBench Robot |     |            |        |       |        |       | DreamGen    |     |     |     |
64
9.4
|     |     | 9.30 |      |     |     |     |     | 61.80 |       |     |     |     |     |
| --- | --- | ---- | ---- | --- | --- | --- | --- | ----- | ----- | --- | --- | --- | --- |
|     |     |      | 9.26 |     |     |     |     | 62    | 61.10 |     |     |     |     |
9.2
60
9.04
|     | erocS | 9.0 |     | 8.96 |     |     |     | erocS 58 |     |     |     |     |     |
| --- | ----- | --- | --- | ---- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
56
8.8
54.00
|     |     |     |     |     |     |     |     | 54  |     | 53.70 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
8.6
|     |     |     |     |     |     | 8.52 |     |     |     |     |     | 51.80 |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | ----- | --- |
52
8.4
50
|     |     | Kairos |     | o * ot-physworld* | Lingbot* | Wan2.2-5B* |     | Kairos | Wan2.2-14B* | GigaWorld-0 | Cosmos3-nano* | Lingbot* |     |
| --- | --- | ------ | --- | ----------------- | -------- | ---------- | --- | ------ | ----------- | ----------- | ------------- | -------- | --- |
Cosmos3-nan
A b
|     |                    | (b)                          | Performance |     | comparison | across | embodied | world              | model                        | benchmarks. |     |     |        |
| --- | ------------------ | ---------------------------- | ----------- | --- | ---------- | ------ | -------- | ------------------ | ---------------------------- | ----------- | --- | --- | ------ |
|     |                    | Inference Time (480p, 16fps) |             |     |            |        |          |                    | Inference Time (720p, 16fps) |             |     |     |        |
|     | Kairos (Ours)      |                              |             |     |            | 183.69 |          | Kairos (Ours)      |                              |             |     |     | 422.54 |
|     | 175 Cosmos 2.5-14B |                              |             |     |            |        |          | 400 Cosmos 2.5-14B |                              |             |     |     |        |
383.10
|          | Cosmos 2.5-2B  |     |     |     |           |               |          | Cosmos 2.5-2B |     |     |     |               |     |
| -------- | -------------- | --- | --- | --- | --------- | ------------- | -------- | ------------- | --- | --- | --- | ------------- | --- |
|          | 150 Wan 2.2 5B |     |     |     |           |               |          | Wan 2.2 5B    |     |     |     |               |     |
|          | 125            |     |     |     |           |               |          | 300           |     |     |     |               |     |
| )s( emiT |                |     |     |     |           | Kairos (Zoom) | )s( emiT |               |     |     |     | Kairos (Zoom) |     |
|          |                |     |     |     | R2=0.9997 |               |          |               |     |     |     | R2=0.9998     |     |
100
200
75
50.96
|     | 50  |     |     |     |     |     |     | 100 |     |     |     |     |       |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
|     | 25  |     |     |     |     |     |     |     |     |     |     |     | 51.59 |
13.57
|     | 0   |     |                  |     |           | 2.54  |            | 0   |     |                  |     |     | 8.95 |
| --- | --- | --- | ---------------- | --- | --------- | ----- | ---------- | --- | --- | ---------------- | --- | --- | ---- |
|     | 5   | 10  | 15               | 20  |           | 25 30 |            | 5   | 10  | 15               | 20  | 25  | 30   |
|     |     |     | Video Length (s) |     |           |       |            |     |     | Video Length (s) |     |     |      |
|     |     |     |                  | (c) | Inference | time  | comparison | per | DiT | step.            |     |     |      |
Figure 3 (a)(b) Kairos achieves competitive performance across embodied world-model and world-action
benchmarks while delivering significant efficiency advantages over baselines. These results provide proxy
evidence for regret-relevant capabilities. (c) Notably, Kairos scales linearly (see the zoom window for DiT
inference time per step), ensuring consistent throughput for long-duration generation.
11

as equally valuable, and provides a more precise criterion for deciding what data should be scaled.
The core contributions of this report are organized around three tightly coupled pillars.
First, we introduce a Native Pre-training Paradigm via Cross-Embodiment Data Cur-
riculum. Kairos learns control-relevant information through a progression from passive physical
observation to intentional human behavior and embodied robot action grounding. This curriculum
addresses the mismatch between broad but ungrounded open-world experience and scarce but
actionable robot interaction. By organizing heterogeneous data by intervention strength, Kairos
moves beyond flat data scaling and provides a principled pathway for learning world knowledge that
can support embodied control.
Second, we introduce a Native Understanding–Generation–Prediction Architecture with
Hybrid Linear Temporal Memory. Rather than framing long-horizon modeling as pure video
continuation, Kairos treats it as the maintenance of a shared world-action state. Understanding
extracts semantic and physical abstractions; generation regularizes physically plausible future
evolution; prediction maps the shared state into future action and visual trajectories. Hybrid Linear
Temporal Attention further maintains this state through local, mid-range, and global pathways,
supporting efficient long-horizon modeling while preserving control-relevant variables.
Third, we introduce a Deployment-Aware System Co-Design that treats practical execution as
a modeling requirement. Kairos integrates runtime optimization, memory efficiency, hardware-aware
execution, quantization, and scalable inference into the world-action model stack. This design moves
Kairos closer to practical observation–action–feedback loops, where future systems can evaluate
imagined rollouts, anticipate failures, filter unsafe actions, and refine policies from real feedback.
These contributions form a single control-sufficient information chain. The Cross-Embodiment Data
Curriculum determines where control-relevant information comes from. The unified architecture
determines how visual, semantic, physical, and action-related information is compressed into a
shared state. Hybrid Linear Temporal Attention determines how that state is maintained over time.
World Prediction and Action DiT determine how the state becomes responsive to alternative actions.
Deployment-AwareCo-Designdetermineswhetherthestatecanbeusedunderrealsystemconstraints.
Together,theymoveKairosfromastaticgenerativemodeltowardadeployableworld-actionsubstrate
for Physical AI.
Results. Extensive evaluations in this report assess Kairos across embodied world-model bench-
marks (WorldModelBench [55], DreamGen Bench [56]), world-action benchmarks (RoboTwin 2.0 [57],
LIBERO-Plus [58]), general world-model benchmarks, long-horizon generation, and inference-
efficiency settings (Figure 3). Using the notation above, these evaluations should be interpreted as
proxy evidence for the components that would enter J or its model-predicted counterpart, rather
H
than as direct estimates of Reg or direct proof of closed-loop regret minimization. Embodied
H
world-model benchmarks assess physical plausibility, instruction grounding, and temporal consistency.
World-action benchmarks assess whether jointly modeling world dynamics and action evolution
improves action prediction and manipulation. Long-horizon generation evaluates whether the model
can preserve state consistency over extended temporal windows. Inference-efficiency experiments
evaluate whether the model moves closer to practical deployment constraints. Together, these results
provide evidence that Kairos learns several capabilities relevant to regret-aware Physical AI: physical
consistency, instruction grounding, joint world-action prediction, long-horizon state maintenance,
and efficient deployment.
Kairos is therefore a step toward control-sufficient world modeling for Physical AI; demonstrating
12

reduced Reg in real robot deployment remains future work. Direct validation of closed-loop regret
H
reduction will require future real-robot experiments that measure the correlation between imagined
and real rollouts, failure prediction before execution, safety filtering effectiveness, recovery learning,
and measurable policy improvement from imagined experience. These future evaluations will be
necessary to determine whether a world-action model can move from proxy capability to real-world
regret reduction. The goal of Kairos is to establish the architectural, data, memory, and deployment
foundation on which such future self-evolving physical agents can be built.
2 Model
Kairosisbuiltaroundthenotionofacontrol-sufficient state. Thisstateisnotintendedtopreserve
all visual details of the future, but to retain the variables required for embodied decision-making:
object state, spatial relation, contact condition, task progress, action consequence, failure risk, and
deployment uncertainty. The unified architecture should therefore be interpreted as a mechanism
for compressing heterogeneous observations and actions into a shared state that is sufficient for
prediction, planning, and future closed-loop evaluation.
The regret formulation in the Introduction defines the target role of this state: Z should preserve
t
the information needed to support low-cost action choices under the horizon-level physical cost
J , while omitting information that does not affect task-relevant outcomes. The model section
H
below specifies how Kairos constructs, regularizes, predicts from, and maintains such a state. This
connection should be understood as a model-side prerequisite for future regret-aware control, not as
a claim that the current system directly proves closed-loop regret minimization.
2.1 Native Architecture with Unified Understanding, Generation, and Prediction
The core architecture of Kairos is built around a single principle: a world model for Physical AI
should not attempt to preserve or generate the entire world, but should learn and maintain a
control-sufficient state. This state should retain the information needed for embodied prediction
and decision-making, including object state, spatial relation, contact condition, task progress, action
consequence, failure boundary, safety risk, and deployment uncertainty. We denote this internal
state as Z , constructed in the current system from the observation–action history H and the task
t t
goal or language instruction g. Z is not a complete copy of the world; it is a compact internal
t
state that should be sufficient for downstream generation, prediction, planning, risk assessment, and
future closed-loop evaluation.
Under this view, the native architecture of Kairos should not be interpreted as a loose connection of
three independent modules. World Understanding, World Generation, and World Prediction are
three interfaces to the same underlying world-action state. World Understanding constructs Z from
t
heterogeneous experience. World Generation turns Z into physically plausible imagined futures,
t
thereby regularizing and probing the state. World Prediction maps Z into joint future state-action
t
trajectories and executable action tokens, thereby turning the model from a passive observer into an
embodied world-action system. These components are coupled through a shared architecture and a
hybrid temporal memory mechanism designed to maintain control-relevant information over long
horizons (Figure 4).
This design departs from the common modular pipeline in which a perception model first produces
semantic features, a video model then generates future frames, and a policy module finally predicts
actions. Suchmodularpipelinescanbeuseful,buttheyoftenproducemismatchedinternalstates: the
13

Figure 4 ModelarchitectureofKairos. Understanding,Generation,andPredictionoperateasthreeinterfaces
to the shared control-sufficient state Z .
t
perception module may preserve semantic information but discard physical variables; the generation
module may synthesize visually plausible futures without preserving task progress; the action module
may learn observation–action correlations without understanding how actions change future states.
Kairos instead aims to maintain semantic, visual, physical, and action-related information in a
shared world-action state.
The purpose of this unified design is to instantiate the model-side component of the regret objective
introduced above: Kairos learns a compressed state Z that is intended to preserve the variables
t
needed for low-cost action selection. Whether this state yields lower closed-loop physical cost than
baseline representations must be validated in future real-robot or high-fidelity simulated experiments.
It gives the model a place to compress control-relevant information, a mechanism to maintain this
information over time, an interface to imagine possible futures, and an action branch that can use
world dynamics without always materializing future video during deployment.
2.1.1 World Understanding: Control-Sufficient State Construction
World Understanding is the entry point through which Kairos converts heterogeneous sensory,
linguistic, physical, and embodied experience into a shared internal state for Physical AI. In
conventional multimodal systems, understanding is often treated as semantic recognition: recognizing
objects, parsing instructions, describing scenes, or aligning images and language. These capabilities
remain necessary, but they are not sufficient for an embodied world model. For a physical agent, the
purpose of understanding is not to describe the world as completely as possible, but to preserve the
subset of information that remains relevant for future control.
Kairos therefore defines World Understanding as control-sufficient state construction. Given an
observation–action history H and a task instruction or goal g, the Understanding module con-
t
structs the shared internal state Z . In the current architecture, Z is realized through structured
t t
multimodal representations: visual observations are represented by visual latent tokens, and task
instructions provide language-conditioned features. This state is intended to preserve task-relevant
semantic variables, physical cues, task-progress information, and uncertainty variables needed by
14

downstream generation, prediction, planning, and future closed-loop evaluation. In this sense, World
Understanding is the first compression stage of the Kairos world-action stack.
From a regret-aware information-compression perspective, the goal is not to maximize the amount
of information stored in Z , but to maximize the amount of control-relevant information preserved
t
per unit of representation size, computation, latency, and risk. In terms of the regret formulation,
the Understanding module should preserve precisely those variables that affect the physical cost c,
including contact conditions, task progress, failure boundaries, safety margins, recovery difficulty,
and imagined–real uncertainty. A robot does not need every visible detail of a scene. It needs to
know which objects matter, where they are, how they can be manipulated, what contact conditions
are likely to occur, how the current state relates to the task goal, and where failure boundaries may
lie. For example, the exact texture of a wall may be irrelevant for a table-top manipulation task,
while a subtle cue about object slippage may determine whether the next grasp succeeds or fails.
This compression objective is inherently task-aware. The same scene may require different un-
derstanding states under different goals. If the instruction is to pick up a cup, the model should
prioritize cup pose, grasp affordance, obstacle layout, and gripper state. If the instruction is to avoid
spilling liquid, it should additionally preserve tilt, fill level, acceleration risk, and stability margin.
If the instruction is to clean a table, it should preserve object categories, reachable regions, task
ordering, and disposal locations. Thus, World Understanding should not simply ask what is in the
scene, but which aspects of the scene matter for the current and future control problem.
Finally, World Understanding should also be history-aware. Many control-relevant cues are not
inferable from a single frame: contact stability depends on recent motion, task progress depends on
earlier subtasks, object permanence depends on memory through occlusion, and failure risk may
depend on delayed effects. In Kairos, the state constructed by World Understanding is maintained
and updated through the temporal modeling mechanisms described in Section 2.2, rather than by
a static frame-level encoder alone. This allows the shared state to carry information about recent
motion, task progress, object persistence, and delayed physical effects for downstream generation
and prediction.
In the current Kairos implementation, the VLM-based Understanding module [59, 60] provides
a practical foundation for instruction grounding and multimodal semantic alignment. It does
not yet establish complete physical understanding; rather, it provides an operational interface
for extracting and conditioning on control-relevant semantic variables and physical cues from the
available multimodal context.
In summary, World Understanding in Kairos should be interpreted as the process of constructing a
control-sufficientstatefromheterogeneousexperience. Itcompressesmultimodalhistoryintovariables
that matter for embodied control, supports multi-timescale state maintenance, and prioritizes high-
density control information. Its success should ultimately be judged not only by visual–language
benchmark performance or instruction-following score, but by whether the resulting state improves
future prediction, failure anticipation, safety assessment, recovery planning, and eventually closed-
loop physical cost relative to baseline states.
2.1.2 World Generation: Control-State Regularization
World Generation is the component through which Kairos imagines possible future observations,
models physically plausible scene evolution, and regularizes the shared world-action state. In many
recent world-model systems, generation is treated as the central objective: the model is judged by
whether it can produce high-fidelity, temporally coherent, and visually impressive future videos.
15

This objective has driven substantial progress in observation-level generative world models, but it
is not sufficient for Physical AI. A robot does not act in order to make future pixels look realistic.
It acts to complete tasks, avoid unsafe states, recover from mistakes, and reduce costly real-world
failures. Therefore, in Kairos, World Generation is not the final purpose of world modeling, but an
auxiliary interface for probing and regularizing a control-sufficient internal state.
Given the shared state Z produced by World Understanding, World Generation predicts future
t
visual observations and tests whether the state preserves physically relevant information. The
generated sequence is not merely a video continuation. It is an operational probe of the shared
world-action state. When used for training or evaluation, future visual prediction can expose whether
the internal state preserves object permanence, temporal continuity, spatial layout, contact-relevant
cues, task progress, and long-horizon causal structure.
At the generation interface, Kairos uses a latent diffusion design for efficient and scalable future-
observation modeling. Visual observations are represented in a compact latent space, and multimodal
conditioning features provide task and context information. A temporally scalable Diffusion Trans-
former [61] performs denoising in latent space under these conditions. This branch supports flexible
generation settings such as text-to-video, image-to-video, and text-image-to-video, while keeping
the role of generation focused on probing and regularizing the shared state rather than defining the
state representation itself.
The first role of World Generation is physical and temporal regularization. When the generation
branch is trained to predict future observations, it encourages the shared state Z to preserve
t
information about motion, object permanence, spatial layout, contact, support, temporal continuity,
task progress, and delayed effects. If the state omits critical physical variables, the generated
future may drift, violate object identity, break contact consistency, ignore task progress, or produce
impossible transitions. In this sense, visual generation acts as a state regularizer rather than a final
evaluation target.
The second role of World Generation is long-horizon state probing. Short-horizon generation can
often succeed by exploiting local appearance smoothness. Long-horizon Physical AI requires more:
persistent object identity, stable spatial relations, consistency through occlusion, delayed contact
effects, and multi-stage task progress. For example, if an object is temporarily occluded, the
generated future should preserve its identity and approximate location rather than treating it as
a new object when it reappears. If a multi-step task requires moving several items in order, the
generated sequence should preserve which items have already been moved and which remain. These
are not merely aesthetic video-quality issues. They are proxies for whether the internal world state
remains useful for control over time.
World Generation is also deployment-aware. Video synthesis can be computationally expensive and
may be unsuitable for real-time decision loops if used naively. Kairos addresses this through latent
diffusion, compact video representation, temporally scalable DiT design, hybrid attention, timestep
distillation, and hardware-aware optimization. The deeper point is not simply speed: in Physical
AI, inference cost determines whether the model can be used before action execution. A generated
future that arrives too late to affect action is not useful for regret-aware control.
At deployment time, Kairos need not always generate full future videos. In many robotic settings,
the prediction branch may use the shared world-action representation to produce future action tokens
directly, while the future video branch is disabled to reduce cost. During training, visual generation
helps the model learn spatiotemporal and physical priors. During deployment, action-only inference
can retain the benefits of those priors without paying the full cost of video synthesis. Thus, World
16

Generation mainly serves as a training-time regularizer and diagnostic interface, while the system
can choose a lighter inference pathway when the control loop requires speed.
The relationship between World Generation, World Understanding, and World Prediction is comple-
mentary. Understanding constructs the shared state; Generation probes and regularizes whether
that state supports physically plausible future evolution; Prediction uses the same state for future
world-action modeling. A better video model does not automatically produce a better policy, but a
generation branch that captures physical dynamics, object interaction, and long-horizon consistency
can provide useful priors for joint world-action prediction. This is why Kairos treats World Gener-
ation as one interface to the shared world-action state rather than as an isolated video synthesis
module.
In summary, World Generation in Kairos should be understood as control-state regularization
rather than merely photorealistic video synthesis. It models future observations under multimodal
conditioning, while regularizing the shared world-action state toward physical plausibility, object
permanence, task consistency, and long-horizon temporal coherence. Its value lies in whether it helps
Kairos preserve and operationalize the information needed for physical decision-making.
2.1.3 World Prediction: Joint World-Action Modeling
World Prediction is the component that extends Kairos from future observation modeling to joint
world-action modeling. Conventional world models primarily ask: given the past, what future
observations are likely to occur? This is useful for forecasting, simulation, and video generation, but
it is insufficient for Physical AI. A robot must also model how future actions and future world states
are coupled under the current task and observation history. A world-action model should therefore
represent future actions not as an external output appended after world modeling, but as part of the
future evolution that the model learns to predict.
Inthenotationoftheregretobjective,WorldPredictionprovidesamodel-sideinterfaceforconnecting
the shared state Z to future physical consequences. Its role is to make action prediction depend on
t
the same state used for physical and temporal world modeling, so that downstream action selection
can be informed by task progress, contact-relevant cues, failure risk, and predicted future dynamics
rather than by visual plausibility alone.
Kairos formulates World Prediction as a unified World-Action Model (WAM). Rather than treating
future actions as an independent policy head detached from world modeling, Kairos couples future
visual dynamics and future action tokens within the same world-action prediction interface. This
design reflects a central assumption of Physical AI: the future state of the world and the future
action of the agent are not independent. The robot does not merely observe the world; it acts within
it. Therefore, action prediction should benefit from the physical priors and temporal dynamics
learned by world modeling.
Let Z be the control-sufficient state constructed by World Understanding and regularized by World
t
Generation. The World Prediction module estimates future action trajectories and, when required,
future visual trajectories from this shared state. Future observations or latent visual states provide
the world-dynamics side of prediction, while future robot action tokens provide the execution side of
prediction. During training, Kairos can jointly optimize future visual evolution and action sequence
generation. During deployment, the model can disable future video generation and generate only
future action tokens, thereby reducing computational cost while retaining the world dynamics learned
from joint training.
17

Architecturally, Kairos implements World Prediction using a Mixture-of-Transformer design with
two tightly coupled components: a Video DiT and an Action DiT. The Video DiT models future
visual tokens and is initialized from the pretrained Kairos World Generation model, allowing it to
inherit spatiotemporal priors, physical regularities, and long-horizon visual dynamics. The Action
DiT predicts future action tokens and follows the same architectural logic while using a smaller scale
for deployment efficiency. The purpose of this design is not simply to attach an action head to a
video model, but to let action prediction benefit from the physical priors learned by world generation.
The input sequence is organized into three token groups:
• History Video Tokens, representing historical visual observations;
• Future Video Tokens, representing future visual states;
• Future Action Tokens, representing future robot actions.
This token organization allows Kairos to jointly model visual dynamics and action prediction while
preserving clear causal constraints.
Inspired by the mixed-attention strategy in [62], Kairos adopts a unified attention masking strategy
for joint video–action modeling. History video tokens attend only to historical tokens, preventing
information leakage from future states and maintaining a stable representation of the observed
past. Future video tokens and future action tokens are both conditioned on the historical visual
context, ensuring that imagined futures and predicted actions are grounded in the same observed
state. Future video tokens use sparse spatiotemporal attention to efficiently capture local visual
dynamics, while future action tokens use broader attention across the action sequence to support
coherent long-horizon action prediction. Importantly, the action branch does not depend on future
video tokens. This creates an asymmetric interaction scheme: video and action are jointly trained,
but future action inference does not require explicit future video synthesis.
This asymmetry is central to the Kairos design. During training, the video objective encourages
the model to learn environmental dynamics, physical consistency, object permanence, and future
state evolution. The action objective encourages the model to learn executable control trajectories
grounded in the same observed context. Joint optimization aligns environmental transitions with
action prediction. During deployment, however, future video synthesis can be skipped when action-
only inference is sufficient. Since action tokens are much fewer than video tokens, this substantially
reduces diffusion and attention computation while preserving the benefits of jointly learned world
dynamics.
From the perspective of world-action prediction, the Action DiT is the action-side interface of the
world model. It uses the shared state to generate future action tokens while benefiting from the
physical and temporal structure learned by the visual branch. The key point is that actions are not
merely labels attached to observations; they are part of the agent’s interaction with the world. By
jointly modeling future visual and action tokens, Kairos moves beyond pure observation prediction
toward a representation that is more suitable for embodied control.
World Prediction also connects to regret-aware modeling. A policy that acts without modeling
consequences can only react to observations. A world-action model can provide a substrate for
evaluating future consequences before execution. In future closed-loop systems, this interface can
support policy evaluation, risk filtering, recovery planning, and imagined rollout ranking. The value
of World Prediction therefore lies not only in action accuracy, but also in its potential to support
lower-cost decisions under physical constraints.
18

The relationship between World Prediction, World Understanding, and World Generation is com-
plementary. Understanding constructs the shared state Z that contains task-relevant information.
t
Generation regularizes this state by modeling physically plausible future observations. Prediction
uses the same state for future action modeling. A better video model does not automatically produce
a better policy, but a generation branch that captures physical dynamics, object interaction, and
long-horizon consistency can provide useful priors for joint world-action prediction. This is why
Kairos should be described as a native world-action stack rather than a VLM plus video model plus
policy head.
World Prediction also reinforces the deployment-aware philosophy of Kairos. In real Physical AI
systems, a world model must produce useful action predictions within the time budget of the
robot’s control loop. A high-fidelity future video that arrives too late to affect action cannot reduce
real-world mistakes. The action-only inference mode directly addresses this constraint. It preserves
the training-time benefits of world simulation while allowing deployment-time inference to avoid
expensive future video materialization.
In summary, World Prediction in Kairos is a world-action prediction interface. It jointly trains video
and action branches to align physical dynamics with executable control, while supporting efficient
action-only inference during deployment. Its role is to establish a model-side prerequisite for future
regret-aware Physical AI. Direct validation of whether predicted futures and action rollouts improve
real closed-loop behavior remains an important direction for future work.
2.2 Efficient Diffusion Transformer with Hybrid Linear Attention
zt
Scale, Shift
SWA / GLA
Gate
+
Multi-Head
Cross-Attention
+
Scale, Shift
Feed-Forward
Network
Gate
+
PLM
t petsemiT
Noised latent t
Sliding-Window
2× Attention
t
Sliding Window Attention Map
1× Dilated SWA
t
M×
Gated Linear
1×
Attention
t
Dilated Sliding Window Attention Map
gniddebmE
dnoC
N×
Figure 5 DiT block architecture of the proposed Hybrid Linear Temporal Attention.
Diffusion Transformers have become powerful backbones for image generation, video generation,
and action prediction. However, standard DiT architectures rely on full Softmax self-attention,
whose quadratic complexity in sequence length becomes prohibitive for long videos and high-
resolution embodied observations. In Physical AI, this problem is not only computational. It is also
representational. Long-horizon world modeling does not simply require longer context; it requires
maintaining the right control-relevant variables across different temporal scales.
19

| Kairos therefore |     | introduces |     | a         | backbone |     | with   |        |          |           | (Fig. | 5). |
| ---------------- | --- | ---------- | --- | --------- | -------- | --- | ------ | ------ | -------- | --------- | ----- | --- |
|                  |     |            |     | LinearDiT |          |     | Hybrid | Linear | Temporal | Attention |       |     |
The goal is not merely to make long-video generation cheaper. The goal is to maintain a control-
sufficient state across local, mid-range, and global timescales. Fast local dynamics include motion
continuity, contact transitions, slip, collision, and hand–eye correction. Mid-range dynamics include
object interaction history, tool use, and subtask transitions. Global dynamics include object
permanence, task progress, delayed physical effects, scene memory, and failure history. These
temporal responsibilities are different and should not be forced into a single attention mechanism.
Kairos factorizes temporal modeling into three complementary pathways: Sliding-Window Attention
(SWA) for local dynamics, Dilated Sliding-Window Attention (DSWA) for mid-range dependencies,
and Gated Linear Attention (GLA) for global causal memory. The resulting backbone is organized
into repeated groups of hybrid blocks that interleave SWA, DSWA, GLA, conditioning layers, and
feed-forward transformations. This design supports efficient local motion modeling, mid-range
interaction aggregation, and persistent global causal memory within a unified DiT architecture.
This factorization should be interpreted as a multi-timescale control-state maintenance mechanism.
SWA handles the local physics that must be updated rapidly. DSWA expands the temporal receptive
field without quadratic cost, allowing intermediate dependencies to be captured. GLA maintains a
persistent global state with linear complexity, allowing supra-window information to influence future
predictions even when it is no longer visible within the local context. Together, these components
allow Kairos to preserve control-relevant information without relying on full dense attention over all
tokens.
2.2.1 Global Pathway: Gated Linear Attention as Persistent Causal Memory
To enable global temporal reasoning with linear complexity, Kairos employs
|     |     |     |     |     |     |     |     |     | Gated | Linear | Attention |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------ | --------- | --- |
(GLA) as the primary mechanism for long-range information propagation. Concretely, GLA is
implemented using GatedDeltaNet [54], a gated linear attention variant closely related to structured
state-space models (SSMs) and to a broader line of efficient and linear-attention architectures [63–74].
Unlike Softmax attention, whose complexity scales quadratically with sequence length, GLA scales
| linearly and | thus | remains |     | efficient | even for | long | video sequences. |     |     |     |     |     |
| ------------ | ---- | ------- | --- | --------- | -------- | ---- | ---------------- | --- | --- | --- | --- | --- |
As illustrated in Fig. 6, the core of the GDN lies in the Delta Update Rule, which addresses
the “key collision” problem found in vanilla linear transformers. Instead of purely additive updates,
GDN learns to remove outdated or less important key–value associations to make room for new
information.
| The computation |     | at  | each | time step | t is defined | as  | follows: |     |     |     |     |     |
| --------------- | --- | --- | ---- | --------- | ------------ | --- | -------- | --- | --- | --- | --- | --- |
1. Feature Extraction. The query q , key k , and value v are projected from the input x .
|     |     |     |     |     | t   |     | t   | t   |     |     |     | t   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Simultaneously, a soft “writing strength” β is computed via a sigmoid gate:
t
|     |     |     | q = | W x , | k = W | x   | , v = W | x , | β = σ(W | x ). |     | (1) |
| --- | --- | --- | --- | ----- | ----- | --- | ------- | --- | ------- | ---- | --- | --- |
|     |     |     | t   | Q t   | t     | K   | t t V   | t   | t       | β t  |     |     |
2. Memory Retrieval and Interpolation. The model retrieves the old value vold using the
t
current key and interpolates it with the current value to generate vnew:
t
|     |     |     |     | vold | = S k | , vnew | = β v +(1−β |     | )vold, |     |     | (2) |
| --- | --- | --- | --- | ---- | ----- | ------ | ----------- | --- | ------ | --- | --- | --- |
|     |     |     |     | t    | t−1   | t      | t t t       |     | t t    |     |     |     |
where Rdv×d denotes a learnable associative memory that stores key–value correlations
|     | S   | ∈   | k   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
t
| over | time. |     |     |     |     |     |     |     |     |     |     |     |
| ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
20

LinLin
|     |     |     |     | LiLnineeaarr |     | Linear |     | Linear |     |
| --- | --- | --- | --- | ------------ | --- | ------ | --- | ------ | --- |
|     |     |     |     | Conv Conv    |     | Conv   |     |        |     |
L2
L2
|     |     |     |     |     |     |     | α β |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | Q K |     | V   |     |     |     |
Gated Delta Rule
Norm
Linear
|     | Figure | 6   | Architecture | of  | the gated | linear attention |     | module (GDN). |     |
| --- | ------ | --- | ------------ | --- | --------- | ---------------- | --- | ------------- | --- |
3. The state matrix is updated by removing the old association and
| Delta State |     | Update. |     |     |     | S   |     |     |     |
| ----------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
t
writing the new one, a process equivalent to a single step of SGD on an online regression loss:
|     |     |     |     | S = | S   | −voldk⊤+vnewk⊤.                        |                              |           | (3) |
| --- | --- | --- | --- | --- | --- | -------------------------------------- | ---------------------------- | --------- | --- |
|     |     |     |     | t   | t−1 | t t                                    | t                            | t         |     |
|     |     |     |     |     |     | (cid:124) (cid:123)(cid:122) (cid:125) | (cid:124) (cid:123)(cid:122) | (cid:125) |     |
|     |     |     |     |     |     | remove                                 | write                        |           |     |
This update can be interpreted as an online delta-rule update that approximates one step of
| gradient | descent | on  |       | ∥2. |     |     |     |     |     |
| -------- | ------- | --- | ----- | --- | --- | --- | --- | --- | --- |
|          |         | ∥v  | t −Sk | t   |     |     |     |     |     |
Gated Delta Update. While the above delta rule corrects key–value associations locally, it does
not explicitly control global forgetting of past information. To improve memory management,
a gating mechanism is introduced to adaptively modulate the contribution of the previous
| state. Specifically, |     | a decay |     | gate α | ∈ (0,1) | is computed | as: |     |     |
| -------------------- | --- | ------- | --- | ------ | ------- | ----------- | --- | --- | --- |
t
|               |        |         |            |     | α     | = σ(W x         | ).  |     | (4) |
| ------------- | ------ | ------- | ---------- | --- | ----- | --------------- | --- | --- | --- |
|               |        |         |            |     | t     | α               | t   |     |     |
| The state     | update | is then | modified   |     | as:   |                 |     |     |     |
|               |        |         |            | S = | α S   | −voldk⊤+vnewk⊤. |     |     | (5) |
|               |        |         |            | t   | t t−1 | t t             | t   | t   |     |
| Equivalently, | this   | can     | be written | as: |       |                 |     |     |     |
|               |        |         |            | S = | α S   | +β (v −vold)k⊤. |     |     | (6) |
|               |        |         |            | t   | t t−1 | t t             | t   | t   |     |
Here, actsasaforgetgatethatgloballyscalesthepreviousmemorystate, enablingthemodel
α
t
to discard outdated information more efficiently. Combined with the local delta correction
term, this gated update provides both precise associative correction and adaptive long-term
| memory | control. |     |     |     |     |     |     |     |     |
| ------ | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
4. Output Generation. The final output is retrieved from the updated memory: o = S q .
t t t
21

In Kairos, GLA plays the role of persistent global causal memory. It propagates information related
to object permanence, task progress, delayed physical effects, scene-level context, and long-range
dependencies across the temporal extent of the video or world-action trajectory. This global pathway
is especially important when a future prediction depends on an event outside the recent local window:
an object temporarily hidden behind another may become relevant later; a prior failed grasp may
change the next action; a delayed instability may only become visible after several seconds. These
are precisely the cases where purely local attention is insufficient. GLA should therefore not be
described merely as a computational shortcut; it is a control-state memory mechanism.
Importantly, GLA serves as the only global attention mechanism in the backbone. All other self-
attention layers are restricted to local temporal neighborhoods. This architectural choice enforces
a clear separation of responsibilities: local attention handles fine-grained motion and interactions,
while GLA is responsible for global temporal consistency and causal structure.
2.2.2 Local and Mid-Range Pathways: Sliding-Window and Dilated Sliding-Window Attention
Sliding Window Attention (SWA). For a sequence of hidden states x ∈ RB×(F·L)×D, where F
is the number of frames and L the number of tokens per frame, SWA restricts attention for query
index i to keys/values within a local window w:
(cid:18) (cid:19)
SWA(Q,K,V)
i
= (cid:88) Softmax Q √iK⊤ j V
j
. (7)
d
w w
j∈[i− ,i+ ]
2 2
The window size is chosen as w = L×window_size to cover a small number of adjacent frames and
their spatial tokens. This local structure is appropriate for fast physical dynamics: motion continuity,
short-range hand–object interaction, immediate contact changes, and local geometric consistency.
Dilated Sliding Window Attention (DSWA). To expand the temporal receptive field without
quadratic cost, Kairos incorporates DSWA, which applies a dilation factor d along the temporal
dimension:
DSWA(Q,K,V) = SWA(rearrange(Q),rearrange(K),rearrange(V)), (8)
where the input is reshaped from (B,F ·L,D) to (B·d, F ·L,D). By interleaving SWA (d = 1) and
d
DSWA (d ∈ {6,12}) blocks, the backbone progressively aggregates information across local and mid-
range timescales: SWA captures frame-adjacent interaction; DSWA captures event-level continuity
and delayed local dependencies; GLA preserves global context. All sliding-window attention blocks
use RoPE-based relative positional encoding to preserve local temporal and spatial geometry, while
global positional and causal information is delegated to the GLA pathway.
Expandability through Modular Hybrid Attention. The architectural decoupling in Kairos
provides a robust foundation for multi-dimensional expansion:
• Interactive World Modeling. The Gated Linear Attention (GLA) state matrix S acts as a
t
compressed latent memory. Action tokens can be injected into the GLA gating mechanism
or the latent state update, enabling low-overhead, latency-aware state updates for future
closed-loop control.
• Long-Horizon Generation. Unlike Softmax-based models constrained by a fixed context
window, the SWA and DSWA components maintain a constant memory footprint per step,
while the GLA compresses historical context. This enables generation through recurrent state
passing, mitigating the memory bottlenecks typical of long-video diffusion.
22

| •           |     |     |              |     | The | modular | block | design | supports cross-modal | integration |     |
| ----------- | --- | --- | ------------ | --- | --- | ------- | ----- | ------ | -------------------- | ----------- | --- |
| Cross-Modal |     |     | Integration. |     |     |         |       |        |                      |             |     |
through additional streams in the hybrid blocks, where local spatial-temporal features are
fused via SWA/DSWA, and global cross-modal alignment is maintained by the GLA pathway.
2.3 Theoretical Scope and Analysis of Hybrid Multi-Scale Temporal Memory
The purpose of the theoretical analysis is to clarify why persistent temporal memory is necessary
for long-horizon world modeling and why a hybrid decomposition into local, mid-range, and global
pathways is a reasonable architectural choice. The analysis should not be read as a universal
guarantee of real-world robotic performance, closed-loop regret reduction, or perfect physical
correctness. Instead, it provides theoretical support for a narrower but important claim:
when future
targets depend on information outside a bounded recent window, purely local temporal mechanisms
are insufficient; under stated assumptions, a hybrid multi-scale memory can bound long-horizon
prediction error in terms of branch-wise approximation error and global-memory perturbation. In
this section we state the core theorems that motivate the design; full proofs appear in Appendix B.
We model the available interaction stream as a discrete-time partially observed
| Problem    | setup.  |     |     |     |     |     |       |     |     |     |     |
| ---------- | ------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
| controlled | process |     |     |     |     |     |       |     |     |     |     |
|            |         |     |     |     |     | {(O | ,A )} | ,   |     |     | (9) |
|            |         |     |     |     |     |     | t t   | t≥1 |     |     |     |
where O ∈ O denotes the observable input available to the model, and A ∈ A denotes the action
t t
| signal that | can | influence | future | evolution. |     | Let   |         |         |     |     |      |
| ----------- | --- | --------- | ------ | ---------- | --- | ----- | ------- | ------- | --- | --- | ---- |
|             |     |           |        |            |     |       | (cid:0) | (cid:1) |     |     | (10) |
|             |     |           |        |            |     | H = σ | O ,     | A       |     |     |      |
|             |     |           |        |            |     | t     | 1:t     | 1:t−1   |     |     |      |
denote the complete information available up to time t, and for t, let
1 ≤ w <
|     |     |     |     |     | (w) | (cid:0) |         |         | (cid:1) |     | (11) |
| --- | --- | --- | --- | --- | --- | ------- | ------- | ------- | ------- | --- | ---- |
|     |     |     |     |     | W   | = σ O   |         | , A     |         |     |      |
|     |     |     |     |     | t   |         | t−w+1:t | t−w:t−1 |         |     |      |
denote the information contained in the recent w-step window. Here, denotes the sigma-field
σ(·)
generatedbytheenclosedrandomvariables, i.e., thecollectionofalleventsorinformationmeasurable
from the corresponding observation–action history. Thus, H and W (w) are information sets rather
|     |     |     |     |     |     |     |     |     | t t |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
than raw tuples of observations and actions. Let Y be a square-integrable future target. In Physical
AI, may represent a future latent-frame coordinate, an object-permanence indicator, a delayed
Y
physical-effect event, a task-progress variable, a failure event, or any other long-horizon functional of
the future world state. For any predictor Z, define the squared prediction risk
|     |     |     |     |     |     |       | E(cid:2) | −Z)2(cid:3) |     |     |      |
| --- | --- | --- | --- | --- | --- | ----- | -------- | ----------- | --- | --- | ---- |
|     |     |     |     |     | R   | (Z) = | (Y       |             | .   |     | (12) |
t
Let R⋆ = inf R (Z) be the optimal risk among predictors that can access the full history,
| full |     | Z∈L2(Ht) | t   |     |     |     |     |     |     |     |     |
| ---- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and let R⋆ be the optimal risk among predictors restricted to the recent
|     | =   | inf        |     | R (Z) |     |     |     |     |     |     |     |
| --- | --- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
|     | w   | Z∈L2(W(w)) |     | t     |     |     |     |     |     |     |     |
setutp
w-step window. This formalizes the difference between a model with persistent history and a
| model restricted |     | to a          | bounded | local    | context. |     |     |     |     |     |     |
| ---------------- | --- | ------------- | ------- | -------- | -------- | --- | --- | --- | --- | --- | --- |
| 2.3.1 Necessity  |     | of Persistent |         | Internal | States   |     |     |     |     |     |     |
The first theoretical observation is that purely local temporal models are fundamentally limited
| when future |     | targets depend |     | on information |     | outside |     | the recent | window. |     |     |
| ----------- | --- | -------------- | --- | -------------- | --- | ------- | --- | ---------- | ------- | --- | --- |
23

(Supra-windowdependenceimpliesthenecessityofpersistentstate). E[Y
| Theorem | 1   |     |     |     |     |     |     |     |     | Let m = | | H ] |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ----- |
|         |     |     |     |     |     |     |     |     |     | t       | t     |
| (w)     |     |     | (w) |     |     |     |     |     |     |         |       |
and m = E[Y | W ]. The excess risk incurred by restricting prediction to the recent window
| t         |           | t        |     |      |           |     |           |                    |                   |     |      |
| --------- | --------- | -------- | --- | ---- | --------- | --- | --------- | ------------------ | ----------------- | --- | ---- |
| satisfies | the exact | identity |     |      |           |     |           |                    |                   |     |      |
|           |           |          |     |      | (cid:104) |     | (cid:105) | (cid:104) (cid:16) | (cid:17)(cid:105) |     |      |
|           |           |          |     |      |           | (w) |           |                    | (w)               |     |      |
|           |           | R⋆       | −R⋆ | =    | E (m −m   |     | )2 = E    | Var m | W          |                   | .   | (13) |
|           |           |          | w   | full | t         | t   |           | t                  | t                 |     |      |
Consequently,
|     |     |     | R⋆  | > R⋆ | ⇐⇒   | m   | is not W | (w) -measurable. |     |     | (14) |
| --- | --- | --- | --- | ---- | ---- | --- | -------- | ---------------- | --- | --- | ---- |
|     |     |     |     | w    | full | t   |          | t                |     |     |      |
That is, the excess risk is strictly positive if and only if the optimal full-history predictor m is not
t
| perfectly | recoverable | from | the | recent | window | W (w) | .   |     |     |     |     |
| --------- | ----------- | ---- | --- | ------ | ------ | ----- | --- | --- | --- | --- | --- |
t
Corollary 1 (Explicit lower bound under recent-window mismatch). Let E denote a recent-window
observation event with P(E) > 0. If an influential past event remains unobservable within E,
producing two distinct future-target expectations µ 1 and µ 2 with conditional probabilities α and 1−α,
then
|     |     |     |     | R⋆ −R⋆ | ≥    | P(E)α(1−α)(µ |     | −µ )2. |     |     | (15) |
| --- | --- | --- | --- | ------ | ---- | ------------ | --- | ------ | --- | --- | ---- |
|     |     |     |     | w      | full |              |     | 1 2    |     |     |      |
Remark 1 (Local smoothness is insufficient for long-horizon consistency). Theorem 1 explains why
local temporal smoothness may remain visually plausible over short horizons but fail over longer
horizons. Once an influential event falls outside the current context window, the model can no
longer condition on the true historical cause; it must average over multiple plausible hidden histories.
The identity of an occluded object, the result of a previous subtask, or the state of a prior contact
interaction may no longer be visible, but may still determine the future. The key point is that
this lower bound is information-theoretic, not an optimization failure: it does not arise because the
model is too small or insufficiently trained, but because the relevant information is absent from the
accessible window. Simply scaling parameters or training compute cannot eliminate the gap when
the architecture lacks a mechanism to preserve supra-window information.
| 2.3.2 | Approximate | Sufficiency |     | of  | Hybrid Multi-Scale |     | Temporal | Memory |     |     |     |
| ----- | ----------- | ----------- | --- | --- | ------------------ | --- | -------- | ------ | --- | --- | --- |
The second theoretical observation concerns the sufficiency of the hybrid design under a structured
assumption. Suppose the Bayes-optimal predictor µ⋆ admits a four-component decomposition
t
|     |     |     |     |     | µ⋆ = Ψ(U⋆, |     | C⋆, D⋆, | G⋆), |     |     | (16) |
| --- | --- | --- | --- | --- | ---------- | --- | ------- | ---- | --- | --- | ---- |
|     |     |     |     |     | t          | t   | t t     | t    |     |     |      |
where U⋆ is a shared predictive representation, C⋆ is a short-range local state corresponding to SWA,
|     | t   |     |     |     |     | t   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
D⋆ is a mid-range dilated state corresponding to DSWA, and G⋆ is a global recurrent causal memory
| t   |     |     |     |     |     |     |     | t   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
corresponding to GLA. Let the learned hybrid predictor µˆ approximate these components with
t
branch-wise approximation error bounded by ε. Suppose further that the global-memory update is
contractive with factor (0,1), and let ξ¯denote the maximum one-step perturbation error in the
ρ ∈
| global-memory | update.      |     |     |             |      |        |             |          |          |       |         |
| ------------- | ------------ | --- | --- | ----------- | ---- | ------ | ----------- | -------- | -------- | ----- | ------- |
|               | (Approximate |     |     | sufficiency | of a | hybrid | multi-scale | temporal | memory). |       |         |
| Theorem       | 2            |     |     |             |      |        |             |          |          | Under | the as- |
sumptions above, the learned hybrid predictor satisfies the asymptotic long-horizon excess-risk bound
|     |     |     |     |      | (cid:18) |     | L ξ¯ | (cid:19)2 |     |     |      |
| --- | --- | --- | --- | ---- | -------- | --- | ---- | --------- | --- | --- | ---- |
|     |     |     |     | )−R⋆ |          |     | G    |           |     |     | (17) |
|     |     |     | R   | (µˆ  | ≤        | Lε  | +    | as t →    | ∞,  |     |      |
|     |     |     |     | t t  | t        |     | 1−ρ  |           |     |     |      |
where L and L are Lipschitz constants associated with the decoder and the global-memory pathway.
G
24

|           | (Exact | sufficiency | in the | realizable | case).         |              |                  |
| --------- | ------ | ----------- | ------ | ---------- | -------------- | ------------ | ---------------- |
| Corollary | 2      |             |        |            | If the learned | hybrid state | exactly recovers |
|           |        |             |        |            | ξ¯=            | µ⋆           | R⋆.              |
the Bayes decomposition at every time step (ε = 0 and 0), then µˆ t = and R t (µˆ t ) =
t t
(Why hybrid multi-scale memory is sufficient). The first term reflects the approxima-
| Remark | 2   |     |     |     |     | Lε  |     |
| ------ | --- | --- | --- | --- | --- | --- | --- |
tion quality of the shared, local, and mid-range branches. The second term L ξ¯/(1−ρ) reflects the
G
asymptotic contribution of global-memory perturbation. Crucially, because the gated delta update
is contractive, the global-memory error does not accumulate arbitrarily but satisfies
1−ρt
ρte (18)
|     |     |     | e t ≤ | 0 + | sup ξ i , |     |     |
| --- | --- | --- | ----- | --- | --------- | --- | --- |
1−ρ
1≤i≤t
yielding ξ¯/(1−ρ) as ∞. This geometric damping ensures that one-step perturbations
|     | e ≤ | t   | →   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
t
are strictly bounded rather than amplified over time. Architecturally, the local and mid-range
branches efficiently capture local appearance changes and intermediate temporal structures, while
GLA selectively propagates the persistent causal state under bounded drift. GLA therefore functions
as a stable information bottleneck: it preserves essential long-range context without accumulating
compounding errors, enabling consistent generation over extended horizons.
| 2.3.3 Interpretation |          | for Kairos |       |               |              |     |     |
| -------------------- | -------- | ---------- | ----- | ------------- | ------------ | --- | --- |
| The theoretical      | analysis | supports   | three | architectural | conclusions. |     |     |
First, persistent memory is unavoidable for long-horizon world modeling whenever relevant
information can fall outside a recent context window. This justifies the need for a recurrent or
persistent state pathway in Kairos. Without such a pathway, long-horizon consistency can fail even
| if short-horizon | visual | quality | remains strong. |     |     |     |     |
| ---------------- | ------ | ------- | --------------- | --- | --- | --- | --- |
Second, separating temporal responsibilities into short-range (SWA), mid-range (DSWA), and
global (GLA) branches is theoretically motivated. Local attention is appropriate for fast motion and
contact dynamics; dilated attention is appropriate for mid-range event dependencies; gated global
memory is appropriate for supra-window causal context. This maps naturally onto the Physical AI
| requirement | of multi-timescale |     | control-state | maintenance. |     |     |     |
| ----------- | ------------------ | --- | ------------- | ------------ | --- | --- | --- |
Third, the theory clarifies the scope. Under the stated assumptions, the proposed factoriza-
tion provides a way to bound long-horizon prediction error in terms of approximation error and
controlled memory perturbation. This is a meaningful theoretical justification for the architec-
ture; complementary real-robot validation is positioned as future work. The full proofs appear in
| Appendix   | B.          |       |             |                 |          |     |     |
| ---------- | ----------- | ----- | ----------- | --------------- | -------- | --- | --- |
| 2.3.4 From | Theoretical | State | Maintenance | to Regret-Aware | Physical | AI  |     |
The connection between this theoretical analysis and the broader goal of Kairos is control-sufficient
state maintenance. A Physical AI system needs to preserve information that affects future action
outcomes. Some of this information is local and fast-changing, such as contact and motion. Some is
mid-range, such as object interaction history and subtask progress. Some is global and persistent,
such as object permanence, delayed effects, accumulated failures, and task-level context. The hybrid
memory structure provides an architectural mechanism for maintaining these different kinds of
information.
From a regret-aware perspective, the purpose of persistent memory is not to remember the past
for its own sake. It is to preserve information that can reduce future costly mistakes. A previous
failure, a hidden object state, a delayed contact effect, or an unfinished subtask may determine
25

whether the next action succeeds or fails. If the model forgets this information, its predictions may
remain visually plausible but become control-irrelevant. Long-horizon state maintenance is therefore
a necessary model-side prerequisite for future closed-loop regret reduction.
In summary, Section 2 establishes the model-side foundation of Kairos. World Understanding
constructs a control-sufficient state. World Generation regularizes and probes that state through
physically plausible future imagination. World Prediction turns the state into a world-action
prediction interface. Hybrid Linear Temporal Attention maintains the state across local, mid-range,
andglobaltemporalscales. Theoreticalanalysisexplainswhypersistentmemoryisnecessaryandwhy
hybrid factorization is well-motivated under stated assumptions. Together, these components define
Kairos as a regret-aware world-action model stack for Physical AI, while leaving direct real-world
closed-loop regret minimization as a future validation objective.
3 Native Pretraining Paradigm for Physical AI
The purpose of native pretraining in Kairos is to provide the information required for constructing a
control-sufficientstateZ . Section2describedhowKairoscompressesheterogeneousobservationsinto
t
Z , regularizes this state through future generation, turns it into a world-action prediction interface,
t
and maintains it through hybrid temporal memory. This section addresses the complementary
question: where does the control-relevant information in Z come from?
t
For Physical AI, pretraining cannot be reduced to scaling generic videos or fine-tuning a pretrained
videogeneratoronasmallrobotdataset. Aworld-actionmodelneedstoacquirebroadphysicalpriors,
intentional task structure, and robot-specific action grounding. These three forms of knowledge are
not equally available in the same data source. Open-world videos are abundant and diverse, but
they mostly capture passive observation. Human-centric behavioral data contains rich intentional
interaction, but it does not directly match robot embodiment. Robot interaction data provides
action–outcome grounding, but it is expensive, narrow, and difficult to scale. A flat mixture of these
data sources is therefore insufficient. It treats fundamentally different intervention regimes as if they
were interchangeable samples.
Kairos adopts a different view. Native pretraining is organized as a curriculum over intervention
strength. The model first learns passive physical regularities from open-world video, then learns
intentional task organization from human-centric behavior, and finally grounds these priors in robot-
specific action trajectories. This progression defines the Cross-Embodiment Data Curriculum
(CEDC). Its goal is not merely to expose the model to more data, but to move the model from
observation–action correlation toward action–outcome causation.
This design is motivated by a central property of Physical AI: deployment is interventional. In
ordinary supervised learning, training and test samples are often assumed to come from similar
distributions. In robotics, this assumption breaks down because the agent’s own actions change the
future data distribution. A robot does not simply observe the world; it intervenes in it. Therefore,
the statistical challenge is not only i.i.d. generalization, but interventional generalization. A model
trained only on passive videos may learn what usually happens next, but not what happens if the
robot acts. A model trained only on narrow robot data may learn action execution in a limited
setting, but not general physical and semantic regularities. CEDC provides a developmental pathway
between these extremes.
We define the three data regimes as
D = D ∪ D ∪ D , (19)
CEDC obs human robot
26

where denotes open-world observational videos, denotes human-centric behavioral and
| D   |     |     |     | D     |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- |
| obs |     |     |     | human |     |     |     |
ego-centric interaction data, and denotes robot interaction data with action, proprioception,
|     |     | D robot |     |     |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- |
tactile, force, or other embodiment-specific signals when available. These regimes can be ordered by
| intervention | strength: |     |     |     |     |     |     |
| ------------ | --------- | --- | --- | --- | --- | --- | --- |
(20)
|     |     | τ(D obs | ) < τ(D human | ) < τ(D | robot ), |     |     |
| --- | --- | ------- | ------------- | ------- | -------- | --- | --- |
where denotes how directly the data expresses an agent’s intervention on the world. Open-world
τ(·)
videos mainly express passive dynamics. Human-centric data expresses intentional intervention.
Robot data expresses embodied intervention with concrete action spaces.
Under this formulation, native pretraining is not simply a data scaling recipe. It is a control-
|             |             | strategy. | The model | first builds | broad physical | priors, then | learns |
| ----------- | ----------- | --------- | --------- | ------------ | -------------- | ------------ | ------ |
| information | acquisition |           |           |              |                |              |        |
task-level intentional structure, and finally aligns these priors with robot actions. This sequence
is designed to produce a world-action state Z that is not merely visually rich, but increasingly
t
control-sufficient.
A second principle is control information density. The value of data for Physical AI should not be
measured only by raw scale. Data is valuable when it reduces uncertainty about action consequences,
failure boundaries, contact dynamics, recovery strategies, and safety risks. Therefore, a small amount
of near-boundary failure, recovery, marginal success, or contact-rich data can be more valuable for
control than a large amount of ordinary successful video. CEDC uses scale where scale is useful,
but it should ultimately be guided by control information density rather than volume alone. In this
report, the current curriculum establishes the main developmental pathway; future iterations can
| further prioritize | high-density | control | data within | each stage. |     |     |     |
| ------------------ | ------------ | ------- | ----------- | ----------- | --- | --- | --- |
The native pretraining pipeline is implemented in three progressive stages:
• Stage I: Physical Pretraining. Trains the Video DiT backbone on large-scale open-world
image and video data to acquire broad spatial–temporal and physical priors.
• Stage II: Embodied Pretraining with Human-centric Data. Adapts the Video DiT
with human-centric and robot-centric visual data, strengthening task structure, instruction
following, multi-view embodiment awareness, and action-relevant visual dynamics without yet
| requiring | full robot | action grounding. |     |     |     |     |     |
| --------- | ---------- | ----------------- | --- | --- | --- | --- | --- |
• Stage III: Regret-Aware World-Action Training. Introduces robot action trajectories
and execution preference pairs with high control information density, then jointly trains the
Action DiT together with the pretrained Video DiT so that visual world dynamics, executable
action prediction, and regret alignment training are connected in a native world-action model.
The pipeline therefore moves from physical priors, to task-structured embodied visual dynamics, to
robot-grounded world-action alignment through regret alignment training.
| 3.1 Native | Pretraining | with Cross-Embodiment |     | Data Curriculum |     |     |     |
| ---------- | ----------- | --------------------- | --- | --------------- | --- | --- | --- |
The Cross-Embodiment Data Curriculum is the structural backbone of Kairos pretraining (Fig. 7).
Its central idea is that different data sources contain different forms of control-relevant information.
Open-world videos (Phase I, on the order of millions of hours of internet-scale clips) provide broad
physical regularities, including object motion, gravity, collision, deformation, fluid motion, human–
object interaction, and scene evolution. (Phase II, on the order of 105 hours of
|     |     |     | Human-centric | data |     |     |     |
| --- | --- | --- | ------------- | ---- | --- | --- | --- |
human behavioral and ego-centric data) provides intentional behavior, including task organization,
tool use, object manipulation, recovery behavior, and multi-step procedural structure. Robot data
27

Cross-Embodiment Data Curriculum for Native Pretraining
|     | Learn the mechanical characteristics of   | Robot Actions |     |     |            |     |     |
| --- | ----------------------------------------- | ------------- | --- | --- | ---------- | --- | --- |
|     | robot bodies and interaction data during  |               |     |     | Robot Data |     |     |
real physical environment operation
Human actions, intentions, goals, and
|     | interaction behaviors with external  | Human Behaviors |     |     | Structured Data |     |     |
| --- | ------------------------------------ | --------------- | --- | --- | --------------- | --- | --- |
objects in specific environments
Reasoning：
An apple is pulled downward by gravity, while
its stem provides an upward tensile force to
The foundation of understanding and cognition:  maintain equilibrium
|     |     | Physical Laws |     |     | Chain-of-Thought Text | As the fruit ripens, the stem weakens. When  g r a vit y   e x c e e d s  i t s  l o a | d -b e a ri n g   l i m i t ,   th e   |
| --- | --- | ------------- | --- | --- | --------------------- | -------------------------------------------------------------------------------------- | -------------------------------------- |
describing the basic operating mechanisms and  st e m   b r e a k s  a n d   r e a c h e s  th e   c ri t i c a l   f a il u re
|     | causal laws of nature |     |     |     |     | point |     |
| --- | --------------------- | --- | --- | --- | --- | ----- | --- |
Once detached, the apple is only acted upon  by gravity and accelerates downward in
accordance with Newton’s Second Law
Figure 7 Cross-Embodiment Data Curriculum. A flat mixture obscures the differences between passive
observation, intentional behavior, and embodied action; CEDC treats these regimes as a developmental
| pathway over | intervention | strength. |     |     |     |     |     |
| ------------ | ------------ | --------- | --- | --- | --- | --- | --- |
(Phase III, including embodiment-specific interaction datasets such as AgiBotWorld-Beta [75] and
Droid [76]) provides embodiment-specific grounding, including action tokens, proprioception, gripper
state, tactile or force cues, actuation constraints, execution errors, and sensorimotor feedback.
A flat data mixture would obscure these differences. It may improve visual diversity but fail to
create a coherent transition from observation to intervention. CEDC instead treats the data sources
as a developmental pathway D → D → D . This progression has three functions. First,
|     |     | obs | human | robot |     |     |     |
| --- | --- | --- | ----- | ----- | --- | --- | --- |
it allows the model to acquire broad physical priors before being exposed to narrow robot-specific
distributions. Second, it allows the model to learn intentional task structure from human behavior
before mapping behavior to robot embodiment. Third, it allows robot data to ground the previously
learned priors in concrete action spaces, reducing the gap between visual forecasting and physical
execution.
The curriculum can also be understood as a staged approximation to control-sufficient state learning.
In Stage I, the model learns a state useful for predicting passive physical evolution. In Stage II, the
state becomes more task-, instruction-, and embodiment-sensitive at the visual level. In Stage III,
the state becomes robot-action-aware and is further shaped by regret-relevant execution preferences.
The final objective is not to make the model remember all details of every training video, but to
make Z preserve variables relevant to control: object state, contact condition, task progress, action
t
| consequence, | and failure | risk. |     |     |     |     |     |
| ------------ | ----------- | ----- | --- | --- | --- | --- | --- |
This formulation also explains why native pretraining is preferable to simple downstream fine-tuning.
If a generic video generator is trained only to synthesize visually plausible futures, then later robot
fine-tuningmustretrofitembodimentgroundingontoarepresentationthatmaynotpreservetheright
control variables. In contrast, Kairos exposes the model to physical regularities, intentional behavior,
and robot actions within a unified developmental process; the pretraining process is designed to
establish the model-side prerequisites for future regret-aware Physical AI.
|             |        |              |           | To operationalize | CEDC | within the | Mixture-of- |
| ----------- | ------ | ------------ | --------- | ----------------- | ---- | ---------- | ----------- |
| Multi-Stage | Native | Pre-training | Pipeline. |                   |      |            |             |
Transformers (MoT) architecture (Section 2.1.3), the native pretraining pipeline is systematically
structured as three progressive stages, each dominated by its corresponding data layer. This
28

multi-stage optimization decouples broad physical prior learning from later robot action grounding,
improving both scaling efficiency and control fidelity. Specifically, Stage I (Physical Pretraining)
and Stage II (Embodied Pretraining with Human-centric Data) focus on optimizing the Video DiT
component. In these phases, the model internalizes open-world physical dynamics, task structure,
instruction-conditioned behavior, and embodiment-aware visual dynamics through dense video
forecasting tokens, optimizing the unified spatial–temporal representation without low-level action-
space interference. Transitioning to Stage III (Regret-Aware World-Action Training), the training
emphasis shifts toward joint optimization of the Action DiT alongside the pretrained Video DiT,
together with cost-sensitive execution preference supervision from robot experience with high control
information density. By injecting low-level robot trajectories, robot-state signals, and regret-relevant
execution comparisons, Stage III aligns visual forecasting with executable action prediction within
| the same | world-action | stack. |     |     |     |     |     |     |
| -------- | ------------ | ------ | --- | --- | --- | --- | --- | --- |
Across stages, Kairos adopts Flow Matching [77, 78] as the primary generative
| Training | Objective. |     |     |     |     |     |     |     |
| -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
training objective. Flow Matching provides a continuous-time formulation for learning a conditional
velocity field that transports samples from a simple prior distribution to the data distribution in
latent space. This objective is suitable for large-scale image and video generation, while also being
extensible to robot action trajectories in Stage III. Let denote a clean latent video sample
|     |     |     |     |     |     | z 0 = | E(x) |     |
| --- | --- | --- | --- | --- | --- | ----- | ---- | --- |
produced by the video VAE encoder, and let c denote conditioning inputs (text, image, instruction,
camera control, robot state, or other multimodal conditions). Sample Gaussian noise ϵ ∼ N(0,I)
with the same shape as , and define a continuous interpolation [0,1]. Under the rectified-flow
|                   |     | z 0   |           |     |        |      | t ∈ |      |
| ----------------- | --- | ----- | --------- | --- | ------ | ---- | --- | ---- |
| parameterization, | the | noisy | latent is |     |        |      |     |      |
|                   |     |       |           | z = | (1−t)z | +tϵ, |     | (21) |
|                   |     |       |           | t   |        | 0    |     |      |
so that z continuously interpolates from a clean sample at t = 0 to pure noise at t = 1. The
t
| ground-truth | velocity | along | this path | is  |     |     |     |     |
| ------------ | -------- | ----- | --------- | --- | --- | --- | --- | --- |
(22)
|               |               |     |          |           | u = ϵ−z | .          |     |     |
| ------------- | ------------- | --- | -------- | --------- | ------- | ---------- | --- | --- |
|               |               |     |          |           | t       | 0          |     |     |
| Kairos trains | a conditional |     | velocity | predictor | by      | minimizing |     |     |
v
θ
|     |     |     |     |     | (cid:104)(cid:13) |     | (cid:105) |     |
| --- | --- | --- | --- | --- | ----------------- | --- | --------- | --- |
(cid:13) 2
|     |     |     | L   | = E      | (cid:13)v | (z ,t,c)−u | (cid:13) . | (23) |
| --- | --- | --- | --- | -------- | --------- | ---------- | ---------- | ---- |
|     |     |     | FM  | t,z0,ϵ,c | θ         | t          | t 2        |      |
This objective is shared across conditioning modes. In Stage I, c may include text, image, or
unconditional generation conditions. In Stage II, c increasingly includes task instructions, human-
centric behavior context, robot-centric visual context, and multi-view conditions. In Stage III,
c
includes robot states and action-related signals, and the same Flow-Matching principle is extended
| to action | trajectories. |     |     |     |     |     |     |     |
| --------- | ------------- | --- | --- | --- | --- | --- | --- | --- |
From the control-sufficient perspective, the Flow-Matching objective should be interpreted carefully.
It does not directly optimize regret. It provides a scalable learning objective through which the
model can acquire physical, semantic, temporal, and action-related priors. The regret-aware aspect
comes from how the data, conditioning, temporal structure, and action grounding are organized
| around control-relevant |             | variables.  |     |     |     |     |     |     |
| ----------------------- | ----------- | ----------- | --- | --- | --- | --- | --- | --- |
| 3.2 Stage               | I: Physical | Pretraining |     |     |     |     |     |     |
Stage I establishes the passive physical foundation of Kairos. Its purpose is to train the Video DiT
backbone to model broad spatial–temporal regularities from large-scale open-world video and image
29

1.0
0.8
0.6
0.4
0.2
0.0
0.0 0.2 0.4 0.6 0.8 1.0
Base schedule (0)
eludehcs
detfihS
s (0)
= ; s=exp(f(L)) F
1+(s 1) (0)
No shift
s=1.6 (Image Pretraining)
s=9.1 (Image-video Mixed Pretraining)
s=14.1 (Post-training)
Figure 8 Shape-aware exponential timestep shifting curves in Kairos across training stages. This
figure shows the σ-domain remapping of the Kairos scheduler for three representative training stages, which
will be introduced in the following sections. As the resolution becomes higher and the video becomes longer,
the effective shift strength s increases, resulting in a stronger upward remapping of the timestep schedule.
data. At this stage, the model is not yet expected to understand robot embodiment or produce
executable actions. It functions primarily as a physical observer: it learns how scenes evolve, how
objects move, how interactions unfold, and how visual dynamics remain coherent across time.
The key role of Stage I is to build broad physical priors: motion continuity, object permanence,
gravity-consistent movement, collision patterns, support relations, deformation, fluid-like motion,
camera motion, and temporal coherence. These priors are not yet sufficient for action grounding,
but they provide the world-dynamics substrate that later stages can reuse. Without such priors,
robot data alone would be too narrow to support generalization across scenes, objects, and tasks.
Stage I relies on two core strategies:
• Web-Scale Physical Prior Injection. Open-world images and videos expose the model to a
wide variety of physical phenomena. This data helps the model learn the statistical structure
of the visual world and the broad regularities of natural temporal evolution. The model learns
broad physical priors useful for future world generation and joint world-action prediction.
• Progressive Training Strategy. Trainingbeginswithspatial–semanticpretrainingonimages
and then gradually moves toward video sequences with increasing resolution and temporal
length. Thisprogressionreducesoptimizationdifficultyandallowsthemodeltoestablishstrong
spatial representations before learning long-horizon temporal dynamics. In practical terms,
Stage I proceeds through image pretraining, image–video mixed pretraining, continual video
pretraining, domain-specific supervised fine-tuning or model merging, and preference-based
refinement where applicable.
A representative training progression is summarized in Table 1.
This workflow is structured into three key phases of progressive physical pretraining:
30

Task Type Stage Resolution Maximum Frames
T2I / N2I Image Pretraining 256P 1
T2V / TI2V / I2V / N2V Video Pretraining 256P 81
T2V / TI2V / I2V / N2V Video Pretraining 480P 81
T2V / TI2V / I2V / N2V Video Pretraining 720P 81
T2V / TI2V / I2V / N2V Continual Training 720P 241
T2V / TI2V / I2V / N2V Domain SFT / Merging 720P 241
T2V / TI2V / I2V / N2V Preference / RL Refinement 720P 241
Table 1 Representative Stage I training progression. T2I: text-to-image; N2I: unconditional image; T2V,
TI2V, I2V, N2V: video counterparts. Image tasks are special cases of video tasks with one frame.
• ImagePretraining. InitialT2Ipretrainingestablishesrobustspatial–semanticpriors,allowing
the model to focus exclusively on temporal consistency and motion dynamics in subsequent
stages. To optimize computational efficiency, this foundational phase is conducted at a reduced
resolution of 256P, facilitating rapid convergence of core visual features.
• Image–Video Mixed Pretraining. We initiate video training using a progressive resolution
strategy, scaling from 256P to 720P to optimize computational efficiency. To maintain spatial
fidelity, we incorporate a small fraction of image data (at a 10% sampling ratio) into the
pipeline. By jointly training on both static images and video sequences, the model effectively
bridges the gap between spatial structures and motion dynamics, fostering temporal coherence
while preventing the catastrophic forgetting of high-quality spatial details.
• Continual Pretraining. The model undergoes continued pretraining on a meticulously
curated, high-quality dataset to refine its aesthetic appeal and capture more nuanced, long-
range temporal dependencies for superior video generation. A key advancement in this phase is
extending the maximum temporal length of training sequences from 81 to 241 frames, enabling
the model to directly synthesize high-fidelity videos of up to 15 seconds.
This progression has a control-sufficient interpretation. Image pretraining gives the model spatial–
semantic priors. Image–video mixed pretraining connects spatial structure with motion dynamics.
Continual long-video pretraining improves temporal state maintenance. Domain-specific fine-tuning
introduces higher-density physical or embodied scenarios. Preference or DPO-like refinement can
be used to improve human preference, physical plausibility, and instruction following. The overall
purpose is to make the Video DiT backbone a stronger state regularizer for Z .
t
Stage I also benefits from structured textual supervision. Ordinary captions describe visible content,
butphysicalworldmodelingrequiresmore. Physics-centriccaptionsandchain-of-thoughtannotations
canexposemotiontrajectories,causaltransitions,collisions,force-likeeffects,gravity-relatedbehavior,
object permanence, and failure-like events. They do not make the model a perfect physics engine,
but they provide weak supervision for organizing physical variables in latent space.
Timestep Scheduler Distribution Shift. The effective timestep distribution induced by a fixed
scheduler changes with latent spatiotemporal shape: longer videos and higher resolutions create
different denoising difficulties than short clips or low-resolution videos. Kairos therefore applies a
shape-aware timestep distribution shift [79–82] to the scheduler-defined σ sequence, as visualized
in Figure 8. Formally, let {σ (0) }N denote a base schedule before shifting, where σ (0) ∈ (0,1) is
i i=1 i
31

| monotonically |     | ordered. | The | default | exponential |     | shift | is  |     |     |     |
| ------------- | --- | -------- | --- | ------- | ----------- | --- | ----- | --- | --- | --- | --- |
(0)
sσ
|     |     |     |     |     | σ˜ = |     | i   | ,   |     |     | (24) |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | ---- |
i
|     |     |     |     |     |     | 1+(s−1)σ |     | (0) |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
i
where s controls the shift strength. An equivalent form in logit space is
|     |     |     |     |      |         | (cid:16) | (cid:16) | (cid:17) (cid:17) |     |     |      |
| --- | --- | --- | --- | ---- | ------- | -------- | -------- | ----------------- | --- | --- | ---- |
|     |     |     |     | σ˜ = | sigmoid | logit    | σ (0)    | +logs             | ,   |     | (25) |
|     |     |     |     | i    |         |          | i        |                   |     |     |      |
which makes the monotonicity of the transformation explicit and preserves the boundary behavior
of the schedule. For adaptive support of varying video lengths and resolutions in a unified model,
Kairos uses a shape-dependent rule for s. With the number of latent frames and the
|        |     |               |     |        |        |     | F   |     |     | L = H ×W |     |
| ------ | --- | ------------- | --- | ------ | ------ | --- | --- | --- | --- | -------- | --- |
| number | of  | latent tokens | per | frame, | we set |     |     |     |     |          |     |
√
(26)
|     |     |     |     |     | s = | exp(f(L)) |     | F,  |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- |
where f(L) = mL+b linearly maps L ∈ [L ,L ] to a predefined range [r ,r ], with
|     |     |     |     |     |     | min | max |     | min | max |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
r −r
|     |     |     |     |     | max | min |     |             |       |     | (27) |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | --- | ---- |
|     |     |     |     | m = |     | ,   | b   | = r min −mL | min . |     |      |
L −L
|     |     |     |     |     | max | min |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
This design increases the effective shift for larger latent spatial token counts and longer videos,
thereby reallocating scheduler steps toward trajectory regions that are more sensitive to prediction
error.
Throughout the pretraining phase, we consistently employ the AdamW optimizer [83] with phase-
specific hyperparameter configurations. Specifically, the learning rate is set to 5×10−5 for image
pretraining and is then progressively decayed to 4×10−5, 3×10−5, 2×10−5, and across
1×10−5
the successive image–video mixed pretraining (256P, 480P, 720P) and continual pretraining stages.
Weight decay is configured at 10−3 during the image and 256P mixed pretraining stages, and is
deactivated (set to 0) for all subsequent high-resolution and continual phases.
In addition, we implement delicate finetuning techniques to further boost the performance of physical
alignment, which consist of three phases: domain-specific supervised fine-tuning (SFT), model
| merging, | and             | reinforcement |     | learning. |       |          |     |              |              |          |      |
| -------- | --------------- | ------------- | --- | --------- | ----- | -------- | --- | ------------ | ------------ | -------- | ---- |
|          | •               |               |     |           |       |          |     | We partition | high-quality | datasets | into |
|          | Domain-specific |               | SFT | and       | Model | Merging. |     |              |              |          |      |
domains and train domain-specific models independently. To fully leverage the strengths of
individual models, we employ a model merging strategy to integrate their features [84, 85],
exploring multiple merging approaches including Model Soup [86], CART [87], TIES [88],
DARE [89], and WUDI-Merging [90]. By analyzing the performance of merged models on
carefully constructed evaluation subsets, we select the configuration that achieves the most
|     | balanced | performance |     | across | all domains. |     |     |     |     |     |     |
| --- | -------- | ----------- | --- | ------ | ------------ | --- | --- | --- | --- | --- | --- |
• Finally, we apply Direct Preference Optimization (DPO) [91–
|     | Reinforcement |     | Learning. |     |     |     |     |     |     |     |     |
| --- | ------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
93] to align model outputs with human preferences and physical plausibility. The DPO
preference pairs are constructed by generating video candidates from multiple generative
models conditioned on identical prompts; the highest- and lowest-scoring samples form (chosen,
reject) pairs, which are then used to fine-tune the model following the DPO objective.
For this stage, the AdamW optimizer is retained, with learning rates tailored to for SFT
1×10−5
and 1×10−6 for RL. To maintain training stability, weight decay is uniformly set to throughout
0
| the | entire | process. |     |     |     |     |     |     |     |     |     |
| --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
32

From the CEDC perspective, Stage I mainly learns passive world evolution and broad physical
common sense. Direct knowledge of how a robot’s own actions change the world is built on top in
Stages II and III, with Stage I providing the broad Video DiT foundation.
3.3 Stage II: Embodied Pretraining with Human-centric Data
Stage II moves the curriculum from passive physical observation to intentional behavior. Open-world
videos expose how the world changes, but they often do not reveal task goals, action intent, or
structured manipulation. Human-centric data provides this missing layer: goal-directed actions, tool
use, object manipulation, task ordering, recovery behavior, and long-horizon procedural structure.
These signals are crucial for Physical AI because many robotic tasks are not just physical transitions;
they are intentional sequences organized around goals.
The objective of Stage II is to make the Video DiT backbone task-sensitive and instruction-aware
before full robot action grounding. This phase bridges the gap between passive observation and
active robotic execution through two primary paradigms:
• Task-Structured Semantic Injection. By leveraging large-scale, human-centric behavioral
datasets (e.g., intentional actions, tool manipulation, and everyday chores), the model transi-
tions from unconditioned video generation to task-structured video forecasting, internalizing
high-level behavioral semantics and task taxonomies.
• Video DiT Optimization for Behavioral Causality. The training execution remains
focused exclusively on the Video DiT component. By predicting intentional human movements
and scene state transitions, Video DiT learns to construct a robust causal representation of
goal-directed actions and their environmental consequences, without yet binding to a specific
robotic action space.
This stage does not yet solve robot control. Instead, it provides transferable action-relevant priors
that can later support Action DiT training.
Stage II uses human-centric data from first-person and third-person perspectives. First-person data
is especially valuable because it captures hand–object interaction from an embodied viewpoint,
making it closer to robot observation. Third-person data provides richer context about whole-body
actions, object relations, and task-level structure. Robot-centric visual data can also be included
in this stage to expose the model to diverse embodiments and camera viewpoints, even if low-level
action grounding is deferred to Stage III.
A central feature of Stage II is the evolution of textual supervision. Early training benefits from
detailed captions that describe objects, motions, contact, temporal events, and scene changes. As
training progresses, the supervision shifts toward instruction-style captions that express task intent
more abstractly. The model therefore moves from “what is happening in the video?” toward “what
task is being carried out, and what future state should follow?”.
The Stage II training protocol is divided into three progressive sub-stages, each with distinct focus:
• Human-centric Pretraining. Mixedtrainingonhuman-centricandrobot-centricvisualdata.
Human data provides task-structured semantic priors and intentional behavior patterns; robot
visual data exposes the model to embodiment-specific appearances and physical configurations.
Variable-length clips (3–15 s) expose both short interactions and longer task segments.
• Robot-Centric Training. Increases the proportion of high-quality robot-centric video clips.
33

Caption sampling gradually shifts from fully detail-oriented captions toward a mixture of
detail-oriented and instruction-style captions, improving instruction following while preserving
physical grounding.
• Target-Embodiment Fine-Tuning. For downstream platforms or specific robot embodi-
ments,themodelcanbefine-tunedontarget-embodimentdata. Formulti-cameraembodiments,
multi-view video generation jointly models synchronized observations across viewpoints.
Stage II has an important control-sufficient interpretation: it increases the amount of task-relevant
information contained in Z . After Stage I, the model may know how objects move. After Stage
t
II, it should better know why objects are moved, what task structure constrains the sequence, and
which future states are consistent with an instruction. Human-centric data also provides a scalable
source of intentional behavior that can complement scarce robot demonstrations: it cannot replace
robot data, because human and robot morphologies differ, but it can provide transferable priors
about tool use, object manipulation, task decomposition, and recovery behavior that are especially
valuable when later grounded through robot trajectories. Figure 9 shows representative samples
generated by Kairos after Stage II, illustrating cross-embodiment generalization across single-arm,
dual-arm, dexterous, and humanoid platforms.
Throughout Stage II we uniformly use the AdamW optimizer with weight decay set to 0 to preserve
the general capabilities acquired in Stage I. The learning rate is dynamically decayed across sub-
stages: 1×10−5 for Human-centric Pretraining, 5×10−6 for Robot-Centric Training, and 1×10−6 for
Target-Embodiment Fine-Tuning.
The limitation of Stage II should also be made clear. Human behavior does not directly specify robot
actuation: a human hand grasping a tool does not map one-to-one onto a robot gripper, dexterous
hand, or humanoid actuator. Stage II should therefore not be claimed as final action grounding. Its
role is to prepare the Video DiT backbone with intentional, instruction-conditioned, task-structured
world dynamics, so that Stage III can align these priors with actual robot actions.
3.4 Stage III: Regret-Aware World-Action Training
Stages I and II build the foundation of Kairos by equipping the Video DiT backbone with broad phys-
ical priors and instruction-conditioned task semantics. As the final stage of the Cross-Embodiment
Data Curriculum, Stage III introduces robot interaction data to connect these priors and task
semantics with executable robot actions, execution outcomes, safety risks, and recovery costs. This
stage performs regret-aware alignment between world prediction and embodied action: the goal is
not only to predict plausible futures, but to use regret-relevant preference supervision from execution
outcomes to shape the shared world-action representation toward futures that are safer, more stable,
more recoverable, and more consistent with logged robot execution.
This regret-aware alignment is implemented through two coupled components. The first component,
regret alignment training, converts robot experience with high control information density into
execution preference supervision. Failures, recoveries, unsafe contacts, unstable executions, and
prediction–observation mismatches are used as contrastive signals for identifying which futures are
physically more costly and which variables should be preserved by the shared state. The second
component, joint world-action training, trains the Action DiT alongside the pretrained Video DiT so
that visual forecasting and executable action prediction are aligned in a native World-Action Model.
This coupling ensures that regret-relevant preference supervision acts on the same representation
used for future action prediction, rather than remaining only a visual or language-level adjustment.
34

Figure 9 Samples generated by Kairos after Stage II. Kairos exhibits cross-embodiment generalization across
single-arm, dual-arm, dexterous hands, and humanoids—a behavior consistent with the goal of building
a unified “brain for multi-embodiment and multi-tasking” that allows world knowledge to transfer across
physical configurations.
35

3.4.1 Regret Alignment Training
Regret Alignment Training operationalizes regret-aware alignment by turning robot experience with
high control information density into preference supervision. In the regret-aware formulation, the
physical cost J provides a lens for identifying execution segments that are especially informative
H
for embodied execution, including task failure, collision, unsafe contact, slippage, recovery effort,
hardware damage, and human intervention. These segments reveal where physical cost can rise,
where the margin between success and failure is thin, and where the shared world-action state should
preserve more control-relevant structure.
Kairos therefore mines failures, recoveries, contact-rich events, near-unsafe interactions, boundary
cases, and mismatches between model-predicted rollouts and logged robot executions from D .
robot
Rather than treating these segments as ordinary samples, Kairos uses them to construct execution
preference pairs within matched task contexts.
The preference labels are derived from criteria intrinsic to embodied execution, including task
completion, physical plausibility, stable contact, safety margin, recovery quality, and agreement
with logged robot outcomes. Given the same task context, low-cost execution outcomes with safer
interaction, more stable contact, better recoverability, higher execution fidelity, or smaller prediction–
observation discrepancy are preferred over high-cost outcomes that exhibit failure, unsafe contact,
unstable execution, or large mismatch. In this way, failures and boundary cases are not simply
filtered out as bad data; they become contrastive evidence about which futures are more physically
costly.
These preferences turn robot experience with high control information density into contrastive
supervision for the shared world-action representation. They emphasize variables that are important
for future physical cost, such as contact stability, safety margin, task progress, recoverability, and
agreement between imagined and logged outcomes.
Given these preference pairs, Kairos uses a DPO-style pairwise objective to align the world-action
modelwithregret-relevantexecutionpreferences. Thepreferredsampleisnotdefinedbygenericvisual
quality or aesthetic realism, but by embodied criteria such as task completion, physical plausibility,
stable contact, safety, recoverability, and consistency between imagined and real rollouts. This turns
the constructed preference pairs into a training signal for the shared world-action representation,
preparing it for subsequent joint world-action training.
3.4.2 Joint World-Action Training
The second component grounds the preference-aligned representation in executable robot action. The
pretrained Video DiT retains macro-level physical priors and coarse task semantics from previous
stages, but it still needs robot-specific grounding for contact-rich, high-frequency control phenomena
such as small slip boundaries, end-effector corrections, and force–torque-sensitive interactions.
Stage III therefore trains the multi-stage Mixture-of-Transformers (MoT) stack [62] by introducing
temporally aligned robot action trajectories through the Action DiT while adapting the Video DiT
for active world-action prediction. The robot’s action is no longer treated merely as an external
label or a downstream policy output; it becomes part of the modeled future trajectory.
During training, video frame sequences and action chunk sequences are strictly aligned in the
temporal dimension so that both branches observe corresponding segments of the same trajectory.
Both the Video DiT and the Action DiT are trained using flow matching objectives. The joint
36

training loss is
L = L +λL , (28)
joint video action
where L regularizes future visual evolution and physical consistency, L trains future action
video action
prediction, and λ balances the two.
To improve training efficiency, the Action DiT is initialized by interpolating the pretrained Video
DiT weights and uses a fixed timestep shift during training, unlike the dynamic exponential shift
used by the Video DiT that scales with latent token count. The Video DiT models high-dimensional
spatiotemporal latents with varying sequence lengths, whereas the Action DiT operates on a low-
dimensional and nearly fixed-length action space; a fixed shift is sufficient for stable optimization in
the latter.
Joint training also supports the counterfactual interface introduced in Section 2.1.3: given the same
Z , different future action candidates should correspond to different predicted outcomes. Stage III
t
establishes the architectural and data-alignment basis for such counterfactual world-action modeling
by coupling visual evolution and action prediction within the same trajectory state. By connecting
execution preference pairs with the same shared state used for action prediction, joint world-action
training reduces the risk that preference alignment only adjusts visual plausibility or language-level
task consistency.
3.5 Training Infrastructure for Control-Sufficient Pretraining
The training infrastructure of Kairos is part of the native pretraining paradigm, not merely an
implementation detail. A control-sufficient world-action model must be trained on long videos, high
spatial resolutions, heterogeneous data sources, and multi-branch architectures involving Video DiT,
Action DiT, hybrid temporal attention, multimodal conditioning, and potentially multi-view or
robot-state inputs. Without a scalable training system, the model cannot acquire the breadth of
physical priors or the depth of action grounding required by Physical AI.
Standard video generation models with full spatial–temporal attention—such as Wan2.2 [82], Hun-
yuan1.5 [34], and Cosmos 2.5 [3]—often rely on parallel partitioning strategies such as Ulysses [94]
or RingAttention [95] to reduce training memory and communication cost. The Kairos architecture,
however, exhibits more complex computational dependency characteristics:
• Linear Attention mechanisms impose stringent sequential dependencies on computation order;
• Dilated local attention does not depend on the complete set of global tokens.
Direct application of standard parallelization strategies such as Context Parallel, Ulysses, or RingAt-
tention to this architecture introduces significant performance degradation due to unnecessary token
broadcasting, redundant computation, and substantial communication overhead.
Kairos therefore adopts an operator-level parallel training strategy:
• Operator-level customization. Sliding-window attention benefits from local sequence
partitioning. Dilated attention requires careful rearrangement to preserve mid-range receptive
fields. Gated Linear Attention requires sequential or recurrent state handling. Feed-forward
and projection layers benefit from tensor parallelism.
• Operator fusion and communication optimization. Hybrid temporal attention can
create communication bottlenecks if intermediate activations are repeatedly moved across
37

devices. Kairos reduces overhead by fusing compatible operators, reordering execution where
possible, and minimizing unnecessary token broadcasting.
• Adaptive parallelism. The optimal partitioning strategy changes across stages. Stage I may
emphasize large-scale video sequences and high-resolution latent tokens. Stage II may include
multi-view or instruction-conditioned embodied videos. Stage III must handle temporally
aligned video and action tokens. The training infrastructure adapts parallel strategies to the
current model configuration, data type, sequence length, and attention pattern.
This infrastructure supports stable and efficient training on high-resolution, long-duration sequences,
including 720P and 15-second video settings. From the perspective of Physical AI, this is important
because long-horizon temporal context is not optional: many control-relevant variables—object
permanence, task progress, delayed effects, and failure history—require extended temporal modeling.
The infrastructure determines not only how large the model can be, but how effectively the model
can absorb the most valuable control information. It also prepares the model for deployment-aware
inference: hybrid attention, efficient temporal factorization, token streaming compatibility, and
action-only inference support make deployment more practical. Kairos is not trained as a generic
offline video generator and then retrofitted for robotics; it is trained from the beginning as a
world-action model whose representation, memory, action interface, and runtime constraints are
aligned.
3.6 Summary: From Flat Data Scaling to a Staged Cross-Embodiment Curriculum
The Native Pretraining Paradigm of Kairos reframes pretraining for Physical AI. Instead of treating
heterogeneous data as a flat mixture, Kairos organizes data by intervention strength. Instead
of treating video generation as the final objective, it uses generation to build and regularize a
control-sufficient state. Instead of treating robot data as a small downstream fine-tuning set, it uses
robot trajectories to ground previously learned physical and intentional priors in action–outcome
dynamics. Instead of treating training infrastructure as implementation detail, it treats scalable
long-horizon training as a prerequisite for learning the state variables required by embodied control.
StageIprovidesphysicalpretrainingfrompassiveobservation. StageIIprovidesembodiedpretraining
from human-centric and robot-centric visual experience. Stage III provides regret-aware world-action
training from robot trajectories and execution preference pairs. Together, they form a progression
from physical priors, to task-structured embodied visual dynamics, to robot-grounded world-action
alignment:
D −→ D −→ D . (29)
obs human robot
(cid:124)(cid:123)(cid:122)(cid:125) (cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
StageI StageII StageIII
The native pretraining paradigm is designed to create the control-relevant world-action state needed
for future regret-aware Physical AI. In terms of the regret formulation, the curriculum supplies
the experience needed to learn variables that affect physical cost: physical priors from passive
observation, task-structured embodied visual dynamics from human-centric and robot-centric visual
experience, and action consequences plus execution preferences from robot data. CEDC’s role is
not simply to scale data, but to turn heterogeneous experience into a developmental pathway for
control-sufficient world modeling.
38

4 Data
Data is the substrate through which Kairos acquires the information required for constructing
and maintaining the control-sufficient state Z . Section 3 described the Cross-Embodiment Data
t
Curriculum as a progression from passive physical observation, to intentional human intervention, to
embodied robot intervention. This section details how the corresponding data are collected, curated,
tagged, captioned, and processed at scale. The central principle is that data for Physical AI should
not be evaluated only by raw scale, visual diversity, or aesthetic quality. It should also be evaluated
| by control | information |     | density. |     |     |     |     |     |     |
| ---------- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- |
For a physical world model, data is valuable when it reduces uncertainty about the variables that
matter for control: action consequences, contact dynamics, failure boundaries, recovery strategies,
task progress, safety risks, and the gap between imagined and real outcomes. A short clip containing
a near-boundary failure, a recovery maneuver, a marginal success, a slip, or a collision may be more
valuable than hours of visually clean but ordinary successful video. This is because near-boundary
events reveal the limits of controllability and the conditions under which actions remain recoverable,
| while ordinary |     | successes | may | only reinforce | common | patterns. |     |     |     |
| -------------- | --- | --------- | --- | -------------- | ------ | --------- | --- | --- | --- |
We define control information density (CID) conceptually as the information gain that a data sample
| provides | about | control-relevant |     | variables | per | unit cost: |                  |         |      |
| -------- | ----- | ---------------- | --- | --------- | --- | ---------- | ---------------- | ------- | ---- |
|          |       |                  |     |           |     |            | (cid:0) (cid:12) | (cid:1) |      |
|          |       |                  |     |           | H(Θ | | D) − H   | Θ(cid:12)D∪{d}   |         |      |
|          |       |                  |     | CID(d)    | =   |            |                  | ,       | (30) |
Cost(d)
where d denotes a data segment, D denotes the existing dataset, and Θ denotes the control-relevant
variables that matter for embodied decision-making, such as action consequences, contact dynamics,
failure boundaries, recovery strategies, safety risks, task progress, and the gap between imagined
and real outcomes. Cost(d) may include acquisition cost, annotation cost, compute cost, safety risk,
or deployment cost. This definition is not introduced as a fully implemented optimization objective
in the current system. Rather, it clarifies the data-side proxy for the regret objective: data should
be selected, structured, and scaled according to how much it helps the model preserve variables that
| enter the | physical | cost | c and | improve | the control-sufficient |     | state Z | .   |     |
| --------- | -------- | ---- | ----- | ------- | ---------------------- | --- | ------- | --- | --- |
t
Under this view, different data types have different expected control value. At a coarse level, Kairos
| uses the | following | priority | order: |     |     |     |     |     |     |
| -------- | --------- | -------- | ------ | --- | --- | --- | --- | --- | --- |
near-boundary failure and recovery data > near-boundary successful data
|     |     | contact-rich |             | data ordinary | successful |     | trajectories |     | (31) |
| --- | --- | ------------ | ----------- | ------------- | ---------- | --- | ------------ | --- | ---- |
|     | >   |              |             | >             |            |     |              |     |      |
|     | >   | ordinary     | observation |               | videos,    |     |              |     |      |
This ordering should be interpreted by diagnostic value rather than by event label alone.
Near-
|          |         |     |          | reveals | where | a task | breaks within | the normal operating | regime |
| -------- | ------- | --- | -------- | ------- | ----- | ------ | ------------- | -------------------- | ------ |
| boundary | failure | and | recovery | data    |       |        |               |                      |        |
and how the agent can return from an error state to a feasible state. Near-boundary successful data
reveals the conditions under which the system remains successful close to failure or safety margins.
reveals friction, force, deformation, support, slip, collision, grasp stability, and
| Contact-rich | data |     |     |     |     |     |     |     |     |
| ------------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
tool–object interaction. Ordinary successful trajectories provide task execution patterns. Ordinary
observation videos provide broad physical priors. All are useful, but they are not equally informative
for control. Extreme, non-diagnostic, or out-of-distribution failures may still be useful for safety
filtering and anomaly detection, but they should not be assumed to have the highest CID for learning
| action consequences, |     |     | failure | boundaries, | or recovery | strategies. |     |     |     |
| -------------------- | --- | --- | ------- | ----------- | ----------- | ----------- | --- | --- | --- |
39

This principle does not replace data scale. Scale remains necessary for coverage, robustness, and
general physical priors. However, scale alone is not sufficient. A Physical AI model trained on
massive but low-density observation data may become a strong visual predictor while remaining
weak at failure anticipation, action–outcome reasoning, or safety filtering. The Kairos data pipeline
therefore combines large-scale collection with filtering, tagging, captioning, and data-engineering
infrastructure designed to make high-value control information retrievable and learnable.
The current data system should be understood as the first stage of this direction. It builds the
large-scale foundation required for world modeling: diverse open-source datasets, in-house Internet-
scale data, first-person manipulation data, standardized shot segmentation, hierarchical filtering,
structured tags, high-quality captions, physics-centric annotations, long-horizon task decomposition,
and high-throughput data processing. Future versions can further strengthen explicit measurement
of control information density through real robot rollouts, simulation alignment, failure mining,
contact event detection, recovery annotation, and safety-risk calibration.
4.1 Data Collection: Multi-Source Experience Acquisition
Kairos adopts a hybrid data collection strategy that combines open-source public datasets with
in-house proprietary data (Figure 10). The purpose is not merely to maximize the number of videos,
but to cover the different experience regimes required by the Cross-Embodiment Data Curriculum.
Figure 10 Distribution of Kairos data sources across passive observation, human intervention, and robot
intervention regimes.
Thecollectionpipelineincludesthreemainsources: publicopen-sourcedatasets,compliantacquisition
of publicly available Internet data, and first-person human manipulation data. Public datasets such
as Koala-36M [96], OpenHumanVid [97], and VidGen [98] contribute diverse visual and temporal
patterns; robotics-oriented datasets such as AgiBotWorld-Beta [75] and DROID [76] contribute
robot-relevant scenes, manipulation examples, and embodied interaction patterns. To overcome the
40

limitationsofpublicdatasets, Kairosfurtherconstructsalarge-scalein-houseproprietarydatasystem
consisting of Internet-crawled data and real-world collected data. The Internet-scale component is
organized through a hierarchical taxonomy with tens of millions of leaf nodes, covering four core
domains: human, robot, general scenes, and physical phenomena. Each domain is subdivided into
hundreds of secondary and thousands of tertiary categories, with further fine-grained subdivisions
per category.
This taxonomy has a control-sufficient interpretation. The human domain provides intentional
behavior and task structure. The robot domain provides robot–environment interaction and action-
relevant scenes. The physics domain provides phenomena such as motion, collision, gravity, fluid-like
behavior,deformation,support,andcontact. Thegeneral-scenedomainprovidesbroadenvironmental
context and semantic diversity.
During raw collection, videos are obtained from publicly available Internet sources and preprocessed
according to platform-specific characteristics. The cleaning phase removes corrupted videos, dupli-
cates, and invalid clips shorter than five seconds. After this process, Kairos accumulates several
millions of hours of valid raw video data. This scale is a foundation rather than the final measure of
data value.
A major limitation of existing open-source and Internet-scale data is the shortage of fine-grained ma-
nipulation and embodied interaction. To address this gap, Kairos additionally collects high-precision
first-person human manipulation data. Ego-centric data captures hand–object interaction from a
viewpoint closer to embodied operation, providing information about reachability, manipulation,
tool use, occlusion, contact transitions, task progress, and recovery behavior.
From the perspective of interventional generalization, collection sources are organized as
D −→ D −→ D . (32)
obs human robot
This ordering is not only a training curriculum; it is also a data collection principle. The system
should collect data that fills gaps along the path from passive physical regularities to action–outcome
grounding.
Shot segmentation and clip standardization. Kairos performs unified shot segmentation on all
raw videos using PySceneDetect with multiple scene detectors, achieving over 95% segmentation
precision and approximately 80% recall. The pipeline applies the following rules:
• keep segments between 5 and 40 seconds;
• further split long shots longer than 40 seconds into 20-second clips;
• discard segments shorter than 5 seconds to avoid fragmented information.
Through this pipeline, Kairos obtains hundreds of millions of standardized video clips, providing a
searchable reservoir from which control-relevant, high-density experiences can be filtered, tagged,
captioned, and sampled.
4.2 Data Curation: From Quality Filtering to Control-Relevant Filtering
Data curation transforms the raw clip pool into a training-ready corpus. The current Kairos pipeline
useshierarchicalfiltering(Figure11)toimprovevisualquality,temporalcoherence,semanticdiversity,
safety, and redundancy control. These filters are necessary because noisy, corrupted, trivial, or unsafe
videos can degrade training. However, for Physical AI, quality filtering is only the first layer. A
41

visually clean clip is not necessarily control-informative. Therefore, Kairos interprets data curation
as a two-level process: basic quality filtering followed by control-relevant event filtering.
Figure 11 Hierarchical curation pipeline: basic quality filtering removes noisy clips, while control-relevant
| event | filtering | prioritizes | clips | with | high | control | information | density. |     |
| ----- | --------- | ----------- | ----- | ---- | ---- | ------- | ----------- | -------- | --- |
| Basic | Quality   | Filtering   |       |      |      |         |             |          |     |
The first level removes clips that are unsuitable for stable world-model training:
• Aesthetic Score. Aesthetic quality indicates visual richness, composition, and content
diversity. Low-aesthetic videos may contain simplistic scenes, poor color distribution, or
insufficient visual structure, limiting their usefulness for learning broad visual priors. Kairos
uses an aesthetic predictor built on a CLIP backbone with an MLP head and filters out samples
|     | below | a predefined |     | threshold. |     |     |     |     |     |
| --- | ----- | ------------ | --- | ---------- | --- | --- | --- | --- | --- |
• Motion Score. Temporal dynamics are essential for world modeling. Static videos contain
insufficient temporal information, while videos with extreme flickering or unstable motion
can harm temporal consistency. Kairos uses RAFT [99] to compute optical flow between
consecutive frames; the magnitude is aggregated into a global motion score, and clips with
|     | excessively |     | low or | high motion |     | are filtered. |     |     |     |
| --- | ----------- | --- | ------ | ----------- | --- | ------------- | --- | --- | --- |
• AI-generated videos are increasingly common on the Internet. Some synthetic
|     | AIGC | Score. |     |     |     |     |     |     |     |
| --- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
videos may be useful in later stages if validated, but low-quality synthetic content can introduce
artifacts,unrealisticdynamics,ormisleadingphysicalpatterns. KairostrainsaViT-Large-based
discriminator on a proprietary synthetic-video dataset and excludes clips above a predefined
|     | AIGC | threshold | in  | relevant | training | stages. |     |     |     |
| --- | ---- | --------- | --- | -------- | -------- | ------- | --- | --- | --- |
• Pornographic, violent, or otherwise unsafe videos can mislead model training
|     | NSFW | Score. |     |     |     |     |     |     |     |
| --- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
and are inappropriate for general-purpose Physical AI. Kairos uses the open-source Falconsai
|     | model | [100] | to filter | NSFW | content | from | crawled | Internet | data. |
| --- | ----- | ----- | --------- | ---- | ------- | ---- | ------- | -------- | ----- |
• Blurriness Score. Sharpness affects the model’s ability to learn object boundaries, contact
points, motion cues, and spatial structure. Kairos uses the Laplacian operator to assess image
sharpness; higher Laplacian scores indicate richer edges and clearer visual details. Clips below
|     | the | sharpness | threshold |     | are removed | or  | downweighted. |     |     |
| --- | --- | --------- | --------- | --- | ----------- | --- | ------------- | --- | --- |
• Human Motion Score. Human behavior is a major source of intentional intervention data.
However, a dataset dominated by static human clips may not teach useful body, hand, or
manipulation dynamics. Kairos uses YOLOX [101] for human detection and ByteTrack [102]
42

for trajectory tracking, then computes normalized pixel velocity for each detected person to
|     | support | selection | of clips | with | meaningful | human | motion. |     |
| --- | ------- | --------- | -------- | ---- | ---------- | ----- | ------- | --- |
• Text-heavy videos may introduce unwanted bias, especially in early video-
|     | OCR | Score. |     |     |     |     |     |     |
| --- | --- | ------ | --- | --- | --- | --- | --- | --- |
generation training where text rendering can interfere with convergence. Kairos uses DB-
Net [103] for text-region detection and computes an OCR score based on the proportion of
text regions in the frame; clips with excessive text are excluded in early phases, while text-rich
clips may be selectively used in later stages if text generation or GUI-like tasks are relevant.
• Internet videos contain large amounts of near-duplicate content.
|     | Data | Deduplication. |     |     |     |     |     |     |
| --- | ---- | -------------- | --- | --- | --- | --- | --- | --- |
Redundant clips increase storage and compute cost without adding new information. Kairos
extracts video embeddings using CLIP and maintains an embedding pool for large-scale
deduplication; for each new clip, pairwise similarity with historical clips is computed and only
the higher-resolution or higher-quality version is retained when similarity exceeds a threshold.
From the control-sufficient perspective, these filters also remove noise that can obscure physical
and action-relevant variables: blurry videos make contact points harder to infer; unstable flickering
weakens temporal state learning; corrupted synthetic videos may teach incorrect dynamics.
| Control-Relevant |     |     | Event Filtering |     |     |     |     |     |
| ---------------- | --- | --- | --------------- | --- | --- | --- | --- | --- |
The second level would prioritize clips according to control information density. The current pipeline
does not yet compute CID directly; future iterations should explicitly target:
• Near-boundary failures: marginal grasp failure, near slip that becomes a drop, near collision
|     | that | becomes | contact, | unstable | stack collapse, | partial | task | failure; |
| --- | ---- | ------- | -------- | -------- | --------------- | ------- | ---- | -------- |
• regrasping, repositioning, replanning, human correction, retry behavior,
|     | Recovery     |     | events:       |     |     |     |     |     |
| --- | ------------ | --- | ------------- | --- | --- | --- | --- | --- |
|     | post-failure |     | continuation; |     |     |     |     |     |
• marginal grasps that remain stable, near slips that are corrected,
|     | Near-boundary |     | successes: |     |     |     |     |     |
| --- | ------------- | --- | ---------- | --- | --- | --- | --- | --- |
near collisions that are avoided, partial successes completed through correction;
• Contact transitions: first contact, loss of contact, grasp closure, slip, collision, support
change;
• Safety and anomaly events: human proximity, sharp-object contact, excessive force,
|     | irreversible |     | state change, | extreme | or non-diagnostic |     | failures; |     |
| --- | ------------ | --- | ------------- | ------- | ----------------- | --- | --------- | --- |
• Long-horizon dependencies: delayed failure, multi-step dependency, hidden object state,
|     | task-progress |     | change. |     |     |     |     |     |
| --- | ------------- | --- | ------- | --- | --- | --- | --- | --- |
These events are rare compared with ordinary successful clips, but they are highly valuable when
they are close to the task manifold and diagnostically interpretable. A model that never sees
near-boundary failures may generate clean success futures but remain unable to predict where
deployment will break. A model that never sees recovery may fail to plan after mistakes. A model
that never sees near-boundary successes may not learn which small corrections or safety margins
| preserve | successful |     | execution. |     |     |     |     |     |
| -------- | ---------- | --- | ---------- | --- | --- | --- | --- | --- |
In the current Kairos report, these control-relevant filters should be presented as a guiding extension
built on top of the existing curation pipeline. The current implementation provides strong quality,
safety, motion, and redundancy filtering. Future iterations can incorporate explicit detectors, human-
in-the-loop annotation, simulation labels, robot rollout logs, and tactile–force signals to compute
| more | precise | control | information | density | scores. |     |     |     |
| ---- | ------- | ------- | ----------- | ------- | ------- | --- | --- | --- |
43

Table 2 Video Domain Tags. Each video is assigned to exactly one domain to ensure unambiguous data
partitioning.
|     |     | Tag | Sub-tags |     |     | Brief | Description |     |
| --- | --- | --- | -------- | --- | --- | ----- | ----------- | --- |
Human scenes/actions/occupation/ Humanbehaviorvideosforlearninghuman
|     |     |     | gender/age/context/face |     |     | blur/- behavior | patterns |     |
| --- | --- | --- | ----------------------- | --- | --- | --------------- | -------- | --- |
body motion
|     |     | Robot | scenes/actions |     |     | Robot        | interaction/task  | execution videos |
| --- | --- | ----- | -------------- | --- | --- | ------------ | ----------------- | ---------------- |
|     |     |       |                |     |     | for learning | robot–environment | interaction      |
mechanisms
|     |     | Physics | principles |     |     | Videosofphysicallaws/naturalphenomena |                        |     |
| --- | --- | ------- | ---------- | --- | --- | ------------------------------------- | ---------------------- | --- |
|     |     |         |            |     |     | for                                   | physical-rule modeling |     |
General content type/scene/animal General-scenevideosensuringcompletecov-
|     |          |            |     |          |                      | erage | of the tagging | system |
| --- | -------- | ---------- | --- | -------- | -------------------- | ----- | -------------- | ------ |
| 4.3 | Tagging: | Structured |     | Indexing | for Control-Relevant |       | Sampling       |        |
Tagging converts raw videos into structured, searchable, and samplable training assets. For Internet-
scale data, manual inspection is impossible. Tags allow the system to organize heterogeneous clips,
balance data proportions, retrieve specific domains, reduce sampling bias, and support downstream
captioning. In Kairos, tagging should be understood not only as semantic indexing, but as a
| mechanism |     | for exposing |     | control-relevant | structure. |     |     |     |
| --------- | --- | ------------ | --- | ---------------- | ---------- | --- | --- | --- |
The current tagging system contains two primary categories: video attribute tags and video domain
tags. Attribute tags describe global properties of the clip that are useful for filtering and sampling,
such as camera motion, static content, blur, motion type, or other intrinsic video characteristics.
describe the semantic or functional category of the clip; the main domain tags are
| Domain     |     | tags     |     |     |     |     |     |     |
| ---------- | --- | -------- | --- | --- | --- | --- | --- | --- |
| summarized |     | in Table | 2.  |     |     |     |     |     |
This tag system supports the Cross-Embodiment Data Curriculum. Human tags help sample
intentional behavior. Robot tags help sample action-grounded interaction. Physics tags help sample
passive physical phenomena. General content tags ensure broad environmental coverage. Together,
they provide the indexing structure required for stage-specific data mixtures.
For control-sufficient world modeling, the tagging system can be extended with control-oriented tags.
These tags need not all be fully implemented in the current version, but they clarify the desired
| direction |     | of the Kairos | data | engine: |     |     |     |     |
| --------- | --- | ------------- | ---- | ------- | --- | --- | --- | --- |
• Intervention-Level Tags: passive observation, human intervention, robot intervention, or
mixed human–robot interaction. Supports intervention-strength curricula rather than flat data
mixtures.
• contact, collision, sliding, rolling, deformation, support, fluid motion,
|     | Physical-Event |     | Tags:   |           |            |                  |     |     |
| --- | -------------- | --- | ------- | --------- | ---------- | ---------------- | --- | --- |
|     | gravity-driven |     | motion, | tool use, | occlusion, | object transfer. |     |     |
• Object–Contact–Action Tags: whichobject, whataction, whatcontactstate, whatphysical
transition.
• Task-Progress Tags: subtask completion, remaining steps, task ordering, long-horizon
dependencies.
• failure type, cause, recovery action, recovery success, return to
|     | Failure–Recovery |     |     | Tags: |     |     |     |     |
| --- | ---------------- | --- | --- | ----- | --- | --- | --- | --- |
44

feasible state.
• Safety-Risk Tags: unsafe contact, human proximity, collision risk, excessive force, unstable
objects, irreversible state changes, high-uncertainty situations.
• Embodiment Tags: robot type, gripper type, camera viewpoint, end-effector state, proprio-
ceptive context, tactile/force availability, control modality.
The purpose of these tags is not to create a rigid symbolic simulator. Rather, tags provide structured
weak supervision and retrieval handles. They help the model and the data pipeline focus on the
variables that matter for control. They also enable stage-specific sampling: Stage I may prioritize
physics and general-scene tags; Stage II may prioritize human-intervention and task-progress tags;
Stage III may prioritize robot, contact, action, failure, and recovery tags.
Tagging also improves caption quality. When tag information is passed into the captioning pipeline,
the generated descriptions become more complete, less ambiguous, and more aligned with the actual
content of the video. This is especially important for control-relevant captions, where the model
must describe not only what appears in the video, but also what action occurs, what state changes,
what risk emerges, and what causal relation connects events.
Tag-annotation pipeline. For large-scale annotation, Kairos adopts an end-to-end automatic
pipeline based on Qwen3-VL-8B [104]. Original videos are uniformly sampled at fixed time steps to
balance representativeness and efficiency; structured tag rules, annotation paradigms, and semantic
constraints are integrated into the prompt; and inference results are stored in a structured JSON
format. The unified structured representation supports downstream data filtering, proportioning,
and sampling without requiring manual annotation at scale.
4.4 Captioning: From Visual Description to Control-State Supervision
Figure 12 Divide-and-conquer captioning: tag information provides semantic constraints; the VLM supplies
detailed natural-language interpretation; a multi-model ensemble fuses initial outputs into a final caption.
Captioning provides language supervision for world-model training. In ordinary video generation,
captions mainly describe the visible content of a clip. For Kairos, captions should play a broader
role: they should help shape the control-sufficient state Z . A useful caption should describe not only
t
objects and scenes, but also actions, physical changes, contact events, task progress, uncertainty,
and possible failure or recovery logic.
ThecurrentKairoscaptioningpipelineusesQwen3-VL-8B[104]asthecoremodelforvideodescription
generation. The baseline caption is required to cover five dimensions: (i) core subjects, including
45

humans, animals, and objects; (ii) subject actions; (iii) surrounding environment and background
| details; | (iv) | lighting | and | atmosphere; |     | and (v) | camera | motion. |     |
| -------- | ---- | -------- | --- | ----------- | --- | ------- | ------ | ------- | --- |
These dimensions provide a strong foundation for visual–semantic alignment. However, a generic
caption can still be incomplete or hallucinated. To improve detail richness and reduce ambiguity,
Kairos adopts a Divide-and-Conquer (DC) captioning strategy (Fig. 12). Instead of generating
captions directly from the raw video alone, the pipeline combines structured tag information with
visual content. Tags provide semantic constraints; the VLM supplies detailed natural-language
interpretation. This combination improves caption completeness and reduces hallucination.
Kairos further uses a multi-model ensemble annotation pipeline. Specifically, multiple medium-
parameter multimodal models—including Qwen3-VL-8B [104], InternVL3.5-8B [105], Mimo-7B [106],
and MiniCPM V4.5 [107]—independently generate initial descriptions. A stronger multimodal model
(Qwen3-VL-8B) then acts as a large-parameter fuser, referencing consensus information from the
initial outputs and supplementing finer details. Because this pipeline is computationally expensive,
it is applied mainly to high-quality continuous training data, balancing annotation quality and
| processing |     | efficiency. |     |     |     |     |     |     |     |
| ---------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
From the control-sufficient perspective, captioning should be evaluated by how well it supervises the
variables in Z . A caption such as “a robot arm moves a red block” is useful but incomplete. A more
t
control-relevant caption would include: the robot arm approaches the red block from the left, closes
the gripper, establishes contact, lifts the block slightly, avoids collision with the bowl, and places
the object on the table. If a slip occurs, the caption should state that the grasp becomes unstable,
the object rotates, the gripper loses contact, and the robot attempts to recover. Such descriptions
| expose | action    | consequences |     | and        | failure    | boundaries. |         |         |     |
| ------ | --------- | ------------ | --- | ---------- | ---------- | ----------- | ------- | ------- | --- |
| We     | therefore | organize     |     | captioning | objectives | into        | several | layers: |     |
• Semantic Captioning. This describes objects, agents, scenes, attributes, and high-level
actions.
• Thisdescribesmotion, contact, gravity, collision, support, deformation,
|     | Physical  | Captioning. |        |             |     |     |     |     |     |
| --- | --------- | ----------- | ------ | ----------- | --- | --- | --- | --- | --- |
|     | friction, | and         | object | permanence. |     |     |     |     |     |
• Embodied Captioning. This describes gripper state, hand–object relation, viewpoint, robot
|     | motion, | end-effector |     | interaction, |     | and action | sequence | where | available. |
| --- | ------- | ------------ | --- | ------------ | --- | ---------- | -------- | ----- | ---------- |
• Task-Progress Captioning. This describes the goal, current subtask, completed steps,
|     | remaining |     | steps, | and dependencies |     | between | steps. |     |     |
| --- | --------- | --- | ------ | ---------------- | --- | ------- | ------ | --- | --- |
• Failure–Recovery Captioning. This describes failure events, failure causes, recovery
|     | attempts, | and | post-recovery |     | state. |     |     |     |     |
| --- | --------- | --- | ------------- | --- | ------ | --- | --- | --- | --- |
• This describes unsafe contact, collision risk, human proximity,
|     | Safety-Risk  |     | Captioning.  |         |     |                 |     |     |     |
| --- | ------------ | --- | ------------ | ------- | --- | --------------- | --- | --- | --- |
|     | instability, |     | irreversible | action, |     | or uncertainty. |     |     |     |
The current implementation already supports semantic, physical, and long-horizon task-oriented
captioning. Future versions can extend this framework with explicit failure–recovery and safety-risk
captions, particularly for real robot and simulation-aligned data. This extension would directly
support regret-aware world modeling by teaching the model which states are costly and how errors
can be corrected.
Captioning should therefore be interpreted as control-state supervision. It converts raw video into
language signals that guide the model toward learning the variables that matter for prediction and
46

action. It is not a replacement for real action labels, tactile data, or robot rollouts, but it provides
scalable weak supervision for organizing large-scale visual experience.
4.5 Enhanced Text with Control-Oriented Chain of Thought
Figure 13 Enhanced text with control-oriented chain-of-thought annotations: physics-centric captions
explainunderlyingphysicalprinciples; long-horizontaskcaptionsdecomposetasksintosub-stepswithexplicit
dependencies.
Kairos further enriches selected data with enhanced text and chain-of-thought-style annotations
(Fig. 13).
Physics-centric. The core of world models lies in learning and reproducing the operational logic
of the real world, where physical laws serve as the key element to achieve this goal and represent
the fundamental characteristic that distinguishes world models from ordinary generative models—
namely, their “world cognition capability.” To fully exploit the core value of physical principles and
ensure the physical realism of world models, we construct specialized text datasets that explicitly
reinforce physical laws from the data source. Specifically, for data tagged as “physics,” we explicitly
strengthen the expression of physical laws within their captions. Our physics-centric caption data
not only describes the surface phenomena observed in videos but also explains the underlying
physical principles embedded in these phenomena, including dynamic behavioral constraints such as
object motion trajectories, collision interactions, gravitational effects, and frictional forces. Through
this approach, we ensure that the content generated by the model conforms to real-world physical
constraints, thereby enhancing physical realism. The left part of Figure 13 presents a typical example
of physics-centric captions.
Long-horizon Tasks. Causality and long-horizon sequence consistency constitute another core
element that distinguishes world models from ordinary generative models. To ensure the logical
consistency and rationality of long-horizon task execution, we focus on strengthening chain-of-
thought construction and task decomposition capabilities, creating datasets that target long-horizon
sequence scenarios. For selected human manipulation and robot interaction data, we construct a
long-horizon task-oriented annotation framework by clearly decomposing task steps and delineating
the causal logical chains between events. Specifically, we decompose complex task captions into
47

Table 3 Throughput optimization across the three core data engineering operators (8×4090 GPUs, 180
vCPUs).
|     | Operator |     |     | Baseline  | Optimized |     | Speedup | Key | techniques |     |     |     |
| --- | -------- | --- | --- | --------- | --------- | --- | ------- | --- | ---------- | --- | --- | --- |
|     |          |     |     | (hrs/day) | (hrs/day) |     |         |     |            |     |     |     |
Shot Detection 1,169.6 8,640.0 7.4× Distributed scheduling, frame
|     |     |     |     |     |     |     |     | skipping, |     | load balancing |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | -------------- | --- | --- |
Frame Filtering 612.0 18,332.7 29.9× FP16inference,CPUdecoding,
|     |            |     |     |       |     |         |       | concurrent |           | scheduling |       |     |
| --- | ---------- | --- | --- | ----- | --- | ------- | ----- | ---------- | --------- | ---------- | ----- | --- |
|     | Captioning |     |     | 137.0 |     | 4,665.9 | 34.0× | CPU        | decoding, | pipeline   | over- |     |
|     |            |     |     |       |     |         |       | lap,       | two-level | batching   |       |     |
multiple executable sub-steps, explicitly defining the dependencies and causal relationships between
each step, enabling the model to understand and reproduce task execution logic over extended
temporal sequences. This design effectively ensures the logical coherence of the model when handling
long-horizon sequence scenarios. The right part of Figure 13 illustrates a typical example of task
| decomposition |           | in long-horizon |     | tasks             | data. |     |         |           |     |             |         |          |
| ------------- | --------- | --------------- | --- | ----------------- | ----- | --- | ------- | --------- | --- | ----------- | ------- | -------- |
|               |           |                 |     |                   |       | A   | natural | extension |     | of enhanced | text is | failure– |
| Failure,      | recovery, |                 | and | risk annotations. |       |     |         |           |     |             |         |          |
recovery–risk annotation, especially important for regret-aware Physical AI. Failure annotations
describe the failure type (slip, collision, unstable grasp, occlusion error, wrong-object selection, task
interruption). Recovery annotations describe regrasping, repositioning, replanning, human correction,
or retry behavior. Risk annotations describe unsafe contact, high uncertainty, marginal stability, or
near-boundary states. The existing physics-centric and long-horizon annotation pipeline provides a
strong foundation; adding failure, recovery, and risk annotations would make the data engine more
| directly | relevant | to deployment-time |     |      | decision    | support.               |     |     |       |           |             |      |
| -------- | -------- | ------------------ | --- | ---- | ----------- | ---------------------- | --- | --- | ----- | --------- | ----------- | ---- |
| Enhanced | text     | functions          | as  |      |             |                        |     |     |       | learning. | It does not | make |
|          |          |                    |     | weak | supervision | for control-sufficient |     |     | state |           |             |      |
the model a symbolic reasoner; rather, it encourages the model to preserve the right variables—
physical relations, causal transitions, task dependencies, failure boundaries, and recovery logic. Its
outputs should ideally support three downstream functions: (1) train the model to associate visual
dynamics with physical and causal explanations; (2) support retrieval and sampling of high-control-
information clips; (3) provide interpretable supervision for failure analysis, long-horizon consistency,
| and risk-aware |     | evaluation. |     |     |     |     |     |     |     |     |     |     |
| -------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4.6 Data Engineering Infrastructure for Scalable Control-Information Processing
TheKairosdatapipelinerequireslarge-scaledataprocessinginfrastructure. Inthedatapre-processing
phase, we built an efficient infrastructure that achieves significant performance improvements for
three core operators: Shot Detection, Frame Filtering, and Captioning. The optimization strategy
focuses on three dimensions: computational parallelization, I/O optimization, and task scheduling, as
| summarized     | in  | Table    | 3.  |               |     |     |                |     |          |          |             |      |
| -------------- | --- | -------- | --- | ------------- | --- | --- | -------------- | --- | -------- | -------- | ----------- | ---- |
|                |     |          |     |               |     | The | shot detection |     | operator | segments | long videos | into |
| Shot Detection |     | Operator |     | Optimization. |     |     |                |     |          |          |             |      |
semantically coherent clips. Kairos employs a combination of multiple detectors on a single machine
with 8×4090 GPUs and 180 vCPUs. Key techniques include: distributed scheduling to replace
the original pipeline; resolution downscaling and frame skipping to reduce redundant computation;
dynamic worker allocation to increase parallelism; and duration-based task partitioning for load
balancing. These optimizations improve throughput from 1,169.6 to 8,640.0 hours/day (7.4×), while
48

maintaining a shot detection recall rate of 77.44%. Good segmentation preserves event integrity:
contact onset, collision, object transfer, task-step completion, or recovery sequence.
Theframefilteringoperatorconductsmulti-dimensional
FrameFilteringOperatorOptimization.
quality assessment, including luminance, blur, aesthetics, and pose detection. Throughput is im-
proved from 612.0 to 18,332.7 hours/day (29.9×) through: pre/post-processing refactoring to reduce
redundancy; adaptive frame sampling; CPU-concurrent decoding to eliminate serial I/O bottlenecks;
FP16 mixed-precision inference; and automatic resource scheduling with zero-copy video access
to achieve computation–I/O overlap. From the control-sufficient perspective, filtering determines
whether the model receives enough clear evidence about physical state: blurry frames may hide
contact; poor lighting may obscure object boundaries; unstable motion may corrupt temporal
continuity.
Caption Operator Optimization. The captioning operator generates textual descriptions for
video clips. Throughput is improved from 137.0 to 4,665.9 hours/day (34.0×) by reusing CPU-
concurrent decoding, adaptively sampling key segments, and decoupling video loading from model
inference into a pipeline architecture with a two-level batching mechanism that balances throughput
and memory utilization. For Physical AI, the caption operator should eventually prioritize clips with
| high control | information |     | density. |     |     |     |     |     |     |
| ------------ | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- |
End-to-end gain. Overall, the Kairos data engineering infrastructure achieves over 30× end-to-end
throughput improvement on a single machine with 8×4090 GPUs, with key contributions from:
(1) Computational Parallelization via distributed scheduling and load-balanced task partitioning;
(2)I/O OptimizationviaCPU-concurrentdecoding, zero-copystreaming, andpipelineoverlap; and
(3) via two-level batching and dynamic resource allocation across sub-modules.
| Task       | Scheduling   |     |        |               |       |                              |     |            |           |
| ---------- | ------------ | --- | ------ | ------------- | ----- | ---------------------------- | --- | ---------- | --------- |
| The deeper | significance |     | is not | just speed—it | makes |                              |     |            | possible. |
|            |              |     |        |               |       | scalable control-information |     | processing |           |
Without high-throughput infrastructure, high-CID data remains too expensive to mine and structure.
| 4.7 Limitations |     | and | Future | Data Directions |     |     |     |     |     |
| --------------- | --- | --- | ------ | --------------- | --- | --- | --- | --- | --- |
The current Kairos data pipeline provides a strong foundation for large-scale world modeling. The
| following | items | are scoped | as  | future work. |     |     |     |     |             |
| --------- | ----- | ---------- | --- | ------------ | --- | --- | --- | --- | ----------- |
| 1.        |       |            |     |              |     |     |     | A   | clip may be |
Visual and semantic quality metrics do not directly measure control value.
visually clean but uninformative for action–outcome learning; a near-boundary failure or
recovery clip may be visually imperfect but highly valuable for control. Future data selection
should explicitly measure contact, near-boundary failure, recovery, marginal success, boundary,
| and           | safety | information. |         |               |          |                |                |       |          |
| ------------- | ------ | ------------ | ------- | ------------- | -------- | -------------- | -------------- | ----- | -------- |
| 2.            |        |              |         |               |          | Internet-scale | videos provide | broad | physical |
| Heterogeneous |        | data         | sources | are not fully | aligned. |                |                |       |          |
priors but limited action grounding; human-centric data provides intentional behavior but
does not directly match robot embodiment; robot data provides action grounding but remains
expensiveandnarrow. Futuredataconstructionshouldstrengthenalignmentamongego-centric
data, robot trajectories, and simulation rollouts through shared event labels and temporally
| aligned | state–action |     | annotations. |     |     |     |     |     |     |
| ------- | ------------ | --- | ------------ | --- | --- | --- | --- | --- | --- |
3. Captions and CoT annotations may contain hallucinations or incomplete causal explanations.
Future systems should calibrate captions against physical signals, robot logs, simulator states,
| and | human | verification |     | where necessary. |     |     |     |     |     |
| --- | ----- | ------------ | --- | ---------------- | --- | --- | --- | --- | --- |
4.
Synthetic or generated data should not be treated as automatically valid training experience.
49

It can enrich rare events, stress-test policies, and generate candidate rollouts, but it must be
calibrated against real or high-fidelity simulated outcomes.
5. Direct closed-loop regret reduction requires further data infrastructure. Future datasets should
explicitly measure whether imagined rollouts correlate with real rollouts, whether failure
predictions anticipate real failures, whether safety filtering reduces unsafe events, and whether
recovery data improves real policy behavior.
These limitations define the next stage of Kairos data development: moving from large-scale data
engineeringtowardclosed-loopdatainfrastructurewithhighcontrolinformationdensity. Futuredata
collection should also support direct estimation of cost-relevant outcomes, including failure events,
recovery effort, unsafe contact, human intervention, and imagined–real rollout discrepancy. These
outcomes are needed to move from data-side proxies toward empirical validation of regret-aware
decision support.
4.8 Summary: A Data Engine for Control-Sufficient World Modeling
This section reframes the Kairos data system as a control-sufficient data engine. The goal is not
merely to collect more videos or produce cleaner captions; the goal is to acquire, filter, annotate,
retrieve, and process the experience most useful for constructing Z .
t
The current pipeline provides five key capabilities: (i) large-scale multi-source data collection
spanning open-world videos, public datasets, in-house Internet data, first-person manipulation
data, and robot-relevant corpora; (ii) standardization of raw videos into training clips through shot
segmentation; (iii) hierarchical curation to remove noise, low-quality clips, unsafe content, AIGC
contamination, redundant videos, and visually unsuitable samples; (iv) structuring of data through
tags and captions, including physics-centric and long-horizon task annotations; (v) high-throughput
engineering infrastructure for scalable shot detection, frame filtering, and captioning.
The broader significance is that Kairos data infrastructure can move beyond raw scale toward control
information density. Control information density should therefore be interpreted as a data-side route
toward reducing Reg (f;g), not as a separate objective disconnected from the rest of the model
H
stack. The most valuable data will be the data that reduces uncertainty about action consequences,
contact dynamics, failure boundaries, recovery strategies, and safety risks. This connects data to
the rest of the Kairos stack: data provides control-relevant information; Section 3.1 organizes it
through a cross-embodiment curriculum; Section 2 compresses and maintains it as a control-sufficient
state; deployment-aware inference will eventually test whether this state reduces real-world mistakes.
The Kairos data engine should be understood as a model-side prerequisite for future regret-aware
Physical AI.
5 Inference
Inference is the stage where the control-sufficient state Z becomes operational. Sections 2–4
t
described how Kairos constructs Z , learns the information required for Z , and builds a data engine
t t
for experience with high control information density. This section addresses the next question: how
can such a state be used under practical deployment constraints?
For Physical AI, inference is not a passive decoding step. It is the mechanism through which a
world model enters an observation–action–feedback loop. A model may generate visually impressive
futures offline, but if its inference is too slow, too memory-intensive, or too dependent on unrealistic
50

hardware assumptions, it cannot support action selection, risk assessment, failure anticipation,
recovery planning, or future closed-loop improvement. Latency, memory footprint, communication
cost, and hardware compatibility are not secondary engineering details—they determine whether the
world model can be used before an action is executed.
Kairos therefore treats inference as regret-relevant information throughput. The practical
question is not only how good a generated rollout looks, but how much control-relevant information
the model can produce per unit of time, memory, compute, and communication. A slow model may
preserve rich visual detail but fail to affect the robot’s decision before the action deadline. A more
efficient model may preserve fewer pixels but provide timely information about task progress, action
consequence, or failure risk—for Physical AI, the latter may be more valuable.
5.1 Toward Self-Evolution: Proxy Rollout–Evaluation–Refinement
The vision of the Kairos framework extends beyond serving as a static inference engine: it is designed
as deployable infrastructure for future self-evolutionary learning. From a regret-aware perspective,
self-evolution is the mechanism through which a world-action model could progressively reduce
the predicted cost J(cid:98)H , and eventually the real physical cost J
H
, by generating candidate futures,
comparing their predicted consequences, learning from discrepancy, and refining the next decision.
This capability is rooted in Kairos’s unified understanding–generation–prediction architecture. By
tightly coupling these three pathways, the model provides a substrate for future observation–
action–feedback loops and continuous refinement of its internal representations and decision-making
strategies.
In practice, the current system instantiates this idea through the rollout–evaluation–refinement
cycle shown in Figure 14. Upon receiving an instruction, the generation and prediction modules
simulate multiple physically plausible future rollout paths and action trajectories. Leveraging the
Chain-of-Thought (CoT) framework, Kairos’s understanding module acts as a proxy evaluator,
analyzing, scoring, and ranking these diverse paths according to physical plausibility, task progress,
and risk-relevant variables. This reflective process enables the system to identify preferable strategies,
correct generation-level errors, and improve prompt-level precision over iterative refinement.
Asaconcreteself-evolutionarystrategy,thismechanismisvalidatedbyinstantiatingpromptrewriting
agents. Building upon the prompt alignment strategy, the rewriter (i.e., the prompt template) serves
as an active evolutionary proxy. The understanding module scores the outputs generated by different
prompts, dynamically evaluates and rewrites user instructions, and constructs a localized self-
improving loop. We empirically observe that this automated process directly enhances the model’s
precision and alignment performance in deployed generation scenarios.
While prompt optimization and trajectory selection represent successful initial validations, this
self-evolutionary paradigm is equally applicable to the policy configurations of the World-Action
Model (WAM). By enabling the model to autonomously simulate, evaluate, and refine its policy
parameters within the closed-loop understanding framework, Kairos can continuously improve its
decision-making and execution strategies for physical interactions. In the regret-aware view, this
extension is the natural path toward measurable regret reduction: the evaluator can score predicted
task success, collision risk, contact stability, recovery cost, and safety margin; refinement can target
the policy, the action proposal distribution, the rollout evaluator, or the world-action model itself.
We will thoroughly investigate this application in subsequent versions of Kairos.
The current self-evolution mechanism should nevertheless be interpreted as a controlled proxy for
51

Figure 14 Proxy rollout–evaluation–refinement framework. The current implementation demonstrates
prompt-level and generation-level refinement; real-robot policy self-evolution remains future work.
future regret-aware Physical AI: it is demonstrated at the prompt and generation level rather than
through end-to-end robot deployment, and it does not yet establish that imagined rollouts correlate
withrealrobotrollouts, thatfailurepredictionsreduceunsafeevents, orthatimaginedpolicyupdates
measurably improve real task success. It nonetheless provides the model-side and inference-side
prerequisites on which future closed-loop, regret-minimizing validation can be built.
5.2 Prompt Self-Alignment
In real-world deployment scenarios, user queries and prompts exhibit significant variations in
expression styles, level of detail, and linguistic conventions. Current mainstream prompt alignment
solutions,adoptedbyleadingtext-to-videomodelssuchasWan[82]andSeedance2.0[108],universally
follow a static template mapping approach: they convert user inputs into standardized dense caption
formats through manual induction of model-preferred prompt paradigms and best practices. While
this method is simple and effective, it fundamentally relies on the accumulation of human expertise,
rendering it incapable of adaptively updating alongside iterative improvements in model capabilities
and insufficient to cover the diversity of user inputs.
Built upon Kairos’s unified self-evolutionary infrastructure, we propose a closed-loop Prompt
Self-Alignment strategy following the generation–evaluation–iterative refinement paradigm, which
reduces reliance on static templates. This strategy instantiates Kairos’s general rollout–evaluation–
refinement paradigm at the prompt and generation level, and is co-driven by two core components:
a prompt rewriting agent with self-reflective and iterative capabilities, and a specially designed
multi-dimensional video quality reward function. This reward function comprehensively quantifies
the physical plausibility, task completion rate, and overall visual quality of generated videos,
providing objective and consistent evaluation criteria for the self-evolutionary process. From a
regret-aware perspective, these dimensions are not arbitrary aesthetic criteria: physical plausibility,
52

task completion, and instruction alignment are direct indicators of whether the imagined future
preserves the control-relevant variables on which downstream action quality depends.
The implementation workflow is as follows. Upon receiving a user instruction, the prompt rewriting
agent first generates an initial batch of diversified rewritten candidates. All candidate prompts are
fed into the video generation model to obtain corresponding outputs, which are then subjected to
fully automated comprehensive evaluation by the multi-dimensional reward function. The system
feeds back the evaluation results along with their corresponding candidate prompts to the rewriting
agent, enabling it to perform self-reflection, defect attribution, and evolutionary refinement based on
actual generation outcomes, thereby producing a new round of higher-quality prompt candidates.
After multiple rounds of closed-loop iteration, the system gradually converges to a higher-scoring
prompt candidate, ultimately achieving significant improvement in the comprehensive quality of
generated videos. The process can operate without human intervention after initialization in the
testedprompt-refinementsetting, whilebroaderdeploymentadaptationtomodel-capabilityevolution
and user-input drift remains to be validated.
From the perspective of control-sufficient world modeling, Prompt Self-Alignment should not be
treated merely as aesthetic prompt enhancement. The reward function should favor prompts that
help the model preserve control-relevant variables: for embodied scenes, a better prompt may
explicitly describe object identity, contact relation, task goal, action sequence, physical constraints,
camera viewpoint, and expected state transition. In this sense, Prompt Self-Alignment is the
prompt-level instantiation of regret-aware refinement: better-conditioned rollouts expose more of the
variables that matter for control, and the refinement loop systematically steers the model toward
prompts that reduce ambiguity, hallucination, and downstream failure. Prompt Self-Alignment
nonetheless remains a proxy: it operationalizes the rollout–evaluation–refinement loop at the prompt
and generation level, while validation against real robot policy improvement is pending.
5.3 Inference Efficiency
World generation within embodied AI applications imposes two contradictory yet critical operational
requirements. First, to power massive data simulation platforms on cloud infrastructure, the world
model must achieve low-latency and high-throughput video synthesis to accelerate policy rollouts.
Second, todemocratizedevelopmentandfacilitaterapidprototyping, theinferencestackmustremain
highly cost-effective, allowing individual researchers to execute the model on resource-constrained,
consumer-grade computing hardware. To reconcile the tension between generation fidelity and
operational cost across these distinct environments, the Kairos stack introduces a deployment-
aware optimization framework. We systematically address these efficiency bottlenecks through
two complementary vectors: Timestep Distillation, which structurally compresses the diffusion
sampling trajectories to reduce empirical sampling latency and lower the cost of imagined rollouts;
and Hardware-Aware Inference Optimization, which co-designs low-level computational kernels and
memory footprints to maximize hardware utilization. The formal mechanisms of these optimizations
are detailed below.
5.3.1 Timestep Distillation
High-resolution embodied world models can generate realistic environment dynamics and agent
interactions, but their diffusion-based iterative sampling often requires dozens or even hundreds
of denoising steps, creating a major computational bottleneck for deployment-oriented inference.
To address this issue, we distill a pretrained 480P Embodied World Model into an efficient 4-step
53

Figure 15 Performance of Distilled Kairos Robot Model on PAI-Bench Dataset
generator. Following Eq. 21 with the timestep relabeled as σ ∈ [0,1] to match standard distillation
notation, noisy samples z = α zT +σϵ (with α ≜ 1−σ and ϵ ∼ N(0,I)) are constructed by
σ σ 0 σ
perturbing clean samples zT from the pretrained teacher model. The student model is then trained
0
to approximate the teacher distribution using significantly fewer sampling steps.
Distribution Matching Distillation. We adopt Distribution Matching Distillation (DMD) [109,
110] to distill the teacher distribution into a compact generator. The student is parameterized as a
feed-forward generator
zθ = G (ξ), (33)
0 θ
which maps Gaussian noise ξ directly to the data space with only a few sampling steps.
Since the student defines an implicit distribution whose score function is unavailable in closed form,
54

we introduce an auxiliary fake-score network ϕ. Under the Rectified Flow formulation, learns the
ϕ
| velocity | field through |     |     |     |                  |     |     |          |     |     |     |
| -------- | ------------- | --- | --- | --- | ---------------- | --- | --- | -------- | --- | --- | --- |
|          |               |     |     |     | (cid:20)(cid:13) |     |     | (cid:21) |     |     |     |
(cid:13)2
|     |     |     | L    | = E | (cid:13)V       | (z ,σ)−(ϵ−zθ)(cid:13) |     | .          |     |     | (34) |
| --- | --- | --- | ---- | --- | --------------- | --------------------- | --- | ---------- | --- | --- | ---- |
|     |     |     | fake |     | zθ,ϵ,σ (cid:13) | ϕ σ                   |     | 0 (cid:13) |     |     |      |
|     |     |     |      |     | 0               |                       |     | 2          |     |     |      |
The predicted velocity can be re-parameterized as a reconstruction of the clean sample
|     |     |     |     |     | z     | −σV (z | ,σ) |     |     |     |      |
| --- | --- | --- | --- | --- | ----- | ------ | --- | --- | --- | --- | ---- |
|     |     |     |     |     | zˆθ = | σ ϕ    | σ , |     |     |     | (35) |
0
α
σ
| which yields | the corresponding |     |     | student | score |     |     |     |     |     |     |
| ------------ | ----------------- | --- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- |
zˆθ
|     |     |     |     |     |        | z σ −α | σ   |     |     |     |      |
| --- | --- | --- | --- | --- | ------ | ------ | --- | --- | --- | --- | ---- |
|     |     |     |     | s   | (z ,σ) | = −    | 0.  |     |     |     | (36) |
|     |     |     |     |     | ϕ σ    | σ2     |     |     |     |     |      |
This estimated score serves as a surrogate for the student’s score field and enables distribution
matching against the teacher during distillation. As the supervision signal, we employ the teacher’s
| classifier-free | guidance | (CFG) | score: |     |     |     |     |     |     |     |     |
| --------------- | -------- | ----- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
(37)
|     |     |     | ˜s = | (1+w)s | (z  | ,σ,c )−ws | (z  | ,σ,c | ),  |     |     |
| --- | --- | --- | ---- | ------ | --- | --------- | --- | ---- | --- | --- | --- |
|     |     |     | T    |        | T σ | pos       | T σ | neg  |     |     |     |
where s (·,·,c) denotes the conditional teacher score, c and c are positive and negative prompt
|     | T   |     |     |     |     | pos | neg |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
embeddings, and w > 0 is the CFG guidance weight (we use w matched to the teacher’s deployment
value). Distilling the CFG-enhanced teacher score enables the student to inherit both the teacher’s
generation quality and guided sampling behavior. Moreover, the discrepancy between positive
and negative conditioning maintains a non-vanishing optimization signal even when the student
approaches the unguided teacher distribution, mitigating optimization stagnation.
To align the student distribution p with the teacher distribution p , we minimize the forward
|     |     |     |     | θ   |     |     |     |     | T   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
KL divergence ). Since the student distribution is implicit, directly optimizing the KL
|     | D   | (p ∥p |     |     |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | KL  | θ T   |     |     |     |     |     |     |     |     |     |
objective is intractable. Using score-function identities, its gradient can be expressed as
|     |     |     |     |     | (cid:20) |     |     | ∂zθ(cid:21) |     |     |     |
| --- | --- | --- | --- | --- | -------- | --- | --- | ----------- | --- | --- | --- |
∂z
|     |     | ∇   | L     | = E | ω(σ)(˜s | −s  | (z ,σ)) | σ      | 0 , |     | (38) |
| --- | --- | --- | ----- | --- | ------- | --- | ------- | ------ | --- | --- | ---- |
|     |     |     | θ DMD | zθ  |         | T   | ϕ σ     |        |     |     |      |
|     |     |     |       |     | 0 ,ϵ,σ  |     |         | ∂zθ ∂θ |     |     |      |
0
where is a noise-dependent weighting factor. Consequently, the DMD gradient estimator
ω(σ)
encourages the student score field to match the teacher score field, thereby aligning the student
| distribution | with the | teacher | distribution. |     |     |     |     |     |     |     |     |
| ------------ | -------- | ------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Consistent with degradation phenomena reported in prior distillation literature, applying DMD to
embodied world models can exhibit several failure modes during development: prolonged training
tends toward instability and mode collapse, producing repetitive or distorted generations;
the distilled generator can show a motion diminution effect, favoring conservative trajectory
updates and underestimating agent dynamics; and can appear, where
|     |     |     |     |     |     | visual | homogenization |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | -------------- | --- | --- | --- | --- |
scene diversity gradually decreases and backgrounds converge toward simplified textures. These
observations—qualitative in our development process rather than quantitatively benchmarked here—
suggest that distribution matching alone is insufficient to fully preserve the temporal dynamics and
geometric fidelity of the teacher’s trajectories, motivating the additional regularization strategies
| introduced  | in the following |     | sections. |         |           |          |     |          |               |            |     |
| ----------- | ---------------- | --- | --------- | ------- | --------- | -------- | --- | -------- | ------------- | ---------- | --- |
|             |                  |     | To        | further | stabilize | training | and | preserve | the teacher’s | generation |     |
| Consistency | Distillation.    |     |           |         |           |          |     |          |               |            |     |
trajectory, we introduce a continuous-time consistency objective based on consistency models
55

(CM) [111–113]. While DMD aligns the student with the teacher at the distribution level, CM
additionally enforces trajectory consistency by encouraging the student prediction at a noisy state
to match the teacher prediction at a neighboring point along the teacher ODE trajectory. This
regularization improves training stability and helps preserve fine-grained temporal and structural
details.
Given a noisy sample , we first construct its neighboring state on the teacher ODE trajectory
z
σn+1
| using a | single  | Euler | step:   |          |        |         |          |     |     |      |
| ------- | ------- | ----- | ------- | -------- | ------ | ------- | -------- | --- | --- | ---- |
|         |         |       | zˆ      | = z      | +(σ −σ | )V (z   | ,σ       | ),  |     | (39) |
|         |         |       | σn      | σn+1     | n      | n+1 tea | σn+1 n+1 |     |     |      |
| where   | denotes | the   | teacher | velocity | field. |         |          |     |     |      |
V tea
| The consistency |     | objective | is then  | defined   | as             |          |         |                 |     |      |
| --------------- | --- | --------- | -------- | --------- | -------------- | -------- | ------- | --------------- | --- | ---- |
|                 |     |           |          | (cid:104) |                |          |         | (cid:105)       |     |      |
|                 |     |           | E        |           | (cid:13)       |          |         | (cid:13) 2      |     | (40) |
|                 |     |           | L =      | λ(σ       | ) (cid:13)f (z | ,σ       | )−f (zˆ | ,σ ) (cid:13) , |     |      |
|                 |     |           | CM zσn+1 | ,n        | n θ            | σn+1 n+1 | tea σn  | n 2             |     |      |
where and denote the student and frozen teacher models, respectively. Optimizing
| f   |     | f   |     |     |     |     |     |     |     | L   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | θ   | tea |     |     |     |     |     |     |     | CM  |
enables the student to approximate the teacher’s multi-step generation trajectory with significantly
| fewer sampling |     | steps | while maintaining |     | high fidelity. |     |     |     |     |     |
| -------------- | --- | ----- | ----------------- | --- | -------------- | --- | --- | --- | --- | --- |
Hybrid Objective. Our final training objective integrates the strengths of both distributional
alignment and trajectory consistency. Specifically, we jointly optimize the consistency objective and
| the DMD | score-matching |     | objective: |     |        |           |     |     |     |      |
| ------- | -------------- | --- | ---------- | --- | ------ | --------- | --- | --- | --- | ---- |
|         |                |     |            | L   | = L +λ | L         | ,   |     |     | (41) |
|         |                |     |            |     | CM     | score DMD |     |     |     |      |
where balances the two terms. This hybrid formulation creates a synergistic effect:
| λ   |       |     |     |     |     |     |     |     |     | L   |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | score |     |     |     |     |     |     |     |     | CM  |
stabilizes the distillation process by anchoring the student to the teacher’s trajectory and preserving
structural integrity, while L leverages CFG-guided teacher supervision to improve generation
DMD
| fidelity | and perceptual |     | quality. |     |     |     |     |     |     |     |
| -------- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
Qualitative Results on PAI-Bench. Fig. 15 presents qualitative comparisons on the PAI-Bench
benchmarkundertheTI2Vsetting. Despiterequiringonlyfourinferencesteps, thedistilledgenerator
qualitatively reproduces much of the teacher’s spatial structure, motion dynamics, and physical
interactions. Fine-grained scene details and coherent object trajectories largely persist, and dynamic
agents exhibit stable and realistic motions; we leave quantitative comparison against the teacher
(e.g., FVD, success-rate parity on downstream embodied benchmarks) to future work.
Compared with the original teacher sampling process, the distilled model achieves comparable visual
qualityandtemporalconsistencywithsubstantiallyreducedsamplingcost. Theseresultsdemonstrate
that the proposed distillation framework effectively transfers both distributional knowledge and
trajectory dynamics from the teacher model, enabling high-fidelity embodied video generation with
| efficient | 4-step         | inference. |           |              |     |     |     |     |     |     |
| --------- | -------------- | ---------- | --------- | ------------ | --- | --- | --- | --- | --- | --- |
| 5.3.2     | Hardware-Aware |            | Inference | Optimization |     |     |     |     |     |     |
Low-Latency Generation on Cloud Service Platforms. This aims to achieve low-latency and rapid
acquisitionofgeneratedvideodataoncloudserviceplatformstomeetuserdemandforfastinteractive
| experience     | in  | embodied  | scenarios.    |     |       |            |           |                |           |     |
| -------------- | --- | --------- | ------------- | --- | ----- | ---------- | --------- | -------------- | --------- | --- |
|                |     |           |               |     | While | the Kairos | DiT model | has a moderate | parameter |     |
| Mixed-Parallel |     | Inference | Optimization. |     |       |            |           |                |           |     |
count, it exhibits extremely long input sequence lengths in each attention block. We adopt a
56

parallel strategy centered on sequence parallelism and supplemented by tensor parallelism. We
further incorporate design insights from Megatron-LM Sequence Parallelism and DeepSpeed-Ulysses
Sequence Parallelism, and propose a customized hybrid parallelism scheme tailored to our model
architecture:
• Sliding-Window Attention Block. UsingUlyssessequenceparallelism,eachGPUmaintains
the full weights, and the input is split along the sequence dimension. Data synchronization
between GPUs is achieved via All-To-All communication, with each GPU only responsible for
|     | attention | computation | for | its assigned | heads. |     |     |     |     |     |
| --- | --------- | ----------- | --- | ------------ | ------ | --- | --- | --- | --- | --- |
• Cross-Attention Block. Adopting the basic Sequence Parallel method. Since the context
information of the attention KV is limited, the results can be precomputed and cached in full
on each GPU. We only split the query sequence along the sequence dimension, enabling each
GPU to compute attention using its local query fragment and the global full key–value (KV)
|     | pairs. | The results | are then | aggregated | via All-Gather. |     |     |     |     |     |
| --- | ------ | ----------- | -------- | ---------- | --------------- | --- | --- | --- | --- | --- |
• Gated DeltaNet. Adopting a modified Tensor Parallel method. The weights are split by
head and distributed across different GPUs. Each GPU receives the full input sequence but
processes attention computation in micro-batches to reduce memory usage.
• The VAE decoder divides the video into multiple segments along the timeline
|     | VAE          | Decoder. |          |             |        |                 |     |     |     |     |
| --- | ------------ | -------- | -------- | ----------- | ------ | --------------- | --- | --- | --- | --- |
|     | and executes | these    | segments | in parallel | across | different GPUs. |     |     |     |     |
DiT-Cache Optimization. TeaCache acts as a dedicated optimization accelerator for the Kairos
DiT. It reuses calculation results correlated with time steps, which significantly reduces inference
latency and GPU memory footprint, thus improving overall inference efficiency without altering the
model structure.
|             |     |            |     |                      |     | Torch.compile | directly | accelerates |     | neural |
| ----------- | --- | ---------- | --- | -------------------- | --- | ------------- | -------- | ----------- | --- | ------ |
| Compilation |     | and Kernel |     | Fusion Optimization. |     |               |          |             |     |        |
network training and inference by automatically applying graph optimizations, kernel fusion, and
hardware-specific optimizations. In addition, we implement a set of dedicated fusion operators to
| improve | performance. |     |     |     |     |     |     |     |     |     |
| ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Cost-EffectiveComputationonConsumer-GradeDevices. Thisaimstoenablecost-effectiveinference
computing on consumer-grade low-memory computing devices to meet the prototype development
| and | usage needs | of individual |     | developers. |     |     |     |     |     |     |
| --- | ----------- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
Low-Precision Computing Optimization (FP8). We apply quantization to the attention layers
but not to linear layers. This mainly involves the following technical points:
|     | •   |               |     | Keep query | (Q) and | key (K) in | INT8 or | INT4 | for faster | QK  |
| --- | --- | ------------- | --- | ---------- | ------- | ---------- | ------- | ---- | ---------- | --- |
|     | Q/K | in INT8/INT4. |     |            |         |            |         |      |            |     |
computation, while ensuring their outputs match the dynamic range of FP8 for the subsequent
|     | PV MatMul. |     |     |     |     |     |     |     |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
• PV MatMul (P ·V) in FP8. Quantize the attention weight matrix P (after softmax) and
the value matrix V to FP8, leveraging hardware-accelerated FP8 Tensor Core instructions.
• Smooth Q by computing Q = Q−mean(Q) (channel-wise mean subtraction) to narrow the
value distribution, improving the precision of INT4/INT8 quantization.
|     | •          |            |     |              |     | Finer | granularity | (16× | smaller | than |
| --- | ---------- | ---------- | --- | ------------ | --- | ----- | ----------- | ---- | ------- | ---- |
|     | Per-thread | / per-warp |     | quantization | for | Q/K.  |             |      |         |      |
per-block) boosts quantization precision without extra overhead, critical for FP8 downstream
computation.
57

Hardware-Aware Memory Optimization. Due to the stringent memory capacity constraints
inherent to consumer-grade graphics hardware, Kairos implements specialized low-level architectural
optimizations to drastically compress the runtime memory footprint:
• Tiled Gated DeltaNet with Streaming Access. Beyond conventional intra-GPU tensor
parallelization across attention heads, we introduce an intra-sequence batching and tiling
mechanism tailored for long-horizon tokens. By deploying a Tile-Based Computation and
Streaming Access paradigm, the network partitions extensive sequence dimensions into discrete,
highly localized blocks (tiles). Queries (Q), Keys (K), and Values (V) are subsequently
processed in a synchronized streaming pipeline. This strategy maximally overlaps hardware
tensor computations with asynchronous memory transactions, effectively concealing DRAM
access latency and avoiding out-of-memory (OOM) triggers during long-horizon generation.
• Weight-Only INT4 Text Encoder Quantization. To mitigate the massive memory
overheadimposedbytextconditioning, thetextencoderutilizesanaggressiveINT4weight-only
quantization protocol. By preserving high-precision activations while compressing stationary
model weights to 4-bit representations, this scheme maximizes computational throughput
and drastically reduces structural memory allocation. Empirically, this design facilitates
sub-millisecond keyword grounding with negligible semantic accuracy degradation, making
high-fidelity world-action generation highly viable on standard edge-computing hardware.
5.3.3 Efficiency Comparison
We tested the performance of the current model on chips with varying architectures and types, as
shown in the following tables. Experimental results show that Kairos achieves strong generation
performance on both professional server GPUs and consumer-grade GPUs.
Table 4 Latency Comparison on Various Hardware Platforms, tested on the Kairos-4B-robot 480P (5s)
distillation model.
GPU Resolution Memory (GB) 1 GPU (s) 4 GPUs (s)
NVIDIA A800 480P 23.5 11.7 3.0
NVIDIA RTX5090 480P 13.9 11.4 5.7
Table 4 reports latency comparisons on various hardware platforms. These results confirm that our
model maintains robust generation performance on both professional and consumer-grade GPUs,
while its efficient memory utilization supports the generation of longer videos and higher-resolution
visual content. Notably, 480P video generation on the NVIDIA A800 reaches real-time throughput
under the 4-GPU setting.
Table 5 Latency Comparison on Various Models. The evaluation was conducted in TI2V mode, with a video
resolution of 720P and a duration of 5 seconds.
Model Memory (GB) Complexity (PFlops) 1 GPU (s) 4 GPUs (s)
Lingbot-28B [35] 46.1 347.4 5525 1436
Cosmos-Predict2.5-14B [3] 70.2 156.5 2526 687
Wan2.2-5B [82] 23.4 16.6 201 85
Kairos-4B 23.5 2.3 43 9
58

To further contextualize these findings, we conducted performance tests to evaluate performance
discrepancies among different models under identical configurations, as presented in Table 5. The
table compares the memory usage, computational complexity, and inference latency of four models on
an NVIDIA A800 server. Among them, Kairos-4B demonstrates outstanding efficiency: it consumes
only23.5GBofmemory(comparabletothelightweightWan2.2-5B),boaststhelowestcomputational
complexity (2.3 PFlops), and achieves the fastest inference speeds—43 seconds on 1 GPU and 9
seconds on 4 GPUs—far outperforming Lingbot-28B, Cosmos-Predict2.5-14B, and Wan2.2-5B across
| all evaluated | metrics. |     |     |     |     |     |     |
| ------------- | -------- | --- | --- | --- | --- | --- | --- |
To eliminate confounding effects from other components in these models, we tested the performance
differences of the single-step DiT model across multiple resolutions and various video generation
durations, as shown in Figure 3 (b). We can clearly observe the time cost (inference latency) of
four models across different resolutions and video durations, which directly reflects the performance
| advantages of | Kairos-4B: |        |          |            |           |              |              |
| ------------- | ---------- | ------ | -------- | ---------- | --------- | ------------ | ------------ |
| •             |            |        |          |            | Under all | combinations | of 480P/720P |
| The Lowest    | Latency    | across | All Test | Scenarios. |           |              |              |
resolutions and 5s/10s/15s durations, Kairos-4B consistently achieves the lowest latency,
| outperforming | all | competing | models. |     |     |     |     |
| ------------- | --- | --------- | ------- | --- | --- | --- | --- |
• Orders-of-Magnitude Speedup over Larger Models. Compared to Cosmos-Predict2.5-
14B, Kairos-4B achieves a 28×–85× latency reduction. Even against the smaller Cosmos-
Predict2.5-2B model, it maintains a performance advantage of to 23×, validating the
6×
| effectiveness | of our | optimization | strategies. |     |     |     |     |
| ------------- | ------ | ------------ | ----------- | --- | --- | --- | --- |
• Superior Efficiency over Similar-Parameter Competitors. Relative to Wan2.2-5B,
Kairos-4B delivers a 2.5× to 3.7× speedup, demonstrating higher computational efficiency
| despite | its smaller | parameter | scale. |     |     |     |     |
| ------- | ----------- | --------- | ------ | --- | --- | --- | --- |
• Stable Scalability under Increasing Workloads. As resolution and duration rise (from
480P 5s to 720P 15s), other models show exponential latency growth, while Kairos-4B scales
linearly with increased workload, making it highly suitable for long-duration, high-resolution
| video generation. |       |            |     |     |     |     |     |
| ----------------- | ----- | ---------- | --- | --- | --- | --- | --- |
| 5.4 Inference     | Modes | for Kairos |     |     |     |     |     |
Kairos supports multiple inference modes because different Physical AI use cases require different
trade-offs between visual fidelity, action relevance, latency, and compute cost.
|             |               | Kairos | generates | future video | observations | conditioned | on instruction, |
| ----------- | ------------- | ------ | --------- | ------------ | ------------ | ----------- | --------------- |
| Full Visual | Rollout Mode. |        |           |              |              |             |                 |
image context, camera control, or other signals. Useful for simulation, data generation, qualitative
inspection, failure analysis, prompt self-alignment, and long-horizon state probing. It is valuable
when the objective is to inspect whether the model preserves physical plausibility, object permanence,
taskprogress, andtemporalcoherence—makingthemodel’simaginedfuturevisibleandinterpretable.
It is, however, the most expensive mode because it requires future visual token generation and VAE
decoding, and is less suitable for low-latency control loops where explicit video materialization is
unnecessary.
|                |     |            |       | Kairos can | evaluate | imagined futures | in latent or |
| -------------- | --- | ---------- | ----- | ---------- | -------- | ---------------- | ------------ |
| Latent Rollout | and | Evaluation | Mode. |            |          |                  |              |
compressed form without always producing full-resolution video. Useful for candidate ranking,
risk estimation, trajectory evaluation, and future policy filtering. It offers a compromise between
interpretability and efficiency. This mode is especially relevant for future regret-aware deployment
59

because many decisions do not require photorealistic rendering: a policy evaluator may only need to
know whether an action is likely to succeed, collide, slip, or require recovery.
|             |            |       | Central | to the World-Action | Model design. | During training, |
| ----------- | ---------- | ----- | ------- | ------------------- | ------------- | ---------------- |
| Action-Only | Prediction | Mode. |         |                     |               |                  |
Kairos jointly learns future visual dynamics and future action trajectories; during deployment, the
future video branch can be disabled and only future action tokens are generated. Since action
tokens are much fewer than video tokens, this is expected to reduce both attention and diffusion
cost while retaining the benefits of jointly learned world dynamics; quantitative latency savings for
the action-only path are not yet reported in this work. This asymmetric design is, in our view, the
| clearest path | toward | deployment-ready | world-action | modeling. |     |     |
| ------------- | ------ | ---------------- | ------------ | --------- | --- | --- |
Proxy Self-Alignment Mode. Uses the rollout–evaluation–refinement loop for prompt rewriting,
generation refinement, and candidate selection. This is the current validated self-improvement
mechanism in Kairos. It demonstrates that Kairos can generate candidates, evaluate outputs, and
refine inputs without direct human intervention. It does not yet demonstrate autonomous robot
policy self-improvement.
|        |             |       | The   | future goal: Kairos | would receive | real observations, |
| ------ | ----------- | ----- | ----- | ------------------- | ------------- | ------------------ |
| Future | Closed-Loop | Robot | Mode. |                     |               |                    |
maintain , generate or evaluate candidate actions, predict failure or safety risk, execute selected
Z t
actions, observe real outcomes, and update its model/evaluator/policy based on discrepancy between
| imagined        | and real rollout. | Required             | validation        | includes: |     |     |
| --------------- | ----------------- | -------------------- | ----------------- | --------- | --- | --- |
| • correlation   | between           | imagined             | and real          | rollouts; |     |     |
| • failure       | prediction        | accuracy             | before execution; |           |     |     |
| • calibration   | of                | risk and uncertainty | estimates;        |           |     |     |
| • effectiveness | of                | safety filtering;    |                   |           |     |     |
| • recovery      | success           | after predicted      | or actual         | failures; |     |     |
• measurable improvement in real policy performance from imagined experience.
The current report establishes the prerequisites for this stage; end-to-end real-robot validation of the
| items above | is positioned | as future | work. |     |     |     |
| ----------- | ------------- | --------- | ----- | --- | --- | --- |
5.5 Summary: From Fast Generation to Deployment-Aware World-Action Operation
This section reframes inference in Kairos as deployment-aware operation of control-sufficient states.
Inference is not merely the final decoding step of a generative model; it is the mechanism through
which Z becomes useful for future Physical AI. Kairos currently provides four inference-side
t
capabilities: (1) a rollout–evaluation–refinement loop; (2) Prompt Self-Alignment as a controlled
proxy; (3) timestep distillation for low-step embodied generation; (4) hardware-aware optimization
across server and consumer devices. These should be interpreted as model-side and inference-
side prerequisites for future regret-aware Physical AI. The next stage is to connect these inference
mechanismstorealrobotrollouts,failureprediction,safetyfiltering,recoverylearning,andmeasurable
policy improvement.
Thus, deployment-aware inference is regret-relevant not because faster generation directly proves
lower regret, but because low latency and efficient memory use determine whether cost-relevant
predictions can enter the observation–action–feedback loop before execution.
60

6 Evaluation Results
6.1 Evaluation Scope and Proxy-Evidence Framing
The goal of this evaluation is to assess whether Kairos learns several capabilities required for control-
sufficient world-action modeling. As argued in earlier sections, a world model for Physical AI should
not be evaluated only by visual fidelity or video-generation quality. The more important question is
whetherthemodelpreservesinformationusefulforaction: physicalplausibility,instructiongrounding,
task progress, joint world-action prediction, long-horizon state consistency, and deployment-ready
inference.
However, the current evaluation should be interpreted with a precise scope. The evaluations in
this section provide proxy evidence for regret-relevant capabilities. They do not directly measure
real-world closed-loop regret reduction. Using the notation introduced in the Introduction, the
current evaluation does not directly estimate Reg (f;g). Instead, it evaluates observable proxies for
H
quantities that would enter J
H
or J(cid:98)H : physical plausibility, instruction grounding, action prediction,
long-horizon state consistency, regret-relevant future prediction, failure-relevant reasoning, and
deployment readiness. In particular, the current evaluation does not yet establish whether imagined
rollouts are highly correlated with real robot rollouts, whether Kairos can predict failures before
execution in real environments, whether safety filtering reduces unsafe events, or whether imagined
experience improves a real robot policy. These remain central directions for future evaluation (see
Section 8.1). Table 6 summarizes the scope: each row pairs an evaluation target with the current
proxy evaluation, what it supports, and what it does not yet prove.
This organization follows the principle that current benchmarks are necessary but not sufficient. A
model that fails physical plausibility or instruction grounding is unlikely to support Physical AI; a
model that performs well on these benchmarks may have learned useful physical and semantic priors.
But the final test of a Physical AI world model is whether it reduces costly real-world mistakes.
The results below should therefore be read as evidence that Kairos establishes several model-side
prerequisites for regret-aware Physical AI.
6.2 Embodied World Model Benchmarks
Embodied world-model benchmarks evaluate whether Kairos can generate future observations that
are physically plausible, instruction-aligned, temporally coherent, and relevant to embodied scenarios.
We evaluate Kairos-robot-4B on three benchmarks—WorldModelBench-Robot [55], DreamGen
Bench [56], and PAI-Bench-Robot [114]—and complement them with human evaluation. The
results show that Kairos-robot-4B achieves strong performance across these embodied benchmarks
despite its compact 4B parameter scale. This supports the claim that Kairos learns physical and
instruction-grounded priors relevant to embodied world modeling.
6.2.1 WorldModelBench-Robot
WorldModelBench [55] is designed to assess the world modeling capability of video generation
models, particularly their ability to follow instructions and adhere to real-world physics across diverse
domains. It primarily evaluates models along two dimensions: (1) Instruction Following, which
measures whether the generated videos accurately follow the given text prompts (and image), and
(2) Future Frame Generation, which assesses whether the generated videos represent plausible future
states of the world, including adherence to physical laws and common sense reasoning. As these
capabilities are essential for embodied reasoning, we conduct our evaluation on the robotics subset
61

Table 6 ScopeofthecurrentKairosevaluation. Eachevaluationprovidesproxyevidenceforaregret-relevant
| capability; closed-loop | real-world regret | reduction | is left as future | work. |     |     |
| ----------------------- | ----------------- | --------- | ----------------- | ----- | --- | --- |
Evaluation target Current proxy evalua- What it supports What it does not yet
|     | tions |     |     |     | prove |     |
| --- | ----- | --- | --- | --- | ----- | --- |
Embodied physical WorldModelBench- Kairoslearnsphysicallyplau- Directreal-worldtasksuc-
plausibility & in- Robot, DreamGen, sible and instruction-aligned cess or failure avoidance
| struction grounding | PAI-Bench-Robot, | hu- | embodied futures |     |     |     |
| ------------------- | ---------------- | --- | ---------------- | --- | --- | --- |
man eval
Action-outcome pre- RoboTwin 2.0, LIBERO- Joint world-action modeling Fullcounterfactualvalida-
diction & embodied Plus improves manipulation and tion under matched real
| generalization |     |     | robustness |     | initial states |     |
| -------------- | --- | --- | ---------- | --- | -------------- | --- |
Interventional gen- WorldModelBench- CEDC and generation– Formal guarantees un-
eralization Robot, LIBERO-Plus prediction joint training der interventional distri-
|     | (human-centric | pretrain- | improve         | action-relevant | bution shift |     |
| --- | -------------- | --------- | --------------- | --------------- | ------------ | --- |
|     | ing and joint  | training  | representations |                 |              |     |
ablations)
Generic physical VideoPhy, PAI-Bench Kairosretainsbroadphysical Direct test of action pre-
reasoning (beyond (full), WorldModelBench andsemanticpriorsacrossdi- diction or closed-loop pol-
| embodied) | (full) |     | verse domains |     | icy |     |
| --------- | ------ | --- | ------------- | --- | --- | --- |
Long-horizon state PAI-Bench-15s Kairosbetterpreservesscene Minute-, hour-, or day-
maintenance consistency over extended scalereal-worldtaskmem-
|     |     |     | generation horizons |     | ory |     |
| --- | --- | --- | ------------------- | --- | --- | --- |
Regret-relevant fu- Regret-Relevant Cases Evidence that Kairos pre- Quantitativeregretreduc-
ture prediction serves goal-conditioned con- tion or closed-loop action-
|     |     |     | trolinformationinembodied |     | cost improvement |     |
| --- | --- | --- | ------------------------- | --- | ---------------- | --- |
rollouts
Deployment- Latency comparison on Kairos offers a favorable Real-time closed-loop
oriented efficiency A800/RTX5090 and efficiency–capability trade- robot control across all
|     | against | Lingbot-28B, | off for future | deployment | hardware | and tasks |
| --- | ------- | ------------ | -------------- | ---------- | -------- | --------- |
Cosmos-Predict2.5-14B,
Wan2.2-5B
of WorldModelBench.
As shown in Table 7, Kairos-4B achieves the highest total score of 9.30 on the WorldModelBench
robot subset, outperforming all baselines. It obtains the best Instruction Following score (2.36),
matchingthe16BCosmos3-Nano,whichindicatesitsstronglanguagegroundingcapability. InPhysics
Adherence, Kairos-4B reaches perfect scores in Newtonian mechanics, fluid dynamics, and gravity
(1.00 each), achieving a high overall Physics Adherence score of 4.96. Additionally, it demonstrates
robust Common Sense reasoning, highlighted by perfect temporal quality (1.00). Overall, these
results show that Kairos-4B delivers leading physical modeling and reasoning capabilities while
remaining highly parameter-efficient. Figure 16 presents qualitative results of selected samples from
| the WorldModelBench | robot subset. |     |     |     |     |     |
| ------------------- | ------------- | --- | --- | --- | --- | --- |
| 6.2.2 DreamGen      | Bench         |     |     |     |     |     |
DreamGen Bench [56] is a video generation benchmark specifically designed for robotics, aiming
to systematically measure the generalization capability of Video World Models on specific robotic
embodiments. The benchmark primarily evaluates two core metrics: Instruction Following, which
assesses whether generated videos strictly adhere to given task instructions; and Physics Adherence,
62

Table 7 Evaluation on WorldModelBench Robot Set. For each column, the highest score is bolded. Models
marked with * indicate results reproduced by our team.
Instruction
Physics Adherence Common Sense Total
Model Param Following
Score
Overall Newton Deform. Fluid Penetr. Grav. Overall Frame Temp.
Lingbot*[35] 28B 2.14 1.00 0.96 1.00 0.96 1.00 4.92 1.00 0.98 9.04
Cosmos3-Nano*[52] 16B 2.36 1.00 0.98 1.00 0.98 1.00 4.96 0.98 0.96 9.26
Abot-Physworld*[115] 14B 2.10 1.00 0.92 1.00 0.96 1.00 4.88 1.00 0.98 8.96
Cosmos-Predict2.5*[3] 14B 2.14 1.00 0.92 1.00 0.94 1.00 4.86 1.00 0.94 8.94
Wan2.2*[82] 5B 2.04 1.00 0.78 1.00 0.86 0.98 4.62 0.96 0.90 8.52
Cosmos-Predict2.5*[3] 2B 2.14 1.00 0.98 1.00 0.96 1.00 4.94 0.98 0.98 9.04
GigaWorld-0*[116] 2B 1.50 1.00 0.98 1.00 1.00 1.00 4.98 0.98 1.00 8.46
Kairos 4B 2.36 1.00 0.98 1.00 0.98 1.00 4.96 0.98 1.00 9.30
Figure 16 Kairos samples on the WordelModelBench robot subset.
which evaluates whether generated videos conform to real-world physical laws. DreamGen Bench
quantifies the generalization ability of video generation models by testing their performance across
three key dimensions: novel object manipulation, novel behavior execution, and novel environment
adaptation. Research results indicate that models achieving higher scores on this benchmark also
demonstrate better performance in downstream robot policy training when using their generated
synthetic data, showing a significant positive correlation between the two.
Table 8 presents the evaluation results of Kairos-4B on the DreamGen Bench. Our model ranks first
in both Average Physical Adherence (AVG_PA, 0.538) and the overall Average Score (AVG_Score,
0.618), while achieving a highly competitive Average Instruction Following (AVG_IF, 0.698), second
only to the 14B Wan2.2 (0.703). The leading AVG_PA score reflects strong physical-plausibility
modeling under this benchmark, and its strong AVG_IF reflects reliable instruction-following ability.
Despite having only 4B parameters, Kairos-4B attains the best overall performance, outperforming
substantiallylargercompetitors,whichhighlightsitsstrongperformanceandgeneralizationcapability.
Figure 17 displays selected visualization samples from our DreamGen test set.
63

Table 8 Evaluation on DreamGen Bench. For each column, the highest score is bolded. Models marked
with * indicate results reproduced by our team.
GR1-Object GR1-Behavior GR1-Env
Method Param AVG_PA AVG_IF AVG_Score
Qwen-IF PA Qwen-IF PA Qwen-IF PA
Cosmos-Predict2.5*[3] 14B 0.260 0.515 0.553 0.418 0.621 0.553 0.495 0.478 0.487
Cosmos-Predict2.5*[3] 2B 0.840 0.374 0.277 0.375 0.586 0.507 0.419 0.568 0.494
GigaWorld-0[116] 2B 0.540 0.481 0.638 0.446 0.586 0.529 0.485 0.588 0.537
Wan2.2*[82] 5B 0.420 0.458 0.553 0.180 0.690 0.303 0.314 0.554 0.434
Wan2.2[82] 14B 0.780 0.531 0.570 0.477 0.760 0.549 0.519 0.703 0.611
Cosmos3-Nano*[52] 16B 0.460 0.509 0.468 0.455 0.793 0.552 0.505 0.574 0.540
ABot-PhysWorld*[115] 14B 0.400 0.493 0.404 0.431 0.414 0.528 0.484 0.434 0.459
Lingbot*[35] 28B 0.400 0.545 0.617 0.340 0.690 0.513 0.466 0.569 0.518
Kairos 4B 0.660 0.544 0.745 0.489 0.690 0.581 0.538 0.698 0.618
Figure 17 Kairos samples on the DreamGen dataset.
6.2.3 PAI-Bench-Robot
PAI-Bench [114] is a benchmark designed to evaluate the visual quality and physical plausibility of
generated videos in real-world physical AI scenarios. The benchmark reports two primary metrics:
Domain Score and Quality Score. The Domain Score evaluates the model’s capability on domain-
specific physical AI tasks, while the Quality Score measures the perceptual quality of generated
videos. The Quality Score is computed using eight evaluation metrics adapted from VBench [117].
Meanwhile, the Domain Score is obtained through a VQA-based evaluation protocol spanning seven
domains, including av, common, human, industry, misc, physics, and robotics. The final Overall
Score is defined as the average of the Domain Score and the Quality Score. To specifically assess the
model’s capability in embodied scenarios, we conduct quantitative evaluation on the Robotics subset
of PAI-Bench.
Table 9 presents the benchmark results between Kairos-4B and baseline models under the PAI-Bench
TI2V evaluation mode. Among small-scale models (<10B), our model achieves the best overall
performance, ranking first in both Domain Score (88.59) and Overall Score (82.57). Notably, using
only 4B parameters, Kairos-4B matches or surpasses several large-scale (≥10B) baselines—it remains
essentially on par with the 16B Cosmos3-Nano (82.62 vs. 82.57) and outperforms 14B models such
64

Table 9 Evaluation on the PAI-Bench-Robot set. For each model group, the highest score in each column is
| bolded. | Models | marked | with * | indicate | results     | reproduced | by our        | team. |         |       |                |
| ------- | ------ | ------ | ------ | -------- | ----------- | ---------- | ------------- | ----- | ------- | ----- | -------------- |
|         |        |        |        |          |             |            | QualityScore  |       |         |       | Domain Overall |
| Model   |        |        | Param  |          |             |            |               |       |         |       |                |
|         |        |        |        |          |             |            |               |       |         |       | Score Score    |
|         |        |        |        | i2v-bg   | i2v-s       | aes        | img bg-con    | mot   | sub-con | o-con |                |
|         |        |        |        |          | Large-scale |            | Models (≥10B) |       |         |       |                |
Lingbot*[35] 28B 97.7 50.2 67.1 93.1 98.9 91.2 19.8 82.98 79.97
97.6
Cosmos3-Nano*[52] 16B 98.2 95.3 48.4 73.0 92.1 99.3 91.7 19.7 88.04 82.62
Abot-Physworld[115] 14B 97.8 95.0 46.2 69.1 93.7 99.2 94.1 19.3 87.85 82.32
Abot-Physworld+DPO[115] 14B 97.7 94.8 46.7 69.2 93.7 99.1 93.6 19.4 93.06 84.91
Cosmos-Predict2.5*[3] 14B 94.3 92.2 48.0 72.0 93.1 99.1 91.3 19.2 82.60 79.40
Wan2.5[118] / 94.4 94.3 54.8 64.6 89.9 96.2 87.8 21.9 86.44 80.96
Veo3.1[119] / 93.2 96.1 54.6 72.4 92.2 97.1 91.5 22.1 83.50 80.45
Wan2.1[82] 14B 97.5 94.5 47.2 71.2 93.2 99.2 91.9 19.2 83.91 80.32
WoW-wan[120] 14B 96.1 92.9 46.6 70.3 93.0 98.6 91.5 19.4 83.01 79.53
Sorav2Pro[121] / 95.1 92.9 53.2 69.6 92.9 97.0 91.6 22.0 76.26 76.52
|             |     |     |     |      | Small-scale |      | Models (<10B) |      |      |      |             |
| ----------- | --- | --- | --- | ---- | ----------- | ---- | ------------- | ---- | ---- | ---- | ----------- |
| Wan2.2*[82] |     |     | 5B  |      |             |      | 70.6 92.3     |      | 90.8 |      | 80.17 78.63 |
|             |     |     |     | 97.8 | 97.4        | 49.3 |               | 99.1 |      | 19.4 |             |
UnifoLM-WMA-0[122] 3B 96.4 94.0 45.5 65.6 94.2 98.8 94.1 18.8 66.93 71.43
Cosmos-Predict2.5*[3] 2B 93.7 91.2 49.3 74.1 92.0 99.1 90.2 19.1 80.44 78.26
GigaWorld-0[116] 2B 96.7 96.1 47.6 65.1 92.2 99.1 91.1 19.4 85.83 80.87
Kairos 4B 97.8 94.8 46.8 69.0 93.2 99.1 93.6 18.1 88.59 82.57
as Wan2.1 and the non-DPO Cosmos-Predict2.5. These results indicate that our model not only
generates high-quality videos but also delivers strong physical modeling and instruction-following
capability with far fewer parameters. Beyond quantitative analysis, qualitative evaluation offers
more intuitive insights into the model’s generation behavior. Figure 18 showcases visualization
samples from the PAI-Bench-Robot test set, illustrating the model’s generation quality across diverse
scenarios.
| 6.2.4 | Human | Evaluation |     |     |     |     |     |     |     |     |     |
| ----- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Video generation involves complex physical causal logic and semantic consistency, and existing
objective metrics cannot fully and accurately capture human perceptions of visual quality and
semantic coherence. Human evaluation directly assesses a model’s performance in instruction
following, adherence to physical laws, and content coherence, effectively compensating for the
limitations of automated evaluation. Therefore, introducing human evaluation is a critical step in
ensuring that generated outputs align with human preferences and possess practical application
value. To this end, we recruited 10 volunteers to conduct subjective evaluations on the complete test
sets of PAI-Bench, WorldModelBench, and DreamGen for five models: Kairos-4B, Cosmos-Predict2.5
(2B/14B),Wan2.2-5B,andLingbot-28B.Toensurefairness, allmodelswereanonymizedwithrandom
identifiers, and volunteers ranked the outputs without knowing the model identities. The final
subjective evaluation results were obtained by averaging the rankings across different volunteers.
Figure 19 presents the pairwise win rates against the strongest baselines on each benchmark (selected
comparisons; full pairwise tables for the remaining baselines are deferred for space):
• PAI-Bench robot subset. Despite a ∼4–7× parameter gap, Kairos-4B reaches a 60.2%
win rate against the 14B Cosmos-Predict2.5 and 49.1% against the 28B Lingbot; it attains a
|     | dominant        | 74.1% | win rate | against | Wan     | 2.2-5B.   |          |       |     |     |                  |
| --- | --------------- | ----- | -------- | ------- | ------- | --------- | -------- | ----- | --- | --- | ---------------- |
|     | •               |       |          |         |         | Kairos-4B | achieves | 86.7% | vs. | Wan | 2.2-5B and 74.7% |
|     | WorldModelBench |       | robot    |         | subset. |           |          |       |     |     |                  |
65

|     |     | Figure | 18 Kairos | samples on | the PAI-Bench-Robot |     | dataset. |     |
| --- | --- | ------ | --------- | ---------- | ------------------- | --- | -------- | --- |
vs. Lingbot-28B; against Cosmos-Predict2.5-14B it leads with a 65.0% win rate, suggesting
| stronger | world-model |     | consistency. |     |     |     |     |     |
| -------- | ----------- | --- | ------------ | --- | --- | --- | --- | --- |
• Kairos-4B wins 88.8% of comparisons against Wan 2.2-5B and 47.6% against
DreamGen.
| Cosmos-Predict2.5-14B—competitive |                   |               |      | given       | the 3.5× | parameter         | gap.             |      |
| --------------------------------- | ----------------- | ------------- | ---- | ----------- | -------- | ----------------- | ---------------- | ---- |
| 6.2.5                             | Ablation Studies: | Human-Centric |      | Scaling and | VLM      | Selection         |                  |      |
|                                   |                   |               |      | To          | validate | the effectiveness | of human-centric | data |
| Effect                            | of Human-Centric  |               | Data | Scaling.    |          |                   |                  |      |
scalingonourembodiedworldmodel, weperformablationsonWorldModelBench-Robot, withresults
summarized in Table 10. Starting from a baseline trained without scaled-up human-centric data and
adopting Qwen2.5-VL-7B-Instruct [123] as the VLM encoder, we inject large-scale human-centric
data into pre-training. This substantially improves instruction following (2.10 2.33), leading to
→
a clear gain in the overall benchmark score (9.08 → 9.25). This improvement reflects a stronger
world-modeling capability: it follows instructions more accurately and generates dynamics that are
better aligned with real-world interaction. We attribute this to the richer behavioral priors carried
by human-centric data, which enhance the world model’s generalization across diverse behaviors,
66

|           |                 |             | Figure     | 19 Human evaluation | results. |
| --------- | --------------- | ----------- | ---------- | ------------------- | -------- |
| resulting | in more correct | instruction | following. |                     |          |
Effect of Understanding. Building on the large-scale human-centric pre-training data, we further
upgrade the VLM encoder from Qwen2.5-VL-7B-Instruct to Qwen3.5-2B [60]. Notably, although
Qwen3.5-2B has fewer parameters, it exhibits stronger multimodal understanding capability (as
shown in Table 11). This upgrade yields further gains in both instruction following (2.33 → 2.36)
and total score (9.25 → 9.30). A stronger VLM enables the world model to better interpret and
align the language instruction and the visual context of the initial frame, leading to more accurate
| instruction | grounding | and higher-quality |            | future predictions. |     |
| ----------- | --------- | ------------------ | ---------- | ------------------- | --- |
| 6.3 World   | Action    | Model              | Benchmarks |                     |     |
We finetuned Kairos and evaluated it on two main-stream benchmarks: LIBERO-Plus and RoboTwin
2.0. ResultsshowthatKairosachievedhighlycompetitiveperformancewithonlyminimaldownstream
finetuning.
| 6.3.1 RoboTwin | 2.0 |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- |
RoboTwin 2.0 [57] is a challenging benchmark for bimanual robotic manipulation, comprising over 50
tasks that require precise coordination between two robotic arms. To comprehensively evaluate our
method, we compare against two representative paradigms for embodied control. The first category
consists of Vision-Language-Action (VLA) models, including π , X-VLA, π , StarVLA, Abot-M0,
0 0.5
LingBot-VLAandG0.5. Thesemethodstypicallylearnadirectmappingfromvisualobservationsand
67

Table 10 Ablation study on human-centric data Table 11 Vision-language capability comparison
| scaling | and VLM | selection |     |     |     |     | referred | from | [123] | [124]. |     |
| ------- | ------- | --------- | --- | --- | --- | --- | -------- | ---- | ----- | ------ | --- |
Human-Centric StrongerVLM Instruction Total Benchmark Qwen2.5-VL-7B Qwen3.5-2B
|     | Scaling | Encoder |     | Following↑ |     | Score↑ |                  |     |       |      |           |
| --- | ------- | ------- | --- | ---------- | --- | ------ | ---------------- | --- | ----- | ---- | --------- |
|     |         |         |     |            |     |        | MMMU[125]        |     |       | 58.6 | 64.2/64.2 |
|     |         |         |     | 2.10       |     | 9.08   |                  |     |       |      |           |
|     |         |         |     |            |     |        | MMMU-Pro[126]    |     |       | 38.3 | 50.3/47.7 |
|     | ✓       |         |     | 2.33       |     | 9.25   |                  |     |       |      |           |
|     |         |         |     |            |     |        | MathVista        |     | [127] | 68.2 | 76.7/73.9 |
|     | ✓       | ✓       |     | 2.36       |     | 9.30   |                  |     | mini  |      |           |
|     |         |         |     |            |     |        | RealWorldQA[128] |     |       | 68.5 | 74.5/71.2 |
|     |         |         |     |            |     |        | MMStar[129]      |     |       | 63.9 | 71.7/68.0 |
language instructions to robot actions. The second category comprises World-Action-Model (WAM)
approaches, including JEPA-VLA, GigaWorld-Policy, Motus, LingBot-VA, Fast-WAM, Being-H0.7,
AIM, SANTS, and MotuBrain. Unlike VLA-based methods, WAM approaches explicitly model both
environment dynamics and action evolution, enabling joint prediction of future states and executable
actions for long-horizon reasoning and planning. As shown in Table 12, Kairos achieves strong and
consistent performance across the RoboTwin 2.0 benchmark. It leads on the Clean setting (96.9)
and achieves the highest average success rate (96.1), while MotuBrain attains the best Randomized
score (96.1). These results demonstrate that jointly modeling world dynamics and action evolution
can improve planning and execution for complex bimanual manipulation.
|     |     |       | Table | 12  | Results | on    | RoboTwin | 2.0        | benchmark. |         |     |
| --- | --- | ----- | ----- | --- | ------- | ----- | -------- | ---------- | ---------- | ------- | --- |
|     |     | Model |       |     |         | Clean |          | Randomized |            | Average |     |
# VLA
|     |     | π0          | [130] |       |       | 65.9 |     | 58.4 |     | 62.2 |     |
| --- | --- | ----------- | ----- | ----- | ----- | ---- | --- | ---- | --- | ---- | --- |
|     |     | X-VLA       |       | [131] |       | 72.9 |     | 72.8 |     | 72.9 |     |
|     |     | π0.5        | [132] |       |       | 82.7 |     | 76.8 |     | 79.8 |     |
|     |     | starVLA     |       | [133] |       | 88.2 |     | 88.3 |     | 88.3 |     |
|     |     | ABot-M0     |       | [134] |       | 81.2 |     | 80.4 |     | 80.8 |     |
|     |     | LingBot-VLA |       |       | [135] | 86.5 |     | 85.3 |     | 85.9 |     |
|     |     | G0.5        | [136] |       |       | 93.7 |     | 92.8 |     | 93.2 |     |
# WAM
|     |     | JEPA-VLA         |       | [137] |       | 73.5 |     | -    |     | -    |     |
| --- | --- | ---------------- | ----- | ----- | ----- | ---- | --- | ---- | --- | ---- | --- |
|     |     | GigaWorld-Policy |       |       | [138] | 86.0 |     | 85.0 |     | 85.5 |     |
|     |     | Motus            | [139] |       |       | 88.7 |     | 87.0 |     | 87.8 |     |
|     |     | LingBot-VA       |       | [140] |       | 92.9 |     | 91.6 |     | 92.2 |     |
|     |     | Fast-WAM         |       | [62]  |       | 91.9 |     | 91.8 |     | 91.8 |     |
|     |     | Being-H0.7       |       | [141] |       | 90.2 |     | 89.6 |     | 89.8 |     |
|     |     | AIM              | [142] |       |       | 94.0 |     | 92.1 |     | 93.1 |     |
|     |     | SANTS            |       | [143] |       | 94.6 |     | 94.2 |     | 94.4 |     |
|     |     | MotuBrain        |       | [144] |       | 95.8 |     | 96.1 |     | 96.0 |     |
|     |     | Kairos           |       |       |       | 96.9 |     | 95.2 |     | 96.1 |     |
6.3.2 LIBERO-Plus
LIBERO-Plus [58] is an extended version of LIBERO. Compared with the original benchmark,
LIBERO-Plus places substantially stronger emphasis on scene-level generalization, robustness to
visual distribution shift, compositional manipulation reasoning, and long-horizon policy stability. As
shown in Table 13, Kairos achieves state-of-the-art performance after fine-tuning on LIBERO-Plus.
68

|     |     |     | Table 13 | Results on | LIBERO-Plus | benchmark. |     |     |     |
| --- | --- | --- | -------- | ---------- | ----------- | ---------- | --- | --- | --- |
Method Camera Robot Language Light Background Noise Layout Average
# VLA
| ACoT-VLA | [145] |      | 70.4 | 79.7 | 95.1 |      | 95.9 | 85.0 | 88.0 |
| -------- | ----- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|          |       | 96.6 |      |      |      | 97.1 |      |      |      |
| π [130]  |       | 61.0 | 40.8 | 63.5 | 89.3 | 84.1 | 80.1 | 76.4 | 69.4 |
0
| π [132] |     | 75.8 | 79.4 | 83.3 | 95.5 | 95.0 | 89.6 | 87.0 | 85.7 |
| ------- | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
0.5
| Being-H0.5  | [146] | -    | -    | -    | -    | -    | -    | -    | 83.1 |
| ----------- | ----- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| MINT-4B     | [147] | -    | -    | -    | -    | -    | -    | -    | 84.1 |
| VLANeXt     | [148] | 90.4 | 65.7 | 81.8 | 95.9 | 82.5 | 94.1 | 80.8 | 83.9 |
| ProGAL-VLA  | [149] | 93.2 | 71.5 | 93.6 | 86.8 | 92.3 | 74.8 | 86.7 | 85.5 |
| RoVLA       | [150] | 96.6 | 32.0 | 91.5 | 95.9 | 96.1 | 95.1 | 74.1 | 82.0 |
| OpenVLA-OFT | [151] | 92.8 | 30.3 | 85.8 | 94.9 | 93.9 | 89.3 | 77.6 | 79.6 |
| Gr00t-N1.6  | [152] | 92.6 | 33.5 | 80.1 | 93.6 | 95.4 | 93.6 | 75.0 | 79.4 |
| ABot-M0     | [153] | 60.4 | 67.9 | 86.4 | 96.2 | 91.6 | 86.4 | 82.6 | 80.5 |
# WAM
| Being-H0.7   | [141] | -    | -    | -    | -    | -    | -    | -    | 84.8 |
| ------------ | ----- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| Kairos       |       | 95.5 | 72.6 | 86.8 |      | 95.8 |      | 81.5 | 89.0 |
|              |       |      |      |      | 97.7 |      | 96.8 |      |      |
| Kairos-joint |       | 95.9 | 74.6 | 95.3 | 97.1 | 97.1 | 95.4 | 83.8 | 90.8 |
The results indicate that the model generalizes effectively to perturbed evaluation settings and
| exhibits | strong robustness |     | across diverse | environmental |     | variations. |     |     |     |
| -------- | ----------------- | --- | -------------- | ------------- | --- | ----------- | --- | --- | --- |
6.3.3 Ablation Studies: Human-Centric Pretraining and Joint World-Action Training
Effect of Embodied Human-centric Pretraining. To investigate the impact of embodied
human-centric pretraining, we compare Kairos with VideoDiT pretrained either with or without
large-scale human-centric data, while keeping all other settings unchanged. As results shown in
Table 14, incorporating human-centric data leads to a significant gain in LIBERO-Plus benchmark,
which suggests the effectiveness of native human-centric pretraining. Kairos can effectively leverage
transferable action-relevant knowledge learned from human-centric data to improve performance
on unseen tasks. More broadly, these findings highlight the potential of large-scale human-centric
data as a scalable supervision source complementary to robot trajectories, offering a promising
path toward reducing real-robot data requirements and enabling more general-purpose world action
models.
|        |          |          |               |     |                 | Building | upon | the human-centric |     |
| ------ | -------- | -------- | ------------- | --- | --------------- | -------- | ---- | ----------------- | --- |
| Effect | of Joint | Training | of Generation |     | and Prediction. |          |      |                   |     |
pretrained WAM, we further investigate the impact of Generation-Prediction joint training on action
prediction. Specifically, an ablated WAM variant optimizing only the ActionDiT is constructed,
with results shown in Table 15. Training only the ActionDiT leads to a consistent performance
degradation across LIBERO-Plus benchmarks. We attribute this degradation to the loss of world-
modeling supervision provided by the generation objective. By jointly optimizing generation and
prediction, VideoDiT learns control-relevant interaction dynamics and produces more informative
visual representations, resulting in stronger conditioning signals and improved action prediction
performance.
|        |          |           |               |     |     |             | Rather | than omitting | video |
| ------ | -------- | --------- | ------------- | --- | --- | ----------- | ------ | ------------- | ----- |
| Effect | of Joint | Denoising | of Generation |     | and | Prediction. |        |               |       |
generation during inference, we explore a variant of Kairos, denoted as Kairos-joint (see Table
13). In this configuration, future video tokens and action tokens are jointly denoised, allowing
69

Table 14 Effectofembodiedhuman-centricpretrain- Table 15 Effect of Joint Training of Generation and
| ing |       |               |      |           | Prediction |            |      |      |      |
| --- | ----- | ------------- | ---- | --------- | ---------- | ---------- | ---- | ---- | ---- |
|     | Model |               |      | Avg. Gain | Model      |            |      | Avg. | Gain |
|     | w/o   | human-centric | data | 83.0 –    | Action     | Prediction | Only | 65.8 | –    |
w/ human-centric data 89.0 +6.0 Video Generation & Action Prediction 89.0 +23.2
action prediction to actively attend to video generation at inference time. Experimental results
demonstrate that this explicit future imagination further elevates performance from 89.0 to 90.8.
This improvement highlights the distinct advantages of the joint attention mechanism in coupling
| generation |         | and prediction. |       |            |     |     |     |     |     |
| ---------- | ------- | --------------- | ----- | ---------- | --- | --- | --- | --- | --- |
| 6.4        | General | World           | Model | Benchmarks |     |     |     |     |     |
Beyond the strong embodied capabilities of our model, we further evaluate its world modeling and
physical reasoning abilities on general video generation benchmarks. In addition to the previously
introducedPAI-BenchandWorldModelBench, wealsoincludeVideoPhy[154], abenchmarkdesigned
to evaluate the physical validity and semantic consistency of generated videos, with a particular focus
on realistic entity interactions and motion dynamics. To examine temporal reasoning and consistency,
we further conduct evaluations under a long-term (15-second) generation setting, enabling assessment
across different temporal scales. For the evaluation, we select Cosmos-Predict2.5-2B/14B [3], and
| Wan2.2-5B |     | [82] as representative |     | baseline models. |     |     |     |     |     |
| --------- | --- | ---------------------- | --- | ---------------- | --- | --- | --- | --- | --- |
6.4.1 PAI-Bench
Following the same evaluation protocol as in the embodied setting, we extend the evaluation to
the full set of PAI-Bench domains, including av, physics, and other real-world scenarios. In the
TI2V setting, we compare our method with aforementioned open-source models. Quantitative
results are summarized in Table 16. With only 4B parameters, Kairos achieves an Overall Score
of 80.8—competitive with Cosmos-Predict2.5-2B/14B (both 81.0) while substantially smaller, and
ahead of other open-source baselines at comparable scale. In particular, Kairos achieves the best
i2v-background score and remains competitive on background consistency, indicating strong stability
in background scenes during video generation. The consistently strong performance across multiple
domains, including robotics, further demonstrates the robustness of Kairos in diverse real-world
scenarios.
Table 16 Evaluation on PAI-Bench. For each column, the highest score is bolded.
|       |     |       |     | QualityScore |     |     | DomainScore |     | Overall |
| ----- | --- | ----- | --- | ------------ | --- | --- | ----------- | --- | ------- |
| Model |     | Param |     |              |     |     |             |     |         |
Score
|     |     |     | i2v-bg i2v-s | aes img bg-con | mot sub-con | o-con | av cs ro in | hu  | ph  |
| --- | --- | --- | ------------ | -------------- | ----------- | ----- | ----------- | --- | --- |
Cosmos-Predict2.5 2B 97.4 96.6 52.4 94.2 92.5 20.1 66.1 94.1 80.8 87.8 81.4
|     |     |     |     | 70.8 | 99.1 |     |     | 93.9 | 81.0 |
| --- | --- | --- | --- | ---- | ---- | --- | --- | ---- | ---- |
Cosmos-Predict2.5 14B 97.9 97.2 52.5 70.0 94.8 99.1 93.4 20.1 67.8 94.2 79.9 87.7 80.0 93.5 81.0
Wan2.2 5B 96.7 95.9 51.9 69.9 93.7 98.8 91.8 20.3 65.2 93.1 79.3 88.4 83.0 91.5 80.4
Kairos 4B 97.9 96.5 51.9 68.8 94.5 98.7 92.0 21.3 64.4 94.3 84.0 84.5 84.1 92.8 80.8
Whilequantitativemetricsprovideanobjectivemeasureofmodelperformance, qualitativeevaluation
is also important for a comprehensive assessment. Objective scores may not always fully capture
the perceptual quality of generated videos, and qualitative analysis can help complement these
metrics by providing a more direct examination of visual fidelity, prompt alignment, and temporal
consistency. For qualitative evaluation, we select representative high-quality video samples generated
70

Figure 20 Kairos samples on the PAI-Bench dataset.
by Kairos from each sub-domain of PAI-Bench, as shown in Fig. 20, covering diverse scenarios such
as autonomous driving, industrial manufacturing, indoor human activities, and robotic environments.
The results show that Kairos is capable of generating realistic and high-quality videos across different
domains. The generated videos demonstrate strong prompt adherence and accurate first-frame
conditioning, while maintaining good physical consistency throughout the video sequence.
6.4.2 WorldModelBench
Following the same benchmark introduced in the embodied evaluation, we further evaluate Kairos
on the full WorldModelBench dataset. In the embodied evaluation we focus on the TI2V setting,
as embodied scenarios are more sensitive to the initial state of the robot or manipulator. Here we
follow the official evaluation protocol and conduct experiments under both TI2V and T2V settings.
Table 17 reports detailed quantitative comparisons between Kairos and other baseline models on
this benchmark. Compared with mainstream open-source models of similar scale, Kairos achieves
71

Table 17 Evaluation on WorldModelBench. For each column, the highest score is bolded.
|       |     |            |             |        | Physics | Adherence |         | Common      | Sense    | Total |
| ----- | --- | ---------- | ----------- | ------ | ------- | --------- | ------- | ----------- | -------- | ----- |
| Model |     | Mode Param | Instruction |        |         |           |         |             |          |       |
|       |     |            |             | Newton | Deform. | Fluid     | Penetr. | Grav. Frame | Temporal | Score |
Cosmos-Predict2.5 TI2V 2B 2.37 1.00 0.8 0.99 0.85 1.00 0.87 0.82 8.71
Cosmos-Predict2.5 TI2V 14B 2.45 1.00 0.84 0.99 0.88 1.00 0.93 0.87 8.95
| Wan2.2 |     | TI2V | 5B 2.30 | 1.00 | 0.78 | 0.99 | 0.82 | 0.99 0.87 | 0.79 | 8.53 |
| ------ | --- | ---- | ------- | ---- | ---- | ---- | ---- | --------- | ---- | ---- |
| Kairos |     | TI2V | 4B 2.36 | 1.00 | 0.85 | 0.99 | 0.89 | 0.99 0.92 | 0.89 | 8.89 |
Cosmos-Predict2.5 T2V 2B 2.30 1.00 0.91 0.99 0.90 1.00 1.00 0.95 9.01
Cosmos-Predict2.5 T2V 14B 2.30 1.00 0.91 0.99 0.92 1.00 1.00 0.97 9.09
| Wan2.2 |     | T2V    | 5B 2.18           | 1.00   | 0.87   | 1.00            | 0.88 | 0.99 0.99 | 0.95 | 8.87 |
| ------ | --- | ------ | ----------------- | ------ | ------ | --------------- | ---- | --------- | ---- | ---- |
| Kairos |     | T2V    | 4B 2.33           | 1.00   | 0.83   | 1.00            | 0.90 | 1.00 0.99 | 0.93 | 8.99 |
|        |     | Figure | 21 Kairos samples | (TI2V) | on the | WorldModelBench |      | dataset.  |      |      |
competitive scores under both settings, and remains close to the 14B Cosmos-Predict2.5 baseline
despite its compact 4B size. In the TI2V setting, where first-frame conditioning introduces stricter
constraints on video generation, Kairos obtains the best scores on several physics and common-sense
metrics, suggesting strong capability in maintaining object structural consistency and avoiding
| physically | implausible | interactions. |     |     |     |     |     |     |     |     |
| ---------- | ----------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
We further conduct qualitative analysis of Kairos on WorldModelBench, focusing on its instruction-
following capability and physics adherence. As illustrated in Fig. 21, Kairos successfully accomplishes
the specified tasks across a variety of complex scenarios. For example, in scenes such as the rotation
of bottled water in a spiral filling machine and a vehicle being lifted by a hydraulic elevator, the
model accurately generates dynamic processes that align with the given instructions, demonstrating
strong instruction-following ability. Meanwhile, the generated videos also exhibit plausible physical
behaviors. Forinstance, flowerpetalstrembleinresponsetothemotionofabutterfly, andthemotion
trajectories and accumulation patterns of falling garbage appear physically reasonable. Similar
behaviors can also be observed in the T2V setting, as shown in Fig. 22.
72

Figure 22 Kairos samples (T2V) on the WorldModelBench dataset.
6.4.3 VideoPhy
To evaluate the physical reasoning capability of our model, we benchmark it on VideoPhy, which
contains 688 human-verified prompts. These prompts describe interactions between entities with
different physical properties, including solid–solid, solid–fluid and fluid–fluid. Following the bench-
mark’s evaluation protocol, we generate videos using 344 test prompts. Each generated video
is evaluated using two metrics: Semantic Adherence (SA) and Physical Commonsense (PC). SA
measures whether the generated video correctly reflects the entities and actions described in the
carefully designed prompts that simulate diverse physical interactions, while PC evaluates whether
the generated scene is consistent with real-world physical laws. Both metrics are defined as binary
judgments (0/1) and are computed using an auto evaluator VIDEOCON-PHYSICS provided by
the benchmark. We report the Average Score (SA=1, PC=1) as the final results. Prompt
enhancement can effectively enrich visual details in generated videos, thereby improving overall
generation quality. Since the prompts in VideoPhy are relatively short, we apply model-specific
prompt enhancement strategies to ensure a fair comparison across different models. Specifically,
for Wan2.2-5B, we follow the official recommendation and employ Qwen/Qwen2.5-7B-Instruct for
prompt enhancement. For Cosmos-Predict2.5-2B/14B, since the prompt enhancement module has
been removed in its NVIDIA official implementation, we adopt the same prompt enhancement
strategy used for Kairos, namely leveraging Qwen3-8B. To ensure a fair comparison, we report the
best performance for each model with or without prompt enhancement.
Table 18 Evaluation on VideoPhy. The highest score is bolded.
Model Cosmos-Predict2.5-2B Cosmos-Predict2.5-14B Wan2.2-5B Kairos
Average Score 44.64 45.16 38.85 45.55
As shown in Table 18, our model achieves the highest average score on VideoPhy with 45.55,
outperforming Wan2.2-5B and Cosmos-Predict2.5-2B/14B. Remarkably, with only 4B parameters,
Kairos outperforms Cosmos-Predict2.5-14B, demonstrating both high parameter efficiency and the
ability to generate videos that adhere to real-world physical laws. Figure 23 presents qualitative
73

Prompt Generated frames
“A hand mixer stirs through thick
cake batter.”
“Milk colliding with piping hot
black coffee.”
“Pickax chisels away at the rock.”
“Rainwater flowing through a rain
gutter.”
“A waterfall cascades over jagged
rocks.”
Figure 23 Kairos samples on the VideoPhy dataset.
results of Kairos on VideoPhy, covering a range of scenarios that involve physical interactions. For
the prompt “A hand mixer stirs through thick cake batter”, the generated video shows a mixer
that continuously rotates within the dense cake batter, creating clearly visible swirling and folding
patterns that reflect the behavior of viscous fluids under mechanical agitation. For “Milk colliding
with piping hot black coffee”, the poured milk gradually disperses into the coffee, forming a natural
mixing process with smooth and coherent fluid dynamics. Our model also captures diverse physical
interactions in other scenarios, producing realistic scenes such as rocks breaking under a pickaxe,
rainwater flowing through a gutter, and a waterfall cascading over jagged rocks. These examples
indicatethatKairoscorrectlyreflectstheentitiesandactionsdescribedintheprompts,demonstrating
strong semantic adherence while maintaining physically consistent motion patterns and interactions.
6.5 Long-Horizon Generation
To further evaluate long-horizon video generation, we conduct experiments on PAI-Bench using a
15-second generation setting. PAI-Bench offers a diverse set of real-world scenarios and measures
models’abilitytocapturerealisticphysicaldynamicswhilemaintainingphysicallyplausiblebehaviors.
The extended 15-second generation setting enables a more comprehensive examination. Long-horizon
consistency is regret-relevant because delayed failures, forgotten object states, and accumulated
rollout drift can affect future physical cost.
Tables 16 and 19 present the quantitative results of PAI-Bench under 5 and 15 second settings. When
the generation horizon is extended to 15 seconds, the baseline models exhibit noticeable degradations
in both quality metrics and domain-specific metrics. For example, Cosmos-Predict2.5-2B/14B shows
clear drops in image-to-video consistency metrics, including i2v-bg (97.4/97.9→93.6/93.7) and i2v-s
(96.6/97.2→92.0/91.8), indicating the increasing difficulty in preserving subject and background
consistency in longer sequences. In addition, several domain-level scores decrease substantially, such
74

| Figure | 24 Kairos samples | on the PAI-Bench-15s | dataset. |
| ------ | ----------------- | -------------------- | -------- |
75

Table 19 Evaluation on PAI-Bench-15s. For each column, the highest score is bolded.
QualityScore DomainScore Overall
Model Param
Score
i2v-bg i2v-s aes img bg-con mot sub-con o-con av cs ro in hu ph
Cosmos-Predict2.5 2B 93.6 92.0 55.0 71.9 91.0 99.3 87.6 20.6 59.7 82.6 72.8 84.9 77.3 90.6 77.2
Cosmos-Predict2.5 14B 93.7 91.8 52.9 68.4 92.4 99.2 89.0 20.4 61.9 82.6 68.1 81.2 75.4 89.2 76.2
Wan2.2 5B 97.9 97.1 51.9 67.6 91.5 99.2 90.7 20.7 54.3 90.9 70.1 84.1 79.6 91.4 77.8
Kairos 4B 97.1 95.6 51.9 68.8 93.4 98.5 89.8 21.5 66.7 89.2 80.4 86.8 83.2 90.0 79.9
as autonomous driving (66.1/67.8→59.7/61.9), common sense (94.1/94.2→82.6/82.6) and robot
(80.8/79.9→72.8/68.1). Wan2.2-5B exhibits similar trends, with noticeable decreases in autonomous
driving (65.2→54.3) and robot (79.3→70.1).
Under the 15-second setting, our model achieves the best overall score of 79.9, outperforming
Cosmos-Predict2.5-2B/14B (77.2/76.2) and Wan2.2-5B (77.8). In particular, Kairos maintains strong
performance in several domain-level metrics, including autonomous driving (66.7), robot (80.4),
industry (86.8) and human (83.2), while also preserving high image-to-video consistency with i2v-bg
(97.1) and i2v-s (95.6). Relative to the compared baselines, Kairos shows the smallest degradation
when moving from 5-second to 15-second generation on Overall Score, suggesting better relative
preservation of scene consistency and physical interaction; absolute long-horizon preservation beyond
the 15-second setting is not evaluated here.
Figure 24 presents the qualitative results of our model in the long-horizon generation. The visual
results show that Kairos maintains consistent object appearance and scene structure over long
temporaldurations while producingnaturaland coherent motion. In theexampleof adog interacting
with floating bubbles, the dog’s head pose and attention gradually change following the bubble’s
trajectory with smooth transitions. In the forest scene, the morning mist and sunlight evolve
smoothly over time. As the sun gets stronger, the mist fades and the trees in the background become
more visible. These results indicate that Kairos produces temporally coherent and visually consistent
long-horizon videos.
6.6 Efficiency–Capability Trade-off as Deployment Proxy
Although inference efficiency is discussed in detail in Section 5, it is also part of evaluation because
deployment readiness is a prerequisite for Physical AI. A world model that performs well offline but
cannot run under practical latency and memory constraints cannot participate in observation–action–
feedback loops.
The current efficiency results (cf. Tables 4 and 5) show that Kairos offers a favorable efficiency–
capability trade-off. Under a 720P, 5-second TI2V setting, Kairos-4B uses 23.5 GB memory, requires
2.3 PFlops, and achieves 43 seconds on 1 GPU and 9 seconds on 4 GPUs—substantially more efficient
than larger baselines such as Lingbot-28B and Cosmos-Predict2.5-14B, and also more efficient than
similarly scaled models such as Wan2.2-5B. Additional experiments show that Kairos maintains
lower latency across 480P and 720P settings and scales approximately linearly as video duration
increases.
6.7 Regret-Relevant Cases
To further examine whether Kairos preserves information that matters for regret-aware embodied
prediction, we present two representative manipulation cases. In our formulation, the physical cost
J (· | H ,g) is conditioned on the task goal g. Therefore, an imagined rollout should keep the goal,
H t
76

Goal: Put the clothes in the washing machine.
Input frame Predicted frames
Kairos
Success
Input frame Predicted frames
Cosmos
predict 2.5
2B
Failure
Goal: Place the yellow container into the plastic bag.
Input frame Predicted frames
Kairos
Success
Input frame Predicted frames
Cosmos
predict 2.5
2B
Failure
Figure 25 Regret-relevant cases in embodied future prediction. Given the same input frame and task goal,
Kairos generates more goal-conditioned future rollouts than Cosmos-Predict2.5-2B. In the clothes-to-washing-
machine case, Kairos better preserves the intended manipulation goal, while the baseline shows weaker
task-completion progress. In the yellow-container-to-plastic-bag case, Kairos better preserves the insertion
intent, whereas the baseline shows weaker object–goal coherence. These cases suggest that Kairos maintains
goal-conditioned control information in embodied future prediction.
manipulated object, and target state coherent over time. A rollout may look plausible as a video,
but if it drifts away from the requested manipulation, it becomes less useful for evaluating low-cost
embodied execution.
We compare Kairos with Cosmos-Predict2.5-2B using the same input frame and task goal. The com-
parison focuses on whether the generated future remains organized around the intended manipulation
and shows progress toward the target state.
Figure 25 shows two representative cases. In the “put the clothes in the washing machine” case,
Kairos keeps the rollout centered on moving the clothes toward the washer opening, while Cosmos-
Predict2.5-2B shows weaker task-completion progress. In the “place the yellow container into the
plastic bag” case, Kairos more clearly preserves the intended container-to-bag interaction, whereas
the baseline shows weaker object–goal coherence and less clear insertion progress.
These cases suggest that Kairos better preserves goal-conditioned control information in embodied
future prediction. For regret-aware Physical AI, this matters because the value of an imagined
rollout depends on whether it preserves the task conditions that determine physical cost.
6.8 Current Evaluation Limitations and Future Closed-Loop Validation
The current evaluations demonstrate strong performance across embodied generation, world-action
benchmarks, general physical reasoning, long-horizon generation, and inference efficiency. However,
several important capabilities required for a complete Physical AI world model remain unmeasured.
77

These missing evaluations are precisely the evaluations needed to move from proxy evidence about
components of to direct evidence of regret-aware decision support. A complete validation would
J H
compare Kairos against baseline representations or policies under matched tasks, and measure
whether decisions based on Z achieve lower realized physical cost, fewer unsafe events, lower recovery
t
| effort, smaller | imagined–real |         | rollout gaps, | or better | task    | success.         |                    |         |
| --------------- | ------------- | ------- | ------------- | --------- | ------- | ---------------- | ------------------ | ------- |
| •               |               |         |               |           | Current | video benchmarks | evaluate generated | plausi- |
| Imagined–real   |               | rollout | correlation.  |           |         |                  |                    |         |
bility but do not directly measure whether imagined rollouts match real robot rollouts. Future
work should compare predicted future states with actual robot executions under the same
| initial | conditions. |     |     |     |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
• Counterfactual action validation. Current WAM benchmarks evaluate action performance
but do not systematically test multiple alternative actions from the same initial state. Future
evaluationshouldmeasurewhetherKairospredictsdifferentoutcomesfordifferentinterventions,
such as grasping versus pushing, lifting versus sliding, or stopping versus continuing.
• Failure prediction and safety filtering. Current benchmarks do not directly measure
whetherKairoscananticipatefailurebeforeexecutionorreduceunsafeevents. Futureevaluation
should test whether the model can predict slips, collisions, unstable grasps, excessive force,
| human-proximity |     | risk, | or irreversible | states | before | they occur. |     |     |
| --------------- | --- | ----- | --------------- | ------ | ------ | ----------- | --- | --- |
• Recovery learning. Current benchmarks primarily evaluate success or generated quality.
Future evaluation should measure whether Kairos can represent recovery strategies after failure
| and whether | recovery    |     | data improves | policy | robustness. |         |                     |     |
| ----------- | ----------- | --- | ------------- | ------ | ----------- | ------- | ------------------- | --- |
| •           |             |     |               |        |             | Current | results show strong | WAM |
| Policy      | improvement |     | from imagined |        | experience. |         |                     |     |
performanceandproxyself-alignmentcapability, butdonotdirectlydemonstratethatimagined
rolloutsimprovearealrobotpolicy. FutureevaluationshouldmeasurewhetherKairos-generated
or Kairos-evaluated rollouts lead to measurable success-rate gains in real deployment.
• Uncertainty and calibration. A world model should know when its prediction is uncertain.
Future evaluation should include uncertainty calibration, risk estimation, and discrepancy
| between | imagined | and | real outcomes. |     |     |     |     |     |
| ------- | -------- | --- | -------------- | --- | --- | --- | --- | --- |
Table 20 summarizes the future evaluation protocol, which should include the following real-robot
tests:
These future evaluations will determine whether Kairos moves from proxy world-action capability to
| validated closed-loop |     | regret | reduction. |     |     |     |     |     |
| --------------------- | --- | ------ | ---------- | --- | --- | --- | --- | --- |
6.9 Summary
The evaluation results show that Kairos establishes several important prerequisites for control-
sufficient world-action modeling. On embodied world-model benchmarks, Kairos-robot-4B demon-
strates strong physical plausibility, instruction grounding, and parameter efficiency. On World
Action Model benchmarks (RoboTwin 2.0, LIBERO-Plus), Kairos achieves strong manipulation
performance and robustness, supporting the value of jointly modeling world dynamics and action
evolution. Ablation studies show that human-centric pretraining and joint generation–prediction
training contribute meaningfully to action-relevant performance. General world-model benchmarks
show that Kairos retains broad physical and semantic priors. Long-horizon generation results suggest
stronger multi-timescale state maintenance. Efficiency evaluation indicates that Kairos offers a
| favorable deployment-oriented |     |     | trade-off. |     |     |     |     |     |
| ----------------------------- | --- | --- | ---------- | --- | --- | --- | --- | --- |
78

Table 20 Future closed-loop evaluation protocol for moving from proxy capabilities to validated regret-
| reducing | Physical AI. |     |     |     |     |
| -------- | ------------ | --- | --- | --- | --- |
Future capability Suggested evaluation protocol Target evidence
Rollout fidelity Compareimaginedrolloutswithrealroll- High correlation between predicted and
|     |     | outs under matched | initial states | observed | outcomes |
| --- | --- | ------------------ | -------------- | -------- | -------- |
Counterfactual clo- Execute different actions from the same Predicted outcome branches match real
| sure |     | initial state |     | action effects |     |
| ---- | --- | ------------- | --- | -------------- | --- |
Failure prediction Predict failure before execution High precision and recall for slips, colli-
|     |     |     |     | sions, drops, | task failures |
| --- | --- | --- | --- | ------------- | ------------- |
Safety filtering Use Kairos to reject unsafe candidate Reductioninunsafeeventswithoutlarge
|     |     | actions |     | task-success | loss |
| --- | --- | ------- | --- | ------------ | ---- |
Recovery learning Evaluate recovery after induced failures Higher recovery success and lower hu-
man intervention
Policy improvement Trainorrankpolicieswithimaginedroll- Measurablerealpolicyimprovementover
|     |     | outs |     | baseline |     |
| --- | --- | ---- | --- | -------- | --- |
Calibration Comparepredicteduncertaintywithroll- Well-calibrated risk and uncertainty es-
|     |     | out error |     | timates |     |
| --- | --- | --------- | --- | ------- | --- |
Taken together, these results support the central claim of the report: Kairos is a regret-aware world-
actionmodelstackthatlearns, maintains, predicts, andrunscontrol-relevantinformationforPhysical
AI. At the same time, the claim boundary remains clear. The next stage of Kairos evaluation should
directly measure real-robot rollout correlation, counterfactual action prediction, failure anticipation,
safety filtering, recovery learning, and policy improvement from imagined experience. Only then can
Kairos be fully validated as a closed-loop regret-reducing Physical AI system. Overall, the evaluation
results should be read as evidence that Kairos improves several components needed for a low-regret
world-action state, rather than as a direct measurement of representation-induced regret itself.
| 7 Related | Work       |        |     |     |     |
| --------- | ---------- | ------ | --- | --- | --- |
| 7.1 Video | Generation | Models |     |     |     |
Diffusion-based Video Generation. The success of Diffusion Models (DMs) [10] in image
synthesis has catalyzed their extension to the video domain. Early pioneers like Video Diffusion
Models (VDM) [11] first extended the standard 2D U-Net to a 3D structure [156] by replacing 2D
convolutions with space-time factorized convolutions. To alleviate the heavy computational burden
of 3D operators, many subsequent works [12–15, 155] adopted a "spatial-then-temporal" paradigm,
inserting 1D temporal attention layers after 2D spatial blocks to capture dynamic dependencies.
A significant architectural shift occurred with the introduction of Diffusion Transformers (DiT)
[61], which demonstrated superior scalability over U-Net. This has led to the emergence of high-
performance open-source video models such as LTX-Video [17], which refines the VAE decoder for
high-frequency detail reconstruction, and HunyuanVideo [16], which integrates Multimodal Large
Language Models (MLLMs) as text encoders to enhance text-video alignment. Building upon these
advancements, Wan [82] meticulously optimizes each critical module—from the autoencoder to
the text-video alignment—and provides comprehensive ablation studies to facilitate future video
generation research. Furthermore, recent advancements in Flow Matching [77] have further optimized
the training efficiency and generation quality of these diffusion-based frameworks.
79

Autoregressive Video Generation. Another prominent paradigm treats video generation as a
sequence modeling task, analogous to Large Language Models (LLMs). Early works like VideoGPT
[157] combined VQ-VAE [158] with GPT-like architectures [159] to autoregressively model discrete
latent tokens in a spatio-temporal grid. To extend the duration of generated content, TATS [160]
introduced a time-agnostic VQGAN and a time-sensitive transformer to synthesize thousands of
frames. While diffusion models have recently dominated the field, autoregressive frameworks remain
highly competitive for long-term consistency and streaming generation. For instance, VideoPoet
[8] utilizes a large-scale transformer to unify multiple video-related tasks within a single LLM-style
framework. More recently, MAGI-1 [9] incorporates causal constraints and KV caching to achieve
real-time, high-fidelity video synthesis, demonstrating the enduring potential of autoregressive
modeling in simulating physical dynamics and causal sequences.
Large Video Foundation Models. The landscape of video generation has been revolutionized
by the emergence of large-scale foundation models that act as general-purpose world simulators.
A landmark moment was the introduction of Sora [2], which demonstrated that Scaling Laws [30]
previouslyobservedinLLMsalsoapplytovideo: increasingparametersandtrainingdatasignificantly
enhances the model’s understanding of 3D geometry and world dynamics. Following this, several
powerful industrial models have emerged to push the boundaries of cinematic synthesis. Kling
[4] (now updated to the Kling O3 architecture in 2026) utilizes a 3D-VAE and a computationally
efficient full-attention mechanism to support ultra-long, complex human motion synthesis. Similarly,
Luma Dream Machine [5] and Runway Gen-3 Alpha [6] focus on high-fidelity motion and temporal
smoothness through massive multi-modal pre-training. Furthermore, ByteDance’s Seedance series [7]
has introduced a unified multimodal joint generation architecture. The latest Seedance 2.0 natively
supports text, image, audio, and video inputs, leveraging a Mixture-of-Transformer-Experts (MoT)
design to balance spatiotemporal consistency with high-fidelity cinematic aesthetics.
7.2 World Models
World models aim to learn compact representations of environments that enable agents to predict
future states and simulate interactions. Early work such as World Models [20] demonstrated that
agents could be trained entirely within a latent “dream” environment produced by a VAE and
recurrent dynamics model. This paradigm was further extended by latent dynamics approaches
including PlaNet [21] and the Dreamer series [22–24], which perform reinforcement learning directly
within imagined trajectories generated by learned world models.
With the rapid progress of large-scale generative models, the concept of world models has expanded
beyond reinforcement learning toward video-based simulation of real-world dynamics. Recent ap-
proaches leverage transformer and diffusion architectures to learn rich spatiotemporal representations
from large video corpora. For example, UniSim [19] proposes a neural closed-loop simulator for
autonomous driving that generates consistent sensor observations under different actions. Similarly,
large-scale video generation models such as Sora [2] have demonstrated the capability to simulate
complex physical interactions and long-term temporal consistency, suggesting that generative video
models may serve as general-purpose world simulators.
More recent work explores interactive world modeling by conditioning generation on actions [178] or
control signals. GAIA-1 [161] learns a generative world model for autonomous driving that predicts
future video conditioned on vehicle controls. Genie [18] further introduces generative interactive
environmentscapableofsynthesizingplayableworldsfromvideodata. Recently,Cosmos[3]proposesa
large-scaleworldfoundationmodeldesignedforroboticsandphysicalAI,enablingrealisticsimulation
80

of environments conditioned on agent actions. These advances indicate a promising direction toward
unified world simulators that combine perception, dynamics modeling, and controllable environment
generation.
7.3 World Action Models
From VLA to WAMs. Generalist embodied agents have long relied on Vision-Language-Action
(VLA) models that learn reactive, direct observation-to-action mappings without modeling how the
physical world evolves under intervention. To overcome the short-sightedness and weak physical
grounding of such purely reactive policies, the World Action Model (WAM) paradigm unifies
predictive environment dynamics with motor control by jointly targeting the distribution over future
states and actions. By internalizing physical laws through future simulation, WAMs enable stronger
long-horizon reasoning and spatial awareness than standard VLAs—though this unified objective
introduces sharp architectural trade-offs between generation fidelity and inference latency.
Cascaded WAMs. Cascaded WAMs synthesize future visual representations conditioned on
task goals before extracting control actions. Explicit methods first forecast raw 2D RGB frames
using inverse dynamics or multimodal conditioning [41, 47, 162]. To mitigate spatial hallucinations
inherentinpixel-levelgeneration, subsequentexplicitarchitecturesextractintermediate2Dgeometric
representations like optical flow and point tracks [48, 50, 163], or extend into 3D and 4D spaces for
rigorous spatial reasoning [49? ]. Despite providing highly interpretable plans, explicit decoding
suffers from severe computational latency, rendering high-frequency closed-loop control intractable
[182]. To circumvent this bottleneck, implicit cascaded WAMs bypass high-dimensional image
rendering by encoding anticipated futures strictly within continuous or discrete latent spaces. This
latent planning involves learning quantized semantic codebooks [165], imposing geometric mask
bottlenecks [166], or operating entirely within diffusion representations [167]. To further accelerate
reactive control, frameworks extract intermediate network features [164] or self-distill multi-step
generation into a single feed-forward pass [182]. Ultimately, while explicit WAMs excel in modularity
with off-the-shelf simulators, implicit approaches prioritize the execution scalability and efficiency
required for real-time deployment.
Joint World-Action Models. Departing from the two-stage pipeline, joint WAMs co-model
decision-making and physical dynamics within a shared space, splitting into autoregressive and
diffusion-based families. The autoregressive family casts states and actions as a unified sequence over
a shared vocabulary: causal transformers first predict pixel-space trajectories as implicit planners
[39, 168], then structure a visual chain-of-thought via intermediate subgoal images [169], and
ultimately fuse text, images, and discrete actions into one vocabulary [38]. Since strict autoregressive
action decoding causes error propagation and trajectory drift, remedies include action-attention
masking [38] and a hybrid design with a parallel continuous action head to avoid quantization
errors [37]; still, sequentially decoding high-dimensional visual states incurs heavy latency that
hampers reactive deployment. Conversely, diffusion-based WAMs frame prediction as denoising or
flow-matching, jointly optimizing states and actions to expose diverse marginal and conditional
distributions for deeper causal understanding and stronger sample efficiency. Early designs fuse
all modalities in a single diffusion transformer [42, 45, 170], while later works resolve action-image
modality conflicts through separate or bridged token streams [171–173]. To avoid costly pixel-
level reconstruction, several adopt implicit latent world modeling [43, 46, 179, 181], and others
decouple diffusion timesteps or scale via mixture-of-transformers [36, 53, 174, 175]. For inference
efficiency,recentframeworksadoptlightweightheads,asynchronoussampling,orspeculativedecoding
[40, 138, 176, 177, 180]. Across both families, the central challenge remains balancing high-fidelity
81

joint simulation in training against lightweight, asymmetric modality decoupling at inference.
7.4 Efficient Attention Mechanisms
The quadratic complexity of the standard self-attention mechanism in Transformers poses a major
challenge for modeling long sequences such as high-resolution videos. Given an input sequence of
length N, vanilla attention requires O(N2) time and memory, which quickly becomes prohibitive as
the spatial and temporal dimensions increase. To address this limitation, a large body of work has
explored efficient attention mechanisms that reduce computational complexity while preserving the
modeling capacity of Transformers.
Early approaches focused on approximating the softmax attention through kernelization or low-rank
decomposition. Linear Transformers [183] reformulated softmax attention using kernel feature
maps, enabling attention computation in linear time with respect to sequence length. Similarly,
Performer [184] introduced FAVOR+ random feature approximations to achieve scalable attention
with theoretical guarantees. Other works explored sparse attention patterns, restricting interactions
to local or predefined structures in order to reduce computational cost [64–66].
More recent research has shifted toward designing sequence models with recurrent or state-space
style updates that scale linearly with sequence length. Retentive Networks (RetNet) [185] replace
the softmax attention with a retention mechanism that supports both parallel training and recurrent
inference. The Mamba architecture [67, 72–74, 186] further demonstrates that selective state space
models can achieve strong sequence modeling performance while maintaining linear complexity.
Building on these developments, recent works further explore gated update mechanisms to improve
the stability of long-context modeling. Delta-based architectures such as Gated Delta Networks [54]
introduce gated update rules that mitigate key-value interference during sequence updates. In a
similar spirit, Gated Linear Attention (GLA) incorporates gating mechanisms into linear attention
to regulate information flow[69, 187]. By introducing learnable gates into the attention update,
GLA selectively integrates new key-value information while suppressing outdated context, enabling
stable long-range dependency modeling with O(N) complexity [63, 68, 70, 71]. Such efficiency is
particularly beneficial for tasks involving extremely long token sequences.
8 Conclusion and Future Works
This report introduced Kairos, a regret-aware native world-action model stack for Physical AI.
We made this notion explicit through a horizon-level regret formulation: a useful compressed state
should support decisions whose expected physical cost approaches the cost achievable from the full
task-relevant history. The central motivation is that a world model for embodied intelligence should
not be understood as a full simulator of all future pixels. In real physical systems, the decisive
requirement is to learn and maintain a compact internal state that preserves the information needed
for control: object state, spatial relations, contact condition, task progress, action consequences,
failure boundaries, safety risks, and deployment uncertainty. We refer to this representation as a
control-sufficient state.
Kairos is designed around this principle. The current report establishes several model-side, data-
side, memory-side, and inference-side prerequisites for future regret-aware Physical AI; real-world
closed-loop regret minimization itself is positioned as future work. These prerequisites include
acquiring control-relevant information from heterogeneous experience, compressing this information
into a shared world-action state, maintaining the state across multiple temporal scales, connecting
prediction to future actions, and running the model under realistic deployment constraints.
82

The first component of Kairos is the Curriculum. Instead of treating
|     |     | Cross-Embodiment |     | Data |     |     |     |
| --- | --- | ---------------- | --- | ---- | --- | --- | --- |
open-world videos, human-centric data, and robot interaction data as a flat mixture, Kairos organizes
them by intervention strength. Open-world videos provide passive physical observation; human-
centric data provides intentional task structure and behavior; robot data provides embodied action
grounding. This curriculum is designed to move the model along a developmental pathway from
passive physical priors toward action grounding; direct empirical validation of action–outcome
causation is deferred to Section 8.1. Its significance is not only data scale, but the organization of
heterogeneous experience into a path that can support control-sufficient state learning.
| The second | component | is the                                     |     |     |     | Architecture. |     |
| ---------- | --------- | ------------------------------------------ | --- | --- | --- | ------------- | --- |
|            |           | Native Understanding–Generation–Prediction |     |     |     |               |     |
In Kairos, understanding, generation, and prediction are not separate modules connected after the
fact. They are three interfaces to a shared world-action state Z . World Understanding constructs Z
|     |     |     |     | t   |     |     | t   |
| --- | --- | --- | --- | --- | --- | --- | --- |
frommultimodalhistory, instruction, robotstate, andphysicalcontext. WorldGenerationregularizes
and probes through physically plausible future imagination. World Prediction turns into a
|     | Z   |     |     |     |     | Z   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     | t   |     |     |     |     | t   |     |
world-action interface through joint modeling of future visual states and future action tokens. This
architecture moves Kairos beyond passive visual forecasting toward a world-action model that can,
| in future | extensions, | support counterfactual | action evaluation. |     |     |     |     |
| --------- | ----------- | ---------------------- | ------------------ | --- | --- | --- | --- |
The third component is Attention. Long-horizon Physical AI requires
|     |     | Hybrid Linear | Temporal |     |     |     |     |
| --- | --- | ------------- | -------- | --- | --- | --- | --- |
more than longer context: it requires maintaining control-relevant state variables across different
timescales. Sliding-window attention supports local dynamics such as motion continuity and
contact changes; dilated sliding-window attention supports mid-range dependencies such as object
interaction and subtask transitions; gated linear attention supports persistent global memory for
object permanence, task progress, delayed effects, and long-range causal context. The theoretical
analysis in this report supports the need for persistent memory and provides bounds for hybrid
multi-scale temporal memory under stated assumptions. It should be interpreted as theoretical
support for the design, not as a universal guarantee of real-world long-horizon correctness.
The fourth component is the Co-Design. For Physical AI, inference
|     |     | Deployment-Aware | System |     |     |     |     |
| --- | --- | ---------------- | ------ | --- | --- | --- | --- |
efficiency is not merely an implementation detail: a world model that cannot run under practical
latency, memory, communication, and hardware constraints cannot participate in observation–
action–feedback loops. Kairos therefore incorporates timestep distillation, hardware-aware inference
optimization, mixed parallelism, quantization, caching, and action-only prediction pathways. These
mechanisms improve deployment readiness and make imagined rollout or action prediction more
practical. They do not, by themselves, prove real-time closed-loop robot control; instead, they
| provide   | necessary infrastructure | for future  | deployment-side | validation. |          |               |     |
| --------- | ------------------------ | ----------- | --------------- | ----------- | -------- | ------------- | --- |
| The fifth | component                | is the      |                 |             | Density. | Kairos builds | a   |
|           |                          | Data Engine | for Control     | Information |          |               |     |
large-scale data pipeline for collection, curation, tagging, captioning, enhanced text annotation, and
high-throughput processing. Under the control-sufficient perspective, the value of this pipeline is not
only that it processes large volumes of data, but that it can be extended to identify and structure
data that most reduces uncertainty about action consequences, contact dynamics, failure boundaries,
recovery strategies, and safety risks. This reframes data construction for Physical AI from raw scale
| toward control | information | density. |     |     |     |     |     |
| -------------- | ----------- | -------- | --- | --- | --- | --- | --- |
The evaluation results provide encouraging evidence for these design choices. Kairos achieves strong
performance on embodied world-model benchmarks, world-action benchmarks, general world-model
benchmarks, long-horizon generation, and inference-efficiency evaluations. These results suggest that
Kairos learns several capabilities relevant to Physical AI, including physical plausibility, instruction
grounding, joint world-action prediction, long-horizon consistency, and deployment-oriented efficiency.
83

Direct validation will require future experiments that measure imagined–real rollout correlation,
counterfactual action accuracy, failure prediction, safety filtering, recovery learning, and measurable
| policy | improvement |     | in  | real robot | settings. |     |     |     |     |     |     |
| ------ | ----------- | --- | --- | ---------- | --------- | --- | --- | --- | --- | --- | --- |
Taken together, Kairos is a step toward control-sufficient world modeling for Physical AI. It moves
world modeling beyond static video generation by integrating cross-embodiment pretraining, unified
world-action state modeling, hybrid temporal memory, deployment-aware inference, and scalable
data engineering. Closed-loop validation in real robots is left to future work.
The future of Kairos is therefore not simply to make generated videos more realistic or benchmarks
higher. The more important goal is to determine whether the internal world-action state can
help physical agents make fewer costly mistakes. The next stage of research should directly test
whether Kairos can predict what matters for control, distinguish the consequences of different actions,
generalize across intervention distributions, maintain state over much longer horizons, and learn
| from | experience |       | with high | control | information |     | density. |     |     |     |     |
| ---- | ---------- | ----- | --------- | ------- | ----------- | --- | -------- | --- | --- | --- | --- |
| 8.1  | Future     | Works |           |         |             |     |          |     |     |     |     |
Future Kairos development will focus on five directions that move it from proxy world-action
| capability |     | toward | directly | validated |     | regret-aware | Physical | AI. |     |     |     |
| ---------- | --- | ------ | -------- | --------- | --- | ------------ | -------- | --- | --- | --- | --- |
The regret formulation also clarifies the target of future work. The next stage is not only to
improve benchmark scores, but to test whether Kairos-based decision support achieves lower realized
physical cost than baseline representations or policies under real or high-fidelity simulated closed-loop
execution. Thisrequiresmatched-taskcomparisonsthatmeasuretasksuccess, unsafeevents, recovery
| cost, | human  | intervention, |     | latency,              | and | imagined–real |        | rollout error. |     |     |     |
| ----- | ------ | ------------- | --- | --------------------- | --- | ------------- | ------ | -------------- | --- | --- | --- |
| 8.1.1 | Direct | Evaluation    |     | of Control-Sufficient |     |               | States |                |     |     |     |
The first future direction is to directly evaluate whether the internal state is control-sufficient.
Z
t
Current benchmarks mainly evaluate generated videos, action prediction scores, long-horizon consis-
tency, or inference efficiency. These are useful proxies, but they do not directly answer the most
important question: does the internal state preserve the information needed for control?
Future work should introduce explicit probes and evaluation protocols for the following variables:
|     |     |     |     |     |     | (cid:8) |           |                | (cid:9) |     | (42) |
| --- | --- | --- | --- | --- | --- | ------- | --------- | -------------- | ------- | --- | ---- |
|     |     |     |     | Z   | −→  | pˆ      | , pˆ      | , pˆ , pˆ , pˆ | ,       |     |      |
|     |     |     |     |     | t   |         | task fail | act risk       | gap     |     |      |
where pˆ denotes predicted task progress, pˆ denotes predicted failure events, pˆ denotes
|     | task |     |     |     |     |     | fail |     |     | act |     |
| --- | ---- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
the predicted future state under a given action, pˆ denotes safety or instability risk, and pˆ
|     |     |     |     |     |     |     |     | risk |     |     | gap |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
denotes the expected discrepancy between imagined and real outcomes. These probes correspond
to measurable components of the physical cost c and the predicted cost J(cid:98)H . Their purpose is to
test whether Z contains the information needed for low-cost decision-making, rather than merely
t
| whether | it  | supports | visually | plausible |     | generation. |     |     |     |     |     |
| ------- | --- | -------- | -------- | --------- | --- | ----------- | --- | --- | --- | --- | --- |
A useful control-sufficient state should support accurate prediction of at least five quantities.
Task progress. For long-horizon tasks, the model should know what has already been completed,
what remains to be done, which subgoal is active, and which future state would count as successful
progress.
The model should identify states that are likely to lead to grasp failure, slip, collision,
| Failure | risk. |     |     |     |     |     |     |     |     |     |     |
| ------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
object drop, unstable contact, wrong-object selection, or task interruption.
84

Given candidate actions, the model should estimate how the object, robot,
Action consequences.
| and task | state | will change. |     |     |     |     |     |     |     |
| -------- | ----- | ------------ | --- | --- | --- | --- | --- | --- | --- |
The state should encode risk related to human proximity, excessive force, collision,
Safety risk.
unstable objects, irreversible state changes, and uncertain physical interaction.
Reality gap. The model should estimate when its imagined future is likely to diverge from real
execution. This is essential for deciding when to trust imagined rollouts and when to request real
| feedback, | additional | sensing, |     | or conservative |     | action. |     |     |     |
| --------- | ---------- | -------- | --- | --------------- | --- | ------- | --- | --- | --- |
A practical evaluation protocol can combine representation probing, rollout prediction, and down-
stream policy evaluation. For example, one can freeze and train lightweight probes for task
Z t
progress, failure, contact state, and rollout discrepancy. If these variables can be predicted from Z ,
t
this provides evidence that the representation contains control-relevant information. More stringent
evaluation should test whether policies or evaluators using outperform policies using visual
Z
t
| embeddings, | language |     | embeddings, |     | or generic | video-generation |     | latents. |     |
| ----------- | -------- | --- | ----------- | --- | ---------- | ---------------- | --- | -------- | --- |
The key metric should not be reconstruction quality alone. Future evaluation should report progress-
prediction accuracy, failure-prediction precision and recall, risk calibration, action prediction error,
and imagined–real discrepancy calibration. These metrics would directly test whether Kairos learns
a state that is sufficient for control rather than merely sufficient for plausible video generation.
| 8.1.2 Counterfactual |     |     | Action | Validation |     |     |     |     |     |
| -------------------- | --- | --- | ------ | ---------- | --- | --- | --- | --- | --- |
The second future direction is to validate counterfactual action prediction. A world model for
Physical AI must answer not only “what will happen next?” but “what will happen if the agent
takes this action, and what would happen under a different action?” This is the requirement of
| counterfactual |     | closure. |     |     |     |     |     |     |     |
| -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
The current Kairos architecture is designed to support this through World Prediction, Video DiT,
Action DiT, mixed attention, and action-only inference (Section 2.1.3). Future work should directly
| test this | capability | under | controlled |     | conditions. |     |     |     |     |
| --------- | ---------- | ----- | ---------- | --- | ----------- | --- | --- | --- | --- |
A rigorous evaluation protocol should begin from the same initial state and execute multiple
| alternative   | actions: |         |                   |         |         |                  |          |            |      |
| ------------- | -------- | ------- | ----------------- | ------- | ------- | ---------------- | -------- | ---------- | ---- |
|               |          |         |                   |         | {a(1),  | a(2), ...,       | a(K)}.   |            | (43) |
| Kairos should |          | predict | the corresponding |         |         | future outcomes: |          |            |      |
|               |          |         |                   | (cid:8) | oˆ (k)  | , aˆ (k)         | , sˆ (k) | (cid:9)K . | (44) |
|               |          |         |                   |         | t+1:t+H | t+1:t+H          | t+H      | k=1        |      |
The robot or simulator should then execute the same actions from matched or carefully reset initial
states to obtain real outcomes {o(k),s(k)}. The evaluation should measure whether the predicted
| outcome | branches | match | the | real outcome |     | branches. |     |     |     |
| ------- | -------- | ----- | --- | ------------ | --- | --------- | --- | --- | --- |
For manipulation, this could include grasp versus push, lift versus slide, fast versus slow movement,
left-side grasp versus right-side grasp, direct placement versus intermediate repositioning, or stop
versus continue under unstable contact. For navigation, it could include turning left versus right,
taking a narrow passage versus detouring, or proceeding versus waiting in a dynamic scene.
Useful metrics include branch classification accuracy, action prediction error, contact outcome
prediction, success/failure prediction under each action, and rank correlation between predicted and
85

real action quality. The model should not only predict a plausible future; it should predict
different
futures for different interventions and preserve the correct ordering of action choices.
This evaluation is essential because observation–action correlation is not enough for deployment.
A model may imitate common actions without understanding their consequences. Counterfactual
validation tests whether Kairos has moved toward action–outcome causation. It will also clarify
when future video generation is necessary and when action-only inference is sufficient. A successful
result would not require perfect pixel-level prediction; what matters is whether Kairos correctly
predicts the control-relevant consequences of each action: whether the object moves as intended,
whether contact is stable, whether the task progresses, whether a failure occurs, and whether the
| predicted risk | matches real | execution. |     |     |     |
| -------------- | ------------ | ---------- | --- | --- | --- |
8.1.3 Interventional Generalization Across Observation, Human Intervention, and Robot Intervention
The third future direction is to evaluate interventional generalization. Kairos is trained through a
Cross-Embodiment Data Curriculum that progresses from passive observation, to intentional human
behavior, to embodied robot interaction. This design is motivated by the fact that Physical AI
deployment is not i.i.d. prediction: once a robot acts, it changes the future data distribution.
Future work should directly test whether CEDC improves generalization across environments, tasks,
and embodiments. The evaluation should be organized around the three intervention levels:
|     |     | D −→ | D −→  | D .   | (45) |
| --- | --- | ---- | ----- | ----- | ---- |
|     |     | obs  | human | robot |      |
Passive observation. At the first level, large-scale passive observation data should provide broad
physicalandsemanticpriors. Evaluationshouldtestwhethermodelstrainedwithsuchdatageneralize
better to unseen objects, unseen scenes, and unseen physical phenomena.
At the second level, human-centric data should provide intentional task
| Human intervention. |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- |
structure. Evaluation should test whether human-centric pretraining improves instruction following,
task decomposition, long-horizon planning, recovery behavior, and object manipulation priors.
Robot intervention. At the third level, robot data should provide embodiment-specific action
grounding. Evaluation should test whether adding robot data improves action prediction, contact
stability, success rate, and adaptation to robot-specific control constraints.
| A strong evaluation | design | should compare | several training | regimes: |     |
| ------------------- | ------ | -------------- | ---------------- | -------- | --- |
| •                   | only;  |                |                  |          |     |
D
obs
| •   | ;     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- |
| D   | +D    |     |     |     |     |
| obs | human |     |     |     |     |
| •   | only; |     |     |     |     |
D
robot
| • flat mixture |       |             | (no curriculum); |     |     |
| -------------- | ----- | ----------- | ---------------- | --- | --- |
|                | D ∪D  | ∪D          |                  |     |     |
|                | obs   | human robot |                  |     |     |
| • full staged  | CEDC. |             |                  |     |     |
The goal is to determine whether the full curriculum improves generalization beyond any single data
| source or flat | mixture. |     |     |     |     |
| -------------- | -------- | --- | --- | --- | --- |
Future benchmarks should test (new backgrounds, lighting, layouts,
|     |     | cross-environment | generalization |     |     |
| --- | --- | ----------------- | -------------- | --- | --- |
scenes), (new task combinations, object categories, instruction composi-
cross-task generalization
tions), and cross-embodiment generalization (across grippers, arms, dexterous hands, humanoid
86

platforms, camera viewpoints, action spaces). Key metrics should include action success rate, action
prediction accuracy, task-progress prediction, failure prediction, data efficiency, and robustness under
perturbation. The strongest evidence would show that CEDC improves not only benchmark scores
but also action prediction and policy robustness under intervention-induced distribution shift.
| 8.1.4 Multi-Timescale |     | Memory | Beyond | 15-Second | Generation |     |
| --------------------- | --- | ------ | ------ | --------- | ---------- | --- |
The fourth future direction is to extend multi-timescale memory evaluation beyond 15-second video
consistency. The current long-horizon evaluation (Section 6.5) shows that Kairos can preserve
scene consistency and physical interaction over extended video generation. However, real Physical
AI tasks often last much longer than 15 seconds. Household manipulation, warehouse operation,
mobile navigation, inspection, care assistance, and human–robot collaboration may require state
| maintenance | over minutes, | hours, | or  | even longer | periods. |     |
| ----------- | ------------- | ------ | --- | ----------- | -------- | --- |
Future work should therefore evaluate memory at multiple temporal scales:
|     |     | seconds | →   | minutes | → hours → day-scale. | (46) |
| --- | --- | ------- | --- | ------- | -------------------- | ---- |
The model should maintain local contact dynamics, motion continuity, slip, collision,
| Seconds       | scale. |               |     |     |     |     |
| ------------- | ------ | ------------- | --- | --- | --- | --- |
| and immediate | action | consequences. |     |     |     |     |
Minutes scale. The model should maintain subtask progress, object locations, tool-use history,
| and intermediate | task | dependencies. |     |     |     |     |
| ---------------- | ---- | ------------- | --- | --- | --- | --- |
Hours scale. The model should maintain environment changes, repeated interaction patterns, user
| preferences, | task schedules, |     | and accumulated | uncertainty. |     |     |
| ------------ | --------------- | --- | --------------- | ------------ | --- | --- |
Day-scale or longer. The model should maintain persistent world knowledge, repeated failure
| patterns, | scene regularities, |     | and long-term | adaptation | signals. |     |
| --------- | ------------------- | --- | ------------- | ---------- | -------- | --- |
Future benchmarks should move beyond long video generation and test real task-state memory. For
example, a robot may be asked to complete a multi-step household task where some objects are
moved, hidden, or used earlier and become relevant later. The model should remember which objects
were moved, which subtasks were completed, which failures occurred, and which recovery strategies
were attempted. Another benchmark could test navigation memory, where a robot must integrate
observations across many rooms and preserve spatial–semantic state over extended exploration.
Useful metrics include object permanence accuracy, subtask-state tracking, delayed-effect prediction,
task-history recall, recovery-history use, and long-horizon action success. For real robot deployment,
the model should be tested on whether memory improves action selection, reduces repeated mistakes,
| and supports | recovery | after | delayed | failures. |     |     |
| ------------ | -------- | ----- | ------- | --------- | --- | --- |
This direction should also evaluate the roles of the three temporal pathways in Kairos. Sliding-
Window Attention should be tested on fast local dynamics; Dilated Sliding-Window Attention on
mid-range event dependencies; Gated Linear Attention on persistent global context. Ablations
should measure which memory branch is necessary for which temporal scale and task type. As
future work, this defines a staged evaluation path from 15-second generation consistency toward real
| long-horizon                      | state maintenance |     | in Physical | AI.    |     |     |
| --------------------------------- | ----------------- | --- | ----------- | ------ | --- | --- |
| 8.1.5 Control-Information-Density |                   |     | Data        | Engine |     |     |
The fifth future direction is to develop a more explicit control-information-density data engine. The
current Kairos data pipeline (Section 4) already supports large-scale collection, curation, tagging,
87

captioning, enhanced text annotation, and high-throughput processing. The next step is to make
| data selection | more | directly aligned | with | control | value. |     |
| -------------- | ---- | ---------------- | ---- | ------- | ------ | --- |
The key principle is that not all data contributes equally to Physical AI. A short near-boundary
failure or recovery clip may teach more about control than a long ordinary success clip, but not
every failure should be treated as maximally valuable. Future data construction should therefore
| follow the | priority | order: |     |     |     |     |
| ---------- | -------- | ------ | --- | --- | --- | --- |
near-boundary failure and recovery data near-boundary successful data
>
|     | > contact-rich | data        | > ordinary |     | successful trajectories | (47) |
| --- | -------------- | ----------- | ---------- | --- | ----------------------- | ---- |
|     | ordinary       | observation | videos,    |     |                         |      |
>
Near-boundary failure and recovery data should include marginal grasp failures, object slips
close to recovery, near collisions, unstable contacts, regrasping, repositioning, replanning, human
correction, retry behavior, and successful return from error states. These data reveal where execution
| breaks within | the normal | task | regime | and how | the agent can recover. |     |
| ------------- | ---------- | ---- | ------ | ------- | ---------------------- | --- |
Near-boundary successful data should include marginal grasps that remain stable, near slips
that are corrected, near collisions that are avoided, partial successes completed through correction,
and other cases close to the decision boundary between success and failure. These data reveal the
conditions under which the system remains controllable near failure or safety margins.
Contact-rich data should include tactile events, force interaction, friction, deformation, sliding,
tool use, support changes, and grasp stability. These data reveal the physical mechanisms through
| which actions | affect | the world. |     |     |     |     |
| ------------- | ------ | ---------- | --- | --- | --- | --- |
Ordinary successful trajectories and ordinary observation videos remain useful—they provide task
execution examples and broad physical priors. Extreme, non-diagnostic, or far out-of-distribution
failures may be useful for safety filtering and anomaly detection, but they should not dominate the
data pipeline if the goal is learning action consequences, failure boundaries, and recovery strategies.
A future Kairos data engine should explicitly estimate or approximate control information density.
This can be done through event detectors, robot logs, simulation labels, tactile–force signals, human
annotation, rollout discrepancy, and model uncertainty. Each data segment can be scored by how
much it reduces uncertainty about action outcomes, failure boundaries, contact dynamics, recovery
| strategies, | or safety | risks. |     |     |     |     |
| ----------- | --------- | ------ | --- | --- | --- | --- |
Future work should also align ego-centric human data, robot trajectories, and simulation data around
shared event labels. For example, a slip event in human hand–object interaction, a robot gripper slip,
and a simulator-labeled friction failure should be mapped into a common contact-failure taxonomy.
This would allow Kairos to learn from human, robot, and simulated experience in a more unified
way.
Thedataengineshouldsupportthreedownstreamcapabilities: (1)itshouldimprovefailureprediction
by providing enough examples of how and why actions fail; (2) it should improve safety filtering by
exposing unsafe, near-unsafe, and high-uncertainty states; (3) it should improve recovery behavior
| by teaching | the model | what to | do after | an error | occurs. |     |
| ----------- | --------- | ------- | -------- | -------- | ------- | --- |
The long-term goal is to close the data loop. Kairos should not only train on static datasets. It should
eventually use real deployment feedback to identify high-value data segments, prioritize annotation,
update the world-action model, and improve future policy evaluation. This would turn the data
| engine into | a continuous | source | of control-relevant |     | learning signal. |     |
| ----------- | ------------ | ------ | ------------------- | --- | ---------------- | --- |
88

8.2 Outlook
The next stage of Kairos should be evaluated by a stricter standard than visual generation quality
alone. A Physical AI world model should be judged by whether its internal state predicts task
progress, whether it distinguishes the consequences of different actions, whether it generalizes across
intervention distributions, whether it maintains state over real task horizons, and whether its data
engine improves failure prediction, safety filtering, and recovery. Kairos has established a foundation
for this direction through its cross-embodiment curriculum, native world-action architecture, hybrid
temporal memory, deployment-aware inference, and scalable data pipeline. The central future
question is no longer whether Kairos can generate plausible futures, but whether its imagined futures
and internal states can be reliably connected to real physical outcomes.
By pursuing the five directions above, Kairos can move from proxy world-action modeling toward
directly validated regret-aware Physical AI. This progression requires careful experiments, calibrated
evaluation, and real robot validation. If successful, future Kairos systems will provide a practical
path toward physical agents that learn from heterogeneous experience, predict action consequences,
anticipate failures, recover from mistakes, and improve through grounded feedback.
89

References
[1] Jiahua Dong, Qi Lyu, Baichen Liu, Xudong Wang, Wenqi Liang, Duzhen Zhang, Jiahang Tu, Hongliu
Li, Hanbin Zhao, Henghui Ding, Yulun Zhang, Zhi Han, Nicu Sebe, Fahad Shahbaz Khan, Salman
Khan, Mubarak Shah, Philip Torr, Ming-Hsuan Yang, and Dacheng Tao. Learning to model the world:
| A survey | of  | world models | in artificial |     | intelligence. |     | TechRxiv, | 2026. |     |
| -------- | --- | ------------ | ------------- | --- | ------------- | --- | --------- | ----- | --- |
[2] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr,
Joe Taylor, Troy Vickrey, Linas Fedarevičius, Huiwen Chang, Rui Zhang, Zheng Yan, Wei Wei,
and Yang Song. Video generation models as world simulators. https://openai.com/index/
| video-generation-models-as-world-simulators/, |     |     |     |     |     |     | 2024. | OpenAI | Blog. |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | ----- | ------ | ----- |
[3] NVIDIA, Arslan Ali, Junjie Bai, Maciej Bala, Yogesh Balaji, Aaron Blakeman, Tiffany Cai, Jiaxin
Cao, Tianshi Cao, Elizabeth Cha, Yu-Wei Chao, Prithvijit Chattopadhyay, Mike Chen, Yongxin Chen,
Yu Chen, Shuai Cheng, Yin Cui, Jenna Diamond, Yifan Ding, Jiaojiao Fan, Linxi Fan, Liang Feng,
Francesco Ferroni, Sanja Fidler, Xiao Fu, Ruiyuan Gao, Yunhao Ge, Jinwei Gu, Aryaman Gupta,
Siddharth Gururani, Imad El Hanafi, Ali Hassani, Zekun Hao, Jacob Huffman, Joel Jang, Pooya
Jannaty, Jan Kautz, Grace Lam, Xuan Li, Zhaoshuo Li, Maosheng Liao, Chen-Hsuan Lin, Tsung-Yi
Lin, Yen-Chen Lin, Huan Ling, Ming-Yu Liu, Xian Liu, Yifan Lu, Alice Luo, Qianli Ma, Hanzi Mao,
KaichunMo, SeungjunNah, YashrajNarang, AbhijeetPanaskar, LindseyPavao, TrungPham, Morteza
Ramezanali, Fitsum Reda, Scott Reed, Xuanchi Ren, Haonan Shao, Yue Shen, Stella Shi, Shuran Song,
Bartosz Stefaniak, Shangkun Sun, Shitao Tang, Sameena Tasmeen, Lyne Tchapmi, Wei-Cheng Tseng,
Jibin Varghese, Andrew Z. Wang, Hao Wang, Haoxiang Wang, Heng Wang, Ting-Chun Wang, Fangyin
Wei, Jiashu Xu, Dinghao Yang, Xiaodong Yang, Haotian Ye, Seonghyeon Ye, Xiaohui Zeng, Jing Zhang,
Qinsheng Zhang, Kaiwen Zheng, Andrew Zhu, and Yuke Zhu. World simulation with video foundation
| models | for physical | ai, | 2025. |     |     |     |     |     |     |
| ------ | ------------ | --- | ----- | --- | --- | --- | --- | --- | --- |
[4] Kuaishou Technology. Kling ai: A next-generation video generation model. https://klingai.com/,
2024.
[5] Luma AI. Dream machine: High-quality video generation from text and images. https://lumalabs.
| ai/dream-machine, |             | 2024. | Luma   | AI  | Official | Website. |           |             |     |
| ----------------- | ----------- | ----- | ------ | --- | -------- | -------- | --------- | ----------- | --- |
| [6] Runway.       | Introducing | gen-3 | alpha: | A   | new      | frontier | for video | generation. |     |
https://runwayml.com/blog/
| introducing-gen-3-alpha/, |     |     |     | 2024. | Runway | Blog. |     |     |     |
| ------------------------- | --- | --- | --- | ----- | ------ | ----- | --- | --- | --- |
[7] ByteDanceSeedTeam. Seedance(danceseed): Unifiedmultimodalfoundationmodelforvideosynthesis.
https://seed.bytedance.com/seedance, 2025. ByteDance Technical Report.
[8] DanKondratyuk,LijunYu,XiuyeGu,JoséLezama,JonathanHuang,GrantSchindler,RachelHornung,
Vighnesh Birodkar, Jimmy Yan, Ming-Chang Chiu, et al. Videopoet: A large language model for
| zero-shot | video | generation. | arXiv | preprint |     | arXiv:2312.14125, |     | 2023. |     |
| --------- | ----- | ----------- | ----- | -------- | --- | ----------------- | --- | ----- | --- |
[9] Hansi Teng, Hongyu Jia, Lei Sun, Lingzhi Li, Maolin Li, Mingqiu Tang, Shuai Han, Tianning Zhang,
WQ Zhang, Weifeng Luo, et al. Magi-1: Autoregressive video generation at scale. arXiv preprint
| arXiv:2505.13211, |     | 2025. |     |     |     |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
[10] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. Advances in
| neural | information | processing |     | systems, | 33:6840–6851, |     | 2020. |     |     |
| ------ | ----------- | ---------- | --- | -------- | ------------- | --- | ----- | --- | --- |
[11] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J Fleet.
Video diffusion models. Advances in neural information processing systems, 35:8633–8646, 2022.
[12] Jonathan Ho, William Chan, Chitwan Saharia, Jay Whang, Ruiqi Gao, Alexey Gritsenko, Diederik P
Kingma, Ben Poole, Mohammad Norouzi, David J Fleet, et al. Imagen video: High definition video
| generation | with | diffusion | models. | arXiv | preprint |     | arXiv:2210.02303, |     | 2022. |
| ---------- | ---- | --------- | ------- | ----- | -------- | --- | ----------------- | --- | ----- |
[13] Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, Qiyuan Hu, Harry Yang,
90

OronAshual, OranGafni, etal. Make-a-video: Text-to-videogenerationwithouttext-videodata. arXiv
| preprint arXiv:2209.14792, |     |     | 2022. |     |     |     |     |
| -------------------------- | --- | --- | ----- | --- | --- | --- | --- |
[14] Daquan Zhou, Weimin Wang, Hanshu Yan, Weiwei Lv, Yizhe Zhu, and Jiashi Feng. Magicvideo:
Efficient video generation with latent diffusion models. arXiv preprint arXiv:2211.11018, 2022.
[15] Yaohui Wang, Xinyuan Chen, Xin Ma, Shangchen Zhou, Ziqi Huang, Yi Wang, Ceyuan Yang, Yinan
He, JiashuoYu, PeiqingYang, etal. Lavie: High-qualityvideogenerationwithcascadedlatentdiffusion
| models. International |     | Journal | of Computer |     | Vision, 133(5):3059–3078, |     | 2025. |
| --------------------- | --- | ------- | ----------- | --- | ------------------------- | --- | ----- |
[16] Weijie Kong, Qi Tian, Zijian Zhang, Rox Min, Zuozhuo Dai, Jin Zhou, Jiangfeng Xiong, Xin Li, Bo Wu,
Jianwei Zhang, et al. Hunyuanvideo: A systematic framework for large video generative models. arXiv
| preprint arXiv:2412.03603, |     |     | 2024. |     |     |     |     |
| -------------------------- | --- | --- | ----- | --- | --- | --- | --- |
[17] Yoav HaCohen, Nisan Chiprut, Benny Brazowski, Daniel Shalem, Dudu Moshe, Eitan Richardson,
Eran Levin, Guy Shiran, Nir Zabari, Ori Gordon, et al. Ltx-video: Realtime video latent diffusion.
| arXiv preprint | arXiv:2501.00103, |     | 2024. |     |     |     |     |
| -------------- | ----------------- | --- | ----- | --- | --- | --- | --- |
[18] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes,
Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive
environments. In Forty-first International Conference on Machine Learning, 2024.
[19] Ze Yang, Yun Chen, Jingkang Wang, Sivabalan Manivasagam, Wei-Chiu Ma, and Raquel Urtasun.
| Unisim: A | neural | closed-loop | sensor | simulator. | In CVPR, | 2023. |     |
| --------- | ------ | ----------- | ------ | ---------- | -------- | ----- | --- |
[20] David Ha and Jürgen Schmidhuber. World models. arXiv preprint arXiv:1803.10122, 2(3):440, 2018.
[21] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Learning latent dynamics for
| planning | from pixels. | In ICML, | 2019. |     |     |     |     |
| -------- | ------------ | -------- | ----- | --- | --- | --- | --- |
[22] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning
| behaviors | by latent | imagination. | arXiv | preprint | arXiv:1912.01603, |     | 2019. |
| --------- | --------- | ------------ | ----- | -------- | ----------------- | --- | ----- |
[23] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete
| world models. | arXiv | preprint | arXiv:2010.02193, |     | 2020. |     |     |
| ------------- | ----- | -------- | ----------------- | --- | ----- | --- | --- |
[24] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains
| through world | models. | arXiv | preprint | arXiv:2301.04104, |     | 2023. |     |
| ------------- | ------- | ----- | -------- | ----------------- | --- | ----- | --- |
[25] Mahmoud Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba Komeili,
Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha
Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick
Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath
Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, and Nicolas Ballas. V-jepa 2: Self-supervised
video models enable understanding, prediction and planning. arXiv preprint arXiv:2506.09985, 2025.
[26] Lorenzo Mur-Labadia, Matthew Muckley, Amir Bar, Mahmoud Assran, Koustuv Sinha, Michael
Rabbat, Yann LeCun, Nicolas Ballas, and Adrien Bardes. V-jepa 2.1: Unlocking dense features in video
| self-supervised | learning. | arXiv | preprint | arXiv:2603.14482, |     | 2026. |     |
| --------------- | --------- | ----- | -------- | ----------------- | --- | ----- | --- |
[27] Federico Baldassarre, Marc Szafraniec, Basile Terver, Vasil Khalidov, Francisco Massa, Yann LeCun,
Patrick Labatut, Maximilian Seitzer, and Piotr Bojanowski. Back to the features: Dino as a foundation
| for video | world models, | 2025. |     |     |     |     |     |
| --------- | ------------- | ----- | --- | --- | --- | --- | --- |
[28] Nicklas Hansen, Xiaolong Wang, and Hao Su. Temporal difference learning for model predictive control.
| In International | Conference |     | on Machine | Learning, | PMLR, | 2022. |     |
| ---------------- | ---------- | --- | ---------- | --------- | ----- | ----- | --- |
[29] Danijar Hafner, Wilson Yan, and Timothy Lillicrap. Training agents inside of scalable world models,
2025.
91

[30] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott
Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. arXiv
| preprint | arXiv:2001.08361, |     | 2020. |     |     |
| -------- | ----------------- | --- | ----- | --- | --- |
[31] World Labs. Marble: A multimodal world model. https://marble.worldlabs.ai/, 2025.
[32] Yabo Chen, Yuanzhi Liang, Jiepeng Wang, Tingxi Chen, Junfei Cheng, Zixiao Gu, Yuyang Huang,
Zicheng Jiang, Wei Li, Tian Li, Weichen Li, Zuoxin Li, Guangce Liu, Jialun Liu, Junqi Liu, Haoyuan
Wang, Qizhen Weng, Xuan’er Wu, Xunzhi Xiang, Xiaoyan Yang, Xin Zhang, Shiwen Zhang, Junyu
Zhou, Chengcheng Zhou, Haibin Huang, Chi Zhang, and Xuelong Li. Teleworld: Towards dynamic
| multimodal | synthesis | with a | 4d world model, | 2025. |     |
| ---------- | --------- | ------ | --------------- | ----- | --- |
[33] Google DeepMind. Genie 3: A new frontier for world models. https://deepmind.google/blog/
| genie-3-a-new-frontier-for-world-models/, |     |     |     | 2025. |     |
| ----------------------------------------- | --- | --- | --- | ----- | --- |
[34] Team HunyuanWorld. Hy-world 1.5: A systematic framework for interactive world modeling with
| real-time | latency and | geometric | consistency. | arXiv preprint, | 2025. |
| --------- | ----------- | --------- | ------------ | --------------- | ----- |
[35] Robbyant Team. Lingbot-world: An interactive world model for embodied intelligence. arXiv preprint,
| January | 2026. Ant | Group Robbyant | Technology. |     |     |
| ------- | --------- | -------------- | ----------- | --- | --- |
[36] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao
Feng, Chendong Xiang, Yinze Rong, et al. Motus: A unified latent action world model. arXiv preprint
| arXiv:2512.13030, | 2025. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
[37] Jun Cen, Siteng Huang, Yuqian Yuan, Kehan Li, Hangjie Yuan, Chaohui Yu, Yuming Jiang, Jiayan
Guo, Xin Li, Hao Luo, et al. Rynnvla-002: A unified vision-language-action and world model. arXiv
| preprint | arXiv:2511.17502, |     | 2025. |     |     |
| -------- | ----------------- | --- | ----- | --- | --- |
[38] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song,
Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. arXiv preprint
| arXiv:2506.21539, | 2025. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
[39] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao
Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale
| knowledge | for robot | manipulation. | arXiv | preprint arXiv:2410.06158, | 2024. |
| --------- | --------- | ------------- | ----- | -------------------------- | ----- |
[40] Yueci Deng, Guiliang Liu, and Kui Jia. Dexworldmodel: Causal latent world modeling towards
automated learning of embodied tasks. arXiv preprint arXiv:2604.16484, 2026.
[41] PhysicalIntelligence,BoAi,AliAmin,RaichelleAniceto,AshwinBalakrishna,GregBalke,KevinBlack,
George Bokinsky, Shihao Cao, Thomas Charbonnier, Vedant Choudhary, Foster Collins, Ken Conley,
Grace Connors, James Darpinian, Karan Dhabalia, Maitrayee Dhaka, Jared DiCarlo, Danny Driess,
Michael Equi, Adnan Esmail, Yunhao Fang, Chelsea Finn, Catherine Glossop, Thomas Godden, Ivan
Goryachev,LachlanGroom,HarounHabeeb,HunterHancock,KarolHausman,GashonHussein,Victor
Hwang, Brian Ichter, Connor Jacobsen, Szymon Jakubczak, Rowan Jen, Tim Jones, Gregg Kammerer,
Ben Katz, Liyiming Ke, Mairbek Khadikov, Chandra Kuchi, Marinda Lamb, Devin LeBlanc, Brendon
LeCount, Sergey Levine, Xinyu Li, Adrian Li-Bell, Vladislav Lialin, Zhonglin Liang, Wallace Lim, Yao
Lu, Enyu Luo, Vishnu Mano, Nandan Marwaha, Aikys Mongush, Liam Murphy, Suraj Nair, Tyler
Patterson, Karl Pertsch, Allen Z. Ren, Gavin Schelske, Charvi Sharma, Baifeng Shi, Lucy Xiaoyang
Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, Will Stoeckle, Jiaming Tang, Jimmy
Tanner, Shalom Tekeste, Marcel Torne, Kyle Vedder, Quan Vuong, Anna Walling, Haohuan Wang,
Jason Wang, XuDong Wang, Chris Whalen, Samuel Whitmore, Blake Williams, Charles Xu, Sukwon
Yoo, Lili Yu, Wuming Zhang, Zhuoyang Zhang, and Ury Zhilinsky. π : a steerable generalist robotic
0.7
| foundation | model with | emergent | capabilities, | 2026. |     |
| ---------- | ---------- | -------- | ------------- | ----- | --- |
[42] Yichao Shen, Fangyun Wei, Zhiying Du, Yaobo Liang, Yan Lu, Jiaolong Yang, Nanning Zheng, and
Baining Guo. Videovla: Video generators can be generalizable robot manipulators. Advances in neural
| information | processing | systems, | 38:95597–95621, | 2026. |     |
| ----------- | ---------- | -------- | --------------- | ----- | --- |
92

[43] Ge Yuan, Qiyuan Qiao, Jing Zhang, and Dong Xu. Adaworldpolicy: World-model-driven diffusion
policy with online adaptive learning for robotic manipulation. arXiv preprint arXiv:2602.20057, 2026.
[44] ZiyangGong,ZehangLuo,AnkeTang, ZheLiu,ShiFu,ZhiHou, GanlinYang, WeiyunWang,Xiaofeng
Wang, Jianbo Liu, Gen Luo, Haolan Kang, Shuang Luo, Yue Zhou, Yong Luo, Li Shen, Xiaosong Jia,
Yao Mu, Xue Yang, Chunxiao Liu, Junchi Yan, Hengshuang Zhao, Dacheng Tao, and Xiaogang Wang.
Ace-brain-0: Spatial intelligence as a shared scaffold for universal embodiments, 2026.
[45] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran
Song, Ming-Yu Liu, Chelsea Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor
control and planning. arXiv preprint arXiv:2601.16163, 2026.
[46] Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck, Yu Fang, Fengyuan Hu, Joel Jang, Kaushil
Kundalia, Zongyu Lin, Loic Magne, et al. Flare: Robot learning with implicit world modeling. arXiv
preprint arXiv:2505.15659, 2025.
[47] Yilun Du, Sherry Yang, Pete Florence, Fei Xia, Ayzaan Wahid, Pierre Sermanet, Tianhe Yu, Pieter
Abbeel, Joshua B Tenenbaum, Leslie Kaelbling, et al. Video language planning. In International
Conference on Learning Representations, volume 2024, pages 31138–31155, 2024.
[48] Homanga Bharadhwaj, Roozbeh Mottaghi, Abhinav Gupta, and Shubham Tulsiani. Track2act: Predict-
ing point tracks from internet videos enables generalizable robot manipulation. In European Conference
on Computer Vision, pages 306–324. Springer, 2024.
[49] Hongyan Zhi, Peihao Chen, Siyuan Zhou, Yubo Dong, Quanxi Wu, Lei Han, and Mingkui Tan.
3dflowaction: Learning cross-embodiment manipulation from 3d flow world model. arXiv preprint
arXiv:2506.06199, 2025.
[50] Po-Chen Ko, Jiayuan Mao, Yilun Du, Shao-Hua Sun, and Joshua B Tenenbaum. Learning to act
from actionless videos through dense correspondences. In International Conference on Learning
Representations, volume 2024, pages 40938–40958, 2024.
[51] Nilaksh, Saurav Jha, Artem Zholus, and Sarath Chandar. Reconstruction or semantics? what makes a
latent space useful for robotic world models. arXiv preprint arXiv:2605.06388, 2026.
[52] Aditi, Niket Agarwal, Arslan Ali, Jon Allen, Martin Antolini, Adeline Aubame, Alisson Azzolini, Junjie
Bai, Maciej Bala, Yogesh Balaji, Josh Bapst, Aarti Basant, Mukesh Beladiya, Mohammad Qazim Bhat,
Zaid Pervaiz Bhat, Dan Blick, Vanni Brighella, Han Cai, Tiffany Cai, Eric Cameracci, Jiaxin Cao,
Yulong Cao, Mark Carlson, Carlos Casanova, Ting-Yun Chang, Yan Chang, Yu-Wei Chao, Prithvijit
Chattopadhyay, Roshan Chaudhari, Chieh-Yun Chen, Junyu Chen, Ke Chen, Qizhi Chen, Wenkai
Chen, Xiaotong Chen, Yu Chen, An-Chieh Cheng, Click Cheng, Xiu Chia, Jeana Choi, Chaeyeon
Chung, Wenyan Cong, Yin Cui, Magdalena Dadela, Nalin Dadhich, Wenliang Dai, Joyjit Daw, Alperen
Degirmenci, Rodrigo Vieira Del Monte, Robert Denomme, Sameer Dharur, Marco Di Lucca, Ke Ding,
Wenhao Ding, Yifan Ding, Yuzhu Dong, Nicole Drumheller, Yilun Du, Aigul Dzhumamuratova,
Aleksandr Efitorov, Hamid Eghbalzadeh, Naomi Eigbe, Imad El Hanafi, Hassan Eslami, Benedikt Falk,
Jiaojiao Fan, Jim Fan, Amol Fasale, Sergiy Fefilatyev, Liang Feng, Francesco Ferroni, Sanja Fidler,
Xiao Fu, Vikram Fugro, Prashant Gaikwad, TJ Galda, Katelyn Gao, Yihuai Gao, Wenhang Ge, Sreyan
Ghosh, Arushi Goel, Vivek Goel, Akash Gokul, Rama Govindaraju, Jinwei Gu, Miguel Guerrero, Elfie
Guo, Aryaman Gupta, Siddharth Gururani, Hugo Hadfield, Song Han, Ankur Handa, Zekun Hao,
Mohammad Harrim, Ali Hassani, Nathan Hayes-Roth, Yufan He, Chris Helvig, Cyrus Hogg, Madison
Huang, Michael Huang, Sophia Huang, Yufan Huang, Jacob Huffman, DeLesley Hutchins, Suneel
Indupuru, Boris Ivanovic, Arihant Jain, Joel Jang, Ryan Ji, Yanan Jian, Dongfu Jiang, Jingyi Jin,
Atharva Joshi, Nikhilesh Joshi, Pranjali Joshi, Jaehun Jung, Weiwei Kang, Scott Kassekert, Jan Kautz,
Ashna Khetan, Julia Kiczka, Slawek Kierat, Gwanghyun Kim, Kuno Kim, Sunny Kim, Kezhi Kong,
Xin Kong, Zhifeng Kong, Tomasz Kornuta, Egor Krivov, Hui Kuang, Saurav Kumar, Chia-Wen Kuo,
George Kurian, Wojciech Kutak, JF Lafleche, Himangshu Lahkar, Omar Laymoun, Jayjun Lee, Sanggil
Lee, Gabriele Leone, Boyi Li, Freya Li, Jiajun Li, Jinfeng Li, Ling Li, Pengcheng Li, Shangru Li, Tingle
Li, XiaolongLi, XuanLi, ZhaoshuoLi, ZhiqiLi, HaoLiang, MaoshengLiao, Chen-HsuanLin, Tsung-Yi
93

Lin, Ming-Yu Liu, Sifei Liu, Zihan Liu, Hai Loc Lu, Xiangyu Lu, Alice Luo, Ruipu Luo, Wenjie Luo,
Jiangran Lyu, Martin Ding Ma, Nic Ma, Qianli Ma, Dawid Majchrowski, Louis Marcoux, Miguel
Martin, Qing Miao, Ashkan Mirzaei, Shreyas Misra, Kaichun Mo, Durra Mohsin, Hyejin Moon, Pawel
Morkisz, Saeid Motiian, Kirill Motkov, Seungjun Nah, Yashraj Narang, Deepak Narayanan, Thabang
Ngazimbi, Julian Ouyang, David Page, Yatian Pang, Sehwi Park, Mahesh Patekar, Mostofa Patwary,
Marco Pavone, Trung Pham, Wei Ping, Soha Pouya, Shrimai Prabhumoye, Varun Praveen, Delin Qu,
Hesam Rabeti, Morteza Ramezanali, Marilyn Reeb, Xuanchi Ren, Kristen Rumley, Wojciech Rymer,
JunSaito, YeonghoSeol, JohnShao, PiyushShekdar, TianweiShen, HumphreyShi, MinShi, StellaShi,
Kevin Shih, Mohammad Shoeybi, Mateusz Sieniawski, Shuran Song, Alexander Sotelo, Amir Sotoodeh,
Sunil Srinivasa, Vignesh Srinivasakumar, Bartosz Stefaniak, Rahul Heinrich Steiger, Shangkun Sun,
Jiaxiang Tang, Shitao Tang, Yangyang Tang, Yue Tang, Tolou Tavakkoli, Kayley Ting, Krzysztof
Tomala, Wei-Cheng Tseng, Jibin Varghese, Sergei Vasilev, Thomas Volk, Raju Wagwani, Roger Waleffe,
Andrew Z. Wang, Boxiang Wang, Haoxiang Wang, Qiao Wang, Shihao Wang, Shijie Wang, Ting-Chun
Wang, Yan Wang, Yu Wang, David Wehr, Fangyin Wei, Xinshuo Weng, Jay Zhangjie Wu, Kedi Wu,
Hongchi Xia, Summer Xiao, Tianjun Xiao, Kevin Xie, Daguang Xu, Jiashu Xu, Mengyao Xu, Ruqing
Xu, Xingqian Xu, Yao Xu, Dinghao Yang, Dong Yang, Hans Yang, Xiaodong Yang, Xuning Yang,
Yichu Yang, Yurong You, Zhiding Yu, Hao Yuan, Simon Yuen, Xiaohui Zeng, Pengcuo Zeren, Cindy
Zha, Haotian Zhang, Jenny Zhang, Jing Zhang, Liangkai Zhang, Paris Zhang, Shun Zhang, Xuanmeng
Zhang, Zhizheng Zhang, Ann Zhao, Yilin Zhao, Yuliya Zhautouskaya, Charles Zhou, Fengzhe Zhou,
Shilin Zhu, Yuke Zhu, Dima Zhylko, and Artur Zolkowski. Cosmos 3: Omnimodal world models for
physical ai, 2026.
[53] MotuBrain Team, Chendong Xiang, Fan Bao, Haitian Liu, Hengkai Tan, Hongzhe Bi, James Li, Jiabao
Liu, Jingrui Pang, Kiro Jing, et al. Motubrain: An advanced world action model for robot control.
arXiv preprint arXiv:2604.27792, 2026.
[54] Songlin Yang, Jan Kautz, and Ali Hatamizadeh. Gated delta networks: Improving mamba2 with delta
rule. In The Thirteenth International Conference on Learning Representations.
[55] Dacheng Li, Yunhao Fang, Yukang Chen, Shuo Yang, Shiyi Cao, Justin Wong, Michael Luo, Xiaolong
Wang, Hongxu Yin, Joseph E Gonzalez, et al. Worldmodelbench: Judging video generation models as
world models. arXiv preprint arXiv:2502.20694, 2025.
[56] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer
Huang, Kaushil Kundalia, Yen-Chen Lin, et al. Dreamgen: Unlocking generalization in robot learning
through video world models. arXiv preprint arXiv:2505.12705, 2025.
[57] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang
Lin, YihengGe, ZhenyuGu, etal. Robotwin2.0: Ascalabledatageneratorandbenchmarkwithstrong
domain randomization for robust bimanual robotic manipulation. arXiv preprint arXiv:2506.18088,
2025.
[58] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo
Zhang, Zhaoye Fei, Jinlan Fu, Jingjing Gong, and Xipeng Qiu. Libero-plus: In-depth robustness
analysis of vision-language-action models. arXiv preprint arXiv:2510.13626, 2025.
[59] Qwen Team. Qwen2.5-vl, January 2025.
[60] Qwen Team. Qwen3.5: Towards native multimodal agents, February 2026.
[61] William Peebles and Saining Xie. Scalable diffusion models with transformers. In Proceedings of the
IEEE/CVF international conference on computer vision, pages 4195–4205, 2023.
[62] Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need
test-time future imagination? arXiv preprint arXiv:2603.16666, 2026.
[63] Maximilian Beck, Korbinian Pöppel, Markus Spanring, Andreas Auer, Oleksandra Prudnikova, Michael
Kopp, Günter Klambauer, Johannes Brandstetter, and Sepp Hochreiter. xlstm: Extended long short-
term memory. Advances in Neural Information Processing Systems, 37:107547–107603, 2024.
94

[64] Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever. Generating long sequences with sparse
transformers. arXiv preprint arXiv:1904.10509, 2019.
[65] Iz Beltagy, Matthew E Peters, and Arman Cohan. Longformer: The long-document transformer. arXiv
preprint arXiv:2004.05150, 2020.
[66] Manzil Zaheer, Guru Guruganesh, Kumar Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago
Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, et al. Big bird: Transformers for longer
sequences. Advances in neural information processing systems, 33:17283–17297, 2020.
[67] Tri Dao and Albert Gu. Transformers are ssms: Generalized models and efficient algorithms through
structured state space duality. arXiv preprint arXiv:2405.21060, 2024.
[68] Tobias Katsch. Gateloop: Fully data-controlled linear recurrence for sequence modeling. arXiv preprint
arXiv:2311.01927, 2023.
[69] Songlin Yang, Bailin Wang, Yikang Shen, Rameswar Panda, and Yoon Kim. Gated linear attention
transformers with hardware-efficient training. arXiv preprint arXiv:2312.06635, 2023.
[70] Zhen Qin, Songlin Yang, and Yiran Zhong. Hierarchically gated recurrent neural network for sequence
modeling. Advances in Neural Information Processing Systems, 36:33202–33221, 2023.
[71] Zhen Qin, Songlin Yang, Weixuan Sun, Xuyang Shen, Dong Li, Weigao Sun, and Yiran Zhong. Hgrn2:
Gated linear rnns with state expansion. arXiv preprint arXiv:2404.07904, 2024.
[72] Tao Huang, Xiaohuan Pei, Shan You, Fei Wang, Chen Qian, and Chang Xu. Localmamba: Visual state
space model with windowed selective scan. In European conference on computer vision, pages 12–22.
Springer, 2024.
[73] Xiaohuan Pei, Tao Huang, and Chang Xu. Efficientvmamba: Atrous selective scan for light weight
visual mamba. In Proceedings of the AAAI conference on artificial intelligence, volume 39, pages
6443–6451, 2025.
[74] AakashLahoti,KevinYLi,BerlinChen,CaitlinWang,AvivBick,JZicoKolter,TriDao,andAlbertGu.
Mamba-3: Improved sequence modeling using state space principles. arXiv preprint arXiv:2603.15569,
2026.
[75] AgiBot-World-Contributors, Qingwen Bu, Jisong Cai, Li Chen, Xi Cui, Yan Ding, Siyuan Feng,
Shenyuan Gao, Xindong He, Xu Huang, Shu Jiang, Yuxin Jiang, Cheng Jing, Hongyang Li, Jialun Li,
Chiming Liu, Yi Liu, Yuxiang Lu, Jianlan Luo, Ping Luo, Yao Mu, Yue Niu, Yixuan Pan, Jiangmiao
Pang, Yu Qiao, Guanghui Ren, Cheng-Xing Ruan, Jiaqi Shan, Yongjian Shen, Cheng Shi, Mi Shi, Modi
Shi, Chonghao Sima, Jia-Yi Song, Huijie Wang, Wenhao Wang, Dafeng Wei, Chengen Xie, Guofeng Xu,
Junchi Yan, Cunbiao Yang, Lei Yang, Shukai Yang, Maoqing Yao, Jiansheng Zeng, Chi Zhang, Qingli
Zhang, Bin Zhao, Chengyu Zhao, Jiaqi Zhao, and Jianchao Zhu. Agibot world colosseo: A large-scale
manipulation platform for scalable and intelligent embodied systems. 2025 IEEE/RSJ International
Conference on Intelligent Robots and Systems (IROS), pages 3549–3556, 2025.
[76] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karam-
cheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David
Fagan, Joey Hejna, Masha Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu,
Suneel Belkhale, Shivin Dass, Huy Ha, Arhan Jain, Abraham Lee, Youngwoon Lee, Marius Memmel,
Sungjae Park, Ilija Radosavovic, Kaiyuan Wang, Albert Zhan, Kevin Black, Cheng Chi, Kyle Beltran
Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R Sanketi, Archit Sharma, Cody
Simpson, Quan Vuong, Homer Rich Walke, Blake Wulfe, Ted Xiao, Jonathan Heewon Yang, Arefeh
Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu
Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, Vitor Guizilini, David Antonio
Herrera,MinhoHeo,KyleHsu,JiahengHu,MuhammadZubairIrshad,DonovonJackson,CharlotteLe,
YunshuangLi,KevinLin,RoyLin,ZehanMa,AbhiramMaddukuri,SuvirMirchandani,DanielMorton,
Tony Nguyen, Abigail O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran,
95

Andrew E. Wang, Yilin Wu, Annie Xie, Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani,
Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Abhishek Gupta, Dinesh Jayaraman,
Joseph J Lim, Jitendra Malik, Roberto Martín-Martín, Subramanian Ramamoorthy, Dorsa Sadigh,
Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn.
Droid: A large-scale in-the-wild robot manipulation dataset. In Robotics: Science and Systems (RSS),
2024.
[77] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching
for generative modeling. In International Conference on Learning Representations (ICLR), 2023.
[78] Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate and
transfer data with rectified flow. In International Conference on Learning Representations (ICLR),
2023.
[79] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas Müller, Harry Saini, Yam
Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, Dustin Podell, Tim Dockhorn, Zion English, Kyle
Lacey, Alex Goodwin, Yannik Marek, and Robin Rombach. Scaling rectified flow transformers for
high-resolution image synthesis. arXiv preprint arXiv:2403.03206, 2024.
[80] Weijie Kong, Qi Tian, Zijian Zhang, Rox Min, Zuozhuo Dai, Jin Zhou, Jiangfeng Xiong, Xin Li, Bo Wu,
Jianwei Zhang, et al. Hunyuanvideo: A systematic framework for large video generative models. arXiv
preprint arXiv:2412.03603, 2024.
[81] Xiangyu Peng, Zangwei Zheng, Chenhui Shen, Tom Young, Xinying Guo, Binluo Wang, Hang Xu,
Hongxin Liu, Mingyan Jiang, Wenjun Li, et al. Open-sora 2.0: Training a commercial-level video
generation model in $200k. arXiv preprint arXiv:2503.09642, 2025.
[82] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming
Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang, Jingfeng Zhang, Jingren Zhou, Jinkai Wang, Jixuan
Chen, Kai Zhu, Kang Zhao, Keyu Yan, Lianghua Huang, Mengyang Feng, Ningyi Zhang, Pandeng Li,
Pingyu Wu, Ruihang Chu, Ruili Feng, Shiwei Zhang, Siyang Sun, Tao Fang, Tianxing Wang, Tianyi
Gui, Tingyu Weng, Tong Shen, Wei Lin, Wei Wang, Wei Wang, Wenmeng Zhou, Wente Wang, Wenting
Shen, Wenyuan Yu, Xianzhong Shi, Xiaoming Huang, Xin Xu, Yan Kou, Yangyu Lv, Yifei Li, Yijing
Liu, Yiming Wang, Yingya Zhang, Yitong Huang, Yong Li, You Wu, Yu Liu, Yulin Pan, Yun Zheng,
Yuntao Hong, Yupeng Shi, Yutong Feng, Zeyinzi Jiang, Zhen Han, Zhi-Fan Wu, and Ziyu Liu. Wan:
Open and advanced large-scale video generative models. arXiv preprint arXiv:2503.20314, 2025.
[83] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization, 2019.
[84] Anke Tang, Li Shen, Yong Luo, Enneng Yang, Han Hu, Lefei Zhang, Bo Du, and Dacheng Tao.
Fusionbench: Acomprehensivebenchmarkofdeepmodelfusion. Journal of Machine Learning Research,
2025.
[85] Enneng Yang, Li Shen, Guibing Guo, Xingwei Wang, Xiaochun Cao, Jie Zhang, and Dacheng Tao.
Model merging in llms, mllms, and beyond: Methods, theories, applications, and opportunities. ACM
Comput. Surv., 58(8), February 2026.
[86] Mitchell Wortsman, Gabriel Ilharco, Samir Yitzhak Gadre, Rebecca Roelofs, Raphael Gontijo-Lopes,
Ari S. Morcos, Hongseok Namkoong, Ali Farhadi, Yair Carmon, Simon Kornblith, and Ludwig Schmidt.
Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing
inference time, 2022.
[87] JihoChoi, DonggyunKim, ChanhyukLee, andSeunghoonHong. Revisitingweightaveragingformodel
merging. arXiv preprint arXiv:2412.12153, 2024.
[88] Prateek Yadav, Derek Tam, Leshem Choshen, Colin Raffel, and Mohit Bansal. Ties-merging: Resolving
interference when merging models, 2023.
96

[89] Le Yu, Bowen Yu, Haiyang Yu, Fei Huang, and Yongbin Li. Language models are super mario:
Absorbing abilities from homologous models as a free lunch, 2024.
[90] Runxi Cheng, Feng Xiong, Yongxian Wei, Wanyun Zhu, and Chun Yuan. Whoever started the
interference should end it: Guiding data-free model merging via task vectors, 2025.
[91] Bram Wallace, Meihua Dang, Rafael Rafailov, Linqi Zhou, Aaron Lou, Senthil Purushwalkam, Stefano
Ermon, CaimingXiong, ShafiqJoty, andNikhilNaik. Diffusionmodelalignmentusingdirectpreference
optimization, 2023.
[92] Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea
Finn. Direct preference optimization: Your language model is secretly a reward model, 2024.
[93] RuntaoLiu,HaoyuWu,ZiqiangZheng,ChenWei,YingqingHe,RenjiePi,andQifengChen. Videodpo:
Omni-preference alignment for video diffusion generation. In Proceedings of the Computer Vision and
Pattern Recognition Conference, pages 8009–8019, 2025.
[94] Sam Ade Jacobs, Masahiro Tanaka, Chengming Zhang, Minjia Zhang, Shuaiwen Leon Song, Samyam
Rajbhandari, and Yuxiong He. Deepspeed ulysses: System optimizations for enabling training of
extreme long sequence transformer models, 2023.
[95] HaoLiu,MateiZaharia,andPieterAbbeel. Ringattentionwithblockwisetransformersfornear-infinite
context, 2023.
[96] Qiuheng Wang, Yukai Shi, Jiarong Ou, Rui Chen, Ke Lin, Jiahao Wang, Boyuan Jiang, Haotian Yang,
Mingwu Zheng, Xin Tao, Fei Yang, Pengfei Wan, and Di Zhang. Koala-36m: A large-scale video
dataset improving consistency between fine-grained conditions and video content. In Proceedings of the
IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2025.
[97] Hui Li, Mingwang Xu, Yun Zhan, Shan Mu, Jiaye Li, Kaihui Cheng, Yuxuan Chen, Tan Chen, Mao
Ye, Jingdong Wang, and Siyu Zhu. Openhumanvid: A large-scale high-quality dataset for enhancing
human-centric video generation. In Proceedings of the IEEE/CVF Conference on Computer Vision and
Pattern Recognition (CVPR), pages 9365–9374, 2025.
[98] Zhiyu Tan, Xiaomeng Yang, Luozheng Qin, and Hao Li. Vidgen-1m: A large-scale dataset for
text-to-video generation. arXiv preprint arXiv:2408.02629, 2024.
[99] Zachary Teed and Jia Deng. Raft: Recurrent all-pairs field transforms for optical flow. In European
Conference on Computer Vision (ECCV), pages 402–419. Springer, 2020.
[100] FalconsAI Team. Fine-tuned vision transformer for nsfw image classification. Hugging Face Model Hub,
2023. Initial commit 2023-10-14, Last updated 2025-04-06, Apache-2.0 License, 80k training images,
98.04% accuracy, 85.8M params.
[101] Zheng Ge, Songtao Liu, Feng Wang, Zeming Li, and Jian Sun. Yolox: Exceeding yolo series in 2021.
arXiv preprint arXiv:2107.08430, 2021.
[102] YifuZhang,PeizeSun,YiJiang,DongdongYu,ZehuanYuan,PingLuo,WenyuLiu,andXinggangWang.
Bytetrack: Multi-object tracking by associating every detection box. arXiv preprint arXiv:2110.06864,
2021.
[103] Minghui Liao, Zhaoyi Wan, Cong Yao, Kai Chen, and Xiang Bai. Real-time scene text detection with
differentiable binarization. arXiv preprint arXiv:1911.08947, 2019.
[104] Qwen Team. Qwen3 technical report, 2025.
[105] WeiyunWang, ZhangweiGao, LixinGu, HengjunPu, LongCui, XingguangWei, ZhaoyangLiu, Linglin
Jing,ShenglongYe,JieShao,etal. Internvl3.5: Advancingopen-sourcemultimodalmodelsinversatility,
reasoning, and efficiency. arXiv preprint arXiv:2508.18265, 2025.
97

[106] XiaomiLLM-CoreTeam. Mimo: Unlockingthereasoningpotentialoflanguagemodel–frompretraining
| to posttraining, | 2025. |     |     |     |
| ---------------- | ----- | --- | --- | --- |
[107] Tianyu Yu, Zefan Wang, Chongyi Wang, Fuwei Huang, Wenshuo Ma, Zhihui He, Tianchi Cai, Weize
Chen, Yuxiang Huang, Yuanqian Zhao, et al. Minicpm-v 4.5: Cooking efficient mllms via architecture,
| data, and training | recipe. | arXiv preprint arXiv:2509.18154, |     | 2025. |
| ------------------ | ------- | -------------------------------- | --- | ----- |
[108] Team Seedance, De Chen, Liyang Chen, Xin Chen, Ying Chen, Zhuo Chen, Zhuowei Chen, Feng Cheng,
Tianheng Cheng, Yufeng Cheng, et al. Seedance 2.0: Advancing video generation for world complexity.
| arXiv preprint | arXiv:2604.14148, | apr 2026. |     |     |
| -------------- | ----------------- | --------- | --- | --- |
[109] Tianwei Yin, Michaël Gharbi, Richard Zhang, Eli Shechtman, Fredo Durand, William T. Freeman, and
Taesung Park. One-step diffusion with distribution matching distillation, 2024.
[110] Tianwei Yin, Michaël Gharbi, Taesung Park, Richard Zhang, Eli Shechtman, Fredo Durand, and
William T. Freeman. Improved distribution matching distillation for fast image synthesis, 2024.
[111] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models, 2023.
[112] Cheng Lu and Yang Song. Simplifying, stabilizing and scaling continuous-time consistency models,
2025.
[113] Kaiwen Zheng, Yuji Wang, Qianli Ma, Huayu Chen, Jintao Zhang, Yogesh Balaji, Jianfei Chen,
Ming-Yu Liu, Jun Zhu, and Qinsheng Zhang. Large scale diffusion distillation via score-regularized
| continuous-time | consistency, | 2026. |     |     |
| --------------- | ------------ | ----- | --- | --- |
[114] Fengzhe Zhou, Jiannan Huang, Jialuo Li, Deva Ramanan, and Humphrey Shi. Pai-bench: A compre-
| hensive benchmark | for physical | ai. arXiv preprint | arXiv:2512.01989, | 2025. |
| ----------------- | ------------ | ------------------ | ----------------- | ----- |
[115] Yuzhi Chen, Ronghan Chen, Dongjie Huo, Yandan Yang, Dekang Qi, Haoyun Liu, Tong Lin, Shuang
Zeng, Junjin Xiao, Xinyuan Chang, et al. Abot-physworld: Interactive world foundation model for
robotic manipulation with physics alignment. arXiv preprint arXiv:2603.23376, 2026.
[116] GigaWorld Team, Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Haoyun Li,
JiagangZhu,KeruiLi,MengyuanXu,QiupingDeng,SitingWang,WenkangQin,XinzeChen,Xiaofeng
Wang, Yankai Wang, Yu Cao, Yifan Chang, Yuan Xu, Yun Ye, Yang Wang, Yukun Zhou, Zhengyuan
Zhang, ZhehaoDong, andZhengZhu. Gigaworld-0: Worldmodelsasdataenginetoempowerembodied
ai, 2025.
[117] Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing
Wu, Qingyang Jin, Nattapol Chanpaisit, et al. Vbench: Comprehensive benchmark suite for video
generative models. In 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition
| (CVPR), pages | 21807–21818. | IEEE, 2024. |     |     |
| ------------- | ------------ | ----------- | --- | --- |
[118] Alibaba Tongyi Lab. Wan 2.5: Open-source ai video generation with audio. https://wan.video, 2025.
| Official product | page. |     |     |     |
| ---------------- | ----- | --- | --- | --- |
[119] Google DeepMind. Veo 3.1. https://deepmind.google/models/veo/, 2025. Official model page.
[120] Xiaowei Chi, Peidong Jia, Chun-Kai Fan, Xiaozhu Ju, Weishi Mi, Kevin Zhang, Zhiyuan Qin, Wanxin
Tian, Kuangzhi Ge, Hao Li, Zezhong Qian, Anthony Chen, Qiang Zhou, Yueru Jia, Jiaming Liu,
Yong Dai, Qingpo Wuwu, Chengyu Bai, Yu-Kai Wang, Ying Li, Lizhang Chen, Yong Bao, Zhiyuan
Jiang, Jiacheng Zhu, Kai Tang, Ruichuan An, Yulin Luo, Qiuxuan Feng, Siyuan Zhou, Chi min Chan,
Chengkai Hou, Wei Xue, Sirui Han, Yike Guo, Shanghang Zhang, and Jian Tang. Wow: Towards a
| world omniscient | world model | through embodied | interaction, | 2025. |
| ---------------- | ----------- | ---------------- | ------------ | ----- |
[121] OpenAI. Sora2pro. https://platform.openai.com/docs/models/sora-2-pro,2025. Officialmodel
| documentation, | accessed | 2026-06-08. |     |     |
| -------------- | -------- | ----------- | --- | --- |
98

[122] Unitree Robotics. Unifolm-wma-0: A world-model-action (wma) framework under the unifolm family.
https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Base, 2025. Hugging Face model card,
accessed June 2026.
[123] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie
Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei
Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang,
Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025.
[124] Qwen Team. Qwen3.5-2B. https://huggingface.co/Qwen/Qwen3.5-2B, 2025. Model card and
benchmark results. Accessed: 2026-06-10.
[125] Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu
Jiang,WeimingRen,YuxuanSun,CongWei,BotaoYu,RuibinYuan,RenliangSun,MingYin,Boyuan
Zheng, Zhenzhu Yang, Yibo Liu, Wenhao Huang, Huan Sun, Yu Su, and Wenhu Chen. Mmmu: A
massive multi-discipline multimodal understanding and reasoning benchmark for expert agi, 2024.
[126] Xiang Yue, Tianyu Zheng, Yuansheng Ni, Yubo Wang, Kai Zhang, Shengbang Tong, Yuxuan Sun,
Botao Yu, Ge Zhang, Huan Sun, Yu Su, Wenhu Chen, and Graham Neubig. Mmmu-pro: A more
robust multi-discipline multimodal understanding benchmark, 2025.
[127] PanLu,HritikBansal,TonyXia,JiachengLiu,ChunyuanLi,HannanehHajishirzi,HaoCheng,Kai-Wei
Chang, Michel Galley, and Jianfeng Gao. Mathvista: Evaluating mathematical reasoning of foundation
models in visual contexts, 2024.
[128] xAI. Grok-1.5 Vision Preview. https://x.ai/blog/grok-1.5v, 2024. Accessed: 2026-06-10.
[129] Lin Chen, Jinsong Li, Xiaoyi Dong, Pan Zhang, Yuhang Zang, Zehui Chen, Haodong Duan, Jiaqi Wang,
Yu Qiao, Dahua Lin, and Feng Zhao. Are we on the right way for evaluating large vision-language
models?, 2024.
[130] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai,
Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey
Levine, AdrianLi-Bell, MohithMothukuri, SurajNair, KarlPertsch, LucyXiaoyangShi, JamesTanner,
Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. π : A vision-language-action flow
0
model for general robot control, 2026.
[131] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng,
Jiayin Zou, Yilun Chen, Jia Zeng, Ya-Qin Zhang, Jiangmiao Pang, Jingjing Liu, Tai Wang, and
Xianyuan Zhan. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action
model, 2025.
[132] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess,
Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy
Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc,
SergeyLevine,AdrianLi-Bell,MohithMothukuri,SurajNair,KarlPertsch,AllenZ.Ren,LucyXiaoyang
Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer
Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. π : a vision-language-action model
0.5
with open-world generalization, 2025.
[133] StarVLA Community. Starvla: A lego-like codebase for vision-language-action model developing. arXiv
preprint arXiv:2604.05014, 2026.
[134] Yandan Yang, Shuang Zeng, Tong Lin, Xinyuan Chang, Dekang Qi, Junjin Xiao, Haoyun Liu, Ronghan
Chen, Yuzhi Chen, Dongjie Huo, et al. Abot-m0: Vla foundation model for robotic manipulation with
action manifold learning. arXiv preprint arXiv:2602.11236, 2026.
[135] Wei Wu, Fan Lu, Yunnan Wang, Shuai Yang, Shi Liu, Fangjing Wang, Shuailei Ma, He Sun, Yong
Wang, Zhenqi Qiu, Houlong Xiong, Ziyu Wang, Shuai Zhou, Yiyu Ren, Kejia Zhang, Hui Yu, Jingmei
99

Zhao, Qian Zhu, Ran Cheng, Yong-Lu Li, Yongtao Huang, Xing Zhu, Yujun Shen, and Kecheng Zheng.
A pragmatic vla foundation model. arXiv preprint arXiv:2601.18692v1, 2026.
[136] Galaxea Team. Galaxea g0.5 technical report. 2026.
[137] Shangchen Miao, Ningya Feng, Jialong Wu, Ye Lin, Xu He, Dong Li, and Mingsheng Long. Jepa-vla:
Video predictive embedding is needed for vla models, 2026.
[138] Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Hao Li, Hengtao Li, Jie Li,
Jindi Lv, Jingyu Liu, et al. Gigaworld-policy: An efficient action-centered world–action model. arXiv
preprint arXiv:2603.17240, 2026.
[139] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao
Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and
Jun Zhu. Motus: A unified latent action world model, 2025.
[140] Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan
Xue, Xing Zhu, Yujun Shen, and Yinghao Xu. Causal world modeling for robot control. arXiv preprint
arXiv:2601.21998, 2026.
[141] Hao Luo, Wanpeng Zhang, Yicheng Feng, Sipeng Zheng, Haiweng Xu, Chaoyi Xu, Ziheng Xi, Yuhui
Fu, and Zongqing Lu. Being-h0. 7: A latent world-action model from egocentric videos. arXiv preprint
arXiv:2605.00078, 2026.
[142] Liaoyuan Fan, Zetian Xu, Chen Cao, Wenyao Zhang, Mingqi Yuan, and Jiayu Chen. Aim: Intent-aware
unified world action modeling with spatial value maps, 2026.
[143] Yirui Sun, Guangyu Zhuge, Keliang Liu, Jie Gu, Xinyu Bing, Zhongxue Gan, and Chunxu Tian. Sants:
A state-adaptive scheduler for world action models, 2026.
[144] MotuBrain Team, Chendong Xiang, Fan Bao, Haitian Liu, Hengkai Tan, Hongzhe Bi, James Li, Jiabao
Liu, Jingrui Pang, Kiro Jing, Louis Liu, Mengchen Cai, Rongxu Cui, Ruowen Zhao, Runqing Wang,
Shuhe Huang, Yao Feng, Yinze Rong, Zeyuan Wang, and Jun Zhu. Motubrain: An advanced world
action model for robot control, 2026.
[145] Linqing Zhong, Yi Liu, Yifei Wei, Ziyu Xiong, Maoqing Yao, Si Liu, and Guanghui Ren. Acot-vla:
Action chain-of-thought for vision-language-action models, 2026.
[146] Hao Luo, Ye Wang, Wanpeng Zhang, Sipeng Zheng, Ziheng Xi, Chaoyi Xu, Haiweng Xu, Haoqi Yuan,
Chi Zhang, Yiqing Wang, Yicheng Feng, and Zongqing Lu. Being-h0.5: Scaling human-centric robot
learning for cross-embodiment generalization. arXiv preprint arXiv:2601.12993, 2026.
[147] Renming Huang, Chendong Zeng, Wenjing Tang, Jintian Cai, Cewu Lu, and Panpan Cai. Mimic intent,
not just trajectories, 2026.
[148] Xiao-Ming Wu, Bin Fan, Kang Liao, Jian-Jian Jiang, Runze Yang, Yihang Luo, Zhonghua Wu, Wei-Shi
Zheng, and Chen Change Loy. Vlanext: Recipes for building strong vla models, 2026.
[149] Nastaran Darabi and Amit Ranjan Trivedi. Progal-vla: Grounded alignment through prospective
reasoning in vision-language-action models, 2026.
[150] Jingzhou Luo, Yifan Wen, Yongjie Bai, Xinshuai Song, Yang Liu, and Liang Lin. Rovla: Multi-
consistency constraints for robust vision-language-action models, 2026.
[151] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing
speed and success, 2025.
[152] NVIDIA,:,JohanBjorck,FernandoCastañeda,NikitaCherniadev,XingyeDa,RunyuDing,Linxi"Jim"
Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil
Kundalia, LawrenceLao, ZhiqiLi, ZongyuLin, KevinLin, GuilinLiu, EdithLlontop, LoicMagne, Ajay
Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang,
100

Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu,
Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation
| model for | generalist | humanoid |     | robots, | 2025. |     |     |     |
| --------- | ---------- | -------- | --- | ------- | ----- | --- | --- | --- |
[153] Yandan Yang, Shuang Zeng, Tong Lin, Xinyuan Chang, Dekang Qi, Junjin Xiao, Haoyun Liu, Ronghan
Chen, Yuzhi Chen, Dongjie Huo, Feng Xiong, Xing Wei, Zhiheng Ma, and Mu Xu. Abot-m0: Vla
foundation model for robotic manipulation with action manifold learning, 2026.
[154] Hritik Bansal, Zongyu Lin, Tianyi Xie, Zeshun Zong, Michal Yarom, Yonatan Bitton, Chenfanfu Jiang,
Yizhou Sun, Kai-Wei Chang, and Aditya Grover. Videophy: Evaluating physical commonsense for
| video generation. |     | arXiv | preprint | arXiv:2406.03520, |     |     | 2024. |     |
| ----------------- | --- | ----- | -------- | ----------------- | --- | --- | ----- | --- |
[155] Jay Zhangjie Wu, Yixiao Ge, Xintao Wang, Stan Weixian Lei, Yuchao Gu, Yufei Shi, Wynne Hsu, Ying
Shan, Xiaohu Qie, and Mike Zheng Shou. Tune-a-video: One-shot tuning of image diffusion models for
text-to-video generation. In Proceedings of the IEEE/CVF international conference on computer vision,
| pages 7623–7633, |     | 2023. |     |     |     |     |     |     |
| ---------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
[156] Haoyu Wu, Diankun Wu, Tianyu He, Junliang Guo, Yang Ye, Yueqi Duan, and Jiang Bian. Geometry
forcing: Marryingvideodiffusionand3drepresentationforconsistentworldmodeling. InTheFourteenth
| International |     | Conference | on  | Learning | Representations, |     | 2026. |     |
| ------------- | --- | ---------- | --- | -------- | ---------------- | --- | ----- | --- |
[157] Wilson Yan, Yunzhi Zhang, Pieter Abbeel, and Aravind Srinivas. Videogpt: Video generation using
| vq-vae | and transformers. |     | arXiv | preprint | arXiv:2104.10157, |     | 2021. |     |
| ------ | ----------------- | --- | ----- | -------- | ----------------- | --- | ----- | --- |
[158] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. Advances in neural
| information | processing |     | systems, | 30, | 2017. |     |     |     |
| ----------- | ---------- | --- | -------- | --- | ----- | --- | --- | --- |
[159] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. Improving language under-
| standing | by generative |     | pre-training. |     | 2018. |     |     |     |
| -------- | ------------- | --- | ------------- | --- | ----- | --- | --- | --- |
[160] Songwei Ge, Thomas Hayes, Harry Yang, Xi Yin, Guan Pang, David Jacobs, Jia-Bin Huang, and Devi
Parikh. Long video generation with time-agnostic vqgan and time-sensitive transformer. In European
| Conference | on  | Computer | Vision, | pages | 102–118. | Springer, | 2022. |     |
| ---------- | --- | -------- | ------- | ----- | -------- | --------- | ----- | --- |
[161] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton,
and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. arXiv preprint
| arXiv:2309.17080, |     | 2023. |     |     |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
[162] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans,
and Pieter Abbeel. Learning universal policies via text-guided video generation. Advances in neural
| information | processing |     | systems, | 36:9156–9172, |     | 2023. |     |     |
| ----------- | ---------- | --- | -------- | ------------- | --- | ----- | --- | --- |
[163] Mengda Xu, Zhenjia Xu, Yinghao Xu, Cheng Chi, Gordon Wetzstein, Manuela Veloso, and Shuran
Song. Flow as the cross-domain manipulation interface. arXiv preprint arXiv:2407.15208, 2024.
[164] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil
Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with
| predictive | visual | representations. |     |     | arXiv preprint | arXiv:2412.14803, |     | 2024. |
| ---------- | ------ | ---------------- | --- | --- | -------------- | ----------------- | --- | ----- |
[165] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Se June Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar,
ReubenTan,Yu-WeiChao,BillYuchenLin,etal.Latentactionpretrainingfromvideos.InInternational
Conference on Learning Representations, volume 2025, pages 28213–28239, 2025.
[166] Yunfan Lou, Xiaowei Chi, Xiaojie Zhang, Zezhong Qian, Chengxuan Li, Rongyu Zhang, Yaoxu Lyu,
Guoyu Song, Chuyao Fu, Haoxuan Xu, et al. Mask world model: Predicting what matters for robust
| robot policy | learning. |     | arXiv | preprint | arXiv:2604.19683, |     | 2026. |     |
| ------------ | --------- | --- | ----- | -------- | ----------------- | --- | ----- | --- |
[167] Shuaiyi Huang, Mara Levy, Zhenyu Jiang, Anima Anandkumar, Yuke Zhu, Linxi Fan, De-An Huang,
andAbhinavShrivastava. Ardup: Activeregionvideodiffusionforuniversalpolicies. In2024IEEE/RSJ
International Conference on Intelligent Robots and Systems (IROS), pages 8465–8472. IEEE, 2024.
101

[168] HongtaoWu,YaJing,ChilamCheang,GuangzengChen,JiafengXu,XinghangLi,MinghuanLiu,Hang
Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation.
In International Conference on Learning Representations, volume 2024, pages 10641–10662, 2024.
[169] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli
Ma,SongHan,ChelseaFinn,etal. Cot-vla: Visualchain-of-thoughtreasoningforvision-language-action
models. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 1702–1713,
2025.
[170] Yanjiang Guo, Yucheng Hu, Jianke Zhang, Yen-Jen Wang, Xiaoyu Chen, Chaochao Lu, and Jianyu
Chen. Prediction with action: Visual policy learning via joint denoising process. Advances in Neural
| Information | Processing |     | Systems, | 37:112386–112410, |     | 2024. |     |     |
| ----------- | ---------- | --- | -------- | ----------------- | --- | ----- | --- | --- |
[171] John Won, Kyungmin Lee, Huiwon Jang, Dongyoung Kim, and Jinwoo Shin. Dual-stream diffusion for
world-model augmented vision-language-action model. arXiv preprint arXiv:2510.27607, 2025.
[172] Liudi Yang, Yang Bai, George Eskandar, Fengyi Shen, Mohammad Altillawi, Dong Chen, Ziyuan
Liu, and Abhinav Valada. Covar: Co-generation of video and action for robotic manipulation via
| multi-modal | diffusion. |     | arXiv | preprint arXiv:2512.16023, |     |     | 2025. |     |
| ----------- | ---------- | --- | ----- | -------------------------- | --- | --- | ----- | --- |
[173] Jiayi Chen, Wenxuan Song, Pengxiang Ding, Ziyang Zhou, Han Zhao, Feilong Tang, Donglin Wang,
andHaoangLi. Unifieddiffusionvla: Vision-language-actionmodelviajointdiscretedenoisingdiffusion
| process. | arXiv | preprint | arXiv:2511.01718, |     | 2025. |     |     |     |
| -------- | ----- | -------- | ----------------- | --- | ----- | --- | --- | --- |
[174] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta.
Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets.
| arXiv preprint | arXiv:2504.02792, |     |     | 2025. |     |     |     |     |
| -------------- | ----------------- | --- | --- | ----- | --- | --- | --- | --- |
[175] Jiangran Lyu, Kai Liu, Xuheng Zhang, Haoran Liao, Yusen Feng, Wenxuan Zhu, Tingrui Shen, Jiayi
Chen, Jiazhao Zhang, Yifei Dong, et al. Lda-1b: Scaling latent dynamics action model via universal
| embodied | data | ingestion. | arXiv | preprint | arXiv:2602.12215, |     |     | 2026. |
| -------- | ---- | ---------- | ----- | -------- | ----------------- | --- | --- | ----- |
[176] Jun Guo, Qiwei Li, Peiyan Li, Zilong Chen, Nan Sun, Yifei Su, Heyun Wang, Yuan Zhang, Xinghang
Li, and Huaping Liu. Unified 4d world action modeling from video priors with asynchronous denoising.
| arXiv preprint | arXiv:2604.26694, |     |     | 2026. |     |     |     |     |
| -------------- | ----------------- | --- | --- | ----- | --- | --- | --- | --- |
[177] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. arXiv preprint
| arXiv:2503.00200, |     | 2025. |     |     |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
[178] Haoyu Wu, Jiwen Yu, Yingtian Zou, and Xihui Liu. Multiworld: Scalable multi-agent multi-view video
| world models. | arXiv | preprint |     | arXiv:2604.18564, |     | 2026. |     |     |
| ------------- | ----- | -------- | --- | ----------------- | --- | ----- | --- | --- |
[179] Runze Li, Hongyin Zhang, Junxi Jin, Qixin Zeng, Zifeng Zhuang, Yiqi Tang, Shangke Lyu, and Donglin
Wang. World-value-action model: Implicit planning for vision-language-action systems. arXiv preprint
| arXiv:2604.14732, |     | 2026. |     |     |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
[180] Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need
| test-time | future | imagination? |     | arXiv preprint |     | arXiv:2603.16666, |     | 2026. |
| --------- | ------ | ------------ | --- | -------------- | --- | ----------------- | --- | ----- |
[181] Han Zhao, Jingbo Wang, Wenxuan Song, Shuai Chen, Yang Liu, Yan Wang, Haoang Li, and Donglin
Wang. Frappe: Infusing world modeling into generalist policies via multiple future representation
| alignment. | arXiv | preprint | arXiv:2602.17259, |     |     | 2026. |     |     |
| ---------- | ----- | -------- | ----------------- | --- | --- | ----- | --- | --- |
[182] Haodong Yan, Zhide Zhong, Jiaguan Zhu, Junjie He, Weilin Yuan, Wenxuan Song, Xin Gong, Yingjie
Cai, Guanyi Zhao, Xu Yan, et al. S-vam: Shortcut video-action model by self-distilling geometric and
| semantic | foresight. | arXiv | preprint | arXiv:2603.16195, |     |     | 2026. |     |
| -------- | ---------- | ----- | -------- | ----------------- | --- | --- | ----- | --- |
[183] Angelos Katharopoulos, Apoorv Vyas, Nikolaos Pappas, and François Fleuret. Transformers are rnns:
Fast autoregressive transformers with linear attention. In International conference on machine learning,
| pages 5156–5165. |     | PMLR, | 2020. |     |     |     |     |     |
| ---------------- | --- | ----- | ----- | --- | --- | --- | --- | --- |
102

[184] Krzysztof Choromanski, Valerii Likhosherstov, David Dohan, Xingyou Song, Andreea Gane, Tamas
Sarlos, Peter Hawkins, Jared Davis, Afroz Mohiuddin, Lukasz Kaiser, et al. Rethinking attention with
| performers. | arXiv preprint | arXiv:2009.14794, | 2020. |
| ----------- | -------------- | ----------------- | ----- |
[185] Yutao Sun, Li Dong, Shaohan Huang, Shuming Ma, Yuqing Xia, Jilong Xue, Jianyong Wang, and
Furu Wei. Retentive network: A successor to transformer for large language models. arXiv preprint
| arXiv:2307.08621, | 2023. |     |     |
| ----------------- | ----- | --- | --- |
[186] Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces. In First
| conference | on language | modeling, 2024. |     |
| ---------- | ----------- | --------------- | --- |
[187] Aonian Li, Bangwei Gong, Bo Yang, Boji Shan, Chang Liu, Cheng Zhu, Chunhao Zhang, Congchao
Guo, Da Chen, Dong Li, et al. Minimax-01: Scaling foundation models with lightning attention. arXiv
| preprint | arXiv:2501.08313, | 2025. |     |
| -------- | ----------------- | ----- | --- |
103

Appendix
A Contributors
| Kairos | is contributed | to by the following | people. |
| ------ | -------------- | ------------------- | ------- |
Advisor:
| Dacheng | Tao, Xiaogang | Wang |     |
| ------- | ------------- | ---- | --- |
Lead:
Project
| Fei Wang, | Shan You, | Qiming Zhang |     |
| --------- | --------- | ------------ | --- |
Core Contributor:
| Tao Huang, | Zuoyi | Fu  |     |
| ---------- | ----- | --- | --- |
Contributor:
Zhisheng Zheng, Yunlong Xi, Feng Lv, Xiaoming Wu, Zeyu Liu, Cong Wan, Pu Li, Ruiqing Yang,
Xiaoou Li, Wei Wang, Kangkang Zhu, Yuwei Zhang, Shi Fu, Zheng Zhang, Xiaoning Wu, Xuzeng
Fan
Acknowledgement:
We would like to thank Anke Tang, Changhui Du, Huiwen Xue, Jiakai Huang, Junxi Jia, Lichen Man,
Menglin Geng, Ruixuan Zhang, Shuaiqi Cheng, Shuo Huang, Weijie Sun, Yu Li, Yunpeng Wang,
Zhongbo Wu, Zihao Gao for their valuable support and contributions to this project, including data
preparation, model evaluation, infrastructure support, architecture analysis, and helpful discussions.
104

B Theoretical Analysis
The proposed world model is grounded in a unified understanding-generation-prediction substrate
and a hybrid temporal backbone. To formally analyze its long-horizon consistency, this section
investigates future targets requiring extended world-state information, such as object permanence,
delayed physical effects, and multi-stage task variables. We address two central questions: when
is a bounded recent window fundamentally insufficient, and under what conditions can a hybrid
multi-scale memory recover near-Bayes-optimal prediction?
Our theoretical contribution is twofold. First, we establish an information-theoretic necessity result:
whenever the Bayes-optimal predictor of a long-horizon target relies on history outside a finite recent
window, any window-restricted predictor incurs a strictly positive, irreducible excess risk. This
proves the fundamental necessity of a persistent internal state. Second, we establish the approximate
sufficiency of a hybrid multi-scale temporal memory. We prove that if the Bayes predictor factorizes
into a shared predictive state alongside short-range, mid-range, and contractive global-memory
branches, the resulting predictor yields an explicit excess-risk bound controlled by branch-wise
approximation errors and a geometrically discounted global-memory perturbation term.
This formal analysis perfectly mirrors the model’s architectural design. The necessity result explains
the inevitable degradation of purely local temporal mechanisms in tasks involving delayed effects
or multi-stage structures. Conversely, the sufficiency result mathematically validates the proposed
hybrid design: short- and mid-range pathways efficiently capture localized and intermediate motion,
while the persistent global memory propagates supra-window context with controlled drift. Together,
these theorems provide a rigorous mathematical justification for the architectural logic underlying
the model’s long-horizon capabilities.
B.1 Problem Setup and Theoretical Scope
Standing probabilistic setup. Let (Ω,F,P) be a probability space. We model the available
interaction stream as a discrete-time partially observed controlled process
{(O ,A )} ,
t t t≥1
where
O ∈ O, A ∈ A.
t t
Here, O denotes the observable input available to the model, and A denotes the control or action
t t
signal that can influence future evolution. Fix a time index t ≥ 1, a prediction horizon τ ≥ 1, and a
window length 1 ≤ w < t. Let Y (τ) ∈ L2(Ω,F,P) be any square-integrable future target, and write
t
(τ)
Y := Y .
t
Throughout, Y may represent a future latent-frame coordinate, an object-permanence indicator, a
delayed physical-effect event, a task-progress variable, or any other long-horizon functional of the
future world state. All scalar statements below extend coordinatewise to vector-valued targets. For
any square-integrable scalar-, vector-, or matrix-valued random variable Z, define
∥Z∥ :=
(cid:0)E[∥Z∥2] (cid:1)1/2
,
L2
where ∥·∥ denotes the absolute value, the Euclidean norm, or the Frobenius norm according to
context.
105

|            |     | (History | and | recent | window). |     |              |     |         |            |                 |     |
| ---------- | --- | -------- | --- | ------ | -------- | --- | ------------ | --- | ------- | ---------- | --------------- | --- |
| Definition |     | 1        |     |        |          |     | The complete |     | history | up to time | t is defined as |     |
(48)
|     |     |     |     | H   | :=  | (O ,...,O | ,   | A ,...,A | ),  |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | -------- | --- | --- | --- | --- |
|     |     |     |     |     | t   | 1         | t   | 1        | t−1 |     |     |     |
generating the associated σ-field H t := σ(H t ). For a window length 1 ≤ w < t, the recent w-step
| window | is given | by  |     |       |         |       |        |       |        |         |     |      |
| ------ | -------- | --- | --- | ----- | ------- | ----- | ------ | ----- | ------ | ------- | --- | ---- |
|        |          |     |     |       | (cid:0) |       |        |       |        | (cid:1) |     |      |
|        |          |     |     | W (w) | := O    |       | ,...,O | , A   | ,...,A | ,       |     | (49) |
|        |          |     |     | t     |         | t−w+1 |        | t t−w |        | t−1     |     |      |
|        |          |     |     |       |         |       | (w)    |       | (w)    |         |     |      |
with its corresponding σ-field denoted by W := σ(W ). Here, σ(·) denotes the sigma-field
|     |     |     |     |     |     |     | t   | t   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
generated by the enclosed random variables, i.e., the collection of all events or information measurable
from the corresponding observation–action history. By construction, it naturally follows that
|     |     |     |     |     |     | W   | (w) ⊆ | H . |     |     |     | (50) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | ---- |
t
t
|            |     | (Predictors |       | and optimal |         | risks).   |     |                 |              |               |     |     |
| ---------- | --- | ----------- | ----- | ----------- | ------- | --------- | --- | --------------- | ------------ | ------------- | --- | --- |
| Definition |     | 2           |       |             |         |           | For | any sub-σ-field |              | G ⊆ F, define |     |     |
|            |     |             | L2(G) |             | (cid:8) | L2(Ω,F,P) |     |                 |              | (cid:9)       |     |     |
|            |     |             |       | :=          | Z ∈     |           |     | : Z is          | G-measurable | .             |     |     |
L2(Ω,F,P),
| For any | Z ∈ |     |     | define the | squared |     | prediction | risk   |     |     |     |      |
| ------- | --- | --- | --- | ---------- | ------- | --- | ---------- | ------ | --- | --- | --- | ---- |
|         |     |     |     |            | R       | (Z) | := E[(Y    | −Z)2]. |     |     |     | (51) |
t
| The optimal |     | full-history | risk | is  |     |      |     |        |     |     |     |      |
| ----------- | --- | ------------ | ---- | --- | --- | ---- | --- | ------ | --- | --- | --- | ---- |
|             |     |              |      |     | R⋆  | :=   | inf | R (Z), |     |     |     | (52) |
|             |     |              |      |     |     | full |     | t      |     |     |     |      |
Z∈L2(Ht)
| and the | optimal | recent-window |     | risk | is  |     |     |     |      |     |     |      |
| ------- | ------- | ------------- | --- | ---- | --- | --- | --- | --- | ---- | --- | --- | ---- |
|         |         |               |     |      | R⋆  | :=  | inf | R   | (Z). |     |     | (53) |
|         |         |               |     |      |     | w   |     | t   |      |     |     |      |
Z∈L2(W(w))
t
|     |     | (Persistent |     | internal | state). |     |     |     |     |     | Rd  |     |
| --- | --- | ----------- | --- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
Definition 3 A recursively updated internal state M t ∈ is called a
persistent internal state if there exist measurable update maps Φ such that
t
|     |     |     | M   | = Φ (M |     | ,ζ ), | ζ := | (O ,A | ),  | t ≥ 2, |     | (54) |
| --- | --- | --- | --- | ------ | --- | ----- | ---- | ----- | --- | ------ | --- | ---- |
|     |     |     |     | t t    | t−1 | t     | t    | t     | t−1 |        |     |      |
with M given. Thus the model compresses historical information into a state that is propagated
1
through time, rather than recomputing prediction from scratch from a bounded local context at every
step.
|     |     | (Exactsufficientstate). |     |     |     |     |     |     | S⋆  | Rd  |     |     |
| --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Definition 4 A recursively updated state ∈ is called an exact sufficient
t
| state for | the   | target Y     | if: |      |        |      |     |     |     |     |     |     |
| --------- | ----- | ------------ | --- | ---- | ------ | ---- | --- | --- | --- | --- | --- | --- |
| 1. S⋆     | is H  | -measurable; |     |      |        |      |     |     |     |     |     |     |
|           | t     | t            |     |      |        |      |     |     |     |     |     |     |
| 2. there  | exist | measurable   |     | maps | T such | that |     |     |     |     |     |     |
t
|          |        |              |     | S⋆ =    | T (S⋆ | ,ζ ), | ζ       | := (O     | ,A ), | t ≥ 2; |     | (55) |
| -------- | ------ | ------------ | --- | ------- | ----- | ----- | ------- | --------- | ----- | ------ | --- | ---- |
|          |        |              |     | t       | t t−1 | t     |         | t         | t t−1 |        |     |      |
|          |        |              |     |         |       | Rd    | R       |           |       |        |     |      |
| 3. there | exists | a measurable |     | decoder |       | g t : | →       | such that |       |        |     |      |
|          |        |              |     |         |       | E[Y   |         | (S⋆)      |       |        |     | (56) |
|          |        |              |     |         |       | |     | H t ] = | g t       | a.s.  |        |     |      |
t
106

In other words, S⋆ retains exactly the historical information that is relevant for predicting Y.
t
|     |     | (Scope | of  | the two results). |     |     |     |     |     |     |
| --- | --- | ------ | --- | ----------------- | --- | --- | --- | --- | --- | --- |
Remark 3 The subsequent necessity theorem relies solely on the
filtration generated by the process history. It imposes no architectural assumptions and does not
require the existence of an exact sufficient state. Furthermore, the ensuing sufficiency theorem
introduces an architecture-motivated factorization of this state into four components: a shared
predictive representation, a short-range state, a mid-range state, and a global recurrent memory.
This conceptualization serves as the theoretical counterpart to our unified understanding–generation–
prediction substrate, alongside its local, dilated, and global temporal pathways.
Lemma 1 (Conditional expectation is the L2-optimal predictor). Let G ⊆ F be any sub-σ-field and
let Y ∈ L2(Ω,F,P). Define η := E[Y | G]. Then η is the unique minimizer of squared risk over
|     |     |     |     | G   |     | G   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
L2(G),
i.e.,
|     |     |     |     | inf | E[(Y | −Z)2] = E[(Y | −η  | )2]. |     | (57) |
| --- | --- | --- | --- | --- | ---- | ------------ | --- | ---- | --- | ---- |
G
Z∈L2(G)
| Moreover, | for   | every | Z ∈     | L2(G),     |     |               |     |        |     |      |
| --------- | ----- | ----- | ------- | ---------- | --- | ------------- | --- | ------ | --- | ---- |
|           |       |       |         | E[(Y −Z)2] |     | E[(Y )2]+E[(η |     | −Z)2]. |     | (58) |
|           |       |       |         |            | =   | −η            |     |        |     |      |
|           |       |       |         |            |     | G             |     | G      |     |      |
| Proof of  | Lemma | 1.    | Fix any | Z ∈ L2(G)  | and | write         |     |        |     |      |
|           |       |       |         |            | η   | := η = E[Y |  | G]. |        |     |      |
G
Then
|           |      |               |       | Y                   | −Z                    | = (Y −η)+(η−Z). |     |            |           |      |
| --------- | ---- | ------------- | ----- | ------------------- | --------------------- | --------------- | --- | ---------- | --------- | ---- |
| Squaring  | both | sides         | and   | taking expectations |                       | gives           |     |            |           |      |
|           |      | E[(Y          | −Z)2] | = E[(Y              | −η)2]+E[(η−Z)2]+2E[(Y |                 |     | −η)(η−Z)]. |           | (59) |
| Since η−Z | is   | G-measurable, |       |                     |                       |                 |     |            |           |      |
|           |      |               |       |                     |                       | (cid:104)       |     |            | (cid:105) |      |
|           |      |               |       | E[(Y                |                       | E E[(Y          |     |            |           |      |
|           |      |               |       | −η)(η−Z)]           |                       | = −η)(η−Z)      |     | | G]       |           |      |
|           |      |               |       |                     |                       | (cid:104)       |     |            | (cid:105) |      |
|           |      |               |       |                     |                       | = E (η−Z)E[Y    | −η  | | G]       | = 0,      | (60) |
because E[Y E[Y 0. Substituting back into Eq. (59) proves Eq. (58), and Eq.
|     |     | −η | | G] = | | G]−η | =   |     |     |     |     |     |
| --- | --- | ---- | ---- | ------ | --- | --- | --- | --- | --- | --- |
(57) follows immediately. Uniqueness holds because equality requires E[(η−Z)2] 0, i.e.,
= Z = η
almost surely.
| B.2 Necessity |     | of  | Persistent | Internal | States |     |     |     |     |     |
| ------------- | --- | --- | ---------- | -------- | ------ | --- | --- | --- | --- | --- |
This subsection formalizes the obstruction faced by purely local temporal models. In long-horizon
prediction, two historical trajectories might share identical recent observations and actions yet
differ in earlier unobserved or supra-window events that dictate the future. Such events include
instances where an object remains present despite temporary occlusion, the prior triggering of a
delayed physical effect, or the completion of a specific stage in a task involving multiple steps.
Consequently, predictors relying solely on recent windows are not merely more difficult to train but
| are fundamentally |     |     | insufficient | from | a statistical | perspective. |     |     |     |     |
| ----------------- | --- | --- | ------------ | ---- | ------------- | ------------ | --- | --- | --- | --- |
107

|          | (Supra-window |              |     | dependence |               | implies  | the     | necessity | of      | persistent |         | state). |           |
| -------- | ------------- | ------------ | --- | ---------- | ------------- | -------- | ------- | --------- | ------- | ---------- | ------- | ------- | --------- |
| Theorem  | 3             |              |     |            |               |          |         |           |         |            |         | Fix t ≥ | 1, τ ≥ 1, |
| and 1 ≤  | w < t,        | and define   |     |            |               |          |         |           |         |            |         |         |           |
|          |               |              |     |            | E[Y           |          |         | (w)       | E[Y     | (w)        |         |         | (61)      |
|          |               |              |     | m t :=     |               | | H t ], | m       | :=        |         | | W        | ].      |         |           |
|          |               |              |     |            |               |          |         | t         |         | t          |         |         |           |
| Then the | following     | statements   |     | hold.      |               |          |         |           |         |            |         |         |           |
| (i) The  | optimal       | full-history |     | and        | recent-window |          | risks   | are       |         |            |         |         |           |
|          |               |              |     | R⋆         | =             | E[(Y     | −m )2]  | =         | E[Var(Y | | H        | )],     |         | (62)      |
|          |               |              |     |            | full          |          | t       |           |         |            | t       |         |           |
|          |               |              |     | R⋆         | = E[(Y        | −m       | (w) )2] | = E[Var(Y |         | | W        | (w) )]. |         | (63)      |
|          |               |              |     | w          |               |          | t       |           |         | t          |         |         |           |
(ii)
The excess risk incurred by restricting prediction to the recent window satisfies the exact identity
|     |     |     |     | R⋆ −R⋆ |      | E[(m | (w)  | )2] | E(cid:2) |     | (w) | (cid:3) | (64) |
| --- | --- | --- | --- | ------ | ---- | ---- | ---- | --- | -------- | --- | --- | ------- | ---- |
|     |     |     |     |        | =    |      | t −m |     | = Var(m  | t   | | W | ) .     |      |
|     |     |     |     | w      | full |      | t    |     |          |     | t   |         |      |
(iii)
Consequently,
|     |     |     |     | R⋆  | R⋆   |     |     |        | (w) |              |     |     | (65) |
| --- | --- | --- | --- | --- | ---- | --- | --- | ------ | --- | ------------ | --- | --- | ---- |
|     |     |     |     | >   |      | ⇐⇒  | m   | is not | W   | -measurable. |     |     |      |
|     |     |     |     | w   | full |     |     | t      | t   |              |     |     |      |
Specifically, if the Bayes predictor cannot be fully recovered from the most recent w steps, every
window-restricted predictor inherently incurs a strictly positive, irreducible excess risk. Consequently,
any Bayes-optimal recursive architecture must retain supra-window information, and implementing
such retention via recursive state propagation necessitates a persistent internal state.
Part(i)followsdirectlyfromLemma1withG andG (w), respectively.
| Proof of | Theorem | 3.  |     |     |     |     |     |     |     | =   | H   | = W |     |
| -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|          |         |     |     |     |     |     |     |     |     |     | t   | t   |     |
Indeed,
|     |     |     | R⋆  | = E[(Y | −m  | )2], |     | R⋆ = | E[(Y | −m (w) | )2], |     |     |
| --- | --- | --- | --- | ------ | --- | ---- | --- | ---- | ---- | ------ | ---- | --- | --- |
|     |     |     |     | full   |     | t    |     | w    |      | t      |      |     |     |
and these equalities are equivalent to Eq. (62) and Eq. (63) by the definition of conditional variance.
| For part       | (ii), | start from | the | decomposition |     |      |      |      |      |     |     |     |      |
| -------------- | ----- | ---------- | --- | ------------- | --- | ---- | ---- | ---- | ---- | --- | --- | --- | ---- |
|                |       |            |     |               | (w) |      |      |      |      | (w) |     |     | (66) |
|                |       |            |     | Y −m          |     | = (Y | −m t | )+(m | t −m | ).  |     |     |      |
|                |       |            |     |               | t   |      |      |      |      | t   |     |     |      |
| After squaring |       | and taking |     | expectations, |     |      |      |      |      |     |     |     |      |
E[(Y −m (w) )2] = E[(Y −m )2]+E[(m −m (w) )2]+2E[(Y −m )(m −m (w) )]. (67)
|         |      | t    |     |     | t            |      | t         | t      |          |       | t     | t t       |      |
| ------- | ---- | ---- | --- | --- | ------------ | ---- | --------- | ------ | -------- | ----- | ----- | --------- | ---- |
| Because | both | and  | (w) | are | -measurable, |      | so is     |        | (w).     | Hence |       |           |      |
|         |      | m t  | m   | H   | t            |      |           | m t −m |          |       |       |           |      |
|         |      |      | t   |     |              |      |           |        | t        |       |       |           |      |
|         |      |      |     |     |              |      | (cid:104) |        |          |       |       | (cid:105) |      |
|         |      |      |     |     | (w)          |      |           |        |          | (w)   |       |           |      |
|         |      | E[(Y | −m  | )(m | −m           | )] = | E E[(Y    | −m     | )(m      | −m    | ) | H | ]         |      |
|         |      |      |     | t t | t            |      |           |        | t t      | t     |       | t         |      |
|         |      |      |     |     |              |      | (cid:104) |        |          |       |       | (cid:105) |      |
|         |      |      |     |     |              |      | E         |        | (w) )E[Y |       |       |           | (68) |
|         |      |      |     |     |              | =    | (m        | −m     |          | −m    | | H   | ] = 0.    |      |
|         |      |      |     |     |              |      | t         |        | t        |       | t t   |           |      |
Therefore,
|     |     |     |     |     | R⋆ −R⋆ |      | E[(m |     | (w) )2]. |     |     |     | (69) |
| --- | --- | --- | --- | --- | ------ | ---- | ---- | --- | -------- | --- | --- | --- | ---- |
|     |     |     |     |     |        |      | =    | −m  |          |     |     |     |      |
|     |     |     |     |     | w      | full |      | t   | t        |     |     |     |      |
To derive the second expression in Eq. (64), note that by the tower property,
|     |     |     |     |     |     | m (w) = | E[m | | W (w) | ].  |     |     |     | (70) |
| --- | --- | --- | --- | --- | --- | ------- | --- | ------- | --- | --- | --- | --- | ---- |
|     |     |     |     |     |     | t       | t   | t       |     |     |     |     |      |
108

Thus
|     |     |     |     |     |        | (w) |     | −E[m  | (w)  |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | ----- | ---- | --- | --- | --- | --- |
|     |     |     |     |     | m t −m |     | = m | t t | | W ], |     |     |     |     |
|     |     |     |     |     |        | t   |     |       | t    |     |     |     |     |
and applying the conditional-variance identity to the random variable conditioned on (w) gives
|           |        |          |               |      |        |      |       |          |     | m       |     | W    |      |
| --------- | ------ | -------- | ------------- | ---- | ------ | ---- | ----- | -------- | --- | ------- | --- | ---- | ---- |
|           |        |          |               |      |        |      |       |          |     |         | t   |      | t    |
|           |        |          |               | E[(m |        | (w)  | )2]   | E(cid:2) | (w) | (cid:3) |     |      | (71) |
|           |        |          |               |      |        | −m   | =     | Var(m    | | W | ) .     |     |      |      |
|           |        |          |               |      | t      | t    |       | t        | t   |         |     |      |      |
| Combining | Eq.    | (69)     | and Eq.       | (71) | proves | part | (ii). |          |     |         |     |      |      |
| For part  | (iii), | Eq. (69) | implies       |      |        |      |       |          |     |         |     |      |      |
|           |        | R⋆       | R⋆            |      |        | E[(m | (w)   | )2]      |     |         | (w) | a.s. |      |
|           |        |          | =             | ⇐⇒   |        | t    | −m    | = 0      | ⇐⇒  | m t =   | m   |      |      |
|           |        | w        | full          |      |        |      | t     |          |     |         | t   |      |      |
| Using Eq. | (70),  | this     | is equivalent |      | to     |      |       |          |     |         |     |      |      |
(w)
|     |     |     |     |     |     | m = | E[m | | W ] a.s. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | t   | t   | t          |     |     |     |     |     |
A square-integrable random variable equals its conditional expectation with respect to a σ-field if
| and only | if it | is measurable |              | with | respect | to  | that | σ-field. Hence       |     |     |     |     |     |
| -------- | ----- | ------------- | ------------ | ---- | ------- | --- | ---- | -------------------- | --- | --- | --- | --- | --- |
|          |       |               |              | R⋆ = | R⋆      | ⇐⇒  | m    | is W (w)-measurable, |     |     |     |     |     |
|          |       |               |              | w    | full    |     |      | t t                  |     |     |     |     |     |
| and Eq.  | (65)  | follows       | by negation. |      |         |     |      |                      |     |     |     |     |     |
Corollary 3 (Explicit lower bound under an atomic recent-window mismatch). Suppose there is
a window value s for which the event E := {W (w) = s} occurs with positive probability, P(E) > 0.
t
Furthermore, suppose there exist disjoint events E ,E ∈ H that partition E into E ∪E = E,
|     |     |     |     |     |     |     |     | 1 2 | t   |     |     | 1   | 2   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
R,
along with distinct constants µ 1 ,µ 2 ∈ such that m t = µ 1 almost surely on E 1 and m t = µ 2 almost
surely on E . If we define the conditional probability α := P(E | E) ∈ (0,1), then the excess risk is
|          | 2         |     |               |     |     |      |              |           | 1           |     |     |     |      |
| -------- | --------- | --- | ------------- | --- | --- | ---- | ------------ | --------- | ----------- | --- | --- | --- | ---- |
| bounded  | below     | by  |               |     |     |      |              |           |             |     |     |     |      |
|          |           |     |               | R⋆  | −R⋆ |      | P(E)α(1−α)(µ |           |             | )2. |     |     | (72) |
|          |           |     |               |     |     | ≥    |              |           | −µ          |     |     |     |      |
|          |           |     |               |     | w   | full |              |           | 1 2         |     |     |     |      |
| Proof of | Corollary |     | 3. By Theorem |     | 3,  |      |              |           |             |     |     |     |      |
|          |           |     |               |     |     |      | E(cid:2)     |           | (w) (cid:3) |     |     |     |      |
|          |           |     |               |     | R⋆  | −R⋆  | =            | Var(m | W | ) .         |     |     |     | (73) |
|          |           |     |               |     | w   | full |              | t         | t           |     |     |     |      |
Since conditional variance is nonnegative almost surely, we may restrict the expectation to the event
E and obtain
|     |     |     |     |     |        |      | E(cid:2) | (w) |     | (cid:3) |     |     |      |
| --- | --- | --- | --- | --- | ------ | ---- | -------- | --- | --- | ------- | --- | --- | ---- |
|     |     |     |     |     | R⋆ −R⋆ | ≥    | Var(m    | | W | )1  | .       |     |     | (74) |
|     |     |     |     |     | w      | full |          | t t | E   |         |     |     |      |
Now (w) (w) and, by assumption, it is an atom of the σ-field (w). Hence every
| E   | = {W | =   | s} ∈ W |     |     |     |     |     |     |     |     | W   |     |
| --- | ---- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |      | t   |        | t   |     |     |     |     |     |     |     | t   |     |
(w)-measurable random variable is almost surely constant on E. In particular, there exists a
W
t
| constant |     | R such | that |     |     |     |     |     |     |     |     |     |     |
| -------- | --- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
c ∈
|     |     |     |     |     | Var(m | | W | (w) ) | = c a.s. | on E. |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | ----- | -------- | ----- | --- | --- | --- | --- |
|     |     |     |     |     |       | t   | t     |          |       |     |     |     |     |
Moreover, because (w) almost surely on E, conditioning on (w) and restricting to is
|            |     |              | W   | = s    |       |           |       |       |     | W   |     |     | E   |
| ---------- | --- | ------------ | --- | ------ | ----- | --------- | ----- | ----- | --- | --- | --- | --- | --- |
|            |     |              | t   |        |       |           |       |       |     |     | t   |     |     |
| equivalent | to  | conditioning |     | on the | event | E itself. |       | Thus  |     |     |     |     |     |
|            |     |              |     |        |       | c =       | Var(m | | E), |     |     |     |     |     |
t
and therefore
|     |     |     |     | E(cid:2) |     |         |     | (cid:3)      |     |       |     |     |      |
| --- | --- | --- | --- | -------- | --- | ------- | --- | ------------ | --- | ----- | --- | --- | ---- |
|     |     |     |     | Var(m    |     | | W (w) | )1  | = P(E) Var(m |     | | E). |     |     | (75) |
|     |     |     |     |          | t   | t       | E   |              | t   |       |     |     |      |
109

| Next, since | and | form | a   | partition | of E, | and |     |     |     |     |     |     |     |
| ----------- | --- | ---- | --- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
E E
|     | 1   | 2   |     |     |         |     |     |          |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | --- | -------- | --- | --- | --- | --- | --- |
|     |     |     | m = | µ   | a.s. on | E , | m   | = µ a.s. | on  | E , |     |     |     |
|     |     |     | t   | 1   |         | 1   | t   | 2        |     | 2   |     |     |     |
it follows that under the conditional law given E, the random variable m takes the value µ with
|     |     |     |     |     |     |     |     |     |     | t   |     |     | 1   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
probability
P(E
|         |              |             |     |     |     | 1 | | E) = α, |     |     |     |     |     |     |
| ------- | ------------ | ----------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
| and the | value µ with | probability |     |     |     |     |         |     |     |     |     |     |     |
2
P(E
|     |     |     |     |     |     | | E) | = 1−α. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | ------ | --- | --- | --- | --- | --- | --- |
2
Hence
|     |     |     |     | E[m | | E] | = αµ | +(1−α)µ |     | ,   |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | ---- | ------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | t    |      | 1       | 2   |     |     |     |     |     |
and
|     |     |     |     | E[m2 |      | αµ2+(1−α)µ2. |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---- | ---- | ------------ | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |      | | E] | =            |     |     |     |     |     |     |     |
|     |     |     |     |      | t    |              | 1   |     | 2   |     |     |     |     |
Therefore
|     |     | Var(m |     | | E) = | E[m2         | | E]− | (cid:0)E[m | | E] (cid:1)2 |     |          |     |     |      |
| --- | --- | ----- | --- | ------ | ------------ | ----- | ---------- | ------------- | --- | -------- | --- | --- | ---- |
|     |     |       | t   |        | t            |       |            | t             |     |          |     |     |      |
|     |     |       |     |        |              |       |            | (cid:0)       |     | (cid:1)2 |     |     |      |
|     |     |       |     | =      | αµ2+(1−α)µ2− |       |            | αµ +(1−α)µ    |     |          |     |     |      |
|     |     |       |     |        | 1            |       | 2          | 1             |     | 2        |     |     |      |
|     |     |       |     |        |              |       | )2.        |               |     |          |     |     | (76) |
|     |     |       |     | =      | α(1−α)(µ     |       | −µ         |               |     |          |     |     |      |
1 2
| Combining | Eq. (74),              | Eq.   | (75), | and              | Eq. (76)    | yields       |         |     |               |           |          |     |      |
| --------- | ---------------------- | ----- | ----- | ---------------- | ----------- | ------------ | ------- | --- | ------------- | --------- | -------- | --- | ---- |
|           |                        |       | R⋆    | −R⋆              | ≥           | P(E)α(1−α)(µ |         | −µ  | )2,           |           |          |     |      |
|           |                        |       |       | w                | full        |              |         | 1   | 2             |           |          |     |      |
| which is  | exactly Eq.            | (72). |       |                  |             |              |         |     |               |           |          |     |      |
|           | (Information-theoretic |       |       | interpretation). |             |              |         |     |               |           |          |     |      |
| Remark    | 4                      |       |       |                  |             |              | Theorem | 3   | yields        | the exact | identity |     |      |
|           |                        |       |       |                  | (cid:13)    |              |         |     | (cid:13)2     |           |          |     |      |
|           |                        |       | R⋆    | −R⋆              | (cid:13)E[Y |              | ]−E[Y   |     | (w) ](cid:13) |           |          |     | (77) |
|           |                        |       |       |                  | =           | |            | H t     | | W |               | .         |          |     |      |
|           |                        |       | w     | full             | (cid:13)    |              |         |     | t (cid:13)    |           |          |     |      |
L2
Thus, the necessity claim is quantitative rather than merely qualitative: whenever the full-history
Bayes predictor depends on information outside the recent window, every bounded-window predictor
incurs an exactly measurable irreducible excess risk. In long-horizon world modeling, this formalizes
the intuition that purely local temporal context is insufficient whenever future consistency depends on
| persistent | world state | beyond | the | visible | short-range |     | past. |     |     |     |     |     |     |
| ---------- | ----------- | ------ | --- | ------- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- |
Remark 5 (Architectural interpretation). Theorem 3 is a statement about information rather than
about a particular neural implementation. What it proves is that supra-window information must be
preserved if one seeks Bayes-optimal long-horizon prediction. In a recursive predictor, the natural
implementation of such preservation is a propagated internal memory in the sense of Definition 3.
This is the theoretical reason why a long-horizon world model requires a dedicated persistent memory
| pathway | rather than | only | local        | attention. |              |     |     |         |             |     |                |            |     |
| ------- | ----------- | ---- | ------------ | ---------- | ------------ | --- | --- | ------- | ----------- | --- | -------------- | ---------- | --- |
|         | (Connection | to   | long-horizon |            | evaluation). |     |     |         |             |     |                |            |     |
| Remark  | 6           |      |              |            |              |     | To  | connect | the theorem |     | with practical | scenarios, |     |
let Y denote a future target directly relevant to long-horizon world-model evaluation. This target
could be a future latent-frame coordinate, an object-identity consistency variable, a collision outcome,
or a task-progress indicator situated several seconds ahead. Consequently, the gap presented in Eq.
(64) provides a formal expression for the identical difficulty probed by our long-horizon evaluations.
Specifically, whenever the historical cause governing the future target remains unrecoverable from the
recent local window alone, any purely local temporal model inevitably incurs a nonzero prediction gap
| regardless | of its optimization |     | quality. |     |     |     |     |     |     |     |     |     |     |
| ---------- | ------------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
110

B.3 Approximate Sufficiency of a Hybrid Multi-Scale Temporal Memory
The necessity result explains why some persistent state is unavoidable, but it does not yet explain
why the particular temporal factorization used in the architecture is adequate. We now show that
a hybrid multi-scale temporal memory is approximately sufficient whenever the Bayes predictor
admits the corresponding decomposition and the global recurrent memory evolves stably. The result
formalizes the complementary roles of a shared predictive representation, a short-range local branch,
a mid-range branch, and a global memory branch.
Definition 5 (Exact hybrid multi-scale predictive decomposition). We say that the Bayes predictor
admits an exact hybrid multi-scale predictive decomposition if there exist square-integrable, H -
t
measurable random variables
U⋆ ∈ RdU, C⋆ ∈ RdC, D⋆ ∈ RdD, G⋆ ∈ Rdv×d k,
t t t t
together with a measurable decoder
h : RdU ×RdC ×RdD ×Rdv×d k → R,
t
such that
µ⋆ := E[Y | H ] = h (U⋆,C⋆,D⋆,G⋆) a.s. (78)
t t t t t t t
The four components are interpreted as follows:
• U⋆: a shared physical predictive state;
t
• C⋆: a short-range local state;
t
• D⋆: a mid-range dilated state;
t
• G⋆: a global recurrent causal memory.
t
Remark 7 (Architecture correspondence). Although stated abstractly, Definition 5 is specifically
designed to parallel our concrete temporal factorization. Within the implemented architecture, C⋆
t
and D⋆ map to the short- and mid-range temporal pathways instantiated by SWA and DSWA.
t
Furthermore, G⋆ represents the global gated memory pathway instantiated by GLA. Finally, the
t
variable U⋆ embodies the shared predictive substrate that is continuously reused across understanding,
t
generation, and prediction tasks.
Definition 6 (Hybrid multi-scale predictor and gated global-memory update). A hybrid multi-scale
predictor is of the form
µˆ = h (Uˆ ,Cˆ ,Dˆ ,Gˆ ), (79)
t t t t t t
where Uˆ ,Cˆ ,Dˆ ,Gˆ are square-integrable, H -measurable estimators of U⋆,C⋆,D⋆,G⋆, respectively.
t t t t t t t t t
The global-memory branch is modeled by a gated delta update. Given a decay gate α ∈ (0,1), a
writing strength β ∈ (0,1), a current value v ∈ Rdv, and a key k ∈ Rd k, we define the update map
for a state S ∈ Rdv×d k as follows:
F(S;α,β,v,k) := αS +β(v−Sk)k⊤, S ∈ Rdv×d k. (80)
Then the exact and learned global memories satisfy
G⋆ = F(G⋆ ;α⋆,β⋆,v⋆,k⋆), (81)
t t−1 t t t t
Gˆ = F(Gˆ ;αˆ ,βˆ,vˆ,kˆ ). (82)
t t−1 t t t t
111

|            |            | (Non-global |        | branch        | approximation |      |        | quality). |        |         |        |             |               |      |
| ---------- | ---------- | ----------- | ------ | ------------- | ------------- | ---- | ------ | --------- | ------ | ------- | ------ | ----------- | ------------- | ---- |
| Definition | 7          |             |        |               |               |      |        |           |        | For the | hybrid | predictor   | in Definition | 6,   |
| define the | non-global |             | branch | approximation |               |      | errors | at        | time t | by      |        |             |               |      |
|            | εU         | := ∥Uˆ      | −U⋆∥   |               | ,             | εSWA | := ∥Cˆ | −C⋆∥      | ,      | εDSWA   |        | := ∥Dˆ −D⋆∥ | .             | (83) |
|            | t          |             | t      | t L2          |               | t    |        | t         | t L2   |         | t      | t t         | L2            |      |
Here, εU measures the approximation quality of the shared predictive substrate, εSWA measures the
| t   |     |     |     |     |     |     |     |     |     |     |     | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
short-range branch error, and εDSWA measures the mid-range branch error.
t
| Definition | 8   | (One-step |     | gate approximation |        |      | errors). |     | Define     |             |              |     |     |      |
| ---------- | --- | --------- | --- | ------------------ | ------ | ---- | -------- | --- | ---------- | ----------- | ------------ | --- | --- | ---- |
|            |     |           |     |                    |        |      |          |     | (cid:13)   |             | (cid:13)     |     |     |      |
|            |     |           |     | εα                 |        | −α⋆∥ |          | εβ  | (cid:13)βˆ | −β⋆(cid:13) |              |     |     | (84) |
|            |     |           |     |                    | := ∥αˆ | t    | ,        |     | :=         | t           |              | ,   |     |      |
|            |     |           |     | t                  |        | t    | L2       |     | t (cid:13) |             | t(cid:13) L2 |     |     |      |
|            |     |           |     |                    |        |      |          |     | (cid:13)   |             | (cid:13)     |     |     |      |
(cid:13)kˆ
|     |     |     |     | εv  | := ∥vˆ | −v⋆∥ | ,   | εk  | :=       | −k⋆(cid:13) |           | .   |     | (85) |
| --- | --- | --- | --- | --- | ------ | ---- | --- | --- | -------- | ----------- | --------- | --- | --- | ---- |
|     |     |     |     | t   |        | t t  | L2  | t   | (cid:13) | t           | t(cid:13) |     |     |      |
L2
| Also define | the | initial | global-memory |     |     | discrepancy |            |             |           |     |     |     |     |      |
| ----------- | --- | ------- | ------------- | --- | --- | ----------- | ---------- | ----------- | --------- | --- | --- | --- | --- | ---- |
|             |     |         |               |     |     |             | (cid:13)   |             | (cid:13)  |     |     |     |     |      |
|             |     |         |               |     |     |             | (cid:13)Gˆ | −G⋆(cid:13) |           |     |     |     |     | (86) |
|             |     |         |               |     |     | e           | :=         |             |           | .   |     |     |     |      |
|             |     |         |               |     |     | 0           | (cid:13)   | 0           | 0(cid:13) |     |     |     |     |      |
L2
| For convenience, |        | define | the | Bayes      | risk |      |      |        |         |     |     |     |     |      |
| ---------------- | ------ | ------ | --- | ---------- | ---- | ---- | ---- | ------ | ------- | --- | --- | --- | --- | ---- |
|                  |        |        |     |            | R⋆   | := R | (µ⋆) | = E[(Y | −µ⋆)2]. |     |     |     |     | (87) |
|                  |        |        |     |            |      | t    | t t  |        |         | t   |     |     |     |      |
|                  | (Bayes | excess |     | identity). |      |      |      |        |         |     |     |     |     |      |
Lemma 2 For any square-integrable, H t -measurable predictor µˆ t ,
|          |       |     |        |         |            | )−R⋆    |           |       | −µ⋆∥2 |          |              |     |     | (88) |
| -------- | ----- | --- | ------ | ------- | ---------- | ------- | --------- | ----- | ----- | -------- | ------------ | --- | --- | ---- |
|          |       |     |        |         | R          | t (µˆ t |           | = ∥µˆ | t     | .        |              |     |     |      |
|          |       |     |        |         |            |         | t         |       | t     | L2       |              |     |     |      |
|          |       |     | Recall | that    |            |         |           |       |       |          |              |     |     |      |
| Proof of | Lemma | 2.  |        |         |            |         |           |       |       |          |              |     |     |      |
|          |       |     |        |         | E(cid:2)   |         | )2(cid:3) |       | R⋆    | E(cid:2) | −µ⋆)2(cid:3) |     |     |      |
|          |       |     |        | R t (µˆ | t ) =      | (Y −µˆ  | t         | ,     | =     | (Y       |              | ,   |     |      |
|          |       |     |        |         |            |         |           |       | t     |          | t            |     |     |      |
| where µ⋆ | E[Y   |     | is the | Bayes   | predictor. |         | Hence,    |       |       |          |              |     |     |      |
|          | =     | | H | t ]    |         |            |         |           |       |       |          |              |     |     |      |
t
|              |     |            |      | R          | (µˆ )−R⋆ | =         | E(cid:2) (Y | −µˆ         | )2−(Y | −µ⋆)2(cid:3) | .        |       |     | (89) |
| ------------ | --- | ---------- | ---- | ---------- | -------- | --------- | ----------- | ----------- | ----- | ------------ | -------- | ----- | --- | ---- |
|              |     |            |      |            | t t      | t         |             |             | t     |              | t        |       |     |      |
| Expanding    | the | difference |      | of squares |          | gives     |             |             |       |              |          |       |     |      |
|              |     |            |      |            |          |           | (cid:0)     |             |       |              | (cid:1)2 |       |     |      |
|              |     | (Y         | −µˆ  | )2−(Y      | −µ⋆)2    | =         | (Y          | −µ⋆)+(µ⋆−µˆ |       |              | ) −(Y    | −µ⋆)2 |     |      |
|              |     |            |      | t          |          | t         |             | t           |       | t t          |          | t     |     |      |
|              |     |            |      |            |          |           | (µ⋆−µˆ      | )2+2(Y      |       | −µ⋆)(µ⋆−µˆ   |          |       |     | (90) |
|              |     |            |      |            |          | =         |             |             |       |              |          | ).    |     |      |
|              |     |            |      |            |          |           | t           | t           |       |              | t t      | t     |     |      |
| Substituting |     | Eq. (90)   | into | Eq.        | (89),    | we obtain |             |             |       |              |          |       |     |      |
)−R⋆ E(cid:2) (µ⋆−µˆ )2(cid:3) +2E(cid:2) −µ⋆)(µ⋆−µˆ (cid:3) (91)
|              |         |     | R t (µˆ | t    | =   |       | t    |           | (Y  |     |     | t ) . |     |     |
| ------------ | ------- | --- | ------- | ---- | --- | ----- | ---- | --------- | --- | --- | --- | ----- | --- | --- |
|              |         |     |         |      | t   |       | t    |           |     |     | t t |       |     |     |
| It therefore | remains |     | to show | that | the | cross | term | vanishes. |     |     |     |       |     |     |
Since both and µ⋆ are -measurable, the difference µ⋆−µˆ is also -measurable and square-
|             | µˆ t |           |          | H t           |     |     |                          |     |            | t   |     | H t            |     |      |
| ----------- | ---- | --------- | -------- | ------------- | --- | --- | ------------------------ | --- | ---------- | --- | --- | -------------- | --- | ---- |
|             |      |           | t        |               |     |     |                          |     | t          |     |     |                |     |      |
| integrable. | By   | the tower |          | property,     |     |     |                          |     |            |     |     |                |     |      |
|             |      |           | E(cid:2) |               |     |     | (cid:3) E(cid:2)E(cid:2) |     |            |     |     | (cid:3)(cid:3) |     |      |
|             |      |           |          | (Y −µ⋆)(µ⋆−µˆ |     |     | ) =                      | (Y  | −µ⋆)(µ⋆−µˆ |     | )   | | H            |     |      |
|             |      |           |          |               | t t | t   |                          |     |            | t t | t   | t              |     |      |
|             |      |           |          |               |     |     | = E[(µ⋆−µˆ               |     | )E[Y       | −µ⋆ | |   | H ]].          |     | (92) |
|             |      |           |          |               |     |     |                          | t   | t          |     | t   | t              |     |      |
112

| Because  |            | E[Y | ],   | we have |          |            |         |           |         |      |     |     |     |     |
| -------- | ---------- | --- | ---- | ------- | -------- | ---------- | ------- | --------- | ------- | ---- | --- | --- | --- | --- |
|          | µ⋆ =       | |   | H    |         |          |            |         |           |         |      |     |     |     |     |
|          | t          |     | t    |         |          |            |         |           |         |      |     |     |     |     |
|          |            |     |      | E[Y     | −µ⋆      | | H        | ] = E[Y | |         | H ]−µ⋆  | = 0. |     |     |     |     |
|          |            |     |      |         |          | t          | t       |           | t       | t    |     |     |     |     |
| Thus the | right-hand |     | side | of Eq.  | (92) is  | zero,      | and     | therefore |         |      |     |     |     |     |
|          |            |     |      |         | E(cid:2) | −µ⋆)(µ⋆−µˆ |         |           | (cid:3) |      |     |     |     |     |
|          |            |     |      |         |          | (Y         |         |           | t ) =   | 0.   |     |     |     |     |
t t
| Returning    | to           | Eq. (91), | we  | conclude  | that  |          |        |           |       |           |     |        |          |       |
| ------------ | ------------ | --------- | --- | --------- | ----- | -------- | ------ | --------- | ----- | --------- | --- | ------ | -------- | ----- |
|              |              |           |     |           | )−R⋆  | E(cid:2) | (µ⋆−µˆ | )2(cid:3) |       | −µ⋆∥2     |     |        |          | (93)  |
|              |              |           |     | R (µˆ     |       | =        |        |           | = ∥µˆ |           | ,   |        |          |       |
|              |              |           |     | t t       |       | t        | t      | t         |       | t t       | L2  |        |          |       |
| which proves |              | Eq. (88). |     |           |       |          |        |           |       |           |     |        |          |       |
|              | (Contraction |           | of  | the exact | gated |          | delta  | update).  |       |           |     |        |          |       |
| Lemma        | 3            |           |     |           |       |          |        |           | Fix   | (α,β,v,k) | and | define | F by Eq. | (80). |
Let ρ := α+β∥k∥2. Suppose ∥k∥2 < 1−α. Therefore, given α,β ∈ (0,1), the update is strictly
|             |      | 2        |     |                   | 2   |     |     |       |       |     |     |     |     |     |
| ----------- | ---- | -------- | --- | ----------------- | --- | --- | --- | ----- | ----- | --- | --- | --- | --- | --- |
| contractive | with | a factor |     | ρ < 1, satisfying |     | for | all | S,T ∈ | Rdv×d | k:  |     |     |     |     |
(94)
|     |     |     | ∥F(S;α,β,v,k)−F(T;α,β,v,k)∥ |     |     |     |     |     | ≤   | ρ∥S | −T∥ . |     |     |     |
| --- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|     |     |     |                             |     |     |     |     |     | F   |     | F     |     |     |     |
Proof of Lemma 3. We prove that the gated delta update is contractive with respect to its memory-
| state argument. |     | Fix | two | memory | states |     | Rdv×d |       | and let |     |     |     |     |     |
| --------------- | --- | --- | --- | ------ | ------ | --- | ----- | ----- | ------- | --- | --- | --- | --- | --- |
|                 |     |     |     |        |        | S,T | ∈     | k     |         |     |     |     |     |     |
|                 |     |     |     |        |        |     | ∆ :=  | S −T. |         |     |     |     |     |     |
Since the value term appears identically in both updates, it cancels when taking the difference.
v
| Indeed, | by the | definition |     | of in | Eq. (80), |     |     |     |     |     |     |     |     |     |
| ------- | ------ | ---------- | --- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
F
|     | F(S;α,β,v,k)−F(T;α,β,v,k) |     |     |     |     |     | = αS        | +β(v−Sk)k⊤−αT |         |               | −β(v−Tk)k⊤ |     |            |      |
| --- | ------------------------- | --- | --- | --- | --- | --- | ----------- | ------------- | ------- | ------------- | ---------- | --- | ---------- | ---- |
|     |                           |     |     |     |     |     |             |               | (cid:2) |               |            |     | (cid:3) k⊤ |      |
|     |                           |     |     |     |     |     | = α(S       | −T)+β         |         | (v−Sk)−(v−Tk) |            |     |            |      |
|     |                           |     |     |     |     |     | = α∆−β∆kk⊤. |               |         |               |            |     |            | (95) |
Thus,thedifferencebetweenthetwoupdatedmemorystatesdependsonlyonthepreviousdiscrepancy
| and | on the | rank-one | correction |     | induced | by  | the | key k. |     |     |     |     |     |     |
| --- | ------ | -------- | ---------- | --- | ------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
∆
We now bound the Frobenius norm of the right-hand side. By the triangle inequality,
|            |     | ∥F(S;α,β,v,k)−F(T;α,β,v,k)∥ |     |        |       |         |       |         | ≤ α∥∆∥ | +β∥∆kk⊤∥ |     | .   |     | (96) |
| ---------- | --- | --------------------------- | --- | ------ | ----- | ------- | ----- | ------- | ------ | -------- | --- | --- | --- | ---- |
|            |     |                             |     |        |       |         |       | F       |        | F        |     | F   |     |      |
| It remains | to  | control                     | the | second | term. | Observe | first | that    |        |          |     |     |     |      |
|            |     |                             |     |        |       | ∆kk⊤    |       | (∆k)k⊤. |        |          |     |     |     |      |
=
This is a rank-one matrix. For any vectors a and b, the Frobenius norm of the outer product
| factorizes | as  |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∥ab⊤∥
|          |      |          |      |        |        |            | F =      | ∥a∥ 2 | ∥b∥ 2 . |     |     |     |     |      |
| -------- | ---- | -------- | ---- | ------ | ------ | ---------- | -------- | ----- | ------- | --- | --- | --- | --- | ---- |
| Applying | this | identity | with | a =    | ∆k and | b =        | k yields |       |         |     |     |     |     |      |
|          |      |          |      | ∥∆kk⊤∥ |        | = ∥(∆k)k⊤∥ |          |       | = ∥∆k∥  | ∥k∥ | .   |     |     | (97) |
|          |      |          |      |        |        | F          |          | F     |         | 2   | 2   |     |     |      |
Next, using the standard operator-norm inequality together with , we obtain
|     |     |     |     |     |      |       |     |     |     | ∥∆∥   | 2 ≤ ∥∆∥ | F   |     |      |
| --- | --- | --- | --- | --- | ---- | ----- | --- | --- | --- | ----- | ------- | --- | --- | ---- |
|     |     |     |     |     | ∥∆k∥ | ≤ ∥∆∥ | ∥k∥ | ≤   | ∥∆∥ | ∥k∥ . |         |     |     | (98) |
|     |     |     |     |     | 2    |       | 2   | 2   | F   | 2     |         |     |     |      |
113

Combining Eq. (97) and Eq. (98), we conclude that
∥∆kk⊤∥ ≤ ∥∆∥ ∥k∥2. (99)
F F 2
Substituting Eq. (99) into Eq. (96) gives
∥F(S;α,β,v,k)−F(T;α,β,v,k)∥ ≤ α∥∆∥ +β∥∆∥ ∥k∥2
F F F 2
= (cid:0) α+β∥k∥2(cid:1) ∥∆∥ . (100)
2 F
Then we obtain
∥F(S;α,β,v,k)−F(T;α,β,v,k)∥ ≤ ρ∥∆∥ = ρ∥S −T∥ . (101)
F F F
This proves Eq. (94).
Lemma 4 (One-step perturbation bound for the global-memory update). Fix t ≥ 1 and define the
one-step update discrepancies by
εα := ∥αˆ −α⋆∥ , εβ := ∥βˆ −β⋆∥ , εv := ∥vˆ −v⋆∥ , εk := ∥kˆ −k⋆∥ . (102)
t t t L2 t t t L2 t t t L2 t t t L2
For notational convenience, let B ,B ,B > 0 denote envelope constants satisfying ∥Gˆ ∥ ≤ B ,
G k v t−1 F G
∥kˆ ∥ ,∥k⋆∥ ≤ B , and ∥vˆ∥ ,∥v⋆∥ ≤ B almost surely. Define
t 2 t 2 k t 2 t 2 v
ξ := B εα+B (B +B B )εβ +B εv +(B +2B B )εk. (103)
t G t k v G k t k t v G k t
Then
(cid:13) (cid:13)
(cid:13)F(Gˆ ;αˆ ,βˆ,vˆ,kˆ )−F(Gˆ ;α⋆,β⋆,v⋆,k⋆)(cid:13) ≤ ξ . (104)
(cid:13) t−1 t t t t t−1 t t t t (cid:13) t
L2
Proof of Lemma 4. For notational brevity, write
Gˆ := Gˆ , αˆ := αˆ , α⋆ := α⋆, βˆ:= βˆ, β⋆ := β⋆, vˆ:= vˆ, v⋆ := v⋆, kˆ := kˆ , k⋆ := k⋆.
t−1 t t t t t t t t
By the definition of F,
F(Gˆ;αˆ,βˆ,vˆ,kˆ)−F(Gˆ;α⋆,β⋆,v⋆,k⋆) = (αˆ−α⋆)Gˆ +(βˆ−β⋆)(vˆ−Gˆkˆ)kˆ⊤
(cid:104) (cid:105)
+β⋆ (vˆ−Gˆkˆ)kˆ⊤−(v⋆−Gˆk⋆)(k⋆)⊤ . (105)
Hence
(cid:13) (cid:13)
(cid:13)F(Gˆ;αˆ,βˆ,vˆ,kˆ)−F(Gˆ;α⋆,β⋆,v⋆,k⋆)(cid:13) ≤ T +T +T , (106)
(cid:13) (cid:13) 1 2 3
F
where
(cid:13) (cid:13) (cid:12) (cid:12) (cid:13) (cid:13)
T := |αˆ−α⋆| (cid:13)Gˆ(cid:13) , T := (cid:12)βˆ−β⋆(cid:12) (cid:13)(vˆ−Gˆkˆ)kˆ⊤(cid:13) ,
1 (cid:13) (cid:13) 2 (cid:12) (cid:12) (cid:13) (cid:13)
F F
and
(cid:13) (cid:13)
T := β⋆(cid:13)(vˆ−Gˆkˆ)kˆ⊤−(v⋆−Gˆk⋆)(k⋆)⊤(cid:13) .
3 (cid:13) (cid:13)
F
Then we obtain:
T ≤ B |αˆ−α⋆|. (107)
1 G
114

Using the fact that (cid:13) (cid:13)ab⊤ (cid:13) (cid:13) = ∥a∥ ∥b∥ , we obtain
F 2 2
(cid:12) (cid:12) (cid:13) (cid:13) (cid:13) (cid:13)
T = (cid:12)βˆ−β⋆(cid:12) (cid:13)vˆ−Gˆkˆ(cid:13) (cid:13)kˆ(cid:13)
2 (cid:12) (cid:12) (cid:13) (cid:13) (cid:13) (cid:13)
2 2
(cid:12) (cid:12)
≤ (cid:12)βˆ−β⋆(cid:12) (B +B B )B . (108)
(cid:12) (cid:12) v G k k
For T , since β⋆ ∈ (0,1), it suffices to bound the norm inside. First,
3
(vˆ−Gˆkˆ)kˆ⊤−(v⋆−Gˆk⋆)(k⋆)⊤ = (vˆ−v⋆)kˆ⊤+v⋆(kˆ−k⋆)⊤
−Gˆ(kˆkˆ⊤−k⋆(k⋆)⊤). (109)
Therefore,
(cid:13) (cid:13) (cid:13) (cid:13) (cid:13) (cid:13)
T ≤ (cid:13)(vˆ−v⋆)kˆ⊤(cid:13) +(cid:13)v⋆(kˆ−k⋆)⊤(cid:13) +(cid:13)Gˆ(kˆkˆ⊤−k⋆(k⋆)⊤)(cid:13)
3 (cid:13) (cid:13) (cid:13) (cid:13) (cid:13) (cid:13)
F F F
(cid:13) (cid:13) (cid:13) (cid:13) (cid:13) (cid:13)
≤ B ∥vˆ−v⋆∥ +B (cid:13)kˆ−k⋆(cid:13) +(cid:13)Gˆ(cid:13) (cid:13)kˆkˆ⊤−k⋆(k⋆)⊤(cid:13) . (110)
k 2 v(cid:13) (cid:13) (cid:13) (cid:13) (cid:13) (cid:13)
2 F F
Now write
kˆkˆ⊤−k⋆(k⋆)⊤ = kˆ(kˆ−k⋆)⊤+(kˆ−k⋆)(k⋆)⊤.
Hence
(cid:13) (cid:13) (cid:13) (cid:13)
(cid:13)kˆkˆ⊤−k⋆(k⋆)⊤(cid:13) ≤ 2B (cid:13)kˆ−k⋆(cid:13) , (111)
(cid:13) (cid:13) k(cid:13) (cid:13)
F 2
and therefore,
(cid:13) (cid:13)
T ≤ B ∥vˆ−v⋆∥ +(B +2B B )(cid:13)kˆ−k⋆(cid:13) . (112)
3 k 2 v G k (cid:13) (cid:13)
2
Combining Eq. (107), Eq. (108), and Eq. (112), then taking the L2 norm and applying Minkowski’s
inequality, yields
(cid:13) (cid:13)
(cid:13)F(Gˆ ;αˆ ,βˆ,vˆ,kˆ )−F(Gˆ ;α⋆,β⋆,v⋆,k⋆)(cid:13)
(cid:13) t−1 t t t t t−1 t t t t (cid:13)
L2
≤ B εα+B (B +B B )εβ +B εv +(B +2B B )εk = ξ , (113)
G t k v G k t k t v G k t t
which proves Eq. (104).
Theorem 4 (Approximate sufficiency of a hybrid multi-scale temporal memory). Suppose that the
Bayes predictor admits the decomposition in Definition 5, the decoder h is coordinate-wise Lipschitz
t
with constants L , L , L , and L , and the conditions in Lemma 3 hold. Define
U C D G
e := ∥Gˆ −G⋆∥ , ε := max (cid:8) εU,εSWA,εDSWA(cid:9) , L := L +L +L . (114)
t t t L2 t t t t U C D
Then, for every t ≥ 0, the following hold:
(i) Global-memory error bound. The global-memory branch satisfies
1−ρt
e ≤ ρte + sup ξ , (115)
t 0 i
1−ρ
1≤i≤t
with ξ defined in Eq. (103), and ρ < 1. In particular, define ξ¯:= sup ξ , we have
i i≥1 i
ξ¯
e ≤ as t → ∞. (116)
t
1−ρ
115

(ii) Long-horizon excess-risk bound. Define ε := limsup ε . Then, the hybrid predictor
t→∞ t
asymptotically satisfies
(cid:18)
L
ξ¯(cid:19)2
R (µˆ )−R⋆ ≤ Lε+ G as t → ∞. (117)
t t t 1−ρ
Proof of Theorem 4. We prove parts (i) and (ii) in sequence.
Part (i): global-memory error bound. Recall from Definition 6 that the exact and learned global-
memory states satisfy
G⋆ = F(G⋆ ;α⋆,β⋆,v⋆,k⋆), Gˆ = F(Gˆ ;αˆ ,βˆ,vˆ,kˆ ).
t t−1 t t t t t t−1 t t t t
Therefore, by the definition of e ,
t
e = ∥Gˆ −G⋆∥
t t t L2
(cid:13) (cid:13)
= (cid:13)F(Gˆ ;αˆ ,βˆ,vˆ,kˆ )−F(G⋆ ;α⋆,β⋆,v⋆,k⋆)(cid:13) . (118)
(cid:13) t−1 t t t t t−1 t t t t (cid:13)
L2
To separate the perturbation of the current update from the propagation of the previous memory
error, we add and subtract the intermediate term
F(Gˆ ;α⋆,β⋆,v⋆,k⋆)
t−1 t t t t
inside the norm. By the triangle inequality,
(cid:13) (cid:13)
e ≤ (cid:13)F(Gˆ ;αˆ ,βˆ,vˆ,kˆ )−F(Gˆ ;α⋆,β⋆,v⋆,k⋆)(cid:13)
t (cid:13) t−1 t t t t t−1 t t t t (cid:13)
L2
(cid:13) (cid:13)
+(cid:13)F(Gˆ ;α⋆,β⋆,v⋆,k⋆)−F(G⋆ ;α⋆,β⋆,v⋆,k⋆)(cid:13) . (119)
(cid:13) t−1 t t t t t−1 t t t t (cid:13)
L2
We now bound the two terms on the right-hand side separately.
For the first term, Lemma 4 gives the one-step perturbation bound
(cid:13) (cid:13)
(cid:13)F(Gˆ ;αˆ ,βˆ,vˆ,kˆ )−F(Gˆ ;α⋆,β⋆,v⋆,k⋆)(cid:13) ≤ ξ . (120)
(cid:13) t−1 t t t t t−1 t t t t (cid:13) t
L2
For the second term, applying the contraction property from Lemma 3 guarantees that
(cid:13) (cid:13)
(cid:13)F(Gˆ ;α⋆,β⋆,v⋆,k⋆)−F(G⋆ ;α⋆,β⋆,v⋆,k⋆)(cid:13) ≤ ρ ∥Gˆ −G⋆ ∥ = ρ e , (121)
(cid:13) t−1 t t t t t−1 t t t t (cid:13) t t−1 t−1 L2 t t−1
L2
where the contraction factor satisfies ρ < 1 for all t ≥ 1. We then suppose that ρ := sup ρ < 1.
t t≥1 t
Substituting Eq. (120) and Eq. (121) into Eq. (119), we obtain the one-step recursion
e ≤ ξ +ρe . (122)
t t t−1
We next unroll this recursion. Repeated application of Eq. (122) yields
e ≤ ξ +ρe
t t t−1
≤ ξ +ρξ +ρ2e
t t−1 t−2
t
(cid:88)
≤ ··· ≤ ρte + ρt−iξ . (123)
0 i
i=1
116

Since ξ ≤ sup ξ for every 1 ≤ i ≤ t, we further obtain
i 1≤j≤t j
t
(cid:16) (cid:17)(cid:88)
e ≤ ρte + sup ξ ρt−i
t 0 j
1≤j≤t
i=1
t−1
(cid:16) (cid:17) (cid:88)
= ρte + sup ξ ρm
0 j
1≤j≤t
m=0
1−ρt
= ρte + sup ξ , (124)
0 i
1−ρ
1≤i≤t
which proves Eq. (115). Now let
ξ¯:= supξ .
i
i≥1
Then Eq. (124) implies
1−ρt
e ≤ ρte + ξ¯. (125)
t 0
1−ρ
Since ρ < 1, we have ρt → 0 and (1−ρt)/(1−ρ) → 1/(1−ρ) as t → ∞. Hence
ξ¯
e ≤ as t → ∞, (126)
t
1−ρ
which proves the asymptotic statement in part (i).
Part (ii): long-horizon excess-risk bound. By Definition 5, the Bayes predictor has the form
µ⋆ = h (U⋆,C⋆,D⋆,G⋆),
t t t t t t
whereas the learned predictor is given by
µˆ = h (Uˆ ,Cˆ ,Dˆ ,Gˆ ).
t t t t t t
Since h is coordinate-wise Lipschitz, we have the pointwise estimate
t
|µˆ −µ⋆| ≤ L ∥Uˆ −U⋆∥+L ∥Cˆ −C⋆∥+L ∥Dˆ −D⋆∥+L ∥Gˆ −G⋆∥ . (127)
t t U t t C t t D t t G t t F
Taking L2 norms on both sides and applying Minkowski’s inequality yields
∥µˆ −µ⋆∥ ≤ L ∥Uˆ −U⋆∥ +L ∥Cˆ −C⋆∥ +L ∥Dˆ −D⋆∥ +L ∥Gˆ −G⋆∥
t t L2 U t t L2 C t t L2 D t t L2 G t t L2
= L εU +L εSWA+L εDSWA+L e . (128)
U t C t D t G t
By the definitions
ε = max
(cid:8) εU,εSWA,εDSWA(cid:9)
, L := L +L +L ,
t t t t U C D
the first three terms can be grouped as
L εU +L εSWA+L εDSWA ≤ (L +L +L )ε = Lε . (129)
U t C t D t U C D t t
Substituting Eq. (129) into Eq. (128), we obtain
∥µˆ −µ⋆∥ ≤ Lε +L e . (130)
t t L2 t G t
117

| Using the | asymptotic |     | estimate | from | part (i), | we further | obtain |     |     |     |     |     |
| --------- | ---------- | --- | -------- | ---- | --------- | ---------- | ------ | --- | --- | --- | --- | --- |
ξ¯
L G
|     |     |     |     | ∥µˆ −µ⋆∥ | ≤ Lε | +   |     | as t | → ∞. |     |     | (131) |
| --- | --- | --- | --- | -------- | ---- | --- | --- | ---- | ---- | --- | --- | ----- |
|     |     |     |     | t        | t L2 | t   |     |      |      |     |     |       |
1−ρ
| Finally,     | Lemma | 2 gives |      |               |            |       |             |      |     |     |     |     |
| ------------ | ----- | ------- | ---- | ------------- | ---------- | ----- | ----------- | ---- | --- | --- | --- | --- |
|              |       |         |      |               | R (µˆ )−R⋆ | = ∥µˆ | −µ⋆∥2       | .    |     |     |     |     |
|              |       |         |      |               | t t        | t     | t           | t L2 |     |     |     |     |
| Substituting | Eq.   | (131)   | into | this identity | yields     |       |             |      |     |     |     |     |
|              |       |         |      |               | (cid:18)   |       | ξ¯(cid:19)2 |      |     |     |     |     |
L
|              |     |        |     | )−R⋆    |       |     | G   | as  |        |     |     | (132) |
| ------------ | --- | ------ | --- | ------- | ----- | --- | --- | --- | ------ | --- | --- | ----- |
|              |     |        | R   | t (µˆ t | ≤ Lε+ |     |     |     | t → ∞, |     |     |       |
|              |     |        |     |         | t     | 1−ρ |     |     |        |     |     |       |
| which proves | Eq. | (117). |     |         |       |     |     |     |        |     |     |       |
Corollary 4 (Exact sufficiency in the realizable case). Suppose that the hypotheses of Theorem 4
hold. Assume further that the learned hybrid state exactly recovers the Bayes decomposition at every
time step, in the sense that εU = εSWA = εDSWA = 0, εα = εβ = εv = εk = 0 for all t, and that the
|     |     |     |     | t t | t   |     | t   | t   | t t |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
initial global-memory state is exactly aligned, e = 0. Then, for every t,
0
Gˆ
|     |     |     |     | =   | G⋆ and |     | µˆ = µ⋆ |     | a.s. |     |     | (133) |
| --- | --- | --- | --- | --- | ------ | --- | ------- | --- | ---- | --- | --- | ----- |
|     |     |     |     | t   | t      |     | t       | t   |      |     |     |       |
Consequently,
|     |     |     |     |     |     |             | R⋆. |     |     |     |     | (134) |
| --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | ----- |
|     |     |     |     |     | R   | t (µˆ t ) = |     |     |     |     |     |       |
t
|          |           | Under |     | conditions | in Corollary |     | 4, the | quantity | in  | Eq. (103) | satisfies |       |
| -------- | --------- | ----- | --- | ---------- | ------------ | --- | ------ | -------- | --- | --------- | --------- | ----- |
| Proof of | Corollary | 4.    |     |            |              |     |        |          | ξ   |           |           | ξ = 0 |
|          |           |       |     |            |              |     |        |          | t   |           |           | t     |
for all t. Since 0, the memory recursion Eq. (115) gives for all t. Substituting these
|            |         | e 0 =         |     |           |        |      |      | e   | t = 0 |     |     |     |
| ---------- | ------- | ------------- | --- | --------- | ------ | ---- | ---- | --- | ----- | --- | --- | --- |
| equalities | into    | Eq. (124)     | and | Eq. (130) | yields |      |      |     |       |     |     |     |
|            |         |               |     |           | ∥µˆ    | −µ⋆∥ | = 0, |     |       |     |     |     |
|            |         |               |     |           | t      | t L2 |      |     |       |     |     |     |
| By Lemma   | 2, this | is equivalent |     | to        |        |      |      |     |       |     |     |     |
)−R⋆
|     |     |     |     |     | R (µˆ |     | = 0. |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- | --- | --- |
|     |     |     |     |     | t     | t   | t    |     |     |     |     |     |
which implies µ⋆ almost surely. This proves both Eq. (133) and Eq. (134).
µˆ =
|     |     | t t |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Remark 8 (Interpretation of the bound). Theorem 4 shows that the long-horizon prediction error is
controlled by two quantities. The first is the aggregated non-global approximation term Lε, which
summarizes the quality of the shared, short-range, and mid-range branches. The second is the
global-memory term, whose asymptotic contribution is bounded by L ξ¯/(1−ρ), where ξ¯measures
G
the worst-case one-step perturbation and ρ < 1 ensures geometric damping of memory drift. In this
sense, a hybrid multi-scale temporal memory is approximately sufficient: once the Bayes predictor
factorizes across the four architectural roles, the remaining long-horizon degradation is fully accounted
for by branchwise approximation quality together with a contractively controlled accumulation of
| global-memory |      | perturbations. |               |     |        |                 |     |      |            |        |                |     |
| ------------- | ---- | -------------- | ------------- | --- | ------ | --------------- | --- | ---- | ---------- | ------ | -------------- | --- |
|               | (Why | the            | global-memory |     | branch | is nontrivial). |     |      |            |        |                |     |
| Remark        | 9    |                |               |     |        |                 |     | Only | the global | branch | can accumulate |     |
error across time. The contraction factor ρ < 1 turns this accumulation into a geometrically
discounted sum, preventing uncontrolled long-horizon drift. Without such a property, even small
one-step errors in the global memory could grow super-linearly and destroy long-horizon consistency.
118

|        | (Architectural | and experimental | relevance). |         |               |               |        |
| ------ | -------------- | ---------------- | ----------- | ------- | ------------- | ------------- | ------ |
| Remark | 10             |                  |             | Theorem | 4 establishes | architectural | suffi- |
ciency rather than providing a performance guarantee for any specific model checkpoint. It serves
to elucidate why the multi-scale temporal factorization is a principled design for long-horizon world
modeling. In the concrete architecture, the short- and mid-range approximation terms reflect the
representation quality of the SWA and DSWA pathways, whereas the discounted memory term char-
acterizes the stability of the GLA pathway. This theoretical mechanism strongly complements the
| empirical | long-horizon results | presented | in this work. |     |     |     |     |
| --------- | -------------------- | --------- | ------------- | --- | --- | --- | --- |
Remark 11 (Necessity–sufficiency template). Taken together, Theorem 3 and Theorem 4 provide
a compact necessity–sufficiency template for long-horizon world modeling: persistent memory is
necessary whenever the Bayes predictor is not recent-window measurable, and a hybrid multi-scale
temporal memory is approximately sufficient whenever the Bayes predictor admits the corresponding
| factorization | and the global | memory | evolves contractively. |     |     |     |     |
| ------------- | -------------- | ------ | ---------------------- | --- | --- | --- | --- |
119