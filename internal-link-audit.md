# Internal link audit (inline body links, read-only)

Root: `E:/Projects/BookBlogsHome/LLMBook` | Scanned: 389 HTML files

Scope: every `<a href>` inside `<body>` that is NOT inside 
`<header class="chapter-header">`, `<nav class="chapter-nav">`, 
`<nav class="header-nav">`, or `<footer>` (those are covered 
by the chapter-nav / footer / header-nav audits).

## 1. Summary

| Category | Total | Broken |
|---|---:|---:|
| Inline body `<a href>` scanned | 10796 | - |
| External (http/https/mailto/tel/data/etc., skipped) | 1673 | - |
| Empty `href` (excluded from broken count) | 0 | - |
| Pure-anchor `#frag` (same-page) | 41 | 0 |
| Relative-file (no anchor) | 5529 | 14 |
| Relative-file with anchor | 3553 | 30 |
|     ... target file missing | - | 30 |
|     ... file ok, anchor missing | - | 0 |
| Absolute-path `/...` | 0 | 0 |
| **Total broken inline links** | - | **44** |

## 2. Common broken patterns (top repeated targets)

### 2.1  Source pages with the most broken inline links

| Broken | Source page |
|---:|---|
| 29 | `front-matter/fm-course-syllabi.html` |
| 14 | `front-matter/fm-reading-pathways.html` |
| 1 | `index.html` |

### 2.2  Broken file targets grouped by first directory of resolved path

(Useful for spotting `../` over- or under-stepping. E.g. references that resolve to 
`glossary/...` at the project root when the real folder is `appendices/glossary/`.)

| Broken | Resolves under |
|---:|---|
| 31 | `glossary/` |
| 2 | `appendix-c-python-for-llm/` |
| 2 | `appendix-a-mathematical-foundations/` |
| 2 | `appendix-q-master-reference-tables/` |
| 1 | `appendix-b-ml-essentials/` |
| 1 | `appendix-d-environment-setup/` |
| 1 | `appendix-j-huggingface-ecosystem/` |
| 1 | `appendix-k-langchain/` |
| 1 | `appendix-u-freshness-2026/` |
| 1 | `appendix-s-pedagogy-kit/` |
| 1 | `KDP/` |

### 2.3  Broken file targets that repeat across pages

| Pages | href |
|---:|---|
| 2 | `../glossary/section-f.2.html#gl-llm` |
| 2 | `../glossary/section-f.5.html#gl-rag` |
| 2 | `../appendix-c-python-for-llm/index.html` |
| 2 | `../appendix-a-mathematical-foundations/index.html` |
| 2 | `../glossary/section-f.2.html#gl-gpt` |
| 2 | `../glossary/section-f.4.html#gl-attention` |
| 2 | `../glossary/section-f.2.html#gl-transformer` |
| 2 | `../glossary/section-f.3.html#gl-fine-tuning` |
| 2 | `../glossary/section-f.3.html#gl-lora` |
| 2 | `../appendix-q-master-reference-tables/index.html` |

## 3. Broken file targets (file not found on disk)

Total: 44

Format: `source_page.html:LINE  href -> resolved_path`

- `front-matter/fm-course-syllabi.html:29`  `../glossary/section-f.2.html#gl-llm` -> `glossary/section-f.2.html`
- `front-matter/fm-course-syllabi.html:29`  `../glossary/section-f.4.html#gl-eval` -> `glossary/section-f.4.html`
- `front-matter/fm-course-syllabi.html:40`  `../glossary/section-f.5.html#gl-rag` -> `glossary/section-f.5.html`
- `front-matter/fm-course-syllabi.html:52`  `../appendix-c-python-for-llm/index.html` -> `appendix-c-python-for-llm/index.html`
- `front-matter/fm-course-syllabi.html:52`  `../appendix-a-mathematical-foundations/index.html` -> `appendix-a-mathematical-foundations/index.html`
- `front-matter/fm-course-syllabi.html:62`  `../glossary/section-f.3.html#gl-tokenizer` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:62`  `../glossary/section-f.2.html#gl-gpt` -> `glossary/section-f.2.html`
- `front-matter/fm-course-syllabi.html:63`  `../glossary/section-f.4.html#gl-attention` -> `glossary/section-f.4.html`
- `front-matter/fm-course-syllabi.html:64`  `../glossary/section-f.2.html#gl-transformer` -> `glossary/section-f.2.html`
- `front-matter/fm-course-syllabi.html:65`  `../glossary/section-f.3.html#gl-decoding` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:67`  `../glossary/section-f.5.html#gl-prompt-engineering` -> `glossary/section-f.5.html`
- `front-matter/fm-course-syllabi.html:68`  `../glossary/section-f.4.html#gl-embedding` -> `glossary/section-f.4.html`
- `front-matter/fm-course-syllabi.html:77`  `../glossary/section-f.4.html#gl-chunking` -> `glossary/section-f.4.html`
- `front-matter/fm-course-syllabi.html:96`  `../glossary/section-f.3.html#gl-pretraining` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:96`  `../glossary/section-f.3.html#gl-scaling-laws` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:99`  `../glossary/section-f.4.html#gl-inference` -> `glossary/section-f.4.html`
- `front-matter/fm-course-syllabi.html:99`  `../glossary/section-f.3.html#gl-quantization` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:100`  `../glossary/section-f.4.html#gl-interpretability` -> `glossary/section-f.4.html`
- `front-matter/fm-course-syllabi.html:101`  `../glossary/section-f.3.html#gl-fine-tuning` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:101`  `../glossary/section-f.3.html#gl-peft` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:101`  `../glossary/section-f.3.html#gl-lora` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:124`  `../glossary/section-f.3.html#gl-kv-cache` -> `glossary/section-f.3.html`
- `front-matter/fm-course-syllabi.html:222`  `../appendix-a-mathematical-foundations/index.html` -> `appendix-a-mathematical-foundations/index.html`
- `front-matter/fm-course-syllabi.html:222`  `../appendix-b-ml-essentials/index.html` -> `appendix-b-ml-essentials/index.html`
- `front-matter/fm-course-syllabi.html:223`  `../appendix-c-python-for-llm/index.html` -> `appendix-c-python-for-llm/index.html`
- `front-matter/fm-course-syllabi.html:223`  `../appendix-d-environment-setup/index.html` -> `appendix-d-environment-setup/index.html`
- `front-matter/fm-course-syllabi.html:224`  `../glossary/index.html` -> `glossary/index.html`
- `front-matter/fm-course-syllabi.html:225`  `../appendix-j-huggingface-ecosystem/index.html` -> `appendix-j-huggingface-ecosystem/index.html`
- `front-matter/fm-course-syllabi.html:225`  `../appendix-k-langchain/index.html` -> `appendix-k-langchain/index.html`
- `front-matter/fm-reading-pathways.html:28`  `../glossary/section-f.5.html#gl-rag` -> `glossary/section-f.5.html`
- `front-matter/fm-reading-pathways.html:40`  `../glossary/section-f.2.html#gl-llm` -> `glossary/section-f.2.html`
- `front-matter/fm-reading-pathways.html:49`  `../glossary/section-f.2.html#gl-transformer` -> `glossary/section-f.2.html`
- `front-matter/fm-reading-pathways.html:56`  `../glossary/section-f.5.html#gl-function-calling` -> `glossary/section-f.5.html`
- `front-matter/fm-reading-pathways.html:56`  `../glossary/section-f.1.html#gl-mcp` -> `glossary/section-f.1.html`
- `front-matter/fm-reading-pathways.html:74`  `../glossary/section-f.3.html#gl-fine-tuning` -> `glossary/section-f.3.html`
- `front-matter/fm-reading-pathways.html:83`  `../glossary/section-f.3.html#gl-lora` -> `glossary/section-f.3.html`
- `front-matter/fm-reading-pathways.html:100`  `../appendix-u-freshness-2026/index.html` -> `appendix-u-freshness-2026/index.html`
- `front-matter/fm-reading-pathways.html:110`  `../glossary/section-f.4.html#gl-attention` -> `glossary/section-f.4.html`
- `front-matter/fm-reading-pathways.html:126`  `../glossary/section-f.3.html#gl-token` -> `glossary/section-f.3.html`
- `front-matter/fm-reading-pathways.html:126`  `../glossary/section-f.2.html#gl-gpt` -> `glossary/section-f.2.html`
- `front-matter/fm-reading-pathways.html:135`  `../appendix-q-master-reference-tables/index.html` -> `appendix-q-master-reference-tables/index.html`
- `front-matter/fm-reading-pathways.html:147`  `../appendix-s-pedagogy-kit/index.html` -> `appendix-s-pedagogy-kit/index.html`
- `front-matter/fm-reading-pathways.html:162`  `../appendix-q-master-reference-tables/index.html` -> `appendix-q-master-reference-tables/index.html`
- `index.html:838`  `KDP/output/editions/` -> `KDP/output/editions/index.html`

## 4. Broken same-page `#anchor` links

Total: 0

_None._

## 5. Broken anchor targets (file exists, anchor missing)

Total: 0

Format: `source_page.html:LINE  href  (target file ok, anchor missing)`

_None._

## 6. Recommended fixes

- Fix the `front-matter/` mis-stepped relative paths (43 broken links across 2 pages, e.g. front-matter/fm-course-syllabi.html, front-matter/fm-reading-pathways.html): links currently use `../glossary/...` and `../appendix-X/...`, which resolve to `glossary/...` and `appendix-X/...` at the project root. The real files live under `appendices/glossary/` and `appendices/appendix-X/`. The references read as if these pages were copied from inside `appendices/`. Change `../glossary/` -> `../appendices/glossary/` and `../appendix-X/` -> `../appendices/appendix-X/` in the affected front-matter files.
- `index.html` line references `KDP/output/editions/` which lives under the `KDP/` build output (excluded from this audit's tree). Confirm the homepage should link to `KDP/output/...` in the published artifact, or rewrite to a non-KDP target.
- After pattern fixes, sweep the residual one-off broken links in Section 3 and Section 5; they are typically typos (missing `.html`, wrong section number, or stale anchor ids).
- Re-run `scripts/_audit_internal_links.py` after each batch of fixes to track progress; current baseline: 44 broken inline links.

---
_Audit script: `scripts/_audit_internal_links.py`. Inline hrefs scanned: 10796; pages: 389._
