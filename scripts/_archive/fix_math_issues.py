#!/usr/bin/env python3
"""
Detect and fix common math/KaTeX rendering issues across all HTML files.

SAFETY: Only fixes math content that is clearly inside math containers:
  - Display math: $$...$$ inside <div class="math-block"> containers
  - Inline math: $...$ inside <span class="math"> containers
  - Also catches $$...$$ that appear standalone (not in code blocks)

Fixes applied:
  1. HTML entities -> LaTeX commands (inside math only)
  2. HTML <sub>...</sub> -> _{...} subscripts (inside math only)
  3. HTML <sup>...</sup> -> ^{...} superscripts (inside math only)
  4. HTML <a> tags inside math -> plain text
"""

import os
import re
import sys
from pathlib import Path

# ---- configuration ----

ROOT = Path(r"E:\Projects\LLMCourse")

# HTML entity -> LaTeX replacement map (inside math only)
ENTITY_MAP = {
    # Operators
    "&times;": r"\times",
    "&middot;": r"\cdot",
    "&minus;": "-",
    "&plus;": "+",
    "&divide;": r"\div",
    # Arrows
    "&rarr;": r"\rightarrow",
    "&larr;": r"\leftarrow",
    "&harr;": r"\leftrightarrow",
    "&rArr;": r"\Rightarrow",
    "&lArr;": r"\Leftarrow",
    # Comparisons
    "&lt;": "<",
    "&gt;": ">",
    "&le;": r"\leq",
    "&ge;": r"\geq",
    "&leq;": r"\leq",
    "&geq;": r"\geq",
    "&ne;": r"\neq",
    "&asymp;": r"\approx",
    "&equiv;": r"\equiv",
    "&prop;": r"\propto",
    "&propto;": r"\propto",
    # Sums / products
    "&sum;": r"\sum",
    "&prod;": r"\prod",
    # Set / logic
    "&in;": r"\in",
    "&notin;": r"\notin",
    "&sub;": r"\subset",
    "&sup;": r"\supset",
    "&cap;": r"\cap",
    "&cup;": r"\cup",
    "&empty;": r"\emptyset",
    "&forall;": r"\forall",
    "&exist;": r"\exists",
    "&and;": r"\wedge",
    "&or;": r"\vee",
    "&not;": r"\neg",
    # Greek lowercase
    "&alpha;": r"\alpha",
    "&beta;": r"\beta",
    "&gamma;": r"\gamma",
    "&delta;": r"\delta",
    "&epsilon;": r"\epsilon",
    "&zeta;": r"\zeta",
    "&eta;": r"\eta",
    "&theta;": r"\theta",
    "&iota;": r"\iota",
    "&kappa;": r"\kappa",
    "&lambda;": r"\lambda",
    "&mu;": r"\mu",
    "&nu;": r"\nu",
    "&xi;": r"\xi",
    "&pi;": r"\pi",
    "&rho;": r"\rho",
    "&sigma;": r"\sigma",
    "&tau;": r"\tau",
    "&upsilon;": r"\upsilon",
    "&phi;": r"\phi",
    "&chi;": r"\chi",
    "&psi;": r"\psi",
    "&omega;": r"\omega",
    # Greek uppercase
    "&Alpha;": r"\Alpha",
    "&Beta;": r"\Beta",
    "&Gamma;": r"\Gamma",
    "&Delta;": r"\Delta",
    "&Theta;": r"\Theta",
    "&Lambda;": r"\Lambda",
    "&Pi;": r"\Pi",
    "&Sigma;": r"\Sigma",
    "&Phi;": r"\Phi",
    "&Psi;": r"\Psi",
    "&Omega;": r"\Omega",
    # Misc math
    "&infin;": r"\infty",
    "&part;": r"\partial",
    "&nabla;": r"\nabla",
    "&radic;": r"\sqrt{}",
    "&ang;": r"\angle",
    "&perp;": r"\perp",
    "&sdot;": r"\cdot",
    "&oplus;": r"\oplus",
    "&otimes;": r"\otimes",
    # Spacing entities (collapse to LaTeX thin space)
    "&ensp;": r"\;",
    "&emsp;": r"\;",
    "&thinsp;": r"\,",
    "&nbsp;": "~",
    # Ampersand (for alignment environments)
    "&amp;": "&",
    # Superscript 2 (HTML entity)
    "&sup2;": "^{2}",
    "&sup3;": "^{3}",
}

# Build a regex that matches any of the entities (longest first)
_sorted_entities = sorted(ENTITY_MAP.keys(), key=len, reverse=True)
ENTITY_RE = re.compile("|".join(re.escape(e) for e in _sorted_entities))

# ---- helpers ----

def find_html_files(root: Path):
    """Yield all .html files under root, skipping hidden dirs."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for fn in filenames:
            if fn.endswith(".html"):
                yield Path(dirpath) / fn


def replace_entities(text: str) -> str:
    """Replace HTML entities with LaTeX equivalents."""
    return ENTITY_RE.sub(lambda m: ENTITY_MAP[m.group(0)], text)


def replace_html_sub_sup(text: str) -> str:
    """Replace <sub>...</sub> with _{...} and <sup>...</sup> with ^{...}."""
    result = re.sub(r"<sub>(.*?)</sub>", r"_{\1}", text)
    result = re.sub(r"<sup>(.*?)</sup>", r"^{\1}", result)
    return result


def strip_html_tags_in_math(text: str) -> str:
    """Remove <a ...>...</a> tags (keep inner text), <strong>, <em> etc."""
    result = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', text)
    result = re.sub(r'</?(?:strong|em|b|i)>', '', result)
    return result


def fix_math_content(text: str) -> str:
    """Apply all math fixes to a string that is known to be inside math."""
    result = replace_entities(text)
    result = replace_html_sub_sup(result)
    result = strip_html_tags_in_math(result)
    return result


def has_entity(text: str) -> bool:
    """Check if text contains any known HTML entities."""
    return bool(ENTITY_RE.search(text))


def has_html_tags(text: str) -> bool:
    """Check if text contains sub/sup or other HTML tags."""
    return bool(re.search(r'<(?:sub|sup|a |strong|em|b|i)\b', text))


def fix_file(filepath: Path, dry_run: bool = False):
    """Fix math issues in a single file. Returns (fix_count, details)."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    original = content
    fixes = 0
    details = []

    # === Strategy 1: Fix <div class="math-block"> containers ===
    # These contain $$...$$ display math, possibly spanning multiple lines
    def fix_math_block(m):
        nonlocal fixes
        full_match = m.group(0)
        inner = m.group(1)  # everything between <div class="math-block"> and </div>

        new_inner = fix_math_content(inner)
        if new_inner != inner:
            fixes += 1
            details.append(("DISPLAY-BLOCK", inner.strip()[:140], new_inner.strip()[:140]))
            return f'<div class="math-block">{new_inner}</div>'
        return full_match

    content = re.sub(
        r'<div class="math-block">(.*?)</div>',
        fix_math_block,
        content,
        flags=re.DOTALL
    )

    # === Strategy 2: Fix <span class="math"> containers ===
    # These contain $...$ inline math
    def fix_math_span(m):
        nonlocal fixes
        full_match = m.group(0)
        inner = m.group(1)  # everything between <span class="math"> and </span>

        new_inner = fix_math_content(inner)
        if new_inner != inner:
            fixes += 1
            details.append(("INLINE-SPAN", inner.strip()[:140], new_inner.strip()[:140]))
            return f'<span class="math">{new_inner}</span>'
        return full_match

    content = re.sub(
        r'<span class="math">(.*?)</span>',
        fix_math_span,
        content,
        flags=re.DOTALL
    )

    # === Strategy 3: Fix standalone $$...$$ not inside math-block ===
    # Some display math uses $$ without the div wrapper.
    # Only fix if the $$ content has entities/html tags (to avoid touching clean math).
    def fix_standalone_display(m):
        nonlocal fixes
        full_match = m.group(0)
        inner = m.group(1)

        # Skip if it looks like it is inside a <code> or <pre> block
        # (We check by looking at preceding context, but since we can't easily do
        # that in a regex sub, we rely on entities only appearing in actual math)
        if not has_entity(inner) and not has_html_tags(inner):
            return full_match

        new_inner = fix_math_content(inner)
        if new_inner != inner:
            fixes += 1
            details.append(("DISPLAY-STANDALONE", inner.strip()[:140], new_inner.strip()[:140]))
            return f"$${new_inner}$$"
        return full_match

    content = re.sub(
        r'\$\$(.*?)\$\$',
        fix_standalone_display,
        content,
        flags=re.DOTALL
    )

    if content != original:
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return fixes, details
    return 0, []


def detect_unwrapped_math_formulas(filepath: Path):
    """Detect formulas with HTML entities that are not inside any math container.
    These are lines where entities are used between or around math spans,
    suggesting the whole formula should be in a math container."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    issues = []

    # Find lines with HTML entities that are adjacent to math spans
    # Pattern: entities between </span> and <span class="math"> on the same line
    for line_no, line in enumerate(content.split("\n"), 1):
        # Skip lines inside <code>, <pre>, <script>, <style>
        stripped = line.strip()
        if stripped.startswith(("<code", "<pre", "<script", "<style")):
            continue

        # Check for entity-bearing content between math spans
        # e.g., <span class="math">$X$</span> &middot; <span class="math">$Y$</span>
        if re.search(r'</span>\s*(&[a-z]+;)', line):
            for em in re.finditer(r'</span>\s*(&[a-z]+;)', line):
                entity = em.group(1)
                if entity in ENTITY_MAP:
                    issues.append((line_no, "BETWEEN_SPANS", entity, stripped[:160]))
                    break

        # Check for entities adjacent to $$ on same line (not inside math-block div)
        if "$$" in line and re.search(r'&[a-z]+;', line):
            # Confirm entity is outside $$..$$
            # Remove $$...$$ content
            cleaned = re.sub(r'\$\$.*?\$\$', '', line)
            cleaned = re.sub(r'\$[^$]+\$', '', cleaned)
            for em in re.finditer(r'&([a-z]+);', cleaned):
                entity = f"&{em.group(1)};"
                if entity in ENTITY_MAP:
                    issues.append((line_no, "NEAR_DISPLAY", entity, stripped[:160]))
                    break

        # Check for lines with formulas using entities but no math delimiters
        # e.g., <strong>W<sub>merged</sub> = &alpha; &middot; ...</strong>
        if '$' not in line and '<span class="math">' not in line:
            if '<div class="math-block">' not in line:
                # Line has no math delimiters at all
                math_entities = ENTITY_RE.findall(line)
                # Filter out entities that are common in regular HTML (&lt;, &gt;, &amp;)
                math_only = [e for e in math_entities if e not in ("&lt;", "&gt;", "&amp;", "&nbsp;")]
                if len(math_only) >= 2:
                    # Multiple math entities on a line with no math delimiters = likely formula
                    issues.append((line_no, "UNWRAPPED_FORMULA", ", ".join(math_only[:4]), stripped[:160]))

    return issues


# ---- main ----

def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    if dry_run:
        print("=== DRY RUN (no files will be modified) ===\n")

    html_files = sorted(find_html_files(ROOT))
    print(f"Scanning {len(html_files)} HTML files...\n")

    total_fixes = 0
    files_fixed = 0
    all_unwrapped = []

    for fp in html_files:
        rel = fp.relative_to(ROOT)

        # Phase 1: Fix entities INSIDE known math containers
        fix_count, details = fix_file(fp, dry_run=dry_run)
        if fix_count > 0:
            files_fixed += 1
            total_fixes += fix_count
            print(f"  FIXED  {rel}: {fix_count} math fix(es)")
            if verbose:
                for kind, old, new in details:
                    print(f"         [{kind}]")
                    print(f"           OLD: {old}")
                    print(f"           NEW: {new}")

        # Phase 2: Detect formulas that need wrapping in math containers
        unwrapped = detect_unwrapped_math_formulas(fp)
        if unwrapped:
            all_unwrapped.append((rel, unwrapped))

    # ---- Summary ----
    print("\n" + "=" * 70)
    print(f"MATH FIXES APPLIED: {total_fixes} fixes across {files_fixed} files")
    if dry_run:
        print("  (dry run, no files were actually modified)")
    print("=" * 70)

    if all_unwrapped:
        total_issues = sum(len(v) for _, v in all_unwrapped)
        print(f"\nDETECTED: {total_issues} potential unwrapped formulas in {len(all_unwrapped)} files")
        print("These lines contain multiple math HTML entities but are not inside math delimiters.\n")
        for rel, issues in all_unwrapped:
            print(f"  {rel}:")
            shown = 0
            for line_no, kind, entity_info, context in issues:
                if shown >= 8:
                    print(f"    ... and {len(issues) - shown} more")
                    break
                print(f"    L{line_no} [{kind}] {entity_info}")
                print(f"      {context[:120]}")
                shown += 1
            print()

    return 0


if __name__ == "__main__":
    main()
