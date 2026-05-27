# 4032_ImageSegmentation — Per-Slide Summary

**Source file:** `4032_ImageSegmentation.pptx`
**Source folder:** `SlidesPool/4030_Vision_DeepSegmentation/`
**Drive link:** https://drive.google.com/file/d/1873z0dDMkG5_-hMMbc_PYI9JjkmMH4Bi/view
**Slide count (exact, via python-pptx):** 25
**Extraction:** Local parse + slide PNG render. 8 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image Segmentation
Section divider; the deck transitions to material on image segmentation.

## Slide 2 — Segmentation vs. Object Detection
Object detection Bounding box and class label Segmentation Identify exact pixels belonging to an object Semantic segmentation: label pixels by a class: tree, car Instance segmentation: label pixels by an object: tree_1, tree_2. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — U-Net Architecture
Section divider; the deck transitions to material on u-net architecture.

## Slide 4 — U-Net
Pixlel2Piexl tasks Input and output have the same dimensions Might have a different number of channels Per-class pixel logits Operation Convolution Upscaling Skip-connection Stacking. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Upscaling
Transposed Convolution Stride and pad input array, convolve with learnable kernel. The slide includes 3 embedded images alongside the bullets.

## Slide 6 — Segmentation with U-Net
Semantic Segmentation.

## Slide 7 — Semantic Segmentation
Per-class pixel labels. The slide includes 1 embedded image alongside the bullets.

## Slide 8 — Data Preparation
12 different classes Mask: single channel image, class ID. The slide includes 6 embedded images alongside the bullets.

## Slide 9 — Define Convolution/Up-Conv block
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Define Convolution/Up-Conv block').

## Slide 10
Pretrained VGG16 is used for encoding layers. The slide includes 3 embedded images alongside the bullets.

## Slide 11 — Train
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Train'.

## Slide 12 — Results
Results slide with 2 screenshots showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 13 — Mask R-CNN
Instance Segmentation.

## Slide 14 — Mask R-CNN
Extension of Faster R-CNN Add mask prediction head Mask for each region Fixed mask size (28x28) for each output BB For each predicted class, foreground/background logits A probability for a pixel belong to object (after sigmoid). The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Mask Head
Res5: stage 5 or ResNet backbone. The slide includes 1 embedded image alongside the bullets.

## Slide 16 — FCN: Fully Convolutional Network
Produce dense output Does not include fully connected layers Might use a transpose convolution layer Might use other layers: dropout, normalization, activation, pooling Might use 1x1 convolution for flattening channels Arbitrary input size. The slide includes 2 embedded images alongside the bullets.

## Slide 17 — Mask head with FCN
Produces a mask of fixed size: 28x28xClasses. The slide includes 1 embedded image alongside the bullets.

## Slide 18 — Dataset: ADE20K: Instance Segmentation
Mask has two channels: class _id(red) and instance_id(green). We will focus on people in the following example. The slide includes 3 embedded images alongside the bullets.

## Slide 19 — Dataset class
Dataset/sample slide containing 10 figures that visualise the data used at this point of the project pipeline.

## Slide 20 — Data Prep
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Data Prep'.

## Slide 21 — Prepare Model
Dataset/sample slide containing 3 figures that visualise the data used at this point of the project pipeline.

## Slide 22 — Model Structure
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Model Structure'.

## Slide 23 — Prediction
The model is hardcoded to return 100 predictions(not Labels are 0/1 human or others. Masks(28x28) are resized to the image dimensions. The slide includes 2 embedded images alongside the bullets.

## Slide 24 — Results
Results slide with 2 screenshots showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 25 — Extending to multiple classes
Multiple instances of person (ID 4) and Table(ID 5). The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 25 slides, opening with "Image Segmentation" and closing with "Extending to multiple classes". Body-text coverage is 60%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Define Convolution/Up-Conv block, Train, Results, Mask R-CNN.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4030_Vision_DeepSegmentation/4032_ImageSegmentation/slides/`.
