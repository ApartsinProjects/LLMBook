"""Fix unescaped HTML in attribute values found by _audit_html_entity_bugs.py.

Two patterns:
1. alt="<strong>Figure X.Y</strong>: text..." -> alt text should be plain.
   Browsers tolerate this; XHTML/EPUB rejects it. Strip <strong>...</strong>
   tags from inside alt= values.
2. Other bare > < in attribute values: escape to &gt; / &lt;
"""

from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = Path(__file__).resolve().parent / "_html_entity_bugs.json"


def strip_html_from_alt(text: str) -> tuple[str, int]:
    """Strip <strong>...</strong> and other simple inline tags from alt='...' values."""
    n = 0
    def fixer(m: re.Match) -> str:
        nonlocal n
        full = m.group(0)
        val = m.group(1)
        # Remove all tags from the alt value
        plain = re.sub(r"<[^>]+>", "", val)
        # Trim whitespace
        plain = re.sub(r"\s+", " ", plain).strip()
        if plain != val:
            n += 1
            return f'alt="{plain}"'
        return full
    new = re.sub(r'\balt="([^"]*<[^"]*)"', fixer, text)
    return new, n


def escape_bare_angle_brackets_in_attrs(text: str) -> tuple[str, int]:
    """For non-alt attributes that have bare > or <, escape them.
    Specifically: this targets known regression points (target=, span=).
    Conservative: only fix attributes named alt|aria-label|title|target|span."""
    n = 0
    def fix_attr(m: re.Match) -> str:
        nonlocal n
        attr, val = m.group(1), m.group(2)
        if "<" not in val and ">" not in val:
            return m.group(0)
        # If the value contains literal markup we cannot easily fix safely,
        # but the simple case: bare ascii > or < surrounded by text/digits.
        new_val = val.replace("<", "&lt;").replace(">", "&gt;")
        n += 1
        return f'{attr}="{new_val}"'

    # Limit to safe attributes
    pattern = r'\b(alt|aria-label|title|target|span)="([^"]*[<>][^"]*)"'
    new = re.sub(pattern, fix_attr, text)
    return new, n


def main() -> None:
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    fixed_files: list[tuple[str, int]] = []
    for rel in data.keys():
        p = ROOT / rel
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        # First: strip HTML from alt= values
        text, n1 = strip_html_from_alt(text)
        # Then: escape remaining bare angle brackets in safe attrs
        text, n2 = escape_bare_angle_brackets_in_attrs(text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            fixed_files.append((rel, n1 + n2))
    print(f"Fixed {len(fixed_files)} files:")
    for rel, n in fixed_files:
        print(f"  {rel}: {n} attribute(s)")


if __name__ == "__main__":
    main()
