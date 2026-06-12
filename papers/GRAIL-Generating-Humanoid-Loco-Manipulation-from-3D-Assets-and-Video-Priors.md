2026-6-4
| GRAIL: | Generating | Humanoid | Loco-Manipulation | from 3D |
| ------ | ---------- | -------- | ----------------- | ------- |
| Assets | and Video  | Priors   |                   |         |
TianyiXie1,2,:,HaotianZhang1,:,JinhyungPark1,:,ZiWang1,:,BowenWen1,JiefengLi1,XuetingLi1,
QingweiBen1,HaoyangWeng1,YufeiYe1,DavidMinor1,TingwuWang1,ChenfanfuJiang2,SanjaFidler1,
JanKautz1,LinxiFan1,YukeZhu1,ZhengyiLuo1,;,UmarIqbal1,;,YeYuan1,;
| 1NVIDIA          | 2UCLA         |     |     |     |
| ---------------- | ------------- | --- | --- | --- |
| :Co-FirstAuthors | ;ProjectLeads |     |     |     |
https://research.nvidia.com/labs/dair/grail/
6202 nuJ 3  ]OR.sc[  1v06150.6062:viXra
Figure 1: From Fully Digital Data Generation to Real-World Deployment. GRAIL generates humanoid
loco-manipulationdatafrom3Dassetsandvideopriorswithoutphysicalscenerebuildsorrobotteleoperation.
Top: simulatedhumanoidsexecutegeneratedreferencesspanningpick-up,whole-bodymanipulation,sitting,
andterraintraversal. egocentricvisualpoliciestrainedonlyonGRAIL-generateddataaredeployedon
Bottom:
aUnitreeG1forstair-climbingandobjectpick-up.
© 2026NVIDIA.Allrightsreserved.

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
Abstract
Scalinghumanoidloco-manipulationrequiresrobot-compatibledemonstrationsacrossdiverseobjects,
whole-bodymotions,andscenegeometries,butteleoperationandmotioncapturearedifficulttoscale
because each collection depends on physical setups, instrumented actors, and robot operation. We
presentGRAIL,adigitalgenerationpipelinethatremainsfullyvirtualuntildeployment: itcomposes3D
assets,simulator-readyscenes,andpriorsfromvideofoundationmodels(VFMs)tosynthesizeinterac-
tionswithoutrebuildingphysicalenvironmentsorteleoperatingtherobot. Ratherthanreconstructing
unconstrainedin-the-wildvideos,GRAILstartsfromfullyspecified3Dconfigurationsinwhichobject
geometry,cameraparameters,metricscale,environmentdepth,andarobot-proportionedcharacterare
knownbeforevideogenerationandreusedduringreconstruction. Thisprivilegedsetupbetterconditions
4Drecovery,allowingmodel-basedobjecttracking,humanmotionestimation,andinteraction-aware
optimizationtoreconstructmetric4Dhuman-objectinteraction(HOI)trajectorieswithreduceddepth
ambiguity and morphology mismatch. We retarget the recovered motions to a humanoid robot and
train complementary task-general trackers: an object-aware latent adaptor for manipulation and a
scene-aware tracker for terrain traversal. GRAIL produces over 20,000 sequences spanning pick-up,
whole-body manipulation, sitting, and terrain traversal. Using only GRAIL-generated data, we train
egocentricvisualpoliciesthroughasim-to-realpipelineanddeploythemonaUnitreeG1humanoid,
achieving84%real-worldsuccessondiverseobjectpick-upand90%successonstair-climbing.
1. Introduction
Humanoidloco-manipulationrequirespoliciesthatcoordinatewhole-bodybalance,objectcontact,andscene-
awarelocomotionacrossabroaddistributionofobjectsandterraingeometries. Scalingthecorresponding
demonstrationdataischallengingbecauseeachtrajectorymustbebothphysicallyplausibleandexecutable
by the target robot. Teleoperation (Aldaco et al., 2024; Ben et al., 2025; Khazatsky et al., 2024; Ze et al.,
2025a,b)andmotioncapture(Luetal.,2025;Taherietal.,2020)providehigh-qualitydemonstrations,but
theyaredifficulttoscale: eachnewobjectorterrainlayoutcanrequirehuman-operatedrobotdemonstrations,
instrumented actors, and physical scene reconfiguration. Reconstructing robot-ready 4D trajectories from
in-the-wildvideos(Houetal.,2023;Kimetal.,2023;Petrovetal.,2023;Wangetal.,2022;Xieetal.,2022,
2026;Zhangetal.,2020)offersbroadvisualcoverage,butrequiresinferringcamera,scale,objectgeometry,
humanshape,contacts,andworld-spacemotionfromambiguousmonocularobservations. Recentadvancesin
3Dassetgenerationandvideofoundationmodelssuggestanalternativeroute: insteadofrecoveringtheentire
3Dinteractionfromanuncontrolledvideo,canwefirstspecifythe3Dsceneandthenusevideogenerative
priorstosynthesizediverseinteractionsforhumanoidpolicylearning?
WeintroduceGRAIL,ahumanoid-centricdata-generationpipelinethatremainsfullydigitaluntilreal-world
deployment. Itusesvideofoundationmodels(VFMs)asinteractionpriorsinsideasimulator-ready3Dasset
pipeline: ratherthanreconstructinguncontrolledvideosintoambiguous4Dscenes,GRAILfirstspecifiesthe
object,scenegeometry,camera,scale,androbot-proportionedcharacter,thenrecoverstheinteractionwithin
this known metric frame. This design addresses two bottlenecks of prior data sources: it avoids repeated
physicalcollectionrequiredbyteleoperationandmotioncapture,anditproducesrobot-trackabletrajectories
alreadyalignedwithsimulationfordownstreamsim-to-realpolicytraining.
Therecovered4DHOItrajectoriesareretargetedtoaUnitreeG1andconvertedintotask-generaltracking
policies built on a pretrained whole-body controller (Luo et al., 2025). Rather than fitting one controller
per sequence or per object, we pool related trajectories so the trackers cover families of manipulation and
scene-interactionbehaviors. Thisstageusestwocomplementaryspecializations: anobject-awarelatentadaptor
thataugmentsthefrozenwhole-bodycontrollerwithmanipulationbymodulatingitslatenttokensandemitting
handactions,andascene-awaretrackerthatfine-tunesthecontrollertogetherwithaheight-mapencoderfor
2

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
terrain-conditionedwhole-bodycontrol. Withthispipeline,wegeneratealarge-scaledatasetofover20,000
humanoid loco-manipulation sequences spanning pick-up, whole-body manipulation, sitting, and terrain
traversal. Using only this generated data, we train egocentric visual policies (He et al., 2025a) with visual
domainrandomizationandcameraalignmentasaclosed-loopsim-to-realvalidation;deployedonaUnitreeG1,
theresultingRGB-basedpoliciesperformautonomousloco-manipulationonpick-upandstair-climbingtasks.
Insummary,GRAILmakesthefollowingcontributions: (i)afullydigitalhumanoid-centricdata-generation
frameworkthatusesVFMsasinteractionpriorsinsideafullyspecified3Dassetpipeline,producingover20,000
physicallyplausibleloco-manipulationsequences;(ii)aninteraction-aware4DHOIreconstructionstackthat
exploits known geometry, metric scale, camera parameters, environment depth, and a robot-proportioned
character; (iii)complementarytask-generaltrackersforreconstructed4DHOI,pairingobject-awarelatent
adaptationformanipulationwithscene-awareheight-mapconditioningforterraintraversalandsitting;and
(iv)anend-to-endsim-to-realvalidationofGRAIL-generateddatathroughegocentricvisualpoliciesdeployed
onaUnitreeG1,achieving84%pick-upsuccessand90%stair-climbingsuccessintherealworld.
2. Related Work
Human-ObjectInteractionGenerationandReconstruction. Synthesizinghuman-objectinteractions(HOI)
requiresreasoningabouthumanmotion,objectaffordances,andphysicalcontact. Existingdatasourcesrely
onmotioncapture(Bhatnagaretal.,2022;Fanetal.,2023;Huangetal.,2022;Jiangetal.,2023;Kimetal.,
2025b;Lietal.,2023a;Luetal.,2025;Taherietal.,2020;Zhangetal.,2023b;Zhaoetal.,2024)orRGB-based
reconstruction(Houetal.,2023;Kimetal.,2023;Petrovetal.,2023;Wangetal.,2022;Xieetal.,2022,2026;
Zhangetal.,2020),butremainexpensive,category-limited,orunderconstrained. Learning-basedmethods
synthesizeHOIfromaffordance,language,orvision-languagepriors(Dangetal.,2025;DillerandDai,2024;
Dwivedietal.,2025;Jiangetal.,2024;Kulkarnietal.,2024;Lietal.,2024;LiandDai,2024;Lietal.,2023b;
Pengetal.,2025;Wuetal.,2025;Xuetal.,2023,2024;Yeetal.,2023;Zhangetal.,2023a,2025;Zheng
etal.,2023;Zhouetal.,2022),butphysicalrealismandtemporalcoherenceremainchallenging. VFM-based
pipelinessuchasDAViD(Kimetal.,2025a),ZeroHSI(Lietal.,2026),andrelatedmethods(Louetal.,2025)
usegeneratedvideosaspriorsfor4DHOIrecovery,yettypicallyleavecamera,scale,charactermorphology,
objectgeometry,orenvironmentstructuretobeinferredaftergeneration. GRAILinsteadspecifiesthe3Dscene
beforegenerationandreusesitduringreconstruction,yieldingrobot-compatible4DHOItrajectoriesgrounded
byknownmetricscale,environmentgeometry,andarobot-proportionedcharacter,facilitatingdownstream
sim-to-realpolicylearning.
HumanVideoasHumanoidSupervision. Humanvideohasbecomeanincreasinglyimportantsupervision
sourceforhumanoids: large-scalemining,retargeting,androbotized-videogenerationprovidebroadpose-
control or pretraining data (Mao et al., 2024; Yang et al., 2025), while VideoMimic (Allshire et al., 2025),
HumanX (Wang et al., 2026), and related systems (Shi et al., 2026; Weng et al., 2025; Yin et al., 2025;
Yu et al., 2025) train interaction policies from third-person, monocular, or egocentric videos. In parallel,
physics-basedcontrolandwhole-bodyimitation(Fuetal.,2024;Heetal.,2024,2025b;Luoetal.,2023,2025;
Pengetal.,2018,2021),residualadaptors(Zhaoetal.,2025),andmultimodalcontrollers(Heetal.,2026;
Jiangetal.,2026)showhowrobot-readyreferencescanbeconvertedintoexecutablepolicies. Theshared
bottleneckisdata: videosstillrequirerecoveringmetricmotion,contacts,objectstate,andscenegeometry,
whileteleoperation,motioncapture,wearableinterfaces,andgeneratedrobot-videodemonstrations(Benetal.,
2025;Khazatskyetal.,2024;Luetal.,2025;Naietal.,2026;Pateletal.,2025;Taherietal.,2020;Zeetal.,
2025a,b)remainlimitedbyhumaneffort,retargeting,platformdependence,ormorphologymismatch. GRAIL
addressesthisupstreambottleneckbyusinggeneratedvideoforbehavioralpriorswhilekeepinggeometry,
scale, camera, environment, and target morphology known, producing robot-compatible 4D references for
task-generaltrackingpolicies.
3

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
Figure2:Asset-Conditioned4DHOIGeneration. Givena3Dobjectasset,werenderafullyspecified3Dscene
withacharacterprefittedtothetargethumanoidandknowncameraparameters,synthesizeastatic-camera
interaction video via a VFM conditioned on the rendered frame, and reconstruct metric 4D human-object
motionbyjointlyrefininginitialhumanandobjecttrajectoryestimateswithkeypoint,depth,andcontactlosses
anchoredtotheprivileged3Dconfiguration.
3. Method
Givena3Dobjectassetℳ𝒪,GRAILproduceshumanoidloco-manipulationdemonstrationscomprisinghu-
manoidkinematicmotiontΘℛu𝑇 ,objectkinematicmotiontΘ𝒪u𝑇 ,androbotactionst𝑎ℛu𝑇 . Ourdata
𝑡 𝑡“1 𝑡 𝑡“1 𝑡 𝑡“1
generation pipeline proceeds in three stages. First, we assemble a fully specified 3D configuration with a
characterprefittedtothetargetrobot,renderaninitialframe,andfeeditintoaVFMtosynthesizeareference
HOIvideot𝐼 u𝑇 (Sec.3.1). Second,leveragingtheknown3Dconfiguration,wereconstructcoherent4DHOI
𝑡 𝑡“1
trajectoriestpΘ r ℋ,Θ r 𝒪qu𝑇 throughhumanposeestimation,objecttracking,andjointoptimization(Sec.3.2).
𝑡 𝑡 𝑡“1
Third,weretargetthereconstructedmotionstothetargethumanoidandtraintask-generaltrackingpolicies
acrosseachtaskfamily(Sec.3.3). Usingthegenerateddata,wefurthertrainegocentricvisualpoliciesthrough
asim-to-realpipelineanddeploythemonarealUnitreeG1forpick-upandstair-climbing(Sec.3.4).
3.1. Robot-Centric Human Video Generation
Althoughonecouldgeneraterobotvideosdirectly,currentVFMshavestrongerpriorsoverhumanmanipulation,
andhumanbodyandhandreconstructiontoolsaremorematurethanrobotreconstructiontools. Wetherefore
synthesizehumaninteractionvideosusingacharacterassetprefittedtothetargethumanoid,whichfacilitates
retargeting the recovered motion to the robot. To assemble the 3D configuration, we construct candidate
environmentsusingInfinigen(Raistricketal.,2023)andpositionthehumanassetinarestposealongsidethe
object. Weuserigidbodysimulation(Macklinetal.,2016)tosettletheobjectintoastable,collision-freeinitial
configuration Θ𝒪. We then render the first frame using Blender with known camera intrinsics 𝐶 P R3ˆ3
1 𝐾
and extrinsics 𝐶 “ p𝑟𝒞,𝑡𝒞q. The generated environment serves two purposes: realistic visual context
𝐸
forVFMgenerationandaground-truthpointcloudformetric-scaledepthalignmentduringreconstruction
(Sec.3.2). AVLM(OpenAI,2024)generatesaninteractionpromptfromtherenderedframe,andaVFM(e.g.,
Kling(Kuaishou,2025))thensynthesizesthereferenceHOIvideot𝐼 u𝑇 underastatic-camerasettingthat
𝑡 𝑡“1
preservestheknowncameraparametersp𝐶 ,𝐶 qforreconstruction.
𝐾 𝐸
3.2. Interaction-Aware HOI Reconstruction
Giventhegeneratedinteractionvideo,werecoverthe4DHOItrajectorytpΘ r ℋ,Θ r 𝒪qu𝑇 intwosteps: inde-
𝑡 𝑡 𝑡“1
pendentinitialestimationofhumanandobjectmotion,followedbyinteraction-awarejointoptimizationthat
anchorsthetrajectoriestotheprivileged3Dconfiguration.
3.2.1. InitialMotionEstimation
Wefirstestimatehumanandobjectmotionindependently,yieldinginitialworld-spacetrajectoriestΘ p ℋu𝑇
𝑡 𝑡“1
andtΘ p 𝒪u𝑇 .
𝑡 𝑡“1
4

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
HumanMotionEstimation.Forthehumanbody,GENMO(Lietal.,2025)providesper-frameSMPL-X(Pavlakos
etal.,2019)poseparametersfromthegeneratedvideoincameraspace;thebodyshapeisheldfixedatthe
prefittedcharactermorphologyfromSec.3.1ratherthanre-estimated,soGENMOonlycontributesper-frame
poseparameters. Thecamera-spacemotionisthentransformedintoworldcoordinatesusingtheknowncamera
extrinsics𝐶 . Forthehands,WiLoR(Potamiasetal.,2025)refinesper-frameMANO(Romeroetal.,2017)
𝐸
parametersfortheleftandrighthandsindependently;missingdetectionsduetopartialocclusionordetection
failurearefilledviatemporallinearinterpolationandsmoothedwithaSavitzky-Golayfilter(Savitzkyand
Golay, 1964) to suppress per-frame jitter. The smoothed hand poses are integrated into the SMPL-X body
throughwristinverse-kinematic(IK)alignment,preservingtheWiLoR-predictedfingerconfiguration.
ObjectPoseTracking. Fortheobject,wefine-tuneFoundationPose(Wenetal.,2024)onitsproposedsynthetic
datasetfor5epochswiththedepthchannelszeroedatbothtrainingandinferencetoadapttoourRGB-only
setup;atinference,the6-DoFtrackerisinitializedfromtheknownfirst-frameposeΘ𝒪 andpropagatesthe
1
objectposeacrossallframes. FoundationPoserequiresknownobjectgeometry,texture,andcameraparameters,
allavailableinourpipelinebyconstruction,whichensuresaccurateobjecttracking. Weadditionallyvalidate
tracking quality by comparing predicted poses against SAM2 (Ravi et al., 2024) segmentation masks and
discardsequenceswithinconsistentgeometry(Sec.A.3).
3.2.2. JointOptimization
Directlycombiningtheindependentreconstructionsoftenproducesmisalignedinteractions(floatingcontacts,
penetration,anddepth-scaledrift). Wethereforejointlyrefinebothtrajectoriesthroughaglobaloptimization
over all frames, holding the hand poses fixed for stability. Rather than optimizing full trajectories directly,
weoptimizeresidualmotionparameterst∆Θℋu𝑇 andt∆Θ𝒪u𝑇 ; thefinalposesareΘℋ “ Θ p ℋ‘∆Θℋ
𝑡 𝑡“1 𝑡 𝑡“1 𝑡 𝑡 𝑡
and Θ𝒪 “ Θ p 𝒪 ‘ ∆Θ𝒪, with ‘ denoting residual translation and rotation updates and the 6D rotation
𝑡 𝑡 𝑡
representation(Zhouetal.,2019)usedforcontinuousparameterization. Thefullrefinementobjectiveis:
𝐿“𝜆kp𝐿kp`𝜆proj𝐿proj`𝜆depth𝐿depth`𝜆cont𝐿cont`𝜆reg𝐿reg, (1)
yieldingtheoptimizedtrajectoriestpΘ r ℋ,Θ r 𝒪qu𝑇 .
𝑡 𝑡 𝑡“1
KeypointAlignment. Tokeeptheoptimizedhumantrajectoryalignedwiththegeneratedvideo,weminimize
thedistancebetweenprojectedanddetected2Dbodyandhandkeypoints:
𝐿kp “
𝑇
1
ÿ𝑇 ›
› 𝒦ℋpΘℋ
𝑡
q´𝑝
𝑡
›
› , (2)
𝑡“1
where𝑝 PR𝐽ˆ3 are2Dkeypointsobtainedfrombodyandhandkeypointestimators(Potamiasetal.,2025;
𝑡
Xuetal.,2022),and𝒦ℋp¨qprojectstheSMPL-Xparametersusingtheknowncamera.
ObjectProjectionAlignment. SinceFoundationPoseprovidesimage-alignedobjectposes,weregularizethe
optimizedobjectposetopreservethatalignment:
𝐿proj “
ÿ𝑇 ›
› ›𝒫p𝑉
𝑡
𝒪q´𝒫p𝑉 p
𝑡
𝒪q
›
› ›, (3)
𝑡“1
where𝒫p¨qisthecameraprojectionfunction,and𝑉𝒪 and𝑉 p 𝒪 areobjectverticesundertheoptimizedand
𝑡 𝑡
initialposes.
DepthAlignment. Leveragingtheknown3Dconfiguration,wefirstestimateadepthmapwithMoGe-2(Wang
etal.,2025)andalignittotheground-truthbackgrounddepthrenderedfromtheenvironment,recovering
metric-scaledepth. WethensegmenthumanandobjectregionswithSAM2(Ravietal.,2024)andunproject
5

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
themintoper-framepointcloudsPℋ andP𝒪. Thedepth-alignmentlossencouragesthereconstructedmeshes
𝑡 𝑡
tomatchthesepointclouds:
1
ÿ𝑇
𝐿depth “
𝑇
𝒞𝒟p𝑉
𝑡
ℋ,vis,Pℋ
𝑡
q`𝒞𝒟p𝑉
𝑡
𝒪,vis,P𝒪
𝑡
q, (4)
𝑡“1
where𝑉ℋ,vis and𝑉𝒪,vis arevisiblemeshverticesand𝒞𝒟 isbidirectionalChamferdistance.
𝑡 𝑡
ContactAlignment. Toencouragephysicallyplausiblecontact,wequeryaVLM(OpenAI,2024)onuniformly
sampledvideoframestopredictper-framecontactlabels(e.g.,leftorrighthand)andpropagateeachlabelto
itssurroundinginterval. Usingtheselabels,weidentifytherelevantSMPL-Xvertices𝑉ℋ,cont viaSMPL-Xpart
𝑡
segmentationandapplythecontactlossonlytoframeswherecontactisdetected. Sincetheimage-spacelosses
alreadyenforceprojectionconsistency,thecontactlossonlyneedstoresolvedepthdiscrepancies,sowerestrict
ittoobjectverticeswhoseprojectedpositionsoverlapwiththecontactbodyregionandpenalizeonlytheir
depthoffset:
ÿ
1
𝐿cont “
|𝒯 |
𝒞𝒟
𝑧
p𝑉
𝑡
ℋ,cont,𝑉
𝑡
𝒪,contq, 𝑉
𝑡
𝒪,cont “ℱp𝑉
𝑡
𝒪,𝑉
𝑡
ℋ,contq, (5)
𝑐
𝑡P𝒯𝑐
where𝒯 isthesetofframeswherecontactisdetected. Thefilterℱ projectsbothvertexsetstoscreenspace
𝑐
andkeepstheobjectverticeswhoseprojectionsfallwithinadistancethresholdofthecontactbodyvertices,
and𝒞𝒟 p¨,¨qisadepth-onlybidirectionalChamferdistancethatpenalizesthepositionaldifferencealongthe
𝑧
viewingdirection. 𝐿cont isdisabledforterrain-onlysequenceswithouthand-objectinteraction.
Regularization. Theregularizationtermdecomposesas𝐿reg “𝐿foot`𝐿vel`𝐿smooth . 𝐿foot leveragesper-frame
footcontactlabelsfromGENMO(Lietal.,2025)topenalizefootvertexdisplacementduringdetectedcontact
frames,suppressingfootskating. 𝐿vel regularizestheoptimizedpelvisvelocitytomatchGENMO’sglobal-space
velocity estimate, suppressing the depth-direction oscillations that camera-space estimates exhibit under
depth-scaleambiguity. 𝐿smooth penalizesthefirst-andsecond-ordertemporalfinitedifferencesofthehuman
andobjectmeshvertexpositionsfortemporalcoherence.
3.3. Task-General Loco-Manipulation Tracking
This robot-proportioned reconstruction allows GMR (Araújo et al., 2025) to retarget the SMPL-X motion
tΘ r ℋu𝑇 totheUnitreeG1withreducedmorphologymismatch,betterpreservinghand-objectandbody-scene
𝑡 𝑡“1
contacts. Theresultisakinematicreferencemotiont𝑞ru𝑇 intherobot’sjointspace,whilethereconstructed
𝑡 𝑡“1
objecttrajectorytΘ r 𝒪u𝑇 providesthereferenceobjectpose.WethentraintrackingpoliciesbuiltonSONIC(Luo
𝑡 𝑡“1
etal.,2025),apretrainedwhole-bodycontroller,toconverttheseretargeted4DHOItrajectoriesintorobot-
actiondata. Ratherthanfittingacontrollerpersequenceorperobject,wetraintask-generalpoliciesacross
each task family; as related trajectories are added, existing policies provide initialization for fine-tuning,
amortizingadaptationacrossthepool. AsoutlinedinFig.3,weinstantiatethisstagewithtwocomplementary
specializations: anobject-awarelatentadaptortrainedonobject-manipulationtrajectoriesandascene-aware
trackertrainedonterraintraversalandchair-sittingtrajectories. Theobject-awareadaptoraddshandactions
andmodulatesthelatenttokensfedtothecontroller’sfrozenactiondecoder,enablingmanipulationwhile
preservingthelocomotionprior;thescene-awaretrackerfine-tunesthecontrollerwithaheight-mapencoder,
improvingterrain-conditionedwhole-bodycontrolfortraversalandsceneinteraction.
Object-AwareTracking. Forobject-manipulation4DHOItrajectories,weextendthepretrainedwhole-body
controllerwithanobject-awareadaptorpolicy𝜋 thatmodulatesitslatenttokenspaceandemitshandactions,
𝜑
givingthefrozencontrollerobject-manipulationcapabilitywhilepreservingitspretrainedlocomotionbehavior.
The controller encodes kinematic motion targets into a discrete latent token 𝑧 “ ℰp𝑞rq via finite scalar
𝑡 𝑡
quantization and decodes them into joint-level actions through 𝒢p𝑧 q. We keep its encoder, quantizer, and
𝑡
6

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
Figure3:Task-GeneralTrackingviaComplementaryControllerAdaptation. Retargeted4DHOItrajectories
areconvertedintorobot-actiondatabyadaptingdifferentpartsofapretrainedwhole-bodycontroller. Object-
manipulationtrajectoriesareusedtotrainanobject-awareadaptor𝜋 whilethecontrollerremainsfrozen: the
𝜑
adaptorobservesproprioception𝑠 andanobjectreference𝑜 ,injectsalatentresidual∆𝑧 ,andemitshand
|     | 𝑡   |     | 𝑡   |     | 𝑡   |     |
| --- | --- | --- | --- | --- | --- | --- |
actions𝑎hand. Terraintraversalandchair-sittingtrajectoriesareusedtofine-tunethecontrollerwithascene-
𝑡
awareheightencoder𝜖 : theencodermapsthelocalheightmapℎ intoterraincontextforscene-conditioned
| ℎ   |     |     |     | 𝑡   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
whole-bodycontrol.
decoderfrozen,thentrainonly𝜋 toinjectmanipulation-specificresiduals. Theadaptorobservesproprioception
𝜑
andanobjectreference𝑜 consistingoftheobjectposeinrobotbodyframe,hand-to-objecttransforms,finger
𝑠
𝑡 𝑡
contactforces,aprecomputedbasispointset(BPS)(Prokudinetal.,2019)shapeencoding,and,critically,
deltaobservationsencodingthedifferencebetweenthereferencefutureobjectposeandthecurrentsimulated
pose. Itoutputsa64-dimlatentresidual∆𝑧 togetherwitha2-dimbinaryhandprimitive𝑎hand thatmapsto7
|     |     | 𝑡   |     |     | 𝑡   |     |
| --- | --- | --- | --- | --- | --- | --- |
fingerDoFsperhand:
|     | ,𝑎handq“𝜋 |             | 𝑎body     |             |     | (6) |
| --- | --------- | ----------- | --------- | ----------- | --- | --- |
| p∆𝑧 | 𝑡 𝑡       | 𝜑 p𝑠 𝑡 ,𝑜 𝑡 | q, 𝑡 “𝒢p𝑧 | 𝑡 `𝜆∆𝑧 𝑡 q, |     |     |
with𝜆“0.1scalingtheresidualbeforeFSQquantization. Eachhandprimitiveproducesabinaryopen/close
graspsignal,whichismappedto7fingerjointpositionsperhandviapredefinedgraspconfigurations. The
BPSencodingprovidestheadaptorwithobject-shapeawareness,enablingasingle𝜋 totrackmotionsacross
𝜑
diverseobjectgeometries. Anauxiliaryℓ penaltyisappliedon∆𝑧 toencouragetheadaptedlatenttoremain
|     | 2   |     | 𝑡   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
closetothepretrainedcontroller’sbehavior.
Scene-AwareTracking. Fortasksinvolvingscene-awareinteractions,suchassteppingovercurbs,climbing
upstairs,andsittingonchairs,thecontroller’sflat-groundpriorisnotdirectlyusable. Wethereforefine-tune
thecontrolleronamixtureofreconstructed4DHOIscene-interactiontrajectoriesanditsoriginalflat-ground
data,whileaugmentingtheencoderinputwithalocalheightmapℎ aroundtherobotprocessedbya2D-
𝑡
convolutionalprojector𝜖 . Thispreservesthebaselocomotiondistributionwhileteachingthecontrollerto
ℎ
adaptwhole-bodymotionstoterrainandscenegeometry. Tostabilizethetraining,inadditiontotheaction
decoder𝒢,wetrainaparallelkinematicdecoder𝒢 thatreconstructstheinputmotiontargetstoprovidean
rec
auxiliaryMSElossthatregularizesthelatenttoremainfaithfultothetrajectory.
RewardDesign. Bothtrackersshareamotion-trackingreward𝑅motion thatencouragesthesimulatedrobotto
𝑡
followtheretargetedreference,togetherwithregularizationpenalties𝑅reg (e.g.,actionrateandjointlimits)
𝑡
forsmoothnessandsafety. Themotion-trackingrewardisasumofexponentialtermsoverreference–simulation
discrepancies:
|     |         |         | ˆ     | ˙     |     |     |
| --- | ------- | ------- | ----- | ----- | --- | --- |
|     |         | ÿ       | }𝑥r   |       |     |     |
|     |         |         | ´𝑥    | }2    |     |     |
|     | 𝑅motion | “ 𝑤 exp | ´ 𝑖,𝑡 | 𝑖,𝑡 , |     | (7) |
|     | 𝑡       | 𝑖       | 𝜎2    |       |     |     |
|     |         | 𝑖       | 𝑖     |       |     |     |
where𝑥r and𝑥 arereferenceandsimulatedquantitiesspanningrootpose,per-bodypositionsandorien-
𝑖,𝑡 𝑖,𝑡
7

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
tations,andlinearandangularvelocities;forobject-awaretrackingweadditionallyboosttheweightonthe
wristlinkstoencourageaccuratehandplacement. Forobject-awaretracking,thetotalrewardaddsanobject
|     |     | “𝑅motion`𝑅reg`𝑅obj`⊮t𝐶 |     |     |     | u𝑅grasp,where⊮t𝐶 |     |     |     |
| --- | --- | ---------------------- | --- | --- | --- | ---------------- | --- | --- | --- |
termandacontact-gatedgraspterm,𝑅 uisaper-frame
|     |     | 𝑡 𝑡 |     | 𝑡   | 𝑡   | 𝑡 𝑡 |     | 𝑡   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
contact indicator carried by the reconstructed trajectory, so the grasp reward is active only during contact
phases. Theobjecttrackingrewardpenalizesdeviationfromthereferenceobjectpose:
|      |     | `               |     | ˘   | `   |             | ˘   |     |     |
| ---- | --- | --------------- | --- | --- | --- | ----------- | --- | --- | --- |
| 𝑅obj | “𝑤  | exp ´𝛼 }𝑝r𝒪´𝑝𝒪} |     | `𝑤  | exp | ´𝛼 }𝑟r𝒪a𝑟𝒪} | ,   |     | (8) |
| 𝑡    | 𝑝   | 𝑝               | 𝑡   | 𝑡   | 𝑟   | 𝑟 𝑡         | 𝑡   |     |     |
withscalingcoefficients𝛼 ,𝛼 ą0. Thegrasprewardcombinesthreetermsperhand:
𝑝 𝑟
|     |     | ˆ   |     | ˙   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | “   |     | ‰   |     |     |
𝑁contact
| 𝑅 grasp | “𝑤  | m i n 𝑡                    | , 1 | `𝑤 𝑑l´oooocoooosopo𝑑oo |     | t h u mb oo,oo𝑑oo i | n d e x `       |     |     |
| ------- | --- | -------------------------- | --- | ---------------------- | --- | ------------------- | --------------- | --- | --- |
| 𝑡       | 𝑐   |                            |     |                        |     | 𝑡o oo om 𝑡          | oo o o ooqooo n |     |     |
|         |     | loo o ooooooo𝑁o mmoionoooo | ooo | oon                    |     |                     |                 |     |     |
grasppose
con´tacttime
|     |     |                  | ř                          |     | ¯    |     |     |     |     |
| --- | --- | ---------------- | -------------------------- | --- | ---- | --- | --- | --- | --- |
|     | `   | 𝑤 exp            | ´𝛾 1                       | }𝑓  | ´𝑐 } | .   |     |     | (9) |
|     |     | 𝑓looooooooooo𝑁oo | ooom𝑗ooooo𝑗o,o𝑡ooooooo𝑡oon |     |      |     |     |     |     |
𝑓
contactproximity
The first term rewards sustained finger contact with the object (saturating at contacts), the second
𝑁
min
encouragesthethumbandindexfingertoapproachfromopposingsidesforastablepinchgrasp(𝑑thumb,𝑑index
|     |     |     |     |     |     |     |     | 𝑡   | 𝑡   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
arevectorsfromtheobjectcentertoeachfingertip),andthethirddrawsallfingertips𝑓 towardtheobject
𝑗,𝑡
contactcentroid𝑐 . Sincescene-awaretasksinvolvenohand-objectinteraction,thescene-awaretrackeruses
𝑡
only𝑅motion and𝑅reg.
𝑡 𝑡
We train each stage with PPO (Schulman et al., 2017) in Isaac Lab on 64 NVIDIA L40 GPUs,
Training.
runningfor30,000iterationswith1,024environmentsperGPU.Object-awaretrackingupdatesonly𝜋 while
𝜑
thecontroller’sencoder,quantizer,anddecoderremainfrozen. Scene-awaretrackinginsteadfine-tunesthe
controllertogetherwiththeheight-mapencoder𝜖 . Multiplereferencemotionsaretrainedjointlywithineach
ℎ
taskfamily,withenvironmentssamplingmotionsfromashared4DHOIpool,andweapplyreferencestate
initializationateveryepisodereset.
FullrewarddefinitionsandimplementationdetailsareprovidedinAppendixB.
3.4. Sim-to-Real Deployment
Forsim-to-realdeployment,wedistilltheobject-awareandscene-awaretrackingpoliciesintoseparateegocen-
tricvisualpolicies(Chietal.,2023;Heetal.,2025a;Luoetal.,2025)forobjectpick-upandstair-climbing,
respectively. The deployed models consume head-camera RGB inputs and output the latent tokens of the
SONICcontroller,andaretrainedwithdomainrandomizationtofacilitatesim-to-realtransfer. Todeployon
therealUnitreeG1,weconnecttherobottoadesktopwithanNVIDIARTX5090GPUandstreamvisualand
proprioceptive input to the desktop before streaming robot actions to the G1. We use a Luxonis OAK-D W
cameraontheG1andruninferenceat10Hz.
4. Results
OurexperimentscoverthethreestagesoftheGRAILpipeline. Wefirstevaluatewhetherthegenerated4DHOI
sequencesaremorephysicallyexecutablethanexistinggenerationbaselines. Wethenaskwhetherthese4D
HOIsequencescanbeconvertedintotask-generalloco-manipulationpoliciesatscale,ratherthanonlyreplayed
throughper-sequencetracking. Finally,wedemonstratethepracticalvalueofthegenerateddatabydeploying
egocentricvisualpoliciesontherealrobotforautonomousloco-manipulation.
8

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
Figure 4: Generated Loco-Manipulation Data. Representative simulated Unitree G1 executions from the
generateddatasetspanpick-up,whole-bodymanipulation,sitting,andterraintraversalacrossdiverseobjects
andscenegeometries.
9

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
|     | Geometric | Perceptual | Smoothness |     | PhysicalExecutability |
| --- | --------- | ---------- | ---------- | --- | --------------------- |
Methods ContactÓ Pen.Ó Inter.ScoreÒ HumanSmo.Ó ObjSmo.Ó SRÒ BodyDev.Ó ObjDev.Ó
HOIDiff(Pengetal.,2025) 0.012 2.07% 1.79 0.0043 0.0118 15.8% 0.2120 0.3352
CHOIS(Lietal.,2024) 0.034 3.74% 2.47 0.0055 0.0062 10.5% 0.2564 0.3642
DAViD(Kimetal.,2025a) 0.246 1.46% 2.74 0.0024 0.0605 24.0% 0.4723 0.5826
| Ours | 0.008 0.90% | 3.58 | 0.0033 | 0.0022 | 88.9% 0.0913 0.0851 |
| ---- | ----------- | ---- | ------ | ------ | ------------------- |
Table1:ComparisonofHOIGeneration. Geometricquality,perceptualrealism(InteractionScore,1-5scale),
motionsmoothness,andphysics-basedtrackingontheshared20-objectevaluationset.
|     |     |     | SRÒ ObjPosÓ | MPJPE-LÓ |     |
| --- | --- | --- | ----------- | -------- | --- |
Method
|     | HDMI(Wengetal.,2025)     |     | 48.5% 0.283 | 122.3 |     |
| --- | ------------------------ | --- | ----------- | ----- | --- |
|     | ResMimic(Zhaoetal.,2025) |     | 49.2% 0.393 | 80.9  |     |
|     | Oursw/oSONIC             |     | 45.0% 0.395 | 243.5 |     |
|     | Oursw/o𝜋                 |     | 39.7% 0.303 | 37.1  |     |
𝜑
|     | Oursw/oRel.Obs. |     | 57.9% 0.257 | 43.0 |     |
| --- | --------------- | --- | ----------- | ---- | --- |
|     | Ours(Full)      |     |             | 41.8 |     |
|     |                 |     | 81.4% 0.135 |      |     |
Table2:Task-GeneralLoco-ManipulationTracking. Comparisonagainstloco-manipulationbaselines(top)
and ablations of GRAIL’s object-aware adaptor (bottom). Metrics: success rate (SR), object position error
(ObjPos),andlocalper-jointerror(MPJPE-L).
| 4.1. Human-Object | Interaction | Generation |     |     |     |
| ----------------- | ----------- | ---------- | --- | --- | --- |
Setup. WecomparetheHOIgenerationcomponentofGRAILagainsttraining-based(CHOIS(Lietal.,2024),
HOIDiff(Pengetal.,2025))andtraining-free(DAViD(Kimetal.,2025a))4DHOIgenerationapproachesona
sharedevaluationsetof20everydayobjectsfromComAsset(Kimetal.,2024). Detailedbaselineconfigurations
areprovidedinAppendixC.1.
Metrics. Weevaluatethegenerated4DHOIsequencesalongthreeaxes. (i)Geometricquality: contactdistance
(Contact)istheaveragetop-𝑘 vertex-to-vertexdistancebetweentheSMPL-Xhumansurfaceandtheobject
surface; (Pen.) is the percentage of SMPL-X vertices that interpenetrate the object mesh.
| penetration | ratio |     |     |     |     |
| ----------- | ----- | --- | --- | --- | --- |
(ii)Perceptualrealism: InteractionScore(Inter.Score)isaVLMrating(OpenAI,2024)ofsampledkeyframes
on a 1-5 scale based on physical plausibility and affordance correctness; motion smoothness for the human
(HumanSmo.) andtheobject(ObjSmo.) isthesecond-ordertemporalderivativeoftheirvertextrajectories.
(iii)Physicalexecutability: weapplyInterMimic(Xuetal.,2025),anSMPL-Xhumanoidtrackingframework,
to reproduce each method’s 4D HOI sequences in physics simulation using humanoids built from capsule
primitivesthatconformtotheinputbodyshape(nomotionretargetingrequired). Wereportthefull-body
meanper-jointpositiondeviation(BodyDev.) andthemeanobjectsurfacedeviation(ObjDev.),anddefine
thetrackingsuccessrate(SR)asthefractionofframeswherethenormalizedfull-bodyandobjectdeviations
(dividedbytheobject’smaximumdimension)arebothbelow0.25.
Comparison. AsshowninTable1,GRAILachievesthestrongestperformanceacrossnearlyallmetrics: the
lowestcontactdistanceandpenetrationratio,thehighestinteractionscore,thesmoothestobjecttrajectories,
and, by a large margin, the highest tracking success rate with the lowest body and object deviation. This
confirmsthatthegenerated4DHOIsequencesarebothperceptuallyrealisticandphysicallyexecutable,making
them well-suited for downstream robot learning. We further conduct a user study and present additional
qualitativecomparisonsinAppendixC.1.
10

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
SeenObjects UnseenObjects
Cube Apple TeaBox Carrot WetWipes Avg. SprayCan LintRoller Peach Flashlight MedicineBottle Avg.
SRÒ 100% 60% 100% 70% 90% 84% 100% 50% 90% 80% 80% 80%
Table3:Pick-upresultsforseenandunseenobjects. Successratesarecomputedover10trials.
4.2. Task-General Loco-Manipulation Tracking
ScalingLoco-ManipulationData. Usingtheasset-conditionedgenerationpipeline,wegeneratealarge-scale
loco-manipulationdatasetfortheUnitreeG1with1,000objectassetssourcedfromRobocasa(Nasirianyetal.,
2024),ComAsset(Kimetal.,2024),OMOMO(Lietal.,2023a),andHunyuan3D(Team,2025),pairedwith
1,000procedurallygeneratedterrainconfigurations. Theresultingdatasetcontainsover20,000sequences
(Fig.4)spanningfourcategories. Pick-upcoverstabletopsandtheground,exercisingdiversegraspstrategies
acrossvaryingobjectshapesandplacementheights. Whole-bodymanipulationcoverstabletopmanipulation
motionsandmobileinteractionsinwhichtherobotcarries,pushes,orrepositionslargeritemssuchasboxes
andcartswhilewalking. Sittingspansdiversechairstyles,requiringapproach,lower-bodyadjustment,and
settlingintoaseatedposture. Terraintraversalcoversprocedurallygeneratedcurbs,slopes,andstairs,asetting
essentialforreal-worlddeploymentbutunderrepresentedinexistingdatasets.
BaselineComparison. Wecompareourmethodagainsttworecenthumanoidloco-manipulationbaselines,
HDMI (Weng et al., 2025) and ResMimic (Zhao et al., 2025), using their official implementations on a
benchmarkof124motionsacross43objects. Wereportmanipulationsuccessrate(SR),objectpositionerror
(ObjPos),andlocalmeanper-jointpositionerror(MPJPE-L);SRisthefractionofepisodeswheretheaverage
objectpositionerrorfallsbelow20cm. Bothtrainwhole-bodytrackingpoliciesfromhumanreferencesbut
differfromourapproachintwokeyways. First,neithermethodactuatesper-fingerDoFs,sotheirevaluated
interactionsrelyonwhole-armorwhole-bodycontactsuchascarrying, lifting, andpushing. Second, both
trainaseparatepolicypertask: ResMimictrainsaper-taskresidualontopofageneralmotion-trackingbase,
whileHDMItrainsonespecialistpolicypertask. Incontrast,GRAILtrainstask-generalpoliciesacrosslarge
in-familypoolsof4DHOItrajectories. AsshowninthetopblockofTable2,GRAILoutperformsthebaselines
byalargemarginacrosssuccessrate,objectpositionerror,andbodytrackingaccuracy.
AblationStudy. Weablatetheobject-awarelatentadaptorformanipulationcasesonthesamebenchmarkand
reportresultsinTable2(bottomblock). RemovingSONICandtrainingfromscratchsubstantiallydegrades
bodytrackingandreducessuccessrate. Disablingthelatentadaptor𝜋 (i.e.,vanillaSONIC)yieldsthelowest
𝜑
manipulation success rate despite the best body tracking, indicating that accurate body imitation alone is
insufficient for object interaction. Replacing relative object observations with absolute ones also decreases
successrate.
4.3. Sim-to-Real Deployment
TodemonstrateGRAIL’sreal-worldapplicability,wedeploytrainedegocentricvisualpoliciesforstair-climbing
and diverse object pick-up. For stair-climbing, a policy trained on diverse terrain-traversal sequences from
GRAILachievesa90%real-worldsuccessrate,asshowninFig.5. Forobjectpick-up,wetrainon200approach-
and-pick-upsequencesperobjectacrosscubes,apples,teaboxes,carrots,andwetwipes. Theresultingpolicy
achieves an 84% real-world success rate, as shown in Table 3, and transfers effectively to unseen objects,
attainingan80%successrate.
5. Conclusion
WepresentedGRAIL,afullydigitalpipelineforgeneratinghumanoidloco-manipulationdatafrom3Dassets
andvideopriors,requiringthephysicalrobotandenvironmentonlyatdeployment. Insteadofreconstructing
11

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
Figure5:Sim-to-RealDeployment. EgocentricvisualpoliciestrainedonlyonGRAIL-generateddatatransfer
toaUnitreeG1forobjectpick-upandstair-climbing.
uncontrolledvideos,GRAILstartsfromfullyspecified3Dsceneswhereobjectgeometryandtexture,camera
parameters,metricscale,environmentdepth,androbot-proportionedmorphologyareavailablebyconstruction.
Thisprivilegedsetupturnskeyambiguitiesin4DHOIreconstructionintocontrolledinputs,enablingmodel-
basedobjecttracking,metricdepthalignment,andinteraction-awareoptimizationtorecoverrobot-compatible
trajectories. TherecoveredmotionsareretargetedtotheUnitreeG1andconvertedintocomplementarytask-
generaltrackers: object-awarelatentadaptationformanipulationandscene-awareheight-mapconditioningfor
terraintraversalandsitting. Fromover20,000generatedsequences,wetrainegocentricvisualpoliciesusing
onlyGRAIL-generateddataanddeploythemonarealG1,achieving84%pick-upsuccessacrossdiverseobjects
and90%stair-climbingsuccess. Theseresultssuggestthatasset-conditionedgenerativedatacancomplement
teleoperationandmotioncaptureasascalableroutetowardhumanoidloco-manipulation.
6. Limitations
Ourpipelineassumes3Dobjectassets,simulator-readyscenesetup,andavideofoundationmodelthatfollows
therequestedinteraction. Reconstructionqualitydegradesundersevereocclusion,fastmotion,orinconsistent
object appearance from the VFM, and the failure-filtering step discards a non-trivial fraction of sequences.
Thetask-generaltrackingpoliciesamortizelearningoverrelated4DHOIpools,butstillrequiretrainingor
fine-tuningwhenthemotionfamilychangessubstantially.
12

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
References
JorgeAldaco,TravisArmstrong,RobertBaruch,JeffBingham,SankyChan,KennethDraper,DebidattaDwibedi,
ChelseaFinn,PeteFlorence,SpencerGoodrich,etal.ALOHA2:Anenhancedlow-costhardwareforbimanual
teleoperation. arXivpreprintarXiv:2405.02292,2024. 2
ArthurAllshire,HongsukChoi,JunyiZhang,DavidMcAllister,AnthonyZhang,ChungMinKim,TrevorDarrell,
PieterAbbeel,JitendraMalik,andAngjooKanazawa. Visualimitationenablescontextualhumanoidcontrol.
arXivpreprintarXiv:2505.03729,2025. 3
João Pedro Araújo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion
retargetingforhumanoidmotiontracking,2025. URLhttps://arxiv.org/abs/2510.02252. ICRA2026. 6
QingweiBen, FeiyuJia, JiaZeng, JuntingDong, DahuaLin, andJiangmiaoPang. Homie: Humanoidloco-
manipulationwithisomorphicexoskeletoncockpit. arXivpreprintarXiv:2502.13013,2025. 2,3
BharatLalBhatnagar,XianghuiXie,IlyaPetrov,CristianSminchisescu,ChristianTheobalt,andGerardPons-Moll.
BEHAVE:Datasetandmethodfortrackinghumanobjectinteractions. InCVPR,2022. 3
ChengChi,SiyuanFeng,YilunDu,ZhenjiaXu,EricCousineau,BenjaminBurchfiel,andShuranSong. Diffusion
policy: Visuomotorpolicylearningviaactiondiffusion. InProceedingsofRobotics: ScienceandSystems(RSS),
2023. 8
LingweiDang,RuizhiShao,HongwenZhang,WeiMin,YebinLiu,andQingyaoWu. SViMo: Synchronized
diffusionforvideoandmotiongenerationinhand-objectinteractionscenarios. InNeurIPS,2025. 3
Christian Diller and Angela Dai. Cg-hoi: Contact-guided 3d human-object interaction generation. In Proc.
ComputerVisionandPatternRecognition(CVPR),IEEE,2024. 3
SaiKumarDwivedi,DimitrijeAntić,ShashankTripathi,OmidTaheri,CordeliaSchmid,MichaelJBlack,and
DimitriosTzionas. Interactvlm: 3dinteractionreasoningfrom2dfoundationalmodels. InProceedingsofthe
ComputerVisionandPatternRecognitionConference,pages22605–22615,2025. 3
ZicongFan,OmidTaheri,DimitriosTzionas,MuhammedKocabas,ManuelKaufmann,MichaelJ.Black,and
OtmarHilliges. ARCTIC:Adatasetfordexterousbimanualhand-objectmanipulation. InCVPR,2023. 3
ZipengFu,QingqingZhao,QiWu,GordonWetzstein,andChelseaFinn. HumanPlus: Humanoidshadowing
andimitationfromhumans. InConferenceonRobotLearning(CoRL),2024. 3
TairanHe,ZhengyiLuo,XialinHe,WenliXiao,ChongZhang,WeinanZhang,KrisKitani,ChangliuLiu,and
GuanyaShi.OmniH2O:Universalanddexteroushuman-to-humanoidwhole-bodyteleoperationandlearning.
InConferenceonRobotLearning(CoRL),2024. 3
Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando
Castañeda,ShankarSastry,etal. Viral: Visualsim-to-realatscaleforhumanoidloco-manipulation. arXiv
preprintarXiv:2511.15200,2025a. 3,8
TairanHe,WenliXiao,ToruLin,ZhengyiLuo,ZhenjiaXu,ZhenyuJiang,JanKautz,ChangliuLiu,Guanya
Shi,XiaolongWang,LinxiFan,andYukeZhu. HOVER:Versatileneuralwhole-bodycontrollerforhumanoid
robots. InIEEEInternationalConferenceonRoboticsandAutomation(ICRA),2025b. 3
XialinHe,SiruiXu,XinyaoLi,RunpeiDong,LiuyuBian,Yu-XiongWang,andLiang-YanGui. Ultra: Unifiedmul-
timodalcontrolforautonomoushumanoidwhole-bodyloco-manipulation. arXivpreprintarXiv:2603.03279,
2026. 3
13

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
ZhiHou,BaoshengYu,andDachengTao. Compositional3dhuman-objectneuralanimation. arXivpreprint
| arXiv:2304.14070,2023. |     | 2,3 |     |     |
| ---------------------- | --- | --- | --- | --- |
YinghaoHuang,OmidTaheri,MichaelJ.Black,andDimitriosTzionas. InterCap: Jointmarkerless3Dtracking
| ofhumansandobjectsininteraction. |     |     | InGCPR,2022. | 3   |
| -------------------------------- | --- | --- | ------------ | --- |
HaoranJiang,JinChen,QingwenBu,LiChen,ModiShi,YanjieZhang,DelongLi,ChuanzheSuo,Chuang
Wang,ZhihuiPeng,andHongyangLi. WholeBodyVLA:TowardsunifiedlatentVLAforwhole-bodyloco-
| manipulationcontrol. |     | InICLR,2026. | 3   |     |
| -------------------- | --- | ------------ | --- | --- |
Nan Jiang, Tengyu Liu, Zhexuan Cao, Jieming Cui, Zhiyuan Zhang, Yixin Chen, He Wang, Yixin Zhu, and
SiyuanHuang. Full-bodyarticulatedhuman-objectinteraction. InICCV,2023. 3
NanJiang,ZhiyuanZhang,HongjieLi,XiaoxuanMa,ZanWang,YixinChen,TengyuLiu,YixinZhu,andSiyuan
Huang. Scalingupdynamichuman-sceneinteractionmodeling. InProceedingsoftheIEEE/CVFConference
onComputerVisionandPatternRecognition,pages1737–1747,2024. 3
Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti,
SoroushNasiriany,MohanKumarSrirama,LawrenceYunliangChen,KirstyEllis,etal. DROID:Alarge-scale
in-the-wildrobotmanipulationdataset. arXivpreprintarXiv:2403.12945,2024. 2,3
HyeonwooKim,SookwanHan,PatrickKwon,andHanbyulJoo.Beyondthecontact:Discoveringcomprehensive
affordancefor3Dobjectsfrompre-trained2Ddiffusionmodels. InEuropeanConferenceonComputerVision,
| pages400–419.Springer,2024. |     |     | 10,11 |     |
| --------------------------- | --- | --- | ----- | --- |
HyeonwooKim,SangwonBaik,andHanbyulJoo. David: Modelingdynamicaffordanceof3dobjectsusing
pre-trainedvideodiffusionmodels. InProceedingsoftheIEEE/CVFInternationalConferenceonComputer
| Vision,pages10330–10341,2025a. |     |     | 3,10,22,23 |     |
| ------------------------------ | --- | --- | ---------- | --- |
JeonghwanKim,JisooKim,JeonghyeonNa,andHanbyulJoo. ParaHome: Parameterizingeverydayhome
activitiestowards3dgenerativemodelingofhuman-objectinteractions. InCVPR,2025b. 3
TaeksooKim,ShunsukeSaito,andHanbyulJoo. NCHO:Unsupervisedlearningforneural3dcompositionof
| humansandobjects. |     | InICCV,2023. | 2,3 |     |
| ----------------- | --- | ------------ | --- | --- |
Kuaishou. Klingaivideogenerator(image-to-videomodel),2025. URLhttps://klingai.com/. Version2.1,
| image-to-videogenerativemodel. |     |     | 4,19 |     |
| ------------------------------ | --- | --- | ---- | --- |
NileshKulkarni,DavisRempe,KyleGenova,AbhijitKundu,JustinJohnson,DavidFouhey,andLeonidasGuibas.
Nifty: Neuralobjectinteractionfieldsforguidedhumanmotionsynthesis. InProceedingsoftheIEEE/CVF
ConferenceonComputerVisionandPatternRecognition(CVPR),pages947–957,June2024. 3
Black Forest Labs, Stephen Batifol, Andreas Blattmann, Frederic Boesel, Saksham Consul, Cyril Diagne,
Tim Dockhorn, Jack English, Zion English, Patrick Esser, Sumith Kulal, Kyle Lacey, Yam Levi, Cheng Li,
Dominik Lorenz, Jonas Müller, Dustin Podell, Robin Rombach, Harry Saini, Axel Sauer, and Luke Smith.
Flux.1 kontext: Flow matching for in-context image generation and editing in latent space, 2025. URL
| https://arxiv.org/abs/2506.15742. |     |     | 22  |     |
| --------------------------------- | --- | --- | --- | --- |
HongjieLi,Hong-XingYu,JiamanLi,andJiajunWu. Zerohsi: Zero-shot4dhuman-sceneinteractionbyvideo
| generation. | In3DV,2026. | 3   |     |     |
| ----------- | ----------- | --- | --- | --- |
JiamanLi,JiajunWu,andCKarenLiu. Objectmotionguidedhumanmotionsynthesis. ACMTransactionson
| Graphics(TOG),42(6):1–11,2023a. |     |     | 3,11 |     |
| ------------------------------- | --- | --- | ---- | --- |
Jiaman Li, Alexander Clegg, Roozbeh Mottaghi, Jiajun Wu, Xavier Puig, and C. Karen Liu. Controllable
| human-objectinteractionsynthesis. |     |     | InECCV,2024. | 3,10,22,23 |
| --------------------------------- | --- | --- | ------------ | ---------- |
14

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
Jiefeng Li, Jinkun Cao, Haotian Zhang, Davis Rempe, Jan Kautz, Umar Iqbal, and Ye Yuan. GENMO: A
GENeralistmodelforhumanMOtion. InProceedingsoftheIEEE/CVFInternationalConferenceonComputer
Vision,2025. 5,6
LeiLiandAngelaDai. Genzi: Zero-shot3dhuman-sceneinteractiongeneration. InProceedingsoftheIEEE/CVF
ConferenceonComputerVisionandPatternRecognition,pages20465–20474,2024. 3
QuanzhouLi,JingboWang,ChenChangeLoy,andBoDai. Task-orientedhuman-objectinteractionsgeneration
withimplicitneuralrepresentations. arXivpreprintarXiv:2303.13129,2023b. 3
YukeLou,YimingWang,ZhenWu,RuiZhao,WenjiaWang,MingyiShi,andTakuKomura. Zero-shothuman-
objectinteractionsynthesiswithmultimodalpriors. arXivpreprintarXiv:2503.20118,2025. 3
JiaxinLu,Chun-HaoPaulHuang,UttaranBhattacharya,QixingHuang,andYiZhou. Humoto: A4ddatasetof
mocaphumanobjectinteractions. arXivpreprintarXiv:2504.10414,2025. 2,3
ZhengyiLuo,JinkunCao,AlexanderWinkler,KrisKitani,andWeipengXu. Perpetualhumanoidcontrolfor
real-time simulated avatars. In Proceedings of the IEEE/CVF International Conference on Computer Vision,
pages10895–10904,2023. 3
ZhengyiLuo,YeYuan,TingwuWang,ChenranLi,SiruiChen,FernandoCastañeda,Zi-AngCao,JiefengLi,
DavidMinor,QingweiBen,etal. SONIC:Supersizingmotiontrackingfornaturalhumanoidwhole-body
control. arXivpreprintarXiv:2511.07820,2025. 2,3,6,8,19
Miles Macklin, Matthias Müller, and Nuttapong Chentanez. Xpbd: position-based simulation of compliant
constraineddynamics. InProceedingsofthe9thInternationalConferenceonMotioninGames,pages49–54,
2016. 4
JiagengMao,SihengZhao,SiqiSong,TianhengShi,JunjieYe,MingtongZhang,HaoranGeng,JitendraMalik,
VitorGuizilini,andYueWang. Learningfrommassivehumanvideosforuniversalhumanoidposecontrol,
2024. URLhttps://arxiv.org/abs/2412.14172. 3
RuiqianNai,BoyuanZheng,JunmingZhao,HaodongZhu,SicongDai,ZunhaoChen,YihangHu,Yingdong
Hu,TongZhang,ChuanWen,andYangGao. HuMI:Humanoidwhole-bodymanipulationfromrobot-free
demonstrations,2026. URLhttps://arxiv.org/abs/2602.06643. 3
SoroushNasiriany,AbhiramMaddukuri,LanceZhang,AdeetParikh,AaronLo,AbhishekJoshi,AjayMandlekar,
and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. arXiv preprint
arXiv:2406.02523,2024. 11
OpenAI. Chatgpt. https://chat.openai.com/,2024. Largelanguagemodelusedfortextgenerationand
editing. 4,6,10,19
Shivansh Patel, Shraddhaa Mohan, Hanlin Mai, Unnat Jain, Svetlana Lazebnik, and Yunzhu Li. Robotic
manipulationbyimitatinggeneratedvideoswithoutphysicaldemonstrations,2025. URLhttps://arxiv.
org/abs/2507.00990. 3
GeorgiosPavlakos,VasileiosChoutas,NimaGhorbani,TimoBolkart,AhmedAAOsman,DimitriosTzionas,and
MichaelJBlack. Expressivebodycapture: 3Dhands,face,andbodyfromasingleimage. InProceedingsof
theIEEE/CVFconferenceoncomputervisionandpatternrecognition,pages10975–10985,2019. 5
XiaogangPeng,YimingXie,ZizhaoWu,VarunJampani,DeqingSun,andHuaizuJiang. Hoi-diff: Text-driven
synthesis of 3d human-object interactions using diffusion models. In CVPR 2025 Workshop of HuMoGen,
2025. 3,10,22,23
15

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
XueBinPeng,PieterAbbeel,SergeyLevine,andMichielVandePanne. Deepmimic: Example-guideddeep
reinforcementlearningofphysics-basedcharacterskills. ACMTransactionsOnGraphics(TOG),37(4):1–14,
2018. 3
XueBinPeng,ZeMa,PieterAbbeel,SergeyLevine,andAngjooKanazawa. Amp: Adversarialmotionpriorsfor
stylizedphysics-basedcharactercontrol. ACMTransactionsonGraphics(ToG),40(4):1–20,2021. 3
IlyaAPetrov,RiccardoMarin,JulianChibane,andGerardPons-Moll. Objectpop-up: Canweinfer3dobjects
andtheirposesfromhumaninteractionsalone? InCVPR,2023. 2,3
Rolandos Alexandros Potamias, Jinglei Zhang, Jiankang Deng, and Stefanos Zafeiriou. Wilor: End-to-end
3d hand localization and reconstruction in-the-wild. In Proceedings of the Computer Vision and Pattern
RecognitionConference,pages12242–12254,2025. 5
SergeyProkudin,ChristophLassner,andJavierRomero. Efficientlearningonpointcloudswithbasispointsets.
InProceedingsoftheIEEE/CVFinternationalconferenceoncomputervision,pages4332–4341,2019. 7
AlexanderRaistrick,LahavLipson,ZeyuMa,LingjieMei,MingzheWang,YimingZuo,KarhanKayan,Hongyu
Wen, Beining Han, Yihan Wang, et al. Infinite photorealistic worlds using procedural generation. In
ProceedingsoftheIEEE/CVFconferenceoncomputervisionandpatternrecognition,pages12630–12641,2023.
4,19
Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr,
RomanRädle,ChloeRolland,LauraGustafson,etal. Sam2: Segmentanythinginimagesandvideos. arXiv
preprintarXiv:2408.00714,2024. 5,19
JavierRomero,DimitriosTzionas,andMichaelJBlack. Embodiedhands: modelingandcapturinghandsand
bodiestogether. ACMTransactionsonGraphics(TOG),36(6):1–17,2017. 5
Abraham Savitzky and Marcel JE Golay. Smoothing and differentiation of data by simplified least squares
procedures. Analyticalchemistry,36(8):1627–1639,1964. 5
JohnSchulman,FilipWolski,PrafullaDhariwal,AlecRadford,andOlegKlimov. Proximalpolicyoptimization
algorithms. arXivpreprintarXiv:1707.06347,2017. 8,20
ModiShi,ShijiaPeng,JinChen,HaoranJiang,YinghuiLi,DiHuang,PingLuo,HongyangLi,andLiChen.
Egohumanoid: Unlockingin-the-wildloco-manipulationwithrobot-freeegocentricdemonstration,2026.
URLhttps://arxiv.org/abs/2602.10106. 3
OmidTaheri,NimaGhorbani,MichaelJBlack,andDimitriosTzionas. Grab: Adatasetofwhole-bodyhuman
graspingofobjects. InEuropeanconferenceoncomputervision,pages581–600.Springer,2020. 2,3
TencentHunyuan3DTeam. Hunyuan3d2.1: Fromimagestohigh-fidelity3dassetswithproduction-readypbr
material,2025. 11
RuichengWang,SichengXu,YueDong,YuDeng,JianfengXiang,ZelongLv,GuangzhongSun,XinTong,and
JiaolongYang. Moge-2: Accuratemonoculargeometrywithmetricscaleandsharpdetails. arXivpreprint
arXiv:2507.02546,2025. 5,19
Xi Wang, Gen Li, Yen-Ling Kuo, Muhammed Kocabas, Emre Aksan, and Otmar Hilliges. Reconstructing
action-conditionedhuman-objectinteractionsusingcommonsenseknowledgepriors. In3DV,2022. 2,3
YinhuaiWang, QihanZhao, YuenFuiLau, RunyiYu, HokWaiTsui, QifengChen, JingboWang, Jiangmiao
Pang, and Ping Tan. HumanX: Toward agile and generalizable humanoid interaction skills from human
videos,2026. URLhttps://arxiv.org/abs/2602.02473. 3
16

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
BowenWen,WeiYang,JanKautz,andStanBirchfield.Foundationpose:Unified6dposeestimationandtracking
ofnovelobjects. InProceedingsoftheIEEE/CVFConferenceonComputerVisionandPatternRecognition,pages
17868–17879,2024. 5
Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and
GuanyaShi. HDMI: Learning interactive humanoid whole-bodycontrol fromhuman videos, 2025. URL
https://arxiv.org/abs/2509.16757. 3,10,11
ZhenWu,JiamanLi,PeiXu,andCKarenLiu. Human-objectinteractionfromhuman-levelinstructions. In
ProceedingsoftheIEEE/CVFInternationalConferenceonComputerVision,pages11176–11186,2025. 3
XianghuiXie,BharatLalBhatnagar,andGerardPons-Moll. Chore: Contact,humanandobjectreconstruction
fromasinglergbimage. InECCV,2022. 2,3
XianghuiXie,BowenWen,YanChang,HesamRabeti,JiefengLi,YeYuan,GerardPons-Moll,andStanBirchfield.
CARI4D:Categoryagnostic4Dreconstructionofhuman-objectinteraction. InCVPR,2026. 2,3
SiruiXu,ZhengyuanLi,Yu-XiongWang,andLiang-YanGui. Interdiff: Generating3dhuman-objectinteractions
withphysics-informeddiffusion. InProceedingsoftheIEEE/CVFInternationalConferenceonComputerVision
(ICCV),pages14928–14940,October2023. 3
Sirui Xu, Ziyin Wang, Yu-Xiong Wang, and Liang-Yan Gui. Interdreamer: Zero-shot text to 3d dynamic
human-objectinteraction. InNeurIPS,2024. 3
SiruiXu,HungYuLing,Yu-XiongWang,andLiang-YanGui. Intermimic: Towardsuniversalwhole-bodycontrol
forphysics-basedhuman-objectinteractions. InProceedingsoftheComputerVisionandPatternRecognition
Conference,pages12266–12277,2025. 10
Yufei Xu, Jing Zhang, Qiming Zhang, and Dacheng Tao. Vitpose: Simple vision transformer baselines for
humanposeestimation. Advancesinneuralinformationprocessingsystems,35:38571–38584,2022. 5
Pei Yang, Hai Ci, Yiren Song, and Mike Zheng Shou. X-Humanoid: Robotize human videos to generate
humanoidvideosatscale,2025. URLhttps://arxiv.org/abs/2512.04537. 3
YufeiYe,XuetingLi,AbhinavGupta,ShaliniDeMello,StanBirchfield,JiamingSong,ShubhamTulsiani,and
SifeiLiu. Affordancediffusion: Synthesizinghand-objectinteractions. InCVPR,2023. 3
Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C. Karen Liu, and Jiajun Wu. VisualMimic: Visual humanoid loco-
manipulationviamotiontrackingandgeneration,2025. URLhttps://arxiv.org/abs/2509.20322. 3
JustinYu,LetianFu,HuangHuang,KarimEl-Refai,RaresAndreiAmbrus,RichardCheng,MuhammadZubair
Irshad, and Ken Goldberg. Real2render2real: Scaling robot data without dynamics simulation or robot
hardware. InConferenceonRobotLearning(CoRL),2025. 3
YanjieZe,ZixuanChen,JoaoPedroAraújo,Zi-angCao,XueBinPeng,JiajunWu,andC.KarenLiu. TWIST:
Teleoperatedwhole-bodyimitationsystem. InConferenceonRobotLearning(CoRL),2025a. 2,3
YanjieZe,SihengZhao,WeizhuoWang,AngjooKanazawa,RockyDuan,PieterAbbeel,GuanyaShi,JiajunWu,
andC.KarenLiu. TWIST2: Scalable,portable,andholistichumanoiddatacollectionsystem. arXivpreprint
arXiv:2511.02832,2025b. 2,3
HuiZhang,SammyChristen,ZicongFan,LuochengZheng,JeminHwangbo,JieSong,andOtmarHilliges.
ArtiGrasp: Physicallyplausiblesynthesisofbi-manualdexterousgraspingandarticulation. arXivpreprint
arXiv:2309.03891,2023a. 3
17

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
JasonY.Zhang,SamPepose,HanbyulJoo,DevaRamanan,JitendraMalik,andAngjooKanazawa. Perceiving
3dhuman-objectspatialarrangementsfromasingleimageinthewild. InEuropeanConferenceonComputer
Vision(ECCV),2020. 2,3
JinluZhang,YixinChen,ZanWang,JieYang,YizhouWang,andSiyuanHuang. Interactanything: Zero-shot
humanobjectinteractionsynthesisviallmfeedbackandobjectaffordanceparsing. InCVPR,2025. 3
JuzeZhang,HaiminLuo,HongdiYang,XinruXu,QianyangWu,YeShi,JingyiYu,LanXu,andJingyaWang.
NeuralDome: Aneuralmodelingpipelineonmulti-viewhuman-objectinteractions. InCVPR,2023b. 3
ChengfengZhao,JuzeZhang,JiashenDu,ZiweiShan,JunyeWang,JingyiYu,JingyaWang,andLanXu. I’M
HOI:Inertia-awaremonocularcaptureof3dhuman-objectinteractions. InCVPR,2024. 3
Siheng Zhao, Yanjie Ze, Yue Wang, C. Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. ResMimic:
Fromgeneralmotiontrackingtohumanoidwhole-bodyloco-manipulationviaresiduallearning,2025. URL
https://arxiv.org/abs/2510.05070. 3,10,11
JuntianZheng,QingyuanZheng,LixingFang,YunLiu,andLiYi. CAMS:Canonicalizedmanipulationspaces
forcategory-levelfunctionalhand-objectmanipulationsynthesis. InCVPR,2023. 3
KeyangZhou,BharatLalBhatnagar,JanEricLenssen,andGerardPons-Moll. TOCH:Spatio-temporalobject-
to-handcorrespondenceformotionrefinement. InECCV,2022. 3
YiZhou,ConnellyBarnes,JingwanLu,JimeiYang,andHaoLi. Onthecontinuityofrotationrepresentations
inneuralnetworks. InProceedingsoftheIEEE/CVFconferenceoncomputervisionandpatternrecognition,
pages5745–5753,2019. 5
18

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
| A. Human-Object |            | Interaction | Generation | Details |     |     |     |
| --------------- | ---------- | ----------- | ---------- | ------- | --- | --- | --- |
| A.1. Video      | Generation |             |            |         |     |     |     |
WeconstructtwocandidatesceneconfigurationsusingInfinigen(Raistricketal.,2023): anindoorfloor-only
environment and a furnished room with a table (Fig. 6). For each input object, a VLM (OpenAI, 2024)
determineswhetheritshouldbeplacedonthefloor(e.g.,asofa)oronthetable(e.g.,afrypan)basedonits
typicalaffordances. WepairtheobjectwithahumanassetprefittedtotheUnitreeG1’smorphology,renderthe
initialframe,anduseaVLM(OpenAI,2024)togenerateatextpromptdescribingtheintendedinteraction.
TherenderedframeandpromptarethenpassedtoKling2.5TurboPro(Kuaishou,2025),whichsupports
generating5or10secondvideosat24fpswithresolutionof1920ˆ1080. Wecanoptionallyrenderanending
frametocontrolthefinalpositionsofthehumanandobject,andproducelongersequencesauto-regressively
byfeedingthelastframeofeachsegmentastheinitialframeofthenext.
| A.2. Generation |     | Runtime |     |     |     |     |     |
| --------------- | --- | ------- | --- | --- | --- | --- | --- |
Table4reportsthewall-clocktimeforeachstageofthe4D
|     |     |     |     |     | Stage |     | Time |
| --- | --- | --- | --- | --- | ----- | --- | ---- |
HOIgenerationpipelinepersequence(a5-secondvideoat
|     |     |     |     |     | VideoGeneration(KlingAPI) |     | „1min |
| --- | --- | --- | --- | --- | ------------------------- | --- | ----- |
24fps,121frames),measuredonasingleNVIDIAA100
|     |     |     |     |     | HumanMotionEstimation |     | „2min |
| --- | --- | --- | --- | --- | --------------------- | --- | ----- |
GPU.Thefullpipelinetakesapproximately14minutesper
|           |                                           |     |     |     | ObjectPoseTracking        |     | „1min |
| --------- | ----------------------------------------- | --- | --- | --- | ------------------------- | --- | ----- |
| sequence. | Videogenerationandinitialmotionestimation |     |     |     |                           |     |       |
|           |                                           |     |     |     | OptimizationPreprocessing |     | „2min |
(humanandobject)togetheraccountforabout4minutes.
|     |     |     |     |     | JointOptimization |     | „8min |
| --- | --- | --- | --- | --- | ----------------- | --- | ----- |
Theoptimizationpreprocessingstage,whichrunsMoGe-
„14min
Total
| 2 (Wang | et al., 2025) | for metric | depth estimation | and |     |     |     |
| ------- | ------------- | ---------- | ---------------- | --- | --- | --- | --- |
SAM2(Ravietal.,2024)forhumanandobjectsegmen-
Table4:RuntimeBreakdown.Wall-clocktimeper
tationtoproduceper-framepointcloudsasoptimization
|     |     |     |     |     | stage of the GRAIL 4D HOI | generation | pipeline, |
| --- | --- | --- | --- | --- | ------------------------- | ---------- | --------- |
targets,takesroughly2minutes. Thejointoptimization measuredonasingleNVIDIAA100GPUfora5-
second,121-framesequence.
stagedominatesatapproximately8minutes,asitjointly
optimizeshumanandobjecttrajectoriesacrossallframes.
| A.3. Failure | Case | Filtering |     |     |     |     |     |
| ------------ | ---- | --------- | --- | --- | --- | --- | --- |
Whileimage-to-videomodelsproducerealisticHOIsequences,theymayintroduceartifactssuchastexturein-
consistenciesorgeometrymismatchesacrossframes,causingFoundationPosetolosetracking. Toautomatically
x
filtersuchfailures,wecompareSAM2(Ravietal.,2024)objectmaskstℳ u𝑇 againstrenderedsilhouettes
𝑡 𝑡“1
fromthepredictedposes,andcomputethemasktrackingerror:
tℳ u𝑇
𝑡 𝑡“1
|     |     |     |     | ´   | ¯   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
x
|     |     |     | ÿ𝑇  | Sum p1´ℳ | q¨ℳ |     |     |
| --- | --- | --- | --- | -------- | --- | --- | --- |
𝑡 𝑡
|     |     |     | 𝑒ℳ “ |     | ,   |     | (10) |
| --- | --- | --- | ---- | --- | --- | --- | ---- |
Sumpℳ
𝑡 q
𝑡“1
whereSump¨qcountsnon-zeropixels. ThismeasuresthefractionofSAM2-trackedmaskpixelsnotcoveredby
thepredictedmask. Wediscardsequenceswhere𝑒ℳ exceeds𝜏 “0.2,effectivelyremovingcasescausedby
fastmotion,blurryframes,orinconsistentobjectappearance.
| B. Task-General |     | Loco-Manipulation |     | Tracking | Details |     |     |
| --------------- | --- | ----------------- | --- | -------- | ------- | --- | --- |
We train two physics-based tracking policies on top of SONIC (Luo et al., 2025), a pretrained whole-body
controller: anobject-awareadaptorformanipulation4DHOItrajectoriesandascene-awaretrackerforterrain-
and chair-conditioned 4D HOI trajectories. Per-tracker policy observations are summarized in Table 5 and
rewardtermsinTable6.
19

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
Figure6:CandidateSceneConfigurations. Twopre-built3Dscenetemplatesusedtoplaceobjects: anindoor
floor-onlyenvironmentforground-levelobjects(e.g.,asofa),andafurnishedroomwithatablefortabletop
objects(e.g.,afrypan). AVLMselectsbetweenthetwobasedoneachobject’stypicalaffordances.
B.1. Object-Aware Adaptor
Architecture. The adaptor policy 𝜋 is a 3-layer MLP with hidden dimensions r512,256,128s and SiLU
𝜑
activations. Itoutputsa66-dimmeta-action: 64dimsforthelatentresidual(matchingthecontroller’stoken
dimof2ˆ32)and2dimsforleft/righthandprimitives. Theresidualisscaledby𝜆“0.1andaddedtothe
controller’sencoderoutputbeforefinitescalarquantization,thendecodedto29bodyjointpositiontargets.
Eachhandprimitiveispassedthroughasigmoidandthresholdedtoabinaryopen/closesignal,mappedto
7 finger joint positions per hand via predefined grasp configurations. The critic is a separate 3-layer MLP
r512,256,128sthatreceivesprivilegedobservationsincludingfullbodystateandground-truthcontactflags.
Training. We train 𝜋 with PPO (Schulman et al., 2017) on 64 NVIDIA L40 GPUs with 1,024 parallel
𝜑
environmentsperGPUinIsaacLabfor30,000iterations;thepretrainedencoder,FSQquantizer,anddecoder
remainfrozenandonly𝜋 isupdated. Environmentssamplereferencemotionsfromasharedtask-family4D
𝜑
HOIpool,andweapplyreferencestateinitializationateveryepisodereset:thestartframeissampleduniformly
fromthefirst30framesandclippedtoprecedethelabeledhand-objectcontact. PPOhyperparameters: actor
learningrate2ˆ10´5 withanadaptivescheduletargetingKL“0.01,criticlearningrate10´3,discountfactor
𝛾 “ 0.99, GAE parameter 𝜆 “ 0.95, clipping parameter 𝜖 “ 0.2, entropy coefficient 0.01, 24 steps per
GAE
environment,5learningepochswith4mini-batches,andmaximumgradientnorm0.1. Episodesterminate
whentheobject’s𝑧-positiondeviatesbymorethan0.4mfromthereference,therootheightdeviatesbymore
than0.25m,ortherootorientationerrorexceeds1.0rad.
B.2. Scene-Aware Tracker
Forscene-levelinteractionssuchassteppingovercurbs,traversingslopesandstairs,orsittingonchairs,the
controller’sflat-groundpriorisnotdirectlyapplicable. Insteadofattachingalatentadaptor,wefine-tunethe
controllerend-to-endtogetherwithaheight-mapencoder𝜖 andanauxiliarykinematicdecoder𝒢 onthe
ℎ rec
reconstructedscene-awaredata.
Architecture. Weconstructan11ˆ11heightmapgridcenteredontherobotwithatotalextentof1.5manda
resolutionof0.15m. Ateachgridpoint,adownwardrayiscastagainstthescenemeshtoobtaintheterrain
hit position; positions are then transformed into the robot’s yaw-aligned local frame, yielding a p11,11,3q
tensor. Theheightmapisprocessedbya3-layerCNNwithchannelsr64,128,256s,kernelsize3ˆ3,stride2,
andLeakyReLUactivations;spatialdimensionsreduceas11 Ñ 6 Ñ 3 Ñ 2,andtheoutputisflattenedtoa
1,024-dimfeaturevector. Thisvectorisconcatenatedwiththeproprioceptiveobservationandthecontroller’s
tokenizer features, then passed through a fusion MLP (r256s, SiLU) that produces the latent input to the
controller’smotiondecoder.
Training. WetrainwithPPO(Schulmanetal.,2017)on64NVIDIAL40GPUswith1,024parallelenvironments
perGPUinIsaacLabfor30,000iterations. Unlikeobject-awaretracking,wefine-tunethecontroller(encoder,
FSQquantizer,andactiondecoder𝒢)end-to-endtogetherwiththeheight-mapencoder𝜖 andtheparallel
ℎ
kinematicdecoder𝒢 . 𝒢 reconstructstheinputmotiontargetstoprovideanauxiliaryMSEloss(weight
rec rec
0.01)thatregularizesthelatenttoremainfaithfultothereference. Referencestateinitializationissampled
20

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
| Term |     | Description | Dim Used |
| ---- | --- | ----------- | -------- |
Proprioception
| Jointposition       |                             | robotjointangles | 43/29 Both |
| ------------------- | --------------------------- | ---------------- | ---------- |
| Jointvelocity       | robotjointangularvelocities |                  | 43/29 Both |
| Baseangularvelocity |                             | inbodyframe      | 3 Both     |
| Previousaction      |                             | lastmeta-action  | 66/29 Both |
| Baselinearvelocity  |                             | inbodyframe      | 3 O        |
| Gravitydirection    |                             | inbodyframe      | 3 S        |
Referencemotiontargets
| Motionanchorposition    | targetrootpositioninbodyframe           |                         | 3 O  |
| ----------------------- | --------------------------------------- | ----------------------- | ---- |
| Motionanchororientation |                                         | targetrootorientation6D | 6 O  |
| Currentcommand          | ref.jointposition+velocity,currentframe |                         | 58 O |
Multi-futurecommand ref.jointposition+velocity,10futureframes 580 O
| Multi-futureanchorori | 10futurerootorientations6D |     | 60 O |
| --------------------- | -------------------------- | --- | ---- |
Objectstate
| Objectposition         | currentobjectposinbodyframe |                    | 3 Both  |
| ---------------------- | --------------------------- | ------------------ | ------- |
| Objectorientation6D    | currentobjectoriinbodyframe |                    | 6 Both  |
| Objectposdelta(10fut.) |                             | ref ´sim ,position | 30 Both |
fut cur
| Objectoridelta(10fut.) |                               | relativerotation,6D | 60 Both |
| ---------------------- | ----------------------------- | ------------------- | ------- |
| Targetobjectposition   | referenceobjectposinbaseframe |                     | 3 O     |
| ObjectBPSencoding      | per-objectshapedescriptor     |                     | 10 O    |
| Tableposition          |                               | inbodyframe         | 3 O     |
| Tableorientation6D     |                               | inbodyframe         | 6 O     |
Hand-objectcontact
| Hand-to-objecttransform | perrighthand(3pos+6ori) |                     | 9 O  |
| ----------------------- | ----------------------- | ------------------- | ---- |
| Fingertipcontactforces  |                         | 3Dforceperfingertip | 12 O |
Scene
| Localheightmap | 11ˆ11terrain𝑧inbodyframe |     | 121 S |
| -------------- | ------------------------ | --- | ----- |
Table 5: Observations for the object-aware adaptor (O) and the scene-aware tracker
Policy Observations.
(S),groupedbycategory. Whentwodimsarelisted(e.g.,43/29),thefirstappliestotheobject-awarepolicy
(43-DoFG1includingfingers)andthesecondtothescene-awarepolicy(29-DoFG1,nofingers). Proprioceptive
andprevious-actionobservationsarestoredas10-framehistories;instantaneousvaluesarelistedabove.
uniformlyacrossthefullmotionateveryepisodereset. Sincehand-objectinteractionisnotinvolvedinthese
tasks,manipulation-specificrewardterms(graspandobject-posetracking)aredisabled. Episodesterminate
undercumulativetracking-errorthresholdswithadaptivestrictorientationandfoot𝑥𝑦𝑧 constraints.
B.3. Training Cost
Becauseeachtrackingpolicyistrainedjointlyoverasharedtask-familypoolratherthanfitpersequence,we
reporttheamortizedtrainingcostpermotion,definedasthetotaltrainingwall-clockofarundividedbythe
numberofmotionsinitspool. Afullpolicyistrainedfor30,000PPOiterationson64NVIDIAL40GPUswith
1,024environmentsperGPU,whichtakesroughly30hours,andeachruntrains2,000–4,000motionsjointly.
The amortized cost is therefore only about 0.5–0.9 minutes per motion, far below the per-sequence cost of
fitting a controller to each trajectory in isolation. As the pool grows with additional in-family motions, we
donotretrainfromscratch: wewarm-startfromthecurrentpolicyandfine-tune,whichtypicallyconverges
within6,000iterations(aboutonefifthofafullrun,„6hours),reducingtheamortizedcostofincorporating
newmotionstoroughlyonefifthofthefull-trainingfigure.
21

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
|     | Term                    |     |     |     |           | Formula  |           |     |     | Weight | Used |
| --- | ----------------------- | --- | --- | --- | --------- | -------- | --------- | --- | --- | ------ | ---- |
|     | Motiontrackingreward    |     |     |     | `         |          |           | ˘   |     |        |      |
|     | Anchorposition          |     |     |     | exp`´}𝑝rr | oot´𝑝r   | oot}2{𝜎2  |     |     | 0.5    | Both |
|     |                         |     |     |     |           | 𝑡        | 𝑡         | ˘   |     |        |      |
|     | Anchororientation       |     |     |     | ex`p´}𝑟ř  | r roota𝑟 | root}2{𝜎2 |     |     | 2.5    | Both |
|     |                         |     |     |     |           | 𝑡        | 𝑡         | ˘   |     |        |      |
|     | Relativebodyposition    |     |     |     | 1         | }𝑝r      | 𝑖,𝑡}2{𝜎2  |     |     |        | Both |
|     |                         |     |     |     | exp`´     | ř𝑖 𝑖,𝑡´𝑝 |           | ˘   |     | 1.0    |      |
|     | Relativebodyorientation |     |     |     | 𝑁         | }𝑟r      | 𝑖,𝑡}2{𝜎2  |     |     |        | Both |
|     |                         |     |     |     | exp`´ 1   | ř𝑖 𝑖,𝑡a𝑟 |           | ˘   |     | 5.0    |      |
𝑁
|     | Bodylinearvelocity |     |     |     | exp`´ 1 | ř𝑖 }𝑣r 𝑖,𝑡´𝑣 | 𝑖,𝑡}2{𝜎2 | ˘   |     | 1.0 | Both |
| --- | ------------------ | --- | --- | --- | ------- | ------------ | -------- | --- | --- | --- | ---- |
𝑁
|     | Bodyangularvelocity |     |     |      | e`xp´ 1 | }𝜔r 𝑖,𝑡´𝜔        | 𝑖,𝑡}2{𝜎2 |     |     | 1.0 | Both |
| --- | ------------------- | --- | --- | ---- | ------- | ---------------- | -------- | --- | --- | --- | ---- |
|     |                     |     |     |      | 𝑁       | ř 𝑖              |          | ˘   |     |     |      |
|     | 5-pointlocalbody    |     |     | exp´ | 1       | }𝑝rloc´𝑝loc}2{𝜎2 |          |     |     | 2.0 | S    |
|     |                     |     |     |      | |𝒮5|    | 𝑖P𝒮5             | 𝑖,𝑡      | 𝑖,𝑡 |     |     |      |
|     | Objectreward        |     |     | `    |         | ˘                |          | `   | ˘   |     |      |
Objectposetracking 𝑤 exp´𝛼 𝑝}𝑝r𝒪 ´𝑝𝒪 } `𝑤 exp´𝛼 𝑟}𝑟r 𝒪a𝑟 𝒪} 20.0 O
|     |     |     | 𝑝   |     | 𝑡   | 𝑡   | 𝑟   | 𝑡   | 𝑡   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Graspreward
|     |                      |     |     |       | `        |           |        | ˘      |     |      |     |
| --- | -------------------- | --- | --- | ----- | -------- | --------- | ------ | ------ | --- | ---- | --- |
|     | Graspcontactcount    |     |     |       | min𝑁     | contact{𝑁 | ,      | 1      |     | 40.0 | O   |
|     |                      |     |     |       |          | 𝑡         | min    |        |     |      |     |
|     | Graspfingerdirection |     |     |       | ´`cosp𝑑t | h umb, 𝑑i | ndexq⊮ |        |     |      | O   |
|     |                      |     |     |       |          | ř         |        | ˘t𝐶 𝑡u |     | 10.0 |     |
|     |                      |     |     |       |          | 𝑡         | 𝑡      |        |     |      |     |
|     | Graspcontactcenter   |     |     | exp´𝛾 | 1        | }𝑓 𝑗,𝑡´𝑐  | 𝑡}     | ⊮t𝐶 𝑡u |     | 0.1  | O   |
|     |                      |     |     |       | 𝑁        | 𝑓 𝑗       |        |        |     |      |     |
Regularization
|     | Latentresidualℓ       |     |     |     |     | 𝑡}2        |     |     |     |       | O   |
| --- | --------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | ----- | --- |
|     |                       | 2   |     |     |     | “ }Δ𝑧      | ‰   |     |     | 0.1   |     |
|     | Finger-primitivelimit |     |     |     |     | ⊮|𝑎fp|ą0.5 |     |     |     | ´10.0 | O   |
𝑗,𝑡
|     | Actionrateℓ               |     |     |     |       | }“ 𝑎 𝑡´𝑎   | 𝑡´1}2    |     |     | ´0.1      | S    |
| --- | ------------------------- | --- | --- | --- | ----- | ---------- | -------- | --- | --- | --------- | ---- |
|     |                           | 2   |     |     | ř     |            |          | ‰   |     |           |      |
|     | Anti-shakeangularvelocity |     |     |     | 1     |            |          | 2   |     | ´5ˆ10´3   | S    |
|     |                           |     |     |     | 𝑖Pℬř  | maxp0,}𝜔   | 𝑖,𝑡}´𝜏q  |     |     |           |      |
|     |                           |     |     |     | |ℬ |  |            |          |     |     |           |      |
|     | Anklejointacceleration    |     |     |     |       |            | 𝑞:2      |     |     | ´2.5ˆ10´7 | S    |
|     |                           |     |     |     |       | 𝑗 P𝒥       | 𝑗 ,𝑡     |     |     |           |      |
|     | Kinematicreconstruction   |     |     |     | }𝑞r   | a n k      | le }2    |     |     |           | S    |
|     |                           |     |     |     | ř     | 𝑡 ´` 𝒢 r e | c p𝑧 𝑡 q | ˘   |     | 0.01      |      |
|     | Jointlimit                |     |     |     |       |            |          |     |     |           | S    |
|     |                           |     |     |     | max0, | |𝑞         | 𝑗,𝑡|´𝑞   | lim |     | ´10.0     |      |
|     |                           |     |     |     | 𝑗     |            |          | 𝑗   |     |           |      |
|     | Undesiredbodycontact      |     |     |     |       | 𝑁undesired |          |     |     | ´0.1      | Both |
𝑡
Table6:RewardTerms. Rewardsfortheobject-awareadaptor(O)andthescene-awaretracker(S),organized
by the four categories from Sec. 3.3. The rightmost column indicates which tracker uses each term. For
grasp terms, the listed weight is the right-hand value; in object-aware training, the left hand uses half the
listedweight. ⊮t𝐶 uistheper-framemotion-labelcontactindicatorthatgatesthegraspfinger-directionand
𝑡
contact-centerterms. Theobjectpose-trackingrewardisadditionallygatedbyasimulatedfinger–objectcontact
indicator,soitisactiveonlywhilethehandisincontactwiththeobject. Foranti-shake,ℬ “tleftwrist,right
wrist,headuwithdeadzone𝜏 “1.5rad/s. Per-termGaussian-kernelbandwidth𝜎 variesbytermandisgiven
| inthereleasedconfig. |              | Negativeweightsindicatepenalties. |     |            |     |     |     |     |     |     |     |
| -------------------- | ------------ | --------------------------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| C.                   | Experiment   | Details                           |     |            |     |     |     |     |     |     |     |
| C.1.                 | Human-Object | Interaction                       |     | Generation |     |     |     |     |     |     |     |
Wecompareagainsttraining-basedandtraining-free4DHOIgenerationapproaches. Training-based
Baselines.
baselinesincludeCHOIS(Lietal.,2024),acontrollablemotiongenerationframeworkguidedbylanguage
andsparsewaypoints,andHOIDiff(Pengetal.,2025),adiffusion-basedmodelforaffordance-conditioned
HOIsynthesis. Fortraining-freecomparison,weevaluateDAViD(Kimetal.,2025a),whichgeneratesthefirst
frameusinganimagegenerativemodel(Labsetal.,2025)andproducesthevideofromthatframe. Since
imagegenerationoftenfailsunderpartialcontrolsignals(e.g.,Cannyedgemaps),wegenerate24imagesper
objectandmanuallyselectasuccessfulresultasthestartingframe. Toensurefairness,DAViDusesKling’s
image-to-videomodelunderthesamesettingasourapproach.
Beyond the quantitative metrics reported in the main paper, we conduct a user study with 30
User Study.
participants to assess perceptual quality. In each trial, participants view sequences from three of the four
methodsdrawnatrandomandselecttheresultwiththemostappropriateobjectaffordances(Aff.Real.) and
themostphysicallyplausiblemotion(Phys.Real.). AsshowninTable7,GRAILispreferredbyawidemargin
onbothcriteria. Thisperceptualstudycomplements, butdoesnotreplace, thephysics-basedtrackingand
robot-executionmetricsreportedinthemainpaper.
22

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
|     |     |     | Aff.Real.Ò |     | Phys.Real.Ò |     |
| --- | --- | --- | ---------- | --- | ----------- | --- |
Methods
|     | HOIDiff(Pengetal.,2025) |     |     | 2.0%  | 1.9%  |     |
| --- | ----------------------- | --- | --- | ----- | ----- | --- |
|     | CHOIS(Lietal.,2024)     |     |     | 12.2% | 16.8% |     |
|     | DAViD(Kimetal.,2025a)   |     |     | 11.2% | 10.4% |     |
Ours
|     |     |     |     | 74.7% | 70.9% |     |
| --- | --- | --- | --- | ----- | ----- | --- |
Table 7: User Study. 30-participant pick rates for the most appropriate object affordances (Aff. Real.) and
themostphysicallyplausiblemotion(Phys.Real.) ontheshared20-objectevaluationset. Pickrateshavea
theoreticalupperboundof75%under3-of-4randomsampling.
| Ours |     | DAViD |     | HOIDiff |     | CHOIS |
| ---- | --- | ----- | --- | ------- | --- | ----- |
Figure 7: Representative 4D HOI sequences from each method on the shared
| Qualitative | Comparison. |     |     |     |     |     |
| ----------- | ----------- | --- | --- | --- | --- | --- |
20-object evaluation set. GRAIL produces more coherent motions with accurate contact and natural hand
poses,whilebaselinemethodsoftenyieldunrealisticallyflatorstatichandconfigurations.
|     |     | ReconstructionQuality |     |     |     | TrackingQuality |
| --- | --- | --------------------- | --- | --- | --- | --------------- |
Methods ContactÓ Pen.Ó MPJPEÓ HumanSmo.Ó ObjSmo.Ó SRÒ ObjPosÓ MPJPE-LÓ
| w/o𝐿proj   | 0.016 1.93% | 16.70 | 0.0023 | 0.0011 | 41.6% | 0.374 47.1 |
| ---------- | ----------- | ----- | ------ | ------ | ----- | ---------- |
| w/o𝐿depth  | 0.017 1.97% | 4.35  | 0.0020 | 0.0011 | 42.6% | 0.372 49.3 |
| w/o𝐿cont   | 0.024 1.52% | 4.81  | 0.0022 | 0.0009 | 53.3% | 0.332 52.4 |
| Ours(Full) | 0.015 1.81% | 4.89  | 0.0020 | 0.0009 | 81.4% | 0.135 41.8 |
Table8:Ablation Study on Reconstruction Losses. Reconstructionquality(Contact,Pen.,MPJPEinpixel
space,motionsmoothness)anddownstreamtrackingquality(SR,ObjPos,MPJPE-L)foreachlossablation.
Each loss targets a different failure mode in reconstruction; the full model achieves the best downstream
trackingdespitenotminimizingeveryreconstructionproxyinisolation.
Qualitative Comparison. Fig.7showsthatGRAILproducesmorecoherentmotionswithaccuratecontact
andnaturalhandposes,whilebaselinemethodsoftenyieldunrealisticallyflatorstatichandconfigurations
unsuitablefordownstreamhumanoidskilllearning.
ReconstructionAblation. Weablatetheinteraction-awarereconstructionlosses(𝐿proj ,𝐿depth ,𝐿cont )onthe
124-motionbenchmark. AsshowninTable8,removing𝐿proj degradesimage-spaceconsistency,whileremoving
𝐿depth or𝐿cont weakensmetricinteractionquality. Thesereconstruction-levelerrorspropagatetodownstream
tracking: eachablationsubstantiallyreducestrackingsuccessrateandincreasestrajectorydeviation,whilethe
23

GRAIL:GeneratingHumanoidLoco-Manipulationfrom3DAssetsandVideoPriors
fullmodelachievesthebestoveralldownstreamtrackingquality.
24