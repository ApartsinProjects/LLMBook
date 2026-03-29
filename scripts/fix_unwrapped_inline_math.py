"""
Find and wrap inline math expressions that aren't inside <span class="math">.

Targets:
1. Standalone variables with subscripts/superscripts in prose (e.g., X<sub>q</sub>)
2. Short formulas with operators in prose (e.g., a × b, n − 1)
3. Greek letter entities not in .math (e.g., &alpha;, &Sigma;)

Does NOT wrap:
- Content inside <pre>, <code>, <a>, or existing .math spans
- HTML markup like <sub>1</sub> that's part of section numbering
- Subscripts in headings (h1-h3)
"""

import re
from pathlib import Path
from collections import defaultdict

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles", "agents", "_lab_fragments"}

# Math operators that suggest formula context
MATH_OPS = {'×', '·', '÷', '±', '≤', '≥', '≠', '≈', '∈', '∉', '⊂', '→', '←', '↔',
            '&times;', '&middot;', '&divide;', '&plusmn;', '&le;', '&ge;', '&ne;', '&asymp;',
            '&minus;', '&#770;', '&#x302;'}

# Greek letters
GREEK = {'&alpha;', '&beta;', '&gamma;', '&delta;', '&epsilon;', '&zeta;', '&eta;',
         '&theta;', '&iota;', '&kappa;', '&lambda;', '&mu;', '&nu;', '&xi;',
         '&pi;', '&rho;', '&sigma;', '&tau;', '&phi;', '&chi;', '&psi;', '&omega;',
         '&Alpha;', '&Beta;', '&Gamma;', '&Delta;', '&Epsilon;', '&Theta;',
         '&Lambda;', '&Sigma;', '&Phi;', '&Psi;', '&Omega;',
         '&nabla;', '&part;', '&infin;', '&sum;', '&prod;', '&int;',
         'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'λ', 'μ', 'σ', 'τ', 'φ', 'π', 'ω',
         'Σ', 'Π', 'Δ', 'Ω', '∇', '∂', '∞'}

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def wrap_math_in_line(line):
    """Wrap identified math expressions in <span class="math">."""
    if '<pre' in line or '<code' in line or '<h1' in line or '<h2' in line or '<h3' in line:
        return line, 0

    fixes = 0
    original = line

    # Pattern 1: Single letter/word followed by <sub> or <sup> not already in .math
    # e.g., X<sub>q</sub>, W<sup>T</sup>, x<sub>i</sub>
    def wrap_var_sub(m):
        nonlocal fixes
        full = m.group(0)
        # Check if already inside span.math by looking at context
        # Simple check: if preceded by class="math"> don't wrap
        start = m.start()
        preceding = line[max(0, start-20):start]
        if 'class="math">' in preceding or '<span class="math">' in preceding:
            return full
        fixes += 1
        return f'<span class="math">{full}</span>'

    # Match: letter(s) followed by <sub>...</sub> or <sup>...</sup> (possibly chained)
    line = re.sub(
        r'(?<![">])\b([A-Za-z]\w{0,5})(<su[bp]>[^<]{1,20}</su[bp]>(?:<su[bp]>[^<]{1,20}</su[bp]>)?)',
        wrap_var_sub,
        line,
    )

    # Pattern 2: Expressions with combining characters (X&#770; = X-hat)
    def wrap_combining(m):
        nonlocal fixes
        start = m.start()
        preceding = line[max(0, start-20):start]
        if 'class="math">' in preceding:
            return m.group(0)
        fixes += 1
        return f'<span class="math">{m.group(0)}</span>'

    line = re.sub(
        r'(?<![">])\b([A-Za-z]\w{0,3})(&#\d{3,4};|&#x[0-9a-fA-F]+;)',
        wrap_combining,
        line
    )

    return line, fixes

def fix_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    new_lines = []
    total_fixes = 0
    in_pre = False
    in_code = False
    in_math_block = False

    for line in lines:
        if '<pre' in line:
            in_pre = True
        if '</pre>' in line:
            in_pre = False
        if '<code' in line and '<pre' not in line:
            in_code = True
        if '</code>' in line:
            in_code = False
        if 'math-block' in line:
            in_math_block = True
        if in_math_block and '</div>' in line:
            in_math_block = False

        if not in_pre and not in_code and not in_math_block:
            line, fixes = wrap_math_in_line(line)
            total_fixes += fixes

        new_lines.append(line)

    if total_fixes:
        filepath.write_text("\n".join(new_lines), encoding="utf-8")
    return total_fixes

def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files for unwrapped inline math...\n")

    total = 0
    files_fixed = 0

    for f in files:
        n = fix_file(f)
        if n:
            files_fixed += 1
            total += n
            if n >= 3:
                print(f"  {f.relative_to(BASE)}: {n} expressions wrapped")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total} inline math expressions wrapped in {files_fixed} files")

if __name__ == "__main__":
    main()
