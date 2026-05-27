# 2445_StableDiffsuion_InstructionEditing — Per-Slide Summary

**Source file:** `2445_StableDiffsuion_InstructionEditing.pptx`
**Source folder:** `SlidesPool/2440_GAI_DiffusionApps/`
**Drive link:** https://drive.google.com/file/d/1SkgMbLJx9Ro4Dk-1yumd4oVbiF0Al1Uj/view
**Slide count (exact, via python-pptx):** 7
**Extraction:** Local parse + slide PNG render. Text bodies were captured directly; slides without body text were visually inspected.

---

## Slide 1 — Instruction Image Editing
Title slide introducing InstructPix2Pix-style instruction-driven image editing built on top of Stable Diffusion.

## Slide 2 — Editing instructions
The slide describes the training setup. The model is fine-tuned on triplets of (source image, editing instruction, edited image); the source image is provided as additional input channels so the UNet's latent input becomes an 8-channel 64x64 tensor combining noise with the encoded source.

## Slide 3 — Implementation
The slide shows three code or schematic panels detailing how to extend the UNet input to accept extra source-image channels and how the editing-instruction text is fed through the text encoder as the conditioning prompt.

## Slide 4 — Examples
A gallery of edited images illustrates instruction-following behavior across operations such as object swaps, season changes, and style transfers.

## Slide 5 — Training
The slide enumerates the training requirements: a UNet conditioned on both source image and instruction, plus a dataset of (source image, instruction, target image) triplets that are generated using the prompt-to-prompt (P2P) technique.

## Slide 6 — Generating training data with P2P
The slide details the synthetic-data pipeline. A source prompt is sampled and run through Stable Diffusion to produce a source image while recording its attention maps. An LLM rewrites the prompt to create an editing instruction and an edited prompt; prompt-to-prompt is then used to synthesize the target image. The intermediate edited prompt is discarded so only the instruction is retained as the training input.

## Slide 7 — Training Dataset Generation
Step 1 of dataset creation starts from an image caption and prompts an LLM to emit both the editing instruction and the resulting caption that describes the desired post-edit image. The schematic panels show this caption-driven prompt expansion as the first stage of the InstructPix2Pix data factory.

---

## Deck-level takeaway
Instruction-based image editing wraps Stable Diffusion's UNet so it consumes both noise and an encoded source image, conditioned on a free-form editing instruction. The hardest piece is data: the InstructPix2Pix recipe uses an LLM to author paired (source caption, instruction, target caption) tuples and then leverages prompt-to-prompt to render the corresponding source/target image pairs that the editor is trained on.
