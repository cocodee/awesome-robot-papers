# LDA-1B: Scaling Latent Dynamics Action Model via Universal Embodied Data Ingestion

Source: https://arxiv.org/pdf/2602.12215

                                            LDA-1B: Scaling Latent Dynamics Action Model
                                               via Universal Embodied Data Ingestion
                                           Jiangran Lyu∗1,2 , Kai Liu∗2,3,4 , Xuheng Zhang∗1,2 , Haoran Liao2,6 , Yusen Feng1,2 , Wenxuan Zhu1 , Tingrui Shen1 ,
                                         Jiayi Chen1,2 , Jiazhao Zhang1,2 , Yifei Dong1 , Wenbo Cui2,3,4 , Senmao Qi2 , Shuo Wang2 , Yixin Zheng2,3,4 , Mi Yan1,2 ,
                                         Xuesong Shi2 , Haoran Li3 , Dongbin Zhao3 , Ming-Yu Liu7 , Zhizheng Zhang2,† , Li Yi5,† , Yizhou Wang1,† , He Wang1,2,†
                                                       1                       2            3           4          5                             6                                7
                                                           Peking University       Galbot       CASIA       BAAI       Tsinghua University           Sun Yat-sen University           NVIDIA
                                                                                                                        ∗                             †
                                                                    Code & Data: https://pku-epic.github.io/LDA             Equal contribution            Corresponding authors
arXiv:2602.12215v1 [cs.RO] 12 Feb 2026




                                         Fig. 1: We introduce LDA-1B, a 1.6 B-parameter robot foundation model scaled on over 30k hours of heterogeneous embodied
                                         data. LDA-1B unifies policy, dynamics, and visual forecasting in a structured DINO [46] latent space, allowing different data
                                         sources to play complementary roles. Beyond high-quality data alone, noisy data and actionless videos also provide valuable
                                         visual and physical priors for dynamics learning. This universal data ingestion paradigm enables stable scaling with data and
                                         model size, significantly outperforming strong baselines such as π0.5 [23] across diverse manipulation tasks.

                                            Abstract—Recent robot foundation models largely rely on                                              I. I NTRODUCTION
                                         large-scale behavior cloning, which imitates expert actions but
                                         discards transferable dynamics knowledge embedded in hetero-
                                                                                                                          Inspired by the success of Large Language Models (LLMs)
                                         geneous embodied data. While the Unified World Model (UWM)                    and Vision-Language Models (VLMs), the robotics commu-
                                         formulation has the potential to leverage such diverse data,                  nity has increasingly pursued general-purpose robot founda-
                                         existing instantiations struggle to scale to foundation-level due             tion models through large-scale pretraining [5, 41]. Most exist-
                                         to coarse data usage and fragmented datasets. We introduce                    ing approaches center on scaling behavior cloning (BC), which
                                         LDA-1B, a robot foundation model that scales through universal
                                         embodied data ingestion by jointly learning dynamics, policy,
                                                                                                                       imitates expert actions but fundamentally restricts learning
                                         and visual forecasting, assigning distinct roles to data of varying           to high-quality demonstrations. Consequently, a large portion
                                         quality. To support this regime at scale, we assemble and                     of heterogeneous embodied data [42] is discarded or only
                                         standardize EI-30k, an embodied interaction dataset comprising                weakly utilized, despite containing rich physical interaction
                                         over 30k hours of human and robot trajectories in a unified                   dynamics [26].
                                         format. Scalable dynamics learning over such heterogeneous
                                         data is enabled by prediction in a structured DINO latent
                                                                                                                          Unified World Model (UWM) formulation [30, 60] provides
                                         space, which avoids redundant pixel-space appearance modeling.                an alternative by jointly optimizes dynamics, policy, and
                                         Complementing this representation, LDA-1B employs a multi-                    video generation within a single model, which can leverages
                                         modal diffusion transformer to handle asynchronous vision and                 not only expert data. Despite the potential value, existing
                                         action streams, enabling stable training at the 1B-parameter                  UWM instantiations remain far from scaling to foundation-
                                         scale. Experiments in simulation and the real world show LDA-
                                         1B outperforms prior methods (e.g., π0.5 ) by up to 21%, 48%,
                                                                                                                       level. A major limitation lies in coarse data usage: hetero-
                                         and 23% on contact-rich, dexterous, and long-horizon tasks,                   geneous embodied data are often treated uniformly, without
                                         respectively. Notably, LDA-1B enables data-efficient fine-tuning,             differentiating their roles by quality or supervision, which
                                         gaining 10% by leveraging 30% low-quality trajectories typically              underutilizes transferable dynamics knowledge. In addition,
                                         harmful and discarded.                                                        the community lacks ready-to-use large-scale datasets that
unify varying-quality data with consistent formats and aligned       Model               Data Src. #Data Action Quality     Train.    Param.
action representations. Furthermore, UWM represent future            π0.5 [23]            Tele.   10k+       High            BC        3B
state in pixel space, entangling dynamics learning with redun-       RDT [32]             Tele.   <10k       High            BC         1B
                                                                     GraspVLA [14]        Sim.    20k+       High            BC        2B
dant appearance modeling. Subtle variations in illumination,         InternVLA-M1 [11]    Sim.    <10k       High            BC         3B
texture, background clutter, or camera viewpoint can dominate        Being-H0 [35]        Hum.    <10k       Mixed        Aln. + BC    14B
the training objective, making large-scale training inefficient      InternVLA-A1 [9]     Het.    10k+       High         VF + BC      3B
                                                                     GR00T-N1.6 [40]      Het.    <10k       Mixed        LA + BC       1B
and hindering the learning of interaction-relevant dynamics.         UniVLA [7]           Het.    <10k       Mixed        LA + BC       7B
   To overcome these limitations, we introduce LDA-1B, a
                                                                     LDA-1B                Het.    30k+      Mixed        UWM[60]      1B
robot foundation model that scales via universal embodied
data ingestion. In this framework, heterogeneous data play          TABLE I: Comparison of Representative Robot Founda-
distinct yet complementary roles: actionless human videos           tion Models. This table compares the proposed LDA with
supervise visual forecasting [38, 37, 25], lower-quality trajec-    recent robot foundation models in terms of data source,
tories primarily inform dynamics learning, and high-quality         data quantity, action quality, training paradigm, and the
trajectories support both policy and dynamics. To realize           number of trainable model parameters (excluding frozen
this approach at scale, we assemble EI-30k, a large-scale           components). Data source abbreviations are as follows:
embodied interaction dataset with over 30k hours of human           Tele.=teleoperation, Sim.=simulation, Hum.=human demon-
and robot trajectories across real and simulated environments,      stration, and Het.=heterogeneous data. Training paradigm ab-
standardized in format and aligned in action representation.        breviations include: BC=behavior cloning, VF=visual fore-
Scalable learning on such diverse data is facilitated by a          sight, Aln.=alignment, LA=latent action modeling, and
structured DINO latent space [46, 59, 22], which reduces re-        UWM=unified world model. Only embodied interaction data
dundant appearance modeling [38, 25], and a multi-modal dif-        are considered, excluding internet-scale VQA data.
fusion transformer that aligns asynchronous visual and action
prediction. By combining this ingestion strategy, dataset, latent
representation, and model architecture, LDA-1B achieves sta-
ble training at the 1B-parameter scale while maximizing data        π0 [4], RDT [32], and InternVLA [11]rely heavily on high-
utilization.                                                        quality teleoperation or simulation data, which fundamentally
   We evaluate LDA-1B on challenging RoboCasa-GR1                   constrains their scalability. Hybrid methods such as Being-
benchmark and a diverse set of real-world tasks involving both      H0 [35] and UniVLA [7] attempt to incorporate heterogeneous
grippers and high-DoF dexterous hands [56]. LDA-1B consis-          data with mixed quality; however, they largely depend on
tently outperforms π0.5 , achieving 21% gains on contact-rich       action alignment or auxiliary pretrained latent action models,
manipulation, benefiting from improved dynamics understand-         limiting the effective data scale to around 6k hour embodied
ing and 48% gains on dexterous manipulation, benefiting from        data. In contrast, LDA-1B breaks this ceiling by adopting a
effective utilization of human data. Moreover, under a mixed-       unified world model formulation, enabling efficient ingestion
quality fine-tuning setting, LDA-1B improves data efficiency        of up to 30k hours of mixed-quality embodied data.
by 10% through leveraging low-quality trajectories that are         Unified Video Action Models. Recent works have explored
detrimental to baseline methods. These results highlight uni-       joint modeling dynamics and policy for embodied decision
versal embodied data ingestion and unified latent dynamics          making. Methods such as DyWA [36], FLARE [58], and the
learning as a scalable alternative to behavior-cloning-centric      WorldVLA series [10, 24] demonstrate that co-training next-
robot pretraining. In summary, our contributions are threefold:     state prediction and policy learning can improve generalization
   • We propose LDA-1B, a scalable robot foundation model
                                                                    in interactive environments. To enrich dynamics modeling,
      that learns generalizable interaction dynamics through        UWM [60] and UVA [30] further propose optimizing multiple
      unified latent dynamics pretraining.                          objectives jointly, including video generation, forward and
   • We construct EI-30k, a large-scale embodied interac-
                                                                    inverse dynamics, and action prediction. Concurrent with our
      tion dataset covering diverse embodiments, environments,      work, Motus [3] adopt UWM paradigm and integrate priors
      data qualities, with aligned end effector coordinate sys-     from pretrained VLM and video generation models. Despite
      tem.                                                          their promising results, these approaches typically operate
   • We demonstrate that LDA-1B achieves superior gen-
                                                                    directly in pixel space and do not explicitly consider the roles
      eralization and robustness across a wide range of set-        of data quality, scale, or heterogeneity during training, which
      tings, including simulation and real-world environments,      limits their ability to fully exploit large-scale, mixed-quality
      contact-rich manipulation, dexterous manipulation, and        interaction data for robust dynamics learning.
      long-horizon manipulation.                                    Large-Scale Embodied Interaction Datasets. The progress
                                                                    in embodied ai relys on large-scale embodied datasets. Many
                     II. R ELATED W ORK                             widely used datasets are collected via teleoperation on real
Robot Foundation Models. Recent robot foundation mod-               robots [4, 23, 27, 31] or generated in simulation [14, 11], pro-
els predominantly adopt the Behavior Cloning paradigm. As           viding high-quality action-labeled trajectories. Beyond robot-
summarized in Table I, representative approachesincluding           collected data, recent works explore human-centric embod-
                                                                                                                                                                                MM-DiT Block
                                                                                                             Action Chunk                       DINO Future
                                                                                                                                                                         FFN                              FFN
                                                                  Conditioning Input
                     Obs
                                                 VLM                                                                                                                     +                                 +
                 Language                                            VLM Tokens

                 Diffusion                   Sinusoidal                                                                                                             Cross      KV      VLM        KV       Cross
                Timestep t                     Encoder
                                                                          𝑓*                                                                                      Attention           Tokens             Attention


                    Task
                                                                                                                 Multi-Modal
                                                     Task Embeddings                                                                                                LayerNorm                          LayerNorm
                 Selection                                                              +                   Diffusion Transformer
                                                                                                                                                                          +                               +
       Forward Dynamics         Inverse Dynamics                 Policy        Visual Planning
                                                                                                       OR                              OR
                                                                                                 register
                       𝒐)                      𝒂             𝒂                    𝒐)
                                                                                                                                register                                Multi-Modal Self-Attention
                                                                                                       Liner Projection                     Liner Projection
                                                                                                                                                                  QKV                                           QKV
           𝒑(𝒐! |𝒐, 𝒂, 𝒍)           𝒑(𝒂|𝒐, 𝒐! , 𝒍)            𝒑(𝒂|𝒐, 𝒍)            𝒑(𝒐! |𝒐, 𝒍)                              𝑻    Time       𝑻
                                                                                                                                                                   AdaLN
                                                                                                                                                                   AdaLN            Task & Time            AdaLN
                                                                                                                                                                                     Embedding

       𝒐                    𝒂   𝒐                     𝒐)     𝒐                    𝒐

                                                                                                     noise
                                                                                                                   dense/sparse sampling
                                                                                                                                            Current DINO+ noise
                                                                                                                                                                                        xN

Fig. 2: Architecture of LDA. LDA jointly denoises action chunks and future visual latent under multiple co-training objectives,
including policy learning, forward dynamics, inverse dynamics, and visual forecasting. Conditioned on VLM tokens, diffusion
timesteps, and task embeddings, the model adopts a multimodal diffusion transformer architecture, where action and visual
experts are decoupled and interact through a shared self-attention layer.


ied datasets, such as egocentric recordings with hand ac-                                                                   observations conditioned on ot . We further extend this formu-
tions [53, 35]. While these datasets significantly expand data                                                              lation by introducing language ℓ conditioning through a VLM,
diversity, many are either not publicly released or provide                                                                 enabling instruction-guided action and observation prediction.
limited action supervision, making them difficult to directly
integrate with robot learning pipelines. More broadly, existing                                                             B. Universal Data Ingestion via Multi-task Co-training
embodied datasets are highly fragmented: some are closed-                                                                      We adopt a universal data ingestion regime to jointly train
source, others are open but vary substantially in data formats,                                                             the unified objectives described above, allowing heterogeneous
sensor configurations, action representations, and annotation                                                               embodied data to contribute according to their supervision
quality. This lack of standardization poses a major obstacle to                                                             quality. Specifically, high-quality robot and human demon-
large-scale data aggregation and unified training. In contrast,                                                             strations are co-trained with all objectives, supporting both
our work introduces EI-30k, a large-scale embodied interac-                                                                 action policy learning and dynamics modeling. Lower-quality
tion dataset that unifies diverse data sourcesincluding robot                                                               trajectories, which may contain suboptimal or noisy actions,
and human trajectories from both real-world and simulated                                                                   are used exclusively for dynamics and visual forecasting,
environmentsunder consistent data formats and aligned action                                                                where accurate action optimality is not required. In addition,
representations.                                                                                                            we leverage large-scale human manipulation videos without
            III. L ATENT DYNAMICS ACTION M ODEL                                                                             action annotations to train the visual forecasting objective,
                                                                                                                            providing supervision for instruction-conditioned future state
A. Preliminary: Unified World Models
                                                                                                                            prediction. This role-aware data usage prevents overfitting
   Given the current observation ot (typically an RGB image),                                                               to expert-only behaviors and enables scalable learning of
UWM [60] jointly models multiple conditional distributions                                                                  transferable dynamics and action representations.
over future observations ot+1:t+k and action chunk at+1:t+k ,                                                                  To implement differentiated objectives within a single dif-
enabling unified learning of:                                                                                               fusion model, we introduce four learnable task embeddings
   1) Policy: p(at+1:t+k | ot )                                                                                             and two learnable register tokens. Each task embedding
   2) Forward Dynamics: p(ot+1:t+k | ot , at+1:t+k )                                                                        corresponds to a specific training objective (policy, forward
   3) Inverse Dynamics: p(at+1:t+k | ot:t+k )                                                                               dynamics, inverse dynamics, or visual forecasting) and is
   4) Visual Planning: p(ot+1:t+k | ot )                                                                                    added to the diffusion timestep embedding ft to condition the
Concretely, UWM [60] instantiates this framework using a                                                                    denoising process. The learnable register tokensone for action
joint diffusion model that predicts noise for both actions and                                                              and one for visual stateserve as placeholders for modalities
future observations:                                                                                                        that are absent in a given task. For example, during policy
                                                                                                                            training, the model receives noisy action tokens along with
               (ϵθa , ϵθo ) = sθ o, ata , o′to , ta , to′ ,
                                                         
                                                                                                                            a visual register token representing the unobserved future
where ta and to are independently sampled diffusion timesteps                                                               state; in contrast, visual forecasting uses noisy future visual
for actions and observations, and ãta , õto denote their corre-                                                           tokens with an action register token. This design enables a
sponding noisy inputs. The model is trained with a standard                                                                 unified architecture to flexibly support different inputoutput
DDPM [20] objective, jointly denoising future actions and                                                                   structures without modifying the network topology. Overall,
the model predicts a denoising vector field vaθ under different    conditioning signals are injected into each Transformer block
task conditions and is trained using a flow-matching objective:    via adaptive layer normalization (AdaLN [43]).
                                                            2
                                                                      Actions are organized as fixed-length chunks and corrupted
   θ
  laction = E(ot:t+k ,at+1:t+k ,ℓ)∼D vaθ − (ϵa − at+1:t+k ) 2 ,    with Gaussian noise. Future visual features (DINO [46] fu-
                   τa ∼U (0,Tτ )
                   ϵa ∼N (0,I)
                                                                   tures) are noised in parallel. Both modalities are projected
     θ                                                      2      into token embeddings through modality-specific linear layers
    lobs = E(ot:t+k ,at+1:t+k ,ℓ)∼D voθ − (ϵo − ot+1:t+k ) 2 ,     and processed jointly by MM-DiT. Each MM-DiT block
                  τo ∼U (0,Tτ )
                  ϵo ∼N (0,I)                                      applies multi-modal self-attention over concatenated action
       θ   θ          θ
      l = laction + lobs  .                                        and visual tokens, enabling cross-modal interaction. Modality-
                                                           (1)     specific QKV projections and FFNs are retained to preserve
   During training, action and visual losses are selectively       inductive biases, while attention is shared across modalities.
activated according to the task specification, allowing het-       Language tokens are incorporated via cross-attention to pro-
erogeneous data to contribute under appropriate supervision.       vide high-level semantic guidance. Finally, modality-specific
At inference time, the same model can be flexibly invoked          output heads predict denoised action sequences and future
for different objectives by specifying the task embedding and      visual features.
corresponding inputs.
                                                                   E. Pre-training and Post-training
C. Representation of Predictive Targets                            Pre-training Configurations. Our model is trained on a
                                                                   server cluster equipped with 48 NVIDIA H800 GPUs. The
   We represent predictive targetsfuture visual states and ac-     training process contains 400k iterations, resulting in a total
tionsin a unified format to maximize knowledge sharing across      computational cost of 4,608 GPU hours. To preserve the
heterogeneous datasets. For visual prediction, we adopt latent     generalization capability and visual representation quality of
features extracted from a pretrained DINO [46] encoder, rather     the pre-trained foundation models, we keep the parameters of
than VAE-based pixel-space representations. DINO latents           the VLM [52] and the DINO [46] encoder frozen throughout
encode high-level semantic and spatial structure while sup-        the pre-training process, updating the MM-DiT and action
pressing background noise and low-level visual variations,         encoder/decoder. This design ensures that the model can learn
which facilitates learning scene dynamics that generalize          from new data without degrading the core abilities of the base
across diverse environments and object configurations.             models in cross-modal understanding and fine-grained visual
   For actions, we define a unified hand-centric action space      feature extraction.
based on end-effector motion, consisting of delta wrist poses      Data-Efficient Finetuning. To adapt the model to target
and finger configurations. For parallel-jaw grippers, the finger   embodiments and tasks for real-world deployment, we in-
state is represented by a single degree-of-freedom gripper         troduce a lightweight post-training stage. This stage follows
width, while for multi-finger dexterous hands, finger config-      the same data regime as pretraining and effectively lever-
urations are described using keypoints expressed in the wrist      ages naturally collected teleoperation data of mixed quality,
coordinate frame. This design enables consistent action model-     without requiring expert-level demonstrations. Compared to
ing across different embodiments and manipulation platforms.       prior finetuning pipelines that rely on carefully curated expert
   To model temporal dynamics, visual states and actions are       datasets, our method directly utilizes unfiltered teleoperation
organized as two synchronized temporal streams with different      data, substantially improving data efficiency and reducing the
sampling rates. Visual observations are sampled at 3hz, a          cost of data collection and annotation, thereby facilitating
lower frequency than actions, 10 hz. This reduces redundant        practical deployment.
computation from highly correlated consecutive frames while
preserving fine-grained action dynamics, allowing the model             IV. E MBODIED I NTERACTION DATASET (EI-30K)
to maintain coherent temporal alignment between fast-varying          We introduce the Embodied Interaction Dataset (EI-30K),
control signals and slower-evolving visual states.                 a large-scale collection of embodied interaction trajectories
                                                                   totaling over 30k hours. It consists of 8.03k hours of real-
D. Architecture: MM-DiT                                            world robot data, 8.6k hours of simulated robot data, 7.2k
   We adopt a Multi-Modal Diffusion Transformer (MM-DiT)           hours of human demonstrations with actions, and 10k hours
to jointly denoise action chunks and predict future visual         of actionless human videos. All subdatasets are annotated
features within a unified diffusion framework (Fig. 2). The        with explicit quality labels, enabling systematic analysis across
model operates on heterogeneous tokens while sharing a com-        different fidelity levels and supporting quality-aware learning.
mon Transformer backbone. Conditioning inputs include the          Data Unification. EI-30K consolidates datasets from hetero-
current observation, language instruction, diffusion timestep,     geneous platforms and tasks, which vary in storage formats,
and task specification. Observations and language are encoded      sensor modalities, and annotations. All data are converted
by a pretrained VLM into conditioning tokens. The diffusion        into the LeRobot format, providing a unified representation of
timestep is encoded using a sinusoidal embedding, and task         observations, actions, and language. This standardization fa-
information is represented by a learned task embedding. All        cilitates plug-and-play training, flexible data composition, and
Fig. 3: Aligned End Effector Coordinate Systems. We manually align coordinate frames across diverse robot and human
embodiments to ensure consistency. This shared representation enables joint learning from heterogeneous interaction data.

                                                                      Model            Vis. Rep. MMDiT      VLM        Success Rate ↑
                                                                      GR00T-N1.6[40]      -       -       Cosmos            47.6
                                                                      StarVLA[47]         -       -      Qwen3vl[52]        47.8
                                                                      GR00T-EI30k         -       -       Qwen3vl           51.3
                                                                      UWM-0.1B[60]      VAE      ✗           -              14.2
                                                                      UWM-1B            VAE      ✗        Qwen3vl           19.3
                                                                      UWM(MM-DiT)       VAE      ✓        Qwen3vl           20.0
                                                                      LDA(DiT)          DINO     ✗        Qwen3vl           48.9
                                                                      LDA-0.5B          DINO     ✓        Qwen3vl           50.7
                                                                      LDA-1B            DINO     ✓        Qwen3vl           55.4

                                                                   TABLE II: Results on RoboCasa-GR1 [39] and impact of state
                                                                   representation (VAE vs. DINO [46])model size the MM-DiT
Fig. 4: Statistics of EI-30K. The dataset contains more than       architecture on task success rates.
30k hours of diverse human and robot interaction data (right).
It spans varying episode lengths (left) and a rich set of
manipulation tasks (center).                                       24 tabletop rearrangement and articulated-object manipulation
                                                                   tasks with the GR-1 humanoid robot and Fourier dexterous
seamless integration of additional annotations, while greatly      hands. The benchmark provides challenging and realistic
reducing engineering overhead for handling diverse sources.        settings that require high-DoF dexterous manipulation from
Aligned Action Representation. To support consistent model-        egocentric RGB observations captured by a head-mounted
ing of physical interactions across embodiments, all available     camera. Following the GR00T [40] evaluation protocol, we
action annotations are expressed as hand-centric motion in a       finetune all models using 1,000 trajectories per task and evalu-
shared coordinate frame (Fig. 3). For robots, this includes the    ate each task with 51 trials, reporting average success rates. We
6-DoF end-effector pose plus gripper width or dexterous hand       compare LDA against GR00T and its strong variants, as well
joints. For humans, the 6-DoF wrist pose and full MANO [45]        as UWM [60], under matched training paradigms and data.
hand parameters are recorded. Camera extrinsics are retained       To ensure a fair comparison in terms of model capacity and
to decouple hand motion from egocentric head motion. All           pretraining, we reproduce a strong GR00T baseline (denoted as
coordinate frames are manually aligned to ensure geometric         GR00T-EI10k) with 1B parameters, pretrained on our curated
consistency across datasets, enabling joint learning from both     EI-30k high-quality subset and using Qwen3-VL as the VLM
human and robot trajectories.                                      encoder.
Quality Annotation and Cleaning. EI-30K applies systematic
                                                                   Comparison with Baselines. As shown in Table II, the orig-
cleaning and quality-aware annotation. Language annotations
                                                                   inal GR00T-N1.6 [40] with 3B parameters achieves a success
are normalized using a vision-language model to ensure
                                                                   rate of 47.6%. When pretrained on our curated EI-30k dataset,
semantic consistency. Motion segments without meaningful
                                                                   the reproduced GR00T-EI10k with 1B parameters shows a
hand-object interaction are removed, e.g., head-only or idle
                                                                   clear improvement, reaching 51.3%, highlighting the impact
segments in egocentric videos. Each trajectory is assigned a
                                                                   of high-quality embodied data. Under the same parameter
quality label based on action accuracy, and annotation com-
                                                                   budget, LDA further improves the success rate to 55.4%.
pleteness. Unlike aggressive filtering, low-quality trajectories
                                                                   These results indicate that, beyond data quality and parameter
are preserved, allowing downstream models to exploit the full
                                                                   scaling, jointly learning actions and dynamics within a unified
spectrum of data through quality-aware training.
                                                                   model provides additional gains when pretrained on mixed-
                      V. E XPERIMENTS                              quality data.
                                                                   Ablation Study. We further analyze key design choices under
A. Simulation Experiments                                          identical training data and optimization settings. UWM [60],
Benchmark and Baselines. We evaluate our method on                 despite jointly predicting actions and dynamics, achieves only
RoboCasa-GR1 [39], a simulated kitchen benchmark featuring         14.2% success due to limited model capacity and the use
                                                    Use the tongs to put the cake on the plate                                                               Sweep the crumbs into the dustpan.




                                                                    Bimanually remove the lid.                                                                             Wipe whiteboard.




                                                        Pull the nail out using the claw hammer.                                                                                   Flip the box.
Fig. 5: Real-World Manipulation Demonstrations Across Multiple Robotic Platforms and End-Effectors. Galbot G1 equipped
with a Sharpa dexterous hand (top-left), Unitree G1 with a BrainCo dexterous hand (middle and bottom-left), and Galbot G1
with a two-finger gripper (right).

                                            Pick & Place                    90.0
                                                                                         Contact-rich Manipulation                               Fine Manipulation                                   Long-horizon Manipulation
                                            80.0                                                                                                      80.0
                     80
                                                                     70.0                                                 72.0
                                                                                                                                                                                                                 65.0
  Success Rate (%)




                                                                                                     60.0                                      60.0
                     60                                                                                                                                                             55.0                  53.0
                                     50.0                    50.0                                           52.0
                                                                                                                   44.0
                             40.0                                                             40.0                                      40.0                                40.0
                     40                                                                                                                                             33.3                           35.0                              35.0

                                                                                       20.0
                     20

                                                                                                                                                                                                                        0.0 0.0
                     0
                          Put the pepper into the box    pick and handover and place      Flip the box        Wipe the board            Watering the flower Knock the specific block with hammer    Sweep the table     Clean the rubbish
                                                                                                            GR00T-N1.6            0.5                 Ours
Fig. 6: Success Rate Comparison on Real-World Gripper Manipulation Tasks. All models are few-shot fine-tuned on Galbot
and evaluated on eight tasks spanning Pick & Place, Contact-rich, Fine, and Long-horizon manipulation. LDA consistently
outperforms GR00T-N1.6 [40] and π0.5 [23].

of entangled VAE latent representations. Scaling UWM to                                                                          22-DoF Sharpa dexterous hands, while Unitree G1 uses 10-
1B parameters or replacing its DiT backbone with our MM-                                                                         DoF BrainCo hands. Across all configurations, the policy
DiT yields only marginal improvements (19.3% and 20.0%,                                                                          receives only egocentric RGB observations from a head-
respectively), suggesting that architectural constraints funda-                                                                  mounted camera. We evaluate four categories of manipulation
mentally limit its performance. In contrast, replacing pixel-                                                                    tasks under the gripper setting, Pick and Place, Contact-
space VAE latents with DINO [46] representations leads to a                                                                      rich Manipulation, Fine Manipulation, and Long-horizon Ma-
substantial performance gain (20.0% → 55.4%), highlighting                                                                       nipulationcovering diverse contact dynamics and temporal
the importance of semantically structured latent spaces for                                                                      horizons. Representative tasks include Beat Block, Flip Box,
effective scaling. Finally, removing the proposed MM-DiT                                                                         Handover, Pick-and-Place (Pepper), Sweep Table, Clean Rub-
architecture or reducing the model size to 0.5B parameters                                                                       bish, Water Flower, and Wipe Board. Dexterous manipulation
results in performance drops of 6.5% and 4.7%, respectively,                                                                     further includes tool-use tasks such as pulling a nail with a
confirming the effectiveness of the multi-expert design and its                                                                  hammer and flipping bread with a spatula, which require pre-
favorable scaling behavior.                                                                                                      cise force control and coordinated finger motion. Qualitative
                                                                                                                                 demonstrations are shown in Fig. 5. For each task, we collect
B. Real-world Experiments                                                                                                        100 teleoperated trajectories without enforcing expert-level
                                                                                                                                 execution. As a result, the dataset naturally exhibits mixed
  To validate the scalability and robustness of LDA-1B, we
                                                                                                                                 quality: approximately 50–80% of trajectories correspond to
conduct extensive real-world experiments focusing on few-
                                                                                                                                 expert behavior, while the remainder contain suboptimal ac-
shot adaptation to new embodiments, dexterous manipulation,
                                                                                                                                 tions such as pauses, retries, or inefficient motion patterns.
and data efficiency under mixed-quality supervision.
Real-World Robot and Task Setup. We evaluate our method                                                                          Baselines and Finetuning Protocol. We compare LDA-1B
on two humanoid platforms: Galbot G1 and Unitree G1.                                                                             against two strong baselines, π0.5 [23] and GR00T [40]. To
Galbot G1 is equipped with either a two-finger gripper or                                                                        ensure stable and competitive performance, baseline models
                                                                                                                                        Place the pen into the box   Bimanually remove the lid
                                             Low DoFs Hand                                        High DoFs Hand              Method
                                                        100 100
                    100                90                                                                             90
                                                                                                                                       63 High 63 High + 37 Low 66 High 66 High + 34 Low
 Success Rate (%)

                                                                                80
                     80      75
                                                                                                       70                     π0.5       60          40 (20↓)         50         40 (10↓)
                                                                                                                              Ours       70          80 (10↑)         50         60 (10 ↑)
                     60
                                                   40                40
                     40                                                                                                    TABLE IV: Data-efficient mixed-quality finetuning. LDA-
                                  20                                                         20
                     20                                                                           10          10 10        1B improves success rates by +10% on both tasks when
                                                                           0                                               incorporating low-quality trajectories, while π0.5 degrades
                      0                                 k




                                                                          il
                              ttle




                                                                                                               ad
                                                                                              ad
                                                                                                                           significantly, demonstrating effective utilization of noisy data

                                                                         Na
                                                   oo




                                                                                                              Bre
                                                                                             Bre
                            Bo




                                               cb




                                                                      ll
                                                                   Pu
                                              Ma




                                                                                                            Flip
                                                                                              k
                              k




                                                                                           Pic
                          Pic




                                                                                                                           for enhanced generalization.
                                              en




                                                            GR00T-N1.6                            Ours
                                            Op




                                                                                     0.5



Fig. 7: Success Rate Comparison on Real-World Dexterous
Manipulation Tasks We evaluate the real-world performance                                                                  stable contact maintenance between the hammer and the nail,
of our model against baselines (GR00T-N1.6 and π0.5 ) on                                                                   LDA-1B achieves 80% success, reliably localizing targets
3 low DoFs hand (BrainCo) tasks and 2 high DoFs hand                                                                       and adjusting sensitive actions, whereas π0.5 largely fails.
(Sharpa) tasks. Ours (dark blue) consistently outperforms                                                                  On high-DoF tasks such as Flip Bread, which involve high-
baselines especially on fine dexterous task (pull nails) and                                                               dimensional control, continuous contact, and coordinated wrist
high DoFs tasks.                                                                                                           motion, LDA-1B attains 90% success, while π0.5 reaches only
                                                                                                                           10%. These results demonstrate that pretraining on large-scale
                                                                   Pick & Place                                            human data provides strong latent priors for dexterous control,
                                       Method
                                                        Object Background OOD Pos.                                         enabling precise finger coordination and object reorientation
                                       π0.5             26.7             20.0                 6.7                          with limited robot data. In contrast, baseline policies struggle
                                       GR00T            40.0             40.0                 20.0                         to generalize as action dimensionality and contact complexity
                                       Ours             60.0             60.0                 40.0
                                                                                                                           increase.
TABLE III: Robust Generalization under visual and spatial                                                                  Generalization Ability. To evaluate the generalization of our
perturbations. LDA-1B maintains 60.0% success across un-                                                                   policy, we test pick and place task under three conditions:
seen objects, backgrounds, and OOD positions, demonstrating                                                                novel objects, unseen backgrounds, and out-of-distribution
effective focus on task-critical affordances over visual noise                                                             (OOD) starting position, shown as Fig 8. As summarized in
through latent dynamics pretraining.                                                                                       Table III, our model maintains high success rates despite visual
                                                                                                                           and spatial perturbations. The large-scale latent dynamics
                                                                                                                           pretraining allows the model to ignore visual distractors (back-
are finetuned exclusively on the filtered expert subset. In                                                                ground changes) while focusing on relevant object affordances,
contrast, LDA-1B leverages all collected trajectories and learns                                                           demonstrating strong generalization relative to baselines.
directly from the full mixed-quality distribution via our Uni-                                                             Data-Efficient Finetuning. We analyze the value of mixed-
versal Embodied Data Ingestion mechanism.                                                                                  quality data ingestion during finetuning stage, by post-training
Results on Gripper Manipulation. We first evaluate few-shot                                                                on two splits: (1) High-Quality Only (expert data), and (2)
adaptation by deploying LDA-1B on the Galbot G1, which is                                                                  High + Low Quality (all 100 trajectories). As shown in Ta-
excluded from our EI-30k pretraining dataset. As shown in                                                                  ble IV, while baseline models degrade when low-quality data
Fig. 6, LDA-1B consistently outperforms all baselines across                                                               is added, LDA-1B effectively leverages these noisy trajecto-
task categories. On simple pick-and-place tasks, LDA-1B                                                                    ries, boosting performance with 10%, substantially improving
achieves success rates of 80%–90%, indicating effective few-                                                               data efficiency and reducing the cost of data collection and
shot adaptation to a new robot embodiment. The performance                                                                 annotation for practical deployment.
gap widens substantially in contact-rich and long-horizon
scenarios. For instance, the Clean the Rubbish task requires                                                               C. Analysis of Scaling Effects
coordinated dual-arm manipulation, tool usage (dustpan), and                                                                  To analyze the scaling behavior of LDA, we systematically
sequential object transfer into a trash bin, where errors can                                                              vary model capacity, data composition, and training objectives.
easily accumulate over time. In this setting, LDA-1B achieves                                                              All models are evaluated on an unseen test set sampled from a
a 35% success rate, while both GR00T and π0.5 fail entirely                                                                held-out subset of Agibot World [6]. We report the action pre-
(0%). This result suggests that latent dynamics modeling en-                                                               diction L1 error as the primary metric, which serves as a stable
ables LDA to better anticipate action-induced state transitions,                                                           and reproducible proxy for real-world performance. Fig. 10
maintain temporal consistency, and recover from intermediate                                                               summarizes the results under four training configurations: (i)
failures in extended manipulation sequences.                                                                               Policy Only, (ii) Policy + Visual Forecasting, (iii) Policy with
Results on Dexterous Manipulation. We further evaluate                                                                     Forward and Inverse Dynamics, and (iv) the full co-training
LDA-1B on both low-DoF and high-DoF dexterous manip-                                                                       framework (Ours). These experiments jointly reveal how LDA
ulation tasks, as reported in Fig. 7. On low-DoF tasks such                                                                scales under heterogeneous supervision and increasing model
as Pull Nail, which requires precise motion direction and                                                                  capacity.
                 Training             OOD-Position                 Novel Objects              Variant Background
                                Fig. 8: Generalization evaluation setup on Pick and Place task




Fig. 9: Visualization of latent forward dynamics. Our model generates accurate future visual representations (top) aligned
with ground truth (bottom) across time steps, capturing semantic object structure and motion dynamics

                                                                    unstable behavior: while moderate scaling initially reduces
                                                                    error, incorporating lower-quality data leads to performance
                                                                    degradation. Similarly, partial co-training variants that exclude
                                                                    either dynamics or visual forecasting objectives (green and
                                                                    brown lines) improve robustness but fail to fully exploit the
                                                                    available data. In contrast, the full co-training framework (blue
                                                                    line) exhibits consistent improvement as additional hetero-
                                                                    geneous data is introduced. Notably, even after all action-
                                                                    labeled trajectories are exhausted, adding 10k actionless videos
                                                                    continues to reduce prediction error. These indicates that
                                                                    LDA can extract useful supervisory signals from low-qaulity
                                                                    data and non-action data through latent dynamics and visual
                                                                    forecasting, rather than treating such data as noise. Overall,
                                                                    these results demonstrate that Universal Data Ingestion is most
                                                                    effective when heterogeneous data and co-training objectives
                                                                    are scaled together, enabling LDA to fully utilize mixed-
                                                                    quality supervision.

                                                                    Effectiveness of Latent Representation. Although both LDA
                                                                    and UWM incorporate dynamics-related supervision, their
Fig. 10: Scaling Analysis of LDA, evaluated by action pre-          scaling behaviors diverge substantially due to differences in
diction error on unseen test set. Top: Action prediction error      the structure of their latent spaces. As shown in Fig. 10,
decreases to 6.6 with 30k hours of training data, demonstrating     UWM quickly saturates as data scale and model capacity
effective utilization of diverse data sources. Bottom: LDA con-     increase, with additional supervision yielding diminishing or
sistently outperforms UWM across model sizes (0.1B→1B)              even negative returns. This indicates that simply increasing
with increasing training data, while the baseline saturates         data or parameters is insufficient when the latent space cannot
rapidly.                                                            support compositional and causal reasoning. This limitation
                                                                    stems from UWM’s VAE-derived latent representation, which
                                                                    entangles appearance, geometry, and dynamics at a low-level
Effectiveness of Universal Data Ingestion. Effectively lever-       feature granularity. Such entanglement restricts the models
aging heterogeneous embodied data requires jointly scaling          ability to factorize action-induced state transitions and prevents
both data sources and training objectives. As shown in Fig. 10,     effective reuse of heterogeneous supervision during scaling.
LDA achieves its best performance only when all supervi-            In contrast, LDA operates in a semantically structured la-
sion signalspolicy learning, dynamics modeling, and visual          tent space obtained from large-scale visual pretraining. This
forecastingare optimized together. When either the data scale       representation preserves object-level semantics and spatial
or the training objectives are reduced, performance degrades        coherence, enabling dynamics learning to scale smoothly with
noticeably. Using only action-labeled trajectories with a Policy    increased model capacity, richer training objectives, and more
Only objective (grey line), increasing the dataset size yields      diverse datasets.
                                                                    surface where contact and force application are expected.
                                                                    Importantly, background clutter and visually salient but non-
                                                                    interactive regions are largely suppressed. These results in-
                                                                    dicate that LDA conditions visual attention on the physical
                                                                    consequences of actions, selectively focusing on regions that
                                                                    drive state transitions rather than static appearance.

                                                                    VI. C ONCLUSION , L IMITATION AND F UTURE D IRECTION
                                                                       We present LDA-1B, a robot foundation model that scales
                                                                    latent dynamics learning via universal embodied data inges-
Fig. 11: Attention Heat Map: ”Push Right”(top) highlights           tion. By assigning heterogeneous data distinct roles and lever-
the mug’s leading edge and trajectory; ”Push Close”(bottom)         aging over 30k hours of human and robot trajectories in the
concentrates on the contact surface. The model attends exclu-       EI-30k dataset, LDA-1B learns dynamics in a structured DINO
sively to movable regions while ignoring irrelevant background      latent space and employs a mixed-frequency multimodal diffu-
clutter.                                                            sion transformer, enabling stable training at the 1B-parameter
                                                                    scale. Experiments show strong performance across diverse
                                                                    manipulation and long-horizon tasks, as well as data-efficient
Effectiveness of Model Scaling. Beyond data scale, LDA
                                                                    fine-tuning on imperfect trajectories. Limitations include the
exhibits consistent and predictable improvements as model
                                                                    reliance on fixed DINO visual features and predominantly
capacity increases. As shown in Fig. 10, scaling the model
                                                                    egocentric camera viewpoints, which may constrain general-
from 0.1B to 0.5B and further to 1B parameters leads to
                                                                    ization to new visual perspectives and multi-modal signals.
monotonic reductions in action prediction error under the full
                                                                    Future work includes jointly learning visual representations
co-training framework. This indicates that LDA can effectively
                                                                    and latent dynamics, extending to richer sensory modalities,
absorb additional capacity to model increasingly complex
                                                                    automatically optimizing data roles, and fostering broader
actiondynamics relationships when sufficient heterogeneous
                                                                    community adoption of scalable, heterogeneous data-driven
supervision is available. The results highlight a promising
                                                                    robot foundation models.
scaling paradigm in which model capacity, training objectives,
and heterogeneous embodied data are jointly aligned, enabling                          ACKNOWLEDGMENTS
reliable performance gains.
                                                                       We thank Caowei Meng for collecting teleoperation data;
                                                                    Haoran Liu and Jiayi Su for their assistance in early-stage
D. Analysis of Dynamics Learning
                                                                    exploration; Yu-Wei Chao and Shengliang Deng for fruit-
Qualitative Analysis of Latent Forward Dynamics. Beyond             ful discussions; and Junkai Zhao for providing experimental
quantitative prediction errors, we qualitatively examine the        equipment.
forward dynamics learned by LDA, visualized via PCA pro-
jections of DINO feature embeddings. As shown in Fig. 16,                                   R EFERENCES
the model produces coherent future-state predictions that re-        [1] Build AI.      Egocentric-10k, 2025.      URL https://
spect physical constraints such as object permanence, contact            huggingface.co/datasets/builddotai/Egocentric-10K.
continuity, and motion consistency under the applied action.         [2] Prithviraj Banerjee, Sindi Shkodrani, Pierre Moulon,
Notably, the predicted dynamics focus on task-relevant objects           Shreyas Hampali, Shangchen Han, Fan Zhang, Linguang
while remaining invariant to visual distractors that do not              Zhang, Jade Fountain, Edward Miller, Selen Basol, et al.
influence the control loop. This suggests that LDA learns a              Hot3d: Hand and object tracking in 3d from egocentric
dynamics-aware latent world model, capturing how actions                 multi-view videos. In Proceedings of the Computer
causally propagate through the scene rather than merely ex-              Vision and Pattern Recognition Conference, pages 7061–
trapolating visual appearance.                                           7071, 2025.
Action-Conditioned Attention. To interpret how LDA rea-              [3] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan
sons about action-induced state transitions, we visualize atten-         Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao
tion maps conditioned on different action primitives. As shown           Feng, Chendong Xiang, Yinze Rong, et al. Motus:
in Fig. 11, we compare the attention patterns induced by an              A unified latent action world model. arXiv preprint
active motion command (a1 ) with those under a static No-Op              arXiv:2512.13030, 2025.
command (a2 ), and compute their difference to reveal action-        [4] Kevin Black, Noah Brown, Danny Driess, Adnan Es-
specific visual grounding. Across tasks, LDA consistently                mail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy
attends to regions that are causally relevant to the commanded           Groom, Karol Hausman, Brian Ichter, et al. π0 : A vision-
interaction. In the Push Right scenario, the attention difference        language-action flow model for general robot control.
highlights the leading edge of the mug and the anticipated               arXiv preprint arXiv:2410.24164, 2024.
motion direction, reflecting awareness of object displacement.       [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yev-
In the Push Close task, attention concentrates on the drawer             gen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana
     Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine         Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert
     Hsu, et al. Rt-1: Robotics transformer for real-world       Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn,
     control at scale. arXiv preprint arXiv:2212.06817, 2022.    Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang,
 [6] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding,       Haochen Shi, Henghui Bao, Heni Ben Amor, Hen-
     Siyuan Feng, Xindong He, Xu Huang, et al. Agibot            rik I Christensen, Hiroki Furuta, Homanga Bharadhwaj,
     world colosseo: A large-scale manipulation platform for     Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch,
     scalable and intelligent embodied systems. In 2025          Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-
     IEEE/RSJ International Conference on Intelligent Robots     Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan
     and Systems (IROS). IEEE, 2025.                             Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg,
 [7] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao,         Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu,
     Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang           Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan
     Li. Univla: Learning to act anywhere with task-centric      Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun
     latent actions. arXiv preprint arXiv:2505.06111, 2025.      Yang, Jitendra Malik, Joo Silvrio, Joey Hejna, Jonathan
 [8] Remi Cadene, Simon Alibert, Alexander Soare, Quentin        Booher, Jonathan Tompson, Jonathan Yang, Jordi Sal-
     Gallouedec, Adil Zouitine, Steven Palma, Pepijn             vador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang,
     Kooijmans, Michel Aractingi, Mustafa Shukor, Dana           Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan
     Aubakirova, Martino Russi, Francesco Capuano, Caro-         Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra
     line Pascal, Jade Choghari, Jess Moss, and Thomas Wolf.     Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin
     Lerobot: State-of-the-art machine learning for real-world   Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran
     robotics in pytorch.      https://github.com/huggingface/   Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan,
     lerobot, 2024.                                              Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle
 [9] Junhao Cai, Zetao Cai, Jiafei Cao, Yilun Chen, Zeyu         Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen,
     He, Lei Jiang, Hang Li, Hengjie Li, Yang Li, Yufei Liu,     Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi ”Jim” Fan, Li-
     et al. Internvla-a1: Unifying understanding, generation     onel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion
     and action for robotic manipulation. arXiv preprint         Lepert, Marius Memmel, Masayoshi Tomizuka, Masha
     arXiv:2601.02456, 2026.                                     Itkina, Mateo Guaman Castro, Max Spero, Maximilian
[10] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang,            Du, Michael Ahn, Michael C. Yip, Mingtong Zhang,
     Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao          Mingyu Ding, Minho Heo, Mohan Kumar Srirama,
     Luo, Fan Wang, et al. Worldvla: Towards autoregressive      Mohit Sharma, Moo Jin Kim, Muhammad Zubair Ir-
     action world model. arXiv preprint arXiv:2506.21539,        shad, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess,
     2025.                                                       Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di
[11] Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya          Palo, Nur Muhammad Mahi Shafiullah, Oier Mees,
     Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang,           Oliver Kroemer, Osbert Bastani, Pannag R Sanketi,
     Yu Qiao, et al. Internvla-m1: A spatially guided vision-    Patrick ”Tree” Miller, Patrick Yin, Paul Wohlhart, Peng
     language-action framework for generalist robot policy.      Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet,
     arXiv preprint arXiv:2510.13778, 2025.                      Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan
[12] Open X-Embodiment Collaboration, Abby O’Neill, Ab-          Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto
     dul Rehman, Abhinav Gupta, Abhiram Maddukuri, Ab-           Mart’in-Mart’in, Rohan Baijal, Rosario Scalise, Rose
     hishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn         Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Rus-
     Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain,          sell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian,
     Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan,          Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan
     Alexander Khazatsky, Anant Rai, Anchit Gupta, An-           Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham
     drew Wang, Andrey Kolobov, Anikait Singh, Animesh           Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu,
     Garg, Aniruddha Kembhavi, Annie Xie, Anthony Bro-           Siddhant Haldar, Siddharth Karamcheti, Simeon Ade-
     han, Antonin Raffin, Archit Sharma, Arefeh Yavary,          bola, Simon Guist, Soroush Nasiriany, Stefan Schaal,
     Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben           Stefan Welker, Stephen Tian, Subramanian Ramamoor-
     Burgess-Limerick, Beomjoon Kim, Bernhard Schlkopf,          thy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj
     Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Char-       Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta,
     lotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng       Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas
     Chi, Chenguang Huang, Christine Chan, Christopher           Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z.
     Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei           Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung,
     Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak        Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Vitor
     Pathak, Dhruv Shah, Dieter Bchler, Dinesh Jayaraman,        Guizilini, Wei Zhan, Wenxuan Zhou, Wolfram Burgard,
     Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan       Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu,
     Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu        Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li,
     Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou,      Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim,
     Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu,                arxiv:2006.11239, 2020.
     Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou,           [21] Ryan Hoque, Peide Huang, David J Yoon, Mouli Siva-
     Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao,                purapu, and Jian Zhang. Egodex: Learning dexterous
     Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang,                  manipulation from large-scale egocentric video. arXiv
     Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwa-                preprint arXiv:2505.11709, 2025.
     sawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff          [22] Yuhang Huang, JIazhao Zhang, Shilong Zou, XInwang
     Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open X-             Liu, Ruizhen Hu, and Kai Xu. Ladi-wm: A latent
     Embodiment: Robotic learning datasets and RT-X mod-               diffusion-based world model for predictive manipulation.
     els. https://arxiv.org/abs/2310.08864, 2023.                      arXiv preprint arXiv:2505.11528, 2025.
[13] Dima Damen, Hazel Doughty, Giovanni Maria Farinella,         [23] Physical Intelligence, Kevin Black, Noah Brown, James
     Sanja Fidler, Antonino Furnari, Evangelos Kazakos, Da-            Darpinian, Karan Dhabalia, Danny Driess, Adnan Es-
     vide Moltisanti, Jonathan Munro, Toby Perrett, Will               mail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al.
     Price, et al. The epic-kitchens dataset: Collection, chal-        π0.5 : a vision-language-action model with open-world
     lenges and baselines. IEEE Transactions on Pattern                generalization. arXiv preprint arXiv:2504.16054, 2025.
     Analysis and Machine Intelligence, 43(11):4125–4141,         [24] Yuming Jiang, Siteng Huang, Shengke Xue, Yaxi Zhao,
     2020.                                                             Jun Cen, Sicong Leng, Kehan Li, Jiayan Guo, Kexiang
[14] Shengliang Deng, Mi Yan, Songlin Wei, Haixin Ma,                  Wang, Mingxiu Chen, et al. Rynnvla-001: Using human
     Yuxin Yang, Jiayi Chen, Zhiqi Zhang, Taoyu Yang,                  demonstrations to improve robot manipulation. arXiv
     Xuheng Zhang, Wenhao Zhang, et al. Graspvla: a                    preprint arXiv:2509.15212, 2025.
     grasping foundation model pre-trained on billion-scale       [25] Siddharth Karamcheti, Suraj Nair, Annie S Chen,
     synthetic action data. arXiv preprint arXiv:2505.03233,           Thomas Kollar, Chelsea Finn, Dorsa Sadigh, and Percy
     2025.                                                             Liang.     Language-driven representation learning for
[15] Zicong Fan, Omid Taheri, Dimitrios Tzionas,                       robotics. In Robotics: Science and Systems (RSS), 2023.
     Muhammed Kocabas, Manuel Kaufmann, Michael J.                [26] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ash-
     Black, and Otmar Hilliges. ARCTIC: A dataset for                  win Balakrishna, Sudeep Dasari, Siddharth Karam-
     dexterous bimanual hand-object manipulation.            In        cheti, Soroush Nasiriany, Mohan Kumar Srirama,
     Proceedings IEEE Conference on Computer Vision and                Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid:
     Pattern Recognition (CVPR), 2023.                                 A large-scale in-the-wild robot manipulation dataset.
[16] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu,              Robotics: Science and Systems (RSS), 2024.
     Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu.             [27] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted
     Rh20t: A comprehensive robotic dataset for learning               Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov,
     diverse skills in one-shot, 2023. URL https://arxiv.org/          Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al.
     abs/2307.00595.                                                   Openvla: An open-source vision-language-action model.
[17] Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michal-              In Conference on Robot Learning, pages 2679–2713.
     ski, Joanna Materzynska, Susanne Westphal, Heuna Kim,             PMLR, 2025.
     Valentin Haenel, Ingo Fruend, Peter Yianilos, Moritz         [28] LejuRobotics. Let:full-size humanoid robot real-world
     Mueller-Freitag, et al. The” something something” video           dataset.     https://huggingface.co/datasets/LejuRobotics/
     database for learning and evaluating visual common                let dataset, 2025.
     sense. In Proceedings of the IEEE international con-         [29] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gok-
     ference on computer vision, pages 5842–5850, 2017.                men, Sanjana Srivastava, Roberto Martn-Martn, Chen
[18] Kristen Grauman, Andrew Westbury, Eugene Byrne,                   Wang, Gabrael Levine, Wensi Ai, Benjamin Martinez,
     Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jack-            Hang Yin, Michael Lingelbach, Minjune Hwang, Ayano
     son Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al.            Hiranaka, Sujay Garlanka, Arman Aydin, Sharon Lee,
     Ego4d: Around the world in 3,000 hours of egocentric              Jiankai Sun, Mona Anvari, Manasi Sharma, Dhruva
     video. In Proceedings of the IEEE/CVF conference on               Bansal, Samuel Hunter, Kyu-Young Kim, Alan Lou,
     computer vision and pattern recognition, pages 18995–             Caleb R Matthews, Ivan Villa-Renteria, Jerry Huayang
     19012, 2022.                                                      Tang, Claire Tang, Fei Xia, Yunzhu Li, Silvio Savarese,
[19] Kristen Grauman, Andrew Westbury, Lorenzo Torresani,              Hyowon Gweon, C. Karen Liu, Jiajun Wu, and Li Fei-
     Kris Kitani, Jitendra Malik, Triantafyllos Afouras, Kumar         Fei. Behavior-1k: A human-centered, embodied ai
     Ashutosh, Vijay Baiyya, Siddhant Bansal, Bikram Boote,            benchmark with 1,000 everyday activities and realistic
     et al. Ego-exo4d: Understanding skilled human activity            simulation. arXiv preprint arXiv:2403.09227, 2024.
     from first-and third-person perspectives. In Proceedings     [30] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran
     of the IEEE/CVF Conference on Computer Vision and                 Song. Unified video action model. arXiv preprint
     Pattern Recognition, pages 19383–19400, 2024.                     arXiv:2503.00200, 2025.
[20] Jonathan Ho, Ajay Jain, and Pieter Abbeel.            De-    [31] Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang,
     noising diffusion probabilistic models. arXiv preprint            Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai,
     Si Liu, Jianlan Luo, et al. Genie envisioner: A uni-            Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey
     fied world foundation platform for robotic manipulation.        Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You
     arXiv preprint arXiv:2508.05635, 2025.                          Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi,
[32] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan,             Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and
     Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun               Sergey Levine. Octo: An open-source generalist robot
     Zhu. Rdt-1b: a diffusion foundation model for bimanual          policy. In Proceedings of Robotics: Science and Systems,
     manipulation. arXiv preprint arXiv:2410.07864, 2024.            Delft, Netherlands, 2024.
[33] Yun Liu, Haolin Yang, Xu Si, Ling Liu, Zipeng Li,          [42] Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex
     Yuxiang Zhang, Yebin Liu, and Li Yi. Taco: Bench-               Bewley, Alex Herzog, Alexander Irpan, Alexander Khaz-
     marking generalizable bimanual tool-action-object under-        atsky, Anant Rai, Anikait Singh, Anthony Brohan, et al.
     standing. In Proceedings of the IEEE/CVF Conference on          Open x-embodiment: Robotic learning datasets and RT-X
     Computer Vision and Pattern Recognition, pages 21740–           models. arXiv preprint arXiv:2310.08864, 2023.
     21751, 2024.                                               [43] William Peebles and Saining Xie.           Scalable dif-
[34] Yunze Liu, Yun Liu, Che Jiang, Kangbo Lyu, Weikang              fusion models with transformers.         arXiv preprint
     Wan, Hao Shen, Boqiang Liang, Zhoujie Fu, He Wang,              arXiv:2212.09748, 2022.
     and Li Yi. Hoi4d: A 4d egocentric dataset for category-    [44] Heqian Qiu, Zhaofeng Shi, Lanxiao Wang, Huiyu Xiong,
     level human-object interaction. In Proceedings of the           Xiang Li, and Hongliang Li. Egome: Follow me via
     IEEE/CVF Conference on Computer Vision and Pattern              egocentric view in real world. arXiv e-prints, pages
     Recognition, pages 21013–21022, 2022.                           arXiv–2501, 2025.
[35] Hao Luo, Yicheng Feng, Wanpeng Zhang, Sipeng Zheng,        [45] Javier Romero, Dimitrios Tzionas, and Michael J. Black.
     Ye Wang, Haoqi Yuan, Jiazheng Liu, Chaoyi Xu, Qin Jin,          Embodied hands: Modeling and capturing hands and
     and Zongqing Lu. Being-h0: vision-language-action pre-          bodies together. ACM Transactions on Graphics, (Proc.
     training from large-scale human videos. arXiv preprint          SIGGRAPH Asia), 36(6), November 2017.
     arXiv:2507.15597, 2025.                                    [46] Oriane Siméoni, Huy V. Vo, Maximilian Seitzer, Federico
[36] Jiangran Lyu, Ziming Li, Xuesong Shi, Chaoyi Xu,                Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khali-
     Yizhou Wang, and He Wang. Dywa: Dynamics-adaptive               dov, Marc Szafraniec, Seungeun Yi, Michaël Ramamon-
     world action model for generalizable non-prehensile ma-         jisoa, Francisco Massa, Daniel Haziza, Luca Wehrstedt,
     nipulation. arXiv preprint arXiv:2503.16806, 2025.              Jianyuan Wang, Timothée Darcet, Théo Moutakanni,
[37] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayara-                Leonel Sentana, Claire Roberts, Andrea Vedaldi, Jamie
     man, Osbert Bastani, Vikash Kumar, and Amy Zhang.               Tolan, John Brandt, Camille Couprie, Julien Mairal,
     Vip: Towards universal visual reward and represen-              Hervé Jégou, Patrick Labatut, and Piotr Bojanowski.
     tation via value-implicit pre-training. arXiv preprint          DINOv3, 2025. URL https://arxiv.org/abs/2508.10104.
     arXiv:2210.00030, 2022.                                    [47] starVLA Contributors. Starvla: A lego-like codebase for
[38] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea           vision-language-action model developing. GitHub repos-
     Finn, and Abhinav Gupta. R3m: A universal visual                itory, 1 2025. URL https://github.com/starVLA/starVLA.
     representation for robot manipulation. In Conference on    [48] Galaxea Team. Galaxea g0: Open-world dataset and dual-
     Robot Learning (CoRL). PMLR, 2022.                              system vla model. arXiv preprint arXiv:2509.00576v1,
[39] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang,              2025.
     Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Man-          [49] Xin Wang, Taein Kwon, Mahdi Rad, Bowen Pan, Ishani
     dlekar, and Yuke Zhu. Robocasa: Large-scale simulation          Chakraborty, Sean Andrist, Dan Bohus, Ashley Feniello,
     of everyday tasks for generalist robots. In Robotics:           Bugra Tekin, Felipe Vieira Frujeri, et al. Holoassist:
     Science and Systems, 2024.                                      an egocentric human interaction dataset for interactive
[40] NVIDIA,       Johan     Bjorck,    Nikita   Cherniadev          ai assistants in the real world. In Proceedings of
     Fernando Castaeda, Xingye Da, Runyu Ding, Linxi ”Jim”           the IEEE/CVF International Conference on Computer
     Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang,           Vision, pages 20270–20281, 2023.
     Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia,      [50] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che,
     Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin           Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao,
     Liu, Edith Llontop, Loic Magne, Ajay Mandlekar,                 Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark
     Avnish Narayan, Soroush Nasiriany, Scott Reed,                  on multi-embodiment intelligence normative data for
     You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang,                robot manipulation. In Robotics: Science and Systems
     Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia           (RSS) 2025. Robotics: Science and Systems Foundation,
     Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang,             2025. URL https://www.roboticsproceedings.org/rss21/
     Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. GR00T                  p152.pdf.
     N1: An open foundation model for generalist humanoid       [51] Shihan Wu, Xuecheng Liu, Shaoxuan Xie, Pengwei
     robots. In ArXiv Preprint, March 2025.                          Wang, Xinghang Li, Bowen Yang, Zhe Li, Kai Zhu,
[41] Octo Model Team, Dibya Ghosh, Homer Walke, Karl                 Hongyu Wu, Yiheng Liu, et al. Robocoin: An open-
     sourced bimanual robotic data collection for integrated   world models: Coupling video and action diffusion for
     manipulation. arXiv preprint arXiv:2511.17441, 2025.      pretraining on large robotic datasets. arXiv preprint
[52] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,          arXiv:2504.02792, 2025.
     Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chen-
     gen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu,
     Fan Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei,
     Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei
     Zhang, Jianxin Yang, Jiaxi Yang, Jing Zhou, Jingren
     Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang,
     Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze
     Li, Pei Zhang, Peng Wang, Qin Zhu, Rui Men, Ruize
     Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi
     Tang, Wenbiao Yin, Xingzhang Ren, Xinyu Wang, Xinyu
     Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang
     Zhang, Yinger Zhang, Yu Wan, Yuqiong Liu, Zekun
     Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and
     Zihan Qiu. Qwen3 technical report. arXiv preprint
     arXiv:2505.09388, 2025.
[53] Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui
     Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin
     Cheng, Ri-Zhao Qiu, et al. Egovla: Learning vision-
     language-action models from egocentric human videos.
     arXiv preprint arXiv:2507.12440, 2025.
[54] Xinyu Zhan, Lixin Yang, Yifei Zhao, Kangrui Mao,
     Hanlin Xu, Zenan Lin, Kailin Li, and Cewu Lu. Oakink2:
     A dataset of bimanual hands-object manipulation in com-
     plex task completion. In Proceedings of the IEEE/CVF
     Conference on Computer Vision and Pattern Recognition,
     pages 445–456, 2024.
[55] Hongxiang Zhao, Xingchen Liu, Mutian Xu, Yiming
     Hao, Weikai Chen, and Xiaoguang Han. Taste-rob:
     Advancing video generation of task-oriented hand-object
     interaction for generalizable robotic manipulation. In
     Proceedings of the Computer Vision and Pattern Recog-
     nition Conference, pages 27683–27693, 2025.
[56] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea
     Finn. Learning fine-grained bimanual manipulation with
     low-cost hardware. In Robotics: Science and Systems
     (RSS), 2023.
[57] Zhenyu Zhao, Hongyi Jing, Xiawei Liu, Jiageng Mao,
     Abha Jha, Hanwen Yang, Rong Xue, Sergey Zakharor,
     Vitor Guizilini, and Yue Wang. Humanoid everyday:
     A comprehensive robotic dataset for open-world hu-
     manoid manipulation, 2025. URL https://arxiv.org/abs/
     2510.08807.
[58] Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck,
     Yu Fang, Fengyuan Hu, Joel Jang, Kaushil Kundalia,
     Zongyu Lin, Loic Magne, et al. Flare: Robot learn-
     ing with implicit world modeling.        arXiv preprint
     arXiv:2505.15659, 2025.
[59] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel
     Pinto. Dino-wm: World models on pre-trained vi-
     sual features enable zero-shot planning. arXiv preprint
     arXiv:2411.04983, 2024.
[60] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin
     Burchfiel, Paarth Shah, and Abhishek Gupta. Unified
                        A PPENDIX A                                • StarVLA: A GR00T variant following StarVLA [47],
                    D ETAILS OF M ODEL                               replacing the original VLM with Qwen3-VL and trained
   We employ Qwen3-VL-4B-Instruct [52] as the joint lan-             from scratch on RoboCasa.
                                                                   • GR00T-EI10k: A strong reproduced baseline pretrained
guage and vision encoder to extract high-level semantic rep-
resentations. Visual observations are encoded using DINOv3-          on our EI-10k high-qaulity subset with Qwen3-VL, where
ViT-s [46]. During pretraining, we freeze both the VLM and           VLM parameters are unfrozen during finetuning.
                                                                   • LDA (DiT): An ablated version of LDA replacing MM-
the DINOv3 image encoder to leverage the strong priors from
the pretrained language and vision models while allowing             DiT with a standard DiT backbone.
                                                                   • LDA-1B: The full Latent Dynamics Action model with
the MM-DiT to be trained thoroughly on the downstream
structure. In the subsequent finetuning stage, we unfreeze the       MM-DiT, designed to model action-induced state transi-
VLM to enable end-to-end adaptation and further improve              tions in a structured latent space.
overall performance.                                             B. Task-Level Results and Analysis.
   Additionally, the MM-DiT is conditioned on a short history
                                                                     Table VI reports detailed per-task success rates. LDA con-
of two timesteps, comprising both past DINO-encoded obser-
                                                                 sistently outperforms GR00T across contact-rich and cluttered
vations and actions, to effectively capture temporal dynamics.
                                                                 rearrangement tasks, with particularly large gains in scenarios
Table V presents the detailed configurations of the model and
                                                                 requiring precise placement and closing actions, such as PnP
the hyperparameters used during training.
                                                                 Bottle To Cabinet Close (76 % vs. 51.5%), PnP Can To Drawer
                                                                 Close (71% vs. 13%), and PnP Milk To Microwave Close
             Parameter                 Value
                                                                 (52% vs. 14%).
             Model                                                   As illustrated in Fig. 12, GR00T frequently fails due to a
             VLM                  Qwen3-VL [52]
             Observation Encoder DINOv3-ViT-s [46]               lack of anticipation of post-action consequences. For example,
             Hidden Size               1536                      after placing an object inside a container, GR00T often retracts
             Layers                     16                       its arm along a trajectory that collides with the object, causing
             Attention Heads            32
             Image Shape           (224, 224, 3)                 it to tip over. In contrast, LDA anticipates such interactions and
             Latent Image Shape    (14, 14, 384)                 generates trajectories that preserve object stability throughout
             Action Chunk               16                       the entire manipulation sequence.
             Training                                                The largest improvements are observed in novel-object re-
             Batch Size         32 * 48 (pretraining)
                                 12 * 8 (finetuning)
                                                                 arrangement tasks involving transfers across surfaces and con-
             Learning Rate              1e−4                     tainers (e.g., Cuttingboard → Basket/Cardboardbox, Placemat
             Optimizer                AdamW                      → Plate/Tieredshelf, and Tray → Cardboardbox/Plate/Pot).
             Weight Decay               1e−5                     These tasks require adaptive contact handling and trajectory
             Betas                   [0.9, 0.95]
             Epsilon                    1e−8                     correction under clutter, where LDA shows clear advantages.
             LR Schedule          cosine w/ min lr               While GR00T remains competitive on a small subset of simple
             Min LR                     5e−7                     pick-and-place tasks with minimal environmental interaction,
TABLE V: Model and Training configuration hyperparameters        these cases are limited. Overall, LDAs higher average success
                                                                 rate (55.4 %vs. 47.6 %) reflects a systematic advantage in
                                                                 complex and contact-rich manipulation scenarios rather than
                     A PPENDIX B                                 isolated gains.
 D ETAILED R ESULTS ON THE S IMULATION B ENCHMARK                                      A PPENDIX C
A. Evaluation Setup and Model Description.                             D ETAILS REGARDING REAL - WORLD EXPERIMENT
   All methods are evaluated on the full set of 24 RoboCasa-     A. Real-world Setup.
GR1 [39] tasks, with 51 evaluation trials per task. Unless          We conduct real-world experiments on two humanoid plat-
otherwise specified, models are finetuned using 1,000 demon-     forms: the Galbot G1 and the Unitree G1, as shown in
strations per task and optimized under the same training         Fig.13. The Galbot G1, with two 7-DoF arms, is equipped
paradigm to isolate architectural differences.                   with two interchangeable end-effectors: two-finger parallel-
   We summarize the evaluated models below:                      jaw grippers and 22-DoF SharpaWave dexterous hands. The
   • UWM: A 140M-parameter Unified World Model [60],             Unitree G1 uses 10-DoF BrainCo hands. In all real-robot
      serving as a lightweight baseline.                         configurations, the policy receives visual input only from an
   • UWM-XL: A 1B-parameter UWM variant equipped with            egocentric head-mounted camera, providing a first-person view
      Qwen3-VL [52] for joint language-vision encoding.          of the workspace.
   • UWM+MM-DiT: UWM-L with its DiT backbone re-
      placed by our MM-DiT architecture.                         B. Task description and evaluation protocol.
   • GR00T-N1.6 [40]: The original GR00T policy model              To validate the effectiveness of our method on physical
      without explicit dynamics modeling.                        systems, we evaluate eight representative manipulation tasks
                                                        PnPBottleToCabinetClose                                𝑡




                                                                                                                   𝑡


              Ours




             GR00T


                                                        PnPMilkToMicrowaveClose                                𝑡




                                                                                                                   𝑡


              Ours




             GR00T


                                                         PnPCanToDrawerClose
                                                                                                                   𝑡


              Ours




             GR00T




Fig. 12: Qualitative comparison between our model and GR00T [40] on RoboCasa-GR1 [39] manipulation tasks. Three
representative tasks demonstrate our model’s superior robustness in object grasping and placement accuracy. Critical failure
modes of GR00T, including grasp slippage, misaligned object placement, and collision during manipulation, are highlighted
with circles, while our model consistently achieves successful task completion.


involving single-arm, dual-arm coordination, tool use, and          Performance on Basic Grasping Tasks. In standard Pick
contact-rich interactions. For object generalization, movable    & Place scenarios, LDA achieves a dominant success rate,
objects are randomized within predefined spatial regions while   reaching 90.0% on the ”handover” task, significantly outper-
several supporting objects (e.g., baskets, dustpans, and trash   forming π0.5 [23] (70.0%) and nearly doubling the success rate
bins) remain fixed to isolate task-specific manipulation chal-   of GR00T-N1.6 [40] (50.0%). This indicates that our policy
lenges rather than compounding errors from initial grasp         has learned a more robust grasping primitive and achieve better
failures. All experiments are conducted in-domain, and each      few-shot adaptation on unseen Galbot robot, benefiting from
trial is terminated after 200 seconds if unsuccessful. Task      larger-scale cross-embodiment learning.
success is defined using task-specific criteria such as suc-
cessful object placement, execution of full procedural steps,       Robustness in Contact-Rich and Fine Manipulation.
or normalized scoring metrics for partial completion in long-    The advantages of LDA become increasingly pronounced in
horizon tasks. We evaluate each task over independent trials.    tasks requiring precise dynamic interaction. In Contact-rich
The corresponding training data volume and success criteria      Manipulation, such as ”flip the box,” LDA achieves a 60.0%
for each task are summarized in Table VII.                       success rate compared to just 20.0% for GR00T-N1.6 [40].
                                                                 This suggests that LDA effectively models the complex contact
C. More Analysis.                                                dynamics required to manipulate objects without slippage
  To validate the efficacy of our proposed approach, we          or instability, whereas the baselines likely struggle with the
conducted a comprehensive comparison against two baseline        discontinuous nature of the contact forces. Similarly, in Fine
policies: GR00T-N1.6 [40] and π0.5 [23]. Our method (LDA)        Manipulation tasks like ”pouring,” which demand continuous
demonstrates superior performance across all four evaluated      closed-loop feedback, our method sustains an 80.0% success
categories: Pick & Place, Contact-rich Manipulation, Fine        rate, surpassing the best baseline (π0.5 [23]) by 20 percentage
Manipulation, and Long-horizon Manipulation.                     points.
        model                                         UWM UWM-XL UWM+MMDiT GR00T StarVLA GR00T-EI10k LDA(DiT) LDA
        PnP Bottle To Cabinet Close                    27    41         49        51.5     46        69          65     76
        PnP Can To Drawer Close                        22    53         55         13      80        61          59     71
        PnP Cup To Drawer Close                        18    12         43         8.5     54        47          40     41
        PnP Milk To Microwave Close                    22    25         33         14      48        75          47     52
        PnP Potato To Microwave Close                  16    29         18        41.5     28        41          39     41
        PnP Wine To Cabinet Close                      31    24         25        16.5     46        51          49     57
        PnP Novel From Cuttingboard To Basket           8    18         10         58      48        43          55     65
        PnP Novel From Cuttingboard To Cardboardbox     8    14         16        46.5     40        39          57     69
        PnP Novel From Cuttingboard To Pan             24    20         27        68.5     68        67          65     75
        PnP Novel From Cuttingboard To Pot             16    25         20         65      52        53          57     61
        PnP Novel From Cuttingboard To Tieredbasket    10    10          6        46.5     56        29          39     51
        PnP Novel From Placemat To Basket               8    16         14        58.5     42        45          37     53
        PnP Novel From Placemat To Bowl                12    10         14        57.5     44        55          53     55
        PnP Novel From Placemat To Plate               10    12         10         63      48        57          51     59
        PnP Novel From Placemat To Tieredshelf          2     2          2        28.5     18        20          22     24
        PnP Novel From Plate To Bowl                   12     8         14         57      60        49          57     53
        PnP Novel From Plate To Cardboardbox            2    10          8        43.5     50        61          43     43
        PnP Novel From Plate To Pan                    10    20         16         51      54        51          49     55
        PnP Novel From Plate To Plate                  22    27         25        78.7     70        67          59     61
        PnP Novel From Tray To Cardboardbox            20    25         20        51.5     38        49          59     65
        PnP Novel From Tray To Plate                   12    18         16         71      56        57          57     63
        PnP Novel From Tray To Pot                     18    25         20        64.5     50        63          53     55
        PnP Novel From Tray To Tieredbasket             6    16         16         57      36        55          39     51
        PnP Novel From Tray To Tieredshelf              4     2          4        31.5     16        31          22     33
        Average                                       14.3   19.3      20.0       47.6    47.8       51.3       48.9    55.4

TABLE VI: Results on RoboCasa-GR1 [39] benchmark. UWM-S: UWM [60] with 100M parameters. UWM-L: UWM with 1B
parameters, using Qwen3-VL [52] as the joint encoder for language instructions and visual inputs. UWM-MMDiT: UWM-L
with its DiT [43] backbone replaced by our MM-DiT architecture. QwenGR00T: GR00T [40] equipped with Qwen3-VL as
its System 2 module. GR00T*: GR00T [40] pretrained on our dataset and equipped with Qwen3-VL as its System 2 module.
LDA (DiT): Our LDA model with the MM-DiT replaced by a standard DiT. During finetuning on RoboCasa, the VLM is
unfrozen to enable end-to-end adaptation.


   Capabilities in Long-Horizon Planning. The most striking         DoF hands, LDA already demonstrates strong robustness on
distinction emerges in the Long-horizon Manipulation cate-          tasks involving tool use and force-sensitive interactions. On
gory. While baseline methods achieve moderate success on            Pick Bottle, LDA achieves a 90% success rate, substantially
the relatively simple sweep the table task, they completely fail    higher than π0.5 (20%) and GR00T-N1.6 (75%). On Pull Nail,
on the more complex throw rubbish task, registering a 0.0%          which requires precise force direction and stable contact main-
success rate. In stark contrast, LDA achieves a 35.0% success       tenance, LDA reaches 80% success, while π0.5 completely
rate, demonstrating robustness in multi-stage, temporally ex-       fails and GR00T-N1.6 achieves only 40%. Notably, all meth-
tended scenarios. This performance gap reveals a fundamental        ods perform well on Open Macbook, suggesting that tasks with
limitation of existing approaches: their inability to manage        strong geometric affordances and limited contact ambiguity
compounding errors over long action sequences due to a lack         are less challenging even for baseline policies. The advantage
of explicit dynamics modeling. LDA’s success stems from its         of LDA becomes even more evident with high-DoF hands,
capacity to reason about the physical consequences of actions       where action spaces are larger and control errors accumulate
across time, maintain temporal consistency in latent states,        more easily. On Pick Bread, LDA attains a 70% success rate,
and recover from intermediate deviationscapabilities that are       outperforming GR00T-N1.6 (20%) and π0.5 (10%). The gap
essential for real-world, multi-step manipulation. Crucially,       further widens on Flip Bread, a highly dexterous task requiring
this advantage is rooted in LDAs dynamics-aware architecture,       coordinated finger motion and continuous contact reasoning,
which aligns predicted visual features with underlying physical     where LDA achieves 90% success while both baselines remain
transitions and mitigates covariate shift through structured        at only 10%. These results highlight LDAs superior ability for
temporal modeling. Collectively, these results validate that        high-dimensional control and contact-rich dexterous manipu-
explicitly modeling latent dynamics is not merely beneficial        lation. Unlike baseline methods that rely primarily on reactive
but necessary for reliable, generalizable robotic manipulation      policies, LDA benefits from dynamics-aware latent representa-
in complex, real-world settings.                                    tions that capture fine-grained physical interactions over time.
                                                                    This enables more stable control, improved contact reasoning,
   Capabilities in Dexterous Manipulation. LDA consis-              and effective recovery from transient failurescapabilities that
tently outperforms baselines on both low-DoF and high-DoF           are critical for dexterous manipulation with complex, multi-
hands, with the performance gap becoming more pronounced            DoF robotic hands.
as task difficulty and dexterity requirements increase. For low-
         Task Abbreviation           Description                                          Test Protocol
         Pick Vegetable              Pick a plastic pepper and place it into a basket 10 trials; success if placed in basket
                                     using the left gripper. Pepper is randomized within
                                     a 15×30 cm region.
         Handover                    Left gripper grasps a bottle and passes it to the 10 trials; success if placed in basket
                                     right gripper, which places it into a basket. Bottle
                                     randomized within 15×30 cm.
         Wipe Board                  Use an eraser to remove marker writing from a 10 trials; scored from 0–5 based on
                                     whiteboard. Writing area randomized within 25×40 cleaning completeness
                                     cm.
         Flip Box                    Flip an upside-down storage box to upright us- 10 trials; success if fully flipped
                                     ing bimanual manipulation. Box randomized within
                                     2×4 cm.
         Water Flower (pouring)      grasp a watering bottle and pour water into a flower 10 trials; success if pouring posture
                                     pot. Pot randomized within 15×15 cm.                 is achieved with spout above pot
         Knock the block with grasp a hammer with a very thin handle and 60 trials; only if both the grasp and
         hammer (pnp2)        then knock the specific block. Hammer randomized knock succeed.
                              within 15×15 cm.
         Sweep Table                 Sweep ten nails into a dustpan using a broom and 10 trials; success rate is computed as
                                     dustpan. Nail positions randomized within 10×25 the proportion of nails collected in the
                                     cm.                                              dustpan.
         Throw Rubbish               Pick paper balls, place them into a dustpan, and 10 trials; success rate is computed as
                                     dump them into a trash can. Paper balls are ran- the proportion of paper balls success-
                                     domized within a 20×25 cm area.                  fully dumped into the trash can.

TABLE VII: Real-world gripper manipulation for Galbot task configurations. All tasks are evaluated in-domain with a timeout
of 200 seconds per trial.




            Task                  Description                                          Test Protocol
            Abbreviation
            Pick Bottle           Pick up a plastic bottle and place it onto a fixed 20 trials; success if bottle is upright
                                  target region using the right hand. Bottle position and its base overlaps at least half of
                                  is randomized.                                      the target region
            Open MacBook          Left hand stabilizes the base while the right hand 20 trials; success if opening angle
                                  opens the hinge by pushing the upper edge. Initial exceeds 75% of maximum
                                  opening angle is randomized.
            Pull Nail             Use a claw hammer held by the right hand to 10 trials; scored with partial credit:
                                  extract a nail from the surface. Hammer pose is 0.25 for locating, 0.5 for single-claw
                                  randomized.                                     removal, 1.0 for full claw removal
            Pick Bread            Pick a bread item and place it into a plate using the 10 trials; success if bread is placed
                                  right hand. Three bread types are used with equal into the plate
                                  distribution.
            Flip Bread            Flip a long bread using a spatula held by the right 10 trials; 1.0 if flipped on first at-
                                  hand. Bread pose is randomized over a large region. tempt, 0.5 if second, 0 otherwise

                          TABLE VIII: Dexterous hand manipulation tasks and evaluation protocols.
Fig. 13: Real-world robot platforms used in our physical experiments. From left to right: (1) Galbot G1 equipped with a
standard two-finger parallel gripper for basic grasping tasks; (2) Galbot G1 fitted with the SharpaWave dexterous hand (22
DoF) for fine manipulation; (3) Unitree G1 mounted with the BrainCo dexterous hand (10 DoF) and a Zed Mini camera.
This multi-platform setup demonstrates the generalization capability of our LDA model across diverse robot morphologies and
end-effectors.


                         A PPENDIX D                                      def __init__(self, dataset: str, eef_in_world:
                     D ETAILS OF EI-30 K .                                int, has_mano: bool):
                                                                              self.dataset = dataset
A. Data Processing Pipeline for Robot and Human Datasets                      self.eef_in_world = eef_in_world
                                                                              # 1 if wrist in world coordinates
   To ensure consistency and usability across heterogeneous                   self.has_mano = has_mano
robot and human datasets, we design a standardized data                       self.eef_offset = {hand: np.eye(4) for hand
                                                                              in HAND_KEYS}
processing pipeline that converts raw recordings into a unified               self.eef_keys = HAND_KEYS
representation suitable for effective learning of both policy and
dynamics. The pipeline consists of three main stages: dataset             def get_wrist(self, df: pd.DataFrame) ->
                                                                          dict[str, np.ndarray]:
standardization, coordinate alignment and cleaning, and post-                 pass
processing for training.
     a) Dataset Standardization: All raw datasets are first               def get_mano_or_gripper(self, df: pd.DataFrame):
                                                                              pass
converted into the common LeRobot [8] 2.1 format. This
format includes:
                                                                         b) Coordinate Alignment and Data Cleaning: Human
   • End-effector poses: 6D position and orientation for both       and robot datasets often employ inconsistent coordinate frame
     hands (human) or manipulators (robot);                         definitions. To unify them, particularly the end-effector (EEF)
   • Hand articulation: 21-point MANO keypoints for hu-             representations, we apply the following alignment and clean-
     man hands (when available) and binary or continuous            ing steps:
     gripper states for robots;
                                                                      • End-effector coordinate alignment: For each dataset,
   • Camera parameters: intrinsic and extrinsic matrices
                                                                        we define a canonical EEF frame (e.g., at the wrist
     enabling reprojection across coordinate frames;
                                                                        or gripper center). All recorded hand or manipulator
   • Task and temporal metadata: task identifiers, episode
                                                                        poses are transformed into this common frame using a
     boundaries and timestamps.
                                                                        dataset-specific rigid offset, estimated through geometric
   During this stage, all sequences are uniformly resampled to          inspection or visual validation.
10 Hz, and structured metadata files are generated to preserve        • Camera motion decoupling: For sequences captured in
the alignment between frames and their semantic annotations,            a moving camera frame, hand trajectories are reprojected
ensuring temporal coherence and task-aware data organization            into a fixed world coordinate system to eliminate artifacts
for downstream training.                                                caused by camera motion.
   After standardization of LeRobot format, we implement              • Keypoint standardization: Human hand poses without
an easy-to-use Dataset class for the following data process             native MANO keypoints are converted into the standard
pipeline to harmonize heterogeneous action data across diverse          21-point MANO representation, expressed relative to the
datasets.                                                               aligned wrist frame.
class EmbodiedDataset:                                                • Data validation: Hand visibility is verified using an off-
Fig. 14: Task descriptions for the Galbot G1 robot equipped with a standard two-finger parallel-jaw gripper, spanning four
manipulation categories.


      the-shelf detector; frames with occluded, truncated, or         Data Type          Source / Sub-dataset     Duration (h)
      kinematically invalid hand data are discarded to ensure
                                                                                       Open X-Embodiment [12]         3000
      annotation reliability.
                                                                                       Agibot World [6]               3276
   For robot datasets, we further normalize actuation signals:                         RoboMIND [50]                  305
gripper widths are scaled to a consistent range (e.g., [0, 1]), and   Real-world Robot Humanoid Everyday [57]          30
joint encodings are harmonized to match a unified kinematic                            RoboCOIN [51]                  500
convention.                                                                            Galaxea [48]                   500
      c) Data Cleaning: Textual annotations are unified into                           LET [28]                       1000
a structured format that explicitly describes the environmental                          InternData-A1 [11]           7433
context, per-hand actions (left/right), and high-level task objec-    Simulated Robot
                                                                                         Behavior-1k [29]             1200
tives. When original annotations are inconsistent or missing,
we leverage vision-language models to generate coherent, se-                             Ego4D [18]                   3670
mantically aligned instructions. Finally, all processed datasets                         Epic-Kitchens [13]           100
are organized by agent type (human or robot) and accompanied                             Ego-Exo4d [19]               1286
                                                                                         SSV2 [17]                     240
by comprehensive metadata files detailing task definitions,
                                                                                         EgoDex [21]                  830
episode boundaries, and dataset statistics. This standardized         Ego Human          HOT3D [2]                      16
pipeline ensures a consistent, interoperable data representation      (w/ Action)        HoloAssist [49]              166
across domainsenabling robust, scalable training of dexterous                            OAKINK2 [54]                  6.5
manipulation policies that generalize across embodiment and                              TACO [33]                     3.2
task complexity.                                                                         HOI4D [34]                    7.6
                                                                                         ARCTIC [15]                   2.3
B. Data Composition.
   Our training data spans four complementary categories,             Ego Human          Egocentric-10k [1]           10000
                                                                                         RH20T-human [16]              100
totaling more than 30,000 hours of egocentric experience:             (Actionless)
                                                                                         Egome [44]                     80
      a) Real-world Robot Data : This category includes large-
                                                                                         Taste-Rob [55]                130
scale physical robot execution logs. We primarily leverage
Open X-Embodiment [12] and Agibot World [6] for general-                                 Total                        30k+
purpose manipulation. To enhance hardware-specific capabili-
ties, we incorporate Humanoid Everyday [57] for bipedal loco-         TABLE IX: Composition of the Embodied Interaction Dataset
motion dynamics and Galaxea [48] for high-fidelity dexterous          (EI-30K). The dataset is categorized into four main types,
tasks. Additionally, we include RoboCOIN [51] despite its             aggregating over 30k hours of data.
                                                                     Fig. 16: DINO Feature Prediction Visualization. Left column:
                                                                     Original RGB input images. Middle column: Ground-truth
                                                                     DINO features extracted by DINOv3 [46]. Right column:
                                                                     DINO features predicted by our model.

                                                                     these trajectories lack explicit action labels, they provide a
                                                                     powerful self-supervised signal for learning world dynamics,
                                                                     visual affordances, and temporal structure.

                                                                                            A PPENDIX E
                                                                                  D ETAILS OF OTHER E XPERIMENTS
Fig. 15: Dexterous manipulation task description across two          A. Action-Conditioned Attention Visualization.
robotic platforms. Top three rows: Unitree robot equipped
with BrainCo hands performing bottle placement, MacBook                 We provide additional details on how action-conditioned
opening, and nail extraction. Bottom two rows: Galbot robot          attention maps are computed and interpreted. Our visualization
utilizing SharpaWave hands executing bread placement and             is based on the Diffusion Transformer (DiT) [43] backbone,
flipping tasks.                                                      where visual tokens and action embeddings interact through
                                                                     shared self-attention layers.
                                                                        For a given observation, we extract attention maps from
noisier action labels, as it provides valuable diverse environ-      the middle transformer blocks, where high-level semantic and
ment explorations.                                                   geometric information is most prominent. Conditioned on an
      b) Simulated Robot Data: To provide dense, noise-free          active action primitive (e.g., “Push Right”), we compute the
supervision, we use high-quality simulated trajectories. The         attention weights A1 , which quantify the influence of each
majority comes from InternData-A1 [11], which offers large-          spatial token on the predicted latent transition. To establish a
scale automated generation of locomotion and basic manip-            reference, we generate a baseline attention map A2 by replac-
ulation sequences. Behavior-1k [29] further contributes long-        ing the action embedding with a No-Op (static) command.
horizon task demonstrations in simulated household environ-             We then compute the absolute difference:
ments, enabling the model to learn complex task hierarchies.
                                                                                           ∆A = |A1 − A2 |,
      c) Egocentric Human Data with Actions: This sub-
set bridges human intent and robot-executable actions. We            which isolates attention changes induced purely by the action
draw from large-scale datasets such as Ego4D [18] , Epic-            condition. This subtraction effectively removes generic visual
Kitchens [13] , Ego-Exo4d [19] and SSV2 [17] focusing                saliency (e.g., high-contrast edges or background objects) and
on object-interaction segments. High-precision sources like          highlights regions whose relevance emerges only when a
EgoDex [21] and HOT3D [2] provide fine-grained 3D hand               specific action is applied.
poses and contact information, critical for learning extrinsic          As illustrated in Fig. 11, the resulting difference maps con-
dexterity.                                                           sistently emphasize contact regions, force application points,
      d) Egocentric Human Data without Actions: Represent-           and anticipated motion trajectories. For example, in the “Push
ing the largest source of visual diversity, this category consists   Right” task, attention shifts toward the gripperobject contact
of first-person observations. Egocentric-10k [1] serves as the       interface and the direction of expected displacement. This
primary source, covering a broad spectrum of daily activi-           behavior demonstrates that the DiT dynamically re-weights
ties. Additional datasets like RH20T-human [16] and Taste-           visual tokens based on the physics implied by the action, rather
Rob [55] contribute domain-specific visual priors. Although          than passively encoding static appearance.
B. Visualization of Latent Forward Dynamics
   We provide additional qualitative visualizations to illustrate
the forward dynamics learned by LDA. These qualitative
results complement the quantitative analysis and provide fur-
ther evidence that LDA learns structured, dynamics-aware
latent representations suitable for long-horizon reasoning and
control.
