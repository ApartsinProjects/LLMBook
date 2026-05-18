# Repeated-Content Audit

Cross-section duplication triage for the LLM textbook.

**READ-ONLY scan.** No HTML files have been modified. This report proposes
canonical homes and lists duplicates for the editor to reconcile manually.


## Methodology

- Scanned **386** main-track section HTML files under `part-*/module-*/section-*.html`.
- Excluded: `tools-of-the-trade` modules, `appendices/`, `front-matter/`, `capstone/`, `KDP/`, vendor dirs.
- For each section extracted:
  - **4,222** non-boilerplate callouts (skipped Prerequisites, Key Takeaways, etc.)
  - **1,287** code-fragment captions
  - **4,808** prose paragraphs (>= 200 chars, outside callouts/blockquotes/bibliography)

**Detection signals (this report only flags REAL duplication, not intentional structure):**

1. **Callout body fingerprint match** -- first-150-char lowercase fingerprint of the callout body
   matches across 2+ sections. (Title-only matches are skipped for structural callout titles like
   `Fun Fact`, `Big Picture`, `Real World Scenario`, `Key Insight`, `Tip: ...`, `Warning: ...`, `Note: ...`.
   Those repeat by design with unique content per section.)
2. **Code-caption exact fingerprint** -- first-80-char fingerprint match. Catches lame
   AI-boilerplate captions like "Install the required packages for this lab" or "Code example".
3. **Code-caption fuzzy match** -- >=5 shared content tokens (stopwords removed) between captions.
   Catches paraphrased boilerplate like "This snippet demonstrates this approach. Study the
   implementation details...".
4. **Prose paragraph fingerprint match** -- first-100-char fingerprint of a paragraph >= 200 chars
   matches across 2+ sections.
5. **Non-structural callout title match** -- a callout title that is NOT one of the recurring
   structural patterns appears in 2+ sections.

**Canonical home assignment** combines topic heuristics (RAG -> Part VII module 32, 
Transformers -> Part I module 3, etc.) with a fallback to the lowest-numbered part containing
the duplicated content.

## Headline Numbers

- **2** callout-body fingerprint duplications (same body text in 2+ sections).
- **7** non-structural callout-title duplications.
- **7** code-caption exact fingerprint duplications.
- **0** code-caption long-fingerprint duplications.
- **87** code-caption fuzzy (>=5 shared tokens) duplications.
- **4** prose-paragraph duplications.

## Estimated Reduction if All Duplicates Reconciled

- Callout-body duplicates: **3** excess blocks (~144 words)
- Non-structural callout-title duplicates: **10** excess blocks (~331 words)
- Code-caption (exact) duplicates: **29** excess captions (~493 words)
- Code-caption (long fingerprint) duplicates: **0** excess captions (~0 words)
- Code-caption (fuzzy) duplicates: **133** excess captions (~5,162 words)
- Prose-paragraph duplicates: **4** excess paragraphs (~189 words)
- **Grand total: ~179 duplicate blocks, ~6,321 words.**

Note: most code-caption duplicates are short generic AI-boilerplate ("Install the required
packages for this lab"). The word count is small per occurrence; the value of fixing them is
clarity and avoiding the appearance of copy-paste, not word reduction.

## Top 20 Duplication Clusters

Each cluster lists: type, canonical home (proposed), and duplicate locations.

**Suggested actions:**
- **DELETE** = remove duplicate copies, replace with `<div class="callout cross-ref">` See-Also pointer to the canonical
- **REWRITE** = the duplicate is lame boilerplate; rewrite with section-specific content
- **RESTRUCTURE** = duplicates overlap but are not identical; decide canonical, consolidate the rest into cross-refs
- **KEEP** = brief restatement is intentional for self-containment (rarely chosen)

### 1. CODE CAPTION (fuzzy >=5 shared tokens)  |  8 sections, 9 occurrences
- **Signature**: `against based cache cached call cosine`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`
- **Occurrences:**
  - `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html:416` [Code Fragment 63.1.5]
    > A semantic cache that uses embedding similarity to match incoming queries against cached responses. When the cosine similarity exceeds the threshold (0.95), the cached response is returned without mak
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:426` [Code Fragment 10.1.5]
    > Embedding generation for converting text into dense vector representations. These vectors capture semantic meaning, enabling similarity search and clustering.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:71` [Code Fragment 10.3.2]
    > Embedding generation for converting text into dense vector representations. These vectors capture semantic meaning, enabling similarity search and clustering.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:519` [Code Fragment 10.3.6]
    > Embedding generation for converting text into dense vector representations. These vectors capture semantic meaning, enabling similarity search and clustering.
  - `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html:126` [Code Fragment 13.2.4]
    > Semantic cache implementation using cosine similarity for cache lookup. The SemanticCache.get_or_generate() method embeds incoming queries, compares against stored vectors at a configurable threshold 
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4.html:420` [Code Fragment 31.4.4]
    > Semantic chunking based on embedding similarity
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:320` [Code Fragment 32.1.2]  *(canonical)*
    > Batch-embedding chunks through the OpenAI text-embedding-3-small endpoint (respecting the 2048-text-per-call limit) and persisting them in a ChromaDB collection configured for cosine similarity. The m
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html:243` [Code Fragment 42.9.3]
    > Hierarchical tracing for a RAG pipeline. Each step (embedding, vector search, reranking, generation) is a child span under the parent rag.pipeline span. The traced_chat_completion function from Code F
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.7.html:184` [Code Fragment 44.7.1]
    > A nightly Braintrust scoring job for a production agent. The wrap_openai() call at app startup captures every LLM call without code changes; the nightly cron rescores the captured traces against your 
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 2. CODE CAPTION (fuzzy >=5 shared tokens)  |  8 sections, 8 occurrences
- **Signature**: `debugging extending similar systems through`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html:281` [Code Fragment 1.2.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:268` [Code Fragment 1.7.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html:484` [Code Fragment 3.3.3]
    > This snippet demonstrates the diff_attention function using attention computation. Notice how the attention weights are computed and applied to the value vectors. Tracing through each step builds the 
  - `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:402` [Code Fragment 26.1.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:272` [Code Fragment 32.1.1]  *(canonical)*
    > This snippet demonstrates the chunk_by_tokens, chunk_by_structure functions using chunking. Notice how the chunking strategy balances granularity with context preservation. Tracing through each step b
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html:199` [Code Fragment 32.3.2]
    > Extracting database schema context (table names, columns, types) and formatting it as a prompt section so the LLM can write accurate SQL. The function encapsulates reusable logic that can be applied a
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html:413` [Code Fragment 35.1.4]
    > This snippet demonstrates the rerank_results function using retrieval, API calls. Notice how the retrieval step filters candidates before passing them to downstream processing. Tracing through each st
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.6.html:168` [Code Fragment 42.6.1]
    > This snippet demonstrates the rag_pipeline, retrieve_documents functions using retrieval, vector search. Notice how the retrieval and generation stages are composed into a single pipeline. Tracing thr
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 3. CODE CAPTION (exact fingerprint)  |  5 sections, 5 occurrences
- **Signature**: `install the required packages for this lab.`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html:519` [Code Fragment 1.4.7]  *(canonical)*
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:775` [Code Fragment 1.7.15]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html:735` [Code Fragment 2.3.14]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:327` [Code Fragment 3.5.5]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:454` [Code Fragment 4.4.9]
    > Install the required packages for this lab.
- **Suggested action**: **REWRITE**: short generic caption ("Code example", "Install the required packages for this lab") repeated verbatim. Replace each with a section-specific one-line description of what the code actually does.

### 4. CODE CAPTION (exact fingerprint)  |  5 sections, 7 occurrences
- **Signature**: `code example`
- **Canonical home (proposed)**: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`
- **Occurrences:**
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html:805` [Code Fragment 31.1.8]  *(canonical)*
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:825` [Code Fragment 32.1.7]
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:978` [Code Fragment 32.1.11]
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:307` [Code Fragment 35.5.2]
    > Code example
  - `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html:406` [Code Fragment 35.5.3]
    > Code example
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html:453` [Code Fragment 40.1.9]
    > Code example
  - `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html:333` [Code Fragment 42.1.2]
    > Code example
- **Suggested action**: **REWRITE**: short generic caption ("Code example", "Install the required packages for this lab") repeated verbatim. Replace each with a section-specific one-line description of what the code actually does.

### 5. CALLOUT BODY (fingerprint match)  |  3 sections, 3 occurrences
- **Signature**: `in production, prefer langchain_text_splitters.recursivecharactertextsplitter(chunk_size=512, chunk_overlap=64) instead of a hand-rolled win`
- **Canonical home (proposed)**: `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html`
- **Occurrences:**
  - `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html:221` ["Library Shortcut: RecursiveCharacterTextSplitter"]  *(canonical)*
    > In production, prefer langchain_text_splitters.RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64) instead of a hand-rolled window loop. It handles paragraph and sentence boundaries, fall
  - `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4.html:206` ["Library Shortcut: RecursiveCharacterTextSplitter"]
    > In production, prefer langchain_text_splitters.RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64) instead of a hand-rolled window loop. It handles paragraph and sentence boundaries, fall
  - `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html:275` ["Library Shortcut: RecursiveCharacterTextSplitter"]
    > In production, prefer langchain_text_splitters.RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64) instead of a hand-rolled window loop. It handles paragraph and sentence boundaries, fall
- **Suggested action**: **DELETE** duplicate callouts in non-canonical sections; replace with `<div class="callout cross-ref">` See-Also. Body fingerprints are identical -- this is copy-paste prone to drift.

### 6. CODE CAPTION (exact fingerprint)  |  4 sections, 10 occurrences
- **Signature**: `tokenization pipeline converting raw text into model-ready input ids. the tokeni`
- **Canonical home (proposed)**: `part-2-understanding-llms/module-10-interpretability/section-10.1.html`
- **Occurrences:**
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:491` [Code Fragment 10.1.6]  *(canonical)*
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:145` [Code Fragment 10.2.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:227` [Code Fragment 10.3.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:273` [Code Fragment 10.3.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:414` [Code Fragment 10.3.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:86` [Code Fragment 10.4.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:246` [Code Fragment 10.4.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:333` [Code Fragment 10.4.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:397` [Code Fragment 10.4.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:492` [Code Fragment 10.4.6]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
- **Suggested action**: **REWRITE**: short generic caption ("Code example", "Install the required packages for this lab") repeated verbatim. Replace each with a section-specific one-line description of what the code actually does.

### 7. CODE CAPTION (fuzzy >=5 shared tokens)  |  5 sections, 5 occurrences
- **Signature**: `install lab packages required`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html:519` [Code Fragment 1.4.7]  *(canonical)*
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:775` [Code Fragment 1.7.15]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html:735` [Code Fragment 2.3.14]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:327` [Code Fragment 3.5.5]
    > Install the required packages for this lab.
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:454` [Code Fragment 4.4.9]
    > Install the required packages for this lab.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 8. CODE CAPTION (fuzzy >=5 shared tokens)  |  4 sections, 10 occurrences
- **Signature**: `automatically converting handles ids padding pipeline`
- **Canonical home (proposed)**: `part-2-understanding-llms/module-10-interpretability/section-10.1.html`
- **Occurrences:**
  - `part-2-understanding-llms/module-10-interpretability/section-10.1.html:491` [Code Fragment 10.1.6]  *(canonical)*
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.2.html:145` [Code Fragment 10.2.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:227` [Code Fragment 10.3.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:273` [Code Fragment 10.3.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.3.html:414` [Code Fragment 10.3.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:86` [Code Fragment 10.4.1]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:246` [Code Fragment 10.4.3]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:333` [Code Fragment 10.4.4]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:397` [Code Fragment 10.4.5]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
  - `part-2-understanding-llms/module-10-interpretability/section-10.4.html:492` [Code Fragment 10.4.6]
    > Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 9. CALLOUT BODY (fingerprint match)  |  2 sections, 2 occurrences
- **Signature**: `your eval set has a half-life. an eval suite that is not refreshed with production samples becomes stale within weeks. schedule a recurring `
- **Canonical home (proposed)**: `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html`
- **Occurrences:**
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html:62` ["Key Insight"]
    > Your eval set has a half-life. An eval suite that is not refreshed with production samples becomes stale within weeks. Schedule a recurring task (weekly for high-traffic products, monthly for lower-tr
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html:60` ["Key Insight"]  *(canonical)*
    > Your eval set has a half-life. An eval suite that is not refreshed with production samples becomes stale within weeks. Schedule a recurring task (weekly for high-traffic products, monthly for lower-tr
- **Suggested action**: **DELETE** the duplicate callout; promote one location to canonical and cross-ref from the other.

### 10. CODE CAPTION (fuzzy >=5 shared tokens)  |  4 sections, 4 occurrences
- **Signature**: `agent`
- **Canonical home (proposed)**: `part-6-agentic-ai/module-28-multi-agent-systems/section-28.3.html`
- **Occurrences:**
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.1.html:137` [Code Fragment 49.1.1]
    > This snippet defines a SecureAgentExecutor that wraps an agent with a policy engine, validating each proposed tool call against allowed actions and parameter constraints before execution. The execute 
  - `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.3.html:313` [Code Fragment 49.3.3]
    > A tau-bench style policy adherence evaluator. The policy is expressed as a list of rules with conditions, required actions, and prohibited actions. The scorer checks each applicable rule against the a
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.3.html:131` [Code Fragment 28.3.1]  *(canonical)*
    > This snippet builds a human-in-the-loop multi-agent workflow using LangGraph with SqliteSaver checkpointing and an interrupt_before parameter on sensitive nodes. The approval_gate node pauses executio
  - `part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html:184` [Code Fragment 28.4.3]
    > A Pydantic-based starter contract. The WeatherQuery schema declares required ( city ) and optional ( units ) fields with allowed values; students fill in call_agent and validate_tool_call so that any 
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 11. CODE CAPTION (fuzzy >=5 shared tokens)  |  4 sections, 4 occurrences
- **Signature**: `audio cloning condition cross different diffusion`
- **Canonical home (proposed)**: `part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html`
- **Occurrences:**
  - `part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html:148` [Code Fragment 20.1.2]  *(canonical)*
    > Zero-shot voice cloning with F5-TTS. The reference audio plus its transcript condition the flow-matching DiT; nfe_step trades quality for latency in the same way num_inference_steps does in Stable Dif
  - `part-5-multimodal-llms/module-20-audio-music-generation/section-20.6.html:154` [Code Fragment 20.6.1]
    > Minimal video DiT with rectified-flow training. The patchifier is a Conv3d with stride equal to patch size; the unpatchifier is a ConvTranspose3d. Real production systems add adaLN-Zero conditioning (
  - `part-5-multimodal-llms/module-22-vision-language-models/section-22.9.html:90` [Code Fragment 22.9.1]
    > GPT-4o Realtime API skeleton. Server-side voice-activity-detection (VAD) handles turn boundaries; the model streams audio responses back over the same WebSocket. Section 40.3 covers the full protocol 
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.5.html:94` [Code Fragment 40.5.1]
    > Moshi's inference loop. The user and model audio streams are processed in lockstep, 80 ms at a time. The model emits both audio codec tokens and text tokens; the text gives you a real-time transcript 
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 12. CODE CAPTION (exact fingerprint)  |  3 sections, 3 occurrences
- **Signature**: `this snippet demonstrates this approach. study the implementation details to und`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html:281` [Code Fragment 1.2.3]  *(canonical)*
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html:268` [Code Fragment 1.7.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
  - `part-6-agentic-ai/module-26-ai-agents/section-26.1.html:402` [Code Fragment 26.1.3]
    > This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed
- **Suggested action**: **REWRITE**: short generic caption ("Code example", "Install the required packages for this lab") repeated verbatim. Replace each with a section-specific one-line description of what the code actually does.

### 13. PROSE PARAGRAPH  |  2 sections, 2 occurrences
- **Signature**: `the solution is to treat production evaluation as a continuous pipeline, not a gate you pass once. c`
- **Canonical home (proposed)**: `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html`
- **Occurrences:**
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html:79`
    > The solution is to treat production evaluation as a continuous pipeline, not a gate you pass once. Chapter 44 covers the mechanics of building eval sets; this section focuses on keeping those evals al
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html:58`  *(canonical)*
    > The solution is to treat production evaluation as a continuous pipeline, not a gate you pass once. Chapter 42 covers the mechanics of building eval sets; the discipline added here is keeping those eva
- **Suggested action**: **DELETE** the redundant paragraph; replace with a 1-line summary plus a link to canonical.

### 14. PROSE PARAGRAPH  |  2 sections, 2 occurrences
- **Signature**: `the most effective drift detection runs automatically on a schedule, comparing recent production met`
- **Canonical home (proposed)**: `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html`
- **Occurrences:**
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html:144`
    > The most effective drift detection runs automatically on a schedule, comparing recent production metrics against baseline values established at launch (or at the last intentional recalibration). The o
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html:110`  *(canonical)*
    > The most effective drift detection runs automatically on a schedule, comparing recent production metrics against baseline values established at launch (or at the last intentional recalibration). The o
- **Suggested action**: **DELETE** the redundant paragraph; replace with a 1-line summary plus a link to canonical.

### 15. CODE CAPTION (fuzzy >=5 shared tokens)  |  3 sections, 5 occurrences
- **Signature**: `attention behavior configuration enables flag improving`
- **Canonical home (proposed)**: `part-4-training-adaptation/module-17-peft/section-17.2.html`
- **Occurrences:**
  - `part-4-training-adaptation/module-17-peft/section-17.2.html:118` [Code Fragment 17.2.2]  *(canonical)*
    > Prefix Tuning configuration that prepends learnable virtual tokens to each softmax layer. The prefix_projection flag enables a small MLP that projects the prefix, improving training stability. This ap
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:142` [Code Fragment 17.4.1]
    > Prompt Tuning with HuggingFace PEFT. The PromptTuningConfig prepends 20 learnable virtual tokens (initialized from a text string) to every input. Only these ~320 KB of soft prompt embeddings are train
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:232` [Code Fragment 17.4.2]
    > Prefix Tuning with HuggingFace PEFT. Unlike Prompt Tuning, Prefix Tuning injects learned key-value pairs into every attention layer via a reparameterization MLP ( encoder_hidden_size=512 ). After trai
  - `part-4-training-adaptation/module-17-peft/section-17.4.html:573` [Code Fragment 17.4.6]
    > The PromptedLlama wrapper holds the base model frozen and prepends a learnable (n_virtual, hidden_size) parameter to the input embeddings, with a matching attention_mask extension so the soft tokens p
  - `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.2.html:181` [Code Fragment 21.2.1]
    > Fine-tuning LayoutLMv3-Base on FUNSD. Total training time on a single RTX 4090: about 38 minutes for 15 epochs. The 0.906 F1 is within 1.5 points of the published LayoutLMv3-Large result and competiti
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 16. CODE CAPTION (fuzzy >=5 shared tokens)  |  3 sections, 5 occurrences
- **Signature**: `agent`
- **Canonical home (proposed)**: `part-6-agentic-ai/module-26-ai-agents/section-26.4.html`
- **Occurrences:**
  - `part-6-agentic-ai/module-26-ai-agents/section-26.4.html:178` [Code Fragment 26.4.2]  *(canonical)*
    > The starter code wires the lab's three moving parts: load_dataset pulls the SWE-bench Lite test split from HuggingFace, Anthropic() opens the model client, and TOOLS declares the read/write/test tool 
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html:208` [Code Fragment 29.1.2]
    > Lab step (starter code) : define JSON tool schemas for read_file, write_file, and run_command, then wire them into an agent loop that sends tool results back to the LLM on each iteration.
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html:225` [Code Fragment 29.1.4]
    > Lab step (starter code) : define 5 coding challenges (string manipulation, data structures, file parsing, API client, math) with test cases and run the agent on each.
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html:122` [Code Fragment 29.2.1]
    > This snippet builds a browser automation agent using Playwright MCP tools via the Anthropic client. The AI agent sends tool_use responses back as tool_result messages, enabling the LLM to chain action
  - `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html:223` [Code Fragment 29.2.6]
    > Lab step (starter code) : initialize a Playwright browser instance and define MCP tool schemas for navigate, click, type, and screenshot so the LLM agent can interact with web pages programmatically.
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 17. CODE CAPTION (fuzzy >=5 shared tokens)  |  3 sections, 4 occurrences
- **Signature**: `agent llm tts voice`
- **Canonical home (proposed)**: `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html`
- **Occurrences:**
  - `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.4.html:737` [Code Fragment 37.4.6.1]  *(canonical)*
    > A full STT to LLM to TTS voice agent with barge-in in 20 lines.
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html:251` [Code Fragment 40.1.2]
    > A LiveKit Agents voice agent with tool calling. The @function_tool decorator exposes methods as callable tools that the LLM can invoke during conversation. LiveKit handles the real-time audio transpor
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html:334` [Code Fragment 40.1.3]
    > Latency-optimized voice agent with overlapping pipeline stages. STT streams partial transcripts while the user speaks. For tool calls, filler speech plays in parallel with tool execution. LLM tokens s
  - `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.5.html:125` [Code Fragment 40.5.2]
    > Pipecat voice agent in 40 lines. The framework handles backpressure (slow TTS causes upstream to pause), interruption (configurable via the transport), and metrics emission. Add an LLM tool-call adapt
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 18. PROSE PARAGRAPH  |  2 sections, 2 occurrences
- **Signature**: `the key discipline is proportionality: do not redesign your architecture when a prompt tweak would s`
- **Canonical home (proposed)**: `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html`
- **Occurrences:**
  - `part-14-designing-llm-agent-products/module-70-shipping-products/section-70.4.html:238`
    > The key discipline is proportionality: do not redesign your architecture when a prompt tweak would suffice, and do not keep tweaking prompts when the architecture is the bottleneck. Your monitoring da
  - `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html:192`  *(canonical)*
    > The key discipline is proportionality: do not redesign your architecture when a prompt tweak would suffice, and do not keep tweaking prompts when the architecture is the bottleneck. Your monitoring da
- **Suggested action**: **DELETE** the redundant paragraph; replace with a 1-line summary plus a link to canonical.

### 19. CODE CAPTION (fuzzy >=5 shared tokens)  |  3 sections, 3 occurrences
- **Signature**: `layer network position token wise`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html:428` [Code Fragment 4.1.5]  *(canonical)*
    > a: A position-wise feed-forward network with GELU activation. Each token passes through the same two-layer MLP independently.
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html:295` [Code Fragment 3.2.3]
    > Position-wise feed-forward network with ReLU activation. This two-layer MLP is applied independently to each token position.
  - `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html:352` [Code Fragment 3.5.1]
    > Layer normalization and a position-wise feedforward network implemented from scratch. Layer norm recenters each token's features to zero mean and unit variance, stabilizing gradients, while the feedfo
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

### 20. CODE CAPTION (fuzzy >=5 shared tokens)  |  3 sections, 3 occurrences
- **Signature**: `decoding greedy highest probability token`
- **Canonical home (proposed)**: `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html`
- **Occurrences:**
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html:136` [Code Fragment 4.1.7]  *(canonical)*
    > The following function implements greedy decoding by repeatedly selecting the highest-probability token at each step.
  - `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.4.html:487` [Code Fragment 4.4.4]
    > Loading GPT-2 and implementing greedy decoding from scratch. The loop repeatedly selects the highest-probability next token, producing deterministic but often repetitive output that serves as the base
  - `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html:566` [Code Fragment 8.6.7]
    > Manual greedy decoding with GPT-2, selecting the highest-probability token at each step. The output illustrates greedy decoding's core weakness: deterministic selection leads to repetitive loops becau
- **Suggested action**: **RESTRUCTURE**: similar Code Fragments cover overlapping ground. Decide whether each is doing distinct didactic work; if not, consolidate to canonical and replace others with a 1-line See-Also pointer.

## Sample Before/After Sketches (5)

### Sketch 1: `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html` (cluster type: code_caption_fuzzy)

**Cluster signature**: `against based cache cached call cosine`

**Before** (duplicate content):
```html
<div class="code-caption"><strong>Code Fragment 63.1.5</strong>: A semantic cache that uses embedding similarity to match incoming queries against cached responses. When the cosine similarity exceeds the threshold (0.95), the cached response is returned without mak</div>
```

**After** (replace with cross-ref to canonical `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html">section-32.1</a>.
    The treatment there covers the full depth; the brief mention previously
    here has been removed to avoid drift.</p>
</div>
```

### Sketch 2: `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.2.html` (cluster type: code_caption_fuzzy)

**Cluster signature**: `debugging extending similar systems through`

**Before** (duplicate content):
```html
<div class="code-caption"><strong>Code Fragment 1.2.3</strong>: This snippet demonstrates this approach. Study the implementation details to understand how each component contributes to the overall computation. Tracing through each step builds the intuition needed</div>
```

**After** (replace with cross-ref to canonical `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html">section-32.1</a>.
    The treatment there covers the full depth; the brief mention previously
    here has been removed to avoid drift.</p>
</div>
```

### Sketch 3: `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html` (cluster type: code_caption_exact)

**Cluster signature**: `install the required packages for this lab.`

**Before** (duplicate content):
```html
<div class="code-caption"><strong>Code Fragment 1.7.15</strong>: Install the required packages for this lab.</div>
```

**After** (replace with cross-ref to canonical `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html`):
```html
<div class="code-caption"><strong>Code Fragment 1.7.15</strong>:
  (rewrite this caption with section-specific content explaining what THIS code does.)
</div>
```

### Sketch 4: `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html` (cluster type: code_caption_exact)

**Cluster signature**: `code example`

**Before** (duplicate content):
```html
<div class="code-caption"><strong>Code Fragment 32.1.7</strong>: Code example</div>
```

**After** (replace with cross-ref to canonical `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`):
```html
<div class="code-caption"><strong>Code Fragment 32.1.7</strong>:
  (rewrite this caption with section-specific content explaining what THIS code does.)
</div>
```

### Sketch 5: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.4.html` (cluster type: callout_body)

**Cluster signature**: `in production, prefer langchain_text_splitters.recursivecharactertextsplitter(chunk_size=512, chunk_overlap=64) instead `

**Before** (duplicate content):
```html
<div class="callout big-picture">
  <div class="callout-title">Library Shortcut: RecursiveCharacterTextSplitter</div>
  <p>In production, prefer langchain_text_splitters.RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64) instead of a hand-rolled window loop. It handles paragraph and sentence boundaries, falls back through a list of separators, and</p>
</div>
```

**After** (replace with cross-ref to canonical `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html`):
```html
<div class="callout cross-ref">
  <div class="callout-title">See Also</div>
  <p>This concept is treated in depth in 
    <a href="../../part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html">section-16.7</a>.
    The treatment there covers the full depth; the brief mention previously
    here has been removed to avoid drift.</p>
</div>
```

## Top-5 Most-Egregious Clusters (one-liners)

1. **Code-caption fuzzy >=5 shared tokens** -- across **8** sections, **9** occurrences. Example: "A semantic cache that uses embedding similarity to match incoming queries agains..."
2. **Code-caption fuzzy >=5 shared tokens** -- across **8** sections, **8** occurrences. Example: "This snippet demonstrates this approach. Study the implementation details to und..."
3. **Code-caption exact fingerprint** -- across **5** sections, **5** occurrences. Example: "Install the required packages for this lab...."
4. **Code-caption exact fingerprint** -- across **5** sections, **7** occurrences. Example: "Code example..."
5. **Callout-body fingerprint match** -- across **3** sections, **3** occurrences. Example: "In production, prefer langchain_text_splitters.RecursiveCharacterTextSplitter(ch..."
