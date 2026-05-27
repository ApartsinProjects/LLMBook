# 1621_MultimodalRepresentationClip — Per-Slide Summary

**Source file:** `1621_MultimodalRepresentationClip.pptx`
**Source folder:** `SlidesPool/1620_LLM_VisionLanguageModels/`
**Drive link:** https://drive.google.com/file/d/1sUHgApd08uTjGQQ8xm3qSTGeq400gZ7k/view
**Slide count (exact, via python-pptx):** 26
**Extraction:** Local parse + slide PNG render. Bullets carry the CLIP and VisualBERT recipes; code screenshots illustrate OpenCLIP and HuggingFace usage.

---

## Slide 1 — Visual Language Models
Title slide for the deck on visual language models.

## Slide 2 — Multimodal Embeddings and Cross-model generation
Multimodal embedding represents images, text, and audio with a single model that maps into a shared semantic space (CLIP). Cross-modal generation generates text or images from a text or image prompt (BLIP, diffusion), frequently using multimodal embeddings.

## Slide 3 — CLIP: Multimodal Embedding
Section divider for CLIP.

## Slide 4 — Multimodal Embeddings: Applications
A figure surveying applications of multimodal embeddings.

## Slide 5 — Background: Cosine Similarity
Reminder of cosine similarity, which for normalized vectors equals the dot product.

## Slide 6 — Shared latent space
CLIP represents images and text in a shared space where similar contents have similar embeddings, trained on (image, text) pairs by jointly training two encoders.

## Slide 7 — Training Data
A figure showing paired images and captions as the CLIP training data.

## Slide 8 — CLIP Architecture: Projection Layers
Two frozen pretrained encoders. The image encoder is a ViT with patch size 14x14. The text encoder is a transformer with [EOS] pooling to represent the entire text. Trainable projection layers map each encoder's output to the shared latent space.

## Slide 9 — Clip: Training
Contrastive loss: maximize similarity between matching images and texts. Given a batch of N images and N matching texts, InfoNCE (Informative Noise-Contrastive Estimation) treats wrong text descriptions as noise / distractors.

## Slide 10 — Example
Section header for an OpenCLIP-based code example.

## Slide 11 — (no title)
Eight screenshots loading the image, tokenizing the caption, and embedding the caption.

## Slide 12 — (no title)
Eight screenshots embedding the image, computing the image-text embedding dot product, and producing the similarity matrix.

## Slide 13 — Clip Internals
Section divider for a step-by-step look at CLIP internals.

## Slide 14 — Pool from ViT
Four screenshots showing how the image representation is pooled from the ViT.

## Slide 15 — Pool from text encoder
Two screenshots showing how the text representation is pooled from the text encoder.

## Slide 16 — Project to common latent space
Five screenshots showing projection to the common latent space and normalization for comparison.

## Slide 17 — Normalize and compare
Three screenshots normalizing and comparing the embeddings, returning probabilities.

## Slide 18 — Example
Section header for a zero-shot classification example.

## Slide 19 — Zero-shot Classification with CLIP
Four screenshots showing zero-shot classification. The CLIP model produces logits per image when supplied with both text and images.

## Slide 20 — Clip model in sentence_transformers
Two screenshots showing the CLIP model used through the sentence-transformers library to embed text and images.

## Slide 21 — Zero-shot classification pipeline
Three screenshots wrapping the above in a reusable pipeline.

## Slide 22 — Visual BERT
Section divider for VisualBERT.

## Slide 23 — VisualBERT
Trained on text-image pairs. Image tokens are derived not from all patches (as in ViT) but from the top 36 bounding boxes where objects are detected; bounding-box features are 2048-dim from R-CNN, projected to 768-dim. Training objectives are MLM (predict masked text tokens) and SIA (Sentence-Image Alignment: predict whether image and text match). Task-specific fine-tuning includes VQA, where the model builds a vocabulary of about 3K answer phrases and adds a classification head to pick the correct answer from image plus question.

## Slide 24 — VisualBERT
Two diagrams of the VisualBERT pipeline.

## Slide 25 — Question-Answering example
A screenshot of QA inference with a fixed set of possible answers (COCO classes). Inputs include text tokens, vision tokens, masks for ignoring padding, token-type IDs (text vs. vision), and ResNet-derived visual embeddings.

## Slide 26 — Open Visual Question Answering
For open-ended VQA, embed image plus question plus candidate answer and put a binary classification head on top to score each candidate.

---

## Deck-level takeaway
The deck explains multimodal representation through two complementary models. CLIP trains an image encoder (ViT) and a text encoder (transformer) jointly with InfoNCE contrastive loss on image-caption pairs, producing a shared latent space where cosine similarity is the universal score. This single trick enables zero-shot image classification (pick the label whose text embedding is closest to the image embedding) and other downstream uses, demonstrated in OpenCLIP and sentence-transformers. VisualBERT takes a different approach for tasks like VQA: it uses R-CNN object-detection features as image tokens, trains with MLM plus Sentence-Image Alignment, and fine-tunes with task-specific heads for closed-vocabulary or open-ended question answering.
