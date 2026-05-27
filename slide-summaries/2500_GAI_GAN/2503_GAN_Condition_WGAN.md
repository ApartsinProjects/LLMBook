# 2503_GAN_Condition_WGAN — Per-Slide Summary

**Source file:** `2503_GAN_Condition_WGAN.pptx`
**Source folder:** `SlidesPool/2500_GAI_GAN/`
**Drive link:** https://drive.google.com/file/d/1aIzcg1wCBc5Vwf5OPWuKhYGSpzitHuBs/view
**Slide count (exact, via python-pptx):** 37
**Extraction:** Local parse + slide PNG render. Most code panels and example galleries were inspected visually; paragraphs kept concise for the large deck.

---

## Slide 1 — Condition GANs
Title slide introducing conditional GANs (cGANs) and the Wasserstein GAN variant.

## Slide 2 — Generating Images with Certain Characteristics
Two methods for controllable generation are outlined: search latent vectors that correspond to desired characteristics (post-hoc), or train the generator on pairs of input noise plus labels (a priori).

## Slide 3 — Conditional GAN
Section-header slide opening the conditional GAN architecture.

## Slide 4 — Recipe
The cGAN recipe specifies the target label as one-hot, passes it through an embedding layer, concatenates the embedding with the noise input, and trains both the generator (produces a fake image given a label) and the discriminator (detects fake images given a label) on the joint input. Labels can also be injected at later layers.

## Slide 5 — Prepare Data
Four code panels resize images along the short edge and center-crop the long edge.

## Slide 6 — Dataset Class
Two code panels implement the cGAN dataset class that returns image and label pairs.

## Slide 7 — Discriminator
Five code panels define a two-stage discriminator: the first sub-model produces a 64x2x2 feature map flattened to 256 features, and the second sub-model takes those 256 features concatenated with a 32-dim label embedding (288 total) and outputs the real/fake score.

## Slide 8 — Generator
Five code panels define the generator that takes a noise vector concatenated with a label embedding and emits an image.

## Slide 9 — Training
Two code panels show the cGAN training step.

## Slide 10 — Training
Two code panels show validation using a fixed noise vector printed each iteration, with random man/woman labels passed to the generator for fake image generation.

## Slide 11 — Results
Two panels show outputs after one epoch versus 25 epochs, illustrating progressive improvement.

## Slide 12 — Conditional Wasserstein GAN
Section-header slide introducing the Wasserstein-loss extension (vɑːsərstaɪn).

## Slide 13 — Dataset
The Kaggle eyeglasses dataset is used, labeled man/woman and glasses/no glasses; two panels show sample images.

## Slide 14 — GAN Training Challenges: Mode Collapse
Mode collapse occurs when the generator finds a single complex image that consistently fools the discriminator. Synthetic outputs collapse to a single mode, the generator's loss stays near its minimum, and neither network gets a useful gradient to improve.

## Slide 15 — GAN Training Challenges: Discriminator Dominance
When the discriminator dominates, D(y) becomes flat around y and its gradient vanishes, again starving the generator of useful signal.

## Slide 16 — Challenges
The slide summarizes both failure modes (mode collapse and discriminator dominance) and notes the common culprit: the discriminator's sigmoid output saturates at large logits and the gradient drops to zero.

## Slide 17 — Vanila GAN: Binary Cross-Entropy Loss
The vanilla GAN loss is the sigmoid-based binary cross-entropy, where the discriminator's output is a probability and the labels are 0/1. The expectations are taken over the real and fake distributions; the generator's training objective is the symmetric flip.

## Slide 18 — Wasserstein Loss
WGAN removes the sigmoid and reinterprets the discriminator's output as a score (calling it a "critic"). The critic loss maximizes the score difference between real and fake images, and the generator loss tries to produce high-score fakes.

## Slide 19 — Enforcing Lipschitz Constraint
Without a sigmoid the critic can output very large numbers, causing numerical instabilities. The fix is to enforce a 1-Lipschitz constraint on the critic by penalizing large gradients, the Gradient Penalty Loss.

## Slide 20 — Sampling Gradient
The expected gradient penalty is estimated by sampling gradients at specific points; the standard recipe uses random interpolations between real and fake images as the sampling locations.

## Slide 21 — WGAN: Stable GAN version
A code panel implements the full WGAN-GP training step: run the critic on real, fake, and their random interpolation to obtain the gradient for the penalty term.

## Slide 22 — Conditional GAN(cGAN): The Training Process
A schematic shows cGAN built on the WGAN architecture, where labels are concatenated and the critic learns Wasserstein-style scores conditioned on them.

## Slide 23 — Critic Model
The critic input is a 64x64 image with five channels: 3 color channels plus 2 one-hot label channels (glasses / no glasses) broadcast over all pixels. Convolutional layers gradually shrink spatial dimensions while growing depth; the first layer uses 16 features.

## Slide 24 — Refresher: InstanceNorm2D
The slide recaps InstanceNorm2D, which normalizes per-sample per-channel and is preferred over batch-norm in WGAN to avoid leaking statistics across the batch.

## Slide 25 — Generator
The generator takes a 102-dim vector (100 noise + 2 label one-hot) and outputs a 64x64x3 image. Label channels are added at training time so the critic remains informed.

## Slide 26 — Weight Initialization
Conv2D and ConvTranspose2D weights are initialized from a reduced-variance Gaussian instead of the PyTorch default to avoid gradient explosion, while bias is initialized to multiply-by-1 plus add-0.

## Slide 27 — Gradient Penalty
Three code panels implement gradient penalty: form a random interpolation, compute the critic's gradient with respect to that input (using `grad_outputs` to sum over the batch), and add the magnitude penalty term to the critic's loss.

## Slide 28 — Prepare data and labels
Three code panels prepare batches of real images concatenated with their label channels.

## Slide 29 — Train Batch
A training batch concatenates 5-channel image-and-label tensors with the one-hot labels (`onehots`). The gradient penalty is averaged over five interpolation samples per step.

## Slide 30 — Training
Three code panels show the outer WGAN-GP training loop.

## Slide 31 — Generating
A code panel shows the inference call: feed noise plus a one-hot label and decode the resulting image.

## Slide 32 — Results: With Glasses
Two panels show generated faces conditioned on the "with glasses" and "without glasses" labels.

## Slide 33 — Label arithmetic's
Instead of supplying a one-hot label, the slide demonstrates interpolating between two one-hot label vectors while fixing the noise (for example interpolating along the glasses axis on a fixed female face).

## Slide 34 — Vector Arithmetic in latent space
The slide demonstrates the dual trick: fix the label (for example "no glasses") and interpolate the noise vector between two latent points that correspond to male and female faces.

## Slide 35 — Selecting two characteristics simultaneously
Both noise and label are interpolated together along their respective axes, producing a 2D grid of attribute variations.

## Slide 36 — Results
A panel shows the generated 2D grid of male-to-female and no-glasses-to-glasses interpolations.

## Slide 37 — Traversing vectors and labels
Three panels demonstrate smooth traversals through latent-and-label space, illustrating that the trained cWGAN-GP has organized its latent space into semantically meaningful axes.

---

## Deck-level takeaway
Conditional GANs steer generation by injecting label embeddings into both generator and discriminator. Plain conditional GANs train fine on small datasets but suffer from mode collapse and discriminator dominance once data and complexity grow. The Wasserstein GAN with gradient penalty (WGAN-GP) fixes this by replacing the sigmoid binary-cross-entropy with a score-based Earth-Mover loss and enforcing 1-Lipschitzness via a gradient penalty on real/fake interpolations. Combining cGAN with WGAN-GP yields a stable conditional model that supports rich latent-and-label arithmetic (interpolating noise, interpolating labels, or both jointly) to produce smooth 2D attribute grids.
