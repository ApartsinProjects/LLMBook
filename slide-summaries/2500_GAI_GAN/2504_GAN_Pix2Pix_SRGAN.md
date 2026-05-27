# 2504_GAN_Pix2Pix_SRGAN — Per-Slide Summary

**Source file:** `2504_GAN_Pix2Pix_SRGAN.pptx`
**Source folder:** `SlidesPool/2500_GAI_GAN/`
**Drive link:** https://drive.google.com/file/d/1Fcx3dyJSKO6_tqpNcTSa7Af0E7zpzNal/view
**Slide count (exact, via python-pptx):** 19
**Extraction:** Local parse + slide PNG render. Code-screenshot and example slides were inspected visually.

---

## Slide 1 — Pix2Pix GAN
Title slide with a hero image introducing Pix2Pix as paired image-to-image translation.

## Slide 2 — Generate one image from another
The slide contrasts approaches. In a supervised setting a UNet with pixel-wise loss ignores semantics, focusing on pixels and producing blurry averages. Pix2Pix improves on this by having discriminators separate fakes from reals so the generator's loss combines pixel and adversarial terms. CycleGAN is previewed for the unpaired case.

## Slide 3 — Task
The Pix2Pix example task is reconstructing shoe images from contour-plus-color inputs, with small color circles drawn over the contour to control palette.

## Slide 4 — Dataset
A panel shows the shoe-images dataset that drives the experiment.

## Slide 5 — Prepare: Detect edges and normalize
Five code panels run edge detection on each image and normalize the resulting contour input.

## Slide 6 — Dataset Class
Two code panels implement the PyTorch Dataset returning (edge image plus color hints, ground-truth shoe).

## Slide 7 — Color Coding
Two panels show how color hints are encoded as small painted circles on the edge map.

## Slide 8 — Prepare Data Loaders
A code panel builds train and validation DataLoaders.

## Slide 9 — Weights initialization
A code panel shows the recommended small-Gaussian weight initialization for stable GAN training.

## Slide 10 — UNet backbone blocks for generator
Four code panels define the encoder block, decoder block, with-skip block, and bottleneck block of the UNet generator.

## Slide 11 — UNet-based Generator
Three code panels assemble the UNet generator: encoder downsamples, bottleneck, decoder upsamples with skip connections from the matching encoder level.

## Slide 12 — Discriminator
Two code panels define a PatchGAN discriminator. It is fully convolutional and returns one score per 16x16 patch (for a 512x512 input), evaluating local realism rather than a single global score.

## Slide 13 — Training
Three code panels show the training loop with the combined pixel-plus-adversarial loss.

## Slide 14 — Results
Two panels show source/fake/real triples after 1 and 20 epochs, illustrating the model learning to colorize the contour input.

## Slide 15 — SRGAN
Section-header slide that pivots to Super-Resolution GAN.

## Slide 16 — Super-Resolution
Three panels illustrate super-resolution as smart upscaling that adds plausible details based on what details are usually present.

## Slide 17 — Architecture
SRGAN's generator upscales the low-resolution input and the discriminator distinguishes generated high-resolution images from real high-resolution images.

## Slide 18 — Running model
Five code panels show loading a pretrained SRGAN, preparing low-resolution inputs, and running the upscaling.

## Slide 19 — Results
A panel shows the SRGAN-upscaled output beside the bicubic baseline, with sharper edges and recovered texture.

---

## Deck-level takeaway
Pix2Pix replaces a pixel-wise UNet's blurry reconstructions with a UNet generator plus a PatchGAN discriminator that scores 16x16 patches; combining pixel and adversarial losses produces sharp paired image-to-image translations (here shoe contour-plus-color to color photo). SRGAN applies the same principle to super-resolution, with the discriminator pushing the generator to hallucinate plausible high-frequency detail rather than blurry averages.
