AlphaNIST: Emergent Assembly Skills from Binary Task Rewards
Octi Zhang1, Iretiayo Akinola1, Rosario Scalise2, Mateo Guaman Castro2, Patrick Yin1,2
Tobias Widmer1, Miles Macklin1, Chris Amevor1, Dylan Turpin1, Dirk Van Gelder1
Jan Carius1, Ankur Handa1, Gavriel State1, Yunrong Guo1, and Yashraj Narang1
1NVIDIA 2University of Washington
Fig.1. Emergentmulti-componentassemblywithasinglepolicy.Trainedwithabinarytaskreward,AlphaNISTlearnstoselect,grasp,reorient,and
assemble diverse components, while autonomously sequencing multiple assemblies within a single episode. Shown are snapshots from a ten-component
assemblysequence.
Abstract—The NIST Assembly Task Board #1 remains a key reasons: (1) The sequence for solving the tasks might
challenging benchmark for learning-based methods in robotic be unspecified, and not all sequences may be efficient or
manipulation.Overshorthorizons,itdemandsprecise,contact-
valid (e.g., solving task N may obstruct the robot from
rich control of small, tight-fitting parts. Over long horizons,
accessing the parts in task N + 1). (2) Each task is long-
it requires recovery and coordination across extended action
sequences. Demonstrations, task decomposition, and dense horizon, encompassing grasping, transport, and contact-rich
progressrewardshaveenabledresearchadvancesbyproviding assembly [2]. Parts may begin in a wide range of poses
guidance on how to assemble. But how much of the strategy and require multiple reorientations before grasping. During
must be specified? The progression from AlphaGo to AlphaGo
transport, parts may need further reorientation in-hand or
ZeroshowedthatRLatscalecandiscoversuperhumanstrate-
through extrinsic contact. During assembly, parts may slip,
gies without prescribing how to win. AlphaNIST asks whether
a sparse binary task reward and task diversity admitted by becomemisaligned,orjamduringinsertionorthreading[2],
this task-agnostic reward can similarly let a robot discover requiring robust recovery and reexecution. (3) Solving the
how to assemble. In simulation, we train a single policy from tasks requires precise control during complex contact inter-
scratch across all 20 assembly tasks on the NIST Assembly
actions.Thepartsthemselvesaresmall(assmallas4mmin
TaskBoard#1,reaching98.2%overalltrainingsuccesswithout
diameter), have high geometric detail (e.g., helical threads),
demonstrations, progress shaping, scripted primitives, or per-
task tuning. The framework also trains policies to complete and have tight clearances between mating surfaces (as low
ten assembly pairs in a single episode without a prescribed aszero).Taskssuchasnutthreadinginvolvelearninghelical
order, with task success rewarded only when all ten pairs motion during frictional contact between multiple mating
are simultaneously complete. The learned policies discover
surfaces, during which a nut can tilt, cross-thread, or jam
dexterousandplanning-likebehaviors:choosinggraspsforlater
instead of advancing along the bolt [2].
assembly, using surrounding geometry to reorient parts, and
preparingonepart,assemblinganother,thenreturningtofinish Learning-free approaches typically rely on planning and
thefirstwithoutanexplicitplanner.Forvideos,seeourwebsite:
strong human priors: assembly sequence planning [3]; cus-
https://alpha-nist.github.io/
tomized fixtures, adapters, and tooling [1], [4]; engineered
I. INTRODUCTION motion and force primitives [5]; and tuned admittance,
impedance, or force-motion controllers [4], [5].
Robotic assembly is a longstanding challenge, and the
NISTAssemblyTaskBoardsareapersistentbenchmark[1]; Learning-based approaches, on the other hand, can relax
to the best of our knowledge, no learning-based approaches some of these constraints, but have shown progress only
have solved all tasks on any of the boards. Assembly Task within a limited scope. Most efforts have assumed a fixed
Board #1 (ATB1) consists of 20 assembly pair tasks (a assembly sequence, heavily constrained the initial poses
part and its fixed mating geometry on the board) that are of parts (e.g., beginning in an already-grasped state) [6],
relevant for manufacturing, including peg insertion, gear assumedaccesstoaccurateposeestimates,learnedspecialist
meshing, electrical connector insertion, and nut threading. rather than multi-task policies [2], addressed only a subset
Solvingthistaskboardisexceptionallychallengingforthree of tasks on the board [6], and/or achieved only low-to-
6202
tcO
9
]IA.sc[
1v45331.0162:viXra

2) Thefirstmulti-taskRLpolicycapableofsolvingall
|     |     |     |     |     |     |     |     | 20         | tasks   | on the | NIST Assembly |           | Task      | Board | 1. The  |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | ------ | ------------- | --------- | --------- | ----- | ------- |
|     |     |     |     |     |     |     |     | policy     | takes   | point  | clouds        | as input; | initial   | part  | poses   |
|     |     |     |     |     |     |     |     | are        | sampled | from   | a wide        | range,    | including |       | adverse |
|     |     |     |     |     |     |     |     | conditions |         | (e.g., | upside-down); |           | and each  | task  | can be  |
solvedwithnear-perfectsuccessrates.Positivetransfer
isobserved,wheremulti-taskpoliciescansolvethe20
|     |     |     |     |     |     |     |     | tasks | with      | higher | success | rate than | individual  |     | special- |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --------- | ------ | ------- | --------- | ----------- | --- | -------- |
|     |     |     |     |     |     |     |     | ists, | including | three  | tasks   | that the  | specialists |     | struggle |
to solve.
|             |          |      |          |      |       |       |             | 3) The | first      | assembly | policy | capable |              | of solving | up      |
| ----------- | -------- | ---- | -------- | ---- | ----- | ----- | ----------- | ------ | ---------- | -------- | ------ | ------- | ------------ | ---------- | ------- |
|             |          |      |          |      |       |       |             | to     | 10 diverse | assembly |        | pairs   | in sequence, |            | without |
| Fig. 2. The | complete | NIST | Assembly | Task | Board | #1 in | simulation. |        |            |          |        |         |              |            |         |
Yellowindicatesthe20movablepartsintheirfully-assembledstates. an explicit hierarchy or prescribed task order. Thus,
|     |     |     |     |     |     |     |     | this | work | demonstrates |     | that sequencing |     | behavior | can |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ------------ | --- | --------------- | --- | -------- | --- |
moderate success rates by industrial standards. Success- emerge within a single low-level assembly policy.
| Guided Sampling |     | (SGS)    | [7],       | for example, |        | solves   | tasks one |            |     |              |     |        |          |           |     |
| --------------- | --- | -------- | ---------- | ------------ | ------ | -------- | --------- | ---------- | --- | ------------ | --- | ------ | -------- | --------- | --- |
|                 |     |          |            |              |        |          |           | We observe |     | a repertoire | of  | unique | emergent | behaviors |     |
| at a time,      | but | requires | a separate |              | policy | per task | and is    |            |     |              |     |        |          |           |     |
includingdexterousskillssuchaspushingandsliding(tosin-
| considerably | less | compute-efficient. |     |     |     |     |     |                |         |           |     |          |            |           |     |
| ------------ | ---- | ------------------ | --- | --- | --- | --- | --- | -------------- | ------- | --------- | --- | -------- | ---------- | --------- | --- |
|              |      |                    |     |     |     |     |     | gulate parts), | in-hand | pivoting, |     | multiple | sequential | regrasps, |     |
WedrawinspirationfromthelandmarkAlphaGoseriesin extrinsic contact (to reorient parts prior to insertion), and
reinforcementlearning,whichsurpassedthestrongesthuman
|     |     |     |     |     |     |     |     | single-gripper |     | nut threading. | The | single | policy | also | exhibits |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | -------------- | --- | ------ | ------ | ---- | -------- |
Goplayers.TheprogressionfromAlphaGotoAlphaGoZero
|           |               |      |                 |          |      |           |          | long-horizon            | planning-like |             | behavior | such      | as     | bringing    | parts |
| --------- | ------------- | ---- | --------------- | -------- | ---- | --------- | -------- | ----------------------- | ------------- | ----------- | -------- | --------- | ------ | ----------- | ----- |
| showed    | that learning | from | a               | terminal | task | objective | could    |                         |               |             |          |           |        |             |       |
|           |               |      |                 |          |      |           |          | into reach,             | moving        | obstructing |          | parts     | aside, | and leaving | a     |
| encourage | superhuman    |      | decision-making |          | over | long      | horizons |                         |               |             |          |           |        |             |       |
|           |               |      |                 |          |      |           |          | task partially-finished |               |             | and then | returning | to     | it later.   | None  |
without human demonstrations [8], [9]. In this paper, we of these skills and behaviors were specified. We encourage
| ask whether | a      | similar | approach | is       | possible | for  | robotics:   |            |          |                   |            |        |     |                |         |
| ----------- | ------ | ------- | -------- | -------- | -------- | ---- | ----------- | ---------- | -------- | ----------------- | ---------- | ------ | --- | -------------- | ------- |
|             |        |         |          |          |          |      |             | readers to | watch    | our supplementary |            | videos | 1   | for additional |         |
| can sparse  | binary | task    | rewards, | combined |          | with | appropriate |            |          |                   |            |        |     |                |         |
|             |        |         |          |          |          |      |             | examples   | of these | emergent          | behaviors. |        | We  | plan to        | release |
trainingstrategies,enablearobottosolvesequencesoflong-
|          |              |              |     |        |         |     |            | our code | following | the | review | and revision | period. |     |     |
| -------- | ------------ | ------------ | --- | ------ | ------- | --- | ---------- | -------- | --------- | --- | ------ | ------------ | ------- | --- | --- |
| horizon, | contact-rich | manipulation |     | tasks, | perhaps |     | leveraging |          |           |     |        |              |         |     |     |
dexterous behaviors that no human could feasibly specify II. RELATEDWORK
| or demonstrate? |     | To make | learning | from | sparse | task | rewards |     |     |     |     |     |     |     |     |
| --------------- | --- | ------- | -------- | ---- | ------ | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
more tractable, we take a seemingly counterintuitive step: A. Scalable Learning for Contact-Rich Assembly
train jointly across heterogeneous assembly pairs differing Parallel physics simulation supports experience collection
| in geometries, | tolerances, |     | and | assembly | requirements |     | (a nut |          |               |         |     |         |           |       |      |
| -------------- | ----------- | --- | --- | -------- | ------------ | --- | ------ | -------- | ------------- | ------- | --- | ------- | --------- | ----- | ---- |
|                |             |     |     |          |              |     |        | at scale | for on-policy | methods |     | such as | PPO [11], | [12], | with |
anditsbolt,agearanditsgearshaft,apeganditshole)from
|     |     |     |     |     |     |     |     | applications | ranging | from | dexterous |     | in-hand | manipulation |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | ---- | --------- | --- | ------- | ------------ | --- |
abroadcoverageofinitialstates,convertingMDPdiversity [13],[14],[15],[16]toindustrialassembly.GPU-accelerated
| into a resource |     | rather | than | a burden. |     |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | ------ | ---- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
physicsenginessuchasPhysX[17]andNewton[18]support
Guidedbythisinsight,wedevelopAlphaNIST,alearning large-scale parallel simulation for robot learning. For indus-
framework that trains a single policy under sparse binary trial assembly, Factory [2] demonstrated real-time or faster
| task rewards | across | all | 20  | tasks on | the | NIST | Assembly |            |     |                    |     |              |     |              |     |
| ------------ | ------ | --- | --- | -------- | --- | ---- | -------- | ---------- | --- | ------------------ | --- | ------------ | --- | ------------ | --- |
|              |        |     |     |          |     |      |          | simulation | of  | 1,000 simultaneous |     | nut-and-bolt |     | interactions |     |
Task Board 1 (Fig. 2). The policy handles an exceptional in Isaac Gym, later incorporated into Isaac Lab. AlphaNIST
| range of | initial | part poses, | learns | from | point-cloud |     | inputs |           |            |            |     |            |            |     |        |
| -------- | ------- | ----------- | ------ | ---- | ----------- | --- | ------ | --------- | ---------- | ---------- | --- | ---------- | ---------- | --- | ------ |
|          |         |             |        |      |             |     |        | uses this | simulation | throughput |     | to collect | experience |     | across |
withoutfirsttrainingspecialistpolicies,andachievesa98.2% heterogeneous assembly pairs.
| overall success |     | rate. Furthermore, |     | the      | same  | framework | can       |                      |      |           |               |          |              |     |          |
| --------------- | --- | ------------------ | --- | -------- | ----- | --------- | --------- | -------------------- | ---- | --------- | ------------- | -------- | ------------ | --- | -------- |
|                 |     |                    |     |          |       |           |           | OmniReset            | [10] | addressed | state         | coverage | through      |     | diverse, |
| train policies  | to  | complete           | 10  | assembly | pairs | in        | sequence, |                      |      |           |               |          |              |     |          |
|                 |     |                    |     |          |       |           |           | manipulation-centric |      | resets,   | demonstrating |          | long-horizon |     | on-      |
with a task reward issued only when all pairs are assembled policy RL with fixed algorithm hyperparameters and no
withnoprescribedorder.Inotherwords,thepolicyexhibits
|     |     |     |     |     |     |     |     | curricula | or human | demonstrations. |     | Success-Guided |     |     | Sam- |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------- | --------------- | --- | -------------- | --- | --- | ---- |
planning-like behavior. pling (SGS) [7] addressed experience allocation by con-
Our contributions are the following: centrating simulation near the policy’s changing capability
1) A highly-effective multi-task RL framework con- frontier, scaling beyond one million parallel environments
sisting of a novel combination of the following com- using sparse rewards. In its reported assembly experiments,
ponents:A)generationofacacheofassembly-relevant
SGStrainsaseparatepolicyforeachsingletask.AlphaNIST
resetstates[10]overheterogeneousassemblypairs,B) retains SGS’s sampling rule but trains one multi-task policy
success-guidedsamplingwithinthecache[7],C)auni- acrossall20ATB1tasksunderacommonbinarytaskreward.
fied sparse binary task reward, D) multi-GPU training Our experiments show that this shared policy learns assem-
at scale. These components are supported by careful blies that remain unsolved in single-task training (Fig. 5).
| ablations. |          | All tasks | share  | one                | training | configuration, |     |                                |     |     |     |     |     |     |     |
| ---------- | -------- | --------- | ------ | ------------------ | -------- | -------------- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- |
| without    | per-task |           | tuning | or demonstrations. |          |                |     | 1https://alpha-nist.github.io/ |     |     |     |     |     |     |     |

B. Multi-Task Reinforcement Learning rich control, with one shared policy learning heterogeneous
assemblies end to end.
Multi-taskRLaimstoimprovelearningbysharingexperi-
ence across tasks. However, standard joint-training baselines
III. PROBLEMFORMULATION
have achieved lower success rates than separately trained
policies on multi-task manipulation benchmarks [19]. One A. Task Definition and MDP
approach to obtaining a single multi-task policy is to distill We formulate all 20 ATB1 assembly tasks [1] as a multi-
multiple separately trained specialists into a shared pol- task reinforcement-learning problem with one shared policy.
icy [20]. Other approaches address the difficulty of joint Let e ∈ E denote an assembly task, with |E| = 20. Each
training directly. PopArt [21] addresses differences in re- task corresponds to one assembly pair: a movable part, its
ward scales with a separate value output and normaliza- mating geometry, and a fully-assembled configuration.
tion statistics for each task, while PCGrad [19] removes We model the problem as a finite-horizon MDP,
conflicting components of task gradients before combining
them. However, Kurin et al. [22] show that shared-network M=(S,A,p,r,γ,T,ρ), (1)
baselines with standard regularization and stabilization can
where p(s | s ,a ) is the transition kernel and ρ is the
match specialized multi-task optimizers. t+1 t t
joint distribution over task identities and initial states. At
AlphaNISTtakesasimpleapproachtomulti-tasklearning
the beginning of each episode, (e,s )∼ρ. A shared policy
by exploiting the shared structure of assembly: threading, 0
π (a | o ) acts on partial observations o of the simulator
gear meshing, and insertion all receive the same binary task θ t t t
state s and maximizes
reward when assembly error falls below a common thresh- t
old. Under this shared objective, we train one geometry- (cid:34)T−1 (cid:35)
(cid:88)
conditioned policy and one value function with standard J(θ)=E ρ,p,πθ γtr t . (2)
PPO at scale, without task-specific value heads, gradient t=0
projection, or specialist pretraining. Task variation is represented through surface point clouds in
o , rather than an explicit discrete task identifier.
t
C. Learning-Based Robot Assembly
IV. METHOD
Prior learning-based assembly systems make exploration
tractable by shortening the task horizon or restricting initial- A. AlphaNIST Training Framework
ization to staged, pre-grasped, or local-insertion problems
AlphaNIST trains one policy across all 20 assembly
[23], [24]. Factory [2] trains separate pick, place, and screw
tasks with standard PPO and a binary task reward for
subpolicies, while AutoMate [20] combines assembly-by-
completed assembly. Its training distribution combines di-
disassembly, imitation learning, and curriculum-based RL
verse cached reset states from OmniReset [10] with beta-
to obtain specialist and generalist assembly policies. Refin-
distributedsuccess-guidedsampling(SGS)[7],whileacom-
ery [25] improves pretrained assembly specialists through
mon binary task reward defines successful assembly across
Bayesian-optimization-guided sampling of initial conditions
all tasks. The three components play distinct roles:
during fine-tuning and Gaussian-mixture-model-based ini-
tialization at deployment. The refined policies can then
Reset bank: Which states are available?
be chained to complete multi-part assemblies. For longer
Beta sampling: Which states are sampled?
sequences, ARCH [26] uses a high-level imitation-learned
Binary task reward: What counts as success?
policy to select from a library of RL and model-based
primitives. These methods structure learning through ini-
B. Reset Coverage and Experience Allocation
tialization,demonstrations,orprescribedsubskills.OmniRe-
We adapt OmniReset [10] to heterogeneous assembly by
set [10] uses a generic dense objective with fixed weights,
caching the assembly identity together with each reset state:
including gripper–object and object–goal distance terms.
Zhang et al. [7] present the first end-to-end RL solution to D ={(e ,s¯)}M . (3)
individualtasksfromtheNISTATB1,butretaintask-specific reset i i i=1
auxiliary grasp- and gripper-related shaping. Such terms can Here, M is the total number of entries across all 20
aid exploration and discourage reward exploitation, but their assemblies. The assembly identity e selects the part and
i
relativeinfluencecanchangewithobjectsize,geometry,and mating-geometryassetsandtheirinertialproperties,whiles¯
i
assembly motion. Even with fixed coefficients, a new task specifies the robot, board, and movable-part state. Sampling
family requires checking that the shaped reward remains an entry therefore selects both the assembly and its initial
aligned with successful assembly. configuration. The cached bank spans ungrasped workspace,
AlphaGo Zero provides a broader motivation: terminal pickup, transport, near-mating, and partially assembled con-
win/lossandsearch-generatedpolicytargetssupportstrategy figurations (Fig. 4), enabling GPU-parallel initialization.
discovery without human game data or intermediate reward These reset families define regions of the training distribu-
shaping[9].AlphaNISTaskswhetherbinarytasksuccesscan tion, not a prescribed sequence; the policy receives no stage
similarly support strategy discovery in continuous, contact- identifier.

|     |     |     |                     |     |        | identity  |           |     | identity  |        |     |                     |     |     |
| --- | --- | --- | ------------------- | --- | ------ | --------- | --------- | --- | --------- | ------ | --- | ------------------- | --- | --- |
|     |     |     |                     |     | linear | LN linear | SW linear | LN  | linear SW | linear | LN  | linear              |     |     |
|     |     |     | two-layerELUencoder |     |        |           |           |     |           |        |     | Gaussianactionat∈R8 |     |     |
|     |     |     |                     |     |        |           | +         |     |           |        | +   |                     |     |     |
Pointcloud
|     |     |        |     |     |     |      |     |     |      |     |     |     | arm∆q1:7 | gripper |
| --- | --- | ------ | --- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- | -------- | ------- |
|     |     |        |     |     | 256 | 1024 | 256 |     | 1024 | 256 |     | 8   |          |         |
|     |     | 3×npts | 256 | 128 |     |      |     |     |      |     |     |     |          |         |
∥
RN
|     |     |     |     |     |     | identity |     |     | identity |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | -------- | --- | --- | --- | --- | --- |
Proprioception
+lastaction 278 linear LN linear SW linear LN linear SW linear LN linear
pose7|twist6|
joints9|action8
|     |     |     |     |     |     |      | +   |     |      |     | +   |     | valueVϕ(ot)∈R |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- | ------------- | --- |
|     |     |     | 150 | 150 |     |      |     |     |      |     |     |     |               |     |
|     |     |     |     |     | 256 | 1024 | 256 |     | 1024 | 256 |     | 1   |               |     |
Fig. 3. Policy architecture. Actor and critic have the same architecture with separate parameters. Inputs are drawn once; each network contains two
consecutiveresidualblocks.RN:runningnormalization;LN:layernormalization;SW:Swishactivation;npts:numberofinputpoints.
|     |     |     |     |     |     |     | where     | ϵ =     | 0.001m.       | The success |              | reward      | is issued   | once,    |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------- | ------------- | ----------- | ------------ | ----------- | ----------- | -------- |
|     |     |     |     |     |     |     | and the   | episode | terminates.   |             | Intermediate |             | progress    | receives |
|     |     |     |     |     |     |     | no task   | reward. | We supplement |             | the          | binary      | task reward | with     |
|     |     |     |     |     |     |     | a control | cost    | to discourage |             | large action | magnitudes, |             | rapid    |
jointmotion,andexcessivetorque.Thisregularizationbiases
|     |     |     |     |     |     |     | learning | toward                               | smoother,   | lower-effort    |                    | behaviors |           | that are |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------------------------------ | ----------- | --------------- | ------------------ | --------- | --------- | -------- |
|     |     |     |     |     |     |     | more     | compatible                           | with        | safe deployment |                    | on        | physical  | robots,  |
|     |     |     |     |     |     |     | without  | providing                            | information |                 | about              | assembly  | progress. |          |
|     |     |     |     |     |     |     |          |                                      |             | (cid:0)         |                    |           | ∥2(cid:1) |          |
|     |     |     |     |     |     |     | r =      | rsucc                                | −c          | ∥a ∥2+∥q˙       |                    | ∥2+∥τ     | ,         | c≥0.     |
|     |     |     |     |     |     |     | t        | t                                    |             | t               | 2                  | t 2       | t 2       |          |
|     |     |     |     |     |     |     |          | (cid:124)(cid:123)(cid:122)(cid:125) |             | (cid:124)       | (cid:123)(cid:122) |           | (cid:125) |          |
|     |     |     |     |     |     |     |          | binarytaskreward                     |             |                 | controlcost        |           |           |          |
(6)
|     |     |     |     |     |     |     | Here,   | a , q˙ , | and τ are | the action, |           | robot joint | velocity,     | and |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | --------- | ----------- | --------- | ----------- | ------------- | --- |
|     |     |     |     |     |     |     |         | t t      | t         |             |           |             |               |     |
|     |     |     |     |     |     |     | applied | joint    | torque.   | The control | penalties |             | are evaluated | at  |
everystep,withasinglecoefficientcfixedacrosstasks.They
Fig. 4. Diverse assembly reset states. Examples of resets across tasks, do not measure assembly progress; the binary task reward
rangingfromrandomobjectposestoin-handgraspsandpartialassemblies. specifies successful completion. Episodes end on assembly
|     |     |     |     |     |     |     | success, | at horizon | T,  | or when | an  | arm | joint exceeds | its |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | --- | ------- | --- | --- | ------------- | --- |
Letpˆ betheempiricalsuccessrateoverthemostrecentL hardware velocity or torque limit. In multi-pair episodes,
i
episodesinitializedfromentry(e ,s¯).Underbetasampling, the success reward remains zero until every active pair is
|     |     |     |     | i i |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
entry i is selected with probability q i : assembled, with no prescribed pair order or intermediate
|     |     |     |     |     |     |     | completion | reward. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- |
(cid:112)
|                                    | q ∝ε | +   | pˆ(1−pˆ), | i=1,...,M,     |                   |          | (4)       |           |           |       |          |     |           |      |
| ---------------------------------- | ---- | --- | --------- | -------------- | ----------------- | -------- | --------- | --------- | --------- | ----- | -------- | --- | --------- | ---- |
|                                    | i    | q   | i         | i              |                   |          |           |           |           |       |          |     |           |      |
|                                    |      |     |           |                |                   |          | D. Shared | Policy    | and       | Robot | Control  |     |           |      |
| normalized                         | over | the | entire    | bank. Sampling | i                 | ∼ Cat(q) |           |           |           |       |          |     |           |      |
|                                    |      |     |           |                |                   |          | We        | implement | AlphaNIST |       | in Isaac | Lab | [11] with | GPU- |
| selectsanassembly–resetpairwithρ(e |      |     |           |                | ,s¯)=q .Thekernel |          |           |           |           |       |          |     |           |      |
i i i parallel environments. Each PPO batch combines rollouts
| favors      | intermediate  | success    | rates,    | while     | ε >0 keeps        | every  |                                                      |             |            |               |                  |           |            |           |
| ----------- | ------------- | ---------- | --------- | --------- | ----------------- | ------ | ---------------------------------------------------- | ----------- | ---------- | ------------- | ---------------- | --------- | ---------- | --------- |
|             |               |            |           |           | q                 |        | fromassembly–resetpairssampledusingEq.(4).Thepolicy, |             |            |               |                  |           |            |           |
| entry       | sampleable.   | Each       | episode’s | outcome   | updates           | pˆ i   | for                                                  |             |            |               |                  |           |            |           |
|             |               |            |           |           |                   |        | reward,                                              | controller, | and        | training      | configuration    |           | are        | shared    |
| its sampled | entry.        | The        | uniform   | ablation  | sets q            | = 1/M; |                                                      |             |            |               |                  |           |            |           |
|             |               |            |           |           | i                 |        | across                                               | all 20      | tasks. The | policy        | observes         | the       | robot      | state and |
| the         | bank, policy, | reward,    | and       | optimizer | remain unchanged. |        |                                                      |             |            |               |                  |           |            |           |
|             |               |            |           |           |                   |        | surface                                              | point       | clouds of  | the movable   |                  | part,     | mating     | geometry, |
| Algorithm   | 1             | summarizes | training. |           |                   |        |                                                      |             |            |               |                  |           |            |           |
|             |               |            |           |           |                   |        | and robot,                                           | without     | a discrete |               | task identifier. |           | We use     | separate  |
|             |               |            |           |           |                   |        | actor and                                            | critic      | SimBa      | networks      | [27],            | [28],     | summarized | in        |
| C. Binary   | Full-Assembly |            | Objective |           |                   |        |                                                      |             |            |               |                  |           |            |           |
|             |               |            |           |           |                   |        | Fig. 3.                                              | Each        | combines   | a point-cloud |                  | embedding |            | with the  |
Across geometries, the assembly objective is the same: proprioception and last action shown in the figure.
complete the assembly. For each instance, an assembly- We simulate a 7-DoF Franka Emika Panda with identified
relative coordinate Φ (α), α∈[0,1], parameterizes the part inertial and drivetrain parameters and a parallel-jaw gripper
e
inthematingframe,withΦ (1)denotingitsfullyassembled withonedrivenandonemechanicallycoupledpassivefinger.
e
pose. Let de (s) be the distance between the part’s current At25Hz,thepolicyoutputsa7Drelativejointpositiontarget
asm
relativeposeandΦ (1).Forasingle-pairepisode,thebinary (qtarget =q +∆q )anda1Dgrippercommand.Animplicit
|     |     | e   |     |     |     |     | t   | t   | t   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
task reward is impedance controller uses the manufacturer’s libfranka stiff-
(cid:40) ness and damping profile with hardware-matched armature
de
1, (s t+1 )<ϵ, and joint friction. Joint-speed limits are 2.175rad/s for
|     |     | rsucc = |     | asm |     |     | (5) |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
t
0, otherwise. joints 1–4 and 2.61rad/s for joints 5–7; torque limits are

(a) Success by task
(b) Success rate ± standard deviation
100
98.2± 0.986%
100
Shared policy
|     | Sparse reward |     |     |     |     |     |     |     | 81.4± 1.732% |     |     |     |     |     |
| --- | ------------- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
78.3± 0.573%
75
| Separate policies |     |     |     |     | )%( sseccuS |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Sparse reward
50
50
Shared policy
Dense reward
17.8± 0.010%
25
Separate policies
Dense reward
|     |     |     |     |     | 0   | 0   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
N 4 N 8 1 2 1 6Gs mGl R 4 R 8 1 2 1 6 P 4 P 8 1 2 1 6 S B W P N C D SRJ Shared Separate Shared Separate
N N G R R P P U B Sparse reward Sparse reward Dense reward Dense reward
Fig.5. Training across heterogeneous assembly pairs substantially improves learning from a sparse binary task reward.At64Kenvironments
across25kiterations:(a)compares20-tasksuccessratesforonesharedpolicyversus20separatelytrainedpolicies.Thesharedpolicy(firstrow)achieved
above98% successrate acrossall tasks,includingthree precisionassemblies thatcorrespondingspecialists rarelysolve. Denseshapingdoes notexhibit
thesamebenefit.Panel(b)showsoverallsuccess,notethattheseparate-policysuccessrateisaverageacrossall20per-taskpolicies;Assetnotation:N,
G, R, and P denote nuts, gears, rods, and pegs, respectively; numeric suffixes indicate nominal diameters in millimeters, while s, m, and l indicate gear
size."Sparsereward"denotesEq.(6);"densereward"additionallyincludestheshapingtermsinEq.(7).
One policy, sparse reward One policy, dense reward Algorithm1AlphaNISTHeterogeneousAssemblyLearning
20-policy mean, sparse reward 20-policy mean, dense reward ,s¯)}M
|     |     |     |     |     |     | Require: |            | D reset ={(e | i         | i i=1   | ; history | length | L; batch | size N; |
| --- | --- | --- | --- | --- | --- | -------- | ---------- | ------------ | --------- | ------- | --------- | ------ | -------- | ------- |
|     | 100 |     |     |     |     |          | shared     | π θ ,V ϕ     |           |         |           |        |          |         |
|     |     |     |     |     |     | 1:       | initialize | each         | rolling   | success | rate pˆ   | i ←0   |          |         |
|     |     |     |     |     |     | 2:       | for each   | PPO          | iteration | do      |           |        |          |         |
|     | 75  |     |     |     |     |          | B←∅        |              |           |         |           |        |          |         |
3:
| )%( sseccuS |     |     |     |     |     |     |       | |B|<N |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- |
|             |     |     |     |     |     | 4:  | while |       | do  |     |     |     |     |     |
n
|     |     |     |     |     |     | 5:  |     | for all | completed | episodes  |            | do         |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --------- | ---------- | ---------- | --- | --- |
|     | 50  |     |     |     |     |     |     | y       | ←⊮[full   | assembly] |            |            | i   |     |
|     |     |     |     |     |     | 6:  |     | n       |           |           | for        | entry      | n   |     |
|     |     |     |     |     |     |     |     | pˆ      | ← mean    | of        | its latest | L outcomes |     |     |
|     |     |     |     |     |     | 7:  |     | in      |           |           |            |            |     |     |
end for
8:
|     | 25  |     |     |     |     |     |     | update | reset probabilities |     | q using | Eq. | (4) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------------------- | --- | ------- | --- | --- | --- |
9:
|     |     |     |     |     |     |     |     | for all | environments |     | n requiring | reset | do  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------------ | --- | ----------- | ----- | --- | --- |
10:
|     |     |     |     |     |     |     |     | i   | ∼Cat(q); | (e  | ,s )←(e |     | ,s¯ ) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------- | --- | ----- | --- |
|     | 0   |     |     |     |     | 11: |     | n   |          |     | n n,0   | in  | in    |     |
end for
|     | 0   | 10                              | 20 30 | 40  | 50  | 12: |     |          |              |     |            |             |     |      |
| --- | --- | ------------------------------- | ----- | --- | --- | --- | --- | -------- | ------------ | --- | ---------- | ----------- | --- | ---- |
|     |     |                                 |       |     |     |     |     | a ∼π     | (·|o         | ),  | ∀n         |             |     |      |
|     |     | Training iterations (thousands) |       |     |     | 13: |     | n,t      | θ            | n,t |            |             |     |      |
|     |     |                                 |       |     |     |     |     | step all | environments |     | and append | transitions |     | to B |
14:
| Fig.                                                         | 6. Joint | sparse training | converges faster | than separate | policies. |     | end    | while |       |       |          |        |     |     |
| ------------------------------------------------------------ | -------- | --------------- | ---------------- | ------------- | --------- | --- | ------ | ----- | ----- | ----- | -------- | ------ | --- | --- |
| Curvescompareonesharedpolicytrainedonall20taskswiththemeanof |          |                 |                  |               |           | 15: |        |       |       |       |          |        |     |     |
|                                                              |          |                 |                  |               |           |     | update | π     | and V | using | standard | PPO on | B   |     |
| 20policiestrainedseparately,onepertask.                      |          |                 |                  |               |           | 16: |        | θ     | ϕ     |       |          |        |     |     |
end for
17:
Success rate ± SD over 5 seeds
|     |     |               |                  |     |     | 87Nm    | and    | 12Nm, |                    | respectively. |           | These | constraints | keep |
| --- | --- | ------------- | ---------------- | --- | --- | ------- | ------ | ----- | ------------------ | ------------- | --------- | ----- | ----------- | ---- |
|     |     | Sparse reward | Beta sampling    |     |     |         |        |       |                    |               |           |       |             |      |
|     |     | Dense reward  | Uniform sampling |     |     |         |        |       |                    |               |           |       |             |      |
|     |     |               |                  |     |     | actions | within | a     | hardware-realistic |               | envelope, |       | preventing  | the  |
100 policy from exploiting unrealistic speeds or torques. Similar
|     |     |     |     |     |     | hardware-aligned |     |     | simulation |     | has enabled | transfer |     | of assem- |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | ---------- | --- | ----------- | -------- | --- | --------- |
)%( sseccus detaulavE
|     |     |     |     |     |     | bly | policies | to the | same | Franka | Panda | platform | [20], | [29]. |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ---- | ------ | ----- | -------- | ----- | ----- |
75
|     |     |     |     |     |     | E.  | Distributed | Training |     | and | Scale |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | --- | ----- | --- | --- | --- |
50
|     |     |     |     |     |     |     | We scale | synchronous |     | PPO | across | 1–256K | environments, |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | --- | ------ | ------ | ------------- | --- |
with4KperGPUinmulti-GPUruns.EachGPUsamplesits
25 local reset bank using rolling success estimates. Actor and
|     |     |     |     |     |     | critic | gradients | are  | averaged  |          | across | GPUs  | before          | each opti- |
| --- | --- | --- | --- | --- | --- | ------ | --------- | ---- | --------- | -------- | ------ | ----- | --------------- | ---------- |
|     |     |     |     |     |     | mizer  | step.     | Each | iteration | collects | 32     | steps | per environment |            |
0
|     |     | 1K 2K 4K | 8K 16K | 32K 64K | 128K 256K |     |     |     |     |     |     |     |     |     |
| --- | --- | -------- | ------ | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
andoptimizesfor5epochswith4minibatcheseach.Network
Parallel training environments
|     |     |     |     |     |     | architecture |     | and | PPO | settings | are fixed | across | scales. |     |
| --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | -------- | --------- | ------ | ------- | --- |
Fig.7. Sparsetaskrewardsbenefitstronglyfromparallelexperience.
Meansuccess±standarddeviationover5evaluationseedsfor25k-iteration V. EXPERIMENTS
| checkpoints, |     | with 32 trials | per task per seed | across 20 assemblies. | Color |     |     |     |     |     |     |     |     |     |
| ------------ | --- | -------------- | ----------------- | --------------------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Weorganizetheexperimentsaroundthreequestions:(Q1)
| denotes | reward; | solid and | dashed lines denote | beta and uniform | training- |                |     |     |       |          |      |         |     |            |
| ------- | ------- | --------- | ------------------- | ---------------- | --------- | -------------- | --- | --- | ----- | -------- | ---- | ------- | --- | ---------- |
|         |         |           |                     |                  |           | Heterogeneity: |     |     | Under | a binary | task | reward, | how | does joint |
resetsampling.
|     |     |     |     |     |     | training |     | compare | with | training | each | task | separately? | (Q2) |
| --- | --- | --- | --- | --- | --- | -------- | --- | ------- | ---- | -------- | ---- | ---- | ----------- | ---- |
Scaling:Howdoparallelexperienceandreset-statesampling

(a)Board-assistedreorientation(waterproof) (b)Release-and-regraspforalignment(d-sub)
(c)Center-to-tipgrasptransfer(peg8mm) (d)Side-cagingforgearplacement(mediumgear)
(e)Edge-to-flatnutreorientation(nutm12) (f)One-sidedtappingforthreading(nutm4)
(g)Shovelingtoabetterpickupposition(rod8mm) (h)Full-circlenutthreading(nutm16)
Fig. 8. One shared policy discovers diverse contact strategies from a sparse binary task reward. Each panel proceeds from left to right. (a)
Waterproofconnector:boardcontacthelpsreorientthepartbeforeinsertion.(b)D-subconnector:thepartissetdownandregraspedforalignmentwith
itssocket.(c)8mmpeg:thepartisdroppedfromacentergraspandregraspednearoneend,leavingitsremaininglengthfreeforinsertion.(d)Medium
gear:thepartpivotsfromasidegraspintoahorizontalposeoveritsmountingpost.(e)M12nut:thenutisrolledfromitsedgeontoaflatfacebefore
placement on the bolt. (f) M4 nut: repeated one-sided taps advance the nut along the thread. (g) 8 mm rod: the fingertip shovels the rod to a position
whereitiseasiertolift.(h)M16nut:thegrippermovesaroundthenut,usingfingertipcontacttoturnitalongthebolt.
affect learning from a binary task reward? (Q3) Reward each task. Success requires full assembly within 15 seconds
formulation: How does a binary task reward compare with without a simultaneous safety failure. The reward ablation
dense assembly-progress shaping as heterogeneous training adds two dense assembly-progress terms to Eq. (6):
scales? We additionally explore multi-pair assembly and
rdense =r +c rreach+c ralign, c ,c ≥0, (7)
inspect the learned policy for behaviors that arise without t t 2 t 3 t 2 3
direct supervision. where rreach rewards end-effector proximity to the part cen-
t
For heterogeneity, we compare one policy trained across troid and ralign rewards alignment with the target assembly
t
all20ATB1taskswithoneseparatelytrainedpolicypertask, orientation. These are common shaping terms in manipula-
using matched per-run interaction budgets and otherwise tionandassemblyRL[2],[10],[20].Wesetc =c =0.01,
2 3
identical settings. We use 64K environments per run to keep matchingthecoefficientsusedinOmniReset[10].Acrossall
the comparison affordable; the shared policy reaches 98.2% experiments, success rates cover all reset configurations.
training success at this scale.
A. Assembly-Pair Heterogeneity Enables Learning
For parallel scaling, GPUs, environments, and rollout
batch size increase together while the task distribution, From randomly initialized states, separately-trained poli-
reward, policy, and environment remain fixed. The sam- cies have ≤0.3% success on M4 nut threading, as well as
pling ablation compares against uniform sampling over the 4mm peg insertion and rod insertion. The main obstacle is
same reset bank instead of beta sampling. For the scaling thatthesmallpartsaredifficulttograspreliablyfromtheta-
evaluation, all checkpoints use stochastic actions and a ble.Incontrast,thesharedpolicyproducessuccessfulgrasp-
commonfrozenmixed-resetbank,sampleduniformlywithin and-assembly rollouts on these same tasks without task-

(a)BringUSB-Acloser,assemblethe8mmrod,thenreturn
(b)MakingsmallturnsthreadingM12toavoidRJ45collision
Fig.9. Emergentcoordinationinmulti-pairassembly.(a)ThepolicybringstheUSB-Aconnectorfromadistantcornertoanearbyworkingposition,
leavesittherewhileassemblingthe8mmrod,thenreturnstoinserttheconnector.(b)DuringM12nutthreading,theendeffectormakessmallturnsto
avoidtouchingtheneighboringRJ45connector.Eachsequenceproceedsfromlefttoright.
TABLEI
SUCCESSRATEFORMULTI-PAIRASSEMBLYEACHPOLICYISTRAINEDANDEVALUATEDONTHESAMENUMBEROFACTIVEASSEMBLYPAIRS,
FROM1–10.ALPHANISTSOLVESTHESETASKSWITHOUTAPRESCRIBEDORDEROREXPLICITTASKDECOMPOSITION.FOREXAMPLE,WHENTHERE
ARE10ACTIVEPAIRS,THEPOLICYRECEIVESASUCCESSREWARDONLYWHENALL10AREINTHEIRASSIGNEDBOARDSLOTS.
| #ActivePairs   |     | 1   | 2   |     | 3   | 4   | 5   | 6   | 7   |     | 8   | 9   | 10  |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SuccessRate(%) |     | 99  | 97  |     | 95  | 93  | 92  | 90  | 89  |     | 87  | 86  | 84  |
specific changes. This result suggests that shared experience overuniformresetsampling.At256Kenvironments,success
canhelpwithassembliesthataredifficulttolearnseparately. with the sparse binary task reward reaches 97.4% with
This benefit depends strongly on the reward formulation. beta sampling versus 84.3% with uniform sampling; the
At their final checkpoints, the 20 separately trained dense- corresponding results with dense reward shaping are 77.4%
reward policies reach a mean success rate of 78.3%, ranging and 34.3%. While the advantage of the sparse task objective
from 45.0% on M4 threading to 93.6% on the medium is already visible at modest scale, beta sampling provides
gear. Joint dense training reaches 17.8% overall success at further gains as parallel experience increases.
| 25K iterations, | with        | low completion |      | across        | tasks | (Fig. 5). |             |            |     |            |          |     |     |
| --------------- | ----------- | -------------- | ---- | ------------- | ----- | --------- | ----------- | ---------- | --- | ---------- | -------- | --- | --- |
|                 |             |                |      |               |       |           | C. Emergent | Strategies |     | over Short | Horizons |     |     |
| One possible    | explanation | is             | that | dense shaping | terms | favor     |             |            |     |            |          |     |     |
different partial solutions across geometries, whereas the The policy exhibits a broad range of dexterous strategies
|             |        |         |         |               |     |           | across assemblies |     | (Fig. | 8), including |     | grasp adaptation, | ex- |
| ----------- | ------ | ------- | ------- | ------------- | --- | --------- | ----------------- | --- | ----- | ------------- | --- | ----------------- | --- |
| binary task | reward | gives a | unified | full-assembly |     | objective |                   |     |       |               |     |                   |     |
for every task. trinsic reorientation, and contact-driven assembly. It releases
|        |          |                |         |     |             |             | and reacquires | parts | when        | the | initial  | grasp is  | unsuitable |
| ------ | -------- | -------------- | ------- | --- | ----------- | ----------- | -------------- | ----- | ----------- | --- | -------- | --------- | ---------- |
| Joint  | training | reaches higher | success | at  | lower       | total cost. |                |       |             |     |          |           |            |
|        |          |                |         |     |             |             | for insertion, | uses  | surrounding |     | geometry | to change | object     |
| At 64K | parallel | environments   | across  | 25K | iterations, | the         |                |       |             |     |          |           |            |
sharedpolicytrainedwiththesparsebinarytaskreward orientation, and discovers intermittent tapping and pivoting
|     |     |     |     |     |     |     | motions. | These | behaviors | emerge | within | a single | policy, |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----- | --------- | ------ | ------ | -------- | ------- |
reaches98.2%trainingsuccessin410GPU-hours(Fig.6),
|           |               |            |          |         |                    |     | without demonstrations |       | or             | rewards    | specifying | the     | individual  |
| --------- | ------------- | ---------- | -------- | ------- | ------------------ | --- | ---------------------- | ----- | -------------- | ---------- | ---------- | ------- | ----------- |
| while the | 20 separately | trained    | policies | average | 81.4%              | and |                        |       |                |            |            |         |             |
|           |               |            |          |         |                    |     | maneuvers.             | For a | peg, a         | successful | pickup     | may     | not produce |
| consume   | 16.1K total   | GPU-hours, |          | 39.3×   | more device-hours. |     |                        |       |                |            |            |         |             |
|           |               |            |          |         |                    |     | a grasp suitable       |       | for insertion; | the        | policy     | drops a | center-held |
B. Sparse Binary Task Rewards Benefit from Scale peg and regrasps it near one end, exposing enough shaft
|     |     |     |     |     |     |     | length for | complete | insertion. |     | For a | nut, repeated | taps on |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | ---------- | --- | ----- | ------------- | ------- |
Performance with the sparse binary task reward improves one side engage and advance the thread, using intermittent
| rapidly        | with increased | parallel    | experience |            | (Fig.       | 7). With |             |            |          |           |          |     |     |
| -------------- | -------------- | ----------- | ---------- | ---------- | ----------- | -------- | ----------- | ---------- | -------- | --------- | -------- | --- | --- |
|                |                |             |            |            |             |          | contact to  | make       | assembly | progress. |          |     |     |
| beta sampling, | evaluation     | success     |            | rises from | 38.6%       | at 1K    |             |            |          |           |          |     |     |
|                |                |             |            |            |             |          | D. Emergent | Strategies |          | over Long | Horizons |     |     |
| environments   | to             | 78.9% at 4K | and        | 86.9%      | at 8K. With | dense    |             |            |          |           |          |     |     |
reward shaping, success remains at 11.8–12.0% over 1K– Beyond the main single-assembly experiments, we train
4Kenvironments.Betasamplingprovidesanadditionalgain policies with multiple assembly pairs per episode. The bi-

nary task reward is issued only when every active pair is [4] W.Lian,T.Kelch,D.Holz,A.Norton,andS.Schaal,“Benchmarking
assembled;episodesallow15secondsperpairandterminate off-the-shelfsolutionstoroboticassemblytasks,”inProc.IEEE/RSJ
Int.Conf.Intell.RobotsSyst.,2021,pp.791–798.
upon success. Table I shows the success rates for episodes
[5] A. S. Morgan, Q. Bateux, M. Hao, and A. M. Dollar, “Towards
with up to ten active pairs. This multi-pair setting reveals generalized robot assembly through compliance-enabled contact for-
coordination over substantially longer horizons (Fig. 9). The mations,”inProc.IEEEInt.Conf.Robot.Automat.,2023,pp.8010–
8016.
policy need not finish assembling a pair before turning to
[6] J.Luoetal.,“Robustmulti-modalpoliciesforindustrialassemblyvia
another, and its approach to one assembly changes based reinforcement learning and demonstrations: A large-scale study,” in
onneighboringparts.Theseplanning-likebehaviors—taking Proc.Robot.:Sci.Syst.,2021.
[7] O. Zhang, M. Guaman Castro, P. Yin, A. Gupta, R. Scalise,
actions whose utility is realized later and adapting one
and B. Boots, “A balanced data diet: Addressing the bottleneck
assemblytothestateofanother—emergewithoutanexplicit in mega-scale RL for robot control,” 2026. [Online]. Available:
planner, policy switching, or prescribed sequence. https://sgs-rl.github.io/
[8] D.Silveretal.,“MasteringthegameofGowithdeepneuralnetworks
VI. LIMITATIONS
andtreesearch,”Nature,vol.529,pp.484–489,2016.
[9] ——,“MasteringthegameofGowithouthumanknowledge,”Nature,
First, all results are in simulation. Hardware-matched vol.550,pp.354–359,2017.
[10] P. Yin et al., “Emergent dexterity via diverse resets and large-scale
velocity and torque limits constrain the learned motions, but
reinforcement learning,” in Proc. Int. Conf. Learn. Representations,
do not establish robustness to perception error, latency, or 2026.[Online].Available:https://arxiv.org/abs/2603.15789
contact-model mismatch. Transfer and repeatability will be [11] M.Mittaletal.,“IsaacLab:AGPU-acceleratedsimulationframework
formulti-modalrobotlearning,”2025,arXiv:2511.04831.
evaluated on the physical board using sensor-derived obser-
[12] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel,
vationsandrandomizedcontactandlatencymodels.Second, “mjlab:AlightweightframeworkforGPU-acceleratedrobotlearning,”
while applying the 10-pair policy to successive groups of 2026,arXiv:2601.22074.
[13] M.Andrychowiczetal.,“Learningdexterousin-handmanipulation,”
parts could offer a route to completing the full board,
Int.J.Robot.Res.,vol.39,no.1,pp.3–20,2020.
extending our multi-pair framework to 20 parts remains an [14] H.Qietal.,“Generalin-handobjectrotationwithvisionandtouch,”
excitingresearchgoal.Achievingthisatscale,underasingle inProc.Conf.RobotLearn.,2023,pp.2549–2564.
[15] R. Singh, A. Allshire, A. Handa, N. Ratliff, and K. Van Wyk,
terminal task reward, will likely benefit from more efficient
“DextrAH-RGB:Visuomotorpoliciestograspanythingwithdexterous
simulation and learning methods. hands,”2024,arXiv:2412.01791.
[16] A. Handa et al., “Dextreme: Transfer of agile in-hand manipulation
VII. CONCLUSION fromsimulationtoreality,”inProc.IEEEInt.Conf.Robot.Automat.
(ICRA),2023,pp.5977–5984.
AlphaNIST shows that heterogeneous contact-rich assem-
[17] NVIDIA, “GPU simulation,” PhysX SDK 5.4.1 documentation,
bly can be learned with a single policy using a binary accessed:Sep.14,2026.[Online].Available:https://nvidia-omniverse.
task objective, diverse reset coverage, and large-scale re- github.io/PhysX/physx/5.4.1/docs/GPURigidBodies.html
[18] The Newton Contributors, “Newton: GPU-accelerated physics
inforcement learning. In simulation, one policy learns all
simulation for robotics and simulation research,” 2025. [Online].
20 ATB1 tasks without demonstrations, prescribed stages, Available:https://github.com/newton-physics/newton
or per-task tuning, while outperforming separately trained [19] T. Yu, S. Kumar, A. Gupta, S. Levine, K. Hausman, and C. Finn,
“Gradient surgery for multi-task learning,” in Proc. Adv. Neural Inf.
specialistsonthemostdifficultsmall-partassemblies.Across
Process.Syst.,2020,pp.5824–5836.
all tested scales, the binary task objective outperforms the [20] B.Tangetal.,“AutoMate:Specialistandgeneralistassemblypolicies
evaluateddenserewardshaping.Thelearnedpolicydiscovers overdiversegeometries,”inProc.Robot.:Sci.Syst.,2024.
[21] M. Hessel, H. Soyer, L. Espeholt, W. Czarnecki, S. Schmitt, and
grasp adaptation, extrinsic reorientation, tapping, threading,
H.vanHasselt,“Multi-taskdeepreinforcementlearningwithPopArt,”
and longer-horizon coordination without direct supervision. inProc.AAAIConf.Artif.Intell.,vol.33,no.1,2019,pp.3796–3803.
In multi-pair assembly, it can prepare one part, complete [22] V. Kurin, A. De Palma, I. Kostrikov, S. Whiteson, and P. K.
Mudigonda,“Indefenseoftheunitaryscalarizationfordeepmulti-task
another,andreturntofinishthefirst,withoutanintermediate
learning,”inProc.Adv.NeuralInf.Process.Syst.,2022,pp.12169–
assembly reward or a planner prescribing the sequence. 12183.
Morebroadly,thesefindingschallengetheassumptionthat [23] G.Schoettleretal.,“Deepreinforcementlearningforindustrialinser-
tiontaskswithvisualinputsandnaturalrewards,”inProc.IEEE/RSJ
taskcomplexityanddiversitymustbereducedtomakerobot
Int.Conf.Intell.RobotsSyst.,2020,pp.5548–5555.
learningtractable.Instead,theyshowthatdiverseexperience [24] C. Florensa, D. Held, M. Wulfmeier, M. Zhang, and P. Abbeel,
under a shared objective can itself become a source of “Reversecurriculumgenerationforreinforcementlearning,”inProc.
Conf.RobotLearn.,2017,pp.482–495.
reusable dexterity and coordination. We view this work as
[25] B. Tang et al., “Refinery: Active fine-tuning and deployment-time
a critical step toward general-purpose assembly policies that optimizationforcontact-richpolicies,”2025,arXiv:2510.11019.
discover how to solve complex physical tasks, rather than [26] J. Sun et al., “ARCH: Hierarchical hybrid learning for long-horizon
contact-rich robotic assembly,” in Proc. Conf. Robot Learn., 2025.
requiring those strategies to be specified in advance.
[Online].Available:https://arxiv.org/abs/2409.16451
[27] K.He,X.Zhang,S.Ren,andJ.Sun,“Deepresiduallearningforimage
REFERENCES recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit.,
2016,pp.770–778.
[1] K.Kimbleetal.,“Benchmarkingprotocolsforevaluatingsmallparts [28] H. Lee et al., “SimBa: Simplicity bias for scal-
roboticassemblysystems,”IEEERobot.Automat.Lett.,vol.5,no.2,
ing up parameters in deep reinforcement learning,” in
pp.883–889,2020. Proc. Int. Conf. Learn. Representations, 2025. [Online].
[2] Y.Narangetal.,“Factory:Fastcontactforroboticassembly,”inProc.
Available: https://proceedings.iclr.cc/paper_files/paper/2025/hash/
Robot.:Sci.Syst.,2022.
741aab8b41a2987867acc9939ad50383-Abstract-Conference.html
[3] T.Lozano-PérezandR.H.Wilson,“Assemblysequencingforarbitrary [29] B. Tang et al., “IndustReal: Transferring contact-rich assembly tasks
motions,” in Proc. IEEE Int. Conf. Robot. Automat., 1993, pp. 527– fromsimulationtoreality,”inProc.Robot.:Sci.Syst.,2023.
532.