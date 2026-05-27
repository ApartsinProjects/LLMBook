# 3013_IP_ColorFundamentals — Per-Slide Summary

**Source file:** `3013_IP_ColorFundamentals.pptx`
**Source folder:** `SlidesPool/3010_Vision_ImageFormation/`
**Drive link:** https://drive.google.com/file/d/1hrstsUq-FnL3EreYYoD8RZcHeQ3rwCUG/view
**Slide count (exact, via python-pptx):** 19
**Extraction:** Local parse + slide PNG render. 3 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Color Fundamentals
Section divider; the deck transitions to material on color fundamentals.

## Slide 2 — Human Color Perception
3 types of cones (6-7 millions) sensitive to primary colors 65% sensitive to red light (575nm) 33% sensitive to green light (535nm) 2% sensitive to blue light (445nm). The slide includes 2 embedded images alongside the bullets.

## Slide 3 — Birds (Pigeons)
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Birds (Pigeons)'.

## Slide 4 — Primary Colors
Represent all light compositions as a combination of the primary colors Red Green Blue Standardized wavelength by CIE Display: Blue (435.1nm), Green (546.1nm), Red (700nm) Approximation to the experimental data Cone responses to a range of wavelengths Can’t generate the perception of all colors. The slide includes 1 embedded image alongside the bullets.

## Slide 5 — Tristimulus: Represent any monochromatic light
Relative amount of Red, Green, and Blue X, Y, Z Mix in different quantities to produce target “color perception.” Trichromatic Coefficients: approximate perceived monochromatic light using primary colors. The slide includes 2 embedded images alongside the bullets.

## Slide 6 — Secondary Colors
Primary colors are a good model for a light source (display RGB pixels) Not very good as a pigment(reflective) color (e.g. print) Red paint absorbs any light but red Combine several of the RGB paints, and most of the light will be absorbed, resulting in a very dark color Use secondary colors as pigments. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — Secondary Colors
Magenta=Red & Blue Subtract green from *white* Cyan=Green &Blue Subtract red from *white* Yellow=Red & Green Subtract blue from *white* Example: Yellow absorbs Blue then Cyan absorbs Red so when printed one over other, white paper only returns back Green. The slide includes 1 embedded image alongside the bullets.

## Slide 8 — CMY and CMYK Color Models
Cyan, Magenta, and Yellow are secondary colors of light or primary colors of pigment A surface coated with cyan reflects no red light Mix of CMY should produce black In practice produces muddy looking black Four color printing CMYK, use black color.

## Slide 9 — Halftoning Printing
Color is defined by relative size of CMYK dots. The slide includes 2 embedded images alongside the bullets.

## Slide 10 — Color Light Characteristics
Brightness- intensity Subjective Hue-dominant wavelength As perceived by an observer Saturation-relative purity of color or amount of white light mixed with a hue Primary colors are fully saturated Pink (red and white mix) is less saturated Hue and Saturation- chromaticity of light Light characterized by brightness and chromaticity.

## Slide 11 — HSI Color Model
RGB/CMY are good for hardware and match the human visual system Not good for describing color Specify car color by trichromatic coefficients? Easier to describe a color by hue, saturation, and brightness (intensity)- HSI.

## Slide 12 — HSI Color Model
Decouples intensity from chromaticity Good for developing image processing algorithms based on color description RGB for color generation, HSI for color description.

## Slide 13 — HSI(HSL) Color Model
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'HSI(HSL) Color Model'.

## Slide 14 — HSI Color Model
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'HSI Color Model'.

## Slide 15 — Representing True Color
Tristimulus representation loses information Can’t represent intensity in all wavelengths of a source by only 3 numbers How to represent the “complete” color information Standard way: SPD-Spectral Power Distribution Power at 31 wavelength region (bands), 10nm each Still approximation but better one then RGB.

## Slide 16 — Human Color Perception
Perceive color by the tristimulus values Different colors (wavelength mixes) may appear to be the same color (metamerism) All SPDs below look the same for an observer. The slide includes 1 embedded image alongside the bullets.

## Slide 17 — Color Image Acquisition
Section divider; the deck transitions to material on color image acquisition.

## Slide 18 — Early 1900’s
http://www.loc.gov/exhibits/empire/. The slide includes 1 embedded image alongside the bullets.

## Slide 19 — Color Images: Bayer Grid
Estimate RGBat ‘G’ cells from neighboring values. The slide includes 2 embedded images alongside the bullets.

---

## Deck-level takeaway
The deck spans 19 slides, opening with "Color Fundamentals" and closing with "Color Images: Bayer Grid". Body-text coverage is 74%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Secondary Colors, CMY and CMYK Color Models, Halftoning Printing, Color Light Characteristics.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3010_Vision_ImageFormation/3013_IP_ColorFundamentals/slides/`.
