"""v3.6 R4: Add <figcaption> to <figure class="illustration"> tags on
appendix index pages (17 missing per audit).

Uses the existing alt text as caption fallback (truncated to first
sentence or 100 chars).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

n_added_total = 0


def add_caption(match: re.Match) -> str:
    global n_added_total
    block = match.group(0)
    if "<figcaption" in block:
        return block
    alt_m = re.search(r'alt="([^"]+)"', block)
    if not alt_m:
        return block
    alt_text = alt_m.group(1).strip()
    first_sentence = alt_text.split(".")[0].strip()
    if len(first_sentence) > 100:
        first_sentence = first_sentence[:100] + "..."
    if not first_sentence:
        return block
    cap = f'<figcaption>{first_sentence}.</figcaption>'
    n_added_total += 1
    return block.replace("</figure>", cap + "</figure>")


def main() -> int:
    for p in (ROOT / "appendices").glob("*/index.html"):
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        text = re.sub(
            r'<figure[^>]*class="illustration"[^>]*>.*?</figure>',
            add_caption,
            text,
            flags=re.DOTALL,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
    print(f"Added {n_added_total} figcaptions to appendix index pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
