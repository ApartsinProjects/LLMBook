# Per-Section Audit - Parts 1-3

_Scope: every `section-N.M.html` under `part-1-foundations/`, `part-2-understanding-llms/`, `part-3-working-with-llms/` (modules 00-16)._

## Summary
- Files audited: 83
- P0 (structure / well-formedness / inline styles / TODO markers): 3 findings across 3 files
- P1 (broken non-external links): 11 findings across 10 files
- P2 (naming drift in <title>/<h1>/breadcrumb/pagefind): 2 findings across 1 files
- P3 (missing captions on figures/code/comparison-tables): 27 findings across 24 files
- P4 (callout palette drift / missing callout-title): 0 findings across 0 files

### Repeating broken-link patterns
- `../../part-12-frontiers/module-61-frontier-architectures/section-33.1.html` -> 5 occurrence(s)
- `../../part-10-idea-to-product/module-42-strategy-prioritization/section-31.2.html` -> 2 occurrence(s)
- `../../part-10-idea-to-product/module-42-strategy-prioritization/section-31.4.html` -> 1 occurrence(s)
- `../../part-2-understanding-llms/module-07-tokenization/index.html` -> 1 occurrence(s)
- `../../part-2-understanding-llms/module-11-mechanistic-interpretability/index.html` -> 1 occurrence(s)
- `../../part-6-agentic-ai/module-38-agent-safety-security/section-25.3.html` -> 1 occurrence(s)

These hrefs reference old numbering (section-33.x, section-31.x, section-25.x) or wrong module names that no longer exist after the part renumbering.

## Per-file findings
### part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html
  - P3 captions (1):
    - significant <pre> (lineno 57) missing caption
### part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html
  - P0 structure (1):
    - 1 inline style= occurrences (sample lines: 328)
  - P3 captions (1):
    - significant <pre> (lineno 153) missing caption
### part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html
  - P3 captions (1):
    - significant <pre> (lineno 106) missing caption
### part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html
  - P3 captions (1):
    - significant <pre> (lineno 216) missing caption
### part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html
  - P3 captions (1):
    - significant <pre> (lineno 194) missing caption
### part-1-foundations/module-02-tokenization-subword-models/section-2.3.html
  - P0 structure (1):
    - 13 inline style= occurrences (sample lines: 199,199,200,201,203)
### part-1-foundations/module-03-sequence-models-attention/section-3.1.html
  - P1 links (1):
    - line 669: broken href '../../part-12-frontiers/module-61-frontier-architectures/section-33.1.html'
  - P3 captions (1):
    - significant <pre> (lineno 111) missing caption
### part-1-foundations/module-03-sequence-models-attention/section-3.3.html
  - P3 captions (2):
    - significant <pre> (lineno 122) missing caption
    - significant <pre> (lineno 368) missing caption
### part-1-foundations/module-04-transformer-architecture/section-4.1.html
  - P0 structure (1):
    - 1 inline style= occurrences (sample lines: 797)
  - P1 links (1):
    - line 1042: broken href '../../part-12-frontiers/module-61-frontier-architectures/section-33.1.html'
  - P3 captions (1):
    - significant <pre> (lineno 574) missing caption
### part-1-foundations/module-04-transformer-architecture/section-4.4.html
  - P3 captions (1):
    - significant <pre> (lineno 219) missing caption
### part-1-foundations/module-04-transformer-architecture/section-4.5.html
  - P1 links (1):
    - line 268: broken href '../../part-12-frontiers/module-61-frontier-architectures/section-33.1.html'
### part-1-foundations/module-05-decoding-text-generation/section-5.1.html
  - P3 captions (1):
    - significant <pre> (lineno 91) missing caption
### part-1-foundations/module-05-decoding-text-generation/section-5.2.html
  - P3 captions (1):
    - significant <pre> (lineno 108) missing caption
### part-1-foundations/module-05-decoding-text-generation/section-5.3.html
  - P3 captions (1):
    - significant <pre> (lineno 84) missing caption
### part-1-foundations/module-05-decoding-text-generation/section-5.4.html
  - P3 captions (1):
    - significant <pre> (lineno 133) missing caption
### part-1-foundations/module-06-tools-of-the-trade/section-6.2.html
  - P1 links (1):
    - line 43: broken href '../../part-2-understanding-llms/module-07-tokenization/index.html'
### part-1-foundations/module-06-tools-of-the-trade/section-6.4.html
  - P1 links (1):
    - line 106: broken href '../../part-2-understanding-llms/module-11-mechanistic-interpretability/index.html'
### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.2.html
  - P1 links (1):
    - line 536: broken href '../../part-12-frontiers/module-61-frontier-architectures/section-33.1.html'
### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.3.html
  - P3 captions (1):
    - significant <pre> (lineno 398) missing caption
### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.5.html
  - P3 captions (2):
    - significant <pre> (lineno 99) missing caption
    - significant <pre> (lineno 210) missing caption
### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.6.html
  - P3 captions (1):
    - significant <pre> (lineno 101) missing caption
### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.7.html
  - P3 captions (1):
    - significant <pre> (lineno 59) missing caption
### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.8.html
  - P3 captions (1):
    - significant <pre> (lineno 250) missing caption
### part-2-understanding-llms/module-07-pretraining-scaling-laws/section-7.9.html
  - P2 naming (2):
    - <title> body 'Lab - Pretrain a Tiny Language Model' != <h1> 'Lab: Pretrain a Tiny Language Model'
    - missing pagefind chapter meta
### part-2-understanding-llms/module-08-modern-llm-landscape/section-8.1.html
  - P3 captions (1):
    - significant <pre> (lineno 313) missing caption
### part-2-understanding-llms/module-08-modern-llm-landscape/section-8.2.html
  - P3 captions (1):
    - significant <pre> (lineno 128) missing caption
### part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html
  - P3 captions (1):
    - significant <pre> (lineno 127) missing caption
### part-2-understanding-llms/module-10-inference-optimization/section-10.1.html
  - P1 links (1):
    - line 68: broken href '../../part-10-idea-to-product/module-42-strategy-prioritization/section-31.4.html'
  - P3 captions (2):
    - significant <pre> (lineno 120) missing caption
    - significant <pre> (lineno 319) missing caption
### part-2-understanding-llms/module-10-inference-optimization/section-10.4.html
  - P3 captions (1):
    - significant <pre> (lineno 105) missing caption
### part-2-understanding-llms/module-10-inference-optimization/section-10.6.html
  - P1 links (2):
    - line 211: broken href '../../part-10-idea-to-product/module-42-strategy-prioritization/section-31.2.html'
    - line 309: broken href '../../part-12-frontiers/module-61-frontier-architectures/section-33.1.html'
### part-2-understanding-llms/module-10-inference-optimization/section-10.7.html
  - P3 captions (1):
    - significant <pre> (lineno 68) missing caption
### part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.4.html
  - P1 links (1):
    - line 247: broken href '../../part-10-idea-to-product/module-42-strategy-prioritization/section-31.2.html'
### part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.5.html
  - P1 links (1):
    - line 1168: broken href '../../part-6-agentic-ai/module-38-agent-safety-security/section-25.3.html'

_Generated by scripts/audit_parts_1_3.py over 83 sections._
