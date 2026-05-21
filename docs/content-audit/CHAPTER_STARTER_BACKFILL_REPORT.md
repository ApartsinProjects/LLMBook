# Chapter Starter Backfill Report

Backfilling the missing `<div class="overview">` block and `Note: Learning Objectives` callout on chapter-index pages flagged by the `CHAPTER_STARTER` and `CHAPTER_INDEX_LAYOUT` audit checks.

## Scope

- 57 chapter-index files edited.
- 54 overview blocks effectively added (52 inserted as new `<div class="overview">` blocks plus 2 existing `<div class="chapter-overview">` blocks renormalized to the canonical `<div class="overview">` class so the layout audit sees them).
- 57 `Note: Learning Objectives` callouts inserted.
- Insertion point: immediately after the closing `</div>` of the chapter `<div class="callout big-picture">` block, before the `<ul class="sections-list">`. Order: overview, then objectives.
- The objectives bullets are first-person-actionable, each starting with a verb (Explain, Apply, Compare, Implement, Architect, Diagnose, Evaluate, Design, Choose, Configure, Use, Wire, Build, Load, Apply, Track).
- No em-dashes used. Content reflects the actual section h1 titles and chapter card descriptions of each chapter.

## Per-Part Counts

| Part | Files | Overviews | Objectives |
|---|---|---|---|
| Part I LLM Building Blocks | 1 | 1 | 1 |
| Part III Working with LLMs | 2 | 1 | 2 |
| Part IV Training and Adaptation | 1 | 1 | 1 |
| Part V Multimodal LLMs | 6 | 6 | 6 |
| Part VI Agentic AI | 1 | 1 | 1 |
| Part VII Retrieval and IE | 4 | 4 | 4 |
| Part VIII Conversational AI | 2 | 2 | 2 |
| Part IX Evaluation and Observability | 4 | 4 | 4 |
| Part X Security and Runtime Safety | 4 | 3 | 4 |
| Part XI Ethics, Trust, Governance | 6 | 4 (+2 class renames) | 6 |
| Part XII LLM Systems at Scale | 5 | 5 | 5 |
| Part XIII LLMOps Lifecycle | 5 | 5 | 5 |
| Part XIV Designing LLM Agent Products | 5 | 4 | 5 |
| Part XIV Industry Applications | 8 | 8 | 8 |
| Part XV Research Frontiers | 3 | 3 | 3 |
| **Total** | **57** | **52 inserted + 2 renames = 54 effective** | **57** |

The two class renames live at:

- `part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html` (was `chapter-overview`, now `overview`)
- `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/index.html` (was `chapter-overview`, now `overview`)

Three chapters needed only the objectives callout because they already had a proper `<div class="overview">` block:

- `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html`
- `part-14-designing-llm-agent-products/module-70-shipping-products/index.html`
- `part-3-working-with-llms/module-12-prompt-engineering/index.html`

## Audit Delta

Before backfill (audit at HEAD):

- `CHAPTER_STARTER`: 109 issues (52 missing overview + 57 missing objectives)
- `CHAPTER_INDEX_LAYOUT`: 291 issues total (54 of those for missing overview + 57 for missing Learning Objectives)
- Total issues: 1975

After backfill:

- `CHAPTER_STARTER`: 0 issues
- `CHAPTER_INDEX_LAYOUT`: 180 issues (0 for overview, 0 for Learning Objectives, the rest are unrelated layout checks like epigraph / looking-back / prereqs / whats-next that are out of this task's scope)
- Total issues: 1742
- **Net reduction: 233 issues**

The `CHAPTER_INDEX_LAYOUT` count drops by 111: 54 overview + 57 Learning Objectives. The remaining 180 issues under that check are the four other recommended elements (canonical epigraph, looking-back callout, Prerequisites callout, canonical whats-next), which were not part of this backfill.

## Sample Pairs

### Sample 1: `part-1-llm-building-blocks/module-05-tools-of-the-trade/index.html`

Overview:

> Part I taught the fundamentals: tensors and autograd, sequence models, attention, the transformer block, and decoding. This chapter consolidates the toolbox that those fundamentals become in practice. We walk the four editors that handle most LLM engineering, the libraries (PyTorch, NumPy, SciPy, scikit-learn, HuggingFace tokenizers) that ship the abstractions, the datasets (MNIST, CIFAR-10, SQuAD, GLUE) that anchor the exercises, the two reference models (BERT-base, GPT-2) sized for a 6 GB GPU, and the external reading and communities that keep your toolbox current.
>
> Bookmark this chapter. Every later Part assumes the vocabulary locked in here, and every Tools of the Trade chapter that follows refers back to one of these primitives by name.

Objectives:

- Evaluate IDE and notebook platforms (VS Code, Cursor, JupyterLab, Colab) for LLM engineering workflows.
- Install and validate the canonical Part I library set (torch, numpy, scipy, scikit-learn, tokenizers, datasets, matplotlib).
- Choose the right teaching dataset (MNIST, CIFAR-10, SQuAD, GLUE) for a given foundations exercise.
- Load and inspect the BERT-base and GPT-2 reference checkpoints on a 6 GB GPU.
- Identify the external venues, blogs, and communities that maintain the modern LLM toolchain.

### Sample 2: `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/index.html`

Overview:

> Guardrails are the runtime layer of LLM safety: the external checks that sit around a model and intercept inputs, outputs, and intermediate tool calls. This chapter walks the full guardrail stack from definition to deployment: what guardrails are (and are not), input guardrails (prompt-injection detection, PII pre-filtering), output guardrails (Llama Guard, NeMo Guardrails, ShieldGemma, Guardrails AI), policy DSLs and constrained decoding as safety primitives, and multimodal guardrails for image, audio, and video.
>
> Guardrails are the difference between a research demo and a deployable system. By the end of this chapter you will know which guardrail to reach for, how to layer them, and how to avoid the false-confidence failure mode that single-guardrail deployments inherit.

Objectives:

- Explain the role of guardrails in the LLM safety stack and what they cannot replace.
- Apply input guardrails (prompt-injection detection, PII pre-filtering) at the request layer.
- Compare Llama Guard, NeMo Guardrails, ShieldGemma, and Guardrails AI as output-guardrail engines.
- Use policy DSLs and constrained decoding to make unsafe output structurally impossible.
- Architect multimodal guardrails for image, audio, and video inputs and outputs.
- Diagnose false-positive and false-negative regressions in a guardrail deployment.

### Sample 3: `part-14-applications-of-llms-across-industries/module-69-healthcare-llms/index.html`

Overview:

> Healthcare LLM deployment is the chapter where regulatory, ethical, and clinical-safety considerations all converge. This chapter walks the use cases that actually work (ambient documentation, clinical decision support, patient triage, medical coding, literature synthesis, drug discovery), the failure modes specific to healthcare (confident wrong answers, demographic bias, privacy leakage), the regulatory framework (FDA SaMD, HIPAA, EU AI Act, state licensure, CHAI assurance standards), the HIPAA-compliant deployment patterns (BAA-covered cloud, de-identified, VPC-isolated, on-premises open-weight), and the vendor landscape plus canonical sources.
>
> Healthcare is the industry where a hallucination can harm a patient. This chapter teaches what works, what hurts, and what FDA and HIPAA actually require.

Objectives:

- Map the healthcare use cases (ambient documentation, CDS, triage, coding, drug discovery) that actually work.
- Diagnose confident wrong answers, demographic bias, and privacy leakage in healthcare LLMs.
- Apply FDA SaMD, HIPAA, EU AI Act, and CHAI assurance standards to a healthcare deployment.
- Architect a HIPAA-compliant LLM deployment across BAA-covered cloud, de-identified, VPC-isolated, and on-premises patterns.
- Evaluate healthcare LLM vendors (Abridge, Suki, Dragon Copilot, Glass Health, Hippocratic AI) against clinical fit.

## Method

1. Ran `scripts/run_book_audit.py --json` against the v2.0 branch to enumerate the 57 chapter-index files with `CHAPTER_STARTER` or `CHAPTER_INDEX_LAYOUT` issues mentioning overview or learning objectives.
2. Built a Python extractor (`.chapter_starter_extract.py`) that read each chapter-index, grabbed the chapter h1 and the section card titles plus descriptions, and dumped a JSON context for each.
3. Authored the overview paragraphs and objectives bullets per chapter, hand-shaped so the content matches the actual section structure of each chapter.
4. Ran `.chapter_starter_apply.py` which located the `<div class="callout big-picture">` block and inserted the missing blocks immediately after it.
5. Renamed two `chapter-overview` divs to `overview` so the layout audit recognizes them.
6. Re-ran the audit to confirm the delta.

## Workflow Artifacts

Working files (kept temporarily in the repo root, not committed):

- `.chapter_starter_targets.txt` (target list with flags)
- `.chapter_starter_context.json` (per-chapter context extracted for authoring)
- `.chapter_starter_extract.py` (extractor)
- `.chapter_starter_apply.py` (writer)
- `.audit.json`, `.audit_after.json`, `.audit_after2.json` (audit snapshots)

These can be deleted once the parent commit lands.
