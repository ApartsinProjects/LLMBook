"""v4.0: Move 4.1.2 'Information Theory: The Language of Learning' from
section 4.1 to Appendix A as a new section A.6.

Mechanics:
  1. Extract everything between '<h2...>4.1.2 Information Theory...</h2>'
     and the next '<h2...>4.1.3' tag in section-4.1.html.
  2. Write a new section-a.6.html in appendix-a-mathematical-foundations
     using the extracted content (rewrap in proper Appendix A header).
  3. Replace the 4.1.2 block in section-4.1.html with a 1-paragraph teaser
     + cross-reference to A.6.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SRC = ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.1.html"
DST = ROOT / "appendices/appendix-a-mathematical-foundations/section-a.6.html"
APP_INDEX = ROOT / "appendices/appendix-a-mathematical-foundations/index.html"

TEASER = '''<h2>4.1.2 Information Theory: The Language of Learning</h2>
<p>Modern language modeling rests on four information-theoretic quantities:
<strong>entropy</strong> (the inherent uncertainty of a distribution),
<strong>cross-entropy</strong> (what we minimize during training),
<strong>perplexity</strong> (the human-readable scorecard derived from
cross-entropy), and <strong>KL divergence</strong> (the gap between two
distributions, used in distillation and alignment). For a self-contained
walk through definitions, formulas, and worked examples, see
<a class="cross-ref" href="../../appendices/appendix-a-mathematical-foundations/section-a.6.html">Appendix A.6 - Information Theory for Language Models</a>.
The transformer architecture in the next subsection assumes you understand
these terms or have skimmed the appendix.</p>
'''


def main() -> int:
    text = SRC.read_text(encoding="utf-8", errors="replace")
    # Extract 4.1.2 block
    m = re.search(
        r'(<h2[^>]*>\s*4\.1\.2\b[^<]*</h2>.*?)(?=<h2[^>]*>\s*4\.1\.3\b)',
        text, re.DOTALL,
    )
    if not m:
        print("[skip] 4.1.2 block not found in section-4.1.html (already moved?)")
        return 0
    primer_html = m.group(1)
    print(f"  Extracted 4.1.2 primer: {len(primer_html)} chars")

    # Build Appendix A.6 file
    a6_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Section A.6: Information Theory for Language Models. A self-contained primer on entropy, cross-entropy, perplexity, KL divergence, and mutual information.">
    <title>Section A.6: Information Theory for Language Models</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="../index.html">Appendices</a> / <a href="index.html">Appendix A</a></div>
    <h1>Information Theory for Language Models</h1>
</header>

<main class="content">
<aside class="callout note">
<div class="callout-title">A primer, not a course</div>
<p>This appendix gives a self-contained working introduction to the four
information-theoretic quantities that recur throughout the book: entropy,
cross-entropy, perplexity, and KL divergence. It originated as a section
of Chapter 4 (Transformer Architecture) but was moved here so the
transformer chapter can stay focused on transformer mechanics. Read this
appendix once and refer back as needed.</p>
</aside>

{primer_html}

</main>
</body>
</html>
'''
    DST.write_text(a6_html, encoding="utf-8")
    print(f"  Wrote {DST.relative_to(ROOT).as_posix()}")

    # Replace 4.1.2 block in section-4.1.html with teaser
    new_text = text[:m.start()] + TEASER + text[m.end():]
    SRC.write_text(new_text, encoding="utf-8")
    print(f"  Replaced 4.1.2 primer in section-4.1.html with teaser")

    # Update Appendix A index to include card for A.6
    if APP_INDEX.exists():
        idx_text = APP_INDEX.read_text(encoding="utf-8", errors="replace")
        if "section-a.6.html" not in idx_text:
            new_card = '''
            <a href="section-a.6.html" class="section-card">
                <span class="section-num">A.6</span>
                <span class="section-title">Information Theory for Language Models</span>
                <span class="section-desc">Entropy, cross-entropy, perplexity, KL divergence. The four information-theoretic quantities that anchor language modeling.</span>
            </a>
'''
            # Insert before closing </main> or after last section-card
            idx_text = idx_text.replace("</main>",
                f"<div class='section-grid'>{new_card}</div>\n</main>", 1)
            APP_INDEX.write_text(idx_text, encoding="utf-8")
            print(f"  Added A.6 card to {APP_INDEX.relative_to(ROOT).as_posix()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
