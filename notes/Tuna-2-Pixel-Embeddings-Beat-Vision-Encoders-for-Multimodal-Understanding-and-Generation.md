# Tuna-2: Pixel Embeddings Beat Vision Encoders for Multimodal Understanding and Generation

## Metadata

- Authors: Zhiheng Liu, Weiming Ren, Xiaoke Huang, Shoufa Chen, Tianhong Li, Mengzhao Chen, Yatai Ji, Sen He, Jonas Schult, Belinda Zeng, Tao Xiang, Wenhu Chen, Ping Luo, Luke Zettlemoyer, Yuren Cong
- Venue/Year: arXiv, 2026
- Source: https://arxiv.org/pdf/2604.24763
- arXiv: 2604.24763v2, revised 2026-05-18
- Project page: https://tuna-ai.org/tuna-2/
- Code: https://github.com/facebookresearch/tuna-2
- Local PDF: [../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.pdf](../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.pdf)
- Converted Markdown: [../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.md](../papers/Tuna-2-Pixel-Embeddings-Beat-Vision-Encoders-for-Multimodal-Understanding-and-Generation.md)

## Research Question

Tuna-2 asks whether a unified multimodal model really needs pretrained vision encoders or VAE latents. The paper tests whether visual understanding, text-to-image generation, and image editing can be learned directly from pixel embeddings in one end-to-end transformer-style system.

The robotics-relevant version of the question is: can a model learn visual representations with enough fine-grained pixel detail for perception and generation without inheriting the resolution limits and semantic biases of a fixed visual encoder?

## Core Method

Tuna-2 progressively removes visual encoding modules from the earlier Tuna architecture. Tuna-R removes the VAE but keeps a SigLIP 2 representation encoder. Tuna-2 removes the representation encoder as well and replaces it with simple patch embedding layers that turn raw image pixels into tokens for a Qwen2.5-7B-Instruct decoder.

For image generation, the model does not use latent diffusion. It applies pixel-space rectified flow with an x-prediction objective and a v-loss, predicting clean image pixels from noisy pixel inputs conditioned on text or image-plus-text prompts. The same model supports multimodal understanding through the language modeling head.

Training has two main stages. Stage 1 does full-model pretraining on image captioning and text-to-image generation, using 550M in-house image-text pairs plus text-only data. Stage 2 performs supervised fine-tuning on image instruction following, image editing, and high-quality image generation data. Tuna-2 also uses masking-based visual feature learning in the later part of pretraining: some image patches are replaced by a learned mask token, making generation harder and forcing understanding to work under partial visual evidence.

## Key Innovation

- Encoder-free unified multimodal modeling: raw image patches go directly into the decoder instead of passing through a pretrained vision encoder.
- VAE-free pixel-space generation: text-to-image and editing are handled by pixel-space flow matching rather than latent diffusion.
- Controlled comparison with Tuna-R, isolating the tradeoff between representation encoders and pure pixel embeddings.
- Masking-based feature learning that regularizes both generation and understanding.
- Evidence that encoder-free pixel-space training can surpass encoder-based designs on fine-grained visual understanding after enough pretraining.

## Problems Solved

Tuna-2 targets the representation mismatch in unified multimodal models. Many systems use one representation for visual understanding and another for generation, or depend on pretrained encoders whose priors may hide low-level details. Tuna-2 simplifies this into one pixel-space representation and one end-to-end training path.

It also addresses fine-grained perception. Fixed vision encoders can compress away small objects, text details, local geometry, or unusual visual cues. Tuna-2's pixel embeddings preserve more direct access to these details, which helps on perception-heavy benchmarks and attention visualizations.

## Experiments

On multimodal understanding, Tuna-2 is competitive with or stronger than 7B-scale native unified multimodal models. It reports GQA 65.0, RealWorldQA 67.7, MMVet 51.7, MMMU 50.7, MMVP 77.3, OCRBench 79.7, V* 59.2, CountBench 81.7, and VisuLogic 28.8. The important result is not just the absolute score but the pattern: Tuna-2 usually beats Tuna-R on understanding after sufficient pretraining, especially on pixel-centric tasks.

On image generation, Tuna-2 remains competitive but Tuna-R is often slightly stronger. Tuna-2 reports GenEval overall 0.87 and DPG-Bench overall 86.54. This suggests representation encoders still provide useful semantic priors for generation, although the gap narrows with scale and SFT.

For image editing, Tuna-2 beats earlier unified baselines such as OmniGen, BAGEL, UniWorld, and OmniGen2, but remains behind Tuna and Tuna-R. Reconstruction experiments show Tuna-2 can reconstruct ImageNet images strongly for a unified tokenizer, with rFID 0.15, PSNR 32.80, and SSIM 0.93 at 512 resolution.

The ablations are practically useful. A 7:3 generation-to-understanding data ratio gives the best tradeoff. Masking improves both Tuna-R and Tuna-2, with Tuna-2 benefiting more. Training curves show Tuna-R learns faster early because its pretrained encoder gives semantic priors, but Tuna-2 catches up and surpasses it on understanding at larger scale.

## Limitations

Tuna-2 is extremely expensive to train. The reported 7B setup uses 550M in-house image-text pairs, 64 nodes, 300k pretraining steps, and 16k sequence length per GPU, then another 50k SFT steps. This is not a small-lab recipe.

The paper's strongest claims are about images, not real robot video, 3D state, temporal consistency, action prediction, or closed-loop control. For robotics, Tuna-2 is best viewed as a perception and generative representation idea, not a ready robot policy.

The encoder-free design improves understanding at scale but does not dominate every task. Tuna-R remains slightly better on several generation and editing metrics, showing that pretrained visual priors still help. The official code is public, but the project page notes that full production-trained weights are not released due to policy constraints.

## Practical Robotics Impact

Tuna-2 is relevant to robotics because many robot failures come from missing fine visual details: small object pose changes, thin handles, cable geometry, transparent objects, text labels, tool tips, contact boundaries, and occluded parts. A pixel-space representation may preserve signals that a generic VLM encoder compresses away.

It also suggests a useful direction for robot world models. Instead of generating future frames through a VAE latent that may lose contact-level detail, a narrow robot model could use pixel-space flow matching for short-horizon future-image prediction or image-conditioned editing, then pair it with a value or action model.

## Application to My Robot

For my robot, I would not try to train Tuna-2 from scratch. The realistic adaptation is to borrow the design principles:

- use raw-patch or high-resolution crop tokens for manipulation-critical regions such as grippers, object contacts, labels, and small target parts;
- keep a VLM encoder for global scene understanding, but add a pixel-space branch for fine local perception;
- train masked visual prediction on robot camera frames so the model learns robust local features under occlusion;
- use pixel-space future prediction for short horizons where contact detail matters more than long-term realism;
- evaluate on robot-specific perception tasks, such as counting small objects, reading labels, localizing handles, detecting whether a gripper is actually touching an object, and recognizing near-failure states.

Required sensors are standard RGB cameras, ideally with wrist and static views. Depth is not required by Tuna-2, but for a robot I would keep depth or tactile data as independent supervision because pixel-space image modeling alone does not guarantee physical correctness.

Expected benefit: better fine-grained perception and more faithful visual imagination around contact-rich manipulation. Main risks: high compute cost, unstable training in pixel space, weak temporal consistency if applied frame by frame, and the possibility that visual detail improves without improving action selection.

## Implementation Notes

A practical first experiment is a small masked pixel-prediction model on wrist-camera crops. Train it to reconstruct masked patches and predict short-horizon future crops from action-conditioned observations. Compare the learned features against a standard VLM encoder on contact-state classifiers and small-object localization before using them in a policy.
