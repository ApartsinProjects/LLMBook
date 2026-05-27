# 2334_GenerativeImage_ImageGPT — Per-Slide Summary

**Source file:** `2334_GenerativeImage_ImageGPT.pptx`
**Source folder:** `SlidesPool/2330_GAI_ViT/`
**Drive link:** https://drive.google.com/file/d/1jhuxHV9NGhHWKUmUKwsMySsYppDH_wTh/view
**Slide count (exact, via python-pptx):** 4
**Extraction:** Local parse + slide PNG render. Most text was captured directly from the deck body; visuals on slides 3 and 4 were inspected to describe the schematic and example completions.

---

## Slide 1 — ImageGPT
Title slide announcing ImageGPT as a decoder-based approach to image completion and representation learning.

## Slide 2 — Generative modeling
The slide describes ImageGPT's tokenization and training recipe. Images are downscaled to 32x32 or 64x64 and each pixel is treated as a token from a 512-value codebook, yielding 1024 tokens per 32x32 image. RGB pixels are quantized with k-means clustering to produce the codebook. A GPT-2-like decoder is trained autoregressively to predict the next pixel token, and the pooled token embeddings serve as the image representation.

## Slide 3 — Train on Autoregressive Image Completions
The slide shows the autoregressive pixel-by-pixel completion task graphically: the model receives the top portion of an image and produces multiple plausible bottom completions, mirroring the way language models autoregressively continue text.

## Slide 4 — Example: ImageGPT for classification
For downstream classification the slide explains that all tokens are encoded by the pretrained ImageGPT, the token embeddings are average-pooled into a single representation, and a classification head is fit on top. This shows ImageGPT functioning both as a generative model and as a transferable feature extractor.

---

## Deck-level takeaway
ImageGPT applies the GPT-2 next-token recipe to images by treating quantized pixels as tokens and predicting them autoregressively. The result is a single decoder-only model that can both complete images and provide pooled-token embeddings that transfer to classification, demonstrating that purely generative pretraining on pixels yields useful visual representations.
