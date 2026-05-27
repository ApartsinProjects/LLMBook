# 2461_StableDiffusion_FullTuning — Per-Slide Summary

**Source file:** `2461_StableDiffusion_FullTuning.pptx`
**Source folder:** `SlidesPool/2460_GAI_StableDiffusionFT/`
**Drive link:** https://drive.google.com/file/d/1QGdAmxeil1KX5_C5Ul7ZOOPuSbWQFoyX/view
**Slide count (exact, via python-pptx):** 14
**Extraction:** Local parse + slide PNG render. Section headers (1, 3, 10) and code-screenshot slides (8, 9, 14) were inspected visually.

---

## Slide 1 — Fine-Tuning Stable Diffusion
Title slide that opens the fine-tuning unit.

## Slide 2 — SD Fine-Tuning objectives
The slide distinguishes two fine-tuning goals: adapting SD to a new visual domain (medical, anime, product photos), and teaching SD new concepts (specific people, objects, or styles). The recipes that follow target the first goal at full-model granularity.

## Slide 3 — Full Stable Diffusion Fine-tuning
Section-header slide that transitions into full-model fine-tuning.

## Slide 4 — Full stable diffusion: text-to-image
Full fine-tuning changes every weight of the model to produce images in a new domain. The training data is text-image pairs, no parameter-efficient adapter such as LoRA is used, and the recipe requires at least 16 GB of VRAM.

## Slide 5 — Example
A worked example fine-tunes SD to generate images of stars using Hubble telescope datasets. The slide shows a representative output from the resulting model.

## Slide 6 — Preparing the dataset
The slide gives practical data-prep guidance: 500 images is often enough; image-to-text models can auto-caption; data is collected by crawling and scraping (Scrapy + BeautifulSoup); and everything is loaded into a Hugging Face Dataset object.

## Slide 7 — HuggingFace Accelerate
Hugging Face Accelerate is introduced as the training launcher. It abstracts CPU/GPU placement, multi-GPU training, and mixed precision, and exposes command-line utilities that run any accelerator-ready Python script across heterogeneous hardware.

## Slide 8 — Full Diffusion Model Fine-Tuning
The slide shows command-line invocations from the diffusers `examples/text_to_image` directory, including the canonical `accelerate launch train_text_to_image.py` command with its dataset and learning-rate flags.

## Slide 9 — Inference
Code snippets show how to load the fine-tuned checkpoint with `StableDiffusionPipeline.from_pretrained` and generate images from prompts targeted at the new domain.

## Slide 10 — Training ControlNet with custom control signal
Section-header slide that pivots to fine-tuning ControlNet for custom control signals.

## Slide 11 — Reminder: ControlNet
A brief recap restates that ControlNet adds conditioning via images (pose, edges, depth, segmentation), encoded as image inputs.

## Slide 12 — Learn to modify the hidden outputs of each up-sample layer
A schematic shows the ControlNet branch injecting additive deltas into each up-sample layer of the frozen SD UNet.

## Slide 13 — Example
A worked example trains ControlNet on a facial-landmark control signal, demonstrating that custom controls beyond the canonical ones can be learned with a small dataset.

## Slide 14 — Training Script
The slide shows the diffusers `train_controlnet.py` script invocation, highlighting the flags that select the control image, the base SD checkpoint, and the training schedule.

---

## Deck-level takeaway
Full fine-tuning of Stable Diffusion changes every weight and is the right tool when adapting to a new domain (medical, anime, astronomy) rather than learning a single concept. The diffusers `train_text_to_image.py` script paired with Hugging Face Accelerate handles the heavy lifting (mixed precision, multi-GPU), and the same infrastructure trains custom ControlNets on bespoke control signals such as facial landmarks.
