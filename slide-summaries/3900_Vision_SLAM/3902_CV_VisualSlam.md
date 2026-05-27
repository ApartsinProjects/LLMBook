# 3902_CV_VisualSlam — Per-Slide Summary

**Source file:** `3902_CV_VisualSlam.pptx`
**Source folder:** `SlidesPool/3900_Vision_SLAM/`
**Drive link:** https://drive.google.com/file/d/1uRrdTkWarigU-bXtAIWJWagMMHEc5SgS/view
**Slide count (exact, via python-pptx):** 8
**Extraction:** Local parse + slide PNG render. 3 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Visual SLAM
Section divider; the deck transitions to material on visual slam.

## Slide 2 — Simultaneous Localization And Mapping
Map building Set of 3D keypoints View-independent descriptors for matching Localization Estimate pose relative to map 6DoF Rotation+Translation. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Monocular Slam Definition
Given images Find 3D landmarks(map) Trajectory (poses) Probabilistic objective Maximize posterior probability Solve two problems. The slide includes 5 embedded images alongside the bullets.

## Slide 4 — SLAM pipeline contains several algorithms
Front-end Algorithms: Algorithms responsible for estimating the camera pose and 3D map points, extract row features From last K=2 frames: Extract and match features Estimate motion Translate matched motion to 3D or match to existing 3D map Update the map with new 3D points Back-end Algorithms: Algorithms responsible for optimizing the estimated camera pose and mapping Reconcile with the previous map Optimize, bundle adjustment. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — SLAM Pipeline
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'SLAM Pipeline'.

## Slide 6 — Fron-End Algorithm
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Fron-End Algorithm'.

## Slide 7 — Back-End Algorithms
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Back-End Algorithms'.

## Slide 8 — Loop Detection
Some drift is inevitable Detect loop closure Using compact descriptor of the pose (visual words, Bag-of-Words) Offline pose refinement Reduce drift. The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 8 slides, opening with "Visual SLAM" and closing with "Loop Detection". Body-text coverage is 50%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Monocular Slam Definition, SLAM pipeline contains several algorithms, SLAM Pipeline.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3900_Vision_SLAM/3902_CV_VisualSlam/slides/`.
