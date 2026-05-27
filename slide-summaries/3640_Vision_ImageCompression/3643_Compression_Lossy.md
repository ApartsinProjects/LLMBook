# 3643_Compression_Lossy — Per-Slide Summary

**Source file:** `3643_Compression_Lossy.pptx`
**Source folder:** `SlidesPool/3640_Vision_ImageCompression/`
**Drive link:** https://drive.google.com/file/d/11_zhStnx2-EnezM_7oUTQ1SJjDKYfAHV/view
**Slide count (exact, via python-pptx):** 12
**Extraction:** Local parse + slide PNG render. 1 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — LOSSY-COMPRESSION
Section divider; the deck transitions to material on lossy-compression.

## Slide 2 — Lossy Predictive Coding
Quantize prediction error into a limited range of values. Introduce distortion but improves compression. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Delta Modulation(DM)
Simple predictor Only two possible values for prediction error Need only a single bit to encode differences.

## Slide 4 — Example
Granular noise distortion in smooth region Slope overload distortion when signal is changing too fast. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Optimal Predictors
Optimal predictor minimizes expected squared error Assume f is mean zero. Differentiate m times and equate to zero Solution in matrix form is the vector of coefficients.

## Slide 6 — Optimal Predictor
Autocorrelation Matrix Vectors. The slide includes 2 embedded images alongside the bullets.

## Slide 7 — Global Predictors
Local predictors Compute prediction coefficients for each image Computationally intensive Global predictors Assume some probabilistic model of the image Depends on horizontal/vertical correlation coefficients. Decrease with distance (I,j).

## Slide 8 — Example: 4 possible predictors
Image. The slide includes 5 embedded images alongside the bullets.

## Slide 9 — Example: Prediction Error
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Example: Prediction Error'.

## Slide 10 — Optimal Quantization
Quantization function q(s) Map input (e.g. prediction level) to limited range of output values (L values) For odd q(s) specified by L/2 values of: si,  decision levels ti-reconstruction levels. The slide includes 1 embedded image alongside the bullets.

## Slide 11 — Optimal Quantization
Input probability density function p(s) and number of levels Minimize expected error Should satisfy. The slide includes 1 embedded image alongside the bullets.

## Slide 12 — Lloyd-Max Quantizer
Satisfies Difficult to obtain explicit closed form solution Evaluate numerically. The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 12 slides, opening with "LOSSY-COMPRESSION" and closing with "Lloyd-Max Quantizer". Body-text coverage is 83%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Optimal Predictors, Optimal Predictor, Global Predictors, Example: 4 possible predictors.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3640_Vision_ImageCompression/3643_Compression_Lossy/slides/`.
