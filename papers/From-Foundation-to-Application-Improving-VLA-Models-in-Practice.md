From Foundation to Application:
Improving VLA Models in Practice
WeiWu∗,FangjingWang∗,FanLu,HeSun,ShiLiu,YunnanWang,YibinYan,YongWang,
ShuaileiMa,XinyangWang,YibinLiu,ShuaiYang,TianxiangZhou,KejiaZhang,LeiZhou,ChengSu,
NanXue,BinTan,HanZhang,YouchaoZhang,FeiLiao,XingZhu,YujunShen,KechengZheng†
∗EqualContribution †ProjectLead
Despite recent progress of VLA foundation models, the disparity between laboratory conditions and real-
world applications continues to impede their practical implementation. To bridge this gap, we present
LingBot-VLA 2.0, which advances LingBot-VLA through improvements in three functional domains.
(1) Generalization across tasks and embodiments. Compared to the previous version, we revamp the data
processingpipelineandcuratearound60,000hoursofdataforpretraining,including50,000hoursofrobot
trajectoriesspanning20robotconfigurationsand10,000hoursofegocentrichumanvideos. (2)Expanded
actionspaceinadditiontodual-armhardwareplatforms. Inparticular,oursystemaccommodatesdegreesof
freedomfortheheads,waists,mobilebases,anddexteroushands,therebyempoweringtherobotstotackle
morecomplextasksinpracticalscenarios. (3)Predictivedynamicsmodelingforimprovedtemporalreasoning.
Specifically,weformulatefuturepredictionasaproxytask,facilitatedbyavideorepresentationmodelfor
semanticpriorsandadepthestimationmodelforgeometriccues. EvaluationsontheGM-100benchmark,
conductedinageneralistsetting,validatethebeneficialimpactoftheseproposedmodifications. Furthermore,
benefitingfromtheexpandedpretrainingdatathatcoverswhole-bodydegreesoffreedom,LingBot-VLA-2.0
demonstratesstrongcross-embodimentlong-horizonmobilemanipulationcapabilityacrossthetworobotic
platforms.
Website:https://technology.robbyant.com/lingbot-vla-v2
Github:https://github.com/robbyant/lingbot-vla-v2
Checkpoints:https://huggingface.co/collections/robbyant/lingbot-vla-v2
1 Introduction
Vision-language-action(VLA)models[4–6,16]haverecentlyemergedasapromisingparadigmforbuildinggeneralist
robotpolicies. Akeyadvantageofthisparadigmisthatpretrainedvision-languagemodelsproviderichmultimodal
alignmentandsemanticrepresentations,enablingVLAmodelstobetterunderstandcomplexscenesandgeneralize
acrossdiversetasks. Beyondsuchmodel-levelpriors,recentadvances[5,31]furthershowthatscalinguprobotdatain
bothquantityanddiversitycansubstantiallyimprovethecapabilityofVLAsystems. Together,thesedevelopmentshave
establishedVLAasacompellingfoundationforrobotlearning.
However, despitethisrapidprogress, asubstantialgapremainsbetweenlaboratorybenchmarksandreal-world
deployment. Inpractice,robotsareexpectedtooperateunderbroaderembodimentdiversity,richeractionspaces,and
moredynamicenvironmentsthanthoseconsideredinmanyexistingVLAsettings. First,generalizationinpracticeis
notonlyabouttransferringacrosstasks,butalsoabouthandlingheterogeneousrobotconfigurationsanddatasources.
Anotherpointisthatmanyreal-worldplatformsinvolvesubstantiallymoredegreesoffreedomthanstandarddual-arm
manipulationsetups,includingheadmovement,waist,mobile-basecontrol,anddexteroushands. Subsequently,real-
worldexecutionoftenrequiresanticipatingfuturesceneevolutionandactionconsequences,ratherthanreactingonlyto
currentobservations. ThesechallengescollectivelylimitthepracticalutilityofcurrentVLAfoundationmodels.
1
6202
luJ
7
]OR.sc[
1v30460.7062:viXra

Current/Future Targets
Continuous Actions
Action Expert with
Understanding Expert
MoELayers
Robot State Noised Actions
strepxE
derahS
1 trepxE 2 trepxE 3 trepxE 4 trepxE 2-N trepxE 1-N trepxE N trepxE
LingBot-Depth & DINO-Video
Unify
ActionSpace
Current Targets Future Targets
Distillation Loss
Arm7D/6D EEF7D Gripper1D Move3D Waist4D Head2D Hand6D
Current Queries Future Queries
LingBot-Depth DetailofMoELayer
DINO-Video A C li u g r n r m en e t n / t F u La tu y r e e r s
Linear + Norm
… Cross Attention
Top-K
Linear
Alignment Queries
Router
"Ar in ra t n h g e e v f a lo se w " ers Q Cu u r e r r e ie n s t Q Fu u t e u r r ie e s H I i n d p d u e t n VLM Current/Future Queries
(a) Framework of LingBot-VLA 2.0 (b) Dual-Query Distillation
Figure1. OverviewofLingBot-VLA 2.0.Werevampthedataprocessingpipelineandcurate60,000hoursofpretrainingdata,
including50,000hoursofrobottrajectoriesacross20robotconfigurationsand10,000hoursofegocentrichumanvideos.Moreover,
ourmodelsupportsdegreesoffreedomforthehead,waist,mobilebase,anddexteroushands,enablingrobotstohandlemorecomplex
real-worldtasks.Weformulatefuturepredictionasaproxytask,leveragingavideorepresentationmodelforsemanticpriorsanda
depthestimationmodelforgeometriccues.
Agrowingbodyofworkhasstartedtoaddresstheseissuesfromdifferentperspectives.Someapproaches[21,31,38]
scalerobotpretrainingdatatoimprovecross-taskandcross-embodimentrobustness. Othersincorporateembodiment-
awarearchitecturaldesigns[13]tobetterhandleheterogeneousrobots. AnotherlineofresearchaugmentsVLAmodels
withlatentactionmodel[11,23]toimprovedecisionmakingindynamicenvironments. Meanwhile,recentsystem-
orientedeffortshaveemphasizedthatpracticalVLAdeploymentdependsnotonlyonmodelscale,butalsoondata
quality,actioncoverage,andtrainingobjectivesthatbetteralignpretrainingwithdownstreamexecution. Thesetrends
indicatethatimprovingVLAmodelsinpracticerequiresacoordinatedtreatmentofdata,embodiment,andpredictive
capability.
Inthiswork,webuildonthisperspectiveandpresentLingBot-VLA 2.0,animprovedversionofLingBot-VLA
aimedatbridgingfoundation-levelVLAcapabilitieswithpracticalroboticdeployment. Ratherthanfocusingona
singleimprovement,LingBot-VLA 2.0advancesthesystemalongthreefunctionaldomainsthatwefindparticularly
criticalforreal-worlddeployment. First,toimprovegeneralizationacrosstasksandembodiments,weredesignthe
dataprocessingpipelineandcuratealarge-scalepretrainingcorpusofaround60,000hours,including50,000hoursof
robottrajectoriesspanning20robotconfigurationsand10,000hoursofegocentrichumanvideos. Thisdesignaimsto
providebroadercoverageoverbothembodimentpatternsandinteractionscenarios. Second,tosupportawiderrangeof
practicalrobots,weextendthemodeltoanexpandedactionspacebeyondstandarddual-armplatforms,enablingcontrol
overthehead,waist,mobilebase,anddexteroushands. Thisexpandedcontrolinterfaceallowsthesystemtoaddress
morecomplextasksthatrequirecoordinatedwhole-bodyinteraction. Third,toimprovetemporalreasoningindynamic
environments,asshowninFig.1,weintroducepredictivedynamicsmodelingasaproxyobjective. Concretely,we
formulatefuturepredictionusingavideorepresentationmodeltoprovidesemanticpriorsandadepthestimationmodel
toprovidegeometriccues,encouragingtheVLAmodeltoreasonaboutfuturesceneevolutionandactionconsequences.
OurcentralhypothesisisthatpracticalVLAsystemsshouldnotonlyscaleinmodelanddatasize,butalsobecome
betteralignedwiththedemandsofreal-worldrobotics: broaderembodimentsupport,richercontrollableactionspaces,
andstrongerpredictiveunderstandingofdynamicscenes. Underthisview,LingBot-VLA 2.0isintendedasastep
fromfoundation-levelcapabilitytowardapplication-orientedusability.
We evaluate LingBot-VLA 2.0 in a generalist setting on nine tasks from the GM-100 dual-arm manipulation
benchmark [36], as well as on two long-horizon mobile manipulation tasks. The results show that the proposed
modificationsconsistentlyimprovepracticalcapability,validatingtheimportanceofjointlyenhancinggeneralization,
action-space coverage, and predictive dynamics modeling. Overall, our work highlights a pragmatic direction for
advancingVLAfoundationmodelsfromlaboratorysuccesstowardreal-worldapplicability.
2

DiverseRobotSource~50000hours Diverse Ego Source ~10000hours
Multi-Embodiment20 robot configuration
Astribot Leju KUAVO Galaxea Realman Galaxea
Qinglong AgiBotG1 AgileX ARXLift2 Franka
S1 4 Pro R1Pro Rs-02 R1Lite
Fourier Tien Unitree MagicBot AgiBot A2 Galbot G1 Moz1 Zerith H1 UR7e FLEXIV Rizon 4
GR-2 Kung G1 Gen1
Figure2. Visualizationofthepre-trainingdatasetusedbyLingBot-VLA-2.0.Thedatasetincludes20robotembodimentswith
degreesoffreedominthearms,heads,waists,mobilebases,anddexteroushands.
2 Related Work
2.1 Generalist Robot Manipulation Policies
Recentvision-language-action(VLA)models[4–8,10,14,30,32–34,39,41,42,47]haveestablishedfoundationVLA
modelasapromisingparadigmforgeneralistrobotcontrol. ExistingeffortshaveimprovedVLAsystemsalongseveral
complementarydirections,includingscalingheterogeneousrobotdataandunifiedpretrainingrecipesforgeneralization
acrosstasksandembodiments[34,43,46,47],leveraginghuman-centricdatasuchasegocentricvideosandhandmotion
tolearntransferableembodiedpriors[20–22],introducingembodiment-awarearchitecturesorunifiedactionspaces
tobettersupportcross-platformtransfer[18],andincorporatingpredictiveorworld-modelingobjectivestoimprove
temporalreasoningandfuture-awaredecisionmaking[11,23]. OtherworksfurtherenhanceVLAmodelsthrough
geometry-aware supervision [49], autoregressive reasoning-action unification [13], or deployment-oriented system
designforreal-worldexecution[15,47]. Together,thesestudiesdemonstratetherapidprogressoffoundationVLA
models,whilealsohighlightingthatpracticaldeploymentstillrequiresjointlyaddressinglarge-scalegeneralization,
richerembodiment,andaction-spacesupport.
3

Multi-View Misalignment
Pool
Valid Hand Frames <20%
Unstable SLAM / Abnormal Camera Motion
Trajectory Discontinuity / Abnormal Vel-Acc-Jerk
Non-egocentric / No Interaction / No Objects / Non-operator Hands
ataD
citoboR
ataD
cirtnecogE
High Quality
High Quality Robotic Data
Videos
Smooth ~ 50,000 Hours
Action& State
Video–State Misalignment
Videos with Blur/ Occlusions/Dropped Frames
Jerk > Threshold
Z-scoreof Vel/Acc > Threshold
Proportion of Static Signals > 95%
High Quality
Reconstructed & Egocentric Data
VLM-filtered Standardized ~ 10,000 Hours
Egocentric Hand Trajectories
Manipulation
Videos
Figure3. Dataprocessingpipeline.
2.2 Mixture-of-Experts Vision-Language-Action Model
Mixture-of-Experts(MoE)hasemergedasapivotalmechanismforscalingactionmodelingcapacityinVLAsystems.
For contact-rich manipulation, ForceVLA [45] and ForceVLA2 [17] introduce force-aware MoE modules to fuse
sparsebutcriticalforcefeedbackwithvisual-languagerepresentations,whileMoDE-VLA[29]furtherexploitsforce
andtactilesignalsfordexterousbimanualmanipulation. Forlong-horizontasks,AtomicVLA[48]structuresexperts
aroundatomicskillstomitigateinter-stageinterference,whileSAMoE-VLA[44]conditionsexpertroutingonscene-
level representations rather than token-level features alone. Other works [3, 12, 21] introduce MoE structures to
addresshumanoidbody-partandmotion-phasespecialization,andembodiment-levelheterogeneity. Inlarge-scaleVLA
pretraining, actionrepresentationsarejointlyshapedbymultipleentangledfactors, includingembodiment-specific
dynamics,task-dependentcontrollogic,anddeploymentscenariodiversity. Ratherthanprescribingexpertsemantics
based on any single dimension of variation, we instantiate token-level sparse MoE layers within the action expert,
enabling each action token to adaptively select experts based on its intrinsic features. Furthermore, we adopt an
auxiliary-loss-free load-balancing mechanism [19] that promotes balanced expert utilization via routing correction
biases,eliminatingtheneedtoinjectanexplicitload-balancinglossintotheprimaryactionlearningobjective.
3 Pre-training Dataset
ToimproveVLAmodelsforstronggeneralizationandpracticalityacrossdiverseembodimentsanddynamicenviron-
ments,weredesignthedataprocessingpipelineandcuratealarge-scalepretrainingdatasetofapproximately60,000
hours,asillustratedinFig.2. TheredesigneddataprocessingpipelineisshowninFig.3.
3.1 Data Curation and Pre-Processing
3.1.1 RoboticData
We collect approximately 90,000 hours of data from 20 embodiments, spanning single-arm, dual-arm, and mobile
roboticplatformsequippedwithdexteroushandsorgrippers. Basedonthecollecteddata,weemployaredesigneddata
processingpipelinetofilternoisysamples,yielding50,000hoursofhigh-qualityroboticdata.
Wefirstcomputethethird-orderfinitedifference(jerk)oftheactionandstatesignals,alongwiththeZ-scoresof
4

Table1. StatisticaloverviewofrobotmanipulationdatainLingBot-VLA-2.0.
RobotType EEtype Hand/GripperDoF ArmDoF BodyDoF∗ TotalDoF PolicyFrequency
Single-ArmRobots
| Franka       | Grppier | 1   | 7   | 0 8 | 30  |
| ------------ | ------- | --- | --- | --- | --- |
| FlexivRizon4 | Grppier | 1   | 7   | 0 8 | 30  |
Dual-ArmRobots
| AgileX   | Grppier | 2   | 12  | 0 14 | 30  |
| -------- | ------- | --- | --- | ---- | --- |
| ARXLift2 | Grppier | 2   | 12  | 0 14 | 30  |
| UR7e     | Grppier | 2   | 12  | 0 14 | 30  |
Half-Humanoid
| AgiBotG1      | Grppier | 2   | 14  | 4 20 | 30  |
| ------------- | ------- | --- | --- | ---- | --- |
| GalbotG1      | Grppier | 2   | 14  | 6 22 | 30  |
| Moz1          | Grppier | 2   | 14  | 0 16 | 30  |
| RealmanRs-02  | Grppier | 2   | 14  | 1 17 | 30  |
| GalaxeaR1Pro  | Grppier | 2   | 14  | 7 23 | 15  |
| GalaxeaR1Lite | Grppier | 2   | 12  | 3 17 | 15  |
| AstribotS1    | Grppier | 2   | 14  | 9 25 | 30  |
| ZerithH1      | Grppier | 2   | 14  | 7 23 | 30  |
Humanoid
| LejuKUAVO4Pro | Grppier/Hand | 2/12 | 14  | 5 21/31 | 30  |
| ------------- | ------------ | ---- | --- | ------- | --- |
| Tienkung      | Grppier      | 2    | 14  | 0 16    | 30  |
| QingLong      | Grppier      | 2    | 14  | 0 16    | 30  |
| MagicBotGen1  | Grppier      | 2    | 14  | 4 20    | 30  |
| UnitreeG1     | Hand         | 12   | 14  | 0 26    | 30  |
| FourierGR-2   | Hand         | 12   | 14  | 6 32    | 30  |
| AgiBotA2      | Hand         | 12   | 14  | 2 28    | 30  |
Humanoid
| Ego                 | -   | -   | 14  | - 14 | 30~60  |
| ------------------- | --- | --- | --- | ---- | ------ |
| Total:20embodiments |     |     |     |      | 60000h |
∗ThetotalnumberofbodyDoFusedformodeltraining.
theirfirst-orderderivatives(velocity)andsecond-orderderivatives(acceleration),toassesstrajectorysmoothness. An
episodeisdiscardedifeitherthejerkoranyderivativeZ-scoreexceedsapredefinedthreshold. Thesethresholdsareset
separatelyforeachembodiment. Moreover,wemeasurethedurationwithinanepisodeduringwhichallstateandaction
signalsexhibitonlysmallvariationsorremainunchanged. Ifthisdurationaccountsformorethan95%oftheentire
episode,theepisodeisalsodiscarded.
Toverifyconsistencybetweenthevideosandstatesignals,weprojecttherobotontotheimageplaneusingthe
correspondingURDFandreplaytherecordedstates. Humanannotatorsareemployedtoidentifydiscrepanciesbetween
theprojectedrobotandthevideostoensurethatthestatesignalsandvideosarecorrectlyrecorded,andsampleswith
suchmisalignmentareremoved. Meanwhile,videoswithblur,severeocclusions,droppedframes,ormisalignment
acrossmultipleviewsarefilteredoutbyhumanannotatorsduringtheannotationprocess.
3.1.2 EgocentricData
We construct an egocentric human video pool of approximately 20,000 hours and retain around 10,000 hours of
high-qualitytrainingdataafterfiltering,reconstruction,standardization,andqualitycontrol. Wefirstapplyaunified
video-levelVLMpre-filtertoallcandidatevideos,regardlessofsource. Thisstepremovesvideosthatdonotsatisfythe
egocentricmanipulationassumption,suchasthird-personobservationvideos,scene-walkingvideos,videoswithout
clearhand-objectinteraction, orvideoswithoutmanipulableobjects. Wealsofilteroutvideoswherenon-operator
handsappearprominently,sincesuchclipscanbreaktheassociationbetweenthecamerawearer’sobservationandthe
correspondinghandmotion. ApplyingthisVLMfilteringstagebeforedownstreamprocessingreducesunnecessary
annotationandreconstructioncost,especiallyforaction-freevideosthatwouldotherwiserequireSLAMandhandpose
5

ActionDimension Arm7D/6D EEF7D Gripper1D Waist4D Move3D Head2D Hand6D
7D 1D 6D 1D 6D 1D 7D 7D 2D 4D 3D 7D 1D 7D 1D 2D 7D 6D 7D 6D
Single-Arm Dual-Arm EGO Humanoid Dexterous Hand
Figure4. Unifiedactionrepresentation.Wemapheterogeneousembodimentcontrolsintocompactactionvectorscomposedof
sharedbody-partcomponents.
estimation.
AfterVLMpre-filtering,weprocesstheremainingdataaccordingtowhetheractionorhandtrajectorylabelsare
available. Fordatawithexistingactionorhandtrajectorylabels,includingaction-labeledopen-sourcedatasetsand
in-house data, we perform metadata organization, timestamp alignment, coordinate transformation, and trajectory
completenesschecking,convertingallsamplesintoastandardizedhandtrajectoryformat. Foraction-freeegocentric
humanvideos,werunegocentricSLAMtoestimatecameraintrinsicsandper-framecameraextrinsics,andthenapply
handposeestimationtorecoverMANOparametersinthecameracoordinateframe. Bycombiningtheestimatedhand
poseswithcameraposes,weliftthehandmotionintotheworldcoordinateframeandobtaintemporallycontinuous
handtrajectories.
Wethenapplytrajectory-levelqualitycontroltothereconstructedandstandardizeddata. Wefilteroutvideoswith
insufficientvalidhandposecoverage,usinga20%valid-frameratioastheminimumthreshold. Wealsoremoveclips
withunstableSLAMtrajectories,identifiedbyabnormalsecond-orderchangesintheestimatedcameramotion,such
assuddentranslationalorrotationalacceleration. Inaddition,werejecthandtrajectorieswithsuddendiscontinuities,
abnormaldisplacement,velocity,acceleration,orjerk,aswellassamplesthatviolatehumanphysiologicalconstraints,
suchasunreasonablehandpositions,inter-handdistances,motionranges,orposes.
Finally,allvalidsamplesarestoredashandtrajectoriesintheworldcoordinateframe. Duringtraining,whena
frameissampledasthecurrentobservation,wetransformthefuturehandtrajectoryfromtheworldcoordinateframe
intothecurrentcameracoordinateframeusingthecameraextrinsicofthatframe:
pCt =T pW. (1)
τ Ct←W τ
Here,pW denotesthehandtrajectoryintheworldcoordinateframe,andT denotesthetransformationfromthe
τ Ct←W
worldcoordinateframetothecameracoordinateframeofthesampledframet. Withthisdesign,theworldcoordinate
frameservesastheunifiedtrajectorystoragespace,whilethecurrentcameracoordinateframeservesasthetraining-time
actionrepresentation. Thisunifiestrajectoryformatsacrossopen-sourceandin-houseegocentrichumanvideos,and
decoupleshandmotionfromegocentriccameramotionduringtraining.
3.1.3 UnifiedActionRepresentation
To jointly learn state and action representations from egocentric data and robotic data collected across multiple
embodiments,weusea55-dimensionalcanonicalvectorrepresentationforbothstatesandactions. Thisrepresentation
consistsof14dimensionsforarmjointposition,14dimensionsforend-effectorpose,2dimensionsforgripperposition,
12dimensionsforhandjointposition,4dimensionsforwaistposition,2dimensionsforheadposition,and3dimensions
formobilitysignal,asshowninFig.4.Theremaining4dimensionsarereserved.Thearmjointpositionandend-effector
posefieldsaredefinedtoaccommodatethemaximumdimensionalityofadual-armembodiment. Specifically, the
end-effectorposeofeacharmisrepresentedbyXYZcoordinatesandarotationquaternion,resultingin7dimensionsper
arm. Forsingle-armdata,only6or7dimensionsareusedforarmjointpositionsand7dimensionsfortheend-effector
pose,whiletheremainingarm-relateddimensionsarepadded. Similarly,forrobotembodimentsthatdonotinclude
specificbodypartsorhavelower-dimensionalsignals,thecorrespondingdimensionsarealsopadded. Thedimensional
configurationsforeachembodimentareshowninTab.1.
6

Table2. Closedvocabularyforsubtaskannotation.Thevocabularyconsistsof15primitivemanipulationactionsandthreeauxiliary
labels:transitforempty-handmotion,idleforstationaryarms,andotherforout-of-vocabularyactions.
Action Description Action Description
Primitivemanipulationactions
move Relocateanobject fold Shrinkflexiblematerial
pour Tiltacontainertodispensecontents unfold Expandflexiblematerial
push Slideanunheldobject wipe Moveatoolacrossasurface
pull Drawanobjectcloser stir Moveatoolcircularlyinacontainer
rotate Turnanobjectinplace cut Severatargetwithablade
open Openahingedorarticulatedobject press Pressabutton,switch,orsurface
close Closeahingedorarticulatedobject attach Insertorconnectanobjecttoafitting
detach Removeordisconnectanobjectfromafitting
Auxiliarylabels
transit Movethegripperwithoutobjectinteraction idle Keepthearmsstationary
other Actionoutsidethevocabulary
3.2 Data Annotation
VLApretrainingbenefitsfrommanipulationvideospairedwithtemporallyalignedlanguagesupervisionatboththetask
andsubtasklevels. Wegeneratetheseannotationswithafullyautomatedpipelinebuiltonavision–languagemodel,and
applythispipelineacrossthepretrainingdataset.
Specifically, we employ Qwen3.6-27B [25] to segment each manipulation video into a sequence of temporally
contiguous subtasks and to generate the corresponding language instructions. For robotic platforms with multiple
cameras,theoverheadandwristviewsareprocessedjointlytodisambiguategripper–objectinteractions. Eachsubtask
isassignedanatomicactionfromaclosedvocabularyof18categories(Tab.2),togetherwiththeprimaryobjectof
interactionandaconciseinstruction. Inaddition,asinglevideo-levelinstructionsummarizestheoveralltask. The
annotatedobjectsformadiverse,openvocabulary,asvisualizedinFig.6.
Tokeepthesegmentationgranularityconsistent,themodelgroupsthegrasp,carry,andreleasephasesofasingle
interactionintoonesubtask,andintroducesatemporalboundaryonlywhenthemanipulatedobjectchanges,theaction
typechanges,orasustainedpausemarksatransitiontoanewsub-goal. AssummarizedinFig.5,moveandtransit
dominateinfrequency,whereasfine-grainedmanipulationssuchascut,fold,andstirarerarebuthaveconsiderably
longermeandurations.
4 Method
4.1 MoE-based VLA model
Vision-Language-Action(VLA)modelspretrainedonreal-worldcross-embodimentrobotdatamustlearnfromhetero-
geneoustrajectoriescharacterizedbymisalignedactionspaces,varyingembodimentdynamics,andtaskdistributions.
AlthoughtheMixture-of-Experts(MoE)mechanismprovidesanaturalwaytoscalemodelcapacity,theunderlying
reasonsforitseffectivenessinVLApretrainingremainpoorlyunderstood. Inthisreport,weintroduceatoken-level
loss-freeMoEarchitectureforlarge-scalemulti-embodimentVLApretraining. Bydecouplingexpertloadbalancing
fromtheprimaryaction-learningobjective,andemployingsigmoid-basedroutingconfidencetoalloweachtokento
independentlyactivatemultipleexperts,ourdesignenablessparseexpertstocapturegeneralrepresentationsandcontrol
logicsharedacrossembodiments.
SparseMoEArchitecture. Tofacilitateconvergenceduringcross-embodimentpretraining,weinstantiatesparse
MoElayersinsidetheactionexpert,whichreplacethefeed-forwardnetwork(FFN)intheactionexpert. Inourdefault
configuration,allaction-experttransformerblocksareequippedwithMoEFFNs. Furthermore,weadoptfine-grained
expertsegmentationandsharedexpertisolation,inwhichalightweightsharedexpertpreservesuniversalpriors,whilea
setofroutedexpertsprovidesspecializedmodelingcapacity.
7

subtask duration: <2s 2–5s 5–10s 10–20s >20s frequency total time mean duration
| move   |     |     |     |     |     |     |       | 46.21% |      | 58.2% |     | 10.4s |       |
| ------ | --- | --- | --- | --- | --- | --- | ----- | ------ | ---- | ----- | --- | ----- | ----- |
| close  |     |     |     |     |     |     | 2.12% |        | 2.1% |       |     | 8.1s  |       |
| attach |     |     |     |     |     |     | 1.52% |        | 1.9% |       |     | 10.2s |       |
| fold   |     |     |     |     |     |     | 1.28% |        | 5.0% |       |     |       | 32.4s |
| open   |     |     |     |     |     |     | 1.23% |        | 1.8% |       |     | 12.1s |       |
| wipe   |     |     |     |     |     |     | 1.00% |        | 2.6% |       |     | 21.1s |       |
noitalupinaM
| pour   |     |     |     |     |     |       | 0.98% |     | 1.6% |     |     | 13.4s |       |
| ------ | --- | --- | --- | --- | --- | ----- | ----- | --- | ---- | --- | --- | ----- | ----- |
| push   |     |     |     |     |     |       | 0.81% |     | 0.7% |     |     | 7.6s  |       |
| pull   |     |     |     |     |     |       | 0.51% |     | 0.6% |     |     | 9.9s  |       |
| press  |     |     |     |     |     |       | 0.51% |     | 0.4% |     |     | 6.6s  |       |
| rotate |     |     |     |     |     |       | 0.47% |     | 0.7% |     |     | 11.8s |       |
| unfold |     |     |     |     |     |       | 0.32% |     | 1.0% |     |     |       | 26.8s |
| detach |     |     |     |     |     | 0.11% |       |     | 0.1% |     |     | 10.9s |       |
| stir   |     |     |     |     |     | 0.07% |       |     | 0.2% |     |     | 21.5s |       |
| cut    |     |     |     |     |     | 0.03% |       |     | 0.1% |     |     |       | 35.6s |
yrailixuA
| transit |     |     |     |     |     |     |       | 42.48% | 22.1% |     | 4.3s |       |     |
| ------- | --- | --- | --- | --- | --- | --- | ----- | ------ | ----- | --- | ---- | ----- | --- |
| other   |     |     |     |     |     |     | 0.33% |        | 0.7%  |     |      | 18.7s |     |
| 0       | 20  |     | 40  | 60  | 80  | 100 |       |        |       |     |      |       |     |
duration composition (%)
Figure5. Per-actionstatisticsofthesubtaskannotations: durationcomposition,frequency(fractionofallsubtasks),totaltime
(fractionofthetotalannotatedtime),andmeanduration.ActionsaregroupedasinTab.2;idleisfilteredoutofthetrainingdataand
omittedhere.
cup
box
parw elbbub pen tube sponge water basket box lid cabinet door bottle baby bottle avocado refrigerator door sausage mooncake container and can spool crushed can nesting doll package beige t-shirt container lid pepsi bottle drawer knob sneaker notebook
cucumber carafe aa battery stove knob sweater pen cap milk carton ebut tset rectangular box carton plush t-shirt coffee pot retpada rewop elttob eulg redloh yrettab
|     |     | diamond block mouse | glasses beige cup |     | fruit |     | kcolb ralugnatcer |     | toothbrush |     |     |     |     |
| --- | --- | ------------------- | ----------------- | --- | ----- | --- | ----------------- | --- | ---------- | --- | --- | --- | --- |
pumpkin jeans nac gniretaw rood enihcam gnihsaw lebal htiw elttob dumbbell peeler banana plate slipper stick structure gift box lewot card reliam elbbub pilc rednib snack bagconnector duvet and medicine box rice cooker lid
lacirdnilyc ebuc strohs mined teehs parw elbbub bun toy car hair dryer soda bottle slippers gift bag pliers snack packet tool pirts rewop kcolb rednilyc erusaem epat kettle ring block ram stick stapler circuit board
pac elttob kcolc latigid coffee capsule jar spice jar laptop soda can toilet seat cross-shaped block stick weight eldal table kcolb nogaxeh
|     |     |     | electronic | and box plush toy | bead case tape roll beige notebook | mango |     | rekaerb tiucric | shirt battery pack |     | cap |     |     |
| --- | --- | --- | ---------- | ----------------- | ---------------------------------- | ----- | --- | --------------- | ------------------ | --- | --- | --- | --- |
bo ecils taem enohptrams ttl bolt billiard ball tablecloth e folder duck toilet lid keychain mug teapot lettuce leaf lid chip bag
|     |     | nut | and cylindrical | decanter | reppep ilihc | cupcake |     |     | bcoylinwder battery |     | whiteboard scissors | hammer lamp |     |
| --- | --- | --- | --------------- | -------- | ------------ | ------- | --- | --- | ------------------- | --- | ------------------- | ----------- | --- |
apple wrapped paintbrush foil ball flower lettuce pear sock gear napkin rose reppep lleb yttap taem kcap eussit t dustpan ool   casemarker pepper cross block button tissue brush esac licnep pencil door l pants revirdwercs cirtcele
|     |     | umbrella garment | psotaumchp shorts | esac sessalg | eggplant |     | cabinet |     | letter toy figure |     | highlighter spatula |     |     |
| --- | --- | ---------------- | ----------------- | ------------ | -------- | --- | ------- | --- | ----------------- | --- | ------------------- | --- | --- |
hexagonal block faucet egg scanner drill case hanger pac rekram diuqil htiw retnaced bag corn desk lamp backpack wrapper microwave door
rotaregirfer cable bundle potato pac htiw elttob tomato beige bowl pillow somreht microwave triangular block cardboard box spoon ylbmessa elbac ebut etsaphtoot
esac licnep egieb marble chess lortnoc etomer meat ebuc s'kibur sphere drill pot lid and strohs egieb cable kcolb depahs-l draob gnittuc ralugnatcer
nap gniyrf elttob yarps daerb fo ecils ecils eseehc skcitspohc screw kcocelttuhs capsule tray elttob deppac-egnaro radish bracket staple strip onion can medicine box scoop tnalp dettop elbac tenrehte elttob tnegreted
|     | kcolb nogatnep |     | straw figurine nobbir htiw xob tfig | eraser | cup with band remote         | carrot |     | pitcher chili beige pitcher |                 | revoc yrettab | leaf       |     |     |
| --- | -------------- | --- | ----------------------------------- | ------ | ---------------------------- | ------ | --- | --------------------------- | --------------- | ------------- | ---------- | --- | --- |
|     |                |     | toy bus toy                         | lemon  | tea bottle headphones packet |        |     | glue stick                  | padded envelope |               | bin insert |     |     |
vase eohs toy truck beige curtain cabinet drawer donut semi-circle block screwdriver fork sauce bottle book kettle lid steamer lid corn cob plug
bread tissue box thread spool pot knife bread slice envelope tennis ball triangle block label water bottle semi-circle
Figure6. Wordcloudofthemanipulatedobjectsinthesubtaskannotations,sizedbyfrequency.
∈Rdoftokentatlayerℓ,theMoElayercomputes
| GiventhemodulatedFFNinputu |     |     | ℓ,t |     |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
|     |     |     | m (u  | )=E(s)(u | )+λ |     | g (u | )E(r)(u | ),  |     |     |     | (2) |
| --- | --- | --- | ----- | -------- | --- | --- | ---- | ------- | --- | --- | --- | --- | --- |
|     |     |     | ℓ ℓ,t | ℓ        | ℓ,t |     | ℓ,j  | ℓ,t ℓ,j | ℓ,t |     |     |     |     |
j∈R(uℓ,t)
whereE(s)(·)denotesthesharedexpert,E(r)(·)denotesthej-throutedexpert,R(u
|     |     |     |     |     |     |     |     |     |     | )istheselectedtop-K |     |     | routed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | ------ |
| ℓ   |     |     |     | ℓ,j |     |     |     |     | ℓ,t |                     |     |     |        |
expertset,andλisarouted-outputscalingfactor. EachsharedorroutedexpertisimplementedasaSwiGLUMLP:
|     |     |     | E(u)=W |     | down (SiLU(W | gate | u)⊙W | up u). |     |     |     |     | (3) |
| --- | --- | --- | ------ | --- | ------------ | ---- | ---- | ------ | --- | --- | --- | --- | --- |
ComparedwiththedenseFFNcounterpart,boththesharedandroutedexpertsemployasmallerintermediatewidth,
encouraging shared experts to capture general principles and routed experts to provide stronger specialization. In
practice,weuseonesharedexpertandN r routedexpertsperMoElayer;onlyK routedexpertsareactivatedforeach
token. Fortoken-choicerouting,wecomputerouterlogitswithalinearrouterinFP32:
|     |     |     |     |     | z (u    | )=u⊤e | ,   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | ℓ,j ℓ,t | ℓ,t   | ℓ,j |     |     |     |     |     | (4) |
8

wheree ℓ,j isthelearnablerouterembeddingofthej-throutedexpert. Toavoidthestrongcompetitionamongexperts
inducedbysoftmaxnormalization, weapplyasigmoid-activatedfunctiontotherouterlogitsfollowingDeepSeek-
V3[19],thetoken-to-expertaffinityisdefinedas
|     |     |     | s (u )=Sigmoid(z |     | (u )).  |     |     | (5) |
| --- | --- | --- | ---------------- | --- | ------- | --- | --- | --- |
|     |     |     | ℓ,j ℓ,t          |     | ℓ,j ℓ,t |     |     |     |
TopreservetheprimaryobjectiveofactioncontrollearninginVLAmodels,weadoptanauxiliary-loss-freestrategy
inspired by DeepSeek-V3 [19] to promote load balancing within the MoE architecture. Under auxiliary-loss-free
balancing,eachexpertmaintainsaroutingcorrectionbiasb . Theactualmixtureweightsarestillcomputedfromthe
ℓ,j
originalunbiasedaffinities:
s (u )
ℓ,j ℓ,t
|     |     | g   | ℓ,j (u ℓ,t )= (cid:80) |      | , j ∈R(u | ℓ,t ), |     | (6) |
| --- | --- | --- | ---------------------- | ---- | -------- | ------ | --- | --- |
|     |     |     |                        | s (u | )        |        |     |     |
k∈R(uℓ,t) ℓ,k ℓ,t
whiletheselectedroutedexpertsetisdeterminedbybiasedaffinities:
|     |     |     | R(u )=TopK | (s (u | )+b ,K). |     |     | (7) |
| --- | --- | --- | ---------- | ----- | -------- | --- | --- | --- |
|     |     |     | ℓ,t        | j ℓ,j | ℓ,t ℓ,j  |     |     |     |
Thisbias-basedbalancingmechanismdecouplesexpertassignmentfromexpertrouting. Specifically,thecorrectionbias
isemployedtopromoteloadbalancing,whiletheroutingconfidenceremainsweightedbythemodel’soriginal,unbiased
affinityscores. Duringtraining,weaccumulatethenumberoftokensassignedtoeachexpertacrossmicro-batchesand
distributedranks. Ateachload-balancingupdate,thecorrectionbiasisadjustedaccordingtothesignofthedeviation
fromthemeanexpertload:
|     |     |     |     | (cid:32) |     | (cid:33) |     |     |
| --- | --- | --- | --- | -------- | --- | -------- | --- | --- |
1 Nr
(cid:88)
|     |     |     | b ℓ,j ←b ℓ,j −γ·sign | n ℓ,j | − n ℓ,k | ,   |     | (8) |
| --- | --- | --- | -------------------- | ----- | ------- | --- | --- | --- |
N
r k=1
wheren ℓ,j istheaccumulatedloadofexpertj inlayerℓ,andγ isthebiasupdatespeed. Optionally,thebiasvectoris
centeredaftereachupdatetopreventcumulativedrift. TheMoEoutputistheninjectedbackthroughtheoriginalFFN
residualbranchoftheactionexperttransformer.
Scaling Experiments. To validate the efficacy of the sparse architecture under an identical compute budget, we
conductacomprehensivecomparisonbetweenMoEandDensemodelswithstrictlymatchedactiveparametercounts.
ExperimentalresultsshowninFig.7indicatethatMoEconsistentlyachieveslowertraininglossandvalidationerror
thanitsdensecounterpart. Thisadvantageisobservedacrossbothoptimizationandgeneralizationmetrics,indicating
thattheperformancegainofMoEdoesnotmerelyarisefromincreasedtotalparametercount,butfromamoreeffective
allocationofmodelcapacitythroughsparseactivation. Theseresultsdemonstratethat,underafixedcomputebudget,
thesparseMoEarchitectureachievesmoreefficientscalingwithreducedtraininglossandvalidationerror,establishing
itasamoreeffectivescalingstrategyforVLApre-training.
7×102
|     |     |     | Dense 0.6B |     |     |     | Dense 0.6B |     |
| --- | --- | --- | ---------- | --- | --- | --- | ---------- | --- |
0.16
|                                 |     |     | MoE 1.6B-A-0.6B |     |                         |     | MoE 1.6B-A-0.6B |     |
| ------------------------------- | --- | --- | --------------- | --- | ----------------------- | --- | --------------- | --- |
| )elacs gol( ssol gniniarT 6×102 |     |     |                 |     | rorre noitca noitadilaV |     |                 |     |
0.14
5×102
0.12
0.10
4×102
0.08
|     | 10 15 20 | 25 30             | 35 40 45 | 50  | 10 15 | 20 25 30 35       | 40 45 | 50  |
| --- | -------- | ----------------- | -------- | --- | ----- | ----------------- | ----- | --- |
|     |          | Training step (k) |          |     |       | Training step (k) |       |     |
Figure7.Comparableactive-parameterscalingcomparisonbetweenDensemodelandMoEmodelusingtraininglossonpre-training
dataandvalidationactionerroronGM-100tasks.
| 4.2 | Spatiotemporal-Aware |     | VLA via | Dual-Query | Distillation |     |     |     |
| --- | -------------------- | --- | ------- | ---------- | ------------ | --- | --- | --- |
TopromotebothgeometricawarenessandcausaltemporalunderstandingintheLingBot-VLA 2.0,weadoptadual-
querydistillationframeworkinspiredbyrecentworks[35],whereLingBot-Depthandourrobotics-awareDINO-Video
9

serveascomplementaryteachers. Specifically,weappendtwolearnablequeries,[Q t ,Q t+T ],tothevisualandtextual
tokens,whereQ targetsthecurrentobservationandQ targetsthefutureobservationathorizonT (i.e.,theaction
|     | t   |     |     |     | t+T |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
chunksize). Thesecontextualizedquerystatesarethendistilledfromtwocomplementaryteachers: adepthteacher,
LingBot-Depth[28],whichprovidesexplicitgeometricsupervision,andacausalvideoteacher,DINO-Video,which
providestemporallygroundedvisualrepresentations.
LingBot-Depthforgeometricsupervision. ToinjectexplicitspatialandgeometricpriorsintoLingBot-VLA 2.0,
wealignthedual-querystateswithdepthtokensextractedfromLingBot-Depth. Specifically,thecurrentandfuture
queries,[Q ,Q ],aretrainedtopredictthecorrespondingdepthrepresentations[D ,D ]fromthecurrentand
| t                                      | t+T |                   |                                 |     |          |          |     |     | t t+T     |     |     |
| -------------------------------------- | --- | ----------------- | ------------------------------- | --- | -------- | -------- | --- | --- | --------- | --- | --- |
| futuremanipulationframes,respectively. |     |                   | Thedepthdistillationobjectiveis |     |          |          |     |     |           |     |     |
|                                        |     | (cid:104)(cid:13) |                                 |     |          |          |     |     | (cid:105) |     |     |
|                                        |     | =E                |                                 |     | (cid:13) | (cid:13) |     |     | (cid:13)  |     |     |
L (cid:13)Proj (Q )−D (cid:13) + (cid:13)Proj (Q )−D (cid:13) , (9)
|     | depth |     | depth | t   | t   | 1   | depth t+T |     | t+T 1 |     |     |
| --- | ----- | --- | ----- | --- | --- | --- | --------- | --- | ----- | --- | --- |
whereProj (·)denotesaprojectionmodulewithcross-attentionfordimensionalalignment. WithinthecausalVLM
depth
architecture,Q capturestheimmediatescenegeometry,whileQ learnstoanticipatefuturegeometricconfigurations
| t   |     |     |     |     |     | t+T |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
relevanttoupcomingmanipulation.
Causal DINO-Video for temporal supervision. While depth supervision provides geometric structure, it does
not capture the causal temporal dynamics required for robotic control. Motivated by the success of latent visual
representationsacrossabroadrangeofactionandroboticsapplications[9,11,22–24,27],weintroduceDINO-Video,
arobotics-awarevideorepresentationmodelbuiltontopoftheDINOv3[26]imagebackbone. Unlikeimage-level
featuresextractedindependentlyforeachframe,DINO-Videoproducesmotion-awarevisualrepresentationswithcausal
temporalattention,suchthatthefeatureateachtimestepdependsonlyonthecurrentandpastobservations. Giventhe
contextualizedquerystates[Q ,Q ],thecurrentqueryistrainedtopredicttheDINO-Videofeatureofthecurrent
t t+T
frame,whilethefuturequeryistrainedtopredictthefeatureofthefutureframeathorizonT. Denotingtheteacher
targetsby[Z ,Z ],extractedfromasinglecausalforwardpassofDINO-Videooverthecorrespondingobservation
| t   | t+T |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
clip,thevideodistillationobjectiveis
|     |         | (cid:104) |       |          |     |        |        |     | (cid:105) |     |      |
| --- | ------- | --------- | ----- | -------- | --- | ------ | ------ | --- | --------- | --- | ---- |
|     |         | =E        |       |          | ∥2  |        |        |     | ∥2        |     |      |
|     | L video | ∥Proj     |       | (Q t )−Z | t   | +∥Proj | (Q t+T | )−Z | t+T ,     |     | (10) |
|     |         |           | video |          | F   |        | video  |     | F         |     |      |
whereProj (·)mapsthequerystatesintothepatch-levelfeaturespaceofDINO-Video. Thisobjectiveencourages
video
LingBot-VLA 2.0torecoverboththecurrentmotion-awarerepresentationanditsfuturecounterpart,complementing
thegeometricsupervisionfromdepthdistillation.
Details of robotics-aware DINO-Video. We initialize DINO-Video from DINOv3 and extend it with block-wise
causaltemporalattentionand3Drotarypositionalembeddings(3D-RoPE)[37],enablingcausalvideomodelingwhile
preservingthespatialsemanticsandgeometrypriorsinheritedfromDINOv3. WetrainDINO-Videoon5Mvideoclips
spanningInternet,egocentric,androboticdata,usingvideo-adaptedDINOandiBOTself-distillationobjectives[40].
Foreachsample,weuniformlysample16framesandassignanabsolutetemporalencodingbasedontheeffectiveframe
ratetodistinguishclipswithdifferentreal-timespans[1]. OnLARYBench[24](seeTab.3),DINO-Videoachievesthe
bestperformanceonthreeoffourbenchmarks,supportingitseffectivenessasarobotics-awaretemporalteacher.
Table3. ResultsofDINO-VideoonLARYBenchClassificationandRegressionEvaluation.
|       |           |                 |     | Classification |                 |     |     |           | Regression        |     |     |
| ----- | --------- | --------------- | --- | -------------- | --------------- | --- | --- | --------- | ----------------- | --- | --- |
| Model | Params(M) |                 |     |                |                 |     |     |           |                   |     |     |
|       |           | CompositeHuman↑ |     |                | CompositeRobot↑ |     |     | RoboCOIN↓ | AgiBotWorld-Beta↓ |     |     |
80.35
| V-JEPA2[2] | 303.89 |     |       |     |     | 70.43 |     | 0.32 |     | 0.33 |     |
| ---------- | ------ | --- | ----- | --- | --- | ----- | --- | ---- | --- | ---- | --- |
| DINOv3[26] | 303.13 |     | 76.19 |     |     | 69.06 |     | 0.22 |     | 0.24 |     |
| DINO-Video | 303.13 |     | 80.21 |     |     | 71.97 |     | 0.20 |     | 0.19 |     |
10

Table4. ScoringcriteriaforthepartofGM-100benchmarktasks.
TaskID Task ScoringCriteria
1.Pickupthelargestblockonthetable(16).
2.Placethelargestblockonthefarleft(12).
3.Pickupthesecond-largestblockonthetable(12).
4.Placethesecond-largestblocktotherightofthelargestblock(12).
BM-19 BlockSorting
5.Pickupthethird-largestblockonthetable(12).
6.Placethethird-largestblocktotherightofthesecond-largestblock(12).
7.Pickupthesmallestblockonthetable(12).
8.Placethesmallestblockonthefarright(12).
1.Pullopenthedrawer(25).
2.Graspthekeychain(25).
BM-20 RetrieveKeychain
3.Movethekeychaintothefrontofthedrawer(25).
4.Putdownthekeychain(25).
1.Pickupthespoonwiththerighthand(20).
2.Scoopricefromthebowlwiththespoon(30).
BM-25 ScoopRice
3.Pourthericeintothecup(30).
4.Placethespoonbackontotheplate(20).
1.Removetheemptypaper-rollcore(22).
2.Placethecoreonthetray(22).
BM-39 ReplacePaperRoll
3.Pickupthenewpaperroll(22).
4.Installthenewpaperrollontotheholder(34).
1.Pickupthefirsttypeofsnack(18).
2.Placeitintothecorrespondingcontainer(16).
3.Pickupthesecondtypeofsnack(17).
BM-45 SortSnacks
4.Placeitintothecorrespondingcontainer(16).
5.Pickupthethirdtypeofsnack(17).
6.Placeitintothecorrespondingcontainer(16).
1.Pickupthefirstegg(16).
2.Placetheeggintoatrayslot(12).
3.Pickupthesecondegg(12).
4.Placetheeggintoatrayslot(12).
BM-47 PackEggs
5.Pickupthethirdegg(12).
6.Placetheeggintoatrayslot(12).
7.Pickupthefourthegg(12).
8.Placetheeggintoatrayslot(12).
1.Pickupthefirsttoybone(25).
2.Movetheboneoutoftheplate(25).
BM-69 PickOutToyBones
3.Pickupthesecondtoybone(25).
4.Movetheboneoutoftheplate(25).
1.Pushtheballtowardthebox(30).
BM-75 PushBallintoBox
2.Pushtheballintothebox(70).
1.Pickuptheketchupbottlewiththelefthandandholditabovetheplate(25).
2.Tiltthebottlesothatthenozzlepointstowardtheplate(25).
BM-82 SqueezeKetchup
3.Squeezethebottlewithbothhandstodispenseketchup(25).
4.Putdowntheketchupbottle(25).
1.Openthemicrowavedoor(25).
2.Graspthebowlinsidethemicrowave(25).
BM-97 TakeBowloutofMicrowave
3.Movethebowlontothetableandplaceitdown(25).
4.Closethemicrowavedoor(25).
1.Pickupthetapeandplaceitintothetoolbox(20).
2.Pickupthemeasuringtapeandplaceitintothetoolbox(20).
BM-105 ToolPacking 3.Pickupthescrewdriverandplaceitintothetoolbox(20).
4.Pickupthecutterandplaceitintothetoolbox(20).
5.Closethetoolbox(20).
1.Liftthemedicineboxandholditupwiththelefthand(20).
2.Pickupthebarcodescannerwiththerighthand(20).
BM-107 BarcodeScan 3.Scanthebarcodeonthemedicineboxwiththescanner(20).
4.Putdownthebarcodescanner(20).
5.Putthemedicineboxbackdown(20).
5 Experiments
5.1 Experimental Settings
Scoring criteria. Table 4 summarizes the scoring criteria for a subset of GM-100 benchmark tasks. Each task is
decomposedintoasequenceoffine-grainedmanipulationsteps,andapartialscoreisassignedtoeachstepaccordingto
11

taskcompletion. Thesecriteriacoverdiversebimanualcapabilities,includingsorting,retrieval,scooping,replacement,
packing,pushing,squeezing,andcoordinatedobjecthandling. Suchstepwiseannotationsenableamorefine-grained
evaluationthanbinarysuccessalone,capturingpartialprogressonlong-horizonmanipulationtasks.
| 5.2 Bimanual | Manipulation | Experiment | Results |     |     |     |
| ------------ | ------------ | ---------- | ------- | --- | --- | --- |
Table5. PerformanceonthebimanualGM-100benchmarkunderthegeneralistsetting.Wereportprogressscore(Prog.,%)and
successrate(Succ.,%)foreachtask.Theshadedrowineachplatformblockreportstheaverageovertheninetasks.
|     |      | GR00TN1.7   | π           | LingBot-VLA-1.0 | LingBot-VLA-2.0 |       |
| --- | ---- | ----------- | ----------- | --------------- | --------------- | ----- |
|     | Task |             | 0.5         |                 |                 |       |
|     |      | Prog. Succ. | Prog. Succ. | Prog.           | Succ. Prog.     | Succ. |
AgilexCobotMagic
|     | Overallaverage         | 36.3 17.8 | 59.1 32.2     | 58.2     | 30.0 66.2  | 34.4  |
| --- | ---------------------- | --------- | ------------- | -------- | ---------- | ----- |
|     | Blocksorting           | 40.0 10.0 | 90.4 60.0     | 59.2     | 10.0 56.8  | 0.0   |
|     | Retrievekeychain       | 12.5 10.0 | 20.0 20.0     | 67.5     | 60.0 100.0 | 100.0 |
|     | Replacepaperroll       | 52.8      | 0.0 62.8 10.0 | 59.6     | 20.0 55.2  | 20.0  |
|     | Sortsnacks             | 91.9 70.0 | 82.4 30.0     | 74.4     | 10.0 66.2  | 10.0  |
|     | Packeggs               | 14.4      | 0.0 72.4 20.0 | 42.4     | 10.0 44.4  | 0.0   |
|     | Pickouttoybone         | 70.0 60.0 | 100.0 100.0   | 77.5     | 70.0 95.0  | 90.0  |
|     | Pushballintobox        | 18.0      | 0.0 38.0 20.0 | 6.0      | 0.0 41.0   | 20.0  |
|     | Takebowloutofmicrowave | 15.0 10.0 | 0.0           | 0.0 77.5 | 70.0 77.5  | 70.0  |
|     | Toolpacking            | 12.0      | 0.0 66.0 30.0 | 60.0     | 20.0 60.0  | 0.0   |
GalaxeaR1Pro
|     | Overallaverage         | 16.4      | 5.6 27.4      | 8.9 32.7 | 15.6 34.6  | 15.6 |
| --- | ---------------------- | --------- | ------------- | -------- | ---------- | ---- |
|     | Blocksorting           | 8.4       | 0.0 12.4      | 0.0 28.0 | 0.0 33.2   | 0.0  |
|     | Retrievekeychain       | 0.0       | 0.0 0.0       | 0.0 0.0  | 0.0 0.0    | 0.0  |
|     | Replacepaperroll       | 6.6       | 0.0 72.0 50.0 | 44.0     | 0.0 57.6   | 40.0 |
|     | Sortsnacks             | 31.3      | 0.0 28.1      | 0.0 10.6 | 0.0 26.1   | 0.0  |
|     | Packeggs               | 1.6       | 0.0 6.7       | 0.0 19.2 | 0.0 4.4    | 0.0  |
|     | Pickouttoybone         | 77.5 50.0 | 72.5 30.0     | 62.5     | 40.0 87.5  | 70.0 |
|     | Pushballintobox        | 9.0       | 0.0 21.0      | 0.0 3.0  | 0.0 18.0   | 0.0  |
|     | Takebowloutofmicrowave | 7.5       | 0.0 7.5       | 0.0 97.5 | 100.0 65.0 | 30.0 |
|     | Toolpacking            | 6.0       | 0.0 26.0      | 0.0 30.0 | 0.0 20.0   | 0.0  |
Experimentsettings. WeevaluatebimanualmanipulationonninetasksfromtheGM-100benchmarkunderageneralist
mixed-trainingsetting. Unliketask-specifictraining,asinglepolicyisjointlytrainedonalltasksforeachembodiment,
requiringthemodeltosharemanipulationprimitivesacrossdiversebimanualskills,includingsorting,retrieval,packing,
pushing,andarticulated-objectinteraction. Wereporttheprogressscoreandsuccessrateforeachtask.
Resultsanalysis. AsshowninTab.5,LingBot-VLA-2.0achievesthebestoverallperformanceunderthegeneralist
setting. OnAgilexCobotMagic,itreaches66.2/34.4inprogressscore/successrate,surpassingLingBot-VLA-1.0
by8.0/4.4pointsandπ by7.1/2.2points. OnGalaxeaR1Pro,itachieves34.6/15.6,outperformingπ by7.2
0.5 0.5
/6.7points. TheseresultsdemonstratethatLingBot-VLA-2.0benefitsfrommixed-tasktrainingandacquiresmore
generalizablebimanualmanipulationbehaviors.
Theimprovementsaremostpronouncedontasksthatdemandaccurateobjectgroundingandgoal-directedaction
Forinstance,onAgilexRetrievekeychain,LingBot-VLA-2.0improvesoverLingBot-VLA-1.0from67.5
execution.
/60.0to100.0/100.0,andonAgilexPickouttoybone,from77.5/70.0to95.0/90.0. Asimilargainisobserved
on the Galaxea Pick out toy bone task, where the performance increases from 62.5 / 40.0 to 87.5 / 70.0. These
improvementsalignwellwiththedesignofLingBot-VLA-2.0,whichadoptsastrongerVLMbackbonewithenhanced
groundingcapabilityandconditionsactionpredictiononfutureinformation,togetherenablingmoreobject-centricand
goal-consistentmanipulation.
Nevertheless,thegainsarenotuniformacrosstasks. Severaltasksstillexhibitasubstantialgapbetweenprogress
12

|     |     | lingbot-vla 2.0 ID |     | π0.5 ID | lingbot-vla 2.0 OOD |     |     | π0.5 OOD |     |     |
| --- | --- | ------------------ | --- | ------- | ------------------- | --- | --- | -------- | --- | --- |
Astribot S1 (task1)
100
)%( erocS ksatbuS naeM
80
60
40
20
0
|     | 1   | 2 3 | 4   | 5   | 6   | 7   | 8   | 9   | 10 11 | Avg. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ---- |
Subtask
Cobot Magic-ARX X5 (task2)
100
)%( erocS ksatbuS naeM
80
60
40
20
0
|     | 1   | 2   | 3   |     | 4   | 5   |     | 6   | 7   | Avg. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
Subtask
Figure8. Per-subtaskperformanceonthelong-horizonmobilemanipulationbenchmark.Barsreportthemeansubtaskcompletion
score(%)across15trialsunderbothin-domain(ID)andout-of-distribution(OOD)settings.
scoreandsuccessrate,indicatingthatthemodeloftenmakespartialprogressbutfailsatthefinalpreciseplacement,
release, or completion step. Moreover, the performance disparity between Agilex Cobot Magic and Galaxea R1
Prosuggeststhatembodiment-specificfactors,suchaskinematics,cameraviewpoints,andaction-spacealignment,
remainchallenging. Overall,LingBot-VLA-2.0deliversconsistentimprovementsingeneralistbimanualmanipulation,
particularlyontasksrequiringstrongvisualgroundingandfuture-awareactionplanning.
| 5.3 Long-Horizon |     | Mobile | Manipulation |     | Experiment |     | Results |     |     |     |
| ---------------- | --- | ------ | ------------ | --- | ---------- | --- | ------- | --- | --- | --- |
Table6. Long-horizonmobilemanipulationbenchmarkresults,reportedasprogressscore/successrate(%).
| Embodiment |     | Task |     |     |     | Setting |     | LingBot-VLA-2.0 |     | π   |
| ---------- | --- | ---- | --- | --- | --- | ------- | --- | --------------- | --- | --- |
0.5
|                  |     |                             |     |     |     | In-domain           |     | 77.1/60.0 |     | 65.3/46.7 |
| ---------------- | --- | --------------------------- | --- | --- | --- | ------------------- | --- | --------- | --- | --------- |
| AstribotS1       |     | Sortobjectsintorefrigerator |     |     |     |                     |     |           |     |           |
|                  |     |                             |     |     |     | Out-of-distribution |     | 37.0/13.3 |     | 30.3/6.7  |
|                  |     |                             |     |     |     | In-domain           |     | 84.3/66.7 |     | 79.9/60.0 |
| CobotMagic-ARXX5 |     | Stovecleaning               |     |     |     |                     |     |           |     |           |
|                  |     |                             |     |     |     | Out-of-distribution |     | 67.5/40.0 |     | 62.5/33.3 |
Experimentsettings. Weevaluatelong-horizonmobilemanipulationperformanceontworoboticembodiments,as
illustratedin Fig.9. Eachembodimentisassociatedwithonerepresentativetask: AstribotS1isevaluatedontheobject
sortingtask,whereobjectsarecollectedandplacedintoarefrigerator,whileCobotMagic-ARXX5isevaluatedonthe
stovecleaningtask. Thedetailedsub-taskdecompositionandcorrespondingscoringcriteriaforeachtaskarelisted
in Tab.7. Foreachtask,weevaluateeachmodelundertwosettings: in-domain(ID)andout-of-distribution(OOD).
13

Eachtask-settingpairisevaluatedwith15independenttrials. Inthein-domainsetting,boththerobotinitialposition
andthemanipulatedobjectsaredrawnfromthetrainingdistribution. Intheout-of-distributionsetting,therobotinitial
positionisperturbedwithin±10cmalongtheforward,backward,left,andrightdirectionsaroundthenominalinitial
pose. Inaddition,fortherefrigeratorsortingtask,thetwofruitsandthewaterbottletobeplacedintotherefrigeratorare
replacedwithunseenobjectcategories. Thissettingisdesignedtoevaluatethemodel’sgeneralizationabilityunder
unseenobjectandpositionconditions.
Resultsanalysis. AsshowninTab.6,LingBot-VLA-2.0consistentlyoutperformsπ acrossbothroboticembodiments
0.5
andbothevaluationsettings. Inthein-domainsetting,LingBot-VLA-2.0achievesaprogressscore/successrateof
77.1/60.0ontherefrigeratorsortingtaskand84.3/66.7onthestovecleaningtask,improvingoverπ by11.8/
0.5
13.3and4.4/6.7points,respectively. TheseresultsindicatethatLingBot-VLA-2.0canbetterexecutelong-horizon
tasksequencesthatrequirecoordinatedbasemovement,objectmanipulation,andinteractionwitharticulatedobjects.
UndertheOODsetting,bothmodelsexhibitperformancedegradation,reflectingtheincreaseddifficultyintroduced
byperturbedinitialrobotposesandunseenmanipulatedobjects. Nevertheless,LingBot-VLA-2.0maintainsaclear
advantageoverπ ,achieving37.0/13.3ontherefrigerator-sortingtaskand67.5/40.0onthestove-cleaningtask.
0.5
Comparedwithπ ,thiscorrespondstoimprovementsof6.7/6.6and5.0/6.7points,respectively. Theperformance
0.5
gapisespeciallymeaningfulintermsofsuccessrate,suggestingthatLingBot-VLA-2.0ismorerobustincompleting
fulltasktrajectoriesratherthanonlymakingpartialprogress. Therefrigeratorsortingtaskshowsalargerdropfromthe
in-domaintotheout-of-distributionsettingthanthestovecleaningtask. Thisisexpectedbecausetheout-of-distribution
refrigeratorsettingsimultaneouslychangesboththeinitialrobotposeandthemanipulatedobjectcategories,requiring
strongerobject-levelgeneralizationandmorepreciselong-horizonrecovery. Incontrast,thestovecleaningtaskmainly
evaluatesrobustnesstoinitialposeperturbationswhilepreservingthetaskobjectsandscenestructure. Overall,the
resultsdemonstratethatLingBot-VLA-2.0achievesstrongerlong-horizonmobilemanipulationcapabilityandbetter
generalizationthanπ acrossbothembodiments.
0.5
Table 7. Scoring criteria for the long-horizon mobile manipulation
experimenttasks.
Task ScoringCriteria 1x head camera
1x fisheye camera
2 DoFhead
1.Movefromtheinitialpositiontothekitchenisland(6).
2.Pickupthedrinkfromthetableandplaceitintothebasket(9). 2x 6 DoFarm + 1 DoFgripper
3.Pickupthefirstfruitfromthetableandplaceitintothebasket(9). 2x wrist camera
4.Pickupthesecondfruitfromthetableandplaceitintothebasket(11). 2x 7 DoFarm +
5.Pickupandliftthebasket(8). 1 DoFgripper
Sortobjectsinto 6.Movetothefrontoftherefrigerator(10). 2x wrist camera
refrigerator 7.Opentherefrigeratordoorwideenoughtoplaceitemsinside(12).
8.Pickupthefirstfruitandplaceitintotherefrigerator(9).
4-DoFtorso
9.Pickupthesecondfruitandplaceitintotherefrigerator(11).
10.Pickupthedrinkandplaceitintotherefrigerator(9).
11.Closetherefrigeratordoor(6).
1.Movefromtheinitialpositiontothefrontofthestove(8).
2-DoFdifferential- 3-DoFomnidirectional-
2.Pickuptheblackpotrackandplaceitontheleftsideofthetable(16). drive base wheel base
3.Pickupthesponge(12).
Cobot Magic-ARX X5 AstribotS1
StoveCleaning 4.Wipeoffthewhitefoamonthestoveusingthesponge(18).
5.Transferthespongeandplaceitontherightsideofthestove(16).
6.Pickuptheblackrackandplaceitbackonthestove(16). Figure 9. Illustration of the long-horizon mobile
7.Pickuptheblackpotandplaceitontheleftburnerofthestove(14). manipulationexperimentsplatform.
6 Ablation Studies
6.1 Action Space
Actiontarget. Fortheactiontarget,relativejointactionssubstantiallyoutperformabsolutejointactions,improvingthe
averagesuccessratefrom33.7to55.0. ThisissupportedbytheactionstatisticsinFig.12A.Acrossthefourtasks,the
standarddeviationofrelQposisonly31%–37%ofthatofabsQpos;onthepooleddistribution,theactionstandard
deviationdecreasesfromabout0.80forabsQposto0.28forrelQpos.Therefore,relativeactionsconverttheprediction
targetfromglobaljoint-configurationregressionintolocalmotionregression,producingtargetsthataremorecentered
andhavelowervariance.
14

80
60
40
20
0
Barcode Scoop Rice Ketchup Microwave Bowl Avg.
)%( etaR
sseccuS
Action target Action space
Absolute (abs) Relative (rel) EEF Joint
81.7
76.8 76.8
58.7 55.0 55.0 58.7 60.0 58.3 56.0 55.0
42.7 41.7 43.8 42.7 41.7
33.7
22.7 24.0
13.3
Barcode Scoop Rice Ketchup Microwave Bowl Avg.
80
60 40
20
0
Barcode Scoop Rice Ketchup Microwave Bowl Avg.
)%(
etaR sseccuS
GM-100 Real-Robot Task Ablations
Each panel compares settings within one ablation group; shaded columns show the average.
Normalization Loss
MinMax Q01-Q99 MeanStd L1 L2
76.8 76.8
61.763.3 61.7
58.7 58.7 53.6 55.0 55.0 48.0 42.7 44.742.7 41.7 39.1 47.547.4 45.0 42.7 41.7 50.0 46.4
26.7 28.7
Barcode Scoop Rice Ketchup Microwave Bowl Avg.
Figure10. ResultsonthefourGM-100real-robottasks.
1L 2L 3L 4L 5L 6L 7L 1R 2R 3R 4R 5R 6R 7R
3
2
1
0
−1
−2
−3
sopQler
tnioJ
eulav
dezilamron-dtSnaeM
Pooled
ALL
PooNle=d3 6A0LkL
1L 2L 3L 4L 5L 6L 7L 1R 2R 3R 4R 5R 6R 7R
Barcode
Scan
GSaRp 508.6.78
1L 2L 3L 4L 5L 6L 7L 1R 2R 3R 4R 5R 6R 7R
Scoop
Rice
GSaRp 402.5.75
1L 2L 3L 4L 5L 6L 7L 1R 2R 3R 4R 5R 6R 7R
Squeeze
Ketchup
GSaRp 411.5.79
1L 2L 3L 4L 5L 6L 7L 1R 2R 3R 4R 5R 6R 7R
Take Bowl
from Microwave
GSaRp 706.7.82
xL yL zL xqL yqL zqL wqL xR yR zR xqR yqR zqR wqR
4
3
2
1
0
−1
−2
−3
−4
lacoLfeEler
FEE
eulav
dezilamron-dtSnaeM
PooNle=d3 6A0LkL
xL yL zL xqL yqL zqL wqL xR yR zR xqR yqR zqR wqR
GSaRp 214.7.03
xL yL zL xqL yqL zqL wqL xR yR zR xqR yqR zqR wqR
GSaRp 610.0.09
xL yL zL xqL yqL zqL wqL xR yR zR xqR yqR zqR wqR
GSaRp 801.9.76
xL yL zL xqL yqL zqL wqL xR yR zR xqR yqR zqR wqR
GSaRp 508.7.31
First column: pooled ALL; other columns: task-specific distributions. Whiskers: 1st-99th percentile.
Figure11. Per-dimensionMeanStd-normalizedactiondistributionsforjointandEEFactionspaces.Thefirstcolumnshowsthe
pooleddistributionoverallfourtasks,whiletheremainingcolumnsshowtask-specificdistributions.Thegapmeasurestask-to-pooled
distributionalignmentbasedonper-dimensionmedianandIQRdifferences.
Actionspace.Fortheactionspace,EEFandjointactionsobtainsimilaraveragesuccessrates,56.0and55.0,respectively,
butshowdifferenttask-levelpreferences. Toanalyzethis,Figure11comparestheper-dimensionMeanStd-normalized
actiondistributionsofeachtaskagainstthepooleddistributionoverallfourtasks. Weadditionallyreportadistribution-
alignment gap, computed from the per-dimension median and IQR differences between each task and the pooled
distribution;asmallergapindicatesthatthetask-specificactiondistributionisclosertotheoveralldistribution.
Theresultsshowthatdistributionalignmentexplainspart,butnotall,oftheaction-spacebehavior. ForBarcode
Scan,jointactionsaremuchclosertothepooleddistributionthanEEFactions,withagapof0.68versus1.73,consistent
withthelargeperformanceadvantageofjointactions(58.7vs. 24.0). ForSqueezeKetchup,theoppositetrendappears:
EEFactionshaveasmallergapthanjointactions(0.96vs. 1.59)andachievemuchhighersuccess(81.7vs. 41.7),
15

suggestingthatcontact-richendpointmotionsarebetterrepresentedinCartesianEEFspace. ForScoopRice,however,
EEFactionsoutperformjointactionsdespitealargerdistributiongap,indicatingthatCartesianmotionregularitycan
outweighpuredistributionalignment. ForTakeBowlfromMicrowave,thetwogapsarenearlyidentical(0.71–0.72),
whilejointactionsstillperformbetter,suggestingthatposture,reachability,andconfiguration-dependentconstraintsare
moreimportantthanmarginalactionstatistics. Overall,thebestactionspacedependsonbothdistributionalalignment
andthephysicalstructureofthetask.
1.0
0.8
0.6
0.4
0.2
0.0
ALL Barcode Scoop Squeeze Take Bowl
Scan Rice Ketchup from Microwave
)mra
D-41(
.dts
noitca
waR
A. Relative target compresses the action scale
4
0.34x 0.37x 0.31x 0.36x 0.35x 3
2
1
0
−1
−2
−3
−4
MinMax Q01-Q99 MeanStd
w/o clip
Absolute qpos Relative qpos
eulav
sopQler
dezilamroN
B. Normalization reshapes relQpos distribution
σ=0.15 σ=0.32 σ=0.95
|x|>1.5: 0.0% |x|>1.5: 0.2% |x|>1.5: 10.0%
Figure12.ActiontargetsandnormalizationstatisticsforthefourGM-100tasks.Left:relQpossubstantiallyreducestheactionscale
comparedwithabsQpos.Right:normalizationchangestheeffectivedynamicrangeofMeanStd-normalizedrelQpos;Q01–Q99is
shownintheactualunclippedsetting.
Normalization. Fornormalization,Figure12BshowsthenormalizedrelQposdistributionsunderthethreeschemes.
MinMaxcompressesmostsamplesintoanarrowrange: itsnormalizedstandarddeviationisonly0.15,andthe1st–99th
percentileintervalisapproximately[−0.42,0.40]. Thisstrongcompressionreducestheeffectiveresolutionoftheaction
targets,whichexplainsitsloweraveragesuccessrateof47.5.
Q01–Q99increasesthenormalizedstandarddeviationto0.32andexpandsthecentralmasstoroughly[−0.96,1.01].
Importantly,theactualimplementationusedhereisnotclipped;onlyabout0.2%ofvaluesfalloutside[−1.5,1.5]. Thus,
itsweaknessisnotinformationlossfromclipping,butratherthatthenormalizedtargetsremainmuchmorecompressed
thanunderMeanStd. ThisexplainswhyQ01–Q99improvesthecentraldynamicrangeoverMinMaxbutstillachievesa
similaraveragesuccessrateof47.4.
MeanStdprovidesthelargesteffectivedynamicrange, withnormalizedstandarddeviation0.95anda1st–99th
percentile interval of approximately [−3.22,3.30]. Around 10.0% of samples lie outside |x| > 1.5, reflecting the
long-tailedstructureoftherelativeactiondistributionratherthanclipping. Bypreservingtheselargercorrectivemotions,
MeanStdachievesthebestaveragesuccessrateof55.0.
Lossfunction. Forthelossfunction,L2achievesthebestaverageperformance,improvingoverL1from46.4to55.0.
Since most relQpos targets are small continuous corrections around zero, L2 better fits the high-density region of
theactiondistributionandencouragespreciseregression. L1performsbetteronSqueezeKetchup,consistentwithits
robustnesstocontact-richorheavy-tailedmotions,butunderperformsontheotherthreetasks.
6.2 Perceptual Results of Dual-query Distillation
WeadoptLingBot-DepthandDINO-Videoasthevisualteachermodelsfordistillationtraining. Despiteperceptual
results not being essential for action generation, integrating specific task queries allows the VLA to obtain visual
perceptualoutcomesduringcausalinference. AsshowninFig.13,wepresentthecausalperceptionresultsofLingBot-
VLA 2.0,whichvalidatetheeffectivenessofourmodelindistillingsemanticpriorsandgeometriccues.
16

CurrentImage Depth-Target Depth-Pred. DINO-Target DINO-Pred. FutureImage Depth-Target Depth-Pred. DINO-Target DINO-Pred.
Figure13. CausalperceptionresultsofLingBot-VLA 2.0undervisualdistillation.Left:depth/DINO-Video-PCAgroundtruth
andpredictionforcurrentimage.Right:depth/DINO-Video-PCAgroundtruthandpredictionforfutureimage.
7 Conclusion
LingBot-VLA 2.0narrowsthegapbetweenVLAfoundationmodelsandreal-worldroboticdeploymentbyimproving
generalization, expanding whole-body action modeling, and strengthening temporal reasoning through predictive
dynamics. Withlarge-scalerobotandegocentricpretrainingdata,LingBot-VLA 2.0achievesimprovedperformance
ontheGM-100benchmarkanddemonstratesstronglong-horizonmobilemanipulationacrossmultipleroboticplatforms.
Acknowledgment. WethankFangyiXu,NingyuanHuang,HaotianLiu,JialiangZheng,LipingZhang,WeilunYao,
ShuaiWang,LinyuSu,FanFan,BoJiang,JingmeiZhao,ShuaiZhou,YinghaoXuandHaiweiLiangforhelpwithdata,
evaluationexperiments,traininginfrastructure,robothardware,androbotsoftware. WealsogratefullyacknowledgeAnt
DigitalTechnologies’PhecdaLaboratoryandGenrobot.aiCo.,Ltd. forprovidingtheegocentricdata.
References
[1] NiketAgarwal,ArslanAli,JonAllen,MartinAntolini,AdelineAubame,AlissonAzzolini,JunjieBai,MaciejBala,Yogesh
Balaji,JoshBapst,etal. Cosmos3:Omnimodalworldmodelsforphysicalai. arXivpreprintarXiv:2606.02800,2026.
[2] MahmoudAssran,AdrienBardes,DavidFan,QuentinGarrido,RussellHowes,MojtabaKomeili,MatthewMuckley,Ammar
Rizvi,ClaireRoberts,KoustuvSinha,ArtemZholus,SergioArnaud,AbhaGejji,AdaMartin,FrancoisRobertHogan,Daniel
Dugas,PiotrBojanowski,VasilKhalidov,PatrickLabatut,FranciscoMassa,MarcSzafraniec,KapilKrishnakumar,YongLi,
XiaodongMa,SarathChandar,FranziskaMeier,YannLeCun,MichaelRabbat,andNicolasBallas. V-jepa2:Self-supervised
videomodelsenableunderstanding,predictionandplanning. arXivpreprintarXiv:2506.09985,2025.
[3] ShuanghaoBai,MengLi,XinyuanLv,JiaweiWang,XinhuaWang,FeiLiao,ChengkaiHou,LangzheGu,WanqiZhou,KunWu,
ZiluoDing,ZhiyuanXu,LeiSun,ShanghangZhang,ZhengpingChe,JianTang,andBadongChen. HEX:Humanoid-aligned
expertsforcross-embodimentwhole-bodymanipulation. arXivpreprintarXiv:2604.07993,2026.
[4] JohanBjorck,FernandoCastañeda,NikitaCherniadev,XingyeDa,RunyuDing,LinxiFan,YuFang,DieterFox,FengyuanHu,
SpencerHuang,etal. GR00TN1:Anopenfoundationmodelforgeneralisthumanoidrobots. arXivpreprintarXiv:2503.14734,
2025.
[5] KevinBlack,NoahBrown,JamesDarpinian,KaranDhabalia,DannyDriess,AdnanEsmail,MichaelRobertEqui,Chelsea
Finn,NiccoloFusai,ManuelY.Galliker,DibyaGhosh,LachyGroom,KarolHausman,brianichter,SzymonJakubczak,Tim
Jones,LiyimingKe,DevinLeBlanc,SergeyLevine,AdrianLi-Bell,MohithMothukuri,SurajNair,KarlPertsch,AllenZ.Ren,
LucyXiaoyangShi,LauraSmith,JostTobiasSpringenberg,KyleStachowicz,JamesTanner,QuanVuong,HomerWalke,Anna
17

Walling,HaohuanWang,LiliYu,andUryZhilinsky. π :Avision-language-actionmodelwithopen-worldgeneralization. In
0.5
ConferenceonRobotLearning,2025.
[6] KevinBlack,NoahBrown,DannyDriess,AdnanEsmail,MichaelEqui,ChelseaFinn,NiccoloFusai,LachyGroom,Karol
Hausman,BrianIchter,SzymonJakubczak,TimJones,LiyimingKe,SergeyLevine,AdrianLi-Bell,MohithMothukuri,Suraj
Nair,KarlPertsch,LucyXiaoyangShi,JamesTanner,QuanVuong,AnnaWalling,HaohuanWang,andUryZhilinsky. π :A
0
vision-language-actionflowmodelforgeneralrobotcontrol. InProceedingsofRobotics:ScienceandSystems,2025.
[7] RuiCai,JunGuo,XinzeHe,PiaopiaoJin,JieLi,BingxuanLin,FutengLiu,WeiLiu,FeiMa,KunMa,FengQiu,Heng
Qu,YifeiSu,QiaoSun,DongWang,DonghaoWang,YunhongWang,RujieWu,DiyunXiang,YuYang,HangjunYe,Yuan
Zhang,andQuanyunZhou. Xiaomi-robotics-0:Anopen-sourcedvision-language-actionmodelwithreal-timeexecution. arXiv
preprintarXiv:2602.12684,2026.
[8] ChilamCheang,SijinChen,ZhongrenCui,YingdongHu,LiqunHuang,TaoKong,HangLi,YifengLi,YuxiaoLiu,XiaoMa,
etal. GR-3technicalreport. arXivpreprintarXiv:2507.15493,2025.
[9] JialeiChen,KaiWang,KangChen,ShuaihangChen,FengGao,WenhaoTang,ZhiyuanLi,WeilinLiu,ZhuyuYao,BoxunLi,
etal. Lawam:Latentworldactionmodelsforefficientdynamics-awarerobotpolicies. arXivpreprintarXiv:2606.15768,2026.
[10] RonghanChen,YandanYang,ZuojinTang,DongjieHuo,TongLin,HaoningWu,HaoyunLiu,YuzhiChen,LuluZheng,Botai
Yuan,TianlunLi,MingxinWang,DekangQi,BinHu,WeiMei,YuzeXuan,HaolongYang,YanqingZhu,MuXu,ZhihengMa,
andXinyuanChang. Abot-m0.5:Unifiedmobility-and-manipulationworldactionmodel. arXivpreprintarXiv:2607.00678,
2026.
[11] DexForceAITeamofPhysicalAI. Dexworldmodel:Causallatentworldmodelingtowardsautomatedlearningofembodied
tasks,2026. Technicalreport.
[12] ZhiyingDu,BeiLiu,YaoboLiang,YichaoShen,HaidongCao,XiangyuZheng,ZhiyuanFeng,ZuxuanWu,JiaolongYang,and
Yu-GangJiang. HiMoE-VLA:Hierarchicalmixture-of-expertsforgeneralistvision-language-actionpolicies. arXivpreprint
arXiv:2512.05693,2025.
[13] GalaxeaTeam. Galaxeag0.5technicalreport,2026. Technicalreport.
[14] TaoJiang,TianyuanYuan,YichengLiu,ChenhaoLu,JianningCui,XiaoLiu,ShuiqiCheng,JiyangGao,HuazheXu,andHang
Zhao. Galaxeaopen-worlddatasetandG0dual-systemvlamodel. arXivpreprintarXiv:2509.00576,2025.
[15] DongyoungKim,HuiwonJang,MyungkyuKoo,SuhyeokJang,TaeyoungKim,BeomjunKim,ByungjunYoon,Changsung
Jang,DaewonChoi,DongsuHan,DongukLee,HeeseungKwon,HojinJeon,JaehyunKang,JaekyoungBae,JihyukLee,Jimin
Lee,JohnWon,JoonwooAhn,JunhyeongPark,JunyoungSung,KyungminLee,MinseongHan,MinsungYoon,SejuneJoo,
SeonilSon,SeungcheolPark,SeunggeunCho,SeungjunMoon,SeungkuKim,YonghoonDong,YongjinCho,YoungchanKim,
etal. RLDX-1technicalreport. arXivpreprintarXiv:2605.03269,2026.
[16] MooJinKim,KarlPertsch,SiddharthKaramcheti,TedXiao,AshwinBalakrishna,SurajNair,RafaelRafailov,EthanPFoster,
PannagRSanketi,QuanVuong,etal. OpenVLA:Anopen-sourcevision-language-actionmodel. InConferenceonRobot
Learning,2025.
[17] YangLi,Zhaxizhuoma,HongruJiang,JunjieXia,HongquanZhang,JindaDu,YunsongZhou,JiaZeng,CeHao,JiejiRen,
QiaojunYu, CewuLu, YuQiao, andJiangmiaoPang. ForceVLA2: Unleashinghybridforce-positioncontrolwithforce
awarenessforcontact-richmanipulation. arXivpreprintarXiv:2603.15169,2026.
[18] XuewuLin,TianweiLin,YunDu,HongyuXie,YiweiJin,JiaweiLi,ShijieWu,QingzeWang,MengdiLi,MengaoZhao,
ZiangLi,ChaodongHuang,HongzheBi,LichaoHuang,andZhizhongSu. Holobrain-0technicalreport. arXivpreprint
arXiv:2602.12062,2026.
[19] AixinLiu,BeiFeng,BingXue,BingxuanWang,BochaoWu,ChengdaLu,ChenggangZhao,ChengqiDeng,ChenyuZhang,
ChongRuan,etal. Deepseek-v3technicalreport. arXivpreprintarXiv:2412.19437,2024.
[20] HaoLuo,YichengFeng,WanpengZhang, SipengZheng, YeWang,HaoqiYuan,JiazhengLiu,ChaoyiXu,QinJin,and
ZongqingLu. Being-h0:Vision-language-actionpretrainingfromlarge-scalehumanvideos. arXivpreprintarXiv:2507.15597,
2025.
[21] HaoLuo,YeWang,WanpengZhang,SipengZheng,ZihengXi,ChaoyiXu,HaiwengXu,HaoqiYuan,ChiZhang,Yiqing
Wang,YichengFeng,andZongqingLu.Being-h0.5:Scalinghuman-centricrobotlearningforcross-embodimentgeneralization.
arXivpreprintarXiv:2601.12993,2026.
[22] HaoLuo,WanpengZhang,YichengFeng,SipengZheng,HaiwengXu,ChaoyiXu,ZihengXi,YuhuiFu,andZongqingLu.
Being-h0.7:Alatentworld-actionmodelfromegocentricvideos. arXivpreprintarXiv:2605.00078,2026.
18

[23] JiangranLyu,KaiLiu,XuhengZhang,HaoranLiao,YusenFeng,WenxuanZhu,TingruiShen,JiayiChen,JiazhaoZhang,
YifeiDong,WenboCui,SenmaoQi,ShuoWang,YixinZheng,MiYan,XuesongShi,HaoranLi,DongbinZhao,Ming-YuLiu,
ZhizhengZhang,LiYi,YizhouWang,andHeWang. LDA-1b:Scalinglatentdynamicsactionmodelviauniversalembodied
dataingestion. arXivpreprintarXiv:2602.12215,2026.
[24] DujunNie,FengjiaoChen,QiLv,JunKuang,XiaoyuLi,XuezhiCao,andXunliangCai. Lary:Alatentactionrepresentation
yieldingbenchmarkforgeneralizablevision-to-actionalignment. arXivpreprintarXiv:2604.11689,2026.
[25] QwenTeam. Qwen3.6-27B:Flagship-levelcodingina27Bdensemodel,April2026.
[26] OrianeSiméoni, HuyV.Vo, MaximilianSeitzer, FedericoBaldassarre, MaximeOquab, CijoJose, VasilKhalidov, Marc
Szafraniec,SeungeunYi,MichaëlRamamonjisoa,FranciscoMassa,DanielHaziza,LucaWehrstedt,JianyuanWang,Timothée
Darcet,ThéoMoutakanni,LeonelSentana,ClaireRoberts,AndreaVedaldi,JamieTolan,JohnBrandt,CamilleCouprie,Julien
Mairal,HervéJégou,PatrickLabatut,andPiotrBojanowski. DINOv3,2025.
[27] YueSu,SijinChen,HaixinShi,MingyuLiu,ZhengshenZhang,NingyuanHuang,WeihengZhong,ZhengbangZhu,Yuxiao
Liu,andXihuiLiu. Worldguidance:Worldmodelinginconditionspaceforactiongeneration. InICML,2026.
[28] BinTan,ChangjianSun,XiageQin,HanatAdai,ZelinFu,TianxiangZhou,HanZhang,YinghaoXu,XingZhu,YujunShen
Shen,andNanXue. Maskeddepthmodelingforspatialperception. https://technology.robbyant.com/lingbot-depth,
2026.
[29] TutianTang,XingyuJi,WanliXing,CeHao,WenqiangXu,LinShao,CewuLu,QiaojunYu,JiangmiaoPang,andKaifeng
Zhang. Towardshuman-likemanipulationthroughRL-augmentedteleoperationandmixture-of-dexterous-expertsVLA. arXiv
preprintarXiv:2603.08122,2026.
[30] GeminiRoboticsTeam,SamindaAbeyruwan,JoshuaAinslie,Jean-BaptisteAlayrac,MontserratGonzalezArenas,Travis
Armstrong,AshwinBalakrishna,RobertBaruch,MariaBauza,MichielBlokzijl,etal. GeminiRobotics:BringingAIintothe
physicalworld. arXivpreprintarXiv:2503.20020,2025.
[31] Generalist Team. Gen-1: Scaling embodied foundation models to mastery. Generalist AI Blog, 2026.
https://generalistai.com/blog/gen-1.
[32] NVIDIAGEARTeam. GR00TN1.6:Animprovedopenfoundationmodelforgeneralisthumanoidrobots. https://research.
nvidia.com/labs/gear/gr00t-n1_6/,2025.
[33] QwenTeam. Qwen-robotmaniptechnicalreport:Alignmentunlocksscaleforroboticmanipulationfoundationmodels. 2026.
[34] QiuyueWang,MingshengLi,JianGuan,JinhuiYe,SichengXie,YitaoLiu,JunhaoChen,ZhixuanLiang,JieZhang,Xintong
Hu,XuhongHuang,PeiLin,JunyangLin,DayihengLiu,ShuaiBai,JingrenZhou,JiazhaoZhang,HaoqiYuan,GengzeZhou,
HangYin,YeWang,YiyangHuang,ZixingLei,WujianPeng,DelinChen,etal. Qwen-VLA:Unifyingvision-language-action
modelingacrosstasks,environments,androbotembodiments. arXivpreprintarXiv:2605.30280,2026.
[35] YunnanWang,FanLu,KechengZheng,ZiyuanHuang,ZiqiangLi,WenjunZeng,andXinJin. Vision-centricactivationand
coordinationformultimodallargelanguagemodels. arXivpreprintarXiv:2510.14349,2025.
[36] ZiyuWang,ChenyuanLiu,YushunXiang,RunhaoZhang,QingboHao,HongliangLu,HouyuChen,ZhizhongFeng,Kaiyue
Zheng,DehaoYe,XianchaoZeng,XinyuZhou,BoranWen,JiaxinLi,MingyuZhang,KechengZheng,QianZhu,RanCheng,
andYong-LuLi. TheGreatMarch100:100detail-orientedtasksforevaluatingembodiedaiagents,2026.
[37] XilinWei,XiaoranLiu,YuhangZang,XiaoyiDong,PanZhang,YuhangCao,JianTong,HaodongDuan,QipengGuo,Jiaqi
Wang,etal. Videorope:Whatmakesforgoodvideorotarypositionembedding? InInt.Conf.Mach.Learn.,2025.
[38] WeiWu,FanLu,YunnanWang,ShuaiYang,ShiLiu,FangjingWang,ShuaileiMa,HeSun,YongWang,ZhenqiQiu,Houlong
Xiong,ZiyuWang,ShuaiZhou,YiyuRen,KejiaZhang,HuiYu,JingmeiZhao,QianZhu,RanCheng,Yong-LuLi,Yongtao
Huang,XingZhu,YujunShen,andKechengZheng. Apragmaticvlafoundationmodel. arXivpreprintarXiv:2601.18692v1,
2026.
[39] TencentRoboticsXandHYVisionTeam. Hy-embodied-0.5-x:Anenhancedembodiedfoundationmodelforreal-worldagents.
2026.
[40] YibinYan,JilanXu,ShangzheDi,HaoningWu,andWeidiXie. Omnistream:Masteringperception,reconstructionandaction
incontinuousstreams. arXivpreprintarXiv:2603.12265,2026.
[41] JianweiYang, ReubenTan, QianhuiWu, RuijieZheng, BaolinPeng, YongyuanLiang, YuGu, MuCai, SeonghyeonYe,
JoelJang,etal. Magma:AfoundationmodelformultimodalAIagents. InIEEEConf.Comput.Vis.PatternRecog.,pages
14203–14214,2025.
19

[42] YandanYang,ShuangZeng,TongLin,XinyuanChang,DekangQi,JunjinXiao,HaoyunLiu,RonghanChen,YuzhiChen,
DongjieHuo,etal. Abot-m0:Vlafoundationmodelforroboticmanipulationwithactionmanifoldlearning. arXivpreprint
arXiv:2602.11236,2026.
[43] JinhuiYe,NingGao,SenqiaoYang,JinliangZheng,ZixuanWang,YuxinChen,PengguangChen,YilunChen,ShuLiu,and
JiayaJia. Starvla-
alpha:Reducingcomplexityinvision-language-actionsystems. arXivpreprintarXiv:2604.11757,2026.
[44] ZihanYou,HongweiLiu,ChenxuDang,ZheWang,SiningAng,AoqiWang,andYanWang. SAMoE-VLA:Asceneadaptive
mixture-of-expertsvision-language-actionmodelforautonomousdriving. arXivpreprintarXiv:2603.08113,2026.
[45] JiawenYu,HairuoLiu,QiaojunYu,JiejiRen,CeHao,HaitongDing,GuangyuHuang,GuofanHuang,YanSong,PanpanCai,
CewuLu,andWenqiangZhang. ForceVLA:EnhancingVLAmodelswithaforce-awareMoEforcontact-richmanipulation.
arXivpreprintarXiv:2505.22159,2025.
[46] RyanYu,PushiZhang,StarrickLiu,BraeLiu,MiracleKang,ShalfunLi,LightsShi,EllieMa,PingYang,ChrisPan,Jerry
Chen,DongxiuLiu,RainSun,MilesGuo,ByronZhang,HugoZhou,ZachXu,VincentChen,HarrisonHuang,JamesWang,
DanceKuzi,AndyZhai,HangSu,RoyGan,LucyLiang,HaoWang,andQianWang. Wall-oss-0.5technicalreport. arXiv
preprintarXiv:2605.30877,2026.
[47] AndyZhai,BraeLiu,BrunoFang,ChalseCai,EllieMa,EthanYin,HaoWang,HugoZhou,JamesWang,LightsShi,etal.
IgnitingVLMstowardtheembodiedspace. arXivpreprintarXiv:2509.11766,2025.
[48] LikuiZhang,TaoTang,ZhihaoZhan,XiuweiChen,ZishengChen,JianhuaHan,JiangtongZhu,PeiXu,HangXu,Hefeng
Wu,LiangLin,andXiaodanLiang. AtomicVLA:Unlockingthepotentialofatomicskilllearninginrobots. arXivpreprint
arXiv:2603.07648,2026.
[49] Ruowen Zhao, Bangguo Li, Zuyan Liu, Yinan Liang, Junliang Ye, Fangfu Liu, Diankun Wu, Zhengyi Wang, Xumin
Yu, Yongming Rao, Han Hu, and Jun Zhu. GEM: Generative supervision helps embodied intelligence. arXiv preprint
arXiv:2605.28548,2026.
20