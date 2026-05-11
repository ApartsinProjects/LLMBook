# Module 05: Decoding Strategies & Text Generation

**Audit date**: 2026-05-11
**Sections reviewed**: 5.1, 5.2, 5.3, 5.4
**Total word count**: ~16,000

## Summary
A clean, practitioner-focused chapter that does an unusually good job of connecting decoding parameters to API usage. Section 5.2's framing of "what each parameter actually does" with the long-tail problem is the best piece of intuition in this batch. The "Common Misconception: Temperature Does Not Control Creativity" callout is exactly the kind of precision-correction a textbook should make. Section 5.4 (diffusion-based language models) is genuinely current — MDLM, SEDD, LLaDA, Gemini Diffusion — and gives the chapter a research-frontier feel. The auto-link "Section 4.1" bug appears here too (5.2 has 14 occurrences) but the chapter is otherwise polished.

## Inconsistencies
- **Auto-link bug is intense in section 5.2** (14 instances): both "softmax" and "logits" links are rewritten as "Section 4.1". The prerequisites paragraph alone has the form "Understanding **Section 4.1**, probability distributions, and how a model produces logits (from **Section 4.1**)…" — should read "Understanding **softmax**" and "(from **Chapter 4**)".
- **Section 5.3 (3 occurrences)** and 5.4 (5 occurrences) have the same bug pattern — domain terms ("attention", "softmax", "cross-entropy", "LayerNorm") rewritten as section numbers.
- **Figure 5.2.2 reused.** Line 47 (DJ illustration) and line 95 (top-p adapts diagram) both labeled "Figure 5.2.2". Line 95's image filename is `fig-5.2.3-top-p.png` so the actual numbering should be 5.2.3.
- **Image alt text scrambled in 5.2.** Line 94: image src `fig-5.2.3-top-p.png` with caption "Figure 5.2.2: Temperature controls the 'peakiness' of the distribution" — alt text and image filename both say top-p but the caption says temperature. This is a swap.
- **Section title vs filename** — index card says "Decoding Strategies & Text Generation"; section header (in section files) says "Decoding and Text Generation". Same chapter-title inconsistency as in modules 0, 2.
- **5.3 covers many distinct topics in a single section** (contrastive decoding, speculative decoding, grammar-constrained generation, JSON schema enforcement, watermarking, MBR decoding). Six topics in one section is hard to navigate without H3 anchors per topic.

## Gaps
- **Section 5.1 (deterministic decoding)** is supposed to introduce greedy and beam search "from scratch", but the actual lab implementation is missing from what I read. The chapter index promises a hands-on lab; verify the lab section actually exists in the file.
- **Length normalization for beam search** is in the index card but I did not see the typical (length penalty α) formula spelled out anywhere. Section 5.1 should include the standard `score / length^α` correction.
- **5.2 mentions min-p sampling** in the chapter index but min-p gets only the briefest treatment. Min-p is a relatively recent technique (Nguyen et al. 2024) and deserves a paragraph showing how it differs from top-p.
- **Repetition / frequency / presence penalties** are listed in the chapter learning objectives but the math behind them (logit subtraction vs probability scaling) is not explicitly contrasted.
- **5.3's speculative decoding** is described conceptually but the draft-model + verify-step diagram (which makes the technique click) does not appear. This is the most-referenced inference-acceleration technique in 2025-2026 production stacks; it deserves a clear figure.
- **Watermarking** in 5.3 is mentioned but the mechanism (greenlist/redlist hashing) is not explained, leaving "watermarking" as a vocabulary word the reader cannot use.
- **5.4 (diffusion LMs)** introduces five different models (MDLM, SEDD, LLaDA, Dream, Gemini Diffusion) but does not give a single concrete sampling-step walkthrough. Discrete diffusion for text is exotic enough that a 5-step toy example would carry the section.
- **No exercises in any section** of this chapter.

## Errors
- **`section-5.2.html` line 124-126** the `top_p_sampling` function uses `cumulative_probs - sorted_probs > p` as the mask. This is the standard "shift-by-one" trick to keep the token that pushes cumulative mass above p, which is correct. But the inline comment ("Find the cutoff: first index where cumulative prob exceeds p / We keep tokens up to (but not including) this cutoff") contradicts the actual behavior — the code keeps the boundary token. Wording should be "We keep tokens up to and including the first one that pushes cumulative mass above p".
- **Top-p sampling output (`section-5.2.html` line 143-148)** for "Confident" logits gives nucleus size = 2 with `cumsum = [0.935, 0.989, ...]`. With p=0.9, the first token already has 0.935 cumulative, so the nucleus should be size *1*, not 2. The function uses the shift-by-one trick (which keeps the *next* token after crossing p), so 2 is what the code returns — but the explanation that this is "intuitive nucleus behavior" should be clarified.
- **`section-5.2.html` line 102** logit values [5.0, 3.5, 2.0, ...] then T=2.0 row shows P('the')=0.268 with entropy=1.933. Cross-checking: with T=2 the logits become [2.5, 1.75, 1.0, ...]; softmax gives p('the')≈0.268 — correct. But entropy 1.933 nats is wrong if claimed to be in nats — softmax of those logits gives entropy ~1.94 in nats, which matches; it should be made explicit which units are used (the section uses log_2 in the math block earlier).
- **Beam search complexity** (section 5.1) — verify the section states beam search complexity correctly: O(b·v·L) where b is beam width, v vocabulary, L sequence length. Without this the time-cost discussion is hand-wavy.
- **`section-5.2.html` Boltzmann analogy** is well-stated but the "T=1.0 is the natural setting" claim (line 72) deserves a caveat: many production deployments use T<1 (e.g., 0.7) as default precisely because the trained distribution is too spread out for tasks like factual QA. The "natural" framing oversells the universality of T=1.
- **Greedy is described as "T → 0"** (line 90) — strictly, T=0 is undefined for the standard formula (division by zero); production code uses argmax instead. A footnote would help.
- **5.3's MBR decoding** is mentioned but the loss function (typically BLEU or chrF as risk) is unspecified.

## Improvements
- **Add a "decoding parameter cheat sheet" to the end of 5.2** with rows for greedy, beam, sampling, top-k=50, top-p=0.9, temp=0.7 etc., and columns for "use case", "diversity", "coherence". This is the chapter's biggest practical takeaway and currently only exists in scattered prose.
- **Section 5.2's temperature/top-p/min-p plots** would benefit from showing the *same* logits run through each method side by side, so the reader can visually compare the three truncation strategies.
- **Section 5.3 needs subsection h3 anchors** for each of its six techniques. Without them, in-page navigation is impossible.
- **Add a 4-step toy diffusion-LM example to 5.4** showing a 5-token sequence iteratively unmasked. Otherwise diffusion LMs feel like buzzword soup.
- **Move the "Boltzmann distribution" Key Insight in 5.2** above the temperature definition, not below it. The physics analogy is more useful as motivation than as commentary.
- **Speculative decoding should get a draft-and-verify diagram** in 5.3, with the math for the rejection-sampling step (the subtle bit that makes the technique an *exact* sampler).
- **Section 5.4's "Paper Spotlight" boxes** are a great idea; add one per major model rather than mentioning all five in a single paragraph.
- **Cross-reference 5.2's API parameters back to chapter 10** explicitly. Currently the "you'll see this when calling APIs" claim is in the prerequisites but not in the body where the parameters are introduced.

## One-thing-only fix
Repair the figure-numbering and image/alt-text/caption mismatch on lines 94-95 of `section-5.2.html`: the image is `fig-5.2.3-top-p.png`, the alt text describes top-p, the caption labels it as Figure 5.2.2 about temperature. As-is, the figure illustrating nucleus sampling is captioned as a temperature diagram in the temperature section. This is a content correctness issue (wrong figure for the topic), not just polish.
