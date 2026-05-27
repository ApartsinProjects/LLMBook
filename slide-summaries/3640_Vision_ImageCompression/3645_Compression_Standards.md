# 3645_Compression_Standards — Per-Slide Summary

**Source file:** `3645_Compression_Standards.pptx`
**Source folder:** `SlidesPool/3640_Vision_ImageCompression/`
**Drive link:** https://drive.google.com/file/d/1u50GiptDP8HRmtSEi2zqBtcMkI0JNlXR/view
**Slide count (exact, via python-pptx):** 4
**Extraction:** Local parse + slide PNG render. 0 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image COMPRESSION STANDARDS
Section divider; the deck transitions to material on image compression standards.

## Slide 2 — Binary Image Compression Standards
CCITT-Run Length. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Continuous Tone Image Compression
JPEG DCT transform on 8-by-8 sub-images Quantize each coefficient Using quantization matrix (defined by standard) Reorder using zig-zag pattern Produce many trailing zeroes Encode DC using predictive coding RLE the linear sequence (compress zero runs) Huffman coding on what is left JPEG2000 Use wavelet transform PNG/GIF- lossless with LZW-like compression.

## Slide 4 — Video Compression
Interframe redundancy Previous frame is a good predictor of the next one I-frame DCT encoded key frames (like stills) P-frame Predicted difference from the previous (P or I) frame Motion vector per block (where it has moved ) relative to a previous frame Difference between the motion compensated block and the corresponding block in the previous frame B-Frame Prediction based on past or future Next I-frame may be a better predictor.

---

## Deck-level takeaway
The deck spans 4 slides, opening with "Image COMPRESSION STANDARDS" and closing with "Video Compression". Body-text coverage is 75%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Binary Image Compression Standards.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3640_Vision_ImageCompression/3645_Compression_Standards/slides/`.
