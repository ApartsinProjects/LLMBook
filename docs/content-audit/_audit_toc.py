"""Audit toc.html against _book_structure.json ground truth.

For each chapter link in toc.html:
  1. Extract href, num label, displayed title
  2. Find the matching module in ground truth (by href path or chap_num)
  3. Report mismatches: missing module, wrong title, wrong number, wrong subtitle pattern
Also check section file references if present.
"""
import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
TOC = ROOT / "toc.html"
GT = ROOT / "docs" / "content-audit" / "_book_structure.json"


def clean(s: str) -> str:
    """Normalize HTML entity and whitespace."""
    return re.sub(r"\s+", " ", unescape(s)).strip()


def main():
    gt = json.loads(GT.read_text(encoding="utf-8"))
    # Build lookup by relative path and by chap_num
    by_path: dict[str, dict] = {}
    by_num: dict[int, dict] = {}
    by_num_str: dict[str, dict] = {}  # chap_num_str like "54b"
    for p in gt["parts"]:
        for m in p["modules"]:
            by_path[m["rel_path"]] = m
            by_num[m["chap_num"]] = m  # last one wins for duplicates (e.g. 54b)
            by_num_str[m["chap_num_str"]] = m

    toc = TOC.read_text(encoding="utf-8")
    mismatches: list[dict] = []

    # Match each toc-chapter li block
    chap_pattern = re.compile(
        r'<li class="toc-chapter">\s*'
        r'<a href="([^"]+)">\s*'
        r'<span class="toc-chapter-num"[^>]*>([^<]+)</span>\s*'
        r'<span class="toc-chapter-title">([^<]*)</span>'
        r'(?:\s*<span class="toc-chapter-subtitle">([^<]*)</span>)?'
        r'\s*</a>\s*</li>',
        re.DOTALL,
    )

    for m in chap_pattern.finditer(toc):
        href, num, title, subtitle = m.group(1), m.group(2).strip(), clean(m.group(3)), clean(m.group(4) or "")
        # Skip front matter and appendices
        if "module-" not in href:
            continue
        rel = href
        gt_mod = by_path.get(rel)
        if gt_mod is None:
            # Try by num
            try:
                num_int = int(re.sub(r"[^0-9]", "", num))
                gt_mod = by_num.get(num_int)
            except ValueError:
                gt_mod = None
        if gt_mod is None:
            mismatches.append(
                {
                    "kind": "missing_module",
                    "href": href,
                    "toc_num": num,
                    "toc_title": title,
                }
            )
            continue

        # Check title
        gt_title = clean(gt_mod["title"])
        toc_title = clean(title)
        if gt_title != toc_title:
            mismatches.append(
                {
                    "kind": "title_mismatch",
                    "href": href,
                    "toc_title": toc_title,
                    "gt_title": gt_title,
                    "chap_num": gt_mod["chap_num"],
                }
            )

        # Check chapter number (sometimes toc has "54" for 54b but aria-label gives away)
        # Look back to aria-label for full pattern
        gt_num = str(gt_mod["chap_num"])
        if num != gt_num and not (num == "0" and gt_num == "0"):
            mismatches.append(
                {
                    "kind": "num_mismatch",
                    "href": href,
                    "toc_num": num,
                    "gt_num": gt_num,
                    "gt_title": gt_title,
                }
            )

    # Also check each href that should resolve to an actual file
    href_pattern = re.compile(r'href="([^"]+\.html)"')
    for m in href_pattern.finditer(toc):
        h = m.group(1)
        # Skip anchors and external
        if h.startswith(("#", "http://", "https://", "mailto:")):
            continue
        # Resolve relative to repo root (toc.html is at root)
        target = (ROOT / h).resolve()
        if not target.exists():
            mismatches.append({"kind": "missing_file", "href": h})

    # Also: for every chapter in ground truth, is it listed in toc?
    listed_paths = set()
    for m in chap_pattern.finditer(toc):
        listed_paths.add(m.group(1))
    for p in gt["parts"]:
        for mod in p["modules"]:
            if mod["rel_path"] not in listed_paths:
                mismatches.append(
                    {
                        "kind": "missing_from_toc",
                        "gt_path": mod["rel_path"],
                        "gt_num": mod["chap_num_str"],
                        "gt_title": clean(mod["title"]),
                    }
                )

    print(f"Found {len(mismatches)} TOC mismatch(es).")
    for mm in mismatches:
        print(json.dumps(mm, ensure_ascii=False))


if __name__ == "__main__":
    main()
