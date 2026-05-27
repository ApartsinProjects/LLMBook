# 2444_StableDiffusion_Prompt2Prompt — Per-Slide Summary

**Source file:** `2444_StableDiffusion_Prompt2Prompt.pptx`
**Source folder:** `SlidesPool/2440_GAI_DiffusionApps/`
**Drive link:** https://drive.google.com/file/d/1LqwETW3KsTI_ONhRamRT5i_OClFQfl49/view
**Slide count (exact, via python-pptx):** 14
**Extraction:** Local parse + slide PNG render. Several slides without body text (3, 4, 9, 11, 12) were inspected visually for figure content.

---

## Slide 1 — P2P: Prompt-to-prompt image editing
Title slide that introduces prompt-to-prompt (P2P), an attention-map editing technique for Stable Diffusion.

## Slide 2 — Task
The slide defines the P2P task: take a source prompt and a target prompt that differ in a controlled aspect, and generate the corresponding pair of images that share layout but differ only in that aspect. The figure shows an example pair.

## Slide 3 — Example: Old + New Prompt
The slide pairs two outputs whose prompts are identical except for a single edited token, demonstrating that P2P preserves the underlying scene composition while applying the targeted change.

## Slide 4 — Reminder: Prompt-Cross Attention in U-Net
The slide visually reminds the reader where prompt tokens enter the SD UNet: they become keys and values that pixel-token queries attend to in each cross-attention block.

## Slide 5 — Attention maps
The slide describes the attention tensor in cross-attention. Each pixel cell is a latent-space feature and each token cell is a token embedding. A single attention map is reshaped into a 3D tensor (pixels x tokens) that records how strongly each pixel attends to each prompt token.

## Slide 6 — Attention Maps
The slide isolates one row of the attention matrix (the response of one token) and reshapes it back into a 2D image. The result is a heatmap showing where in the image that token's influence is concentrated.

## Slide 7 — Editing attention maps
If two prompts differ in only a few tokens, P2P reuses the source prompt's attention maps during sampling and only swaps in new attention rows for the changed tokens. This locks layout while changing semantics.

## Slide 8 — Algorithm
The slide presents the sampling-time algorithm: at every denoising step, run the target prompt through cross-attention but inject the source's attention maps for shared tokens; only the last step uses fully edited maps. The base diffusion sampling loop is otherwise unchanged.

## Slide 9 — Example
The slide shows a worked example pair illustrating that swapping a noun in the prompt while reusing attention maps yields a near-identical scene with the object changed.

## Slide 10 — Control the amount of attention map editing
A scheduling knob is introduced: randomly select a proportion of timesteps at which to use edited attention maps. Injecting only at early steps locks the global object layout, while later-step editing changes finer detail.

## Slide 11 — More examples
A gallery of P2P edits illustrates noun swaps, attribute additions, and color changes performed while preserving spatial structure.

## Slide 12 — Style transfer
The slide shows that P2P also supports style transfer: the same prompt is augmented with a style phrase and the attention reuse trick keeps geometry while re-skinning the image.

## Slide 13 — Control attention weights of specific words
P2P additionally exposes a per-word attention-weight slider: with the same prompt, the weight of a particular token's attention map can be increased or decreased to amplify or attenuate its visual influence.

## Slide 14 — Local Editing
By combining attention-map editing with a region mask (as in inpainting), P2P performs local edits restricted to user-specified areas, while leaving the rest of the image untouched.

---

## Deck-level takeaway
Prompt-to-prompt editing exploits the fact that cross-attention maps localize each prompt token's effect on the generated image. By reusing the source prompt's attention maps and only overriding the rows for changed tokens, P2P lets users edit an object's identity, attributes, style, or local region while preserving the overall scene layout, all at sampling time and without retraining.
