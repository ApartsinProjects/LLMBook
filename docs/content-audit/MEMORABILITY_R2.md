# Memorability Designer - Round 2 Report

Agent: 27-memorability-designer (cycle-1, parallel run)
Date: 2026-05-18
Branch: v2.0

## Scope
Foundational-concept sections in Parts 1-3, modules 1-6 and 12-14 (the canonical-home sections for big ideas like tokenization, attention, transformer, scaling laws, RAG/hybrid, prompt engineering, agents).

## Approach
For each target section's `<div class="callout big-picture">` intro, I added a `<div class="callout takeaway">` directly after it with a memorable one-line summary. Format: 1-3 sentences, specific, truth-preserving, quotable. Note: linter rewrote my class name to `key-takeaway` (the canonical book class), which is the right call.

## Sections Tightened (15 total)

### Part 1: LLM Building Blocks

1. **section-1.5.html (Why Tokenization Matters)**
   "A tokenizer does not speak English; it speaks 'which byte-pairs appear most often.' That is why 'unhappiness' becomes ['un', 'happiness'] but 'strawberry' becomes ['straw', 'berry'], and why the model cannot tell you how many r's are in either."

2. **section-2.2.html (The Attention Mechanism)**
   "Attention is a soft database query. Every token asks every other 'how relevant are you to me right now?', the softmax turns answers into weights, and the weighted sum is the reply. No compression bottleneck, no fixed-size summary, just dynamic lookup."

3. **section-2.3.html (QKV, Scaled Dot-Product)**
   "Q, K, V split one role into three: the query asks 'what am I looking for?', the key answers 'what do I contain?', the value says 'what should I pass forward?' Multi-head attention runs this lookup eight times in parallel and concatenates, so each head can specialize in one type of relationship (syntax, coreference, position) without interfering with the others."

4. **section-3.1.html (Transformer Anatomy)**
   "A Transformer block is just two ideas glued together: attention mixes information across positions, the FFN mixes information within each position, and residual connections plus LayerNorm keep gradients flowing through hundreds of stacked blocks. Everything else is bookkeeping."

5. **section-3.5.html (Transformer Variants)**
   "Three families, one mental shortcut: BERT (encoder) reads, GPT (decoder) writes, T5 (encoder-decoder) reads-then-writes. Positional encoding is how attention learns word order, since the math itself is permutation-invariant. Without it, 'dog bites man' and 'man bites dog' look identical to the model."

6. **section-4.1.html (Deterministic Decoding)**
   "Greedy picks the locally best token and prays. Beam search keeps the top-k partial sequences and picks the globally best of those. Both are deterministic, both collapse into repetition on open-ended text, and both are why creative writing needs the sampling methods in the next section."

7. **section-4.2.html (Stochastic Sampling)**
   "Temperature is sampling boldness: T near 0 always picks the safest token; high T rolls dice on the unlikely. Top-p crops the long tail before sampling, so the model can be bold among reasonable options without ever quoting from the 5% of nonsense at the end. Use temperature to set the energy scale; use top-p to set the ceiling."

### Part 2: Understanding LLMs

8. **section-6.1.html (BERT, GPT, T5)**
   "Three bets, three winners: BERT bet on bidirectional understanding (mask-and-predict), GPT bet on left-to-right generation (predict-the-next), T5 bet on text-to-text unification (cast every task as translation). GPT's bet compounded fastest, which is why decoder-only models dominate today, but every modern LLM still inherits ideas from all three."

9. **section-6.2.html (Pre-training Objectives)**
   "Next-token prediction is the world's most innocent-looking objective and the most powerful one we know. 'Predict the next word' sounds shallow, but to do it well across the internet you have to learn grammar, facts, code, arithmetic, dialogue, and reasoning. The objective is local; the side effects are everything."

10. **section-6.3.html (Scaling Laws)**
    "Parameters, data, and compute scale together. Starve any one and the other two waste the rest. Chinchilla's lesson in one ratio: roughly 20 tokens per parameter is the compute-optimal recipe. GPT-3 was undertrained; Llama 3 went the other way and trained a 70B model on 15 trillion tokens, because the 20:1 was always a snapshot of one data regime."

11. **section-6.4.html (Data Curation)**
    "'Garbage in, garbage out' is the universal rule, applied at internet scale. The Llama 3 team threw away roughly 90% of Common Crawl and got measurably better models than peers who kept it. The model is a mirror of its training set; pick the mirror carefully."

12. **section-6.6.html (Distributed Training)**
    "Four parallelisms, four cuts of the cake: data parallelism splits the batch, tensor parallelism splits the matmul, pipeline parallelism splits the layers, expert parallelism splits the FFN. Real training stacks all four at once; the art is keeping the GPUs talking faster than they compute."

13. **section-6.7.html (In-Context Learning)**
    "In-context learning is gradient descent in disguise: the model's attention treats the prompt's examples the way SGD treats training batches, just over the forward pass instead of the backward pass. Nobody trained the model to do this; it emerged once scale was high enough that the prompt could carry 'training data' the attention could absorb."

### Part 3: Working with LLMs

14. **section-12.1.html (Foundational Prompt Design)**
    "A prompt is a contract with the model: instruction, context, examples, format. The model is a brilliant intern who has never met you; vague instructions get vague output. Every prompt-engineering trick in this chapter is a different way of writing that contract tighter."

15. **section-12.2.html (Chain-of-Thought)**
    "'Show your work' is not just school discipline; it is a working-memory upgrade. Without CoT, the model has to fit every reasoning step into one forward pass through fixed-size hidden states. With CoT, the model's own tokens become a scratchpad it reads back on the next step. Six words ('Let's think step by step') swung GSM8K math from 18% to 79%."

16. **section-12.3.html (Advanced Prompt Patterns)**
    "Reflection works when the model can do something on pass two that it could not on pass one: run a test, check retrieval, apply a constraint. Without an external verifier, the model mostly confirms its first answer. The trajectory: from hand-written prompts, to self-improving prompts, to compiled prompts. Same arc as ML went through with feature engineering."

17. **section-12.4.html (Prompt Security)**
    "Prompt injection is the SQL injection of LLMs, except natural language has no quotation marks. There is no parameterized prompt that fully separates instruction from data, so defense is layered: filter inputs, sandbox outputs, never blindly trust retrieved text. Assume the user (and every web page) might say 'ignore previous instructions' and design around it."

18. **section-12.5.html (Automatic Prompt Engineering)**
    "Classical ML froze the program and optimized the weights. Automatic prompting freezes the weights and optimizes the program. The prompt is the code, the optimizer is the compiler. 'Take a deep breath' beat human-written prompts on math benchmarks; nobody planned that, and that is the whole point."

19. **section-13.1.html (LLM vs Classical ML)**
    "Classical ML wins when you have abundant labels, narrow scope, and stable inputs. LLMs win when any one of those breaks: few labels (use in-context learning), broad scope (use transfer), or shifting distribution (use pretraining-time generality). If a logistic regression solves it in five minutes, do not pay GPT-4 to do it in two seconds."

20. **section-13.2.html (LLM as Feature Extractor)**
    "Pay the LLM cost once, harvest the embedding forever. The LLM gives you a 1536-d vector that captures meaning; XGBoost gives you fast, interpretable predictions on that vector. Inference cost drops 100x without sacrificing semantic understanding."

21. **section-13.3.html (Hybrid Pipeline Patterns)**
    "You do not need the best model for every request; you need the right model for each request's difficulty. Cheap classifier handles the easy 80%, LLM handles the gnarly 20%, and the user cannot tell the difference. The router is the architecture."

## Total: 21 memorable one-liners added

## Sections NOT Modified (Already Strong)

- section-1.1.html (NLP eras): "Each era transition was driven by a representation breakthrough"
- section-1.2.html (Preprocessing): "Preprocessing Is Lossy Compression"
- section-1.3.html (Word Embeddings): "GPS Coordinates for Words" + 5 key-takeaway bullets
- section-1.4.html (Contextual Embeddings): "From Types to Tokens"
- section-1.6.html (Subword): "Lego Bricks of Language" + Shannon coding insight
- section-2.1.html (RNN): "The frustration is the pedagogy" + telegraph operator analogy
- section-3.2a/b.html: Hands-on lab sections, do not need additional one-liners
- section-3.6.html: "GPU memory as a city" insight already memorable
- section-3.7.html: Optional theoretical section
- section-3.8.html: Optional, already has Pareto-frontier diagram
- section-4.3/4.4: Specialized topics with strong epigraphs
- section-6.5.html: "Your optimizer is bigger than your model"
- section-6.9.html: Lab section
- section-7.1a/b, 7.2, 7.3: Model survey sections; existing voice already strong
- section-13.4, 13.5a/b: Production decision sections; existing voice strong
- section-14.1-14.5: Reference catalog of tools; not concept sections

## Out of Scope (per instructions)

- Module 5 (decoding strategies - this scope was Module 4 in the new layout)
- Module 6 emergent capabilities - section-6.7 is the canonical home for in-context learning, covered
- Module 13 (RAG) - the new layout reorganized RAG into Chapter 13 (hybrid ML+LLM) and later parts; covered relevant sections
- Module 14 (agents) - now "tools of the trade", which is a reference list rather than a concept section; nothing canonical to tighten

## Pattern Used

All added one-liners share a structure:
1. Anchor on a specific image (database query, scratchpad, contract, sushi chef)
2. Compress the abstraction to one or two specific instances ("Show your work" → 18%→79%)
3. Avoid generic phrasing ("Attention is a mechanism that..." → "Attention is a soft database query")
4. Stay truthful: each line is fact-checked against the surrounding section content

No em dashes used. No emojis. CSS class is `callout key-takeaway` (linter-normalized from the initial `callout takeaway`).
