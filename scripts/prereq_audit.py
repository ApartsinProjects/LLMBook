"""Prerequisite-correctness audit.

For each prereq callout in the book, verify:
  1. The link target EXISTS (no 404s)
  2. The target is EARLIER in the book reading order (a prereq should
     be back-pointing, not forward-pointing)
  3. The descriptive text matches the actual section title (no stale
     references like "Section 13.1: LoRA" pointing to a section that
     was retitled or moved)

The book's reading order is:
  front-matter -> part-1/module-00 -> part-1/module-01 -> ...
  -> part-K/module-N -> appendices

A prereq inside section X.Y.Z should point to ANY earlier file in that
total order, OR to a same-chapter earlier section (e.g. X.Y.Z prereq
can point to X.Y.W where W < Z).

Outputs docs/content-audit/PREREQ_AUDIT.md with categorized findings.
"""
from __future__ import annotations

import argparse
import html as html_mod
import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts"}

PREREQ_BLOCK_RE = re.compile(
    r'<div\s+class="(?:callout\s+)?prerequisites"[^>]*>(.*?)</div>',
    re.DOTALL | re.IGNORECASE,
)
LINK_RE = re.compile(r'<a\s+[^>]*href="([^"#]+)(?:#[^"]*)?"[^>]*>(.*?)</a>',
                      re.IGNORECASE | re.DOTALL)
TITLE_RE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')


def visible(s: str) -> str:
    return re.sub(r'\s+', ' ', html_mod.unescape(TAG_RE.sub(' ', s))).strip()


def section_order(p: Path) -> tuple[int, int, int]:
    """Returns sortable tuple (part_num, module_num, section_decimal)."""
    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    part_m = re.search(r'part-(\d+)', rel)
    mod_m = re.search(r'module-(\d+)', rel)
    sec_m = re.search(r'section-(\d+)\.(\d+)', p.name)
    part_n = int(part_m.group(1)) if part_m else 0
    mod_n = int(mod_m.group(1)) if mod_m else 0
    sec_major = int(sec_m.group(1)) if sec_m else 0
    sec_minor = int(sec_m.group(2)) if sec_m else 0
    # Heuristic: a section's order is (part, module, major*100 + minor)
    return (part_n, mod_n, sec_major * 100 + sec_minor)


def gather() -> dict[Path, tuple[int, int, int]]:
    """Return all section + index files keyed by absolute path, sorted by reading order."""
    out: dict[Path, tuple[int, int, int]] = {}
    for p in ROOT.rglob("*.html"):
        if set(p.parts) & SKIP_DIRS:
            continue
        if not (p.name.startswith("section-") or p.name == "index.html"):
            continue
        out[p.resolve()] = section_order(p)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    order_map = gather()
    findings = {
        "missing_target": [],
        "forward_pointing": [],
        "stale_title": [],
        "no_prereq_block": [],
    }

    for p in sorted(order_map):
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        my_order = order_map[p]
        rel = str(p.relative_to(ROOT)).replace('\\', '/')

        block_m = PREREQ_BLOCK_RE.search(html)
        if not block_m:
            # Only flag sections (not index) without prereqs
            if p.name.startswith("section-"):
                findings["no_prereq_block"].append({
                    "section": rel,
                    "issue": "no prerequisites block",
                })
            continue

        block_html = block_m.group(1)
        for lm in LINK_RE.finditer(block_html):
            href = lm.group(1)
            link_text = visible(lm.group(2))
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target = (p.parent / unquote(href)).resolve()
            if target not in order_map:
                findings["missing_target"].append({
                    "section": rel,
                    "href": href,
                    "link_text": link_text[:60],
                    "issue": "target file does not exist",
                })
                continue
            target_order = order_map[target]
            # Forward-pointing check: prereq target should be <= my_order
            # Allow same-chapter earlier sections OR any earlier chapter
            if target_order > my_order:
                findings["forward_pointing"].append({
                    "section": rel,
                    "href": href,
                    "link_text": link_text[:60],
                    "issue": f"prereq points FORWARD: target is at {target_order}, "
                             f"this section is at {my_order}",
                })
            # Stale-title check: extract target h1 title and compare to link_text
            try:
                target_html = target.read_text(encoding="utf-8", errors="replace")
                tm = TITLE_RE.search(target_html)
                if tm:
                    target_title = visible(tm.group(1))
                    # Heuristic: if link_text mentions a section number or topic
                    # that doesn't appear in the target's h1, flag as stale.
                    # Skip if link_text is generic like "Chapter X" or just "Section X.Y"
                    if (len(link_text) > 12
                            and not re.match(r'^(?:Chapter|Section)\s+[\d.]+(?:\s+\(.+\))?$', link_text)
                            and link_text.lower() not in target_title.lower()
                            and target_title.lower() not in link_text.lower()):
                        # Quick same-word overlap check; if zero word overlap, flag
                        text_words = set(re.findall(r'\b\w{4,}\b', link_text.lower()))
                        title_words = set(re.findall(r'\b\w{4,}\b', target_title.lower()))
                        if text_words and not (text_words & title_words):
                            findings["stale_title"].append({
                                "section": rel,
                                "href": href,
                                "link_text": link_text[:60],
                                "target_title": target_title[:60],
                                "issue": "link text and target h1 share no significant words",
                            })
            except OSError:
                pass

    # Render
    lines = []
    lines.append("# Prerequisite-Correctness Audit")
    lines.append("")
    total = sum(len(v) for v in findings.values())
    lines.append(f"Total findings: {total}")
    lines.append("")
    for cat in ("missing_target", "forward_pointing", "stale_title", "no_prereq_block"):
        lst = findings[cat]
        lines.append(f"## {cat.replace('_', ' ').title()} ({len(lst)} findings)")
        lines.append("")
        if not lst:
            lines.append("None.")
            lines.append("")
            continue
        lines.append("| Section | href | link text | issue |")
        lines.append("|---|---|---|---|")
        for f in lst[:80]:
            ht = f.get("link_text", "")[:50].replace("|", "\\|")
            href = f.get("href", "")[:60].replace("|", "\\|")
            lines.append(f"| {f['section']} | {href} | {ht} | {f.get('issue', '')[:80]} |")
        if len(lst) > 80:
            lines.append(f"\n... and {len(lst) - 80} more.")
        lines.append("")

    md = "\n".join(lines)
    out_path = Path(args.out) if args.out else ROOT / "docs" / "content-audit" / "PREREQ_AUDIT.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Report: {out_path.relative_to(ROOT)}")
    print(f"\nFindings:")
    for cat, lst in findings.items():
        print(f"  {cat}: {len(lst)}")


if __name__ == "__main__":
    main()
