# 2501_GAN_Intro — Per-Slide Summary

**Source file:** `2501_GAN_Intro.pptx`
**Source folder:** `SlidesPool/2500_GAI_GAN/`
**Drive link:** https://drive.google.com/file/d/1Mi8Bv_1soEyee7W29AgViqA1GtPMvE_U/view
**Slide count (exact, via python-pptx):** 44
**Extraction:** Local parse + slide PNG render. Many code-screenshot slides were inspected visually; long deck so paragraphs are kept concise.

---

## Slide 1 — Generative Adversary Networks- GANs
Title slide introducing the GAN lecture.

## Slide 2 — Generate number pairs
Section-header slide presenting Toy Problem 1 (generating number pairs).

## Slide 3 — Toy Example
Section-header slide that motivates the toy problem with a simple 2D distribution.

## Slide 4 — Generative Adversary Networks
The slide presents the GAN loss in two parts: the discriminator minimizes its classification error (outputting the probability of "real"), while the generator maximizes that error through its contribution to the same objective.

## Slide 5 — GAN
The generator produces fake samples to fool the discriminator, and the discriminator classifies samples as real or fake. Both networks are trained in alternating turns, and once training completes only the generator is used to sample new data.

## Slide 6 — Prepare the dataset and labels
Three code panels prepare the toy training dataset and label tensors for the discriminator's binary classification.

## Slide 7 — Discriminator Network
Two code panels define the discriminator as a small fully connected network with a sigmoid output for real/fake probability.

## Slide 8 — Generator Network
A code panel defines the generator as a small fully connected network that maps a noise vector to the same domain as the real data.

## Slide 9 — Measuring Performance
For toy examples it is easy to test how synthetic data differs from real, and the slide highlights that the per-network loss must be measured separately.

## Slide 10 — Loss and optimizers
The slide shows the classification loss for the discriminator and the use of two separate optimizers (one for discriminator parameters, one for generator parameters) even though both networks have similar architectures.

## Slide 11 — Early Stop: No improvements over patients
A code panel shows the early-stopping helper that halts training when neither network improves for several epochs.

## Slide 12 — Discriminator: Fake/Real Training Step
Two code panels detail the discriminator's update: forward pass on real samples, forward pass on detached generator outputs, combined cross-entropy loss, optimizer step.

## Slide 13 — Train Generator
Two code panels show the generator's update step: forward pass through generator and then discriminator (without detach), with the loss measuring how well the generator fools the discriminator.

## Slide 14 — Training Loop
A code panel shows the outer training loop alternating one discriminator step and one generator step per batch, optimizing each loss independently.

## Slide 15 — Results
A figure shows the toy-problem outputs at the end of training, with generated samples approaching the real distribution.

## Slide 16 — PyTorch JIT and TorchScript
The slide introduces PyTorch JIT and TorchScript as a just-in-time compiler that turns eager-mode models into a static computational graph, producing portable code that runs without Python (for example in C++) and applies optimizations.

## Slide 17 — Two modes of JIT
Two JIT modes are described. Static compilation (`torch.jit.script`) performs static analysis and understands the computational graph but cannot handle all Python constructs (generators, mixed scripts). Tracing (`torch.jit.trace`) records tensor operations along a sample input and captures data-dependent control flow.

## Slide 18 — Load and run trained generator
Two code panels show loading the TorchScript-compiled generator and running it without the original Python class definition.

## Slide 19 — Generate numbers with patterns
Section-header slide presenting Toy Problem 2 (generating numbers that follow a pattern).

## Slide 20 — Generate Number with Patterns
The task is to learn to generate integers between 0 and 99 that are multiples of five without explicitly coding the pattern. Training data consists of one-hot vectors of size 100 representing such integers.

## Slide 21 — 1HE Helper functions
Nine code panels show helper functions for one-hot encoding, decoding, sampling, and visualization for the integer task.

## Slide 22 — Discriminator and generator
Two code panels show the discriminator (estimating per-number scores; argmax during generation) and the generator for the integer task.

## Slide 23 — Generate training sequence
Five code panels build the training data of integers that are multiples of five, one-hot encoded.

## Slide 24 — Training step
Two code panels show the training step, noting that fake inputs are one-hot at integer positions but the generator's outputs are vectors in [0,1], which may make the discriminator's job easier.

## Slide 25 — Training Loop
A code panel runs the loop with a custom distance criterion (sum of remainders mod 5) used as the performance metric.

## Slide 26 — Saving and using trained model
Three code panels show saving the trained generator via TorchScript and using it to produce new integers that respect the divisible-by-5 pattern.

## Slide 27 — GAN for Image Generation
Section-header slide pivoting from toy problems to image generation.

## Slide 28 — Generate Handwritten Digits
A code panel previews the MNIST handwritten-digits generation task.

## Slide 29 — GAN
A schematic recaps the GAN architecture as applied to images: noise into generator, fake plus real into discriminator.

## Slide 30 — Prepare Data
A code panel loads MNIST through torchvision and applies normalization.

## Slide 31 — Discriminator
Four code panels define an MLP-based discriminator that flattens the 28x28 image and outputs a real/fake probability.

## Slide 32 — Generator
Five code panels define the generator as an MLP that maps a 100-dim noise vector through dense layers to a 784-dim image, reshaped to 28x28.

## Slide 33 — Tanh activation
The slide shows the tanh activation used at the generator's output to match the [-1, 1] normalized image range.

## Slide 34 — Train steps
Two code panels show the per-batch discriminator and generator updates for MNIST.

## Slide 35 — Training
Two code panels run the full training loop and report periodic samples.

## Slide 36 — Generate synthetic digits
Two code panels show the trained generator producing batches of synthetic digits.

## Slide 37 — Generate Fashion-MNIST images
Section-header slide for Toy Problem 3 (Fashion-MNIST).

## Slide 38 — Toy Problem 3: Learn To Generate Fashion-MNIST
Fashion-MNIST contains 60K grayscale 28x28 clothing-item images scaled to [-1, 1].

## Slide 39 — Discriminator Network
A code panel defines the Fashion-MNIST discriminator, identical in shape to the MNIST one.

## Slide 40 — Generator
A code panel defines the generator with a 100-dim noise input mapped to 784 output pixels.

## Slide 41 — Tanh activation
The slide again notes the tanh output to match the [-1, 1] data range.

## Slide 42 — The Model
A code panel ties the generator and discriminator together for the Fashion-MNIST experiment.

## Slide 43 — Training
Three code panels show the training run with periodic image snapshots.

## Slide 44 — Results
Two panels show generated Fashion-MNIST samples at the end of training, illustrating the model learning recognizable garment shapes.

---

## Deck-level takeaway
The deck builds up GANs from first principles through three escalating toy problems. After defining the generator-discriminator min-max game and its alternating training loop, it walks through (1) sampling number pairs, (2) generating integers that obey a hidden divisibility pattern, and (3) generating MNIST and Fashion-MNIST images, all in plain PyTorch. Along the way it introduces practical concerns: separate optimizers per network, early stopping, TorchScript for serving, tanh outputs to match normalized image ranges, and per-task distance metrics for evaluating sample quality.
