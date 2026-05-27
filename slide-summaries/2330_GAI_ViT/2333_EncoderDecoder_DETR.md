# 2333_EncoderDecoder_DETR — Per-Slide Summary

**Source file:** `2333_EncoderDecoder_DETR.pptx`
**Source folder:** `SlidesPool/2330_GAI_ViT/`
**Drive link:** https://drive.google.com/file/d/1ITUcjl7cuIBcTMF9VgL7H4P-RxrjQ00s/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render. Title/header slides (1, 2, 8) and pure-image slides (6, 7, 9, 12, 13) were visually inspected.

---

## Slide 1 — Vision Encoder-Decoder Transformers
Title slide introducing DETR (Detection Transformer) as the canonical vision encoder-decoder transformer.

## Slide 2 — Detection Transformer for Object Detection
Section header that transitions from background to the DETR object-detection pipeline.

## Slide 3 — Object Detection with DeTR
The slide describes the DETR architecture as a transformer encoder-decoder operating on top of a CNN backbone. The CNN reduces the image to a (H/32)x(W/32) feature map with C=2048 channels, which the encoder processes. The decoder consumes learned object queries (slots that act as placeholders for "top-left animals" or similar search criteria) and attends to the encoder output via cross-attention to produce a bounding box and class probability vector per query.

## Slide 4 — Background: Hungarian Matching
DETR uses Hungarian matching to assign predictions to ground-truth boxes during training. The slide visually defines the bipartite-matching problem of finding the best pairing between two sets of objects so that a permutation-invariant loss can be computed.

## Slide 5 — Object Queries
Object queries are described as 100 learned vectors that act as detection slots. Predictions are aligned to ground-truth boxes via Hungarian matching, and the loss is the best-match cost between predictions and labels. Unused slots are trained to predict the "no object" class.

## Slide 6 — Example
The slide shows worked DETR detections, with bounding boxes drawn for several object queries on natural images and the "no object" slots producing nothing.

## Slide 7 — Results
A gallery of DETR outputs on COCO-style images demonstrates that the model handles cluttered scenes and small objects without anchor boxes or non-maximum suppression.

## Slide 8 — DETR for Segmentation
Section header that introduces the segmentation extension of DETR, where pixel-level masks are predicted per detected object.

## Slide 9 — Semantic Segmentation
The slide visually motivates the segmentation task, showing pixel-wise class labels and noting that DETR can be extended to produce one mask per detected query.

## Slide 10 — Background: Feature Pyramid Networks (FPN)
FPN combines multiple CNN layers to produce multi-scale features: low-level layers carry high resolution with fine details, while upper layers carry low resolution with semantic content. DETR's segmentation head reuses this multi-scale idea.

## Slide 11 — Add Mask Prediction Head
The slide describes the mask head. Each object query's embedding is reshaped into a 2D feature map, stacked with the original image features, and upscaled while being enriched with backbone features. Cross-attention enforces global consistency across object masks. Each pixel inside an object's attention map is classified as foreground or background, yielding 100 candidate masks.

## Slide 12 — Semantic Segmentation with DETR
The slide shows four example outputs of the segmentation pipeline, producing tight per-instance masks plus the implicit semantic-segmentation map that arises from aggregating them.

## Slide 13 — Results
A final panel reports DETR-segmentation visualizations on natural scenes with overlaid masks.

---

## Deck-level takeaway
DETR reframes object detection as a set prediction problem: a CNN-encoded image plus 100 learned object queries pass through a transformer encoder-decoder, producing a fixed-size set of (box, class) predictions matched to ground truth by Hungarian assignment. This anchor-free design extends naturally to segmentation by attaching a mask head that turns each query's embedding into a per-object pixel mask, with FPN-style multi-scale features sharpening boundaries.
