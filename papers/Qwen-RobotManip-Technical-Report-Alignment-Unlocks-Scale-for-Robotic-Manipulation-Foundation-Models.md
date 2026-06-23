June18,2026
Qwen-RobotManip Technical Report: Alignment Unlocks Scale for
Robotic Manipulation Foundation Models
QwenTeam
https://qwen.ai/blog?id=qwen-robotmanip
https://github.com/QwenLM/Qwen-RobotManip
Abstract
Foundationmodelsinlanguageandmultimodalityachievestronggeneralizationbe-
cause heterogeneous data sources can be aligned under a unified formulation, and
abundantlow-costdatafromtheinternetallowsdiversetrainingsignalstoreinforce
oneanotheratscale. Inthisreport,weinvestigatewhetherthisscalingrecipecanbe
appliedtoroboticmanipulationtoachievegenuinegeneralization. Thisischalleng-
ingbecause,unliketext,manipulationdataisheterogeneousbynature,expensiveto
collect,andnarrowindiversity,makingalignmentandscalesimultaneouslydifficult
toachieve. WepresentQWEN-ROBOTMANIP,ageneralizableVision-Language-Action
foundation model built upon Qwen-VL. QWEN-ROBOTMANIP introduces a unified
alignmentframeworkacrosstherepresentation,motion,andbehavioraldimensionsof
manipulation,makinglarge-scalemulti-sourcetrainingcoherentratherthanconflicting.
ThisalignmentcapabilityinturnenablesQWEN-ROBOTMANIPtoabsorbmanipulation
dataatascalethatpriortrainingregimescouldnotsustain. Toprovideascalingen-
gineformanipulationdata, ahuman-to-robotsynthesispipelineconvertsegocentric
handdemonstrationsintorobottrajectoriesacross15platforms,andarigorouscuration
pipelineharmonizesheterogeneousreal-robotandsyntheticdatasets. Tooursurprise,
byleveragingonlyopen-sourceroboticmanipulationdatasetsandhumandemonstra-
tionvideoswithoutanyproprietarydatacollection,QWEN-ROBOTMANIPconstructsa
∼38,100-hourpretrainingcorpusandalreadyexhibitsemergentgeneralizationcapabili-
ties,includingzero-shotinstructionfollowing,robustnesstoperturbations,reactiveerror
recovery,andcross-embodimentknowledgetransfer. Inexperiments,wefurtherfind
thatmoststandardbenchmarkssystematicallyfailtocapturethequalityofpretraining.
Thus,weinsteadadoptOODevaluationsettings,includingRoboCasa365,LIBERO-Plus,
EBench,RoboTwin-Clean2Rand,RoboTwin-IF(ournewinstruction-followingbench-
mark),andRoboTwin-XE(ournewcross-embodimenttransferbenchmark),asournorth
starformeasuringgenuinegeneralization. QWEN-ROBOTMANIPachievessubstantially
betterperformancethanpriorstate-of-the-artmodels,includingπ ,acrossallOOD
0.5
settings,ranks1stinRoboChallengewitha20%relativeimprovement,andisvalidated
onreal-robotplatformsincludingAgileXALOHA,Franka,UR,andARX.
1 Scaling Robotic Manipulation Data 2 Unified Cross-Embodiment Alignment 3 Performance
Human-to-Robot Synthesis (15 platforms) Joint Pos. EEF Pose Gripper Dexterous I P n- e d r i f s o t r r m ib a u n ti c o e n R E e v a a l l - u W at o i r o l n d
Hand
Representation Alignment
Shared canonical state vector
Unified Motion Alignment
Diverse Robot Embodiments EEF Pose Camera-centric consistency Cross-Embodiment
Transfer
...
Task & Scene
Generalization Instruction
Following
Multi-source Data Curation
4 Scaling Law (Emergent Generalization)
... ... ... ...
Vision System Prompt State Context
> 38,100 Hours
Heterogeneous Manipulation Data Behavior Alignment
Robot Data Human Videos Synthetic Data System prompt and In-
+Vision-Language Co-training Data context adaptation
1
6202
nuJ
71
]OR.sc[
2v64871.6062:viXra

1 Introduction
Foundationmodelsinlanguageandmultimodality(Brownetal.,2020;OpenAI,2023;Dubeyetal.,2024;
Teametal.,2023;Yangetal.,2025;Baietal.,2025;Team,2026)achievestronggeneralizationbecause
heterogeneousdatasourcescanbealignedunderaunifiedformulation,andabundantlow-costdatafrom
theinternetallowsdiversetrainingsignalstoreinforceoneanotheratscale. Inthisreport,weinvestigate
whetherthisscalingrecipecanbeappliedtoroboticmanipulationtoachievegenuinegeneralization.
Thisischallengingbecause, unliketext, manipulationdataisheterogeneousbynature, expensiveto
collect,andnarrowindiversity,makingalignmentandscalesimultaneouslydifficulttoachieve.
ThecurrentstateofVision-Language-Action(VLA)models(Kimetal.,2024;Bjorcketal.,2025;Black
etal.,2024;2025;Community,2026;Liangetal.,2026;Kimetal.,2025)illustrateshowfarthisgapremains.
Despite a rapid succession of models reporting competitive numbers on standard benchmarks (Liu
et al., 2023; Nasiriany et al., 2024; Mu et al., 2025), the generalization being demonstrated is largely
superficial(Zhangetal.,2026c). OODevaluationsinmostworksinvolveonlyminorvisualperturbations
whilepreservingthesameembodiment,taskstructure,andworkspacelayoutasdatacollection,and
performancedegradessharplywhenmodelsaretestedbeyondthesenarrowsettings.
The reason these pretrained priors fail to transfer is twofold. First, existing robotic demonstration
corpora (Padalkar et al., 2024; Khazatsky et al., 2024; Fang et al., 2024) are concentrated in narrow
teleoperationsetups,fartoolimitedinembodimentandtaskdiversityforascalingrecipetotakehold.
Second, and more fundamentally, data diversity alone is insufficient without alignment (Luo et al.,
2026a;Wangetal.,2026). Whendemonstrationsfromdifferentembodimentsarrivewithincompatible
observationandactionrepresentations,scalingdatavolumeproducesinterferenceratherthansynergy.
Priorcross-embodimentefforts(Bjorcketal.,2025;Zhengetal.,2025;Blacketal.,2025)haveadopted
sharedarchitectures,embodimenttokens,orunifiedactiontokenization,butwithoutaformulationthat
makesthesamephysicalmotionnumericallyconsistentacrossembodiments,additionaldatacannotbe
convertedintoimprovedcapability. Alignmentisthereforenotanindependentengineeringchoicebuta
prerequisitefordatascalingitself.
We present QWEN-ROBOTMANIP, a Vision-Language-Action foundation model built upon Qwen-
VL(Yangetal.,2025;Baietal.,2025;Team,2026),designedaroundthisprinciple: alignmentfirst,thenscale.
QWEN-ROBOTMANIPintroducesaunifiedalignmentframeworkacrosstherepresentation,motion,and
behavioraldimensionsofmanipulation,makinglarge-scalemulti-sourcetrainingcoherentratherthan
conflicting: acanonicalstate-actionrepresentationwithper-dimensionbinarymaskingaccommodates
diverserobotmorphologieswithinasingletemplate,acamera-framedeltaposeparameterizationmakes
visually similar motions numerically proximate across coordinate frames, and an in-context policy
adaptationmechanismreadsintra-episodeexecutionhistoryasanimplicitembodimentidentifierfor
kinematic-awarebehavioraladjustment. Trainingisconductedunderadual-streamco-trainingstrategy
thatjointlyoptimizesovermanipulationdataandacuratedvision-languagestream,preventingtheVLM
backbone’sperceptualandreasoningcapabilitiesfromerodingunderactionpredictionpressure.
ThisalignmentcapabilityinturnenablesQWEN-ROBOTMANIPtoabsorbmanipulationdataatascalethat
priortrainingregimescouldnotsustain. Ahuman-to-robotsynthesispipelineconvertsegocentrichand
demonstrationsintorobottrajectoriesacross15platforms,andarigorouscurationpipelineharmonizes
heterogeneousreal-robotandsyntheticdatasets,togetheraccumulating∼38,100hoursofmanipulation
data. Notably,thisentirecorpusisconstructedfromonlyopen-sourceroboticmanipulationdatasets
andegocentrichumanvideoswithoutanyproprietarydatacollection,yetQWEN-ROBOTMANIPalready
exhibitsemergentgeneralizationcapabilities,includingrobustnesstoperturbations,zero-shotinstruction
following,reactiveerrorrecovery,andcross-embodimenttransfer.
Wefurtherarguethatthefield’sevaluationmethodologymustevolvealongsideitsmodels. Standard
in-domainbenchmarks,wheremodelswithoutlarge-scalerobotpretrainingmatchorexceedpretrained
ones(Yanetal.,2025;Community,2026),systematicallyfailtodistinguishgenuinegeneralizationfromin-
distributionpatternmemorization. QWEN-ROBOTMANIPthereforeintroducesOODevaluationsettings
includingLIBERO-Plus(Feietal.,2025),RoboTwin-Clean2Rand(Muetal.,2025),RoboCasa365(Nasiriany
etal.,2026),andEBench(Laboratory,2026),alongsidetwonewbenchmarks:RoboTwin-IF,aninstruction-
followingbenchmarkthattestswhetherpoliciesconditiononlanguageasagenuinecontrolsignalrather
thanexploitvisualshortcuts,andRoboTwin-XE,whichevaluateszero-shottransfertomorphologically
distinctrobots. QWEN-ROBOTMANIPachievesstate-of-the-artonstandardbenchmarksandsubstantially
outperformsexistingVLAmodelsincludingGR00T-N1.7andπ acrossallOODevaluationaxes,ranks
0.5
1stontheRoboChallengeTable30-v1generalisttrackwitha20%relativeimprovement,andisvalidated
on various real-robot platforms and tasks. We hope these results and benchmarks together raise the
standardforhowVLAgeneralizationismeasuredacrossthefield.
2

Ourcontributionsareasfollows.
A unified alignment framework for cross-embodiment training. We address representational het-
erogeneity through three complementary mechanisms. A canonical state-action representation with
per-dimensionbinarymasking,acamera-framedeltaposeparameterizationthatgroundsend-effector
actionsinthevisualdomain,andanin-contextpolicyadaptationmechanismthattreatsintra-episode
executionhistoryasanimplicitembodimentidentifiertogetherenableconsistentsignalextractionacross
diverseembodiments. Adual-streamco-trainingstrategyjointlyoptimizesmanipulationandvision-
languageobjectivestopreservetheperceptualandreasoningcapabilitiesthatunderpingeneralization.
Ascalablemulti-sourcedatacorpus. Weconsolidate∼38,100hoursofmanipulationdatafromopen-
source robot datasets and egocentric human demonstrations. A human-to-robot synthesis pipeline
convertsanyegocentricdemonstrationintotrajectoriesacross15robotplatforms,providingascalable
and embodiment-rich data source. A multi-stage curation pipeline ensures signal quality across all
heterogeneoussources. Beyondmanipulationdata,acuratedvision-languagemixtureincludingnovel
embodiedchain-of-thoughtandegocentricvideounderstandingdatapreservestheVLMbackbone’s
perceptualandreasoningcapabilitiesduringVLAtraining.
AnewstandardforevaluatingVLAgeneralization. WeintroduceOODevaluationsettingsincluding
LIBERO-Plus,RoboTwin-Clean2Rand,RoboCasa365,andEBench,alongsideRoboTwin-IF,abenchmark
that diagnoses genuine language conditioning, and RoboTwin-XE, a benchmark for zero-shot cross-
embodimenttransfer. Wearguethatin-domainmetricsareinsufficientproxiesforfoundationmodel
capabilityandthatOODtransferisthecorrectmeasure. QWEN-ROBOTMANIPsubstantiallyoutperforms
existingVLAmodelsacrossallOODsettingswhileachievingstate-of-the-artonstandardbenchmarks.
Real-robot validation across diverse deployment scenarios. We validate QWEN-ROBOTMANIP on
fourphysicalplatforms(AgileXALOHA,Franka,UR,andARX)acrossin-domain,out-of-domain,few-
shotadaptation,andzero-shotcross-embodimenttransfersettings. OntheRoboChallengeTable30v1
generalisttrack,QWEN-ROBOTMANIPranks1st. Resultsconfirmthatthegeneralizationcapabilitiesof
QWEN-ROBOTMANIPholdunderreal-worlddeploymentconditions.
2 DataSourcesforRoboticManipulation
The quality and diversity of training data are foundational to the generalization ability we seek. To
buildsuchaVLAmodelwithstronggeneralizationacrossembodiments,tasks,andenvironments,we
curatealarge-scaleheterogeneoustrainingcorpuscomprisingthreecomplementarydatamodalities:
roboticmanipulationdemonstrationsacrossdiversehardwareplatforms,egocentrichumanmanipulation
videos, and synthetic robot data generated by our human-to-robot pipeline. A unified curation and
pre-processingpipelineprocessesallsourcestoensurehigh-qualityandconsistentstate,action,video,
andlanguageannotations. Table1summarizesthecompositionofthefullcorpus.
Table1: Overviewofthetrainingdatacorpus.
DataType EmbodimentType DataSources TaskSetting TotalTime
Single-arm {OXE, RoboMIND, DROID, RH20T, Tabletop 3,808h
Robot Dual-arm AgibotWorld-Beta, RoboCOIN, RDT, Tabletop 6,744h
Mobile&humanoid InternData-A1,GalaxeaOpen-World} Tabletop&indoor 868h
Human Humanhands EgoDex,VITRA,EgoVerse Tabletop&in-the-wild 1,933h
Human-to-Robot 15dual-armplatforms Synthesizedfromhumandata. Tabletop&in-the-wild 24,808h
2.1 RoboticDatasets
Robotmanipulationdemonstrationsconstitutethecoreofourpretrainingcorpus,spanningsingle-arm
andbimanualtabletopmanipulation, dexterousmanipulation, mobilemanipulation, andhumanoid
loco-manipulationinbothsimulationandrealworld. Weincorporatenineopen-sourcedatasets,totaling
over11,000hoursofdemonstrations.
OpenX-Embodiment(OXE)(Padalkaretal.,2024)aggregatesreal-worldroboticdatasetsfromdiverse
research institutions. We retain three subsets (Fractal, Bridge, and BC-Z) of high-quality single-arm
tabletopmanipulationdataacrosstheGoogleRobotandWidowXplatforms, contributingabout600
hours.
AgiBotWorld-Beta(AgiBot-World-Contributors,2025)isalarge-scalereal-worldhumanoidmanipulation
3

datasetcollectedontheAgiBotG1bimanualplatform. Weusedatasetscollectedwithgrippers,covering
about200tasktypesand2,400hours.
RoboMIND (Wu et al., 2025a) and RoboMIND 2.0 (Wu et al., 2025b) provide large-scale real-world
datasetscoveringsingle-arm,dual-arm,ALOHA(Zhaoetal.,2023),andhumanoidrobotsacrossdiverse
tabletopmanipulationtasks. RoboMINDspansfourembodimentsincludingFrankaEmikaPanda,UR5e,
AgileXCobotMagicV2.0,andTienKunghumanoid;RoboMIND2.0extendscoveragetosixplatforms
includingFranka,UR5,AgileX,ARX,TienKung,andTianYi. Togethertheycontributeabout1,400hours
ofdemonstrations.
GalaxeaOpen-WorldDataset(GalaxeaAI,2025)provides∼500hoursofreal-worldbimanualmobile
manipulationdemonstrationscollectedonGalaxeadual-armrobotsacrossdiversehouseholdtasks.
RoboCOIN(Wuetal.,2025c)isalarge-scalemulti-embodimentreal-worlddatasetcoveringawiderange
ofbimanualandhumanoidplatforms. Weretain10embodimenttypesincludingAgiBotG1, Airbot
MMK2,AlphaBot2,AgileXCobotMagic,UnitreeG1edu,Leju,RealmanR1Lite,RealmanRMC-AIDA-L,
ALOHA,andTianqinA2,resultinginabout430hoursofdemonstrations.
DROID(Khazatskyetal.,2024)isanin-the-wildsingle-armdatasetcollectedwithFrankaPandarobots
across86diversereal-worldenvironments,contributingabout95,000trajectoriestotaling500hours.
RH20T(Fangetal.,2024)isalarge-scalecontact-richreal-worlddatasetspanning4embodiments(Flexiv,
UR5,Franka,andKuka)withmulti-modalsensingincludingvisual,force-torque,audio,andpropriocep-
tion. Itcovers140+tasksacross42skillcategories,resultinginabout1,100hoursofdemonstrations.
RDT-1B(Liuetal.,2025)provides29hoursofbimanualmanipulationdemonstrationscollectedonthe
ALOHAplatform.
InternData-A1 (Tian et al., 2025) is a large-scale dataset generated in high-fidelity simulation envi-
ronments,coveringvarioussingle-armanddual-armembodimentsacrosspick-and-place,articulated
manipulation,andlong-horizontasks,totalingover3,600hours.
2.2 EgocentricHumanDatasets
Egocentrichumanhandmanipulationdataisnaturallyalignedwiththeperspectiveofrobot-mounted
cameras,servingasanefficientsourceforexpandingmanipulationdata(Kareeretal.,2025;Qiuetal.,
2025;Zhengetal.,2026;Luoetal.,2025;2026b;Zhangetal.,2026a). Wecollectegocentricdatafromthree
sourceswithhandposeannotations.
EgoDex(Hoqueetal.,2025),collectedusingAppleVisionPro,contains338Kdemonstrationsacross194
tabletopmanipulationtaskstotaling829hoursof30Hzegocentricvideo.ItprovidesSE(3)annotationsfor
25jointsofbothhandsperframe,trackedon-deviceusingmultiplecalibratedcamerasandvisual–inertial
SLAM.Weutilize732hoursfortraining.
VITRA(Lietal.,2025a)performsfullyautomated3Dhandreconstruction,cameratrajectoryestima-
tion, and atomic action segmentation on unstructured egocentric videos. It draws from five video
sources: Ego4D (Grauman et al., 2022) (cooking-and-cleaning and general activity subsets), EPIC-
KITCHENS(Damenetal.,2018),EgoExo4D(Graumanetal.,2024),andSomething-Somethingv2(Goyal
etal.,2017),totallingapproximately1Mtrajectories. WeutilizetheEgo4DandEPIC-KITCHENSsubsets,
contributingabout247hoursofvideo.
EgoVerse(Punamiyaetal.,2026)isalarge-scalecollaborativeegocentricmanipulationdatasetspanning
1,362hoursacross1,965tasks,240scenes,and2,087demonstrators. Handposes(21keypointsperhand)
and 6-DoF head poses are recovered via vision-based methods including visual–inertial SLAM and
model-basedposeestimation. Weutilizetheindustry-contributedportion,contributingapproximately
954hoursofvideo.
Thethreesourcescollectivelyamounttoapproximately1,933hoursofvideo.Allhandposesareconverted
intoaunifiedrepresentationofMANO(Romeroetal.,2022)parametersand21keypoints;forsources
lackingnativeMANOannotations,parametersarerecoveredviaoptimization-basedfitting.
2.3 Human-to-RobotDataSynthesis
Asignificantgapexistsbetweenegocentrichumandataandrobotdatainbothmorphologyandvisual
domains. Tobridgethisgap,wemaphumanhandtrajectoriestotherobotactionspace,andreplace
humanhandsinvideoswithrobotmodels. Inspiredbypriorwork(Lepertetal.,2025b;a),wedesign
anend-to-endsynthesispipelinethatexplicitlyseparatestheprocessintoactionalignmentandvisual
4

①Input ②Retarget + Smooth ③Arm Segmentation ④Hand Removal ⑤Base Search + IK ⑥Depth Composite
| Diverse Ego Sources ~1,933 hours |     |     |     | Multi-Scene × Multi-Robot 15 robot morphologies |     |     |     |     |     |
| -------------------------------- | --- | --- | --- | ----------------------------------------------- | --- | --- | --- | --- | --- |
Figure1: Human-to-robotdatasynthesispipeline. (Top)Givenegocentricvideo,thepipelineperforms
actionretargetingandsmoothing,SAM3-basedhandsegmentation,ProPainterinpainting,basepose
∼1,933h
search with MuJoCo IK, and depth-guided compositing. (Bottom) of egocentric data from 3
sourcesisrenderedacross15robotmorphologies,yielding∼24,808hofsynthesizeddemonstrations.
alignment(Figure1).
ActionAlignment. Thisstagefocusesontrajectoryretargetingandsmoothingtobridgethemorphology
gap between human hands and parallel-jaw grippers. We define the robot action at frame t as a t =
(p , R , w ), where p ∈ R3 is the end-effector position, R ∈ SO(3) is the gripper orientation, and
| t t | t   | t   |     |     |     | t   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
w ∈ R is the gripper width. Using the 3D hand keypoints k from MANO, we define a virtual
| t ≥0 |     |     |     |     |     |     | i   |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
fingerk vf asaweightedcombinationoftheindexandmiddlefingertips. Theend-effectorpositionp t is
retargetedasthemidpointbetweenthethumbtipandthevirtualfinger,andthegripperwidthw t istheir
Euclideandistance:
|     |         |       |       |        | 1(cid:0) | (cid:1) |           |      |     |
| --- | ------- | ----- | ----- | ------ | -------- | ------- | --------- | ---- | --- |
|     | k =0.7k |       | +0.3k | ,      | p = k    | +k ,    | w = ∥k −k | ∥ .  | (1) |
|     | vf      | index |       | middle | 2 thumb  | vf      | thumb     | vf 2 |     |
Thegripperorientationisconstructedasaright-handedorthonormalframeR = [x y z].Wefirstestablish
thegraspaxiszalongthejaw-linedirection(thelineconnectingthethumbtipandthevirtualfinger).
Togetherwiththewrist-to-fingertipdirectiond = k −k ,thesetwovectorsdefinethejawplane;the
vf wrist
gripper-normalaxisyisthenormalofthisplane,andtheapproachaxisxcompletestheright-handed
frame:
|     |     |     | s·(k | −k    | )     | z×d   |         |     |     |
| --- | --- | --- | ---- | ----- | ----- | ----- | ------- | --- | --- |
|     |     |     |      | thumb | vf    |       |         |     |     |
|     |     |     | z =  |       | , y = | ,     | x = y×z |     | (2) |
|     |     |     |      | w     |       | ∥z×d∥ |         |     |     |
wheres = +1fortherighthandands = −1forthelefthand. Thissignflipensuresthatzpointsina
consistentdirectionregardlessofhandedness,sothatbothhandsmaptothesamegripperframe. The
threeaxescorrespondto: x–approachdirection,y–grippernormal(perpendiculartothejawplane),z–
graspaxis(alongthejawline).
Per-framehanddetectionintroduceshigh-frequencynoise. WeapplySavitzky–Golay(Savitzky&Golay,
1964)filteringtopositionsandwidths,andGaussian-weightedSLERPtoorientations,producingsmooth
trajectorieswhilepreservingmotionstructure.
VisualAlignment. Thisstagereplacesthehumanappearancewitharobotmodelthroughasequenceof
masking,inpainting,andrenderingstepstobridgethevisualdomaingap.First,SAM3(Carionetal.,2025)
{0,1}H×W
generatesabinarymask M ∈ forthehumanarmusingtextprompts. Next,ProPainter(Zhou
t
etal.,2023)inpaintsthemaskedregionsguidedbyopticalflow,creatingacleanbackgroundsequence
{Iˆ}withouthumanhands.
t
Afundamentalchallengeinconvertingegovideostorobotdataisdeterminingtherobotbaseplacement.
Unlikerobot-to-robottransferwhereasourcebasepositionisavailable,egocentrichandtrajectoriesare
embodiment-free: thereisnophysicalrobotbasetoreference. Weformulatethisasanoptimizationover
baseplacements: givenNtargetend-effectorposes{Tee}N andarobotwithmaximumreachr ,we
|     |     |     |     |     |     | i i=1 |     | max |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
seek:
|     |     |     |      |         | 1 ∑ (cid:104) |                   | (cid:105) |     |     |
| --- | --- | --- | ---- | ------- | ------------- | ----------------- | --------- | --- | --- |
|     |     |     | T ∗  | =argmax | 1 IK(T        | −1 Tee)isfeasible |           |     | (3) |
|     |     |     | base | |K|     |               | base k            |           |     |     |
Tbase
k∈K
5

S1.Sudden Change Detection S2. State-Action Trend Alignment S3. Extreme Value Detection S4. Kinematic Consistency S5. Orientation Alignment
|                         | St a t e   |     | ①   |     |                    | Joints |     |     |     |     |
| ----------------------- | ---------- | --- | --- | --- | ------------------ | ------ | --- | --- | --- | --- |
|                         | A c t i on |     |     |     | q99 + α(q99 - q01) |        |     |     |     |     |
| State/action Trajectory |            |     |     |     |                    | eef    |     |     |     |     |
q99
Smoothed Trajectory
q01
| Residual Trajectory |     |     | ②   |     |                    |     |                    |     |     |     |
| ------------------- | --- | --- | --- | --- | ------------------ | --- | ------------------ | --- | --- | --- |
|                     |     |     |     |     | q01 - α(q99 - q01) |     | eef =?= FK(joints) |     |     |     |
•
|     |     |     |     | For each machine type in each  |     | Resolve: |     |     |     |     |
| --- | --- | --- | --- | ------------------------------ | --- | -------- | --- | --- | --- | --- |
F ilt e r   I t e m s : d a ta s e t ,   q 0 1  a n d   q 9 9   a r e • T C P   o f f s e t R o b o t s   a c r o s s  d i f f e r e n t   d a t a s e t s
| •   | T wo   W r o n | g   C a s e s : |     | c o m p u t e d i n d | e p e n d e n t l y . | •   | J o in t o f f s e t |     |     |     |
| --- | -------------- | --------------- | --- | --------------------- | --------------------- | --- | -------------------- | --- | --- | --- |
R e s i d u a l  ( 1s t  d if f . ) ① S t at e  i s  b e f o r e  A ction  • F r a m e s   w it h   a n y   d i m e n s i on s h a r e   t h e  s a m e  o r i e n t a t i o n   a n d
• A c c e le r a t io n   (2 n d   diff.) • R o t a t io n R epresentation a r e   a l i g n e d  t o   a   c o m m o n   w o r l d
• Jerk (3rd diff.) ② State-Action Trend Misaligned  outside the band are excluded. • … frame.
|       | C1. Instruction Consistency |     |     |                  | C2. Video-State Consistency |     |                          | C3.Video Quality Filtering     |                  |     |
| ----- | --------------------------- | --- | --- | ---------------- | --------------------------- | --- | ------------------------ | ------------------------------ | ---------------- | --- |
|       |                             |     |     |                  |                             |     | Re n d er  r o b o t   r | e p ro je c ti on Black frames | Corrupted frames |     |
| State |                             |     |     | SAM3segmentation |                             |     | ( U R D F   +  j o i     | n t  s ta te s )               |                  |     |
Raw video
| S1~5 C2 |     |     |     |     |      |     | IoU       |     |     |     |
| ------- | --- | --- | --- | --- | ---- | --- | --------- | --- | --- | --- |
|         |     |     |     |     | SAM3 |     | (overlap) |     |     |     |
Action Video
|     | Subtask |     |     |     |     |     |     | Blur frames | StaticSegment |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | ----------- | ------------- | --- |
|     | segment | …   |     |     |     |     |     |             |               |     |
C1
Instruction
|     | M u l ti - ex p e r t   |     |     | W h e n  I o U              | <  th r e s ho l d :                                       |     |     |     |     |     |
| --- | ----------------------- | --- | --- | --------------------------- | ---------------------------------------------------------- | --- | --- | --- | --- | --- |
|     |                         |     | …   | • I f  ca u s e d           | b y  c a m e r a  parameters:  optimize camera parameters  |     |     |     |     |     |
|     | cro s s - m o d e l     |     |     | •                           |                                                            |     |     |     |     |     |
|     | adjudication            |     |     | Else:  exclude the episodes |                                                            |     |     |     |     |     |
…
Figure2: Multi-stagedatacurationpipeline. Five-stagestate-actionsignalfiltering(suddenchange,
trendalignment,extremevalueremoval,FKconsistency,andbase-framealignment)followedbythree
cross-modalqualitychecks(instructionconsistency,video-stateconsistency,andvideoqualityfiltering).
whereK ⊂ {1,...,N}isasetofrepresentativekeyframescoveringthespatialextremesofthetrajectory.
Candidatebaseplacementsaregeneratedviagridsearcharoundthetrajectorycentroid,constrainedby
theper-morphologykinematicreachr max . Thissearchisperformedindependentlyforeachofthe15
robotmorphologies,asdifferentarmlengthsandjointconfigurationsrequiredifferentbaseplacements
forthesametrajectory.
Giventheoptimizedbasepose,weruninversekinematicsinaMuJoCo(Todorovetal.,2012;Zakka,
2026)virtualenvironmenttotrackthesmoothedactiontrajectory,renderingtherobotimage Irobotandits
t
depthmapDrobot. DepthAnythingv3(Linetal.,2025)estimatesametricdepthmapD forthescene.
t t
|                          |     | Mocc | =1[Drobot | ≤   | ]tonaturallycompositetherobotontotheclean |     |     |     |     |     |
| ------------------------ | --- | ---- | --------- | --- | ----------------------------------------- | --- | --- | --- | --- | --- |
| Wecomputeanocclusionmask |     |      |           |     | D t                                       |     |     |     |     |     |
|                          |     |      | t         | t   |                                           |     |     |     |     |     |
background:
(cid:0) 1−Mocc(cid:1)
|     |     | I syn | = Mocc⊙Irobot+ |     |     |     | ⊙Iˆ. |     |     | (4) |
| --- | --- | ----- | -------------- | --- | --- | --- | ---- | --- | --- | --- |
|     |     | t     | t              | t   |     | t   | t    |     |     |     |
Eachhumandemonstrationisrenderedinto15bimanualrobotconfigurations(eachcomposedoftwo
identical arms from: Panda, UR5e, ARX-L5, xArm7, Sawyer, Kinova Gen3, IIWA, Jaco, FR3, UR10e,
ViperX,WidowX,Piper,YAM,AgileXALOHA),yieldingapproximately24,808hoursofsynthesized
demonstrationsintotal.
ActionSpeedAlignment. Egocentrichandmanipulationexhibitssignificantlyhigheractionspeedsthan
robotteleoperationdata. Toaligntheactionspeeddistributions,weapplyper-sourceframesubsampling
duringtrainingtomatchtherobotdataspeed. Specifically,EgoDexisdownsampledto60%ofitsoriginal
framerate(∼1.7×slower),EgoVerseto45%(∼2.2×slower),andViTRAto25%(∼4×slower).
2.4 DataCurationandPre-Processing
Aggregatingmanipulationdataacrossdiverseembodiments,simulators,andcollectionpipelinesintro-
ducesheterogeneousnoiseinrecordedstateandactionsignals,includingdiscreteoutliersfromphysical
collisions,temporalmisalignmentbetweenstateandactionstreamsduetounsynchronizedclocksor
packetloss,extremevaluesthatdestabilizeoptimization,andinconsistentend-effectorconventionsacross
datasetssharingthesamerobotembodiment. Weaddressthesethroughafive-stagefilteringpipeline
appliedtoalldatasetspriortotraining.
Stage1: SuddenChangeDetection. Foreachsignaldimension, weextractasmoothtrendviacas-
cadedmedianfilteringandSavitzky–Golaysmoothing(Savitzky&Golay,1964), thencomputethree
complementarydeviationsignals: theabsoluteresidualbetweentherawandsmoothedtrajectory,the
second-orderfinitedifference(acceleration),andthethird-orderfinitedifference(jerk). Aframeisflagged
whentheresidualexceedsascaledthresholdandeitheraccelerationorjerkalsoexceedsitsthreshold,
reducingfalsepositivesfromslowdriftwhilepreservingsensitivitytoabrupttransients. Thresholdsare
6

setperdatasetaccordingtoembodimenttype,rotationrepresentation,datasource(realvs.simulation),
and base mobility. Exclusion strategies range from frame-level removal to full episode discard. For
instance, in InternData-A1 (Tian et al., 2025) where sudden changes arise exclusively from physical
collisions(e.g.,agrippercontactingarigidobject),thecorruptedepisodeisdiscardedentirely.
Stage2: State-ActionTrendAlignment. In acorrectlyrecordedepisode, action commandsshould
temporally lead or coincide with resulting state changes, which is a causal invariant violated when
timestampsareunsynchronizedorthereispacketloss. Foreachsharedjointdimension, wesmooth
boththestateandactiontrajectories,thenestimatetheoptimaltemporallagviacross-correlation,then
computeadirectionalagreement(DA)metriconlag-alignedfirst-orderdifferences. DimensionswithDA
belowadataset-specificthreshold(typically0.6-0.7)areflaggedandtheirepisodesexcluded. Fordatasets
usingdeltaactions,wefirstintegratetheactionsequencetorecoverabsolutevaluesbeforecomparison.
Thisstagerevealedseverequalityissuesincertainsubsets: 81%ofepisodesintheRoboMINDUR-type
datafailedthischeckandwereexcluded.
Stage3: ExtremeValueFiltering. Frameswithstateoractionvaluesoutsidetheexpectedrangeare
removed to prevent distortion of the quantile-based normalization ([q ,q ] → [−1,1]) used during
01 99
training. Per-dimensionq andq percentilesarecomputedperembodimenttype,andframesoutside
1 99
theband[q −α(q −q ), q +α(q −q )]areexcluded. Gripperdimensionsareexemptduetotheir
1 99 1 99 99 1
bimodaldistributions.
Stage4: Joint-End-EffectorForwardKinematicsConsistency. Wecomputeforwardkinematics(FK)
viaPinocchio(Carpentieretal.,2019)fromeachrobot’sURDFandcompareagainstloggedend-effector
poses. Thediscrepanciescanarisefromdifferingjoint-anglesignconventions, differingend-effector
framedefinitions,incorrectrotationrepresentations,incorrectbase-frameassumptions,anderroneous
end-effector logging. Rather than aggressively filtering, this stage primarily performs data correction:
constantpositionaloffsetsareresolvedbyadjustingthetool-center-point(TCP)definition,andshoulder-
relative bimanual poses are transformed into the world frame. This process revealed that the same
robotmodelcancarrydifferentjoint-angleconventionsacrossdatasets,furthermotivatingtheunified
state-actionrepresentationofSec.3.2.
Stage5: BaseFrameandEnd-EffectorOrientationAlignment. Weapplyper-datasetrotationcorrec-
tionstoalignworld-frameorientationconventions,ensuringthepositivex-axisconsistentlycorresponds
totherobot’sforward-facingdirectionandthattheunifiedstate-actionrepresentationisgeometrically
consistentacrossembodiments.
Beyondthisfive-stagestateandactionsignalqualityfiltering,weapplythreeadditionalcheckstoensure
cross-modalconsistencyacrossvideo,language,andproprioceptiveobservations.
Check1: InstructionConsistency. Weverifysemanticconsistencybetweeneachdemonstrationandits
languageannotationviaathree-stageVLM-basedpipeline. First,longepisodesaredecomposedinto
subtask-levelsegments(Leietal.,2026)sothateachclipcorrespondstoatemporallylocalizedactionunit,
keepingthevisualevidencefocusedandtractableforautomatedassessment(TemporalNormalizationfor
EvaluationUnits). Second,eachsegmentisevaluatedthroughstructuredreasoning-guidedprompting:
ratherthanrequestinganimmediatebinarylabel,theVLMisdirectedtoattendtomanipulatedobjects,
action semantics, temporal ordering, and agent-environment interaction, producing an intermediate
analytical judgment before issuing a final consistency decision. This structured prompting reduces
superficial or heuristic responses and improves label interpretability (Structured Reasoning-Guided
Annotation). Third, clips flagged as non-aligned or ambiguous by the initial model are adjudicated
bymultipleVLMsasindependentevaluators,withthefinallabeldeterminedbycross-modelvoting,
reducingsingle-modelbiasandimprovinglabelrobustness(Multi-ExpertCross-ModelAdjudication).
Inconsistentsamplesareexcludedfromtraining.
Check 2: Video-State Consistency. We perform rigorous data cleaning to remove low-quality or
misalignedsamples. Toverifyvideo-stateconsistency,werendertherobotprojectionintotheimage
plane using the URDF and recorded joint states, segment the actual robot mask with a fine-tuned
SAM3(Carionetal.,2025)model,andmeasuretheiroverlap. Sampleswithlowoverlaparefilteredout.
Check 3: Video Quality Filtering We apply video-level data cleaning to remove frames that may
degradepolicylearning. Weremovevisuallyinvalidframesincludingblack,corrupted,blurred,and
prolongedstaticsegments,usingimageprocessingchecksappliedjointlywithstateandactionsignalsto
detectredundantstaticperiodstypicallyatepisodeboundaries. Task-criticalkeyframessuchasgripper
7

closureeventsareexplicitlypreservedtoavoiddiscardingvisuallysubtlebutsemanticallyimportant
transitions.
2.5 Vision-LanguageCo-trainingDatasets
Prior works have demonstrated that co-training VLAs with vision-language (VL) data mixtures can
significantlyimprovetheirgeneralizationability(Blacketal.,2025;Driessetal.,2025;Fangetal.,2026).
ByincorporatingVLdataduringVLAtraining,themodelretainstherichvisualandsemanticknowledge
acquired from web-scale multimodal pretraining and transfers this knowledge to action generation
throughtheactionexpert. Forexample,thisenablesthemodeltofollownovellanguageinstructions,
operateinunfamiliarscenebackgrounds,ormanipulatepreviouslyunseenobjects.
Tothisend,wecurateacomprehensiveVLdatasetfrommultiplesources,includingproprietarydata,
open-sourcedatasets(e.g.,RoboPoint(Yuanetal.,2024),RefSpatial(Zhouetal.,2025),PixMo(Deitke
etal.,2025),andCapsFusion(Yuetal.,2024)),andcarefullysynthesizedembodied-centricdata. The
resultingVLmixturecomprisesapproximately28Mdatapoints,spanningthefollowingcategories:
(1)GeneralVisualUnderstanding,includingvisualquestionanswering,multi-imagereasoning,and
imagecaptioningatvaryinggranularities(fromsingle-sentencesummariestoparagraph-leveldetailed
descriptions),whichpreservesthemodel’sbroadvisualperceptionandcommonsensereasoningcapabil-
ities;
(2)SpatialPerceptionandReasoning,covering2D/3Dvisualgrounding,pointlocalization,counting,
spatialrelationshipreasoning(depthcomparison,distanceestimation,cameraviewpointinference),and
manipulationfeasibilityreasoning,whicharedirectlytransferabletoroboticspatialunderstanding;
(3) OCR and Document Understanding, which helps maintain the VLM’s ability to recognize text,
numbers,andsymbols,acapabilitythatisalsorequiredinrobotictasksinvolvinglabeledobjects(e.g.,
identifyingablockmarkedwithaspecificnumber);
(4)MultimodalSpecializedKnowledge,coveringdomain-specificvisualreasoningtaskssuchasSTEM
problemsolving,chartinterpretation,andvisualpuzzlereasoning,whichhelpspreventcatastrophic
forgettingoftheVLM’sgeneralmultimodalreasoningcapabilitiesduringVLAfine-tuning;
(5)InstructionFollowing,Multilingual,andPureTextdata,whichstrengthensthemodel’sabilityto
followdiversenaturallanguageinstructions,acapabilitythatiscriticalforgeneralizingtonovelrobot
tasks,whilealsoenablingmultilingualrobotcontrolandpreservingtextgenerationquality;
(6)Embodied-CentricVLData,whichwespecificallycuratetobridgethegapbetweenweb-scaleVL
knowledge and robotic manipulation. This subset includes: (a) embodied chain-of-thought (ECoT)
reasoning data derived from robot manipulation trajectories, where the model performs structured
reasoninginthreestages: firstdescribingthecurrentscenestatefrommulti-viewobservations(including
gripperstatus,objectpositions,andspatiallayout),thenassessingtaskprogressbycomparingthecurrent
stateagainsttheoverallgoal,andfinallypredictingthenextatomicmanipulationaction;(b)egocentric
videounderstandingdata,wherethemodeldescribesfine-grainedhand/armmovements,hand-object
interactions,andobjectstatechangesfromshortclipsoffirst-personhumanmanipulationvideos;and(c)
2Dtrajectorypredictiondata,wherethemodelpredictsfuturemovementtrajectoriesofhumanhandsor
robotend-effectorsassequencesofnormalized2Dcoordinates,conditionedonvisualobservationsand
taskinstructions.
Amongthese,categories(1)–(5)serveadualpurpose: theypreventcatastrophicforgettingofthepre-
trainedVLM’sgeneralcapabilities,whilecertainsubsets,suchasspatialreasoning,visualgrounding,and
OCR,directlybenefitroboticmanipulationbystrengtheningthemodel’sspatialunderstanding,object
recognition,andscenegeneralization. Category(6)isspecificallycuratedtobridgeVLunderstanding
andactiongeneration: ECoTdatateachesthemodeltoperceiveembodiment-specificscenestates,track
taskprogress,andreasonaboutnextactionsinlanguage. ThisencouragestheVLMbackbonetobuild
richerembodiedrepresentationsthataremoredirectlyusefulfordownstreamcontinuousactiongenera-
tion(Zawalskietal.,2024;Chenetal.,2025c);egocentricvideodataexposesthemodeltofine-grained
humanmanipulationpatternsandobjectstatetransitionsfromafirst-personperspective,grounding
itsunderstandingofhowphysicalinteractionsunfold,includinghowobjectsdeform,slide,ortopple
undercontactandhowhand-objectconfigurationsevolveduringgrasping,placing,andtooluse. This
knowledgetransferstoroboticmanipulationdespitetheembodimentgap. Inaddition,2Dtrajectory
predictiondatadirectlyconnectsvisualobservationstospatialmotionreasoninginimagecoordinates,
andtogetherthesedatasourcesestablishasharedrepresentationalfoundationthatfacilitatesknowledge
transfertolow-levelactionpredictionthroughtheactionexpert.
8

Table2: Taxonomyofatomicactiontypes.
| Category | ActionType | Example |
| -------- | ---------- | ------- |
Reach(andgrasp) “Reachtowardtheredcupontheleftsideofthetableandgraspit.”
Movement Move(andrelease) “Movetheheldcupontothewoodentrayandreleaseit.”
|              | Flip         | “Flipthegoldenpancake180degreesinthefryingpan.”  |
| ------------ | ------------ | ------------------------------------------------ |
|              | Rotate       | “Rotatetheblackknobontheovendoorclockwise.”      |
|              | Toggle       | “Toggletheredpowerswitchtoon.”                   |
|              | Open         | “Openthewoodendrawerontheleftsideofthecabinet.”  |
| Manipulation | Close        | “Closethelidoftheblacklaptop.”                   |
|              | Push         | “Pushtheyellowblockforwardalongthetable.”        |
|              | Pull         | “Pullthesilverdrawerhandleawayfromthecabinet.”   |
|              | Insert       | “Inserttheredpegintothecircularholeintheboard.”  |
|              | Press        | “Pressthespongeagainstthetablesurface.”          |
|              | Click        | “Clicktheredbuttononthecontrolpanel.”            |
|              | Strike       | “Strikethesilvernailwiththewoodenhammer.”        |
|              | Handover     | “Movetheheldcabletowardtherightarmandreleaseit.” |
| Special      | Returntohome | “Returnthearmtoitshomeposition.”                 |
|              | Other        | “Pourthewaterfromtheredcupintotheglass.”         |
Wedescribethesynthesisprocedureforeachtypeofembodied-centricVLdatabelow.
EmbodiedChain-of-Thought(ECoT)Data. Inspiredbypriorwork(Zawalskietal.,2024;Fengetal.,
2026;Lietal.,2026),weconstructECoTsupervisionthattrainstheVLMtojointlyperformthreeformsof
embodiedreasoning:describingthecurrentscene,assessingtaskprogress,andpredictingthenextatomic
manipulationaction. Forasampledtimestamptinamanipulationtrajectorywithtaskinstruction,we
synthesizeoneECoTannotationusingboththecurrentmulti-viewobservationandadditionaltrajectory
contextavailableonlyatannotationtime.
Specifically,attimestampt,wefirstextractsynchronizedimagesfromallavailablecameraviews(e.g.,
front,wrist,andsideviews).Wethenconstructthreeformsofadditionalcontext.First,webuildamemory
summarybyuniformlysubsamplingframesfromthebeginningoftheepisodeuptotandpromptinga
strongVLMtosummarizecompletedactionsandvisiblestatechanges. Thismemorymainlysupports
taskprogressassessmentduringannotation,sincemanyintermediategoalsorpriormanipulationsareno
longerdirectlyobservableinthecurrentframe. Second,weconstructafutureactionpreviewfrom6frames
sampledat1-secondintervalsstartingfromtandaskastrongVLMtosummarizetherobot’simmediate
future behavior in this short clip. This future preview provides direct annotation-time evidence for
predictingthenextatomicaction. Third,wecomputeacoarsetemporalprogressestimatefromtherelative
positionoftwithinthefulltrajectory,whichservesasaweakauxiliarycueforjudgingwhetherthetask
islikelyclosetocompletion.
Giventhemulti-viewimagesatt,thetaskinstruction,andtheauxiliaryannotation-timecontextdescribed
VLM1
above, we prompt a strong to generate a structured three-part ECoT response: (1) a Scene
Descriptionsummarizingobservableobjects,spatialrelations,robotarmpositions,andgripperstates;
(2)aTaskProgressAssessmentevaluatingcompletedsubgoalsandendingwithanexplicitcompletion
judgment (Task complete. or Task not yet complete.); and (3) a Next Action predicting a single atomic
manipulationstepfromTable2. AlthoughtheannotatingVLMhasaccesstoprivilegedtrajectorycontext,
the prompt requires the generated ECoT text to be expressed using only evidence from the current
observationandtaskinstruction. Duringtraining,eachECoTdatasampleisconvertedintoastandard
VLinput-outputpair: themodelreceivesonlythemulti-viewimagesandtaskinstruction,andistrained
togeneratethefullthree-partECoTtext. Theprivilegedsignalsareusedonlyduringdatasynthesisto
improveannotationqualityandareexcludedfromtraininginputs.
EgocentricVideoUnderstandingData. Weconstructegocentricvideounderstandingdatafromthe
humanmanipulationvideos. Foreachepisode,wesplitthemain-cameravideointonon-overlapping
clipsofrandomduration(1.5–3seconds)andextract4uniformlyspacedframesperclip(at0%,33%,67%,
and100%oftheclipduration). AstrongVLMispromptedtodescribethefine-grainedmanipulation
actionsobservedacrossthe4-framesequence,includinghandandarmmovementdirections,hand-object
interactionswithspatialrelationships,andanyobjectstatechanges. Clipswithverylittlevisualchange,
as determined by the VLM, are filtered out to avoid training on uninformative static segments. The
resultingannotationsteachthemodeltoperceiveanddescribethedynamicsofphysicalmanipulation
1Inpractice,weuseQwen3.6-PluswiththinkingmodethroughouttheECoTdatasynthesisprocess.
9

fromanegocentricperspective,complementingtheECoTdata,whichoperatesonrobotobservations.
2DTrajectoryPredictionData. TofurtherfacilitatetheVLMinlearningmotionplanningfromboth
roboticandhumanmanipulationdemonstrations,whilealleviatingambiguityindepthperception,we
projectthetrajectoriesoftherobotend-effector(EEF)andthehumanhandinegocentricdataontothe
imageusingtheestimatedcameraparameters. Inaddition,wefilteroutsampleswithlittlemotionusing
abounding-box-basedcriterion,therebyremovinguninformativedatapointsinwhichtheEEForhuman
handbarelymoves.
3 Qwen-RobotManip: TheGeneralizableVision-Language-ActionModelDesign
3.1 MainArchitecture
QWEN-ROBOTMANIP followsadecoupledarchitectureconsistingofavision-languagebackbonefor
multimodalperceptionandsemanticreasoning,andaflow-matchingactionexpertforcontinuousaction
generation. Thisdecouplingallowstheactionexperttospecializeinhigh-frequency,fine-grainedmotor
control while the backbone retains and extends its pretrained perceptual and reasoning capabilities
throughjointend-to-endtraining.
Vision-language backbone. We adopt Qwen3.5-4B (Team, 2026) as the vision-language backbone.
Qwen3.5isanativelymultimodalmodeltrainedwithearlyvision-languagefusion: visualtokensfroma
VisionTransformerwithdynamic-resolutionspatialmergingareinterleaveddirectlyintothetexttoken
streamandprocesseduniformlyacrossimagesandlanguageinstructionswithinasingletransformer.
Givenoneormorecameraviewstogetherwithanaturallanguagetaskinstruction,thebackboneencodes
themjointlyintocontextualrepresentations(e.g.,last-layerhiddenstatesD =2560)thatcaptureboth
vlm
fine-grainedvisualfeaturesandtask-levelsemantics,whicharethenconsumedbytheactionexpertvia
cross-attention.
Actionexpert. WeattachaDiffusionTransformer(DiT)(Peebles&Xie,2023)asaflow-matchingaction
expert (Chi et al., 2023; Black et al., 2024; Liang et al., 2023) for learning precise continuous actions
frombothrobottrajectorydataandegocentrichumandemonstrations. Theexpertconsistsof N=10
transformer blocks with hidden dimension D =768 and 12 attention heads. Each block performs
act
self-attentionovertheconcatenatedstate-and-actiontokensequence,followedbycross-attentiontoVLM
hiddenstatesandaSwiGLUfeed-forwardnetwork. Cross-attentionlayersalternatebetweenattending
tovisualtokens(even-indexedblocks)andlanguagetokens(odd-indexedblocks),bothextractedfromthe
finallayeroftheVLM,lettingtheexpertseparatelygroundactionpredictionsinspatialobservationsand
linguisticinstructionsateachprocessingstage. Therobot’sproprioceptivestateisencodedbyatwo-layer
MLP and prepended to the noisy action token sequence before entering the DiT blocks. The expert
isfurtherconditionedondenoisingtimestepembeddingsandadditionallearnedcameraembeddings
detailedin§§3.3.
Theexpertistrainedwithaflow-matchingobjective(Lipmanetal.,2023;Esseretal.,2024). Givena
ground-truthactionchunka,atimestept ∼Beta(1,1.5)issampledandaninterpolantx = (1−t)ϵ+ta
t
isconstructedfromGaussiannoiseϵ ∼ N(0,I). Themodelisthentrainedtominimizemeansquared
erroronthepredictedvelocityfield x −x . Atinference, actionsequencesareproducedvia4Euler
1 0
integrationsteps,enablinglow-latencyreal-timecontrol.
3.2 Cross-EmbodimentStateandActionRepresentation
Heterogeneousproprioceptivestatesandactionspacesacrossembodimentsmakescalabletrainingon
mixedmulti-embodimentdatasetsakeychallenge. Weaddressthisbyintroducingan80-dimensional
canonical vector representation for states and actions. The representation is structured as two 29-
dimensionalper-armblocksfollowedby22reserveddimensions. Eachper-armblockisorganizedinto
thefollowingsemanticgroups:
• Jointpositions(7dims): jointpositionsfortherobotarm;
• End-effectorpose(9dims): Cartesianposition(3)andorientationina6Dcontinuousrotationrepre-
sentation(Zhouetal.,2019)(6);
• Gripperstate(1dim): jointpositionfortheparallelgripper;
• Dexteroushandjoints(12dims): activehandjointpositionsforembodimentsequippedwithmulti-
fingereddexteroushands.
10

Architecture Design Overview
|                          |     |     |     | VLM co-train output | (separate batch from VLA; |     |     | Velocity field |
| ------------------------ | --- | --- | --- | ------------------- | ------------------------- | --- | --- | -------------- |
| Last-layer hidden states |     |     |     |                     | mutually exclusive.)      |     |     |                |
|                          | ... | ... |     | ...                 |                           | ... |     | ...            |
k, v
|     | CaPE + TimePE |     |     | No PE | CaPE + TimePE |     |     |     |
| --- | ------------- | --- | --- | ----- | ------------- | --- | --- | --- |
DiT
mroNSMRoreZadA
Qwen-VL
CaPE + TimePE
|          | ...        | ...   |                         | ...                              |             | ...     |         | ...                   |
| -------- | ---------- | ----- | ----------------------- | -------------------------------- | ----------- | ------- | ------- | --------------------- |
|          | Vision     |       |                         | Language                         |             | Context | Queries | State & noisy actions |
|          | Left Front | Right | Structured              | Embodied                         |             |         |         |                       |
| tnerruC  |            |       | Embodiment              | Chain of                         |             |         |         | ...                   |
|          |            |       |                         | Prompt Thought                   | Context MLP |         |         |                       |
|          |            |       | embodiment: robot_aloha | scene: shirt flat,  pinch sleeve |             | ...     |         |                       |
| suoiverP |            |       | instruction:            | progress: not                    |             |         |         | Conditions:           |
|          |            |       | fold the clothes        | complete                         |             |         |         |                       |
|          |            |       | speed:1000              | next: grasp right                |             |         |         | denoise timestep      |
|          |            |       | ...                     | sleeve                           |             |         |         | end-effector type     |
All cameras, sampled timestamps Instruction & prompt History state & actions has camera parameters
Unified State & Action Representation Unified End-Effector Motion Prediction
Planned Action Trajectory
|     |     | DiT |     |     | Camera |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- |
Action Reference Frame
|     | ... |     | ... | ... |     |     | Current State |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- |
Desired State
Left Arm Actions Right Arm Actions ... Relative EEF Action Camera Delta Action
"!
!
|     | Joint Pos. EEF Pose (9D) |     | Gripper | Dexterous Hand |     |     |     |     |
| --- | ------------------------ | --- | ------- | -------------- | --- | --- | --- | --- |
|     | (7D) [3D pos + 6D rot]   |     | (1D)    | (12D)          |     |     |     |     |
Figure3: OverviewofQWEN-ROBOTMANIP. ThemodelcouplesaQwen-VLbackbonewithaflow-
matching Diffusion Transformer (DiT) action head. The backbone jointly encodes multi-view visual
tokens, structured embodiment prompts, and historical context tokens, with last-layer hidden states
injectedintotheDiTviaalternatingcross-attention. Statesandactionsshareaunified80-dimensional
canonicalrepresentation,withend-effectoractionsexpressedascamera-framedeltaposestoalignthe
actionspacewithvisualobservationsacrossembodiments,conditionedoncameraandend-effectortype
embeddingsforembodiment-awaredenoising. VLMco-trainingandVLAtraininguseseparatebatches,
whereeachbatchcontainseither(Vision,QA)or(Vision,Language,Context,Action)data.
Thetrailing22reserveddimensionsaresharedacrossbotharmsandareavailableforadditionaldegreesof
freedomsuchasmobile-basevelocity. Forthestatevector,allvaluesareexpressedinabsolutecoordinates.
Fortheactionvector,jointactionsareexpressedasabsolutevaluesandend-effectoractionsareexpressed
asrelativedeltasfromthecurrentstate. Inparticular,end-effectororientationdeltasareparameterized
as 3D rotation vectors rather than the 6D representations used for states. §§ 3.3 further details the
camera-framedeltarepresentationforend-effectoractions.
Differentrobotembodimentspopulatedifferentsubsetsofthiscanonicaltemplate. Forexample,a7-DOF
single-armgripper(e.g.,FrankaPanda)fillsthejoint,end-effector,andgripperfieldsofonearm,leaving
theremainingdimensionsaszero. Adual-armsystem(e.g.,ALOHA)fillsbothper-armblocks. Arobot
withdexteroushandsadditionallypopulatesthehand-jointdimensions. Zero-paddeddimensionsare
excluded from the training loss via a per-dimension binary mask, ensuring that gradients flow only
through semantically populated entries and preventing spurious supervision on structurally absent
degreesoffreedom.
3.3 UnifiedEnd-EffectorMotionPrediction
Thecanonicalstate-actionrepresentationof§§3.2unifiesthestructurallayoutofstatesandactionsacross
embodiments,butdoesnotyetaddressasubtlersourceoffragmentation: end-effectorposesrecordedin
differentcoordinateframesacrossdatasets(Lyuetal.,2026). Whenthesamemotionisexpressedrelative
todifferentbaseframesorcameraframesdependingonthedatasource,themodelmustlearntoreconcile
thesegeometricinconsistenciesratherthanfocusingontheunderlyingmanipulationskill. Weaddress
thisbygroundingallend-effectoractionsinasharedcamera-framedeltaposerepresentationandinjecting
camerageometrydirectlyintotheactionexpertviapositionalencodings. Togetherwithembodiment-
11

awareconditioning,thisensuresthatactionswhichappearvisuallysimilararenumericallyproximate
acrossembodiments,enablingthemodeltoextractcross-embodimentsynergiesfromheterogeneous
data.
Concretely,weextractN ∈ {1,2}independent40-dimensionalper-end-effectortokensfromthe80-
ee
dimensionalstate-actionvector. The29activedimensionsofeacharmarepackedintoa40-dimensional
slotwith11reservedforfutureextension,andtheDiTprocessesthesetokensjointlyviaself-attention.
Camera-framedeltaposeactionrepresentation. Ratherthanrepresentingend-effectormotionasan
absoluteposeintherobotbaseframe,arelativeposeintheend-effectorlocalframe,oraworld-frame
delta,weadoptacamera-framedeltaposerepresentation(Chenetal.,2025a). Itskeypropertyisthatactions
appearing visually similar in the image are also numerically proximate in the action space, directly
aligningtheactionrepresentationwiththevisualobservationspaceandfacilitatingcross-embodiment
transfer. Thisrequirescalibratedcameraintrinsicsandextrinsicsatbothtrainingandinference.
Formally,letcdenotethereferencecameraframe,ethecurrentend-effectorframe,ande∗ thedesired
end-effectorframeatafuturestep. Theposecomponentofthepredictedactionis:
(cid:20) (cid:21)
a = c e Re e∗ Re c R c e Ret e∗ (5)
p 0 1
TherotationalblockcRe ReRexpressestherelativeend-effectorrotatione Rinthecameraframeby
e e∗ c e∗
conjugatingwiththecamera-to-end-effectorextrinsics,whilethetranslationalblockc e Ret e∗ projectsthe
desiredend-effectordisplacementintocameracoordinates. Thefullexpressionisthusgeometrically
equivalenttoprojectingtherelativeend-effectoractionintothecameraframeviatheextrinsics. Amore
compactalternativeis(Zhangetal.,2026b):
a
p
= c e∗Te
c
T (6)
Whileeq.(6)eliminatesend-effectordefinitioninconsistenciesentirely,itstranslationalcomponentis
coupledwiththerelativeend-effectorrotatione Randthecamera-to-end-effectoroffsetet ,makingit
e∗ c
moresusceptibletolong-taildistributionsandmoresensitivetocalibrationerrors. Wethereforeadopt
eq.(5)inimplementation.
Camera-awarepositionalencoding. Toenabletheactionexperttoreasonaboutcamerageometry,wein-
jectcameraparametersintotheDiT’scross-attentionlayersviaCameraPositionalEncoding(CaPE)(Kong
etal.,2024). CameraposeisencodedviaCaPE,occupying32ofeach64-dimensionalattentionhead’s
dimensions, with the remaining 32 used by RoPE (Heo et al., 2024) for temporal indexing. Each im-
agetoken’spositionalencodingisderivedfromtheextrinsicsofitscorrespondingcamera,whileeach
state/action token uses the extrinsics of its selected reference camera. Because CaPE is a rotational
positionalencoding,theglobalworld-frameorigincancelsalgebraicallyinthedot-productattention,
leavingonlytherelativeposebetweeneachvisualtokenandthequeryingstate/actiontokens.
FollowingthepracticeofGTA(Miyatoetal.,2024)andPRoPE(Lietal.,2025b),weapplyCaPEnotonly
tokeysandqueriesbutalsotovaluesandattentionoutputs,strengtheningthegeometricconsistency
of the cross-attention. Camera intrinsics are incorporated by projecting the normalized image-plane
coordinatesofeachvisualpatchthroughalearnedlinearlayerandaddingthemtothecorresponding
imagetoken,providingper-tokenfield-of-viewawareness.
End-effector-awareconditioning. Beyondthedenoisingtimestep,theDiTisfurtherconditionedontwo
additionalsignals,bothappliedviaadditiveembeddingsthroughadaptivelayernormalization(Peebles
&Xie,2023).
1. End-effectortypeembedding: alearnedcodebookentryperend-effectorcategory(single-arm,dual-arm
left,dual-armright,egocentrichead,ormobilebase)associatedwitheachstate/actiontoken,allowing
themodeltoapplyembodiment-specificactionpriors.
2. Auxiliaryflagembedding: abinaryembeddingindicatingwhethercalibratedcameraparametersare
availableforthecurrentsample,switchingthepredictedposeactionspacebetweencamera-frame
deltamodeandrobot-baserelativemode.
Multi-viewreferencecameraselection. Inmulti-viewsettings,theend-effectoractionisexpressed
relativetoachosenreferencecameraframe. Duringtraining,forsingle-armdatasetswerandomlyselect
any available external or wrist-mounted view as the reference. For dual-arm datasets, we randomly
applyoneoftwostrategies: (1)botharmsshareahead-mountedcameraoranyavailablethird-person
viewasthecommonreferenceframe;(2)theleftarmusestheleftwristcameraandtherightarmusesthe
rightwristcameraastheirrespectivereferenceframes.
12

WithintheDiT’scross-attention,eachimagetokenusestheposeofitscorrespondingcameraforCaPE,
whileeachstate/actiontokenusestheposeofitsselectedreferencecameraforCaPE,guidingtheDiTto
denoisethecameradeltaactionexpressedinthatreferenceframe. BecauseCaPEisarotationalencoding,
inter-viewrelativeposesareencodedimplicitly,withtheworld-framesuperscriptcancelingalgebraically.
3.4 EmbodimentPrompt
Weadoptastructuredprompttoconditionthepolicyonbothtasksemanticsandexecutioncontext. Each
promptconsistsofthefollowingfields:
• Embodiment: therobotplatform(e.g.,robot_aloha),enablingthemodeltoaccountformorphological
andcontroldifferencesacrossembodiments.
• Instruction: thehigh-leveltaskdescription,definingtheoverallobjectiveoftheepisode.
• Speed: theepisodelengthintimesteps,discretizedintobinsof500steps.
• FPS:thetemporalsamplingrateoftheinputsequence.
• CameraViewDirection: thecamera’spositionrelativetotherobotarm,eitherarm sideoropposite
side.
StructuredEmbodimentPromptExample
embodiment:robot_aloha
instruction:Take the toy off the table and put it on the mat.
speed:1000
fps:30
cameraviewdirection:arm side
Together,thesefieldsallowthemodeltocapturenotonlywhattaskshouldbeperformed,butalsowhich
robotisactingandhowthebehavioristemporallystructured,reducingambiguityinpolicylearning,
improvingadaptabilityacrossembodiments,andincreasingrobustnesstovariationsinexecutionspeed
andframerate. Tofurtherimproverobustnesstoincompleteinputs,werandomlydroptheembodiment,
speed,andfpsfieldswithprobability15%duringtraining,encouragingthemodeltogeneralizewhen
promptinformationispartiallyunavailableattesttime.
3.5 In-ContextPolicyAdaptation
Despitethestronggeneralizationenabledbycross-embodimentpretraining,deployingaVLApolicy
toanewrobotorenvironmentoftenrequiresrapidbehavioraladaptationwithoutparameterupdates.
Inspiredbyin-contextlearninginlargelanguagemodels,weequipQWEN-ROBOTMANIPwithanin-
contextpolicyadaptationmechanismthatconditionscurrentactionpredictiononastructuredwindow
ofrecentexecutionhistory(observation-actionpairs)fromthesameepisode,enablingthepolicytoadapt
itsbehavioratdeploymenttimewithoutanyparameterupdateortask-specificfine-tuning.
Executioncontextrepresentation. Akeydesignquestioniswhatinformationconstitutesausefulpolicy
context. Wedrawadirectanalogyfromthemodel’sowninferenceprocedure. Ateachdecisionstep,
QWEN-ROBOTMANIPobservesthecurrentvisualobservationsandproprioceptivestateandpredictsa
completeactionchunkofKsteps. Wethereforedefineonecontextchunkasexactlythistriplet(o ,s ,a ),
h h h
consistingofthevisualobservation,proprioceptivestate,andtheK-stepactionsequenceexecutedduring
chunkh. Thisrecordswhattherobotsaw,wasin,anddid. AcontextofHsuchchunksthusprovidesthe
policywithastructuredwindowofrecentbehavioritcandirectlyreasonabout.
Thetwomodalitieswithineachcontextchunkareprocessedthroughcomplementarypathways,owing
totheirfundamentallydifferentrepresentationalstructures. Historicalframeso areprependedtothe
h
currentframeandprocessedjointlybytheVLMvisualencoderwithinasingleforwardpass,withan
image-countannotationappendedtothelanguageinstructiontohelptheVLMattributeeachvisualtoken
toitscorrecttemporalposition. Proprioceptivestatesandactionchunks,whichcannotbeprocessedby
thevisualpathway,areprojectedintotheVLMhiddenspacebytwolightweightMLPencoders. Thestate
encoderMLP andactionencoderMLP produceper-chunktokenrepresentationswithlearnedtemporal
s a
positionembeddingse temp todistinguishchunksandslotembeddingseslot todistinguishactiontokens
h 0:K′
13

withineachchunk:
ts
h
=MLP
s
(s
h
)+e t
h
emp ∈ RD vlm, (7)
(cid:2) t
h
a,0,...,t
h
a,K′−1(cid:3) =reshape(MLP
a
(flatten(a
h
)))+e t
h
emp+es
0
l
:
o
K
t
′
∈ RK′×D vlm. (8)
AllHchunksareserializedchronologicallyintoasinglecontexttokensequence:
C = (cid:2) ts, ta,0:K′ , ts, ta,0:K′ , ..., ts , ta,0:K′(cid:3) ∈ RH(1+K′)×D vlm. (9)
0 0 1 1 H−1 H−1
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
chunk0 chunk1 chunkH−1
Thecurrentstates isnotencodedhereandcontinuestoflowthroughtheactionhead’sdedicatedstate
t
encoderunchanged,preservingfullbackwardcompatibilitywiththebaseQWEN-ROBOTMANIPmodel.
Historyintegration. Westudytwostrategiesforinjectingcontexttokensequenceintothepolicy. Inthe
unifiedmode,contexttokensCareappendedtotheendoftheVLMinputsequenceandprocessedjointly
withvisualandlanguagetokensundercausalself-attention,allowingtheVLMtoreasonoverhistory,
taskdescription,andvisualobservationstogether. Theresultinghistory-fusedlast-layerhiddenstates
arepassedtotheDiTactionheadviacross-attention. Inthedualmode,thestate-actioncontextisinjected
directlyintotheDiTactionheadratherthantheVLM,keepingtheVLMcontextlengthunchangedat
thecostofshallowerhistoryintegration. UnifiedinjectionallowstheVLM’sfullself-attentiontojointly
reasonoverbehavioralhistory,taskdescription,andvisualobservations,enablingrichercross-modal
contextintegrationthanispossiblewhenhistoryisconfinedtotheactionheadalone. Wethereforeadopt
unifiedinjectionasthedefaultconfiguration.
Stochasticcontextsampling. AnaivestrategyofalwaysprovidingtheHmostrecentchunksleadstoa
degenerateshortcut. Becausethelastcontextchunkistemporallyclosesttothecurrentstep,themodel
canachievelowtraininglossbysimplycopyingthemostrecentactionchunkratherthangenuinely
reasoningabouttheepisode’sbehavioraldynamics. Thiscollapsesthecontextmechanismintoatrivial
action-copyheuristic,whichbreaksdownwhenevertheimmediatehistoryisambiguous,atypical,or
doesnotreflecttherobot’sbroaderexecutionstyle. Whatwewantthemodeltolearnisthebehavioral
profileofthecurrentepisode(Huangetal.,2025),itsvelocitypatterns,graspingstrategies,andinteraction
signatures,notashortcutbasedontemporalproximity. Topreventthis,weintroducestochasticcontext
samplingduringtraining. RatherthanalwayssupplyingtheHchunksimmediatelyprecedingthecurrent
step,thecontextwindowisdrawnfromarandompositionwithintheepisode. Thesampledchunks
maythereforebetemporallydistantfromthecurrentstep,forcingthemodeltoreasonabouttherobot’s
behavioralprofileacrossthefullepisoderatherthanexploitingrecencyasashortcut.
This randomization serves as a form of curriculum diversification. The model must learn to extract
consistentbehavioralstylefromanysubsetoftheepisodehistory,makingitrobusttomissing,partial,
ortemporallydisplacedcontextatinferencetime. Atdeployment,wesupplyarollingwindowofthe
mostrecentHchunksascontext,allowingthemodeltoleveragethefullavailablehistory. Empirically,
stochasticcontextsamplingprovescriticalforpreventingthiscollapse. Withoutit,thepolicyachieves
lowtraininglossbutpoortasksuccess,aclearsignthatthemodelhaslearnedtocopyrecentactions
ratherthanreasonaboutexecutioncontext. Withit,themodelgenuinelyexhibitsin-contextadaptation,
adjustingitsbehaviorbasedonthebroaderbehavioraldynamicsofthecurrentepisode.
4 Training
4.1 Pre-trainingRecipe
4.1.1 Dual-StreamCo-Training
WetrainQWEN-ROBOTMANIPontwocomplementarydatastreamssimultaneously. TheVLAstreamis
builtfromthefullmulti-sourcemanipulationcorpusdescribedinSection2,comprisingreal-robotdemon-
strations,egocentrichuman-handmanipulationvideos,andhuman-to-robotsynthesizedtrajectories.
TheVLMstreamconsistsoflarge-scalevision-languagesupervisiondata(§§2.5),co-trainedalongsidethe
VLAstreamtopreventthepre-trainedperceptualandlanguagecapabilitiesfromdegradingunderaction
predictionoptimization,whichwoulddirectlyweakenthemodel’sabilitytointerpretnovelinstructions
andgeneralizetounseenvisualcontexts(Driessetal.,2025). Inpractice,weadopta9:1ratioofrobot
datatoVLdata.
14

4.1.2 TrainingObjectives
Flow matching loss. For each VLA sample, we are given a ground-truth action chunk a ∈ RT×D.
Followingtheflow-matchingformulation,weconstructanoisyinterpolant
x = (1−t)ϵ+ta,
t
whereϵ ∼ N(0,I)andt ∼Beta(1,1.5). Theactionexpertistrainedtopredictthecorrespondingvelocity
fieldv = a−ϵ,minimizing:
L =E ∥f (x , t, s, o)−(a−ϵ)∥2 , (10)
FM a,ϵ,t θ t 2
where f denotes the full model conditioned on the proprioceptive state s and the visual-language
θ
observationo. GradientsfromL areappliedtoboththeVLMbackboneandtheactionexpert.
FM
Becausedifferentrobotembodimentspopulatedifferentsubsetsofthe80-dimensionalcanonicalaction
space(§§3.2),weapplyacomposedbinarymaskm ∈ {0,1}T×D thatrestrictstheobjectivetoonlythe
dimensionsandtimestepscarryingvalidsupervision.Themaskisconstructedfromthreecomplementary
sources. Theper-dimensionslotmaskidentifiesactivelypopulateddimensionsforthecurrentembodiment.
Forinstance,asingle-armgripperpopulatesthejoint,end-effector,andgripperfieldsofonearmwhile
leavingtheoppositearmandhandslotsaszeros. Thestepvaliditymaskexcludestimestepsflaggedas
anomalousbythedatacurationpipeline(§§2.4)oroutsideepisodeboundaries,withallsubsequentsteps
alsomaskedonceanystepisdeemedinvalidtopreservecausalconsistency. Foregocentrichumandata,
aper-handvaliditymaskzerosoutanentirearmslotfromthemomentthecorrespondinghandexitsthe
cameraview,preventingthemodelfrombeingtrainedonoccludedhandtrajectories. Thethreemasks
areAND-combined,andthemaskedflowmatchinglossbecomesaper-sampleaverageovervalidentries
only:
1 ∑ B ∑ t,j m i,t,j (cid:0) f θ (x i,t , t i , s i , o i ) j −v i,t,j (cid:1)2
L = , (11)
FM B ∑ m
i=1 t,j i,t,j
whereBisthebatchsizeandsubscriptst,jindexthetimestepanddimension. Thisformulationensures
thateverysampleinthebatchcontributesequallytothegradientregardlessofhowmanydimensions
areactive,preventingembodimentswithmorepopulatedslotsfromdominatingoptimization.
VLM next-token prediction loss. For each VLM sample, the backbone is trained with the standard
autoregressivenext-tokenpredictionobjective:
L
VLM
=
−E∑
logp
ϕ
(y
i
| y<i , c), (12)
i
wherey isthetargetresponsetokenatpositioni,andcistheinputcontext,whichmaybetext-onlyor
i
aninterleavedsequenceofimagesandtext. Theoverallobjectiveis
L = L +λL , (13)
FM VLM
whereλcontrolstherelativeweightofthetwolosses. Wesetλ =0.1sothatVLMsupervisionprovides
stabilizingregularizationwithoutovershadowingactionlearning. Separatelearningratesareusedfor
thebackboneandtheactionexperttoaccountfortheirdifferentinitializationscales. Toamortizethe
costoftheVLMforwardpass,theactionexpertperformsK =8repeateddiffusionstepspertraining
repeat
sample,drawing8independentnoisesamplesandtimestepsforthesameactionchunk,andsubstantially
improvingtrainingefficiencywithoutincreasingdataconsumption.
4.2 Post-TrainingRecipe
4.2.1 Domain-specificSupervisedFine-tuning
Oncethefoundationmodelhasbeenpre-trainedonthefullheterogeneouscorpus,weadaptittospecific
deploymentscenariosthroughsupervisedfine-tuning(SFT).Ratherthantrainingspecialistpoliciesfor
individualtasks,weadoptageneralistSFTparadigm. Foreachbenchmarkorreal-worlddeployment
scenario,allavailabledemonstrationdataiscombinedintoasingletrainingset,producingoneunified
fine-tunedmodelthatcanexecuteeverytaskwithinthetargetdomain.
Compared with pre-training, SFT differs in several aspects. First, the SFT procedure only optimizes
theflowmatchingobjective L ofeq.(11)withouttheVLMnext-tokenpredictionloss. Wedisable
FM
themulti-stagedatacurationfilteringof§§2.4andtrainonthecompleteunfiltereddata, preserving
everyvaliddemonstrationforpost-training. Weapplycolorjitteraugmentationtotheinputimages. In
addition,withthemodelinitializedfromapre-trainedcheckpoint,SFTisconductedonfewerGPUswith
fewertrainingstepsthanpre-training.
15

4.2.2 Co-TraininginPost-Training
Domain-specificSFThasbecomeanimportantprotocolforquantitativelyevaluatingthequalityofapre-
trainedVLAmodel. Astrongpre-trainedmodelisexpectedtoadaptefficientlytoatargetdomainafter
fine-tuningonthebenchmarktrainingset. However,thisevaluationprotocolcanalsoexposeacritical
failuremode. Afterextensivebenchmark-specificSFT,aVLAmodelmayimprovetaskperformance
by exploiting repeated visual and task patterns in the benchmark, while becoming less sensitive to
thelanguageinstruction. Inthiscase,thepolicyisnolongerstronglyconditionedonbothvisionand
language. Instead,itbehavesmorelikeavision-actionpatternmatcher. Werefertothisphenomenonas
VLA-to-VAdegradation.
Thisdegradationstemsfromthreecompoundingfactors. First,domain-specificSFTdatasetsarelimited
indiversitywithconcentratedvisuallayoutsandinstructionexpressions,makingshortcutcorrelations
betweenscenepatternsandactionseasytolearn. Second,trainingandtestsplitssharesimilarvisual
patterns, allowing high benchmark scores to be achieved through pattern memorization rather than
genuinelanguagegrounding. Asaresult,suchbenchmarksoverestimateinstruction-followingability
andfailtodistinguishtruelanguage-conditionedcontrolfrombenchmark-patternoverfitting. Third,
modelswithoutstrongcompositionalgroundingabilitytendtotreatlanguageasaweakcontextsignal
duringSFT,withactionsincreasinglydominatedbyvisualshortcutslearnedfromthebenchmarkdata.
To mitigate this risk, we propose a mixed post-training strategy as an optional enhancement to the
standarddomainSFTdescribedin§§4.2.1: ratherthanfine-tuningsolelyonthebenchmarktraining
set, the model is co-trained with a subset of pre-training data filtered by distributional proximity to
thetargetdomain. Thisprovidesbroaderadaptationsignalswhilepreservingthebasemodel’srobust
executioncapabilities,withoutintroducingunrelateddatathatmightdilutedomain-specificlearning. In
ourmainexperiments,wefollowthestandarddomain-specificSFTprotocoltoensurefaircomparison
withbaselines;themixedpost-trainingstrategyisvalidatedasanadditionalenhancementin§§6.5.1.
Todirectlyevaluatewhetherthelanguage-followingcapabilityispreserved,weconstructanewbench-
mark,RoboTwin-IF(InstructionFollowing),basedonRoboTwin2.0(Chenetal.,2025b). Thebenchmark
examineswhetherthemodelperformstheinstructedactioninthesameorsimilarvisualsceneswith
differentinstructions,ratherthanrelyingonvisualpatternmatchingtoselectadefaultbehavior. The
detailedbenchmarkdesignispresentedin§§6.2.1.
5 Deployment
In our deployment setup, inference is performed on a remote server with observations and actions
transmittedbetweentherobotandtheserveroveraWiFiconnection. Tomitigatethelatencyintroduced
bycloud-basedinferenceandnetworktransmission,weadoptReal-TimeChunking(RTC)(Blacketal.,
2026),whichasynchronouslygeneratesthenextactionchunkwhiletherobotexecutesthecurrentone,
effectivelyhidingtheround-triplatencyandenablingsmoothreal-timecontrol.
6 Experiments
6.1 AreStandardBenchmarksEnough?
We evaluate QWEN-ROBOTMANIP on robotic manipulation benchmarks that span a diverse range
of embodiments and task types, and compare against several recent VLA models (Black et al., 2024;
Bjorck et al., 2025; Community, 2026; Black et al., 2025). We begin with LIBERO (Liu et al., 2023)
andRoboTwin(Muetal.,2025), twostandardbenchmarksthatarewidelyusedforVLAevaluation.
LIBERO(Liuetal.,2023)comprisesfoursingle-armtabletopmanipulationsuitesacross130combinations
oftasksandscenes. RoboTwin(Muetal.,2025)presents50dual-armmanipulationtasksineasyand
hardmodes,requiringadaptationtovariedbackgrounds,objects,andspatiallayouts.
Figure4(left)reportstheresults. Anotablepatternisthatmodelstrainedfromscratch—StarVLAand
Ours-scratch—attaincompetitiveorevensuperiorresultscomparedtowell-pretrainedmodelssuchas
π andAbot-M0onLIBEROandRoboTwin,despitelackinglarge-scaleroboticpretraining. Thisisnot
0.5
acoincidencebutastructuralpropertyofthesebenchmarks. Becausetrainingandevaluationdataare
drawnfromthesameenvironmentandtaskdistributions,highsuccessratescanbeachievedthrough
in-distributionpatternmatchingalone. Modelsthatlackgenuinegeneralizationcanperformwellsimply
bymemorizingrecurringvisualandbehavioralpatterns,andthebenchmarkcannotdistinguishthisfrom
realcapability. Priorworkhasfurthershownthatfine-tuningapretrainedVLAonabenchmark’sown
trainingsplityieldsperformancecomparabletotrainingfromscratch(Yanetal.,2025),confirmingthat
16

|          | Standard Benchmarks |     |     |                              | OOD Benchmarks |     |
| -------- | ------------------- | --- | --- | ---------------------------- | -------------- | --- |
| 100      |                     |     | 95  | 90                           |                |     |
| 98.6     |                     |     |     |                              | 47.9           | 50  |
| 98.098.2 |                     |     |     | )%( etaR sseccuS sulP-OREBIL |                |     |
)%( etaR sseccuS OREBIL 98 97.6 88.7 90 )%( etaR sseccuS niwToboR )%( etaR sseccuS niwToboR
|     |           | 88.4 |     | 85  | 84.4 |     |
| --- | --------- | ---- | --- | --- | ---- | --- |
|     |           | 87.3 |     |     |      | 40  |
|     | 85.7 86.1 |      |     |     | 36.0 |     |
85.1
| 96  |      |     | 85  |     | 80.5 |     |
| --- | ---- | --- | --- | --- | ---- | --- |
|     | 82.7 |     |     |     |      | 30  |
80
78.3 22.6
| 94  |     |     | 80  |     |     | 20  |
| --- | --- | --- | --- | --- | --- | --- |
76.8
75 74.1
| 92  |     |     | 75  |     | 10.6 |     |
| --- | --- | --- | --- | --- | ---- | --- |
10
| 90     |                |               | 70  | 70          |          | 0   |
| ------ | -------------- | ------------- | --- | ----------- | -------- | --- |
| LIBERO | RoboTwin Clean | RoboTwin Rand |     | LIBERO-Plus | RoboTwin |     |
Clean2Rand
|     |     | StarVLA 0.5          | w/o robot data pretrain |     |     |     |
| --- | --- | -------------------- | ----------------------- | --- | --- | --- |
|     |     | Ours-scratch Abot-M0 | w/ robot data pretrain  |     |     |     |
Figure4: Standardin-distributionbenchmarkscannotrevealwhetheramodelbenefitsfromlarge-
scalerobotdatapretraining. Left: onin-distributionbenchmarks(LIBERO,RoboTwin),modelswithout
large-scalerobotpretraining(dashedborders)matchorexceedpretrainedones. Right: onOODbench-
marks(LIBERO-Plus,RoboTwin-Clean2Rand),aclearseparationemerges—pretrainingprovidesgenuine
generalizationthattraining-from-scratchcannotreplicate.
thepretrainedpriorcontributesnegligibletransferablevalueunderin-domainevaluation.
Figure4(right)tellsadifferentstory. OnOODbenchmarks—LIBERO-PlusandRoboTwin-Clean2Rand—
whereevaluationconditionsdivergefromtraining,aclearseparationemerges: π 0.5 substantiallyoutper-
formsStarVLAandOurs-scratch,withthegapwideningasperturbationseverityincreases. StarVLA
collapses from 85.7% (RoboTwin Easy, IID) to 10.6% (RoboTwin-Clean2Rand, OOD). This confirms
thatOODevaluationisthecorrectnorthstarformeasuringfoundationmodelquality: itrevealsthe
transferablestructurethatpretrainingprovidesandthatin-domainmetricssystematicallyfailtocapture.
Thewaypractitionersactuallyuseafoundationmodelreinforcesthisconclusion.Aresearcherorengineer
deployingaVLAmodeldoesnothaveaccesstothesamedistributionoftasks,objects,andenvironments
presentinanybenchmark. Theyhaveahandfulofdemonstrationscollectedontheirownhardware,in
theirownworkspace,fortheirowntask. Whatdetermineswhetherthefoundationmodelhelpsthemis
notitsin-domainbenchmarkrankbuthowmuchgeneralizablestructureithasinternalized,andhow
efficientlythatstructuretransfersunderminimalfine-tuningonunfamiliardata. Thefollowingsection
thereforeadoptsOODevaluationastheprimarymeasureandreportscomprehensivebenchmarking
resultsforQWEN-ROBOTMANIPacrossbothin-distributionandout-of-distributionsettings.
6.2 GeneralizationCapabilities
The following sections evaluate QWEN-ROBOTMANIP on a suite of out-of-distribution settings that
directlymeasurethegeneralizationcapabilitiesafoundationmodelisexpectedtoprovide. Weorga-
nize these evaluations around three axes (Figure 5): task and scene generalization under controlled
perturbations,instructionfollowingwithnovellanguageandtasks,andzero-shotcross-embodiment
transfer.
6.2.1 EvaluationProtocol
TaskandSceneGeneralization. WeevaluaterobustnessofVLAmodelstovisualandphysicalchanges
onfourbenchmarks. LIBERO-Plus(Feietal.,2025)introducescontrolledperturbationsalongseven
orthogonaldimensionsontopoftheoriginalLIBERObenchmark—backgroundtextures,cameraview-
points,languageinstructions,lightingconditions,objectlayouts,robotinitialstates,andsensornoise—
withmodelsfine-tunedonthestandardLIBEROtrainingsetandevaluatedundereachperturbation.
RoboTwin-Clean2RandconstructsanOODevaluationprotocolontopofRoboTwin(Muetal.,2025): all
modelsarefine-tunedexclusivelyonaCleandatasetwithfixedwhitebackground,defaultlighting,no
distractors,andafixedtableheight,thenevaluatedundercontrolledrandomizationsalongindividual
axes(background,lighting,clutter,tableheight)aswellasaHardsettingthatappliesallrandomiza-
tionssimultaneously. RoboCasa365(Nasirianyetal.,2026)providesalarge-scalekitchenmanipulation
benchmarkwiththreeevaluationsuitesofincreasingdifficulty: Atomic(18basicmanipulationskills
withdiverseobjectandlayoutvariations),Composite-Seen(multi-steplong-horizontasksseenduring
17

LIBERO & LIBERO-Plus
RoboChallenge (UR & Franka)
EBench
RoboChallenge (AgileX & ARX)
RoboTwin & Robotwin-IF (newly proposed)& RoboTwin-XE (newly proposed)
Qwen Real-World Evaluation (AgileX & ARX)
RoboCasa365
Figure5: EvaluationsettingsforQWEN-ROBOTMANIP,spanning500+simulationtasksacrossLIBERO,
LIBERO-Plus,EBench,RoboTwin,RoboTwin-IF,RoboTwin-XE,andRoboCasa365,and80+real-world
tasksacross4embodimentsincludingUR,Franka,AgileX(ALOHA),andARX.
training),andComposite-Unseen(long-horizontasksabsentfromthetrainingset). EBench(Laboratory,
2026)isanindoormobilemanipulationbenchmarkbuiltonNVIDIAIsaacSim,spanning26tasktypes
and794evaluationinstances. Thebenchmarkevaluatesgeneralizationalongperturbationdimensions:
background, instruction, object, and a mixed setting that combines all perturbations, reporting both
successrateandaprocessscoreforeach.
InstructionFollowing. ExistingOODbenchmarksprimarilyproberobustnesstovisualandphysical
perturbations,whileleavinggeneralizationtounseenlanguageinstructionslargelyuntested. Wedevelop
RoboTwin-IF(InstructionFollowing),abenchmarkbuiltonRoboTwin(Muetal.,2025)thatsystematically
evaluatesinstruction-followingcapabilitiesacrossfivetasksuites,eachtargetingadistinctdimensionof
languagegrounding:
• Pick-Diverse-Object: Four objects are randomly sampled from a pool of 12 everyday items. The
instructionnamesoneobjectbycolorandnoun. Therobotmustidentifyandliftthecorrecttarget
amongthreedistractors,testingtarget-objectgrounding.
• Place-Relative: Two named objects and 1–3 distractors are on the table. The instruction specifies
pickingupobjectAandplacingitinaspatialrelation(“beside”or“ontopof”)withrespecttoobjectB,
testingspatial-relationunderstanding.
• Operate-Mic-Drawer: A microphone and a cabinet with a functional drawer are present. The in-
structionspecifiesamulti-stepbimanualsequence: openthedrawerwithonearm,thenpickupthe
microphone with the other arm and place it inside. Some instructions further specify which arm
performswhichsub-task,testingmulti-stepsequencingandbimanualcoordination.
• Operate-Stapler:Astapler,acoloredpad,and1–2distractorsareonthetable. Theinstructionspecifies
eitherpressingthestaplerormovingitontothecoloredpad. Thepadisalwayspresentregardlessof
theverb,actingasadistractorinpressepisodesandastheplacementtargetinmoveepisodes,testing
verbdiscriminationwithsharedsceneelements.
• Operate-Tabletop: A bell, a stapler, and 1–2 pickable objects are all present simultaneously. The
instructionspecifiesoneofthreeactions: ringthebell,pressthestapler,orpickupanamedobject.
Onlyoneactioniscorrect;theotherinteractiveobjectsaredistractors,testingthree-wayverb-and-target
discriminationinamulti-affordancescene.
Allmodelsarefine-tunedexclusivelyonRoboTwinClean. Eachsuiteusesatwo-tierlanguagediversity
system: “seen”instructiontemplates(usedduringtrainingdatacollection)and“unseen”templates(held
outforevaluation),combinedwithper-objectdescriptionvariantsthatfurtherdiversifynounphrases.
Atevaluationtime,eachepisodeispairedwithaheld-outunseeninstructiontemplate,ensuringzero
18

Operate-Tabletop Three-way verb-and-target discrimination
1. Touchthebellwithraisedroundtopwiththeleftarm
Operate-Stapler Verb discrimination with shared scene elements
1. Usetherightarmtoshiftthebluestaplerforholdingpapersto
thecyanpad
Ringbell
Move stapler
2. Pushontherectangularstaplerwithcurvedcorners onto pad
2. Applypressuretotheplasticstaplerwiththerightarm
Press stapler
3. Collectthelightbrowncoffeebox
Press stapler
in place
Pick target
object
RoboTwin-IF: Instruction following requires choosing the correct action among multiple plausible alternatives in the same scene.
We evaluate language grounding through target-object grounding, verb discrimination, and action selection under shared visual contexts.
Figure 6: Representative task suites from RoboTwin-IF. Operate-Tabletop (left) requires three-way
verb-and-targetdiscriminationwhereabell,stapler,andpickableobjectsareallpresentandonlythe
instruction-specifiedactioniscorrect. Operate-Stapler(right)requiresverbdiscriminationundershared
visualcontext,wherethecoloredpadandstaplerarealwayspresentregardlessoftheinstructedverb.
Bothsuitesareevaluatedonunseeninstructiontemplatesheldoutfromtraining.
overlapwiththetrainingdistribution.
Cross-EmbodimentGeneralization. Camera-framerelativeEEFactionsexpressdeltasinthecamera
coordinateframeratherthanarobot-specificjointspace,enablingasinglepolicytopotentiallycontrol
morphologicallydistinctrobotswithoutre-training. WedevelopRoboTwin-XE,abenchmarkbasedon
RoboTwinthatevaluateszero-shottransfertounseenrobotembodiments. Themodelisfine-tunedon
theRoboTwinCleandatasetandtestedundertheRoboTwinHardsetting,replacingthedefaultAgileX
platformwithARX-X5,UR5-WSG,andFrankaPanda. InitialEEFposesarealignedviaIK,headandwrist
cameraextrinsicsarekeptidentical,andtaskscenes,objectlayouts,andperturbationseedsareshared
across embodiments. The model must therefore generalize across two types of embodiment-specific
differences: thevisualappearanceoftherobotarmincameraobservations,andkinematicdifferences
(DOFcount,jointarrangement,linklengths,andworkspacegeometry)thataffectreachabilityandmotion
dynamics. Themodelisfine-tunedexclusivelyonAgileXdemonstrations;notarget-embodimentdatais
used.
6.2.2 SummaryofResults
Onstandardin-distributionbenchmarks,QWEN-ROBOTMANIPachievesstate-of-the-artorcompetitive
performance(Table3)onLIBERO(99.2%)andRoboTwinEasy/Hard(93.7%/94.0%). However,asargued
in§§6.1,thesemetricsdonotreliablydistinguishgenuinegeneralizationfromin-distributionpattern
matching. WethereforefocusonOODevaluationastheprimarymeasureofroboticfoundationmodel
capabilities.
Figure7summarizesresultsacrossbenchmarksevaluatedunderOODsettings,whereQWEN-ROBOTMANIP
consistentlyoutperformspriorstate-of-the-artmodelsbyasubstantialmargin. QWEN-ROBOTMANIP
outperformsπ onallbenchmarksevaluated,withthegapwideningastheevaluationbecomesmore
0.5
challenging.
Ontaskandscenegeneralization,QWEN-ROBOTMANIPsurpassesπ
0.5
by7.0pointsonLIBERO-Plus
(91.4vs.84.4),by21.5pointsonthemostdemandingRoboTwin-C2RHardsetting(69.4vs.47.9),andby
18.5pointsonEBench(45.6vs.27.1). OnRoboCasa365,theadvantagereaches19.0points(35.9vs.16.9).
Oninstructionfollowing,QWEN-ROBOTMANIPscores72.2%onRoboTwin-IFagainst49.6%forπ
0.5
—a
largeimprovementof22.6points. Thisresultisparticularlysignificantbecauseinstructionfollowingis
thecapabilitymostpronetodegradationduringVLAtraining: fine-tuningaVLMonactionprediction
canerodethelanguageconditioningpathway,causingthepolicytocollapseintoavisually-triggered
19

Table3: In-distributionbenchmarkresults. QWEN-ROBOTMANIPmatchesorexceedspriorstate-of-the-
artacrossallstandardbenchmarks.
|     |                     |     |     | LIBERO | RoboTwin-Easy |      | RoboTwin-Hard |      |
| --- | ------------------- | --- | --- | ------ | ------------- | ---- | ------------- | ---- |
|     | π (Blacketal.,2024) |     |     | 94.4   |               | 65.9 |               | 58.4 |
0
|     | π (Blacketal.,2025) |     |     | 97.6 |     | 82.7 |     | 76.8 |
| --- | ------------------- | --- | --- | ---- | --- | ---- | --- | ---- |
0.5
|     | StarVLA(Community,2026)    |     |     | 98.0 |     | 85.7 |     | 87.3 |
| --- | -------------------------- | --- | --- | ---- | --- | ---- | --- | ---- |
|     | Abot-M0(Yangetal.,2026)    |     |     | 98.6 |     | 86.1 |     | 85.1 |
|     | Being-H0.7(Luoetal.,2026c) |     |     | 99.2 |     | 90.2 |     | 89.6 |
|     | QWEN-ROBOTMANIP-scratch    |     |     | 98.2 |     | 88.7 |     | 88.4 |
|     | QWEN-ROBOTMANIP            |     |     | 99.1 |     | 93.4 |     | 92.5 |
|     | QWEN-ROBOTMANIP-Context    |     |     | 99.2 |     | 93.7 |     | 94.0 |
(a) Task & Scene Generalization (b) Instruction Following (c) Cross-Embodiment Transfer
100
1.08×
100
|     |     |     | 91.4 | 1.80× |     |     | 50 3.73× |     |
| --- | --- | --- | ---- | ----- | --- | --- | -------- | --- |
1.30×
|     |       |     | 84.8 |     | 79 3.55× |     |     | 42.9 |
| --- | ----- | --- | ---- | --- | -------- | --- | --- | ---- |
|     |       |     |      | 80  |          | 75  |     |      |
| 80  | 1.45× |     |      |     | 71       |     |     |      |
40
)%( etaR sseccuS 69.4
|     |     |     |     | 60  |     | 57.7 |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- |
60
|     | 1.68× |      |     |     |     |     | 30  | 2.28× |
| --- | ----- | ---- | --- | --- | --- | --- | --- | ----- |
|     | 47.9  | 45.6 |     | 44  |     |     |     | 22.8  |
40
| 40  |     |     |     |     |     |     | 20  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
27.1
|     |     | 2.7 | 6×    |     | 20  |     | 11.5 |          |
| --- | --- | --- | ----- | --- | --- | --- | ---- | -------- |
|     |     |     |       | 20  |     |     |      | 10 5.36× |
| 20  |     |     | 1 4.9 |     |     |     | 10   |          |
5.9
5.4
1.1
| 0   |     |     |     | 0   |     |     | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
RT-C2R EBench RoboCasa LIBERO Pick Place Operate ARX-X5 UR5-WSG Franka
|     | (Hard) | 365-Unseen | Plus | Diverse    | Relative        | (avg) |     |     |
| --- | ------ | ---------- | ---- | ---------- | --------------- | ----- | --- | --- |
|     |        |            |      | Prev. SOTA | Qwen-RobotManip |       |     |     |
Figure7: OODgeneralizationsummary. QWEN-ROBOTMANIPvs.previousstate-of-the-artVLAmodel
across three generalization axes. (a) Task and scene generalization under controlled perturbations.
(b)Instructionfollowingwithheld-outlanguagetemplates. (c)Zero-shotcross-embodimenttransfer.
QWEN-ROBOTMANIPoutperformspreviousmodelsoneveryOODbenchmark,withthegapwidening
onhardersettings.
defaultbehaviorthatignorestheinstructionentirely(Section4). Thefactthat QWEN-ROBOTMANIP
maintains strong instruction following across all five RoboTwin-IF suites—including tasks requiring
target-objectgrounding,spatial-relationunderstanding,andmulti-wayverbdiscrimination—indicates
thatthedual-streamco-trainingstrategyandthediversityofthepretrainingcorpustogetherpreserve
genuinelanguage-conditionedcontrol.
Themostrevealingcomparisoniscross-embodimenttransferonRoboTwin-XE.Whenbothmodelsare
trainedexclusivelyondemonstrationscollectedontheAgileXALOHAplatformandevaluatedzero-shot
onunseenrobots,QWEN-ROBOTMANIPachieves23.9%usingcamera-frameEEFactions—3.2×the7.5%
achievedbyπ 0.5 . Thisgapvalidatesourcamera-framealignmentstrategyforactionrepresentation: by
expressingactionsinthevisualdomain,physicallysimilarmotionsbecomenumericallyproximateacross
morphologicallydistinctrobots,enablingeffectivecross-embodimenttransfer.
Acomplementarysignalcomesfromthecomparisonwithmodelstrainedfromscratch. OnLIBERO-Plus,
QWEN-ROBOTMANIP-scratchscores78.3versusQWEN-ROBOTMANIP’s89.0andQWEN-ROBOTMANIP-
Context’s91.4.ThegapisevenmorepronouncedonRoboTwin-C2R,whereQWEN-ROBOTMANIP-scratch
collapsesfrom71.6(Easy)to22.6(Hard),retainingabout30%ofitsEasyperformance,while QWEN-
ROBOTMANIPdegradesfarmoregracefullyfrom73.2to62.6,retainingroughly86%(comparedto66%for
π 0.5 ). Aconsistentpatternemergesacrossbenchmarks. ThepretrainedVLMbackbonealreadyprovides
robustnesstosomeofthevisualandlinguisticvariationssuchasbackground,lighting,andlanguage
perturbations. However,thecapabilitiesthatdistinguishgenuinegeneralizationfromin-distribution
memorization,includingspatialreasoningundernovelviewpoints,robustnesstounseenrobotstates,and
attentiontotask-relevantobjectsinclutteredscenes,specificallyrequirethelarge-scalecross-embodiment
pretrainingthatQWEN-ROBOTMANIPprovides.
20

Table4: Out-of-distributionrobustnessevaluationonLIBERO-Plusacrosssevenperturbationdimen-
sions.
|                     | Camera | Robot Language | Light Background | Noise | Layout Total |
| ------------------- | ------ | -------------- | ---------------- | ----- | ------------ |
| π (Blacketal.,2024) | 13.8   | 6.0 58.8       | 85.0 81.4        | 79.0  | 68.9 53.6    |
0
| π (Blacketal.,2025) | 78.4 | 73.6 80.8 | 96.2 94.1 | 89.0 | 84.5 84.4 |
| ------------------- | ---- | --------- | --------- | ---- | --------- |
0.5
StarVLA(Community,2026) 52.5 49.8 88.5 95.7 95.7 73.0 76.9 74.1
Abot-M0(Yangetal.,2026) 60.4 67.9 86.4 96.2 91.6 86.4 82.6 80.5
Cosmos-Policy(Kimetal.,2026b) 75.8 63.3 81.7 96.5 88.9 92.7 82.2 82.2
Being-H0.7(Luoetal.,2026c) 82.0 59.0 82.8 97.8 90.0 93.5 88.5 84.8
QWEN-ROBOTMANIP-scratch 70.4 44.9 88.1 95.8 95.5 84.4 79.1 78.3
| QWEN-ROBOTMANIP | 87.2 | 75.5 85.6 | 96.6 97.7 | 97.7 | 87.3 89.0 |
| --------------- | ---- | --------- | --------- | ---- | --------- |
QWEN-ROBOTMANIP-Context 89.9 83.9 86.5 98.6 99.9 97.9 87.5 91.4
Table5: Out-of-distributionevaluationonRoboTwin-Clean2Rand. Modelsarefine-tunedontheClean
datasetonlyandtestedundervariousenvironmentalrandomizations.
|                              |     | Easy Background | Light Clutter | Height | Hard |
| ---------------------------- | --- | --------------- | ------------- | ------ | ---- |
| StarVLA(Community,2026)      |     | 58.1 27.1       | 50.9 24.2     | 48.4   | 10.6 |
| GR00T-N1.7(Bjorcketal.,2025) |     | 43.6 40.4       | 41.9 27.1     | 39.0   | 20.7 |
| π (Blacketal.,2025)          |     | 73.1 67.0       | 69.2 57.9     | 67.6   | 47.9 |
0.5
| Abot-M0(Yangetal.,2026)        |     | 70.7 56.5 | 68.8 46.0 | 56.3 | 36.0 |
| ------------------------------ | --- | --------- | --------- | ---- | ---- |
| QWEN-ROBOTMANIP-scratch        |     | 71.6 60.6 | 70.7 24.6 | 63.6 | 22.6 |
| QWEN-ROBOTMANIP(joint)         |     | 73.2 74.6 | 68.4 61.3 | 71.0 | 62.6 |
| QWEN-ROBOTMANIP(eef)           |     | 74.0 75.8 | 70.1 59.8 | 69.4 | 60.8 |
| QWEN-ROBOTMANIP-Context(joint) |     | 84.7 82.4 | 84.2 75.4 | 79.5 | 69.4 |
| QWEN-ROBOTMANIP-Context(eef)   |     | 85.0 82.4 | 84.7 66.8 | 82.9 | 64.0 |
6.2.3 DetailedAnalysis
LIBERO-Plus. Table4reportsper-dimensionresults. QWEN-ROBOTMANIPachieves89%andQWEN-
ROBOTMANIP-Contextachieves91.4%overall, surpassingallbaselines. Beyondtheaggregatescore,
theper-dimensionbreakdownrevealswhichcapabilitiesbenefitfromlarge-scalerobotdatapretraining
andwhicharealreadyprovidedbythepretrainedVLMbackbone. Modelswithoutrobotdatapretrain-
ing(StarVLA,QWEN-ROBOTMANIP-scratch)matchmostpretrainedmodelsonLanguage,Light,and
Backgroundperturbations,indicatingthattheVLM’svisualandlinguisticrepresentationsareinherently
robusttothesevariations. Incontrast,thesesamemodelssuffersharpdegradationunderRobotpertur-
bation(49.8%and44.9%vs.75.5%forQWEN-ROBOTMANIP),wherethepolicymustgeneralizeacross
unseeninitialrobotstatesthatlieoutsidetheVLM’spurview. QWEN-ROBOTMANIP-Contextfurther
raisesRobotperturbationrobustnessto83.9%,a+8.4pointgainoverQWEN-ROBOTMANIP,indicating
thatin-contexthistoryprovidesanimplicitkinematicpriorthathelpsthepolicyadapttounfamiliar
initialrobotconfigurationswithintheepisode. Cameraviewpointperturbationexhibitsasimilarpattern
(+34.7and+16.8overthescratchmodels),suggestingthatrobustspatialreasoningundernovelcamera
posesrequiresthegroundingthatVLApretrainingondiverserobotsetupsprovides,ratherthanthe
appearance-levelrobustnessalreadycapturedbytheVLM.
RoboTwin-Clean2Rand. Table5reportsresultsacrossindividualandcompoundperturbationaxes.
QWEN-ROBOTMANIPachievesthehighestsuccessrateontheHardsettingunderbothjoint-spacecontrol
(62.6%)andend-effectorcontrol(60.8%),withbothmodesperformingsimilarlyacrossallperturbation
dimensions. Amongallmethods, QWEN-ROBOTMANIP exhibitsthesmallestdegradationfromEasy
toHard,retainingroughly86%ofitsEasyperformancecomparedto66%forπ 0.5 andabout30%for
modelswithoutrobotdatapretraining. TheClutterperturbationfurtherhighlightsthisgap: QWEN-
ROBOTMANIP-scratchcollapsesfrom71.6%to24.6%whendistractorobjectsareintroduced,suggesting
thattheabilitytoattendtotask-relevantobjectsamidclutterrequireslarge-scaleroboticdatapretraining
ratherthanin-domainfine-tuningalone. Notably,QWEN-ROBOTMANIPscoreshigherunderBackground
randomization(74.6%)thanundertheEasysetting(73.2%),likelybecausediversereal-worldscenesinthe
pretrainingdatamakerandomizedbackgroundsmorein-distributionthantheplainwhitebackgroundof
theEasymode. QWEN-ROBOTMANIP-Contextfurtheramplifiesthesegains,reaching84.7%(Easy)and
69.4%(Hard)underjointcontrol—animprovementof+11.5and+6.8pointsoverQWEN-ROBOTMANIP.
Thissubstantialboostsuggeststhatconditioningonintra-episodeexecutionhistoryprovidescomple-
mentaryrobustnesstovisualperturbations,asthepolicycandynamicallycalibrateitsactionsbasedon
observedoutcomesratherthanrelyingsolelyonthecurrentobservation.
21

Table6: EvaluationonRoboCasa365acrossatomicandlong-horizonmanipulationtasks.
Atomic Composite-Seen Composite-Unseen Total
π (Blacketal.,2024) 36.3 5.2 0.7 15.0
0
π (Blacketal.,2025) 39.6 7.1 1.2 16.9
0.5
GR00T-N1.5(Bjorcketal.,2025) 50.7 14.8 2.7 23.9
GR00T-N1.6(Bjorcketal.,2025) 51.1 9.4 1.7 21.9
RLDX-1(Kimetal.,2026a) 63.0 27.5 5.4 33.2
QWEN-ROBOTMANIP 68.6 20.1 14.9 35.9
QWEN-ROBOTMANIP-Context 63.9 22.6 11.2 33.8
Table 7: Evaluation on EBench across three splits. Each split reports both success rate (SR) and the
EBenchcompositescore(Score).
TableTop SimplePnP LongHorizon Overall
SR Score SR Score SR Score SR Score
π (Blacketal.,2024) 15.7 30 35.0 39 17.0 41 23.6 37
0
π (Blacketal.,2025) 12.9 32 45.0 50 18.1 39 27.1 41
0.5
X-VLA(Zhengetal.,2025) 8.6 24 50.0 54 6.2 25 23.7 36
InternVLA-A1(Caietal.,2026) 4.3 11 43.0 47 17.9 46 23.9 36
QWEN-ROBOTMANIP 50.0 70 56.5 60 29.9 55 45.6 60
QWEN-ROBOTMANIP-Context 49.3 56 55.0 66 26.6 55 43.6 59
50
40
30
20
10
0
)%(
etaR
sseccuS
Operating Mode Horizon Precision
50 50 51 50
44 44
35 35 33 33 36 35 31 31
29 29 29 26 25 24 27 24
18 19
15 14 15 15 15 14
10
9 6 7 5
Mobile Dexterous Long Short Low Medium High
Horizon Horizon Precision Precision Precision
0 0.5 X-VLA InternVLA-A1 Qwen-RobotManip
Figure8: EBenchperformanceacrossoperatingmode,horizon,andprecision.
RoboCasa365. Table6reportsresultsacrossthethreeevaluationsuites. QWEN-ROBOTMANIPachieves
35.9%overall,surpassingthepreviousstate-of-the-artRLDX-1(33.2%). OntheAtomicsuite, QWEN-
ROBOTMANIPachievesthehighestscore(68.6%)amongallmethods,reflectingstronggeneralization
acrossdiversemanipulationprimitives. OnComposite-Unseen—wheretherobotmustcompletelong-
horizontasksinOODscenes—QWEN-ROBOTMANIPachieves14.9%,nearlytriplingthenext-bestresult
(5.4%forRLDX-1),demonstratingsubstantiallystrongerout-of-distributioncompositionalgeneralization.
EBench. Table7andFigure8reporttheresultsonEBench(Laboratory,2026),anIsaacSim-basedindoor
manipulationbenchmarkthatevaluates26tasktypesonadual-armmobileplatform(Lift2+R5a)across
three splits: dexterous tabletop tasks (Table Top), pick-and-place with mobile manipulation (Simple
PnP),andextendedmulti-stepsequences(LongHorizon). QWEN-ROBOTMANIPachieves45.6%overall
successrateandacompositescoreof60,outperformingπ (27.1%/41)andallotherbaselinesbya
0.5
largemarginacrosseverysplit.
Thegainsaremoststrikingonthedexteroussplit. OnTableTop,QWEN-ROBOTMANIPachieves50.0%
SRandascoreof70,nearlyquadruplingπ ’ssuccessrate(12.9%)andmorethandoublingitsscore(32).
0.5
OnSimplePnP,QWEN-ROBOTMANIPleadsat56.5%SRwhilethenext-bestbaselineisX-VLAat50.0%.
OnLongHorizon,whichrequiresmobilemanipulationoverextendedsequences,QWEN-ROBOTMANIP
reaches29.9%SRandascoreof55, improvingover π by+11.8SRand+16score. Figure8further
0.5
breaksdownperformancebyoperatingmode,horizonlength,andprecisionlevel,showingconsistent
22

| 50  |     |     |     |     |     |     | 65  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | 47  |     |     | 62  |     | 61  |     |
|     | 45  | 45  |     | 44  |     |     |     |     |     | 61  |     |     |
| 45  |     |     |     |     |     |     | 60  |     |     |     |     | 59  |
)%( etaR sseccuS
| 40    |      |       |     |     |       |     | 55    |         |     |      |     |       |
| ----- | ---- | ----- | --- | --- | ----- | --- | ----- | ------- | --- | ---- | --- | ----- |
| 35    |      |       |     |     |       |     | erocS | 50      |     |      |     |       |
| 35    |      | 32    |     |     |       |     | 50    |         |     | 47   |     |       |
|       | 3029 | 32 30 |     |     |       |     |       |         |     |      |     |       |
| 30 30 |      |       | 29  |     |       |     | 45    | 44 4342 |     | 4344 |     |       |
|       | 27   |       |     |     |       |     |       |         |     |      | 42  |       |
|       |      |       |     | 26  |       |     |       |         | 40  |      |     | 40    |
| 25    |      |       | 24  |     | 23    |     | 40    |         |     |      |     |       |
|       |      |       |     | 21  |       | 22  |       |         |     |      | 38  |       |
|       |      |       |     |     |       |     |       |         |     |      | 35  | 35    |
| 20    |      |       |     |     | 18 19 |     | 35    |         |     |      |     |       |
|       |      |       |     |     |       |     |       |         |     |      | 31  | 32 32 |
| 15    |      |       |     |     |       |     | 30    |         |     |      |     |       |
Background Instruction Object Mix Background Instruction Object Mix
|     |     |          | 0                                             | 0.5 | X-VLA |     | InternVLA-A1 |     | Qwen-RobotManip |     |     |     |
| --- | --- | -------- | --------------------------------------------- | --- | ----- | --- | ------------ | --- | --------------- | --- | --- | --- |
|     |     | Figure9: | Per-dimensiongeneralizationbreakdownonEBench. |     |       |     |              |     |                 |     |     |     |
Table8: Instruction-followingevaluationonRoboTwin-IF.Modelsarefine-tunedonRoboTwinClean
datasetandevaluatedwithheld-outunseeninstructiontemplates.
|                              |     |     |     | Pick-Diverse |     | Place-Rel. | Ope.-Mic-Dr. |     | Ope.-Stapler |     | Ope.-Table | Average |
| ---------------------------- | --- | --- | --- | ------------ | --- | ---------- | ------------ | --- | ------------ | --- | ---------- | ------- |
| StarVLA(Community,2026)      |     |     |     | 11           |     | 13         |              | 0   |              | 49  | 74         | 29.4    |
| GR00T-N1.7(Bjorcketal.,2025) |     |     |     | 20           |     | 17         |              | 0   |              | 14  | 32         | 16.6    |
| π (Blacketal.,2025)          |     |     |     | 44           |     | 20         |              | 15  |              | 92  | 66         | 49.6    |
0.5
| QWEN-ROBOTMANIP         |     |     |     | 79  |     | 57  |     | 42  |     | 90  | 93  | 72.2 |
| ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
| QWEN-ROBOTMANIP-Context |     |     |     | 77  |     | 71  |     | 33  |     | 89  | 90  | 72.0 |
advantagesacrossallsevendimensions.
The per-dimension generalization breakdown (Figure 9) further confirms robustness to distribution
shift. As perturbation complexity increases, baseline performance degrades substantially—π 0.5 ’s SR
dropsfrom34.6underBackgroundto23.3underMix(a33%decline). Incontrast,QWEN-ROBOTMANIP
remainsremarkablystableacrossalldimensions(SR44.5–46.8),withvirtuallynodegradationunder
compoundedperturbations. Thegapoverthenext-bestmethodwidensfromBackground(+10.7SR)and
Instruction(+12.9),toObject(+15.9)andMix(+23.5). UnderthemostdemandingMixcondition—where
background,instruction,andobjectperturbationsareappliedsimultaneously—QWEN-ROBOTMANIP
achieves 46.8%, even surpassing its own Background score (45.3%), whereas π 0.5 drops from 34.6 to
23.3 (−33%). This near-uniform performance under diverse distribution shifts demonstrates strong
generalizationrobustness.
RoboTwin-IF. Table8reportsper-suiteresults. QWEN-ROBOTMANIPachieves72.2%averageversus
π ’s49.6%,agapof22.6points. Theimprovementhappensonfouroffivesuites,withlargegainson
0.5
Pick-Diverse(+35),Place-Relative(+37),Operated-Mic-Drawer(+27),andOperated-Tabletop(+27)—
taskswheretheinstructionmustbeparsedtodeterminethecorrectactionamongmultipleplausible
alternativesinthesamescene. ThiscomprehensiveadvantageconfirmsthatQWEN-ROBOTMANIPhas
learnedgenuinelanguage-conditionedcontrolratherthanrelyingonvisualshortcuts.
Zero-ShotCross-Embodiment. Table9reportszero-shottransferforbothjoint-spaceandcamera-frame
relativeEEFrepresentationsonRoboTwin-XE.Joint-spacecontroltransferspoorly: jointconfigurations
arerobot-specific,soactionsmeaningfulforonemorphologyproducenear-randombehavioronanother—
UR5andFrankastaybelow5%forbothmethods. Switchingtocamera-frameEEFdramaticallyimproves
transfer: QWEN-ROBOTMANIPreaches42.9%onARX,22.8%onUR5(5.6×thejointresult),and5.9%on
Franka,foracross-embodimentaverageof23.9%. Thisconfirmsthatthecamera-framerepresentation
successfullyabstractsawaymorphologicaldifferences,allowingthepolicytoreasoninsharedCartesian
space. Our model consistently outperforms π in both action spaces, with the largest gap on UR5
0.5
Theperformancegradient(ARX>UR5>Franka)correlateswithvisualandkinematic
(22.8vs.10.0).
similaritytothetrainingembodiment: ARX-X5sharesavisuallysimilar6-DOFformfactorandsimilar
reachtoAgileX,UR5differsinappearanceandjointarrangementbuthasasimilarworkspace,while
Franka’sdistinct7-DOFmorphologyandlargerreachpresentthegreatestmismatch.
23

Figure10: Zero-shotcross-embodimentevaluationonRoboTwin-XE.Left: ARX-X5. Middle: UR5-WSG.
Right: FrankaPanda.
Table9: Zero-shotperformanceonRoboTwin-XE,wheremodelsaretrainedonRoboTwinCleanand
testedonHardsettingswithunseenrobotembodiments.
|     |     |                          |     | ARX-X5 | UR5-WSG | FrankaPanda | Total |
| --- | --- | ------------------------ | --- | ------ | ------- | ----------- | ----- |
|     | π   | (joint)(Blacketal.,2025) |     | 24.6   | 2.2     | 0.9         | 9.2   |
0.5
|     | π   | (eef)(Blacketal.,2025) |     | 11.5 | 10.0 | 1.1 | 7.5 |
| --- | --- | ---------------------- | --- | ---- | ---- | --- | --- |
0.5
|     | QWEN-ROBOTMANIP(joint) |     |     | 37.6 | 4.1  | 1.8 | 14.5 |
| --- | ---------------------- | --- | --- | ---- | ---- | --- | ---- |
|     | QWEN-ROBOTMANIP(eef)   |     |     | 42.9 | 22.8 | 5.9 | 23.9 |
In-domain real-world evaluation setup
table-cleanup three-bowl-stacking melon-in-bowl towel-folding block-in-drawer-compartment yellow-disc-insertion three-block-stacking
etatS laitinI
etatS laniF
| tpmorPelpmaxE | P i c k   u | p   t h e   p i n k   b o w l   a n d   p l a c e   i t   |     |     | O p e n |   t h e   d r a w e r ,   p i c k   u p   t h e  r e d  |     |
| ------------- | ----------- | --------------------------------------------------------- | --- | --- | ------- | ------------------------------------------------------- | --- |
o n   t o p   o f   t h e   g r e e n   b o w l .  T h e n   P ic k  u p   th e  b lu e  b o w l,  t h en place  b l o c k ,   p l a c e   i t   i n t o   t h e   s m a ll   I n s e r t  t h e   yellow disc into the  S ta c k   t h e   b lu e   b l o c k   o n  t o p   o f  t h e
Clean up the table p i c k   u p   t h e   b l u e   b o w l   a n d   p l a c e   i t   th e  m e l o n  in to   th e  b o w l . Fold the towel. c o m p a r t m e n t   i n s i d e   t h e   d r a w e r ,  y e ll o w   s lo t . r e d  b lo c k ,  a n d   t h e n   p l a c e   t h e
o n   t o p   o f   t h e   p in k   b o w l . a n d   th e n   c lo s e   t h e   d r a w e r . y e ll o w   b l o c k  o n   t o p   o f   th e   b l u e  o n e .
Out-of-domain real-world evaluation setup
|     | target-object-in-basket |     | left-right-bowl-stacking |     | tool-on-towel |     | banana-on-towel |
| --- | ----------------------- | --- | ------------------------ | --- | ------------- | --- | --------------- |
enecS
OOD factors: cluttered background, unseen  OOD factors: cluttered background, unseen  OOD factors: cluttered background, unseen  OOD factors: dynamic lighting disturbance
|     | objects, randomized targets       |                                                         | objects, left-right reference                   |                            | small objects, distractors |     | (disco light) |
| --- | --------------------------------- | ------------------------------------------------------- | ----------------------------------------------- | -------------------------- | -------------------------- | --- | ------------- |
|     | P a tt er n :  P u t  t h e  [ co | lo r ]  [ o b je ct ]   i n t o   t h e   b a s k e t . | P ic k   u p   t h e   [ r i g h t  /   le f t] |  bowl and place it on top  |                            |     |               |
tpmorP Pick the [sliver spoon / black knife]onto the towel. Pick the banana and place it onto the towel.
|     | Ex a m p le :  P u t   th e  o ra | n g e   ca r ro t    i n t o   t h e   b a s k e t . | of  t h e   [ l e ft   /  r i g h t ]   b o w | l.  |     |     |     |
| --- | --------------------------------- | ---------------------------------------------------- | --------------------------------------------- | --- | --- | --- | --- |
Figure11: In-domainandout-of-domaintasksofreal-worldCobotMagicALOHAplatform.
6.3 Real-WorldEvaluation
6.3.1 EvaluationonALOHAPlatforms
In-Domain(ID)andOut-of-Domain(OOD)EvaluationonCobotMagicALOHA.Wefine-tuneQWEN-
ROBOTMANIP on 22.9 hours of teleoperated demonstrations collected on the CobotMagic ALOHA
platform,coveringmultiplebimanualmanipulationtasks. Wethenevaluatethefine-tunedpolicyon
real-worldIDandOODbenchmarks(Figure11)constructedonthesameplatform.
TheIDbenchmarkincludesseventasks: table-cleanup(clearingobjectsfromthetable),three-bowl-stacking
(stackingthreebowlsinthespecifiedorder),melon-in-bowl(placingasmallsphericalmelontoyintoa
bowl),towel-folding(foldingatowel),place-block-into-drawer(openingadrawer,placingablockinside,
andclosingthedrawer),yellow-disc-insertion(pickingupadisc,performingabimanualhandover,and
insertingitintoamatchingslot),andthree-block-stacking(stackingthreeblocksinsequence). Thesetasks
spanawiderangeofmanipulationdifficulty.
24

Table 10: In-domain real-world evaluation on the CobotMagic ALOHA platform. We report task
successover5trialsforeachtask.
|     | Task |     | π StarVLA | QWEN-ROBOTMANIP |     |     |
| --- | ---- | --- | --------- | --------------- | --- | --- |
0.5
|     | table-cleanup               |     | 4/5   | 0/5   | 5/5   |     |
| --- | --------------------------- | --- | ----- | ----- | ----- | --- |
|     | three-bowl-stacking         |     | 5/5   | 4/5   | 5/5   |     |
|     | melon-in-bowl               |     | 2/5   | 0/5   | 5/5   |     |
|     | towel-folding               |     | 4/5   | 3/5   | 4/5   |     |
|     | block-in-drawer-compartment |     | 0/5   | 0/5   | 5/5   |     |
|     | yellow-disc-insertion       |     | 0/5   | 0/5   | 2/5   |     |
|     | three-block-stacking        |     | 0/5   | 0/5   | 5/5   |     |
|     | Averagesuccessrate          |     | 42.9% | 20.0% | 88.6% |     |
Table11: Out-of-domainreal-worldevaluationontheCobotMagicALOHAplatform. Wereporttask
successover10trialsforeachtask.
| Task |     | OODfactors |     | π StarVLA | QWEN-ROBOTMANIP |     |
| ---- | --- | ---------- | --- | --------- | --------------- | --- |
0.5
target-object-in-basket clutteredbackground, unseen 8/10 0/10 10/10
objects,randomizedtargets
left-right-bowl-stacking clutteredbackground, unseen 1/10 0/10 10/10
objects,left-rightreference
| tool-on-towel |     | clutteredbackground, | unseen | 0/10 | 0/10 | 6/10 |
| ------------- | --- | -------------------- | ------ | ---- | ---- | ---- |
smallobjects,distractors
| banana-on-towel |     | dynamic lighting | disturbance | 6/10 | 0/10 | 9/10 |
| --------------- | --- | ---------------- | ----------- | ---- | ---- | ---- |
(discolight)
| Averagesuccessrate |     | –   |     | 37.5% | 0.0% | 87.5% |
| ------------------ | --- | --- | --- | ----- | ---- | ----- |
Attheeasierend,table-cleanup,three-bowl-stacking,andmelon-in-bowlprimarilytestbasiclanguageground-
ingandsequentialpick-and-placeexecution. Towel-foldingismorechallengingduetothedeformable
natureoftheobject. Theremainingtasksaresubstantiallyharder: place-block-into-drawerisparticularly
challengingbecauseitrequirestherobottoaccuratelygraspthesmalldrawerhandleandperformprecise
pullingandpushingmotionstoopenandclosethedrawer,yellow-disc-insertionrequiresfine-grainedpose
alignmentforcontact-richinsertion,andthree-block-stackingdemandsreliablerelationalreasoningand
robustmulti-stepexecution,whilealsotestingthemodel’sabilitytorecoverfromintermediatefailures,
sinceblocksmaysliporcollapseduringthestackingprocess.
As shown in Table 10, QWEN-ROBOTMANIP achieves an average success rate of 88.6%, significantly
outperformingπ (42.9%)andStarVLA(20.0%). Itsucceedsinall5trialsonfivetasksandremains
0.5
strongontowel-folding(4/5). Theonlytaskwithnoticeableroomforimprovementisyellow-disc-insertion
(2/5), highlightingthedifficultyofpreciseinsertiononrealhardware. Incomparison, π 0.5 performs
reasonably well on relatively simple tasks such as table-cleanup, three-bowl-stacking, and towel-folding,
butitsperformancedegradessharplyonmorechallengingtasksthatrequirelong-horizonplanning,
precise contact-rich manipulation, or recovery from intermediate failures. StarVLA performs poorly
acrossalmostalltasks,withlimitedsuccessevenontheeasierones. TheseresultsindicatethatQWEN-
ROBOTMANIPnotonlyhandlesbasicreal-worldmanipulationreliably,butalsoscalesmuchbetterto
morechallengingtasksettings.
Wefurtherevaluatereal-worldgeneralizationinanout-of-domain(OOD)settingonCobotMagicALOHA.
Compared with the ID benchmark, these tasks introduce distribution shifts in visual scenes, object
instances, and task instructions, and are designed to test whether the model can robustly generalize
beyondtheseendistribution.
The OOD benchmark contains four tasks: target-object-in-basket (placing the instructed objects into a
basket),left-right-bowl-stacking(stackingonebowlontoanotherbasedonleft-rightreferences),tool-on-
towel(placingaspecifiedtoolontoatowel),andbanana-on-towel(placingabananaontoatowel). Each
tasktargetsadifferentaspectofgeneralization. Target-object-in-basketintroducesclutteredbackgrounds,
varied objects, and randomized target objects, testing whether the model can correctly identify and
Left-right-bowl-stackingcombinesclutteredscenes
manipulatetheinstructedobjectundervisualvariation.
andleft-rightrelationalreferences,requiringrobustspatiallanguageunderstanding. Tool-on-towelfurther
increasesdifficultybyintroducingunseenandphysicallysmallobjects(i.e.,knifeandspoon)together
withdistractors,makingbothtargetidentificationandstablegraspingmoredifficult. Finally,banana-
on-towelevaluatesrobustnesstosevereilluminationchangesinducedbyadiscolightinthereal-world
environment.
25

laitinI
ssergorP
nI
laniF
tpmorP
Put Fruits Put Blocks Fold Towel Insert Screw Unscrew Cap
P in u t t o a t l h l e th b e a f s r k u e it t s . P b u r l i o t g c t h h k t s e d i b n ra u to w il d e t i h r n . e g Fo a ld s m th a e l l t o sq w u e a l r i e n . to Inse in rt t o t h t e h e t o h y o s le c . rew Unscrew the cap.
laitinI
laniF
tpmorP
Few-shot Adaptation Real-world ARX Evaluation Setup
Cross-embodiment Skill Transfer on ARX Evaluation Setup
Stack Plates Stack Blocks Fruits in Plate Trash in Bucket
Stac p k l a t t h e e s . pink Stack b l t o h c e k s b . rown in P to u t t h a e ll t p h in e k f r p u l i a t t s e. Pu b t a a l b l l s l u t i c n h k t e e o t p . t a h p e er
Figure12: Real-worldevaluationsetupontheARXALOHAplatform.
AsshowninTable11, QWEN-ROBOTMANIPgeneralizessubstantiallybetterthanthebaselinesinthe
OODsetting,achievinganaveragesuccessrateof87.5%,comparedwith37.5%forπ and0.0%for
0.5
StarVLA.Inparticular, QWEN-ROBOTMANIP attainsperfectsuccessontarget-object-in-basketandleft-
right-bowl-stacking,demonstratingstrongrobustnesstoclutteredscenes,attribute-basedgrounding,and
left-rightspatialreferences. Italsoremainseffectiveonthemoredifficulttool-on-toweltask(6/10),where
therobotmustidentifynoveltargetobjectsunderobjectdistractors,andonbanana-on-towel(9/10)under
lightingvariation.
Incontrast,π retainssomerobustnessonrelativelysimplerOODvariations,achieving8/10ontarget-
0.5
object-in-basket and 6/10 on banana-on-towel. However, its performance collapses on tasks requiring
stronger compositional and relational generalization, obtaining only 1/10 on left-right-bowl-stacking
and 0/10 on tool-on-towel. StarVLA fails on all four OOD tasks. These results suggest that QWEN-
ROBOTMANIPpreservesmuchstrongervisual-linguisticrepresentationandisconsiderablymorerobust
tosceneclutter,novelobjects,spatialreferences,andlightingchangesinreal-worldsettings.
Few-shotAdaptationonARXALOHA.WecompareQWEN-ROBOTMANIPagainsttwobaselinesonfive
real-worldmanipulationtasks(Figure12,top;Table12): π (Blacketal.,2025),apretrainedopen-source
0.5
VLA,andStarVLA(Community,2026)trainedfromscratchwithoutpretraining. Allmethodsusejoint
positions and EEF pose as state and predict actions in EEF space, jointly fine-tuned on the same 130
teleoperateddemonstrations(50forUnscrewCap,20foreachothertask). Thefivetasksspanmulti-
objectpick-and-place(PutFruits),long-horizonsequentialmanipulation(PutBlocks),deformableobject
handling(FoldTowel),bimanualprecisionassembly(InsertScrew),andfine-grainedrotationalcontrol
(UnscrewCap).
QWEN-ROBOTMANIPoutperformsbothbaselinesonfouroffivetasks. ThelargestgainappearsonPut
Blocks(15/40vs.10/40forπ
0.5
),whereQWEN-ROBOTMANIPmaintainshighersub-stepsuccessthrough
allfourstages—opendrawer,placetwoblocks,andclosedrawer—indicatingmorerobustlong-horizon
execution.OnUnscrewCap,QWEN-ROBOTMANIPdoublesthecap-removalrateoverπ
0.5
(4/10vs.2/10)
andtriplesthefull-taskcompletion(3/10vs.1/10),showingstrongerfine-grainedrotationalcontrol.
FoldTowelimprovesnotablyonthesecondfold(3/10vs.1/10). InsertScrewremainschallengingforall
methods,withnomodelcompletingafullinsertion(0/10),thoughbothπ
0.5
andQWEN-ROBOTMANIP
succeedatthehandoversub-step(2/10). StarVLA,withoutpretraining,achievesnear-zeroacrosstasks,
confirmingtheimportanceoflarge-scalepretrainingforreal-worldmanipulation.
26

Table12: Few-shotadaptationonARXALOHA.Sub-stepsuccessover10trials. Allmethodsarejointly
fine-tunedon130teleoperateddemonstrations(50forUnscrewCap,20foreachothertask).
|     | Task | Sub-step |     | StarVLA π | QWEN-ROBOTMANIP |     |     |
| --- | ---- | -------- | --- | --------- | --------------- | --- | --- |
0.5
|     |     | Placefruit1 |     | 3/10 9/10 | 9/10 |     |     |
| --- | --- | ----------- | --- | --------- | ---- | --- | --- |
|     |     | Placefruit2 |     | 1/10 5/10 | 5/10 |     |     |
PutFruits
|     |             | Placefruit3   |     | 0/10 2/10   | 3/10  |     |     |
| --- | ----------- | ------------- | --- | ----------- | ----- | --- | --- |
|     |             | Avg.success   |     | 13.3% 53.3% | 56.7% |     |     |
|     |             | Opendrawer    |     | 1/10 4/10   | 5/10  |     |     |
|     |             | Placeblock1   |     | 1/10 2/10   | 4/10  |     |     |
|     | PutBlocks   | Placeblock2   |     | 0/10 2/10   | 3/10  |     |     |
|     |             | Closedrawer   |     | 0/10 2/10   | 3/10  |     |     |
|     |             | Avg.success   |     | 5.0% 25.0%  | 37.5% |     |     |
|     |             | Firstfold     |     | 0/10 3/10   | 3/10  |     |     |
|     | FoldTowel   | Secondfold    |     | 0/10 1/10   | 3/10  |     |     |
|     |             | Avg.success   |     | 0.0% 20.0%  | 30.0% |     |     |
|     |             | Handoverscrew |     | 0/10 2/10   | 2/10  |     |     |
|     | InsertScrew | Insertscrew   |     | 0/10 0/10   | 0/10  |     |     |
|     |             | Avg.success   |     | 0.0% 10.0%  | 10.0% |     |     |
|     |             | Graspbottle   |     | 4/10 9/10   | 9/10  |     |     |
|     |             | Unscrewcap    |     | 0/10 2/10   | 4/10  |     |     |
UnscrewCap
|                                |          | Placedown                           |             | 0/10 1/10   | 3/10          |               |       |
| ------------------------------ | -------- | ----------------------------------- | ----------- | ----------- | ------------- | ------------- | ----- |
|                                |          | Avg.success                         |             | 13.3% 40.0% | 53.3%         |               |       |
|                                | Table13: | Cross-embodimentskilltransferonARX. |             |             |               |               |       |
|                                |          |                                     | StackPlates | StackBlocks | FruitsinPlate | TrashinBucket | Avg.  |
| QWEN-ROBOTMANIPw/oUnifiedSpace |          |                                     | 0/10        | 0/10        | 3/10          | 0/10          | 7.5%  |
| QWEN-ROBOTMANIPw/oUnifiedEEF   |          |                                     | 0/10        | 0/10        | 5/10          | 0/10          | 12.5% |
| QWEN-ROBOTMANIP                |          |                                     | 3/10        | 5/10        | 7/10          | 7/10          | 55.0% |
Cross-embodimenttransfer. Wealsoinvestigatecross-embodimentskilltransfer(Figure12,bottom;
Table13). Asinglepolicyisjointlyfine-tunedon6KCobotMagicand130ARXdemonstrations,usingthe
samestate-actionparameterizationasabove,thenevaluatedonfournoveltasksontheARXplatform:
stackingtwoplates,stackingblocks,placingfruitsintoadesignatedpinkplatewithdistractorplates,
andcollectingpaperballsintoabucket. ARXhaszerodemonstrationsforanyofthesetasks—therelevant
manipulation skills (stacking, precise placement, object collection) must generalize from related but
notidenticalCobotMagicbehaviorsacrossakinematicallydifferentembodiment. Weablatetwokey
components: QWEN-ROBOTMANIPw/oUnifiedSpaceremovestheunifiedaction-spacemappingand
insteadnaivelyconcatenatesandzero-padseachrobot’sactiondimensionswithoutsemanticalignment;
QWEN-ROBOTMANIPw/oUnifiedEEFremovestheunifiedEEFrepresentationwhileretainingabasic
slotlayoutwithrotationunificationandgrippernormalization. Bothvariantsfailalmostentirely(7.5%
and12.5%),showingthatneithersurface-leveldimensionalignmentnorpartialunificationcanbridgethe
combinedembodimentandtaskgap. QWEN-ROBOTMANIPachieves55.0%—over4×thebestvariant—
succeedingonallfourtasksincludingStackBlocks(5/10)andTrashinBucket(7/10). Thefullunified
action space and EEF representation enable QWEN-ROBOTMANIP to learn a stronger manipulation
representationthroughlarge-scalediversepretraining,enablingskill-leveltransfer: apolicycanleverage
skillslearnedfromoneembodimenttoexecutenoveltasksonanotherembodimentwithminimaltraining
dataandnotask-specificdemonstrations.
6.3.2 Table30-v1Challenge
To evaluate the generalization capability of QWEN-ROBOTMANIP, we submit to the RoboChallenge
Table30 v1 benchmark under the generalist track. This benchmark comprises 30 manipulation tasks
distributedacross4robotembodiments,andofferstwoevaluationtracks: thespecialisttrack,wherea
dedicatedpolicyistrainedforeachindividualtask(requiring30separatemodels),andthegeneralist
track,whereasingleunifiedpolicyistrainedperembodimenttohandlealltasksassociatedwiththat
robot. Thegeneralistsettingissubstantiallymorechallenging,asitdemandsthatthepolicygeneralize
acrossdiversemanipulationskillswithineachembodimentratherthanoverfittingtoasingletask. We
focusonthistrackasitbetterreflectsreal-worlddesideratumofbuildingversatilemanipulationpolicies.
27

Table14: Per-taskresultsontheRoboChallengeTable30v1GeneralistTrack. Eachcellreportssuccess
| rate(%)/processscore. Bestresultspertaskareinbold. |     |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- |
Robot Task QWEN-ROBOTMANIP DM0_generalist pi05_generalist GR00T-MULTI pi0_generalist
Average(all) 45/59.83 37/48.43 17.67/31.27 15.33/32.29 9/20.22
| arrangeflowers   | 30/64 | 20/49   | 0/30.5 | 20/57 | 0/13.5 |
| ---------------- | ----- | ------- | ------ | ----- | ------ |
| arrangepapercups | 70/83 | 10/54   | 0/31   | 0/19  | 0/15   |
| folddishcloth    | 30/48 | 10/10.5 | 0/0    | 0/17  | 0/0    |
| openthedrawer    | 0/47  | 90/95   | 50/80  | 0/50  | 0/20   |
100/98.5
| placeshoesonrack | 70/85  |         | 0/20  | 40/54.5 | 0/16.5 |
| ---------------- | ------ | ------- | ----- | ------- | ------ |
| putcuponcoaster  | 100/99 | 100/100 | 70/63 | 80/92   | 0/0    |
ARX5
| searchgreenboxes           | 90/92     | 100/95.5  | 0/3       | 30/37.5   | 0/0       |
| -------------------------- | --------- | --------- | --------- | --------- | --------- |
| sortelectronicproducts     | 50/60.4   | 0/18.4    | 0/22.5    | 10/34.8   | 0/22.5    |
| turnonlightswitch          | 70/69.5   | 70/70.5   | 10/25     | 0/5       | 20/29     |
| waterpottedplant           | 0/9       | 0/33.5    | 0/0       | 0/6       | 0/0       |
| wipethetable               | 0/72.5    | 0/47.5    | 10/28     | 0/66      | 0/29      |
| Avg(ARX5)                  | 46.4/66.3 | 45.5/61.1 | 12.7/27.5 | 16.4/39.9 | 1.8/13.2  |
| cleandiningtable           | 20/57.5   | 0/12      | 30/62     | 10/11.5   | 0/25.5    |
| makevegetariansandwich     | 10/46.5   | 0/15      | 0/0       | 0/7       | 0/0       |
| pluginnetworkcable         | 30/51     | 10/26     | 0/0       | 0/3       | 0/0       |
| pourfriesintoplate         | 30/56     | 0/6       | 0/0       | 0/36      | 0/0       |
| putopenerindrawer          | 0/0       | 10/10     | 20/38     | 0/0       | 0/0       |
| ALOHA putpenintopencilcase | 90/95     | 20/40     | 50/63.5   | 20/58     | 0/14.5    |
| scanQRcode                 | 10/13     | 0/0       | 0/7       | 30/26.5   | 0/3       |
| stackbowls                 | 100/98.5  | 70/71     | 80/83     | 40/55.5   | 40/53.5   |
| sticktapetobox             | 0/22.5    | 0/14      | 0/16      | 0/2       | 0/0       |
| sweeptherubbish            | 70/84.5   | 30/40     | 10/46     | 10/10     | 0/17      |
| turnonfaucet               | 100/100   | 70/84.5   | 60/56     | 20/44     | 60/67.5   |
| Avg(ALOHA)                 | 41.8/56.8 | 19.1/29.0 | 22.7/33.8 | 11.8/23.0 | 9.1/16.5  |
| arrangefruitsinbasket      | 80/89.5   | 70/87     | 0/9       | 30/54.5   | 0/11.5    |
| hangtoothbrushcup          | 60/80     | 90/95     | 50/71     | 70/85     | 20/62     |
| settheplates               | 100/87.5  | 60/62     | 40/49.5   | 0/24      | 50/69.5   |
| UR5 shredscrappaper        | 0/15      | 30/45     | 20/36     | 0/0       | 20/27     |
| sortbooks                  | 0/9       | 0/8.5     | 0/24      | 0/6.5     | 10/26.5   |
| stackcolorblocks           | 70/84.5   | 100/100   | 10/30     | 0/44.5    | 30/39     |
| Avg(UR5)                   | 51.7/60.9 | 58.3/66.2 | 20.0/36.6 | 16.7/35.8 | 21.7/39.2 |
| moveobjectsintobox         | 70/75.5   | 50/64.5   | 20/40     | 50/62     | 20/44.5   |
| Franka pressthreebuttons   | 0/0       | 0/0       | 0/4       | 0/0       | 0/0       |
Avg(Franka) 35.0/37.8 25.0/32.2 10.0/22.0 25.0/31.0 10.0/22.2
Specifically, we post-train QWEN-ROBOTMANIP on the demonstration data provided by Table30 v1
usingjointcontrol,andsubmitundertheanonymousidentityLira_generalist2.
QWEN-ROBOTMANIP
achievesasuccessrateof45%andaprocessscoreof59.83. Notably, QWEN-ROBOTMANIPsurpasses
DM0_generalist(37%successrate,48.43processscore)by8percentagepointsinsuccessrateand11.4in
processscore,demonstratingitsstrongmulti-taskgeneralizationability. Wehighlightthreekeyfindings
fromdetailedanalysisofthebenchmarkresults.
Strongbimanualcoordination. Amongthe30benchmarktasks,8requiretightbimanualcoordination
ontheALOHAplatform3,wherethetwoarmsmustjointlystabilize,transport,andmanipulateobjects.
QWEN-ROBOTMANIPachievesanaveragesuccessrateof40%onthesetasks,farexceedingπ (21.2%),
0.5
DM0 (16.2%), GR00T-MULTI (7.5%), and π (7.5%) (Figure 14, left). Notably, QWEN-ROBOTMANIP
0
| only | pour fries | into plate |     |     |     |
| ---- | ---------- | ---------- | --- | --- | --- |
is the model to succeed on (30% vs. 0% for all baselines), a task demanding
sequential bimanual steps—stabilizing the fries box with the left arm, opening it with the right arm,
pickingitup,andpouringthecontentsontotheplate. AsillustratedinFigure13,QWEN-ROBOTMANIP
completesthisfullsequence,whileDM0_generalistfailsattheinitialcoordinationstage: therightarm
neverreachesagraspablepositiononthebox,resultinginimmediatetaskfailure. Weattributethisstrong
bimanualperformancetotwofactors: (1)ourpre-trainingcorpuscontainsasubstantialproportionof
bimanualdemonstrationrobotdata,enablingthemodeltoeffectivelylearncoordinateddual-armcontrol
primitives;and(2)ourHuman2Robotpipeline,whichsynthesizesbimanualrobotdatafromegocentric
humanvideos,furtherexpandstheeffectivebimanualpre-trainingdataandexposesthemodeltodiverse
manipulationstrategiesbeyondthosecapturedinteleoperateddemonstrationsalone.
2SeeLira_generalistinhttps://robochallenge.cn/home.
3The8bimanualtasks:cleandiningtable,makevegetariansandwich,pourfriesintoplate,putopenerindrawer,putpen
intopencilcase,sticktapetobox,sweeptherubbish,turnonfaucet.
28

…
|     | Stabilize the friesbox with the left hand and open the  |     | Pick up the fries |     | Pour the fries |     |
| --- | ------------------------------------------------------- | --- | ----------------- | --- | -------------- | --- |
Success!
|     | bottom-right corner of the box with the right hand. |     |     | box | box |     |
| --- | --------------------------------------------------- | --- | --- | --- | --- | --- |
Task start
QWEN-ROBOTMANIP, pour fries into plate, 30%success rate
…
|     | Stabilize the friesbox with the left hand and reach the  |     |     | Failed! The right arm is not yet  |     |     |
| --- | -------------------------------------------------------- | --- | --- | --------------------------------- | --- | --- |
Task start bottom-right corner of the box with the right hand. at a graspable position.
DM0_generalist, pour fries into plate, 0%success rate
Figure13: Casestudyonpourfriesintoplate(ALOHA).QWEN-ROBOTMANIP(top)coordinatesboth
armstostabilize,open,pickup,andpourthefriesbox,completingthetasksuccessfully. DM0_generalist
(bottom)failsattheinitialstageastherightarmneverreachesagraspableposition.
|     | Bimanual Tasks (8 tasks) |     |     | Pick-and-Place Tasks (12 tasks) |     |     |
| --- | ------------------------ | --- | --- | ------------------------------- | --- | --- |
70
| 40.0 |     |     | 63.3 |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- |
40
60
|                     |     | 50               |     |     | 48.3 |     |
| ------------------- | --- | ---------------- | --- | --- | ---- | --- |
| )%( etaR sseccuS 30 |     | )%( etaR sseccuS |     |     |      |     |
40
21.2
20
|     | 16.2 | 30  |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- |
23.3
20.8
20
| 10  |     |     |     |     |     | 12.5 |
| --- | --- | --- | --- | --- | --- | ---- |
7.5 7.5
10
| 0    |                 | 0   |      |     |                 |     |
| ---- | --------------- | --- | ---- | --- | --------------- | --- |
| Ours | DM0 GR00T-MULTI |     | Ours |     | DM0 GR00T-MULTI |     |
|      | 0.5             | 0   |      | 0.5 |                 | 0   |
Figure14: Averagesuccessrateonbimanualcoordinationtasks(left,8tasks)andpick-and-placetasks
(right,12tasks). QWEN-ROBOTMANIPsubstantiallyoutperformsallbaselinesinbothcategories.
Robustpick-and-placeacrossembodiments. Weidentify12tasksacrossallfourplatformsthatcenter
onpick-and-placeprimitives4,rangingfromsingle-objectgrasping(putcuponcoasterandstackcolorblocks)
tomulti-stepsequentialmanipulationinvolving4–5objects(arrangepapercupsandsortelectronicproducts).
AsshowninFigure14(right),QWEN-ROBOTMANIPachieves63.3%averagesuccessrateonthesetasks,
surpassingthenext-bestbaselineDM0(48.3%)by15.0percentagepoints. Weattributethiscapabilityto
twofactors: (1)thelarge-scalecross-embodimentpre-trainingdataencodesabundantpick-and-place
patterns,and(2)theunifiedactionspaceenablesknowledgesharingoffundamentalspatialskillsacross
different robot morphologies. Figure 15 shows a representative comparison on arrange paper cups, a
taskrequiringsequentialpick-and-placeofmultiplecupsfollowedbystacking. QWEN-ROBOTMANIP
(70%SR)successfullypickseachcupinsequence,stacksthemprecisely,whileπ _generalist(0%SR)
0.5
encountersastuckcupduringstackingandfailstorecover,leadingtocascadingerrorsinsubsequent
steps.
Emergentretrybehavior. Arecurringpatternweobserveduringreal-robotevaluationisthatQWEN-
ROBOTMANIPexhibitsspontaneousretrybehavior: whenaninitialmanipulationattemptfails(e.g.,a
graspslipsoraplacementmisses)thepolicyautonomouslyre-attemptstheactionratherthanproceeding
tothenextsteporstalling. Whilethisbehaviorisdifficulttoquantifywithasinglemetric,weobserve
4The12pick-and-placetasksare:arrangeflowers,arrangefruitsinbasket,arrangepapercups,cleandiningtable,move
objectsintobox,settheplates,sortbooks,sortelectronicproducts,stackbowls,placeshoesonrack,putcuponcoaster,and
stackcolorblocks.
29

…
Pick the third Stack the third Pick the last Stack the last Pick up all the
Success!
Task start paper cup paper cup paper cup paper cup stacked paper cups
QWEN-ROBOTMANIP, arrange paper cups, 70%success rate
…
Pick the first Stack the first Pick the second The paper cup Pick the third
Failed!
Task start paper cup paper cup paper cup gets stuck! paper cup
pi05_generalist, arrange paper cups, 0%success rate
Figure15: Casestudyonarrangepapercups(ARX5). QWEN-ROBOTMANIP (top)sequentiallypicks,
stacks,andcollectsallpapercupswithpreciseplacement. π _generalist(bottom)encountersastuck
0.5
cupduringstackingandfailstorecover.
…
The first Pick up success The second Pick up success The third
Success!
Task start attempt but fall down attempt but fall down again attempt
QWEN-ROBOTMANIP, sort electronic products, 50%success rate
…
The first The second Pick up failed The third
Pick up failed Failed!
Task start attempt attempt again attempt
DM0_generalist, sort electronic products, 0%success rate
Figure16: Casestudyonsortelectronicproducts(ARX5). QWEN-ROBOTMANIP(top)picksuptheobject
butitfallstwice;thepolicyautonomouslyretriesandsucceedsonthethirdattempt. DM0_generalist
(bottom)alsoattemptsthreetimesbutneverachievesasecuregrasp.
it consistently across diverse action primitives including picking, placing, pouring, folding, wiping,
andsweeping. Thisself-correctivecapabilitysignificantlyimprovesfaulttolerance,allowing QWEN-
ROBOTMANIP to recover from intermediate failures that would otherwise cause task-level failures.
Figure16providesavividexampleonsortelectronicproducts: QWEN-ROBOTMANIPsuccessfullypicks
up the object on its first attempt, but the object falls; it then re-attempts, and the object falls again;
onthethirdattempt, QWEN-ROBOTMANIP finallycompletesthegraspandplacestheobjectintothe
targetbin,achievingtasksuccess(50%SR).Incontrast,DM0_generalist(0%SR)alsoattemptsthepick
threetimesbutfailseveryattempt—thegripperneverachievesasecuregrasp,leadingtotaskfailure.
We hypothesize that this retry behavior emerges from the diversity of the pre-training data, where
demonstrationsnaturallycontainimperfectattemptsfollowedbycorrections,enablingthemodeltolearn
recoverystrategiesaspartofitspolicy.
Breakthroughonchallengingtasks. TheabovethreecapabilitiesjointlyenableQWEN-ROBOTMANIP
to achieve leading performance on several high-difficulty tasks where most generalist baselines fail
entirely(seeFigure17). OntheALOHAplatform,pluginnetworkcable(30%)andpourfriesintoplate(30%)
bothdemandprecisebimanualcoordinationwithfinepostureadjustment,yetQWEN-ROBOTMANIP
30

6 challenging, long horizon manipulation tasks across ALOHA and ARX5
Previous SOTA methods:5%success | Qwen-RobotManip: 36.7% success
These results highlight the effectiveness of Qwen-RobotManipin tackling complex, multi-step real-world manipulation.
1 Plug in Network Cable 30% success vs. 10% 2 Pour Fries into Plate 30% success vs. 0%
Hand-over
3 Make Vegetarian Sandwich 10% success vs. 0% 4 Arrange Paper Cups 70% success vs. 10%
5 Sort Electronic Products 50% success vs. 0% 5 FoldDishcloth 30% success vs. 10%
Figure17: QWEN-ROBOTMANIPonsixchallenginglong-horizontasksfromRoboChallengeTable30-
v1,spanningbimanualdexterousmanipulation,sequentialingredientstacking,multi-objectarrangement,
anddeformableobjecthandling. PriorSOTAgeneralistmethodsachieveanaverageof5%successacross
thesetasks. QWEN-ROBOTMANIPachieves36.7%,withsubstantialmarginsoneverytask.
is the only model achieving ≥30% success rate. On make vegetarian sandwich (10%)—a long-horizon
task requiring sequential ingredient stacking—QWEN-ROBOTMANIP is the only model to achieve a
non-zerosuccessrate. OnARX5,spatialprecisionandself-correctioncombinetoyieldstrongresults
on arrange paper cups (70%), sort electronic products (50%), and fold dishcloth (30%), outperforming the
next-bestmethodby60,40,and20percentagepointsrespectively. Theseresultsdemonstratethatcross-
embodimentpre-trainingenablestheinterleavedacquisitionofbimanualcoordination,spatialprecision,
andself-correctivestrategies,whichcollectivelyunlockcomplexmanipulationskillsthatremainoutof
reachforexistinggeneralistpolicies.
6.4 AblationStudy
We ablate the core design choices of QWEN-ROBOTMANIP: alignment strategies (state-action repre-
sentation,in-contextadaptation,architecture)anddatarecipesforscaling(human-to-robotsynthesis,
vision-languageco-training).Allvariantswithineachgroupshareidenticaltrainingconditionsatreduced
pretrainingscale;configurationsmaydifferfromthemainresults.
Actionspacealignmentfordatascaling. Acentralpromiseoffoundationmodelsisthatperformance
should improve predictably as training data grows. For vision-language-action models trained on
heterogeneous cross-embodiment data, verifying this property requires careful design of how data
from distinct robots is combined. If the action representations across embodiments are misaligned,
simplyaddingmoredatamaynotyieldincreasingperformance,becausethemodelmustspendcapacity
reconcilingconflictingconventionsratherthanlearningtransferablemanipulationstructure.
To investigate this, we construct a controlled data-scaling experiment. Starting from the full cross-
embodimentpre-trainingmixture,wecreatenestedsubsetsat1%,5%,10%,25%,50%,and100%ofthe
originaldatasetbysamplingattheper-embodimenttasklevel,ensuringthatsmallersubsetsarestrict
subsetsoflargerones. Allmodelsareevaluatedonafixedheld-outOODevaluationsetspanning15
embodimenttypesand154tasksthatareentirelyabsentfromanytrainingset. Foreachdatapercentage
andmodelvariant,wereportthebestvalidationMSEachievedacrossalltrainingcheckpoints,measured
inaunifiedactionrepresentationtoensurefaircomparisonacrossmodelvariants.
Figure18comparesthescalingbehaviorofthreeactionspacedesigns. Oursw/oUnifiedSpaceconcate-
nateseachembodiment’srawactionfieldsandzero-padsto80dimensionswithoutanycross-embodiment
structuralalignment. Oursw/oUnifiedEEFmapsjoints,end-effectors,grippers,andhandsintoseman-
tically fixed positions within the 80-dimensional canonical vector (§§ 3.2), with end-effector actions
31

End-Effector Action Prediction Joint Action Prediction Overall
0.16
0.24
0.18
| 0.14 |     |     |     | 0.22 |     |     |     |     |     |     |     |
| ---- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
0.16
| ESM .laV |     |     |     | 0.20 |     |     |     |     |     |     |     |
| -------- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
0.12
|      |     |     |     | 0.18 |     |     |     | 0.14 |     |     |     |
| ---- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- |
| 0.10 |     |     |     | 0.16 |     |     |     |      |     |     |     |
0.12
0.14
0.08
0.10
0.12
0.06
|     |                   |         |                       | 0.10 |                   |                     |           | 0.08 |                   |         |        |
| --- | ----------------- | ------- | --------------------- | ---- | ----------------- | ------------------- | --------- | ---- | ----------------- | ------- | ------ |
|     | 1                 | 5 10 25 | 50 100                | 1    |                   | 5 10                | 25 50 100 |      | 1                 | 5 10 25 | 50 100 |
|     | Training Data (%) |         |                       |      | Training Data (%) |                     |           |      | Training Data (%) |         |        |
|     |                   |         | Ours w/o UnifiedSpace |      |                   | Ours w/o UnifiedEEF |           | Ours |                   |         |        |
Figure18: Datascalingcurvesformodelswithvariedstateandactionrepresentations,evaluatedon
held-outvalidationdatasets. EachpointreportsthebestvalidationMSEacrossalltrainingcheckpoints
foragiventrainingdatapercentage.
|                  | Easy (joint) |     |     | Hard (joint) |     |     | Easy (eef) |     |     | Hard (eef) |     |
| ---------------- | ------------ | --- | --- | ------------ | --- | --- | ---------- | --- | --- | ---------- | --- |
| 70               |              |     | 50  |              |     |     |            |     |     |            |     |
| )%( etaR sseccuS |              |     |     |              |     | 70  |            |     |     |            |     |
40
| 60  |     |     |     |     |     | 60  |     |     | 40  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
30
50
50
20
|     |     |     | 20  |     |     | 40  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 5 10 25 50 100 1 5 10 25 50 100 1 5 10 25 50 100 1 5 10 25 50 100
Training Data (%) Training Data (%) Training Data (%) Training Data (%)
|     |     |     | Ours w/o UnifiedSpace |     |     | Ours w/o UnifiedEEF |     | Ours |     |     |     |
| --- | --- | --- | --------------------- | --- | --- | ------------------- | --- | ---- | --- | --- | --- |
Figure19: DownstreamperformanceonRoboTwin-C2Rafterfine-tuningmodelspre-trainedwith
varieddatapercentagesandactionrepresentations. Eachsubplotreportssuccessrateunderadifferent
controlmode(jointorEEF)andevaluationsetting(EasyorHard).
expressedasaxis-angledeltasrelativetotheinitialend-effectorpose. Oursfurtherunifiesend-effector
motionbyexpressingitascamera-framedeltaposes(§§3.3),groundingactionsinthevisualobservation
frame.
Modelswithunifiedrepresentations,Oursw/oUnifiedEEFandOurs,bothexhibitacleardatascalinglaw:
theirbestvalidationMSEdecreasesapproximatelylog-linearlywithtrainingdatavolumeacrossthefull
1%–100%range,confirmingthatwithproperaction-spacealignment,scalingupcross-embodimentdata
consistentlyreducesOODpredictionerror. Oursw/oUnifiedSpace,bycontrast,showsnotablydifferent
behavior. Foractionpredictiononend-effectordimensions(Figure18, left), Oursw/oUnifiedSpace
producesanunstablescalingcurvewithsubstantiallyhigherMSEthanthetwounifiedvariants. Ours
achievesthelowestend-effectorMSEonaverage,demonstratingthatcamera-framealignmentenables
themosteffectivecross-embodimenttransferforend-effectorcontrol.
Theseofflinepredictionimprovementstranslatedirectlyintodownstreamtaskperformance. Figure19
reports success rates on RoboTwin-C2R after fine-tuning each pre-trained variant on the RoboTwin
Clean dataset for 80k steps, evaluated under four settings that combine two control modes (joint-
space and end-effector) with two perturbation settings (Easy and Hard). Colors from dark to light
correspondtoprogressivelylessalignedactionrepresentations: Ours,Oursw/oUnifiedEEF,andOurs
w/oUnifiedSpace. OntheOODHardsettings(secondandfourthsubplots),Oursexhibitsacleardata
scalingproperty: downstreamsuccessrateincreasessteadilyaspretrainingdatagrowsfrom1%to100%,
reaching50.2%(joint)and56.6%(EEF)atfullscale. Oursconsistentlyoutperformsbothablatedvariants
across all data percentages, while Ours w/o UnifiedEEF and Ours w/o UnifiedSpace show noisier
scalingcurveswithlessconsistentimprovement. Incontrast,onthein-distributionEasysettings(first
andthirdsubplots),noneofthethreevariantsshowsaclearupwardtrendwithincreasingpretraining
data. This corroborates the finding in §§ 6.1 that standard in-distribution evaluation fails to capture
thebenefitsoflarge-scalepretraining,andthatOODevaluationisneededtorevealthegenuinescaling
behavior. Afurthernotablepatternemergesinthecontrol-modecomparison: Oursachievescomparable
orhighersuccessratesunderEEFcontrolthanunderjointcontrolonbothEasyandHard,whileboth
ablatedvariantsshowtheoppositetrend. Thisconfirmsthatcamera-framealignmentproducesastrong
EEF-spacepolicy,acapabilityessentialforcross-embodimenttransfer.
Ablation study on embodiment prompt design and in-context policy adaptation. We ablate the
32

Table15: Ablationstudyonembodimentpromptdesignandin-contextpolicyadaptation. Out-of-
distributionevaluationonRoboTwin-Clean2Rand(joint). Thespeedissetto500.
Emb.Tag FPS Context DenoiseSteps Easy Hard Avg
QWEN-ROBOTMANIPw/oUnifiedEEF × × × 4 71.2 54.2 62.7
+Soft-Prompt soft × × 4 70.2 52.1 61.2
+LanguagePrompt lang. 15 × 4 71.7 55.1 63.4
+StructurePrompt ✓ 15 × 4 73.4 58.3 65.9
QWEN-ROBOTMANIP-Context ✓ 15 ✓ 4 72.1 54.4 63.3
QWEN-ROBOTMANIP-Context ✓ 15 ✓ 10 80.1 61.6 70.9
QWEN-ROBOTMANIP-Context ✓ 15 ✓ 20 79.8 62.1 71.0
embodiment prompt design and in-context policy adaptation mechanism using an early checkpoint
ofQWEN-ROBOTMANIPtrainedonasmallerdatasubset,evaluatedonRoboTwin-Clean2Randunder
out-of-distributionsettings. ResultsarereportedinTable15.
Onthepromptside,encodingembodimentidentityasalearnablesoftpromptslightlydegradesperfor-
mancerelativetothenaïvebaseline. Anaturallanguagepromptrecoversthisandyieldsamodestgain,
suggestingthatsemanticembodimentlabelscarrysomeusefulsignal,buttheimprovementremains
small,indicatingthatcoarseidentityinformationaloneisinsufficienttomeaningfullyadjustbehavior
acrossembodiments. Thestructuredembodimentprompt,whichadditionallyconditionsthemodelon
thetemporalpropertiesoftheepisodeviatheFPSfield,producesconsistentimprovementsof2.2-3.2
points. Thestructuredpromptprovidesrobustnessunderdistributionshiftratherthanoverfittingto
afixedtemporalconfiguration, butismosteffectivewhenitsfieldsfaithfullyreflectthedeployment
context.
Prompt-level conditioning, however, captures only static episode metadata. The in-context policy
adaptationmechanismintroducesdynamicintra-episodeinformationintheformofasinglehistorical
observation-actionchunk,enablingthemodeltoobservetherobot’sactualbehavioraldynamicsrather
thanrelyingoncoarsecategorylabels. Withoutcontext, thepolicyactiondistributionissmoothand
4denoisingstepsisalreadysufficient, producingstablebehaviorwithnosignsofjitter. Introducing
executionhistoryincreasesthecomplexityoftheactiondistribution,causingthepolicytoproducejittery
motion at the same 4-step budget, which largely negates the benefit of the context signal and yields
performancenearthenaïvebaseline. Increasingthedenoisingbudgetto10stepsresolvestheinstability
andunlocksthefullbenefitofthecontextmechanism,reaching70.9averageanda5.0-pointimprovement
overthestructurepromptbaseline,amarginthatdwarfsthecontributionofanypromptdesignvariant.
Furtherincreasingto20stepsyieldsnoadditionalgain. Theseresultssupporttheviewthatin-context
history functions as an implicit embodiment identifier reflecting intra-episode kinematic signatures
ratherthanasepisodicmemory,andthatthissignalisqualitativelydistinctfromwhatstaticprompt
conditioningcanprovide,providedtheactionheadhassufficientcapacitytodecodeitfaithfully.
Wedonoteonepracticallimitationobservedinreal-robotdeployment: atthestartofanepisode,the
contextconsistsentirelyofzero-paddedplaceholders,andthemodel,havinglearnedtoconditionon
quiescent history, tends to hesitate before initiating motion. We therefore release both the context-
conditioned and context-free variants of QWEN-ROBOTMANIP, allowing users to select appropriate
configurationdependingonwhetherrapidresponseorricherintra-episodeadaptationisthepriority.
Ablation study on human-to-robot synthetic data. To isolate the contribution of egocentric human
data,wecomparethreepretrainingconfigurationsonRoboTwin-Clean2Rand(eef)andLIBERO-Plusata
fixed7:3robot-to-auxiliaryratio(Tables16and17): Robot-onlyusesrobotdataonly;+Egomixesinraw
egocentricdata;+H2Rreplacestherawdatawithpipeline-synthesizedrobotdemonstrationsfromthe
sameegosources. Allthreeshareidenticaltrainingsteps,hyperparameters,andfinetuningdata,soany
performancedifferenceisattributablesolelytotheauxiliarydatasource.
On RoboTwin-Clean2Rand, the Hard setting—where all perturbations are applied simultaneously—
showstheclearestseparation: +H2Rreaches58.7%,a+4.0gainoverRobot-only(54.7%)and+3.7over
+Ego(55.0%). Per-dimensiongainsareconsistent, withthelargestonLight(+3.0)andHeight(+3.2),
wherethevariedcameraperspectivesandlightinginegodatanaturallyaugmentrobustness. TheEasy
settingalsoseesamodestimprovement(72.9→73.4→74.2).
OnLIBERO-Plus,+H2Rraisestheaveragesuccessratefrom87.1%to89.0%. TheCameradimension
showsthelargestimprovement(+7.2overRobot-only,72.8→80.0),asegocentricdataprovidesdiverse
viewpointcoveragethatrobot-onlydatalacks. TheRobotdimensionalsobenefits(+2.0), suggesting
thatthediversemanipulationtrajectoriesinH2Rdataimproverobustnesstoinitialposevariation. The
33

Table16: Human2RobotablationonRoboTwin-Clean2Rand(eef).
Easy Background Light Clutter Height Hard
QWEN-ROBOTMANIP(robot-only) 72.9 70.4 70.3 57.2 67.8 54.7
QWEN-ROBOTMANIP(+ego) 73.4 70.6 71.7 59.2 70.2 55.0
QWEN-ROBOTMANIP(+h2r) 74.2 71.4 73.3 58.1 71.0 58.7
Table17: Human2RobotablationonLIBERO-Plus.
Camera Robot Language Light Background Noise Layout Total
QWEN-ROBOTMANIP(robot-only) 72.8 78.2 88.7 97.5 97.6 95.4 85.4 87.1
QWEN-ROBOTMANIP(+ego) 77.7 79.0 88.5 98.8 98.7 97.3 84.9 88.4
QWEN-ROBOTMANIP(+h2r) 80.0 80.2 89.3 98.5 98.2 96.6 85.2 89.0
Table 18: Ablations on VL data co-training in the pre-training and post-training stage. By default,
QWEN-ROBOTMANIPispre-trainedwithVLdataandpost-trainingwithoutit. (“RT”istheabbreviation
of“RoboTwin”.)
LIBERO LIBERO-Plus RT-C2R(easy) RT-C2R(hard) RT-IF
QWEN-ROBOTMANIP 99.1 90.1 73.2 62.6 71.6
-withoutVLdatainpre-training 98.2 88.9 66.5 54.4 64.6
-withVLdatainpost-training 98.6 91.4 74.0 62.5 73.1
monotonicRobot-only→+Ego→+H2Rprogressionacrossbothbenchmarksconfirmsthatrawego
datacontributesthroughvisualdiversity,whiletheH2Rpipelineunlocksadditionalgainsviaactionand
visualalignment.
Effect of VL data co-training during pre-training. We study the role of VL data in the pre-training
stagebycomparingourfullmodelwithavariantpre-trainedwithoutanyVLdatamixture(Table18).
OnLIBEROandLIBERO-Plus, removingVLdatacausesrelativelysmalldropsof0.9and1.2points,
respectively. Incontrast,theperformancedegradationismuchlargeronthemorechallengingRoboTwin
benchmarks: RoboTwin-Clean2Rand(easy)dropsby6.7points,RoboTwin-Clean2Rand(hard)by8.2
points,andRoboTwin-IFby7.0points. ThistrendindicatesthatVLco-trainingbecomesincreasingly
importantastaskdiversity,scenecomplexity,anddistributionshiftgrow.
WeattributethesegainstothecomplementarybenefitsofdifferentVLdatasources. General-domain
VLdatahelpspreservetheVLM’sbroadperceptualandlinguisticcapabilities,reducingcatastrophic
forgettingduringVLAtraining. Spatialgroundingandreasoningdataimprovesthemodel’sabilityto
localizeobjects,understandspatialrelations,andreasonovercomplexscenes,whichiscrucialforprecise
manipulation. Embodied-centricVLdatafurtheralignstheVLM’srepresentationswiththesemantic
structureofembodiedtasks. Together,thesedatasourcesyieldVLMrepresentationsthatarebettersuited
fordownstreamalignmentwiththeactionexpert.
Architecturedesign. Weconductablationexperimentsonthreenetworkarchitecturevariants(Figure20):
1. The first variant replicates the VLM’s vision and language hidden states as input to the DiT, and
employsapureself-attentionarchitecturewithintheDiT.Aftereachself-attentionlayerintheDiT,the
visionandlanguagefeaturesarefusedwiththecorrespondingper-layervisionandlanguagefeatures
fromtheVLMviaaweightedresidualcombination.
2. ThesecondvariantfeedsonlytheVLM’slast-layerhiddenstatesintotheDiT.TheDiTlikewiseusesa
pureself-attentionarchitecture,butwithoutanyper-layerfeaturefusionwiththeVLM’sintermediate
representations.
3. The third variant introduces a small set of learnable query tokens (Darcet et al., 2024) that act as
condensedproxiesfortheVLM’svisionandlanguagetokens. Thesequerytokensareconcatenated
withthestateandactiontokens;alltokensjointlycross-attendtotheVLM’slast-layerhiddenstates
andself-attendamongthemselves. Thequerytokens’outputsarediscardedafterprocessing.
Allthreevariantsarepretrainedexclusivelyonrobotdataandthenfine-tunedontheLIBEROdataset.
Duringbothpretrainingandfine-tuning,weexcludethestructuredembodimentprompt(retainingonly
theoriginaltaskinstruction),ECoTdata,andin-contextpolicyadaptation,isolatingthecamera-frame
deltaposerepresentationasthesolealignmentdesignretainedinthiscomparison.
34

Velocity Field
(1) Layer-wise self attention
| ... ... | ... |            |     |     |     | ... |     |
| ------- | --- | ---------- | --- | --- | --- | --- | --- |
| Qwen-VL |     | Layer-wise |     | DiT |     |     |     |
hidden state
fusion V/L/A self attention with block attention mask
| ... ... | ... |     | ... ... | ... |     | ... |     |
| ------- | --- | --- | ------- | --- | --- | --- | --- |
>>>>>>
Replicate
| Vision                        | Language |     | Vision | Language | State & noisy actions |                |     |
| ----------------------------- | -------- | --- | ------ | -------- | --------------------- | -------------- | --- |
| (2) Last-layer self attention |          |     |        |          |                       | Velocity Field |     |
| ... ...                       | ...      |     |        |          |                       | ...            |     |
Last-layer
| Qwen-VL |     | hidden state  |     | DiT |     |     |     |
| ------- | --- | ------------- | --- | --- | --- | --- | --- |
as DiT inputs
V/L/A self attention with block attention mask
| ... ...                        | ...      |     | ... ... | ...            |                       | ... |     |
| ------------------------------ | -------- | --- | ------- | -------------- | --------------------- | --- | --- |
| Vision                         | Language |     | Vision  | Language       | State & noisy actions |     |     |
| (3) Last-layer cross attention |          |     |         | Velocity Field |                       |     |     |
| ... ...                        | ...      |     |         | ...            |                       |     |     |
Last-layer
hidden state
as KV
| Qwen-VL |     |     | DiT |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- |
Q/A cross attend to V/L, Q/A self attend to each other
| ... ...   | ...                                       |     |                               | ... |     |     |     |
| --------- | ----------------------------------------- | --- | ----------------------------- | --- | --- | --- | --- |
| Vision    | Language                                  |     | Queries State & noisy actions |     |     |     |     |
| Figure20: | Ablationstudyofmodelarchitecturevariants. |     |                               |     |     |     |     |
Table19: EvaluationonLIBERO-Plusfordifferentnetworkarchitecturevariants.
|     | Camera | Robot | Language Light | Background | Noise | Layout | Total |
| --- | ------ | ----- | -------------- | ---------- | ----- | ------ | ----- |
layer-wiseselfattention 74.5 74.3 86.8 98.6 96.0 94.9 86.1 86.4
last-layerselfattention 75.5 71.4 87.2 98.3 98.9 96.1 88.1 87.0
last-layercrossattention 76.9 73.4 86.9 98.9 97.7 97.3 87.3 87.5
The results are presented in Table 19. On LIBERO-Plus, the third variant (last-layer cross-attention)
achievesthehighestaveragesuccessrate(87.5%)whileincurringthelowestcomputationalcost,asit
avoidsbothper-layerfeaturefusionandstoringthefullsetofVLMvision-languagetokensintheDiT.
Thepureself-attentionarchitectures,whetherwithper-layerorlast-layerfusion,donotexhibitaclear
advantageforvision-language-actionfeatureinteraction. Wethereforeadoptthethirdarchitectureinall
subsequentexperiments.
6.5 NewFeaturesafterAlignment
6.5.1 Post-trainwithVLDataandVLADatainPre-trainingRecipe
Setting 1: Post-training with VL data co-training. In our main experiments, to match the standard
fine-tuningsetting,VLdataisusedonlyduringpre-trainingandexcludedfrompost-training. Here,we
furtherinvestigatewhetherincorporatingVLdataintothepost-trainingstagecanimprovegeneralization.
AsshowninTable18(see“-withVLdatainpost-training”),addingVLdataduringpost-trainingleads
to improved performance on several benchmarks. In particular, it improves LIBERO-Plus from 90.1
to91.4,RoboTwin-Clean2Rand(easy)from73.2to74.0,andRoboTwin-IFfrom71.6to73.1,whilethe
performanceonRoboTwin-Clean2Rand(hard)remainsnearlyunchanged(62.6vs.62.5). Theseresults
suggestthatpost-trainingwithVLdataisparticularlyhelpfulforout-of-distributiongeneralization.
Acloseranalysisshowsthatthegainismostevidentonlanguage-relatedgeneralizationbenchmarks. For
example, on LIBERO-Plus, the success rate under language perturbations increases from 86.9% for
QWEN-ROBOTMANIPto93.9%whenVLdataisincludedduringpost-training.Similarly,onRoboTwin-IF,
35

80
75
70
65
60
55
50
45
40
35 10k 30k 50k 70k 90k
Training Steps
)%(
etaR
sseccuS
80
70
60
50
40
30
20
10 Pi0.5 + VLM Data Cotrain
Ours + VLM Data + Pretrain VLA Data Cotrain
0 Qwen-RobotManip Qwen-RobotManip Qwen-RobotManip Qwen-RobotManip
w/o UnifiedEEF w/o UnifiedEEF + mixed pretrain + mixed pretrain
Figure21: Performancecomparisonunderdiffer-
entproportionsoftrainingdatainRoboTwin-IF.
Wereportthescoreat10k,30k,50k,70k,and90k
trainingsteps. Comparedwiththebaselinepi05,
ourmethodbenefitsfromincorporatingVLMdata
andfurtherimproveswhenco-trainingwithboth
VLMdataandVLApretrainingdata.
)%(
etaR
sseccuS
egarevA
75.8
71.6
35.0
0.0
Figure 22: Instruction-following success rates
across configurations. The chart highlights the
criticalnecessityoftheUnifiedEEFmodule,show-
ingseveredegradationwithoutit(35.0%)andtotal
failure when combined with mixed pretraining
(0.0%). Theoptimalconfigurationutilizesboththe
basearchitectureandmixedpretraining(75.8%).
post-trainingwithVLdataimprovesthesuccessratefrom76%to81%onthe“Pick-Diverse-Object”suite.
Incontrast, RoboTwin-Clean2Rand(hard)keepstheinstructionsfixedandinsteadintroducesvisual
distractors,backgroundchanges,andlightingvariations,sothebenefitofVLdataislesspronouncedin
thissetting.
We attribute these improvements to better preservation of the base VLM’s foundational capabilities.
Fine-tuningsolelyonactionpredictioncanerodethepretrainedVLM’slanguageunderstandingand
visualgroundingabilitiesduetocatastrophicforgetting,therebyweakeningitscapacitytointerpretnovel
instructionsattesttime. Incontrast,mixingVLdataintopost-traininghelpsmaintainthesecapabilities,
enablingthemodeltobetterparseunseeninstructions,groundreferringexpressionstovisualentities,
andtranslatelinguisticintentintoappropriateactions.
Setting2:Post-trainingwithVLandauxiliaryVLAdataco-training.WhentransferringVLAmodelstoa
specificdownstreamdomainviapost-trainingsuchasanovelsimulationenvironment,robotembodiment,
or operational scene—it is standard practice to rely exclusively on clean, domain-specific datasets.
However,thisparadigmintroducesaprominentbottleneckinVLAadaptation:severedomainoverfitting.
Inmostscenarios,ratherthanacquiringgenuine,generalizableinstruction-followingcapabilities,the
model essentially memorizes the specific scene dynamics. Leveraging our proposed unified action
spacerepresentation,weintroduceamixedpost-trainingstrategytosystematicallyenhancethemodel’s
generalizationcapacitywithinthetargetdomain. Specifically,duringthecurationofthepost-training
dataset,weaugmentthetarget-domaindatabyintegratingamixtureofgeneralVision-Language(VL)
dataandpre-trainingVLAdata. Crucially,thismixed-dataapproacheffectivelymitigatesoverfitting
withoutcompromisingthemodel’slow-levelphysicalexecutionproficiencyinthetargetdomain.
Specifically, our augmented dataset comprises two primary categories. The first consists of Vision-
Language (VL) data, predominantly derived from standard Vision-Language Model (VLM) training
corpora,encompassingtaskssuchasobjectdetection,spatialpointing,andtrajectoryprediction. The
secondcategoryentailsVLAdata, whichaggregatestrajectoriesfromauxiliarysimulatorsalongside
large-scale,real-worlddemonstrationsfrommorphologicallysimilarembodiments. Tofacilitateeffective
cross-embodimenttransfer,wealignandoptimizethisauxiliaryVLAdatawithinthehighlytransferable
end-effector(EEF)actionspace.
WeevaluateourapproachonRoboTwin-IF,theOut-of-Distributionbenchmarkwithinourtargetdomain,
RoboTwin. AsshowninFigure21,whenfine-tuningexclusivelyonthedomain-specificRoboTwin-Clean
dataset,ourmodelinitiallyachievesperformancethatsignificantlysurpassesthatofπ . However,as
0.5
thenumberoftrainingstepsincreases,severeoverfittingemerges,leadingtoaprogressiveperformance
decayontheRoboTwin-IFevaluation.ByintegratingVLdata(accountingfor10%ofthetrainingmixture),
boththeinstabilityofthepeakperformanceandthesubsequentdegradationaresubstantiallymitigated.
Furthermore,whenweexpandthemixturetoincludetheauxiliaryVLAdata(comprising75%ofthetotal
vladatainthetrainingmixture),theoverfittingphenomenonisentirelyeradicated. Notably,astraining
progresses, the model’s performance on RoboTwin-IF exhibits continuous improvement rather than
decay,ultimatelyachievingcomparablepeakperformancewhilemaintainingrobustOODgeneralization.
36

Table20: Systematicadvantagesofcamera-framedeltaEEFacrossthreeevaluationdimensions,pro-
gressingfromin-distributiontozero-shotsettings.
Dimension Evaluation Bestbaseline QWEN-ROBOTMANIP Gain
EEFcontrolquality RT-C2REasy/Hard(eefmode) 49.0/33.0(w/oUnifiedEEF) 72.5/56.6 +23.5/+23.6
Skillcomposition CobotMagic→ARX,4noveltasks 12.5%(w/oUnifiedEEF) 55.0% 4.4×
Zero-shottransfer AgileX→ARX,UR5,Franka(avg) 14.5%(joint) 23.9%(eef) 1.65×
Besides, as shown in Figure 22, the most critical insight is that the UnifiedEEF module serves as the
exclusiveprerequisiteformixedpost-training. Whilesimplyremovingthemoduledegradesbaseline
performance(from71.6%to35.0%),attemptingtointroducemixedpost-trainingdatawithoutittriggers
acompleterepresentationcollapse(0.0%successrate). Thiscatastrophicfailurefundamentallyproves
thatthemodelisentirelyincapableofassimilatingmixedVLM/VLAdataonitsown. Itisonlythrough
thestructuralalignmentprovidedbyUnifiedEEFthatthearchitecturecanunlockthebenefitsofmixed
post-training,successfullypushingtheperformanceceilingto75.8%.
6.5.2 EEFcontrol&Cross-EmbodimentTransfer
Camera-framedeltaEEFexpressesactionsasposedeltasinthevisualobservationcoordinatesystem,
makingtheactionrepresentationinherentlysharedacrossembodimentsregardlessoftheirunderlying
kinematics. Weevaluatethisdesignalongthreecomplementarydimensions—in-distributioncontrol
quality,compositionalskilltransfer,andzero-shotcross-embodimentgeneralization—andconsolidate
thekeyresultsinTable20.
In-distributionEEFcontrol. AsthefirstrowofTable20shows,QWEN-ROBOTMANIPwithcamera-frame
EEF achieves 72.5% / 56.6% on RoboTwin-C2R Easy / Hard under EEF-mode execution, compared
with49.0%/33.0%forthebestalternativeaction-spacedesign(QWEN-ROBOTMANIPw/oUnifiedEEF).
Morenotably,QWEN-ROBOTMANIPistheonlyvariantwhereEEF-modeexecutionsurpassesitsown
joint-modeperformance(72.5%vs.68.1%Easy,56.6%vs.50.2%Hard,seeFigure19);allotheraction-space
designsdegradewhenswitchingfromjointtoEEFcontrol. Thisreversalindicatesthatcamera-frame
alignment produces a genuinely strong EEF-space policy rather than merely an alternative control
interface. Experiments for data scaling (Figure 18) corroborates this finding: under the unified EEF
representation,cross-embodimentdatafollowsacleanlog-linearscalinglaw,whereastheablatedmethod
yieldsanerraticcurvewithsubstantiallyhigherpredictionerror.
Compositional skill transfer. Camera-frame EEF decouples manipulation skills from robot-specific
kinematics,enablingskill-levelcompositionacrossembodiment–taskcombinations. Inajoint-training
experimentwith6KCobotMagicand130ARXdemonstrations,thepolicyisevaluatedonfournovel
ARXtasksforwhichzerotarget-taskdemonstrationsexist. AsthesecondrowofTable20shows,QWEN-
ROBOTMANIPachieves55.0%—4.4×thebestablatedvariant(QWEN-ROBOTMANIPw/oUnifiedEEF,
12.5%)—while QWEN-ROBOTMANIP w/o UnifiedSpace manages only 7.5%. Because camera-frame
deltasmapthesamemanipulationprimitivetoaconsistentnumericalpatternregardlessoftheexecuting
robot, the model acquires embodiment-agnostic skill representations that compose freely with new
embodiment–taskpairings(per-taskbreakdowninTable13).
Zero-shotcross-embodimenttransfer. Themostdemandingtestdeploysapolicytrainedexclusivelyon
AgileXtothreeunseenembodiments—ARX,UR5,andFranka—withoutanytarget-embodimentdata.
AsthethirdrowofTable20shows,EEFcontrolachievesanaveragesuccessrateof23.9%,farexceeding
the14.5%ofjointcontrol. TheimprovementisespeciallypronouncedonUR5,whereEEFmodereaches
22.8%versus4.1%forjointmode(5.6×). Joint-spaceactionsareinherentlyrobot-specificandproduce
near-randombehavioronunseenmorphologies,whereascamera-framedeltasabstractawaykinematic
differencesandenablemeaningfultransferinsharedCartesianspace(per-embodimentresultsinTable9).
Takentogether,thethreerowsofTable20revealacoherentprogression: camera-framedeltaEEFfirst
strengthensin-distributionEEFcontrol,thenenablescross-embodimentskillcomposition,andfinally
supportszero-shotdeploymentonunseenrobots—confirmingthatitprovidesanembodiment-agnostic
actioninterfacewhosebenefitscompoundacrossincreasinglychallengingtransfersettings.
37

7 Conclusion
This report set out to investigate whether the scaling recipe behind large language and multimodal
models,aligningheterogeneousdataunderaunifiedformulationandtrainingatscale,canbeapplied
to robotic manipulation to achieve genuine generalization. We present QWEN-ROBOTMANIP as an
affirmative answer, built on the principle that alignment and scale are not independent engineering
challengesbuttightlycoupledprerequisites: withoutaunifiedcross-embodimentformulation,scaling
dataproducesconflictsratherthansynergy;withoutsufficientdatadiversity,evenawell-alignedmodel
cannotgeneralizebeyonditstrainingdistribution.
Severalfindingsfromthisworkcarryimplicationsbeyondthespecificsystemwedescribe. First,the
unifiedalignmentframework,spanningacanonicalstate-actionrepresentation,camera-framedeltapose
parameterization,andin-contextpolicyadaptation,provescriticalnotmerelyforaccommodatingdiverse
embodimentsbutforenablingdatascalingitself. Ourablationsshowthatnaïverepresentationsfailto
exhibitscalingbehavior;alignmentiswhatconvertsadditionaldatavolumeintoimprovedcapability.
Second,thefactthat QWEN-ROBOTMANIP constructsa∼38,100-hourcorpusandachievesemergent
generalizationcapabilitiesusingonlyopen-sourceroboticmanipulationdatasetsandegocentrichuman
videos,withoutanyproprietarydatacollection,suggeststhatthedatabarrierformanipulationfoundation
modelsmaybelowerthancommonlyassumed,providedtherightsynthesisandcurationinfrastructure
isinplace. Third, oursystematiccomparisonbetweenin-domainandout-of-distributionevaluation
revealsthatstandardbenchmarksconsistentlyfailtodistinguishmodelswhosepretrainingcontributes
genuinegeneralizablestructurefromthosethatsucceedthroughin-distributionpatternmatching. We
believetheOODevaluationsettingsintroducedinthisworkprovideamorefaithfulmeasureofrobotic
foundationmodelcapability,andwehopetheyserveasusefuldiagnosticsforthecommunity.
Limitationsremain.Thehuman-to-robotsynthesispipeline,whilescalable,introducesdistributionalgaps
fromretargetingapproximationsandinpaintingartifactsthatboundtheeffectivequalityofsynthesized
data. OurOODevaluations,thoughsubstantiallymorechallengingthanstandardbenchmarks,arestill
predominantlysimulation-based. Broaderreal-worldevaluationacrossdeploymentconditionsisneeded.
Thefixedactionchunklengthandinferencelatencyofthecurrentsystemalsoconstrainapplicabilityto
tasksrequiringreactivesub-secondcontrol.
Lookingforward,thealignment-then-scaleparadigmdemonstratedherenaturallyextendsinseveral
directions:incorporatingmorerobotmorphologiesandtaskdomainsintothepretrainingcorpus,improv-
ingsynthesisfidelitythroughmoreaccuratehand-robotretargetingandphysicallygroundedrendering,
andincorporatingagenticsystemstowardlonger-horizonreasoningandmanipulation. Moreover,we
hopethisworkcontributestoashiftinhowthecommunityevaluatesVLAmodels, fromin-domain
benchmark rank toward the out-of-distribution generalization that ultimately determines whether a
modelcanserveasagenuinefoundationforreal-worlddeployment.
8 Authors
Core Contributors: Haoqi Yuan∗, Zhixuan Liang∗, Anzhe Chen∗, Ye Wang∗, Haoyang Li∗, Pei Lin∗,
Yiyang Huang∗, Zixing Lei∗, Tong Zhang∗, Jiazhao Zhang, Jie Zhang, Jingyang Fan, Gengze Zhou,
QihangPeng,ChenxuLv,XiaoyueChen,AnYang,FeiHuang,JunyangLin,DayihengLiu,JingrenZhou,
ChenfeiWu†,Xiong-HuiChen‡†
∗EqualContribution. † CorrespondingAuthor. ‡ ProjectLead.
Contributors: JinhuiYe,SichengXie,HaleYin,XudongGuo,ShuaiBai,LuluHu,MinyingZhang,Shurui
Li,WenhuXiao,YueWang,KunYan,XiaoXu,JiahaoLi,XuanchengRen
Acknowledgments: WeacknowledgetheNationalPilotBaseforEmbodiedIntelligenceApplicationsfor
providingthereal-robotexperimentalenvironmentandequipment. WethankAgileXRoboticsfortheir
hardwaresupport. WealsothankProf. HaoDongandProf. YaoMufortheirsupport.
38

References
AgiBot-World-Contributors. AgiBotWorldColosseo: Alarge-scalemanipulationplatformforscalable
andintelligentembodiedsystems. arXivpreprintarXiv:2503.06669,2025.
ShuaiBai,YuxuanCai,RuizheChen,KeqinChen,XionghuiChen,ZesenCheng,LianghaoDeng,Wei
Ding,ChangGao,ChunjiangGe,etal. Qwen3-vltechnicalreport. arXivpreprintarXiv:2511.21631,2025.
JohanBjorck,FernandoCastaneda,LinxiFan,DieterFox,etal. GR00TN1: Anopenfoundationmodel
forgeneralisthumanoidrobots. arXivpreprintarXiv:2503.14734,2025.
KevinBlack, NoahBrown, DannyDriess, AdnanEsmail, MichaelEqui, ChelseaFinn, NiccoloFusai,
LachyGroom,KarolHausman,BrianIchter,etal. π : Avision-language-actionflowmodelforgeneral
0
robotcontrol. arXivpreprintarXiv:2410.24164,2024.
Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail,
MichaelRobertEqui,ChelseaFinn,NiccoloFusai,ManuelYGalliker,etal. π : avision-language-
0.5
actionmodelwithopen-worldgeneralization. In9thAnnualConferenceonRobotLearning,2025.
KevinBlack,ManuelGalliker,andSergeyLevine. Real-timeexecutionofactionchunkingflowpolicies.
AdvancesinNeuralInformationProcessingSystems,38:33383–33407,2026.
TomBrown,BenjaminMann,NickRyder,MelanieSubbiah,JaredDKaplan,PrafullaDhariwal,Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot
learners. InNeurIPS,2020.
JunhaoCai,ZetaoCai,JiafeiCao,YilunChen,ZeyuHe,LeiJiang,HangLi,HengjieLi,YangLi,YufeiLiu,
etal. Internvla-a1: Unifyingunderstanding,generationandactionforroboticmanipulation. arXiv
preprintarXiv:2601.02456,2026.
NicolasCarion,LauraGustafson,Yuan-TingHu,ShoubhikDebnath,RonghangHu,DidacSuris,Chai-
tanyaRyali,KalyanVasudevAlwala,HaithamKhedr,AndrewHuang,JieLei,TengyuMa,Baishan
Guo,ArpitKalla,MarkusMarks,JosephGreer,MengWang,PeizeSun,RomanRädle,Triantafyllos
Afouras,EffrosyniMavroudi,KatherineXu,Tsung-HanWu,YuZhou,LilianeMomeni,RishiHazra,
ShuangruiDing,SagarVaze,FrancoisPorcher,FengLi,SiyuanLi,AishwaryaKamath,HoKeiCheng,
Piotr Dollár, Nikhila Ravi, Kate Saenko, Pengchuan Zhang, and Christoph Feichtenhofer. Sam 3:
Segmentanythingwithconcepts,2025. URLhttps://arxiv.org/abs/2511.16719.
JustinCarpentier,GuilhemSaurel,GabrieleBuondonno,JosephMirabel,FlorentLamiraux,OlivierStasse,
andNicolasMansard. ThePinocchioC++library: Afastandflexibleimplementationofrigidbody
dynamicsalgorithmsandtheiranalyticalderivatives. InIEEE/SICEInternationalSymposiumonSystem
Integration(SII),pp.614–619.IEEE,2019.
AnzheChen,YifeiYang,ZhenjieZhu,KechunXu,ZhongxiangZhou,RongXiong,andYueWang.Toward
embodimentequivariantvision-language-actionpolicy. arXivpreprintarXiv:2509.14630,2025a.
TianxingChen,ZanxinChen,BaijunChen,ZijianCai,YibinLiu,ZixuanLi,QiweiLiang,XianliangLin,
YihengGe,ZhenyuGu,etal. Robotwin2.0: Ascalabledatageneratorandbenchmarkwithstrong
domain randomization for robust bimanual robotic manipulation. arXiv preprint arXiv:2506.18088,
2025b.
WilliamChen,SuneelBelkhale,SuvirMirchandani,OierMees,DannyDriess,KarlPertsch,andSergey
Levine. Trainingstrategiesforefficientembodiedreasoning. ArXiv,abs/2505.08243,2025c.
ChengChi,SiyuanFeng,YilunDu,ZhenjiaXu,EricCousineau,BenjaminBurchfiel,andShuranSong.
Diffusionpolicy: Visuomotorpolicylearningviaactiondiffusion. InRobotics: ScienceandSystems(RSS),
2023.
StarVLACommunity. Starvla: Alego-likecodebaseforvision-language-actionmodeldeveloping. arXiv
preprintarXiv:2604.05014,2026.
Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Sanja Fidler, Antonino Furnari, Evangelos
Kazakos, DavideMoltisanti, JonathanMunro, TobyPerrett, WillPrice, andMichaelWray. Scaling
egocentricvision: TheEPIC-KITCHENSdataset. InEuropeanConferenceonComputerVision(ECCV),
2018.
39

TimothéeDarcet,MaximeOquab,JulienMairal,andPiotrBojanowski. Visiontransformersneedregisters.
InB.Kim,Y.Yue,S.Chaudhuri,K.Fragkiadaki,M.Khan,andY.Sun(eds.),InternationalConference
onLearningRepresentations,volume2024,pp.2632–2652,2024. URLhttps://proceedings.iclr.cc/
paper_files/paper/2024/file/0b408293619f725fd30162af057e531a-Paper-Conference.pdf.
MattDeitke,ChristopherClark,SanghoLee,RohunTripathi,YueYang,JaeSungPark,Mohammadreza
Salehi,NiklasMuennighoff,KyleLo,LucaSoldaini,JiasenLu,TairaAnderson,ErinBransom,Kiana
Ehsani,HuongNgo,Yen-SungChen,AjayPatel,MarkYatskar,ChrisCallison-Burch,AndrewHead,
RoseHendrix,FavyenBastani,EliVanderBilt,NathanLambert,YvonneChou,ArnaviChheda,Jenna
Sparks,SamSkjonsberg,MichaelSchmitz,AaronSarnat,ByronBischoff,PeteWalsh,ChrisNewell,
PiperWolters,TanmayGupta,Kuo-HaoZeng,JonBorchardt,DirkGroeneveld,CrystalNam,Sophie
Lebrecht,CaitlinWittlif,CarissaSchoenick,OscarMichel,RanjayKrishna,LucaWeihs,NoahA.Smith,
HannanehHajishirzi,RossB.Girshick,AliFarhadi,andAniruddhaKembhavi. Molmoandpixmo:
Openweightsandopendataforstate-of-the-artvision-languagemodels. InIEEE/CVFConferenceon
ComputerVisionandPatternRecognition,CVPR2025,Nashville,TN,USA,June11-15,2025,2025.
DannyDriess,JostTobiasSpringenberg,BrianIchter,LiliYu,AdrianLi-Bell,KarlPertsch,AllenZRen,
HomerWalke,QuanVuong,LucyXiaoyangShi,etal. Knowledgeinsulatingvision-language-action
models: Trainfast,runfast,generalizebetter. arXivpreprintarXiv:2505.23705,2025.
Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models.
arXiv:2407.21783,2024.
PatrickEsser,SumithKulal,AndreasBlattmann,RahimEntezari,JonasMüller,HarrySaini,YamLevi,
Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers for high-
resolutionimagesynthesis. InICML,2024.
Hao-ShuFang, HongjieFang, ZhenyuTang, JirongLiu, ChenxiWang, JunboWang, HaoyiZhu, and
CewuLu. RH20T:Acomprehensiveroboticdatasetforlearningdiverseskillsinone-shot. InIEEE
InternationalConferenceonRoboticsandAutomation(ICRA),2024.
HaoquanFang,JiafeiDuan,DonovanClay,SamWang,ShuoLiu,WeikaiHuang,XiangFan,Wei-Chuan
Tsai,ShiruiChen,YiRuWang,etal. Molmoact2: Actionreasoningmodelsforreal-worlddeployment.
arXivpreprintarXiv:2605.02881,2026.
SenyuFei,SiyinWang,JunhaoShi,ZihaoDai,JikunCai,PengfangQian,LiJi,XinzheHe,ShiduoZhang,
ZhaoyeFei,etal. Libero-plus: In-depthrobustnessanalysisofvision-language-actionmodels. arXiv
preprintarXiv:2510.13626,2025.
YouheFeng,HansenShi,HaoyangLi,XinleiGuo,YangWang,ChengyangZhang,JinkaiZhang,Xiaohan
Zhang,JieTang,andJingZhang. Procvlm: Learningprocedure-groundedprogressrewardsforrobotic
manipulation. CoRR,abs/2605.08774,2026.
GalaxeaAI. Galaxeaopen-worlddatasetandG0dual-systemVLAmodel. arXivpreprintarXiv:2509.00576,
2025.
Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, JoannaMaterzynska, Susanne Westphal,
HeunaKim,ValentinHaenel,IngoFruend,PeterYianilos,MoritzMueller-Freitag,etal.The"something
something"videodatabaseforlearningandevaluatingvisualcommonsense. InProceedingsoftheIEEE
internationalconferenceoncomputervision,pp.5842–5850,2017.
KristenGrauman,AndrewWestbury,EugeneByrne,etal. Ego4D:Aroundtheworldin3,000hoursof
egocentricvideo. InIEEE/CVFConferenceonComputerVisionandPatternRecognition(CVPR),2022.
KristenGrauman,AndrewWestbury,LorenzoTorresani,KrisKitani,JitendraMalik,TriantafyllosAfouras,
KumarAshutosh,VijayBaiyya,SiddhantBansal,BikramBoote,etal.Ego-exo4d:Understandingskilled
humanactivityfromfirst-andthird-personperspectives. InProceedingsoftheIEEE/CVFConferenceon
ComputerVisionandPatternRecognition,pp.19383–19400,2024.
ByeonghoHeo,SongPark,DongyoonHan,andSangdooYun. Rotarypositionembeddingforvision
transformer. InEuropeanConferenceonComputerVision,pp.289–305.Springer,2024.
Ryan Hoque, Peide Huang, David J Yoon, Mouli Sivapurapu, and Jian Zhang. Egodex: Learning
dexterousmanipulationfromlarge-scaleegocentricvideo. arXivpreprintarXiv:2505.11709,2025.
40

Yiyang Huang, Yuhui Hao, Bo Yu, Feng Yan, Yuxin Yang, Feng Min, Yinhe Han, Lin Ma, Shaoshan
Liu,QiangLiu,etal. Dadu-corki: Algorithm-architectureco-designforembodiedai-poweredrobotic
manipulation. InProceedingsofthe52ndAnnualInternationalSymposiumonComputerArchitecture,pp.
327–343,2025.
SimarKareer,DhruvPatel,RyanPunamiya,PranayMathur,ShuoCheng,ChenWang,JudyHoffman,
andDanfeiXu. Egomimic: Scalingimitationlearningviaegocentricvideo. In2025IEEEInternational
ConferenceonRoboticsandAutomation(ICRA),pp.13226–13233.IEEE,2025.
AlexanderKhazatsky,KarlPertsch,SurajNair,etal.DROID:Alarge-scalein-the-wildrobotmanipulation
dataset. InRobotics: ScienceandSystems(RSS),2024.
DongyoungKim,HuiwonJang,MyungkyuKoo,SuhyeokJang,TaeyoungKim,BeomjunKim,Byungjun
Yoon, Changsung Jang, Daewon Choi, Dongsu Han, et al. Rldx-1 technical report. arXiv preprint
arXiv:2605.03269,2026a.
Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael
Rafailov,EthanFoster,GraceLam,PannagSanketi,etal. Openvla: Anopen-sourcevision-language-
actionmodel. arXivpreprintarXiv:2406.09246,2024.
MooJinKim,ChelseaFinn,andPercyLiang. Fine-tuningvision-language-actionmodels: Optimizing
speedandsuccess. arXivpreprintarXiv:2502.19645,2025.
MooJinKim,YihuaiGao,Tsung-YiLin,Yen-ChenLin,YunhaoGe,GraceLam,PercyLiang,ShuranSong,
Ming-YuLiu,ChelseaFinn,etal. Cosmospolicy: Fine-tuningvideomodelsforvisuomotorcontroland
planning. arXivpreprintarXiv:2601.16163,2026b.
XinKong,ShikunLiu,XiaoyangLyu,MarwanTaher,XiaojuanQi,andAndrewJ.Davison. EscherNet: A
generativemodelforscalableviewsynthesis. InProceedingsoftheIEEE/CVFConferenceonComputer
VisionandPatternRecognition(CVPR),pp.9503–9513,2024.
Shanghai AI Laboratory. Ebench: Elemental mobile manipulation benchmark, 2026. URL https://
internrobotics.github.io/EBench-doc/.
ZixingLei,ChangxingLiu,YichenXiong,MinhaoXiong,YuanzhuoDing,ZhipengZhang,WeixinLi,
andSihengChen. Towardslong-horizonembodiedagentswithtool-alignedvision-language-action
models. arXivpreprintarXiv:2605.13119,2026.
MarionLepert,JiayingFang,andJeannetteBohg. Masquerade: Learningfromin-the-wildhumanvideos
usingdata-editing. arXivpreprintarXiv:2508.09976,2025a.
MarionLepert,JiayingFang,andJeannetteBohg. Phantom: Trainingrobotswithoutrobotsusingonly
humanvideos. arXivpreprintarXiv:2503.00779,2025b.
HaoLi,ZiqinWang,Zi-HanDing,ShuaiYang,YilunChen,YangTian,XiaolinHu,TaiWang,Dahua
Lin,FengZhao,SiLiu,andJiangmiaoPang. Robointer: Aholisticintermediaterepresentationsuite
towardsroboticmanipulation. CoRR,abs/2602.09973,2026.
QixiuLi,YuDeng,YaoboLiang,LinLuo,LeiZhou,ChengtangYao,LingqiZeng,ZhiyuanFeng,Huizhi
Liang,SichengXu,etal. Scalablevision-language-actionmodelpretrainingforroboticmanipulation
withreal-lifehumanactivityvideos. arXivpreprintarXiv:2510.21571,2025a.
RuilongLi,BrentYi,JunchenLiu,HangGao,YiMa,andAngjooKanazawa.Camerasasrelativepositional
encoding. AdvancesinNeuralInformationProcessingSystems,2025b.
Zhixuan Liang, Yao Mu, Mingyu Ding, Fei Ni, Masayoshi Tomizuka, and Ping Luo. Adaptdiffuser:
diffusionmodelsasadaptiveself-evolvingplanners. InProceedingsofthe40thInternationalConference
onMachineLearning,pp.20725–20745,2023.
ZhixuanLiang,YizhuoLi,TianshuoYang,ChengyueWu,SitongMao,LiuaoPei,TianNian,Shunbo
Zhou, XiaokangYang, JiangmiaoPang, etal. Discretediffusionvla: Bringingdiscretediffusionto
actiondecodinginvision-language-actionpolicies. InProceedingsofthe43rdInternationalConferenceon
MachineLearning,2026.
HaotongLin,SiliChen,JunhaoLiew,DonnyYChen,ZhenyuLi,GuangShi,JiashiFeng,andBingyi
Kang. Depthanything3: Recoveringthevisualspacefromanyviews. arXivpreprintarXiv:2511.10647,
2025.
41

YaronLipman,RickyT.Q.Chen,HeliBen-Hamu,MaximilianNickel,andMattLe. Flowmatchingfor
generativemodeling. InInternationalConferenceonLearningRepresentations(ICLR),2023.
BoLiu,YifengZhu,ChongkaiGao,YihaoFeng,QiangLiu,YukeZhu,andPeterStone. Libero: Bench-
markingknowledgetransferforlifelongrobotlearning. arXivpreprintarXiv:2306.03310,2023.
SongmingLiu, LingxuanWu, BangguoLi, HengkaiTan, HuayuChen, ZhengyiWang, KeXu, Hang
Su,andJunZhu. RDT-1B:adiffusionfoundationmodelforbimanualmanipulation. InInternational
ConferenceonLearningRepresentations(ICLR),2025.
HaoLuo,YichengFeng,WanpengZhang,SipengZheng,YeWang,HaoqiYuan,JiazhengLiu,Chaoyi
Xu,QinJin,andZongqingLu. Being-h0: vision-language-actionpretrainingfromlarge-scalehuman
videos. arXivpreprintarXiv:2507.15597,2025.
Hao Luo, Ye Wang, Wanpeng Zhang, Haoqi Yuan, Yicheng Feng, Haiweng Xu, Sipeng Zheng, and
ZongqingLu. Joint-alignedlatentaction: Towardsscalablevlapretraininginthewild. InProceedingsof
theIEEE/CVFConferenceonComputerVisionandPatternRecognition,pp.35047–35058,2026a.
HaoLuo,YeWang,WanpengZhang,SipengZheng,ZihengXi,ChaoyiXu,HaiwengXu,HaoqiYuan,Chi
Zhang,YiqingWang,etal. Being-h0.5: Scalinghuman-centricrobotlearningforcross-embodiment
generalization. arXivpreprintarXiv:2601.12993,2026b.
HaoLuo,WanpengZhang,YichengFeng,SipengZheng,HaiwengXu,ChaoyiXu,ZihengXi,YuhuiFu,
andZongqingLu. Being-h0.7: Alatentworld-actionmodelfromegocentricvideos. arXivpreprint
arXiv:2605.00078,2026c.
JiangranLyu,KaiLiu,XuhengZhang,HaoranLiao,YusenFeng,WenxuanZhu,TingruiShen,JiayiChen,
JiazhaoZhang,YifeiDong,etal. Lda-1b: Scalinglatentdynamicsactionmodelviauniversalembodied
dataingestion. arXivpreprintarXiv:2602.12215,2026.
TakeruMiyato,BernhardJaeger,MaxWelling,andAndreasGeiger. GTA:Ageometry-awareattention
mechanismformulti-viewtransformers. InInternationalConferenceonLearningRepresentations(ICLR),
2024.
YaoMu,TianxingChen,ZanDing,etal. Robotwin: Dual-armrobotbenchmarkwithgenerativedigital
twins. arXivpreprintarXiv:2501.00062,2025.
SoroushNasiriany,AbhiramMaddukuri,LanceZhang,AdeetParikh,AaronLo,AbhishekJoshi,Ajay
Mandlekar,andYukeZhu. Robocasa: Large-scalesimulationofeverydaytasksforgeneralistrobots.
InRobotics: ScienceandSystems(RSS),2024.
SoroushNasiriany,SepehrNasiriany,AbhiramMaddukuri,andYukeZhu. Robocasa365: Alarge-scale
simulationframeworkfortrainingandbenchmarkinggeneralistrobots. InInternationalConferenceon
LearningRepresentations(ICLR),2026.
OpenAI. Gpt-4technicalreport. arXiv:2303.08774,2023.
Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog, Alex Irpan, Alexander
Khazatsky,AnantRai,AnikaitSingh,AnthonyBrohan,etal. OpenX-Embodiment: Roboticlearning
datasetsandRT-Xmodels. InIEEEInternationalConferenceonRoboticsandAutomation(ICRA),2024.
William Peebles and Saining Xie. Scalable diffusion models with transformers. In Proceedings of the
IEEE/CVFInternationalConferenceonComputerVision(ICCV),pp.4195–4205,2023.
RyanPunamiya, SimarKareer, ZeyiLiu, JoshCitron, Ri-ZhaoQiu, XiongyiCai, AlexeyGavryushin,
JiaqiChen,DavideLiconti,LawrenceYZhu,etal. Egoverse: Anegocentrichumandatasetforrobot
learningfromaroundtheworld. arXivpreprintarXiv:2604.07607,2026.
Ri-ZhaoQiu,ShiqiYang,XuxinCheng,ChaitanyaChawla,JialongLi,TairanHe,GeYan,DavidJYoon,
RyanHoque,LarsPaulsen,etal. Humanoidpolicy˜humanpolicy. arXivpreprintarXiv:2503.13441,
2025.
JavierRomero,DimitriosTzionas,andMichaelJBlack. Embodiedhands: Modelingandcapturinghands
andbodiestogether. arXivpreprintarXiv:2201.02610,2022.
AbrahamSavitzkyandMarcelJEGolay. Smoothinganddifferentiationofdatabysimplifiedleastsquares
procedures. Analyticalchemistry,36(8):1627–1639,1964.
42

GeminiTeam,RohanAnil,SebastianBorgeaud,YonghuiWu,Jean-BaptisteAlayrac,JiahuiYu,Radu
Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, et al. Gemini: A family of highly capable
multimodalmodels. arXiv:2312.11805,2023.
QwenTeam. Qwen3.5: Acceleratingproductivitywithnativemultimodalagents,February2026. URL
https://qwen.ai/blog?id=qwen3.5.
YangTian,YuyinYang,YimanXie,ZetaoCai,XuShi,NingGao,HangxuLiu,XuekunJiang,ZheruiQiu,
FengYuan,YapingLi,PingWang,JunhaoCai,JiaZeng,HaoDong,andJiangmiaoPang.InternData-A1:
Pioneeringhigh-fidelitysyntheticdataforpre-traininggeneralistpolicy.arXivpreprintarXiv:2511.16651,
2025.
EmanuelTodorov,TomErez,andYuvalTassa. Mujoco: Aphysicsengineformodel-basedcontrol. In
2012IEEE/RSJinternationalconferenceonintelligentrobotsandsystems,pp.5026–5033.IEEE,2012.
Ye Wang, Sipeng Zheng, Hao Luo, Wanpeng Zhang, Haoqi Yuan, Chaoyi Xu, Haiweng Xu, Yicheng
Feng,MingyangYu,ZhiyuKang,etal. Rethinkingvisual-language-actionmodelscaling: Alignment,
mixture,andregularization. arXivpreprintarXiv:2602.09722,2026.
Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, et al. RoboMIND: Benchmark on multi-
embodiment intelligence normative data for robot manipulation. In Robotics: Science and Systems
(RSS),2025a.
KunWuetal. RoboMIND2.0: Amultimodal,bimanualmobilemanipulationdatasetforgeneralizable
embodiedintelligence. arXivpreprintarXiv:2512.24653,2025b.
ShihanWuetal. RoboCOIN:Anopen-sourcedbimanualroboticdatacollectionforintegratedmanipula-
tion. arXivpreprintarXiv:2511.17441,2025c.
FengYan,FanfanLiu,YiyangHuang,ZechaoGuan,LimingZheng,YufengZhong,ChengjianFeng,and
LinMa. Robotron-mani: All-in-onemultimodallargemodelforroboticmanipulation. InProceedingsof
theIEEE/CVFInternationalConferenceonComputerVision(ICCV),pp.13707–13718,October2025.
AnYang,AnfengLi,BaosongYang,BeichenZhang,BinyuanHui,BoZheng,BowenYu,ChangGao,
ChengenHuang,ChenxuLv,etal. Qwen3technicalreport. arXivpreprintarXiv:2505.09388,2025.
YandanYang,ShuangZeng,TongLin,XinyuanChang,DekangQi,JunjinXiao,HaoyunLiu,Ronghan
Chen,YuzhiChen,DongjieHuo,etal. Abot-m0: Vlafoundationmodelforroboticmanipulationwith
actionmanifoldlearning. arXivpreprintarXiv:2602.11236,2026.
QiyingYu,QuanSun,XiaosongZhang,YufengCui,FanZhang,YueCao,XinlongWang,andJingjing
Liu. Capsfusion: Rethinkingimage-textdataatscale. InIEEE/CVFConferenceonComputerVisionand
PatternRecognition,CVPR2024,Seattle,WA,USA,June16-22,2024,2024.
Wentao Yuan, Jiafei Duan, Valts Blukis, Wilbert Pumacay, Ranjay Krishna, Adithyavairavan Murali,
Arsalan Mousavian, and Dieter Fox. Robopoint: A vision-language model for spatial affordance
predictioninrobotics. InConferenceonRobotLearning,6-9November2024,Munich,Germany,2024.
KevinZakka. Mink: PythoninversekinematicsbasedonMuJoCo,February2026. URLhttps://github.
com/kevinzakka/mink.
Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic
controlviaembodiedchain-of-thoughtreasoning. arXivpreprintarXiv:2407.08693,2024.
Tao Zhang, Song Xia, Ye Wang, and Qin Jin. Easymimic: A low-cost framework for robot imitation
learningfromhumanvideos. arXivpreprintarXiv:2602.11464,2026a.
TianyiZhang, HaonanDuan, HaoranHao, YuQiao, JifengDai, andZhiHou. Groundingactionsin
cameraspace: Observation-centricvision-language-actionpolicy. InProceedingsoftheAAAIConference
onArtificialIntelligence,volume40,pp.18782–18790,2026b.
Zhanguang Zhang, Zhiyuan Li, Behnam Rahmati, Rui Heng Yang, Yintao Ma, Amir Rasouli, Sajjad
Pakdamansavoji, Yangzheng Wu, Lingfeng Zhang, Tongtong Cao, et al. Do world action models
generalizebetterthanvlas? arobustnessstudy. arXivpreprintarXiv:2603.22078,2026c.
TonyZ.Zhao,VikashKumar,SergeyLevine,andChelseaFinn. Learningfine-grainedbimanualmanipu-
lationwithlow-costhardware. InRobotics: ScienceandSystems(RSS),2023.
43

JinliangZheng,JianxiongLi,ZhihaoWang,DongxiuLiu,XiruiKang,YuchunFeng,YinanZheng,Jiayin
Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-embodiment
vision-language-actionmodel. arXivpreprintarXiv:2510.10274,2025.
Ruijie Zheng, Dantong Niu, Yuqi Xie, Jing Wang, Mengda Xu, Yunfan Jiang, Fernando Castañeda,
FengyuanHu,YouLiangTan,LetianFu,etal. Egoscale: Scalingdexterousmanipulationwithdiverse
egocentrichumandata. arXivpreprintarXiv:2602.16710,2026.
EnshenZhou,JingkunAn,ChengChi,YiHan,ShanyuRong,ChiZhang,PengweiWang,Zhongyuan
Wang,Tie-JunHuang,LuSheng,andShanghangZhang. Roborefer: Towardsspatialreferringwith
reasoninginvision-languagemodelsforrobotics. CoRR,abs/2506.04308,2025.
ShangchenZhou,ChongyiLi,KelvinCKChan,andChenChangeLoy. Propainter: Improvingpropa-
gationandtransformerforvideoinpainting. InProceedingsoftheIEEE/CVFinternationalconferenceon
computervision,pp.10477–10486,2023.
YiZhou,ConnellyBarnes,JingwanLu,JimeiYang,andHaoLi. Onthecontinuityofrotationrepresen-
tationsinneuralnetworks. InProceedingsoftheIEEE/CVFConferenceonComputerVisionandPattern
Recognition(CVPR),2019.
44