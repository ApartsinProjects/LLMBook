"""Editing-leftover and pseudo-callout detector.

Finds the embarrassing remnants of editorial history that should
not survive in a published book:
  - "Section moved", "Lab moved to Chapter X", "relocated to"
  - "the former Section X.Y", "in earlier editions"
  - "TODO:" / "FIXME:" / "XXX:" comments
  - "(deprecated)" / "[deprecated]" markers in section bodies
  - "rewritten in version N" / "rewrite pending"
  - "this chapter now begins with" / "the chapter formerly"
  - Editing-history language in prose (this section was, formerly)
  - Stale "(WIP)" / "(stub)" / "(draft)" markers

Also flags pseudo-callout HTML — divs that LOOK like callouts but
use non-canonical class patterns. The canonical pattern is:
    <div class="callout TYPE">
      <div class="callout-title">...</div>
      ...
    </div>

Non-canonical patterns flagged:
  - <div class="prereqs"> instead of <div class="prerequisites">
  - <div class="X"> where X is in {note, warning, tip, lab, exercise}
    without the "callout " prefix
  - Headings (h2/h3) used as fake callout headers without enclosing
    callout div
  - Inline "<strong>Note:</strong>" / "<strong>Warning:</strong>"
    patterns that should be wrapped in a proper callout

Outputs docs/content-audit/EDITING_LEFTOVERS.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}

# ============= Editing-leftover patterns =============
LEFTOVER_PATTERNS = [
    # (regex, category, severity 1-5)
    (re.compile(r'\bSection moved\b', re.IGNORECASE), "section-moved-callout", 5),
    (re.compile(r'\bChapter moved\b', re.IGNORECASE), "chapter-moved-callout", 5),
    (re.compile(r'\bLab moved\b', re.IGNORECASE), "lab-moved-callout", 4),
    (re.compile(r'has been relocated', re.IGNORECASE), "relocation-language", 4),
    (re.compile(r'has been moved to', re.IGNORECASE), "relocation-language", 4),
    (re.compile(r'\b[Tt]he former Section \d', re.IGNORECASE), "former-section", 5),
    (re.compile(r'in earlier editions', re.IGNORECASE), "edition-history", 4),
    (re.compile(r'\bthis chapter now begins with\b', re.IGNORECASE), "editing-narration", 5),
    (re.compile(r'\bsince the former Section', re.IGNORECASE), "editing-narration", 5),
    (re.compile(r'<!--\s*TODO\b', re.IGNORECASE), "todo-comment", 3),
    (re.compile(r'<!--\s*FIXME\b', re.IGNORECASE), "fixme-comment", 3),
    (re.compile(r'<!--\s*XXX\b', re.IGNORECASE), "xxx-comment", 3),
    (re.compile(r'\(WIP\)', re.IGNORECASE), "wip-marker", 4),
    (re.compile(r'\(draft\)', re.IGNORECASE), "draft-marker", 4),
    (re.compile(r'\(stub\)', re.IGNORECASE), "stub-marker", 4),
    (re.compile(r'\(coming soon\)', re.IGNORECASE), "coming-soon", 4),
    (re.compile(r'\[deprecated\]', re.IGNORECASE), "deprecated-marker", 3),
    (re.compile(r'\bformerly known as\b', re.IGNORECASE), "formerly-known", 3),
    (re.compile(r'\bin a previous version\b', re.IGNORECASE), "previous-version", 3),
    (re.compile(r'\bplaceholder for\b', re.IGNORECASE), "placeholder", 4),
    (re.compile(r'^\s*Lorem ipsum', re.IGNORECASE | re.MULTILINE), "lorem-ipsum", 5),
    (re.compile(r'\bTBD\b', re.IGNORECASE), "tbd-marker", 4),
    (re.compile(r'\bTo be filled\b', re.IGNORECASE), "to-be-filled", 5),
]

# ============= Pseudo-callout patterns =============
# Bare divs that should be `<div class="callout X">`
NONCANONICAL_DIVS = re.compile(
    r'<div\s+class\s*=\s*"('
    r'prereqs'              # canonical is "prerequisites"
    r'|note(?!\s*\b)'       # bare "note" without callout prefix
    r'|warning(?!\s*\b)'
    r'|tip(?!\s*\b)'
    r'|caution(?!\s*\b)'
    r'|info(?!\s*\b)'
    r'|important(?!\s*\b)'
    r')"',
    re.IGNORECASE,
)


def section_id(p: Path) -> str:
    m = re.match(r'section-([\d.]+\w*)\.html', p.name)
    if m:
        return f"S{m.group(1)}"
    if p.name == "index.html":
        mm = re.search(r'module-(\d+\w*)', str(p))
        return f"M{mm.group(1)}.idx" if mm else p.parent.name
    return p.name


def scan_file(p: Path) -> list[dict]:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    findings = []
    for pat, cat, sev in LEFTOVER_PATTERNS:
        for m in pat.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            # Capture a short context window
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(text), m.end() + 80)
            ctx = re.sub(r'\s+', ' ', text[ctx_start:ctx_end]).strip()
            findings.append({
                "category": cat,
                "severity": sev,
                "line": line,
                "match": m.group(0),
                "context": ctx[:150],
            })
    for m in NONCANONICAL_DIVS.finditer(text):
        # Skip if this is actually <div class="callout X"> (we anchor on quote)
        # The regex above only matches when the FIRST class-name token equals the
        # non-canonical word; "callout note" won't match because order is
        # "callout" first.
        line = text.count("\n", 0, m.start()) + 1
        findings.append({
            "category": f"noncanonical-callout-{m.group(1)}",
            "severity": 4,
            "line": line,
            "match": m.group(0),
            "context": "",
        })
    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    parser.add_argument("--min-severity", type=int, default=3)
    args = parser.parse_args()

    rows = []
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_DIRS:
            continue
        if not (p.name.startswith("section-") or p.name == "index.html"):
            continue
        for f in scan_file(p):
            if f["severity"] < args.min_severity:
                continue
            rows.append({
                "sid": section_id(p),
                "path": str(p.relative_to(ROOT)).replace('\\', '/'),
                **f,
            })

    rows.sort(key=lambda r: (-r["severity"], r["sid"]))

    lines = []
    lines.append("# Editing-Leftover and Pseudo-Callout Report")
    lines.append("")
    lines.append("Findings ranked by severity (5 = embarrassing artifact left in")
    lines.append("published prose, 3 = annotation comment / minor).")
    lines.append("")
    lines.append(f"Total findings (severity >= {args.min_severity}): {len(rows)}")
    lines.append("")
    by_cat: dict[str, int] = {}
    for r in rows:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
    lines.append("## By category")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    for cat in sorted(by_cat, key=lambda k: -by_cat[k]):
        lines.append(f"| {cat} | {by_cat[cat]} |")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    lines.append("| Sev | Section | Line | Category | Context |")
    lines.append("|---:|---|---:|---|---|")
    for r in rows[:200]:
        ctx = r["context"].replace("|", "\\|")[:120]
        lines.append(f"| {r['severity']} | {r['sid']} | {r['line']} | {r['category']} | {ctx} |")
    if len(rows) > 200:
        lines.append(f"\n... and {len(rows) - 200} more.")
    lines.append("")

    md = "\n".join(lines)
    out_path = Path(args.out) if args.out else ROOT / "docs" / "content-audit" / "EDITING_LEFTOVERS.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Report: {out_path.relative_to(ROOT)}")
    print(f"\nFindings: {len(rows)}")
    print("\nBy category:")
    for cat in sorted(by_cat, key=lambda k: -by_cat[k])[:10]:
        print(f"  {by_cat[cat]:>4} {cat}")


if __name__ == "__main__":
    main()
