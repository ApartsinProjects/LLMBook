# 3841_CV_Stereo — Per-Slide Summary

**Source file:** `3841_CV_Stereo.pptx`
**Source folder:** `SlidesPool/3840_Vision_Classical3D/`
**Drive link:** https://drive.google.com/file/d/1ALtNwLzhvgkciDF941eF3FvJT3L5MQch/view
**Slide count (exact, via python-pptx):** 25
**Extraction:** Local parse + slide PNG render. 3 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Stereo and Motion
Section divider; the deck transitions to material on stereo and motion.

## Slide 2 — Recovering depth
Estimate distance from the camera to each pixel Depth map. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Triangulation
A pixel in the image corresponds to a ray(direction) Need at least two viewpoint cameras. The slide includes 2 embedded images alongside the bullets.

## Slide 4 — Two viewpoints
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Two viewpoints'.

## Slide 5 — Recipe: Depth estimation
Perform stereo camera calibration Estimate relative camera positions Find dense correspondence Pixel(s) in image B that correspond to each pixel in image A Estimate relative depth In “baseline” units Transform to true depth Known external scale in true units Need camera calibration/scale. The slide includes 1 embedded image alongside the bullets.

## Slide 6 — Stereo calibration: Relative Camera Position
Fixed-world target stereo calibration Simultaneous monochromatic calibration using the same fixed pattern position Stereo self-calibration, no known target Based on the correspondence of features Solve for relative position and intrinsic (encode as a fundamental matrix) Use to find dense correspondence and estimate depth Individual calibration joint Calibrate each camera individually for intrinsic parameters using targets Self-calibrate only for relative position.

## Slide 7 — Unconstrainted dense point correspondence
It’s very difficult to find point correspondence for all image points Not a special feature point, many have similar descriptors/patches Search space is too large Need a useful constraint (“epipolar constraint”). The slide includes 1 embedded image alongside the bullets.

## Slide 8 — Epipolar Geometry
Given a point in one image, where the corresponding point can be found in the second image On a line (epipolar line) Line defined by camera relative position Position on the line is defined by a point depth. The slide includes 1 embedded image alongside the bullets.

## Slide 9 — Representing line  in 2D
A 3D vector up to a scale Homogenous vectors Projective space Unified representation of points and lines in the plane Points and lines (a,b,c), c!=0, equivalence class Line that passes through the origin c=0. The slide includes 2 embedded images alongside the bullets.

## Slide 10 — Epipolar Geometry: Definitions
Epipolar line for a point: location of possible correspondences Epipole of the camera C1 in C2: projection of camera C1 center to C2 image Baseline: the line between two camera centers Epipolar plane: pass through C1,C2 (and this e1 and e2) and point X Epipolar plane intersect image plane in the epipolar line. The slide includes 1 embedded image alongside the bullets.

## Slide 11 — Fundamental Matrix
Represent epipolar geometry with a single matrix Relative pose between cameras (rotation and translation up to scale) Intrinsic parameters of both cameras Epipolar constraint Fundamental matrix 3x3, rank 2, 7 DoF Epipolar line. The slide includes 3 embedded images alongside the bullets.

## Slide 12 — Essential Matrix
Fundamental matrix Encode epipolar geometry and camera intrinsic parameters 7 DoF Essential matrix Relative camera geometry only Useful when the intrinsic parameters of each camera are calibrated 7 DoF. The slide includes 3 embedded images alongside the bullets.

## Slide 13 — Find Fundamental/Essential Matrix
7 DoF parameters in the fundamental matrix, solve the overspecified system of equations Find best fit (reduce MSE error), omit outliers. RANSAC. The slide includes 2 embedded images alongside the bullets.

## Slide 14 — Foundation Matrix from Point Correspondence
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Foundation Matrix from Point Correspondence'.

## Slide 15 — End-to-End Calibration: 1
First calibrate with checkerboard. The slide includes 1 embedded image alongside the bullets.

## Slide 16 — End-to-End Calibration : 2
Reuse intrinsic parameter matrix, find essential matrix. The slide includes 2 embedded images alongside the bullets.

## Slide 17 — End-to-End Calibration: 3
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'End-to-End Calibration: 3'.

## Slide 18 — Special Case: Paralleled Imaging Planes
Find features and descriptors in both images Epipolar lines are rows y=y1 Simple dense correspondence No need to calibrate (for relative depth). The slide includes 3 embedded images alongside the bullets.

## Slide 19 — Disparity
A shift in x coordinates between two pixels corresponding to the same world point in two images Recovering depth Need calibrated camera for real unit focal length. The slide includes 2 embedded images alongside the bullets.

## Slide 20 — Disparity vs. Depth
Measure actual depth for few points to estimative scaling factor. Z is the distance, coeff is inverse disparities. The slide includes 3 embedded images alongside the bullets.

## Slide 21 — Semi-Global Block Matching
Find matches (in the same line) Minimize energy Dynamical programming. The slide includes 2 embedded images alongside the bullets.

## Slide 22 — Compute Disparity
Relative depth is inversely proportional to disparity. The slide includes 3 embedded images alongside the bullets.

## Slide 23 — Rectification
Rectify images after stereo calibration and solve disparity for parallel imaging planes. The slide includes 2 embedded images alongside the bullets.

## Slide 24 — Precompute for fast rectification
Repeat on may frames, same transformation if camera positions doe not change. The slide includes 2 embedded images alongside the bullets.

## Slide 25 — Beyond two-view stereo
The third view can be used for verification. The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 25 slides, opening with "Stereo and Motion" and closing with "Beyond two-view stereo". Body-text coverage is 84%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Representing line  in 2D, Epipolar Geometry: Definitions, Fundamental Matrix, Essential Matrix.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3840_Vision_Classical3D/3841_CV_Stereo/slides/`.
