"""Boilerplate-prose detector: hybrid statistical + LLM pipeline.

Theory
------
A section is "boilerplate" when it reads like a generic outline that
could appear in any LLM textbook. Tell-tale features:
  - Many short paragraphs, few long ones (stub content)
  - High list-density (shopping lists instead of explanation)
  - High hedging density (may / might / could / perhaps / often)
  - Low concrete-evidence density (few numbers, named entities,
    citations, code references, named papers)
  - High generic-phrase density ("In this section we will...",
    "As we have seen...", "It is important to note that...")
  - Repeated boilerplate openings across sections (template scaffolding)

This script extracts per-section features deterministically with regex
and produces a ranked list of suspects. An LLM agent can then read each
suspect and decide: real-but-thin vs. true boilerplate vs. fine-as-is.

The pipeline is fast (few seconds for the whole book) because all
features are regex-counted with no LLM calls. The LLM only sees the
top N suspects for judgment.

Usage
-----
    /c/Python314/python scripts/boilerplate_detector.py
    /c/Python314/python scripts/boilerplate_detector.py --top 30
    /c/Python314/python scripts/boilerplate_detector.py --chapter 42
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}

# ============= Feature regex patterns =============
HEDGE_TERMS = re.compile(
    r'\b(may|might|could|perhaps|sometimes|often|typically|usually|'
    r'generally|frequently|in some cases|in many cases|tend to|tends to|'
    r'in general|broadly|by and large|more or less|somewhat)\b',
    re.IGNORECASE,
)
GENERIC_PHRASES = re.compile(
    r'\b(in this section we will|in this section,? we will|'
    r'as we have seen|as we will see|as discussed|as mentioned|'
    r'it is important to note|it is worth noting|it should be noted|'
    r'in summary|to summarize|the key takeaway|the main point|'
    r'broadly speaking|generally speaking|put simply|in other words|'
    r'this section covers|this section will|this section discusses|'
    r'this section explores|we will discuss|we will explore|'
    r'in this chapter,? we|in conclusion|to conclude)\b',
    re.IGNORECASE,
)
NUMBER_RE = re.compile(r'\b\d+(?:[.,]\d+)*\b')
CITATION_RE = re.compile(r'\b(?:[A-Z][a-z]+\s+(?:et al\.|and \w+),?\s*\(?\d{4}\)?|'
                          r'\(\d{4}\)|arxiv\.org/abs/\d|doi\.org/10\.)')
CODE_REF_RE = re.compile(r'<code\b[^>]*>([^<]+)</code>')
LINK_RE = re.compile(r'<a\s+[^>]*href=')
STRONG_RE = re.compile(r'<strong\b[^>]*>')

# Section/paragraph extraction
TAG_RE = re.compile(r'<[^>]+>')
CODE_BLOCK_RE = re.compile(
    r'<div\s+class="code-block-wrapper"[^>]*>.*?</div>\s*',
    re.DOTALL | re.IGNORECASE,
)
HEADER_FOOTER_RE = re.compile(
    r'<(header|footer|nav|script|style)[^>]*>.*?</\1>',
    re.DOTALL | re.IGNORECASE,
)
PARAGRAPH_RE = re.compile(r'<p\b[^>]*>(.*?)</p>', re.DOTALL | re.IGNORECASE)
LIST_RE = re.compile(r'<(ul|ol)\b[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
H2_RE = re.compile(r'<h2\b[^>]*>(.*?)</h2>', re.DOTALL | re.IGNORECASE)


def visible_text(s: str) -> str:
    s = HEADER_FOOTER_RE.sub(' ', s)
    s = TAG_RE.sub(' ', s)
    s = html_mod.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def split_into_subsections(html: str) -> list[dict]:
    """Split a section file by h2 boundaries; each subsection is what
    follows an h2 up to (but not including) the next h2."""
    headers = list(H2_RE.finditer(html))
    if not headers:
        return [{"title": "(intro)", "html": html, "start": 0}]
    out = []
    # The bit BEFORE the first h2 (intro + big-picture)
    if headers[0].start() > 0:
        out.append({"title": "(intro)",
                    "html": html[:headers[0].start()],
                    "start": 0})
    for i, h in enumerate(headers):
        next_start = headers[i + 1].start() if i + 1 < len(headers) else len(html)
        title = TAG_RE.sub('', h.group(1)).strip()
        out.append({
            "title": title,
            "html": html[h.start():next_start],
            "start": h.start(),
        })
    return out


def extract_features(html: str) -> dict:
    """Compute boilerplate-suspect features for a subsection."""
    # Strip code blocks for prose-only metrics
    prose_html = CODE_BLOCK_RE.sub(' ', html)
    prose = visible_text(prose_html)
    words = prose.split()
    n_words = len(words)

    # Paragraph stats
    paras = [
        visible_text(m.group(1))
        for m in PARAGRAPH_RE.finditer(prose_html)
    ]
    paras_nonempty = [p for p in paras if len(p.split()) >= 3]
    n_paras = len(paras_nonempty)
    para_word_counts = [len(p.split()) for p in paras_nonempty]
    avg_para_words = sum(para_word_counts) / max(1, n_paras)
    short_para_pct = sum(1 for c in para_word_counts if c < 30) / max(1, n_paras)

    # List stats (count words inside <ul>/<ol>)
    list_words = 0
    for m in LIST_RE.finditer(prose_html):
        list_words += len(visible_text(m.group(2)).split())
    list_pct = list_words / max(1, n_words)

    # Concrete-evidence density
    n_numbers = len(NUMBER_RE.findall(prose))
    n_citations = len(CITATION_RE.findall(prose))
    n_code_refs = len(CODE_REF_RE.findall(prose_html))
    n_links = len(LINK_RE.findall(prose_html))
    n_strong = len(STRONG_RE.findall(prose_html))
    concrete_per_100w = (n_numbers + n_citations + n_code_refs + n_links) * 100 / max(1, n_words)

    # Hedging + generic
    n_hedges = len(HEDGE_TERMS.findall(prose))
    n_generic = len(GENERIC_PHRASES.findall(prose))
    hedge_per_100w = n_hedges * 100 / max(1, n_words)
    generic_per_100w = n_generic * 100 / max(1, n_words)

    return {
        "n_words": n_words,
        "n_paras": n_paras,
        "avg_para_words": round(avg_para_words, 1),
        "short_para_pct": round(short_para_pct, 2),
        "list_pct": round(list_pct, 2),
        "concrete_per_100w": round(concrete_per_100w, 1),
        "hedge_per_100w": round(hedge_per_100w, 1),
        "generic_per_100w": round(generic_per_100w, 1),
        "n_strong": n_strong,
    }


def boilerplate_score(f: dict) -> float:
    """Higher score = more suspicious. Combines features into one number.

    A genuinely-boilerplate subsection has:
      - >= 200 and <= 1500 words (very short = stub, very long = real)
      - high list_pct (>= 0.3)
      - high short_para_pct (>= 0.5)
      - LOW concrete density (< 3 per 100w)
      - HIGH hedge density (>= 2 per 100w)
      - any generic phrases
    """
    if f["n_words"] < 50:
        return 0.0  # too short to judge
    if f["n_words"] > 2500:
        return 0.0  # too long, likely real
    s = 0.0
    s += min(2.0, f["list_pct"] * 4)            # 0..2 from list density
    s += min(1.5, f["short_para_pct"] * 2)      # 0..1.5
    s += max(0.0, 4.0 - f["concrete_per_100w"]) / 2.0   # higher if low concrete
    s += min(1.5, f["hedge_per_100w"] / 2.0)    # higher if hedging
    s += min(1.0, f["generic_per_100w"])        # higher if generic phrases
    return round(s, 2)


def gather_sections(chapter: str | None) -> list[Path]:
    paths = []
    for p in ROOT.rglob("section-*.html"):
        if set(p.parts) & SKIP_DIRS:
            continue
        if chapter and f"module-{chapter}-" not in str(p):
            continue
        paths.append(p)
    return sorted(paths)


def section_id(p: Path) -> str:
    m = re.match(r'section-([\d.]+\w*)\.html', p.name)
    return f"S{m.group(1)}" if m else p.name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", help="Limit to one module number (e.g. 42)")
    parser.add_argument("--top", type=int, default=30, help="Top-N suspects")
    parser.add_argument("--out", default=None, help="Markdown output path")
    args = parser.parse_args()

    paths = gather_sections(args.chapter)
    rows = []
    for p in paths:
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        subsecs = split_into_subsections(html)
        for sub in subsecs:
            f = extract_features(sub["html"])
            score = boilerplate_score(f)
            if score < 1.5:
                continue
            rows.append({
                "section": section_id(p),
                "path": str(p.relative_to(ROOT)).replace('\\', '/'),
                "subsection": sub["title"][:60],
                "score": score,
                **f,
            })

    rows.sort(key=lambda r: -r["score"])
    top = rows[:args.top]

    # Render markdown
    lines = []
    lines.append("# Boilerplate-Prose Suspect Report")
    lines.append("")
    lines.append("Higher score = more suspicious for boilerplate / shopping-list prose.")
    lines.append("Scoring combines: list density, short-paragraph share, low concrete-")
    lines.append("evidence density (numbers/citations/links/code refs), high hedging")
    lines.append("(may/might/could/often), and generic templated phrases.")
    lines.append("")
    lines.append("Each row is one h2-bounded subsection of a section file.")
    lines.append("")
    lines.append(
        "| Score | Section | Subsection | Words | Paras | "
        "AvgP | %Short | %List | Conc/100w | Hedge/100w | Generic/100w |"
    )
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in top:
        lines.append(
            f"| {r['score']} | {r['section']} | {r['subsection']} | "
            f"{r['n_words']} | {r['n_paras']} | {r['avg_para_words']} | "
            f"{r['short_para_pct']} | {r['list_pct']} | "
            f"{r['concrete_per_100w']} | {r['hedge_per_100w']} | "
            f"{r['generic_per_100w']} |"
        )
    lines.append("")
    lines.append(f"\nTotal candidates above threshold: {len(rows)}.")

    md = "\n".join(lines)
    out_path = (Path(args.out) if args.out
                else ROOT / "docs" / "content-audit" / "BOILERPLATE_PROSE_SUSPECTS.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Report: {out_path.relative_to(ROOT)}")
    print(f"\nTop 10 suspects:")
    for r in top[:10]:
        print(f"  {r['score']:>4.2f}  {r['section']:<10}  {r['subsection']:<40}  "
              f"({r['n_words']}w, {r['list_pct']*100:.0f}% list, "
              f"{r['concrete_per_100w']} conc/100w)")
    print(f"\nTotal suspects: {len(rows)}")


if __name__ == "__main__":
    main()
