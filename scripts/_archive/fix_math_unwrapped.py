#!/usr/bin/env python3
"""
Phase 2: Fix partially-wrapped math formulas.

These are formulas where some parts are in <span class="math"> but operators
and Greek letters between the spans use HTML entities. The whole formula
should be a single math expression.

Common patterns:
  - <span class="math">$X$</span> &middot; <span class="math">$Y$</span>
  - &alpha; &middot; <span class="math">$W_{A}$</span> + (1 - &alpha;) &middot; <span class="math">$W_{B}$</span>

This script detects and reports these for review but can also apply safe fixes.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")

# Entity -> LaTeX map (same as fix_math_issues.py)
ENTITY_MAP = {
    "&times;": r"\times", "&middot;": r"\cdot", "&minus;": "-",
    "&plus;": "+", "&divide;": r"\div",
    "&rarr;": r"\rightarrow", "&larr;": r"\leftarrow",
    "&rArr;": r"\Rightarrow", "&lArr;": r"\Leftarrow",
    "&lt;": "<", "&gt;": ">",
    "&le;": r"\leq", "&ge;": r"\geq", "&ne;": r"\neq",
    "&asymp;": r"\approx", "&equiv;": r"\equiv",
    "&prop;": r"\propto", "&propto;": r"\propto",
    "&sum;": r"\sum", "&prod;": r"\prod",
    "&in;": r"\in", "&notin;": r"\notin",
    "&alpha;": r"\alpha", "&beta;": r"\beta", "&gamma;": r"\gamma",
    "&delta;": r"\delta", "&epsilon;": r"\epsilon", "&theta;": r"\theta",
    "&lambda;": r"\lambda", "&mu;": r"\mu", "&pi;": r"\pi",
    "&sigma;": r"\sigma", "&tau;": r"\tau", "&phi;": r"\phi",
    "&omega;": r"\omega",
    "&Gamma;": r"\Gamma", "&Delta;": r"\Delta", "&Theta;": r"\Theta",
    "&Lambda;": r"\Lambda", "&Sigma;": r"\Sigma", "&Phi;": r"\Phi",
    "&Omega;": r"\Omega",
    "&infin;": r"\infty", "&part;": r"\partial",
    "&sup2;": "^{2}", "&sup3;": "^{3}",
    "&nbsp;": "~",
}

_sorted = sorted(ENTITY_MAP.keys(), key=len, reverse=True)
ENTITY_RE = re.compile("|".join(re.escape(e) for e in _sorted))


def find_html_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for fn in filenames:
            if fn.endswith(".html"):
                yield Path(dirpath) / fn


def entity_to_latex(text):
    return ENTITY_RE.sub(lambda m: ENTITY_MAP[m.group(0)], text)


def html_to_latex(text):
    """Convert HTML math fragment to LaTeX."""
    result = text
    # Strip <span class="math">$...$</span> -> inner math content (without $)
    result = re.sub(r'<span class="math">\$([^$]*)\$</span>', r'\1', result)
    result = re.sub(r'<span class="math">([^<]*)</span>', r'\1', result)
    # Convert sub/sup
    result = re.sub(r'<sub>(.*?)</sub>', r'_{\1}', result)
    result = re.sub(r'<sup>(.*?)</sup>', r'^{\1}', result)
    # Strip remaining HTML tags (strong, em, a, etc.)
    result = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', result)
    result = re.sub(r'</?(?:strong|em|b|i)>', '', result)
    # Convert entities
    result = entity_to_latex(result)
    return result


def process_file(filepath, dry_run=False, verbose=False):
    content = filepath.read_text(encoding="utf-8", errors="replace")
    original = content
    fixes = 0
    rel = filepath.relative_to(ROOT)

    # Pattern 1: <p> or similar containing a centered formula with mixed spans+entities
    # e.g., <p style="text-align: center..."><strong>W<sub>merged</sub> = &alpha; &middot; <span class="math">$W_{A}$</span>...</strong></p>
    def fix_centered_formula(m):
        nonlocal fixes
        full = m.group(0)
        attrs = m.group(1)
        inner = m.group(2)

        # Must contain at least one math span AND at least one entity
        if '<span class="math">' not in inner:
            return full
        if not ENTITY_RE.search(inner):
            return full

        # Convert inner to pure LaTeX
        latex = html_to_latex(inner).strip()

        # Build replacement: a proper math-block div
        new = f'<div class="math-block">\n$${latex}$$\n</div>'

        if verbose:
            print(f"  {rel}: centered formula fix")
            print(f"    OLD: {inner.strip()[:120]}")
            print(f"    NEW: $${latex[:120]}$$")
        fixes += 1
        return new

    content = re.sub(
        r'<p\s+(style="text-align:\s*center[^"]*"[^>]*)>\s*(.*?)\s*</p>',
        fix_centered_formula,
        content,
        flags=re.DOTALL
    )

    # Pattern 2: Lines inside <div class="math-block"> that don't have $$ but have entities
    # (these are already caught by fix_math_issues.py, skip)

    # Pattern 3: <li> or <p> with "X = <span class="math">$Y$</span> &middot; <span class="math">$Z$</span>"
    # These are inline formulas where entities connect math spans
    # Fix by wrapping the whole expression in a single math span
    def fix_inline_mixed(m):
        nonlocal fixes
        full = m.group(0)
        prefix_tag = m.group(1)  # e.g., <strong> or empty
        inner = m.group(2)       # the formula part
        suffix_tag = m.group(3)  # e.g., </strong> or empty

        # Must have both math spans and entities
        if '<span class="math">' not in inner:
            return full
        if not ENTITY_RE.search(inner):
            return full
        # Skip if this is inside a <td> (table cells often have entities for display)
        # We handle those separately
        return full  # Skip for safety; these are harder to auto-fix

    if content != original:
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return fixes
    return 0


def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    if dry_run:
        print("=== DRY RUN ===\n")

    html_files = sorted(find_html_files(ROOT))
    print(f"Scanning {len(html_files)} HTML files for unwrapped formulas...\n")

    total = 0
    for fp in html_files:
        n = process_file(fp, dry_run=dry_run, verbose=verbose)
        total += n

    print(f"\nFixed {total} unwrapped formulas.")
    if dry_run:
        print("(dry run, no files modified)")


if __name__ == "__main__":
    main()
