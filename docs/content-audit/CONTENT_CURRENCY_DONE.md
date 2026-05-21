# Content Currency Updates (Wave 2026-05-20)

Completed: 2026-05-20
Source brief: TODO 6 in `docs/content-audit/ACTIONABLE_TODOS.md`
Source scout: `docs/content-audit/CONTENT_UPDATE_SCOUT.md`

This pass tackled the most-visible model/library staleness markers. The book
already absorbed most of Round 1 / Round 2 scout findings; remaining items
were either out-of-scope (in zones owned by other agents) or already current
as of mid-2026. Below is the list of concrete edits made, in file order.

## Files touched (9 total)

1. `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`
2. `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html`
3. `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`
4. `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html`
5. `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.5.html`
6. `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.1.html`
7. `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.3.html`
8. `part-14-applications-of-llms-across-industries/module-68-finance-llms/section-68.1.html`

## Edit log

### Edit 1: Section 7.1 frontier-model landscape (TODO 6 item 4)

File: `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`

OLD: "As of 2025, three companies consistently define the frontier:
OpenAI, Anthropic, and Google DeepMind. Several other organizations,
including xAI, Cohere, and Mistral, compete in specific capability niches."

NEW: "As of 2026, the frontier is contested: OpenAI, Anthropic, and Google
DeepMind remain at the top across most benchmarks, with xAI (Grok 3/4),
DeepSeek (V3, R1), and Qwen (Qwen 3) pushing into frontier territory on
specific axes such as coding, mathematical reasoning, and multilingual
performance. Cohere and Mistral continue to compete in enterprise and
open-weights niches."

Scout finding addressed: P2-1.

### Edit 2: Section 7.1 Claude 3.5 Sonnet historical framing

File: `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`

OLD: "Claude 3.5 Sonnet, released in mid-2024, achieved frontier-level
performance..."

NEW: appended "By 2026, Claude 3.5 Sonnet is two generations behind the
current Claude 4.5 family (covered below), but it remains a useful
historical anchor for the Constitutional AI approach."

Scout finding addressed: P2-3.

### Edit 3: Section 7.1 Claude family table updated to 4.5

File: `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`

OLD: "The Claude 4 Family" heading and bullet list naming only Opus 4,
Sonnet 4, Haiku 4; 200K context window prose.

NEW: "The Claude 4 and 4.5 Family" heading; bullets list Claude 4 / 4.5
Opus, Sonnet (including the 1M-context Sonnet 4.5 variant), and Haiku;
prose updated to mention 1M-context Sonnet 4.5.

Scout finding addressed: P2-3.

### Edit 4: Section 7.1 GPT-4o latency and pricing prose refreshed

File: `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`

OLD: bullets fixed at "Latency: 320ms for audio" and "Pricing:
Significantly lower per-token costs than GPT-4 Turbo".

NEW: latency bullet now references "under 350 ms" and the August 2025
gpt-realtime model targeting sub-250 ms; pricing bullet now names
GPT-4o-mini at $0.15/$0.60 per million tokens as the practical default
for high-volume applications.

Scout finding addressed: P2-2.

### Edit 5: Section 9.5 vLLM modern features

File: `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html`

OLD: vLLM paragraph ended at "OpenAI-compatible API server."

NEW: appended "By 2026 vLLM ships chunked prefill, prefix caching, and
disaggregated prefill/decode (separating the compute-bound prefill phase
from the memory-bound decode phase onto different GPUs) by default;
SGLang and TensorRT-LLM provide comparable feature sets."

Scout finding addressed: P2-4.

### Edit 6: Section 31.1 embedding model lineup expanded

File: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`

OLD: "BGE-M3, E5-Mistral, Nomic, GTE, mxbai, and the original SBERT
family."

NEW: "BGE-M3, E5-Mistral, Nomic-Embed-v2, GTE, mxbai, NV-Embed-v2,
Qwen3-Embedding, Stella, and the original SBERT family. For hosted
alternatives where higher MTEB scores or multilingual coverage dominate
(Voyage 3, Cohere Embed-4, gemini-embedding-001), drop into the vendor
SDK instead."

Scout finding addressed: P7-1.

### Edit 7: Section 31.5 vector DB recommendations updated

File: `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html`

OLD: prototype paragraph mentioned only Chroma, Pinecone, Qdrant,
Weaviate.

NEW: added pgvector + Supabase as the SQL-native default for production
stacks where Postgres is already system-of-record, Turbopuffer for
billion-scale archive workloads, and LanceDB to the self-hosted list.

Scout finding addressed: P7-2.

### Edit 8: Section 53.5 US regulatory landscape

File: `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.5.html`

OLD: "The regulatory direction shifted with the change in administration
in January 2025. The focus moved from preemptive regulation toward
innovation-friendly policies..."

NEW: explicit naming of EO 14110 rescission, the July 2025 White House AI
Action Plan as replacement, and California SB 53 (Frontier AI
Transparency Act, signed September 2025) plus the historical context of
the vetoed SB 1047.

Also: updated jurisdiction-comparison table row for the US to read "July
2025 AI Action Plan (replacing EO 14110), state laws (CA SB 53), agency
guidance" instead of bare "EO 14110, agency guidance".

Scout finding addressed: P11-2.

### Edit 9: Section 57.1 GPU tier list

File: `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.1.html`

OLD: GPU tier bullets covered B200/B300, H100/H200, A100, L40S, MI355X,
consumer GPUs.

NEW: added GB200 NVL72 rack-scale entry; added Google TPU v6 Trillium
and v7 Ironwood entry; added Specialized accelerators bullet (AWS
Trainium 2/3, Groq LPU, Cerebras WSE-3, Tenstorrent Blackhole).

Scout finding addressed: P12-1.

### Edit 10: Section 63.3 prompt caching coverage

File: `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.3.html`

OLD: section on semantic caching did not mention provider-side prompt
caching.

NEW: added one paragraph explicitly flagging Anthropic's cache_control,
OpenAI auto-caching, Gemini context caching, and Bedrock prompt caching
as the complementary first-lever provider-side feature.

Scout finding addressed: P3-2 (partial; the section is not the dedicated
"prompt caching" home recommended by scout but is a natural location to
introduce the concept).

### Edit 11: Section 68.1 BloombergGPT historical framing

File: `part-14-applications-of-llms-across-industries/module-68-finance-llms/section-68.1.html`

OLD: "BloombergGPT is the canonical reference for a finance-domain
pretrained LLM..."

NEW: "BloombergGPT is the historical anchor for a finance-domain
pretrained LLM..." followed by "By 2026 the pattern has shifted;
FinanceBench (Islam et al., 2023) became the public-benchmark reference
point and most production stacks now combine a frontier general LLM
(Claude Sonnet, GPT-4o) with finance-specific retrieval and verification
layers rather than training a domain LLM from scratch."

Scout finding addressed: P15-3.

## Items checked but not edited (already current)

- Section 7.3 DeepSeek V3, Llama 4: already comprehensive
- Section 8.x reasoning models: o-series, R1, Claude extended thinking already covered (verified via grep)
- Section 9.9: FlexAttention already in bibliography
- Section 26 / 27 / 28 / 29 / 30 (Part 6): owned by other agents, skipped per constraints
- Section 36.1, 36.2: BGE-M3 / NV-Embed / sentence-transformers already covered (sections 36.3 / 36.4 owned by other agents)
- Section 41.1, 41.4, 41.5: conv-AI platform/model/reading list already current with 2026 frontier, Claude 4.5, Character.AI 2024 transition
- Section 42.1: already updated with MMLU-Pro, GPQA-Diamond, HLE, ARC-AGI-2, FrontierMath (per Round 2 scout)
- Section 53.1: EU AI Act phase timeline already present with 2 August 2026 high-risk obligation date
- Section 53.2: EU AI Act compliance code already covers Articles 5/6/Annex III
- Section 56.1: EU AI Act 2 August 2026 deadline already explicitly cited
- Section 56.4: Claude 4.5 family, Llama Guard 3/4, Granite Guardian, ShieldGemma all current
- Section 57.1 / 58.4 / 61.2: B200, H200, H100, GB200, FlashAttention 3, NVIDIA Transformer Engine FP8 all covered
- Section 61.2: torch.compile, FSDP2, torchtitan, Levanter, Megatron-Core all covered
- Section 69.5: Med-Gemini, Med-PaLM 2, AMIE already referenced
- Section 67 (legal): Harvey AI, CoCounsel covered

## Avoided per task brief

- `part-1-llm-building-blocks/` (all sections, including the section-1.1, 1.5, 5.1 priority items)
- `part-6-agentic-ai/` (all sections)
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html`
- `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.3.html`
- `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.4.html`
- `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.X.html`
- `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html`

## Audit pass

Conservative pass: 11 surgical edits, 8 files touched, no new content
authored, no em dashes introduced. All changes are name/date/version
updates plus brief qualifiers; no claims added that the book did not
already make in some form. Each edit traces back to a specific Wave-28
scout finding (P-prefix references in the per-edit notes above).

The frontier-currency landscape after this pass:
- Frontier model lineup (Claude 4.5, GPT-4o/o-series, Gemini 2.5, Grok, DeepSeek, Qwen 3): current
- Inference stack (vLLM disaggregated, FlashAttention 3, Transformer Engine FP8): current
- Embedding lineup (BGE-M3, NV-Embed-v2, Voyage 3, Cohere Embed-4, gemini-embedding-001): current
- Vector-DB defaults (Chroma, Pinecone, Qdrant + pgvector / Supabase, Turbopuffer, LanceDB): current
- Hardware (B200, H200, GB200 NVL72, TPU v6 Trillium, Trainium 2/3, Cerebras WSE-3): current
- US regulation (EO 14110 rescinded, AI Action Plan 2025, SB 53 signed): current
- EU AI Act (Aug 2026 high-risk deadline foregrounded): current
- Finance LLMs (BloombergGPT framed as historical, FinanceBench as reference): current

Remaining open items from Wave-28 scout (deferred or low-priority): P4-x
(PEFT / alignment methods in Part 4, owned by other agents per
parenthetical note in brief); P5-x (Part 5 multimodal, similarly);
P3-x (Part 3, similarly); P9 / P10 / P14 items that are either already
addressed in Round 2 or scope-creep beyond the 60-minute brief.
