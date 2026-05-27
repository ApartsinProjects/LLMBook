# 3002_CousreProject — Per-Slide Summary

**Source file:** `3002_CousreProject.pptx`
**Source folder:** `SlidesPool/3000_Vision_Intro/`
**Drive link:** https://drive.google.com/file/d/1Dv31pRgr0koVyu1g-6hkVeX1VTMVV0_J/view
**Slide count (exact, via python-pptx):** 35
**Extraction:** Local parse + slide PNG render. 27 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Image Processing/Vision Course Project
Objective: evaluate the robustness of image processing and vision algorithms/models Select a public dataset: KITTI,…, Select 3 tasks: Corner-detection, Object Detection, … Select a model/algorithm for each task For each task/dataset combination: Baseline: measure performance on clean images Distortion: apply distortions (noise, rain, low-light) and measure degradation of methods Improvement: Try to measure two approaches Enhance distorted images during pre-processing (denoise, de-rain, …) Fine-tune models (for DL based methods) Detailed requirements/instructions are published Read carefully.

## Slide 2 — 1. Prepare Dataset and a sample
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic '1. Prepare Dataset and a sample'.

## Slide 3 — Plot sample with labels
Code walkthrough slide. The figure on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Plot sample with labels').

## Slide 4 — Result
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 5 — Run ORB feature detector
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Run ORB feature detector').

## Slide 6 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 7 — Run Pretrained Object Detection
Code walkthrough slide. The figure on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Run Pretrained Object Detection').

## Slide 8 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 9 — Run Pretrained Segmentation
Code walkthrough slide. The figure on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Run Pretrained Segmentation').

## Slide 10 — Display
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Display'.

## Slide 11 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 12 — Compute IoU metric
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Compute IoU metric').

## Slide 13 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 14 — Introducing Distortions
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Introducing Distortions'.

## Slide 15 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 16 — Features on Noisy Images
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Features on Noisy Images'.

## Slide 17 — Dark Images
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Dark Images'.

## Slide 18 — Measuring Feature Matching Accuracy
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Measuring Feature Matching Accuracy'.

## Slide 19 — degradation level ->SNR
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'degradation level ->SNR'.

## Slide 20 — Performance per SNR
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 21 — Performance per SNR
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 22 — Enhancing Images
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Enhancing Images'.

## Slide 23 — Results: Noise
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 24 — Results: Low Light
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 25 — Run on enhanced images
Code walkthrough slide. The figure on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Run on enhanced images').

## Slide 26 — Comparing results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 27 — Fin-Tuning Model: Create Labels from Clean
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Fin-Tuning Model: Create Labels from Clean'.

## Slide 28 — Fine-Tune YOLO
Code walkthrough slide. The figures on the slide are screenshots of Python/notebook code implementing the action named in the title; the title itself states the step ('Fine-Tune YOLO').

## Slide 29 — Project Choices
Section divider; the deck transitions to material on project choices.

## Slide 30 — Project Outcomes
Section divider; the deck transitions to material on project outcomes.

## Slide 31 — This PPT skips (but your project must have)
Section divider; the deck transitions to material on this ppt skips (but your project must have).

## Slide 32 — Advices
Section divider; the deck transitions to material on advices.

## Slide 33 — Submission
Section divider; the deck transitions to material on submission.

## Slide 34 — Requirements
A dataset with GT for at least one task At least 3 different tasks: include low-level and high-level tasks At least one DL model At least 3 distortion methods Measure performance: per class, per SNR Document (in your ReadMe) Your choices Tables of results/metrics Visualization Input/Output processing steps: Image with annotation, before/after Measurements: plot bar plot, curves, comparisons.

## Slide 35 — Suggested Weekly Plan
[TABLE] Week | Task | Artifact 1 | Form team, open Git, register | Opened GitHub repo, entry in course project table 2 | Research and select: dataset, distortions, tasks | A table with decisions embedded in ReadMe (with links) 3 | Research and select: methods and enhancements | A table with decisions embedded in ReadMe (with links) 4 | Download data, visualize images, and annotations | Download and EDA code, sample image grid with annotations embedded in ReadMe 5 | Run methods/models on clean data and save outcomes | Folder with outcomes/labels in repo 6 | Measure performance of selected method using GT | Table of results, visualization per class 7 | Apply distortions and save data | Distortion code, data folder with distorted images, visualization of before/after 8 | Run models and measure degradation in performance | Code of model application, tables of performance, visuals of image annotations and performance comparison 9 | Apply enhancements and measure performance | Visuals of images/with annotations, side-by-side grid, visuals of performance comparison 10 | Fine-Tune model(s) | Code of fine-tuned models, checkpoint/model weights 11 | Measure performance of Fine-Tuned model(s) | Table of results in Git, visualization 12 | Review ReadMe so far, improve visualization, text, tables | Improved, rich, informative, detailed ReadMe with all decisions and visualization 13 | Prepare and upload PPT, Review Repo | Full repo, Slides (PPT and PDF). The slide includes 1 table alongside the bullets.

---

## Deck-level takeaway
The deck spans 35 slides, opening with "Image Processing/Vision Course Project" and closing with "Suggested Weekly Plan". Body-text coverage is 9%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Compute IoU metric, Results, Introducing Distortions, Results.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3000_Vision_Intro/3002_CousreProject/slides/`.
