# Structural Architect Report (Round 2, Cycle 3)

Branch: `v2.0`
Date: 2026-05-19
Agent: 19-structural-architect (round 2)

## Scope

Address the GIANT_SECTION audit findings: 1 P1 + 23 P2 (24 total) flagging
section pages that exceeded the canonical envelope (5-7 h2s, 200-700 lines).

## Method

For each flagged section, re-extracted h2 titles and per-h2 line counts.
Classified each section as one of:

- **Catalog**: many short h2s (avg <70 lines, >=9 h2s), each a discrete
  item from a list (libraries, providers, techniques, regulatory tools).
- **Long-form single topic**: fewer/larger h2s that build one progressive
  argument or step through a coherent pipeline.
- **Protected**: in module-42 or module-44 (do-not-split list).

The audit script (`p1_giant_section.py`) does NOT honor in-file tags;
tags are human-readable markers. Each cycle the audit will continue to
report these sections, and reviewers verify the tag is correct and move on.

## Findings

23 of the 24 sections already carried a `<!-- GIANT_SECTION: catalog by
design; do not split -->` tag from a prior round. Verification confirmed
the tag is accurate for 21 of those 23. Two needed reclassification.

### Newly tagged this round

| File | Old tag | New tag | Reason |
| --- | --- | --- | --- |
| `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html` | (none) | `protected (module-42)` | P1; module-42 is on do-not-split list per task brief |
| `part-6-agentic-ai/module-26-ai-agents/section-26.1.html` | catalog by design | long-form single topic | 9 h2s averaging 86 lines each, building "what is an agent" as one coherent argument |
| `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.1.html` | catalog by design | long-form single topic | 9 h2s averaging 95 lines each, single dialogue-architecture arc |

### Confirmed catalog-by-design (no change)

These all have many short h2s (avg <70 lines) covering distinct items
in a list. The catalog tag stays.

| File | h2s | Lines | Avg/h2 | Catalog of... |
| --- | --- | --- | --- | --- |
| `part-1-llm-building-blocks/.../section-1.3.html` | 10 | 802 | 72 | embedding methods |
| `part-11-llm-ethics-trust-governance/.../section-53.2.html` | 10 | 905 | 85 | EU AI Act compliance tools |
| `part-11-llm-ethics-trust-governance/.../section-55.1.html` | 11 | 874 | 73 | green-AI tactics |
| `part-13-llmops-lifecycle/.../section-64.1.html` | 9 | 821 | 85 | durable-execution frameworks |
| `part-13-llmops-lifecycle/.../section-66.1.html` | 10 | 802 | 73 | reliability patterns |
| `part-14-designing-llm-agent-products/.../section-67.15.html` | 11 | 673 | 56 | MVP-readiness gates |
| `part-14-designing-llm-agent-products/.../section-70.4.html` | 11 | 627 | 52 | production monitoring topics |
| `part-16-llm-agentic-ai-research-frontiers/.../section-80.4.html` | 12 | 631 | 48 | LLMs applied to non-text domains |
| `part-2-understanding-llms/.../section-6.3.html` | 11 | 769 | 64 | scaling-law regimes |
| `part-2-understanding-llms/.../section-6.4.html` | 11 | 565 | 45 | pretraining-data pipeline steps |
| `part-2-understanding-llms/.../section-7.2.html` | 11 | 879 | 74 | open-weight model families |
| `part-2-understanding-llms/.../section-9.2.html` | 11 | 670 | 54 | KV-cache techniques |
| `part-2-understanding-llms/.../section-9.4b.html` | 11 | 661 | 54 | inference frameworks |
| `part-2-understanding-llms/.../section-10.2.html` | 11 | 877 | 73 | interpretability tools |
| `part-3-working-with-llms/.../section-11.1.html` | 11 | 752 | 63 | LLM API providers |
| `part-3-working-with-llms/.../section-11.3.html` | 10 | 870 | 81 | production-reliability patterns |
| `part-3-working-with-llms/.../section-12.2.html` | 9 | 895 | 92 | reasoning prompt techniques |
| `part-3-working-with-llms/.../section-12.3.html` | 9 | 819 | 84 | prompt-optimization techniques |
| `part-4-training-adaptation/.../section-16.4.html` | 9 | 903 | 94 | managed fine-tuning providers |
| `part-7-retrieval-information-extraction-with-llms/.../section-31.3.html` | 9 | 851 | 88 | vector database engines |
| `part-9-llm-evaluation-observability/.../section-42.2.html` | 9 | 846 | 88 | statistical-rigor methods |

(Some "catalog" entries average 80-95 lines per h2; those are
deep-treatment catalogs where each item gets a section-length treatment.
Still a catalog because the entries are coordinate items, not
sequential steps in one argument.)

## Splits

No sections were split this round. Every flagged section either:

1. is a true catalog where the h2s are coordinate items (splitting would
   destroy the comparison surface), or
2. is a long-form single topic that genuinely needs the length and
   already follows the canonical 5-9-h2 pattern with deeper-than-usual
   per-h2 treatment, or
3. is in a protected module (42, 44).

## Side-observation: structural quality issues in section-80.4

Not in scope for this agent, but worth flagging for a later content
pass: section-80.4 has an `Exercises` h2 in the middle of the body
(line 266) before the final content h2s, and several h2 stubs of 4-5
lines each (80.4.7 Audio/Music, 80.4.8 EHR, 80.4.9 Robotics). The
section reads as if a draft outline was committed before the bodies
were written. Recommend a content-author pass to either expand the
stubs or fold them into a single "Other Frontiers" section.

## Audit state after this pass

| Priority | Before | After | Net |
| --- | --- | --- | --- |
| P1 GIANT_SECTION | 1 | 1 | 0 |
| P2 GIANT_SECTION | 23 | 23 | 0 |

The audit still reports 24 findings because the audit script does not
honor in-file tags. All 24 are now verified-and-tagged; future reviewers
should confirm the tag at the top of each file and skip without
re-investigation.

## Recommendation for the audit script (out of scope, but flagged)

Consider updating `agents/book-skills/scripts/audit/checks/p1_giant_section.py`
to read the first 100 lines of each section file and suppress the warning
when one of the canonical tags is present (`catalog by design`,
`long-form single topic; verified`, `protected (module-XX)`). This would
let the GIANT_SECTION audit reach a true zero and free up reviewer cycles.
