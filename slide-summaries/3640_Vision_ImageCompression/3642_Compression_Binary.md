# 3642_Compression_Binary — Per-Slide Summary

**Source file:** `3642_Compression_Binary.pptx`
**Source folder:** `SlidesPool/3640_Vision_ImageCompression/`
**Drive link:** https://drive.google.com/file/d/1tcJpP-SgHYB_EqSvM-9tTEA7op_krxYt/view
**Slide count (exact, via python-pptx):** 8
**Extraction:** Local parse + slide PNG render. 2 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Binary IMAGE COMPRESSION
Section divider; the deck transitions to material on binary image compression.

## Slide 2 — Constant Area Coding (CAC)
Divide binary image into p-by-q blocks Assign 3 categories to each block White, Black, Mixed Encode white/black blocks with 1-2 bit codewords Use 2 bit prefix for mixed block to encode mixed content White Block Skipping (WBS) -a simple version for predominantly white documents (e.g. scanned text) 0 for all white areas 1 prefix for all other areas Iterative approach: continue to divide mixed blocks into smaller areas.

## Slide 3 — Run-Length Coding
Used in FAX coding starting from 1950s Encode line by line. Use pairs (value, run-length) Use variable-length coding to encode run (e.g. longer white runs are more probable in handwritten text).

## Slide 4 — GRAY IMAGE CODING
Section divider; the deck transitions to material on gray image coding.

## Slide 5 — Lossless Predictive Coding
Explore interpixel redundancy Code only for pixel differences Code only for new information in each pixel Predict value of a next pixel Encode only a difference from the predicted value.

## Slide 6 — Predictive Coding
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Predictive Coding'.

## Slide 7 — Linear Predictor
Linear combination of previous values Estimate parameters (prediction coefficients, order m) from the data.

## Slide 8 — Example: LPC
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Example: LPC'.

---

## Deck-level takeaway
The deck spans 8 slides, opening with "Binary IMAGE COMPRESSION" and closing with "Example: LPC". Body-text coverage is 50%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Run-Length Coding, GRAY IMAGE CODING, Lossless Predictive Coding.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3640_Vision_ImageCompression/3642_Compression_Binary/slides/`.
