# Module 27: Multimodal Generation

**Audit date**: 2026-05-11
**Sections reviewed**: 27.1, 27.2, 27.3, 27.4, 27.5, 27.6, 27.7
**Total word count**: ~51,800 words (raw HTML; substantial markup overhead)

## Summary
Module 27 covers a huge surface area (image generation, audio/music/video, document AI, omni-models, VLA/embodied agents, robotics, 3D Gaussian Splatting) with strong technical content and reasonable code samples. Quality is uneven: section 27.1 in particular suffers from chronic figure/code-fragment numbering bugs and a code/output mismatch that suggests an automated build glitch. Section 27.7 is the most polished narratively but has broken lab cross-references. Several sections begin with figures or callouts that splice prose oddly (e.g., "Section 27.5" rendered as `<strong>While Section 27.</strong>5...`).

## Inconsistencies
- **27.1**: Three different figures all labeled `Figure 27.1.3` (the chapter-opener illustration at line 46, the diffusion-restoration illustration at line 50, and the DDPM diagram at line 71). No `Figure 27.1.1` or `Figure 27.1.2` exists.
- **27.1**: Two consecutive `Code Fragment 27.1.1` and `Code Fragment 27.1.2` captions appear back-to-back for the *same* SDXL snippet (lines 117, 119), with identical caption text "Stable Diffusion XL: load the SDXL pipeline with a DPM++ scheduler".
- **27.1**: The SDXL code block (line 88) has an Output panel showing DALL-E text ("Revised prompt: A detailed isometric illustration of a cozy, warmly-lit independent bookshop... Image URL: https://oaidalleapiprodscus.blob..."). DALL-E output is paired with the SDXL pipeline.
- **27.1**: ControlNet code block (line 245) shows Output panel listing "a photo of a cat: 0.923 / a photo of a dog: 0.065 / a photo of a car: 0.012" which is CLIP zero-shot output, not ControlNet output.
- **27.1**: Key Takeaways (line 593) reads "VLM **<a class="cross-ref" href="...section-32.2.html">Section 32.2</a>**" — a cross-ref token has replaced the word "hallucination" inside a takeaway bullet.
- **27.2**: Ghost code caption "Code Fragment 27.2.2: Working with openai, OpenAI" (line 77) appears before the code block it claims to caption; the actual library-shortcut block uses no caption. The output panel under Coqui TTS code (lines 66-74) ends with audio-transcript output ("Detected language: en (probability 0.98)... Welcome everyone to the quarterly planning meeting...") that belongs to a Whisper transcription, not VITS TTS.
- **27.3**: Section opens with `Figure 27.3.2` (chapter-opener illustration, line 38). No `Figure 27.3.1` exists in the section. The LayoutLMv3 architecture diagram (line 154) is *also* labeled `Figure 27.3.2` — duplicate number.
- **27.3**: Prerequisites paragraph (line 34) is stale: "Familiarity with tokenization from Section 02.1 provides context for how audio and video signals are discretized for transformer processing." This is the document-OCR section, not audio/video; the boilerplate was copied from 27.2 without editing.
- **27.4**: Prereqs paragraph (line 35) is broken: "the <a>Section 4.1</a> covered in <a>Section 04.1</a>" — text and link both replaced with the same cross-ref token, leaving an ungrammatical sentence.
- **27.4**: The "Pipeline vs. Native" SVG `aria-label` (line 45) reads "Diagram: 1. Pipeline vs. Native Multimodal Architectures Intermediate" — auto-generated annotation leak.
- **27.5**: Big Picture for sec 27.6 starts "While Section 27." with the `5` outside the `<strong>` tag (`<strong>While Section 27.</strong>5 focused on...`) — markup straddling number.
- **27.6**: Big Picture (line 30) has the same kind of `<strong>` straddling: "<strong>While Section 27.</strong>5 focused on..."
- **27.7**: Section opens with `Figure 27.7.2` (line 67). No `Figure 27.7.1` is defined anywhere.
- **27.7 lab exercise** (line 639) tells the reader to "Run the COLMAP preprocessing pipeline (Code Fragment 27.7.8) and train a 3DGS model (Code Fragment 27.7.2)". The actual COLMAP fragment is 27.7.5 and the actual training fragment is 27.7.6; 27.7.8 is the cat-image fetch in the unrelated CLIP/LLaVA lab below, and 27.7.2 is the SDS sketch.
- **27.7**: Two separate "Lab" sub-trees coexist inside section 27.7 (a 3DGS training lab numbered 27.7.7.6–27.7.7.10 *and* a "Build a Vision-Language Pipeline" lab labelled `lab-27-7`). The vision-language lab is thematically out-of-place in a 3DGS chapter and probably belongs in 27.1.

## Gaps
- **27.1** never re-references Figure 27.1.3 (the diffusion restoration illustration that appears before any subsection); the narrative reference "Figure 27.1.3 illustrates the forward and reverse diffusion processes" actually points at the *other* figure with the same number.
- **27.7** has no introductory `Figure 27.7.1` even though the book elsewhere uses an "Anatomy of …" diagram convention. Numbering jumps straight to 27.7.2.
- **27.5** never defines a stable-baseline reference for "PaLM-E (a 12B VLM)"; PaLM-E was published as 562B parameters (Driess et al. 2023) and the 12B figure in line 53 looks like an editing error.
- **27.6** prerequisites mention "Part VI" generically rather than the specific tool-use sections; readers chasing prereqs land on the part index instead of the relevant section.
- **27.7** prerequisites omit the `Section 27.5` VLA/embodied content that the LLM-and-VLM-integration subsection (27.7.5.3) uses.
- **27.4 chapter-opener illustration** at the section level is missing entirely — the section jumps from header straight to a Big Picture, no Figure 27.4.0 or 27.4.1 hero image.

## Errors
- **27.1**, line 85 (Real-World Scenario callout): claims "diffusion happens in this smaller space ... 50x" but the math right after says "48× reduction" and then "comparable to running a single step in full pixel space" — the body's "48x compression ratio again" for SDXL is also internally inconsistent (the SDXL latent is 4 channels at 128×128, which is 65,536 elements vs 1024×1024×3 = 3,145,728, so the ratio is ~48× yes — but the wording "48× compression ratio again" is then contradicted by the surrounding "50x" claim).
- **27.1**, line 599: "OpenVLA (7B parameters, open source) builds on a Llama 2 backbone with a SigLIP vision encoder". OpenVLA actually uses Llama 2 7B + SigLIP + DinoV2 (the dual-encoder design is one of its distinguishing features); only mentioning SigLIP misrepresents the architecture.
- **27.5**, line 53: "RT-2 ... starts with PaLI-X (a 55B-parameter VLM) or PaLM-E (a 12B VLM)". PaLM-E is 562B; the 12B variant cited may be confused with PaLI's 12B image-text model.
- **27.5**, line 38 specifies the action vector as `(x, y, z, roll, pitch, yaw, gripper)` 7-D, but later RT-2 example (line 55) shows seven *integer* tokens "128 140 130 128 128 128 255" — 8 values, not 7. (Counted: 128, 140, 130, 128, 128, 128, 255 = 7. Correct, but the surrounding phrasing "move right 3cm, up 1cm, close gripper" only describes 3 of 7 dimensions, suggesting the example was abbreviated mid-edit.)
- **27.7**, line 54: "59 floats (about 236 bytes)" assumes 4-byte floats — fine — but earlier the SH coefficient count is given as "48 floats for degree-3 SH" while the same paragraph then says "16 coefficients per color channel, or 48 floats total" (line 95). Degree-3 SH has 16 basis functions × 3 channels = 48, OK; but the introductory bullet (line 52) says "48 floats for degree-3 SH" without the per-channel breakdown, which can confuse a reader doing the arithmetic (3+4+3+1+48 = 59, matches).
- **27.1**, ControlNet code (line 245): the result variable is named `result` but the surrounding prose talks about `image`; minor consistency nit.
- **27.2** and **27.5** both list `from typing import List, Tuple, Dict` patterns but Python 3.9+ allows lowercase generics; the book targets Python 3.14 per CLAUDE.md, so importing `List`/`Tuple` from `typing` is dated style.

## Improvements
- Re-number every figure in 27.1 (currently 27.1.3, 27.1.3, 27.1.3, 27.1.4, 27.1.5; should be 1, 2, 3, 4, 5) and re-number code fragments to drop the duplicate 27.1.1/27.1.2 pair.
- Strip the auto-generated "Implementation example", "Working with openai, OpenAI", and "Define ChatRequest"-style code captions throughout the chapter; replace with descriptive captions. (This is a corpus-wide pattern that the code-caption-agent should re-run.)
- Audit every code block's `<div class="code-output">` payload: at least three blocks in 27.1 and 27.2 show outputs from a *different* code block, suggesting the output extractor matched on file order rather than block ID.
- Replace the "While Section 27.</strong>5" markup straddle in 27.5 and 27.6 Big Picture callouts.
- Move the misplaced "Build a Vision-Language Pipeline" lab from 27.7 back into 27.1 where it belongs; alternatively, retitle and rescope it as a 3DGS+VLM understanding lab (e.g., LangSplat queries).
- Fix the Lab Exercise cross-references in 27.7 (Code Fragment 27.7.8 → 27.7.5 for COLMAP; 27.7.2 → 27.7.6 for training).
- Update prereq stub in 27.3 to talk about document understanding, not audio/video tokenization.
- The native vs. adapter VLM comparison table in 27.1 lists Claude 3.5 Sonnet but not the more recent Sonnet 4 / Opus 4 family; given a 2026-05 audit date, the table is starting to age.

## One-thing-only fix
Re-run the figure-and-code-fragment numbering pass on section 27.1: collapse the three different `Figure 27.1.3` instances to 27.1.1, 27.1.2, 27.1.3 in source order, fix the duplicated `Code Fragment 27.1.1`/`27.1.2` pair, and re-pair the `<div class="code-output">` payloads with the correct code blocks. This single cleanup removes the most jarring reader-visible defects of the chapter and unblocks the rest of the audit chain.
