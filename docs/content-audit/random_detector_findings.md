# Random Detector Findings — Round 1 (2026-05-17)

Random-sampling audit of 40 HTML pages drawn from the in-scope book tree (parts 1-16, appendices, capstone, front-matter). Seed = 20260517. The first 10 iterations took files of any size; iterations 11-40 filtered to files >=5KB.

## EXECUTIVE SUMMARY

### Headline numbers
- **40 iterations** completed against pages randomly sampled across all 16 parts and the front-matter / capstone / appendices roots.
- **178 distinct issue entries** logged (most iterations logged 3-8 issues each).
- **88 explicit recurrence-counter increments** across pages, confirming that several bug families are systemic rather than isolated.
- Only **2 pages out of 40** (iters 25 and 40) were essentially clean. Every other page had at least one substantive issue.

### Top 10 most-common patterns (ranked by recurrence count and per-page detection rate)

1. **Double-close `</strong>` in code-caption / comparison-table-title** — `<strong>Code Fragment N.M.K</strong>:</strong>` (the literal `</strong>` after the colon). Seen in iters 2, 3, 5, 7, 9, 10, 13, 18, 19, 21, 27, 31, 32 (13 distinct pages). Likely a single bad template substitution that has propagated everywhere captions are rendered. Trivial regex fix.
2. **Stale chapter number in breadcrumb / pagefind chapter meta** — file says module-67 but breadcrumb says "Chapter 65" or "Chapter 68" or "Chapter 64"; module-78 says "Chapter 74"; module-09 prereq link says "Chapter 11". Seen in iters 5, 9, 14, 18, 19, 24, 32, 34, 38 (9 distinct pages). Indicates one or more chapter-renumber passes were applied incompletely.
3. **Python code indent-rot inside dataclass / function bodies** — module-level invocation code (`spec = LLMProductSpec(...)`, `candidates = [...]`, examples) indented inside class/def bodies; in some cases entire function bodies sit at column 0. Seen in iters 3, 5, 9, 21, 22, 23, 26, 29, 32, 36 (10 pages, with iter 26 being the most severe). Causes the rendered code to look broken; copy-paste yields non-executable Python.
4. **Stale `<em>` numeric prefix inside `comparison-table-title`** — e.g., `<strong>Table 51.3.1:</strong> <em>39.3.1 Safety datasets...</em>`. Same renumber-pass family as #2 but specifically in table captions. Seen in iters 1, 3, 10, 15, 20, 35, 40 (7 pages).
5. **Bare prose section/chapter references that should be hyperlinks** — "Section 22.1 a tokenizer...", "Section 38 covers...", "Chapter 29 covers agent frameworks", "Section 3" (ambiguous). Seen in iters 2, 6, 7, 11, 12, 24, 31 (7 pages, often with multiple bare refs per page).
6. **`<div class="prerequisites">` not wrapped in canonical `callout` class** — sections all use `<div class="prerequisites">` while every other call-to-attention element uses `<div class="callout {kind}">`. Seen in iters 3, 9, 12, 21, 22, 23, 29, 30, 32, 33, 36 (11 pages).
7. **Trailing whitespace inside inline tags** — `<strong>Embeddings </strong>are` (space before closing tag). Seen in iters 3, 5, 9, 13, 29, 32, 36, 38, 39 (9 pages).
8. **`<figure>` wrapping a `<table>` labeled "Figure N.M.K"** — comparison tables miscategorized as figures in figcaption. Seen in iters 2, 7, 11, 18, 19, 27, 31 (7 pages). Book uses two table styles (`<table class="complex-table">` with `<div class="comparison-table">` wrapper VS `<figure><table>`) and the figure-wrapped form often gets the wrong "Figure" label instead of "Table".
9. **Image filename has wrong chapter prefix (and often dot-separated numbering)** — `images/figure-32-1-1.svg` on a chapter-20 page; `images/fig-37.3.1-*.svg` on a chapter-22 page; `images/ch26-sandbox-fishbowl.png` on a chapter-49 page. Seen in iters 2, 18, 19, 27, 32, 35, 37, 39 (8 pages).
10. **Heading text drift / mismatched anchor IDs / mismatched code-fragment numbers** — section H2 say "Message format and protocol libraries" with id `41-2-5-message-history-...`; prose says "Code Fragment 46.2.6" but caption shows 46.2.2; prose says "Figure 21.1.1" but caption says "Table 21.1.1"; "Pseudocode 35.8.1" inside section 47.2. Seen in iters 6, 7, 13, 18, 20, 26, 27, 32 (8 pages).

### Other notable patterns (lower-frequency but high-impact)

- **Malformed pagefind chapter-meta attribute** (`<span class="pagefind-meta-injected" b: LLM...` — chopped attribute name leaving stray `b:`, `c:`, `f:`). Iters 21, 26, 30, 33, 36. Suggests a regex substitution that chopped too much. Pagefind chapter labels broken on these pages.
- **Orphan content after `</main>` close** — sections concatenate a `tot-subsection` block after the original chapter-nav and footer, producing 2-5 nav/footer pairs per page. Iter 20 (2 pairs), iter 35 (5 pairs in one file). Reader navigation broken.
- **Code-output disconnected from preceding code** — iter 3 (DP-SGD output under a perplexity function), iter 9 (auto-linked HTML inside stdout), iter 13 (Garak output under a commented-only invocation), iter 21 (training output under a measurement function).
- **Placeholder text shipping in production** — `# implement <function_name>` Python comments (iters 22, 30), "Code Fragment h.7.N" / "Code Fragment I.2.1" appendix-letter placeholders (iters 20, 35), `<em>(Diagram to commission for final styling.)</em>` (iter 33).
- **Big Picture / Part Overview / meta description verbatim duplication** — iters 4, 8, 15, 17, 28 (Big Picture body equals meta description; some pages duplicate in 3 places).
- **`<h2>` inside `<div class="whats-next">`** instead of `<h3>`, elevating "What Comes Next" to the page's top-level TOC. Iters 18, 19, 24.
- **Visible / hidden corrupt `�` replacement character** (encoding mismatch in duplicated footers) — iter 35.
- **Auto-linker swallowed a content word leaving compound-word fragments** ("multi-Section 26.1", "llm apis" lowercased, "clip" linked to an audio chapter) — iters 5, 9, 39.

### Proposed validator scripts (35 new) — sketch by family

Each script returns a list of `(file, line_or_context, message)` and is targeted to be runnable from the repo root in under a minute against the 556-file HTML corpus.

**Markup well-formedness family (low false-positive, automatable fixes):**

```
check_double_close_tags.py                    # </strong>:</strong>  family
check_trailing_whitespace_in_inline_tags.py   # <strong>X </strong>
check_heading_open_close_match.py             # <h3>...</h4>
check_callout_div_balance.py                  # unclosed callout divs
check_main_chapter_nav_footer_order.py        # </main> before chapter-nav/footer
check_duplicate_chapter_nav_and_footer.py     # >1 nav + footer in <main>
check_pagefind_meta_attribute_wellformed.py   # "b:" / "f:" / "c:" stray attrs
check_replacement_character_in_html.py        # U+FFFD in body
```

**Numbering / labeling family (most also automate-fixable):**

```
check_table_caption_numbers.py                # stale <em> prefix in comparison-table-title
check_breadcrumb_chapter_number.py            # page-breadcrumb chapter mismatches file path
check_breadcrumb_chapter_title_present.py     # "Chapter N" without ": Title"
check_breadcrumb_vs_pagefind_chapter_meta.py  # two chapter strings on same page disagree
check_pagefind_chapter_meta_format.py         # part: vs chapter: prefix sanity
check_pagefind_part_meta_format.py            # part: value must start "Part [IVX]+"
check_pagefind_meta_completeness.py           # both part: and chapter: spans present
check_exercise_numbering_prefix.py            # Exercise C.S.K matches file
check_h2_numeric_prefix.py                    # <h2 id="..."> matches "N.M.K text"
check_heading_id_text_drift.py                # id slug matches heading text
check_caption_numbering_sequence.py           # no gaps in Figure/Table/Code Fragment
check_figure_table_counter_collision.py       # Figure and Table share a number
check_pseudocode_numbering.py                 # Pseudocode N.M.K chapter prefix
check_code_caption_label_format.py            # placeholder h.7.N / I.2.1
check_figure_filename_chapter_prefix.py       # image filename chapter prefix
check_long_truncated_image_filenames.py       # >80 chars or mid-word ending
check_figure_table_prose_caption_agreement.py # "Figure X" prose but caption Table X
check_table_labeled_as_figure.py              # <figure><table> with Figure caption
check_chapter_label_vs_link_target.py         # "Chapter 34" anchor pointing to ch42
check_chapter_nav_label_href_consistency.py   # nav-num text matches href filename
check_section_top_structure.py                # missing Big Picture etc.
check_section_end_structure.py                # missing whats-next / takeaway
check_whats_next_canonical_structure.py       # whats-next must use <h3> + div wrapper
check_whats_next_heading_level.py             # <h2> inside whats-next div
check_whats_next_chapter_end_contradiction.py # "Chapter N ends here" + "Section N.M"
check_whats_next_wrong_chapter.py             # whats-next references section in different chapter
```

**Content drift / placeholder family (mostly report-only):**

```
check_big_picture_vs_meta_description.py     # Big Picture == meta description
check_part_index_section_redundancy.py       # subtitle, big-picture, overview overlap
check_part_index_bottom_nav.py               # part-index needs chapter-nav
check_part_index_template_completeness.py    # subtitle, epigraph, hero illustration
check_meta_description_matches_section.py    # meta says Section 49.10 but file is 50.1
check_meta_description_punctuation.py        # ?. trailing
check_title_pipe_spacing.py                  # title pipe must have spaces
check_header_nav_indentation.py              # tabs in nav
check_truncated_alt_supplemental.py          # ends in "...."
check_alt_figcaption_word_boundary.py        # alt+figcaption splits mid-word/paragraph
check_implement_placeholder_comment.py       # "# implement foo"
check_lame_code_captions.py                  # "Defines X and Y" only
check_code_caption_boilerplate.py            # "encapsulates reusable logic..."
check_code_caption_matches_code.py           # caption mentions classes not in code
check_visible_todo_markers.py                # "(Diagram to commission...)" etc.
check_anchor_inside_code_output.py           # <a> tags inside code-output
check_code_output_alignment.py               # output identifiers vs code identifiers
check_commented_only_code_with_output.py     # output without executable code
check_html_entity_strings_in_code.py         # &quot; inside string spans
check_pygments_percent_misparse.py           # "% o" parsed as f-string spec
check_code_block_lang_mismatch.py            # Markdown content as lang-python
check_pseudocode_lang_attr.py                # pseudocode as lang-python
check_python_code_indent_rot.py              # dataclass body absorbs module-level code
check_arxiv_id_validity.py                   # future-dated YYMM IDs, 404s
check_github_io_benchmark_links.py           # user-page benchmark links
check_corporate_author_miscoded.py           # "Communication, S." for Seamless Communication
check_unlinked_section_references.py         # bare "Section N.M" without <a>
check_ambiguous_section_reference.py         # "Section 7" without subsection number
check_lowercased_acronym_anchor_text.py      # "llm apis" lowercased
check_polysemous_autolink.py                 # "clip" → audio chapter
check_hyphen_swallowed_by_autolink.py        # "multi-Section 26.1"
check_prev_nav_crosses_part_silently.py      # prev/next crosses part boundary
check_quiz_in_warning_callout.py             # self-check styled as warning
check_callout_class_palette.py               # rare callout classes (postmortem, cross-ref, production-pattern)
check_prerequisites_uses_callout_class.py    # <div class="prerequisites"> w/o callout
check_prereq_anchor_class_consistency.py     # mixed prereq-link classing
check_rare_anchor_classes.py                 # cross-ref / prereq-link / etc.
check_epigraph_markup_canonical.py           # <div class="epigraph"> vs <blockquote class="epigraph">
check_table_wrapper_canonical.py             # <table><caption> vs <div class="comparison-table">
check_bibliography_markup_canonical.py       # bib-entries div vs details.bibliography-collapsible
check_thin_content_pages.py                  # low text-to-markup ratio
check_structural_diversity.py                # <4 distinct structural element types
check_h2_callout_title_duplication.py        # H2 + immediately-following callout-title same text
check_duplicate_figure_caption.py            # two identical Figure N.M.K captions
check_duplicate_code_caption.py              # code-caption followed by stale p.caption
check_inline_numbered_lists.py               # "1. ... 2. ..." inside <p>
check_em_dash_comma_artifact.py              # " , " in SVG/headings (em-dash strip residue)
check_sentence_fragments_in_big_picture.py   # noun-phrase-list with no main verb
check_merged_list_items.py                   # <li> containing two "(X min)" markers
check_head_link_template_drift.py            # <head> stylesheet set differs from template
check_breadcrumb_book_title_consistency.py   # breadcrumb book title vs book-title-link
check_code_fragment_cross_reference.py       # "Code Fragment 46.2.6" with no matching caption
check_code_fragment_ordering.py              # 16.5.3 referenced before 16.5.1
check_empty_callouts.py                      # callout with no body
check_alt_supplemental_markup_consistency.py # supplemental inside vs outside figcaption
```

### Proposed fix scripts (high-leverage, auto-applicable)

Five fix scripts would land most of the value:

1. **`fix_double_close_tags.py`** — regex replace `(</(strong|em|b|i)>):\s*</\2>` with `\1:`. Will land ~13+ pages' fix in one pass.
2. **`fix_breadcrumb_and_pagefind_chapter_label.py`** — derive chapter number and title from the file path + `book_structure.yaml`; rewrite breadcrumb anchor text, pagefind chapter span, prereq prose chapter labels, and `<em>` prefixes in comparison-table-title captions. Single source of truth for chapter identity. Will land iters 5, 9, 14, 18, 19, 24, 32, 34, 38 + the seven `<em>`-prefix pages.
3. **`fix_callout_class_normalize.py`** — mapping table `{prerequisites → callout prerequisites, cross-ref → callout note, postmortem → callout practical-example, production-pattern → callout practical-example}`. Run with a `--report` first then `--apply`.
4. **`fix_section_end_structure.py`** — wrap orphan `<h2>What Comes Next</h2>` in `<div class="whats-next">`; convert nested `<h2>` to `<h3>`; merge duplicate chapter-nav + footer pairs after the first.
5. **`fix_pagefind_meta_attribute.py`** — regenerate the chapter-meta span entirely from the file path and `book_structure.yaml` rather than trying to repair the truncated attribute.

### Recommended next steps

1. Land scripts 1, 2, 5 above first. They are the highest-impact, lowest-risk fixes.
2. Run all validators in CI as a `--fail-on-new` mode (only fail if the issue count regresses).
3. Re-run this random-detector loop with seed 20260518 (next day) over a fresh 40-page sample to confirm pattern coverage and surface anything missed.
4. Add `book_structure.yaml`-derived single sources of truth for chapter title, chapter number, and part name to all templated injections (breadcrumb, pagefind meta, prev/next nav, prerequisites prose).

---

## Iteration 1 (part-15-llm-agentic-ai-research-frontiers/module-78-tools-of-the-trade/section-78.3.html)

### Issue: caption number mismatch inside `comparison-table-title`
- **Where**: line 60 — `<strong>Table 78.3.1:</strong> <em>65.3.1 Frontier benchmarks (2026).</em>`
- **What's wrong**: Caption has two table numbers; the `<em>` label starts with `65.3.1` while the chapter is 83. Stale number from a previous renumber pass.
- **Generalized pattern**: Inside `<div class="comparison-table-title">`, the `<strong>Table X.Y.Z:</strong>` number must match the chapter prefix of the enclosing file path (`section-<chap>.<sec>.html`). Detect when the bold label and the italic descriptor disagree on the leading numeric token. Regex sketch: `<div class="comparison-table-title">\s*<strong>Table (\d+\.\d+\.\d+):</strong>\s*<em>(\d+\.\d+\.\d+)\s` and assert the two captures are equal AND share the chapter prefix of the file.
- **Suggested fix**: Strip stale numeric prefix from `<em>` label; keep only descriptive caption. Cross-check chapter prefix matches file name.
- **TODO**: validator `check_table_caption_numbers.py`; fix `fix_stale_table_caption_numbers.py` (drop leading "N.M.K " from `<em>` content when it differs from the `<strong>Table N.M.K:</strong>`).

### Issue: external link points to unverifiable host
- **Where**: line 47 — `<a href="https://lukasberglund.github.io/MOC-bench/" ...>Mathematical Olympiad Programming benchmark (MOC)</a>`
- **What's wrong**: User-page on github.io for a benchmark; high risk of being either fabricated or transient. Benchmarks should link to a canonical source (arXiv, the maintaining lab, or a HuggingFace dataset card).
- **Generalized pattern**: External links matching `https://[a-z0-9-]+\.github\.io/[^/]+/?` that are presented as canonical benchmark/library references. Detect with `<a href="https://[^/]+\.github\.io/[^"]+"[^>]*>([^<]*\b(bench|benchmark|MOC|GPQA)\b[^<]*)</a>` and flag for verification.
- **Suggested fix**: Replace with the arXiv / HuggingFace / GitHub-repo canonical link.
- **TODO**: validator `check_github_io_benchmark_links.py`; suggest-list (no automated fix).

---

## Iteration 2 (part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html)

### Issue: figure asset filename has wrong chapter prefix
- **Where**: line 48 — `<img ... src="images/figure-32-1-1.svg"/>` inside section 20.1.
- **What's wrong**: SVG file is named `figure-32-1-1.svg` but lives under chapter 20. Either the asset is misnamed (should be `figure-20-1-1.svg`) or it's a leftover pointer from an earlier reorg.
- **Generalized pattern**: `<img src="(?:\./)?images/figure-(\d+)-(\d+)-(\d+)\.(?:svg|png|jpg|webp)"` where the first number must equal the chapter number derived from the file path (`module-\d\d-` or `section-(\d+)\.`). Flag mismatches.
- **Suggested fix**: Rename file and update src, or update src to match an existing renamed asset.
- **TODO**: validator `check_figure_filename_chapter_prefix.py`; fix script `fix_figure_filename_chapter_prefix.py` (probe existing same-prefix files; if a renamed asset exists, point to it; else flag).

### Issue: double-closing `</strong>` in code-caption
- **Where**: line 79 — `<div class="code-caption"><strong>Code Fragment 20.1.1</strong>:</strong> Bark synthesis...`
- **What's wrong**: Spurious extra `</strong>` after the colon; produces invalid HTML.
- **Generalized pattern**: Detect any `</TAG>:?</TAG>` sequence (mismatched closing of same tag with no opening). Regex: `<(strong|em|b|i)>[^<]*</\1>\s*:?\s*</\1>`.
- **Suggested fix**: Remove the spurious second `</strong>`.
- **TODO**: validator `check_double_close_tags.py`; fix `fix_double_close_tags.py` (regex replace, scoped to within `code-caption` and `figcaption`).

### Issue: figure number applied to a table
- **Where**: lines 88-105 — text introduces "**Figure 20.1.2**" and a `<figure>` block contains a `<table>` (no `<img>`) with `<figcaption><strong>Figure 20.1.2</strong>: Representative TTS systems...`
- **What's wrong**: A pure table is labeled "Figure" rather than "Table". Mixes the figure and table numbering schemes (book elsewhere uses `Table N.M.K` for tabular comparisons).
- **Generalized pattern**: `<figure>` blocks that contain `<table>` but no `<img>/svg/picture/canvas`, and whose `<figcaption>` starts with `<strong>Figure ...</strong>`. Regex (multiline): `<figure>[\s\S]*?<table[\s\S]*?</figure>` AND inside, `<figcaption>\s*<strong>Figure\b`.
- **Suggested fix**: Either wrap in `comparison-table` class with `comparison-table-title` (matching book's table style) or change `Figure` → `Table` in figcaption.
- **TODO**: validator `check_table_labeled_as_figure.py`; fix `fix_relabel_table_figure.py` (rewrite `<strong>Figure </strong>` to `<strong>Table </strong>` and also update prose mentions, with renumbering audit).

### Issue: cross-chapter forward references to sections by bare number
- **Where**: line 43 — "In Section 22.1 a tokenizer..."; line 57 — "see Section 33.1 for the video DiT variant"; line 152 — "connect this to the rectified flow discussion in Section 31.1".
- **What's wrong**: Inline text mentions sections in other chapters by number only, without an `<a href>`. Readers cannot click through; if numbering changes the cross-references rot silently.
- **Generalized pattern**: Bare prose mentions matching `\bSection \d+\.\d+(?:\.\d+)?\b` that are not inside an `<a>...</a>`. Same for `Chapter \d+`, `Part [IVX]+`.
- **Suggested fix**: Wrap each cross-reference in an `<a href>` to the linked section. If the link target does not exist, flag for content sync.
- **TODO**: validator `check_unlinked_section_references.py`; fix `fix_unlinked_section_references.py` (best-effort: resolve target by chapter/section number to a file path, wrap with `<a>`; queue unresolved for human review).

### Issue: section-relative reference uses bare "Section N"
- **Where**: line 153 — "the LLM-prosody-planner-plus-small-TTS factorization in Section 7".
- **What's wrong**: "Section 7" almost certainly means subsection 20.1.7 inside the current page, but the text is ambiguous (could be parsed as part 7 etc.). Single-digit section references are confusing.
- **Generalized pattern**: Self-check / prose `\bSection \d{1,2}\b` (no decimal point). Regex: `\bSection \d{1,2}\b(?!\.\d)`.
- **Suggested fix**: Replace with the fully qualified subsection number (e.g., "Section 20.1.7") or "subsection above" if intentionally vague.
- **TODO**: validator `check_ambiguous_section_reference.py`.

### Issue: long-distance prev nav crosses parts silently
- **Where**: line 175 — first section of Chapter 20 (Part V) `prev` link points back to `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.6.html`.
- **What's wrong**: Cross-part backward nav can be intentional (linear reading), but the absence of any visual cue or "Previous Part" label can disorient readers. The label says "Previous · Section 19.6" with no part hint.
- **Generalized pattern**: For any `nav.chapter-nav > a.prev`, compare `href` directory prefix vs. current file's directory prefix; flag when the part directory differs. Regex: parse `part-(\d+)-` prefix; alert when prev's part differs.
- **Suggested fix**: Include a "Previous Part" label or wrap nav with an explicit part-boundary marker in CSS.
- **TODO**: validator `check_prev_nav_crosses_part_silently.py`; (no automated fix; report only).

---

## Iteration 3 (part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.5.html)

### Issue: stray trailing space inside `<strong>` tags
- **Where**: line 36 — `<strong>Embeddings </strong>are`; line 344 — `<strong>Fine-tuned embeddings </strong>are`.
- **What's wrong**: Space inside the closing `</strong>` produces ugly bolded whitespace.
- **Generalized pattern**: `<strong>[^<]*?\s</strong>` (or similar for `em`, `b`, `i`, `code`). Detect any inline tag whose contents end with whitespace.
- **Suggested fix**: Trim trailing whitespace inside inline tags.
- **TODO**: validator `check_trailing_whitespace_in_inline_tags.py`; fix `fix_trailing_whitespace_in_inline_tags.py` (simple regex replace `(\s+)(</(?:strong|em|b|i|code)>)` → `\2\1`).

### Issue: double-closing `</strong>` in `comparison-table-title` (recurrence)
- **Where**: line 64 — `<strong>Table 16.5.1</strong>:</strong> <em>...`. Same pattern as iteration 2.
- **What's wrong**: Spurious second `</strong>`.
- **Generalized pattern**: covered by `check_double_close_tags.py`.
- **Suggested fix**: Drop the second `</strong>`. The bug is widespread; this is recurrence #1 from iter-2.
- **TODO**: same as iter 2 (counter +1).

### Issue: stale chapter prefix in exercise numbers
- **Where**: lines 354, 361, 368, 375, 382 — Exercises are labeled `14.5.1`, `14.5.2`, ..., `14.5.5` inside section 16.5.
- **What's wrong**: Section was probably renumbered from 14 to 16 but exercise numbers were not updated.
- **Generalized pattern**: For each section file at `module-MM-*/section-CC.SS.html`, all `<div class="callout exercise">` titles matching `Exercise (\d+)\.(\d+)\.(\d+)` should have leading two numbers == chapter `CC` and section `SS`. Regex: `Exercise (\d+\.\d+)\.\d+` inside `<div class="callout exercise">` titles; mismatched if chapter+section prefix differs from file's CC.SS.
- **Suggested fix**: Replace stale chapter prefix with current chapter number.
- **TODO**: validator `check_exercise_numbering_prefix.py`; fix `fix_exercise_numbering_prefix.py` (re-derive prefix from file path, rewrite leading numbers in exercise titles).

### Issue: out-of-order code-fragment numbering and prose forward-reference
- **Where**: line 136 — "<strong>Code Fragment 16.5.3</strong> shows this approach in practice." appears *before* fragments 16.5.1 (line 194) and 16.5.2 (line 232). Prose at line 138 says "Code Fragment 16.5.2 loads the model" but Code Fragment 16.5.2 (line 232) actually fine-tunes a model with `CosineSimilarityLoss`, it does not load the model from Section 3.1. Code Fragment 16.5.1's caption (line 194) is just "Preparing contrastive training data" but the prose at line 138 talks about *loading*, which is unrelated.
- **What's wrong**: Code-fragment numbering and prose pointers got disconnected during a re-ordering. Reader cannot trace the narrative.
- **Generalized pattern**: For each section, collect every `<strong>Code Fragment X.Y.Z</strong>` in `code-caption` (the actual numbering) and every prose mention of `Code Fragment X.Y.Z`. Detect (a) numbering gaps/jumps in declaration order; (b) prose mentions that reference an unseen-yet fragment without a forward-reference marker; (c) prose claims that contradict the captured caption ("loads the model" vs caption "Preparing contrastive training data").
- **Suggested fix**: Manual or semi-automatic re-numbering + re-write of prose pointers.
- **TODO**: validator `check_code_fragment_ordering.py` (catches a, b); flag report-only for (c).

### Issue: malformed Python code (dataclass body absorbs unrelated code)
- **Where**: lines 140-184 — `ContrastivePair` dataclass body contains `medical_pairs = [...]` (class-level), `pairs_to_dataset` defined as a class method, etc. The indentation is wrong; this is not runnable.
- **What's wrong**: Code formatting / indent-rot during Pygments highlighting or earlier transformation. The fragment is not executable as written.
- **Generalized pattern**: Inside `<pre><code class="pygments-highlighted lang-python">`, find any block where (a) a `@dataclass` class is followed by lines that are indented under it but assign to module-level-looking names like `medical_pairs`, or (b) any `def` is indented inside a class but its first parameter is not `self`. Regex (with context): look for `\n    [a-z_]+_pairs = \[` after `@dataclass`.
- **Suggested fix**: Re-indent the example so module-level variables sit at column 0.
- **TODO**: validator `check_python_code_indent_rot.py`; (no automated fix; flag for author).

### Issue: code-output does not match its code
- **Where**: lines 185-193 — code-output prints `recommendation: fine-tune`, `gap: 0.17...`, etc. — but the preceding code (lines 140-184) prepares contrastive data and never calls `should_finetune_embeddings`. The output belongs to Code Fragment 16.5.3 (line 257), not 16.5.1.
- **What's wrong**: Output block is stranded next to the wrong code block. Misleads readers.
- **Generalized pattern**: Pair `<div class="code-output">` with its preceding `<pre><code>` and check that printed variable names appear (`recommendation`, `gap`, `reasons` etc.) in that code. Heuristic: extract `print(...)`/function names from code, then check the output substring.
- **Suggested fix**: Move output below the correct code block.
- **TODO**: validator `check_code_output_alignment.py` (extract identifiers from code, intersect with output text; flag low overlap).

### Issue: irrelevant cross-link from "clip" to audio chapter
- **Where**: line 343 — `"fastening mechanism" now retrieved "bolt assembly," "adhesive bonding system," and "<a href="../../part-5-multimodal-llms/module-20-audio-music-generation/index.html">clip</a> attachment device."`
- **What's wrong**: The word "clip" (a mechanical fastener) is hyperlinked to "Audio & Music Generation" (where "clip" means audio clip). Auto-linking has mis-resolved a polysemous word.
- **Generalized pattern**: Detect any `<a>` whose anchor text is one of a known polysemous shortlist (`clip`, `cell`, `bank`, `plot`, `node`, `model`, `tank`, `train`, etc.) and whose href target's path keywords are unrelated to the surrounding sentence. Practical regex: anchor text from a polysemous shortlist that links to a `part-*/index.html` with no immediate keyword overlap in the same `<p>`.
- **Suggested fix**: Remove the spurious link (plain text).
- **TODO**: validator `check_polysemous_autolink.py` (report-only).

### Issue: empty `fun-note` callout swallowed by bibliography `<details>`
- **Where**: lines 396-422 — `<div class="callout fun-note">` opens, then `<div class="callout-title">Fun Fact</div>`, then immediately a `<details class="bibliography-collapsible" open>` with the Further Reading bibliography. There is no `<p>` content for the Fun Fact, and the fun-note `<div>` is never closed before the bibliography.
- **What's wrong**: HTML structure is broken: bibliography is nested inside fun-note, and fun-note has no actual content. The "Fun Fact" callout displays empty (or with bibliography inside it).
- **Generalized pattern**: Detect `<div class="callout fun-note">` (or any callout) whose first sibling element after `<div class="callout-title">` is `<details class="bibliography-collapsible">` (or a section/footer) rather than a `<p>` or `<ul>` of content. Equivalent: empty callout body. Also: unmatched `<div>` open before page-level structural elements.
- **Suggested fix**: Either fill the Fun Fact with content or remove the callout wrapper; close the fun-note div before the bibliography.
- **TODO**: validator `check_empty_callouts.py`; validator `check_callout_div_balance.py` (verify each `<div class="callout ...">` closes before any structural breakpoint).

### Issue: prerequisite block sits inside content but is not visually identified
- **Where**: lines 40-43 — `<div class="prerequisites"><h3 id="prerequisites">Prerequisites</h3>...`
- **What's wrong**: The `prerequisites` div is not a callout class (per book convention everything in the body uses `callout *`). The element is unstyled-by-convention.
- **Generalized pattern**: Detect `<div class="prerequisites">` and convert to `<div class="callout prerequisites">` (book uses callout-named classes everywhere else). Regex: `<div class="prerequisites">` (without `callout`).
- **Suggested fix**: Wrap as `class="callout prerequisites"` to inherit callout styling.
- **TODO**: validator `check_prerequisites_uses_callout_class.py`; fix `fix_prerequisites_callout_class.py`.

---

## Iteration 4 (part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/index.html)

### Issue: Big Picture content is verbatim copy of meta description
- **Where**: line 7 meta description "Chapter 33: Cross-Modal Reasoning and Multimodal RAG. Joint embedding spaces, multimodal retrieval, when to retrieve vs reason, and production multimodal reasoning." vs. line 27 Big Picture body "Joint embedding spaces, multimodal retrieval, when to retrieve vs reason, and production multimodal reasoning."
- **What's wrong**: Big Picture is a chapter-level callout meant to set perspective for the reader; here it's just a section-list summary copied from the meta description. Placeholder quality.
- **Generalized pattern**: For every `index.html` under a `module-NN-*` folder, compute string similarity between the `<meta name="description" content="...">` value (after stripping the leading "Chapter N: title.") and the text inside `<div class="callout big-picture">`. Flag when normalized-Levenshtein > 0.8 or when both strings, after lowercasing and stripping leading title, share >70% of word 4-grams.
- **Suggested fix**: Rewrite the chapter Big Picture so it explains *why* the chapter matters and what the reader will be able to do; do not duplicate the meta description.
- **TODO**: validator `check_big_picture_vs_meta_description.py`; (no automated fix; report list of pages whose Big Picture is template-quality).

### Issue: chapter index missing `part:` pagefind-meta injection
- **Where**: line 24 — only `data-pagefind-meta="chapter:..."` is present; no `part:` injection.
- **What's wrong**: Other index pages emit *two* hidden spans (`part:` and `chapter:`) so Pagefind search results can show the part context; this index emits only `chapter:`.
- **Generalized pattern**: For each `index.html` (chapter or part level), confirm presence of both `data-pagefind-meta="part:..."` and (for chapter index) `data-pagefind-meta="chapter:..."`. Regex: count occurrences of `data-pagefind-meta="part:` and `data-pagefind-meta="chapter:` and flag chapter-index pages with zero `part:`.
- **Suggested fix**: Inject the missing `<span class="pagefind-meta-injected" data-pagefind-meta="part:Part VII: Retrieval & Information Extraction with LLMs" hidden=""></span>` next to the chapter span.
- **TODO**: validator `check_pagefind_meta_completeness.py`; fix `fix_inject_part_meta.py` (derive from breadcrumb).

### Issue: indentation inside `<nav class="header-nav">` uses tabs while other pages use spaces
- **Where**: lines 17-18 — tab-indented `<a>` lines.
- **What's wrong**: Inconsistent whitespace; downstream diff tools and template comparisons trip over mixed indentation. Most index pages have flush-left `<a>` lines here.
- **Generalized pattern**: Inside `<nav class="header-nav">...</nav>`, detect leading `\t` chars on `<a>` lines. Regex: `<nav class="header-nav">\s*\n(\t+<a)` (multiline).
- **Suggested fix**: Strip leading tabs from those lines.
- **TODO**: validator `check_header_nav_indentation.py`; fix `fix_header_nav_indentation.py` (remove leading whitespace inside the nav).

### Issue: chapter-index page missing pygments.css link (template consistency)
- **Where**: lines 9-12 — only `book.css`, no `pygments.css`.
- **What's wrong**: Other chapter-index pages include `pygments.css` even when they have no code blocks (template uniformity). Worth confirming whether this is intentional or an omission.
- **Generalized pattern**: Confirm every `index.html` under `module-NN-*` carries the same `<link>` set as the templates/chapter-index.html. Diff `<head>` against template.
- **Suggested fix**: Add missing stylesheet links to align with template.
- **TODO**: validator `check_head_link_template_drift.py`.

---

## Iteration 5 (part-14-designing-llm-agent-products/module-67-ideation/section-67.7.html)

### Issue: breadcrumb and chapter-meta reference wrong chapter number
- **Where**: line 27 — breadcrumb says "Chapter 65: LLM Strategy & Use Case Prioritization"; line 31 — pagefind chapter meta also says "Chapter 65"; line 28 — page-current div correctly says "Section 67.7".
- **What's wrong**: The file lives under `module-67-ideation/section-67.7.html` so the chapter is 67, not 65. Pagefind, breadcrumb, and link text reference an old chapter number from before a renumber pass. The page-current shows 67.7 so prose/numbering are correctly 67.7, but every chapter-level pointer is stale.
- **Generalized pattern**: For each `section-CC.SS.html` file under `module-CC-*`, parse the breadcrumb `<a href="index.html">Chapter N: ...</a>` and assert `N == CC`. Same for `<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter N: ...">`. Regex: `<a href="index.html">Chapter (\d+):` inside `page-breadcrumb`, and `data-pagefind-meta="chapter:Chapter (\d+):`.
- **Suggested fix**: Replace stale chapter number with the chapter derived from the directory path.
- **TODO**: validator `check_breadcrumb_chapter_number.py`; fix `fix_breadcrumb_chapter_number.py`.

### Issue: link text lowercased ("llm apis" instead of "LLM APIs")
- **Where**: line 42 — `<a href="...">llm apis</a>` (the second anchor).
- **What's wrong**: Acronym capitalization lost — should be "LLM APIs". Probably from an auto-link insertion that lowercased the anchor text.
- **Generalized pattern**: Detect anchor text equal to a known acronym (case-insensitive match) but in lowercase. Shortlist: `llm`, `api`, `rag`, `gpu`, `cnn`, `rnn`, `ml`, `ai`, `dpo`, `rlhf`, `tts`, `asr`, `ocr`, `sql`, `mlops`, `cicd`, `dpr`, `nlp`, `cli`, `sdk`. Regex: `<a [^>]*>\s*((?:llm|api|rag|gpu|...) ?(?:[a-z]+s?)?)\s*</a>` where the anchor body is fully lowercase but starts with an acronym.
- **Suggested fix**: Re-case anchor body to canonical form.
- **TODO**: validator `check_lowercased_acronym_anchor_text.py`; fix `fix_lowercased_acronym_anchor_text.py` (maintained dictionary of acronym → canonical case).

### Issue: figure numbering gap (Figure 67.7.2 missing)
- **Where**: line 45 — `Figure 67.7.1`; line 312 — `Figure 67.7.3`; line 365 — `Figure 67.7.4`; line 560 — `Figure 67.7.5`. No `Figure 67.7.2` anywhere.
- **What's wrong**: Reader expects a Figure 67.7.2 between 67.7.1 (hero) and 67.7.3 (workshop diagram). Either a figure was deleted without renumbering or the second figure was supposed to be inserted.
- **Generalized pattern**: Per page, collect all `Figure (\d+\.\d+)\.(\d+)` numbers and assert they form a contiguous 1..N sequence. Same for `Table N.M.K` and `Code Fragment N.M.K`.
- **Suggested fix**: Renumber later figures down, or supply the missing Figure 67.7.2.
- **TODO**: validator `check_caption_numbering_sequence.py`; fix `fix_renumber_captions.py` (renumber + update all in-page references).

### Issue: indent-rot in Python code blocks (recurring)
- **Where**: lines 99-138 (`ReadinessAssessment`), lines 150-189 (`UseCase`), lines 369-393 (`RICEScore`). In each, the example invocation (`assessment = ...`, `candidates = [...]`, `use_cases = [...]`) is indented inside the class definition.
- **What's wrong**: Same pattern as iter 3.
- **Generalized pattern**: covered by `check_python_code_indent_rot.py`.
- **Suggested fix**: De-indent module-level code.
- **TODO**: same as iter 3 (counter +3).

### Issue: f-string with `%` escape gone wrong in Pygments output
- **Where**: line 175 — `"Lawyers spend 60</span><span class="si">% o</span><span class="s2">f time on routine clauses"` — string literal `"Lawyers spend 60% of time"` got tokenized as if `% o` were a format spec.
- **What's wrong**: The plain string literal contains `%` followed by space and `o` — Pygments mis-tokenized this. The rendered code looks visually OK but the syntax highlighting class breaks the string into "60", `% o`, and `f time`.
- **Generalized pattern**: Inside `<pre><code class="lang-python">`, detect `% ` (percent-space) inside what should be a single string literal. Heuristic: `<span class="s2">[^<]*\d</span><span class="si">% \w</span>` outside f-strings.
- **Suggested fix**: Re-highlight with corrected lexer or escape the `%`.
- **TODO**: validator `check_pygments_percent_misparse.py`; (no automated fix; rerun pygments highlighter with explicit lexer hints).

### Issue: placeholder-quality code captions
- **Where**: line 147 — "Defines total_score and weakest_pillar"; line 196 — "Defines estimated_annual_value and passes_screening"; line 402 — "Implementation of score".
- **What's wrong**: Captions just enumerate method names instead of explaining what the snippet teaches the reader (e.g., "Four-pillar readiness scoring with a recommendation routine that gates pilot vs. enterprise commitment.").
- **Generalized pattern**: Detect `<div class="code-caption">` whose body matches `^\s*Defines? [a-z_]+( and [a-z_]+)?\s*$` or `^\s*Implementation of [a-z_]+\s*$` or similar template phrases.
- **Suggested fix**: Replace with one-sentence description of the concept the code demonstrates.
- **TODO**: validator `check_lame_code_captions.py`; (no automated fix; flag for author rewrite).

### Issue: double-closing `</strong>` in code-caption (recurrence)
- **Where**: line 402 — `<strong>Code Fragment 67.7.3</strong>:</strong>`; line 65 — table title (already covered).
- **What's wrong**: Same as before.
- **TODO**: covered by `check_double_close_tags.py`. Counter +2.

### Issue: list item conflates two distinct workshop phases
- **Where**: lines 222-224 — workshop phases list. Line 223 contains: "LLM Fit Screening (20 min): ... Would a human expert need context and judgment?, Data Availability Check (20 min): For each surviving candidate, assess whether..."
- **What's wrong**: A single `<li>` runs two phases together (LLM Fit Screening and Data Availability Check), separated only by a comma. The next `<li>` is the impact phase. Visible result: workshop becomes 3 listed phases instead of 4 (yet diagram and prose say 4).
- **Generalized pattern**: For ordered/unordered lists describing N phases, parse explicit phase counters ("Phase X" or "(Y min)") and assert list-item count matches. Heuristic: a single `<li>` containing two occurrences of `\(\d+ min\)` is suspicious.
- **Suggested fix**: Split the list item.
- **TODO**: validator `check_merged_list_items.py`; (no automated fix; flag).

---

## Iteration 6 (part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.2.html)

### Issue: breadcrumb / pagefind chapter meta omit chapter title
- **Where**: line 23 — `<a href="index.html">Chapter 41</a>` (no title); line 27 — pagefind meta `chapter:Chapter 41` (no title); other pages include the chapter title.
- **What's wrong**: Breadcrumb / search-result chapter label is less informative. Pagefind search will show "Chapter 41" instead of "Chapter 41: Conversational AI Tools of the Trade", which the chapter-nav up-link (line 291) confirms is the correct title.
- **Generalized pattern**: Inside `page-breadcrumb`, the last `<a href="index.html">Chapter N</a>` should have the format `Chapter N: <title>`. Regex: `<a href="index.html">Chapter \d+</a>` (without colon-title).
- **Suggested fix**: Append the chapter title from `nav.chapter-nav > a.up > nav-title`.
- **TODO**: validator `check_breadcrumb_chapter_title_present.py`; fix `fix_breadcrumb_chapter_title.py` (look up chapter title from sibling index.html or chapter-nav).

### Issue: heading text mismatches anchor id
- **Where**: line 81 — `<h2 id="41-2-5-message-history-and-protocol-libraries">Message format and protocol libraries</h2>`; line 229 — `<h2 id="41-2-11-an-extended-comparison">Choosing among the orchestration frameworks</h2>`.
- **What's wrong**: anchor IDs encode an earlier heading text. Cross-links pointing at these anchors may still resolve, but anyone searching by id-keyword will not find the right section. Also indicates content drift between the heading and the anchor.
- **Generalized pattern**: For each `<h([1-6]) id="(.+?)">(.+?)</h\1>`, slugify the heading text and compare against the id (after stripping leading `\d+-\d+-\d+-` prefix). Flag if Levenshtein distance > 5 or if no shared content tokens.
- **Suggested fix**: Rewrite ids to match current heading text.
- **TODO**: validator `check_heading_id_text_drift.py`; fix `fix_regenerate_heading_ids.py` (with a redirect map to old ids for backward compat).

### Issue: bibliography section uses ad-hoc `bib-entries` div, not the canonical `details.bibliography-collapsible`
- **Where**: lines 268-288 — `<h2 id="41-2-12-references">...</h2><div class="bib-entries">...` (no `<details>` wrapper, no `<summary>Further Reading</summary>`).
- **What's wrong**: Other pages (see iter 1, iter 3) wrap further-reading in `<details class="bibliography-collapsible" open><summary><strong>Further Reading</strong></summary><section class="bibliography">...`. This page uses a `<div class="bib-entries">` without a collapsible/summary, which is inconsistent and may break book-wide CSS expectations.
- **Generalized pattern**: For every section page that contains `bib-entry-card` or `bib-ref`, assert its containing element is `<details class="bibliography-collapsible">` (or `<section class="bibliography">` inside one). Flag `<div class="bib-entries">` as legacy markup.
- **Suggested fix**: Wrap in canonical bibliography markup. May also want to standardize heading from "References" to "Further Reading".
- **TODO**: validator `check_bibliography_markup_canonical.py`; fix `fix_bibliography_markup.py`.

### Issue: bare cross-chapter reference ("Chapter 29 covers agent frameworks")
- **Where**: line 201 — "Chapter 29 covers agent frameworks; the libraries here are for human-facing conversational AI."
- **What's wrong**: Bare prose chapter reference, not hyperlinked (same as iter 2 issue).
- **Generalized pattern**: covered by `check_unlinked_section_references.py` extended to `\bChapter \d+\b`.
- **TODO**: same as iter 2 (counter +1).

### Issue: section lacks "What Comes Next" / Key Takeaway / Self-Check
- **Where**: end of `<main>` (line 295). The section closes after Choosing among the orchestration frameworks + fun note + references; no "What Comes Next" callout, no Key Takeaway, no exercises.
- **What's wrong**: Most section pages (see iters 2, 3, 5) end with `whats-next` + `key-takeaway` + sometimes `self-check`. This section is a "Libraries and Frameworks" survey that ends after references, breaking the book's chapter-end consistency.
- **Generalized pattern**: For each `section-N.M.html` (not index.html), assert presence of at least one of: `<div class="whats-next">`, `<div class="callout key-takeaway">`, `<div class="callout self-check">` OR `<section class="exercises">`. Flag pages missing all four.
- **Suggested fix**: Add a Key Takeaway and What Comes Next at minimum.
- **TODO**: validator `check_section_end_structure.py`; (no automated fix; flag for author).

### Issue: HTML entity quotes inside code blocks (`&quot;`)
- **Where**: lines 96-118 — all string literals in the Python code use `&quot;` rather than literal `"`. Other Pygments-highlighted code blocks elsewhere in the book use literal `"` (after `<span class="s2">"text"</span>`).
- **What's wrong**: Mixed encoding of strings across the book; copy-paste from this page yields code with `&quot;` artifacts that won't run. Inconsistent rendering between sections.
- **Generalized pattern**: Inside `<pre><code class="pygments-highlighted ..." ...>`, detect occurrences of `&quot;` or `&apos;` that are inside `<span class="s2">` / `<span class="s1">` / etc. (string token classes).
- **Suggested fix**: Re-render with the highlighter set to UTF-8 literal strings.
- **TODO**: validator `check_html_entity_strings_in_code.py`; fix `fix_decode_html_entity_strings_in_code.py` (substitute `&quot;` → `"`, `&apos;` → `'` only inside string-token spans).

---

## Iteration 7 (part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html)

### Issue: bibliography author parsed as last-name "Communication"
- **Where**: line 119 prose — `Meta's SeamlessM4T-v2 (Communication, 2023)`; line 149 bibliography — `Communication, S. (2023). <em>SeamlessM4T...`
- **What's wrong**: The corporate authorship "Seamless Communication" team was parsed as last-name "Communication" with initial "S." This produces both a wrong bibliography line and a wrong parenthetical citation in prose.
- **Generalized pattern**: Bibliography entries beginning with single-word "last names" that are common nouns (`Communication`, `Research`, `Team`, `Labs`, `OpenAI`, `Anthropic`, ...) followed by `, [A-Z]\.` indicate likely corporate authors miscoded. Regex: `<div class="bib-ref"><a [^>]*>(?:[A-Z][a-z]+)+, [A-Z]\.\s*\(\d{4}\)` where the surname is in a known corporate-noun shortlist.
- **Suggested fix**: Replace with proper corporate-author convention (`Seamless Communication Team (2023)` or `Meta AI (2023)`); update prose citations accordingly.
- **TODO**: validator `check_corporate_author_miscoded.py`; (no automated fix; flag for author).

### Issue: cross-chapter references "Section 38" / forward-section that may not exist
- **Where**: line 36 — "(Section 38 covers the realtime stack in detail)"; line 126 — "Section 38 on streaming multimodal".
- **What's wrong**: Section 38 is at chapter level (chapter 38 in part 8). "Section 38" without subsection is ambiguous; the realtime/voice content is actually in module 40 / Chapter 40 (voice & realtime multimodal). Likely a stale reference from an earlier numbering pass.
- **Generalized pattern**: covered by `check_unlinked_section_references.py` extended with "resolve target file"; flag when no `module-NN/section-N.M.html` matches.
- **Suggested fix**: Replace with correct chapter/section pointer or link.
- **TODO**: extension of the validator: include a resolver that checks if the referenced section file exists; emit "unresolved cross-reference" warning.

### Issue: "What Comes Next" contradicts chapter boundary
- **Where**: line 141 — "Chapter 20 ends here, with audio fully covered from generation through editing through recognition. Section 20.6 opens on the modality with the steepest 2025-2026 capability gain: video."
- **What's wrong**: Asserts the chapter ends at 20.5 but then mentions 20.6 (in the same chapter) as the next section. Reads as a self-contradiction. The chapter title (line 159) says "Audio, Music, and Video Generation" so 20.6 (video) does belong in chapter 20.
- **Generalized pattern**: Inside `<div class="whats-next">`, detect prose claiming "Chapter N ends here" together with reference to "Section N.M" where N matches. Regex: text containing `Chapter (\d+) ends here` and `Section \1\.\d+`.
- **Suggested fix**: Rewrite: "This section ends our audio coverage; next, Section 20.6 turns to video."
- **TODO**: validator `check_whats_next_chapter_end_contradiction.py`; (no automated fix; flag for author).

### Issue: `figure` containing a `<table>` (recurrence)
- **Where**: lines 85-101 — same pattern as iter 2, line 88-105. Markup: `<figure>` then `<table>` then `<figcaption><strong>Figure 20.5.1</strong>`. No image element.
- **What's wrong**: A pure comparison table labeled as a Figure rather than a Table.
- **TODO**: covered by `check_table_labeled_as_figure.py`. Counter +1.

### Issue: double-closing `</strong>` in code-caption (recurrence)
- **Where**: line 78 — `<strong>Code Fragment 20.5.1</strong>:</strong>`.
- **TODO**: covered by `check_double_close_tags.py`. Counter +1.

---

## Iteration 8 (part-4-training-adaptation/index.html)

### Issue: `<title>` separator missing space before pipe
- **Where**: line 8 — `<title>Part IV: LLM Training and Adaptation| Building Conversational AI with LLMs and Agents</title>`.
- **What's wrong**: Missing space — should be `Adaptation | Building`. Other pages (e.g., section-41.2 line 8: `Section 41.2: Libraries and Frameworks | Building...`) use ` | ` with surrounding spaces.
- **Generalized pattern**: For every `<title>...</title>` containing `|`, assert pattern `^.* \| .*$` (single pipe with spaces on both sides).
- **Suggested fix**: Insert space before the pipe.
- **TODO**: validator `check_title_pipe_spacing.py`; fix `fix_title_pipe_spacing.py` (regex `(\S)\|` → `\1 |` and `\|(\S)` → `| \1`).

### Issue: tab indentation in `<nav class="header-nav">` (recurrence)
- **Where**: lines 17-18 — tab-indented `<a>` tags.
- **TODO**: covered by `check_header_nav_indentation.py`. Counter +1.

### Issue: missing bottom navigation on part-index
- **Where**: line 115 — `<footer>` immediately after `</div>` for chapter-card-list. No `<nav class="chapter-nav">` linking to previous/next part.
- **What's wrong**: Other part-index pages (e.g., per repo `bottom-nav-fix-report.md` history) include a `<nav class="chapter-nav">` with `prev`/`up`/`next` links to neighboring parts.
- **Generalized pattern**: For each `part-NN-*/index.html`, assert a `<nav class="chapter-nav">` exists with at least a `next` or `prev` to a sibling part-index. Regex: presence of `<nav class="chapter-nav">` block.
- **Suggested fix**: Add part-level nav linking to part-3 and part-5.
- **TODO**: validator `check_part_index_bottom_nav.py`; fix `fix_part_index_bottom_nav.py` (generate links from `toc.html` or directory listing).

### Issue: Big Picture overlaps meta description (recurrence-style)
- **Where**: line 7 meta description "Off-the-shelf models only get you so far." vs. line 45 Big Picture body opening "Off-the-shelf models only get you so far. Part IV teaches you to bend LLMs to your needs..."
- **What's wrong**: First sentence of Big Picture exactly duplicates the meta description. The Big Picture should provide more depth than the meta description, not repeat it verbatim.
- **TODO**: covered by `check_big_picture_vs_meta_description.py`. Counter +1.

### Issue: chapter-subtitle uses period-ending sentence; Part Overview restates same content
- **Where**: line 26 — `<p class="chapter-subtitle">Generating data, fine-tuning models, distilling knowledge, and aligning with human preferences.</p>`; line 37 — Part Overview repeats nearly the same enumeration.
- **What's wrong**: Subtitle, big picture, and part overview are all telling the reader the same thing (a comma-separated list of topics). Reader gets four paragraphs of "this part is about X" without ever learning *why*.
- **Generalized pattern**: For each part-index, compute Jaccard similarity over content words between subtitle, big-picture, and part-overview first paragraph. Flag when any pair is > 0.6.
- **Suggested fix**: Differentiate: subtitle = tagline; big-picture = motivation; part-overview = roadmap.
- **TODO**: validator `check_part_index_section_redundancy.py`; (no automated fix; flag for author).

### Issue: alt-supplemental description is truncated
- **Where**: line 29 — `<span class="alt-supplemental" hidden="" id="part-opener-desc">a Kurzgesagt-meets-XKCD visual metaphor ... preferenc...</span>` (ends with "pref...").
- **What's wrong**: The supplemental alt description ends mid-word (`preferenc...`). Looks like the auto-generated description was truncated to N characters without trailing-word respect.
- **Generalized pattern**: `<span class="alt-supplemental" ...>.*?\.\.\.</span>` — detect ellipsis-ending truncation. Regex: `class="alt-supplemental"[^>]*>[^<]*?\.\.\.</span>`.
- **Suggested fix**: Either extend the description to a full sentence ending or truncate at a complete word boundary.
- **TODO**: validator `check_truncated_alt_supplemental.py`; fix `fix_trim_alt_supplemental_at_word_boundary.py`.

---

## Iteration 9 (part-14-designing-llm-agent-products/module-67-ideation/section-67.5.html)

### Issue: chapter number mismatch (breadcrumb & pagefind), Recurrence
- **Where**: line 27 and 31 — "Chapter 64: LLM Product Management"; file is `module-67/section-67.5.html`.
- **TODO**: covered by `check_breadcrumb_chapter_number.py`. Counter +1.

### Issue: auto-linked HTML inside code-output (`<a>` tag inserted into stdout)
- **Where**: line 128 — `Model recommendation: Frontier model (GPT-4o, Claude 3.5 Sonnet) with <a href="../../part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html">guardrails</a>`.
- **What's wrong**: The output block is supposed to reproduce what `print()` would emit. Auto-linking pass inserted an `<a>` for "guardrails" inside the rendered stdout. Misleads readers (no code would print HTML) and breaks copy-paste fidelity.
- **Generalized pattern**: Detect `<a ...>...</a>` anywhere inside `<div class="code-output">...</div>`. Regex: `<div class="code-output">[^<]*(?:<(?!/div|span)[^>]*>)*<a [^>]*>` — more loosely: any `<a` tag that appears between `<div class="code-output">` and its closing `</div>`.
- **Suggested fix**: Strip `<a>` wrappers inside code-output, keep anchor text only.
- **TODO**: validator `check_anchor_inside_code_output.py`; fix `fix_strip_anchors_inside_code_output.py`.

### Issue: stale chapter prefix; placeholder code captions; indent-rot — all recurrences
- **Where**: line 38 trailing space in `<strong>` (recurrence); line 133 placeholder caption "Define RiskLevel, LLMProductSpec; implement model_tier_recommendation" (recurrence of lame-caption pattern); lines 96-125 indent-rot inside LLMProductSpec class; line 133 double-close `</strong>`.
- **TODO**: All covered by previously listed validators. Counter +5.

### Issue: prereq cross-link uses non-standard class `prereq-link`
- **Where**: line 42 — `<a class="prereq-link" href="...">Section 42.1</a>` while two other anchors in the same paragraph are unclassed.
- **What's wrong**: Inconsistent classing on cross-links; CSS rules for `.prereq-link` may exist (or not), and the inconsistency suggests an incomplete migration.
- **Generalized pattern**: Inside the `prerequisites` div, all anchor tags should use the same class (or none). Flag mixed class usage.
- **Suggested fix**: Normalize class usage (all or none).
- **TODO**: validator `check_prereq_anchor_class_consistency.py`.

---

## Iteration 10 (part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.3.html)

### Issue: stale numeric prefix in `<em>` caption (recurrence of iter 1)
- **Where**: line 51 — `<strong>Table 51.3.1:</strong> <em>39.3.1 Safety datasets (2026).</em>` — italic descriptor begins with "39.3.1" but the chapter is 51.
- **TODO**: covered by `check_table_caption_numbers.py`. Counter +1. The pattern recurs across "Tools of the Trade" sections specifically, suggesting these chapters were renumbered from 39 / 65 / etc. without updating embedded labels.

### Issue: section lacks Big Picture / epigraph / objectives / takeaway
- **Where**: lines 27-28 — no `<div class="callout big-picture">` callout, no `<blockquote class="epigraph">`, no Learning Objectives, no Key Takeaway, no Self-Check, no Further Reading.
- **What's wrong**: While "Tools of the Trade" sections are typically leaner, the surrounding sections (51.1 Platforms, 51.2 Libraries, 51.4 Models) likely follow the same scaffold; this 51.3 section drops the entire structural frame.
- **Generalized pattern**: For sections deeper than `section-*.1`, assert presence of at least one callout (big-picture OR key-insight OR practical-example) at top of `<main>` content. Regex: `<main[^>]*>(?:\s|<span[^>]*>[^<]*</span>)*<(?!div class="callout)` indicates missing top callout.
- **Suggested fix**: Add a Big Picture explaining why dataset choice matters for safety eval; add Key Takeaway with 3-4 bullets.
- **TODO**: validator `check_section_top_structure.py`; (no automated fix; flag for author).

### Issue: missing Further Reading / bibliography section
- **Where**: page ends at line 94 with a warning callout before chapter-nav.
- **What's wrong**: Dataset survey with no canonical-references bibliography. Other tools-of-the-trade sections (e.g., iter 1 `section-78.3.html`) close with a `<details class="bibliography-collapsible">`.
- **Generalized pattern**: For each `tools-of-the-trade/section-*.3.html` (datasets-and-benchmarks pattern), assert presence of `<details class="bibliography-collapsible">` or `<section class="bibliography">`.
- **Suggested fix**: Add Further Reading listing the canonical papers (Mazeika 2024, Zou 2023, etc.) referenced in the bullets.
- **TODO**: validator `check_tools_of_the_trade_section_completeness.py`.

### Issue: small file (<5KB after iter 10) — page is a thin survey
- **Where**: file size ~10KB but content is minimal — 4 H2 sections of 3-4 bullets each plus one warning.
- **What's wrong**: Even though it's above the 5KB threshold, the content density is low for a "Datasets & Benchmarks" page — no per-dataset code example, no MTEB-style comparison snippet, no benchmark-loading prose. Compared to peer pages (section-78.3.html iter 1 is even thinner but section-19.3.html is much richer), this one feels stub-y.
- **Generalized pattern**: For each section page, compute content-to-markup ratio. Flag pages where `text-only / total bytes` < 0.20.
- **Suggested fix**: Add a code fragment showing how to load each benchmark, plus a section on `lm-evaluation-harness` integration.
- **TODO**: validator `check_thin_content_pages.py`; (no automated fix; flag for author).

---

## Iteration 11 (part-5-multimodal-llms/module-20-audio-music-generation/section-20.9.html)

### Issue: "What Comes Next" references a section in a different chapter
- **Where**: line 145 — "Section 33.5 closes the chapter with the hardest open problem in video AI..."
- **What's wrong**: We're in section 20.9 of Chapter 20; "Section 33.5 closes the chapter" implies chapter 33. Pagefind chapter meta (line 29) confirms Chapter 20. The next-section link (line 164) goes to section 20.10. Either Section 33.5 is a stale link from when video lived in Chapter 33, or the "What Comes Next" was carried over from an old layout.
- **Generalized pattern**: Inside `<div class="whats-next">`, detect any `\bSection (\d+)\.(\d+)\b` whose chapter number `\1` differs from the current file's chapter prefix. Regex: parse chapter from filename `section-(\d+)\.\d+\.html` and find any `Section \d+\.\d+` reference in whats-next whose chapter number doesn't match.
- **Suggested fix**: Update to the correct in-chapter target (here, probably "Section 20.10").
- **TODO**: validator `check_whats_next_wrong_chapter.py`; fix `fix_whats_next_chapter_pointer.py` (resolve from chapter-nav next link).

### Issue: Big Picture sentence fragment
- **Where**: line 36 — "Removing an unwanted object from a finished shot (inpainting), replacing the style or season of a video (style transfer), doubling the frame rate of a vintage recording (frame interpolation with RIFE, FILM), upscaling a 480p archive to 4K (Real-ESRGAN, Topaz Video AI), and stitching all of this into a production pipeline with the DAW-equivalent of audio editing in Section 20.4."
- **What's wrong**: This is a comma-spliced list with no main clause — there's no verb governing the noun phrases. The sentence reads as a fragment because it starts with a participle clause and has no "is", "involves", etc.
- **Generalized pattern**: Detect long sentences (>40 words) where the first token is a gerund/participle (`Removing`, `Doing`, `Setting`, etc.) and that contain a comma-separated list culminating in "and ..." with no main-verb predicate.
- **Suggested fix**: Add a topic clause: "The 2026 production workflow looks like this: removing an unwanted object..."
- **TODO**: validator `check_sentence_fragments_in_big_picture.py`; (no automated fix; flag for author).

### Issue: breadcrumb omits chapter title (recurrence iter 6)
- **Where**: line 26 — `<a href="index.html">Chapter 20</a>` (no `: Audio, Music, and Video Generation`).
- **TODO**: covered by `check_breadcrumb_chapter_title_present.py`. Counter +1.

### Issue: figure-containing-table (recurrence iter 2/7)
- **Where**: lines 99-116 — `<figure>` with `<table>` and `<figcaption><strong>Figure 20.9.1</strong>`. 
- **TODO**: covered by `check_table_labeled_as_figure.py`. Counter +1.

### Issue: double-close `</strong>` in code-caption (recurrence)
- **Where**: line 88 — `<strong>Code Fragment 20.9.1</strong>:</strong>`.
- **TODO**: counter +1.

### Issue: cross-chapter bare section references (recurrence)
- **Where**: line 36 — "Section 20.4"; line 39 — "Section 33.1"; line 46 — "Section 33.3"; line 97 — "Section 33.2 ... Section 20.3 ... Section 20.1 ... Section 20.4"; line 117 — "Section 20.6"; line 124 — "Section 20.2"; line 133 — "Sections 33.1-33.3".
- **TODO**: covered by `check_unlinked_section_references.py`. Counter +9.

---

## Iteration 12 (part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html)

### Issue: duplicated figure caption — caption stranded outside its container
- **Where**: line 83 inside `<div class="diagram-container">`: `<div class="diagram-caption"><strong>Figure 1.1.3</strong>: ...</div>`; then line 85 again — `<div class="diagram-caption"><strong>Figure 1.1.3</strong>: The four eras of NLP...</div>` — sitting outside the diagram-container.
- **What's wrong**: The Figure 1.1.3 caption appears twice in rendered HTML; same text, once inside and once outside the diagram container.
- **Generalized pattern**: Detect two `<div class="diagram-caption">` elements with the same content within close proximity. Regex: scan for repeated `<div class="diagram-caption"><strong>Figure (\d+\.\d+\.\d+)</strong>` referencing the same figure number within 200 chars.
- **Suggested fix**: Remove the orphan caption.
- **TODO**: validator `check_duplicate_figure_caption.py`; fix `fix_remove_orphan_diagram_caption.py` (de-dupe identical captions within same page).

### Issue: meta description trailing `?.`
- **Where**: line 7 — `<meta content="Section 1.1: Introduction to NLP &amp; the LLM Revolution. This entire book is a journey through one central question: How do we represent language in a form that machines can work with?." ...>`.
- **What's wrong**: Sentence ends with `?.` (question mark immediately followed by period). Reads as a typo and shows up in search engine snippets.
- **Generalized pattern**: For all `<meta ... content="...">`, detect punctuation pairs `[!?][.,;:]`, or `\.\.` (double period). Regex: `<meta[^>]*content="[^"]*[!?][.,;:]`.
- **Suggested fix**: Drop the trailing period after the question mark.
- **TODO**: validator `check_meta_description_punctuation.py`; fix `fix_meta_description_punctuation.py`.

### Issue: non-standard anchor class `cross-ref`
- **Where**: line 74 — `<a class="cross-ref" href="../module-00-ml-pytorch-foundations/index.html">Chapter 0</a>` while other cross-references elsewhere don't use this class.
- **What's wrong**: Inconsistent classing (similar to iter 9's `prereq-link`).
- **Generalized pattern**: Audit all anchor classes; flag those that appear on < 1% of pages.
- **Suggested fix**: Drop the class or apply it universally.
- **TODO**: validator `check_rare_anchor_classes.py`.

### Issue: prerequisites div without `callout` class (recurrence)
- **Where**: lines 33-36 — `<div class="prerequisites">`.
- **TODO**: covered by `check_prerequisites_uses_callout_class.py`. Counter +1.

### Issue: details body is multi-space-separated rather than a list
- **Where**: line 178 — `<p>1. Rule-based (hand-written grammar)   2. Statistical (n-gram language model)   3. LLM era (in-context learning)   4. Neural (Word2Vec)</p>` (note triple-space separators).
- **What's wrong**: Answers to a numbered quiz should be in an `<ol>` for accessibility (screen readers, EPUB readers) and visual layout. Multiple spaces inside `<p>` collapse to single spaces in HTML rendering.
- **Generalized pattern**: Inside `<details>` or quiz answer divs, detect `<p>` content of form `^\d\.\s+[^\d]+(\s{2,}\d\.\s+)+`. Regex: `>(\d)\.\s+\S[^<]*?\s{2,}\d\.\s`.
- **Suggested fix**: Replace with `<ol><li>...</li>...</ol>`.
- **TODO**: validator `check_inline_numbered_lists.py`; fix `fix_convert_inline_numbered_to_ol.py`.

### Issue: "Quick Check" formatted as a `warning` callout
- **Where**: line 167 — `<div class="callout warning"><div class="callout-title">Quick Check: Can You Match the Era?</div>`.
- **What's wrong**: A self-check / quiz is wrapped in `warning` callout class. The book uses `self-check` for this elsewhere. Visual styling for warning (red/orange) misrepresents this as an alert.
- **Generalized pattern**: Detect `<div class="callout warning">` whose `callout-title` contains "Quick Check", "Check", "Quiz", "Self-Check", "Try It", or whose body contains numbered questions plus a `<details>` with answers. Such callouts should use `self-check` class.
- **Suggested fix**: Change `warning` → `self-check`.
- **TODO**: validator `check_quiz_in_warning_callout.py`; fix `fix_quiz_callout_class.py`.

---

## Iteration 13 (part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.3.html)

### Issue: stale numbering on pseudocode callout
- **Where**: line 68 — `<div class="callout-title">Pseudocode 35.8.1: Automated red teaming pipeline</div>` inside section 47.2.
- **What's wrong**: Pseudocode is labeled `35.8.1` but chapter is 47. Same pattern as iter 1 stale prefix.
- **Generalized pattern**: For `<div class="callout-title">` starting with `Pseudocode N.M.K:` or `Algorithm N.M.K:`, assert the chapter prefix matches the file's chapter.
- **TODO**: extension of `check_table_caption_numbers.py` to include pseudocode/algorithm labels; or new validator `check_pseudocode_numbering.py`.

### Issue: duplicate code caption with second-form stale label
- **Where**: lines 161-163 — first `<div class="code-caption"><strong>Code Fragment 47.3.1:</strong>...` (correct), then immediately `<p class="caption"><strong>Code 32.8.1:</strong> Basic PyRIT red teaming setup...` — *both* describing the same code block.
- **What's wrong**: Two captions for one code block; the second uses a different label scheme ("Code" vs "Code Fragment") AND a stale chapter prefix (32 vs 47).
- **Generalized pattern**: After `<div class="code-caption">`, detect immediately following `<p class="caption">`. Regex: `<div class="code-caption">[^<]*<strong>Code Fragment [\d.]+:.*?</div>\s*<p class="caption"><strong>Code [\d.]+`.
- **Suggested fix**: Remove the orphan `<p class="caption">`.
- **TODO**: validator `check_duplicate_code_caption.py`; fix `fix_remove_orphan_code_caption.py`.

### Issue: library-shortcut output unrelated to the code it accompanies
- **Where**: lines 168-178 — Garak code block contains only commented-out CLI invocations (no executable Python), but the following `<div class="code-output">` reports `file_system_access_via_social_engineering: 1/20 (5.0%)` etc.
- **What's wrong**: The output is correct content for the Garak topic but does not match anything that the visible code would print. Output-without-code creates reader confusion.
- **Generalized pattern**: When a `<pre><code>` block is entirely comments (no executable line), but a sibling `<div class="code-output">` is present, flag.
- **Suggested fix**: Either turn the comments into a real invocation that would print the shown output, or inline the output in prose.
- **TODO**: validator `check_commented_only_code_with_output.py`.

### Issue: trailing space in `<strong>` (recurrence iter 3)
- **Where**: line 38 — `<strong>Red teaming </strong>`.
- **TODO**: counter +1.

### Issue: `prereq-link` class (recurrence iter 9)
- **Where**: line 42.
- **TODO**: counter +1.

---

## Iteration 14 (part-14-applications-of-llms-across-industries/module-72-government-llms/section-72.3.html)

### Issue: "What Comes Next" rendered as plain `<h2>` instead of canonical `whats-next` block
- **Where**: lines 59-60 — `<h2 id="what-comes-next">What Comes Next</h2><p><a href="section-72.4.html">Section 72.4</a> covers the public-sector-grounded-assistant architecture...`.
- **What's wrong**: Most other pages wrap "What Comes Next" in `<div class="whats-next"><h3>What Comes Next</h3>...</div>`. This page uses a top-level `<h2>` heading instead, which (a) elevates it into the page TOC and (b) bypasses the styled whats-next div.
- **Generalized pattern**: For each section page, detect `<h([23]) id="what-comes-next">What Comes Next</h\1>` that is not inside a `<div class="whats-next">`. Regex: `<h[23] id="what-comes-next">` outside `whats-next` container.
- **Suggested fix**: Wrap in canonical `<div class="whats-next">` + `<h3>`.
- **TODO**: validator `check_whats_next_canonical_structure.py`; fix `fix_whats_next_wrap.py`.

### Issue: section is text-only with no visual or structural callouts beyond Big Picture + one Key Insight
- **Where**: entire file. 1 Big Picture + 1 Key Insight + no figure/diagram/code-block/comparison-table/exercises/self-check.
- **What's wrong**: A regulatory survey page can legitimately be text-heavy, but the absence of even a comparison-table for the 8 frameworks (a natural fit) misses an opportunity for reader scanability. Also the page lacks the Further Reading bibliography that other survey-style pages carry.
- **Generalized pattern**: For each section page, count distinct callout/structure types (`big-picture`, `key-insight`, `practical-example`, `warning`, `fun-note`, `tip`, `key-takeaway`, `self-check`, `whats-next`, plus `figure`, `table`, `code-block-wrapper`, `comparison-table`, `details.bibliography-collapsible`). Flag pages with < 4 distinct types.
- **Suggested fix**: Add a comparison-table of the 8 frameworks (jurisdiction / scope / required artifacts / who enforces) and a Further Reading list of canonical legal docs.
- **TODO**: validator `check_structural_diversity.py`; (no automated fix; flag for author).

### Issue: H2 anchors use plain slugs without chapter-section prefix
- **Where**: lines 32, 43, 45, 47, 49, 51, 53, 59 — `<h2 id="the-eight-frameworks-that-apply">`, `<h2 id="omb-m-24-10-in-practice">`, etc.
- **What's wrong**: Other section pages number their H2s with the section prefix (e.g., `id="47-2-1-...">47.3.1 ...`), enabling deep linking by number and supporting the book-wide section/subsection grid. This page uses plain text slugs without the numeric prefix, breaking the convention.
- **Generalized pattern**: For each `<h2 id="...">N.M.K ...</h2>` in `section-N.M.html`, assert id starts with `N-M-K-`. Regex: `<h2 id="([^"]+)">(\d+\.\d+\.\d+) ` and assert id slug starts with `\2`'s dot-to-dash form.
- **Suggested fix**: Renumber H2s and update IDs.
- **TODO**: validator `check_h2_numeric_prefix.py`; fix `fix_h2_numeric_prefix.py` (use section number + sequential subsection counter).

---

## Iteration 15 (part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/section-77.4.html)

### Issue: Big Picture body verbatim-duplicates opening line of section prose
- **Where**: lines 39 (Big Picture: `"If the capability frontier is the headline, the labor market is the lede. The 2025-26 data is unusually clean..."`) and 41 (first body paragraph: `"If the capability frontier is the headline, the labor market is the lede. The 2025 data is unusually clean..."`).
- **What's wrong**: Big Picture and opening paragraph share the same hook sentence (and similar second sentence). Reader sees the same sentence twice on opening the page.
- **Generalized pattern**: For each page, compute longest common substring between `<div class="callout big-picture"><p>` and the first `<p>` of `<main>` after the big-picture div. Flag overlaps > 30 chars.
- **Suggested fix**: Rewrite either the Big Picture (more abstract framing) or the opening paragraph (concrete numbers, no rhetorical hook).
- **TODO**: validator `check_big_picture_duplicates_opening.py`; (no automated fix; flag for author).

### Issue: stale `<em>` prefix and double-close `</strong>` in comparison-table-title (recurrence iter 1)
- **Where**: line 51 — `<strong>Table 77.4.1</strong>:</strong> <em>64.4.1 Labor-market signals on AI impact, 2025-26.</em>`. Stale `64.4.1` prefix; chapter is 82.
- **TODO**: covered by previous validators. Counter +2.

### Issue: suspicious arXiv ID (potential hallucinated citation)
- **Where**: lines 41, 48, 57, 116 — `<a href="https://arxiv.org/html/2604.06906v1" ...>` for "AI Skills Shift" paper.
- **What's wrong**: arXiv ID `2604.06906` would be a paper submitted in 2026-04 (April 2026) with sequence number 06906. The validity depends on whether that paper exists; given the book's 2026 publishing horizon and the use of this ID at multiple places, it's worth flagging for verification. Pattern: arXiv IDs at the edge of the publication horizon are higher-risk for hallucination.
- **Generalized pattern**: Collect all `arxiv.org/abs/YYMM.NNNNN` and `arxiv.org/html/YYMM.NNNNN` links across the book; flag those whose YYMM is in the future relative to a configurable cutoff (e.g., today's date 2026-05). Also flag IDs that share prefixes with multiple distinct paper titles (collision check).
- **Suggested fix**: Verify the arXiv ID resolves, and if not, replace with the correct citation or remove.
- **TODO**: validator `check_arxiv_id_validity.py` (resolve HEAD against arxiv.org, flag 404s; flag future-dated YYMM).

---

## Iteration 16 (part-14-applications-of-llms-across-industries/module-68-finance-llms/section-68.2.html)

### Issue: H2 + callout pair duplicate each other's title verbatim
- **Where**: lines 32-34 (H2 "Hallucinated Numbers" + warning "Hallucinated Numbers"); lines 39-41 (Fair Lending and Disparate Impact); lines 46-48 (Market Manipulation Adjacency).
- **What's wrong**: Each H2 heading is immediately followed by a callout whose `callout-title` exactly matches the H2 text. Reader sees the same phrase twice (large H2, then small bold). This is structural duplication that should either be a single H2 + prose, or a single callout (without a preceding H2).
- **Generalized pattern**: Detect adjacent `<h([23])[^>]*>([^<]+)</h\1>\s*<div class="callout [^"]*"><div class="callout-title">\2</div>` — H2 text equals immediately-following callout-title text.
- **Suggested fix**: Drop the callout-title (let the section H2 carry the label) and keep the warning content as prose; or drop the H2 and let the callout stand alone.
- **TODO**: validator `check_h2_callout_title_duplication.py`; fix `fix_dedupe_h2_callout_title.py`.

### Issue: H2 anchor IDs use plain slugs (recurrence iter 14)
- **Where**: lines 32, 39, 46, 52, 54, 60.
- **TODO**: covered by `check_h2_numeric_prefix.py`. Counter +1.

### Issue: "What Comes Next" not wrapped in canonical `whats-next` div (recurrence iter 14)
- **Where**: lines 60-61.
- **TODO**: counter +1.

### Issue: non-standard callout class `postmortem`
- **Where**: line 56 — `<div class="callout postmortem">`.
- **What's wrong**: `postmortem` is not in the book's documented callout palette (`big-picture`, `key-insight`, `warning`, `tip`, `practical-example`, `fun-note`, `key-takeaway`, `self-check`, `note`, `library-shortcut`, `algorithm`, `pathway`, `research-frontier`, `exercise`). May lack CSS rules.
- **Generalized pattern**: Collect every `class="callout X"` value across the book; flag values that appear in fewer than 5 pages, suggesting an ad-hoc class that should be normalized.
- **Suggested fix**: Replace with `practical-example` or `case-study`, or add `postmortem` to the canonical palette with documented CSS.
- **TODO**: validator `check_callout_class_palette.py`; fix `fix_callout_class_normalize.py` (with a mapping table from rare → canonical).

---

## Iteration 17 (part-3-working-with-llms/index.html)

This page replicates the part-4-index issues confirmed in iter 8 (same template family). All issues are recurrences:

- title pipe spacing: `LLMs| Building` (counter +1, validator `check_title_pipe_spacing.py`)
- tab indentation in header-nav (counter +1, `check_header_nav_indentation.py`)
- alt-supplemental truncation: `archite...` (counter +1, `check_truncated_alt_supplemental.py`)
- Big Picture verbatim-duplicates meta description "Theory becomes practice here." (counter +1, `check_big_picture_vs_meta_description.py`)
- Big Picture / Part Overview / chapter-subtitle redundancy (counter +1, `check_part_index_section_redundancy.py`)
- missing `<nav class="chapter-nav">` for inter-part navigation (counter +1, `check_part_index_bottom_nav.py`)

Confirms that the part-index template has systematic drift across the book: every part-index page likely needs the same fixes. The fix scripts should target the part-index template specifically.

---

## Iteration 18 (part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.4.html)

### Issue: image filename has old `N.M.K` format AND wrong chapter
- **Where**: line 48 — `<img ... src="images/fig-38.3.1-latency-breakdown.svg"/>` inside section 40.4.
- **What's wrong**: (a) filename uses dots `38.3.1` rather than dashes `38-3-1` (book uses dashes elsewhere); (b) chapter prefix is `38` while file is in chapter 40.
- **Generalized pattern**: Extension of `check_figure_filename_chapter_prefix.py` to also enforce dash-separated numeric components: regex `images/fig(?:ure)?-?\d+(?:[\.-]\d+){1,2}-` should be all dashes.
- **Suggested fix**: Rename to `images/fig-40-4-1-latency-breakdown.svg` and update src.
- **TODO**: counter +1 (also: extension to validator to flag dot-separated numbering).

### Issue: mixed Figure/Table counter for same numbering sequence
- **Where**: line 49 Figure 40.4.1; line 80 Table 40.4.2; line 133 Figure 40.4.3. Same N.M.K pool used for figure and table.
- **What's wrong**: Convention in book (per iters 1, 5) is separate counters: Figure 40.4.1, Figure 40.4.2... and Table 40.4.1, Table 40.4.2... Here the figure and table counters interleave (Figure-Table-Figure share 1, 2, 3).
- **Generalized pattern**: For each page, partition `<strong>Figure N.M.K</strong>` and `<strong>Table N.M.K</strong>` references; flag pages where the same N.M.K number is used for both Figure and Table (collision) OR where one type's counter has gaps because the other type's counter consumed the numbers.
- **Suggested fix**: Re-number Tables on a separate counter.
- **TODO**: validator `check_figure_table_counter_collision.py`; fix `fix_split_figure_table_counters.py`.

### Issue: figure-containing-table again — Figure 40.4.3 labels a table
- **Where**: lines 119-134 — `<figure>` wraps `<table>` with `<figcaption><strong>Figure 40.4.3</strong>`.
- **TODO**: covered by `check_table_labeled_as_figure.py`. Counter +1.

### Issue: H2 inside `<div class="whats-next">` should be H3
- **Where**: line 174 — `<div class="whats-next"><h2 id="what-comes-next">What Comes Next</h2>...`. Other pages (iters 2, 7, 11) use `<h3>` here.
- **What's wrong**: Mixing H2 and H3 for the same semantic element creates an inconsistent TOC. The whats-next is a sub-section closing element, not a top-level heading.
- **Generalized pattern**: Inside `<div class="whats-next">`, assert the heading tag is `<h3>` not `<h2>`. Regex: `<div class="whats-next">\s*<h2`.
- **Suggested fix**: Replace `<h2>` with `<h3>` inside whats-next div.
- **TODO**: validator `check_whats_next_heading_level.py`; fix `fix_whats_next_heading_level.py`.

### Issue: breadcrumb / pagefind chapter missing title (recurrence)
- **Where**: line 35 — `Chapter 40` (no `: Voice and Realtime Multimodal Assistants`); line 38 — pagefind `chapter:Chapter 40` (no title).
- **TODO**: counter +1.

### Issue: double-close `</strong>` (recurrence)
- **Where**: line 116.
- **TODO**: counter +1.

---

## Iteration 19 (part-5-multimodal-llms/module-22-vision-language-models/section-22.8.html)

### Issue: divergence between breadcrumb chapter text and pagefind chapter meta
- **Where**: line 26 breadcrumb — `<a href="index.html">Chapter 22</a>` (no title); line 29 pagefind — `<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 22: Vision-Language and Omni Models" hidden="">` (with title).
- **What's wrong**: The same page declares different chapter strings for the visible breadcrumb vs the search index. Search hits will display "Chapter 22: Vision-Language and Omni Models" while clicking through shows breadcrumb "Chapter 22". The two must agree.
- **Generalized pattern**: Extract the chapter string from both `data-pagefind-meta="chapter:..."` and the last `<a>` of `page-breadcrumb`; flag when they differ.
- **Suggested fix**: Mirror the title in the breadcrumb.
- **TODO**: validator `check_breadcrumb_vs_pagefind_chapter_meta.py`; fix `fix_breadcrumb_to_match_pagefind.py`.

### Issue: image filename has wrong chapter prefix + dot-separated numbering
- **Where**: line 39 — `images/fig-37.3.1-any-to-any-architecture.svg` for Figure 22.8.1.
- **TODO**: covered by `check_figure_filename_chapter_prefix.py`. Counter +1.

### Issue: figure-containing-table (recurrence)
- **Where**: lines 89-104 — `Figure 22.8.2` labels a table.
- **TODO**: counter +1.

### Issue: H2 inside `whats-next` div (recurrence iter 18)
- **Where**: line 147.
- **TODO**: counter +1.

### Issue: double-close `</strong>` (recurrence)
- **Where**: line 78.
- **TODO**: counter +1.

---

## Iteration 20 (part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html)

### Issue: orphaned `tot-subsection` placed AFTER the page's chapter-nav and footer
- **Where**: lines 74-79 — first `<nav class="chapter-nav">` and `<footer>` close the page; lines 81-282 — a `<section class="tot-subsection" id="14-1-api-keys-and-secrets-management">` appended after the footer; lines 276-281 — a second `<nav class="chapter-nav">` and `<footer>` close the orphan section; line 284 — `</main>`.
- **What's wrong**: The page has TWO chapter-navs and TWO footers separated by an orphan `<section>`. Renders as: end-of-page, then a fresh "API Keys and Secrets Management" subsection, then another end-of-page. Looks like a "tools of the trade" appendix-section was concatenated after the original page's close. Probably from a merge that didn't remove the original closing block.
- **Generalized pattern**: For each section page, count `<nav class="chapter-nav">` and `<footer>` occurrences inside `<main>`; both should be exactly 1. Regex: count occurrences inside `<main>...</main>`.
- **Suggested fix**: Delete the first set of `<nav class="chapter-nav">` + `<footer>` (lines 74-79) so the orphan section becomes part of the normal flow; or move the orphan section before the chapter-nav and delete the duplicate nav/footer at the end.
- **TODO**: validator `check_duplicate_chapter_nav_and_footer.py`; fix `fix_dedupe_section_close_blocks.py` (collapse to single chapter-nav + footer at end of `<main>`).

### Issue: code-fragment labels use placeholder `h.7.N` instead of section numbering
- **Where**: lines 97, 120, 140, 177, 200, 220, 244 — captions like "Code Fragment h.7.1:", "Code Fragment h.7.2:", "Table h.7.1:". The `h` may be a leftover from an earlier draft using appendix-letter numbering or it's the literal Markdown heading char.
- **What's wrong**: Labels do not include the section number; readers cannot reference a specific fragment.
- **Generalized pattern**: For each `<div class="code-caption"><strong>Code Fragment ([^<]+?)</strong>`, assert the captured label matches `\d+\.\d+\.\d+`. Flag matches starting with `[a-z]\.` (appendix-letter pattern in main-chapter file) or non-digit prefix.
- **Suggested fix**: Renumber to `Code Fragment 14.1.N`.
- **TODO**: validator `check_code_caption_label_format.py`; fix `fix_renumber_code_captions.py` (re-derive prefix from file path).

### Issue: closing tag mismatch on H3 elements (open `<h3>` closed with `</h4>`)
- **Where**: line 89 — `<h3 id="1-the-env-file-and-python-dotenv">1. The .env File and python-dotenv</h4>` — opens `<h3>`, closes `</h4>`. Same at lines 127, 143, 161, 184.
- **What's wrong**: HTML well-formedness violation. Browsers will auto-correct but downstream tools (epub conversion, screen readers, validators) may misbehave.
- **Generalized pattern**: Detect mismatched opening/closing heading tags. Regex: `<h([1-6])(?:\s[^>]*)?>(?:[^<]|<(?!/h[1-6]))*?</h(?!\1)([1-6])>` (multiline). Or run HTML5 validator (`html5validator` package).
- **Suggested fix**: Replace `</h4>` with `</h3>`.
- **TODO**: validator `check_heading_open_close_match.py`; fix `fix_heading_close_mismatch.py`.

### Issue: stale anchor href in prev/next nav
- **Where**: line 277 — `<a class="prev" href="section-14.2.html#16-2-langchain-output-parsers-and-structured-output">` — section 14.2 file with anchor `#16-2-...` (chapter 16 prefix on a chapter-14 file); nav-num says "Section 14.7" (but href is to 14.2). Line 279 — `<a class="next" href="../../part-4-training-adaptation/module-15-synthetic-data/section-15.1.html">...Section 17.1...</a>` — text says "Section 17.1" but href is to section-15.1.
- **What's wrong**: Both the anchor inside href and the navigation label are stale from a previous numbering.
- **Generalized pattern**: For each `<a class="prev|next" href="...">...<span class="nav-num">Section X.Y</span>`, assert (a) href filename matches the X.Y in the span, (b) any `#anchor` in the href starts with `X-Y-` prefix.
- **Suggested fix**: Update nav-num to match href; update anchor to current numbering of target file.
- **TODO**: validator `check_chapter_nav_label_href_consistency.py`; fix `fix_chapter_nav_labels.py`.

### Issue: stale numeric prefix in `<em>` table-title (recurrence iter 1)
- **Where**: line 44 — `<strong>Table 14.1.1:</strong> <em>16.1.1 2026 LLM API platforms at a glance.</em>` — stale `16.1.1`.
- **TODO**: counter +1.

---

## Iteration 21 (part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html)

### Issue: meta description is for a different section entirely
- **Where**: line 7 — `<meta content="Section 49.10: Privacy Attacks &amp; Differential Privacy for LLMs. Federated learning (FL) enables multiple parties to collaboratively train or fine-tune a model without sharing their raw data." ...>`.
- **What's wrong**: Page title (line 8) is "Section 50.1: Privacy Attacks and Differential Privacy" but the meta description (a) says "Section 49.10" (wrong number) and (b) describes federated learning (wrong topic — this section is about privacy attacks and DP-SGD, not FL).
- **Generalized pattern**: For each section page, parse the section number from filename and from meta description; flag if they differ. Also compute keyword overlap between meta description and page H1/intro paragraph; flag low overlap.
- **Suggested fix**: Regenerate meta description from current section content.
- **TODO**: validator `check_meta_description_matches_section.py`; fix `fix_meta_description_regenerate.py` (regenerate from H1 + first paragraph).

### Issue: pagefind chapter meta has wrong type prefix and wrong number
- **Where**: line 40 — `<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Part XIV: Privacy and Data Protection" hidden="">`.
- **What's wrong**: Says "Part XIV" (this is Part X = 10) AND uses "Part" prefix where it should be "Chapter" (chapter 50). Two distinct bugs in one string.
- **Generalized pattern**: For `data-pagefind-meta="chapter:X"`, assert X starts with `Chapter `. Regex: `data-pagefind-meta="chapter:(?!Chapter )`.
- **Suggested fix**: Replace with `chapter:Chapter 50: Privacy and Data Protection`.
- **TODO**: validator `check_pagefind_chapter_meta_format.py`; fix `fix_pagefind_chapter_meta.py`.

### Issue: code-output mismatched with preceding code (recurrence iter 3)
- **Where**: lines 110-117 — code block shows `measure_memorization` perplexity function; output shows `sigma=0.8712 for (8.0, 1e-05)-DP over 3 epochs ... epsilon_spent=...` which is DP-SGD training output. Different code, different topic.
- **TODO**: counter +1.

### Issue: duplicate / wrong code caption (caption copied from previous code block)
- **Where**: line 163 — `<div class="code-caption"><strong>Code Fragment 50.1.2:</strong> Measuring memorization: perplexity-based extraction detection</div>` but the code is the `PrivacyConfig` + `privacy_aware_pipeline` block (lines 120-162).
- **What's wrong**: Caption text was copy-pasted from Code Fragment 50.1.1 (line 117) and never updated. Misrepresents the second snippet.
- **Generalized pattern**: For each code block on a page, extract identifiers / docstring from the code and compare to caption text. Flag low overlap.
- **Suggested fix**: Replace caption with description of `PrivacyConfig` + `privacy_aware_pipeline`.
- **TODO**: validator `check_code_caption_matches_code.py`.

### Issue: double-close `</strong>` (recurrence)
- **Where**: line 117.
- **TODO**: counter +1.

### Issue: indent-rot inside `PrivacyConfig` / `privacy_aware_pipeline` (recurrence iter 3)
- **Where**: lines 119-162.
- **TODO**: counter +1.

### Issue: prerequisites div without callout class (recurrence iter 3)
- **Where**: lines 49-52.
- **TODO**: counter +1.

---

## Iteration 22 (part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html)

### Issue: code-prefix placeholder comment "# implement <function_name>"
- **Where**: line 56 — `# implement ask_about_table`; line 162 — `# implement get_schema_context`; line 191 — `# implement text_to_sql`. Each Python code fragment begins with a one-line comment that reads like a code-generation task spec.
- **What's wrong**: These are leftover scaffolding comments from a code generation pipeline ("here, model, implement this function"). They serve no purpose for the reader and look like a coder's TODO.
- **Generalized pattern**: Detect Python comments matching `^\s*#\s*implement\s+[a-z_]+\s*$` at the start of `<pre><code class="lang-python">` blocks. Regex: `<pre><code class="pygments-highlighted lang-python"><span class="c1"># implement \w+`.
- **Suggested fix**: Replace with a one-sentence prose comment that describes what the function does.
- **TODO**: validator `check_implement_placeholder_comment.py`; fix `fix_strip_implement_placeholder_comment.py`.

### Issue: caption appends generic boilerplate sentence
- **Where**: line 186 — Code Fragment 32.4.2 caption ends with "The function encapsulates reusable logic that can be applied across different inputs. Tracing through each step builds the intuition needed when debugging or extending similar systems."
- **What's wrong**: Two sentences of pure boilerplate appended to a code caption. They describe code in general, not this specific code. Looks like an LLM template suffix.
- **Generalized pattern**: Detect `<div class="code-caption">` body containing one or more of these stock phrases: "encapsulates reusable logic", "Tracing through each step builds the intuition", "applied across different inputs", "for debugging or extending similar systems".
- **Suggested fix**: Trim to the topic sentence only.
- **TODO**: validator `check_code_caption_boilerplate.py`; fix `fix_trim_code_caption_boilerplate.py` (regex strip a maintained shortlist of stock sentences).

### Issue: double-close `</strong>` recurrences
- **Where**: lines 76, 186.
- **TODO**: counter +2.

### Issue: prerequisites div without callout class (recurrence)
- **Where**: lines 40-43.
- **TODO**: counter +1.

### Issue: code-indent-rot in `get_schema_context` (recurrence)
- **Where**: lines 167-185 — `return "\n\n".join(schema_parts)` indented deeper than the for-loop, so function returns after first iteration.
- **TODO**: counter +1.

---

## Iteration 23 (part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.6.html)

### Issue: dataclass fields not indented under the class (broken Python)
- **Where**: lines 75-90 — `<span class="nc">ProofState</span>` defined as `@dataclass class`, but then line 78 `<span class="n">goal</span>: ...` has no leading indentation (the docstring on line 77 has only single-space indent). The fields are at column 0, outside the class scope.
- **What's wrong**: Same indent-rot pattern as iter 3, here producing class-less attribute declarations that won't run.
- **TODO**: counter +1 of `check_python_code_indent_rot.py`.

### Issue: HTML entities inside code-block string literals (recurrence iter 6)
- **Where**: line 87 — `<span class="s2">"intro n; induction n with | zero =&gt; rfl | succ n ih =&gt; simp [Nat.add_succ, ih]"</span>` — `=&gt;` for `=>`.
- **What's wrong**: The Lean code inside a Python string literal contains `=>` rendered as HTML entity `=&gt;`. The Pygments rendering preserves it as an entity in the HTML output; if a reader copies the rendered code into a Python file, they get `=&gt;` literal characters, not `=>`.
- **TODO**: counter +1 of `check_html_entity_strings_in_code.py`.

### Issue: prerequisites div without callout class (recurrence)
- **Where**: lines 36-39.
- **TODO**: counter +1.

---

## Iteration 24 (part-3-working-with-llms/module-14-tools-of-the-trade/index.html)

### Issue: alt text split between `alt` attribute and figcaption at arbitrary char boundary
- **Where**: line 27 — `<img ... alt="Warm cartoon-style hero illustration introducing chapter 'Tools of the Trade: LL" aria-describedby="long-desc-18"/><figcaption id="long-desc-18">M API Stack', a Kurzgesagt-meets-XKCD visual metaphor ...`. Alt ends "LL" and figcaption begins "M API Stack'" — the title was split mid-word across the two strings.
- **What's wrong**: Auto-generated alt/figcaption pair was clipped without word-boundary respect. The alt ends in a quote-and-letter fragment; the figcaption begins with the missing letters. Reader and screen reader both get garbled text.
- **Generalized pattern**: For each `<img alt="..." aria-describedby="X">...<figcaption id="X">...</figcaption>`, concatenate alt + figcaption text; check whether the concatenation contains the apparent original string and whether the split occurs at a word boundary. Heuristic: alt does not end at sentence boundary AND figcaption starts mid-sentence (no leading capital after stripped whitespace).
- **Suggested fix**: Re-split at the closest punctuation; or set alt to a short description and put the full description in figcaption.
- **TODO**: validator `check_alt_figcaption_word_boundary.py`; fix `fix_realign_alt_figcaption.py`.

### Issue: alt-text and figcaption duplicate the meta description / subtitle
- **Where**: line 27 figcaption ends with "Consolidated reference: platforms, libraries, datasets, models, and external resources..." — same string as line 7 meta description and line 24 chapter-subtitle.
- **TODO**: counter +1 of `check_big_picture_vs_meta_description.py` (generalized cross-element redundancy).

### Issue: stale chapter reference in whats-next
- **Where**: line 63 — "Chapter 21 closes Part IV with its own Tools of the Trade chapter". Per iter 8 part-4 index, Part IV closes with Chapter 19 (Tools of the Trade: Training & Adaptation Stack). "Chapter 21" is wrong.
- **Generalized pattern**: Detect `Chapter N closes Part ...` claims; cross-reference against the part-index to verify the chapter exists in that part.
- **Suggested fix**: Replace with "Chapter 19".
- **TODO**: extension of `check_unlinked_section_references.py` with chapter-existence resolver.

### Issue: H2 inside whats-next (recurrence iter 18)
- **Where**: line 61-62.
- **TODO**: counter +1.

### Issue: breadcrumb omits chapter title (recurrence iter 6)
- **Where**: line 22 — `Chapter 14` (no title).
- **TODO**: counter +1.

---

## Iteration 25 (part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.5.html)

### Issue: breadcrumb + pagefind chapter meta omit chapter title (recurrence)
- **Where**: line 23 breadcrumb `Chapter 41`; line 27 pagefind `chapter:Chapter 41`. Both omit the chapter title.
- **What's wrong**: Same as iter 6. Notable: this is the second section in module-41 confirmed with the bug (after iter 6 confirmed section-41.2). All sections in this module are likely affected.
- **TODO**: counter +1.

Otherwise this page is structurally clean: well-formed callouts, no double-close strong tags, no indent-rot, no stale references. Useful baseline of what a "Tools of the Trade — External Reading" section looks like when correct.

---

## Iteration 26 (part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html)

### Issue: pagefind chapter meta span has malformed attribute
- **Where**: line 24 — `<span class="pagefind-meta-injected" f: LLM-as-Judge &amp; Automated Evaluation" hidden=""></span>` — the second span's attribute is `f:` (garbage) instead of `data-pagefind-meta="chapter:Chapter 46:`. The opening `data-pagefind-meta="chapter:Chapter 46` text was clipped, leaving `f:` orphan.
- **What's wrong**: Broken HTML. The string-replace pass that injects pagefind meta deleted too much of the attribute name. Pagefind will fail to extract the chapter label for this page.
- **Generalized pattern**: For each page, verify that pagefind-meta spans have well-formed attribute syntax. Regex: `<span class="pagefind-meta-injected"\s+(?!data-pagefind-meta=")`.
- **Suggested fix**: Restore the full `data-pagefind-meta="chapter:Chapter 46: LLM-as-Judge &amp; Automated Evaluation"` attribute.
- **TODO**: validator `check_pagefind_meta_attribute_wellformed.py`; fix `fix_pagefind_meta_attribute.py`.

### Issue: page opens at H2 subsection 46.2.2 — no Big Picture, no 46.2.1
- **Where**: lines 25-28 — first content element is `<h2 id="46-2-2-g-eval-chain-of-thought-scoring">46.2.2 G-Eval: Chain-of-Thought Scoring</h2>`.
- **What's wrong**: Where is Section 46.2.1? There's no Big Picture, no epigraph, no introduction. Page jumps straight into subsection 46.2.2. Either content was deleted or the page renders only a fragment.
- **Generalized pattern**: For each `section-N.M.html`, assert the first `<h2 id="...">N-M-1-...">N.M.1 ...</h2>` exists. Flag pages where the first H2 numbering is `\d+-\d+-\d+-` with last component > 1.
- **Suggested fix**: Author Section 46.2.1 (or 46.2 intro) at top.
- **TODO**: validator `check_first_h2_numbering.py`; (no automated fix; flag for author).

### Issue: prose references Code Fragment X but caption labels it Y
- **Where**: line 28 prose: "Code Fragment 46.2.6 implements the G-Eval scoring pipeline"; line 90 caption: "Code Fragment 46.2.2: G-Eval chain-of-thought scoring...".
- **What's wrong**: Forward reference to a `Code Fragment 46.2.6` that doesn't exist on this page (only 46.2.2 visible). Prose mention is stale or caption is stale.
- **Generalized pattern**: For each `Code Fragment N.M.K` mentioned in prose, assert a matching `<div class="code-caption"><strong>Code Fragment N.M.K</strong>` exists on the page.
- **Suggested fix**: Align prose and caption.
- **TODO**: validator `check_code_fragment_cross_reference.py`.

### Issue: severe code-indent-rot — function body at column 0
- **Where**: lines 50-89 — `def geval_score(...)` opens, body lines 57-89 have no leading indent and most code is dedented out of the function. Then `return {...}` is deeply nested inside `if score_probs:` / `else:` chain at unrelated indent levels.
- **TODO**: counter +1 of `check_python_code_indent_rot.py`. This is the most severe indent-rot seen so far.

### Issue: chapter-nav and footer placed OUTSIDE `</main>`
- **Where**: line 113 — `</main>`; line 114 — `<nav class="chapter-nav">`; line 119 — `<footer>`. Both nav and footer are after the main close.
- **What's wrong**: Section template convention puts chapter-nav and footer INSIDE `<main class="content">`. Other pages (most prior iterations) follow this. This page closes main first, then puts both elements at the page level. May affect CSS layout.
- **Generalized pattern**: Detect `</main>\s*<nav class="chapter-nav">` and `</main>\s*<footer>` patterns.
- **Suggested fix**: Move `</main>` to after the footer.
- **TODO**: validator `check_main_chapter_nav_footer_order.py`; fix `fix_close_main_after_footer.py`.

### Issue: thin section structure (recurrence iter 10)
- **Where**: entire page. Missing epigraph, Big Picture, Prerequisites, intro paragraph, Key Takeaway, Self-Check, Further Reading. Only one code block, one library shortcut, one tip callout.
- **TODO**: counter +1 of `check_section_top_structure.py`.

---

## Iteration 27 (part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.1.html)

### Issue: pagefind `part:` meta contains the book title, not the part name
- **Where**: line 38 — `<span ... data-pagefind-meta="part:Building Conversational AI with LLMs and Agents" hidden="">`.
- **What's wrong**: `part:` should be `Part V: Multimodal LLMs` (the part heading). Here it's the book's overall title. Pagefind searches will mis-group this page under the book title rather than its part.
- **Generalized pattern**: For `data-pagefind-meta="part:X"`, assert X starts with `Part [IVXLC]+`. Regex: `data-pagefind-meta="part:(?!Part [IVXLC]+)`.
- **Suggested fix**: Replace with correct part label.
- **TODO**: validator `check_pagefind_part_meta_format.py`; fix `fix_pagefind_part_meta.py` (derive from directory path).

### Issue: epigraph uses non-canonical markup
- **Where**: lines 39-42 — `<div class="epigraph"><blockquote>...</blockquote><cite>...</cite></div>` instead of canonical `<blockquote class="epigraph"><p>...</p>...<cite>...</cite></blockquote>` used by most pages.
- **What's wrong**: Two epigraph templates coexist in the book, leading to inconsistent CSS application.
- **Generalized pattern**: Detect `<div class="epigraph">` (the non-canonical form). The canonical form is `<blockquote class="epigraph">`.
- **Suggested fix**: Replace with canonical markup.
- **TODO**: validator `check_epigraph_markup_canonical.py`; fix `fix_epigraph_to_blockquote.py`.

### Issue: prose calls it "Figure" but caption labels it "Table"
- **Where**: line 60 prose — "<strong>Figure 21.1.1</strong> summarizes the four published TrOCR variants"; line 74 caption — `<figcaption><strong>Table 21.1.1</strong>: TrOCR model variants...`.
- **What's wrong**: Prose forward-reference says Figure; rendered caption is Table. Disagreement between prose and caption labels.
- **Generalized pattern**: For each `<strong>(Figure|Table) (\d+\.\d+\.\d+)</strong>` mentioned in prose, find the corresponding figcaption/caption on the page and assert the (Figure|Table) prefix matches.
- **Suggested fix**: Pick one — most likely the caption is correct (it's a table); update prose to "Table 21.1.1".
- **TODO**: validator `check_figure_table_prose_caption_agreement.py`.

### Issue: figure filename has wrong chapter prefix (recurrence iter 2)
- **Where**: line 127 — `images/figure-34-1-1.svg` in chapter 21.
- **TODO**: counter +1.

### Issue: double-close `</strong>:</strong>` in code-caption (recurrence)
- **Where**: line 116.
- **TODO**: counter +1.

---

## Iteration 28 (part-14-designing-llm-agent-products/index.html)

### Issue: Part Overview, Big Picture, and meta description are the SAME sentence
- **Where**: line 7 meta description body, line 26 Part Overview content, line 29 Big Picture content all equal: "From idea to MVP: the product owner's operating model for shipping AI-centered products."
- **What's wrong**: Three different places display the same sentence on page load. Reader sees the same hook three times within the first screen.
- **TODO**: counter +2 (one for `check_big_picture_vs_meta_description.py`, one for `check_part_index_section_redundancy.py`).

### Issue: part-index missing chapter-subtitle, epigraph, hero illustration
- **Where**: lines 14-22 — header has only `<h1>Part XIV: Designing LLM/Agent Products</h1>`; no chapter-subtitle, no epigraph, no chapter-opener figure. Part-3 and Part-4 indexes (iter 8, 17) have all three.
- **What's wrong**: Template drift: this part-index page is missing roughly half the structural elements of its siblings.
- **Generalized pattern**: Compare every `part-NN-*/index.html` against a reference template; flag missing elements (`p.chapter-subtitle`, `blockquote.epigraph`, `figure.chapter-opener`, `nav.chapter-nav`, etc.).
- **Suggested fix**: Add chapter-subtitle (drawn from H1 tagline), epigraph (carry from authored content), hero illustration.
- **TODO**: validator `check_part_index_template_completeness.py`; (no automated fix; flag for author).

### Issue: title pipe spacing (recurrence iter 8)
- **Where**: line 8 — `Products| Building`.
- **TODO**: counter +1.

### Issue: tab indentation in header-nav (recurrence iter 4)
- **Where**: lines 17-18.
- **TODO**: counter +1.

### Issue: breadcrumb uses truncated book title
- **Where**: line 20 — `<a href="../index.html">Building Conversational AI</a>` instead of `Building Conversational AI with LLMs and Agents` (the full title shown elsewhere).
- **What's wrong**: Breadcrumb book-title differs from the canonical `book-title-link` text on the same page.
- **Generalized pattern**: For each part-index `page-breadcrumb`, assert the first anchor text equals the `book-title-link` text on the same page.
- **Suggested fix**: Normalize to full book title (or to a documented short form, but be consistent across all pages).
- **TODO**: validator `check_breadcrumb_book_title_consistency.py`; fix `fix_breadcrumb_book_title.py`.

### Issue: missing bottom-nav for inter-part navigation (recurrence iter 8)
- **Where**: line 101 — `</main>` directly followed by `<footer>` (line 102). No `<nav class="chapter-nav">` linking to Part XIII or Part XIV.
- **TODO**: counter +1.

---

## Iteration 29 (part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html)

### Issue: meta description section number mismatches title
- **Where**: line 7 — `<meta content="Section 28.5: Testing Multi-Agent Systems. ..."` vs line 8 `<title>Section 28.4: Testing Multi-Agent Systems</title>`. Number drift.
- **TODO**: counter +1 of `check_meta_description_matches_section.py`.

### Issue: prose "Chapter 34" but link target is Chapter 42
- **Where**: line 38 — `<a href="../../part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html">evaluation frameworks</a> from Chapter 34`.
- **What's wrong**: Anchor text is generic ("evaluation frameworks") but the prose after it says "from Chapter 34". The link target is in Chapter 42. So the visible text references Chapter 34 while the link points to Chapter 42.
- **Generalized pattern**: For each `<a href="...">...</a> from Chapter (\d+)` in prose, assert the href's chapter prefix matches the captured number.
- **Suggested fix**: Either update prose "Chapter 34" → "Chapter 42" or change the link to a Chapter 34 target.
- **TODO**: validator `check_chapter_label_vs_link_target.py`.

### Issue: caption describes classes that don't exist in the code
- **Where**: line 90 — caption for Code Fragment 28.4.1 says "...explicit contracts between a PlannerOutput (with steps list and confidence float) and an ExecutorInput". But the code (lines 62-89) defines `ResearchOutput` and `WritingInput` instead.
- **What's wrong**: Caption text references different class names than the code. Either the caption was carried over from a different example, or the code was renamed and the caption never updated.
- **Generalized pattern**: covered by `check_code_caption_matches_code.py` (iter 21 validator).
- **TODO**: counter +1.

### Issue: severe indent-rot in `ResearchOutput`/`WritingInput`/`ChaosInjector` (recurrence)
- **Where**: lines 62-89 (one class defined inside another), lines 102-144 (function defined inside class method body).
- **TODO**: counter +2.

### Issue: trailing space in `<strong>` (recurrence)
- **Where**: line 38 — `<strong>Testing multi-agent systems </strong>`.
- **TODO**: counter +1.

### Issue: prerequisites div without callout class (recurrence)
- **Where**: lines 40-43.
- **TODO**: counter +1.

---

## Iteration 30 (part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.2.html)

### Issue: pagefind chapter meta attribute truncated (recurrence iter 26)
- **Where**: line 31 — `<span class="pagefind-meta-injected" b: LLM Evaluation &amp; Quality Metrics" hidden="">` — leading `data-pagefind-meta="chapter:Chapter 42` clipped, leaving stray `b:` (also matching `f:` from iter 26).
- **What's wrong**: Same widespread attribute clipping. The character-pattern (`f:`, `b:`) suggests the substitution regex chopped off everything up to and including the LAST `f` or `b` in the original `chapter:Chapter 42:LLM` etc. (chap → ter clip → b).
- **TODO**: counter +1 of `check_pagefind_meta_attribute_wellformed.py`.

### Issue: pseudocode numbering uses stale chapter prefix
- **Where**: line 89 prose — "Pseudocode 27.2.1 below"; line 91 callout — `Pseudocode 27.2.1: Bootstrap confidence interval...` — section is 42.2 but pseudocode prefix is 27. Recurrence of iter 13.
- **TODO**: counter +1 of `check_pseudocode_numbering.py`.

### Issue: pseudocode block marked as `lang-python` but content is pseudocode
- **Where**: lines 93-102 — pseudocode (containing `Input:`, `Output:`, mathematical notation `θ̂`, `α`) inside `<pre><code class="pygments-highlighted lang-python">`. Should be `lang-text` or a dedicated pseudocode class.
- **What's wrong**: Lexer mismatch results in Pygments incorrectly tokenizing pseudocode as Python (e.g., `Input:` becomes a name + colon punctuation).
- **Generalized pattern**: For `<div class="callout algorithm">` callouts containing a `<pre><code>`, assert the code class is `lang-text` (or `lang-pseudo`).
- **Suggested fix**: Change `lang-python` → `lang-text`.
- **TODO**: validator `check_pseudocode_lang_attr.py`; fix `fix_pseudocode_lang_attr.py`.

### Issue: `# implement bootstrap_ci` placeholder comment (recurrence iter 22)
- **Where**: line 105.
- **TODO**: counter +1.

### Issue: prerequisites div without callout class (recurrence)
- **Where**: lines 39-42.
- **TODO**: counter +1.

---

## Iteration 31 (part-5-multimodal-llms/module-20-audio-music-generation/section-20.3.html)

All issues observed are recurrences:

- Double-close `</strong>:</strong>` in code-caption at line 78 (counter +1)
- Figure-containing-table at lines 86-102 with `Figure 20.3.1` labeling a table (counter +1)
- Figure filename with wrong chapter prefix: `images/figure-32-3-2.svg` at line 116 (counter +1)
- Bare ambiguous "Section 3" cross-references at lines 80 and 131 (counter +2 of `check_ambiguous_section_reference.py`)

Page is otherwise well-structured: good Big Picture, multiple genre-relevant callouts, comparison-table-as-figure (a recurrence of an established bug pattern, not a novel one), Self-Check, What Comes Next, bibliography.

---

## Iteration 32 (part-2-understanding-llms/module-09-inference-optimization/section-9.4.html)

### Issue: prerequisites prose references wrong chapter ("Chapter 11" instead of "Chapter 9")
- **Where**: line 47 — `<a href="index.html">Chapter 11: Inference Optimization &amp; Efficient Serving</a>` inside section 9.4.
- **What's wrong**: Anchor text says "Chapter 11" but href is `index.html` of module-09 (chapter 9). Stale link text from earlier renumbering.
- **TODO**: counter +1 of `check_chapter_label_vs_link_target.py`.

### Issue: image filename includes half-word truncated title
- **Where**: line 88 — `images/fig-9.4.2-the-layers-of-an-llm-serving-stack-from-http-clients-down-t.png`. Filename truncated at `down-t.png` (missing `o-gpu-hardware`).
- **What's wrong**: Long auto-generated filenames clipped mid-word. Also alt text truncated as "...HTTP clients down to G..." with ellipsis.
- **Generalized pattern**: For each `<img src="images/[^"]*">`, flag filenames over 80 chars OR ending in a partial-word pattern (`[a-z]-[a-z]{1,3}\.(png|svg|jpg)` where the trailing letters look mid-word).
- **Suggested fix**: Rename to shorter slug and update src; pair with alt text that ends in a complete word.
- **TODO**: validator `check_long_truncated_image_filenames.py`; fix `fix_shorten_image_filenames.py`.

### Issue: code-fragment numbering jumps (9.6.5 as first fragment in section 9.4)
- **Where**: line 169 — `<strong>Code Fragment 9.6.5</strong>:</strong>` — first code block in section 9.4 should be 9.5.1.
- **What's wrong**: Numbering jumps to 9.6.5 with no 9.5.1-9.4.6 preceding. Suggests fragments from elsewhere were referenced/renumbered.
- **TODO**: counter +1 of `check_caption_numbering_sequence.py`.

### Issue: non-canonical `cross-ref` callout class
- **Where**: line 53 — `<div class="callout cross-ref">`.
- **What's wrong**: `cross-ref` is not in the canonical callout palette. Plus the referenced "Appendix K: Inference Serving" target is `module-10-interpretability/section-10.6.html#12-2-vllm-deep-dive` which is not an appendix at all — it's section 10.6 with a stale `#12-2-` anchor.
- **TODO**: counter +1 of `check_callout_class_palette.py`; also stale anchor in href (extension of `check_chapter_nav_label_href_consistency.py`).

### Issue: prerequisites div without callout class (recurrence)
- **Where**: lines 45-48.
- **TODO**: counter +1.

### Issue: indent-rot in `send_request`/`benchmark` (recurrence)
- **Where**: lines 133-160.
- **TODO**: counter +1.

### Issue: double-close `</strong>:</strong>` (recurrence)
- **Where**: line 169.
- **TODO**: counter +1.

---

## Iteration 33 (part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.1.html)

### Issue: visible "to commission for final styling" placeholder in published diagram caption
- **Where**: line 110 — `<div class="diagram-caption"><strong>Figure 43.1.1:</strong> The three-layer RAG evaluation cake. Each layer answers a different diagnostic question and points to a different repair. <em>(Diagram to commission for final styling.)</em></div>`.
- **What's wrong**: Author-facing TODO note ("to commission for final styling") shipped in the rendered HTML. Reader sees an internal task marker.
- **Generalized pattern**: For each `<figcaption>` or `<div class="diagram-caption">`, detect text inside `<em>(...)</em>` containing words/phrases from a maintained list: "to commission", "TODO", "placeholder", "for final styling", "fix me", "todo:", "tbd", "draft".
- **Suggested fix**: Remove the parenthetical TODO.
- **TODO**: validator `check_visible_todo_markers.py`; fix `fix_strip_visible_todo_markers.py`.

### Issue: pagefind chapter meta malformed (recurrence iter 26)
- **Where**: line 40 — `<span ... c: Specialized Evaluation: RAG, Agents, Multimodal, Long-Context" hidden="">`. `c:` stray.
- **TODO**: counter +1.

### Issue: stylistic "Layer N , Title" comma instead of em-dash
- **Where**: SVG text lines 97, 101, 105 — `Layer 1 , Retrieval`.
- **What's wrong**: A comma+space where an em-dash or colon is the natural separator. Possibly an em-dash strip pass replaced `—` with `,` to comply with the book's no-em-dash rule, but `,` reads awkwardly.
- **Generalized pattern**: Detect ` , ` (space-comma-space) inside SVG `<text>` and HTML headings/labels — likely em-dash artifacts. Regex: `\s,\s` in `<text>` content or `<h[1-6]>` content.
- **Suggested fix**: Replace ` , ` with `: ` (colon) or `. ` (period) for these label patterns.
- **TODO**: validator `check_em_dash_comma_artifact.py`; fix `fix_em_dash_comma_artifact.py` (targeted at SVG text and headings, not body prose).

### Issue: prerequisites div without callout class (recurrence)
- **Where**: lines 48-51.
- **TODO**: counter +1.

---

## Iteration 34 (part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.7.html)

### Issue: chapter title mismatch — breadcrumb/pagefind say Chapter 74, but file is in module-78
- **Where**: line 23 breadcrumb — `Chapter 74: LLMs in Creative Industries`; line 27 pagefind meta — `chapter:Chapter 74: LLMs in Creative Industries`; line 91 chapter-nav up — `Chapter 73` (correct); file at `module-73-manufacturing-llms/section-73.7.html`.
- **What's wrong**: Three different chapter identities on the same page: file path says 78 (manufacturing), breadcrumb and pagefind say 79 (creative), chapter-nav says 78 (no title). Section 73.7 content is creative-industries topic but is in the manufacturing module. Either the section is misfiled OR the breadcrumb/pagefind have wrong chapter number.
- **TODO**: counter +1 of `check_breadcrumb_chapter_number.py`. Also flag the broader content-vs-location mismatch (this is a content-organization bug, not just a label bug).

### Issue: non-canonical callout class `production-pattern`
- **Where**: line 42 — `<div class="callout production-pattern">`.
- **TODO**: counter +1 of `check_callout_class_palette.py`.

### Issue: anchor text mismatches link target (Section 32.6 → Chapter 33)
- **Where**: line 61 — `<a href="../../part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/index.html">Section 32.6</a>` — text says Section 32.6, href is `module-33/index.html`.
- **What's wrong**: Anchor text and link target disagree (recurrence iter 32 chapter-label-vs-link-target).
- **TODO**: counter +1.

---

## Iteration 35 (part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3.html)

### Issue: massive orphan-section pileup (5 chapter-navs + 5 footers in one file)
- **Where**: lines 107-112 (first nav+footer); then 4 more `<section class="tot-subsection">` blocks, each with its own chapter-nav + footer at lines 179-184, 717-722, 983-988, 1298-1303. File is 1308 lines / 152KB.
- **What's wrong**: This is iter 20's pattern but worse: the page concatenates 5 separate self-contained "tot-subsection" blocks (DVC, PySpark, Delta Lake, Feature Stores, plus the dataset survey), each ending with its own chapter-nav and footer copy. Result: rendered page has 5 sets of prev/next navigation interspersed with subsections. Reader navigation completely broken.
- **TODO**: counter +1 of `check_duplicate_chapter_nav_and_footer.py`. This is the most extreme observation of the pattern (5 occurrences); validator should report per-page count and treat anything > 1 as a hard error.

### Issue: code-fragment label uses `I.2.1` placeholder (appendix letter pattern, recurrence iter 20)
- **Where**: line 116 — "Code Fragment I.2.1 below puts this into practice." (line 117 is the pre-code block).
- **TODO**: counter +1 of `check_code_caption_label_format.py`.

### Issue: stale `<em>` prefix in comparison-table caption (recurrence iter 1)
- **Where**: line 57 — `<strong>Table 19.3.1:</strong> <em>21.3.1 Training datasets for Part IV.</em>` — stale `21.3.1`.
- **TODO**: counter +1.

### Issue: meta description body is unrelated content
- **Where**: line 7 — meta description begins "Delta Lake is an open-source storage layer that brings ACID transactions..." but the page's H1 is "Datasets & Benchmarks" and the primary content surveys instruction-tuning, preference, and pretraining datasets. The Delta Lake content is in a tot-subsection further down (line 726). The meta description was generated from one of the tot-subsection bodies rather than the section's main content.
- **TODO**: counter +1 of `check_meta_description_matches_section.py`.

### Issue: corrupt UTF-8 char in repeated footer ("·" rendered as "�")
- **Where**: line 112, 184, 722, 988, 1303 — `Sixteenth Edition, 2026 � <a href...` — the bullet/middot character (`·`) renders as `�` (replacement char), suggesting encoding mismatch when the footer was copied across blocks.
- **What's wrong**: Several pages already use `·` (U+00B7) correctly; here the duplicated footers got their byte-level encoding mangled.
- **Generalized pattern**: For each page, detect `U+FFFD` (replacement character) in HTML body. Regex: detect `�` in file contents.
- **Suggested fix**: Re-encode file as UTF-8 with consistent bullet character.
- **TODO**: validator `check_replacement_character_in_html.py`; fix `fix_normalize_bullet_encoding.py`.

---

## Iteration 36 (part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html)

All issues observed are recurrences:

- pagefind chapter meta `b:` truncation at line 40 (counter +1 of `check_pagefind_meta_attribute_wellformed.py`)
- trailing space in `<strong>` at line 47 (counter +1)
- indent-rot at lines 107-141 inside `run_niah_test` (counter +1)

Page is otherwise well-structured with Big Picture, prerequisites (still missing callout class — counter +1), Self-Check expected later, code fragments, library shortcut.

---

## Iteration 37 (part-6-agentic-ai/module-29-specialized-agents/section-29.4.html)

### Issue: Markdown content highlighted as Python (lexer mismatch)
- **Where**: lines 60-89 — `<pre><code class="pygments-highlighted lang-python">` whose content is a CLAUDE.md Markdown file. Pygments mis-tokenizes prose lines like "This is a FastAPI application for managing customer support tickets." as Python (operators, identifiers, keywords like `is`, `for`, `in`).
- **What's wrong**: Wrong language attribute. The rendered HTML produces incorrect coloring and breaks Markdown structure.
- **Generalized pattern**: Detect `<pre><code class="pygments-highlighted lang-python">` whose first non-comment line begins with `## ` or `# ` followed by a real word AND is followed by prose lines (not import statements / def / class). Markdown content can be more cleanly detected by file-name heuristic: if the comment near the top says "CLAUDE.md", "README.md", etc., lang should be `markdown`.
- **Suggested fix**: Change `lang-python` → `lang-markdown` (or `lang-text`).
- **TODO**: validator `check_code_block_lang_mismatch.py`; fix `fix_code_block_lang_attr.py` (heuristics-based).

### Issue: image filename has wrong chapter prefix and dot-separated numbering (recurrence)
- **Where**: line 52 — `images/fig-24.7.1-coding-agent-generations.png` in chapter 29.
- **TODO**: counter +1 of `check_figure_filename_chapter_prefix.py`.

### Issue: `prereq-link` class (recurrence iter 9)
- **Where**: line 42.
- **TODO**: counter +1.

### Issue: alt/figcaption split at sentence boundary but mid-paragraph (recurrence iter 24)
- **Where**: line 52 — alt text ends with `Gen 2 (2023) chat-based Q and A.` and the `alt-supplemental` continues `Gen 3 (2024)...`. Split is at a sentence boundary (better than iter 24's mid-word) but the content is one coherent paragraph artificially split.
- **TODO**: counter +1 of `check_alt_figcaption_word_boundary.py` (extend to split-mid-paragraph case).

---

## Iteration 38 (part-14-designing-llm-agent-products/module-67-ideation/section-67.11.html)

### Issue: breadcrumb / pagefind chapter mismatch (recurrence iter 5 / iter 9)
- **Where**: line 26 — `Chapter 68: From Idea to Product Hypothesis`; line 30 — pagefind `chapter:Chapter 68: From Idea to Product Hypothesis`. File is in `module-67-ideation/section-67.11.html` so chapter should be 67. Confirmed by chapter-nav (not shown in slice; but the file path and section number 67.11 are decisive).
- **What's wrong**: Module 67 is consistently mis-labeled as Chapter 65, 64, or 68 across its sections (we've now seen iter 5 = "Chapter 65", iter 9 = "Chapter 64", iter 38 = "Chapter 68"). Chapter renumbering pass clearly hit module 67 with multiple stale values.
- **TODO**: counter +1 of `check_breadcrumb_chapter_number.py`. Note that module 67's sections may have *different* stale chapter numbers — a global pass needs to normalize all of them to 67.

### Issue: trailing space in `<strong>` (recurrence)
- **Where**: line 73.
- **TODO**: counter +1.

### Issue: `prereq-link` class (recurrence)
- **Where**: line 41.
- **TODO**: counter +1.

### Issue: `<table>` with `<caption>` not wrapped in `comparison-table` / `comparison-table-title`
- **Where**: lines 89-90 — `<table><caption><strong>Table 67.11.1</strong>: Error Tolerance by Domain</caption>...`.
- **What's wrong**: Book elsewhere uses `<div class="comparison-table"><div class="comparison-table-title"><strong>Table N.M.K</strong>: ...</div><table class="complex-table">...</table></div>`. This page uses `<table><caption>` directly. Two table-styling conventions coexist.
- **Generalized pattern**: Detect `<table>` elements not wrapped in `<div class="comparison-table">`. Decide on a single convention.
- **Suggested fix**: Normalize to `comparison-table` wrapper.
- **TODO**: validator `check_table_wrapper_canonical.py`; fix `fix_table_wrapper_normalize.py`.

---

## Iteration 39 (part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.2.html)

### Issue: prose anchor text dropped a word, producing nonsense ("multi-Section 26.1")
- **Where**: line 42 — `multi-<a class="prereq-link" href="../../part-6-agentic-ai/module-26-ai-agents/section-26.1.html">Section 26.1</a> (...Chapter 28)`. Should read "multi-agent" — the auto-linker swallowed "agent" and replaced it with the section anchor.
- **What's wrong**: Auto-link injection ate a content word. Reader sees "multi-Section 26.1" which is meaningless.
- **Generalized pattern**: For each anchor matching `<a [^>]*>Section \d+\.\d+</a>`, check the immediately preceding text for a trailing hyphen or compound-word fragment (e.g., `multi-`, `cross-`, `single-`, `inter-`). Such patterns likely indicate the link replaced a content word.
- **Suggested fix**: Restore "agent" before the link, or restructure the sentence.
- **TODO**: validator `check_hyphen_swallowed_by_autolink.py`; fix `fix_restore_compound_word_before_link.py` (semi-automatic — requires content judgment).

### Issue: image filename uses `ch26-` prefix in chapter 49 (recurrence iter 2)
- **Where**: line 45 — `images/ch26-sandbox-fishbowl.png`.
- **TODO**: counter +1.

### Issue: alt-supplemental span nested inside figcaption (not a separate hidden sibling)
- **Where**: line 46 — `<figcaption><strong>Figure 49.2.1</strong>: ...glass barrier.<span class="alt-supplemental" hidden="">while the real production environment...</span></figcaption>`.
- **What's wrong**: Earlier pages (iter 8 `part-4/index.html`) place `<span class="alt-supplemental" hidden="" id="...">` as a sibling of `<img>` inside `<figure>` and reference it via `aria-describedby`. Here the supplemental is nested inside `<figcaption>` with no aria reference. Inconsistent supplemental-text markup.
- **TODO**: validator `check_alt_supplemental_markup_consistency.py`.

### Issue: trailing space in `<strong>` (recurrence)
- **Where**: line 38.
- **TODO**: counter +1.

---

## Iteration 40 (part-6-agentic-ai/module-30-tools-of-the-trade/section-30.6.html)

### Issue: redundant `<em>` numeric prefix in `comparison-table-title`
- **Where**: line 58 — `<strong>Table 30.6.1:</strong> <em>30.6.1 Where to go for what (Part VI).</em>`. The numeric prefix in `<em>` is correct (matches 30.6.1) but redundant with the preceding bold "Table 30.6.1".
- **What's wrong**: Even when the number is correct, repeating it inside the italic descriptor reads awkwardly. The convention should be either bold-only with number (Table 30.6.1: descriptor) OR italic-only without leading number.
- **Generalized pattern**: Same family as iter 1 (stale prefix) — extend to also flag *redundant* identical prefix.
- **Suggested fix**: Drop the numeric prefix from `<em>` whenever it matches the bold `Table N.M.K`.
- **TODO**: extension of `check_table_caption_numbers.py`; fix script can simply strip the leading `\d+\.\d+\.\d+ ` from `<em>` content.

Page is otherwise clean (no double-close strong, no indent-rot, no stale chapter references, well-structured prose + comparison-table + tip callout + bottom-nav crossing into Part VII).

---
