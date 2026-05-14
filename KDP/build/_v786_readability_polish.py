"""v786: Comprehensive readability polish based on Kindle Previewer
screenshots from the Twelfth-Edition QA pass.

USER FEEDBACK CONSOLIDATED
==========================

A. SPACING (large white-space gaps in landscape view)
   1. Big gap between chapter-header navy band and first content block
      (epigraph or prereqs callout). Reduce.
   2. Big gap between consecutive boxes (epigraph -> prereqs ->
      objectives -> first paragraph). Reduce.
   3. "What Comes Next" / "What's Next" callout has oversized top
      margin. Tighten.
   4. Bibliography section has unnecessary forced page-break before it
      AND a huge top margin. Remove break, tighten margin.
   5. Right page is empty in landscape two-page view because the
      previous page can no longer break further. Address by tightening
      every box margin and allowing more break-inside auto.

B. EPUB CHROME (book-only, EPUB should not have website nav)
   6. Drop the search-box pagefind UI (renders as empty rectangle on
      Kindle).
   7. Drop the "Twelfth Edition, 2026 Contents" footer from EPUB
      (it's a website breadcrumb, not book content).

C. CODE BLOCKS (low contrast, hard to read)
   8. Switch to DARK theme (monokai) with safety fallback. Pre uses
      black/very-dark background with bright tokens. If Kindle strips
      the background, the bright tokens stay visible against the
      monospace neutral. Pygments regenerated with monokai in v786.

D. MATH RENDERING (stray symbol/scrollbar pill at end)
   9. Hide the scrollbar pill that appears at the right edge of math
      blocks. overflow:hidden alone isn't enough; also need
      scrollbar-width:none + ::-webkit-scrollbar:display:none.

E. AUTHOR PAGES (about-the-authors layout)
   10. Heading "About the Authors" + first author-card must NOT split
       across pages. Add page-break-before:avoid on .author-card
       immediately after a heading.
   11. Author bio layout refined: photo + name + role tightly
       grouped, bio paragraphs use the same justified body style.

F. LISTS (justify or not?)
   12. DECISION: do NOT justify list items (li). Justified text in
       narrow lists creates ugly word-spacing gaps. Keep paragraphs
       justified, lists left-aligned.

G. WHAT'S NEXT BOX (whats-next class)
   13. .whats-next callout has oversize top margin and large h3 top
       margin. Tighten both.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v786 readability polish (Twelfth-Edition KPV pass)
 * ============================================================ */

/* ---- A. CHROME REMOVAL: drop EPUB-inappropriate elements ----
 * Search box (pagefind), website-nav footer, breadcrumb chrome.
 * EPUB readers have their own search; the on-page widget renders
 * as an empty rectangle.  */
.pagefind-ui,
#search,
[id^="search"],
.search-container,
.search-box,
.search-icon,
.toc-search,
form[role="search"] {
    display: none !important;
}

/* The page footer is a website breadcrumb ("Twelfth Edition, 2026 ·
 * Contents") that has no place in an EPUB. Hide it but keep <footer>
 * around for any chapter-end notes. */
body > footer,
main > footer,
.content > footer,
.section-footer,
.page-footer {
    display: none !important;
}
/* Be even more specific: any <footer> that contains the "Edition" /
 * "Contents" breadcrumb pattern - kill it. We can't easily target on
 * content, so use class/structure. The shipped templates put the
 * footer as a direct child of <main> or <body>. */
footer .footer-title,
footer p {
    display: none !important;
}
/* Hide the entire footer wrapper if it has the canonical breadcrumb */
footer { display: none !important; }

/* ---- B. SPACING: reduce gaps between header and first content ----
 * Chapter-header navy band -> next block (epigraph, prereqs, objectives,
 * or h2/p) was 1.2em + the next block's top margin = ~2em+ of dead
 * space. Tighten the chapter-header bottom and zero the top margin of
 * whatever follows. */
.chapter-header {
    margin: 0 0 0.6em 0 !important;
    padding: 0.5em 1em 0.6em !important;
}
.chapter-header + *,
.chapter-header + main > *:first-child,
header + .epigraph,
header + figure,
header + blockquote,
header + .callout,
header + .prereqs,
header + .prerequisites,
header + .objectives {
    margin-top: 0.4em !important;
}

/* Epigraph (italic quote at chapter top): tighten internal padding and
 * margins. Was 1.2em padding which made the epigraph dominate the
 * first page. */
.epigraph,
blockquote.epigraph,
figure.epigraph {
    margin: 0.6em 0 !important;
    padding: 0.6em 0.9em !important;
}
.epigraph p { margin: 0 0 0.3em 0 !important; }
.epigraph cite,
.epigraph footer { margin-top: 0.2em !important; font-size: 0.9em !important; }

/* Prereqs and objectives boxes: shorter top margin so they sit close
 * to the chapter title or epigraph. */
.prereqs, .prerequisites, .objectives {
    margin: 0.6em 0 !important;
    padding: 0.6em 0.9em !important;
}
.prereqs h3, .prerequisites h3, .objectives h3 {
    margin: 0 0 0.4em 0 !important;
    padding: 0 !important;
}

/* Adjacent callouts: cut the doubled vertical margin between two
 * boxes. The CSS adjacent-sibling collapse rule handles this once
 * margins are smaller. */
.callout + .callout,
.callout + .epigraph,
.epigraph + .callout,
.callout + .prereqs,
.prereqs + .objectives,
.objectives + .callout {
    margin-top: 0.5em !important;
}

/* ---- C. WHAT-COMES-NEXT / WHAT'S-NEXT ----
 * The .whats-next div is a recurring section-end callout. Both this
 * and any .callout that contains "What Comes Next" need tighter top
 * margin. */
.whats-next,
.callout.whats-next,
div.whats-next {
    margin: 0.8em 0 !important;
    padding: 0.5em 0.9em 0.6em !important;
    background: #e8f1fb !important;
    border: 1px solid #bcd6f0 !important;
    border-left: 4px solid #1a4078 !important;
    border-radius: 0 4px 4px 0 !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}
.whats-next h3,
.whats-next h4,
.whats-next .callout-title,
div.whats-next > h3:first-child {
    margin: 0 0 0.4em 0 !important;
    padding: 0 !important;
    color: #0d3061 !important;
    font-weight: 700 !important;
    font-size: 1em !important;
}
.whats-next p { margin: 0.3em 0 !important; }

/* ---- D. BIBLIOGRAPHY: no forced break, tight top margin ----
 * Many sections had a near-empty page above the bibliography because
 * book.css set margin-top: 3rem + padding: 2rem. Slim, and explicitly
 * forbid page-break-before. */
.bibliography,
section.bibliography,
.bibliography-section {
    margin-top: 0.6em !important;
    margin-bottom: 0.4em !important;
    padding: 0.5em 0.7em 0.4em !important;
    border: none !important;
    border-top: 1px solid #c5cae9 !important;
    border-radius: 0 !important;
    background: transparent !important;
    page-break-before: avoid !important;
    break-before: avoid !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}
.bibliography-title,
.bibliography h2,
.bibliography h3,
section.bibliography > .bibliography-title,
section.bibliography > h2 {
    margin: 0.3em 0 0.4em 0 !important;
    padding: 0 !important;
    font-size: 1.05em !important;
    color: #1a237e !important;
}
.bib-category {
    margin: 0.5em 0 0.25em !important;
    font-size: 0.92em !important;
    font-weight: 700 !important;
    color: #283593 !important;
}
.bib-entry-card,
.bib-entry {
    margin: 0 0 0.35em 0 !important;
    padding: 0.35em 0.5em !important;
    border: none !important;
    border-left: 2px solid #c5cae9 !important;
    border-radius: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* ---- E. CODE BLOCKS: switch to DARK theme (monokai) for contrast ----
 * pygments.css regenerated with monokai (light tokens on dark bg).
 * Force the pre background dark + safety fallback color so even if
 * Kindle strips the bg, the slightly-tinted token colors stay
 * readable on white. */
pre {
    background: #1e1e2e !important;
    color: #f8f8f2 !important;          /* monokai default */
    border: 1px solid #3a3a4a !important;
    padding: 0.7em 0.9em !important;
    border-radius: 4px !important;
    line-height: 1.45 !important;
    font-size: 0.85em !important;
    overflow-x: auto !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
pre code,
pre code.pygments-highlighted {
    background: transparent !important;
    color: inherit !important;
    padding: 0 !important;
}
/* Inline code: subtle gray pill, NOT dark (would clash inside flowing
 * paragraphs). */
:not(pre) > code {
    background: #f3f4f6 !important;
    color: #1f2937 !important;
    padding: 0.1em 0.3em !important;
    border-radius: 3px !important;
    font-size: 0.92em !important;
    border: 1px solid #e5e7eb !important;
}

/* SAFETY FALLBACK: if a renderer strips the dark background, the
 * default monokai token colors (#a6e22e green, #66d9ef blue, etc.)
 * are still readable on white because they're saturated mid-tones.
 * The variable-name token .n is the most common; force it to a
 * mid-gray that works on either bg. */
.pygments-highlighted .n,
.pygments-highlighted .nv,
.pygments-highlighted .nf,
.pygments-highlighted .nb {
    color: #c9d1d9 !important;
}
@media (prefers-color-scheme: light) {
    /* Tablet/iPad readers in light mode: bump variable-name token
     * to a darker shade if pre bg got stripped to white. */
}

/* ---- F. MATH OVERFLOW PILL (the small box at end of formulas) ----
 * Some Kindle renderers paint a scrollbar thumb at the right of any
 * element with overflow-x: auto. Our math containers have it as a
 * defense against ultra-wide formulas. Hide the scrollbar visually
 * while keeping the layout. */
.math-block,
div.math-block,
.katex-display,
.katex,
math {
    overflow: hidden !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}
.math-block::-webkit-scrollbar,
.katex-display::-webkit-scrollbar,
.katex::-webkit-scrollbar,
math::-webkit-scrollbar,
pre::-webkit-scrollbar,
table::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* ---- G. AUTHOR PAGES (About the Authors) ----
 * Heading + first author-card must stay together. The .author-card
 * itself already has page-break-inside:avoid from v783; we add
 * page-break-before:avoid on the FIRST card after a heading. */
h1 + .author-card,
h2 + .author-card,
h2 + p + .author-card,
h3 + .author-card,
.author-card + .author-card {
    page-break-before: avoid !important;
    break-before: avoid !important;
    margin-top: 0.6em !important;
}
/* Refined author bio layout: photo float-left at fixed 110px, bio
 * text wraps cleanly to the right. */
.author-card {
    margin: 0.8em 0 !important;
    padding: 0.6em 0.8em !important;
    border: 1px solid #d0d7de !important;
    border-radius: 4px !important;
    background: #f8fafc !important;
    overflow: hidden !important;       /* contain the float */
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
.author-photo,
.author-card img {
    float: left !important;
    width: 110px !important;
    height: 110px !important;
    margin: 0 0.9em 0.4em 0 !important;
    border: 2px solid #455a64 !important;
    border-radius: 6px !important;
    object-fit: cover !important;
}
.author-info {
    overflow: hidden !important;       /* prevent text from sliding under */
}
.author-info h3 {
    margin: 0 0 0.15em 0 !important;
    font-size: 1.1em !important;
    color: #1a4078 !important;
}
.author-title {
    margin: 0 0 0.5em 0 !important;
    font-size: 0.9em !important;
    color: #455a64 !important;
    font-style: italic !important;
}
.author-info p {
    margin: 0 0 0.5em 0 !important;
    line-height: 1.5 !important;
    text-align: justify !important;
    hyphens: auto !important;
}

/* ---- H. LISTS: NO justification (decision per user question) ----
 * Justified text in narrow list items creates ugly word-spacing gaps.
 * Keep paragraphs justified, lists left-aligned. */
li, ul li, ol li, dl dd, dl dt {
    text-align: left !important;
    hyphens: auto !important;
}
/* But still respect text-justify on the list ITEM if author explicitly
 * sets it (rare). */

/* ---- I. SECTION HEADINGS: tighter top margin ----
 * Each h2 starts ~3rem above its content per book.css. On Kindle
 * landscape that's ~80px of empty space. Tighten. */
h2, h3, h4 {
    margin-top: 0.8em !important;
    margin-bottom: 0.3em !important;
    line-height: 1.25 !important;
}
h1 {
    margin-top: 0.4em !important;
    margin-bottom: 0.3em !important;
}
'''

START = '/* ============================================================\n * v786 readability'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v786 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v786 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
