| Tuna-2:    |     | Pixel |               | Embeddings |     | Beat |     | Vision     | Encoders | for |
| ---------- | --- | ----- | ------------- | ---------- | --- | ---- | --- | ---------- | -------- | --- |
| Multimodal |     |       | Understanding |            |     |      | and | Generation |          |     |
ZhihengLiu1,2,∗, WeimingRen1,3,∗, XiaokeHuang1, ShoufaChen1, TianhongLi1, MengzhaoChen2, YataiJi2, Sen
He1, JonasSchult1, BelindaZeng1, TaoXiang1, WenhuChen3, PingLuo2, LukeZettlemoyer1, YurenCong1
| 1Meta  | AI, 2The       | University |                | of Hong | Kong, 3University |      | of Waterloo |     |     |     |
| ------ | -------------- | ---------- | -------------- | ------- | ----------------- | ---- | ----------- | --- | --- | --- |
| ∗Joint | first authors, | listed     | alphabetically |         | by last           | name |             |     |     |     |
Unified multimodal models typically rely on pretrained vision encoders and use separate visual
representations for understanding and generation, creating misalignment between the two tasks
and preventing fully end-to-end optimization from raw pixels. We introduce Tuna-2, a native
6202 yaM 81  ]VC.sc[  2v36742.4062:viXra
unified multimodal model that performs visual understanding and generation directly based on
pixel embeddings. Tuna-2 drastically simplifies the model architecture by employing simple patch
embeddinglayerstoencodevisualinput,completelydiscardingthemodularvisionencoderdesignssuch
Tuna-2
as the VAE or the representation encoder. Experiments show that achieves state-of-the-art
performance in multimodal benchmarks, demonstrating that unified pixel-space modelling can fully
compete with latent-space approaches for high-quality image generation. Moreover, while the encoder-
based variant converges faster in early pretraining, Tuna-2’s encoder-free design achieves stronger
multimodal understanding at scale, particularly on tasks requiring fine-grained visual perception.
These results show that pretrained vision encoders are not necessary for multimodal modelling, and
end-to-end pixel-space learning offers a scalable path toward stronger visual representations for both
| generation | and       | perception. |     |     |     |     |     |     |     |     |
| ---------- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Date:      | April 28, | 2026        |     |     |     |     |     |     |     |     |
https://tuna-ai.org/tuna-2
Projectpage:
|     | TUNA |     |     | TUNA-R |     |     | TUNA-2 |     |     |     |
| --- | ---- | --- | --- | ------ | --- | --- | ------ | --- | --- | --- |
Image
VAE Decoder
| Response       |                        |     | Response       |             | Image                  | Response       |             | Image            |     |     |
| -------------- | ---------------------- | --- | -------------- | ----------- | ---------------------- | -------------- | ----------- | ---------------- | --- | --- |
| Language Head  | Unpatchify Layer       |     | Language Head  |             | Unpatchify Layer       | Language Head  |             | Unpatchify Layer |     |     |
|                | Transformer            |     |                | Transformer |                        |                | Transformer |                  |     |     |
| Text Tokenizer | Representation Encoder |     | Text Tokenizer |             | Representation Encoder | Text Tokenizer |             | Patchify Layer   |     |     |
| Prompt         |                        |     |                | Prompt      |                        | Prompt         |             | Image            |     |     |
|                | Patchify Layer         |     |                |             | Patchify Layer         |                |             |                  |     |     |
Image
VAE Encoder
Image
|     |     | Tuna-2 |     |     |     |     |     |     | Tuna |     |
| --- | --- | ------ | --- | --- | --- | --- | --- | --- | ---- | --- |
Figure1 Evolution of architecture and multimodal performance comparison. We simplify (Liu et al.,
Tuna-R,
2025) by progressively stripping away its visual encoding components. By removing the VAE, we first derive
a pixel-space UMM that relies solely on a representation encoder. Tuna-2 further streamlines the design by bypassing
the representation encoder entirely, utilizing direct patch embedding layers for raw image inputs. Tuna-2 using pixel
embeddings outperforms both Tuna-R and Tuna across a diverse suite of multimodal benchmarks.
1 Introduction
Visual understanding and generation are two core capabilities in multimodal AI. Recent work has increasingly
focused on native unified multimodal models (UMMs) (Zhou et al., 2024; Deng et al., 2025; Liu et al., 2025),
which aim to integrate both capabilities within a single framework. A central challenge in building such
models is encoding input images into visual representations that effectively support both understanding and
1

generation. Early approaches (Deng et al., 2025; Chen et al., 2025c) adopted decoupled representations, using
representation encoders such as CLIP (Radford et al., 2021) for understanding and reconstruction-oriented
encoders such as VQ-VAE (Esser et al., 2021) for generation. To address the representation mismatch
introducedbythisdesign,morerecentUMMs(Xieetal.,2025b;Liuetal.,2025)havemovedtowardmodelling
both tasks using unified visual representations through a shared vision encoder.
Despite the significant progress, both decoupled and unified visual representation designs still rely heavily on
pretrained vision encoders (Wan et al., 2025; Tschannen et al., 2025) for visual feature extraction. In parallel,
recent research on multimodal understanding and generation has begun to move away from encoder-based
modular designs toward simpler monolithic, encoder-free architectures. In multimodal understanding, newer
native vision-language models (Diao et al., 2025) remove the pretrained representation encoder and instead
align images and natural language within a unified, end-to-end architecture. In visual generation, pixel-space
diffusionmodels(Hoogeboometal.,2023;Chenetal.,2025b;LiandHe,2025)haveshownincreasingflexibility,
stronger scalability, and state-of-the-art performance on a wide range of tasks, suggesting that pretrained
VAE encoders may no longer be essential even for high-fidelity image synthesis.
Motivated by these observations, we ask a natural but largely unexplored question: can we move beyond
pretrained vision encoders altogether, and build unified multimodal models through end-to-end native
modelling directly from raw pixels?
WeanswerthisquestionaffirmativelybyintroducingTuna-2,anativeunifiedmultimodalmodelthatattempts
to progressively simplify the encoder modules, and ultimately remove vision encoders completely. We first
introduce Tuna-R, which eliminates the VAE model while keeping a representation encoder in the model
architecture. Tuna-R performs multimodal understanding similar to standard encoder-based LMMs, and
supports visual generation through pixel-space flow matching with an x-prediction objective. We then propose
Tuna-2, which further simplifies the architecture by removing the encoder entirely and using only a single
transformer decoder to process image and video tokens. As a result, Tuna-2 enables end-to-endnative unified
modelling directly from raw pixels, without relying on any pretrained encoder modules.
Sincelearningunifiedrepresentationsdirectlyinhigh-dimensionalpixelspaceissubstantiallymorechallenging
than learning them in a compact latent space, we further introduce a masking-based visual feature learning
scheme to stabilize training and encourage the learning of more robust pixel-space representations. Together,
these designs enable Tuna-2 to achieve state-of-the-art performance across a diverse set of multimodal
understanding and generation benchmarks. More importantly, our controlled comparison reveals a clear
design insight: after sufficient visual pretraining, the encoder-free Tuna-2 becomes competitive with the
encoder-basedTuna-Ronvisualgeneration,whileconsistentlyoutperformingitonmultimodalunderstanding,
especially on benchmarks that require fine-grained visual perception. These findings suggest that removing
pretrained vision encoders can be advantageous for learning stronger fine-grained visual representations in
end-to-end pretraining. As shown in Figures 1 and 2, this leads to highly competitive performances in both
multimodal understanding and generation.
Our main contributions are summarized as follows:
1. We propose Tuna-2, a native unified multimodal model that supports multimodal understanding and
generation with encoder-free designs, achieving state-of-the-art performance across a wide range of
understanding and generation benchmarks.
2. We conduct controlled comparisons between Tuna-2 and an encoder-based pixel-space UMM variant
Tuna-R, and show that after sufficient multimodal pretraining, Tuna-2 and its encoder-free design are
competitive on generation and advantageous for understanding, especially on fine-grained, perception-
intensive tasks.
3. Weconductcomprehensiveablationsandanalysesonpixel-spaceUMMstostudytheirtrainingdynamics
and model behaviours, offering useful insights for the development of future native unified multimodal
models.
2

Figure2 While being completely encoder-free, Tuna-2 is capable of performing high-fidelity text-to-image generation
and image editing.
3

2 Method
In this section, we present Tuna-2, a native unified multimodal model that performs visual understanding
and generation both in pixel space. We start by detailing our approach to progressively remove vision encoder
components to derive Tuna-2 in Section 2.1. We then describe our masked feature learning scheme in
| Section | 2.2 and our model | training | pipeline in Section | 2.3. |     |     |     |
| ------- | ----------------- | -------- | ------------------- | ---- | --- | --- | --- |
2.1 TowardsEncoder-FreeUnifiedModels
Tuna
As shown in Figure 1, existing UMMs with unified visual representations, such as (Liu et al., 2025),
typically consist of a vision encoder and an LLM decoder for joint vision-language modeling, followed by
modality-specific heads, including a language modelling head for autoregressive text generation and a flow
Tuna-2
matching head for image generation. In this work, we propose as an encoder-free UMM formulation
by progressively simplifying the vision encoder components in existing architectures. Our design process for
| this architectural | simplification | is as | follows:  |                   |               |          |        |
| ------------------ | -------------- | ----- | --------- | ----------------- | ------------- | -------- | ------ |
|                    |                |       | First, we | attempt to remove | the VAE model | and only | employ |
Representationencoder-basedarchitecture.
a pretrained representation encoder in the vision encoder. As shown in Figure 1, this resonates a standard
paradigm for vision-language modelling: the representation encoder first encodes input images into visual
tokens, which are then combined with the text tokens in the LLM decoder for joint vision-language modelling.
Originally proposed in LLaVA (Liu et al., 2023), this paradigm has been verified and scaled up by later works
such as Qwen3-VL (Bai et al., 2025a) and InternVL3.5 (Wang et al., 2025d), and remains the most popular
framework for multimodal understanding. We refer to this intermediate design as Tuna-R. Although our
ultimate goal is to move beyond encoder-based architectures, we view Tuna-R as an important intermediate
| step that | enables a controlled | comparison | with Tuna-2. |     |     |     |     |
| --------- | -------------------- | ---------- | ------------ | --- | --- | --- | --- |
Encoder-free(non-encoder)architecture. Second, we consider a further simplified architecture that removes
the representation encoder entirely, which becomes our main design for Tuna-2. As shown in Figure 1, this
design replaces pretrained vision encoders with simple patch embedding layers that convert images into visual
tokens, which are then processed jointly with text tokens by the LLM decoder. Similar encoder-free designs
have recently been explored in models such as Mono-InternVL (Luo et al., 2025) and NEO (Diao et al., 2025).
By removing the pretrained representation encoder, this design avoids its built-in inductive biases, such as
fixed input resolutions and limited access to fine-grained low-level visual details. It also simplifies the model
architecture into a single unified transformer. In Section 3, we present a series of in-depth analyses comparing
Tuna-2 with Tuna-R, and demonstrate the effectiveness and scalability of Tuna-2.
Pixel-spaceimagegeneration. Our VAE-free design allows us to directly perform multimodal understanding
and text generation using the LLM decoder and the language modelling head. However, discarding the VAE
also means that we can no longer adopt the designs from existing UMMs and generation-only models that
follow the latent diffusion architecture. To effectively perform pixel-space image generation, we adopt the
x-prediction and v-loss paradigm from JiT (Li and He, 2025) for pixel-space flow matching. Specifically, given
the source image x 1 , the sampled noise x 0 ∼N(0,I) and the timestamp t, we employ rectified flow (Liu et al.,
2022; Lipman et al., 2022) and its linear schedule to construct a noisy sample in pixel space:
|     |     |     | x =tx +(1−t)x | ,t∈[0,1]. |     |     | (1) |
| --- | --- | --- | ------------- | --------- | --- | --- | --- |
|     |     |     | t 1           | 0         |     |     |     |
Tuna-2 is then formulated to directly predict the clean image from the noisy image in pixel space:
|     |     |     | x =π | (x ,c,t), |     |     | (2) |
| --- | --- | --- | ---- | --------- | --- | --- | --- |
|     |     |     | θ    | θ t       |     |     |     |
where π is our unified model (vision-language backbone and flow matching head) and c is the conditioning
θ
signals (text for text-to-image generation and text+image for image editing). As suggested in JiT, while
our model directly predicts x , we still transform it into the velocity term v and regress v as our learning
|     |     | θ   |     |     | θ   | θ   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
objective:
x θ −x t,
|     |     |     | v =            |            |     |     | (3) |
| --- | --- | --- | -------------- | ---------- | --- | --- | --- |
|     |     |     | θ 1−t          |            |     |     |     |
|     |     |     | L =E           | ||v −v||2, |     |     | (4) |
|     |     |     | flow t,c,x1,x0 | θ 2        |     |     |     |
4

Input Image
Generation: predict full clean images Understanding: predict new text tokens
Visual Token Noisy Visual Token Learnable Mask Token Text Token
Figure3 Illustration of our proposed masking-based feature learning scheme. During training, we use the learnable
mask token to regularize multimodal understanding and perform masked prediction for visual generation.
where v is the ground truth velocity defined by v =x −x . During inference, we employ the Euler solver
1 0
and predict the denoised image at t′ from the noisier image at t<t′ based on the velocity term v , such that
θ
x =x +(t′−t)v , where v is transformed from our model prediction x , based on Equation 3.
t′ t θ θ θ
2.2 LearningRobustVisualRepresentationsviaMasking
While removing the VAE simplifies our model architecture and enables fully end-to-end unified multimodal
training,italsoshiftsvisualmodellingfromacompactlatentspacetothemuchhigher-dimensionalpixelspace.
As a result, learning a unified visual representation becomes more challenging: the increased redundancy in
pixel-space inputs makes it easier for the model to rely on superficial shortcuts, rather than learning visual
cues that are genuinely informative for both understanding and generation. To learn more robust visual
representations in pixel space, we introduce a masking-based visual feature learning scheme. As shown in
Figure 3, during training, we (optionally) randomly select a subset of image patches according to a masking
ratio and replace the masked visual tokens with a learnable mask token before feeding them into the LLM
decoder. The same masking operation is applied to both generation and understanding examples, but plays
different roles in the two settings:
1. For generation examples, we let the model predict the clean image patches in both the masked and the
unmasked regions, such that (1) we create a harder denoising problem for the model to predict clean
images from partially observed noisy images; and (2) it encourages the learnable mask token to absorb
useful information for image reconstruction conditioned on the visible context.
2. For understanding examples, our model predicts the ground truth text response based on the masked
visual input. Inthiscase, maskingservesasaregularizationmechanismthatforcesthemodeltoperform
multimodal reasoning under partial visual observation, leading to more robust visual representations.
Our masking-based feature learning scheme resembles masked modelling methods in visual understanding and
generation, such as MAE (He et al., 2022) and SigLIP 2 (Tschannen et al., 2025) for semantic learning and
MaskGIT (Chang et al., 2022) and DeTok (Yang et al., 2025a) for visual generation. Empirically, we find that
applying masking leads to enhanced model performance during pretraining stages.
2.3 TrainingPipeline
Our encoder-free design enables fully end-to-end training of Tuna-2, without requiring separate stages to
train connector layers, which is a common design in encoder-based modular approaches. As described below,
our training pipeline consists of two stages, both of which are carried out in a fully end-to-end manner:
Stage1:fullmodelpretraining. Inthefirststage,weaimtoestablishastronginitializationfortheflowmatching
head, and adapt pixel-space visual inputs for unified multimodal understanding and generation. To achieve
this, we train the full model jointly on two tasks: image captioning and text-to-image generation.
Stage2:supervisedfinetuning(SFT). Next, we perform supervised fine-tuning (SFT) of the full model with a
lower learning rate. We use datasets for image editing, image instruction-following, and high-quality image
generation. This step refines Tuna-2’s abilities, boosting performance and generalization across various
multimodal tasks.
5

Table1 Comparisons between Tuna-2 and baseline models on multimodal understanding benchmarks. Results with
modelsizegreaterthan13Baregrayed. Bold: bestresultsamongallUMMs. Underline: second-bestamongallUMMs.
GeneralBenchmarks Pixel-centricBenchmarks
Models Size
GQA RealWorldQA MMVet MMMU MMVP SEED-Bench2+ AI2D ChartQA OCRBench V* CountBench VisuLogic
Understanding-onlyModels(LMMs)
LLaVA-1.5(Liuetal.,2023) 7B 62.0 54.8 32.9 35.7 - - 55.5 17.8 31.8 - - -
Qwen-VL-Chat(Baietal.,2023) 7B 57.5 49.3 47.3 37.0 - - 57.7 49.8 48.8 - - -
LLaVA-OV(Lietal.,2024a) 7B - 69.9 51.9 48.8 77.3 62.2 81.4 80.9 62.2 72.7 76.2 24.8
Qwen2.5-VL(Baietal.,2025b) 7B 60.7 69.9 61.7 58.6 78.0 70.5 82.7 83.0 83.7 71.2 74.1 20.0
CompositeUMMs
TokenFlow-XL(Quetal.,2025) 14B 62.5 56.6 - 43.2 - - - - - - - -
BLIP3-o(Chenetal.,2025a) 4B - 60.4 - 46.6 - - - - - - - -
Tar(Hanetal.,2025) 7B 61.3 - - 39.0 74.3 46.2 - - - 41.4 64.2 24.3
X-Omni(Gengetal.,2025) 7B 62.8 62.6 - 47.2 - - 76.8 81.5 70.4 - - -
NativeUMMs
BAGEL(Dengetal.,2025) 14B 66.4 72.8 67.2 55.3 85.0 71.9 89.2 78.5 73.3 70.2 82.5 41.7
Ming-UniVision(Huangetal.,2025a) 16B 59.4 59.1 64.2 40.3 71.0 56.8 82.8 76.7 72.4 48.2 76.8 26.7
Harmon(Wuetal.,2025d) 1.5B 58.9 49.8 - 38.9 61.7 41.6 57.0 29.8 11.2 41.9 67.0 25.1
JanusFlow(Maetal.,2025b) 1.3B 60.3 41.2 36.2 29.3 67.7 39.8 54.2 42.4 53.2 42.9 78.6 22.0
Emu3(Wangetal.,2024b) 8B 60.3 57.4 23.5 31.6 71.0 44.6 70.0 69.4 68.7 53.4 65.2 24.7
VILA-U(Wuetal.,2024) 7B 60.8 46.8 26.3 31.2 62.7 31.9 49.0 11.4 23.3 38.7 55.2 25.4
Janus-Pro(Chenetal.,2025c) 7B 62.0 58.0 41.1 41.0 73.3 56.3 71.3 25.8 59.0 47.6 53.2 23.8
Show-o2(Xieetal.,2025b) 7B 63.1 64.7 39.6 48.9 76.7 61.3 78.6 52.3 32.4 44.5 63.5 26.9
OneCat(Lietal.,2025) 9B 63.1 65.2 52.2 41.9 71.3 61.6 77.8 81.2 79.0 63.4 34.2 24.9
Tuna(Liuetal.,2025) 7B 63.9 66.1 42.9 49.8 70.7 52.7 79.3 85.8 74.3 52.4 73.5 22.4
Tuna-R 7B 63.5 67.9 46.7 51.1 74.7 58.4 79.4 85.6 78.3 57.6 77.8 26.2
Tuna-2 7B 65.0 67.7 51.7 50.7 77.3 61.1 79.6 85.6 79.7 59.2 81.7 28.8
For Tuna-R, which includes a connector layer between the representation encoder and the LLM decoder,
we add an extra alignment stage before Stage 1. In this stage, we train only the connector layer for a short
period using image captioning and text-to-image generation data. As noted above, Tuna-2 does not require
this additional stage because of its encoder-free design.
3 Experiments
3.1 ExperimentSetup
We employ Qwen2.5-7B-Instruct (Qwen et al., 2024) as the LLM decoder and use a patch embedding size of
16 for Tuna-2. For Stage 1 pretraining, we use 550M in-house image-text pairs, consisting of 30% image
captioningdataformultimodalunderstandingand70%text-to-imagegenerationdata. Inaddition, weinclude
text-only data from Nemotron (Bercovich et al., 2025), which accounts for 20% of the total pretraining data.
The full model is trained end-to-end for 300k steps on 64 nodes with the AdamW optimizer (Loshchilov
and Hutter, 2017) and a learning rate of 1×10−4. We employ the proposed masking-based feature learning
strategy during the final 40% of pretraining, applying masking in 50% of training examples and randomly
sampling the masking ratio from 0% to 50%. For Stage 2 supervised finetuning, we use a curated SFT corpus
covering image instruction-following, image editing, and high-quality image generation. Specifically, for image
instruction-following, we include 13M conversational examples from the open-source FineVision (Wiedmann
et al., 2025) dataset. For image editing, we use approximately 2M examples from OmniEdit (Wei et al., 2024).
This stage is trained for 50k steps with AdamW and a learning rate of 2×10−5. For all training stages, we
pad the input sequence length to 16k tokens per GPU.
For Tuna-R, we use the same Qwen2.5-7B-Instruct as the LLM decoder. We follow Tuna and adopt SigLIP
2 So400M (Tschannen et al., 2025) as the representation encoder. For the connector-alignment stage in
Tuna-R, we train the model for 3k steps with AdamW and a learning rate of 5×10−4.
3.2 MainResults
Imageunderstanding. We employ a comprehensive evaluation suite consisting of nine VQA benchmarks,
including GQA (Hudson and Manning, 2019), RealWorldQA (xAI), MMVet (Yu et al., 2023), MMMU
(Yue et al., 2024), MMVP (Tong et al., 2024), SEED-Bench2+ (Li et al., 2024b), AI2D (Kembhavi et al.,
2016), ChartQA (Masry et al., 2022) and OCRBench (Liu et al., 2024), to evaluate the image understanding
capabilities for Tuna-2. As shown in Table 1, after removing the VAE model, both Tuna-R and Tuna-2
outperform Tuna and achieve state-of-the-art results among all 7B-scale native UMMs, demonstrating the
effectiveness of our pixel-space unified representations. Notably, Tuna-2 outperforms Tuna-R even after
6

Table2 Image generation results on GenEval and DPG-Bench. “Col. Attr.” means “Color Attribute”. † refers to
methods using LLM rewriters in GenEval. Bold: best results among native UMMs. Underline: second-best.
|     |     |     |     |     |     | GenEval |     |     |     | DPG-Bench |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --------- | --- | --- | --- |
Models Size 1-Obj.2-Obj.CountColorsPositionCol. Attr.OverallGlobalEntityAttributeRelationOtherOverall
Generation-onlyModels
SD3-M(Esseretal.,2024) 2B 0.99 0.94 0.72 0.89 0.33 0.60 0.74 87.90 91.01 89.96 80.70 88.68 84.08
FLUX.1[dev]†(Batifoletal.,2025) 12B 0.98 0.93 0.75 0.93 0.68 0.65 0.82 82.10 89.50 88.70 91.10 89.40 84.00
LongCat-Image(Teametal.,2025) 6B 0.99 0.98 0.86 0.86 0.75 0.73 0.87 89.10 92.54 92.00 93.28 87.50 86.80
Qwen-Image(Wuetal.,2025a) 20B 0.99 0.92 0.89 0.88 0.76 0.77 0.87 91.32 91.56 92.02 94.31 92.73 88.32
Seedream3.0(Gaoetal.,2025) - 0.99 0.96 0.91 0.93 0.47 0.80 0.84 94.31 92.65 91.36 92.78 88.24 88.27
Z-Image-Turbo(Caietal.,2025) 6B 1.00 0.95 0.77 0.89 0.65 0.68 0.82 91.29 89.59 90.14 92.16 88.68 84.86
CompositeUMMs
Tar(Hanetal.,2025) 7B 0.99 0.92 0.83 0.85 0.80 0.65 0.84 83.98 88.62 88.05 93.98 84.86 84.19
| BLIP3-o(Chenetal.,2025a) |     |     |     | 8B - | - - | -   | - - | 0.84 | -   | - - | -   | -   | 81.60 |
| ------------------------ | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | ----- |
UniWorld-V1†(Linetal.,2025a) 12B 0.98 0.93 0.81 0.89 0.74 0.71 0.84 83.64 88.39 88.44 89.27 87.22 81.38
OmniGen2†(Wuetal.,2025b)
|     |     |     |     | 7B 0.99 0.96 | 0.74 | 0.98 | 0.71 0.75 | 0.86 | 88.81 | 88.83 90.18 | 89.37 | 90.27 | 83.57 |
| --- | --- | --- | --- | ------------ | ---- | ---- | --------- | ---- | ----- | ----------- | ----- | ----- | ----- |
NativeUMMs
| MUSE-VL(Xieetal.,2025c)     |     |     |     | 7B - | - - | -   | - - | 0.57 | -   | - - | -   | -   | -     |
| --------------------------- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | ----- |
| Transfusion(Zhouetal.,2024) |     |     |     | 7B - | - - | -   | - - | 0.63 | -   | - - | -   | -   | -     |
| Emu3(Wangetal.,2024b)       |     |     |     | 8B - | - - | -   | - - | 0.66 | -   | - - | -   | -   | 81.60 |
Show-o2(Xieetal.,2025b) 7B 1.00 0.87 0.58 0.92 0.52 0.62 0.76 89.00 91.78 89.96 91.81 91.64 86.14
Janus-Pro(Chenetal.,2025c) 7B 0.99 0.89 0.59 0.90 0.79 0.66 0.80 86.90 88.90 89.40 89.32 89.48 84.19
HBridge†(Wangetal.,2025e) 7B 0.96 0.80 0.94 0.77 0.78 0.87 90.23 90.06 88.42 85.23
|     |     |     |     | 1.00 |     |     |     |     | 91.78 | 91.82 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | ----- | ----- | --- | --- | --- |
Ming-UniVision(Huangetal.,2025a)16B 1.00 0.93 0.59 0.93 0.92 0.70 0.85 - - - - - 82.12
BAGEL†(Dengetal.,2025) 14B 0.98 0.95 0.84 0.95 0.78 0.77 0.88 88.94 90.37 91.29 90.82 88.67 85.07
Mogao(Liaoetal.,2025) 7B 0.83 0.93 0.84 0.80 0.89 82.37 90.03 88.26 93.18 85.40 84.33
|     |     |     |     | 1.00 0.97 |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Tuna(Liuetal.,2025) 7B 1.00 0.97 0.81 0.91 0.88 0.83 0.90 90.42 91.68 90.94 91.87 90.73 86.76
Tuna-R 7B 1.00 0.95 0.82 0.89 0.86 0.79 0.88 86.00 91.80 91.03 93.48 84.89 86.35
Tuna-2 7B 0.99 0.96 0.80 0.91 0.84 0.76 0.87 89.50 91.40 91.91 88.81 86.54
92.07
Table3 Evaluation results under GPT-5.4 and Table4 ImageeditingresultsonImgEdit. Bolddenotesthebestresult
Claude Opus 4.7. Quality measures image real- among unified models and underlining denotes the second-best.
ismandfine-graineddetailrichness,whileDiver-
|     |     |     |     |     |     | Models | Add Adj. | Ext. | Rep. Rm. | Bg. | Sty. Hyb. | Act. | Total |
| --- | --- | --- | --- | --- | --- | ------ | -------- | ---- | -------- | --- | --------- | ---- | ----- |
sitymeasuresvariationamongimagesgenerated
Generation-onlyModels
| from the same | prompt.     | Bold    | denotes | the          | best |            |           |      |           |      |           |      |      |
| ------------- | ----------- | ------- | ------- | ------------ | ---- | ---------- | --------- | ---- | --------- | ---- | --------- | ---- | ---- |
|               |             |         |         |              |      | FLUX.1     | 4.25 4.15 | 2.35 | 4.56 3.57 | 4.26 | 4.57 3.68 | 4.63 | 4.00 |
| result and    | underlining | denotes | the     | second-best. |      |            |           |      |           |      |           |      |      |
|               |             |         |         |              |      | Qwen-Image | 4.38 4.16 | 3.43 | 4.66 4.14 | 4.38 | 4.81 3.82 | 4.69 | 4.27 |
UnifiedModels
GPT-5.4 ClaudeOpus4.7 OmniGen 3.47 3.04 1.71 2.94 2.43 3.21 4.19 2.24 3.38 2.96
|     |     |     |     |     |     | BAGEL | 3.56 3.31 | 1.70 | 3.30 2.62 | 3.24 | 4.49 2.38 | 4.17 | 3.20 |
| --- | --- | --- | --- | --- | --- | ----- | --------- | ---- | --------- | ---- | --------- | ---- | ---- |
Models Quality Diversity Quality Diversity UniWorld 3.82 3.64 2.27 3.47 3.24 2.99 4.21 2.96 2.74 3.26
|     |     |     |     |     |     | OmniGen2 | 3.57 3.06 | 1.77 | 3.74 3.20 | 3.57 | 4.81 2.52 | 4.68 | 3.44 |
| --- | --- | --- | --- | --- | --- | -------- | --------- | ---- | --------- | ---- | --------- | ---- | ---- |
Tuna
22.3% 20.6% 28.1% 28.2% GPT-Image 4.61 4.33 2.90 4.35 3.66 4.57 4.93 3.96 4.89 4.20
|     |     |     |     |     |     | T u n a | 4 . 4 3 | 2 . 4 6 |     | 4 . 5 2 | 4 . 6 9 | 4 . 7 6 |     |
| --- | --- | --- | --- | --- | --- | ------- | ------- | ------- | --- | ------- | ------- | ------- | --- |
Tuna-R 35.7% 30.9% 37.2% 29.9% 4 .4 8 4 .6 5 4 .5 5 4 .2 2 4 . 3 1
|        |     |     |     |     |     | T u n a-R | 4 . 4 6 4 . 2 | 7 2 . 3 8 | 4 . 6 1 4 | . 4 8 4 . 4 4 | 4 . 5 4 4 | . 0 6 4 . 4 3 | 4 . 1 8 |
| ------ | --- | --- | --- | --- | --- | --------- | ------------- | --------- | --------- | ------------- | --------- | ------------- | ------- |
| Tuna-2 |     |     |     |     |     | Tuna-2    |               |           |           |               |           |               |         |
32.1% 48.4% 34.8% 41.9% 4.34 4.13 2.22 4.53 4.42 4.36 4.58 3.91 4.28 4.09
replacing the representation encoder with the simple patchify layer. This may indicate that large-scale joint
training of a unified, monolithic architecture achieves better understanding performance than relying on the
inductive bias in the pretrained representation encoders in the modular setting. We show more analysis
|           | Tuna-R |     | Tuna-2 |            |      |     |     |     |     |     |     |     |     |
| --------- | ------ | --- | ------ | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
| comparing |        | and |        | in Section | 3.5. |     |     |     |     |     |     |     |     |
Tofurtherunderstandthebenefitofourpixel-spaceunifiedmodels,weincludeseveralpixel-centricbenchmarks
that focus heavily on visual reasoning over fine-grained visual details (e.g. recognizing very small objects in
high-resolution images). These benchmarks include V* (Wu and Xie, 2024), CountBench (Paiss et al., 2023)
|     |     |     |     |     |     |     | Tuna-R |     | Tuna-2 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | ------ | --- | --- | --- | --- |
and VisuLogic (Xu et al., 2025). As shown in Table 1, both and outperform latent-space
UMMs (e.g. Show-o2, Tuna, etc.) across all benchmarks, indicating the necessity of pixel-space visual
| representations | when | reasoning |     | over fine-grained |     | visual | details. |     |     |     |     |     |     |
| --------------- | ---- | --------- | --- | ----------------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- |
Imagegeneration. We evaluate the image generation performance of Tuna-2 on GenEval (Ghosh et al., 2023)
and DPG-Bench (Hu et al., 2024). As shown in Table 2, both Tuna-R and Tuna-2 achieve state-of-the-art
results on these benchmarks and perform competitively with contemporary approaches such as BAGEL,
Mogao, and Tuna. Between the two variants, Tuna-R consistently performs slightly better than Tuna-2,
suggesting that the semantic prior introduced by the representation encoder helps our method learn a stronger
image generation model. Overall, these results show that even without a VAE and while performing image
7

|                  |                |             |       | Original | Flux-VAE | RAE | Tuna-R | Tuna-2 |
| ---------------- | -------------- | ----------- | ----- | -------- | -------- | --- | ------ | ------ |
| Table5 Image     | reconstruction | performance | for   |          |          |     |        |        |
| different visual | tokenizers.    |             |       |          |          |     |        |        |
| Tokenizer        | Res.           | rFID↓ PSNR↑ | SSIM↑ |          |          |     |        |        |
| Specialized      | tokenizers     |             |       |          |          |     |        |        |
| SD-VAE           | 256            | 1.06 28.62  | 0.86  |          |          |     |        |        |
| GigaTok          | 256            | 0.51 21.32  | 0.69  |          |          |     |        |        |
| VA-VAE           | 256            | 0.26 28.59  | 0.80  |          |          |     |        |        |
| DC-AE            | 512            | 0.22 26.15  | 0.71  |          |          |     |        |        |
| MAE-Tok          | 512            | 0.62 –      | –     |          |          |     |        |        |
| TexTok           | 512            | 0.73 24.45  | 0.66  |          |          |     |        |        |
| FLUX.1[dev]-VAE† | 512            | 0.06 33.65  | 0.93  |          |          |     |        |        |
Unified tokenizers
| UniTok    | 256 | 0.38 –     | –    |                     |         |               |                    |     |
| --------- | --- | ---------- | ---- | ------------------- | ------- | ------------- | ------------------ | --- |
| TokenFlow | 384 | 0.63 22.77 | 0.73 |                     |         |               |                    |     |
| X-Omni†   | 512 | 8.30 15.66 | 0.38 |                     |         |               |                    |     |
| MingTok†  | 512 | 0.53 23.49 | 0.61 |                     |         |               |                    |     |
| RAE       | 256 | 0.61 19.20 | 0.44 |                     |         |               |                    |     |
| PS-VAE    | 256 | 0.20 28.79 | 0.82 |                     |         |               |                    |     |
| Tuna-R    | 512 | 0.12 32.22 | 0.93 |                     |         |               |                    |     |
| Tuna-2    | 512 | 0.15 32.80 | 0.93 |                     |         |               |                    |     |
|           |     |            |      | Figure4 Qualitative | results | for different | visual tokenizers. |     |
Tuna-2
generation entirely in pixel space, remains competitive with recent state-of-the-art unified models,
highlighting the effectiveness and scalability of our pixel-space generation design.
Since existing image generation benchmarks such as GenEval mainly evaluate text-image alignment and
the model’s world knowledge, we further adopt an LLM-judge-based evaluation to assess the quality and
diversity of images generated by Tuna-2, Tuna-R, and Tuna. Specifically, we sample 1.5K text prompts
and ask each model to generate four images per prompt. We then use GPT-5.4 (OpenAI, 2026) and Claude
Opus 4.7 (Anthropic, 2026) as judges to select the best model among the three for each prompt based on the
quality and diversity of the generated images, where quality mainly refers to realism and fine-grained detail
and texture fidelity, while diversity measures the extent to which the four generated images exhibit distinct
visual variations under the same prompt. The results are reported in Table 3. We find that under both LLM
| Tuna-2 |     |     |     |     |     |     | Tuna-R |     |
| ------ | --- | --- | --- | --- | --- | --- | ------ | --- |
judges, achieves competitive image generation quality, performing comparably to and better
than Tuna, while being significantly preferred in terms of diversity. These results demonstrate that our
encoder-free design is highly effective and enables Tuna-2 to generate both high quality and diverse images.
Imageediting. We further evaluate the image editing capability of Tuna-2 on ImgEdit (Ye et al., 2025). As
shown in Table 4, Tuna-2 achieves strong editing performance among unified models, outperforming earlier
baselines such as OmniGen (Xiao et al., 2025), BAGEL (Deng et al., 2025), UniWorld (Lin et al., 2025a), and
OmniGen2 (Wu et al., 2025b). While being slightly behind Tuna and Tuna-R, Tuna-2 remains competitive
with strong generation-only and unified editing systems, despite performing editing directly in pixel space
withoutrelyingonvisionencoders. Theseresultssuggestthatourpixel-spaceunifiedmodellingframeworkcan
effectively support instruction-guided image editing, while the small gap between Tuna-2 and encoder-based
variants indicates that pretrained visual priors may still provide benefits for fine-grained editing fidelity.
To further investigate the image generation capability of Tuna-2, we examine whether
Imagereconstruction.
the model can faithfully reconstruct an input image from its corresponding pixel-space visual representations.
To this end, we perform lightweight finetuning on an image reconstruction task and evaluate reconstruction
|     |     |     |     |     |     |     | Tuna-R | Tuna-2 |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------ |
quality on the ImageNet validation set (Deng et al., 2009). As shown in Table 5, both and
achieve strong reconstruction performance, ranking first among unified tokenizers and approaching specialized
image tokenizers such as the VAE model in FLUX.1 [dev] (Batifol et al., 2025). Figure 4 further shows that
our models produce substantially better reconstructions than other non-KL-regularized VAE approaches such
as RAE (Zheng et al., 2025). These results indicate that our pixel-space unified visual representation can
support strong image reconstruction and generation quality even without relying on VAE models.
8

Figure5 Comparison of the image generation (MSE) and language modelling (CE) loss curves based on different
understanding-generation data ratios during model training.
3.3 Ablation: ModelTrainingDynamics
To better understand the learning dynamics of our joint multimodal training paradigm, we conduct a series of
pretraining ablation studies on both Tuna-R and Tuna-2 by varying the sampling ratio between generation
and understanding data. We use the notation xgyu (e.g., 8g2u) to represent a generation-to-understanding
sampling ratio of x:y. As shown in Figure 5, increasing the proportion of either generation or understanding
data consistently reduces its corresponding training loss, namely MSE for flow matching and cross entropy
loss (CE) for language modelling. Notably, the MSE loss is more sensitive to changes in the sampling ratio,
while the CE loss varies within a relatively smaller range across different ratios. This suggests that both
tasks benefit from scaling up the amount of their corresponding training data, with the generation objective
being more affected by the data mixture. We also observe that a generation-to-understanding ratio of 7:3
(7g3u) achieves the best trade-off between the two objectives, yielding a strong balance between generation
and understanding performance. We therefore adopt this data sampling ratio in all experiments.
3.4 Ablation: Masking-basedFeatureLearning
To verify the effectiveness of our proposed masking-based feature learning strategy, we conduct controlled
experiments on both Tuna-R and Tuna-2 using the smaller Qwen-2.5-Instruct-1.5B backbone. Since we
expect this strategy to serve as a representation enhancement strategy after the model has acquired basic
multimodal knowledge, we do not apply this objective from the beginning of pretraining. Instead, we first
train all models for 50k steps; We then split each model variant into two groups: one continues standard
pretraining, while the other continues pretraining with the masking-based feature learning objective applied
with a probability of 50%. Both groups are further trained for another 50k steps. As shown in Table 6, this
9

|     |     | Tuna-R | Tuna-2, |     |     |     |
| --- | --- | ------ | ------- | --- | --- | --- |
Table6 Ablation study results for and with or without our proposed masking-based feature learning
| scheme | during pretraining. |     |          |      |            |         |
| ------ | ------------------- | --- | -------- | ---- | ---------- | ------- |
|        | Models              |     | OCRBench | MMVP | CountBench | GenEval |
|        | Tuna                |     | 56.9     | 54.0 | 55.6       | 57.2    |
|        | Tuna-Rw/oMasking    |     | 58.3     | 56.7 | 57.2       | 55.7    |
Tuna-Rw/Masking
|     |     |     | 59.2 | 58.0 | 58.2 | 56.0 |
| --- | --- | --- | ---- | ---- | ---- | ---- |
Tuna-2w/oMasking
|     |                 |     | 55.4 | 52.3 | 53.4 | 47.6 |
| --- | --------------- | --- | ---- | ---- | ---- | ---- |
|     | Tuna-2w/Masking |     | 56.8 | 55.7 | 57.6 | 48.2 |
strategy consistently improves performance on both understanding and generation benchmarks for both model
variants. We further observe that Tuna-2 benefits more from masked training than Tuna-R. We hypothesize
Tuna-R,
that this difference is related to the SigLIP 2 representation encoder used in since SigLIP 2 itself
is pretrained with a similar masked prediction objective. In addition, the results suggest that compressing
images into the VAE latent space before visual encoding (Tuna) can introduce certain information loss
for visual understanding, compared with directly encoding pixel-level inputs through the vision encoder
(Tuna-R).Basedonthesefindings, weapplythemasking-basedfeaturelearningstrategyduringthefinal40%
of pretraining, encouraging more robust visual representation learning for both multimodal understanding
and generation.
Figure6 Model accuracy curves with respect to training dataset size (measured by the number of tokens consumed by
| the model)    | for Tuna-R | and Tuna-2. |     |     |     |     |
| ------------- | ---------- | ----------- | --- | --- | --- | --- |
| 3.5 Analysis: | Tuna-Rvs.  | Tuna-2      |     |     |     |     |
OurexperimentalresultsinSection3.2revealtwointerestingfindings: First, withoutvisionencoders, Tuna-2
|     | Tuna-R |     |     |     | Tuna-R |     |
| --- | ------ | --- | --- | --- | ------ | --- |
outperforms on most image understanding benchmarks. Second, achieves similar or slightly
stronger performance than Tuna-2 on generation tasks. To better understand these trends, we plot the
performance curves of both models on understanding and generation benchmarks as the training data scale
increases. AsshowninFigure6,onthethreeunderstandingbenchmarks(OCRBench(Liuetal.,2024),MMVP
(Tong et al., 2024) and V* (Wu and Xie, 2024)), Tuna-R actually outperforms Tuna-2 during the early stage
Tuna-R,
of the training. We believe this advantage comes from the pretrained representation encoder in
whose rich semantic priors help the model acquire multimodal understanding capabilities more quickly at
Tuna-2 Tuna-R.
the beginning of training. Nevertheless, later catches up and eventually surpasses This
suggests that the monolithic, encoder-free design of Tuna-2 may be better suited to benefit from large-scale
unified multimodal pretraining, enabling it to develop stronger multimodal understanding capabilities.
For generation evaluation on GenEval (Ghosh et al., 2023), we observe that Tuna-R consistently outperforms
Tuna-2 throughout the entire training process. This suggests that the semantic priors provided by the
representation encoder play an important role in improving generation performance, which is consistent with
prior findings from REPA (Yu et al., 2024) and Tuna (Liu et al., 2025). However, this trend gradually
weakens as the training data scale increases. As shown in the figure, the two model variants achieve nearly
identicalperformanceafterSFT.Overall,comparedwithlatent-spacegeneration,bothTuna-RandTuna-2’s
| pixel-space | generation | paradigm achieves | competitive | performances. |     |     |
| ----------- | ---------- | ----------------- | ----------- | ------------- | --- | --- |
10

Input LLaVA-OV-1.5-8B Penguin-VL-8B Qwen2.5-VL-7B Tuna Tuna-R Tuna-2
“What in the picture isshining?”
“What is the purpleobject?”
“Anna loves kittens. She decided to go to a cat cafe to see them. As shown in the picture, what animaldid she see when she opened the door?”
“In a heated football match, players are sprinting, passing, and shooting the ball as the crowd roars with excitement. The player strikes with force,
kicking something flying through the air. What objectdid he kick away?”
Figure7 AttentionmapvisualizationforTuna-R,Tuna-2andotherbaselinemodels. Redareadenoteshighattention
scores and Blue area denotes low attention scores.
3.6 Analysis: AttentionMapVisualizations
To qualitatively analyze and compare the cross-modal alignment capabilities learned by different models, we
visualizetheattentionmapsofselectedkeywordsintheinputpromptwithrespecttotheinputimage. Wefocus
on the Tuna model family, including Tuna, Tuna-R, and Tuna-2, and compare them with representative
encoder-based open-source LMMs, including models with ViT-based encoders, such as LLaVA-OneVision-1.5
(An et al., 2025) and Qwen2.5-VL (Bai et al., 2025b), as well as models with LLM-based encoders, such as
Penguin-VL (Zhang et al., 2026a). The results are shown in Figure 7.
Our first observation is that Tuna-2 exhibits more accurate vision-language alignment in basic perception
scenarios. For example, in the “shining window” case, Tuna-2 consistently highlights the regions that
are semantically associated with “shining”, while other models tend to provide only coarse or incomplete
localization. In the “purple object” case, the attention activations of Tuna-2 are well aligned with the target
object, whereas other methods often show dispersed attention or spurious activations in irrelevant regions.
We further construct examples with misleading linguistic contexts to evaluate whether models overly rely on
language priors. For example, in the “dog cafe” case, the prompt suggests a cat cafe scenario, whereas the
actual animals in the image are dogs. Some models tend to rely on textual cues within the image (e.g. “dog
cafe” sign) instead of the actual visual subjects. In contrast, Tuna-2 places its attention on the truly relevant
visual regions, demonstrating more robust cross-modal alignment under misleading linguistic contexts.
In the more challenging counterintuitive “football match” case, we introduce both strong linguistic priors
and salient visual distractors. Specifically, the prompt contains strong football-related cues, such as “football
match”, “players”, and “kicking”. The image also includes a large and visually salient football as a distractor.
However, the actual object being kicked by the player is a glass cup. Most models are easily misled by either
11

the textual prior or the salient distractor and therefore attend to incorrect regions. In contrast, Tuna-2
accurately localizes the key object that is consistent with the question semantics, showing stronger robustness
in such counterintuitive settings.
Overall, as an encoder-free native multimodal architecture, Tuna-2 produces more accurate and stable
attention distributions across all cases. These results suggest that Tuna-2 learns more reliable visual
representations, leading to more consistent cross-modal alignment and better robustness to misleading
language priors and visual distractors.
4 RelatedWorks
4.1 UnifiedMultimodalModels
Unified multimodal models (UMMs) (Xin et al., 2025; You et al., 2026; Tian et al., 2026; Tong et al., 2026;
Zhang et al., 2026b; Yang et al., 2025b; Shi et al., 2025; Shen et al., 2025; Xie et al., 2025a; Niu et al.,
2025; Wei et al., 2025a; Wang et al., 2025f; Wei et al., 2025b; Cui et al., 2025; He et al., 2025; Wang et al.,
2025a; Hao et al., 2025; Team et al., 2025; AI et al., 2025; Wu et al., 2025c; Fan et al., 2025a) seek to
integrate multimodal understanding and generation within a single framework. A prevalent approach for
UMMs combines autoregressive (AR) language models for text generation (Grattafiori et al., 2024; Bai
et al., 2023) with diffusion or flow-matching models for visual generation (Ho et al., 2020; Rombach et al.,
2022). While AR models excel at understanding, their integration with high-fidelity generation typically relies
on decoupled encoders (Chen et al., 2025c; Liao et al., 2025; Deng et al., 2025), leading to representation
mismatches and inefficiencies. To address this problem, recent works such as UniTok (Ma et al., 2025a),
TokLip (Lin et al., 2025b), UniLip (Tang et al., 2025), UniFlow (Yue et al., 2025), UAE (Fan et al., 2025b)
and OpenVision 3 (Zhang et al., 2026c) pretrain unified vision tokenizers for both semantic understanding and
visual reconstruction. Meanwhile, native UMMs like the Show-o series (Xie et al., 2024, 2025b), Tuna (Liu
et al., 2025), Ming-UniVision (Huang et al., 2025b), and Transfusion-RAE (Tong et al., 2026) build unified
representations using pretrained VAE (Wan et al., 2025) and representation encoders (Zheng et al., 2025).
Despite the significant progress, recent native UMMs still predominantly rely on VAE latents to build their
unifiedrepresentations,whichhindersthemodel’sperformanceonfine-grainedvisualperceptionandreasoning.
In this work, we systematically investigate pixel-space UMMs with Tuna-R and Tuna-2. Concurrent to our
work, SenseNova-U1 (Diao et al., 2026b) investigates a similar encoder-free architecture (Neo-Unify (Diao
et al., 2026a)) with a mixture-of-transformer (MOT) (Liang et al., 2024) style LLM decoder.
4.2 Encoder-FreeMultimodalUnderstandingandGeneration
Large multimodal models (LMMs) have traditionally adopted a modular design, combining pixel-space
representation encoders with LLM decoders. Early work on LMMs explored integration strategies between
representation encoders and LLM decoders, such as using cross-attention in Flamingo (Alayrac et al., 2022)
and MLP connectors in LLaVA (Liu et al., 2023). Subsequent research largely followed LLaVA and scaled
this paradigm to larger models (Wang et al., 2024a; Bai et al., 2025b; Wang et al., 2025d; An et al., 2026c),
datasets (Zhang et al., 2024; Wiedmann et al., 2025; An et al., 2025), and diverse understanding tasks (Cheng
et al., 2024; Li et al., 2024c; Ren et al., 2025). More recently, an alternative design of employing a monolithic,
encoder-free transformer to natively process vision and language has emerged (Wang et al., 2025b; Li et al.,
2026; Lei et al., 2025; Shukor et al., 2025). Fuyu (Bavishi et al., 2023), EVE (Diao et al., 2024), Chameleon
(Team, 2024), Mono-InternVL (Luo et al., 2025) and NEO (Diao et al., 2025) employ simple MLP or patch
embedding layers to tokenize raw image pixels into patches, and jointly process these image patches with
language tokens using a single transformer. In this work, we show that both the representation encoder-based
design and the monolithic design can be integrated into pixel-space UMMs and achieve high performance on
multimodal understanding.
Recentvisualgenerationmodels(Yangetal.,2026;Chenetal.,2024;Anetal.,2026a,b;Zhouetal.,2025;Qiu
etal.,2025)typicallyoperateinacompressedlatentspaceusingKL-orVQ-regularizedVAEs(Rombachetal.,
2022; Esser et al., 2024; Wu et al., 2025a; Esser et al., 2021; Sun et al., 2024). Although pixel-space diffusion
or flow matching is often considered more challenging, recent work such as PixelFlow (Chen et al., 2025b),
12

PixNerd (Wang et al., 2025c), DiP (Chen et al., 2025d), PixelDiT (Yu et al., 2025) and JiT (Li and He, 2025)
increasingly suggests that pixel-space flow matching has the potential to match or surpass latent diffusion
models. However, these studies are usually limited to small-scale settings (e.g., class-conditioned generation
on ImageNet (Russakovsky et al., 2015)). We demonstrate in Tuna-2 that pixel-space flow matching can be
scaled up to large-scale unified multimodal pretraining and support free-form text-to-image generation and
image editing.
5 Conclusion
We introduced Tuna-2, a family of native unified multimodal models that perform multimodal understanding
and visual generation directly in pixel space, without relying on VAE encoders or latent diffusion. By
combining a unified vision-language backbone with a pixel-space flow matching head, Tuna-2 supports
image understanding, text-to-image generation, and image editing within a single framework. We further
instantiated Tuna-2 with both a representation encoder-based variant and an encoder-free monolithic variant,
and showed that both designs achieve strong performance across multimodal understanding and generation
benchmarks. Our experiments demonstrate that Tuna-2 surpasses prior latent-space unified models such
as Tuna and Show-o2 on fine-grained visual understanding benchmarks while remaining competitive with
state-of-the-art unified models on image generation. Overall, these results highlight the effectiveness and
scalability of pixel-space unified multimodal modelling and suggest a promising direction for future native
UMMs.
13

References
Inclusion AI, Bowen Ma, Cheng Zou, Canxiang Yan, Chunxiang Jin, Chunjie Shen, Chenyu Lian, Dandan Zheng,
Fudong Wang, Furong Xu, et al. Ming-flash-omni: A sparse, unified architecture for multimodal perception and
| generation. | arXiv | preprint | arXiv:2510.24821, |     |     | 2025. |     |     |     |
| ----------- | ----- | -------- | ----------------- | --- | --- | ----- | --- | --- | --- |
Jean-BaptisteAlayrac,JeffDonahue,PaulineLuc,AntoineMiech,IainBarr,YanaHasson,KarelLenc,ArthurMensch,
Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. Advances in
| neural information |     | processing | systems, |     | 35:23716–23736, |     | 2022. |     |     |
| ------------------ | --- | ---------- | -------- | --- | --------------- | --- | ----- | --- | --- |
Xiang An, Yin Xie, Kaicheng Yang, Wenkang Zhang, Xiuwei Zhao, Zheng Cheng, Yirui Wang, Songcen Xu, Changrui
Chen,ChunshengWu,etal. Llava-onevision-1.5: Fullyopenframeworkfordemocratizedmultimodaltraining. arXiv
| preprint | arXiv:2509.23661, |     | 2025. |     |     |     |     |     |     |
| -------- | ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
ZhaochongAn,MenglinJia,HaonanQiu,ZijianZhou,XiaokeHuang,ZhihengLiu,WeimingRen,KumaraKahatapitiya,
Ding Liu, Sen He, et al. Onestory: Coherent multi-shot video generation with adaptive memory. CVPR, 2026a.
Zhaochong An, Orest Kupyn, Théo Uscidda, Andrea Colaco, Karan Ahuja, Serge Belongie, Mar Gonzalez-Franco, and
Marta Tintore Gazulla. Vggrpo: Towards world-consistent video generation with 4d latent reward. arXiv preprint
| arXiv:2603.26599, |     | 2026b. |     |     |     |     |     |     |     |
| ----------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
Zhaochong An, Zirui Li, Mingqiao Ye, Feng Qiao, Jiaang Li, Zongwei Wu, Vishal Thengane, Chengzu Li, Lei Li,
Luc Van Gool, et al. Video understanding: From geometry and semantics to unified models. Machine Intelligence
| Research, | 2026c. |     |     |     |     |     |     |     |     |
| --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Anthropic. Introducing claude opus 4.7. https://www.anthropic.com/news/claude-opus-4-7, April 2026. Accessed:
2026-04-24.
Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang,
| et al. Qwen | technical | report. | arXiv | preprint |     | arXiv:2309.16609, |     | 2023. |     |
| ----------- | --------- | ------- | ----- | -------- | --- | ----------------- | --- | ----- | --- |
Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang
Gao, Chunjiang Ge, et al. Qwen3-vl technical report. arXiv preprint arXiv:2511.21631, 2025a.
Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun
| Tang, et | al. Qwen2. | 5-vl | technical | report. | arXiv | preprint | arXiv:2502.13923, |     | 2025b. |
| -------- | ---------- | ---- | --------- | ------- | ----- | -------- | ----------------- | --- | ------ |
Stephen Batifol, Andreas Blattmann, Frederic Boesel, Saksham Consul, Cyril Diagne, Tim Dockhorn, Jack English,
Zion English, Patrick Esser, Sumith Kulal, et al. Flux. 1 kontext: Flow matching for in-context image generation
| and editing | in  | latent space. | arXiv | e-prints, | pages | arXiv–2506, |     | 2025. |     |
| ----------- | --- | ------------- | ----- | --------- | ----- | ----------- | --- | ----- | --- |
Rohan Bavishi, Erich Elsen, Curtis Hawthorne, Maxwell Nye, Augustus Odena, Arushi Somani, and Sağnak Taşırlar.
Fuyu-8b: Amultimodalarchitectureforaiagents,October2023. https://www.adept.ai/blog/fuyu-8b/. Adeptblog
post.
Akhiad Bercovich, Itay Levy, Izik Golan, Mohammad Dabbah, Ran El-Yaniv, Omri Puny, Ido Galil, Zach Moshe,
TomerRonen,NajeebNabwani,etal. Llama-nemotron: Efficientreasoningmodels. arXivpreprintarXiv:2505.00949,
2025.
Huanqia Cai, Sihan Cao, Ruoyi Du, Peng Gao, Steven Hoi, Zhaohui Hou, Shijie Huang, Dengyang Jiang, Xin Jin,
LiangchenLi,etal. Z-image: Anefficientimagegenerationfoundationmodelwithsingle-streamdiffusiontransformer.
| arXiv preprint |     | arXiv:2511.22699, |     | 2025. |     |     |     |     |     |
| -------------- | --- | ----------------- | --- | ----- | --- | --- | --- | --- | --- |
HuiwenChang,HanZhang,LuJiang,CeLiu,andWilliamTFreeman. Maskgit: Maskedgenerativeimagetransformer.
In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 11315–11325, 2022.
Jiuhai Chen, Zhiyang Xu, Xichen Pan, Yushi Hu, Can Qin, Tom Goldstein, Lifu Huang, Tianyi Zhou, Saining Xie,
Silvio Savarese, et al. Blip3-o: A family of fully open unified multimodal models-architecture, training and dataset.
| arXiv preprint |     | arXiv:2505.09568, |     | 2025a. |     |     |     |     |     |
| -------------- | --- | ----------------- | --- | ------ | --- | --- | --- | --- | --- |
Junsong Chen, Chongjian Ge, Enze Xie, Yue Wu, Lewei Yao, Xiaozhe Ren, Zhongdao Wang, Ping Luo, Huchuan Lu,
and Zhenguo Li. Pixart-σ: Weak-to-strong training of diffusion transformer for 4k text-to-image generation. In
| European | Conference | on  | Computer | Vision, | pages | 74–91. | Springer, | 2024. |     |
| -------- | ---------- | --- | -------- | ------- | ----- | ------ | --------- | ----- | --- |
Shoufa Chen, Chongjian Ge, Shilong Zhang, Peize Sun, and Ping Luo. Pixelflow: Pixel-space generative models with
| flow. arXiv | preprint | arXiv:2504.07963, |     |     | 2025b. |     |     |     |     |
| ----------- | -------- | ----------------- | --- | --- | ------ | --- | --- | --- | --- |
14

XiaokangChen,ZhiyuWu,XingchaoLiu,ZizhengPan,WenLiu,ZhendaXie,XingkaiYu,andChongRuan. Janus-pro:
Unified multimodal understanding and generation with data and model scaling. arXiv preprint arXiv:2501.17811,
2025c.
Zhennan Chen, Junwei Zhu, Xu Chen, Jiangning Zhang, Xiaobin Hu, Hanzhen Zhao, Chengjie Wang, Jian Yang, and
Ying Tai. Dip: Taming diffusion models in pixel space. arXiv preprint arXiv:2511.18822, 2025d.
Zesen Cheng, Sicong Leng, Hang Zhang, Yifei Xin, Xin Li, Guanzheng Chen, Yongxin Zhu, Wenqi Zhang, Ziyang Luo,
Deli Zhao, et al. Videollama 2: Advancing spatial-temporal modeling and audio understanding in video-llms. arXiv
preprint arXiv:2406.07476, 2024.
YufengCui,HonghaoChen,HaogeDeng,XuHuang,XinghangLi,JirongLiu,YangLiu,ZhuoyanLuo,JinshengWang,
Wenxuan Wang, et al. Emu3. 5: Native multimodal models are world learners. arXiv preprint arXiv:2510.26583,
2025.
Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie,
Ziang Song, et al. Emerging properties in unified multimodal pretraining. arXiv preprint arXiv:2505.14683, 2025.
Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image
database. In 2009 IEEE conference on computer vision and pattern recognition, pages 248–255. Ieee, 2009.
Haiwen Diao, Yufeng Cui, Xiaotong Li, Yueze Wang, Huchuan Lu, and Xinlong Wang. Unveiling encoder-free
vision-language models. Advances in Neural Information Processing Systems, 37:52545–52567, 2024.
HaiwenDiao,MingxuanLi,SileiWu,LinjunDai,XiaohuaWang,HanmingDeng,LeweiLu,DahuaLin,andZiweiLiu.
From pixels to words–towards native vision-language primitives at scale. arXiv preprint arXiv:2510.14979, 2025.
Haiwen Diao, Lewei Lu, and Ziwei Liu. NEO-unify: Building native multimodal unified models end to end. https:
//huggingface.co/blog/sensenova/neo-unify, March 2026a. Hugging Face Community Article, published March 5,
2026.
Haiwen Diao, Penghao Wu, Hanming Deng, Jiahao Wang, Shihao Bai, Silei Wu, Weichen Fan, Wenjie Ye, Wenwen
Tong, Xiangyu Fan, Yan Li, Yubo Wang, Zhijie Cao, Zhiqian Lin, Zhitao Yang, Zhongang Cai, Yuwei Niu, Yue
Zhu, Bo Liu, Chengguang Lv, Haojia Yu, Haozhe Xie, Hongli Wang, Jianan Fan, Jiaqi Li, Jiefan Lu, Jingcheng
Ni, Junxiang Xu, Kaihuan Liang, Lianqiang Shi, Linjun Dai, Linyan Wang, Oscar Qian, Peng Gao, Pengfei Liu,
Qingping Sun, Rui Shen, Ruisi Wang, Shengnan Ma, Shuang Yang, Siyi Xie, Siying Li, Tianbo Zhong, Xiangli
Kong, Xuanke Shi, Yang Gao, Yongqiang Yao, Yves Wang, Zhengqi Bai, Zhengyu Lin, Zixin Yin, Wenxiu Sun,
Ruihao Gong, Quan Wang, Lewei Lu, Lei Yang, Ziwei Liu, and Dahua Lin. Sensenova-u1: Unifying multimodal
understanding and generation with neo-unify architecture, 2026b. https://arxiv.org/abs/2605.12500.
Patrick Esser, Robin Rombach, and Bjorn Ommer. Taming transformers for high-resolution image synthesis. In
Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 12873–12883, 2021.
Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas Müller, Harry Saini, Yam Levi, Dominik
Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers for high-resolution image synthesis. In
Forty-first international conference on machine learning, 2024.
Lijie Fan, Luming Tang, Siyang Qin, Tianhong Li, Xuan Yang, Siyuan Qiao, Andreas Steiner, Chen Sun, Yuanzhen Li,
Tao Zhu, et al. Unified autoregressive visual generation and understanding with continuous tokens. arXiv preprint
arXiv:2503.13436, 2025a.
Weichen Fan, HaiwenDiao, QuanWang, Dahua Lin, and ZiweiLiu. The prism hypothesis: Harmonizingsemantic and
pixel representations via unified autoencoding. arXiv preprint arXiv:2512.19693, 2025b.
Yu Gao, Lixue Gong, Qiushan Guo, Xiaoxia Hou, Zhichao Lai, Fanshi Li, Liang Li, Xiaochen Lian, Chao Liao, Liyang
Liu, et al. Seedream 3.0 technical report. arXiv preprint arXiv:2504.11346, 2025.
Zigang Geng, Yibing Wang, Yeyao Ma, Chen Li, Yongming Rao, Shuyang Gu, Zhao Zhong, Qinglin Lu, Han Hu,
XiaosongZhang,etal. X-omni: Reinforcementlearningmakesdiscreteautoregressiveimagegenerativemodelsgreat
again. arXiv preprint arXiv:2507.22058, 2025.
Dhruba Ghosh, Hannaneh Hajishirzi, and Ludwig Schmidt. Geneval: An object-focused framework for evaluating
text-to-image alignment. Advances in Neural Information Processing Systems, 36:52132–52152, 2023.
Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. arXiv preprint
arXiv:2407.21783, 2024.
15

Jiaming Han, Hao Chen, Yang Zhao, Hanyu Wang, Qi Zhao, Ziyan Yang, Hao He, Xiangyu Yue, and Lu Jiang.
Vision as a dialect: Unifying visual understanding and generation via text-aligned representations. arXiv preprint
| arXiv:2506.18898, | 2025. |     |     |
| ----------------- | ----- | --- | --- |
Jitai Hao, Hao Liu, Xinyan Xiao, Qiang Huang, and Jun Yu. Uni-x: Mitigating modality conflict with a two-end-
separated architecture for unified multimodal models. arXiv preprint arXiv:2509.24365, 2025.
KaimingHe,XinleiChen,SainingXie,YanghaoLi,PiotrDollár,andRossGirshick. Maskedautoencodersarescalable
vision learners. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages
| 16000–16009, | 2022. |     |     |
| ------------ | ----- | --- | --- |
Xin He, Longhui Wei, Jianbo Ouyang, Minghui Liao, Lingxi Xie, and Qi Tian. Emma: Efficient multimodal
understanding, generation, and editing with a unified architecture. arXiv preprint arXiv:2512.04810, 2025.
Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. Advances in neural information
| processing | systems, 33:6840–6851, | 2020. |     |
| ---------- | ---------------------- | ----- | --- |
Emiel Hoogeboom, Jonathan Heek, and Tim Salimans. simple diffusion: End-to-end diffusion for high resolution
images. In International Conference on Machine Learning, pages 13213–13232. PMLR, 2023.
Xiwei Hu, Rui Wang, Yixiao Fang, Bin Fu, Pei Cheng, and Gang Yu. Ella: Equip diffusion models with llm for
| enhanced | semantic alignment. | arXiv preprint arXiv:2403.05135, | 2024. |
| -------- | ------------------- | -------------------------------- | ----- |
Ziyuan Huang, DanDan Zheng, Cheng Zou, Rui Liu, Xiaolong Wang, Kaixiang Ji, Weilong Chai, Jianxin Sun,
Libin Wang, Yongjie Lv, Taozhi Huang, Jiajia Liu, Qingpei Guo, Ming Yang, Jingdong Chen, and Jun Zhou.
Ming-univision: Joint image understanding and generation with a unified continuous tokenizer. arXiv preprint
| arXiv:2510.06590, | 2025a. |     |     |
| ----------------- | ------ | --- | --- |
Ziyuan Huang, DanDan Zheng, Cheng Zou, Rui Liu, Xiaolong Wang, Kaixiang Ji, Weilong Chai, Jianxin Sun, Libin
Wang, Yongjie Lv, et al. Ming-univision: Joint image understanding and generation with a unified continuous
| tokenizer. | arXiv preprint arXiv:2510.06590, | 2025b. |     |
| ---------- | -------------------------------- | ------ | --- |
Drew A Hudson and Christopher D Manning. Gqa: A new dataset for real-world visual reasoning and compositional
question answering. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages
| 6700–6709, | 2019. |     |     |
| ---------- | ----- | --- | --- |
Aniruddha Kembhavi, Mike Salvato, Eric Kolve, Minjoon Seo, Hannaneh Hajishirzi, and Ali Farhadi. A diagram is
worth a dozen images. In European conference on computer vision, pages 235–251. Springer, 2016.
WeixianLei,JiacongWang,HaochenWang,XiangtaiLi,JunHaoLiew,JiashiFeng,andZilongHuang. Thescalability
of simplicity: Empirical analysis of vision-language learning with a single transformer. In Proceedings of the
IEEE/CVF International Conference on Computer Vision, pages 20758–20769, 2025.
Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Peiyuan Zhang, Yanwei Li,
Ziwei Liu, et al. Llava-onevision: Easy visual task transfer. arXiv preprint arXiv:2408.03326, 2024a.
Bohao Li, Yuying Ge, Yi Chen, Yixiao Ge, Ruimao Zhang, and Ying Shan. Seed-bench-2-plus: Benchmarking
multimodal large language models with text-rich visual comprehension. arXiv preprint arXiv:2404.16790, 2024b.
Han Li, Xinyu Peng, Yaoming Wang, Zelin Peng, Xin Chen, Rongxiang Weng, Jingang Wang, Xunliang Cai, Wenrui
Dai, and Hongkai Xiong. Onecat: Decoder-only auto-regressive model for unified understanding and generation.
| arXiv preprint | arXiv:2509.03498, | 2025. |     |
| -------------- | ----------------- | ----- | --- |
TianhongLiandKaimingHe.Backtobasics: Letdenoisinggenerativemodelsdenoise.arXivpreprintarXiv:2511.13720,
2025.
Tianle Li, Yongming Rao, Winston Hu, and Yu Cheng. Breen: bridge data-efficient encoder-free multimodal learning
with learnable queries. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision,
| pages 5384–5395, | 2026. |     |     |
| ---------------- | ----- | --- | --- |
Xinhao Li, Yi Wang, Jiashuo Yu, Xiangyu Zeng, Yuhan Zhu, Haian Huang, Jianfei Gao, Kunchang Li, Yinan He,
Chenting Wang, et al. Videochat-flash: Hierarchical compression for long-context video modeling. arXiv preprint
| arXiv:2501.00574, | 2024c. |     |     |
| ----------------- | ------ | --- | --- |
WeixinLiang,LiliYu,LiangLuo,SrinivasanIyer,NingDong,ChuntingZhou,GargiGhosh,MikeLewis,Wen-tauYih,
Luke Zettlemoyer, et al. Mixture-of-transformers: A sparse and scalable architecture for multi-modal foundation
| models. arXiv | preprint arXiv:2411.04996, | 2024. |     |
| ------------- | -------------------------- | ----- | --- |
16

Chao Liao, Liyang Liu, Xun Wang, Zhengxiong Luo, Xinyu Zhang, Wenliang Zhao, Jie Wu, Liang Li, Zhi Tian,
and Weilin Huang. Mogao: An omni foundation model for interleaved multi-modal generation. arXiv preprint
| arXiv:2505.05472, | 2025. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
Bin Lin, Zongjian Li, Xinhua Cheng, Yuwei Niu, Yang Ye, Xianyi He, Shenghai Yuan, Wangbo Yu, Shaodong Wang,
Yunyang Ge, et al. Uniworld: High-resolution semantic encoders for unified visual understanding and generation.
| arXiv preprint | arXiv:2506.03147, | 2025a. |     |     |     |
| -------------- | ----------------- | ------ | --- | --- | --- |
Haokun Lin, Teng Wang, Yixiao Ge, Yuying Ge, Zhichao Lu, Ying Wei, Qingfu Zhang, Zhenan Sun, and Ying Shan.
Toklip: Marry visual tokens to clip for multimodal comprehension and generation, 2025b. https://arxiv.org/abs/
2505.05422.
Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative
| modeling. | arXiv preprint | arXiv:2210.02747, | 2022. |     |     |
| --------- | -------------- | ----------------- | ----- | --- | --- |
HaotianLiu,ChunyuanLi,QingyangWu,andYongJaeLee. Visualinstructiontuning. Advancesinneuralinformation
| processing | systems, 36:34892–34916, | 2023. |     |     |     |
| ---------- | ------------------------ | ----- | --- | --- | --- |
Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate and transfer data with
| rectified flow. | arXiv preprint | arXiv:2209.03003, | 2022. |     |     |
| --------------- | -------------- | ----------------- | ----- | --- | --- |
YuliangLiu,ZhangLi,MingxinHuang,BiaoYang,WenwenYu,ChunyuanLi,Xu-ChengYin,Cheng-LinLiu,Lianwen
Jin,andXiangBai. Ocrbench: onthehiddenmysteryofocrinlargemultimodalmodels. Science China Information
| Sciences, | 67(12):220102, | 2024. |     |     |     |
| --------- | -------------- | ----- | --- | --- | --- |
ZhihengLiu,WeimingRen,HaozheLiu,ZijianZhou,ShoufaChen,HaonanQiu,XiaokeHuang,ZhaochongAn,Fanny
Yang, Aditya Patel, et al. Tuna: Taming unified visual representations for native unified multimodal models. arXiv
| preprint arXiv:2512.02014, |     | 2025. |     |     |     |
| -------------------------- | --- | ----- | --- | --- | --- |
Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101, 2017.
Gen Luo, Xue Yang, Wenhan Dou, Zhaokai Wang, Jiawen Liu, Jifeng Dai, Yu Qiao, and Xizhou Zhu. Mono-internvl:
Pushing the boundaries of monolithic multimodal large language models with endogenous visual pre-training. In
Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 24960–24971, 2025.
Chuofan Ma, Yi Jiang, Junfeng Wu, Jihan Yang, Xin Yu, Zehuan Yuan, Bingyue Peng, and Xiaojuan Qi. Unitok: A
unified tokenizer for visual generation and understanding. arXiv preprint arXiv:2502.20321, 2025a.
YiyangMa,XingchaoLiu,XiaokangChen,WenLiu,ChengyueWu,ZhiyuWu,ZizhengPan,ZhendaXie,HaoweiZhang,
Xingkai Yu, et al. Janusflow: Harmonizing autoregression and rectified flow for unified multimodal understanding
andgeneration. InProceedings of the Computer Vision and Pattern Recognition Conference,pages7739–7751,2025b.
Ahmed Masry, Xuan Long Do, Jia Qing Tan, Shafiq Joty, and Enamul Hoque. Chartqa: A benchmark for question
answeringaboutchartswithvisualandlogicalreasoning. InFindingsoftheassociationforcomputationallinguistics:
| ACL 2022, | pages 2263–2279, | 2022. |     |     |     |
| --------- | ---------------- | ----- | --- | --- | --- |
Yuwei Niu, Weiyang Jin, Jiaqi Liao, Chaoran Feng, Peng Jin, Bin Lin, Zongjian Li, Bin Zhu, Weihao Yu, and Li Yuan.
Does understanding inform generation in unified multimodal models? from analysis to path forward. arXiv preprint
| arXiv:2511.20561, | 2025. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
OpenAI. Introducing gpt-5.4. https://openai.com/index/introducing-gpt-5-4/, March 2026. Accessed: 2026-04-24.
Roni Paiss, Ariel Ephrat, Omer Tov, Shiran Zada, Inbar Mosseri, Michal Irani, and Tali Dekel. Teaching clip to count
to ten. In Proceedings of the IEEE/CVF international conference on computer vision, pages 3170–3180, 2023.
Haonan Qiu, Shikun Liu, Zijian Zhou, Zhaochong An, Weiming Ren, Zhiheng Liu, Jonas Schult, Sen He, Shoufa Chen,
Yuren Cong, et al. Histream: Efficient high-resolution video generation via redundancy-eliminated streaming. arXiv
| preprint arXiv:2512.21338, |     | 2025. |     |     |     |
| -------------------------- | --- | ----- | --- | --- | --- |
Liao Qu, Huichao Zhang, Yiheng Liu, Xu Wang, Yi Jiang, Yiming Gao, Hu Ye, Daniel K Du, Zehuan Yuan, and
Xinglong Wu. Tokenflow: Unified image tokenizer for multimodal understanding and generation. In Proceedings of
| the Computer | Vision and | Pattern Recognition | Conference, | pages 2545–2555, | 2025. |
| ------------ | ---------- | ------------------- | ----------- | ---------------- | ----- |
A Yang Qwen, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengpeng Li, Dayiheng Liu, Fei
| Huang, Haoran | Wei, et al. | Qwen2. 5 technical | report. | arXiv preprint, | 2024. |
| ------------- | ----------- | ------------------ | ------- | --------------- | ----- |
17

AlecRadford,JongWookKim,ChrisHallacy,AdityaRamesh,GabrielGoh,SandhiniAgarwal,GirishSastry,Amanda
Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision.
| In International | conference | on machine | learning, | pages 8748–8763. | PmLR, 2021. |
| ---------------- | ---------- | ---------- | --------- | ---------------- | ----------- |
Weiming Ren, Wentao Ma, Huan Yang, Cong Wei, Ge Zhang, and Wenhu Chen. Vamba: Understanding hour-long
videos with hybrid mamba-transformers. In Proceedings of the IEEE/CVF International Conference on Computer
| Vision, pages | 21197–21208, | 2025. |     |     |     |
| ------------- | ------------ | ----- | --- | --- | --- |
Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-resolution image
synthesis with latent diffusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern
| recognition, | pages 10684–10695, | 2022. |     |     |     |
| ------------ | ------------------ | ----- | --- | --- | --- |
OlgaRussakovsky,JiaDeng,HaoSu,JonathanKrause,SanjeevSatheesh,SeanMa,ZhihengHuang,AndrejKarpathy,
Aditya Khosla, Michael Bernstein, et al. Imagenet large scale visual recognition challenge. International journal of
| computer | vision, 115(3):211–252, | 2015. |     |     |     |
| -------- | ----------------------- | ----- | --- | --- | --- |
Tao Shen, Xin Wan, Taicai Chen, Rui Zhang, Junwen Pan, Dawei Lu, Fanding Lei, Zhilin Lu, Yunfei Yang, Chen
Cheng, et al. Mammothmoda2: A unified ar-diffusion framework for multimodal understanding and generation.
| arXiv preprint | arXiv:2511.18262, | 2025. |     |     |     |
| -------------- | ----------------- | ----- | --- | --- | --- |
Qingyu Shi, Jinbin Bai, Zhuoran Zhao, Wenhao Chai, Kaidong Yu, Jianzong Wu, Shuangyong Song, Yunhai Tong,
Xiangtai Li, Xuelong Li, et al. Muddit: Liberating generation beyond text-to-image with a unified discrete diffusion
| model. arXiv | preprint | arXiv:2505.23606, | 2025. |     |     |
| ------------ | -------- | ----------------- | ----- | --- | --- |
Mustafa Shukor, Enrico Fini, Victor Guilherme Turrisi da Costa, Matthieu Cord, Joshua Susskind, and Alaaeldin
El-Nouby. Scaling laws for native multimodal models. In Proceedings of the IEEE/CVF International Conference
| on Computer | Vision, pages | 12–23, | 2025. |     |     |
| ----------- | ------------- | ------ | ----- | --- | --- |
Peize Sun, Yi Jiang, Shoufa Chen, Shilong Zhang, Bingyue Peng, Ping Luo, and Zehuan Yuan. Autoregressive model
beats diffusion: Llama for scalable image generation. arXiv preprint arXiv:2406.06525, 2024.
Hao Tang, Chenwei Xie, Xiaoyi Bao, Tingyu Weng, Pandeng Li, Yun Zheng, and Liwei Wang. Unilip: Adapting clip
for unified multimodal understanding, generation and editing. arXiv preprint arXiv:2507.23278, 2025.
Chameleon Team. Chameleon: Mixed-modal early-fusion foundation models. arXiv preprint arXiv:2405.09818, 2024.
Meituan LongCat Team, Hanghang Ma, Haoxian Tan, Jiale Huang, Junqiang Wu, Jun-Yan He, Lishuai Gao, Songlin
Xiao, Xiaoming Wei, Xiaoqi Ma, et al. Longcat-image technical report. arXiv preprint arXiv:2512.07584, 2025.
Changyao Tian, Danni Yang, Guanzhou Chen, Erfei Cui, Zhaokai Wang, Yuchen Duan, Penghao Yin, Sitao Chen,
GanlinYang,MingxinLiu,etal. Internvl-u: Democratizingunifiedmultimodalmodelsforunderstanding,reasoning,
| generation | and editing. | arXiv preprint | arXiv:2603.09877, | 2026. |     |
| ---------- | ------------ | -------------- | ----------------- | ----- | --- |
Shengbang Tong, Zhuang Liu, Yuexiang Zhai, Yi Ma, Yann LeCun, and Saining Xie. Eyes wide shut? exploring the
visualshortcomingsofmultimodalllms. InProceedings of the IEEE/CVF conference on computer vision and pattern
| recognition, | pages 9568–9578, | 2024. |     |     |     |
| ------------ | ---------------- | ----- | --- | --- | --- |
Shengbang Tong, David Fan, John Nguyen, Ellis Brown, Gaoyue Zhou, Shengyi Qian, Boyang Zheng, Théophane
Vallaeys, Junlin Han, Rob Fergus, et al. Beyond language modeling: An exploration of multimodal pretraining.
| arXiv preprint | arXiv:2603.03276, | 2026. |     |     |     |
| -------------- | ----------------- | ----- | --- | --- | --- |
Michael Tschannen, Alexey Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil
Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, et al. Siglip 2: Multilingual vision-language
encoders with improved semantic understanding, localization, and dense features. arXiv preprint arXiv:2502.14786,
2025.
Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao
Yang, et al. Wan: Open and advanced large-scale video generative models. arXiv preprint arXiv:2503.20314, 2025.
Guo-Hua Wang, Shanshan Zhao, Xinjie Zhang, Liangfu Cao, Pengxin Zhan, Lunhao Duan, Shiyin Lu, Minghao Fu,
Xiaohao Chen, Jianshan Zhao, et al. Ovis-u1 technical report. arXiv preprint arXiv:2506.23044, 2025a.
Han Wang, Yongjie Ye, Bingru Li, Yuxiang Nie, Jinghui Lu, Jingqun Tang, Yanjie Wang, and Can Huang. Vision as
| lora. arXiv | preprint arXiv:2503.20680, |     | 2025b. |     |     |
| ----------- | -------------------------- | --- | ------ | --- | --- |
PengWang,ShuaiBai,SinanTan,ShijieWang,ZhihaoFan,JinzeBai,KeqinChen,XuejingLiu,JialinWang,Wenbin
Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. arXiv preprint
| arXiv:2409.12191, | 2024a. |     |     |     |     |
| ----------------- | ------ | --- | --- | --- | --- |
18

Shuai Wang, Ziteng Gao, Chenhui Zhu, Weilin Huang, and Limin Wang. Pixnerd: Pixel neural field diffusion. arXiv
| preprint | arXiv:2507.23268, |     | 2025c. |     |     |     |     |
| -------- | ----------------- | --- | ------ | --- | --- | --- | --- |
WeiyunWang,ZhangweiGao,LixinGu,HengjunPu,LongCui,XingguangWei,ZhaoyangLiu,LinglinJing,Shenglong
Ye, Jie Shao, et al. Internvl3. 5: Advancing open-source multimodal models in versatility, reasoning, and efficiency.
| arXiv preprint | arXiv:2508.18265, |     | 2025d. |     |     |     |     |
| -------------- | ----------------- | --- | ------ | --- | --- | --- | --- |
Xiang Wang, Zhifei Zhang, He Zhang, Zhe Lin, Yuqian Zhou, Qing Liu, Shiwei Zhang, Yijun Li, Shaoteng Liu,
Haitian Zheng, et al. Hbridge: H-shape bridging of heterogeneous experts for unified multimodal understanding and
| generation. | arXiv preprint |     | arXiv:2511.20520, |     | 2025e. |     |     |
| ----------- | -------------- | --- | ----------------- | --- | ------ | --- | --- |
Xinlong Wang, Xiaosong Zhang, Zhengxiong Luo, Quan Sun, Yufeng Cui, Jinsheng Wang, Fan Zhang, Yueze Wang,
Zhen Li, Qiying Yu, et al. Emu3: Next-token prediction is all you need. arXiv preprint arXiv:2409.18869, 2024b.
Zeyu Wang, Zilong Chen, Chenhui Gou, Feng Li, Chaorui Deng, Deyao Zhu, Kunchang Li, Weihao Yu, Haoqin Tu,
Haoqi Fan, et al. Lightfusion: A light-weighted, double fusion framework for unified multimodal understanding and
| generation. | arXiv preprint |     | arXiv:2510.22946, |     | 2025f. |     |     |
| ----------- | -------------- | --- | ----------------- | --- | ------ | --- | --- |
Cong Wei, Zheyang Xiong, Weiming Ren, Xeron Du, Ge Zhang, and Wenhu Chen. Omniedit: Building image
editing generalist models through specialist supervision. In The Thirteenth International Conference on Learning
| Representations, | 2024. |     |     |     |     |     |     |
| ---------------- | ----- | --- | --- | --- | --- | --- | --- |
Cong Wei, Quande Liu, Zixuan Ye, Qiulin Wang, Xintao Wang, Pengfei Wan, Kun Gai, and Wenhu Chen. Univideo:
Unified understanding, generation, and editing for videos. arXiv preprint arXiv:2510.08377, 2025a.
Hongyang Wei, Baixin Xu, Hongbo Liu, Size Wu, Jie Liu, Yi Peng, Peiyu Wang, Zexiang Liu, Jingwen He, Yidan
Xietian, et al. Skywork unipic 2.0: Building kontext model with online rl for unified multimodal model. arXiv
| preprint | arXiv:2509.04548, |     | 2025b. |     |     |     |     |
| -------- | ----------------- | --- | ------ | --- | --- | --- | --- |
Luis Wiedmann, Orr Zohar, Amir Mahla, Xiaohan Wang, Rui Li, Thibaud Frere, Leandro von Werra, Aritra Roy
Gosthipaty, and Andrés Marafioti. Finevision: Open data is all you need. arXiv preprint arXiv:2510.17269, 2025.
Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin, Kaiyuan Gao, Kun Yan, Sheng-ming Yin, Shuai Bai, Xiao Xu,
Yilei Chen, et al. Qwen-image technical report. arXiv preprint arXiv:2508.02324, 2025a.
Chenyuan Wu, Pengfei Zheng, Ruiran Yan, Shitao Xiao, Xin Luo, Yueze Wang, Wanli Li, Xiyan Jiang, Yexin Liu,
Junjie Zhou, et al. Omnigen2: Exploration to advanced multimodal generation. arXiv preprint arXiv:2506.18871,
2025b.
PenghaoWuandSainingXie. V?: Guidedvisualsearchasacoremechanisminmultimodalllms. InProceedings of the
IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 13084–13094, 2024.
Size Wu, Zhonghua Wu, Zerui Gong, Qingyi Tao, Sheng Jin, Qinyue Li, Wei Li, and Chen Change Loy. Openuni: A
simple baseline for unified multimodal understanding and generation. arXiv preprint arXiv:2505.23661, 2025c.
Size Wu, Wenwei Zhang, Lumin Xu, Sheng Jin, Zhonghua Wu, Qingyi Tao, Wentao Liu, Wei Li, and Chen Change
Loy. Harmonizing visual representations for unified multimodal understanding and generation. arXiv preprint
| arXiv:2503.21979, | 2025d. |     |     |     |     |     |     |
| ----------------- | ------ | --- | --- | --- | --- | --- | --- |
Yecheng Wu, Zhuoyang Zhang, Junyu Chen, Haotian Tang, Dacheng Li, Yunhao Fang, Ligeng Zhu, Enze Xie, Hongxu
Yin,LiYi,etal. Vila-u: aunifiedfoundationmodelintegratingvisualunderstandingandgeneration. arXiv preprint
| arXiv:2409.04429, | 2024.           |     |                              |     |     |              |       |
| ----------------- | --------------- | --- | ---------------------------- | --- | --- | ------------ | ----- |
| xAI. Grok-1.5     | vision preview. |     | https://x.ai/news/grok-1.5v. |     |     | Company news | post. |
Shitao Xiao, Yueze Wang, Junjie Zhou, Huaying Yuan, Xingrun Xing, Ruiran Yan, Chaofan Li, Shuting Wang, Tiejun
Huang, and Zheng Liu. Omnigen: Unified image generation. In Proceedings of the Computer Vision and Pattern
| Recognition | Conference, | pages | 13294–13304, | 2025. |     |     |     |
| ----------- | ----------- | ----- | ------------ | ----- | --- | --- | --- |
Ji Xie, Trevor Darrell, Luke Zettlemoyer, and XuDong Wang. Reconstruction alignment improves unified multimodal
| models. | arXiv preprint | arXiv:2509.07295, |     | 2025a. |     |     |     |
| ------- | -------------- | ----------------- | --- | ------ | --- | --- | --- |
Jinheng Xie, Weijia Mao, Zechen Bai, David Junhao Zhang, Weihao Wang, Kevin Qinghong Lin, Yuchao Gu, Zhijie
Chen, Zhenheng Yang, and Mike Zheng Shou. Show-o: One single transformer to unify multimodal understanding
| and generation. | arXiv | preprint | arXiv:2408.12528, |     | 2024. |     |     |
| --------------- | ----- | -------- | ----------------- | --- | ----- | --- | --- |
Jinheng Xie, Zhenheng Yang, and Mike Zheng Shou. Show-o2: Improved native unified multimodal models. arXiv
| preprint | arXiv:2506.15564, |     | 2025b. |     |     |     |     |
| -------- | ----------------- | --- | ------ | --- | --- | --- | --- |
19

Rongchang Xie, Chen Du, Ping Song, and Chang Liu. Muse-vl: Modeling unified vlm through semantic discrete
encoding. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 24135–24146,
2025c.
Yi Xin, Qi Qin, Siqi Luo, Kaiwen Zhu, Juncheng Yan, Yan Tai, Jiayi Lei, Yuewen Cao, Keqi Wang, Yibin Wang,
et al. Lumina-dimoo: An omni diffusion large language model for multi-modal generation and understanding. arXiv
| preprint arXiv:2510.06308, |     |     | 2025. |     |     |     |     |     |
| -------------------------- | --- | --- | ----- | --- | --- | --- | --- | --- |
Weiye Xu, Jiahao Wang, Weiyun Wang, Zhe Chen, Wengang Zhou, Aijun Yang, Lewei Lu, Houqiang Li, Xiaohua
Wang, Xizhou Zhu, et al. Visulogic: A benchmark for evaluating visual reasoning in multi-modal large language
| models. arXiv | preprint | arXiv:2504.15279, |     | 2025. |     |     |     |     |
| ------------- | -------- | ----------------- | --- | ----- | --- | --- | --- | --- |
Jiawei Yang, Tianhong Li, Lijie Fan, Yonglong Tian, and Yue Wang. Latent denoising makes good tokenizers. In The
| Fourteenth | International |     | Conference | on Learning | Representations, |     | 2025a. |     |
| ---------- | ------------- | --- | ---------- | ----------- | ---------------- | --- | ------ | --- |
Ling Yang, Ye Tian, Bowen Li, Xinchen Zhang, Ke Shen, Yunhai Tong, and Mengdi Wang. Mmada: Multimodal large
| diffusion | language | models. | arXiv | preprint arXiv:2505.15809, |     | 2025b. |     |     |
| --------- | -------- | ------- | ----- | -------------------------- | --- | ------ | --- | --- |
Yuhang Yang, Fan Zhang, Huaijin Pi, Shuai Guo, Guowei Xu, Wei Zhai, Yang Cao, and Zheng-Jun Zha. Gloria:
Consistent character video generation via content anchors. arXiv preprint arXiv:2603.29931, 2026.
YangYe,XianyiHe,ZongjianLi,BinLin,ShenghaiYuan,ZhiyuanYan,BohanHou,andLiYuan. Imgedit: Aunified
| image editing | dataset | and | benchmark. | arXiv | preprint | arXiv:2505.20275, |     | 2025. |
| ------------- | ------- | --- | ---------- | ----- | -------- | ----------------- | --- | ----- |
Zebin You, Xiaolu Zhang, Jun Zhou, Chongxuan Li, and Ji-Rong Wen. Llada-o: An effective and length-adaptive
| omni diffusion | model. | arXiv | preprint | arXiv:2603.01068, |     | 2026. |     |     |
| -------------- | ------ | ----- | -------- | ----------------- | --- | ----- | --- | --- |
Sihyun Yu, Sangkyung Kwak, Huiwon Jang, Jongheon Jeong, Jonathan Huang, Jinwoo Shin, and Saining Xie.
Representation alignment for generation: Training diffusion transformers is easier than you think. arXiv preprint
| arXiv:2410.06940, |     | 2024. |     |     |     |     |     |     |
| ----------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
Weihao Yu, Zhengyuan Yang, Linjie Li, Jianfeng Wang, Kevin Lin, Zicheng Liu, Xinchao Wang, and Lijuan Wang.
Mm-vet: Evaluating large multimodal models for integrated capabilities. arXiv preprint arXiv:2308.02490, 2023.
Yongsheng Yu, Wei Xiong, Weili Nie, Yichen Sheng, Shiqiu Liu, and Jiebo Luo. Pixeldit: Pixel diffusion transformers
| for image | generation. | arXiv | preprint | arXiv:2511.20645, |     | 2025. |     |     |
| --------- | ----------- | ----- | -------- | ----------------- | --- | ----- | --- | --- |
Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu Jiang, Weiming
Ren, Yuxuan Sun, et al. Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark
for expert agi. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages
| 9556–9567, | 2024. |     |     |     |     |     |     |     |
| ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
Zhengrong Yue, Haiyu Zhang, Xiangyu Zeng, Boyu Chen, Chenting Wang, Shaobin Zhuang, Lu Dong, KunPeng Du,
Yi Wang, Limin Wang, et al. Uniflow: A unified pixel flow tokenizer for visual understanding and generation. arXiv
| preprint arXiv:2510.10575, |     |     | 2025. |     |     |     |     |     |
| -------------------------- | --- | --- | ----- | --- | --- | --- | --- | --- |
BoqiangZhang,LeiKe,RuihanYang,QiGao,TianyuanQu,RossellChen,DongYu,etal. Penguin-vl: Exploringthe
efficiency limits of vlm with llm-based vision encoders. arXiv preprint arXiv:2603.06569, 2026a.
Huichao Zhang, Liao Qu, Yiheng Liu, Hang Chen, Yangyang Song, Yongsheng Dong, Shikun Sun, Xian Li, Xu Wang,
Yi Jiang, et al. Nextflow: Unified sequential modeling activates multimodal understanding and generation. arXiv
| preprint arXiv:2601.02204, |     |     | 2026b. |     |     |     |     |     |
| -------------------------- | --- | --- | ------ | --- | --- | --- | --- | --- |
Letian Zhang, Sucheng Ren, Yanqing Liu, Xianhang Li, Zeyu Wang, Yuyin Zhou, Huaxiu Yao, Zeyu Zheng, Weili Nie,
Guilin Liu, et al. Openvision 3: A family of unified visual encoder for both understanding and generation. arXiv
| preprint arXiv:2601.15369, |     |     | 2026c. |     |     |     |     |     |
| -------------------------- | --- | --- | ------ | --- | --- | --- | --- | --- |
Yuanhan Zhang, Jinming Wu, Wei Li, Bo Li, Zejun Ma, Ziwei Liu, and Chunyuan Li. Video instruction tuning with
| synthetic | data. arXiv | preprint | arXiv:2410.02713, |     | 2024. |     |     |     |
| --------- | ----------- | -------- | ----------------- | --- | ----- | --- | --- | --- |
BoyangZheng,NanyeMa,ShengbangTong,andSainingXie. Diffusiontransformerswithrepresentationautoencoders.
| arXiv preprint | arXiv:2510.11690, |     |     | 2025. |     |     |     |     |
| -------------- | ----------------- | --- | --- | ----- | --- | --- | --- | --- |
Chunting Zhou, Lili Yu, Arun Babu, Kushal Tirumala, Michihiro Yasunaga, Leonid Shamis, Jacob Kahn, Xuezhe Ma,
Luke Zettlemoyer, and Omer Levy. Transfusion: Predict the next token and diffuse images with one multi-modal
| model. arXiv | preprint | arXiv:2408.11039, |     | 2024. |     |     |     |     |
| ------------ | -------- | ----------------- | --- | ----- | --- | --- | --- | --- |
20

Zijian Zhou, Shikun Liu, Haozhe Liu, Haonan Qiu, Zhaochong An, Weiming Ren, Zhiheng Liu, Xiaoke Huang,
Kam Woh Ng, Tian Xie, et al. Scaling zero-shot reference-to-video generation. arXiv preprint arXiv:2512.06905,
2025.
21