# 4014_CNNVisualizations — Per-Slide Summary

**Source file:** `4014_CNNVisualizations.pptx`
**Source folder:** `SlidesPool/4010_Vision_DeepClassification/`
**Drive link:** https://drive.google.com/file/d/1vz68D86rQYrB_hnKNbhSPvp2L5Snv2GC/view
**Slide count (exact, via python-pptx):** 26
**Extraction:** Local parse + slide PNG render. 9 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Practical Aspects of Image Classification
Section divider; the deck transitions to material on practical aspects of image classification.

## Slide 2 — CAM: Class Activation Maps
Understand why the trained model predicts classes What pixels were used in making predictions. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Computing Grad-CAM
Intermediate feature maps/activation Shape: n-channels x height x weight Average: activation for all images Class-specific activations of a convolution layer Some are activated for both classes Some are activated but not used for the decision Find features that are responsible for the class decision Compute the gradient with respect to the “cat” class High gradient only to features that affect the decision.

## Slide 4 — CAM: Step 1
Select the class and target convolution layer Class: “Cat”, a convolution layer with Input: 256 features, 512 filters Kernel size : 256 x 3 x 3 Output: 512 x 7 x 7 Total parameters: 256 x 512x 3 x 3. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — CAM Step 2,3:
Compute the layer activations Compute the gradient of layer parameter with respect class score Output gradient shape is: 256 x 512 x 3 x 3. The slide includes 1 embedded image alongside the bullets.

## Slide 6 — CAM : Step 4
Compute the mean of the gradients with each channel Output: vector of size 512 Average importance of each channel. The slide includes 2 embedded images alongside the bullets.

## Slide 7 — CAM : Step 5
Computed weighted activation map Multiply gradient mean with the activation feature map. Gradients provide class-specific importance, activation where the features are. The slide includes 2 embedded images alongside the bullets.

## Slide 8 — CAM : Step 6,7,8
Compute the mean across channels Resize upscale to the original image size Overlay image and CAM. The slide includes 2 embedded images alongside the bullets.

## Slide 9 — Overall
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Overall'.

## Slide 10 — CAM Implementation
Section divider; the deck transitions to material on cam implementation.

## Slide 11
Detect malaria infection. The slide includes 3 embedded images alongside the bullets.

## Slide 12 — Dataset Class
Dataset/sample slide containing 3 figures that visualise the data used at this point of the project pipeline.

## Slide 13 — Model
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Model'.

## Slide 14 — Training
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Training'.

## Slide 15 — Grad-CAM
Fetch the first four blocks and the first convolution layer of the 5th block Fetch the activation map and compute gradients. 6 layers back in the sequential module list, and we get to the convolution layer. The slide includes 3 embedded images alongside the bullets.

## Slide 16 — Multiply, aggregate across channels
Up-sample and overlay. The slide includes 2 embedded images alongside the bullets.

## Slide 17 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 18 — Sign Classification
Impact of data augmentation and batch normalization.

## Slide 19 — German Signs
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'German Signs'.

## Slide 20 — Transformation without augmentation
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Transformation without augmentation'.

## Slide 21 — Model
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Model'.

## Slide 22 — Training
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Training'.

## Slide 23 — Results: Ablation Study
Batch norm increase training power/accuracy, Augmentation reduces overfitting. The slide includes 1 embedded image alongside the bullets.

## Slide 24 — Best Practices for Image Classification
Section divider; the deck transitions to material on best practices for image classification.

## Slide 25 — Imbalanced data
Select appropriate accuracy metrics Assign higher weights to samples from rare classes in the loss function Oversample for a rare class Augment data and use transfer learning. The slide includes 1 embedded image alongside the bullets.

## Slide 26 — Small objects
A small patch in the image might dictate the entire image class Use object detection techniques Divide the image into a 10-by-10 grid and classify each cell. The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 26 slides, opening with "Practical Aspects of Image Classification" and closing with "Small objects". Body-text coverage is 54%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Overall, CAM Implementation, Dataset Class, Model.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4010_Vision_DeepClassification/4014_CNNVisualizations/slides/`.
