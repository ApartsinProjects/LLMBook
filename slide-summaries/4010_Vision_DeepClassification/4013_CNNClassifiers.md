# 4013_CNNClassifiers — Per-Slide Summary

**Source file:** `4013_CNNClassifiers.pptx`
**Source folder:** `SlidesPool/4010_Vision_DeepClassification/`
**Drive link:** https://drive.google.com/file/d/1PmyvJdDkgqixZiWpXc5D6uwtWXaGU6iK/view
**Slide count (exact, via python-pptx):** 41
**Extraction:** Local parse + slide PNG render. 20 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Transfer Learning for Image Classification
Section divider; the deck transitions to material on transfer learning for image classification.

## Slide 2 — Transfer Learning
Previous examples Need a large training dataset Not always available Transfer Learning Train the model on a large, generic dataset Fine-tune to a specific dataset/task. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — ImageNet
14M images, 1000 classes Train classifiers and reuse their layers for a specific task Add additional layers of task-specific classification head. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — Transfer Learning: the recipe
Normalize task input images to the same mean and std used fro the training of the pretrained model Fetch pretrained model architecture and load it with pretrained weights Discard the last few layers and add task-specific layers to be trained Freeze all other layers of the model Update trainable parameters of the last layers.

## Slide 5 — VGG16
Pretrained model.

## Slide 6 — VGG16 Architecture (2014, Oxford)
5 blocks of convolution, Conv 1-2: second convolution in block 1. The slide includes 4 embedded images alongside the bullets.

## Slide 7 — VGG16: Architecture
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'VGG16: Architecture'.

## Slide 8 — Include normalization in the dataset class
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Include normalization in the dataset class'.

## Slide 9 — Adaptive Average Pooling
Fixed Kernel size pooling MaxPool2D: Maximum Pooling AvgPool2D: Average Pooling Adaptive pooling Specify the output dimension instead Kernel size is computed automatically.

## Slide 10 — Add new layers
Replace the last average pooling Had output 512 x 7 x 7, now will be 521 x 1 x 1. Replace classifier module. The slide includes 3 embedded images alongside the bullets.

## Slide 11 — Training
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Training'.

## Slide 12 — Results:98% validation accuracy
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 13 — VGG16 Variants
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'VGG16 Variants'.

## Slide 14 — ResNet
Pretrained models.

## Slide 15 — Vanishing Gradient Problem
The gradients for earlier layers are computed using the chain rule The last few layers have no information on the input image, and gradients might be small Multiplication of small gradients almost zeros out the gradient of the first layers. The slide includes 2 embedded images alongside the bullets.

## Slide 16 — Residual Connection
Need padding so the dimensions of input and output will be equivalent for sum. The slide includes 4 embedded images alongside the bullets.

## Slide 17 — 1x1 Convolution : Projection
Change the number of channels/depth. The slide includes 1 embedded image alongside the bullets.

## Slide 18 — ResNet18 Architecture
18 layers, dotted residuals include projections to adapt depth \2 is stride 2, residual connection between same dimensions. The slide includes 1 embedded image alongside the bullets.

## Slide 19 — Implementation
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Implementation'.

## Slide 20 — ResNet Variants
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'ResNet Variants'.

## Slide 21 — Facial Keypoint Detection
Section divider; the deck transitions to material on facial keypoint detection.

## Slide 22 — Previously
Binary classification: Dogs vs. Cats Multilabel Classification: Fashion-MNIST Next: Mult regression learning Predict several continuous outputs.

## Slide 23 — Facial keypoints
Fixed reference landmarks for the face Popular 68 landmark schemes Required for face detection and alignment. The slide includes 1 embedded image alongside the bullets.

## Slide 24 — Dataset
Image + 68 key point coordinates Even column: x-coordinate Odd columns : y-coordinate. The slide includes 1 embedded image alongside the bullets.

## Slide 25 — Normalization
Resize all images to 224 x 224 x 3 Normalize keypoint coordinate to 0..1 Sigmoid output layer (as in previous binary classification) Optimize L1 loss function (instead of BCE) Error function is equal to loss function. The slide includes 1 embedded image alongside the bullets.

## Slide 26 — Dataset
Dataset/sample slide containing 10 figures that visualise the data used at this point of the project pipeline.

## Slide 27 — Data Preparation
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Data Preparation'.

## Slide 28 — VGG16-based Model
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'VGG16-based Model'.

## Slide 29 — Results
Results slide with 2 screenshots showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 30 — Pretrained facial keypoints model
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Pretrained facial keypoints model'.

## Slide 31 — 3D Keypoint Prediction
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic '3D Keypoint Prediction'.

## Slide 32 — Age estimation and Gender Classification
Multi-task leraning.

## Slide 33 — Multitask  learning
Predict output for two related tasks simultaneously Autonomous task: identify obstacles, plan routes, and control brakes/steering This example Estimate the age and gender of a person from an image Gender classification accuracy Age mean absolute error (L1).

## Slide 34 — Data
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Data'.

## Slide 35 — Dataset Class
Dataset/sample slide containing 3 figures that visualise the data used at this point of the project pipeline.

## Slide 36 — Collate function for data loader
Batch individual records into tensors. Probably could use default collate function. The slide includes 4 embedded images alongside the bullets.

## Slide 37 — Prepare the classifier to replace
Dataset/sample slide containing 4 figures that visualise the data used at this point of the project pipeline.

## Slide 38 — Load Pretrained Model
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Load Pretrained Model').

## Slide 39 — Training
Visual slide containing 6 embedded figures with no body text; the visual carries the content of the topic 'Training'.

## Slide 40 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 41 — Example
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Example'.

---

## Deck-level takeaway
The deck spans 41 slides, opening with "Transfer Learning for Image Classification" and closing with "Example". Body-text coverage is 46%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include ResNet, Vanishing Gradient Problem, Residual Connection, 1x1 Convolution : Projection.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4010_Vision_DeepClassification/4013_CNNClassifiers/slides/`.
