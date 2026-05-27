# 2462_StableDiffusion_LoRA — Per-Slide Summary

**Source file:** `2462_StableDiffusion_LoRA.pptx`
**Source folder:** `SlidesPool/2460_GAI_StableDiffusionFT/`
**Drive link:** https://drive.google.com/file/d/17YK7Ztqvb_PNYe1XdIam1tv-PLDBFtFa/view
**Slide count (exact, via python-pptx):** 5
**Extraction:** Local parse + slide PNG render. Text on the reminder and fine-tuning slides was visually inspected (no body text in struct).

---

## Slide 1 — Training with LoRA
Title slide introducing LoRA as the fine-tuning method for Stable Diffusion in this section.

## Slide 2 — Reminder: LoRA
The slide visually recaps Low-Rank Adaptation: a frozen weight matrix W is augmented with two small trainable matrices A (down-projection) and B (up-projection) whose product BA injects a low-rank update; only A and B are optimized, leaving the base model frozen.

## Slide 3 — Fine-tuning SD with LoRA
LoRA adapters are added to two components of Stable Diffusion: the UNet and the text encoder. The slide points to the diffusers example script `examples/text_to_image/train_text_to_image_lora.py` for a working full-model fine-tuning recipe.

## Slide 4 — Fine-Tuning
The slide shows code and configuration screenshots for invoking the LoRA training script, illustrating where rank, alpha, learning rate, and which submodules receive adapters are specified.

## Slide 5 — Loading 3rd party adapters
The slide demonstrates loading externally trained LoRA adapters on top of a standard Stable Diffusion model, showing three small code snippets that fetch and attach community LoRA checkpoints to drive new styles or characters without retraining the base.

---

## Deck-level takeaway
LoRA enables cheap personalization of Stable Diffusion by inserting low-rank trainable adapters into the UNet and text encoder while freezing the base weights. The diffusers `train_text_to_image_lora.py` script standardizes training, and the resulting (or third-party) adapters can be loaded at inference time to swap styles and concepts in seconds.
