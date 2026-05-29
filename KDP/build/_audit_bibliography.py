"""Audit bibliography sections across the LLMBook for look-and-feel consistency."""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {
    "node_modules",
    ".git",
    "KDP/output",
    "KDP/build",
    "KDP/html2epub",
    "pagefind",
    "temp_epub",
    "backup",
    "source_fix_backups",
}

# Headings that may signal a bibliography section
HEADING_PATTERNS = [
    "Further Reading",
    "Bibliography",
    "References",
    "Citations",
    "Sources",
    "Works Cited",
    "Read more",
    "Suggested Reading",
    "Recommended Reading",
]

# Markup patterns to scan for
MARKUP_PATTERNS = {
    "bib-ref": re.compile(r'class="[^"]*\bbib-ref\b[^"]*"'),
    "bib-entry-card": re.compile(r'class="[^"]*\bbib-entry-card\b[^"]*"'),
    "bib-entry": re.compile(r'class="[^"]*\bbib-entry\b[^"]*"'),
    "bib-list": re.compile(r'class="[^"]*\bbib-list\b[^"]*"'),
    "bibliography": re.compile(r'class="[^"]*\bbibliography\b[^"]*"'),
    "references_class": re.compile(r'class="[^"]*\breferences\b[^"]*"'),
    "further-reading": re.compile(r'class="[^"]*\bfurther-reading\b[^"]*"'),
}

# Heading pattern: H2 or H3 with the right text
H2H3 = re.compile(
    r'<h([23])\b[^>]*>(.*?)</h\1>', re.IGNORECASE | re.DOTALL
)

# Emoji / icon list (common ones seen on bibliography entries)
ICONS = ["\U0001F4DA", "\U0001F4D6", "\U0001F4DD", "\U0001F4D2", "\U0001F4D1", "\U0001F4D3", "\U0001F4D4"]


def should_skip(path: Path) -> bool:
    rel = path.relative_to(REPO).as_posix()
    for sk in SKIP_DIRS:
        if rel == sk or rel.startswith(sk + "/"):
            return True
    return False


def normalize_heading(text: str) -> str:
    """Strip tags/whitespace from heading inner HTML."""
    t = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def classify_heading(text: str) -> str | None:
    """Return canonical heading name if this looks like a bibliography heading."""
    t = text.lower()
    # Strip leading numbering like "5.4.1" or "Section 5.4"
    t = re.sub(r'^[\d\.\s]+', '', t)
    t = re.sub(r'^section\s+[\d\.]+\s*[:\-]?\s*', '', t)
    t = t.strip()
    if not t:
        return None
    candidates = {
        "further reading": "Further Reading",
        "further readings": "Further Reading",
        "bibliography": "Bibliography",
        "references": "References",
        "citations": "Citations",
        "sources": "Sources",
        "works cited": "Works Cited",
        "read more": "Read more",
        "suggested reading": "Suggested Reading",
        "recommended reading": "Recommended Reading",
        "suggested readings": "Suggested Reading",
    }
    return candidates.get(t)


def extract_section_after_heading(html: str, heading_match: re.Match) -> str:
    """Return content from end of heading until next heading at same/higher level
    or end of document."""
    start = heading_match.end()
    level = int(heading_match.group(1))
    # Find next heading at level <= current
    next_pattern = re.compile(
        r'<h([1-' + str(level) + r'])\b', re.IGNORECASE
    )
    m = next_pattern.search(html, start)
    end = m.start() if m else len(html)
    return html[start:end]


def detect_markup(section: str) -> dict:
    """Detect which bib markup classes are present and counts."""
    found = {}
    for name, pat in MARKUP_PATTERNS.items():
        cnt = len(pat.findall(section))
        if cnt:
            found[name] = cnt
    return found


def count_icons(section: str) -> int:
    n = 0
    for ic in ICONS:
        n += section.count(ic)
    return n


def count_li(section: str) -> int:
    return len(re.findall(r'<li\b', section, re.IGNORECASE))


def detect_wrapper_class(section: str, heading_match: re.Match, html: str) -> str | None:
    """Look at the parent wrapper just before/after the heading to spot a container class."""
    # Inspect a 200-char window before heading and 200 after for class attribute
    start = max(0, heading_match.start() - 400)
    pre = html[start:heading_match.start()]
    # Find the last opening tag in `pre`
    tags = re.findall(r'<(\w+)\b[^>]*class="([^"]+)"[^>]*>', pre)
    if tags:
        last_tag, last_class = tags[-1]
        for cand in ("bibliography", "bib-list", "references", "further-reading", "bib-entry-card-grid"):
            if cand in last_class.split():
                return cand
    return None


def main():
    bibs = []
    files_scanned = 0
    files_with_bib = 0

    for html_path in REPO.rglob("*.html"):
        if should_skip(html_path):
            continue
        files_scanned += 1
        try:
            html = html_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        rel = html_path.relative_to(REPO).as_posix()
        found_any = False

        for hm in H2H3.finditer(html):
            heading_text = normalize_heading(hm.group(2))
            canonical = classify_heading(heading_text)
            if not canonical:
                continue

            section_body = extract_section_after_heading(html, hm)
            markup = detect_markup(section_body)
            icons = count_icons(section_body)
            li_count = count_li(section_body)
            wrapper = detect_wrapper_class(section_body, hm, html)

            # Determine primary markup pattern
            patterns_present = list(markup.keys())
            if "bib-entry-card" in markup:
                primary = "bib-entry-card"
            elif "bib-ref" in markup:
                primary = "bib-ref"
            elif "bib-entry" in markup:
                primary = "bib-entry"
            elif li_count > 0 and not markup:
                primary = "plain-ul-li"
            else:
                primary = "other-or-empty"

            # Count entries
            if primary == "bib-entry-card":
                entry_count = markup.get("bib-entry-card", 0)
            elif primary == "bib-ref":
                entry_count = markup.get("bib-ref", 0)
            elif primary == "bib-entry":
                entry_count = markup.get("bib-entry", 0)
            elif primary == "plain-ul-li":
                entry_count = li_count
            else:
                entry_count = 0

            bibs.append({
                "file": rel,
                "heading_level": int(hm.group(1)),
                "heading_text": heading_text,
                "canonical": canonical,
                "primary_markup": primary,
                "wrapper_class": wrapper,
                "markup_counts": markup,
                "icons": icons,
                "li_count": li_count,
                "entry_count": entry_count,
            })
            found_any = True

        if found_any:
            files_with_bib += 1

    return bibs, files_scanned, files_with_bib


def deduplicate_per_file(bibs):
    """If multiple bibliography headings appear in the same file, keep all but mark them."""
    counts = Counter(b["file"] for b in bibs)
    for b in bibs:
        b["multi_in_file"] = counts[b["file"]] > 1
    return bibs


def page_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except Exception:
        return 0


def find_missing_bibs(bibs, threshold_bytes: int = 30000):
    """Find files with substantial content but no bibliography section.

    threshold_bytes ~ approximation for ">5 pages" of substantive content.
    """
    bib_files = {b["file"] for b in bibs}
    candidates = []
    for html_path in REPO.rglob("*.html"):
        if should_skip(html_path):
            continue
        rel = html_path.relative_to(REPO).as_posix()
        # Only audit substantive section files
        name = html_path.name.lower()
        # Likely section files
        if not (
            re.match(r'^section-[\w\.\-]+\.html$', name)
            or name == "index.html"
        ):
            continue
        # Skip top-level/toc/front-matter index summaries
        if rel in {"index.html", "toc.html"}:
            continue
        if "front-matter" in rel:
            continue
        size = page_size(html_path)
        if size >= threshold_bytes and rel not in bib_files:
            candidates.append({"file": rel, "size_kb": round(size / 1024, 1)})
    return candidates


def render_report(bibs, files_scanned, files_with_bib, missing):
    by_canon = Counter(b["canonical"] for b in bibs)
    by_primary = Counter(b["primary_markup"] for b in bibs)
    by_wrapper = Counter(b["wrapper_class"] or "(none)" for b in bibs)
    icons_present = sum(1 for b in bibs if b["icons"] > 0)
    icons_absent = sum(1 for b in bibs if b["icons"] == 0)

    # Per-canonical primary markup mix
    canon_to_primary = defaultdict(Counter)
    for b in bibs:
        canon_to_primary[b["canonical"]][b["primary_markup"]] += 1

    # Per primary markup -> headings
    primary_to_canon = defaultdict(Counter)
    for b in bibs:
        primary_to_canon[b["primary_markup"]][b["canonical"]] += 1

    out = []
    out.append("# Bibliography Audit\n")
    out.append(f"_Generated 2026-05-15. Scanned {files_scanned} HTML files; {files_with_bib} contain >=1 bibliography section._\n")
    out.append(f"\n**Total bibliography sections found:** {len(bibs)}\n")

    out.append("\n## Distribution by heading name\n")
    out.append("| Heading | Count |\n|---|---|")
    for k, v in by_canon.most_common():
        out.append(f"| {k} | {v} |")

    out.append("\n## Distribution by markup pattern\n")
    out.append("| Primary markup | Count |\n|---|---|")
    for k, v in by_primary.most_common():
        out.append(f"| `{k}` | {v} |")

    out.append("\n## Wrapper class on container\n")
    out.append("| Wrapper | Count |\n|---|---|")
    for k, v in by_wrapper.most_common():
        out.append(f"| `{k}` | {v} |")

    out.append("\n## Heading <-> markup cross-tab\n")
    out.append("| Heading | Markup | Count |\n|---|---|---|")
    for canon in sorted(canon_to_primary):
        for prim, cnt in canon_to_primary[canon].most_common():
            out.append(f"| {canon} | `{prim}` | {cnt} |")

    out.append(f"\n## Icon usage (book/page emoji prefixes on entries)\n")
    out.append(f"- Entries with at least one icon: **{icons_present}**")
    out.append(f"- Entries with no icons: **{icons_absent}**")

    # Top inconsistencies
    out.append("\n## Top inconsistencies\n")
    # 1. Mixed heading names
    canon_list = [k for k, _ in by_canon.most_common()]
    if len(canon_list) > 1:
        out.append(
            f"1. **Mixed heading names**: {', '.join([f'{k} ({by_canon[k]})' for k in canon_list])}. "
            f"Sections that use the same markup pattern but differ in heading title cause the reader to see "
            f"`{canon_list[0]}` in one chapter and `{canon_list[1]}` in another."
        )
    # 2. Mixed markup
    primary_list = [k for k, _ in by_primary.most_common() if k not in {"other-or-empty"}]
    if len(primary_list) > 1:
        out.append(
            f"2. **Mixed markup styles**: {', '.join([f'`{k}` ({by_primary[k]})' for k in primary_list])}. "
            f"`bib-ref` and `bib-entry-card` render with different visual weight; some sections list references as compact "
            f"`<p class=\"bib-ref\">` lines, others as full cards."
        )
    # 3. Wrappers
    wrapper_keys = [k for k in by_wrapper if k != "(none)"]
    if len(wrapper_keys) > 1:
        out.append(
            f"3. **Mixed wrapper classes**: {', '.join([f'`{k}` ({by_wrapper[k]})' for k in wrapper_keys])} "
            f"plus {by_wrapper.get('(none)', 0)} sections with no wrapper. The wrapper drives spacing and borders, so a missing or differently named "
            f"wrapper breaks the visual rhythm."
        )
    # 4. Icons
    if icons_present and icons_absent:
        out.append(
            f"4. **Inconsistent icon usage**: {icons_present} sections include book icons (e.g. {chr(0x1F4DA)} {chr(0x1F4D6)}) prefixing entries; "
            f"{icons_absent} omit them entirely."
        )
    # 5. Missing
    if missing:
        out.append(
            f"5. **Missing bibliography sections**: {len(missing)} substantive section files (>30 KB) lack any bibliography heading. "
            f"This makes references inconsistent across chapters."
        )

    out.append("\n## Recommended canonical pattern\n")
    # Pick canonical based on dominant choices
    top_heading = canon_list[0] if canon_list else "Further Reading"
    top_markup = primary_list[0] if primary_list else "bib-entry-card"
    top_wrapper = wrapper_keys[0] if wrapper_keys else "bibliography"
    out.append(
        f"- **Heading**: `<h2>{top_heading}</h2>` (already dominant: {by_canon[top_heading]} of {len(bibs)} sections)."
    )
    out.append(
        f"- **Wrapper**: `<div class=\"{top_wrapper}\">` (already dominant: {by_wrapper[top_wrapper]} sections)."
    )
    out.append(
        f"- **Entry markup**: `{top_markup}` (already dominant: {by_primary[top_markup]} sections). "
        f"Pick one of `bib-ref` (compact line) or `bib-entry-card` (card-style) and apply uniformly. "
        f"Recommend `bib-entry-card` because it gives author/year/title/URL each their own slot and matches the visual register of "
        f"sidebars/callouts used elsewhere in the book."
    )
    out.append(
        f"- **Icons**: pick one rule and stick to it. If keeping icons, prepend the same single icon to every entry; "
        f"otherwise strip all of them. Currently {icons_present}/{icons_absent} are mixed."
    )

    out.append("\n## Files missing a bibliography (substantive content)\n")
    if not missing:
        out.append("_(none found)_")
    else:
        out.append("| File | Size (KB) |\n|---|---|")
        for m in sorted(missing, key=lambda x: -x["size_kb"])[:40]:
            out.append(f"| `{m['file']}` | {m['size_kb']} |")
        if len(missing) > 40:
            out.append(f"\n_...and {len(missing) - 40} more._")

    # Detailed listing per non-dominant primary markup, for fix targeting
    out.append("\n## Sections to retrofit (non-dominant markup)\n")
    rare = [b for b in bibs if b["primary_markup"] != top_markup and b["primary_markup"] != "other-or-empty"]
    if not rare:
        out.append("_(none)_")
    else:
        out.append("| File | Heading | Markup | Entries |\n|---|---|---|---|")
        for b in sorted(rare, key=lambda x: x["file"])[:60]:
            out.append(
                f"| `{b['file']}` | {b['canonical']} | `{b['primary_markup']}` | {b['entry_count']} |"
            )
        if len(rare) > 60:
            out.append(f"\n_...and {len(rare) - 60} more._")

    # Detailed listing per non-dominant heading
    out.append("\n## Sections to retrofit (non-dominant heading)\n")
    rare_h = [b for b in bibs if b["canonical"] != top_heading]
    if not rare_h:
        out.append("_(none)_")
    else:
        out.append("| File | Heading | Markup |\n|---|---|---|")
        for b in sorted(rare_h, key=lambda x: x["file"])[:60]:
            out.append(
                f"| `{b['file']}` | {b['canonical']} | `{b['primary_markup']}` |"
            )
        if len(rare_h) > 60:
            out.append(f"\n_...and {len(rare_h) - 60} more._")

    return "\n".join(out) + "\n"


if __name__ == "__main__":
    bibs, files_scanned, files_with_bib = main()
    bibs = deduplicate_per_file(bibs)
    missing = find_missing_bibs(bibs)
    report = render_report(bibs, files_scanned, files_with_bib, missing)

    out_path = REPO / "KDP" / "build" / "AUDIT_bibliography.md"
    out_path.write_text(report, encoding="utf-8")

    # Also dump raw JSON for follow-up scripts
    raw_path = REPO / "KDP" / "build" / "AUDIT_bibliography.json"
    raw_path.write_text(json.dumps({
        "files_scanned": files_scanned,
        "files_with_bib": files_with_bib,
        "bibs": bibs,
        "missing": missing,
    }, indent=2), encoding="utf-8")

    print(f"Wrote report to {out_path}")
    print(f"Wrote raw data to {raw_path}")
    print(f"Total bib sections: {len(bibs)}")
    print(f"Files scanned: {files_scanned}, files with bib: {files_with_bib}")
