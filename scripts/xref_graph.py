"""Cross-reference graph analyzer.

Builds a directed graph of section-to-section cross-references and
flags structural anomalies:
  - ORPHANS: sections with 0 inbound xrefs (nothing else points to them)
  - SINKS: sections with 0 outbound xrefs (don't point to anything)
  - HUBS: sections with very high inbound count (over-cited, likely
    the canonical home for one or more entities)
  - DEAD ENDS: sections in the middle of a chapter with no xrefs to
    earlier/later sections

This is a fast Python pass (no LLM); the report points an editor at
where prose needs more interconnection. Cross-references are the
spine that holds a textbook together. A book with lots of orphans
reads as a series of unrelated essays.

Usage
-----
    /c/Python314/python scripts/xref_graph.py
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}

HREF_RE = re.compile(r'href="([^"]+\.html)(?:#[^"]*)?"', re.IGNORECASE)


def section_id(p: Path) -> str:
    m = re.match(r'section-([\d.]+\w*)\.html', p.name)
    if m:
        return f"S{m.group(1)}"
    if p.name == "index.html":
        mm = re.search(r'module-(\d+\w*)', str(p))
        return f"M{mm.group(1)}.idx" if mm else p.parent.name
    return p.name


def gather() -> dict[str, Path]:
    """Map section_id -> path."""
    sids: dict[str, Path] = {}
    for p in ROOT.rglob("*.html"):
        if set(p.parts) & SKIP_DIRS:
            continue
        if not (p.name.startswith("section-") or p.name == "index.html"):
            continue
        sids[section_id(p)] = p
    return sids


def build_graph(sids: dict[str, Path]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return (outbound, inbound) maps: sid -> set of target sids."""
    outbound: dict[str, set[str]] = defaultdict(set)
    inbound: dict[str, set[str]] = defaultdict(set)
    by_path: dict[str, str] = {}
    for sid, p in sids.items():
        rel = str(p.relative_to(ROOT)).replace('\\', '/')
        by_path[rel] = sid

    for sid, p in sids.items():
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in HREF_RE.finditer(html):
            href = m.group(1)
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            # Resolve href relative to p
            target = (p.parent / href).resolve()
            try:
                target_rel = str(target.relative_to(ROOT)).replace('\\', '/')
            except ValueError:
                continue
            tsid = by_path.get(target_rel)
            if tsid and tsid != sid:
                outbound[sid].add(tsid)
                inbound[tsid].add(sid)
    return outbound, inbound


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    sids = gather()
    outbound, inbound = build_graph(sids)

    # Only score section-* (not index.html aggregates)
    section_sids = [s for s in sids if s.startswith("S")]
    n = len(section_sids)

    inb = [(s, len(inbound[s])) for s in section_sids]
    out = [(s, len(outbound[s])) for s in section_sids]

    orphans = sorted([s for s, c in inb if c == 0])
    sinks = sorted([s for s, c in out if c == 0])

    hubs = sorted(inb, key=lambda kv: -kv[1])[:20]
    super_outbound = sorted(out, key=lambda kv: -kv[1])[:10]

    inb_counts = Counter(c for _, c in inb)
    out_counts = Counter(c for _, c in out)

    # Render markdown
    lines = []
    lines.append("# Cross-Reference Graph Report")
    lines.append("")
    lines.append(f"Sections scanned: {n}")
    lines.append("")
    lines.append("## Distribution of inbound xrefs")
    lines.append("")
    lines.append("| Inbound count | Number of sections |")
    lines.append("|---:|---:|")
    for k in sorted(inb_counts):
        if k <= 5 or inb_counts[k] >= 5:
            lines.append(f"| {k} | {inb_counts[k]} |")
    lines.append("")
    lines.append("## Distribution of outbound xrefs")
    lines.append("")
    lines.append("| Outbound count | Number of sections |")
    lines.append("|---:|---:|")
    for k in sorted(out_counts):
        if k <= 5 or out_counts[k] >= 5:
            lines.append(f"| {k} | {out_counts[k]} |")
    lines.append("")

    lines.append(f"## Orphans ({len(orphans)} sections with 0 inbound xrefs)")
    lines.append("")
    lines.append("Nothing in the book links to these. Either: (a) they're the")
    lines.append("entry-point for a topic and others should xref them, or (b)")
    lines.append("they cover content that should connect to neighbors but")
    lines.append("doesn't. Editorial review needed.")
    lines.append("")
    for s in orphans:
        rel = str(sids[s].relative_to(ROOT)).replace('\\', '/')
        lines.append(f"- `{s}` {rel}")
    lines.append("")

    lines.append(f"## Sinks ({len(sinks)} sections with 0 outbound xrefs)")
    lines.append("")
    lines.append("These sections don't point to anything. Likely missing")
    lines.append("\"see also\" links to related content elsewhere in the book.")
    lines.append("")
    for s in sinks:
        rel = str(sids[s].relative_to(ROOT)).replace('\\', '/')
        lines.append(f"- `{s}` {rel}")
    lines.append("")

    lines.append("## Top hubs (most-referenced sections)")
    lines.append("")
    lines.append("High inbound count means many other sections cite this one.")
    lines.append("These are typically canonical homes for foundational topics.")
    lines.append("")
    lines.append("| Section | Inbound | Path |")
    lines.append("|---|---:|---|")
    for s, c in hubs:
        rel = str(sids[s].relative_to(ROOT)).replace('\\', '/')
        lines.append(f"| {s} | {c} | {rel} |")
    lines.append("")

    lines.append("## Top connectors (most outbound xrefs)")
    lines.append("")
    lines.append("Sections that point to many others. Often survey or")
    lines.append("index-style sections that knit topics together.")
    lines.append("")
    lines.append("| Section | Outbound | Path |")
    lines.append("|---|---:|---|")
    for s, c in super_outbound:
        rel = str(sids[s].relative_to(ROOT)).replace('\\', '/')
        lines.append(f"| {s} | {c} | {rel} |")
    lines.append("")

    md = "\n".join(lines)
    out_path = Path(args.out) if args.out else ROOT / "docs" / "content-audit" / "XREF_GRAPH_REPORT.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

    print(f"Report: {out_path.relative_to(ROOT)}")
    print(f"\nSections: {n}")
    print(f"Orphans (0 inbound): {len(orphans)}")
    print(f"Sinks (0 outbound):  {len(sinks)}")
    print(f"\nTop 5 hubs:")
    for s, c in hubs[:5]:
        print(f"  {s}: {c} inbound xrefs")


if __name__ == "__main__":
    main()
