"""Table-class consistency audit (READ-ONLY).

Walks every .html file under the book root (excluding KDP/, .claude/,
node_modules/, build/, temp_*, scripts/, vendor/, templates/, etc.) and
records, for every <table>:

    - file path
    - approximate line number of the opening tag
    - class attribute value
    - inline style="..." override (if any)
    - explicit border="..." attribute (if any)
    - whether the table is wrapped in <center>
    - caption text (from <caption>, <figcaption>, <p|div class="table-caption">,
      or the immediately-preceding <p>/<h*> heuristic)
    - which caption mechanism was used
    - whether the caption uses a "Table N.N(.N): " prefix (and the captured id)
    - column count (max <td>/<th> per row)
    - whether the table has <thead>
    - whether the table has a <caption> element

Findings are written to ``table-class-audit.md`` and a short
console summary is printed.

Run from the project root:
    /c/Python314/python scripts/_audit_table_classes.py
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from bs4 import BeautifulSoup, Tag

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "table-class-audit.md"

SKIP_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "build", ".git", "__pycache__", "agents", "vendor", "downloads",
    "source_fix_backups", "images",
}
SKIP_PREFIXES = ("temp_",)
SKIP_NAME_FRAGMENTS = ("backups",)

TABLE_ID_RE = re.compile(r"\bTable\s+([A-Z]?\.?\d+(?:\.\d+)*)\s*[:—–-]", re.IGNORECASE)


def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    for part in p.parts:
        if part.startswith(SKIP_PREFIXES):
            return True
        if any(frag in part for frag in SKIP_NAME_FRAGMENTS):
            return True
    return False


def collect_html_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.rglob("*.html")):
        if should_skip(p):
            continue
        files.append(p)
    return files


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def make_line_index(text: str) -> list[int]:
    """Return a list where index i = byte/char offset of line i+1 start."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def offset_to_line(starts: list[int], offset: int) -> int:
    # Binary search.
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= offset:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


def find_table_offsets(text: str) -> list[int]:
    """Return char offsets of every '<table' opening (lowercase only)."""
    return [m.start() for m in re.finditer(r"<table\b", text, re.IGNORECASE)]


def column_count(tbl: Tag) -> int:
    max_cols = 0
    for tr in tbl.find_all("tr"):
        # Count <th>/<td> that are direct enough children (BS4 find_all on tr
        # is fine: nested tables are vanishingly rare in this book).
        n = sum(1 for c in tr.find_all(["th", "td"], recursive=False))
        if n == 0:
            # Fallback: some authors nest a <span> wrapper, count any descendant cell.
            n = len(tr.find_all(["th", "td"]))
        if n > max_cols:
            max_cols = n
    return max_cols


def gather_caption(tbl: Tag) -> tuple[str, str]:
    """Return (caption_text, caption_mechanism).

    Mechanism is one of:
      - "<caption>"
      - "<figcaption>"
      - "p.table-caption"
      - "div.table-caption"
      - "preceding-p"   (paragraph immediately before the table-container)
      - "none"
    """
    cap = tbl.find("caption", recursive=False)
    if cap is not None and cap.get_text(strip=True):
        return cap.get_text(" ", strip=True), "<caption>"

    # <figcaption> inside the same <figure> wrapper
    fig = tbl.find_parent("figure")
    if fig is not None:
        fc = fig.find("figcaption")
        if fc is not None and fc.get_text(strip=True):
            return fc.get_text(" ", strip=True), "<figcaption>"

    # table-container wrapper: look for sibling p.table-caption / div.table-caption
    container = tbl.find_parent(class_="table-container") or tbl.parent
    if container is not None:
        # First look inside the container.
        cand = container.find(attrs={"class": "table-caption"})
        if cand is not None and cand.get_text(strip=True):
            tag = cand.name
            return cand.get_text(" ", strip=True), f"{tag}.table-caption"
        # Then look at preceding siblings of the container.
        prev = container.previous_sibling
        seen = 0
        while prev is not None and seen < 4:
            if isinstance(prev, Tag):
                seen += 1
                cls = " ".join(prev.get("class", []))
                if "table-caption" in cls and prev.get_text(strip=True):
                    return prev.get_text(" ", strip=True), f"{prev.name}.table-caption"
                if prev.name == "p" and prev.get_text(strip=True):
                    txt = prev.get_text(" ", strip=True)
                    if TABLE_ID_RE.search(txt):
                        return txt, "preceding-p"
                    break
                if prev.name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                    break
            prev = prev.previous_sibling

    return "", "none"


def caption_id(text: str) -> str:
    m = TABLE_ID_RE.search(text)
    return m.group(1) if m else ""


def truncate(s: str, n: int = 80) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


# ----------------------------------------------------------------------
# Audit
# ----------------------------------------------------------------------

def audit_file(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [{"error": f"read failed: {exc}", "path": str(path)}]
    line_starts = make_line_index(text)
    offsets = find_table_offsets(text)

    soup = BeautifulSoup(text, "html.parser")
    tables = soup.find_all("table")

    results = []
    for idx, tbl in enumerate(tables):
        line_no = offset_to_line(line_starts, offsets[idx]) if idx < len(offsets) else 0
        classes = tbl.get("class", []) or []
        cls = " ".join(classes) if classes else ""
        style = tbl.get("style", "") or ""
        border = tbl.get("border", "") or ""
        has_thead = tbl.find("thead") is not None
        cap_tag = tbl.find("caption", recursive=False)
        has_caption_elem = cap_tag is not None and cap_tag.get_text(strip=True) != ""
        caption_text, caption_mech = gather_caption(tbl)
        tid = caption_id(caption_text)
        in_center = tbl.find_parent("center") is not None
        # Check if table-container wrapper used.
        in_container = tbl.find_parent(class_="table-container") is not None

        results.append({
            "path": path,
            "line": line_no,
            "class": cls,
            "style": style,
            "border": border,
            "in_center": in_center,
            "in_container": in_container,
            "cols": column_count(tbl),
            "has_thead": has_thead,
            "has_caption_elem": has_caption_elem,
            "caption_text": caption_text,
            "caption_mech": caption_mech,
            "table_id": tid,
        })
    return results


def relpath(p: Path) -> str:
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def render_md(records: list[dict]) -> str:
    by_class: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        if "error" in r:
            continue
        key = r["class"] or "(no class)"
        by_class[key].append(r)

    total = sum(len(v) for v in by_class.values())
    class_counts = Counter({k: len(v) for k, v in by_class.items()})

    cap_mech_counts: Counter = Counter()
    no_caption_count = 0
    no_thead_count = 0
    border_attr = []
    inline_style = []
    in_center = []
    no_container = []
    table_ids: Counter = Counter()
    dup_table_ids: dict[str, list[dict]] = defaultdict(list)

    for r in records:
        if "error" in r:
            continue
        cap_mech_counts[r["caption_mech"]] += 1
        if not r["has_caption_elem"]:
            no_caption_count += 1
        if not r["has_thead"]:
            no_thead_count += 1
        if r["border"]:
            border_attr.append(r)
        if r["style"]:
            inline_style.append(r)
        if r["in_center"]:
            in_center.append(r)
        if not r["in_container"]:
            no_container.append(r)
        if r["table_id"]:
            table_ids[r["table_id"]] += 1
            dup_table_ids[r["table_id"]].append(r)

    lines: list[str] = []
    lines.append("# Table-class consistency audit\n")
    lines.append(f"Total `<table>` elements scanned: **{total}**\n")
    lines.append("## Class distribution\n")
    lines.append("| Class | Count |")
    lines.append("|---|---|")
    for cls, n in class_counts.most_common():
        lines.append(f"| `{cls}` | {n} |")
    lines.append("")

    lines.append("## Caption mechanism distribution\n")
    lines.append("| Mechanism | Count |")
    lines.append("|---|---|")
    for mech, n in cap_mech_counts.most_common():
        lines.append(f"| `{mech}` | {n} |")
    lines.append("")
    lines.append(f"- Tables with **no `<caption>` element**: {no_caption_count}")
    lines.append(f"- Tables with **no `<thead>`**: {no_thead_count}")
    lines.append(f"- Tables with **explicit `border=` attribute**: {len(border_attr)}")
    lines.append(f"- Tables with **inline `style=` attribute**: {len(inline_style)}")
    lines.append(f"- Tables wrapped in `<center>`: {len(in_center)}")
    lines.append(f"- Tables **not** wrapped in `.table-container`: {len(no_container)}")
    lines.append("")

    # Detail each non-standard class.
    def dump(title: str, rows: list[dict]) -> None:
        lines.append(f"## {title}  ({len(rows)})\n")
        if not rows:
            lines.append("_None._\n")
            return
        lines.append("| File | Line | Cols | thead | caption-mech | caption (truncated) |")
        lines.append("|---|---:|---:|:-:|---|---|")
        for r in rows:
            lines.append(
                "| `{p}` | {ln} | {c} | {th} | `{m}` | {cap} |".format(
                    p=relpath(r["path"]),
                    ln=r["line"],
                    c=r["cols"],
                    th="Y" if r["has_thead"] else "n",
                    m=r["caption_mech"],
                    cap=truncate(r["caption_text"], 70).replace("|", "\\|") or "_(no caption)_",
                )
            )
        lines.append("")

    dump("class=`data-table` instances (non-standard grid)", by_class.get("data-table", []))
    dump("class=`comparison-table` instances (gradient title bar; keep as-is)",
         by_class.get("comparison-table", []))
    dump("class=`psk-table` instances (appendix problem-solution; keep as-is)",
         by_class.get("psk-table", []))

    # A sample of complex-table and unclassed (first 10 each) for comparison.
    ct = by_class.get("complex-table", [])
    dump("Sample: first 10 `class=complex-table` (the standard)", ct[:10])
    nc = by_class.get("(no class)", [])
    dump("Sample: first 10 tables with **no class**", nc[:10])

    # Tables with legacy/non-CSS borders.
    if border_attr:
        lines.append("## Legacy `border=` attribute on `<table>`\n")
        lines.append("| File | Line | class | border= |")
        lines.append("|---|---:|---|---|")
        for r in border_attr:
            lines.append(
                f"| `{relpath(r['path'])}` | {r['line']} | `{r['class'] or '(none)'}` | `{r['border']}` |"
            )
        lines.append("")

    if inline_style:
        lines.append("## Inline `style=` attribute on `<table>`\n")
        lines.append("| File | Line | class | style= |")
        lines.append("|---|---:|---|---|")
        for r in inline_style:
            lines.append(
                f"| `{relpath(r['path'])}` | {r['line']} | `{r['class'] or '(none)'}` | `{truncate(r['style'], 80)}` |"
            )
        lines.append("")

    if in_center:
        lines.append("## Tables wrapped in `<center>`\n")
        lines.append("| File | Line | class |")
        lines.append("|---|---:|---|")
        for r in in_center:
            lines.append(
                f"| `{relpath(r['path'])}` | {r['line']} | `{r['class'] or '(none)'}` |"
            )
        lines.append("")

    # Duplicate Table IDs across the book (sanity check).
    dups = {k: v for k, v in dup_table_ids.items() if len(v) > 1}
    if dups:
        lines.append("## Duplicate `Table N.N(.N)` captions across the book\n")
        for k in sorted(dups):
            lines.append(f"### Table {k}")
            for r in dups[k]:
                lines.append(f"- `{relpath(r['path'])}` line {r['line']}: {truncate(r['caption_text'], 90)}")
            lines.append("")

    # Caption-mechanism breakdown by class (helps see where inconsistency lives).
    lines.append("## Caption mechanism by table class\n")
    lines.append("| Class | <caption> | preceding-p | p/div.table-caption | <figcaption> | none |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for cls, rows in sorted(by_class.items(), key=lambda kv: -len(kv[1])):
        c = Counter(r["caption_mech"] for r in rows)
        ptc = c.get("p.table-caption", 0) + c.get("div.table-caption", 0)
        lines.append(
            f"| `{cls}` | {c.get('<caption>', 0)} | {c.get('preceding-p', 0)} | {ptc} | {c.get('<figcaption>', 0)} | {c.get('none', 0)} |"
        )
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    files = collect_html_files()
    print(f"Scanning {len(files)} HTML files...", flush=True)
    all_records: list[dict] = []
    for f in files:
        all_records.extend(audit_file(f))

    md = render_md(all_records)
    OUT_PATH.write_text(md, encoding="utf-8")

    # Console summary.
    class_counts = Counter(
        (r["class"] or "(no class)") for r in all_records if "error" not in r
    )
    print("Class distribution:")
    for cls, n in class_counts.most_common():
        print(f"  {cls:<20} {n}")
    total = sum(class_counts.values())
    print(f"  total tables:        {total}")
    print(f"Report written to: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
