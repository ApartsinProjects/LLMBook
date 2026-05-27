# 1203_TextDecodingStrategies — Per-Slide Summary

**Source file:** `1203_TextDecodingStrategies.pptx`
**Source folder:** `SlidesPool/1200_LLM_LanguageFM/`
**Drive link:** https://drive.google.com/file/d/1MwjvB6yGaksBisjkHSIyy4ksRUq2k0w1/view
**Slide count (exact, via python-pptx):** 20
**Extraction:** Local parse + slide PNG render. Body bullets and figure captions carry most of the content; code screenshots illustrate the HF generate API.

---

## Slide 1 — Text Decoding Strategies
Title slide for the deck on how to convert next-token probabilities into actual text.

## Slide 2 — Next Token Prediction
Reminder that the LLM outputs a probability vector of length equal to vocabulary size, one entry per candidate next token.

## Slide 3 — Text Generation Strategies
Catalogs three strategies: greedy (pick the highest-probability token), sampling (sample according to the predicted probabilities), and beam search (keep several hypotheses and choose the one with the highest overall probability over a horizon).

## Slide 4 — Greedy Text Generation
Greedy decoding selects the most likely token at each step. Three illustrations show the argmax pick over a probability bar chart.

## Slide 5 — Generating Text
A code screenshot running the autoregressive process for 20 steps using greedy decoding.

## Slide 6 — Greedy Decoding
Greedy decoding does not account for overall sentence probability. Worked example: after the prefix "sky", "sky blue" might be more probable than "sky rockets", but the multi-token continuation "sky rockets soar" (0.4 times 0.9 = 0.36) can have higher overall probability than "sky blue color" (0.5 times 0.4 = 0.20).

## Slide 7 — Text generation using beam search
Beam search keeps several candidate sequences in parallel and returns the best by accumulated log-probability, which mitigates the greedy pitfall.

## Slide 8 — Penalize repetitions
A global criterion for high-quality text is to avoid repeating tokens; decoders penalize repeated n-grams to discourage degenerate outputs.

## Slide 9 — Sampling
Instead of picking the argmax, sampling randomly draws tokens according to the predicted probabilities, producing more diverse texts.

## Slide 10 — Text Generation and Temperature Parameter
Temperature reshapes the probability distribution before sampling: higher temperature flattens probabilities and yields more variety; lower temperature sharpens them toward argmax-like behavior. Four screenshots illustrate sampling, temperature-scaled sampling, and the resulting output diversity.

## Slide 11 — Example
Six output screenshots showing concrete generations under different temperature settings.

## Slide 12 — Nucleus sampling
Top-k sampling restricts the candidate set to the k highest-probability tokens. Top-p (nucleus) sampling restricts the set to the most probable tokens whose cumulative probability exceeds threshold p.

## Slide 13 — Inspecting top-k candidates
Three screenshots showing how to print top-k candidate tokens and their probabilities for a generation step.

## Slide 14 — Top-k sampling
Sampling is performed only from the top-k tokens after renormalizing their probabilities to sum to one.

## Slide 15 — Top-p Samples
With top-k, very improbable tokens can slip in when a long tail is allowed. Top-p limits sampling to the smallest set of most-probable tokens whose cumulative probability exceeds p, adapting the candidate set to the local distribution shape.

## Slide 16 — Text Generation Use Cases
Illustration relating each decoding strategy to use cases (greedy for deterministic tasks, sampling for creative tasks, beam search for tasks that need globally good answers).

## Slide 17 — Speculative Decoding
Section divider introducing speculative decoding.

## Slide 18 — Reminder: Parallel Next Token Prediction
Recaps parallel token prediction: during training, predict every prefix simultaneously; during generation, use the last prediction. Background for speculative decoding, which exploits the parallel-prediction capability.

## Slide 19 — Speculative decoding
Speculative decoding optimizes generation by using a small "draft" model to propose several possible next tokens quickly, then using the large model to validate or correct those speculative tokens in parallel. Additional prediction heads can be attached to the large model for faster validation.

## Slide 20 — Pipeline
A pipeline diagram showing the core model (8B parameters) and the smaller assistant or draft model (1B parameters) running together to accelerate generation.

---

## Deck-level takeaway
The deck surveys the decoding strategies that sit on top of next-token probability outputs. It opens with deterministic methods (greedy, beam search) and motivates beam search by showing that greedy ignores future probability. It then introduces stochastic methods (plain sampling, temperature-scaled sampling, top-k, top-p / nucleus), positioned by their balance of fidelity and diversity. The closing arc covers a performance optimization rather than a quality optimization: speculative decoding, which pairs a fast draft model with the main large model to amortize the latency of long generations while preserving the large model's output distribution.
