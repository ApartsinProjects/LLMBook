"""v3.9: Clean up the 66 prose Code Fragment refs that R5 P3 couldn't
auto-resolve.

These are mentions like "(Code Fragment 17.2.5)" inside prose where no
caption with that ID exists. Strategy: strip the parenthetical entirely
since the reader can't navigate to a non-existent target. This is less
embarrassing than leaving a broken pointer.

Detect: any "Code Fragment X.Y.Z" or "Figure X.Y.Z" mention in prose
(not inside a caption) where no caption with that ID exists in the same
file. Strip the parenthetical surrounding it.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

PROSE_REF = re.compile(
    r'\s*[\(\[]?(Code Fragment|Figure)\s+(\d+\.\d+\.\d+)\b[\)\]]?'
)
CAPTION = re.compile(
    r'<div class="(?:code|figure|diagram)-caption"[^>]*>\s*'
    r'<strong>\s*(Code Fragment|Figure)\s+(\d+\.\d+\.\d+):?\s*</strong>'
)


def main() -> int:
    n_files = 0
    n_stripped = 0
    for p in ROOT.glob("part-*/module-*/section-*.html"):
        try:
            if p.stat().st_size > 5_000_000: continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        captions = set()
        for m in CAPTION.finditer(text):
            captions.add((m.group(1), m.group(2)))
        if not captions: continue

        original = text
        local_strips = 0
        # Iterate from end so positional offsets are stable
        for m in list(PROSE_REF.finditer(text))[::-1]:
            kind, ref_id = m.group(1), m.group(2)
            if (kind, ref_id) in captions:
                continue
            # Check if mention is inside a caption (skip)
            preceding = text[max(0, m.start()-60):m.start()]
            if 'class="code-caption"' in preceding[-50:] or \
               'class="figure-caption"' in preceding[-50:] or \
               'class="diagram-caption"' in preceding[-50:]:
                continue
            # Strip - replace with empty (the leading whitespace/punct is part of match)
            text = text[:m.start()] + text[m.end():]
            local_strips += 1

        if local_strips > 0 and text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_stripped += local_strips

    print(f"Stripped {n_stripped} orphan Code Fragment / Figure refs across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
