# 3644_Compression_TransformCoding — Per-Slide Summary

**Source file:** `3644_Compression_TransformCoding.pptx`
**Source folder:** `SlidesPool/3640_Vision_ImageCompression/`
**Drive link:** https://drive.google.com/file/d/1huPGnMIgTbxs4AEJN3dW3y7bd6VDgCfl/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render. 2 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — TRANSFORM CODING
Section divider; the deck transitions to material on transform coding.

## Slide 2 — Transform Coding
Map image into a set of transform coefficients. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Transform Selection
Two major consideration Computational complexity Information packing (more information in less coefficients) Example: DFT transform.

## Slide 4 — Walsh-Hadamard Transform
Binary (-1,1) base functions. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Discrete Cosine Transform(DCT)
In-between DFT and WHD in terms of computational complexity. The slide includes 2 embedded images alongside the bullets.

## Slide 6 — Information Packing
Compression is by discarding or quantizing less significant coefficients Introduce error(distortion) For *good* transformations Look for transformation that have most of the variance in smaller number of coefficients (information packing) KLT transform (computationally heavy) DCT is a good compromise between information packing and computational complexity.

## Slide 7 — Bit Allocation
Which coefficient to discard? How many bits allocate for each coefficient (precision) Zonal Coding Scheme Coefficients with large variance are important Non-adaptive (computed once using sample data set) Threshold Coding Scheme Coefficient of large magnitude are important Adaptive (ordered for each image).

## Slide 8 — Zonal Coding
Zonal Mask- which coefficient to retain Encode each coefficient using fixed number of bits (divide by its variance first). The slide includes 1 embedded image alongside the bullets.

## Slide 9 — Zonal Coding
Variable Bit Allocation proportional to the estimated variance. The slide includes 1 embedded image alongside the bullets.

## Slide 10 — Threshold Coding
Select largest transform coefficient (might be different per image) Reorder to a linear sequence Encode non-zeros using variable length codes. The slide includes 2 embedded images alongside the bullets.

## Slide 11 — WAVELET CODING
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'WAVELET CODING'.

## Slide 12 — WAVELET CODING
No decomposition into smaller subimages is required Why? Flexibility Choose wavelet Choose number of decomposition levels? Bonus Some correlation across decomposition levels Bands are scaled version of each of each other Use Huffman for final symbol coding steps.

## Slide 13 — Example
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Example'.

---

## Deck-level takeaway
The deck spans 13 slides, opening with "TRANSFORM CODING" and closing with "Example". Body-text coverage is 77%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Discrete Cosine Transform(DCT), Information Packing, Bit Allocation, Zonal Coding.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3640_Vision_ImageCompression/3644_Compression_TransformCoding/slides/`.
