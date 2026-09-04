SmoothRL: Online Reinforcement Learning During
Asynchronous Execution
AstribotTeam
research@astribot.com
ProjectPage: https://www.astribot.com/research/SmoothRL
AuthorListinContributions
Abstract
Deploying robot policies in the physical world requires simultaneously satisfying two fun-
damentaldesiderata: reliability,asreflectedbyhightasksuccessrates,andsmoothreal-time
execution. However,deployingstate-of-the-artgeneralistmodels,includingVision-Language-
Action(VLA)modelsandWorld-ActionModels(WAMs),presentssignificantchallengeson
bothfronts. Achievingtheprecisionandrobustnessrequiredforreal-worlddeploymentne-
cessitatessample-efficientonlinereinforcementlearning(RL)toadaptpretrainedmodelsfor
reliabledeployment. Meanwhile, theincreasingscaleofrobotfoundationmodelshasledto
correspondinglyhigherinferencelatency. Tosatisfyreal-timeconstraintsunderhighlatency,
modern systems adopt asynchronous inference together with action chunking, overlapping
policycomputationwithchunkexecutiontohidelatencyandenablesmoothcontrol. Despite
their complementary roles, integrating asynchronous execution with gradient-based online
RLremainsunderexplored. WepresentSmoothRL,anonlineRLframeworkthatfine-tunesa
pretrainedpolicywithinanasynchronousinferenceloop. SmoothRLfollowsavalue-gradient
paradigm, directly updating the policy parameters using gradients of the action-value func-
tion with respect to the policy actions. To enable correct optimization under asynchronous
execution, SmoothRL explicitly models the asynchronous inference process during training.
Specifically, each generated action chunk is partitioned by frame index into three regions: a
committed region, which consists of actions committed by the previous inference cycle; an ex-
ecution region, which contains newly generated actions that are executed by the robot; and a
discarded region, which contains actions that will be superseded by the next inference cycle.
Gradientsarepropagatedonlythroughtheexecutionregion,ensuringthatpolicyoptimization
is aligned with the trajectory distribution induced by asynchronous execution. We evaluate
SmoothRLonreal-worldrobotictasksrequiringhighprecision,aswellashighlydynamictasks
thatnecessitateasynchronousexecution.
6202
guA
03
]OR.sc[
1v86792.8062:viXra

Velocity Acceleration Jerk
s/m ²s/m ³s/m
Base Policy Base Policy Base Policy
Online RL Online RL Online RL
Time Time Time
Figure1|Top: SmoothRLenablesonlineRLfine-tuningofpretrainedrobotpoliciesunderasynchronous
inference,supportinghighlydexterousanddynamictaskssuchasthrowinganobjectatatarget. Bottom:
SmoothRL produces smoother motion, reducing acceleration and jerk by 52% and 47%, respectively.
ValuesareRMSmeasurementsoftherightend-effector’sXYZmotionovereachactionchunkduringa
realautonomousthrowingrollout.
1. Introduction
RecentadvancesinVision-Language-Action(VLA)modelsandWorld-ActionModels(WAMs)
havedemonstratedremarkableprogresstowardendowingrobotswithgeneralmanipulation
capabilities [40, 42–49]. However, deploying such generalist policies in the physical world
requiressimultaneouslyaddressingtwofundamentalchallenges: reliabilityandsmoothreal-
timeexecution. Achievingtherobustnessrequiredfordiversereal-worldtaskssuchascutting
opensealedpackagesdemandssample-efficientonlinereinforcementlearning(RL).Meanwhile,
the increasing scale of robot foundation models has led to correspondingly higher inference
latency. Undersynchronousexecution,thislatencyliesdirectlyonthecontrolpath: therobot
mustpauseateverychunkboundarywhilewaitingforthenextforwardpasstocomplete. When
successdependsonmaintainingcontinuousmotion, suchpausescanseverelydegradeboth
tasksuccessandexecutionefficiency. Modernrobotsystemsthereforeadoptactionchunking
together with asynchronous inference, overlapping policy inference with action execution.
Asynchronous execution eliminates these pauses but introduces a discontinuity of its own:
eachincomingchunkisgeneratedfromanearlierobservation,soswitchingtoitcanproduce
a discontinuity at the junction. A family of chunk-stitching methods [1–4] therefore studies
howtomaintaincontinuitybetweennewlygeneratedactionsandthosealreadycommittedfor
execution. Althoughreliabilityandsmoothreal-timeexecutionarecomplementaryrequirements
for real-world deployment, they have largely been studied in isolation. Existing online RL
methodstypicallyoptimizepoliciesassumingsynchronousexecution,whiledeploymentalmost
invariablyreliesonasynchronousinference. Thismismatchcausesthepolicytobeoptimized
under dynamics that differ from those encountered at test time. We argue that online RL
shouldinsteadbeperformedunderthesameasynchronousexecutionparadigmusedduring
deployment: ReinforceinDeployment.
2

Pursuingreliabilityandsmoothreal-timeexecutionsimultaneouslyreducesthedesignspaceto
threeessentialrequirements. Online: thepolicyimprovesfromthedataitiscurrentlygenerating,
ratherthanthroughofflinetrainingrounds. Asynchronous: inferenceoverlapsexecutionso
thatmodelinferencelatencydoesnotlimitthecontrolfrequency. Value-gradient: thegradient
oftheaction-valuefunctionwithrespecttothepolicyactionsisbackpropagatedintothepolicy
parameters,allowingthelearningsignaltodirectlyoptimizethepolicy. Existingapproaches
eachsacrificeoneoftheserequirements,inthesameorder. OfflineRLseparateslearningfrom
deploymentbyconductingRLinofflinerounds,leavingdeploymentfreetobeasynchronous.
Estimated advantages influence policy updates through reweighting or conditioning, rather
thandirectgradientoptimizationthroughthevaluefunction[29,30]. SynchronousOnlineRL
performsonlinereinforcementlearningbybackpropagatinggradientsfromthevaluefunction
𝑄 into the policy parameters. While effective for adapting pretrained policies [7, 9, 11–13],
thesemethodsassumesynchronousexecution. AsynchronousRestrictedOnlineRLconsiders
online adaptation under asynchronous execution. However, policy optimization is confined
toalatentsteeringspaceratherthanthepolicyparametersthemselves,makingtheachievable
improvementultimatelyboundedbythedecodingcapabilityofthepretrainedbasepolicy[31].
Asynchronous Online RL, which satisfies all three requirements, is the focus of this work.
Underasynchronousexecution,eachgeneratedactionchunkisonlypartiallyexecutedbefore
anewlyinferredchunksupersedesitsremainingactions. However,policyupdatesshouldbe
drivenexclusivelybytheconsequencesoftheactionstherobotactuallyexecutes. Unlikethe
threesettingsabove,asynchronousonlineRLcannotavoidgradientcontaminationbydesign:
taking the value-gradient pathway while deploying asynchronously inevitably exposes the
policyparameterupdatetoun-executed,supersededactions. Theobjectiveitselfmusttherefore
eliminatethiscontamination,ratherthanrelyingontheexecutionschedule.
We present SmoothRL, a general framework for online RL fine-tuning of pretrained robot
policies under asynchronous inference, enabling highly dexterous and dynamic tasks, such
asthrowinganobjectatatarget,asillustratedinFigure1. Theframeworkfollowsthevalue-
gradientparadigm,wheretheaction-valuefunction𝑄 updatesthepolicyparametersdirectly
throughitsgradientwithrespecttothepolicyactions. Thisparadigmadmitseitherfine-tuning
thepretrainedbasepolicydirectlyorlearningalightweightpolicyontopofafrozenone;we
adopt the latter as one instantiation, where a frozen base policy generates reference action
chunks under a receding horizon and a trainable attached network in the raw action space
carriesalllearnableparameters. Underasynchronousexecution,eachgeneratedactionchunkis
partitionedaccordingtoitsexecutionstatusintothreeregions: acommittedregion,containing
actionsalreadyissuedduringthepreviousinferencecycle;anexecutionregion,containingnewly
generated actions that are actually executed by the robot; and a discarded region, containing
newlygeneratedactionsthataresupersededbythenextinferencecyclebeforeexecution. The
boundaries between these regions are determined by two distinct forward passes and are
unknownatchunkgenerationtime,unlesstheinferenceloopisconstrainedtoafixedlatency
budget. Moreover,becauseinferenceandexecutionoverlap,achunkbeginsexecutiononlyafter
theprecedingin-flightinferencehascompleted,makingeachdecisioninherentlyconcurrent[35]:
theactionchunkcurrentlyinflightispartofthestateagainstwhichthenextchunkisgenerated.
Thetwocontributionsbelowformalizetheresultingimplicationsfortraining:
• Gradienttruncationtotheexecutionregion. Holdingtheasynchronouslooptoalatency
budget of 𝑛 frames fixes both boundaries of the execution window, making the three
action-chunk regions a function of frame index alone. The value gradient ∇ 𝑎 𝑄 is then
computedonlywithrespecttotheexecutionregion𝑎 [𝑛,2𝑛),ensuringthatpolicyupdates
3

depend exclusively on actions whose consequences are observed. The critic, however,
retainsthecommittedregionaspartofitsinputfortworeasons: thechunk-skipbootstrap
is unbiased only when the critic is conditioned on the action sequence that generated
theintervalreward,whiletheactioncurrentlyinflightprovidesthestateaugmentation
requiredtomodeltheconcurrentdecisionprocess.
• Asynchronousexecutionembeddedinthetrainingloop. Theasynchronousinference
loop - where policy forward passes and action execution overlap in time - runs during
training rollouts and not only at deployment. Replay trajectories therefore record the
actions the robot actually executed under the same timing and execution schedule the
objectiveisdefinedagainst,ensuringthepolicyisneveroptimizedunderdynamicsitwill
notencounteratdeployment.
Afurtherbenefitofoperatingintherawactionspaceisthathumaninterventionslieinthesame
spaceasthepolicyoutputs. Consequently,ademonstratedchunkcanbeuseddirectly,without
latent inversion or a separate offline data-collection stage: it serves as a regression target for
thepolicyunderabehavioralcloninglossovertheexecutionregionandasatransitionforthe
criticunderthestandardTDbackup. WeevaluateSmoothRLonasuiteofreal-worldrobotic
manipulationtasksrequiringhighprecision,aswellashighlydynamictasksthatnecessitate
asynchronousexecution.
2. Related Work
Wefirstreviewmechanismsforasynchronouspolicydeployment,andthenorganizeexisting
RL approaches along the three dimensions introduced in §1: whether learning is online or
offline,whetherdeploymentissynchronousorasynchronous,andwhethervaluegradientsare
propagateddirectlytothepolicy.
2.1. AsynchronousPolicyDeployment
Receding-horizonactionchunkinghasbecomethestandarddeploymentparadigmforcontem-
porary large-scale generalist robot policies [5, 6, 40, 42, 47, 48]. Since generating each action
chunkrequiresacompletepolicyforwardpass,typicallytakingtenstohundredsofmilliseconds,
asynchronousinferenceisapracticalnecessity: synchronousper-segmentforwardswouldpin
controlfrequencytoanunacceptablerate[36–38]. Consequently,eachnewlygeneratedchunkis
conditionedonastaleobservationandisunawareoftheactionsexecutedsincethatobservation
was captured. As a result, successive chunks generally fail to connect smoothly along the
executedtrajectory, introducingvelocityoraccelerationdiscontinuitiesatchunkboundaries.
One line of work addresses this problem through consistency-aware chunk-stitching [1–4].
Thesemethodsconstrainthealready-consumedprefixofeachnewlygeneratedchunktomatch
theactionsthathavealreadybeenexecuted,whileleavingtheremaininghorizonunconstrained.
Arelatedapproachinsteadcorrectsanin-flightchunkusingnewlyacquiredobservations[39].
Over time, these methods have evolved from inference-time guidance external to the policy
toward training-time modeling within the policy, and from hard prefix constraints toward
soft interpolation. An orthogonal line of work employs trajectory blending [6, 29], which
smoothschunkboundariesbypost-processingtheoverlappingpredictionsofsuccessivechunks
usingadecayinginterpolationweight. Ratherthanconstrainingthepolicyoutputsthemselves,
trajectoryblendingoperatesonlyaftermultiplechunkshavebeengenerated. Althoughboth
4

approacheseliminatediscontinuities,theydifferfundamentallyinwhentheexecutedactionis
determined: chunkstitchingfixestheactionbeforeitisemittedbythepolicy,whereastrajectory
blendingdeterminesitonlyafterthechunksoverlappingthatinstantbecomeavailable. This
distinctionisinconsequentialforimitationlearningandofflineRL,wherebothfamilieshave
primarilybeenstudied. However,itbecomesdecisivefortheonlineRLobjective,whichrequires
theactionatwhichthevaluefunction𝑄 isevaluatedtobeexactlytheactionexecutedbythe
robot, while simultaneously preserving a differentiable path from that action to the policy
parameters. This requirement raises a new question for asynchronous online RL, which we
addressinthiswork.
2.2. OfflineRL
Offline RL consumes the learning signal entirely during training, leaving the policy fixed at
deployment. Methods such as 𝜒 [29] and RECAP [30] support asynchronous deployment:
0
theadvantageisestimatedbyaseparatevaluemodelandinfluencesthepolicyonlythrough
weighting(AWR[50])orconditioning(CFG-styleguidance[51]),ratherthanbybackpropagating
valuegradientsintothepolicyparameters. Conversely,CO-RFT[10]performsallchunk-level
𝑄-learningoffline(ChunkedCal-QL)butadoptssynchronousdeployment. Thecoexistenceof
bothdeploymentmodeswithinthisclassshowsthat,forofflineRL,asynchronousexecutionis
merelyaninference-schedulingchoiceanddoesnotalterthelearningsignal. Incontrast,our
methodclosestheactor-criticlooparoundreal-robotexecution,wherethemismatchbetween
generatedandexecutedactionsdirectlyaffectsthelearningsignal.
2.3. SynchronousOnlineRL
This body of work performs online actor-critic updates in the same loop as robot rollout.
All methods in this category follow the value-gradient paradigm, in which the action-value
functionbackpropagatesgradientsdirectlyintothepolicyparameters. Theydifferprimarily
in where reinforcement learning is applied: either on a lightweight module attached to a
frozen pretrained policy, or on the entire policy through end-to-end fine-tuning. One line
of work freezes the pretrained VLA and learns a chunk-level policy on top. RLT [9], whose
architectureourimplementationdirectlyadopts,appendsalearnableRLtokentoafrozenVLA
andconditionsachunk-levelactoronboththeresultingrepresentationandtheVLAreference
action. TheactorisoptimizedwithaTD3-style[58]off-policyobjective,whileabehavior-cloning
regularizerconstrainslearningtolocalcorrections. EXPO-FT[7]similarlyattachesaresidual
editingheadtoafrozenVLAandoptimizesitusingaSAC-style[60]actorobjectivetogether
withBest-of-𝑁 selection,placingitwithinthesamevalue-gradientframework. Othermethods
retain the frozen-base interface but learn per-step residual policies rather than chunk-level
ones[11–13,27,28],reducingtheRLoptimizationunitfromanactionchunktoasinglecontrol
step. Chunk-level off-policy methods outside the frozen-policy setting [34, 52] nevertheless
adoptthesamechunk-leveloptimizationunitasourapproach. Thissharedoptimizationunit
motivates our formalization of the action chunk as the fundamental RL optimization unit
(§3.2). In a per-step formulation, actions carry no frame index within a chunk, making it
impossible to express gradients that apply only to a selected sub-segment of that chunk. A
secondlineofworkappliesreinforcementlearningdirectlytotheentirepolicy. Representative
examplesincludeend-to-endtoken-leveloptimizationforVLAs[15–18],reinforcementlearning
offlow-anddiffusion-basedpolicies[8,19–22],andconsistency-distillationapproaches[24,25].
FQL [23], while operating in an offline-to-online rather than closed-loop real-robot setting,
5

distills a pretrained flow policy into a one-step policy that directly receives value gradients,
a design also explored as a variant of QAM [55]. LWD [26] closes the loop on real-robot
executionbyperformingfleet-scaleonlineupdateswithachunk-levelcriticandpropagating
∇ 𝑎 𝑄 into a flow-policy action head through an adjoint-matching formulation. Despite their
differences,allmethodsinthiscategoryassumesynchronousreceding-horizonexecution,so
partialchunkexecutionneverenterstheirformulation. Bycontrast,openingthedeployment
looptoasynchronousinferenceturnspartialexecutionintoaconstraintonthevalue-gradient
pathway. Ourmethodaddressesthisconstraintthroughchunk-rolepartitioningandgradient
truncation,bothdefinedoverframeindiceswithinanactionchunk. Becausetheformulation
operates directly on raw action chunks rather than a particular policy parameterization, it
appliesequallytoresidual-policyadaptationandend-to-endpolicyfine-tuning.
2.4. AsynchronousRestrictedOnlineRL
Onlineactor-criticlearningrequiresexactchunktransitions,yetasynchronousexecutioncauses
each generated action chunk to be only partially executed, contaminating those transitions.
Existing methods avoid this issue by keeping the value gradient, ∇ 𝑎 𝑄, away from the raw-
actionpolicyparameters. Instead,reinforcementlearningisperformedinlatentspace,through
value-based action selection, or by using the value function only to rank or verify sampled
candidates [53, 54]. Our method instead follows the value-gradient paradigm, embedding
asynchronousexecutiondirectlyintotheRLobjectiveasaknownoptimizationconstraint. GR-
RL[31]performsonlinelearningunderasynchronousexecution,butplacestheRLoptimization
variableinthelatentnoisespaceofafrozendiffusionpolicy[32]. Itlearnsalatent-noisepredictor,
whileafrozendecodermapstheoptimizedlatentbacktoactions. Optimizingthelatentnoise
thereforeselectsamongactionsalreadyrepresentedbythepretrainedpolicyprior. Consequently,
partialexecutionisboundedinitseffectratherthaneliminated: ifvalueestimationincludes
un-executedportionsofanactionchunk,theresultingerrormayalterwhichlatentcandidate
isselected,butthefrozendecoderensuresthateveryissuedactionremainswithintheaction
distributionrepresentedbythepretrainedprior. Thispropertyboundsnotonlytheerrorbut
alsotheattainableimprovement,whichremainslimitedbytheexpressivecapacityofthefrozen
decoder. Moreover, human intervention cannot be incorporated as direct policy regression
targetswithoutunreliablelatentinversion. Incontrast,ourmethodoptimizesdirectlyinraw
actionspace,allowinghumaninterventiondatatoservesimultaneouslyassupervisedregression
targetsandvalue-labeledonlinetransitions.
3. Method
Ourworkaddressesonesinglechallenge:
HowcanonlineRLfine-tuningbeintegratedintoanasynchronousdeploymentloop?
3.1. TheAsynchronousInferenceLoop
We exclusively consider an asynchronous inference setting to satisfy the smooth real-time
executionrequirementsofreal-worlddeployment,whichhasbecomethestandardparadigmfor
contemporarylarge-scalegeneralistrobotpolicies. Thebasepolicyinfersthenextactionchunk
whiletherobotcontinuesexecutingthecurrentone. Meanwhile,thecontrolprocessoperatesat
6

(a)latencyfluctuates:𝑑 𝑘and𝑐 𝑘varyfromchunktochunk
chunk𝑘−1 ···
committed(𝑑𝑘) execution(𝑐𝑘) discarded
chunk𝑘 ···
predictionstart predictionend
chunk𝑘+1 ···
𝑑𝑘+1 𝑐𝑘+1
(b)thesamescheduleheldtothebudget𝑛:𝑑 𝑘=𝑐 𝑘=𝑛forevery𝑘
chunk𝑘 ···
0 𝑛 2𝑛 𝐻
chunk𝑘+1 ···
committed execution discarded
Figure2|Chunkrolepartitioningunderasynchronousexecution. Thecommittedregionreusesactions
alreadyissuedbythepreviousinference,theexecutionregioncontainstheframesexecutedfromthe
currentchunk,andthediscardedregioncontainsframessupersededbythenextinference. Chunk𝑘’s
committedlength𝑑
𝑘
isdeterminedbythelatencyofitsowninference,whereasitsexecutionlength𝑐
𝑘
isdeterminedbythelatencyofthesubsequentinferencecycle. (a)Undervariableinferencelatency,𝑑 𝑘
and𝑐 𝑘 fluctuateindependentlyacrosschunks. (b)Thesamescheduleunderalatencybudgetof𝑛,where
𝑑 𝑘 =𝑐 𝑘 =𝑛foreverychunk,yieldingafixedexecutionwindow [𝑛,2𝑛). Section3.1detailsthepartition,
andSection3.3definesthelearningobjectivebasedonthepartition.
thedesiredcontrolfrequencyandalwaysissuesthelatestavailableactionwithoutwaitingfor
inferencetocomplete;onceanewchunkbecomesavailable,itimmediatelytakesoverexecution.
Thisdesigneffectivelyhidesinferencelatency.
Asynchronous execution introduces a fundamental consequence: a policy-generated action
chunkisonlypartiallyexecutedbytheenvironment. Wethereforepartitioneachactionchunk
ofhorizon 𝐻 intothreeregionsbyframeindex,accordingtohowtheasynchronousschedule
usesthegeneratedactions. Thecommittedregion [0,𝑑) containstheframesthatelapseduring
theinferencelatencyofthischunk. Itslength𝑑 isdeterminedbythecurrentinferencetime. By
thetimethechunkbecomesavailable,theseframeshavealreadypassed: thepreviouschunk
hassuppliedthecorrespondingactions,andthepredictionsinthisregioncanneveraffectthe
environment through the current chunk. The execution region [𝑑,𝑑+𝑐) corresponds to the
intervalduringwhichthischunkisthelatestavailablepolicyoutputbeforethenextinference
completes. Itslength𝑐isdeterminedbythearrivaltimeofthesubsequentchunk. Everyaction
inthisregionisissuedtotherobotexactlyasgenerated,makingittheonlypartofthechunk
thatdirectlydeterminestheresultingenvironmenttrajectory. Theremainingdiscardedregion
containsframesafterthenextchunkbecomesavailable. Theseactionsaresupersededbythe
newlyarrivedchunkandthereforeneverreachtheenvironment.
Stabilizingtheloopwithalatencybudget. Theboundariesbetweenchunkregions,illustrated
in Figure 2 (a), are stochastic in real deployments. Since they are determined by different
inference cycles, they fluctuate independently and are unknown when an action chunk is
generated. Rather than modeling this stochasticity, we eliminate it through a fixed latency
budget. Weestimateanupperbound𝑛ontheinferencetimeandenforceascheduledexecution
7

loop: eachchunkisrequested𝑛controlstepsbeforeitsfirstframeisdue. Ifinferencecompletes
earlier,thesystemwaits,ensuringthatchunkhandoveralwaysoccursatthepredefinedtime.
Consequently,bothregionlengthsarefixedbythesameconstant, 𝑑 = 𝑐 =𝑛. Foranyhorizon
𝐻 ≥ 2𝑛,thecommittedregionistherefore [0,𝑛),theexecutionregionis [𝑛,2𝑛),andthediscarded
regionis [2𝑛,𝐻) (Figure2(b)). Theslackbetweentheactualinferencelatencyandthebudget
𝑛isconvertedintowaitingtimeratherthanusedtoexploitfresherobservations. Inexchange,
everychunkisexecutedoveranidenticalwindowdeterminedsolelybyitsframeindices.
3.2. Gradient-basedRLinContinuousActionSpace
Thissubsectionreviewsthegeneralformulationofcontinuous-actionreinforcementlearning
used throughout the paper. Given a Markov decision process (MDP), a policy 𝜋 seeks to
maximizetheexpecteddiscountedreturn. Value-basedmethodsdefinetheaction-valuefunction
𝑄𝜋(𝑠,𝑎),whichsatisfiestheBellmanequation:
𝑄𝜋(𝑠,𝑎) =E
𝑟,𝑠′∼𝑃
(cid:2) 𝑟+𝛾𝑄𝜋(𝑠′ ,𝜋(𝑠′)) (cid:3)
, (1)
where 𝛾 isthediscountfactorand 𝑠′ isthesuccessorstatereachedafterexecutingaction 𝑎in
state 𝑠. Off-policy actor-critic methods alternate between two updates. The critic learns the
action-valuefunction𝑄 byfittingthetemporal-difference(TD)targetgivenbytheright-hand
sideoftheBellmanequationusingtransitionssampledfromareplaybuffer. Theactorthen
updatesthepolicyparameterstoincreasethepredictedactionvalue,i.e.,tomaximize𝑄.
Incontinuousactionspaces,maximizingtheactionvaluecanberealizedthroughtwodistinct
routes. One route improves actions through candidate selection, advantage weighting, or
latent-space guidance, without backpropagating ∇ 𝑎 𝑄 to the policy parameters that generate
the executed actions. Our framework instead follows the value-gradient route: the gradient
of the action-value function with respect to the action, ∇ 𝑎 𝑄, is backpropagated through the
deterministicpolicy𝑎 =𝜋
𝜃
(𝑠) tothepolicyparameters𝜃,
∇ 𝜃 𝐽
=E(cid:2)
∇ 𝑎 𝑄(𝑠,𝑎)
(cid:12)
(cid:12) 𝑎=𝜋 𝜃(𝑠) ·∇ 𝜃 𝜋 𝜃 (𝑠)
(cid:3)
, (2)
sothat𝑄 directlyupdatesthepolicythroughaction-spacegradients.
ActionChunkastheAtomicUnitofRL. Weformulatereinforcementlearningoveraction
chunks,treatingeachchunkasanatomicactionintheunderlyingMDP.Forachunkspanning
𝐻 frames, the transition is represented as (𝑠 𝑡,𝑎 𝑡:𝑡+𝐻,𝑟 𝑡,𝑠 𝑡+𝐻 ), where 𝑎 𝑡:𝑡+𝐻 is the action chunk
generatedbythepolicyatstate𝑠 𝑡,𝑟 𝑡 isthediscountedreturnaccumulatedduringexecutionof
thechunk,and𝑠 𝑡+𝐻 istheobservationafterthechunkhasbeenfullyexecuted. Whenindexing
frames relative to the start of a chunk rather than to the episode - as in the chunk regions
definedin§3.1-wedenotethechunkby𝑎 [0,𝐻) andasub-segmentby𝑎 [𝑖,𝑗). Thecorresponding
action-value function is written 𝑄(𝑠 𝑡,𝑎 𝑡:𝑡+𝐻 ), and its temporal-difference update follows the
chunk-skipBellmanbackup:
𝑄(𝑠 𝑡,𝑎 𝑡:𝑡+𝐻 ) ← 𝑟 𝑡 +𝛾𝐻𝑄(cid:0)𝑠 𝑡+𝐻, 𝜋(𝑠 𝑡+𝐻 ) (cid:1) . (3)
This backup remains unbiased because the critic is conditioned on the action sequence that
generatedtherewardoverthecorrespondinginterval. Thesameformulationhassincebeen
adopted by recent chunk-level RL methods (§2.3), where the action span on which the critic
is conditioned need not coincide with the span for which the policy is optimized [14]. Our
framework likewise adopts this formulation, with the modification required to account for
asynchronousexecution.
8

3.3. Chunk-LevelRLunderAsynchronousDeployment
Underasynchronousdeployment,directlyconcatenatingthetwocomponentsabove-allowing
∇ 𝑎 𝑄 to backpropagate through the entire chunk - would cause policy updates to depend on
generated actions that never reached the environment. Instead, we explicitly treat “which
segmentisactuallyexecuted”asaknownconstraintimposedbythedeploymentprocess.
Theregionsintroducedin§3.1wereoriginallydefinedsolelybytheexecutionschedule;here,
they are assigned distinct training roles. From this point onward, the span over which the
objective is defined is restricted to the first 2𝑛 frames of the chunk, with the committed and
execution regions of §3.1 each occupying one budget interval; the horizon 𝐻 the base policy
emits may be longer. We denote by 𝑎˜[0,𝑛) the actions actually executed by the robot in the
committed region of the current chunk. These actions were issued by the preceding chunk
andaretreatedasfixed,regardlessofhowtheyweregenerated. Theobjectivedefinedinthis
subsectionistherefore:
(cid:104) (cid:105)
max E 𝑄(cid:0)𝑠, 𝑎˜[0,𝑛), 𝜋 𝜃 (𝑠) [𝑛,2𝑛) (cid:1) s.t. (𝑎˜[0,𝑛), 𝜋 𝜃 (𝑠) [𝑛,2𝑛) ) ∈ E (4)
𝜃
where E denotes the set of chunks over [0,2𝑛) that are physically executable by the robot.
Importantly,admissibilityisapropertyofthefullchunkspan,notmerelytheexecutionregion:
achunkisincludedonlywhenitsexecutionisvalidwithinbothregionsandremainsconsistent
acrosstheboundaryatframe𝑛. Thediscardedregion [2𝑛,𝐻),whichfallsoutsidetheeffective
execution horizon, is therefore excluded entirely from the objective above. The chunk-skip
backupofEq.(3)isrestrictedtothesamespan: theintervalitspansis [0,2𝑛) ratherthanthe
fullhorizon 𝐻,sothereward𝑟 𝑡 accumulatesoverthose2𝑛frames,thebootstrapstateis 𝑠 𝑡+2𝑛,
andthediscountexponentis2𝑛. Thismodificationpreservestherequiredunbiasedbackup: the
criticisconditionedontheactionsequencethatactuallygeneratedtherewardovertheinterval,
namely𝑎˜[0,𝑛) followedby𝑎 [𝑛,2𝑛).
Value gradient truncation. From the policy’s perspective, the committed region induces
no valid environmental feedback for policy updates: as described in §3.1, these actions are
overwrittenbythoseissuedfromtheprecedingchunkandthereforedonotformavalidgradient
pathforthecurrentpolicy. Accordingly,thevaluegradientistruncatedtotheexecutionregion:
∇ 𝑎 𝑄 iscomputedonlywithrespectto𝑎 [𝑛,2𝑛). Thistruncationestablishesacrucialidentity: the
segmentreceivingthevaluegradientissimultaneouslythepolicyoutputandtheactionactually
executedbytheenvironment,makingtheresultinggradientwell-definedwithrespecttothe
policyparameters. Importantly,thetruncationappliesonlytothegradientpath,whilethecritic
continuestooperateonthefullactionchunk.
Criticoverthefullactionspan. Asynchronousexecutionturnsthissettingintoaconcurrent
decisionproblem. Theexecutionregiondoesnotbeginactingfrom 𝑠 𝑡,butfrom 𝑠 𝑡+𝑛,withthe
intervening frames being governed by the chunk already in flight. A critic conditioned only
on (𝑠 𝑡,𝑎 [𝑛,2𝑛) ) wouldthereforemarginalizeovertheunknowndistributionofin-flightchunks
presentinthereplaybuffer,which,intheoff-policysetting,reflectsbehaviorsinducedbyolder
policies. Aconcurrentdecisionprocessrequiresaugmentingthestatewithtwoquantities[35]:
the action currently in flight and the remaining time until its completion. In our setting, the
latencybudgetfixesthelattertotheconstant𝑛,whilechunk-stitchingconsistencymakesthe
9

formerdirectlyavailableat generation time: foreach newly generatedchunk, itscommitted
region exactly corresponds to the actions already issued by the preceding chunk. Recording
theseissuedactionsthereforeprovidestherequiredstateaugmentationbothfreelyandexactly.
The same latency budget that determines this augmentation also fixes the timescale of the
bootstrapchain,whichweanalyzefurtherin§5.
Smoothness. Theexecutable-setconstraintrestrictsnottheframesoverwhichthepolicycan
act,butthesetofchunksoverwhichtheoptimizationisperformed. Theactoralsoconditionson
thecommittedregion,butforadifferentreasonthanthecritic: sincethecommittedandexecution
regionsareconnectedatframeindex𝑛,acandidatechunkmustbeselectedwithawarenessofthe
trajectoryitmustcontinuefrom. Smoothnessinheritedfromthepretrainedpolicyisprovidedby
thedemonstrations,ratherthanexplicitlyenforced. However,oncethevalueobjectiveincreases
𝑄overtheexecutionregion,thissmoothnessisnolongerguaranteed. Continuitymusttherefore
bereintroducedasanexplicitconstraintintheobjective. Theoptimizationconsequentlysearches
onlyover E,transferringtherequirementofsmoothnessbacktothepolicy. Theformulation
aboveisdefinedwithrespecttothetimingmodelin§3.1;therefore,transitionsmustbecollected
underthesameexecutionsemantics. Theasynchronouslooprunsduringtrainingrolloutsrather
thanonlyatdeployment,ensuringthatthereplaybufferrecordstheactionsactuallyexecuted
bytherobot. Incontrast,transitionscollectedundersynchronousexecutionwouldcontainno
explicitregionboundariesfortheobjectivetoalignwith.
Explorationisfundamentaltoreinforcementlearning. However,explorationonarealrobotis
costly: failedtrialsconsumewall-clocktimeand, forcontact-richtasks, mayincurhardware
wear or damage. Consequently, human intervention during impending policy failures has
becomeastandardcomponentofreal-robotRLratherthanmerelyaconvenience[7,9,28,30].
The objective above naturally accommodates such interventions without modification. The
critic takes a state and an action chunk as input, and the target in Eq. (3) is independent of
thecontrollerthatgeneratedthechunk;thus,intervenedepisodescanbestoredinthereplay
bufferasordinarytransitions. Thestateaugmentationintroducedaboveremainsvalidunder
intervention: 𝑎˜[0,𝑛) isdefinedbytheactionsactuallyissuedratherthantheactionsproposed
by the policy, and therefore directly records human commands when intervention occurs.
Interpretinghumanactionsasvalue-estimatedactionsrequiresnoadditionaltransformationin
ourformulation,unlikesettingswheretheRLvariableisrepresentedinalatentactionspace
(§2.4). §3.4describesthecorrespondinginterventionmechanism.
Underasynchronousdeployment,twoactionsmustbedistinguished: theactionemittedbythe
policyandtheactionexecutedbytherobot. Optimizing𝑄 withrespecttotheformerimproves
behavioronlywhenthetwocoincide. Furthermore, theactionatwhich 𝑄 isevaluatedmust
admit a valid gradient path back to 𝜃. We refer to these two requirements as agreement and
differentiability, respectively. Issuing the policy output directly satisfies both by construction,
which is the setting assumed in Eq. (4); this is precisely where the two boundary-smoothing
familiesdiscussedin§2.1diverge. Aconsistencyconstraintmodifiesthechunkbeforeexecution,
ensuringthatthepolicyoutputandtheexecutedactionremainidentical. Incontrast,blending
isperformedonlyafterboththenewandpreviouschunksbecomeavailable. Topreservethe
agreementrequirement, thecriticmustevaluatetheblendedactionactuallyexecutedbythe
robot. Thetruncationprincipleintroducedabove-thatgradientspropagateonlythroughactions
that enter the environment - extends naturally to this setting. The value gradient should be
computedwithrespecttoeverychunkcontributingtotheexecutedwindow,restrictedtothe
segmentthatthechunkcontributes. Becausethesesegmentsaredisjointacrosstransitions,each
10

chunkisdifferentiatedexactlyonce. Thisextensionrequiresanobjectivehorizonexceeding2𝑛,
anadditionalactorforwardpassforeachcontributingchunktorecoveritsoutputunderthe
currentpolicyparameters,andareformulationofthecontinuityconstraintsaroundthemixing
operator(§5). Forsimplicity,weadoptdirectpolicyoutputexecutionandenforcesmoothness
throughconstrainedoptimization.
Asynchronous Execution
Committed Execution Intervention Discarded
Chunk1
Chunk0
Chunk2
Chunk0 Chunk1 Chunk2
t
0 n 2n 3n 4n
Data
Rollout
Buffer Online RL
Actor Action chunk
Base policy
UUppddaattee
Feature
Encoder Action chunk tt tt++nn tt++22nn
VLA
Critic
Image Lang … Issued action
Figure3|OneinstantiationofourasynchronousonlineRLframework. Thefrozenbasepolicyproduces
a latent representation 𝑧 𝑡 and a reference action chunk 𝑎¯𝑡:𝑡+2𝑛. A trainable attached network takes
[𝑧 𝑡,𝑠 𝑡,𝑎¯𝑡:𝑡+2𝑛 ] as input and predicts a bounded correction, which is added to the reference action to
producethefinalactionchunk. Thecriticisconditionedonthecorrectedactionchunk,whilegradients
arepropagatedtotheactoronlythroughtheexecutionregion(§3.3). Humaninterventionisapplied
totheissuedactioninthesamerawactionspace,allowingintervenedtrajectoriestobeincorporated
directlyintotraining(§3.4).
3.4. Instantiation
We provide a concrete instantiation of the proposed asynchronous online RL framework, as
illustratedinFigure3. OurimplementationfollowstheRLT[9]skeleton: afrozenbasepolicy
generatesreferenceactionchunks,whilealightweightTD3-styleactor-criticaccessesthebase
policy’sinternalrepresentationsthroughanRLtokenandpredictsaresidualactioncorrection.
Thefollowingparagraphsclarifywhatthisskeletonprovidesandwhereourimplementation
departsfromit. Theskeletonrequiresnostructuralmodificationtosatisfytherequirementsof
§3.3: itprovidesachunk-levelactor,makingframe-indexedgradienttruncationexpressible;
operates in the raw action space, eliminating the need to invert human interventions; and
exposesacriticinputtowhichthecommittedregioncanbeappendedasastop-gradientterm.
11

Inference starts Inference finishes
Inference delay, n
A1
A0 Issued action Absolute
Intervention
A1*
(a)Absoluteintervention.
Inference starts Inference finishes
Inference delay, n
A1
A0 Issued action R In e t s e i r d v u e a n l t ion
A1*
(b)Residualintervention.
Figure4|Twohumaninterventionmodesduringpolicydeployment. Undera,theteleoperatedaction
chunkisissueddirectlyandtheactoroutputisdiscarded. Underb,thehumaninputisaddedtotheactor
output,allowingtheoperatortomodifythepolicy-generatedchunk. Bothmodesaretreatedidentically
downstream: theactionactuallyissuedisrecordedin𝑎˜[0,𝑛) andusedastheBCtarget.
Keepingthebasepolicyfrozenandconfiningalltrainableparameterstoalightweightattached
networkalsomakeseachgradientstepinexpensiverelativetoabase-policyforwardpass. This
isimportantbecausetheupdaterateisboundedbyrolloutthroughput,whilethesmallnumber
oftrainableparametersmakesonlineoptimizationpracticalatthedatavolumegeneratedbya
realrobot. Thechoicesthatfollowarethereforeimplementationdetailsratherthanrequirements
of the framework: §3.1–§3.3 are formulated in terms of generic 𝜋 and 𝑄, and none of their
argumentsdependsonthisparticularinstantiation.
Humanintervention. Toevolvethepolicyduring deployment, wesupporttwohumanin-
terventionmodes,asillustratedinFigure4: absoluteinterventionandresidualintervention.
Interventionisactivatedanddeactivatedbyaswitchontheteleoperationdevice. Thetraining
loopcontinueswhilethehumanisincontrol: boththebasepolicyandtheattachednetwork
continuetoperforminference,whileonlytheissuedactionismodified. Underabsoluteinter-
vention, the teleoperated chunk is issued directly and the actor output is discarded. Under
residualintervention,thehumaninputisaddedtotheactoroutput,allowingtheoperatorto
modifythepolicy-generatedchunkratherthanreplaceit. Eachmodeissupportedbyasuitable
input device: absolute intervention uses VR teleoperation, where the operator’s hand pose
directly specifies the target action, while residual intervention uses a hand controller, where
stickdisplacementsspecifyactiondeltas.
Thetwointerventionmodesaresuitedtodifferenttaskregimes. Residualinterventionpreserves
thetemporalstructureoftheunderlyingactionchunkwhilemodifyingitstrajectory,allowing
the operator to correct the policy without disrupting its velocity profile. We therefore use it
12

fordynamictasks. Absoluteintervention,incontrast,givestheoperatorfullcontroloverthe
action chunk and is therefore suited to tasks requiring greater flexibility and high precision,
wherethedemonstratedmotionmaydiffersubstantiallyfromthetrajectoryproposedbythe
policy. Despitetheirdifferentinteractionmechanisms, thetwomodesaretreatedidentically
downstream. The action actually issued by the operator is recorded in 𝑎˜[0,𝑛) and used as the
BCtarget. Chunksareflaggedasintervenedatthechunklevel, andthisflagdeterminesthe
BCtargetfortheexecutionregion:
𝑎target
istheactionchunkactuallyissuedforanintervened
[𝑛,2𝑛)
chunk and the base-policy reference otherwise, while the committed region always uses the
referenceactionasitstarget. Theinputto𝑄 isindependentoftheinterventionflag: becausethe
committedregionrecordstheactionactuallyissued,itcontainsthehumanactionswhenever
theprecedingchunkwasintervened. Thus,thestateaugmentationintroducedin§3.3continues
tofaithfullyrepresenttheactionactuallyinflight.
Thebase-policyinterface. Theskeleton’sinterfaceispreserved: thetrainablenetworksaccess
the base policy through a compressed token of its internal representation, while the actor
is conditioned on the reference action chunk generated by the base policy. Let 𝜋 denote
base
the frozen base policy and 𝐸 the encoder that reads its internal representation during chunk
inferenceandcompressesitintotheRLtoken𝑧 𝑡 =𝐸(𝜋 base ). ThebasepolicyrunsunderaTT-RTC
scheduler[2]tomaintainthetimingguaranteesof§3.1. Eachbase-policyforwardpasstherefore
produces both the reference action chunk 𝑎¯𝑡:𝑡+2𝑛 = 𝜋 base (𝑠 𝑡 ) and the RL token 𝑧 𝑡 on which the
trainable networks are conditioned. The committed region provided to 𝑄 remains 𝑎˜[0,𝑛) as
definedin§3.3,whichcoincideswiththereferencechunkonlyintheabsenceofintervention.
Fortheconcreteinstantiation,thestateargumentofthegeneric𝜋and𝑄 isrepresentedbythe
pair (𝑧 𝑡,𝑠 𝑡 ). Consequently, each transition must store this pair for the bootstrap state so that
theactortargetat𝑠 𝑡+2𝑛 canbeevaluated,togetherwiththecommittedregionofthatnextstate,
whichbecomesavailableonlyonedecisionsteplaterduringrollout. Algorithm1summarizes
thecompletetrainingloopdescribedinthefollowingtwoparagraphs: anasynchronousrollout
processthatgeneratestransitionsandanoff-policyoptimizationprocessthatconsumesthem,
withbothoperatingconcurrentlyoverasharedreplaybuffer.
The critic. The critic is an MLP with LayerNorm [57] applied to every hidden layer. It
takes [𝑧 𝑡,𝑠 𝑡,𝑎˜[0,𝑛),𝑎 [𝑛,2𝑛) ] asinputandpredictsascalarvalue. Thetargetconstructionfollows
TD3[58]: thetargetactor’sactionchunkisperturbedwithclippedGaussiannoise,followed
byapessimisticestimateovertheresultingtargetvalues. Threeaspects,however,departfrom
theoriginalskeleton. First,theactionchunkisexplicitlypartitionedintothecommittedand
executionregions,withbothprovidedtothecriticasinputs. Second,thebackupfollowsthe
chunk-skipping formulation rather than a single-decision backup. Third, the fixed pair of
𝑄 networks is expanded into a REDQ-style [56] ensemble of 𝑁 independent critics, with the
minimumtakenoverarandomlysampledsubsetoftargetcriticsratherthanoverthefullpair.
The actor. The actor is an MLP of the same architecture. It takes [𝑧 𝑡,𝑠 𝑡,𝑎¯𝑡:𝑡+2𝑛 ] as input and
outputsanactionchunk𝑎 𝑡:𝑡+2𝑛 oflength2𝑛,asillustratedinFigure3. Intheresidualmodeused
inthiswork,thenetworkpredictsaboundedcorrectiontothereferenceaction,whichisadded
tothereferencechunktoproducethefinalactionchunk. Theactorlossconsistsofthreeterms,
definedbelowfortheactoroutput𝑎 =𝜋 𝜃 (𝑧,𝑠,𝑎¯). ThefirsttwolossesfollowtheRLTskeleton: a
𝑄-maximizationtermregularizedbyaBCanchorinthespiritofTD3+BC[59],wheretheanchor
13

isdefinedagainstthereferenceactionratherthanadatasetaction. Specifically,thesecorrespond
tothe 𝑄 termintroducedin§3.3andaper-frameMSElossagainstatargetaction 𝑎target. The
thirdtermisspecifictoourframework: asmoothnessregularizerthatinstantiatestheexecutable
setE introducedin§3.3. WecharacterizeE byper-frameboundsonvelocity,acceleration,and
jerk, and relax the corresponding membership constraint into a penalty with overall weight
𝑤 smooth andrelativeweight𝑤 𝑘 foreachderivativeorder:
3
L actor =−𝑄(cid:0)𝑧, 𝑠, sg[𝑎˜[0,𝑛) ], 𝑎 [𝑛,2𝑛) (cid:1) + 𝑤 bc · (cid:13) (cid:13)𝑎−𝑎target (cid:13) (cid:13) 2 [0,2𝑛) + 𝑤 smooth ∑︁ 𝑤 𝑘 · (cid:13) (cid:13)Δ𝑘𝑎 (cid:13) (cid:13) 2 [0,2𝑛) , (5)
𝑘=1
wheresg[·] denotesthestop-gradientoperator: thefullactionchunkisprovidedto 𝑄,while
gradientswithrespectto𝜃propagateonlythroughtheexecutionregion.
Thereplaybuffer. Thereplaybufferisinitializedbyrollingoutthebasepolicyaloneunderthe
deploymentloopof§3.1,withtheattachednetworkinactive;subsequenttransitionscollected
bytheasynchronousrolloutareappendedtothesamebuffer. Thisinitializationensuresthat
every transition is collected under the timing assumptions of the objective, rather than from
teleoperated demonstrations, and provides the critic with an initial fit to the behavior from
whichpolicyimprovementbegins. Thereward𝑟 introducedin§3.2issparse: itisassignedonly
attheendofeachepisode,withsuccessdeterminedbyanoperatorobservingtherollout.
The update schedule. Updates are paced by rollout progress rather than wall-clock time.
Process2ofAlgorithm1performs𝐺criticiterationsforeverytrajectoryappendedbytherollout,
yielding an update-to-data ratio that keeps the update rate bounded by rollout throughput,
regardlessofthechoiceof𝐺. Theactorandtargetnetworksareupdatedlessfrequently: one
actorupdateandonesofttarget-networkupdateareperformedevery 𝐷criticiterations.
4. Experiments
ThissectionevaluatestheSmoothRLframeworkonreal-robotmanipulationtasks. Weconsider
three tasks spanning two complementary regimes - high-speed dynamic manipulation and
high-precisionbimanualmanipulation-toassesstheframeworkunderthecompetingdemands
ofreal-timeresponsivenessandexecutionreliability. Weuse𝜋 [41],fine-tunedforeachtask,
0.5
asthefrozenbasepolicy. Foreachtask,wecompareitssuccessratebeforeandafteronlineRL
fine-tuningwithintheSmoothRLframework.
4.1. Platform
All three tasks are performed on Astribot S1, a mobile bimanual robot with 25 degrees of
freedom,comprisingtwo7-DoFarmswithparallelgrippers,a4-DoFtorso,a2-DoFhead,anda
3-DoFwheeledbase. Forthebasepolicy,theobservationconsistsofthreecamerastreams(head,
left wrist, and right wrist), each processed at 224×224 resolution, together with the robot’s
proprioceptivejointstate. Thebasepolicyissuesa31-dimensionalactionat30Hz,comprising
9-dimensionalCartesiandeltaposesfortheleftarm,rightarm,andtorsoend-effector,along
14

Algorithm1SmoothRLtrainingintheasynchronousinferenceloop
Require: frozen𝜋 withRL-tokenencoder 𝐸,budget𝑛,discount𝛾,soft-updaterate𝜏,step
base
|             | size𝜂,update-to-dataratio𝐺,actordelay |       |     |      |     |     | 𝐷   |     |     |     |     |     |
| ----------- | ------------------------------------- | ----- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initialize: |                                       | 𝜋     | {𝑄  | } 𝑁  |     |     |     |     |     |     |     |     |
|             |                                       | 𝜃 and |     | 𝜙𝑖 𝑖 |     |     |     |     |     |     |     |     |
=1
|     | targets𝜃−←𝜃and𝜙 |     |     | −←𝜙 |     |     |     |     |     |     |     |     |
| --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |                 |     |     | 𝑖   | 𝑖   |     |     |     |     |     |     |     |
replaybufferD
𝑎˜[0,𝑛) ←theholdaction ⊲therobotisstationaryuntilthefirstchunkarrives
|     |           |                     |     |     | Processes1and2runconcurrently,sharingD |     |     |     |     |     | andtheparameters. |     |
| --- | --------- | ------------------- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- | ----------------- | --- |
| 1:  | Process1: | asynchronousrollout |     |     |                                        |     |     |     |     |     |                   |     |
|     | for𝑡      | =0,𝑛,2𝑛,...         |     | do  |                                        |     |     |     |     |     |                   |     |
2:
3: observe𝑠
𝑡
|     | 𝑎¯𝑡:𝑡+2𝑛 |          | 𝜋        | (𝑠 𝑡,𝑎˜[0,𝑛)   | 𝑧 𝐸(𝜋  |      |     |     |                      |     |     |         |
| --- | -------- | -------- | -------- | -------------- | ------ | ---- | --- | --- | -------------------- | --- | --- | ------- |
| 4:  |          | ←        |          |                | ); 𝑡 ← |      | )   |     |                      |     |     |         |
|     |          |          | base     |                |        | base |     |     |                      |     |     |         |
|     | 𝑎        | ←        | 𝜋 (𝑧     | 𝑡,𝑠 𝑡,𝑎¯𝑡:𝑡+2𝑛 | )      |      |     |     |                      |     |     |         |
| 5:  | 𝑡:𝑡+2𝑛   |          | 𝜃        |                |        |      |     |     |                      |     |     |         |
|     | 𝑎        | ←        | 𝑎˜[0,𝑛)  |                |        |      |     |     | ⊲committedregionover |     |     | [𝑡,𝑡+𝑛) |
| 6:  | [0,𝑛)    |          |          |                |        |      |     |     |                      |     |     |         |
|     | 𝑎t       | a r g et |          |                |        |      |     |     |                      |     |     |         |
| 7:  |          | ←        | 𝑎¯[0,2𝑛) |                |        |      |     |     |                      |     |     |         |
[ 0 , 2𝑛 )
ifteleoperationthen
8:
| 9:  |     | 𝑎           | ← 𝑎h | u m a n   |     |     |     |     |     | ⊲absoluteorresidual,§3.4 |     |     |
| --- | --- | ----------- | ---- | --------- | --- | --- | --- | --- | --- | ------------------------ | --- | --- |
|     |     | [𝑛,2𝑛)      |      | [𝑛 , 2𝑛 ) |     |     |     |     |     |                          |     |     |
|     |     | 𝑎t a r g et | ← 𝑎  |           |     |     |     |     |     |                          |     |     |
| 10: |     |             |      | [𝑛,2𝑛)    |     |     |     |     |     |                          |     |     |
[ 𝑛 , 2𝑛 )
issue𝑎
| 11: |     | [𝑛,2𝑛) |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
recordatransition𝜏 =(𝑠 𝑧 𝑎˜[0,𝑛), 𝑎 𝑎t a r g et ) ⊲finishedat𝑡+2𝑛
| 12: |     |     |     |     | 𝑡 𝑡, 𝑡, |     | [𝑛,2𝑛), |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | ------- | --- | --- | --- | --- | --- |
[ 0 ,2 𝑛 )
|     | if𝑡 | ≥ 2𝑛then |     |     |     |     |     |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
13:
𝜏 ← 𝜏 ∪(𝑟 𝑡−2𝑛, 𝑠 𝑡, 𝑧 𝑡, 𝑎¯𝑡:𝑡+2𝑛, 𝑎 ) ⊲rewardover [𝑡−2𝑛,𝑡);nextstate
| 14: |           | 𝑡−2𝑛              | 𝑡−2𝑛   |     |     |     | [0,𝑛) |                                   |     |     |     |     |
| --- | --------- | ----------------- | ------ | --- | --- | --- | ----- | --------------------------------- | --- | --- | --- | --- |
| 15: |           | append𝜏           | 𝑡−2𝑛   | toD |     |     |       |                                   |     |     |     |     |
|     | 𝑎˜[0,𝑛)   | ←                 | 𝑎      |     |     |     |       | ⊲updatecommittedregionfornextstep |     |     |     |     |
| 16: |           |                   | [𝑛,2𝑛) |     |     |     |       |                                   |     |     |     |     |
|     | Process2: | off-policyupdates |        |     |     |     |       |                                   |     |     |     |     |
17:
18: foreachtrajectoryappendedbyProcess1do
for𝐺
| 19: |     | iterationsdo |         |             |                    |          |        |           |          |        |                   |     |
| --- | --- | ------------ | ------- | ----------- | ------------------ | -------- | ------ | --------- | -------- | ------ | ----------------- | --- |
|     |     |              |         |             | 𝐵 ⊂ D              |          |        |           |          |        |                   |     |
| 20: |     | sampleabatch |         |             |                    |          |        |           |          |        |                   |     |
|     |     | foreach𝜏=(𝑠, |         | 𝑧,          | 𝑎˜[0,𝑛), 𝑎 [𝑛,2𝑛), | 𝑎target, | 𝑟,     | 𝑠′, 𝑧′,   | 𝑎¯′, 𝑎˜′ | ) ∈ 𝐵: |                   |     |
| 21: |     |              |         |             |                    |          |        |           | [0,𝑛)    |        |                   |     |
| 22: |     | drawM        |         | ⊂ {1,...,𝑁} | atrandom           |          |        |           |          |        |                   |     |
|     |     | 𝑎′           | 𝜋       | (𝑧′, 𝑠′,    | 𝑎¯′)+𝜖             |          |        |           |          |        | ⊲𝜖clippedGaussian |     |
| 23: |     |              | ← 𝜃−    |             |                    |          |        |           |          |        |                   |     |
|     |     | 𝑦            | ← 𝑟+𝛾2𝑛 |             | 𝑄 (cid:0)𝑧′,       | 𝑠′,      | 𝑎˜′ 𝑎′ | (cid:1)   |          |        |                   |     |
| 24: |     |              |         | min𝑖∈M      | 𝜙 −                |          | ,      |           |          |        |                   |     |
|     |     |              |         |             | 𝑖                  |          | [0,𝑛)  | [𝑛,2𝑛)    |          |        |                   |     |
|     |     |              |         | (cid:205)   | (cid:0)𝑄           |          |        | 𝑦(cid:1)2 |          |        |                   |     |
| 25: |     | 𝜙 ←          | 𝜙 −𝜂∇   |             | (𝑧, 𝑠,             | 𝑎˜[0,𝑛), | 𝑎      | )−        | forall𝑖  |        |                   |     |
|     |     | 𝑖            | 𝑖       | 𝜙𝑖          | 𝐵 𝜙𝑖               |          | [𝑛,2𝑛) |           |          |        |                   |     |
𝐷-thiterationthen
| 26: |     | ifevery |        |            |       |     |     |     |     |     |     |         |
| --- | --- | ------- | ------ | ---------- | ----- | --- | --- | --- | --- | --- | --- | ------- |
|     |     | 𝜃       | ← 𝜃−𝜂∇ | L          |       |     |     |     |     |     |     | ⊲Eq.(5) |
| 27: |     |         |        | 𝜃          | actor |     |     |     |     |     |     |         |
|     |     | 𝜃−      | ←      | 𝜏𝜃+(1−𝜏)𝜃− |       |     |     |     |     |     |     |         |
28:
|     |     |     | −   |              | −       |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------------ | ------- | --- | --- | --- | --- | --- | --- | --- |
| 29: |     | 𝜙   | ←   | 𝜏𝜙 𝑖 +(1−𝜏)𝜙 | forall𝑖 |     |     |     |     |     |     |     |
|     |     |     | 𝑖   |              | 𝑖       |     |     |     |     |     |     |     |
with2grippercommandsand2head-jointcommands. Theattachedactorandcriticmodify
onlythe20arm-actiondimensions,leavingthetorsoandheadactionsunchanged. Thecontrol
frequencydeterminestheframerateatwhichthelatencybudget𝑛in§3.1ismeasured. Inference
isrequestedat5Hz,soanewactionchunkarrivesevery200ms,correspondingtoalatency
| budgetof𝑛 |     | =6frames. |     |     |     |     |     |     |     |     |     |     |
| --------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Eachchunkthereforecontributes6framestoitsexecutionregionwhile
the subsequent chunk is being inferred. The base policy is trained to predict 𝐻 = 32 frames
15

Dynamic Tossing:
Grasp an object and toss it into a target container.
Pen Capping:
Align the pen with its cap, secure the cap onto the pen, and release the cap.
Box Opening:
Stabilize the box with the left hand while the right hand precisely aligns with the seam, cuts the tape, and opens the flaps.
Figure 5 | Thethreereal-robot tasksevaluatedinthiswork: dynamic objecttossingintoatargetbin,
bimanualpencapping,andhigh-precisionboxopeningbyslittingthesealingtapeandopeningtheflaps.
per chunk; thus, the committed and execution regions occupy 12 frames in total, while the
remaining20framesformthediscardedregionandaresupersededbythesubsequentchunk
beforeexecution.
4.2. TaskSpecification
Dynamictossing. Therobotisinstructedtograsparandomlyplacedobjectandtossitinto
a randomly placed bin. Successful tossing requires the end effector to accumulate sufficient
velocity throughout the swing prior to release, rather than attaining the target velocity at a
singleinstant. Thismakesthetaskparticularlysensitivetoasynchronousexecution: apauseat
achunkboundarycanbringthearmnearlytorest,leavinginsufficienttimefortheremaining
swingtorecovertherequiredreleasevelocity. Consequently,successfulexecutionrequiresboth
precise release timing and continuous motion across chunk boundaries. The bin opening is
approximately7×12cm,whiletheobjectisapproximately6×7cm,makingthetaskchallenging
inboththrowingspeedandspatialaccuracy.
16

Pencapping. Therobotisinstructedtoalignthepenwithitscap,securethecapontothepen,
andreleasethecap. Successfulinsertionrequirestherelativeposebetweenthepenandcapto
fallwithinaclearancetoleranceofapproximately5mm. Errorsbeyondthistolerancecannot
bereliablycorrectedbyapplyingadditionalforce,asthecaptendstodeflectratherthanseat
properly. Sincebotharmsareactivelycontrolled,theinsertionaccuracydependsontheirrelative
poseratherthanthemotionofeitherarmalone. Thismakesthetaskparticularlychallengingfor
thepretrainedbasepolicy: althoughittypicallyreachesthevicinityofthedesiredconfiguration,
smallresidualposeerrorscanpreventsuccessfulinsertion. Theattachednetworkistherefore
responsibleforcorrectingtheseresidualerrorsandachievingtherequiredinsertionprecision.
Boxopening. Thetaskrequirestherobottostabilizeapackageboxwithitslefthandwhile
therightarminsertsabladeintotheseambetweentheflapsanddrawsitalongtheseamto
cutthetape,afterwhichtheflapsareopened. Thebladeisapproximately1mmwide,while
theseamisonly2–3mmwide,requiringtheinsertiontolocatetheseamwithapproximately
millimeter-levelprecision. Aninsertionerrorcanfailineitherdirection: theblademaycutinto
thecardboardanddamagethebox,oritmaymissthetapeandleavetheboxsealed. Oncethe
bladeisinserted, theseamguidesitsmotion, substantiallyreducingthepositionaldemands
duringthesubsequentcuttingphase;thebladeonlyneedstomaintainsufficientdepthtosever
the tape. Thus, the primary challenge lies in precise insertion, where the pretrained policy
reachesthevicinityofthedesiredconfigurationbutremainsinsufficientlyreliable.
4.3. TrainingSetup
Hyperparameters. Theattachedactorandcriticareimplementedas3-layerMLPswith512
hiddenunitsperlayer. Weuseanupdate-to-dataratioof𝐺 =5andanactorupdatedelayof
𝐷 =5,suchthatfivegradientupdatesareperformedforeachnewlycollectedtrajectory,while
the actor and target networks are updated every fifth gradient step. The training batch size
issetto256. Wesetthecorrectionbound to0.05, reflectingthatthepretrained basepolicyis
alreadyclosetosuccessfulbehaviorandthereforerequiresonlysmallcorrectiveadjustments.
Allremaininghyperparametersfollowstandardoff-policyactor-criticpracticeandarekeptfixed
acrossalltasks.
Rewardlabelingandhumanintervention. Thesparserewarddefinedin§3.4isprovidedby
anoperatorthroughagamepadorVRinterface. Anepisodeisterminatedandassignedabinary
reward only when the operator judges the task to be complete; no intermediate rewards are
providedatanyearliertimestep. Followingeachepisode,therobotisreturnedtoitsinitialpose
andthesceneisresetforthenexttrial. Evaluationisbasedsolelyontasksuccessrate. During
training,theoperatorintervenesasneededtomaintainabalancedratioofsuccessfulandfailed
episodes. Human-intervenedactionsareincorporatedthroughtherawactionspace,suchthat
theyarestoredandtrainedoninthesamemanneraspolicy-generatedactions.
The two intervention modes introduced in §3.4 exhibit markedly different performance on
thedynamictossingtask,motivatingtheuseofresidualintervention. Thisdifferenceismost
pronouncedforbinpositionsfarthestfromtherobot,whichrequirehigherreleasevelocitiesand
arethereforemorechallenging. Fortheseconfigurations,directchunk-levelteleoperationvia
VRachievesasuccessrateofapproximately30%,comparedwithapproximately80%whenthe
operatorprovidesaresidualcorrectiontothebasepolicy’sactionchunk. Directteleoperation
17

Dynamic Tossing Pen Capping Box Opening
Figure6|Initial-stateconfigurationsusedforevaluation. Ghostedoverlaysindicatethesampledconfigu-
rations. Theinsetillustratesthevariationinthein-handgrasppose,whichismanuallysetduringreset
andisnotincludedintheenumeratedconfigurationcombinations.
requirestheoperatortocontrolboththedirectionandmagnitudeofthereleasevelocitywhile
simultaneouslymaintainingcontinuitywhentransitioningbetweenhumanandpolicycontrol.
Residual intervention instead preserves the base policy’s velocity profile and requires the
operatoronlytocompensateforitsdeviations. Thissubstantiallyreducesthecontrolburden
whilebetterpreservingmotioncontinuityacrossinterventionboundaries.
4.4. Evaluation
Protocol. Each task is evaluated across a predefined set of initial-state configurations. Box
opening uses 10 box positions, dynamic tossing uses 18 configurations comprising 3 object
positions×6target-binpositions,andpencappinguses12configurationscomprising4initial
handstates×3pen-cappositions. Figure6visualizestheconfigurationsforeachtask,which
are identical to those used during online fine-tuning. Each configuration is evaluated once,
yielding 10, 18, and 12 episodes per checkpoint for box opening, dynamic tossing, and pen
capping,respectively. Anepisodeterminateswhentheoperatorjudgeseitherthatthetaskhas
beensuccessfullycompletedorthatitcannolongerbecompleted. Anepisodeiscountedas
successfulonlyintheformercase,andthesuccessrateiscomputedasthenumberofsuccessful
episodesdividedbythetotalnumberofevaluationepisodes.
Comparison. EachtaskisevaluatedatfourpointsthroughouttheonlineRLprocess. Thefirst
isthefrozenbasepolicy𝜋 [41],pretrainedonthetaskanddeployedwithitsparametersfixed,
0.5
without the attached network in the control loop. This baseline represents the performance
attainablethroughsupervisedpretrainingaloneandservesasthezeropointonthehorizontal
axisofthelearningcurvesshowninFigure7. Supervisedpretraininguses1,500teleoperated
demonstrations for box opening and pen capping, and 500 for dynamic tossing. The latter
requires fewer demonstrations because it is substantially more difficult to collect: across all
binpositions,teleoperationsucceedsononlyapproximately50%ofattempts,ashumanoper-
ators face the same challenge of maintaining a continuous swing. Online RL starts from the
corresponding pretrained policy. We first collect 50 rollout episodes under the frozen base
policy alone to seed the replay buffer. The attached actor and critic are then introduced into
the loop, and subsequent rollout episodes are collected under the online RL procedure. The
remainingthreeevaluationpointsarecheckpointsfromthissamerun,takenafter150,200,and
250rolloutepisodes. Allfourcheckpointsareevaluatedonthesamehardwareusingthesame
asynchronous inference loop and latency budget. Thus, the only variable across evaluation
18

100
80
60
40
20
0
0 150 200 250
rollout episodes collected
)%(
etar
sseccus
94
83 90
83
72
75
67
39 40
30
20
Dynamic tossing
8 Pen capping
Box opening
Figure 7 | Success rate versus online interaction episodes, with one curve per task. The zero marker
denotesthefrozenbasepolicy,withitssuccessrateextendedasadashedlineforreference. Eachpoint
reportssuccessover𝑁 evaluationepisodesatthecorrespondingcheckpointasspecifiedin§4. Thethree
nonzerocheckpointscomefromasingleRLrunpertask;linesareconnectedforvisualizationonly.
pointsistheamountofonlinefine-tuningappliedtotheattachednetwork.
4.5. Results
Figure 7 and Table 1 report the success rates of all three tasks as a function of the number of
rollout episodes collected during online RL. After 250 episodes, all three tasks substantially
outperformthefrozenbasepolicy: dynamictossingimprovesfrom39%to94%,pencapping
from8%to83%,andboxopeningfrom30%to90%. Thefollowingparagraphsexaminewhat
thefrozenbasepolicyfailstocaptureoneachtask,howmuchofthisgapisrecoveredthrough
onlinefine-tuning,andthefailuremodesthatremain.
Failuremodesofthebasepolicy. Acrossallthreetasks,failuresofthefrozenbasepolicyare
systematicratherthanrandom,primarilyarisingfrominsufficientadaptationtovariationsin
objectortargetposes. Inpencapping,thepolicyproducessimilarmotiontrajectoriesacross
differentcappositionsandfailstoadequatelyadjusttothevaryingcapposes,resultinginonly
an8%successrate. Inboxopening,thebladeexhibitsaconsistentleftwardbias,causingitto
pierce the cardboard rather than enter the tape seam. In dynamic tossing, the policy fails to
appropriatelymodulatethereleasevelocitywithtargetdistance: ittendstoovershootnearby
bins and undershoot distant ones, while also exhibiting systematic left-right deviations for
targetsonoppositesides.
WhatonlineRLremedies. Theattachednetworkprogressivelycorrectsthesystematicoffsets
ofthefrozenbasepolicy,withthefinalcheckpointsubstantiallyimprovingperformanceacross
allthreetasks,althoughthelearningdynamicsvarybytask. Dynamictossingandpencapping
improve monotonically across checkpoints, with the largest gains occurring within the first
19

|     | Task | NumberofRolloutEpisodes |              | SuccessRate |
| --- | ---- | ----------------------- | ------------ | ----------- |
|     |      | 0                       | (basepolicy) | 39%         |
|     |      |                         | 150          | 72%         |
DynamicTossing
|     |     |     | 200          | 83% |
| --- | --- | --- | ------------ | --- |
|     |     |     | 250          | 94% |
|     |     | 0   | (basepolicy) | 8%  |
|     |     |     | 150          | 67% |
PenCapping
|     |     |     | 200          | 75% |
| --- | --- | --- | ------------ | --- |
|     |     |     | 250          | 83% |
|     |     | 0   | (basepolicy) | 30% |
|     |     |     | 150          | 20% |
BoxOpening
|     |     |     | 200 | 40% |
| --- | --- | --- | --- | --- |
|     |     |     | 250 | 90% |
Table1|Successrateateachcheckpoint,withthecumulativenumberofrolloutepisodescollectedbefore
evaluation. Eachsuccessrateiscomputedfromoneepisodeperinitial-stateconfigurationunderthe
evaluationprotocolspecifiedin§4.4.
150episodes. Forpencappinginparticular,thesuccessrateincreasesfrom8%to67%during
thisinitialphase,indicatingthatthedominantsystematicoffsetislargelycorrectedearly,after
whichperformanceisprimarilylimitedbyresidualvariationaroundthecorrectedtrajectory.
Boxopeningexhibitsadifferentlearningtrajectory: performanceinitiallydropsto20%after150
episodes,fallingbelowthefrozenbasepolicy,beforerecoveringto40%andultimatelyreaching
90%. Thistransientdegradationlikelyreflectstheexplorationrequiredfortheattachednetwork
todiscovereffectivecorrectionswhileadaptingtothetask.
Closingthelastmillimeter. Figure8showsrepresentativefailuresoneachtask,atthefinal
checkpoint (250 episodes) and under the frozen base policy for comparison. Comparing the
tworowsofFigure8showsthefailuresmovingclosertosuccess: thebasepolicymissesina
consistentdirectionandbyavisiblemargin,whereaswhatremainsafterRLisasmallspread
aroundthecorrectpose. Ondynamictossing,theobjectlandsclosertothebinandbreaksthe
basepolicy’spatternoffixedbias;onboxopening,theblade’sdeviationfromtheseamismuch
smaller,withleft-rightdeviationsof1–2mmaroundthecorrectposition;onpencapping,the
axial misalignment between cap and barrel is likewise much smaller, a small spread around
thecorrectpose. Thesedeviationmagnitudesarepreciselywhatmakesthesetaskschallenging:
successisnotaboutreachingthetargetregionbutclosingthelastfewmillimeters,andanerror
smallenoughtobebarelydistinguishableintheimageissufficienttofailtheepisode.
| 5. Conclusion, | Limitations | and Future | Work |     |
| -------------- | ----------- | ---------- | ---- | --- |
ThisworkpresentsSmoothRL,aframeworkforfine-tuningpretrainedrobotpolicieswithonline
RL under asynchronous inference, improving success on fine-grained real-robot tasks while
preservingreal-timeresponsiveness. Asynchronybreaksthecorrespondencebetweentheaction
optimizedbythevaluegradientandtheactionactuallyexecutedbytheenvironment. Ourchunk
rolepartitioningandgradienttruncationexplicitlyrestorethiscorrespondencebyrestricting
policyupdatestotheexecutedregion. Operatingintherawactionspacefurtherenablesdirect
20

Dynamic Tossing Pen Capping Box Opening
RL
VLA
Figure8|Representativefailuresondynamictossing,pencapping,andboxopening. Columnsdenote
tasks;topandbottomrowsshowfailuresoftheRLpolicyandfrozenbasepolicy,respectively. RL-tuned
failuresarenearmisses,whilethebasepolicyexhibitslarger,systematicdeviations.
stateaugmentationforconcurrentexecutionandallowshumaninterventiontobeincorporated
naturallyastrainingdata.
Limitations
The proposed online RL framework with asynchronous inference is general, yet the current
instantiationhastwoknownlimitations:
1. Inferencelatencyconstraint. Theproposedframeworkoperatesunderafixedinference
frequency,requiringeachchunk-levelinferencetocompletewithinapredefinedlatency
budget. Whentemporalfluctuationsininferencelatencycausetheactualcomputation
timetoexceedthisbudget,scheduledchunkhandovercannotbeguaranteed. Theresultant
timingmisalignmentdestabilizestheasynchronousexecutionloop.
2. Outputexpressivenessboundedbythebasepolicy. TheexpressivecapacityoftheRL
moduleisconstrainedbythebasepolicyintwokeyaspects. First,theconditionalfeatures
usedforRLoptimizationarederivedfromtheinternalrepresentationsoftheVLAmodel,
sotheperceptualcapabilityoftheRLbranchisupper-boundedbytheinformationrichness
of VLA embeddings. Second, in the current implementation, the RL module produces
onlyboundedresidualcorrectionsuponthereferenceactionsprovidedbythebasepolicy.
Thecorrectionmagnitudeisconfinedwithinafixedlocalneighborhood, whoseradius
balances the effective correction range and the strength of trust-region regularization.
Whenthebasepolicyexhibitssystematicbiasesontarget-domaindata,suchlocalresidual
correctionslacksufficientexpressivenesstorectifyerroneouspolicybehaviors.
21

FutureWork
Threebroaderdirectionsemergefromthisstudy. First,theproposedframeworkmayextend
beyond the particular policy parameterization considered here. Since §3.3 constrains only
where the value gradient is applied, the same principle could accommodate a wider class
of offline-to-online learning algorithms and substantially different policy architectures. In
particular, the value gradient need not be restricted to a small attached network; it could
propagatethroughtheparametersofanentiregenerativepolicy,asinQAM[55],whoseadjoint
terminalcondition∇ 𝑎 𝑄 overthegeneratedchunkprovidesanaturalmechanismforexpressing
thetruncationinducedbyasynchronousexecution. Suchformulations,however,wouldneed
totreatthecommittedprefixexplicitly: preservingpreviouslyissuedactionsbecomesaprefix-
constrainedgenerationproblemratherthananoutput-spaceoverwrite. Thisperspectivepoints
towardamoregeneralformulationofonlinepolicyoptimizationunderpartiallycommitted
generation. Second,theinteractionbetweenpolicylearningandactionblendingwarrants
furtherinvestigation. Whiletheframeworkrulesoutanexternalmixingoperator,itdoesnot
precludeincorporatingthemixturedirectlyintothelearningobjective. Doingsowouldallowthe
critictoevaluatetheactionsthatareultimatelyexecuted,potentiallyprovidingamorefaithful
trainingsignalunderasynchronousdeployment. Thiscomesatthecostofabroadertemporal
dependencyintheobjective,additionalcontinuityconstraintsaroundtheblendingoperator,and
anadditionalactorforwardpassforeachcontributingchunk. Morefundamentally,theblending
weight typically decays toward the junction between chunks, precisely where continuity is
most critical, suggesting a potentially unfavorable trade-off between execution smoothness
andthestrengthofthelearningsignal. Understandingthistrade-offcouldleadtoprincipled
formulationsthatjointlyoptimizepolicyimprovementandtemporalconsistency. Third,scaling
theevaluationtosubstantiallybroaderandmorediversetaskdistributionsisessentialfor
characterizingthefundamentalexpressivenesslimitsoftheproposedadaptationmechanism.
Inparticular,systematicallyincreasingthedistributionalshiftfromthepretrainedbasepolicy
could reveal when local correction around the reference action ceases to be sufficient, and
whetherthislimitationisbestaddressedthroughamoreexpressiveadapter,afullygenerative
policy update, or a mechanism that can progressively relax the reference constraint. Such
experimentswouldhelpdistinguishlimitationsarisingfromthelearningalgorithmitselffrom
thoseimposedbythechosenpolicyparameterization.
6. Contributions
• Contributors: GuangGao∗,YuxuanNong∗,BaifuHuang
• ProjectLead: JiananWang
∗Equalcontribution.
22

References
[1] KevinBlacketal.Real-TimeExecutionofActionChunkingFlowPolicies.arXiv:2506.07339,
2025.
[2] KevinBlacketal.Training-TimeActionConditioningforEfficientReal-TimeChunking.
arXiv:2512.05964,2025.
[3] Yufeng Liu et al. Learning Native Continuation for Action Chunking Flow Policies.
arXiv:2602.12978,2026.
[4] Dongyang Liu et al. Action-Prior Denoising for Smooth Real-Time Chunking.
arXiv:2605.25537,2026.
[5] Cheng Chi et al. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion.
arXiv:2303.04137,2023.
[6] TonyZ.Zhaoetal.LearningFine-GrainedBimanualManipulationwithLow-CostHard-
ware.arXiv:2304.13705,2023.
[7] PerryDongetal.EXPO-FT:Sample-EfficientReinforcementLearningFinetuningforVision-
Language-ActionModels.arXiv:2605.25477,2026.
[8] ChenyuYangetal.SERNF:Sample-EfficientReal-WorldDexterousPolicyFine-Tuningvia
Action-ChunkedCriticsandNormalizingFlows.arXiv:2602.09580,2026.
[9] CharlesXuetal.RLToken: BootstrappingOnlineRLwithVision-Language-ActionModels.
arXiv:2604.23073,2026.
[10] DongchiHuangetal.CO-RFT:EfficientFine-TuningofVision-Language-ActionModels
throughChunkedOfflineReinforcementLearning.arXiv:2508.02219,2025.
[11] WenliXiaoetal.Self-ImprovingVision-Language-ActionModelswithDataGenerationvia
ResidualRL.arXiv:2511.00091,2025.
[12] Lars Ankile et al. Residual Off-Policy RL for Finetuning Behavior Cloning Policies.
arXiv:2509.19301,2025.
[13] Guozheng Ma et al. What Makes Value Learning Efficient in Residual Reinforcement
Learning? arXiv:2602.10539,2026.
[14] QiyangLietal.DecoupledQ-Chunking.arXiv:2512.10926,2025.
[15] GuanxingLuetal.VLA-RL:TowardsMasterfulandGeneralRoboticManipulationwith
ScalableReinforcementLearning.arXiv:2505.18719,2025.
[16] Haozhan Li et al. SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning.
arXiv:2509.09674,2025.
[17] YanjiangGuoetal.ImprovingVision-Language-ActionModelwithOnlineReinforcement
Learning.arXiv:2501.16664,2025.
[18] Si-ChengWangetal.VLAModelPost-TrainingviaAction-ChunkedPPOandSelfBehavior
Cloning.arXiv:2509.25718,2025.
23

[19] Kang Chen et al. 𝜋 RL: Online RL Fine-tuning for Flow-based Vision-Language-Action
Models.arXiv:2510.25889,2025.
[20] SitingWangetal.𝜋-StepNFT:WiderSpaceNeedsFinerStepsinOnlineRLforFlow-based
VLAs.arXiv:2603.02083,2026.
[21] AllenZ.Renetal.DiffusionPolicyPolicyOptimization.arXiv:2409.00588,2024.
[22] TongheZhangetal.ReinFlow: Fine-tuningFlowMatchingPolicywithOnlineReinforce-
mentLearning.arXiv:2505.22094,2025.
[23] SeohongParketal.FlowQ-Learning.arXiv:2502.02538,2025.
[24] KunLeietal.RL-100: PerformantRoboticManipulationwithReal-WorldReinforcement
Learning.arXiv:2510.14830,2025.
[25] YuhuiChenetal.ConRFT:AReinforcedFine-tuningMethodforVLAModelsviaConsis-
tencyPolicy.arXiv:2502.05450,2025.
[26] YiWangetal.LearningWhileDeploying: Fleet-ScaleReinforcementLearningforGeneralist
RobotPolicies.arXiv:2605.00416,2026.
[27] Perry Dong et al. EXPO: Stable Reinforcement Learning with Expressive Policies.
arXiv:2507.07986,2025.
[28] Jianlan Luo et al. Precise and Dexterous Robotic Manipulation via Human-in-the-Loop
ReinforcementLearning.arXiv:2410.21845,2024.
[29] ChechengYuetal.𝜒 : Resource-AwareRobustManipulationviaTamingDistributional
0
Inconsistencies.arXiv:2602.09021,2026.
[30] PhysicalIntelligence.𝜋∗ : aVLAThatLearnsFromExperience.arXiv:2511.14759,2025.
0.6
[31] ByteDanceSeed.GR-RL:GoingDexterousandPreciseforLong-HorizonRoboticManipu-
lation.arXiv:2512.01801,2025.
[32] AndrewWagenmakeretal.SteeringYourDiffusionPolicywithLatentSpaceReinforcement
Learning.arXiv:2506.15799,2025.
[33] QiyangLietal.ReinforcementLearningwithActionChunking.arXiv:2507.07969,2025.
[34] Ge Li et al. TOP-ERL: Transformer-based Off-Policy Episodic Reinforcement Learning.
arXiv:2410.09536,2024.
[35] TedXiaoetal.ThinkingWhileMoving: DeepReinforcementLearningwithConcurrent
Control.arXiv:2004.06089,2020.
[36] AyoubAgouzoul.UnderstandingAsynchronousInferenceMethodsforVision-Language-
ActionModels.arXiv:2605.08168,2026.
[37] JiamingTangetal.VLASH:Real-TimeVLAsviaFuture-State-AwareAsynchronousInfer-
ence.arXiv:2512.01031,2025.
[38] AstribotTeam.AsynchronousFast-SlowVision-Language-ActionPoliciesforWhole-Body
RoboticManipulation.arXiv:2512.20188,2025.
24

[39] KoheiSendaietal.LeaveNoObservationBehind: Real-timeCorrectionforVLAAction
Chunks.arXiv:2509.23224,2025.
[40] PhysicalIntelligence.𝜋 : AVision-Language-ActionFlowModelforGeneralRobotControl.
0
arXiv:2410.24164,2024.
[41] PhysicalIntelligence.𝜋 : aVision-Language-ActionModelwithOpen-WorldGeneraliza-
0.5
tion.arXiv:2504.16054,2025.
[42] SongmingLiuetal.RDT-1B:aDiffusionFoundationModelforBimanualManipulation.
arXiv:2410.07864,2024.
[43] YueSuetal.WorldGuidance: WorldModelinginConditionSpaceforActionGeneration.
arXiv:2602.22010,2026.
[44] LinLietal.CausalWorldModelingforRobotControl.arXiv:2601.21998,2026.
[45] BeingBeyondTeam.Being-H0.7: ALatentWorld-ActionModelfromEgocentricVideos.
arXiv:2605.00078,2026.
[46] AstribotTeam.TowardsPredictive,Aligned,andScalableRobotLearning.arXiv:2607.11270,
2026.
[47] NVIDIA. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots.
arXiv:2503.14734,2025.
[48] TianyuanYuanetal.Fast-WAM:DoWorldActionModelsNeedTest-timeFutureImagina-
tion? arXiv:2603.16666,2026.
[49] MooJinKimetal.CosmosPolicy: Fine-TuningVideoModelsforVisuomotorControland
Planning.arXiv:2601.16163,2026.
[50] Xue Bin Peng et al. Advantage-Weighted Regression: Simple and Scalable Off-Policy
ReinforcementLearning.arXiv:1910.00177,2019.
[51] Kevin Frans et al. Diffusion Guidance Is a Controllable Policy Improvement Operator.
arXiv:2505.23458,2025.
[52] Chenxiao Gao et al. FlowRL: A Taxonomy and Modular Framework for Reinforcement
LearningwithDiffusionPolicies.arXiv:2603.27450,2026.
[53] Mitsuhiko Nakamoto et al. Steering Your Generalists: Improving Robotic Foundation
ModelsviaValueGuidance.arXiv:2410.13816,2024.
[54] JackyKwoketal.RoboMonkey: ScalingTest-TimeSamplingandVerificationforVision-
Language-ActionModels.arXiv:2506.17811,2025.
[55] QiyangLi,SergeyLevine.Q-learningwithAdjointMatching.arXiv:2601.14234,2026.
[56] XinyueChenetal.RandomizedEnsembledDoubleQ-Learning: LearningFastWithouta
Model.arXiv:2101.05982,2021.
[57] JimmyLeiBaetal.LayerNormalization.arXiv:1607.06450,2016.
[58] ScottFujimotoetal.AddressingFunctionApproximationErrorinActor-CriticMethods.
arXiv:1802.09477,2018.
25

[59] Scott Fujimoto, Shixiang Shane Gu. A Minimalist Approach to Offline Reinforcement
Learning.arXiv:2106.06860,2021.
[60] TuomasHaarnojaetal.SoftActor-Critic: Off-PolicyMaximumEntropyDeepReinforcement
LearningwithaStochasticActor.arXiv:1801.01290,2018.
26