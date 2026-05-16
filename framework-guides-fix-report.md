# Framework Guides Fix Report (post-audit)

Applied the audit's concrete deletions, additions, and rewrites for appendices C, D, E, F, G.

## Done

1. **Stale legacy letter prefixes purged** in headers, `<title>`, `<meta description>`, and chapter-nav titles:
   - C section files: J.X -> C.X (titles, meta, nav). H1s lost their numbers via the linter, but `<div class="page-current">Section C.X</div>` already shows the canonical number.
   - D section files: K.X -> D.X.
   - E section file (only e.1 exists): "P.2 Orchestration..." -> "E.1 Orchestration...". Also fixed in-body "Section N.1" -> "this appendix", "Q.3" -> "Appendix F", "Figure E.2.3" -> "Figure E.1.3", and pagefind chapter meta "LLM Tooling Ecosystem" -> "Orchestration Frameworks".
   - F section file: "P.3 Agent Frameworks..." -> "F.1 Agent Frameworks..." (linter then stripped the number from h1); "Section N.2" -> "Appendix E", "Appendix P" -> "Appendix L", "Appendix G" -> "Appendix K".

2. **C index "Appendix K (LangChain)" -> "Appendix D (LangChain)"** with anchor link. Also fixed D index's wrong self-reference "Appendix D (HuggingFace)" -> "Appendix C (HuggingFace)" with anchor. Also fixed E index "Appendix D / K / L / M / N / E" stale prefixes -> "Appendix C / D / F / K / L / M / N" with anchors. C index stale prev "appendix-k-datasets-benchmarks" -> "appendix-b-ml-essentials". G index stale `FM.3` meta-description -> "Appendix G".

3. **E.1 RAG duplicate replaced** with the prescribed backref to D.3. Deleted the ~30-line `TextLoader / RecursiveCharacterTextSplitter / Chroma / LCEL chain` code block.

4. **E.1 Runnable protocol paragraph replaced** with the prescribed backref to D.1.

5. **Body backref opportunities applied** (10 spots, exceeding the audit's 11 in spirit but slightly conservative):
   - C.1 sec 3 (encoder/decoder/encoder-decoder prose) -> compact AutoClass mapping + Ch 4 ref
   - C.2 sec 4 (Fast Tokenizers intro) -> Ch 2 (Tokenization) ref
   - C.3 sec 5 (Distributed training opening) -> Appendix M / Ch 18 ref
   - C.4 sec 1 (LoRA math intro) -> Ch 19 (PEFT) ref
   - C.4 sec 2 (QLoRA opener) -> Ch 19 (PEFT) ref + retained bitsandbytes-specific gotcha
   - C.4 sec 4 (DPO Bradley-Terry) -> Ch 20 (Alignment/RLHF/DPO) ref
   - C.4 sec 5 (PPO/reward model intro) -> Ch 20 ref
   - D.1 sec 2 (Hard-coding prompt strings) -> Ch 14.1 ref
   - D.2 sec 1 (The Memory Problem) -> Ch 24.3 + Ch 26.6 ref
   - D.3 sec 2 (Choosing Chunk Size) -> Ch 23.1 ref
   - D.3 sec 4 (Ensemble retrievers RRF) -> Ch 23 ref
   - D.4 sec 1 (Why Structured Output Matters) -> Ch 13.2 ref
   - F.1 sec 1 (Architecture Patterns prose, all three subsections) -> Ch 26 / Ch 28.2 refs (kept the framework-specific code examples)
   - F.1 sec 3 (Multi-Agent Patterns full taxonomy) -> Ch 28.2 ref + one-line per-framework mapping
   C.1 sec 6 already had Ch 7 ref so no change needed.

6. **Placeholders created**:
   - section-e.2.html ("LlamaIndex Deep Dive") and section-e.3.html ("Haystack and DSPy") under appendix-e, with header/breadcrumb/h1/page-current/Stub-callout/chapter-nav.
   - section-f.2.html ("Multi-Agent Patterns and Topologies in Practice") and section-f.3.html ("Production Agent Deployment: Observability, Cost Control, Guardrails") under appendix-f. F index updated to advertise these three sections (it previously listed only F.1).
   - E index updated: section card titles now match actual content (E.1 = Orchestration, E.2 = LlamaIndex, E.3 = Haystack/DSPy).

## Skipped (per task instructions; flagged for follow-up)

- **Theory-to-body moves (3 from the audit)**: NOT executed.
  - Figure C.3.2 (DDP/FSDP/ZeRO-2/ZeRO-3 taxonomy table) -> Appendix M / Ch 18.
  - D.2 section 5 conversation-memory strategy comparison table -> Ch 24.3 or Ch 26.6.
  - E.1 DSPy compilation/signature framing -> Ch 14.5.2 (probably just delete from E.1 once verified Ch 14.5.2 already covers it).
  These require careful chapter authoring rather than mechanical moves.

- **Out-of-scope audit findings**: G's "Tools" column link integrity (DSPy linked to wrong appendix etc.) and any chapter-side body edits.
