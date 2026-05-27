# 2423_StableDiffusion_LongPrompts — Per-Slide Summary

**Source file:** `2423_StableDiffusion_LongPrompts.pptx`
**Source folder:** `SlidesPool/2420_GAI_StableDiffusion/`
**Drive link:** https://drive.google.com/file/d/1pVt-zP1MAjSvE4817MvDlS4Svffp6ZLb/view
**Slide count (exact, via python-pptx):** 6
**Extraction:** Local parse + slide PNG render. Implementation slides are code-screenshot heavy.

---

## Slide 1 — Long Text Prompts
Title slide for a short focused lecture on overcoming the prompt-length limit of Stable Diffusion's text encoder.

## Slide 2 — 77 prompt limit
States the constraint: the CLIP text encoder used by Stable Diffusion is BERT-based with a design choice of **77 token limit**, and SDXL keeps the same 77-token limit. Any prompt longer than this is truncated — a hard wall that breaks careful, detailed prompt engineering.

## Slide 3 — Workaround: Manual Encoding
Where to break the wall. Cross-attention in the UNet can in principle work with *any* sequence length; the bottleneck is purely in the text encoder. The solution is therefore: chunk the long text into ≤77-token pieces, encode each chunk through the text encoder separately, concatenate the resulting embedding sequences, and feed the concatenated embeddings into the UNet via the `prompt_embed` parameter rather than `prompt`. Special treatment is required because the tokenizer automatically adds start/end tokens to *each* chunk; you must drop the intermediate ones and keep only the first start and the last end.

## Slide 4 — Implementation
The full implementation as a sequence of six code screenshots: chunk-the-prompt, encode-each-chunk, drop-redundant-special-tokens, concatenate-embeddings, pass `prompt_embed` to the pipeline.

## Slide 5 — Prepare single encoding
A focused look at the per-chunk encoding helper function — two code screenshots showing how to encode one chunk of ≤77 tokens correctly.

## Slide 6 — Example
A worked example (three screenshots): a long descriptive prompt that exceeds 77 tokens, the code that chunks and encodes it, and the resulting generated image — closing the loop on the technique.

---

## Deck-level takeaway

A short, focused 6-slide deck that solves one practical problem (Stable Diffusion's 77-token prompt limit) end-to-end. The pedagogical signature is "find the bottleneck, route around it": the slide identifies *where* the limit actually lives (text encoder, not UNet), and the rest of the deck is a code-screenshot walkthrough of chunking + manual encoding + concatenation. Useful as a self-contained "snippet lecture" the reader can apply directly.
