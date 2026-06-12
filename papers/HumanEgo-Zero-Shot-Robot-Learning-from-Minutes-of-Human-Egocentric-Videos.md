| HumanEgo: |              |     | Zero-Shot   |       |         | Robot            | Learning    |        |     |
| --------- | ------------ | --- | ----------- | ----- | ------- | ---------------- | ----------- | ------ | --- |
| from      | Minutes      |     | of          | Human |         | Egocentric       |             | Videos |     |
|           | Zhi(Leo)Wang |     | BotaoHe     |       | KelinYu |                  | SeungjaeLee |        |     |
|           | RuohanGao    |     | FurongHuang |       |         | YiannisAloimonos |             |        |     |
UniversityofMaryland
https://humanego-ai.github.io/
6202 yaM 82  ]OR.sc[  2v43942.5062:viXra
Fig. 1: HumanEgo learns robot policy from human egocentric videos. A human wears Aria
glasses and collects demonstrations (left); the egocentric videos are converted into an interaction-
centricrepresentationandusedtotrainaflowmatchingpolicy(middle); thepolicytransferszero-
shottotherobot—freeofenvironment,setup,orembodiment(right).
| Abstract: | Human     | egocentric | video | captures     |       | rich manipulation |           | demonstrations |       |
| --------- | --------- | ---------- | ----- | ------------ | ----- | ----------------- | --------- | -------------- | ----- |
| without   | any robot | hardware,  | yet   | transferring | these | skills            | to robots | remains        | chal- |
lengingduetotheembodimentgapbetweenhumanandrobotinbothvisualap-
| pearanceandkinematics. |     |     | WepresentHumanEgo, |     |     | aframeworkthatbridgesthe |     |     |     |
| ---------------------- | --- | --- | ------------------ | --- | --- | ------------------------ | --- | --- | --- |
embodimentgapbyliftingeachhumandemonstrationtoanentity-levelrepresen-
tationofhand–objectinteraction,andtrainingaflowmatchingpolicywithdense
| auxiliaryobjectivesthatamplifysupervisionfromeverytrajectory. |     |                    |     |                 |     |               |     | HumanEgois     |     |
| ------------------------------------------------------------- | --- | ------------------ | --- | --------------- | --- | ------------- | --- | -------------- | --- |
| robot-data-free,                                              |     | hardware-agnostic, |     | data-efficient, |     | and zero-shot |     | human-to-robot |     |
transferable.Withonly30minutesofhumanvideospertask,HumanEgoachieves
| 92.5%                                               | average      | success | across four | real-world    |     | tasks (75% | with              | just 15  | minutes), |
| --------------------------------------------------- | ------------ | ------- | ----------- | ------------- | --- | ---------- | ----------------- | -------- | --------- |
| outperforms                                         | matched-time |         | robot       | teleoperation |     | by 41%,    | and               | robustly | transfers |
| zero-shotacrossnovelrobots,cameras,andenvironments. |              |         |             |               |     |            | WereleaseHumanEgo |          |           |
asaneasy-to-use,open-sourceframeworkforlearningrobotpoliciesdirectlyfrom
| humandata: | https://github.com/TX-Leo/HumanEgo. |     |     |     |     |     |     |     |     |
| ---------- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
1 Introduction
State-of-the-artmanipulationpoliciesrequirehundredstothousandsoftask-specificrobotdemon-
strations [1, 2, 3, 4, 5, 6], which are costly, time-consuming, and inconvenient to collect. Human
egocentricvideooffersamuchcheaperandmoreaccessiblealternative: withahead-mountedcam-
era [7], a single person can collect task demonstrations anywhere, in minutes. But how should
we leverage this data? Existing approaches fall into two paradigms, each with significant limita-
tions. Co-trainingmethods[8,9,10,11]supplementrobotdatawithhumanvideo,butstillrequire
substantialrobotdemonstrationsforeverynewtask—reducing,ratherthaneliminating,thedatabur-
den. Large-scalepretrainingapproaches[12,13,14,15]learnfrommassiveegocentriccorpora,but
demandenormouscomputeandstillrequirerobot-specificpost-trainingtoproducedeployablepoli-
cies.Wepursueamoredirectgoal:learningdeployablemanipulationpoliciesfromonlyminutes
ofhumanegocentricdemonstrations—withoutanyrobotdataandinternet-scalepretraining.
Achievingthisgoalexposestwofundamentalchallenges.(1)Therepresentationchallenge:bridg-
ingtheembodimentgap. Humansandrobotsdifferinbothvisualappearanceandkinematics,and

these gaps demand distinct solutions. On the visual side, retargeting-based methods [16, 17, 18]
synthesize robot-like imagery from human video but are brittle to morphological and viewpoint
differences;point-trackingapproaches[19,20,21]extractsparsegeometricfeaturesbutdiscardthe
richvisualcontextsurroundinginteractions.Onthekinematicside,hierarchicalmethods[22,23,24]
separatehigh-levelplansfromlow-levelexecutionbutstillrequirerobotdataforthelow-levelcon-
troller;object-centricapproaches[25,26,27]trackonlythemanipulatedobject,losingcriticalinfor-
mationabouthowthehandapproaches,grasps,andreleasesit.Wearguethatneitherhandnorobject
alone defines a skill—what matters is their interaction. This is the key representational claim be-
hindHumanEgo:robotsshouldnotimitatethehumanbody,butrecoverthetask-relevantinteraction
geometrythattransfersacrossbodies.
(2)Thelearningchallenge: learningfromminimaldata. Althoughrawhumanvideoisabundant
online, clean clips with precise action labels remain scarce, making data-efficient learning from
minutesofper-taskvideoscritical. Thisregimeintroducestwodistinctchallenges: multi-modality
andsignalsparsity. Forthemulti-modalitychallenge, thesametaskadmitsmanyvalidstrategies.
Diffusion-based methods [3] capture this distribution but need many denoising steps and are slow
at inference; faster alternatives [28] are less expressive. For the signal-sparsity challenge, each
trajectory carries rich signal beyond the hand action—object motion, visual traces, hand–object
state—yet prior work taps only a fraction: single auxiliary targets such as visual foresight [25,
29, 30] or 2D tracks [19, 27, 31], or upstream pretraining corpora [12, 13, 32]. We argue that a
fastgenerativepolicypairedwithmulti-typedensesupervisionisthekeytodata-efficientlearning
from minutes of human egocentric videos. In other words, the goal is to squeeze many forms of
supervisionfromhumanvideo,sosmallcurateddemonstrationscanpunchabovetheirsize.
We present HumanEgo, addressing each gap with a targeted design. For the visual gap, we in-
paint the human arm from each egocentric frame and render a virtual gripper with tracked object
keypoints in its place, producing an embodiment-agnostic visual observation. For the kinematic
gap,weencodeeveryhandandobjectasanInteraction-CentricToken(ICT),producingacompact,
embodiment- and viewpoint-invariant spatial observation of hand–object interaction. For multi-
modality, we adopt a flow matching [33] policy, producing expressive multi-modal actions at fast
inference. Forsignalsparsity,wedesignthreedenseauxiliaryobjectives: 2Dtrace,objectmotion,
andlatentconsistency. Togethertheyproducemulti-typedensesupervisionfromeachtrajectory’s
scenedynamics,boostinglearningfromfewdemonstrations. Ourcontributions:
• HumanEgo, a robot-data-free, hardware-agnostic, and data-efficient pipeline that learns robot
manipulationpoliciesfromminutesofrawhumanegocentricvideos—poweredbyatransferable
interactionrepresentationandaflowmatchingpolicywithdenseauxiliaryobjectives.
• Interaction-CentricTokens(ICT),acompactentity-levelrepresentationofhand–objectinter-
actioninvarianttoembodiment,viewpoint,andenvironment.
• Robustzero-shothuman-to-robottransfer. Trainedon30minutesofhumanvideopertask,
HumanEgo reaches 92.5% success across 4 real-world tasks and 75% at half that budget. At
matched collection time, it surpasses robot teleoperation by 41%. The learned policy also de-
ploys zero-shot to novel robot embodiments, camera setups, lighting, backgrounds, and object
instances,withoutanyretrainingorfine-tuning. Thissuggeststhathumanvideoisnotmerelya
cheapsubstitutebutascalableandpotentiallysuperiordatasourceforpolicylearning.
2 RelatedWork
Recent years have produced rich large-scale egocentric and hand–object interaction datasets [34,
35, 15, 36, 37, 38, 39, 14] that provide the data foundation for learning manipulation from hu-
man video. Building on this foundation, one line of work scales up generalist policies and world
models[12,13,40,41,42]thatlearnembodiment-agnosticrepresentationsfrommassivecorpora,
yet deployment demands enormous compute and per-task robot post-training. Another line co-
trains[8,9,26,43,10,44,11]onpairedhumanandrobotdata,jointlyoptimizingacrossembodi-
mentstoamortizethehumansignal,yeteverynewtaskstillrequiresitsownbatchofrobotdemon-
strations. Visualretargetingapproaches[16,23,17,18]synthesizepseudo-robotdemonstrationsby
inpainting the human arm and rendering a robot in its place, but the rendered imagery is brittle to
2

Fig.2:SystemoverviewofHumanEgo.Arminpaintingandvisualkeypointsbridgethevisualgap;
Interaction-Centric Tokens encode spatial relationships among all entities; a flow matching policy
withdenseauxiliaryobjectiveslearnsbimanualrobotactionsfromminutes-scalehumandata.
morphological and viewpoint variations. Hierarchical methods [22, 24, 45] learn high-level plans
fromhumanvideoanddelegatelow-levelcontroltoarobot-trainedcontroller,whichstilldependson
robotdataforthelow-levelskill.Toavoidrobotdataaltogether,athirdfamilypursuesembodiment-
agnosticrepresentationsforzero-shottransfer, differinginwhat theyrepresent: point-basedmeth-
ods [21, 20, 46, 47] encode the scene as 2D or 3D points and gain computational efficiency, but
losethestructuralrelationshipbetweenhandandobject;object-centricmethods[48,49,31,29,50]
representthescenethroughtheobject’s6-DoFposeormotion,capturingobjectdynamicsyetmod-
eling the manipulator only implicitly; and goal-conditioned methods [19, 51] predict 2D tracks or
3Dwristtrajectoriesconditionedonatargetimage,butrequireexplicitgoalspecificationatdeploy-
ment. Several other directions [52, 25, 53, 30, 54, 55, 56, 57] also explore learning manipulation
fromvideoalongcomplementaryaxes. Acommonthreadrunsthroughthesezero-shotlines: they
representthehandortheobject,butrarelytheirinteraction—theverysignalthatdefinesmanipula-
tion. HumanEgobridgesthisgapwithaninteraction-centricrepresentationthatexplicitlyencodes
thespatialrelationshipbetweenhandsandobjects,achievingzero-shottransferfromonlyminutes
ofhumanegocentricvideowithoutanyrobotdataorlarge-scalepretraining.
3 HumanEgo
HumanEgoturnshumanegocentricvideointoadeployablebimanualpolicyinfourstages(Fig.2).
AdemonstratorwearingAriaglassesrecordsthetask(Sec.3.1); weclosetheembodimentgapby
inpaintingthehumanarmandrenderingavirtualgripper(Sec.3.2)andbyencodingeveryentity’s
poserelativetoothertaskentitiesintoInteraction-CentricTokens(Sec.3.3).Aflowmatchingpolicy
withthreeauxiliaryobjectivesgeneratesmulti-modalbimanualactions(Sec.3.4).
3.1 EgocentricDataCollection
A human demonstrator wearing Aria Gen1 glasses [7] performs the target task in any conve-
nient environment—regardless of table height, lighting, or background, and without specialized
workspace or calibration (Fig. 11; App. A). Each demonstration takes only seconds; we collect
around 30 minutes of human demonstrations per task at 30Hz. Aria glasses are particularly well
suited for learning from human video: their Machine Perception Services (MPS) provide high-
quality 6-DoF SLAM tracking, calibrated 3D hand pose estimation, and synchronized egocentric
RGBstreams—allfromasinglelightweightwearabledevice.
3

3.2 VisualObservationPreprocessing
We transform the undistorted egocentric frames into embodiment-agnostic RGB observations in
two steps. First, we segment the human hand and arm with SAM2 and remove them via LaMa
inpainting [58], eliminating the visual embodiment gap. Second, we render a virtual gripper and
the tracked object keypoints into the inpainted image—both derived from the spatial observation
(Sec. 3.3)—implicitly encoding 6D pose information as visual cues. This lightweight procedure
bridgesthevisualembodimentgapwithoutexpensivedomainadaptationorimagetranslation.
3.3 SpatialObservationPreprocessing
We build our explicit entity-level spatial observation: treating every object and both hands as an
entity,wetrackthehandsandobjectstorecovereachentity’s6-DoFpose,thenencodetheirrelative
| relationsintoInteraction-CentricTokens. |     |     |     | Wedetailthesethreestepsbelow: |     |     |
| --------------------------------------- | --- | --- | --- | ----------------------------- | --- | --- |
Hand tracking and motion optimization. We start from the 3D hand keypoints produced by
Aria MPS [7], lift them to the world frame via SLAM, and smooth them with Savitzky–Golay on
positionsandanexponentialmovingaverage(EMA)onrotations. Wethentreatthethumb–index
pairasavirtualparallel-jawgripper(Fig.12),extractinganSE(3)end-effectorposeT
ee andascalar
graspg. Forposition,wetakethefingertipmidpointp =(p +p )/2. Fororientation,we
|     |     |     |     | ee  | thumb index |     |
| --- | --- | --- | --- | --- | ----------- | --- |
build a Gram–Schmidt frame on the metacarpophalangeal (MCP) joints rather than the fingertips,
R ee =GramSchmidt(x:thumbMCP→indexMCP, y:wrist→MCPmid),whereMCPmidisthe
midpointofthetwoMCPs;thisavoidsthedegeneracywhenfingertipsconvergeduringpinchgrasps.
Forgrasp,wecomputeascalarg ∈[0,1]bynormalizingthethumb–indexfingertipdistance(details
inApp.B.3),andbinarizeatdeployment.
Object tracking and pose estimation. We detect each object with text-prompted Grounding
DINO [59], segment it with SAM2 [60], and sample contour keypoints from the mask. We
track these 2D keypoints u across the video with CoTracker3 [61] and lift them to 3D via
n
p = Triangulate(u , K, T ),usingcameraintrinsicsK andtheper-frameAriaSLAMpose
| n   | n   | SLAM |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- |
T . WetakethecentroidoftheN trackedpointsastheobjectpositiontocancelper-pointtri-
| SLAM |     | (cid:80)N |     |     |     |     |
| ---- | --- | --------- | --- | --- | --- | --- |
angulationnoise,p = 1 p ,andestimateorientationR withOrient-AnythingV2[62].
|     | obj | N n=1 | n   |     | obj |     |
| --- | --- | ----- | --- | --- | --- | --- |
Duringgraspingtheobjectisoccludedbythehand,soweapplykinematiclatching—rigidlytying
| theobjectposetothehandfromthegrasponsett |     |     |     | : Tt  | =Tt ·(Tt0 )−1Tt0. |     |
| ---------------------------------------- | --- | --- | --- | ----- | ----------------- | --- |
|                                          |     |     |     | 0 obj | hand hand obj     |     |
EntitySpatialEncodingviaInteraction-CentricTokens(ICT). Weencodeeachentity’s6-DoF
poseintoanICT,capturingbothitsposeinasharedreferenceframeanditsspatialrelationtoboth
| hands. Foreachentityk=1,...,N,thetokenICT |     |     |     | ∈R29is: |     |     |
| ----------------------------------------- | --- | --- | --- | ------- | --- | --- |
k
|     |     | ICT =[ | τ ∥ REFT                                       | ∥ ET                                                              | ∥ ET ∥ g ],                                                                 | (1) |
| --- | --- | ------ | ---------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------- | --- |
|     |     | k      |                                                | E LH                                                              | RH                                                                          |     |
|     |     |        | (cid:124)(cid:123)(cid:122)(cid:125) (cid:124) | (cid:123)(cid:122) (cid:125) (cid:124)(cid:123)(cid:122)(cid:125) | (cid:124) (cid:123)(cid:122) (cid:125) (cid:124)(cid:123)(cid:122)(cid:125) |     |
|     |     |        | 1                                              | 9 9                                                               | 9                                                                           |     |
1
REFT
where τ is the entity type (hand or object); E is entity k’s pose in a shared reference frame
REF(astaticcameraframe);ET andET aretheleft-hand(LH)andright-hand(RH)poses
|     |     |     | LH  | RH  |     |     |
| --- | --- | --- | --- | --- | --- | --- |
expressedinentityk’slocalframeE;andgisthegraspstate(binarizedfingerdistanceforhands;a
sentinelforobjects). WeflatteneachSE(3)transformtoa9Dvectorbyconcatenatingthenormal-
izedtranslationwitha6Drotationrepresentation[63],andderiveeveryquantityfromoff-the-shelf
perceptionwithoutground-truthlabels. Unlikepriormethodsusingglobalpointcloudsorabsolute
coordinates[21,20],weanchoreachICTtoanentitysothattheevolvingET andET directly
LH RH
reflect the manipulation state—approaching, grasping, or transporting—making the representation
inherently interaction-centric. Expressing every quantity relative to scene entities rather than the
camerayieldsidenticaltokensregardlessofviewpoint,enablingdirecthuman-to-robottransfer. We
also gain a unified, variable-length interface that accommodates scenes with different numbers of
objects without architectural changes. We empirically show that ICT is the key enabler of cross-
embodimenttransfer(Sec.4.4).
3.4 FlowMatchingPolicywithDenseAuxiliaryObjectives
Ourpolicy(Fig.2)takesthescenestates t —ICT tokensandanRGBimage—andgeneratesabi-
manualactiontrajectorya∈RK×Da overaK-stephorizon,whereeachD -dimsliceconcatenates
a
| bothhands’6-DoFposesandbinarygrasps. |     |     |     | Wedescribethetrainingbelow. |     |     |
| ------------------------------------ | --- | --- | --- | --------------------------- | --- | --- |
4

Flowmatchingactiongeneration. Weformulateactiongenerationasaconditionalflowmatch-
ing[33,64]problem:weparameterizeavelocityfieldv withatransformerdecoderconditionedon
θ
s t ,andtrainittotransportaGaussianpriorsampletotheactiontarget. Ourprimarytraininglossis:
|     |     |            | (cid:104) |         |         |      | (cid:105) |             |           |     |
| --- | --- | ---------- | --------- | ------- | ------- | ---- | --------- | ----------- | --------- | --- |
|     | L   | =E         | w         | ∥∆p∥2+w | ∥∆r∥2+w |      | ∥∆g∥2     | , x =(1−t)x | +tx ,     |     |
|     |     | FM t,x0,x1 | p         |         | r       | g    |           | t           | 0 1       | (2) |
|     | w   | ,w ,w      |           |         |         | (p), |           | (r),        | (g); ∆(·) | =   |
where p r g are the loss weights for position rotation and grasp
v (x ,t,s )−(x −x )isthevelocitypredictionerror;x =(1−t)x +tx istheinterpolatedsam-
| θ   | t   | t 1 | 0   |     |     |     | t   | 0 1 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
pleatflowtimet ∼ U(0,1);x ∼ N(0,I)isaGaussianpriorsample;andx istheground-truth
|     |     |     |     | 0   |     |     |     | 1   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bimanualaction. Atinference,weintegratethelearnedODEwithafixed-stepEulersolver.
Dense auxiliary objectives. To extract rich supervision from every demonstration, we add three
auxiliaryobjectivesthatsharethecontextencoderwiththeflowmatchinghead: (1)Objectmotion
(L ): wepredicteachmanipulatedobject’sfuture6-DoFtrajectory,forcingtheencodertomodel
OM
objectdynamicsunderhandmotion;(2)2Dtrace(L ): weregressfuture2Dprojectionsofentity
2D
trajectories,groundingtherepresentationinthevisualobservation;(3)Latentconsistency(L ):we
LC
predictthe ICT stateK stepsahead,pushingtheencodertocapturescenedynamics. Wecombine
themwiththeflowmatchinglossintoasingleobjective:
|     |     |     | L=L |     | +λ L  | +λ  | L +λ | L ,   |     | (3) |
| --- | --- | --- | --- | --- | ----- | --- | ---- | ----- | --- | --- |
|     |     |     |     | FM  | OM OM | 2D  | 2D   | LC LC |     |     |
whereλ ,λ ,λ arethelossweightsofthethreeauxiliaryobjectives.Wederiveeveryauxiliary
|     | OM  | 2D LC |     |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
targetautomaticallyfromtheperceptionpipeline, soeachdemonstrationyieldsadensemulti-task
signal. Allthreeobjectivesforecasthowthesceneevolvesincomplementaryspaces(3Dphysical,
2D visual, latent space), equipping the shared encoder with a lightweight world model of hand–
objectinteraction. Wealsoexploitthesharedencoderasamulti-taskregularizerthatcurbsoverfit-
ting,withthelargestgainsinthelow-dataregime(Sec.4.2,4.4).
4 Experiments
| We  | evaluate | HumanEgo | to  | answer | four ques- |     |     |     |     |     |
| --- | -------- | -------- | --- | ------ | ---------- | --- | --- | --- | --- | --- |
tions: (1)Cantheembodimentgapbebridgedto
achievereliablemanipulationfromhumanvideo
| alone? | (Sec. | 4.1) (2)   | How  | does policy | perfor- |     |     |     |     |     |
| ------ | ----- | ---------- | ---- | ----------- | ------- | --- | --- | --- | --- | --- |
| mance  | scale | with human | data | versus      | matched |     |     |     |     |     |
robotdata?(Sec.4.2)(3)Howrobustisthepolicy
| to  | distribution | shifts | in embodiment, |     | viewpoint, |     |     |     |     |     |
| --- | ------------ | ------ | -------------- | --- | ---------- | --- | --- | --- | --- | --- |
Fig.3: FourReal-WorldEvaluationtasks.
| andenvironment? |     | (Sec.4.3)(4)Howmuchdoes |     |     |     |     |     |     |     |     |
| --------------- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
eachcomponentcontributetothefinalperformance? (Sec.4.4)Unlessotherwisenoted, allexper-
iments are conducted on Trossen WidowX arms with a top-mounted RealSense D405 (App. D.1),
andwereportsuccessrate(%)over40trialspertaskwithrandomizedinitialobjectpositions.
4.1 HumanEgoBridgestheEmbodimentGapEfficiently
WeevaluateHumanEgoonfourreal-worldmanipulationtasks(Fig.3; detailsinApp.A.2): Serve
Bread, a pick-and-place task in which the robot grasps a croissant from arbitrary positions and
placesitonaplate;DownstackCups,along-horizonmulti-steptaskrequiringsequentialtoppling,
grasping,andre-stackingofthreenestedcups; WaterFlowers,acontact-richbimanualtaskwith
stricttemporalordering—onearmholdsapulled-outspraynozzleoveraflowerpotwhiletheother
opensthevalve;andAdjustTable,asustainedrotational-controltaskinwhichtherobotgraspsa
crankhandleandturnsitthreefullrevolutionswithoutreleasing. Wecompareagainstfivezero-shot
methodsthatlearnmanipulationfromhumanegocentricvideo,organizedintothreedesignfamilies.
Two are point-based: EgoZero [21] lifts the egocentric scene into 3D point clouds that treat hand
andobjectalike, whilePointPolicy[20]insteadtrackssparsekeypointsoneach. Anothertwoare
goal-conditioned: ZeroMimic[51]distills3Dwristtrajectoriesfromwebvideoandconditionsona
goalimageattesttime,andTrack2Act[19]predicts2Dpointtrackswithoutexplicit3Dreasoning.
Thelast,SPOT [48],isobject-centric,generatingSE(3)objecttrajectorieswithadiffusionmodel.
All five are trained on the same 30 minutes of human data per task. We also include ACT [28],
trainedon30minutesofrobotteleoperationcollectedonthesamehardware.
5

Overall Real-World Evaluation
| 100  |     |     | 95.0 |     |     |     | 95.0 |     |      |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | ---- | --- |
| 92.5 |     |     |      |     |     |     |      |     | 92.5 |     |
87.5
82.5
| 80               | 75.0 |     |      |     |      |     | 75.0 |     | 75.0 |     |
| ---------------- | ---- | --- | ---- | --- | ---- | --- | ---- | --- | ---- | --- |
| )%( etaR sseccuS |      |     |      |     | 67.5 |     |      |     |      |     |
|                  |      |     | 62.5 |     |      |     |      |     | 62.5 |     |
60
|     | 51.2 |     | 52.5 |     |     |     |     |     |     |     |
| --- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
47.5
|     | 45.0 |     |     |      | 45.0 |     | 45.045.0 |     |      |     |
| --- | ---- | --- | --- | ---- | ---- | --- | -------- | --- | ---- | --- |
| 40  |      |     |     | 35.0 | 35.0 |     |          |     | 37.5 |     |
30.0
|     | 26.2 |      |     |      |     | 27.5 |     |      |     |     |
| --- | ---- | ---- | --- | ---- | --- | ---- | --- | ---- | --- | --- |
| 20  |      | 18.8 |     |      |     |      |     | 17.5 |     |     |
|     |      |      |     | 12.5 |     | 12.5 |     |      |     |     |
10.0
|     |     | 6.9 |     | 5.0 |     |        |     | 7.5 |     | 5.0     |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | ------- |
|     |     | 1.9 |     |     |     | 2.50.0 |     | 2.5 |     | 0.0 0.0 |
0
|     | Overall |     | Serve Bread |     | Downstack Cups |     | Water Flowers |     | Adjust Table |     |
| --- | ------- | --- | ----------- | --- | -------------- | --- | ------------- | --- | ------------ | --- |
HumanEgo-30 HumanEgo-15 ACT (Robot Teleop) SPOT ZeroMimic Track2Act PointPolicy EgoZero
Fig. 4: Overall Real-World Evaluation. Real-world success rate (%) for each method across
all four tasks. HumanEgo with 30 min of data achieves the highest success rate on every task,
demonstrating consistent improvements over both human-video baselines and robot teleoperation
methods.
HumanEgoachievesthehighestsuccessrateoneverysingletask.AsshowninFig.4,HumanEgo
with only 30 minutes of human data reaches 92.5% average success rate across all four tasks. In
contrast, the five human-video baselines range from 1.9% to 45.0%, a wide spread revealing that
eachmethodcapturesonlyapartialaspectofmanipulation,performingadequatelyonsimplertasks
butcollapsingonthosethatdemandprecisehand–objectreasoning. HumanEgoistheonlymethod
thatmaintainshighperformanceregardlessoftaskcomplexity.
Even with half the data, HumanEgo outperforms robot teleoperation. HumanEgo with only
15minutesofhumandataalreadyreaches75.0%, surpassingACTtrainedon30minutesofrobot
teleoperation(51.2%),highlightingthedataefficiencyofourapproach—andthatreadilyavailable
humanvideoscanbeasurprisinglypotentdatasourceforrobotlearning.
HumanEgoexcelsontasksthatdemandprecisecoordinationandspatialreasoning.OnDown-
stack Cups, a long-horizon task requiring sequential unstacking of three nested cups with ∼1cm
tolerancewhereearlyerrorscompound,HumanEgoreaches87.5%whilenobaselineexceeds45%.
OnWaterFlowers,therobotmustcoordinatebotharmssequentially—onearmcompletesitssubtask
beforetheotheropensthefaucettopourwater—andpreciselyaimthestreamintothepot,demand-
inggenuinespatialunderstandingofobjectpositionsratherthanmemorizedtrajectories;HumanEgo
achieves95%,morethandoublethebestbaseline(45%).
Data Efficiency
4.2 TheEfficiencyofHumanDemonstrations
|     |     |     |     |     |     |      | HumanEgo (Human Data)         |     | HumanEgo (Robot Data) |     |
| --- | --- | --- | --- | --- | --- | ---- | ----------------------------- | --- | --------------------- | --- |
|     |     |     |     |     |     | 100% | HumanEgo w/o Aux (Human Data) |     | ACT (Robot Data)      |     |
WecompareHumanEgotrainedonhumanvideo
| against | ACT | and HumanEgo | trained | on  | robot |     |     |     |     |     |
| ------- | --- | ------------ | ------- | --- | ----- | --- | --- | --- | --- | --- |
75%
)%( etaR sseccuS
| teleoperation      | as     | a function  | of collection |              | time on |     |     |     |     |     |
| ------------------ | ------ | ----------- | ------------- | ------------ | ------- | --- | --- | --- | --- | --- |
| ServeBread(Fig.5). |        |             |               |              |         | 50% |     |     |     |     |
| HumanEgo           | learns | effectively |               | from minimal |         |     |     |     |     |     |
25%
| human | data. | With only | ∼7 minutes | of  | human |     |     |     |     |     |
| ----- | ----- | --------- | ---------- | --- | ----- | --- | --- | --- | --- | --- |
demonstrations,HumanEgoalreadyreaches50%
0%
success rate and continues to climb smoothly, 1 2 4 8 12 18 24 30
Collection Time (mins)
reaching 95% at 30 minutes. This steep, mono- Fig. 5: Data efficiency. Success rate (%) vs.
tonic scaling curve indicates that our pipeline data collection time. HumanEgo trained on
extracts useful manipulation signal from even a 8 min of human data surpasses ACT’s 30-min
| handfulofdemonstrations. |     |     |     |     |     | robotdata. |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- |
Auxiliaryobjectivesamplifylearningwhendemonstrationsarescarce. Between2and12min-
utes, HumanEgo with auxiliary losses consistently outperforms the variant without them, with the
largestgainat8min(57.5%vs.37.5%).Beyond18minutesbothvariantsconverge,reaching95%at
30minutes,confirmingthatauxiliarylossesextractrichersupervisionfromeachdemonstration—a
benefitthatdiminishesasdatagrowsabundant.
6

Human vs. Robot Data
| Human | video | is a more | efficient | data source |     |     | Human Data Has Higher Quality |     |     |     |
| ----- | ----- | --------- | --------- | ----------- | --- | --- | ----------------------------- | --- | --- | --- |
than robot teleoperation. At 8 minutes of (a) Signal-to-Noise Ratio )³01×( kreJ dezilamroN 1000 (b) Motion Smoothness (c) Action Idle Time
)%( noitcarF eldI 15
|                                          |       |          |               |                  | 20       |             | 800 |             |       |       |
| ---------------------------------------- | ----- | -------- | ------------- | ---------------- | -------- | ----------- | --- | ----------- | ----- | ----- |
| collection                               | time, | HumanEgo |               | trained on human | )Bd( RNS |             | 600 |             | 10    |       |
|                                          |       |          |               |                  | 10       |             | 400 |             |       |       |
| video(57.5%)alreadysurpassesACTtrainedon |       |          |               |                  |          |             |     |             | 5     |       |
|                                          |       |          |               |                  | 0        |             | 200 |             |       |       |
| 30 minutes                               | of    | robot    | teleoperation | (52.5%)—a        |          |             | 0   |             | 0     |       |
|                                          |       |          |               |                  |          | Human Robot |     | Human Robot | Human | Robot |
3.75×reductionincollectioneffort. Offlinemet- Human Data Has Higher Diversity
rics further confirm that human demonstrations (d) Position Density (e) Trajectory t-SNE )mc( daerpS noitisoP naeM 30 (f) Inter-Session Variance
|     |     |     |     |     | 1.0 |     | H u m a n 10 | Human |     | Human |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | --- | ----- |
|     |     |     |     |     |     |     | Ro b o t     | Robot | 25  | Robot |
exhibit greater spatial density and trajectory di- )m( Z 0.8 2 ACP 0 20
|                               |           |                |     |                 | 0.6 |             |     |         | 15              |                |
| ----------------------------- | --------- | -------------- | --- | --------------- | --- | ----------- | --- | ------- | --------------- | -------------- |
| versity,                      | producing | higher-quality |     | training signal |     |             |     |         |                 |                |
|                               |           |                |     |                 | 0.4 |             | 10  |         | 10              |                |
| perminuteofcollection(Fig.6). |           |                |     |                 |     |             |     |         | 5               |                |
|                               |           |                |     |                 |     | 0.2 0.0 0.2 | 0.4 | 10 0 10 | 0.00 0.25       | 0.50 0.75 1.00 |
|                               |           |                |     |                 |     | X (m)       |     | PCA 1   | Normalized Time |                |
4.3 OnePolicy,ManyConditions Fig.6: Humanvs.robotdata. Humanegocen-
tricdataexhibitshigherSNR,smoothermotion,
We deploy HumanEgo on Serve Bread and less idle time (top), and greater spatial and tra-
| Downstack | Cups | across | 9   | out-of-distribution | jectorydiversity(bottom). |     |     |     |     |     |
| --------- | ---- | ------ | --- | ------------------- | ------------------------- | --- | --- | --- | --- | --- |
conditions—withoutanyretrainingorfine-tuning
(40trialseachforeachtask;resultsinFig.7,real-worldsetupinFig.8).
Zero-Shot Cross-Condition Generalization
| Cross-           |             | Trossen |     | Cross-       |     |     |     |     |     |     |
| ---------------- | ----------- | ------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
| Environment      |             |         |     | Embodiment   |     |     |     |     |     |     |
|                  | Distractors | 91.25%  |     | UR10         |     |     |     |     |     |     |
|                  | 91.25%      |         |     | 87.5%        |     |     |     |     |     |     |
| Novel Objects    |             |         |     | Franka       |     |     |     |     |     |     |
|                  | 85%         |         |     | 88.75%       |     |     |     |     |     |     |
|                  | 91.25%      |         |     | 90%          |     |     |     |     |     |     |
| Novel Background |             |         |     | Novel Camera |     |     |     |     |     |     |
Cross-
Setup
|     | 91.25%         |       |     | 86.25%       |     |     |     |     |     |     |
| --- | -------------- | ----- | --- | ------------ | --- | --- | --- | --- | --- | --- |
|     | Novel Lighting | 87.5% |     | Novel Height |     |     |     |     |     |     |
Novel Viewpoint
Fig. 7: Zero-Shot Cross-Condition General- Fig. 8: Cross-condition real-world evalua-
ization. HumanEgo maintains robust success tion: cross-embodiment/environment/setup.
acrossdifferentconditionswithoutretraining.
HumanEgo is robust to arbitrary visual conditions. Changing the background, lighting, view-
point, or adding distractors all yield 85–91.25% success, with no measurable degradation in most
cases. Thepolicyevenhandlesnovelobjectinstancesthatneverappearinthetrainingset,demon-
strating that it effectively extracts task-relevant information from the visual input while remaining
invarianttoirrelevantvariations.
HumanEgoisrobusttoarbitraryobjectplacements. OnServeBread,itdeliversthebreadtothe
plateacrossarbitraryabsoluteandrelativepositionsonthetableandevenatnovelheights;onDown-
stack Cups, it completes the three-step sequence under varied table heights and cup positions—
scenarioswheremethodslikeEgoZero[21]andPointPolicy[20]oftenfail.Beyondthisquantitative
evaluation,wealsoobservesimilarplacementrobustnessqualitativelyonWaterFlowers,wherethe
robot aims the faucet into the pot wherever it sits in the sink. This robustness reflects the object-
centricstructureembeddedinourinteraction-centricrepresentation,enablingplacementinvariance.
HumanEgoishardware-agnostic. AlltrainingdataiscollectedwithAriaglasses,yetatinference
thepolicyachieveshighsuccessratesregardlessofthedeploymenthardware—whetherthecamera
is a RealSense or a ZED, and whether the robot arm is a Trossen, Franka, or UR10. The training
anddeploymentsetupssharenohardwareincommon,yetthepolicytransfersseamlessly—enabled
bytheframe-invariantrepresentationandtrainingarchitecturedetailedinSec.4.4.
4.4 WhatDrivesPerformanceofHumanEgo?
WeablateHumanEgo’stwocoredesignchoicesonWaterFlowers:thespatialrepresentation(Fig.9)
andtheauxiliarytrainingobjectives(Fig.10).
Explicitspatialrepresentation,notvisualfidelity,isthekeytobridgingtheembodimentgap.
Weisolatevisualpreprocessingfromspatialrepresentation. Progressivelyreducingthevisualem-
bodimentgap—fromrawhumanRGB(7.5%)tokeypointrenderingwitharminpainting(20%)to
7

100
75
50
25
0
Human + Kpts & Robot Human RGB HumanEgo
RGB Inpaint RGB + ICT (Full)
)%(
etaR
sseccuS
Representation Study
Visual Only VViissuuaall ++ SSppaattiiaall
+62.5pp
95%
85% 100
75
50
32.5%
20% 25
7.5%
0
No + Object + 2D + Latent HumanEgo
Aux Motion Trace Consistency (Full)
Fig.9: Representationstudy. Successrate(%)
forfiveinputconfigurations. Visual-onlymeth-
ods plateau at 32.5% withany strategy; adding
spatialtokensyields+52.5pp.
)%(
etaR
sseccuS
Auxiliary Training Study
Baseline Single Auxiliary AAllll AAuuxx
+25pp
75% 67.5%
62.5%
55% 50%
Fig. 10: Auxiliary training study. Success
rate (%) at 15min of data for each auxil-
iaryobjectiveindividually. Objectmotioncon-
tributes the most (+17.5pp); all three combine
for+25pp.
robotRGBthateliminatesthegapentirely(32.5%)—yieldsonlymodestgains; evenwithzerovi-
sual mismatch, the policy barely exceeds 30%. Monocular RGB encodes appearance, not the 3D
spatialrelationshipsthatmanipulationdemands. Adding ICT torawhumanRGBproducesadra-
maticjumpfrom7.5%to85%,andthefullsystemreaches95%. ICTdirectlyencodestherelative
6-DoFtransformsbetweenhandsandobjects—thecoremanipulationstate—turningtheproblemof
inferring3Ddynamicsfrompixelsintolearningactionsfromexplicitspatialrelationships.
Auxiliary objectives provide complementary gains. We evaluate each objective individually at
15 minutes of data. Each loss independently improves performance: object motion (+17.5pp),
latent consistency (+12.5pp), and 2D trace (+5pp). Combined, they yield a cumulative +25pp
improvementoverthebasemodel. Atahighlevel, allthreeobjectivesperformforwarddynamics
prediction—forecastinghowmanipulationstatesevolve—indifferentspaces(3Dphysicalspace,2D
visualspace,andlatentstateembeddings),forcingthesharedencodertolearnthecausalstructure
of manipulation rather than visual appearance alone. Together, the ablations support the main ex-
perimentalthesis: ICTsuppliesthetransferablemanipulationstate,anddenseauxiliarysupervision
makesthatstatelearnablefromminutesofhumanvideo.
5 Conclusion
We presented HumanEgo, a framework that learns robot manipulation policies from minutes of
human egocentric videos—without any robot data or large-scale pretraining. HumanEgo adopts
a hardware-agnostic representation that bridges the embodiment gap through visual preprocessing
(arminpainting,keypointrendering)andspatialencoding(ICT),makingthelearnedpolicyinvariant
to embodiment, viewpoint, and environment. Combined with a flow matching policy and dense
auxiliaryobjectivesthatsuperviseforwarddynamicsincomplementaryspaces,HumanEgoachieves
92.5%averagesuccessacrossfourreal-worldtasks,outperformsfiverecenthuman-videobaselines,
yieldsa41%improvementovermatched-timerobotteleoperation,andgeneralizeszero-shottonovel
robotembodiments,camerasetups,andreal-worldenvironments—withoutanyretraining.
Limitationsandfuturework. OurframeworkreliesonAria’sstereohandtracking—monocular
substitutes drop real-world success sharply (App. E.1), calling for stronger monocular hand pose
estimators that recover absolute depth. We use per-frame object detection rather than real-time
tracking;in-handmanipulationandotherdynamicscenariosinvolvingocclusionorfastmotionwill
requireonline,occlusion-robusttrackers. Thepipelinechainsseveraloff-the-shelfperceptionmod-
uleswhosefailurescascadeintothepolicy,motivatingstrongerorjointly-trainedfrontends. Finally,
few-shot learning plateaus at ∼1cm precision; reaching sub-centimeter accuracy on contact-rich
taskswilllikelyrequirereinforcement-learningrefinementorsimulation-basedfine-tuning. Wesee
HumanEgoasastartingpoint—afullyzero-shot,robot-data-freepipelinethatfutureworkcanex-
tendwithonlinetracking,learnedfrontends,anddownstreamRLrefinement.
8

Acknowledgments
We thank Eadom Dessalene, Yoonkyo Jung, Zikui Cai, and other members of the PRG Lab and
Furong’sLabfortheirhelpfulfeedbackandsupportthroughoutthisproject.
References
[1] A.Brohan,N.Brown,J.Carbajal,Y.Chebotar,X.Chen,K.Choromanski,T.Ding,D.Driess,
A.Dubey,C.Finn,P.Florence,C.Fu,M.G.Arenas,K.Gopalakrishnan,K.Han,K.Hausman,
A.Herzog,J.Hsu,B.Ichter,A.Irpan,N.Joshi,R.Julian,D.Kalashnikov,Y.Kuang,I.Leal,
L. Lee, T.-W. E. Lee, S. Levine, Y. Lu, H. Michalewski, I. Mordatch, K. Pertsch, K. Rao,
K. Reymann, M. Ryoo, G. Salazar, P. Sanketi, P. Sermanet, J. Singh, A. Singh, R. Soricut,
H.Tran, V.Vanhoucke, Q.Vuong, A.Wahid, S.Welker, P.Wohlhart, J.Wu, F.Xia, T.Xiao,
P. Xu, S. Xu, T. Yu, and B. Zitkovich. RT-2: Vision-language-action models transfer web
knowledgetoroboticcontrol. arXivpreprintarXiv:2307.15818,2023.
[2] ALOHA 2 Team, J. Aldaco, T. Armstrong, R. Baruch, J. Bingham, S. Chan, K. Draper,
D. Dwibedi, C. Finn, P. Florence, S. Goodrich, W. Gramlich, T. Hage, A. Herzog, J. Hoech,
T.Nguyen,I.Storz,B.Tabanpour,L.Takayama,J.Tompson,A.Wahid,T.Wahrburg,S.Xu,
S. Yaroshenko, K. Zakka, and T. Z. Zhao. ALOHA 2: An enhanced low-cost hardware for
bimanualteleoperation. arXivpreprintarXiv:2405.02292,2024.
[3] C.Chi,Z.Xu,S.Feng,E.Cousineau,Y.Du,B.Burchfiel,R.Tedrake,andS.Song. Diffusion
policy: Visuomotor policy learning via action diffusion. In Robotics: Science and Systems
(RSS),2023.
[4] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany,
M. K. Srirama, L. Y. Chen, K. Ellis, P. D. Fagan, J. Hejna, M. Itkina, M. Lepert, Y. J. Ma,
P.T.Miller,J.Wu,S.Belkhale,S.Dass,H.Ha,A.Jain,A.Lee,Y.Lee,M.Memmel,S.Park,
I. Radosavovic, K. Wang, A. Zhan, K. Black, C. Chi, K. B. Hatch, S. Lin, J. Lu, J. Mercat,
A.Rehman,P.R.Sanketi,A.Sharma,C.Simpson,Q.Vuong,H.R.Walke,B.Wulfe,T.Xiao,
J. H. Yang, A. Yavary, T. Z. Zhao, C. Agia, R. Baijal, M. G. Castro, D. Chen, Q. Chen,
T. Chung, J. Drake, E. P. Foster, J. Gao, V. Guizilini, D. A. Herrera, M. Heo, K. Hsu, J. Hu,
M.Z.Irshad,D.Jackson,C.Le,Y.Li,K.Lin,R.Lin,Z.Ma,A.Maddukuri,S.Mirchandani,
D.Morton,T.Nguyen,A.O’Neill,R.Scalise,D.Seale,V.Son,S.Tian,E.Tran,A.E.Wang,
Y. Wu, A. Xie, J. Yang, P. Yin, Y. Zhang, O. Bastani, G. Berseth, J. Bohg, K. Goldberg,
A. Gupta, A. Gupta, D. Jayaraman, J. J. Lim, J. Malik, R. Mart´ın-Mart´ın, S. Ramamoorthy,
D.Sadigh, S.Song, J.Wu, M.C.Yip, Y.Zhu, T.Kollar, S.Levine, andC.Finn. DROID:A
large-scale in-the-wild robot manipulation dataset. In Robotics: Science and Systems (RSS),
2024.
[5] M.J.Kim,K.Pertsch,S.Karamcheti,T.Xiao,A.Balakrishna,S.Nair,R.Rafailov,E.P.Foster,
P.R.Sanketi,Q.Vuong,T.Kollar,B.Burchfiel,R.Tedrake,D.Sadigh,S.Levine,P.Liang,and
C.Finn. OpenVLA:Anopen-sourcevision-language-actionmodel. In8thAnnualConference
onRobotLearning,2024. URLhttps://openreview.net/forum?id=ZMnD6QZAE6.
[6] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, C. Finn,
N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, brian ichter, S. Jakubczak,
T.Jones, L.Ke, D.LeBlanc, S.Levine, A.Li-Bell, M.Mothukuri, S.Nair, K.Pertsch, A.Z.
Ren, L.X.Shi, L.Smith, J.T.Springenberg, K.Stachowicz, J.Tanner, Q.Vuong, H.Walke,
A.Walling,H.Wang,L.Yu,andU.Zhilinsky. $\pi {0.5}$: avision-language-actionmodel
with open-world generalization. In 9th Annual Conference on Robot Learning, 2025. URL
https://openreview.net/forum?id=vlhoswksBO.
[7] J.Engel,K.Somasundaram,M.Goesele,A.Sun,A.Gamino,A.Turner,A.Talattof,A.Yuan,
B. Souti, B. Meredith, C. Peng, C. Sweeney, C. Wilson, D. Barnes, D. DeTone, D. Caruso,
D. Valleroy, D. Ginjupalli, D. Frost, E. Miller, E. Mueggler, E. Oleinik, F. Zhang, G. Soma-
sundaram,G.Solaira,H.Lanaras,H.Howard-Jenkins,H.Tang,H.J.Kim,J.Rivera,J.Luo,
9

J.Dong,J.Straub,K.Bailey,K.Eckenhoff,L.Ma,L.Pesqueira,M.Schwesinger,M.Monge,
N.Yang,N.Charron,N.Raina,O.Parkhi,P.Borschowa,P.Moulon,P.Gupta,R.Mur-Artal,
R.Pennington, S.Kulkarni, S.Miglani, S.Gondi, S.Solanki, S.Diener, S.Cheng, S.Green,
S. Saarinen, S. Patra, T. Mourikis, T. Whelan, T. Singh, V. Balntas, V. Baiyya, W. Dreewes,
X.Pan,Y.Lou,Y.Zhao,Y.Mansour,Y.Zou,Z.Lv,Z.Wang,M.Yan,C.Ren,R.DeNardi,
and R. Newcombe. Project Aria: A new tool for egocentric multi-modal AI research. arXiv
preprintarXiv:2308.13561,2023.
[8] S. Kareer, D. Patel, R. Punamiya, P. Mathur, S. Cheng, C. Wang, J. Hoffman, and D. Xu.
EgoMimic:Scalingimitationlearningviaegocentricvideo. InIEEEInternationalConference
onRoboticsandAutomation(ICRA),2025.
[9] R.Punamiya,D.Patel,P.Aphiwetsa,P.Kuppili,L.Y.Zhu,S.Kareer,J.Hoffman,andD.Xu.
EgoBridge: Domain adaptation for generalizable imitation from egocentric human data. In
AdvancesinNeuralInformationProcessingSystems(NeurIPS),2025.
[10] Y. Liu, W. C. Shin, Y. Han, Z. Chen, H. Ravichandar, and D. Xu. ImMimic: Cross-domain
imitationfromhumanvideosviamappingandinterpolation.arXivpreprintarXiv:2509.10952,
2025.
[11] R.-Z. Qiu, S. Yang, X. Cheng, C. Chawla, J. Li, T. He, G. Yan, D. J. Yoon, R. Hoque,
L.Paulsen,G.Yang,J.Zhang,S.Yi,G.Shi,andX.Wang.Humanoidpolicy˜humanpolicy.In
9thAnnualConferenceonRobotLearning,2025. URLhttps://openreview.net/forum?
id=Tx54fkQ3Cq.
[12] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, X. Cheng, R.-Z. Qiu,
H.Yin,S.Liu,S.Han,Y.Lu,andX.Wang.EgoVLA:Learningvision-language-actionmodels
fromegocentrichumanvideos. arXivpreprintarXiv:2507.12440,2025.
[13] R. Zheng, D. Niu, Y. Xie, J. Wang, M. Xu, Y. Jiang, F. Castan˜eda, F. Hu, Y. L. Tan, L. Fu,
T. Darrell, F. Huang, Y. Zhu, D. Xu, and L. Fan. EgoScale: Scaling dexterous manipulation
withdiverseegocentrichumandata. arXivpreprintarXiv:2602.16710,2026.
[14] R.Punamiya, S.Kareer, Z.Liu, J.Citron, R.-Z.Qiu, X.Cai, A.Gavryushin, J.Chen, D.Li-
conti, L.Y.Zhu, P.Aphiwetsa, B.Li, A.Cheluva, P.Kuppili, Y.Liu, D.Patel, M.Pollefeys,
R.Katzschmann,X.Wang,S.Song,J.Hoffman,D.Xu,etal.EgoVerse:Anegocentrichuman
datasetforrobotlearningfromaroundtheworld. arXivpreprintarXiv:2604.07607,2026.
[15] R. Hoque, P. Huang, D. J. Yoon, M. Sivapurapu, and J. Zhang. EgoDex: Learning dexter-
ousmanipulationfromlarge-scaleegocentricvideo. InInternationalConferenceonLearning
Representations(ICLR),2026.
[16] M.Lepert,J.Fang,andJ.Bohg. Phantom: Trainingrobotswithoutrobotsusingonlyhuman
videos. InConferenceonRobotLearning(CoRL),2025.
[17] M.Lepert,J.Fang,andJ.Bohg. Masquerade: Learningfromin-the-wildhumanvideosusing
data-editing. arXivpreprintarXiv:2508.09976,2025.
[18] E.Dessalene,P.Mantripragada,M.Maynord,andY.Aloimonos. EmbodiSwapforzero-shot
robotimitationlearning. arXivpreprintarXiv:2510.03706,2025.
[19] H. Bharadhwaj, R. Mottaghi, A. Gupta, and S. Tulsiani. Track2Act: Predicting point tracks
from internet videos enables generalizable robot manipulation. In European Conference on
ComputerVision(ECCV),2024.
[20] S. Haldar and L. Pinto. Point policy: Unifying observations and actions with key points for
robotmanipulation. InConferenceonRobotLearning(CoRL),2025.
10

[21] V.Liu,A.Adeniji,H.Zhan,S.Haldar,R.Bhirangi,P.Abbeel,andL.Pinto. EgoZero: Robot
learningfromsmartglasses. arXivpreprintarXiv:2505.20290,2025.
[22] C.Wang,L.Fan,J.Sun,R.Zhang,L.Fei-Fei,D.Xu,Y.Zhu,andA.Anandkumar.MimicPlay:
Long-horizonimitationlearningbywatchinghumanplay. InConferenceonRobotLearning
(CoRL),2023.
[23] G.Li,Y.Lyu,Z.Liu,C.Hou,J.Zhang,andS.Zhang. H2R:Ahuman-to-robotdataaugmen-
tationforrobotpre-trainingfromvideos. arXivpreprintarXiv:2505.11920,2025.
[24] M.Xu,Z.Xu,C.Chi,M.Veloso,andS.Song. XSkill: Crossembodimentskilldiscovery. In
7thAnnualConferenceonRobotLearning,2023. URLhttps://openreview.net/forum?
id=8L6pHd9aS6w.
[25] M.Xu,Z.Xu,Y.Xu,C.Chi,G.Wetzstein,M.Veloso,andS.Song. Flowasthecross-domain
manipulationinterface. InConferenceonRobotLearning(CoRL),2024.
[26] V. Jain, M. Attarian, N. J. Joshi, A. Wahid, D. Driess, Q. Vuong, P. R. Sanketi, P. Sermanet,
S.Welker,C.Chan,I.Gilitschenski,Y.Bisk,andD.Dwibedi. Vid2Robot: End-to-endvideo-
conditionedpolicylearningwithcross-attentiontransformers. InRobotics: ScienceandSys-
tems(RSS),2024.
[27] C.Wen,X.Lin,J.So,K.Chen,Q.Dou,Y.Gao,andP.Abbeel. Any-pointtrajectorymodeling
forpolicylearning,2024. URLhttps://arxiv.org/abs/2401.00025.
[28] T.Z.Zhao, V.Kumar, S.Levine, andC.Finn. Learningfine-grainedbimanualmanipulation
withlow-costhardware. InRobotics: ScienceandSystems(RSS),2023.
[29] K.Yu,S.Zhang,H.Soora,F.Huang,H.Huang,P.Tokekar,andR.Gao.GenFlowRL:Shaping
rewards with generative object-centric flow in visual reinforcement learning. arXiv preprint
arXiv:2508.11049,2025.
[30] H.Li,L.Sun,Y.Hu,D.Ta,J.Barry,G.Konidaris,andJ.Fu. NovaFlow: Zero-shotmanipula-
tionviaactionableflowfromgeneratedvideos. arXivpreprintarXiv:2510.08568,2025.
[31] S.Patel,S.Mohan,H.Mai,U.Jain,S.Lazebnik,andY.Li. Roboticmanipulationbyimitating
generatedvideoswithoutphysicaldemonstrations. arXivpreprintarXiv:2507.00990,2025.
[32] K. Yu, Y. Han, Q. Wang, V. Saxena, D. Xu, and Y. Zhao. Mimictouch: Leveraging multi-
modalhumantactiledemonstrationsforcontact-richmanipulation. In8thAnnualConference
onRobotLearning,2024. URLhttps://openreview.net/forum?id=7yMZAUkXa4.
[33] Y.Lipman,R.T.Q.Chen,H.Ben-Hamu,M.Nickel,andM.Le. Flowmatchingforgenerative
modeling. InInternationalConferenceonLearningRepresentations(ICLR),2023.
[34] K.Grauman,A.Westbury,E.Byrne,Z.Chavis,A.Furnari,R.Girdhar,J.Hamburger,H.Jiang,
M. Liu, X. Liu, M. Martin, T. Nagarajan, I. Radosavovic, S. K. Ramakrishnan, F. Ryan,
J. Sharma, M. Wray, M. Xu, E. Z. Xu, C. Zhao, et al. Ego4D: Around the world in 3,000
hoursofegocentricvideo. InIEEE/CVFConferenceonComputerVisionandPatternRecog-
nition(CVPR),2022.
[35] D. Damen, H. Doughty, G. M. Farinella, A. Furnari, E. Kazakos, J. Ma, D. Moltisanti,
J.Munro,T.Perrett,W.Price,andM.Wray. Rescalingegocentricvision: Collectionpipeline
andchallengesforEPIC-KITCHENS-100. InternationalJournalofComputerVision(IJCV),
2022.
[36] P.Banerjee, S.Shkodrani, P.Moulon, S.Hampali, F.Zhang, J.Fountain, E.Miller, S.Basol,
R.Newcombe,R.Wang,J.J.Engel,andT.Hodan.IntroducingHOT3D:Anegocentricdataset
for3dhandandobjecttracking. arXivpreprintarXiv:2406.09598,2024.
11

[37] Y. Liu, Y. Liu, C. Jiang, K. Lyu, W. Wan, H. Shen, B. Liang, Z. Fu, H. Wang, and L. Yi.
HOI4D: A 4d egocentric dataset for category-level human-object interaction. In IEEE/CVF
ConferenceonComputerVisionandPatternRecognition(CVPR),2022.
[38] Y.Liu,H.Yang,X.Si,L.Liu,Z.Li,Y.Zhang,Y.Liu,andL.Yi.TACO:Benchmarkinggener-
alizablebimanualtool-ACtion-objectunderstanding. InIEEE/CVFConferenceonComputer
VisionandPatternRecognition(CVPR),2024.
[39] X.Wang,T.Kwon,M.Rad,B.Pan,I.Chakraborty,S.Andrist,D.Bohus,A.Feniello,B.Tekin,
F.V.Frujeri,N.Joshi,andM.Pollefeys. HoloAssist: Anegocentrichumaninteractiondataset
forinteractiveAIassistantsintherealworld. InIEEE/CVFInternationalConferenceonCom-
puterVision(ICCV),2023.
[40] G.Zhang,Q.Xu,H.Zhang,J.Ma,L.He,Y.Bao,Z.Ping,Z.Yuan,C.Lu,C.Yuan,T.Liang,
X.Tian,M.Shao,F.Zhang,M.Ding,Y.Gao,H.Zhao,H.Zhao,andH.Xu. UniDex: Arobot
foundation suite for universal dexterous hand control from egocentric human videos. arXiv
preprintarXiv:2603.22264,2026.
[41] S. Lee, Y.Jung, I. Chun, Y.-C. Lee, Z.Cai, H. Huang, A. Talreja, T.D. Dao, Y. Liang, J.-B.
Huang, and F. Huang. TraceGen: World modeling in 3d trace-space enables learning from
cross-embodimentvideos. arXivpreprintarXiv:2511.21690,2025.
[42] C. Yuan, C. Wen, T. Zhang, and Y. Gao. General flow as foundation affordance for scal-
able robot learning. In 8th Annual Conference on Robot Learning, 2024. URL https:
//openreview.net/forum?id=nmEt0ci8hi.
[43] L. Y. Zhu, P. Kuppili, R. Punamiya, P. Aphiwetsa, D. Patel, S. Kareer, S. Ha, and D. Xu.
EMMA:Scalingmobilemanipulationviaegocentrichumandata. IEEERoboticsandAutoma-
tionLetters,2025.
[44] S.Kareer,K.Pertsch,J.Darpinian,J.Hoffman,D.Xu,S.Levine,C.Finn,andS.Nair. Emer-
genceofhumantorobottransferinvision-language-actionmodels. Preprint,2025.
[45] H.Kim,J.Kang,H.Kang,M.Cho,S.J.Kim,andY.Lee.Uniskill:Imitatinghumanvideosvia
cross-embodimentskillrepresentations. In9thAnnualConferenceonRobotLearning,2025.
URLhttps://openreview.net/forum?id=EgSDP6AOF1.
[46] I. Guzey, H. Qi, J. Urain, C. Wang, J. Yin, K. Bodduluri, M. Lambeta, L. Pinto, A. Rai,
J.Malik,T.Wu,A.Sharma,andH.Bharadhwaj. Dexterityfromsmartlenses: Multi-fingered
robotmanipulationwithin-the-wildhumandemonstrations. arXivpreprintarXiv:2511.16661,
2025.
[47] A. Singh, K. Torshizi, K. Habib, K. Yu, R. Gao, and P. Tokekar. Afford2Act: Affordance-
guided automatic keypoint selection for generalizable and lightweight robotic manipulation.
arXivpreprintarXiv:2510.01433,2025.
[48] C.-C. Hsu, B. Wen, J. Xu, Y. Narang, X. Wang, Y. Zhu, J. Biswas, and S. Birchfield.
SPOT: SE(3) pose trajectory diffusion for object-centric manipulation. arXiv preprint
arXiv:2411.00965,2024.
[49] Y. Zou, C. Shi, W. Yu, H. Xue, J. Lv, Y. Pan, C. Wen, and C. Lu. ActiveGlasses: Learn-
ing manipulation with active vision from ego-centric human demonstration. arXiv preprint
arXiv:2604.08534,2026.
[50] Z.-H. Yin, S. Yang, and P. Abbeel. Object-centric 3d motion field for robot learning from
humanvideos. arXivpreprintarXiv:2506.04227,2025.
[51] J.Shi,Z.Zhao,T.Wang,I.Pedroza,A.Luo,J.Wang,J.Ma,andD.Jayaraman. ZeroMimic:
Distillingroboticmanipulationskillsfromwebvideos. InIEEEInternationalConferenceon
RoboticsandAutomation(ICRA),2025.
12

[52] S. Park, H. Bharadhwaj, and S. Tulsiani. DemoDiffusion: One-shot human imitation using
pre-traineddiffusionpolicy. arXivpreprintarXiv:2506.20668,2025.
[53] R.Shah,S.Liu,Q.Wang,Z.Jiang,S.Kumar,M.Seo,R.Mart´ın-Mart´ın,andY.Zhu. Mim-
icDroid: In-contextlearningforhumanoidrobotmanipulationfromhumanplayvideos. arXiv
preprintarXiv:2509.09769,2025.
[54] H.Chen,T.Dong,T.Wu,L.Wang,Y.Jangir,Y.Niu,Y.Ye,H.Bharadhwaj,Z.Erickson,and
J. Ichnowski. Dexterous manipulation policies from RGB human videos via 3d hand-object
trajectoryreconstruction. arXivpreprintarXiv:2602.09013,2026.
[55] J. Shi, J. Smith, J. Qian, and D. Jayaraman. Points2Reward: Robotic manipulation rewards
fromjustonevideo. InRSSWorkshoponSemanticRobotics(SemRob),2025.
[56] B. Wang, N. Sridhar, C. Feng, M. van der Merwe, A. Fishman, N. Fazeli, and J. J. Park.
This&that: Language-gesture controlled video generation for robot planning. In 2025 IEEE
InternationalConferenceonRoboticsandAutomation(ICRA),pages12842–12849,2025.doi:
10.1109/ICRA55743.2025.11128780.
[57] H.Xiong, Q.Li, Y.-C.Chen, H.Bharadhwaj, S.Sinha, andA.Garg. Learningbywatching:
Physicalimitationofmanipulationskillsfromhumanvideos. In2021IEEE/RSJInternational
ConferenceonIntelligentRobotsandSystems(IROS),pages7827–7834,2021. doi:10.1109/
IROS51168.2021.9636080.
[58] R.Suvorov,E.Logacheva,A.Mashikhin,A.Remizova,A.Ashukha,A.Silvestrov,N.Kong,
H. Goka, K. Park, and V. Lempitsky. Resolution-robust large mask inpainting with Fourier
convolutions. InIEEE/CVFWinterConferenceonApplicationsofComputerVision(WACV),
2022.
[59] S.Liu,Z.Zeng,T.Ren,F.Li,H.Zhang,J.Yang,Q.Jiang,C.Li,J.Yang,H.Su,J.Zhu,and
L.Zhang. GroundingDINO:MarryingDINOwithgroundedpre-trainingforopen-setobject
detection. InEuropeanConferenceonComputerVision(ECCV),2024.
[60] N. Ravi, V. Gabeur, Y.-T. Hu, R. Hu, C. Ryali, T. Ma, H. Khedr, R. Ra¨dle, C. Rolland,
L. Gustafson, E. Mintun, J. Pan, K. V. Alwala, N. Carion, C.-Y. Wu, R. Girshick, P. Dolla´r,
and C. Feichtenhofer. SAM 2: Segment anything in images and videos. arXiv preprint
arXiv:2408.00714,2024.
[61] N.Karaev,I.Rocco,B.Graham,N.Neverova,A.Vedaldi,andC.Rupprecht. CoTracker: Itis
bettertotracktogether. InEuropeanConferenceonComputerVision(ECCV),2024.
[62] Z. Wang, Z. Zhang, J. Xu, J. Wang, T. Pang, C. Du, H. Zhao, and Z. Zhao. Orient anything
V2: Unifyingorientationandrotationunderstanding. InAdvancesinNeuralInformationPro-
cessingSystems(NeurIPS),2025.
[63] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li. On the continuity of rotation representations
in neural networks. In IEEE/CVF Conference on Computer Vision and Pattern Recognition
(CVPR),2019.
[64] X. Liu, C. Gong, and Q. Liu. Flow straight and fast: Learning to generate and transfer data
withrectifiedflow. InInternationalConferenceonLearningRepresentations(ICLR),2023.
[65] R.A.Potamias,J.Zhang,J.Deng,andS.Zafeiriou. WiLoR:End-to-end3dhandlocalization
andreconstructionin-the-wild. arXivpreprintarXiv:2409.12259,2024.
[66] G.Pavlakos,D.Shan,I.Radosavovic,A.Kanazawa,D.Fouhey,andJ.Malik. Reconstructing
handsin3Dwithtransformers. InIEEEConferenceonComputerVisionandPatternRecog-
nition(CVPR),2024.
13

[67] Z.Yu,S.Zafeiriou,andT.Birdal. Dyn-HaMR:Recovering4dinteractinghandmotionfroma
dynamiccamera. arXivpreprintarXiv:2412.12861,2025.
[68] J.Zhang,J.Deng,C.Ma,andR.A.Potamias. HaWoR:World-spacehandmotionreconstruc-
tionfromegocentricvideos. arXivpreprintarXiv:2501.02973,2025.
[69] C.Lugaresi,J.Tang,H.Nash,C.McClanahan,E.Uboweja,M.Hays,F.Zhang,C.-L.Chang,
M. G. Yong, J. Lee, W.-T. Chang, W. Hua, M. Georg, and M. Grundmann. MediaPipe: A
frameworkforbuildingperceptionpipelines. arXivpreprintarXiv:1906.08172,2019.
[70] X.Zhang,Z.Kou,C.Qin,M.Huang,E.Ristani,A.KumarLele,L.Chen,K.He,A.Boularias,
and L. Guan. Glove2Hand: Synthesizing natural hand-object interaction from multi-modal
sensinggloves. arXivpreprintarXiv:2603.20850,2026.
[71] A. Sarker, Z. Kou, E. Ristani, L. Guan, and T. Niehues. Real-time hand pose tracking using
6-axis IMUs. In ACM/IEEE International Conference on Human-Robot Interaction (HRI),
2026.
14

Appendix
A DataCollectionDetails
A.1 AriaGen1Glasses
Aria Gen1 recording configuration. We record every hu-
man demonstration with Project Aria Gen1 glasses, configured
throughtheofficialProjectAriaMobileAppwiththesensorpro-
filelistedbelow:
• RGB:30fpsat2MP.
• SLAM:2×monochromecameras,30fpsatVGA.
• ET(eyetracking): 2×cameras,10fpsatQVGA.
• IMUs: two6-axisIMUssampledat1000Hzand800Hz.
• Magnetometer, barometer, 7-mic audio array, GPS, Wi-
Fi,andBLE:allenabledforsynchronizationmetadataand
environmentalcontext.
All streams are hardware-timestamped on-device and synchro-
nizedtoacommonAriaclock,soeverymodalityistime-aligned
atthemillisecondlevel. Fig.11: Datacollectionsetup.
AriaMachinePerceptionServices. Ontopoftherawrecord-
ings, Aria’s cloud-hosted Machine Perception Services (MPS) [7] post-process each capture into
metric,ready-to-usesignals. TwoMPSoutputsarecriticalforourpipeline:
• Closed-looptrajectory. Theclosed-loopSLAMoutputfusesthetwomonochromeSLAMcam-
eras and the two IMUs and applies loop closure plus global optimization to yield a globally
consistent, drift-corrected6-DoFdevicetrajectoryinagravity-alignedworldframe. Wequery
thistrajectoryateveryRGBframetoobtainthecalibratedcameraextrinsicsusedfortriangula-
tion(App.B.1)andtolifteveryhandkeypointintotheworldframeconsumedbyICT(Sec.3.3).
• Handtracking.TheMPShandtrackerjointlyprocessesthestereoSLAMcamerastoproduce21
3Dkeypointsperhand(fiveperfingerplusthewrist),reporteddirectlyintheworldframewith
per-keypointconfidencescores. Thissuppliesthe3Dhandskeletonconsumedbyourhand-to-
gripperretargeting(App.B.3).
Together,theclosed-looptrajectoryandthehandtrackerprovideametric6-DoFcameraposeanda
3Dhandskeletonateveryframe,withoutanycalibrationorsceneinstrumentationbeyondwearing
theglasses.
A.2 TaskDetails
WeevaluateHumanEgoonfourreal-worldmanipulationtasksspanningpick-and-place,multi-step
bimanual coordination, contact-rich reasoning, and sustained rotational control (Fig. 3). For each
taskwedescribethescene,per-trialrandomization,targetbehavior,andsuccess/failurecriteriaused
toscorethe40trialsperconditionreportedinthemainpaper.
Serve Bread. Scene. A croissant and a dinner plate sit on a tabletop, plate on the left and bread
on the right. Randomization. Across trials we independently randomize (i) the horizontal offset
betweenthetwoobjects,sampledfrom[0,50]cm,and(ii)theirdepthsalongthetable’sfront–back
axis, sothepairisgenerallynot colinear. Therightarmstartsfromanarbitrary, non-alignedpose
abovethebread. Targetbehavior. Graspthecroissantfromabove,liftitclearofthetable,transport
ittoareleaseposeabovethecenteroftheplate,andopenthegripper. Success. Thecroissantcomes
torestontheplate,inanyorientation. Failure. (a)thebreadendsupoutsidetheplate(onthetable,
drapedovertherim,orknockedoff);or(b)thebreadslipsfromthegripperduringtransport.
DownstackCups. Scene. Threecupsofdistinctcolorsonatabletop: awhitecupatbottom-right,
a dark-blue cup at bottom-left, and a light-blue cup stacked on top of the white cup. The table
height and the absolute position of the cup group are varied across trials. Randomization. The
15

horizontalgapbetweenthewhiteanddark-bluecupsisdrawnfrom[0,1]cm; thelight-bluecupis
jitteredleft/rightwithin[0,2]cmontopofthewhitecup. Targetbehavior. Athree-stepsequence:
(1)Topple—knockthelight-bluecupsidewayssoitlandsontopofthedark-bluecup;(2)Grasp—
swing over to the white cup and grasp it from above; (3) Cover—lower the white cup onto the
dark-blue/light-bluestackandrelease,formingathree-cuptowerontheleft(dark-blue/light-blue/
white,bottom-to-top). Success. Thethreecupsendintheintendedstablestackontheleft. Failure.
(a) the light-blue cup is never contacted; (b) it is toppled but does not land on the dark-blue cup;
(c) the white cup is not grasped; or (d) the white cup is not correctly placed on the stack (misses
it, topples it, or lands off-axis so the tower collapses). Early errors compound, so the policy must
succeedateverysub-stage.
WaterFlowers. Scene. Awall-mountedfaucetstandsatthefrontoftheworkspace,withasunken
sinkrecessed∼10cmbelowthetabletopdirectlyunderneath. Aflowerpotfilledwithfreshflowers
sitsinsidethesink.Randomization.Thepotisplacedatoneofthreequalitativelydifferentpositions
inthesink(top-left,middle,orbottom-right);thefaucetisfreetorotateaboutitsverticalaxiswithin
[−15◦,+15◦]. Targetbehavior. Coordinatedbimanualexecutionwithstricttemporalordering. Left
arm(sprayhead):graspthepull-outsprayhead,pullit∼15cmdownwardoutofthefaucetsocket,
and hold the nozzle 3–5cm above the center of the flower pot, pointed downward. Right arm
(handle): remain visible in a stationary pre-grasp pose near the faucet handle while the left arm
works; once the left arm is in place, grasp the handle and flick it to the right by 3–5cm to open
thevalve,sowaterflowsontotheflowers. Success. Theleftarmholdsthesprayheadoverthepot
whiletherightarmhasopenedthevalveandwaterpoursontotheflowers. Failure. Leftarm:(a)the
sprayheadisnotgraspedornotpulleddown;(b)itslipsduringpull-outortransport;or(c)itisnot
positioneddirectlyabovethepot. Rightarm: (a)thehandleisnotgrasped;or(b)itisnotflickedfar
enoughtoopenthevalve,orslipsbeforewaterflows.
AdjustTable. Scene. Theoperatorfacesanadjustabletablewhoseheightiscontrolledbyahand
crankprotruding fromits side, orientedroughly horizontally. Randomization. The initialangle of
thecrankhandleaboutitsrotationaxisisjitteredby±10◦ aroundhorizontal. Targetbehavior. The
right arm (1) approaches the crank handle from an arbitrary initial pose and grasps it firmly, then
(2) performs a continuous counter-clockwise rotation about the crank axis, completing three full
revolutions(3×360◦)withoutreleasingthehandle. Success. Allthreerevolutionsarecompleted
whilethegraspismaintainedthroughout. Failure. (a)thehandleisnevergrasped;or(b)thehandle
slipsfromthegripperduringtherotation,beforethreefullrevolutionsarecompleted.
Per-demonstrationcollectiontime. Acrossallfourtasks,asinglehumanegocentricdemonstra-
tiontakesapproximately30–40seconds,whileamatchedteleoperateddemonstrationonthesame
hardware takes 60–70 seconds. The roughly 2× gap reflects that everyday human manipulation
is naturally faster and more dexterous than teleoperation through a piloting interface; combined
withtheembodiment-agnosticrepresentation,thismakeshumanvideoasubstantiallymoresample-
efficienttrainingsourceperminuteofcollection.
Additional tasks (demonstration-only). Beyond the four tasks evaluated quantitatively above,
wealsocollecteddataandtrainedHumanEgopoliciesonfiveadditionaltasks,illustratingthespeed
withwhichourpipelinecanbebroughttobearonnewbehaviors. Thesetasksappearinoursupple-
mentarydemonstrationvideosbutarenotpartofthequantitativeevaluationinSec.4.1.
Charge Devices. The operator places a smartwatch, a pair of earphones, and a phone from the
tabletop onto their corresponding magnetic chargers. Each item is treated as a separate sub-task,
followingaGRASP→TRANSPORT→RELEASE-ON-PADtemplate;wecollectandtrainadedicated
modelforeachsub-task.
UnscrewCap. Abimanualtask: onehandgraspsandstabilizesthebottlebodywhiletheotherhand
graspsthecap,rotatesitthrough2–3fullrevolutionstodisengagethethread,andliftsthefreedcap
aside.
16

OpenDoor. Theoperatoropensaself-closingdoorfittedwithalever-stylehandle. Theactinghand
graspsthelever,rotatesitclockwisetoreleasethelatch,andthenpullsthedooroutwardagainstits
returnspring.
Open Cabinet. A bimanual task: both hands simultaneously grasp a pair of vertically oriented
handlesonacabinetdoorandpullitopenalonganoutwardarc.
GrabTissue. Theoperatorpinchesasinglesheetoftissuefromatissuebox,liftsitupwardandthen
translatesitlaterallytofullyextractit,andplacesitonthetable.
B PreprocessingDetails
B.1 Triangulation
Aria Gen1 glasses lack a depth sensor, so we recover each object’s 3D position by triangulating
tracked 2D keypoints across frames, treating the moving head-mounted camera as a multi-view
systemwithcalibratedextrinsicsgivenbythe6-DoFAriaMPSSLAMpose[7]. Thisrequiresthe
objecttoremainstationaryduringtheobservationwindow;oncemanipulationbegins,theobjectis
freetomove.
Pre-episode scene sweep. Multi-view triangulation requires the same 3D point to be seen from
sufficientlydifferentviewpoints,yetduringmanipulationthehead-mountedcameraisoftennearly
stationarywhileonlythehandsmove,collapsingtheeffectivecamerabaseline. Wethereforeprefix
everydemonstrationwithashortscenesweep: thedemonstratorkeepsthescenestaticandslowly
movestheirheadfor∼1–2seconds(∼30–60frames),usingeitherahorizontalleft-to-rightpanora
forwardwalk-intowardtheobject,beforeproceedingtotheactualmanipulation.
Multi-view triangulation from 2D tracks. For each object we detect it in the first sweep frame
withGroundingDINO[59],segmentitwithSAM2[60],sampleN keypointsontheresultingmask,
and track them through the F sweep frames with CoTracker3 [61]. Let K ∈ R3×3 be the RGB
intrinsics,T =[R |t ]thecamera-to-worldSLAMposeofframei,andP =K[R⊤| −R⊤t ]∈
i i i i i i i
R3×4 the corresponding world-to-image projection. A track {u(i)}F and the unknown 3D point
n i=1
X ∈R4(homogeneous)satisfyu(i)×P X =0,whichyieldstwolinearequationsperframe:
n n i n
(cid:34) (cid:35)
u(i)p(i)⊤−p(i)⊤
n 3 1 X = 0, (4)
v(i)p(i)⊤−p(i)⊤ n
n 3 2
wherep(i)⊤isthej-throwofP .Stacking(4)acrossallF framesgivesa2F×4systemA X =0;
j i n n
we solve it in the least-squares sense via SVD by taking the right singular vector of A with the
n
smallest singular value and dehomogenizing to recover x ∈ R3. The object position is then the
n
centroidp = 1 (cid:80)N x ,whichcancelsper-pointtriangulationnoise.
obj N n=1 n
B.2 PhaseDetection
ArawAriarecordinginterleavesactivemanipulationwithnon-manipulationsegments—walkingup
to the workspace, the pre-episode scene sweep (App. B.1), and stepping back once the task ends.
Only the manipulation portions carry clean hand–object dynamics, so we run an automatic phase
detectionstepthatsegmentseveryrecordingintokinematicmodesandkeepsonlythemanipulation
framesfortraining.
Phase taxonomy. Each frame is assigned one of five modes: (0) MANIP—demonstrator stands
still and actively manipulates the scene; (1) FORWARD—linear walking; (2) ROTATE—in-place
head/bodyrotation(e.g.thescenesweep);(3)TRANSITION—shortbuffersbetweenadjacentmodes;
(4)FINISHED—sustainedfinalholdattheendoftherecording.
Segmentation signals and training-data selection. Phases are computed from two streams: the
6-DoF head trajectory from Aria SLAM (body motion) and the 3D hand trajectory from the hand
tracker(manipulationmotion). AframeentersMANIPwhentheheadlinearandangularspeedssi-
multaneouslyfallbelowv
stop
=0.03m/sandw
stop
=0.15rad/sfor≥15consecutiveframes;ROTATE
17

requires ∥ω ∥ > 0.10rad/s with ∥v ∥ < 0.08m/s; FORWARD collects the remaining high-
|     | head |     |     | head |     |     |     |     |     |     |
| --- | ---- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
linear-speedframes; TRANSITION fillsa10-framebufferateverymodechange; and FINISHED is
declaredoncethetrailingstoplastsfor≥30frames. WeadditionallyrefineMANIPwithhandkine-
matics: acandidateframeisdemotedto TRANSITION iftheaveragehandspeedexceeds0.15m/s
overa5-framewindow,trimmingreaching/retractingmotionawayfromthemanipulationcore. The
trainingpipelinethenkeepsonlyMANIP(0)andFINISHED(4),droppingFORWARD,ROTATE,and
TRANSITION, so the scene sweep, navigation, and mode-change buffers never reach the training
signal.
B.3 Hand-to-GripperTransfer
| To treat                             | a human        | egocentric | video        | as robot          | data,     | every    | frame  |     |     |     |
| ------------------------------------ | -------------- | ---------- | ------------ | ----------------- | --------- | -------- | ------ | --- | --- | --- |
| of the demonstration                 |                | must       | carry        | an end-effector   |           | target   | that a |     |     |     |
| parallel-jawrobotcanactuallyexecute. |                |            |              | Thehumanhand,how- |           |          |        |     |     |     |
| ever, has                            | 21 articulated | keypoints  |              | and a morphology  |           | very     | dif-   |     |     |     |
| ferent from                          | a 2-finger     | gripper,   | so           | the raw           | hand pose | cannot   | be     |     |     |     |
| passed through                       | directly.      |            | We therefore | retarget          |           | the hand | into   |     |     |     |
SE(3)
| a virtual      | gripper—a | 6-DoF |              | pose   | plus a    | 1-DoF | grasp |     |     |     |
| -------------- | --------- | ----- | ------------ | ------ | --------- | ----- | ----- | --- | --- | --- |
| scalar—derived | from      | a few | anatomically | stable | keypoints |       | after |     |     |     |
ashortmotion-optimizationpipeline.
| Hand keypoint |     | extraction. | We  | start from | the | 21-keypoint |     |     |     |     |
| ------------- | --- | ----------- | --- | ---------- | --- | ----------- | --- | --- | --- | --- |
handskeletonproducedbyAriaMPS[7],whichfusesthestereo
|              |     |     |           |        |         |       |      | Fig.12: Hand-to-grippermap- |     |     |
| ------------ | --- | --- | --------- | ------ | ------- | ----- | ---- | --------------------------- | --- | --- |
| SLAM cameras | and | the | on-device | IMU to | recover | every | key- |                             |     |     |
ping.
point’s3DpositionintheSLAMworldframeateachframe.For
retargetingweuseonlyfivekeypointsperhand(Fig.12): thewrist, thumbMCP,thumbtip, index
MCP,andindextip.
Motion optimization. Raw MPS keypoints are noisy and occasionally drop frames, and feeding
themdirectlyintotheSE(3)constructionproducesjittery,flip-pronetrajectories. Wethereforerun
a short optimization pipeline: (1) Confidence masking—we drop any keypoint whose MPS confi-
dence falls below 0.8 and discard detection segments shorter than 30 consecutive frames as likely
ghostdetections;(2)Gapinterpolation—shortmissingintervals(≤10frames)arefilledwithlinear
interpolationonpositionsandSLERPonorientations,sothelatersmootherseesadensesequence;
(3)Savitzky–Golaypositionsmoothing—weapplyanSGfilterwithwindowsize21andpolynomial
order2tothefiveretargetkeypoints,removinghigh-frequencyjitterwhilepreservingmanipulation-
relevant accelerations; (4) EMA orientation smoothing—we apply an exponential moving average
withα =α =0.15totheX-andY-axesofthegripperframe(definedbelow),re-orthonormalize
| x   | y   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
viaGram–Schmidtaftereachupdate,andenforcesignconsistencyacrossadjacentframestoprevent
spurious180◦flips.
End-effector position. We take the midpoint of the thumb tip and the index tip as the gripper
position,whichnaturallycorrespondstothecenterofaparallel-jawgrasp:
|     |     |     |     | p = 1(cid:0) | p        | +p  | (cid:1) . |     |     | (5) |
| --- | --- | --- | --- | ------------ | -------- | --- | --------- | --- | --- | --- |
|     |     |     |     | ee           | thumbtip |     | indextip  |     |     |     |
2
End-effectororientation. Choosinganorientationthatisbothaccurateandstablethroughpinch
graspsisthesubtlepartofretargeting;twonaturalalternativesbothfail. (i)Rawwristpose: using
theMPSwristorientationdirectlyasthegripperframeisinaccurate,becausetheanatomicalwrist
frameisnotalignedwiththethumb–indexactionaxisthatthegripperactuallyuses. (ii)Wrist-to-
fingertip-midpoint: definingtheforwardaxisaswrist→mid(thumbtip,indextip)andthejawaxis
as thumbtip → indextip works when the hand is open but becomes degenerate at the moment of
grasp—the two fingertips converge to nearly the same point, so the jaw axis collapses to a near-
zero vector and the frame is ill-defined. We instead build the gripper frame from the MCP joints,
whichremainwell-separatedthroughoutthefullpinchcycle.Writingp ,p ,p forthewrist,
|     |     |     |     |     |     |     |     | w tMCP | iMCP |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ---- | --- |
thumb-MCP,andindex-MCPpositions,weconstruct
(cid:92)
|     | x =p | (cid:92) | −p   | , y | =y˜−( | y˜⊤x | )x ,  | z =x  | ×y , | (6) |
| --- | ---- | -------- | ---- | --- | ----- | ---- | ----- | ----- | ---- | --- |
|     | ee   | iMCP     | tMCP | ee  |       |      | ee ee | ee ee | ee   |     |
18

wherey˜ = 1(p +p )−p istherawwrist-to-MCP-midpointvectorand((cid:99)·)denotesunit
2 tMCP iMCP w
normalization. Intuitively,y istheforwardaxis(wrist→MCPmidpoint),x isthejawopening
ee ee
axis (thumb MCP → index MCP), and z is the orthogonal complement. The rotation R =
ee ee
[x |y |z ] ∈ SO(3) together with the position p from Eq. (5) gives the SE(3) end-effector
ee ee ee ee
poseT . BecausethetwoMCPsnevercollapsetoeachotherduringapinch,thisconstructionstays
ee
numericallystableacrossthefullgrasp/releasecycle.
Gripper aperture. We derive the 1-DoF gripper command from the thumb–index fingertip dis-
tance:
(cid:16) (cid:17)
g =clip ∥pthumbtip−pindextip∥−dmin, 0, 1 , (7)
dmax−dmin
where d and d are the closed and fully-open fingertip distances calibrated per user. The
min max
normalizedg isthenmedian-filteredandrunthroughashortflicker-suppressionpasstoproducea
cleanopen/closecommandstream,andbinarizedatdeployment.
C TrainingDetails
C.1 FlowMatchingPolicy
Velocity field and loss. We train a conditional flow matching [33] policy that maps a Gaussian
priorx
0
∼ N(0,I)totheground-truthbimanualactionchunkx
1
∈ RK×Da alongthelinearpath
x = (1−t)x +tx withflowtimet ∼ U(0,1). Thetargetvelocityistheconstantdisplacement
t 0 1
v =x −x ,andtheflow-matchinglossisanMSEoverthepredictedvelocitywithdimension-
target 1 0
wise reweighting: w =5 on position, w =1 on 6D rotation, and w =10 on the grasp logit. We
p r g
also supportan optimal-transport matchingvariant (OT-CFM) that solvesa Hungarian assignment
between noise and action samples within each mini-batch before computing the loss, producing
straightertargetflows;weleaveitoffbydefaultsincewedidnotfindconsistentwinsonourtasks.
Network. Thevelocityfieldv isa6-layer,8-headtransformerdecoderwithembeddingdimension
θ
384anddropout0.05. Eachaction-chunktokenattends(viaself-attention)totherestofthechunk
and (via cross-attention) to the conditioning context. Context is built from two streams: (i) the
RGBframe, embeddedwitha16×16patchembeddingona240×320inputandasinusoidaltime
embedding fused through a small MLP; and (ii) the state tokens, i.e., the per-entity ICT tokens
describedinSec.3.3,linearlyprojectedto384channels.
Auxiliaryheads. Threedenseauxiliaryobjectivessharethecontextencoderwiththevelocityfield
(Sec.3.4). Theobject-dynamicsheadpredictsthe9-Dfutureposetraceofthemanipulatedobject
and is trained with 0.5(w ,w )-weighted MSE; the 2D visual-foresight head emits K×3×2 nor-
p r
malized image coordinates of three anchor keypoints through a shallow deconvolution stack with
loss weight w =20; and the temporal-consistency head predicts the hand tokens K steps ahead
f
withamaskedMSEweightedbyw ∈[0.1,1.0]. Allthreetargetsareproducedautomaticallybythe
c
perceptionpipeline,soeachdemonstrationyieldsadensemulti-tasksignalwithoutextralabeling.
Additionaltricks. Twolightweighttrainingtricksfurtherstabilizelearningfromminutesofdata.
Regionattentionbiasestheimagecross-attentiontowardthecurrentlyactivemanipulationanchor:
given the anchor’s 2D image projection (u ,v ), we multiply the attention logits by a Gaussian
0 0
spotlight
(cid:16) (u−u )2+(v−v )2(cid:17)
w(u,v)=exp − 0 0 , (8)
2σ2
whose spatial scale σ is a learnable parameter, softly focusing the encoder on task-relevant image
regions without hard-cropping. State-noise injection perturbs every hand token during training,
s˜ = s + ϵ with ϵ ∼ N(0,Σ ) and separate standard deviations on the position, 6D rotation,
t t s
and grasp channels, which makes the policy robust to the small perception noise it encounters at
deployment.
Optimization recipe. We train with AdamW at a base learning rate of 10−4, cosine decay with
200-stepwarmup, minimum-LRratio0.05, batchsize32, and400epochs. Weclipgradientnorm
at1.0, usebfloat16mixedprecision, andkeepanexponentialmovingaverageoftheweightswith
decay0.999forevaluationanddeployment.
19

Data augmentation. To expand the effective training distribution from only ∼40min of human
videopertask,weapplyacocktailofaugmentationsontheflyinthedataloader,groupedintothree
families.(i)ImageaugmentationsontheRGBstream.Photometricjitter(p=0.8)randomlyperturbs
brightness(±0.20),contrast(±0.20),andgamma(±0.15),addsGaussianpixelnoise(σ=0.02),op-
tionally converts the frame to grayscale (p=0.1), and jitters HSV hue by ±10 and saturation by
[0.6,1.4]. A random resized crop (p=0.5) draws a sub-window with scale in [0.7,1.0] and aspect
ratioin[0.9,1.1]beforeresizingbacktothenetworkinputsize. AGaussianblurwitha3×3ker-
nel is applied with p=0.15, and random erasing (p=0.5) overlays 3–8 black cutout patches each
covering 5–20% of the frame area. (ii) Action-target augmentation. We additively perturb every
targetposeintheactionchunkwithGaussiannoise—σ =1mmontranslationandσ =0.5◦ on
pos rot
rotation—before the flow-matching loss is computed, which regularizes the velocity field against
small tracking noise in the labels. (iii) Temporal augmentation. With p=0.5 we apply sub-step
interpolation: adjacent state/action frames are linearly blended at a random α ∈ [0,1], effectively
densifyingthetemporalgridatnoextracollectioncost.
D InferenceDetails
D.1 RobotInferenceSetup
Apart from the zero-shot generalization study
(Sec.4.3),allreal-worldexperimentsinthemain
paper use the single inference setup shown in
Fig.13: twoTrossenWidowXAIarmsmounted
side-by-side on a shared workbench, forming a
bimanual platform that handles both single-arm
and two-arm tasks without any hardware change Fig.13: Robotinferencesetup.
betweentasks. EachWidowXAIarmisa6-DoFparallel-jawmanipulatorwitha∼1.5kgpayload
atfullreachand±1mmend-effectorrepeatability. ForvisualinputweuseasingleIntelRealSense
D405mountedtop-downabovetheworkspace;itsRGBstreamisthesoleobservationconsumedby
HumanEgo. EachWidowXAIarmalsoshipswithabuilt-inwristcamera, butwedeliberatelydo
not use it for HumanEgo: the robot-teleoperation ACT baseline [28] in Sec. 4.1, in contrast, does
consumethewristcamerasaspartofitsstandardobservationinterface.
D.2 FlowMatchingRolloutandControl
ODE rollout. At test time we integrate the learned velocity field with a fixed-step Euler solver
using 20 inference steps: starting from a noise sample x ∼ N(0,I) drawn once at policy load
0
time, weiteratex ← x +v (x ,t,s )∆twith∆t = 1/20, yieldingaK=50-stepbimanual
t+∆t t θ t t
action chunk in one forward pass per re-plan. Predictions are unpacked dimension-wise into per-
hand position, 6D rotation, and grasp logit, with positions denormalized by the dataset mean/std,
rotationsprojectedbacktoSO(3)vianormalize-then-Gram–Schmidtonthe6Drepresentation,and
graspspassedthroughasigmoid.
Actionchunkingandcontrol. Thecontrollerre-plansateverycycle(10Hz),keepingatmostone
predictioninhistoryandexecutingoneactionpercycle. Astepstrideof2sub-samplesthechunkso
theeffectiveexecutedrateis5Hz,andalook-aheadoffsetof25stepsletsthecontrollerquerythe
chunkslightlyaheadofthecurrentexecutionindextomaskplanninglatency. Forgraspweusean
any-over-horizonrule: thegripperclosesassoonasanystepinthecurrentchunkpredictsagrasp
probability above 0.6; an optional grasp-latchmode additionally locks the gripper closed after the
firstgraspeventtopreventaccidentalmid-taskreleases.
Smoothing and safety. To hide small noise in the predicted SE(3) stream we apply an EMA on
positions (α=0.5) and quaternion SLERP on rotations before streaming targets to the arms, and a
trajectory-overlap blend (smoothing parameter 12) to avoid jerky starts/stops between consecutive
chunks. Finally,asafetycagelimitseachper-cycletargetdisplacementto≤0.08minpositionand
≤0.02rad in rotation to guard against sudden outliers; we did not observe any safety-cage clamp
duringnormalrolloutsinourexperiments.
20

E AdditionalExperimentsAnalysis
E.1 HandTrackingMethodStudy
Hand Tracking Comparison
|     | Midpoint Translational Jerk |     |     |     |     | Midpoint Angular Jerk       |     |     |     | All-keypoint Jerk            |     |
| --- | --------------------------- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | ---------------------------- | --- |
|     | gripper position  log scale |     |     |     |     | gripper rotation  log scale |     |     |     | mean over 21 kpts  log scale |     |
103
| 103 |     |     |     |     | 100 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ssenhtoomS
| 3emarf/mm |     |     |     |     |     |     |     | 3emarf/mm | 102 |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- |
3emarf/dar
102
101
101
101
|     |     |     |     |     | 102 |     |     |     | 100 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Aria-MPS WiLoR HaMeR Aria-MPS WiLoR HaMeR Aria-MPS WiLoR HaMeR
|     |                                 |     | MediaPipe |     |     |                             | MediaPipe |     |     |                | MediaPipe |
| --- | ------------------------------- | --- | --------- | --- | --- | --------------------------- | --------- | --- | --- | -------------- | --------- |
|     | Per-keypoint Error  vs Aria-MPS |     |           |     |     | Rotation Error  vs Aria-MPS |           |     |     | Detection Rate |           |
Procrustes-aligned (shape error per joint) Procrustes-aligned residual fraction of frames with valid hand
70
| ycaruccA |     |     |     |     |     |     |     | Aria-MPS |     |     | 95.2% |
| -------- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | ----- |
60
)ged( rorrE noitatoR
50
|     |     |     |     |     |     |     |     | WiLoR |     |     | 86.9% |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ----- |
40
30
|     |     |     |     |     |     |     |     | HaMeR |     |     | 92.4% |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ----- |
20
10
|     | WiLoR | HaMeR | MediaPipe |     |     |     |     |           |     |     |       |
| --- | ----- | ----- | --------- | --- | --- | --- | --- | --------- | --- | --- | ----- |
|     |       |       |           |     | 0   |     |     | MediaPipe |     |     | 66.5% |
0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 WiLoR HaMeR MediaPipe 0 20 40 60 80 100 120
|     | Per-keypoint Error (cm) |     |     |     |     |     |     |     |     | Detection Rate (%) |     |
| --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- |
Fig. 14: Hand tracking comparison on Serve Bread (45 demonstrations, ∼45k frames). Top—
Smoothness: per-frame jerk of the gripper midpoint (translational and angular) and of all 21 key-
points(lowerisbetter,logscale). Bottom—Accuracyvs.Aria-MPS:per-keypointshapeerrorafter
Procrustesalignment,residualrotationerroraftersubtractingthesystematicframeoffset,andfrac-
tionofframeswithavalidhanddetection.
Hand Tracking Method Study
Setup. ICTconsumes3Dhandkeypointsasin- Monocular RGB SStteerreeoo  ++  IIMMUU
| put,                                        | so the          | quality           | of the upstream |       | hand     | tracker |                  |       |     | +50pp |     |
| ------------------------------------------- | --------------- | ----------------- | --------------- | ----- | -------- | ------- | ---------------- | ----- | --- | ----- | --- |
|                                             |                 |                   |                 |       |          |         | 100              |       |     |       | 95% |
| directlyaffectswhatthepolicycanlearn.       |                 |                   |                 |       |          | Weiso-  | )%( etaR sseccuS |       |     |       |     |
| late                                        | this dependency |                   | on Serve        | Bread | by       | holding | 75               |       |     |       |     |
| everything                                  |                 | else constant—the |                 | same  | 45       | demon-  |                  |       |     |       |     |
|                                             |                 |                   |                 |       |          |         | 50               |       | 45% |       |     |
| strations                                   | (30min          | total),           | the             | same  | HumanEgo | ar-     |                  | 32.5% |     |       |     |
| chitecture,thesametrainingrecipe—andvarying |                 |                   |                 |       |          |         | 25               |       |     |       |     |
| onlythehand-trackingmodulethatproducesthe   |                 |                   |                 |       |          |         | 0%               |       |     |       |     |
0
|     |     |     |     |     |     |     | MediaPipe | HaMeR | WiLoR |     | Aria-MPS |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----- | ----- | --- | -------- |
action labels. We compare four trackers span- Fig.15: HandTrackingMethodStudy.
| ning | the dominant |     | design | choices | in the | litera- |     |     |     |     |     |
| ---- | ------------ | --- | ------ | ------- | ------ | ------- | --- | --- | --- | --- | --- |
ture: (1) Aria-MPS [7], our default, which fuses the two wide-FoV monochrome SLAM cam-
eras with the on-device IMU through Meta’s MPS pipeline to recover metric 3D keypoints—
note that the central RGB camera is used only for video logging, not for hand tracking; (2)
WiLoR [65], a transformer that regresses MANO parameters from a single RGB crop per frame;
(3)HaMeR[66],astrongmonocularRGBestimatorthatalsopredictsMANOparametersbutpro-
cessesframesindependently—temporalandworld-frameextensionsofthisfamilyhavesincebeen
proposed[67,68];and(4)MediaPipe[69],alightweightmonocularRGBpipelinewhose3Dout-
putsareroot-relativeandhavetobeliftedwiththecameradepth. Beyondthesevision-onlytrack-
ers, instrumented alternatives recover hand pose from multi-modal sensing gloves [70] or 6-axis
IMUsystems[71],butrequirespecializedhardwareonthedemonstratorandfalloutsideourzero-
instrumentationcollectionsetup.Foreachtrackerwere-runthedatapreprocessing,trainHumanEgo
fromscratch,andevaluate40real-worldtrialsonServeBread(Fig.15). Aria-MPSistreatedasthe
referenceforallalignment-stylemetricsinFig.14.
Results. Fig.15showsreal-worldsuccesscollapsingby95→45→32.5→0%aswemovefrom
stereoAria-MPStomonoculartrackers,andFig.14explainswhy. Wehighlightfourobservations.
21

Stereodepthisdecisivefordownstreamsuccess.Real-worldsuccessdropsfrom95%(Aria-MPS)
toatmost45%(WiLoR)themomentwereplacestereowithmonocularRGB.Monocularnetworks
are inherently scale-ambiguous along the depth axis, producing a 5–11cm systematic depth offset
thatpropagatesdirectlyintotheICTreferenceframe,sothepolicyneverlearnsaconsistentgrasp.
Smoothnessandtrackingpersistence—notposeaccuracyperse—separatethesurvivingbase-
lines. AfterProcrustesalignmenttheper-keypointresidualerrorisnearlyidenticalforHaMeRand
WiLoR (1.4cm vs. 1.4cm; both dominated by the shared MANO inductive bias) and only mod-
estlyworseforMediaPipe(2.2cm). YetWiLoR(45%)clearlybeatsHaMeR(32.5%). Thegapis
explainedbythesmoothnesspanels:WiLoR’sgripper-midpointjerkismorethananorderofmagni-
tudelowerthanHaMeR’s—itsper-framepredictionshappentobefarmoretemporallystable—and
its detection rate is 86.9% vs. MediaPipe’s 66.5%. A jittery or intermittently missing trajectory
teachesthepolicyincoherentactionlabels.
TheMANOpriorisadouble-edgedsword. HaMeRandWiLoRshowessentiallyidenticalper-
keypoint Procrustes residuals (Fig. 14, bottom-left): the colored patterns on the two hand skele-
tonsarevisuallyindistinguishable. Thisisnotacoincidence—bothnetworksregressMANOpose
parameters and inherit the same canonical bone proportions. The shared shape prior means their
residualshapeerrorsarecorrelatedbyconstruction,whilemethodswithoutaparametricconstraint
(Aria-MPS,MediaPipe)deviateindifferentways. Thisexplainswhyposeaccuracyaloneisapoor
predictorofdownstreampolicysuccess.
MediaPipefailsentirely. With0%real-worldsuccessandonly66.5%detectionrate,MediaPipe
cannotproducecoherentactionlabelsevenwiththe ICT representationabsorbingsomenoise. Its
3Doutputisroot-relativeandmustbeliftedwiththecameradepth,andtheliftcollapsesthehand
thicknessto∼7cm(vs.∼16cmforAria),flatteningtheposeinformationthatICTrelieson.
Togethertheseresultspointtoaclearpracticalmessage: investintheperceptionfrontend. Amore
accuratehandtracker—especiallyonethatexploitsstereoorlearneddepth—isthehighest-leverage
upgradeforanypolicythatoperatesonhand-derivedspatialtokens.
E.2 Human-RobotCo-TrainingStudy
Setup. Thedata-efficiencystudy(Sec.4.2)showedthathumandemonstrationsareroughly3.75×
more sample-efficient than robot teleoperation at the same total collection time. Here we ask the
complementary question: when both modalities are available, what is the best mixing ratio? We
hold the total collection time fixed at 30min and vary the fraction of human data from 0% (pure
robotteleoperation,∼45teleopepisodes)to100%(purehumanegocentricvideo,∼45egocentric
demos)in25-ppsteps. Eachbatchissampledwiththecorrespondingratio,sothepolicyseesboth
modalitiesintheintendedproportionateverygradientstep. Thearchitecture,optimizer,schedule,
and number of training steps are kept identical across the five conditions; only the data mixture
changes. Weevaluate40real-worldtrialsonServeBreadpercondition.
100
75
50
25
0
Pure 25% Human 50% Human 75% Human Pure
Robot + 75% Robot + 50% Robot + 25% Robot Human
)%( etaR
sseccuS
Human-Robot Co-Training Study
Results. Real-world success increases mono-
Robot Data HHuummaann DDaattaa
+30pp
tonically as the human-data ratio grows: 65 →
95%
90%
72.5 → 77.5 → 90 → 95% for human ra-
77.5% 72.5% tios of 0/25/50/75/100% (Fig. 16). The pure- 65%
human policy improves over the pure-robot pol-
icy by +30pp—a gap larger than that between
mostofourbaselines. Weextracttwomainfind-
ings.
Even a small slice of human data dominates. Fig.16: Human-RobotCo-TrainingStudy.
Replacing just 25% of the robot teleop with egocentric video already lifts success from 65% to
72.5%(+7.5pp),eventhoughtheabsoluteamountofrobotdatadropsfrom30minto22.5minin
thatcondition.Anaive“moredataisalwaysbetter”viewwouldpredicttheopposite:lessrobotdata
shouldhurt. Insteadthepolicyimproves,indicatingthatthemarginalrobotminutescontributeless
signalthanthemarginalhumanminutes.Thisreproducesthedata-efficiencyconclusion(Sec.4.2)at
22

thelevelofthegradientstep: thepolicyishappierlearningfromasmallamountofcleanegocentric
videothanfromalargeamountofteleoptrajectory.
The more human data, the better—no co-training sweet spot. Across all four transitions the
curve only goes up, and the pure human policy is the global maximum. We find no “sweet spot”
wheremixinginrobotdataoutperformsthehuman-onlycondition—infact75/25(90%)isalready
5ppbelow100/0(95%), soaddingeven7.5minofrobotteleoperationactivelyerodesa22.5min
human dataset. We attribute this to the higher per-minute information density of human demon-
strations documented in Sec. 4.2 (Fig. 6): human videos exhibit higher signal-to-noise ratio, an
order-of-magnitude smoother trajectories, near-zero idle time, and broader spatial coverage than
robotteleoperation. Atafixedcomputeandtimebudget,thepolicyisbestservedbyspendingevery
minuteonhumandata.Combinedwiththeembodiment-invarianceofICT,thismeansapractitioner
deployingHumanEgoshouldnotinvestinrobotteleoperationatall—thesamebudgetcollectedas
egocentrichumanvideoyieldsastrictlybetterpolicy.
E.3 ReferenceFrameStudy
100
75
50
25
0
Anchor Camera Anchor Camera
)%(
etaR
sseccuS
Coordinate Frame Study
4 mins 40 mins
Thechoiceofreferenceframeisakeydesignde-
cisioninICT.Wecomparetwostrategies:(1)the +7.5pp
95%
anchor frame, in which every entity pose—as 87.5%
well as the action trajectory—is expressed rela-
tive to the first object grasped in the trajectory,
+5.0pp
and (2) the camera frame (used in our main ex-
27.5%
22.5%
periments), in which all poses are expressed in
the camera’s coordinate system. The two repre-
sentationsexhibitacleartrade-offwhosebalance Fig.17: CoordinateFrameStudy.
shiftswiththeamountoftrainingdata(Fig.17).
Low-data regime: the anchor frame wins. With few training demonstrations, expressing the
sceneintheanchorframesubstantiallyacceleratespolicylearning. Becausetheanchorframeties
spatial reasoning to a task-relevant object rather than to the camera, the model can recover the
fundamental geometry of manipulation—in particular, the relative pose between the hand and the
target object at the moment of contact—from far fewer demonstrations. This grasping prior is
precisely the bottleneck that limits sample efficiency in many imitation learning settings, and the
anchorframesuppliesastronginductivebiasthatbypassesit. Theresultismarkedlybettergrasp
successanddownstreamtaskcompletionwhenonlyahandfuloftrajectoriesareavailable.
Large-data regime: the camera frame catches up and surpasses anchor frame. As training
data grows, the model has enough signal to recover the same relational geometry directly from
camera-frame observations. At that point, the camera frame becomes the more reliable represen-
tation, for two reasons: (i) it is grounded in the raw sensor and is not contaminated by upstream
perception errors, whereas (ii) the anchor frame inherits noise from the object detection and pose
estimationmodules(GroundingDINO,SAM2,Orient-Anything),whoseerrorsdirectlyperturbev-
erytransformedcoordinate.Empirically,givensufficientdatathecamera-framevariantmatchesand
modestlyexceedstheanchor-framevariantonin-distributionevaluations,becausetheanchor-frame
policyisultimatelyboundedbytheaccuracyofitsupstreamobjectposeestimates.
Theanchorframe’senduringadvantage:camera-poseinvariance. Despitetheasymptoticpar-
ity (or slight inferiority) in raw success rate, the anchor frame retains a property that the camera
framecannotoffer: deployment-timeinvariancetocameraplacement. Becauseeverycoordinateis
expressedrelativetotheobject,theabsolutepositionandorientationofthecameraareirrelevant—
thepolicycanbedeployedwithacameramountedatanyreasonableangle,height,ordistance,and
it will behave identically. In contrast, a camera-frame policy is tied to a specific viewpoint distri-
bution and degrades sharply whenever the camera is repositioned, forcing every new mounting to
triggerfreshdatacollectionorfine-tuning.
23

F Hyperparameters
Table1consolidateseveryhyperparametervaluethatappearsinthemainpaperandtheappendix,
grouped by pipeline stage. Unless explicitly noted, a single value is used across all four tasks, all
trainingruns,andallreal-worldtrials.
Table1: AllhyperparametersusedinHumanEgo. Valuesaresharedacrossthefourtasksunless
noted.
| Parameter |     |     | Value |
| --------- | --- | --- | ----- |
DataCollection(App.A.1,App.A.2)
| Demonstrationspertask                     |     |              | 60          |
| ----------------------------------------- | --- | ------------ | ----------- |
| Totalhuman-videotimepertask               |     |              | 40min       |
| RGBstreamrate/resolution                  |     |              | 30fps/2MP   |
| SLAMcameras:count,rate,resolution         |     |              | 2,30fps,VGA |
| Eye-trackingcameras:count,rate,resolution |     | 2,10fps,QVGA |             |
| IMUrates                                  |     | 1000Hz,800Hz |             |
| Pre-episodescene-sweepduration            |     |              | 1–2s        |
| Scene-sweepframecount                     |     |              | 30–60       |
PhaseDetection(App.B.2)
| Headlinear-speedstopthresholdv  |     | stop    | 0.03m/s   |
| ------------------------------- | --- | ------- | --------- |
| Headangular-speedstopthresholdw |     | stop    | 0.15rad/s |
| Minimumstop-holdduration        |     |         | 15frames  |
| Rotatetriggerw                  | rot |         | 0.10rad/s |
| Rotatemaxlinearspeedv           |     | rot,max | 0.08m/s   |
| Transitionbuffer                |     |         | 10frames  |
| Hand-velocitydemotionthresholdv |     | hand    | 0.15m/s   |
| Hand-velocityaveragingwindow    |     |         | 5frames   |
| Finished-stoplength             |     |         | 30frames  |
Hand-to-GripperRetargeting(App.B.3)
| Retargetkeypointsperhand |     |     | 5        |
| ------------------------ | --- | --- | -------- |
| MPSconfidencethreshold   |     |     | 0.8      |
| Minimumdetectionsegment  |     |     | 30frames |
| Maxgapforinterpolation   |     |     | 10frames |
21frames
Savitzky–Golaywindow
2
Savitzky–Golaypolynomialorder
| EMAsmoothingfactorα |     | =α  | 0.15 |
| ------------------- | --- | --- | ---- |
|                     |     | x y |      |
PolicyNetwork(App.C.1)
6
Transformerlayers
| Transformerattentionheads |     |     | 8       |
| ------------------------- | --- | --- | ------- |
| Transformerembeddingdim   |     |     | 384     |
| Dropout                   |     |     | 0.05    |
| RGBpatchsize              |     |     | 16×16   |
| RGBinputresolution        |     |     | 240×320 |
| ICTtokendim               |     |     | 29      |
| PredictionhorizonK        |     |     | 50      |
Losses(App.C.1)
| Positionweightw |     |     | 5   |
| --------------- | --- | --- | --- |
p
| Rotationweightw |     |     | 1   |
| --------------- | --- | --- | --- |
r
| Graspweightw |     |     | 10  |
| ------------ | --- | --- | --- |
g
| Object-dynamicsweight(pos/rot) |     |     | 0.5w /0.5w |
| ------------------------------ | --- | --- | ---------- |
p r
| Visual-foresightweightw |     |     | 20  |
| ----------------------- | --- | --- | --- |
f
| Temporal-consistencyweightw |     |     | [0.1,1.0] |
| --------------------------- | --- | --- | --------- |
c
Optimization(App.C.1)
| Optimizer |     |     | AdamW |
| --------- | --- | --- | ----- |
1×10−4
Baselearningrate
200
Warmupsteps
0.05
Min-LRratio
| Batchsize |     |     | 32  |
| --------- | --- | --- | --- |
| Epochs    |     |     | 400 |
Continuedonnextpage
24

Table1–continuedfrompreviouspage
Parameter Value
Gradient-normclip 1.0
EMAdecay 0.999
DataAugmentation(App.C.1)
Photometricjitterprobability 0.8
Brightness/contrastdelta ±0.20/±0.20
Gammadelta ±0.15
Pixelnoiseσ 0.02
Grayscaleprobability 0.1
HSVhuejitter ±10
HSVsaturationrange [0.6,1.4]
Randomresizedcropprobability 0.5
Scalerange [0.7,1.0]
Aspect-ratiorange [0.9,1.1]
Gaussianblurprobability 0.15
Kernelsize 3×3
Randomerasingprobability 0.5
Numberofholes 3–8
Per-holearea 5–20%
Targetpositionnoiseσ 1mm
pos
Targetrotationnoiseσ 0.5◦
rot
Sub-stepinterpolationprobability 0.5
Hardware(App.D.1)
Robotarms 2×TrossenWidowXAI
WidowXAIDoF 6
WidowXAIpayloadatfullreach ∼1.5kg
WidowXAIend-effectorrepeatability ±1mm
InferenceRGBcamera IntelRealSenseD405(top-mounted)
Inference(App.D.2)
EulerODEsteps 20
Stepsize∆t 1/20
Executedaction-chunklength K =50
Control-loopfrequency 10Hz
Action-stepstride 2
Effectiveexecutedrate 5Hz
Look-aheadoffset 25steps
Graspprobabilitythreshold 0.6
PositionsmoothingEMAα 0.5
Rotationsmoothing quaternionSLERP
Trajectory-overlapsmoothingparameter 12
Safetycage:maxpositionstep 0.08m
Safetycage:maxrotationstep 0.02rad
RobotTeleoperationforACTBaseline
Teleopcontrolfrequency(leader→follower) 200Hz
Teleoprecordingfrequency 30Hz
Leader→followerEMAα 0.5
Topcameraresolution 640×480
Wristcameraresolution 320×240
Actionspace 7-DoFjointpositions
Proprioceptiondim 7
ACTBaselineTraining
Visualbackbone ResNet-18(pretrained)
Embeddingdim 256
Attentionheads 8
Encoder/decoderlayers 4/1
Feed-forwarddim 2048
CVAElatentdim 32
Dropout 0.1
PredictionhorizonK 50
Continuedonnextpage
25

Table1–continuedfrompreviouspage
Parameter Value
Imageinputresolution 240×320
Batchsize 24
Epochs 400
Baselearningrate 1×10−4
Weightdecay 1×10−2
Warmupsteps 500
EMAdecay 0.999
ActionL1weightw 5.0
pos
CVAEKLlossweight(annealedto) 10.0
26