# 3011_IP_HumanVisualSystem — Per-Slide Summary

**Source file:** `3011_IP_HumanVisualSystem.pptx`
**Source folder:** `SlidesPool/3010_Vision_ImageFormation/`
**Drive link:** https://drive.google.com/file/d/1zxt2NNK1sF6AA0oaKpbQI8sdgCN16nKV/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render.

---

## Slide 1 — Why study human visual system (HVS)
Title slide; the only body content is "*curiosity*", lampshading the fact that a computer-vision course is starting from the biology. The implicit answer (filled in by the next slide) is that many decisions in image processing and display are downstream of how humans perceive.

## Slide 2 — Some HVS-driven decisions
Three categories of engineering choices that are driven by the human visual system. *Image acquisition, representation, and compression*: discard information humans cannot perceive (the JPEG/MPEG bet). *Processing*: what is feasible for humans should be feasible for algorithms (a benchmark, not just a constraint). *Displays*: retina-density screens, VR/AR glasses — all designed to the limits of human acuity.

## Slide 3 — Structure of the Human Eye
The eye is a 20 mm diameter sphere. The iris (Hebrew: קֶשֶׁתִית) acts as the camera diaphragm, contracting and expanding to control the light entering. The lens absorbs ultraviolet and infrared. A properly focused eye images light onto the *retina*, where rods and cones live.

## Slide 4 — Retina: Cones
6-7 million cells, concentrated in the central *fovea*. Sensitive to color (3, sometimes 4 receptor types per color response). The eye-rotating muscles aim the eyeball so that the image of interest lands on the fovea. Cones support *photopic* (bright-light) vision and are insensitive to low light.

## Slide 5 — Retina: Rods
75-100 million cells (10-15× more than cones). Several rods connect to a single nerve fiber (spatial pooling that boosts sensitivity at the cost of resolution). Not involved in color vision. Sensitive to very low illumination — the source of *scotopic* (dim-light) vision and the proverb "all cats are grey at night".

## Slide 6 — Retina: Rods vs. Cones
Comparison and a memorable fact: the blind spot has no receptors at all, and the rod+cone density makes the eye "equivalent" to a 52-megapixel camera (a pop-science number, but useful for calibrating intuition about resolution).

## Slide 7 — Image Formation in the eye
The eye as a flexible camera: muscles deform the lens to focus on near or distant objects. The distance from the lens center to the retina (the focal length) varies from 14 to 17 mm depending on focus distance. An image-height formula is sketched. The slide flags that "we will talk more about the equation: pinhole camera and thin-lens camera" — the bridge to the next lectures.

## Slide 8 — Brightness Adaptation and Discrimination
A digital image is a discrete set of intensities. The question: how well can the eye discriminate between intensity levels? The eye can adapt over an enormous intensity range, *but not simultaneously* — similar to a camera adjusting gain (ISO).

## Slide 9 — Subjective (perceived) Brightness
Perceived brightness is *proportional to the log of light intensity* — the Weber-Fechner observation. The full intensity range cannot be perceived simultaneously; instead, an *adaptation level* (the average brightness of the scene) is selected, and all intensities below this floor appear black.

## Slide 10 — Brightness Discrimination (experiment)
The classical psychophysical setup. Look at a flat opaque glass illuminated from behind at intensity I; flash an additional ΔI at the center; record the minimum ΔI such that the change is correctly detected 50% of the time. The ratio ΔI/I is the *Weber ratio*.

## Slide 11 — Brightness Discrimination (Weber's law)
*Weber's law*: at a fixed background, only 10-20 intensity levels are distinguishable by a typical observer. As the eye scans across the image, it adapts to different background levels, so the *total* number of distinguishable intensities across the whole image is much larger than 10-20 — but at any single instant it's small.

## Slide 12 — Perceived brightness (illusions)
Perceived brightness is *not* a simple function of intensity. The visual system *undershoots and overshoots* near intensity boundaries — the phenomenon known as **Mach bands**. A uniform grey patch *appears darker* when the background is lighter. Two illustrative images.

## Slide 13 — Optical Illusions
Closing slide (image-only) — a curated optical illusion that makes the previous slide's point viscerally rather than analytically.

---

## Deck-level takeaway

A 13-slide tour of the human visual system aimed at justifying the engineering choices that come up later in image processing: why JPEG discards what it does, why we model brightness on a log scale, why the discrete intensity quantization of digital images is "good enough" (10-20 distinguishable levels per adaptation), and why perceived brightness is nonlinear in physical intensity (Mach bands, simultaneous contrast). The pedagogical signature is *biology-as-specification*: each slide either describes a piece of the eye or measures a perceptual limit, and the implicit promise is "these are the numbers and laws every later technique will respect or exploit."
