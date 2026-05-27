# 4015_CNN-Manipulations — Per-Slide Summary

**Source file:** `4015_CNN-Manipulations.pptx`
**Source folder:** `SlidesPool/4010_Vision_DeepClassification/`
**Drive link:** https://drive.google.com/file/d/1Mmv3sKYToGmamdsKwxrW-sbO3jdzTuld/view
**Slide count (exact, via python-pptx):** 17
**Extraction:** Local parse + slide PNG render. 8 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image Manipulation
Section divider; the deck transitions to material on image manipulation.

## Slide 2 — Adversary Attack
Section divider; the deck transitions to material on adversary attack.

## Slide 3 — Adversary Attacks
Changes to make to the image to meet a specific objective Usually, slight, invisible changes Undisguisable by the human eye Usually, fool a pre-trained model Make a model to classify an image into a target class Recipe Freeze classification model parameters Consider image values as trainable parameters Backpropagate for minimizing target loss.

## Slide 4 — Prepare model
Dataset/sample slide containing 1 figure that visualise the data used at this point of the project pipeline.

## Slide 5 — Normalize image
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Normalize image'.

## Slide 6 — Predict on image
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Predict on image'.

## Slide 7 — Attack function
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Attack function'.

## Slide 8 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 9 — Neural Style Transfer
Section divider; the deck transitions to material on neural style transfer.

## Slide 10 — Neural Style Transfer
Input Content image, Style Image Output: preserve content, transfer style. The slide includes 2 embedded images alongside the bullets.

## Slide 11 — Gram Matrix
Measure similarity between vectors based on dot product Multiplication of matrix by its transpose Gram matrix on low-level feature maps Each channel encodes certain visual aspect High values for channels that are activated together Capture texture and patterns. The slide includes 2 embedded images alongside the bullets.

## Slide 12 — Target Loss using base model (VGG16)
Content loss Difference in content between input image and the target Difference in feature map activations of the underlying model Style loss Correlation between style image and he targets For l feature maps. The slide includes 1 embedded image alongside the bullets.

## Slide 13 — Style Loss
Div_: in-place division. The slide includes 2 embedded images alongside the bullets.

## Slide 14 — Model
Return intermediate feature maps. The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Prepare Image
Dataset/sample slide containing 6 figures that visualise the data used at this point of the project pipeline.

## Slide 16 — Optimization
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Optimization'.

## Slide 17 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

---

## Deck-level takeaway
The deck spans 17 slides, opening with "Image Manipulation" and closing with "Results". Body-text coverage is 35%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Predict on image, Attack function, Results, Neural Style Transfer.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4010_Vision_DeepClassification/4015_CNN-Manipulations/slides/`.
