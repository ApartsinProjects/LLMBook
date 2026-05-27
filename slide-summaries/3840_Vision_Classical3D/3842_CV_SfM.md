# 3842_CV_SfM — Per-Slide Summary

**Source file:** `3842_CV_SfM.pptx`
**Source folder:** `SlidesPool/3840_Vision_Classical3D/`
**Drive link:** https://drive.google.com/file/d/1gJqrOQQ5VDT0S938sGhFyVJ6Fzl0tni3/view
**Slide count (exact, via python-pptx):** 8
**Extraction:** Local parse + slide PNG render. 3 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Structure from Motion
Section divider; the deck transitions to material on structure from motion.

## Slide 2 — MVS: Multiple View Stereo
Point coordinates from calibrated pair Fundamental matrix(3x3, 7DoF) encodes camera geometry and intrinsic Essential matrix(3x3, 5DoF encodes relative camera position. The slide includes 4 embedded images alongside the bullets.

## Slide 3 — Structure from Motion
The single camera is moving Pose (Extrinsic) parameters are unknown Simultaneously estimate: Camera poses (position and orientation, essential matrices) A sparse 3D structure. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — SfM Pipeline
Feature detection (SIFT/ORB/etc.) Feature matching across images(with trcakig) Relative pose estimation (essential/fundamental matrix) Triangulation → sparse 3D points Bundle adjustment → jointly refine all camera poses and 3D points. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Reminder Feature Matching/Tracking
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Reminder Feature Matching/Tracking'.

## Slide 6 — Bundle Adjustment
Optimize rotation/translation and estimated 3D point Minimize back projection error Linearize reprojection error loss with Jacobian Solve linear system Solve efficiently because special block structure of Jacobian. The slide includes 4 embedded images alongside the bullets.

## Slide 7 — OpenCV
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'OpenCV'.

## Slide 8 — Examples
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Examples'.

---

## Deck-level takeaway
The deck spans 8 slides, opening with "Structure from Motion" and closing with "Examples". Body-text coverage is 50%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Structure from Motion, SfM Pipeline, Reminder Feature Matching/Tracking.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3840_Vision_Classical3D/3842_CV_SfM/slides/`.
