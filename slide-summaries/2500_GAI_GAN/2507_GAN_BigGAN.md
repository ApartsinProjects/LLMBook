# 2507_GAN_BigGAN — Per-Slide Summary

**Source file:** `2507_GAN_BigGAN.pptx`
**Source folder:** `SlidesPool/2500_GAI_GAN/`
**Drive link:** https://drive.google.com/file/d/1v9DgLbJcwsk1d4KyIdNDyAiMtTIcc6mF/view
**Slide count (exact, via python-pptx):** 15
**Extraction:** Local parse + slide PNG render. Schematic and code slides were inspected visually.

---

## Slide 1 — BigGAN
Title slide for BigGAN, a large-scale class-conditional GAN.

## Slide 2 — Class-conditional image synthesis
BigGAN generates high-resolution, high-quality class-conditional images. It is trained on a massive image dataset (ImageNet) and conditioned on a class id.

## Slide 3 — Self-Attention GAN
Self-Attention GAN augments convolutions, whose receptive fields are local, with self-attention to recover global coherence. The self-attention operates over a feature map of length C channels, projecting the input into a new C' embedding space before computing attention.

## Slide 4 — GAN loss: Saturation Problem
Vanilla GAN training saturates: early in training the generator is weak, the discriminator easily detects fakes, and the generator's BCE-based loss is close to zero, killing its gradient.

## Slide 5 — Hinge Loss
BigGAN replaces the saturating log-loss with a hinge loss. The discriminator's loss limits how far it pushes correct classifications beyond the margin (avoiding over-confidence), while the generator's loss tries to push fake scores above the discriminator's hinge boundary.

## Slide 6 — Class embedding
A trainable class embedding feeds the generator: the embedding controls batch-normalization scales and biases, combined with parts of the latent input (split-z conditioning).

## Slide 7 — Class embedding in discriminator
The discriminator logit is modified to force its features and the class embedding to be similar via an inner product. With f(x) the discriminator's CNN features and u its linear head, real images should have features close to the class embedding.

## Slide 8 — Spectral Normalization
Spectral normalization ensures linear layers do not amplify small changes. The weight matrix's largest singular value (spectral norm) is bounded by clipping after each SGD update, keeping the network 1-Lipschitz.

## Slide 9 — Update the discriminator more than the generator
BigGAN trains the discriminator twice per generator update. The discriminator must stay strong to provide a useful gradient signal to the generator.

## Slide 10 — Moving Average of Model Weights
Generator weights fluctuate noisily because the discriminator changes underneath them. BigGAN maintains an exponential moving average of the generator weights during training and uses the EMA version for inference, smoothing out the noise.

## Slide 11 — Orthogonal weights initialization
Kaiming initialization controls variance, but BigGAN uses orthogonal initialization (the Q factor from a QR decomposition of a random matrix), which makes weight matrices behave like rotations and avoids squashing or distorting inputs early in training.

## Slide 12 — Truncation Trick
At inference, BigGAN samples the latent near zero (truncated to a small radius). This trades diversity for quality: closer to the mean produces sharper but more uniform images.

## Slide 13 — More tricks
Additional engineering boosts BigGAN: very large batch sizes (2048), more parameters, skip-z connections that feed the latent directly to deep layers, and orthogonal regularization that enforces orthogonality during training rather than just at init.

## Slide 14 — BigGAN: Preparation
Two code panels show loading a pretrained BigGAN model and preparing class conditioning.

## Slide 15 — BigGAN: Generation
Two code panels show running BigGAN sampling with the truncation trick and visualizing the class-conditional outputs.

---

## Deck-level takeaway
BigGAN turns class-conditional ImageNet generation into a practical problem by stacking many stabilizing tricks: self-attention for global coherence, hinge loss instead of saturating BCE, class embeddings injected into batch-norm and into the discriminator logit, spectral normalization for 1-Lipschitz behavior, asymmetric update ratios (2 discriminator steps per generator step), exponential moving averages of generator weights, orthogonal initialization and regularization, very large batches, skip-z connections, and a truncation trick that trades diversity for sharpness at inference time.
