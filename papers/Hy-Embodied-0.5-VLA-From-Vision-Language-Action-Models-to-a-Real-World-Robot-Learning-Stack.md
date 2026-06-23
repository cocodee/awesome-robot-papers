Hy-Embodied-0.5-VLA: From Vision-Language-Action
Models to a Real-World Robot Learning Stack
TencentRoboticsX×TencentHyTeam
ThepastyearhaswitnessedarapidproliferationofVision-Language-Action(VLA)models,
withgrowingattentionnowturningtothenextgenerationofembodiedfoundationmodels.
However,atrulygeneralistrobotisunlikelytoemergefromanysinglemodelinisolation.
Rather,itmustbebuiltonafullrobotlearningstackthatremainsrobustfromdatacollection
toreal-worlddeployment.
Inthisreport,wepresentHy-Embodied-0.5-VLA,abbreviatedasHyVLA-0.5,anend-to-end
systemthatspansthefullrobotlearningstack:datacollection,modeldesign,continued
pre-trainingandsupervisedfine-tuning,RLpost-training,andreal-worlddeployment.Each
componentservesadistinctroleinthisstack.Fordata,wedevelopacustomfingertipUMI
devicewithamotion-capturecagetocollectover10,000hoursofegocentric,sub-millimeter-
precisionhumandemonstrationsthatcanalsodirectlyserveaspost-trainingtrajectories.
Formodeling,weextendtheHy-Embodied-0.5backbonewithaflow-matchingaction
expert,acompactmemoryencoder,andadelta-chunkactionrepresentationthatdecouples
policylearningfromembodiment-specifickinematics.Forcontinuedpre-trainingand
fine-tuning,startingfromthecheckpointcontinued-pre-trainedontheUMIcorpus,we
introducetworeal-robotSFTtracks:Track-Afortarget-robotadaptationandTrack-Bfor
UMI-onlycross-embodimenttransfer.ForRLpost-training,weintroduceaProximalized
PreferenceOptimization(PRO)-basedofflineRLalgorithmthatturnsfailurecasesinto
rapidpolicyimprovementanddrivesperformancetowardnear-ceilingsuccessrateswithout
requiringalearnedrewardmodel.Fordeployment,anasynchronousinferencepipeline
withlightweighttrajectorysmoothingenableshigh-frequencyclosed-loopcontrol.Taken
asawhole,theHy-Embodied-0.5-VLAstackmarksameaningfulsteptowarddeployable
generalistrobots.
Website:tairos.tencent.com/openSourceModels/hy-embodied-0.5-vla
Github:github.com/Tencent-Hunyuan/Hy-Embodied-0.5-VLA
Model:huggingface.co/tencent/Hy-Embodied-0.5-VLA-UMI
Dataset:huggingface.co/datasets/tencent/Hy-Embodied-0.5-VLA-Data
1 Introduction
Recent advances in Vision-Language-Action (VLA) architectures have demonstrated promising
capabilitiesincontinuousroboticcontrol[1–6].Yetturningthesemodeladvancesintodeployable
generalistrobotsrequiresmorethanstrongerpolicies:thedata,training,adaptation,andexecution
layersmustbeco-designedaroundreal-hardwareconstraints.
Thesesystem-levelrequirementsexposethreecoupledchallengesonthedataside.First,traditional
teleoperation [7, 8] relies on master–slave interfaces that force operators to unnaturally adapt to
therobot’sworkspace,lacksdirecthapticfeedback,andthereforeprecludesdelicatemanipulation.
Second,whileleveraginghumandata[9,10]orhand-heldframeworkssuchasUMI[11]alleviates
datascarcity,thesealternativesintroducenewlimitations:rawhumandemonstrationsgreatlyenrich
behavioraldiversitybutprovideoverlycoarseactionlabels,andexistingUMIrigsimprovelocalization
throughSLAMatthecostofcumbersomehandhelddevicesthatfailtocapturefingertip-levelforce
transmission.Third,bridgingthecross-embodimentgapinvolvesmorethanadaptingkinematics:it
requiresaddressingtheembodimentgapbetweenhumanandrobotmotionspaces,thecontrolgap
inducedbydifferentdynamicsandactuation,andtheperceptiongapbetweenhumanegocentricviews
androbot-mountedcameraobservations.
Beyonddata,thearchitecturaldesign,trainingparadigms,anddeploymentstackofVLAmodels
presentequallycriticalbottlenecks.Earlyapproacheslargelyreliedonautoregressivemodelingover
1
6202
nuJ
21
]OR.sc[
1v90441.6062:viXra

| ❰ Customized UMI Data ❱  |     |     |     |     | ❰ RL Fine-Tuning ❱  |     |
| ------------------------ | --- | --- | --- | --- | ------------------- | --- |
Hy-Embodied-0.5-VLA
human-in-the-loop preference optimization
|     |     | Language  Vision + History  |                 |          |                                              | SFT Policy  |
| --- | --- | --------------------------- | --------------- | -------- | -------------------------------------------- | ----------- |
|     |     |                             | Proprioception  | Noise ε  |                                              |             |
|     |     | “Insert the RAM”            | Rel-EE Pose     |          | Human-in-the-loop rollout & data collection  |             |
& Gripper
Head camera · Ego-centric view
| Left wrist  | Right wrist  |     |     |     |     |     |
| ----------- | ------------ | --- | --- | --- | --- | --- |
Joint-Attention
|     | TRAIN  |                        |     |                | RL  |     |
| --- | ------ | ---------------------- | --- | -------------- | --- | --- |
|     |        | HY-Embodied-0.5 · VLM  |     | Action Expert  |     |     |
Key features
Ego-centric capture
| head-mounted, first-person view    |                         | NTP Loss              | Flow-matching  |               |                |              |
| ---------------------------------- | ----------------------- | --------------------- | -------------- | ------------- | -------------- | ------------ |
| F i n g e r - a tt a c h e d       |   g r i p p e rs        | VQA, 2D/3D Grounding  |  Loss          | Action Chunk  |                |              |
| tri g g e r- fr e e,  h u m a n -d | r iv e n   ac tu a tion |                       |                |               | push− / pull+  |              |
| Sub-millimeter precision           |                         |                       |                |               | πl  πw         | Improved π*  |
high-fidelity demonstration tracking
|     |     |     | EXECUTE  |     | Preference optimization · proximal regularizer   |     |
| --- | --- | --- | -------- | --- | ------------------------------------------------ | --- |
❰ Cross-Embodiment Deployment ❱
one policy, multiple bodies — real and simulated
|                  |          | Real Robots  |              |             | Robotwin 2.0 Simulation  |     |
| ---------------- | -------- | ------------ | ------------ | ----------- | ------------------------ | --- |
| Dobot X-Trainer  | JAKA K1  | AGIBOT G2    | Astribot S1  | Unitree G1  |                          |     |
Fig.1:OverviewofHy-Embodied-0.5-VLA.Anend-to-endVLAsystemthatpairstheHy-Embodied-
0.5-MoTbackbonewithaflow-matchingactionexpertunderadelta-chunkactionrepresentation,
pre-trained on a 10K-hour egocentric UMI corpus and refined with a reward-free, Proximalized
PreferenceOptimization(PRO)-basedofflineRLstage(FlowPRO).Asinglepre-trainedcheckpoint
specializesalongtwoparallelpost-trainingtracksforcross-embodimenttransfertomorphologically
unseenrobots.
discretizedactiontokens[12,13],whichinherentlylimitsbothexecutionspeedandcontrolprecision.
RecentframeworksmitigatethisbycouplingaVision-LanguageModelwithaflow-matchingaction
expertthatpredictscontinuousactions[1],yettheirfoundationalvisualbackbonesarenotexplicitly
engineeredforroboticcontrol:asignificantgapremainsbetweengeneralistvisualrepresentationsand
thedensespatiotemporalreasoningrequiredforphysicalinteraction.Ontopofrepresentationalissues,
standardimitationlearningstrugglestoreachlast-miledexterity,whileexistingreinforcementlearning
recipes for continuous control typically depend on brittle reward models or value networks [14].
Finally,evenawell-trainedpolicyisoflimiteduseunlessitcanbeservedathighfrequencyina
closedvisuallooponrealhardware—adeploymentconstraintthatisrarelytreatedasafirst-class
designtarget.Addressingthesecombinedbottlenecksthereforerequiresaunifiedpipelinethatjointly
tacklesdata,model,policyrefinement,anddeployment.
Toaddressthesechallenges,wepresentHy-Embodied-0.5-VLA(Fig.1),anend-to-endsystemthat
spansthefullstack—fromcustomdata-collectionhardwaretoproduction-readydeployment.Rather
thantreatingVLAmodelingasanisolatedproblem,HyVLA-0.5isorganizedasacompletepipeline
inwhichdata,modeling,RLpost-training,anddeploymenteachserveadistinctrole.
Fordata,webuildacustomfingertipUMIdevicepairedwithamotion-capturecage,anduseitto
collectover10Khoursofegocentric,sub-millimeter-precisionhumandemonstrations.Thefingertip
formfactorrestoresnaturalhapticperceptionthatbulkyhandheldrigscannotoffer;themotion-capture
cageproduceshigh-fidelityactionlabelsbeyondthereachofSLAM-onlypipelines;andtheegocentric
viewpointsuppliesglobalsemanticcontextratherthanover-relyingonlocalwristcameras.Crucially,
thesametrajectoriescanalsodirectlyserveaspost-trainingdata,makingthemreusablefordownstream
adaptationandreducingtheneedforseparatetarget-robotdatacollection(Sec.3.1).
Formodeling,weextendourHy-Embodied-0.5[15]backbone—a4BMixture-of-TransformersVLM
pre-trainedonembodiedcorpora—withaflow-matchingactionexpertforcontinuous,high-frequency
actionprediction.Comparedwithadaptinggeneral-purposeVLMs[16–18],thisembodied-native
initializationyieldsstrongerspatialpriorsandfasterpost-trainingconvergence.Wefurtherintroduce
acompactmemoryencoderforspatiotemporalcontext,andadoptadelta-chunkactionrepresentation
thatpredictsincrementalend-effectormotionbetweenconsecutivesteps.Thedelta-chunkformulation
decouples policy learning from embodiment-specific kinematics and substantially shrinks the
optimization search space, providing a clean substrate for cross-embodiment post-training and
deployment (Secs.2and5.1).
2

Forcontinuedpre-trainingandfine-tuning,wefirstpre-trainHyVLA-0.5onthe10K-hourUMI
corpus,thenspecializetheresultingcheckpointthroughtask-specificsupervisedfine-tuning.Real-
robotSFTisorganizedintotwotracks:Track-Astudiesintra-embodimentadaptationwithtarget-robot
demonstrations and deployment on the same platform, while Track-B studies UMI-only cross-
embodimenttransfertomorphologicallydifferentrobotswithouttarget-robotteleoperation(Sec.3.3).
ForRLpost-training,weintroduceFlowPRO[19],acritic-free,reward-freeProximalizedPrefer-
enceOptimization(PRO)-basedofflinereinforcementlearningalgorithm.Throughateleoperated
intervention-and-rollbackpipeline,pairedsuccess/failuretrajectoriesareharvesteddirectlyfrompolicy
rollouts.AnRPROlossthenalignsthesepreferenceswiththecontinuousflow-matchingobjective,
whileacontrastivegradient-cancellationpropertysuppressescatastrophicforgetting.FlowPROturns
failurecasesintoarapiditerationloopforimprovinglong-tailmanipulationrobustnessanddriving
performancetowardnear-ceilingsuccessrates,withouttraininganyrewardorvaluenetwork(Sec.4).
For deployment, we implement an asynchronous inference framework that overlaps backbone
forwardpasseswithactionexecution,andstitchessuccessivedeltachunksviaasimpleyeteffective
cubic Bézier action smoother that guarantees C1-continuous transitions (Sec. 5). Together, these
components enable high-frequency, closed-loop control on real hardware and complete the path
from data collection to real-world operation on the factory floor. The rest of this report details
how the full HyVLA-0.5 pipeline is built, trained, and validated across large-volume pre-training,
cross-embodimentpost-training,PRO-basedrefinement,andphysicalrobotdeployment.
2 ModelArchitecture
HyVLA-0.5 follows the vision-language-action (VLA) paradigm, in which a pre-trained vision-
languagemodel(VLM)suppliesbroadsemanticperceptionandadedicatedactionmoduletranslates
the resulting multi-modal context into low-level robot control (Fig. 2). On top of this paradigm,
HyVLA-0.5comprisesthreecomponents.Firstly,thebackboneistheembodiedVLMHy-Embodied-
0.5[15],whichadoptsaMixture-of-Transformers(MoT)architecture[20]withmodality-adaptive
computationandnative-resolutionimageencoding.Secondly,anactionexpertgeneratescontinuous
actionchunksthroughconditionalflowmatching[1,21],withtherobotics-specificstateandaction
streamskeptseparatefromtheVLMandcoupledtoitthroughsharedattention.Finally,theimage
encoderisextendedintoacompactmemoryencoderthataggregatesamulti-frameobservationhistory
throughinterleavedtemporal-spatialattention[22].WefirstformalizetheprobleminSec.2.1,and
thendetailthebackbone(Sec.2.2),theactionexpert(Sec.2.3),andthecompactmemoryencoder
(Sec.2.4).
Layer N Multi-view RGBs “Grasping and inserting State Noisy Action Img1 Img2 Img3 Text State Action
a memory module onto
QKV a motherboard”
Temporal-Attn HY-ViT TextTokenizer MLP
Spatial-Attn
VisionMoT LanguageMoT ActionMoT
Every4layer QKV QKV QKV
Joint-Attention
FFN FFN FFN
Fig.2:Architecturaloverviewof HyVLA-0.5.TheframeworkadoptsaMoTarchitecturetofacilitate
cross-modalinteractionsviaasharedjoint-attentionmechanism.ToeffectivelyprocessK-framemulti-
viewRGBsequences,theimageencoderisextendedintoacompactmemoryencoder.Specifically,
temporal attention blocks are interleaved every four layers to enforce causal masking across the
temporaldimensionandseamlesslyincorporatehistoricalvisualcontext.Asdepictedontheright,
theattentionmaskdemonstratesourblock-wisecausalattentionstrategy.FollowingHy-Embodied-
0.5[15],weapplylocalbidirectionalattentiontomodelthemulti-viewobservations.
3

2.1 ProblemFormulation
Weformulatemanipulationasagoal-conditioned,chunk-levelcontrolproblem.Ateverydecision
stept,thepolicyconsumesamulti-modalobservationo andpredictsachunkoffutureactionsA ;
t t
thatis,wemodeltheconditionaldistributionp(A |o ).Formally,
t t
o = (cid:0) I , ℓ, s (cid:1) , I = (cid:8) Iv (cid:9)k=0:K−1 , A = (cid:0) a , a , ..., a (cid:1) , (1)
t t t t t−k v=1:n t t t+1 t+H−1
where I is the visual stream, ℓ the language instruction, s the proprioceptive state, and A the
t t t
predictedactionchunkofhorizonH.Wedescribeeachcomponentbelow.
VisualInput.ThevisualstreamI isamulti-view,multi-frameRGBobservation:atsteptitcomprises
t
theK mostrecentframesfromeachofthencameraviewpoints(e.g.ahead-mountedviewtogether
withawrist-mountedviewperarm),i.e.n×K imagesintotal.ThehistorylengthK isaconfigurable
hyperparameter; its value at each training stage is specified in Sec. 3, with K=1 recovering the
single-framecase.
Language Input. A natural-language task instruction ℓ (e.g. “hang the mug on the rack”)
definesthegoal.ItistokenizedandjointlyencodedwiththevisualstreambytheVLMbackbone,
enablingthepolicytogrounditsbehaviorsinthecommandedsemantics.
ProprioceptiveInput.Therobotstates encodesthecurrentposeofthecontrolledend-effector(s)
t
andisprojectedintothebackboneembeddingspace,providingtheembodiment-groundedcontext
thatanchorsactionpredictiontotherobot’spresentconfiguration.
Action Output. Instead of single-step execution, the policy predicts an entire action chunk [7]
ofhorizonH perinferencecycle.Thisensurestemporallysmooth,high-frequencycontrolwhile
significantlyreducingtheinferencelatency,astheVLMbackboneisevaluatedonlyoncetocondition
theentireH-stepgenerationviaflowmatching.
End-effector-frameRepresentation.Boththeproprioceptivestates
t
andtheactiona
t′
areformulated
intheend-effectorframe(EEF),anembodiment-agnosticrepresentationthatdecouplesthepolicy
from robot-specific joint kinematics. For each controlled arm, a pose is parameterized by a 3-D
Cartesiantranslation(xyz)anda6-Dcontinuousrotationrepresentation[23],augmentedbya1-D
normalizedgrippercommand,i.e.,s ,a ∈R10perarm.Theproprioceptivestates isdefinedinthe
t t′ t
end-effectorframewithrespecttotheembodimentroot,whileeachfutureactiona isadelta-chunk
t′
definedintherelativeEEFthattakesthecurrentstates asitsreferenceframe.
t
OptionalCo-TrainingTasks.Beyondlearningfromaction-labeledtrajectories,theunifiedVLA
architecture integrates auxiliary next-token prediction tasks to preserve its foundational vision-
language reasoning and spatial grounding capabilities. We denote this auxiliary data mixture as
D = D ∪D ∪D . Each training instance is formulated as a pair (c,y ), where c
ct VQA 2D 3D 1:M
representsthevision-languageconditions,andy denotesasequenceofM serializedtargettokens.
1:M
Depending on the specific task, y consists of semantic answer tokens for VQA, normalized
1:M
2Dspatialcoordinates,or3Dgeometricparametersformulatedwithinthecameraorsceneframe.
Crucially,thisco-trainingobjectivedirectlyoptimizestheparametersofthesharedVLMbackbone,
ensuringitmaintainsandenrichesthevitalsemanticandspatialrepresentations.
2.2 Hy-Embodied:Modality-AdaptiveComputingBackbone
HyVLA-0.5buildsupontheembodiedVLMHy-Embodied-0.5-MoT[15],acompactmodelwith4B
parametersoptimizedforedgedeployment.Itinstantiatesthestandardimage-encoder-plus-language-
modelrecipe,andwedetailthreekeydesignchoicesadaptedformanipulation.
Native-resolution visual encoding. The backbone encodes images with Hy-ViT 2.0, a native-
resolutionVisionTransformer(ViT)[24,25]thatacceptsarbitraryinputresolutionsandisdistilled
fromalargerinternalteacher.Eachcamerastreamcanthereforebeprocessedatitsnativeresolution
ratherthanbeingdown-sampledtoafixedsize.
4

Modality-adaptiveComputationviaMoT.ThebackboneadoptsaMixtureofTransformers(MoT)
architecture[20],whichisdirectlyinitializedwiththepre-trainedweightsofHY-Embodied-0.5[15].
This design maintains non-shared QKV and FFN parameters for the visual and textual streams.
Specifically,duringtheforwardpass,allvisualtokensextractedbytheViTarecomputedusinga
duplicated,vision-specificparameterset,whereastextualtokensareprocessedusingtheoriginal
languageparameters.Cross-modalinteractionisstrictlylimitedtothesharedself-attentionlayers.
Consequently,thevisualandtextualparametersareupdatedindependently.Furthermore,following
theoriginalconfigurationofHY-Embodied-0.5[15],thebackboneappliesbidirectionalattention
strictlyamongthevisualtokensofeachindividualimage,whilemaintainingstandardcausalattention
forthelanguagetokens.
Co-trainingObjective.FortheauxiliaryVQAandspatialgroundinginstancessampledfromD ,the
ct
VLMbackboneemploysitsnativelanguagemodelingheadtoautoregressivelydecodetheserialized
targettokens.Weoptimizethisprocessviaastandardnext-tokenpredictionobjective:
|     |     |     |     |    |     |    |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
M
|     |         | =E  |           | X       | (cid:0) | (cid:1) |     |
| --- | ------- | --- | --------- | ------- | ------- | ------- | --- |
|     | Lntp(θ) |     |           | − logp | y |c,y  | ,      | (2) |
|     |         |     | (c,y)∼Dct |         | θ j     | <j      |     |
j=1
wherey denotesthej-thserializedtargettoken.
j
2.3 ActionExpertwithDual-TowerFlowMatching
Rather than discretizing actions into language-like tokens, HyVLA-0.5 equips the backbone with
anaction expert that modelsthecontinuous distributionp(A | o ) directly viaconditional flow
t t
matching[21].
Dual-towerRouting.OntopoftheMoTbackbone,HyVLA-0.5separatesthejointtransformerinto
anunderstanding-orientedVLMtowerandageneration-orientedaction-experttower.TheVLMtower
processesvisualandtextualcontextwiththemodality-adaptiveparametersdescribedabove,while
the action expert consumes the projected robot state and noisy action tokens [s ,Aτ] to produce
|     |     |     |     |     |     | t t |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
thecontinuousactionvelocityfield.Thetwotowersinteractthroughsharedself-attention,allowing
groundedvisual-languagecontexttoguideactiongeneration.
Block-wiseCausalAttention.Wepartitionthetokensequenceintothreeblocks,[I ,ℓ],[s ],and
t t
|     | ], and apply | attention |     | that is bidirectional | within | each block but strictly | causal |
| --- | ------------ | --------- | --- | --------------------- | ------ | ----------------------- | ------ |
[aτ ,...,aτ
t,0 t,H−1
across blocks. The perception block is prevented from attending to the robotics-specific blocks,
minimizingdistributionshiftfromVLMpre-training;thestateblockisisolatedsothatitskeysand
valuescanbecached;andthenoisy-actionblockattendstothefullprefix.
Flow-matchingObjective.LetAτ = τA +(1−τ)ϵwithϵ ∼ N(0,I)denotethenoisyaction
|     |     |     | t   | t   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
chunkatflowtimestepτ ∈ [0,1].Theactionexpertregressesthevelocityfieldv thattransports
θ
noisetothetargetactions,trainedwith
|     |        | E               |     | (cid:13) (Aτ     |               | (cid:13) 2     | (3) |
| --- | ------ | --------------- | --- | ---------------- | ------------- | -------------- | --- |
|     | Lfm(θ) | = p(At|ot),q(Aτ |     | |At) (cid:13)v θ | t ,o t )−(ϵ−A | t ) (cid:13) , |     |
|     |        |                 |     | t                |               | 2              |     |
where is the ground-truth chunk, its noised version, the predicted velocity
| A   |     |     | Aτ  |     | A   | (Aτ,o ) |     |
| --- | --- | --- | --- | --- | --- | ------- | --- |
| t   |     |     |     | t   | θ   | t t     |     |
conditionedontheobservationo ,andϵ−A thetargetdenoisingdirection.Theflowtimestepτ is
|     |     | t   |     | t   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
sampledfromaBetadistributionskewedtowardhigh-noiseregimes,whichemphasizestheharder,
moreinformativestagesofactiondenoising.Whenauxiliarydataismixedwithrobotdemonstrations,
thetotalobjectiveisL(θ) =Lfm(θ)+λntpLntp(θ),withλntp=0recoveringaction-onlytraining.
Inference.Atdeployment,thepolicygeneratesanactionchunkbyintegratingthelearnedvelocity
fieldfromτ=0toτ=1viatheforwardEulerupdateAτ+δ =Aτ +δv (Aτ,o )over10integration
|     |     |     |     | t   | t   | θ t t |     |
| --- | --- | --- | --- | --- | --- | ----- | --- |
steps (δ=0.1). Because the conditioning observation prefix remains constant across all solver
o t
iterations,itskeysandvaluesarecachedduringtheinitialforwardpass.Consequently,subsequent
stepsexclusivelyrecomputetheactiontokens,significantlyreducingcomputationaloverhead.
5

2.4 CompactMemoryEncoderwithTemporal-SpatialAttention
HyVLA-0.5conditionsontheK-framemulti-viewhistoryI ofEq.(1)toformacompactmemory
t
encoding.Encodingalln×K framesindependentlyandforwardingthemtothebackbonewould
multiplythevisualtokencountpassedtotheVLM.Weinsteadextendtheimageencoderintoavideo
encoderthatcompressesthetemporaldimensionbeforetokensreachtheVLMbackbone.
FactorizedTemporal-spatialAttention.FollowingPi-MEM[22],thevideoencoderpreservesthe
patchify-then-attendstructureofastandardViTandinsertsatemporalpassonceeveryLlayers.At
suchalayer,weaddafixedsinusoidaltemporalencodinge(k)(withe(0) =0)andreusethesame
QKVandoutputprojectionW oftheunderlyingViTblock,thenfactorizetheattentionintotwo
O
passesthatsharetheseprojections:
(temporal) V˜ =CausalAttn (cid:0) Q ,K ,V (cid:1) , overtheK framesateachpatchp; (4)
p p p p
(spatial) X˜ =W Attn (cid:0) Q ,K ,V˜ (cid:1) , overthenpatcheswithineachframek, (5)
k O k k k
where X˜ is the attention output that the block feeds into its residual connection and MLP. The
k
temporalpassisacausalattention,soeachframeattendsonlytothepresentandpast,matchingthe
streamingnatureofon-robotperception.Thespatialpassistheoriginalbidirectionalself-attention
withinaframe,appliedtothetime-mixedvaluesV˜.ThisfactorizationavoidstheO(n2K2)costof
jointspace-timeattentionandreducestheper-layercosttoO(Kn2+nK2).
Token-count-preservingcompression.Intheupperlayersofthevideoencoderwediscardthepatch
representationsofpastframesandforwardonlythecurrent-frametokenstothebackbone.Because
theinterleavedtemporalattentionhasalreadybaked thehistoricalcontextintothecurrent-frame
representation,thenumberofvisualtokenspassedtotheVLMmatchesthatofasingle-framepolicy.
Parameter-free,Transfer-friendlyDesign.Thevideoencoderintroducesnonewlearnableparam-
etersrelativetothesingle-imageHy-ViT2.0:bothpassesreusetheQKVandW projectionsof
O
Eq.(4)–(5),andthetemporalencodinge(k)isafixedsinusoidwithe(0) =0ratherthanalearned
table.Consequently,whenK=1thecausaltemporalattentionistheidentityande(0) = 0leaves
theinputunchanged,soeachaugmentedblockreducesexactlytothepre-trainedViTblock.The
memory-augmentedbackboneisthereforeinitializeddirectlyfromtheHy-Embodied-0.5weightsand
recoversthesingle-frameencoderasaspecialcase.
3 Pre-trainingandSupervisedFine-tuning
ThissectionfocusesonthesupervisedstagesofHyVLA-0.5training:large-scalepre-trainingonthe
Hy-UMI-10Kcorpustolearnageneralistactionprior,followedbysupervisedfine-tuning(SFT)on
task-specificdemonstrationsfromeachtargetembodiment.
3.1 Hy-UMI-10K:High-FidelityManipulationDataset
HyVLA-0.5 is pre-trained on Hy-UMI-10K, a hand-held Universal Manipulation Interface (UMI)
dataset[11]ofmorethan10Khourscollectedin-house(Fig.4),anditisthesoledatasourcefor
pre-training.UnlikestandardUMIpipelinesthatrecovergripperposesfromon-boardvisualSLAM,
ourcapturerigtrackseachgripperwithanexternalopticalmotion-capturesystem,whichlabelsevery
6-DoFtrajectoryatsub-millimetreprecisioninasingle,globallyconsistentworldframe—hence
high-fidelity.Wedescribeitscapturedevice,composition,andthepre-trainingrecipebelow.
Capture device. Demonstrations are acquired with custom-designed hand-held UMI grippers
detachedfromkinematicsofspecificembodiments(Fig.3).Thegripperdesignfollowsthatofa
commonlyadoptedindustrialgripper,ChangingtekCTAG2F90,tohelpreducedeploymentgap.The
gripper-mountedcameraislocatedclosetothegrippersurface,minimizingcollisionsoftheprotruding
camerawhenoperatingintightspace.Gripperopennessismeasuredbytherotaryencodersatgripper
jointsproducingsub-millimetreaccuracy,withoutrelyingonvisualidentificationofgripperopenness.
Gripperposesaretrackedbyanexternalopticalmotion-capturesystemwhichresolveseach6-DoF
trajectoryatsub-millimetreprecisioninasingleglobalCartesianframeandalsosynchronisesthe
6

T Top
L
R
Left Right
(a)UMIworkstationandgrippers (b)Cameraviews
Fig.3:UMIcustomdatacollectionworkstation.Thein-housedesignedhardwaresetupfeatures
an external optical motion-capture system delivering sub-millimeter high-precision tracking, an
ego-centric visual perspective camera with native depth capture, a 6-dimensional force-sensing
gripperoneachhand.
headRGB-DcameratoavoidinterferenceofIRemissions.Thisopticaltrackingreplacestheon-board
visualSLAMusedbyconventionalUMIrigs,obtainingsuperioraccuracyinposetrajectorieswith
minimaloperationalrisksofposejittersandtracklossesduetotemporarylackofvisualfeaturesin
SLAM-basedposeestimationsystems.Thissetupwithopticaltrackingsystemsprioritizeshighquality
actionlabelsfortasksinvolvingfinemotorskills,atthecostofinconvenientin-the-wilddeployment.
Thegrippersaredesignedwithergonomicfinger-attachedmechanismsthatallowdirectactuationwith
contactandforcefeedbackontohumanfingersratherthanrelyingonindirecttrigger-basedactuation
withlessobviousforcefeedback.Somegrippersareoptionallyinstrumentedwith6-dimensionalforce
torquesensorslocatedatthetips,andtheirfingersareattachedtotheoperator’sownfingersrather
thanoperatedthroughmechanicaltriggers,givingaproprioception-alignedmappingbetweenhuman
intentandrecordedaction,andthetip-locatedsensorsallowmoredirectmeasurementsofforceintent
comparedwrist-locatedsensors.Becausetherecordingisanchoredtothegripperratherthantoany
fixedbase,thecorpusisfreeofbase-placementvariance.TherigscaptureRGB-Dstreams,thoughin
thecurrentversionofHyVLA-0.5,onlytheRGBmodalityisconsumedintraining,whiledepthdata
remainavailableforfuturetrainingstages.
Composition and distribution. The corpus spans more than 1M episodes and 10K hours of
demonstrations across 70 distinct tasks, organised into six scene-based task families—Laundry
Room(28.5%),Kitchen(19.2%),PersonalCare&Miscellaneous(13.8%),Dexterous/Tool-use
(10.4%),Storage&Organization(10.0%),andCleaning(5.7%).Thesesixfamiliesaccountforthe
bulkofthecorpus,whiletheremainingtasksformalongtailspanningdiverseobjectcategories
andenvironmentalconditions.Manipulatedobjectscoverabroadspectrumfromrigidcontainers
andtablewaretoprecisioninstrumentsanddeformablefabrics.Acompletecharacterizationoftask
families,object-categorybreakdown,andper-taskhourdistributionisprovidedinFig.4.
3.2 Pre-training
Setup. We initialize the VLM from the Hy-Embodied-0.5-MoT [15] checkpoint for pre-training.
WhiletheactionexpertsharesthesamearchitecturalconfigurationastheVLM,itisinstantiatedand
randomlyinitializedasanindependentTransformermodule.Furthermore,itshiddenandintermediate
sizesarescaleddownfrom2048to1024andfrom6144to2048,respectively,yieldinganeffective
parameter count of 370M. All model parameters are trainable and are optimized under the flow-
matchingobjective(Eq.3).Toacceleratelarge-scalepre-training,wesetK=1,i.e.,nohistorical
imageframesareusedasinput,sothevideoencoder(Sec.2.4)reducestothestandardsingle-image
encoder.Thepolicyingests3cameraviewsat224×320resolutionandpredictsafutureactionchunk
ofhorizonH=50at10Hz.
7

(a) Task Family Distribution (b) Skill Primitives (c) Object Categories
Share of ~10K hours across 6 scene-based task families Hours-per-skill cluster Hours per physical object class interacted with by the policy
Bimanual Fold & Stack 3,945 h Deformable Textiles 3,050 h
Laundry Room 3,025 h · 28.5% Precision Placement 3,065 h Tableware & Utensils 2,060 h
6 K Pe it r c s h o e n n a l Care & Misc 1 2 , , 4 0 6 4 5 0 h h · · 1 1 3 9 .8 .2 % % Spatial Organization 1,495 h Small Rigid Objects 1,475 h
TA 1 S 0 K K F h A o M u I r L s I ES C S D t l e o e x a r t a n e g i r n e o g u & s O / r T g o a o n l- iz u a s t e io n 1 1 , , 0 1 6 1 6 0 1 5 0 h h h · · · 1 1 5 0 0 . . 7 4 .0 % % % Seque S n u t r i f a a l c R e e W tri i e p v in a g l 4 1 3 , 8 0 4 h 5 h Rigi P d r C ec o i n si t o a n in I e n r s s t r & u R m a e c n k t s s 1, 1 0 ,1 7 2 5 0 h h
Other / Misc 1,315 h · 12.4% Articulated Manipulation 251 h Cleaning Implements 1,051 h
Constrained Insertion 209 h Packaged Goods 674 h
Dexterous Assembly 61 h
(d) Sample Scenes
One scene per top use-case
Bimanual Folding Contianer Filling Accessory Organization Charger Insertion Flower Arranging
Fig.4: UMI dataset distribution. Detailed characterization of our diverse, in-house collected
10K-hourUMIdemonstrationcorpus.Thedistributionoutlinesbroadscale,diverseskillcategories,
environmentalconditions,andmanipulatedobjects,ensuringgeneralist-levelmanipulationcapacity.
DataandPre-trainingrecipe.Weusethefull10K-hourUMIcorpusforpre-training.Thedataloader
samplesthedatasetwithreplacement:itfirstsamplesanepisodefromthefullcorpuswithprobability
proportionaltoepisodelength,thenuniformlysamplesoneframefromthatepisodeasthecurrent
frame,andfinallytakesthefutureactionsequencewithchunksizeH=50at10Hzastheground-truth
actionchunk.Bothstateandactioninputsarenormalizedusingtheirdataset-widemeanandstandard
deviationbeforebeingfedintothenetwork.Wetrainfor200Kstepswithaglobalbatchsizeof1,024
andabaselearningrateof5×10−5.Thelearningrateislinearlywarmeduptoitsmaximumvalue
overthefirst1Ksteps,decayedtoonetenthofthepeakvalueoverthesubsequent160Ksteps,and
kepttrainingforanother40Ksteps.WeuseAdamWoptimizer[26]andperformtraininginbfloat16
mixedprecision.
3.3 SupervisedFine-tuning
Setup.InitializingfromtheUMIpre-trainedVLAcheckpoint(Sec.3.2),werunsupervisedfine-tuning
(SFT)ontask-specificdemonstrationsfromeachtargetembodimentundertheflow-matchingobjective
(Eq. 3). Both the VLM and action expert weights are loaded from the pre-trained model, and all
parameters remain trainable. Unlike pre-training, SFT sets K=6, enabling the video encoder of
Sec.2.4toconditiononthecurrentframetogetherwithfivehistoricalframes.
EmbodimentsandData.Wefine-tuneourmodelacrossonesimulatedembodimentandfourreal-
worldplatforms.Insimulation,weemploytheAloha-AgileXbimanualsetupfromtheRoboTwin2.0
benchmark[27],covering50manipulationtasks;eachtaskprovides50clean-environmentepisodes
and500randomized-environmentepisodes,resultingin2.75Kepisodesandmorethan6Mframes
in total. For real-world SFT, we organize the data into two deployment tracks that separate intra-
embodiment adaptation from cross-embodiment transfer. Track A (intra-embodiment) collects
demonstrationsthroughtele-operationonthesamerobotplatformusedforevaluation;here,theDobot
X-Trainercoversfourtaskswith300demonstrationspertask(18hoursintotal).TrackB(cross-
embodiment)fine-tunesonlyontask-specificUMIdemonstrationsanddeploystomorphologically
differenttargetrobotswithouttarget-robotteleoperation;thistrackcoversonetaskonJAKAK1(300
UMIdemonstrations,1.2hours)andonetaskonAstribotS1(200UMIdemonstrations,1.5hours).
Separately,weuseUnitreeG1(1task,400UMIdemonstrations,2.2hours)fortheforce-modality
validationinSec.6.2.
Post-trainingrecipe.Forreal-worlddeployment,actionsaresampledat50Hzwithanaction-chunk
horizon of H=50 and a history interval of 1 second. We train for 60K steps with a global batch
sizeof32andabaselearningrateof2.5×10−5,decayedover40Ksteps.ForRoboTwin2.0,due
tothelargerdatascale,wedownsamplefutureactionsfromthecurrentframewithstride3,usean
action-chunkhorizonofH=20andahistoryintervalof5×stride.Theglobalbatchsizeissetto128
andtheremainingoptimizationsettingsfollowthepre-trainingrecipe.Moredetailsaredescribedin
AppendixA.
8

Fig.5:FlowPROdatapipelineforcollectingreal-robotpreferencetrajectoriesandconvertingthem
intodenseper-statepreferencetuples.Duringpolicyrollouts,anoperatortriggersanintervention-and-
rollback:thesystemrewindstoapriorstate,logstheexecutedsegmentasanegativetrajectory,and
recordsacorrectiveteleoperationsegmentasthepairedpositivetrajectory.Asmooth-interpolation
procedurethensynthesizesthemissingcounterpartactiononeachbranchtoyieldper-statetuples
(s,aw,al)usedforpreferenceoptimization.
4 ReinforcementLearningPost-Training
Aftersupervisedpre-trainingandSFT(Sec.3.3),HyVLA-0.5furtherimprovesreal-robotdeployment
through failure-driven post-training. This stage follows the FlowPRO recipe [19], using a flow-
matching-awarepreference-optimizationloss(RPRO)togetherwithateleoperatedintervention-and-
rollbackdatapipeline.Inthisway,HyVLA-0.5convertsasmallnumberofreal-robotcorrectionsinto
measurabledeploymentgainswithouttraininganyrewardorvaluemodel.
4.1 DesignPrinciples
Asdiscussedinsection7,real-robotpost-traininggenerallyfallsintothreefamilies:SFT/DAgger,
reward-orvalue-basedRL,andpreference-basedRL.Theircharacteristiclimitationsmotivatethe
threeFlowPROdesignprinciplesbelow:
– (P1) Exploit failures directly. Negative trajectories are not discarded or merely flagged for
re-labelling;theyarefedbackintotheaction-generationlossasper-state,per-chunkcontrastive
signalsagainsttheirpairedpositivecorrections.
– (P2)Avoidrewardandcriticmodelsentirely.Thetrainingsignaliscomputedinclosedform
fromafrozenreferencepolicyandthecurrentpolicy,usingaflow-matchinglog-likelihoodproxy.
Thisbypassesthedense-reward-designbottleneckthatplaguescontact-richmanipulation.
– (P3) Anchor the implicit reward. A symmetric proximal regularizer prevents the absolute
magnitude of the implicit reward from exploding. This structurally forbids the plain-DPO
reward-hackingfailuremodeinwhichthepolicydriftsawayfrombothaw andal.
Theremainderofthissectionformalisestheloss(Sec.4.2)andthedatapipelinethatsuppliesthe
per-statepreferencetuplesitconsumes.
4.2 Method
FlowPRO proceeds as an iterative offline-RL loop on top of an SFT-pretrained HyVLA-0.5 base
policy(Fig.5).Eachroundcontainsthreesteps:(1)collecton-robotpreferencepairsviateleoperated
intervention-and-rollback;(2)convertthesesparsetrajectory-levelcorrectionsintodenseper-state
preferencetuplesviaSmoothInterpolation;(3)optimizethepolicywiththeRPROlossonamixed
batchofnewpairs,historicalpairs,andSFTdata(Fig.6).Thepreviousround’spolicyservesasthe
referencepolicyπref inthenextround.
RPROloss.TheHyVLA-0.5actionheadisaflow-matchingmodel[21,28].Givenastates= (o,l)
with visual observations o and a language instruction l, a velocity field v (a ,t | s) transports
θ t
9

Fig.6:RPROoptimization.Thelearnablepolicyπ andfrozenreferenceπref predictactionsaθ and
θ
ref forthesamestate.Theobjectivepullsaθ towardthepreferredactionaw (rw↑)andpushesit
a
fromthedispreferredal (rl↓).Aproximalregularizer(bluedashed)anchorsbothrewardbranchesto
| ,preventingrewardhacking.BatchesmixD |     |     |     |     | k     | ,D < k ,andDSFT |     | .   |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | ----- | --------------- | --- | --- | --- | --- | --- |
| πref                                 |     |     |     |     | p ref | p re f          |     |     |     |     |     |
Gaussian noise ϵ ∼ N(0,I) to an action chunk a. This transport follows the linear interpolant
a = (1−t)ϵ+taoverflowtimet∈[0,1],withconditionalvelocityu(a |a):=a−ϵ.Following
| t   |     |     |     |     |     |     |     | t   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Flow-DPO[29],weadopttheper-sampleflow-matchingregressionlossasatractablesurrogatefor
thenegativelog-likelihood,
|     |     | (s,a) | =E                |     | (cid:2) | (a ,t|s)−u(a |     | |a)∥2(cid:3) |     |     | (6) |
| --- | --- | ----- | ----------------- | --- | ------- | ------------ | --- | ------------ | --- | --- | --- |
|     | ℓ   | θ     | t∼U[0,1],ϵ∼N(0,I) |     | ∥v      | θ t          |     | t            | ,   |     |     |
whichyieldstheimplicit-rewardproxyusedbyRPRO,
|     |     |     | r   | (s,a) | = β (cid:0) ℓref(s,a)−ℓ | (s,a) | (cid:1) , |     |     |     | (7) |
| --- | --- | --- | --- | ----- | ----------------------- | ----- | --------- | --- | --- | --- | --- |
|     |     |     | θ   |       | 2                       | θ     |           |     |     |     |     |
whereℓref andℓ denotetheflow-matchinglossesunderthereferenceandcurrentpolicies.Substituting
θ
Eq.(7)intothePROpairwiseobjective[30]givestheflow-matching-adaptedPROloss,
h
|         | =−E |             |     |      | (cid:0) (s,aw)−r | (s,al) | (cid:1) |     |     |     |     |
| ------- | --- | ----------- | --- | ---- | ---------------- | ------ | ------- | --- | --- | --- | --- |
| LPRO(θ) |     | (s,aw,al)∼D |     | logσ | r θ              | θ      |         |     |     |     |     |
|         |     |             |     | |    |                  | {z     | }       |     |     |     |     |
Lcon:contrastiveoptimizer
(cid:1)(cid:3)i
|     |     |     |     |     | X 1(cid:2) | (cid:0)        | (cid:1) | (cid:0) |            |     | (8) |
| --- | --- | --- | --- | --- | ---------- | -------------- | ------- | ------- | ---------- | --- | --- |
|     |     |     |     | +   |            | logσ r θ (s,a) | +logσ   |         | −r θ (s,a) | ,   |     |
2
a∈{aw,al}
|     |     |     |     | |   |     |     | {z  |     |     | }   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Lreg:proximalregularizer
where Lreg is minimized at r (s,a) = 0 and grows symmetrically with |r (s,a)|, anchoring the
|     |     |     | θ   |     |     |     |     |     | θ   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
absolutemagnitudeoftheimplicitrewardandtherebypreventingthereward-hackingpathologyof
plainFlow-DPO.Topreservebase-policyperformanceandreinforcedirectregressiontowardaw,we
| combineLPRO | withasupervisedterm: |     |     |     |     |     |     |     |     |     |     |
| ----------- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
LRPRO(θ) =λPROLPRO(θ)+λSFTLSFT(θ), LSFT(θ) =E [ℓ (s,aw)]. (9)
|     |     |     |     |     |     |     |     | (s,aw)∼D |     | θ   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
Ausefulside-propertyofEq.(8)iscontrastivegradientcancellation:whenaw =al,∇ =0,
Lcon
θ
leavingonly∇ Lreg and∇ LSFT active.ThismakesitsafetorouteSFT-styledemonstrationsthrough
θ θ
thesameRPROloss,whichweexploitinbatchcompositionbelow.
|                  |                            |     |     |     | We  | collect preference |     | trajectory | pairs | (τw,τl) | via |
| ---------------- | -------------------------- | --- | --- | --- | --- | ------------------ | --- | ---------- | ----- | ------- | --- |
| Data collection: | intervention-and-rollback. |     |     |     |     |                    |     |            |       |         |     |
a teleoperated intervention-and-rollback pipeline (Fig. 5). During rollouts of the current policy,
theoperatorinterveneswheneveranerroneousordangerousactionisobserved.Thesystemthen
(1)rewindstoanearlierstates withoperator-chosenhorizon∆andrecordstheexecutedsegment
t−∆
asthenegativetrajectoryτl;(2)retrievestheobservationatt−∆asavisualreferenceincasethe
environmenthaschangedandthephysicalsceneneedstobereset;and(3)recordstheoperator’s
correctivedemonstrationfroms asthepositivetrajectoryτw.Asingleoperatoractionthusyields
t−∆
anaturallypaired(τw,τl)sharingthesameinitialstate.Varying∆acrossinterventionsdiversifies
theper-pairstartingstatewithoutrecordingseparatepositiveandnegativerollouts.
10

SmoothInterpolationandbatchmixing.Becauseτw andτl divergeafters
t−∆
,eachsubsequent
statebelongstoonlyonetrajectory.Toproducedenseper-statetuples(s,aw,al)requiredbyEq.(8),
wesynthesizethemissingcounterpartwithaSmoothInterpolationprocedure(Fig.5).ForastateM
onτl,welocateitsclosestpointM′ onτw underaweighteddistancemetric.Wethenconstructa
syntheticpositiveactionchunkthatbridgesfromM toatransitionpointJ onτw viaacubicBézier
forpositions,Slerpfororientations,andlinearinterpolationforthegripper.Thechunkthenfollows
τwuntilitendsatN′,whilethenegativeactionissimplythenextH stepsalongτl.Forstatesalready
onτw orinDSFT ,wesetaw =al.Thecontrastivegradientcancellationabovemakesthesesamples
actasregularizedSFTsamples.Acrossiterations,wekeeptheround-k pairsDk ,thehistorical
pref
poolD
p
<
re
k
f
= S
j<k
D
p
j
ref
,andDSFT inseparatebuffers.Wemixmini-batchesatfixedproportions:
80%/20%fork=1(D
p
k ref/DSFT )and70%/15%/15%fork≥2(D
p
k ref/D
p
<
re
k f/DSFT ).Thisschedule
up-weightsthenewest,mostinformativefailurestates,replayspreviouslycorrectedonestoprevent
regression,andretainsanon-trivialSFTsharetoanchorbasecapabilities.
ExperimentalvalidationofFlowPROonfourreal-robotbimanualtasks(Bottle,Cap,USB,Zip)is
reportedin6.3togetherwiththerestoftheempiricalevaluation.
5 Deployment
Deploymentmainlyaddressesthreeruntimeissues:mappingend-effectordeltachunkstoheteroge-
neousrobotplatforms,servingVLApredictionsattherobotcontrolrate,andstitchingindependently
predictedchunksintosmoothmotion.Wehandlethemwiththreelightweightcomponents:aplat-
formmapperthatkeepsthelearnedactioninterfaceunchangedacrossembodiments(Sec.5.1);an
asynchronousinference–executionloopthatoverlapsbackboneforwardpasseswithservoexecution
(Sec.5.2);andalatency-awarecubic-Bézierstitcherthatremovesstaleprefixesandenforcessmooth
chunktransitions(Sec.5.3).Thesamedeploymentstackisusedacrossallreal-robotevaluations.
5.1 Embodiment-AgnosticPlatformMapping
Theroleofplatformmappingistopreservetherobot-agnosticcontractestablishedbythedelta-chunk
representation. The policy outputs a 20-dimensional dual-arm action chunk (10 dimensions per
end-effector:a3-DCartesiantranslationanda6-Drotation—thefirsttworowsofanSO(3)rotation
matrix—bothexpressedrelativetotheend-effectorposeatthestartofthechunk,togetherwitha
1-Dgripperopeningcommand).Embodiment-specifickinematicsaredeferredtodeployment,where
the relative SE(3) prediction is composed with the initial end-effector pose to recover absolute
world-frametargetsandinversekinematics(IK)isthensolvedonthetargetrobottoproducejoint
commands.
Forintra-embodimentdeployment(TrackA),theworldframeremainsthesameindeploymentand
datacollection.Forcross-embodimentdeployment(TrackB),datacollectionanddeploymentuse
differentembodiments,soweinstantiatemappingsfortwoembodimenttypes:fixed-basearmsand
thefloating-basehumanoid.Intheequationsbelow,AT denotestheposeofframeBinframeA;
B
W,G ,G ,andC aretheworld,currentgripper,predictedfuturegripperkstepsfurther,andthe
t t+k
chassisframe.
Forfixed-basearmssuchasJAKAK1,therel-EEchunkiscastintotheworldframeusingthecurrent
gripperposeWT fromforwardkinematics,
Gt
WT = WT ·GtT , (10)
Gt+k Gt Gt+k
ForthehumanoidlikeAstribotS1,adeterministicheuristicinfersafixedchassisframeWT anda
C
floatingtorsoframefromthepredictedgrippertargets(AppendixB.1),yielding
CT = (cid:0)WT (cid:1)−1 ·WT ·GtT . (11)
Gt+k C Gt Gt+k
whereWT isaconstanttransformcachedaftercalculation.Theadditional24head/torsodimensions
C
(12each:3position+9rotation)aresetbythisheuristicratherthanpredictedbythepolicy.This
keeps the learned action interface unchanged across Track A intra-embodiment deployment and
TrackBcross-embodimentdeployment.
11

Béz Béz Béz
latency latency latency
Inference
overwrite
𝑎"! ← overwrite on each inference → pop
pop
Execution
History: executed actions for 𝐶" tangent computation
Bézier smooth (buffer) (History)
Fig.7:Asynchronousexecutiontimeline.Policyinference,Béziersmoothing,bufferoverwrite,and
servo-rateactionexecutionareoverlapped;executedactionsarerecordedinHtoestimatetangents
forthenextchunkstitch.
5.2 AsynchronousExecutionforReal-TimeControl
Ahigh-capacityVLApolicyrunsslowerthantherobotservoloop,sosynchronousexecutionwould
leavetherobotidlebetweenforwardpasses.Wethereforedecoupleinferencefromcommanddispatch
usingaproducer–consumerruntimewithathread-safeactionbufferB(Fig.7).Theinferencethread
queriesthepolicyfromthelatestobservationandoverwritesB withasmoothedactionsequence,
whiletheexecutionthreadpopscommandsfromBatthecontrolfrequencyandrecordsrecentposes
for tangent estimation. Overlapping these two loops hides much of the backbone latency behind
continuousexecution.
5.3 Latency-AwareBézierChunkStitching
Chunkstitchingiscriticalinasynchronousexecution:delayedchunksmustbereconnectedtothe
robot’scurrentstatewithoutintroducingmotiondiscontinuities.WeuseacubicBéziersegmentto
formacompactC1-continuousconnectorwithcontrollableendpointpositionsandtangents.
ThefirstdesignchoiceistoselecttheconnectionpointbetweentheBézierconnectorandtheretained
chunk.Wesetγasalightweightdeploymenthyperparameter,chosenaccordingtohardwareresponse
suchasaccelerationlimitsandservorate.Asmallerγ selectsanearlierpointintheretainedchunk
andpreservesmorepolicy-predictedactions,butleaveslessroomtocorrectthedelayedboundary.A
largerγ providesasmootherlandingtargetbutskipsmorepredictedactions.Wecliptheresulting
indexawayfrombothendssothatthefuturetangentcanbeestimatedfromneighboringwaypoints.
Thecontrolpointsarechosenwiththesameintuition.TheBéziercurveshouldleavetherobot’s
currenttrajectoryinthedirectionitwasalreadymoving,andenterthefuturechunkinthedirection
that the policy predicts next. We therefore place the two inner control points along the historical
motiondirectionandthelocaldirectionofthefuturechunk,withtheirdistancescaledbythegap
betweenthecurrentrobotstateandthereconnectionpoint.Thisgivesasmoothtransitionwithout
introducinganadditionallearnedcontroller.
Basedonthisdesign,theruntimeprocedureisasfollows.GivenanoriginalchunkoflengthN,we
firstdiscardthestaleprefix
K =⌈N/α⌉, K ≤N −3, (12)
whereα>1isthetruncationratio,andretainF ={f ,...,f }withM =N −K.
0 M−1
Let h be the last executed EE position. We choose an interior connection point f with c =
0 c
clip(⌊γM⌋,1,M −2), where the clipping keeps the two-sided future tangent well-defined, and
constructacubicBéziersegmentB(t)satisfying
B(0) =h , B(1) =f , B˙(0)∥dˆ , B˙(1)∥dˆ , (13)
0 c hist fut
12

Fig.8:Trajectorycomparisonbetweenrawactionchunks(orange)andtheasynchronousBézier-
smoothedtrajectory(blue).Smoothingreducesvisiblediscontinuitiesatchunkboundariesforboth
armsacrossx,y,andzdimensions.
withtangents
|     |      | h   | −h   |     | f   | −f   |     |      |
| --- | ---- | --- | ---- | --- | --- | ---- | --- | ---- |
|     | dˆ   | 0   | −1   | dˆ  | c+1 | c−1  |     | (14) |
|     | hist | =   | ,    | fut | =   |      | ,   |      |
|     |      | ∥h  | −h ∥ |     | ∥f  | −f ∥ |     |      |
|     |      | 0   | −1   |     | c+1 | c−1  |     |      |
whenthecorrespondingnormisnon-zero.Theendpointcontrolpointsanchorthetransitionatthe
currentstateandthereconnectionpoint,whilethetwoinnercontrolpointsencodethehistoricaland
futuretangents:
| P   | =h  | ,     |     |     | P =P | +λdˆ | ,    | (15) |
| --- | --- | ----- | --- | --- | ---- | ---- | ---- | ---- |
|     | 0   | 0     |     |     | 1    | 0    | hist |      |
| P   | =P  | −λdˆ  | ,   |     | P =f | ,    |      | (16) |
|     | 2   | 3 fut |     |     | 3    | c    |      |      |
whereλ=σ∥P −P ∥controlsthetangentlength.Thetransitioncurveis
3 0
| B(t) | = (1−t)3P |     | +3(1−t)2tP | +3(1−t)t2P |     | +t3P | ,   | (17) |
| ---- | --------- | --- | ---------- | ---------- | --- | ---- | --- | ---- |
|      |           |     | 0          | 1          |     | 2    | 3   |      |
andisuniformlysampledtoreplacethediscontinuousboundarysegment.Positionissmoothedin
R3,orientationusesSLERP,grippercommandsarelinearlyinterpolated,andeacharmisprocessed
independently. The resulting transition is C1-continuous, policy-agnostic, and controlled by the
embodiment-dependentparametersα,γ,andσ.
Fig.8comparesrawchunkedactionswiththeasynchronouslyBézier-smoothedtrajectory.
6 Evaluation
The empirical validation addresses two parallel questions: how well HyVLA-0.5 performs after
standarddownstreamsupervisedfine-tuninginsimulationandonrealhardware(Secs.6.1and6.2),
andhowmuchFlowPROpost-trainingfurtherimprovesadeployedpolicy(Sec.6.3).
Forrealhardware,weorganizetheSFTevaluationintotwodeploymenttracks:TrackAfine-tunes
and evaluates on the same tele-operated robot platform, while Track B fine-tunes only on UMI
demonstrationsanddeploysonmorphologicallydifferentrobotswithouttarget-robotteleoperation.
We evaluate four Track-A tasks and two Track-B tasks. Foundational baselines and are
|     |     |     |     |     |     |     | π 0 | π 0.5 |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- |
identicallyparameterizedandtrainedwithmatcheddataanditerationbudgets.
13

6.1 SimulatedTasks
OnRoboTwin2.0[27],wereporttasksuccessratesaveragedover100stochasticrolloutspertaskand
thenoverthefull50-tasksuite.ResultsareevaluatedunderbothCleanandRandomizedsettings,with
aggregatecomparisonsandablationsshowninTable1;thecompleteper-taskbreakdownisdeferred
toAppendixA(Table3).
| Method | Clean | Randomized |
| ------ | ----- | ---------- |
Othermethods
| π [1] | 65.9 | 58.4 |
| ----- | ---- | ---- |
0
| ABot-M0[31] | 81.2 | 80.4 |
| ----------- | ---- | ---- |
| [2]         | 82.7 | 76.8 |
π 0.5
| Qwen-VLA[32]    | 86.1 | 87.2 |
| --------------- | ---- | ---- |
| LingBot-VLA[33] | 86.5 | 85.3 |
| starVLA[34]     | 88.2 | 88.3 |
| Motus[35]       | 88.7 | 87.0 |
| JoyAI-RA[36]    | 90.5 | 89.3 |
Ablations
| HyVLA-0.5                                 | 90.9 | 90.1 |
| ----------------------------------------- | ---- | ---- |
| w/ocompactmemoryencoder                   | 88.8 | 88.6 |
| w/ocompactmemoryencoderandUMIpre-training | 88.1 | 87.9 |
Table 1: Evaluation results on the RoboTwin2.0 benchmark [27]. Success rate (%) under the
CleanandRandomizedsettings,averagedover100runspertaskandthenoverthe50-tasksuite.The
upperblocklistscompetingmethods;thelowerblockreportsremoval-basedablationsfromthefull
HyVLA-0.5model.Percolumn,thebestresultisinbold.
Baselines and main results. We benchmark against eight contemporary VLA systems—π [1],
0
[2],ABot-M0[31],LingBot-VLA[33],starVLA[34],Motus[35],JoyAI-RA[36],andQwen-
π 0.5
VLA[32]—usingeachmethod’sofficiallyreportedsuccessratesunderthesameCleanandRandomized
protocol.AsshownintheupperblockofTable1,HyVLA-0.5attainsthebestsuccessrateinboth
settings,reaching90.9%onCleanand90.1%onRandomized.Itoutperformsπ by25.0pointson
0
Clean (vs. 65.9%) and by 31.7 points on Randomized (vs. 58.4%), and remains clearly ahead of
by8.2and13.3points(vs.82.7%and76.8%).Evenagainstthestrongestcompetingmethod,
π 0.5
JoyAI-RA,HyVLA-0.5stillleadsby0.4and0.8points(vs.90.5%and89.3%).
Ablation. The lower block of Table 1 conducts a removal-based ablation starting from the full
HyVLA-0.5model.Removingthecompactmemoryencoderreducesperformancefrom90.9%/90.1%
to88.8%/88.6%onClean/Randomized;furtherremovingthelarge-scaleUMIpre-trainingstage
lowers the scores to 88.1%/87.9%. Together, these ablations show that both UMI pre-training
andshort-horizonvisualmemorycontributeconsistentgains.Althoughtheegocentricreal-world
UMIcorpusisvisuallydistantfromthesyntheticRoboTwin2.0renderings,UMIpre-trainingstill
providesamodestgaininsimulation.Thelimitedmagnitudeisexpected,giventhelargegapsin
taskdistribution,actiontrajectories,andvisualappearance.Incontrast,Sec.6.2showsitssignificant
benefitonreal-robottasks,wherethedomaingaptoUMIdemonstrationsissmaller.
6.2 Real-WorldTasks
We evaluate HyVLA-0.5 on real-robotbimanual manipulation throughthe twodeployment tracks
introduced above, spanning three platforms and six benchmark tasks, plus a qualitative force-
discriminationtaskonaUnitreeG1.Allper-tasksnapshotsandsuccessratesarereportedinFigure9.
TrackAtestsintra-embodimentfine-tuning,whileTrackBprobeswhetherUMI-onlypost-training
cantransfertasksemanticsacrossembodiments.
14

Fig.9: Real-robot evaluation on six bimanual manipulation tasks. Left panel: Snapshots of
representativetaskexecutionscapturedduringrollout.Rightpanel:Per-tasksuccessrates(%)after
supervisedfine-tuningontele-operatedorUMIdemonstrations.
Track A — Intra-Embodiment Fine-Tuning (Dobot X-Trainer). Data are collected via tele-
operationonaDobotX-Trainerandthesameplatformisusedforevaluation.Webenchmarkfour
bimanualtasks:InsertBottles,wheretherobotgraspstwocylindricalbottlesandinsertseachintoa
dedicatedholderundertightgeometrictolerances;FoldandStoreGlasses,whereitpicksupapairof
eyeglasses,foldsthetemplesinwardthroughcoordinatedbimanualmotion,andplacesthemintoa
protectivecase;SettheTable,whereitarrangesaplate,afork,andaknifeatcanonicalpositionsona
diningsurface,requiringlong-horizonspatialplanningandprecise6-DoFplacement;andZipUpthe
PenCase,whereitopensthezipper,insertsapen,andclosesthezipperalongthefulltrackunder
deformable-objectdynamics.
EffectofUMIPre-trainingonTrack-ATasks.Theper-taskresultsinFigure9revealaconsistent
patternontheprecision-criticaltasks.ForFoldandStoreGlassesandZipUpthePenCase,success
hingesonafewdecisivesub-stepsratherthanonthetrajectoryasawhole,e.g.foldingthetemples
withoutslipping,orpinchingthezippersliderbeforepulling.WithoutHy-UMI-10Kpre-training,
thepolicyisvisiblylessaccurateatexactlythesemoments,wheresub-centimetrepositioningand
stablebimanualforcecouplingarerequired.Theresultinglocalerrorsthenpropagatedownstreamand
dominatethefailuremodes.Pre-trainingreversesthispattern:predictionssharpenatthesamecritical
moments,end-to-endsuccessratesriseaccordingly,andcoarsersegmentsofthetrajectoryremain
essentiallyunchanged.Thistask-levelevidencecorroboratesthesimulationablationinSection6.1.It
suggeststhattheprincipalvalueoflarge-scale,high-precisionUMIpre-trainingistosharpenthe
actiondistributionattheprecision-criticalbottlenecksofdownstreammanipulation,andthatthis
benefittransfersfromhumandemonstrationstoreal-robotpost-training.
Track B — Cross-Embodiment Transfer (JAKA K1, Astribot S1). For each target robot, we
post-traintheUMIpre-trainedcheckpointontask-specificUMIdemonstrationsonly—withoutany
target-robotteleoperation—anddeploytheresultingpolicyonthecorrespondingrobot.Webenchmark
twotasks:PutAwaytheAccessoryonJAKAK1,wheretherobotpicksupasub-centimetrehair
tieandplacesitintothecentrecellofacompartmentboxwhosecellsizenearlymatchesthetie’s
diameter;andCleanUptheTableonAstribotS1,wherethehumanoidlocatesscatteredpapercups
onatabletopanddepositsthemsequentiallyintoawastebin.
EffectofUMIPre-trainingonTrack-BTasks.TrackBisolatesthecontributionofUMIpre-training
tocross-embodimentdeployment:sincenotarget-robotdataiseverseenduringfine-tuning,anygain
overanidenticallyconfiguredbaselinemustcomefromthepriorlearnedduringpre-training.Figure9
showsthatthisgainissubstantialonbothrobots:HyVLA-0.5achievesmarkedlyhighersuccessrates
thanπ andπ onPutAwaytheAccessoryandCleanUptheTable,despiteallthreepoliciesbeing
0 0.5
post-trainedonthesameUMIdata.Theimprovementindicatesthatlarge-scale,high-fidelityUMI
15

pre-trainingequipsthemodelwithembodiment-agnosticactionpriorsthatsurviveadeploymentshift
tomorphologicallyunseenrobots,andthatthesepriorsmakethesmallUMIfine-tuningsetsufficient
onitsowntorecoverdeployableperformanceonanewplatform.
Force-ModalityValidation(UnitreeG1).BecauseourhandheldUMIgripperrecordstipforcesignals
duringdemonstrationcollection,theresultingdatadirectlycontainsthephysicalcuesneededfor
force-aware,andpotentiallyforce-controlled,manipulation.WeshowthiscapabilityonaUnitreeG1
equippedwithourendeffector,wherethepolicyperformsaforce-discriminationtask:itsequentially
graspstwoboxesandplacesthelighteroneintoafrontbasket.Forthistask,weaugmenttheaction
expertwithtwolightweightTCNencoders[37]andanMLPprojector,whichtogetherencodea50-step
F/Twindowforeachhand(∼2Maddedparameters).Theaugmentedpolicyisthenpost-trainedona
smallsetofUMIdemonstrationsrecordedwiththeworkstation’stipforce/torquesignals(Sec.3.1).
Sincethelighter-objectpositionisrandomizedacrosstrials,spatialmemoryalonecannotsolvethe
task; the policy must compare thegrasp-phase force profiles before deciding which box to place.
HyVLA-0.5 reliably selects the lighter box across trials (Fig. 10), showing that the tactile signals
capturedbytheUMIworkstationprovideactionablenon-visualcuesfordownstreampolicylearning.
Fig.10:Force-guidedobjectdiscriminationonaUnitreeG1.Therobotsequentiallygraspstwo
boxesofdifferingmassandplacesthelighteroneintothefrontbasket,confirmingthatthein-house
UMIworkstationcapturesactionabletactileinformation.
6.3 Real-WorldReinforcement
USB Insertion Pen-Cap Assembly
Fig.11: Additional fine-grained real-robot tasks for FlowPRO post-training. Beyond Insert
Bottles(Bottle,sub-cminsertion)andZipUpthePenCase,whichareshowninFig.9,wefurther
evaluateFlowPROontwofine-grainedtasks:USBinsertion(USB,sub-mmprecision)andPen-Cap
Assembly(Cap,in-airbimanualcoordination).Thisfigureillustratesthesetwoadditionaltasks.
Setup. All FlowPRO experiments are conducted on a Dobot X-Trainer bimanual platform. We
evaluateonfourlong-horizonbimanualtasks(Fig.11):Bottle,Cap,USB,andZip.Startingfrom
thesameHyVLA-0.5SFTcheckpointπref ,everymethodrunsK=3roundsofiterativepost-training
underanidenticaldata-collectionbudget.EachentryinTable2isaveragedover3trainingseeds;
per-seedsuccessrate(SR)iscomputedfromn=100rolloutswithrandomizedinitialplacements,and
completiontime(CT)isaveragedoverthesamerollouts.
Baselines.WecompareRPROagainsttworepresentativecomparatorsthatcoverbothregimesofthe
designspace:DAgger[38](positive-onlydatasetaggregation)andπ *[14](advantage-conditioned
0.6
regressionthatusesthesamepositive-and-negativepairsasRPRObutinjectsthepreferencesignalas
aconditioningtokenratherthanthroughacontrastiveloss).AllmethodssharethesameHyVLA-0.5
SFTbackboneandthesameiterativedata-collectionprotocol.
16

|     |     | Bottle |     |     | Cap |     | USB |     | Zip |     |
| --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Fine-tune
|        |     | SR      | CT  |         | SR  | CT  | SR      | CT  | SR      | CT  |
| ------ | --- | ------- | --- | ------- | --- | --- | ------- | --- | ------- | --- |
| DAgger |     | 93±2.1% | 27s | 88±1.8% |     | 29s | 86±2.4% | 25s | 83±2.0% | 55s |
| π      | *   | 95±1.5% | 24s | 95±1.2% |     | 27s | 95±1.4% | 23s | 89±1.6% | 45s |
0.6
| RPRO |     | 99±0.6% | 16s | 99±0.7% |     | 21s | 98±0.9% | 22s | 94±1.1% | 37s |
| ---- | --- | ------- | --- | ------- | --- | --- | ------- | --- | ------- | --- |
Table 2: Final success rate and completion time after K=3 rounds of post-training on four
real-robotbimanualtasks,withHyVLA-0.5asthebasepolicy.SR(↑,%)isreportedasmean±std
(inpoints)across3trainingseeds,witheachper-seedSRcomputedovern=100randomizedrollouts;
CT(↓,s)isthecross-rolloutmean.Bestpercolumninbold.
Results.Table2andFig.12summarizethecomparison.RPROvs.DAgger.DAggerreliesonpositive
samplesonly,whileRPROadditionallyexploitsnegativetrajectoriesthroughacontrastiveloss;the
resulting per-state push-away gradient from al pulls the policy back from nearby failure modes,
yieldingaconsistentgainacrossallfourtasks.RPROvs.π *.Onidenticalpreferencedata,RPRO
0.6
still outperforms the advantage-conditioned π * baseline. π * relies on the model to discover
|     |     |     |     |     |     | 0.6 | 0.6 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the“improved”/“unimproved”partitionfromasingleconditioningtokenunderapureregression
objective—anindirectpressurethatcanbedilutedbytherestoftheVLMcontext—whereasRPRO
(4.2)injectsthepreferencesignaldirectlyintotheaction-generationloss,pushingπ towardaw and
θ
awayfromal perstateandperchunk.Acrossallfourtasks,RPROattainsthehighestSRwiththe
shortestCT,indicatingbothmorereliableandmoreefficienttaskexecution.
Insert Bottles Pen-Cap Assembly USB Insertion Zip the Pen Case
| SR   |     |     | SR   |     |     | SR   |     | SR  |     |     |
| ---- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- | --- |
| 100% |     |     | 101% |     |     | 100% |     |     |     |     |
95%
| 99% |     |     | 99% |     |     | 98%   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
| 98% |     |     | 97% |     |     | 9 6 % |     | 90% |     |     |
9 4 %
| 97% |     |     | 95% |     |     | 92%   |     | 85% |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
| 96% |     |     | 93% |     |     | 90%   |     |     |     |     |
|     |     |     |     |     |     | 88%   |     | 80% |     |     |
| 95% |     |     | 91% |     |     | 8 6 % |     |     |     |     |
| 94% |     |     | 89% |     |     |       |     |     |     |     |
| 93% |     |     | 87% |     |     | 8 4 % |     | 75% |     |     |
82%
| 92% |           |     | 85% |           |        | 80%    |           | 70% |           |     |
| --- | --------- | --- | --- | --------- | ------ | ------ | --------- | --- | --------- | --- |
|     | 0 1       | 2 3 |     | 0 1       | 2 3    |        | 0 1       | 2 3 | 0 1       | 2 3 |
|     | Iteration |     |     | Iteration |        |        | Iteration |     | Iteration |     |
|     |           |     |     |           | Dagger | PI0.6* | RPRO      |     |           |     |
Fig.12:Per-iterationsuccessrateonthefourreal-robottaskswithHyVLA-0.5asthebasepolicy.
Iteration0correspondstothesharedSFTcheckpoint;iterations1–3correspondtosuccessiverounds
ofpost-training.RPROconsistentlydominatesDAggerandπ *throughouttheiterativeprocess.
0.6
7 RelatedWork
GeneralistVLAModels EarlyVLAsabstractedroboticcontrolintodiscretetokensprocessedby
autoregressiveheadsatoppre-trainedVLMs,asexemplifiedbyRT-2[12]andOpenVLA[13].While
effectivelytransferringsemanticpriors,thisdiscretisationinherentlyconstrainedcontrolfrequency
andspatialprecision.π [1]supplanteddiscreteactionspaceswithflow-matchingvelocityfields,
0
restoringcontinuous,high-frequency(e.g.,50Hz)executioncapabilities.Concurrently,DeepMind
introducedGeminiRobotics[3],bringingGemini-levelreasoningtophysicalcontrol,andNVIDIA
releasedGR00TN1[4],anopenfoundationmodelforgeneralisthumanoidcontrolpre-trainedon
teleoperation,humanvideo,andsyntheticdata.π [2]subsequentlyadvancedtheflow-matching
0.5
paradigmwithopen-worldgeneralization,whileGeminiRobotics1.5[39]extendedtheapproach
withadvancedembodiedreasoningandcross-embodimentmotiontransfer.LingBot-VLA[33]takes
a pragmatic approach, scaling to 20K hours of real-world dual-arm data across 100 tasks with
athroughput-optimisedopen-sourcecodebase.UnlikeautoregressiveVLAs,HyVLA-0.5operates
entirelywithinacontinuousflow-matchingparadigm;unlikeπ andπ ,itadoptsanMoT-based
|     |     |     |     |     |     |     | 0   | 0.5 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
embodied-nativebackbone,reliesona10K-hourUMIpre-trainingcorpus,andfeaturesaspecialised
deploymentprotocolforzero-shotcross-embodimenttransfer.
17

EmbodiedVLMBackbones ThemajorityofcontemporaryVLAsdependongeneral-purpose
vision-language models such as PaliGemma [16] or Qwen-VL [40]. Recently, domain-specific
backbonessuchasRoboBrain[41],RynnBrain[42],andHy-Embodied-0.5[15]haveemergedto
betteraddressthefine-grainedvisualacuityrequiredformanipulation.TheinternalHy-Embodied
report introduced a prototype VLA fine-tuned from 5k hours of UMI data, achieving promising
baselinesuccessratesonX-Trainertasks[15].Buildingstrictlyuponthisfoundation,HyVLA-0.5
doublestheUMIscaleto10khours,implementstherel-EErepresentationtofacilitatehumanoid
deployment,andintroducestheFlowPRORLpost-trainingstage,therebyextendingefficacytounseen
platformsincludingJAKAandAstribotS1.
Pre-training and Post-training Recipes for VLAs Current multi-embodiment pre-training
paradigms, such as TRI’s Large Behaviour Models [43] and the π methodology, primarily
0.5
leverageaggregatedteleoperationdatasets(e.g.,Open-X-Embodiment[44],DROID[45]).Bycon-
trast,thefoundationalpre-trainingsignalofHyVLA-0.5ispredominantlysourcedfromhuman-centric
UMIdata,optimisingtheactionexpertunderasingularflow-matchingloss.
Hand-HeldDemonstrationsandUMI TheUniversalManipulationInterface(UMI)[11]pioneered
thecaptureofrobot-agnosticdemonstrationdataviahand-heldgripperrigs.Subsequentefforts,such
asDexUMI[46],expandedthemorphologicalapplicabilityofsuchrigs.Recently,severalframeworks
haveaddressedthefeasibilityofmigratingUMI-stylehand-helddatatohumanoidandmobilesystems,
suchasEgoMI[47](whichcapturessynchronizedhead-handtrackingforwhole-bodyandactive
visionmanipulation)andHoMMI[48](whichlearnswhole-bodymobilemanipulationdirectlyfrom
robot-freeegocentrichumandemonstrations).HyVLA-0.5scalesUMIdatatoover10khours,and
demonstratesUMI-basedcross-embodimenttransfertoahumanoidunderaStage-2protocolentirely
devoidoftarget-robotteleoperation.
Preference Post-Training in Continuous Control Real-robot post-training pipelines for VLA
modelsbroadlyfallintothreefamilies,eachwithacharacteristiclimitationthatre-emergesinthe
flow-matchingsetting.(i)SFTanditsinteractiveextensions—vanillaSFT[1,13]andDAgger-style
human correction [38]—scale to real hardware but only weakly exploit the failure signals from
autonomousrollouts:vanillaSFTdiscardsthem,whileDAggerusesthemmerelytotriggerexpert
correctionratherthanasadirectoptimizationsignal.(ii)Reward-orvalue-basedRL[14,49–51]
requirestrainingareliablereward,value,oradvantagemodel,whichitselfbecomesakeyobstaclefor
contact-richmanipulationwheredenserewardsignalsaredifficulttoobtain;HIL-SERL[51]and
π ∗[14]additionallyintroducesignificantengineeringoverheadssuchasadvantagevaluesand
0.6
intricaterewardshaping.(iii)Preference-basedRLbypassesrewarddesignviapreferencedata:Direct
PreferenceOptimization(DPO)[52]operateswithoutcriticsbyoptimisinglikelihoodratiosbutwas
originallydesignedfordiscretetext,whilerecentextensionstocontinuousflow-matchingpolicies,
suchasFlow-DPO[29]andthetrajectory-levelGRAPE[53],restorepreferencelearningtoflow-based
VLAsbutinheritthereward-hackingfailuremodeofplainDPOanddilutetheper-statelearning
signal.Unlikeπ ∗,ourFlowPROrecipe(4)isentirelycritic-andreward-free;unlikeFlow-DPOand
0.6
GRAPE,theunderlyingRPROlossanchorstheimplicitrewardviaaproximalregularizerthatexplicitly
forbidstheplain-DPOreward-hackingpathology,andexploitsacontrastive-gradient-cancellation
propertytosafelyco-trainonSFTsamplesthroughthesameobjective.
AsynchronousInferenceandAction-ChunkSmoothing Actionchunking[7]hasbecomethe
de-facto deployment recipe for VLA policies but introduces intra-chunk jitter, chunk-boundary
discontinuities,andidlegapswhenthebackbonelatencyexceedstheservoperiod.Inference-Time
RTC[54]introducesalightweightflow-matchingactionserverthatrefinescoarseactionchunksat
highfrequency,decouplingtheslowbackbonefromfastcontrol;Training-TimeRTC[55]further
co-trainsthisrefinementmodulewiththepolicy.VLASH[56]learnsanadaptivehaltingmechanism
thatdetermineschunksizebasedontaskcomplexity,reducinginter-chunkgaps.Bycontrast,our
deploymentrecipe(5)istraining-freeandplug-and-playforarbitrarypolicies,explicitlyguarantees
C1continuityatchunkboundariesviatangent-alignedcubicBéziercurves,andisapplicabletoboth
Cartesianandjoint-spacecontrol.
18

8 Discussion
HyVLA-0.5Pipeline HyVLA-0.5co-designsdata,representation,policyrefinement,anddeployment
execution for deployable generalist robots, rather than treating the VLA as a standalone policy.
Cross-embodimentdeploymentreliesonacompletesetofcomponentsbeyondmodelscalealone:
high-fidelityUMIdataprovidesreusablesupervisionforlearningprecisemanipulationpriors;the
compactmemoryencoderandrel-EE/delta-chunkrepresentationgivethepolicytemporalcontext
whilekeepingtheactioninterfaceindependentofplatform-specifickinematics;FlowPROconverts
realfailurecasesintocompactofflinerefinementwithoutrequiringlarge-scaleonlineexploration;
andasynchronouschunkstitchingmakesthesamecheckpointexecutableunderrealhardwarelatency.
Thesecomponentsaddressdifferentbottlenecks—dataquality,actionrepresentation,failurecorrection,
anddeploymenttiming—buttheysharethesamegoal:preservingastablepolicyinterfacewhile
absorbingembodiment-specificdifferencesoutsidethelearnedcore.Together,theyturnHyVLA-0.5
fromasinglemodelintoapracticalrobot-learningstackforcross-embodimentdeployment.
FutureWork HyVLA-0.5opensseveralquestionsthatweareeagertoexplore,especiallyaround
data, model generalization, and real-world deployment. On the data side, an important direction
istomovebeyondmotioncapturewhilepreservinghigh-precisionsupervision;exoskeleton-based
collectionisapromisingroutetowardthisgoal.SinceHy-UMI-10Kalreadyprovideshigh-accuracy
actionlabels,italsooffersasimplewaytostudythemarginalvalueofprecisionforpre-training,for
examplebyinjectingcontrollednoiseintothelabels.Inaddition,theegocentricUMIcamerastill
differsfromrobot-mounteddeploymentcameras,leavingroomforsystematicvisualaugmentation
studies.Tosupporttheseexplorations,wewillreleasea2,000-hourself-collectedUMIsubsetand
invitethecommunitytostudythesequestionsandbeyond.
Anotherkeydirectionisreal-worldexecutionefficiency.Indeployment,successisnotonlywhether
therobotcancompleteatask,butalsowhetheritcanexecuteatapracticaltaskcadence.Akeynext
stepisthereforetoimprovedeployment-timeexecutionspeedwhilemaintainingsafetyandprecision.
Thislikelyrequirescombiningdeployment-timeadaptationwithreinforcementlearning.
Finally,theemergenceofembodiedintelligenceremainsanimportantopendirection.HyVLA-0.5
doesnotstudyzero-shotgeneralization,aswebelievethecurrentdatascaleisstillinsufficientfor
makingsuchclaims.Atthesametime,recentsystemssuchasπ [57]havebeguntoshowearlysigns
0.7
ofzero-shotbehavior,suggestingthatlarger-scaledataandstrongerpipelinesmayleadtoqualitatively
newcapabilities.Howtoevaluatethesecapabilitiesrigorously,andhowtouseevaluationitselfto
drivetheiterationofembodiedmodelsanddeploymentpipelines,remainsanopenproblem.
19

References
[1] KevinBlack,NoahBrown,DannyDriess,AdnanEsmail,MichaelEqui,ChelseaFinn,Niccolo
Fusai,LachyGroom,KarolHausman,BrianIchter,SzymonJakubczak,TimJones,Liyiming
Ke,SergeyLevine,AdrianLi-Bell,MohithMothukuri,SurajNair,KarlPertsch,LucyXiaoyang
Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. π : A
0
vision-language-actionflowmodelforgeneralrobotcontrol. arXivpreprintarXiv:2410.24164,
2024.
[2] Physical Intelligence. π : A VLA with open-world generalization. arXiv preprint
0.5
arXiv:2504.16054,2025.
[3] GeminiRoboticsTeam,SamindaAbeyruwan,JoshuaAinslie,Jean-BaptisteAlayrac,Montser-
ratGonzalezArenas,TravisArmstrong,AshwinBalakrishna,RobertBaruch,MariaBauza,
MichielBlokzijl,etal. Geminirobotics:Bringingaiintothephysicalworld. arXivpreprint
arXiv:2503.20020,2025.
[4] JohanBjorck,FernandoCastañeda,NikitaCherniadev,XingyeDa,RunyuDing,LinxiFan,
YuFang,DieterFox,FengyuanHu,SpencerHuang,etal. Gr00tn1:Anopenfoundationmodel
forgeneralisthumanoidrobots. arXivpreprintarXiv:2503.14734,2025.
[5] HaitaoLin,HanyangYu,JingshunHuang,HeZhang,YonggenLing,PingTan,XiangyangXue,
andYanweiFu. Universalposepretrainingforgeneralizablevision-language-actionpolicies.
RSS2026,2026.
[6] SongmingLiu,LingxuanWu,BangguoLi,HengkaiTan,HuayuChen,ZhengyiWang,KeXu,
HangSu,andJunZhu. Rdt-1b:adiffusionfoundationmodelforbimanualmanipulation. In
International Conference on Learning Representations, volume 2025, pages 29982–30009,
2025.
[7] TonyZ.Zhao,VikashKumar,SergeyLevine,andChelseaFinn. Learningfine-grainedbimanual
manipulationwithlow-costhardware. InRobotics:ScienceandSystems(RSS),2023.
[8] TonyZZhao,VikashKumar,SergeyLevine,andChelseaFinn. Learningfine-grainedbimanual
manipulationwithlow-costhardware. arXivpreprintarXiv:2304.13705,2023.
[9] RuihanYang,QinxiYu,YechengWu,RuiYan,BoruiLi,An-ChiehCheng,XueyanZou,Yunhao
Fang,XuxinCheng,Ri-ZhaoQiu,etal. Egovla:Learningvision-language-actionmodelsfrom
egocentrichumanvideos. arXivpreprintarXiv:2507.12440,2025.
[10] QixiuLi,YuDeng,YaoboLiang,LinLuo,LeiZhou,ChengtangYao,LingqiZeng,Zhiyuan
Feng,HuizhiLiang,SichengXu,etal. Scalablevision-language-actionmodelpretrainingfor
roboticmanipulationwithreal-lifehumanactivityvideos. arXivpreprintarXiv:2510.21571,
2025.
[11] ChengChi,ZhenjiaXu,ChuerPan,EricCousineau,BenjaminBurchfiel,SiyuanFeng,Russ
Tedrake,andShuranSong. Universalmanipulationinterface:In-the-wildrobotteachingwithout
in-the-wildrobots. InRobotics:ScienceandSystems(RSS),2024.
[12] AnthonyBrohan,NoahBrown,JusticeCarbajal,YevgenChebotar,XiChen,KrzysztofChoroman-
ski,TianliDing,DannyDriess,AvinavaDubey,ChelseaFinn,etal.RT-2:Vision-language-action
modelstransferwebknowledgetoroboticcontrol. InConferenceonRobotLearning(CoRL),
2023.
[13] MooJinKim,KarlPertsch,SiddharthKaramcheti,TedXiao,AshwinBalakrishna,SurajNair,
RafaelRafailov,EthanFoster,GraceLam,PannagSanketi,etal. OpenVLA:Anopen-source
vision-language-actionmodel. InConferenceonRobotLearning(CoRL),2024.
[14] PhysicalIntelligence.π∗ :AVLAthatlearnsfromexperience.arXivpreprintarXiv:2511.14759,
0.6
2025.
[15] TencentRoboticsXandTencentHYVisionTeam. Hy-Embodied-0.5:Embodiedfoundation
models for real-world agents. Tencent hy technical report, Tencent, 2025. URL https:
//github.com/Tencent-Hunyuan/HY-Embodied.
[16] LucasBeyer,AndreasSteiner,AndréSusanoPinto,AlexanderKolesnikov,XiaoWang,Daniel
Salz,MaximNeumann,IbrahimAlabdulmohsin,MichaelTschannen,EmanueleBugliarello,
etal. PaliGemma:Aversatile3BVLMfortransfer. arXivpreprintarXiv:2407.07726,2024.
[17] PengWang,ShuaiBai,SinanTan,ShijieWang,ZhihaoFan,JinzeBai,KeqinChen,Xuejing
Liu,JialinWang,WenbinGe,etal. Qwen2-vl:Enhancingvision-languagemodel’sperception
oftheworldatanyresolution. arXivpreprintarXiv:2409.12191,2024.
[18] ZhiqiLi,GuoChen,ShilongLiu,ShihaoWang,VibashanVS,YishenJi,ShiyiLan,HaoZhang,
YilinZhao,SubhashreeRadhakrishnan,etal. Eagle2:Buildingpost-trainingdatastrategies
fromscratchforfrontiervision-languagemodels. arXivpreprintarXiv:2501.14818,2025.
20

[19] YihaoWu,HeZhang,JunboTan,XueqianWang,andZhengyouZhang. Flowpro:Reward-free
reinforcedfine-tuningofflow-matchingvlasviaproximalizedpreferenceoptimization. InarXiv
preprintarXiv:2606.05468,2026. Underreview.
[20] Weixin Liang, Lili Yu, Liang Luo, Srinivasan Iyer, Ning Dong, Chunting Zhou, Gargi
Ghosh, Mike Lewis, Wen-tau Yih, Luke Zettlemoyer, and Xi Victoria Lin. Mixture-of-
transformers: A sparse and scalable architecture for multi-modal foundation models. arXiv
preprintarXiv:2411.04996,2024.
[21] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow
matchingforgenerativemodeling. InInternationalConferenceonLearningRepresentations
(ICLR),2023.
[22] PhysicalIntelligence. Multi-scaleembodiedmemoryforvision-language-actionmodels. arXiv
preprintarXiv:2603.03596,2026.
[23] HeZhang,SebastianStarke,TakuKomura,andJunSaito. Mode-adaptiveneuralnetworksfor
quadrupedmotioncontrol. ACMTransactionsonGraphics(ToG),37(4):1–11,2018.
[24] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai,
ThomasUnterthiner,MostafaDehghani,MatthiasMinderer,GeorgHeigold,SylvainGelly,etal.
Animageisworth16x16words:Transformersforimagerecognitionatscale. arXivpreprint
arXiv:2010.11929,2020.
[25] MostafaDehghani,BasilMustafa,JosipDjolonga,JonathanHeek,MatthiasMinderer,Mathilde
Caron, Andreas Steiner, Joan Puigcerver, Robert Geirhos, Ibrahim M Alabdulmohsin, et al.
Patchn’pack:Navit,avisiontransformerforanyaspectratioandresolution. AdvancesinNeural
InformationProcessingSystems,36:2252–2274,2023.
[26] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization, 2019. URL
https://arxiv.org/abs/1711.05101.
[27] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Qiwei Liang, Zixuan Li,
Xianliang Lin, Yiheng Ge, Zhenyu Gu, Weiliang Deng, and Yubin Guo. RoboTwin 2.0: A
scalabledatageneratorandbenchmarkwithstrongdomainrandomizationforrobustbimanual
roboticmanipulation. arXivpreprintarXiv:2506.18088,2025.
[28] XingchaoLiu,ChengyueGong,andQiangLiu. Flowstraightandfast:Learningtogenerateand
transferdatawithrectifiedflow. InternationalConferenceonLearningRepresentations(ICLR),
2023.
[29] JieLiu,GongyeLiu,JiajunLiang,ZhihaoYuan,XingchaoLiu,MengnanZheng,XueweiWu,
QianWang,WeiQin,MinXia,etal. Improvingvideogenerationwithhumanfeedback. arXiv
preprintarXiv:2501.13918,2025.
[30] KuanGuo,YifanLi,andZhengyangChen. Proximalizedpreferenceoptimizationfordiverse
feedback types: A decomposed perspective on DPO. In Advances in Neural Information
ProcessingSystems(NeurIPS),volume38,pages94533–94576,2026.
[31] FanYangetal. ABot-M0:VLAfoundationmodelforroboticmanipulationwithactionmanifold
learning. arXivpreprintarXiv:2602.11236,2026.
[32] QwenTeam. Qwen-vla:Unifyingvision-language-actionmodelingacrosstasks,environments,
androbotembodiments. 2026. URLhttps://arxiv.org/abs/2605.30280.
[33] Wei Wu et al. LingBot-VLA: A pragmatic VLA foundation model. arXiv preprint
arXiv:2601.18692,2026.
[34] StarVLA Community. starVLA: A lego-like codebase for vision-language-action model
developing. arXivpreprintarXiv:2604.05014,2026.
[35] DongBietal. Motus:Aunifiedlatentactionworldmodel. arXivpreprintarXiv:2512.13030,
2025.
[36] TianleZhangetal. JoyAI-RA0.1:Afoundationmodelforroboticautonomy. arXivpreprint
arXiv:2604.20100,2026.
[37] ColinLea,RenéVidal,AustinReiter,andGregoryD.Hager. Temporalconvolutionalnetworks:
Aunifiedapproachtoactionsegmentation. InComputerVision–ECCV2016Workshops,pages
47–54.Springer,2016.
[38] StéphaneRoss,GeoffreyJ.Gordon,andJ.AndrewBagnell. Areductionofimitationlearning
andstructuredpredictiontono-regretonlinelearning. InInternationalConferenceonArtificial
IntelligenceandStatistics(AISTATS),2011.
[39] AbbasAbdolmaleki,SamindaAbeyruwan,JoshuaAinslie,etal. Geminirobotics1.5:Pushing
thefrontierofgeneralistrobotswithadvancedembodiedreasoning,thinking,andmotiontransfer.
arXivpreprintarXiv:2510.03342,2025.
[40] ShuaiBai,YuanboCai,etal. Qwen3-VLtechnicalreport. arXivpreprintarXiv:2511.21631,
2025.
21

[41] HuajieTanetal. RoboBrain2.5:Depthinsight,timeinmind. arXivpreprintarXiv:2601.14352,
2026.
[42] RonghaoDang,JiayanGuo,ZixuanZeng,KangYan,JinpengWu,ChenruiShi,HaifengWang,
LeLiu,ShiyangChen,JinHuang,ZimingHuang,andDeliZhao. RynnBrain:Openembodied
foundationmodels,2026. URLhttps://arxiv.org/abs/2602.14979.
[43] JoseBarreiros,AdityaBhat,EricCousineau,etal. Acarefulexaminationoflargebehavior
modelsformultitaskrobotmanipulation. arXivpreprintarXiv:2507.05331,2025.
[44] OpenX-EmbodimentCollaboration. OpenX-Embodiment:RoboticlearningdatasetsandRT-X
models. InIEEEInternationalConferenceonRoboticsandAutomation(ICRA),2024.
[45] AlexanderKhazatsky,KarlPertsch,SurajNair,AshwinBalakrishna,SudeepDasari,Siddharth
Karamcheti,SoroushNasiriany,MohanKumarSrirama,LawrenceYunliangChen,KirstyEllis,
etal. DROID:Alarge-scalein-the-wildrobotmanipulationdataset. InRobotics:Scienceand
Systems(RSS),2024.
[46] Mengda Xu, Han Zhang, Yifan Hou, Zhenjia Goldie Xu, Linxi Fan, Manuela Veloso, and
ShuranSong. DexUMI:Usinghumanhandastheuniversalmanipulationinterfacefordexterous
manipulation. arXivpreprintarXiv:2505.21864,2025.
[47] JustinYu,YideShentu,DiWu,PieterAbbeel,andKenGoldberg. EgoMI:Learningactive
visionandwhole-bodymanipulationfromegocentrichumandemonstrations. arXivpreprint
arXiv:2511.00153,2025.
[48] Xiaomeng Xu, Jisang Park, Han Zhang, Eric Cousineau, Aditya Bhat, Jose Barreiros, Dian
Wang,ShuranSong,andChengChi. HoMMI:Learningwhole-bodymobilemanipulationfrom
humandemonstrations. arXivpreprintarXiv:2603.03243,2026.
[49] LongOuyang,JeffreyWu,XuJiang,DiogoAlmeida,CarrollL.Wainwright,PamelaMishkin,
ChongZhang,SandhiniAgarwal,KatarinaSlama,AlexRay,etal. Traininglanguagemodels
tofollowinstructionswithhumanfeedback. InAdvancesinNeuralInformationProcessing
Systems(NeurIPS),2022.
[50] JohnSchulman,FilipWolski,PrafullaDhariwal,AlecRadford,andOlegKlimov. Proximal
policyoptimizationalgorithms. arXivpreprintarXiv:1707.06347,2017.
[51] Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey Levine. Precise and dexterous robotic
manipulationviahuman-in-the-loopreinforcementlearning.ScienceRobotics,10(105):eads5033,
2025.
[52] RafaelRafailov,ArchitSharma,EricMitchell,StefanoErmon,ChristopherD.Manning,and
ChelseaFinn. Directpreferenceoptimization:Yourlanguagemodelissecretlyarewardmodel.
InAdvancesinNeuralInformationProcessingSystems(NeurIPS),2023.
[53] Zijian Zhang, Kaiyuan Zheng, Zhaorun Chen, Joel Jang, Yi Li, and Siwei Lyu. GRAPE:
Generalizingrobotpolicyviapreferencealignment. arXivpreprintarXiv:2411.19309,2024.
[54] Physical Intelligence. Real-time action chunking with large models. arXiv preprint
arXiv:2503.07206,2025.
[55] Physical Intelligence. Training-time real-time chunking: Co-training high-frequency action
refinementwithpolicies,2025. PhysicalIntelligenceBlogPost.
[56] JiamingTang,YufeiSun,YilongZhao,etal. VLASH:Real-timeVLAsviafuture-state-aware
asynchronousinference. arXivpreprintarXiv:2512.01031,2025.
[57] PhysicalIntelligence,BoAi,AliAmin,RaichelleAniceto,AshwinBalakrishna,GregBalke,
Kevin Black, George Bokinsky, Shihao Cao, Thomas Charbonnier, et al. π : a steerable
0.7
generalistroboticfoundationmodelwithemergentcapabilities.arXivpreprintarXiv:2604.15483,
2026.
22

Appendix
A RoboTwin2.0EvaluationDetails
Per-taskresults. Table3reportstheper-tasksuccessratesofHyVLA-0.5onthe50-taskRoboTwin2.0
suite.WeevaluateeachtaskundertheCleanandRandomizedsettingsandincludethisbreakdownas
acomplementtotheaggregatecomparisoninTable1(§6.1).
| We apply | an offline cleaning | step because | a small subset | of RoboTwin2.0 | de- |
| -------- | ------------------- | ------------ | -------------- | -------------- | --- |
Data filtering.
mostrationscontainsimplausibleinverse-kinematicssolutions,whichoftenmanifestasabnormal
episodelengths.Foreachtask,weclustertheepisode-lengthdistributionusingHDBSCANwith
cluster-selectionradius5andallothersettingskeptatdefaults.Thisidentifiesstablelengthmodes.
Anepisodeisflaggedasdirtyifitsatisfiesanyofthefollowingconditions:(i)itisassignedasan
HDBSCANnoisepoint;(ii)itbelongstoanunder-populatedlengthmodewithestimatedsizebelow
100episodes;or(iii)itliesinthetop5%lengthtailofthelongestwell-populatedmode.Episodes
passingallthreechecksformthecleansubsetusedfortraining.
Weletthepolicypredictactionsundertwocomplementaryframes:(i)relative-
Actiondecoding.
EEF,whichcapturessmoothlocalmotion;and(ii)EEF,whichanchorsthetargetgloballyandavoids
driftaccumulation.TheEEFbasedactionsareconcatenatedaftertherelativeonesalongthechunk
axis,resultingadoubledchunksize.Atinferencethesetwopredictionsarefused,withquaternion
orientationsinterpolatedviaSLERP,combiningthelocalprecisionofrelativemotionwiththeglobal
stabilityofabsolutetargets.
| Task                | Clean Rand. | Task                    |     | Clean Rand. |     |
| ------------------- | ----------- | ----------------------- | --- | ----------- | --- |
| adjustbottle        | 99 99       | placecanbasket          |     | 91 81       |     |
| beatblockhammer     | 99 99       | placecansplasticbox     |     | 100 100     |     |
| blocksrankingrgb    | 99 99       | placecontainerplate     |     | 98 99       |     |
| blocksrankingsize   | 93 94       | placedualshoes          |     | 94 95       |     |
| clickalarmclock     | 100 100     | placeemptycup           |     | 100 100     |     |
| clickbell           | 100 99      | placefan                |     | 96 98       |     |
| dumpbinbigbin       | 96 98       | placemousepad           |     | 88 93       |     |
| grabroller          | 100 100     | placeobjectbasket       |     | 86 85       |     |
| handoverblock       | 93 73       | placeobjectscale        |     | 90 89       |     |
| handovermic         | 87 98       | placeobjectstand        |     | 94 98       |     |
| hangingmug          | 37 33       | placephonestand         |     | 91 94       |     |
| liftpot             | 99 99       | placeshoe               |     | 98 100      |     |
| movecanpot          | 94 99       | pressstapler            |     | 88 80       |     |
| movepillbottlepad   | 96 96       | putbottlesdustbin       |     | 89 85       |     |
| moveplayingcardaway | 98 96       | putobjectcabinet        |     | 78 83       |     |
| movestaplerpad      | 94 95       | rotateqrcode            |     | 93 98       |     |
| openlaptop          | 99 98       | scanobject              |     | 91 94       |     |
| openmicrowave       | 72 64       | shakebottle             |     | 100 99      |     |
| pickdiversebottles  | 88 72       | shakebottlehorizontally |     | 100 99      |     |
| pickdualbottles     | 82 82       | stackblocksthree        |     | 98 97       |     |
| placea2bleft        | 77 75       | stackblockstwo          |     | 98 99       |     |
| placea2bright       | 74 78       | stackbowlsthree         |     | 87 83       |     |
| placebreadbasket    | 95 93       | stackbowlstwo           |     | 98 97       |     |
| placebreadskillet   | 94 90       | stampseal               |     | 85 81       |     |
| placeburgerfries    | 99 98       | turnswitch              |     | 50 49       |     |
| Average(50tasks)    | 90.9 90.1   |                         |     |             |     |
Table3:Per-taskevaluationresultsof HyVLA-0.5ontheRoboTwin2.0benchmark[27].
23

B SupplementaryDeployment
B.1 UMI-to-RobotDeploymentDerivation
Humanoid-specificderivation. UMIdemonstrationsarerecordedinitsownworldframeandlack
atorsopose.AsendeffectorposesonAstribotS1aredefinedinitsownchassisframe,asmentioned
in Eq. (11), and a torso pose in the chassis frame is crucial for reasonable upper-body poses and
efficientIKsolving,weneedtofindamappingfromUMIworldframetoS1chassisframeandfigure
outatorsoposeaswell.Twomethodologieshavebeenprovedfeasibleeitherbyourexperimentsor
byrelatedworks:
1. Heuristic torso/head pose inference (used in our experiments). A lightweight rule-based
estimator consumes bimanual gripper poses {WT ,WT } and infers the world-to-chassis
GL GR
transform,thetorsopose,andtheheadposesuchthatt(i)thettorsoforwardaxisalignswiththe
centroid of the two gripper positions and (ii) the torso height places both grippers within an
empiricallyestablishedcomfortablereachshelloftheupperbody;seeAlgorithm1fordetails.It
assumesthattheUMIworldframeandtherobotchassisframearerelatedbyapuretranslation
(identicalorientation),whichholdsonAstribotS1.Forrobotplatformswhosechassisframehas
adifferentorientation,anadditionalfixedrotationcanbeappliedwithoutfurtheralteringthe
algorithm.
2. Whole-bodyIKsolvers(alternative).HoMMI-stylewhole-bodyIK[48]jointlyresolvestorso
andarmconfigurationsfromEEtargetsandcouldreplacetheheuristicabove.Wedocumentthis
compatibilityforcompleteness;ourAstribotS1resultsin§6.2usetheheuristicexclusively.
B.2 Track-BReachabilityandDataHygiene
BecauseUMIdemonstrationsarecapturedwithoutarobotintheloop,theyintrinsicallylackany
guaranteeofreachabilityforarbitrarytargetmorphologies.Wedeploytwostandardisedpre-deployment
hygieneprotocols,bothexecutedofflinewithzeroruntimeoverhead:
– UnitreeG1&AstribotS1.Apre-deploymentreachabilityverificationboundstheplannedtask
envelopetotheplatform;tasksexceedingthehumanoid’sreachableshellareexcludedfromthis
report.
– JAKAK1.Thepost-trainingUMIcorpusforagivenJAKAtaskisfilteredviaasingle-passIK
feasibilitycheckonthetargetarm;trajectoriesthatviolateJAKA’sarmkinematicsareremoved
fromthepost-trainingset.
Neithermechanismaltersthepolicyoritsactionrepresentation;theymerelyenforcedistributional
alignmentbetweenthepost-trainingsetandthephysicaldeploymentfrontier.
C FlowPROHyperparameters
Confirmedimplementations:
– Iterations:k ∈{1,2,3};eachroundruns25000optimizersteps(75000total).
– Batchsize:Globalbatchsizeof20(5samplesperGPU).
– Optimizer:AdamW,initiallearningrate1×10−5,linearwarmupover1,000steps,cosinedecay
overthenext15,000stepstoafloorof2.5×10−6.
– Batchcomposition:
• k =1:D
p
1
ref
/DSFT =80/20.
• k ≥2:D
p
k
ref
/D
p
<
re
k
f
/DSFT =70/15/15.
– Distance metric: To find the closest point M′ on τw for a given state M on τl, we use
d(M,M′) = ∥p
M
−p
M′
∥
2
+0.5·dgeo(R
M
,R
M′
)+0.2·|g
M
−g
M′
|, where p ∈3 is the
end-effectorposition,dgeo isthegeodesicdistancebetweenrotationmatricesinSO(3),g ∈[0,1]
isthenormalizedgripperwidth,andtheweightsaresetempirically.
– Initialization:TheStage-2checkpointservesasbothinitialisationθandfrozenreferencepolicy
θ .
ref
– Datascale:≤O(102)preferencepairspertask;X-Trainerrolloutsonly.
24

Algorithm1:HeuristicMappingfromUMIGripperPosestoWhole-BodyTargetsintheChassis
Frame
Input :TW,TW∈SE(3) /* UMI gripper poses in the world frame W */
L R
1 L /* full nominal arm reach (meters) */
2 h 0 /* nominal standing height of chassis–shoulder line */
3 α∈[0,1] /* horizontal back-shift as a fraction of L */
4 ∆z C /* net vertical offset for chassis localization */
5 θ 0 /* constant forward torso pitch */
6 δ∈[0,1] /* blend factor between hand height and h 0 */
7 R align /* fixed UMI→robot gripper-axis rotation */
8 T H T /* fixed torso-to-head calibration transform */
Output Chassis-frametargetsTC,TC,TC,TC.
L R T H
:
/* Step 1: align UMI gripper axes to robot gripper axes */
TW ←TW R
9 L L align
TW ←TW R
10 R R align
/* Step 2: hand midpoint and horizontal facing direction */
11 mW ← 1 2 (cid:0) t(T L W)+t(T R W) (cid:1) /* mean of hand translations */
12 fW ←Π xy (mW)/∥Π xy (mW)∥ /* unit vector in world XY plane */
if ∥Π (mW)∥<εthen
13 xy
14 fW ←e x /* degenerate fallback */
end
15
/* Step 3: one-shot chassis localization (cached per episode) */
if TW isnotcachedthen
16 C
17 pW C ←mW −αLfW +∆z C e z /* back-shift + vertical drop */
TW ←(I, pW )
18 C C
cacheTW
19 C
end
20
/* Step 4: re-express grippers and helpers in the chassis frame */
TC ←(TW)−1TW
21 L C L
TC ←(TW)−1TW
22 R C R
mC ←(TW)−1mW
23 C
fC ←R(TW)⊤fW
24 C
/* Step 5: heuristic torso pose */
25 ψ ←atan2(f y C, f x C) /* yaw aligned with the hands */
26 R T C ←R z (ψ)R y (θ 0 ) /* yaw, then constant forward pitch */
27 pC T ← (cid:0) 0, 0, (1−δ)mC z +δh 0 (cid:1)⊤ /* height = convex blend of hand and standing
*/
TC ←(RC, pC)
28 T T T
/* Step 6: head by fixed torso-to-head transform */
TC ←TCTT
29 H T H
return(TC, TC, TC, TC)
30 L R T H
25

D AuthorContributions
Projectsupervisors. HanHuandZhengyouZhang.
Projectleaders. HeZhangandLingzhuXiang.
Corecontributors. HaitaoLin,ZeyuHuang,MinghuiWang,DingyanZhong,YuboDong,Yihao
Wu,andYongmingRao.
Contributors. DongshengZhang,WanjiaHe,LingChen,KaiHuang,JiahaoChen,SichangSu,
XuminYu,ZiyiWang,ChengweiZhu,XiaoTeng,YuchunGuo,YufengZhang,YuandongLiu,Rui
WangandZishengLu.
26