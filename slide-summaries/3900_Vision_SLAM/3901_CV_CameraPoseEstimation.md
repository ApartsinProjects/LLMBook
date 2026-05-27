# 3901_CV_CameraPoseEstimation — Per-Slide Summary

**Source file:** `3901_CV_CameraPoseEstimation.pptx`
**Source folder:** `SlidesPool/3900_Vision_SLAM/`
**Drive link:** https://drive.google.com/file/d/1bD-WGeiisSst8vO2fUjPmmFanQ_F08OT/view
**Slide count (exact, via python-pptx):** 7
**Extraction:** Local parse + slide PNG render. 1 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Camera Pose Estimation
Section divider; the deck transitions to material on camera pose estimation.

## Slide 2 — Perspective-n-Point(PnP) Pose Computation
Where is the camera in the world Frequently based on a “3D map.” Stores points in 3D and their image features Assume we have 3D points and their corresponding 2D points in the image Find unknown camera rotation and translation Minimize reprojection error. The slide includes 3 embedded images alongside the bullets.

## Slide 3 — P3P Solver
Number of parameters Translation: 3 and rotation 3 Each correspondence gives 2 constraints Rotation about the ray axis Translation along the ray is unconstrained Need at least three correspondences Solution Reduces to 3 quadric polynomial on distances to the camera of 3 points Ambiguous solution, constraints are satisfied by 4 configurations Camera can be on either side of the plane that passes through 3 points Two near/far configuration. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — Representing Rotation
Rodrigues angles Any rotation can be represented by a single rotation axis and angle Represent using a single 3D vector Direction corresponds to the rotation axis Magnitude to rotation angle Euler angles Around each coordinate axis(order matter) Yaw, Pitch, Roll. The slide includes 3 embedded images alongside the bullets.

## Slide 5 — P3P Solver OpenCV
Return rotation vector (Rodrigues). Return a single solution, heuristic choice. All 4 solutions. The slide includes 4 embedded images alongside the bullets.

## Slide 6 — P3P with RANSAC
Randomly select K(K=3) points Fit the model Compute the error for each point Partition all points into inliers/outliers based on error Keep the best hypothesis (maximum number of inliers) Stop after M iterations or when sufficient inlier mass. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — Visualization
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Visualization'.

---

## Deck-level takeaway
The deck spans 7 slides, opening with "Camera Pose Estimation" and closing with "Visualization". Body-text coverage is 71%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include P3P Solver, Representing Rotation.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3900_Vision_SLAM/3901_CV_CameraPoseEstimation/slides/`.
