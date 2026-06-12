XRZero-G0: Pushing the Frontier of Dexterous
Robotic Manipulation with Interfaces, Quality and
Ratios
, , , , , , , ,
JamesWang PrimoPu ZephyrFung AlexWang SamWang BenderDeng KevinWang ZividLiu Chris
, , , , , , , , , ,
Pan PandaYang AndyZhai LucyLiang ShalfunLi JohnnySun JackyXu WillTian KaiYan KohlerYe
ScottLi , QianWang , RoyGan†, HaoWang‡
XSQUAREROBOT
†Project Lead, ‡Correspondence
The acquisition of high-quality, action-aligned demonstration data remains a fundamental bottle-
neck in scaling foundation models for dexterous robot manipulation. Although robot-free human
demonstrations (e.g., the UMI paradigm) offer a scalable alternative to traditional teleoperation,
current systems are constrained by sub-optimal hardware ergonomics, open-loop workflows, and a
lack of systematic data-mixing strategies. To address these limitations, we present XRZero-G0, a
hardware-software co-designed system for embodied data collection and policy learning. The system
features an ergonomic, virtual reality interface equipped with a top-view camera and dual special-
ized grippers to directly improve collection efficiency. To ensure dataset reliability, we propose a
closed-loop collection, inspection, training, and evaluation pipeline for non-proprioceptive data. This
workflow achieves an 85% data validity rate and establishes a transparent mechanism for quality
control. Furthermore, we investigate the empirical scaling behaviors and optimal mixing ratios of
robot-free data. Extensive experiments indicate that combining a minimal volume of real-robot data
with large-scale robot-free data (e.g., a 10:1 ratio) achieves performance comparable to exclusively
real-robot datasets, while reducing acquisition costs by a factor of twenty. Utilizing XRZero-G0, we
construct a 2,000-hour robot-free dataset that enables zero-shot cross-embodiment transfer to a target
physical robot, demonstrating a highly scalable methodology for generalized real-world manipulation.
Date: April 15, 2026
ProjectRepo: https://github.com/X-Square-Robot/XRZero-G0
1 Introduction
The rapid development of generalist robot foundation models (15, 17, 1, 22, 11) relies intrinsically on the
availability of massive, high-fidelity human demonstration datasets (6). For complex dexterous manipulation,
scaling data collection while preserving precise human-robot kinematic alignment remains a formidable
challenge. Traditional paradigms, such as master-slave teleoperation or VR teleoperation, provide accurate
proprioceptive data but are constrained by spatial limitations, high hardware costs, and low collection
throughput. Consequently, portable, robot-free data collection interfaces (e.g., the UMI paradigm (8, 13))
have emerged as a highly scalable alternative. By utilizing sensorized handheld devices, this paradigm
decouples data acquisition from robotic hardware limits and unlocks the potential for large-scale, in-the-wild
manipulation capture.
Despite their significant potential, current robot-free frameworks exhibit critical bottlenecks across three
primary dimensions. First, regarding Interfaces, existing handheld systems typically rely on visual SLAM
for pose estimation. This approach is highly susceptible to tracking drift in visually degraded or dynamic
environments, often restricting continuous, long-horizon data collection and causing operational fatigue.
Second, concerningData Quality, current dataprocessingpipelinesfrequentlyoperateinan open-loopmanner.
The absence of comprehensive, automated quality inspection creates a reliability bottleneck where subtle
kinematic anomalies remain undetected, ultimately degrading policy convergence. Finally, regarding Ratios,
the community lacks systematic empirical guidelines on how to optimally combine cost-effective robot-free
6202
rpA
61
]OR.sc[
2v10031.4062:viXra

C
P
Zero-Shot
Cross-
Embodiment
Gripper
Human Demonstrations
Long-Horizon Precise Deformable Contact-Rich Vision Occlusion
Figure1 XRZero-G0enablesscalablerobot-freedatacollectionandcross-embodimentpolicytransfer. An operator utilizes
an untethered wearable system comprising a VR headset for robust spatial tracking, versatile manual grippers, and
a backpack computing unit. Trajectories captured by this system map directly onto a physical dual-arm robot
for policy training, facilitating zero-shot cross-embodiment execution. The system effectively captures high-fidelity
demonstrations across diverse conditions, including long-horizon, precision-demanding, deformable, contact-rich, and
visually occluded tasks.
demonstrations with precise, yet expensive, real-robot data. Without principled scaling behaviors, the utility
of non-proprioceptive data is significantly constrained.
This raises fundamental questions: what constitutes an optimal hardware interface for robust and
continuous collection, how can we systematically guarantee dataset quality, and what data-mixing ratios
best leverage non-proprioceptive demonstrations?
Our key insight is that addressing these challenges requires a tight co-design of hardware components,
verification pipelines, and training methodologies. To this end, we introduce (see Fig. 1), a
XRZero-G0
comprehensive framework structured to advance dexterous manipulation through targeted innovations in
interfaces, quality, and ratios. At the level, we pivot from unconstrained visual SLAM to a highly
Interface
robust wearable architecture. By integrating a commercial VR headset for stable inside-out spatial tracking,
specializeddual-modegrippers(apress-actuatedH-shapeandafinger-drivenG-shape)forkinematicalignment
(seeFig.3),andabackpackcomputingunit,XRZero-G0ensuresuninterrupted,high-frequencydataacquisition
regardless of environmental constraints.
Toguaranteesuperiordataset ,wereplacetraditionalopen-loopcollectionwithaclosed-loop“Collection-
Quality
Inspection-Training-Evaluation” pipeline. This architecture incorporates automated filtering and annotation
modules to systematically identify and discard suboptimal demonstrations before they impact policy learning,
significantly increasing the yield of usable training data. Furthermore, to rigorously validate the scalability
of this data, we conduct systematic investigations into data . We evaluate four distinct training
Ratios
regimes: a baseline trained exclusively on real-robot data, a zero-shot model utilizing solely robot-free data, a
co-training approach for representation alignment, and an aggressive data-scaling strategy (10) combining a
minimal real-robot anchor with a massive volume of robot-free trajectories. Concluding this architecture is an
automated benchmarking framework that delivers rapid evaluation of policy performance, completing a highly
efficient iteration cycle.
The core contributions of this work are summarized as follows:
• We develop a wearable hardware architecture that leverages stable
DecoupledHardwareInterfaces:
2

Table1 ComparisonofXRZero-G0withOtherUMI-basedFrameworks. XRZero-G0demonstratessuperiorperformance
in various aspects, including the highest positional accuracy (≤4mm), support for three or more views, and the ability
to natively handle multiple modalities (visual, tactile, and auditory). These unique characteristics enable XRZero-G0
to achieve high collaboration efficiency, portability, and strong cross-embodiment generalization compared to other
UMI-based frameworks.
Method Pos.Accuracy #Views Modalities(V/T/A) Coll.Efficiency Portability Cross-Embod.
|                 |      |       |     | ✓         | ★   | ★★  | ★   |
| --------------- | ---- | ----- | --- | --------- | --- | --- | --- |
| UMI (4)         |      | ∼10mm | 2   | /× /×     |     |     |     |
|                 |      |       |     | ✓/        | ★   | ★★  | ★   |
| MV-UMI (16)     |      | -     | 3   | ×/ ×      |     |     |     |
| FastUMI (13)    |      | ∼8mm  | 2   | ✓/ ×/ ×   | ★   | ★★  | ★★  |
| ActiveUMI(20)   |      | ∼4mm  | 3   | ✓/ ×/ ×   | ★★  | ★★  | ★★  |
| DexUMI (18)     |      | ∼5mm  | 1   | ✓ /✓ /×   | ★★  | ★★  | ★★  |
| UMI-FT(5)       |      | ∼5mm  | 2   | ✓/ ✓/ ×   | ★★  | ★★  | ★★  |
| TacUMI (3)      |      | ∼5mm  | 2   | ✓/ ✓/ ×   | ★★  | ★★  | ★★  |
|                 |      |       |     | ✓/        | ★★  | ★★  | ★★  |
| UMI-Underwater  | (12) | -     | 2   | ×/×       |     |     |     |
|                 |      |       |     | ✓         | ★★  | ★★  | ★★  |
| UMI-on-Air (7)  |      | -     | 2   | /× /×     |     |     |     |
| UMI-on-Legs(8)  |      | -     | 2   | ✓/ ×/×    | ★★  | ★★  | ★★  |
| RDT2(14)        |      | -     | 2   | ✓/ ×/ ×   | ★★  | ★★  | ★★  |
| XRZero-G0(Ours) |      | ≤4mm  | ≥3  | ✓ / ✓ / ✓ | ★★★ | ★★★ | ★★★ |
VR spatial tracking and heterogeneous grippers to decouple human mobility from robotic kinematics,
enabling sustained and high-throughput data capture without structural constraints.
• Closed-LoopQualityVerification: We introduce a comprehensive inspection pipeline incorporating visual
cleansingandinversekinematics(IK)validation,systematicallyresolvingthequalityassurancechallenges
| of human-centric | data | to yield an | 85% validity | rate. |     |     |     |
| ---------------- | ---- | ----------- | ------------ | ----- | --- | --- | --- |
• We establish optimal cross-domain data-mixing guidelines, demonstrating
EmpiricalData-MixingLaws:
the effect. We show that augmenting a massive volume of robot-free data
| Few-Shot | Physical | Anchoring |     |     |     |     |     |
| -------- | -------- | --------- | --- | --- | --- | --- | --- |
with a minimal real-robot anchor achieves performance comparable to purely real-robot datasets at a
| fraction | of the cost. |     |     |     |     |     |     |
| -------- | ------------ | --- | --- | --- | --- | --- | --- |
• Large-ScaleDatasetDeployment: Leveraging this framework, we construct the G0-Dataset encompassing
over 2,000 hours of validated multi-modal data. This extensive dataset supports robust spatial general-
ization and highly efficient cross-embodiment transfer to physical hardware, demonstrating a highly
| scalable | methodology | for real-world | manipulation. |     |     |     |     |
| -------- | ----------- | -------------- | ------------- | --- | --- | --- | --- |
2 RelatedWork
The Universal Manipulation Interface (UMI) establishes the foundational framework (in Table. 1) for scalable,
robot-free demonstration collection, recently evolving to support rapid, large-scale deployment. Pioneered by
Chi et al. (4), UMI utilizes a portable handheld gripper equipped with a wrist-mounted camera, an inertial
measurement unit (IMU), and robust localization to capture high-fidelity, in-the-wild human demonstrations
across unstructured environments. By employing an inference-time latency-aligned policy interface and
relative-trajectory actions, UMI facilitates the generation of hardware-agnostic visuomotor policies. These
policies demonstrate zero-shot transfer capabilities across diverse robotic platforms, enabling dynamic, precise,
bimanual, and long-horizon behaviors without the need for robot-specific fine-tuning. Building directly
upon this paradigm, FastUMI (13) introduces a comprehensive hardware-software redesign. This decoupled
architecture simplifies system integration, minimizes setup complexity, and accommodates large-scale dataset
acquisition (e.g., FastUMI-100K), thereby significantly reducing operational costs while preserving robust
real-world performance.
To address contact-rich and force-sensitive manipulation, subsequent iterations of the UMI framework have
integrated advanced multimodal sensing to capture fine-grained tactile and compliance feedback. For instance,
UMI-FT (5) augments the baseline handheld interface with compact six-axis force/torque sensors at the
3

Interfaces Quality
(Portable & Ergonomic) (Breaking the Data Black-Box)
Dev 2 Data Pipeline
Dev 1
Dev 0
Edge-Side Data Parsing Manual
Screening
Text Instructions
Fuzzy
Check
Action
IK
3-View Camera
Inspection
Streams
XRZero-G0 85% Data Validity Rate
Figure2 ArchitectureofXRZero-G0. Raw visuo-motor data is collected via an ergonomic VR interface and routed
throughamulti-tieredqualityassurancepipelinetoeliminatethedata“black-box” problem. Theresultinghigh-fidelity,
robot-free dataset is then strategically mixed with real-robot data to train foundation policy networks, demonstrating
strong positive transfer (1+1>2) for precise robotic manipulation.
fingertips,empoweringpoliciestopredictbothspatialtrajectoriesandgraspingdynamics(e.g.,graspforceand
stiffness) for the adept execution of wiping, insertion, and skewering tasks. Similarly, TacUMI (3) consolidates
ViTac tactile sensors, wrist-mounted force-torque sensing, and drift-free pose tracking into a unified, compact
gripper. This integration facilitates synchronized multimodal data acquisition and precise task segmentation,
which are critical for complex, contact-rich operations. Furthermore, exUMI (19) significantly improves
system extensibility through AR motion-capture-based proprioception, modular visuo-tactile fingertips, rotary
encoders,andautomatedcalibration. Thisarchitectureachieves100%datausabilityandsupportsaction-aware,
task-agnostic tactile representation learning via a predictive modeling framework.
Beyond proprioceptive and tactile enhancements, recent advancements within the UMI ecosystem have
expanded into active perception, dexterous manipulation, and cross-embodiment integration. ActiveUMI (3)
leverages a VR-augmented portable kit—featuring sensorized controllers and a head-mounted display—to
explicitly record operator head movements and egocentric visual attention. This active perception approach
yields policies with substantially higher in-distribution (70%) and out-of-distribution (56%) success rates
in bimanual tasks compared to passive baselines. In the domain of dexterous manipulation, DexUMI (18)
employs wearable exoskeletons and high-fidelity visual inpainting to utilize the human hand itself as the data
collection interface, effectively minimizing kinematic and appearance discrepancies to ensure seamless skill
transfer to multi-fingered robotic hands. Finally, UMI-on-Legs (8) synthesizes UMI-derived demonstrations
with simulation-trained whole-body controllers, successfully bridging the embodiment gap to enable mobile
manipulation on quadrupedal platforms. Collectively, these progressive developments solidify UMI as a
highly versatile paradigm for abundant, high-quality, robot-free data acquisition, fundamentally driving the
generalization of visuomotor learning.
3 Method
This section details the architecture of , a hardware-software co-designed framework tailored for
XRZero-G0
robust data collection and policy learning (Fig. 2). To overcome the limitations of existing non-proprioceptive
data paradigms, we construct a closed-loop pipeline encompassing spatial tracking, automated quality assess-
4

Battery
|     |     |     |     |     |     | 2000 | 3000 |
| --- | --- | --- | --- | --- | --- | ---- | ---- |
PC
|     |     |     |     |     |     | Hours | Tasks |
| --- | --- | --- | --- | --- | --- | ----- | ----- |
Headset
|     |     | Right Top | Left |     |     |     |     |
| --- | --- | --------- | ---- | --- | --- | --- | --- |
Gripper-G
G0-Datasets
Gripper-H
Figure3 TheXRZero-G0HardwareandDataset. An backpack-powered VR data collection rig equipped with multi-view
egocentriccamerasandcustomizedphysicalgrippers(H&G).Thisergonomicframeworkenablestherapidacquisition
of the large-scale G0-Dataset, encompassing 2,000 hours of multi-modal data, and 3,000 diverse manipulation tasks.
ment, and principled data integration. The framework is systematically presented through four foundational
components: portablehardwareinterfacedesign,dataqualityverification,cross-domaindatascalingstrategies,
| and universal policy | compatibility.                         |     |     |     |     |     |     |
| -------------------- | -------------------------------------- | --- | --- | --- | --- | --- | --- |
| 3.1 Interfaces:      | RobustandErgonomicHardwareArchitecture |     |     |     |     |     |     |
Traditional teleoperation is physically constrained by robotic hardware, whereas recent robot-free paradigms
relying on handheld monocular visual SLAM are highly susceptible to tracking drift in textureless or dynamic
environments. To resolve these spatial limitations, XRZero-G0 introduces a wearable architecture that
decouples human operational dexterity from robotic kinematics while maintaining rigorous tracking stability.
| •   |     |     | The | operator is equipped | with | a high-precision | PICO 4 VR |
| --- | --- | --- | --- | -------------------- | ---- | ---------------- | --------- |
Multi-ViewSensingandAnti-DriftDesign:
headset, which provides a genuine egocentric view via an adjustable RGB camera. To mitigate the
severe visual occlusions common in complex tasks, the main egocentric view is synchronously recorded
alongside dual-wrist camera feeds. This comprehensive multi-view stream provides robust visual context
| regardless | of operational | angles. |     |              |           |              |                 |
| ---------- | -------------- | ------- | --- | ------------ | --------- | ------------ | --------------- |
| •          |                |         |     | We initially | evaluated | the tracking | accuracy across |
HeterogeneousGrippersandPrecisePoseTracking:
various controller mounting configurations to identify the optimal position and orientation for spatial
localization. To accommodate manipulation tasks of varying granularities, the system natively supports
heterogeneous end-effectors. We engineered two novel physical grippers, rigidly attaching the left and
right VR controllers to them: an H-shaped press-actuated gripper optimized for rapid, macroscopic
grasping, and aG-shaped finger-driven gripper tailored fordexterous, fine-grained manipulation. During
data acquisition, to minimize the morphological gap between human operators and the target dual-arm
robot, the spatial distance between the two VR grippers is explicitly calibrated to match the baseline
distance of the real robotic arms, thereby ensuring structural consistency. Concurrently, leveraging its
highly stable inside-out tracking technology, the PICO 4 system delivers millimeter-accurate 6-Degree-
of-Freedom (6-DoF) pose estimations in a unified world coordinate system. This facilitates the precise
extraction of translational and rotational (roll,pitch,yaw) trajectories.
(x,y,z)
• A wearable edge computing unit manages hardware-level synchro-
Edge-SideSpatiotemporalParsing:
nization. This module utilizes rigorous spatiotemporal matching to precisely align natural language
instructions, high-frequency 6-DoF controller trajectories, and 30Hz multi-view video streams. The
synchronized data packets are subsequently transmitted to a centralized server, ensuring data fidelity
| while fully  | liberating                           | the operator’s | physical workspace. |     |     |     |     |
| ------------ | ------------------------------------ | -------------- | ------------------- | --- | --- | --- | --- |
| 3.2 Quality: | AutomatedPipelineforDataVerification |                |                     |     |     |     |     |
Directly injecting raw, unverified robot-free trajectories into Vision-Language-Action (VLA) architectures
introduces imperceptible noise that degrades policy convergence. XRZero-G0 mitigates this by deploying a
5

multi-tiered post-processing pipeline designed to filter anomalies and enforce physical realism.
1. Human kinematic frequencies frequently exceed standard robotic
VisualCleansingandMotionFiltering:
control limits, inducing severe motion blur. We implement automated image quality assessment
algorithms to identify and discard severely blurred frames. Concurrently, stationary frames where
positional variance falls below a predefined threshold are downsampled, preventing the model from
| internalizing |     | passive | behaviors. |     |           |                    |     |           |            |         |
| ------------- | --- | ------- | ---------- | --- | --------- | ------------------ | --- | --------- | ---------- | ------- |
| 2.            |     |         |            |     | Utilizing | the spatiotemporal |     | alignment | parameters | and the |
KinematicRetargetingandIKValidation:
Unified Robot Description Format (URDF) of the target embodiment, human 6-DoF trajectories are
mapped directly into the robotic end-effector space. An automated Inverse Kinematics (IK) solver
processes these trajectories to rigorously filter out invalid segments that violate joint limits, encounter
| kinematic |     | singularities, | or pose | self-collision | risks. |     |     |     |     |     |
| --------- | --- | -------------- | ------- | -------------- | ------ | --- | --- | --- | --- | --- |
3. PhysicalPlaybackVerification: To guarantee high-fidelity translation to physical hardware, we establish a
closed-loop playback protocol. For each task category, a subset of the filtered trajectories is randomly
sampled and replayed strictly open-loop on the target dual-arm robot. Successful task completion
during this physical execution serves as the definitive benchmark for trajectory validity, ensuring that
| the | remaining | dataset | is fundamentally |     | executable. |     |     |     |     |     |
| --- | --------- | ------- | ---------------- | --- | ----------- | --- | --- | --- | --- | --- |
4. SemanticAnnotation: Prolonged continuous trajectories are segmented into discrete sub-task chunks.
We augment these segments with fine-grained semantic annotations detailing manipulated objects and
critical keyframes, facilitating both large-scale pre-training and task-specific fine-tuning.
Through this rigorous verification pipeline, the framework achieves a data validity rate of up to 85%,
| establishing | a robust                                 | foundation | for | downstream | policy | learning. |     |     |     |     |
| ------------ | ---------------------------------------- | ---------- | --- | ---------- | ------ | --------- | --- | --- | --- | --- |
| 3.3 Ratios:  | PrincipledDataMixingandScalingStrategies |            |     |            |        |           |     |     |     |     |
Acentralchallengeinscalingembodiedfoundationmodelsisdeterminingtheoptimalalgorithmicintegrationof
massive,low-costrobot-freedatawithprecise,high-costreal-robotdemonstrations. Weformulateasynergistic
data-mixing methodology where these two domains fulfill complementary roles across distinct training phases.
| •   |     |     |     |     |     | During | the | initial training | phase, large | volumes |
| --- | --- | --- | --- | --- | --- | ------ | --- | ---------------- | ------------ | ------- |
GeneralizableLatentSpaceConstructionviaPre-Training:
of XRZero-G0 data serve as a semantic and spatial generalization engine. Exposed to extensive
environmental diversity, the foundational model acquires robust visual-semantic alignment, object
affordance recognition, and topological trajectory planning capabilities. This phase establishes a
generalized multi-modal representation independent of specific robotic hardware.
| •   |     |     |     |     |     | Whilerobot-freedataprovidesprofoundenvironmental |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- |
KinematicGroundingviaProportionateFine-Tuning:
cognition, itinherentlylacksembodiment-specificlow-levelphysicalpriors. Inthesubsequentfine-tuning
phase, a highly constrained proportion of real-robot data is introduced as a kinematic anchor. This
physically accurate subset guides the pre-trained latent space to converge and align with the specific
| motor | delays, | friction | coefficients, | and | joint limits | of the target | hardware. |     |     |     |
| ----- | ------- | -------- | ------------- | --- | ------------ | ------------- | --------- | --- | --- | --- |
This structured mixing ratio methodology theoretically justifies how augmenting a minimal fraction of real-
robot data with an overwhelming volume of robot-free trajectories enables rapid zero-shot adaptation to novel
| environments,      | a   | claim empirically | validated                   |     | in Section | 5.  |     |     |     |     |
| ------------------ | --- | ----------------- | --------------------------- | --- | ---------- | --- | --- | --- | --- | --- |
| 3.4 PolicyNetwork: |     |                   | UniversalModelCompatibility |     |            |     |     |     |     |     |
XRZero-G0 is fundamentally designed to output a universal, model-agnostic embodied dataset. Rather than
being tightly coupled to a specific learning algorithm, the meticulously verified multi-modal data streams
(comprising synchronized multi-view images, language instructions, and IK-validated 6-DoF trajectories) are
formatted to provide standardized supervision. This ensures direct compatibility with the two predominant
| policy paradigms |     | driving | contemporary | robotics: |     |     |     |     |     |     |
| ---------------- | --- | ------- | ------------ | --------- | --- | --- | --- | --- | --- | --- |
• Vision-Language-Action(VLA)Paradigms: Mainstream end-to-end continuous control models require mas-
sive quantities of precise visuo-motor pairings. The XRZero-G0 dataset natively fulfills this requirement.
6

Figure4 OverviewoftheG0-Dataset. Left: A word cloud illustrating the pronounced long-tail task distribution,
heavily featuring fundamental operations alongside thousands of specialized semantic tasks. Right: Egocentric visual
perspectives captured during data acquisition. The frames demonstrate the deployment of the heterogeneous physical
end-effectors(Gripper-GfordexterousmanipulationandGripper-Hformacroscopicgrasps), augmentedwithsemantic
bounding boxes highlighting the target objects for precise multi-modal supervision.
The comprehensive spatial context from the 3-view camera configuration directly enhances robust visual
feature extraction, while the rigorously filtered 6-DoF pose trajectories serve as clean, noise-free action
labels. This high-fidelity pairing allows VLA architectures to map observations to accurate end-effector
movements without the performance degradation typically caused by anomalous human demonstrations.
• Emerging architectures incorporating predictive world models rely
WorldActionModel(WAM)Paradigms:
heavily on understanding physical transition dynamics. Our dataset naturally supports this objective
by supplying stable, high-frequency visual streams alongside fine-grained semantic annotations and
discrete temporal segmentations. This structured multi-modal temporal data explicitly assists WAMs in
establishing rigorous causal relationships between actions and subsequent environmental state changes,
thereby enabling the forward-predictive planning required for complex, long-horizon manipulation.
4 DataComposition
4.1 DatasetStatisticsandDistribution
TovalidatetheefficacyoftheXRZero-G0framework,weconstructedthecomprehensive . Utilizing
G0-Dataset
the wearable rig, human operators collected over 2,000 hours of high-fidelity, multi-modal demonstration data.
The dataset spans 3,000 distinct manipulation tasks, capturing extensive object interactions within complex,
unstructured environments.
The dataset composition exhibits a pronounced long-tail distribution (Fig. 4). The head
TaskDistribution:
of the distribution is dominated by fundamental, highly repeatable tasks (e.g., fold towel,” clean up desk,”
and “organize objects”). These substantial quantities of common interactions enable the policy network to
learn robust visual-semantic alignments and universal spatial affordances. Conversely, the long tail consists of
thousands of fine-grained, specialized tasks. This structural diversity ensures extensive semantic coverage,
facilitating the generalization capabilities of the model to novel operational scenarios.
A primary structural advantage of this robot-free wearable paradigm is its exceptional
CollectionEfficiency:
data acquisition throughput. Based on dedicated continuous collection benchmarking across representative
daily tasks, operators achieved a peak collection speed of up to 93.2 episodes per hour. This high-throughput
efficiencyeffectivelyresolvesthespatialfootprintlimitationsandoperationalbottlenecksinherenttotraditional
real-robot teleoperation, demonstrating the practical viability of scaling embodied data by deeply leveraging
human kinematics.
7

5 Experiments
In this section, we comprehensively evaluate the effectiveness and universality of the proposed XRZero-G0
framework through real-world physical experiments. The experimental design is formulated to systematically
answer the following four core research questions (RQs):
• Compared to traditional physical master-slave and standard VR-based
RQ1(CollectionEfficiency):
teleoperation paradigms, what are the quantitative and qualitative advantages of the XRZero-G0 system
regarding usability and data acquisition throughput?
• Can the human-centric data collected by this framework enable
RQ2(Cross-EmbodimentFidelity):
high-fidelity trajectory replay and direct policy inference across heterogeneous robotic embodiments?
• Isitfeasibletoexecutecomplexlong-horizontasksrelyingexclusively
RQ3(PureRobot-FreeDataScaling):
onpurerobot-freedata? Furthermore,doesscalingthevolumeofthispuredatayieldastableperformance
improvement?
• What is the optimal quantitative mixing strategy for combining human-centric
RQ4(DataMixingLaws):
robot-free data with embodiment-specific teleoperation data to maximize policy robustness?
5.1 ExperimentalSetup
To rigorously validate cross-embodiment generalization, we deploy two structurally distinct
Embodiments:
dual-arm robotic systems. The CX001 platform emphasizes high dexterity with a multi-joint configuration,
while the EX001 platform is designed for heavy payloads and an extended operational workspace. Both
embodiments utilize the heterogeneous physical grippers detailed in Section 4.
We evaluate the data pipeline using three contemporary vision-language-action (VLA)
BasePolicyNetworks:
foundation models to demonstrate broad architectural compatibility:
• An end-to-end embodied foundation model incorporating a Unified Cross-layer Chain-of-
Wall-OSS(21):
Thought (Uni-CoT) mechanism, designed for robust language-action alignment and complex 3D spatial
reasoning.
• π 0(2): A general-purpose robot foundation model utilizing a flow-matching architecture to generate
low-level motor commands from visual observations.
• π 0.5(9): An advanced iteration of π 0 co-trained on heterogeneous multi-robot datasets and web-scale
data, optimized for open-world generalization.
Master-Slave Teleoperation XRZero-G0 Efficiency Comparison
VR Teleoperation
Figure5 QuantitativeUsabilityandEfficiencyComparison(RQ1). The XRZero-G0 framework demonstrates significant
temporal advantages over traditional Master-Slave and standard VR teleoperation paradigms. By ergonomically
decoupling human mobility from rigid robotic kinematics, the system achieves remarkable collection speedups across
varying task complexities (up to 2.33× in simple tasks), validating its high-throughput viability.
8

| 5.2 | RQ1: | UsabilityandDataCollectionEfficiency |     |     |     |     |     |     |     |     |     |     |
| --- | ---- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
To address RQ1, we conduct a comparative temporal analysis evaluating the XRZero-G0 system against
traditional physical master-slave teleoperation and standard VR teleoperation paradigms. Figure 5 illustrates
the average time required to complete manipulation tasks across varying difficulty levels.
Empirical results demonstrate that the XRZero-G0 framework yields substantial
QuantitativeEfficiency:
improvements in collection throughput. Specifically, compared to the traditional master-slave setup, the
proposed system reduces the average completion time from 35s to 15s for simple tasks, from 75s to 40s for
medium tasks, and from 120s to 70s for hard tasks. This translates to relative efficiency speedups of 2.33×,
| 1.88×, | and | 1.71×, respectively. |     |     |     |     |     |     |     |     |     |     |
| ------ | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The observed efficiency gains are primarily attributed to the ergonomic decoupling of
QualitativeErgonomics:
human mobility from robotic kinematics. Traditional master-slave systems force operators to map human
arm trajectories to structurally disparate robot joints, inducing high cognitive load. While standard VR
teleoperation mitigates spatial constraints, it relies on virtual controllers that deprive the operator of essential
tactile feedback. In contrast, XRZero-G0 employs a backpack-powered rig integrated with customized physical
grippers. This configuration preserves authentic proprioceptive feedback and unconstrained first-person
mobility, effectively minimizing the translation gap between human cognitive intention and physical execution.
|                  |          | Grasp Grape |       |                  |          | Grasp Eggplant |       |                  |          | Grasp Banana |       |     |
| ---------------- | -------- | ----------- | ----- | ---------------- | -------- | -------------- | ----- | ---------------- | -------- | ------------ | ----- | --- |
| 80               |          |             |       | 80               |          |                |       | 80               |          |              |       |     |
|                  | 0        |             |       |                  | 0        |                | 75.0% |                  | 0        |              | 75.0% |     |
|                  | Wall-OSS |             |       |                  | Wall-OSS |                |       |                  | Wall-OSS |              |       |     |
| 70               |          |             |       | 70               |          |                |       | 70               |          |              |       |     |
|                  |          |             | 62.5% |                  |          | 62.5%          | 62.5% |                  |          | 62.5%        | 62.5% |     |
| )%( etaR sseccuS |          |             |       | )%( etaR sseccuS |          |                |       | )%( etaR sseccuS |          |              |       |     |
| 60               |          |             |       | 60               |          |                |       | 60               |          |              |       |     |
| 50               |          | 50.0%       | 50.0% | 50               | 50.0%    |                |       | 50               | 50.0%    |              |       |     |
| 40               | 37.5%    |             |       | 40               |          |                |       | 40               |          |              |       |     |
| 30               |          |             |       | 30               |          |                |       | 30               |          |              |       |     |
| 20               |          |             |       | 20               |          |                |       | 20               |          |              |       |     |
|                  |          | 300         | 500   |                  | 300      |                | 500   |                  | 300      |              | 500   |     |
|                  |          | Data Volume |       |                  |          | Data Volume    |       |                  |          | Data Volume  |       |     |
Data Scale: 500 XRZero-G0 Demos Data Scale: 1000 XRZero-G0 Demos Data Scale: 2000 XRZero-G0 Demos
| 100 |     |     | H=0.4 | 0.5      | 100 |     |     | H=0.4 | 0.5      | 100 |     |     | H=0.4 | 0.5      |     |
| --- | --- | --- | ---------------- | --- | --- | --- | ---------------- | --- | --- | --- | ---------------- | --- |
|     |     |     | H=0.4 | Wall-OSS |     |     |     | H=0.4 | Wall-OSS |     |     |     | H=0.4 | Wall-OSS |     |
|     |     |     | H=0.45 | 0.5     |     |     |     | H=0.45 | 0.5     |     |     |     | H=0.45 | 0.5     |     |
80 H=0.45 | Wall-OSS 80 H=0.45 | Wall-OSS 80 H=0.45 | Wall-OSS
| )%( etaR sseccuS egarevA |                                              |                  |     | )%( etaR sseccuS egarevA |     |                  |              | )%( etaR sseccuS egarevA |          |                  |                    |     |
| ------------------------ | -------------------------------------------- | ---------------- | --- | ------------------------ | --- | ---------------- | ------------ | ------------------------ | -------- | ---------------- | ------------------ | --- |
| 60                       |                                              |                  |     | 60                       |     |                  |              | 60                       |          |                  |                    |     |
| 40                       |                                              |                  |     | 40                       |     |                  |              | 40                       |          |                  |                    |     |
| 20                       |                                              |                  |     | 20                       |     |                  |              | 20                       |          |                  |                    |     |
|                          | 0                                            |                  |     |                          | 0   |                  |              |                          | 0        |                  |                    |     |
|                          | 0                                            | 25 50            | 75  | 100                      | 0   | 25 50            | 75           | 100                      | 0        | 25 50            | 75                 | 100 |
|                          |                                              | Number of Trials |     |                          |     | Number of Trials |              |                          |          | Number of Trials |                    |     |
|                          |                                              |                  |     |                          |     |                  | Foundational |                          | grasping | tasks            | exhibit a positive |     |
| Figure6                  | ScalingLawsinPureRobot-FreeRegimes(RQ2&RQ3). |                  |     |                          |     |                  | Top:         |                          |          |                  |                    |     |
linear scaling correlation utilizing exclusively pure robot-free data (up to 500 episodes). Bottom: Evaluation of a
complexlong-horizondual-armtask. Scalingthepurerobot-freedatasetupto2,000episodesyieldsstableconvergence.
Notably, Wall-OSS demonstrates robust 3D spatial generalization across varying operation heights (H =0.4m and
0.45m), effectively overcoming the fixed-base spatial overfitting typical of traditional teleoperation datasets.
5.3 RQ2&RQ3: High-FidelityReplayandPureRobot-FreePolicyInference
To answer RQ2, we first validate the spatial transferability of the XRZero-G0 data. Subsequently, for RQ3, we
investigate the feasibility of training VLA models exclusively on pure robot-free data, sequentially evaluating
| foundational |     | grasping | and complex | dual-arm | manipulation. |     |     |     |     |     |     |     |
| ------------ | --- | -------- | ----------- | -------- | ------------- | --- | --- | --- | --- | --- | --- | --- |
9

A primary concern in human-centric data collection is
StrictDataEquivalenceandTrajectoryReplay(RQ2):
the physical realizability of the generated trajectories on actual robots. The XRZero-G0 system precisely
captures 6-DoF spatial poses within a strictly calibrated world coordinate frame. Through inverse kinematics
(IK), these trajectories map directly to the end-effectors of heterogeneous platforms (CX001 and EX001).
Real-world validation confirms that the collected data supports precise one-to-one (1:1) spatial replay, proving
that the robot-free data is functionally equivalent to conventional real-robot teleoperation data.
Building upon this equivalence, we conduct policy inference
Scaling Laws in Foundational Tasks (RQ3):
experiments utilizing exclusively pure robot-free data. Models are evaluated on three geometrically diverse
grasping tasks: Grasp Grape, Grasp Eggplant, and Grasp Banana. As depicted in the top row of Figure 6,
scaling the pure robot-free data volume from 300 to 500 episodes yields a positive linear improvement in
success rates for both π and Wall-OSS. Notably, Wall-OSS achieves a 75.0% success rate at 500 episodes in
0
the Eggplant and Banana tasks, demonstrating superior 3D spatial alignment.
To push the limits of pure robot-free data, we evaluate a
ScalingtoComplexLong-HorizonTasks(RQ3):
demanding dual-arm Flower Arrangement task. Because human operators wear the XRZero-G0 backpack,
their unconstrained bodily movements introduce dynamic variations in camera perspective and operational
height. This inherently breaks the fixed-base assumption prevalent in traditional robotic datasets.
To test spatial invariance, we scale the pure robot-free dataset significantly (up to 2,000 pure robot-free
episodes) and evaluate the models at two distinct robot heights (H =0.4m and H =0.45m). The running
average curves (bottom row of Figure 6) reveal that Wall-OSS exhibits robust convergence as data scales.
At 2,000 pure robot-free episodes, Wall-OSS achieves a 70% success rate at H =0.4m and maintains a 60%
success rate at the unseen H =0.45m height. This confirms that sufficient volumes of unconstrained, pure
robot-free data inherently endow the policy with true 3D spatial robustness, effectively overcoming the brittle
spatial overfitting common in fixed-base teleoperation.
5.4 RQ4: DataMixingLawsandCost-EfficiencyParadigms
To address RQ4, we systematically investigate the optimal scaling strategies for amalgamating cost-effective
robot-free data with high-fidelity, expensive real-robot teleoperation data. Inspired by the morphological
gap highlighted in recent human-centric collection systems (e.g., UMI), we hypothesize that while robot-free
data provides immense semantic diversity and spatial affordances, real-robot teleoperation data remains
indispensableasakinematicanchortoprovidetarget-specificphysicalpriors(e.g.,jointfriction,PIDcontroller
delays, and kinematic singularities).
To rigorously quantify this interaction without introducing confounding variables related to total dataset size,
we define a pure real-robot baseline comprising exactly 500 teleoperation episodes ( ). We
500Teleop.Baseline
evaluate our data-mixing strategies against this baseline through two distinct experimental paradigms:
• Consisting of the 500 baseline real-robot episodes augmented
DataAugmentationParadigm(1:1Ratio):
with an additional 500 robot-free episodes (Total Volume: 1,000). The objective here is to determine
whether cheap robot-free data can act as a cognitive amplifier to push the performance ceiling of an
existing, fixed-size real-robot dataset.
• Consisting of 500 robot-free episodes explicitly anchored by a
Cost-SubstitutionParadigm(10:1Ratio):
minimal footprint of only 50 real-robot episodes (Total Volume: 550). Since the total dataset volume
(550) is strictly comparable to the baseline (500), this paradigm rigorously isolates the efficacy of the
Few-Shot Anchoring mechanism, investigating whether cheap data can replace 90% of the expensive
kinematic data without performance degradation.
Models are evaluated across five diverse manipulation tasks (Figure 7).
Across all evaluated tasks, augmenting the fixed 500 robotic anchor
TheAugmentationCeiling(1:1Ratio):
trajectories with an equivalent volume of 500 robot-free trajectories triggers a substantial performance
enhancement. In the precision-demanding Inserting Flower into Vase task, the Wall-OSS success rate
increases from 50% (pure teleoperation) to 75% (1:1 mixed regime). This corroborates that even when
real-robot data is abundant, robot-free data continues to function as a powerful cognitive amplifier, supplying
10

100
80
60
40
20
)%(
etaR
sseccuS
Picking Bananas Picking Grapes Folding Towel
100% 100% 100%
100 100
87.5% 87.5% 87.5%
75.0% 75.0% 75.0% 80 75.0% 75.0% 80 75%
62.5% 62.5% 62.5% 62.5%
60 60
50% 50%
40 40
20 20
0.5 Wall-OSS 0.5 Wall-OSS 0.5 Wall-OSS
100
80
60
40
20
)%(
etaR
sseccuS
500 Teleop. Data 1:1 Ratio 10:1 Ratio
Adding Sausage to Rice Cooker Inserting Flower into Vase
100
80 75.0%
62.5% 62.5% 62.5%
60
50% 50% 50% 50% 50%
37.5% 37.5% 37.5% 40
20
0.5 Wall-OSS 0.5 Wall-OSS
Figure7 EmpiricalAnalysisofDataMixingStrategiesandCost-Efficiency(RQ4). Comparedtoa500real-robotbaseline,Data
Augmentation (1:1) adds 500 robot-free episodes to raise the performance ceiling. Meanwhile, Cost-Substitution (10:1)
(500 robot-free + 50 real-robot) maintains a comparable total dataset volume while matching baseline performance.
This demonstrates that few-shot physical anchoring effectively replaces 90% of expensive real-robot data without
capability loss.
Task 1 : Take the bouquet from the flower basket and insert it into the white vase.
Grab the bouquet from the flower basket Pass the bouquet to your left arm Raise the bouquet and aim it at the bottle opening Insert the bouquet Complete the task ✅
Task 2 : Fold the yellow towel on the table neatly.
EX001
Grasp both sides of the towel Lift the towel upwards Hold the towel with your right arm Fold it from right to left Complete the task ✅
Task 3 : Fold the yellow towel on the table neatly.
Grab grapes from the white plate Transfer grapes to the purple bowl Place grapes down Retract the robotic arm Complete the task ✅
Task 4 : Place the sausage from the plate into the rice cooker.
CX001
Press the rice cooker button Grab the first sausage Grab the second sausage Place them in the rice cooker Complete the task ✅
Figure8 Zero-ShotCross-EmbodimentExecution. Qualitativesequencesofphysicalrolloutsutilizingpoliciestrainedunder
the optimal 1:1 mixing strategy. The framework successfully translates multi-modal spatial intentions to structurally
heterogeneous dual-arm platforms (EX001 and CX001) for complex tasks, including long-horizon coordination (Task
1), highly deformable manipulation (Tasks 2 and 3), and sequential tool interaction (Task 4).
11

robust visual-semantic representations that maximize the utility of physical demonstrations without diluting
their kinematic accuracy.
The most profound insight emerges from the 10:1 cost-
Zero-Degradation Cost-Substitution (10:1 Ratio):
substitution regime. In this setup, the absolute volume of expensive real-robot data is drastically reduced
to merely 50 episodes (a 90% reduction), while maintaining a comparable total dataset size (550 vs. 500
baseline). Remarkably, the 10:1 policy demonstrates an exceptional capability to
matchorcloselyapproachthe
pure500real-robotbaseline . For instance, in the Folding Towel task, Wall-OSS achieves an 87.5% success
rate under the 10:1 regime, identical to the performance yielded by 500 pure real-robot episodes. Similarly, in
the Picking Bananas task, Wall-OSS achieves 75.0% in both the pure baseline and the 10:1 mixed setup.
We attribute this phenomenon to Few-Shot Physical Anchoring. The 500 robot-free episodes provide sufficient
environmental variance and spatial awareness, allowing the network to construct a generalized affordance
manifold. Consequently,thenetworkrequiresonlyaminimalvolumeofreal-robotdemonstrations(50episodes)
to successfully fine-tune its low-level control policies to the specific hardware kinematics.
Considering equipment maintenance, platform development, and human
EconomicViabilityforEmbodiedAI:
operational constraints, the acquisition cost of XRZero-G0 robot-free data is approximately one-twentieth ( 1 )
20
thatoftraditionalreal-robotteleoperation. Demonstratingthatacost-substitutedcompositionof500low-cost
robot-free episodes and 50 high-cost real-robot episodes yields comparable efficacy to 500 pure high-cost
real-robot episodes proves the tremendous economic viability of our framework. It presents a highly scalable
paradigm for democratizing embodied AI data collection.
To validate the real-world execution stability of policies trained
QualitativeCross-EmbodimentValidation:
under these mixed paradigms, Figure 8 illustrates continuous physical rollouts on heterogeneous platforms
(EX001 and CX001). The system reliably executes intricate multi-stage behaviors, confirming that leveraging
extensive robot-free data coupled with sparse physical anchoring effectively bridges the morphological gap.
6 ConclusionandFutureWork
6.1 Conclusion
Scaling generalist robot foundation models for dexterous manipulation has long been bottlenecked by the pro-
hibitiveacquisitioncostsandergonomicconstraintsassociatedwithhigh-fidelity, action-aligneddemonstration
data. In this work, we presented , a hardware-software co-designed framework that fundamentally
XRZero-G0
addresses these bottlenecks through innovations in decoupled human-centric interfaces, closed-loop validation,
and cost-efficient data amalgamation.
First, our backpack-powered VR interface equipped with multi-view egocentric perception and heterogeneous
physical grippers successfully decoupled human manipulation from rigid robotic kinematics. This design not
only minimized operator fatigue but also yielded a highly efficient collection throughput (93.2 episodes/hour).
Second, to resolve the prevalent “quality black box” inherent in human-centric data, we introduced an
automated Collection-Inspection-Training-Evaluation pipeline. By incorporating rigorous visual cleansing,
spatial retargeting, and physical playback validation, the system maintained an 85% deterministic spatial
validity rate.
Crucially, we systematically decoded the scaling laws and economic paradigms of cross-domain data mixing.
Rather than experiencing catastrophic distribution shifts under highly skewed data ratios, our empirical
results demonstrated a profound Few-Shot Physical Anchoring phenomenon. Specifically, coupling a large
volume of low-cost robot-free data with a minimal footprint of real-robot demonstrations (e.g., a 10:1 ratio
comprising 500 robot-free and merely 50 real-robot episodes) achieved execution success rates comparable to
a pure real-robot baseline. Given that the acquisition cost of XRZero-G0 data is approximately one-twentieth
( 1 ) that of traditional teleoperation, this finding establishes an exceptionally cost-effective scaling paradigm.
20
Ultimately, by culminating in the large-scale G0-Dataset, the XRZero-G0 framework successfully enabled
zero-shotcross-embodimenttransfertostructurallyheterogeneousdual-armrobots,providingahighlyscalable
and commercially viable infrastructure for generalized real-world manipulation.
12

6.2 FutureWork
While XRZero-G0 establishes a robust foundation for scalable Embodied AI data generation, it opens
several critical avenues for future exploration. Our subsequent research will primarily focus on the following
dimensions:
• Although the current backpack-powered rig ensures
HardwareMiniaturizationandTactileIntegration:
unconstrained mobility, the physical weight of the integrated edge-computing unit still limits ultra-long-
duration collection sessions. We intend to customise ultra-lightweight compute boards.
• GranularExplorationofCost-EfficiencyBoundaries: Building upon the Few-Shot Physical Anchoring
insights discussed in Section 5.4, we will conduct more granular scaling experiments to determine the
absolute theoretical lower bound of real-robot data required for successful kinematic alignment.
• To further push the boundaries of spatial invariance
ExpansionofTaskTaxonomytoMobileManipulation:
in VLA models, future data collection will transition from static tabletop manipulation to whole-body,
unconstrained mobile environments (e.g., dynamic navigation and bimanual tool-use in active industrial
or domestic settings). We will specifically target extreme contact-rich tasks and the manipulation of
highlydeformableobjects(e.g.,clothingfoldingandliquidpouring)toenrichthemorphologicaldiversity
of the G0-Dataset.
Bycontinuouslyrefiningthehardware-softwareacquisitionloopandprobingthelimitsofdatamixingstrategies,
we envision the XRZero-G0 paradigm serving as a universal, low-cost catalyst for deploying human-level
dexterity across open-world robotic ecosystems.
13

References
[1] Michael Ahn et al. Do as i can, not as i say: Grounding language in robotic affordances. arXiv preprint
| arXiv:2204.01691, | 2022.  | https://arxiv.org/abs/2204.01691. |     |     |     |
| ----------------- | ------ | --------------------------------- | --- | --- | --- |
| [2] Kevin Black   | et al. |                                   |     |     |     |
pi : A vision-language-action flow model for general robot policies. arXiv preprint arXiv:2410.24164, 2024.
0
[3] Tailai Cheng, Kejia Chen, Lingyun Chen, Liding Zhang, Yue Zhang, Yao Ling, Mahdi Hamad, Zhenshan Bing,
Fan Wu, Karan Sharma, et al. Tacumi: A multi-modal universal manipulation interface for contact-rich tasks.
| arXiv preprint | arXiv:2601.14550, | 2026. |     |     |     |
| -------------- | ----------------- | ----- | --- | --- | --- |
[4] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran
Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. arXiv preprint
| arXiv:2402.10329, | 2024. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
[5] Hojung Choi, Yifan Hou, Chuer Pan, Seongheon Hong, Austin Patel, Xiaomeng Xu, Mark R Cutkosky, and
Shuran Song. In-the-wild compliant manipulation with umi-ft. arXiv preprint arXiv:2601.09988, 2026.
[6] Open X-Embodiment Collaboration, Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog,
Alex Irpan, Alexander Khazatsky, Anant Rai, Anikait Singh, Anthony Brohan, et al. Open x-embodiment:
| Robotic learning | datasets | and rt-x models. | arXiv preprint | arXiv:2310.08864, | 2023. |
| ---------------- | -------- | ---------------- | -------------- | ----------------- | ----- |
[7] Harsh Gupta, Xiaofeng Guo, Huy Ha, Chuer Pan, Muqing Cao, Dongjae Lee, Sebastian Scherer, Shuran Song,
and Guanya Shi. Umi-on-air: Embodiment-aware guidance for embodiment-agnostic visuomotor policies. arXiv
| preprint arXiv:2510.02614, |     | 2025. |     |     |     |
| -------------------------- | --- | ----- | --- | --- | --- |
[8] Huy Ha, Yihuai Gao, Zipeng Fu, Jie Tan, and Shuran Song. Umi on legs: Making manipulation policies mobile
with manipulation-centric whole-body controllers. arXiv preprint arXiv:2407.10353, 2024.
[9] Physical Intelligence, Kevin Black, Noah Brown, et al. π : a vision-language-action model with open-world
0.5
generalization. arXiv preprint arXiv:2504.16054, 2025. https://arxiv.org/abs/2504.16054.
[10] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec
Radford,JeffreyWu,andDarioAmodei. Scalinglawsforneurallanguagemodels. arXivpreprintarXiv:2001.08361,
2020.
[11] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song,
Ming-Yu Liu, Chelsea Finn, et al. Cosmos policy: Fine-tuning video models for visuomotor control and planning.
| arXiv preprint | arXiv:2601.16163, | 2026. |     |     |     |
| -------------- | ----------------- | ----- | --- | --- | --- |
[12] Hao Li, Long Yin Chung, Jack Goler, Ryan Zhang, Xiaochi Xie, Huy Ha, Shuran Song, and Mark Cutkosky.
Umi-underwater: Learning underwater manipulation without underwater teleoperation. arXiv preprint
| arXiv:2603.27012, | 2026. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
[13] Kehui Liu, Chuyue Guan, Zhongjie Jia, Ziniu Wu, Xin Liu, Tianyu Wang, Shuai Liang, Pengan Chen, Pingrui
Zhang, Haoming Song, et al. Fastumi: A scalable and hardware-independent universal manipulation interface
| with dataset. | arXiv preprint | arXiv:2409.19499, | 2024. |     |     |
| ------------- | -------------- | ----------------- | ----- | --- | --- |
[14] Songming Liu, Bangguo Li, Kai Ma, Lingxuan Wu, Hengkai Tan, Xiao Ouyang, Hang Su, and Jun Zhu. Rdt2:
Exploring the scaling limit of umi data towards zero-shot cross-embodiment generalization. arXiv preprint
| arXiv:2602.03310, | 2026. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
[15] NVIDIA, Nikita Cherniadev Johan Bjorck andFernando Castañeda, Xingye Da, Runyu Ding, Linxi "Jim" Fan,
Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia,
Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish
Narayan,SoroushNasiriany,ScottReed,YouLiangTan,GuanzhiWang,ZuWang,JingWang,QiWang,Jiannan
Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao,
Ruijie Zheng, and Yuke Zhu. GR00T N1: An open foundation model for generalist humanoid robots. In ArXiv
| Preprint, | March 2025. |     |     |     |     |
| --------- | ----------- | --- | --- | --- | --- |
[16] Omar Rayyan, John Abanes, Mahmoud Hafez, Anthony Tzes, and Fares Abu-Dakka. Mv-umi: A scalable
multi-view interface for cross-embodiment learning. arXiv preprint arXiv:2509.18757, 2025.
[17] Junming Wang. Latentvla: Taming latent space for generalizable and long-horizon bimanual manipulation. In
Proceedings of the AAAI Conference on Artificial Intelligence, volume 40, pages 18593–18601, 2026.
[18] Mengda Xu, Han Zhang, Yifan Hou, Zhenjia Xu, Linxi Fan, Manuela Veloso, and Shuran Song. Dexumi: Using
humanhandastheuniversalmanipulationinterfacefordexterousmanipulation. arXiv preprint arXiv:2505.21864,
2025.
[19] Yue Xu, Litao Wei, Pengyu An, Qingyu Zhang, and Yong-Lu Li. exumi: Extensible robot teaching system with
action-aware task-agnostic tactile representation. arXiv preprint arXiv:2509.14688, 2025.
[20] Qiyuan Zeng, Chengmeng Li, Jude St John, Zhongyi Zhou, Junjie Wen, Guorui Feng, Yichen Zhu, and Yi Xu.
Activeumi: Robotic manipulation with active perception from robot-free human demonstrations. arXiv preprint
| arXiv:2510.01607, | 2025. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
14

[21] Andy Zhai, Brae Liu, Bruno Fang, Chalse Cai, Ellie Ma, Ethan Yin, Hao Wang, Hugo Zhou, James Wang, Lights
Shi, et al. Igniting vlms toward the embodied space. arXiv preprint arXiv:2509.11766, 2025.
[22] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan.
3d-vla: A 3d vision-language-action generative world model. In Proceedings of the 41st International Conference
on Machine Learning (ICML), volume 235 of Proceedings of Machine Learning Research, pages 61229–61245.
PMLR, July 2024. https://proceedings.mlr.press/v235/zhen24a.html.
15