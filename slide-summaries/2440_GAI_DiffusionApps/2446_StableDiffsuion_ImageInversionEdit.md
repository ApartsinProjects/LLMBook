# 2446_StableDiffsuion_ImageInversionEdit — Per-Slide Summary

**Source file:** `2446_StableDiffsuion_ImageInversionEdit.pptx`
**Source folder:** `SlidesPool/2440_GAI_DiffusionApps/`
**Drive link:** https://drive.google.com/file/d/1rJvSQt2RZNYLuL3tyxVTcIzONide9nsV/view
**Slide count (exact, via python-pptx):** 10
**Extraction:** Local parse + slide PNG render. Several slides (1, 4, 6, 7, 8, 9, 10) carry their content only as figures or formulas and were visually inspected.

---

## Slide 1 — DDIMP Inversion
Title slide that introduces DDIM-style inversion as the tool for editing real images with Stable Diffusion.

## Slide 2 — Strategies for injecting controls to SD
The slide enumerates the control surfaces for Stable Diffusion. Prompts steer generation through cross-attention with text tokens, with guidance adjusting the direction relative to the empty prompt. Images can be injected by starting from their latents and tuning the control strength. Editing methods such as ControlNet adjust hidden-layer activations from auxiliary controls, while Prompt2Prompt edits attention maps directly.

## Slide 3 — Image Inversion
Image inversion is defined as the problem of finding a noisy latent that, when denoised, reproduces a target image. The found latent can then be denoised under a slightly altered prompt to perform image editing.

## Slide 4 — Task: Image Editing with text prompts
The slide shows the desired interface: an input image plus a text instruction yields an edited image that preserves the unedited regions and respects the user prompt.

## Slide 5 — Image Inversion with DDIM
The slide walks through the deterministic DDIM forward and backward processes, showing the equations that let one recover x_t (the noisy latent) from a clean image. The trick is to use the diffusion model's noise-to-clean direction in reverse: instead of stepping backward in time, step forward by adding the predicted noise back into the current latent.

## Slide 6 — LEDITS++
Section-header slide that introduces LEDITS++ as a more recent inversion-based editing method.

## Slide 7 — Reminder: SAGA
The slide visually recaps SAGA-style semantic guidance, showing how additional gradient terms can steer denoising toward or away from concepts during sampling.

## Slide 8 — Combine inversion and SAGA guidance
The slide illustrates that LEDITS++ combines DDIM inversion (to lock onto the source image) with SAGA-style guidance (to add or remove concepts), enabling text-driven edits without retraining.

## Slide 9 — Example: Glass Removal
A worked example shows an input portrait whose eyeglasses are removed by the inversion-plus-guidance pipeline, while hair, skin, and background remain visually identical.

## Slide 10 — Example
A final gallery panel demonstrates another edit, confirming that the method preserves identity and layout while applying the requested semantic change.

---

## Deck-level takeaway
Editing real photos with Stable Diffusion requires first inverting them: DDIM inversion deterministically recovers the latent trajectory that produced the image. Once the latent is in hand, semantic guidance such as SAGA (and its LEDITS++ refinement) can push denoising toward or away from target concepts, yielding text-driven local edits that preserve unrelated content.
