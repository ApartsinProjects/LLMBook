# Code Pedagogy R2 - Cycle 3 pass

Agent: 08-code-pedagogy (round 2). Scope: code-heavy sections in Parts 4-7 (excluding module 19, module 30 tools-of-the-trade catalogs and `index.html`). Pass focused on fixing critical structural bugs (return-inside-for-loop, break-followed-by-dead-code, mis-indented decorators), replacing placeholder `# implement X` comments with purpose-stating opening comments, modernizing function signatures with type hints, and rewriting generic captions to reference specific variables.

## Files touched (16)

### Part 4 (training and adaptation)
- `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.6.html` — rewrote weak caption "Using open reasoning models for inference" into a specific caption referencing the verification chain in the output.

### Part 6 (agentic AI)
- `part-6-agentic-ai/module-26-ai-agents/section-26.1.html` — fixed CRITICAL indentation bug in `reflect_and_improve` where the revise step was nested under `break`, making the loop unreachable. Refactored into helper `_chat()`, added type hints, expanded caption.
- `part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html` — rewrote two generic captions ("Using openai, OpenAI" and "Using anthropic") to describe the specific tool schemas and dispatch shape.
- `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html` — fixed CRITICAL cascade-indentation bug in the MCP server example: `@server.call_tool()` decorator, `raise ValueError`, `main()`, and `if __name__ == "__main__"` were all nested inside `list_tools`, making the file unparseable. Hoisted them to module scope, added type hints, expanded caption.

### Part 7 (retrieval and information extraction)
- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html` — fixed return-inside-for-loop bug in `mine_hard_negatives` (function returned after first iteration). Removed 240-char whitespace blob in docstring. Replaced verbose pairwise loop with `itertools.combinations`. Added type hints to both functions.
- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html` — fixed broken `multi_query_retrieve` (return-inside-for-loop, dangling indented return). Rewrote three weak captions ("Implementation of precision_at_k", "Using OpenAI embeddings with dimension control", "Using SentenceTransformer, numpy, sentence_transformers") to reference output values and dimensionality.
- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.7.html` — rewrote two weak captions ("Implementation of search_chunks", "Using data, labeled") to describe the comparative chunking experiment and corpus structure.
- `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.8.html` — added missing opening `<pre><code>` tag and import (file was missing its first three lines after a prior bad edit), restored ColQwen2 example. Fixed 240-char whitespace blob in `maxsim_score` docstring.
- `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html` — fixed two CRITICAL indentation bugs: `chunk_by_structure` had its `else` branch and trailing return nested inside the for-loop body; `build_context_with_budget` had `break` followed by unreachable code, and a return inside the loop. Replaced four placeholder `# implement X` comments with substantive purpose-stating openers. Added type hints, modernized to f-strings and `@` operator for matmul, switched to `gpt-4o` encoder.
- `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html` — rewrote three weak captions ("Implementation of retrieve", "Implementation of rag_answer", "Using sentence_transformers, SentenceTransformer, numpy") referencing the specific retrieval scores and pre-computed norms.
- `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html` — completely rewrote the broken `multi_source_search` example where `search_one` was incorrectly nested inside `multi_source_search` with cascade-indented body. Fixed `evaluate_and_refine` where the entire follow-up retrieve was inside a `for` body that returned early. Extracted system prompt as a constant. Added type hints, used Python 3.10+ pipe-union syntax. Rewrote two captions.
- `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html` — replaced five placeholder `# implement X` comments (ask_about_table, get_schema_context, text_to_sql, execute_with_retry, csv_to_queryable) with purpose-stating openers explaining the table-Q&A, text-to-SQL self-correction, and CSV-to-SQLite shortcut patterns.
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html` — fixed `multi_query_retrieve` return-inside-for-loop bug (same pattern as 31.1b). Fixed `rerank_results` return-inside-for-loop. Replaced two placeholder comments. Added type hints throughout.
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html` — fixed same `multi_query_retrieve` bug, replaced placeholder comment, rewrote three weak captions ("Implementation of baseline_search/rerank/recall_at_k").
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html` — fixed CRITICAL bug in `extract_triples` where the OpenAI call was unreachable when `entity_types=None` (entire body of function nested under `if entity_types:`). Extracted system prompt as constant, switched to `triples` array contract. Fixed `hybrid_kg_vector_retrieve` where vector search and combination were mis-indented inside the entity loop. Replaced two placeholder comments. Rewrote one caption.
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html` — rewrote two captions ("Querying with local and global search", "Evaluating GraphRAG with LLM-as-judge") to reference specific output scores and the local-vs-global routing distinction.
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html` — rewrote weak caption "Implementation of structure_aware_chunk" to reference heading-based section labels visible in the output.
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.6.html` — replaced two placeholder `# implement X` comments (`format_docs` in the LCEL block, `embed/retrieve/generate` in the framework-free block) with purpose-stating openers.
- `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.7.html` — replaced placeholder `# implement build_langchain_rag, build_llamaindex_rag` comment, fixed dangling `# --- LlamaIndex Implementation ---` comment that was nested inside `build_langchain_rag` (so the second function was defined at the wrong indent level).

## Patterns of bugs fixed

1. **Return-inside-for-loop** (10+ functions): the return statement was indented inside the loop body, so the function only ever processed the first iteration. Affected `mine_hard_negatives`, `multi_query_retrieve` (two copies in 35.1/35.1b), `rerank_results`, `chunk_by_structure`, `build_context_with_budget`, `evaluate_and_refine`, and others.
2. **Cascade indentation** (3 examples): top-level functions and `if __name__` blocks accidentally nested inside an earlier function's body. Affects the MCP server, the `multi_source_search` async fan-out, and `hybrid_kg_vector_retrieve`.
3. **Dead code after `break`**: `build_context_with_budget` had four lines of "should-append" code below a `break`, plus a `return` also inside the loop.
4. **Reflect-and-improve loop**: the revise step was nested inside the `if "no major issues" in critique: break` block, so revision never ran.
5. **Placeholder `# implement X` comments** (15+): replaced with 2-line opening comments that explain WHY the function exists and what library it uses.
6. **Generic auto-generated captions** ("Implementation of X", "Using X, Y"): rewrote ~15 captions to reference specific variables, parameter values, or output content.
7. **240-char whitespace blobs in docstrings**: two docstrings had been corrupted with massive runs of leading whitespace from a prior auto-format pass.
8. **`range(len(x))`**: replaced with `itertools.combinations` where pairwise; left other simple cases alone.

## Counts
- Code blocks substantially improved: ~30
- Captions rewritten for specificity: ~15
- Critical runtime/syntax bugs fixed: 10+
- Files touched: 19
- Type hints added to function signatures: ~20
