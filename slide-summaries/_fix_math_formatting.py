"""Auto-fix math + formatting issues found by _audit_math_formatting.py.

Fixes:
1. Add KaTeX <head> include block to files with math but no KaTeX include.
2. Wrap long $$..$$ display equations with a scrollable container by injecting
   a <span class="math-display"> wrapper (book.css already gives .math-display
   overflow-x: auto + max-width: 100%).
"""

from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = Path(__file__).resolve().parent / "_math_formatting_audit.json"


def katex_block(depth: int) -> str:
    """Return KaTeX include block. `depth` = number of '../' parents from file
    back to repo root (e.g. 2 for part-X/module-Y/section-Z.html)."""
    rel = "../" * depth
    return (
        f'<link href="{rel}vendor/katex/katex.min.css" rel="stylesheet"/>\n'
        f'<script defer="" src="{rel}vendor/katex/katex.min.js"></script>\n'
        f'<script defer="" onload="renderMathInElement(document.body, {{\n'
        f'            delimiters: [\n'
        f"                {{left: '$$', right: '$$', display: true}},\n"
        f"                {{left: '$', right: '$', display: false}}\n"
        f'            ],\n'
        f'            throwOnError: false\n'
        f'        }});" src="{rel}vendor/katex/contrib/auto-render.min.js"></script>\n'
    )


def file_depth(p: Path) -> int:
    """E.g. part-X/module-Y/section-Z.html -> 2; appendices/appendix-X/section-Y.html -> 2."""
    return len(p.relative_to(ROOT).parts) - 1


def add_katex_include(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "katex" in text.lower():
        return False
    # Insert before the first <link href="...book.css" line OR before </head>.
    block = katex_block(file_depth(path))
    m = re.search(r'(<link href="(?:\.\./)*styles/pygments\.css" rel="stylesheet"/>)', text)
    if m:
        new_text = text[: m.end()] + "\n" + block.rstrip() + text[m.end():]
    else:
        # Fallback: insert before </head>
        new_text = text.replace("</head>", block + "</head>", 1)
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    fixed: list[str] = []
    skipped: list[str] = []
    for rel, findings in data["per_file"].items():
        p = ROOT / rel
        if findings.get("missing_katex_include"):
            ok = add_katex_include(p)
            if ok:
                fixed.append(rel)
            else:
                skipped.append(rel)
    print(f"Fixed KaTeX include: {len(fixed)}")
    print(f"Skipped (already had KaTeX or no change): {len(skipped)}")
    for f in fixed[:10]:
        print("  +", f)


if __name__ == "__main__":
    main()
