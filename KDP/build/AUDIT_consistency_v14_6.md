# v14.6 Consistency Audit

_Generated 2026-05-15 after v14.5 restructuring (industries -> Part XII, appendix AH dropped, appendix numbering aligned, bibliography headers consolidated, 940 hyperlinks added, v14.4 nav boundary fixes)._

_Repository: `E:/Projects/BookBlogsHome/LLMBook`_

## Scope

- HTML pages scanned: **389**
- Pages with chapter-nav: **387**
- Pages indexed for IDs:  **389**
- ToC entries indexed:    **459**
- Unparseable pages:      **0**

## Findings Summary

| Category | Count |
|---|---|
| Broken internal links | **27** |
| Broken anchor fragments | **1** |
| Orphan HTML files (no inbound link) | **0** |
| ToC links broken | **0** |
| Section files not in ToC | **0** |
| Module/appendix indexes not in ToC | **7** |
| Asymmetric prev/next chains | **1** |
| Broken prev/up/next targets | **0** |
| Self-links (next/prev to same page) | **0** |
| All self-links (any kind) | **18** |
| Stale section references in prose | **2** |
| Refs to dropped appendix letters (W/X/Y/Z/AA/AB/AC) | **0** |
| Refs to dropped Appendix AH | **4** |
| Suspicious-depth `../` paths | **0** |
| Bibliography broken internal links | **0** |
| Glossary/concept hyperlinks (total) | **3641** |
| Glossary/concept broken file targets | **27** |
| Glossary/concept broken anchors | **0** |
| Part XII chain issues | **0** |

## Part XII Restructuring Status

| Module | Inbound Refs | In ToC |
|---|---|---|
| `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` | 2 | **NO** |
| `part-12-llm-applications-across-industries/module-37-finance-llms/index.html` | 3 | **NO** |
| `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` | 3 | **NO** |
| `part-12-llm-applications-across-industries/module-39-education-llms/index.html` | 3 | **NO** |
| `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` | 3 | **NO** |
| `part-12-llm-applications-across-industries/module-41-government-llms/index.html` | 3 | **NO** |
| `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` | 3 | **NO** |

> **CRITICAL: 7 of 7 Part XII modules are missing from the Table of Contents.**

## Dropped Appendix AH (Conceptual Map)

- Source-tree presence of `appendices/appendix-ah-*/`: **GONE (correct)**
- Prose references to "Appendix AH": **4**

  - `appendices/appendix-af-pedagogy-kit/index.html`: "Appendix AH" ctx: ...Engineer building AI products (revised) Front matter: read Appendix AH (Conceptual Map), Appendix AD (Reference Tables), Appendix...
  - `appendices/appendix-af-pedagogy-kit/index.html`: "Appendix AH" ctx: ...Pathway: Researcher / grad student (revised) Front matter: Appendix AH (Conceptual Map) and Appendix AE (Freshness Index). The con...
  - `appendices/appendix-af-pedagogy-kit/index.html`: "Appendix AH" ctx: ...Founder / product / tech lead (revised) Front matter only: Appendix AH (Conceptual Map), Appendix AD (Reference Tables, especially...
  - `appendices/appendix-aj-reading-pathways/index.html`: "Appendix AH" ctx: ...substance. Know which deeper rabbit hole to fall down next. Appendix AH (Conceptual Map) · 1 hr (read the 5 unifying theses and 3 t...

## References to Moved/Dropped Appendix Letters (W, X, Y, Z, AA, AB, AC)

- Total mentions: **0**

## Broken Internal Links (first 40)

- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.5.html#gl-rag` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-grounding` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-37-finance-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-37-finance-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-hallucination` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-37-finance-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-gpt` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-hallucination` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-eval` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.3.html#gl-fine-tuning` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-inference` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-synthetic-data` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-inference` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.5.html#gl-system-prompt` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.5.html#gl-rag` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-grounding` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.3.html#gl-temperature` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-eval` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.1.html#gl-vllm` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-alignment` (class="glossary-link")
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-inference` (class="glossary-link")

## Broken Anchor Fragments (first 30)

- `part-1-foundations/module-04-transformer-architecture/section-4.1.html` -> `#scaled-dot-product-attention` (#scaled-dot-product-attention not in target)

## Orphan HTML Files (no inbound links)

_None._

## ToC Broken Links

_None._

## Section Files Not in ToC

_All section files are referenced in the ToC._

## Module/Appendix Indexes Not in ToC

- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html`
- `part-12-llm-applications-across-industries/module-37-finance-llms/index.html`
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html`
- `part-12-llm-applications-across-industries/module-39-education-llms/index.html`
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html`
- `part-12-llm-applications-across-industries/module-41-government-llms/index.html`
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html`

## Asymmetric prev/next Chains

- next/prev: `part-11-idea-to-product/module-35-shipping-scaling/section-35.4.html` -> `part-12-llm-applications-across-industries/index.html` (back-link: `part-11-idea-to-product/index.html`)

## Broken prev/up/next Targets

_None._

## Self-Links (page hyperlinking to itself)

- `appendices/appendix-aj-reading-pathways/index.html` -> `index.html` (class="")
- `appendices/appendix-ak-course-syllabi/index.html` -> `index.html` (class="")
- `appendices/appendix-t-distributed-ml/section-t.1.html` -> `section-t.1.html` (class="")
- `appendices/appendix-t-distributed-ml/section-t.1.html` -> `section-t.1.html` (class="")
- `part-1-foundations/module-00-ml-pytorch-foundations/index.html` -> `index.html` (class="")
- `part-1-foundations/module-01-foundations-nlp-text-representation/index.html` -> `index.html` (class="")
- `part-1-foundations/module-02-tokenization-subword-models/index.html` -> `index.html` (class="")
- `part-1-foundations/module-03-sequence-models-attention/index.html` -> `index.html` (class="")
- `part-1-foundations/module-04-transformer-architecture/index.html` -> `index.html` (class="")
- `part-1-foundations/module-05-decoding-text-generation/index.html` -> `index.html` (class="")
- `part-11-idea-to-product/module-34-idea-to-product/index.html` -> `index.html` (class="")
- `part-11-idea-to-product/module-34-idea-to-product/section-34.5.html` -> `../../part-11-idea-to-product/module-34-idea-to-product/section-34.5.html` (class="prereq-link")
- `part-11-idea-to-product/module-35-shipping-scaling/index.html` -> `index.html` (class="")
- `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html` -> `index.html` (class="")
- `part-5-retrieval-conversation/module-20-conversational-ai/section-20.5.html` -> `section-20.5.html` (class="")
- `part-6-agentic-ai/module-21-ai-agents/section-21.6.html` -> `../../part-6-agentic-ai/module-21-ai-agents/section-21.6.html` (class="prereq-link")
- `part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` -> `../../part-8-evaluation-production/module-28-evaluation-observability/section-28.6.html` (class="prereq-link")
- `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` -> `../../part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.3.html` (class="prereq-link")

## Stale Section References (prose)

_Mentions of `Section X.Y` or `Appendix X.Y` where the referenced section file does not exist._

### Top stale ref tokens

| Ref | Mentions |
|---|---|
| 24.8 | 1 |
| 24.6 | 1 |

### Sample mentions
- `part-6-agentic-ai/module-24-specialized-agents/section-24.1.html`: "Section 24.8" ctx: ...for correctness, not a sufficient one. Section 24.8 covers AI-generated code quality in det...
- `part-6-agentic-ai/module-24-specialized-agents/section-24.4.html`: "Section 24.6" ctx: ...ection 24.1 , SWE-bench evaluation from Section 24.6, agent foundations from Chapter 21 , an...

## Suspicious-Depth `../` Paths

_None._

## Glossary / Concept Hyperlinks (v14.5 additions)

- Total `.glossary-link` and `.concept-link` anchors: **3641**
- With broken file target: **27**
- With broken anchor: **0**

### Broken-target hyperlinks (first 20)

- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.5.html#gl-rag` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-36-legal-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-grounding` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-37-finance-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-37-finance-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-hallucination` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-37-finance-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-gpt` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-hallucination` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-eval` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.3.html#gl-fine-tuning` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-inference` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-38-healthcare-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-synthetic-data` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-inference` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.4.html#gl-classification` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-40-cybersecurity-llms/index.html` -> `../appendix-f-glossary/section-f.5.html#gl-system-prompt` (class=glossary-link)
- `part-12-llm-applications-across-industries/module-42-manufacturing-llms/index.html` -> `../appendix-f-glossary/section-f.2.html#gl-llm` (class=glossary-link)

_...and 7 more._

## Bibliography Link Status

- Internal bibliography links: **148**
- External (URL) bibliography links: **1481**
- Broken internal bibliography links: **0**

## Recommended v14.7 Patch Priority

- **P0** Add Part XII (7 modules) to `toc.html` (both short and detailed views). Currently 7/7 modules invisible in nav.
- **P0** Fix 27 broken internal link(s).
- **P1** Remove or redirect 4 prose reference(s) to dropped Appendix AH.
- **P1** Reconcile 1 asymmetric prev/next chain(s).
- **P1** Repair 18 self-link(s) (page hyperlinks to itself).
- **P2** Fix 1 `#anchor` fragment(s) that don't resolve.
- **P2** Repair 27 broken-target + 0 broken-anchor `.glossary-link`/`.concept-link` instance(s).
- **P3** Review 2 stale `Section X.Y` mention(s) in prose.

---

_End of report._