"""Helper: find duplicate singleton callouts in target files.

Lists each file's duplicate callout types with their byte offsets so we can
inspect/consolidate them.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

SINGLETONS = [
    ("big-picture",   r'<div\s+class="callout big-picture"', "div"),
    ("prerequisites", r'<div\s+class="prerequisites"',       "div"),
    ("lab",           r'<div\s+class="callout lab"',         "div"),
    ("key-takeaway",  r'<div\s+class="callout key-takeaway"', "div"),
    ("self-check",    r'<div\s+class="callout self-check"',  "div"),
    ("exercises",     r'<section\s+class="exercises"',       "section"),
    ("whats-next",    r'<div\s+class="(?:callout\s+)?whats-next"', "div"),
    ("bibliography",  r'<details\s+class="bibliography-collapsible', "details"),
]

def find_matching_close(text: str, start: int, tag: str) -> int:
    open_re = re.compile(rf'<{tag}\b', re.IGNORECASE)
    close_re = re.compile(rf'</{tag}>', re.IGNORECASE)
    depth = 1
    gt = text.find('>', start)
    if gt < 0:
        return -1
    pos = gt + 1
    while depth > 0 and pos < len(text):
        next_open = open_re.search(text, pos)
        next_close = close_re.search(text, pos)
        if not next_close:
            return -1
        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            pos = next_close.end()
    return pos if depth == 0 else -1


def report_file(p: Path):
    text = p.read_text(encoding="utf-8")
    print(f"\n=== {p.relative_to(ROOT)} ===")
    for name, pat, kind in SINGLETONS:
        regex = re.compile(pat, re.IGNORECASE)
        matches = list(regex.finditer(text))
        if len(matches) > 1:
            print(f"  DUPLICATE '{name}' x{len(matches)}:")
            for m in matches:
                # Line number
                line = text.count('\n', 0, m.start()) + 1
                end = find_matching_close(text, m.start(), kind)
                length = end - m.start() if end > 0 else -1
                # Get a short preview
                preview_end = min(m.start() + 200, end if end > 0 else m.start() + 200)
                preview = text[m.start():preview_end].replace('\n', ' ')[:160]
                print(f"    L{line} (len={length}): {preview}...")


if __name__ == "__main__":
    files = sys.argv[1:]
    for f in files:
        report_file(ROOT / f)
