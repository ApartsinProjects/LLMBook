# Shallow Audit Plan: Parts II and III

**Scope:** sections 6.1-6.9, 7.1-7.4, 8.1-8.6, 9.1-9.7 (Part II) and 10.1-10.4, 11.1-11.5, 12.1-12.6 (Part III)
**Date:** 2026-05-12
**Total findings: 21** (under 120 cap)

---

## DOMINANT ISSUE: Unreplaced "Section X.Y" template placeholders

**13 of 21 findings (HIGH priority).** A previous auto-linker pass replaced concept-name strings with the section number where they're canonically explained, but never substituted back the actual concept name. Result: prose reads "Temperature scales the logits before Section 4.1" instead of "before the softmax operation".

| # | File | Placeholder | Should read |
|---|---|---|---|
| F3 | section-7.1 | "extended Section 8.1 at inference time" | "extended chain-of-thought reasoning at inference time" |
| F8 | section-10.1 | "Temperature scales the logits before Section 4.1" | "...before the softmax operation" |
| F9 | section-10.1 | "Built-in Section 8.1 reasoning" | "Built-in chain-of-thought reasoning" |
| F13 | section-10.4 | "running its own Section 8.1 automatically" | "running its own chain-of-thought trace automatically" |
| F14 | section-10.4 | "an internal Section 8.1 (the 'thinking' tokens)" | "an internal scratchpad of reasoning tokens" |
| F15 | section-11.1 | "trying Section 8.1 prompting" | "trying chain-of-thought prompting" |
| F16 | section-11.3 | "basic and Section 8.1 prompting" | "basic and chain-of-thought prompting" |
| F18 | section-12.2 | "Section 4.1 library" (for embeddings) | "sentence-transformers library" |
| F20 | section-12.5 | "Section 4.1 models" (spaCy) | "transformer-based models (en_core_web_trf)" |
| F21 | section-12.5 | "Section 32.2 risk" (table label) | "Hallucination risk" |

**Action:** book-wide grep for `Section \d+\.\d+` outside `<a>` tags and outside explicit "see Section X.Y" constructs. Replace each with intended concept name + hyperlink to canonical section.

---

## SECONDARY ISSUE: HTML pre-block indentation rendering artifact (4 cases)

Python code blocks where all content after a certain line shows extra indentation, making class methods look like nested closures. The Python source runs correctly (outputs are right) but copy-paste from rendered HTML produces IndentationError.

| # | File | Affected fragment |
|---|---|---|
| F7 | section-9.7 | `arithmetic_intensity()` — return + print indented inside elif branch |
| F11 | section-10.2 | Instructor shortcut — client/contact appear inside `Contact` class body |
| F12 | section-10.3 | `CircuitBreaker` — class + methods appear inside `class CircuitState(Enum)` |
| F19 | section-12.3 | `TriageRouter` — `fit`/`classify` appear nested inside `__init__` |

**Action:** Fix HTML pre-block indentation in build pipeline (likely a stray leading-whitespace issue in source HTML files).

---

## TERTIARY: Code Fragment numbering artifacts

| # | File | Issue |
|---|---|---|
| F2 | section-6.9 | Code fragment labels say "11.5.4-11.5.6" but file is section-6.9. Should be "6.9.1-6.9.3". |
| F10 | section-10.2 | Two different code fragments both labeled "10.2.5" in same prose sentence. |

---

## CONTENT FINDINGS

### F1 (MEDIUM) — section-6.9 — TransformerEncoder used for causal LM
Uses `nn.TransformerEncoderLayer` for GPT-style causal LM with explicit causal_mask. Misleading: production uses `nn.TransformerDecoder`.
**Action:** ADD-FAILURE-MODE-NOTE explaining the simulation pattern.

### F4 (MEDIUM) — section-7.3 — Three PRM training strategies
Human annotation, Monte Carlo estimation, automated verification — each described in 1-2 sentences with no code.
**Action:** NEW-WORKED-EXAMPLE — show Monte Carlo labeling: "rollout 8 trajectories; step gets correctness=k/8" + cross-ref to section-8.3.

### F5 (LOW) — section-9.6 — Reasoning model paragraph (o-series, R1, Gemini, Claude)
Names 4 model families in ~80 words. Bridge section, appropriate as a survey but should anchor each name to its canonical home.
**Action:** add hyperlinks to section-7.3 and section-8.2.

### F6 (LOW) — section-9.6 — PRM bridge section
Discusses PRMs in prose only; full treatment is in section-8.3.
**Action:** CROSS-REF-TO-8.3 — "see Section 8.3 for full PRM training pseudocode".

### F17 (HIGH) — section-11.4 — Sandwich defense code missing
Heading "The Sandwich Defense" introduces concept but the supporting code block shown is actually the LLMLingua compression snippet. Sandwich defense itself has no code.
**Action:** DEEPEN-HERE — add system-prompt template showing `[INSTRUCTIONS] + [USER INPUT] + [INSTRUCTIONS REPEATED]` pattern with rationale (recency bias).

---

## SECTIONS RATED GOOD (35 of 38 reviewed)

Module 6 (all sections), Module 7 (all sections — minus F3 placeholder), Module 8 (all), Module 9 (all — minus F5/F6 minor bridge), Modules 10-12 (all content — minus placeholders).

---

## OVERALL ASSESSMENT

Parts II and III are in strong shape. The dominant problems are NOT shallow content — they are mechanical artifacts:

1. **Unreplaced section-placeholder text** (10 instances, 7 files) — highest priority because broken inline prose
2. **HTML pre-block indentation** (4 sections) — code unrunnable if copied
3. **Code fragment numbering mismatches** (2 sections)

**No genuine SHOPPING-LIST or MISSING-INTUITION failures of substance found** in the technical content. The one real depth gap is F4 (PRM training strategies in section-7.3 lack worked numeric trace).
