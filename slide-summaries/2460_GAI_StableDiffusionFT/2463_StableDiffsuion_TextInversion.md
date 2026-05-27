# 2463_StableDiffsuion_TextInversion — Per-Slide Summary

**Source file:** `2463_StableDiffsuion_TextInversion.pptx`
**Source folder:** `SlidesPool/2460_GAI_StableDiffusionFT/`
**Drive link:** https://drive.google.com/file/d/1zTQzD_gxmmMjJx4Ikc_LUUT0XDZwn-xI/view
**Slide count (exact, via python-pptx):** 7
**Extraction:** Local parse + slide PNG render. Body text covered the method; the comparison and library slides were visually inspected.

---

## Slide 1 — Textual Inversion
Title slide announcing Textual Inversion as a lightweight personalization technique for Stable Diffusion.

## Slide 2 — Textual Embedding
The slide describes the core idea: introduce a new placeholder token (S*) for the target concept or object and train only its 768-dimensional embedding vector using a small set of 3-20 image-prompt pairs. The denoiser and the text encoder stay frozen; the new embedding is passed through the existing frozen encoder. At inference time, prompts that include S* invoke the learned concept.

## Slide 3 — Midjourney-Style Images
The slide motivates the method with a worked example: Midjourney's signature cinematic, stylized, dramatically lit aesthetic comes from training on digital art. The goal is to capture that style with a single learned token rather than retraining a base model.

## Slide 4 — Generate image with SD (no Midjourney-style)
The slide shows three baseline Stable Diffusion outputs from a chosen prompt, demonstrating the model's default look without any style token.

## Slide 5 — Same prompt with Midjourney text inversion
The slide shows three outputs from the same prompt augmented with a Midjourney-style inversion token, making the change in lighting, color palette, and composition immediately visible.

## Slide 6 — SD Concepts Library
The slide presents Hugging Face's SD Concepts Library, a community catalog of pretrained textual-inversion embeddings that users can load on demand to summon styles, objects, or characters.

## Slide 7 — Training Textual Inversion
Practical guidance on dataset size is given: 3-5 images for a simple object, 10-20 images for styles or complex objects, and 30+ images for abstract styles with significant variability. The new embedding is initialized from an existing token to speed convergence.

---

## Deck-level takeaway
Textual Inversion personalizes Stable Diffusion by learning a single new 768-dimensional token embedding from a handful of images while keeping the UNet and text encoder frozen. The result is a tiny, portable checkpoint, exchangeable through resources like the SD Concepts Library, that adds new styles or objects to any prompt without retraining the base model.
