"""v3.6 R4#4: Targeted rewrites for the worst generic caption patterns.

These are conservative improvements (not LLM-quality), aimed at fixing
captions that read as auto-generated. Truly excellent captions need
context-aware rewriting; this script does the safe minimum:

  "pip install X"          -> "Install <X>"
  "implement <fn>"         -> "Implementation of <fn>"
  "Define X; implement Y"  -> "Implementation of <X>"
  "Working with X"         -> "Using <X>"
  "This command <verb>..." -> capitalize, drop "This command"

Captions that already start with a CONCRETE verb/noun (Encode, Compute,
Build, etc.) are left alone.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

# (regex, replacement-callable)
def _make_install(m: re.Match) -> str:
    pkgs = m.group(2).strip().rstrip(".").rstrip(",")
    pkg_list = re.split(r"\s+", pkgs)[:3]
    pkg_str = ", ".join(p for p in pkg_list if p) or "package"
    return f"{m.group(1)} Install {pkg_str}"


def _make_implement(m: re.Match) -> str:
    name = m.group(2).strip().rstrip(".").rstrip(",")
    return f"{m.group(1)} Implementation of {name}"


def _make_define_implement(m: re.Match) -> str:
    name = m.group(2).strip().rstrip(",")
    return f"{m.group(1)} Implementation of {name}"


def _make_working_with(m: re.Match) -> str:
    name = m.group(2).strip().rstrip(".").rstrip(",")
    return f"{m.group(1)} Using {name}"


def _make_this_command(m: re.Match) -> str:
    rest = m.group(2).strip()
    # Capitalize first verb
    if rest:
        rest = rest[0].upper() + rest[1:]
    return f"{m.group(1)} {rest}"


REWRITES = [
    (re.compile(r'(<strong>Code Fragment\s+\d+\.\d+\.\d+:?</strong>)\s+pip install ([^<]{1,80})'),
     _make_install),
    (re.compile(r'(<strong>Code Fragment\s+\d+\.\d+\.\d+:?</strong>)\s+implement (\w[^<]{0,50})'),
     _make_implement),
    (re.compile(r'(<strong>Code Fragment\s+\d+\.\d+\.\d+:?</strong>)\s+Define \w+; implement ([^<]{1,60})'),
     _make_define_implement),
    (re.compile(r'(<strong>Code Fragment\s+\d+\.\d+\.\d+:?</strong>)\s+Working with (\w[^<]{0,50})'),
     _make_working_with),
    (re.compile(r'(<strong>Code Fragment\s+\d+\.\d+\.\d+:?</strong>)\s+This command (\w[^<]{0,80})'),
     _make_this_command),
]


def main() -> int:
    n_files = 0
    n_rewrites = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        file_n = 0
        for pat, fn in REWRITES:
            text, n = pat.subn(fn, text)
            file_n += n
        if file_n > 0 and text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_rewrites += file_n
    print(f"Improved {n_rewrites} generic captions across {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
