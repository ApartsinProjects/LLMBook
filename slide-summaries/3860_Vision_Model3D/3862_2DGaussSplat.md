# 3862_2DGaussSplat — Per-Slide Summary

**Source file:** `3862_2DGaussSplat.pptx`
**Source folder:** `SlidesPool/3860_Vision_Model3D/`
**Drive link:** https://drive.google.com/file/d/1TwIUeBxRd3LN5JllGdVeXFqrwGldlvii/view
**Slide count (exact, via python-pptx):** 7
**Extraction:** Local parse + slide PNG render. 1 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — 2D Gaussian Splatting
Section divider; the deck transitions to material on 2d gaussian splatting.

## Slide 2 — 3D vs. 2D Gaussian Splatting
3D Gaussian Splatting Model the world with blobs scattered through space 2D Gaussian Splatting Model the world using flat-oriented 2D disks Surface aligned Better photorealism and geometric accuracy.

## Slide 3 — From NeRF to 3DGS
NeRF Does not store geometry explicitly, implicit function Represent the world as a continuous neural function Sample points along the ray and compose 3DGS Does not store geometry explicitly, implicit representation Set of millions of Gaussian primitives Project Gaussians impact along the ray and compose. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — Geometry Problem in 3DGS
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Geometry Problem in 3DGS'.

## Slide 5 — 2GDS
Represent the world as flat elliptical discs. The slide includes 1 embedded image alongside the bullets.

## Slide 6 — Disk Representation
3D parametric surface parametrized by 2D point coordinates inside the disc. The slide includes 3 embedded images alongside the bullets.

## Slide 7 — Perspective-Correct Ray-Splat Intersection
No need to project as in 3GDS Explicitly compute each disc contribution to each ray Intersection point coordinate (internal 2D Disk position) Evaluate Gaussian on (u,v). The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 7 slides, opening with "2D Gaussian Splatting" and closing with "Perspective-Correct Ray-Splat Intersection". Body-text coverage is 71%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include From NeRF to 3DGS, Geometry Problem in 3DGS.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3860_Vision_Model3D/3862_2DGaussSplat/slides/`.
