"""
Fix mechanical math quality issues in HTML files.

Fixes:
1. TEXT_SHOULD_BE_OPERATOR: \text{log} -> \log, \text{softmax} -> \operatorname{softmax}, etc.
2. SUBSCRIPT_NO_BRACES: _word -> _{word} for multi-char subscripts
3. HTML_ENTITY_IN_BLOCK / HTML_ENTITY_IN_LATEX: Convert HTML entities inside math delimiters
4. LEGACY_STYLED_MATH: Convert inline-styled math paragraphs to math-block divs

Does NOT fix:
- HTML_TAG_IN_LATEX (mostly false positives)
- BRACE_MISMATCH (needs manual review)
"""

import re
from pathlib import Path
from collections import defaultdict

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {
    "_scripts_archive", "node_modules", ".claude", "scripts",
    "templates", "styles", "agents", "_lab_fragments", "vendor"
}

# Standard LaTeX operators (have built-in commands)
STANDARD_OPERATORS = {
    "log": r"\log",
    "exp": r"\exp",
    "max": r"\max",
    "min": r"\min",
    "cos": r"\cos",
    "sin": r"\sin",
    "tan": r"\tan",
    "det": r"\det",
    "dim": r"\dim",
    "sup": r"\sup",
    "inf": r"\inf",
    "lim": r"\lim",
    "ln": r"\ln",
    "lg": r"\lg",
    "sec": r"\sec",
    "csc": r"\csc",
    "cot": r"\cot",
    "gcd": r"\gcd",
    "deg": r"\deg",
    "hom": r"\hom",
    "ker": r"\ker",
    "Pr": r"\Pr",
}

# Non-standard operators (need \operatorname)
OPERATORNAME_WORDS = {
    "softmax", "sigmoid", "tanh", "argmax", "argmin",
    "ReLU", "relu", "GELU", "gelu", "swish",
    "trace", "diag", "sign", "abs", "rank",
    "Var", "Cov", "MSE", "CE", "KL",
    "concat", "flatten", "pool", "conv",
    "Attention", "FFN", "LayerNorm",
}

# HTML entity to LaTeX mapping
ENTITY_MAP = {
    "&lt;": "<",
    "&gt;": ">",
    "&amp;": r"\&",
    "&nbsp;": r"\;",
    "&times;": r"\times",
    "&minus;": "-",
    "&plusmn;": r"\pm",
    "&le;": r"\le",
    "&ge;": r"\ge",
    "&ne;": r"\ne",
    "&asymp;": r"\approx",
    "&sim;": r"\sim",
    "&equiv;": r"\equiv",
    "&infin;": r"\infty",
    "&sum;": r"\sum",
    "&prod;": r"\prod",
    "&int;": r"\int",
    "&part;": r"\partial",
    "&nabla;": r"\nabla",
    "&alpha;": r"\alpha",
    "&beta;": r"\beta",
    "&gamma;": r"\gamma",
    "&delta;": r"\delta",
    "&epsilon;": r"\epsilon",
    "&theta;": r"\theta",
    "&lambda;": r"\lambda",
    "&mu;": r"\mu",
    "&pi;": r"\pi",
    "&sigma;": r"\sigma",
    "&tau;": r"\tau",
    "&phi;": r"\phi",
    "&omega;": r"\omega",
    "&radic;": r"\sqrt{}",
    "&prop;": r"\propto",
    "&larr;": r"\leftarrow",
    "&rarr;": r"\rightarrow",
    "&harr;": r"\leftrightarrow",
    "&lArr;": r"\Leftarrow",
    "&rArr;": r"\Rightarrow",
    "&hArr;": r"\Leftrightarrow",
    "&sub;": r"\subset",
    "&sube;": r"\subseteq",
    "&isin;": r"\in",
    "&notin;": r"\notin",
    "&cap;": r"\cap",
    "&cup;": r"\cup",
    "&empty;": r"\emptyset",
    "&forall;": r"\forall",
    "&exist;": r"\exists",
    "&sdot;": r"\cdot",
    "&middot;": r"\cdot",
    "&hellip;": r"\ldots",
    "&prime;": "'",
    "&Prime;": "''",
    "&lfloor;": r"\lfloor",
    "&rfloor;": r"\rfloor",
    "&lceil;": r"\lceil",
    "&rceil;": r"\rceil",
    "&lang;": r"\langle",
    "&rang;": r"\rangle",
    "&ensp;": r"\enspace",
    "&emsp;": r"\quad",
    "&bull;": r"\bullet",
    "&Ropf;": r"\mathbb{R}",
    "&Copf;": r"\mathbb{C}",
    "&Zopf;": r"\mathbb{Z}",
    "&Nopf;": r"\mathbb{N}",
    "&Lscr;": r"\mathcal{L}",
    "&Hscr;": r"\mathcal{H}",
    "&Escr;": r"\mathcal{E}",
    "&Oscr;": r"\mathcal{O}",
}


def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)


def fix_text_operators(latex):
    """Replace \\text{op} with \\op or \\operatorname{op}."""
    changed = False
    for word, replacement in STANDARD_OPERATORS.items():
        old = f"\\text{{{word}}}"
        if old in latex:
            latex = latex.replace(old, replacement)
            changed = True
    for word in OPERATORNAME_WORDS:
        old = f"\\text{{{word}}}"
        if old in latex:
            latex = latex.replace(old, f"\\operatorname{{{word}}}")
            changed = True
    return latex, changed


def fix_subscript_braces(latex):
    """Fix _word to _{word} for multi-char subscripts."""
    # Match _ followed by 2+ alpha chars NOT already followed by { or preceded by {
    # Also avoid matching inside \text{...} or \operatorname{...}
    pattern = r'(?<!\\text\{)(?<!\\operatorname\{)_([a-zA-Z]{2,})(?!\{)(?![a-zA-Z])'
    new_latex = re.sub(pattern, r'_{\1}', latex)

    # Simpler fallback: just look for _ + multi-alpha not in braces
    # Need to be more careful: _abc should become _{abc}, but _{abc} should stay
    if new_latex == latex:
        # Try a more direct approach
        new_latex = re.sub(r'_([a-zA-Z]{2,})(?![{}a-zA-Z])', r'_{\1}', latex)

    return new_latex, new_latex != latex


def fix_html_entities_in_math(latex):
    """Convert HTML entities to LaTeX equivalents inside math."""
    changed = False
    for entity, replacement in ENTITY_MAP.items():
        if entity in latex:
            latex = latex.replace(entity, replacement)
            changed = True
    return latex, changed


def fix_math_in_text(text):
    """Apply fixes to all math blocks and inline math in text."""
    stats = defaultdict(int)

    # Fix display math $$...$$ first (greedy from outer)
    def fix_display_block(m):
        original = m.group(1)
        latex = original

        latex, c1 = fix_text_operators(latex)
        if c1:
            stats["TEXT_SHOULD_BE_OPERATOR"] += 1

        latex, c2 = fix_subscript_braces(latex)
        if c2:
            stats["SUBSCRIPT_NO_BRACES"] += 1

        latex, c3 = fix_html_entities_in_math(latex)
        if c3:
            stats["HTML_ENTITY_IN_BLOCK"] += 1

        if latex != original:
            return f"$${latex}$$"
        return m.group(0)

    # NOTE: In Python 3.14, \$ in regex is treated as end-of-string anchor ($),
    # not a literal dollar sign. Use [$] instead for literal dollar matching.
    text = re.sub(r'[$][$](.*?)[$][$]', fix_display_block, text, flags=re.DOTALL)

    # Fix inline math $...$
    def fix_inline_math(m):
        original = m.group(1)
        latex = original

        # Skip if it looks like it contains HTML (false positive territory)
        if re.search(r'<(?:div|p|span|strong|em|h[1-6])\b', latex):
            return m.group(0)

        latex, c1 = fix_text_operators(latex)
        if c1:
            stats["TEXT_SHOULD_BE_OPERATOR_INLINE"] += 1

        latex, c2 = fix_subscript_braces(latex)
        if c2:
            stats["SUBSCRIPT_NO_BRACES_INLINE"] += 1

        latex, c3 = fix_html_entities_in_math(latex)
        if c3:
            stats["HTML_ENTITY_IN_LATEX"] += 1

        if latex != original:
            return f"${latex}$"
        return m.group(0)

    text = re.sub(r'(?<![$])[$](?![$])(.*?)(?<![$])[$](?![$])', fix_inline_math, text, flags=re.DOTALL)

    return text, stats


def fix_legacy_styled_math(text):
    """Convert <p style="text-align: center; font-style: italic;...">content</p> to math-block divs."""
    count = 0

    def replace_legacy(m):
        nonlocal count
        content = m.group(1).strip()

        # If content already has $$ delimiters, just wrap it
        if '$$' in content:
            count += 1
            return f'<div class="math-block">\n{content}\n</div>'

        # Otherwise, strip any remaining HTML formatting and wrap with $$
        clean = re.sub(r'</?(?:em|i|b|strong|span)[^>]*>', '', content).strip()
        if clean:
            count += 1
            return f'<div class="math-block">\n$${clean}$$\n</div>'

        return m.group(0)

    # Match the legacy pattern: <p with text-align:center and font-style:italic
    pattern = r'<p\s+style="[^"]*text-align:\s*center[^"]*font-style:\s*italic[^"]*"[^>]*>(.*?)</p>'
    text = re.sub(pattern, replace_legacy, text, flags=re.DOTALL)

    # Also match reversed order (font-style first, then text-align)
    pattern2 = r'<p\s+style="[^"]*font-style:\s*italic[^"]*text-align:\s*center[^"]*"[^>]*>(.*?)</p>'
    text = re.sub(pattern2, replace_legacy, text, flags=re.DOTALL)

    return text, count


def process_file(filepath):
    """Process a single file and return change stats."""
    text = filepath.read_text(encoding="utf-8")
    original = text

    # Apply math fixes
    text, math_stats = fix_math_in_text(text)

    # Apply legacy styled math fixes
    text, legacy_count = fix_legacy_styled_math(text)
    if legacy_count:
        math_stats["LEGACY_STYLED_MATH"] = legacy_count

    if text != original:
        filepath.write_text(text, encoding="utf-8")
        return math_stats
    return {}


def main():
    files = find_html_files()
    print(f"Processing {len(files)} HTML files...\n")

    total_stats = defaultdict(int)
    files_changed = 0

    for f in files:
        stats = process_file(f)
        if stats:
            files_changed += 1
            rel = f.relative_to(BASE)
            fixes = ", ".join(f"{k}: {v}" for k, v in sorted(stats.items()))
            print(f"  {rel}: {fixes}")
            for k, v in stats.items():
                total_stats[k] += v

    total_fixes = sum(total_stats.values())
    print(f"\n{'='*60}")
    print(f"TOTAL: {total_fixes} fixes in {files_changed} files\n")
    print("By type:")
    for k, v in sorted(total_stats.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
