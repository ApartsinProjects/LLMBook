# Part I Foundations: Example, Analogy, and Code Pedagogy Review

**Review date:** 2026-03-26
**Scope:** Modules 00 through 05 (all of Part I: Foundations)
**Reviewers:** Example and Analogy Designer (Agent 06) + Code Pedagogy Engineer (Agent 08)

---

## Executive Summary

Part I is strong overall. Analogies are generally concrete and well matched to the target audience (software engineers). Code examples are syntactically correct, use current libraries, and show expected output in most sections. The main systemic issues are: (1) several modules lack "modify and observe" exercises that would deepen understanding; (2) a few key concepts are explained only in abstract terms without a grounding analogy; (3) Section 0.4 (RL) and Section 4.5 (expressiveness theory) have no code output shown, breaking the pattern set elsewhere; and (4) the Adam optimizer is used in code across multiple modules but never explained.

**Overall concreteness:** ADEQUATE (strong in places, with specific gaps identified below)
**Overall code quality:** GOOD (with targeted improvements needed)

---

## Part 1: Example and Analogy Review

### Module 00: ML and PyTorch Foundations

**Strengths:**
- Section 0.1 uses the "learning sheet music before playing a symphony" analogy for ML basics, which is vivid and sets the right tone.
- Section 0.1's house price features example grounds the abstract concept of feature engineering in everyday terms.
- Section 0.2's backpropagation numerical walkthrough with a concrete chain rule example is outstanding pedagogy.
- Section 0.4's dog training analogy for RL is carried consistently and mapped precisely to LLM training terms.
- The RL vocabulary table mapping each concept to its LLM analogy (agent = LLM, action = next token, etc.) is one of the best reference artifacts in Part I.
- The salt/soup analogy for PPO clipping in Section 0.4 is memorable and mechanistically accurate.

**Weaknesses and Missed Opportunities:**
1. **Gradient descent (Section 0.1):** The gradient descent explanation relies on the formula and an SVG curve. A "hiking downhill in fog" analogy (you feel the slope under your feet and step in the steepest-downhill direction) would make the local nature of gradient descent visceral. Currently the concept is explained correctly but abstractly.
   - Suggested addition: One paragraph with the fog analogy, noting where it breaks down (real landscapes have terrain; loss landscapes have millions of dimensions).

2. **Cross-entropy loss (Section 0.1):** The formula is given and its connection to LLMs is noted, but there is no worked numeric example showing what cross-entropy looks like for a few sample predictions (e.g., model says P=0.9 for the right token vs. P=0.01). This is a missed "aha moment" opportunity.
   - Suggested addition: A 3-row table showing predicted probability, cross-entropy value, and a plain-language interpretation.

3. **Activation functions (Section 0.2):** GELU is mentioned as important for transformers but gets no intuitive explanation. "Smoothed ReLU that allows small negative values" does not help students picture why it matters.
   - Suggested analogy: "GELU is like a bouncer at a club who lets a few people with almost-valid IDs slip through, instead of a strict yes/no at the door (ReLU)."
   - Where it breaks down: the analogy does not capture the probabilistic weighting by the Gaussian CDF.

4. **Adam optimizer (Sections 0.2, 0.3, 0.4):** Adam appears in code across three sections but is never explained. Students encounter `optim.Adam(...)` without understanding what distinguishes it from SGD. This is the single most referenced unexplained concept in Part I.
   - Suggested addition: A 2-paragraph callout box in Section 0.2 or 0.3 explaining Adam as "SGD with two memories: one for the average gradient direction, one for the average gradient magnitude."

5. **Section 0.4 lacks edge case examples:** The RL section does not show what happens when the reward signal is sparse or delayed, which is the exact scenario in RLHF (reward comes only after the full response). A brief example of how early token choices affect final reward would strengthen the LLM connection.

**Analogy quality check for "where it breaks down" notes:**
- The dog training analogy (0.4) does NOT include a note about where it breaks down. Dogs learn from immediate treats; LLMs receive reward only after generating a complete response. This distinction matters and should be called out.
- The "filing cabinet vs. color mixer" analogy (1.2) does include a clear breakdown note. Good.
- The "GPS coordinates for words" analogy (1.3) does include a breakdown note. Good.

---

### Module 01: NLP and Text Representation

**Strengths:**
- The four-eras framework (rule-based, statistical, neural, LLM) in Section 1.1 provides an excellent mental model that the whole module hangs on.
- The "filing cabinet vs. color mixer" analogy bridging sparse to dense representations (Section 1.2) is one of the strongest analogies in Part I. It illuminates the mechanism, not just the surface.
- Section 1.3's "GPS coordinates for words" mental model for embeddings is concrete and internationally accessible.
- The king/queen/man/woman analogy example with actual vector arithmetic is the classic "aha moment" example and is executed well.
- The cosine similarity SVG with king, queen, and refrigerator vectors gives students a geometric picture they can carry forward.

**Weaknesses and Missed Opportunities:**
1. **Negative sampling (Section 1.3):** The math formula is shown and there is a brief plain-English explanation, but no concrete numerical walkthrough. Given that negative sampling is the actual training trick that makes Word2Vec practical, a step-by-step example with 3 to 5 words showing which words are positive and negative samples would cement understanding.
   - Suggested addition: A worked example with a center word "cat," positive context "sat," and 3 random negative samples ("economics," "quantum," "umbrella"), showing why the dot products should be large for "sat" and small for the negatives.

2. **GloVe (Section 1.3):** Coverage is thin compared to Word2Vec. The co-occurrence ratio insight is mentioned but no concrete numeric example is shown. A small 4x4 co-occurrence matrix with actual word pairs would make the concept tangible.
   - Suggested addition: A mini co-occurrence matrix for words like "ice," "steam," "solid," "water" showing how ratios reveal semantic relationships.

3. **ELMo layer behavior (Section 1.4):** The claim that lower layers capture syntax and upper layers capture semantics is stated but not demonstrated. A concrete example showing the same word "bank" getting different attention from different layers would strengthen this significantly.

4. **Polysemy examples (Section 1.4):** "Bank" appears in three contexts, which is good, but the section would benefit from a running example tracked through the entire module (the same word processed by BoW, Word2Vec, and ELMo) to show how each method handles it differently. This would create a narrative thread.

---

### Module 02: Tokenization and Subword Models

**Strengths:**
- Section 2.1's "invisible gateway" framing effectively conveys that tokenization is not just preprocessing but a critical design decision.
- The "token tax" concept for multilingual equity is a memorable framing that resonates with the target audience of software engineers who think about API costs.
- The BPE merge tree SVG in Section 2.2 is excellent: it shows the algorithm step by step with actual corpus text.
- The full BPE implementation from scratch (Section 2.2) is the kind of "build it to understand it" lab that works extremely well for engineers.

**Weaknesses and Missed Opportunities:**
1. **Vocabulary size tradeoff (Section 2.1):** This is explained in prose but lacks a concrete numeric example. A table showing the same sentence tokenized at character level (150 tokens), BPE (30 tokens), and word level (25 tokens but with 3 OOV words) would make the tradeoff visceral.
   - Suggested addition: A side-by-side comparison table with actual token counts and the resulting context window impact.

2. **Tokenization artifact failures (Section 2.1):** The section mentions that tokenization causes arithmetic failures but does not show a concrete example of an LLM failing at math because of token boundaries (e.g., "372" being split as "37" + "2" vs. "3" + "72"). This is one of the most surprising and memorable examples in the field.
   - Suggested addition: A "Try it yourself" exercise asking students to tokenize numbers with tiktoken and observe the splits.

3. **Unigram model (Section 2.2):** This is the most abstract of the three algorithms and gets the least analogy support. The Viterbi decoding explanation would benefit from a "cheapest route on a map" analogy (finding the path through a city where each segment has a cost).
   - Where it breaks down: in a real map you can revisit nodes; in Viterbi segmentation you move strictly left to right.

4. **No analogy for byte-level BPE (Section 2.2):** The transition from character-level to byte-level is explained technically but lacks an intuitive hook. A possible analogy: "Byte-level BPE is like building words from LEGO bricks where you only need 256 different brick shapes instead of thousands of character shapes."

---

### Module 03: Sequence Models and Attention

**Strengths:**
- The "sticky note" analogy for the RNN hidden state (Section 3.1) is vivid: summarizing a book by reading one page at a time and keeping only a single sticky note.
- The "searching a library" analogy for attention (Section 3.2) is a strong setup for the Q/K/V framework.
- The vanishing gradient SVG visualization showing shrinking gradients across time steps is an excellent "aha moment" diagram.
- The attention weight heatmap for translation (Section 3.2) gives students a visual they can reference when thinking about what attention "does."
- The "differentiable dictionary lookup" framing for attention (Section 3.2) is precise and carries forward perfectly into the Q/K/V abstraction.

**Weaknesses and Missed Opportunities:**
1. **LSTM gating (Section 3.1):** The LSTM cell is explained with gates labeled, but there is no everyday analogy for the gating mechanism itself. A possible analogy: "The LSTM's forget gate is like an email filter: it decides which old messages to keep and which to discard before new messages arrive."
   - Where it breaks down: email filters are binary (keep/delete); forget gates produce continuous values between 0 and 1.

2. **Seq2seq bottleneck (Section 3.1):** The bottleneck problem is described but could benefit from a more visceral example. "Imagine translating a 500-page novel into a single tweet, and then asking someone to reconstruct the novel from that tweet." This would make the tension that attention resolves feel urgent.

3. **Scaling factor in scaled dot-product attention (Section 3.3):** The sqrt(d_k) scaling is explained mathematically (variance analysis) but the intuitive reason is not given a memorable framing. Possible: "Without scaling, as d_k grows, dot products become so large that softmax saturates and assigns nearly all weight to one key. Scaling is like adjusting the volume knob so you can still hear all the instruments."
   - Where it breaks down: volume is linear; scaling by sqrt(d_k) is specific to the variance of random dot products.

4. **Multi-head attention "why" (Section 3.3):** The concept that different heads capture different relationship types is stated but not demonstrated with a concrete example. A table showing "Head 1 attends to the previous word (syntax), Head 2 attends to the subject (semantics), Head 3 attends to negation words" would ground this claim.

---

### Module 04: Transformer Architecture

**Strengths:**
- Section 4.1's positional encoding heatmap SVG is a visually striking way to show the frequency interpretation.
- Section 4.2's full from-scratch implementation is the crown jewel of Part I. Breaking it into logical pieces (config, attention, FFN, block, model) with shape annotations at each stage is textbook scaffolding.
- The hyperparameter table at the start of Section 4.2 sets clear expectations.
- Section 4.3's "Modern LLM recipe table" showing which components real models combine is an excellent reference artifact.
- Section 4.4's roofline model explanation grounds GPU performance in a visual framework engineers can reason about.

**Weaknesses and Missed Opportunities:**
1. **Residual connections (Section 4.1):** The "information superhighway" concept is present but could be strengthened with a concrete analogy. "Residual connections are like express lanes on a highway: information can skip congested layers and arrive at the output directly, while the transformer blocks add refinements at each exit."
   - Where it breaks down: highway lanes do not process information; they just pass it through.

2. **Pre-LN vs. Post-LN (Section 4.1):** This important distinction is explained but lacks a memorable example of what goes wrong with Post-LN (training instability at depth). A brief note like "GPT-2 used Post-LN and required careful initialization; switching to Pre-LN allowed GPT-3 to scale to 96 layers without special tricks" would make the practical impact concrete.

3. **Weight tying (Section 4.2):** The decision to share weights between embedding and output projection is mentioned in passing but deserves more attention. This is a genuinely surprising design choice that saves significant parameters.

4. **Section 4.5 (Expressiveness Theory):** This is entirely theoretical with no code examples. While acceptable for a research-oriented section, a single demonstration showing a fixed-depth transformer failing at a counting task (then succeeding with chain-of-thought) would make the theoretical limits feel real rather than abstract.

5. **MoE routing (Section 4.3):** The routing mechanism is described but could benefit from a concrete numeric example showing how tokens get assigned to experts.

---

### Module 05: Decoding and Text Generation

**Strengths:**
- Section 5.1's search tree SVG for greedy vs. beam search is the definitive "aha moment" diagram for why greedy decoding fails. The colored paths showing locally optimal vs. globally optimal choices are immediately clear.
- Section 5.2's side-by-side "confident" vs. "uncertain" distribution diagram for top-p sampling is excellent pedagogy, showing adaptive behavior visually.
- The progression from temperature to top-k to top-p to min-p in Section 5.2 builds perfectly from simple to complex.
- Every sampling method in Section 5.2 includes both implementation code AND a concrete numeric example with output. This is the gold standard for code pedagogy.
- Section 5.3's speculative decoding explanation is accessible and connects to practical serving concerns.

**Weaknesses and Missed Opportunities:**
1. **Repetition penalty (Section 5.2):** The concept is explained but lacks a before/after example showing the same prompt with and without repetition penalty. This is the kind of side-by-side comparison that makes the effect tangible.

2. **Beam search pruning (Section 5.1):** The algorithm is shown but there is no concrete example of beam search producing a different (better) result than greedy. Walking through a 3-step example where greedy picks "cat sat on" but beam search finds "old cat quietly" with a higher joint probability would make the value of beam search unmistakable.

3. **Diffusion LMs (Section 5.4):** This section covers a cutting-edge topic. The discrete diffusion forward/reverse process is inherently hard to analogize. A possible analogy: "Imagine a ransom note where each word is gradually replaced with a random word. The diffusion model learns to reverse this process, restoring the original message by guessing which words were replaced."
   - Where it breaks down: diffusion LMs generate new text, not restore original text.

4. **Grammar-constrained decoding (Section 5.3):** The concept of logit masking with finite-state machines is powerful but abstract. A concrete example showing how a JSON schema constrains token choices at each step (after `{"name":` only `"` is valid) would ground the concept.

---

## Part 2: Code Pedagogy Review

### Module 00: ML and PyTorch Foundations

**Code block counts:** Section 0.1: 4 blocks, Section 0.2: 3 blocks, Section 0.3: ~14 blocks, Section 0.4: 2 blocks
**Output shown:** Sections 0.1 and 0.2 show output consistently. Section 0.4 shows NO output for either code example.

**Strengths:**
- Section 0.1 code uses only NumPy, appropriate for foundations. Each example illustrates exactly one concept (standardization, mini-batch SGD, overfitting, cross-validation).
- Section 0.3 (PyTorch tutorial) is the most code-dense section in Part I and has excellent pedagogical scaffolding: tensors, autograd, nn.Module, DataLoader, training loop, saving/loading, debugging, full lab.
- The FashionMNIST lab in Section 0.3 is runnable end-to-end with clear expected output.
- Code comments explain "why" rather than "what" in most places.

**Issues:**
1. **Section 0.4: No code output shown.** The SimpleGridWorld environment and REINFORCE sketch have no output blocks. Students cannot verify their understanding without running the code. This is the most significant code pedagogy gap in Module 00.
   - Fix: Add 5 to 10 lines of training output showing reward improving over episodes.

2. **Section 0.4: REINFORCE code is a sketch, not runnable.** The code shows the environment class but does not include a complete training loop that a student could copy, run, and observe learning.
   - Fix: Add a minimal training loop (10 to 15 lines) that trains for 1000 episodes and prints average reward every 200 episodes.

3. **Adam optimizer used but not explained.** `optim.Adam` appears in Section 0.2 (Example 3), Section 0.3 (training loop), and Section 0.4 (REINFORCE sketch) without any explanation of what makes it different from SGD.
   - Fix: Add a brief explanation in Section 0.2 or 0.3 before first use.

4. **No mixed-precision example in Section 0.3.** Given that every LLM training run uses mixed precision, the PyTorch tutorial should include a 5-line `torch.cuda.amp` example.
   - Fix: Add a minimal autocast/GradScaler snippet, even if it requires GPU.

5. **No "modify and observe" exercises in Section 0.4.** This is the only section in Module 00 without hands-on exercises. The chapter plan identifies this gap.
   - Fix: Add 2 to 3 exercises (change gamma, modify reward structure, compare random vs. trained policy).

---

### Module 01: NLP and Text Representation

**Code block counts:** Section 1.2: 6 blocks, Section 1.3: 7 blocks, Section 1.4: 2 blocks
**Output shown:** Sections 1.2 and 1.3 show output for most examples. Section 1.4 does not consistently show output.

**Strengths:**
- Section 1.2 shows both NLTK and spaCy implementations for the same pipeline, which is practical and helps students see library differences.
- Section 1.3's Word2Vec training code is complete and runnable with Gensim. Parameters are well-commented.
- The cosine similarity implementation (Section 1.3) shows both the manual NumPy version and the concept, teaching the math alongside the library call.
- The t-SNE visualization code is a valuable "see the embeddings" moment.
- Section 1.4 uses BERT via Hugging Face for contextual embeddings, which is the right library choice for practical work.

**Issues:**
1. **Section 1.3 Word2Vec training corpus is tiny (10 sentences).** While this is acknowledged in a comment, the output will show unreliable similarities. Adding a note like "With only 10 sentences, similarities will be noisy. With millions of sentences (or pre-trained vectors), you would see king/queen, paris/france, and dog/cat cluster reliably" would manage expectations.
   - Fix: Add a brief callout below the training code.

2. **Section 1.3 lacks library version pins.** The code imports gensim, numpy, seaborn, and sklearn without specifying versions. Since gensim's API has changed between major versions, a comment like `# Tested with gensim==4.3, numpy==1.24` would improve reproducibility.
   - Fix: Add version comments at the top of each code block or in a requirements callout.

3. **Section 1.4 BERT code does not show output.** The `get_word_embedding` function and the "bank" polysemy demonstration do not include expected output. Students cannot verify that "bank" in financial and river contexts produces different vectors without running the code.
   - Fix: Add output showing cosine similarity values between the different "bank" embeddings.

4. **Exercise scaffolding for "Word2Vec from scratch in PyTorch" (Section 1.4).** This challenge exercise has no starter code or skeleton. For intermediate students, this is too open-ended.
   - Fix: Provide a skeleton with the Skip-gram architecture defined and blanks for the training loop.

5. **No "modify and observe" exercises in Sections 1.1, 1.2, or 1.3.** All exercises are consolidated at the end of Section 1.4. The earlier sections have only inline "Try It Yourself" prompts without structure.
   - Fix: Add 1 to 2 short exercises per section (e.g., "Change the window size to 5 and re-train Word2Vec. What changes in the most_similar output?").

---

### Module 02: Tokenization and Subword Models

**Code block counts:** Section 2.1: 4 blocks, Section 2.2: 3 blocks, Section 2.3: ~6 blocks
**Output shown:** Good coverage in Sections 2.1 and 2.2. Section 2.3 likely shows output for the comparison lab.

**Strengths:**
- The BPE from-scratch implementation (Section 2.2) is the standout code example. Every line maps to a step in the algorithm. This is textbook "build it to understand it."
- Section 2.1 uses tiktoken (OpenAI's library), which is the right choice for showing real-world tokenizer behavior.
- Section 2.3's chat template examples using Hugging Face `apply_chat_template` are immediately practical.
- The multilingual fertility comparison lab (Section 2.3) produces quantitative results that make the "token tax" concept concrete.
- The API cost estimation utility (Section 2.3) connects tokenization directly to dollars, which is memorable for engineers.

**Issues:**
1. **BPE encoding function not shown (Section 2.2).** The lab implements BPE training (learning merges) but according to the chapter plan, the encoding function (applying learned merges to new text) should also be shown. If missing, this is a gap: students learn to train a tokenizer but not to use it.
   - Fix: Add a `bpe_encode(text, merges)` function that applies the merge table to tokenize new input.

2. **WordPiece implementation is simulated/pseudocode (Section 2.2).** The chapter plan notes a "simulated WordPiece MaxMatch tokenization." If this is pseudocode rather than runnable code, it breaks the pattern of runnable examples.
   - Fix: Make it a runnable Python function, even if simplified.

3. **No Unigram code example (Section 2.2).** The Unigram model is explained conceptually but has no implementation. Given that Unigram uses Viterbi decoding (a dynamic programming algorithm), even a simplified 20-line implementation would help engineers who think in code.
   - Fix: Add a minimal Viterbi segmentation function with a small vocabulary.

4. **Section 2.1 code blocks use tiktoken but do not show installation.** A `pip install tiktoken` note or requirements comment would help reproducibility.

5. **No "modify and observe" exercises for BPE.** The BPE lab is a follow-along implementation. Adding a prompt like "Change the corpus to include code snippets. How do the merges change? Why?" would deepen understanding.
   - Fix: Add 2 exploration prompts after the BPE lab.

---

### Module 03: Sequence Models and Attention

**Code block counts:** Section 3.1: 5 blocks, Section 3.2: 4 blocks, Section 3.3: 6 blocks
**Output shown:** Sections 3.1 and 3.3 show output consistently. Section 3.2 should be verified.

**Strengths:**
- Section 3.1's gradient magnitude demonstration across time steps is a perfect "show, don't tell" moment for vanishing gradients.
- Section 3.3's `MultiHeadSelfAttention` class is the most important reusable code artifact in Module 03, and it is well-structured as an `nn.Module`.
- The softmax temperature demonstration (Section 3.3) with concrete values showing how temperature changes attention distributions is effective.
- The causal mask construction (Section 3.3) is a concise, self-contained example that illustrates the concept perfectly.
- The complexity benchmarking code (Section 3.3) grounds the O(n^2) claim in measured numbers.

**Issues:**
1. **Seq2seq model in Section 3.1 may be too complex for a "putting it all together" example.** A complete translation model with encoder, decoder, and attention is a lot of code in one block. If this exceeds 50 lines, consider breaking it into smaller pieces with explanations between each piece.
   - Fix: Split into encoder, decoder, and training loop subsections.

2. **Bahdanau attention implementation (Section 3.2) should include shape comments.** Attention implementations are notorious for shape confusion. Adding `# shape: (batch, seq_len, hidden)` comments at key lines would prevent confusion.
   - Fix: Add shape annotations to all tensor operations.

3. **No "modify and observe" exercises in Module 03.** The quiz questions are conceptual (multiple choice and short answer). No section asks students to modify the attention code and observe what happens.
   - Fix: Add exercises like "Remove the causal mask and observe how the output changes" or "Set all attention weights to uniform and compare generation quality."

4. **Attention visualization code (Section 3.2) should show a rendered heatmap.** If the visualization code only generates the attention weights without showing the plot output, students miss the payoff.
   - Fix: Include a rendered example heatmap (as an SVG or description of expected output).

---

### Module 04: Transformer Architecture

**Code block counts:** Section 4.1: 6 blocks (including positional encoding), Section 4.2: 10 blocks (the full implementation), Section 4.3: 3 blocks (pseudocode/snippets), Section 4.4: 3 blocks (Triton)
**Output shown:** Section 4.2 shows training output. Section 4.1 shows encoding visualization.

**Strengths:**
- Section 4.2 is the best coding lab in Part I. The progression from config to CausalSelfAttention to FeedForward to TransformerBlock to GPTModel is perfect pedagogical scaffolding, building one layer at a time.
- Shape annotations at each stage in Section 4.2 (`B, T, C = x.shape`) are excellent. This should be the standard for all code in Part I.
- The dataclass for configuration is a good modern Python practice.
- Section 4.4's Triton vector addition and fused softmax kernels are a unique offering not found in most LLM courses.
- Using `register_buffer` for the causal mask (Section 4.2) teaches a real PyTorch pattern that students will need in practice.

**Issues:**
1. **Section 4.2 training loop output should show a loss curve.** The chapter plan mentions a training loss curve example diagram. If the code does not print loss at intervals, students cannot observe learning.
   - Fix: Ensure the training loop prints loss every N steps, and show expected output.

2. **Section 4.3 code is pseudocode, not runnable.** RoPE, GQA, and MoE top-k gating are shown as pseudocode or simplified snippets. For the survey section, this is acceptable, but at least one (RoPE is the best candidate) should be runnable.
   - Fix: Make the RoPE snippet a self-contained function that students can apply to the Section 4.2 model.

3. **Section 4.4 Triton code requires GPU.** This is unavoidable for Triton, but a note about CPU-only alternatives or Colab links would help students without GPU access.
   - Fix: Add a "Requirements" callout noting GPU necessity and suggesting Colab.

4. **Section 4.5 has no code at all.** This is the only section in Part I that is purely prose-based. A demonstration of transformer failure on a counting task (e.g., counting "a" tokens in a string) with and without chain-of-thought would make the theory tangible.
   - Fix: Add one 15-line code example showing the model failing at a task that exceeds its computational depth.

5. **Weight tying (Section 4.2):** If weight tying between embedding and output projection is implemented, a comment explaining the parameter savings (eliminating vocab_size * d_model parameters) would reinforce the concept.

---

### Module 05: Decoding and Text Generation

**Code block counts:** Section 5.1: 5 blocks, Section 5.2: 6 blocks, Section 5.3: ~5 blocks, Section 5.4: 3 blocks
**Output shown:** Sections 5.1 and 5.2 show output excellently. Section 5.3 and 5.4 should be verified.

**Strengths:**
- Section 5.2 is the code pedagogy gold standard in Part I. Every function (temperature, top-k, top-p, min-p) follows the same pattern: definition, implementation, concrete example with numeric output. This consistency is outstanding.
- The side-by-side comparison of "confident" vs. "uncertain" distributions for top-p and min-p (Section 5.2) grounds adaptive behavior in specific numbers.
- Each sampling function is self-contained and uses only PyTorch (no hidden dependencies).
- The code uses f-strings, descriptive variable names, and comments that explain "why."
- Section 5.1's beam search implementation with score tracking teaches the algorithm by building it.

**Issues:**
1. **Section 5.3 code may not be fully runnable.** Contrastive decoding requires two models (expert and amateur), and grammar-constrained decoding uses Outlines. If these are shown as conceptual code, a note should clarify: "This code requires two loaded models; see the linked notebook for a runnable version."
   - Fix: Add requirements notes and links where full runnable versions would be too large for inline display.

2. **Section 5.4 diffusion code is conceptual.** The simplified discrete diffusion training loop is appropriate for a research-oriented section, but expected output should still be shown, even if simulated.
   - Fix: Add expected output comments or a brief description of what the output would look like.

3. **No "modify and observe" exercises in Module 05.** The quiz questions are conceptual. No section asks students to experiment with different temperature/top-p values on the same prompt and compare outputs.
   - Fix: Add a lab exercise: "Using the sampling functions from Section 5.2, generate 5 completions at temperature 0.3, 0.7, and 1.2. Describe the quality/diversity tradeoff you observe."

4. **Repetition penalty code (Section 5.2) should include a before/after demonstration.** The penalty formula is shown, but running the same prompt with and without the penalty would make the effect visible.
   - Fix: Add a comparison showing generated text with and without repetition penalty.

5. **Library versions not pinned.** Section 5.2 uses PyTorch's `F.softmax` and `torch.multinomial`, which are stable, but Section 5.3's Outlines library reference should note the version.

---

## Cross-Cutting Issues

### Systemic Issue 1: Missing "modify and observe" exercises
Modules 00 (Section 0.4), 01 (Sections 1.1 through 1.3), 03 (all sections), 04 (Sections 4.1, 4.3, 4.5), and 05 (all sections) lack structured exercises that ask students to change code and observe the effect. This is the single most impactful improvement opportunity across Part I.

**Recommendation:** Add 2 to 3 "modify and observe" prompts per section, each asking the student to change one parameter and describe what happens.

### Systemic Issue 2: Inconsistent output display
Sections 0.4, 1.4 (partially), 4.5, and 5.4 do not show expected output for their code examples. The rest of Part I sets a strong standard of showing output inline.

**Recommendation:** Every code block that produces output should have a corresponding output block, even if the output is approximated or described.

### Systemic Issue 3: Library version reproducibility
No section in Part I pins library versions in code comments or a requirements block. Given that gensim, transformers, tiktoken, and triton all have API-breaking changes between major versions, this is a reproducibility risk.

**Recommendation:** Add a `# Requirements: gensim>=4.3, transformers>=4.36, tiktoken>=0.5` comment at the top of each section's first code block, or add a centralized requirements file.

### Systemic Issue 4: Adam optimizer gap
Adam is the default optimizer used in code across Modules 00, 01, 03, and 04, but it is never explained. Students are told what SGD does but not what Adam adds.

**Recommendation:** Add a focused 2-paragraph explanation (with the "two memories" analogy) in Section 0.2 or 0.3, before its first use in code.

---

## Priority Improvements (Ranked)

| Rank | Issue | Impact | Effort |
|------|-------|--------|--------|
| 1 | Add "modify and observe" exercises across all modules | High | Medium |
| 2 | Add code output to Section 0.4 (RL) and make REINFORCE runnable | High | Low |
| 3 | Explain Adam optimizer before first code use | High | Low |
| 4 | Add cross-entropy worked numeric example (Section 0.1) | Medium | Low |
| 5 | Add output to Section 1.4 BERT contextual embedding demo | Medium | Low |
| 6 | Pin library versions across all code blocks | Medium | Low |
| 7 | Add BPE encoding function to complete the Section 2.2 lab | Medium | Low |
| 8 | Add "where the analogy breaks down" note to Section 0.4 dog training | Medium | Low |
| 9 | Add negative sampling worked example (Section 1.3) | Medium | Low |
| 10 | Add one code example to Section 4.5 (expressiveness theory) | Medium | Medium |
| 11 | Add concrete beam search advantage example (Section 5.1) | Medium | Low |
| 12 | Add modify-and-observe lab to Section 5.2 (sampling methods) | Medium | Low |
| 13 | Strengthen the gradient descent analogy (Section 0.1) | Low | Low |
| 14 | Add GloVe co-occurrence matrix numeric example (Section 1.3) | Low | Medium |
| 15 | Make RoPE snippet runnable in Section 4.3 | Low | Medium |
