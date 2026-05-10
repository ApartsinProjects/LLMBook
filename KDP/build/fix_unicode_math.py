"""Replace precomposed Unicode math characters (ŷ, x̂, ȳ etc.) with proper
LaTeX commands (\\hat{y}, \\hat{x}, \\bar{y}) inside `$...$`, `$$...$$`,
and `\\(...\\)` blocks.

Root cause: source HTML has math like `$$MSE = \\sum (ŷ_i - y_i)^2$$`.
KaTeX renders Unicode characters but spacing + font for precomposed combining
characters is unreliable, producing displaced hats / shifted superscripts.
LaTeX `\\hat{y}` is the canonical form and renders perfectly.

Idempotent: running multiple times is safe.
"""
from __future__ import annotations
import re
import shutil
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Map precomposed Unicode -> LaTeX command (kept for completeness).
PRECOMPOSED_TO_LATEX = {
    "ŷ": r"\hat{y}",  "Ŷ": r"\hat{Y}",  # ŷ Ŷ
    "â": r"\hat{a}",  "Â": r"\hat{A}",  # â Â
    "î": r"\hat{i}",  "Î": r"\hat{I}",  # î Î
    "ô": r"\hat{o}",  "Ô": r"\hat{O}",  # ô Ô
    "û": r"\hat{u}",  "Û": r"\hat{U}",  # û Û
    # ȳ Ȳ x̄ X̄
    "ȳ": r"\bar{y}", "Ȳ": r"\bar{Y}",
    # ỹ Ỹ x̃ X̃
    "ỹ": r"\tilde{y}", "Ỹ": r"\tilde{Y}",
}

# Combining marks (these are the COMMON case in this book):
#   y + U+0302 (combining circumflex) -> \hat{y}
#   y + U+0304 (combining macron)     -> \bar{y}
#   y + U+0303 (combining tilde)      -> \tilde{y}
#   y + U+0307 (combining dot above)  -> \dot{y}
COMBINING_TO_LATEX_FUNC = {
    "̂": "hat",
    "̄": "bar",
    "̃": "tilde",
    "̇": "dot",
    "̊": "mathring",
}

# Greek letter Unicode -> LaTeX command (used for combining cases like θ̂)
GREEK_TO_LATEX = {
    "α": r"\alpha",   "β": r"\beta",    "γ": r"\gamma",
    "δ": r"\delta",   "ε": r"\epsilon", "ζ": r"\zeta",
    "η": r"\eta",     "θ": r"\theta",   "ι": r"\iota",
    "κ": r"\kappa",   "λ": r"\lambda",  "μ": r"\mu",
    "ν": r"\nu",      "ξ": r"\xi",      "ο": "o",
    "π": r"\pi",      "ρ": r"\rho",     "σ": r"\sigma",
    "τ": r"\tau",     "υ": r"\upsilon", "φ": r"\phi",
    "χ": r"\chi",     "ψ": r"\psi",     "ω": r"\omega",
    "Θ": r"\Theta",   "Λ": r"\Lambda",  "Ξ": r"\Xi",
    "Σ": r"\Sigma",   "Φ": r"\Phi",     "Ψ": r"\Psi",
    "Ω": r"\Omega",   "Δ": r"\Delta",   "Γ": r"\Gamma",
}


def fix_combining_accents(s: str) -> tuple[str, int]:
    """Walk through string, replace `letter + combining-mark` with LaTeX."""
    out = []
    i = 0
    n_replaced = 0
    while i < len(s):
        c = s[i]
        # Look ahead for combining mark
        if i + 1 < len(s) and s[i + 1] in COMBINING_TO_LATEX_FUNC:
            mark = s[i + 1]
            func_name = COMBINING_TO_LATEX_FUNC[mark]
            # Determine the letter: ASCII letter or Greek
            if c.isascii() and c.isalpha():
                latex_letter = c
            elif c in GREEK_TO_LATEX:
                latex_letter = GREEK_TO_LATEX[c]
            else:
                # Unknown base, keep as-is
                out.append(c)
                i += 1
                continue
            out.append(f"\\{func_name}{{{latex_letter}}}")
            i += 2  # skip the combining mark
            n_replaced += 1
        else:
            out.append(c)
            i += 1
    return "".join(out), n_replaced

MATH_PAT = re.compile(
    r"(\$\$.+?\$\$|\$[^$\n]+?\$|\\\(.+?\\\)|\\\[.+?\\\]|<span class=\"math\">[^<]+</span>)",
    re.DOTALL,
)


def fix_math(content: str) -> tuple[str, int]:
    n_total = 0
    def replace_math(m: re.Match) -> str:
        nonlocal n_total
        s = m.group(0)
        n_local = 0
        # Step 1: precomposed
        for uni, latex in PRECOMPOSED_TO_LATEX.items():
            if uni in s:
                count = s.count(uni)
                s = s.replace(uni, latex)
                n_local += count
        # Step 2: combining accents (letter + diacritic)
        s2, n_acc = fix_combining_accents(s)
        s = s2
        n_local += n_acc
        n_total += n_local
        return s
    new_content = MATH_PAT.sub(replace_math, content)
    return new_content, n_total


def main() -> int:
    files_modified: list[tuple[str, int]] = []
    backup_dir = PROJECT_ROOT / "KDP/build/source_fix_backups" / time.strftime("unicode_math_%Y%m%d_%H%M%S")

    for path in PROJECT_ROOT.rglob("*.html"):
        if any(part in path.parts for part in ("KDP", "vendor", "scripts", "templates", "md", "node_modules")):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        # Quick filter: only process files containing math syntax + any
        # combining mark or precomposed accent
        if not any(marker in text for marker in ("$$", "\\(", "\\[", 'class="math"')):
            continue
        has_combining = any(c in text for c in COMBINING_TO_LATEX_FUNC)
        has_precomposed = any(c in text for c in PRECOMPOSED_TO_LATEX)
        if not (has_combining or has_precomposed):
            continue

        new_text, n = fix_math(text)
        if n > 0 and new_text != text:
            backup_dir.mkdir(parents=True, exist_ok=True)
            rel = path.relative_to(PROJECT_ROOT)
            backup = backup_dir / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
            path.write_text(new_text, encoding="utf-8")
            files_modified.append((str(rel).replace("\\", "/"), n))

    print(f"Fixed {sum(n for _, n in files_modified)} precomposed Unicode math chars in {len(files_modified)} files")
    for rel, n in files_modified[:30]:
        print(f"  {n}x  {rel}")
    if len(files_modified) > 30:
        print(f"  ... +{len(files_modified) - 30} more")
    if files_modified:
        print(f"\nBackups: {backup_dir.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
