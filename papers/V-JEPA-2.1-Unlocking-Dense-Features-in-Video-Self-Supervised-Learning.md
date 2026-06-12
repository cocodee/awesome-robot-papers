| V-JEPA          | 2.1: Unlocking |          | Dense | Features | in Video |
| --------------- | -------------- | -------- | ----- | -------- | -------- |
| Self-Supervised |                | Learning |       |          |          |
LorenzoMur-Labadia1,2, , MatthewMuckley1, AmirBar1, MidoAssran1, KoustuvSinha1, MikeRabbat1,
∗
| YannLeCun1, | NicolasBallas1,    | , AdrienBardes1, |     |     |     |
| ----------- | ------------------ | ---------------- | --- | --- | --- |
|             |                    | †                | †   |     |     |
| 1FAIR at    | Meta, 2Universidad | de Zaragoza      |     |     |     |
| ∗Work       | Meta, †Joint       |                  |     |     |     |
| done        | at                 | last author      |     |     |     |
Wepresent ,afamilyofself-supervisedmodelsthatlearnsdense,high-qualityrepresentations
V-JEPA2.1
forvisualscenesinbothimagesandvideos,whileretainingstrongglobal sceneunderstanding. V-JEPA
2.1 combines four key ingredients: (i) a , a masking-based objective in which
6202 raM 71  ]VC.sc[  2v28441.3062:viXra DensePredictiveLoss
tokens—visible context and masked tokens alike—contribute to the training loss, encouraging
all
explicit spatial and temporal grounding; (ii) , which applies the self-supervised
DeepSelf-Supervision
objective hierarchically at multiple intermediate encoder layers to improve representation quality ;
(iii) Multi-ModalTokenizers that support unified training over images and videos; and (iv) effective
. These design choices substantially improve dense feature quality, yielding
modelanddatascaling
representations that are spatially structured, semantically coherent, and temporally consistent. .
Empirically, V-JEPA 2.1 achieves state-of-the-art results on a range of benchmarks: 7.71 mAP on
Ego4D for short-term object-interaction anticipation, 40.8 Recall@5 on EPIC-KITCHENS for high-
level action anticipation, and a 20% improvement in real-robot grasping success rate over VJEPA-2
AC. The model also demonstrates state-of-art performances in robotic navigation (5.687 ATE on
Tartan Drive), depth estimation (0.307 RMSE on NYUv2 with a linear probe), and global recognition
(77.7% on Something-Something-V2). Our results demonstrate that V-JEPA 2.1 advances the state of
| the art in  | dense visual understanding | and              | world modeling. |     |     |
| ----------- | -------------------------- | ---------------- | --------------- | --- | --- |
| Date: March | 18, 2026                   |                  |                 |     |     |
|             | lmur@unizar.es,            | abardes@meta.com |                 |     |     |
Correspondence:
Code: https://github.com/facebookresearch/vjepa2
oediV/egamI
2APEJ-V
1.2APEJ-V
Figure1 V-JEPA2.1unlockshigh-qualitydensefeatures. We compute PCA on patch features extracted from the same
image or video and map the top three components to RGB channels for both V-JEPA 2 (ViT-g) and V-JEPA 2.1
(ViT-G). Our novel V-JEPA 2.1 produces dense representations with strong spatial and temporal consistency, learning
semantically coherent features where similar objects map to the same PCA components.
1

V-JEPA2 V-JEPA2.1 PreviousSOTAusingfrozenbackbone
87.387.789.4 85.185.588.1
7.71 77.377.7
+35%
69.071.1 71.1
.642 6.02 +31%
5.67 52.5 54.8
47.9
+52%
39.740.8
.307.309 +96%
27.6
24.4
NYUv2Depth Ego4DShortTerm DAVISObject ADE20KSemantic SSv2Action EKAction K400Action IN1KImage
Estimation() Anticipation Tracking Segmentation Recognition Anticipation Recognition Classification
↓
Densetasks Globaltasks
Figure2 V-JEPA2.1ViT-Gperformanceacrossdenseandglobalpredictiontasks. We show the relative improvements of
V-JEPA 2.1 compared to the previous V-JEPA 2 ViT-g model (Assran et al., 2025). We also report the performance
of previous SOTA models using a frozen backbone evaluation: DINOv3 (Siméoni et al., 2025) is the reference model
for depth estimation, object tracking, semantic segmentation, SSv2 action recognition, and image classification;
InternVideo2s (Wang et al., 2024b) for K400 action recognition, STAformer (Mur-Labadia et al., 2024) for short-term
object interaction anticipation, and PlausiVL (Mittal et al., 2024) for action anticipation. Tasks where V-JEPA 2.1
ViT-G obtains SOTA in frozen-backbone evaluation are underlined.
1 Introduction
World models hold the promise of enabling agents to perceive, predict, and plan effectively in the physical
world (Sutton, 1981; Ha and Schmidhuber, 2018; Assran et al., 2023). At the core of these models lies the
state-estimation problem: learning representations that reliably summarize the current world state from
low-level, noisy perceptual inputs. Self-Supervised Learning (SSL) from video has recently emerged as a
powerfulroutetothisgoal(Caronetal.,2021;Assranetal.,2025),becauseitcanexploitlarge-scale,label-free
datatolearnrepresentationsthatcapturescenegeometry,dynamics,andintrinsicphysicalproperties(Siméoni
et al., 2025; Garrido et al., 2025).
Despite rapid progress, learning representations that simultaneously preserve dense spatio-temporal structure
(needed for localization, geometry, and tracking) while also capturing dynamics and supporting global
understanding (needed for high-level recognition) remains an open challenge. Among recent advances, Joint
Embedding Predictive Architectures (JEPA) (LeCun, 2022)—and in particular the V-JEPA family (Bardes
et al., 2024; Assran et al., 2025)—have demonstrated strong global video understanding, especially in settings
that require modeling motion and dynamics, and have shown promise for enabling prediction and planning
in embodied agents (Assran et al., 2025). However, as illustrated in Figure 1, their learned representations
can be less amenable to extracting fine-grained local spatial structure. In contrast, other SSL approaches
such as DINO (Caron et al., 2021; Oquab et al., 2023; Siméoni et al., 2025) yield high-quality dense features
for detection and segmentation, but are primarily image-based and therefore do not directly learn temporal
dynamics from video.
Inthiswork,westudyself-supervisedlearningwithalatentmask-denoisingobjective,wherethemodelpredicts
masked segments of an image or video directly in a learned representation space. Our central finding is that
high-quality dense spatio-temporal features—preserving fine-grained spatial layout and motion dynamics—do
not emerge reliably when the prediction loss is applied only to masked regions. Instead, extending the
predictive loss to the entire input, both masked and unmasked segments, substantially improves the low-level
(dense) representations.
Building on this insight, we introduce , a self-supervised approach for learning unified image and
V-JEPA2.1
video representations. V-JEPA 2.1 uses a dense predictive loss applied to all tokens (both visible context
and masked tokens), grounding each token in its spatio-temporal location and preventing visible tokens from
acting as global aggregators—an effect that is key to improving dense feature quality (Figure 3). Additionally,
we find that deep self-supervision—applying the loss hierarchically at multiple intermediate encoder layers to
2

providetrainingsignalsthroughoutthenetwork—yieldsconsistentgainsonbothdenseandglobaldownstream
tasks. To enable native joint training across modalities, we use modality-specific learned tokenizers for images
and videos within a single shared encoder. Finally, we show these improvements scale with data and model
capacity: expanding the image component from 1M to 142M images using VisionMix-163M and scaling the
model from 300M to 2B parameters leads to systematic downstream gains.
We train and release a suite of V-JEPA 2.1 models (ViT-g/G, 1B/2B), along with two distilled, smaller
variants (ViT-B/L, 80M/300M). Empirically, V-JEPA 2.1 achieves state-of-the-art performance on predictive
video benchmarks spanning both fine-grained and semantic forecasting: it reaches 7.71 mAP on Ego4D
short-term object-interaction anticipation, which requires predicting where and when interactions will occur
(localized interaction regions and time-to-interaction), and 40.8 Recall@5 on EPIC-KITCHENS-100 action
anticipation, which evaluates the ability to forecast upcoming actions from partial temporal context.
We further show that better dense-features also improves performances on world modelling tasks. V-JEPA 2.1
dense-features leads to +20% success rate compared to VJEPA-2 AC (Assran et al., 2025) on grasping when
when deploy our model on real Franka arms in new environment zero-shot. V-JEPA 2.1 is also suitable for
robot navigation where it achieves state-of-art performances (5.687 ATE on Tartan Drive) while having 10x
faster planning speed compared to previous work (Bar et al., 2025).
Beyond prediction and planning, V-JEPA 2.1 also delivers strong performance in both dense and global
understandingtasks. Fordensetasks, V-JEPA2.1ViT-Gsetsanewstateoftheartinlinear-probemonocular
depth estimation (0.307 RMSE on NYUv2), achieves competitive linear-probe semantic segmentation (85.0
mIoUonPascalVOC),andproducestemporallyconsistentfeaturesforvideoobjectsegmentation(72.7J&F-
Mean on YouTube-VOS). At the global level, it also attains state-of-the-art accuracy in action recognition
(77.7% on Something-Something-v2) and achieves competitive performances in Video Question Answering
(VQA) tasks (83.1 accuracy on PerceptionTest).
We hope that these contributions will foster research in learning strong representations for physical world
modelling, while empowering many applications in video understanding. We make our code and pretrained
models publicly available to facilitate further research and applications.
2 Methodology
2.1 Preliminaries: Joint-EmbeddingPredictiveArchitectures
Joint-Embedding Predictive Architecture (JEPA) (LeCun, 2022) is a self-supervised learning framework
designed to learn representations of data by making predictions in a learned latent space, rather than directly
in the observation (input) space. JEPA models operate by encoding both a noise-corrupted version and an
uncorrupted(clean)versionofthesameinput. Apredictornetworkisthentrainedtopredicttherepresentation
of the clean input from the representation of the corrupted input.
Corrupted and clean inputs are processed by the encoder E (·), which produces latent representations. The
θ
predictor, P (·), is then used to map the representation of the corrupted input to the representation of the
ϕ
clean input. Given that the encoder and predictor are learned simultaneously, the system admits a trivial and
uninformative solution in which the encoder E (·) outputs a constant vector regardless of its input. To avoid
θ
this representation collapse, explicit (Bardes et al., 2021; Balestriero and LeCun, 2025; Mo and Tong, 2024)
or implicit (Grill et al., 2020a; Assran et al., 2023) regularization is used to promote representations that
preserve input information.
In this work, we build upon the V-JEPA family of models, where video representations are learned through a
mask-denoising objective in the representation space (Bardes et al., 2024; Assran et al., 2025). The V-JEPA
objective aims to predict the representation of a video y from another view x of that video that has been
corruptedthroughmasking,i.e.,fromwhichpatcheshavebeenrandomlydropped. TheencoderE (·)processes
θ
the masked video x, and outputs an embedding vector, or context tokens, for each visible patch. The outputs
of the encoder are concatenated with a set of learnable mask tokens ∆ that specify the spatio-temporal
y
position of the masked patches. The predictor network processes the combined tokens sequence, and outputs
an embedding vector for each input token. The encoder and predictor are trained by minimizing the following
3

objective:
|     |     |     |     |         | 1   | (cid:88) |          |     |       |        |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | -------- | -------- | --- | ----- | ------ | --- | --- | --- | --- |
|     |     |     |     | L       | =   | ∥P       | (E (x),∆ | )   | −sg(E | (y) )∥ | ,   |     |     | (1) |
|     |     |     |     | predict |     | ϕ        | θ        | y i |       | θ i    | 1   |     |     |     |
|M|
i M
∈
where is a set containing the masked patch indexes from the view. The loss use a stop-gradient operator,
| M   |     |     |     |     |     |     |     | x   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sg, to prevent representation collapse (Grill et al., 2020b) and an exponential moving average θ of θ is used to
update the weight of the encoder processing the video y. is only applied on masked tokens, and
|     |     |     |     | E   | (y) |     |     | L   | predict |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
θ
| not on | the context | tokens. |     |     |     |     |     |     |     |     |     |     |     |     |
| ------ | ----------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Both encoder and predictor are parametrized with Vision Transformer (Dosovitskiy, 2020) and we
|     |     | E θ (·) |     | P   | ϕ (·) |     |     |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
rely on the same masking strategy as Assran et al. (2025). Refer to Appendix A for more details.
2.2 AnalysisofV-JEPAFeaturesforDenseVisionTasks
While V-JEPA has proven to be an effective approach for understanding global semantic information from
video, predicting future actions, and planning to reach specific goals (Bardes et al., 2024; Assran et al., 2025),
previous works have not investigated the suitability of V-JEPA 2 features for dense vision tasks. To address
this gap, we analyze the V-JEPA 2 feature maps through qualitative visualizations and dense downstream
tasks evaluation.
For the qualitative visualizations, we compute the Principal Component Analysis (PCA) of patch features
extracted from the V-JEPA 2 encoder, and we map the first three components to the RGB color channels.
We assess the encoder performance on dense tasks using a linear probing protocol, in which we train a single
linear layer on top of the frozen encoder features. We evaluate V-JEPA 2 on semantic segmentation using the
ADE20K dataset (Zhou et al., 2017a) and depth estimation on NYUv2 (Silberman et al., 2012b). Refer to
| Appendix | C   | for more | details | on the | evaluation | setup. |     |     |     |     |     |     |     |     |
| -------- | --- | -------- | ------- | ------ | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Featuremapvi-
| Observations  |           | and         | Hypothesis.  |               |              |            |       |     |     |     |     |     |     |     |
| ------------- | --------- | ----------- | ------------ | ------------- | ------------ | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
| sualizations  | of        | V-JEPA      | 2 are        | shown         | in Figure    | 1 and      |       |     |     |     |     |     |     |     |
| Figure        | 3. We     | observe     | that feature |               | maps         | are noisy  | egamI |     |     |     |     |     |     |     |
| and show      | only      | fragmented  |              | local spatial |              | structure. |       |     |     |     |     |     |     |     |
| Additionally, |           | V-JEPA      | 2 features   | obtain        | limited      | per-       |       |     |     |     |     |     |     |     |
| formance      | on        | dense tasks | when         | using         | a simple     | linear     |       |     |     |     |     |     |     |     |
| probing       | protocol, | such        | as semantic  |               | segmentation |            |       |     |     |     |     |     |     |     |
2
| (22.2 mIoU | on  | ADE20K) | or depth | estimation |     | (0.682 |     |     |     |     |     |     |     |     |
| ---------- | --- | ------- | -------- | ---------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
APEJ-V
| RMSE        | on NYUv2), |            | as reported | in                | Table  | 1. Over-   |     |     |     |     |     |     |     |     |
| ----------- | ---------- | ---------- | ----------- | ----------------- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
| all, these  | results    | support    | the         | conclusion        |        | that local |     |     |     |     |     |     |     |     |
| information | about      | the        | visual      | scene             | is not | easily ex- |     |     |     |     |     |     |     |     |
| tractable   | from       | the V-JEPA |             | 2 representation. |        |            |     |     |     |     |     |     |     |     |
Wehypothesizethattheabsenceoflocalstructurein
xtc
thefeaturemapsisduetothelackofself-supervision
L+
| on patches | that | are       | not masked, |       | i.e. the | context  |     |     |     |     |     |     |     |     |
| ---------- | ---- | --------- | ----------- | ----- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| patches.   | The  | predictor |             | takes | as input | the con- |     |     |     |     |     |     |     |     |
P ϕ (·)
| catenationofcontexttokenscomputedbyE |     |     |     |     |     | (x)and |     |     |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
θ
| asetofmasktokens∆ |     |      | thatspecifythemaskedposi-  |     |     |     |                |                            |     |             |     |                 |         |         |
| ----------------- | --- | ---- | -------------------------- | --- | --- | --- | -------------- | -------------------------- | --- | ----------- | --- | --------------- | ------- | ------- |
|                   |     |      | y                          |     |     |     | Figure3        | InfluenceofthecontextlossL |     |             |     | ctx.            | We show | PCA     |
| tionstopredict.   |     | Thep | redictoroutputsonetokenfor |     |     |     |                |                            |     |             |     |                 |         |         |
|                   |     |      |                            |     |     |     | visualizations |                            | of  | the feature | map | representations |         | learned |
eachinput, i.e., forbothcontextandmaskedtokens. with V-JEPA 2 and with a model trained using V-JEPA
| However, | the | original | loss from | V-JEPA |     | 2 (Assran |        |     |             |       |        |          |      |      |
| -------- | --- | -------- | --------- | ------ | --- | --------- | ------ | --- | ----------- | ----- | ------ | -------- | ---- | ---- |
|          |     |          |           |        |     |           | 2 plus | our | L ctx loss. | While | V-JEPA | features | only | show |
et al., 2025) is applied only to the masked tokens, fragmented local spatial structure, explicitly supervising
as Equation 1 shows. Therefore, the model has unmasked regions with L leads to feature maps that
ctx
no incentive to encode local information within the exhibit coherent spatial structure. Similar semantic parts
|     |     |     |     |     |     |     | (e.g., | heads | of dogs, | wheels | of cars) | are mapped |     | to the |
| --- | --- | --- | --- | --- | --- | --- | ------ | ----- | -------- | ------ | -------- | ---------- | --- | ------ |
contexttokensandcaninsteaddevotethiscomputa-
| tion to | aggregating | global | information |     | to  | minimize | same | PCA | components. |     |     |     |     |     |
| ------- | ----------- | ------ | ----------- | --- | --- | -------- | ---- | --- | ----------- | --- | --- | --- | --- | --- |
,similarlytoregistertokens(Darcetetal.,
L
prediction
2023).
4

Figure 4 V-JEPA 2.1 Detailed Architecture. Images and videos are processed by respectively either a 2D or 3D
Convolutional patch embedding. Then, 3D Rotational Positional Encoding (RoPE) and learnable modality embedding
areadded. Thex−encoderprocessesthevisibletokensandoutputsmulti-levelembeddingsformedbyconcatenatingthe
normalizedoutputfromintermediateencoderblocks. Then,aMLPfusesthismulti-levelrepresentationandreducesits
dimensionality. These context tokens are concatenated with learnable mask tokens carrying spatio-temporal positional
information. The predictor processes the combined sequence and produces multi-level predictions for the masked
tokens. Training uses two different losses: (i) an L1 loss on masked-token predictions (the original V-JEPA objective),
and(ii)adistance-weightedL1lossonnearbycontexttokens,bothsupervisedusingthey-encodermulti-leveloutputs.
Context Self-Supervision. To verify this hypothesis, we propose to self-supervise both the mask and
context patches and introduce a context loss L , which is a weighted version of L applied on the
ctx predict
context tokens:
1 (cid:88)
L = λ ∥P (E (x),∆ ) −sg(E (y) )∥ , (2)
context |C| i ϕ θ y i θ i 1
i C
∈
where C is the set of indexed context tokens, and λ is a patch-specific weighting parameter described in
i
the next section. The model is trained to minimize L +L . Figure 3 shows that adding L has a
predict ctx ctx
significant effect on the learned feature maps. With the context loss, local structure now clearly appears in
the feature maps, and similar semantic parts (e.g., head of the dogs, wheel of the car) are mapped to the same
PCA components. Additionally, adding L significantly improves performance on dense-prediction tasks,
ctx
achieving 33.9 mIoU on ADE20K (up from 22.2), and 0.473 RMSE on NYUv2 (down from 0.682). Hence,
those results validate that by explicitly supervising context tokens, the model learns features that encode
coherent local structure.
2.3 V-JEPA2.1: ImprovingDenseVideoSSLFeatures
Building on the previous observation, we introduce V-JEPA 2.1, a self-supervised training recipe for learning
representations that combine high-quality dense local features with global semantic understanding. Our
key algorithmic innovations are (1) Dense Prediction loss that applies self-supervision on both masked and
unmasked tokens (Section 2.3.1) and, (2) Deep Self-Supervision of the encoder intermediate layers via a
multi-level predictor (Section 2.3.2). Additionally, we explore (3) a Multi-Modal Tokenizer with modality-
specific patch embeddings for images and videos (Section 2.3.4); (4) Data Scaling through a more diverse
and balanced image–video training distribution (Section 2.3.3); and Model Scaling to ViT-G (Section 2.3.5),
enabling state-of-the-art downstream performance and effective distillation to smaller models (ViT-L, ViT-B,
Section 3.10).
5

|     | 50  |     |     |     |     |     | 80  |
| --- | --- | --- | --- | --- | --- | --- | --- |
47.1 47.9
|     |     | Segmentation(ADE20k) |     |     |      |     | 77.7 78 |
| --- | --- | -------------------- | --- | --- | ---- | --- | ------- |
|     |     | Classification(SSv2) |     |     | 76.1 |     |         |
|     | 45  |                      |     |     |      |     | 76      |
41.4
40.8
|     | )k02EDA(UoIm 40 72.8 |     | 38.6 | 72.6 | 72.6 |     | 74     |
| --- | -------------------- | --- | ---- | ---- | ---- | --- | ------ |
|     |                      |     | 72.1 |      |      |     | )2vSS( |
72
|     | 35  | 33.8 |     |     |     |     | 70      |
| --- | --- | ---- | --- | --- | --- | --- | ------- |
|     |     |      |     |     |     |     | 68 .ccA |
|     | 30  |      |     |     |     |     | 66      |
|     | 25  | 62.5 |     |     |     |     | 64      |
22.2
62
|     | 20  |      |                   |         |                |           | 60  |
| --- | --- | ---- | ----------------- | ------- | -------------- | --------- | --- |
|     | 2   | Loss | Self-Supervision. | Scaling | Patch. Scaling | Annealing |     |
V-JEPA
Context
|     |     |     |     | Data | modal Model |     |     |
| --- | --- | --- | --- | ---- | ----------- | --- | --- |
High-Res.
|     |     | +    |     | + Multi |     |     |     |
| --- | --- | ---- | --- | ------- | --- | --- | --- |
|     |     | Deep |     |         | +   |     |     |
+
+
+
Figure5 ImpactofindividualcomponentsofournovelV-JEPA2.1trainingrecipe. The ablation is conducted starting from a
ViT-L architecture, on single-image semantic segmentation on ADE20k, and action classification on SSv2. Introducing
Weighted-ContextSelf-Supervision withthecontextlosssignificantlyimprovessegmentation,atthecostofclassification.
Deep Self-Supervision allows to retrieve the performance, and further improving segmentation. Scaling the image data
with VisionMix 163M dataset, combined with a Multi-Modal Tokenizer further improve the results. Finally, the recipe
| scales with | model size and | high resolution | cool-down. |     |     |     |     |
| ----------- | -------------- | --------------- | ---------- | --- | --- | --- | --- |
VJEPA 2.1 Architecture. We illustrate the V-JEPA 2.1 architecture in Figure 4. An input, either an
image or a video, is projected into a sequence of embedding vectors, or tokens, using a modality-specific
patch embedding. Mask corruption is then applied to the sequence by randomly dropping patch tokens. The
x-encoder processes the remaining visible context tokens and outputs representations from multiple encoder
levels in addition to the final output. The multi-level representations are then concatenated along the channel
axis and fed to an MLP to reduce their dimensionality. Context tokens are concatenated, along the sequence
axis, with learnable mask tokens that carry spatio-temporal positional information of the masked patches.
The predictor processes the combined sequence and produces multi-level predictions for each token. Training
uses two different losses: (i) an L1 loss on masked-token predictions (the original V-JEPA objective), and (ii)
a distance-weighted L1 loss for context tokens. Both use the y-encoder outputs as targets, which process the
unmasked sequence of patches from the input images or videos. Losses are applied to several intermediate
| representation | levels in | addition to | the encoder | output. |     |     |     |
| -------------- | --------- | ----------- | ----------- | ------- | --- | --- | --- |
We follow the warmup-constant learning rate schedule of V-JEPA 2 and we
| Implementation | Details. |     |     |     |     |     |     |
| -------------- | -------- | --- | --- | --- | --- | --- | --- |
train models for 135,000 iterations. We maintain the teacher EMA coefficient and weight decay at fixed values.
Each video sample is a clip of 16 frames at a resolution of 256×256, and each image sample has a resolution
of 256×256. Additionally, in a second stage we explore the effect of applying a cool-down phase, i.e., decaying
the learning rate and increasing the input images and videos resolution. We further train our models for
12,000 iterations during this cool-down phase, increasing the input resolution: video clips now have 64 frames
at a resolution of 384×384, and images have a resolution of 512×512. Ablation results are reported after the
first training phase, whereas final downstream tasks results use the full warmup–constant–cooldown schedule.
| More details | and all hyper-parameters |     | are provided | in Appendix | A.  |     |     |
| ------------ | ------------------------ | --- | ------------ | ----------- | --- | --- | --- |
To evaluate our design choice, we rely on a set of dense-vision tasks (ADE20K and
| Empirical | Evaluation. |     |     |     |     |     |     |
| --------- | ----------- | --- | --- | --- | --- | --- | --- |
NYUv2) using a linear probing evaluation protocol following Siméoni et al. (2025) and global recognition
tasks (Something-Somethingv2 for action recognition and ImageNet for object recognition) with an attentive
probing protocol following Assran et al. (2025). We ablate the effect of each architecture component in
Figure 5 and Table 1. In the following, we describe each component in more detail, as well as their impact on
| downstream | performance. |     |     |     |     |     |     |
| ---------- | ------------ | --- | --- | --- | --- | --- | --- |
6

Table1 ImpactofindividualcomponentsofournovelV-JEPA Table2 Impactofthecontextlossweightingscheme. Results
2.1trainingrecipe. Results on image classification (IN1K), on semantic segmentation (ADE20K) and video classifi-
video classification (SSv2), depth estimation (NYU), and cation (SSv2). Introducing the context loss with a fixed
semantic segmentation (ADE20K). Introducing the Con- coefficienthasasignificantpositiveimpactonthesegmen-
text Loss improves dense tasks but reduces classifica- tation performance, however at the cost of classification
tion performance on SSv2. Incorporating our Deep Self- performance. Warmup on the coefficient allows to miti-
Supervision restores the classification performance. The gate part of the lost performance. Our weighted scheme
VisionMix163Mdataset,theMulti-ModalTokenizer,and further improves the performance on both segmentation
| scaling model | size further | improve the results. |     | and classification. |     |     |
| ------------- | ------------ | -------------------- | --- | ------------------- | --- | --- |
| IN1K SSv2     | NYU          | ADE20K               |     | ADE20K SSv2         |     |     |
Scheme Warmup
| Acc. | Acc. RMSE↓ | mIoU                   |     | mIoU Acc. | λ           |            |
| ---- | ---------- | ---------------------- | --- | --------- | ----------- | ---------- |
| 82.2 | 72.8 0.682 | 22.2 V-JEPA2           |     | 22.2 72.8 | V-JEPA2,λ=0 | cte        |
| 72.6 | 62.5 0.474 | 33.8 +ContextLoss      |     | 26.4 71.0 | 0.05        | cte        |
| 80.8 | 72.1 0.463 | 38.6 +Multi-levelPred. |     | 29.6 62.5 | 0.2         | cte        |
| 81.6 | 72.6 0.418 | 40.8 +VisionMix        |     | 27.5 53.8 | 0.5         | cte        |
| 81.6 | 72.6 0.415 | 41.4 +Multi-modalTok.  |     | 24.6 51.1 | 1.0         | cte        |
| 84.8 | 76.1 0.365 | 47.1 +ModelScaling     |     | 30.5 60.5 | 0.2         | cte ✓      |
| 85.5 | 77.7 0.307 | 47.9 +Cool-down.       |     | 32.2 61.5 | 0.5         | cte ✓      |
|      |            |                        |     | 33.8 62.5 | 0.5         | weighted ✓ |
2.3.1 DensePredictionLoss
We propose applying our self-supervised loss to both masked and visible patches by minimizing
L dense =
L +L , where L is defined in Eq. 1 and L is defined in Eq. 2. Naive application of L loss
| predict | ctx | predict |     | ctx |     | ctx |
| ------- | --- | ------- | --- | --- | --- | --- |
leads to poor performance on global semantic tasks, as the system can potentially find trivial solutions, such
as copying the context features. We therefore explore various weighting coefficients in Eq. 2. Table 2
λ i
presents an ablation on various weighting schemes. First, we experiment with fixed values and set all λ
i
to a constant λ and try values in the range λ = [0.0,0.05,0.2,0.5,1.0]. We observe that as we increase λ,
the performance in semantic segmentation in the ADE20k dataset increases significantly up to certain point,
but at the cost of the performance in action recognition in the SSv2 dataset decreases. We then introduce a
progressive warm-up of to restore action-recognition performance, with a schedule from epochs 50–100. We
λ
found empirically that it greatly stabilizes training. Following, we introduce a dynamic weighting scheme
where L for a given patch i is weighted by the inverse square root of its minimum spatio-temporal distance
ctx
| to any masked | token | in the video sequence: | i.e. setting |     |     |     |
| ------------- | ----- | ---------------------- | ------------ | --- | --- | --- |
λ
λ = (3)
i (cid:112)d
(i,M)
min
in L in Eq. 2, where d is the distance, in number of blocks, between a context token and its closest mask
| ctx |     | min |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
token. This weighting emphasizes patches near masked regions by enforcing local continuity between masked
and context areas, yielding a good trade-off between segmentation and action recognition performance.
Introducing our novel context loss L with our weighted scheme improves the performance on dense vision
ctx
tasks (22.2 33.9 mIoU on ADE20k, 0.682 0.473 RMSE on NYUv2). Qualitatively, this loss smooths the
|     | →   |     | →   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
feature maps by removing noisy artifacts, as shown in Figure 3. However, Table 1 shows that there is still a
degradation in video understanding (72.8 → 62.5 on SSv2) and image classification (82.2 → 72.6 on IN1K).
2.3.2 DeepSelf-Supervision
We self-supervise the encoder representation not only at the output but also at multiple intermediate levels.
We first concatenate, along the channel dimension, the outputs of three intermediate x-encoder blocks, in
addition to the output layer. Then, a lightweight MLP fuses these multi-level representations and reduces
their dimensionality before feeding them into the predictor. The predictor processes the fused multi-level
sequence of context and mask tokens and produces four outputs corresponding to the four encoder layers.
Both the prediction loss and the context loss are then applied at each one of these four levels.
Deep Self-Supervision leads to significant improvement on downstream performance for both global and dense
tasks, as shows Figure 5. Furthermore, it allows local information to flow towards the final layers, effectively
7

Table3 ComparisonbetweenVideoMix22MandVisionMix163M. We increase the visual diversity of the pretraining dataset
by increasing the number of images, replacing ImageNet with LVD-142M, and update the YT-1B sampling weight to
| promote data-source | with    | more  | visual diversity. |         |          |            |         |           |
| ------------------- | ------- | ----- | ----------------- | ------- | -------- | ---------- | ------- | --------- |
|                     |         |       |                   |         |          |            | V-JEPA2 | V-JEPA2.1 |
| Source              |         |       |                   | Samples | Type     | TotalHours |         |           |
|                     |         |       |                   |         |          |            | weights | weights   |
| SSv2 (Goyal         | et al., | 2017) |                   | 168K    | EgoVideo | 168        | 0.056   | 0.170     |
Kinetics (Carreira et al., 2019) 733K ExoVideo 614 0.188 0.010
Howto100M (Miech et al., 2019) 1.1M ExoVideo 134K 0.318 0.100
| ImageNet | (Deng et         | al., 2009)    |     | 1M    | Images         | n/a  | 0.250 | 0.    |
| -------- | ---------------- | ------------- | --- | ----- | -------------- | ---- | ----- | ----- |
| YT-1B    | (Zellers et al., | 2022)         |     | 19M   | ExoVideo       | 1.6M | 0.188 | 0.720 |
| LVD-142M | (Oquab           | et al., 2023) |     | 142 M | Curated images | n/a  |       |       |
removing the need for intermediate layers in dense downstream tasks as we show in Appendix D.1. Deep
Self-Supervision allows to recover the global understanding capabilities of V-JEPA 2 (72.0 on SSv2, 80.8 on
IN1K) while improving on dense tasks with the context loss (38.6 mIoU on ADE20K, 0.463 RMSE on NYU).
2.3.3 ScalingImageData.
DINOv2 (Oquab et al., 2023) introduced a cluster-based retrieval strategy to select images from a large pool
of raw internet data, resulting in a curated set of 142 million images, referred to as the LVD-142M dataset.
Using a similar approach, V-JEPA 2 (Assran et al., 2025) collected and curated video scenes from YT1B
videos (Zellers et al., 2022), combined with other publicly available video datasets, yielding a large-scale
collection of 19 million video samples from the internet, corresponding to million hours. Both works
1.6
| demonstrated | the positive | effect | of data | scaling for | SSL pretraining. |     |     |     |
| ------------ | ------------ | ------ | ------- | ----------- | ---------------- | --- | --- | --- |
Building on these insights, we construct our VisionMix163M Dataset, combining large-scale curated sources
from these two prior works. As we show in Table 3, we replace the 1M-image ImageNet subset from VJEPA-2
pretraining data with LVD-142M, providing a broader and more diverse appearance distribution. Since this
extensive image collection already covers many static visual concepts, we shift the video sampling strategy
towards more dynamic, motion-rich content, increasing the SSv2 sampling weight from 0.056 to 0.170. We
also found beneficial to increase the contribution of YT-1B from 0.188 to 0.720, which contains much more
| heterogeneous | video samples. |     |     |     |     |     |     |     |
| ------------- | -------------- | --- | --- | --- | --- | --- | --- | --- |
Rather than mixing images and videos within the same training batch, we leverage distributed training by
assigning separate workers to each modality. After each iteration, gradients from video-only and image-only
nodes are aggregated before updating the model. The image/video ratio is controlled through per-modality
batch sizes. Empirically, we found optimal performance with 128 video clips (16 frames each) and 2,304
images per global batch. As we report in Table 1, the improvement of training on a more diverse and extend
database is beneficial in all tasks (72.1 → 72.6 on SSv2, 80.8 → 81.6 on ImageNet, 38.6 → 40.8 on ADE20K,
| 0.463 0.418 | RMSE | on NYUv2). |     |     |     |     |     |     |
| ----------- | ---- | ---------- | --- | --- | --- | --- | --- | --- |
→
2.3.4 Multi-ModalTokenizer
Previous work exploring joint training on image and video, such as V-JEPA 2, was suboptimal: it employed
a single 3D convolution as the patch-embedding layer. Images were duplicated temporally and treated as
a 16-frame static video, which significantly increased their computational cost and introduced an incorrect
representational bias (i.e., images were interpreted as static videos). Instead, we introduce a multi-modal
tokenizer, which applies a 3D convolution of 16×16×2 for processing videos and a 2D convolution of 16×16
for images. We also add a modality-learnable token to both the encoder and the predictor inputs, which
explicitlyencodeswhethertheinputcomesfromtheimageorvideopathway. Theselearnabletokenscondition
the processing on the input modality, helping the model disentangle stronger static appearance cues in images
| and temporal | motion information |     | in  | videos. |     |     |     |     |
| ------------ | ------------------ | --- | --- | ------- | --- | --- | --- | --- |
8

This design allows each modality to be processed in its native form, eliminating the need for temporal
duplication of images and improving computational efficiency. Additionally, we observe that using the
Multi-Modal Tokenizer has a positive effect on dense-task performance: it improves mIoU on ADE20K from
40.8 to 41.4, while performance on action or object recognition remains stable.
2.3.5 ScalingModelSizetoViT-G(2B)andHigh-ResolutionCool-Down
Next, we explore the effect of model scaling and high-resolution cooldown. Scaling the V-JEPA encoder from
a ViT-L with 300 million parameters to a ViT-G with 2 billion parameters leads to significant improvements
on all downstream tasks (72.6 → 76.1 on SSv2, 81.6 → 84.8 accuracy on ImageNet, 41.4 → 47.1 mIoU on
ADE20K, 0.415 → 0.365 RMSE on NYUv2).
Additionally, introducing a cool-down phase for the learning rate, during which we increase both the spatial
resolution of images (from 256×256 to 512×512) and the spatio-temporal resolution of videos (from 16
frames at 256×256 to 64 frames at 384×384), further improves performance on all tasks. This achieves an
accuracy of 77.7 on SSv2, 85.5 on ImageNet, an mIoU of 47.9 on ADE20K, and an RMSE of 0.307 on NYUv2,
resulting in our best performing model. The benefits of a cool-down training phase are particularly strong in
depth estimation (0.365 →0.307 RMSE on NYUv2).
2.3.6 ModelDistillation
Wescaledthesizeofthemodelnotonlytoachievetop-tierperformancebutalsotoenableeffectivecompression
of the model through distillation Hinton et al. (2015). We distill our ViT-G (2B) model into smaller variants
(ViT-B, 80M; ViT-L, 300M). The distillation protocol is adapted from our pretraining recipe, with key
differences: i) we replace the Exponential-Moving-Average (EMA) of the target encoder by a frozen teacher
model, ii) we keep an EMA copy of the student encoder, that is not used in the loss, but serves as the final
model, iii) the distillation loss is identical to our pretraining loss, except it is only computed on the last layer
of the teacher encoder, and it does not use deep self-supervision, iv) we use a predictor with only 12 blocks
and a final linear layer matching the teacher embedding dimension. All other hyper-parameters—including
masking ratios, cool-down schedules, learning rates, and data augmentations—remain identical to the original
pretraining recipe. We provide more details on the distillation protocol in Appendix B.
3 Results
Inthissection,weevaluatetheperformanceofV-JEPA2.1onalargevarietyofdownstreamtasks. Throughout
the experiments, we employ V-JEPA 2.1 as a frozen encoder, demonstrating the versatility of its features.
We first demonstrate the predictive capabilities of V-JEPA 2.1 in two forecasting tasks: short-term object
interaction anticipation (Section 3.1) and action anticipation (Section 3.2). We then demonstrate that can
leverage V-JEPA 2.1 to learn an action-condition world model and performs robot manipulation (Section 3.3)
and navigation tasks (Section 3.4) in zero-shot setup. Then, we evaluate the quality of the learned dense
featuresbyassessingtheV-JEPA2.1performanceonsingle-imagedepthestimationandsemanticsegmentation
(Section 3.5). Following, we analyze the temporal consistency of V-JEPA 2.1 representations through the
video object segmentation task (Section 3.5). We also analyze V-JEPA 2.1 global understanding on two
high-level understanding tasks: probe-based video classification and image classification (Section 3.7). Finally,
we present results for our smaller distilled models (Section 3.10). We provide more details on the experimental
setup and all pretraining hyper-parameters in Appendices A and C.
3.1 Short-TermObjectInteractionAnticipation
Short-Term object-interaction Anticipation (STA) consists in predicting future object interaction in a ego-
centric scenario, predicting the next active object bounding box b, the object noun category N the action
verb V and the time until contact (δ). This formulation evaluates fine-grained 2D localization, semantic
understanding of objects, temporal reasoning over video dynamics, and the ability to forecast user intentions.
Using the Ego-4D STA benchmark (Grauman et al., 2022), we show that V-JEPA 2.1 outperforms previous
9

Figure6 Short-TermAnticipationtask. Given a video observed up to time t (denoted V :t ), the model predicts a set
of future object–interaction events. Each prediction includes: (i) a bounding box localizing the object that will
be interacted with, (ii) the noun class of that object, (iii) a verb class describing the upcoming interaction, and
(iv) the anticipation time δ, i.e., the number of seconds between the current frame and the start of the interaction.
Ground-truth labels are derived from the contact frame V , but are expressed in the coordinate frame of the last
t+δ
observed frame V .
t
state-of-the-art performance by a significant margin due to its high-quality dense features and predictive
capabilities.
Task. We evaluate V-JEPA 2.1 on the STA v2 split of Ego4D (Grauman et al., 2022), which comprises 243
hours of annotated video clips spanning 128 noun and 81 verb categories, with a total of 98,276 training and
47,395 validation samples. We compare against state-of-the-art methods (Ragusa et al., 2023; Mur-Labadia
et al., 2024; Thakur et al., 2023), and we further asses the performance of DINOv2 (Darcet et al., 2023) and
DINOv3 (Siméoni et al., 2025) image encoders using our proposed attentive probe. Following the evaluation
protocolofGraumanetal.(2022), wereportTop-5AveragePrecision(AP)andTop-5meanAveragePrecision
(mAP) metrics. As in standard mAP, predictions are matched to ground-truth boxes using IoU > 0.5 and
additionalclass-specificcriteria. Forinstance,theTop-5mAPAllvariantrequiresacorrectnoun, correctverb,
IoU above 0.5, and a time-to-contact δ prediction within a 0.25-second tolerance. To address the inherently
multi-modal nature of future anticipation—where multiple plausible next-active objects may exist—the metric
discounts up to four highest-scoring false positives per example, thereby avoiding penalties for plausible but
unannotated predictions. Additionally, we report individual metrics to evaluate the temporal (δ), spatial
(bounding boxes), and semantic (noun and verb) dimensions of the task.
Evaluation protocol. The model receives as input a low-resolution video clip (384 px, 8 frames spanning
0.5seconds)andahigh-resolutionimage(1080px)correspondingtothelastframeoftheclip. Usingthefrozen
encoder of V-JEPA 2.1, we extract last-level features independently from both inputs using the respective
patchifier (a 2D convolution for the high-resolution image and a 3D convolution for the video) and adding the
corresponding modality embedding. For the video features, we train a four-layer attentive probe, followed by
the frame-guided temporal pooling module from Mur-Labadia et al. (2024). This module aggregates the 3D
video tokens into a 2D representation that is spatially aligned with the spatial reference of the last frame.
The pooled video features are then summed to the image features, and the resulting fused representation
is rescaled into four multiscale feature maps, which serve as input to the detection head. To ensure a fair
comparison with state-of-the-art methods (Ragusa et al., 2023; Mur-Labadia et al., 2024; Thakur et al., 2023),
we adopt the same detection head (Ragusa et al., 2023) utilized in these approaches. This head extends Faster
R-CNN by adding linear layers to additionally predict the verb category and the time to contact.
10

Table4 Short-TermObjectInteractionAnticipationonEgo4D. Following Grauman et al. (2022), we report different Top-5
Average Precision (AP) and mean Average Precision (mAP) metrics, where the winning score is the mAP All. We
compare results reported in the literature with different frozen SSL encoders (DINOv2, DINOv2, V-JEPA 2 and our
V-JEPA 2.1) extended with an attentive-based predicted head. V-JEPA 2.1 obtains the state-of-the-art due to its
high-quality dense features and predictive capabilities.
AP AP AP AP AP AP AP AP mAP mAP mAP mAP
Model
b b+N b+V b+δ b+N+V b+δ+N b+δ+V All N N+V N+δ All
ResultsReportedintheLiterature
StillFast(Ragusaetal.,2023) - - - - - - - - 20.2 10.3 7.17 3.96
STAformer(Mur-Labadiaetal.,2024) 38.3 28.3 16.6 12.27 12.8 8.89 5.47 4.06 29.4 15.3 9.94 5.67
GANO(Thakuretal.,2023) 45.3 27.0 12.2 16.6 6.54 9.0 4.18 2.47 - - - -
Encodersusingoursameprotocol
DINOv2ViT-L(Oquabetal.,2023) 45.1 37.8 21.9 14.4 17.6 10.6 7.27 5.25 28.3 15.2 9.22 5.25
DINOv2ViT-g(Oquabetal.,2023) 47.8 38.1 23.6 14.1 19.1 10.9 7.29 5.73 30.6 16.8 9.37 5.44
DINOv3ViT-H+(Siméonietal.,2025) 48.9 40.2 23.4 13.6 19.4 10.8 6.71 5.45 32.4 17.2 9.53 5.20
DINOv3ViT-7B(Siméonietal.,2025) 50.2 40.9 23.8 14.2 19.8 11.5 7.33 5.82 33.8 17.4 10.3 5.68
V-JEPA2ViT-g(Assranetal.,2025) 45.7 34.4 22.2 16.7 16.9 12.1 8.56 6.26 27.2 14.9 10.4 6.02
V-JEPA2.1ViT-g 47.3 36.5 23.6 18.1 18.2 13.5 9.55 7.21 28.7 15.5 11.4 6.75
V-JEPA2.1ViT-G 50.7 39.3 25.8 20.2 20.3 15.1 10.8 8.20 30.9 17.2 12.8 7.71
V-JEPA2.1Prediction Ground-truth V-JEPA2.1Prediction Ground-truth
Figure7 Short-TermAnticipation(STA)qualitativeresults. We compare our model predictions with the ground-truth
data. V-JEPA 2.1 predicts multiple scenarios, where the predicted object and verb classes correspond with plausible
human-object interactions.
Results. Table 4 presents a comparison with state-of-the-art methods on the Short Term Anticipation task.
V-JEPA 2.1 demonstrates achieves the absolute state-of-the-art performance with an overall mAP of 7.71.
This represents a relative improvement of approximately 35% over the previous best method (Mur-Labadia
etal., 2024), whichintroduces task-specifictraining components. As itisshownbytheindividual metrics, this
gain is primarily driven by improved understanding of the next action 25.8 AP and the time to contact
b+V
20.20 AP , 12.9 mAP . Furthermore, the high-quality V-JEPA 2.1 dense features enable the precise 2D
b+δ b+δ
detection of the next-active object bounding boxes, achieving 50.7 AP and surpassing DINOv3 ViT-7B in this
category. Qualitative results are shown in Figure 7. V-JEPA 2.1 predicts plausible short-term interactions,
with accurate bounding box localization, robust understanding of object categories, and plausible inference of
the user next action intentions.
3.2 ActionAnticipation
Action anticipation consists in predicting the future action given a contextual video clip leading up to some
time before the action. Using the Epic-Kitchens-100 (EK100) benchmark (Damen et al., 2022), we show that
V-JEPA 2.1 outperforms the action anticipation performance of V-JEPA 2, and sets a new state-of-the-art for
11

Table5 ActionAnticipationonEK100. Comparisonwiththestate-of-the-artontheEK100ActionAnticipationbenchmark.
Wereportmean-classrecall-at-5forverb,nounandactiononthevalidationsetofEK100. V-JEPA2.1offerscomparable
performance to V-JEPA 2 for the ViT-g 1B model, but shows improved performance for the ViT-G 2B model, setting
| a new state-of-the-art | for the     | task.                 |            |        |                     |        |
| ---------------------- | ----------- | --------------------- | ---------- | ------ | ------------------- | ------ |
|                        | Method      |                       |            | Param. | Action Anticipation |        |
|                        |             |                       |            |        | Verb Noun           | Action |
|                        | InAViT      | (Roy et al., 2024)    |            | 160M   | 51.9 52.0           | 25.8   |
|                        | Video-LLaMA |                       |            | 7B     | 52.9 52.0           | 26.0   |
|                        |             | (Zhang et al.,        | 2023)      |        |                     |        |
|                        | PlausiVL    |                       |            | 8B     | 55.6 54.2           | 27.6   |
|                        |             | (Mittal et al., 2024) |            |        |                     |        |
|                        | V-JEPA      | 2 ViT-g (Assran et    | al., 2025) | 1B     | 63.6 57.1           | 39.7   |
|                        | V-JEPA      | 2.1 ViT-g             |            | 1B     | 63.6 56.2           | 38.4   |
|                        | V-JEPA      | 2.1 ViT-G             |            | 2B     | 64.3 59.9           | 40.8   |
the task.
Task. The EK100 dataset is comprised of 100 hours of cooking activities recorded from an egocentric
perspective across 45 kitchen environments. Each video in EK100 is annotated with action segments, which
include a start timestamp, an end timestamp, and an action label. There are 3,568 unique action labels, each
consisting of a verb and a noun category, with a total of 97 verb categories and 300 noun categories. The
EK100 action anticipation task involves predicting noun, verb, and action (i.e., predicting verb and noun
jointly) from a video clip, referred to as context, that occurs before the start timestamp of an action segment.
The interval between the end of the context and the beginning of the action segment is the anticipation time,
which is set to 1 second by default. Given that different future actions may be possible from a given context,
mean-class recall-at-5 is used as the metric to measure performance (Damen et al., 2022).
Evaluation protocol. We employ the same protocol as V-JEPA 2 and use an attentive probe trained on
top of the frozen V-JEPA 2.1 encoder and predictor to anticipate future actions. Specifically, we sample a
video clip that ends 1 second before an action starts. This video context is fed to the encoder. The predictor
takes the encoder representation, along with the mask tokens corresponding to the frame 1 second into the
future, and predicts the representation of the future video frame. The outputs of the predictor and encoder
are concatenated along the token dimension and fed to an attentive probe with a similar architecture to
those used in our probe-based video classification protocol, with the difference being that the anticipation
probe’s final cross-attention layer learns three query tokens (as opposed to one), and each query output is
fed to a different linear classifier to predict the action category, the verb category, and the noun category
respectively. A focal loss (Lin et al., 2017b) is applied to each classifier independently and then summed
| before back-propagating | through | the shared | attention | blocks of | the probe. |     |
| ----------------------- | ------- | ---------- | --------- | --------- | ---------- | --- |
Results. Table 5 summarizes the results on the validation set of the EK100 action anticipation benchmark.
We compare V-JEPA 2.1 ViT-g 1B and ViT-G 2B encoders with V-JEPA 2 ViT-g 1B encoder. Both leverage
32 frames with 8 frames per second at resolution 384 × 384 as video context. V-JEPA 2.1 is comparable to
V-JEPA 2 on the same 1B model size, but show scaling of the performance to the 2B models size, setting a
new absolute state-of-the-art performance at 40.8 Action Recall@5, corresponding to a +2.8% improvement.
3.3 RoboticArmPlanning
Next,weevaluateV-JEPA2.1forrobotmanipulation. Tothatend,wetrainaframe-causalaction-conditioned
predictor, following the protocol of Assran et al. (2025). In particular, we use the public codebase from Assran
et al. (2025) and modify it to compute features using our V-JEPA 2.1 video encoder; the predictor is an
identical 24-layer transformer network containing approximately 300M parameters, and is trained on the
Droid raw dataset (Khazatsky et al., 2024) using both a teacher-forcing and two-step rollout loss. The model
is then deployed in our lab, zero-shot, on a table-top Franka Panda robot arm with a parallel-jaw gripper,
and evaluated on reach, grasp, and pick-and-place tasks with visual goal specification via model-predictive
12

| VJEPA 2 |     |     |     |     |     | VJEPA 2.1 Energy Landscape |     |     |
| ------- | --- | --- | --- | --- | --- | -------------------------- | --- | --- |
VJEPA 2.1
| Goal Frame |     | Start Frame |     | Robot Execution |     |     |     |     |
| ---------- | --- | ----------- | --- | --------------- | --- | --- | --- | --- |
|            |     | (a)         |     |                 |     |     | (b) |     |
Zero-shot evaluation of VJEPA 2 and VJEPA 2.1 models on a table-top Franka Panda robot arm with a
Figure8
parallel-jaw gripper, demonstrating Grasp of a cup using visual goal specification via model-predictive control. VJEPA
2.1 features better encode depth information, leading to an improvement in robot manipulation when grasping the cup
| involves reasoning | over actions | along | the depth | axis of the | camera. |     |     |     |
| ------------------ | ------------ | ----- | --------- | ----------- | ------- | --- | --- | --- |
control. We use the same exact task configuration files provided in Assran et al. (2025), and similar planning
hyper-parameters.
Success rates are reported in Table 6. VJEPA 2.1 exhibits an improved depth understanding, leading to a 10%
improvement in the success rate of Grasp compared to VJEPA 2 (cf. Figure 8). Moreover, we find that the
VJEPA2.1modelunlocksthebenefitofplanningwithslightlylongerrollouts,perhapsduetotheimprovement
in dense features afforded by our model. In particular, by reducing the number of CEM samples and planning
over 8 steps, we observe an additional improvement in the success rate on Grasp. By contrast, we actually
observe a degradation in the success rate of VJEPA 2 when planning over longer horizons. Qualitatively, we
further observe that task failures using the VJEPA 2.1 model on Pick-and-Place and Grasp are a result of
poor planning over gripper actions, as opposed to failures in spatial understanding; e.g., closing the gripper
too soon such that you cannot grasp the object, or slightly opening the gripper while in transit leading to the
| object being | dropped. |     |     |     |     |     |     |     |
| ------------ | -------- | --- | --- | --- | --- | --- | --- | --- |
Table6 Planning Performance. Comparing closed-loop robot manipulation of a cup using MPC with VJEPA 2
versus VJEPA 2.1. In both cases we leverage the cross-entropy method (Rubinstein, 1997) for optimizing the sequence
of actions using a single A100 GPU. For each robot skill, we evaluate each model across 10 tasks and average the
results. TheimproveddepthunderstandinganddensefeaturesofVJEPA2.1leadtoa20%improvementinthesuccess
rate of Grasp. Moreover, qualitatively, we find that any failures on Pick-and-Place and Grasp are a result of poor
planning over gripper actions, as opposed to failures in spatial understanding (e.g., closing the gripper too soon, such
that you cannot grasp the object, or slightly opening the gripper while in transit leading to the object being dropped.
|                 |        |            |          | Planning | Details |         |             |              |
| --------------- | ------ | ---------- | -------- | -------- | ------- | ------- | ----------- | ------------ |
|                 |        |            | #Samples | Iter.    | Horizon | Time    |             |              |
| Method          |        |            |          |          |         |         | Reach Grasp | Pick-&-Place |
| VJEPA 2 (Assran | et     | al., 2025) | 800      | 10       | 1       | 3 sec.  | 100% 60%    | 80%          |
|                 |        |            | 800      | 10       | 1       | 3 sec.  | 100% 70%    | 80%          |
| VJEPA 2.1       | (ours) |            |          |          |         |         |             |              |
|                 |        |            | 300      | 15       | 8       | 14 sec. | 100% 80%    | 80%          |
13

Figure9 PlanningNavigationTrajectoriesinLatentSpace. V-JEPA 2.1 enables 10× faster and more accurate navigation
planning compared to (Bar et al., 2025). We show PCA visualizations of 8 denoising steps of the planned latent
| trajectory between | a   | start frame | and | a goal frame. |     |     |     |     |     |
| ------------------ | --- | ----------- | --- | ------------- | --- | --- | --- | --- | --- |
Table7 OpenLoopNavigationPlanning.WefinetuneV-JEPA2.1onrobotnavigationdatasetsandcomparetheopen-loop
planning performance to NWM. Reporting the average planning time (seconds), normalized Average Trajectory Error
(ATE) and Relative Trajectory Error (RTE). V-JEPA 2.1 representation enables 10× speed-up without sacrificing
performance.
| Model |     |     | Time | Recon   | TartanDrive | Scand   | Sacson  |     | Average |
| ----- | --- | --- | ---- | ------- | ----------- | ------- | ------- | --- | ------- |
|       |     |     |      | ATE RTE | ATE RTE     | ATE RTE | ATE RTE | ATE | RTE     |
NWM(Baretal.,2025) 103.2(s) 1.146 0.339 5.831 1.219 1.113 0.297 4.037 0.928 3.032 0.696
| V-JEPA2.1ViT-g |     |     | 10.6    |             | 5.758 1.200 | 1.094 0.299 |             |       | 0.690 |
| -------------- | --- | --- | ------- | ----------- | ----------- | ----------- | ----------- | ----- | ----- |
|                |     |     | (s)     | 1.146 0.338 |             |             | 3.904 0.921 | 2.975 |       |
| V-JEPA2.1ViT-G |     |     |         | 1.179 0.340 |             |             | 4.054 0.938 | 2.990 |       |
|                |     |     | 10.6(s) |             | 5.687 1.187 | 1.038 0.285 |             |       | 0.688 |
3.4 NavigationPlanning
Next, we evaluate the utility of V-JEPA 2.1 representations for short-term robotic navigation. Specifically,
given an agent’s most recent observation and a goal location specified by an image, we predict a 2-second
navigation trajectory toward the goal. We adopt the navigation planning setup of NWM (Bar et al., 2025)
and train a latent world model on top of the V-JEPA 2.1 representations. We find that V-JEPA 2.1 enables
|                      |     | while | achieving |                        |     | than the previously | used SD-VAE |     | (Rombach |
| -------------------- | --- | ----- | --------- | ---------------------- | --- | ------------------- | ----------- | --- | -------- |
| moreaccurateplanning |     |       |           | 10×fasterplanningspeed |     |                     |             |     |          |
et al., 2022). Results are reported in Table 7, with qualitative examples shown in Figure 9.
We train a Conditional Diffusion Transformer (CDiT) on top of the V-JEPA 2.1 representations, similarly
to NWM. Our initial experiments indicate that directly training a diffusion model in the high-dimensional
embedding space of the V-JEPA 2.1 is challenging: because the representations are high-dimensional (at least
larger than those of an SD-VAE), injecting noise in arbitrary directions can easily push samples off the
80×
data manifold. To improve robustness, we introduce two modifications. First, we train the model to predict a
clean representation rather than noise (Li and He, 2025). Second, we use DDIM sampling (Song et al., 2020),
which is less stochastic than DDPM (Ho et al., 2020) and empirically improves stability.
For planning, given an initial context embedding and a goal, we use the Cross-Entropy Method to sample
N =480 candidate trajectories of length 2 seconds at 4 FPS. We select the best candidate by simulating it in
the world model and choosing the trajectory that minimizes the distance to the goal embedding. To simplify
the search, we plan in a reduced 3-DoF action space (translation and yaw rotation). With V-JEPA 2.1, we
require only 8 denoising steps, compared to the optimal SD-VAE setting which requires at least 128 steps.
This yields lower Absolute Trajectory Error (ATE) and Relative Trajectory Error (RTE) on the validation set
| while reducing | planning | time | by 10×. |     |     |     |     |     |     |
| -------------- | -------- | ---- | ------- | --- | --- | --- | --- | --- | --- |
14

Table8 Performanceondensevisualtasks. We report the Root Mean Squared Error (RMSE) for depth estimation
(NYUv2, KITTI), mean Intersection-over-Union (mIoU) for semantic segmentation (ADE20K, Cityscapes, VOC12),
and the J&F-Mean for video object segmentation (DAVIS, YouTube-VOS). Following Siméoni et al. (2025), ADE20K
andVOC12areevaluatedataninputresolutionof448×448formodelswithpatchsize14and512×512forthosewith
patch size 16. Cityscapes, NYUv2, and KITTI use their default evaluation resolutions. For DAVIS and YouTube-VOS,
we evaluate with the shorter image side set to 480 px (patch size 16) or 420 px (patch size 14). V-JEPA 2.1 VIT G
demonstrates strong performance on dense vision tasks. Notably, it achieves state-of-art performances on NYUv2
| depth estimation, |     | outperforming |     | a   | DINOv3 | backbone | with   | 7 billion | parameters. |              |     |         |         |
| ----------------- | --- | ------------- | --- | --- | ------ | -------- | ------ | --------- | ----------- | ------------ | --- | ------- | ------- |
|                   |     |               |     |     |        |          | Depth  |           |             | Segmentation |     |         | VOS     |
| Method            |     |               |     |     | Param. |          |        |           |             |              |     |         |         |
|                   |     |               |     |     |        |          | NYUv2↓ | KITTI↓    | ADE20k      | Citysc.      | VOC | DAVIS-S | YTVOS-S |
7Bmodels
Web-DINO(Fanetal.,2025) 7B/14 0.466 3.158 42.7 68.3 76.1 57.2 43.9
DINOv3(Siméonietal.,2025) 7B/16 0.309 2.346 55.9 81.1 86.6 71.1 74.1
Modelslessthan2Bparameters
PEcore(Bolyaetal.,2025) 2B/14 0.590 4.119 38.9 61.1 69.2 48.2 34.7
PEspatial(Bolyaetal.,2025) 2B/14 0.362 3.082 49.3 73.2 82.7 68.4 68.5
AM-RADIOv2.5(Ranzingeretal.,2024) 1B/14 0.340 2.918 53.0 78.4 85.4 66.5 70.1
InternVideo2-1B(Wangetal.,2024b) 1B/14 0.471 4.739 28.4 35.6 65.2 50.6 51.2
SigLIP2(Tschannenetal.,2025) 1B/16 0.494 3.273 42.7 64.8 72.7 56.1 52.0
DINOv2(Oquabetal.,2023) 1B/14 0.372 2.624 49.5 75.6 83.1 63.9 65.6
| DINOv3ViT-H+(Siméonietal.,2025) |     |     |     |     | 0.8B/16 |     | 0.352 | 2.635 |     |           |      |      |      |
| ------------------------------- | --- | --- | --- | --- | ------- | --- | ----- | ----- | --- | --------- | ---- | ---- | ---- |
|                                 |     |     |     |     |         |     |       |       |     | 54.8 79.5 | 85.8 | 71.1 | 74.0 |
V-JEPA2ViT-g(Assranetal.,2025) 1B/16 0.642 4.650 24.4 45.9 63.9 52.5 53.7
| V-JEPA2.1ViT-g |     |     |     |     | 1B/16 |     | 0.350 | 2.601 |     | 47.8 71.8 | 84.7 | 68.1 | 72.3 |
| -------------- | --- | --- | --- | --- | ----- | --- | ----- | ----- | --- | --------- | ---- | ---- | ---- |
| V-JEPA2.1ViT-G |     |     |     |     | 2B/16 |     |       |       |     | 47.9 73.5 | 85.0 | 69.0 | 72.7 |
|                |     |     |     |     |       |     | 0.307 | 2.461 |     |           |      |      |      |
3.5 DepthEstimationandSemanticSegmentation
We evaluate the quality of the learned representations on semantic segmentation and depth estimation, two
| tasks that | require | fine-grained |     | understanding |     |     | of the | image | spatial | structure. |     |     |     |
| ---------- | ------- | ------------ | --- | ------------- | --- | --- | ------ | ----- | ------- | ---------- | --- | --- | --- |
Task. Semantic segmentation probes the model’s ability to capture category-level semantics and object
boundaries. We evaluate our model on PASCAL VOC12 (Everingham et al., 2015), ADE20K (Zhou et al.,
2017b), and Cityscapes (Cordts et al., 2016), reporting the mean Intersection over Union (mIoU). As in
Siméoni et al. (2025), the input resolution of the images is adapted to 1024 patch tokens (i.e.,
512×512
for patch size 16, 448×448 for patch size 14). On the other hand, depth estimation evaluates the model’s
understanding of the scene’s geometric structure. For this task, we use the NYUv2 (Silberman et al., 2012a)
and KITTI (Geiger et al., 2013b) benchmarks and report the Root Mean Squared Error (RMSE).
| Evaluation        |              | protocol.    |            | Following  | the         | protocol    | of   |     |     |     |     |     |     |
| ----------------- | ------------ | ------------ | ---------- | ---------- | ----------- | ----------- | ---- | --- | --- | --- | --- | --- | --- |
| DINOv3            | (Siméoni     |              | et al.,    | 2025),     | we train    | a dense     |      |     |     |     |     |     |     |
| linear projection |              | on           | top of     | the frozen | final-layer |             | fea- |     |     |     |     |     |     |
| tures of          | the V-JEPA   |              | 2.1        | encoder    | using       | the image   |      |     |     |     |     |     |     |
| patchifier.       | Importantly, |              | we         | do not     | utilize     | intermedi-  |      |     |     |     |     |     |     |
| ate layers        | from         | the encoder. |            | As V-JEPA  |             | 2.1 adopts  |      |     |     |     |     |     |     |
| a 3D RoPe         | for          | positional   |            | encoding,  | the         | frequencies |      |     |     |     |     |     |     |
| are interpolated  |              | according    |            | to the     | image       | resolution. |      |     |     |     |     |     |     |
| Results.          | Table        | 8            | summarizes | the        | performance |             | of   |     |     |     |     |     |     |
| V-JEPA            | 2.1 and      | other        | visual     | encoders   | on          | depth       | es-  |     |     |     |     |     |     |
timation and single-image semantic segmentation. Figure12 QualitativecomparativeofV-JEPA2.1ViT-Gvs
|                 |           |           |          |                  |             |         |     | DINOv3ViT-H+. |         | V-JEPA            | 2.1 captures | fine-grained | details           |
| --------------- | --------- | --------- | -------- | ---------------- | ----------- | ------- | --- | ------------- | ------- | ----------------- | ------------ | ------------ | ----------------- |
| V-JEPA          | 2.1 ViT-G |           | achieves | state-of-the-art |             | results |     |               |         |                   |              |              |                   |
|                 |           |           |          |                  |             |         |     | (i.e the      | traffic | light contour)    | and          | obtains      | better scale con- |
| on linear-probe |           | monocular |          | depth            | estimation, | reach-  |     |               |         |                   |              |              |                   |
|                 |           |           |          |                  |             |         |     | sistency.     | In      | the two rightmost | columns,     | DINOv3       | mislabel          |
ing0.307RMSEonNYUv2andstrongperformance
thedepthofthegreenobjectonthebed,andtheTV,and
onKITTIwith2.461RMSE,performingbestacross detect them closer to the camera than they are.
| models | that have | less | than | 2 billion | parameter. |     | On  |     |     |     |     |     |     |
| ------ | --------- | ---- | ---- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
NYUv2, V-JEPA 2.1 surpasses prior image encoders, including DINOv3 ViT-7B (0.309 RMSE on NYU) and
15

NYUv2 KITTI
egamI
2APEJ-V
1.2APEJ-V
Figure10 DepthestimationcomparisononNYUandKITTIdatasets. While V-JEPA 2 captures the overall scene geometry,
its predictions lack local consistency and precise boundary structure. In contrast, our V-JEPA 2.1 produces sharper,
more coherent, and fine-grained depth maps.
PE -G (0.362 RMSE on NYU), and it represents a significant improvement over video encoders such as
spatial
InternVideo2-1B (0.471 RMSE) and V-JEPA 2 (0.642 RMSE). Figure 10 provides a qualitative comparison
of the depth maps predicted by V-JEPA 2 and V-JEPA 2.1. While V-JEPA 2 captures the overall scene
geometry, the inconsistencies of its local features lead to noisy depth maps. In contrast, our novel V-JEPA 2.1
produces sharper and more coherent depth maps with well-defined object boundaries. We also visualize a
more detailed qualitative comparative with DINOv3 ViT-H+ in Figure 12.
In semantic segmentation, V-JEPA 2.1 is also highly competitive with the state-of-the-art models, obtaining
85.0 mIoU on VOC12, 73.5 mIoU on Cityscapes and 47.9 mIoU on ADE20K. Compared with its previous
versionV-JEPA2,thegainsareremarkableacrossalldatasets: +23.4pointsinADE20K,+27.6onCityscapes,
and + 20.7 on VOC12; showing the benefits of explicitly supervising the context tokens and incorporating the
multi-level predictor.
Performance on ADE20K and Cityscapes remains slightly behind the best image encoders. These datasets
containnumerousobjectclassesspanninglargescalevariations, withclutteredscenelayoutsthatimposestrict
demands on fine-grained segmentation. We hypothesize that VisionMix contains comparatively fewer highly
clutteredscenes,limitingexposuretothelevelofgranularityrequiredbysuchbenchmarks. Figure11illustrates
segmentation predictions on Cityscapes and VOC12. V-JEPA 2.1 yields detailed and spatially accurate masks,
capturing multi-scale structures and fine object contours with high fidelity, showing competitive performance
with state-of-the-art methods such as DINOv3 ViT-H+ (Siméoni et al., 2025).
3.6 VideoObjectSegmentation
We evaluate V-JEPA 2.1 on Video Object Segmentation (VOS) to assess the temporal consistency of its
learned features.
Task. Video Object Segmentation consists in, given the ground-truth object mask in the first frame,
propagating this mask accurately across all subsequent frames. This task evaluates the model’s ability to
preserve long-range correspondences while remaining robust to camera motion, object deformation, and visual
distractions. We evaluate on DAVIS 2017 (Pont-Tuset et al., 2017) and YouTube-VOS (Xu et al., 2018)
datasets, reporting the standard J&F-mean metric (Perazzi et al., 2016) that jointly measures the region
similarity and contour accuracy.
16

|     | Image | Ground-truth | DINOv3 |     | V-JEPA2      | V-JEPA2.1       |     |
| --- | ----- | ------------ | ------ | --- | ------------ | --------------- | --- |
|     |       |              |        |     | The previous | version, V-JEPA | 2,  |
Figure11 SemanticsegmentationqualitativeresultsinVOC12andCityscapesdatasets.
produced sparse semantic masks due to the presence noisy feature maps. However, V-JEPA 2.1 achieves competitive
| performance | with state | of the art methods | such as DINOv3 | ViT-H+. |     |     |     |
| ----------- | ---------- | ------------------ | -------------- | ------- | --- | --- | --- |
Evaluation protocol. We adopt a non-parametric label propagation approach (Jabri et al., 2020) that
matches local patch features across frames using cosine similarity in the embedding space. This procedure
introduces no learnable parameters, making it a direct probe of the representation’s temporal stability.
Following Siméoni et al. (2025), input videos are resized to produce a consistent number of patch tokens
(short side of 420 px for patch size 14, and 480 px for patch size 16). On the training split of each dataset, we
conduct a systematic search of the best hyper-parameters: maximum context length, neighborhood mask size,
number of top-K nearest neighbors, and the temperature parameter used in similarity computation. The best
configuration in DAVIS-S (15 context frames, circle mask of size 12, top-5 neighbors and temperature = 0.2),
| was applied | to all the | validation sets. |     |     |     |     |     |
| ----------- | ---------- | ---------------- | --- | --- | --- | --- | --- |
Results. V-JEPA2.1achieves69.0J&F onDAVIS-17and72.7J&F onYouTube-VOSdatasets,obtaining
the second best performance and surpassing all prior encoders except DINOv3, which attains a slightly higher
score. These results highlight the temporal consistency of the V-JEPA 2.1 features, which enable stable
object tracking despite significant appearance changes across frames. Figure 13 illustrates two qualitative
examples: even under fast motion and substantial visual variations, V-JEPA 2.1 maintains consistent object
| segmentation | masks | throughout the | sequence. |     |     |     |     |
| ------------ | ----- | -------------- | --------- | --- | --- | --- | --- |
3.7 VideoandImageClassification
Real-world video reasoning requires recognizing static visual cues (i.e, objects, textures, scene layouts) as well
as dynamic patterns (i.e, gestures, hand-object interactions, camera motion, long-term temporal evolution).
17

| InitialGTframe |     |     |     |     |     |       | Framessequence |              |              |     |             |           |
| -------------- | --- | --- | --- | --- | --- | ----- | -------------- | ------------ | ------------ | --- | ----------- | --------- |
|                |     |     |     |     |     | Given | the            | ground-truth | object masks | for | the initial | frame, we |
Figure13 VideoObjectSegmentationqualitativeexamples.
propagate the instance masks to subsequent frames based on patch similarity within the V-JEPA 2.1 embedding space.
| All videos | are processed |     | at a | resolution | where the    | shorter side   | is set | to 480   | pixels.               |     |            |        |
| ---------- | ------------- | --- | ---- | ---------- | ------------ | -------------- | ------ | -------- | --------------------- | --- | ---------- | ------ |
|            |               |     |      | We         | report Top-1 | classification |        | accuracy | on action recognition |     | benchmarks | (SSv2, |
Table9 Performanceonglobaltasks.
Diving-48, and K400) and image classification (IN1K). Our protocol uses a resolution of 256×256 by default, and
384×384 for V-JEPA 2 ViT-g and V-JEPA 2.1; and uses 16×2×3 inputs for SSv2 (16-frame clips, 2 temporal
crops, 3 spatial crops), 16×8×3 for K400, and 32×4×3 for Diving-48. V-JEPA 2.1 VIT-G achieves state-of-art
performance on the SSv2 action recognition asks while being competitive on appearance understanding tasks.
| Method          |            |           |            |               | Param.   | Motion | Understanding |           | Appearance |     | Understanding |     |
| --------------- | ---------- | --------- | ---------- | ------------- | -------- | ------ | ------------- | --------- | ---------- | --- | ------------- | --- |
|                 |            |           |            |               |          | SSv2   |               | Diving-48 | K400       |     | IN1K          |     |
| Results         | Reported   | in the    | Literature |               |          |        |               |           |            |     |               |     |
| VideoMAEv2      |            | (Wang     | et al.,    | 2023)         | 1B       | 56.1   |               | –         | 82.8       |     | 71.4          |     |
| InternVideo2-1B |            | (Wang     | et al.,    | 2024b)        | 1B       | 67.3   |               | –         | 87.9       |     |               | –   |
| VideoPrism      | (Zhao      | et        | al., 2024) |               | 1B       | 68.5   |               | 71.3      | 87.6       |     |               | –   |
| DINOv3          | ViT-H+     | (Siméoni  |            | et al., 2025) | 0.8B     | 69.8   |               | –         | 86.7       |     | 87.9          |     |
| DINOv3          | (Siméoni   | et        | al., 2025) |               | 7B       | 70.1   |               | –         | 87.8       |     | 88.4          |     |
| Image Encoders  |            | Evaluated | Using      | the Same      | Protocol |        |               |           |            |     |               |     |
| DINOv2          | (Darcet    | et al.,   | 2023)      |               | 1.1B     | 50.7   |               | 82.5      | 83.6       |     | 86.1          |     |
| PE G            | (Bolya     | et al.,   | 2025)      |               | 1.9B     | 55.4   |               | 76.9      | 88.5       |     | 87.6          |     |
| core            |            |           |            |               |          |        |               |           |            |     |               | ∗   |
| SigLIP2         | (Tschannen | et        | al., 2025) |               | 1.2B     | 49.9   |               | 75.3      | 87.3       |     | 88.0          |     |
| Video Encoders  |            | Evaluated | Using      | the Same      | Protocol |        |               |           |            |     |               |     |
| InternVideo2    |            | -1B (Wang | et         | al., 2024b)   | 1B       | 69.7   |               | 86.4      | 89.4       |     | 85.8          |     |
2s
| V-JEPA | ViT-H     | (Bardes | et al., | 2024)      | 600M | 74.3 |     | 87.9 | 84.5 |     | 80.0 |     |
| ------ | --------- | ------- | ------- | ---------- | ---- | ---- | --- | ---- | ---- | --- | ---- | --- |
| V-JEPA | 2 ViT-g   | (Assran | et      | al., 2025) | 1B   | 77.3 |     | 90.2 | 87.3 |     | 85.1 |     |
| V-JEPA | 2.1 ViT-g |         |         |            | 1B   | 76.9 |     | 89.0 | 87.0 |     | 84.8 |     |
| V-JEPA | 2.1 ViT-G |         |         |            | 2B   | 77.7 |     | 89.2 | 87.7 |     | 85.5 |     |
Tocapturethisdualnature,weevaluatetherepresentationslearnedduringpretrainingonfourcomplementary
classification datasets. Something-Something v2 (Goyal et al., 2017) and Diving-48 (Li et al., 2018) assess
motion-centric understanding, as their labels require modeling multi-frame dynamics to correctly identify the
action. In contrast, Kinetics-400 (Kay et al., 2017) and ImageNet-1K (Deng et al., 2009) primarily measure
appearance-based recognition, since many of their classes can be predicted from a single frame, even when the
| label describes |     | an action. |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Task. We compare the video classification performance of V-JEPA 2.1 against a broad set of visual encoders.
For image-based self-supervised models, we include DINOv2 with registers (Darcet et al., 2023) and the more
recent DINOv3 (Siméoni et al., 2025), both representing state-of-the-art in image-only pretraining. We further
evaluate against leading image–text contrastive approaches, including SigLIP2 (Tschannen et al., 2025) and
the Perception Encoder PE G (Bolya et al., 2025). For video models, we benchmark against the previous
core
V-JEPA (Bardes et al., 2024) and V-JEPA 2 (Assran et al., 2025), as well as InternVideo2s2-1B (Wang et al.,
2024b), a state-of-the-art video encoder trained primarily through vision–text contrastive objectives.
In addition, we report comparisons with results available in the literature for VideoMAEv2 (Wang et al.,
2023), InternVideo2-1B (Wang et al., 2024b), VideoPrism (Zhang et al., 2024), and DINOv3 (Siméoni et al.,
18

Table10 VideoQAresults. We report the performance of VJEPA 2.1 trained with Llama 3.1 8B backbone on several
popular temporal video understanding datasets. We train on a modified subset of the PerceptionLM (Cho et al., 2025)
data, and compare to VJEPA 2 (Assran et al., 2025) by training it on the same data regime. VJEPA 2.1 achieves
comparatively better performance than VJEPA 2 on several video understanding tasks which require both rich visual
information and temporal understanding. For PerceptionTest (Pătrăucean et al., 2023), we report the validation
accuracy, as the test server to compute the test accuracy (indicated by *) is no longer active.
hcneBlaropmeT )AQtrohs-ABM(
|     |     |     |     |     |     | tseTnoitpecreP | ssapmoCpmeT             |     |                |         |
| --- | --- | --- | --- | --- | --- | -------------- | ----------------------- | --- | -------------- | ------- |
|     |     |     |     |     |     |                | ccA-deriaP eciohc-itlum |     | OTAMOT hcneBVT | hcneBVM |
ccAtseT
|        |     |     |     | P ar a m | s    |     | PVM |     |         |     |
| ------ | --- | --- | --- | -------- | ---- | --- | --- | --- | ------- | --- |
| Method |     |     |     |          | Avg. |     |     |     | ccA ccA | ccA |
En c / L L M
| ≤8B Video | Language | Models | Results | Reported in | the Literature |     |     |     |     |     |
| --------- | -------- | ------ | ------- | ----------- | -------------- | --- | --- | --- | --- | --- |
InternVL-2.5(Chenetal.,2024) 300M/7B 52.1 68.9 39.9 68.3 24.3 29.4 61.6 72.6
Qwen2VL(Wangetal.,2024a) 675M/7B 47.0 66.9 29.2 67.9 20.4 31.5 46.0 67.0
Qwen2.5VL(QwenTeametal.,2025) 1B/7B 49.7 70.5 36.7 71.7 24.5 24.6 50.5 69.6
PLM8B(Choetal.,2025) 1B/8B 56.7 82.7* 39.7 72.7 28.3 33.2 63.5 77.1
VJEPA2ViT-g384 (Assranetal.,2025) 1B/8B 59.5 84.0* 44.5 76.9 36.7 40.3 60.6 73.5
| Models         | trained in   | this paper | using filtered | Perception | LM data (Cho | et al., | 2025)     |      |           |      |
| -------------- | ------------ | ---------- | -------------- | ---------- | ------------ | ------- | --------- | ---- | --------- | ---- |
| VJEPA2ViT-g384 |              |            |                | 1B/8B      | 57.8         | 80.1    | 40.9 74.1 | 32.3 | 41.4 62.6 | 73.3 |
| VJEPA          | 2.1 ViT-G384 |            |                | 2B/8B      | 57.9         | 83.1    | 43.2 74   | 28.5 | 38 62.8   | 75.4 |
2025). Note that these models are evaluated under similar frozen-probe protocols, but their attentive heads
differ from ours. For instance, DINOv3 augments its probe with explicit spatial and temporal positional
embeddings and applies a 3D factorized RoPE across its attention blocks. In contrast, our V-JEPA 2.1
encoder already encodes spatio–temporal structure in its features, allowing our probe to operate without such
| additional | components. |     |     |     |     |     |     |     |     |     |
| ---------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Evaluation protocol. Following the protocol proposed by Assran et al. (2025), we train a 4-layers attentive
probe on top of the frozen encoder features using the respective training data from each task. The attentive
probeconsistsoffourtransformerblocksfollowedbyafinalcross-attentionmechanismthatemploysalearnable
query token. At inference, we sampled several clips with a fixed number of frames from the video, and we
| averaged | the classification |     | logits across | clips. |     |     |     |     |     |     |
| -------- | ------------------ | --- | ------------- | ------ | --- | --- | --- | --- | --- | --- |
Table 9 summarizes the global video understanding performance of V-JEPA 2.1, previous V-JEPA
Results.
models, and other strong visual encoders. V-JEPA 2.1 ViT-G achieves a top-1 accuracy of 77.7 on SSv2,
setting a new absolute state-of-the-art on the task compared to 77.5 for InternVideo2 full fine-tuning, 77.3 for
V-JEPA 2, 70.1 for DINOv3 ViT-7B and 69.7 for InternVideo2 using the same protocol, demonstrating a
strong understanding of video dynamics. Our model is also highly-competitive in appearance-based tasks,
reaching 87.7 on K400 and 85.5 on IN1K. These results show that properly designing the loss over context
tokens, together with deep self-supervision, enables fine-grained dense features that also capture strong global
scene understanding. We also observe consistent improvements with model scaling from ViT-g to ViT-G with
| an average | improvement | of  | +0.6 points. |     |     |     |     |     |     |     |
| ---------- | ----------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
3.8 VideoQuestionAnswering
In this section, we evaluate V-JEPA 2.1 on Video Question Answering (VidQA), by training a Video Large
Language Model (VidLLM) using V-JEPA 2.1 encoder and Llama 3.1 8B LLM as the backbone, following the
| recipe proposed | by  | Assran | et al. (2025). |     |     |     |     |     |     |     |
| --------------- | --- | ------ | -------------- | --- | --- | --- | --- | --- | --- | --- |
Task. We compare the VidQA performance of V-JEPA 2.1 with popular open-source multimodal models
reported in the literature, where the LLM backbone size is ≤ 8B. Following the protocol set of Assran et al.
(2025), we report performance on video understanding benchmarks which require rich visual and temporal
understanding, such as PerceptionTest (Pătrăucean et al., 2023), Minimal Video Pairs (MVP) (Krojer et al.,
2024), TempCompass (Liu et al., 2024), TemporalBench (Cai et al., 2024), TOMATO (Shangguan et al., 2024)
| and MVBench | (Li | et al., | 2024). |     |     |     |     |     |     |     |
| ----------- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
19

Evaluation protocol. We train our Video-LLM model using a subset of PerceptionLM that is publicly
available (Cho et al., 2025). Starting with this data, we perform data quality filtering using domain filters,
vision-textmisalignmentfilters,andanexternalmultimodalLLM,Qwen3VL,asadata-qualityjudge,assigning
scores to each data samples. This process resulted us to filter out and remove of the training data. It is
18%
important to note that we do not rephrase any data from PerceptionLM (Cho et al., 2025) using this setup -
we only filter the data based on the model’s judgement.
We reproduced LLM alignment of VJEPA 2 on this new data, and compare our model, VJEPA 2.1, with it.
Wefollowthesamethree-stagetrainingprocedurefromAssranetal.(2025)totrainVJEPA2.1LLM,starting
from image-text captioning to progressively training on higher quality image and video-text captioning and
QA data. We further add a fourth stage of alignment, where we expand the context length of the base LLM
to support 64 frames of video input, compared to 32 frames supported by VJEPA 2 (Assran et al., 2025).
We primarily use VJEPA 2.1 in video-only mode in our experiments, to better compare with VJEPA 2.
Interestingly, we find adding a final post-training stage using PerceptionTest training set further improves
performance on all downstream tasks.
Results. Table 10 summarizes the results on VidQA evaluation tasks. Comparing VJEPA 2 and VJEPA
2.1 on the same data, we find on average VJEPA 2.1 to be slightly better, with significant improvements on
PerceptionTest, Minimal Video Pairs, and crucially, improvement on datasets requiring rich visual semantics
- MVBench and TVBench. We observe VJEPA 2.1 to be worse on TemporalBench and TOMATO - both
datasets requiring understanding of the motion events, but on shorter videos.
Compared to results reported in the literature, VJEPA 2.1 slightly underperforms results reported Assran
et al. (2025) which uses significantly alignment data (88.5 million samples in (Assran et al., 2023) vs 72.5
million samples in VJEPA 2.1) Nevertheless, VJEPA 2.1 is competitive with state-of-the-art, outperforming
most open-source multimodal LLMs with similar model size.
3.9 QualitativeresultsofV-JEPA2.1DenseFeatures
Figure 14 presents a comparison of dense feature maps obtained from a single image using V-JEPA 2.1 ViT-G,
DINOv2 ViT-g (Oquab et al., 2023), DINOv3 ViT-H+ (Siméoni et al., 2025) and V-JEPA 2 ViT-g (Assran
et al., 2025). We project each encoder’s feature space into three dimensions using PCA. Following Siméoni
et al. (2025), we permute the three components across the six possible RGB channels permutations, and we
display the most visually appealing. The qualitative results in Figure 14 illustrate the high-quality of V-JEPA
2.1 dense feature maps obtained from a single image, which show fine-grained and precise identification of
objects, such as the cat’s fur details or pedestrians in Cityscapes scenes. Figure 15 further extends this
comparison to full video sequences of 64 frames, showing temporal consistent dense maps across diverse
scenarios, including egocentric videos from Ego4D (Grauman et al., 2022), Cityscapes sequences (Cordts et al.,
2016), Diving48 videos (Li et al., 2018) and animal camouflage footage from MOC (Lamdouar et al., 2020).
3.10 Familyofdistilledmodels
We follow the same protocol to evaluate our distilled ViT-L and ViT-B models. Table ?? presents our results,
whereweobserveasignificantimprovementinallourbenchmarksbetweentheViT-Ltrainedfromscratchand
the ViT-L distilled from ViT-G, almost closing the gap with ViT-G performance. On action recognition on
SSv2, performance improves from 74.2% to 76.5%, almost reaching 77.7% from ViT-G. In image segmentation
onADE20k,performanceimprovesfrom42.0mIoUto46.7mIoU.Indepthestimationandvideosegmentation,
the ViT-L distilled is even closer to ViT-G, with 2.490 RMSE on KITTI, close to 2.461 RMSE, and 68.7
J&F-Mean on DAVIS, close to 67.0 J&F-Mean. Finally, our ViT-B offers competitive performance with our
ViT-L trained from scratch.
4 Relatedwork
Early SSL approaches in vision focus on simple pretext tasks such as predicting
Self-SupervisedLearning.
the relative position of image patches (Doersch et al., 2015), reordering shuffled patches (Noroozi and Favaro,
20

| Image |     | DINOv2 | DINOv3 | V-JEPA2 | V-JEPA2.1 |
| ----- | --- | ------ | ------ | ------- | --------- |
Figure14 ComparisonofdensefeaturesproducedbydifferentSSLmethodsonasingleimage. We compare DINOv2 ViT-g
(Oquab et al., 2023), DINOv3 ViT-H+ (Siméoni et al., 2025) and V-JEPA 2 ViT-g (Assran et al., 2025) against
V-JEPA 2.1 ViT-G. Images are resized so that their shorter side is set to 1024 pixels, after which they are processed
| using the | 2D convolution | image tokenizer. |     |     |     |
| --------- | -------------- | ---------------- | --- | --- | --- |
21

Figure15 V-JEPA2.1unlocksdensefeaturesfromvideo. Qualitative results on Ego4D (1080px), Cityscapes (1080px),
Diving48 (768px), and MOCA (768px) illustrate the strong temporal consistency of the dense features produced
by our ViT-G model, particularly on dynamic objects. Since we process entire video sequences, we employ the 3D
convolutional video tokenizer.
22

2016; Misra and Maaten, 2020), inpainting missing regions (Pathak et al., 2016), re-colorizing grayscale
images (Zhang et al., 2016), or predicting applied image transformations (Gidaris et al., 2018). Beyond hand-
crafted tasks, view-invariant approaches proposed to use a joint-embedding architecture to learn invariances
to visual transformations, which led to significant advances in SSL, with contrastive approaches (Hénaff
et al., 2019; He et al., 2020; Chen et al., 2020), non-contrastive approaches (Chen and He, 2020; Grill
et al., 2020b; Bardes et al., 2021), or clustering-based techniques (Caron et al., 2018, 2020). Later, the
adoption of vision transformers (Dosovitskiy, 2020) became the standard in self-supervised learning, first by
revisiting existing view-invariant approaches (Chen et al., 2021; Caron et al., 2021), and then with masked
image modeling approaches, which can operate in pixel space (Xie et al., 2021b; Wei et al., 2021), or in
the latent space of the transformer (Bao et al., 2021). Most powerful approaches employ a combination of
view-invariant and masked image-modeling techniques (Zhou et al., 2021; Oquab et al., 2023). The concept of
learningrepresentationsbypredictingmissinginformationinlatentspaceisformalizedbytheJoint-Embedding
PredictiveArchitecture(JEPA)(LeCun,2022),whichhavebeensuccessfullyappliedacrossmultiplemodalities,
including audio (Baevski et al., 2022), images (Assran et al., 2023; Bar et al.), and video (Bardes et al., 2024).
Motion cues from videos have inspired many early video pretext tasks. Early methods
Video Models.
predicted camera transformations between image pairs (Agrawal et al., 2015) or future frames from ego-
motion (Jayaraman and Grauman, 2015). Others brought consecutive frame patches closer in feature
space (Wang and Gupta, 2015) or used unsupervised object retrieval for segmentation (Pathak et al., 2017).
The rise a large labeled video datasets such as Kinetics (Carreira and Zisserman, 2017) changed the focus
of the community towards supervised video models. Early approaches used image sequences with late
fusion (Donahue et al., 2015) or 3D convolutions (Tran et al., 2015), but 3D ConvNets are computationally
expensive. Recent work improves efficiency with 2D spatial and 1D temporal convolutions (Tran et al., 2018;
Xie et al., 2018), dual-pathways (Feichtenhofer et al., 2019), and vision transformers adapted for video (Arnab
et al., 2021; Bertasius et al., 2021). Despite rapid progress, supervised learning requires extensive labeled
data and may not fully exploit temporal information, and the focus went back to self-supervised learning.
Early self-supervised learning methods focused on temporal order verification (Misra et al., 2016; Xu et al.,
2019), contrastive learning (Han et al., 2020; Dave et al., 2022), and future prediction (Han et al., 2019).
Recent masked modeling approaches, like VideoMAE (Tong et al., 2022; Feichtenhofer et al., 2022), extend
image-based masking to video. Other advances include masked modeling in CLIP space (Li et al., 2023), joint
image-video training (OmniMAE (Girdhar et al., 2023)), and architectural innovations such as hierarchical
transformers (Ryali et al., 2023) and decoupled encoders/decoders (Gupta et al., 2023). Despite progress,
defining optimal pretext tasks and efficient video processing remain open challenges.
Scaling existing approaches, both in terms of data and model size, has demonstrated that generalist video
encoders can be learned from extensive observation datasets of videos using self-supervised learning (Carreira
et al., 2024; Wang et al., 2023; Rajasegaran et al., 2025). In particular, Joint-Embedding Predictive
architectures show promising efficiency gains at large scale compared to generative approaches (Bardes et al.,
2024), and open the door to applications in world modeling (Assran et al., 2025). Self-supervised models
can also incorporated weak language supervision (Zhao et al., 2024; Wang et al., 2024b; Bolya et al., 2025),
unlocking language-based tasks.
Learningdensefeatures. Learning dense features is often achieved through designing local loss functions and
objectives, such as leveraging spatio-temporal consistency in videos (Jabri et al., 2020), spatial alignment
between image crops (Pinheiro et al., 2020; Bardes et al., 2022), and patch consistency (Yun et al., 2022).
Contrastive learning approaches such as DetCon (Hénaff et al., 2021) and ORL (Xie et al., 2021a) use
region proposals, while newer methods relax this requirement (Hénaff et al., 2022; Wen et al., 2022). Recent
distillation-based methods combine strengths from multiple encoders, such as AM-RADIO (Ranzinger
et al., 2024), Perception Encoder (Bolya et al., 2025), and DINOv3 (Siméoni et al., 2025), using objectives
like cosine similarity and Gram matrix regularization to improve dense features. Some works focus on
post-hoc improvements, including fine-tuning with clustering objectives (Ziegler and Asano, 2022), patch
alignment (Salehi et al., 2023), and patch-sorting (Pariza et al., 2025). Others enhance features without
fine-tuning, such as STEGO (Hamilton et al., 2022) and feature augmentation (Simoncini et al., 2024).
Beyondplayingwiththelossfunction,thestandardVisionTransformer(ViT)(Dosovitskiyetal.,2021)canbe
23

adapted for dense prediction tasks, Ranftl et al. (2021) introduced the Dense Prediction Transformer (DPT),
evolving from their prior CNN-based work on MiDaS (Ranftl et al., 2020). DPT solved the token-to-pixel
problem using a "reassemble" operation that converts the 1D ViT sequence into multi-scale 2D feature maps,
which are then fused by a convolutional decoder adapted from RefineNet (Lin et al., 2017a). This design,
which leverages the global receptive field of the transformer backbone, proved effective for obtaining structural
coherence, moving beyond the limitations of purely hierarchical CNNs. The work also catalyzed parallel
research, including the development of purely transformer-based decoders like Segmenter (Strudel et al., 2021)
and hierarchical transformer backbones like the Swin Transformer (Liu et al., 2021) and the Multiscale Vision
Transformer (Fan et al., 2021). DPT architectural framework has proven to be the most influential design for
scaling up, serving as the basis for current state-of-the-art foundation models like Depth Anything (Yang
et al., 2024).
5 ConclusionandFuturework
This work demonstrates how Joint-Embedding Predictive Architectures and Self-Supervised Learning from
videounlockhigh-qualitydenselocalfeatureswithstrongglobalsemanticunderstanding. Ourkeyingredientis
a novel deep spatio-temporal self-supervision, composed by a weighted context loss and a multi-level predictor
that enables supervision across the intermediate encoder layers. This design unlocks high-quality dense
features that are spatially structured, semantically coherent and temporally consistent, as evidenced by PCA
visualizations. Beyond the training objective, we demonstrate the importance of modality-specific tokenizers,
large-scale and balanced image–video data curation, and scaling to ViT-G, which together enable an effective
distillation to compact models. Our V-JEPA 2.1 ViT-G achieves absolute state-of-the-art performance in
short-term object interaction anticipation, action anticipation and action recognition, showcasing its excellent
predictive and motion understanding capabilities. Moreover, the dense feature maps achieve linear-probe
state-of-the-art performance in monocular depth estimation and strong results in semantic segmentation
and video object tracking. We hope these findings encourage further research on predictive physical world
modeling.
Future work. Futureworkwillfocusonseveralpromisingdirections. First,scalingalongtwoaxes: a)model
size,weobserveaverypositivetrendscalingfrom1Bto2BandotherworksuchasDINOv3showedthebenefit
ofscalingto7Binvision;b)datasize,ourworkondatacurationhighlightedthatvideoself-supervisedlearning
really benefit from large-scale datasets. Second, this work focus on learning better representation, whereas
V-JEPA 2 showed the potential of building world models on top of these representations. Future work in this
directionwillexploreworldmodelingaspectswiththeprismoflearningdensepredictioncapabilities(Karypidis
et al., 2024; Bojanowski, 2025). Finally, world models with dense understanding and prediction abilities will
unlock many applications in robotics and autonomous agents, where a precise estimation of the state down
to the pixel level is required, for example navigation in challenging real world environment, or fine-grained
manipulation.
24

References
Pulkit Agrawal, Joao Carreira, and Jitendra Malik. Learning to see by moving. In ICCV, 2015.
AnuragArnab,MostafaDehghani,GeorgHeigold,ChenSun,MarioLucic,andCordeliaSchmid. Vivit: Avideovision
| transformer. | In ICCV, 2021. |     |     |     |     |
| ------------ | -------------- | --- | --- | --- | --- |
Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and
Nicolas Ballas. Self-supervised learning from images with a joint-embedding predictive architecture. In Proceedings
of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 15619–15629, 2023.
Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Matthew Muckley, Ammar Rizvi, Claire
Roberts, Koustuv Sinha, Artem Zholus, et al. V-jepa 2: Self-supervised video models enable understanding,
| prediction | and planning. arXiv | preprint | arXiv:2506.09985, | 2025. |     |
| ---------- | ------------------- | -------- | ----------------- | ----- | --- |
AlexeiBaevski,Wei-NingHsu,QiantongXu,ArunBabu,JiataoGu,andMichaelAuli. Data2vec: Ageneralframework
for self-supervised learning in speech, vision and language. arXiv preprint arXiv:2202.03555, 2022.
Randall Balestriero and Yann LeCun. Lejepa: Provable and scalable self-supervised learning without the heuristics.
| arXiv preprint | arXiv:2511.08544, | 2025. |     |     |     |
| -------------- | ----------------- | ----- | --- | --- | --- |
Hangbo Bao, Li Dong, and Furu Wei. Beit: Bert pre-training of image transformers. arXiv preprint arXiv:2106.08254,
2021.
AmirBar,FlorianBordes,AssafShocher,MidoAssran,PascalVincent,NicolasBallas,TrevorDarrell,AmirGloberson,
and Yann LeCun. Stochastic positional embeddings improve masked image modeling. In Forty-first International
| Conference | on Machine Learning. |     |     |     |     |
| ---------- | -------------------- | --- | --- | --- | --- |
Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation world models. In Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 15791–15801, June 2025.
Adrien Bardes, Jean Ponce, and Yann LeCun. Vicreg: Variance-invariance-covariance regularization for self-supervised
| learning. arXiv | preprint arXiv:2105.04906, |     | 2021. |     |     |
| --------------- | -------------------------- | --- | ----- | --- | --- |
Adrien Bardes, Jean Ponce, and Yann LeCun. Vicregl: Self-supervised learning of local visual features. NeurIPS, 2022.
AdrienBardes,QuentinGarrido,JeanPonce,XinleiChen,MichaelRabbat,YannLeCun,MahmoudAssran,andNicolas
Ballas. Revisitingfeaturepredictionforlearningvisualrepresentationsfromvideo. arXiv preprint arXiv:2404.08471,
2024.
GedasBertasius,HengWang,andLorenzoTorresani. Isspace-timeattentionallyouneedforvideounderstanding? In
ICML, 2021.
Federico Baldassarre Marc Szafraniec Basile Terver Vasil Khalidov Francisco Massa Yann LeCun Patrick Labatut
Maximilian Seitzer Piotr Bojanowski. Back to the features: Dino as a foundation for video world models. arXiv
| preprint arXiv:2507.19468, |     | 2025. |     |     |     |
| -------------------------- | --- | ----- | --- | --- | --- |
DanielBolya,Po-YaoHuang,PeizeSun,JangHyunCho,AndreaMadotto,ChenWei,TengyuMa,JialeZhi,Jathushan
Rajasegaran, Hanoona Rasheed, et al. Perception encoder: The best visual embeddings are not at the output of the
| network. arXiv | preprint arXiv:2504.13181, |     | 2025. |     |     |
| -------------- | -------------------------- | --- | ----- | --- | --- |
MuCai,ReubenTan,JianruiZhang,BochengZou,KaiZhang,FengYao,FangruiZhu,JingGu,YiwuZhong,Yuzhang
Shang, Yao Dou, Jaden Park, Jianfeng Gao, Yong Jae Lee, and Jianwei Yang. Temporalbench: Benchmarking
fine-grained temporal understanding for multimodal video models. arXiv preprint arXiv:2410.10818, 2024.
MathildeCaron,PiotrBojanowski,ArmandJoulin,andMatthijsDouze. Deepclusteringforunsupervisedlearning. In
ECCV, 2018.
Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, and Armand Joulin. Unsupervised
| learning of | visual features by | contrasting | cluster assignments. | In NeurIPS, | 2020. |
| ----------- | ------------------ | ----------- | -------------------- | ----------- | ----- |
Mathilde Caron, Hugo Touvron, Ishan Misra, Herve Jegou, and Julien Mairal Piotr Bojanowski Armand Joulin.
| Emerging | properties in self-supervised |     | vision transformers. | In ICCV, 2021. |     |
| -------- | ----------------------------- | --- | -------------------- | -------------- | --- |
Joao Carreira, Eric Noland, Chloe Hillier, and Andrew Zisserman. A short note on the kinetics-700 human action
| dataset. arXiv | preprint arXiv:1907.06987, |     | 2019. |     |     |
| -------------- | -------------------------- | --- | ----- | --- | --- |
25

JoãoCarreiraandAndrewZisserman. Quovadis,actionrecognition? anewmodelandthekineticsdataset. InCVPR,
2017.
JoãoCarreira,DilaraGokay,MichaelKing,ChuhanZhang,IgnacioRocco,AravindhMahendran,ThomasAlbertKeck,
Joseph Heyward, Skanda Koppula, Etienne Pot, Goker Erdogan, Yana Hasson, Yi Yang, Klaus Greff, Guillaume Le
Moing, Sjoerd van Steenkiste, Daniel Zoran, Drew A. Hudson, Pedro Vélez, Luisa Polanía, Luke Friedman, Chris
Duvarney, Ross Goroshin, Kelsey Allen, Jacob Walker, Rishabh Kabra, Eric Aboussouan, Jennifer Sun, Thomas
Kipf, Carl Doersch, Viorica Pătrăucean, Dima Damen, Pauline Luc, Mehdi S. M. Sajjadi, and Andrew Zisserman.
Scaling 4d representations. arXiv preprint arXiv:2412.15212, 2024.
Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey E. Hinton. A simple framework for contrastive
learning of visual representations. In ICML, 2020.
Xinlei Chen and Kaiming He. Exploring simple siamese representation learning. In CVPR, 2020.
Xinlei Chen, Saining Xie, and Kaiming He. An empirical study of training self-supervised vision transformers. In
ICCV, 2021.
Zhe Chen, Weiyun Wang, Yue Cao, Yangzhou Liu, Zhangwei Gao, Erfei Cui, Jinguo Zhu, Shenglong Ye, Hao Tian,
Zhaoyang Liu, Lixin Gu, Xuehui Wang, Qingyun Li, Yimin Ren, Zixuan Chen, Jiapeng Luo, Jiahao Wang, Tan
Jiang, Bo Wang, Conghui He, Botian Shi, Xingcheng Zhang, Han Lv, Yi Wang, Wenqi Shao, Pei Chu, Zhongying
Tu, Tong He, Zhiyong Wu, Huipeng Deng, Jiaye Ge, Kai Chen, Kaipeng Zhang, Limin Wang, Min Dou, Lewei Lu,
Xizhou Zhu, Tong Lu, Dahua Lin, Yu Qiao, Jifeng Dai, and Wenhai Wang. Expanding performance boundaries of
open-source multimodal models with model, data, and test-time scaling. arXiv preprint arXiv:2412.05271, 2024.
Jang Hyun Cho, Andrea Madotto, Effrosyni Mavroudi, Triantafyllos Afouras, Tushar Nagarajan, Muhammad Maaz,
YaleSong,TengyuMa,ShumingHu,SuyogJain,MiguelMartin,HuiyuWang,HanoonaRasheed,PeizeSun,Po-Yao
Huang, Daniel Bolya, Nikhila Ravi, Shashank Jain, Tammy Stark, Shane Moon, Babak Damavandi, Vivian Lee,
Andrew Westbury, Salman Khan, Philipp Krähenbühl, Piotr Dollár, Lorenzo Torresani, Kristen Grauman, and
Christoph Feichtenhofer. Perceptionlm: Open-access data and models for detailed visual understanding. arXiv
preprint arXiv:2504.13180, 2025.
MariusCordts,MohamedOmran,SebastianRamos,TimoRehfeld,MarkusEnzweiler,RodrigoBenenson,UweFranke,
Stefan Roth, and Bernt Schiele. The cityscapes dataset for semantic urban scene understanding. In Proceedings of
the IEEE conference on computer vision and pattern recognition, pages 3213–3223, 2016.
Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Antonino Furnari, Jian Ma, Evangelos Kazakos, Davide
Moltisanti, Jonathan Munro, Toby Perrett, Will Price, and Michael Wray. Rescaling egocentric vision: Collection,
pipeline and challenges for epic-kitchens-100. International Journal of Computer Vision (IJCV), 2022.
Timothée Darcet, Maxime Oquab, Julien Mairal, and Piotr Bojanowski. Vision transformers need registers. arXiv
preprint arXiv:2309.16588, 2023.
Ishan Dave, Rohit Gupta, Mamshad Nayeem Rizve, and Mubarak Shah. Tclr: Temporal contrastive learning for video
representation. Computer Vision and Image Understanding, 2022.
Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image
database. In 2009 IEEE conference on computer vision and pattern recognition, pages 248–255. Ieee, 2009.
Carl Doersch, Abhinav Gupta, and Alexei A. Efros. Unsupervised visual representation learning by context. In ICCV,
2015.
JeffDonahue,LisaAnneHendricks,SergioGuadarrama,MarcusRohrbach,SubhashiniVenugopalan,andKateSaenko.
Long-term recurrent convolutional networks for visual recognition and description. In CVPR, 2015.
Alexey Dosovitskiy. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint
arXiv:2010.11929, 2020.
Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner,
Mohammad Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby. An
image is worth 16x16 words: Transformers for image recognition at scale. In ICLR, 2021.
Mark Everingham, SM Ali Eslami, Luc Van Gool, Christopher KI Williams, John Winn, and Andrew Zisserman. The
pascalvisualobjectclasseschallenge: Aretrospective. International journal of computer vision,111(1):98–136,2015.
26

David Fan, Shengbang Tong, Jiachen Zhu, Koustuv Sinha, Zhuang Liu, Xinlei Chen, Michael Rabbat, Nicolas Ballas,
Yann LeCun, Amir Bar, and Saining Xie. Scaling language-free visual representation learning. arXiv preprint
| arXiv:2504.01017, | 2025. |     |     |     |
| ----------------- | ----- | --- | --- | --- |
Haoqi Fan, Bo Xiong, Karttikeya Mangalam, Yanghao Li, Zhicheng Yan, and Jitendra Malik. Multiscale vision
| transformers. | In ICCV, | 2021. |     |     |
| ------------- | -------- | ----- | --- | --- |
Christoph Feichtenhofer, Haoqi Fan, Jitendra Malik, and Kaiming He. Slowfast networks for video recognition. In
ICCV, 2019.
Christoph Feichtenhofer, Haoqi Fan, Yanghao Li, and Kaiming He. Masked autoencoders as spatiotemporal learners.
| In NeurIPS, | 2022. |     |     |     |
| ----------- | ----- | --- | --- | --- |
Quentin Garrido, Nicolas Ballas, Mahmoud Assran, Adrien Bardes, Laurent Najman, Michael Rabbat, Emmanuel
Dupoux, and Yann LeCun. Intuitive physics understanding emerges from self-supervised pretraining on natural
| videos. arXiv | preprint | arXiv:2502.11831, | 2025. |     |
| ------------- | -------- | ----------------- | ----- | --- |
Andreas Geiger, Philip Lenz, Christoph Stiller, and Raquel Urtasun. Vision meets robotics: The kitti dataset. In The
| International | Journal | of Robotics Research, | 2013a. |     |
| ------------- | ------- | --------------------- | ------ | --- |
Andreas Geiger, Philip Lenz, Christoph Stiller, and Raquel Urtasun. Vision meets robotics: The kitti dataset. The
| international | journal of | robotics research, | 32(11):1231–1237, | 2013b. |
| ------------- | ---------- | ------------------ | ----------------- | ------ |
S.Gidaris,P.Singh,andN.Komodakis. Unsupervisedrepresentationlearningbypredictingimagerotations. InICLR,
2018.
Rohit Girdhar, Alaaeldin El-Nouby, Mannat Singh, Kalyan Vasudev Alwala, Armand Joulin, and Ishan Misra.
Omnimae: Single model masked pretraining on images and videos. In CVPR, 2023.
Ross Girshick. Fast r-cnn. In Proceedings of the IEEE international conference on computer vision, pages 1440–1448,
2015.
Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, Joanna Materzynska, Susanne Westphal, Heuna Kim,
Valentin Haenel, Ingo Fruend, Peter Yianilos, Moritz Mueller-Freitag, et al. The" something something" video
database for learning and evaluating visual common sense. In Proceedings of the IEEE international conference on
| computer | vision, pages | 5842–5850, 2017. |     |     |
| -------- | ------------- | ---------------- | --- | --- |
Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson
Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video.
In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 18995–19012, 2022.
Jean-BastienGrill,FlorianStrub,FlorentAltché,CorentinTallec,PierreRichemond,ElenaBuchatskaya,CarlDoersch,
BernardoAvilaPires,ZhaohanGuo,MohammadGheshlaghiAzar,etal. Bootstrapyourownlatent-anewapproach
to self-supervised learning. Advances in neural information processing systems, 33:21271–21284, 2020a.
Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre H. Richemond, Elena Buchatskaya, Carl
Doersch, Bernardo Avila Pires, Zhaohan Daniel Guo, Mohammad Gheshlaghi Azar, Bilal Piot, Koray Kavukcuoglu,
RémiMunos,andMichalValko. Bootstrapyourownlatent: Anewapproachtoself-supervisedlearning. InNeurIPS,
2020b.
Ankush Gupta, Viorica Patraucean, Lucas Smaira, Larisa Markeeva, Menglin Chen, Teli He, Dylan Banarse, Antoine
Miech, Alex Frechette, Raphael Koster, et al. Decoupled video coding with decoupled video prediction. arXiv
| preprint | arXiv:2307.13532, | 2023. |     |     |
| -------- | ----------------- | ----- | --- | --- |
David Ha and Jürgen Schmidhuber. World models. arXiv preprint arXiv:1803.10122, 2(3), 2018.
MarkHamilton,ZhoutongZhang,BharathHariharan,NoahSnavely,andWilliamT.Freeman. Unsupervisedsemantic
| segmentation | by distilling | feature correspondences. |     | In ICLR, 2022. |
| ------------ | ------------- | ------------------------ | --- | -------------- |
TengdaHan,WeidiXie,andAndrewZisserman. Videorepresentationlearningbydensepredictivecoding. InWorkshop
| on Large | Scale Holistic | Video Understanding, | ICCV, | 2019. |
| -------- | -------------- | -------------------- | ----- | ----- |
Tengda Han, Weidi Xie, and Andrew Zisserman. Self-supervised co-training for video representation learning. In
| NeurIPS, | 2020. |     |     |     |
| -------- | ----- | --- | --- | --- |
Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick. Momentum contrast for unsupervised visual
| representation | learning. | In CVPR, 2020. |     |     |
| -------------- | --------- | -------------- | --- | --- |
27

Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network. arXiv preprint
arXiv:1503.02531, 2015.
Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. Advances in neural information
processing systems, 33:6840–6851, 2020.
Olivier J. Hénaff, Aravind Srinivas, Jeffrey De Fauw, Ali Razavi, Carl Doersch, S. M. Ali Eslami, and Aäron van den
Oord. Data-efficient image recognition with contrastive predictive coding. In ICML, 2019.
Olivier J. Hénaff, Skanda Koppula, Jean-Baptiste Alayrac, Aaron van den Oord, Oriol Vinyals, and João Carreira.
Efficient visual pretraining with contrastive detection. arXiv preprint arXiv:2103.10957, 2021.
Olivier J. Hénaff, Skanda Koppula, Evan Shelhamer, Daniel Zoran, Andrew Jaegle, Andrew Zisserman, João Carreira,
and Relja Arandjelović. Object discovery and representation networks. In ECCV, 2022.
Allan Jabri, Andrew Owens, and Alexei Efros. Space-time correspondence as a contrastive random walk. Advances in
neural information processing systems, 33:19545–19560, 2020.
D. Jayaraman and K. Grauman. Learning image representations tied to ego-motion. In ICCV, 2015.
Efstathios Karypidis, Ioannis Kakogeorgiou, Spyros Gidaris, , and Nikos Komodakis. Dino-foresight: Looking into the
future with dino. arXiv preprint arXiv:2412.11673, 2024.
WillKay,JoaoCarreira,KarenSimonyan,BrianZhang,ChloeHillier,SudheendraVijayanarasimhan,FabioViola,Tim
Green, Trevor Back, Paul Natsev, et al. The kinetics human action video dataset. arXiv preprint arXiv:1705.06950,
2017.
Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush
Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, Peter David Fagan, Joey Hejna, Masha
Itkina, Marion Lepert, Yecheng Jason Ma, Patrick Tree Miller, Jimmy Wu, Suneel Belkhale, Shivin Dass, Huy Ha,
ArhanJain,AbrahamLee,YoungwoonLee,MariusMemmel,SungjaePark,IlijaRadosavovic,KaiyuanWang,Albert
Zhan, Kevin Black, Cheng Chi, Kyle Beltran Hatch, Shan Lin, Jingpei Lu, Jean Mercat, Abdul Rehman, Pannag R
Sanketi,ArchitSharma,CodySimpson,QuanVuong,HomerRichWalke,BlakeWulfe,TedXiao,JonathanHeewon
Yang, Arefeh Yavary, Tony Z. Zhao, Christopher Agia, Rohan Baijal, Mateo Guaman Castro, Daphne Chen, Qiuyu
Chen, Trinity Chung, Jaimyn Drake, Ethan Paul Foster, Jensen Gao, Vitor Guizilini, David Antonio Herrera,
Minho Heo, Kyle Hsu, Jiaheng Hu, Muhammad Zubair Irshad, Donovon Jackson, Charlotte Le, Yunshuang Li,
Kevin Lin, Roy Lin, Zehan Ma, Abhiram Maddukuri, Suvir Mirchandani, Daniel Morton, Tony Nguyen, Abigail
O’Neill, Rosario Scalise, Derick Seale, Victor Son, Stephen Tian, Emi Tran, Andrew E. Wang, Yilin Wu, Annie Xie,
Jingyun Yang, Patrick Yin, Yunchu Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav
Gupta, Abhishek Gupta, Dinesh Jayaraman, Joseph J Lim, Jitendra Malik, Roberto Martín-Martín, Subramanian
Ramamoorthy, Dorsa Sadigh, Shuran Song, Jiajun Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine,
and Chelsea Finn. Droid: A large-scale in-the-wild robot manipulation dataset. arXiv preprint arXiv:2403.12945,
2024.
Benno Krojer, Mojtaba Komeili, Candace Ross, Quentin Garrido, Koustuv Sinha, Nicolas Ballas, and Mido Assran. A
shortcut-aware video-qa benchmark for physical understanding via minimal video pairs. preprint, 2024.
Hala Lamdouar, Charig Yang, Weidi Xie, and Andrew Zisserman. Betrayed by motion: Camouflaged object discovery
via motion segmentation. In Proceedings of the Asian conference on computer vision, 2020.
Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. Open Review, 62(1):1–62,
2022.
Kai Li, Yulin Liu, Lei Li, et al. Unmasked teacher: Towards training-efficient video foundation models. arXiv preprint
arXiv:2303.16035, 2023.
Kunchang Li, Yali Wang, Yinan He, Yizhuo Li, Yi Wang, Yi Liu, Zun Wang, Jilan Xu, Guo Chen, Ping Luo, Limin
Wang, and Yu Qiao. Mvbench: A comprehensive multi-modal video understanding benchmark. In Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 22195–22206, 2024.
TianhongLiandKaimingHe.Backtobasics: Letdenoisinggenerativemodelsdenoise.arXivpreprintarXiv:2511.13720,
2025.
Yingwei Li, Yi Li, and Nuno Vasconcelos. Resound: Towards action recognition without representation bias. In
Proceedings of the European conference on computer vision (ECCV), pages 513–528, 2018.
28

GuoliangLin,AntonMilan,ChunhuaShen,andIanReid.Refinenet: Multi-pathrefinementnetworksforhigh-resolution
| semantic | segmentation. |     | In CVPR, 2017a. |     |     |     |     |
| -------- | ------------- | --- | --------------- | --- | --- | --- | --- |
Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollár. Focal loss for dense object detection. In
Proceedings of the IEEE international conference on computer vision, pages 2980–2988, 2017b.
Yuanxin Liu, Shicheng Li, Yi Liu, Yuxiang Wang, Shuhuai Ren, Lei Li, Sishuo Chen, Xu Sun, and Lu Hou.
TempCompass: Do video LLMs really understand videos? arXiv preprint arXiv:2403.00476, 2024.
Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, and Baining Guo. Swin transformer:
| Hierarchical | vision | transformer | using | shifted windows. | In  | ICCV, 2021. |     |
| ------------ | ------ | ----------- | ----- | ---------------- | --- | ----------- | --- |
Antoine Miech, Dimitri Zhukov, Jean-Baptiste Alayrac, Makarand Tapaswi, Ivan Laptev, and Josef Sivic. Howto100m:
Learningatext-videoembeddingbywatchinghundredmillionnarratedvideoclips. InProceedingsoftheIEEE/CVF
| international | conference |     | on computer | vision, pages | 2630–2640, | 2019. |     |
| ------------- | ---------- | --- | ----------- | ------------- | ---------- | ----- | --- |
Ishan Misra and Laurens van der Maaten. Self-supervised learning of pretext-invariant representations. In CVPR,
2020.
Ishan Misra, C. Lawrence Zitnick, and Martial Hebert. Shuffle and learn: Unsupervised learning using temporal order
| verification. | In  | ECCV, | 2016. |     |     |     |     |
| ------------- | --- | ----- | ----- | --- | --- | --- | --- |
Himangi Mittal, Nakul Agarwal, Shao-Yuan Lo, and Kwonjoon Lee. Can’t make an omelette without breaking some
eggs: Plausible action anticipation using large video-language models. In Proceedings of the IEEE/CVF Conference
| on Computer | Vision | and | Pattern Recognition, | pages | 18580–18590, |     | 2024. |
| ----------- | ------ | --- | -------------------- | ----- | ------------ | --- | ----- |
ShentongMoandShengbangTong. Connectingjoint-embeddingpredictivearchitecturewithcontrastiveself-supervised
| learning. | Advances | in neural | information | processing | systems, | 37:2348–2377, | 2024. |
| --------- | -------- | --------- | ----------- | ---------- | -------- | ------------- | ----- |
Lorenzo Mur-Labadia, Ruben Martinez-Cantin, Jose J Guerrero, Giovanni Maria Farinella, and Antonino Furnari.
Aff-ttention! affordancesandattentionmodelsforshort-termobjectinteractionanticipation. InEuropeanConference
| on Computer | Vision, | pages | 167–184. | Springer, 2024. |     |     |     |
| ----------- | ------- | ----- | -------- | --------------- | --- | --- | --- |
M. Noroozi and P. Favaro. Unsupervised learning of visual representations by solving jigsaw puzzles. In ECCV, 2016.
Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez,
Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without
| supervision. | arXiv | preprint | arXiv:2304.07193, | 2023. |     |     |     |
| ------------ | ----- | -------- | ----------------- | ----- | --- | --- | --- |
Valentinos Pariza, Mohammadreza Salehi, Gertjan J. Burghouts, Francesco Locatello, and Yuki M. Asano. Near, far:
Patch-ordering enhances vision foundation models’ scene understanding. In ICLR, 2025.
Deepak Pathak, Philipp Krahenbuhl, Jeff Donahue, Trevor Darrell, and Alexei A. Efros. Context encoders: Feature
| learning | by inpainting. |     | In CVPR, 2016. |     |     |     |     |
| -------- | -------------- | --- | -------------- | --- | --- | --- | --- |
Deepak Pathak, Ross Girshick, Piotr Dollár, Trevor Darrell, and Bharath Hariharan. Learning features by watching
| objects | move. In | CVPR, | 2017. |     |     |     |     |
| ------- | -------- | ----- | ----- | --- | --- | --- | --- |
Federico Perazzi, Jordi Pont-Tuset, Brian McWilliams, Luc Van Gool, Markus Gross, and Alexander Sorkine-Hornung.
A benchmark dataset and evaluation methodology for video object segmentation. In Proceedings of the IEEE
| conference | on computer |     | vision and pattern | recognition, | pages | 724–732, | 2016. |
| ---------- | ----------- | --- | ------------------ | ------------ | ----- | -------- | ----- |
Pedro O. Pinheiro, Amjad Almahairi, Ryan Y. Benmaleck, Florian Golemo, and Aaron Courville. Unsupervised
| learning | of dense | visual | representations. | In NeurIPS, | 2020. |     |     |
| -------- | -------- | ------ | ---------------- | ----------- | ----- | --- | --- |
JordiPont-Tuset,FedericoPerazzi,SergiCaelles,PabloArbeláez,AlexSorkine-Hornung,andLucVanGool. The2017
davis challenge on video object segmentation. arXiv preprint arXiv:1704.00675, 2017.
Viorica Pătrăucean, Lucas Smaira, Ankush Gupta, Adrià Recasens Continente, Larisa Markeeva, Dylan Banarse,
Skanda Koppula, Joseph Heyward, Mateusz Malinowski, Yi Yang, Carl Doersch, Tatiana Matejovicova, Yury Sulsky,
Antoine Miech, Alex Frechette, Hanna Klimczak, Raphael Koster, Junlin Zhang, Stephanie Winkler, Yusuf Aytar,
Simon Osindero, Dima Damen, Andrew Zisserman, and João Carreira. Perception test: A diagnostic benchmark for
multimodal video models. Advances in Neural Information Processing Systems, 36:42748–42761, 2023.
Qwen Team, Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie
Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei
Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang
Xu, Junyang Lin, An Yang, Binyuan Hui, Bowen Yu, Chen Cheng, Dayiheng Liu, Fan Hong, Fei Huang, Jiawei
29

Liu, Jin Xu, Jianhong Tu, Jianyuan Zeng, Jie Zhang, Jinkai Wang, Jianwei Zhang, Jingren Zhou, Kexin Yang, Mei
Li, Ming Yan, Na Ni, Rui Men, Songtao Jiang, Xiaodong Deng, Xiaoming Huang, Ximing Zhou, Xingzhang Ren,
Yang Fan, Yichang Zhang, Yikai Zhu, Yuqiong Liu, and Zhifang Guo. Qwen2.5-vl technical report. arXiv preprint
| arXiv:2502.13923, |     | 2025. |     |     |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
Francesco Ragusa, Giovanni Maria Farinella, and Antonino Furnari. Stillfast: An end-to-end approach for short-term
object interaction anticipation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
| Recognition | (CVPR) | Workshops, |     | 2023. |     |     |     |     |
| ----------- | ------ | ---------- | --- | ----- | --- | --- | --- | --- |
Jathushan Rajasegaran, Ilija Radosavovic, Rahul Ravishankar, Yossi Gandelsman, Christoph Feichtenhofer, and
Jitendra Malik. An empirical study of autoregressive pre-training from videos. arXiv preprint arXiv:2501.05453,
2025.
René Ranftl, Katrin Lasinger, and Vladlen Koltun. Toward robust monocular depth estimation: Mixing datasets for
| zero-shot | cross-dataset |     | transfer. | In ECCV, | 2020. | Published | in TPAMI | in 2022. |
| --------- | ------------- | --- | --------- | -------- | ----- | --------- | -------- | -------- |
René Ranftl, Alexey Bochkovskiy, and Vladlen Koltun. Vision transformers for dense prediction. In ICCV, 2021.
Mike Ranzinger, Greg Heinrich, Jan Kautz, and Pavlo Molchanov. Am-radio: Agglomerative vision foundation model
| reduce all | domains | into | one. In | CVPR, | 2024. |     |     |     |
| ---------- | ------- | ---- | ------- | ----- | ----- | --- | --- | --- |
Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-resolution image
synthesis with latent diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern
| recognition, | pages | 10684–10695, |     | 2022. |     |     |     |     |
| ------------ | ----- | ------------ | --- | ----- | --- | --- | --- | --- |
Debaditya Roy, Ramanathan Rajendiran, and Basura Fernando. Interaction region visual transformer for egocentric
actionanticipation. InProceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision,pages
| 6740–6750, | 2024. |     |     |     |     |     |     |     |
| ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
Reuven Y. Rubinstein. Optimization of computer simulation models with rare events. European Journal of Operations
| Research, | 99:89–112, | 1997. |     |     |     |     |     |     |
| --------- | ---------- | ----- | --- | --- | --- | --- | --- | --- |
Chaitanya Ryali, Yuan-Ting Hu, Daniel Bolya, Chen Wei, Haoqi Fan, Po-Yao Huang, Vaibhav Aggarwal, Arkabandhu
Chowdhury, Omid Poursaeed, Judy Hoffman, et al. Hiera: A hierarchical vision transformer without the bells-and-
| whistles. | arXiv | preprint | arXiv:2306.00989, |     | 2023. |     |     |     |
| --------- | ----- | -------- | ----------------- | --- | ----- | --- | --- | --- |
Mohammadreza Salehi, Efstratios Gavves, Cees G. M. Snoek, and Yuki M. Asano. Time does tell: Self-supervised
| time-tuning | of  | dense image | representations. |     | In  | ICCV, 2023. |     |     |
| ----------- | --- | ----------- | ---------------- | --- | --- | ----------- | --- | --- |
Ziyao Shangguan, Chuhan Li, Yuxuan Ding, Yanan Zheng, Yilun Zhao, Tesca Fitzgerald, and Arman Cohan. Tomato:
Assessing visual temporal reasoning capabilities in multimodal foundation models. arXiv preprint arXiv:2410.23266,
2024.
Nathan Silberman, Derek Hoiem, Pushmeet Kohli, and Rob Fergus. Indoor segmentation and support inference from
rgbd images. In European conference on computer vision, pages 746–760. Springer, 2012a.
Nathan Silberman, Derek Hoiem, Pushmeet Kohli, and Rob Fergus. Indoor segmentation and support inference from
| rgbd images. | In  | ECCV, | 2012b. |     |     |     |     |     |
| ------------ | --- | ----- | ------ | --- | --- | --- | --- | --- |
Oriane Siméoni, Huy V Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc
Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, et al. Dinov3. arXiv preprint arXiv:2508.10104, 2025.
Walter Simoncini, Andrei Bursuc, Spyridon Gidaris, and Yuki Asano. No train, all gain: Self-supervised gradients
| improve | deep frozen | representations. |     | In  | NeurIPS, | 2024. |     |     |
| ------- | ----------- | ---------------- | --- | --- | -------- | ----- | --- | --- |
JiamingSong,ChenlinMeng,andStefanoErmon. Denoisingdiffusionimplicitmodels. arXivpreprintarXiv:2010.02502,
2020.
RobinStrudel,RicardoGarcia,IvanLaptev,andCordeliaSchmid. Segmenter: Transformerforsemanticsegmentation.
| In ICCV, | 2021. |     |     |     |     |     |     |     |
| -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
Richard S Sutton. An adaptive network that constructs and uses and internal model of its world. Cognition and Brain
| Theory, | 4(3):217–246, | 1981. |     |     |     |     |     |     |
| ------- | ------------- | ----- | --- | --- | --- | --- | --- | --- |
Sanket Thakur, Cigdem Beyan, Pietro Morerio, Vittorio Murino, and Alessio Del Bue. Guided attention for next
| active object@ |     | ego4d sta | challenge. | arXiv | preprint | arXiv:2305.16066, |     | 2023. |
| -------------- | --- | --------- | ---------- | ----- | -------- | ----------------- | --- | ----- |
Zhan Tong, Yibing Song, Jue Wang, and Limin Wang. Videomae: Masked autoencoders are data-efficient learners for
self-supervised video pre-training. Advances in neural information processing systems, 35:10078–10093, 2022.
30

Du Tran, Lubomir Bourdev, Rob Fergus, Lorenzo Torresani, and Manohar Paluri. Learning spatiotemporal features
| with 3d | convolutional | networks. |     | In ICCV, | 2015. |     |
| ------- | ------------- | --------- | --- | -------- | ----- | --- |
Du Tran, Heng Wang, Lorenzo Torresani, Jamie Ray, Yann LeCun, and Manohar Paluri. Look at spatiotemporal
| convolutions | for action | recognition. |     | In CVPR, | 2018. |     |
| ------------ | ---------- | ------------ | --- | -------- | ----- | --- |
Michael Tschannen, Alexey Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil
Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, et al. Siglip 2: Multilingual vision-language
encoders with improved semantic understanding, localization, and dense features. arXiv preprint arXiv:2502.14786,
2025.
Limin Wang, Bingkun Huang, Zhiyu Zhao, Zhan Tong, Yinan He, Yi Wang, Yali Wang, and Yu Qiao. Videomae v2:
Scaling video masked autoencoders with dual masking. In Proceedings of the IEEE/CVF conference on computer
| vision and | pattern | recognition, |     | pages 14549–14560, | 2023. |     |
| ---------- | ------- | ------------ | --- | ------------------ | ----- | --- |
PengWang,ShuaiBai,SinanTan,ShijieWang,ZhihaoFan,JinzeBai,KeqinChen,XuejingLiu,JialinWang,Wenbin
Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, and
JunyangLin. Qwen2-vl: Enhancingvision-languagemodel’sperceptionoftheworldatanyresolution. arXivpreprint
| arXiv:2409.12191, |     | 2024a. |     |     |     |     |
| ----------------- | --- | ------ | --- | --- | --- | --- |
Xiaolong Wang and Abhinav Gupta. Unsupervised learning of visual representations using videos. In ICCV, 2015.
YiWang,KunchangLi,XinhaoLi,JiashuoYu,YinanHe,GuoChen,BaoqiPei,RongkunZheng,ZunWang,Yansong
Shi, etal. Internvideo2: Scalingfoundationmodelsformultimodalvideounderstanding. InEuropean Conference on
| Computer | Vision, | pages | 396–416. | Springer, | 2024b. |     |
| -------- | ------- | ----- | -------- | --------- | ------ | --- |
Chen Wei, Haoqi Fan, Saining Xie, Chao-Yuan Wu, Alan Yuille, and Christoph Feichtenhofer. Masked feature
prediction for self-supervised visual pre-training. arXiv preprint arXiv:2112.09133, 2021.
Xin Wen, Bingchen Zhao, Anlin Zheng, Xiangyu Zhang, and Xiaojuan Qi. Self-supervised visual representation
| learning | with semantic | grouping. |     | In NeurIPS, | 2022. |     |
| -------- | ------------- | --------- | --- | ----------- | ----- | --- |
JiahaoXie,XiaohangZhan,ZiweiLiu,YewSoonOng,andChenChangeLoy. Unsupervisedobject-levelrepresentation
| learning | from scene | images. | In  | NeurIPS, 2021a. |     |     |
| -------- | ---------- | ------- | --- | --------------- | --- | --- |
SainingXie,ChenSun,JonathanHuang,ZhuowenTu,andKevinMurphy. Rethinkingspatiotemporalfeaturelearning:
| Speed-accuracy | trade-offs |     | in video | classification. | In ECCV, 2018. |     |
| -------------- | ---------- | --- | -------- | --------------- | -------------- | --- |
ZhendaXie,ZhengZhang,YueCao,YutongLin,JianminBao,ZhuliangYao,QiDai,andHanHu. Simmim: Asimple
| framework | for masked | image | modeling. | arXiv | preprint arXiv:2111.09886, | 2021b. |
| --------- | ---------- | ----- | --------- | ----- | -------------------------- | ------ |
Dejing Xu, Jun Xiao, Zhou Zhao, Jian Shao, Di Xie, and Yueting Zhuang. Self-supervised spatiotemporal learning via
| video clip | order prediction. |     | In  | CVPR, 2019. |     |     |
| ---------- | ----------------- | --- | --- | ----------- | --- | --- |
Ning Xu, Linjie Yang, Yuchen Fan, Jianchao Yang, Dingcheng Yue, Yuchen Liang, Brian Price, Scott Cohen, and
Thomas Huang. Youtube-vos: Sequence-to-sequence video object segmentation. In Proceedings of the European
| conference | on computer |     | vision | (ECCV), pages | 585–601, 2018. |     |
| ---------- | ----------- | --- | ------ | ------------- | -------------- | --- |
Lihe Yang, Binghui Kang, Zhiwen Huang, Xiaoxiao Xu, Jonathan Feng, and Hengshuang Zhao. Depth anything:
| Unleashing | the power | of  | large-scale | unlabeled | data. In CVPR, 2024. |     |
| ---------- | --------- | --- | ----------- | --------- | -------------------- | --- |
Sukmin Yun, Hankook Lee, Jaehyung Kim, and Jinwoo Shin. Patch-level representation learning for self-supervised
| vision transformers. |     | In CVPR, |     | 2022. |     |     |
| -------------------- | --- | -------- | --- | ----- | --- | --- |
Rowan Zellers, Jiasen Lu, Ximing Lu, Youngjae Yu, Yanpeng Zhao, Mohammadreza Salehi, Aditya Kusupati, Jack
Hessel,AliFarhadi,andYejinChoi. Merlotreserve: Neuralscriptknowledgethroughvisionandlanguageandsound.
In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 16375–16387, 2022.
Hang Zhang, Xin Li, and Lidong Bing. Video-llama: An instruction-tuned audio-visual language model for video
| understanding. | arXiv | preprint |     | arXiv:2306.02858, | 2023. |     |
| -------------- | ----- | -------- | --- | ----------------- | ----- | --- |
Richard Zhang, Phillip Isola, and Alexei A. Efros. Colorful image colorization. In ECCV, 2016.
Yuanhan Zhang, Jinming Wu, Wei Li, Bo Li, Zejun Ma, Ziwei Liu, and Chunyuan Li. Video instruction tuning with
| synthetic | data. arXiv | preprint |     | arXiv:2410.02713, | 2024. |     |
| --------- | ----------- | -------- | --- | ----------------- | ----- | --- |
Long Zhao, Nitesh B Gundavarapu, Liangzhe Yuan, Hao Zhou, Shen Yan, Jennifer J Sun, Luke Friedman, Rui Qian,
TobiasWeyand,YueZhao,etal. Videoprism: Afoundationalvisualencoderforvideounderstanding. arXiv preprint
| arXiv:2402.13217, |     | 2024. |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- |
31

Bolei Zhou, Hang Zhao andXavier Puig, Sanja Fidler, Adela Barriuso, and Antonio Torralba. Scene parsing through
| ade20k dataset. In | CVPR, 2017a. |     |     |
| ------------------ | ------------ | --- | --- |
Bolei Zhou, Hang Zhao, Xavier Puig, Sanja Fidler, Adela Barriuso, and Antonio Torralba. Scene parsing through
ade20k dataset. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 633–641,
2017b.
JinghaoZhou,ChenWei,HuiyuWang,WeiShen,CihangXie,AlanYuille,andTaoKong. ibot: Imagebertpre-training
| with online tokenizer. | arXiv preprint | arXiv:2111.07832, | 2021. |
| ---------------------- | -------------- | ----------------- | ----- |
AdrianZieglerandYukiM.Asano. Self-supervisedlearningofobjectpartsforsemanticsegmentation. InCVPR,2022.
32

Table11 PretraininghyperparametersforthePrimaryandCooldownphases. Hyperparameters are identical across all our
| ViT architectures | (ViT-L,             | -g and -G). |     |              |               |
| ----------------- | ------------------- | ----------- | --- | ------------ | ------------- |
| Parameter         |                     |             |     | PrimaryPhase | CooldownPhase |
| Number            | of frames           |             |     | 16           | 64            |
| Frames            | per Second          |             |     | 4.0          | 4.0           |
| Video             | Crop Size           |             |     | 256          | 384           |
| Image             | Crop Size           |             |     | 256          | 512           |
| Random            | Resize Aspect       | Ratio       |     | [0.75, 1.35] | [0.75, 1.35]  |
| Random            | Resize Scale        |             |     | [0.3, 1.0]   | [0.3, 1.0]    |
| Steps             |                     |             |     | 135,000      | 12000         |
| Warmup            | Steps               |             |     | 12,000       | N/A           |
| Image             | batch Size          | (global)    |     | 2,304        | 2,304         |
| Video             | batch Size (global) |             |     | 128          | 128           |
| Starting          | Learning            | Rate        |     | 1e-4         | 6e-4          |
| Final             | Learning Rate       |             |     | 5.25e-4      | 1e-6          |
| Weight            | Decay               |             |     | 0.04         | 0.04          |
| EMA               |                     |             |     | 0.99925      | 0.99925       |
| Spatial           | Mask Scale          |             |     | [0.15, 0.7]  | [0.15, 0.7]   |
| Temporal          | Mask Scale          |             |     | [1.0, 1.0]   | [1.0, 1.0]    |
| Mask              | Aspect Ratio        |             |     | [0.75, 1.5]  | [0.75, 1.5]   |
| Tubelet           | Size                |             |     | 2            | 2             |
| Patch             | Size                |             |     | 16           | 16            |
| Predictor         | Blocks              |             |     | 24           | 24            |
| Predictor         | Embedding           | Size        |     | 384          | 384           |
Encoder Intermediate Blocks (ViT-G) [12, 24, 36, 48] [12, 24, 36, 48]
Context Loss λ 0.5 for video, 0.7 for image 0.5 for videos, 0.7 for images
Appendix
A Pretrainingdetails
In this section, we detail our pretraining protocol and provide hyper-parameters. We use identical hyper-
parameters for all our ViT architectures (ViT-L, -g and -G). Following Assran et al. (2025), pretraining
consists of two phases: 1) the primary phase, lasting for 135k iterations, where the learning rate follows a
warmup (from 1e-4 to 5.25e-4) for 12k iterations, then a constant schedule (5.25e-4); and 2) a cooldown phase,
lasting for 12k iterations, where the learning rate is decayed to a small value (from 6e-4 to 1e-6).
During the primary phase, video samples consist of 16-frames clips sampled at 4 frames per second, both
video and images have a resolution of 256×256. The cooldown phase is shorter, allowing for higher input
resolutionwithmanageable computeresources, videosamplesconsist of 64-framesclipsatresolution384×384
and images are sampled at resolution 512×512. During both phases, the masking strategy follows the one
introduced in Bardes et al. (2024), the image and video batch sizes are set to, respectively, 2304 and 128, the
| weight-decay | is set to | 0.04 and the EMA | coefficient | is set to 0.99925. |     |
| ------------ | --------- | ---------------- | ----------- | ------------------ | --- |
We use the standard ViT architecture with a patch size of 16 for both images and videos, and a tubelet size of
2 for videos. Our predictor has 24 blocks (versus 12 in V-JEPA 2) and an embedding size of 384. For our deep
self-supervision loss, we use 4 intermediate blocks of the encoder, at equally spaced indices. The parameter λ
we use for Eq. 3 is different for video and images, with a value of 0.5 for video and 0.7 for images.
33

B Distillationdetails
Our distillation protocol is adapted from the pretraining recipe, maintaining the same JEPA loss, masking,
architecture,andhyperparameters,exceptforafewkeymodifications: theExponentialMovingAverage(EMA)
encoderisreplacedbyafrozenTeachernetwork. Thepredictor’sfinallayerembeddingdimensionisadaptedto
match the Teacher’s dimension to enable the computation of the loss. We do not use deep-self-supervision for
distillation: the predictor operates only on the last layer of the encoder, and the loss is only calculated on this
last layer. We do not initialize the predictor with the pretraining weights and instead retrain a new predictor,
which has 12 blocks (instead of 24 for pretraining), greatly improving distillation stability. Throughout
training, a separate EMA of the context encoder is maintained, corresponding to Polyak averaging, which is
never used in the loss calculation but serves as the final, high-performing model released for downstream tasks.
Distillation follows a multi-stage training approach similar to pretraining. Stage 1 (Primary Phase) with a
warmup-then-constant schedule and low-resolution data (16 frames, 256×256 pixels) using a pre-cooldown
low-resolution V-JEPA 2.1 ViT-G as the teacher, and Stage 2 (Cooldown Phase) with a short annealing
scheduleandhigh-resolutiondata(64frames,384×384)usingthecorrespondingpost-cooldownhigh-resolution
V-JEPA 2.1 ViT-G as the teacher. The Stage 2 student network is initialized with the EMA student network
from Stage 1, a two-stage strategy found to produce the best-performing models compared to alternatives
such as single-stage approaches or always distilling from the final high-resolution V-JEPA 2.1 teacher.
C Evaluationprotocols
C.1 DepthEstimation
Datasets and Metrics. We evaluated the geometric quality of the dense features of V-JEPA 2.1 in depth
estimation on NYUv2 (Silberman et al., 2012b) and KITTI (Geiger et al., 2013a), reporting the root mean
square error (RMSE).
Evaluation Protocol. Forfaircomparisonwiththestate-of-the-art,weadoptedthesameprotocolreported
by Siméoni et al. (2025), training a corresponding linear classifier on the training set of each data set. The
linear layer is applied only on top of the V-JEPA 2.1 visual encoder frozen patch features, and it is further
normalized using a learned BatchNorm layer. Note that we both train and evaluate single-image classifiers, as
we process individual images using the 2D Convolution image tokenizer described in Sec.2.3.4. We sweep
learningrates{1.5×10 3,1×10 3,8×10 4,3×10 4,1×10 4,8×10 5,3×10 5}andweightdecay{10 3,10 4}.
− − − − − − − − −
C.2 SemanticSegmentation
Datasets and Metrics. We evaluate semantic segmentation with linear probing on the image seman-
tic segmentation datasets ADE20K (Zhou et al., 2017a), Pascal VOC12 (Everingham et al., 2015), and
Cityscapes (Cordts et al., 2016), reporting mean intersection-over-union (mIoU).
Evaluation Protocol. Similarly,wealsofollowthesameprotocolreportedinDINOv3Siméonietal.(2025).
We train a linear classifier on top of last-block patch features from the frozen encoder (already normalized via
LayerNorm). Similar to the depth estimation evaluation protocol, we both train and evaluate single-image
classifiers. LinearprobesareoptimizedwithAdamWusinglearningrates{1.5×10 3,8×10 4,5×10 4,8×10 5}
− − − −
and weight decay {0.1,0.01,10 4}. We use a 512px resolution for ADE20K and VOC12, and 1024px height
−
for Cityscapes.
C.3 VideoObjectSegmentationTracking
Dataset and Metrics. We evaluate on DAVIS 2017 (Pont-Tuset et al., 2017) and YouTube-VOS (Xu et al.,
2018). DAVIS provides dense annotations for train/val (60/30 videos). In YouTube-VOS, as only the training
set is publicly available, we divided this set both training (80%) and validation (20%) videos.
34

Evaluation Protocol. Following (Rajasegaran et al., 2025) and Siméoni et al. (2025), we implement a
non-parametric label-propagation approach based on cosine similarity between patch features from a frozen
backbone. Segmentation labels from the first frame are encoded as one-hot patch assignments. For each
subsequent frame, we compute similarities with patches from the first frame and a small set of past frames,
and propagate labels via a weighted k-NN scheme within a spatial neighborhood.
We sweep over several hyperparameters, including context length {4,7,10,15}, neighborhood size {12,24,36},
neighborhood shape {square,circle}, top-k neighbors {3,5,10}, and similarity temperature {0.01,0.1,0.2,0.7}.
Hyperparameters are selected on the DAVIS training set and applied to all test splits. We use an input
resolution of 480px.
C.4 ShortTermObjectInteractionAnticipation
Dataset and Metrics. We evaluate V-JEPA 2.1 on the STA v2 split of Ego4D (Grauman et al., 2022),
which comprises 243 hours of annotated video clips spanning 128 noun and 81 verb categories, with a total of
98,276 training and 47,395 validation samples. Following the established evaluation protocol (Grauman et al.,
2022), we report Top-5 Average Precision (AP) and Top-5 mean Average Precision (mAP) metrics. As in
standard mAP, predictions are matched to ground-truth boxes using IoU > 0.5 and additional class-specific
criteria. For instance, the Top-5 mAP All variant requires a correct noun, correct verb, IoU above 0.5, and a
time-to-contact δ prediction within a 0.25-second tolerance. To address the inherently multi-modal nature
of future anticipation—where multiple plausible next-active objects may exist—the metric discounts up to
four highest-scoring false positives per example, thereby avoiding penalties for plausible but unannotated
predictions. Additionally, we report individual metrics to evaluate the temporal (δ), spatial (bounding boxes),
and semantic (noun and verb) dimensions of the task.
Evaluation Protocol. For a fair comparison with the previous state-of-the-art, we follow the official
StillFast baseline implementation (Ragusa et al., 2023), which extends Faster R-CNN (Girshick, 2015). Our
attentive probe consists of four attention blocks followed by the frame-guided temporal pooling mechanism
of (Mur-Labadia et al., 2024), since STA predictions must remain spatially aligned with the last video frame.
This pooling mechanism adopts a residual cross-attention module between the 3D tokens of the full video clip
and the 2D tokens of the last frame. Queries are computed from the last-frame tokens via a linear projection,
while keys and values are obtained from the video tokens using corresponding projections. Once the video
tokens are pooled in 2D, we apply a bilinear interpolation to match the resolution of the high-resolution image
tokens. Both representations are summed and fused through a 2D convolution layer. Finally, we upsample
this representation to produce a multi-scale pyramid at 1/4, 1/8, 1/16, 1/32, and 1/64 of the image input
resolution. This pyramid forms the input to the prediction head, which follows the design used in prior
work (Ragusa et al., 2023; Mur-Labadia et al., 2024; Thakur et al., 2023).
Probe Architecture. In this prediction head, first a Region Proposal Network (RPN) generates proposals
from a feature pyramid, and RoIAlign extracts corresponding local features. To enrich these features with
scene-level context, we concatenate to each local RoI feature the resulting pooled token from the 4-layers
attentive probe. The fused representation is processed by two fully connected layers and added back to the
local features through a residual connection, enabling global cues to modulate––rather than replace––local
information. Noun, verb and time to contact δ are predicted using respective linear layers from the fused
RoI features. A Softplus activation layers is applied to the δ output in order to obtain positive predictions.
Training is end-to-end, combining standard Faster R-CNN losses with an additional verb loss L and a
v
Smooth-L TTC loss L , weighted by 0.1 and 0.5 respectively.
1 ttc
Optimization. Models are optimized with Adam using learning rates in {1×10 5, 8×10 5, 1.2×10 4, 2×
− − −
10 4, 5×10 4}. Weadditionallyexploredifferentinputconfigurations,includingsamplingrates{16,8,4,2}fps,
− −
cliplengths{32,16,8,4}frames,andspatialresolutions{256px, 384px},coveringvideoswithvaryingtemporal
spans. We follow the multi-scale training strategy of Faster R-CNN, sampling image short sides uniformly
from {640,672,704,736,768,800} with a maximum long side of 1333 px. Our final best configuration consist
of 16 frames videos at 384px with a sampling rate of 2 fps, and using a learning rate of 1.2×10 4. We apply
−
35

the same protocol to DINOv2 Oquab et al. (2023), DINOv3 Siméoni et al. (2025) and V-JEPA 2 Assran et al.
(2025) models, reporting the best respective performance.
C.5 VideoandImageClassification
Dataset and Metrics. We use the evaluation benchmarks of V-JEPA 2 and evaluate our models on image
classification on ImageNet Deng et al. (2009), and video classification on Kinetics-400 Kay et al. (2017),
Something-Something-v2 Goyal et al. (2017) and Diving-48 Li et al. (2018).
Probe Architecture. We train an attentive probe on top of the frozen encoder output using the training
data from each downstream task. Our attentive probe is composed of four transformer blocks, each using
16 heads in the attention layer. The first three blocks use standard self-attention; the final block uses a
cross-attention layer with a learnable query token. The output of the cross-attention layer in the final block is
added back to the query token as a residual connection before applying the rest of the block (LayerNorm,
followed by MLP with a single GeLU activation). The transformer blocks are followed by a final linear
classifier layer.
Evaluation Protocol. We follow the evaluation protocol of V-JEPA 2. For video evaluations, we sampled
multiple clip segments from each input video. During validation, we also extracted three spatial views from
each segment (instead of one view during training). The number of clip segments, frame step parameter, and
global batch size vary for each evaluation. We use 64×2×3 input for SSv2 (16 frames clip, 2 temporal crops,
3 spatial crops), 16×8×3 for K400, and 32×4×3 for Diving-48. For all benchmarks, we use a spatial
resolution of 384×384. We use the 2D or 3D tokenizer, respectively, for image and video benchmarks. We
use a batch size of 256 except for ImageNet, we use 1024. For ImageNet, we do not use multiple clips or views
per sample. For Diving-48, we employ a multilayer strategy. Instead of attending to the tokens from only the
last layer of the encoder, we extract tokens from four encoder layers (the last layer and three intermediate
layers) and attend to all of them.
Optimization. For each evaluation, we simultaneously train multiple classifier heads with different hyper-
parameters (learning rate and weight decay), reporting the accuracy of the best-performing classifier. For
most of our evaluations (Kinetics, SSv2, and ImageNet), we train for 20 epochs and use 20 heads, each using
one of five learning rate values and four weight decay values, and the learning rate decays according to a
cosine schedule. For Diving-48, which benefit from longer training, we train for 50 epochs.
C.6 ActionAnticipation
Dataset and Metrics. We evaluated V-JEPA 2.1 on the Action Anticipation task of the Epic-Kitchen-100
benchmark Damen et al. (2022). The EK100 dataset is comprised of 100 hours of cooking activities recorded
from an egocentric perspective across 45 kitchen environments. Each video in EK100 is annotated with action
segments, which include a start timestamp, an end timestamp, and an action label. There are 3,568 unique
action labels, each consisting of a verb and a noun category, with a total of 97 verb categories and 300 noun
categories. The EK100 action anticipation task involves predicting noun, verb, and action (i.e., predicting
verb and noun jointly) from a video clip, referred to as context, that occurs before the start timestamp of an
action segment. The interval between the end of the context and the beginning of the action segment is the
anticipation time, which is set to 1 second by default. Given that different future actions may be possible
from a given context, mean-class recall-at-5 for noun, verb and action, is used as the metric to measure
performance (Damen et al., 2022).
Evaluation Protocol. We follow the same evaluation protocol introduced in V-JEPA 2 and use a focal
loss Lin et al. (2017b) with α = 0.25 and γ = 2.0 when training the probe. We used a context of 32 frames
with a frame-rate of 8 frames per second at resolution 384×384. During probe training, we randomly sample
an anticipation time between 0.25 and 1.75 seconds and an anticipation point between 0.0 and 0.25. Our
probe architecture for action anticipation follows the architecture introduced in V-JEPA 2 and described
in Appendix C.5, consisting of four transformer blocks, including a last cross-attention layer with a set of
learnable query tokens, followed by a final linear classifier layer for each query token.
36

Table12 Impactofdeepself-supervisionontheneedformulti-scaleevaluation. We conduct experiments with our V-JEPA
2.1 ViT-L trained from scratch. Last-Layer indicates that evaluation is conducted with only the last layer of the
encoder as input to the probe. 4-Layers indicates that evaluation is conducted by concatenating 4 intermediate layers
of the encoder and feeding it to the probe.
DeepSelf-Supervision ADE20k NYU Diving-48
Last-Layer 4-Layers Last-Layer 4-Layers Last-Layer 4-Layers
(cid:37) 34.9 39.1 0.513 0.463 85.8 86.9
(cid:34) 42 43.9 0.381 0.370 87.2 88.1
Table13 Impactofpretrainingspatialresolution. We compare models trained during the cooldown phase at 256×256
spatial resolution against 384×384.
Model Res SSv2 D-48 K400 IN1K EK100 ADE20k Citys. VOC NYU KITTI DAVIS YT-VOS
ViT-g 256 76.7 88.6 86.2 84.1 35.7 47.8 71.7 84.6 0.359 2.611 68.0 72.0
ViT-g 384 76.9 89 87 84.8 38.4 47.8 71.8 84.7 0.350 2.601 67.4 71.3
ViT-G 256 77.1 89.5 87.3 84.8 38.8 47.8 73.2 84.7 0.313 2.472 68.6 72.7
ViT-G 384 77.7 89.2 87.7 85.5 40.8 47.9 73.5 85.0 0.307 2.461 69.0 72.6
D AdditionalAblations
D.1 Multi-scaleevaluation
We evaluate the impact of Deep Self-Supervision on the need for multi-scale evaluation, i.e. using multiple
layers of the encoder as input to the evaluation probe. Table 12 compares a model trained with Deep
Self-Supervision with a model trained without, and we measure performance on image segmentation on
ADE20k, depth estimation on NYU, and action recognition on Diving-48, using either; a) only the last layer
of the encoder as input to the probe (Last-Layer) or b) 4 equally spaced intermediate layers (4-Layers). We
observe that the model trained without Deep Self-Supervision has a wide gap in performance between using
Last-Layer and 4-Layers, and benefits a lot from multi-scale evaluation. On the other hand, the model trained
with Deep Self-Supervision is already stronger using Last-Layer, and only benefits a little from using 4-Layers.
D.2 PretrainingSpatialResolution
Table 13 presents the impact of the resolution used during the cooldown phase of pretraining on performance
on most of our downstream tasks. We compare models trained with a video spatial resolution of 256×256
to the models we present in the main paper that are trained with a video spatial resolution of 384×384.
V-JEPA 2.1 benefits from higher resolution pretraining across all of our downstream tasks.
37