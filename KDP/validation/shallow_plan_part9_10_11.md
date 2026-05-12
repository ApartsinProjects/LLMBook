# Shallow Audit Plan: Parts IX, X, XI

**Total findings: 87** (33 structural + metadata bugs + 26 shallow-content + 28 GOOD assessments)

## DOMINANT ISSUE: Template "Section X.Y" placeholders in module-29/30 (9 cases)

| File | Bare text | Intended |
|---|---|---|
| 29.2 prereq | "the Section 27.1 are essential" | "the evaluation metrics from Section 27.1 are essential" |
| 29.4 prereq | "the Section 27.6 that support compliance monitoring" | "the audit tooling in Section 27.6" |
| 29.5 prereq | "Section 27.1" (bare) | "the evaluation framework from Section 27.1" |
| 30.1 epigraph | "Strategy without execution is a Section 29.2" | "...is a hallucination" |
| 30.2 prereq + Big Picture | "Section 27.1...", "Section 29.2 risk" | concept names + links |
| 30.3 prereq | "Section 27.1...", "Section 9.1..." | concept names |
| 30.5 prereq | "the Section 9.1 that reduce hardware requirements" | "the inference optimization techniques from Section 9.1" |

**Same systemic bug as Parts I, II+III, V+VI.** Book-wide grep needed.

## SECONDARY: Wrong sub-heading number prefixes

| File | Wrong | Correct |
|---|---|---|
| 29.1, 29.9 | "32-1-1", "32.9.1.1" | "29-1-1", "29.9.1.1" |
| 31.1, 31.3 | "18.1.1.1", "18.3.1.1" | "31.1.1.1", "31.3.1.1" |
| 32.3 | "34.3.2.1" | "32.3.2.1" |
| 33.2 | "36.2.2.1" | "33.2.x.x" |
| 34.3 | "38.3.1.1" through "38.3.4.1" | "34.3.x.x" |
| 34.4 | "38.4.2.1" through "38.4.7.2" | "34.4.x.x" |

These were renumbered for body text but heading IDs/anchors not updated. Need follow-up renumber pass on `<h3>`/`<h4>` numeric prefixes.

## TERTIARY: 4 missing figure images (sections 33.4, 33.5, 33.6, 33.7)

Captions present but no `<img>` tag. Renders as blank space + floating caption. Production-critical.

## OTHER STRUCTURAL BUGS

- 29.10: Code Fragment label "29.11.1" (off by one)
- 29.11: HTML `<title>` says "Section 29.10"
- 29.12: part-label says "Part X: Frontiers" (should be Part IX)
- 31.3: Misplaced SentenceTransformer code unrelated to section topic
- 31.4: Code Fragment 31.4.1 caption describes "tokenization pipeline" but code implements attention rollout
- 32.10: Malformed `2&gt;1. The Universal Recipe` instead of `<h2>` heading
- 30.2 table: "Productsas of 2026)" missing space

## SHOPPING-LIST findings

- 29.1 OWASP Top 10 table (10 threats, no worked attack scenarios for 7 of 10)
- 29.4 GDPR articles table (Art.17 right-to-erasure not explained)
- 29.5 governance frameworks (NIST AI RMF vs ISO 42001 not differentiated)
- 29.7 weight editing (LOKA, representation surgery name-dropped)
- 30.4 vector DB comparison (5 DBs, single-phrase descriptions)

## MISSING-INTUITION

- 29.6 DP-SGD epsilon/delta meaning never explained
- 32.3 SSM ZOH discretization mathematics without intuition
- 32.4 Ha & Schmidhuber V/M/C framework needs before/after framing
- 33.4 Intent + Evidence Bundle problem statement weak

## MISSING-FAILURE-MODE

- 29.7 gradient ascent → catastrophic forgetting
- 31.1 attention pattern taxonomy breakdown (sink heads, dual-use)
- 31.4 attention rollout assumptions (linear combination, head equality)
- 32.4 video world model failures (physics drift, object permanence)
- 33.3 risk misclassification (low-risk-looking but high-consequence delayed-detection)
- 34.4 A/B test novelty effect bias

## UNJUSTIFIED CLAIMS

- 30.7 "60-80% cost reduction from cascade routing" — no derivation
- 30.5 "ROCm/oneAPI may require additional engineering" — no specifics
- 30.3 10% productivity gain vs 20-55% study figures — gap not reconciled
- 32.4 video model claims need failure mode coverage

## SECTIONS RATED EXEMPLARY

29.2, 29.8, 31.2, 32.1, 32.5, 33.1, 34.3 — exemplary depth, problem-first framing, four-question coverage, worked examples, explicit failure modes. Use as internal templates.

## CROSS-CUTTING

- 29.7 SAE and 32.7 SAE: same concept, no cross-reference
- 30.7 cascade routing and 32.9 tool economy: same engineering problem, no cross-reference
- All module-30 code blocks: HTML pre-block indentation rendering shows nested methods at wrong levels (pre-existing artifact)
