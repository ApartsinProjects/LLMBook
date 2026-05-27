# 3015_IP_ImageSamplingAndQuatization — Per-Slide Summary

**Source file:** `3015_IP_ImageSamplingAndQuatization.pptx`
**Source folder:** `SlidesPool/3010_Vision_ImageFormation/`
**Drive link:** https://drive.google.com/file/d/1fjduv9RR5p_VjNb8zw-lwyJ9um2JAGL3/view
**Slide count (exact, via python-pptx):** 15
**Extraction:** Local parse + slide PNG render. 3 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image Sampling and Quantization
Section divider; the deck transitions to material on image sampling and quantization.

## Slide 2 — Image Projection onto a sensor array
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Image Projection onto a sensor array'.

## Slide 3 — Sampling and Quantization
Sampling: digitizing the image coordinates Quantization: digitizing the amplitude values. The slide includes 1 embedded image alongside the bullets.

## Slide 4 — Representing Digital Images
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Representing Digital Images'.

## Slide 5 — Matrix Form
M-by-N image (MN pixels) Traditional matrix notation. The slide includes 2 embedded images alongside the bullets.

## Slide 6 — Image Storage
M-by-N image L different grey levels, k bits per pixel Need bits total If M=N. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — Image Resolution: Subsampling
Fixed number of bits per pixel Subsampling by omitting columns and rows Hard to compare images. The slide includes 1 embedded image alongside the bullets.

## Slide 8 — Image Resolution: Subsampling +Scaling
Remove every other row and column Upscale by replicating pixels. The slide includes 1 embedded image alongside the bullets.

## Slide 9 — Image vs. Spatial Resolution
Image Resolution: number of pixels Large images could be obtained by interpolation of outputs from smaller sensor arrays Spatial(Sensor) Resolution: distinguishable features Affected by Sensor size (smaller is better) Number of sensors (greater is better) Sensor correlation (smaller is better, depends on optics).

## Slide 10 — Grey-level resolution
Smallest distinguishable change in the grey levels Controlled by quantization Highly Subjective.

## Slide 11 — Reducing number of grey levels
Produces false contouring. The slide includes 2 embedded images alongside the bullets.

## Slide 12 — Zooming and Shrinking
Zooming- is oversampling Shrinking-is undersampling Sampling and quantization is applied to an original continuous image Shrinking and Zooming are applied to the digital image.

## Slide 13 — Zooming
New pixel locations Assign grey levels to those new locations Example 500 by 500 image Want 750 by 750 image Conceptually Lay imaginary 750 by 750 grid over the original image What are the value of pixels on the new grid.

## Slide 14 — Zooming: Grey Level Assignment
Nearest-Neighbor Interpolation Find closest pixels in the original image Pixel replication when zoom by integer factor Bilinear Interpolation Look for 4 closest neighboring pixels. The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Zooming: Bilinear Interpolation
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Zooming: Bilinear Interpolation'.

---

## Deck-level takeaway
The deck spans 15 slides, opening with "Image Sampling and Quantization" and closing with "Zooming: Bilinear Interpolation". Body-text coverage is 73%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Image Storage, Image Resolution: Subsampling, Image Resolution: Subsampling +Scaling, Image vs. Spatial Resolution.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3010_Vision_ImageFormation/3015_IP_ImageSamplingAndQuatization/slides/`.
