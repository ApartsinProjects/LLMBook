# 2442_StableDiffusion_DepthNet — Per-Slide Summary

**Source file:** `2442_StableDiffusion_DepthNet.pptx`
**Source folder:** `SlidesPool/2440_GAI_DiffusionApps/`
**Drive link:** https://drive.google.com/file/d/1QonOyp7sQ_Wyae6CCetbDYYZr4zyXKny/view
**Slide count (exact, via python-pptx):** 5
**Extraction:** Local parse + slide PNG render. Body text captured the depth-conditioning recipe; example and results slides were visually inspected.

---

## Slide 1 — DepthNet
Title slide introducing depth-conditioned Stable Diffusion (DepthNet variant).

## Slide 2 — Depth-based generation
The slide describes how to keep a subject's geometry while changing its appearance. A depth map is supplied as an additional fifth input channel to the UNet, and the denoiser is trained to interpret both depth and text when predicting noise. The training set consists of (image, text) pairs with depth maps computed offline using MiDaS.

## Slide 3 — Example
The slide shows a source image together with its MiDaS depth estimate to illustrate the depth-channel input that DepthNet consumes alongside the prompt.

## Slide 4 — Results
A gallery shows the same depth structure regenerated under multiple prompts; the subject layout is preserved across stylistic variations driven by the text condition.

## Slide 5 — Object Replacement
A final example demonstrates that the depth map locks the object's silhouette so the prompt can swap the object class (or appearance) while keeping spatial composition intact.

---

## Deck-level takeaway
DepthNet conditions Stable Diffusion on a precomputed MiDaS depth map injected as an extra UNet channel. This lets prompts re-skin or replace a subject while preserving its 3D layout, providing a lightweight form of structural control without needing per-prompt segmentation masks.
