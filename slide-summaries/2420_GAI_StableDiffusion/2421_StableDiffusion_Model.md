# 2421_StableDiffusion_Model — Per-Slide Summary

**Source file:** `2421_StableDiffusion_Model.pptx`
**Source folder:** `SlidesPool/2420_GAI_StableDiffusion/`
**Drive link:** https://drive.google.com/file/d/1v3WQhYH1tExBeV_gtELSlCmHE6DS3eJN/view
**Slide count (exact, via python-pptx):** 40
**Extraction:** Local parse + slide PNG render. Reminder slides without body text and section-header slides were inspected visually.

---

## Slide 1 — Stable Diffusion
Title slide that opens the technical anatomy of Stable Diffusion.

## Slide 2 — Reminder: Diffusion Model
The slide recaps the gradual denoising process: many iterations of denoising a full-size image until clean output emerges from pure noise.

## Slide 3 — Reminder: Denoiser Model
A two-panel schematic recaps the denoiser as a network that predicts the noise added at the current timestep, given the noisy image and the timestep embedding.

## Slide 4 — Reminder: VAE and Latent Space
The slide recaps a VAE encoder mapping images to a compact latent and a decoder reconstructing pixels back from those latents.

## Slide 5 — Reminder CLIP Model
The slide recaps CLIP as a contrastive image-text model that produces aligned image and text embeddings in a shared space.

## Slide 6 — Latent Diffusion Model
Latent diffusion runs the diffusion process in the VAE latent space rather than pixel space. Training pairs an image (encoded by VAE) with prompt tokens (encoded by CLIP); noise is added in latent space and the denoiser is trained for conditional denoising. Sampling traces a trajectory through latent space before the VAE decoder reconstructs pixels.

## Slide 7 — Pretraining SD Denoiser model
The slide diagrams the SD denoiser pretraining loop: sample timestep, add noise to the latent, predict noise conditioned on CLIP text embeddings, optimize MSE.

## Slide 8 — Reminder: Cross-Attention
The slide recaps cross-attention, where queries from one source attend to keys and values from another, used by SD to inject prompt information into the denoiser.

## Slide 9 — Latent Pixels-to-Tokens Cross Attention
A schematic shows latent-pixel queries attending to CLIP token keys and values inside the UNet, the mechanism by which text guides denoising.

## Slide 10 — Stable Diffusion: Text Conditioning
SD is the latent diffusion model in its text-to-image form. Sampling starts from a random latent and the UNet denoiser is conditioned on the encoded prompt; conditioning is injected via cross-attention.

## Slide 11 — SD: Image-to-image
Image-to-image extends text-conditioning by additionally starting from an encoded reference image rather than pure noise. A strength parameter (0 to 1) controls how much noise is added to that latent before denoising; 0 leaves the image untouched and 1 starts from near-pure noise.

## Slide 12 — Stable Diffusion: Image-to-Image
A schematic shows the workflow: encode the reference image with VAE, add noise to its latent, then conditioned denoising transforms the noisy latent toward a representation matching the new prompt.

## Slide 13 — Image conditioning: Example
A worked example with 80 reverse-diffusion steps shows that strength=0.2 yields 16 actual denoising steps starting close to the original (output similar to input), while strength=0.8 yields 64 steps starting near pure noise (output very different from input).

## Slide 14 — VAE Image Encoding
Section-header slide that transitions into the SD VAE in detail.

## Slide 15 — VAE Training objective
The slide motivates moving away from conventional MSE reconstruction loss: shifting an image by one pixel produces a large MSE but is perceptually identical. The fix is to train the VAE with a perceptual reconstruction loss.

## Slide 16 — LPIPS Loss: Overview
LPIPS uses a pretrained CNN (AlexNet, ResNet) as a feature extractor. The assumption is that perceptually similar images produce similar intermediate feature maps, so the loss compares features rather than pixels.

## Slide 17 — LPIPS: Learned Perceptual Image Patch Similarity
The slide walks through the LPIPS algorithm: pass reconstructed and ground-truth images through a frozen VGG-like network, extract feature maps at several layers, normalize channel-wise, compute per-location feature distances, weight channels with learned weights calibrated to human perceptual judgments, average spatially per layer, and sum across layers.

## Slide 18 — LPIPS
LPIPS is trained on a patch-similarity dataset of triplets (an original patch and two distorted ones) with a contrastive classification objective that learns which distortion is closer to the original.

## Slide 19 — LPIPS as a loss
A code panel shows LPIPS used as a training loss for the SD VAE by back-propagating through the frozen VGG backbone.

## Slide 20 — Encoding with SD VAE
The SD VAE is trained separately from the diffusion model. Input is 512x512x3, latent is 64x64x4. Loss is L1 plus LPIPS. The latent representation is scaled so variance equals 1 (calibrated on the training data) for stable diffusion training and unscaled before decoding.

## Slide 21 — Latent Image Encoding
The slide notes that the latent encoding does not necessarily preserve the original image structure; two panels show that two visually similar images can produce different latent maps.

## Slide 22 — Text Encoder
Section-header slide that transitions to the SD text encoder.

## Slide 23 — Reminder: Clip Model
A schematic again recaps CLIP and the text encoder branch SD uses.

## Slide 24 — Text(Prompt) Encoder in Stable Diffusion
SD uses a frozen pretrained text encoder from CLIP (BERT-like). SDv1 produces 77 token embeddings of 768 dimensions; SDv2 uses 77 tokens of 1024 dimensions.

## Slide 25 — Applying SD Text Encoder
Two code panels show invoking the tokenizer and text encoder to produce the per-token embedding tensor that feeds the denoiser.

## Slide 26 — Conditional Denoising Model
Section-header slide that transitions to the UNet-based conditional denoiser.

## Slide 27 — Conditioned UNet model
The slide describes the conditioning pipeline: CLIP encoder produces 1024-dim token embeddings (OpenClip) or 768-dim (Clip), shaped (77, dim) and consumed by cross-attention layers in the UNet.

## Slide 28 — UNet conditioned on time and text embedding
Two schematics show the UNet receiving both a timestep embedding and a text embedding; the time embedding modulates each block while the text embedding enters via cross-attention.

## Slide 29 — UNet blocks: Transformer + ResNet + Down/Up-sample
The slide diagrams UNet blocks composed of ResNet stages, transformer attention, and down/up-sampling. Time and condition embeddings are fed via cross-attention with pixel features acting as queries.

## Slide 30 — Diffusion Transformer
Section-header slide that introduces the Diffusion Transformer (DiT) variant.

## Slide 31 — Reminder: Vision Transformer
A schematic recaps the Vision Transformer architecture that DiT builds upon.

## Slide 32 — Diffusion Transformer
DiT replaces the UNet with a pure transformer. Its conditional mechanism is Adaptive Layer Norm (AdaLN), which uses the conditioning vector to predict per-block scale and shift parameters.

## Slide 33 — Example: Class Conditioned Transformer
The slide shows a DiT trained on ImageNet, conditioned on class labels, as the canonical proof-of-concept for the transformer-only diffusion architecture.

## Slide 34 — Stable Diffusion Versions
Section-header slide previewing SDXL and DALL-E 3.

## Slide 35 — Stable Diffusion XL
SDXL has 2.6B parameters (versus 860M for SD). It is trained on multiple resolutions and aspect ratios and uses two text encoders: 77 1024-dim per-token embeddings concatenated, plus a single 1280-dim pooled global prompt embedding. Per-token embeddings handle objects and attributes; the global embedding handles style and composition. Optional conditions include image prompts and target size/aspect ratio. Image-prompt VAE encoding starts from latents of size (H/8, W/8, 4).

## Slide 36 — Different method for Image Prompting
SD and SDXL encode the image prompt as the starting latent representation, controlling the reverse-diffusion starting point. DALL-E v2 instead starts from random noise, embeds the image, and conditions via FiLM (feature-wise linear modulation).

## Slide 37 — Better Text Encoding
CLIP is trained for image-text similarity, not for visual-content prediction. DALL-E v2 adds an explicit prior model fine-tuned to predict image embeddings from text embeddings, which improves prompt fidelity.

## Slide 38 — OpenAI Interface
Section-header slide that transitions to OpenAI's image generation API.

## Slide 39 — Image Generation with OpenAI
A code panel shows invoking the OpenAI image generation API (`openai.images.generate`) with a text prompt.

## Slide 40 — DALL-E 3: OpenAI interface
Two panels show DALL-E 3 outputs generated through the OpenAI API, contrasting with the open-source SD examples earlier in the deck.

---

## Deck-level takeaway
Stable Diffusion is a latent diffusion model: a VAE compresses pixels to a 64x64x4 latent, CLIP encodes the text prompt to 77 token embeddings, and a UNet denoiser is trained to remove noise from latents while attending to text via cross-attention. The deck walks through every piece (latent diffusion concept, VAE with LPIPS perceptual loss, CLIP text encoder, conditioned UNet with time and text embeddings, and the newer Diffusion Transformer variant), then situates SDXL (larger model, dual text encoder, additional spatial conditions) and DALL-E (different prompt-conditioning style, separate prior model) within the same framework.
