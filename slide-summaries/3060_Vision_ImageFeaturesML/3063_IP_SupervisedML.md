# 3063_IP_SupervisedML — Per-Slide Summary

**Source file:** `3063_IP_SupervisedML.pptx`
**Source folder:** `SlidesPool/3060_Vision_ImageFeaturesML/`
**Drive link:** https://drive.google.com/file/d/19qr9h_nluJkNUPTe4ps6MljNDOWaruYf/view
**Slide count (exact, via python-pptx):** 39
**Extraction:** Local parse + slide PNG render. 14 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Classical Supervised ML for image processing
Section divider; the deck transitions to material on classical supervised ml for image processing.

## Slide 2 — Image Classicfication
Section divider; the deck transitions to material on image classicfication.

## Slide 3 — The process
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'The process'.

## Slide 4 — MNIST dataset
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'MNIST dataset'.

## Slide 5 — K-NN Classifier
Section divider; the deck transitions to material on k-nn classifier.

## Slide 6 — K-NN Classifier
Define distance between images (Euclidean) Check k closest points in the training set Assign label by majority vote. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — Representing images
Fast search for nearest neighbors Ball tree K-d tree. The slide includes 2 embedded images alongside the bullets.

## Slide 8 — Example
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Example'.

## Slide 9 — Evaluating
Confusion Matrix. The slide includes 2 embedded images alongside the bullets.

## Slide 10 — Bayes Classifier
Section divider; the deck transitions to material on bayes classifier.

## Slide 11 — Maximum Likelihood Estimation
Assume the distribution of pixel values given a class label is Gaussian A 784 vector (28x28 image) A class mean is a 784 vector Class Covariance is a 784x784 matrix Compute MLE estimations using training data. The slide includes 1 embedded image alongside the bullets.

## Slide 12 — Compute posteriori using Bayes rules
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Compute posteriori using Bayes rules').

## Slide 13 — Classifier
Section divider; the deck transitions to material on classifier.

## Slide 14 — SVM Classifier
Section divider; the deck transitions to material on svm classifier.

## Slide 15 — Maximum Margin Separating Hyperplane
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Maximum Margin Separating Hyperplane'.

## Slide 16 — Relaxation: Slack Variable
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Relaxation: Slack Variable'.

## Slide 17 — Linear Separability
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Linear Separability'.

## Slide 18 — Lifting to linear separable in high-dimensional space
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Lifting to linear separable in high-dimensional space'.

## Slide 19 — Kernel Trick
No need to project each datapoint, only indicate the kernel, the “distance” (inner product) in the new space. The slide includes 1 embedded image alongside the bullets.

## Slide 20 — Multiclass Classification
One-vs-all Each classifier gives a score Pick the class with the maximum score One-vs-one (OvO) Classify by majority vote Implemented at the sklearn SVC function. The slide includes 2 embedded images alongside the bullets.

## Slide 21 — Example
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Example'.

## Slide 22 — Object Detection
Section divider; the deck transitions to material on object detection.

## Slide 23 — Object Detection
Identify and localize objects in the image Bounding box and label. The slide includes 1 embedded image alongside the bullets.

## Slide 24 — Viola-Jones Face detector
AdaBost with Haar-like features.

## Slide 25 — Haar-Features
Defined by a matrix: +1, -1, 0 Axis-aligned and rectangular blocks. Fast computation with integral image. The slide includes 5 embedded images alongside the bullets.

## Slide 26 — AdaBoost
Start from the ensemble of weak learners Slightly better than random Boost sample weights when adding the next classifier Start from uniform sample weights Add and train the next classifier Increase the weights of incorrectly classified points Viloa Jones Each Haar feature is a classifier Training -> select thresholds. The slide includes 1 embedded image alongside the bullets.

## Slide 27 — Cascade
At inference time Run weak classifiers one-by-one Quickly discard non-faces Run a window over the image and decide at each window face-no-face Try different scales for small-large faces Scale Haar Kernels size Use non-maximum suppression (NMS). The slide includes 1 embedded image alongside the bullets.

## Slide 28 — Viola-Jones
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Viola-Jones'.

## Slide 29 — Dataset : Positive and Negative Examples
Dataset/sample slide containing 2 figures that visualise the data used at this point of the project pipeline.

## Slide 30 — Find best Haar feature with Random Forrest
Section divider; the deck transitions to material on find best haar feature with random forrest.

## Slide 31 — Decision Tree
Build incrementally with a greedy objective Simple decisions can overfit easily High-variance model. The slide includes 2 embedded images alongside the bullets.

## Slide 32 — Random Forrest
Ensemble of trees Build each tree on a random sample from training data Select from a random subset of features for each split Aggregate by majority vote Low variance ensemble. The slide includes 1 embedded image alongside the bullets.

## Slide 33 — Feature importance with Random Forre4st
Important features are frequently used Impurity measure Measure of class mix in the set Impurity =0: a single class Mean decrease in impurity Important features decrease impurity in each child Feature importance. The slide includes 3 embedded images alongside the bullets.

## Slide 34 — Example
Extract Haar-like features. The slide includes 1 embedded image alongside the bullets.

## Slide 35 — Train random forest classifier
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Train random forest classifier'.

## Slide 36 — Find important features
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Find important features'.

## Slide 37 — Detecting Objects with HOG features
Section divider; the deck transitions to material on detecting objects with hog features.

## Slide 38 — The process
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'The process'.

## Slide 39 — Detect people with OpenCV
Extract HOG features and feed to pretrained classifier. The slide includes 2 embedded images alongside the bullets.

---

## Deck-level takeaway
The deck spans 39 slides, opening with "Classical Supervised ML for image processing" and closing with "Detect people with OpenCV". Body-text coverage is 41%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include SVM Classifier, Maximum Margin Separating Hyperplane, Relaxation: Slack Variable, Linear Separability.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3060_Vision_ImageFeaturesML/3063_IP_SupervisedML/slides/`.
