# 2448_StableDiffusion_Superresolution — Per-Slide Summary

**Source file:** `2448_StableDiffusion_Superresolution.pptx`
**Source folder:** `SlidesPool/2440_GAI_DiffusionApps/`
**Drive link:** https://drive.google.com/file/d/10MMgjIsQ9jzNUhHPY3Vm-DLvLqNaAaGf/view
**Slide count (exact, via python-pptx):** 15
**Extraction:** Local parse + slide PNG render. Many gallery and example slides were inspected visually.

---

## Slide 1 — Image Super-Resolution
Title slide introducing diffusion-based image super-resolution.

## Slide 2 — Background: Image upscaling
The slide contrasts two upscaling regimes. Classical interpolation (nearest neighbor, bicubic) fills missing values from neighbors. Super-resolution, by contrast, predicts plausible high-frequency details using a learned prior, yielding high quality when those guesses are correct.

## Slide 3 — Generate Small Image: 256x256
Three example panels show base 256x256 outputs from Stable Diffusion that will be upscaled in the following slides.

## Slide 4 — Background: Image Interpolation
A schematic shows how interpolation kernels fill missing pixels between known samples in a small image.

## Slide 5 — Background: Lanczos Interpolation
The slide describes Lanczos interpolation as convolution with the central lobe of the sinc function. Multiple panels illustrate the kernel shape and the resulting interpolated image.

## Slide 6 — Upscale by Interpolation
The slide shows the same 256x256 image upscaled by Lanczos to 768x768. The result is smoother but lacks fine texture detail, motivating learning-based super-resolution.

## Slide 7 — Upscale by image-to-image
The slide describes a diffusion-based super-resolution recipe. Start from the interpolated 768x768 image, run Stable Diffusion's image-to-image pipeline with a "super-resolution" prompt at low strength (about 0.3 of 80 timesteps). Because SD is trained at 512x512 (or SDXL at 1024x1024), inputs and outputs are resized to match. Diffusion adds plausible detail without altering global structure.

## Slide 8 — (untitled)
A two-panel comparison shows the interpolated baseline against the SD-refined output, with the diffusion version recovering texture and edge sharpness.

## Slide 9 — Results
Three side-by-side galleries illustrate the recovered detail across different image types.

## Slide 10 — ControlNet Tile
Section-header slide that introduces ControlNet Tile as a structure-preserving super-resolution backbone.

## Slide 11 — Reminder: ControlNet
A schematic reminder of ControlNet: a parallel encoder branch injects per-block deltas into the frozen SD UNet, conditioned on an auxiliary signal.

## Slide 12 — ControlNet Tile
The slide explains tile-based ControlNet super-resolution. The VAE decoder and the SD denoiser are fully convolutional and accept arbitrarily large latents, but SD was trained at 64x64 latents and cannot invent new global structure at larger scales. ControlNet Tile sidesteps the issue by feeding the low-resolution image to ControlNet as a constraint, so SD does not have to invent new structure; tiles are processed with strided convolutions to cover the full image.

## Slide 13 — Example
The slide shows four side-by-side outputs comparing baseline upscaling against ControlNet Tile super-resolution.

## Slide 14 — Upscale
The slide demonstrates ControlNet Tile pushing a small image to a much larger resolution while preserving fine structure and global layout.

## Slide 15 — Results
A final gallery panel reports results across diverse content, with sharp, plausible high-frequency detail.

---

## Deck-level takeaway
Diffusion-based super-resolution uses a two-stage recipe: interpolate the image to the target size, then run SD or SDXL image-to-image at low strength to hallucinate plausible detail. ControlNet Tile extends this to arbitrarily large outputs by feeding the low-resolution image as a structural constraint and processing tiles convolutionally, so the model adds detail without inventing new global structure.
