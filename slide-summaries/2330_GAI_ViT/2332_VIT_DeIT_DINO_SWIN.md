# 2332_VIT_DeIT_DINO_SWIN — Per-Slide Summary

**Source file:** `2332_VIT_DeIT_DINO_SWIN.pptx`
**Source folder:** `SlidesPool/2330_GAI_ViT/`
**Drive link:** https://drive.google.com/file/d/1P8Y4PjrTxPvLrMW12M3ERUyg8YAT6N9y/view
**Slide count (exact, via python-pptx):** 22
**Extraction:** Local parse + slide PNG render. Code-only and example-only slides were inspected visually.

---

## Slide 1 — Image Classification with ViT
Title slide that introduces ViT-based image classification and the variants that improve it.

## Slide 2 — Prepare dataset
Five code panels show preparing an image classification dataset for a Hugging Face ViT, including loading, splitting, and applying image processor transforms.

## Slide 3 — Classifier Model
A code panel shows building a ViT image-classification model with `ViTForImageClassification.from_pretrained`, swapping in the user's label vocabulary.

## Slide 4 — Training and evaluation
Two code panels show the Hugging Face Trainer setup and the resulting evaluation metrics on the custom dataset.

## Slide 5 — DeIT: Data-Efficient Image Transformers
Title slide introducing DeIT as a way to train a strong ViT without ImageNet-21K, by distilling knowledge from a CNN teacher.

## Slide 6 — Motivation
ViTs outperform CNNs but require massive training data. DeIT addresses this by distilling knowledge from a pretrained CNN; the ViT's attention is trained to learn what the CNN knows by matching its SoftMax classification head, which was itself trained on labeled ImageNet.

## Slide 7 — Distillation token
DeIT introduces a special distillation token alongside the [CLS] token. Both attend over the same patches and parameters, and a classification head on the distillation token is optimized with a cross-entropy loss against the CNN teacher's SoftMax output. The final image embedding can be the [CLS] token, the distillation token, or their combination. The recipe enables training on ImageNet-1K (1M images) rather than ImageNet-21K (14M).

## Slide 8 — Example
A worked example panel shows DeIT outputs and the relative performance versus a plain ViT trained on the same data.

## Slide 9 — Dino
Title slide that introduces DINO (self-distillation with no labels).

## Slide 10 — Motivation
A good semantic representation should be similar across scale and viewpoint. DINO picks a random region of the image and creates a local crop (under 50% of the image, resized to 96x96) and a global crop (over 50%, resized to 224x224); both should map to similar [CLS] embeddings. A high-dimensional pseudo-label linear layer (about 65K outputs) with SoftMax measures similarity as agreement between probability distributions. The target is to train both the embedding and the linear layer so local and global crops yield similar distributions.

## Slide 11 — Self-Distillation Training
Two copies of the model are maintained: a slow-changing teacher and a fast-changing student. Both produce large pseudo-label logit vectors. Global crops (224x224) are fed through the teacher, and the student is trained to match the teacher's output on the local (96x96) crops.

## Slide 12 — Training
The training loop is detailed. The student processes both local and global crops; the teacher processes only global crops. In each batch, the teacher sees two global crops and the student sees N local plus 2 global crops; every student output is matched to a teacher output. Teacher weights are updated as an exponential moving average of the student.

## Slide 13 — Prevention collapse
A collapse failure mode is avoided by centering the teacher's logits: maintain an EMA of the logits, subtract the center before SoftMax, and apply a temperature. If a pseudo label dominates, the center shifts it toward zero, stabilizing training.

## Slide 14 — Dino Training
A code panel shows a Dino training script invocation, illustrating the canonical training run.

## Slide 15 — Attention Maps (to [CLS] token)
The slide shows DINOv2 attention maps to the [CLS] token, with the larger dataset and network producing cleaner object-localized attention than the original DINO.

## Slide 16 — Image Representation
The slide notes that the image representation is the sequence of all patch token embeddings, which can be pooled or replaced by the [CLS] token for a single per-image embedding.

## Slide 17 — Swin Transformer
Title slide that introduces Swin (Shifted Window Visual Transformer).

## Slide 18 — Hierarchical Transformer
Swin computes attention within local windows rather than globally (W-MSA), which is much cheaper for high-resolution images. To recover cross-window interaction, the next layer shifts the windows by half-size (SW-MSA), creating connections to neighboring windows.

## Slide 19 — Hierarchical Transformer
Swin builds a hierarchy by merging neighboring windows: concatenate the embeddings of four (2x2) patches (giving 4xC channels), then apply a linear layer to reduce to 2xC channels. This halves the resolution and doubles the channel count, mimicking a CNN pyramid.

## Slide 20 — Swin Transformer: Architecture
A diagram lays out the full Swin architecture, alternating W-MSA and SW-MSA blocks across multiple hierarchical stages.

## Slide 21 — Representation
The slide shows the per-stage hierarchical representations Swin produces, suitable as a backbone for detection and segmentation in the style of FPN.

## Slide 22 — Classification
A final panel shows Swin used for image classification by adding a head over the global-pooled top-stage features.

---

## Deck-level takeaway
The deck surveys the ViT family beyond the vanilla model. DeIT shrinks the data requirement by distilling from a CNN teacher into a dedicated distillation token; DINO removes labels entirely via student-teacher self-distillation between local and global crops, with centering to prevent collapse; and Swin restructures attention into shifted local windows arranged in a hierarchy, recovering CNN-style multi-scale features and making ViTs practical for dense prediction.
