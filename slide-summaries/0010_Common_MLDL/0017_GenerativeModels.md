# 0017_GenerativeModels — Per-Slide Summary

**Source file:** `0017_Generative Models.pptx`
**Source folder:** `SlidesPool/0010_Common_MLDL/`
**Drive link:** https://drive.google.com/file/d/1EIcSEq0tvY2_haVLJ3uqN4L_sKxmUOk9/view
**Slide count (exact, via python-pptx):** 4
**Extraction:** Local parse + slide PNG render. Visual inspection of all four slides confirmed the title divider, two diagrammatic content slides, and a final image-based table of use cases.

---

## Slide 1 — Generative Models
Title divider introducing the section on generative models.

## Slide 2 — Generative Models
This slide contrasts three paradigms that frame the rest of the deck. Discriminative models are trained on labeled pairs (x, y) and learn to predict the label y given a new sample x. Generative models, by contrast, are trained on unlabeled samples x and learn to produce a new sample that resembles the training data. Conditional generative models bridge the two by training on pairs (x, y) and generating a sample x conditioned on a guidance signal y, where the guidance can be a class label, a text prompt, an image, or a sketch. The accompanying figure shows two scatter-style clusters of cat and dog thumbnails: on the left, a "Generative" view groups all samples by similarity within each green and blue blob, while on the right, a "Discriminative" view draws a dashed boundary that separates the two classes. The visual reinforces the conceptual distinction between modeling the data distribution itself and modeling the decision surface between classes.

## Slide 3 — Representation Learning
This slide positions representation learning and generative modeling as two complementary mappings between data space and latent space. Representation models map inputs into a compact representation, often called a feature vector or embedding, while preserving the meaning relevant for downstream tasks. Generative models instead learn the full space of valid representations, referred to as the latent space or embedding space, and then sample within it. The generative pipeline first draws a new latent representation and then applies a decoder model that maps this representation back to the original data space. The diagram at the bottom makes this symmetry explicit: on the left, "Representation learning" shows a blue blob labeled p_data in data space being mapped by an encoder f into a circular representation space containing the embedding z; on the right, "Generative modeling" reverses the arrows, sampling z from a prior p_z in representation space and using a generator g to map it back into the blue blob of data space x. The shared shapes emphasize that an encoder and a generator are mirror operations across the same latent bottleneck.

## Slide 4 — Major use cases for generative models
This slide presents a color-banded table that organizes the four canonical use cases for generative models. Unconditional generation trains on samples {X} drawn from a distribution D and produces a new sample X, with the example of training on cat images and generating a new cat image. Conditional generation trains on pairs {(X, Y)} from D and generates a new X given Y, illustrated by training on image and text caption pairs to generate an image from a prompt. Density estimation trains on samples {X} from D and, given a new sample x, estimates D(x) = Probability(x), with anomaly detection as the canonical application. Representation learning, shown in the blue band at the bottom, learns a compact representation of {X} from D and, given a new sample X, produces its compact representation Z for downstream tasks such as classification. Together the four rows give a clean taxonomy that the rest of the curriculum can map specific architectures (VAE, GAN, diffusion, autoregressive) onto.

---

## Deck-level takeaway
The deck offers a compact conceptual scaffold for generative modeling rather than a deep dive into any specific architecture. It first separates discriminative, generative, and conditional generative paradigms, then frames generative modeling as the mirror image of representation learning across a shared latent space, and finally enumerates four canonical use cases (unconditional generation, conditional generation, density estimation, and representation learning) that together cover the practical landscape.

The visual choices reinforce the pedagogy: the cat-and-dog clustering figure makes the distribution-versus-boundary contrast tangible, while the encoder/generator mirror diagram with p_data, p_z, f, and g sets up the vocabulary needed for VAEs, GANs, normalizing flows, and diffusion models in subsequent decks.
