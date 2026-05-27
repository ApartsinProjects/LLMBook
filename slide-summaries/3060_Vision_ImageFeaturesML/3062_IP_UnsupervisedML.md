# 3062_IP_UnsupervisedML — Per-Slide Summary

**Source file:** `3062_IP_UnsupervisedML.pptx`
**Source folder:** `SlidesPool/3060_Vision_ImageFeaturesML/`
**Drive link:** https://drive.google.com/file/d/1-Ke1W_4n_6RMNDl65g-3vPY7GwRFobkG/view
**Slide count (exact, via python-pptx):** 17
**Extraction:** Local parse + slide PNG render. 2 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Classical ML  in Image Processing
Section divider; the deck transitions to material on classical ml  in image processing.

## Slide 2 — Supervised vs. Unsupervised ML
Supervised Model trained on (input, output pairs) Example (image, label) Unsupervised Derive structure from input only Example: cluster similar images.

## Slide 3 — Vector Quantization with K-Means
Section divider; the deck transitions to material on vector quantization with k-means.

## Slide 4 — K-means Clustering
Vector quantization (VQ) Color image: RGB 2^24 colors (24 bits) Reduce to 2^8, 2^4 (8-bit, 4-bit) Assign single color to a cluster. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — VQ with k-Means
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'VQ with k-Means'.

## Slide 6 — Spectral Clustering for image segmentation
With theoretical sketch.

## Slide 7 — Graph Laplacian
Define a weighted graph G=(V,E) Edge weights: similarity between I and j Laplacian Similarity matrix Degree matrix Suppose each graph has a value(x) associated Given a vector of all node values LX is a weighted difference of the node from all others Value is Large for nodes that are different from neighbors Normalize for account nodes with larger degree. The slide includes 5 embedded images alongside the bullets.

## Slide 8 — Cuts and Normalized Cuts
Minimal cut problem: minimize along A and B Minimal normalized cuts balance cost and cluster volume NP-hard. The slide includes 2 embedded images alongside the bullets.

## Slide 9 — Spectral relaxation
Encode partition as an indicator vector Positive and negative values a=+1, b=-1, some scaling applies Relaxation, find an approximation to the indicator vector under constraints Split edge weights equally Normalized values Minimize cut. The slide includes 7 embedded images alongside the bullets.

## Slide 10 — Spectral Relaxation of NCut
Encode partition as an indicator vector Positive and negative values a=+1, b=-1 Some scaling applies Find optima Constraints Balance nodes between clusters (not all in one cluster) Split total edge weights. The slide includes 3 embedded images alongside the bullets.

## Slide 11 — Eigenvalue solution
Lagrangian multipliers Take derivatives and set to zero, use constraints Eigenvector is the solution Corresponding to the second smallest eigenvalue All eigenvalues are non-negative for a graph Laplacian Zero eigenvalue: no partition, second smallest: best non-trivial 2-way cut Threshold assignment vector for partition label Extend to k-way clustering Non-trivial method (cluster using first k eigenvalues). The slide includes 2 embedded images alongside the bullets.

## Slide 12 — Spectral Clustering
Construct graph: Neighboring graph+ pixel value similarity weights. The slide includes 3 embedded images alongside the bullets.

## Slide 13 — PCA and Eigenfaces
Section divider; the deck transitions to material on pca and eigenfaces.

## Slide 14 — PCA
Rotate multidimensional data Order variance from largest to smallest Decorrelate dimensions Usage Reduce dimensionality Represent as linear combination of basis vectors. The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Eigenfaces
Space of all faces 64x64 image is a 4096-dim vector Represent each image as a linear combination of basis vectors First 10 Eigenfaces. The slide includes 1 embedded image alongside the bullets.

## Slide 16 — PCA on Faces
With 64 components it’s possible to explain 90% of variance. The slide includes 4 embedded images alongside the bullets.

## Slide 17 — Reconstruction
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Reconstruction'.

---

## Deck-level takeaway
The deck spans 17 slides, opening with "Classical ML  in Image Processing" and closing with "Reconstruction". Body-text coverage is 71%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Spectral Clustering for image segmentation, Graph Laplacian, Cuts and Normalized Cuts, Spectral relaxation.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3060_Vision_ImageFeaturesML/3062_IP_UnsupervisedML/slides/`.
