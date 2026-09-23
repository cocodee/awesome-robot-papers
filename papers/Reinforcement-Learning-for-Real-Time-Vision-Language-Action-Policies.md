                                         Reinforcement Learning for Real-Time Vision-Language-Action Policies
                                                                    Perry Dong∗,†     Kuo-Han Hung∗        Dorsa Sadigh        Chelsea Finn
                                                                                    Stanford University
                                                                    https://pd-perry.github.io/real-time-expo-ft/
arXiv:2609.18207v1 [cs.RO] 16 Sep 2026




                                         Fig. 1: Overview of Real-Time EXPO-FT. Real-Time EXPO-FT addresses the latency of large VLA models by combining
                                         slow action generation with fast reactive control. Bottom left: Task success rates before and after applying Real-Time
                                         EXPO-FT. Bottom right: Training success rates on real-world tasks compared with baselines.


                                            Abstract— Reinforcement learning fine-tuning on top of        this gap by enabling RL fine-tuning that meets the real-time
                                         large, pretrained Vision-Language-Action (VLA) models offers     control requirements of dynamic real-world manipulation. Our
                                         promise for highly reliable robot deployment. However, because   approach builds on EXPO-FT, a framework for sample-efficient,
                                         of their scale, modern VLA models suffer from high inference     reliable VLA fine-tuning with reinforcement learning, and
                                         latency, so the observation used to select an action is often    decouples slow, expressive action generation from fast, reactive
                                         stale by execution time, creating a distribution shift that      action edits: a large pretrained VLA proposes action chunks
                                         can substantially degrade reliability and performance. Prior     using its strong behavior prior, while a lightweight edit policy
                                         work has explored asynchronous policy execution to reduce        performs fast, reactive decision-making by editing actions
                                         the effect of latency, but these methods are mostly built on     in response to changes in state, conditioned on the latest
                                         imitation learning and offer no mechanism for moving beyond      observation. We instantiate this as Real-Time EXPO-FT, an
                                         the training distribution toward higher reliability. We close    RL framework for finetuning real-time VLA policies. On the
                                                                                                          Kinetix benchmark, Real-Time EXPO-FT enables a delayed
                                           * Equal contributions.                                         policy to achieve the best performance among delayed and
                                           † Corresponding author: perryd@stanford.edu                    non-delayed methods in 10 out of 10 environments. On four
dynamic real-world tasks—robot object passing, ball balancing,      to perform fast, reactive decision-making by editing actions
table soccer kicking, and dynamic object picking—with online        in response to changes in the observation. Concretely, at
robot data capped at 10 minutes, Real-Time EXPO-FT improves         inference, the VLA proposes candidates of action chunks;
average policy performance from 42% to 97%, all without
human intervention, demonstrating rapid, sample-efficient           once the actions have been generated and a delay has elapsed,
adaptation to challenging real-world dynamics.                      the edit policy transforms the remaining actions taking into
                                                                    account the latest observation and selects the chunk of
                                                                    remaining actions with the highest Q-value. We instantiate
                      I. I NTRODUCTION                              these ideas as Real-Time EXPO-FT, a reinforcement learning
   Reinforcement learning fine-tuning on top of large, pre-         (RL) framework for fine-tuning real-time VLA policies.
trained vision-language-action (VLA) models offers promise             Our key contribution is a framework for reinforcement
toward highly reliable robot deployment in the real world [19,      learning fine-tuning of real-time policies. We evaluate our
35]. However, the scale behind pretrained VLA models that           approach in both simulation and the real world on highly
makes it a strong behavior prior cuts both ways. While the          dynamic and stochastic tasks that require both fast reaction
large capacity enables complex, multi-step behaviors across         and accurate control. In simulation, we evaluate on the
diverse tasks and embodiments, it also inflates inference           Kinetix benchmark [26] following prior work on real-time
latency, and the physical world does not pause while the            control, and empirically show that Real-Time EXPO-FT
robot computes its next action. As a result, for the most           enables a delayed policy to achieve the best performance
capable models, the observation used to infer an action is          among delayed and non-delayed methods in 10 out of
often not the observation at the time of execution, creating a      10 environments. In the real world, we evaluate on four
distribution shift that can substantially degrade reliability and   dynamic manipulation tasks, including robot object passing,
performance. In this work, we study RL fine-tuning of VLA           ball balancing, table soccer kicking, and dynamic object
policies for real-time execution, trained explicitly considering    picking. These tasks involve rapid state changes, stochastic
inference latency of a large VLA model so that the policy can       outcomes, and tight timing requirements. Across these tasks,
retain maximal reactivity to changes in the environment while       capping the online robot data to 10 minutes, our method
achieving higher reliability with reinforcement learning.           improves the average evaluation policy performance from
   Prior work on asynchronous policy execution has explored         42% (12.5/30) to 97% (29/30), all without human intervention
alternative inference schemes [15, 49], alternative training        during training, demonstrating rapid and sample-efficient
schemes [16], or both [29, 47] to enable reactive control           adaptation to challenging real-world dynamics.
under inference latency. A representative example is real-
time chunking (RTC) [15, 16], which uses action inpainting                              II. R ELATED W ORK
to generate the next action chunk while the current one is          Deep Reinforcement Learning for Robotic Manipulation.
still executing. While such methods enable smooth inference         Reinforcement learning has been widely used to improve
despite latency, they offer no natural mechanism for moving         manipulation policies through direct interaction with the
beyond the training data distribution. While methods like           environment [1, 2, 4–6, 10, 14, 23, 43]. However, real-
RTC can be used for reinforcement learning as a base policy,        world interaction is costly, making sample efficiency a
directly applying RL leaves performance on the table since          fundamental challenge. Prior work addresses this challenge
actions are predicted from previous observations, and thus          through algorithmic design [3, 7, 9, 12, 18, 24] to enable
cannot fully capture the reliability gains that reinforcement       effective policy improvement from limited experience. These
learning affords by improving on the base policy. This gap          methods typically optimize lightweight Gaussian policies,
motivates our work of enabling reinforcement learning fine-         which provide low inference latency and support high-
tuning for real-time policies, so as to simultaneously obtain       frequency control for dynamic manipulation tasks. However,
the reliability benefits of reinforcement learning and the          their limited policy capacity prevents them from leveraging
reactivity benefits of real-time execution.                         the broad behavioral priors of large pretrained models, often
   Our key insight is that reinforcement learning can allow the     requiring substantial number of samples and small breadth
VLA policy to be maximally reactive by editing the action           of initial states. Our work bridges this gap by enabling
to be executed using the latest observation at the time of          sample-efficient RL adaptation of pretrained VLAs while
execution, with the base action being generated from the            satisfying the latency and reactivity constraints of real-time
VLA using previous observations given the inference latency.        manipulation.
We build on EXPO-FT [35], a system for sample-efficient,            Reinforcement Learning for Vision-Language-Action Mod-
reliable VLA fine-tuning with reinforcement learning that           els. Recent work has explored reinforcement learning for
features a large VLA base policy and a small edit policy.           finetuning pretrained vision-language-action models. However,
Specifically, we turn pretrained VLA policies into reactive         modern VLAs [19, 20, 27, 30, 33] often employ expressive
controllers by decoupling slow action generation from fast,         generative policies, such as diffusion or flow-matching poli-
observation-conditioned action generation. We assign the            cies, making conventional continuous-control RL algorithms
base VLA, a large policy with a strong behavior prior, to           difficult to apply directly. Several works address this mismatch
be responsible for initial action chunk generation, which           by developing RL algorithms tailored to diffusion or flow-
can incur substantial inference delay, and the edit policy          based policies [11, 13, 28, 36–38, 40, 41, 44, 48, 52]. Multiple
                                                                       hP                        i
                                                                            T      t
online RL methods use on-policy algorithms to finetune the          Eπ      t=0  γ   r(st , at )  , where γ ∈ [0, 1] is the discount factor.
VLA [28, 34, 52], which can require extensive environment           We consider the problem of reinforcement learning fine-tuning
interaction. Consequently, recent work has increasingly ex-         of VLA models under a real-time constraint, where policy
plored off-policy RL for VLA finetuning [17, 22, 31, 35,            inference time needs to be faster than the control frequency f .
39, 50, 51], as it can reuse previously collected experience        Because VLAs are large models, inference itself is costly. We
and substantially improve sample efficiency. Our work builds        denote the delay of timesteps from inference as d. Modern
on EXPO-FT [35], a system for sample-efficient, reliable            VLAs often employs action chunking, predicting a sequence
finetuning of VLA models with reinforcement learning, and           of H future actions at:t+H at each timestep and executing
we focus on a largely unexplored challenge: enabling RL fine-       C ≤ H at each timestep. We assume the delay d is less than
tuning while meeting the real-time control requirements of          or equal to execution length C.
dynamic real-world manipulation. In particular, whereas prior          Training-Time Real-Time Chunking [16]. When infer-
work have shown improving policy performance and sample             ence incurs a delay of d timesteps, the first d actions of a
efficiency from RL fine-tuning, we study how to obtain these        newly predicted chunk cannot be executed, since by the time
benefits while achieving sufficiently low inference latency for     they are produced the environment has already advanced to
high frequency control in dynamic environments.                     t + d. Training-time RTC [16] addresses this issue in the
Real-Time Inference for Vision-Language-Action Models.              imitation learning setting by additionally executing actions
VLA models typically incur substantial inference latency            at+C:t+C+d from the previous chunk while inference for
due to their large size, limiting their ability to support          the new chunk is in progress, and conditioning the new
high-frequency control. Prior work has explored system-             prediction on this committed action prefix. Specifically, given
level techniques to accelerate VLA inference [25, 32, 45,           the original state st and the committed action prefix aprev       t:t+d ,
46], including model compression [32], kernel-level opti-           the policy predicts the remaining actions as at+d:t+d+H ∼
mization [25], accelerated sampling [45], and speculative           π(· | st , aprev
                                                                                t:t+d ). By conditioning on both the current state
inference [46]. Another line of work modifies the inference         and the already-committed actions, the policy can account
or training procedure to enable more responsive execution.          for inference latency and produce a coherent continuation of
One strong, widely used approach is real-time chunking              the action chunk. During training, the delay d is randomly
(RTC) [15], which uses action inpainting to generate the            sampled across a range of values so that the policy learns to
next action chunk while the current chunk is still being            remain robust to varying inference latencies at deployment
executed, thereby enabling asynchronous VLA execution.              time.
Subsequent works incorporate this capability directly into             EXPO and EXPO-FT [35, 38]. To finetune the VLA
policy training. Training-Time RTC [16] and VLASH [49]              policy with RL, we build on EXPO [38], a recently proposed
modify the standard VLA training procedure by incorporating         RL algorithm that is both highly sample-efficient and stable
action conditioning or future-state prediction during training      for training expressive policies. Classical sample-efficient RL
to enable asynchronous action generation during inference.          algorithms are designed around Gaussian policies and cannot
πR2 [47] combines a fast proprioceptive channel alongside a         be directly applied to pretrained VLAs, which typically use
slow updated vision-language channel. Other approaches use          flow or diffusion policies; EXPO instead provides a principled
auxiliary policies and correction modules to refine actions         foundation for RL fine-tuning in this regime.
between successive VLA updates [29, 42]. Different to these            EXPO couples two parameterized policies. The first is
approaches, we focus on the reinforcement learning setting          a base flow policy—in our setting the VLA model πVLA ,
with the goal of enabling reinforcement learning fine-tuning        obtained through supervised training—and the second is a
for real-time policies. These prior methods are general and         small edit policy πedit whose objective is to maximize the
can in principle be combined with RL post-training; our             learned Q-value:
insight, however, is that the structure of modern RL algorithms
enables us to design an approach that is even more performant
                                                                                                            
                                                                       L(πedit ) = −E(st ,at )∼D, ât ∼πedit Qϕ (st , at + ât )
(Figure 3 and Figure 5).                                                                                                                         (1)
                                                                                                              − α log πedit (ât |st , at )
                     III. BACKGROUND                                 Rather than altering the base action outright, πedit predicts
   We consider the standard reinforcement learning frame-           a bounded edit â restricted to [−β, β], which is summed
work, where problems are modeled by a Markov decision               with the base action a to yield the edited action ã = a + â,
process (MDP) M = (S, A, r, T, γ, ρ). In the MDP, S is the          transforming the base action to a higher value distribution.
state space and A is the action space. At each timestep             Confining the Q-function signal to this edit avoids backpropa-
t, the agent selects action at ∈ A according to policy              gation of the Q-value to the VLA backbone and also anchored
π(· | st−d , st ) and receives scalar reward r(st , at ) ∈ R. The   to actions already close to optimal. During rollout or backup
environment transitions following the transition dynamics of        target construction, EXPO uses an on-the-fly (OTF) policy
the MDP st+1 ∼ T (· | st , at ), with starting state initialized    that chooses the highest-value action candidate from the base
from s0 ∼ ρ(·). The tuple (st , at , rt , st+1 ) is added to the    and edited actions:
replay buffer D for learning. The goal of reinforcement                                ã∗ =        arg max        Qϕ (s, a)                      (2)
learning is to maximize the expected discounted return                                         a∈
                                                                                                    SN {a , ã }
                                                                                                     i=1 i    i
Figure 2 - method


                                                         Policy Inference                                                                            Q function Training
                               delay d (async inference)                                                                                                         delay d


             st⋅1       st         st+1          st+2          st+3      st+4        st+5       st+6        st+7         st+8                         st       st+1      st+2        st+3
                                                                                                                                      Time

                              at          at+1          at+2          at+3       aat+4
                                                                                    t       at+5         at+6       at+7
                                                                                                                                    Action
                                    Action prefix                                                                                    Queue           ϵ1
                                                                                                                                                     ϵ2                         ϵk
                                                    1
                                                   at:t+H                                   ã1t+d:t+d+C     1
                                                                                                            at+d:t+d+C           Q(st+d, a 1)                     Q dn                πVLA
                                                                                                                                                     …
                                                                                                                …
                                                    2
                                                   at:t+H                                   ã2t+d:t+d+C     N
                                                                                                            at+d:t+d+C              Q(st+d, a N )    ϵN
                      πVLA                                               πedit
                                                                                                            ã1t+d:t+d+C        Q(st+d, ã1)
                                                                                                                                                                                      ad:d+C
                                                                                                                                                            Noise filtering
                                                        …             Edit Policy               …           ã2t+d:t+d+C              Q(st+d, ã2)
                    VLA Policy                                                                                                                                (optional)
                                                                                                                …
                                                    N
                                                   at:t+H                                   ãNt+d:t+d+C    ãNt+d:t+d+C           Q(st+d, ã N )
                                                                                                                                                           Distill Q dn from Q
                                                                                                                                                                                        Q
            VLA Inference Asynchronously                              Edit and Select Best Action Synchronously


       Fig. 2: Left: Real-time policy inference of Real-Time EXPO-FT. Real-Time EXPO-FT decouples slow VLA action
       generation from fast, reactive decision-making. While the robot executes the current action chunk, the VLA asynchronously
       generates multiple candidate action chunks. Once new actions are required, a lightweight edit policy refines candidates using
       the latest observation, and a learned Q-function selects the highest-value action chunk for execution. Right: Noise-level
       filtering during Bellman backup. During Bellman backup, we filter samples in the noise space to reduce training compute.


        The critic itself is fit by temporal-difference:                                                    inference finishes. This assumption is increasingly untenable
                                                  h                                                         for large VLA policies, and it is especially costly to make
              L(ϕ) = E(st ,at ,st+1 )∼D                 rt + γQϕ′ (st+1 , ã∗t+1 )
                                                                                                   (3)
                                                                                                            during RL fine-tuning because standard RL assumes the
                                                                               2 i
                                                              − Qϕ (st , at )                               Markov property, that the executed action is a function of
                                                                                                            the current state, at ∼ π(· | st ); under latency the action
         EXPO-FT [35] is a system on top of EXPO to finetune                                                at t is actually a function of st−d , so the delayed process
       VLA models, incorporating human-in-the-loop and action                                               is no longer Markovian in st , and applying standard RL
       chunking. We build directly on top of EXPO-FT. While                                                 updates as if can bias credit assignment. This is specifically a
       human intervention can provide useful corrective signals, we                                         problem when running RL for high reliability, where actions
       do not use human intervention for the experiments in this                                            are refined precisely. Treating inference latency as negligible
       paper.                                                                                               therefore risks significantly undermining the reliability that
                             IV. R EAL -T IME EXPO-FT                                                       RL fine-tuning can deliver, motivating the need for an explicit
                                                                                                            solution.
         In this section, we present a complete framework for fine-
       tuning VLA models with reinforcement learning for real-time                                             For tasks that require real-time execution, we empirically
       control. Our goal is to efficiently enable pretrained VLA                                            observe that existing πVLA models cannot achieve satisfactory
       policies to reach high reliability in dynamic environments.                                          success rates out of the box. Therefore, following the standard
       We first formalize the learning setting and objective (Section                                       online RL finetuning practices, we assume access to a small
       IV-A), then introduce our real-time RL algorithm for VLA                                             offline dataset of expert demonstrations, D0 , collected via
       models (Section IV-B), and finally describe the training                                             either human teleoperation or scripted policies operating at
       procedure (Section IV-C).                                                                            the same control frequency. We adopt a sparse binary reward
                                                                                                            r ∈ [0, 1] indicating successful task completion. The task
       A. Problem Statement                                                                                 completion classifier may be either rule-based or learned.
          We consider the problem of finetuning vision-language-                                            Observations consist of multi-view RGB images from a wrist-
       action models πVLA using reinforcement learning for real-time                                        mounted camera and a fixed side-view camera, augmented
       robotic control. Policy inference, especially for a large policy,                                    with the robot’s proprioceptive state. Policy parameters are
       may take non-negligible time, such that naively executing the                                        updated either after every environment step, at the end of each
       predicted actions with a delay will result in distribution shift                                     episode, or at fixed episode-batch intervals. The objective is
       and the action executed at time t + d has to be computed                                             to maximize the task success rate.
       from earlier observations to mitigate the compute latency.                                              To address the latency of πVLA under high-frequency
          A common simplifying assumption in prior work is that                                             control, rather than optimizing the inference latency of the
       policy inference is effectively instantaneous, so the action                                         VLA model itself, we focus on asynchronously fine-tuning
       computed from an observation can simply be executed once                                             and executing the policy while maintaining a fixed real-
time control frequency. Suppose the VLA model requires            selects the highest-value action chunk for execution:
t seconds for each inference and the robot operates at a
control frequency of f Hz. The inference process therefore         ã∗t+d:t+d+C =        SN
                                                                                                   arg max                 Qϕ (st+d , a)
                                                                                                i            i
                                                                                    a∈    i=1 {at+d:t+d+C ,ãt+d:t+d+C }
incurs a delay of approximately d = ⌊t × f ⌋ + 1 control
                                                                                                                             (6)
steps, meaning that to execute a new action at timestep t + d,
                                                                  This design enables expensive VLA inference to run asyn-
inference must be initiated approximately d control steps
                                                                  chronously in the background while preserving fast, state-
earlier, at timestep t. For typical hardware and VLA models,
                                                                  aware correction and selection immediately before execution.
we assume 1 ≤ d ≤ C, where C denotes the execution
                                                                  Training Objective. We now describe how the action critic
horizon of the policy. This inference delay creates a mismatch
                                                                  Qϕ , edit policy πedit , and VLA πVLA are updated. We use
between the observation used to initiate VLA inference and
                                                                  Qϕ′ to denote the target critic.
the robot state at which the resulting action is eventually
                                                                     We fine-tune πVLA with the Training-Time RTC objective
executed. Our goal is therefore to fine-tune the VLA policy
                                                                  [16] on both offline demos and online data from rollouts.
using RL to explicitly account for this delay and improve
                                                                  Following RTC, we simulate inference delay during training
policy performance under real-time control. In the following
                                                                  by splitting each ground-truth action chunk into a d-step
section, we discuss how these challenges are addressed in
                                                                  action prefix and a remaining action postfix. The prefix is
our approach, Real-Time EXPO-FT.
                                                                  provided to the policy as clean, non-noisy actions with its
                                                                  flow-matching timesteps set to 1, while noise is added only to
B. RL for Real-Time Vision-Language-Action Policies               the postfix. The flow-matching loss is masked to the postfix:
    We build on EXPO-FT [35] as a sample efficient RL fine-
tuning framework. Real-Time EXPO-FT addresses the real-                      Aτt = τ At + (1 − τ )ϵ, ϵ ∼ N (0, I),
                                                                                               h
time inference challenge by decoupling action generation into        LBC (πVLA ) = E(st ,At )∼D md ⊙ vVLA (Aτt , st , τ d )               (7)
two timescales: a slow, asynchronous step that generates                                                               2i
candidate action chunks ahead of execution, and a fast,                                                 − (ϵ − At ) 2
synchronous step that edits and selects among the highest
value candidates at the time of execution, conditioned on the        where md masks out the first d actions from the loss and
most recent observation. The method is illustrated in Figure 2.   τ d assigns flow-matching timestep 1 to the prefix and τ to
                                                                  the postfix. We use the specific execution delay d for the
Asynchronous VLA Action Generation. The VLA is a
                                                                  state after first chunk, and 0 for the first [0, C] state in each
large, expressive model for capturing behaviors, and because
                                                                  episode during training.
of its scale, calling the model during inference introduces a
delay of d steps. We therefore begin inference from πVLA             We train the edit policy to bring the base actions from
asynchronously at time t when d steps remain in the currently     the VLA toward higher value regions like in EXPO [38] and
queued action chunk. We sample multiple candidate action          EXPO-FT [35]:
chunks from the observation st . Following the training-time                                         h                         
RTC formulation [16], the actions from the previous chunk,              L(πedit ) = −E(st ,at:t+C )∼D Qϕ st , at:t+C + ât:t+C
aprev
  t:t+d , that are executed during the VLA inference window
                                                                                         ât:t+C ∼πedit                                   (8)
                                                                                                                               i
are inpainted as conditioning input when sampling future                                 − α log πedit ât:t+C | st , at:t+C
actions. Specifically, for each candidate i, we sample:
                                                                     Because the edit is conditioned on the latest observation,
                                                                  the combined base-plus-edit policy remains Markovian with
        ait:t+H = πVLA (st , aprev     i
                              t:t+d , ϵ ),   ϵi ∼ p(ϵ)      (4)
                                                                  delays. We train the critic to fit a chunk-level temporal-
                                                                  difference backup, in which one transition spans the full
   where ϵi denotes the sampling noise used to produce diverse
                                                                  execution horizon C and the bootstrap term is evaluated at
VLA candidates. Since the first d actions correspond to the
                                                                  the next chunk ã∗t+C:t+2C ,
inference-delay window, we retain only the subsequent C-step
action segment ait+d:t+d+C for each action candidate.                                                 h
                                                                                                          rt + γ Qϕ′ st+C , ã∗t+C:t+2C
                                                                                                                                          
Fast, Synchronous Edits. Once the environment arrives at           L(Qϕ ) = E(st ,at:t+C ,st+C )∼D
the latest observation st+d for execution, a lightweight edit                                                                 2 i
                                                                                                             − Qϕ st , at:t+C
policy πθedit transforms each candidate based on the latest
                                                                                                                                          (9)
observation to account for state changes during the inference
                                                                     Constructing the next chunk ã∗t+C:t+2C is computationally
delay and maintain reactivity:
                                                                  expensive, as naively sampling N candidates from πVLA
                                                                  requires N full VLA rollouts. We instead (optionally) search
         âit+d:t+d+C ∼ πθedit · | st+d , ait+d:t+d+C
                                                        
                                                            (5)   in noise space using a lightweight critic Qdn    ψ , which scores
                                                                  candidate noise without denoising full actions, following
    The edited actions are ãit+d:t+d+C = ait+d:t+d+C +           FASTER [40]. At backup time, we select the best noise,
âit+d:t+d+C . Finally, the action critic Qϕ evaluates both the   decode it once with πVLA to obtain a, generate K edits with
original and edited candidates under the current state and        πedit , and use the target critic to select the final action chunk,
                                         Car Launch                   Cartpole Thrust                         Catapult                          Catcher V3                     H17 Unicycle
Training Success Rate
                        1.0

                        0.8

                        0.6

                        0.4

                        0.2

                        0.0

                                  Hard Lunar Lander                   Mjc Half Cheetah                        Trampoline                    Chain Lander                          Grasp Easy
Training Success Rate




                        1.0

                        0.8

                        0.6

                        0.4

                        0.2

                        0.0
                              0    20k    40k   60k   80k    100k 0   20k   40k    60k   80k   100k 0   20k    40k   60k   80k   100k 0   20k    40k   60k   80k   100k 0   20k    40k   60k   80k   100k
                                           Env Step                         Env Step                            Env Step                          Env Step                          Env Step


                                                            Ours (d=4)                         EXPO-FT w/o RTC (d=4)               DSRL w/o RTC (d=4)               BC (d=0)
                                                            EXPO-FT w/ RTC (d=4)               DSRL w/ RTC (d=4)                   RLPD (d=0)                       RTC (d=4)



Fig. 3: Training success across all 10 Kinetix [26] simulation tasks. The vertical dashed lines indicate the evaluation
performance of two BC baselines, one with no inference delay and one with a 4-step delay. Each setting is run with 4 seeds.


                                                                                                                     learning with Equation (7) under a randomized delay d, until
                                   ϵ∗ = arg max Qdn
                                                                                                                    it reaches a success rate of around 30% or higher. This data
                                                   ψ st+C−d , ϵi ,
                                        h
                                            i∈[N ]                                                                   is then used to initialize the replay buffer. Starting from
                                                                       i                                            the supervised fine-tuned VLA policy, we then begin online
                                    a = πVLA st+C−d , aprev
                                                        t+C−d:t+C , ϵ
                                                                     ∗
                                                                                ,
                                                                          d:d+C                                      RL training. The actor executes rollouts in the environment
                         ã∗t+C:t+2C = arg max Qϕ′ st+C , a′
                                                               
                                                                                                                     without human intervention, and the policy is updated after
                                                a′ ∈{a, a+â}
                                                                                                                     each episode, depending on the task requirements and
                                                              (10)
                                                                                                                     available computational resources.
   where ϵi ∼ N (0, I), â ∼ πedit (· | st+C , a). In this way the
                                                                                                                     Reward Classifier. Reliable deployment requires an accurate
candidate set is filtered once in noise space and once again
                                                                                                                     and robust reward signal. To minimize task-specific reward
after editing, while only a single VLA decode is required
                                                                                                                     engineering, we use a sparse binary reward for all tasks.
per backup regardless of N . Finally, Qdn  ψ is kept consistent
                                                                                                                     Specifically, we define a rule-based classifier for each task that
with the action critic by regressing it onto the value that Qϕ′
                                                                                                                     assigns a positive reward only when the task is successfully
assigns to the decoded chunk, with a stop-gradient on the
                                                                                                                     completed, and zero otherwise. The reward classifiers for all
target,
                                            h                                                                        tasks are detailed in Section VII-D. This simple formulation
                                                         ∗
                                  L(Qdn        dn
                                     ψ ) = E Qψ st+C , ϵ                                                             avoids dense reward design while remaining effective across
                                                                          2 i                         (11)        a diverse set of tasks.
                                              − sg Qϕ′ st+C , ã∗t+C:t+2C
                                                  

                                                                                                                                                  V. E XPERIMENTS
   so that noise-space selection inherits the ranking of the
action-space critic as the latter improves. This allows a large                                                         We evaluate Real-Time EXPO-FT on ten environments in
number of action candidates to be used during training, which                                                        the Kinetix environment [26] and four dynamic real-world
is helpful for accelerating training.                                                                                tasks, comparing against strong prior methods.

C. Implementation Details                                                                                            A. Baselines
Vision Backbone. At each timestep t, the state st comprises                                                             RLPD [9]. RLPD is a sample-efficient off-policy reinforce-
visual observations from the side and wrist cameras and                                                              ment learning algorithm based on Soft Actor-Critic (SAC) [3],
robot joint positions, and is provided to both actor and                                                             using balanced sampling between offline demonstrations and
critic. VLA actor processes the visual observations using                                                            online experience. It has demonstrated strong performance
its pretrained visual encoder. Following EXPO-FT [35], we                                                            across robotic manipulation tasks. RLPD uses a lightweight
equip critic with a separate, lightweight ResNet-50 encoder,                                                         Gaussian policy as the actor, enabling efficient high-frequency
which achieves high task performance at low computational                                                            control. Since it is naturally suited for real-time control, we
cost. Full architectural details are provided in Section VII-E.                                                      run it as is without modification.
Training Procedure. For each task, we begin by configuring                                                              DSRL [31], DSRL w/ RTC. DSRL is a recent reinforce-
the camera setup and defining the reward signal, which                                                               ment learning method for finetuning pretrained diffusion and
can take the form of a rule-based criterion or a learned                                                             flow-matching policies. Rather than directly optimizing the
binary classifier. Before online RL begins, we collect a set                                                         policy weights, it learns to predict noise input to the pretrained
of demonstrations and fine-tune the VLA using imitation                                                              policy. However, applying DSRL directly to high-frequency
control, such as 30 Hz, causes the policy to pause between        matching policy and no delay for only the action edit. This
action chunks, disrupting real-time execution. We therefore       result is particularly notable because the RLPD policy has
also evaluate DSRL with training-time RTC [16].                   access to the current observation when producing each action,
   EXPO-FT [35], EXPO-FT w/ RTC. EXPO-FT is a state-              whereas Real-Time EXPO-FT must generate the candidate
of-the-art reinforcement learning framework for finetuning        actions based on delayed observations. We present additional
pretrained VLA policies. Similar to Real-Time EXPO-FT, it         experiments on the effectiveness of noise filtering evaluated
adopts EXPO [38] for policy improvement. However, directly        in simulation in Section VII-A.
applying EXPO-FT to high-frequency control can cause
pauses between action chunks at 30 Hz. We therefore also          C. Real-World Experiment
evaluate EXPO-FT with training-time RTC [16] for a stronger       Task Setup. In all real-world experiments, the robot is
comparison under real-time execution.                             controlled in end-effector space using Cartesian and gripper
   RLPD and DSRL are trained asynchronously, with the             velocity commands at 30 Hz. At each timestep, the policy
learner updating asynchronously at high update-to-data (UTD)      receives two 224 × 224 RGB images from side- and wrist-
ratios; this affords them substantially more gradient updates     mounted cameras, along with proprioceptive observations
than EXPO-FT and Real-Time EXPO-FT, which perform                 comprising the end-effector position and orientation. Envi-
updates per episode. This asymmetry favors RLPD and DSRL.         ronment resets are performed either automatically or by a
We nonetheless retain this advantage for these prior methods      human operator, depending on the task. We evaluate Real-
throughout our experiments, as without it their performance       Time EXPO-FT on four real-world tasks, shown in Figure 4.
degrades considerably, noting that even so, EXPO-FT and           Ball Balancing. The Ball Balancing task requires the robot
Real-Time EXPO-FT achieve higher performance despite the          to control a black plate with a ping-pong ball on top. The
compute disadvantage.                                             robot must continuously rotate the plate to keep the ball near
                                                                  its center for several consecutive frames. The task is highly
B. Simulation Experiment                                          dynamic and stochastic, requiring smooth and reactive control
   Task Setup. For our simulation experiments, we evaluate        to small changes in the ball’s position.
each approach on 10 dynamic tasks from the Kinetix bench-         Dynamic Picking. The Dynamic Picking task requires the
mark [26], as shown in Figure 3, following the RTC setup          robot to pick up a block placed on a rotating plate. The block
[15]. The environments use force-based control with Gaussian      can start at arbitrary positions, resulting in different motion
action noise and feature dynamic motions such as catching         speeds and trajectories. The policy must infer the block’s
and balancing, making dynamic control crucial for successful      motion and quickly reach and grasp it before it moves away.
execution. Following the RTC setup [15], we pretrain the          Object Passing. The Object Passing task requires the robot
RTC flow-matching policy offline on 1M transitions, then          to receive an object from another robot arm with random
finetune it online for 100k environment steps across all tasks.   motion. The policy must continuously react to the motion
For all RL methods that use a base flow-matching policy,          of the other arm and rapidly move the end effector toward
each call to the base policy incurs a 4-step inference delay      the object’s predicted position. The unpredictability of the
during online finetuning and evaluation. The policy in RLPD       object’s motion makes timely and reactive control essential.
and the edit policy in our method incurs no additional delay      Soccer Kicking. The Soccer Kicking task requires the robot
due to their lightweight nature, and is evaluated with zero       to kick a ball into a small goal while avoiding a moving
inference delay. As a reference, we additionally report the       defender. Successful execution requires precise spatial control
pretrained BC policy under zero delay, which provides a           and timing. The policy must determine both where to kick
reference on the performance achievable without inference         the ball and when to initiate the kick.
latency.                                                             The VLA policy has an inference latency of approximately
   Experiment Results. Now we present the simulation              67 ms on our server. For Ball Balancing, Object Passing, and
results. Figure 3 shows the training curves, while the full       Soccer Kicking, we introduce an additional 100 ms delay to
evaluation results are reported in Section VII-B. Real-Time       simulate the higher inference latency associated with more
EXPO-FT achieves an average success rate of 96.2% under           constrained computing resources or a larger model, yielding a
the 4-step delay, substantially outperforming all delayed RL      total latency of approximately 167 ms. For these three tasks,
baselines. In particular, it improves over DSRL, DSRL w/          we set the delay d to 5, corresponding to approximately 167
RTC, EXPO-FT, and EXPO-FT w/ RTC by 34.5, 20.1, 21.3,             ms. For Dynamic Picking, we retain the original inference
and 14.5 percentage points, respectively, demonstrating that      latency of 67 ms and set the delay d to 3. Adding further
explicitly addressing stale observations and delayed action       latency reduces the success rates of all non-asynchronous
generation is broadly effective across dynamic tasks and          baselines to nearly zero, as delayed gripper closure prevents
delayed settings. Importantly, Real-Time EXPO-FT not only         timely grasping of the moving block.
compensates for inference delay but also surpasses the no-           Given the number of baselines and the computational cost,
delay RLPD baseline on average. While the RLPD policy             we cap training at 10 minutes of online robot interaction
achieves an average success rate of 81.4% when evaluated          per task for all methods. We evaluate each task over 30
with zero delay, Real-Time EXPO-FT reaches 96.2% while            trials. Success is independently verified by a human observer.
operating with a 4-step inference delay for the base flow-        Further details on reward definitions, success detection,
Fig. 4: Four real-world manipulation tasks in our evaluation suite: Dynamic Picking, Ball Balancing, Object Passing,
and Soccer Kicking. All tasks require fast and reactive policies for dynamic environment changes.



                                  Dynamic Picking                       Ball Balancing                                                                Object Passing                                                                        Soccer Kicking
                        1.0
Training Success Rate




                        0.8


                        0.6


                        0.4


                        0.2


                        0.0
                              2     4       6         8     10    2         4        6         8      10     0.8                                     1.6       2.4          3.2         4      4.8                                    2         4          6       8        10
                                   Robot Data (min)                         Robot Data (min)                                                               Robot Data (min)                                                                   Robot Data (min)


                                            Ours           EXPO-FT w/ RTC                EXPO-FT w/o RTC                                             DSRL w/ RTC                            DSRL w/o RTC                                            RLPD



Fig. 5: Training success across four real-world dynamic tasks. We train each policy with at most 10 minutes of online
robot data, or until one of the policies achieves 30/30 success during evaluation.

TABLE I: Success rates on four real-world tasks. Each task is evaluated over 30 trials. We train each policy until one
policy reaches a 30/30 success rate or 10 minutes of online data have been collected and used for training.
                                                                        Success Rate (x/30). Training is capped at 10 minutes of online data.
Task
                                          SFT         SFT w/ RTC      RLPD           DSRL          DSRL w/ RTC                                               EXPO-FT                    EXPO-FT w/ RTC                                               Real-Time EXPO-FT
Dynamic Picking                          19/30            22/30        0/30          23/30             25/30                                                   21/30                               24/30                                                    30/30
Ball Balancing                            8/30            12/30        12/30         11/30             15/30                                                   18/30                               23/30                                            28/30 (10 min reached)
Object Passing                           10/30            22/30         0/30         23/30             23/30                                                   19/30                               27/30                                                    30/30
Soccer Kicking                           13/30            16/30        6/30          16/30             17/30                                                   17/30                               26/30                                            28/30 (10 min reached)
Average                                 12.5/30           18/30       4.5/30        18.3/30            20/30                                                  18.8/30                              25/30                                                       29/30


                                                                                                                                                           H17 Unicycle (Sim)                                                              Object Passing (Real)
reset procedures, and task randomization are provided in
                                                                                                             Evaluation Success Rate (%)




                                                                                                                                                                                                      Evaluation Success Rate (%)




                                                                                                                                           100                                                                                      100

Section VII-D.
                                                                                                                                                                                                                                     85
   Experiment Results. We now present our experimental                                                                                     90


results on the four dynamic real-world tasks. As shown in Fig-                                                                                                                                                                       70

                                                                                                                                           80
ure 5 and Table I, Real-Time EXPO-FT consistently achieves                                                                                                                                                                           55

near-perfect performance across all four tasks, with an average                                                                            70
                                                                                                                                                 0            1       2       3                4                                     0.5x      0.75x      1.0x      1.25x
success rate of 29/30, substantially outperforming all prior                                                                                                  Execution Delay d                                                       Environment Object Operation Speed

methods. In particular, Ball Balancing exhibits substantial                                                                                                          Ours         RTC                                               Ours    EXPO-FT w/ RTC      EXPO-FT w/o RTC

environmental randomness, where small perturbations in the
ball’s motion can lead to significantly different future states,                                           Fig. 6: Success rates under varying delays and environment
making rapid adaptation to the latest observation particularly                                             speeds. We evaluate Real-Time EXPO-FT and the baselines
important. On this task, Real-Time EXPO-FT achieves 28/30                                                  on the H17 Unicycle task with varying delays d and on the
success, while no prior method exceeds 23/30. Overall, Real-                                               Object Passing task with varying passing speeds.
Time EXPO-FT significantly improves over prior methods.
                                                                                                           additional experiments varying inference delays in the H17
D. Performance under varying delays and environment speeds                                                 Unicycle simulation task and object-passing speeds in the
  To further investigate the effectiveness of Real-Time EXPO-                                              real-world Object Passing task. For varying delays, we
FT in highly dynamic, real-time settings, we conduct two                                                   train Real-Time EXPO-FT with different delays to simulate
variations in hardware capabilities and base-model inference         [5]   Tuomas Haarnoja, Aurick Zhou, Kristian Hartikainen,
speeds. As shown in Figure 6, Real-Time EXPO-FT maintains                  George Tucker, Sehoon Ha, Jie Tan, Vikash Kumar,
stable performance as the delay increases, whereas RTC’s                   Henry Zhu, Abhishek Gupta, Pieter Abbeel, and Sergey
performance deteriorates under longer delays. These results                Levine. Soft Actor-Critic Algorithms and Applications.
highlight the importance of accounting for inference latency               2019. arXiv: 1812.05905 [cs.LG].
in real-time control and demonstrate that our approach can           [6]   Ajay Mandlekar, Fabio Ramos, Byron Boots, Silvio
better handle delays. For the object speed experiment, we                  Savarese, Li Fei-Fei, Animesh Garg, and Dieter Fox.
evaluate Real-Time EXPO-FT against two EXPO-FT variants                    IRIS: Implicit Reinforcement without Interaction at
across different environment speeds. As shown in Figure 6,                 Scale for Learning Control from Offline Robot Manip-
Real-Time EXPO-FT maintains a near-100% success rate                       ulation Data. 2020. arXiv: 1911.05321 [cs.RO].
across all tested speeds, whereas EXPO-FT without real-time          [7]   Xinyue Chen, Che Wang, Zijian Zhou, and Keith W.
degrade in performance as the passing speed increases. These               Ross. “Randomized Ensembled Double Q-Learning:
results further demonstrate the importance of fast, reactive               Learning Fast Without a Model”. In: International
action edits for dynamic environments.                                     Conference on Learning Representations. 2021.
                                                                     [8]   Edward J Hu, yelong shen, Phillip Wallis, Zeyuan
                      VI. D ISCUSSION
                                                                           Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
   We presented Real-Time EXPO-FT, a framework for RL                      Weizhu Chen. “LoRA: Low-Rank Adaptation of Large
finetuning of real-time VLA policies. Across a suite of                    Language Models”. In: International Conference on
challenging dynamic robotic tasks, Real-Time EXPO-FT                       Learning Representations. 2022.
demonstrates rapid sample-efficient adaptation to complex            [9]   Philip J. Ball, Laura Smith, Ilya Kostrikov, and Sergey
real-world dynamics. Despite these results, Real-Time EXPO-                Levine. “Efficient online reinforcement learning with
FT has limitations. First, a human provides environment resets             offline data”. In: Proceedings of the 40th International
in our experiments, which introduces operational burden; au-               Conference on Machine Learning. ICML’23. Honolulu,
tomating the reset process is an important direction for future            Hawaii, USA: JMLR.org, 2023.
work. Second, we use task-specific success detector following       [10]   Archit Sharma, Ahmed M. Ahmed, Rehaan Ahmad,
prior work; however, this requires designing classifier per task.          and Chelsea Finn. Self-Improving Robots: End-to-End
While we do not explore alternative reward specifications in               Autonomous Visuomotor Reinforcement Learning. 2023.
this work, identifying which reward formulation performs                   arXiv: 2303.01488 [cs.RO].
best remains an open question for future work.                      [11]   Max Sobol Mark, Tian Gao, Georgia Gabriela Sampaio,
                 VII. ACKNOWLEDGMENTS                                      Mohan Kumar Srirama, Archit Sharma, Chelsea Finn,
                                                                           and Aviral Kumar. Policy Agnostic RL: Offline RL and
  This work was in part supported by NSF CAREER, NSF                       Online RL Fine-Tuning of Any Class and Backbone.
#1941722, RAI Institute, ONR grant N00014-22-1-2293, and                   2024. arXiv: 2412.06685 [cs.LG].
ONR grant N00014-22-1-2621.                                         [12]   Michal Nauman, Mateusz Ostaszewski, Krzysztof
                        R EFERENCES                                        Jankowski, Piotr Miłoś, and Marek Cygan. Bigger, Reg-
                                                                           ularized, Optimistic: scaling for compute and sample-
 [1] Sergey Levine, Chelsea Finn, Trevor Darrell, and Pieter
                                                                           efficient continuous control. 2024. arXiv: 2405 .
     Abbeel. End-to-End Training of Deep Visuomotor
                                                                           16158 [cs.LG].
     Policies. 2016. arXiv: 1504.00702 [cs.LG].
                                                                    [13]   Michael Psenka, Alejandro Escontrela, Pieter Abbeel,
 [2] Shixiang Gu, Ethan Holly, Timothy Lillicrap, and
                                                                           and Yi Ma. Learning a Diffusion Model Policy from
     Sergey Levine. “Deep reinforcement learning for
                                                                           Rewards via Q-Score Matching. 2024.
     robotic manipulation with asynchronous off-policy
                                                                    [14]   Lars Ankile, Zhenyu Jiang, Rocky Duan, Guanya Shi,
     updates”. In: 2017 IEEE International Conference on
                                                                           Pieter Abbeel, and Anusha Nagabandi. Residual Off-
     Robotics and Automation (ICRA). 2017, pp. 3389–3396.
                                                                           Policy RL for Finetuning Behavior Cloning Policies.
     DOI: 10.1109/ICRA.2017.7989385.
                                                                           2025. arXiv: 2509.19301 [cs.RO].
 [3] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and
                                                                    [15]   Kevin Black, Manuel Y Galliker, and Sergey Levine.
     Sergey Levine. Soft Actor-Critic: Off-Policy Maximum
                                                                           “Real-Time Execution of Action Chunking Flow Poli-
     Entropy Deep Reinforcement Learning with a Stochas-
                                                                           cies”. In: The Thirty-ninth Annual Conference on
     tic Actor. 2018. arXiv: 1801.01290 [cs.LG].
                                                                           Neural Information Processing Systems. 2025.
 [4] Henry Zhu, Abhishek Gupta, Aravind Rajeswaran,
                                                                    [16]   Kevin Black, Allen Z. Ren, Michael Equi, and Sergey
     Sergey Levine, and Vikash Kumar. Dexterous Manip-
                                                                           Levine. Training-Time Action Conditioning for Efficient
     ulation with Deep Reinforcement Learning: Efficient,
                                                                           Real-Time Chunking. 2025. arXiv: 2512 . 05964
     General, and Low-Cost. 2018. arXiv: 1810.06045
                                                                           [cs.RO].
     [cs.AI].
                                                                    [17]   Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou,
                                                                           Haoran Li, and Dongbin Zhao. ConRFT: A Reinforced
                                                                           Fine-tuning Method for VLA Models via Consistency
                                                                           Policy. 2025. arXiv: 2502.05450 [cs.RO].
[18] Perry Dong, Alec M. Lessing, Annie S. Chen, and          [25] Yunchao Ma, Yizhuang Zhou, Yunhuan Yang, Tiancai
     Chelsea Finn. Reinforcement Learning via Implicit             Wang, and Haoqiang Fan. Running VLAs at Real-time
     Imitation Guidance. 2025. arXiv: 2506 . 07505                 Speed. 2025. arXiv: 2510.26742 [cs.RO].
     [cs.LG].                                                 [26] Michael Matthews, Michael Beukman, Chris Lu, and
[19] Physical Intelligence, Ali Amin, Raichelle Aniceto,           Jakob Nicolaus Foerster. “Kinetix: Investigating the
     Ashwin Balakrishna, Kevin Black, Ken Conley, Grace            Training of General Agents through Open-Ended
     Connors, James Darpinian, Karan Dhabalia, Jared               Physics-Based Control Tasks”. In: The Thirteenth
     DiCarlo, Danny Driess, Michael Equi, Adnan Es-                International Conference on Learning Representations.
     mail, Yunhao Fang, Chelsea Finn, Catherine Glossop,           2025.
     Thomas Godden, Ivan Goryachev, Lachy Groom,              [27] NVIDIA, : Johan Bjorck, Fernando Castañeda, Nikita
     Hunter Hancock, Karol Hausman, Gashon Hussein,                Cherniadev, Xingye Da, Runyu Ding, Linxi "Jim" Fan,
     Brian Ichter, Szymon Jakubczak, Rowan Jen, Tim                Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang,
     Jones, Ben Katz, Liyiming Ke, Chandra Kuchi,                  Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia,
     Marinda Lamb, Devin LeBlanc, Sergey Levine, Adrian            Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin,
     Li-Bell, Yao Lu, Vishnu Mano, Mohith Mothukuri,               Guilin Liu, Edith Llontop, Loic Magne, Ajay Man-
     Suraj Nair, Karl Pertsch, Allen Z. Ren, Charvi Sharma,        dlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed,
     Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springen-         You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang,
     berg, Kyle Stachowicz, Will Stoeckle, Alex Swerdlow,          Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu,
     James Tanner, Marcel Torne, Quan Vuong, Anna                  Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang,
     Walling, Haohuan Wang, Blake Williams, Sukwon Yoo,            Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke
                                                 ∗
     Lili Yu, Ury Zhilinsky, and Zhiyuan Zhou. π0.6 : a VLA        Zhu. GR00T N1: An Open Foundation Model for
     That Learns From Experience. 2025. arXiv: 2511 .              Generalist Humanoid Robots. 2025. arXiv: 2503 .
     14759 [cs.LG].                                                14734 [cs.RO].
[20] Physical Intelligence, Kevin Black, Noah Brown, James    [28] Allen Z. Ren, Justin Lidard, Lars Lien Ankile, An-
     Darpinian, Karan Dhabalia, Danny Driess, Adnan                thony Simeonov, Pulkit Agrawal, Anirudha Majumdar,
     Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai,            Benjamin Burchfiel, Hongkai Dai, and Max Sim-
     Manuel Y. Galliker, Dibya Ghosh, Lachy Groom,                 chowitz. “Diffusion Policy Policy Optimization”. In:
     Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim            The Thirteenth International Conference on Learning
     Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine,             Representations. 2025.
     Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl       [29] Kohei Sendai, Maxime Alvarez, Tatsuya Matsushima,
     Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura               Yutaka Matsuo, and Yusuke Iwasawa. Leave No Obser-
     Smith, Jost Tobias Springenberg, Kyle Stachowicz,             vation Behind: Real-time Correction for VLA Action
     James Tanner, Quan Vuong, Homer Walke, Anna                   Chunks. 2025. arXiv: 2509.23224 [cs.RO].
     Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky.       [30] Gemini Robotics Team et al. Gemini Robotics 1.5:
     π0.5 : a Vision-Language-Action Model with Open-              Pushing the Frontier of Generalist Robots with Ad-
     World Generalization. 2025. arXiv: 2504 . 16054               vanced Embodied Reasoning, Thinking, and Motion
     [cs.LG].                                                      Transfer. 2025. arXiv: 2510.03342 [cs.RO].
[21] Alexander Khazatsky et al. DROID: A Large-Scale          [31] Andrew Wagenmaker, Mitsuhiko Nakamoto, Yunchu
     In-The-Wild Robot Manipulation Dataset. 2025. arXiv:          Zhang, Seohong Park, Waleed Yagoub, Anusha Naga-
     2403.12945 [cs.RO].                                           bandi, Abhishek Gupta, and Sergey Levine. “Steering
[22] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng                 Your Diffusion Policy with Latent Space Reinforcement
     Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and             Learning”. In: Conference on Robot Learning (2025).
     Ziwei Wang. VLA-RL: Towards Masterful and General        [32] Yantai Yang, Yuhao Wang, Zichen Wen, Luo Zhongwei,
     Robotic Manipulation with Scalable Reinforcement              Chang Zou, Zhipeng Zhang, Chuan Wen, and Linfeng
     Learning. 2025. arXiv: 2505.18719 [cs.RO].                    Zhang. “EfficientVLA: Training-Free Acceleration and
[23] Jianlan Luo, Zheyuan Hu, Charles Xu, You Liang Tan,           Compression for Vision-Language-Action Models”.
     Jacob Berg, Archit Sharma, Stefan Schaal, Chelsea             In: The Thirty-ninth Annual Conference on Neural
     Finn, Abhishek Gupta, and Sergey Levine. SERL:                Information Processing Systems. 2025.
     A Software Suite for Sample-Efficient Robotic Re-        [33] Kevin Black, Noah Brown, Danny Driess, Adnan
     inforcement Learning. 2025. arXiv: 2401 . 16013               Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai,
     [cs.RO].                                                      Lachy Groom, Karol Hausman, Brian Ichter, Szymon
[24] Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey               Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine,
     Levine. Precise and Dexterous Robotic Manipulation            Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl
     via Human-in-the-Loop Reinforcement Learning. 2025.           Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan
     arXiv: 2410.21845 [cs.RO].                                    Vuong, Anna Walling, Haohuan Wang, and Ury Zhilin-
                                                                   sky. π0 : A Vision-Language-Action Flow Model for
       General Robot Control. 2026. arXiv: 2410.24164            [47] Sungjae Park and Shubham Tulsiani. πR2 : Reactive
       [cs.LG].                                                       Real-time Flow Policies. 2026. arXiv: 2607.26055
[34]   Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo, Si              [cs.RO].
       Xu, Hao Lin, Hongzhi Zang, Xiang Li, Quanlu Zhang,        [48] Sarvesh Patil, Mitsuhiko Nakamoto, Manan Agarwal,
       Zhaofei Yu, Guoliang Fan, Tiejun Huang, Yu Wang,               Shashwat Saxena, Jesse Zhang, Giri Anantharaman,
       and Chao Yu. πRL : Online RL Fine-tuning for Flow-             Cleah Winston, Chaoyi Pan, Douglas Chen, Nai-Chieh
       based Vision-Language-Action Models. 2026. arXiv:              Huang, Zeynep Temel, Oliver Kroemer, Sergey Levine,
       2510.25889 [cs.LG].                                            Abhishek Gupta, Hongkai Dai, Paarth Shah, and Max
[35]   Perry Dong, Kuo-Han Hung, Tian Gao, Dorsa                      Simchowitz. OGPO: Sample Efficient Full-Finetuning
       Sadigh, and Chelsea Finn. EXPO-FT: Sample-                     of Generative Control Policies. 2026. arXiv: 2605.
       Efficient Reinforcement Learning Finetuning for Vision-        03065 [cs.LG].
       Language-Action Models. 2026. arXiv: 2605.25477           [49] Jiaming Tang, Yufei Sun, Yilong Zhao, Shang Yang,
       [cs.RO].                                                       Yujun Lin, Zhuoyang Zhang, James Hou, Yao Lu,
[36]   Perry Dong, Kuo-Han Hung, Alexander Swerdlow,                  Zhijian Liu, and Song Han. VLASH: Real-Time VLAs
       Dorsa Sadigh, and Chelsea Finn. TQL: Scaling Q-                via Future-State-Aware Asynchronous Inference. 2026.
       Functions with Transformers by Preventing Attention            arXiv: 2512.01031 [cs.RO].
       Collapse. 2026. arXiv: 2602.01439 [cs.LG].                [50] Wenli Xiao, Haotian Lin, Andy Peng, Haoru Xue,
[37]   Perry Dong, Yueru Jia, Chelsea Finn, and Dorsa Sadigh.         Tairan He, Zhengyi Luo, Yuqi Xie, Fengyuan Hu,
       Q-Learning With World Models. 2026. arXiv: 2608.               Linxi Fan, Guanya Shi, and Yuke Zhu. “Self-Improving
       17163 [cs.LG].                                                 Vision-Language-Action Models with Data Generation
[38]   Perry Dong, Qiyang Li, Dorsa Sadigh, and Chelsea               via Residual RL”. In: The Fourteenth International
       Finn. “EXPO: Stable Reinforcement Learning with                Conference on Learning Representations. 2026.
       Expressive Policies”. In: The Fourteenth International    [51] Charles Xu, Jost Tobias Springenberg, Michael Equi,
       Conference on Learning Representations. 2026.                  Ali Amin, Adnan Esmail, Sergey Levine, and Liyiming
[39]   Perry Dong, Ron Polonsky, Dorsa Sadigh, and Chelsea            Ke. RL Token: Bootstrapping Online RL with Vision-
       Finn. Do You Really Need to Pretrain Q-Functions for           Language-Action Models. 2026. arXiv: 2604.23073
       Online RL Fine-Tuning? 2026. arXiv: 2607.27203                 [cs.LG].
       [cs.LG].                                                  [52] Tonghe Zhang, Chao Yu, Sichang Su, and Yu Wang.
[40]   Perry Dong, Alexander Swerdlow, Dorsa Sadigh, and              ReinFlow: Fine-tuning Flow Matching Policy with
       Chelsea Finn. FASTER: Value-Guided Sampling for                Online Reinforcement Learning. 2026. arXiv: 2505.
       Fast RL. 2026. arXiv: 2604.19730 [cs.LG].                      22094 [cs.RO].
[41]   Perry Dong, Chongyi Zheng, Chelsea Finn, Dorsa
       Sadigh, and Benjamin Eysenbach. Value Flows. 2026.
       arXiv: 2510.07650 [cs.LG].
[42]   Hai Jiang, Yixian Zou, Binbin Liang, Boqian Liu,
       Fanman Meng, and Shuaicheng Liu. FutureRTC: Real-
       Time Robot Execution with Anticipatory-Conditioned
       Action Chunking. 2026. arXiv: 2607 . 24008
       [cs.RO].
[43]   Kun Lei, Huanyu Li, Dongjie Yu, Zhenyu Wei, Lingx-
       iao Guo, Zhennan Jiang, Ziyu Wang, Shiyu Liang, and
       Huazhe Xu. RL-100: Performant Robotic Manipulation
       with Real-World Reinforcement Learning. 2026. arXiv:
       2510.14830 [cs.RO].
[44]   Qiyang Li and Sergey Levine. “Q-Learning with
       Adjoint Matching”. In: The Fourteenth International
       Conference on Learning Representations. 2026.
[45]   Yuxiang Lu, Zhe Liu, Xianzhe Fan, Zhenya Yang,
       Jinghua Hou, Junyi Li, Kaixin Ding, and Hengshuang
       Zhao. “FASTER: Rethinking Real-Time Flow VLAs”.
       In: arXiv preprint arXiv:2603.19199 (2026).
[46]   Jiahui Niu, Kefan Gu, Yucheng Zhao, Shengwen Liang,
       Tiancai Wang, Xing Hu, Ying Wang, and Huawei Li.
       Realtime-VLA FLASH: Speculative Inference Frame-
       work for Diffusion-based VLAs. 2026. arXiv: 2605.
       13778 [cs.RO].
                          A PPENDIX                                   2) Learner Configuration: The critic, filter, and edit policy
A. Noise-level Filtering Studies                                   use the same overall architecture as in the real-world setting,
                                                                   including a REDQ ensemble of 10 networks with two
    To handle the high randomness of dynamic tasks, we
                                                                   networks subsampled for each target estimate, LayerNorm,
empirically find that a larger sampling number such as
                                                                   and hidden dimensions (256, 256, 256). For simulation, the
N = 32 is often required. However, setting a large N such
                                                                   visual encoder is replaced by an MLP state encoder with a 256-
as 32 introduces a substantial computational burden during
                                                                   dimensional output. Different from the real-world settings,
training. To address this issue, we incorporate the noise-level
                                                                   the base-policy update is not restricted to successful episodes,
filtering technique introduced in Equation (10) to filter action
                                                                   the BC loss Equation (7) is applied to all the rollout and
candidates during Bellman updates.
                                                                   demo data.
    To evaluate the effectiveness and efficiency of noise-
                                                                      3) State-Based Baselines:
level filtering, we compare using and not using noise-level
                                                                         a) DSRL (state): DSRL applies SAC in the flow policy’s
filtering and instead filters over the fully denoised actions.
                                                                   noise space over the frozen per-level base policy, with M =
As shown in the Figure 7, using noise filtering learns
                                                                   1.5, target entropy 0, no entropy term in the Bellman backup,
significantly more efficiently than not using it under the same
                                                                   and no demonstration data. We evaluate three settings: no
training compute, demonstrating that noise-level filtering can
                                                                   inference delay; delay d = 4 with real-time chunking, where
effectively improve training by enabling a large N without
                                                                   the in-flight prefix is inpainted into chunk positions [0 :
incurring the computational cost.
                                                                   4] and the window [4 : 8] is executed; and delay d = 4
B. Full Simulation Experiment Results                              with naive replanning, which uses the same stale observation
  Here, we provide detailed simulation experiment results,         without prefix conditioning. The third setting isolates the
including evaluations of all baselines. For each method, we        effect of prefix conditioning from the effect of acting on stale
conduct 100 trials in each environment and average the results     observations.
across four random seeds. As shown in Table II, Real-Time                b) RLPD (state): RLPD uses SAC and learns directly
EXPO-FT outperforms all baselines across the evaluated             from scratch, with 50% demonstration data in every batch
environments.                                                      and zero inference delay. The pretrained flow checkpoint
                                                                   is used only for observation preprocessing and reference
C. Detailed Simulation Task Settings                               evaluation and does not contribute to the learned policy.
   1) Environment and Base Policy: For simulation, we use          Critic hyperparameters are identical to those of Real-Time
the vector-state (symbolic) Kinetix benchmark, where no            EXPO-FT, so the two methods differ only in their actor
VLA is involved and the base policy is a pretrained state-         parameterization and use of the pretrained policy.
based flow-matching policy. We evaluate on 10 environ-
ments: car_launch, cartpole_thrust, catapult,                      D. Detailed Real-World Task Settings
catcher_v3, h17_unicycle, hard_lunar_lander,                          1) Task Setting Description: Here, we provide detailed
mjc_half_cheetah, trampoline, chain_lander,                        task settings for the four real-world tasks evaluated in our
and grasp_easy. We use four random seeds and a budget              experiments, including the task objectives, success detector
of 100k environment steps per run. The environment applies         implementation and definition, reward function, initial-state
Gaussian action noise with a standard deviation of 0.1,            randomization, camera configuration, and demonstration
matching the reference data generation and evaluation rollouts.    collection procedure.
Success is determined by the environment’s episode-solved             All four real-world tasks use the same single-arm
flag.                                                              DROID [21] setup with a 30 Hz control rate and two policy
   The base policy is the publicly released per-level behavior-    camera views, consisting of one exterior camera and one
cloned flow policy from the real-time-chunking [15] Kinetix        wrist-mounted camera. Each image is resized to 224 × 224.
benchmark [26]. It uses a channel dimension of 256, a channel      Rewards are sparse and binary: an automatic detector emits
hidden dimension of 512, a token hidden dimension of 64,           r = 1 on the step at which it declares success and terminates
four layers, an action-chunk length of H = 8, and five             the episode. A timeout terminates the episode with r = 0
flow-matching steps during training. The policy is not delay-      and is treated as a failure. Episodes are additionally capped
conditioned. At rollout and during the critic backup, we           at a task-specific horizon.
sample the policy using 10 Euler denoising steps.                     2) Success Detectors: All success detectors operate on
   Online fine-tuning of the base policy uses AdamW                the robot’s own observation stream and therefore require
with a learning rate of 3 × 10−4 , weight decay of 10−2 ,          no external instrumentation. Dynamic Picking is detected
gradient-norm clipping of 10, and a 1000-step warmup.              proprioceptively: a successful lift is declared when the end-
We use a prefix-conditioned flow-matching objective with           effector height exceeds 0.30 while the gripper is closed
d ∼ Unif{0, . . . , 4}, where the prefix length is resampled       beyond a mid-aperture threshold for 5 consecutive steps.
independently for each training example. Unlike the real-          Soccer Kicking and Ball Balancing use analogous wrist-view-
world setting, where the online prefix length is fixed to the      based detectors, with Ball Balancing additionally requiring
deployment delay, the simulation setting resamples the prefix      the ball to remain within a specified center tolerance for 10
length during training.                                            consecutive frames. Object Passing uses a wrist-view-based
Fig. 7: Comparison of noise-level filtering. We compare Real-Time EXPO-FT with and without noise-level filtering, where
the latter uses only Q-level filtering during the Bellman backup. The x-axis shows training compute, allowing us to compare
the efficiency of the two approaches.




       Grasp Easy                       Catapult            Cartpole Thrust           Hard Lunar Lander         MJC Half Cheetah




       H17 Unicycle                 Chain Lander               Catcher v3                Trampoline               Car Launch

                              Fig. 8: 10 Kinetix simulation tasks [26] evaluated in our experiments.

TABLE II: Full simulation results on the Kinetix benchmark: success rate (%). RL results average four random seeds × 100
evaluation episodes; BC deploys the pretrained policy without fine-tuning, and RTC adds real-time chunking on top of it (512
episodes each). Delay-4 methods replan every 4 steps under a 4-step inference delay; RLPD supports only zero delay. Bold
marks every RL method within 0.95× the best RL result on that task (BC and RTC are excluded from the comparison).
                        Delay = 0                                                Delay = 4
Task
                       BC       RLPD       BC      RTC     DSRL    DSRL w/ RTC    EXPO-FT      EXPO-FT w/ RTC     Real-Time EXPO-FT
Car Launch             94%      97%        51%     70%     76%        79%             44%             64%               98%
Cartpole Thrust       100%      57%        37%     92%     49%        85%             99%             96%               98%
Catapult               62%      83%        31%     42%     36%        49%             18%             47%               93%
Catcher                97%      90%        23%     90%     40%        71%             90%             85%               97%
Unicycle               97%      90%        58%     74%     48%        86%             48%             87%               99%
Hard Lunar Lander     95%       70%        57%     87%     75%        79%             95%             90%               94%
Half-Cheetah           88%      93%        72%     75%     86%        85%             75%             79%               98%
Trampoline            84%       47%        68%     85%     43%        42%             93%             83%               94%
Chain Lander           95%      90%        94%     94%     92%        96%             90%             94%               92%
Grasp                 95%       97%        61%     91%     72%        89%             97%             92%               99%
Average               90.7%     81.4%     55.2%    80.0%   61.7%      76.1%           74.9%           81.7%            96.2%



detector to determine whether the robot has successfully             control steps.
grasped the object: a success is declared when the gripper
is closed and the object remains detected for 5 consecutive            3) Additional Critic Inputs: For two tasks, a small number
                                                                     of quantities already measured by the success detector are
written into unused slots of the proprioceptive state vector.       Bellman target and rollout-time action selection, samples two
These quantities are available to the critic, the noise-Q filter,   networks uniformly from the target ensemble and takes their
and the edit policy. The base VLA’s own state input remains         minimum. The target ensemble follows the online ensemble
unchanged, so the supervised checkpoint and normalization           using Polyak averaging with τQ = 5 × 10−3 . For Kick and
statistics are unaffected.                                          Balance, we additionally train the critic on reward windows
   Ball Balancing exposes the plate center, ball position, and      containing terminal transitions, whose targets consist only of
ball velocity. Soccer Kicking exposes the keeper’s position         the observed reward.
and velocity.                                                            b) Critic visual encoder: The critic uses a pre-activation
   For Ball Balancing, we additionally remove the vertical (z)      ResNetV2 with basic, non-bottleneck residual blocks, stage
proprioceptive dimension from the critic input because it drifts    depths (3, 4, 6, 3), GroupNorm with four groups, and 64
monotonically with episode time and may allow the value             base filters that double at each stage to 512. At 224 × 224
function to exploit episode-time information. Both DSRL and         resolution, the stem consists of a stride-2 7 × 7 convolution
RLPD receive the same privileged state dimensions in their          followed by max pooling. A single encoder consumes the
critics.                                                            camera views as a channel-stacked tensor, using six channels
   4) Observation Layout: Three tasks use one exterior view         for two views and nine channels for Balance’s three-frame
and one wrist view. The critic encoder consumes these views         stack. The resulting representation is projected to a 512-
as a six-channel tensor. Ball Balancing instead uses a three-       dimensional image embedding using a Dense+LayerNorm
frame stack of the exterior view at t, t − k, and t − 2k, while     head. Proprioception is embedded into 64 dimensions and
dropping the wrist view from the policy input. Consequently,        concatenated with the image embedding and flattened action
the critic encoder consumes nine channels, and the VLA              chunk for Q-value prediction.
receives the corresponding three-image configuration.                    c) Edit policy: The edit policy is a tanh-squashed
   5) Task Full Execution Strips: We visualize the full             Gaussian over the flattened execution window, with dimension
execution trajectories of the evaluated tasks. As shown in          D = C × 7. For C = 8, this gives D = 56. The policy is
Figure 9, each strip illustrates the temporal progression of        conditioned on the critic’s image embedding, proprioceptive
the task from initiation to completion, providing a qualitative     embedding, and the base action chunk being corrected. It
view of the robot’s behavior throughout the entire execution.       reuses the critic’s image encoder and contains three hidden
   6) Task Initial-State Randomization Space: We visualize          layers of width 256. Its output lies in [−1, 1]D and is
the task initial-state randomization space to illustrate the        multiplied by a task-specific edit scale before being added
range of initial object positions. As shown in Figure 10,           to the base action chunk. For Dynamic Pick, the rotational
the randomized space is highlighted by the orange boxes,            components of the edit are masked to zero, so the edit acts
capturing the randomization applied to both the objects and         only on translation and gripper dimensions.
the robot.                                                               d) Action selection: At each replan boundary, the base
                                                                    policy draws N = 32 stochastic action chunks using 10 Euler
E. Detailed Training Settings                                       denoising steps. Because the VLM prefix is shared across
   1) Base Policy Initialization: We instantiate Real-Time          noise samples, it is computed only once. Each base chunk
EXPO-FT with π0.5 [20] as the base policy. The model uses a         receives one sampled edit, producing 64 candidates in total:
LoRA [8] configuration with a gemma_2b_lora language                32 base candidates and 32 edited candidates. The executed
backbone and a gemma_300m_lora action expert. The                   chunk is selected deterministically using the arg max of the
padded action dimension is 32, the action horizon is H = 16,        minimum-over-two-subsampled target Q value. No softmax
and the output action dimension is 7. Proprioceptive state is       is applied over candidates.
provided to the VLA in Cartesian form, and input images                  e) Noise-Q backup filter: Denoising 32 candidates
are resized to 224 × 224.                                           during every Bellman backup would substantially increase
   The initialization is a task-specific prefix-conditioned real-   computational cost. We therefore pre-filter candidates in noise
time-chunking LoRA supervised fine-tuning of π0.5 using             space. A filter critic Qf (s′ , ϵ) scores 32 raw Gaussian seeds in
the corresponding task demonstrations and normalization             the padded model action space (H × 32). The highest-scoring
statistics. During supervised training, the per-example prefix      seed is denoised using arg max with a sampling temperature
length is sampled as d ∼ Unif{0, . . . , dmax }. The first d        of zero, and one edit candidate is sampled from the resulting
chunk positions are provided with clean ground-truth actions        action chunk. The outer target-Q maximization then considers
at flow time τ = 1, and the flow-matching loss is applied only      one base candidate and one edited candidate.
to the remaining H − d positions. This exposes the model               Qf is a two-network ensemble trained at every critic step
to both the boot regime (d = 0) and the delayed inpainting          using MSE regression onto the outer target critic’s Q value for
regime during supervised training. The image encoder is             the denoised survivor, with the target stop-gradient applied.
trainable during this stage.                                        Because the regression target is supervised, Qf does not
   2) Model Structure and Learned Components:                       require a target network. The filter additionally conditions on
      a) Value function: The critic is a REDQ-style [7]             the delayed observation used by the base policy, consisting
ensemble of 10 Q-networks with LayerNorm and three hidden           of the image embedding and proprioception. Rollout action
layers of width 256. Every Q evaluation, including both the         selection is unaffected by this filter.
Fig. 9: Full execution strips for the evaluated tasks. Each strip shows the temporal progression of a complete task execution,
from initialization to successful completion.




Fig. 10: Initial-state randomization spaces for the real-world tasks. The orange boxes indicate the regions within which object
and robot initial states are randomized.

                      TABLE III: Shared optimization hyperparameters used across all real-world experiments.
Hyperparameter                                                                                                 Value
Optimizer (critic, filter, edit policy, temperature)                                                     Adam, 3 × 10−4
Optimizer (base VLA)                                                                                AdamW, 2.5 × 10−5 , clip 1.0
Critic target update τQ                                                                                     5 × 10−3
Base-policy Polyak copy τπ                                                                                    10−3
Initial temperature α0                                                                                         0.01
Target entropy                                                                                          −D/2, D = C × 7
Critic minibatch size                                                                                           64
Update-to-data ratio                                                                                            20
Q-ensemble size / subsample                                                                                   10/2
Filter-critic ensemble size                                                                                      2
Action-chunk horizon H                                                                                          16
Base candidates N / edit candidates                                                                           32/32
Backup noise seeds / survivors / edits                                                                       32/1/1
Denoising steps                                                                                                 10
Image / state embedding dimensions                                                                           512/64
Hidden layers                                                                                            (256, 256, 256)



     f) Base-policy fine-tuning: The base VLA is fine-tuned       an episode and d equal to the deployment delay thereafter.
using prefix-conditioned flow-matching behavior cloning on        Unlike supervised initialization, the online prefix length is
successful episodes, including demonstrations and successful      therefore not resampled.
online episodes. Exactly one base-policy update is performed         The trainable parameters include the LoRA adapters in the
per update call. The prefix length is deterministic during        language model as well as all parameters outside the frozen
online training: d = 0 for transitions in the first chunk of      non-LoRA language-model weights, including the SigLIP
TABLE IV: Task-specific hyperparameters for Real-Time EXPO-FT. K denotes the number of collected transitions per
update call. “Prior data” indicates whether demonstrations are sampled as a fixed fraction of each critic batch or seeded into
the online replay buffer. Environment steps denote the total budget of the reported run.
Task                       Edit scale          Replan C            Delay d           K                Prior data             Env. steps
Dynamic Picking              0.1                   8                   3            25             Seeded in buffer           ∼ 18k
Soccer Kicking               0.05                  8                   5            20            50% of each batch           ∼ 18k
Ball Balancing               0.1                   8                   5            30             Seeded in buffer           ∼ 18k
Object Passing               0.1                   8                   5            30             Seeded in buffer           ∼ 5k



vision tower and projection layers. The frozen language-               minibatches, followed by exactly one base-policy step, one
model parameters are maintained in bfloat16. The VLA is                edit-policy step, and one temperature step. Thus, the base-
optimized using the AdamW configuration of the underlying              policy-to-critic gradient-step ratio is 1 : 20 rather than 1 : 1.
implementation [20], with β1 = 0.9, β2 = 0.95, ϵ = 10−8 ,                 Update calls are accumulated at a rate of one per K
weight decay 10−10 , and gradient-norm clipping at 1.0. We             collected transitions and flushed at episode boundaries.
use a constant learning rate of 2.5 × 10−5 and no EMA. A               Training begins only after 10 episodes have been completed.
Polyak copy of the base-policy parameters is maintained with              5) Evaluation Protocol: Each method is evaluated from its
τπ = 10−3 but is not used by the current Bellman backup,               final checkpoint unless otherwise specified, under the same
which samples next actions from the live base policy.                  latency condition used during training.
      g) Entropy and temperature: The learnable temperature
is initialized at α0 = 0.01 and optimized with Adam at                 F. Baseline Implementations
3 × 10−4 using a target entropy of −D/2, where D = C × 7
is the edit-policy dimension. Entropy affects only the edit-                 a) RLPD [9]: We follow the SERL [23] setup for
policy objective and does not appear in the Bellman backup.            RLPD [9], using the same π0.5 -style observation pipeline as
      h) Image augmentation: Both current and next observa-            our real-robot stack. No VLA is used in the policy. The policy
tions are augmented independently. For each view, we apply a           is a tanh-Gaussian distribution over a single 7-dimensional
95% random crop followed by resizing to 224×224, a random              action and is queried at every control step. It runs with zero
rotation in [−5◦ , 5◦ ], and color jitter with brightness, contrast,   inference delay, so its Bellman backup uses γ per environment
and saturation changes of ±0.1. The same augmentation                  step rather than γ C .
procedure is applied to critic, filter, edit-policy, and base-            We use hidden dimensions (256, 256, 256), Adam with
policy inputs.                                                         a learning rate of 3 × 10−4 , γ = 0.99 (0.997 for Kick),
   3) Latency Model: We study two ways of realizing                    minibatch size 256, UTD ratio 4, initial temperature 0.1, target
inference latency at a 30 Hz control rate. In the wall-clock           entropy −7/2 = −3.5, and no entropy term in the Bellman
condition, we set d = 0 and add 100 ms of real sleep to every          backup. The critic uses the same REDQ-style ensemble as
sample actions call for soccer kicking, ball balancing, and            Real-Time EXPO-FT, with 10 networks and two subsampled
object passing, approximating the compute time of running              for each target estimate, together with LayerNorm, a 512-
the π0.5 model on a typical edge GPU. For dynamic picking,             dimensional image latent, and a 64-dimensional state latent.
we do not inject additional wall-clock latency, as the task is         We use the same augmentation procedure, but a smaller
highly dynamic and even modest additional latency causes               ResNetV2 visual backbone with stage depths (1, 1, 1, 1).
the baseline methods to fail almost entirely, making the                  Demonstrations constitute 50% of every critic batch.
comparison less informative. In the chunk-delay condition,             Training runs in an asynchronous learner thread that is not
the policy observes a d-step-old observation, the d actions            rate-limited by the environment. We report the measured
currently in flight are inpainted into chunk positions [0, d)          number of optimizer steps per environment step for each run
as a clean prefix, and the window [d, d + C) is executed.              rather than assuming a fixed ratio.
We use d = 3 for dynamic picking and d = 5 for the other                     b) DSRL [31], DSRL w/ RTC: DSRL uses the frozen
tasks, corresponding to approximately 100 ms and 167 ms,               π0.5 policy loaded from the same prefix-conditioned super-
respectively, and matching the inference-time settings used            vised checkpoint used to initialize Real-Time EXPO-FT.
in the wall-clock condition.                                           SAC operates in noise space: the actor outputs a single 32-
   4) Optimization Hyperparameters: Table III lists the                dimensional noise vector corresponding to the padded model
hyperparameters shared across all real-world experiments,              action dimension, squashed as M tanh(u) with M = 1.0 and
while Table IV lists the task-specific settings.                       tiled across the 16-step action horizon.
   All learned components other than the base VLA, including              The critic is parameterized as Q(enc(s), ϵ) and uses the
the Q ensemble, filter critic, edit policy, and temperature, use       same ResNetV2 encoder as Real-Time EXPO-FT, with stage
Adam with a learning rate of 3 × 10−4 . The base VLA                   depths (3, 4, 6, 3), width 64, input resolution 224 × 224, a
uses the AdamW configuration described above. Each update              512-dimensional image latent, a 64-dimensional state latent,
call samples batch size × UTD transitions and performs                 hidden dimensions (256, 256, 256), LayerNorm, and a REDQ
the specified number of critic gradient steps on disjoint              ensemble of 10 networks with two subsampled for the target.
State information is included in the critic, and the same image
augmentation is applied.
    The actor learning rate is 10−4 , while the critic and
temperature use 3 × 10−4 . We use γ = 0.99 (0.997 for
Kick), τQ = 5 × 10−3 , minibatch size 64, UTD ratio 20,
initial temperature 0.01, target entropy 0, and no entropy
term in the Bellman backup.
    DSRL executes C = 8 steps per replan. Under nonzero
delay, it uses the same real-time-chunking prefix inpainting
as Real-Time EXPO-FT, with SAC noise applied only to
the postfix. The Bellman backup requires no modification
because DSRL operates entirely in noise space. DSRL is
trained purely online without demonstration data because
demonstrations do not contain the corresponding noise labels.
For DSRL w/ RTC, we use the same delay as Real-Time
EXPO-FT and same optimization parameters as DSRL.
       c) EXPO-FT [35], EXPO-FT w/ RTC: EXPO-FT uses
the same learner architecture, network sizes, candidate counts,
filter, optimizer settings, and prior-data configuration as Real-
Time EXPO-FT. The only difference is that EXPO-FT is
delay-unaware: it is trained and evaluated with d = 0 while
incurring 100 ms of real inference latency. This setting isolates
the contribution of delay-aware chunking from the underlying
EXPO optimization. For EXPO-FT with RTC, we use the
same delay and optimization parameters as Real-Time EXPO-
FT.
