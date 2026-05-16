# Framework Guides Duplication Audit (post-v9)

Scope: appendices C (HuggingFace), D (LangChain), E (Orchestration Frameworks), F (Agent Frameworks), G (Problem-Solution Key).
Method: read every section, cross-checked against body chapters (parts 1-12). "Body" = main chapter text; "Appendix" = framework guides under audit.

## Summary

- Total duplication candidates: 14
- Strong duplications (D vs E): 5 (the single E.1 section overlaps four times with D, plus one cross-overlap with F's LangGraph framing)
- Body backref opportunities: 11 (most live in C and D; concept paragraphs that already exist in chapters 23/26/14/20)
- Theory-to-body moves: 3 (DSPy compilation/signatures, agent architecture taxonomy, prompt-vs-program framing)
- Structural problems found:
  - E has only ONE section (`section-e.1.html`) despite the index advertising three. The "P.2" content covers four frameworks in one page and is largely a comparison essay, not API reference.
  - F is similarly a single section (`section-f.1.html`) that is mostly a taxonomy + decision table.
  - C still self-identifies internally as "Appendix D" / "Section D.1-D.5" in headers (`<h1>J.1 ...</h1>`, "Section D.1" page-current). D internally identifies as "Section K". These are stale renumber artifacts but flagged here because they affect cross-ref accuracy.
  - C.0 opener references `Appendix K (LangChain)` which is now Appendix D, plus prerequisites that point to legacy chapter numbers (Chapter 04, 18, 20). Fix in a separate pass.

## Appendix C: HuggingFace

### Section C.1: Transformers Library: Models, Pipelines, AutoClasses
- Topic: `pipeline()`, AutoClasses, encoder/decoder/encoder-decoder families, `from_pretrained`, precision/quantization, `.generate()` decoding strategies.
- Body coverage:
  - Encoder/decoder family taxonomy and the why-behind it are in Chapter 4 (Transformer Architecture) and Part 2.
  - Decoding strategies (greedy/top-k/top-p/beam) are body content for Chapter 5 (Decoding & Text Generation) and section 14.5 (prompt engineering touches sampling).
- Verdict: KEEP for API recipes (`pipeline()`, `AutoModelFor*`, `device_map="auto"`, `load_in_4bit`). DUPLICATE OF BODY for the 3-paragraph encoder/decoder family explanation and the 2-paragraph decoding-strategy explanation.
- Action:
  - Keep code fragments k.1.1-k.1.6 unchanged.
  - In section "3. Model Architectures" (3 paragraphs starting "Encoder-only models..."), replace prose explanations with: "See Chapter 4 (Transformer Architecture) for why each family exists. When picking an AutoClass: encoder-only -> `AutoModel*`/`AutoModelForSequenceClassification`; decoder-only -> `AutoModelForCausalLM`; encoder-decoder -> `AutoModelForSeq2SeqLM`." Keep the code that shows loading one of each.
  - In section "6. Inference Patterns and Generation Strategies", remove the 1-paragraph teaching about greedy/top-k/top-p; replace with backref to Chapter 5 decoding sections. Keep code fragment k.1.6 (the API recipe).

### Section C.2: Datasets and Tokenizers
- Topic: `load_dataset()`, streaming, `.map()/.filter()`, training a BPE tokenizer with `tokenizers`, preprocessing for classification/NER/QA.
- Body coverage: Tokenization theory and BPE algorithm covered in Chapter 2 (Tokenization). NER subword alignment (`-100` label trick) is a HuggingFace-specific gotcha not covered in the body and should stay.
- Verdict: KEEP. This is the cleanest framework-reference section in C. Only the 3-sentence intro to "Fast Tokenizers" trips into theory (Rust backing, 10-100x speedup). That phrase belongs in body chapter 2 or in Appendix B.
- Action: Light. Add a backref before the BPE training example: "For BPE algorithm theory, see Chapter 2.X (Tokenization)." No content removal.

### Section C.3: Training with Trainer and Accelerate
- Topic: `TrainingArguments`, `Trainer`, callbacks, custom Accelerate loop, DDP / FSDP / DeepSpeed ZeRO.
- Body coverage:
  - Chapter 18 (Fine-Tuning Fundamentals) - already linked from C.3 opener. Good.
  - Distributed training strategies (DDP vs FSDP vs ZeRO-2/3) are body theory and should appear in Chapter 18 or Appendix M (Distributed ML). The Figure C.3.2 table compresses what is genuinely chapter-length theory into one row each.
- Verdict: KEEP code; MOVE the distributed-strategy taxonomy (figure C.3.2 + paragraph 1 of section 5) to Appendix M or Chapter 18 with a backref.
- Action:
  - Keep all `TrainingArguments` and `Trainer` code unchanged - this is canonical API reference.
  - In section "5. Distributed Training and Multi-GPU Strategies", trim the opening paragraph to: "See Appendix M (Distributed ML) or Chapter 18 for DDP / FSDP / ZeRO theory. The HuggingFace integration is below."
  - Move Figure C.3.2 (Strategy / Model Size / What Is Distributed / When to Use) to Appendix M; keep the CLI launch examples (Code Fragment k.3.5, k.3.6).

### Section C.4: PEFT and TRL
- Topic: LoRA, QLoRA, SFTTrainer, DPOTrainer, RewardTrainer, PPOTrainer, adapter save/load/merge.
- Body coverage:
  - LoRA / QLoRA math (the `W + BA` decomposition) is body theory, covered by Chapter 19 (PEFT). The first paragraph of C.4 section 1 explains this in 2 sentences with LaTeX - it duplicates Chapter 19.
  - DPO theory ("Bradley-Terry preference model", KL penalty) is body content for Chapter 20 (Alignment, RLHF, DPO).
  - PPO loop conceptual description duplicates Chapter 20.
  - The "DPO vs. PPO: Practical Considerations" callout is solid practitioner advice that doesn't appear in Chapter 20 - this is valuable framework-reference content and should stay.
- Verdict: KEEP code unchanged. DUPLICATE OF BODY for the math paragraphs in sections 1, 2, 4, 5.
- Action:
  - Section 1 LoRA: trim 2-sentence math intro; replace with "See Chapter 19 for LoRA derivation. To apply LoRA via `peft`:" then keep code.
  - Section 2 QLoRA: keep the NF4/4-bit/double-quantization gotcha paragraph (this is `bitsandbytes`-specific framework reference). Trim the 1-sentence "QLoRA combines 4-bit quantization with LoRA" prefix; replace with backref to Chapter 19.4 if it exists, otherwise leave (theory may belong in body).
  - Section 4 DPO: trim the Bradley-Terry paragraph; backref Chapter 20.
  - Section 5 PPO: trim the "first train a reward model, then PPO" 2-sentence concept; backref Chapter 20.
  - KEEP the practical "DPO vs PPO" warning callout.

### Section C.5: HuggingFace Hub
- Topic: `huggingface_hub` API, `push_to_hub`, model cards, repo management, gated models, Spaces.
- Body coverage: None. The Hub is an external platform; this is pure platform reference. Some content overlaps Appendix K (Experiment Tracking - W&B/MLflow) for "model lifecycle" framing but that overlap is fine.
- Verdict: KEEP entirely. This section is the model of what a framework guide should look like.
- Action: None.

## Appendix D: LangChain

### Section D.1: Core Abstractions (Models, Prompts, Chains, LCEL)
- Topic: Chat models, `PromptTemplate`/`ChatPromptTemplate`, deprecated `LLMChain`, LCEL pipe operator, `RunnablePassthrough`/`RunnableParallel`, `configurable_fields`.
- Body coverage:
  - Chapter 13 (LLM APIs) covers provider SDKs and message format.
  - Chapter 14.1 (Foundational Prompt Design) covers prompt templates, variable injection, system messages - section 12.1.5 is literally "Prompt Templates and Variable Injection."
  - The 1-paragraph intro to D.1 section 2 ("Hard-coding prompt strings into application code leads to maintenance headaches") duplicates a Chapter 14 motivation.
- Verdict: KEEP API mechanics; DUPLICATE OF BODY for the prompt-template motivation, the streaming/batch motivation ("real-time user-facing applications"), and the deprecation discussion of `LLMChain` (which is purely historical and should be a sidebar, not 28 lines including a code example of a deprecated API).
- Action:
  - Section 2 opener: replace "Hard-coding prompt strings..." with "See Chapter 14.1.5 (Prompt Templates and Variable Injection) for template design fundamentals. The LangChain API is below."
  - Section 3 (Legacy LLMChain): shrink from 28 lines to a 3-line note. Move the code example to a `details/summary` block or just delete it - linking the v0.2 deprecation notice is enough.
  - Keep all LCEL content (section 4-6). This is the canonical LangChain framework reference and the rest of the book / E.1 / F.1 explicitly point here.

### Section D.2: Memory and Conversation Management
- Topic: Legacy memory classes (`ConversationBufferMemory`, `ConversationSummaryMemory`, `ConversationTokenBufferMemory`), modern `RunnableWithMessageHistory`, Redis-backed history, trimming strategies.
- Body coverage:
  - Chapter 24.3 (Memory & Context Management) covers conversation memory strategies in the body.
  - Chapter 26.6 (Memory Architecture for Agents) covers 5-layer memory taxonomy, storage design, write/read policies, TTL/decay, PII.
  - D.2 section 1 ("The Memory Problem") and section 5 ("Strategies for Long Conversations" with the 4-row comparison table) duplicate this body theory.
- Verdict: KEEP API code for LangChain classes; DUPLICATE OF BODY for the memory-strategy taxonomy (table in section 5) and the "memory problem" framing (section 1).
- Action:
  - Section 1: replace the 2 paragraphs explaining why memory matters with a single sentence + backref: "For conversation memory theory and the taxonomy of buffer / summary / token-window / hybrid strategies, see Chapter 24.3 (Memory & Context Management) and Chapter 26.6 (Memory Architecture for Agents). This section shows the LangChain mappings."
  - Section 5 comparison table (Full buffer / Token buffer / Summary / Summary+buffer): delete from D.2; this table belongs in Chapter 24.3 or 26.6 if not already there. If chapter 24.3 lacks it, this is a THEORY-MISSING-FROM-BODY move.
  - Keep all legacy memory class examples and the `RunnableWithMessageHistory` + Redis section unchanged.

### Section D.3: Document Loaders, Splitters, Retrievers
- Topic: `PyPDFLoader`, `WebBaseLoader`, `CSVLoader`, `RecursiveCharacterTextSplitter`, specialized splitters (Markdown, Python, HTML), `FAISS`/vector store retrievers, `EnsembleRetriever`, `ContextualCompressionRetriever`, end-to-end RAG chain.
- Body coverage:
  - Chapter 23.1 (RAG Architecture & Fundamentals) covers the ingestion pipeline (section 19.1.2 "The Ingestion Pipeline" is 168 lines!), chunking strategies, naive RAG, context window management.
  - Chapter 22 (Embeddings & Vector DB) covers embedding generation and vector stores.
  - Chapter 25.2 (Tools of the Trade: Retrieval Libraries) already lists LangChain, LlamaIndex, Haystack with one-line summaries.
  - D.3 section 2.2 "Choosing Chunk Size" (3 sentences on small vs large chunks) duplicates Chapter 23.1.2's chunking discussion.
  - D.3 section 4 opens with a 1-paragraph explanation of why ensemble retrieval helps (reciprocal rank fusion, dense+sparse) - that theory belongs in Chapter 23 (hybrid search).
- Verdict: KEEP all LangChain-specific code; DUPLICATE OF BODY for the chunk-size paragraph and the ensemble/RRF motivation. Section 6 ("Putting It All Together") is canonical LCEL+RAG recipe - keep.
- Action:
  - Section 2 "Choosing Chunk Size" 3-sentence prose: replace with "See Chapter 23.1 for chunk-size tradeoffs. Start at 500-1000 characters with 10-20% overlap."
  - Section 4 opening: replace the RRF motivation paragraph with "See Chapter 23 for hybrid search and RRF rationale. `EnsembleRetriever` is the LangChain implementation."
  - Keep code fragments D.3.1 - D.3.5 and the RAG chain example.

### Section D.4: Output Parsers and Structured Output
- Topic: `with_structured_output`, Pydantic schemas, `PydanticOutputParser`, `JsonOutputParser`, `OutputFixingParser`, `RetryOutputParser`, streaming structured output.
- Body coverage:
  - Chapter 13.2 (Structured Output) is the body home for structured-output theory and provider-native support.
  - D.4 section 1 ("Why Structured Output Matters") is a single paragraph that duplicates Chapter 13.2 motivation.
- Verdict: KEEP API code; DUPLICATE OF BODY for section 1 (1 paragraph). Everything else is framework-specific and stays.
- Action:
  - Section 1 (5 sentences): replace with "See Chapter 13.2 (Structured Output) for the motivation. The LangChain API is below." or delete entirely - the "Why" is small enough that just deleting it works.
  - Keep all parser examples.

### Section D.5: Agents, Tools, and Callbacks
- Topic: `@tool` decorator, built-in tools, `create_tool_calling_agent` + `AgentExecutor`, callbacks, LangSmith tracing, custom agent loops, production checklist.
- Body coverage:
  - Chapter 26 (AI Agents) covers the agent loop, memory architecture, deployment blueprint.
  - Chapter 27.1 (Function Calling Across Providers) covers function calling across OpenAI/Anthropic/Google - this is theory that D.5 sections 1-2 do not duplicate (D.5 is correctly LangChain-specific).
  - Chapter 27.4 (Custom Tool Design: Validation, Error Handling, Security) covers tool-design principles and the production checklist in D.5's Figure D.5.2.
  - Figure D.5.2 (Concern / Recommendation 6-row table: Runaway loops, Cost control, Tool safety, Error handling, Observability, Timeouts) duplicates Chapter 27.4 and Chapter 26.5 (production agent architecture).
  - The "When to Use Custom Loops vs AgentExecutor vs LangGraph" warning callout is correctly framework-specific (it compares LangChain offerings) - keep.
- Verdict: KEEP code and LangChain-specific guidance; DUPLICATE OF BODY for Figure D.5.2 (production checklist).
- Action:
  - Figure D.5.2: trim to 2 rows that are LangChain-specific (max_iterations, handle_parsing_errors). For the other 4 rows (cost control, tool safety, observability, timeouts), replace with: "See Chapter 26.5 (Production Agent Architecture) and Chapter 27.4 (Custom Tool Design) for the cross-framework production checklist."
  - Keep all 7 sections of D.5 otherwise. This is the strongest framework reference in D.

## Appendix E: Orchestration Frameworks

E has a single section file (`section-e.1.html`) titled "P.2 Orchestration Frameworks: LangChain, LlamaIndex, Haystack, and DSPy." The appendix index advertises 3 sections but only 1 exists - the index is broken.

### Section E.1: LangChain, LlamaIndex, Haystack, DSPy comparison
- Topic: Framework design philosophies, feature-matrix table, code-complexity demo (same RAG pipeline in all 4), strengths/weaknesses, production-readiness matrix, decision table.
- Body coverage:
  - Chapter 25.2 (Tools of the Trade Part 5) already lists LangChain, LlamaIndex, Haystack with comparison tables. The E.1 framework comparison and the 25.2 comparison are doing the same job at different granularities.
  - Chapter 14.5.2 (DSPy: Declarative Prompting with Optimizers) covers DSPy in the body - so E.1's DSPy paragraphs ARE on body topic. The signature/teleprompter framing in E.1 section 1 "DSPy takes the most radical approach..." duplicates Chapter 14.5.2's framing.
- Cross-appendix duplication (D vs E):
  - E.1 section 3.1 "LangChain" code example (load + chunk + vectorstore + LCEL chain) duplicates D.3 section 6 "Putting It All Together" almost line-for-line. Both use `TextLoader`, `RecursiveCharacterTextSplitter`, `Chroma`/`FAISS`, `ChatPromptTemplate`, `RunnablePassthrough`, `StrOutputParser`. This is the strongest D-vs-E duplication.
  - E.1 section 1 paragraph 1 on LangChain ("component-based philosophy... hundreds of integrations... Runnable protocol") duplicates D.1 section 4 LCEL intro ("Every LCEL component implements the Runnable interface").
  - E.1 section 4.1 "LangChain strengths/weaknesses" paragraph duplicates the D appendix opener's framing.
- Verdict: Most of E.1 is essay-style comparison, not framework reference. Three classifications:
  - **KEEP** the 4-column feature-comparison tables (section 2, section 5) and the decision table (section 6) - these are unique cross-framework reference content not duplicated elsewhere.
  - **DUPLICATE OF ANOTHER APPENDIX** for section 3.1 (LangChain code example - lives better in D.3.6).
  - **DUPLICATE OF BODY (move to Chapter 25.2)** for sections 1, 3, 4: the design-philosophy prose and the strengths/weaknesses paragraphs, which is exactly Chapter 25.2's job.
  - **THEORY MISSING FROM BODY** for the DSPy signature/teleprompter framing - but it is already in body chapter 14.5.2! E.1's DSPy paragraphs are actually duplicating body, not filling a gap.
- Action:
  - Delete section 1 (Framework Overview and Design Philosophies) and section 4 (Strengths and Weaknesses). The chapter-25.2 comparison table + the v0.X feature matrix in E.1 section 2 cover this.
  - Section 3 (Code Complexity Comparison): keep ONLY 3.2 (LlamaIndex), 3.3 (Haystack), 3.4 (DSPy). Replace 3.1 (LangChain) with: "See Appendix D.3.6 for the LangChain RAG chain. The same pipeline in LlamaIndex / Haystack / DSPy is below for comparison."
  - Keep section 2 (Feature Comparison table), section 5 (Production Readiness table), section 6 (Decision Table). These are the value-add.
  - Replace section 1 with a single short paragraph: "This appendix compares orchestration frameworks at a glance. For deep dives, see D (LangChain), the LlamaIndex documentation, Haystack documentation, and Chapter 14.5.2 (DSPy)."
  - Fix the missing sections (the index advertises 3, only 1 exists) OR repair the appendix index to reflect the single-section reality.

## Appendix F: Agent Frameworks

F also has a single section file (`section-f.1.html`) titled "P.3 Agent Frameworks: LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Semantic Kernel, smolagents, PydanticAI."

### Section F.1: Seven-framework comparison
- Topic: Three architecture patterns (graph-based, role-based, code-first), feature-matrix table, multi-agent patterns (supervisor / collaborative / hierarchical), production-readiness, decision table, integration/MCP/A2A notes.
- Body coverage:
  - Chapter 26 (AI Agents) covers agent loops, ReAct, planning.
  - Chapter 27.2 (Model Context Protocol) is the body home for MCP. F.1 section 6 mentions MCP correctly with a backref-worthy framing.
  - Chapter 27.3 (Agent-to-Agent Protocol A2A) is the body home for A2A. F.1 mentions A2A in section 6 - already does this right.
  - Chapter 28.2 (Architecture Patterns) covers multi-agent topologies. F.1 section 3 (Supervisor / Collaborative / Hierarchical) duplicates 28.2.
  - Chapter 30.2 (Tools of the Trade Part 6: Libraries & Frameworks) already lists LangGraph, CrewAI, smolagents, PydanticAI with one-line summaries and a comparison table.
- Cross-appendix duplication:
  - F.1 section 1.1 "Graph-Based Architecture (LangGraph)" overview prose duplicates the D.5 "When to Use Custom Loops vs AgentExecutor vs LangGraph" callout context plus the Chapter 30.2.1 row on graph-based agent runtimes.
  - F.1's seven-framework feature table (section 2) is broader than 30.2's table; it's unique to F.
- Verdict:
  - **KEEP** the comprehensive 7-framework feature table (section 2), the production-readiness table (section 4), and the selection guide (section 5). These are unique reference content.
  - **DUPLICATE OF BODY (move to Chapter 28.2)** for section 3 (Multi-Agent Patterns: supervisor / collaborative / hierarchical) - body 28.2 already covers this.
  - **DUPLICATE OF BODY (replace with backref)** for section 1 (Architecture Patterns) prose. The 3 architecture patterns are described in Chapter 26 and 28.2; the framework-specific code examples in 1.1-1.3 should stay but be reframed as "Here's how each pattern looks in code:" rather than re-explaining the pattern from scratch.
  - Section 6 (Integration and Interoperability) handles MCP and A2A correctly with cross-references - keep.
- Action:
  - Section 1 architecture-pattern paragraphs (the 3-sentence intros before each code example): replace each with "See Chapter 26 / 28.2 for the pattern. The LangGraph implementation is:" / "The CrewAI implementation is:" / "The OpenAI Agents SDK implementation is:" Keep the code examples.
  - Delete section 3 (Multi-Agent Patterns, 3 sub-sections of 1-paragraph each). Replace with: "See Chapter 28.2 (Architecture Patterns) for the supervisor / collaborative / hierarchical taxonomy. The framework-specific implementations are referenced in the feature table above."
  - Keep sections 2, 4, 5, 6.
  - Fix the broken appendix index that advertises 3 sections when only 1 exists.

## Appendix G: Problem-Solution Key

### Whole appendix
- Topic: Task-to-chapter lookup table with 11 categories (Text Understanding, Information Extraction, Generation, Search/Retrieval, Conversational AI, Agents, Training, Scaling, Deployment, Multimodal, Safety) and roughly 60 rows.
- Body coverage: By design G is a lookup index that points INTO the body. It is not duplicating; it is a routing layer.
- Verdict: KEEP entirely. This is exactly what a problem-solution key should look like.
- Action: None for duplication. (Out-of-scope issue: many "Tools" links point to wrong appendices, e.g. row "Sentiment analysis" links DSPy to appendix-c-huggingface-ecosystem when DSPy is actually in E and Chapter 14.5. That's a link-integrity bug, not a duplication problem. Out of scope for this audit.)

## Cross-appendix duplications (focused on D vs E)

1. **E.1 section 3.1 vs D.3 section 6**: LangChain RAG pipeline code (loader -> splitter -> Chroma/FAISS -> LCEL chain). E.1 reproduces ~25 lines that exist verbatim in D.3.6. Strong duplicate. Action: replace E.1 section 3.1 with a backref + the LCEL chain summary only.
2. **E.1 section 1 paragraph 1 vs D.1 section 4 LCEL intro**: Both explain LangChain's Runnable protocol and component-based composition. Action: delete E.1's design-philosophy paragraph; keep D.1's because D is the canonical LangChain reference.
3. **E.1 section 4.1 LangChain strengths/weaknesses vs D index opener**: The strengths-and-weaknesses paragraph in E.1 ("Unmatched integration breadth; large community...; LCEL provides a powerful composition model; LangSmith provides excellent observability") is essay-style and already implicit in D's framing. Action: delete from E.1.
4. **F.1 section 1.1 LangGraph paragraphs vs D.5 callout "When to Use Custom Loops vs AgentExecutor vs LangGraph"**: F.1 frames LangGraph as the "max-control graph-based" option; D.5 also tells the reader "for branching/cycles/state, use LangGraph." Mild overlap, but D.5's framing is contextual (when you've outgrown AgentExecutor) and F.1's is comparative (vs CrewAI/AutoGen/etc.). Action: leave both; they serve different reader paths.
5. **C.4 LoRA math intro vs C.4 itself**: Within C.4 there are mini-duplicates - section 1's `W + BA` LaTeX appears, then section 2 (QLoRA) re-explains "LoRA matrices in higher precision." This is self-duplication within C. Action: consolidate section 1 to be "LoRA math" + code, section 2 to start with "QLoRA = NF4 base + LoRA adapter" and skip re-explaining the decomposition.

## Theory-to-body moves

1. **Move Figure C.3.2 (Distributed training strategies table) -> Chapter 18 or Appendix M (Distributed ML).** The DDP / FSDP / ZeRO-2 / ZeRO-3 taxonomy is foundational distributed-training theory, not HuggingFace API reference. C.3 can keep the HuggingFace-specific CLI examples.

2. **Move D.2 section 5 conversation-memory strategy comparison table (Full buffer / Token buffer / Summary / Summary+buffer) -> Chapter 24.3 (Memory & Context Management) or Chapter 26.6.** This is conversational AI theory that happens to be illustrated with LangChain. The strategies are framework-agnostic and belong in body.

3. **Move E.1's DSPy compilation framing -> Chapter 14.5.2 (which already covers DSPy).** If chapter 14.5.2 is already comprehensive (it is - 9 sub-sections including "From Manual Craft to Programmatic Optimization", "DSPy: Declarative Prompting with Optimizers"), then E.1's DSPy paragraphs are pure duplication and should just be deleted from E.1 with a backref to 14.5.2. Verify 14.5.2 already explains signatures and teleprompters; if so, no theory needs to "move" - just delete from E.1.

## Notable observations not in the duplication frame

- E and F each have a single section file but the appendix index promises 3 sections (E) and the dirs are sized as if expecting more. Either build the missing sections (E.1 about "LLM Tooling Landscape" and E.3 about "Agent Frameworks"; F.1 about "Agent Frameworks") or fix the index. Note that the current E.1 is internally numbered "P.2" and F.1 is "P.3" - the numbering implies an "E.1 = tooling landscape" and "E.2 = orchestration" and "E.3 = agent frameworks" plan that was partially executed. Renaming and re-routing pending.
- C, D, E, F all still carry stale legacy letters in their `<h1>` and `<title>` tags (J for C, K for D, P.2 for E, P.3 for F). Doesn't affect duplication but does affect cross-refs from G.
- Appendix G's "Tools" links sometimes target the wrong appendix (e.g., DSPy linked to appendix-c-huggingface-ecosystem). Out of scope for this audit but worth a follow-up.
- C's index `When to Use This Appendix` callout still says "For orchestration frameworks that wrap LLM calls, see Appendix K (LangChain) instead" - that's a stale reference to Appendix K when LangChain is now D.

## Prioritized action list

Highest-impact (do first):
1. E.1 section 3.1 -> backref D.3.6. Single biggest D-vs-E duplicate.
2. E.1 sections 1 and 4 -> delete; keep only the tables (sections 2, 5, 6).
3. F.1 section 3 (Multi-Agent Patterns) -> backref Chapter 28.2.
4. D.2 section 5 strategy table -> move to Chapter 24.3.

Medium:
5. C.1 section 3 (encoder/decoder/encoder-decoder explanation) -> trim, backref Chapter 4.
6. C.1 section 6 (decoding strategies) -> trim, backref Chapter 5.
7. C.4 sections 1, 4, 5 (LoRA/DPO/PPO math intros) -> trim, backref Chapters 19/20.
8. D.1 section 3 (legacy LLMChain) -> shrink to a 3-line note.
9. D.5 Figure D.5.2 -> trim 4 of 6 rows to backref Chapters 26.5/27.4.

Low (style cleanup, mostly already-correct):
10. C.2 fast-tokenizer 3-sentence intro -> backref Chapter 2 tokenization.
11. D.3 chunk-size paragraph -> backref Chapter 23.1.
12. D.4 section 1 "Why Structured Output Matters" -> delete or shrink to one sentence.

Structural (separate task, not duplication):
13. Fix E and F appendix indexes to match the single-section reality (or build the missing sections).
14. Update stale legacy letters (C is "Appendix D / Section D.1-D.5" in headers; D is "Section K"; E is "P.2"; F is "P.3").
15. Verify G's Tools column links go to the right appendices.
