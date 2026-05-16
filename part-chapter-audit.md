# Part and Chapter Landing Audit

Audit root: `E:/Projects/BookBlogsHome/LLMBook`

## Summary Table

| Part | Landing nav OK? | Chapter cards OK? | Chapters with broken landings |
|------|-----------------|-------------------|-------------------------------|
| Front Matter | yes | n/a | (none) |
| Part I: Foundations | **no** | yes | (none) |
| Part II: Understanding LLMs | **no** | yes | (none) |
| Part III: Working with LLMs | **no** | yes | (none) |
| Part IV: Training and Adapting | **no** | yes | Ch 16 |
| Part V: Retrieval and Conversation | **no** | yes | (none) |
| Part VI: Agentic AI | **no** | yes | Ch 21, Ch 24 |
| Part VII: AI Applications | **no** | yes | (none) |
| Part VIII: Evaluation & Production | **no** | yes | (none) |
| Part IX: Safety & Strategy | **no** | yes | Ch 30 |
| Part X: Frontiers | **no** | yes | (none) |
| Part XI: From Idea to AI Product | **no** | yes | Ch 34 |
| Part XII: LLM Applications Across Industries | yes | yes | (none) |
| Appendices | yes | n/a | appendix-g-model-cards, appendix-h-prompt-templates, appendix-i-datasets-benchmarks, appendix-j-huggingface-ecosystem, appendix-k-langchain, appendix-l-experiment-tracking, appendix-m-inference-serving, appendix-n-distributed-ml, appendix-o-docker-containers, appendix-p-tooling-ecosystem, appendix-u-freshness-2026 |
| Capstone | yes | n/a | (none) |

## Broken chapter-nav (missing nav or required link)

(none)

## Broken chapter-nav (404 hrefs)

- appendices/appendix-g-model-cards/index.html:75: chapter-nav `next` href `section-f.1.html` -> 404 (resolved `appendices/appendix-g-model-cards/section-f.1.html`)
- appendices/appendix-h-prompt-templates/index.html:105: chapter-nav `next` href `section-g.1.html` -> 404 (resolved `appendices/appendix-h-prompt-templates/section-g.1.html`)
- appendices/appendix-i-datasets-benchmarks/index.html:83: chapter-nav `next` href `section-h.1.html` -> 404 (resolved `appendices/appendix-i-datasets-benchmarks/section-h.1.html`)
- appendices/appendix-j-huggingface-ecosystem/index.html:86: chapter-nav `next` href `section-i.1.html` -> 404 (resolved `appendices/appendix-j-huggingface-ecosystem/section-i.1.html`)
- appendices/appendix-k-langchain/index.html:86: chapter-nav `next` href `section-j.1.html` -> 404 (resolved `appendices/appendix-k-langchain/section-j.1.html`)
- appendices/appendix-l-experiment-tracking/index.html:86: chapter-nav `next` href `section-k.1.html` -> 404 (resolved `appendices/appendix-l-experiment-tracking/section-k.1.html`)
- appendices/appendix-m-inference-serving/index.html:82: chapter-nav `next` href `section-l.1.html` -> 404 (resolved `appendices/appendix-m-inference-serving/section-l.1.html`)
- appendices/appendix-n-distributed-ml/index.html:94: chapter-nav `next` href `section-m.1.html` -> 404 (resolved `appendices/appendix-n-distributed-ml/section-m.1.html`)
- appendices/appendix-o-docker-containers/index.html:80: chapter-nav `next` href `section-n.1.html` -> 404 (resolved `appendices/appendix-o-docker-containers/section-n.1.html`)
- appendices/appendix-p-tooling-ecosystem/index.html:74: chapter-nav `next` href `section-o.1.html` -> 404 (resolved `appendices/appendix-p-tooling-ecosystem/section-o.1.html`)
- appendices/appendix-u-freshness-2026/index.html:110: chapter-nav `next` href `../appendix-aj-reading-pathways/index.html` -> 404 (resolved `appendices/appendix-aj-reading-pathways/index.html`)

## Backwards / skipped / wrong-target chapter-nav

- part-1-foundations/index.html:129: chapter-nav `next` href `../part-2-understanding-llms/index.html` (expected `part-1-foundations/module-00-ml-pytorch-foundations/index.html`)
- part-2-understanding-llms/index.html:126: chapter-nav `next` href `../part-3-working-with-llms/index.html` (expected `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html`)
- part-3-working-with-llms/index.html:95: chapter-nav `next` href `../part-4-training-adapting/index.html` (expected `part-3-working-with-llms/module-11-llm-apis/index.html`)
- part-4-training-adapting/index.html:116: chapter-nav `next` href `../part-5-retrieval-conversation/index.html` (expected `part-4-training-adapting/module-14-synthetic-data/index.html`)
- part-5-retrieval-conversation/index.html:99: chapter-nav `next` href `../part-6-agentic-ai/index.html` (expected `part-5-retrieval-conversation/module-18-embeddings-vector-db/index.html`)
- part-6-agentic-ai/index.html:126: chapter-nav `next` href `../part-7-multimodal-applications/index.html` (expected `part-6-agentic-ai/module-21-ai-agents/index.html`)
- part-7-multimodal-applications/index.html:85: chapter-nav `next` href `../part-8-evaluation-production/index.html` (expected `part-7-multimodal-applications/module-26-multimodal/index.html`)
- part-8-evaluation-production/index.html:92: chapter-nav `next` href `../part-9-safety-strategy/index.html` (expected `part-8-evaluation-production/module-28-evaluation-observability/index.html`)
- part-9-safety-strategy/index.html:90: chapter-nav `next` href `../part-10-frontiers/index.html` (expected `part-9-safety-strategy/module-30-safety-ethics-regulation/index.html`)
- part-10-frontiers/index.html:72: chapter-nav `next` href `../part-11-idea-to-product/index.html` (expected `part-10-frontiers/module-33-emerging-architectures/index.html`)
- part-11-idea-to-product/index.html:82: chapter-nav `next` href `../part-12-llm-applications-across-industries/index.html` (expected `part-11-idea-to-product/module-34-idea-to-product/index.html`)

## Missing or orphan chapter cards (Part landings)

(none)

## Missing or orphan section cards (Chapter landings)

- [missing] part-4-training-adapting/module-16-peft/index.html: section file `section-16.5.html` exists in module but not linked from chapter landing
- [missing] part-4-training-adapting/module-16-peft/index.html: section file `section-16.6.html` exists in module but not linked from chapter landing
- [missing] part-4-training-adapting/module-16-peft/index.html: section file `section-16.7.html` exists in module but not linked from chapter landing
- [missing] part-11-idea-to-product/module-34-idea-to-product/index.html: section file `section-34.4.html` exists in module but not linked from chapter landing
- [missing] part-11-idea-to-product/module-34-idea-to-product/index.html: section file `section-34.5.html` exists in module but not linked from chapter landing
- [missing] part-11-idea-to-product/module-34-idea-to-product/index.html: section file `section-34.6.html` exists in module but not linked from chapter landing
- [missing] part-11-idea-to-product/module-34-idea-to-product/index.html: section file `section-34.7.html` exists in module but not linked from chapter landing
- [missing] appendices/appendix-g-model-cards/index.html: section file `section-g.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-g-model-cards/index.html: section file `section-g.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-g-model-cards/index.html: section file `section-g.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.5.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.6.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.7.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-h-prompt-templates/index.html: section file `section-h.8.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-i-datasets-benchmarks/index.html: section file `section-i.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-i-datasets-benchmarks/index.html: section file `section-i.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-i-datasets-benchmarks/index.html: section file `section-i.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-i-datasets-benchmarks/index.html: section file `section-i.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-i-datasets-benchmarks/index.html: section file `section-i.5.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-j-huggingface-ecosystem/index.html: section file `section-j.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-j-huggingface-ecosystem/index.html: section file `section-j.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-j-huggingface-ecosystem/index.html: section file `section-j.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-j-huggingface-ecosystem/index.html: section file `section-j.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-j-huggingface-ecosystem/index.html: section file `section-j.5.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-k-langchain/index.html: section file `section-k.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-k-langchain/index.html: section file `section-k.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-k-langchain/index.html: section file `section-k.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-k-langchain/index.html: section file `section-k.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-k-langchain/index.html: section file `section-k.5.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-l-experiment-tracking/index.html: section file `section-l.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-l-experiment-tracking/index.html: section file `section-l.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-l-experiment-tracking/index.html: section file `section-l.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-l-experiment-tracking/index.html: section file `section-l.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-l-experiment-tracking/index.html: section file `section-l.5.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-m-inference-serving/index.html: section file `section-m.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-m-inference-serving/index.html: section file `section-m.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-m-inference-serving/index.html: section file `section-m.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-m-inference-serving/index.html: section file `section-m.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-m-inference-serving/index.html: section file `section-m.5.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-n-distributed-ml/index.html: section file `section-n.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-n-distributed-ml/index.html: section file `section-n.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-n-distributed-ml/index.html: section file `section-n.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-n-distributed-ml/index.html: section file `section-n.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-n-distributed-ml/index.html: section file `section-n.5.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-n-distributed-ml/index.html: section file `section-n.6.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-n-distributed-ml/index.html: section file `section-n.7.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-o-docker-containers/index.html: section file `section-o.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-o-docker-containers/index.html: section file `section-o.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-o-docker-containers/index.html: section file `section-o.3.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-o-docker-containers/index.html: section file `section-o.4.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-p-tooling-ecosystem/index.html: section file `section-p.1.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-p-tooling-ecosystem/index.html: section file `section-p.2.html` exists in appendix but not linked from landing
- [missing] appendices/appendix-p-tooling-ecosystem/index.html: section file `section-p.3.html` exists in appendix but not linked from landing
- [orphan] part-6-agentic-ai/module-21-ai-agents/index.html: section list not in ascending order: [('21', 1), ('21', 6), ('21', 2), ('21', 3), ('21', 4), ('21', 5)]
- [orphan] part-6-agentic-ai/module-24-specialized-agents/index.html: section list not in ascending order: [('24', 1), ('24', 2), ('24', 2), ('24', 3), ('24', 1), ('24', 4), ('24', 4)]
- [orphan] part-9-safety-strategy/module-30-safety-ethics-regulation/index.html: section list not in ascending order: [('30', 1), ('30', 2), ('30', 3), ('30', 4), ('30', 5), ('30', 12), ('30', 6), ('30', 7), ('30', 8), ('30', 9), ('30', 10), ('30', 11)]
- [orphan] appendices/appendix-g-model-cards/index.html:54: section link `section-f.1.html` -> 404 (no such file `section-f.1.html`)
- [orphan] appendices/appendix-g-model-cards/index.html:60: section link `section-f.2.html` -> 404 (no such file `section-f.2.html`)
- [orphan] appendices/appendix-g-model-cards/index.html:66: section link `section-f.3.html` -> 404 (no such file `section-f.3.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:54: section link `section-g.1.html` -> 404 (no such file `section-g.1.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:60: section link `section-g.2.html` -> 404 (no such file `section-g.2.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:66: section link `section-g.3.html` -> 404 (no such file `section-g.3.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:72: section link `section-g.4.html` -> 404 (no such file `section-g.4.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:78: section link `section-g.5.html` -> 404 (no such file `section-g.5.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:84: section link `section-g.6.html` -> 404 (no such file `section-g.6.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:90: section link `section-g.7.html` -> 404 (no such file `section-g.7.html`)
- [orphan] appendices/appendix-h-prompt-templates/index.html:96: section link `section-g.8.html` -> 404 (no such file `section-g.8.html`)
- [orphan] appendices/appendix-i-datasets-benchmarks/index.html:50: section link `section-h.1.html` -> 404 (no such file `section-h.1.html`)
- [orphan] appendices/appendix-i-datasets-benchmarks/index.html:56: section link `section-h.2.html` -> 404 (no such file `section-h.2.html`)
- [orphan] appendices/appendix-i-datasets-benchmarks/index.html:62: section link `section-h.3.html` -> 404 (no such file `section-h.3.html`)
- [orphan] appendices/appendix-i-datasets-benchmarks/index.html:68: section link `section-h.4.html` -> 404 (no such file `section-h.4.html`)
- [orphan] appendices/appendix-i-datasets-benchmarks/index.html:74: section link `section-h.5.html` -> 404 (no such file `section-h.5.html`)
- [orphan] appendices/appendix-j-huggingface-ecosystem/index.html:53: section link `section-i.1.html` -> 404 (no such file `section-i.1.html`)
- [orphan] appendices/appendix-j-huggingface-ecosystem/index.html:59: section link `section-i.2.html` -> 404 (no such file `section-i.2.html`)
- [orphan] appendices/appendix-j-huggingface-ecosystem/index.html:65: section link `section-i.3.html` -> 404 (no such file `section-i.3.html`)
- [orphan] appendices/appendix-j-huggingface-ecosystem/index.html:71: section link `section-i.4.html` -> 404 (no such file `section-i.4.html`)
- [orphan] appendices/appendix-j-huggingface-ecosystem/index.html:77: section link `section-i.5.html` -> 404 (no such file `section-i.5.html`)
- [orphan] appendices/appendix-k-langchain/index.html:53: section link `section-j.1.html` -> 404 (no such file `section-j.1.html`)
- [orphan] appendices/appendix-k-langchain/index.html:59: section link `section-j.2.html` -> 404 (no such file `section-j.2.html`)
- [orphan] appendices/appendix-k-langchain/index.html:65: section link `section-j.3.html` -> 404 (no such file `section-j.3.html`)
- [orphan] appendices/appendix-k-langchain/index.html:71: section link `section-j.4.html` -> 404 (no such file `section-j.4.html`)
- [orphan] appendices/appendix-k-langchain/index.html:77: section link `section-j.5.html` -> 404 (no such file `section-j.5.html`)
- [orphan] appendices/appendix-l-experiment-tracking/index.html:53: section link `section-k.1.html` -> 404 (no such file `section-k.1.html`)
- [orphan] appendices/appendix-l-experiment-tracking/index.html:59: section link `section-k.2.html` -> 404 (no such file `section-k.2.html`)
- [orphan] appendices/appendix-l-experiment-tracking/index.html:65: section link `section-k.3.html` -> 404 (no such file `section-k.3.html`)
- [orphan] appendices/appendix-l-experiment-tracking/index.html:71: section link `section-k.4.html` -> 404 (no such file `section-k.4.html`)
- [orphan] appendices/appendix-l-experiment-tracking/index.html:77: section link `section-k.5.html` -> 404 (no such file `section-k.5.html`)
- [orphan] appendices/appendix-m-inference-serving/index.html:49: section link `section-l.1.html` -> 404 (no such file `section-l.1.html`)
- [orphan] appendices/appendix-m-inference-serving/index.html:55: section link `section-l.2.html` -> 404 (no such file `section-l.2.html`)
- [orphan] appendices/appendix-m-inference-serving/index.html:61: section link `section-l.3.html` -> 404 (no such file `section-l.3.html`)
- [orphan] appendices/appendix-m-inference-serving/index.html:67: section link `section-l.4.html` -> 404 (no such file `section-l.4.html`)
- [orphan] appendices/appendix-m-inference-serving/index.html:73: section link `section-l.5.html` -> 404 (no such file `section-l.5.html`)
- [orphan] appendices/appendix-n-distributed-ml/index.html:49: section link `section-m.1.html` -> 404 (no such file `section-m.1.html`)
- [orphan] appendices/appendix-n-distributed-ml/index.html:55: section link `section-m.2.html` -> 404 (no such file `section-m.2.html`)
- [orphan] appendices/appendix-n-distributed-ml/index.html:61: section link `section-m.3.html` -> 404 (no such file `section-m.3.html`)
- [orphan] appendices/appendix-n-distributed-ml/index.html:67: section link `section-m.4.html` -> 404 (no such file `section-m.4.html`)
- [orphan] appendices/appendix-n-distributed-ml/index.html:73: section link `section-m.5.html` -> 404 (no such file `section-m.5.html`)
- [orphan] appendices/appendix-n-distributed-ml/index.html:79: section link `section-m.6.html` -> 404 (no such file `section-m.6.html`)
- [orphan] appendices/appendix-n-distributed-ml/index.html:85: section link `section-m.7.html` -> 404 (no such file `section-m.7.html`)
- [orphan] appendices/appendix-o-docker-containers/index.html:53: section link `section-n.1.html` -> 404 (no such file `section-n.1.html`)
- [orphan] appendices/appendix-o-docker-containers/index.html:59: section link `section-n.2.html` -> 404 (no such file `section-n.2.html`)
- [orphan] appendices/appendix-o-docker-containers/index.html:65: section link `section-n.3.html` -> 404 (no such file `section-n.3.html`)
- [orphan] appendices/appendix-o-docker-containers/index.html:71: section link `section-n.4.html` -> 404 (no such file `section-n.4.html`)
- [orphan] appendices/appendix-p-tooling-ecosystem/index.html:53: section link `section-o.1.html` -> 404 (no such file `section-o.1.html`)
- [orphan] appendices/appendix-p-tooling-ecosystem/index.html:59: section link `section-o.2.html` -> 404 (no such file `section-o.2.html`)
- [orphan] appendices/appendix-p-tooling-ecosystem/index.html:65: section link `section-o.3.html` -> 404 (no such file `section-o.3.html`)

## Recommended Fixes

1. Fix Part landing `next` links on Parts I-XI: each currently points `next` -> next Part's landing, but per the audit spec `next` must point to the first chapter (module-NN/index.html) of THIS Part. Part XII already follows the correct pattern (`next` -> `module-36-legal-llms/index.html`); mirror that fix in Parts I-XI.
2. Re-prefix the stale `section-<letter>.<n>.html` references in 10 appendix landings (Appendix G through Appendix P). Each landing lists section cards using the letter of an adjacent appendix instead of its own letter (e.g. Appendix G lists `section-f.1.html`, Appendix H lists `section-g.1.html`, etc.). The same stale prefix is also used in the bottom chapter-nav `next` link of every affected appendix. Re-generate the section lists with the correct letter or run a search/replace within each appendix landing.
3. Fix `appendices/appendix-u-freshness-2026/index.html:110`: the bottom chapter-nav `next` link points to `../appendix-aj-reading-pathways/index.html`, which doesn't exist. Either point it to `appendices/index.html` (or back to `front-matter/fm-reading-pathways.html`), or create the missing appendix.
4. Add the missing section cards to `part-4-training-adapting/module-16-peft/index.html` (sections 16.5, 16.6, 16.7) and `part-11-idea-to-product/module-34-idea-to-product/index.html` (sections 34.4-34.7). The section files exist on disk but are not surfaced from the chapter landing, so readers cannot navigate to them through the chapter card list.
5. Fix the misordered/duplicated section lists in: `part-6-agentic-ai/module-21-ai-agents/index.html` (cards listed as 21.1, 21.6, 21.2, 21.3, 21.4, 21.5; move 21.6 to the end), `part-6-agentic-ai/module-24-specialized-agents/index.html` (cards repeat 24.1 and 24.2 with different titles; the underlying section-24.{5,6,7}.html files appear to be missing on disk, so either rename the cards or create the files), and `part-9-safety-strategy/module-30-safety-ethics-regulation/index.html` (30.12 appears between 30.5 and 30.6; move 30.12 to the end).
6. After applying the above structural fixes, re-run this audit script to confirm the residual issue count drops to zero. The audit script is at `E:/Claude/LLMBook/romantic-ardinghelli-50c3ba/audit_run.py`.
