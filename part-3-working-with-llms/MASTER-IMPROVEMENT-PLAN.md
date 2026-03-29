# Part III Master Improvement Plan

**Date:** 2026-03-26
**Source Reports:** phase1-3-combined-report.md, phase4-12-combined-report.md
**Scope:** Modules 09, 10, 11 (12 HTML sections)

---

## Consolidated Findings (De-duplicated)

The two reports collectively identify 80 findings. After de-duplication, 52 unique action items remain. Duplicates removed:
- "Missing Gemini function calling" (Report 1 #2, Report 2 #25 partial overlap)
- "Multimodal API coverage" (Report 1 #13, Report 2 #34)
- "Section 11.1 opening needs a hook" (Report 1 implied in #4, Report 2 #2)
- "Paper Spotlight callouts" (Report 1 implied, Report 2 #11)
- "Where This Leads Next boxes" (Report 1 implied, Report 2 #33)
- "Prompt technique decision flowchart" (Report 1 implied in #5, Report 2 #16)
- "Semantic cache duplication" (Report 1 #3, Report 2 #38 related)
- "LLMLingua citation update" (Report 1 #7, Report 2 #40)

---

## Priority Tiers and Action Plan

### BLOCKING (Must fix before publication)

| # | Finding | Section | Action |
|---|---------|---------|--------|
| B1 | Quiz count is 5, not 6 in Section 13.2 | 11.2 | Add one quiz question at Apply/Evaluate level on embedding model selection |
| B2 | Missing Gemini function calling example | 9.2 | Add a Gemini function_declarations code example |
| B3 | Semantic cache code duplicated between 9.3 and 11.4 | 9.3, 11.4 | Keep implementation in 9.3; replace 11.4 code with cross-reference and cost-optimization focus |

### HIGH (Significant quality gaps)

| # | Finding | Section | Action |
|---|---------|---------|--------|
| H1 | No AWS Bedrock code example | 9.1 | Add a boto3 Bedrock snippet (10-15 lines) |
| H2 | Step-back prompting underdeveloped | 10.2 | Expand with a two-phase code snippet |
| H3 | Missing few-shot CoT code | 10.2 | Add 2-3 exemplar reasoning chain example |
| H4 | LLMLingua has no code example | 10.4 | Add pip install + compression call with token counts |
| H5 | BAML Python integration missing | 11.5 | Add pip install, compilation, and Python calling code |
| H6 | Section 11.1 opens like API docs, not a story | 9.1 | Rewrite Big Picture with a narrative hook (cost/failure scenario) |
| H7 | No decision flowchart for prompt techniques | 10.2 | Add SVG decision flowchart |
| H8 | No "Paper Spotlight" callouts | 10.2, 10.3, 11.1 | Add Paper Spotlight boxes for Wei, Kojima, Wang, Yao, Shinn, Khattab |
| H9 | No "Where This Leads Next" at module endings | 9.3, 10.4, 11.5 | Add forward-looking callout boxes |
| H10 | Missing cross-references to Part I and Part II | 11.2, 9.1 | Add bridge paragraphs referencing prerequisite modules |
| H11 | No reasoning models coverage (o3, R1) | 10.2 | Add subsection on prompting vs. native reasoning models |
| H12 | No MCP / tool-use standards mention | 9.2 | Add callout about emerging MCP standard |
| H13 | A/B testing promised but not implemented | 10.4 | Add minimal A/B test skeleton or remove from learning objectives |

### MEDIUM (Meaningful enhancements)

| # | Finding | Section | Action |
|---|---------|---------|--------|
| M1 | No "modify and observe" exercises | 09, 10, 11 | Add one per module |
| M2 | Aha-moment: CoT as "scratchpad/working memory" | 10.2 | Add dedicated Key Insight callout |
| M3 | Aha-moment: cost of NOT using structured output | 9.2 | Add malformed JSON failure scenario before solutions |
| M4 | Aha-moment: prompt injection is unsolvable in principle | 10.4 | Expand the "No Complete Defense" callout with SQL injection analogy |
| M5 | Misconception risk: ToT practical for production | 10.2 | Move cost/practicality warning before the ToT code |
| M6 | Missing forward reference from 9.2 to BAML (11.5) | 9.2 | Add one-sentence forward reference |
| M7 | Missing LLMLingua connection from 10.4 to 11.4 | 10.4 | Add cross-reference |
| M8 | Semantic cache threshold tuning guidance | 9.3 | Add calibration note |
| M9 | Instructor retry on validation failure demo | 9.2 | Add short code example |
| M10 | Multimodal API mention | 9.1 | Add callout noting image input capabilities |
| M11 | Module 11 self-declaration of novelty | 11.1 | Add callout: "This module teaches when NOT to use LLMs" |
| M12 | Pareto frontier gentle introduction | 11.4 | Add one-paragraph intuition before the diagram |
| M13 | Pricing volatility disclaimer | 9.1, 11.4 | Add notes about pricing date and checking current rates |
| M14 | Data privacy as a decision factor | 11.1 | Add mention of GDPR/HIPAA constraints |
| M15 | DSPy version compatibility note | 10.3 | Add pip install version note |
| M16 | TTFT defined before first use | 9.1 | Move definition to first occurrence |
| M17 | XGBoost deprecated parameter | 11.1 | Remove `use_label_encoder=False` |
| M18 | Structured output vs. function calling distinction | 9.2 | Add prominent clarification callout |
| M19 | LLM Integration Stack mnemonic (Connect, Control, Combine) | Part III intro | Add to module index pages |

### LOW (Polish)

| # | Finding | Section | Action |
|---|---------|---------|--------|
| L1 | Batch API savings not quantified | 9.1 | Add dollar calculation |
| L2 | No concrete CoT failure case | 10.2 | Add example of CoT hurting on simple tasks |
| L3 | APE section too brief | 10.3 | Expand or merge into OPRO comparison |
| L4 | Ensemble arbitration LLM call not shown | 11.3 | Add the actual arbitration API call |
| L5 | Confidence threshold calibration | 11.3 | Add validation set guidance |
| L6 | OpenTelemetry mention | 9.3 | Add brief mention |
| L7 | Complete production system prompt | 10.1 | Add combined five-layer example |
| L8 | Jinja2 mention for templates | 10.1 | Add one-sentence pointer |
| L9 | CSS duplication across files | All | Extract to shared stylesheet (deferred) |
| L10 | Voice inconsistency (we vs. you) | All | Standardize (deferred, needs full pass) |

---

## Execution Order

1. BLOCKING fixes first (B1, B2, B3)
2. HIGH fixes by section order (H1 through H13)
3. MEDIUM fixes integrated during section edits
4. LOW fixes as time permits
5. Write REMAINING-WORK.md for deferred items

---

## Success Criteria

- All 12 sections have exactly 6 quiz questions
- All promised code examples exist (Gemini, Bedrock, few-shot CoT, LLMLingua, BAML)
- No duplicated code blocks between sections
- Every module ending has a "Where This Leads Next" box
- At least 4 Paper Spotlight callouts across Part III
- Decision flowchart present in Module 10
- One "modify and observe" exercise per module
- Cross-references to Part I/II prerequisites where relevant
