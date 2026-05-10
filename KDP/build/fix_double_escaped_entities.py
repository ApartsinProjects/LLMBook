"""Fix double-escaped HTML entities (`&amp;X;` -> `&X;`) in source HTML.

Root cause: at some point the build pipeline (or a manual edit) ran the
text through an HTML-escaper that turned `&` into `&amp;` even where it
was already part of a named entity. So `&odot;` became `&amp;odot;` which
renders as the literal string "&odot;" instead of the ⊙ symbol.

Idempotent: running multiple times is safe.
"""
from __future__ import annotations
import re
import shutil
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Whitelist of entity names we know are real HTML5 entities, so we only
# unescape these (avoid breaking accidental literal strings like "&amp;name;").
KNOWN_ENTITIES = {
    "amp", "lt", "gt", "quot", "apos", "nbsp",
    # Math / Greek / arrows commonly used in textbook
    "odot", "otimes", "oplus", "ominus", "times", "div", "divide",
    "sum", "prod", "int", "ne", "le", "ge", "approx", "equiv",
    "infin", "infty", "asymp", "sim", "cong",
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta",
    "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron",
    "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta",
    "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron",
    "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
    "nabla", "partial", "forall", "exists", "empty", "isin", "notin",
    "sub", "sup", "supe", "sube", "cap", "cup",
    "rarr", "larr", "uarr", "darr", "harr",
    "rArr", "lArr", "uArr", "dArr", "hArr",
    "to", "leftarrow", "rightarrow", "leftrightarrow",
    "ldots", "cdots", "vdots", "ddots", "middot", "bull", "hellip",
    "deg", "plusmn", "frac12", "frac14", "frac34",
    "copy", "reg", "trade", "para", "sect",
    "minus", "perp",
}


def main() -> int:
    pat = re.compile(r"&amp;([a-zA-Z][a-zA-Z0-9]*);")
    files_modified: list[tuple[str, int]] = []
    backup_dir = PROJECT_ROOT / "KDP/build/source_fix_backups" / time.strftime("entities_%Y%m%d_%H%M%S")

    for path in PROJECT_ROOT.rglob("*.html"):
        if any(part in path.parts for part in ("KDP", "vendor", "scripts", "templates", "md", "node_modules")):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "&amp;" not in text:
            continue

        def replace(m: re.Match) -> str:
            name = m.group(1)
            if name.lower() in {n.lower() for n in KNOWN_ENTITIES}:
                return f"&{name};"
            return m.group(0)  # leave alone if not in whitelist

        new_text, n = pat.subn(replace, text)
        if n > 0:
            backup_dir.mkdir(parents=True, exist_ok=True)
            rel = path.relative_to(PROJECT_ROOT)
            backup = backup_dir / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
            path.write_text(new_text, encoding="utf-8")
            files_modified.append((str(rel).replace("\\", "/"), n))

    print(f"Fixed {sum(n for _, n in files_modified)} double-escaped entities in {len(files_modified)} files")
    for rel, n in files_modified:
        print(f"  {n}x  {rel}")
    if files_modified:
        print(f"\nBackups: {backup_dir.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
