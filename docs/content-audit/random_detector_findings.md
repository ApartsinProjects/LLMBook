# Random Detector Findings — Round 1 (2026-05-17)

Random-sampling audit of 40 HTML pages drawn from the in-scope book tree (parts 1-16, appendices, capstone, front-matter). Seed = 20260517. The first 10 iterations took files of any size; iterations 11-40 filtered to files >=5KB.

The executive summary is regenerated after all 40 iterations and appears at the bottom of this file (search for "## EXECUTIVE SUMMARY").

---

## Iteration 1 (part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.3.html)

### Issue: caption number mismatch inside `comparison-table-title`
- **Where**: line 60 — `<strong>Table 83.3.1:</strong> <em>65.3.1 Frontier benchmarks (2026).</em>`
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
- **Where**: line 175 — first section of Chapter 20 (Part V) `prev` link points back to `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.5.html`.
- **What's wrong**: Cross-part backward nav can be intentional (linear reading), but the absence of any visual cue or "Previous Part" label can disorient readers. The label says "Previous · Section 19.5" with no part hint.
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
