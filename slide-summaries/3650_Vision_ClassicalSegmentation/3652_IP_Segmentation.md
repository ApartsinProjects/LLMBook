# 3652_IP_Segmentation — Per-Slide Summary

**Source file:** `3652_IP_Segmentation.pptx`
**Source folder:** `SlidesPool/3650_Vision_ClassicalSegmentation/`
**Drive link:** https://drive.google.com/file/d/1Vp5d7BzewjKIAIb1BWgY1Q-ipBQ6wfqk/view
**Slide count (exact, via python-pptx):** 33
**Extraction:** Local parse + slide PNG render. 7 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image Segmentation
Low-level, pixel-based segmentation algorithms.

## Slide 2 — Thresholding and Otsu’s segmentation
Section divider; the deck transitions to material on thresholding and otsu’s segmentation.

## Slide 3 — Segment object vs. background
Threshold pixel value Assume pixel value histogram is bi-modal Find bets threshold. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — Otsu method
Maximize between-class variance Threshold defines Class means (average brightness) Class weight (% of total pixels). The slide includes 4 embedded images alongside the bullets.

## Slide 5 — Edge-based Segmentation
Section divider; the deck transitions to material on edge-based segmentation.

## Slide 6 — Detect Edges
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Detect Edges'.

## Slide 7 — Fill holes with morphological processing
A “binary” hole Background pixel(zero) Completely enclosed by foreground pixels(one) Algorithm Start from outer background pixels Flood-fill till boundary Fill remaining holes. The slide includes 3 embedded images alongside the bullets.

## Slide 8 — Drop small objects
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Drop small objects'.

## Slide 9 — Region-based segmentation
Section divider; the deck transitions to material on region-based segmentation.

## Slide 10 — Morphological watershed
Analogy Image as a topographic surface Water rises from local minima(marker) Grows catchment basin Watershed lines: water from different basins is about to merge. The slide includes 3 embedded images alongside the bullets.

## Slide 11 — Implementation
Find starting points(markers) and run watershed “flooding” Elevation map: use gradient strength. The slide includes 2 embedded images alongside the bullets.

## Slide 12 — Find Markers
Bright points are inside the coins Background basic (marker=1) competes with foreground basin Each distinct market value becomes a segment Same ID markers ->basin s are merged. Many markets for each of the two segments. The slide includes 2 embedded images alongside the bullets.

## Slide 13 — Watershed Flooding
On an elevation map of Sobel edges With starting markers from brightness. The slide includes 2 embedded images alongside the bullets.

## Slide 14 — Fill Holes and label connected components
Hole filling: start from the background flood fill, and the remaining pixels are inside the objects. The slide includes 2 embedded images alongside the bullets.

## Slide 15 — Graph-based image segmentation
Section divider; the deck transitions to material on graph-based image segmentation.

## Slide 16 — Image as a graph
Pixels are nodes, connected to neighbors Weights according to dissimilarity Partition graph into “soft” connected components Weights inside components are lower. The slide includes 3 embedded images alongside the bullets.

## Slide 17 — Algorithm(felzenzwalb “FEL-zen-shvalb”)
Start with pixel-size components Edge e =(p,1) between nodes (pixels p and q), k-scale parameter Threshold term (tau): make it easer to merge smaller regions. The slide includes 2 embedded images alongside the bullets.

## Slide 18 — Scale parameter
Control size of the components. The slide includes 1 embedded image alongside the bullets.

## Slide 19 — SLIC
Simple Linear Iterative Clustering.

## Slide 20 — SLIC
K-means clustering in five-dimensional space Pixel location and RGB/LAB color space (2+3) Compactness parameter control tradeoff between color and space similarity Segments are not necessarily connected Start from many clusters (super pixels) Postprocessing Reassign small disconnected components. The slide includes 2 embedded images alongside the bullets.

## Slide 21 — Quickshift Segmentation
Section divider; the deck transitions to material on quickshift segmentation.

## Slide 22 — Mode pixels
Consider pixels in 5-dim space (RGB/LAB + position) “Ratio” parameter control importance Estimate density around each pixel Connect each pixel to a nearest neighbor with a higher density Become a “parent” of a pixel If non exists, mark as mode (local density maximum) Result in a graph/forest Repeatedly assign to the parent till reaching the mode (tree root). The slide includes 2 embedded images alongside the bullets.

## Slide 23 — Quick Shift
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Quick Shift'.

## Slide 24 — Compare
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Compare'.

## Slide 25 — Low-level segmentation
Not semantic like modern DL-based Break image into coherent regions Usually, preprocessing before other steps Segment medical image into patches, classify each patch.

## Slide 26 — Active Contours (Snakes)
Section divider; the deck transitions to material on active contours (snakes).

## Slide 27 — Active Contour model
Fit open or closed splines (smooth piecewise polynomials) To edges or lines Cubic 2D spline Optimize energy function Fit to image edges, minimize gradient along the spline Maximize smoothness: first/second derivative. Find the best positions of control points that minimize energy Optimize using gradient descent. The slide includes 2 embedded images alongside the bullets.

## Slide 28 — Energy function
Visual slide containing 5 embedded figures with no body text; the visual carries the content of the topic 'Energy function'.

## Slide 29 — GrabCut with OpenCV
Section divider; the deck transitions to material on grabcut with opencv.

## Slide 30 — GrabCut
Model foreground/background with color distributions User provide rectangle around the object Fit color model (GMM) to background and foreground Gaussian Mixture Model User provides labels Sure BG/FG/Probable Create a graph Source: FG terminal Sink: Background terminal Pixels as nodes t-links (price to pay if selected) FG->node: likelihood of BG BG->node: likelihood of FG n-links: neighbors n-links: pixel differences (color position). The slide includes 3 embedded images alongside the bullets.

## Slide 31 — Graph Min-Cut/Max Flow
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Graph Min-Cut/Max Flow'.

## Slide 32 — Interactive segmentation with GrabCut
Initial object bounding box GMM color modeling Mask Pixel labeling. The slide includes 2 embedded images alongside the bullets.

## Slide 33 — OpenCV
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'OpenCV'.

---

## Deck-level takeaway
The deck spans 33 slides, opening with "Image Segmentation" and closing with "OpenCV". Body-text coverage is 58%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Find Markers, Watershed Flooding, Fill Holes and label connected components, Graph-based image segmentation.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3650_Vision_ClassicalSegmentation/3652_IP_Segmentation/slides/`.
