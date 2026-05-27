# 4021_BasicsOfObjectDetection — Per-Slide Summary

**Source file:** `4021_BasicsOfObjectDetection.pptx`
**Source folder:** `SlidesPool/4020_Vision_DeepObjDetection/`
**Drive link:** https://drive.google.com/file/d/1Apy1qF-_sipbfx4hcW0zZ2Bg_jvdqZxy/view
**Slide count (exact, via python-pptx):** 33
**Extraction:** Local parse + slide PNG render. Many implementation slides are code-screenshot-only; their content is inferred from titles + surrounding prose.

---

## Slide 1 — Basics of Object Detection
Title slide for the lecture that walks from classical region-proposal-based detection through R-CNN and Fast R-CNN.

## Slide 2 — Object Detection Tasks
Defines the task in one line: *localize* (find where) and *identify* (find what) objects in an image. The diagram shows a typical detection output with bounding boxes and class labels.

## Slide 3 — Creating labels: class labels and bounding boxes
Diagram of the supervision signal: each ground-truth object is annotated with a bounding box (x, y, w, h) and a class label.

## Slide 4 — Regional Proposals
The classical decomposition. A *region proposal* is a candidate window where an object might be. Detection then becomes: propose, refine, classify. The naive proposal algorithm — slide a window over all possible locations at all scales — produces a huge number of candidates, motivating smarter proposers.

## Slide 5 — Selective Search
The dominant pre-deep proposal algorithm. Group pixels by similarity in color, texture, and size; start from an over-segmented image and gradually merge similar segments; add salient regions as proposals at different merge levels. Stop when there's a manageable number of proposals (~2K). The same pixels can appear in many proposals.

## Slide 6 — Felzenszwalb Segmentation
The graph-based segmentation underneath selective search. Nodes are pixels connected to their neighbors; edge weights are the difference in intensity/color. Combine pixels greedily into segments, controlled by a per-segment "internal variation" threshold. Four diagrams show the merge process.

## Slide 7 — Selective Search (in practice)
Code walkthrough (seven screenshots) using the `selectivesearch` Python library, which packages both the Felzenszwalb segmentation and the rectangular bounding-box construction.

## Slide 8 — IoU: Intersection over Union
The detection accuracy metric. IoU = (area of intersection) / (area of union) between two bounding boxes — used to measure both proposal quality (how close to a ground-truth box) and prediction accuracy.

## Slide 9 — Non-max suppression
Post-processing for detection. Multiple proposals often overlap significantly on the same object. The fix: sort by classification confidence, keep the highest-confidence box, discard all others with IoU above a threshold (typically 0.5), repeat. Three diagrams show the suppression in action.

## Slide 10 — mAP: Mean Average Precision
The detection-wide accuracy metric. For each class compute *average precision*: a predicted box is a true positive if it has the correct class and sufficient IoU with a ground-truth box (one true positive allowed per GT box); other boxes are false positives. *mAP* averages this across all classes. Standard detection benchmark.

## Slide 11 — R-CNN
Section divider before the first deep-learning detector.

## Slide 12 — R-CNN: Region-Based CNN
The architecture. Take a pretrained classifier (VGG, ResNet), feed it the warped region proposals (so each proposal is resized to the network's standard input size), and add two output heads: one for object/background class prediction, one for bounding-box offset refinement from the proposal.

## Slide 13 — Google Open Images
The dataset used in the walkthrough. Annotations use *relative* coordinates for bounding boxes — a small but important detail because resizing the image changes pixel coordinates but not relative ones. Three example screenshots.

## Slide 14 — Images Dataset Class
Code (three screenshots) for the PyTorch `Dataset` class that yields (image, list-of-boxes, list-of-labels) tuples from Open Images.

## Slide 15 — Extract Candidates Regions
Code screenshot wrapping the selective-search call to produce region proposals per image.

## Slide 16 — Compute IoU
Code screenshot of an IoU helper that scores each proposal against each ground-truth box.

## Slide 17 — Create training data
The labeling step. Run selective search; for each proposal, compute IoU against all ground-truth boxes; assign the proposal a class label if IoU > threshold, else "background"; compute the offset between the proposal and the matching ground-truth box for the regression head. Two screenshots.

## Slide 18 — Region dataset class
Code (four screenshots) for the `Dataset` class that yields (region image, class label, box offset) tuples for training.

## Slide 19 — R-CNN Network
The model. Backbone: VGG16. Two heads: a linear+sigmoid layer for class prediction, four scalar outputs for box offsets.

## Slide 20 — Load Backbone
Code screenshot loading a pretrained VGG16 backbone in PyTorch.

## Slide 21 — RCNN Model
The full model definition (five code screenshots): backbone + classification head + regression head + the forward pass.

## Slide 22 — Loss Calculation
The multitask loss. Classification loss is computed on all proposals. Regression loss is computed only for non-background proposals (no box to refine if there's nothing there). The two losses are combined with a weighting factor λ.

## Slide 23 — Training
The training loop (five code screenshots): standard PyTorch with the loss from slide 22.

## Slide 24 — Dataset: Bus vs. Trucks
The toy training task used for the demo: a binary classification subset of Open Images (buses vs. trucks).

## Slide 25 — Results
A qualitative result image showing detected boxes on a test image.

## Slide 26 — Inference
The full inference pipeline (six code screenshots): run selective search on the test image, classify and regress each proposal, threshold by confidence, run non-max suppression, draw boxes.

## Slide 27 — Fast R-CNN
Section divider before the speed-improved variant.

## Slide 28 — R-CNN prediction is slow
The diagnosis. R-CNN runs the CNN backbone *once per proposal*, so for 2000 proposals you do 2000 forward passes. *Fast R-CNN* runs the backbone *once for the whole image* and then fetches the right region of the feature map per proposal — at the cost of some spatial resolution.

## Slide 29 — ROI Pool Layer
The component that makes Fast R-CNN work. Input: a feature map (e.g., 512 × 14 × 14) and a variable-size region of interest. Algorithm: map the ROI to pixel coordinates; divide it into a fixed bin grid (e.g., 7×7); translate each bin's pixel coordinates into feature-map coordinates by dividing by the scaling factor; max-pool the feature map within each bin. Output is a *fixed-size* tensor regardless of ROI size — which is what lets the downstream heads work.

## Slide 30 — FRCNN Network
Code (eight screenshots) for the Fast R-CNN model definition: backbone + ROI pool + heads.

## Slide 31 — Fast R-CNN: Cont'd
Continuation slide (one diagram) — probably the data flow through the ROI-pooling-based network.

## Slide 32 — Training
Code screenshot showing the Fast R-CNN training loop adapted from R-CNN.

## Slide 33 — Results
Closing comparison (two screenshots): Fast R-CNN results on the bus-vs-truck task, with the prediction-time speedup over R-CNN as the headline.

---

## Deck-level takeaway

A 33-slide constructive walkthrough of two-stage object detection, from the classical pre-deep-learning ingredients (Felzenszwalb segmentation → selective search → IoU → non-max suppression → mAP) through R-CNN (use a CNN to classify and refine each proposal) and onward to Fast R-CNN (one CNN pass per image + ROI pooling to crop the feature map). The pedagogical signature is *theory + working PyTorch code for every step* — there are ~40 code screenshots across the deck, so the reader can reproduce both detectors end-to-end on the Bus-vs-Trucks subset of Open Images. The narrative is "build the slow honest version first, see why it's slow, then engineer the cheap version".
