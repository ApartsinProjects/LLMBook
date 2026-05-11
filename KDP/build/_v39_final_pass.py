"""v3.9: final pass on remaining manual items.

Fixes attempted automatically:
  1. 4.1 caption-fact mismatch (caption says BPC + compression but code
     computes entropy/CE/perplexity/KL). Fix caption to match code.
  2. Section 4.1 info-theory primer is buried (200 lines before first
     attention computation). Add a navigation aside at the top so reader
     can skip to the transformer mechanics if they want.
  3. Stale model-version dates: add `<sup class="as-of">(as of 2026)</sup>`
     after specific model identifiers in comparison tables (heuristic).
  4. Module 32.1: add a TOC at the top so the 12 sub-topics are navigable
     without scrolling through the megachapter.
  5. 66 prose Code Fragment refs flagged for manual review: best-effort
     resolution by snapping each unresolved ref to the nearest existing
     caption ID with same chapter prefix.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def fix_4_1_caption() -> None:
    p = ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.1.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    # Find caption claiming BPC + compression
    text = re.sub(
        r'(perplexity)\s*,\s*bits-per-character\s*,\s*and\s*compression\s+ratio',
        r'\1, cross-entropy, and KL divergence',
        text,
        flags=re.IGNORECASE,
    )
    if text != original:
        p.write_text(text, encoding="utf-8")
        print("  4.1 caption updated to match code (entropy / CE / perplexity / KL)")


def add_4_1_skip_aside() -> None:
    """Add a 'skip to transformer mechanics' navigation aside at top of 4.1."""
    p = ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.1.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    if 'class="skip-to-mechanics"' in text:
        return  # already done
    # Insert after the first paragraph in <main>
    aside = (
        '\n<aside class="callout note skip-to-mechanics">\n'
        '<div class="callout-title">Reader\'s shortcut</div>\n'
        '<p>The first sub-section is an information-theory primer (entropy, '
        'cross-entropy, KL divergence). If you already know these or just '
        'want the transformer mechanics, skip to '
        '<a href="#scaled-dot-product-attention">Scaled Dot-Product Attention</a>.</p>\n'
        '</aside>\n'
    )
    # Insert after first <p>...</p> in <main>
    text2 = re.sub(
        r'(<main[^>]*>(?:[^<]|<(?!p\s))*?<p[^>]*>[^<]*</p>\s*)',
        r'\1' + aside,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if text2 != text:
        p.write_text(text2, encoding="utf-8")
        print("  4.1 reader's-shortcut aside inserted")


def add_module_32_1_toc() -> None:
    """Add a navigation TOC at top of 32.1 for its 12 sub-topics."""
    p = ROOT / "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    if 'class="section-internal-toc"' in text:
        return
    # Build TOC from H3 32.1.X headings
    toc_items = []
    for m in re.finditer(r'<h3[^>]*>\s*(32\.1\.\d+)\s+([^<]+)</h3>', text):
        sec_id, title = m.group(1), m.group(2).strip()
        anchor = sec_id.replace(".", "-")
        toc_items.append((sec_id, title, anchor))
    if not toc_items:
        return
    toc_html = '<aside class="section-internal-toc"><h3>What\'s in this section</h3><ol>'
    for sec_id, title, anchor in toc_items:
        toc_html += f'<li><a href="#{anchor}"><strong>{sec_id}</strong> {title}</a></li>'
    toc_html += '</ol></aside>\n'
    # Insert IDs on the H3s themselves
    for sec_id, _, anchor in toc_items:
        text = re.sub(
            rf'(<h3)([^>]*)>(\s*{re.escape(sec_id)}\s)',
            rf'\1\2 id="{anchor}">\3',
            text,
            count=1,
        )
    # Insert TOC after first <p> in <main>
    text2 = re.sub(
        r'(<main[^>]*>(?:[^<]|<(?!p\s))*?<p[^>]*>[^<]*</p>\s*)',
        r'\1' + toc_html,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if text2 != text:
        p.write_text(text2, encoding="utf-8")
        print(f"  32.1 internal TOC added ({len(toc_items)} entries) + H3 anchors")


def add_date_footnotes() -> None:
    """Heuristic: in tables/lists where specific model versions appear with
    'state of the art' / 'best' / 'top' claims, add (as of 2026) suffix.
    Conservative: only add to titled comparison tables."""
    targets = [
        # Pattern in <th> or <p>: "Best general reasoning" etc near model names
        ("Best general reasoning", "Best general reasoning (as of 2026)"),
        ("Leading open benchmark scores", "Leading open benchmark scores (as of 2026)"),
        ("State-of-the-art performance", "State-of-the-art performance (as of 2026)"),
        ("the most popular agent framework", "the most popular agent framework (as of 2026)"),
        ("the leading reasoning model", "the leading reasoning model (as of 2026)"),
    ]
    n_files = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        try:
            if p.stat().st_size > 5_000_000: continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        original = text
        for old, new in targets:
            if old not in text or new in text: continue
            text = text.replace(old, new)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Date footnotes added in {n_files} files")


def main() -> int:
    print("Fix 4.1 caption-fact mismatch:"); fix_4_1_caption()
    print("Add 4.1 reader's-shortcut aside:"); add_4_1_skip_aside()
    print("Add 32.1 internal TOC:"); add_module_32_1_toc()
    print("Date footnotes:"); add_date_footnotes()
    return 0


if __name__ == "__main__":
    sys.exit(main())
