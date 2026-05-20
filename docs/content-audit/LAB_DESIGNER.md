# Lab Designer Audit (Parts 4 to 9 chapter index.html files)

Date: 2026-05-19
Agent: 41-lab-designer (book-skills cycle)
Branch: v2.0

## Mandate

End-of-chapter "labs" are 2 to 4 hour hands-on builds that anchor each chapter's concepts in a concrete artifact. This pass auditied the chapter-level `index.html` files in Parts 4 through 9 (modules 15 through 46) and inserted lab callouts where missing.

## Starting state

Grep for `callout lab` or `class="lab"` across the 30 candidate `index.html` files returned ZERO matches. Labs existed only at the section level (e.g. `section-35.5.html`), never at chapter-overview level. This was a fresh-add task across the board, not an audit-existing one.

## Placement decision

Labs are inserted as a `<div class="callout lab">` block immediately after the closing `</ul>` of the sections list, just before the `<div class="whats-next">` block. This matches the look of the existing section-level labs and uses the project's already-styled `.callout.lab` CSS class (defined in `styles/book.css` lines 1640, 1873 to 1880, with the existing flask icon).

The simpler `callout lab` HTML pattern (not the full 7-subsection template from the role file) was chosen to match the in-repo style and the explicit format the task brief specified.

## Labs added (22 total)

### Part IV: Training and Adaptation (4 of 5 modules covered; 19 is tools-of-the-trade, skipped)

| Module | Lab title | Time | Difficulty |
|---|---|---|---|
| 15 Synthetic Data | Generate, Filter, and Validate a 1,000-Example Synthetic SFT Dataset | 3 to 4h | Intermediate |
| 16 Fine-Tuning Fundamentals | Full Fine-Tune a 350M Model on a Domain Corpus and Measure Forgetting | 4 to 5h | Intermediate |
| 17 PEFT (PRIORITY) | Fine-Tune Llama-3.2-3B as a Writing-Style Mimic on Free Colab T4 | 4 to 6h | Intermediate |
| 18 Alignment / DPO | Run DPO on Llama-3.2-1B With a UltraFeedback Subset | 4 to 5h | Advanced |

### Part V: Multimodal LLMs (3 of 6 modules; skipped 23 3D, 24 VLA, 25 tools)

| 20 Audio | Build a Podcast Transcript-and-Summary Pipeline With Whisper + Diarization | 2 to 3h | Beginner-Intermediate |
| 21 Document/OCR | Build an Invoice-to-JSON Extractor With a VLM + Validation | 3h | Intermediate |
| 22 VLM | Fine-Tune a CLIP-Style Embedding on Your Own Image-Text Pairs | 3 to 4h | Intermediate |

### Part VI: Agentic AI (4 of 5 modules; skipped 30 tools)

| 26 AI Agents (PRIORITY) | Build a Research Agent for Wikipedia Questions | 4 to 5h | Intermediate |
| 27 Tool Use Protocols | Build an MCP Server That Exposes a Local Tool to Claude Desktop | 2 to 3h | Intermediate |
| 28 Multi-Agent | Build a 3-Agent Debate System That Beats a Single-Agent Baseline | 3 to 4h | Intermediate |
| 29 Specialized Agents | Build a Browser-Use Agent That Fills a Form Across Tabs | 3 to 4h | Intermediate |

### Part VII: Retrieval (5 of 6 modules; skipped 36 tools-of-the-trade)

| 31 Embeddings | Benchmark Five Embedding Models on Your Own Domain Data | 2 to 3h | Beginner-Intermediate |
| 32 RAG (PRIORITY) | Build a Q&A Bot Over a Docs Site You Actually Use | 3 to 4h | Intermediate |
| 33 Cross-Modal RAG | Build a Visual RAG Over a PDF Manual With ColPali | 3h | Intermediate |
| 34 Structured IE | Extract Entities and Relations From 100 News Articles Into a Queryable Graph | 4h | Intermediate |
| 35 Advanced RAG | Upgrade Lab 32's Naive RAG to GraphRAG + DSPy Compiled Pipeline | 4 to 5h | Advanced |

### Part VIII: Conversational AI (2 of 3 modules; skipped 41 tools)

| 37 Conversational AI (PRIORITY) | Build a Long-Term-Memory Chatbot That Remembers You Across Sessions | 3 to 4h | Intermediate |
| 40 Voice | Build a Realtime Voice Agent With Sub-1-Second Latency | 3 to 4h | Intermediate |

### Part IX: Evaluation (4 of 5 modules; skipped 45 tools)

| 42 Eval Foundations | Build an Eval Harness With Inspect AI Plus Three Custom Metrics | 3h | Intermediate |
| 43 Specialized Eval | Run RAGAS + Trajectory-Eval on Your Lab 26 and Lab 32 Bots | 3h | Intermediate |
| 44 Online Eval | Instrument a RAG App With Langfuse, Then Replay and Score Production Traffic | 3 to 4h | Intermediate |
| 46 LLM-as-Judge (PRIORITY) | Score Your RAG Bot With a Debiased Multi-Judge Panel | 2 to 3h | Intermediate |

## Lab chaining (intentional progression)

Labs are designed to compound. Reader who runs them in order builds a coherent portfolio:

- Lab 15 (synthetic data) -> Lab 17 (PEFT uses that data)
- Lab 32 (RAG bot) -> Lab 35 (upgrades to GraphRAG/DSPy) -> Lab 43 (evaluates with RAGAS) -> Lab 44 (instruments with Langfuse) -> Lab 46 (judges with multi-judge panel)
- Lab 26 (agent) -> Lab 43 (trajectory-evaluates it)
- Lab 27 (MCP server) generalizes the tool pattern used by Lab 26

This dependency graph is documented inline in each lab's description with explicit cross-references.

## Quality bar applied

Every lab includes:
- Concrete library names (specific packages, e.g. `instructor`, `inspect-ai`, `graphrag`, `pyannote/speaker-diarization-3.1`)
- A specific dataset or data source (real, fetchable)
- An explicit metric to track (recall@10, F1, kappa, ppl, latency)
- A "library shortcut" final step where the from-scratch build is re-implemented in 5 to 30 lines using the production library, mirroring the book's "Right Tool" principle
- Honest time estimate (2 to 6 hours)
- A named artifact the reader walks away with

## Coverage decisions (skipped modules)

The "tools of the trade" chapters (19, 25, 30, 36, 41, 45) are catalog chapters; they do not have a single dominant concept to anchor a lab against. Modules 23 (3D / Gaussian splatting) and 24 (VLA / robotics) were skipped because both require hardware (multi-view captures, robotic sims) beyond what the rest of the book assumes.

If you want labs in those modules, recommend lighter "explore three tools and write a one-pager" exercises instead of full 3-hour builds.

## Style conformance

- No em dashes or double dashes in any prose (manually checked; `--` matches in grep are all inside HTML comments or CLI `--flag` examples inside `<code>` tags).
- Numbered `<ol>` of 6 to 7 steps each.
- Final `<p><em>` line with time / difficulty / artifact.

## Files modified (22)

```
part-4-training-adaptation/module-15-synthetic-data/index.html
part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html
part-4-training-adaptation/module-17-peft/index.html
part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html
part-5-multimodal-llms/module-20-audio-music-generation/index.html
part-5-multimodal-llms/module-21-document-understanding-ocr/index.html
part-5-multimodal-llms/module-22-vision-language-models/index.html
part-6-agentic-ai/module-26-ai-agents/index.html
part-6-agentic-ai/module-27-tool-use-protocols/index.html
part-6-agentic-ai/module-28-multi-agent-systems/index.html
part-6-agentic-ai/module-29-specialized-agents/index.html
part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/index.html
part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html
part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/index.html
part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/index.html
part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/index.html
part-8-conversational-ai-with-llms/module-37-conversational-ai/index.html
part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/index.html
part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html
part-9-llm-evaluation-observability/module-43-specialized-evaluation/index.html
part-9-llm-evaluation-observability/module-44-online-eval-observability/index.html
part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/index.html
```

## Follow-up suggestions

1. The book skill expects 1 to 2 labs per chapter and prefers section-level placement. The chapter-index labs added here are course-anchor labs (one per chapter). Section-level labs already exist in many chapters (e.g. 35.4 "Building a Living Knowledge Base"). The two coexist coherently because chapter labs are weekend-scale and section labs are 30 to 90 min.
2. Consider adding section-level labs to chapters that lack them (currently mostly absent in Parts 4 and 9). That is a separate pass against `section-*.html` files.
3. Modules 23, 24, and the six "tools of the trade" chapters got skipped; revisit when (or if) they grow into hands-on chapters.
