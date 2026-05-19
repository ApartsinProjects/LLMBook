# Bibliography Backfill Report

Backfilled `<details class="bibliography-collapsible">` Further Reading blocks across the 114 sections flagged by the `SECTION_PAGE_LAYOUT` audit.

## Audit delta

| Metric | Before | After |
| --- | --- | --- |
| `SECTION_PAGE_LAYOUT` issues with "bibliography" in the message | 114 | 0 |

Verified by `python scripts/run_book_audit.py --json` and filtering on `check_id == 'SECTION_PAGE_LAYOUT'` + message contains "bibliography".

## Per-chapter / per-module count

| Chapter / Module | Sections backfilled |
| --- | --- |
| Appendix A (Mathematical Foundations) | 5 |
| Module 5 (Tools of the Trade, Part I) | 4 |
| Module 6 (Pretraining and Scaling Laws) | 1 (lab section 6.9) |
| Module 10 (Interpretability tools sub-section) | 4 (sections 10.5-10.8) |
| Module 14 (Tools of the Trade, Part III) | 4 |
| Module 19 (Tools of the Trade, Part IV) | 14 |
| Module 25 (Tools of the Trade, Part V) | 4 |
| Module 30 (Tools of the Trade, Part VI) | 4 |
| Module 34 (Structured Information Extraction / NER) | 4 |
| Module 37 (Conversational AI) | 1 (section 37.3) |
| Module 40 (Voice, Realtime, Multimodal) | 1 (section 40.6) |
| Module 44 (Online Evaluation, Observability) | 3 |
| Module 45 (Tools of the Trade, Part IX) | 4 |
| Module 46 (LLM-as-Judge) | 4 |
| Module 47 (Adversarial Security, Red Team) | 1 (section 47.3) |
| Module 50 (Privacy and Data Protection) | 1 (section 50.3) |
| Module 51 (Tools of the Trade, Part X) | 4 |
| Module 57 (Compute Planning and Infrastructure) | 3 |
| Module 65 (Containers and Kubernetes) | 4 |
| Module 67 (Ideation) | 2 |
| Module 68 (Vibe Coding) | 3 |
| Module 69 (LLM Economics) | 2 |
| Module 71 (Tools of the Trade, Part XIV) | 4 |
| Module 72 (Legal LLMs) | 4 |
| Module 73 (Finance LLMs) | 4 |
| Module 74 (Healthcare LLMs) | 4 |
| Module 75 (Education LLMs) | 4 |
| Module 76 (Cybersecurity LLMs) | 4 |
| Module 77 (Government LLMs) | 4 |
| Module 78 (Manufacturing / Misc Verticals) | 5 |
| Module 79 (Tools of the Trade, Part XIV) | 4 |
| **Total** | **114** |

## Format

Every block follows the in-book pattern already used by `section-44.1.html`, `section-46.5.html`, etc:

```html
<details class="bibliography-collapsible">
  <summary><strong>Further Reading</strong></summary>
  <section class="bibliography">
    <h3 id="foundational">Foundational Papers</h3>
    <div class="bib-entry-card">
      <div class="bib-ref">Author. (YYYY). "Title." <em>Venue</em>. <a href="..." rel="noopener" target="_blank">arXiv:XXXX.XXXX</a>. <span class="bib-note">Annotation.</span></div>
    </div>
    ...
  </section>
</details>
```

Entries are grouped under h3 sub-headings (Foundational Papers, Recent Advances, Surveys, Tools, etc.) appropriate to the section content. Every section receives 3 to 7 entries, with at least one foundational paper and at least one 2023-or-later reference where the topic supports it.

## Sample bibliographies

### Sample 1: Mathematical Appendix (Section A.1 -- Linear Algebra)

```html
<details class="bibliography-collapsible">
  <summary><strong>Further Reading</strong></summary>
  <section class="bibliography">
    <h3 id="foundational">Foundational Textbooks</h3>
    <div class="bib-entry-card">
      <div class="bib-ref">Strang, G. (2016). <em>Introduction to Linear Algebra</em> (5th ed.). Wellesley-Cambridge Press. <span class="bib-note">The standard undergraduate reference; chapters on eigenvalues, SVD, and projection underpin every embedding and attention computation in this book.</span></div>
    </div>
    <div class="bib-entry-card">
      <div class="bib-ref">Trefethen, L. N., &amp; Bau, D. (1997). <em>Numerical Linear Algebra</em>. SIAM. <span class="bib-note">The reference for numerically stable algorithms; relevant to mixed-precision training and inference quantization.</span></div>
    </div>
    <div class="bib-entry-card">
      <div class="bib-ref">Golub, G. H., &amp; Van Loan, C. F. (2013). <em>Matrix Computations</em> (4th ed.). Johns Hopkins University Press. <span class="bib-note">Encyclopedic reference for matrix algorithms; the source for FlashAttention-style tiling analyses.</span></div>
    </div>
    <h3 id="modern">Modern Treatments for ML</h3>
    <div class="bib-entry-card">
      <div class="bib-ref">Deisenroth, M. P., Faisal, A. A., &amp; Ong, C. S. (2020). <em>Mathematics for Machine Learning</em>. Cambridge University Press. <span class="bib-note">Free online textbook; covers the linear algebra and probability prerequisites for modern deep learning.</span></div>
    </div>
    ...
  </section>
</details>
```

### Sample 2: Industry vertical (Section 67.1 -- Legal LLMs Use Cases)

References anchored to legal-LLM empirical studies (Stanford HAI hallucination audit, Dahl et al. legal fictions paper, LegalBench, LexGLUE). Two h3 groupings: Foundational Papers and Legal Benchmarks.

### Sample 3: Frontier research section (Section 47.3 -- Supply Chain, Confidential Compute, Multimodal Threats)

Three h3 groupings: Supply Chain and Provenance (Carlini et al. on data poisoning, Hugging Face Sigstore signing, OpenSSF Model Signing), Confidential Compute (NVIDIA H100/H200 TEE docs, Costan and Devadas SGX paper), and Multimodal Attacks (Bagdasaryan et al. on image-prompt-injection, Greshake et al. on indirect prompt injection).

### Sample 4: Production engineering section (Section 65.1 -- Docker Fundamentals)

Three h3 groupings: Foundational Sources (official Docker docs, Merkel 2014 paper), Container Internals (OCI Runtime Spec, Burns/Beda/Hightower Kubernetes book), and ML Container Patterns (NVIDIA NGC catalog, NVIDIA Container Toolkit).

### Sample 5: Tools-of-the-trade section (Section 19.13 -- Distributed Training Deep Dive)

One h3 grouping (Distributed Training) with four entries: ZeRO paper (Rajbhandari et al.), FSDP paper (Zhao et al.), Megatron-LM paper (Shoeybi et al.), and GPipe paper (Huang et al.). Anchors the implementation walkthroughs in the section to canonical primary literature.

## Rules followed

- No em-dashes anywhere in inserted content.
- No fabricated arXiv IDs. Every `<a href="https://arxiv.org/abs/...">` either cites a paper I am confident exists or the entry is written without a link (text-only citation).
- Insertion is idempotent: the apply script checks for an existing `<details class="bibliography-collapsible"` and skips if already present. None of the previously authored bibliographies were overwritten.
- Sections that already had a bibliography were not touched (verified by re-running and seeing 0 new insertions on second run).
- Entries grouped under h3 subheadings (Foundational Papers, Recent Advances, Surveys, Tools, Production Patterns, etc.) chosen for the section topic.
- Tools-of-the-trade sections received documentation-anchored bibliographies citing the official docs and foundational papers for the libraries they discuss (e.g., Section 19.2 cites the Transformers paper, TRL docs, and PEFT docs; Section 65.4 cites the vLLM paper, NVIDIA TensorRT-LLM, and HF TGI).

## Implementation artifacts

- `scripts/bib_data.py`: dictionary of 64 bibliographies for non-tools-of-the-trade sections.
- `scripts/bib_data_tot.py`: dictionary of 50 bibliographies for tools-of-the-trade sections, importing the helper `bib_block` from `bib_data`.
- `scripts/bib_apply.py`: idempotent applier that inserts each block right before `<nav class="chapter-nav">` and skips files that already have a bibliography block.
- `scripts/bib_insert.py`: single-file helper kept for ad-hoc use.
- `scripts/bib_check_targets.py`: small target-discovery utility.
- `bib_targets.txt`, `targets_with_titles.txt`: intermediate working files (114 paths, with titles and existing-bib status).
