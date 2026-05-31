"""Apply all 21 fragment fixes to the corresponding HTML files.

Uses MANIFEST.tsv (number\trelpath\tline\tstart\tend) to locate each block.
Re-runs find_block from regen_block instead of trusting old offsets because
the HTML may have shifted from prior fixes.
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from regen_block import find_block, regen

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
WORK = Path(__file__).parent

import ast


def main() -> None:
    manifest = (WORK / "MANIFEST.tsv").read_text(encoding="utf-8").strip().splitlines()
    for line in manifest:
        parts = line.split("\t")
        num = parts[0]
        relpath = parts[1]
        ln = int(parts[2])
        src = (WORK / f"frag_{num}.py").read_text(encoding="utf-8")
        # Sanity-parse
        ast.parse(src)
        html_path = ROOT / relpath
        text = html_path.read_text(encoding="utf-8")
        s, e = find_block(text, ln)
        new_block = regen(src)
        new_text = text[:s] + new_block + text[e:]
        html_path.write_text(new_text, encoding="utf-8")
        print(f"  {num}  {relpath}:{ln}  (offset {s}->{e}, new_len={len(new_block)})")


if __name__ == "__main__":
    main()
