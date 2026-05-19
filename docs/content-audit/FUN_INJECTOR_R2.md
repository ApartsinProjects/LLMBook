# Fun Injector R2 — 34-fun-injector cycle-B run

**Date:** 2026-05-19
**Agent:** 34-fun-injector
**Branch:** v2.0
**Total sections touched:** 8 new fun-notes added (R2)

## Summary

R1 had already covered Parts 9-16 thoroughly: 174 of 183 in-scope sections
(modules 42-83, excluding tools-of-the-trade) had at least one fun-note.
The remaining 9 sections without fun-notes were all in tools-of-the-trade
modules (56 and 61) which are out of scope per CONTENT_GUIDELINES.

R2 therefore focused on the second-pass goal: raising selected sections
from 1 fun-note to 2, picking dense technical territory where humor
genuinely aids learning. Each pick targeted a different region and
humor style.

All inserts use the canonical `<div class="callout fun-note">` format
with a `<div class="callout-title">` of "Fun Fact", "Mental Model",
"Did You Know", or "Trivia". No em dashes. Each fun-note placed after a
concept has been explained, never inside math derivations or procedural
code blocks. None duplicate an existing fun-note in the same section.

---

## R2 Inserts

### 1. `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1a.html`
**Concept illuminated:** Prompt injection as the SQL injection of the LLM era,
with the humbling difference that SQL had parameterized queries within a
generation and LLMs still rely on defense in depth + crossed fingers.
**Inserted:** After "indirect injection" paragraph, before instruction hierarchy.
**Tone:** Mental Model.

### 2. `part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.5.html`
**Concept illuminated:** Horizontal scope = four walls of a house with no
roof, ugly tin-shack vertical slice is the only structure that ships dry.
**Inserted:** After "Christmas tree anti-pattern" intro, before five-layers.
**Tone:** Mental Model.

### 3. `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.5.html`
**Concept illuminated:** H100 hourly rent maps to a senior staff engineer's
hourly rate; every co-design decision is a salary-burn decision in disguise.
**Inserted:** After MoE asymmetry paragraph, before speculative decoding section.
**Tone:** Mental Model.

### 4. `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.2.html`
**Concept illuminated:** Reasoning models bill per thought; flipping
`reasoning_effort: high` to default can triple the monthly bill overnight.
**Inserted:** End of test-time compute economics subsection, before scaling-axis table.
**Tone:** Did You Know.

### 5. `part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.3.html`
**Concept illuminated:** Yes-man simulator collapse — RLHF training that makes
Claude pleasant in production makes it disastrous as an adversarial user,
because it has been deeply taught that the human is always right.
**Inserted:** End of yes-man collapse paragraph, before loop collapse.
**Tone:** Trivia.

### 6. `part-14-designing-llm-agent-products/module-67-ideation/section-67.9.html`
**Concept illuminated:** Traditional QA tests a value, AI QA tests a
distribution at 0.7 kappa — the gap between "works on my laptop" and
"works for 50,000 users" is a probability claim about the same model.
**Inserted:** After key insight on probabilistic correctness, before human-AI UX section.
**Tone:** Mental Model.

### 7. `part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.1.html`
**Concept illuminated:** Exactly-once semantics has been a holy grail
since the 1980s and remains mythological in pure form; Temporal's trick
is at-least-once activity + once-only commit, accepted because
"approximately once" is 50x better than "we hope the cron job ran".
**Inserted:** Before "Temporal: Infrastructure-Level Durability" h2, after key insight.
**Tone:** Trivia.

### 8. `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/section-81.4.html`
**Concept illuminated:** The agency ladder reads like SAE driving levels —
L2 ships, L5 is "five years away" and has been for ten; the LLM L2-to-L3
boundary is the one that actually moves, and it is where lawyers and
SRE teams arrive together at 3 a.m.
**Inserted:** After L4 self-modifying agents description, before key insight.
**Tone:** Mental Model.

---

## Final tally

- 8 additional sections received a second fun-note
- 0 em dashes used in any fun-note (project style rule)
- 0 sections now exceed the 2-per-chapter cap (one previously at 3
  flagged but not touched, see below)
- All inserts placed after concept introduction; none inside procedures,
  math derivations, or warning callouts
- 8 distinct humor styles spread across Parts 9, 10, 12, 13, 14, 16

## Style notes

Mix of mental models (5: prompt injection as SQL, horizontal scope as
four-walls, H100 as engineer hourly rate, distribution-vs-value testing,
SAE driving levels), witty trivia (2: yes-man simulators, exactly-once
semantics), and one Did-You-Know (reasoning-effort billing). No two
adjacent sections reuse the same humor pattern.

## Pre-existing audit issues observed (not fixed by R2)

- `section-67.11.html` already has 3 fun-notes (over cap). This is a
  pre-R2 condition; R2 did not touch the section. Future audit pass
  should rank the three and keep the strongest two.
- `section-62.2.html` has 2 fun-notes from R1; the second is solid
  ("git for prompts and your sanity") and was not modified.
- `section-65.5.html` had a stale-feeling fun-note about Google standby
  TPU pods; left in place because the cold-start trade-off it teaches
  is still accurate as of 2026.

## Sections deliberately skipped

- All tools-of-the-trade modules (45, 51, 56, 61, 71, 79, 83): reference-
  style by design, per agent brief.
- `module-56-responsible-ai-tools/*` and `module-61-scale-tools/*`:
  the 9 sections in scope-but-without-fun-notes all fall here. Skipped
  per CONTENT_GUIDELINES.
- Sections with 2 fun-notes already (e.g., 70.4, 70.6, 49.5, 53.4,
  62.2): the agent's max-2 cap blocks further additions.
- Section 82.5 (closing chapter of the book): deeply reflective text; a
  third fun-note would undercut the deliberate tone shift.
- Tax / legal regulatory dense paragraphs in Parts 11 and 15: the
  existing fun-note in each section was deemed sufficient; humor inside
  regulatory specifics risks misleading practitioners.

## Cycle-B overlap discipline

Stayed clear of:
- Figure captions (39-figure-fact-checker territory)
- Long dense paragraphs that need restructuring (05-cognitive-load territory)
- Standalone readability fixes (21-self-containment territory)
- New why-explanations or worked examples (02/06 territory)

R2 added 8 callouts only, no inline humor changes, no prose restructuring.
