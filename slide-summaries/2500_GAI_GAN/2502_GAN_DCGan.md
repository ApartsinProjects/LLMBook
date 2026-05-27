# 2502_GAN_DCGan — Per-Slide Summary

**Source file:** `2502_GAN_DCGan.pptx`
**Source folder:** `SlidesPool/2500_GAI_GAN/`
**Drive link:** https://drive.google.com/file/d/1iB7L18E5xka_uK3iIHoqMuy-whWJBHNL/view
**Slide count (exact, via python-pptx):** 24
**Extraction:** Local parse + slide PNG render. Most slides have minimal body text; code-screenshot and example-gallery slides were inspected visually.

---

## Slide 1 — GAN
Title slide for the Deep Convolutional GAN (DCGAN) lecture.

## Slide 2 — Refresher: Convolution layer
Four panels recap 2D convolution as the sliding multiply-add of a kernel over an image, including stride and channel arithmetic.

## Slide 3 — Refresher: Dilated Convolution
The slide recaps dilated (atrous) convolution, which spreads the kernel taps to enlarge the receptive field without extra parameters.

## Slide 4 — Refresher: Transposed Convolution
Transposed convolution is recapped as inserting zeros (stride=2) into the input before running a usual convolution; this is the upsampling primitive used by DCGAN generators.

## Slide 5 — Batch normalization
A figure introduces batch normalization, which DCGAN relies on for stable training.

## Slide 6 — Refresher: Batch Norm
Batch normalization is recapped as normalizing to zero mean and unit variance per channel, then applying learned shift and scale parameters.

## Slide 7 — Anime Face Generation
Section-header slide for the first DCGAN example: generating anime faces.

## Slide 8 — Training Data
A panel previews the anime-faces training dataset.

## Slide 9 — High-Res Image Generation
The Kaggle dataset has 63,632 color anime faces. The slide shows tensor handling (PyTorch puts channels first; permute back for display) and four sample images.

## Slide 10 — Refresher: Leaky ReLU
Two panels recap LeakyReLU, which DCGAN uses in the discriminator to avoid dead-unit problems.

## Slide 11 — Discriminator
Two code panels define the DCGAN discriminator as a stack of strided convolutions plus LeakyReLU plus batch-norm blocks ending in a single scalar output.

## Slide 12 — Generator
Two code panels define the generator as a stack of transposed convolutions plus batch-norm plus ReLU blocks that turn a 100-channel 1x1 latent into a full-resolution color image.

## Slide 13 — The Model
A code panel ties the generator and discriminator together with their separate optimizers.

## Slide 14 — Training Loop
Two code panels show the DCGAN training loop with per-batch discriminator and generator updates.

## Slide 15 — Results
Two panels show generated anime faces after a single epoch and after 20 epochs, illustrating the model rapidly approaching plausible outputs.

## Slide 16 — Synthetic Face Photo
Section-header slide for the second DCGAN example: photorealistic faces.

## Slide 17 — Dataset: Male-Female Faces
A panel shows the male/female face dataset used for the next experiment.

## Slide 18 — Prepare cropped faces
Three code panels run face cropping on the raw photos to focus the GAN on the relevant region.

## Slide 19 — Haar cascade
Haar cascade face detection is described as extracting Haar features, sliding a fixed 24x24 window across rescaled images, applying weak classifiers (shallow decision trees), an AdaBoost-stronger classifier, and non-maximum suppression.

## Slide 20 — Dataset Class
Four code panels implement a custom PyTorch Dataset class that loads, crops, and normalizes the face images.

## Slide 21 — PyTorch Default Weight Initialization
PyTorch initializes weights from a Kaiming uniform distribution suitable for linear and convolution layers. Generative models start from noise and large values lead to instability and high variance, so smaller initial values closer to zero help.

## Slide 22 — Weight Initialization for GAN
The slide shows DCGAN's recommended init: a normal distribution (instead of Kaiming) with small standard deviation, keeping weights closer to zero.

## Slide 23 — Models
Three code panels define the photorealistic-face DCGAN models with the recommended initialization.

## Slide 24 — Synthetic faces
Two panels show generated synthetic face photos after training, demonstrating that DCGAN scales the toy-problem recipe to plausible-looking faces.

---

## Deck-level takeaway
DCGAN swaps the fully connected discriminator and generator of vanilla GANs for fully convolutional ones: strided convolutions plus LeakyReLU plus batch-norm in the discriminator, and transposed convolutions plus batch-norm plus ReLU in the generator. With small Gaussian weight initialization and standard alternating training the recipe scales to 64x64 color images (anime faces, photorealistic male/female faces), and Haar-cascade face cropping is shown as a useful preprocessing step for face datasets.
