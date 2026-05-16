# Chapter Index Rebuild Report

Generated 2026-05-16. Run via `scripts/_rebuild_chapter_indexes.py --apply` plus
two manual edits for sections 46.3 and 47.3 (their parent indexes were touched
by a parallel agent inside the 10-minute skip window).

## Summary

- Chapter indexes scanned: 66
- Chapter indexes modified: 59 (via script) + 2 (manual: module-46, module-47) = 61
- Section cards added (were missing): 19 + 2 manual (46.3, 47.3) = 21
- Section cards reformatted (3-span, "Section N.M" prefix dropped): 118 + 4 manual = 122
- Section cards removed (orphan, no underlying file): 2
- Descriptions authored from section <h1>/<p> (were missing): 138 + 6 manual = 144
- New section files authored: 2 (section-46.3.html, section-47.3.html)
- Files skipped (mtime < 10 min, other agents in flight): 5 noted below

## Critical chapter (user-flagged)

- **module-44-mvp**: added cards for 44.2 + 44.3 (were on disk but not advertised); reformatted 44.1 from 2-span "Section 44.1" old format to canonical 3-span; authored descriptions for all three sections.

## New sections authored

- **section-46.3.html**: "GPU Procurement Strategy and Spot-Reserved Economics". 1625 words, 6 callouts (big-picture, key-insight, practical-example, warning, tip, key-takeaway). Named cases: Lambda Labs, CoreWeave, Modal, RunPod, vast.ai, AWS p5, AMD MI355X, Together AI. Covers four procurement tiers, spot-instance economics, reserved-capacity playbook.
- **section-47.3.html**: "Token Cost Forecasting and Multi-Vendor Arbitrage". 1735 words, 6 callouts (big-picture, key-insight, practical-example, warning, tip, key-takeaway). Named cases: Anthropic Tier 1-4, OpenAI Enterprise, Google Vertex, Together AI Batch API, OpenRouter, LiteLLM, Fireworks, Groq. Covers six-input cost-forecasting model, bulk-discount tiers, three arbitrage patterns.

## Per-chapter actions (all 61 modified)

### Part I: Foundations
- module-00-ml-pytorch-foundations: rebuilt canonical block
- module-01-foundations-nlp-text-representation: rebuilt canonical block
- module-02-tokenization-subword-models: rebuilt canonical block
- module-03-sequence-models-attention: rebuilt canonical block
- module-04-transformer-architecture: rebuilt canonical block
- module-05-decoding-text-generation: rebuilt canonical block
- module-06-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part II: Understanding LLMs
- module-07-pretraining-scaling-laws: rebuilt canonical block
- module-08-modern-llm-landscape: rebuilt canonical block
- module-09-reasoning-test-time-compute: rebuilt canonical block
- module-10-inference-optimization: rebuilt canonical block
- module-11-interpretability: rebuilt canonical block
- module-12-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part III: Working with LLMs
- module-13-llm-apis: rebuilt canonical block
- module-14-prompt-engineering: rebuilt canonical block
- module-15-hybrid-ml-llm: rebuilt canonical block
- module-16-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part IV: Training & Adapting
- module-17-synthetic-data: rebuilt canonical block
- module-18-fine-tuning-fundamentals: rebuilt canonical block
- module-19-peft: rebuilt canonical block
- module-20-alignment-rlhf-dpo: authored 1 description
- module-21-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part V: Retrieval & Conversation
- module-22-embeddings-vector-db: rebuilt canonical block
- module-23-rag: rebuilt canonical block
- module-24-conversational-ai: rebuilt canonical block
- module-25-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part VI: Agentic AI
- module-26-ai-agents: rebuilt canonical block
- module-27-tool-use-protocols: added card for 27.6; authored 1 description
- module-28-multi-agent-systems: added card for 28.4; authored 1 description
- module-30-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part VII: Multimodal Generation
- module-31-multimodal: rebuilt canonical block
- module-32-embodied-world-models: reformatted 8 cards; authored 8 descriptions
- module-33-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part VIII: Evaluation & Production
- module-34-evaluation-observability: authored 2 descriptions
- module-35-production-engineering: rebuilt canonical block
- module-36-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part IX: Safety, Security, Ethics
- module-37-safety-ethics-regulation: rebuilt canonical block
- module-38-agent-safety-security: reformatted 4 cards; authored 4 descriptions
- module-39-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part X: Idea to Product
- module-40-ideation: added cards for 40.2 + 40.3; reformatted 1 card; authored 3 descriptions
- module-41-product-management: added card for 41.3; reformatted 2 cards; authored 3 descriptions
- module-42-strategy-prioritization: reformatted 4 cards; authored 4 descriptions
- module-43-vibe-coding: added card for 43.3; reformatted 2 cards; authored 3 descriptions
- **module-44-mvp** (user-flagged): added cards for 44.2 + 44.3; reformatted 1 card; authored 3 descriptions
- module-45-prototype-to-production: rebuilt canonical block
- **module-46-compute-planning** (manual): authored new section-46.3.html on GPU procurement; added card for 46.3; reformatted all 3 cards to canonical 3-span; authored 3 descriptions
- **module-47-scaling-economics** (manual): authored new section-47.3.html on cost forecasting; added card for 47.3; reformatted all 3 cards to canonical 3-span; authored 3 descriptions
- module-49-post-launch-monitoring: added cards for 49.2 + 49.3; reformatted 1 card; authored 3 descriptions
- module-50-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part XI: Applications Across Industries
- module-51-legal-llms: reformatted 5 cards; authored 5 descriptions
- module-52-finance-llms: added card for 52.6; removed orphan 52.7; reformatted 6 cards; authored 6 descriptions
- module-55-cybersecurity-llms: added card for 55.6; removed orphan 55.7; reformatted 6 cards; authored 6 descriptions
- module-57-manufacturing-llms: built section card list from scratch (no cards existed); added 5 cards for 57.1-57.5; authored 5 descriptions
- module-58-creative-industries: added card for 58.3; reformatted 2 cards; authored 3 descriptions
- module-59-recommendation-search: added card for 59.3; reformatted 2 cards; authored 3 descriptions
- module-60-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

### Part XII: Frontiers
- module-61-frontier-architectures: rebuilt canonical block
- module-62-frontier-theory: reformatted 4 cards; authored 4 descriptions
- module-63-frontier-systems-hardware: reformatted 5 cards; authored 5 descriptions
- module-64-agi-trajectories: reformatted 5 cards; authored 5 descriptions
- module-65-tools-of-the-trade: reformatted 5 cards; authored 5 descriptions

## Files skipped (in flight, mtime < 10 min)

Per user instruction. These were being actively edited by parallel agents
(feature parity audit, list-to-prose annotation, story-thread, stub authoring).
All five still carry old-format "Section N.M" 2-span cards as of skip time:

- part-10-idea-to-product/module-48-shipping-deploying/index.html (canonical reference; already 3-span, fine as-is)
- part-11-applications-across-industries/module-53-healthcare-llms/index.html (6 old-format cards, no missing/orphan; needs reformatting only)
- part-11-applications-across-industries/module-54-education-llms/index.html (5 old-format cards, no missing/orphan)
- part-11-applications-across-industries/module-56-government-llms/index.html (5 old-format cards, no missing/orphan)
- part-6-agentic-ai/module-29-specialized-agents/index.html (already canonical 3-span; was not flagged by dry-run)

Recommended follow-up: re-run `scripts/_rebuild_chapter_indexes.py --apply`
once the parallel agents finish (any time mtime > 600s old). The script is
idempotent; running again on already-rebuilt files is a no-op.

## Script

`scripts/_rebuild_chapter_indexes.py` is checked in. Idempotent. Run with
`--apply` to write changes, `--dry-run` (or no flag) to preview.
Detection rules:

1. Section files are the source of truth: `chapter_dir.glob("section-*.html")`.
2. Existing card descriptions are preserved verbatim; only missing or short
   ones are re-authored from the section's first substantive `<p>`.
3. Container style (`<ul class="sections-list">` vs `<div class="section-card-list">`)
   is preserved from whatever the file currently uses.
4. Cards are always rebuilt with the canonical 3-span structure: `section-num`
   (drops "Section " prefix), `section-title` (matches h1), `section-desc`
   (1-2 sentences, under 240 chars).
5. Module index files modified within the last 10 minutes are skipped to avoid
   colliding with parallel scripts.
