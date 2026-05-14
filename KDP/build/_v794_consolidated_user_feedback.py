"""v794: Consolidated CSS fixes for user feedback received during
landscape-audit cycle.

Issues addressed (CSS-only; source HTML untouched):

1. DROP BIBLIOGRAPHY BADGES (BOOK / PAPER / BLOG POST)
   User: "drop badges (e.g., book)"
   Hide `.bib-meta` entirely. These are small uppercase pills below
   each bibliography entry that say "Book", "Paper", "Blog post",
   "Repo", etc. The category header above already groups them by
   type, making per-entry badges redundant and noisy.

2. STANDARDIZE CALLOUT-TITLE TYPOGRAPHY
   User: "some are all capital (like Learning Objectives), different
   sizes. Let's make header/title of each calloutbox standard"
   The book has several title-like elements that should all look
   identical (uppercase sans-serif, same size, same letter-spacing):
     - .callout-title (already standard)
     - .prereqs h3, .prerequisites h3
     - .objectives h3
     - .comparison-table-title
     - .bib-category (FOUNDATIONAL TEXTBOOKS, KEY PAPERS & RESOURCES)
     - .exercise-type
     - .lab-title
   Apply a unified `.unified-callout-title` set of rules to ALL of
   these so they render with the same typography on Kindle.

3. JUSTIFY TEXT IN BULLET POINTS
   User: "justify text in bullet points across the book"
   `li` text was left-aligned (ragged right) while `p` is justified,
   creating visual inconsistency. Apply `text-align: justify` to all
   list items, with hyphens to prevent rivers.

4. SPLIT AUTHOR BIO CARD TO START IMMEDIATELY AFTER HEADER
   User: "split author bio card so start immediately after 'about the
   author' header"
   The first `.author-card` after the `About the Authors` heading had
   a margin-top from generic `.author-card { margin-top: 1em }` rules.
   Pull the first card flush against the heading.

5. BIBLIOGRAPHY CALLOUT FORMAT WITH TITLE
   User: "reference and bibliography, lost callout format, no title,
   many non-standard"
   The screenshot shows the bibliography section as a plain list
   without the callout-box typography (no boxed title, just bare
   bold text). Wrap `.bibliography` (and `section.bibliography`) in
   a callout-like visual treatment: subtle left border, padded
   section title.

6. EMPTY PAGES BETWEEN FRONT-MATTER CHAPTERS
   User: "tow empty pages before this, why? / empty pages between
   front matter pages, why?"
   Each chapter XHTML is a separate spine item; the reader inserts an
   implicit page-break before each. When a short front-matter chapter
   ends mid-page, the reader pads with an empty page before the next.
   Mitigation: `page-break-before: auto` on chapter-header (instead
   of `always`), and remove top margin on `body > *:first-child` for
   front-matter chapters so they start at the visual top of the page.
   We can't eliminate spine-induced page breaks at the EPUB level
   (Kindle decides), but we can ensure each chapter starts at the
   visual top of its first page.

7. INLINE MATH FLOATING (ROOT CAUSE FIXED OUT-OF-BAND)
   The actual cause was: KaTeX `node_modules` was missing from this
   git worktree. The math_render.py silently caught the import
   failure and left raw `<span class="math">$\eta$</span>` in HTML,
   which Kindle then rendered with the wrapper as a separate block
   (effectively "floating" above the line). Fixed by copying
   `node_modules` from the sibling worktree before this rebuild.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v794 CONSOLIDATED USER FEEDBACK FIXES
 * ============================================================ */

/* 1. DROP BIBLIOGRAPHY PER-ENTRY BADGES
 * The category header (FOUNDATIONAL TEXTBOOKS, KEY PAPERS &
 * RESOURCES) already groups entries; per-entry "Book" / "Paper" /
 * "Blog post" pills are redundant. */
.bib-meta,
.bib-entry-card .bib-meta,
.bib-entry-card > .bib-meta,
.bib-entry > .bib-meta,
.bib-entry-card .badge,
.bib-entry > .badge,
span.bib-meta {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* 2. UNIFIED CALLOUT-TITLE TYPOGRAPHY
 * Every title-like element gets the same sans-serif uppercase
 * treatment so the reader recognizes "this is a section heading
 * inside a structured block" regardless of which block it is.
 * Single source of truth for typography. */
.callout-title,
.prereqs h3,
.prerequisites h3,
.objectives h3,
.objectives > h3,
.comparison-table-title,
.bib-category,
.exercise-type,
.lab-title,
.bibliography h3,
.bibliography-section h3,
section.bibliography h3,
.whats-next-title,
.what-next-title,
.what-next h3,
.whats-next h3,
.math-block-label {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92em !important;
    line-height: 1.3 !important;
    margin: 0 0 0.5em 0 !important;
    padding-bottom: 0.2em !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid currentColor !important;
    display: block !important;
    color: inherit !important;
}

/* The bibliography category headings need a clearer color (navy
 * matches the rest of the book's structural accents). */
.bib-category,
.bibliography h3,
section.bibliography h3 {
    color: #1a4078 !important;
    border-bottom-color: #c5cae9 !important;
}

/* 3. JUSTIFY TEXT IN BULLET POINTS AND NUMBERED LISTS
 * `p` was already justified; list items were left-ragged. */
li,
ul li,
ol li,
ul > li,
ol > li,
ul li p,
ol li p {
    text-align: justify !important;
    -webkit-hyphens: auto !important;
    hyphens: auto !important;
    -ms-hyphens: auto !important;
}
/* Nested lists: keep first-line indent normal (don't double-indent) */
li > ul,
li > ol {
    text-align: left !important;  /* sub-list bullets stay close to bullet */
}
/* Don't justify list items that are interactive (TOC links, nav).
 * Only justify body lists. */
nav li,
.toc li,
.table-of-contents li,
.chapter-nav li,
.breadcrumb li,
.section-list li,
.sections-list li,
.section-grid li,
.section-grid > a,
ul.outline li {
    text-align: left !important;
    -webkit-hyphens: none !important;
    hyphens: none !important;
}

/* 4. SPLIT AUTHOR BIO CARD TO START AT HEADER
 * The first .author-card after "About the Authors" heading should
 * snug up to the heading (no extra gap). */
h1 + .author-card,
h2 + .author-card,
h2 + .author-cards > .author-card:first-child,
h2 + div > .author-card:first-child,
.about-authors > h1 + .author-card,
.about-authors > h2 + .author-card,
.about-the-authors > h1 + .author-card,
.about-the-authors > h2 + .author-card,
section.about-authors h2 + .author-card,
section h2 + .author-card,
h2 + p + .author-card {
    margin-top: 0 !important;
    padding-top: 0.4em !important;
    page-break-before: avoid !important;
    break-before: avoid !important;
}
/* Heading immediately followed by author cards: keep close */
h1.about-title,
h2.about-title,
.about-authors h1,
.about-authors h2,
.about-the-authors h1,
.about-the-authors h2 {
    margin-bottom: 0.4em !important;
    padding-bottom: 0.2em !important;
}

/* 5. BIBLIOGRAPHY CALLOUT FORMAT WITH TITLE
 * Restore a visible callout-style frame around the bibliography
 * section. Subtle navy left border (matches other structural
 * blocks), explicit BIBLIOGRAPHY title at the top. */
.bibliography,
section.bibliography,
.bibliography-section {
    margin: 1.2em 0 0.8em !important;
    padding: 0.8em 1em 0.6em !important;
    border: none !important;
    border-left: 4px solid #1a4078 !important;
    border-top: 1px solid #c5cae9 !important;
    background: #f8f9fc !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}
.bibliography > h2:first-child,
section.bibliography > h2:first-child,
.bibliography-title {
    margin: 0 0 0.6em 0 !important;
    padding-bottom: 0.3em !important;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-weight: 700 !important;
    font-size: 1em !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #1a4078 !important;
    border-bottom: 1px solid #c5cae9 !important;
    display: block !important;
}

/* 6. EMPTY-PAGE MITIGATION (front-matter and chapter starts)
 * We can't fully control the EPUB reader's pagination, but we can
 * ensure each chapter's first content has zero top margin so it
 * starts at the visual top of its first page without padding. */
body > main:first-child,
body > main.content:first-child,
body > main.content > *:first-child,
body > .chapter-header {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
/* For chapter-header that DOES have padding, only the top is
 * trimmed; bottom can keep its rhythm */
body > header.chapter-header,
header.chapter-header {
    margin-top: 0 !important;
    padding-top: 0.3em !important;
}
/* Don't force a page break BEFORE every chapter (let the reader's
 * default spine pagination handle it). This was causing extra
 * pages in some readers. */
.chapter-header,
header.chapter-header,
main.content {
    page-break-before: auto !important;
    break-before: auto !important;
}
/* Front-matter chapter headers were ending mid-page; reduce
 * bottom padding so the next chapter packs in tighter. */
.front-matter .chapter-header,
.fm-chapter .chapter-header,
body.front-matter .chapter-header {
    padding-bottom: 0.4em !important;
    margin-bottom: 0.4em !important;
}

/* 7. INLINE MATH BASELINE - reinforce v791 (also see node_modules
 * fix that actually causes math to render). The selector here
 * targets BOTH the now-rendered katex output AND any leftover
 * raw <span class="math"> wrapper (which should no longer occur
 * after the rebuild but is defensive). */
span.math,
span.math:not(.katex-display) {
    display: inline !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
    vertical-align: baseline !important;
    line-height: inherit !important;
    font-size: 1em !important;
    white-space: normal !important;
}
'''

START = '/* ============================================================\n * v794 CONSOLIDATED'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v794 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v794 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
print(f'  size now: {len(s):,} chars')
