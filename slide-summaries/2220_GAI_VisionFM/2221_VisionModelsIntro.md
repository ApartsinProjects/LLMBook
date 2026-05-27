# 2221_VisionModelsIntro — Per-Slide Summary

**Source file:** `2221_VisionModelsIntro.pptx`
**Source folder:** `SlidesPool/2220_GAI_VisionFM/`
**Drive link:** https://drive.google.com/file/d/1C4nepSqoLSDTijRvmMFbYO0hP0nHeZL3/view
**Slide count (exact, via python-pptx):** 5
**Extraction:** Local parse + slide PNG render.

---

## Slide 1 — Pretrained Vision Models
Title slide for a short "menu" lecture that enumerates the four families of pretrained vision models the rest of the course will visit.

## Slide 2 — 1. Pretrained Task-specific models
The first family. Models pretrained on large image datasets for a *specific task* (image classification, image segmentation, object detection), trained on a large but *fixed* set of classes, used inside custom application pipelines with optional fine-tuning. The defining feature: the task is baked into the model.

## Slide 3 — 2. Pretrained Image Representation Models
The second family. Models that embed an image into a vector, pretrained on an extensive image collection. Used as a *backbone* for task-specific models or as the front end of multiple downstream tasks. Examples: CNN-based (ResNet, Inception) and Vision-Transformer-based (with different training strategies named: DINO, DeiT). The defining feature: the model is task-agnostic; downstream code chooses what to do with the embedding.

## Slide 4 — 3. Pretrain multimodal model
The third family. Models that represent images *and* other modalities (text) in the same vector space, so embeddings can be compared across modalities directly. Used in multimodal applications. Examples: CLIP (encodes both text and images into one space) and BLIP (a multimodal assistant that can also generate text). The defining feature: the space is shared across modalities.

## Slide 5 — 4. Generative Models
The fourth family. Models that *generate* images from prompts and conditioning, pretrained on large text/image collections, with many conditioning mechanisms (prompt, other images, mask). Used to generate synthetic data — art, ML training data, segmentation maps (every per-pixel task can be framed as conditional image generation). Examples: VAE/GAN, latent diffusion models, flow-based models. The defining feature: the output is an image, not a representation.

---

## Deck-level takeaway

A short, navigational deck (5 slides) that gives the reader a four-bucket taxonomy of "pretrained vision models" before any specific model is introduced. The four buckets — task-specific, representation, multimodal, generative — are presented with one defining property each and a couple of canonical examples, so by the end of the deck the reader has a mental shelf where every later model (BERT, CLIP, Stable Diffusion, SAM, DINO, …) can be placed. Pedagogically, this is the "before you dive into the trees, here is the forest" slide.
