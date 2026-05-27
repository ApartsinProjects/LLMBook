# 2222_VisionTaskModels — Per-Slide Summary

**Source file:** `2222_VisionTaskModels.pptx`
**Source folder:** `SlidesPool/2220_GAI_VisionFM/`
**Drive link:** https://drive.google.com/file/d/1__aJUkrilZcrtPog1IpeM09AA8uWce5k/view
**Slide count (exact, via python-pptx):** 24
**Extraction:** Local parse + slide PNG render. Many code-screenshot and gallery slides were inspected visually.

---

## Slide 1 — Pretrained Task-Specific Vision Model
Title slide that introduces pretrained task-specific vision models (classification, detection, segmentation, face analysis).

## Slide 2 — Image Classification
Section-header slide leading into image classification.

## Slide 3 — ImageNet: Large Scale General Purpose
ImageNet is described as the standard large-scale general-purpose dataset with 14M images across 21K classes; the figure shows a sample grid of representative categories.

## Slide 4 — Pretrained Classification Model
The slide shows a schematic of a pretrained ImageNet classifier as a black-box mapping from image to class probabilities, available off-the-shelf in PyTorch and Hugging Face.

## Slide 5 — Fine-tune on custom labels dataset
Three code panels illustrate fine-tuning a pretrained backbone on a custom-labeled dataset by swapping the last layer and continuing training under the user's class vocabulary.

## Slide 6 — Training
Section-header slide that previews the training utilities (Ultralytics and Hugging Face) used in the following code examples.

## Slide 7 — Ultralytics library
A code panel shows the Ultralytics library's one-line classifier-loading and training API for fine-tuning on a custom image dataset.

## Slide 8 — Object Detection
Section-header slide transitioning to detection.

## Slide 9 — Object Detection
Object detection is defined as predicting per-object bounding boxes and class labels. OpenImages v7 is mentioned as a reference dataset with 9M images and 1.9M boxes, and the figure shows detection outputs.

## Slide 10 — Ultralytics: Pretrained Object Detector
A code panel shows loading a pretrained YOLO detector through Ultralytics and running inference on a folder of images.

## Slide 11 — Object Detection: HuggingFace
A code panel shows the equivalent recipe through Hugging Face Transformers, using `AutoModelForObjectDetection` and `AutoImageProcessor` to load and apply DETR-style detectors.

## Slide 12 — HuggingFace: Fine-Tuning with a custom dataset (COCO annotation)
Three code panels show how to fine-tune a Hugging Face detector on a custom COCO-formatted dataset, covering dataset construction, transforms, and the `Trainer` configuration.

## Slide 13 — Fine-tuning with Ultralytics
A code panel shows the equivalent Ultralytics fine-tuning workflow for YOLO models on a `data.yaml` description of a custom dataset.

## Slide 14 — Image Segmentation
Section-header slide transitioning to segmentation.

## Slide 15 — Image Segmentation
The slide differentiates four flavors of segmentation: object segmentation produces a binary foreground/background mask per object; semantic segmentation labels each pixel with a class (sky, cars, people); instance segmentation labels each pixel with an instance id; panoptic segmentation combines both, giving each pixel a class plus an id.

## Slide 16 — Object detection with masks
A schematic shows object detection augmented with per-instance pixel masks, sometimes called instance segmentation.

## Slide 17 — Panoptic Segmentation
A worked example shows panoptic outputs where each pixel carries both a semantic label (chair, floor) and an instance id where applicable.

## Slide 18 — Segment Anything
A figure introduces SAM (Segment Anything Model) and its general-purpose prompted segmentation capability.

## Slide 19 — SAM
SAM is described as a prompted segmentation model that consumes multiple cue types (a point, a box, or a combination) and emits the corresponding object mask.

## Slide 20 — SAM with prompts
The slide visually demonstrates how different prompt types steer SAM to different masks for the same image.

## Slide 21 — FastSAM
FastSAM is presented as a faster SAM variant that additionally supports text prompts for segmentation; two panels show its faster inference and the text-prompt interface.

## Slide 22 — More Tasks
Section-header slide that transitions to additional task families.

## Slide 23 — Face Analysis
Face analysis is split into four tasks: face detection (bounding box), face classification or identification (fixed-vocabulary label), face reidentification (matching against a gallery), and identity validation (matching against a previously registered face).

## Slide 24 — Fine-tuned fashion detection
A worked example shows a YOLO-style detector fine-tuned for fashion-item detection, with side-by-side examples of the model identifying garments in catalog and street imagery.

---

## Deck-level takeaway
Modern computer vision is dominated by pretrained task-specific models that are loaded from public hubs and either used directly or fine-tuned on a small custom dataset. The slides walk through the canonical task families (classification, detection, segmentation variants, face analysis) and contrast Ultralytics (a YOLO-centric library) with Hugging Face Transformers (a broader DETR/SAM ecosystem). SAM and FastSAM appear as the modern general-purpose, prompted segmentation backbones.
