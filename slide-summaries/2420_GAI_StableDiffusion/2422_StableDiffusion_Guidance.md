# 2422_StableDiffusion_Guidance — Per-Slide Summary

**Source file:** `2422_StableDiffusion_Guidance.pptx`
**Source folder:** `SlidesPool/2420_GAI_StableDiffusion/`
**Drive link:** https://drive.google.com/file/d/19YL38t1l-MqYfspr1CJ-ky8yIxKAchET/view
**Slide count (exact, via python-pptx):** 29
**Extraction:** Local parse + slide PNG render. Many code panels and example galleries were inspected visually.

---

## Slide 1 — Guidance for stable diffusion
Title slide that introduces the guidance unit (prompt weighting, classifier-free guidance, negative guidance, SEGA).

## Slide 2 — Prompt Weighting
Section-header slide that opens the prompt-weighting topic.

## Slide 3 — Prompt weighting for image generation
The slide motivates per-token weighting (Dogs++ vs Dogs--) and weighted prompt merging (Dogs * 0.8 + Cats * 0.2). The method multiplies the CLIP text encoder's token embedding vector before cross-attention in the UNet denoiser. The Compel library, integrated with Hugging Face, parses the textual syntax such as "dogs++" and applies the scaling.

## Slide 4 — Compel Lib
The slide shows Compel-library setup: build a Compel object, point it at the right CLIP text encoder (SDXL has two), set `requires_pooling` when pooled embeddings are needed, and pick the embedding source layer ("penultimate" is the layer next to last, often used by SD variants).

## Slide 5 — Generating with Compel
Compel parses the prompt string, scales the embeddings, and feeds them into the diffusion pipeline. Some pipeline operations such as end-of-sequence handling apply only to pooled embeddings.

## Slide 6 — Result
Two panels show example outputs comparing a baseline prompt against a weighted version, illustrating the shift in emphasis Compel produces.

## Slide 7 — CFG: Class-Free Guidance
Section-header slide that introduces classifier-free guidance.

## Slide 8 — Introduction
SD is trained on text-image pairs but sometimes ignores the prompt and reverts to frequent training images. Classifier-free guidance amplifies the influence of the condition relative to the unconditioned (empty-prompt) prediction. To enable this, training drops the conditioning (empty prompt, EOS only) 10% of the time, so the model learns to denoise in both conditional and unconditional modes.

## Slide 9 — Amplify at inference time
At inference time both noise predictions are computed in a single batched pass and combined as `eps_uncond + w * (eps_cond - eps_uncond)`; two visual panels illustrate how higher w pushes generations toward stronger prompt adherence at the cost of fidelity to the data distribution.

## Slide 10 — CFG: Example
Two panels show the same prompt rendered at low and high guidance scale, illustrating the trade-off between sample diversity and prompt fidelity.

## Slide 11 — Stable Diffusion Sampling Loop for class-free guidance
The slide announces a code walkthrough of the CFG-enabled sampling loop, already implemented in the Stable Diffusion pipeline.

## Slide 12 — 1. Setup parameters
A code panel shows initial setup: guidance scale, number of inference steps, prompt encoding.

## Slide 13 — 2. Prepare Text Embedding
The text embeddings for the conditional and unconditional prompts are concatenated along the batch dimension so the UNet evaluates both in one pass.

## Slide 14 — 3. Prepare initial latents and scheduler
A code panel shows preparing the noise latents and the scheduler that determines the noise schedule.

## Slide 15 — 4. Loop through sampling steps with guidance
The denoising loop concatenates the latents along the batch dimension, runs a single UNet forward pass, splits the result, and combines the two predictions with the CFG formula before stepping the scheduler.

## Slide 16 — 5. Decode Resulting Latents to Image
The final latents are decoded by the VAE decoder back to RGB pixels.

## Slide 17 — Negative Guidance/Prompt
Section-header slide that introduces negative prompts as a richer alternative to the empty unconditional prompt.

## Slide 18 — Negative Guidance
Positive guidance steers the noise prediction away from the unconditional ("empty" prompt) toward the positive prompt. With a negative prompt, the model instead steers from the negative prompt toward the positive prompt, so explicit "do not produce X" instructions can be enforced.

## Slide 19 — Example
A code panel and example show that the default empty negative prompt acts as the standard unconditional baseline; replacing it with a textual negative prompt shifts the trade-off accordingly.

## Slide 20 — SEGA: Semantic Guidance
Section-header slide that introduces SEGA (semantic guidance).

## Slide 21 — Motivation
Classifier-free guidance uses a single positive-versus-negative direction. SEGA generalizes this to multiple text prompts (multiple semantic directions) that simultaneously steer the noise prediction.

## Slide 22 — Motivation
The slide draws an analogy to Word2Vec: just as embedding space has meaningful directions, the diffusion latent space (noise) has semantic directions for color, mood, and object presence.

## Slide 23 — Recovering Semantic Direction
At each step, two noise predictions are produced (for example "a man" and "a man with glasses") and their difference vector defines a semantic direction (dimension 4 x 64 x 64). To suppress noise, only the top 1-5% of dimensions by magnitude are kept (others zeroed). The selected direction is added with a negative sign because noise is subtracted during denoising.

## Slide 24 — SEGA
SEGA defines a basis prompt ("A man"), a set of edit prompts ("smiling", "glasses"), and recovers an edit direction for each by predicting noise with and without it. Top-5% "tailing" is applied per direction. The directions are summed and used to adjust the predicted noise.

## Slide 25 — Semantic Guidance
The slide visually summarizes that SEGA composes multiple CLIP text embedding directions, producing a richer multi-axis guidance than CFG.

## Slide 26 — Example with negative prompt
Three panels show SEGA combined with negative prompts to push a generation away from undesired concepts while still adding desired semantic edits.

## Slide 27 — Edit image: Smile
Three panels show the SEGA "smile" direction being added to a base portrait, with progressively stronger smiles.

## Slide 28 — Edit Image: Add Glasses
Two panels demonstrate the SEGA "glasses" direction installing eyewear on the same subject.

## Slide 29 — Edit Image: Multiple Prompts
Two panels show SEGA stacking smile and glasses directions simultaneously, illustrating that multiple semantic edits compose linearly in latent space.

---

## Deck-level takeaway
Guidance is the family of techniques that bend Stable Diffusion's sampling trajectory toward what the user wants. Prompt weighting (Compel) rescales token embeddings before cross-attention. Classifier-free guidance amplifies the conditional-versus-unconditional noise prediction at inference, enabled by 10% conditioning dropout during training. Negative prompts replace the unconditional baseline with an explicit "avoid this" prompt. SEGA generalizes to multiple semantic directions discovered from prompt-pair noise differences, with sparse "tailing" to keep only the strongest dimensions, enabling compositional edits like adding a smile and glasses in a single sampling run.
