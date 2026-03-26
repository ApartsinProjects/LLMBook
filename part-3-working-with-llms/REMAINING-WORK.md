# Part III Remaining Work

**Date:** 2026-03-26
**Context:** Items from the MASTER-IMPROVEMENT-PLAN.md that were not applied in this pass, with justification.

---

## Applied Summary

### BLOCKING (3/3 applied)
- [x] B1: Added 2 quiz questions to Section 11.2 (now has 6)
- [x] B2: Added Gemini function calling code example to Section 9.2
- [x] B3: Deduplicated semantic cache (kept in 9.3, replaced in 11.4 with cross-reference + threshold analysis)

### HIGH (11/13 applied)
- [x] H1: Added AWS Bedrock boto3 code example to Section 9.1
- [x] H2: Expanded step-back prompting with two-phase code example in Section 10.2
- [x] H3: Added few-shot CoT code example with exemplar reasoning chains in Section 10.2
- [x] H4: Added LLMLingua pip install + compression code example in Section 10.4
- [x] H5: Added BAML installation/compilation steps in Section 11.5
- [x] H6: Rewrote Section 9.1 Big Picture with narrative hook (cost overrun war story)
- [x] H7: Added prompt technique decision flowchart (SVG) to Section 10.2
- [x] H8: Added 3 Paper Spotlight callouts (Wei et al., Wang et al., Khattab et al.)
- [x] H9: Added "Where This Leads Next" boxes at ends of Sections 9.3, 10.4, 11.5
- [x] H10: Added cross-reference to Part I/II prerequisites in Section 11.2
- [x] H11: Added reasoning models note (o3, o4-mini, DeepSeek R1) in Section 10.2 flowchart

### HIGH (2/13 not applied)
- [ ] H12: MCP standard mention in Section 9.2 (APPLIED as an MCP callout near function calling section)
- [ ] H13: A/B testing skeleton code or learning objective removal in Section 10.4

**H13 Justification:** Adding a full A/B testing code skeleton requires careful design (random assignment, metric comparison, statistical significance) and would add 40+ lines to an already dense section. The better approach is either (a) adding it as a standalone subsection or (b) removing the claim from the learning objectives. Both options need editorial decision that goes beyond code insertion.

### MEDIUM (15/19 applied)
- [x] M1: "Modify and Observe" exercises added to 9.1, 10.2, 11.1
- [x] M2: CoT "scratchpad/working memory" Aha Moment callout in 10.2
- [x] M3: Malformed JSON failure scenario callout in 9.2
- [x] M4: Prompt injection fundamental impossibility explanation in 10.4
- [x] M5: ToT misconception warning moved before code in 10.2
- [x] M6: Forward reference from 9.2 to BAML (11.5)
- [x] M7: LLMLingua to 11.4 cross-reference in 10.4
- [x] M8: Semantic cache threshold tuning guidance in 9.3
- [x] M10: Multimodal API callout in 9.1
- [x] M11: Module 11 distinctiveness declaration in 11.5
- [x] M12: Pareto frontier gentle introduction in 11.4
- [x] M13: Pricing volatility disclaimer in 9.1
- [x] M14: Data privacy as decision factor in 11.1
- [x] M15: DSPy version compatibility note in 10.3
- [x] M17: Removed deprecated `use_label_encoder=False` from 11.1 and 11.2
- [x] M18: Structured output vs function calling distinction callout in 9.2
- [x] MCP callout added to 9.2 (H12)

### MEDIUM (4/19 not applied)
- [ ] M9: Instructor retry validation failure demo (Section 9.2)
- [ ] M16: TTFT definition before first use (Section 9.1)
- [ ] M19: LLM Integration Stack mnemonic (Connect, Control, Combine) on index pages

**M9 Justification:** Adding a retry demo that deliberately triggers a validation error requires careful setup (a Pydantic model with constrained ranges, a prompt that generates out-of-range values). The existing note callout about retries is adequate for now; a future pass can add the code example.

**M16 Justification:** The TTFT abbreviation appears in a Key Insight callout that already expands the term on first use. The report flagged a potential ordering issue, but on closer inspection the current ordering is correct (the abbreviation is expanded parenthetically on its first occurrence).

**M19 Justification:** Adding mnemonics to index pages requires reading and editing the three `index.html` files for Modules 09, 10, and 11. This is a visual/branding improvement that does not affect section content and can be done in a polish pass.

### LOW (0/10 applied)
None of the LOW priority items were applied. These are polish-level improvements:
- L1: Batch API savings calculation (9.1)
- L2: Concrete CoT failure case (10.2)
- L3: APE section expansion (10.3)
- L4: Ensemble arbitration LLM call (11.3)
- L5: Confidence threshold calibration (11.3)
- L6: OpenTelemetry mention (9.3)
- L7: Complete production system prompt (10.1)
- L8: Jinja2 mention for templates (10.1)
- L9: CSS extraction to shared stylesheet (all files)
- L10: Voice consistency (we vs. you) standardization

**Justification:** LOW items are polish improvements that do not affect pedagogical completeness or accuracy. They should be addressed in a subsequent polish pass. L9 (CSS extraction) in particular is a structural change that affects all 12 files and should be done as a dedicated refactoring task.

### Items from Phase 4-12 Report Not Addressed
- Cognitive overload in Section 10.3 (splitting into 10.3 + 10.5): This is a structural reorganization requiring new file creation, navigation link updates, and index page changes. Not appropriate for a content improvement pass.
- CSS duplication: Same as L9 above.
- Voice consistency: Same as L10 above.
- Code output JSON syntax highlighting: CSS enhancement, deferred.
- Quiz answer length reduction with toggle: Requires HTML/CSS structural changes across all files, deferred.
- Missing observability pipeline diagram, latency bar chart, TCO pie chart: New SVG diagrams flagged in chapter plans. These require dedicated design work.

---

## Recommended Next Steps

1. **Editorial decision on H13:** Remove A/B testing from Section 10.4 learning objectives, or add a minimal A/B skeleton.
2. **CSS extraction (L9):** Create `part3-styles.css` and replace inline styles across all 12 section files.
3. **LOW items pass:** Address L1 through L8 in a targeted pass.
4. **New SVG diagrams:** Create the three missing diagrams flagged by chapter plans.
5. **Section 10.3 split consideration:** Evaluate whether the cognitive load warrants splitting.
