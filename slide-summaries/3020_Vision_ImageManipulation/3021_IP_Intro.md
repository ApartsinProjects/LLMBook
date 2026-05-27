# 3021_IP_Intro — Per-Slide Summary

**Source file:** `3021_IP_Intro.pptx`
**Source folder:** `SlidesPool/3020_Vision_ImageManipulation/`
**Drive link:** https://drive.google.com/file/d/1MBouEm7_zB4i2iYIOYvl5Op_fun2fqgk/view
**Slide count (exact, via python-pptx):** 26
**Extraction:** Local parse + slide PNG render. 14 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image Processing
1. Libraries, Input-Output, Formats and Classes.

## Slide 2 — An image is a multidimensional array
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'An image is a multidimensional array'.

## Slide 3 — Python Image Library
[TABLE] Library | Representation | Typical shape / structure | What it is best for PIL / Pillow | PIL.Image.Image object | Stores image metadata plus pixel data; uses image mode such as L, RGB, RGBA, CMYK | Loading, saving, format conversion, basic edits scikit-image (skimage) | numpy.ndarray | Grayscale usually (H, W), color usually (H, W, C) | Image processing, segmentation, filters, measurement scipy.ndimage | Array-like input, typically numpy.ndarray | Any dimensionality: 2D, 3D, volumes, stacks, labels | Filtering, morphology, interpolation, labeling, measurements matplotlib.image / plt.imread | numpy.ndarray | (M, N) for grayscale, (M, N, 3) for RGB, (M, N, 4) for RGBA | Displaying images, simple reading for plotting workflows. The slide includes 1 table alongside the bullets.

## Slide 4 — Relevant Python Libraries: PIL, Skimage, SciPy, Matplotlib
PIL: Pillow Python Library. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Pillow
Section divider; the deck transitions to material on pillow.

## Slide 6 — Read and Display
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Read and Display'.

## Slide 7 — Convert to Grayscale
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Convert to Grayscale'.

## Slide 8 — Matplotlib
Section divider; the deck transitions to material on matplotlib.

## Slide 9 — Matplotlib.image
Return a NumPy ndarray with pixel values between 0 and 1. The slide includes 2 embedded images alongside the bullets.

## Slide 10 — Manipulate Images
Set pixels below 0.5 to 0. The slide includes 2 embedded images alongside the bullets.

## Slide 11 — Image scaling
Showing 50x50 image on a large screen Interpolate pixels. The slide includes 2 embedded images alongside the bullets.

## Slide 12 — Image Interpolation Methods
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Image Interpolation Methods'.

## Slide 13 — Scikit-Image
Section divider; the deck transitions to material on scikit-image.

## Slide 14 — Read Image
NumPy ndarry of unit8. The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Representing Color: HSV color space
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Representing Color: HSV color space'.

## Slide 16 — Change Saturation
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Change Saturation'.

## Slide 17 — Built-in Datasets
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Built-in Datasets'.

## Slide 18 — Misc in scipy
Mostly depriciated.

## Slide 19 — Build-in Dataset
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Build-in Dataset'.

## Slide 20 — Reading Images
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Reading Images'.

## Slide 21 — Image Formats
Section divider; the deck transitions to material on image formats.

## Slide 22 — Converting
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Converting'.

## Slide 23 — COLOR->GRAY
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'COLOR->GRAY'.

## Slide 24 — Color Space Conversions
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Color Space Conversions'.

## Slide 25 — Change Image Class: PIL->NDARRAY
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Change Image Class: PIL->NDARRAY'.

## Slide 26 — NDARRAY->PIL
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'NDARRAY->PIL'.

---

## Deck-level takeaway
The deck spans 26 slides, opening with "Image Processing" and closing with "NDARRAY->PIL". Body-text coverage is 31%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Matplotlib.image, Manipulate Images, Image scaling, Image Interpolation Methods.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3020_Vision_ImageManipulation/3021_IP_Intro/slides/`.
