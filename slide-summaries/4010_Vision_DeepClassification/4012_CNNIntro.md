# 4012_CNNIntro — Per-Slide Summary

**Source file:** `4012_CNNIntro.pptx`
**Source folder:** `SlidesPool/4010_Vision_DeepClassification/`
**Drive link:** https://drive.google.com/file/d/1xMRqkeK6uqL9UF_lF9RHjLLGlm6hi8zw/view
**Slide count (exact, via python-pptx):** 32
**Extraction:** Local parse + slide PNG render. 14 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Convolution Neural Networks
Section divider; the deck transitions to material on convolution neural networks.

## Slide 2 — Motivation
Class probabilities of MLP on a single image. The slide includes 3 embedded images alongside the bullets.

## Slide 3 — Shifting Image: +/- 5 pixel
Almost no change in image content, the prediction class changes Need a model that is invariant to the position of content in the image: translation-invariant model. The slide includes 5 embedded images alongside the bullets.

## Slide 4 — Convolution Operation
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Convolution Operation'.

## Slide 5 — Multiple Filters
Input An image where each pixel has features RGB (3 features) or previous layers feature values Depth: number of features Filters Multiple convolution kernels Number of filters define the depth of the output. The slide includes 1 embedded image alongside the bullets.

## Slide 6 — Strides and Padding
Strides Stride 1: Move filters by one position Stride k: move by K positions Padding Can’t position filter where it’s off the input image Pad with zeroes. The slide includes 2 embedded images alongside the bullets.

## Slide 7 — Pooling
Aggregate information of a small patch Framing as a convolution with a filter. Filter size : 2, stride 2. The slide includes 1 embedded image alongside the bullets.

## Slide 8 — Low Level and High-Level Features
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Low Level and High-Level Features'.

## Slide 9 — Flatten Layer
Linearize 2D tensors. The slide includes 1 embedded image alongside the bullets.

## Slide 10 — Typical CNN architecture
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Typical CNN architecture'.

## Slide 11 — Image Translation
Convolution+ Pooling. The slide includes 2 embedded images alongside the bullets.

## Slide 12 — Receptive Field of a CNN Neuron
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Receptive Field of a CNN Neuron'.

## Slide 13 — Convolution with bias
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Convolution with bias'.

## Slide 14 — CNN Model: Toy Example
Input with depth 1, single filter. The slide includes 4 embedded images alongside the bullets.

## Slide 15 — Classifying images with CNN
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Classifying images with CNN'.

## Slide 16 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 17 — Translation-Invariance
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Translation-Invariance'.

## Slide 18 — What features the convolution kernels(filters) learn?
Example: Classify images of “0” and “X”. The slide includes 1 embedded image alongside the bullets.

## Slide 19 — Let’s examine the output of the first layer
Some learn edges(0), others invert (54). The slide includes 4 embedded images alongside the bullets.

## Slide 20 — Inspect same filter across many images
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Inspect same filter across many images'.

## Slide 21 — After the second convolution layer
Im[None]: add new dimension (batch of size 1) Same as Im.unsqueeze(0). The slide includes 2 embedded images alongside the bullets.

## Slide 22 — Activation of the single filter on different images
Second Convolution layer. Similar on different images “Learns” to detect “left half of the ‘O’. The slide includes 2 embedded images alongside the bullets.

## Slide 23 — Classifying Cats and Dogs
Section divider; the deck transitions to material on classifying cats and dogs.

## Slide 24 — Dataset
Color 224x224. The slide includes 5 embedded images alongside the bullets.

## Slide 25 — Convolution Block
Output shape : (size-2)/2. The slide includes 2 embedded images alongside the bullets.

## Slide 26 — Model Summary
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Model Summary'.

## Slide 27 — Data Preparation
Visual slide containing 5 embedded figures with no body text; the visual carries the content of the topic 'Data Preparation'.

## Slide 28 — Training Loop
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Training Loop'.

## Slide 29 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 30 — Reducing data size
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Reducing data size'.

## Slide 31 — MobileNet
CNN complexity A single kernel position: DxKxK Entire map: HxWxDxKxK Split into two operations (approximation) Single-layer convolution: HxWxKxK Pointwise convolution: HxWxD Total: HxW(KxK+D) instead HxWx (DxKxK). The slide includes 1 embedded image alongside the bullets.

## Slide 32 — MobileNet vs. Others
V2 and v3: inverted linear residuals and other tricks. The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 32 slides, opening with "Convolution Neural Networks" and closing with "MobileNet vs. Others". Body-text coverage is 50%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Image Translation, Receptive Field of a CNN Neuron, Convolution with bias, CNN Model: Toy Example.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4010_Vision_DeepClassification/4012_CNNIntro/slides/`.
