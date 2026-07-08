HoloBrain-0 Technical Report
XuewuLin, TianweiLin, YunDu, HongyuXie, YiweiJin, JiaweiLi, ShijieWu, QingzeWang,
MengdiLi, MengaoZhao, ZiangLi, ChaodongHuang, HongzheBi, LichaoHuang, ZhizhongSu
HorizonRobotics
Inthiswork, weintroduceHoloBrain-0, acomprehensiveVision-Language-Action(VLA)framework
that bridges the gap between foundation model research and reliable real-world robot deployment.
The core of our system is a novel VLA architecture that explicitly incorporates robot embodiment
priors, including multi-view camera parameters and kinematic descriptions (URDF), to enhance 3D
spatialreasoningandsupportdiverseembodiments. Wevalidatethisdesignthroughascalable“pre-
trainthenpost-train”paradigm,achievingstate-of-the-artresultsonsimulationbenchmarkssuchas
RoboTwin 2.0, LIBERO, and GenieSim, as well as strong results on challenging long-horizon real-
world manipulation tasks. Notably, our eﬀicient 0.2B-parameter variant rivals significantly larger
baselines, enabling low-latency on-device deployment. To further accelerate research and practical
adoption, we fully open-source the entire HoloBrain-0 ecosystem, which includes: (1) powerful pre-
trained VLA foundations; (2) post-trained checkpoints for multiple simulation suites and real-world
tasks; and (3) RoboOrchard, a full-stack VLA infrastructure for data curation, model training and
deployment. Together with standardized data collection protocols, this release provides the commu-
nity with a complete, reproducible path toward high-performance robotic manipulation.
Code: github.com/HorizonRobotics/RoboOrchardLab
Webpage: horizonrobotics.github.io/robot_lab/holobrain
Correspondence: Tianwei Lin at tianwei.lin@horizon.auto
Figure1: OverviewofHoloBrain-0. Byincorporatingexplicitembodimentmodeling(e.g.,cameraparameters
and kinematic descriptions), our model effectively unifies training across heterogeneous robots. Together
with a full-stack VLA infrastructure (RoboOrchard) and an effective test-driven data strategy, HoloBrain-0
delivers superior performance on both real world and simulation manipulation benchmarks.
1
6202
beF
21
]OR.sc[
1v26021.2062:viXra

1 Introduction
Achievingatrulygeneral-purposeroboticagenthaslongbeenacentralgoalofroboticsresearch. Traditional
roboticsystems[1,2,3]typicallyrelyonmodularpipelinesthatcombineperception,stateestimation,motion
planning, and control. While effective in structured environments, these approaches require extensive task-
and platform-specific engineering, which limits their ability to scale and generalize. Recent progress in
robot learning has shifted attention toward end-to-end, data-driven models. Vision–action (VA) models
[4,5,6],trainedviaimitationlearning,haveshownstrongcapabilityinlearningcomplexmanipulationskills
directly from expert demonstrations. Building on this paradigm, the integration of vision–language models
(VLM) [7, 8] has led to vision–language–action (VLA) models [9, 10]. By combining perception, language
understanding, and control, these models pave the way for more general robotic agents.
However,developingatrulygeneralroboticagentremainsasignificantchallenge. AlthoughweexpectVLAs
to understand diverse language instructions, real-world deployment inevitably exposes agents to complex,
out-of-distribution (OOD) states that were not seen during training [9, 11]. This requires robust general-
ization across various factors, from visual perturbations (e.g., lighting, textures, backgrounds) to physical
variations in objects (e.g., poses, shapes, and deformability). To address these complexities, large-scale pre-
training has become a key strategy [10, 12, 13]. Yet, this introduces a new challenge: utilizing diverse data
meanshandlingdifferentrobotembodiments,requiringthemodeltomastercross-embodimentcompatibility
[13,14,15]. Buildingonpowerfulpre-trainedVLAfoundations, recentworks[14,16,17]havedemonstrated
impressive capabilities in complex, long-horizon tasks via post-training. However, translating these models
from isolated demos to robust, general-purpose systems faces systemic bottlenecks. Specifically, two critical
challengesremain: theprohibitivecostofcuratinghigh-quality,expert-leveldemonstrationsatscale,andthe
diﬀiculty of deploying large models for low-latency, real-time control. These challenges underscore a critical
reality: scalable progress demands not only advanced architectures but also robust infrastructure. Without
a unified stack to streamline data and inference, the path toward generalizability remains bottlenecked by
ineﬀiciency and reproducibility issues.
In this work, we present HoloBrain-0, a holistic framework that addresses these challenges through a unified
design integrating novel VLA model architecture, scalable data strategy, and full-stack infrastructure.
• Embodiment-awareVLAArchitecture. ConventionalVLAstypicallylearnadirectmappingfromvision
to action, relying on composite action spaces [18, 10], heterogeneous encoder [15] or textual prompts
[14] to handle data from different robots. This severely overlooks explicit structural priors, including
cameraparametersandkinematicchains, forcingmodelstofitcross-embodimentdatawithoutaphysical
understanding. To address this, we explicitly incorporate embodiment priors into our architecture (Fig.
1). First, a Spatial Enhancer uses camera parameters and depth map to project multi-view images into
a unified 3D coordinate system. Second, an Action Expert explicitly encodes the robot’s kinematic chain
via a novel Joint-Graph Attention mechanism. Finally, to unify control across heterogeneous robots, we
design a hybrid action space that predicts both relative joint and SE(3) motions for each joint. This
ensures compatibility across single/dual-arm manipulators, mobile robots, and human-captured data.
• EffectiveandReproducibleDataStrategy. Weadoptatwo-stagedatacurationpipeline. Forpre-training,
we leverage a heterogeneous mixture of multi-embodiment robot and human demonstrations to build a
generalistfoundation. Forpost-training,specificallytargetingdexterousandlong-horizonbimanualtasks
under constrained budgets, we introduce a novel test-driven data collection paradigm. This closed-loop
approach dynamically adjusts collection strategy based on model performance. We detail this iterative
process, demonstratinghowtoselectivelytargetfailurecasesandensurehighdataquality. Thisprovides
a reproducible and cost-effective solution for learning complex tasks.
• Open-Source Full-Stack VLA Infrastructure. Finally, to enable eﬀicient experimentation and deploy-
ment, we introduce RoboOrchard, an open-source infrastructure that covers the entire pipeline from data
collection to model deployment. RoboOrchard offers a web-based interface for data acquisition with vi-
sualization, ensures data quality through automated validation, organizes data using the MCAP format,
andpackagesdatasetsintoArrow-basedrepresentationsforscalabletraining. Fordeployment,itsupports
bothsynchronousandasynchronousinference,providingflexibilityandeﬀiciencyacrossdiverseusecases.
2

Drivenbythisunifieddesign,weextensivelyevaluateHoloBrain-0inbothsimulationandreal-worldsettings.
In simulation, our framework achieves state-of-the-art performance on competitive benchmarks including
RoboTwin 2.0, LIBERO, LIBERO-Plus, and GenieSim. In the real world, HoloBrain-0 excels in challenging
manipulation tasks—such as flexible clothes folding, deformable box folding, and generalized “Grasp Any-
thing” tasks. Notably, our lightweight 0.2B variant achieves performance comparable to larger baselines,
enabling eﬀicient, low-latency on-device deployment. Finally, we fully open-source the HoloBrain-0 ecosys-
tem, releasing all pre-trained foundations, post-trained checkpoints, and the RoboOrchard infrastructure.
2 ProblemFormulation
We formulate the robotic manipulation task as a conditional action generation problem. At each time
step, the system receives multi-view RGB images I ∈ RN×H×W×3 and corresponding depth maps D ∈
RN×H×W×1, along with the robot’s current proprioceptive joint state S ∈ RNj. In this work, our policy
operatesdirectlyonthiscurrentobservationframe. Formulti-taskexecution,themodelisfurtherconditioned
on natural language instructions T. Crucially, to explicitly ground the model in the physical world, we
incorporate camera parameters C (intrinsics and extrinsics of the N views) and robot kinematic priors E
(e.g., URDF descriptions) into the input space. Formally, the complete input space is defined as:
(cid:8) (cid:9)
I ∈RN×H×W×3,D ∈RN×H×W×1,S ∈RNj,T ∪{C,E} (1)
Here, N denotes the number of camera views and N is the degrees of freedom (DoF) of the robot. Given
j
these inputs, the model generates action chunk for the subsequent t
out
steps, denoted as S
out
∈RNj ×tout.
3 Method: ModelArchitecture
As illustrated in Fig. 1, the overall architecture of HoloBrain-0 presents a unified, end-to-end framework
composed of three core modules. First, a Vision-Language Model (VLM) serves as the semantic back-
bone, encoding text instructions and visual observations. To balance inference eﬀiciency with performance,
we instantiate this module with two distinct architectures: a 2D detection foundation model (Ground-
ingDINO [19]) and an LLM-based VLM (Qwen2.5-VL [8]). Second, a Spatial Enhancer (Section 3.1) injects
multi-view spatial consistency and geometric priors into the VLM-extracted visual embeddings. Third, the
Embodiment-aware Action Expert (Section 3.2) explicitly encodes the robot’s kinematic chain. It facili-
tates dense interaction of action queries with robot proprioception, text prompts, and spatially-enhanced
visual features via cross-attention mechanisms. Ultimately, it predicts control commands within a unified,
relative action space, accommodating heterogeneous robot configurations. Finally, to ensure stable and
fluid real-world deployment, we introduce SimpleRTC combined with a Teacher Forcing training strategy
(Section 3.4), enabling smooth asynchronous inference.
3.1 Perspective-awareSpatialEnhancer
To effectively bridge the gap between rich 2D visual semantics and accurate 3D spatial geometry, we adopt
theSpatialEnhancerfromourpriorworks(BIP3D[20]andSEM[21]). Thismoduleexplicitlyinjectsspatial
priors by projecting 2D image features from multiple views along their respective camera frustums into a
unified 3D coordinate system. Functionally, it utilizes camera intrinsics and extrinsics to sample 3D points,
predictsadiscretedepthdistribution(withpluggabledepthsensorinputs),andaggregatesthesetogenerate
depth-aware 3D positional embeddings. These embeddings are then fused with image features to produce
a globally consistent, geometry-aware 3D representation. Crucially, to facilitate cross-embodiment training,
wemodifytheoriginalSEM[21]designbyshiftingthe3Dprojectioncoordinateframefromtherobot’slocal
baseframetothecentral fixed camera frame(e.g.,third-personorhead-mountedview). Fusingauxiliary
views (e.g., wrist cameras) into this central frame offers two major advantages: (1) it eliminates learning
3

Figure 2: Visualization of input state representation and output action space of our action expert.
interference caused by inconsistent base definitions across different robotic platforms, enabling robust cross-
embodiment generalization; and (2) it seamlessly accommodates egocentric human data (e.g., EgoDex [22]),
which inherently lacks a fixed robotic “base” frame but possesses a natural head-mounted view.
3.2 Embodiment-AwareActionExpert
Motivated by the distinct nature of the robot motion planning task compared to other problem domains,
wedesignaninnovativeActionExpert, ratherthandirectlyadoptingthestructureoflargelanguagemodels
(LLMs)asmostexistingmethodsdo. ThedesignoftheActionExpertadherestotheprincipleofenhancing
embodiment generalization and ensuring compatibility with data from arbitrary embodiment. The overall
architecture largely builds upon SEM [21]. It consists of a robot state encoder and an action decoder, both
primarily implemented with a joint-centric transformer. The core component is the joint-graph attention
mechanism (see [21] for details). To model the action probability distribution, we employ a diffusion-based
approach where, instead of predicting noise, we perform x-prediction to directly estimate the states.
Building upon SEM, we introduce improvements to both the input state representation and the output
actionspace,furtherboostingthemodel’sembodimentgeneralizationandperformance. First,regardingthe
input state representation, we mask joint angle information and feed only the 6D pose of each joint into the
| model. Formally, | the | input state | for the | i-th joint is defined | as: | | | |
| ---------------- | --- | ----------- | ------- | --------------------- | --- | --- | --- | --- |
(
| | | | [−1]⊕[x,y,z,q | ,q ,q ,q | ] if m | =1 | | |
| --- | --- | ----- | ------------- | ---------- | --------- | ----- | --- | --- |
| | | | | w x y | z i | 1≤i≤N | | |
| | | s i = | | | | | j | (2) |
| | | | [θ]⊕[x,y,z,q | ,q ,q ,q ] | otherwise | | | |
w x y z
Here,thebinarymaskm =1indicatesthatthescalarjointangleθisexcluded(settoamaskedvalue). Inour
i
implementation,alljointanglesexceptthegripperopenness(inmeters)aremasked. Wearguethatthejoint
6D poses are suﬀicient to represent a robot’s state. Unlike joint angles, which suffer from inconsistent zero-
positiondefinitions,rotationdirections,andURDFvariationsacrossdifferentrobotembodiments,Cartesian
link poses offer a unified geometric reference. Consequently, providing ambiguous, embodiment-dependent
joint angles as input can hinder the model’s ability to generalize across different embodiments.
For the output action space, our model predicts hybrid relative transformations for each joint, encompass-
ing both joint angle space and Cartesian pose space. Specifically, for each joint i, the model outputs a
concatenation of joint angle residuals (in radians) and link pose displacements (in meters and quaternions):
| | | | (cid:8) | | | (cid:12) | (cid:9) | |
| --- | --- | --- | ------- | --- | --- | -------- | ------- | --- |
(cid:12)
| | | a = | [∆θ,∆x,∆y,∆z,∆q | ,∆q | ,∆q ,∆q | ] 1≤i≤N | | (3) |
| --- | --- | --- | --------------- | --- | ------- | ------- | --- | --- |
| | | t | | w | x y | z i | j | |
Here, both joint angle and link pose displacements are calculated based on the current robot state, without
normalized. Thisdual-spacepredictionformulationofferstwosignificantadvantages. First,itenablesflexible
deploymentacrossdiversehardwareinterfaces,supportingbothlow-leveljointpositioncontrolandhigh-level
end-effector pose control. Second, it facilitates training on heterogeneous datasets, including human video
| data without | explicit | joint angle | annotations. | | | | | |
| ------------ | -------- | ----------- | ------------ | --- | --- | --- | --- | --- |
4

3.3 TrainingObjectives
During training, we optimize four loss terms as defined in (4).
(cid:0) (cid:1)
L=α λ L +λ L +λ Lfk +λ L (4)
τ 1 joint 2 pose 3 pose 4 depth
Here,thejointpositionlossL andjointposelossL aredefinedasthedistancesbetweenthepredicted
joint pose
and ground truth joint angles and 6D poses, respectively. Crucially, as the model predicts relative updates,
we add these predictions to the current robot state to compute the loss on absolute values. To further
improve positional accuracy, we add a forward kinematics pose loss Lfk . This loss first recomputes the 6D
pose
poses from the predicted joint angles using forward kinematics, and then evaluates the distance between the
recomputedposesandgroundtruth. Sincerobotmotiontrajectoriesexhibithighlycomplexdistributionsand
the dataset contains substantial noise, we replace the standard L2 distance used in most diffusion policies
with the smooth L1 distance, which mitigates instability caused by exceptionally large training errors on
certain samples. The depth loss L , applied to the depth distribution predicted by the spatial enhancer,
depth
is formulated as a cross-entropy loss. In (4), α is a timestep-dependent coeﬀicient that varies with the
τ
diffusion timestep τ, given by:
α =T/(τ +1) (5)
τ
where T denotes the maximum number of noise addition steps in diffusion training, set to T =1000 in our
experiments. Consequently, higher noise levels are assigned smaller loss weights, and vice versa.
Tofurtherenhancethemodel’scapacitytomodelingmultimodalactiondistributions,weintroduceawinner-
takes-more training strategy. Specifically, for each training sample, we generate N candidate trajectories
and dynamically modulate the loss weights based on prediction error. A higher weight is assigned to the
trajectorywiththeminimumpredictionerror(the“winner”),whiletheweightsfortheremainingtrajectories
aresuppressed. Thismechanismpreventsthemodelfromconvergingtothemeanofdistinctmodes, thereby
preserving the diversity of valid solutions.
3.4 SimpleRTCandTeacher-forcingTraining
In VLA deployment, synchronous inference sequentially executes full action chunks. While effective for
quasi-static tasks, this modality inherently induces motion pauses and prolonged decision intervals (often
reaching ≈ 1s). Consequently, the system is rendered incapable of handling highly dynamic or fine-grained
manipulation tasks. Alternatively, asynchronous inference decouples model inference from action execution,
maximizing inference frequency (typically 5–10 FPS). However, observation latency and the inherent incon-
sistencies between consecutive action chunks induce trajectory jumps. This results in mechanical jerks that
compromisetasksuccessratesandpotentiallydamagethehardware. Tomitigatethesediscontinuities,Black
et al. [23] introduced Real-Time Chunking (RTC), which enforces temporal consistency via inference-time
gradient guidance from the preceding unexecuted chunk. However, this gradient computation significantly
exacerbates inference latency. To address this, they proposed Training-time RTC [24], incorporating consis-
tency directly into the training phase via fixed-length action prefixes. While eliminating inference overhead,
this approach need extensive model retraining.
Conceptually, both approaches draw inspiration from image diffusion inpainting. However, inference-time
RTC [23] relies on gradient guidance [25], which incurs significant computational overhead and optimization
instability. Conversely, Training-time RTC [24] functions as a mask-as-condition model, severely restricted
by its rigid, fixed-mask structure. To address these limitations, we rethink the RTC paradigm for VLA
modelsandproposeaflexible,two-partstrategy: (1)Inference-timestrategy-SimpleRTC :Azero-overhead
pluggablestrategybasedonsoft-constraintinpainting,seamlesslyintegrableintoanydiffusionorflowpolicy.
(2) Training-time strategy - Teacher Forcing . A training strategy that dynamically replaces the first N
steps of input noise with ground-truth actions, enabling robust adaptation to arbitrary-length guidance.
Inference-time-SimpleRTC.SimpleRTCisagradient-freemethodthatrequiresneithermodelmodification
nor retraining. SimpleRTC directly leverages the unexecuted segment of the preceding action chunk to
5

guide the denoising phase during inference. Adopting a soft-masking strategy inspired by RTC [23], our
method enforces strict consistency with the preceding chunk for the initial d steps (corresponding to the
inference latency), followed by a smooth trajectory fusion within a subsequent transition window of length
L. Formally,letAˆ =Model(A ,τ)denotethex-predictionoutputatdiffusionstepτ,andA represent
| | | 0|τ | | τ | | | | | | prev | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- |
A˜
the unexecuted remainder of the preceding action chunk. The blend action is formulated as:
0|τ
| | | | | | A˜ | =w⊙A | | +(1−w)⊙Aˆ | | | |
| --- | --- | --- | --- | --- | --- | ---- | --- | --------- | --- | --- | --- |
| | | | | | 0|τ | | | | 0|τ | | (6) |
prev
where ⊙ denotes element-wise multiplication, and w∈[0,1]H is a temporal weighting vector determined by
the specific decay strategy. Then, we conduct denoise sampling as A = Sampler(A ,A˜ ,τ). Notably,
| | | | | | | | | | τ−1 τ | 0|τ | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
this guidance is derived for x-prediction. Modifications are necessary for noise or flow prediction parameter-
izations. To govern this transition, we define a normalized variable ρ for each time step t in the prediction
t
| horizon | H, representing | | the | residual | influence | | of the historical | | trajectory: | | |
| ------- | --------------- | --- | --- | -------- | --------- | --- | ----------------- | --- | ----------- | --- | --- |
8
| | | | | | | ><1 | | t∈[0,d] | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- |
t−d
| | | | | | ρ | = 1− | | t∈(d,d+L) | | | (7) |
| --- | --- | --- | --- | --- | --- | ---- | --- | --------- | --- | --- | --- |
| | | | | | t | >: | L | | | | |
t∈[d+L,H)
0
Here,drepresentstheinferencedelaywherethetrajectoryisstrictlyconstrainedtohistory,andLdenotesthe
length of the fusion window. Experimental results demonstrate that this concise strategy yields surprisingly
robust control performance. To accommodate varying smoothness requirements across different tasks, we
introduce Linear and Quadratic decay curves alongside the original Exponential decay:
eρt −1
| | | | | wlin | | wquad | =ρ2, | wexp | | | |
| --- | --- | --- | --- | ---- | --- | ----- | ---- | ---- | ---- | --- | --- |
| | | | | | =ρ | t , | | | =ρ t | | (8) |
| | | | | | t | t | | t t | e−1 | | |
Training-time-TeacherForcing. Since we incorporate inference-time SimpleRTC, the model receives A in
(6)asinputduringtheinferencephase,wherethefirsttstepsarealreadynoise-freeactions. However,under
standard diffusion training, all actions fed to the model are noisy, which leads to a pronounced domain gap
betweeninferenceandtraining. Tomitigatethisdiscrepancy,wefurtherintroduceateacher forcing strategy
during training. Specifically, we construct a hybrid input trajectory by overwriting the initial noisy steps
with ground-truth actions. Let A gt denotes the ground-truth action, and A noise denotes the corresponding
A′
| noisy action. | | We define | the | teacher-forced | | input | | as: | | | |
| ------------- | --- | --------- | --- | -------------- | --- | ----- | --- | --- | --- | --- | --- |
noise
(
| | | | | | | | A | , t<N | | | |
| --- | --- | --- | --- | --- | ------- | --- | ------- | ----- | ------ | --- | --- |
| | | | | | ′ | | gt,t | | prefix | | |
| | | | | | A | = | | | | | (9) |
| | | | | | noise,t | | A | , t≥N | | | |
| | | | | | | | noise,t | | prefix | | |
Here, the prefix length N is sampled from a Poisson distribution Poisson(λ), where the mean λ is a
prefix
hyperparameter calibrated to match the expected inference delay. To ensure robustness against history-free
inference, we apply this strategy (9) with a small teacher forcing ratio γ (e.g. 25%). This probabilistic
mixture effectively aligns the training distribution with SimpleRTC inference while preserving the model’s
| general | denoising | capabilities | | on fully | noisy | inputs. | | | | | |
| --------- | --------- | ------------ | --- | -------- | ----- | ------- | --- | --- | --- | --- | --- |
| 4 Method: | | DataStrategy | | | | | | | | | |
4.1 Pre-trainingDataCorpus
To cultivate a foundational VLA model with robust generalization capabilities, we curate a large-scale,
heterogeneous dataset for pre-training. Our data selection strategy is guided by three core principles:
• Cross-EmbodimentandSpatialGrounding. Aligningwithourembodiment-awarearchitecture,wetarget
extensive cross-embodiment and 3D spatial generalization. Therefore, we source data across diverse
6

Figure 3: Visualizing 3D consistency verification. We project the 6D pose of each joint onto the image coor-
dinates (including third-person and wrist cameras) based on the camera intrinsic and extrinsic parameters.
Any episodes with inaccurate projection results are identified as erroneous and subsequently filtered out.
robotic platforms and sensor configurations. Crucially, to satisfy our architectural requirements, all
selected datasets strictly include multi-view camera parameters (intrinsics and extrinsics) and complete
kinematic descriptions (i.e., URDFs).
• High-FidelityGeometricPriorsfromSimulation. Simulation environments naturally provide exact geo-
metricgroundtruth,includingaccuratedepthmapsandcameraparameters. Weincorporateasubstantial
volume of simulation data, as this rich spatial supervision significantly aids the model in developing a
rigorous understanding of 3D world dynamics.
• SemanticandObjectDiversity. Diversity in task types and interactive objects is critical for open-world
generalization. To maximize this diversity, we adopt two explicit data curation strategies. First, we
integrate large-scale human-centric dataset, which naturally encapsulate extensive open-world variance
in both object appearances and interaction patterns. Second, to systematically benchmark and enhance
robotic manipulation across extreme object varieties, we specifically design and collect the “Grasp Any-
thing” dataset, ensuring the model’s robustness against unseen and geometrically complex objects.
Afterdatacollection,weconductrigorousdatacleaning. Themostcriticalstepis3Dconsistencyverification:
we project joint 6D poses onto images and filter out data exhibiting significant reprojection errors, as shown
in Fig. 3. This method enables simultaneous validation of camera parameters, action labels, and URDF
accuracy. We also apply further filtering using criteria including task type, motion trajectory plausibility,
and instruction-video consistency to eliminate low-quality samples.
As shown in Table 1, the complete pre-training dataset consists of four main components: proprietary self-
collected data, open-source real-world data, simulation data and human video data. In total, the corpus
comprises over 156 million frames (captured over 3,500+ hours) derived from seven distinct embodiments.
During pre-training, we manually set sampling ratios for different sources based on data quality and task
richness;forinstance,weincreasetheproportionofself-collecteddatato41%andreducethatoftheEgoDex
dataset from 19%(frame ratio) to 9.8%.
4.2 IterativeTest-DrivenDataStrategyforPost-Training
Followingpre-training,effectivepost-trainingiscriticalforequippingVLAstomastercomplex,long-horizon
tasks. However, the eﬀicacy of this phase is often bottlenecked by the high cost of collecting high-quality,
real-world data. Naive dataset expansion becomes increasingly ineﬀicient for dexterous manipulation due to
distribution noise and high marginal collection costs. While prior methods address distribution shifts via
7

|     |     |     | Table 1: | Pre-training | Data | Statistics | of HoloBrain-0. |     |     |     |
| --- | --- | --- | -------- | ------------ | ---- | ---------- | --------------- | --- | --- | --- |

Data Type Dataset Name Embodiment Frames(M) Time(H) Traj Training ratio
| Self-collected | | | | Dual-arm | Piper | | 32.9 | 304.7 | 42539 | 41.41% |
| -------------- | --- | ------ | ---------- | -------- | ----- | --- | ---- | ------ | ------ | ------ |
| | | Agibot | World [26] | Agibot | G1 | | 71.6 | 1990.1 | 113846 | 24.5% |
Real-world
| | | Droid | [27] | Franka | | | 14.5 | 267.8 | 54636 | 11.76% |
| ---------- | ----- | -------------- | -------- | -------- | ------ | --- | ------ | ------ | ------ | ------ |
| | | | | Dual-arm | Piper | | 2.65 | 29.5 | 10883 | 4.7% |
| | | | | Dual-arm | Franka | | 0.34 | 3.7 | 2269 | 0.98% |
| | | RoboTwin | 2.0 [28] | | | | | | | |
| Simulation | | | | Dual-arm | UR5 | | 0.30 | 3.4 | 2032 | 0.98% |
| | | | | Dual-arm | Arx | | 0.37 | 4.1 | 2306 | 0.98% |
| | | Agibot-digital | [29] | Agibot | G1 | | 4.04 | 112.2 | 7350 | 4.9% |
| Human | Video | EgoDex | [22] | Human | | | 29.9 | 831.9 | 338219 | 9.8% |
| Total | | | | | | | 156.66 | 3547.4 | 531541 | - |
adversarialcollection[30,31]orinteractivecorrections[32,33],eﬀicientlyscalinginformationdensityremains
achallenge. Toaddressthis,weproposeatest-driveniterativeframeworkthatshiftsfocusfromscale-oriented
expansion to quality-driven iteration. This approach integrates two strategies: proactively expanding state
diversity to anticipate potential Out-of-Distribution (OOD) scenarios, and reactively targeting observed
failure clusters to align the training distribution with real-world complexities. An empirical analysis of this
| evolution | is provided | in | Appendix | C. | | | | | | |
| --------- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
ProactiveStateExpansion. To mitigate potential OOD failures before deployment, we proactively enhance
state diversity during the data collection phase. Rather than relying on random augmentation, we target
specific failure-prone conditions across two key dimensions. First, regarding visual states, we systematically
vary environmental factors such as lighting, background textures, and object instances to ensure perceptual
robustness. Second,regardingrobotstates,wetransitionfromfull-taskdemonstrationstogranular,sub-task
collection. Thisallowsustospecificallyreinforceidentifiedbottlenecksinthemanipulationpipelinewithout
| the redundancy | | of collecting | entire | successful | trajectories. | | | | | |
| -------------- | --- | ------------- | ------ | ---------- | ------------- | --- | --- | --- | --- | --- |
Test-Driven Failure Recovery. Inevitably, real-world deployment exposes agents to unanticipated OOD
states. To close the gap between training-time and test-time distributions, we employ a dynamic, closed-
loop recovery strategy. This process begins with failure mode characterization, where policy failures are
systematically analyzed and clustered by root cause. Next, we use these failed states as “seeds” for targeted
augmentation,varyingvisualandphysicalparameterstocoverthefailureneighborhood. Finally,weperform
distribution alignment by collecting short-horizon recovery trajectories (typically 2–3s) that guide the agent
back to the successful manifold. Unlike standard interactive methods like DAgger [32, 33], which typically
address individual errors, our approach resolves entire clusters of failure modes simultaneously, significantly
| optimizing | the | data collection | budget. | | | | | | | |
| --------------------------- | --- | --------------- | ------- | --- | ----------- | --- | --- | --- | --- | --- |
| 5 Full-StackInfrastructure: | | | | | RoboOrchard | | | | | |
While data-driven imitation learning has received significant attention for robotic manipulation, real-world
deployment is often hindered by fragmented toolchains and non-standardized interfaces. Unlike the mature
field of computer vision, robotic learning lacks unified data standards and deployment paradigms, resulting
insubstantialengineeringoverhead. Asaconsequence,researchersoftenexpendsubstantialeffortonsystem
| integration | tasks | rather | than focusing | on | algorithmic | innovation. | | | | |
| ----------- | ----- | ------ | ------------- | --- | ----------- | ----------- | --- | --- | --- | --- |
To address these challenges, we introduce RoboOrchard, a full-stack modular infrastructure illustrated
in Fig. 4. Its design centers on the principle of Artifact-Driven Decoupling: rather than relying on tightly
coupled code across system layers, RoboOrchard links independent modules through standardized artifacts.
To support this, we define Unified Artifact Specifications that precisely describe the protocols for key as-
sets, including self-describing datasets and self-contained model artifacts. Building on these specifications,
8

Figure 4: Overview of the RoboOrchard infrastructure. The system comprises three decoupled layers: a
bottom Hardware Abstraction Layer that bridges the gap between simulation and real-world hardware via
unified interfaces; a central Middleware Layer that drives the data-to-policy pipeline including storage,
training, and deployment; and a top Interaction Layer facilitating user management and visualization.
RoboOrchard provides a suite of ready-to-use components, such as a companion app for high-fidelity data
collection(Sec5.1),aPydantic-basedtrainingframework(Sec5.2),andadeploymentruntimethatsmoothly
switches between simulation and real hardware (Sec 5.3). Additionally, we provide several convenient tools,
suchasaninteractivevisualhand-eyecalibrationnodeandalightweightfileserverfordatareview. Together,
these components reduce engineering effort and accelerate experimental iteration on robot systems.
5.1 InfrastructureforDataAcquisition
High-quality real-world data serves as the cornerstone of embodied intelligence. RoboOrchard establishes a
completeinfrastructurerangingfromhardwareacquisitiontostandardizedstorage,aimedatresolvingissues
regarding the temporal synchronization and storage eﬀiciency of multimodal data.
DataAcquisitionSystem. We provide a unified data collection suite comprising a high-performance ROS 2
Recorder backendandauser-friendlyCompanionApp. Toguaranteehigh-bandwidthwriteperformance,the
backend leverages the MCAP format, featuring an integrated Integrity Monitor that automatically flags
sensor frame drops or timestamp anomalies. Complementing this, the frontend application offers a “What
You See Is What You Get” visual interface for task orchestration (via Foxglove). This interactive workflow
significantly lowers the barrier to entry for collecting expert demonstrations in laboratory settings.
RODatasetSpecification. To overcome the limitations of traditional flat files in handling large-scale multi-
modaldata,weproposetheRODatasetSpecification. Thisspecificationadoptsahybridstoragearchitecture:
high-bandwidth sensor data (e.g., images, joint states) is stored in the Apache Arrow format, enabling zero-
copy memory loading and seamless integration with the HuggingFace [34] ecosystem. Meanwhile, global
metadata such as task descriptions and statistical metrics are structured via an embedded DuckDB engine.
ThisdesignenableseﬀicientSQL-basedqueryingonmillion-framedatasetsandnativelyhandlesnon-aligned
multi-frequency signals, preserving the authentic temporal dynamics of the physical world.
9

5.2 InfrastructureforModelTraining
AsacoresubmoduleofRoboOrchard,RoboOrchardLabisamodulartrainingframeworkbuiltona“Library-
First” philosophy, designed to enhance the reproducibility of algorithm research and the safety of configu-
ration management. RoboOrchardLab currently provides native support for multiple VLA models, such as
HoloBrain-0, with plans to integrate additional models and learning algorithms in future releases.
Type-SafeConfiguration&Hook-basedTrainer. To move beyond traditional error-prone, unstructured dic-
tionary configurations, we employ a strict schema-based configuration system powered by Pydantic. This
approach ensures runtime automatic structural validation and enables IDE autocompletion for complex hy-
perparameters, effectively mitigating potential failures caused by configuration mismatches at the source.
Furthermore,thetrainingpipelineadoptsahook-based,event-drivenarchitecture. Thisdesignempowersre-
searcherstoinjectcustommonitoring,logging,orcontrollogicatspecificexecutionstageswithoutmodifying
the core training loop, ensuring both flexibility and codebase integrity.
ModelZoo&ModelArtifacts. The framework provides a baseline algorithm library (Model Zoo) that ad-
heres to unified I/O interfaces. Crucially, once training is completed, the system automatically packages a
standardizedModelArtifact. Unlikesimpleweightfiles,thisartifactencapsulatesSafeTensorsmodelweights
together with preprocessing pipelines, and environment dependencies into a single portable unit. This self-
contained design ensures that the model maintains independent inference capabilities after being detached
from the training codebase, embodying the principle of “Training as Delivery”.
5.3 InfrastructureforModelDeployment
In the deployment phase, RoboOrchard prioritizes enhancing both the reliability and eﬀiciency of the work-
flow. We achieve this through three key pillars: decoupled inference and control nodes with standardized
interfaces, flexible inference modes, and intuitive visualization tools. Collectively, these designs also enable
a seamless transition between real-world robots and simulation environments.
DecoupledInferenceArchitecture. Prevalent open-source deployment scripts often entangle model initial-
ization with robot control loops. This coupling leads to severe dependency conflicts (e.g., between model
libraries and hardware drivers) and hinders model switching. To resolve this, RoboOrchard implements a
decoupled Client-Server Architecture. On the server side, we provide a Flask-based Inference Service. It
can directly load standardized model bundle without modification and can be deployed locally or remotely
to isolate environments. This single service unifies inference for both simulation and physical hardware.
On the robot client side, we provide a lightweight Generic ROS2 Client. By reading the metadata from
the model bundle, this node dynamically configures its subscription (observation) and publication (action)
topics, formatting raw sensor data into standardized requests for the inference server.
InferenceModes. To accommodate diverse task requirements, the ROS2 client supports two distinct infer-
ence modes: (1) Synchronous mode: Enforces strict “Observation-Inference-Execution” timing. It is suited
for model debugging and quasi-static manipulation tasks. (2) Asynchronous mode: Decouples perception
and inference frequencies via non-blocking callbacks and timestamp alignment. This significantly improves
responsivenessinhighlydynamictasks. Crucially,theclientfeedsbackexecutionlatencyandunexecutedac-
tionhistorytothemodelserver. Thiscontextenablesserver-sidesmoothingalgorithms,suchasSimpleRTC,
to generate temporally consistent action chunks that compensate for asynchronous delays.
InteractiveEvaluationInterface. To close the loop between model evaluation and data expansion, we seam-
lessly integrated the deployment runtime into the data acquisition Companion App. This unified interface
provides centralized control over both the model inference server and the ROS2 Robot Client. Specifically,
userscaneasilymanagetheserverlifecycle(e.g.,specifyingmodelpathsandlaunchingservices)whilesimul-
taneouslycommandingtheclientexecutionflowviafine-grainedcontrols(e.g.,Start,Pause,andTakeover).
Coupled with real-time recording, this design transforms the deployment tool into a powerful data engine,
enabling the eﬀicient collection of both automatic model rollouts and human intervention data, thereby
accelerating the iterative improvement of policies. See Appendix xx for more details of companion App.
10

6 Experiments
In this section, we conduct extensive experiments to evaluate the effectiveness of our proposed HoloBrain-0
model. Our evaluation is two-fold: First, we benchmark our method against state-of-the-art (SOTA) base-
lines across 10 diverse real-world manipulation tasks and 4 representative simulation benchmarks. Second,
we present a detailed analysis of key experiments that offer valuable insights, including how multi-task co-
training improves success rates, and how our proposed joint training and inference-time strategies enhance
the smoothness and performance of asynchronous inference in dexterous tasks.
6.1 ImplementationDetails
WeadoptGroundingDINOTiny[19]andQwen2.5-VL-3B[8]asourVLMbackbones. ForQwen2.5-VL-3B,
we freeze both the vision and text encoders to preserve their pre-trained capability to extract semantic
representations. Importantly,fortheLLMcomponent,weretainonlythefirsttransformerlayeranddiscard
all subsequent layers to reduce computational overhead. The resulting parameter statistics are detailed in
Tab. 2, with HoloBrain-0-QW containing 1.1B parameters and HoloBrain-0-GD containing 0.2B. Compared
with prevalent VLA models such as GR00T [12], π [10], and RDT [18], HoloBrain-0 features a significantly
0
morelightweightactionexpert. Thisalignswithahierarchicaldesignphilosophy: theVLMbackboneactsas
the“brain”forsemanticreasoning, whiletheactiondecoderissolelyresponsibleforexecution. Thisfocused
roleallowstheaction expertto requiresignificantlyfewerparameters, resultingin a lightweightarchitecture
that enables eﬀicient deployment on resource-constrained edge devices (e.g., RDK S100 [35]).
Table2: Modelparametercounts(inmillions). GDdenotesGroundingDINOTiny,QWrepresentsQwen2.5-
VL-3B. LM refers to the language model component. In GD, the LM consists of a BERT module and a
feature enhancer. For QW, we retain only the first layer of its LM, resulting in a reduced parameter size of
388.24M. We freeze the BERT module in GD and the vision encoder in QW during training.
Model Vision Encoder LM Spatial Enhancer Action Expert Trainable All
HoloBrain-0-GD 29.64 130.80 2.28 20.79 74.81 183.70
HoloBrain-0-QW 668.68 388.24 2.09 20.79 412.17 1080.86
TrainingDetails. During the pretraining stage, both HoloBrain-0-QW and HoloBrain-0-GD are trained for
200k steps, with batch sizes of 2048 and 512, respectively. The learning rate remains fixed at 1×10−4
throughout the entire pretraining phase. In the post-training stage, the number of training steps is selected
within the range of 100k–200k depending on the dataset size. The learning rate starts at 1×10−4 and is
decayed to 1×10−5 during the final 10% of the training steps. The batch sizes for post-training are set to
256 for HoloBrain-0-QW and 128 for HoloBrain-0-GD. The AdamW optimizer is used consistently across all
stages. Refer to Appendix A for more implementation details.
6.2 ResultsonReal-worldTasks
RealWorldTaskSetup. We evaluate our models on the Dual-arm Piper embodiment setting (Fig. A2). As
illustratedinFig.5,wedesignedacomprehensivesuiteofreal-worldexperimentscategorizedintotwoprimary
groups to rigorously evaluate our model. The first category consists of 7 fundamental tasks (short-horizon
dexterous, single-step, and multi-step pick-and-place). We collect only 200 episodes per task and train a
single multi-task model, aiming to validate the model’s learning eﬀicacy with limited post-training data.
The second category targets challenging, long-horizon tasks, including cloth folding, box folding, and grasp
anything. The first two tasks involve the long-horizon manipulation of deformable objects, representing a
researchdirectioncurrentlyattractingsignificantattention. Incontrast, thegraspanythingtaskemphasizes
object diversity. Conditioned on a single high-level instruction (e.g., “cleanup desktop”), the model must
clear a wide variety of objects from a table into a basket. During evaluation, the object set is evenly divided
11

Figure 5: Real-world evaluation task suite for HoloBrain-0. The suite comprises 7 basic tasks (shaded in
gray), 2 long-horizon dexterous manipulation tasks, and 1 general object pick-and-place task.
betweenseenandunseenitems. Utilizingadatasetofapproximately30hourspertask,weadoptatest-driven
paradigm to validate the synergy between our model and the data collection pipeline.
For quantitative evaluation, we measure the success rate and task-specific progress score (detailed in Ap-
pendix B) over average 20 trials per task. Crucially, to guarantee a fair comparison while covering a diverse
range of initial states, we strictly utilize a fixed set of pre-defined object poses for every evaluation roll-
out. Specifically, to ensure evaluation consistency, the fold clothes task is evaluated starting from Step 3
(Adjusting); the complete pipeline is illustrated in Fig. A4.
Table 3: Real-world robot experiment results. Each cell follows the format “progress score / success rate”.
model Foldtowel Placeemptycup Placeshoe Stackblocksthree Stackbowlsthree Putbottlesbasket
π 61.58/31.58 48.5/30.00 75.48/48.39 70.00/13.33 97.78/93.33 55.24/21.43
0
π 61.58/63.16 99.50/95.00 84.19/54.84 80.00/26.67 100.00/100.00 94.29/78.57
0.5
HB-GD 95.26/84.21 89.50/85.00 96.77/96.77 81.11/40.00 98.22/80.00 96.67/78.57
HB-QW 84.74/84.21 78.50/70.00 93.23/93.55 83.33/46.67 100.00/100.00 95.24/85.71
model Placetoslot Graspanything Foldclothes Foldpaperbox Averageprogress Averagesuccessrate
π 68.00/33.33 87.50/87.50 33.33/15.00 86.00/80.00 68.34 45.39
0
π 84.22/60.00 98.40/98.40 60.95/50.00 81.50/65.00 84.46 69.16
0.5
HB-GD 80.00/60.00 93.50/93.50 67.62/55.00 82.00/75.00 88.07 74.81
HB-QW 62.22/26.67 95.00/95.00 81.43/75.00 99.50/95.00 87.32 77.18
ResultsAnalysis. WecompareHoloBrain-0withπ andπ ,andtheresultsaresummarizedinTable3. Asa
0 0.5
baseline,π achievesaprogressscoreof68.34andasuccessrateof45.39%. Comparedtoπ ,π makesonly
0 0 0.5
minormodificationstothemodelarchitecturebutundergoesmoreextensiveandbetter-designedpretraining;
its real-world performance improves significantly, particularly excelling in pick-and-place tasks such as place
empty cup and grasp anything. Compare with π , HoloBrain-0 achieves superior performance: HoloBrain-
0.5
0-GD and HoloBrain-0-QW outperform π by average success rates of 5.65% and 8.02%, respectively,
0.5
across the 10 evaluated tasks. Further experimental findings are summarized as follows:
• HoloBrain-0 substantially outperforms π on two long-horizon tasks, fold clothes and fold paper box,
0.5
with success rates improved by 25% and 30%, respectively.
12

Table 4: Evaluation on the RoboTwin2.0 benchmarks (Clean vs Randomized, 50 tasks). The performance
metrics for π [17] are cited from Lingbot-VLA [38], while the results for X-VLA [14] are sourced from
0.5
Motus [39]. See Table A4 and Table A5 for our full results.
π X-VLA Lingbot-VLA Motus HoloBrain-0-GD HoloBrain-0-QW
0.5
Simulation Task (3B) (0.9B) (4B) (8B) (0.2B) (1.1B)
Clean Rand. Clean Rand. Clean Rand. Clean Rand. Clean Rand. Clean Rand.
PlaceDualShoes 75% 75% 79% 88% 87% 86% 93% 87% 92% 95% 96% 96%
MoveStaplerPad 56% 42% 78% 73% 74% 48% 83% 85% 74% 77% 73% 84%
StackBlocksTwo 97% 100% 92% 87% 100% 99% 100% 98% 100% 97% 100% 99%
ScanObject 72% 65% 14% 36% 92% 96% 67% 66% 85% 80% 84% 84%
PlaceObjectStand 91% 85% 86% 88% 93% 88% 98% 97% 92% 93% 94% 94%
PlaceFan 87% 85% 80% 75% 92% 87% 91% 87% 90% 92% 96% 92%
MovePillbottlePad 84% 61% 73% 71% 92% 90% 93% 96% 96% 97% 95% 91%
PickDualBottles 93% 63% 47% 36% 99% 90% 96% 90% 98% 97% 98% 96%
BlocksRankingRgb 92% 85% 83% 83% 92% 91% 99% 97% 100% 98% 98% 96%
......(50tasks)
TurnSwitch 62% 54% 40% 61% 67% 63% 84% 78% 70% 67% 89% 79%
PickDiverseBottles 81% 71% 58% 36% 88% 85% 90% 91% 86% 87% 89% 87%
PlaceBreadBasket 77% 64% 81% 71% 95% 93% 91% 94% 97% 95% 93% 90%
StackBlocksThree 91% 76% 6% 10% 96% 95% 91% 95% 96% 98% 93% 94%
PutBottlesDustbin 84% 79% 74% 77% 92% 93% 81% 79% 93% 97% 97% 98%
PlaceCanBasket 62% 62% 49% 52% 75% 72% 81% 76% 89% 80% 79% 90%
StampSeal 79% 55% 76% 82% 74% 77% 93% 92% 75% 76% 77% 85%
HangingMug 18% 17% 23% 27% 34% 53% 38% 38% 48% 45% 55% 52%
HandoverBlock 66% 57% 73% 37% 83% 95% 86% 73% 96% 93% 100% 90%
StackBowlsThree 77% 71% 76% 86% 71% 77% 79% 87% 92% 81% 88% 88%
PlaceObjectBasket 80% 76% 44% 39% 90% 88% 81% 87% 87% 81% 92% 90%
OpenMicrowave 34% 77% 79% 71% 91% 92% 95% 91% 99% 98% 97% 99%
Average (%) 82.74 76.76 72.80 72.84 88.56 86.68 88.66 87.02 91.30 90.80 91.90 92.30
• Inscenarioswithfewerstagesandlimiteddata,HoloBrain-0-GDshowscertainadvantagesoverthelarger
HoloBrain-0-QW; however, for long-horizon complex tasks, HoloBrain-0-QW is recommended.
• Benefiting from our data acquisition strategy — the iterative test-driven data strategy (Sec. 4.2), we
achieve highly robust performance on long-horizon dexterous tasks using only around 30 hours of data,
and the system can operate continuously for extended periods without getting stuck.
• For the grasp anything task, Table 3 reports the average success rates across both seen and unseen
object categories. Specifically, HoloBrain-0-QW achieves 93.5% on seen objects and 97.5% on unseen
objects. We attribute the slightly lower performance on seen objects to the inherent diﬀiculty of the test
set, whichincludesseveralobjectswithchallenging, irregulargeometries. Crucially, theseresultsindicate
thatgraspingsuccessislargelyindependentofwhetheranobjectappearedduringtraining,demonstrating
that our data collection strategy effectively equips the model with generalized grasping capabilities.
6.3 ResultsonSimulationBenchmarks
Although the sim-to-real gap persists, simulation benchmarks remain essential for evaluating a model’s
capacity to fit specific task distributions under fixed data budgets. Furthermore, certain benchmarks are
designedtotargetandevaluatespecificaxesofgeneralization. Toprovideaholisticevaluation,weutilizefour
benchmarks—RoboTwin2.0[28],LIBERO[36],LIBERO-plus[37],andGenieSimDigitWorld[29]—thereby
assessing our method’s performance across a spectrum of tasks and environments.
RoboTwin2.0Benchmark. We train a 50-task multi-task model. We utilize a dataset mix of 50 clean and
500 randomized demonstrations per task, where randomization includes background, lighting, table height,
and cluttered table. The model undergoes 200k steps of post-training. For comprehensive evaluation, we
execute 100 trials per task in both clean and randomized settings aggregating to 10,000 total rollouts. On
13

Table 5: Evaluation on LIBERO and LIBERO-Plus benchmarks. For LIBERO-Plus, we evaluate the model
trained on LIBERO in a zero-shot manner, without further fine-tuning, across seven distinct distribution
shifts: Camera, Robot, Language, Light, Background, Noise, and Layout.
LIBERO LIBERO-Plus
Methods Size
Spatial Object Goal Long Avg Cam Robot Lang Light BG Noise Layout Avg
MemoryVLA[40] 7B 98.4 98.4 96.4 93.4 96.7 - - - - - - - -
Octo[41] 0.1B 78.9 85.7 84.6 51.1 75.1 - - - - - - - -
FLOWER[42] 1B 97.1 96.7 95.6 93.5 95.7 - - - - - - - -
SmolVLA[43] 2B 93.0 94.0 91.0 77.0 88.8 - - - - - - - -
GR00T-N1[12] 3B 94.4 97.6 93.0 90.6 93.9 - - - - - - - -
OpenVLA[9] 7B 84.7 88.4 79.2 53.7 76.5 0.8 3.5 23.0 8.1 34.8 15.2 28.5 15.6
OpenVLA-OFT[44] 7B 97.6 98.4 97.9 94.5 97.1 56.4 31.9 79.5 88.7 93.3 75.8 74.2 69.6
WorldVLA[45] 1B 85.6 89.0 82.6 59.0 79.1 0.1 27.9 41.6 43.7 17.1 10.9 38.0 25.0
UniVLA[46] 7B 96.5 96.8 95.6 92.0 95.2 1.8 46.2 69.6 69.0 81.0 21.2 31.9 42.9
π [10] 3B 96.8 98.8 95.8 85.2 94.1 13.8 6.0 58.8 85.0 81.4 79.0 68.9 53.6
0
π +FAST[47] 3B 96.4 96.8 88.6 60.2 85.5 65.1 21.6 61.0 73.2 73.2 74.4 68.8 61.6
0
π [17] 3B 98.8 98.2 98.0 92.4 96.9 - - - - - - - -
0.5
X-VLA[14] 0.9B 98.2 98.6 97.8 97.6 98.1 22.2 87.8 73.1 88.2 95.3 61.8 70.7 69.7
HoloBrain-0-GD 0.2B 97.8 98.2 95.2 95.6 96.7 65.5 58.2 78.7 88.1 90.3 66.9 79.5 74.0
HoloBrain-0-QW 1.1B 97.2 99.6 97.6 95.2 97.4 66.3 49.0 65.9 94.9 93.3 73.1 78.2 72.6
this benchmark, our approach achieves SOTA-level performance, as shown in Table 4. Firstly, HoloBrain-0-
GD surpasses all existing VLA models with only 0.2B parameters, achieving a 90.8% success rate under the
randomization setting. Furthermore, HoloBrain-0-QW attains a higher success rate of 92.3%. These results
demonstrate the superior precision and stability of HoloBrain-0 in multi-task execution.
LIBEROandLIBERO-PlusBenchmark. LIBERO [36] is a widely used benchmark for evaluating robotic
policies, consisting of four task suites: LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-
Long. Each suite includes 10 tasks, with 50 human-teleoperated demonstrations per task. Following the
protocol in OpenVLA [9], we replay the oﬀicial demonstrations in simulation and discard any unsuccessful
trajectories before training. For evaluation, we run 50 independent trials per task, yielding 500 rollouts per
suite. AkeylimitationoftheoriginalLIBERObenchmarkisitslimitedenvironmentaldiversity: thetraining
and testing conditions are nearly identical. As a result, the extremely high reported success rates (often
exceeding95%)mayreflectoverfittingratherthantruerobustness. Toaddressthisissue, LIBERO-Plus[37]
introduces multi-dimensional perturbations for rigorous generalization assessment across seven axes: object
arrangement, camera viewpoints, robot initial states, language instructions, lighting, background textures,
and sensor noise. The benchmark comprises 10,030 diverse evaluation rollouts in total. Following the
standardized zero-shot protocol in LIBERO-Plus, we directly evaluate our policy trained on the original
LIBERO dataset, without any additional fine-tuning.
As detailed in Table 5, our approach demonstrates great performance across both standard and robust
evaluationprotocols. OnthestandardLIBERObenchmark,HoloBrain-0-QWachievesa97.4%successrate,
performingonparwithleadingmethodslikeX-VLA(98.1%)andOpenVLA-OFT(97.1%). Crucially,inthe
zero-shotLIBERO-PlusbenchmarkwhichdesignedtorigorouslyassessOODgeneralization,ourHoloBrain-
0-GDsetsanewstate-of-the-artwithanaveragescoreof74.0%. Thissignificantlyoutperformstheprevious
best method, OpenVLA-OFT (69.6%), and the X-VLA (69.7%), confirming that our policy learns robust,
transferable manipulation primitives rather than merely memorizing training distributions.
GenieSim2.2Benchmark(AgibotChallenge2025). While the benchmarks mentioned above focus on fixed-
base tabletop manipulation, we extend our evaluation to the GenieSim Benchmark [48]. This platform
utilizes the Agibot G1, a humanoid robot featuring a wheeled mobile base and a vertically adjustable torso.
Specifically,weadoptGenieSimv2.2,theversionservedasthebasisfortheAgibotChallenge2025[29]. This
benchmark comprises 10 diverse and challenging manipulation tasks. Each task is evaluated over 25 trials,
totaling 250 evaluation episodes. We traine a multi-task model to evaluate all tasks and tune the effective
steps used in the action chunk for each task individually. As shown in Table 6, HoloBrain-0-QW achieves
an overall score of 4.685, surpassing X-VLA’s score of 4.541. This result demonstrates that our model can
deliver strong performance on humanoid (upper-body) embodiments.
14

Table 6: Evaluation on the GenieSim 2.2 benchmark. Baselines are sourced from the oﬀicial leaderboard,
| limited | to methods | | with associated | | papers. | Values | denote progress | | scores. | | |
| ------- | ----------- | ----------- | --------------- | -------- | ------- | -------- | --------------- | ---- | ---------- | -------------- | ----- |
| Task | | | | | | RDT [18] | UniVLA | [46] | X-VLA [14] | HoloBrain-0-QW | |
| Clear | the | countertop | waste | | | 0.296 | 0.097 | | 0.622 | | 0.398 |
| Open | drawer | and | store | items | | 0.000 | 0.020 | | 0.400 | | 0.152 |
| Heat | the | food in | the microwave | | | 0.133 | 0.033 | | 0.524 | | 0.518 |
| Pack | moving | objects | from | conveyor | | 0.000 | 0.350 | | 0.280 | | 0.350 |
| Pickup | items | from | the | freezer | | 0.480 | 0.260 | | 0.424 | | 0.472 |
| Restock | supermarket | | items | | | 0.250 | 0.400 | | 0.610 | | 0.820 |
| Pack | in the | supermarket | | | | 0.825 | 1.000 | | 0.940 | | 0.940 |
| Make | a sandwich | | | | | 0.000 | 0.080 | | 0.143 | | 0.145 |
| Clear | table | in the | restaurant | | | 0.250 | 0.375 | | 0.310 | | 0.570 |
| Stamp | the | seal | | | | 0.200 | 0.180 | | 0.288 | | 0.320 |
| Total | Score | | | | | 2.434 | 2.795 | | 4.541 | | 4.685 |
Table7: Evaluationoftheeffectivenessofco-trainingfundamentaltaskswith“GraspAnything”data. Each
| cell follows | the | format: | “progress | score | / success | rate”. | | | | | |
| ------------ | --- | ------- | --------- | ----- | --------- | ------ | --- | --- | --- | --- | --- |
Co-Training Fold towel Place empty cup Place shoe Stack blocks three
| | | | 84.74 | / 84.21 | | 78.50 | / 70.00 | 93.23 | / 93.55 | 83.33 | / 46.67 |
| --- | --- | --- | ----- | ------- | --- | ----- | ------- | ----- | ------- | ----- | ------- |
✓
| | | | 88.95 | / 89.47 | | 82.00 | / 70.00 | 95.16 | / 93.55 | 91.11 | / 66.67 |
| --- | --- | --- | ----- | ------- | --- | ----- | ------- | ----- | ------- | ----- | ------- |
Co-Training Stack bowls three Put bottles basket Place to slot Average
| | | | 100.00 | / 100.00 | | 95.24 | / 85.71 | 62.22 | / 26.67 | 85.32 | / 72.40 |
| --- | --- | --- | ------ | -------- | --- | ----- | ------- | ----- | ------- | ----- | ------- |
| | ✓ | | 99.56 | / 93.33 | | 96.67 | / 78.57 | 70.89 | / 33.33 | 89.19 | 75.00 |
6.4 AblationandAnalysis
Co-TrainingwithGraspAnything. To validate whether co-training with auxiliary task data can mitigate
insuﬀicient post-training data, we conduct an ablation study where we jointly train on the Grasp Anything
task and seven basic tasks. The Grasp Anything task, with its diverse objects (varying shapes, materials,
poses) and focus on robust grasping, is chosen specifically to enhance the generalization of the grasp skill—
a foundational capability critical for nearly all basic tasks. As shown in Table 7, augmenting training
with Grasp Anything data yields significant performance gains across the seven basic tasks, with average
success rates increasing markedly compared to training on basic tasks alone. These results highlight that
leveraging data from a skill-focused auxiliary task (like Grasp Anything) is a viable approach to strengthen
| core competencies | | and | improve | generalization | | on simpler | tasks. | | | | |
| ----------------- | --- | --- | ------- | -------------- | --- | ---------- | ------ | --- | --- | --- | --- |
WeevaluatedourSimpleRTCmoduleandTeacherForcing
HowtoAchieveSmoothAsynchronousInference.
(TF) training strategy through an ablation study on the cloth folding task. Because cloth folding requires
highlysmoothmotion,itservesasastrongbenchmarkfortestingasynchronousinference. Ourexperimental
setupcomparedasynchronousinferencebaselineagainstfivemodelsutilizingSimpleRTC,eachtrainedwith
varying teacher-forcing ratios ranging from 0% (without TF) to 75%. As illustrated in Fig. 6, SimpleRTC-
based asynchronous inference significantly outperforms the synchronous baseline in both success rates and
progress scores. Furthermore, while higher teacher-forcing ratios yield substantial gains for dexterous tasks,
very low ratios (e.g., 5%) prove detrimental to performance. In Table 3, we adopted a unified ratio of
25% to balance performance across diverse tasks. Regarding eﬀiciency, Fig. 6 (b) demonstrates that while
SimpleRTC significantly reduces task completion time compared to the synchronous baseline, varying the
teacher-forcing rate has a negligible impact on eﬀiciency. In conclusion, our proposed inference-time and
training-timestrategiesexhibitstrongcomplementarity,effectivelyeliminatinginferencepausesandachieving
| smooth | control | for | complex | dynamic | tasks. | | | | | | |
| ------ | ------- | --- | ------- | ------- | ------ | --- | --- | --- | --- | --- | --- |
15

Figure 6: Analysis of the proposed smooth asynchronous inference strategy, including SimpleRTC and
Teacher Forcing (TF) training. Experiments are conducted on the cloth folding task. We benchmark a
synchronous baseline against five models utilizing SimpleRTC trained with different teacher-forcing rates.
(Left) Comparison of success rates and scores. (Right) Average inference time for successful episodes.
7 RelatedWork
ActionModelforManipulation. End-to-end robot manipulation model have advanced rapidly, with progress
achieved from multiple perspectives. Some approaches focus on modeling the probability distribution of
actions, proposing methods such as implicit behavioral cloning [49], gaussian mixture models [50], and
diffusion [4]. Others explore designing more suitable network architectures to improve manipulation perfor-
mance [5, 6, 51, 52, 53, 54, 55]. Over the past two years, spurred by the rapid advancement of VLMs [56,
57, 7, 58], an increasing number of studies have integrated VLMs with action models to build end-to-end
vision-language-action systems. These methods are typically trained on large-scale action datasets, aiming
to endow models with strong visual generalization and instruction following capabilities. OpenVLA [9] aug-
ments word vocabulary with discrete action tokens and generates actions autoregressively via a language
model. π [10, 17] attaches an additional action expert to the VLM and leverages flow matching to model
0
the action distribution. FAST [47] introduces the discrete cosine transform to encode actions for higher
training eﬀiciency. π [16] combines offline reinforcement learning and decision transformer to boost per-
0.6
formance. SpatialVLA [59] enhances VLMs with 3D positional embeddings to improve spatial reasoning,
while X-VLA [14] investigates eﬀicient heterogeneous data mixing strategies. LingBot-VLA [38] utilizes
larger-scale real-world action data to enhance model generalization. Beyond those VLA models extended
from VLMs, several large action models aim to improve performance by incorporating video generation.
GR-1 [60], Motus [39], and LingBot-VA [61] integrate video generation tasks into the training process. In
thiswork, weproposeHoloBrain-0, anovelmodelthatseekstopushtheperformanceboundariesofexisting
action models through superior architectural design, training methodology, and data acquisition strategy.
DatasetandDataStrategy. Existing data collection strategies for mitigating distribution shift generally
followthreemainparadigms. First,adversarialcollectionmethods,suchasADC[30]andMOVE[31],utilize
manualperturbationstoenhancemodelrobustness. However,theseapproachesareoftenlabor-intensiveand
susceptible to causal misalignment, particularly when predicted action chunks fail to account for stochastic
external interventions. Second, state-space augmentation strategies, exemplified by HDSpace [62], focus
on systematically expanding the state space through hierarchical sampling. Despite improving coverage,
such methods are frequently limited to initial joint states and trajectory-level diversity, often overlooking
critical variations in visual conditions and object states. Moreover, they typically treat all initial states
with uniform importance, ignoring the disproportionate impact that specific critical states may have on
overall policy performance. Finally, distinct from these offline approaches, interactive collection frameworks
like DAgger [32] and Genie Centurion [33] employ human-in-the-loop corrections to rectify policy drift in
real-time. Nevertheless, these methods suffer from diminishing sampling eﬀiciency: as the policy improves,
failure cases become increasingly rare, rendering large-scale data collection progressively impractical.
RoboticInfrastructure. Recentadvancementsinroboticinfrastructurehavecenteredondemocratizingaccess
toembodiedAI.PlatformslikeLeRobot[63],builtupontheHuggingFaceecosystem,representasignificant
leap forward by standardizing multimodal data formats and providing accessible PyTorch implementations
16

ofpoliciessuchasACTandDiffusionPolicy. Byintegratinghardwareinterfaceswithcloud-hosteddatasets,
LeRoboteffectivelylowersthebarriertoentry, enablingrapidprototypingandcross-institutionaldatashar-
ing [13]. However, while such platforms streamline development accessibility, they often face bottlenecks in
high-throughputdatahandlinganddeploymentreproducibility. Addressingtheselimitations,ourframework
RoboOrchard prioritizes eﬀiciency by adopting the MCAP format for robust logging and Apache Arrow for
zero-copy training data loading, significantly accelerating I/O compared to standard serialization. Further-
more, to bridge the fragmentation between simulation and reality often found in existing codebases, we
implement a Unified Environment Interface alongside a rigorous Model Artifact system; unlike basic check-
points, these artifacts encapsulate the full inference context to ensure self-contained deployment. Finally,
movingbeyondCLI-basedworkflows,weintroduceano-codeCompanionApp,simplifyingtheentirelifecycle
from data acquisition to model deployment.
8 Conclusion
In this work, we presented HoloBrain-0, a holistic Vision-Language-Action (VLA) framework designed to
bridgethegapbetweenfoundationmodelresearchandreliablereal-worlddeployment. Byexplicitlyinjecting
embodiment priors, such as kinematic chains and multi-view camera parameters, our architecture enables
robust 3D spatial reasoning and cross-embodiment generalization. Through a rigorous “pre-train then post-
train” paradigm supported by the open-source RoboOrchard infrastructure, HoloBrain-0 achieves state-of-
the-artperformanceacrosssimulationbenchmarks(e.g.,RoboTwin2.0,LIBERO,LIBERO-Plus,GenieSim)
and challenging real-world manipulation tasks. Finally, by open-sourcing the entire ecosystem, including
pre-trained foundations, post-trained checkpoints, and the software stack, we provide the community with
a complete, reproducible path toward high-performance generalist robotic agents.
9 FutureWork
We are actively developing the next iteration of the HoloBrain ecosystem. The primary objective of our
upcomingreleaseistoenhancetheVLApolicy’stasksuccessrate,instructionadherence,andgeneralization
capabilities, all while minimizing data acquisition costs. Specifically, we will focus on three key directions:
• Off-Policy Reinforcement Learning: While HoloBrain-0 focuses on imitation learning, our next ver-
sion will integrate off-policy reinforcement learning algorithms. This expansion aims to maximize the
utilityofdiversedatasources,includingexpertdemonstrations,policyrollouts,andhumaninterventions.
To support this, we plan to architecturally integrate a Value Model within the VLA framework.
• Rigorous Instruction Following: We observe that precise instruction following is still an under-
evaluated ability in current VLA research, especially when instructions are easy to confuse. Future work
will focus on building clearer and more thorough benchmarks to assess this ability, along with improving
the model’s reliability in carrying out easily confusable instructions.
• Advanced Co-training Strategies: Ourpreliminaryresultsshowthatmixingdatafromdifferenttasks
during post-training leads to notable synergistic gains. This suggests that co-training can help break
down complex capabilities across diverse datasets. We will further explore these strategies to improve
generalizability and support eﬀicient few-shot transfer to new robot embodiments.
17

References
[1] Leslie Pack Kaelbling and Tomás Lozano-Pérez. Hierarchical task and motion planning in the now. In
2011 IEEE international conference on robotics and automation, pages 1470–1477. IEEE, 2011.
[2] Caelan Reed Garrett, Rohan Chitnis, Rachel Holladay, Beomjoon Kim, Tom Silver, Leslie Pack Kael-
bling,andTomásLozano-Pérez.Integratedtaskandmotionplanning.Annualreviewofcontrol,robotics,
and autonomous systems, 4(1):265–293, 2021.
[3] Huihui Guo, Fan Wu, Yunchuan Qin, Ruihui Li, Keqin Li, and Kenli Li. Recent trends in task and
motion planning for robotics: A survey. ACM Computing Surveys, 55(13s):1–36, 2023.
[4] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake,
and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. The International
Journal of Robotics Research, page 02783649241273668, 2023.
[5] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion
policy. arXiv e-prints, pages arXiv–2403, 2024.
[6] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-actor: A multi-task transformer for robotic
manipulation. In Conference on Robot Learning, pages 785–799. PMLR, 2023.
[7] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz,
MaximNeumann,IbrahimAlabdulmohsin,MichaelTschannen,EmanueleBugliarello,etal.Paligemma:
A versatile 3b vlm for transfer. arXiv preprint arXiv:2407.07726, 2024.
[8] ShuaiBai,KeqinChen,XuejingLiu,JialinWang,WenbinGe,SiboSong,KaiDang,PengWang,Shijie
Wang, Jun Tang, et al. Qwen2. 5-vl technical report. arXiv preprint arXiv:2502.13923, 2025.
[9] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael
Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-
action model. arXiv preprint arXiv:2406.09246, 2024.
[10] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai,
LachyGroom,KarolHausman,BrianIchter,etal. pi0: Avision-language-actionflowmodelforgeneral
robot control. arXiv preprint arXiv:2410.24164, 2024.
[11] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn,
Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics trans-
former for real-world control at scale. arXiv preprint arXiv:2212.06817, 2022.
[12] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang,
Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist
humanoid robots. arXiv preprint arXiv:2503.14734, 2025.
[13] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham
Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic
learning datasets and rt-x models: Open x-embodiment collaboration 0. In 2024 IEEE International
Conference on Robotics and Automation (ICRA), pages 6892–6903. IEEE, 2024.
[14] Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng,
JiayinZou,YilunChen,JiaZeng,etal. X-vla: Soft-promptedtransformerasscalablecross-embodiment
vision-language-action model. arXiv preprint arXiv:2510.10274, 2025.
[15] Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with
heterogeneouspre-trainedtransformers. Advancesin neuralinformation processingsystems,37:124420–
124450, 2024.
18

[16] Physical Intelligence, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley,
Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, et al. π0.6: a vla that learns from
experience. arXiv preprint arXiv:2511.14759, 2025.
[17] P Intelligence, K Black, N Brown, J Darpinian, K Dhabalia, D Driess, A Esmail, M Equi, C Finn,
N Fusai, et al. π0.5: A vision-language-action model with open-world generalization. arxiv 2025. arXiv
preprint arXiv:2504.16054, 2025.
[18] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang
Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. In The Thirteenth
International Conference on Learning Representations.
[19] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Qing Jiang, Chunyuan Li,
Jianwei Yang, Hang Su, et al. Grounding dino: Marrying dino with grounded pre-training for open-set
object detection. In European Conference on Computer Vision, pages 38–55. Springer, 2024.
[20] XuewuLin,TianweiLin,LichaoHuang,HongyuXie,andZhizhongSu. Bip3d: Bridging2dimagesand
3dperceptionforembodiedintelligence. InProceedingsoftheComputerVisionandPatternRecognition
Conference, pages 9007–9016, 2025.
[21] Xuewu Lin, Tianwei Lin, Lichao Huang, Hongyu Xie, Yiwei Jin, Keyu Li, and Zhizhong Su. Sem:
Enhancing spatial understanding for robust robot manipulation. arXiv preprint arXiv:2505.16196, 2025.
[22] Ryan Hoque, Peide Huang, David J Yoon, Mouli Sivapurapu, and Jian Zhang. Egodex: Learning
dexterous manipulation from large-scale egocentric video. arXiv preprint arXiv:2505.11709, 2025.
[23] Kevin Black, Manuel Y Galliker, and Sergey Levine. Real-time execution of action chunking flow
policies. arXiv preprint arXiv:2506.07339, 2025.
[24] Kevin Black, Allen Z Ren, Michael Equi, and Sergey Levine. Training-time action conditioning for
eﬀicient real-time chunking. arXiv preprint arXiv:2512.05964, 2025.
[25] JiamingSong,ArashVahdat,MortezaMardani,andJanKautz. Pseudoinverse-guideddiffusionmodels
for inverse problems. In International Conference on Learning Representations, 2023.
[26] AgiBot World Team. Agibotworld-beta dataset. https://github.com/OpenDriveLab/AgiBot-World, 2024.
[27] AlexanderKhazatsky,KarlPertsch,SurajNair,AshwinBalakrishna,SudeepDasari,SiddharthKaram-
cheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid:
A large-scale in-the-wild robot manipulation dataset. arXiv preprint arXiv:2403.12945, 2024.
[28] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Qiwei Liang, Zixuan Li, Xianliang
Lin,YihengGe,ZhenyuGu,etal. Robotwin2.0: Ascalabledatageneratorandbenchmarkwithstrong
domain randomization for robust bimanual robotic manipulation. arXiv preprint arXiv:2506.18088, 2025.
[29] Jiyao Zhang, Mingjie Pan, Baifeng Xie, Yinghao Zhao, Wenlong Gao, Guangte Xiang, Jiawei Zhang,
DongLi,ZhijunLi,ShengZhang,HongweiFan,ChengyueZhao,ShukaiYang,MaoqingYao,Chuanzhe
Suo, and Hao Dong. Agibot digitalworld. https://agibot-digitalworld.com/, 2025.
[30] Siyuan Huang, Yue Liao, Siyuan Feng, Shu Jiang, Si Liu, Hongsheng Li, Maoqing Yao, and Guanghui
Ren. Adversarial data collection: Human-collaborative perturbations for eﬀicient and robust robotic
imitation learning. arXiv preprint arXiv:2503.11646, 2025.
[31] Huanqian Wang, Chi Bene Chen, Yang Yue, Danhua Tao, Tong Guo, Shaoxuan Xie, Denghang Huang,
Shiji Song, Guocai Yao, and Gao Huang. Move: A simple motion-based data collection paradigm for
spatial generalization in robotic manipulation. arXiv preprint arXiv:2512.04813, 2025.
19

[32] Stéphane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured
prediction to no-regret online learning. In Proceedings of the fourteenth international conference on
artificialintelligenceandstatistics,pages627–635.JMLRWorkshopandConferenceProceedings,2011.
[33] Wenhao Wang, Jianheng Song, Chiming Liu, Jiayao Ma, Siyuan Feng, Jingyuan Wang, Yuxin Jiang,
Kylin Chen, Sikang Zhan, Yi Wang, et al. Genie centurion: Accelerating scalable real-world robot
training with human rewind-and-refine guidance. arXiv preprint arXiv:2505.18793, 2025.
[34] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi,
Pierric Cistac, Tim Rault, Remi Louf, Morgan Funtowicz, et al. Transformers: State-of-the-art natural
language processing. In Proceedings of the 2020 conference on empirical methods in natural language
| processing: | system demonstrations, | pages 38–45, | 2020. | |
| ----------- | ---------------------- | ------------ | ----- | --- |
[35] D-Robotics. RDK S100 Series: Robot Development Kit for Embodied Intelligence. D-Robotics (Digua
| Robotics), | 2025. Accessed: 2026-02-11. | | | |
| ---------- | --------------------------- | --- | --- | --- |
[36] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero:
Benchmarkingknowledgetransferforlifelongrobotlearning.AdvancesinNeuralInformationProcessing
| Systems, | 36:44776–44791, 2023. | | | |
| -------- | --------------------- | --- | --- | --- |
[37] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo
Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of vision-language-action models.
| arXiv preprint | arXiv:2510.13626, | 2025. | | |
| -------------- | ----------------- | ----- | --- | --- |
[38] Wei Wu, Fan Lu, Yunnan Wang, Shuai Yang, Shi Liu, Fangjing Wang, Qian Zhu, He Sun, Yong Wang,
Shuailei Ma, et al. A pragmatic vla foundation model. arXiv preprint arXiv:2601.18692, 2026.
[39] HongzheBi, HengkaiTan,ShenghaoXie, ZeyuanWang,ShuheHuang, HaitianLiu, RuowenZhao, Yao
Feng, Chendong Xiang, Yinze Rong, et al. Motus: A unified latent action world model. arXiv preprint
| arXiv:2512.13030, | 2025. | | | |
| ----------------- | ----- | --- | --- | --- |
[40] Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan,
Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-language-action
| models | for robotic manipulation. | arXiv preprint | arXiv:2508.19236, | 2025. |
| ------ | ------------------------- | -------------- | ----------------- | ----- |
[41] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari,
Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. arXiv
| preprint | arXiv:2405.12213, 2024. | | | |
| -------- | ----------------------- | --- | --- | --- |
[42] MoritzReuss,HongyiZhou,MarcelRühle,ÖmerErdinçYağmurlu,FabianOtto,andRudolfLioutikov.
Flower: Democratizinggeneralistrobotpolicieswitheﬀicientvision-language-actionflowpolicies. arXiv
| preprint | arXiv:2509.04996, 2025. | | | |
| -------- | ----------------------- | --- | --- | --- |
[43] MustafaShukor,DanaAubakirova,FrancescoCapuano,PepijnKooijmans,StevenPalma,AdilZouitine,
Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-
action model for affordable and eﬀicient robotics. arXiv preprint arXiv:2506.01844, 2025.
[44] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing
| speed and | success. arXiv preprint | arXiv:2502.19645, | 2025. | |
| --------- | ----------------------- | ----------------- | ----- | --- |
[45] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song,
Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. arXiv preprint
| arXiv:2506.21539, | 2025. | | | |
| ----------------- | ----- | --- | --- | --- |
[46] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and
Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. arXiv preprint
| arXiv:2505.06111, | 2025. | | | |
| ----------------- | ----- | --- | --- | --- |
20

[47] KarlPertsch,KyleStachowicz,BrianIchter,DannyDriess,SurajNair,QuanVuong,OierMees,Chelsea
Finn, and Sergey Levine. Fast: Eﬀicient action tokenization for vision-language-action models. arXiv
preprint arXiv:2501.09747, 2025.
[48] Chenghao Yin, Da Huang, Di Yang, Jichao Wang, Nanshu Zhao, Chen Xu, Wenjun Sun, Linjie Hou,
ZhijunLi,JunhuiWu,ZhaoboLiu,ZhenXiao,ShengZhang,LeiBao,RuiFeng,ZhenquanPang,Jiayu
Li, Qian Wang, and Maoqing Yao. Genie sim 3.0 : A high-fidelity comprehensive simulation platform
for humanoid robot, 2026.
[49] PeteFlorence,CoreyLynch,AndyZeng,OscarARamirez,AyzaanWahid,LauraDowns,AdrianWong,
Johnny Lee, Igor Mordatch, and Jonathan Tompson. Implicit behavioral cloning. In Conference on
robot learning, pages 158–168. PMLR, 2022.
[50] Nur Muhammad Shafiullah, Zichen Cui, Ariuntuya Arty Altanzaya, and Lerrel Pinto. Behavior trans-
formers: Cloningkmodeswithonestone. Advancesinneuralinformationprocessingsystems,35:22955–
22968, 2022.
[51] Theophile Gervet, Zhou Xian, Nikolaos Gkanatsios, and Katerina Fragkiadaki. Act3d: 3d feature field
transformers for multi-task robotic manipulation. arXiv preprint arXiv:2306.17817, 2023.
[52] Qi Lv, Hao Li, Xiang Deng, Rui Shao, Yinchuan Li, Jianye Hao, Longxiang Gao, Michael Yu Wang,
andLiqiangNie. Spatial-temporalgraphdiffusionpolicywithkinematicmodelingforbimanualrobotic
manipulation. InProceedingsoftheComputerVisionandPatternRecognitionConference,pages17394–
17404, 2025.
[53] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina Fragkiadaki. 3d diffuser actor: Policy diffusion with
3d scene representations. In 8th Annual Conference on Robot Learning, 2024.
[54] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view
transformerfor3dobjectmanipulation. InConference on Robot Learning,pages694–710.PMLR,2023.
[55] Ankit Goyal, Valts Blukis, Jie Xu, Yijie Guo, Yu-Wei Chao, and Dieter Fox. Rvt-2: Learning precise
manipulation from few demonstrations. In RSS 2024 Workshop: Data Generation for Robotics.
[56] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Car-
los Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual
vision and language model. arXiv preprint arXiv:2305.18565, 2023.
[57] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. Advances in
neural information processing systems, 36:34892–34916, 2023.
[58] PengWang,ShuaiBai,SinanTan,ShijieWang,ZhihaoFan,JinzeBai,KeqinChen,XuejingLiu,Jialin
Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any
resolution. arXiv preprint arXiv:2409.12191, 2024.
[59] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu,
Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action
model. arXiv preprint arXiv:2501.15830, 2025.
[60] HongtaoWu,YaJing,ChilamCheang,GuangzengChen,JiafengXu,XinghangLi,MinghuanLiu,Hang
Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation.
arXiv preprint arXiv:2312.13139, 2023.
[61] Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan
Xue, Xing Zhu, et al. Causal world modeling for robot control. arXiv preprint arXiv:2601.21998, 2026.
[62] Jinrong Yang, Kexun Chen, Zhuoling Li, Shengkai Wu, Yong Zhao, Liangliang Ren, Wenqiu Luo,
Chaohui Shang, Meiyu Zhi, Linfeng Gao, et al. Bootstrapping imitation learning for long-horizon
manipulation via hierarchical data collection space. arXiv preprint arXiv:2505.17389, 2025.
21

[63] RemiCadene,SimonAlibert,AlexanderSoare,QuentinGallouedec,AdilZouitine,StevenPalma,Pepijn
Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano,
Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. Lerobot: State-of-the-art machine
learning for real-world robotics in pytorch. https://github.com/huggingface/lerobot, 2024.
[64] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep
bidirectional transformers for language understanding. In Proceedings of the 2019 conference of the
North American chapter of the association for computational linguistics: human language technologies,
| volume | 1 (long and short | papers), pages 4171–4186, | 2019. | |
| ------ | ----------------- | ------------------------- | ----- | --- |
[65] ZeLiu,YutongLin,YueCao,HanHu,YixuanWei,ZhengZhang,StephenLin,andBainingGuo. Swin
transformer: Hierarchical vision transformer using shifted windows. In Proceedings of the IEEE/CVF
| international | conference | on computer vision, | pages 10012–10022, | 2021. |
| ------------- | ---------- | ------------------- | ------------------ | ----- |
[66] Tony Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipu-
| lation with | low-cost hardware. | Robotics: | Science and Systems | XIX, 2023. |
| ----------- | ------------------ | --------- | ------------------- | ---------- |
22

A HoloBrain-0ImplementationDetails
We employ two versions of vision-language models as our base models: GroundingDINO Tiny and Qwen-
2.5-VL-3B, which are used to construct HoloBrain-0-GD and HoloBrain-0-QW, respectively. For Ground-
ingDINOTiny,allarchitecturalcomponentsandparametersareretained,withtheBERT[64]modulefrozen
during training. For Qwen-2.5-VL, the language model is pruned by retaining only the first layer, with the
vision encoder frozen. Beyond the base models, we additionally introduce two randomly initialized mod-
ules: the spatial enhancer and the action expert. The spatial enhancer adopts a Swin Transformer [65] as
its backbone to encode the depth map, and fuses the encoded depth features with the 2D image features.
The action expert comprises two transformers, one for encoding the current robot state and another for
decodingthefuturerobotstate; thedetailedarchitectureisillustratedintheFig. A1. Thehyperparameters
involved in the model and training are listed in Tab. A1. Notably, under the image resolution settings in
Tab. A1, HoloBrain-0-QW and HoloBrain-0-GD can be configured with single-GPU batch sizes of 32 and
8, respectively, requiring only approximately 30 GB of GPU memory without any optimization techniques.
This implies that the HoloBrain-0 can be trained on a wider range of GPUs. Note that HoloBrain-0-GD
requires more GPU memory because we unfroze its vision encoder.
Figure A1: Detailed architecture of Action Expert in HoloBrain-0
23

Table A1: Hyperparameter settings of HoloBrain-0. Parameters not explicitly specified for post-training
| remain | the same as in pretraining, | | such | as | learning | rate | and weight | decay. | | |
| ------ | --------------------------- | --- | ------ | ------------- | -------------- | ------- | ---------- | ------ | --- | ------- |
| | | | | Configuration | | | | | | Value |
| | | | action | expert | embedding | | channel | | | 256 |
| | | | action | expert | FFN | channel | | | | 2048 |
| | | | | attention | | heads | | | | 8 |
| | | | action | | decoder | layers | | | | 6 |
| | Model | | | state | encoder | layers | | | | 4 |
| | | | | prediction | | steps | | | | 64 |
| | | | | historical | | steps | | | | 1 |
| | | | | normalization | | | | | | RMSNorm |
| | | | | activation | | | | | | SiLU |
| | | | batch | size for | HoloBrain-0-QW | | | | | 2048 |
| | | | batch | size for | HoloBrain-0-GD | | | | | 512 |
10−4
| | | | | learning | | rate | | | | |
| --- | ----------- | --- | ------- | --------- | ------- | ---- | --- | --- | --- | ------ |
| | | | | optimizer | | | | | | AdamW |
| | | | | weight | decay | | | | | 0.0005 |
| | Pretraining | | | | | | | | | 2×105 |
| | | | | training | steps | | | | | |
| | | | teacher | | forcing | N | | | | 16 |
prefix
| | | | | smooth | L1 | beta | | | | 0.04 |
| --- | --- | --- | --------- | ------ | ------------ | ----- | --- | --- | --- | ---- |
| | | | candidate | | trajectories | | N | | | 4 |
| | | | | warmup | | steps | | | | 500 |
308×252
| | | | image | size for | HoloBrain-0-QW | | | | | |
| --- | --- | -------- | ----- | -------- | -------------- | ---------- | ----- | --- | --- | ------- |
| | | | image | size for | HoloBrain-0-GD | | | | | 320×256 |
| | | | batch | size for | HoloBrain-0-QW | | | | | 256 |
| | | | batch | size for | HoloBrain-0-GD | | | | | 128 |
| | | training | | steps | for 7 | real-world | tasks | | | 1.2×105 |
2×105
| | Post-training | training | | steps | for 3 | long-term | tasks | | | |
| --- | ------------- | -------- | -------- | ----- | ----- | --------- | ----- | --- | --- | ----- |
| | | | training | steps | for | RoboTwin | | | | 2×105 |
| | | | training | steps | for | LIBERO | | | | 2×105 |
2×105
| | | | training | steps | for | GenieSim | | | | |
| --- | --------- | --- | --------- | ----- | --------- | --------- | --- | ---- | ----------- | ------------------ |
| | | | | lr | scheduler | | | ×0.1 | for | the last 10% steps |
| | | | training | | noise | scheduler | | | | DDPM |
| | | | inference | | noise | scheduler | | | DPMSolver++ | |
| | Diffusion | | training | | diffusion | steps | | | | 1000 |
| | | | inference | | diffusion | steps | | | | 10 |
| | | | | beta | schedule | | | | squaredcos | cap v2 |
24

B Real-WorldExperimentalDetails
Weconductreal-worldexperimentsusingadual-armAgileXPiperrobotequippedwiththreeIntelRealSense
D435 RGB-D cameras. Data collection is performed via homologous teleoperation, following a paradigm
similar to ALOHA [66]. The hardware setup is illustrated in Fig. A2. All tasks involve fixed-base tabletop
manipulation. To accommodate the extensive workspace required for the cloth folding task, we employ two
distinct global camera configurations: Setting 1 (the default for standard tasks) and Setting 2 (optimized
for cloth folding). Specifically, Setting 2 elevates the camera by 25 cm relative to Setting 1, with a minor
adjustment to the pitch angle.
Figure A2: Illustration of the real-world experimental setup. Two global camera configurations are imple-
mented to accommodate the specific field-of-view requirements of different tasks.
For the “Grasp Anything” task, we collected a large-scale pick-and-place dataset involving over 200 distinct
objects. The data acquisition process was highly eﬀicient, characterized by continuous grasping sequences
of dozens of items per episode. As illustrated in Fig. A3 (a), the object set spans a broad spectrum of
categories, including rigid geometries, irregular shapes, deformable materials, and semi-transparent items.
During evaluation (Fig. A3 (b)), we tested the model on a mix of objects seen during training and a suite
of novel, unseen objects. The results demonstrate comparable success rates across both groups, suggesting
that the model has acquired robust, object-agnostic grasping capabilities and exhibits strong generalization.
Figure A3: Visualization of the ”Grasp Anything” task. (Left) The scenario during data collection. (Right)
All training objects, as well as the seen and unseen objects used during evaluation.
InTableA2,wedetailthelanguageinstructions,datacollectionprotocols(SOPs),anddefinitionsofprogress
scores for all 10 tasks. During data collection, while adhering to these protocols, we maximized the spatial
diversity of initial object placements within the available workspace. Meanwhile, for evaluation, we estab-
lished a standardized object placement guide. We strictly followed these pre-defined configurations during
testing to ensure consistency and comparability across trials. Additionally, Fig. A4 illustrates the detailed
stage-wise workflow for the two long-horizon dexterous tasks.
25

Figure A4: Illustration of the Standard Operating Procedures (SOPs) for two long-horizon dexterous tasks.
The cloth folding task consists of 8 distinct stages, while the paper box folding task involves 6 stages.
Task Name Instruction Collection SOP Progress Score Definition
Place Empty Cup Place an empty Usethearmcorrespondingtothe Total 1.0: Grip (0.5), On mat
cup on a mat. cup’s side (L/R). Top-down grip (0.2), Perfectly placed (0.3).
| | on the wall. | Place on mat | and | | |
| --- | ------------ | ------------ | --- | --- | --- |
retract.
Place Shoe Place a shoe on Use same-side arm. Top-down Total 1.0: Lift (0.4), Partial on
a mat using one grip at the middle. Place on mat mat(0.2),Fullyonmat(0.2),Di-
| arm. | and retract. | | rection | (0.2). | |
| ---- | ------------ | --- | ------- | ------ | --- |
Stack Bowls Three Stack three L-arm for left, R-arm for right, Total 1.5: Pick (0.25), Mis-
bowls. nearestarmforcenter. Gripsides aligned stack (+0.15), Perfect
| | (L/R arm | accordingly). | stack (+0.1). | Max | 3 attempt- |
| --- | -------- | ------------- | ------------- | --- | ---------- |
s/bowl.
Stack Blocks Three Stack cubes in Side-specific arm usage. Se- Total 1.5: For 3 blocks, Pick
→
RGB order. quence: Red (bottom) Green (0.25)andPlace(0.25)perblock.
| | → Blue | (top). Top-down | grip. | | |
| --- | ------ | --------------- | ----- | --- | --- |
Put Bottles Dustbin Put3bottlesinto L-arm: bottles 1 & 2. R-arm: Total 1.5: For 3 bottles, Pick
the bin. handbottle3toL-arm. Horizon- (0.3) and Place (0.2) per bottle.
| | tal grip. | Retract arms. | | | |
| --- | --------- | ------------- | --- | --- | --- |
Place to Slot Insert blocks into L-arm: Square. R-arm: Total 1.5: Pick (0.25), Within
matching slots. Cylinder/T-shape. Top-down 2cm (+0.15), Perfect placement
| | grip. Must | fully enter the | slot. (+0.1). | Max 3 attempts/block. | |
| --- | ---------- | --------------- | ------------- | --------------------- | --- |
Two Fold Towel Fold a towel Center towel. Dual arms pick Total 1.0: Pick corner (0.1), 1st
twice. bottom corners and fold up. R- fold (0.3), Pick right (0.1), 2nd
| | arm folds | right edge to the | left. fold (0.3), | Quality (0.2). | |
| --- | --------- | ----------------- | ----------------- | -------------- | --- |
Fold Clothes Fold a T-shirt Orient shirt. 1st/2nd folds on Total 21: Orientation (1), Folds
four times. sides; 3rd/4th folds after adjust- 1-4 (3, 4, 4, 4), Stacking/Storage
| | ment. Stack | or store in top-left. | (5). | | |
| --- | ----------- | --------------------- | ---- | --- | --- |
Grasp Anything Clearobjectsinto Move basket to center. Alternat- Total1.0(10objects): Success
a basket. ingarmspickobjectsandplacein (0.1),Pickonly(0.05). Max3at-
| | bin until | finished. | tempts/object. | | |
| --- | --------- | --------- | -------------- | --- | --- |
Fold Paper Box Foldapaperbox. L-arm grip, R-arm buckle. Fold Total1.0: L-grip(0.2),R-buckle
| | sequence: | 1st → 2nd → | Move to (0.1), | 1st fold (0.3), | 2nd fold |
| --- | --------- | ----------- | -------------- | --------------- | -------- |
| | top-left. | | (0.3), Store | (0.1). | |
Table A2: Task SOP and progress score definition of 10 real-world tasks. Success criteria: For place shoe,
fold towel, andplace to slot, ascoregreaterthan0.9, 0.9, and1.3, respectively, isdeemedsuccessful. Forthe
remaining tasks, success is defined as attaining the maximum achievable score.
26

Figure A5: Overview of the Proactive State Expansion strategy. (1) Vision State: We actively augment
the training distribution with diverse environmental factors, including variations in position, lighting, back-
ground, and object appearance. (2) Robot State: The method transitions from collecting redundant full
trajectories to an eﬀicient, step-wise expansion focused on critical key frames.
C EmpiricalAnalysisofTest-drivenPerformanceEvolution
During the post-training phase, Standard Operating Procedures (SOPs) are typically established to ensure
data consistency when collecting demonstrations for target tasks. However, strict adherence to SOPs intro-
duces a trade-off: while it yields standardized datasets, it significantly reduces the information entropy of
individual episodes. Consequently, models trained on such low-variance data risk overfitting to a narrow
distribution, resulting in poor generalization. To address this, we implement the Iterative Test-Driven Data
Strategy (Sec. 4.2). In this section, we detail the implementation of this strategy with cloth-folding task.
C.1 ProactiveStateExpansion
Using the cloth-folding task as a primary example, we first construct an SOP (Fig. A4) based on backward
induction. Thismethodspecifiesthetargetstatesinadvanceandthenidentifiesthekeywaypointsbytracing
the task in reverse. During data collection, we incorporate proactive state expansion to improve state diver-
sity. Vision-based state expansion, illustrated in Fig. A5(1), is applied during full-pipeline demonstrations
by deliberately increasing visual variation. This includes modifying background environments, adjusting
lighting conditions, and ensuring diverse spatial configurations of the cloth. The objective is to maximize
the incremental information contributed by each episode. For defensive robot state expansion, once a small
baseline dataset has been gathered (for example, 200 full-pipeline episodes), the data-collection strategy
shifts from complete demonstrations to step-wise acquisition with an emphasis on augmenting the robot
state, as shown in Fig. A5(2).
Defensiverobotstateexpansioncanbeimplementedinvariousforms; typicalexamplesincludeempty-grasp
recoveryandstep-wisestateexpansion. Empty-grasprecoveryisawidelyusedstrategythatenablesmodels
to remediate failed manipulation attempts. Notably, as illustrated in Fig. A5(2), step-wise state expansion
is achieved through keyframe selection and state-space augmentation around trajectory waypoints. Distinct
from the full-episode collection approach in HDSpace [62], we selectively extract brief (2–3 second) recovery
27

Figure A7: Quantitative Analysis of Iterative Training Results. Panel A highlights the positive correlation
between iteration rounds and task completion metrics, specifically noting the significant jump in Success
Rate during the final stages. Panel B illustrates the mean score progression for specific categories (e.g.,
Off-white XS, Yellow S), confirming a balanced performance gain across all test cases.
segments. By focusing on high-value error-correction behaviors, this approach maximizes the information
density of the training data.
C.2 Test-DrivenFailureRecovery
While proactive expansion broadens the state space, real-world deployment inevitably reveals specific, on-
policyweaknesses. WeaddressthesethroughTest-DrivenFailureRecovery,aclosed-loopoptimizationcycle.
As detailed in Table A3, we categorize failure modes and their frequencies based on empirical deployment
analysis. Following the workflow illustrated in Fig. A6, we then execute state expansion and targeted data
collection specifically for high-frequency failures.
As shown in Fig. A7, this strategy yields a consistent upward trend in performance. The Success Rate (SR)
escalates from an initial 0% to 75% by Iteration 4. A critical observation occurs in Iteration 4: while the
average progress increases marginally (80.5% → 81.4%), the Success Rate surges significantly (50% → 75%).
This disparity indicates that the final iteration successfully resolved ”last-mile” long-tail failure modes (e.g.,
Case 7 and Case 16 in Fig. A6 ). Although these failures have a minor impact on the progress score (as the
robot completes most of the task), correcting them is decisive for task completion.
Furthermore, we observe substantial gains in generalization (Panel B). Specifically, the ”Yellow S” garment
category, which performed poorly in Iteration 1, evolved into a top-performing class by Iteration 4. This
confirms that our targeted data collection effectively bridges generalization gaps, compensating for initial
performance disparities across diverse object variations.
C.3 DataQualityAssuranceandCuration
Beyond data scale, we identify that the intrinsic quality of demonstrations is paramount for stable policy
learning. We implement a rigorous data quality assurance protocol centered on the following four pillars:
• Data Self-containment and Standardization: To ensure geometric integrity and prevent systemic
ambiguities (e.g., quaternion conventions), all trajectories are encapsulated using Protobuf definitions.
Each data package is self-describing, incorporating essential hardware metadata including URDF models
and firmware versions. We strictly enforce that the end-effector (EE) pose link is explicitly defined
28

withintheURDF,witheverykinematiclinkmaintainingarigidparent-childframerelationshiptoensure
transform consistency.
• Visual Consistency Verification: Allcollecteddemonstrationsundergoamandatoryvalidationphase
via real-robot replay. By re-projecting the EE trajectory onto the image plane using calibrated intrinsic
and extrinsic camera parameters (as shown in Fig. 3), we perform a pixel-level consistency check. This
process allows for the systematic exclusion of invalid samples caused by calibration drifts, temporal
desynchronization, or teleoperation errors.
• Temporal Fidelity and Causal Filtering: To mitigate causal confusion in state-action mapping, we
employ automated scripts to prune non-informative static frames. However, we introduce a context-
aware filtering heuristic: static joint states are preserved if they coincide with critical task phases—such
as waiting for a container to fill or a conveyor to deliver an object—as identified through synchronized
vision and task-level metadata. This ensures that purposeful pauses are distinguished from redundant
idle data.
• Multi-embodiment Consistency: To minimize the domain gap introduced by mechanical variances,
validatedepisodesarereplayedacrossmultiplephysicalrobotentities. Thiscross-robotvalidationensures
that the learned operational logic remains invariant to specific hardware instances, effectively isolating
and rectifying discrepancies stemming from subtle calibration errors or mechanical tolerances.
C.4 FailureModeAnalysis
Despite the iterative refinements leading to version 4.0, certain ”long-tail” failure modes persist in the
complex cloth-folding task. We categorize and analyze these persistent challenges as follows:
• Progress Reversion: A primary challenge in manipulating thin-shell deformable objects is the high-
dimensionalstatespaceandtheexistenceofirreversiblefailuremodes. Weobservedcaseswherethepolicy,
unable to recover from a tangled configuration through local adjustments, caused the task progress to
revert entirely to the initial flattening phase. This ”reset-to-zero” behavior highlights the lack of robust
mid-level recovery strategies for highly disordered states.
• State Confusion: Duringthefoldingsequence, thevisualappearanceofpartiallyfoldedgarmentsoften
resemblesthatofacrumpledstate. Thisperceptualambiguityoccasionallycausesthepolicytomisidentify
thecurrenttaskstage, leadingto”stateoscillation”wheretherobotre-executesaflatteningactioninthe
middle of a folding trajectory.
• Insuﬀicient Clothes Generalization: The physical properties of garments significantly influence ma-
nipulation success. For instance, low-friction materials like silk frequently lead to ”empty grasps” or
slippage. The model struggles to generalize across more diverse sizes and intricate designs, although
performance remains consistent on standard solid-colored T-shirts.
• Low Flattening Eﬀiciency: While our Standard Operating Procedure (SOP) utilizes repetitive primi-
tives for flattening, human demonstrators often employ ”implicit heuristics”—such as specific tensioning
forces and strategic grasp point selection—that are diﬀicult to capture through limited data. Conse-
quently,themodelexhibitslowereﬀiciencyinresolvinghighlydisorderedstatescomparedtothenuanced
techniques demonstrated by human experts.
29

Table A3: Corrected Failure Frequency and Success Rate (20 Trials per Iteration)
| | | | | | Failure | Frequency |
| --- | --- | --- | --- | --- | ------- | --------- |
Stage ID Milestone / Action Description Iter 1 Iter 2 Iter 3 Iter 4
| Initial | - Initial | Setup / Score | 0 | | 0% 15% | 0% 10% |
| ------- | --------- | ------------- | --- | --- | ------ | ------ |
Preparation 0 Complete pre-folding organization (Score 1) 0% 0% 0% 5%
First Fold 1.1 Capture the first fold point (Score 2) 5% 0% 0% 0%
| | 1.2 Complete | the first | flipping action | (Score 3) | 5% 0% | 0% 0% |
| --- | ------------ | --------- | ------------------ | --------- | ----- | ----- |
| | 1.3 Complete | the first | sleeve fold (Score | 4) | 0% 0% | 0% 0% |
Second Fold 2.1 Perform downward transition adjustment (Score 5) 0% 0% 0% 0%
| | 2.2 Capture | the garment | corner (Score | 6) | 0% 0% | 0% 0% |
| --- | ----------- | ----------- | ------------- | --- | ----- | ----- |
2.3 Complete the second flipping action (Score 7) 35% 10% 10% 0%
| | 2.4 Complete | the second | sleeve fold | (Score 8) | 0% 0% | 0% 0% |
| --- | ------------ | ---------- | ----------- | --------- | ----- | ----- |
Third Fold 3.1 Transition to target position 3 (Score 9) 5% 0% 10% 0%
| | 3.2 Capture | the garment | corner (Score | 10) | 5% 0% | 0% 0% |
| --- | ------------ | ----------- | ------------- | ---------- | ------ | ----- |
| | 3.3 Complete | the third | fold (Score | 11) | 0% 0% | 0% 5% |
| | 3.4 Complete | the nudging | adjustment | (Score 12) | 10% 5% | 0% 0% |
Fourth Fold 4.1 Transition to target position 4 (Score 13) 10% 10% 0% 0%
| | 4.2 Capture | the garment | corner (Score | 14) | 0% 0% | 0% 0% |
| --- | ------------ | ----------- | ------------- | --- | ----- | ----- |
| | 4.3 Complete | the fourth | fold (Score | 15) | 0% 0% | 0% 5% |
4.4 Complete the nudging adjustment (Score 16) 20% 20% 30% 0%
Stacking 5.1 Shift garment to the left (Score 17) 0% 0% 0% 0%
| | 5.2 Relocate | garment | to the right (Score | 18) | 5% 5% | 0% 0% |
| --- | ------------ | --------------- | ------------------- | ----------------- | -------- | ------- |
| | 5.3 Stack | current garment | onto pile | (Score 19) | 0% 0% | 0% 0% |
| | 5.4 Relocate | the stack | to the right | (Score 20) | 0% 0% | 0% 0% |
| | | | Total | Failure Frequency | 100% 65% | 50% 25% |
| | | | | Success Rate | 0% 35% | 50% 75% |
Figure A6: Badcase Frequency Analysis and Iterative Policy Improvement. The 3D histogram tracks the
distributionoffailuremodesacrossfouriterationrounds. Byidentifyinghigh-frequencybadcases(e.g.,Cases
7,12,13,and16),weimplementtargetedfailuremodeconstructionandstateaugmentation. Thesignificant
growth of the “Success Indicator” (yellow bars) demonstrates the effectiveness of targeted data collection in
| recovering from | specific test-driven | failures. | | | | |
| --------------- | -------------------- | --------- | --- | --- | --- | --- |
30

D DetailsResultforSimulationBenchmarks
In this section, we present detailed evaluation metrics for our model across three simulation benchmarks:
RoboTwin-2.0 (Table A5 and Table A4), and LIBERO-Plus (Table A6 and Table A7).
Table A4: Detailed results of HoloBrain-0-GD on the RoboTwin-2.0 benchmark.
Task Clean Rand. Task Clean Rand. Task Clean Rand.
Adjust Bottle 100.0 100.0 Open Microwave 99.0 98.0 Place Object Stand 92.0 92.9
Beat Block Hammer 98.0 91.0 Pick Diverse Bottles 86.0 87.0 Place Phone Stand 92.0 98.0
Blocks Ranking RGB 100.0 98.0 Pick Dual Bottles 98.0 97.0 Place Shoe 99.0 98.0
Blocks Ranking Size 85.0 87.0 Place A2B Left 70.0 76.8 Press Stapler 96.0 90.0
Click Alarmclock 99.0 100.0 Place A2B Right 72.0 66.0 Put Bottles Dustbin 93.0 97.0
Click Bell 100.0 100.0 Place Bread Basket 97.0 95.0 Put Object Cabinet 92.0 87.0
Dump Bin Bigbin 92.0 98.0 Place Bread Skillet 82.0 86.0 Rotate QRcode 90.0 89.0
Grab Roller 100.0 100.0 Place Burger Fries 99.0 99.0 Scan Object 85.0 80.0
Handover Block 96.0 93.0 Place Can Basket 89.0 80.0 Shake Horizontally 100.0 100.0
Handover Mic 100.0 100.0 Place Cans Plasticbox 100.0 99.0 Shake Bottle 100.0 100.0
Hanging Mug 48.0 45.0 Place Container Plate 99.0 100.0 Stack Blocks Three 96.0 98.0
Lift Pot 100.0 100.0 Place Dual Shoes 92.0 95.0 Stack Blocks Two 100.0 97.0
Move Can Pot 100.0 99.0 Place Empty Cup 100.0 100.0 Stack Bowls Three 92.0 81.0
Move Pillbottle Pad 96.0 97.0 Place Fan 90.0 92.0 Stack Bowls Two 95.0 96.0
Move Playingcard Away 92.0 93.0 Place Mouse Pad 76.0 76.0 Stamp Seal 75.0 76.0
Move Stapler Pad 74.0 77.0 Place Object Basket 87.0 81.0 Turn Switch 70.0 67.0
Open Laptop 95.0 100.0 Place Object Scale 87.0 85.0 Average 91.3 90.8
Table A5: Detailed results of HoloBrain-0-QW on the RoboTwin-2.0 benchmark.
Task Clean Rand. Task Clean Rand. Task Clean Rand.
Adjust Bottle 100.0 99.0 Open Microwave 97.0 99.0 Place Object Stand 94.0 94.0
Beat Block Hammer 92.0 91.0 Pick Diverse Bottles 89.0 87.0 Place Phone Stand 94.0 98.0
Blocks Ranking RGB 98.0 96.0 Pick Dual Bottles 98.0 96.0 Place Shoe 100.0 100.0
Blocks Ranking Size 81.0 91.0 Place A2B Left 77.0 81.0 Press Stapler 91.0 90.0
Click Alarmclock 99.0 99.0 Place A2B Right 74.0 73.0 Put Bottles Dustbin 97.0 98.0
Click Bell 97.0 100.0 Place Bread Basket 93.0 90.0 Put Object Cabinet 89.0 85.0
Dump Bin Bigbin 88.0 92.0 Place Bread Skillet 91.0 89.0 Rotate QRcode 89.0 95.0
Grab Roller 100.0 100.0 Place Burger Fries 98.0 95.0 Scan Object 84.0 84.0
Handover Block 100.0 90.0 Place Can Basket 79.0 90.0 Shake Horizontally 100.0 98.0
Handover Mic 100.0 100.0 Place Cans Plasticbox 100.0 100.0 Shake Bottle 100.0 99.0
Hanging Mug 55.0 52.0 Place Container Plate 100.0 99.0 Stack Blocks Three 93.0 94.0
Lift Pot 100.0 100.0 Place Dual Shoes 96.0 96.0 Stack Blocks Two 100.0 99.0
Move Can Pot 99.0 97.0 Place Empty Cup 100.0 100.0 Stack Bowls Three 88.0 88.0
Move Pillbottle Pad 95.0 91.0 Place Fan 96.0 92.0 Stack Bowls Two 97.0 96.0
Move Playingcard Away 88.0 96.0 Place Mouse Pad 82.0 83.0 Stamp Seal 77.0 85.0
Move Stapler Pad 73.0 84.0 Place Object Basket 92.0 90.0 Turn Switch 89.0 79.0
Open Laptop 97.0 98.0 Place Object Scale 91.0 97.0 Average 91.9 92.3
31

Table A6: Detailed results of HoloBrain-0-QW on the LIBERO-PLUS benchmark
Original Camera Robot Language Light Background Noise Layout Total
| Spatial 97.2 | 84.0 60.6 | 77.7 96.6 | 96.5 87.2 | 88.1 83.6 |
| ------------ | --------- | --------- | --------- | --------- |
| Object 99.6 | 87.4 47.0 | 74.2 99.7 | 96.8 89.3 | 81.1 80.9 |
| Goal 97.6 | 48.0 36.9 | 49.3 91.4 | 89.0 54.4 | 64.5 59.2 |
| Long 95.2 | 48.2 53.2 | 64.0 91.6 | 91.7 62.6 | 81.1 67.7 |
| Avg 97.4 | 66.3 49.0 | 65.9 94.9 | 93.3 73.1 | 78.2 72.6 |
Table A7: Detailed results of HoloBrain-0-GD on the LIBERO-PLUS benchmark
Original Camera Robot Language Light Background Noise Layout Total
| Spatial 97.8 | 73.9 81.4 | 96.7 94.2 | 91.4 67.2 | 92.5 85.1 |
| ------------ | --------- | --------- | --------- | --------- |
| Object 98.2 | 87.1 51.5 | 95.5 98.7 | 96.4 86.3 | 80.9 83.8 |
| Goal 95.2 | 45.1 47.4 | 42.9 75.3 | 86.8 59.4 | 64.7 58.2 |
| Long 95.6 | 57.5 55.5 | 83.0 83.2 | 87.5 54.8 | 82.0 69.9 |
| Avg 96.7 | 65.5 58.2 | 78.7 88.1 | 90.3 66.9 | 79.5 74.0 |
32
