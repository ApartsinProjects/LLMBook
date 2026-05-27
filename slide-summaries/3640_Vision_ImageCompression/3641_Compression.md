# 3641_Compression — Per-Slide Summary

**Source file:** `3641_Compression.pptx`
**Source folder:** `SlidesPool/3640_Vision_ImageCompression/`
**Drive link:** https://drive.google.com/file/d/1GhNh_jnCkho5qDgK4LWMpiy6PBU143yQ/view
**Slide count (exact, via python-pptx):** 24
**Extraction:** Local parse + slide PNG render. 3 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Digital Image processing
8.Image Compression.

## Slide 2 — Fundamentals
Data compression=reducing amount of data required to represent a given quantity of information Data <> Information. Data are means by which information is conveyed Tell the same story using less words Words that do not provide additional information are redundant (data redundancy).

## Slide 3 — Data Redundancy
Assume n1, n2 are number of information-carrying units in two data sets that represent the same information The relative data redundancy and compression ratio No redundancy Highly redundant.

## Slide 4 — Redundancy In Images
Coding redundancy Less bits on average to encode an individual pixel Interpixel redundancy Less bits on average to encode pixel groups Psychovisual redundancy Less bits on average to represent same visual information.

## Slide 5 — Coding Redundancy
Assign shorter codes to more frequent gray levels Compute gray level histogram Code length for pixel value rk is l(rk) Average bits per pixels.

## Slide 6 — Example
8 possible gray levels encoded with fixed 3 bits code or. The slide includes 2 embedded images alongside the bullets.

## Slide 7 — Selecting Code
Code length is inversely proportional to gray level frequency. The slide includes 1 embedded image alongside the bullets.

## Slide 8 — Interpixel Redundancy
Consider two images with almost identical histograms In the bottom image, it’s more probable that the pixel above a give pixel has the same gray level. This more probable pair can be encoded using less bits than other pairs. The slide includes 2 embedded images alongside the bullets.

## Slide 9 — Measuring difference between 2 R.V
Assume x, y are two random variable with std=1, mean=0 How do we measure their similarity? x is large when y is large (with high prob.)? X is large when y is small (with high prob.)? Are they *independent* Define Is small=>x,y have similar values(*usually*) Is large=>x,y have very different values (*usually*) Is intermediate=> *usually* are not related Simplify.

## Slide 10 — Correlation Coefficient
Difference Define covariance Define correlation coefficient In our case If is small, the difference is large and vice versa Use correlation coefficient to measure similarity between the r.v.

## Slide 11 — Autocorrelation Function
Consider gray level of pixel at (x,y) and gray level of pixel at (x+m,y+n) Autocorrelation coefficient. The slide includes 1 embedded image alongside the bullets.

## Slide 12 — Interpixel Redundancy
A value at each individual pixel can be guessed from its neighbors Contribution (to the information) of each individual pixel is small Different names Spatial redundancy Geometric redunancy Interframe redundancy.

## Slide 13 — Reversible Mapping
Exploit interpixel redundancy by transforming image into more suitable representation Image can be reconstructed “Decompose into pixel groups” and encode them Example: run-length encoding.

## Slide 14 — Example: Binary Image by Thresholding
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Example: Binary Image by Thresholding'.

## Slide 15 — Line Profile
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Line Profile'.

## Slide 16 — Run-length encoding
Line profile of a binary (thresholded) image contains many regions of constant intensity Encode each line by a sequence of pairs Gray level and length of the region (run). The slide includes 1 embedded image alongside the bullets.

## Slide 17 — Example: RLE
1024 pixel in line (1024 bits un-encoded) 88 bits for 8 runs (11 bits per run) Entire 1024x343 section requires 12166 runs. The slide includes 4 embedded images alongside the bullets.

## Slide 18 — Psychovisual Redundancy
Perceived brightness of the region depends on other factors that are simply the light reflected An eye does not respond to with equal sensitivity to all visual information Some information is less important for normal visual processing (by humans) Psychovisually redundant information.

## Slide 19 — Psychovisual Redundancy
Elimination of psychovisual redundant data may result in a loss of quantitative information The process of elimination of psychovisual redundancy is frequently called quantization Mapping of a broad range of values into a limited (visually important) set of values.

## Slide 20 — Example
Reduce 256 gray levels to 16 possible levels (compression ratio is 2) Some false contouring. The slide includes 1 embedded image alongside the bullets.

## Slide 21 — Improved Gray Scale Quantization
Break contours by adding a pseudo-random number to low-order bits Introduce slight variation at neighboring pixels Same amount of bits, better visuals. The slide includes 1 embedded image alongside the bullets.

## Slide 22 — Fidelity criteria
Objective criteria Quantitative information loss Subjective criteria Visual information loss.

## Slide 23 — Objective Criteria
Error at each pixel Total error Root-Mean-Square error (RMS) Mean-square signal-to-noise ratio (SNR). The slide includes 1 embedded image alongside the bullets.

## Slide 24 — Subjective Fidelity Criteria
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Subjective Fidelity Criteria'.

---

## Deck-level takeaway
The deck spans 24 slides, opening with "Digital Image processing" and closing with "Subjective Fidelity Criteria". Body-text coverage is 88%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Measuring difference between 2 R.V, Correlation Coefficient, Autocorrelation Function, Interpixel Redundancy.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3640_Vision_ImageCompression/3641_Compression/slides/`.
