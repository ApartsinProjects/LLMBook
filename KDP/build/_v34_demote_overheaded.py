"""v3.4 #2: Light-touch H2/H3 cap on the worst over-headed chapters.

32.1 (LLM Security Threats): demote 32.1.1..32.1.12 from <h2> to <h3>.
     Keeps content navigable in TOC but removes 12 noisy H2 entries.

27.7.7 (Applications): demote the 21 H3s under it to bold paragraphs
     `<p class="subsection-heading"><strong>...</strong></p>`. They're
     brief application paragraphs (60-100 words each) that don't earn
     a TOC entry.

Both are reversible if we change our mind later (find/replace).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def demote_32_1() -> int:
    """Demote 32.1.1 .. 32.1.12 H2s to H3."""
    p = ROOT / "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    n = 0
    # Match <h2 ...>32.1.X ... </h2> -> <h3>...</h3>
    def _sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        attrs = m.group(1)
        body = m.group(2)
        return f"<h3{attrs}>{body}</h3>"

    new_text = re.sub(
        r'<h2(\s[^>]*)?>(\s*32\.1\.\d+\b.*?)</h2>',
        _sub,
        text,
        flags=re.DOTALL,
    )
    if new_text != text:
        p.write_text(new_text, encoding="utf-8")
    print(f"  32.1: demoted {n} H2 -> H3")
    return n


def demote_27_7_7() -> int:
    """Demote H3s inside 27.7.7 'Applications' to bold paragraphs."""
    p = ROOT / "part-7-multimodal-applications/module-27-multimodal/section-27.7.html"
    text = p.read_text(encoding="utf-8", errors="replace")
    # Find the 27.7.7 H2 block: from <h2>27.7.7 ... up to next <h2>
    h2_match = re.search(
        r'(<h2[^>]*>\s*27\.7\.7\b[^<]*</h2>)(.*?)(?=<h2[^>]*>)',
        text,
        flags=re.DOTALL,
    )
    if not h2_match:
        print("  27.7.7: H2 block not found")
        return 0
    h2_tag = h2_match.group(1)
    block = h2_match.group(2)
    # Demote H3 tags inside this block
    n = 0

    def _sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        body = m.group(1)
        # Wrap in subsection-heading paragraph for visual distinction
        return f'<p class="subsection-heading"><strong>{body}</strong></p>'

    new_block = re.sub(
        r'<h3(?:\s[^>]*)?>(.*?)</h3>',
        _sub,
        block,
        flags=re.DOTALL,
    )
    if new_block != block:
        new_text = text[:h2_match.start()] + h2_tag + new_block + text[h2_match.end():]
        p.write_text(new_text, encoding="utf-8")
    print(f"  27.7.7: demoted {n} H3 -> bold paragraphs")
    return n


def main() -> int:
    demote_32_1()
    demote_27_7_7()
    return 0


if __name__ == "__main__":
    sys.exit(main())
