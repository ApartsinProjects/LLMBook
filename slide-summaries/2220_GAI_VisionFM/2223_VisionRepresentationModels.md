# 2223_VisionRepresentationModels — Per-Slide Summary

**Source file:** `2223_VisionRepresentationModels.pptx`
**Source folder:** `SlidesPool/2220_GAI_VisionFM/`
**Drive link:** https://drive.google.com/file/d/1Vw8JZFNosUccyO58GkvIdZmpntp82N_A/view
**Slide count (exact, via python-pptx):** 9
**Extraction:** Local parse + slide PNG render. Pure-image slides (3, 5, 6, 7, 9) and code-only slides (4, 8) were visually inspected.

---

## Slide 1 — Pretrained Visual Representation Models
Title slide that introduces pretrained backbones (ResNet, ViT, DINO) used as image feature extractors.

## Slide 2 — Image Representation
The slide describes how pretrained backbones encode images either as a single vector or as a sequence of per-patch vectors. Two pretraining objectives are highlighted: image classification or class discrimination, and instance discrimination (for example distinguishing different faces). The accompanying figures show a CNN flattening a feature map into a vector and a ViT producing CLS plus patch embeddings.

## Slide 3 — Class vs. Mean Pooling
The slide compares two pooling strategies for ViT representations: using the dedicated [CLS] token versus mean-pooling all patch tokens. The figure shows that the two yield distinct embeddings with different properties for downstream tasks.

## Slide 4 — Fixed representation as classifier features
The slide shows PyTorch code that freezes a pretrained backbone, runs images through it to extract feature vectors, and treats those vectors as fixed inputs to a downstream classifier.

## Slide 5 — Train Classifier using fixed representation
The slide visually walks through training a small linear or shallow classifier on the frozen embeddings produced in the previous step, using the standard supervised loop.

## Slide 6 — Embed
The slide shows the encode step in isolation: an image goes through the frozen backbone and emerges as a fixed-dimensional embedding vector that downstream heads consume.

## Slide 7 — Train Classification Head
The slide focuses on the head training step, showing the classification layer being optimized while the backbone gradient is detached.

## Slide 8 — Training using HF
The slide presents Hugging Face Transformers code snippets that wrap the same workflow using the AutoModel and AutoImageProcessor pipeline, plus a Trainer for the classification head.

## Slide 9 — Freeze backbone
The slide illustrates the `requires_grad = False` recipe applied to backbone parameters so that only the head receives gradient updates during training.

---

## Deck-level takeaway
Pretrained visual representation models (CNNs, ViTs, self-distilled networks like DINO) serve as frozen feature extractors that turn an image into either a single vector or a sequence of patch embeddings. With the backbone frozen, downstream tasks reduce to training a lightweight classification head on those representations, a workflow that PyTorch and Hugging Face Transformers both expose in a few lines of code.
