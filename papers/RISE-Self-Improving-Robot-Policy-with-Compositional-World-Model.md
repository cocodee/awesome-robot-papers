RISE: Self-Improving Robot Policy with
Compositional World Model
Jiazhi Yang1,2∗† Kunyang Lin2∗ Jinwei Li2,6∗ Wencong Zhang2∗ Tianwei Lin5 Longyan Wu4
Zhizhong Su5 Hao Zhao6 Ya-Qin Zhang6 Li Chen3 Ping Luo3 Xiangyu Yue1♮ Hongyang Li3♮
1 The Chinese University of Hong Kong 2 Kinetix AI 3 The University of Hong Kong
4 Shanghai Innovation Institute 5 Horizon Robotics 6 Tsinghua University
∗Equal Contribution †Project lead ♮Equal Advising
https://opendrivelab.com/RISE
(a) Physical-World RL (b) Self-Improving via Imagination
Fail to grasp Succeed in grasping
-1.00
Launch Training
+0.75
A: -0.83 -0.76 A: +1.00
+0.94
Laborious
Reset &
Monitoring Dynamics Value Interacting with
World Model
Low Advantage High Advantage
Serial Execution
Time-consuming & Costly
Compositional World Model Online RL within Imaginary Space
(c) Real-World Evaluation Tasks
Success Rate Success Rate Success Rate
90 90 100
70 +35% 70 +45% 80 +35%
50 50 60
30 30 40
Recap KaOi0u-rRsL Recap Ours Recap Ours
Dynamic Brick Sorting Backpack Packing Box Closing
Fig.1:WepresentRISE,aframeworkforReinforcementlearningviaImaginationforSElf-improvingrobots.(a)Conventional
physical-world RL is bottlenecked by hardware cost, slow serial interaction, and the need for manual reset. (b) RISE shifts the
learning environment to a Compositional World Model, which first emulates future observations for proposed actions, then
evaluates imagined states to derive advantage for policy improvement. (c) Training on massive imaginative rollouts effectively
bootstraps RISE’s performance across a variety of complex, contact-rich tasks, surpassing prior art by a non-trivial margin.
Abstract—Despitethesustainedscalingonmodelcapacityand rollouts, estimates advantages, and updates the policy in imag-
dataacquisition,Vision–Language–Action(VLA)modelsremain inary space without costly physical interaction. Across three
brittle in contact-rich and dynamic manipulation tasks, where challenging real-world tasks, RISE yields significant improve-
minor execution deviations can compound into failures. While mentoverpriorart,withmorethan+35%absoluteperformance
reinforcement learning (RL) offers a principled path to robust- increase in dynamic brick sorting, +45% for backpack packing,
ness,on-policyRLinthephysicalworldisconstrainedbysafety and +35% for box closing, respectively.
risk, hardware cost, and environment reset. To bridge this gap,
wepresentRISE,ascalableframeworkofroboticreinforcement I. INTRODUCTION
learning via imagination. At its core is a Compositional World
Model that (i) predicts multi-view future via a controllable The trajectory of embodied intelligence has been reshaped
dynamics model, and (ii) evaluates imagined outcomes with a by the scaling of foundation models. Particularly, VLA mod-
progress value model, producing informative advantages for the
els have emerged as the dominant paradigm for generalist
policy improvement. Such compositional design allows state and
robot control, leveraging massive pre-training on web-scale
value to be tailored by best-suited yet distinct architectures and
objectives. These components are integrated into a closed-loop data to acquire broad semantic understanding and instruction-
self-improving pipeline that continuously generates imaginary followingcapabilities[9,7,8,46,22,76].Despitetheprogress
6202
rpA
82
]OR.sc[
2v57011.2062:viXra

on high-level semantic competence, such VLAs still fall short bility, which contributes to effective fine-tuning on targeted
of robust manipulation under complex physical dynamics, tasks. The value model is initialized from a pre-trained VLA
such as precise grasping of moving objects or effective bi- backbone [8] and adapted with both progress estimate [66,
manual coordination [65, 37]. This discrepancy highlights 92, 25] and Temporal-Difference learning [77] objectives,
the inherent limitation of Imitation Learning (IL), a core providing dense and failure-sensitive evaluation of imagined
mechanism enabling VLAs to generate executable actions. states.Thesecomponentsarecombinedtocomputeadvantages
Concretely,ILisinherentlylimitedbythequalityandcoverage for candidate actions, enabling stable policy improvement via
oftheexpertdemonstrationswhilesufferingfromtheexposure advantage-conditioned training. As a result, RISE performs
bias problem: once the robot drifts slightly off the expert’s on-policy reinforcement learning effectively in imagination.
manifold, it lacks the recovery skills to correct its course, As presented in Fig. 2, we rigorously evaluate RISE on a
leadingtocompoundingerrors[73,45,37,15].Reinforcement suite of real-world tasks that stress-test dynamic adaptation
Learning (RL), which improves agents through their own and precision. The results demonstrate that RISE outperforms
success and failure, offers a potential remedy. previous RL methods by a non-trivial margin, while avoiding
In virtual simulators such as LIBERO [60], agents can play costly real-world trial-and-error.
massive interactions in parallel, where both state and reward Our contributions are threefold: (1) We propose RISE, a
updates are controllable and accessible. Such properties of principled framework for robotic reinforcement learning, that
highly-crafted simulators have inspired successful RL adap- enablesautonomousself-improvementinascalableandonline
tations upon recent VLAs [63, 56, 61]. Nonetheless, such manner. RISE overcomes the physical restrictions posed by
controllability and parallelization do not hold in a real-world prior art by shifting the robotic interactions from physical en-
regime, where robot executions are serial, time-consuming, vironmenttoimaginativespace.(2)Atthecoreofthissystem
and labor-intensive due to manual monitoring and resets, isanonlinelearningenvironmentachievedbyaCompositional
as depicted in Fig. 1(a). These physical challenges largely WorldModelthatbuildsreliabledynamicsandvalueestimates
confine previous methods of real-world RL to offline data forreal-worldtasks.Weunveilcriticaldesignchoicestoderive
withheavydistributionshifttocurrentpolicy[85,64,65,80]. stable learning signals for policy improvement. (3) Through
Ultimately, the policy improvement could be bottlenecked extensiveexperimentsondexteroustasks,wedemonstratethat
without sufficient on-policy data stream [52, 90, 72]. RISE exhibits significantly higher performance compared to
The gap between the simulator and the physical world existing RL methods.
motivates the development of world models, which first learn We view our work as the first study on leveraging world
|              |            |          |                          |     | models as | an effective | learning environment | for challenging |     |
| ------------ | ---------- | -------- | ------------------------ | --- | --------- | ------------ | -------------------- | --------------- | --- |
| from passive | experience | and then | simulate future outcomes |     |           |              |                      |                 |     |
conditioned on different actions [78, 27, 29, 30, 31, 50]. real-world manipulation, bootstrapping performance on tasks
Nevertheless, constructing a world model applicable to real- requiring high dynamics, dexterity, and precision. Code is
world robotics poses fundamental challenges. For control, available at: https://github.com/OpenDriveLab/RISE.
| world models | must faithfully | follow | actions to represent | the |     |     |                 |     |     |
| ------------ | --------------- | ------ | -------------------- | --- | --- | --- | --------------- | --- | --- |
|              |                 |        |                      |     |     |     | II. PRELIMINARY |     |     |
accurateconsequences.Despitetheimprovedvisualrealismby
|             |               |            |                 |          | A. World | Model Formulation |     |     |     |
| ----------- | ------------- | ---------- | --------------- | -------- | -------- | ----------------- | --- | --- | --- |
| integrating | high-capacity | generative | models [87, 26, | 99], how |          |                   |     |     |     |
toimprovecontrollabilityovervariousactionsremainsanopen We aim to construct a world model consisting of a dy-
problem [55]. Furthermore, learning from imagination neces- namics model for predicting future states and a value model
sitates informative learning signals for intermediate actions, for predicting rewards over different courses of action. Cru-
rather than relying solely on a binary indicator. Otherwise, cially, these predicted rewards are converted into advantages
determiningterminalsuccesswouldrequiretheworldmodelto to guide RL training. Formally, let o = [m1,...,mn]
|     |     |     |     |     |     |     |     | t t | t   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
simulatetheentiretaskexecution,whichisbeyondthereliable be the multi-view observation at time t with n camera
horizon of most generative world models [55, 57]. views. We apply a history window of length N as O t =
To handle these issues, we present RISE, a holistic learn- {o ,...,o ,o } to capture temporal dependency. The
|     |     |     |     |     | t−N | t−1 t |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
ing framework that Reinforces robot foundation model via conditional action a is drawn from a running policy π
t
Imagination to enable SElf-improving, as shown in Fig. 1(b). as a = [a ,a ,...,a ] ∼ π(·|o ,ℓ), where a is
|     |     |     |     |     | t   | t t+1 | t+H−1 | t   | t   |
| --- | --- | --- | --- | --- | --- | ----- | ----- | --- | --- |
At its core is an online learning environment achieved by a commonlyappliedasasequenceofactionswithchunklength
learned world model. Inspired by prior works that decompose H,i.e.,actionchunk,andℓisalanguageinstructiondescribing
world modeling into tractable sub-problems to flexibly lever- the task. The dynamics model D predicts future observations
age heterogeneous architectures and priors [5, 20, 97, 86], {oˆ ,...,oˆ } conditioned on both the historical context
|     |     |     |     |     | t+1 | t+H |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
we build a Compositional World Model that factorizes the and the proposed action sequence:
| simulation | problem into | two objectives, | dynamics prediction |      |     |            |      |       |     |
| ---------- | ------------ | --------------- | ------------------- | ---- | --- | ---------- | ---- | ----- | --- |
|            |              |                 |                     |      |     | oˆ ,...,oˆ | =D(O | ,a ). | (1) |
|            |              |                 |                     |      |     | t+1        | t+H  | t t   |     |
| and value  | estimation,  | allowing each   | to be instantiated  | with |     |            |      |       |     |
architectures and training objectives best suited to its role. To evaluate the utility of imagined trajectories, we further
Builtonanefficientvideodiffusionmodel[59,28],wepre- introduce a value model V, which assigns a progress signal
train our dynamics model on large-scale robot datasets with towards successful completion conditioned on observation
a Task-centric Batching strategy to improve action controlla- and task instruction as V(oˆ,ℓ). We define the advantage as
t

(a) Dynamic Brick Sorting Pick and Sort Bricks on Running Conveyor
(b) Backpack Packing Put Clothes into Backpack Lift Zip
(c) Box Closing Place Cup Fold Flap Tuck Tab
Fig. 2: Evaluation task suite of RISE. Left: Tabletop setting. Right: Zoomed-in details of each task procedure. Dynamic
Brick Sorting involves precisely picking up colored bricks from a moving conveyor and placing them into the corresponding
color-designated bins. Backpack Packing requires the robot to open, insert clothes, lift, and zip the backpack. Box Closing
necessitates subtle controls to fold the flap and tuck the tab into the box precisely.
the average cumulative improvement across the entire chunk. Sinceimprovementisfullydeterminedbytheadvantagevalue,
Specifically, we compute the difference between the value of we have p(I|Aπref) ≡ p(I|a
t
,o
t
,ℓ). Applying Bayes’ rule
eachpredictedfutureobservationoˆ andtheinitialobserva- allows us to express the improvement likelihood as a density
t+k
tion o as the reward of action a , then take the expectation ratio:
t t+k
over the horizon of the action chunk as the advantage: π (a |I,o ,ℓ)p(I|o ,ℓ)
p(I |a ,o ,ℓ)∝ ref t t t . (4)
(cid:32) H (cid:33) t t π (a |o ,ℓ)
1 (cid:88) ref t t
A(o ,a ,ℓ)= V(oˆ ,ℓ) −V(o ,ℓ), (2)
t t H t+k t Substituting Eq. (4) into the target distribution and setting
k=1
β = 1 cancels the unconditional prior π , yielding the sim-
ref
where A is associated with the action chunk proposed by the
plified objective πˆ(a |o ,ℓ) = π (a | I,o ,ℓ). Practically,
t t ref t t
policy π, forming the learning signal for policy optimization.
we implement this by conditioning the policy on discretized
TheinteractionbetweenDandV occursinimaginationspace,
advantages,guidinggenerationtowardhigh-returntrajectories.
and both modules are compatible with multi-view images.
III. METHODOLOGY
B. Reinforcement Learning
Our approach is structured as follows: In Sec. III-A, we
We formulate the problem as a standard RL setting with
propose a Compositional World Model that composes dynam-
decision-makingprocessasaMarkovDecisionProcess(MDP)
ics prediction with value estimation, providing an interactive
characterized by the tuple (O,ℓ,A,H,r). At each timestep t,
environment with informative learning signals. In Sec. III-B,
given an observation o ∈O and task instruction ℓ, the policy
t
weestablishaPolicyWarm-upstageonreal-worldexperience
πgeneratesanactionsequencea ∈AH ofhorizonH,obtain-
t
to anchor the policy to practical behavioral distribution and
ingrewardr foreachstep.Theinteractionbetweenthepolicy
equipitwithadvantage-conditionedcapabilities.InSec.III-C,
and the environment induces a trajectory distribution ρ (τ),
π
we present a Self-Improving Loop that iteratively generates
whereτ =(o ,a ,...,o )∈O×A···O.Theobjectiveisto
0 0 T
maximizetheexpectedreturnJ(π)=E [ (cid:80)T r(o ,a )]. imaginary rollouts and optimizes the policy within the world
τ∼ρπ t=0 t t model. Implementation details with compute allocation are
To quantify the quality of a specific action sequence relative
covered in Sec. III-D.
to the average policy performance, we utilize the advantage
function Aπ(o t ,a t ,ℓ), estimated via Eq. (2). A. Compositional World Model
To ensure stable improvement over a reference policy π ,
ref Scalable RL necessitates precise environment modeling to
we adopt the probabilistic inference framework from π∗ [2].
0.6 map current states and policy actions to future dynamics and
Rather than maximizing a regularized objective directly, we
rewards. To this end, we introduce a Compositional World
construct a target distribution πˆ by weighting π with the
ref Model to disentangle dynamics prediction from value estima-
probability of improvement I:
tion, thereby enabling independent architectural optimization
πˆ(a
t
|o
t
,ℓ)∝π
ref
(a
t
|o
t
,ℓ)·p(I |Aπref(o
t
,a
t
,ℓ))β. (3) for each component. Starting from a context observation, the

|     | Initial State |     |     | Future #1 |     | Future #2 |     |              |        |     |                        |             |     |     |     |
| --- | ------------- | --- | --- | --------- | --- | --------- | --- | ------------ | ------ | --- | ---------------------- | ----------- | --- | --- | --- |
|     |               |     |     |           |     |           |     | Task-Centric |        |     |                        | Progress +  |     |     |     |
|     |               |     |     |           |     |           |     |  Batching    |        |     |                        | TD Learning |     |     |     |
|     |               |     |     | Future #3 |     | Future #4 |     |              |        |     |                        |             |     |     |     |
|     |               |     |     |           |     |           |     |              | Genie  |     | Success + Failure Data |             |     |     |     |
�
|     |     |     |     |     |     |     |     |     | Envisioner |     |     |     |     |     | �.� |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
(a) Diverse Future Imagination
Case #1  Zipper Over-pulling
Dynamics Model
Value Model
|     |     |     |     |     |     |     |     |     |     |     | Multiview Predictions |     | Reward |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | ------ | --- | --- |
for � steps
Case #2  Backpack Lifting Failure
Policy
|     |     |     |     |     |     |     |     | Multiview Images |     |     |     |     |     | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
Optimization
|     |     |     |     |     |     |     |     | Action Chunk |     |     |     |     |     |     | Step |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | ---- |
(b) Failure Case Simulation Fig. 4: Workflow of compositional world model. Top:
Ground Truth Training recipe upon proper model initialization. Bottom:
   Inference pipeline that yields rewarded samples for policy
|     |     |     |     |     |     |     |     | optimization. | Both    | modules     | are | compatible |        | with multi-view |       |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ------- | ----------- | --- | ---------- | ------ | --------------- | ----- |
|     |     |     |     |     |     |     |     | images.       | We omit | text prompt |     | for both   | policy | and value       | model |
Model Prediction
|     |     |     |     |     |     |     |     | for brevity. |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
(c) High-Fidelity Generation
modelonlarge-scaleaction-labeleddatasets,includingAgibot
| Fig.3: QualitativeimaginationsproducedbyRISE. |     |         |     |           |        |         | Given |            |     |         |       |                  |     |     |            |
| --------------------------------------------- | --- | ------- | --- | --------- | ------ | ------- | ----- | ---------- | --- | ------- | ----- | ---------------- | --- | --- | ---------- |
|                                               |     |         |     |           |        |         |       | World [11] | and | Galaxea | [43], | by incorporating |     | an  | additional |
| initial multi-view                            |     | context | and | candidate | action | chunks, | RISE  |            |     |         |       |                  |     |     |            |
can (a) emulate a variety of future accordingly, (b) simulate light-weight action encoder. Additionally, we impose stronger
|               |      |               |     |        |        |     |           | noise on | context | frames | compared | to  | the original |     | GE-base |
| ------------- | ---- | ------------- | --- | ------ | ------ | --- | --------- | -------- | ------- | ------ | -------- | --- | ------------ | --- | ------- |
| failure cases | with | corresponding |     | reward | drops, | and | (c) main- |          |         |        |          |     |              |     |         |
tain coherent predictions consistent with real executions. training, to improve the generation robustness when encoun-
|     |     |     |     |     |     |     |     | tering motion  |     | blurs and   | visual | artifacts           | that | might       | occur in |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ----------- | ------ | ------------------- | ---- | ----------- | -------- |
|     |     |     |     |     |     |     |     | both recorded  | and | synthesized |        | data. Nevertheless, |      | fine-tuning |          |
|     |     |     |     |     |     |     |     | a controllable |     | world model | on     | heterogeneous       |      | action      | data is  |
dynamicsmodelemulatesafaithfulfutureunderthecandidate
|               |              |       |            |           |              |           |         | prone to          | instability | and        | slow     | convergence | when | diverse | tasks     |
| ------------- | ------------ | ----- | ---------- | --------- | ------------ | --------- | ------- | ----------------- | ----------- | ---------- | -------- | ----------- | ---- | ------- | --------- |
| action chunk, | which        | would | be         | evaluated | by           | the value | model   |                   |             |            |          |             |      |         |           |
|               |              |       |            |           |              |           |         | and visual        | domains     | are        | included | within      | the  | same    | batch for |
| to derive     | an advantage |       | for policy |           | improvement. |           | We show |                   |             |            |          |             |      |         |           |
|               |              |       |            |           |              |           |         | each optimization |             | iteration. |          | We mitigate | this | issue   | with a    |
samples from imagination in Fig. 3 qualitatively. Crucially, Task-Centric Batching strategy, where each batch is sampled
| the model          | is employed |          | exclusively | during     | training, |          | imposing |             |                |            |       |           |          |              |         |
| ------------------ | ----------- | -------- | ----------- | ---------- | --------- | -------- | -------- | ----------- | -------------- | ---------- | ----- | --------- | -------- | ------------ | ------- |
|                    |             |          |             |            |           |          |          | from a      | small fraction | of         | tasks | while     | covering | more         | samples |
| zero computational |             | overhead | at          | inference. | The       | training | recipe   |             |                |            |       |           |          |              |         |
|                    |             |          |             |            |           |          |          | of the same | task           | correlated | with  | different | actions. | Intuitively, |         |
andinferencepipelineofourworldmodelareshowninFig.4. this batching strategy prioritizes action diversity under the
Controllable Dynamics Model. Reliably simulating future samesceneoverscenariodiversityforbatchoptimization,thus
states for RL yields two fundamental requirements: (i) The contributing to improved action controllability. Empirically,
| generation | latency | should | not | be prohibitively |     | high, | which |          |               |          |     |      |               |             |     |
| ---------- | ------- | ------ | --- | ---------------- | --- | ----- | ----- | -------- | ------------- | -------- | --- | ---- | ------------- | ----------- | --- |
|            |         |        |     |                  |     |       |       | applying | this strategy | improves |     | both | task-specific | fine-tuning |     |
would bottleneck the throughput of the RL system. (ii) The efficiency, as in Table V, and stronger policy improvement,
generatedstatesshouldnotonlybeplausibleinvisualsbutalso as in Table IV. With these design choices, our dynamics
consistent with the conditional actions. Thereby, we initialize modeliscapableofprovidingfastandfaithfulmulti-viewstate
our dynamics model from pre-trained Genie Envisioner [59], prediction to support the self-improving loop.
i.e.,GE-basevariant,whichinheritsthearchitecturaladvances
|     |     |     |     |     |     |     |     | Progress | Value | Model. | Imagination-based |     |     | policy | improve- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ------ | ----------------- | --- | --- | ------ | -------- |
in LTX-Video [28] and features a favorable trade-off between ment critically depends on a reward-related signal that is (i)
| generation | quality | and | inference | speed. | In  | comparison, | ad- |     |     |     |     |     |     |     |     |
| ---------- | ------- | --- | --------- | ------ | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
denseoverlonghorizonsand(ii)sensitivetosubtlefailuresin
vanced world models such as Cosmos [1] takes more than 10 contact-richmanipulation.Wethereforelearnavalueestimator
minutes for synthesizing 25 multi-view observations, whereas V that maps sensory observations to a scalar value used
| GE only | requires | less | than | 2 seconds | to  | achieve | such | a        |          |           |     |                  |     |      |        |
| ------- | -------- | ---- | ---- | --------- | --- | ------- | ---- | -------- | -------- | --------- | --- | ---------------- | --- | ---- | ------ |
|         |          |      |      |           |     |         |      | to score | imagined | rollouts. | V   | is parameterized |     | from | a pre- |
horizon, leading to 300x speedup. Such generation efficiency trained VLA policy π [8], that brings in two advantages.
0.5
| is a critical | pillar | for applicable |     | RL training. |     |     |     |              |     |              |     |       |                |     |          |
| ------------- | ------ | -------------- | --- | ------------ | --- | --- | --- | ------------ | --- | ------------ | --- | ----- | -------------- | --- | -------- |
|               |        |                |     |              |     |     |     | First, π 0.5 | has | been trained | on  | broad | robot datasets |     | and thus |
Despite its efficiency, GE-Base is originally conditioned carries robot-centric understanding that transfers naturally to
on text rather than fine-grained robot actions. To endow the value estimation. Second, the policy backbone is compatible
model with precise action controllability that could be further with multi-view inputs, whereas generic VLMs are mostly
transferredintotask-specificscenarios,wefurtheroptimizethe developed on single-view images without such adaptation.

| As          | for training, | we         | warm-start  |           | V with      | a simple  | temporal |           |           |         |     |           |                       |     |
| ----------- | ------------- | ---------- | ----------- | --------- | ----------- | --------- | -------- | --------- | --------- | ------- | --- | --------- | --------------------- | --- |
| p r o gr es | s e s t i     | m a te a s | o b j e c t | ive , w h | i c h e q u | ip s ou r | v a lu e | m o d e l | P r o m p | t e d   |     |           |                       |     |
|             |               |            |             |           |             |           |          |           |           |         |     | Action a� | E v a l u a t e d  �� |     |
w i th a c o a r s e u n de r st a n d i n g o f m o n o to n i c t em p or a l st ru ct u r e . A d v an t a g e A d v a n t a g e
|       |           |      |             |              |                  |     |         |     |             | >>>                                | VLA >>> | >>>         | >>>                          |     |
| ----- | --------- | ---- | ----------- | ------------ | ---------------- | --- | ------- | --- | ----------- | ---------------------------------- | ------- | ----------- | ---------------------------- | --- |
|       |           |      |             |              |                  |     |         |     | Observation |  � �                               |         |             |                              |     |
|       |           |      |             |              |                  |     |         |     |             |                                    |         | C om p o s  | it io n a l Observation ��+� |     |
|       | L         | =E   |             | (cid:2) (V(o | ,ℓ)−t/T)2(cid:3) |     | ,       | (5) |             |                                    |         |             |                              |     |
|       |           | prog | (ot,ℓ)∼Dexp |              | t                |     |         |     |             |                                    |         | W or ld   M | o d e l                      |     |
|       |           |      |             |              |                  |     |         |     |             | N e xt rollout with generated obs. |         |             |                              |     |
| where | t indexes | the  | current     | timestep     | within           | an  | episode | of  | Parallel    |                                    |         |             |                              |     |
Rollout
| length | T. While | progress | regression |     | provides | a   | dense | signal, |     |     |     |     |     |     |
| ------ | -------- | -------- | ---------- | --- | -------- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- |
it is often overly smooth and can be insensitive to failures, Training
especiallyincontact-richsettingswhereexecutionerrorsmight (��,a�,��
besubtleinvisuals.Toconquerthis,weaugmenttheprogress Action a� MSE Loss Action a�  E v a l u a t e d  �� )
|     |     |     |     |     |     |     |     |     |     |     | >>> | >>> A d v | a n t a g e >>> |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --------------- | --- |
losswithTemporal-Difference(TD)learning[77],whichuses       VLA
Observation ��
bothsuccessfuldemonstrationsandfailurerolloutstoestablish Buffer
| a value | function | that | distinguishes |     | success | from | errors. |     |     |     |     |     |     |     |
| ------- | -------- | ---- | ------------- | --- | ------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
=E (cid:2) )2(cid:3) Fig. 5: Self-improving loop of RISE. Our learning pipeline
|     | L   |     |     |     | (V(o ,ℓ)−y |     | ,   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TD (ot,ℓ,ot+1)∼D t t (6) encompassestwostages.Top:Rolloutstage.Promptedwithan
y =r +γV(o ,ℓ), optimal advantage, the rollout policy interacts with the world
|       |          | t t      |          | t+1 |         |         |        |         |          |         |               |         |                 |     |
| ----- | -------- | -------- | -------- | --- | ------- | ------- | ------ | ------- | -------- | ------- | ------------- | ------- | --------------- | --- |
|       |          |          |          |     |         |         |        |         | model to | produce | rollout data. | Bottom: | Training stage. | The |
| where | γ is the | temporal | discount |     | factor, | and r t | is set | to 0 in |          |         |               |         |                 |     |
behaviorpolicyisthentrainedtogenerateproperactionunder
intermediatestepswhilebeing+1/−1attheendofsuccessful
and failure episodes, respectively. Our final value learning an advantage-conditioning scheme.
| objective   | simply | combines |          | both      | terms | L =       | L +         | L   |     |     |     |     |     |     |
| ----------- | ------ | -------- | -------- | --------- | ----- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
|             |        |          |          |           |       | V         | prog        | TD  |     |     |     |     |     |     |
| to leverage |        | both the | learning | stability |       | and error | sensitivity |     |     |     |     |     |     |     |
provided by two terms, respectively. additionally prompt the rollout policy π rollout with an optimal
|           |         |     |            |     |            |     |     |     | advantage | 1, to infer | an action | with positive | intent. |     |
| --------- | ------- | --- | ---------- | --- | ---------- | --- | --- | --- | --------- | ----------- | --------- | ------------- | ------- | --- |
| B. Policy | Warm-up | on  | Real-world |     | Experience |     |     |     |           |             |           |               |         |     |
(1,o
Before performing the on-policy improvement, we first aˆ =π ,ℓ). (7)
|            |     |          |         |     |                        |     |     |       |     |     | t   | rollout t |     |     |
| ---------- | --- | -------- | ------- | --- | ---------------------- | --- | --- | ----- | --- | --- | --- | --------- | --- | --- |
| warm-start | the | learning | process |     | with offline-collected |     |     | data, |     |     |     |           |     |     |
which anchors the policy to a physically plausible behavior Visual history and action proposal are fed into the dynamics
distribution on the targeted task, avoiding careless exploration model to synthesize the next H visual states. These imagined
inthelaterstage.Bothdatacompositionandtrainingobjective states are then evaluated by the value model to compute
mainly follow RECAP [2]. For each task, we fine-tune the the actual advantage of the proposed action, denoted as
pre-trained policy, i.e., π [8], on offline collected data, Aπrollout(o ,aˆ ,ℓ). We define 1 as the prompted advantage for
|     |     |     | 0.5 |     |     |     |     |     | t   | t   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
comprising expert demonstrations, policy rollout with success inferringoptimalactions,whereasAπrollout(o ,aˆ ,ℓ)denotesthe
t t
andfailure,andhuman-intervenedcorrection.Duringtraining, evaluatedadvantage,reflectingthetrueutilityofthegenerated
the policy is conditioned on an advantage signal, labeled by action. This advantage is discretized into one of N uniform
our learned value model V as in Eq. (2), by treating oˆ as bins representing the practical advantage of the action in
t+k
laterframesfromanofflinerecordedvideo.Differentfromthe the current state. To broaden the state coverage during the
practice in RECAP that labels advantage for offline data and online training process, imagined states would also serve as
policy rollout, in early experiments, we found that assigning input for the subsequent rollout. From each offline state, such
advantages for both sources yields worse results than labeling consecutiveinteractionwouldbeconductedatmosttwotimes,
for rollout only. Thereby, only rollout data is assigned the considering the known error accumulation issue of generative
learnedadvantageswhereasbothexpertandhumancorrection video models [38]. The rollout policy parameters are updated
data are directly paired with optimal advantages, denoted as via an Exponential Moving Average (EMA) [40], blended
1, in our experiments. Consequently, this warm-up stage em- from behavior policy weights. One major difference between
| powers | the policy | to  | absorb | action | data in | different | qualities, |     |          |                  |     |                    |             |     |
| ------ | ---------- | --- | ------ | ------ | ------- | --------- | ---------- | --- | -------- | ---------------- | --- | ------------------ | ----------- | --- |
|        |            |     |        |        |         |           |            |     | RISE and | prior approaches |     | that also leverage | world model | as  |
whichiscriticalforthenextself-improvementstagethatlearns learningenvironment[44,93,13]isthatRISEavoidsexplicitly
from trial-and-error in an online manner. simulating terminal states to obtain rewards, yet produces
|         |           |      |       |       |     |     |     |     | chunk-wise | advantage | for proposed  | actions | directly.     |      |
| ------- | --------- | ---- | ----- | ----- | --- | --- | --- | --- | ---------- | --------- | ------------- | ------- | ------------- | ---- |
| C. Self | Improving | with | World | Model |     |     |     |     |            |           |               |         |               |      |
|         |           |      |       |       |     |     |     |     | Training   | Stage.    | The on-policy | rollout | data ⟨o,aˆ,A⟩ | form |
With the advantage conditioning capability acquired from batch samples to optimize the policy. The VLA is trained to
the warm-up stage on offline data, we then apply the com- minimize the distance between its output and the proposed
positional world model as an interactive simulator to improve actionaˆ,giventheevaluatedadvantageAasacondition.This
thepolicy.Theself-improvingloopexecutestheRolloutstage allows the policy to learn from both high-advantage successes
and Training stage iteratively, as shown in Fig. 5. and low-advantage failures discovered in imagination. To
Rollout Stage. To start off, we sample an initial state from preventcatastrophicforgettingduringexploration,wealsomix
the warm-up offline dataset. Along with the observation, we offlinelabeleddataintothebatchdata.Bothofflineandonline

TABLE I: Performance comparisons on real-world tasks. We evaluate success rates and scores across three diverse tasks,
ranging from dynamic sorting to precise packing. RISE exhibits superior performance compared to baselines in all scenarios.
Dynamic Brick Sorting Backpack Packing Box Closing
Method
Succ. (%) Score Succ. (%) Score Succ. (%) Score
π [8] 35.00 8.28 30.00 4.25 35.00 7.50
0.5
π +DAgger [73, 45] 15.00 6.10 50.00 7.00 40.00 7.50
0.5
π +PPO [75] 10.00 7.68 35.00 5.88 10.00 4.75
0.5
π +DSRL [80] 10.00 6.65 10.00 3.50 10.00 7.63
0.5
RECAP [2] 50.00 9.00 40.00 6.13 60.00 8.13
RISE (Ours) 85.00 9.78 85.00 9.50 95.00 9.88
experiences are leveraged under unified learning objective: A. Real-world Experimental Setup
π(Aπrollout(o,aˆ
t
,ℓ),o
t
,ℓ)→aˆ. (8) Our real-world experiments employ a dual 7-DoF AgileX
robot with absolute joint control. We benchmark three dexter-
whichisoptimizedundergenericflow-matchingcriteria[7,8]. ous, long-horizon tasks, including: Dynamic Brick Sorting:
The robot is required to sort diverse bricks dynamically on an
D. Implementation Details operating conveyor belt, shown in Fig. 2(a), Backpack Pack-
ing: This task presents challenges involving compliant and
World Model Training. The dynamics model goes through
deformable object manipulation as in Fig. 2(b). Box Closing
twophases.Thepre-trainingstageonGalaxea[43]andAgibot
The task requires precise bi-manual coordination to package
World [11] is conducted on 16 NVIDIA H100 GPUs with
a cup, as in Fig. 2(c). Notably, ablations are conducted on the
a global batch size of 512, taking about seven days. Subse-
mostchallengingtaskinpractice,i.e.,DynamicBrickSorting.
quently, for task-specific fine-tuning, we utilize 8 NVIDIA
Hyperparameters remain fixed across variants. Detailed robot
H100 GPUs with a global batch size of 64, which takes
setup and evaluation metrics are included in the Appendix.
aboutthreedaystocomplete.Parameterizedfromapre-trained
VLA[8],thevaluemodelisdirectlyfine-tunedontask-specific
B. Main Results
data, thanks to the robot-centric knowledge inherited from
the policy backbone. We apply progress estimate loss only Baselines. We benchmark RISE against state-of-the-art imita-
for the first 10k training steps and include TD learning loss tion and reinforcement learning baselines. Each counterpart is
additionally for the remaining 40k steps. With a total batch developed with a close compute budget. Implementation and
size of 64 on 8 GPUs, the model converges in about one day datacompositionforeachvariantaredetailedintheAppendix.
of training. Importantly, both modules of our world model are
• π 0.5 [8]:Astate-of-the-artVLApre-trainedonweb-scale
onlyappliedduringthepolicylearningphase,thusposingzero
multi-robot data and fine-tuned on task demonstrations.
inference overhead during real-world policy execution.
• π 0.5 + DAgger [73, 45]: An interactive baseline utilizing
Policy Training. The policy warm-up phase largely follows
on-policy human corrections to mitigate exposure bias.
the training procedure of RECAP [2] on an offline collected
• π 0.5 + PPO [75]: A standard online RL baseline fine-
dataset, where the policy is conditioned on advantage labeled
tuning VLA weights via PPO.
by our learned value model. The following self-improving
• π 0.5 + DSRL [80]: A sample-efficient method steering
stagethengoesaround10ksteps.Forbothstages,globalbatch
frozenVLAsbyoptimizingdiffusionlatentnoiseviaRL.
size is 64 on 8 GPUs.
• RECAP [2]: An advantage-conditioned offline RL ap-
Task-specific Data. Both our world model and policy share
proach [23, 48] originally built off a proprietary pre-
the same set of offline data for each task, including expert
trained policy, i.e., π [2]. Due to the inaccessibility
0.6
demonstrations and policy rollouts with success and failure,
of π , we apply this approach to π upon the same
0.6 0.5
exceptthatpolicylearningalsoconsumesafractionofDAgger
parameter-tuning and offline data corpora as ours.
data to enrich the recovery mode, similar to RECAP [2].
Results. We present quantitative results in Table I, reporting
bothSuccessRateandStage-wiseScore,withevaluationcrite-
IV. EVALUATIONS
riaprovidedintheAppendix.Althoughπ offerspreliminary
0.5
We conduct a comprehensive evaluation to investigate the capability,weobservethatonlineadaptation(PPO,DSRL)in-
capabilities of RISE. In particular, we focus on the following curs severe instability. This leads to performance degradation,
questions: Comparative Analysis: Does RISE outperform e.g., a sharp drop (35%→ 10%) in the Dynamic Brick Sorting
existing mainstream RL and IL methods, particularly in real- task. RECAP validates the benefit of advantage conditioning
world dexterous and long-horizon tasks? Design Choices: but falls short of RISE. Notably, our method yields a 40%
How can the world model be effectively integrated into the margininBackpackPacking,whileincreasingsuccessratesto
RL loop, and is each module design essential? 85%and95%onthebrickandboxtasks,respectively.Overall,

TABLE II: Ablation on offline data ratio. Overall perfor-
mance peaks at 0.6, indicating that balanced offline data is
crucial for complex generalization.
Pick&Place Sort Complete
Ratio
Succ. (%) Acc. (%) Succ. (%) Score
0.1 15.00 83.33 5.00 1.35
0.3 78.75 80.95 25.00 7.03
0.6 90.00 87.50 50.00 8.32
0.9 90.00 80.56 30.00 7.90
TABLEIII: Ablationononlineactionandstateintegration.
Resultsdemonstratethenecessityofincorporatingbothonline
action proposed by the rollout policy and the online state
generated by the dynamics model.
Pick&Place Sort Complete OnlineAction OnlineState
Succ.(%) Acc.(%) Succ.(%) Score
(cid:37) (cid:37) 80.00 76.56 35.00 6.98
(cid:33) (cid:37) 96.25 84.42 40.00 8.73
(cid:33) (cid:33) 98.75 92.41 70.00 9.43
TABLEIV: Ablationsonthemodulardesignsofdynamics
and value models. “w/o Progress” indicates that the value
model is trained without the auxiliary progress loss. Our full
architecture proves to be the most effective across all metrics.
Pick&Place Sort Complete
ModuleVariants
Succ.(%) Acc.(%) Succ.(%) Score
w/oPre-train 97.50 60.26 15.00 7.43
Dynamics
w/oTask-Centric 93.75 89.33 40.00 8.78
w/oProgress 95.00 86.84 50.00 8.78
Value
w/oTDLearning 98.75 72.15 35.00 8.38
RISE(Ours) w/alldesigns 98.75 92.41 70.00 9.43
RISEsignificantlyoutperformsallRLandILbaselinesacross
all tasks, with consistently high success rate.
C. Ablation Study
What ratio of the offline data should be allocated during
RL training?Relyingsolelyononlineexperienceoftenleads
to performance collapse due to the distribution shift between
offlinedemonstrationsandonlinerollouts.Toaddressthis,we
investigate the optimal mixing ratio of offline data to retain
performance.AsshowninTableII,weobserveadistincttrade-
off. When the offline data ratio is too low (e.g., 0.1), the suc-
cess rate plummets to 5%. This confirms our hypothesis that
insufficient offline retention leads to catastrophic forgetting
in the face of massive online data. Conversely, an excessive
ratio(e.g.,0.9)alsodegradesperformance.Weattributethisto
over-regularization, where the policy becomes too constrained
to the offline distribution, hindering its ability to explore and
discover superior policies.
Can VLA models benefit from world-model generated
online actions or states? To validate this, we evaluate three
variants: a baseline without online signals, one with online
GT
RISE
(Ours)
Cosmos
GE
ACTION INCONSISTENCY
ACTION INCONSISTENCY
DISTORTED
DISTORTED BLURRED ACTION INCONSISTENCY
Fig. 6: Qualitative Comparison on Dynamics Models. Cos-
mos [1] and Genie Envisioner [59] suffer from geometric dis-
tortion, motion blurring, and physical inconsistency, whereas
our method showcases temporally coherent and physically
consistent results with Ground Truth (GT).
TABLE V: Quantitative comparison of dynamics models.
↑ (↓) denotes higher (lower) is better. Our method shows
superior motion accuracy (EPE) and perceptual quality across
both real-world tasks in Fig. 2 and the Bridge dataset [81].
Method PSNR↑ LPIPS↓ SSIM↑ FVD↓ EPE↓
Experiment#1:Fine-tuningonourrealworldtasks
Cosmos 21.17 0.14 0.79 97.90 1.21
GE 21.16 0.11 0.79 85.72 1.05
RISE(w/oTask-Centric) 22.67 0.08 0.80 61.22 0.68
RISE(Ours) 23.90 0.07 0.82 66.84 0.54
Experiment#2:Fine-tuningonBridgedataset[81]
Cosmos 21.32 0.14 0.80 73.21 1.18
GE 21.47 0.12 0.79 64.55 0.96
RISE(w/oTask-Centric) 22.61 0.10 0.78 49.07 0.72
RISE(Ours) 23.68 0.10 0.82 45.21 0.64
actions only, and the full RISE with both. Our results con-
firm the necessity of online signals. As shown in Table III,
introducing online actions increases the success rate from
35% to 40%. We attribute this improvement to the expanded
action space exploration; unlike the static behavioral mode
typically found in offline data, online rollouts allow the VLA
to distinguish between high-advantage actions and suboptimal
failures.Crucially,incorporatingonlinestatesfurtherraisesthe
successrateto70%.Thissuggeststhatdynamicallygenerated
onlinestatesprovidearicher,virtuallyunboundedtrainingdis-
tribution, overcoming the limitations of fixed offline datasets.
How significant is the impact of the modules on RISE?
Quantitative results in Table IV highlight the criticality of
eachcomponent.Inthedynamicsmodel,removingvisualpre-
training drops sorting accuracy by 32.15% and completion

to 15%, underscoring the need for visual priors. Absence of nipulation. A large body of work adapts VLA post-training
task-centricdesignreducescompletionby30%,validatingthe with RL within simulated environments [60, 69, 16, 67],
filteringofdistractions.Forthevaluemodel,ablatingprogress whereinteractionsarecheap,resettable,andparallelizable[63,
regression lowers success by 20%, confirming the importance 56, 14, 61, 17]. However, such scalability does not hold
of dense signals. Furthermore, omitting TD learning leads to in the physical world, where interactions are serial, slow,
a 35% decline, demonstrating its role in robust estimation. and labor-intensive. Thereby, prior work on real-world RL is
Howreliableisthedynamicsmodel?WecompareRISEwith constrainedtoheavilyreuseoff-policydatawhileonlineinter-
Cosmos [1] and Genie Envisioner (GE) [59] to investigate actions are performed on limited robot hardware only, which
the reliability. We evaluate generation quality using PSNR, potentially bottlenecks the policy improvement and is hard to
SSIM [82], LPIPS [95], and FVD [79], alongside optical flow scale [65, 85, 4, 64]. Regarding learning stability, some work
end-point error (EPE) [93] for action controllability. Quanti- proposes to freeze the large-scale pre-trained policy while
tatively, Table V underscores the superiority of RISE across optimizing an additional residual policy [85] or input noise
all baselines under identical experimental settings. Notably, distribution only [80, 58]. With most parameters unchanged,
the significant reduction in EPE validates our task-centric such approaches sacrifice the adaptability of the policy to
pre-training, confirming that prioritizing action-conditioned target tasks. In contrast, RECAP [2] enables finetuning the
|     |     |     |     |     |     |     |     | pre-trained | policy | via | an advantage-conditioned |     |     | formulation |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------ | --- | ------------------------ | --- | --- | ----------- | --- |
dynamicseffectivelyenhancesmotionawarenessbeyondstan-
dard pixel-level reconstruction. Qualitatively (Fig. 6), while [23,48],eliminatingthecomplexityofadjustingthedenoising
baselines suffer from blurring and kinematic inconsistencies, chain for diffusion or flow-matching policy [51]. To derive
RISE generates physically plausible dynamics with high fi- reliableadvantagesforpolicyoptimization,recentworksresort
delity. Additional comparisons are provided in the Appendix. to vision language models with a progress estimate formu-
|     |     |     |             |     |     |     |     | lation, which |      | is numerically |          | stable and | free | from | laborious |
| --- | --- | --- | ----------- | --- | --- | --- | --- | ------------- | ---- | -------------- | -------- | ---------- | ---- | ---- | --------- |
|     |     | V.  | RELATEDWORK |     |     |     |     |               |      |                |          |            |      |      |           |
|     |     |     |             |     |     |     |     | annotations   | [66, | 94, 2,         | 92, 25]. | However,   | such | an   | objective |
A. World Models for Robot Learning is prone to the over-fitting problem and is less sensitive to
World models have been envisioned as a pathway to en- subtle failures [2, 58]. Distinguished from prior approaches,
able effective planning and learning through internal imag- we enable on-policy RL by shifting the learning environment
fromthephysicalworldintoanimaginativespaceviaalearned
| ination | [50, 27, | 29, 78]. | Early | approaches |     | in robotics | and |     |     |     |     |     |     |     |     |
| ------- | -------- | -------- | ----- | ---------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
controlfocusedonabstractstatemodelinginlatentspacewith worldmodel.Furthermore,ourvaluemodelbenefitsfromboth
|              |          |     |        |       |             |     |           | progress | estimate | and | Temporal-Difference |     |     | learning | [77] in |
| ------------ | -------- | --- | ------ | ----- | ----------- | --- | --------- | -------- | -------- | --- | ------------------- | --- | --- | -------- | ------- |
| low-capacity | dynamics |     | model, | which | are limited | in  | capturing |          |          |     |                     |     |     |          |         |
the rich visual and contact dynamics required for real-world stability and failure sensitivity.
| manipulation     | [29,       | 30,         | 31, 34,  | 35,   | 33, 49]. | Recent  | advances |               |     |       |             |     |           |     |            |
| ---------------- | ---------- | ----------- | -------- | ----- | -------- | ------- | -------- | ------------- | --- | ----- | ----------- | --- | --------- | --- | ---------- |
|                  |            |             |          |       |          |         |          |               |     | VI.   | CONCLUSION  |     |           |     |            |
| in large-scale   | generative |             | modeling |       | renewed  | world   | modeling |               |     |       |             |     |           |     |            |
|                  |            |             |          |       |          |         |          | We introduced |     | RISE, | a framework | for | on-policy |     | reinforce- |
| in high-fidelity |            | observation |          | space | [10, 1,  | 32, 87, | 88, 99]. |               |     |       |             |     |           |     |            |
However,adaptingsuchmodelstoserveasinteractiveenviron- ment learning of robot foundation policies through imagina-
tion.RISEreplacesthephysicalenvironmentwithimagination
| ments for         | reinforcement   |             | learning     | remains |       | challenging. | Most       |         |             |          |                    |         |             |              |       |
| ----------------- | --------------- | ----------- | ------------ | ------- | ----- | ------------ | ---------- | ------- | ----------- | -------- | ------------------ | ------- | ----------- | ------------ | ----- |
|                   |                 |             |              |         |       |              |            | during  | training,   | enabling | scalable           | online  | improvement |              | with- |
| approaches        | prioritize      | visual      | plausibility |         | over  | action       | controlla- |         |             |          |                    |         |             |              |       |
|                   |                 |             |              |         |       |              |            | out the | prohibitive | cost     | and                | risk of | real-world  | exploration. |       |
| bility, incurring |                 | prohibitive | inference    |         | costs | that prevent | their      |         |             |          |                    |         |             |              |       |
|                   |                 |             |              |         |       |              |            | Central | to the      | system   | is a compositional |         | world       | model        | that  |
| use inside        | a reinforcement |             | learning     |         | loop. | Beyond       | dynamics   |         |             |          |                    |         |             |              |       |
prediction, reward and value shaping also introduce an addi- coherently orchestrates dynamics and value models, built
|     |     |     |     |     |     |     |     | from proper | recipes, | to  | efficiently | emulate | state | and | estimate |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | ----------- | ------- | ----- | --- | -------- |
tionalbottlenecktoapplythesemodelstopolicyimprovement.
|     |     |     |     |     |     |     |     | advantage | for | policy improvement. |     | Across |     | real-world | tasks |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------------------- | --- | ------ | --- | ---------- | ----- |
Prioreffortsheavilyrelyonsparseterminalrewardsorheuris-
|              |                  |     |              |        |       |                      |       | spanning             | dynamic | interaction,  |     | deformable-object |            |             | handling, |
| ------------ | ---------------- | --- | ------------ | ------ | ----- | -------------------- | ----- | -------------------- | ------- | ------------- | --- | ----------------- | ---------- | ----------- | --------- |
| tic distance | towards          | the | goal         | state, | which | provide insufficient |       |                      |         |               |     |                   |            |             |           |
|              |                  |     |              |        |       |                      |       | and bi-manual        |         | coordination, |     | RISE consistently |            | outperforms |           |
| guidance     | for long-horizon |     | manipulation |        | and   | are brittle          | under |                      |         |               |     |                   |            |             |           |
|              |                  |     |              |        |       |                      |       | strong post-training |         | baselines,    |     | proving           | that world | models      | can       |
long-termpredictionerrors[96,93,100,68].Importantly,prior
|              |        |        |           |     |            |      |         | be applied         | as  | an effective | learning    | environment  |     | to  | improve   |
| ------------ | ------ | ------ | --------- | --- | ---------- | ---- | ------- | ------------------ | --- | ------------ | ----------- | ------------ | --- | --- | --------- |
| works center | around | either | simulated |     | benchmarks | [34, | 35, 29, |                    |     |              |             |              |     |     |           |
|              |        |        |           |     |            |      |         | policy performance |     | on           | challenging | manipulation |     |     | tasks. We |
30,31,32,33,24],low-levelcontrolproblems[54,84,36,74],
|               |               |        |         |       |              |                |         | hope this | work     | serves         | as a reference |     | for the | community | in  |
| ------------- | ------------- | ------ | ------- | ----- | ------------ | -------------- | ------- | --------- | -------- | -------------- | -------------- | --- | ------- | --------- | --- |
| or short-term | tasks         | (e.g., | pick    | and   | place),      | with limited   | val-    |           |          |                |                |     |         |           |     |
|               |               |        |         |       |              |                |         | exploring | scalable | self-improving |                | VLA | models. |           |     |
| idation       | in real-world |        | tasks   | under | contact-rich | and            | complex |           |          |                |                |     |         |           |     |
| dynamics      | [93, 13,      | 44,    | 39, 49, | 26,   | 41, 3,       | 98]. Motivated | by      |           |          |                |                |     |         |           |     |
VII. LIMITATIONSANDFUTUREWORK
| prior efforts | that | carefully | integrate |     | heterogeneous | modules |     | to  |     |     |     |     |     |     |     |
| ------------- | ---- | --------- | --------- | --- | ------------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tacklethechallengingworldmodelingproblem[97,5,20],we The Gap between Imagination and Realism. The effective-
|            |         |     |          |       |     |         |          | ness of | RISE | is constrained |     | by the accuracy |     | and | coverage |
| ---------- | ------- | --- | -------- | ----- | --- | ------- | -------- | ------- | ---- | -------------- | --- | --------------- | --- | --- | -------- |
| seamlessly | compose | a   | dynamics | model | and | a value | function |         |      |                |     |                 |     |     |          |
to achieve faithful simulation for various actions. of the learned world model. Although our compositional de-
|     |     |     |     |     |     |     |     | sign improves |     | controllability |     | and consistency |     | relative | to prior |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --------------- | --- | --------------- | --- | -------- | -------- |
B. Reinforcement Learning for Foundation Policies generative simulators, the model can still produce physically
Reinforcement learning is increasingly used to strengthen implausible transitions in rare or underrepresented scenarios.
VLA foundation policies on robustness and precision of ma- Addressingthisgaprequiresfutureworkonuncertainty-aware

imagination and principled integration of physical constraints N1:Anopenfoundationmodelforgeneralisthumanoid
that explicitly encode geometry properties. robots. arXiv preprint arXiv:2503.14734, 2025. 18
The Simulated–Real Data Balance. Our results indicate that [7] Kevin Black, Noah Brown, Danny Driess, Adnan Es-
a non-trivial amount of real-world data remains essential to mail,MichaelEqui,ChelseaFinn,NiccoloFusai,Lachy
anchor the learning procedure. However, the optimal ratio Groom, Karol Hausman, Brian Ichter, et al. π : A
0
betweensimulatedrolloutsandreal-worldexperiencerequires vision-language-action flow model for general robot
further parameter tuning. Understanding the effectiveness and control. arXiv preprint arXiv:2410.24164, 2024. 1, 6,
principles of these offline data represents an open problem. 18
From Physical Cost to Compute Cost. RISE shifts the [8] Kevin Black, Noah Brown, James Darpinian, Karan
primary bottleneck in robot learning from physical interaction Dhabalia, Danny Driess, Adnan Esmail, Michael Equi,
to computation. While this trade-off releases the burden of Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker,
physicalinteraction,traininghigh-fidelityworldmodelsincurs Dibya Ghosh, Lachy Groom, Karol Hausman, Brian
a high computational cost. Improving the efficiency of world Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke,
models will be critical for the compute-constrained regime. Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mo-
Outlook. Taken together, these limitations suggest a promis- hith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z.
ing pathway in integrating learned simulation into a broader Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias
data ecosystem, where model-based reinforcement learning Springenberg, Kyle Stachowicz, James Tanner, Quan
complementsscarcephysicalinteraction.Discoveringtheright Vuong, Homer Walke, Anna Walling, Haohuan Wang,
balance between these two key components points to a future Lili Yu, and Ury Zhilinsky. π : a vision-language-
0.5
of adaptive, robust, and sample-efficient robotic intelligence. action model with open-world generalization. arXiv
preprint arXiv:2504.16054, 2025. 1, 2, 4, 5, 6, 16, 17,
VIII. ACKNOWLEDGMENTS
18
This study is supported by National Natural Science Foun- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yev-
dationofChina(62206172).Thisworkisinpartsupportedby gen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana
the JC STEM Lab of Autonomous Intelligent Systems funded Gopalakrishnan,KarolHausman,AlexHerzog,Jasmine
by The Hong Kong Jockey Club Charities Trust. Hsu, et al. RT-1: Robotics transformer for real-world
control at scale. In RSS, 2023. 1
REFERENCES
[10] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack
[1] Arslan Ali, Junjie Bai, Maciej Bala, Yogesh Balaji, Parker-Holder,YugeShi,EdwardHughes,MatthewLai,
Aaron Blakeman,Tiffany Cai,Jiaxin Cao, Tianshi Cao, AditiMavalankar,RichieSteigerwald,ChrisApps,etal.
Elizabeth Cha, Yu-Wei Chao, et al. World simulation Genie: Generative interactive environments. In ICML,
with video foundation models for physical ai. arXiv 2024. 8
preprint arXiv:2511.00062, 2025. 4, 7, 8, 18 [11] QingwenBu,JisongCai,LiChen,XiuqiCui,YanDing,
[2] Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Siyuan Feng, Xindong He, Xu Huang, et al. AgiBot
Kevin Black, Ken Conley, Grace Connors, James World Colosseo: A large-scale manipulation platform
Darpinian, Karan Dhabalia, Jared DiCarlo, Danny forscalableandintelligentembodiedsystems. InIROS,
Driess, et al. π∗ : a vla that learns from experience. 2025. 4, 6, 18
0.6
arXiv preprint arXiv:2511.14759, 2025. 3, 5, 6, 8, 14, [12] QingwenBu,YantingYang,JisongCai,ShenyuanGao,
16, 17, 18 GuanghuiRen,MaoqingYao,PingLuo,andHongyang
[3] Mido Assran, Adrien Bardes, David Fan, Quentin Gar- Li. Univla: Learning to act anywhere with task-centric
rido, Russell Howes, Matthew Muckley, Ammar Rizvi, latent actions. In RSS, 2025. 18
Claire Roberts, Koustuv Sinha, Artem Zholus, et al. [13] Akshay L Chandra, Iman Nematollahi, Chenguang
V-JEPA 2: Self-supervised video models enable un- Huang, Tim Welschehold, Wolfram Burgard, and Ab-
derstanding, prediction and planning. arXiv preprint hinav Valada. DiWA: Diffusion policy adaptation with
arXiv:2506.09985, 2025. 8 world models. arXiv preprint arXiv:2508.03645, 2025.
[4] Philip J Ball, Laura Smith, Ilya Kostrikov, and Sergey 5, 8
Levine. Efficient online reinforcement learning with [14] Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo,
offline data. In ICML, 2023. 8 SiXu,HaoLin,HongzhiZang,QuanluZhang,Zhaofei
[5] Leonardo Barcellona, Andrii Zadaianchuk, Davide Al- Yu, Guoliang Fan, et al. π : Online rl fine-tuning
RL
legro, Samuele Papa, Stefano Ghidoni, and Efstratios for flow-based vision-language-action models. arXiv
Gavves. Dream to Manipulate: Compositional world preprint arXiv:2510.25889, 2025. 8
modelsempoweringrobotimitationlearningwithimag- [15] Li Chen, Chonghao Sima, Kashyap Chitta, Antonio
ination. arXiv preprint arXiv:2412.14957, 2024. 2, 8 Loquercio,PingLuo,YiMa,andHongyangLi. Intelli-
[6] Johan Bjorck, Fernando Castan˜eda, Nikita Cherniadev, gent robot manipulation requires self-directed learning.
Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter OpenReview, 2026. URL https://openreview.net/forum?
Fox, Fengyuan Hu, Spencer Huang, et al. GR00T id=Seb7rprW1Y. Accessed: 2026-01-02. 2

[16] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Levin,GuyShiran,NirZabari,OriGordon,etal. LTX-
Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Video: Realtime video latent diffusion. arXiv preprint
YihengGe,ZhenyuGu,etal. RoboTwin2.0:Ascalable arXiv:2501.00103, 2024. 2, 4
data generator and benchmark with strong domain ran- [29] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and
domization for robust bimanual robotic manipulation. Mohammad Norouzi. Dream to Control: Learning
arXiv preprint arXiv:2506.18088, 2025. 8 Behaviors by Latent Imagination. arXiv preprint
[17] Zengjue Chen, Runliang Niu, He Kong, Qi Wang, arXiv:1912.01603, 2019. 2, 8
Qianli Xing, and Zipei Fan. TGRPO: Fine- [30] Danijar Hafner, Timothy Lillicrap, Mohammad
tuningvision-language-actionmodelviatrajectory-wise Norouzi, and Jimmy Ba. Mastering Atari with Discrete
group relative policy optimization. arXiv preprint World Models. In ICLR, 2021. 2, 8
arXiv:2506.08440, 2025. 8 [31] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Tim-
[18] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric othy Lillicrap. Mastering Diverse Domains through
Cousineau, Benjamin Burchfiel, and Shuran Song. Dif- WorldModels. arXivpreprintarXiv:2301.04104,2023.
fusion Policy: Visuomotor policy learning via action 2, 8
diffusion. In RSS, 2023. 18 [32] Danijar Hafner, Wilson Yan, and Timothy Lillicrap.
[19] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Training agents inside of scalable world models. arXiv
Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and preprint arXiv:2509.24527, 2025. 8
Shuran Song. Universal Manipulation Interface: In-the- [33] Nicklas Hansen, Yixin Lin, Hao Su, Xiaolong Wang,
wild robot teaching without in-the-wild robots. In RSS, Vikash Kumar, and Aravind Rajeswaran. MoDem:
2024. 18 Acceleratingvisualmodel-basedreinforcementlearning
[20] Yilun Du, Sherry Yang, Pete Florence, Fei Xia, Ayzaan with demonstrations. arXiv preprint arXiv:2212.05698,
Wahid,BrianIchter,PierreSermanet,TianheYu,Pieter 2022. 8
Abbeel, Joshua B. Tenenbaum, Leslie Pack Kaelbling, [34] NicklasHansen,HaoSu,andXiaolongWang.Temporal
Andy Zeng, and Jonathan Tompson. Video Language difference learning for model predictive control. In
Planning. In ICLR, 2024. 2, 8 ICML, 2022. 8
[21] PatrickEsser,SumithKulal,AndreasBlattmann,Rahim [35] Nicklas Hansen, Hao Su, and Xiaolong Wang. TD-
Entezari,JonasMu¨ller,HarrySaini,YamLevi,Dominik MPC2: Scalable, robust world models for continuous
Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling control. arXiv preprint arXiv:2310.16828, 2023. 8
rectified flow transformers for high-resolution image [36] Nicklas Hansen, Jyothir SV, Vlad Sobal, Yann LeCun,
synthesis. In Forty-first international conference on XiaolongWang,andHaoSu.Hierarchicalworldmodels
machine learning, 2024. 15 as visual whole-body humanoid controllers. arXiv
[22] Kuan Fang, Fangchen Liu, Pieter Abbeel, and Sergey preprint arXiv:2405.18418, 2024. 8
Levine. MOKA: Open-World Robotic Manipulation [37] Zheyuan Hu, Robyn Wu, Naveen Enock, Jasmine
through Mark-Based Visual Prompting. In RSS, 2024. Li, Riya Kadakia, Zackory Erickson, and Aviral Ku-
1 mar. RaC: Robot learning for long-horizon tasks
[23] Kevin Frans, Seohong Park, Pieter Abbeel, and Sergey by scaling recovery and correction. arXiv preprint
Levine. Diffusion guidance is a controllable policy im- arXiv:2509.07953, 2025. 2
provement operator. arXiv preprint arXiv:2505.23458, [38] Xun Huang, Zhengqi Li, Guande He, Mingyuan Zhou,
2025. 6, 8 andEliShechtman. SelfForcing:Bridgingthetrain-test
[24] Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, gap in autoregressive video diffusion. arXiv preprint
and Chuang Gan. AdaWorld: Learning adaptable arXiv:2506.08009, 2025. 5
world models with latent actions. arXiv preprint [39] Chia-Yu Hung, Navonil Majumder, Haoyuan Deng,
arXiv:2503.18938, 2025. 8 Liu Renhang, Yankang Ang, Amir Zadeh, Chuan Li,
[25] Seyed Kamyar Seyed Ghasemipour, Ayzaan Wahid, Dorien Herremans, Ziwei Wang, and Soujanya Poria.
JonathanTompson,PannagSanketi,andIgorMordatch. NORA-1.5:Avision-language-actionmodeltrainedus-
Self-improving embodied foundation models. arXiv ing world model-and action-based preference rewards.
preprint arXiv:2509.15155, 2025. 2, 8, 18 arXiv preprint arXiv:2511.14659, 2025. 8
[26] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and [40] Pavel Izmailov, Dmitrii Podoprikhin, Timur Garipov,
Chelsea Finn. Ctrl-world: A controllable generative Dmitry P. Vetrov, and Andrew Gordon Wilson. Av-
world model for robot manipulation. arXiv preprint eraging weights leads to wider optima and better gen-
arXiv:2510.10125, 2025. 2, 8 eralization. In UAI, 2018. 5
[27] David Ha and Ju¨rgen Schmidhuber. Recurrent World [41] JoelJang,SeonghyeonYe,ZongyuLin,JiannanXiang,
Models Facilitate Policy Evolution. In NeurIPS, 2018. Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang,
2, 8 KaushilKundalia,Yen-ChenLin,etal. DreamGen:Un-
[28] Yoav HaCohen, Nisan Chiprut, Benny Brazowski, locking generalization in robot learning through video
Daniel Shalem, Dudu Moshe, Eitan Richardson, Eran world models. In CoRL, 2025. 8, 18

[42] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Robotic World Model: A neural network simulator for
Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang robust policy optimization in robotics. arXiv preprint
Wang, Zhihui Peng, and Hongyang Li. Whole- arXiv:2501.10100, 2025. 8
BodyVLA: Towards unified latent vla for whole-body [55] Dacheng Li, Yunhao Fang, Yukang Chen, Shuo Yang,
loco-manipulation control. In ICLR, 2026. 18 Shiyi Cao, Justin Wong, Michael Luo, Xiaolong Wang,
[43] Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Hongxu Yin, Joseph E Gonzalez, et al. WorldMod-
Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, elBench: Judging video generation models as world
Huazhe Xu, and Hang Zhao. Galaxea open-world models. arXiv preprint arXiv:2502.20694, 2025. 2
dataset and g0 dual-system vla model. arXiv preprint [56] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhao-
arXiv:2509.00576, 2025. 4, 6, 18 hui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang,
[44] Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yu- Tianxing Chen, Ganqu Cui, et al. SimpleVLA-RL:
peng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, and Scaling vla training via reinforcement learning. arXiv
Dongbin Zhao. World4RL: Diffusion world models preprint arXiv:2509.09674, 2025. 2, 8
for policy refinement with reinforcement learning for [57] XinqingLi,XinHe,LeZhang,MinWu,XiaoliLi,and
roboticmanipulation. arXivpreprintarXiv:2509.19080, Yun Liu. A comprehensive survey on world models for
2025. 5, 8 embodied ai. arXiv preprint arXiv:2510.16732, 2025.
[45] Michael Kelly, Chelsea Sidrane, Katherine Driggs- 2
Campbell, and Mykel J Kochenderfer. HG-DAgger: [58] YunfeiLi,XiaoMa,JiafengXu,YuCui,ZhongrenCui,
Interactive imitation learning with human experts. In Zhigang Han, Liqun Huang, Tao Kong, Yuxiao Liu,
ICRA, 2019. 2, 6 Hao Niu, et al. GR-RL: Going dexterous and precise
[46] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted for long-horizon robotic manipulation. arXiv preprint
Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, arXiv:2512.01801, 2025. 8
Ethan Paul Foster, Pannag R. Sanketi, Quan Vuong, [59] Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang,
Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai,
DorsaSadigh,SergeyLevine,PercyLiang,andChelsea Si Liu, Jianlan Luo, et al. Genie Envisioner: A unified
Finn. OpenVLA: An open-source vision-language- world foundation platform for robotic manipulation.
action model. In CoRL, 2024. 1, 18 arXiv preprint arXiv:2508.05635, 2025. 2, 4, 7, 8, 17,
[47] Moo Jin Kim, Chelsea Finn, and Percy Liang. 18
Fine-tuning vision-language-action models: Optimizing [60] BoLiu,YifengZhu,ChongkaiGao,YihaoFeng,Qiang
speed and success. arXiv preprint arXiv:2502.19645, Liu,YukeZhu,andPeterStone. LIBERO:Benchmark-
2025. 18 ing knowledge transfer for lifelong robot learning. In
[48] Aviral Kumar, Xue Bin Peng, and Sergey Levine. NeurIPS, 2023. 2, 8
Reward-conditioned policies. arXiv preprint [61] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qing-
arXiv:1912.13465, 2019. 6, 8 min Liao, Yi Wu, Chao Yu, and Yu Wang. What can
[49] PatrickLancaster,NicklasHansen,AravindRajeswaran, rl bring to vla generalization? an empirical study. In
and Vikash Kumar. MoDem-V2: Visuo-motor world NeurIPS, 2025. 2, 8
models for real-world robot manipulation. In ICRA, [62] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai
2024. 8 Tan,HuayuChen,ZhengyiWang,KeXu,HangSu,and
[50] Yann LeCun. A path towards autonomous machine JunZhu. RDT-1B:Adiffusionfoundationmodelforbi-
intelligence. Open Review, 2022. 2, 8 manualmanipulation.arXivpreprintarXiv:2410.07864,
[51] KunLei,HuanyuLi,DongjieYu,ZhenyuWei,Lingxiao 2024. 18
Guo, Zhennan Jiang, Ziyu Wang, Shiyu Liang, and [63] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng
Huazhe Xu. RL-100: Performant robotic manipulation Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and
with real-world reinforcement learning. arXiv preprint Ziwei Wang. VLA-RL: Towards masterful and general
arXiv:2510.14830, 2025. 8 roboticmanipulationwithscalablereinforcementlearn-
[52] SergeyLevine,AviralKumar,GeorgeTucker,andJustin ing. arXiv preprint arXiv:2505.18719, 2025. 2, 8
Fu. Offline reinforcement learning: Tutorial, review, [64] Jianlan Luo, Zheyuan Hu, Charles Xu, You Liang Tan,
and perspectives on open problems. arXiv preprint Jacob Berg, Archit Sharma, Stefan Schaal, Chelsea
arXiv:2005.01643, 2020. 2 Finn, Abhishek Gupta, and Sergey Levine. SERL: A
[53] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gok- softwaresuiteforsample-efficientroboticreinforcement
men, Sanjana Srivastava, Roberto Mart´ın-Mart´ın, Chen learning. In ICRA, 2024. 2, 8
Wang, Gabrael Levine, Wensi Ai, Benjamin Martinez, [65] Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey
et al. BEHAVIOR-1K: A human-centered, embodied ai Levine. Precise and dexterous robotic manipulation
benchmark with 1,000 everyday activities and realistic via human-in-the-loop reinforcement learning. Science
simulation. arXiv preprint arXiv:2403.09227, 2024. 18 Robotics, 2025. 2, 8, 17
[54] Chenhao Li, Andreas Krause, and Marco Hutter. [66] Yecheng Jason Ma, Joey Hejna, Chuyuan Fu, Dhruv

Shah, Jacky Liang, Zhuo Xu, Sean Kirmani, Peng Xu, [80] Andrew Wagenmaker, Yunchu Zhang, Mitsuhiko
Danny Driess, Ted Xiao, et al. Vision language models Nakamoto, Seohong Park, Waleed Yagoub, Anusha
are in-context value learners. In ICLR, 2024. 2, 8 Nagabandi,AbhishekGupta,andSergeyLevine. Steer-
[67] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and ing your diffusion policy with latent space reinforce-
Wolfram Burgard. CALVIN: A benchmark for ment learning. In CoRL, 2025. 2, 6, 8, 14, 16, 17
language-conditioned policy learning for long-horizon [81] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan
robot manipulation tasks. RA-L, 2022. 8 Vuong, Chongyi Zheng, Philippe Hansen-Estruch, An-
[68] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. dre Wang He, Vivek Myers, Moo Jin Kim, Max Du,
Structured world models from human videos. In CoRL, et al. BridgeData v2: A dataset for robot learning at
2023. 8 scale. In CoRL, 2023. 7, 18
[69] Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, [82] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and
Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Eero P Simoncelli. Image quality assessment: From er-
Yude Zou, Mingkun Xu, et al. RoboTwin: Dual-arm ror visibility to structural similarity. IEEE transactions
robot benchmark with generative digital twins. In on image processing, 2004. 8
CVPR, 2025. 8 [83] Longyan Wu, Checheng Yu, Jieji Ren, Li Chen, Ran
[70] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Huang, Guoying Gu, and Hongyang Li. FreeTac-
Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Man- Man:Robot-freevisuo-tactiledatacollectionsystemfor
dlekar, and Yuke Zhu. RoboCasa: Large-scale simu- contact-rich manipulation. In ICRA, 2026. 18
lation of everyday tasks for generalist robots. arXiv [84] Philipp Wu, Alejandro Escontrela, Danijar Hafner,
preprint arXiv:2406.02523, 2024. 18 Pieter Abbeel, and Ken Goldberg. DayDreamer: World
[71] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, models for physical robot learning. In CoRL, 2023. 8
Abhishek Gupta, Abhishek Padalkar, Abraham Lee, [85] Wenli Xiao, Haotian Lin, Andy Peng, Haoru Xue,
Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya TairanHe,YuqiXie,FengyuanHu,JimmyWu,Zhengyi
Jain, et al. Open X-Embodiment: Robotic learning Luo, Linxi Fan, et al. Self-improving vision-language-
datasets and rt-x models: Open x-embodiment collabo- actionmodelswithdatagenerationviaresidualrl. arXiv
ration. In ICRA, 2024. 18 preprint arXiv:2511.00091, 2025. 2, 8, 17, 18
[72] Xue Bin Peng, Aviral Kumar, Grace Zhang, and [86] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long
SergeyLevine. Advantage-weightedregression:Simple Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, An-
and scalable off-policy reinforcement learning. arXiv dreas Geiger, Xiangyu Yue, and Li Chen. ReSim:
preprint arXiv:1910.00177, 2019. 2 ReliableWorldSimulationforAutonomousDriving. In
[73] StephaneRoss,GeoffreyGordon,andDrewBagnell. A NeurIPS, 2025. 2
reductionofimitationlearningandstructuredprediction [87] Sherry Yang, Yilun Du, Seyed Kamyar Seyed
to no-regret online learning. In AISTATS, 2011. 2, 6 Ghasemipour, Jonathan Tompson, Leslie Pack Kael-
[74] Pascal Roth, Jonas Frey, Cesar Cadena, and Marco bling, Dale Schuurmans, and Pieter Abbeel. Learning
Hutter. Learned perceptive forward dynamics model interactive real-world simulators. In ICLR, 2024. 2, 8
for safe and platform-aware robotic navigation. In RSS, [88] Sherry Yang, Jacob Walker, Jack Parker-Holder, Yilun
2025. 8 Du,JakeBruce,AndreBarreto,PieterAbbeel,andDale
[75] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Schuurmans. Video as the new language for real-world
Radford, and Oleg Klimov. Proximal policy opti- decision making. In ICML, 2024. 8
mization algorithms. arXiv preprint arXiv:1707.06347, [89] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune
2017. 6 Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar,
[76] Modi Shi, Li Chen, Jin Chen, Yuxiang Lu, Chiming Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al.
Liu,GuanghuiRen,PingLuo,DiHuang,MaoqingYao, Latent action pretraining from videos. arXiv preprint
and Hongyang Li. Is diversity all you need for scalable arXiv:2410.11758, 2024. 18
roboticmanipulation?arXivpreprintarXiv:2507.06219, [90] TianheYu,GarrettThomas,LantaoYu,StefanoErmon,
2025. 1 JamesYZou,SergeyLevine,ChelseaFinn,andTengyu
[77] Richard S. Sutton. Learning to predict by the methods Ma. Mopo:Model-basedofflinepolicyoptimization. In
of temporal differences. Machine learning, 1988. 2, 5, NeurIPS, 2020. 2
8 [91] Hongzhi Zang, Mingjie Wei, Si Xu, Yongji Wu, Zhen
[78] Richard S. Sutton. Dyna, an integrated architecture for Guo, Yuanqing Wang, Hao Lin, Liangzhi Shi, Yuqing
learning, planning, and reacting. ACM Sigart Bulletin, Xie, Zhexuan Xu, et al. RLinf-VLA: A unified and
1991. 2, 8 efficient framework for vla+ rl training. arXiv preprint
[79] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Ku- arXiv:2510.06710, 2025. 17
rach, Raphae¨l Marinier, Marcin Michalski, and Sylvain [92] ShaopengZhai,QiZhang,TianyiZhang,FuxianHuang,
Gelly. Fvd: A new metric for video generation. 2019. HaoranZhang,MingZhou,ShengzheZhang,LitaoLiu,
8 Sixu Lin, and Jiangmiao Pang. A vision-language-

action-criticmodelforroboticreal-worldreinforcement Brown, Anthony Brohan, Montserrat Gonzalez Arenas,
learning. arXiv preprint arXiv:2509.15937, 2025. 2, 8 and Kehang Han. RT-2: Vision-language-action models
[93] Jiahui Zhang, Ze Huang, Chun Gu, Zipei Ma, and transfer web knowledge to robotic control. In CoRL,
Li Zhang. Reinforcing action policies by prophesying. 2023. 18
arXiv preprint arXiv:2511.20633, 2025. 5, 8
[94] JiahuiZhang,YusenLuo,AbrarAnwar,SumedhAnand
Sontakke,JosephJLim,JesseThomason,ErdemBiyik,
and Jesse Zhang. ReWiND: Language-guided rewards
teach robot policies without new demonstrations. arXiv
preprint arXiv:2505.10911, 2025. 8
[95] Richard Zhang, Phillip Isola, Alexei A Efros, Eli
Shechtman, and Oliver Wang. The unreasonable ef-
fectiveness of deep features as a perceptual metric. In
ProceedingsoftheIEEEconferenceoncomputervision
and pattern recognition, 2018. 8
[96] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel
Pinto. DINO-WM: World models on pre-trained visual
features enable zero-shot planning. arXiv preprint
arXiv:2411.04983, 2024. 8
[97] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-
Yan Yeung, and Chuang Gan. RoboDreamer: Learn-
ing compositional world models for robot imagination.
arXiv preprint arXiv:2404.12377, 2024. 2, 8
[98] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin
Burchfiel, Paarth Shah, and Abhishek Gupta. Unified
world models: Coupling video and action diffusion for
pretraining on large robotic datasets. In RSS, 2025. 8
[99] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu,
Chilam Cheang, and Tao Kong. IRASim: Learning
interactive real-robot action simulators. arXiv preprint
arXiv:2406.14540, 2024. 2, 8
[100] Fangqi Zhu, Zhengyang Yan, Zicong Hong, Quanxin
Shou, Xiao Ma, and Song Guo. WMPO: World model-
based policy optimization for vision-language-action
models. arXiv preprint arXiv:2511.09515, 2025. 8
[101] Wanrong Zhu, Jack Hessel, Anas Awadalla,
Samir Yitzhak Gadre, Jesse Dodge, Alex Fang,
Youngjae Yu, Ludwig Schmidt, William Yang Wang,
and Yejin Choi. Multimodal C4: An open, billion-scale
corpus of images interleaved with text. In NeurIPS,
2023. 18
[102] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu,
Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan
Welker, Ayzaan Wahid, Quan Vuong, Vincent Van-
houcke, Huong T. Tran, Radu Soricut, Anikait Singh,
Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi,
Grecia Salazar, Michael S. Ryoo, Krista Reymann,
Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk
Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-
Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry
Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan,
Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol
Hausman,KeerthanaGopalakrishnan,ChuyuanFu,Pete
Florence, Chelsea Finn, Kumar Avinava Dubey, Danny
Driess, Tianli Ding, Krzysztof Marcin Choromanski,
Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah

APPENDIX
The appendix is organized as follows:
• InAppendixSec.IX,wepresentadditionalexperimental
results,includingsomeablationstudiesonminorcompo-
nents and visualization of the learned representations.
• In Appendix Sec. X, we list the comprehensive experi-
mental settings, including hyperparameter configurations
and hardware environments.
• In Appendix Sec. XI, we elaborate on the implementa-
tion details of modules of RISE.
• In Appendix Sec. XII, we provide a conceptual com-
parison between our method and several highly related
works.
• In Appendix Sec. XIII, we provide more qualitative
visualizations.
• InAppendixSec.XIV,weanalyzefailuremodeofRISE.
• InAppendixSec.XV,weincludeadditionalrelatedwork
on vision-language-action models.
• In Appendix Sec. XVI, we list the license for each asset
used in this paper, i.e., data and pre-trained weights.
• In Appendix Sec. XVII, we envision the broader impact
of the proposed method.
IX. ADDITIONALRESULTS
100
80
60
40
20
0
etaR
sseccuS
100
80
60
40
20
0
40 49 50 60 70 80 90
Training Steps (k)
100.0095.00 95.25 bin 10 bin 5 bin 1 93.75 90.79
84.00 85.00
60.00
40.00
Pick & Place Sort Complete
Fig.7:Tasksuccessrateacrossadvantagebins.Aclearper-
formance drop is observed from high to low advantage levels,
especially in Sorting. This confirms that our policy effectively
captures behavior diversity through advantage conditioning.
Can bins with different advantages reveal different per-
formance of the policy? RISE utilizes advantage-based bins
toguideRLtraining.Weinvestigatewhetherthepolicyyields
diverse task performance when conditioned on different bins.
To this end, we evaluate the policy conditioned on high (Bin
10), neutral (Bin 5), and low (Bin 1) advantage bins. Results
inFig.7showaperformancedropfrombin10tobin1,which
supports our hypothesis. This performance drop is primarily
attributedtosortingerrors,asthesuccessrateforsortdeterio-
rates more significantly than for pick-and-place. Furthermore,
theagentdisplaysincreasedinstabilitywithlowerbinindices.
These findings demonstrate that our learned advantages are
convincingandthatthepolicyeffectivelycapturesthediversity
of behaviors through our conditioning RL.
Can extended training of RL baselines match RISE’s
performance? To verify that our gains are not simply due to
more training, we extended the RECAP and DSRL baselines
)%(
etaR
sseccuS
Success Rate: RISE (Ours) RECAP DSRL
Score: RISE (Ours) RECAP DSRL
10
8
6
4
Score
Fig. 8: Learning dynamics of RL alternatives. Compared
to RECAP [2] and DSRL [80], RISE yields significantly
higher results, which cannot be attained by the competing
methods even with extended training [2] and increased real-
world interactions [80].
TABLE VI: Quantitative ablation on the pre-training of
our dynamics model.
Method PSNR↑ LPIPS↓ SSIM↑ FVD↓ EPE↓
RISE(w/opre-train) 20.95 0.11 0.78 83.36 1.09
RISE(Ours) 23.90 0.07 0.82 66.84 0.54
with an extra 50k steps under the same batch size of our
method.AsshowninFig.8,RECAPsaturatesata30%to50%
successrate,whileDSRLsaturatesat5%to10%.Incontrast,
RISEyieldsa+35%improvement(boostingsuccessratefrom
50% to 85%) with only 9k additional steps. We attribute this
efficiencytoonlineworldmodelinteraction,providingdiverse
samples to mitigate overfitting.
Whatistheimpactofpre-trainingandtask-centricstrate-
gies on the generation quality of future dynamics? We
investigate the impact of strategies on the generation quality
of future dynamics. As shown in Table VI, pre-training
significantly enhances video generation fidelity. Moreover,
Fig. 12 provides visual comparisons, revealing that ablated
variants(specificallyw/otask-centricandw/opre-train)suffer
from action misalignment and severe blurring, whereas our
method maintains high consistency with ground truth dynam-
ics.Additionally,asample-wiseopticalflowanalysisinFig.9
isolates the role of the task-centric mechanism. The results
demonstrate that this objective effectively enhances motion
sensitivity, yielding sharper and more physically coherent
predictions.
X. REAL-WORLDEXPERIMENTALDETAILS
A. Task Evaluation Standard
To provide a fine-grained analysis of policy performance
beyond binary success, we define a quantitative evaluation

RGB Frames Visualized Optical Flow TABLE VII: Task evaluation standard.
Task Sub-goals Total Score
Graspbrick 1.0each
Conveyor Placeinmatchedbin 10 1.5each
G Workspacecleared 10.0max
T
Openbag&Insertitems 2.5
Lifttosettlecontents 5.0
Backpack 10
Ziphalfway 7.5
Zipfully 10.0max
EPE: 3.379
Loadcup 2.5
Foldsideflaps 5.0
Box 10
Foldrearflap 7.5
R
SI Tucklockingtab 10.0max
E
O(
u
sr
)
B. Real-World Deployment
Tobridgethegapbetweenthediscrete,low-frequencyinfer-
ence of the VLA model and the continuous, high-frequency
EPE: 4.857
requirements of real-world robotic control, we implemented
an asynchronous control framework operating directly in joint
R
SI space. Specifically, the VLA policy predicts action chunks
CE
n e w( with a horizon of H = 50 steps at a relatively low in-
)
cirt
a T
o/
ference frequency, while the robot controller executes joint
s commands at a 30 Hz frequency. Instead of executing these
k
chunks sequentially, which would cause motion freezing dur-
ing inference, we adopt a Temporal Ensembling strategy that
continuously integrates newly predicted action chunks into a
Fig. 9: Task-centric versus non-task-centric during pre-
running execution plan.
train stage. The optical flow maps demonstrate that our
This integration is governed by a linear weighting scheme
method captures action adherence more effectively during the
designed to smooth out transitions and suppress high-
initial stages of pre-training.
frequency jitter. When a new action chunk anew is received
from the inference thread, it overlaps with the unexecuted
portion of the existing action sequence aold in the buffer.
rubricdetailedinTableVII.Giventhatourtasksinvolvemulti-
For any time step t within this overlapping window, the final
stage and long-horizon planning (as qualitatively illustrated in executed action command a ∈ R14 (corresponding to the
t
Figure 17), a simple success/failure metric fails to capture the
bi-manual setup in Figure 11) is derived via a time-varying
incremental progress of the agent. Therefore, we decompose
linear interpolation between the previous plan aold and the
each task into distinct sub-goals, with a total score of 10 per
new prediction anew. This ensures that the robot’s trajectory
episode to ensure consistency across different tasks. Through-
is primarily guided by the established plan at the beginning
out the paper, each of our evaluation results is based on an
of the update to maintain continuity, while gradually shifting
average score of 20 autonomous trials.
priority to the latest sensory observations towards the end.
For the Dynamic Brick Sorting task, the scoring mecha-
nism focuses on both manipulation robustness and classifica- XI. IMPLEMENTATIONDETAILS
tion accuracy. As the task involves processing a stream of ob- A. Task-specific Data Composition
jects,pointsareaccumulateddynamically:successfulgrasping
DynamicBrickSortingincludes3063humandemonstration
rewards the robot’s low-level control, while correct placement
data and 610 policy rollout data. Backpack Packing covers
into color-matched bins rewards semantic understanding. The
2478 human demonstrations and 507 policy rollout data.
score is capped at 10 to represent perfect clearing of the
Box Closing features 2286 human demonstrations, 524 policy
workspace.
rollouts, and 540 human corrections (DAgger) data.
For the Backpack Packing and Box Closing tasks, which
B. Dynamics Model
arestrictlysequential,weadoptamilestone-basedscoringsys-
tem. As shown in Table VII, these tasks are divided into four Our dynamics model operates on multi-view RGB obser-
logical phases, with intermediate rewards assigned upon the vations (192 × 256) captured from top-down and bilateral
completion of each sub-goal. This stepwise evaluation allows wrist cameras, conditioned on future actions. We employ a
ustopinpointexactlywhereapolicymightdegrade—whether FlowMatchingobjectivefortraining.Fortimestepscheduling,
duringtheinitialinteractionwithdeformableobjectsorduring we adopt the Logit-Normal distribution following SD3 [21],
precision-critical phases like zipping or tab insertion. defined as logit(t) ∼ N(m,s2), with m = 0.2 and s = 1.0.

View
Dynamics model prediction
Timestep
GT final frame
Dynamics model prediction
GT final frame
Fig. 10: More multi-view rollouts on real world tasks. Our dynamics model synthesizes coherent multi-view video rollouts
with high visual fidelity, laying a solid foundation for reinforcement learning. Each video clip is ordered top to bottom.
| Gripper A |     |     |     |     | C. Value     | Model          |     |     |        |       |       |            |
| --------- | --- | --- | --- | --- | ------------ | -------------- | --- | --- | ------ | ----- | ----- | ---------- |
|           |     |     |     |     | The training | configurations |     |     | of the | value | model | are listed |
Top Camera
Gripper B in Table IX. For each task, the total training takes about 50k
|     |     |     |     |     | steps. For       | the first | 10k steps,   | we  | apply    | progress | estimate     | loss |
| --- | --- | --- | --- | --- | ---------------- | --------- | ------------ | --- | -------- | -------- | ------------ | ---- |
|     |     |     |     |     | only, whereasfor |           | theremaining |     | steps,we | apply    | bothprogress |      |
Wrist Cameras
|     |     |     |          |     | estimate    | and Temporal   | Difference |      | learning   |               | loss jointly. | No-    |
| --- | --- | --- | -------- | --- | ----------- | -------------- | ---------- | ---- | ---------- | ------------- | ------------- | ------ |
|     |     |     | Top View |     | tably, both | dynamics       | model      | and  | value      | model         | are kept      | frozen |
|     |     |     |          |     | during the  | self-improving |            | loop | for policy | optimization. |               |        |
Grippers
|     |     |     |     |     | D. Policy | Optimization |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --------- | ------------ | --- | --- | --- | --- | --- | --- |
0.75 m
Left View
Thepolicyfirstgetswarmedupmainlyfollowingtheoffline
|     |     |     |            |     | RL approach    | [2]        | with two    | differences. |          | RECAP          |           | discretizes |
| --- | --- | --- | ---------- | --- | -------------- | ---------- | ----------- | ------------ | -------- | -------------- | --------- | ----------- |
|     |     |     |            |     | the labeled    | advantages |             | into binary  |          | bins,          | yet we    | find that   |
|     |     |     |            |     | discretizing   | advantages |             | into 10      | bins     | with           | uniform   | intervals   |
|     |     |     | Right View |     | yields higher  | results.   | Moreover,   |              | directly |                | assigning | human       |
|     |     |     |            |     | demonstrations | to         | the highest |              | bins     | while labeling |           | only the    |
|     |     |     |            |     | policy rollout | data       | stabilizes  |              | learned  | behavior.      |           | These two   |
2 x (6 DoF Arm + 1 DoF Gripper) discrepancies might emerge from the fact that our model
|                                                      |     |     |     |     | initialization | π        | is not | pre-trained |     | with         | advantage | condi-     |
| ---------------------------------------------------- | --- | --- | --- | --- | -------------- | -------- | ------ | ----------- | --- | ------------ | --------- | ---------- |
| Fig.11:Experimentalsetup.Weutilizeabi-manualplatform |     |     |     |     |                | 0.5      |        |             |     |              |           |            |
|                                                      |     |     |     |     | tioning,       | contrary | to the | offline     | RL  | pre-training |           | as in π∗ , |
for our tasks. Each arm possesses 6 DoF along with a 1-DoF 0.6
gripper, equipped with a wrist-mounted camera. To provide where RECAP is instantiated. Subsequently, we start the self-
|          |                  |                           |            |             | improving   | loop with      | configurations |     | listed | in  | Table | X.  |
| -------- | ---------------- | ------------------------- | ---------- | ----------- | ----------- | -------------- | -------------- | --- | ------ | --- | ----- | --- |
| a global | view, a top-down | camera is                 | positioned | centrally   |             |                |                |     |        |     |       |     |
| between  | the arms at      | a height of approximately |            | 0.75 m. The |             |                |                |     |        |     |       |     |
|          |                  |                           |            |             | E. Baseline | Implementation |                |     |        |     |       |     |
controlfrequencyissetto30Hz.TopLeft:WeapplyGripper
Throughoutthispaper,allpolicyvariants,includingbaseline
| A for brick | sorting | and backpack packing, | while | applying |     |     |     |     |     |     |     |     |
| ----------- | ------- | --------------------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
π
GripperBforboxclosingforthehigherprecisionrequirement. and our policy, are instantiated on pre-trained 0.5 to fairly
|     |     |     |     |     | evaluate | the effectiveness                           |     | of various | post-training |     | strategies. |     |
| --- | --- | --- | --- | --- | -------- | ------------------------------------------- | --- | ---------- | ------------- | --- | ----------- | --- |
|     |     |     |     |     | a)       | π : Thisvariantisfine-tunedonourhumandemon- |     |            |               |     |             |     |
0.5
|     |     |     |     |     | stration       | corpus only | via   | imitation  |       | learning, | without | using |
| --- | --- | --- | --- | --- | -------------- | ----------- | ----- | ---------- | ----- | --------- | ------- | ----- |
|     |     |     |     |     | policy rollout | or          | human | correction | data. |           |         |       |
Optimization is performed using AdamW with a constant b) DSRL: The overall training configurations follow the
learning rate of 1×10−4 after a linear warmup for 2k steps. official implementation of DSRL [80]. We utilize the π
0.5
During inference, we solve the flow ODE using the Euler model[8]asthebasepolicy.Toadaptthepolicy,weinitialize
discrete formulation, with 50 denoising steps. See Table VIII the replay buffer with 10 trajectories collected from the base
for more configurations. policy sampled with standard Gaussian noise w ∼ N(0,I),

GT
RISE (Ours)
RISE
(w/o Task Centric)
RISE
(w/o Pretrain)
Fig. 12: Visual ablation study on training strategies. Compared to the other baselines, which exhibit significant degradation
in image quality and motion coherence, our proposed method generates sharper, physically consistent predictions that strictly
| adhere | to control   | actions. |     |                  |     |     |         |     |            |     |                 |                |     |
| ------ | ------------ | -------- | --- | ---------------- | --- | --- | ------- | --- | ---------- | --- | --------------- | -------------- | --- |
|        | (a) HIL-SERL |          |     | (b) DSRL         |     |     | (c) PLD |     | (d) RECAP  |     | (e) RISE (Ours) |                |     |
|        |              |          |     | Latent Noise (𝑧) |     |     |         |     |            |     |                 | Rollout Policy |     |
Base Policy (𝝅)
Base Policy (𝜋)
|     |     |     |     |     |     |     |     |     |     |     | EMA   | 𝑎   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
Weight
|     |     |     |     |                         |     |     |     |     | 𝑠,𝑟 |     |        |     | 𝑠   |
| --- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
|     |     |     |     | Noise Steering (𝝅steer) |     |     |     |     |     |     | Update |     |     |
Human Correction
|     |     |     |     |     |     |     | Residual Policy(𝝅res) |     |     |     |     | Compositional  |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | -------------- | --- |
Advantage
|     |     |     |     |     |     |     |     |     | Labeling |     |     | World Model |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | ----------- | --- |
𝑠’
|     |     |     |     |                   |     |     | 𝑠,𝑟 |     | Policy (𝝅) |     |     |     |     |
| --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- |
| 𝑠,𝑟 |     | a   |     | Base P o licy (𝜋) |     |     |     |     |            |     |     | 𝑠,𝑟 |     |
𝑎base+𝑎res
|     | RL             |     | 𝑠,𝑟 |                |     | 𝑎   |                |     |                | a   | RL  |     |     |
| --- | -------------- | --- | --- | -------------- | --- | --- | -------------- | --- | -------------- | --- | --- | --- | --- |
|     |                |     |     | R L            |     |     | RL             |     | RL             |     |     |     |     |
|     | Real World Env |     |     |                |     |     |                |     | Real World Env |     |     |     |     |
|     |                |     |     | Real World Env |     |     | Real World Env |     |                |     |     |     |     |
Policy (𝝅)
Fig. 13: Conceptual comparisons with highly-related work. Different from prior works that heavily rely on off-policy
samples from real-world interactions for policy optimization [65, 80, 85, 2], RISE enables on-policy RL by building a world
| model | as an | interactive | environment. |     |     |     |     |     |     |     |     |     |     |
| ----- | ----- | ----------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TABLE VIII: Hyper-parameters of dynamics model. TABLE IX: Hyper-parameters of value model.
| Hyperparameter                         |     |     |     |     |     |     | Value       | Hyperparameter      |     |     |     |     | Value    |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | ----------- | ------------------- | --- | --- | --- | --- | -------- |
| Basics                                 |     |     |     |     |     |     |             | Basics              |     |     |     |     |          |
| Modelinitialization                    |     |     |     |     |     |     | GE-Base[59] | Modelinitialization |     |     |     |     | π0.5 [8] |
| Input/Predictionframes                 |     |     |     |     |     |     | 4/25        | Inputframes         |     |     |     |     | 1        |
| Numberofviews                          |     |     |     |     |     |     |             | 3 Numberofviews     |     |     |     |     | 3        |
| Samplingfrequency(pre-train/Fine-tune) |     |     |     |     |     |     | 30/15Hz     |                     |     |     |     |     |          |
Optimization
| Optimization                       |     |     |     |     |     |     |          | Trainingsteps |     |     |     |     | 50k   |
| ---------------------------------- | --- | --- | --- | --- | --- | --- | -------- | ------------- | --- | --- | --- | --- | ----- |
| Trainingsteps(pre-train/Fine-tune) |     |     |     |     |     |     | 120k/50k | Batchsize     |     |     |     |     | 64    |
| Batchsize(pre-train/Fine-tune)     |     |     |     |     |     |     | 512/64   | Optimizer     |     |     |     |     | AdamW |
2.5×10−5
| Optimizer              |     |           |          |          |     |              | AdamW  | Learningrate        |                  |     |        |                 |       |
| ---------------------- | --- | --------- | -------- | -------- | --- | ------------ | ------ | ------------------- | ---------------- | --- | ------ | --------------- | ----- |
| Learningrate           |     |           |          |          |     |              | 1×10−4 | Valuediscountfactor |                  |     |        |                 | 0.995 |
| Conditionednoiselevelσ |     |           |          |          |     |              | 0.2    |                     |                  |     |        |                 |       |
|                        |     |           |          |          |     |              |        | TABLE X:            | Hyper-parameters | of  | policy | self-improving. |       |
| followed               | by  | 70 online | steering | episodes |     | to fine-tune | the    |                     |                  |     |        |                 |       |
|                        |     |           |          |          |     |              |        | Hyperparameter      |                  |     |        |                 | Value |
behavior.
c) PPO: We initialize the PPO policy via a pre-trained Batchsize 64
|     |     |     |     |     |     |     |     | Optimizer |     |     |     |     | cosine |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | ------ |
π model. At the rollout stage, we sample real-world tra- Learningrate 1×10−4
0.5
jectories, preserving the inference noise and log probabilities Minimumlearningrateratio 0.1
|            |           |     |          |       |        |           |        | Rolloutemadecayrate |     |     |     |     | 0.995 |
| ---------- | --------- | --- | -------- | ----- | ------ | --------- | ------ | ------------------- | --- | --- | --- | --- | ----- |
| calculated | according |     | to RLinf | [91]. | During | training, | we use |                     |     |     |     |     |       |
|            |           |     |          |       |        |           |        | Actionchunksize     |     |     |     |     | 50    |
this stored inference noise to generate on-policy actions with Actiondimension 14
| gradient. | We  | then compute |     | the PPO | loss by | combining | these |     |     |     |     |     |     |
| --------- | --- | ------------ | --- | ------- | ------- | --------- | ----- | --- | --- | --- | --- | --- | --- |
actionswiththenewandoldlogprobabilitiesandadvantages.
| The PPO | policy | is updated |     | by the PPO | loss. |     |     |     |     |     |     |     |     |
| ------- | ------ | ---------- | --- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |

d) DAgger: Due to hardware constraints that pre- XIV. FAILUREMODES
clude high-frequency mode switching, we adopt a single- We depict representative failure behaviors of the RISE
intervention protocol where the human supervisor takes over policy in Fig. 18. In Dynamic Brick Sorting, failures stem
uponimminentfailureandcompletestheepisode.Thisvariant from temporal inconsistency, manifesting as tracking failure
istrainedonbothexpertdemonstrationsandadditionalhuman or grasp slippage, alongside classification noise. In Backpack
correction data via imitation learning. Packing,highdeformabilityinducesstowingfailureandlifting
e) RECAP: This variant follows the recipe of the policy
instability, while surface compliance leads to zipper stuck
warm-up stage, detailed in Sec. XI-D.
or miss. In Box Closing, tight geometric tolerances cause
XII. CONCEPTUALCOMPARISONSWITH incompleteloading,whereasbi-manualsynchronizationerrors
HIGHLY-RELATEDWORK result in flap misalignment or tab deformation.
We conceptually compare our method with highly-related XV. ADDITIONALRELATEDWORKONVLAMODELS
work in Fig. 13. Contrary to prior methods that learn from
One recent breakthrough in robot learning is the VLA
off-policy data through costly real-world interactions, RISE
framework that integrates general-purpose vision-language
enableson-policyreinforcementlearningwithalearnedworld
modelswithlow-levelroboticcontrol.Buildingoffpre-trained
modelthatgeneratesnewstatesandassignsadvantageforeach
vision-language models, RT2 [102] and OpenVLA [46] rep-
action chunk.
resent actions as discretized bins following the training pro-
XIII. QUALITATIVEVISUALIZATIONS cedure of language models. OpenVLA-OFT [47] parallelizes
Compositional World Model. We visualize rollout trajecto- the decoding process of chunked actions to improve inference
latency.Toovercomethemulti-modalityissueofrobotactions
ries conditioned on distinct action sequences. As shown in
where a variety of actions are correlated with the same state,
Fig. 16, the dual-arm robot starts with the left arm grasping
GR00T [6], π-series [7, 8, 2], and RDT [62] further incorpo-
a blue brick. The expert trajectory executes a smooth pick-
rate action generation with diffusion or flow matching-based
and-place operation into the target (blue) box, accompanied
architecture inspired by diffusion policy [18]. The massive
byanincreasingrewardcurve.Similarly,therolloutdrivenby
trainingofthesemodelsisprimarilysupportedbyteleoperated
optimized actions exhibits a comparable trend. Notably, the
robot datasets [71, 11, 43]. Other data corpora derived from
generated video maintains high fidelity, accurately capturing
simulators [70, 53], wearable devices [19, 83], neural synthe-
complex environmental dynamics such as the operating con-
sis [41], and generic internet [101] are also considered for the
veyor belt. The corresponding reward curve shows improve-
lack of costly real-world robot data. Effective approaches are
ment but remains slightly below the expert baseline, likely
proposedtoincorporateheterogeneousdatasourcesuniformly,
due to minor deviations in the optimized actions or subtle
even without sufficient action labels [12, 89, 42]. Despite
visual artifacts in the imagination. In contrast, the suboptimal
advanced architecture and data scaling, VLAs still struggle
trajectory clearly depicts the arm misplacing the brick into
with complex manipulation that requires high dexterity and
thewrong(yellow)box.Consequently,therewardrisesduring
precision [85, 25, 2], where our self-improving approach
the picking phase but drops significantly once the arm moves
excels.
toward the incorrect target. These results demonstrate the
reliabilityofourworldmodelincapturingbothvisualrealism XVI. LICENSEOFASSETS
and logical consistency.
Our dynamics model is built on pre-trained Genie Envi-
DynamicsModel.Weprovideacomprehensivevisualassess-
sioner [59] under the Apache License 2.0. The pre-training
ment to benchmark our dynamics model against state-of-the-
of our dynamics model leverages two large-scale public
art alternatives. As shown in Fig. 20, our method distinctly
datasets, where Agibot World [11] is under CC BY-NC-SA
outperformsotherapproaches,particularlyinmaintaininghigh
4.0 and Galaxea [43] is under Apache-2.0 license. Some
image quality and precise action alignment. Extending this
comparisons of the dynamics model are conducted on the
analysis, Fig. 10 and Fig. 19 present additional multi-view
Bridge dataset [81] under Creative Commons Attribution 4.0
rollouts across real-world tasks, as well as the Galaxea and
International License. Additionally, Cosmos-Predict2.5 [1] is
Agibot World environments, confirming our model’s consis-
applied as a baseline under the Apache License 2.0. Both our
tency in complex domains.
policy and value model are initialized from the pre-trained
ValueModel.Weshowcasethepredictedvaluetrajectoryover
π [8] under the Apache License 2.0.
0.5
time alongside corresponding visual observations in Fig. 14.
Greenregionsindicatesuccessfulexecution,whileredregions XVII. BROADERIMPACT
highlight inferior or suboptimal actions. The value model Overall, this work contributes to a growing vision of robots
assigns increasing scores during successful executions (e.g., that learn continuously and efficiently by reasoning about the
accurate sorting, stable grasping, and successful cover clo- consequences of their actions via imagination. By improving
sure), while degrading when subtle failures occur, such as robustness without excessive physical data collection costs,
missed grasps, failure to release, or the cover getting stuck. this work may contribute to safer and more reliable robotic
Moreover, we visualize the impact of each loss for training systems that assist humans in physically demanding or haz-
value model in Fig. 15. ardous tasks.

Pushing down the cover
|     | Accurate sorting |     |     | Succesful grasping |
| --- | ---------------- | --- | --- | ------------------ |
Failed to grasp [Top-view] Failed to release Cover gets stuck
Fig. 14: Qualitative visualizations of value prediction on real-world data. Our value model is capable of distinguishing
| success | and failure, highlighted | in green | and red, respectively. |     |
| ------- | ------------------------ | -------- | ---------------------- | --- |
Tucking the boxcover Retrying to insert the tab
(a) Progress only (b) TD learning only (c) TD learning + Progress (Ours)
Fig. 15: Qualitative ablation of value model. This visualization ablates the effectiveness of imposing each loss during the
training of the value model. Green and gray regions highlight the favorable and retrying behaviors, respectively. In the green
region, (b) exhibits a stronger capability in detecting critical steps, compared to (a) progress only variant, where the result is
simply monotonic. However, (b) is less numerically stable compared to (a), as depicted in the gray region. We jointly apply
| two losses | to feature both | visual sensitivity | and numerical | stability. |
| ---------- | --------------- | ------------------ | ------------- | ---------- |

| Initial State |     | Step 10 |     | Step 20 |     | Step 30 | Step 40 |     |
| ------------- | --- | ------- | --- | ------- | --- | ------- | ------- | --- |
Expert Trajectory
WM Rollout 1
WM Rollout 2
Fig. 16: Multiple rollouts from the same initial state. Left: Starting from the same state where the gripper grasps a blue
brick, our world model can synthesize outcomes that accurately follow different actions. Top Row: Expert demonstration for
reference. Middle Row: Imagined rollout of successful action that correctly put the blue brick into the blue basket, where the
rewards go positive. Bottom Row: Imagined rollout of failed action that mistakenly put the blue brick into the yellow basket,
| where the     | rewards become | negative.      |     |      |                                          |     |                 |     |
| ------------- | -------------- | -------------- | --- | ---- | ---------------------------------------- | --- | --------------- | --- |
| Initial State |                |                |     |      | Pick and Sort Bricks on Running Conveyor |     |                 |     |
| Initial State |                | Put Clothes in |     | Lift |                                          |     | Zip up Backpack |     |
Initial State Load Cup Fold Side Flaps Fold Rear Flap Tuck Locking Tab
Fig. 17: Policy rollout. RISE demonstrates robust performance across diverse manipulation regimes. Top: Handling dynamic
scenes by sorting bricks on a moving conveyor. Middle: Manipulating deformable objects in the Backpack Packing task.
| Bottom: Achieving  |                     | high-precision | bi-manual           | control           | in Box Closing.  |     |                      |                 |
| ------------------ | ------------------- | -------------- | ------------------- | ----------------- | ---------------- | --- | -------------------- | --------------- |
|                    | Incorrect Placement |                |                     |                   | Tracking Failure |     |                      | Grasp Slippage  |
| Stowing Failure    |                     |                | Lifting Instability |                   |                  |     | Zipper Stuck or Miss |                 |
| Incomplete Loading |                     |                |                     | Flap Misalignment |                  |     |                      | Tab Deformation |
Fig. 18: Failure modes during inference. Top: Failures typically involve temporal inconsistency in tracking moving objects
or precise grasping errors. Middle: The high deformability can lead to incomplete cloth insertion or slippage during the lifting
and zipping stages. Bottom: Slight misalignments during bi-manual coordination can cause the cup to tip over during loading
| or result in | unsuccessful | folding | and tucking. |     |     |     |     |     |
| ------------ | ------------ | ------- | ------------ | --- | --- | --- | --- | --- |

Fig. 19: Dynamics model rollouts. Each video clip is ordered top to bottom.
G
T
R EPE: 1.141
SI
E
O(
u
sr
) EPE: 2.914
C
o
s
m
o
s
EPE: 2.952
G
e
n
ei
b-
a
s
e
(a) RGB frames (b) Visualized Optical Flow
G
T
R
SI
E
O(
u
sr
)
C
o
s
m
o
s
G
e
n
ei
b-
a
s
e
(c) Comparison on Bridge Dataset
Fig. 20: Comparisons with other generative counterparts.