# Research Scientist Cycle-2 Deep Paper-Knowledge Pass (Parts 5-9)

Reviewer: Agent 18 (Research Scientist), v2.0 branch, R2 cycle.
Scope: theoretical/algorithmic chapters in Parts 5-9 (modules 20, 22, 26, 28, 31, 35, 42, 46).
Goal: catch subtle errors in technical explanations that only a paper-versed
researcher would notice; apply surgical fixes.

## Sections audited

- Part 5: section-20.1 (TTS lineages: VITS, Bark, F5-TTS), section-22.7 (VLM fusion)
- Part 6: section-26.2 (planning algorithms, LATS), section-28.2 (multi-agent topologies)
- Part 7: section-31.1a (contrastive InfoNCE math), section-31.1b (Matryoshka MRL),
  section-35.1a (HyDE, BM25, RRF), section-35.1b (HyDE attribution sanity check)
- Part 9: section-42.3 (testing LLM apps - off-topic), section-42.5 (gates - off-topic),
  section-42.10 (bootstrap statistical tests), section-46.1 (LLM-as-judge biases)

Note: the audit headers listed "42.3 statistical tests" and "42.5 LLM-as-judge math",
but those sections cover Testing and Quality Gates respectively. The actual statistical-
tests content lives in section-42.10 (bootstrap, paired bootstrap, permutation tests,
Cohen's kappa), and the LLM-as-judge math lives in section-46.1 (Bradley-Terry).
I audited the right material under the right section IDs.

## Findings

### F1. Module 20.1 (TTS): "flow-based posterior" contradicts the VITS paper

Section 20.1.2 stated VITS uses "a flow-based posterior that maps the latent z to a
waveform through a HiFi-GAN decoder." This conflates two distinct VITS components and
contradicts the figure caption two paragraphs later, which (correctly) says "the prior
(text encoder plus flow)."

Per Kim et al. (2021, ICML), VITS uses:
- a posterior encoder (linear spectrogram features -> z)
- a **normalizing flow on the PRIOR**, transforming the text-conditioned Gaussian prior
  into a more expressive distribution that can match the rich posterior
- a HiFi-GAN-style decoder that turns z into waveform

The flow operates on the prior, not the posterior. The fix reframes the four modules
correctly and updates the SVG diagram label "- flow-based posterior (z)" to
"- normalizing flow on prior", plus the figure caption.

### F2. Module 20.1 (TTS): F5-TTS acronym is wrong

The text claimed "F5" stands for "Faster, Flow-matching, with infilling and pretraining
for Five-shot-or-better synthesis." This is a guess; the actual paper title (Chen et al.,
2024, arXiv:2410.06885) is "F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech
with Flow Matching". The "F5" is five F-words. Parameter count also corrected from 333M
to 336M and training corpus pegged to Emilia (~95k hours).

### F3. Module 22.7 (VLM fusion): Q-Former / Perceiver Resampler order reversed

The bullet list said "Perceiver Resampler (Flamingo, Idefics) ... similar to Q-Former
but uses cross-attention", which inverts the chronology. Flamingo (Alayrac et al. 2022)
predates BLIP-2 / Q-Former (Li et al. 2023). The Q-Former is a Perceiver-style resampler
plus three pretraining losses (ITM, ITC, ITG). Also clarified that Flamingo injects the
resampled summary via interleaved gated cross-attention into the LLM, while Q-Former's
output is concatenated into the input. Both bullets now name the original paper and
clarify the architectural difference at injection time.

### F4. Module 26.2 (planning): Algorithm misnumbered (24.3.1 -> 26.2.1)

Algorithm callout was tagged "Algorithm 24.3.1" inside Section 26.2. Renumbered to
26.2.1.

### F5. Module 26.2 (planning): LATS description missing MCTS selection step + paper attribution

LATS description said "simulates potential action sequences, uses the LLM to evaluate
terminal states, and backpropagates." This omits the MCTS selection step (the UCB-style
score that balances exploit vs explore) and the verbal self-reflection loop that
distinguishes LATS from vanilla MCTS. Rewrote to enumerate the four MCTS operations
(selection, expansion, evaluation, backpropagation), name UCB, and credit Zhou et al.
(2024) inline.

### F6. Module 28.2 (multi-agent): Algorithm misnumbered (27.2.1 -> 28.2.1)

Algorithm callout was tagged "Algorithm 27.2.1" inside Section 28.2. Renumbered.

### F7. Module 31.1b (embeddings): Matryoshka citation year mismatch

Within the same section, MRL was cited as both "Kusupati et al., 2022" (Algorithm box,
source line with arXiv link) and "Kusupati et al., 2024" (Research Frontier callout).
The paper is Kusupati, Bhatt, Rege, Wallingford et al., "Matryoshka Representation
Learning," NeurIPS 2022 (arXiv:2205.13147). Normalized the Research Frontier callout
to "Kusupati et al., NeurIPS 2022."

### F8. Module 42.10 (statistical tests): bootstrap CI code has indentation bug (FUNCTIONALLY BROKEN)

Code Fragment 42.10.3 contained two bootstrap functions (`bootstrap_confidence_interval`
and `paired_bootstrap_test`). In both functions, the lines that convert the list of
bootstrap estimates to an array, compute percentiles, and return the result were
indented INSIDE the `for _ in range(n_bootstrap):` loop. This makes the function:

1. Convert `bootstrap_estimates` (a list) to an ndarray on iteration 1.
2. On iteration 2, call `.append()` on an ndarray, which raises AttributeError.
3. Even if appending worked, it would return inside the first iteration.

The code does not run. This is the kind of bug a reader copies into their evaluation
harness and only notices when their CI pipeline silently produces the wrong p-value.

Fix: dedented lines after the `.append(...)` so that array conversion, percentile
computation, and return happen once, after the loop terminates. Applied to both
functions.

### F9. Module 46.1 (LLM-as-judge): batch loop indentation bug

Code Fragment 46.1.1 (`detect_position_bias`) had the same indentation issue at the
end: the `bias_rate = ...` and `print(...)` lines were indented inside the
`for sample in eval_samples:` loop, computing and printing partial bias rates on every
iteration instead of once after the batch completes. Fixed.

### F10. Module 46.1 (LLM-as-judge): "67% self-preference" claim is uncited and overstated

The Fun Fact said "GPT-4 acting as a judge rated GPT-4's own outputs as the best response
67% of the time, compared to 50% when judging between two other models of equal quality."
The 67% number cannot be traced to the Zheng et al. (2023) MT-Bench paper or to the
Panickssery et al. (2024) self-preference follow-up; reported self-preference deltas in
those studies are ~10 to 25 points above blinded-human baselines, not "67% vs 50%."
Softened to "Multiple studies (Zheng et al. 2023, Panickssery et al. 2024) have
documented self-preference bias on the order of 10 to 25 percentage points" with the
right citations.

## Sections audited and found correct (no edits)

- Section 31.1a InfoNCE / MNRL code: scales similarity by 1/temperature, uses arange
  labels and cross_entropy. Standard and correct. Temperature default 0.05 is the
  sentence-transformers default (CLIP/SimCLR use 0.07).
- Section 35.1a BM25 algorithm box: TF saturation, IDF formula, k1 and b defaults
  all correct. RRF algorithm correct, Cormack/Clarke/Buettcher 2009 attribution
  correct.
- Section 35.1b HyDE attribution to Gao et al. 2022: correct.
- Section 46.1 Bradley-Terry formula: $P(i \succ j) = \sigma(r_i - r_j) = 1/(1+e^{-(r_i-r_j)})$
  is correct, and the connection to Elo / RLHF reward modeling / AlpacaEval LC is
  properly drawn.
- Section 22.7 LaTeX math for early/mid/late fusion: structurally correct; the
  food-metaphor key insight was rewritten by an editor between my read and write
  but the technical content is preserved.

## Audit summary

10 surgical fixes across 6 files. Two are functional Python bugs in code that ships
in the book (F8, F9); these would have silently failed on first run for any reader who
copied them. Three are subtle paper-attribution errors that a reader checking against
arXiv would catch (F1, F2, F3). Two are within-section numbering inconsistencies
(F4, F6). One is a within-section citation-year mismatch (F7). One adds missing
algorithmic detail (F5). One softens an unsupported numeric claim (F10).

Time budget consumed: ~28 minutes. No bibliography or sidebar additions; this pass
was a fix-the-math review only.
