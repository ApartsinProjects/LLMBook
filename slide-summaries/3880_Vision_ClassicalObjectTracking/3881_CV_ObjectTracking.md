# 3881_CV_ObjectTracking — Per-Slide Summary

**Source file:** `3881_CV_ObjectTracking.pptx`
**Source folder:** `SlidesPool/3880_Vision_ClassicalObjectTracking/`
**Drive link:** https://drive.google.com/file/d/1AqmY0_mJkr2GHaIxdgvO-MJuZsafKnLk/view
**Slide count (exact, via python-pptx):** 29
**Extraction:** Local parse + slide PNG render. 4 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Object Tracking
Classical Models.

## Slide 2 — What is object tracking?
Locating the same object in successive frames of the video Single vs multiple object tracking. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Tracking vs. Detection
Alternative to tracking Detect objects in each frame If a single object tracking, no need for matching Tracking Detection always starts from scratch Is faster, easier to find the moved object Works where detection might fail, easier to match known objects Might accumulate error or lose object (occluded) Rerun detection step Preserves identity If multiple objects.

## Slide 4 — OpenCV comes with several tracking algorithms
BOOSTING MIL KCF TLD MEDIANFLOW GOTURN MOSSE CSRT. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Tracking loop
Initializing with a detector Try to reacquire if tracking failed (OK=False). The slide includes 2 embedded images alongside the bullets.

## Slide 6 — Motion Model vs. Appearance Model
Motion model Estimates of object direction and velocity Obtained from tracking object in previous frames Can predict object position based on the current model Appearance model Encode the appearance of the object Search objects/pixels of the same appearance in a small neighborhood around the location predicted by the motion model Update motion model with new observations.

## Slide 7 — Appearance-only models
Section divider; the deck transitions to material on appearance-only models.

## Slide 8 — Appearance model
Simple template matching Only if the object does not change between frames Classifier with online training Classify a region object/background A binary classifier return score After each match, select positive (object) and negative (background) examples Update classifier with current examples (or short history). The slide includes 1 embedded image alongside the bullets.

## Slide 9 — Reminder : Haar features
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Reminder : Haar features'.

## Slide 10 — Reminder: AdaBoost
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Reminder: AdaBoost'.

## Slide 11 — Boosting Tracker
No motion model Search around the previous location Online learning for a specific video/object Gradually improves Observe positive and negative patches Appearance model with AdaBoost and Haar Features Add the best weak classifiers for the best classification of the current observation. The slide includes 1 embedded image alongside the bullets.

## Slide 12 — Background : Multiple Instance Learning
Basic unit of data is a bag of instances Positive bag: at least one instance is positive Negative bag: all instances are negative But the model should score instances Usually During training: only bags are available During inference: individual instances are scored with optional bag aggregation Usually trained with bag-level loss. The slide includes 2 embedded images alongside the bullets.

## Slide 13 — MIL Tracker
Form a positive bag by considering patches around the detection Include correct object BB Handle inaccurate detection Same classifier as Boosting Trained with MIL(multiple instance learning) loss for positive bags. The slide includes 1 embedded image alongside the bullets.

## Slide 14 — MOSSE Tracker
Minimum Output Sum of Squared Error Learn a simple correlation-based template (w) Peak around the box center location Represent soft label as a Gaussian around the location Minimize error (y is label) Soft update. The slide includes 4 embedded images alongside the bullets.

## Slide 15 — Reminder: HoG Features
Section divider; the deck transitions to material on reminder: hog features.

## Slide 16 — KCF Tracker
Kernelized Correlation Filters Appearance model based on templates Template and image are represented by HoG features Find the best match around the past location Update with new training patch Optimization Efficient FFT-based correlation Use Gaussian kernels instead of correlation. The slide includes 5 embedded images alongside the bullets.

## Slide 17 — Reminder: Sparse Optical Flow
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Reminder: Sparse Optical Flow'.

## Slide 18 — Scale estimation
Is the object becoming smaller or larger? How the distance between points changes From optical flow Compute scale using point pairs Take median as object scale Resize box/template according to scale during tracking. The slide includes 3 embedded images alongside the bullets.

## Slide 19 — Tracking with motion model
Optical flow-based.

## Slide 20 — Random Fern Classifier
Aggregate many binary features Comparison of random (but fixed) pixels Fixed location within the box Classifier Compute binary code c: 010100011 Use a lookup table for the decision score. The slide includes 3 embedded images alongside the bullets.

## Slide 21 — TLD Tracker
Tracking-Learning-Detection Maintain two processes: tracking and detection Tracking: optical-flow based Compute flows for special points(corners) Aggregate as a single motion vector (median) Search for objects around the predicted location okT: True if object is found Detection: cascade detector with various features Search everywhere Variance features: reject low variance patches Random ferns Nearest neighbors okD: true if object is found Trust detector more than tracker Learning: update detector Update fern probability tables and NN templates Decision: track if tracker and detector agree Otherwise, re-initialize tracker. The slide includes 1 embedded image alongside the bullets.

## Slide 22 — OpenCV tracker
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'OpenCV tracker'.

## Slide 23 — MEDIANFLOW Tracker
Optical-flow based tracker Compute forward optical flow Compute backward optical flow Discard points that do not match Estimate object motion as the median of the remaining vectors Update bounding box with estimated scale. The slide includes 4 embedded images alongside the bullets.

## Slide 24 — GOTURN Tracker
Generic Object Tracking Using Regression Network Implicit motion model (encoded by network) Uses a pretrained network that predicts a bounding box 4-value regression Pretrain on a lot of videos Input Crop fixed ratio around the location of the previous box in both images Source crop implicitly specifies bounding box center and size Trained to predict how bounding box usually move. The slide includes 1 embedded image alongside the bullets.

## Slide 25 — Reminder: Foreground-Background Segmentation with Pixel Statistics
Sample background-foreground pixels Shrink current bounding box Inside: more foreground, outside more background Build a statistical model (histogram) of features Generate mask by thresholding. The slide includes 4 embedded images alongside the bullets.

## Slide 26 — CSRT Tracker
Discriminative Correlation Filter with Channel and Spatial Reliability (DCF-CSR) Multichannel Appearance Model Each pixel is a feature vector HoG Color Names (map RGB to 11 colors: black, blue, …) 11-dim distance to (black, blue, brown…) Grayscale values Learn filter (template) per channel With suppressed background pixels (via segmentation) Compute channel reliability and weight estimates. Update M with Foreground-Background Histogram of features. The slide includes 5 embedded images alongside the bullets.

## Slide 27 — Multi-object Tracking
Section divider; the deck transitions to material on multi-object tracking.

## Slide 28 — Multi-object Tracking
Assign ID to an object. The slide includes 1 embedded image alongside the bullets.

## Slide 29 — Naïve MOT
Track each object independently with a single-object tracker No interaction, detection, re-identification. The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 29 slides, opening with "Object Tracking" and closing with "Naïve MOT". Body-text coverage is 76%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Reminder: AdaBoost, Boosting Tracker, Background : Multiple Instance Learning, MIL Tracker.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3880_Vision_ClassicalObjectTracking/3881_CV_ObjectTracking/slides/`.
