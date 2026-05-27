# 2224_VisionMultimodall — Per-Slide Summary

**Source file:** `2224_VisionMultimodall.pptx`
**Source folder:** `SlidesPool/2220_GAI_VisionFM/`
**Drive link:** https://drive.google.com/file/d/1YRLqXZr6Ak7Qciis4i1uwP70kyK5LyVQ/view
**Slide count (exact, via python-pptx):** 6
**Extraction:** Local parse + slide PNG render. Most slides have minimal body text and rely on visuals such as CLIP diagrams and chat-with-image examples.

---

## Slide 1 — Pretrained Vision Multimodal Models
Title slide that introduces multimodal foundation models combining images and text.

## Slide 2 — Multimodal Embedding
Section-header slide that frames the upcoming material on joint image-text embedding spaces.

## Slide 3 — Multimodal embedding
The slide defines a multimodal embedding space as one where images and text are mapped to vectors that lie close together when they describe the same concept; an image of a cat and the word "cat" should be neighbors in this shared latent space.

## Slide 4 — Zero-shot classification with CLIP
The slide illustrates CLIP-style zero-shot classification: candidate class names are embedded with the text encoder, the query image is embedded with the image encoder, and the predicted class is the one whose text embedding has the highest cosine similarity to the image embedding.

## Slide 5 — Image Captioning
Section-header slide that transitions to captioning models which produce text from image embeddings.

## Slide 6 — Chatting with image
The slide describes interactive visual dialogue: a decoder converts joint image/text embeddings into natural-language text, enabling multi-turn questioning about an image. The visual panels show example chat exchanges where a user asks questions about an image and the model responds in natural language.

---

## Deck-level takeaway
Multimodal vision foundation models hinge on aligning images and text in a shared embedding space (CLIP-style). Once aligned, the same embedding supports zero-shot classification by nearest-neighbor matching against class-name embeddings, and chat-style image understanding when a decoder is attached to convert joint embeddings back into language.
