# Section Audit, Parts 10-12 of LLMBook

**Date:** 2026-05-16
**Generator:** `scripts/_audit_parts_10_12_5dim.py` (read-only)

Audit covers five quality dimensions across every `section-*.html` file in Parts 10, 11, and 12:

1. **Uniform format**, DOCTYPE, head-asset links, breadcrumb, page-current, chapter-nav, footer, title-tag prefix.
2. **Working links**, internal cross-refs (relative hrefs) and image `src` attributes resolved against the filesystem.
3. **Section naming**, single `<h1>`, `<h2>` numbering of the form `X.Y.Z` matching the section's chapter and section number.
4. **Captions**, every `<figure>` has a `<figcaption>`, every `<table>` has either a `<caption>` or a `<div class="comparison-table-title">` sibling, every `<img>` has an `alt`.
5. **Styles**, every `callout` div uses a class from the canonical palette of 22 names.

**Files audited:** 111 section HTML files.

**Scope:**
- `part-10-idea-to-product/` modules 40-50 (39 sections).
- `part-11-applications-across-industries/` modules 51-60 (49 sections).
- `part-12-frontiers/` modules 61-65 (23 sections).

## Headline finding

Styles (Dimension 5) are clean: every callout in 111 sections uses a class from the canonical 22-name palette (735 callouts checked). The four other dimensions surface 138 findings, and **two cross-cutting root causes account for almost all of them**:

- **Legacy renumbering cruft** (h2 IDs like `27.x`, `31.x`, `33.x`, `35.x`, `36.x`-`42.x` from a previous monolithic ToC) is preserved in `52.7`, `53.7`, `55.7`, `58.2`, `59.2`, every `61.x`, every `62.x`, and four `48.x` sections. This drives **25 of the 25** "h2 wrong section prefix" findings, 11 of the 11 title-prefix mismatches, and a large fraction of the broken cross-references (legacy hrefs like `section-31.5.html` and `section-33.10.html` that no longer exist).
- **House-style drift in h2 numbering**, split between three flavours: "Exercises" (22 sections, intentionally unnumbered, like "Further Reading"), Pattern-A omnibus splits using `1. Foo / 2. Bar / 3. Baz` (8 sections, mostly Part 10), and prose-style h2 with no number at all (39 sections, almost all of Part 11). All three are visually consistent within their own chapter, but together they make the book inconsistent at the part level. Parts 1-9 settled on `X.Y.Z Foo`, so the recommendation is to converge on that form for v11.

After removing those two systemic causes, the residue is small: a handful of genuinely broken cross-refs to renamed/missing files (canonical-path drift on `module-23-rag-fundamentals`, `module-31-multimodal`, `module-35-llmops-mlops`, `module-37`, `module-38`, `module-48-shipping-scaling`), 2 raw `<table>` tags lacking captions, and zero `<h1>` problems (every section has exactly one).

## Per-part fingerprint

| Part | Sections | Format | Links | Naming | Captions | Styles | Dominant root cause |
|---|---:|---:|---:|---:|---:|---:|---|
| Part 10 | 39 | 1 | 7 | 35 | 1 | 0 | Pattern A `1./2./3.` h2 numbering + 4 sections in module 48 still carrying `35.x` legacy prefixes. |
| Part 11 | 49 | 5 | 14 | 47 | 0 | 0 | Legacy `27.x` / `36.x` IDs preserved inside the 5 surviving `.7` files; otherwise clean h2 prose-style numbering. |
| Part 12 | 23 | 5 | 10 | 12 | 1 | 0 | Renumbering after 33->61/62/63/64/65 left every module-62 file with old h1/title/breadcrumb mismatches and cross-refs into nonexistent `62.5`-`62.9`. |

## Cross-cutting patterns

### Legacy chapter-number prefixes still alive in renumbered files

These sections carry IDs from the pre-v9 monolithic ToC and were never re-stamped:

| File | Legacy prefix | Should be |
|---|---|---|
| `part-10/module-41/section-41.2.html` | `31.2.x` | `41.2.x` |
| `part-10/module-42/section-42.3.html` | `31.1.x` | `42.3.x` |
| `part-10/module-42/section-42.4.html` | `31.4.x` | `42.4.x` |
| `part-10/module-43/section-43.2.html` | `27.1.x` | `43.2.x` |
| `part-10/module-45/section-45.4.html` | `45.5.x` | `45.4.x` |
| `part-10/module-45/section-45.5.html` | `45.6.x` | `45.5.x` |
| `part-10/module-45/section-45.6.html` | `45.7.x` | `45.6.x` |
| `part-10/module-45/section-45.7.html` | `45.9.x` | `45.7.x` |
| `part-10/module-48/section-48.1.html` | `35.1.x` | `48.1.x` |
| `part-10/module-48/section-48.2.html` | `35.2.x` | `48.2.x` |
| `part-10/module-48/section-48.3.html` | `35.3.x` | `48.3.x` |
| `part-10/module-48/section-48.4.html` | `35.4.x` | `48.4.x` |
| `part-11/module-52/section-52.7.html` | `27.2.x` | `52.7.x` (or retire per `_section_split_plan.md`) |
| `part-11/module-53/section-53.7.html` | `27.3.x` | `53.7.x` (or retire) |
| `part-11/module-55/section-55.7.html` | `27.5.x` | `55.7.x` (or retire) |
| `part-11/module-58/section-58.2.html` | `27.6.x` | `58.2.x` (or retire) |
| `part-11/module-59/section-59.2.html` | `27.4.x` | `59.2.x` (or retire) |
| `part-12/module-61/section-61.1.html` | `33.1.x` | `61.1.x` |
| `part-12/module-61/section-61.2.html` | `33.2.x` | `61.2.x` |
| `part-12/module-61/section-61.3.html` | `33.3.x` | `61.3.x` |
| `part-12/module-61/section-61.4.html` | `33.10.x` | `61.4.x` |
| `part-12/module-62/section-62.1.html` | `33.5.x` | `62.1.x` |
| `part-12/module-62/section-62.2.html` | `33.6.x` | `62.2.x` |
| `part-12/module-62/section-62.3.html` | `33.7.x` | `62.3.x` |
| `part-12/module-62/section-62.4.html` | `33.8.x` | `62.4.x` |

All 25 cases drive both the "h2 wrong section prefix" findings in Section 3 and a large share of the "title prefix mismatch" findings in Section 1. A single mechanical pass that renumbers h2 text, `id` attributes, in-page `Section X.Y` references, `<title>`, `<meta description>`, and the `page-current` div would resolve them together.

### Module 62 cross-references to nonexistent sections

Module 62 contains only four section files (`62.1`-`62.4`), but in-section prose and `chapter-nav` blocks point to `section-62.5.html`-`section-62.9.html` that were dropped during the renumbering. Affected files:

- `section-62.1.html` claims to be 62.5 in its title and links to 62.6.
- `section-62.2.html` links to 62.5 and 62.7.
- `section-62.3.html` links to 62.8.
- `section-62.4.html` links to 62.5, 62.6, 62.7, 62.9.

These are the same renumbering symptoms as the legacy-prefix table above, just visible as broken hrefs instead of wrong-prefix h2s.

## 1. Uniform format

### title prefix mismatch (11)
- part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html
- part-11-applications-across-industries/module-52-finance-llms/section-52.7.html
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html
- part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html
- part-11-applications-across-industries/module-58-creative-industries/section-58.2.html
- part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html
- part-12-frontiers/module-61-frontier-architectures/section-61.4.html
- part-12-frontiers/module-62-frontier-theory/section-62.1.html
- part-12-frontiers/module-62-frontier-theory/section-62.2.html
- part-12-frontiers/module-62-frontier-theory/section-62.3.html
- part-12-frontiers/module-62-frontier-theory/section-62.4.html


## 2. Working links

**31 broken internal hrefs or images.**

- `../module-31-multimodal/section-31.1.html` (broken from 4 locations)
  - part-10-idea-to-product/module-43-vibe-coding/section-43.2.html
  - part-11-applications-across-industries/module-52-finance-llms/section-52.7.html
  - part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html
  - part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html
- `../../part-6-agentic-ai/module-38-agent-safety-security/index.html` (broken from 3 locations)
  - part-11-applications-across-industries/module-52-finance-llms/section-52.5.html
  - part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.1.html
  - part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.5.html
- `../../part-10-idea-to-product/module-48-shipping-scaling/section-48.1.html` (broken from 2 locations)
  - part-10-idea-to-product/module-48-shipping-deploying/section-48.2.html
  - part-10-idea-to-product/module-48-shipping-deploying/section-48.4.html
- `section-62.6.html` (broken from 2 locations)
  - part-12-frontiers/module-62-frontier-theory/section-62.1.html
  - part-12-frontiers/module-62-frontier-theory/section-62.4.html
- `section-62.5.html` (broken from 2 locations)
  - part-12-frontiers/module-62-frontier-theory/section-62.2.html
  - part-12-frontiers/module-62-frontier-theory/section-62.4.html
- `section-62.7.html` (broken from 2 locations)
  - part-12-frontiers/module-62-frontier-theory/section-62.2.html
  - part-12-frontiers/module-62-frontier-theory/section-62.4.html
- `../../part-5-retrieval-conversation/module-23-rag-fundamentals/index.html` (broken from 1 location)
  - part-10-idea-to-product/module-40-ideation/section-40.1.html
- `../module-37-safety-ethics-regulation/section-37.4.html` (broken from 1 location)
  - part-10-idea-to-product/module-41-product-management/section-41.2.html
- `../module-37-safety-ethics-regulation/section-37.2.html` (broken from 1 location)
  - part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html
- `section-42.5.html` (broken from 1 location)
  - part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html
- `../../part-12-frontiers/module-61-frontier-architectures/section-33.10.html` (broken from 1 location)
  - part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html
- `../../part-6-agentic-ai/module-38-agent-safety-security/section-25.1.html` (broken from 1 location)
  - part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.3.html
- `section-55.6.html` (broken from 1 location)
  - part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html
- `../../part-6-agentic-ai/module-29-multi-agent/index.html` (broken from 1 location)
  - part-11-applications-across-industries/module-57-manufacturing-llms/section-57.5.html
- `../../part-8-evaluation-production/module-35-llmops-mlops/index.html` (broken from 1 location)
  - part-11-applications-across-industries/module-57-manufacturing-llms/section-57.5.html
- `../module-31-multimodal/section-31.3.html` (broken from 1 location)
  - part-11-applications-across-industries/module-58-creative-industries/section-58.2.html
- `section-58.7.html` (broken from 1 location)
  - part-11-applications-across-industries/module-58-creative-industries/section-58.2.html
- `section-59.5.html` (broken from 1 location)
  - part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html
- `../../part-10-idea-to-product/module-42-strategy-prioritization/section-31.5.html` (broken from 1 location)
  - part-12-frontiers/module-61-frontier-architectures/section-61.2.html
- `../../part-10-idea-to-product/module-42-strategy-prioritization/section-31.2.html` (broken from 1 location)
  - part-12-frontiers/module-61-frontier-architectures/section-61.2.html
- `section-62.8.html` (broken from 1 location)
  - part-12-frontiers/module-62-frontier-theory/section-62.3.html
- `section-62.9.html` (broken from 1 location)
  - part-12-frontiers/module-62-frontier-theory/section-62.4.html

## 3. Section naming

**94 naming issues.** Sub-categorised below.

### "Exercises" h2 without numeric prefix (22)

`Exercises` is conventionally unnumbered across the book, like `What Comes Next` and `Further Reading`. These findings are informational only and do not need fixing if that convention holds.

- part-10-idea-to-product/module-41-product-management/section-41.2.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-43-vibe-coding/section-43.2.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.1.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.2.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.3.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.4.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.5.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.6.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.7.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-48-shipping-deploying/section-48.1.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-48-shipping-deploying/section-48.3.html: non-numbered h2: ['Exercises']
- part-10-idea-to-product/module-48-shipping-deploying/section-48.4.html: non-numbered h2: ['Exercises']
- part-11-applications-across-industries/module-52-finance-llms/section-52.7.html: non-numbered h2: ['Exercises']
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html: non-numbered h2: ['Exercises']
- part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html: non-numbered h2: ['Exercises']
- part-11-applications-across-industries/module-58-creative-industries/section-58.2.html: non-numbered h2: ['Exercises']
- part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html: non-numbered h2: ['Exercises']
- part-12-frontiers/module-61-frontier-architectures/section-61.1.html: non-numbered h2: ['Exercises']
- part-12-frontiers/module-61-frontier-architectures/section-61.2.html: non-numbered h2: ['Exercises']
- part-12-frontiers/module-61-frontier-architectures/section-61.4.html: non-numbered h2: ['Exercises']

### Pattern A `1./2./3.` h2 numbering (8)

New Pattern-A omnibus splits in Parts 10 and 11 use `1. Foo / 2. Bar / 3. Baz` rather than the older `X.Y.Z Foo` style. This is a deliberate house choice for prose-essay sections, but it is inconsistent with the older sections in the same chapters. Recommend picking one form per part for v11.

- part-10-idea-to-product/module-40-ideation/section-40.2.html: non-numbered h2: ['1. The "I Wish I Had an Intern" Filter', '2. The Manual-Handoff Spotter', '3. The Abandonment Trail']...
- part-10-idea-to-product/module-40-ideation/section-40.3.html: non-numbered h2: ['1. The Three Uncomfortable Questions', '2. Mapping Problem Shapes to LLM Capabilities', '3. One Capability Per MVP']...
- part-10-idea-to-product/module-41-product-management/section-41.3.html: non-numbered h2: ['1. Conversational UX Is Not the Default', "2. Disclosure: Showing the User What the Model Knows and Doesn't", '3. The Confidence-Calibration Curve']...
- part-10-idea-to-product/module-43-vibe-coding/section-43.3.html: non-numbered h2: ['1. The Taxonomy: Five Axes That Matter', '2. The Six Tools That Matter', '3. The Tool-Combination Pattern']...
- part-10-idea-to-product/module-44-mvp/section-44.2.html: non-numbered h2: ['1. Why Horizontal Scope Fails', '2. The Five Layers of an LLM Vertical Slice', '3. The Discipline That Holds the Slice Thin']...
- part-10-idea-to-product/module-44-mvp/section-44.3.html: non-numbered h2: ['1. The Four Pilot Signals', '2. The Sunk-Cost Failure Mode', '3. The Pivot That Works']...
- part-10-idea-to-product/module-49-post-launch-monitoring/section-49.2.html: non-numbered h2: ['1. The Five Flavors of Drift', '2. The Silent Provider Update', '3. Detecting Drift Before Users Do']...
- part-10-idea-to-product/module-49-post-launch-monitoring/section-49.3.html: non-numbered h2: ['1. The History That Made Rotation Mandatory', '2. The Four Ingredients of a Workable Strategy', '3. The Hidden Lock-In Surface']...

### Other prose-style h2 (no number, no leading digit) (39)

- part-10-idea-to-product/module-50-tools-of-the-trade/section-50.1.html: non-numbered h2: ['50.1.1.5 Text-to-app and vibe-coding platforms']
- part-11-applications-across-industries/module-51-legal-llms/section-51.1.html: non-numbered h2: ['Contract Review: Assistive, Not Autonomous', 'E-Discovery and Document Triage', 'Citation Generation, With Verification']...
- part-11-applications-across-industries/module-51-legal-llms/section-51.2.html: non-numbered h2: ['Hallucinated Precedent: The Canonical Failure', 'Privilege Leakage', 'Jurisdictional Bias']...
- part-11-applications-across-industries/module-51-legal-llms/section-51.3.html: non-numbered h2: ['The Five Principles That Have Stabilized', 'The EU AI Act for Legal-Decision Systems', 'State-Level Variation']...
- part-11-applications-across-industries/module-51-legal-llms/section-51.4.html: non-numbered h2: ['Layer 1: Source Acquisition', 'Layer 2: Verified Extraction', 'Layer 3: Retrieval With Matter-Level Access Control']...
- part-11-applications-across-industries/module-51-legal-llms/section-51.5.html: non-numbered h2: ['The 2026 Vendor Landscape, Revisited', 'Cross-References Inside This Book', 'Canonical External References']
- part-11-applications-across-industries/module-52-finance-llms/section-52.1.html: non-numbered h2: ['Equity Research Synthesis', 'Sentiment and Event Extraction', 'Code Generation for Finance Workflows']...
- part-11-applications-across-industries/module-52-finance-llms/section-52.2.html: non-numbered h2: ['Hallucinated Numbers', 'Fair Lending and Disparate Impact', 'Market Manipulation Adjacency']...
- part-11-applications-across-industries/module-52-finance-llms/section-52.3.html: non-numbered h2: ['SR 11-7 Model Risk Management', 'EU AI Act High-Risk Classification', 'FINRA and SEC Supervision Rules']...
- part-11-applications-across-industries/module-52-finance-llms/section-52.4.html: non-numbered h2: ['The Tier Framework', 'Tier 0: Decisions That Cannot Be LLM-Mediated', 'Tier 1: LLM as Drafting Assistant']...
- part-11-applications-across-industries/module-52-finance-llms/section-52.5.html: non-numbered h2: ['The 2026 Vendor Landscape', 'Cross-References Inside This Book', 'Canonical External References']
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.1.html: non-numbered h2: ['Ambient Clinical Documentation', 'Clinical Decision Support (Assistive Only)', 'Patient-Facing Triage and Education']...
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.2.html: non-numbered h2: ['Confident Wrong Answers in High-Stakes Contexts', 'Bias Across Demographic Groups', 'Privacy Leakage']...
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.3.html: non-numbered h2: ['FDA Software as a Medical Device (SaMD)', 'HIPAA and Equivalent Privacy Regulations', 'EU AI Act High-Risk Classification']...
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.4.html: non-numbered h2: ['The Five-Layer Defensive Pattern', 'Choosing Among the Four Patterns', 'Cross-Pattern Considerations']...
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.5.html: non-numbered h2: ['The 2026 Healthcare LLM Vendor Landscape', 'Cross-References Inside This Book', 'Canonical External References']
- part-11-applications-across-industries/module-54-education-llms/section-54.1.html: non-numbered h2: ["One-on-One Tutoring (Bloom's Two-Sigma, Sort Of)", 'Assessment Generation and Item Banking', 'Accessibility']...
- part-11-applications-across-industries/module-54-education-llms/section-54.2.html: non-numbered h2: ['The Plagiarism-Detector Mirage', 'Hallucinated Citations in Student Work', 'Learning-Loss Through Over-Reliance']...
- part-11-applications-across-industries/module-54-education-llms/section-54.3.html: non-numbered h2: ['FERPA and Student-Privacy', 'COPPA and Child Online Protection', 'EU AI Act Provisions on Education']...
- part-11-applications-across-industries/module-54-education-llms/section-54.4.html: non-numbered h2: ['The Five-Layer Pattern', 'Layer 1: Domain-Bounded Retrieval', 'Layer 2: Socratic-Prompt Design']...
- part-11-applications-across-industries/module-54-education-llms/section-54.5.html: non-numbered h2: ['The 2026 Vendor Landscape', 'Cross-References Inside This Book', 'Canonical External References']
- part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.1.html: non-numbered h2: ['SOC Alert Triage and Enrichment', 'Phishing-Email Analysis', 'Code Review for Security Vulnerabilities']...
- part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.2.html: non-numbered h2: ['Phishing Content Generation', 'Vulnerability Research Acceleration', 'Malware Adaptation']...
- part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.3.html: non-numbered h2: ['Prompt Injection', 'Training-Data Poisoning', 'Membership-Inference and Extraction']...
- part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.4.html: non-numbered h2: ['The Five-Layer Trust-Boundary Pattern', 'Layer 1: Input Classification', 'Layer 2: Output Filtering']...
- ... and 14 more

### h2 with wrong section prefix (25)

All 25 cases are legacy renumbering cruft. See the "Cross-cutting patterns" table above for the full mapping.

- part-10-idea-to-product/module-41-product-management/section-41.2.html: h2 with wrong section prefix (expected 41.2.*): ['31.2.1 Translating Business Problems to LLM Requirements', '31.2.2 Success Metrics for LLM Products', '31.2.3 Hallucination Risk Management']
- part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html: h2 with wrong section prefix (expected 42.3.*): ['31.1.1 AI Readiness Assessment', '31.1.2 Use Case Identification', '31.1.3 Prioritization Frameworks']
- part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html: h2 with wrong section prefix (expected 42.4.*): ['31.4.1 LLM Provider Evaluation', '31.4.2 Vector Database Evaluation', '31.4.3 Agent Framework Evaluation']
- part-10-idea-to-product/module-43-vibe-coding/section-43.2.html: h2 with wrong section prefix (expected 43.2.*): ['27.1.1 Code Completion and Fill-in-the-Middle', '27.1.2 AI-Native IDEs and Coding Assistants', '27.1.3 Agentic Coding']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.4.html: h2 with wrong section prefix (expected 45.4.*): ['45.5.1 What Is Vibe Coding?', '45.5.2 The Observe-Steer Loop', '45.5.3 Documentation as a Control Surface']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.5.html: h2 with wrong section prefix (expected 45.5.*): ['45.6.1 Vertical-Slice Prototyping', '45.6.2 The Build-Measure-Steer Loop', '45.6.3 AI Coding Assistants: Trust but Verify']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.6.html: h2 with wrong section prefix (expected 45.6.*): ['45.7.1 The Documentation Shift', '45.7.2 Three Documentation Imperatives', '45.7.3 Machine-Readable Documentation']
- part-10-idea-to-product/module-45-prototype-to-production/section-45.7.html: h2 with wrong section prefix (expected 45.7.*): ['45.9.1 When Is a Prototype Ready to Graduate?', '45.9.2 Quality Gates by Role Type', '45.9.3 The MVP Evaluation Contract']
- part-10-idea-to-product/module-48-shipping-deploying/section-48.1.html: h2 with wrong section prefix (expected 48.1.*): ['35.1.1 Billing Physics: How Tokens Become Dollars', '35.1.2 Deployment Platform Choices', '35.1.3 Security and Compliance Readiness']
- part-10-idea-to-product/module-48-shipping-deploying/section-48.2.html: h2 with wrong section prefix (expected 48.2.*): ['35.2.1 The Copilot Lifecycle Map', "35.2.2 Idea Framing: The LLM as Devil's Advocate", '35.2.3 Requirements: Generating Structured Artifacts']
- part-10-idea-to-product/module-48-shipping-deploying/section-48.3.html: h2 with wrong section prefix (expected 48.3.*): ['35.3.1 Vendor Lock-in vs. Cognitive Lock-in', '35.3.2 AI Continuity Planning', '35.3.3 Translation Cost Collapse: Why Traditional Lock-in Is Fading']
- part-10-idea-to-product/module-48-shipping-deploying/section-48.4.html: h2 with wrong section prefix (expected 48.4.*): ['35.4.1 Production Evaluation Is Continuous, Not One-Shot', '35.4.2 Drift Detection: Knowing When Quality Degrades', '35.4.3 Cost Monitoring and Optimization']
- part-11-applications-across-industries/module-52-finance-llms/section-52.7.html: h2 with wrong section prefix (expected 52.7.*): ['27.2.1 Financial NLP and Sentiment Analysis', '27.2.2 Automated Report Generation', '27.2.3 Trading Signals and Risk Analysis']
- part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html: h2 with wrong section prefix (expected 53.7.*): ['27.3.1 Medical LLMs', '27.3.2 Clinical NLP Applications', '27.3.3 Medical Question Answering']
- part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html: h2 with wrong section prefix (expected 55.7.*): ['27.5.1 Threat Intelligence with LLMs', '27.5.2 Log Analysis and Anomaly Detection', '27.5.3 Vulnerability Detection and Code Auditing']
- part-11-applications-across-industries/module-58-creative-industries/section-58.2.html: h2 with wrong section prefix (expected 58.2.*): ['27.6.1 Education and AI Tutoring', '27.6.2 Legal Applications', '27.6.3 Creative Writing and Co-Authorship']
- part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html: h2 with wrong section prefix (expected 59.2.*): ['27.4.1 LLMs as Recommendation Engines', '27.4.2 LLM-Powered Search', '27.4.3 Conversational Recommendation']
- part-12-frontiers/module-61-frontier-architectures/section-61.1.html: h2 with wrong section prefix (expected 61.1.*): ['33.1.1 The Original Emergence Claim', '33.1.2 The Mirage Hypothesis', '33.1.3 Resolution Attempts: Where the Debate Stands']
- part-12-frontiers/module-61-frontier-architectures/section-61.2.html: h2 with wrong section prefix (expected 61.2.*): ['33.2.1 The Data Wall', '33.2.2 Synthetic Data: Promise and Peril', '33.2.3 The Three Axes of Scaling']
- part-12-frontiers/module-61-frontier-architectures/section-61.3.html: h2 with wrong section prefix (expected 61.3.*): ['33.3.1 The Scaling Problem with Self-Attention', '33.3.2 State Space Models: S4, Mamba, and Mamba-2', '33.3.3 Linear Attention and Recurrent Alternatives']
- part-12-frontiers/module-61-frontier-architectures/section-61.4.html: h2 with wrong section prefix (expected 61.4.*): ['33.10.2 Tokenization Strategies Across Domains', '33.10.3 Genomics: DNA Language Models', '33.10.4 Protein Language Models']
- part-12-frontiers/module-62-frontier-theory/section-62.1.html: h2 with wrong section prefix (expected 62.1.*): ['33.5.1 What Do We Mean by "Reasoning"?', '33.5.2 Chain-of-Thought as Emergent Computation', '33.5.3 Process Reward Models and Verification']
- part-12-frontiers/module-62-frontier-theory/section-62.2.html: h2 with wrong section prefix (expected 62.2.*): ['33.6.1 The Memory Problem in LLMs', '33.6.2 A Taxonomy of Memory Architectures', '33.6.3 Working Memory vs. Long-Term Memory']
- part-12-frontiers/module-62-frontier-theory/section-62.3.html: h2 with wrong section prefix (expected 62.3.*): ['33.7.1 The Superposition Hypothesis', '33.7.2 Sparse Autoencoders for Feature Discovery', '33.7.3 Circuit Analysis']
- part-12-frontiers/module-62-frontier-theory/section-62.4.html: h2 with wrong section prefix (expected 62.4.*): ['33.8.1 Defining Agency: A Framework', '33.8.2 A Spectrum of Agency', '33.8.3 Philosophical Dimensions of Agency']


## 4. Captions

**2 caption issues.**

### table without caption or comparison-table-title (2)
- part-10-idea-to-product/module-45-prototype-to-production/section-45.3.html: <table> without caption or comparison-table-title
- part-12-frontiers/module-61-frontier-architectures/section-61.3.html: <table> without caption or comparison-table-title


## 5. Styles

### Callout class usage

| Class | Canonical? | Occurrences |
|---|---|---:|
| `key-insight` | canonical | 151 |
| `exercise` | canonical | 109 |
| `big-picture` | canonical | 94 |
| `warning` | canonical | 82 |
| `practical-example` | canonical | 81 |
| `tip` | canonical | 51 |
| `fun-note` | canonical | 30 |
| `self-check` | canonical | 29 |
| `note` | canonical | 22 |
| `key-takeaway` | canonical | 21 |
| `research-frontier` | canonical | 18 |
| `pathway` | canonical | 14 |
| `library-shortcut` | canonical | 11 |
| `production-pattern` | canonical | 9 |
| `postmortem` | canonical | 7 |
| `numeric-example` | canonical | 2 |
| `looking-back` | canonical | 2 |
| `algorithm` | canonical | 1 |
| `thesis-thread` | canonical | 1 |

All callouts use classes from the canonical palette.

## Recommended remediation order

1. **Module 62 renumbering sweep** (highest yield). Renumber `62.1`-`62.4` `<title>`, `<meta description>`, `breadcrumb`, and `page-current` to the live filenames, retire prose pointers to `62.5`-`62.9`, and re-stamp every `33.x` h2 prefix to `62.x`. Eliminates 4 title-prefix, 6 broken hrefs, and 4 wrong-prefix h2 findings in one batch.
2. **Module 61 + Module 48 renumbering sweep**. Same pattern, smaller surface. `33.x` -> `61.x` and `35.x` -> `48.x`. Eliminates 8 wrong-prefix h2 findings and 2 broken `48-shipping-scaling` hrefs (rename to `48-shipping-deploying`).
3. **Legacy `.7` and `58.2` / `59.2` files**. Either renumber the inner `27.x` h2s and `<title>` to the modern chapter, or retire the files per `_section_split_plan.md`. Affects 6 files, removes 6 title-prefix mismatches and 6 wrong-prefix h2 entries.
4. **Targeted broken-href cleanup** (small list, mechanical). Notable canonical-path drift:
   - `part-5-retrieval-conversation/module-23-rag-fundamentals` -> `module-23-rag` (1 hit in 40.1).
   - `../module-37-safety-ethics-regulation/...` from inside Part 10 -> `../../part-9-safety-security-ethics/module-37-safety-ethics-regulation/...` (2 hits in 41.2 and 42.3, relative-path drift, not a missing directory).
   - `part-6-agentic-ai/module-38-agent-safety-security/` -> `part-9-safety-security-ethics/module-38-agent-safety-security/` (3 hits in finance/cyber sections, wrong parent part).
   - `../module-31-multimodal/section-31.x.html` -> `../../part-7-multimodal-generation/module-31-multimodal/section-31.x.html` (5 hits in 43.2, 52.7, 53.7, 58.2, 59.2).
   - `module-29-multi-agent` -> `module-28-multi-agent-systems` (1 hit in 57.5).
   - `part-8-evaluation-production/module-35-llmops-mlops` -> `module-35-production-engineering` (1 hit in 57.5).
   - `module-48-shipping-scaling` -> `module-48-shipping-deploying` (2 hits, internal to Part 10).
   - `module-42-strategy-prioritization/section-31.x.html` -> these `31.x` hrefs refer to legacy section numbers; check whether they should point to current `42.x` content (3 hits).
5. **Pattern A vs `X.Y.Z` style alignment**. Decide whether Part 10/11 omnibus sections keep `1./2./3.` h2 numbering or convert to `X.Y.Z`. Either is internally consistent; mixing inside one chapter is the actual gap. Recommend converting to `X.Y.Z` for searchability and TOC generation parity with Parts 1-9.
6. **Two raw `<table>` fixes**. Wrap or `<caption>`-tag the remaining bare tables in `section-45.3.html` and `section-61.3.html`.

Steps 1-3 alone eliminate roughly 60% of all findings in the report. Step 4 cleans up the residue. Step 5 is a stylistic choice rather than a defect.
