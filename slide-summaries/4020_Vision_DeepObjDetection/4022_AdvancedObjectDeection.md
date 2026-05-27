# 4022_AdvancedObjectDeection — Per-Slide Summary

**Source file:** `4022_AdvancedObjectDeection.pptx`
**Source folder:** `SlidesPool/4020_Vision_DeepObjDetection/`
**Drive link:** https://drive.google.com/file/d/1TxYRRXMDO01LQ-6ukznadqjRe3tY8Fmy/view
**Slide count (exact, via python-pptx):** 42
**Extraction:** Local parse + slide PNG render. 15 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Advanced Object Detection
Section divider; the deck transitions to material on advanced object detection.

## Slide 2 — Faster R-CNN
Section divider; the deck transitions to material on faster r-cnn.

## Slide 3 — Regional Proposal Networks
Two-step processing Regional proposals (selective search) Classifier and BB regressions R-CNN and Fast R-CNN Slow: Apply prediction to every proposal Modern architectures Faster R-NN YOLO: You Only Look Once SSDL Single-shot Detector.

## Slide 4 — Anchor Boxes
Replace selective search Typical anchor boxes Several fixed aspect ratios Several fixed scales/sizes Perform K-means clustering over ground truth Example 3 different scales 3 different aspect ratios A total of nine possible anchors centered at each pixel. The slide includes 3 embedded images alongside the bullets.

## Slide 5 — RPN: Region Proposal Network
Learnable network for proposal generation Prepare data Slide all possible anchor boxes across the image Make as an “object” if IoU with ground truth is high enough, otherwise mark as “background” Train Neural Network At each pixel, consider an anchor boxes(A=9) of different scales and aspect ratios Output at each pixel for each anchor Objectiveness score: s (or s and 1-s) Total nine boxes: 3-scales, three aspect ratios Regression refinement: 4 values Total: 9*(4+1)=45 values per pixel Filter proposals with non-maximum suppression Sort by objectiveness score Higher objective proposal “masks”/drops other overlapping proposals Keep the top N proposals, N=200 or N=300. The slide includes 1 embedded image alongside the bullets.

## Slide 6 — FPN: Feature Pyramid Network
Apply RPN at different scales efficiently Need to align backbone feature maps to the same depth/semantic. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — FPN: Architecture
Learn multiscale feature maps Repeatedly up-sample (2x) and merge with the original Run 256 1x1 convolution kernels on ResNet Feature Maps Add up-sampled and projected feature maps Additional 3x3 kernel mixture. The slide includes 2 embedded images alongside the bullets.

## Slide 8 — RoI Align vs. RoI Pool
ROI Pool Round coordinates Max Pool for each bin ROI Align Sample 4 points Interpolate their values from the closest features Average [pooling for a single number per bin Still produces the tensors of the same dimension (7x7x512). The slide includes 1 embedded image alongside the bullets.

## Slide 9 — Classification and Regression Heads
Second stage Consider certain (score>0.7) refined proposal ROI Align RoI from the appropriate feature map Classifier: predict N+1 labels (still allow background) Regression: refine the anchor box ROI with offset. The slide includes 1 embedded image alongside the bullets.

## Slide 10 — Faster R-CNN
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Faster R-CNN'.

## Slide 11 — Step-By-Step forward pass for each image
RPN: class agnostic scoring and offset RoI head: class-specific scoring and offset.

## Slide 12 — Train Faster R-CNN on a custom dataset
Section divider; the deck transitions to material on train faster r-cnn on a custom dataset.

## Slide 13 — Detecting buses and trucks
Open Images Bus-Trucks subset. The slide includes 1 embedded image alongside the bullets.

## Slide 14 — Dataset Class
Dataset/sample slide containing 5 figures that visualise the data used at this point of the project pipeline.

## Slide 15 — Define Model
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Define Model').

## Slide 16 — Normalization Transform
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Normalization Transform'.

## Slide 17 — Region Propose Network
Bbox_pred: 3 anchor boxes(aspect ratios) with four coordinates each, 12 outputs cls_logits: single objectiveness score for three anchor boxes Apply to each pixel on each resolution. The slide includes 1 embedded image alongside the bullets.

## Slide 18 — ROI Heads
Process top proposals in a batch Proposals are represented using ROI Align Linear layer with ReLU for each output type For each proposal Predict three classes: buses vs. trucks vs. background: 00,01,10 Each object class has its box regression: 8 values. The slide includes 1 embedded image alongside the bullets.

## Slide 19 — Trainingprep
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Trainingprep'.

## Slide 20 — Train Loop
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Train Loop'.

## Slide 21 — Training results
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Training results'.

## Slide 22 — Predict on new image
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Predict on new image'.

## Slide 23 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 24 — YOLO
Section divider; the deck transitions to material on yolo.

## Slide 25 — Limitations of Faster R-CNN
Faster R-CNN has two networks Few passes over an image (multiscale FPN) to produce proposals Batched proposal predictions with RoI aligned features RoI Head sometimes needs to guess boundaries without complete information RPN class agnostic ROI offset prediction might not contain the entire object.

## Slide 26 — Yolo: You Only Look Once
Divide the image into a grid and identify cells that have at least one center of GT BB These cells are responsible for predicting BB of the object Normalize cell coordinate to (0,1). The slide includes 2 embedded images alongside the bullets.

## Slide 27 — Expected output of the cell prediction (GT)
For now, assume a single or no objects per cell PC: Objectness score bx, by: coordinates of BB centers within the cell Center of the cell is 0.5, 0.5 bw, bh: BB size, relative to cell size, width and height c1-c3: class logits vector N+1 values Total: 8 values per cell. The slide includes 1 embedded image alongside the bullets.

## Slide 28 — Example
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Example'.

## Slide 29 — Model: Sample Architecture
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Model: Sample Architecture'.

## Slide 30 — Prediction
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Prediction'.

## Slide 31 — Multiple objects per cell
Define a fixed number of anchor boxes Example: 3 scales and three aspect ratios For each prediction, eight values Predict offsets from the anchor box Total predictions for each cell B boxes Center, dimension, and objectiveness score for each box YoloV3:Class prediction for each box Total: B*(5+C). Ground Truth. The slide includes 2 embedded images alongside the bullets.

## Slide 32 — YOLO v2: Architecture
YOLO v2 defaults: 416x416 image 13-by-13 grid, five anchors, shared classes for call anchors: 20 classes(Pascal VOC): 13x13*5*(5+20)=13x13x125. The slide includes 2 embedded images alongside the bullets.

## Slide 33 — Loss Function
Do not calculate regression loss and classification loss when objectiveness loss is below the threshold If object Ensure correct classification Ensure correct offset prediction BB loss The center is limited by the cell size, small Width/Height is not limited, might be large. Use their square root.

## Slide 34 — Loss Function
B- number of anchors S-greed size. The slide includes 2 embedded images alongside the bullets.

## Slide 35 — YOLO Evaluation on COCO
MAP@05:0.95 Compute average precision at IoU thresholds 0.5 to 0.95 in steps of 0.05 Take the mean. The slide includes 1 embedded image alongside the bullets.

## Slide 36 — Darknet and Ultralytics
C/CUDA based DNN framework created for YOLO Different from PyTorch Ultralytics YOLO and other models implemented in PyTorch.

## Slide 37 — Training YOLO in Ultralytics
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Training YOLO in Ultralytics'.

## Slide 38 — SSD: Single Shot Detection
Section divider; the deck transitions to material on ssd: single shot detection.

## Slide 39 — SSD
YOLO v2 : Final head predicts cell BBs from the same feature map For small objects, use a fine grid: 26x26 For large objects, use a coarse grid 13x13 SSD Detect from multiple feature maps Add convolution layers over the backbone. The slide includes 1 embedded image alongside the bullets.

## Slide 40 — Multibox Loss
Total 8732 anchor boxes. The slide includes 3 embedded images alongside the bullets.

## Slide 41 — SSD Components
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'SSD Components'.

## Slide 42 — Since YOLO v5 : Multiscale Prediction
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Since YOLO v5 : Multiscale Prediction'.

---

## Deck-level takeaway
The deck spans 42 slides, opening with "Advanced Object Detection" and closing with "Since YOLO v5 : Multiscale Prediction". Body-text coverage is 52%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Define Model, Normalization Transform, Region Propose Network, ROI Heads.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4020_Vision_DeepObjDetection/4022_AdvancedObjectDeection/slides/`.
