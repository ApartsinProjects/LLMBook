# 3001_TypicalVisionTasks — Per-Slide Summary

**Source file:** `3001_TypicalVisionTasks.pptx`
**Source folder:** `SlidesPool/3000_Vision_Intro/`
**Drive link:** https://drive.google.com/file/d/17TSe0tZ2C4WakmGOp4BQ4V2qHOvYZbBI/view
**Slide count (exact, via python-pptx):** 33
**Extraction:** Local parse + slide PNG render. 23 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Vision Processing Tasks
Section divider; the deck transitions to material on vision processing tasks.

## Slide 2 — Source of image data
Section divider; the deck transitions to material on source of image data.

## Slide 3 — Digital Image: Where it comes from?
Scene. Imaging System (Camera). Digital Image in a Computer.

## Slide 4 — Digital Image == Array of Numbers
The slide shows a small RGB picture exploded into three colour-channel planes (red, green, blue) with the per-pixel integer matrices overlaid. The message is the conceptual definition: a digital image is literally a stack of integer arrays, one per channel, and every vision algorithm ultimately operates on these numbers.

## Slide 5
Scene or scene representation. Imaging System (Camera). Digital Image in a Computer. Computer Vision: Infer details of the scene from its imagery. Computer Graphics: generate synthetic imagery from scene description.

## Slide 6
Scene or scene representation. Imaging System (Camera). Digital Image in a Computer. Image Processing: enhance image or recover its properties. Computational Geometry*: infer properties of the scene from its representation.

## Slide 7 — Continuum from low-level to high level tasks
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Continuum from low-level to high level tasks'.

## Slide 8 — Low-Level processing
Image Processing Tasks.

## Slide 9 — Image Enhancements
A two-column reference table of common enhancement tasks (denoising, deblurring, super-resolution, contrast enhancement, color correction, low-light enhancement, JPEG artifact removal, image debanding, dehazing, defogging, image sharpening, exposure correction, HDR reconstruction, reflection removal, underwater image enhancement, illumination correction) paired with one-line definitions, plus before/after photographic examples (foggy versus clear scene, low-light portrait).

## Slide 10 — Image Compression
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Image Compression'.

## Slide 11 — Interest Point Detection
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Interest Point Detection'.

## Slide 12 — Geometric Features Detection
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Geometric Features Detection'.

## Slide 13 — High-Level processing
Computer Vision Tasks.

## Slide 14 — Image Classification
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Image Classification'.

## Slide 15 — Object Detection
Contrasts image recognition (single label "Dog" assigned to an entire image of a puppy) with object detection (bounding boxes drawn around a "Person" and a "Cat" in a multi-subject scene). The pedagogical point is that object detection localises *and* classifies, producing one labelled box per instance.

## Slide 16 — Segmentation
A four-panel comparison of segmentation flavours: (a) input image of a family on a beach, (b) semantic segmentation (every "person" pixel painted the same colour), (c) instance segmentation (each individual person painted a distinct colour while still being a "person"), and (d) panoptic segmentation (instance labels for things plus semantic labels for stuff). A side panel defines instance segmentation as labelling each pixel by class id ("all cars are 'car'") without distinguishing instances, and panoptic segmentation as labelling each pixel by class *and* instance.

## Slide 17 — Depth Estimation
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Depth Estimation'.

## Slide 18 — 3D Reconstruction
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic '3D Reconstruction'.

## Slide 19 — Anomaly Detection
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Anomaly Detection'.

## Slide 20 — Pose Estimation
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Pose Estimation'.

## Slide 21 — Object Reidentification
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Object Reidentification'.

## Slide 22 — Gaze Estimation
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Gaze Estimation'.

## Slide 23 — Gesture Recognition
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Gesture Recognition'.

## Slide 24 — Video Tasks
Section divider; the deck transitions to material on video tasks.

## Slide 25 — Multimodal  and Generative Tasks
Generative Computer Vision.

## Slide 26 — Text-to-Image
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Text-to-Image'.

## Slide 27 — Image Captioning
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Image Captioning'.

## Slide 28 — Visual Question-Answering
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Visual Question-Answering'.

## Slide 29 — Text-based image Editing
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Text-based image Editing'.

## Slide 30 — Image inpainting
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Image inpainting'.

## Slide 31 — Super-Resolution
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Super-Resolution'.

## Slide 32 — Image Style Transfer
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Image Style Transfer'.

## Slide 33 — Representing signals as images
Many ways to encode a signal as an image. STFT The slide includes 1 embedded image alongside the bullets.

---

## Deck-level takeaway
The deck spans 33 slides, opening with "Vision Processing Tasks" and closing with "Representing signals as images". Body-text coverage is 21%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include High-Level processing, Image Classification, Object Detection, Segmentation.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3000_Vision_Intro/3001_TypicalVisionTasks/slides/`.
