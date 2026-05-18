"""Phase 4: regenerate prev/next nav for Part 9 + Part 10 affected modules."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TARGETS = [
    "part-9-safety-security-ethics/module-39-adversarial-security-red-team",
    "part-9-safety-security-ethics/module-40-guardrails-runtime-safety",
    "part-9-safety-security-ethics/module-41-agent-safety-autonomy",
    "part-9-safety-security-ethics/module-42-privacy-data-protection",
    "part-9-safety-security-ethics/module-43-bias-fairness",
    "part-9-safety-security-ethics/module-44-hallucination-truthfulness",
    "part-9-safety-security-ethics/module-45-regulation-compliance",
    "part-9-safety-security-ethics/module-46-watermarking-provenance",
    "part-9-safety-security-ethics/module-47-transparency-documentation",
    "part-9-safety-security-ethics/module-48-environmental-sustainability",
    "part-9-safety-security-ethics/module-49-frontier-safety-open-problems",
    "part-9-safety-security-ethics/module-50-tools-of-the-trade",
    "part-10-idea-to-product/module-51-ideation",
    "part-10-idea-to-product/module-52-product-management",
    "part-10-idea-to-product/module-53-strategy-prioritization",
    "part-10-idea-to-product/module-54-vibe-coding",
    "part-10-idea-to-product/module-55-mvp",
    "part-10-idea-to-product/module-56-prototype-to-production",
    "part-10-idea-to-product/module-57-compute-planning",
    "part-10-idea-to-product/module-58-scaling-economics",
    "part-10-idea-to-product/module-59-shipping-deploying",
    "part-10-idea-to-product/module-60-production-engineering",
    "part-10-idea-to-product/module-61-tools-of-the-trade",
]


def get_chapter_title(mod_dir):
    idx = mod_dir / "index.html"
    if not idx.exists(): return "?"
    t = idx.read_text(encoding="utf-8")
    m = re.search(r"<h1>([^<]+)</h1>", t)
    return m.group(1) if m else "?"


def get_section_title(sec):
    t = sec.read_text(encoding="utf-8")
    m = re.search(r"<h1>([^<]+)</h1>", t)
    return m.group(1) if m else "?"


def get_section_num(filename):
    m = re.match(r"section-(\d+)\.(\d+)\.html", filename)
    if not m: return None
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
    for mod_rel in TARGETS:
        mod = ROOT / mod_rel
        if not mod.exists(): continue
        ct = get_chapter_title(mod)
        secs = sorted(mod.glob("section-*.html"),
                      key=lambda p: get_section_num(p.name) or (999, 999))
        if not secs: continue
        cn = get_section_num(secs[0].name)[0]
        for i, sec in enumerate(secs):
            prev = secs[i-1] if i > 0 else None
            nxt = secs[i+1] if i < len(secs)-1 else None
            n += regen(sec, prev, nxt, ct, cn, dry_run)
    print(f"Sections nav regenerated: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
