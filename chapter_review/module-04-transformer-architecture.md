# Module 04: The Transformer Architecture

**Audit date**: 2026-05-11
**Sections reviewed**: 4.1, 4.2, 4.3, 4.4, 4.5
**Total word count**: ~30,000+ (the longest chapter in the batch by a wide margin)

## Summary
The keystone chapter of the book, and ambitious in scope: paper walkthrough, from-scratch code, variant survey, GPU systems, and expressiveness theory in a single chapter. Section 4.1's information-theory primer is well-placed. Section 4.2 (build-from-scratch lab) is the most concrete deliverable in Part 1. Sections 4.3-4.5 try to cover too much: linear attention, sparse attention, FlashAttention, SSMs/Mamba, RWKV, MoE, MLA, GPU memory hierarchy, Triton kernels, TC0 expressiveness, chain-of-thought theory. Each topic gets a paragraph that introduces enough vocabulary to be confusing without enough depth to be useful. The auto-link bug is at its absolute peak here (sections 4.1, 4.2, 4.3 each have multiple instances).

## Inconsistencies
- **Auto-link "Section 4.1" bug occurs throughout, including self-referentially.** Examples:
  - `section-4.2.html` line 31: "solid understanding of the Transformer architecture from Section 4.1 and **Section 4.1** from Section 3.3" — section 4.2's prereqs link to itself with the wrong text.
  - `section-4.1.html` line 86: "KL divergence penalty in **Section 17.1**" — link, but the term should be inline.
  - `section-4.4.html` references `softmax` as `Section 4.1` in at least one callout based on the global grep results.
- **Section 4.1's information-theory section** redefines softmax probabilities (line 156-) but does not cross-reference the activation functions table from section 0.2. Cross-reference cleanup would help.
- **Figure 4.1.2 reused** (chapter opener layer-cake illustration uses "Figure 4.1.2" but so does the encoder-decoder block diagram later).
- **Hyperparameter table in 4.2** (line 70-) has a row "dropout" with the term as a cross-ref link; the link text should remain "dropout", not the section number.
- **Code line counts**: 4.2's section text says "approximately 300 lines" (line 95); the chapter index card also says "~300 lines". Verify the assembled implementation actually adds up.
- **Section 4.3 covers a list of "Transformer variants"** in the chapter index but the actual section depth varies wildly: BERT/GPT/T5 each get a few paragraphs, while Mamba, RWKV, MoE each get one paragraph. The chapter card promises balanced treatment.

## Gaps
- **Positional encoding is the fundamental contribution of the Transformer paper** (sinusoidal vs learned) and is listed in section 4.1's promises, but the actual coverage feels thin given the depth of the information-theory primer. RoPE is in the bibliography but not discussed in the body — and RoPE is the standard in 2026 LLMs.
- **Pre-LN vs Post-LN**: chapter index card promises this discussion. Verify it actually appears in 4.1 with both block diagrams.
- **Layer normalization** is referenced repeatedly (and as a frequent victim of the auto-link bug) but is never defined in this chapter; the reader is sent back to chapter 0 for it. A 4-line LayerNorm explanation in 4.1 would close the loop because the chapter's normalization choices (Pre-LN, RMSNorm in modern variants) are an architectural decision, not just a chapter-0 building block.
- **Section 4.3** mentions FlashAttention as both an "efficient attention" technique and (in section 4.4) a GPU implementation. The split between "algorithm" and "kernel" is not made explicit; readers may be confused why FlashAttention appears twice.
- **Section 4.4's GPU primer** is written for someone who already knows what a streaming multiprocessor is. Without a "GPU 101" sidebar, this section will lose readers from the ML side and frustrate readers from the systems side.
- **Section 4.5** is supposed to cover "TC0, log-precision" formal results — these need either a definitions box (what is TC0?) or a clear sign that the section is for advanced readers only.
- **No working Pre-LN vs Post-LN side-by-side code example** despite this being one of the section's promises.
- **No exercises** in any of the five sections (modules 0-3 had at least Self-Check). For the most central chapter of the book, this is the largest pedagogical gap.

## Errors
- **`section-4.1.html` line 184-187** quotes specific perplexity numbers for GPT-2 (~30) and GPT-3 (~20) without specifying the dataset. Perplexity is dataset-dependent; quoting numbers without "on Penn Treebank" or "on WikiText-103" makes them meaningless. The hedge "exact numbers depend heavily on the evaluation dataset" appears two lines later but the bullet points still misleadingly imply these are universal numbers.
- **`section-4.1.html` line 122** — "loaded coin H = 0.47 bits" — correct (-(0.9·log2 0.9 + 0.1·log2 0.1) = 0.469), but rounded to two decimals while other entropies in the section are reported to three. Standardize.
- **`section-4.2.html` line 78** the hyperparameter table has `dropout` as a row in a 7-row table; the "Notes" column for the cross-ref'd `dropout` row is just "Dropout rate" — the cross-ref serves no purpose because the term is the row label itself.
- **Cross-reference to Karpathy's nanoGPT** in the bibliography is correct, but the section 4.2 lab is essentially a slimmed nanoGPT — acknowledge this debt explicitly in the section, not just in the references.
- **`section-4.1.html` Information Theory** uses log_2 throughout (correct for "bits" framing) but most ML practitioners and most PyTorch loss functions use natural log (nats). This conversion is never mentioned; readers may be surprised when their `nn.CrossEntropyLoss()` returns a value of 4.6 instead of 6.6 for a perplexity of 100.
- **`section-4.1.html` Cross-Entropy section** (line 148) says "If the model assigns probability 0.9 to the correct token, the loss is about 0.15 bits." Correct (-log2 0.9 ≈ 0.152). "If it assigns only 0.01, the loss jumps to about 6.64 bits." Correct (-log2 0.01 ≈ 6.643). Good arithmetic, but again contrast with PyTorch's nat-units behavior is missing.
- **Section 4.3 SSMs/Mamba claim** ("linear-time sequence modeling") needs a complexity caveat: Mamba is linear *for inference* but the recurrence still has constant work per token. Readers leaving with "Mamba is asymptotically faster than Transformers" will be wrong about prefill.
- **Triton lab section in 4.4** — verify the kernel actually compiles on a current Triton release; the API has changed several times in 2024-2025.
- **Universal approximation claim in 4.5** for sequence-to-sequence functions cites Yun et al. 2020 implicitly; the citation needs to be explicit.

## Improvements
- **Sections 4.3, 4.4, 4.5 should be split into Appendices** or shrunk to "survey + bibliography pointers". As a reading experience, getting through the GPU primer and then the formal-language complexity discussion in the same section is exhausting and breaks the chapter's pace. Section 4.2 is the natural ending point of the chapter for most readers.
- **Add a Pre-LN vs Post-LN diagram** to 4.1 with a one-line explanation of why every modern LLM uses Pre-LN (training stability without aggressive learning-rate warmup).
- **Replace the layer-cake illustration** with a labeled block diagram of one decoder layer (LN → MHA → residual → LN → FFN → residual). The layer-cake is cute but does not survive the transition from "intuition" to "implementation".
- **Add a Self-Check at the end of 4.1** asking the reader to compute the cross-entropy loss for a given (logits, target) tuple. This is the single concrete skill the section teaches.
- **Section 4.2's lab** should output a sample of the trained model's text. The reader should see "the cat sat on the mat"-style output to feel that the from-scratch implementation works.
- **Drop the strawberry/sushi/cake illustrations** in favor of one technical block diagram per section. The book has ~9 cartoony illustrations in this chapter alone; the cumulative effect is more confusing than helpful for what should be the most rigorous chapter.
- **Convert the "Code Fragment X.Y.Z" labels to actual section anchors** so cross-refs work correctly.
- **Section 4.4 needs a "you can skip this section" callout** at the top if the reader is not interested in CUDA/Triton. Currently it sits in the critical path.

## One-thing-only fix
Cut sections 4.3-4.5 down to roughly half their current length and move the deep dives (full Mamba derivation, GPU memory hierarchy details, TC0 formal results) into appendices. The current chapter is ~30,000 words; a 15,000-word version focused on 4.1 + 4.2 with brief overviews of 4.3-4.5 would be a stronger reading experience and would let the central architectural contribution (decoder block + multi-head attention + residual + LN) get the focus it deserves.
