# 4011_MLPClassifier — Per-Slide Summary

**Source file:** `4011_MLPClassifier.pptx`
**Source folder:** `SlidesPool/4010_Vision_DeepClassification/`
**Drive link:** https://drive.google.com/file/d/1m9P19NmpCJUIm0dQSxMwQMII0aucphvL/view
**Slide count (exact, via python-pptx):** 32
**Extraction:** Local parse + slide PNG render. 14 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Deep Neural Network for Image Classification
Section divider; the deck transitions to material on deep neural network for image classification.

## Slide 2 — Traditional Computer Vision
Feature-based algorithms. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Deep Neural Networks
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Deep Neural Networks'.

## Slide 4 — Example: Fashion-MNIST
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Example: Fashion-MNIST'.

## Slide 5 — Create a dataset and data loader  class
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Create a dataset and data loader  class').

## Slide 6 — Prepare model, loss, optimizer
Fully connected layer with ReLU activation. The slide includes 4 embedded images alongside the bullets.

## Slide 7 — Processing a single batch
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Processing a single batch'.

## Slide 8 — Calculate Prediction Accuracy
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Calculate Prediction Accuracy'.

## Slide 9 — Training loop
Visual slide containing 9 embedded figures with no body text; the visual carries the content of the topic 'Training loop'.

## Slide 10 — Training Progress
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Training Progress'.

## Slide 11 — Scaling the images
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Scaling the images'.

## Slide 12 — Why scaling help
Small changes in model weights now result in a considerable change in the output Exponent of very large negative numbers are almost zero. The slide includes 2 embedded images alongside the bullets.

## Slide 13 — Adding validation data and validation loss
Visual slide containing 5 embedded figures with no body text; the visual carries the content of the topic 'Adding validation data and validation loss'.

## Slide 14 — Training Results
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Training Results'.

## Slide 15 — Batch size of 10000
Loss does not reach the same level as batch 32 Model weights are updated fewer times per epoch. The slide includes 1 embedded image alongside the bullets.

## Slide 16 — Loss optimizer: Adaptive Movements
Adapt learning rate to each parameters and use moment. The slide includes 2 embedded images alongside the bullets.

## Slide 17 — Model Architectures: 0,1,2 hidden layers
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Model Architectures: 0,1,2 hidden layers'.

## Slide 18 — Training results
Underfit, training loss is stuck around 0.3. Overfit, training loss around 0.1, validation loss above 0.5. The slide includes 3 embedded images alongside the bullets.

## Slide 19 — Batch Normalization
Very small input values, the exponential function change only slightly with model weight change. The slide includes 2 embedded images alongside the bullets.

## Slide 20 — Batch Normalization
Normalize value across batch. The slide includes 4 embedded images alongside the bullets.

## Slide 21 — Batch Normalization: Inference
State Learnable parameters Satet variables, moving average of mean and variance during training Single sample inference. The slide includes 1 embedded image alongside the bullets.

## Slide 22 — Order of placement
Two options: before and after activation. The slide includes 1 embedded image alongside the bullets.

## Slide 23 — Toy example: Make input data very small
Model returns two outputs: hidden activations and output layer values. The slide includes 2 embedded images alongside the bullets.

## Slide 24 — Result
Model does not train. Most of the weights are zero or very large to account for small inputs. Leaning requires large weights updates. The slide includes 2 embedded images alongside the bullets.

## Slide 25 — Add Batch Normalization
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Add Batch Normalization'.

## Slide 26 — Results
Results slide with 2 screenshots showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 27 — Weights Distribution
Hidden layer output (after batch norm) has a wider spread, and weights connecting the hidden layer to the output have a smaller distribution. The slide includes 2 embedded images alongside the bullets.

## Slide 28 — Dropout
So far Training accuracy 95%, validation accuracy 89% The model does not generalize well to unseen data, overfit to training data “Few training images control a few impactful parameters” Dropout Training: randomly drop (zero) certain weights with probability p, force other weights to adapt Inference: scale all weights by a factor (p). The slide includes 1 embedded image alongside the bullets.

## Slide 29 — Add dropout layer
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Add dropout layer'.

## Slide 30 — Regularization
Penalize large weights by a regularization factor in the loss function L1 regularization. The slide includes 2 embedded images alongside the bullets.

## Slide 31 — Results
Less overfitting, difference between training and validation accuracy. The slide includes 1 embedded image alongside the bullets.

## Slide 32 — L2 Regularization
Cross-Entropy Loss with L2 regularization. The slide includes 3 embedded images alongside the bullets.

---

## Deck-level takeaway
The deck spans 32 slides, opening with "Deep Neural Network for Image Classification" and closing with "L2 Regularization". Body-text coverage is 53%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Scaling the images, Why scaling help, Adding validation data and validation loss, Training Results.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4010_Vision_DeepClassification/4011_MLPClassifier/slides/`.
