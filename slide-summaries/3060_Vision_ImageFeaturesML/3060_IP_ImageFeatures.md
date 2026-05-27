# 3060_IP_ImageFeatures — Per-Slide Summary

**Source file:** `3060_IP_ImageFeatures.pptx`
**Source folder:** `SlidesPool/3060_Vision_ImageFeaturesML/`
**Drive link:** https://drive.google.com/file/d/1dEfDV85fI5stSy17qNJJ-GTOL2s6_xCY/view
**Slide count (exact, via python-pptx):** 14
**Extraction:** Local parse + slide PNG render. 2 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image Features and Descriptors
Section divider; the deck transitions to material on image features and descriptors.

## Slide 2 — Features vs. Descriptors
Image features Corners, regions, keypoints Frequently defined by location and orientation Identified by a feature detector Image descriptor A numerical vector corresponding to a feature Can be matched, compared, classified Additional output by feature detector. The slide includes 2 embedded images alongside the bullets.

## Slide 3 — Harris Corner Detector
Section divider; the deck transitions to material on harris corner detector.

## Slide 4 — Harris Corner Detector
Corner: image changes strongly in two perpendicular directions Intuitions Shift a small window over the pixel Shift in any direction causes a significant change in all pixel values. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Computation
Square difference of change in the intensity Approximation using gradient Plug into the squared difference M defines an ellipse with axes defined by eigenvectors and eigenvalues Eigenvalues give extreme values for the change Both eigenvalues must be significant for the corner. The slide includes 6 embedded images alongside the bullets.

## Slide 6 — Example
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Example'.

## Slide 7 — Subpixel Accuracy for Harris detector
Pass over pixel grid Compute score Non-maximum suppression Interpolate using a quadratic surface. Yellow is pixel-level detection, red is refined subpixels. The slide includes 3 embedded images alongside the bullets.

## Slide 8 — Application: Image Matching
Compute features/points-of-interest in two images Consider a region around each point Compute a descriptor of each region Compute “similarity” between every pair of descriptors in two images Keep the highest similarity matches. The slide includes 1 embedded image alongside the bullets.

## Slide 9 — Robust matching with RANSAC algorithm
Task Estimate geometric transformation between two images (affine, different viewpoints) If enough matches are found, can estimate transformation parameters using least squares Challenge Many correspondences are likely to be faulty RANSAC Classify points (correspondences) into inliers and outliers Ignore outliers when estimated transformation parameters.

## Slide 10 — RANSAC algorithm
Random Sample Consensus Build many models with samples Search the largest consensus. Try N times, select the best model, refit it using its own inliers. The slide includes 2 embedded images alongside the bullets.

## Slide 11 — Blob Detectors
Region locally different from surrounding.

## Slide 12 — Image blobs
Bright on a dark or dark on a bright region in the image. The slide includes 1 embedded image alongside the bullets.

## Slide 13 — LoG/DoG/DoH with scale -space
Blob in Gaussian Pyramid looks like a bright extremum at some coarse scale Use LoG to detect it in the correct scale Approximate with DoG, faster computation Also triggered by edges DoH: Determinant of Hessian Hession: 2nd order derivatives Edges does not trigger. The slide includes 2 embedded images alongside the bullets.

## Slide 14 — Example
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Example'.

---

## Deck-level takeaway
The deck spans 14 slides, opening with "Image Features and Descriptors" and closing with "Example". Body-text coverage is 71%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Computation, Example, Subpixel Accuracy for Harris detector, Application: Image Matching.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3060_Vision_ImageFeaturesML/3060_IP_ImageFeatures/slides/`.
