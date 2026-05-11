# Module 00: ML & PyTorch Foundations

**Audit date**: 2026-05-11
**Sections reviewed**: 0.1, 0.2, 0.3, 0.4
**Total word count**: ~22,000 (very long; the four sections together feel more like a mini-textbook than a chapter)

## Summary
A solid, well-paced launchpad. The voice is consistent (Tensor agent epigraphs land), the practical-example callouts are concrete and convincing, and the scope (classical ML, neural nets, PyTorch, RL) is appropriate for an LLM audience. The biggest single problem is a systemic auto-link bug that has rewritten domain terms (Softmax, Cross-Entropy, Layer Normalization, BERT, fine-tune, dropout, weight decay, backpropagation) into the link text "Section X.Y", producing noticeably broken sentences and tables. A handful of figure-numbering and caption mismatches also crept in. Content quality is high; the polish pass is what is missing.

## Inconsistencies
- **Figure numbering is repeatedly wrong.** In `section-0.2.html`, the chapter-opener illustration is called "Figure 0.0.1" while the next illustration is also labeled "Figure 0.2.2" *twice* (lines 49 and 57). The backprop figure is labeled "Figure 0.2.4" but it is the third figure in the section. In `section-0.3.html` the PyTorch workbench is "Figure 0.3.3" before any 0.3.1 or 0.3.2. In `section-0.4.html` the agent-environment loop diagram is "Figure 0.4.2" without a 0.4.1 anywhere.
- **Code Fragment numbering is also out of order.** `section-0.4.html` has Code Fragment 0.4.7 (line 514, the timeline) appearing before 0.4.6 (line 540, GridWorld), 0.4.5 (line 578, Q-learning), and 0.4.4 (line 596, the heatmap). They are literally in reverse order.
- **Chapter labels are inconsistent.** `index.html` says "Chapter 00: Machine Learning & PyTorch Foundations" while every section uses "Chapter 00: ML and PyTorch Foundations". Pick one.
- **Cross-reference link text rewritten as section numbers.** Examples:
  - `section-0.2.html` line 82: the **activation-function** comparison table has a row whose Function column reads "**Section 4.1**" with the formula `e^z_i / Σe^z_j`. That row is supposed to be **Softmax**.
  - `section-0.2.html` line 192: "consider **Section 4.1** instead (which normalizes across features…)" should be **Layer Normalization**.
  - `section-0.2.html` line 199: "applied class-weighted **Section 4.1** loss" should be **cross-entropy**.
  - `section-0.4.html` line 101: "this is exactly the **Section 4.1** output" should be **softmax**.
  - `section-0.1.html` line 123: "the standard is **Section 4.1** Loss" should be **Cross-Entropy** Loss.
  - `section-0.1.html` line 231: "called **weight decay**" link points at section 0.2 but the text just says weight decay (acceptable here, only mention because the broader pattern is broken).
  - `section-0.3.html` line 31: prerequisites end up reading "you have read Section 0.1: ML Basics (especially **Section 0.1**) and Section 0.2: Deep Learning Essentials (neural network layers and **backpropagation**)" -- the inner cross-ref is meaningless self-reference.
- **Self-referential links.** `section-0.4.html` line 39 reads "directly prepare you for understanding **Section 17.1** in **Section 17.1**". `section-0.1.html` line 39 reads "covered in **Section 0.1**, loss functions, and the bias-variance tradeoff" inside section 0.1's own prerequisites.
- **Figure 0.0.1** in `section-0.2.html` (line 31) is labeled as a chapter opener inside what is supposed to be section 0.2.

## Gaps
- **Adam is referenced before it is defined.** `section-0.2.html` and `section-0.3.html` use `optim.Adam(...)` in code without ever explaining what Adam does. The "Understanding Optimizers" callout in section 0.3 (line 374-) does eventually define momentum/adaptive LR, but section 0.2's complete training loop (line 308) calls `optim.Adam` 100 lines earlier. Section 0.1 (line 395) only forward-references Adam to section 0.3.
- **Section 0.3 has no Self-Check or Key Takeaways callout** like 0.1, 0.2, and 0.4 do. The pedagogical scaffolding is inconsistent.
- **GELU formula is half-Unicode-half-text.** `section-0.2.html` line 81 gives "z · Φ(z)" without ever defining Φ; readers without a stats background will be lost.
- **Promised but missing prerequisites.** Section 0.1 lists "Bayes' theorem" as a prerequisite in the chapter index but never uses it; section 0.4 drops in "expectation" and "discount factor" without a primer.
- **CNN section (0.2.4) is a stub.** It is one paragraph plus a bullet list, with no code, no figure, and no exercise. Either drop it or expand to match the depth of the surrounding subsections.
- **The Figure 0.1.4 "bias-variance tradeoff" image is referenced in prose but the caption-with-truncation alt text** ("Figure 0.1.4: As model complexity increases, bias decreases but variance incr...") suggests the alt text was generated from a truncated caption. Other images in 0.1, 0.2, 0.3 share this "..." pattern (e.g., section 0.2 line 122 alt text is OK, but section 0.4 fig-0.4.4 alt is "Figure 0.4.4: How RL concepts map to LLM training with RLHF. The LLM is the p...").
- **Section 0.3 mentions a hands-on "build an image classifier" lab** in the chapter index card, but the actual section is a tutorial walkthrough; the "lab" promised by the index never materializes as a clearly delineated exercise.

## Errors
- **Code Fragment 0.3.1 is two unrelated snippets glued together** (line 50-128 of `section-0.3.html`). The "Output" block under the first snippet (line 69) prints `tensor([1, 2, 3])` only, but the second snippet (a full FashionMNIST training loop) is a totally separate program with its own Output. The single caption ("Two building blocks side by side…") tries to paper over what is really a code-block mismerge.
- **Code Fragment 0.3.10 has no actual code.** The "callout: Understanding Optimizers" callout is followed by `<div class="code-caption"><strong>Code Fragment 0.3.10:</strong> Assume model, train_loader, device are already defined.</div>` with nothing above it. The training loop it captions is missing.
- **Figure 0.2.4 backprop walk-through has a calculation off by a label.** The text (line 152) says "z = w · x + b = 0.5 · 2 + 0.5 = 1.5" but does not state w=0.5, x=2, b=0.5 anywhere prior. The reader must reverse-engineer the inputs from the arithmetic.
- **Code Fragment 0.3.6 calls `x.grad.zero_()` but x was created with `torch.tensor(2.0, requires_grad=True)`.** The earlier `y = x * 3` then `y.backward()` works, but on the next iteration the second `y = x * 3` is a *new* leaf relationship; the print labelled "After 2nd backward" predicts 6.0, which is correct for the accumulation behavior — but the explanation never mentions that `y` had to be recomputed because the graph was destroyed. Readers will be confused why the 2nd snippet is needed.
- **Code Fragment 0.3.2 has a bizarre `lang-text`** code block (line 178 of `section-0.3.html`) for a Python broadcasting example — it should be `lang-python` and is missing syntax highlighting.
- **`section-0.2.html` Code Fragment 0.2.1 indentation is wrong** (lines 90-115). The `def relu` and `def softmax` bodies are indented with a single space instead of four, and the model-construction lines lose the function bodies' visual nesting. The code may still run as written, but it is not Python's standard 4-space style and is hard to read.
- **In `section-0.4.html` line 414**, Exercise 0.4.2 says "In the REINFORCE code (Code Example 2)" — the book uses "Code Fragment", not "Code Example". A copy-edit miss.
- **`section-0.2.html` line 80**, GELU range `(&approx;-0.17, ∞)` has an unrendered `&approx;` HTML entity.
- **Universal Approximation Theorem citation (`section-0.2.html` line 423)** says "Cybenko, 1989; Hornik, 1991" but the bibliography only lists Goodfellow/Karpathy and the foundational papers — Cybenko and Hornik are never properly cited.
- **`section-0.1.html` line 94** lists "temperature" as a regression example with a cross-ref to 5.2 — but section 5.2 is about stochastic sampling temperature, not temperature regression. The link is a broken pun.

## Improvements
- **Move the optimizer overview (currently 0.3.5.1 callout) to 0.1.3** alongside SGD, so Adam is defined before any code uses it. Section 0.1's "Variants of Gradient Descent" table is the natural home.
- **Renumber every figure and code fragment in 0.2, 0.3, and 0.4** in a single pass; the current numbering is inconsistent enough that the table of contents and references will break at build time.
- **Cross-reference cleanup pass.** A regex sweep for `<a class="cross-ref"[^>]*>Section \d+\.\d+</a>` will flag every place where the link text was auto-generated from the destination section number rather than the term being linked. Replacing with the term name (Softmax, LayerNorm, cross-entropy, BERT, dropout, fine-tuning, attention, …) would fix dozens of unreadable sentences in one pass.
- **Section 0.2.4 (CNNs)** should be either a full subsection with a small image-classifier code example or a one-paragraph "see Appendix" pointer. As-is, it interrupts the flow without earning its space.
- **Section 0.3 needs the same Self-Check + Key Takeaways scaffolding** as the other three sections.
- **Section 0.4's lab (line 452+)** should appear *before* the chapter conclusion, and the lab's Code Fragments need renumbering to avoid the reverse order described above.
- **Add a single "What you should be able to do" diagnostic at the end of section 0.3** asking the reader to write a 5-line training loop. This is the minimum-viable check before chapter 1.
- **The "Practical Example" callouts are excellent but redundant in length.** Section 0.2 has three of them, each ~250 words. Trimming each to 120 words would tighten the chapter without losing the lesson.

## One-thing-only fix
Run a single global replace across all four sections to repair the "Section X.Y" auto-link text. This one bug (visible in section 0.1's Cross-Entropy reference, section 0.2's activation-function table, section 0.4's softmax-policy reference, and section 0.3's prerequisites) is the most jarring problem in the chapter and the only one that produces sentences that literally do not parse. Everything else is polish; this is broken English.
