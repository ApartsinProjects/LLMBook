# Redundant Figures Audit

Pairwise figure-caption similarity within each `section-*.html` file. Detects two figures in the same section that illustrate the same concept (e.g. Figure 29.1.2 and 29.1.3 both depicting the self-debugging loop).

## Executive Summary

- Sections scanned (with at least one figure): 352
- Figures extracted: 678
- Flagged pairs (currently outstanding): 54
  - Auto-fix candidates (caption-cosine > 0.75 AND caption-overlap >= 8, or manual override): 0
  - Needs human review (flagged but below auto-fix bound): 54

**Note**: 1 auto-fix has already been applied in this branch by `scripts/fix_redundant_figures.py`: Figure 29.1.3 was removed from `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` because it duplicated Figure 29.1.2 (both depicted the self-debugging loop). See git history for the change.

## Methodology

For every section file, every `<figure>`, `<div class="diagram-container">`, or `<div class="figure-caption">` block is parsed for its label (`Figure X.Y.Z`), caption text, and any preceding `<img alt="">` description. Captions and alt text are concatenated, lowercased, and stopwords are removed. Every pair of figures within the same file is compared using:

1. **Caption cosine similarity** over TF-IDF (IDF built across the whole book corpus).
2. **Caption Jaccard similarity** over substantive tokens (>= 4 chars, stopwords removed).
3. **Caption substantive overlap count**: number of shared >=4-char content words.
4. **Rare shared phrase**: a 3-5 word phrase that appears in BOTH captions and in <= 8 sections book-wide. This catches concept-named figures (like "the self-debugging loop") where two figures share a distinctive n-gram even when the surrounding wording differs.

A pair is flagged when any one of the four signals fires (caption-cosine >= 0.55, caption-Jaccard >= 0.5, caption-overlap >= 6, OR a rare shared phrase). Auto-fix triggers only on STRONG caption evidence (caption-cosine > 0.75 AND caption-overlap >= 8) or on a manual override registered in the detector source. Auto-fix pairs have the second figure removed by `scripts/fix_redundant_figures.py`; review pairs are listed for human triage. The conservative auto-fix bound is intentional: phrase-based and combined-cosine matches commonly fire on complementary figures (e.g. two different diagrams of the same concept that show DIFFERENT aspects) and would over-prune without human review.

Skipped directories: `_archive/`, `KDP/`, `node_modules/`, `pagefind/`, `build/`, `.book-update/`, plus tooling dirs.

## Recommendation Heuristics

For each flagged pair we suggest which figure to KEEP and which to DROP. The default is to keep the figure whose caption is more **concrete and specific** (longer, more distinct content words, more references to mechanism). When the captions are essentially equivalent, we default to keeping the **first** occurrence.

## Flagged Pairs by Part

### part-1-llm-building-blocks  (13 pairs)

- **[REVIEW]** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html`
  - Figure 1.3.2 vs Figure 1.3.3 | caption-cosine=0.51 | caption-jaccard=0.39 | caption-shared=9 | combined-cosine=0.58
  - Rare shared phrase: "center word", "context words"
  - Figure 1.3.2 caption: "The Skip-gram neural network. A one-hot center word vector is multiplied by the embedding matrix W to produce a hidden representation, which is then used to predict context words."
  - Figure 1.3.3 caption: "The Skip-gram architecture. A center word is fed through an embedding layer, and the model learns to predict surrounding context words. The hidden layer weights become the word vectors."
  - Shared caption words: center, context, embedding, gram, hidden, predict, skip, word, words
  - **Suggestion**: KEEP Figure 1.3.3, DROP Figure 1.3.2 (second figure has more specific detail (7 unique caption words, 185 char caption vs 7 / 179 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`
  - Figure 1.4.1 vs Figure 1.4.2 | caption-cosine=0.24 | caption-jaccard=0.21 | caption-shared=5 | combined-cosine=0.28
  - Rare shared phrase: "regardless of context"
  - Figure 1.4.1 caption: "The polysemy trap. Static embeddings assign one vector to "bank" regardless of context, producing a blurry average that captures none of its distinct meanings well."
  - Figure 1.4.2 caption: "Static vs. contextual embeddings. Word2Vec assigns one fixed vector per word regardless of context, while contextual models produce different vectors for each usage."
  - Shared caption words: context, embeddings, regardless, static, vector
  - **Suggestion**: KEEP Figure 1.4.1, DROP Figure 1.4.2 (first figure has more specific detail (10 unique caption words, 164 char caption vs 9 / 165 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`
  - Figure 1.4.3 vs Figure 1.4.4 | caption-cosine=0.38 | caption-jaccard=0.24 | caption-shared=7 | combined-cosine=0.32
  - Rare shared phrase: "forward and backward"
  - Figure 1.4.3 caption: "The ELMo computation graph. Input tokens pass through a character embedding layer, then through forward and backward LSTMs. The final ELMo vector for each token is a learned weighted sum across all layers."
  - Figure 1.4.4 caption: "The ELMo architecture. A forward and backward LSTM each process the full sentence, and the outputs from multiple layers are combined with learned weights to produce a contextual embedding for each token."
  - Shared caption words: backward, elmo, embedding, forward, layers, learned, token
  - **Suggestion**: KEEP Figure 1.4.3, DROP Figure 1.4.4 (first figure has more specific detail (11 unique caption words, 205 char caption vs 11 / 203 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html`
  - Figure 0.1.1 vs Figure 0.1.2 | caption-cosine=0.31 | caption-jaccard=0.20 | caption-shared=4 | combined-cosine=0.34
  - Rare shared phrase: "gradient descent"
  - Figure 0.1.1 caption: "Gradient descent navigates a loss landscape by following the steepest downhill direction at each step, seeking the lowest valley (minimum loss)."
  - Figure 0.1.2 caption: "Gradient descent follows the slope downhill, step by step. The learning rate controls step size."
  - Shared caption words: descent, downhill, gradient, step
  - **Suggestion**: KEEP Figure 0.1.1, DROP Figure 0.1.2 (first figure has more specific detail (10 unique caption words, 144 char caption vs 6 / 96 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html`
  - Figure 0.3.4 vs Figure 0.3.5 | caption-cosine=0.17 | caption-jaccard=0.16 | caption-shared=4 | combined-cosine=0.27
  - Rare shared phrase: "training loop"
  - Figure 0.3.4 caption: "The training loop as a racetrack. Each lap (epoch) passes through the same four stations: forward pass, loss computation, backward pass, and optimizer step. The robot gets a little better each lap."
  - Figure 0.3.5 caption: "The canonical training loop. Step 0 (zero gradients) prevents gradient accumulation. Steps 1 through 4 repeat for every mini-batch in every epoch."
  - Shared caption words: epoch, loop, step, training
  - **Suggestion**: KEEP Figure 0.3.4, DROP Figure 0.3.5 (first figure has more specific detail (11 unique caption words, 197 char caption vs 10 / 146 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html`
  - Figure 1.3.1 vs Figure 1.3.2 | caption-cosine=0.31 | caption-jaccard=0.22 | caption-shared=5 | combined-cosine=0.40
  - Rare shared phrase: "center word"
  - Figure 1.3.1 caption: "The Skip-gram sliding window. The center word "sat" is paired with each context word within a window of size 2, generating training pairs."
  - Figure 1.3.2 caption: "The Skip-gram neural network. A one-hot center word vector is multiplied by the embedding matrix W to produce a hidden representation, which is then used to predict context words."
  - Shared caption words: center, context, gram, skip, word
  - **Suggestion**: KEEP Figure 1.3.2, DROP Figure 1.3.1 (second figure has more specific detail (11 unique caption words, 179 char caption vs 7 / 138 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html`
  - Figure 1.3.1 vs Figure 1.3.3 | caption-cosine=0.37 | caption-jaccard=0.22 | caption-shared=5 | combined-cosine=0.49
  - Rare shared phrase: "center word"
  - Figure 1.3.1 caption: "The Skip-gram sliding window. The center word "sat" is paired with each context word within a window of size 2, generating training pairs."
  - Figure 1.3.3 caption: "The Skip-gram architecture. A center word is fed through an embedding layer, and the model learns to predict surrounding context words. The hidden layer weights become the word vectors."
  - Shared caption words: center, context, gram, skip, word
  - **Suggestion**: KEEP Figure 1.3.3, DROP Figure 1.3.1 (second figure has more specific detail (11 unique caption words, 185 char caption vs 7 / 138 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html`
  - Figure 1.5.4 vs Figure 1.5.5 | caption-cosine=0.27 | caption-jaccard=0.18 | caption-shared=5 | combined-cosine=0.21
  - Rare shared phrase: "tokenization artifacts"
  - Figure 1.5.4 caption: "Tokenization artifacts as a broken telephone game. When the tokenizer splits words at unexpected boundaries, the resulting fragments can confuse the model, leading to arithmetic errors, inconsistent spelling, and strange behavior at token boundaries."
  - Figure 1.5.5 caption: "Tokenization artifacts propagate through the model pipeline, causing unexpected failures in downstream tasks like arithmetic."
  - Shared caption words: arithmetic, artifacts, model, tokenization, unexpected
  - **Suggestion**: KEEP Figure 1.5.4, DROP Figure 1.5.5 (first figure has more specific detail (17 unique caption words, 250 char caption vs 6 / 125 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html`
  - Figure 3.2.5 vs Figure 3.2.6 | caption-cosine=0.42 | caption-jaccard=0.17 | caption-shared=6 | combined-cosine=0.45
  - Rare shared phrase: "residual stream"
  - Figure 3.2.5 caption: "The residual stream as a branch-and-merge highway. Each sub-layer (Attention, FFN) reads the current stream, computes its contribution, and adds it back. The stream is never overwritten, sub-layers can only add. This is why information from early layers reaches late layers directly, and why deleting a layer often degrades the model less than expected."
  - Figure 3.2.6 caption: "The residual stream perspective (Elhage et al., 2021). The Transformer's residual path acts as a shared communication channel. Each attention and FFN sub-layer reads from the stream and adds its output back, rather than sequentially transforming a single representation."
  - Shared caption words: adds, attention, layer, reads, residual, stream
  - **Suggestion**: KEEP Figure 3.2.5, DROP Figure 3.2.6 (first figure has more specific detail (17 unique caption words, 353 char caption vs 13 / 270 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html`
  - Figure 3.5.3 vs Figure 3.5.4 | caption-cosine=0.36 | caption-jaccard=0.18 | caption-shared=7 | combined-cosine=0.39
  - Rare shared phrase: "rope rotates"
  - Figure 3.5.3 caption: "RoPE rotates each pair of embedding dimensions by an angle proportional to the token's position. Because the dot product of two rotated vectors depends only on the angle between them (the relative position), RoPE naturally captures relative position without explicit position IDs."
  - Figure 3.5.4 caption: "The four major positional encoding strategies. Sinusoidal and learned embeddings inject absolute position before the first attention layer. RoPE rotates Q and K vectors in each attention layer so their dot product depends on relative distance. ALiBi bypasses embeddings entirely and subtracts a distance penalty from attention scores. RoPE has become the dominant choice in frontier LLMs."
  - Shared caption words: depends, position, product, relative, rope, rotates, vectors
  - **Suggestion**: KEEP Figure 3.5.4, DROP Figure 3.5.3 (second figure has more specific detail (22 unique caption words, 388 char caption vs 10 / 280 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html`
  - Figure 4.2.1 vs Figure 4.2.2 | caption-cosine=0.32 | caption-jaccard=0.17 | caption-shared=4 | combined-cosine=0.27
  - Rare shared phrase: "temperature controls"
  - Figure 4.2.1 caption: "Temperature controls the entropy of the sampling distribution, like a DJ controls the energy of a mix. Low temperature produces focused, deterministic outputs; high temperature flattens the distribution, allowing rare tokens to surface more often."
  - Figure 4.2.2 caption: "Temperature controls the "peakiness" of the distribution. Lower temperatures concentrate probability on top tokens; higher temperatures spread it more evenly."
  - Shared caption words: controls, distribution, temperature, tokens
  - **Suggestion**: KEEP Figure 4.2.1, DROP Figure 4.2.2 (first figure has more specific detail (12 unique caption words, 247 char caption vs 8 / 158 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html`
  - Figure 4.3.1 vs Figure 4.3.3 | caption-cosine=0.26 | caption-jaccard=0.28 | caption-shared=7 | combined-cosine=0.32
  - Rare shared phrase: "single pass", "speculative decoding"
  - Figure 4.3.1 caption: "Speculative decoding pairs a fast apprentice model with an expert verifier. The apprentice drafts multiple tokens quickly; the expert checks them in a single pass, accepting correct ones and rewriting the rest."
  - Figure 4.3.3 caption: "Speculative decoding generates multiple draft tokens cheaply, then verifies them in a single pass of the expensive target model."
  - Shared caption words: decoding, model, multiple, pass, single, speculative, tokens
  - **Suggestion**: KEEP Figure 4.3.1, DROP Figure 4.3.3 (first figure has more specific detail (12 unique caption words, 210 char caption vs 6 / 128 char))

- **[REVIEW]** `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html`
  - Figure 3.5.1 vs Figure 3.5.2 | caption-cosine=0.29 | caption-jaccard=0.17 | caption-shared=3 | combined-cosine=0.69
  - Figure 3.5.1 caption: "The three Transformer architectural families. The decoder-only pattern dominates modern LLMs."
  - Figure 3.5.2 caption: "The three Transformer families: encoder-only models (like BERT) read bidirectionally, decoder-only models (like GPT) generate left to right with causal attention, and encoder-decoder models (like T5) combine both approaches."
  - Shared caption words: decoder, families, transformer
  - **Suggestion**: KEEP Figure 3.5.2, DROP Figure 3.5.1 (second figure has more specific detail (10 unique caption words, 224 char caption vs 5 / 93 char))

### part-10-llm-security-runtime-safety  (5 pairs)

- **[REVIEW]** `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.2.html`
  - Figure 50.2.1 vs Figure 50.2.2 | caption-cosine=0.57 | caption-jaccard=0.35 | caption-shared=6 | combined-cosine=0.84
  - Rare shared phrase: "methods trade", "unlearning methods", "unlearning methods trade"
  - Figure 50.2.1 caption: "Forgetting on purpose turns out to be much harder than learning by accident. Approximate unlearning methods trade perfect erasure guarantees for practical computational costs."
  - Figure 50.2.2 caption: "Unlearning methods trade off between forgetting guarantees and computational cost."
  - Shared caption words: computational, forgetting, guarantees, methods, trade, unlearning
  - **Suggestion**: KEEP Figure 50.2.1, DROP Figure 50.2.2 (first figure has more specific detail (10 unique caption words, 175 char caption vs 1 / 82 char))

- **[REVIEW]** `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.2.html`
  - Figure 48.2.1 vs Figure 48.2.2 | caption-cosine=0.33 | caption-jaccard=0.16 | caption-shared=8 | combined-cosine=0.36
  - Rare shared phrase: "input guardrail", "topic classifier"
  - Figure 48.2.1 caption: "A layered input guardrail runs three checks in parallel before any tokens reach the model. Prompt Guard 2 (Meta's 86M DeBERTa) flags injection / jailbreak patterns at ~20ms. Microsoft Presidio redacts PII via 50+ regexes plus NER. A topic classifier or LLM-as-judge enforces application-specific policy. If any check fails, the request is blocked or redacted before incurring the model's higher per-token cost."
  - Figure 48.2.2 caption: "The canonical input guardrail pipeline. Regex runs first because it is the cheapest filter. The classifier and the PII redactor run in parallel because they have no data dependency. The topic classifier runs last because it is the most expensive and most informative; it sees the redacted text so PII never reaches the LLM-as-judge."
  - Shared caption words: classifier, guardrail, input, judge, parallel, redacted, runs, topic
  - **Suggestion**: KEEP Figure 48.2.1, DROP Figure 48.2.2 (first figure has more specific detail (30 unique caption words, 410 char caption vs 13 / 332 char))

- **[REVIEW]** `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.3.html`
  - Figure 48.3.1 vs Figure 48.3.2 | caption-cosine=0.27 | caption-jaccard=0.11 | caption-shared=7 | combined-cosine=0.30
  - Figure 48.3.1 caption: "The four open-source output guardrails take four different design stances. Llama Guard 3 is a fine-tuned LLM that returns a verdict plus MLCommons categories. NeMo Guardrails is a Colang DSL for programming conversational flows. ShieldGemma scales the same classifier across 2B / 9B / 27B for a latency-versus-accuracy knob. Guardrails AI is a Python validator framework that emphasizes structural and PII checks rather than harm classification. Production stacks layer two of them because each catches a different failure mode."
  - Figure 48.3.2 caption: "Side-by-side comparison of the four major output guardrail platforms. Numbers are illustrative based on each platform's published model card and represent typical production configurations. The right choice depends on the dominant constraint: accuracy (ShieldGemma 9B), customization (NeMo Colang or Guardrails AI), or footprint (Guardrails AI validators on CPU)."
  - Shared caption words: accuracy, colang, guardrails, nemo, output, production, shieldgemma
  - **Suggestion**: KEEP Figure 48.3.1, DROP Figure 48.3.2 (first figure has more specific detail (35 unique caption words, 528 char caption vs 22 / 363 char))

- **[REVIEW]** `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.5.html`
  - Figure 48.5.1 vs Figure 48.5.2 | caption-cosine=0.18 | caption-jaccard=0.12 | caption-shared=7 | combined-cosine=0.25
  - Figure 48.5.1 caption: "Multimodal attacks (image-embedded injection, ultrasonic audio jailbreaks, harmful visual outputs) need modality-specific guardrails. The hosted APIs (Azure Content Safety, AWS Rekognition, Vertex AI Safety) ship four to eighty categories with severity scoring. The open-source path chains modality-specific encoders (Tesseract, CLIP, Whisper) into the text-guardrail stack so injection hidden in pixels or in ultrasound becomes visible to Prompt Guard 2."
  - Figure 48.5.2 caption: "The multimodal guardrail stack. Each modality has its own classifier pipeline, but the policy decision module is shared so that thresholds are consistent across modalities. The output side runs the same classifiers in reverse: generated images go through the image classifier, generated text through Llama Guard, generated audio through transcription-then-text-guardrail."
  - Shared caption words: audio, guard, guardrail, modality, multimodal, stack, text
  - **Suggestion**: KEEP Figure 48.5.1, DROP Figure 48.5.2 (first figure has more specific detail (35 unique caption words, 455 char caption vs 18 / 371 char))

- **[REVIEW]** `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.1.html`
  - Figure 49.1.1 vs Figure 49.1.3 | caption-cosine=0.19 | caption-jaccard=0.11 | caption-shared=7 | combined-cosine=0.20
  - Figure 49.1.1 caption: "Defense in depth for agent security. Multiple protective layers (input filtering at the moat, permission checks at the outer wall, sandboxing at the inner vault) ensure that no single failure can compromise the system. The outer layer is a water-filled moat with a drawbridge; the middle layer is a stone outer wall with cartoon guards holding shields; the inner layer is an inner courtyard wall with a sealed vault door. A cartoon trickster character is being politely turned away at the drawbridge. Title text 'DEFENSE IN DEPTH' overlaid at the top in dark navy bold all-caps."
  - Figure 49.1.3 caption: "Five layers of prompt injection defense. Each layer (input sanitization, prompt hardening, privilege separation, output filtering, action approval) reduces the probability of a successful attack and limits blast radius when one layer fails. No single layer is sufficient; the depth is the defense."
  - Shared caption words: defense, depth, filtering, input, layer, layers, single
  - **Suggestion**: KEEP Figure 49.1.1, DROP Figure 49.1.3 (first figure has more specific detail (40 unique caption words, 578 char caption vs 18 / 297 char))

### part-11-llm-ethics-trust-governance  (5 pairs)

- **[REVIEW]** `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html`
  - Figure 52.1.1 vs Figure 52.1.2 | caption-cosine=0.50 | caption-jaccard=0.25 | caption-shared=7 | combined-cosine=0.58
  - Rare shared phrase: "bias enters", "bias enters at every stage", "data collection"
  - Figure 52.1.1 caption: "Fairness is not something you achieve once and forget. Bias enters at every stage of the LLM lifecycle, from data collection through deployment, and requires continuous measurement. with diverse groups of cartoon people on one side and training data represented as colorful documents on the other, with some documents tilted or stacked unevenly to show how bias enters through unbalanced data."
  - Figure 52.1.2 caption: "Bias enters at every stage: data collection, training, alignment, and deployment context."
  - Shared caption words: bias, collection, data, deployment, enters, stage, training
  - **Suggestion**: KEEP Figure 52.1.1, DROP Figure 52.1.2 (first figure has more specific detail (19 unique caption words, 393 char caption vs 2 / 89 char))

- **[REVIEW]** `part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.8.html`
  - Figure 54.8.1 vs Figure 54.8.2 | caption-cosine=0.17 | caption-jaccard=0.09 | caption-shared=6 | combined-cosine=0.31
  - Rare shared phrase: "openai s preparedness", "openai s preparedness framework", "preparedness framework"
  - Figure 54.8.1 caption: "Comparison of frontier-lab disclosure frameworks. OpenAI's Preparedness Framework, Anthropic's RSP, and Google DeepMind's FSF are the dominant three. They differ in risk category enumeration, capability-level granularity, and mitigation prescription. As of 2026, all three reference each other and the UK/US AISI evaluations as standard practice."
  - Figure 54.8.2 caption: "OpenAI's Preparedness Framework as it appears in the o1 system card (September 2024) and later: four risk axes (cybersecurity, CBRN, persuasion, model autonomy) each scored Low / Medium / High / Critical. A model classified Medium on CBRN, which is where o1 was placed, can be released only with Anthropic-RSP-3-equivalent mitigations and a red-team report attached to the system card. Two cells at the Critical column require Anthropic-style "do not deploy" classification, the property the system card has to publicly affirm. The 16-cell grid is the structural skeleton system cards from OpenAI, Anthropic (mapped via ASL), and DeepMind (mapped via CCL) all converge on; Section 54.8.1 catalogs the differences."
  - Shared caption words: anthropic, deepmind, framework, openai, preparedness, risk
  - **Suggestion**: KEEP Figure 54.8.2, DROP Figure 54.8.1 (second figure has more specific detail (42 unique caption words, 713 char caption vs 19 / 346 char))

- **[REVIEW]** `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.3.html`
  - Figure 54.3.1 vs Figure 54.3.2 | caption-cosine=0.28 | caption-jaccard=0.17 | caption-shared=9 | combined-cosine=0.32
  - Rare shared phrase: "synthid-image embeds"
  - Figure 54.3.1 caption: "Image and video provenance ships in two complementary layers. C2PA embeds a cryptographically signed manifest (claim generator, action history, X.509 or Ed25519 signature chain) inside PNG / JPEG / MP4 metadata, and gets stripped by a screenshot or aggressive recompression. SynthID-Image embeds a pixel-domain statistical mark that survives JPEG re-encoding, cropping, and modest filtering, but falls to inversion-then-regenerate attacks. Production stacks layer both because each closes the other's weakness."
  - Figure 54.3.2 caption: "C2PA and SynthID-Image are complementary. C2PA gives strong cryptographic provenance (signer identity, parent chain) but lives in stripable metadata. SynthID-Image embeds in the pixels themselves so it survives metadata loss but cannot identify the specific signer. Production deployments use both layers."
  - Shared caption words: chain, complementary, embeds, layers, metadata, production, provenance, survives, synthid
  - **Suggestion**: KEEP Figure 54.3.1, DROP Figure 54.3.2 (first figure has more specific detail (32 unique caption words, 510 char caption vs 12 / 305 char))

- **[REVIEW]** `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.4.html`
  - Figure 54.4.1 vs Figure 54.4.2 | caption-cosine=0.21 | caption-jaccard=0.11 | caption-shared=7 | combined-cosine=0.19
  - Rare shared phrase: "deepfake detection"
  - Figure 54.4.1 caption: "Deepfake detection accuracy 2026 split by modality and condition. GAN-era images give specialized classifiers (CNNDetect, FreqNet) about 98 percent accuracy; diffusion-era images drop to roughly 90 percent with ensemble approaches; voice clones land around 92 percent with end-to-end raw-waveform models like RawNet2; and in-the-wild video (the 2024 DeepFake Detection Challenge winner) collapses to about 65 percent. The lab-to-wild gap is what makes detection a defense layer, not a single-point solution."
  - Figure 54.4.2 caption: "A 2026-typical video deepfake detection ensemble. Three independent analysis streams (per-frame, temporal, audio-video) feed a meta-classifier. Stream independence is crucial: an attacker who fixes per-frame artifacts often leaves temporal signals untouched, and vice versa. Reported performance is from the 2025 DFDC public leaderboard; in-the-wild compression and downsampling drop accuracy by 5-10 points."
  - Shared caption words: accuracy, deepfake, detection, drop, ensemble, video, wild
  - **Suggestion**: KEEP Figure 54.4.2, DROP Figure 54.4.1 (second figure has more specific detail (29 unique caption words, 408 char caption vs 27 / 507 char))

- **[REVIEW]** `part-11-llm-ethics-trust-governance/module-54b-transparency-and-disclosure/section-54.10.html`
  - Figure 54.10.1 vs Figure 54.10.2 | caption-cosine=0.27 | caption-jaccard=0.08 | caption-shared=6 | combined-cosine=0.25
  - Rare shared phrase: "attention rollout"
  - Figure 54.10.1 caption: "Three complementary views of the same decision. SHAP attributes the prediction to input tokens. Attention rollout shows which tokens the model attended to. SAE features show which internal concepts were active. SHAP and attention answer "what in the input mattered?"; SAE features answer "what did the model think about?". For compliance, SHAP is the established artifact; for genuine understanding, SAE-based views are pulling ahead."
  - Figure 54.10.2 caption: "Coverage matrix of the four explanation methods against the four legal-and-operational questions the section discusses. SHAP and counterfactual explanations are the only two methods accepted today as primary evidence under both the 2023 CFPB advisory on ECOA adverse-action notices and the EU AI Act Article 86 right to explanation. Attention rollout fails on all four because Jain &amp; Wallace (2019) showed permuting attention weights leaves the output intact. SAE features (Templeton et al., 2024) are improving fast on the audit side but remain a research artifact for per-decision recourse. The pattern the section recommends, SHAP plus a counterfactual generator (DiCE), is the only pair that lights up all four columns."
  - Shared caption words: artifact, attention, decision, features, rollout, shap
  - **Suggestion**: KEEP Figure 54.10.2, DROP Figure 54.10.1 (second figure has more specific detail (47 unique caption words, 727 char caption vs 21 / 434 char))

### part-12-llm-systems-at-scale  (7 pairs)

- **[REVIEW]** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.4.html`
  - Figure 58.4.1 vs Figure 58.4.2 | caption-cosine=0.17 | caption-jaccard=0.12 | caption-shared=9 | combined-cosine=0.18
  - Rare shared phrase: "online softmax"
  - Figure 58.4.1 caption: "Four FlashAttention versions in four years, one per NVIDIA hardware generation. The kernel rewrites itself because the SM architecture and tensor-core instruction set rewrite themselves. A100 Ampere SM, IO-aware tiling and online softmax in FP16), FA-2 (2023, H100 Hopper, reordered work for better SM occupancy), FA-3 (2024, H100 with warp-specialization and FP8 for 1.5-2x speedup), and FA-4 (2026, Blackwell B200/B300 with asymmetric SM pipelining for 2x over FA-3). Each version is paired with its underlying architectural change in NVIDIA hardware."
  - Figure 58.4.2 caption: "FlashAttention-4 tiling on a Blackwell SM. The IO-aware idea from FA-1 (keep tiles in fast SRAM) is preserved; FA-4's new contribution is to schedule the matmul (tensor partition) and the softmax (special-function partition) asymmetrically so they overlap instead of stalling each other. That overlap is the ~2x speedup over FA-3. s full Q, K, V matrices and the naive O(seqlen^2) attention matrix; inner SRAM/L1 per SM holds resident Q tile plus streamed K and V tiles plus an online softmax accumulator; innermost Registers hold the running m, l, O statistics. The SRAM box also splits into Tensor partition (tcgen05 MMA) and SFU partition (exp, division, softmax) with an arc labeled async pipelining. A bandwidth bar at the bottom shows HBM ~8 TB/s, SRAM ~20 TB/s, Registers ~80 TB/s."
  - Shared caption words: aware, blackwell, flashattention, online, pipelining, softmax, speedup, tensor, tiling
  - **Suggestion**: KEEP Figure 58.4.2, DROP Figure 58.4.1 (second figure has more specific detail (39 unique caption words, 788 char caption vs 25 / 553 char))

- **[REVIEW]** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.5.html`
  - Figure 58.5.1 vs Figure 58.5.2 | caption-cosine=0.18 | caption-jaccard=0.09 | caption-shared=9 | combined-cosine=0.17
  - Figure 58.5.1 caption: "Training and inference were once two separate stacks with two separate teams. By 2026, six layers (scaling-law math, attention kernels, quantization schedules, MoE routing, speculative draft heads, multi-stage pipelines) are co-designed across both. The fusion did not happen all at once; the bottom timeline shows when each layer crossed over. Left column shows two separate stacks circa 2023: a Training stack (Chinchilla optimum, FA-2, bf16, all params trained, H100 cluster) and an Inference stack (throughput/latency, PagedAttention, int4 post-hoc, retrofitted routing, whatever-fits hardware). A central arrow labeled '2024-26: layers fuse (Sardana, MoE, QAT, EAGLE)' points to the right column. Right column shows one fused 2026 stack with co-designed layers: inference-aware scaling laws, FA-4 attention, quantization-aware training, MoE trained-all-serve-sparse, speculative-decoding draft heads, and a multi-stage HERMES pipeline. A bottom timeline marks FA-1 in 2022 through FA-4 + HERMES in 2026."
  - Figure 58.5.2 caption: "How Sardana et al. (arXiv:2401.00448, 2024) shifted the field's compute-optimal frontier. The Chinchilla training-only optimum at 20:1 tokens-per-parameter ratio (red, dashed) minimizes training cost; the inference-aware curve (blue) adds amortized inference cost over the model's serving lifetime and shifts the optimum 50x to the right, toward smaller models trained on more tokens. The 2026 reference points cluster in that shifted zone: Llama-3.1 8B near 1800:1, SmolLM2 360M and Qwen3-0.6B in the 30,000-60,000:1 band, and Liquid LFM2.5-350M setting the 2026 record at 80,000:1 on 28T training tokens. The economics that make this rational are exactly the "frontier serves to a billion users daily" condition the section's first paragraph describes."
  - Shared caption words: aware, chinchilla, cluster, inference, optimum, points, sardana, trained, training
  - **Suggestion**: KEEP Figure 58.5.1, DROP Figure 58.5.2 (first figure has more specific detail (46 unique caption words, 1008 char caption vs 43 / 754 char))

- **[REVIEW]** `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html`
  - Figure 59.1.1 vs Figure 59.1.2 | caption-cosine=0.30 | caption-jaccard=0.30 | caption-shared=7 | combined-cosine=0.45
  - Rare shared phrase: "parallelism data", "production training", "production training composes"
  - Figure 59.1.1 caption: "Three flavors of parallelism. Data, pipeline, and tensor each split a different axis of the work. Production training composes all three."
  - Figure 59.1.2 caption: "The three axes of parallelism. Data parallel replicates the model and splits the batch; pipeline parallel splits the layer stack; tensor parallel splits a single weight matrix. Production training composes all three."
  - Shared caption words: composes, data, parallelism, pipeline, production, tensor, training
  - **Suggestion**: KEEP Figure 59.1.2, DROP Figure 59.1.1 (second figure has more specific detail (11 unique caption words, 216 char caption vs 5 / 137 char))

- **[REVIEW]** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.1.html`
  - Figure 58.1.1 vs Figure 58.1.2 | caption-cosine=0.24 | caption-jaccard=0.13 | caption-shared=8 | combined-cosine=0.31
  - Figure 58.1.1 caption: "Memory bandwidth, not FLOPs, sets batch-1 inference latency. SRAM-class silicon (Groq, Cerebras) jumps a full log unit past HBM, which is why they hold the latency crown despite far lower nominal FLOPs."
  - Figure 58.1.2 caption: "The five 2026 frontier-silicon families positioned on the training-vs-inference axis (horizontal) and the throughput-vs-latency axis (vertical). Bubble size reflects effective memory-bandwidth class. NVIDIA Blackwell B200 and AMD MI355X dominate the training quadrant; Cerebras CS-3 anchors high-throughput inference; the Groq LPU (now NVIDIA-owned LPX since the December 2025 $20B acquisition) holds the latency quadrant. The dashed arrow is the dominant 2026 deployment pattern from the OpenAI Cerebras case study: train on Blackwell, serve on Cerebras. AWS Trainium 2/4 and Tenstorrent Blackhole serve narrower cloud-locked and research niches respectively."
  - Shared caption words: bandwidth, cerebras, class, groq, inference, latency, memory, silicon
  - **Suggestion**: KEEP Figure 58.1.2, DROP Figure 58.1.1 (second figure has more specific detail (40 unique caption words, 660 char caption vs 13 / 202 char))

- **[REVIEW]** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html`
  - Figure 58.2.2 vs Figure 58.2.3 | caption-cosine=0.09 | caption-jaccard=0.06 | caption-shared=5 | combined-cosine=0.10
  - Rare shared phrase: "top-k sparsification"
  - Figure 58.2.2 caption: "One DeMo optimizer step across heterogeneous workers. Top-k sparsification of the local momentum buffer reduces per-step bandwidth from 140 GB to roughly 140 MB; Solana attestation replaces the InfiniBand trust model. (cloud H100, university A100, hobbyist RTX 4090, rented L40S). Three boxes show step 1 local momentum and top-k extract producing roughly 140 MB sparse vectors, step 2 sparse sync with Solana attestation, and step 3 global merge into local parameters. A second panel compares bandwidth per step at 70B parameters: DDP at 140 GB, FSDP at 70 GB, DiLoCo at 14 GB, DeMo at 140 MB, bars to scale."
  - Figure 58.2.3 caption: "The decentralized-training arc from the Folding@home cultural ancestor (2000) through Lin et al.'s 2017 Deep Gradient Compression (the top-k sparsification idea), the DeepMind DiLoCo line (2023), and the Peng-Kingma DeMo paper (November 2024, arXiv:2411.19870) that scaled the kernel to LLMs at 500-1000x compression. The Nous Psyche network's January 2025 launch trained a 1B model with ~300 nodes and landed within 1.5 perplexity of a centralized baseline. The Q4 2025 Psyche 7B run is in flight; the 2027 open question is whether the next run crosses the GPT-4 quality threshold and whether SNARK-based attestation closes the adversarial gap the warning in this section calls out."
  - Shared caption words: attestation, demo, diloco, model, sparsification
  - **Suggestion**: KEEP Figure 58.2.3, DROP Figure 58.2.2 (second figure has more specific detail (44 unique caption words, 683 char caption vs 31 / 609 char))

- **[REVIEW]** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html`
  - Figure 58.2.1 vs Figure 58.2.2 | caption-cosine=0.28 | caption-jaccard=0.11 | caption-shared=7 | combined-cosine=0.34
  - Figure 58.2.1 caption: "Per-step gradient bytes for a 70B model. Classical data-parallel pushes 70-280 GB per step (NVLink/InfiniBand only); DeMo's top-1% sparsification collapses that to ~140 MB, which fits inside an ordinary residential uplink. The 500-1000x gap is the entire reason decentralized training became viable in 2025. model. DDP all-reduce ~280 GB; FSDP ~140 GB; ZeRO-3 ~70 GB; DeMo v2 top-1% sparse ~0.14 GB; DisTrO async ~0.04 GB. A dashed red arrow spans the ZeRO-3-to-DeMo gap with a callout reading 500-1000x compression."
  - Figure 58.2.2 caption: "One DeMo optimizer step across heterogeneous workers. Top-k sparsification of the local momentum buffer reduces per-step bandwidth from 140 GB to roughly 140 MB; Solana attestation replaces the InfiniBand trust model. (cloud H100, university A100, hobbyist RTX 4090, rented L40S). Three boxes show step 1 local momentum and top-k extract producing roughly 140 MB sparse vectors, step 2 sparse sync with Solana attestation, and step 3 global merge into local parameters. A second panel compares bandwidth per step at 70B parameters: DDP at 140 GB, FSDP at 70 GB, DiLoCo at 14 GB, DeMo at 140 MB, bars to scale."
  - Shared caption words: demo, fsdp, infiniband, model, sparse, sparsification, step
  - **Suggestion**: KEEP Figure 58.2.2, DROP Figure 58.2.1 (second figure has more specific detail (29 unique caption words, 609 char caption vs 27 / 516 char))

- **[REVIEW]** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html`
  - Figure 58.2.1 vs Figure 58.2.3 | caption-cosine=0.18 | caption-jaccard=0.09 | caption-shared=7 | combined-cosine=0.17
  - Figure 58.2.1 caption: "Per-step gradient bytes for a 70B model. Classical data-parallel pushes 70-280 GB per step (NVLink/InfiniBand only); DeMo's top-1% sparsification collapses that to ~140 MB, which fits inside an ordinary residential uplink. The 500-1000x gap is the entire reason decentralized training became viable in 2025. model. DDP all-reduce ~280 GB; FSDP ~140 GB; ZeRO-3 ~70 GB; DeMo v2 top-1% sparse ~0.14 GB; DisTrO async ~0.04 GB. A dashed red arrow spans the ZeRO-3-to-DeMo gap with a callout reading 500-1000x compression."
  - Figure 58.2.3 caption: "The decentralized-training arc from the Folding@home cultural ancestor (2000) through Lin et al.'s 2017 Deep Gradient Compression (the top-k sparsification idea), the DeepMind DiLoCo line (2023), and the Peng-Kingma DeMo paper (November 2024, arXiv:2411.19870) that scaled the kernel to LLMs at 500-1000x compression. The Nous Psyche network's January 2025 launch trained a 1B model with ~300 nodes and landed within 1.5 perplexity of a centralized baseline. The Q4 2025 Psyche 7B run is in flight; the 2027 open question is whether the next run crosses the GPT-4 quality threshold and whether SNARK-based attestation closes the adversarial gap the warning in this section calls out."
  - Shared caption words: compression, decentralized, demo, gradient, model, sparsification, training
  - **Suggestion**: KEEP Figure 58.2.3, DROP Figure 58.2.1 (second figure has more specific detail (42 unique caption words, 683 char caption vs 27 / 516 char))

### part-15-llm-agentic-ai-research-frontiers  (1 pairs)

- **[REVIEW]** `part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/section-77.4.html`
  - Figure 77.4.1 vs Figure 77.4.2 | caption-cosine=0.19 | caption-jaccard=0.09 | caption-shared=8 | combined-cosine=0.19
  - Figure 77.4.1 caption: "Two 2027 scenarios for the augmentation/automation split. The 2025 78.7/21.3 split is measured; the 2027 split is two scenarios that hinge on whether agentic deployments scale. Left column shows the 2025 measured split: 78.7% augmentation (green large block) and 21.3% automation (red small block). Middle column is a labeled fork: 'Scenario A: augmentation share holds above 70%' and 'Scenario B: augmentation falls toward 50%'. Right column shows 2027 outcomes: Scenario A keeps 72% augmentation / 28% automation; Scenario B drops augmentation to 52% and automation rises to 48%. A bottom box lists three indicators (agentic-coding adoption, tier-1 customer-support absorption, BLS layoff share) that arbitrate the fork."
  - Figure 77.4.2 caption: "Both panels are true at once. Aggregated across the economy, 2025 is still dominated by augmentation; inside aggressive-adopter firms, specific roles have contracted 20-50%, while AI/ML engineering and senior software engineering have expanded. Policy that averages over occupations misses the concentrated impact; product strategy that averages over teams misses where adoption is fast. Left panel shows the aggregate 2025 Anthropic Economic Index split: a single stacked horizontal bar with 21.3% red automation and 78.7% navy augmentation, plus a smaller bar showing 5% of U.S. layoffs were AI-attributed and 95% from other causes. Right panel shows per-role workforce change within aggressive-adopter firms: junior copywriters -50%, voice-over artists -45%, tier-1 customer support -35%, paralegals -30%, basic translation -25%, basic graphic design -22%, senior SWE (augmented) +12% hiring, AI/ML engineers +85% hiring. Red bars for contraction, green bars for expansion."
  - Shared caption words: adoption, augmentation, automation, customer, green, split, support, tier
  - **Suggestion**: KEEP Figure 77.4.2, DROP Figure 77.4.1 (second figure has more specific detail (56 unique caption words, 976 char caption vs 27 / 722 char))

### part-2-understanding-llms  (3 pairs)

- **[REVIEW]** `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html`
  - Figure 8.2.1 vs Figure 8.2.2 | caption-cosine=0.30 | caption-jaccard=0.17 | caption-shared=4 | combined-cosine=0.28
  - Rare shared phrase: "reasoning model"
  - Figure 8.2.1 caption: "The reasoning model landscape as an archipelago: each island represents a model family (o1/o3, DeepSeek R1, QwQ), with bridges showing shared training techniques and architectural patterns."
  - Figure 8.2.2 caption: "Three patterns for reasoning model output. OpenAI hides the reasoning trace; DeepSeek and QwQ make it fully visible; Gemini exposes it as a separate API field."
  - Shared caption words: deepseek, model, patterns, reasoning
  - **Suggestion**: KEEP Figure 8.2.1, DROP Figure 8.2.2 (first figure has more specific detail (10 unique caption words, 189 char caption vs 10 / 159 char))

- **[REVIEW]** `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.5.html`
  - Figure 8.5.1 vs Figure 8.5.2 | caption-cosine=0.26 | caption-jaccard=0.15 | caption-shared=6 | combined-cosine=0.35
  - Rare shared phrase: "compute-optimal inference"
  - Figure 8.5.1 caption: "Compute-optimal inference means matching the reasoning budget to problem difficulty: easy questions need minimal tokens, while hard problems justify the full thinking budget."
  - Figure 8.5.2 caption: "Compute-optimal inference frontier. On easy tasks (green), larger models are optimal. On hard tasks (red), smaller models with test-time compute scaling cross over and outperform larger models at matched total FLOPs. The crossover point depends on task difficulty and reward model quality."
  - Shared caption words: compute, difficulty, easy, hard, inference, optimal
  - **Suggestion**: KEEP Figure 8.5.2, DROP Figure 8.5.1 (second figure has more specific detail (21 unique caption words, 289 char caption vs 13 / 174 char))

- **[REVIEW]** `part-2-understanding-llms/module-09-inference-optimization/section-9.4.html`
  - Figure 9.4.1 vs Figure 9.4.2 | caption-cosine=0.33 | caption-jaccard=0.24 | caption-shared=6 | combined-cosine=0.39
  - Rare shared phrase: "drafts tokens", "speculative decoding"
  - Figure 9.4.1 caption: "Speculative decoding: a fast junior model drafts tokens and a powerful senior model checks them in bulk, turning serial generation into parallel verification."
  - Figure 9.4.2 caption: "Speculative decoding drafts γ tokens with a fast model, then verifies them in one target model pass. Accepted tokens are free; rejected tokens are resampled from an adjusted distribution."
  - Shared caption words: decoding, drafts, fast, model, speculative, tokens
  - **Suggestion**: KEEP Figure 9.4.1, DROP Figure 9.4.2 (first figure has more specific detail (10 unique caption words, 158 char caption vs 9 / 187 char))

### part-3-working-with-llms  (1 pairs)

- **[REVIEW]** `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html`
  - Figure 12.4.1 vs Figure 12.4.2 | caption-cosine=0.20 | caption-jaccard=0.18 | caption-shared=4 | combined-cosine=0.72
  - Rare shared phrase: "prompt injection", "user input"
  - Figure 12.4.1 caption: "Prompt injection is the Trojan horse of LLM applications: malicious instructions hiding inside innocent-looking user input."
  - Figure 12.4.2 caption: "Three categories of prompt injection: direct (user input), indirect (third-party content), and jailbreaks (safety bypass)."
  - Shared caption words: injection, input, prompt, user
  - **Suggestion**: KEEP Figure 12.4.1, DROP Figure 12.4.2 (first figure has more specific detail (9 unique caption words, 123 char caption vs 9 / 122 char))

### part-4-training-adaptation  (3 pairs)

- **[REVIEW]** `part-4-training-adaptation/module-17-peft/section-17.4.html`
  - Figure 17.4.1 vs Figure 17.4.2 | caption-cosine=0.17 | caption-jaccard=0.09 | caption-shared=3 | combined-cosine=0.36
  - Rare shared phrase: "prompt methods", "soft prompt", "soft prompt methods"
  - Figure 17.4.1 caption: "The four main soft prompt methods differ in where they insert their learnable parameters. Prompt Tuning touches only the input embedding layer; Prefix Tuning and P-Tuning v2 inject learned key-value pairs into every attention layer; P-Tuning v1 uses a trainable encoder to place embeddings at chosen input positions."
  - Figure 17.4.2 caption: "Decision guide for choosing among soft prompt methods and LoRA. Most practitioners should default to LoRA unless they have a specific reason to use a soft prompt approach."
  - Shared caption words: methods, prompt, soft
  - **Suggestion**: KEEP Figure 17.4.1, DROP Figure 17.4.2 (first figure has more specific detail (22 unique caption words, 316 char caption vs 10 / 171 char))

- **[REVIEW]** `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html`
  - Figure 18.1.2a vs Figure 18.1.3 | caption-cosine=0.23 | caption-jaccard=0.13 | caption-shared=5 | combined-cosine=0.28
  - Rare shared phrase: "reward model"
  - Figure 18.1.2a caption: "The RL fine-tuning step of RLHF. The language model generates responses scored by a reward model, and PPO optimizes the policy to maximize reward while staying close to the original distribution via a KL penalty. (Source: Lambert et al., "Illustrating RLHF" , Hugging Face Blog, 2023.)"
  - Figure 18.1.3 caption: "The full ChatGPT-style training pipeline in three phases: pretraining on web-scale text, supervised fine-tuning on demonstration data, and RLHF optimization against a learned reward model."
  - Shared caption words: fine, model, reward, rlhf, tuning
  - **Suggestion**: KEEP Figure 18.1.2a, DROP Figure 18.1.3 (first figure has more specific detail (19 unique caption words, 285 char caption vs 14 / 188 char))

- **[REVIEW]** `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.6.html`
  - Figure 18.4.1a vs Figure 18.6.2 | caption-cosine=0.21 | caption-jaccard=0.08 | caption-shared=4 | combined-cosine=0.60
  - Figure 18.4.1a caption: "RLVR vs RLHF as exam-grading metaphors. Math answers can be auto-graded by a verifier (left, RLVR): objective, scalable, no humans needed. Essays must be judged by humans (right, RLHF): subjective, slow, but handles open-ended quality criteria. an ANSWER KEY and displays checkmarks and crosses, an objective binary reward. Right panel (RLHF): a robot hands an ESSAY EXAM to a panel of four human judges seated at a table, who deliberate and assign a subjective preference score."
  - Figure 18.6.2 caption: "RLHF uses a learned (noisy) reward model. RLVR uses verifiable correctness checks, producing exact reward signals without human annotation."
  - Shared caption words: human, reward, rlhf, rlvr
  - **Suggestion**: KEEP Figure 18.4.1a, DROP Figure 18.6.2 (first figure has more specific detail (36 unique caption words, 479 char caption vs 10 / 139 char))

### part-5-multimodal-llms  (3 pairs)

- **[REVIEW]** `part-5-multimodal-llms/module-22-vision-language-models/section-22.7.html`
  - Figure 22.7.1 vs Figure 22.7.2 | caption-cosine=0.55 | caption-jaccard=0.14 | caption-shared=5 | combined-cosine=0.59
  - Rare shared phrase: "early fusion", "late fusion", "modalities late"
  - Figure 22.7.1 caption: "The fusion spectrum. Early fusion shares all transformer layers across modalities. Late fusion shares almost nothing until the final layers. Mid-fusion (e.g., LLaVA) sits in between with a projection layer that maps a frozen vision encoder's output into the LLM's embedding space."
  - Figure 22.7.2 caption: "Fusion design space, late 2025. Mid-fusion dominates open-source because it leverages pretrained text LLMs; early fusion dominates frontier labs because it scales cleanly to many modalities; late fusion lives almost entirely in the retrieval world."
  - Shared caption words: early, fusion, late, modalities, space
  - **Suggestion**: KEEP Figure 22.7.1, DROP Figure 22.7.2 (first figure has more specific detail (16 unique caption words, 280 char caption vs 16 / 248 char))

- **[REVIEW]** `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.4.html`
  - Figure 23.4.1 vs Figure 23.4.2 | caption-cosine=0.12 | caption-jaccard=0.06 | caption-shared=2 | combined-cosine=0.17
  - Rare shared phrase: "direct d diffusion"
  - Figure 23.4.1 caption: "Direct 3D diffusion samples in a 3D latent space and decodes once. Multi-view-then-lift pipelines sample $N$ views and optimize 3D parameters to match, which is both more expensive and more failure-prone."
  - Figure 23.4.2 caption: "Comparison of late-2024 to 2025 direct 3D diffusion models. The output column matters most for practitioners: pick based on whether your downstream tool wants Gaussians (Trellis, GaussianAnything) or meshes (Direct3D, 3DTopia)."
  - Shared caption words: diffusion, direct
  - **Suggestion**: KEEP Figure 23.4.2, DROP Figure 23.4.1 (second figure has more specific detail (17 unique caption words, 227 char caption vs 16 / 204 char))

- **[REVIEW]** `part-5-multimodal-llms/module-22-vision-language-models/section-22.9.html`
  - Figure 22.9.1 vs Figure 22.9.2 | caption-cosine=0.24 | caption-jaccard=0.17 | caption-shared=5 | combined-cosine=0.24
  - Rare shared phrase: "early snapshot", "frontier omni"
  - Figure 22.9.1 caption: "Frontier omni models on six capability axes (early 2026 snapshot). Each model has a different Pareto curve; the optimal choice depends on which axes matter for your application."
  - Figure 22.9.2 caption: "Frontier omni model matrix, early 2026 snapshot. Benchmarks are approximate and shift quarterly. Cost figures are list price; volume discounts and free tiers vary by provider."
  - Shared caption words: early, frontier, model, omni, snapshot
  - **Suggestion**: KEEP Figure 22.9.2, DROP Figure 22.9.1 (second figure has more specific detail (14 unique caption words, 175 char caption vs 11 / 177 char))

### part-6-agentic-ai  (5 pairs)

- **[REVIEW]** `part-6-agentic-ai/module-26-ai-agents/section-26.1.html`
  - Figure 26.1.4 vs Figure 26.1.5 | caption-cosine=0.40 | caption-jaccard=0.20 | caption-shared=3 | combined-cosine=0.47
  - Rare shared phrase: "agentic design", "agentic design patterns", "design patterns"
  - Figure 26.1.4 caption: "Four agentic design patterns define the modern agent landscape: reflection, tool use, planning, and multi-agent coordination. Most real systems combine several."
  - Figure 26.1.5 caption: "The four agentic design patterns (Ng, 2024)"
  - Shared caption words: agentic, design, patterns
  - **Suggestion**: KEEP Figure 26.1.4, DROP Figure 26.1.5 (first figure has more specific detail (12 unique caption words, 160 char caption vs 0 / 43 char))

- **[REVIEW]** `part-6-agentic-ai/module-27-tool-use-protocols/section-27.4.html`
  - Figure 27.4.1 vs Figure 27.4.2 | caption-cosine=0.26 | caption-jaccard=0.22 | caption-shared=6 | combined-cosine=0.23
  - Rare shared phrase: "multi-purpose tool"
  - Figure 27.4.1 caption: "Good tool design versus bad. A monolithic multi-purpose tool confuses the agent, while atomic, well-labeled tools with clear boundaries make selection straightforward."
  - Figure 27.4.2 caption: "One multi-purpose tool gives the model a complicated interface to misuse. Four atomic tools each name themselves. The right-hand agent makes the same call in half the tokens, with half the retries."
  - Shared caption words: agent, atomic, multi, purpose, tool, tools
  - **Suggestion**: KEEP Figure 27.4.2, DROP Figure 27.4.1 (second figure has more specific detail (11 unique caption words, 197 char caption vs 10 / 167 char))

- **[REVIEW]** `part-6-agentic-ai/module-28-multi-agent-systems/section-28.2.html`
  - Figure 28.2.1 vs Figure 28.2.2 | caption-cosine=0.17 | caption-jaccard=0.11 | caption-shared=6 | combined-cosine=0.21
  - Rare shared phrase: "multi-agent topologies"
  - Figure 28.2.1 caption: "Three foundational multi-agent topologies. Hub-and-Spoke gives a single supervisor full control. Pipeline gives clean sequential handoff with no back-talk. Fully Connected gives maximum flexibility at the cost of message volume that scales as O(N²). Most production systems are hybrids: a supervisor handing structured subgoals to a pipeline of specialists."
  - Figure 28.2.2 caption: "Three advanced multi-agent topologies that extend the foundational set. Swarm uses directed handoffs (good when categories are known in advance). Debate forces structured disagreement followed by judgement (good for high-stakes evaluation). Hierarchical stacks supervisors recursively so each layer reasons at its own abstraction level (good when one supervisor would overflow its context budget)."
  - Shared caption words: agent, foundational, multi, structured, supervisor, topologies
  - **Suggestion**: KEEP Figure 28.2.2, DROP Figure 28.2.1 (second figure has more specific detail (28 unique caption words, 397 char caption vs 23 / 357 char))

- **[REVIEW]** `part-6-agentic-ai/module-28-multi-agent-systems/section-28.3.html`
  - Figure 28.3.1 vs Figure 28.3.2 | caption-cosine=0.26 | caption-jaccard=0.13 | caption-shared=4 | combined-cosine=0.34
  - Rare shared phrase: "graduated autonomy"
  - Figure 28.3.1 caption: "Human-in-the-loop oversight with graduated autonomy. Low-risk decisions (gold star) pass through automatically, while high-consequence actions require explicit human approval at the control panel."
  - Figure 28.3.2 caption: "Graduated autonomy in one conveyor belt. The agent is allowed to ship low-risk parcels without asking, medium-risk parcels after logging them, and never the red-flagged crates without a human signature."
  - Shared caption words: autonomy, graduated, human, risk
  - **Suggestion**: KEEP Figure 28.3.1, DROP Figure 28.3.2 (first figure has more specific detail (14 unique caption words, 196 char caption vs 12 / 202 char))

- **[REVIEW]** `part-6-agentic-ai/module-28-multi-agent-systems/section-28.3.html`
  - Figure 28.3.1 vs Figure 28.3.3 | caption-cosine=0.38 | caption-jaccard=0.14 | caption-shared=6 | combined-cosine=0.34
  - Figure 28.3.1 caption: "Human-in-the-loop oversight with graduated autonomy. Low-risk decisions (gold star) pass through automatically, while high-consequence actions require explicit human approval at the control panel."
  - Figure 28.3.3 caption: "Risk-routed approval flow. The classifier sorts proposed actions into three lanes. Low-risk actions skip the human entirely. Medium-risk actions run but emit an audit log so a human can review post-hoc. High-risk actions block the agent loop, page a human via Slack, and only resume on approval. As trust calibrates, more action categories migrate left (from "request approval" toward "auto execute")."
  - Shared caption words: actions, approval, high, human, loop, risk
  - **Suggestion**: KEEP Figure 28.3.3, DROP Figure 28.3.1 (second figure has more specific detail (26 unique caption words, 401 char caption vs 12 / 196 char))

### part-7-retrieval-information-extraction-with-llms  (4 pairs)

- **[REVIEW]** `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html`
  - Figure 32.3.1 vs Figure 32.3.2 | caption-cosine=0.35 | caption-jaccard=0.18 | caption-shared=3 | combined-cosine=0.21
  - Rare shared phrase: "agentic rag iterates"
  - Figure 32.3.1 caption: "Agentic RAG iterates through search, evaluation, and refinement cycles until the full picture emerges."
  - Figure 32.3.2 caption: "Agentic RAG iterates through decomposition, multi-source retrieval, and sufficiency evaluation before synthesizing a final answer."
  - Shared caption words: agentic, evaluation, iterates
  - **Suggestion**: KEEP Figure 32.3.2, DROP Figure 32.3.1 (second figure has more specific detail (8 unique caption words, 130 char caption vs 6 / 102 char))

- **[REVIEW]** `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.8.html`
  - Figure 31.8.2 vs Figure 31.8.3 | caption-cosine=0.33 | caption-jaccard=0.19 | caption-shared=5 | combined-cosine=0.27
  - Rare shared phrase: "late interaction", "query token"
  - Figure 31.8.2 caption: "ColPali processes document pages as images through a vision transformer, producing per-patch embeddings. Late interaction (MaxSim) scores each query token against all patches, finding the best match for each token."
  - Figure 31.8.3 caption: "Late interaction models let each query token independently interrogate every document token. It is like having a panel of specialist judges instead of one generalist."
  - Shared caption words: document, interaction, late, query, token
  - **Suggestion**: KEEP Figure 31.8.2, DROP Figure 31.8.3 (first figure has more specific detail (15 unique caption words, 214 char caption vs 7 / 166 char))

- **[REVIEW]** `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html`
  - Figure 33.1.1 vs Figure 33.1.2 | caption-cosine=0.15 | caption-jaccard=0.11 | caption-shared=4 | combined-cosine=0.18
  - Rare shared phrase: "joint embedding"
  - Figure 33.1.1 caption: "A joint embedding space. Each encoder maps its modality into the same vector space, normalized to lie on the unit hypersphere. Cosine similarity (equivalent to dot product on the sphere) is the retrieval score."
  - Figure 33.1.2 caption: "Joint embedding model landscape, late 2025. CLIP and SigLIP dominate the image-text axis; ImageBind, LanguageBind, and CLAP cover other modalities. Pick based on which modality combinations matter for your retrieval task."
  - Shared caption words: embedding, joint, modality, retrieval
  - **Suggestion**: KEEP Figure 33.1.2, DROP Figure 33.1.1 (second figure has more specific detail (18 unique caption words, 221 char caption vs 13 / 210 char))

- **[REVIEW]** `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html`
  - Figure 35.3.2 vs Figure 35.3.4 | caption-cosine=0.27 | caption-jaccard=0.12 | caption-shared=5 | combined-cosine=0.23
  - Rare shared phrase: "knowledge graph"
  - Figure 35.3.2 caption: "A small knowledge graph centred on Albert Einstein, showing how entities (cylinders, colour-coded by type) are connected by labelled relationships (named edges). A question like "who influenced the developer of General Relativity?" becomes a one-hop traversal: General Relativity ← developed ← Einstein → influenced_by → Newton. This is the structure RAG systems traverse when they have access to a knowledge graph instead of (or in addition to) raw text."
  - Figure 35.3.4 caption: "A knowledge graph encodes entities as nodes and relationships as labeled directed edges, enabling structured queries and multi-hop reasoning."
  - Shared caption words: edges, entities, graph, knowledge, relationships
  - **Suggestion**: KEEP Figure 35.3.2, DROP Figure 35.3.4 (first figure has more specific detail (26 unique caption words, 455 char caption vs 9 / 141 char))

### part-8-conversational-ai-with-llms  (1 pairs)

- **[REVIEW]** `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html`
  - Figure 37.3.1 vs Figure 37.3.2 | caption-cosine=0.49 | caption-jaccard=0.18 | caption-shared=5 | combined-cosine=0.51
  - Rare shared phrase: "long-term memory", "short-term memory"
  - Figure 37.3.1 caption: "Memory management in conversational AI: short-term memory holds the current chat, long-term memory stores user preferences, and working memory juggles it all without spilling."
  - Figure 37.3.2 caption: "Layered memory architecture showing how short-term memory, long-term memory, session storage, and user profiles feed into the LLM context window. This section covers the upper-left tier; Section 37.5 covers the rest."
  - Shared caption words: long, memory, short, term, user
  - **Suggestion**: KEEP Figure 37.3.2, DROP Figure 37.3.1 (second figure has more specific detail (13 unique caption words, 216 char caption vs 10 / 175 char))

### part-9-llm-evaluation-observability  (3 pairs)

- **[REVIEW]** `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.3.html`
  - Figure 42.3.1 vs Figure 42.3.2 | caption-cosine=0.56 | caption-jaccard=0.28 | caption-shared=5 | combined-cosine=0.86
  - Rare shared phrase: "llm testing pyramid", "llm testing pyramid unit", "llm testing pyramid unit tests"
  - Figure 42.3.1 caption: "The LLM testing pyramid: unit tests form the solid base, integration tests fill the middle, and expensive end-to-end evaluations sit at the narrow top. Do not invert this pyramid."
  - Figure 42.3.2 caption: "The LLM testing pyramid. Unit tests with mocked responses form the foundation; adversarial tests sit at the top."
  - Shared caption words: form, pyramid, testing, tests, unit
  - **Suggestion**: KEEP Figure 42.3.1, DROP Figure 42.3.2 (first figure has more specific detail (9 unique caption words, 179 char caption vs 4 / 112 char))

- **[REVIEW]** `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.5.html`
  - Figure 42.5.1 vs Figure 42.5.2 | caption-cosine=0.44 | caption-jaccard=0.35 | caption-shared=7 | combined-cosine=0.78
  - Rare shared phrase: "pipeline each gate"
  - Figure 42.5.1 caption: "Evaluation quality gates act as checkpoints in the deployment pipeline. Each gate requires the model to meet predefined metric thresholds before proceeding to the next stage."
  - Figure 42.5.2 caption: "A three-stage quality gate pipeline. Each gate uses different evaluation strategies and thresholds appropriate to its position in the deployment lifecycle."
  - Shared caption words: deployment, evaluation, gate, pipeline, quality, stage, thresholds
  - **Suggestion**: KEEP Figure 42.5.1, DROP Figure 42.5.2 (first figure has more specific detail (8 unique caption words, 174 char caption vs 5 / 155 char))

- **[REVIEW]** `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.5.html`
  - Figure 43.5.1 vs Figure 43.5.2 | caption-cosine=0.26 | caption-jaccard=0.16 | caption-shared=6 | combined-cosine=0.20
  - Rare shared phrase: "benchmarks aggregating"
  - Figure 43.5.1 caption: "Multimodal eval is inherently a per-pair leaderboard. Vision-language, audio-language, and video-language models occupy different podiums with different benchmarks; aggregating across modalities hides the regression that matters."
  - Figure 43.5.2 caption: "The modality matrix. Each input-output pair is a separate evaluation regime with its own canonical benchmarks. Aggregating across cells hides cell-specific failures; modality-stratified eval sets keep each pair's metrics independent so a regression in one cell does not get masked by an improvement in another."
  - Shared caption words: aggregating, benchmarks, eval, hides, pair, regression
  - **Suggestion**: KEEP Figure 43.5.2, DROP Figure 43.5.1 (second figure has more specific detail (18 unique caption words, 310 char caption vs 13 / 229 char))
