# 2505_GAN_Cycle_Style — Per-Slide Summary

**Source file:** `2505_GAN_Cycle_Style.pptx`
**Source folder:** `SlidesPool/2500_GAI_GAN/`
**Drive link:** https://drive.google.com/file/d/1RU9ewMyBVSV-80B3iFKXtt29JxU7D5Md/view
**Slide count (exact, via python-pptx):** 53
**Extraction:** Local parse + slide PNG render. Long deck so paragraphs are kept concise; code, schematic, and result slides were inspected visually as needed.

---

## Slide 1 — CycelGAN
Title slide for CycleGAN and StyleGAN.

## Slide 2 — CycleGAN
CycleGAN tackles image-to-image translation without paired training data. Paired data is hard to obtain (add/remove glasses, blond/black hair, winter/summer, photo/painting); CycleGAN takes two unpaired image sets and learns to translate between them.

## Slide 3 — CycleGAN Architecture
Two generators and two critics: G1 maps black hair to blond, G2 the reverse, with discriminators D1 (real vs fake blond) and D2 (real vs fake black). Generators consume source images rather than latent noise.

## Slide 4 — Cycle Consistency Loss
The cycle consistency loss requires the fake blond image to retain enough information to reconstruct the original black-hair input via the reverse generator. The total loss has two parts: adversarial fidelity (fakes indistinguishable from reals) plus cycle consistency.

## Slide 5 — Combine Losses
A schematic combines the adversarial losses for both directions with both cycle losses.

## Slide 6 — Components
The slide lists components: Gen_AB and Gen_BA generators plus D_A and D_B discriminators.

## Slide 7 — All Losses: A and B classes
The training objective is the sum of adversarial losses (average BCE between real and fake for each class), cycle losses (GenAB(GenBA(B))=B and GenBA(GenAB(A))=A), and an optional identity loss (GenAB(A)=A and GenBA(B)=B).

## Slide 8 — Fruits Style(Attribute) Transfer
Section-header slide for the apple-to-orange example.

## Slide 9 — Task
The task is to swap apple and orange texture while keeping shape, using two image sets.

## Slide 10 — Dataset Class
Three code panels show a Dataset that pairs each apple with a randomly sampled orange via `glob`.

## Slide 11 — Weights Initialization
A code panel applies the standard small-Gaussian initialization.

## Slide 12 — Generator architecture
A panel diagrams the CycleGAN generator built from convolutions, residual blocks, and transposed convolutions.

## Slide 13 — Residual Block for generator
Two code panels define the residual block (conv-norm-relu-conv-norm with skip connection).

## Slide 14 — Generator
Two code panels assemble the generator from the residual blocks.

## Slide 15 — Discriminator
A code panel defines a PatchGAN-style discriminator returning a 16x16 score map; ground-truth labels for the real class are all-ones patch maps.

## Slide 16 — Generator Training
Two code panels show the generator's combined adversarial-plus-cycle loss and optimization step.

## Slide 17 — Generation
A code panel shows running inference (apple to orange and back).

## Slide 18 — Discriminator Training
Two code panels show the per-discriminator update with the 16x16 logit output.

## Slide 19 — Training
Two code panels show the overall epoch loop running both directions.

## Slide 20 — Results
A panel shows apple-to-orange-to-apple round-trip outputs after training.

## Slide 21 — Face Image Editing
Section-header slide pivoting to facial attribute editing.

## Slide 22 — Celebrities face dataset: Kaggle
The CelebA-style dataset has 200K images with hair-color attributes.

## Slide 23 — Splitting into blond/black hair partitions
Two code panels split the dataset along the hair-color label.

## Slide 24 — Dataset Class returns black/blond hair pair
A code panel returns paired samples (one black, one blond) per iteration.

## Slide 25 — Prepare augmentation transforms and DataLoader
A code panel uses Albumentations to apply a rich set of augmentations.

## Slide 26 — Background: Mirror padding
Mirror padding produces smoother transitions and avoids the artificial zero-edge artifacts of zero padding.

## Slide 27 — Create two discriminators
Two code panels instantiate the two PatchGAN discriminators.

## Slide 28 — Generator Blocks
Three code panels define down, residual, and up blocks for the face generator.

## Slide 29 — Two Generators
Three code panels assemble both generators (black to blond and blond to black).

## Slide 30 — Background: Automatic Mixed Precision
PyTorch defaults to float32 but its AMP package automatically uses float16 where safe, accelerating training.

## Slide 31 — Training
Five code panels run the full training loop with AMP.

## Slide 32 — Round-trip Conversion
Two panels show that a black-haired face mapped to blond and back recovers the original.

## Slide 33 — Results
Two panels show high-quality blond and black hair conversions.

## Slide 34 — Style GAN
A hero image introduces StyleGAN.

## Slide 35 — ProgressiveGAN: Large image generation with GAN
Plain GANs struggle beyond 64x64 and often collapse. ProgressiveGAN starts with small 4x4 generators and discriminators and progressively adds layers (8x8, 16x16, etc.) without freezing earlier layers.

## Slide 36 — StyleGAN
StyleGAN injects noise at multiple levels rather than once. A learned mapping network disentangles the noise into per-layer style codes that control different aspects: coarse (pose, face shape), middle (hairstyle), fine (colors, microstructure). Two noise types are used: A-noise injected via AdaIN for style attributes and B-noise added per-pixel for stochastic variations.

## Slide 37 — Noise Entanglement
Because noise dimensions and attributes are entangled at training time, the user only discovers control axes by post-hoc mixing and matching across images.

## Slide 38 — AdaIN: Adaptive Instance Normalization
AdaIN normalizes the previous-layer feature map and then scales and biases it with style parameters y derived by passing the latent W through a per-target-layer linear projection.

## Slide 39 — Image Generator Recipe
The full recipe samples a 512-dim noise z, maps it through the mapping network to W, samples regularization noise B, and runs the 18-layer generator: at each layer add B to the feature map, compute per-layer style scale and bias from W, and apply AdaIN.

## Slide 40 — Latent Space Extension
The extended StyleGAN (W+ space) produces a different latent vector W per layer rather than sharing one W across all layers, giving finer-grained control.

## Slide 41 — Style Transfer
Section-header slide that introduces style transfer using StyleGAN.

## Slide 42 — Inversion: Extracting Latent from real Image
Inversion freezes a trained StyleGAN, generates an image from a candidate (z, B), measures the difference to the target real image, and back-propagates to update W. Regeneration with the recovered W and a fresh B yields a similar identity with different microstructure.

## Slide 43 — Style Transfer Recipe
Early-layer noise controls coarse attributes (pose, face shape, orientation); middle layers control hairstyle and facial features; late layers control fine details.

## Slide 44 — Style Transfer Recipe
The transfer recipe inverts both target and style images. The composite latent uses layers 0-3 from the target (coarse identity) and layers 8-17 from the style image (fine style), with different W for affine transforms, and regenerates the composite.

## Slide 45 — Layer Effect
A GIF illustrates how editing each layer changes a different aspect of the generated face.

## Slide 46 — Transferring Styles
Two panels show real target images and generated outputs that adopt the style of a randomly sampled 512-noise vector.

## Slide 47 — Truncation of random latent vectors
Truncation pulls random W vectors toward the mean inverted vector, avoiding weird-corner artifacts at the cost of diversity.

## Slide 48 — Generated Image from random latent vector
Two panels show images generated from sampled latent vectors before and after truncation.

## Slide 49 — Generate latent vector from real image
Four panels show the inversion procedure that recovers a W from a real image.

## Slide 50 — Style Transfer
An extension that maintains a 18x512 latent matrix (one row per layer) supports row-wise swapping between images for targeted style transfer.

## Slide 51 — High-level feature transfer
Swapping high-level latent rows (layers 0-3) produces age swaps and other coarse attribute changes.

## Slide 52 — Results
Two panels show that swapping layers 15-18 changes almost nothing, while swapping layers 4-15 swaps color and background.

## Slide 53 — Extract specific style: Smile
To isolate a "smile" direction, generate many synthetic images, invert them to latent codes, manually label smile/no-smile, fit a linear SVM, and take the hyperplane normal as the smile direction in W. To modify a real image's smile, invert it and step along that direction.

---

## Deck-level takeaway
The deck unifies two unpaired-translation breakthroughs. CycleGAN uses two generators and two discriminators tied together by a cycle-consistency loss to translate between unpaired domains (apples to oranges, blond to black hair). StyleGAN reorganizes the GAN generator around a style hierarchy: a mapping network projects noise into per-layer style codes injected via AdaIN, with coarse, middle, and fine layers controlling distinct visual attributes. Inversion plus per-layer style mixing enables principled style transfer, attribute swaps, and direction-based edits (e.g. SVM-recovered "smile" axis) on real images.
