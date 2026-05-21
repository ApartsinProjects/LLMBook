# Templating System Design for Safe Section/Chapter Restructures

**Book:** Building Conversational AI with LLMs and Agents, 15th Edition 2026
**Root:** `E:/Projects/BookBlogsHome/LLMBook/`
**Scale:** 529 HTML files across 12 parts, ~70 modules, ~280 sections, 20 appendices
**Date:** 2026-05-16

## 1. Problem statement

Every restructure round (the "zero_p1" series, `_fix_section_audits`, `_polish_toc_metadata`, `_rebuild_chapter_indexes`, the 8-step `_migration_step*` series) replays the same cleanup: chapter numbers, section numbers, slugs, and filenames embedded as plain text and href fragments throughout 529 HTML files. Drift between the structure source-of-record (`book_structure.yaml`) and the on-disk HTML accumulates faster than the manual fix scripts can absorb it.

The reference surface in a single section file (sampled from `section-4.1.html`, `section-18.1.html`, `section-4.7` history) covers at least:

1. `<title>Section N.M: Title</title>` and the description meta tag
2. `<h1>` plus `<div class="page-current">Section N.M</div>`
3. `<div class="page-breadcrumb"> <a href="../index.html">Part IV: ...</a> > <a href="index.html">Chapter 18: ...</a></div>`
4. `<span data-pagefind-meta="part:Part IV: ...">` and `chapter:Chapter 18: ...`
5. Inline prose hrefs to sibling sections (`<a href="section-18.2.html">Section 18.2</a>`) and across-part sections (`<a href="../../part-3-working-with-llms/module-14-prompt-engineering/section-14.1.html">`)
6. Prereq/cross-ref/looking-back callouts naming chapter and section numbers in prose ("from Chapter 14", "see Section 15.1")
7. Caption labels `Figure N.M.K`, `Code Fragment N.M.K`, `Table N.M.K`, `Listing N.M.K`
8. `<h2>N.M.K Title</h2>` and `<h3>N.M.K.L Title</h3>` (sub-section numbering inside a section file)
9. Prev/next nav at the bottom: `<a class="next" href="section-18.2.html">...Section 18.2... title</a>`
10. The parent chapter index's `section-card` (3-span: number, title, description)
11. The part index's `chapter-card` `section-list` mini-TOC
12. `toc.html`'s two-level entry
13. Cross-file forward references in unrelated sections that mention "see Section 18.7"

Plus filenames themselves: `section-N.M.html`, `module-MM-slug/`, `part-N-slug/`. When section 4.7 becomes 4.8 because a new 4.7 is inserted, every one of these touch-points drifts, plus the file gets `git mv`'d.

## 2. Investigation findings

### 2.1 What already exists

The repo already has the bones of a templating system. Use them, don't replace them:

- **`book_structure.yaml`** (1864 lines): a hand-edited but build-script-rebuildable structure source-of-record. Each section already has a `slug` field (`section-0.1`, `section-1.3`, ...). Today the slug is derived from the number (so it changes when the number changes). This is the seed for stable IDs.
- **`book_structure.target.yaml`**: an aspirational structure file used as the target by the `_migration_step*` scripts. This is exactly the "intent" file the new system needs.
- **`scripts/_build_book_structure.py`**: walks the file system and rebuilds `book_structure.yaml`. Today it round-trips: code on disk -> yaml. The new system needs the inverse: yaml -> rendered HTML pages.
- **`scripts/_rebuild_chapter_indexes.py`**: already regenerates every chapter `index.html`'s section-card list from on-disk section files. This is a working precedent for "regenerate one navigational artifact from a structural truth."
- **`scripts/_polish_toc_metadata.py`**: regenerates `toc.html` from `book_structure.yaml`. Another working precedent.
- **`scripts/_migration_step{1..8}*.py`**: an existing 8-step pipeline for executing a `target.yaml` -> on-disk migration. The new system can reuse the spirit (file renames via `git mv`, idempotent prose rewrites) but route everything through stable IDs instead of literal number strings.
- **`scripts/_audit_numbering_consistency.py`**, **`_audit_crossref_integrity.py`**, **`_audit_templating_opportunities.py`**: drift-detection scaffolding already in place. These can become the new system's CI guard.
- **`agents/drift-detector/scripts/book_utils.py`**: shared file-discovery, HTML parsing, section-number-extraction utilities. The new system extends rather than replaces this module.

### 2.2 What's missing

- No stable ID for sections, chapters, or parts that survives renumbering. The slug `section-0.1` is just the number with a prefix.
- No pre-build substitution layer. References are typed as final HTML and edited in lockstep.
- No render step from `book_structure.yaml` to the navigation chrome (header, breadcrumb, prev/next, page-current, title tag) in section files. `_rebuild_chapter_indexes.py` does it for chapter indexes only; section bodies still hand-edited.
- No structural diff between `book_structure.yaml` and on-disk files. `_build_book_structure.py` overwrites the yaml from disk, so divergence is hidden.

## 3. Recommended design (pick ONE)

Recommendation: **HTML-comment-marker placeholders resolved by a single render-pass Python script, anchored on a stable-ID system added to `book_structure.yaml`**. Rationale appears in section 7. The remainder of section 3 lays out the components.

### 3.1 Stable IDs (component A + B)

Add an `id` field to every part, chapter, section, and appendix in `book_structure.yaml`. The id is:

- a kebab-case slug
- assigned once, never reused, never renamed (even if the section title changes)
- topic-derived ("tokenization-bpe", "rope-positional-encoding") not number-derived
- globally unique across the whole book (not just within a chapter), so a single id resolves with no ambiguity

```yaml
parts:
- id: pt-foundations
  num: 1
  roman: I
  slug: foundations
  title: Foundations
  chapters:
  - id: ch-transformer-architecture
    num: 4
    slug: transformer-architecture
    title: The Transformer Architecture
    sections:
    - id: sec-transformer-one-token
      num: '4.1'
      slug: section-4.1
      title: How a Transformer Computes One Token
    - id: sec-transformer-from-scratch
      num: '4.2'
      slug: section-4.2
      title: Build a Transformer from Scratch
appendices:
- id: ap-huggingface
  letter: C
  slug: huggingface-ecosystem
  title: HuggingFace Ecosystem
```

Initial id assignment: a one-shot script seeds `id: sec-<chapter-slug>-<section-title-slug>` for each existing section based on the current title; the editor then renames any awkward ones once. After that, ids are immutable forever.

The yaml file remains the single source of truth. `num`, `roman`, `letter`, and `slug` are all computed views over the ordering of the yaml. The `id` is the pointer used by every cross-reference.

### 3.2 File layout decision (component D)

**Filenames stay number-based.** `section-4.7.html` remains the on-disk name and the URL.

Reason: shorter URLs, matches reader mental model when sharing links, and the current file count (529) is small enough that renaming files on each restructure remains cheap if it happens in one place. The render script does the `git mv` automatically when a section's `num` changes between two yaml versions.

The renderer also writes a `redirects.json` (or `.htaccess`-style redirect map, or per-page `<meta http-equiv="refresh">` stubs) so that old URLs from the published-on-disk version continue to resolve after a renumber. This is the trade for keeping number-based filenames.

If the user prefers stable filenames at the cost of uglier URLs, the alternative is `section-<id>.html` and only displayed numbers change. URL stability becomes free, but every external link to the published book has to be updated once. Recommend keeping number-based filenames because the book is already published with them and the redirect file is cheap to maintain.

### 3.3 Reference syntax in HTML source (component C)

Author writes references using a small set of HTML comment markers. The render script expands them in-place. The HTML on disk remains valid HTML at all times — comment markers don't break browsers if the render step is skipped — but the "expanded form" is the form that's checked into git as the publishing artifact.

Source markers:

```
<!--ref:sec-transformer-one-token-->
<!--ref:sec-transformer-one-token|title-->
<!--ref:sec-transformer-one-token|number-->
<!--ref:ch-transformer-architecture|number-->
<!--ref:ch-transformer-architecture|title-->
<!--ref:pt-foundations|roman-->
<!--ref:ap-huggingface|letter-->
<!--ref:sec-transformer-one-token|fullref-->   (resolves to: "Section 4.1: How a Transformer Computes One Token")
<!--ref:sec-transformer-one-token|shortref-->  (resolves to: "Section 4.1")
<!--ref:sec-transformer-one-token|link-->      (resolves to: '<a href="path/to/section-4.1.html">Section 4.1: Title</a>')
<!--ref:sec-transformer-one-token|link-short--> (resolves to: '<a href="path/to/section-4.1.html">Section 4.1</a>')
<!--href:sec-transformer-one-token-->          (resolves inside an existing <a href="...">)
```

`|` separates the id from the variant; default (no variant) is `shortref` for prose and `link` for inside an `<a>` whose href is the marker.

Why HTML comments specifically:

- Valid HTML; existing render pipeline (Pagefind, html2pub) sees them as comments and ignores them. Browsers ignore them. Search ignores them. Authors can hand-edit alongside.
- A `<!--ref:foo-->` is trivially regex-findable for the render script.
- Diff-friendly: a yaml change that renumbers section 4.7 -> 4.8 triggers a clean diff in every consumer file ("`Section 4.7`" -> "`Section 4.8`" near the same line).
- No invented HTML grammar, no JS dependency, no client-side fetch.

Compared to alternatives:

| Approach | Pro | Con |
|---|---|---|
| Custom elements `<x-secref id="..."/>` | Looks templated | Browser must parse unknown elements; complicates Pagefind; needs polyfill for older readers; harder to grep |
| Client-side JS fetching `book-structure.json` | Zero build step | Brittle (one fetch failure breaks every cross-ref); slower TTI; offline-readers break; KDP/EPUB pipeline can't follow JS |
| Markdown source compiled to HTML | Cleanest source | Massive rebuild cost; the book is in HTML; loses inline SVG and complex layout |
| Find-and-replace pipeline | Simple | Stateless: re-runs replace stale text, can't know "this 4.7 was a literal value, not a section number" |
| HTML comment markers (this proposal) | Lightweight, additive, regex-trivial | Source is slightly uglier than plain prose ("Section <!--ref:foo|shortref-->") |

The marker is only used at edit time and at restructure time. Once expanded, the file is plain HTML; the marker survives in the source through a paired `<!--/ref:foo-->` closer in cases where the expanded text is multi-token (so the render script can re-find and re-expand on the next pass without double-expanding). For the simple inline variants (number, letter, roman, shortref) a single comment is enough — the script regenerates the comment + its expanded text together every run.

Concrete pattern:

```html
<!-- Source form -->
<p>As shown in <!--ref:sec-tokenization-bpe|link-short--> and discussed in
   Chapter <!--ref:ch-transformer-architecture|number-->, ...</p>

<!-- Rendered form (what gets committed and shipped) -->
<p>As shown in <!--ref:sec-tokenization-bpe|link-short--><a href="../../part-1-foundations/module-02-tokenization-subword-models/section-2.2.html">Section 2.2</a><!--/ref--> and discussed in
   Chapter <!--ref:ch-transformer-architecture|number-->4<!--/ref-->, ...</p>
```

The render script:

1. Reads `book_structure.yaml`, builds an in-memory id -> resolution map: `{id, num, slug, title, file_path, full_url}`.
2. Walks every HTML file under scope.
3. For each `<!--ref:ID|VARIANT-->...<!--/ref-->` block, recomputes the expansion and replaces only the bracketed content. The yaml is the ground truth; the bracketed text is a cache.
4. For each `<!--ref:ID|VARIANT-->` without a closing comment, treats it as a fresh insertion and writes the expansion plus the closer.
5. Idempotent: re-running produces zero diff if yaml hasn't changed.

### 3.4 Non-prose surfaces (navigation chrome)

The navigation chrome (title tag, page-current, breadcrumb, prev/next, page-fag meta, h1 prefix) is regenerated wholesale from yaml. Each section file gets:

- A `<head>` regenerated from yaml.
- A `<header class="chapter-header">` regenerated from yaml (down to the closing `</header>`).
- A `<nav class="chapter-nav">` and `<footer>` at the bottom regenerated from yaml.

The body content between `</header>` and `<nav class="chapter-nav">` is **author territory**: the renderer never touches it except to expand `<!--ref:...-->` markers.

This means each section file's first ~30 lines and last ~10 lines are owned by the renderer; the middle is owned by the author. The boundary is enforced by two sentinel comments:

```html
</header>
<!--GENERATED-CHROME-END-->
<main class="content">
  ... author content with <!--ref:...--> markers ...
</main>
<!--GENERATED-CHROME-START-->
<nav class="chapter-nav"> ... </nav>
<footer> ... </footer>
```

The renderer overwrites everything from the start of the file up to `<!--GENERATED-CHROME-END-->` and everything from `<!--GENERATED-CHROME-START-->` to end-of-file. Authors who want to edit the chrome edit `book_structure.yaml` (for content) or `templates/section.html.j2` (for layout).

### 3.5 Index pages

The chapter `index.html`, part `index.html`, `appendices/index.html`, `toc.html`, and `front-matter/*/index.html` files are fully regenerated. Author writes nothing in them except a single sentinel comment block for the chapter description or "what's next" text where prose is needed, and these are stored back in the yaml so the renderer can re-emit them.

Effectively this collapses the work of `_polish_toc_metadata.py`, `_rebuild_chapter_indexes.py`, the part-index rebuild logic in `_migration_step3`, and all of the "fix the page-current text" fixes from `_zero_p1_round5.py` into one render script.

## 4. Architecture

### 4.1 Files at rest

```
book_structure.yaml                       # SOURCE OF TRUTH (canonical)
  parts[].id, .num, .slug, .roman, .title, .subtitle, .opener_image
  parts[].chapters[].id, .num, .slug, .title, .subtitle
  parts[].chapters[].sections[].id, .num, .slug, .title, .description
  appendices[].id, .letter, .slug, .title, .subtitle
  front_matter[].id, .slug, .title
  cross_refs:                             # OPTIONAL: long-form prose blocks
    looking-back-ch18:
      text: "You have data (...) cross-references when fine-tuning comes up."

templates/                                # SOURCE OF TRUTH (layout)
  section.html.j2                         # Jinja2 template for a section page
  chapter-index.html.j2
  part-index.html.j2
  toc.html.j2
  appendix-index.html.j2
  appendices-index.html.j2
  front-matter-index.html.j2

part-N-slug/module-MM-slug/section-N.M.html     # GENERATED but committed
  - head, chrome, nav, footer: regenerated wholesale
  - body content (between sentinels): author edits, with <!--ref:--> markers

redirects.json                            # GENERATED: legacy URLs -> new URLs
```

`templates/` already exists at the repo root (listed in `_audit_templating_opportunities.py`'s SKIP_DIRS). The new system populates it.

### 4.2 Render pipeline

Add **`scripts/render_book.py`**, the single entry point:

```
render_book.py [--check] [--apply] [--only PATTERN]
  Reads book_structure.yaml.
  Walks every HTML file under part-*/, appendices/, front-matter/, capstone/,
  plus toc.html and index.html.
  For each file:
    1. Determine its (id, role) from path. Role in {section, chapter-index,
       part-index, appendix-index, appendix-section, toc, front-matter,
       book-index}.
    2. Look up the yaml record by id. If missing, log "orphan file".
    3. Compute the expected chrome (head + header + nav-chrome + footer).
    4. Read the file; split at sentinel comments into [chrome-top, body, chrome-bottom].
    5. Render expected chrome from Jinja template + yaml record.
    6. Expand <!--ref:--> markers in body using yaml index.
    7. Write file = [new-chrome-top, body-with-refs-expanded, new-chrome-bottom].
    8. Rename file if yaml's num changed: git mv + add redirect.
  After all files, regenerate chapter-indexes, part-indexes, toc.html, appendices/index.html
  from yaml. Write redirects.json.
  --check: dry-run; exit 1 if any diff.
  --apply: write the diff.
```

The Jinja templates are filled in once and rarely change. They look roughly like:

```jinja2
{# templates/section.html.j2 #}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Section {{ sec.num }}: {{ sec.title }}. A comprehensive chapter from the {{ book.short_title }} textbook." name="description"/>
<title>Section {{ sec.num }}: {{ sec.title }}{% if include_book_title %} | {{ book.title }}{% endif %}</title>
{% include "_assets.html.j2" %}
</head>
<body>
<header class="chapter-header">
  {% include "_nav-header.html.j2" %}
  <div class="page-breadcrumb" data-pagefind-meta="chapter">
    <a href="{{ part.url_from(sec) }}">Part {{ part.roman }}: {{ part.title }}</a>
    <span class="bc-sep">›</span>
    <a href="{{ chapter.url_from(sec) }}">Chapter {{ chapter.num }}: {{ chapter.title }}</a>
  </div>
  <h1>{{ sec.title }}</h1><div class="page-current">Section {{ sec.num }}</div>
</header>
<!--GENERATED-CHROME-END-->
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="part:Part {{ part.roman }}: {{ part.title }}" hidden=""></span>
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {{ chapter.num }}: {{ chapter.title }}" hidden=""></span>
{{ body_content_with_refs_expanded }}
</main>
<!--GENERATED-CHROME-START-->
<nav class="chapter-nav">
  {% if prev %}<a class="prev" href="{{ prev.url_from(sec) }}"><span class="nav-label">Previous</span><span class="nav-num">{{ prev.label }}</span><span class="nav-title">{{ prev.title }}</span></a>{% endif %}
  <a class="up" href="{{ chapter.url_from(sec) }}"><span class="nav-label">In Chapter</span><span class="nav-num">Chapter {{ chapter.num }}</span><span class="nav-title">{{ chapter.title }}</span></a>
  {% if next %}<a class="next" href="{{ next.url_from(sec) }}"><span class="nav-label">Next</span><span class="nav-num">{{ next.label }}</span><span class="nav-title">{{ next.title }}</span></a>{% endif %}
</nav>
<footer><p>{{ book.edition }}, {{ book.year }} · <a href="{{ toc.url_from(sec) }}">Contents</a></p></footer>
</body>
</html>
```

### 4.3 Resolver function (drives `<!--ref:-->` expansion)

```python
def resolve(ref_id: str, variant: str, current_file: Path, yaml_index: dict) -> str:
    target = yaml_index.get(ref_id)
    if not target:
        raise BrokenRefError(f"unknown id {ref_id} in {current_file}")
    if variant == "number":
        return target.num            # "4.1" or "C" or "C.3"
    if variant == "letter":
        return target.letter         # "C" for appendix
    if variant == "roman":
        return target.roman          # "IV"
    if variant == "title":
        return target.title
    if variant == "shortref":
        return f"{target.kind_title} {target.num}"   # "Section 4.1"
    if variant == "fullref":
        return f"{target.kind_title} {target.num}: {target.title}"
    if variant == "link":
        href = relative_href(current_file, target.file_path)
        return f'<a href="{href}">{target.kind_title} {target.num}: {target.title}</a>'
    if variant == "link-short":
        href = relative_href(current_file, target.file_path)
        return f'<a href="{href}">{target.kind_title} {target.num}</a>'
    if variant == "href":
        return relative_href(current_file, target.file_path)
```

`kind_title` is "Part" | "Chapter" | "Section" | "Appendix" | "Appendix Section" depending on what the id resolves to.

Same resolver feeds the prev/next nav, breadcrumb, and chapter-index/part-index regeneration.

## 5. Migration plan

Five phases, each deliverable on its own without breaking the published book.

### Phase 1 — Seed stable IDs (1 day)

- Run a one-shot `scripts/_assign_ids.py` over `book_structure.yaml`. For each section, generate `id: sec-<chapter-slug>-<short-title-slug>` (collision-safe by appending a numeric suffix). For each chapter: `ch-<chapter-slug>`. Each part: `pt-<part-slug>`. Each appendix: `ap-<appendix-slug>`. Write back to yaml.
- Audit, hand-rename any awkward IDs. Commit the yaml.
- Add **`scripts/yaml_index.py`** providing `load_yaml_index()` -> dict[id] = record.
- No HTML changes yet.

**Verification:** `scripts/_audit_id_uniqueness.py` passes; `_build_book_structure.py` round-trips with the new id field preserved.

### Phase 2 — Build the renderer + templates (3-5 days)

- Create `templates/` directory with Jinja2 templates for section, chapter-index, part-index, appendix-index, appendices-index, toc, front-matter pages.
- Author the templates by extracting the exact chrome from a high-quality reference file in each role. Use `part-4-training-adapting/module-18-fine-tuning-fundamentals/index.html` as the chapter-index reference, `section-18.1.html` as the section reference, etc.
- Implement `scripts/render_book.py` with `--check` mode only at first.
- Run `render_book.py --check` against every HTML file. Diff against current. The diff will be enormous (every file has chrome). Triage: which diffs are "renderer wrong" vs "file drifted"? Fix the renderer until the diff for the canonical reference files is empty.

**Verification:** for the 5 reference files (one per part), `render_book.py --check` produces zero diff. The other files drift from the canonical template but that's expected; phase 3 handles them.

### Phase 3 — Insert sentinel comments and ref markers in NEW or TOUCHED files (continuous, ~2 weeks)

- Convention: every time the author edits a section file, they add the two sentinel comments (`<!--GENERATED-CHROME-END-->` and `<!--GENERATED-CHROME-START-->`) and convert hand-written cross-refs into `<!--ref:...-->` markers in the body.
- The renderer now runs in `--apply` mode for files that have the sentinels. Files without sentinels are skipped (so the renderer is opt-in per file).
- Add a pre-commit hook (`.git/hooks/pre-commit`) that runs `render_book.py --apply --only=<changed-files>` and re-stages.

**Verification:** `_audit_crossref_integrity.py` shows steady decrease in drift over time. Newly inserted sections are zero-drift by construction.

### Phase 4 — Bulk migration (1 week, scripted)

- Write **`scripts/_bulk_insert_sentinels.py`** that adds the two sentinel comments to every section, chapter-index, and part-index file. Uses BeautifulSoup to find `</header>` and `<nav class="chapter-nav">` and inserts the markers around them. Idempotent.
- Run it. Then run `render_book.py --apply` against everything. Expect drift cleanup of all chrome to converge to template.
- Write **`scripts/_bulk_convert_refs.py`** that scans each file's body for patterns like `<a href="(?:\.\./)+part-(\d+)-[^/]+/module-(\d+)-[^/]+/section-(\d+)\.(\d+)\.html">Section \d+\.\d+(?:: [^<]+)?</a>` and converts them to `<!--ref:sec-...|link--><...><!--/ref-->`. Resolves the id by looking up the yaml entry whose num matches. Idempotent.
- Run it. Run `render_book.py --apply` again to re-expand.

**Verification:** `_audit_crossref_integrity.py` clean. `_audit_numbering_consistency.py` clean. The diff between the existing files and a fresh `render_book.py --apply` from scratch is zero.

### Phase 5 — Decommission ad-hoc fix scripts (1-2 days)

- Once `render_book.py` is authoritative, move the `_zero_p1_round*.py`, `_fix_section_audits.py`, `_polish_toc_metadata.py`, `_rebuild_chapter_indexes.py`, `_fix_section_title_letter_drift.py`, `_fix_caption_drift_in_moved_sections.py`, and `_migration_step*.py` scripts into `scripts/archived/`. Add a README explaining what each one used to do and that the renderer subsumes it.
- Keep the `_audit_*.py` scripts; they become the renderer's regression suite.

**Verification:** restructure rounds 1-5 of the prior cleanup history can no longer recur, because every fix they performed is now derived from `book_structure.yaml`.

**Total effort estimate:** 3-4 weeks of one-developer-day-equivalent work, spread over wall-clock weeks. Phase 1 and 2 are the front-loaded effort; phases 3-5 are mostly mechanical.

## 6. Operations after migration

### 6.1 Insert a new section 4.7

```
1. Edit book_structure.yaml: add the new section entry between current 4.6 and 4.7.
   - id: sec-transformer-rope-positions
     num: '4.7'
     slug: section-4.7
     title: Rotary Position Embeddings
2. The downstream sections (current 4.7 onward) get num bumped: 4.7 -> 4.8, 4.8 -> 4.9.
3. Run: python scripts/render_book.py --apply
   - Creates new file: part-1-foundations/module-04-transformer-architecture/section-4.7.html
     (from template, with empty body).
   - git mv section-4.7.html -> section-4.8.html (and 4.8 -> 4.9 etc.)
   - Rewrites every <!--ref:sec-transformer-old-4-7-id--> across the book to render
     "Section 4.8" instead of "Section 4.7" (because the resolution changed).
   - Rebuilds chapter-index, part-index, toc.html.
   - Writes redirects.json: section-4.7.html -> section-4.8.html.
4. Author writes the body content of the new section-4.7.html. Uses <!--ref:...-->
   markers for any cross-references.
5. Run: python scripts/render_book.py --apply (again, to expand the markers).
6. Commit.
```

What used to take a "_zero_p1_round_N" cleanup pass is now two commands, both of which are deterministic and idempotent.

### 6.2 Move section 8.3 to part 9 as section 9.7

```
1. Edit book_structure.yaml: cut section sec-reasoning-test-time-compute from
   chapter 8's sections, paste into chapter ~46's sections at position 5.
2. Run: python scripts/render_book.py --apply
   - git mv part-2-understanding-llms/module-08-modern-llm-landscape/section-8.3.html
            part-9-safety-security-ethics/module-46-???/section-9.7.html  (path computed from yaml)
   - Rewrites breadcrumb, prev/next, page-current, title, chapter-pagefind-meta.
   - Every <!--ref:sec-reasoning-test-time-compute|...--> across the book re-renders
     as "Section 9.7" instead of "Section 8.3" with the new path.
   - Chapter 8's index regenerated without the orphan section.
   - Chapter 46's index regenerated with the new section.
   - Both part indexes regenerated.
   - toc.html regenerated.
   - Redirects.json: section-8.3.html -> section-9.7.html.
3. Commit.
```

### 6.3 Split chapter 12 into chapters 12 and 13

```
1. Edit book_structure.yaml: duplicate chapter 12's entry, split its sections list
   between the two. Add a new id for the split-off chapter. Renumber chapters 13
   onward to 14 onward.
2. Run: python scripts/render_book.py --apply
   - Creates new module-MM-slug directory (with index.html).
   - git mv-s sections from old to new module-dir.
   - Renames all downstream module-NN-* dirs.
   - All inter-chapter prose ("see Chapter 14") that used <!--ref:ch-...|number-->
     now resolves to 15. All hand-written "Chapter 14" prose that did NOT use the
     marker still shows 14 — these are flagged by _audit_numbering_consistency.
3. Commit.
```

### 6.4 The new fix-script idiom

The user's "small fix scripts" idiom doesn't go away. It becomes:

```
scripts/_yaml_edit_<task>.py    # 20-line script that mutates book_structure.yaml
                                # (insert/move/split/rename) then prints what to
                                # do next (run render_book.py).
```

The render step is the single fix-all. Small scripts only mutate yaml.

## 7. Why this design (versus alternatives)

| Alternative | Why not |
|---|---|
| **Switch to Hugo/Jekyll/Astro.** | Explicitly ruled out by user — too much rebuild cost. Also loses the SVG-heavy, inline-diagram aesthetic. |
| **JavaScript client-side resolution.** | Adds runtime risk (offline readers, search engines, EPUB/KDP), and book is already published on plain HTML. |
| **Markdown -> HTML build.** | Loses inline SVG, callout fidelity, KaTeX integration that's already wired in. Full rewrite. |
| **Just keep fix scripts.** | This is the status-quo. The user has shown the failure mode: every restructure costs hours. Even one round more justifies a few days of upfront work. |
| **Custom HTML elements `<x-secref>`.** | More invasive than comment markers; requires parser polyfill thinking; harder to grep; worse diff readability. |
| **Pre-existing build tools (e.g., Pandoc filters).** | Wrong granularity; would touch chrome too. The renderer needs the specific chrome regeneration the templates encode. |

The comment-marker + Jinja approach wins because:

1. It composes with existing scripts (`_build_book_structure.py`, `_rebuild_chapter_indexes.py`) rather than replacing them.
2. Source files remain valid HTML at every step. If the renderer breaks, the book still works.
3. The yaml + templates + renderer total is ~1500 lines of new code, smaller than the combined `_migration_step*.py` series.
4. It directly attacks the documented drift surface (chrome regeneration handles items 1-4 and 9 from problem-statement section 1; ref markers handle items 5-7; index regeneration handles items 10-13; renaming on yaml diff handles item 14).

## 8. Risks and tradeoffs

### 8.1 Risks

- **Bug in the renderer corrupts every HTML file at once.** Mitigations: (a) `--check` mode that diffs without writing; (b) renderer always writes through `git`, so a bad apply can be reverted with `git checkout`; (c) the `--only PATTERN` flag scopes the blast radius for testing; (d) the renderer never touches the body between sentinels.
- **Yaml merge conflicts on a multi-author branch.** Mitigation: yaml is structured top-down with one section per ~3 lines and stable id keys, so conflicts are local. Sections can be moved/inserted by id without touching neighbors' fields. A `--validate-yaml` precommit check catches malformed yaml early. Honestly: this is the most likely source of pain. Recommend a "structure changes go through a single editor" social rule for the first month.
- **Author forgets to use `<!--ref:-->` markers in new prose.** Mitigation: `_audit_numbering_consistency.py` catches phantom and drift references. Renderer optionally emits warnings for `Section N.M` text not wrapped in a marker.
- **Stable id collisions.** Mitigation: phase 1 audit script enforces uniqueness; renderer fails loudly on dup.
- **Render step breaks the dev loop.** Mitigation: `--only=<file>` to render just the file you're editing (sub-second). Optional file-watch mode.
- **Templates drift from the original artisan-edited chrome (loss of "personality").** Mitigation: extract the templates from the cleanest existing files; review the diff before phase 4. The chrome is largely uniform anyway (`_audit_templating_opportunities.py` was built specifically to find these duplications).

### 8.2 The "is this overengineering for 529 files?" sanity check

Honestly answered: **no, but it's marginal.** Five rounds of zero_p1 plus the 8-step migration plus four audit scripts plus `_fix_section_audits` is more code than the proposed renderer. The marginal cost-benefit clearly favors building it. The risk is sunk-cost overcommit if structure changes stop after this design lands, but the user's pattern (4 editions of restructure in the visible scripts, 8 migration steps, 5 zero_p1 rounds) suggests more restructures are coming, not fewer.

If the user genuinely expects structural stability going forward, phase 1 + phase 5 alone (just kill the fix scripts and rely on `_audit_numbering_consistency.py` to flag drift early) would be cheaper. But phase 1 alone is a 1-day investment with the option value of phase 2-4 unlocked any time.

### 8.3 What I'd cut if budget shrinks to one week

- Drop phase 3 (continuous ref-marker conversion). Phase 4's bulk-convert script covers it.
- Drop appendices from the first iteration (only 20 files; their letters change less often than chapter numbers).
- Drop `redirects.json`; use only sub-page anchors and let inbound external links break on the rare rename.
- Use Python f-strings or `string.Template` instead of Jinja2, saves one dependency.

The minimum viable version is: stable IDs + a `render_book.py --apply` that handles section chrome + ref-marker expansion + chapter-index regeneration. ~600 lines of Python. The rest is polish.

## 9. Recommendation

Build the system as described in section 3, in the phased order of section 5. Specifically:

1. **Adopt HTML comment markers (`<!--ref:id|variant-->`) as the reference syntax.**
2. **Build a single `scripts/render_book.py` driven by `book_structure.yaml` (with new stable `id` fields) and Jinja2 templates in `templates/`.**
3. **Keep filenames number-based, paired with a generated `redirects.json` to preserve already-published URLs.**
4. **Migrate in five phases, with phase 1 alone deliverable in one day.**

This is the cheapest design that closes the recurring drift loop: the chrome is generated, the cross-references are resolved at render time, the source-of-truth is one yaml, and the existing fix-script idiom evolves into "edit yaml, run renderer" — the same number of steps as today, but with deterministic and idempotent outcomes instead of round-after-round cleanup.
