# Templating Opportunities — Review

The book already has 3 page-level templates at `agents/book-skills/templates/`:
- `part-index-template.html`
- `chapter-index-template.html`
- `section-template.html`

Plus the CSS at `book-template.css`.

This doc lists OTHER blocks that benefit from templating (canonical structure
audited by plugins) so authors don't reinvent the markup each time.

## Block templates already canonical (enforced by plugins)

| Block | Canonical structure | Plugin enforcing |
|-------|---------------------|------------------|
| **Page header** | `<header class="chapter-header">` + nav + (search) + breadcrumb + h1 + (page-current) | `p2_header_template` |
| **Callout** (20 types) | `<div class="callout TYPE"><div class="callout-title">Prefix: Title</div>...</div>` | `p2_callout_canonical_structure`, `p2_callout_title_prefix`, `p2_callout_visual_consistency` |
| **Code fragment** | `<div class="code-block-wrapper"><pre><code class="pygments-highlighted lang-X">...</code></pre><div class="code-output">...</div><div class="code-caption">Code Fragment X.Y.Z: ...</div></div>` (wrapper optional) | `p2_code_fragment_structure`, `p2_code_no_language` |
| **Figure** | `<figure class="illustration"><img ...><figcaption><strong>Figure X.Y.Z</strong>: ...</figcaption></figure>` | (informal — img-dims, figure-sequence plugins) |
| **Bibliography** | `<details class="bibliography-collapsible"><summary><strong>Further Reading</strong></summary><section class="bibliography"><div class="bib-entry-card">...</div></section></details>` | `p1_structural_violations` (NON_CANONICAL_BIB) |
| **Self-check** | `<div class="callout self-check"><div class="callout-title">Self-Check</div><div class="quiz-question"><strong>Q1:</strong>...</div><details><summary>Show Answer</summary><div class="answer">...</div></details>...</div>` | `p1_self_check_canonical` |
| **Exercise** | `<div class="callout exercise"><div class="callout-title">Exercise N.M.K: ... <span class="exercise-type ...">type</span></div><p>...</p><details><summary>Answer Sketch</summary><p>...</p></details></div>` | (audit by structure heuristics) |
| **Lab** | `<div class="callout lab" id="lab-N-M"><div class="callout-title">Lab: ...</div><div class="lab-meta">duration + difficulty</div><div class="lab-objective"><h3>Objective</h3>...</div><div class="lab-skills"><h3>What You'll Practice</h3><ul>...</ul></div><div class="lab-prereqs">...</div><div class="lab-steps"><h3>Steps</h3><div class="lab-step">...</div>...</div><div class="lab-expected">...</div><div class="lab-stretch">...</div></div>` | (audit verifies sub-divs present) |
| **Real-World Scenario** | `<div class="callout practical-example"><div class="callout-title">Real-World Scenario: title</div><p><strong>Who:</strong> ...</p><p><strong>Situation:</strong> ...</p><p><strong>Problem:</strong> ...</p><p><strong>Dilemma:</strong> ...</p><p><strong>Decision:</strong> ...</p><p><strong>How:</strong> ...</p><p><strong>Result:</strong> ...</p><p><strong>Lesson:</strong> ...</p></div>` | (RWS template normalization wave) |
| **See Also** | `<div class="callout cross-ref"><div class="callout-title">See Also</div><p>For <topic>, see <a href="...">Section X.Y</a>. For ...</p></div>` | `p2_see_also_canonical` |
| **Library Shortcut** | `<div class="callout library-shortcut"><div class="callout-title">Library Shortcut: name</div><p>pip install ...</p><div class="code-block-wrapper">...</div></div>` | (informal) |
| **Comparison table** | `<div class="comparison-table"><table class="complex-table"><thead><tr><th scope="col">...</th></tr></thead><tbody>...</tbody></table></div>` | `p2_table_no_thead` |
| **Chapter-nav** | `<nav class="chapter-nav"><a class="prev" href="..."><span class="nav-label">Previous</span><span class="nav-num">Section X.Y</span><span class="nav-title">...</span></a><a class="up" ...></a><a class="next" ...></a></nav>` | `p2_nav_linear_chain` |

## Templating gaps to consider adding

| Block | Why it would help | Suggested plugin |
|-------|-------------------|------------------|
| **`<div class="prerequisites">`** wrapper | Currently inconsistent (some use h3, some don't; some have intro prose, some don't). Canonical form: `<div class="prerequisites"><h3 id="prerequisites">Prerequisites</h3><p>This section assumes ...</p></div>` | extend `p1_section_page_layout` |
| **`<div class="overview">`** on chapter index pages | Some chapters have it, some don't. Canonical form: `<div class="overview"><h2>Chapter Overview</h2><p>...</p></div>` | extend `p1_chapter_index_layout` |
| **`<div class="page-current">Section N.M</div>`** sub-label | Verified in p2_header_template; could add stricter format check (must match section number from filename) | extend `p2_header_template` |
| **`<aside class="section-internal-toc">`** | Used inconsistently (only some long sections have one). Canonical form: `<aside class="section-internal-toc"><h3 id="what-s-in-this-section">What's in this section</h3><ol><li>...</li></ol></aside>`. Could add audit: long sections (10+ h2) SHOULD have an internal TOC. | new `p2_internal_toc_for_long_sections` |
| **Module's `<div class="learning-objectives">`** | Some chapter indexes have it, others not. Canonical: `<div class="callout pathway">` was retired; now use `<div class="callout note">` titled "Note: Learning Objectives" or convert to direct content. | new `p2_learning_objectives` |
| **Footer text** | All footers say "Sixteenth Edition, 2026 · Contents". Currently a literal string everywhere; could be templated. | `p1_section_page_layout` already checks for footer |
| **Skip-link** | `<a class="skip-link" href="#main-content">Skip to main content</a>` — already book-wide standard. No new template needed. | n/a (handled by wave 41) |
| **Pagefind meta** | `<span class="pagefind-meta-injected" data-pagefind-meta="part:..." hidden>` should appear at start of `<main>`. Currently only checked informally. | extend `p2_header_template` |
| **PagefindUI init script** | Bottom of `</main>` should always have the canonical Pagefind init script (currently 4 page variants exist). | new `p3_pagefind_init_script` |

## Page-level templates (for new authoring)

The 3 templates at `agents/book-skills/templates/` are the master copies:
- Authors copying a new section should start from `section-template.html`
- New chapter index from `chapter-index-template.html`
- New part index from `part-index-template.html`

The templates need ONE refresh:
- `section-template.html`: should include the canonical `<div class="callout cross-ref"><div class="callout-title">See Also</div>...` placeholder (See Also pattern is new since the template was last updated)
- All 3 templates: ensure they use the toc-icon HTML entity `&#9776;` not the literal ☰

## Status
- 13 block templates already canonical and audited
- 9 templating opportunities identified for future enforcement
- 3 page templates in `agents/book-skills/templates/` need a minor refresh (See Also placeholder, toc-icon entity)
