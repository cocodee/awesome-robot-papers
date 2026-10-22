VIDEO PREDICTION POLICY 2: PREDICT BETTER,
ACT BETTER
YanjiangGuo1,2,*,HaodongYan1,3,*,ZhideZhong1,3,*,ZhongruZhang2,*,QingyuanYang1,2,*
QingzhouLu1,2,XiaoyuChen2,Yen-JenWang4,ShuyingDeng1,2,4,ChenghanYang2,PuzhenYuan1,2
ChenxinLiu1,2,TunBan1,5,XiangZhu1,2,YichenLiu1,2,KunFeng1,2,HaoangLi3,JianyuChen1,2
*EqualContribution 1Robotera 2TsinghuaUniversity 3HKUST(GZ)
4UniversityofCalifornia,Berkeley 5ShanghaiJiaotongUniversity
ProjectPage:https://robert-gyj.github.io/video-prediction-policy-2
ABSTRACT
World action models (WAMs) have emerged as an important class of general-
ist robot policies, aiming to transfer video prediction priors to action learning.
However,wefindthatexistingWAMsfrequentlyproduceincorrectmotionpre-
dictionsinopen-endedenvironments,leadingtoerroneousactions. Weattribute
this limitation to two factors: (1) base video models are not optimized for ma-
nipulation, and (2) naively incorporating action components into video models
can substantially degrade their generalization capabilities. We introduce Video
PredictionPolicy2(VPP2),aWAMthatenablesstrongzero-shotgeneralizationin
bothvideopredictionandactiongeneration. First,wecuratealarge-scale,diverse
datasetofmanipulationvideostocontinuepretrainingthebasevideofoundation
model. Weannotatevideoclipswithdetailedcaptionsandperformevent-level
videopretrainingtopromotegeneralizationacrossopen-endedmanipulationtasks.
Second,wepost-trainanddistillthevideomodelintoasingle-stepvisualplanner
with a fixed prediction horizon. Finally, we introduce an action module via a
mixture-of-transformers(MoT)architecturetolearnanimplicitinversedynamics
model. Experimentsdemonstratethreekeyresults: (1)VPP2-14Boutperforms
Cosmos3-64Bby11.0%pointsinvideopredictioninstruction-followingsuccess
rate on open-ended tasks; (2) VPP2 surpasses the strongest baseline by 18.5%
pointsinsuccessrateonreal-worldzero-shotALOHAmanipulationtasks; and
(3)followingbenchmark-specificpost-training,VPP2achievesthehighestsuccess
ratesamongevaluatedmethodsonthechallengingLIBERO-Pro,LIBERO-OOD,
andRoboDojobenchmarks.
(1) Video PredictionInstruction (2) Zero-shotReal- (3) Post-training on
Following World Manipulation Benchmarks
1.0 1.0 40
0.85 29.47
0.8 0.74 0.8 30
Large diverse manipulation Data 0 0 0 0 . . . .2 0 4 6 0. n B a 4 W 1- 18 0 P VL .54 som soC 0.3 B 61- 8 3som s B o 4 C 6- 2PP V 0 0 0 0 . . . .2 0 4 6 0 𝝅 . 𝟎 𝟓. 40 0 tsaF .2 M AW 1 0. 2PP V 58 1 2 0 0 0 6. 𝝅 9 𝟎𝟓. 3 14 5.0G .88 1 nepO 1.9 M A W 2 2PP V
o1 ··· oH a1 ··· ah Simple Caption → Short Future Chunks Detailed Caption → Complete trajectory
Video DiT Action DiT P th l e a c b e o t x h . e bowl inside T t b h o h e x e l . e l T e f f t h t a e r n o c d b a m o p t l e a g r c a r e i p v i p t i e e i w n r s p i k i d e c e e k p s th s u e s p t t r a w a ti n h c s i . t p e a b re o n w t l in Goal
o0 o1 ··· oH a1 ··· ah
Start
Event-level Continue Pretraining +
Chunk-level Post-training Unstable mapping Multiple modes Unique, stable mapping Concentrated distribution
Figure1: Atypicalrobotpolicymapsasimpleinstructionandanobservationintoashortaction
chunk. As datasets scale, this mapping becomes increasingly multimodal and uncertain, leading
modelstolearnspuriousshort-horizoncorrelations. VPP2firstestablishesconsistentsemantic-to-
trajectorymappingsvianexteventvideopredictionwithdetailedcaptions,thenpost-trainsanddistills
themodeltogenerateshortactionchunks.
1
6202
tcO
8
]VC.sc[
2v07201.0162:viXra

1 INTRODUCTION
Worldactionmodels(WAMs)aredevelopingrapidlyandhavebecomeanimportantclassofgeneralist
robotpolicies(Huetal.,2024;Liaoetal.,2025;Kimetal.,2026;Yuanetal.,2026;Maetal.,2026;
Lietal.,2026a;b;AgiBotResearchTeametal.,2026;Yeetal.,2026). ManyWAMsbuildonvideo
foundationmodels(Wanetal.,2025;Agarwaletal.,2025;Yangetal.,2025),aimingtotransfer
theirrichpriorsaboutphysicaldynamicstopolicylearning. Thispremiseiscompelling: accurate,
instruction-conditionedvideopredictionscanguideactiongenerationthroughanexplicitorimplicit
inversedynamicsmodel(Duetal.,2023;Huetal.,2024). However,priorwork(Zhangetal.,2026b)
hasfoundthatexistingWAMsoftenperformwellonlyonanarrowsetofseentasks,whileproducing
unreliablefuturemotionpredictionsinunseen,out-of-distributionscenarios.Thesepredictionfailures,
inturn,leadtoerroneousactions. Inrecentbenchmarksthatrequiregeneralization,robotpolicies,
including WAMs, with near-perfect success rates on standard evaluation suites suffer substantial
performancedropsunderperturbedtaskconfigurationsandnovelskillcompositions(Zhouetal.,
2025;Li,2025;Mishraetal.,2026).
We identify two key factors that limit the generalization of existing WAMs to unseen scenarios.
First,basevideomodelsareprimarilyoptimizedforcreativecontentgenerationandaestheticquality
ratherthanprecisephysicaldynamics,andthereforeoftenfailtofollowmanipulationinstructions
faithfully (Chen et al., 2025; Zhang et al., 2026b). Second, introducing action-specific compo-
nentsortrainingobjectivesintopretrainedvideofoundationmodelscansubstantiallydegradetheir
generalizationcapabilities(Mishraetal.,2026).
To address these issues, we introduce Video Prediction Policy 2 (VPP2), a WAM that achieves
strongzero-shotgeneralizationinbothvideopredictionandactiongeneration. Ourfirstobjective
istotrainageneralizablevideofoundationthatcanfaithfullyfollowinstructionsandmakefuture
predictionsgroundedinthecurrentobservation,withoutunsupportedchangestothesceneortask.
Tothisend,weannotateeachclipwithadetailedcaptionspecifyingthemanipulationprocess,active
end effector, and target object, and perform event-level video prediction training. As illustrated
inFigure1, detailedcaptionsandcompleteevent-leveltrajectorypredictionsubstantiallyreduce
uncertaintyinfuturepredictionandencourageconsistentmappingsfromsemanticdescriptionsto
visualtrajectories,improvinggeneralizationacrossdiverseinstructions. Wethenpost-trainthevideo
modeltopredictfixed-horizonfuturechunksandapplyconsistencydistillation(Songetal.,2023)
toobtainasingle-stepvisualplannerforreal-timerobotexecution. Finally,weintroduceanaction
expertthroughamixture-of-transformers(MoT)architecture(Liangetal.,2025)tolearnanimplicit
inversedynamicsmodelconditionedonthepredictedfuture. Duringpolicyexecution,wepairVPP2
withaVLMplanner(Baietal.,2025;BytedanceSeed,2026)thattranslatesopen-endedinstructions
intoexplicitsubtaskinstructions.
OurexperimentsdemonstratethreekeyadvantagesofVPP2. (1)VPP2-14Bfollowsmanipulation
instructionsfaithfully,outperformingCosmos3-64B(Agarwaletal.,2026)by11%ininstruction-
following success rate on open-ended tasks. (2) VPP2 exhibits strong zero-shot manipulation
capabilitiesonareal-worldALOHAplatform(Zhaoetal.,2023),achievinganaveragesuccessrate
of58.5%across10taskcategories,comparedwith40.0%forπ (Intelligenceetal.,2025)and
0.5
20.5%forFast-WAM(Yuanetal.,2026). (3)Followingbenchmark-specificpost-training,VPP2
achievesthehighestsuccessratesamongevaluatedmethodsonLIBERO-Pro(Zhouetal.,2025)
(45.0%,comparedwith11.0%forthestrongestbaseline),LIBERO-OOD(Li,2025;Mishraetal.,
2026)(63.9%),andRoboDojo(Chenetal.,2026)(32.26%,state-of-the-art).
2 DATA PROCESSING PIPELINE
Inthissection,wedescribeourdatacollectionandcurationpipeline,includinghowweunifythe
inputsandoutputsacrossdiversemanipulationdatasets.
VideoSources. Wecompilealarge-scale,diversecollectionofmanipulationvideosforcontinued
pretrainingofanopen-sourcevideofoundationmodel(Wanetal.,2025). Ourdataspanthreecate-
gories: robotmanipulationdatasets,humanactivitydatasets,andgeneral-purposevideodatasets. For
general-purposevideodatasets,weapplyanextensivefilteringpipelinesimilartothatofLVP(Chen
etal.,2025)toretainonlyvideosdepictingmanipulation-relatedactivities. Table1summarizesthe
datasetsusedfortraining;fulldatasetreferencesareprovidedinAppendixA.
2

| DataType | EmbodimentType |     | DataSources                       |     |     |     |     |
| -------- | -------------- | --- | --------------------------------- | --- | --- | --- | --- |
|          | Single-arm     |     | OXE,RoboMIND,DROID,RH20T,MolmoAct |     |     |     |     |
Robot Dual-arm AgiBot World-Beta, RoboCOIN, RDT, GM-100, ABC-130K, Self-
collectedALOHAData
|       | Mobile&humanoid |     | InternData-A1,GalaxeaOpen-World,Self-collecteddexteroushands |         |                       |     |            |
| ----- | --------------- | --- | ------------------------------------------------------------ | ------- | --------------------- | --- | ---------- |
|       |                 |     | Open-source:                                                 | EgoDex, | Ego4D, EPIC-KITCHENS, |     | Something- |
| Human | Humanhands      |     |                                                              |         |                       |     |            |
SomethingV2,VITRA-1M
Self-collectedegocentricdata
| GeneralVideo | Humanhands |     | OpenVid,Panda-70M |     |     |     |     |
| ------------ | ---------- | --- | ----------------- | --- | --- | --- | --- |
Table 1: Overview of training data sources. Full dataset references are provided in Appendix A,
Table5.
|     | End-effector is not  | End effector fully    | Specify the left cup.    |     | Specify the left most yellow box.  |     |     |
| --- | -------------------- | --------------------- | ------------------------ | --- | ---------------------------------- | --- | --- |
|     | visible. →Delete     | visible. →First frame | (Two cups on the table.) |     | (Three boxes on the table.)        |     |     |
Caption Tempelate:
Final caption: The left robot gripper picks up the
stainless steel cup in the left side and place it inside the
Left gripper ……
|     |     |     | Right Gripper ……   | left most yellow box,  the right gripper is not visible in  |     |     |     |
| --- | --- | --- | ------------------ | ----------------------------------------------------------- | --- | --- | --- |
|     |     |     | Specified object … | the video. This is a composed robot video with two wrist    |     |     |     |
Camera view ……
views in the right side.
Multi-view concatenation
Figure2: Anexampleofourdataprocessingpipeline. Thecentralobjectiveistoreduceuncertainty
infutureprediction,therebyencouragingthemodeltolearnaconsistentmappingfromconditioning
informationtosub-tasktrajectories. Tothisend,eachcaptionincludesdetailedtaskdescriptions,
explicitend-effectoridentification,adescriptionofthevisibletargetobject,andcamera-viewchanges.
VideoFiltering,SegmentationandCaptioning. Wefirstremovecorruptedtrajectories,including
those with camera failures or abrupt discontinuities, and segment the remaining trajectories into
semanticallycoherentclipslasting1–12seconds. Weidentifycandidateboundariesusingheuristic
cuesassociatedwithnaturaltransitions,suchaslocalminimainhuman-handorend-effectorvelocity
andmomentswhenthegripperorfingersopenorclose. Avision-languagemodel(VLM)thenrefines
thesegmentationbymergingadjacentclipswhereappropriateandadjustingtheirstartandendpoints.
Aftersegmentation,wegeneratedetailedcaptionsthatdescribethetask,explicitlyidentifytheactive
end effectors, unambiguously specify the target objects, and characterize the camera views and
motion. Figure2illustratesanexample,andAppendixA.1providesfurtherdetails.
| UnifiedActionSpaceandUnifiedEnd-effector |     |     |     |     |     | 𝑩   |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
𝒅
| Coordinate | Systems. | Different | robot datasets |     |     |     |     |
| ---------- | -------- | --------- | -------------- | --- | --- | --- | --- |
oftenadoptinconsistentcoordinatesystemsand
cameraviewpoints,resultinginconflictingaction
| representationsforvisuallysimilarmotions. |     |     | For |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
example,aleftwardmotionmaycorrespondtothe
| positive | x-direction | in one dataset | but the nega- |     |     | 𝑩   |     |
| -------- | ----------- | -------------- | ------------- | --- | --- | --- | --- |
𝒅
tivey-directioninanother,makingitdifficultfor
| themodeltolearnthesemanticmeaningofeach |     |     |     |     | 𝑨 𝒅 |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
actiondimension.
(a) Workspace alignment             (b) End-effector alignment
Wefocusonegocentricbimanualdatasets,includ-
| ing ALOHA-style, |           | humanoid-style, | and human |            |                                |           |             |
| ---------------- | --------- | --------------- | --------- | ---------- | ------------------------------ | --------- | ----------- |
|                  |           |                 |           | Figure3:   | (a)Boundingboxesshowthealigned |           |             |
| egocentric       | datasets. | These datasets  | account   | for        |                                |           |             |
|                  |           |                 |           | workspaces | of different                   | datasets. | (b) Aligned |
morethan80%ofthetotaldataandshareasim-
end-effectorcoordinateframes.
| ilarbimanualstructureandcameraviewpoint. |     |     |     | We  |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
explicitlyaligntheircoordinatesystemsattwolevels: (1)workspacealignment,whichappliesa
world-frametransformationsothatdifferentrobotshavecomparableend-effectorworkspaces;and
(2)end-effectoralignment,whichappliesalocaltransformationtostandardizeend-effectororigins
andaxisorientations.
3

Foranarmdatasetd,letT =WdT ∈SE(3)denotetheoriginalend-effectorpose,whereW and
|     |     |     | d Ed |     |     |     |     |     | d   |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
E arethedataset’sworldandend-effectorframes,respectively. Wedefinetheworkspacealignment
d
asA =W¯T andtheend-effectoralignmentasB =EdT E¯,whereW¯ andE¯denotethecanonical
| d   | Wd  |     |     |     | d   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
worldandend-effectorframes. Thealignedend-effectorposeisgivenbyT(cid:101)d =A T B ,.
d d d
UnifiedT-shapeMulti-viewInputacrossDatasets. Roboticsdatasetscommonlycontainobser-
vationsfrommultiplecameraviews. WearrangethemintoaT-shapedcompositeimage,withthe
primaryviewontheleftandtwoauxiliaryviewsstackedverticallyontheright,asillustratedinthe
bottom-leftpanelofFigure2. Whenfewerthantwoauxiliaryviewsareavailable,wefillthemissing
slotswithblackplaceholderimages.
| 3 VPP2: | A GENERALIST |     | POLICY |     | WITH | ZERO-SHOT |     | CAPABILITY |     |
| ------- | ------------ | --- | ------ | --- | ---- | --------- | --- | ---------- | --- |
Overview. Ourlarge-scale,diverse,anddenselyannotateddatasetenablesustotrainapolicywith
stronggeneralizationcapabilities. VPP2buildsuponthepretrainedWan2.1-I2V-14Bmodel(Wan
etal.,2025)andintroducesanactionexpertviaamixture-of-transformers(MoT)architecture(Liang
etal.,2025).Ourtrainingobjectiveistwofold:wefirstadaptthevideomodeltoproducegeneralizable
futurepredictionsatreal-timeinferencespeedforopen-endedmanipulationtasks,andthentrainthe
actionexpertconditionedontheKVcacheofthevideomodel. Tomaximizepolicygeneralization,
weorganizetrainingintothestagessummarizedinFigure4.
3.1 VIDEOPREDICTIONMODELTRAININGPIPELINE
Stage 1: Event-level Video Model Continued Pre-training. We first adapt a pretrained video
generation model to the manipulation domain through event-level continued pre-training. Each
trainingexamplecoversacompletemanipulationsubtask,aligningthesubtaskdescriptionwiththe
correspondingvisualevolutionfromtheinitialobservationtosubtaskcompletion.
Givenademonstrationτ =(o 0 ,o 1 ,...,o T ),weuniformlysampleN futureframesacrosstheentire
event:
|     |     |     |       | (cid:0) |       |        |        | (cid:1) |     |
| --- | --- | --- | ----- | ------- | ----- | ------ | ------ | ------- | --- |
|     |     |     | y     | = o     | ,o ,o |        | ,...,o | ,       | (1) |
|     |     |     | event | 0       | ⌊T/N⌋ | ⌊2T/N⌋ |        | T       |     |
whereT isthefinalframeindexandN excludestheinitialconditioningframeo .Letx =E(y )
|     |     |     |     |     |     |     |     | 0 1 | event |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
denotethecorrespondingvideolatentrepresentation,whereE isthevideoencoder. Weconstructthe
interpolatedlatentas
|     |     | x   | =(1−s)ϵ+sx |     | , ϵ∼N(0,I), |     |     | s∈[0,1], | (2) |
| --- | --- | --- | ---------- | --- | ----------- | --- | --- | -------- | --- |
|     |     | s   |            |     | 1           |     |     |          |     |
where s denotes flow time, with s = 0 corresponding to noise and s = 1 to data. The model is
optimizedwiththeflowmatchingobjective(Lipmanetal.,2023)
|     |     |     |       |            | (cid:104) |          |     | (cid:105) |     |
| --- | --- | --- | ----- | ---------- | --------- | -------- | --- | --------- | --- |
|     |     | L   | (θ)=E |            | ∥v (x     | ,s,c)−(x |     | −ϵ)∥2 ,   | (3) |
|     |     | FM  |       | (x1,c),ϵ,s | θ         | s        |     | 1 2       |     |
wherev θ predictstheflowvelocityandcincludesthesubtaskinstructionandinitialobservationo 0 .
Inthisstage,wepredict49framesataresolutionof416×240andcontinuepre-trainingWan2.1-
I2V-14Bfor30,000optimizationstepswithbatchsize1,024andlearningrate1e-5. Ourexperiments
inSec.4.1showthattheresultingmodelachievesstronginstructionfollowingonmanipulationtasks,
outperformingthe64BCosmos3-Super-Image2Videomodel(Agarwaletal.,2026).
Stage 2: Chunk-level Video Model Post-training. Event-level continued pre-training enables
themodeltogeneralizewelltomanipulationtasks. However,samplingafixednumberofframes
fromeventsofdifferentdurationsproducesvariabletemporalintervalsbetweenpredictedframes,
complicatingtheiralignmentwithdownstreamactions. Wethereforefurtherpost-trainthemodel
topredictafixed-durationfuturechunk,establishingaconsistenttemporalscaleforactionlearn-
ing. Inexperiments,wepredict2secondsforhuman-handmanipulationand8secondsforrobot
manipulation.
LetH denotethepredictionhorizoninsecondsandf thedatasetframerateinframespersecond
(fps). Thenominalintervalbetweensampledframesisδ =fH/N,measuredindatasetframes. For
achunkstartingatframet,thetargetvideois
|     |     |     | y(t) = | (cid:0) o ,o | ,o           | ,...,o |        | (cid:1) , | (4) |
| --- | --- | --- | ------ | ------------ | ------------ | ------ | ------ | --------- | --- |
|     |     |     | chunk  | t            | t+⌊δ⌋ t+⌊2δ⌋ |        | t+⌊Nδ⌋ |           |     |
4

|                     |     |     | Noise                    |     | Denoised latent observations/actions |     |             |     |              |     |     |
| ------------------- | --- | --- | ------------------------ | --- | ------------------------------------ | --- | ----------- | --- | ------------ | --- | --- |
| Complete trajectory |     |     | Fixed-length video chunk |     |                                      |     | Video chunk |     | Action chunk |     |     |
Event level
| 0   |     | T   | 0   |     | H   | 0   | H   |     | 0 h | Attention mask |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- |
o0ohoh′oHa0ah
|     | o   | ··· o |     | o   | ··· o |     | o ··· | o   | a ··· | a    |     |
| --- | --- | ----- | --- | --- | ----- | --- | ----- | --- | ----- | ---- | --- |
|     | 1   | T     |     | 1   | H     |     | 1     | H   | 1     | h o0 |     |
oh
|     | Video DiT |     |     | Video DiT |     |     | Video DiT |     | Action DiT | oh′ |     |
| --- | --------- | --- | --- | --------- | --- | --- | --------- | --- | ---------- | --- | --- |
oH
a0
| o   | o   | ··· o |     | o o | ··· o | o   | o ··· | o   | a ··· | a    |     |
| --- | --- | ----- | --- | --- | ----- | --- | ----- | --- | ----- | ---- | --- |
|     | 0 1 | T     |     | 0 1 | H     |     | 0 1   | H   | 1     | h ah |     |
Short Action Chunk Generation
| Video Event Prediction   |     |     | Long Video Chunk Prediction      |     |     |     |     |                          |     |     |     |
| ------------------------ | --- | --- | -------------------------------- | --- | --- | --- | --- | ------------------------ | --- | --- | --- |
| (1) Continue Pretraining |     |     | (2) Post-training & Distillation |     |     |     |     | (3) ActionDiTPretraining |     |     |     |
Figure4: TheVPP2trainingpipelineisdesignedtomaximizegeneralization. Stage1useslarge-
scale,event-levelvideopretrainingtolearnageneralizablevideomodelformanipulation. Stage2
post-trainsanddistillsthismodeltopredictlong-horizonvideochunksspanning8secondsinasingle
forwardpass,takingapproximately0.1seconds. Finally,Stage3trainsanactionexperttogenerate
2-secondactionchunksconditionedontheone-stepvideolatents.
withconditioninginputsccontainingtheobservationo andthecorrespondingsubtaskinstruction.
t
Theindext+⌊fH⌋iscappedatthefinalframeindexT,andweoptimizethesameflowmatching
| objectiveinEq.equation3,withx |     |     |     |     | =E(y(t) | ).  |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
|                               |     |     |     |     | 1 chunk |     |     |     |     |     |     |
Stage2: ConsistencyDistillation. Wedistillthechunk-levelvideomodelforsingle-stepgenera-
tion(Songetal.,2023)byenforcingconsistentterminalpredictionsatadjacentflowtimes:
|     |     |     |     | (cid:104) |                     |     |     |      |            | (cid:105) |     |
| --- | --- | --- | --- | --------- | ------------------- | --- | --- | ---- | ---------- | --------- | --- |
|     |     | L   | =E  | λ(s,s′)∥F | (x ,s,c)−stopgrad(F |     |     | θ¯(x | ,s′,c))∥   | 2 ,       | (5) |
|     |     | CD  |     |           | θ s                 |     |     |      | (cid:98)s′ | 2         |     |
where0≤s<s′ ≤1,x isobtainedbyintegratingthefrozenteacherflowfrom(x ,s)tos′,andθ¯
|     |     |     | (cid:98)s′ |     |     |     |     |     |     | s   |     |
| --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
denotestheEMAstudentparameters. ThestudentsatisfiesF (x,1,c)=x. Toemphasizesingle-step
θ
generation,wesamples′ =1withprobability0.5;otherwise,wesamples′fromtheremainingflow
times. Atinference,thevideolatentisgeneratedinasingleforwardpassasF θ (ϵ,0,c).
3.2 ACTIONMODELING
Stage 3: Action Pretraining across Datasets. After training a generalizable video model, we
traintheactionexpertonourprocessedbimanualdatasetswithunifiedworkspaceandend-effector
coordinate systems. The action expert is a 0.9B-parameter diffusion transformer (DiT) (Peebles
& Xie, 2023) with a standard MoT architecture. Since the action expert is newly initialized, we
freezethebaseparametersofthevideoDiTduringtheearlystagesofactiontrainingandadaptthe
videobackboneusingonlyLoRA(Huetal.,2022). Thisstrategyhelpspreservethepretrainedvideo
representationswhilelimitingdisruptionfromaction-traininggradients.
InferenceLatency. Wegeneratevideoefficientlybyreducingthevideoinputto17×416×240
duringpost-traininganddistillingthevideomodelforone-stepgeneration,asdescribedinSec.3.1.
Withbfloat16precisionandtorch.compile,thevideomodeltakesapproximately0.12seconds. The
actionexpertthengeneratesanactionchunkconditionedonthevideolatentsusingfivedenoising
steps,takingapproximately0.1seconds.Thetotallatencyperactionchunkisthereforeapproximately
0.22seconds.
3.3 VLMFORHIGH-LEVELPLANNING.
Sub-taskPlanning. Totacklelong-horizontasksandhandleambiguoushumaninstructions,we
adoptahierarchicalarchitectureinwhichaVLMgeneratessubtaskplans(Shietal.,2025). The
VLMhandleshigh-levelreasoning,semanticunderstanding,andmemory,allowingVPP2tofocus
onmappingexplicitinstructionstotrajectories. Inpractice,theVLMcanbedeployedlocallyor
accessedthroughanAPItoafrontiermodel.
5

Grab the black gas nozzle. Place the spoon on the iPad.
Opentheoven. Lift the lid off the white jar.
Close the laptop. Graspthetissue and use it to wipe the screen.
Transferthe left slipper to the right side. Use scissors to cut the paper.
Clean the white board. Pack the device into box.
Put the cap back on bottle. Place the green block on the controller.
Flip the package. Sweep the block into dustpan.
Use the towel to wipe the plate. Open the upper-layer drawer.
Figure5: VPP2videopredictionsforhuman-handandrobotmanipulation. Trainedonlarge-scale,
diverse manipulation datasets, VPP2 generalizes across human hands and a wide range of robot
embodiments. Forrobotmanipulation,VPP2jointlypredictsonetothreecameraviewsarrangedin
aT-shapedcomposite. Duetospaceconstraints,single-stepvideopredictionsafterdistillationare
showninFigure10intheappendix.
Prompt Enhancement. VLM planning also generates detailed subtask descriptions that match
thecaptiontemplateusedduringtraining. Priorworkonvideogenerationlikewisehighlightsthe
importanceofdetailedcaptionsforgenerationquality(Wanetal.,2025;Yangetal.,2025).
4 EXPERIMENTS
Inthissection,weconductexperimentstoanswerthefollowingquestions: (1)Howdoesthemotion
qualityofVPP2’svideopredictionscomparewiththatofstate-of-the-artvideofoundationmodelson
manipulationtasks? (2)HowbroadareVPP2’szero-shotmanipulationcapabilities? (3)Howwell
doesVPP2performafterdomain-specificpost-training?
4.1 VIDEOPREDICTIONQUALITYANALYSIS
VideoPredictionforHumanandRobotManipulation. Figure5visualizespredictionsforhuman-
hand manipulation and diverse robot embodiments from the pretrained VPP2 model. To assess
generalization, we randomly sample test cases from prior work (Chen et al., 2025; Zhang et al.,
2026b)andtakephotographsinofficeenvironmentsandrobotworkspaces,pairingthemwithfreely
chosenmanipulationinstructions. Trainedondataspanningmorethan20robotembodiments,VPP2
alsogeneralizestounseenembodimentsandtasks,asshowninFigure5. VPP2alsosupportsjoint
predictionacrossonetothreecameraviews,withtheprimaryviewplacedontheleftanduptotwo
auxiliaryviewsstackedontheright.
QuantitativeComparisons. WecompareVPP2withfourvideofoundationmodelsandoneablation
variant: (1)Wan-2.1-I2V-14B-480p(Wanetal.,2025),ourbasemodel;(2)LVP(Chenetal.,2025),
whichalsoadaptsWan-2.1-I2V-14B-480ptomanipulationtasks;(3)Cosmos3-Nano-16B,whichis
extensivelytrainedonrobotmanipulationdata;(4)Cosmos3-Super-Image2Video-64B,thestrongest
6

| Method | Human Robot | Wan-2.1-14B |     | Baseline wins Ties | VPP2 wins |     |     |
| ------ | ----------- | ----------- | --- | ------------------ | --------- | --- | --- |
|        |             | 4%          | 44% | 52% 0%4%           |           | 96% |     |
LVP
| Wan2.1-14B      | 0.32 0.04 |               |             |                  |         |         |          |
| --------------- | --------- | ------------- | ----------- | ---------------- | ------- | ------- | -------- |
|                 |           | 1 2%          | 58%         | 30%              | 6% 44%  |         | 50%      |
| LVP             | 0.62 0.46 | C o smos3-16B |             |                  |         |         |          |
| Cosmos3-16B     | 0.44 0.32 | 10%           | 44%         | 46%              | 10% 22% | 68%     |          |
| Cosmos3-64B     | 0.70 0.78 | Cosmos3-64B   |             |                  |         |         |          |
|                 |           | 18%           | 54%         | 28%              | 12%     | 64%     | 24%      |
| VPP2-Fixed-Step | 0.48 0.42 |               |             |                  |         |         |          |
|                 |           | 0%            | 20% 4 0 %   | 6 0% 80% 100% 0% | 20%     | 40% 60% | 80% 100% |
| VPP2(ours)      | 0.80 0.90 |               | H u m an Ha | n d              |         | Robot   |          |
Figure6: WinratesofthepretrainedVPP2modelagainstdifferent
| Table 2: Instruction | following |     |     |     |     |     |     |
| -------------------- | --------- | --- | --- | --- | --- | --- | --- |
baselinesonvideopredictiontasks.
successrates.
B41-naW
B46-3somsoC
2PPV
(a) Grasp leftmost bottle and place it in front of the short cup. (b) Stack red paper cup on leftmostblack paper cup.
Figure7: Comparisonofinstruction-followingcapabilitiesamongVPP2,Wan-14B,andCosmos3-
64B.VPP2demonstratesbetterinstructionfollowingoncomplextasksrequiringspatialunderstand-
ing.
model in the Cosmos 3 family (Agarwal et al., 2026); and (5) VPP2-Fixed-Step, an ablation of
our method that predicts a fixed-duration future chunk rather than a complete event, potentially
misaligningthepredictedfuturewiththeinstructiondescribingthefullevent.
Werandomlycollect50image–instructionpairseachforhuman-handandrobotmanipulationand
generatevideopredictionsforeverypairusingeachmodel. WefirstuseaGPT-basedevaluatorto
assessinstruction-followingsuccessrates,reportedinTable2. Humanevaluatorsthencomparepairs
ofpredictionstodeterminewhichbetterfollowstheinstruction,yieldingVPP2’spairwisewinrates
againsteachbaselineinFigure6. VPP2’sadvantagesaremostpronouncedincomplexmanipulation
scenariosrequiringspatialunderstanding,asillustratedinFigure7. Wehypothesizethattrainingwith
detailedcaptionsencouragesmoreaccuratemappingsfrominstructionstotrajectories,contributing
totheseimprovements.
4.2 POLICYPERFORMANCEANALYSIS
Zero-shotPerformanceonReal-worldAlohaRobot. Afterpretrainingastrongvideofoundation
modelformanipulation,wepost-trainanddistillitintoafast,single-stepgeneratortosupportaction
learning. Withitsgeneralizablevideopredictions,VPP2demonstratesstrongzero-shotcapabilities
acrossopen-endedmanipulationtasks. WedeployVPP2directlyonarobotembodimentseenduring
training,withouttask-specificfine-tuning. Forcomparison,wetrainπ (Intelligenceetal.,2025)
0.5
andtheWan-14BversionofFast-WAM(Yuanetal.,2026)onthesamedatausedinVPP2training.
Weevaluatemodelson10differentcategoriesofzero-shottasksandpresentresultsinFigure8.VPP2
achievesanaveragesuccessrateof58.5%,comparedwith40.0%forπ and20.5%forFast-WAM,
0.5
andperformsbestin9ofthe10categories.
LIBERO-ID,LIBERO-Pro,andLIBERO-OODBenchmarks. Allmodelsaretrainedexclusively
onthefourstandardLIBEROsuites(Liuetal.,2023)andareevaluatedunderthreecomplementary
settings. LIBERO-ID measures standard in-distribution manipulation performance. To assess
generalizationbeyondthetrainingdistribution, wefurtherevaluateonLIBERO-Pro(Zhouetal.,
2025)andLIBERO-OOD(Li,2025)withoutadditionaltraining.FollowingHarnessVLA(Zhangetal.,
2026d),weevaluatethePositionandTaskperturbationsofLIBERO-Pro,whichtestgeneralizationto
changesinobjectpositionsandtaskspecifications,respectively. Wefurtherfollow(Mishraetal.,
2026)toevaluatecompositionalgeneralizationonLIBERO-OOD,whichrecombinesfamiliarobjects,
7

|      | Success rate |     | π   | FastWAM-14B |     |     | VPP2 |     |     |     |
| ---- | ------------ | --- | --- | ----------- | --- | --- | ---- | --- | --- | --- |
| 100% |              |     | 0.5 |             |     |     |      |     |     |     |
80%
|     | 65%     | 70% 75% | 70% |     |     |     |        |     | 65% |       |
| --- | ------- | ------- | --- | --- | --- | --- | ------ | --- | --- | ----- |
|     |         | 55%     |     |     |     | 55% |        | 60% |     | 58.5% |
| 50% | 45%     |         |     |     | 50% | 50% |        |     | 45% |       |
|     | 40%     | 40%     | 35% | 40% | 35% |     | 35%    | 30% | 30% | 40%   |
|     | 25% 20% |         |     |     | 20% |     | 20%20% |     |     | 20.5% |
15%
|     |     |     |     | 0% 0% |     |     |     | 0%  |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
0%
Stack Pick Place Fold Pour Pull Insert Open Close Wipe Average
Figure 8: Zero-shot success rates on the real-world ALOHA across 10 randomly selected task
categories. Forafaircomparison,wefinetuneπ andFastWAMonallALOHAdatasetsexposedin
0.5
VPP2’strainingdataandusethe14BvariantofFastWAM.
|     |     |     | LIBERO-ID |     | LIBERO-Pro |     |     | LIBERO-OOD |     |     |
| --- | --- | --- | --------- | --- | ---------- | --- | --- | ---------- | --- | --- |
Method Overall Position Task Overall Spatial Object Goal Overall
|     | π0(Blacketal.,2024) |     | 94.2 | 0.5 | 0.0 | 0.3 | 0.7 | 0.3 4.3 | 1.7 |     |
| --- | ------------------- | --- | ---- | --- | --- | --- | --- | ------- | --- | --- |
π0.5(Intelligenceetal.,2025) 96.9 20.8 1.3 11.0 36.7 2.3 41.7 26.8
|     | MolmoAct(Leeetal.,2025)      |     | 86.6 | 1.5 | 1.5 | 1.5 | –    | –        | – –  |     |
| --- | ---------------------------- | --- | ---- | --- | --- | --- | ---- | -------- | ---- | --- |
|     | X-VLA(Zhengetal.,2026)       |     | 98.1 | 0.8 | 6.8 | 3.8 | –    | –        | – –  |     |
|     | AtomVLA(Sunetal.,2026)       |     | 97.0 | 7.3 | 5.3 | 6.3 | –    | –        | – –  |     |
|     | Cosmos-Policy(Kimetal.,2026) |     | 98.5 |     | – – | –   | 30.7 | 0.3 0.7  | 10.5 |     |
|     | Fast-WAM(Yuanetal.,2026)     |     | 97.6 |     | – – | –   | 12.7 | 0.0 15.7 | 9.4  |     |
|     | DiT4DiT(Maetal.,2026)        |     | 98.6 |     | – – | –   | 9.0  | 0.0 10.3 | 6.4  |     |
TemporalRatio(Mishraetal.,2026) 94.0 – – – 58.6 40.0 80.3 59.4
|     | VPP2(Ours) |     | 98.8 | 42.3 | 47.8 | 45.0 | 59.3 | 44.5 87.7 | 63.9 |     |
| --- | ---------- | --- | ---- | ---- | ---- | ---- | ---- | --------- | ---- | --- |
Table3: Post-trainingonLIBERO-ID,LIBERO-Pro,andLIBERO-OODbenchmarks. Allmodels
aretrainedexclusivelyonthefourstandardLIBEROsuites(Liuetal.,2023)andareevaluatedunder
threecomplementarysettings.
layouts,andgoalsintounseentaskconfigurationsalongspatial,object,andgoaldimensions.Per-suite
LIBERO-IDresultsareprovidedinAppendixC.1.
AsshowninTable3,whilemostbaselinesexceed94%onLIBERO-ID,thisin-distributionperfor-
mancedoesnottransfertogeneralization. OnLIBERO-Pro,VLAbaselinesdroptoatmost11.0%
overall,whereasVPP2reaches45.0%,withthelargestgainontheTaskperturbation(47.8%vs.6.8%),
indicatingthatVPP2followsthegiveninstructionratherthanreplayingmemorizedtrajectories. On
LIBERO-OOD,video-basedpoliciessuchasCosmos-Policy,Fast-WAM,andDiT4DiTreachatmost
10.5%,whileVPP2achieves63.9%,alsosurpassingTemporalRatio(Mishraetal.,2026),which
specificallytargetsthisgeneralizationgap. Weattributethesegainstonext-eventvideoprediction
withdetailedcaptions,whichestablishesconsistentmappingsfrominstructionstofuturetrajectories.
RoboDojo Benchmark. RoboDojo (Chen et al., 2026) is a unified sim-and-real benchmark for
evaluatinggeneralistrobotmanipulationpolicies. Itssimulationbenchmarkcontains42bimanual
taskscoveringfivecapabilitydimensions: generalization,memory,precision,long-horizonexecution,
andopen-vocabularyinstructionfollowing. Wefollowtheofficialtrainingandevaluationprotocol
andreportboththesuccessrateandtheaveragescore,whichcapturespartialtaskprogress.
AsshowninTable4,VPP2achievesanaveragescoreof39.26andasuccessrateof32.26%,achieving
| state-of-the-artperformance.1 |     |     | ItoutperformsrepresentativeVLAssuchasπ |     |     |     |     |                         |     |     |
| ----------------------------- | --- | --- | -------------------------------------- | --- | --- | --- | --- | ----------------------- | --- | --- |
|                               |     |     |                                        |     |     |     |     | 0.5 (Intelligenceetal., |     |     |
2025),X-VLA(Zhengetal.,2026),andXiaomi-Robotics-1(Guoetal.,2026),worldactionmodels
such as Fast-WAM (Yuan et al., 2026) and OpenWAM-α (Wang et al., 2026a), and the frontier
foundationmodelGPT-6-Astra(Zhangetal.,2026c)(28.97/22.48%). Per-dimensionresultsare
providedinAppendixC.2.
VPP2withSubtaskPlanning. TheVPP2resultsinTable4usefull-taskinstructionswithoutsubtask
planning. WefurtherinvestigateVLM-basedsubtaskplanningonfiveselectedRoboDojotaskgroups
coveringobjectclassification,blockstacking,blockswapping,mahjong,andtic-tac-toe. Totrain
thesubtask-conditionedpolicy,wesegmentdemonstrationsandpaireachsegmentwithasubtask
instruction. Attesttime,avision-languagemodel(VLM)usesvisualobservationsandexecution
feedbacktoselectthenextsubtaskforVPP2toexecute.
1BaselineresultsaretakenfromtheofficialRoboDojosimulationleaderboardasofSeptember2026.
8

|                |     | π    | π X-VLA     | Fast-WAM | OpenWAM-α | Xiaomi-Robotics-1 |       | GPT-6-Astra | VPP2(Ours) |
| -------------- | --- | ---- | ----------- | -------- | --------- | ----------------- | ----- | ----------- | ---------- |
|                |     | 0    | 0.5         |          |           |                   |       |             |            |
| Avg.Score      |     | 3.48 | 11.44 10.13 | 3.48     | 17.18     |                   | 20.07 | 28.97       | 39.26      |
| SuccessRate(%) |     | 1.53 | 6.93 6.52   | 2.03     | 11.92     |                   | 13.93 | 22.48       | 32.26      |
Table4: Post-trainingresultsontheRoboDojosimulationbenchmark. Averagescorecapturespartial
taskprogress, andsuccessratemeasuresbinarytaskcompletion; bothareaveragedoverthefive
| capabilitydimensions. |     |     | Baselineresultsaretakenfromtheofficialleaderboard. |     |      |                         |     |     |     |
| --------------------- | --- | --- | -------------------------------------------------- | --- | ---- | ----------------------- | --- | --- | --- |
|                       |     |     |                                                    |     | VPP2 | VPP2 + Subtask Planning |     |     |     |
Success rate (%)
100
|     |     | 70  |     | 76  |     |     |     |     |      |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
|     | 46  |     | 52  |     |     | 52  |     |     | 57.6 |
| 50  |     |     |     | 44  | 38  |     | 38  |     |      |
27.6
|     |     |     | 10  |     |     |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0
|     | Classify |     | Stack    | Swap   | Make |     | Tic-tac- |     | Average |
| --- | -------- | --- | -------- | ------ | ---- | --- | -------- | --- | ------- |
|     | objects  |     | by lang. | blocks | kong |     | toe      |     |         |
Figure9: SuccessrateswithandwithoutVLM-basedsubtaskplanning(50trialspertask). Average
isthefive-taskmean;thebaselinecheckpointmatchesTable4.
Figure 9 summarizes the results across the five selected task groups. The evaluated planning
configurationsachieveanaveragesuccessrateof57.6%,comparedwith27.6%forthebaseline. The
largest gains occur in language-conditioned block stacking (10% to 52%) and tic-tac-toe (0% to
38%).
| 5   | RELATED | WORKS |     |     |     |     |     |     |     |
| --- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
VideoFoundationModel. Videogenerationhasadvancedrapidlythroughlatentdiffusionmod-
els(Blattmannetal.,2023b;a)andlarge-scalediffusiontransformermodels(Yangetal.,2025;Wan
et al., 2025; Agarwal et al., 2025; 2026). Large-scale bidirectional video models provide strong
general-purposevideopriors;evenrecentautoregressivegeneratorsbuildonpretrainedbidirectional
models,usingthemforinitializationorasteachersbeforecausaladaptationanddistillation(Yinetal.,
2025;Huangetal.,2025). Thismotivatesourstrategyoffirstlearningageneralizablevideomodel
andthenadaptingitforefficientprediction. Besidesthetrainingstrategy,promptenhancementisan
importantcomponentofvideofoundationmodels(Yangetal.,2025;Wanetal.,2025). Similarly,we
useaVLMtoproducedetailed,manipulation-specificdescriptionsthatreduceambiguityinthese
mappings. After establishing this manipulation-focused video prior, we post-train the model for
fixed-horizonpredictionanddistillitforsingle-stepgenerationtosupportefficientactionlearning.
WorldActionModel. Worldactionmodels(WAMs)leveragevideopredictiontofacilitaterobot
policylearning. Earlyapproachesfirstgeneratefutureframesandtheninferactionsthroughinverse
dynamics(Duetal.,2023;Blacketal.,2023;Bharadhwajetal.,2024;Liangetal.,2024;Fengetal.,
2025),butiterativevideogenerationcanincursubstantiallatencyforclosed-loopcontrol.Hierarchical
approaches also combine video-based motion planning with reactive VLA control (Zhang et al.,
2026e). Morerecentapproachesconditionactionsonfeaturesfromvideomodels(Huetal.,2024;
Liao et al., 2025; Jia et al., 2025; Yan et al., 2026b) or jointly learn visual prediction and action
generation(Zhangetal.,2025;Guoetal.,2024;Lietal.,2025b;Zhuetal.,2025;Maetal.,2026;
Kimetal.,2026;Yanetal.,2026a;Yeetal.,2026;Lietal.,2026a;Bietal.,2026;MotubrainTeam
etal.,2026). Recentworkalsoexploresevent-groundedworld-actionlearning(Lietal.,2026b)and
large-scalemanipulation-specificpretraining(AgiBotResearchTeametal.,2026). Nevertheless,
actionlearningcancompromisepretrainedcapabilities,includingvideo-modelgeneralization(Mishra
etal.,2026)andVLMsemanticunderstanding(Zhangetal.,2026a). VPP2emphasizesinstruction-
alignedfutureprediction,combiningevent-levelpretrainingwithdetailedcaptions,fixed-horizon
post-training,andsingle-stepdistillationtoprovideanefficientvideobackboneforactionlearning.
6 CONCLUSION
WepresentedVideoPredictionPolicy2(VPP2),aworldactionmodelthatachievesstrongzero-shot
generalization in both video prediction and action generation. We first continue pretraining the
basevideomodeltoproducegeneralizable,instruction-followingpredictions,thenlearnapolicy
whilepreservingthesepredictivecapabilities. ExperimentsshowthatVPP2followsmanipulation
9

instructionsmorefaithfullythansubstantiallylargervideofoundationmodels,exhibitsstrongzero-
shotmanipulationcapabilitiesonareal-worldALOHAplatform,andachievesthehighestsuccess
ratesafterpost-trainingonchallengingbenchmarks. WehopethesefindingsencouragefutureWAM
researchtolookbeyondarchitecturalchoicesforactionmodelingandplacegreateremphasison
learninggeneralizablevideopredictionsandpreservingthisgeneralizationduringactionlearning.
10

ACKNOWLEDGMENTS
WethankYuchengHuandJiankeZhangforinsightfuldiscussionsthatgreatlybenefitedthedevelop-
mentofVPP2.
AI USE STATEMENT
WeusedgenerativeAItoolstoassistwithlanguagepolishing,improvetheclarityandreadability
ofthemanuscript,anddraftportionsofthepaper. Intheresearchprocess,thesetoolswereusedto
suggestexperimentalparametersettingsandassistwithsearchesforrelevantliteratureandtechnical
information. WealsousedAItoolstoannotatehumanandroboticmanipulationdatasetsatscale
formodeltraining. Theauthorsevaluatedthesuggestionsandmadethefinaldecisionsregarding
experimentaldesignandparameterselection. AllAI-assistedtextwasreviewedandrevisedbythe
authors,andretrievedinformationwascheckedagainstoriginalsourcesbeforeuse. Theauthorstake
fullresponsibilityforthefinalcontentofthepaper,includingitsdata,claims,results,andreferences.
REPRODUCIBILITY STATEMENT
Wedescribethemodelarchitecture,trainingobjectives,andevaluationprotocolsinthemaintext,
withadditionaldataprocessingdetailsprovidedintheappendix. Detailedtrainingconfigurations,
code,andmodelcheckpointsareavailableonourprojectwebsite.
REFERENCES
NiketAgarwal,ArslanAli,MaciejBala,YogeshBalaji,ErikBarker,TiffanyCai,PrithvijitChat-
topadhyay,YongxinChen,YinCui,YifanDing,etal. Cosmosworldfoundationmodelplatform
forphysicalai. arXivpreprintarXiv:2501.03575,2025.
NiketAgarwal,ArslanAli,JonAllen,MartinAntolini,AdelineAubame,AlissonAzzolini,Junjie
Bai, Maciej Bala, Yogesh Balaji, Josh Bapst, et al. Cosmos 3: Omnimodal world models for
physicalai. arXivpreprintarXiv:2606.02800,2026.
AgiBot Research Team, Renhang Liu, Wenzhi Zhao, Zhuo Yang, Liliang Chen, Pengfei Zhou,
ShengcongChen,GuanghuiRen,YoulunPeng,RongjunJin,etal. GE-Act2.0: Pretrainingand
scalingaworld-actionmodelforroboticmanipulation. arXivpreprintarXiv:2609.05588,2026.
URLhttps://arxiv.org/abs/2609.05588.
Arthur Allshire, Himanshu Gaurav Singh, Ritvik Singh, Adam Rashid, Hongsuk Choi, David
McAllister, Justin Yu, Yiyuan Chen, Huang Huang, Pieter Abbeel, et al. Scalable Behavior
CloningwithOpenData,Training,andEvaluation. arXivpreprintarXiv:2606.27375,2026. URL
https://arxiv.org/abs/2606.27375.
Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao
Deng, WeiDing, ChangGao, ChunjiangGe, etal. Qwen3-vltechnicalreport. arXivpreprint
arXiv:2511.21631,2025.
HomangaBharadhwaj,DebidattaDwibedi,AbhinavGupta,ShubhamTulsiani,CarlDoersch,Ted
Xiao,DhruvShah,FeiXia,DorsaSadigh,andSeanKirmani. Gen2act:Humanvideogenerationin
novelscenariosenablesgeneralizablerobotmanipulation. arXivpreprintarXiv:2409.16283,2024.
Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen
Zhao,YaoFeng,ChendongXiang,YinzeRong,HongyanZhao,HanyuLiu,ZhizhongSu,Lei
Ma, Hang Su, and Jun Zhu. Motus: A unified latent action world model. In Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 35101–35113,
2026. URL https://openaccess.thecvf.com/content/CVPR2026/html/Bi_
Motus_A_Unified_Latent_Action_World_Model_CVPR_2026_paper.html.
KevinBlack,MitsuhikoNakamoto,PranavAtreya,HomerWalke,ChelseaFinn,AviralKumar,and
SergeyLevine. Zero-shotroboticmanipulationwithpretrainedimage-editingdiffusionmodels.
arXivpreprintarXiv:2310.10639,2023.
11

KevinBlack,NoahBrown,DannyDriess,AdnanEsmail,MichaelEqui,ChelseaFinn,NiccoloFusai,
LachyGroom,KarolHausman,BrianIchter,etal. π0: Avision-language-actionflowmodelfor
generalrobotcontrol. arXivpreprintarXiv:2410.24164,2024.
AndreasBlattmann,TimDockhorn,SumithKulal,DanielMendelevitch,MaciejKilian,Dominik
Lorenz,YamLevi,ZionEnglish,VikramVoleti,AdamLetts,etal. Stablevideodiffusion: Scaling
latentvideodiffusionmodelstolargedatasets. arXivpreprintarXiv:2311.15127,2023a.
AndreasBlattmann,RobinRombach,HuanLing,TimDockhorn,SeungWookKim,SanjaFidler,and
KarstenKreis. Alignyourlatents: High-resolutionvideosynthesiswithlatentdiffusionmodels.
InProceedingsoftheIEEE/CVFConferenceonComputerVisionandPatternRecognition,pp.
22563–22575,2023b.
Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Xindong He, Xu Huang,
etal. AgiBotWorldColosseo: ALarge-scaleManipulationPlatformforScalableandIntelligent
EmbodiedSystems. InIEEE/RSJInternationalConferenceonIntelligentRobotsandSystems,
2025. URLhttps://arxiv.org/abs/2503.06669.
BytedanceSeed. Seed2.0modelcard: Towardsintelligencefrontierforreal-worldcomplexity. arXiv
preprintarXiv:2607.00248,2026.
BoyuanChen,TianyuanZhang,HaoranGeng,CaiyiZhang,PeihaoLi,KiwhanSong,WilliamTFree-
man,JitendraMalik,PieterAbbeel,RussTedrake,etal. Largevideoplannerenablesgeneralizable
robotcontrol. arXivpreprintarXiv:2512.15840,2025.
TianxingChen,YueChen,ZixuanLi,JunyuanTang,KailunSu,HaoranLu,WeijieWan,BaijunChen,
SonglingLiu,HaowenYan,etal. Robodojo: Aunifiedsim-and-realbenchmarkforcomprehensive
evaluationofgeneralistrobotmanipulationpolicies. arXivpreprintarXiv:2607.04434,2026.
Tsai-Shien Chen, Aliaksandr Siarohin, Willi Menapace, Ekaterina Deyneka, Hsiang-wei Chao,
ByungEunJeon,YuweiFang,Hsin-YingLee,JianRen,Ming-HsuanYang,andSergeyTulyakov.
Panda-70M:Captioning70mvideoswithmultiplecross-modalityteachers. InProceedingsof
theIEEE/CVFConferenceonComputerVisionandPatternRecognition, 2024. URLhttps:
//snap-research.github.io/Panda-70M/.
DimaDamen,HazelDoughty,GiovanniMariaFarinella,SanjaFidler,AntoninoFurnari,Evangelos
Kazakos,DavideMoltisanti,JonathanMunro,TobyPerrett,WillPrice,andMichaelWray. Scaling
egocentricvision: TheEPIC-KITCHENSdataset. InEuropeanConferenceonComputerVision,
2018. URLhttps://arxiv.org/abs/1804.02748.
YilunDu,SherryYang,BoDai,HanjunDai,OfirNachum,JoshTenenbaum,DaleSchuurmans,and
PieterAbbeel. Learninguniversalpoliciesviatext-guidedvideogeneration. AdvancesinNeural
InformationProcessingSystems,36,2023.
Hao-ShuFang,HongjieFang,ZhenyuTang,JirongLiu,ChenxiWang,JunboWang,HaoyiZhu,
andCewuLu. RH20T:AComprehensiveRoboticDatasetforLearningDiverseSkillsinOne-
Shot. In IEEE International Conference on Robotics and Automation, 2024. URL https:
//arxiv.org/abs/2307.00595.
YaoFeng,HengkaiTan,XinyiMao,GuodongLiu,ShuheHuang,ChendongXiang,HangSu,and
JunZhu. Vidar: Embodiedvideodiffusionmodelforgeneralistbimanualmanipulation. arXiv
preprintarXiv:2507.12898,2025.
Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, Joanna Materzynska, Susanne
Westphal, Heuna Kim, Valentin Haenel, Ingo Fruend, Peter Yianilos, Moritz Mueller-
Freitag, Florian Hoppe, Christian Thurau, Ingo Bax, and Roland Memisevic. The
“Something Something” video database for learning and evaluating visual common sense.
In Proceedings of the IEEE International Conference on Computer Vision, pp. 5842–
5850,2017.URLhttps://openaccess.thecvf.com/content_iccv_2017/html/
Goyal_The_Something_Something_ICCV_2017_paper.html.
12

Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit
Girdhar,JacksonHamburger,HaoJiang,MiaoLiu,XingyuLiu,etal. Ego4D:Aroundtheworld
in3,000hoursofegocentricvideo. InProceedingsoftheIEEE/CVFConferenceonComputer
Vision and Pattern Recognition, pp. 18995–19012, 2022. URL https://openaccess.
thecvf.com/content/CVPR2022/html/Grauman_Ego4D_Around_the_World_
in_3000_Hours_of_Egocentric_Video_CVPR_2022_paper.html.
JunGuo,PiaopiaoJin,JasonLi,PeiyanLi,YingyanLi,FutengLiu,WanliPeng,OptimusQin,Yifei
Su,NanSun,etal. Xiaomi-robotics-1: Scalingvision-language-actionmodelswithover100k
hoursofreal-worldtrajectories. arXivpreprintarXiv:2607.15330,2026.
YanjiangGuo,YuchengHu,JiankeZhang,Yen-JenWang,XiaoyuChen,ChaochaoLu,andJianyu
Chen. Predictionwithaction: Visualpolicylearningviajointdenoisingprocess. Advancesin
NeuralInformationProcessingSystems,37:112386–112410,2024.
RyanHoque,PeideHuang,DavidJ.Yoon,MouliSivapurapu,andJianZhang. EgoDex: Learning
DexterousManipulationfromLarge-ScaleEgocentricVideo. arXivpreprintarXiv:2505.11709,
2025. URLhttps://arxiv.org/abs/2505.11709.
EdwardJ.Hu,YelongShen,PhillipWallis,ZeyuanAllen-Zhu,YuanzhiLi,SheanWang,LuWang,
and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In International
ConferenceonLearningRepresentations,2022. URLhttps://openreview.net/forum?
id=nZeVKeeFYf9.
YuchengHu,YanjiangGuo,PengchaoWang,XiaoyuChen,Yen-JenWang,JiankeZhang,Koushil
Sreenath,ChaochaoLu,andJianyuChen. Videopredictionpolicy: Ageneralistrobotpolicywith
predictivevisualrepresentations. arXivpreprintarXiv:2412.14803,2024.
Xun Huang, Zhengqi Li, Guande He, Mingyuan Zhou, and Eli Shechtman. Self forc-
ing: Bridging the train-test gap in autoregressive video diffusion. In Advances in Neu-
ral Information Processing Systems, volume 38, 2025. doi: 10.52202/085713-5576.
URL https://proceedings.neurips.cc/paper_files/paper/2025/hash/
f4823f831af67a3ef15e41a85434422a-Abstract-Conference.html.
PhysicalIntelligence,KevinBlack,NoahBrown,JamesDarpinian,KaranDhabalia,DannyDriess,
AdnanEsmail,MichaelEqui,ChelseaFinn,NiccoloFusai,etal. π : avision-language-action
0.5
modelwithopen-worldgeneralization. arXivpreprintarXiv:2504.16054,2025.
YueruJia,JiamingLiu,ShengbangLiu,RuiZhou,WanheYu,YuyangYan,XiaoweiChi,Yandong
Guo, Boxin Shi, and Shanghang Zhang. Video2Act: A dual-system video diffusion policy
withroboticspatio-motionalmodeling. arXivpreprintarXiv:2512.03044,2025. URLhttps:
//arxiv.org/abs/2512.03044.
TaoJiang,TianyuanYuan,YichengLiu,ChenhaoLu,JianningCui,XiaoLiu,ShuiqiCheng,Jiyang
Gao,HuazheXu,andHangZhao. GalaxeaOpen-WorldDatasetandG0Dual-SystemVLAModel.
arXivpreprintarXiv:2509.00576,2025. URLhttps://arxiv.org/abs/2509.00576.
Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth
Karamcheti,SoroushNasiriany,MohanKumarSrirama,LawrenceYunliangChen,KirstyEllis,
etal.Droid:Alarge-scalein-the-wildrobotmanipulationdataset.arXivpreprintarXiv:2403.12945,
2024.
Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang,
Shuran Song, Ming-Yu Liu, Chelsea Finn, and Jinwei Gu. Cosmos policy: Fine-tuning video
modelsforvisuomotorcontrolandplanning. arXivpreprintarXiv:2601.16163,2026.
JasonLee, JiafeiDuan, HaoquanFang, YuquanDeng, ShuoLiu, BoyangLi, BohanFang, Jieyu
Zhang,YiRuWang,SanghoLee,etal. Molmoact: Actionreasoningmodelsthatcanreasonin
space. arXivpreprintarXiv:2508.07917,2025.
LinLi,QihangZhang,YimingLuo,ShuaiYang,RuilinWang,FeiHan,MingruiYu,ZelinGao,Nan
Xue,XingZhu,YujunShen,andYinghaoXu. Causalworldmodelingforrobotcontrol. arXiv
preprintarXiv:2601.21998,2026a. doi: 10.48550/arXiv.2601.21998. URLhttps://arxiv.
org/abs/2601.21998.
13

Qixiu Li, Yu Deng, Yaobo Liang, Lin Luo, Lei Zhou, Chengtang Yao, Lingqi Zeng, Zhiyuan
Feng, HuizhiLiang, Sicheng Xu, YizhongZhang, XiChen, Hao Chen, LilySun, DongChen,
JiaolongYang,andBainingGuo. Scalablevision-language-actionmodelpretrainingforrobotic
manipulationwithreal-lifehumanactivityvideos. arXivpreprintarXiv:2510.21571,2025a. URL
https://arxiv.org/abs/2510.21571.
Quanyi Li. Vlas are confined yet capable of generalizing to novel instructions. arXiv preprint
arXiv:2505.03500,2025.
Shalfun Li, Victor Yao, Charles Yang, Truth Qu, Regis Cheng, Ryan Yu, Howard Lu, Newton
Von, Vincent Chen, Yohann Tang, et al. WALL-WM: Carving world action modeling at the
eventjoints. arXivpreprintarXiv:2606.01955,2026b. doi: 10.48550/arXiv.2606.01955. URL
https://arxiv.org/abs/2606.01955.
ShuangLi,YihuaiGao,DorsaSadigh,andShuranSong. Unifiedvideoactionmodel. arXivpreprint
arXiv:2503.00200,2025b.
JunbangLiang,RuoshiLiu,EgeOzguroglu,SruthiSudhakar,AchalDave,PavelTokmakov,Shuran
Song,andCarlVondrick. Dreamitate: Real-worldvisuomotorpolicylearningviavideogeneration.
arXivpreprintarXiv:2406.16862,2024.
Weixin Liang, Lili Yu, Liang Luo, Srinivasan Iyer, Ning Dong, Chunting Zhou, Gargi Ghosh,
MikeLewis,Wen-tauYih,LukeZettlemoyer,andXiVictoriaLin. Mixture-of-Transformers: A
sparseandscalablearchitectureformulti-modalfoundationmodels. TransactionsonMachine
Learning Research, 2025. ISSN 2835-8856. URL https://openreview.net/forum?
id=OutjGuJnNk.
Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu,
JingbinCai,SiLiu,JianlanLuo,etal. Genieenvisioner: Aunifiedworldfoundationplatformfor
roboticmanipulation. arXivpreprintarXiv:2508.05635,2025.
YaronLipman,RickyT.Q.Chen,HeliBen-Hamu,MaximilianNickel,andMattLe. Flowmatching
forgenerativemodeling. InInternationalConferenceonLearningRepresentations,2023. URL
https://openreview.net/forum?id=PqvMRDCJT9t.
BoLiu,YifengZhu,ChongkaiGao,YihaoFeng,QiangLiu,YukeZhu,andPeterStone. Libero:
Benchmarkingknowledgetransferforlifelongrobotlearning. AdvancesinNeuralInformation
ProcessingSystems,36,2023.
SongmingLiu,LingxuanWu,BangguoLi,HengkaiTan,HuayuChen,ZhengyiWang,KeXu,Hang
Su,andJunZhu. Rdt-1b: adiffusionfoundationmodelforbimanualmanipulation. arXivpreprint
arXiv:2410.07864,2024.
TeliMa,JiaZheng,ZifanWang,ChunliJiang,AndyCui,JunweiLiang,andShuoYang. Dit4dit:
Jointly modeling video dynamics and actions for generalizable robot control. arXiv preprint
arXiv:2603.10448,2026.
FarzanehMahdisoltani,GuillaumeBerger,WaseemGharbieh,DavidFleet,andRolandMemisevic.
Ontheeffectivenessoftaskgranularityfortransferlearning. arXivpreprintarXiv:1804.09235,
2018. URLhttps://arxiv.org/abs/1804.09235.
Utkarsh A Mishra, Yongxin Chen, Danfei Xu, Yang Liu, Xi Chen, and Jiayuan Mao. Under-
standingandmitigatingthevideo-actiongeneralizationgapviatemporalratio. arXivpreprint
arXiv:2607.08127,2026.
Motubrain Team, Chendong Xiang, Fan Bao, Haitian Liu, Hengkai Tan, Hongzhe Bi, James Li,
Jiabao Liu, Jingrui Pang, Kiro Jing, Louis Liu, Mengchen Cai, Rongxu Cui, Ruowen Zhao,
RunqingWang,ShuheHuang,YaoFeng,YinzeRong,ZeyuanWang,andJunZhu. Motubrain:
Anadvancedworldactionmodelforrobotcontrol. arXivpreprintarXiv:2604.27792,2026. doi:
10.48550/arXiv.2604.27792. URLhttps://arxiv.org/abs/2604.27792.
14

KepanNan,RuiXie,PenghaoZhou,TiehanFan,ZhenhengYang,ZhijieChen,XiangLi,JianYang,
andYingTai. OpenVid-1M:ALarge-ScaleHigh-QualityDatasetforText-to-videoGeneration.
InInternationalConferenceonLearningRepresentations,2025. URLhttps://arxiv.org/
abs/2407.02371.
OpenX-EmbodimentCollaboration. OpenX-Embodiment: RoboticLearningDatasetsandRT-X
Models. arXivpreprintarXiv:2310.08864,2023. URLhttps://arxiv.org/abs/2310.
08864.
William Peebles and Saining Xie. Scalable diffusion models with transformers. In Proceed-
ings of the IEEE/CVF International Conference on Computer Vision, pp. 4195–4205, 2023.
URL https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_
Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html.
LucyXiaoyangShi,BrianIchter,MichaelEqui,LiyimingKe,KarlPertsch,QuanVuong,James
Tanner,AnnaWalling,HaohuanWang,NiccoloFusai,etal. Hirobot: Open-endedinstruction
following with hierarchical vision-language-action models. arXiv preprint arXiv:2502.19417,
2025.
YangSong,PrafullaDhariwal,MarkChen,andIlyaSutskever. Consistencymodels. InProceedings
ofthe40thInternationalConferenceonMachineLearning,volume202ofProceedingsofMachine
Learning Research, pp. 32211–32252. PMLR, 2023. URL https://proceedings.mlr.
press/v202/song23a.html.
XiaoquanSun,ZetianXu,ChenCao,ZongheLiu,YihanSun,JingruiPang,RuijianZhang,Zhen
Yang,KangPang,DingxinHe,etal. Atomvla: Scalablepost-trainingforroboticmanipulationvia
predictivelatentworldmodels. arXivpreprintarXiv:2603.08519,2026.
YangTian,YuyinYang,YimanXie,ZetaoCai,XuShi,NingGao,HangxuLiu,XuekunJiang,Zherui
Qiu,FengYuan,etal. InternData-A1: PioneeringHigh-FidelitySyntheticDataforPre-training
GeneralistPolicy. arXivpreprintarXiv:2511.16651,2025. URLhttps://arxiv.org/abs/
2511.16651.
Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu,
HaimingZhao,JianxiaoYang,etal. Wan: Openandadvancedlarge-scalevideogenerativemodels.
arXivpreprintarXiv:2503.20314,2025.
YuranWang,SiqiaoHuang,MingleyangLi,ChenhaoZhang,JiaqiLiang,WeiyangJin,YueChen,
XueminChi,DonghaoZhou,QizeYu,etal. Openwam: Anopen,modularexplorationtowards
systematicworld-actionmodelpretraining. arXivpreprintarXiv:2609.07398,2026a.
Ziyu Wang, Chenyuan Liu, Yushun Xiang, Runhao Zhang, Qingbo Hao, Hongliang Lu, Houyu
Chen,ZhizhongFeng,KaiyueZheng,DehaoYe,etal. TheGreatMarch100: 100Detail-oriented
Tasks for Evaluating Embodied AI Agents. arXiv preprint arXiv:2601.11421, 2026b. URL
https://arxiv.org/abs/2601.11421.
KunWu,ChengkaiHou,JiamingLiu,ZhengpingChe,XiaozhuJu,ZhuqinYang,MengLi,Yinuo
Zhao,ZhiyuanXu,GuangYang,etal. RoboMIND:BenchmarkonMulti-embodimentIntelligence
Normative Data for Robot Manipulation. In Robotics: Science and Systems, 2025a. URL
https://arxiv.org/abs/2412.13877.
Shihan Wu, Xuecheng Liu, Shaoxuan Xie, Pengwei Wang, Xinghang Li, Bowen Yang, Zhe Li,
Kai Zhu, Hongyu Wu, Yiheng Liu, et al. RoboCOIN: An Open-Sourced Bimanual Robotic
Data Collection for Integrated Manipulation. arXiv preprint arXiv:2511.17441, 2025b. URL
https://arxiv.org/abs/2511.17441.
HaodongYan,JunfengLi,JunjieHe,ZhideZhong,MingMingYu,WenxuanSong,JiaguanZhu,
YangyangZheng,YuqiaoDu,JiadiYou,etal. Robust-wam: Bridginggenerativepretrainingand
semanticforesightinworld-actionmodels. arXivpreprintarXiv:2608.05903,2026a.
HaodongYan,ZhideZhong,JiaguanZhu,JunjieHe,WeilinYuan,WenxuanSong,XinGong,Yingjie
Cai,GuanyiZhao,XuYan,etal. S-vam: Shortcutvideo-actionmodelbyself-distillinggeometric
andsemanticforesight. arXivpreprintarXiv:2603.16195,2026b.
15

Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming
Yang,WenyiHong,XiaohanZhang,GuanyuFeng,etal. CogVideoX:Text-to-videodiffusion
modelswithanexperttransformer. InInternationalConferenceonLearningRepresentations,
2025. URL https://proceedings.iclr.cc/paper_files/paper/2025/hash/
ce31378e9f41d8907e97dab172b6c559-Abstract-Conference.html.
SeonghyeonYe,YunhaoGe,KaiyuanZheng,ShenyuanGao,SihyunYu,GeorgeKurian,Suneel
Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. World action models are zero-
shotpolicies. arXivpreprintarXiv:2602.15922,2026. doi: 10.48550/arXiv.2602.15922. URL
https://arxiv.org/abs/2602.15922.
TianweiYin,QiangZhang,RichardZhang,WilliamT.Freeman,FredoDurand,EliShechtman,and
XunHuang. Fromslowbidirectionaltofastautoregressivevideodiffusionmodels. InProceedings
oftheIEEE/CVFConferenceonComputerVisionandPatternRecognition, pp.22963–22974,
2025. URLhttps://openaccess.thecvf.com/content/CVPR2025/html/Yin_
From_Slow_Bidirectional_to_Fast_Autoregressive_Video_Diffusion_
Models_CVPR_2025_paper.html.
TianyuanYuan,ZibinDong,YichengLiu,andHangZhao. Fast-wam: Doworldactionmodelsneed
test-timefutureimagination? arXivpreprintarXiv:2603.16666,2026.
JiankeZhang,YanjiangGuo,YuchengHu,XiaoyuChen,XiangZhu,andJianyuChen. UP-VLA:
Aunifiedunderstandingandpredictionmodelforembodiedagent. InProceedingsofthe42nd
InternationalConferenceonMachineLearning,volume267ofProceedingsofMachineLearning
Research, pp. 74911–74922. PMLR, 2025. URL https://proceedings.mlr.press/
v267/zhang25w.html.
JiankeZhang,YuanfeiLuo,YuchengHu,XiaoyuChen,YanjiangGuo,ZiyangLiu,HongbinXu,
TianLan,andJianyuChen. UAM:Adual-streamperspectiveonforgettinginVLAtraining. arXiv
preprintarXiv:2605.15735,2026a. doi: 10.48550/arXiv.2605.15735. URLhttps://arxiv.
org/abs/2605.15735.
JieZhang,XiaoyueChen,AnzheChen,DayihengLiu,DeqingLi,GengzeZhou,HaleYin,Haoqi
Yuan,HaoyangLi,JiahaoLi,etal. Qwen-robotworldtechnicalreport: Unifyingembodiedworld
modeling through language-conditioned video generation. arXiv preprint arXiv:2606.17030,
2026b.
WenboZhang,KaixuanWang,YutaoOuyang,XiaoyuHuang,LiyangLi,KailunSu,WeiyangJin,
WenhaoChai,HaotianLiang,ZhiyangDou,etal. Anunexpectedrobotpolicy: Earlyevaluations
ofgpt-6astraonrobodojoandbeyond. arXivpreprintarXiv:2609.24170,2026c.
Yixian Zhang, Huanming Zhang, Feng Gao, Xiao Li, Zhihao Liu, Chunyang Zhu, Jiaxing Qiu,
Yuchen Yan, Jiyuan Liu, Wenhao Tang, et al. Harness vla: Steering frozen vlas into reliable
manipulationprimitivesviamemory-guidedagents. arXivpreprintarXiv:2607.08448,2026d.
Zhongru Zhang, Chenghan Yang, Qingzhou Lu, Yanjiang Guo, Jianke Zhang, Yucheng Hu, and
Jianyu Chen. Veo-Act: Enhancing VLA policies with frontier video models. arXiv preprint
arXiv:2604.04502, 2026e. doi: 10.48550/arXiv.2604.04502. URL https://arxiv.org/
abs/2604.04502.
TonyZZhao, VikashKumar, SergeyLevine, andChelseaFinn. Learningfine-grainedbimanual
manipulationwithlow-costhardware. arXivpreprintarXiv:2304.13705,2023.
JinliangZheng,JianxiongLi,ZhihaoWang,DongxiuLiu,XiruiKang,YuchunFeng,YinanZheng,
Jiayin Zou, Yilun Chen, Jia Zeng, et al. X-vla: Soft-prompted transformer as scalable cross-
embodimentvision-language-actionmodel. InInternationalConferenceonLearningRepresenta-
tions,2026.
XueyangZhou,YangmingXu,GuiyaoTie,YongchaoChen,GuowenZhang,DuanfengChu,Pan
Zhou,andLichaoSun. Libero-pro: Towardsrobustandfairevaluationofvision-language-action
modelsbeyondmemorization. arXivpreprintarXiv:2510.03827,2025.
16

ChuningZhu,RaymondYu,SiyuanFeng,BenjaminBurchfiel,PaarthShah,andAbhishekGupta.
Unifiedworldmodels:Couplingvideoandactiondiffusionforpretrainingonlargeroboticdatasets.
arXivpreprintarXiv:2504.02792,2025.
17

A DATASET PROCESS DETAILS
DatasetSources. Table5providesthefulldatasetreferencesforthetrainingdatasummarizedin
Table1.
DataType EmbodimentType DataSources
Single-arm OXE (Open X-Embodiment Collaboration, 2023), RoboMIND (Wu
Robot etal.,2025a), DROID(Khazatskyetal.,2024), RH20T(Fangetal.,
2024),MolmoAct(Leeetal.,2025)
Dual-arm AgiBotWorld-Beta(Buetal.,2025),RoboCOIN(Wuetal.,2025b),
RDT(Liuetal.,2024),GM-100(Wangetal.,2026b),ABC-130K(All-
shireetal.,2026),Self-collectedALOHAData
Mobile&humanoid InternData-A1(Tianetal.,2025), GalaxeaOpen-World(Jiangetal.,
2025),Self-collecteddexteroushands
Open-source: EgoDex(Hoqueetal.,2025), Ego4D(Graumanetal.,
Human Humanhands
2022),EPIC-KITCHENS(Damenetal.,2018),Something-Something
V2(Goyaletal.,2017;Mahdisoltanietal.,2018),VITRA-1M(Lietal.,
2025a)
Self-collectedegocentricdata
GeneralVideo Humanhands OpenVid(Nanetal.,2025),Panda-70M(Chenetal.,2024)
Table5: Trainingdatasourceswithreferencestotheoriginaldatasets. Self-collecteddatasetsare
collectedaspartofthiswork.
A.1 VIDEOCAPTIONING.
Aftersegmentation,weuseaVLMtogeneratedetailedcaptionsforeachclipaccordingtoapredefined
template. Ourcaptioningpipelineaimstoreduceuncertaintyinfuturepredictionandencourage
consistentmappingsfromsemanticdescriptionstovisualtrajectories. Specifically,weaddressfour
majorsourcesofuncertainty:
(1)DetailedTaskDescription. Wedescribehowtheendeffectorcompletesthetask,includingthe
sequenceandmannerofmanipulation.
(2)ExplicitEnd-EffectorIdentification. Theactiveendeffectormustbevisibleinthefirstframe;
otherwise,wetrimthecliptobeginwhenitfirstbecomesvisible. Whenmultipleendeffectorsare
involved,wedescribethemotionofeachoneexplicitly.
(3)UnambiguousTarget-ObjectSpecification. Whenmultipleidenticalorsimilarobjectsarepresent,
weidentifythetargetusingdistinctiveattributesorspatialrelationships. Thetargetobjectmustalso
bevisibleinthefirstframe.
(4) Camera-View Description. We use optical flow to remove egocentric clips with excessive
viewpointchanges. Forclipswithmoderatecameramotion,aVLMdescribestheviewpointchanges
andthecameraviewsincludedinthevideo,andweincorporatethisinformationintothecaption.
A.2 UNIFIEDACTIONSPACE
Wefocusonegocentricbimanualdatasets,includingALOHA-style,humanoid-style,andhuman
egocentricdatasets. Thesedatasetsaccountformorethan80%ofthetotaldataandshareasimilar
bimanual structure and camera viewpoint. We explicitly align their coordinate systems at two
levels: (1)workspacealignment,whichappliesaworld-frametransformationsothatdifferentrobots
have comparable end-effector workspaces; and (2) end-effector alignment, which applies a local
transformationtostandardizeend-effectororiginsandaxisorientations.
Foranarmdatasetd,letT
d
=WdT
Ed
∈SE(3)denotetheoriginalend-effectorpose,whereW
d
and
E arethedataset’sworldandend-effectorframes,respectively. Wedefinetheworkspacealignment
d
asA
d
=W¯T
Wd
andtheend-effectoralignmentasB
d
=EdT E¯,whereW¯ andE¯denotethecanonical
worldandend-effectorframes. Thealignedend-effectorposeisgivenby
T(cid:101)d =A
d
T
d
B
d
, (6)
18

B MORE VIDEO PREDICTION RESULTS
after
distillation
(a) Instruction: Transfer the bowl from the top left onto the towel.
after
distillation
(b) Instruction: Stack the bowl in the middle on top of the bowl on the right.
after
distillation
(c) Instruction: Grasp the two corners of the cloth and fold it upward.
after
distillation
(d) Instruction: Move the green apple out of the basket and place it on the left.
after
distillation
(e) Instruction: Place the candy on the left into the bowl filled with the same type of candy.
after
distillation
(f) Instruction: Pull out a tissue and use it to wipe the plate.
after
distillation
(g) Instruction: Place the blue bowl in the microwave.
after
distillation
(h) Instruction: Remove the paper covering the bowl so that the bowl is fully visible.
Figure10: Additionalvideopredictionresultsonopen-endedtasks. Wecomparesingle-stepvideo
predictionsbeforeandafterdistillation. Distillationenableshigh-qualityvideopredictionwithjust
onesamplingstep.
19

| C DETAILED | BENCHMARK | RESULTS |     |     |     |     |
| ---------- | --------- | ------- | --- | --- | --- | --- |
C.1 DETAILEDLIBERORESULTS
Table6reportsper-suitesuccessratesonthefourstandardLIBEROsuites(Liuetal.,2023),which
correspondtotheLIBERO-IDresultsinTable3. Baselineresultsaretakenfromtheoriginalpapers
andfromZhangetal.(2026d)andMishraetal.(2026).
|     | Method              |     | Spatial Object | Goal | Long Avg. |     |
| --- | ------------------- | --- | -------------- | ---- | --------- | --- |
|     | π (Blacketal.,2024) |     | 96.8 98.8      | 95.8 | 85.2 94.2 |     |
0
|     | π (Intelligenceetal.,2025) |     | 98.8 98.2 | 98.0 | 92.4 96.9 |     |
| --- | -------------------------- | --- | --------- | ---- | --------- | --- |
0.5
|     | MolmoAct(Leeetal.,2025)         |     | 87.0 95.4  | 87.6 | 77.2 86.6 |     |
| --- | ------------------------------- | --- | ---------- | ---- | --------- | --- |
|     | X-VLA(Zhengetal.,2026)          |     | 98.2 98.6  | 97.8 | 97.6 98.1 |     |
|     | AtomVLA(Sunetal.,2026)          |     | 96.4 99.6  | 97.6 | 94.4 97.0 |     |
|     | Cosmos-Policy(Kimetal.,2026)    |     | 98.1 100.0 | 98.2 | 97.6 98.5 |     |
|     | Fast-WAM(Yuanetal.,2026)        |     | 98.2 100.0 | 97.0 | 95.2 97.6 |     |
|     | DiT4DiT(Maetal.,2026)           |     | 98.4 99.6  | 98.6 | 97.6 98.6 |     |
|     | TemporalRatio(Mishraetal.,2026) |     | 96.3 99.6  | 97.6 | 82.6 94.0 |     |
|     | VPP2(Ours)                      |     | 99.2 99.8  | 98.2 | 98.0 98.8 |     |
Table6: Per-suitesuccessrates(%)onthestandardLIBERObenchmark. Bestresultsineachcolumn
areinbold.
C.2 DETAILEDROBODOJORESULTS
RoboDojo(Chenetal.,2026)evaluatesgeneralistmanipulationpolicieson42bimanualsimulation
tasks organized into five capability dimensions. Generalization tests robustness to unseen back-
grounds,lighting,clutter,andtargetobjects,andisevaluatedunderbothstandardandrandomized
settings. Precisionrequiresfine-grainedtargetlocalizationandcontact-richcontrol. Long-Horizon
requirescompletingallsub-stepsofmulti-steptasks. Memorycontainstaskswhosecorrectactions
dependoninformationobservedearlierintheepisode. Openevaluatesunseentaskspecifications
whose required skills appear in the training data under different contexts. We follow the official
trainingandevaluationprotocol. Theaveragescorecapturespartialtaskprogress,andthesuccess
ratemeasuresbinarytaskcompletion.
Tables7and8reporttheper-dimensionaveragescoreandsuccessrate,respectively,complementing
Table4.BaselineresultsaretakenfromtheofficialRoboDojosimulationleaderboardasofSeptember
2026.
Generalization
| Method              |     | Std. | Rand. Precision Long-Horizon |      | Memory Open | Avg. |
| ------------------- | --- | ---- | ---------------------------- | ---- | ----------- | ---- |
| π (Blacketal.,2024) |     | 7.18 | 0.71 3.56                    | 6.19 | 3.47 0.25   | 3.48 |
0
π (Intelligenceetal.,2025) 20.93 5.82 12.40 23.54 5.89 1.98 11.44
0.5
X-VLA(Zhengetal.,2026) 17.90 3.04 18.32 16.53 4.76 0.55 10.13
| Fast-WAM(Yuanetal.,2026) |     | 4.33 | 0.34 1.96 | 9.14 | 3.55 0.42 | 3.48 |
| ------------------------ | --- | ---- | --------- | ---- | --------- | ---- |
OpenWAM-α(Wangetal.,2026a) 33.16 8.26 18.45 34.93 10.41 1.41 17.18
Xiaomi-Robotics-1(Guoetal.,2026) 35.65 11.44 26.69 38.39 7.81 3.94 20.07
GPT-6-Astra(Zhangetal.,2026c) 35.32 31.40 12.65 21.45 43.04 34.36 28.97
| VPP2(Ours) |     | 36.39 | 43.03 | 56.28 | 56.01 4.61 | 39.26 |
| ---------- | --- | ----- | ----- | ----- | ---------- | ----- |
Table7: Per-dimensionaveragescoreontheRoboDojosimulationbenchmark. Generalizationis
evaluatedunderstandard(Std.) andrandomized(Rand.) settings. Avg.isthemeanoverthefive
capabilitydimensions,wherethegeneralizationscoreisthemeanoftheStd.andRand.settings. For
VPP2,wereportthegeneralizationresultpooledoverbothsettings(25episodeseach,followingthe
officialprotocol),whichequalstheirmean. Baselineresultsaretakenfromtheofficialleaderboard.
20

Generalization
| Method                | Std. Rand. | Precision | Long-Horizon | Memory Open | Avg. |
| --------------------- | ---------- | --------- | ------------ | ----------- | ---- |
| π 0 (Blacketal.,2024) | 4.89 0.22  | 0.75      | 2.00         | 2.11 0.25   | 1.53 |
π 0.5 (Intelligenceetal.,2025) 14.89 1.44 5.50 14.67 4.67 1.67 6.93
| X-VLA(Zhengetal.,2026)   | 12.22 1.33 | 12.00 | 9.75 | 3.56 0.50 | 6.52 |
| ------------------------ | ---------- | ----- | ---- | --------- | ---- |
| Fast-WAM(Yuanetal.,2026) | 2.11 0.11  | 0.00  | 5.17 | 3.44 0.42 | 2.03 |
OpenWAM-α(Wangetal.,2026a) 25.56 4.11 9.25 25.33 9.11 1.08 11.92
Xiaomi-Robotics-1(Guoetal.,2026) 28.00 6.00 18.83 23.67 6.56 3.58 13.93
GPT-6-Astra(Zhangetal.,2026c) 32.67 28.33 4.00 8.25 38.67 31.00 22.48
| VPP2(Ours) | 29.50 | 35.17 | 37.00 | 55.56 4.08 | 32.26 |
| ---------- | ----- | ----- | ----- | ---------- | ----- |
Table8: Per-dimensionsuccessrate(%)ontheRoboDojosimulationbenchmark,computedinthe
samewayasTable7.
21