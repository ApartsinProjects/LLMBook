"""Detect unescaped < and > inside HTML attribute values (a subtle bug class
that browsers silently auto-correct but XHTML/EPUB parsers reject).

Pattern: <tag attr="...> ... " ...> where the value contains a bare '>'
or '<' (not as part of a child tag). The parser usually treats the first
'>' as end-of-opening-tag, truncating the attribute value silently.
"""

from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTION_GLOBS = [
    "part-*/module-*/section-*.html",
    "appendices/appendix-*/section-*.html",
    "front-matter/*.html",
]


def find_files() -> list[Path]:
    out: list[Path] = []
    for g in SECTION_GLOBS:
        out.extend(sorted(ROOT.glob(g)))
    return out


def scan(text: str) -> list[tuple[int, str]]:
    """Find attribute values with unescaped > inside them."""
    bad: list[tuple[int, str]] = []
    # Match any attribute name="value with > inside" up to next quote
    for m in re.finditer(r'(\w+)\s*=\s*"([^"]*[<>][^"]*)"', text):
        attr, val = m.group(1), m.group(2)
        # Allow CSS in style attributes (they don't usually have < or >)
        # but DO catch real problems
        if "<" in val or ">" in val:
            # Skip benign cases: arrow text in title/aria-label etc.
            # Real issue: a > or < that's not part of an HTML entity.
            # Allow text-arrow like → ← (those are unicode chars, not <).
            line = text.count("\n", 0, m.start()) + 1
            bad.append((line, f'{attr}="{val[:140]}"'))
    return bad


def main() -> None:
    files = find_files()
    findings: dict[str, list] = {}
    total = 0
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        bad = scan(text)
        if bad:
            rel = p.relative_to(ROOT).as_posix()
            findings[rel] = bad
            total += len(bad)
    out = Path(__file__).resolve().parent / "_html_entity_bugs.json"
    out.write_text(json.dumps(findings, indent=2), encoding="utf-8")
    print(f"Total unescaped <,> in attr values: {total} across {len(findings)} files")
    for rel, items in list(findings.items())[:10]:
        print(f"  {rel}: {len(items)} (first: line {items[0][0]} -> {items[0][1][:100]})")


if __name__ == "__main__":
    main()
