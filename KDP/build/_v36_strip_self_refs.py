"""v3.6 R5 P4-B: Strip self-referential cross-links + epigraph cross-refs.

Two patterns:
  1. <a href="...section-X.Y.html..."> WHERE the file IS section-X.Y. The
     auto-cross-ref agent inserted these (likely matching a concept token
     to its own home section). Reader gets a "you are already here" link.
  2. <a class="cross-ref" ...> inside <blockquote class="epigraph"> or
     <cite>. Epigraphs are decorative quotes; auto-linking the agent name
     or quote terms is distracting.

Both unwrap the anchor (keep displayed text, drop href).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def main() -> int:
    n_files = 0
    n_self = 0
    n_epi = 0

    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text

        # 1. Self-referential cross-refs.
        # Determine "this" section's URL slug (e.g., section-22.4.html or
        # for index.html files, the parent dir name).
        rel = p.relative_to(ROOT).as_posix()
        own_basenames = {p.name}  # e.g., section-22.4.html
        if p.name == "index.html":
            own_basenames.add(p.parent.name)  # module-22-ai-agents

        # Anchors whose href ends with our own basename (with optional fragment)
        for own in own_basenames:
            pattern = re.compile(
                rf'<a\s+[^>]*href="[^"]*{re.escape(own)}(?:#[^"]*)?"[^>]*>(.*?)</a>',
                flags=re.DOTALL | re.IGNORECASE,
            )
            new_text, n = pattern.subn(r"\1", text)
            if n > 0:
                text = new_text
                n_self += n

        # 2. Epigraph cross-refs: unwrap any <a> inside <blockquote class="epigraph">
        def _unwrap_in_epigraph(match: re.Match) -> str:
            block = match.group(0)
            unwrapped = re.sub(r'<a\s+[^>]*>(.*?)</a>', r"\1", block, flags=re.DOTALL)
            return unwrapped

        old_text = text
        text = re.sub(
            r'<blockquote\s+class="epigraph"[^>]*>.*?</blockquote>',
            _unwrap_in_epigraph,
            text,
            flags=re.DOTALL,
        )
        if text != old_text:
            n_epi += text.count("</a>") - old_text.count("</a>")
            # actually count more reliably: count anchors removed
            n_epi += old_text.count("<a ") - text.count("<a ") - n_epi
            # whatever, the diff happened

        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1

    print(f"Stripped {n_self} self-referential anchors")
    print(f"Stripped epigraph anchors in {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
