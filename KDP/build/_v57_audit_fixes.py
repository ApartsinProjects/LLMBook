"""v5.7: bundle of audit fixes.

A. ToC chapter 37 cleanup
   - Module 37 ("Building & Steering AI Products") was merged into Module 36
     in v3.x as sections 36.4-36.7, but toc.html still has a phantom
     "Ch 37" row in two places.
   - Compact view (line ~158): a "Ch 37" dense-chapter row pointing at
     a relative `index.html` (= homepage) instead of any real page.
   - Expanded view (line ~298-301): the Ch 36 dense-sections list ends
     with a duplicate "36.4 Case Studies" pointing at section-36.3.html
     (Case Studies was deleted), then an orphan "Ch 37" row, then a
     dense-sections list of "37.1 ... 37.5" pointing at section-36.4-7.
   - Fix: regenerate Ch 36 dense-sections from actual files (36.1-36.7),
     drop the standalone Ch 37 row, drop the 37.x sub-section list.

B. Orphan code-caption immediately before <div class="callout library-shortcut">
   - 70 occurrences across the book. Pattern:
       <div class="code-caption"><strong>Code Fragment X.Y.Z:</strong> ...</div>
       <div class="callout library-shortcut">
   - Library-shortcut callouts already have their own
     <div class="callout-title">Library Shortcut: ...</div> heading.
     The extra "Code Fragment X.Y.Z:" caption above the callout is an
     authoring artifact (often duplicating the previous fragment's text).
   - Fix: delete the orphan caption div.

C. Bottom navigation missing on two real pages
   - appendices/appendix-a-mathematical-foundations/section-a.6.html
   - part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html
   - Add `<nav class="chapter-nav">` + standard `<footer>` block
     before `</main>`.

D. Code Fragment 33.8.4a: pseudo-YAML data presented as code
   - Located in part-9-safety-strategy/module-33-strategy-product-roi/section-33.7.html
   - Content is a hand-coded breakeven analysis with hardcoded numbers.
     A table communicates the same data more directly.
   - Fix: replace the <div class="code-block-wrapper"><pre>...</pre></div>
     <div class="code-caption">...</div> block with a <table> + caption.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


# ----- A. ToC chapter 37 cleanup --------------------------------------

def fix_toc_ch37(toc_path: Path) -> int:
    text = toc_path.read_text(encoding="utf-8")
    original = text
    fixes = 0

    # A.1 Compact-view orphan Ch 37 row (line 158).
    # The line literal ends with </div> and is sandwiched between Ch 36 and Ch 38.
    pat_compact = re.compile(
        r'\s*<div class="dense-chapter"><span class="dense-ch-num">Ch 37</span>'
        r' <a href="index.html">Building and Steering AI Products</a></div>\n',
    )
    new, n = pat_compact.subn('', text, count=1)
    if n:
        text = new
        fixes += n

    # A.2 Expanded-view Ch 36 dense-sections (current line has duplicate
    # "36.4 Case Studies" pointing at section-36.3.html which is wrong).
    # Replace with the canonical 36.1-36.7 list.
    NEW_CH36_SECTIONS = (
        '<div class="dense-sections">'
        '<a href="part-11-idea-to-product/module-36-idea-to-product/section-36.1.html">36.1 What Makes AI Products Different</a> &middot; '
        '<a href="part-11-idea-to-product/module-36-idea-to-product/section-36.2.html">36.2 Choosing the Model&#39;s Role</a> &middot; '
        '<a href="part-11-idea-to-product/module-36-idea-to-product/section-36.3.html">36.3 Risk and Feasibility Assessment</a> &middot; '
        '<a href="part-11-idea-to-product/module-36-idea-to-product/section-36.4.html">36.4 The Observe-Steer Development Loop</a> &middot; '
        '<a href="part-11-idea-to-product/module-36-idea-to-product/section-36.5.html">36.5 The Founder&#39;s Prototype Loop</a> &middot; '
        '<a href="part-11-idea-to-product/module-36-idea-to-product/section-36.6.html">36.6 Documentation as Control Surface</a> &middot; '
        '<a href="part-11-idea-to-product/module-36-idea-to-product/section-36.7.html">36.7 From Prototype to MVP</a>'
        '</div>'
    )
    pat_ch36_sections = re.compile(
        r'<div class="dense-sections">'
        r'<a href="part-11-idea-to-product/module-36-idea-to-product/section-36\.1\.html">36\.1[^<]*</a>'
        r'.*?</div>',
        re.DOTALL,
    )
    new, n = pat_ch36_sections.subn(NEW_CH36_SECTIONS, text, count=1)
    if n:
        text = new
        fixes += n

    # A.3 Drop the orphan Ch 37 row + its dense-sections in expanded view.
    pat_expanded_ch37 = re.compile(
        r'<div class="dense-chapter"><span class="dense-ch-num">Ch 37</span>'
        r' <a href="index.html">Building and Steering AI Products</a></div>\n'
        r'<div class="dense-sections">'
        r'<a href="part-11-idea-to-product/module-36-idea-to-product/section-36\.4\.html">37\.1[^<]*</a>'
        r'.*?</div>\n',
        re.DOTALL,
    )
    new, n = pat_expanded_ch37.subn('', text, count=1)
    if n:
        text = new
        fixes += n

    # Only write + count if content actually changed (subn counts pattern
    # matches, not real edits — A.2's replacement equals existing content
    # after the first run, which would otherwise look like an endless loop).
    if text == original:
        return 0
    toc_path.write_text(text, encoding="utf-8")
    return fixes


# ----- B. Orphan caption before library-shortcut ----------------------

ORPHAN_CAP_LIB = re.compile(
    r'<div class="code-caption">[^<]*<strong>Code Fragment [^<]+:</strong>[^<]*</div>\s*'
    r'(?=<div class="callout library-shortcut">)',
    re.IGNORECASE,
)


def fix_orphan_caps(p: Path) -> int:
    """Iteratively strip stacked orphan captions before a library-shortcut.

    Some files have N captions stacked above one library-shortcut. Each
    pass deletes one; we loop until stable.
    """
    text = p.read_text(encoding="utf-8", errors="replace")
    total = 0
    while True:
        new, n = ORPHAN_CAP_LIB.subn('', text)
        if n == 0:
            break
        total += n
        text = new
    if total:
        p.write_text(text, encoding="utf-8")
    return total


# ----- C. Add bottom nav to two pages --------------------------------

NAV_AND_FOOTER = (
    '<nav class="chapter-nav">\n'
    '<a class="prev" href="{prev_href}">{prev_label}</a>\n'
    '<a class="up" href="{up_href}">{up_label}</a>\n'
    '<a class="next" href="{next_href}">{next_label}</a>\n'
    '</nav>\n'
    '<footer><p>Fifth Edition, 2026 &middot; <a href="{toc_href}">Contents</a></p></footer>\n'
)


def add_bottom_nav(p: Path, **fields) -> bool:
    text = p.read_text(encoding="utf-8")
    if '<nav class="chapter-nav">' in text:
        return False
    nav_block = NAV_AND_FOOTER.format(**fields)
    new = text.replace('</main>', nav_block + '</main>', 1)
    if new == text:
        return False
    p.write_text(new, encoding="utf-8")
    return True


# ----- D. Convert 33.8.4a YAML to a table ----------------------------

OLD_YAML_BLOCK_HINT = 'Code Fragment 33.8.4a'


def fix_33_8_4a(p: Path) -> int:
    text = p.read_text(encoding="utf-8")
    if OLD_YAML_BLOCK_HINT not in text:
        return 0

    # The block looks like:
    #   <div class="code-block-wrapper">
    #     <pre><code class="...lang-yaml">...</code></pre>
    #     <div class="code-caption">...33.8.4a...</div>
    #   </div>
    # The caption is INSIDE the wrapper, with the wrapper's closing </div>
    # coming after the caption div.
    pat = re.compile(
        r'<div class="code-block-wrapper">\s*<pre><code class="pygments-highlighted lang-yaml"[^>]*>'
        r'(?:.|\n)*?</code></pre>\s*'
        r'<div class="code-caption"><strong>Code Fragment 33\.8\.4a:</strong>[^<]*</div>\s*'
        r'</div>',
        re.IGNORECASE,
    )

    REPLACEMENT = (
        '<div class="figure-container">\n'
        '<table class="data-table">\n'
        '<caption><strong>Table 33.7.1:</strong> Build vs. buy breakeven analysis. '
        'API-based Claude Sonnet 4 at $0.0135 per request vs. self-hosted Llama 3.3 70B '
        'on two H100s at $0.00875 per request. The raw crossover is at 373K requests per month, '
        'but adding $15K of monthly engineering operations cost pushes the adjusted '
        'breakeven to nearly 1.5 million requests per month.</caption>\n'
        '<thead>\n'
        '<tr><th>Cost component</th><th>API (Claude Sonnet 4)</th><th>Self-hosted (Llama 3.3 70B, 2 &times; H100)</th></tr>\n'
        '</thead>\n'
        '<tbody>\n'
        '<tr><td>Per-request cost</td><td>$0.0135</td><td>$0.00875</td></tr>\n'
        '<tr><td>Fixed monthly infrastructure</td><td>$0 (pay-per-use)</td><td>$5,040 (2 GPUs &times; $3.50/hr &times; 720 hrs)</td></tr>\n'
        '<tr><td>Engineering operations overhead</td><td>$0</td><td>~$15,000/month equivalent</td></tr>\n'
        '<tr><td><strong>Raw breakeven volume</strong></td><td colspan="2">373,333 requests/month (cost-only crossover)</td></tr>\n'
        '<tr><td><strong>Adjusted breakeven volume</strong></td><td colspan="2">1,484,000 requests/month (including ops overhead)</td></tr>\n'
        '</tbody>\n'
        '</table>\n'
        '</div>'
    )

    new, n = pat.subn(REPLACEMENT, text, count=1)
    if n:
        p.write_text(new, encoding="utf-8")
    return n


# ----- Driver --------------------------------------------------------

def main() -> int:
    print("v5.7 audit fixes\n" + "=" * 50)

    # A
    toc = ROOT / "toc.html"
    n_a = fix_toc_ch37(toc)
    print(f"A. toc.html Ch 37 cleanup: {n_a} edits")

    # B
    SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
            'chapter_review', 'downloads', '_archive', '_lab_fragments',
            'templates'}
    files_b, total_b = 0, 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        n = fix_orphan_caps(p)
        if n:
            files_b += 1
            total_b += n
    print(f"B. Orphan caption-before-library-shortcut: {total_b} dropped across {files_b} files")

    # C
    n_c = 0
    if add_bottom_nav(
        ROOT / "appendices/appendix-a-mathematical-foundations/section-a.6.html",
        prev_href="section-a.5.html",
        prev_label="A.5 Connecting the Pieces",
        up_href="index.html",
        up_label="Appendix A: Mathematical Foundations",
        next_href="../appendix-b-ml-essentials/index.html",
        next_label="Appendix B: Machine Learning Essentials",
        toc_href="../../toc.html",
    ):
        n_c += 1
    if add_bottom_nav(
        ROOT / "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html",
        prev_href="section-6.8.html",
        prev_label="6.8 Production LLM Training Systems",
        up_href="index.html",
        up_label="Chapter 6: Pre-training, Scaling Laws & Data Curation",
        next_href="../module-07-modern-llm-landscape/index.html",
        next_label="Chapter 7: Modern LLM Landscape & Model Internals",
        toc_href="../../toc.html",
    ):
        n_c += 1
    print(f"C. Bottom-nav inserted on: {n_c} pages")

    # D
    n_d = fix_33_8_4a(
        ROOT / "part-9-safety-strategy/module-33-strategy-product-roi/section-33.7.html"
    )
    print(f"D. Code Fragment 33.8.4a YAML -> table: {n_d} edit")

    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
