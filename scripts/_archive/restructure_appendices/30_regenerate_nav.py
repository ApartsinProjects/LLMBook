"""Phase 30: regenerate prev/next nav for ToT modules that received
new sections from appendices. Same logic as restructure_part8/70.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

TARGET_MODULES = [
    "part-1-foundations/module-06-tools-of-the-trade",
    "part-2-understanding-llms/module-12-tools-of-the-trade",
    "part-3-working-with-llms/module-16-tools-of-the-trade",
    "part-4-training-adapting/module-21-tools-of-the-trade",
    "part-5-retrieval-conversation/module-25-tools-of-the-trade",
    "part-6-agentic-ai/module-30-tools-of-the-trade",
    "part-8-evaluation-production/module-38-tools-of-the-trade",
    "part-10-idea-to-product/module-52-tools-of-the-trade",
]


def get_chapter_title(mod_dir):
    idx = mod_dir / "index.html"
    if not idx.exists():
        return "?"
    t = idx.read_text(encoding="utf-8")
    m = re.search(r"<h1>([^<]+)</h1>", t)
    return m.group(1) if m else "?"


def get_section_title(sec):
    t = sec.read_text(encoding="utf-8")
    m = re.search(r"<h1>([^<]+)</h1>", t)
    return m.group(1) if m else "?"


def get_section_num(filename):
    m = re.match(r"section-(\d+)\.(\d+)\.html", filename)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def regen(sec, prev, nxt, ch_title, ch_num, dry_run):
    text = sec.read_text(encoding="utf-8")
    parts = []
    if prev:
        pn = get_section_num(prev.name)
        pt = get_section_title(prev)
        parts.append(
            f'<a class="prev" href="{prev.name}"><span class="nav-label">Previous</span>'
            f'<span class="nav-num">Section {pn[0]}.{pn[1]}</span>'
            f'<span class="nav-title">{pt}</span></a>'
        )
    parts.append(
        f'<a class="up" href="index.html"><span class="nav-label">In Chapter</span>'
        f'<span class="nav-num">Chapter {ch_num}</span>'
        f'<span class="nav-title">{ch_title}</span></a>'
    )
    if nxt:
        nn = get_section_num(nxt.name)
        nt = get_section_title(nxt)
        parts.append(
            f'<a class="next" href="{nxt.name}"><span class="nav-label">Next</span>'
            f'<span class="nav-num">Section {nn[0]}.{nn[1]}</span>'
            f'<span class="nav-title">{nt}</span></a>'
        )
    new_nav = '<nav class="chapter-nav">\n' + '\n'.join(parts) + '\n</nav>'
    new_text = re.sub(r'<nav class="chapter-nav">[\s\S]*?</nav>', new_nav, text, count=1)
    if new_text != text and not dry_run:
        sec.write_text(new_text, encoding="utf-8")
    return 1 if new_text != text else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    n = 0
    for mod_rel in TARGET_MODULES:
        mod = ROOT / mod_rel
        if not mod.exists():
            continue
        ct = get_chapter_title(mod)
        secs = sorted(
            mod.glob("section-*.html"),
            key=lambda p: get_section_num(p.name) or (999, 999),
        )
        if not secs:
            continue
        cn = get_section_num(secs[0].name)[0]
        for i, sec in enumerate(secs):
            prev = secs[i - 1] if i > 0 else None
            nxt = secs[i + 1] if i < len(secs) - 1 else None
            n += regen(sec, prev, nxt, ct, cn, dry_run)
    print(f"Sections nav regenerated: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
