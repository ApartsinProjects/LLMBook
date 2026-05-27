# 3861_3DGaussSplat — Per-Slide Summary

**Source file:** `3861_3DGaussSplat.pptx`
**Source folder:** `SlidesPool/3860_Vision_Model3D/`
**Drive link:** https://drive.google.com/file/d/1JVkkPjhIBwY-5f5LDxX_FhehraacavWp/view
**Slide count (exact, via python-pptx):** 24
**Extraction:** Local parse + slide PNG render. 8 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — 3D Gaussian Splattng
Section divider; the deck transitions to material on 3d gaussian splattng.

## Slide 2 — 3D Data Representations
Point Clouds Meshes Voxel Grid. The slide includes 3 embedded images alongside the bullets.

## Slide 3 — NeRF: Neural Radiant Fields
Represent Radiant Field with a Network. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — 3D Gaussian Splatting: Overview
Represent scene with millions of Gaussians Compare “millions of training” with surface rendering Volume patch of space Position and shape Opacity (how transparent it is) Color contributed Initialize from sparse point cloud Generate from SfM: Structure-From-Motion Optimize with alignment control Refine distribution and alignment of Gaussians Tile-based rasterization for efficient rendering What gaussians affects each image tile Efficient, real-time navigation.

## Slide 5 — Analogy
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Analogy'.

## Slide 6 — Representing with 3D Gaussian
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Representing with 3D Gaussian'.

## Slide 7 — Traditional Image Formation
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Traditional Image Formation'.

## Slide 8 — 3D to 2D Projection in Gaussian Splatting
From world coordinate to camera coordinates. The slide includes 5 embedded images alongside the bullets.

## Slide 9 — From 3D Camera to 2D Image Coordinates
Visual slide containing 6 embedded figures with no body text; the visual carries the content of the topic 'From 3D Camera to 2D Image Coordinates'.

## Slide 10 — Ray Space Transformation
Need to integrate along the ray Transform to ray-aligned coordinates. The slide includes 3 embedded images alongside the bullets.

## Slide 11 — Taylor Expansion of Ray Space Transformation
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Taylor Expansion of Ray Space Transformation'.

## Slide 12 — Covariance Matrix Transformation in Ray Space
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Covariance Matrix Transformation in Ray Space'.

## Slide 13 — From 3D Gaussian to 2D Gaussian
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'From 3D Gaussian to 2D Gaussian'.

## Slide 14 — 3D Gaussian to Ellipsoid
Covariance matrix should be positive semi-definite If optimized with gradient descent might lose this property Represent covariance matrix as 3D ellipsoid. The slide includes 1 embedded image alongside the bullets.

## Slide 15 — 3D Gaussian to Ellipsoid
Ellipsoid Matrix eigenvalues: length of ellipsoid principal values Matrix eigenvectors: orientation of principal axes. The slide includes 4 embedded images alongside the bullets.

## Slide 16 — Optimization
Start from spars point cloud Initialize Gaussian per point Add random Gaussian elsewhere Adaptive density control Prune Gaussians Densification of the Gaussians.

## Slide 17 — Adaptive Density Control
Pruning Opacity is too small Gaussian is extremely small or large Densification Gaussian too large->split No neighboring gaussians->clone. The slide includes 1 embedded image alongside the bullets.

## Slide 18 — Point alpha composing
Each Gaussian Pixel color becomes. The slide includes 2 embedded images alongside the bullets.

## Slide 19 — Gaussian Composing
Compute the contribution from the density of each Gaussian Sort front-to-back (distance on the ray, 3rd coordinate in ray space). The slide includes 2 embedded images alongside the bullets.

## Slide 20 — Training Pipeline
Rasterize Project for specific target training image and compose. The slide includes 1 embedded image alongside the bullets.

## Slide 21 — Tile-Based Rasterization
Culling Eliminate Gaussians that are entirely outside the camera view Tiling Partition screen into tiles Allows parallel processing Duplicate Gaussians belonging to multiple tiles. The slide includes 1 embedded image alongside the bullets.

## Slide 22 — View-Depending Colors with Spherical Harmonics
A volume element might emit different colors in different directions A single-color parameter is not enough Encode color with spherical harmonics Coordinates of basis spherical functions Different for each color. The slide includes 2 embedded images alongside the bullets.

## Slide 23 — Optimization Pipeline
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Optimization Pipeline'.

## Slide 24 — Training Gaussian Splatting on a Custom Dataset
Gsplat: library used by nerf-studio. The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 24 slides, opening with "3D Gaussian Splattng" and closing with "Training Gaussian Splatting on a Custom Dataset". Body-text coverage is 62%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include From 3D Camera to 2D Image Coordinates, Ray Space Transformation, Taylor Expansion of Ray Space Transformation, Covariance Matrix Transformation in Ray Space.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3860_Vision_Model3D/3861_3DGaussSplat/slides/`.
