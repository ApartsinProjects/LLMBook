"""v785: Comprehensive callout color/typography polish + landscape
two-page tablet rendering (no half-empty pages) + final tooltip-glyph
suppression + light-background code blocks.

WHAT THIS FIXES (re-reading user feedback in detail)
====================================================

1. CODE BLOCKS UNREADABLE
   v783 fixed pygments.css to a LIGHT theme (`friendly`), but
   default_overrides.css still forces `pre { background: #1e1e2e;
   color: #cdd6f4 }` - a DARK background. On Kindle the background is
   often stripped while the foreground color is honored, leaving light
   text on white - the exact "invisible code" the user reported.
   Fix: switch `pre` to a light GitHub-style background (#f6f8fa with
   #24292f text) so the friendly-theme dark green/blue/red token colors
   are readable AND survive Kindle's background stripping.

2. CALLOUT BOXES - "BEST DESIGN" UNIFICATION
   The 19 callout variants in book.css use `linear-gradient(135deg, ...)`
   for backgrounds. Kindle's Mobi converter:
     - drops gradients on most renderers (background goes white)
     - sometimes keeps the second stop (which is usually almost-white anyway)
   Either way the effect collapses, leaving the callout looking like a
   plain bordered block.
   Fix: explicitly set SOLID light backgrounds (the lighter of the two
   gradient stops) for every variant, with semantic accent border-left
   in the canonical category color. Also unify: 4px solid border-left,
   1px solid border-color (lighter shade), 0.7em/0.9em padding,
   0.85em/0.95em titles in the accent color.

3. PAGE BREAKS - "AVOID HALF-EMPTY PAGES IN LANDSCAPE TWO-PAGE READ"
   v783 incorrectly added `page-break-inside: avoid !important` to
   `.callout`, `figure`, `.code-block-wrapper`. On landscape tablet
   two-page view, a long callout that doesn't fit at the bottom of
   page-N gets pushed entirely to page-N+1, creating a HALF-EMPTY
   page-N. The user explicitly said: "avoid empty spaces, audit and fix
   everywhere".
   Fix:
     - LONG containers (callouts, code wrappers, math blocks): allow
       page-break-inside auto WITH `box-decoration-break: clone` so the
       border/padding repaints cleanly on each page-fragment.
     - SHORT atomic blocks (figure, .author-card, .key-takeaway,
       chapter-header): keep `avoid` because they SHOULD stay together.
     - Headings (h1-h4): page-break-after: avoid (so a heading isn't
       orphaned at the column bottom with content on next column).
     - widows: 2; orphans: 2 globally so a 1-line trailing remnant is
       acceptable (avoid pushing a near-full block to next page).

4. TOOLTIP GLYPH AT END OF MATH SECTIONS
   v783's `[title]::after` rule only catches elements that have an
   HTML `title=""` attribute. Many of the tooltip ::after rules in
   book.css use class selectors (e.g. `.prereqs h3::after`,
   `.objectives h3::after`, `.callout .callout-title::after`) and rely
   on `opacity: 0` + hover to hide. Kindle ignores `opacity: 0` on some
   renderers and reveals the tooltip text as a visible block under
   every titled element - looks like a stray glyph or text fragment.
   Fix: explicitly set `display: none !important` on every ::after that
   has hover-only intent. This is the safe catch-all.

5. EXERCISE HEADER LAYOUT (already in v783, refined)
   `.callout.exercise .callout-title` was set to `display: block`
   in v783. Refine: also kill the icon ::before (PNG) on Kindle if the
   PNG didn't bundle, since the empty box renders as tofu (square).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v785 callout typography + landscape two-page tablet polish
 * ============================================================ */

/* ---- 1. CODE BLOCKS: light background to match the friendly Pygments
 *        theme (dark green/blue/red tokens). The previous dark theme
 *        (#1e1e2e) was stripped by Kindle leaving invisible light text.
 *        GitHub-style #f6f8fa / #24292f is the same palette as github.com
 *        and survives Kindle's background-stripping because we use a
 *        very light gray (the eye still reads it as "code panel"). */
pre {
    background: #f6f8fa !important;
    color: #24292f !important;
    border: 1px solid #d0d7de !important;
    padding: 0.7em 0.9em !important;
    border-radius: 4px !important;
    line-height: 1.45 !important;
    font-size: 0.88em !important;
    overflow-x: auto !important;
    /* Allow long code to break across pages; render the border on each
     * fragment so it doesn't visually "open" mid-block. */
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
}
pre code, pre code.pygments-highlighted {
    background: transparent !important;
    color: inherit !important;
    padding: 0 !important;
}
:not(pre) > code {
    background: #f3f4f6 !important;
    color: #1f2937 !important;
    padding: 0.1em 0.3em !important;
    border-radius: 3px !important;
    font-size: 0.92em !important;
}

/* ---- 2. CALLOUT BOXES: unified solid-color design.
 *        Kindle drops gradient backgrounds, so we explicitly set the
 *        lighter solid color. Border-left (4px) is the primary visual
 *        identifier; thin border on the other three sides ties the box
 *        together. Title is bold, in the accent color, no icon (PNG
 *        icons render as tofu when Kindle doesn't bundle them). */
.callout {
    background: #fafafa !important;
    border: 1px solid #e0e0e0 !important;
    border-left: 4px solid #9e9e9e !important;
    border-radius: 0 4px 4px 0 !important;
    padding: 0.7em 0.9em !important;
    margin: 1em 0 !important;
    /* CRITICAL: allow long callouts to break across pages so we don't
     * leave huge empty space at the bottom of the previous page in
     * landscape two-column view. The clone box-decoration repaints
     * the border/padding on each page fragment. */
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
    widows: 2 !important;
    orphans: 2 !important;
}
.callout-title {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95em !important;
    letter-spacing: 0.3px !important;
    margin: 0 0 0.4em 0 !important;
    padding: 0 !important;
    display: block !important;
    text-align: left !important;
}
.callout p, .callout li { line-height: 1.5 !important; }
.callout p:last-child { margin-bottom: 0 !important; }

/* SUPPRESS PNG ICONS in callout titles. They were loaded via
 * background-image: url('icons/...') which Kindle often fails to
 * bundle correctly, leaving empty 1.2em x 1.2em boxes (tofu) before
 * every title. Use the title text + accent color instead. */
.callout .callout-title::before {
    content: none !important;
    display: none !important;
    background: none !important;
}

/* SUPPRESS HOVER TOOLTIPS (::after pseudo-elements). On desktop these
 * are hidden via opacity: 0 + revealed on hover. Kindle has no hover
 * AND ignores opacity on some renderers, so the tooltip text leaks
 * out as a visible glyph. Force display:none across every known
 * tooltip carrier. */
.callout .callout-title::after,
.prereqs h3::after,
.prerequisites h3::after,
.objectives h3::after,
.comparison-table-title::after,
.exercise-type::after,
[title]::after {
    content: none !important;
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    width: 0 !important;
}

/* Per-variant solid colors. Each pair is (background, accent-border,
 * title-color). Backgrounds are very light tints so the box is visually
 * present without dominating the page; accents are saturated. */
.callout.big-picture        { background: #f3e5f5 !important; border-color: #e1bee7 !important; border-left-color: #8e24aa !important; }
.callout.big-picture .callout-title        { color: #6a1b9a !important; }

.callout.key-insight        { background: #e8f5e9 !important; border-color: #c8e6c9 !important; border-left-color: #43a047 !important; }
.callout.key-insight .callout-title        { color: #1b5e20 !important; }

.callout.note               { background: #e3f2fd !important; border-color: #bbdefb !important; border-left-color: #1976d2 !important; }
.callout.note .callout-title               { color: #0d47a1 !important; }

.callout.warning            { background: #fff8e1 !important; border-color: #ffe0b2 !important; border-left-color: #f57c00 !important; }
.callout.warning .callout-title            { color: #b71c1c !important; }

.callout.practical-example  { background: #eceff1 !important; border-color: #cfd8dc !important; border-left-color: #5dade2 !important; }
.callout.practical-example .callout-title  { color: #1a4078 !important; }

.callout.fun-note           { background: #fce4ec !important; border-color: #f8bbd0 !important; border-left-color: #e91e63 !important; }
.callout.fun-note .callout-title           { color: #ad1457 !important; }

.callout.research-frontier  { background: #ede7f6 !important; border-color: #d1c4e9 !important; border-left-color: #5e35b1 !important; }
.callout.research-frontier .callout-title  { color: #311b92 !important; }

.callout.algorithm          { background: #f3effc !important; border-color: #d1c4e9 !important; border-left-color: #4a55a2 !important; }
.callout.algorithm .callout-title          { color: #2e3990 !important; }

.callout.tip                { background: #e0f7fa !important; border-color: #b2ebf2 !important; border-left-color: #00acc1 !important; }
.callout.tip .callout-title                { color: #006064 !important; }

.callout.exercise           { background: #fff3e0 !important; border-color: #ffe0b2 !important; border-left-color: #e64a19 !important; }
.callout.exercise .callout-title           { color: #c62828 !important; }

.callout.self-check         { background: #e8eaf6 !important; border-color: #c5cae9 !important; border-left-color: #3949ab !important; }
.callout.self-check .callout-title         { color: #283593 !important; }

.callout.library-shortcut   { background: #e0f2f1 !important; border-color: #b2dfdb !important; border-left-color: #00897b !important; }
.callout.library-shortcut .callout-title   { color: #00695c !important; }

.callout.looking-back       { background: #eceff1 !important; border-color: #cfd8dc !important; border-left-color: #455a64 !important; }
.callout.looking-back .callout-title       { color: #263238 !important; }

.callout.cross-ref          { background: #fafafa !important; border-color: #cfd8dc !important; border-left-color: #607d8b !important; }
.callout.cross-ref .callout-title          { color: #37474f !important; }

.callout.production-pattern { background: #e0f2f1 !important; border-color: #b2dfdb !important; border-left-color: #00695c !important; }
.callout.production-pattern .callout-title { color: #004d40 !important; }

.callout.postmortem         { background: #fff3e0 !important; border-color: #ffcc80 !important; border-left-color: #b71c1c !important; }
.callout.postmortem .callout-title         { color: #b71c1c !important; }

.callout.thesis-thread      { background: #e8eaf6 !important; border-color: #c5cae9 !important; border-left-color: #283593 !important; }
.callout.thesis-thread .callout-title      { color: #1a237e !important; }

.callout.numeric-example,
.callout.numerical-example  { background: #fff8e1 !important; border-color: #ffecb3 !important; border-left-color: #ff9800 !important; }
.callout.numeric-example .callout-title,
.callout.numerical-example .callout-title  { color: #e65100 !important; }

/* Key Takeaway (warm gold) - usually short, keep it whole */
.callout.key-takeaway {
    background: #fff8e1 !important;
    border-color: #ffd54f !important;
    border-left-color: #f9a825 !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
.callout.key-takeaway .callout-title { color: #e65100 !important; }

/* ---- 3. PAGE-BREAK CORRECTIONS for landscape two-page reading.
 *        Reversal of the over-aggressive v783 `avoid` rules. Only items
 *        that MUST stay together on one page get `avoid`; everything
 *        else gets `auto` so we don't waste half a column. */

/* Items that MUST stay together (small, atomic) */
figure,
.figure,
.author-card,
.chapter-header,
.diagram-container img,
.callout.key-takeaway {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* Items that should be ALLOWED to break (large, fluid) */
.callout,
.callout.exercise,
.callout.algorithm,
.code-block-wrapper,
.exercises-container,
.bibliography,
section.bibliography,
.math-block,
table {
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
}

/* Headings: never orphan at column/page bottom */
h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid !important;
    break-after: avoid !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
/* Heading + first paragraph stay together */
h2 + p, h3 + p, h4 + p {
    page-break-before: avoid !important;
    break-before: avoid !important;
}

/* Body widows/orphans */
body, p {
    widows: 2 !important;
    orphans: 2 !important;
}

/* ---- 4. EXERCISES container: open by default and breakable so a
 *        block of 6 exercises doesn't get shoved to a fresh column. */
.exercises-container {
    page-break-inside: auto !important;
    break-inside: auto !important;
}
.exercises-container > details {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* ---- 5. TABLE polish for landscape: header background survives,
 *        cells word-wrap so wide tables don't extend off-page. */
table {
    border-collapse: collapse !important;
    width: 100% !important;
    margin: 0.8em 0 !important;
}
th, td {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
    hyphens: auto !important;
}
'''

# Idempotent insertion: replace previous v785 block if present, else append.
START = '/* ============================================================\n * v785 callout typography'
END_MARKER = 'hyphens: auto !important;\n    }\n}'  # unused; we use START to detect

if START in s:
    # Strip from START to end-of-file (block must be the LAST thing
    # appended). Safe because v786+ would also be appended after.
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v785 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v785 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
