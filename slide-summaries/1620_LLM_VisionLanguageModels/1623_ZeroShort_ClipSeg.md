# 1623_ZeroShort_ClipSeg — Per-Slide Summary

**Source file:** `1623_ZeroShort_ClipSeg.pptx`
**Source folder:** `SlidesPool/1620_LLM_VisionLanguageModels/`
**Drive link:** https://drive.google.com/file/d/1AY6JzzFQ4lrQQu_Sw3n2AxY6ZyJCHIvB/view
**Slide count (exact, via python-pptx):** 9
**Extraction:** Local parse + slide PNG render. Bullets describe the FiLM conditioning trick that enables zero-shot segmentation on CLIP features.

---

## Slide 1 — ClipSeg
Title slide; sub-title "Zero-shot segmentation model".

## Slide 2 — Object Background Segmentation
ClipSeg produces a segmentation mask image conditioned on either a text query ("a horse") or an image query ("an object like this").

## Slide 3 — Text-Guided Segmentation
A figure illustrating text-guided segmentation of an image.

## Slide 4 — Detect object by text/image prompt
The decoder predicts a segmentation mask of the query image given the prompt.

## Slide 5 — Background Feature-Wise Linear Modulation (FiLM)
FiLM conditions every decoder layer by linearly transforming the feature map with a learned scale and shift, applied to each channel independently. The scale and shift are produced as a learned function of the conditioning signal (the text or image embedding).

## Slide 6 — ClipSEG
The full ClipSeg model is encoder-decoder. Every image patch embedding is conditioned with the text prompt via FiLM, and skip connections link the visual encoder to the decoder. The output is a single image-size binary segmentation mask.

## Slide 7 — Example: Segment by Text Prompt
Four screenshots demonstrating segmentation driven by a text prompt.

## Slide 8 — Results
A figure of segmentation results.

## Slide 9 — Segment by image prompt
Five screenshots demonstrating segmentation driven by an image prompt instead of text.

---

## Deck-level takeaway
ClipSeg adds zero-shot segmentation to CLIP by attaching an encoder-decoder where every decoder layer is conditioned on the CLIP-encoded prompt via FiLM (Feature-wise Linear Modulation): a learned scale and shift per channel. The prompt can be either text ("a horse") or an example image, and skip connections from the visual encoder preserve spatial detail through the decoder, yielding a single binary image-size mask without segmentation-specific labels for the target class.
