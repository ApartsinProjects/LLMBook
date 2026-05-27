# 2041_GenAI_SampleProject — Per-Slide Summary

**Source file:** `2041_GenAI_SampleProject.pptx`
**Source folder:** `SlidesPool/2040_GAI_SampleProjects/`
**Drive link:** https://drive.google.com/file/d/18PKckoZ1DSwG_MoFjrXjIv2XUB2JjQ8G/view
**Slide count (exact, via python-pptx):** 31
**Extraction:** Local parse + slide PNG render. Code-screenshot slides (3-13) and past-project gallery slides (22-31) were inspected visually.

---

## Slide 1 — Skeleton of Course Project
Title slide framing the sample course project as a simplified end-to-end walkthrough.

## Slide 2 — Project Motivation
A motivating use case: rapid dog-breed classification, easy for a veterinary expert but challenging in shelters, customer-facing, or travel settings. Framing it as image classification reveals that no good labeled dataset exists for training and evaluation, so the project must search existing work, generate a dataset, and then train and compare classification methods.

## Slide 3 — Step 1: LLM to generate a list of breeds
A code panel shows prompting an LLM to enumerate dog breeds, producing the class vocabulary for the dataset.

## Slide 4 — Dog Breeds
The slide shows the resulting list of breed names that will drive synthetic image generation.

## Slide 5 — Step 2: Diffusion Model to Generate Dataset
A code panel uses Stable Diffusion to render images of each breed, producing the synthetic training and evaluation set.

## Slide 6 — Images
Two panels display sample generated images across multiple breeds.

## Slide 7 — Step 3: Resize and split
A code panel shows resizing the generated images to a fixed resolution and splitting them into train/validation/test partitions.

## Slide 8 — Step 4: Prepare Numerical Labels
A code panel maps breed names to integer label ids using a Hugging Face label mapping.

## Slide 9 — Step 5: Prepare Classification Pipelines
A code panel shows the candidate classification pipelines under comparison (ResNet, ViT, DINOv2 features plus linear head).

## Slide 10 — Step 6: Training Helpers
A code panel shows utility functions for loss, metrics, and dataloader construction.

## Slide 11 — Step 7: Freeze layers/backbone
A code panel demonstrates freezing the pretrained backbone so only the classification head is trained, with `requires_grad = False` on backbone parameters.

## Slide 12 — Step 8: Prepare Trainer
Two code panels configure a Hugging Face `Trainer` (training arguments, metric callbacks, evaluation strategy).

## Slide 13 — Step 9: Train
Four code panels show the actual training run, including the resulting accuracy curves and confusion-matrix snapshot.

## Slide 14 — Discussion
Section-header slide that opens the reflection on extending the baseline project.

## Slide 15 — Is it a Novel Task/Dataset
The slide encourages searching prior work and asking ChatGPT to check whether the proposed task or dataset is genuinely novel, with two example query screenshots.

## Slide 16 — Adding Novelty
A panel suggests directions for adding novelty (rare breeds, mixed breeds, breed-aware augmentation) on top of the baseline.

## Slide 17 — Diverse Approaches for Synthetic Data Generation
A schematic enumerates alternative synthetic-data strategies (DreamBooth, ControlNet, augmentation pipelines) that could be compared against vanilla SD generation.

## Slide 18 — Robust training
Robustness comes from sweeping training strategies (optimizers, schedulers, learning rates, hyperparameters) and varying which layers and blocks are frozen.

## Slide 19 — Detailed evaluation and model comparison
Two panels showcase richer evaluation: per-breed metrics, error analysis, and qualitative comparisons across models.

## Slide 20 — Other Tasks
A summary panel notes that the same recipe extends to object detection, image restoration, and other tasks beyond classification.

## Slide 21 — Past Student Projects
Section-header slide introducing a gallery of past course projects.

## Slide 22 — Compare Floor Plans
A panel shows a project that compares architectural floor plans using vision representations.

## Slide 23 — Zoom Student Profiling
Three panels showcase a project that profiles online-class students from Zoom video frames.

## Slide 24 — Plant Damage
A panel shows a project detecting damage on plants from leaf imagery.

## Slide 25 — Child Safety: Objects
A panel shows a project detecting dangerous objects in scenes containing children.

## Slide 26 — Vision Through Mud
Two panels show a project that restores or classifies through muddy imagery.

## Slide 27 — Customer-Object Interaction
Two panels show a project analyzing how customers interact with objects in a retail setting.

## Slide 28 — Search-and-Rescue in Storm
Two panels show a search-and-rescue project that classifies aerial imagery captured during storms.

## Slide 29 — Headshot Quality Scoring
A panel shows a project that scores the quality of professional headshots.

## Slide 30 — Robust room re-identification
A panel shows a project that re-identifies rooms across illumination and viewpoint changes.

## Slide 31 — Abandoned Objects in crowded Scenes
Two panels show a project detecting abandoned objects in crowded surveillance footage.

---

## Deck-level takeaway
This is the canonical course-project blueprint. A motivating real-world problem (dog-breed classification) where labeled data is scarce drives a complete pipeline: prompt an LLM for the class vocabulary, generate a synthetic dataset with Stable Diffusion, prepare labels and train/val splits, freeze a pretrained backbone, train a classification head via the Hugging Face Trainer, and evaluate. The discussion then opens the door to novelty (alternative data-generation strategies, robust training sweeps, richer evaluation) and concludes with a long gallery of past student projects spanning floor plans, video profiling, plant damage, child safety, vision through mud, retail analytics, search-and-rescue, headshot quality, room re-identification, and abandoned-object detection.
