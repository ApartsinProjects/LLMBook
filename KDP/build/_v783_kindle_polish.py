"""v783: Comprehensive Kindle rendering polish per user feedback.

Issues addressed:

1. CODE RENDERING BROKEN (visible everywhere)
   Root cause: pygments.css uses Monokai DARK theme (variable names
   colored #f8f8f2 = white). EPUB forces <pre> background to LIGHT, so
   white text becomes invisible.
   Fix: regenerated pygments.css with 'friendly' light theme (already
   done in this commit).

2. CHAPTER NAVY BAND MISSING
   Root cause: epub_overrides has the rule but Kindle's color renderer
   may strip backgrounds during Mobi conversion. Add a strong colored
   TOP BORDER as visual fallback (borders are universally supported).

3. FM.3.1 BOXES NOT CENTERED (spillover from band color)
   Root cause: tinted background bands extend wider than box content.
   Fix: regenerate FM.3.1 v5 WITHOUT background tint bands (clean
   white background only).

4. TEXT NOT JUSTIFIED
   Add `text-align: justify` to body <p> in epub_overrides.

5. TABLE CELL CENTERING
   Add `vertical-align: middle` to <td> and <th>.

6. MATH SYMBOL AT END (decorative tooltip glyph)
   The .comparison-table-title::after and .exercise-type::after rules
   use content: attr(title) which renders the title attribute as a
   visible glyph. Suppress these too.

7. PAGE BREAK INSIDE CALLOUTS
   Add `page-break-inside: avoid` to .callout, .code-block-wrapper,
   <figure>, <pre>.

8. EXERCISE BOX HEADER LAYOUT
   Add `display: block` (not flex) to .callout-title for Kindle.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

# Add the fallback colored top border + justify + table + page-break rules
NEW_BLOCK = '''
/* ============================================================
 * v783 Kindle polish (per user feedback after KPV preview)
 * ============================================================ */

/* CHAPTER HEADER: belt-and-suspenders fallback for the navy band.
 * Kindle's Mobi conversion sometimes strips background colors. A solid
 * BORDER survives the conversion reliably and gives the same "this is
 * a new chapter" visual cue at the top of every chapter. */
.chapter-header {
    border-top: 6px solid #1a1a2e !important;
    border-bottom: 1px solid #c9d3df !important;
}

/* JUSTIFIED BODY TEXT for printed-book feel on Kindle */
.content > p,
.content > div > p,
.callout > p,
.callout-body > p,
.author-info > p {
    text-align: justify !important;
    text-justify: inter-word;
    hyphens: auto;
    -webkit-hyphens: auto;
}

/* TABLE CELL CENTERING. Header cells get center horizontally; body
 * cells stay top-aligned but middle-vertical for short cells. */
table th {
    vertical-align: middle !important;
    text-align: left !important;
    padding: 0.5em 0.75em !important;
    background: #f1f5f9 !important;
}
table td {
    vertical-align: middle !important;
    padding: 0.5em 0.75em !important;
}
.complex-table th,
.complex-table td {
    vertical-align: middle !important;
}

/* PAGE-BREAK CONTROL: keep callouts, code blocks, figures, and key
 * takeaways together so they do not split mid-content. */
.callout,
.code-block-wrapper,
.callout pre,
figure,
.diagram-container,
.diagram,
.author-card {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
/* Allow pre to break if it is too long for one page (very long code
 * blocks would otherwise create a huge orphan page). */
pre {
    page-break-inside: auto !important;
    break-inside: auto !important;
}

/* CALLOUT TITLE SPACING: tighten margin above the title (user said
 * "too much margin on top, above title of takeaway box"). */
.callout {
    padding: 0.6em 0.9em 0.7em !important;
    margin: 1em 0 !important;
}
.callout-title {
    margin: 0 0 0.5em 0 !important;
    padding: 0 !important;
}
.callout > p:first-of-type {
    margin-top: 0 !important;
}

/* MATH BLOCK: suppress decorative tooltips that Kindle renders as a
 * visible square at the end of the formula. The hover-tooltip pattern
 * was already neutered for .callout-title::after, .prereqs h3::after,
 * etc. but two more sites use it: .comparison-table-title::after and
 * .exercise-type::after. Force display:none for ALL ::after that uses
 * content: attr(title) (defensive, catches any future tooltip pattern). */
.comparison-table-title::after,
.exercise-type::after,
[title]::after {
    /* Defang any ::after whose content references attr(title). Kindle
     * cannot show the hover state, so the tooltip text/glyph would
     * always be visible without this rule. */
    content: none !important;
    display: none !important;
}

/* EXERCISE BOX HEADER LAYOUT: replace any flex on the callout title
 * with simple block layout that Kindle reliably supports. */
.callout.exercise .callout-title,
.exercise .callout-title {
    display: block !important;
    text-align: left !important;
}
'''

if '/* v783 Kindle polish' not in s:
    s = s.rstrip() + '\n' + NEW_BLOCK
    overrides.write_text(s, encoding='utf-8')
    print(f'  [v783 polish block added to epub_overrides.css '
          f'({len(NEW_BLOCK)} chars)]')
else:
    print('  [v783 polish already present, skip]')
