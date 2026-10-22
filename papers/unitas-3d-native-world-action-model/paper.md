Underreview
UNITAS: A 3D-NATIVE WORLD ACTION MODEL FOR
EMBODIED MANIPULATION
RuixiangWang1,2* YongyiSu3*† WenlveZhou3 BoYue1,2 HengyanLiu1,2 DekunLu2
YuxinTian1,2 YihanFang1,2 ZeruiWu2 XingHu2 JietaoChen2 YongGuo2
ZiyanHe2 JunbinYuan4 GuiliangLiu1 XiaofenXing5 KuiJia1,2
1TheChineseUniversityofHongKong,Shenzhen 2DexForceTechnologyCo.,Ltd.
3FoshanUniversity 4SunYat-senUniversity 5SouthChinaUniversityofTechnology
*Equalcontribution. †Correspondenceto<suyongyi@fosu.edu.cn>.
ABSTRACT
Worldactionmodels(WAMs)aimtoansweracoupledphysicalquestion: given
a task instruction, what motion should the robot execute, and how will that mo-
tion change the surrounding world? Most existing WAMs build on pretrained
videogeneratorsandrepresentworldevolutionthroughimagesorvisuallatents.
Roboticinteraction,however,takesplaceinmetricthree-dimensionalspace,while
imagesareview-dependentprojectionswhosepixeldistancesdonotdirectlyen-
code physical distances. We introduce UNITAS, to our knowledge the first 3D-
nativeworldactionmodelthatunifiesobservations,actions,andscenedynamics
in a shared metric 3D frame within each interaction, using a common represen-
tation across robot embodiments and human hands. Action flow represents hu-
manhandsandrobotgrippersas3Dpointtrajectories,whilesceneflowdescribes
scene-point displacements conditioned on these trajectories. World-aligned 3D
positional embeddings ground visual tokens with or without depth input, and a
physical-timetrajectorytokenizerencodeseachpointtrajectoryasonetokenan-
chored at its current 3D position. This interface supports both direct action ex-
ecution and action-conditioned scene prediction. With 1.7B parameters, UNI-
TAS achieves the best action-conditioned scene prediction on RoboTwin among
the compared methods, with up to 49% lower displacement errors than Point-
World, and state-of-the-art manipulation success, including 99.8% on LIBERO
andanaverageof85%acrossreal-worldtasks. Thecodeisavailableathttps:
//github.com/DexForce/UNITAS.
1 INTRODUCTION
WorldActionModels(WAMs)aimtoansweracoupledphysicalquestion: givenataskinstruction,
what motion should the robot execute, and how will that motion change the surrounding world?
Most existing WAMs couple action learning with prediction of future images or visual latents, in-
creasinglybuildingonpretrainedvideomodels(Yangetal.,2023;Lietal.,2025b;Zhuetal.,2025;
Cen et al., 2025; Bi et al., 2025; Ye et al., 2026; Yuan et al., 2026b; Zhou et al., 2026b). Robotic
interaction, however, takes place in metric three-dimensional space, and an image is only a view-
dependentprojectionofthatspace.
Thesamerobotmotion, objectdisplacement, orcontacteventcanproducedifferentpixelchanges
across views, and equal pixel displacements need not correspond to equal physical distances (Ze
et al., 2024; Qu et al., 2025). Differences in camera intrinsics and camera-to-robot poses further
makethismappingvaryacrossembodiments. Evaluationsofvideo-basedWAMsreportsensitivity
toviewpointandrobot-statechanges(Zhangetal.,2026b),andaphotorealisticpredictionmaystill
misrepresent object displacement, deform rigid geometry, or allow static regions to drift (Huang
etal.,2026). Suchvisualrepresentationsleavemetricmotionandcontactrelationshipsimplicitfor
spatialreasoning,prediction,andcontrol.
1
6202
tcO
8
]OR.sc[
1v99021.0162:viXra

Underreview
(a) Diverse embodiments (b) One world-coordinate interface (c) Performance
VLABench
Simulation Multi-view RGB + camera calibration Overall89.1 Plus  SR VLABench  PS
Action Flow
|     |     |     | 56.2            | 67.6                  |
| --- | --- | --- | --------------- | --------------------- |
|     |     |     | Robot94.2 Plus  | 85.0 Real-world  Avg. |
conditions
Human hands Unitas Scene Flow P lu s   82.1 92.9Ro b o T w in
|     |     |     | Ca m e r a | C l e a n |
| --- | --- | --- | ---------- | --------- |
Initial 3D
| point queries                      |                  |               | LI B E 9 R 9 O .4   | 93 R .0 o b o T w in  |
| ---------------------------------- | ---------------- | ------------- | ------------------- | --------------------- |
|                                    | Gripper history  | Robot actions | L o n g 9 9 .8      | R a n d .             |
|                                    | + current state  |               | LI Avg. B E RO      |                       |
| “Insert the flower into the vase.” |                  |               | Unitas X-VLA        | π0.5 Fast-WAM         |
Align diverse embodiments )%( aremaC sulP-OREBIL
|             |     | Action       | Unitas        |      |
| ----------- | --- | ------------ | ------------- | ---- |
| Calibrated  |     | + scene flow | 80            |      |
| RGB views   |     |              | π0.5          | LaMP |
|             |     |              | 50 LingBot-VA |      |
...
20
|     |     |     | X-VLA | Fast-WAM |
| --- | --- | --- | ----- | -------- |
|     |     |     | 1 3   | 5 6      |
Real robots Parameters (B)
World-model scene predictions
Gripper
Scene flow
|     |     |     | RoboTwin · lift pot LIBERO · place bowl |     |
| --- | --- | --- | --------------------------------------- | --- |
Figure1: UNITAS isa3D-nativeworldactionmodel. Observations, actionflow, andsceneflow
shareametricframewithineachpredictionwindow,withacommonrepresentationacrossembod-
iments. With1.7Bparameters,UNITASachievesleadingmanipulationresultsamongthecompared
methodsandpredictsaction-conditionedscenetrajectories.
Recentmethodsincorporatedepth,opticalflow,sceneflow,orreconstructed4Dgeometryintopre-
diction(Zhenetal.,2025;Guoetal.,2026;Zhaoetal.,2026;Wangetal.,2026b)orgroundaction
generation in explicit 3D structure (Shridhar et al., 2023; Ze et al., 2024; Zhen et al., 2024; Qu
etal.,2025). Yetgeometryoftenservesasaninputcueorauxiliarypredictiontarget,ratherthana
sharedinterfaceforactiongenerationandscenedynamics. PointWorld(Huangetal.,2026)directly
predictsmetricpointflowsconditionedonexternallysuppliedrobotmotion,ratherthangenerating
thatmotionfromataskinstruction. A3D-nativeWAMshouldplaceobservations,actions,andre-
sulting scene changes in a shared metric frame, enabling task-conditioned behavior, consequence
prediction,andexecutablecontrol.
We introduce UNITAS, UNIfied Trajectories for Action and Scene flow. To our knowledge, it is
the first 3D-native world action model that aligns observations, actions, and scene dynamics in a
shared metric frame within each prediction window, using a common representation across robot
embodimentsandhumanhands,asillustratedinFig.1.
Realizing this 3D-native world action model presents three challenges. First, visual observations
must be grounded in metric space even when depth is unavailable. We propose world-aligned 3D
positionembeddingsderivedfromobserveddepthorlearnedweightsovercandidatepositionsalong
calibratedcamerarays. Second, humanhandsandrobotgrippershavedifferentmorphologiesand
control interfaces. We propose action flow, which represents their motion as trajectories of corre-
sponding3Dpointsinthesharedframe. Third,trajectoriesdifferinframerateanddurationacross
data sources. Representing each timestep as a token allocates backbone capacity across unequal
physical-timeintervals. Weproposeaphysical-timetrajectorytokenizer,whichalignseachtrajec-
torytoelapsedtimeandencodesthewholetrajectoryasonetokenbeforethebackbone. Sceneflow
describesscene-pointdisplacementsdecodedfromtrajectorytokensconditionedonactionflow.
In the backbone, observation tokens are grounded in world coordinates, while action-flow tokens
acrossembodimentsandscene-flowtokensareanchoredateachpoint’scurrent3Dposition,allow-
ingthenetworktomodelmotionthroughfeaturesassociatedwithfixedspatialanchors. Giventhe
instructionandcurrentobservations,alayer-coupledMixture-of-Transformersjointlymodelspoint
trajectories and executable commands. This supports two modes: policy mode directly generates
executableactions,whilesimulatormodepredictsscenechangesconditionedonexternallysupplied
actionflow. Acausalattentionmaskenableskey–valuecachingofsharedcontextacrossdenoising
steps,reducingrepeatedcomputationandacceleratinginference.
WeevaluateUNITASonaction-conditionedscenepredictionandroboticmanipulation. Insimulator
mode,itleadsthecomparedmethodsacrossallfourRoboTwinscene-predictionmetrics,reducing
2

Underreview
MovingADE,MovingFDE,andStaticADEby35%,21%,and49%,respectively,relativetoPoint-
World(Huangetal.,2026). Inpolicymode,itachieves99.8%successonLIBEROandoutperforms
largervideo-basedWAMsonRoboTwin. ItleadsthecomparedmethodsinVLABenchsuccessrate
andprogressscore,andreaches89.1%successonLIBERO-Pluswithstrongrobustnesstocamera
androbot-statechanges. Real-robotsuccessreaches90%onOrganizeBooksand65%onPackthe
Ball, exceeding both baselines. Ablations show that world-aligned visual grounding, action- and
scene-flowsupervision,andmotionhistoryimprovepolicyperformanceandrobustness.
Ourcontributionsare:
• Toourknowledge, UNITAS isthefirst3D-nativeworldactionmodelthatalignsobserva-
tions,actions,andscenedynamicsinasharedmetricframe,usingacommonrepresentation
acrossrobotembodimentsandhumanhands.
• Action flow represents human hands and robot grippers through point trajectories, while
sceneflowrepresentstheenvironmentalresponseconditionedonthatmotion. Bothpolicy
andsimulatormodesusethisinterface.
• World-aligned positional embeddings ground visual observations with or without depth,
andaphysical-timetrajectorytokenizerencodeseachpointtrajectoryasonetokenspatially
anchoredatitscurrent3Dposition.
• With 1.7B parameters, UNITAS achieves leading action-conditioned scene prediction and
strongmanipulationperformanceinsimulationandonrealhardware.
2 RELATED WORK
Video world–action modeling. Video-based policies use future prediction for control (Hu et al.,
2024),withearlyWAMscouplingpredictionandactionlearningthroughsharedrepresentationsand
generativeobjectives(Lietal.,2025b;Zhuetal.,2025;Cenetal.,2025;Xuetal.,2025a). Video-
generationpriorssubsequentlysupportjointvideo–actionlearningandfuture-conditionedpolicies
(Liaoetal.,2025;Shenetal.,2025;Bietal.,2025;Kimetal.,2026;Lietal.,2026;Wangetal.,
2026a), while heterogeneous robot and video-only data support cross-task and cross-embodiment
transfer(Yeetal.,2026;Zhangetal.,2026a).Efficientvariantsomitfuturegenerationatdeployment
orreplaceitwithlatentsubgoals(Yuanetal.,2026b;Chenetal.,2026a). Thesemodelsprimarily
represent world evolution in images or visual latents. Reported sensitivity to viewpoint and robot
initial-statechanges(Zhangetal.,2026b;Hongetal.,2026)highlightstheimportanceofgrounding
perception,worldevolution,andexecutableactionsinasharedphysicalspace.
Policy learning in 3D space. Explicit 3D representations improve spatial understanding for ma-
nipulation (Shridhar et al., 2023; Ze et al., 2024; Zhen et al., 2024; Qu et al., 2025). Geometry-
aware world models augment visual prediction with image-aligned geometric signals (Zhen et al.,
2025;Guoetal.,2026;Zhaoetal.,2026). Inpolicylearning,LaMP(Wangetal.,2026b)andGe-
omVLA(Xiongetal.,2026)useintermediatemotionfeaturesfromtrajectorydenoisingtocondition
actiongeneration. PointWorld(Huangetal.,2026)followsthecomplementarydirection,predicting
sceneflowconditionedonrobotmotionforplanning. UNITAS jointlymodelsagentmotionandits
conditionalsceneresponsethroughpointflows,whilesupportingdirectcommandexecutionwithout
generatingsceneflows.
Unifiedactionrepresentationsformanipulation. Cross-embodimentlearningmustreconciledif-
ferentmorphologiesandcontrolinterfaces(Chietal.,2024). Generalistpoliciesuseembodiment-
specific prompts, canonical state–action formats, and aligned end-effector conventions (Liu et al.,
2024;Zhengetal.,2025;Yuanetal.,2026a;XiaomiRoboticsTeametal.,2026). Pointflowspro-
videtransferablemotiontargetsacrossembodiments(Yuanetal.,2024;Bharadhwajetal.,2024;Xu
etal.,2025b),connectingobject-motionpredictiontocontrol(Zhietal.,2025;Dharmarajanetal.,
2025)andrepresentingrobotandobjecttrajectories(Huangetal.,2026;Linetal.,2026). UNITAS
unifieshuman-hand,robot-gripper,andscenetrajectorieswithasharedphysical-timetokenizer.
3 METHODOLOGY
We first revisit video-based world action modeling, then formulate UNITAS in a shared metric 3D
frame,asillustratedinFig.2.
3

Underreview
(a) World-coordinate architecture (b) Attention mask
Generated result Action Flow Scene Flow Robot commands Training
Key / Value
tH tH O HA AγAcleanSγs q0 uγ
O
τ 1 , …, τ k t0 Physical Time Trajectory De t c 0 oder Δp, ΔR, w Ac H A le A γ an
Mixture of Transformers
Action-flow latents Scene latents Denoised commands û
Sγs
q0
Point Dyn × a L mics DiT S A c c e le n a e n condition S ing Acti × on L DiT uγ
O HA Aγ Aclean Sγs q0 uγ
Observation + Action-flow Noisy action Clean action Noisy scene EEF state Noisy commands
language history latents latents latents
+ One latent per point trajectory
P W os o it r i l o d n A E l m ig b ne e d d d 3 in D g VLM encoder 3 RGB views Physical Time Trajectory Tokenizer
Physical time encoding
“Insert the flower
into the vase.” Point trajectories τ k = k / f
yreuQ
World-aligned zy 3D PE KV cache x per token
Inference
Action policy World model
O HA q0 uγ O HAAcleanSγs
O O
HA HA
q0 Aclean
uγ Sγs
Observation Action flow Scene
Command mask
Figure 2: UNITAS architecture and attention masks. Left: The point dynamics expert models
bothactionandsceneflows,whiletheactionexpertgeneratestheend-effectoractionchunk. Scene
flowgenerationisconditionedoncleandemonstratedactionflowduringtrainingandgeneratedor
supplied action flow at inference. Right: Colored/white cells indicate allowed/blocked attention.
Policy-onlyinferenceomitsbothfutureaction-flowandscene-flowtokens.
3.1 REVISITINGVIDEOWORLDACTIONMODELS
Let o denote current image observations, ℓ the instruction, a an action chunk, and v future
1:H 1:T
images. Video-based WAMs represent future interactions through images or visual latents. For
modelsthatconditionactionsonpredictedfutures,theactiondistributioncanbewrittenas
(cid:90)
p(a |o,ℓ)= p(v |o,ℓ)p(a |o,ℓ,v )dv . (1)
1:H 1:T 1:H 1:T 1:T
Futurevideosandactionsmaybegeneratedjointlyorsequentially. Fast-WAM(Yuanetal.,2026b)
insteadretainsvideoco-trainingbutomitsfuture-videogenerationatinference:
p (a |o,ℓ)=p (a |z(o,ℓ)), L=L +λL . (2)
θ 1:H θ 1:H act vid
Itsvideobackboneencodesthecurrentobservationandinstructionintoz(o,ℓ)inoneforwardpass,
whiletheactionexpertstillperformsiterativedenoising. Thisremovesfuture-videosampling,but
thesharedrepresentationremainsimage-based,withoutanexplicitmetric3Dframe.
3.2 3D-NATIVEWORLDACTIONFORMULATION
Attimet,contextC comprisestheinstructionℓ,multi-viewobservationsO = {O }Nv ,camera
t t,i i=1
calibration {K ,TW}Nv , and historical action flow H . Here K denotes camera intrinsics, and
i t,i i=1 A i
TW ∈ SE(3) maps camera coordinates into the metric frame FW, fixed within each prediction
t,i
window. Actionpredictionadditionallyusesthecurrentend-effectorstateq .
0
Given query points and future timestamps, we predict action flow A for the interacting body and
sceneflowSfortheenvironment,bothasdisplacementtrajectoriesinFW.Aseparateactionbranch
predictsanexecutableend-effectoractionchunku. Ourmodelfactorizestheirjointdistributionas
p (A,u,S|C,q )=p (A|C)p (u|C,q )p (S|A,C). (3)
θ 0 θ θ 0 θ
Action flow and the action chunk can be sampled in parallel; scene prediction then conditions on
generated action flow A(cid:98) or an externally supplied trajectory A
ext
in simulator mode. Policy-only
executionevaluatesonlyp (u | C,q ),omittingbothpointflows. Thefollowingsectionsdescribe
θ 0
spatialgrounding,thesharedtrajectoryrepresentation,andthecoupledexpertsthatimplementthese
factors.
3.3 WORLD-ALIGNEDOBSERVATIONS
Framealignment.Withineachpredictionwindow,observations,robotorhumanmotion,andscene
trajectoriesshareonefixedmetricframe. Robotdemonstrationsusearobot-baseorsharedembod-
imentframe. Egocentrichumandemonstrationsusethecameraframeofthewindowanchor, held
fixedthroughoutthewindow. AppendixA.1liststhedatasetconventions.
4

Underreview
World-aligned 3D position embedding. Each visual token receives a position embedding in the
worldframe. Foraviewwithvaliddepth,O =(I ,D )containstheRGBimageandthedepth
t,i t,i t,i
alongtheopticalaxis. ThevisionencodermapstheimagetoatokengridF = Enc (I ). We
t,i vis t,i
back-projecteachpixelandtransformitintoworldcoordinates,
(cid:20) (cid:21) (cid:20) (cid:21)
P (u,v) P (u,v)
P (u,v)=D (u,v)K−1[u,v,1]⊤, world,i =TW camera,i . (4)
camera,i t,i i 1 t,i 1
Here, (u,v) denotes pixel-center coordinates, and the time index is omitted from the coordinate
maps. AfixedFouriermapψ encodestheworldposition. Insideeachpatch,Enc appliesψ and
3D
projectstheresulttothevisual-tokendimension:
E
pos,t,i
=Enc
3D
(P
world,i
), F(cid:101)t,i =F
t,i
+E
pos,t,i
. (5)
Spatialgroundingwithoutobserveddepth. Withoutdepth,thepositionembeddingiscomputed
from a weighted combination of positional features along the camera ray. For a patch centered at
(u,v),wedrawM =64depthsuniformlyfrom0.1to2.0m,back-projectthembyEq.4,andscore
themwiththepatchfeaturef:
(cid:18) (W f)⊤W ψ(p ) (cid:19)
α =softmax q k√ camera,m ,
m m
d
(6)
M
(cid:88)
E =W α W ψ(p ).
ground o m v world,m
m=1
Here f ∈ Rdf is the patch feature and ψ(·) ∈ Rdψ, with W
q
∈ Rd×df, W
k
∈ Rd×dψ, and
W
v
∈Rd×dψ. Keysencodecamera-framepositions,andvaluesencodethesamecandidatesinthe
world frame. E is added to the visual tokens in place of E in Eq. 5. Where depth is
ground pos,t,i
reliable, weusedepth-derivedembeddingsandsupervisetheroutingweightsbymatchingFourier
features:
(cid:13) (cid:13)2
(cid:88) Nv (cid:13)(cid:88) M (cid:16) (cid:17)(cid:13)
L = E (cid:13) α ψ(p )−sg Avg ψ(P (u,v)) (cid:13) . (7)
PE R∈Vi(cid:13) m world,m (u,v)∈R world,i (cid:13)
(cid:13) (cid:13)
i=1 m=1 2
Here V contains regions with reliable depth in view i, and sg denotes stop-gradient. Only valid-
i
depth pixels contribute to the target average. With this module, UNITAS pretrains jointly on RGB
andRGB-Ddata,anddepthmaybeabsentatinference.AppendixBevaluatestherouterwhendepth
isremovedattesttime.
3.4 PHYSICAL-TIMEPOINT-FLOWREPRESENTATION
Actionflowandsceneflow.Inthesameworldframe,actionandsceneflowsdescribedisplacement
from each query point’s current position. For query n at x , the target is {∆x }H , with
t,n n,k k=1
∆x = x −x . The elapsed time is τ , and point identity is preserved throughout the
n,k t+τk,n t,n k
trajectory.
For robots, we sample N = 20 points from the URDF-defined gripper geometry of each arm
g
andretaintheirlink-localcoordinates. Forwardkinematicsmapsthesepointsintotheworldframe
at each recorded joint configuration, preserving correspondence through arm and finger motion.
Humandemonstrationsuse21MANO-derivedkeypoints(Romeroetal.,2017)perobservedhand.
FollowingPointWorld(Huangetal.,2026),wemaskrobotpixelsusingtheURDFandcurrentjoint
state, back-project the remaining RGB-D pixels, and sample N scene query points. Simulator
s
states supply ground-truth correspondences where available and scene-flow loss is applied only to
validtrajectories. Atinference,scenepredictionrequirescurrent3Dquerycoordinatesfromdepth
orsuppliedgeometry.
Physical-time trajectory tokenizer. To better align different trajectories within diverse datasets,
weencodetimeinsecondsratherthanframeindices, usingτ = k/f atsamplingratef. Afixed
k
basisϕ ofτ/T ,withT =3ssharedacrossdatasets,givesequalelapsedtimesthesame
time max max
features;historyusesnegativeoffsets.AninputMLPmapseachdisplacementtoh ,andtemporal
n,k
MLPsmapϕ (τ )toFiLMparameters(a ,b )fortheencoderandthedecoder. Theencoder
time k k k
5

Underreview
| Simulation | Simulation |     | Real robot |     | Human |     |                              |     |
| ---------- | ---------- | --- | ---------- | --- | ----- | --- | ---------------------------- | --- |
|            |            |     |            |     |       |     | Single-dataset Mixed-dataset |     |
EEF XYZ error (mm)
20
10
5
3
2
|     |     |     |     |     |     |     | 0 50 100 150 | 200 |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- |
Gripper / hand flow Scene flow start → end Training steps (K)
Figure3: Sharedpoint-flowrepresentationsacrossdatasources. Left: gripper/handtrajectories
(purple)andscenetrajectories(yellow–blue),withRGBinsets.Right:RoboTwinend-effectorXYZ
error(mm). Thickcurvesshowexponentialmovingaverages(EMA)ofthethincurves.
poolsthetrajectoryintoonelatent,andthedecoderreadsthatlatentbackatarequestedtime:
|     |     |     | 1   | H                    |     |         |     |     |
| --- | --- | --- | --- | -------------------- | --- | ------- | --- | --- |
|     |     |     |     | (cid:88) [(1+aenc)⊙h |     | +benc], |     |     |
|     |     | z   | = √ |                      |     |         |     |     |
|     |     | n   | H   |                      | k   | n,k     | k   |     |
(8)
k=1
|     |     |            |      | (cid:2) |       |     | ec(cid:3) |     |
| --- | --- | ---------- | ---- | ------- | ----- | --- | --------- | --- |
|     |     | ∆(cid:99)x | =MLP | (1+ad   | ec)⊙z | +bd | .         |     |
|     |     | n,k        |      | out     | k     | n   | k         |     |
Paddingisexcludedfromthesum. Actionflow,sceneflow,andhistorysharethistokenizer,soeach
pointisonetokenregardlessoftrajectorylengthorsamplingdensity.Flowtokensareanchoredonly
at current world-frame points: positional embeddings as in Eq. 5 are added throughout denoising.
Decodinggivesx =x +∆(cid:99)x .AppendixA.2givesthebasisandthereconstructionstage.
|     | (cid:98)t+τk,n | t,n | n,k |     |     |     |     |     |
| --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
3.5 MODELARCHITECTURE
Coupledexperts. UNITASusesaMixture-of-Transformers(Liangetal.,2024)withtwodiffusion
transformers (Peebles & Xie, 2023): a point dynamics expert for action and scene flows, and an
action expert for the end-effector action chunk u. The point dynamics expert processes spatially
grounded primary-view VLM tokens, auxiliary-view features from the shared vision tower, and
historicalandfutureflowlatents.Ateachlayer,thesmalleractionexpertreadsthedynamicsexpert’s
observation/languagekeysandvalues(KV),togetherwithitsowncurrent-stateandnoisycommand
tokens. It predicts relative end-effector translation, rotation, and gripper openness at each future
timestep.
Attention structure. Let O and H be the observation/language and history tokens, and let A ,
|     |     |     | A   |     |     |     |     | γ   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
A clean , and S γs be the noisy action-flow, clean action-flow, and noisy scene latents. The context
[O,H ]isbidirectional. Eachaction-flowgroupattendstothiscontextandtoitself. Scenetokens
A
attendtothecontext,toA ,andtooneanother,butnottoA ,soscenepredictionconditionson
|     |     | clean |     |     |     | γ   |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- |
actionflowwithoutenteringaction-flowdenoising. Actionchunktokensattendtotheobservation
KV, the current end-effector state, and one another. They do not attend to future action-flow or
scene-flowtokens,sopolicy-onlyinferencecanskipbothfuture-flowbranches,asshowninFig.2.
Training. Wefirsttrainthetrajectorytokenizertoreconstructhistoricalandfutureactionflowand
available scene trajectories, then freeze it. Both experts learn through rectified flow (Liu et al.,
2022). For a clean target y, either a normalized trajectory latent or an action chunk, and noise
ϵ ∼ N(0,I), we form y γ = (1−γ)ϵ+γy and regress y −ϵ. Action flow and action chunk
shareγbutuseindependentnoise,whilesceneflowdrawsγ s independently. Duringtraining,scene
predictionconditionsoncleanaction-flowlatentsfromdemonstrations. Theobjectiveis
|     |     | L=λ A | L A +λ | s L scene | +λ ctrl L | ctrl +λ | PE L PE . | (9) |
| --- | --- | ----- | ------ | --------- | --------- | ------- | --------- | --- |
Thefirstthreetermsusemeansquarederror(MSE)lossestosuperviseactionflow,sceneflow,and
theactionchunk,withλ = λ = λ = 1. L isEq.7,withλ = 0.1. Eachlossusesonly
|     |     | A s | ctrl |     | PE  |     | PE  |     |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- |
availableannotations,withmissingtargetsandabsentarmslotsmasked.
Inference. ActionflowandactionchunkaredenoisedinparallelononeEulerschedule. Generated
actionflow,oranexternallysuppliedtrajectoryinsimulatormode,thenconditionsscenedenoising.
The context and clean action-flow keys and values are cached and reused across scene-denoising
steps.Policy-onlyexecutionkeepstheobservationandhistorycontextanddenoisesonlyu,skipping
bothpointdynamicsbranches. AppendixA.3givestheschedule,widths,andoptimization.
6

Underreview
| 4 POLICY EVALUATION |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Our policy evaluation tests whether representing interaction in a shared metric space supports ef-
fectiverobotcontrol. Weexaminetaskcompletionacrosssimulationbenchmarks,robustnesswhen
observationsandinitialstateschange,andexecutiononreal-worldrobots.
4.1 EXPERIMENTALSETUP
Trainingsettings. Weinitializethevision-languagebackbonefromFlorence-2(Xiaoetal.,2023)
andrandomlyinitializeallremainingcomponents. Weconsidertwotrainingsettings: (1)withpre-
training, UNITASispretrainedonamixtureofreal-robot,simulation,andhumanhanddemonstra-
tions,thenfine-tunedoneachdownstreambenchmarkordataset; (2)withoutpretraining, UNITAS
(w/oPretrain)isfine-tuneddirectlyoneachtargetbenchmarkordatasetwithoutthemixed-dataset
pretrainingstage. Moredetailedtrainingconfigurationsareprovidedintheappendix.
Baselines. We compare against VLA policies (Zheng et al., 2025; Sun et al., 2026; Black et al.,
2024; Physical Intelligence et al., 2025; Yang et al., 2026), video-based WAMs (Kim et al., 2026;
Liao et al., 2025; Bi et al., 2025; Li et al., 2026; Yuan et al., 2026b), and 3D-aware policies (Qu
etal.,2025;Wangetal.,2026b;Guoetal.,2026;Zhouetal.,2026a).
4.2 SIMULATIONBENCHMARKS
We evaluate UNITAS on single-arm and bimanual manipulation benchmarks. LIBERO (Liu et al.,
2023) includes Spatial, Object, Goal, and long-horizon LIBERO-10 suites; RoboTwin 2.0 (Chen
etal.,2025)covers50bimanualtasksunderCleanandRandomizedconditions. VLABench(Zhang
etal.,2024)testsobjectandinstructiongeneralizationacrossfivetracks,measuredbysuccessrate
(SR),progressscore(PS),andintentionscore(IS).LIBERO-Plus(Feietal.,2025)evaluatesrobust-
ness to seven types of observation, instruction, and initial-state perturbations. Detailed protocols
andper-taskresultsareprovidedintheappendix.
Manipulation performance. Tab. 1 reports policy performance across the evaluated simulation
benchmarks. OnLIBERO, UNITAS achievesastate-of-the-artaveragesuccessrateof99.8%,with
strong results on spatial and long-horizon tasks. Without mixed-dataset pretraining, it achieves
99.5%, also exceeding all baselines. On RoboTwin 2.0, UNITAS achieves 92.94% and 93.04%
under Clean and Randomized conditions, respectively. Its 1.7B model outperforms the compared
methods while using fewer parameters than Fast-WAM (6B) and Motus (8B). On VLABench, it
achieves56.2%SRcomparedwith48.1%forπ ,alongsideahigherprogressscore.
0.5
Robustnesstodistributionshifts.AsshowninTab.1,UNITASachievesthehighestoverallsuccess
rate of 89.1% on LIBERO-Plus. Appendix C reports the perturbation-wise results. Under camera
Table1: Policyperformance(%, ↑). Our1.7Bmodelisevaluatedwithandwithoutmixed-dataset
pretraining. Bold and underlined scores denote the best and second-best results, respectively.
| LIBERO-Plusranksuseone-decimalprecision. |        |     |        | Dashesdenoteunavailableresults. |             |             |     |          |     |
| ---------------------------------------- | ------ | --- | ------ | ------------------------------- | ----------- | ----------- | --- | -------- | --- |
|                                          | Params |     | LIBERO |                                 | LIBERO-Plus | RoboTwin2.0 |     | VLABench |     |
Method
(B)
|     |     | Spatial | Object Goal | 10 Avg. | Overall | Clean | Rand. | SR  | PS IS |
| --- | --- | ------- | ----------- | ------- | ------- | ----- | ----- | --- | ----- |
VLAPolicies
X-VLA 1.0 98.2 98.6 97.8 97.6 98.1 71.4 72.88 72.84 29.4 51.2 70.2
| VLA-JEPA | 2.0 | 96.2 | 99.6 97.2 95.8 | 97.2 | 77.9 | –   | –   | –   | – – |
| -------- | --- | ---- | -------------- | ---- | ---- | --- | --- | --- | --- |
π 3.0 96.8 98.8 95.8 85.2 94.15 53.6 65.92 58.40 29.4 44.1 55.0
0
π 0.5 3.0 98.8 98.2 98.0 92.4 96.9 85.7 82.74 76.76 48.1 62.3 64.9
| ABot-M0 | 4.0 | 98.8 | 99.8 99.0 96.6 | 98.6 | 80.5 | 80.42 | 81.16 | –   | – – |
| ------- | --- | ---- | -------------- | ---- | ---- | ----- | ----- | --- | --- |
Video-BasedWAMs
| CosmosPolicy | 2.0 | 98.1 | 100.0 98.2 97.6 | 98.5 | 82.2 | –   | –   | –   | – – |
| ------------ | --- | ---- | --------------- | ---- | ---- | --- | --- | --- | --- |
| GE-Act       | 2.2 | 98.2 | 97.6 95.8 94.4  | 96.5 | 80.3 | –   | –   | –   | – – |
LingBot-VA 5.3 98.5 99.6 97.2 98.5 98.5 69.5 92.93 91.55 – – –
Fast-WAM 6.0 98.2 100.0 97.0 95.2 97.6 51.5 91.88 91.78 – – –
| Motus | 8.0 | 96.8 | 99.8 96.6 97.6 | 97.7 | –   | 88.66 | 87.02 | –   | – – |
| ----- | --- | ---- | -------------- | ---- | --- | ----- | ----- | --- | --- |
3D-AwarePolicies
| SpatialVLA | 3.5 | 88.2   | 89.9 78.6 55.5 | 78.1 | –    | –    | –    | –   | – – |
| ---------- | --- | ------ | -------------- | ---- | ---- | ---- | ---- | --- | --- |
| LaMP       | 5.0 | 99.4   | 99.8 97.4 96.7 | 98.3 | 79.3 | –    | –    | –   | – – |
| X-WAM      | 6.7 | –      | – –            | – –  | –    | 89.8 | 90.7 | –   | – – |
| Dex-BEV    |     | – 98.2 | 98.0 97.8 97.0 | 97.8 | –    | 76.0 | 42.0 | –   | – – |
UNITAS(w/oPretrain) 1.7 99.8 99.8 99.4 99.0 99.5 86.5 91.08 90.74 50.3 64.3 71.2
UNITAS 1.7 99.8 100.0 100.0 99.4 99.8 89.1 92.94 93.04 56.2 67.6 69.3
7

Underreview
Table2: Quantitative
Organize Books
comparisonresultsofreal-robot
| 1   |     | 2   | 3   |     | 4   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
experiments(20trialspertask).
OrganizeBooks
|     |     |     |     |     |     | π   | 15/20(75%) |
| --- | --- | --- | --- | --- | --- | --- | ---------- |
0.5
|     |     | Pack the Ball |     |     |     | Fast-WAM | 13/20(65%) |
| --- | --- | ------------- | --- | --- | --- | -------- | ---------- |
| 1   |     | 2             | 3   |     | 4   | UNITAS   | 18/20(90%) |
PacktheBall
|     |     |     |     |     |     | π 0.5    | 11/20(55%) |
| --- | --- | --- | --- | --- | --- | -------- | ---------- |
|     |     |     |     |     |     | Fast-WAM | 12/20(60%) |
Figure4: Qualitativereal-robotrolloutsonOrganizeBooksand UNITAS 16/20(80%)
| Pack the | Ball. | Numbered | keyframes | show | task progression |     |     |
| -------- | ----- | -------- | --------- | ---- | ---------------- | --- | --- |
throughpreciseplacementandsequentialmanipulation.
perturbations, it achieves 82.1%, compared with 75.8% for Cosmos Policy and 64.5% for LaMP.
Bothtrainingsettingsshowstrongviewpointrobustness,consistentwithworld-coordinateground-
ingofvisualobservations.
Mixed-datasetpretrainingimprovesoverallsuccessby2.6percentagepoints,withthelargestgains
underrobotinitial-statechangesfrom84.8%to94.2%, andlanguageperturbationsfrom77.6%to
85.0%. Theseimprovementssuggestbettergeneralizationtochangesinbothphysicalconfiguration
andinstructionphrasing.AsillustratedinFig.3,addingotherdatasourceswhilekeepingthenumber
ofRoboTwinsamplesperbatchunchangedyieldslowerRoboTwintestXYZerror. Together,these
resultssupportpositivecross-datasettransferunderourunifiedmodelingformulation.
4.3 REAL-WORLDEVALUATION
Weevaluatetworeal-worldtasks:OrganizeBooksrequiresaligningbookswithshelfcompartments,
whilePacktheBallrequiresplacingaballinsideabagandclosingitszipper. Wecompareagainst
π and Fast-WAM using 20 trials per method per task. As shown in Tab. 2, UNITAS achieves
0.5
90% and 80% success on the two tasks, respectively, outperforming both baselines. Fig. 4 shows
representativeexecutions.
4.4 ABLATIONSTUDY
We ablate visual 3D positional encoding, action-flow supervision, action-flow history tokens, and
scene-flowsupervisiononLIBERO-Pluswithoutmixed-datasetpretraining. AsshowninTab.3,the
firstthreeablationsuseareferencemodelwithoutscene-flowsupervision,whichachieves85.74%
overallsuccess. Removing3Dpositionalencodingreducessuccessto81.35%,withthelargestdrop
undercameraperturbations, from79.11%to66.73%. Thishighlightstheroleofworld-coordinate
groundinginrelatingvisualobservationstorobotmotionandimprovinggeneralizationacrosscam-
eraviewpoints.
Removingaction-flowsupervisionreducesoverallsuccessto78.89%,supportingthevalueofgeo-
metricmotionsupervisionforactionlearning. Removingaction-flowhistorytokensreducesoverall
success to 75.92%, with a drop of 19.87 percentage points under robot initial-state perturbations,
suggestingthatrecentmotionprovidesusefulcontextbeyondthecurrentstate. Removingallthree
componentsyieldsaVLA-stylebaselinewith67.58%success.Addingscene-flowsupervisiontothe
referencemodelimprovesoverallsuccessfrom85.74%to86.47%,suggestingthatfuturescenepre-
Table3: LIBERO-Plusablationswithoutmixed-datasetpretraining. Checkmarksindicateenabled
components. Successrates(%)arereportedforeachperturbation;Overallpoolsall10,030evalua-
tionepisodes.
|     | Components |     |     |     | PerturbationType |     | Overall |
| --- | ---------- | --- | --- | --- | ---------------- | --- | ------- |
History
| Visual Action-flow |     | Scene-flow |     |     |     |     |     |
| ------------------ | --- | ---------- | --- | --- | --- | --- | --- |
3DPE Loss Tokens Loss Camera Robot Language Light Background Noise Layout
|     |     |     |     | 50.47 | 59.48 67.14 | 81.00 74.44 74.70 | 71.80 67.58 |
| --- | --- | --- | --- | ----- | ----------- | ----------------- | ----------- |
✓ ✓
|     |     |     |     | 66.73 | 79.29 75.21 | 94.57 92.19 84.13 | 84.46 81.35 |
| --- | --- | --- | --- | ----- | ----------- | ----------------- | ----------- |
| ✓   |     | ✓   |     | 75.05 | 76.13 66.17 | 90.72 87.45 86.45 | 75.74 78.89 |
| ✓   | ✓   |     |     | 69.04 | 64.71 72.41 | 88.88 80.48 81.01 | 79.80 75.92 |
| ✓   | ✓   | ✓   |     | 79.11 | 84.58 77.10 | 96.32 94.42 89.07 | 85.05 85.74 |
| ✓   | ✓   | ✓   | ✓   |       |             |                   |             |
|     |     |     |     | 81.86 | 84.84 77.62 | 96.67 94.42 89.82 | 85.11 86.47 |
8

Underreview
Book extraction Drawer opening Bimanual lifting Object release Real-world transfer
Figure 5: Action-conditioned scene-flow predictions. Top: observed RGB images. Middle: ini-
tial point clouds. Bottom: predicted endpoint point clouds and scene trajectories (color gradient),
conditionedonrecordedgrippertrajectories(purple). Translucentrobotmeshesindicatethecorre-
spondingposes.
dictionhelpslearnrepresentationsbeneficialtoactionprediction, consistentwithfindingsinother
WAMs(Yuanetal.,2026b).
5 ACTION-CONDITIONED WORLD MODELING
Evaluation setup. We evaluate action-conditioned scene prediction on held-out RoboTwin roll-
outsusingmatchedinitialobservationsandrobot-motionconditions,withsimulatorstatesproviding
ground-truthpointtrajectories.WecompareagainstPointWorld(Huangetal.,2026),whichdirectly
predicts 3D trajectories, and video-based Ctrl-World (Guo et al., 2025) and X-WAM (Guo et al.,
2026). Video predictions are lifted to 3D using SpatialTrackerV2 (Xiao et al., 2025), with Depth
Anything3(Linetal.,2025)forCtrl-WorldandnativedepthpredictionsforX-WAM.Botharecal-
ibratedusingonlyinitial-frameground-truthdepth. WereportMovingADEandFDEfortrajectory
andendpointaccuracy,StaticADEforbackgrounddrift,andMovingAcc@1cmforthefractionof
moving-pointpredictionswithin1cmofgroundtruth. Detailedevaluationprotocolsareprovidedin
AppendixF.1.
Table4: Action-conditionedscenepredictiononRoboTwin. Errorsareincm(↓); Acc@1cmisin
%(↑). DA3andSTv2denoteDepthAnything3andSpatialTrackerV2,respectively.
Method MovingADE↓ StaticADE↓ MovingFDE↓ MovingAcc@1cm↑
PointWorld 0.656 0.084 1.050 88.22
Ctrl-World+DA3+STv2 3.310 0.369 5.503 41.54
X-WAM+STv2 2.286 0.122 3.886 49.69
UNITAS 0.427 0.043 0.825 92.31
Action-conditioned scene prediction. UNITAS achieves the best results across all four metrics,
as shown in Tab. 4, reducing Moving ADE from 0.656 to 0.427cm relative to PointWorld while
improvingmoving-point accuracyand reducingstatic-region drift. Fig.5 illustratesobject motion
andresultingspatialconfigurationsconditionedongrippertrajectories.Thesimulationexamplesuse
trainingclipsandDROIDexampleshowsreal-worldscenepredictionwithoutreal-worldscene-flow
supervision.
Action-sceneconsistency.Wetestwhetherpredictedscenechangesagreewiththeconsequencesof
themodel’sownactionsonthreeRoboTwintasks. UNITAS achievesthebestconsistencybetween
predictedsceneevolutionandexecutedactionsamongthecomparedWAMs.AppendixF.2provides
theevaluationdetailsandfullresults.
6 CONCLUSION
UNITASadvancesaphysical-spaceformulationofworldactionmodeling: whattherobotobserves,
howitmoves,andhowthescenerespondsareexpressedwithinacommonmetricreference.Making
9

Underreview
interactiongeometryanexplicitpredictiontargetconnectsworldmodelingwithactionlearningand
provides a shared representation across differing embodiments and observation views. The strong
policyperformanceobservedinsimulationsupportsthevalueofthisformulationformanipulation.
More broadly, this work positions physical interaction as a unifying basis for embodied learning,
with robot behavior and environmental change represented as complementary parts of the same
process. Extendingthisfoundationtoreliablepredictionoverlongerinteractionsandbroaderreal-
worlddeploymentisapromisingdirectionforgeneral-purposerobotintelligence.
AIUSESTATEMENT
Generative AI tools were used to assist with literature review to identify related work and with
languagepolishing.
REFERENCES
AgiBot-World-Contributors, Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan
Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. AgiBot World Colosseo: A
large-scalemanipulationplatformforscalableandintelligentembodiedsystems. arXivpreprint
arXiv:2503.06669,2025.
Homanga Bharadhwaj, Roozbeh Mottaghi, Abhinav Gupta, and Shubham Tulsiani. Track2Act:
Predicting point tracks from internet videos enables generalizable robot manipulation. arXiv
preprint arXiv:2405.01527, 2024. doi: 10.48550/arXiv.2405.01527. URL http://arxiv.
org/abs/2405.01527.
HongzheBi,HengkaiTan,ShenghaoXie,ZeyuanWang,ShuheHuang,HaitianLiu,RuowenZhao,
YaoFeng,ChendongXiang,YinzeRong,HongyanZhao,HanyuLiu,ZhizhongSu,LeiMa,Hang
Su,andJunZhu. Motus: Aunifiedlatentactionworldmodel. arXivpreprintarXiv:2512.13030,
2025. doi: 10.48550/arXiv.2512.13030. URLhttp://arxiv.org/abs/2512.13030.
Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo
Fusai,LachyGroom,KarolHausman,BrianIchter,SzymonJakubczak,TimJones,LiyimingKe,
SergeyLevine,AdrianLi-Bell,MohithMothukuri,SurajNair,KarlPertsch,LucyXiaoyangShi,
James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. π : A vision-
0
language-action flow model for general robot control. arXiv preprint arXiv:2410.24164, 2024.
doi: 10.48550/arXiv.2410.24164. URLhttp://arxiv.org/abs/2410.24164.
JunCen,ChaohuiYu,HangjieYuan,YumingJiang,SitengHuang,JiayanGuo,XinLi,YibingSong,
HaoLuo,FanWang,DeliZhao,andHaoChen. WorldVLA:Towardsautoregressiveactionworld
model. arXiv preprint arXiv:2506.21539, 2025. URL http://arxiv.org/abs/2506.
21539.
JialeiChen,KaiWang,KangChen,ShuaihangChen,FengGao,WenhaoTang,ZhiyuanLi,Weilin
Liu,ZhuyuYao,BoxunLi,YuanboXu,andChaoYu. LaWAM:Latentworldactionmodelsfor
efficientdynamics-awarerobotpolicies.arXivpreprintarXiv:2606.15768,2026a.doi:10.48550/
arXiv.2606.15768. URLhttp://arxiv.org/abs/2606.15768.
Ronghan Chen, Yandan Yang, Zuojin Tang, Dongjie Huo, Tong Lin, Haoning Wu, Haoyun Liu,
YuzhiChen,LuluZheng,BotaiYuan,TianlunLi,MingxinWang,DekangQi,BinHu,WeiMei,
YuzeXuan,HaolongYang,YanqingZhu,MuXu,ZhihengMa,andXinyuanChang.ABot-M0.5:
Unified Mobility-and-Manipulation World Action Model. arXiv preprint arXiv:2607.00678,
2026b. URLhttp://arxiv.org/abs/2607.00678.
Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xian-
liang Lin, Yiheng Ge, Zhenyu Gu, et al. RoboTwin 2.0: A scalable data generator and bench-
markwithstrongdomainrandomizationforrobustbimanualroboticmanipulation.arXivpreprint
arXiv:2506.18088,2025.
Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ
Tedrake,andShuranSong. Universalmanipulationinterface: In-the-wildrobotteachingwithout
in-the-wild robots. arXiv preprint arXiv:2402.10329, 2024. doi: 10.48550/arXiv.2402.10329.
URLhttp://arxiv.org/abs/2402.10329.
10

Underreview
Karthik Dharmarajan, Wenlong Huang, Jiajun Wu, Li Fei-Fei, and Ruohan Zhang. Dream2Flow:
Bridging video generation and open-world manipulation with 3D object flow. arXiv preprint
arXiv:2512.24766,2025.doi:10.48550/arXiv.2512.24766.URLhttp://arxiv.org/abs/
2512.24766.
Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu,
andCewuLu. RH20T:Acomprehensiveroboticdatasetforlearningdiverseskills inone-shot.
arXivpreprintarXiv:2307.00595,2023. URLhttps://arxiv.org/abs/2307.00595.
SenyuFei,SiyinWang,JunhaoShi,ZihaoDai,JikunCai,PengfangQian,LiJi,XinzheHe,Shiduo
Zhang,ZhaoyeFei,JinlanFu,JingjingGong,andXipengQiu. LIBERO-Plus: In-depthRobust-
nessAnalysisofVision-Language-ActionModels. arXivpreprintarXiv:2510.13626,2025. URL
http://arxiv.org/abs/2510.13626.
JunGuo,QiweiLi,PeiyanLi,ZilongChen,NanSun,YifeiSu,HeyunWang,YuanZhang,Xing-
hang Li, and Huaping Liu. Unified 4D world action modeling from video priors with asyn-
chronous denoising. arXiv preprint arXiv:2604.26694, 2026. URL http://arxiv.org/
abs/2604.26694.
YanjiangGuo,LucyXiaoyangShi,JianyuChen,etal.Ctrl-World:AControllableGenerativeWorld
ModelforRobotManipulation,2025. URLhttps://arxiv.org/abs/2510.10125v1.
Jihoon Hong, Julian Skifstad, Qiyue Dai, Alice Chan, and Glen Chou. Steering robustness
into world action models via mechanistic interpretability and optimal control. arXiv preprint
arXiv:2607.14943,2026. URLhttp://arxiv.org/abs/2607.14943.
YuchengHu,YanjiangGuo,PengchaoWang,XiaoyuChen,Yen-JenWang,JiankeZhang,Koushil
Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy
with predictive visual representations. arXiv preprint arXiv:2412.14803, 2024. URL http:
//arxiv.org/abs/2412.14803.
Wenlong Huang, Yu-Wei Chao, Arsalan Mousavian, Ming-Yu Liu, Dieter Fox, Kaichun Mo, and
Li Fei-Fei. PointWorld: Scaling 3D world models for in-the-wild robotic manipulation. arXiv
preprintarXiv:2601.03782,2026. URLhttp://arxiv.org/abs/2601.03782.
AlexanderKhazatsky,KarlPertsch,SurajNair,etal.DROID:Alarge-scalein-the-wildrobotmanip-
ulationdataset. arXivpreprintarXiv:2403.12945, 2024. URLhttps://arxiv.org/abs/
2403.12945.
Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair,
Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Ben-
jamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn.
OpenVLA: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246,
2024. doi: 10.48550/arXiv.2406.09246. URLhttp://arxiv.org/abs/2406.09246.
MooJinKim,YihuaiGao,Tsung-YiLin,Yen-ChenLin,YunhaoGe,GraceLam,PercyLiang,Shu-
ranSong,Ming-YuLiu,ChelseaFinn,andJinweiGu. CosmosPolicy: Fine-TuningVideoMod-
els for Visuomotor Control and Planning, 2026. URL https://arxiv.org/abs/2601.
16163v1.
LinLi,QihangZhang,YimingLuo,ShuaiYang,RuilinWang,FeiHan,MingruiYu,ZelinGao,Nan
Xue, XingZhu, YujunShen, andYinghaoXu. Causalworldmodelingforrobotcontrol. arXiv
preprintarXiv:2601.21998,2026. URLhttp://arxiv.org/abs/2601.21998.
QixiuLi,YuDeng,YaoboLiang,LinLuo,LeiZhou,ChengtangYao,LingqiZeng,ZhiyuanFeng,
HuizhiLiang,SichengXu,YizhongZhang,XiChen,HaoChen,LilySun,DongChen,Jiaolong
Yang,andBainingGuo. Scalablevision-language-actionmodelpretrainingforroboticmanipu-
lationwithreal-lifehumanactivityvideos. arXivpreprintarXiv:2510.21571,2025a.
ShuangLi,YihuaiGao,DorsaSadigh,andShuranSong.Unifiedvideoactionmodel.arXivpreprint
arXiv:2503.00200,2025b. URLhttp://arxiv.org/abs/2503.00200.
11

Underreview
WeixinLiang,LiliYu,LiangLuo,SrinivasanIyer,NingDong,ChuntingZhou,GargiGhosh,Mike
Lewis,Wen-tauYih,LukeZettlemoyer,andXiVictoriaLin. Mixture-of-Transformers: ASparse
andScalableArchitectureforMulti-ModalFoundationModels.arXivpreprintarXiv:2411.04996,
2024. URLhttps://arxiv.org/abs/2411.04996.
Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu,
Jingbin Cai, Si Liu, Jianlan Luo, Liliang Chen, Shuicheng Yan, Maoqing Yao, and Guanghui
Ren. GenieEnvisioner: AUnifiedWorldFoundationPlatformforRoboticManipulation,2025.
URLhttps://arxiv.org/abs/2508.05635v2.
BokaiLin, YifuXu, XinyuZhan, HongjieFang, JialinTian, Fu-ChengZhang, Yong-LuLi, Cewu
Lu,andLixinYang. ChronoFlow-Policy: Unifyingpast-current-futureinteractionflowinvisuo-
motorpolicylearning. arXivpreprintarXiv:2606.31493,2026. doi:10.48550/arXiv.2606.31493.
URLhttp://arxiv.org/abs/2606.31493.
Haotong Lin, Sili Chen, Jun Hao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, and
Bingyi Kang. Depth Anything 3: Recovering the visual space from any views. arXiv preprint
arXiv:2511.10647,2025. URLhttp://arxiv.org/abs/2511.10647.
BoLiu,YifengZhu,ChongkaiGao,YihaoFeng,QiangLiu,YukeZhu,andPeterStone. LIBERO:
Benchmarkingknowledgetransferforlifelongrobotlearning. arXivpreprintarXiv:2306.03310,
2023. URLhttps://arxiv.org/abs/2306.03310.
Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu,
HangSu,andJunZhu. RDT-1B:adiffusionfoundationmodelforbimanualmanipulation. arXiv
preprintarXiv:2410.07864,2024. URLhttp://arxiv.org/abs/2410.07864.
Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate
and transfer data with rectified flow. arXiv preprint arXiv:2209.03003, 2022. URL http:
//arxiv.org/abs/2209.03003.
William Peebles and Saining Xie. Scalable diffusion models with transformers. In Proceed-
ings of the IEEE/CVF International Conference on Computer Vision, pp. 4195–4205, 2023.
URL http://openaccess.thecvf.com/content/ICCV2023/html/Peebles_
Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html.
Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees,
ChelseaFinn, andSergeyLevine. Fast: Efficientactiontokenizationforvision-language-action
models. arXiv preprint arXiv:2501.09747, 2025. URL http://arxiv.org/abs/2501.
09747.
PhysicalIntelligence,KevinBlack,NoahBrown,JamesDarpinian,etal. π : Avision-language-
0.5
actionmodelwithopen-worldgeneralization. arXivpreprintarXiv:2504.16054, 2025. doi: 10.
48550/arXiv.2504.16054. URLhttp://arxiv.org/abs/2504.16054.
Delin Qu, Haoming Song, Qizhi Chen, Dong Wang, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang
Wang, Jiayuan Gu, Bin Zhao, and Xuelong Li. SpatialVLA: Exploring spatial representations
forvisual-language-actionmodel. arXivpreprintarXiv:2501.15830,2025. doi: 10.48550/arXiv.
2501.15830. URLhttp://arxiv.org/abs/2501.15830.
JavierRomero,DimitriosTzionas,andMichaelJ.Black. Embodiedhands:Modelingandcapturing
hands and bodies together. ACM Transactions on Graphics, 36(6):245:1–245:17, 2017. URL
http://mano.is.tue.mpg.de/.
Yichao Shen, Fangyun Wei, Zhiying Du, Yaobo Liang, Yan Lu, Jiaolong Yang, Nanning Zheng,
andBainingGuo. VideoVLA:Videogeneratorscanbegeneralizablerobotmanipulators. arXiv
preprintarXiv:2512.06963,2025. URLhttp://arxiv.org/abs/2512.06963.
Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-actor: A multi-task transformer for
robotic manipulation. In Proceedings of the 6th Conference on Robot Learning, volume 205
of Proceedings of Machine Learning Research, pp. 785–799. PMLR, 2023. URL http://
proceedings.mlr.press/v205/shridhar23a.html.
12

Underreview
Jingwen Sun, Wenyao Zhang, Zekun Qi, Shaojie Ren, Zezhi Liu, Hanxin Zhu, Guangzhong Sun,
XinJin,andZhiboChen.VLA-JEPA:Enhancingvision-language-actionmodelwithlatentworld
model. arXivpreprintarXiv:2602.10098,2026. doi: 10.48550/arXiv.2602.10098. URLhttp:
//arxiv.org/abs/2602.10098.
RuixiangWang,QingmingLiu,YueciDeng,GuiliangLiu,ZhenLiu,andKuiJia. EVA:Aligning
videoworldmodelswithexecutablerobotactionsviainversedynamicsrewards. arXivpreprint
arXiv:2603.17808,2026a. URLhttps://arxiv.org/abs/2603.17808.
XinkaiWang,ChenyiWang,YifuXu,MingzheYe,FuchengZhang,JialinTian,XinyuZhan,Lifeng
Zhu, Cewu Lu, and Lixin Yang. LaMP: Learning vision-language-action policy with 3D scene
flowaslatentmotionprior. arXivpreprintarXiv:2603.25399,2026b. doi: 10.48550/arXiv.2603.
25399. URLhttp://arxiv.org/abs/2603.25399.
KunWu, ChengkaiHou, JiamingLiu, etal. RoboMIND:Benchmarkonmulti-embodimentintel-
ligence normative data for robot manipulation. arXiv preprint arXiv:2412.13877, 2024. URL
https://arxiv.org/abs/2412.13877.
BinXiao,HaipingWu,WeijianXu,XiyangDai,HoudongHu,YumaoLu,MichaelZeng,CeLiu,
andLuYuan. Florence-2: Advancingaunifiedrepresentationforavarietyofvisiontasks. arXiv
preprint arXiv:2311.06242, 2023. doi: 10.48550/arXiv.2311.06242. URL http://arxiv.
org/abs/2311.06242.
Yuxi Xiao, Jianyuan Wang, Nan Xue, Nikita Karaev, Yuri Makarov, Bingyi Kang, Xing Zhu, Hu-
jun Bao, Yujun Shen, and Xiaowei Zhou. SpatialTrackerV2: 3d point tracking made easy.
In Proceedings of the IEEE/CVF International Conference on Computer Vision, 2025. URL
http://arxiv.org/abs/2507.12462.
XiaomiRoboticsTeam,JunGuo,PiaopiaoJin,JasonLi,PeiyanLi,YingyanLi,FutengLiu,Wanli
Peng, Optimus Qin, Yifei Su, Nan Sun, Qiao Sun, Runze Suo, Heyun Wang, Yunhong Wang,
RujieWu,CaoyuXia,LinaZhang,JackZhao,GuoliangChen,WenlongChen,XinzeHe,BinLi,
QingLi, ZhuorongLi, HengQu, WenxuanSong, DiyunXiang, YifanXie, PeiranXu, Hangjun
Ye,WenYe,HanZhao,andQuanyunZhou. Xiaomi-Robotics-1: Scalingvision-language-action
modelswithover100Khoursofreal-worldtrajectories. arXivpreprintarXiv:2607.15330,2026.
doi: 10.48550/arXiv.2607.15330. URLhttp://arxiv.org/abs/2607.15330.
ZiyinXiong,NikolaosGkanatsios,MoritzReuss,andKaterinaFragkiadaki. GeomVLA:Unifying
scene, motion, andactionin3D. InProceedingsoftheConferenceonRobotLearning(CoRL),
2026. URLhttp://arxiv.org/abs/2609.13812.
Huilin Xu, Jian Ding, Jiakun Xu, Ruixiang Wang, Jun Chen, Jinjie Mai, Yanwei Fu, Bernard
Ghanem, Feng Xu, and Mohamed Elhoseiny. Diffusion-based imaginative coordination for
bimanualmanipulation. InProceedingsoftheIEEE/CVFInternationalConferenceonComputer
Vision, pp. 11469–11479, 2025a. doi: 10.1109/iccv51701.2025.01067. URL http://
openaccess.thecvf.com/content/ICCV2025/html/Xu_Diffusion-Based_
Imaginative_Coordination_for_Bimanual_Manipulation_ICCV_2025_
paper.html.
MengdaXu,ZhenjiaXu,YinghaoXu,ChengChi,GordonWetzstein,ManuelaVeloso,andShuran
Song. Flowasthecross-domainmanipulationinterface. InProceedingsofThe8thConference
onRobotLearning,volume270ofProceedingsofMachineLearningResearch,pp.2475–2499.
PMLR,2025b. URLhttp://proceedings.mlr.press/v270/xu25a.html.
Sherry Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Leslie Kaelbling, Dale Schu-
urmans, and Pieter Abbeel. Learning interactive real-world simulators. arXiv preprint
arXiv:2310.06114,2023. URLhttp://arxiv.org/abs/2310.06114.
YandanYang,ShuangZeng,TongLin,etal. ABot-M0: VLAFoundationModelforRoboticMa-
nipulationwithActionManifoldLearning,2026. URLhttps://arxiv.org/abs/2602.
11236v1.
13

Underreview
Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel
Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William
Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish
Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie,
Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan
Kautz, Yuke Zhu, Linxi “Jim” Fan, and Joel Jang. World action models are zero-shot poli-
cies. arXiv preprint arXiv:2602.15922, 2026. doi: 10.48550/arXiv.2602.15922. URL http:
//arxiv.org/abs/2602.15922.
Chengbo Yuan, Chuan Wen, Tong Zhang, and Yang Gao. General flow as foundation affordance
forscalablerobotlearning. arXivpreprintarXiv:2401.11439, 2024. doi: 10.48550/arXiv.2401.
11439. URLhttp://arxiv.org/abs/2401.11439.
Haoqi Yuan, Zhixuan Liang, Anzhe Chen, Ye Wang, Haoyang Li, Pei Lin, Yiyang Huang, Zixing
Lei,TongZhang,JiazhaoZhang,JieZhang,JingyangFan,GengzeZhou,QihangPeng,Chenxu
Lv,XiaoyueChen,AnYang,FeiHuang,JunyangLin,DayihengLiu,JingrenZhou,ChenfeiWu,
andXiong-HuiChen. Qwen-RobotManiptechnicalreport: Alignmentunlocksscaleforrobotic
manipulationfoundationmodels. arXivpreprintarXiv:2606.17846,2026a. doi: 10.48550/arXiv.
2606.17846. URLhttp://arxiv.org/abs/2606.17846.
Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-WAM: Do world action models
need test-time future imagination? arXiv preprint arXiv:2603.16666, 2026b. doi: 10.48550/
arXiv.2603.16666. URLhttp://arxiv.org/abs/2603.16666.
Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3D dif-
fusion policy: Generalizable visuomotor policy learning via simple 3D representations. In
Robotics: ScienceandSystems,2024. doi: 10.15607/RSS.2024.XX.067. URLhttp://www.
roboticsproceedings.org/rss20/p067.html.
QihangZhang, LinLi, LuyaoZhang, ShuaiYang, YimingLuo, ShuaitingLi, RuilinWang, Junke
Wang, Jiahao Shao, Gangwei Xu, Jiaming Zhou, Yishu Shen, Yudong Jin, Fangyi Xu, Shuailei
Ma, Jiaqi Liao, Guanxing Lu, Zifan Shi, Yongkun Wen, Yujie Zhao, Weixuan Tang, Xinyang
Wang,ChaojianLi,JiapengZhu,KaLeongCheng,NanXue,XingZhu,YujunShen,andYinghao
Xu. Native Video-Action Pretraining for Generalizable Robot Control, 2026a. URL https:
//arxiv.org/abs/2607.08639v1.
Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue
Yin, Zuxuan Wu, Yu-Gang Jiang, and Xipeng Qiu. VLABench: A large-scale benchmark for
language-conditioned robotics manipulation with long-horizon reasoning tasks. arXiv preprint
arXiv:2412.18194,2024. URLhttps://arxiv.org/abs/2412.18194.
ZhanguangZhang,ZhiyuanLi,BehnamRahmati,RuiHengYang,YintaoMa,AmirRasouli,Saj-
jad Pakdamansavoji, Yangzheng Wu, Lingfeng Zhang, Tongtong Cao, Feng Wen, Xinyu Wang,
XingyueQuan,andYingxueZhang. DoworldactionmodelsgeneralizebetterthanVLAs? aro-
bustnessstudy. arXivpreprintarXiv:2603.22078,2026b. doi: 10.48550/arXiv.2603.22078. URL
http://arxiv.org/abs/2603.22078.
Haoyu Zhao, Xingyue Zhao, Siteng Huang, Xin Li, Deli Zhao, and Zhongyu Li. RynnWorld-4D:
4D embodied world models for robotic manipulation. arXiv preprint arXiv:2607.06559, 2026.
URLhttp://arxiv.org/abs/2607.06559.
Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and
Chuang Gan. 3D-VLA: A 3D vision-language-action generative world model. arXiv preprint
arXiv:2403.09631,2024. URLhttp://arxiv.org/abs/2403.09631.
Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan.
TesserAct: Learning4Dembodiedworldmodels. arXivpreprintarXiv:2504.20995,2025. URL
http://arxiv.org/abs/2504.20995.
JinliangZheng,JianxiongLi,ZhihaoWang,DongxiuLiu,XiruiKang,YuchunFeng,YinanZheng,
Jiayin Zou, Yilun Chen, Jia Zeng, Ya-Qin Zhang, Jiangmiao Pang, Jingjing Liu, Tai Wang,
14

Underreview
and Xianyuan Zhan. X-VLA: Soft-prompted transformer as scalable cross-embodiment vision-
language-action model. arXiv preprint arXiv:2510.10274, 2025. doi: 10.48550/arXiv.2510.
10274. URLhttp://arxiv.org/abs/2510.10274.
Hongyan Zhi, Peihao Chen, Siyuan Zhou, Yubo Dong, Quanxi Wu, Lei Han, and Mingkui Tan.
3DFlowAction: Learning cross-embodiment manipulation from 3D flow world model. arXiv
preprint arXiv:2506.06199, 2025. doi: 10.48550/arXiv.2506.06199. URL http://arxiv.
org/abs/2506.06199.
Huayi Zhou, Wei Gao, Dekun Lu, Ruiji Liu, Zhanqi Zhang, Ziyang Zhang, Jian Chen, Wenlve
Zhou, Sheng Xu, Shumin Li, Kangyi Guo, Shichen Xu, Zixin Huang, Yongyi Su, and Kui Jia.
Dexterity-BEV:Aligning3Dworldandactionsforgeneralizablerobotpolicieslearning. arXiv
preprintarXiv:2606.02274,2026a. URLhttps://arxiv.org/abs/2606.02274v2.
Pengfei Zhou, Shengcong Chen, Di Chen, Jiaxu Wang, Rongjun Jin, Bingwen Zhu, Yike Pan,
SongenGu,KuanningWang,ShufengNan,etal.τ -WM:Aunifiedvideo-actionworldmodelfor
0
roboticmanipulation. arXivpreprintarXiv:2606.01027,2026b. URLhttp://arxiv.org/
abs/2606.01027.
ChuningZhu,RaymondYu,SiyuanFeng,BenjaminBurchfiel, PaarthShah,andAbhishekGupta.
Unified world models: Coupling video and action diffusion for pretraining on large robotic
datasets. arXiv preprint arXiv:2504.02792, 2025. URL http://arxiv.org/abs/2504.
02792.
15

Underreview
A IMPLEMENTATION AND TRAINING DETAILS
A.1 DATAMIXTUREANDTEMPORALSAMPLING
Heterogeneous data mixture. We pretrain on a mixture of nine data sources: RoboTwin (Chen
et al., 2025), LIBERO (Liu et al., 2023), VLABench (Zhang et al., 2024), DROID (Khazatsky
et al., 2024), AgiBot (AgiBot-World-Contributors et al., 2025), RoboMIND (Wu et al., 2024),
RH20T(Fangetal.,2023),VITRA(Lietal.,2025a),andourself-collectedW1data. Fig.6shows
representativeobservationsandalignedgeometry.
RoboTwin VLABench
LIBERO DROID
AGIBot W1
— — — —
RoboMIND VITRA Human Hand
Single RGB camera · no scene depth
Figure 6: Representative observations and aligned geometry from pretraining data. Robot
panels show RGB, depth where available, and scene points with robot overlays. VITRA shows
egocentricRGBandhandlandmarks.
Dataset-specific coordinate conventions. Robot data use a base or shared embodiment frame.
Wherespecifiedbythebimanualadapter,theoriginisthearm-basemidpoint,withorientationinher-
itedfromthesharedrootortorso. W1trainingcoordinatesarecenteredatthemedianend-effector
trajectory midpoint. For VITRA, source camera poses transform hand positions into the current
anchor’scameraframe,heldfixedthroughoutthewindow,with(x ,y ,z )=(z ,−x ,−y ).
M M M C C C
Temporalsampling. Tab.5reportsthetrajectorysamplingsettingsofpretraining. Theeffective
samplingratef accountsfortemporalsubsampling:H futureintervalsspanH/f secondsandyield
H +1 coordinates including the current anchor. We observe slower robot motion in AgiBot and
RoboMIND and therefore subsample their 45-Hz trajectories with stride 3 (15 Hz). This extends
thephysicaltimecoveredbyeachactionchunk,bringingitsspatialmotionextentclosertothatof
16

Underreview
chunksfromtheotherdatasets. VITRAuses6HzforEgo4D,8HzforEgoExo4DandSomething-
SomethingV2,and10HzforEPIC-KITCHENS.H specifiesthedatahistorywindow.
hist
Table 5: Pretraining trajectory sampling configuration. H and H count future and historical
hist
| intervals;durationisH/f |         | inseconds. | H +1includesthecurrentanchor. |        |              |     |     |
| ----------------------- | ------- | ---------- | ----------------------------- | ------ | ------------ | --- | --- |
|                         | Dataset | Source     |                               | f (Hz) | H H Duration | H+1 |     |
hist
|     | RoboTwin | Simulation |     | 15     | 20 20 1.33 | 21  |     |
| --- | -------- | ---------- | --- | ------ | ---------- | --- | --- |
|     | LIBERO   | Simulation |     | 20     | 20 20 1.00 | 21  |     |
|     | VLABench | Simulation |     | 10     | 15 15 1.50 | 16  |     |
|     | DROID    | Realrobot  |     | 15     | 20 20 1.33 | 21  |     |
|     | AgiBot   | Realrobot  |     | 15     | 20 20 1.33 | 21  |     |
|     | RoboMIND | Realrobot  |     | 15     | 20 20 1.33 | 21  |     |
|     | RH20T    | Realrobot  |     | 20     | 20 20 1.00 | 21  |     |
|     | W1-data  | Realrobot  |     | 15     | 20 20 1.33 | 21  |     |
|     | VITRA    | Humanhand  |     | 6/8/10 | 10 10 10/f | 11  |     |
A.2 PHYSICAL-TIMETRAJECTORYTOKENIZER
The encoder and decoder are defined in Eq. equation 8. The temporal basis takes timestamps in
| secondsonthesharedscaleT |     |     | =3s: |     |     |     |     |
| ------------------------ | --- | --- | ---- | --- | --- | --- | --- |
max
|     |         |                | (cid:34) |                            | (cid:35)     |       |      |
| --- | ------- | -------------- | -------- | -------------------------- | ------------ | ----- | ---- |
|     |         |                |          | π (cid:12) τ (cid:12) j/dz |              |       |      |
|     |         |                |          | (cid:12) (cid:12)          |              |       |      |
|     | [ϕ time | (τ)] j =sgn(τ) | sin      | (cid:12) (cid:12)          | , j =0,...,d | z −1, | (10) |
|     |         |                |          | 2 (cid:12)T (cid:12)       |              |       |      |
max
withlatentdimensiond =256.Futuretrajectoriesusepositiveoffsets;historyusesnegativeoffsets
z
anddisplacementsfrompastpositionstowardthecurrentanchor.AninputMLPproducesh from
n,k
∆x ,andseparatetemporalMLPsproducetheencoderanddecoderFiLMparameters.
n,k
Reconstructiontraining. WeminimizesquaredEuclideanerrorovervalidpoint–timepairs, av-
eraging the future and historical action losses and adding available scene reconstruction loss. The
trainedtokenizerisfrozen,anditslatentsarestandardizedwithfixedchannelwisetrainingstatistics
beforeworld-actionmodeltraining.
Spatial anchoring and query sets. The spatial anchor is separate from the displacement latent.
PointwiseFourierfeaturesofx t,n areprojectedtothepointdynamicsexpert’shiddendimensionand
addedtothetrajectorytokenthroughoutdenoising. Sharedtokenprocessingandorder-independent
attentionmasksmakepredictionpermutationequivariantwithineachquerytype: reorderingquery
points and their noise tokens together reorders the outputs. Variable query counts support sparse
object-levelpredictionordenserscenecoverage.
Held-outtrajectoryreconstruction. Weevaluatethefrozentokenizeron600held-outtrajectory
windows per source and trajectory type, none used for tokenizer training. Each point trajectory is
encoded into one token and decoded at its original physical timestamps. Tab. 6 reports ADE, the
mean Euclidean error across future timesteps, and FDE, the error at the final timestep, averaged
over point trajectories. The millimeter-scale errors indicate that the tokenizer preserves motion
informationacrossrobotactionflow,human-handactionflow,andsceneflowinthesesamples.
17

Underreview
Table6: Held-outtrajectoryreconstructionerrorsofthefrozentokenizer(mm).
Dashesindicateunavailablescene-flowgroundtruth.
|     | Actionflow |     | Sceneflow |     |
| --- | ---------- | --- | --------- | --- |
Datasource
|                  | ADE↓ | FDE↓ | ADE↓ | FDE↓ |
| ---------------- | ---- | ---- | ---- | ---- |
| RoboTwin         | 1.96 | 4.62 | 1.01 | 2.32 |
| LIBERO           | 2.54 | 6.05 | 0.78 | 1.56 |
| VLABench         | 3.38 | 6.25 | 0.94 | 1.89 |
| DROID            | 3.17 | 7.85 | –    | –    |
| AgiBot           | 2.26 | 4.62 | –    | –    |
| RoboMIND         | 3.48 | 7.60 | –    | –    |
| RH20T            | 3.16 | 4.91 | –    | –    |
| W1               | 1.70 | 3.33 | –    | –    |
| VITRA(humanhand) | 4.68 | 8.18 | –    | –    |
A.3 ARCHITECTUREANDOPTIMIZATION
Tab.7summarizesthemodelconfiguration.
| Table7: Modelarchitecture. | Parametercountsincludethefrozentokenizer. |     |            |         |
| -------------------------- | ----------------------------------------- | --- | ---------- | ------- |
| Component                  | Configuration                             |     | Params.(M) |         |
| VLM                        | Florence-2-large                          |     |            | 570.7   |
| Pointdynamicsexpert        | 28layers;width1,280;20heads               |     |            | 826.3   |
| Actionexpert               | 28layers;width640;10heads                 |     |            | 256.0   |
| Trajectorytokenizer        | Time-conditionedMLPs;latentdim.256        |     |            | 1.9     |
| Embeddingsandprojections   | Spatialandmodalityinterfaces              |     |            | 39.7    |
| Total                      |                                           |     |            | 1,694.5 |
Tokenstructureandattention. ThemaskisspecifiedinSec.3.5. Theactionexperthasthesame
depthasthedynamicsexpertandasmallerhiddendimension,withonenoisycommandtokenper
futuretimestep. Physicalexecutiontimeτ enterscommandtokensthroughFiLM,separatelyfrom
k
thedenoisingtime.
Flow matching and inference. The interpolation and the loss weights are given in Sec. 3.5. At
inference, action flow and commands use the same Euler schedule for 10 steps. Scene denoising
startsfromindependentnoise.
Trainingconfiguration. Wepretrainfor200Kstepswithatotalbatchsizeof1,024usingAdamW.
Thelearningratesare10−4 forthepointdynamicsandactionexpertsand10−5 fortheVLM,with
10−8.
weight decay We use constant learning rates after 1,000 steps of linear warmup. Training
uses64BW1000 HDCUs(64GiBeach)withFSDP.
Queriesandobjectives. Robotgrippersuse20querypointssampledfromURDF-definedgripper
geometryperarm;humanhandsuse21MANO-derivedkeypointsperobservedhand. Scenepoints
are voxelized and capped at 12,000 before random subsampling. The mixed-dataset run retains
1% (approximately 120 scene queries at the cap), with 5-mm voxels for the simulation datasets.
RGB inputs are resized to 224×224. The flow-matching weights are set in Sec. 3.5; unavailable
supervision is masked. This run uses a frustum-routing substitution probability of 0.1. Action
positioncoordinatesarescaledby10; rotationandgrippercoordinatesretainunitscale. Inference
uses10Eulerstepsforeachactiveexpert.
A.4 INFERENCEEFFICIENCY
We measure inference latency on a single NVIDIA GeForce RTX 5090 D. As shown in Tab. 8,
UNITAS directlyproducesexecutableactionswithoutgeneratingactionorsceneflowsin55.77ms
per chunk, providing a 2.20× speedup over jointly generating actions and action flow. With only
18

Underreview
1.7Bparameters,thismodeis2.81×fasterthanFast-WAMwithoutvideogenerationandsubstan-
tially faster than the joint video–action baselines Fast-WAM (Yuan et al., 2026b) and Motus (Bi
et al., 2025), supporting low-latency robot control. In world-model mode, the number of scene
queriescanbeadjustedatinferencetomatchthedesiredspatialsamplingdensityandcomputebud-
get. Reducingscenequeriesfrom3,000to1,024lowersjointpredictionlatencyfrom561.60msto
305.49ms,allowingaflexibletrade-offbetweenscenecoverageandinferencecost.
Table8: InferenceefficiencyonanRTX5090D.Latencyismeasuredperpredictionchunk; N
s
denotesthenumberofscenequeries.
|     | Method/outputmode |     |     | Params(B) | N   | Latency(ms) |
| --- | ----------------- | --- | --- | --------- | --- | ----------- |
s
|           | Fast-WAM(w/ovideo)        |     |     | 6.0         | –     | 156.81   |
| --------- | ------------------------- | --- | --- | ----------- | ----- | -------- |
|           | Fast-WAM(joint)           |     |     | 6.0         | –     | 579.79   |
|           | Motus                     |     |     | 8.0         | –     | 2,414.90 |
|           | UNITAS:actionsonly        |     |     | 1.7         | –     | 55.77    |
|           | UNITAS:actions+actionflow |     |     | 1.7         | –     | 122.51   |
|           | UNITAS:actions+bothflows  |     |     | 1.7         | 1,024 | 305.49   |
|           | UNITAS:actions+bothflows  |     |     | 1.7         | 3,000 | 561.60   |
| B SPATIAL | GROUNDING                 |     |     | DEPTH INPUT |       |          |
WITHOUT
Candidate depths, the router, and L are defined in Sec. 3.3, Eqs. equation 6 and equation 7.
PE
Duringtraining, routedfeaturesoccasionallyreplacedepth-derivedfeatures onvalidregions, with
the substitution rate reported in Appendix A.3. This section evaluates the router when depth is
removedattesttime.
B.1 EVALUATIONWITHOUTDEPTHINPUT
WeevaluatepolicyexecutiononLIBERO-Plusat100Ktrainingsteps, withoutmixed-datasetpre-
trainingorscene-flowsupervision. Tab.9comparesroutedPEwithoutdepthinputagainstground-
truthdepthPEusingthesamecheckpoint,andincludestheno-3D-PEbaselinefromTab.3. Camera
calibrationandrobot-stateinputsremainavailableinallsettings.
Table 9: Spatial grounding without depth input on LIBERO-Plus. Success rates (%, ↑) over
| 10,030episodes. | RoutedPEandground-truthdepthPEusethesamecheckpoint. |     |     |     |     |     |
| --------------- | --------------------------------------------------- | --- | --- | --- | --- | --- |
Visualspatialencoding Camera Robot Language Light Background Noise Layout Overall
| Novisual3DPE |     | 66.73 | 79.29 | 75.21 94.57 | 92.19 | 84.13 84.46 81.35 |
| ------------ | --- | ----- | ----- | ----------- | ----- | ----------------- |
RoutedPE(nodepth) 83.74 79.61 74.30 91.68 84.20 93.38 85.57 84.43
Ground-truthdepthPE 84.37 79.68 74.24 91.94 85.13 93.88 85.18 84.68
Results. Without depth input, routed PE achieves 84.43% overall success, closely matching the
84.68%obtainedwithground-truthdepthPE.Thegapofonly0.25percentagepointssupportsthe
effectiveness of distilling depth-derived spatial information into RGB-conditioned positional fea-
tures, preserving policy performance when depth is unavailable at inference. Compared with re-
moving visual 3D PE, routed PE improves overall success by 3.08 points, with the largest gains
undercamera-viewpointperturbationsandsensornoise.
| C DETAILED | LIBERO-PLUS |     | RESULTS |     |     |     |
| ---------- | ----------- | --- | ------- | --- | --- | --- |
Forbothtrainingsettings,wetrainUNITASonstandardLIBEROdemonstrationsandusethesame
checkpointsasintheLIBEROevaluationtoevaluatedirectlyonLIBERO-Plus. Noadditionaltrain-
ingoradaptationisperformedonLIBERO-Plus;thisisanout-of-distributionevaluation.
19

Underreview
Tab. 10 breaks down success rates across all seven perturbation types in LIBERO-Plus (Fei et al.,
2025);Tab.1reportsoverallsuccess. ThecomparisonadditionallyincludesOpenVLA(Kimetal.,
2024)andABot-M0.5(Chenetal.,2026b).
Table10: LIBERO-Plussuccessrates(%,↑)acrosssevenperturbationtypes. Robotdenotesinitial-
stateperturbations.
Method Params(B) Camera Robot Language Light Background Noise Layout Overall
| X-VLA |     | 1   | 23.4 | 89.7 | 75.7 88.2 96.0 | 62.7 | 71.8 | 71.4 |
| ----- | --- | --- | ---- | ---- | -------------- | ---- | ---- | ---- |
| π     |     | 3   | 13.8 | 6.0  | 58.8 85.0 81.4 | 79.0 | 68.9 | 53.6 |
0
| π 0.5        |     | 3   | 75.4 | 77.5 | 85.6 96.9 94.6 | 89.7 | 85.7 | 85.7 |
| ------------ | --- | --- | ---- | ---- | -------------- | ---- | ---- | ---- |
| OpenVLA      |     | 7   | 0.8  | 3.5  | 23.0 8.1 34.8  | 15.2 | 28.5 | 15.6 |
| CosmosPolicy |     | 2   | 75.8 | 63.3 | 81.7 96.5 88.9 | 92.7 | 82.2 | 82.2 |
| LingBot-VA   |     | 5.3 | 40.9 | 83.0 | 86.4 82.3 53.1 | 64.4 | 76.2 | 69.5 |
| Fast-WAM     |     | 6   | 16.4 | 44.5 | 68.9 78.2 53.7 | 37.7 | 60.7 | 51.5 |
| ABot-M0.5    |     | 6   | 70.5 | 87.4 | 88.6 94.0 89.7 | 75.5 | 85.2 | 83.4 |
| LaMP         |     | 5   | 64.5 | 69.6 | 88.2 95.3 97.4 | 76.9 | 73.8 | 79.3 |
UNITAS(w/oPretrain) 1.7 81.9 84.8 77.6 96.7 94.4 89.8 85.1 86.5
| UNITAS     |          | 1.7 | 82.1    | 94.2 | 85.0 98.1 96.3 | 84.5 | 87.7 | 89.1 |
| ---------- | -------- | --- | ------- | ---- | -------------- | ---- | ---- | ---- |
| D DETAILED | VLABENCH |     | RESULTS |      |                |      |      |      |
Tab. 11 reports five evaluation tracks: in-distribution, cross-category, commonsense, semantic in-
struction, and unseen texture (Tracks 1, 2, 3, 4, and 6). The comparison additionally includes
π -FAST(Pertschetal.,2025).
0
Table11: DetailedVLABenchresults(%). SR,PS,andISdenotesuccessrate,progressscore,and
intentionscore,respectively(all↑).
| Method |     |      | In-distribution |      | Cross-category |      | Commonsense |      |
| ------ | --- | ---- | --------------- | ---- | -------------- | ---- | ----------- | ---- |
|        |     | SR   | PS              | IS   | SR PS IS       | SR   | PS          | IS   |
| π      |     | 47.0 | 62.7            | 67.8 | 21.2 33.6 44.0 | 29.1 | 43.0        | 54.9 |
0
| π 0 -FAST |     | 56.2 | 66.8 | 72.4 | 31.0 38.2 47.8 | 38.0 | 48.6 | 56.8 |
| --------- | --- | ---- | ---- | ---- | -------------- | ---- | ---- | ---- |
| X-VLA     |     | 40.0 | 66.5 | 88.0 | 11.0 24.0 42.0 | 33.0 | 51.7 | 66.0 |
| π         |     | 65.4 | 77.8 | 80.4 | 38.2 49.7 52.0 | 43.9 | 57.3 | 60.0 |
0.5
UNITAS(w/oPretrain) 62.0 76.5 80.2 25.4 37.2 45.7 49.0 63.4 72.8
| UNITAS  |     | 75.1                | 85.6 | 82.3 | 28.9 39.1 44.4 | 53.8 | 65.9 | 68.5 |
| ------- | --- | ------------------- | ---- | ---- | -------------- | ---- | ---- | ---- |
| Method  |     | Semanticinstruction |      |      | Unseentexture  |      | Avg. |      |
|         |     | SR                  | PS   | IS   | SR PS IS       | SR   | PS   | IS   |
| π 0     |     | 17.3                | 38.7 | 58.0 | 32.2 42.5 50.6 | 29.4 | 44.1 | 55.0 |
| π -FAST |     | 35.0                | 45.0 | 59.4 | 39.0 49.0 56.8 | 39.8 | 49.5 | 58.6 |
0
| X-VLA |     | 39.0 | 62.5 | 82.0 | 24.0 51.2 73.0 | 29.4 | 51.2 | 70.2 |
| ----- | --- | ---- | ---- | ---- | -------------- | ---- | ---- | ---- |
| π 0.5 |     | 48.2 | 64.2 | 67.0 | 44.9 62.3 65.0 | 48.1 | 62.3 | 64.9 |
UNITAS(w/oPretrain) 62.4 75.8 79.8 52.6 68.5 77.6 50.3 64.3 71.2
| UNITAS     |          | 67.7 | 79.9    | 78.7 | 55.4 67.4 72.7 | 56.2 | 67.6 | 69.3 |
| ---------- | -------- | ---- | ------- | ---- | -------------- | ---- | ---- | ---- |
| E DETAILED | ROBOTWIN |      | RESULTS |      |                |      |      |      |
Tab.12givesper-taskresultsforbothtrainingsettingsinTab.1. Eachsettingcontains50taskswith
100evaluationepisodespertask;averagesweightalltasksequally.
20

Underreview
Table12: DetailedRoboTwin2.0successrates(%,↑). CleanandRand.denotedemo cleanand
demo randomized. Allmethodsareevaluatedover100episodespertaskineachsetting.
UNITAS
| Task                |     | π0.5        | Motus       | Fast-WAM    | (w/oPretrain) | UNITAS      |
| ------------------- | --- | ----------- | ----------- | ----------- | ------------- | ----------- |
|                     |     | Clean Rand. | Clean Rand. | Clean Rand. | Clean Rand.   | Clean Rand. |
| AdjustBottle        |     | 100 99      | 89 93       | 100 100     | 100 98        | 100 100     |
| BeatBlockHammer     |     | 96 93       | 95 88       | 99 97       | 97 92         | 100 98      |
| BlocksRankingRGB    |     | 92 85       | 99 97       | 100 100     | 100 99        | 97 94       |
| BlocksRankingSize   |     | 49 26       | 75 63       | 94 98       | 91 83         | 78 82       |
| ClickAlarmclock     |     | 98 89       | 100 100     | 100 100     | 100 100       | 100 100     |
| ClickBell           |     | 99 66       | 100 100     | 100 100     | 100 100       | 100 100     |
| DumpBinBigbin       |     | 92 97       | 95 91       | 97 96       | 97 98         | 98 97       |
| GrabRoller          |     | 100 100     | 100 100     | 100 100     | 100 100       | 100 100     |
| HandoverBlock       |     | 66 57       | 86 73       | 95 81       | 88 74         | 96 84       |
| HandoverMic         |     | 98 97       | 78 63       | 99 100      | 100 99        | 100 97      |
| HangingMug          |     | 18 17       | 38 38       | 58 62       | 48 57         | 61 41       |
| LiftPot             |     | 96 85       | 96 99       | 100 100     | 98 99         | 99 99       |
| MoveCanPot          |     | 51 55       | 34 74       | 90 88       | 97 100        | 94 96       |
| MovePillbottlePad   |     | 84 61       | 93 96       | 100 99      | 99 99         | 93 98       |
| MovePlayingcardAway |     | 96 84       | 100 96      | 100 100     | 98 100        | 100 100     |
| MoveStaplerPad      |     | 56 42       | 83 85       | 77 64       | 54 50         | 79 78       |
| OpenLaptop          |     | 90 96       | 95 91       | 98 100      | 98 99         | 100 100     |
| OpenMicrowave       |     | 34 77       | 95 91       | 62 45       | 96 86         | 74 80       |
90 91
| PickDiverseBottles      |     | 81 71  |        | 80 85   | 84 81   | 86 88   |
| ----------------------- | --- | ------ | ------ | ------- | ------- | ------- |
| PickDualBottles         |     | 93 63  | 96 90  | 100 96  | 96 98   | 100 98  |
| PlaceA2BLeft            |     | 87 82  | 88 79  | 95 93   | 90 95   | 100 98  |
| PlaceA2BRight           |     | 87 84  | 91 87  | 93 99   | 92 95   | 93 98   |
| PlaceBreadBasket        |     | 77 64  | 91 94  | 91 93   | 95 98   | 95 91   |
| PlaceBreadSkillet       |     | 85 66  | 86 83  | 90 93   | 87 95   | 89 86   |
| PlaceBurgerFries        |     | 94 87  | 98 98  | 96 99   | 100 99  | 96 98   |
| PlaceCanBasket          |     | 62 62  | 81 76  | 71 69   | 72 74   | 77 92   |
| PlaceCansPlasticbox     |     | 94 84  | 98 94  | 99 96   | 99 97   | 99 99   |
| PlaceContainerPlate     |     | 99 95  | 98 99  | 96 100  | 99 95   | 100 99  |
| PlaceDualShoes          |     | 75 75  | 93 87  | 94 88   | 92 91   | 99 96   |
| PlaceEmptyCup           |     | 100 99 | 99 98  | 100 100 | 100 100 | 100 100 |
| PlaceFan                |     | 87 85  | 91 87  | 96 96   | 89 92   | 90 94   |
| PlaceMousePad           |     | 60 39  | 66 68  | 83 89   | 89 92   | 91 87   |
| PlaceObjectBasket       |     | 80 76  | 81 87  | 89 88   | 79 94   | 94 91   |
| PlaceObjectScale        |     | 86 80  | 88 85  | 90 97   | 91 94   | 91 91   |
| PlaceObjectStand        |     | 91 85  | 98 97  | 90 94   | 92 88   | 97 97   |
| PlacePhoneStand         |     | 81 81  | 87 86  | 97 99   | 85 89   | 89 95   |
| PlaceShoe               |     | 92 93  | 99 97  | 96 99   | 97 97   | 100 98  |
| PressStapler            |     | 87 83  | 93 98  | 90 97   | 98 98   | 98 96   |
| PutBottlesDustbin       |     | 84 79  | 81 79  | 95 90   | 87 90   | 85 98   |
| PutObjectCabinet        |     | 80 79  | 88 71  | 94 89   | 88 84   | 77 92   |
| RotateQRCode            |     | 89 87  | 89 73  | 93 89   | 91 91   | 92 92   |
| ScanObject              |     | 72 65  | 67 66  | 89 92   | 87 92   | 97 96   |
| ShakeBottle             |     | 99 97  | 100 97 | 100 100 | 100 97  | 100 99  |
| ShakeBottleHorizontally |     | 99 99  | 100 98 | 100 100 | 100 94  | 100 100 |
| StackBlocksThree        |     | 91 76  | 91 95  | 95 97   | 93 84   | 98 94   |
| StackBlocksTwo          |     | 97 100 | 100 98 | 100 100 | 99 98   | 100 96  |
| StackBowlsThree         |     | 77 71  | 79 87  | 80 81   | 84 87   | 84 85   |
| StackBowlsTwo           |     | 95 96  | 98 98  | 92 98   | 91 99   | 95 100  |
| StampSeal               |     | 79 55  | 93 92  | 90 94   | 79 63   | 83 92   |
| TurnSwitch              |     | 62 54  | 84 78  | 61 59   | 68 63   | 83 72   |
Average 82.74 76.76 88.66 87.02 91.88 91.78 91.08 90.74 92.94 93.04
| F WORLD | MODEL | EVALUATION | DETAILS |     |     |     |
| ------- | ----- | ---------- | ------- | --- | --- | --- |
F.1 ACTION-CONDITIONEDSCENEPREDICTION
Evaluation protocol. Tab. 4 evaluates 550 test clips from 50 RoboTwin tasks, with one Clean
andtenRandomizedepisodespertask. Eachepisodecontributesafixedwindownearitsmidpoint,
containing the current frame and 20 future recorded frames. Initial scene points are sampled with
a 1.5cm voxel grid. All methods share initial queries, point identities, ground-truth trajectories,
and robot-motion conditions. For video methods, queries are projected into the initial image us-
21

Underreview
ingcameracalibration,accountingforresizingandcropping;onlyin-frameprojectionsaretracked
by SpatialTrackerV2. Ctrl-World uses Depth Anything 3 depth, whereas X-WAM uses its native
depthpredictions. DepthscaleforCtrl-Worldandinverse-depthaffinecalibrationforX-WAMare
estimatedfrominitialobserveddepthandfixedthroughoutthevideo. Trackedtrajectoriesaretrans-
formedintoworldcoordinates,andtheirpredicteddisplacementsareanchoredatthesharedinitial
queries. Nofutureground-truthdepthortrajectoriesareusedforalignment.
Scoring. Inourevaluation,welabelapointasmovingwhenitsmaximumground-truthdisplace-
mentfromitsinitialpositionoverthe20futureframesexceeds1cm,andasstaticotherwise. These
labelsarefixedperclipandsharedacrossmethods.Wescorefutureframes4,8,12,16,20:ADEav-
eragesEuclideanerrorsovervalidpoint–framepairsineachgroup,MovingFDEmeasuresmoving-
point error at frame 20, and Moving Acc@1cm is the fraction of valid moving-point–frame pairs
withpredictionerroratmost1cm. Metricsarefirstcomputedperclip,averagedwithineachtask–
condition group, and then averaged equally across groups. Clips without valid moving points are
excludedonlyfromthecorrespondingmovingmetrics.
F.2 CLOSED-LOOPACTION–SCENECONSISTENCY
WeevaluatethreeRoboTwintasks,AdjustBottle,BeatBlockHammer,andBlocksRankingRGB,
underCleanandRandomizedconditions,yieldingsixsettings.Eachmethodisevaluatedover10tri-
alspersetting,for60trialsintotal. WecomparewithX-WAM(Guoetal.,2026),Fast-WAM(Yuan
et al., 2026b), LingBot-VA (Li et al., 2026), and Motus (Bi et al., 2025). Each generated action
chunk is executed in the simulator, and the resulting observation conditions the next prediction.
Modelsretaintheirnativepredictionhorizonsandarescoredatcompletedactionboundariesuntil
termination. Fast-WAMexecutesall32actionsratherthanreplanningafter24.
ForUNITAS,thepointdynamicsexpertgeneratesanactionflow,whiletheactionexpertseparately
generatesanexecutablecommandchunkfromthesameobservationandinstruction. Thedynamics
expert then predicts scene-flow trajectories conditioned on its generated action flow. We compare
thesepredictionswiththeground-truthscenetrajectoriesresultingfromexecutingtheactionexpert’s
commandchunkinthesimulator.
Trajectory extraction and scoring. Ground-truth query points follow their simulator objects or
links. SpatialTrackerV2 lifts video predictions using X-WAM’s native depth or Depth Anything
3 estimates for RGB-only models, with initial-frame depth calibration and query anchoring. We
applythe1cmdisplacementthresholdtolabelmovingpointswithineachscoredchunk. Metricsare
averagedwithinrounds, thenwithinepisodes, acrosstrialswithineachsetting, andfinallyequally
acrossthesixsettings. Roundswithoutvalidmovingpointsareexcludedonlyfrommoving-point
metrics;allepisodesareretainedregardlessoftaskoutcome.
Table 13: Closed-loop action–scene consistency on RoboTwin. Predictions are compared with
the scene evolution produced by executing the same model’s generated actions. Errors are in cm;
MovingAcc@1cmisin%.
Method MovingADE↓ StaticADE↓ MovingFDE↓ MovingAcc@1cm↑
X-WAM+STv2 2.579 0.166 4.056 35.55
Fast-WAM+STv2 3.554 0.586 5.133 30.37
LingBot-VA+STv2 2.603 0.810 4.716 33.64
Motus+STv2 3.216 0.318 6.778 35.66
UNITAS 1.211 0.054 2.020 64.26
Thesescoresmeasureaction–sceneconsistencyalongeachmodel’sownrolloutandincludevideo-
to-3Dreconstructionerrorforvideo-basedmethods.ForUNITAS,agreementbetweenpredictedand
observedscenechangesalsoprovidesindirectevidencethatitsgeneratedactionflowandexecutable
commandsareconsistentintheirsceneeffects.
22

Underreview
G ADDITIONAL ACTION-CONDITIONED SCENE PREDICTIONS
G.1 SCENEPREDICTIONINSIMULATION
Figs. 7–10 extend Fig. 5 with 19 training clips, showing RGB, initial points, predicted flows, and
ground-truthflows. Purpledenotesconditioninggrippermotion. Theseexamplesillustratelearned
geometryratherthanheld-outaccuracy.Fordenservisualization,werelaxpart-boundaryanddepth-
jump filters while retaining valid-depth and non-robot checks. Every displayed scene point is di-
rectlypredicted;initialRGBcolorsareretainedandunobservedsurfacesarenotsynthesized.
Observation Initial Predicted scene GT scene
RGB point cloud + action flow + action flow
Insert the chrysanthemum into the vase_seen.
Please take the book cybersecurity
Hold the cylindrical kitchenpot with both arms
Place red block and green block together at the center, then stack green block on top.
Figure 7: Additional scene-flow visualizations (1/4): insertion, extraction, bimanual lifting, and
blockstacking.
23

Underreview
Observation Initial Predicted scene GT scene
RGB point cloud + action flow + action flow
Put the black bowl in the top drawer of the cabinet.
Pull the rectangular microwave's handle using the left arm. (articulated motion)
Put the white mug on the plate.
Release the red playing-card box into the woven basket. (gravity)
Open the middle drawer of the cabinet. (articulated motion)
Figure8: Additionalscene-flowvisualizations(2/4): bowlandmugplacement,articulatedmotion,
andgravity-drivenmotionafterobjectrelease.
24

Underreview
Observation Initial Predicted scene GT scene
RGB point cloud + action flow + action flow
Pick up the book and place it in the back compartment of the caddy.
Carefully grab the dark drink bottle with logo head-up.
Put the wine bottle in the bottom drawer of the cabinet.
Place the red block on the blue pad.
Put the black bowl on top of the cabinet.
Figure 9: Additional scene-flow visualizations (3/4): book, bottle, block, and bowl manipulation
acrossLIBEROandRoboTwin.
25

Underreview
Observation Initial Predicted scene GT scene
RGB point cloud + action flow + action flow
Put the white mug on the left plate.
Open the drawer and place the blue-and-white playing-card box inside. (articulated motion)
Close the top drawer of the cabinet. (articulated motion)
Move the orange bottle toward the blue pad.
Open the microwave. (articulated motion)
Figure10: Additionalscene-flowvisualizations(4/4): objectplacement,draweropeningandclos-
ing,andmicrowaveopening.
26

Underreview
G.2 TRANSFERTOREAL-WORLDOBSERVATIONS
Fig.11showspredictionsonDROIDandRH20Tconditionedonground-truthgrippertrajectories.
Despitereceivingscene-flowsupervisiononlyfromsimulation,UNITAScapturesaction-conditioned
scene changes in real environments outside this supervision distribution. These qualitative results
suggestthatthelearnedinteractiondynamicscantransferfromsimulationtorealscenes.
Observation Initial Predicted midpoint Predicted endpoint
RGB point cloud + flows + flows
Lower the orange object into the metal pan.
Lift the grasped item toward the upper cabinet.
Lift the patterned cloth beside the coffee machine.
Move the orange object toward the metal pan.
Move the yellow turtle toy away from the shelf.
Figure11: Zero-shotscene-flowpredictionsonreal-worldobservations. Thefirstfourrowsare
fromDROIDandthelastisfromRH20T.ColumnsshowobservedRGB,initialpoints,andpredicted
midpointandendpointpointcloudswithscenetrajectories(orangetopurple)andground-truthgrip-
pertrajectoriesusedforconditioning(magenta). Noscene-trajectorygroundtruthisshown.
27