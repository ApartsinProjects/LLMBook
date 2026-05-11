# Module 03: Sequence Models & Attention

**Audit date**: 2026-05-11
**Sections reviewed**: 3.1, 3.2, 3.3
**Total word count**: ~18,000

## Summary
The pedagogical arc — RNN, encoder-decoder bottleneck, attention as soft alignment, scaled dot-product, multi-head — is the right one and is executed well. The "Attn" agent's epigraphs are good. Section 3.1's framing of "the frustration is the pedagogy" is exactly the right tone for a topic that exists mostly as motivation. The biggest issues: (1) the auto-link bug is at its most destructive here, with "Section 4.1" appearing 11 times in section 3.3 alone, including in a Key Takeaways list; (2) figure numbers are wildly out of order and re-used; (3) several mathematical statements need tightening before they confuse a careful reader.

## Inconsistencies
- **Auto-link "Section 4.1" bug is endemic.** Worst offenders:
  - `section-3.3.html` line 667 (Key Takeaways): "we will combine multi-head self-attention with feedforward layers, **Section 4.1**, and **Section 4.1** to build the complete Transformer" — should read "feedforward layers, **layer normalization**, and **residual connections**".
  - `section-3.2.html` line 345 (callout): "The direct path is analogous to a **Section 4.1**: gradient flows directly…" — should be "**residual connection**" or "**skip connection**".
  - `section-3.1.html` prerequisites: links labelled with section numbers when topic names are intended.
- **Figure 3.1.2 reused.** `section-3.1.html` has the telegraph operator illustration at line 47 ("Figure 3.1.2") and the unrolled-RNN diagram at line 100 also captioned "Figure 3.1.2".
- **Figure 3.3.2 reused.** `section-3.3.html` has the four-detectives illustration captioned "Figure 3.3.2" (line 48) and the scaled-dot-product diagram presumably also gets labeled 3.3.2 below.
- **Section title vs filename.** Chapter 3 index card calls section 3.1 "Recurrent Neural Networks & Their Limitations" but the actual section title is "Why RNNs Couldn't Scale to Modern LLMs". The two should match (or the breadcrumb should point to the actual h1).
- **Code Fragment 3.1.1 has a duplicate caption** at line 131: "Code Fragment 3.1.1: Combine input and previous hidden state, then apply tanh." immediately followed by "Code Fragment 3.1.14: Define VanillaRNNCell". One of those numbers is wrong.
- **Apostrophe usage** is inconsistent in chapter labels: `index.html` uses "Couldn't" with curly quote; section files use "Couldn't" with straight ASCII apostrophe.

## Gaps
- **Bahdanau attention math is presented in section 3.2** without ever stating dimensions of the alignment-network parameters. A reader trying to implement it will not know the shapes of W_a, U_a, v_a.
- **`section-3.3.html`** introduces Q/K/V projections but never says explicitly that for *self-attention* Q, K, V are all derived from the same input X via three separate `nn.Linear` layers. This conceptual point is lurking in the code but not stated in the prose.
- **Causal masking is mentioned in the chapter index card** for 3.3 but the actual section appears to push the implementation detail into chapter 4. The split feels arbitrary; either keep causal masking out of 3.3's promises or include the 5 lines of code.
- **No discussion of LSTM gating equations.** Section 3.1 references LSTM "gating mechanisms (input, forget, output gates)" but never writes the equations. Given that the section is supposedly the "study the problem before studying the solution", and given that LSTMs are the most successful sequential approach pre-Transformer, a brief equation block would be appropriate.
- **Backpropagation-through-time (BPTT) gets one paragraph** before the Jacobian product hits. Many readers will want a worked numerical example showing how a small Jacobian eigenvalue makes the gradient shrink across 50 time steps.
- **Multi-head attention motivation** is currently "more heads = more views" but does not include the parameter-counting argument that a single head with d-dim Q/K/V is equivalent in capacity to h heads each with d/h. This is a standard pedagogical point and missing.
- **No exercises** in any of the three sections.

## Errors
- **`section-3.1.html` line 100** image alt text reads "Gradient magnitude vanishes exponentially over time steps in vanilla RNN" but the figure is captioned "An RNN unrolled through time. The same weights are applied at every step." These are two different diagrams; alt text and caption do not match.
- **`section-3.1.html` line 184** the BPTT chain-rule expression uses `diag(1 - h_k^2)` for the tanh derivative, which is correct, but the formula is written as a *product* of `diag(1 - h_k^2) · W_hh` matrices — readers may wonder why the diagonal matrix multiplies W_hh from the right and what shape the final product has. Worth clarifying as `(diag(...) W_hh)^(T-t)` for the all-equal case.
- **`section-3.3.html` Key Takeaway** about O(n²) complexity (line 666) says it is "the primary scalability bottleneck of self-attention." Strictly: for inference, the bottleneck is more often the KV cache size (O(n) memory but with very large constants), not the attention computation itself, which is now usually FlashAttention-fused. A 2026 textbook should hedge.
- **`section-3.3.html` line 79** scaled-dot-product attention formula is stated correctly, but the surrounding text says "Without this scaling, the dot products would grow in magnitude with d_k" — more precisely they grow as √d_k in standard deviation (which is exactly why we divide by √d_k). The wording "grow in magnitude with d_k" suggests linear growth.
- **`section-3.1.html` Code Fragment 3.1.1 output** shows 5 hidden-state norms that increase from 2.79 to 3.61 — for a randomly initialized RNN with tanh, hidden state norms saturate quickly, but the reported numbers do not match what you would get from a fresh `torch.manual_seed`-less run. The example is reproducible only if a seed is set; mention that.
- **`section-3.3.html` "Tip: The Scaling Fix That Saved Transformers"** asserts the original paper "reports that unscaled dot-product attention produced significantly worse results." The actual paper reports a brief ablation showing the scaling matters; "saved Transformers" is grandiose. Tone down.

## Improvements
- **Add a 6-line LSTM gate-equation block to section 3.1.** The current "LSTMs use gating mechanisms" is almost content-free for a reader who needs to understand why LSTMs reduced the vanishing-gradient problem.
- **Add a numerical BPTT example** showing how `(0.9)^50 ≈ 0.005` and `(1.1)^50 ≈ 117` to viscerally demonstrate why the Jacobian product blows up or vanishes.
- **Section 3.3 needs a single end-to-end worked example** showing Q/K/V projections, the n×n attention matrix, the softmax, and the n×d_v output for a tiny n=3, d_k=2 example. Currently the formulas are correct but no concrete numbers ground them.
- **Replace the four "detectives" multi-head illustration** with a heatmap of actual learned attention patterns from BERT (one head doing coreference, one doing syntactic dependencies, etc.). The XKCD-style cartoon is fine but a real heatmap would teach more.
- **Causal masking** belongs in section 3.3 with a 4-line code example, not deferred to section 4.2. The chapter explicitly promises it in the learning objectives.
- **The "Why Study a 'Dead' Architecture?" tip** (3.1) is great. Add a similar "Why these formulas matter" tip in 3.3 explaining what the reader should *do* with the Q/K/V abstraction in the next chapter.
- **Library shortcut formatting**: section 3.1 has a `<div class="callout library-shortcut">` containing only a `<pre><code>` block with no closing `</p>` — verify HTML validity.

## One-thing-only fix
Sweep the chapter for the auto-rewritten "Section 4.1" link text. Section 3.3's Key Takeaways list has the headline statement of the entire chapter — "we will combine multi-head self-attention with feedforward layers, Section 4.1, and Section 4.1 to build the complete Transformer" — rendered nonsensical. This is the closing thought of the foundations Part of the book and currently does not parse as English.
