# Part 10 (Idea to Product) Review and Enrichment Report

Date: 2026-05-16. Scope: modules 40-49 sections only. Index files were untouched per coordination with in-flight index-staleness agent (a2251a4de72513129).

## Per-chapter results

### Module 40 (Ideation) - sections 1 -> 3
- Authored `section-40.2.html` "Problem-Discovery Heuristics" (~1,100 words, 4 callouts: big-picture, practical-example Harvey AI, key-insight, warning, key-takeaway). Covers the five heuristics: I-wish-I-had-an-intern, manual-handoff spotter, abandonment trail, schema-bridge, support-ticket audit.
- Authored `section-40.3.html` "The Bet-My-Money Test and Capability Mapping" (~1,200 words, 5 callouts: big-picture, practical-example fintech kill, warning, tip, key-takeaway, bibliography). Covers the three uncomfortable questions plus the 2026 problem-shape-to-capability mapping table with typical costs.
- Existing 40.1 retained (already strong omnibus, 2,500 words).

### Module 41 (Product Management) - sections 2 -> 3
- Authored `section-41.3.html` "UX and Iteration for LLM Products" (~1,300 words, 5 callouts: big-picture, practical-example Notion AI redesign, key-insight, warning Friday-prompt-edit, key-takeaway). Covers chat-vs-task UI, disclosure patterns, trust calibration, the fortnightly iteration cadence, and the three-bucket backlog.
- Existing 41.1 retained (strong, 2,100 words). 41.2 retained (large omnibus, 6,200 words). Note: 41.2 still carries legacy "31.2.x" h2 numbering per the `_section_split_plan.md`; not corrected in this pass to avoid touching the in-flight index.

### Module 42 (Strategy & Prioritization) - 4 sections, no changes
- 42.1, 42.2 are intro-style (1,000-1,200 words) but already callout-rich (3-4 callouts each). 42.3 and 42.4 are deep (5,800-6,800 words). No enrichment needed.

### Module 43 (Vibe-Coding) - sections 2 -> 3
- Authored `section-43.3.html` "The AI-Native IDE Landscape in 2026" (~1,400 words, 4 callouts: big-picture, practical-example Shopify workflow, warning cost-amplification, tip one-week paid trial, key-takeaway). Covers the six tools (Cursor, Claude Code, Cline, Zed, Windsurf, Copilot Workspace) with a comparison table, the editor-plus-terminal-agent pattern, repo-context strategies, and a decision matrix.
- Existing 43.1 and 43.2 retained.

### Module 44 (MVP) - sections 1 -> 3
- Authored `section-44.2.html` "The Vertical-Slice Pattern in Depth" (~1,200 words, 4 callouts: big-picture, practical-example 2025 legal-tech 5-day MVP, warning almost-done trap, key-insight slice-as-sensor, key-takeaway). Covers the five-layer slice template, three holding disciplines (freeze list, single demo path, five-day rule), three productive-surprise patterns.
- Authored `section-44.3.html` "Pilot Triggers: Keep, Pivot, or Kill" (~1,300 words, 4 callouts: big-picture, practical-example zombie that ate a year, warning two-pivot ceiling, tip kill ceremony, key-takeaway). Covers the four pilot signals decision matrix, sunk-cost failure mode, three productive pivots, and the kill postmortem template.
- Existing 44.1 retained.

### Module 45 (Prototype to Production) - 7 sections, no changes
- All sections are 4,700-6,300 words with rich callout coverage. No enrichment needed.

### Module 46 (Compute Planning) - 4 sections, no changes
- 46.1 and 46.2 are intro-style (1,000-1,100 words) but already have 3-4 callouts each. 46.3 and 46.4 are large (7,200-8,900 words). No enrichment needed.

### Module 47 (Scaling Economics) - 4 sections, no changes
- 47.1 and 47.2 are intro-style (1,000-1,200 words) already callout-rich. 47.3 and 47.4 are very large (7,400-11,700 words). No enrichment needed.

### Module 48 (Shipping & Deploying) - 6 sections, no changes
- All sections in 3,400-9,500 word range with strong callout coverage. No enrichment needed.

### Module 49 (Post-Launch Monitoring) - sections 1 -> 3
- Authored `section-49.2.html` "Drift Detection in Production" (~1,300 words, 4 callouts: big-picture, practical-example "11 percent thumbs-down" investigation, key-insight eval-set half-life, warning cost-drift inside agentic workflows, key-takeaway). Covers the five flavors of drift with detection signals, the silent provider update pattern, three detection practices.
- Authored `section-49.3.html` "Model-Rotation Strategy" (~1,400 words, 5 callouts: big-picture, practical-example one-afternoon rotation, warning vendor lock-in by a thousand cuts, tip route-cheap-pin-expensive, key-takeaway, bibliography). Covers the three 2024-2026 deprecation events that made rotation mandatory, the four ingredients (abstraction, portable eval, second source, runbook), the four hidden lock-in surfaces.
- Existing 49.1 retained (2,725-word omnibus already covering similar territory; new sections deepen specific topics).

## Summary
- Sections authored: 8 new files (40.2, 40.3, 41.3, 43.3, 44.2, 44.3, 49.2, 49.3).
- Callouts added: 36 across new sections, all standard classes (big-picture, key-insight, practical-example, warning, tip, key-takeaway, bibliography).
- Per-section word count: range 1,100-1,400, all within the 800-1,500 target.
- Section count gates: all in-scope chapters (40, 41, 43, 44, 49) now meet the 3-section minimum.
- Index files: untouched per coordination constraint. Index rebuild will pick up new sections on the next pipeline run.
- Named cases anchored to 2024-2026: Harvey AI (40.2), Intercom Fin AI (40.2), Notion AI redesign (41.3), Shopify engineering blog 2025 (43.3), 2025 legal-tech MVP (44.2), A16Z portfolio zombie project (44.3), Anthropic/OpenAI silent updates (49.2), 2024 OpenAI deprecation wave (49.3), 2026 EU AI Act enforcement (49.3).

## Diagram opportunities flagged for technical-diagram-designer
The following are high-value diagram candidates spotted while authoring; they were not generated in this pass.

1. **Section 40.3 capability-cost map**: scatter plot with x=typical-cost-per-call (log scale), y=integration-complexity, points labeled with the seven capabilities from the mapping table. Good first-pass diagram for ideation.
2. **Section 41.3 disclosure-pattern lattice**: a 2x2 of disclosure type (citation, confidence, trace, refusal) crossed with calibration impact (low/high), with example UI snippets in each cell.
3. **Section 43.3 IDE-tool taxonomy**: a hierarchical tree splitting the six tools by surface (VS Code fork, native editor, terminal agent, cloud workspace) and agent depth (completion-only, multi-file, agentic, autonomous). Replaces or supplements the comparison table.
4. **Section 44.2 vertical-slice diagram**: a five-layer vertical bar showing input -> capability -> output -> surface -> feedback, contrasted with a horizontal-scope alternative that fails at integration seams. Strong didactic value.
5. **Section 44.3 pilot-trigger decision tree**: from "pilot complete" through observable thresholds (abandonment, thumbs-up, return-rate, unit-economics) to the four action buckets. Replaces the table with a flowchart.
6. **Section 49.2 drift-flavor matrix**: 5x4 grid (flavor x detection-signal/cause/response/example), color-coded by urgency, with an arrow showing which flavor foreshadows which other.
7. **Section 49.3 rotation-strategy stack**: four-tier diagram showing abstraction layer at top, portable eval suite, second-source contract, and runbook; with arrows showing dependencies and event-trigger callouts (deprecation, price change, regulation).

All seven opportunities are well-scoped, didactic, and would survive the "two minutes of unaided reading" test the diagram brief calls for. Ready to hand off to a future `technical-diagram-designer` run.
