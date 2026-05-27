# 3061_IP_ImageDescriptors — Per-Slide Summary

**Source file:** `3061_IP_ImageDescriptors.pptx`
**Source folder:** `SlidesPool/3060_Vision_ImageFeaturesML/`
**Drive link:** https://drive.google.com/file/d/1Ys0Ejwlgh9UMNp0eSFbWY9wKD42P2_rp/view
**Slide count (exact, via python-pptx):** 33
**Extraction:** Local parse + slide PNG render. 7 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Feature Descriptors
Section divider; the deck transitions to material on feature descriptors.

## Slide 2 — Core Invariants
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Core Invariants'.

## Slide 3 — Discriminative requirements
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Discriminative requirements'.

## Slide 4 — HoG: Histogram of Oriented Gradients
Feature descriptor.

## Slide 5 — Step 1: Gradient Computation
Sasha Apartsin. 1-D centered point discrete derivative mask is applied on an image in both the horizontal and vertical directions filtering of the gray-scale image with the following filter kernels: Derivatives of the image I in the x and y directions: The orientation  and the magnitude |g| of the gradient are: The slide includes 3 embedded images alongside the bullets.

## Slide 6 — Step 2: Cell Orientation Histogram
Sasha Apartsin. The image is divided into small (usually 8x8 pixels) cells Each cell has a fixed number of gradient orientation bins evenly spread over 0, 180o or 0, 360o(depending on whether the gradient is unsigned or signed) Each pixel within the cell casts a weighted vote for a gradient orientation bin based on the gradient magnitude at that pixel For the vote weight, the pixel contribution can be the gradient magnitude or the square root of the gradient magnitude. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — HOG after step 2: Cells in a region
Sasha Apartsin. The slide includes 1 embedded image alongside the bullets.

## Slide 8 — Block/Region descriptor
Sasha Apartsin. Partition image into blocks of multiple cells (e.g., 4-by-4 cells) Concatenate histograms from each cell within the block Still might have different descriptors of the same object Differences in contrast Want to focus on gradient orientation, not magnitude Need to normalize the block feature vector Make it invariant to contrast/illumination.

## Slide 9 — Step 3: Block Normalization
Sasha Apartsin. Let v be the non-normalized vector containing all histograms in a given block, ||v||k be its k-norm for k D 1; 2, and ε be a small constant Then the normalization factor can be one of the following: The slide includes 1 embedded image alongside the bullets.

## Slide 10 — Example: HoG Descriptor
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Example: HoG Descriptor'.

## Slide 11 — Example
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Example'.

## Slide 12 — SIFT: Scale-Invariant Feature Transforms
Section divider; the deck transitions to material on sift: scale-invariant feature transforms.

## Slide 13 — Image keypoints
Not all pixels/image patches are equally informative Detect and describe informative locations. The slide includes 1 embedded image alongside the bullets.

## Slide 14 — Keypoints
Sasha Apartsin. Keypoints has large variance around them White walls are not very informative Variance can be detected and different scales Small variance in the immediate neighborhood Large variance in a large neighborhood that remains after some smoothing is applied Compare SIFT keypoints and HOG descriptors for every window.

## Slide 15 — Reminder
Sasha Apartsin. Edge point detection using LoG Laplacian of Gaussian. The slide includes 1 embedded image alongside the bullets.

## Slide 16 — Edge Points on Different Scales
Sasha Apartsin. Can control how much smoothing to apply before computing the Laplacian (second derivative). The slide includes 1 embedded image alongside the bullets.

## Slide 17 — Edges at different scales
Sasha Apartsin. The slide includes 1 embedded image alongside the bullets.

## Slide 18 — Image Scale-Space
Sasha Apartsin. Stack images at different scales Smoothed with different signals in this example. The slide includes 2 embedded images alongside the bullets.

## Slide 19 — Local maxima at scale-space
Sasha Apartsin. Local maxima are within 26 neighbors. 8 in the same scale, +18 in scale above, and scale below. The slide includes 1 embedded image alongside the bullets.

## Slide 20 — Maximum in scale space
Sasha Apartsin. At each level, each pixel has 9+9+8 neighbors 8 neighbors in the same scale 9 neighbors in 1 scale up 9 neighbors in 1 scale downs LoG scale-space Each pixel is a value of LoG A pixel is a local extrema if its value is greater than its 26 neighbors Keypoint coordinate is 3 numbers (x,y,sigma). The slide includes 1 embedded image alongside the bullets.

## Slide 21 — Additional steps
Sasha Apartsin. Accurate localization Filter out some unstable keypoints (low contrast, unstable) Compute a histogram of orientations at the scale where the keypoint has been detected Find a dominant direction (histogram peak) Rotate gradient orientation relative to the maximum Makes descriptor rotation invariant.

## Slide 22 — Example
Sasha Apartsin. A dominant orientation estimate is computed by creating a histogram of all the gradient orientations weighted by their magnitudes and then finding the significant peaks in this distribution. The slide includes 1 embedded image alongside the bullets.

## Slide 23 — Keypoint Descriptor
Sasha Apartsin. The gradient orientations are rotated relative to the orientation of the keypoint Then, a 16x16 neighborhood around the keypoint is divided into 16 sub-blocks of size 4x4 For each sub-block, an 8-bin orientation histogram is created SIFT descriptor: feature vector with 16x8=128 elements.

## Slide 24 — Example
Sasha Apartsin. (left) an input image (middle) some of the detected keypoints with their corresponding scales and orientations (right) SIFT descriptors, a 16x16 neighborhood around each keypoint is divided into 16 sub-blocks of 4x4 size. The slide includes 1 embedded image alongside the bullets.

## Slide 25 — Object Recognition Using SIFT
Sasha Apartsin. The slide includes 1 embedded image alongside the bullets.

## Slide 26 — Example: OpenCV
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Example: OpenCV'.

## Slide 27 — Matching images with BRIEF, SIFT, and ORB
Section divider; the deck transitions to material on matching images with brief, sift, and orb.

## Slide 28 — Variants
BRIEF Binary local feature descriptor Describe appearances around keypoints with simple binary comparisons Is pixel A brighter than pixel B ORB Efficient alternative to SIFT FAST corner detector in scale-space instead of LoG Faster descriptors (BRIEF).

## Slide 29 — Example
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Example'.

## Slide 30 — Haar-Like Features
Section divider; the deck transitions to material on haar-like features.

## Slide 31 — Haar-like features
Useful for object detection Viola-Jones face detector Set of convolution features Simple binary kernels Descriptor for a pixel Vector of convolution values. The slide includes 1 embedded image alongside the bullets.

## Slide 32 — Face Detection: Viola-Jones
Scan image with a sliding window (24x24) As many as 160K features per window (all possible configurations) Select a subset of Haar-like features to evaluate Compare with threshold as weak classifiers Decision by weighted average Fast evaluation using integral image No per-pixel multiplication by 0 and 1 Training Select iteratively best features (around 2000) and weights. The slide includes 1 embedded image alongside the bullets.

## Slide 33 — Example: Face and Eyes detection
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Example: Face and Eyes detection'.

---

## Deck-level takeaway
The deck spans 33 slides, opening with "Feature Descriptors" and closing with "Example: Face and Eyes detection". Body-text coverage is 67%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include SIFT: Scale-Invariant Feature Transforms, Image keypoints, Keypoints, Reminder.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3060_Vision_ImageFeaturesML/3061_IP_ImageDescriptors/slides/`.
