# Psi-0: An Open Foundation Model Towards Universal Humanoid Loco-Manipulation

Source: https://arxiv.org/pdf/2603.12263

                                                       Ψ0: An Open Foundation Model Towards
                                                       Universal Humanoid Loco-Manipulation
                                                Songlin Wei1* , Hongyi Jing1* , Boqian Li1* , Zhenyu Zhao1* , Jiageng Mao1 , Zhenhao Ni1 , Sicheng He1 ,
                                            Jie Liu1 , Xiawei Liu1 , Kaidi Kang1 , Sheng Zang1 , Weiduo Yuan1 , Marco Pavone2 , Di Huang3 , Yue Wang1†
                                                                       1
                                                                           USC Physical Superintelligence (PSI) Lab 2 NVIDIA 3 WorldEngine
                                                                                   * Equal Contribution † Corresponding Author
                                                                                                https://psi-lab.ai/Psi0
arXiv:2603.12263v1 [cs.RO] 12 Mar 2026




                                         Fig. 1: Humanoid Loco-Manipulation. Ψ0 performs diverse loco-manipulation tasks in a pantry, including taking a cup from the coffee
                                         machine, pushing a cart, wiping the table, grasping a bottle and placing it in the sink, and pushing the fridge door.

                                            Abstract—We introduce Ψ0 (Psi-Zero), an open foundation            contrast to approaches that scale with noisy Internet clips or
                                         model to address challenging humanoid loco-manipulation tasks.        heterogeneous cross-embodiment robot datasets, we demonstrate
                                         While existing approaches often attempt to address this funda-        that pre-training on high-quality egocentric human manipulation
                                         mental problem by co-training on large and diverse human and          data followed by post-training on domain-specific real-world
                                         humanoid data, we argue that this strategy is suboptimal due          humanoid trajectories yields superior performance. Extensive
                                         to the fundamental kinematic and motion disparities between           real-world experiments demonstrate that Ψ0 achieves the best
                                         humans and humanoid robots. Therefore, data efficiency and            performance using only about 800 hours of human video data
                                         model performance remain unsatisfactory despite the consider-         and 30 hours of real-world robot data, outperforming baselines
                                         able data volume. To address this challenge, Ψ0 decouples the         pre-trained on more than 10× as much data by over 40% in
                                         learning process to maximize the utility of heterogeneous data        overall success rate across multiple tasks. We will open-source the
                                         sources. Specifically, we propose a staged training paradigm          entire ecosystem to the community, including a data processing
                                         with different learning objectives: First, we autoregressively pre-   and training pipeline, a humanoid foundation model, and a real-
                                         train a VLM backbone on large-scale egocentric human videos           time action inference engine.
                                         to acquire generalizable visual-action representations. Then, we
                                         post-train a flow-based action expert on high-quality humanoid
                                         robot data to learn precise robot joint control. Our research
                                         further identifies a critical yet often overlooked data recipe: in
                      I. I NTRODUCTION                             is more capable than a naive DiT. Conditioned on the visual-
                                                                   language features from the VLM, the action expert efficiently
   Humanoid robots, endowed with human-like morphology             and concurrently outputs joint-space action chunks. This stage
and dexterity, have achieved remarkable progress in whole-         enables the action expert to capture embodiment-specific dy-
body motion control [12, 28, 22, 14]. However, their ma-           namics. As a result, only a small amount of additional real-
nipulation capabilities, which could eventually unlock enor-       robot data is required for task-specific fine-tuning, after which
mous potential for society, have received less attention and       the model can rapidly acquire long-horizon, dexterous loco-
faced greater challenges. Recent advances in large language        manipulation skills.
models (LLMs) have illuminated a promising path towards               To enable effective training and deployment of our hu-
intelligence: by scaling both data and model capacity, gen-        manoid VLA, we make several key contributions. First, we
eral intelligence can emerge. Inspired by this paradigm, the       optimize a manipulation-oriented teleoperation pipeline that
robotics community has begun exploring scaling laws that are       improves lower-body stability during whole-body manipula-
suitable for agents with physical bodies. Recently, works such     tion. Second, to ensure smooth execution in the real world
as RT 1-2 [8, 48], OpenVLA [24], Gemini Robotics [38],             at inference time, we introduce training-time real-time action
GR00T [4], and Physical Intelligence’s π0 , π0.5 [5, 21] have      chunking, which mitigates motion jitter caused by model infer-
advocated training large action models using massive amounts       ence latency. Finally, we deploy our model on a real humanoid
of real robot data. These approaches provide early evidence        robot and benchmark it against state-of-the-art methods on
that the reasoning and planning abilities of large models can      several complex, long-horizon tasks. Our experiments suggest
significantly improve generalization in robotic manipulation.      that, using only 800 hours of human egocentric video and
However, these methods often rely on large-scale teleoperation     30 hours of real-robot data, our model achieves significantly
data, which is prohibitively costly and challenging to acquire     better performance than existing methods trained with more
for humanoid loco-manipulation.                                    than 10 × as much data on long-horizon loco-manipulation
   Fortunately, human egocentric videos provide a scalable         tasks. These results reveal that effective scaling requires
alternative as they capture abundant natural motion patterns       scaling the right data in the right way. We will release the
and rich behavior-level information without the expense of         full training pipeline, pre-trained model weights, deployment
robot teleoperation. However, directly transferring knowledge      code to facilitate future research.
from human videos to humanoid control is non-trivial due to
the substantial embodiment gap between humans and robots.                              II. R ELATED W ORKS
Early efforts [10, 40, 3] attempt to learn from human videos by    A. Whole-Body Dexterous Manipulation
adopting a unified human-centric state-action representation.         Humanoid whole-body control has witnessed significant
Nevertheless, learning from such heterogeneous data remains        progress in recent works [42, 12, 26, 27, 16, 1, 45, 36].
challenging due to intrinsic discrepancies between humans and      Humanoid robots are now able to mimic diverse human
humanoids, including differences in action frequency, motion       motions like running, dancing, and even flipping. Despite
dynamics, and degrees of freedom. Although these approaches        significant progress in locomotion, researchers have struggled
employ domain adaptation [10] or co-training strategies that       to achieve comparable success in humanoid dexterous loco-
mix human and robot data [40], a single monolithic policy          manipulation. LangWBC [37] and LeVERB [39] introduce
that models two fundamentally different action distributions       language-conditioned whole-body control policies, allowing
is inherently suboptimal. As a result, the learned policies        humanoid robots to robustly execute high-level and language-
still struggle to control humanoids to perform complex, long-      specified behaviors. However, these methods primarily focus
horizon tasks. Therefore, this paper studies a fundamental         on locomotion and navigation, with limited emphasis on
question: how can we effectively distill motion priors and         dexterous manipulation scenarios. In parallel, AMO [25] and
world knowledge from human egocentric videos to enable             TWIST2 [43] enable humanoid whole-body control through
robust whole-body control for humanoid robots?                     VR-based teleoperation, providing an effective framework for
   To that end, we propose a novel multi-stage training            collecting loco-manipulation data. However, they emphasize
paradigm with different learning goals for each stage: we          more on low-level control, rather than learning a precise policy
first pre-train a VLM to predict next-step actions using the       for long-horizon dexterous loco-manipulation.
human-robot unified action space. The objective of this stage         Dexterous manipulation [18], on the other hand, poses a
is to enable the model to learn task-level motion priors across    long-standing challenge due to the high degree-of-freedom
diverse activities, while also learning visual representations     control and frequent self-occlusion between palms and fingers,
aligned with downstream robotic tasks. We then train a sepa-       which make vision-based dexterous manipulation extremely
rate flow-based action expert using real humanoid robot data to    challenging. Being-H0 [30] proposes to learn from human
predict action sequences directly in the joint space. This post-   video by curating a large amount of hand-object interaction
training stage includes both task-agnostic training on cross-      videos and fine-tuning a pre-trained VLM using multiple
task humanoid data and task-specific fine-tuning on in-domain      task data like motion-infilling and translation. However, this
teleoperated demonstrations. We implement our action expert        method is limited to single-arm tabletop manipulation. To
as a multi-modal diffusion transformer (MM-DiT) [15], which        address the mentioned challenges, we propose to build a
                                                                                      Humanoid VLA
                                                                                                                                              ...
       Discrete Action Tokens 9       14   ...   40                                                      Continuous Action Chunks                   t
                                                                                                                                            ...


              Qwen3-VL-2B-Instruct                    copy              Pre-Trained
                                                                    Qwen3-VL 2B     VLM (2B)                           Action Expert (500M)             Lower-Body Controller
                                                                                (System 2)                                    (System 1)                     (System 0)

                                                                                                                       ...                  ...

                   Grasp the cup and pour the                             Pull the tray out of chips can and
                   water into the cup.                                    throw the can into trash bin.
                                                                                                               VLM Features     States     Noise            Whole-Body Control
  Human Egocentric Videos   Video Description                Head Camera View        Task Instruction                                                      (Real-Time Chunking)

              Stage 1 | Pre-Training of VLM                                         Stage 2 | Post-Training of Acton Expert                              Deployment

Fig. 2: Model Training and Deployment: First, we pre-train the VLM on the EgoDex [20] dataset to autoregressively predict the next-action
tokens in the task space. Then, we post-train the flow-based action expert using robotic data to predict action chunks in the joint space.
Finally, we implement a real-time chunking mechanism that leverages the lower-body controller to achieve smooth whole-body control.

unified VLA model for humanoid whole-body dexterous ma-                                                          III. T HE Ψ0 F OUNDATION M ODEL
nipulation.
                                                                                                   In this section, we introduce Ψ0 (Psi-Zero), a VLA model
                                                                                                for humanoid dexterous loco-manipulation. Given a natural
B. Humanoid VLAs
                                                                                                language task instruction ℓ and the current observation ot , our
   Inspired by the remarkable success of foundation models,                                     model predicts the whole-body action chunk at:t+H . The ob-
VLAs [48, 24, 5, 44, 17, 38] have emerged as a promising di-                                    servation ot contains the current head camera image It and the
rection toward bringing artificial intelligence into the physical                               whole-body proprioceptive state qt , including upper joint state,
world. π series [5, 21] demonstrate exceptional generalization                                  torso roll, pitch, yaw, and the base height. The action a ∈ R36
and robustness across challenging manipulation scenarios, in-                                   is defined as {qhand , qarm , torsorpy , hb , vx , vy , vyaw , pyaw },
cluding dual-arm and mobile manipulation. GR00T [4] further                                     where qhand ∈ R14 and qarm ∈ R14 are the two hand and arm
open-sources the first foundation model for humanoid robots,                                    joints respectively, torsorpy ∈ R3 is the torso roll, pitch, yaw.
trained on a large-scale mixture of real-world and synthetic                                    hb ∈ R is the base height of the humanoid and vx , vy ∈ R are
data generated from videos. However, in contrast to them,                                       the horizontal linear velocities, and vyaw ∈ R denotes angular
we find that training on higher-quality data is more critical                                   velocity around the upward direction. pyaw ∈ R is the target
than simply scaling to large volumes of heterogeneous cross-                                    yaw rotation. We employ an RL-based control policy [25]
embodiment data. In this work, we explore a new paradigm                                        to control the lower body and torso joints throughout data
for training humanoid VLAs that leverages large-scale human                                     collection and policy evaluation.
egocentric video data, complemented by a smaller amount of
real robot interaction data.                                                                    A. Model Architecture
                                                                                                   Ψ0 is a foundation model that adopts a triple-system archi-
C. Learning From Egocentric Videos
                                                                                                tecture, following prior work [21, 4]. As shown in Fig. 2,
   Data scarcity remains a fundamental constraint in training                                   the high-level policy consists of two end-to-end–trained com-
VLAs, as teleoperation data collection is less efficient and                                    ponents: a vision–language backbone (system-2) and a multi-
more expensive to scale. In contrast, human video data con-                                     modal diffusion transformer (MM-DiT) action expert (system-
tains rich prior knowledge of human–object interactions [33,                                    1). We use the state-of-the-art vision–language foundation
23, 41], providing a scalable alternative. Recent approaches,                                   model Qwen3-VL-2B-Instruct [2] as system-2. The action
such as EgoVLA [40] and In-n-On [10], co-train their models                                     expert is implemented as a flow-based MM-DiT inspired
on human video and robot data to predict unified human wrist                                    by Stable Diffusion 3 [15], containing approximately 500M
and hand actions, followed by inverse kinematics (IK) during                                    parameters. Compared to a naive DiT-based action head,
inference to map these predictions to robot actions. Similarly,                                 this design enables more efficient fusion of action and vi-
H-RDT [3] trains a large diffusion transformer (DiT) to predict                                 sion–language features. Conditioned on hidden features from
arm and hand actions in the end-effector space. However,                                        the VLM backbone, the action expert predicts future whole-
co-training the model end-to-end on a mixture of humanoid                                       body action chunks at:t+H . The 8-DoF lower-body actions
and non-humanoid robot data is suboptimal, as the model                                         {torsorpy , hb , vx , vy , vyaw , pyaw } are passed to system-0, a
must simultaneously learn two fundamentally different action                                    RL–based tracking policy. We adopt the off-the-shelf con-
distributions. Instead, we identify a critical yet overlooked                                   troller AMO [25], which maps these inputs to 15-DoF lower-
training recipe: after pre-training with next-action prediction                                 body joint angles qlower ∈ R15 , including 3 DoF waist and
to learn task semantics and visual representations, we post-                                    12 DoF leg joint. Together with the 28-DoF upper-body joints
train the action expert to directly model actions in the joint                                  (qarm , qhand ), the system outputs 43-DoF actions for whole-
space, thereby avoiding the inefficiencies of co-training.                                      body control.
                                                                               500,000 randomly sampled actions from EgoDex [20]. The
                                                                               final trained tokenizer achieves an average L1 reconstruction
        VL                       A                             A          VL   loss of 0.005, and compresses each action sequence from 48
                                     c
                                                                               tokens to a variable token length N ≈ 20. Then, the VLM is
                    c                                    Q     K V             trained autoregressively to predict next-action tokens, i.e., to




                                                FiLM
FiLM




                                         FiLM
        c                                                Self Attention
                                                                               maximize
                                                                                                         N
       Q             K               V
                                                                                                         Y
               Joint Attention
                                                               V         QK                     pθ (a) =    pθ (at |a<t , ℓ, ot ).          (1)
                                                         Cross Attention                                 t=1
                     s
                                                                                  2) Post-Training on Cross-Task Real Humanoid Data:
                                                                               After the VLM backbone is trained, we freeze its parameters
            (a) MM-DiT for VLA                         (b) Naive DiT Head      and train the action expert from scratch. Conditioning on
Fig. 3: MM-DiT for VLA: Comparison of MM-DiT architecture                      the hidden feature extracted from the VLM backbone zt =
with naive DiT. τ is the flow timestep and VL and A denotes hidden             fθvlm (ot , ℓ), and a uniformly sampled flow timestep τ ∈ [0, 1],
states of the vision-language and action respectively.                         the flow-matching training objective is
B. Training Recipe                                                                          Lf m = E ∥vρf low (zt , aτt , τ ) − (ϵ − at )∥
                                                                                                                                          
                                                                                                                                             (2)
   We present an efficient training recipe for learning hu-
                                                                               where ϵ is Gaussian noise and aτt = τ at +(1−τ )ϵ is the noised
manoid loco-manipulation skills from both human videos and
                                                                               action. We adapt the MM-DiT architecture [15] to implement
real robot data. The overall training procedure consists of three
                                                                               the action expert network vρf low , as illustrated in Fig. 3.
stages: first, pre-training the VLM backbone on the large-scale
                                                                               Specifically, the model uses the time-conditioning feature τ
high-quality and diverse human egocentric videos; second,
                                                                               to modulate the action (A) feature and the vision–language
post-training the flow-based action expert on cross-task real
                                                                               (VL) features separately. During each transformer block, the
humanoid data; and third, fine-tuning the action expert using
                                                                               action tokens and VL tokens perform joint global attention,
a small amount of in-domain task data, which enables rapid
                                                                               which facilitates more effective fusion of visual information
adaptation to new tasks.
                                                                               compared to the naive DiT.
   1) Pre-Training on Egocentric Human Video: Training a                          3) Fine-Tuning on In-domain Teleoperation Data: With the
humanoid foundation model faces a significant data scarcity                    pre-trained VLM and the post-trained action expert, our model
bottleneck. Human egocentric videos, which are much cheaper                    can be fine-tuned further end-to-end using a small amount of
to scale than real-world robotics data, offer a promising alter-               in-domain data and rapidly learn long-horizon, dexterous loco-
native. Therefore, we leverage EgoDex [20], which contains                     manipulation tasks. We evaluate the model on eight real-world
approximately 829 hours of human egocentric video capturing                    tasks (as illustrated in Fig. 6), each posing distinct challenges:
human hands performing diverse dexterous manipulation tasks.                   some require precise arm coordination, while others demand
To further mitigate the visual gap between human videos                        long-distance navigation. Most tasks exceed 2,000 steps at
and robotic observations, we incorporate Humanoid Everyday                     30Hz, rendering them truly long-horizon. Each task contains
[47], which contains 31 hours of humanoid data covering                        three to five sub-tasks, and each sub-task corresponds to a skill
260 diverse tasks, ranging from human–object interactions to                   such as grasping or pushing.
manipulations of deformable and articulated objects. We use a
shared action representation for both human hands and robot                    C. Real-Time Action Chunking
end-effectors. Specifically, the 48-DoF action in task space                      Humanoid robots require smooth and reactive control, par-
is defined as a ≜ {al , ar } and each al or ar ∈ R24 is                        ticularly when executing long-horizon, dexterous manipulation
{Twrist , Pthumb , Pindex , Pmiddle , Pring , Ppinky }. The T ∈                tasks. However, existing VLAs typically contain billions of
R9 is the 9-DoF wrist pose vector consisting of 3D position                    parameters, which inevitably introduce a “stop-and-think”
and 6D rotation. Each P ∈ R3 is a 3D fingertip position. Such                  behavior due to inference latency. Our Ψ0 model similarly
unified action representation enables joint training of human                  comprises over 2.5 billion parameters, with a single forward
and robot data and achieves stable training.                                   pass taking approximately 160 ms. To enable smooth pol-
   However, naively training the model to autoregressively                     icy rollout despite this latency, we adopt training-time real-
predict multiple high-dimensional action chunks is very com-                   time chunking (RTC) following [7]. With RTC, each action
putationally expensive and drastically slows down pre-training.                prediction is conditioned on the previously committed action
Our key insight is that the goal of pre-training the VLM                       chunk and outputs a consistent chunk of future actions, as
backbone is to learn the task semantics of the language instruc-               illustrated in Fig. 4. To faithfully simulate inference delay
tion and the visual representation for downstream real-robot                   during training, we randomly remove diffusion noise from
manipulations. Predicting a single next-step action suffices for               the first d = uniform(0, dmax ) tokens and mask them out
such a goal. Therefore, we train the VLM to predict only a                     in the loss computation in Eq. 2. Here, dmax ∈ [0, H − s)
single-step action at instead of at:t+H , which requires much                  denotes the maximum inference delay in timesteps, while H
less computation. We use FAST [34] to tokenize continuous                      and s correspond to the action chunk prediction horizon and
actions into discrete tokens. We train the FAST tokenizer on                   the execution horizon, respectively.
                                                 Robot Joint Angle over Time
                         1.0                                                                            eration framework that explicitly separates upper-body pose
                                                                         Next Action (w/o RTC)          tracking, dexterous manipulation, and locomotion commands,
                         0.8                                                                            while enabling single-operator whole-body control. As shown
 Joint Angle (degrees)




                                                                                                        in Fig. 5, the teleoperator’s upper-body pose is captured using
                         0.6                                             Previous Action                a PICO headset [35] and wrist trackers, and a multi-target
                                                                                                        inverse kinematics solver is implemented to compute the
                         0.4
                                                                                                        humanoid’s arm and torso configurations. Fine-grained finger
                                                                                                        motions are acquired using MANUS gloves [32], allowing
                         0.2
                                                                                                        direct control over all degrees of freedom of the dexterous
                                                                            Next Action (w/ RTC)
                                   Inference Start Switch Action Chunk                                  hands. Locomotion commands, including translational velocity
                         0.0
                               0         5          10           15          20            25      30   and turning orientation, are directly inferred from waist and
                                                              Timestep                                  foot trackers and provided as high-level commands to a RL
Fig. 4: Real-Time Chunking: Given that the previous action is being
executed (yellow line), the next action can diverge significantly (cyan                                 policy [25] responsible for stable lower-body control.
line) without RTC, which leads to control jitter. With RTC (red                                            By using a small set of wearable trackers and separating
line), the divergence between two consecutive actions is strongly                                       locomotion from in-place whole-body actions, our framework
suppressed, resulting in smoother and more stable behavior.                                             enables single-operator humanoid teleoperation with improved
                                                                                                        locomotion stability across diverse task scenarios. Further-
                                                         VR Headset                                     more, the combination of wrist trackers and MANUS gloves
                                                                                                        alleviates common occlusion and out-of-view issues in vision-
                                                                                                        based VR tracking, enabling accurate and reliable upper-body
                                                                                                        and hand tracking. Together, these design choices support
                                                     MANUS Gloves                                       robust and practical humanoid whole-body teleoperation for
                                                                                                        complex loco-manipulation tasks.
                                                         Waist Tracker
                                                                                                                              IV. E XPERIMENTS
                                                                                                        A. Implementation
                                                                                                           1) Hardware Platform: Throughout all real-world experi-
                                                         Foot Tracker
                                                                                                        ments, we employ the Unitree G1 humanoid platform, which
                                                                                                        provides 29 degrees of freedom for whole-body control. In
Fig. 5: Real-Robot Teleoperation Setup: We use MANUS gloves for                                         addition, each arm is equipped with a 7-DoF Dex3-1 dexterous
dexterous hand retargeting; a VR headset and wrist trackers capture                                     hand. Visual observations are obtained using the default head-
upper-body poses for inverse kinematics, while waist and foot trackers                                  mounted Intel RealSense D435i camera.
provide high-level locomotion commands.                                                                    2) Data Preparation: The EgoDex dataset contains approx-
                                                                                                        imately 900M frames and provides per-frame global trans-
                                                                                                        formation matrices for the upper humanoid body, including
D. Tailoring Teleoperation for Loco-Manipulation                                                        7 spine joints, 2 arms, and 21 joints for each hand. To
   Efficiently learning a long-horizon loco-manipulation task                                           improve pre-training efficiency, all actions are transformed
critically depends on the quality of in-domain data for fine-                                           into the current head-camera coordinate frame, and the frame
tuning. However, existing teleoperation systems are primarily                                           rate is upsampled by a factor of 3. Due to the presence
designed for locomotion and lack the stability and adaptability                                         of extreme outliers in EgoDex, action values are normalized
required for dexterous manipulation. Designing an effective                                             using the 1st and 99th quantiles. We omit state inputs dur-
teleoperation system for humanoid loco-manipulation requires                                            ing the pre-training stage. We use the Humanoid Everyday
balancing whole-body expressiveness, locomotion stability,                                              dataset [47] for task-agnostic post-training, which contains
and operational simplicity. Existing end-to-end whole-body                                              approximately 3 million frames of real-world teleoperated
teleoperation pipelines [43, 31] that directly map full-body                                            data. Actions are represented as 36-DoF joint-space vectors
human motion to humanoid control through reinforcement                                                  a = {qhand , qarm , torsorpy , hb , vx , vy , vyaw , pyaw }. Since
learning often suffer from limited robustness due to noisy                                              Humanoid Everyday only provides upper-body motion, we
tracking signals and unstable whole-body motion patterns.                                               similarly pad missing lower-body action components. States
Moreover, these systems rely on handheld controllers and                                                consist of 28-DoF joint positions of both hands and arms
reduce dexterous hand control to low-dimensional gripper-like                                           from the current frame and are fed into the model without
commands, limiting manipulation expressiveness. On the other                                            normalization.
hand, systems that decouple manipulation from locomotion                                                   3) Training Details: Training begins by fitting a FAST tok-
through explicit base commands [25] improve lower-body                                                  enizer using 500,000 randomly sampled actions from EgoDex.
stability, but typically require additional controllers or multiple                                     The resulting L1 reconstruction loss on held-out action data
operators and thus reduce practicality.                                                                 is approximately 0.005, improving upon the 0.01 using the
   To address these limitations, we propose a tailored teleop-                                          original open-source FAST tokenizer. The FAST tokenizer
Fig. 6: Real-World Task Setup: We evaluate Ψ0 on eight diverse long-horizon dexterous loco-manipulation tasks involving manipulation,
whole-body motion, and locomotion. The task instruction is overlayed on the task images and each sub-task is denoted with marker for
better visualization. Our policy rollout videos are included in the Supplementary Materials.


compresses each action sequence into 20 tokens which accel-             2) Evaluation Protocols: We collect 80 teleoperated trajec-
erates subsequent training. Then, we fine-tune Qwen3-VL-2B-          tories for each task. All baseline models are fine-tuned on the
Instruct [2] during the pre-training stage using 64 A100 GPUs        same dataset, using identical image observations as well as
for 10 days. Training is formulated as next-action prediction        the same action and state representations. Each long-horizon
only, and we avoid action chunking to reduce computational           task consists of three to five sub-tasks involving dexterous
overhead. The learning rate is fixed at 0.0001 and the global        manipulation, dual-arm coordination, and locomotion. As a
batch size is 1024. Next, we post-train the action expert,           result, policies may fail at early sub-tasks, which can lead
containing approximately 500M parameters, on the Humanoid            to complete rollout failure. To fully assess the capabilities
Everyday dataset. During this stage, the VLM backbone is             of each baseline, the evaluator is allowed to intervene and
frozen, the learning rate is fixed at 0.0001, and the global batch   assist the policy in progressing past failed sub-tasks so that
size is set to 2048. This stage takes approximately 30 hours on      execution can continue. We therefore report success rates for
a single node with 32 A100 GPUs. Finally, we fine-tune only          individual sub-tasks in addition to the overall task success rate.
the action expert for each downstream task for 40,000 steps,         For each task, we perform 10 rollout trials per model. A rollout
using a cosine learning rate scheduler with an initial learning      is considered successful only if all sub-tasks are completed.
rate of 0.0001.                                                      All baselines, including Ψ0 , are deployed using the same client
                                                                     code to control the robot.
B. Real-World Humanoid Experiments                                     3) Baselines: We conduct comprehensive real-world bench-
   1) Task Description: As shown in Fig. 6, we evaluate              marking against most recent open-source baselines. We invest
Ψ0 on eight real-world long-horizon manipulation tasks span-         huge effort to reproduce the best possible results for each.
ning diverse daily scenarios. The tasks range from simple                  a) π0.5: demonstrates strong generalization on mobile
interactions, such as pick-and-place, pushing, and wiping, to        robot platforms with dual arms and grippers. However, the
more challenging dexterous manipulations requiring precise           released model and checkpoint are limited to 30-dimensional
finger-object coordination, including turning a faucet and           action spaces. To adapt the model to humanoid tasks, we
pulling out a chip tray. Beyond upper-body manipulation, the         expand the action dimension to 36 and set the action chunk
tasks also involve whole-body motions, such as torso rotation        size to 16. The checkpoint weights of the corresponding linear
and squatting, as well as lower-body locomotion and turn-            layers are padded accordingly to accommodate the expanded
ing. Overall, this evaluation benchmarks model performance           action space. To account for the embodiment gap between the
on complex long-horizon dexterous loco-manipulation tasks            original training data and humanoids, we increase the learning
across multiple real-world environments.                             rate from 1e-5 to 1e-4 and the global batch size from 32 to 128
 100%
                                                                                       Ours
                                                                                       GR00T N1.6                            Grasping
                                                                                       𝜋0.5                                      100%
  80%                                                                                  InternVLA-M1
                                                                                                              Pulling                         Placing
                                                                                       EgoVLA                                    80%
                                                                                       H-RDT
                                                                                       Diffusion Policy                          60%
                                                                                       ACT
  60%                                                                                                                            40%

                                                                                                    Pushing                      20%                    Pouring

  40%



  20%                                                                                                 Carrying                                      Rotating


              00000     0000       0   000     00000      0000   0   0000     0   0      0000
   0%                                                                                                              Walking              Squatting
            Task 1    Task 2     Task 3      Task 4    Task 5    Task 6     Task 7    Task 8

Fig. 7: Real-World Benchmark: Evaluation results of policies across our eight tasks, showing task-wise success rates (%) (left) and
aggregated skill-level success rates (%) (right). The task descriptions are shown in Fig. 6. Detailed results for each task including all sub-task
progress are included in the Supplementary Materials.


for better performance, ensuring fair comparison. We fine-tune              training configuration reported in the original paper, training
the Pi05 DROID checkpoint, which we convert to a PyTorch                    for 115 epochs with an effective batch size of 16×8×4. In our
implementation.                                                             experiments, EgoVLA shows limited performance on lower-
     b) GR00T N1.6: shows strong performance in grasping                    body commands, likely because its pre-training primarily
and loco-manipulation, with robust spatial generalization. We               captures upper-body and hand manipulation skills and does
use all the default hyperparameters for fine-tuning in the                  not provide strong priors for coordinated lower-body motion.
release code. We initialize the model from the GR00T N1.6                         f) Diffusion Policy (DP) [13]: For visual feature extrac-
3B pre-trained checkpoint and fine-tune it on our teleoperated              tion, we employ a pre-trained ResNet-18 [19] as the visual
data for 20,000 steps with a global batch size of 24 on                     encoder. We set the learning rate to 1 × 10−4 and the global
three NVIDIA A100 GPUs. We use cosine scheduling for the                    batch size to 32. Training is conducted for 40,000 steps using
learning rate at 1e-4. As the RTC inference code for GR00T                  two A100 GPUs, with each task trained for approximately 15
N1.6 is not publicly available in the official repository, we               hours. We observe that DP fails on most tasks, even though
adopt a standard sequential inference scheme, in which the                  it can reasonably fit the training data. We conjecture that the
observation corresponding to the most recently executed action              UNet-based DP model has insufficient visual capacity. During
is used to condition the prediction of subsequent actions.                  inference, we perform 100 iterative denoising steps to progres-
     c) InternVLA-M1 [11]: is a unified framework for spatial               sively transform random noise into actionable trajectories.
grounding and robot control, which demonstrates strong spatial                    g) Action Chunking with Transformers (ACT) [46]: To
reasoning capabilities. However, it is only pre-trained on                  adapt to the humanoid locomotion and manipulation tasks, we
spatial reasoning and robotic arm data which limits its perfor-             reconfigure the action head to output 36-dimensional actions
mance on humanoid tasks. We start with the checkpoint pre-                  and tune the chunk size to 100, and initialize the transformer
trained on the RT-1 Bridge dataset, freeze the VLM backbone                 block with a configuration of 4 encoder layers and 1 decoder
and fine-tune the action head for 30,000 steps with a batch size            layer, aligning with the publicly released ACT framework [9].
of 64 on a single NVIDIA A100 GPU. In our experiments,                      Other training hyper-parameters like learning rate, batch size
InternVLA-M1 exhibits action jitter across consecutive action               and training steps are kept the same as DP.
chunks, resulting in unstable executions.                                      4) Comparisons to Baselines: As illustrated in Fig. 7,
     d) H-RDT: is a single large DiT action expert with 2B                  our model outperforms all baselines by a large margin. Our
parameters. We train the model for 10,000 training steps with               model exhibits the most stable performance across all eight
a batch size of 32 on a single NVIDIA A100 GPU. The                         long-horizon dexterous loco-manipulation tasks. Notably, it
resulting policy excels at tasks that do not require precise                achieves an average overall success rate that is at least 40%
movements. However, it struggles with manipulation tasks that               higher than that of the second-best baseline, GR00T-N1.6
require high-precision across many joints.                                  [4], which is the most recently released humanoid foundation
     e) EgoVLA: is a vision–language–action model pre-                      model. These results highlight the effectiveness of our training
trained on egocentric human manipulation videos using                       paradigm, despite using a relatively small amount of robotic
EgoDex and additional data sources. Since the original code-                data in both the pre-training and post-training stages. We
base predicts only end-effector wrist and hand poses, we                    attribute this success to the unique training recipe. A key
adapt the action decoder to output robot joint-space commands               insight is that pre-training the VLM on large-scale human
required by downstream tasks. We fine-tune the pre-trained                  video enables it to learn domain-aligned visual representa-
EgoVLA on our teleoperated downstream tasks following the                   tions for downstream manipulation tasks, while avoiding the
        Pre-Training   Post-Training   Real-Time    MM-DiT        Naive DiT     Right-Arm      Left-Arm      Dual-Arm     Overall
       EgoDex     HE     (On HE)       Chunking    Action Head   Action Head   Pick-n-Place   Pick-n-Place    Carry     Success Rate
         ✗        ✗         ✗             ✗            ✗               ✓          1/10           1/10         1/10          0/10
         ✗        ✗         ✗             ✗            ✓               ✗          9/10           2/10         3/10          2/10
         ✓        ✗         ✗             ✗            ✓               ✗          8/10           6/10          6/10         6/10
         ✓        ✓         ✗             ✗            ✓               ✗          8/10           8/10          9/10         8/10
         ✓        ✓         ✓             ✗            ✓               ✗          9/10           9/10         10/10         9/10
         ✓        ✓         ✓             ✓            ✓               ✗          9/10           9/10          9/10         9/10

TABLE I: Ablation Studies. We study the effects of pre-training, post-training, and real-time chunking on a dual-arm long-horizon task
which consists of three steps: right-arm pick and place, left-arm pick-and-place and dual-arm lift.


hazardous and difficult co-training of two fundamentally dif-          features from the VLM backbone with Action (A) branch
ferent distributions. With language and visual representations         representations. Our analysis suggests that naive DiT, origi-
extracted from the pre-trained VLM, we further post-train only         nally designed for text-conditioned image generation, provides
the action expert in the joint space using high-quality real-          weaker conditioning when applied to VL-guided action pre-
robot data, enabling it to learn a strong prior for embodied           diction. Additional ablation studies on the action expert are
control. More detailed results, including per-subtask progress         provided in the Supplementary Material.
and policy rollout videos, are provided in the Supplemental                  c) Real-Time Chunking Behaviors: VLAs typically suf-
Material.                                                              fer from slow inference due to their large model size. When
                                                                       receiving a new query to generate actions, inference can take
C. Ablation Studies
                                                                       more than 200 ms, during which the humanoid robot must
    Due to limited compute and time, we perform our ablation           pause while waiting for the actions to become available,
study using a single real-world task: pick toys into a box and         introducing jitter and unstable behavior in whole-body control
lift it. This task consists of three sub-tasks: (1) picking up a toy   tasks. One solution is test-time real-time chunking [6]. It
dumpling with the right arm and placing it into the box; (2)           employs inference-time gradient guidance to the flow-based
picking up a toy hippopotamus with the left arm and placing it         action generation to steer the future actions to be consistent
into the box; and (3) carrying the box with both arms. This task       with past ones, therefore achieving smooth execution of the
consists of multiple execution stages and requires the policy to       joint commands. However, we found that our model can not
handle single-arm pick-and-place and dual-arm coordination.            be guided at test time stably; as a result, we implemented
       a) The Role of Pre-Training and Post-Training: First, we        training-time real-time chunking [7]. We observed that real-
study how the original Qwen3-VL VLM pre-trained on text-               time chunking mitigates physical collisions during policy
generation tasks performs in our settings. As shown in Table I,        execution and increases policy rollout throughput without
freezing the pre-trained Qwen3-VL backbone and fine-tuning             performance degradation.
only the action head yields the poorest performance, achieving
an overall success rate of only 0.2. This result highlights                                    V. C ONCLUSION
the importance of pre-training the VLM backbone on human
data to learn how to generate action tokens. After pre-training           We introduce Ψ0 , an open foundation model accompanied
on EgoDex for task-space next-action prediction, the model             by a complete open-source suite for teleoperation, learning in-
achieves a substantial performance improvement. Notably,               frastructure, and deployment. Through extensive experiments,
even though the VLM backbone is trained to predict a dif-              our results suggest that scaling humanoid learning requires
ferent action representation than that used by the downstream          scaling the right data in the right way. In contrast to blindly
action head, supervising it with next-step 48-DoF actions still        increasing the volume of teleoperation data at substantial
enables the model to learn meaningful visual representations           cost, we leverage affordable, high-quality egocentric videos
for robotic tasks. These findings suggest an effective pathway         to learn human motion priors and human-object interaction
for learning from large-scale human video data while avoiding          knowledge. Our work further introduces several novel and
the inference latency associated with fully autoregressive VLM         empirically validated techniques that significantly improve the
action generation. With post-training of the action expert             effectiveness of humanoid VLAs, including efficient whole-
on high-quality robot data, overall performance is further             body dexterous teleoperation, MM-DiT-based action experts,
improved.                                                              and real-time control at deployment. Together, our training
       b) MM-DiT versus Naive DiT: We also ablate the effec-           recipe and model architecture achieve state-of-the-art perfor-
tiveness of the proposed MM-DiT action head by comparing               mance on challenging, complex, long-horizon tasks, while
it with a naive DiT for action prediction. The results show            relying on substantially less real-world robotic data. We hope
that MM-DiT consistently outperforms the DiT variant. This             this work can serve as a foundation for humanoid learning, ac-
improvement can be attributed to MM-DiT’s dual-modulation              celerating the development of humanoids capable of assisting
design and its joint attention mechanism, which integrates VL          with everyday tasks.
  Limitation. Due to compute and time constraints, we are              Hsu, et al. Rt-1: Robotics transformer for real-world
unable to further scale training to larger collections of human        control at scale. arXiv preprint arXiv:2212.06817, 2022.
videos and real-world robotic data, which we leave for future      [9] Remi Cadene, Simon Alibert, Alexander Soare, Quentin
work. Another limitation stems from the hardware platform,             Gallouedec, Adil Zouitine, Steven Palma, Pepijn
whose payload capacity constrains the execution of potentially         Kooijmans, Michel Aractingi, Mustafa Shukor, Dana
more capable manipulation behaviors.                                   Aubakirova, Martino Russi, Francesco Capuano, Caro-
                                                                       line Pascal, Jade Choghari, Jess Moss, and Thomas Wolf.
                        R EFERENCES                                    Lerobot: State-of-the-art machine learning for real-world
 [1] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David                 robotics in pytorch.        https://github.com/huggingface/
     McAllister, Anthony Zhang, Chung Min Kim, Trevor                  lerobot, 2024.
     Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo           [10] Xiongyi Cai, Ri-Zhao Qiu, Geng Chen, Lai Wei, Isabella
     Kanazawa. Visual imitation enables contextual humanoid            Liu, Tianshu Huang, Xuxin Cheng, and Xiaolong Wang.
     control. In Proceedings of The Conference on Robot                In-n-on: Scaling egocentric manipulation with in-the-
     Learning, Proceedings of Machine Learning Research,               wild and on-task data. arXiv preprint arXiv:2511.15704,
     2025.                                                             2025.
 [2] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen,              [11] Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya
     Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding,              Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang,
     Chang Gao, Chunjiang Ge, Wenbin Ge, Zhifang Guo,                  Yu Qiao, Yang Tian, Bin Wang, Bolun Wang, Fangjing
     Qidong Huang, Jie Huang, Fei Huang, Binyuan Hui, Shu-             Wang, Hanqing Wang, Tai Wang, Ziqin Wang, Xueyuan
     tong Jiang, Zhaohai Li, Mingsheng Li, Mei Li, Kaixin              Wei, Chao Wu, Shuai Yang, Jinhui Ye, Junqiu Yu, Jia
     Li, Zicheng Lin, Junyang Lin, Xuejing Liu, Jiawei Liu,            Zeng, Jingjing Zhang, Jinyu Zhang, Shi Zhang, Feng
     Chenglong Liu, Yang Liu, Dayiheng Liu, Shixuan Liu,               Zheng, Bowen Zhou, and Yangkun Zhu. Internvla-m1:
     Dunjie Lu, Ruilin Luo, Chenxu Lv, Rui Men, Lingchen               A spatially guided vision-language-action framework for
     Meng, Xuancheng Ren, Xingzhang Ren, Sibo Song,                    generalist robot policy, 2025. URL https://arxiv.org/abs/
     Yuchong Sun, Jun Tang, Jianhong Tu, Jianqiang Wan,                2510.13778.
     Peng Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang,           [12] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang,
     Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu, Zhibo                 Ge Yang, and Xiaolong Wang. Expressive whole-
     Yang, Mingkun Yang, Jianxin Yang, An Yang, Bowen                  body control for humanoid robots. arXiv preprint
     Yu, Fei Zhang, Hang Zhang, Xi Zhang, Bo Zheng,                    arXiv:2402.16796, 2024.
     Humen Zhong, Jingren Zhou, Fan Zhou, Jing Zhou,              [13] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau,
     Yuanzhi Zhu, and Ke Zhu. Qwen3-vl technical report.               Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran
     arXiv preprint arXiv:2511.21631, 2025.                            Song. Diffusion policy: Visuomotor policy learning via
 [3] Hongzhe Bi, Lingxuan Wu, Tianwei Lin, Hengkai Tan,                action diffusion, 2024. URL https://arxiv.org/abs/2303.
     Zhizhong Su, Hang Su, and Jun Zhu. H-rdt: Human                   04137.
     manipulation enhanced bimanual robotic manipulation.         [14] Pengxiang Ding, Jianfei Ma, Xinyang Tong, Binghong
     arXiv preprint arXiv:2507.23523, 2025.                            Zou, Xinxin Luo, Yiguo Fan, Ting Wang, Hongchao Lu,
 [4] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev,             Panzhong Mo, Jinxin Liu, et al. Humanoid-vla: Towards
     Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox,            universal humanoid control with visual integration. arXiv
     Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open              preprint arXiv:2502.14795, 2025.
     foundation model for generalist humanoid robots. arXiv       [15] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim
     preprint arXiv:2503.14734, 2025.                                  Entezari, Jonas Müller, Harry Saini, Yam Levi, Dominik
 [5] Kevin Black, Noah Brown, Danny Driess, Adnan Es-                  Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling
     mail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy            rectified flow transformers for high-resolution image syn-
     Groom, Karol Hausman, Brian Ichter, et al. π0 : A vision-         thesis. In Forty-first international conference on machine
     language-action flow model for general robot control.             learning, 2024.
     arXiv preprint arXiv:2410.24164, 2024.                       [16] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wet-
 [6] Kevin Black, Manuel Y Galliker, and Sergey Levine.                zstein, and Chelsea Finn. Humanplus: Humanoid shad-
     Real-time execution of action chunking flow policies.             owing and imitation from humans. arXiv preprint
     arXiv preprint arXiv:2506.07339, 2025.                            arXiv:2406.10454, 2024.
 [7] Kevin Black, Allen Z Ren, Michael Equi, and Sergey           [17] Haoran Geng, Songlin Wei, Congyue Deng, Bokui Shen,
     Levine. Training-time action conditioning for efficient           He Wang, and Leonidas Guibas. Sage: Bridging semantic
     real-time chunking. arXiv preprint arXiv:2512.05964,              and actionable parts for generalizable articulated-object
     2025.                                                             manipulation under language instructions. arXiv preprint
 [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yev-                arXiv:2312.01307, 2, 2023.
     gen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana          [18] Kristen Grauman, Andrew Westbury, Lorenzo Torresani,
     Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine               Kris Kitani, Jitendra Malik, Triantafyllos Afouras, Kumar
     Ashutosh, Vijay Baiyya, Siddhant Bansal, Bikram Boote,          Ye Wang, Haoqi Yuan, Jiazheng Liu, Chaoyi Xu, Qin Jin,
     et al. Ego-exo4d: Understanding skilled human activity          and Zongqing Lu. Being-h0: vision-language-action pre-
     from first-and third-person perspectives. In Proceedings        training from large-scale human videos. arXiv preprint
     of the IEEE/CVF Conference on Computer Vision and               arXiv:2507.15597, 2025.
     Pattern Recognition, pages 19383–19400, 2024.              [31] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li,
[19] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian               Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng
     Sun. Deep residual learning for image recognition. In           Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing
     2016 IEEE Conference on Computer Vision and Pattern             motion tracking for natural humanoid whole-body con-
     Recognition (CVPR), pages 770–778, 2016. doi: 10.1109/          trol. arXiv preprint arXiv:2511.07820, 2025.
     CVPR.2016.90.                                              [32] MANUS Technology Group. MANUS – High-Precision
[20] Ryan Hoque, Peide Huang, David J. Yoon, Mouli Siva-             Data Gloves for Robotics, VR & Mocap. https://www.
     purapu, and Jian Zhang. Egodex: Learning dexterous              manus-meta.com/, 2024.
     manipulation from large-scale egocentric video, 2025.      [33] Jiageng Mao, Siheng Zhao, Siqi Song, Chuye Hong,
     URL https://arxiv.org/abs/2505.11709.                           Tianheng Shi, Junjie Ye, Mingtong Zhang, Haoran Geng,
[21] Physical Intelligence, Kevin Black, Noah Brown, James           Jitendra Malik, Vitor Guizilini, et al. Universal humanoid
     Darpinian, Karan Dhabalia, Danny Driess, Adnan Es-              robot pose learning from internet human videos. In 2025
     mail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al.         IEEE-RAS 24th International Conference on Humanoid
     π0.5 : A vision-language-action model with open-world           Robots (Humanoids), pages 1–8. IEEE, 2025.
     generalization. arXiv preprint arXiv:2504.16054, 2025.     [34] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny
[22] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi,          Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea
     Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang,             Finn, and Sergey Levine. Fast: Efficient action tokeniza-
     Zhihui Peng, et al. Wholebodyvla: Towards unified latent        tion for vision-language-action models. arXiv preprint
     vla for whole-body loco-manipulation control. arXiv             arXiv:2501.09747, 2025.
     preprint arXiv:2512.11047, 2025.                           [35] PICO Immersive Pte. Ltd. PICO 4 Ultra: An All-
[23] Simar Kareer, Dhruv Patel, Ryan Punamiya, Pranay                New Mixed Reality Experience. https://www.picoxr.com/
     Mathur, Shuo Cheng, Chen Wang, Judy Hoffman, and                global/products/pico4-ultra, 2023.
     Danfei Xu. Egomimic: Scaling imitation learning via        [36] Haozhi Qi, Yen-Jen Wang, Toru Lin, Yi Brent,
     egocentric video, 2024. URL https://arxiv.org/abs/2410.         Yi Ma, Koushil Sreenath, and Jitendra Malik. Co-
     24221.                                                          ordinated humanoid manipulation with choice policies.
[24] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted            arXiv:2512.25072, 2025.
     Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov,     [37] Yiyang Shao, Xiaoyu Huang, Bike Zhang, Qiayuan Liao,
     Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla:        Yuman Gao, Yufeng Chi, Zhongyu Li, Sophia Shao,
     An open-source vision-language-action model. arXiv              and Koushil Sreenath. Langwbc: Language-directed
     preprint arXiv:2406.09246, 2024.                                humanoid whole-body control via end-to-end learning.
[25] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang,             arXiv preprint arXiv:2504.21738, 2025.
     Rizhao Qiu, and Xiaolong Wang. Amo: Adaptive motion        [38] Gemini Robotics Team, Abbas Abdolmaleki, Saminda
     optimization for hyper-dexterous humanoid whole-body            Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac,
     control. Robotics: Science and Systems 2025, 2025.              Montserrat Gonzalez Arenas, Ashwin Balakrishna,
[26] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei             Nathan Batchelor, Alex Bewley, Jeff Bingham, et al.
     Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop          Gemini robotics 1.5: Pushing the frontier of generalist
     whole-body humanoid teleoperation for long-horizon              robots with advanced embodied reasoning, thinking, and
     tasks, 2025.                                                    motion transfer. arXiv preprint arXiv:2510.03342, 2025.
[27] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yu-           [39] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao,
     man Gao, Guy Tevet, Koushil Sreenath, and C Karen               Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng,
     Liu. Beyondmimic: From motion tracking to versatile             Guanya Shi, Trevor Darrell, Koushil Sreenath, et al. Le-
     humanoid control via guided diffusion. arXiv preprint           verb: Humanoid whole-body control with latent vision-
     arXiv:2508.08241, 2025.                                         language instruction. arXiv preprint arXiv:2506.13751,
[28] Minghuan Liu, Zixuan Chen, Xuxin Cheng, Yandong Ji,             2025.
     Ri-Zhao Qiu, Ruihan Yang, and Xiaolong Wang. Visual        [40] Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui
     whole-body control for legged loco-manipulation. arXiv          Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin
     preprint arXiv:2403.16967, 2024.                                Cheng, Ri-Zhao Qiu, et al. Egovla: Learning vision-
[29] Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho              language-action models from egocentric human videos.
     Lee, Maximilian Du, and Chelsea Finn. Bidirectional             arXiv preprint arXiv:2507.12440, 2025.
     decoding: Improving action chunking via closed-loop        [41] Justin Yu, Yide Shentu, Di Wu, Pieter Abbeel, Ken
     resampling. arXiv preprint arXiv:2408.17355, 2024.              Goldberg, and Philipp Wu. Egomi: Learning active vision
[30] Hao Luo, Yicheng Feng, Wanpeng Zhang, Sipeng Zheng,             and whole-body manipulation from egocentric human
     demonstrations, 2025. URL https://arxiv.org/abs/2511.
     00153.
[42] Yanjie Ze, Zixuan Chen, João Pedro Araújo, Zi ang
     Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu.
     Twist: Teleoperated whole-body imitation system. arXiv
     preprint arXiv:2505.02833, 2025.
[43] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo
     Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi,
     Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable,
     and holistic humanoid data collection system. arXiv
     preprint arXiv:2511.02832, 2025.
[44] Jiazhao Zhang, Kunyu Wang, Shaoan Wang, Minghan Li,
     Haoran Liu, Songlin Wei, Zhongyuan Wang, Zhizheng
     Zhang, and He Wang. Uni-navid: A video-based vision-
     language-action model for unifying embodied navigation
     tasks. arXiv preprint arXiv:2412.06224, 2024.
[45] Siheng Zhao, Yanjie Ze, Yue Wang, C. Karen Liu, Pieter
     Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From
     general motion tracking to humanoid whole-body loco-
     manipulation via residual learning, 2025. URL https:
     //arxiv.org/abs/2510.05070.
[46] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea
     Finn. Learning fine-grained bimanual manipulation with
     low-cost hardware. arXiv preprint arXiv:2304.13705,
     2023.
[47] Zhenyu Zhao, Hongyi Jing, Xiawei Liu, Jiageng Mao,
     Abha Jha, Hanwen Yang, Rong Xue, Sergey Zakharor,
     Vitor Guizilini, and Yue Wang. Humanoid everyday: A
     comprehensive robotic dataset for open-world humanoid
     manipulation. arXiv preprint arXiv:2510.08807, 2025.
[48] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu,
     Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan
     Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-
     action models transfer web knowledge to robotic control.
     In Conference on Robot Learning, pages 2165–2183.
     PMLR, 2023.
                        C ONTENTS                               X      More Ablation Studies                            16
                                                                       X-A    Effect of RTC . . . . . . . . . . . . . . 16
I     Introduction                                         2           X-B    Pre-Training on only 10% EgoDex . . . 16
                                                                       X-C    Pre-Training on only Humanoid Everyday 16
II    Related Works                                        2           X-D    Multi-Task Fine-Tuning . . . . . . . . . 17
      II-A    Whole-Body Dexterous Manipulation .          2
                                                                                VI. M ORE T RAINING D ETAILS
      II-B    Humanoid VLAs . . . . . . . . . . . .        3
      II-C    Learning From Egocentric Videos . . .        3    A. Pre-Training
                                                                   FAST Tokenization: We use the data processing script from
III   The Ψ0 Foundation Model                              3    H-RDT [3] to obtain a 48-DoF task-space action represen-
      III-A  Model Architecture . . . . . . . . . . .      3    tation, along with the corresponding dataset statistics. The
      III-B  Training Recipe . . . . . . . . . . . . .     4    action data is down-sampled from the original 30 Hz to 10 Hz.
             III-B1    Pre-Training on Egocentric               We find that the original open-sourced FAST tokenizer [34]
                       Human Video . . . . . . . .          4   exhibits a large reconstruction loss (0.583×10−4 ), particularly
             III-B2    Post-Training on Cross-Task              under noisy token settings. To address this issue, we trained
                       Real Humanoid Data . . . .           4   the FAST tokenizer from scratch using 500,000 randomly
                                                                sampled actions, leading to longer token lengths. Actions are
             III-B3    Fine-Tuning on In-domain
                                                                normalized using the 1st and 99th quantiles of the dataset. The
                       Teleoperation Data . . . . . .      4
                                                                action horizon, vocabulary size, and scale are set to 1, 2048,
      III-C  Real-Time Action Chunking . . . . . .         4
                                                                and 100, respectively. A comparison of action reconstruction
      III-D  Tailoring Teleoperation for Loco-                  performance before and after fitting is shown in Table II.
             Manipulation . . . . . . . . . . . . . . .     5
                                                                                Reconstruction L1 Loss   Avg Token Length
IV    Experiments                                          5
                                                                 Before              5.83 × 1e−4               2.08
      IV-A   Implementation . . . . . . . . . . . . .      5     After               1.95 × 1e−4               13.04
             IV-A1     Hardware Platform . . . . .         5
             IV-A2     Data Preparation . . . . . . .      5    TABLE II: Fast Tokenizer. Comparison of reconstruction loss and
                                                                average token length before and after training. Boldface indicates the
             IV-A3     Training Details . . . . . . .      5    best performance.
      IV-B   Real-World Humanoid Experiments . .           6
             IV-B1     Task Description . . . . . . .      6       Hyper-Parameters: We train the full VLM backbone using
             IV-B2     Evaluation Protocols . . . . .      6    DeepSpeed, following the original Qwen3-VL training setup
             IV-B3     Baselines . . . . . . . . . . .     6    [2]. The learning rates for the language backbone, MM projec-
             IV-B4     Comparisons to Baselines . .        7    tor, and vision tower are set to 1×10−4 , 1×10−5 , and 1×10−5 ,
      IV-C   Ablation Studies . . . . . . . . . . . . .    8    respectively, and are kept constant throughout pre-training.
                                                                We observe that the default learning rate of 1 × 10−6 is too
V     Conclusion                                            8   small for effective convergence. The default image resolution
                                                                in EgoDex is 1920 × 1080, which is prohibitively memory-
VI    More Training Details                                12   intensive; therefore, we resize images to 360 × 240. We pre-
      VI-A   Pre-Training . . . . . . . . . . . . . . .    12   train the Qwen3-VL-2B-Instruct variant using 64 A100 GPUs
      VI-B   Post-Training . . . . . . . . . . . . . . .   12   with a global batch size of 1024. Training takes approximately
      VI-C   Fine-Tuning . . . . . . . . . . . . . . .     13   10 days to reach 230k steps, where the first 200k steps are
                                                                trained exclusively on the EgoDex dataset and the remaining
VII   Real-Time Chunking                                   13   30k steps are trained solely on the Humanoid Everyday dataset
      VII-A Training-Time RTC . . . . . . . . . . .        13   [47].
      VII-B System Implementation . . . . . . . . .        13   B. Post-Training
                                                                   Data Processing: We post-train the action expert in joint
VIII Whole-Body Teleoperation Pipeline                     13   space using the Humanoid Everyday (HE) dataset [47]. Since
     VIII-A Whole-Body Control . . . . . . . . . .         13   HE contains two different embodiments—G1 with Dex3-1
     VIII-B Dexterous Manipulation . . . . . . . . .       14   and H1 with the Inspire Hand—which have different finger
     VIII-C Locomotion . . . . . . . . . . . . . . .       14   joint morphologies and degrees of freedom, we align the
                                                                action representations by reordering the default joint indices.
IX    Real-World Experiment Details                        14   The resulting action representation has 28 DoF, consisting of
      IX-A   Task Descriptions . . . . . . . . . . . .     14   14 DoF for the hand and 14 DoF for the arm. The state
      IX-B   Detail Evaluation Metrics . . . . . . . .     16   representation is processed in a similar manner. To enable
      IX-C   Deployment . . . . . . . . . . . . . . .      16   future fine-tuning of the action expert without reinitializing the
state and action projectors, we pad the action and state vectors      these approaches, real-time chunking with training-time [7] or
to 36 DoF and 32 DoF, respectively. The padded dimensions             test-time [6] action inpainting method demonstrates the best
correspond to lower-body control signals that are not present         performance.
in the HE dataset.                                                       In practice, we found that our model cannot be guided
   Hyper-Parameters: During post-training, the VLM back-              stably at test time [6]; as a result, we implemented training-
bone is frozen, and only the action expert is optimized using         time real-time chunking [7]. Unlike test-time RTC, which only
a constant learning rate of 1 × 10−4 . The global batch size is       requires correcting the velocity v (in flow matching) or noise
set to 2048, and training is conducted for 30k steps. Training        ϵ (in diffusion models) predicted by the action head during
took approximately 30 hours on 32 A100 GPUs. Input images             inference, training-time RTC necessitates modifying the model
are down-scaled to 320 × 240. We adopt uniform sampling for           during the training phase. Specifically, we randomly mask
the diffusion time steps τ ∈ [0, 1] and observe no performance        the first d ∈ [1, dmax ] action tokens, where dmax is set to
difference compared to alternative sampling strategies [21, 4]        6 in our experiments. The masked action tokens are excluded
in our real-world experiments.                                        from loss computation, as illustrated in Fig. 8. The model is
                                                                      trained to predict actions conditioned on the preceding clean
        Clean Tokens                  Noisy Tokens
                                                                      action tokens, so that it can generate the remaining tokens with
                                                                      smooth continuity to the clean action tokens. During inference,
 ...    1.0         1.0                                        ...    action steps that have not yet been executed are treated as clean
                                                                      tokens and are used to generate the next action chunk.
          No Loss                 Flow Mathcing Loss
                                                                      B. System Implementation
Fig. 8: Training-Time RTC. Diffusion timesteps and loss calculation
in training.                                                             We demonstrate our real-time action chunking system de-
                                                                      sign in Fig. 9. The system consists of two components: a
C. Fine-Tuning                                                        client for obtaining observations and executing actions, and a
                                                                      server for control and model inference. The overall operating
   For real-world tasks, we fine-tune only the action expert          frequency is determined by the Control Loop on the server
while keeping the VLM backbone frozen. Each real-world task           side, running at 30Hz. At each timestep in the Control Loop,
consists of 80 episodes of teleoperation data. We set the global      the observation is updated, an action is queried and sent to the
batch size to 128 and train for 40k steps per task. A cosine          client for execution, which then generates a new observation.
learning rate scheduler is used, with the initial learning rate          To ensure uninterrupted action execution, model inference
set to 1 × 10−4 . The state and action are normalized using           runs asynchronously with action execution, controlled by the
their respective minimum and maximum values. The image                Inference Loop. The Inference Loop shares the action chunk,
resolution and diffusion timestep sampling follow the same            observation, and timestep counter with the Control Loop.
settings as in post-training. Support for real-time chunking is       When the current action chunk has been executed beyond a
described in Section VII-A.                                           certain threshold (t ≥ smin ), the inference loop is triggered to
                    VII. R EAL -T IME C HUNKING                       obtain the next action chunk. The system switches to the new
                                                                      action chunk before the previous one completes, ensuring that
A. Training-Time RTC
                                                                      no system interruption occurs between action chunks due to
   In addition to training, Ψ0 enables real-time control at           inference latency.
deployment time. Modern VLAs usually have billions of
parameters [24, 38, 6], leading to substantial inference latency
                                                                           VIII. W HOLE -B ODY T ELEOPERATION P IPELINE
with naive synchronous inference strategies. Specifically, with
the naive ”stop-think-execute” strategy, rollouts exhibit visible     A. Whole-Body Control
pauses and even jitters between consecutive action chunks.
Introducing pauses between chunks not only slows down                    As shown in Fig. 10, using the PICO4U [35] headset
the rollout process but also creates a training-evaluation gap,       together with two wrist trackers, we treat the head and wrist
which will cause a higher failure rate [6].                           poses as three end-effectors and solve a multi-target inverse
   A straightforward approach to address this issue is naive          kinematics (IK) problem. This directly produces the humanoid
action chunking, which starts the next inference before the           arm joint positions qarm , as well as intermediate variables
previous action chunk is fully executed and switches to the           including torso orientation torsorpy and pelvis height hb , which
new chunk once it becomes available. While this strategy              modulate the robot’s upper-body posture. These intermediate
mitigates the inference delay problem, it introduces jittery tran-    variables are further provided to a low-level locomotion RL
sitions between chunks due to randomness and discontinuity,           policy (AMO) [25], which outputs the lower-body joint states
which can be even more detrimental to rollout performance.            qlower .
To address this limitation, recent work has explored methods             This hierarchical design enables coordinated whole-body
to maintain continuity between chunks [46, 29, 6, 7]. Among           control while maintaining balance and locomotion stability.
              CLIENT                      NETWORK
                                                                                                  SERVER
              Send Obs        Obs                 Obs          Receive Obs                                                      Shared
            (30Hz Active)                                       (Passive)                                                     latest_obs




                                                                                                   Real-Time Chunking Controller & Inference
                                                                                       a. Control Loop (30Hz Active)
                                                                                                                                                   Shared States (Mutex 𝓜)
           Action Execution    Strict Synchronization Loop                                                                                           t (timestep counter)
                                                                                                           t=t+1                                      (current action chunk)
                                      Real-time 30Hz                                     Return
            (~60Hz Active)                                                                                    =               Acquire 𝓜                 (current observation)
                                                                                                           notify C


                                                                                       b. Inference Loop
                                                                 Shared
                Shared                                                                                                    Set s = t                           Release 𝓜
                                                              latest_action           Wait on C
             latest_action                                                                             Acquire 𝓜          Update       , Get o =              (crucial for
                                                                                      Until t ≥
                                                                                                                          Estimate d = max (Q)               non-blocking)


                                                 Action                                                               INPAINTING-INFERENCE(𝛑, o,            , d)
            Receive Action    Action                          Send Action
              (Passive)                                      (30Hz Active)
                                                                                                                           Update        =
                                                                                       Release 𝓜                           Reset t = t - s                     Acquire 𝓜
                                                                                                                           Enqueue t onto Q




Fig. 9: Real-Time Action Chunking System Design. The system consists of a client (observation collection and action execution) and a
server (control and inference). The Control Loop (30Hz) coordinates observation updates and action dispatch, while the Inference Loop runs
asynchronously to compute the next action chunk when t ≥ smin , enabling seamless chunk transitions without inference-induced interruptions.

                                       Control Loop Thread
                                          (30Hz Active)
B. Dexterous Manipulation
   We use MANUS gloves [32] to obtain accurate finger track-
ing from the teleoperator. The thumb, index finger, and middle
finger motions are retargeted to the three-finger dexterous
hands of the G1 humanoid to enable dexterous manipulation.
By combining MANUS gloves with PICO wrist trackers,
we directly obtain reliable hand and wrist end-effector poses
without relying on unstable vision-based VR hand tracking.
This design avoids common occlusion and out-of-view issues
and provides more precise hand pose estimation for whole-
body dexterous manipulation.
                                                                              Fig. 10: Single Operator Teleoperation Framework. Our frame-
                                                                              work maps human upper-body motions to robot arm and hand
C. Locomotion                                                                 control via retargeting and multi-target IK, while lower-body pose
                                                                              is generated through an RL-based policy.
   Unlike prior approaches such as TWIST2 [43] and
SONIC [31], we do not directly retarget the whole-body
SMPL motion provided by the PICO tracking system to the
                                                                                       IX. R EAL -W ORLD E XPERIMENT D ETAILS
humanoid. We find that end-to-end whole-body tracking and
retargeting is often not robust, frequently leading to foot                   A. Task Descriptions
drifting, unstable lower body motion, and excessive small                        We evaluate Ψ0 on eight real-world long-horizon manipula-
corrective steps that hinder policy learning. Instead, we control             tion tasks spanning diverse daily scenarios. The policy rollouts
locomotion through high-level commands (vx , vy , vyaw , pyaw ).              for all tasks are included in the supplementary video.
The PICO waist tracker estimates the operator’s translational                    Task 1. Remove the lid, turn on the faucet, and fill with
velocity (vx , vy ), which is mapped to the robot’s base transla-             water: The robot grasps the spray bottle with its right hand,
tion. In addition, the foot trackers provide signals to compute               and removes the lid from the bottle with left hand and places
yaw commands (vyaw , pyaw ) for regulating the humanoid’s base                it on the table. The robot then moves the bottle under the
orientation. We also apply clipping and filtering to suppress                 faucet. With the index finger of its left hand, the robot turns
noise caused by natural human body sway, ensuring accurate                    the faucet clockwise to start the water flow and fills the bottle
locomotion command estimation.                                                with water. Finally, the robot places the filled bottle back on
                                                                              the table.
  Overall, our teleoperation pipeline enables a single operator
to perform stable humanoid whole-body teleoperation and
execute complex dexterous loco-manipulation tasks.
Task 3                                                                                                                               Task 2
                                                                                    Spray the bowl with water,
Descriptions       Pick the bottle, turn around, and pour into cup
                                                                                    wipe clean, and fold it up
                   Grasp       Move        Pour       Place              Overall     Grasp         Pull       Spray        Put       Overall
Diffusion Policy     0/10      0/10        0/10        0/10                 0/10     0/10         0/10           0/10     0/10           0/10
ACT                  0/10      0/10        0/10        0/10                 0/10     3/10         2/10           4/10     3/10           1/10
InternVLA-M1         0/10      0/10        0/10        0/10                 0/10     0/10         0/10           2/10     4/10           0/10
EgoVLA               4/10      6/10        1/10        2/10                 1/10     0/10         0/10           0/10     0/10           0/10
H-RDT                1/10      0/10        0/10        1/10                 0/10     0/10         1/10           0/10     0/10           0/10
π0.5                10/10      6/10        3/10        2/10                 2/10     9/10          7/10          5/10     7/10           3/10
GR00T N1.6           3/10      5/10        5/10        4/10                 4/10     5/10         5/10           9/10     7/10           4/10
Ψ0 (Ours)            9/10      8/10        8/10        8/10                 8/10     10/10        10/10          9/10     7/10           7/10
Task 4                                                                                                                               Task 1
                   Grab the can, turn and pour onto plate,                          Remove the lid, turn on the faucet,
Descriptions
                   push the cart forward                                            and fill with water
                   Grasp      Rotate       Pour       Grab       Push    Overall     Grasp      Remove         Turn        Put       Overall
Diffusion Policy     0/10      0/10        0/10        0/10       0/10      0/10     0/10         0/10           0/10     0/10           0/10
ACT                  0/10      0/10        0/10        0/10       0/10      0/10     7/10          0/10          0/10     0/10           0/10
InternVLA-M1         2/10      0/10        1/10        0/10       0/10      0/10     0/10         0/10           0/10     0/10           0/10
EgoVLA               0/10      0/10        1/10        0/10       0/10      0/10     0/10         0/10           0/10     0/10           0/10
H-RDT                3/10      1/10        1/10        0/10       0/10      0/10     7/10          0/10          0/10     1/10           0/10
π0.5                 2/10      5/10        5/10        8/10       1/10      1/10     4/10         4/10           8/10     2/10           2/10
GR00T N1.6           5/10      7/10        5/10       4/10       3/10       3/10     10/10         3/10          2/10      3/10          2/10
Ψ0 (Ours)           10/10      9/10        7/10       10/10      10/10      7/10     10/10        10/10          6/10     10/10          6/10
Task 5                                                                                                                               Task 6
                   Put toy into basket, walk                                        Push the cart, grab the grapes,
Descriptions
                   to human, hand it over                                           and place on the plate
                   Grasp       Hook        Walk       Hand               Overall    Handle        Push        Grasp       Place      Overall
Diffusion Policy    0/10       0/10         0/10       0/10                 0/10     0/10         0/10           0/10     0/10           0/10
ACT                 3/10       0/10         5/10       5/10                 0/10     2/10         2/10           0/10     0/10           0/10
InternVLA-M1        2/10       3/10         1/10       1/10                 1/10     8/10         8/10           5/10     5/10           5/10
EgoVLA              0/10       0/10        10/10       1/10                 0/10     0/10         0/10           0/10     0/10           0/10
H-RDT               2/10       0/10         0/10       0/10                 0/10     0/10         0/10           6/10     1/10           0/10
π0.5                9/10       8/10        5/10       5/10                  5/10     8/10         9/10           3/10     3/10           3/10
GR00T N1.6          8/10       5/10        0/10       0/10                  0/10     7/10         9/10           8/10     7/10           4/10
Ψ0 (Ours)           9/10       9/10        10/10      10/10                 9/10     9/10         9/10           7/10     7/10           6/10
Task 8                                                                                                                               Task 7
                   Pull out the tray and                                            Hold the lunch bag and
Descriptions
                   turn to throw the chip can into the trash                        squat down to place on the table
                   Grasp       Pull        Walk       Drop               Overall     Hold         Turn         Squat       Put       Overall
Diffusion Policy     0/10      0/10         0/10       0/10                 0/10     0/10          0/10          0/10     0/10           0/10
ACT                  7/10      1/10         7/10       0/10                 0/10     6/10          8/10          5/10     5/10           5/10
InternVLA-M1         8/10      5/10         1/10       1/10                 1/10     0/10          0/10          0/10     0/10           0/10
H-RDT                8/10      4/10        2/10        0/10                 0/10     9/10          9/10          7/10     6/10           6/10
EgoVLA               0/10      0/10         0/10       0/10                 0/10     3/10          4/10          2/10     2/10           2/10
π0.5                 9/10      3/10        3/10        3/10                 1/10     3/10          9/10          2/10     2/10           2/10
GR00T N1.6          10/10      1/10        10/10       3/10                 1/10     5/10         10/10          5/10     5/10           5/10
Ψ0 (Ours)           10/10      5/10        10/10       9/10                 5/10     10/10         9/10          9/10     9/10           9/10

TABLE III: Real-World Benchmarking: We provide a detailed report of real-world benchmarking results, including sub-task progress. Each
task consists of three to five subtasks, and a trial is counted as successful only if all subtasks are completed. Boldface indicates the best
performance, while underlining denotes the second-best performance.
   Task 2. Spray the bowl with water, wipe clean, and fold             control thread continuously reads actions from the buffer and
it up: The robot holds the spray bottle with its left hand and         feeds them to the RL controller. This control thread operates
removes the cap into the bowl at the center of the desk. It            at 60 Hz to ensure stable lower-body locomotion and maintain
then places the spray bottle back and grasps the green rag.            overall robot stability.
The robot presses the bowl with the fingers of its right hand
to stabilize it, while inserting its left hand with the rag into the                    X. M ORE A BLATION S TUDIES
bowl to wipe the interior. After cleaning, the robot places the
cloth back on the table. Finally, the robot uses its right hand        A. Effect of RTC
to stack the cleaned bowl on top of the bowl on the right.
   Task 3. Pick the bottle, turn around, and pour into cup:               In general, RTC improves action smoothness and stability,
The robot grasps the water bottle with its right hand. It then         and it can reduce failures such as collisions; this might
turns to the right and walks to the blue plate on the table. The       indirectly contribute to higher task success rates. Empirically,
robot pours water from the bottle into the cup on the plate.           we observe that RTC slightly improves Ψ0 performance. To
Finally, the robot places the bottle on the plate.                     fully evaluate the effect of RTC, we also implement RTC
   Task 4. Grab the can, turn and pour onto plate, push the            on GR00T-N1.6 [4] as their code is not fully released. The
cart forward: The robot grasps the can on the table with its           results are given in Table IV. RTC again achieves comparable
right hand. It then turns to the left to face the big food cart.       performance with the baseline.
The robot pours the food from the can onto the plate on the
cart. After pouring, the robot then places the can on the cart.              GR00T-N1.6    Pick the      Pick the       Carry       Overall
Finally, the robot grasps the handle of the cart with both hands                           dumpling      hippo          the box     SR

and pushes the cart forward.                                                 w/o RTC       10/10         7/10           9/10        7/10
                                                                             w/ RTC        6/10          7/10           10/10       6/10
   Task 5. Push the cart, grab the grapes, and place on the
plate: The robot grasps the white cart containing grapes with          TABLE IV: GR00T with RTC. We study the effect of RTC on
both hands and pushes the cart toward the seated person. The           the GR00T baseline. The task consists of three steps. It achieves
robot then grasps the grapes from the cart. It rotates its upper       comparable performance on GR00T with and without RTC.
body to the right and places the grapes onto the plate handed
by the person.
   Task 6. Put the toy into the basket, turn around, and               B. Pre-Training on only 10% EgoDex
hand it over: The robot uses its left hand to place the pink
dumpling toy into the small basket on the right. It then hooks           We also study the data scaling effect for pre-training. In this
the handle of the basket with its right hand, turns around and         case, we use only 10% EgoDex dataset for pre-training, we
walks toward the seated person. Finally, the robot extends its         keep all protocols of post-training and fine-tuning unchanged.
right hand and hands the basket containing the toy to the
person.                                                                  Experiment 1           Pick the        Pick the    Carry          Overall
   Task 7. Hold the lunch bag and squat down to place on                                        dumpling        hippo       the box        SR
the table: The robot holds the lunch bag on the cart with both           Baseline (Ψ0 )         9/10            9/10        10/10          8/10
hands. It then rotates its upper body to the right and slowly            Variant (10% EgoDex)   6/10            1/10        5/10           1/10
squats down, and places the lunch bag flat on the small side             Experiment 2           Grasp           Wipe        Stack up       Overall
                                                                                                bottle          the bowl                   SR
table on the right.
   Task 8. Pull out the tray and turn to throw the chip can              Baseline (Ψ0 )         10/10           9/10        7/10           7/10
                                                                         Variant (10% EgoDex)   9/10            10/10       7/10           6/10
into the trash: The robot grasps the chip can on the table
with its right hand. Using the index finger of its left hand, the      TABLE V: Ablation of Pre-Training on 10% EgoDex. We found
robot inserts it into the inner tray and pulls the tray out of the     that using 10% of EgoDex perform worse than the baseline Ψ0 ,
can. The robot then picks up the chip can, turns to the right,         demonstrating the efficacy of full EgoDex pre-training.
and walks toward the trash area. Finally, the robot places the
empty chip can into the recycling bin.                                   The comparison with baseline Ψ0 for two real-world exper-
                                                                       iments are given in Table V. The experiments show that using
B. Detail Evaluation Metrics                                           only 10% of the EgoDex dataset leads to significantly worse
  Detailed evaluations including all the sub-task progress are         performance on certain tasks and inferior overall performance.
provided in Table III.
C. Deployment                                                          C. Pre-Training on only Humanoid Everyday
   During inference, the deployment system is executed using             To fully evaluate the effect of EgoDex pre-training, we
two asynchronous threads. The policy inference thread peri-            pre-train only on Humanoid Everyday and keep all protocols
odically updates a shared action buffer, running at a lower            of post-training and fine-tuning the same as baseline. The
frequency due to inference latency. In parallel, a low-level           comparisons with two baselines are given in Table VI
  Experiment 1                     Pick the    Pick the   Carry          Overall
                                   dumpling    hippo      the box        SR
  Baseline (Ψ0 )                   9/10        9/10       10/10          8/10
  Variant (HE)                     9/10        4/10       10/10          4/10
  Experiment 2                     Grasp       Wipe       Stack up       Overall
                                   bottle      the bowl                  SR
  Baseline (Ψ0 )                   10/10       9/10       7/10           7/10
  Variant (HE)                     10/10       9/10       4/10           4/10

TABLE VI: Ablation of Pre-Training on HE. We discover that the
HE variant achieves high performance on tasks that do not require
fine-grained manipulation; however, it still lags behind our baseline
on subtasks requiring more precise manipulation.


D. Multi-Task Fine-Tuning
   We also explore the effect of multi-task fine-tuning and
observed that the performance for each individual task drops
compared with single task fine-tuning. We hypothesize that
multi-task training disperses the model’s learning objective and
causes underfitting. The performance comparison is reported
at Fig. 11.


                     0.8
      Success Rate




                                              -10%               - 20%




                           - 70%


        0
                      Task 1              Task 2          Task 3
Fig. 11: Multi-Task Fine-Tuning. Joint fine-tuning (Cyan) across
multiple tasks leads to a performance drop on individual tasks (Pink).
