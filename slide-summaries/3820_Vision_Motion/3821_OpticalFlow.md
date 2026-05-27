# 3821_OpticalFlow — Per-Slide Summary

**Source file:** `3821_OpticalFlow.pptx`
**Source folder:** `SlidesPool/3820_Vision_Motion/`
**Drive link:** https://drive.google.com/file/d/11Ro4NyCRz5O_b_XXDue1BfQvmZiJBlO2/view
**Slide count (exact, via python-pptx):** 18
**Extraction:** Local parse + slide PNG render. 6 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Optical Flow
Section divider; the deck transitions to material on optical flow.

## Slide 2 — Random Dot
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Random Dot'.

## Slide 3 — Optical Flow
Per-pixel motion estimation between two consecutive frames in one video Shift vector per pixel Used in motion analysis and tracking. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — Pixel Intensity Function
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Pixel Intensity Function'.

## Slide 5 — Brightness Consistency Assumption
Brightness does not change when the pixel moves Using Taylor expansion. Solve for u and v at each point using spatial and temporal gradients. The slide includes 7 embedded images alongside the bullets.

## Slide 6 — Sparse vs. Dense Optical Flows
Sparse optical flow algorithms Compute motion vectors for specific objects (e.g., corners) Extract feature first Dense optical flow algorithms Compute optical flow for each pixel.

## Slide 7 — Sparse Optical Flow
Section divider; the deck transitions to material on sparse optical flow.

## Slide 8 — Lucas-Kanade algorithm
Brightness Consistency for n points that move in the same direction (small image patch around corner) Solving using least squares (closed-form). The slide includes 4 embedded images alongside the bullets.

## Slide 9 — Multiscale (Pyramid Lucas-Kanade)
Small motion limitation due to Taylor linearization Patch consistency (exclude non-rigid or occlusion) Build a pyramid Compute coarse optical flow Compute finer correction at the finer level. The slide includes 1 embedded image alongside the bullets.

## Slide 10 — Lucas-Kanade
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Lucas-Kanade'.

## Slide 11 — Computing
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Computing'.

## Slide 12 — Visualize optical flow
Encode displacement into color (HSV color space). The slide includes 1 embedded image alongside the bullets.

## Slide 13 — Dense Optical Flow
Section divider; the deck transitions to material on dense optical flow.

## Slide 14 — Via Interpolation
Compute dense optical flow Use LK dense optical flow algorithm first Interpolate motion vectors. The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Farneback algorithm
Approximate small patches in two frames using a quadratic polynomial Model assumption for unknown displacement vector d Assuming a similar quadratic term and constants encode uniform brightness change between frames Symmetrically. The slide includes 7 embedded images alongside the bullets.

## Slide 16 — OpenCV example
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'OpenCV example'.

## Slide 17 — Robust Local Optical Flow
Assume brightness consistency at each pixel Minimize robust cost (sub-quadratic error) Reduce the effect of outliers Weight pixels in the window Spatial: close to center(target pixel) dominate Gradient: downgrade pixels with a small gradient Photometric: suppress outliers, Solve iteratively Find motion estimates Update photometric weight. The slide includes 5 embedded images alongside the bullets.

## Slide 18 — OpenCV
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'OpenCV'.

---

## Deck-level takeaway
The deck spans 18 slides, opening with "Optical Flow" and closing with "OpenCV". Body-text coverage is 50%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Sparse Optical Flow, Lucas-Kanade algorithm, Multiscale (Pyramid Lucas-Kanade), Lucas-Kanade.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3820_Vision_Motion/3821_OpticalFlow/slides/`.
