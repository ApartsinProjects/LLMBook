"""Refined bibliography audit, capturing:
- heading level (h2 vs h3) for 'Further Reading'
- bib-meta span presence / consistency
- bib-category usage
- bib-annotation usage
- empty bibs (heading present, zero entries)
- variant containers (section.bibliography vs div.bibliography)
- non-card variants (ul.bibliography-list, table.comparison-table)
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {
    "node_modules", ".git", "KDP/output", "KDP/build", "KDP/html2epub",
    "pagefind", "temp_epub", "backup", "source_fix_backups",
}

H_BIB = re.compile(
    r'<h([23])\b[^>]*>\s*(Further Reading|Bibliography|References|Citations|Sources|Works Cited|Read more|Suggested Reading|Recommended Reading)\s*</h\1>',
    re.IGNORECASE,
)

WRAP_OPEN = re.compile(
    r'<(div|section)\b[^>]*\bclass\s*=\s*"([^"]*)"[^>]*>\s*$',
    re.IGNORECASE,
)


def should_skip(p: Path) -> bool:
    rel = p.relative_to(REPO).as_posix()
    return any(rel == s or rel.startswith(s + "/") for s in SKIP_DIRS)


def find_section_extent(html: str, hm: re.Match) -> str:
    """Body from end of heading to next h1/h2/h3 at same/higher level (use h1-h3 cutoff)."""
    start = hm.end()
    cutoff = re.compile(r'<h[1-3]\b', re.IGNORECASE)
    m = cutoff.search(html, start)
    return html[start:m.start() if m else len(html)]


def classify(body: str) -> str:
    if 'class="bib-entry-card"' in body or "class='bib-entry-card'" in body:
        return "bib-entry-card"
    if 'class="bibliography-list"' in body:
        return "ul-bibliography-list"
    if 'class="bib-list"' in body:
        return "ul-bib-list"
    if 'class="references"' in body:
        return "references-class"
    if 'class="bib-ref"' in body and 'class="bib-entry-card"' not in body:
        return "bib-ref-only"
    if 'class="comparison-table"' in body:
        return "comparison-table"
    if re.search(r'<li\b', body, re.I):
        return "plain-ul-li"
    if body.strip() == "" or len(re.sub(r'<[^>]+>', '', body).strip()) < 10:
        return "empty"
    return "other"


def find_outer_wrapper(html: str, hm: re.Match) -> tuple[str | None, str | None]:
    """Look backwards from heading for the most recent <div|section class=...> open tag."""
    pre = html[max(0, hm.start() - 1500):hm.start()]
    matches = list(re.finditer(r'<(div|section)\b[^>]*class="([^"]+)"[^>]*>', pre, re.I))
    if not matches:
        return None, None
    tag, classes = matches[-1].group(1), matches[-1].group(2)
    return tag.lower(), classes


def main():
    bibs = []
    for html_path in REPO.rglob("*.html"):
        if should_skip(html_path):
            continue
        try:
            html = html_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = html_path.relative_to(REPO).as_posix()
        for hm in H_BIB.finditer(html):
            level = int(hm.group(1))
            label = hm.group(2)
            body = find_section_extent(html, hm)
            tag, classes = find_outer_wrapper(html, hm)
            variant = classify(body)

            entry_count = (
                len(re.findall(r'class="bib-entry-card"', body))
                if variant == "bib-entry-card"
                else len(re.findall(r'<li\b', body, re.I))
                if "ul-" in variant or variant == "plain-ul-li"
                else len(re.findall(r'<tr\b', body, re.I)) - 1
                if variant == "comparison-table"
                else 0
            )
            bib_meta = len(re.findall(r'class="bib-meta"', body))
            bib_annotation = len(re.findall(r'class="bib-annotation"', body))
            bib_category = len(re.findall(r'class="bib-category"', body))
            bib_note = len(re.findall(r'class="bib-note"', body))
            bib_ref = len(re.findall(r'class="bib-ref"', body))
            inline_icons = sum(
                body.count(ic) for ic in [
                    "\U0001F4DA", "\U0001F4D6", "\U0001F4DD", "\U0001F4D2",
                    "\U0001F4D1", "\U0001F4D3", "\U0001F4D4",
                    "\U0001F4C4",  # page-facing-up icon (used in 'Paper' label)
                ]
            )
            bibs.append({
                "file": rel,
                "label": label,
                "h_level": level,
                "variant": variant,
                "outer_tag": tag,
                "outer_classes": classes,
                "entry_count": entry_count,
                "bib_ref": bib_ref,
                "bib_meta": bib_meta,
                "bib_annotation": bib_annotation,
                "bib_category": bib_category,
                "bib_note": bib_note,
                "inline_icons": inline_icons,
            })
    return bibs


def render(bibs):
    out = []
    out.append("# Bibliography Audit\n")
    out.append("_Repository: `E:/Projects/BookBlogsHome/LLMBook`. Generated 2026-05-15._\n")
    out.append(
        "_Scope: every `<h2>`/`<h3>` whose text matches Further Reading, Bibliography, References, Citations, Sources, etc., and the markup that follows._\n"
    )

    out.append(f"\n## Headline numbers\n")
    out.append(f"- **Total bibliography sections found:** {len(bibs)}")
    label_counts = Counter(b["label"] for b in bibs)
    out.append(f"- **Distinct heading texts used:** {len(label_counts)}")
    h2 = sum(1 for b in bibs if b["h_level"] == 2)
    h3 = sum(1 for b in bibs if b["h_level"] == 3)
    out.append(f"- **Heading levels:** `<h2>` = {h2}, `<h3>` = {h3}")

    out.append("\n## Distribution by heading name\n")
    out.append("| Heading text | Count |\n|---|---|")
    for k, v in label_counts.most_common():
        out.append(f"| {k} | {v} |")

    out.append("\n## Distribution by markup variant\n")
    variant_counts = Counter(b["variant"] for b in bibs)
    out.append("| Variant | Count |\n|---|---|")
    for k, v in variant_counts.most_common():
        out.append(f"| `{k}` | {v} |")

    out.append("\n## Outer wrapper tag and class\n")
    wrappers = Counter((b["outer_tag"], b["outer_classes"]) for b in bibs)
    out.append("| Tag | Classes | Count |\n|---|---|---|")
    for (tag, classes), v in wrappers.most_common(10):
        out.append(f"| `{tag}` | `{classes}` | {v} |")

    # Annotation / meta / category usage among the dominant card variant
    cards = [b for b in bibs if b["variant"] == "bib-entry-card"]
    n_cards = len(cards)
    with_meta = sum(1 for b in cards if b["bib_meta"] > 0)
    full_meta = sum(1 for b in cards if b["bib_meta"] >= b["entry_count"] and b["entry_count"] > 0)
    no_meta = sum(1 for b in cards if b["bib_meta"] == 0)
    with_anno = sum(1 for b in cards if b["bib_annotation"] > 0)
    with_cat = sum(1 for b in cards if b["bib_category"] > 0)

    out.append(f"\n## Sub-element coverage among the dominant `bib-entry-card` variant ({n_cards} sections)\n")
    out.append("| Sub-element | Sections using it | Notes |\n|---|---|---|")
    out.append(f"| `bib-ref` (entry title link) | {sum(1 for b in cards if b['bib_ref'] > 0)} | Should be every card. |")
    out.append(f"| `bib-annotation` (1-line gloss) | {with_anno} | Roughly the descriptive 'why read it' line. |")
    out.append(f"| `bib-meta` (e.g. emoji + 'Paper'/'Documentation') | {with_meta} ({with_meta-full_meta} partial, {full_meta} full) | {no_meta} sections **omit it entirely**. |")
    out.append(f"| `bib-category` (mini section group) | {with_cat} | Used to group entries; not all sections do. |")

    # Empty bibliographies
    empty = [b for b in bibs if b["variant"] == "empty"]
    out.append(f"\n## Empty bibliography sections ({len(empty)})\n")
    out.append("These have a `<h3>Further Reading</h3>` heading inside `<section class=\"bibliography\">` but no entries:\n")
    out.append("| File |\n|---|")
    for b in sorted(empty, key=lambda x: x["file"]):
        out.append(f"| `{b['file']}` |")

    # Non-card non-empty variants
    odd = [b for b in bibs if b["variant"] not in {"bib-entry-card", "empty"}]
    out.append(f"\n## Non-card non-empty variants ({len(odd)})\n")
    if odd:
        out.append("| File | Variant | Entries | Notes |\n|---|---|---|---|")
        for b in sorted(odd, key=lambda x: (x["variant"], x["file"])):
            note = ""
            if b["variant"] == "ul-bibliography-list":
                note = "Uses `<ul class=\"bibliography-list\">` with `<li><strong>Author (YEAR)</strong>...</li>` style."
            elif b["variant"] == "comparison-table":
                note = "Uses a `<table class=\"comparison-table\">` Topic/Paper/Why Read columns."
            out.append(f"| `{b['file']}` | `{b['variant']}` | {b['entry_count']} | {note} |")

    # Top inconsistencies summary
    out.append("\n## Top inconsistencies\n")
    out.append("1. **Heading text is uniform** (every section says `Further Reading`), but the **heading level varies**: "
               f"`<h3>` = {h3}, `<h2>` = {h2}. All sections should pick one level.")
    if odd:
        out.append(f"2. **Three competing markup styles for entries**: the dominant `bib-entry-card` "
                   f"({n_cards} sections), `ul-bibliography-list` ({sum(1 for b in odd if b['variant']=='ul-bibliography-list')}), "
                   f"and the one-off `comparison-table` ({sum(1 for b in odd if b['variant']=='comparison-table')}). "
                   f"This produces visibly different rendering (boxed cards vs bulleted list vs table).")
    if empty:
        out.append(f"3. **{len(empty)} empty bibliographies**: heading present but no entries. These are "
                   f"placeholders that should be either populated or removed (concentrated in Part 6 agentic-ai "
                   f"modules 22/23/25 and the Part-1/2 module `index.html` files).")
    out.append(f"4. **`bib-meta` icon-tag is inconsistent**: {full_meta} card sections use it on every entry, "
               f"{with_meta-full_meta} use it on some entries, and {no_meta} omit it entirely. The icon (e.g. \U0001F4C4 Paper, "
               f"\U0001F4D6 Documentation) appears or disappears unpredictably between chapters.")
    out.append(f"5. **`bib-category` grouping is optional**: {with_cat} of {n_cards} card sections group entries with "
               f"`<div class=\"bib-category\">`. Readers in those chapters see grouped subsections; in others, the "
               f"references are an undifferentiated list.")

    # Missing bibliography sections
    bib_files = {b["file"] for b in bibs}
    missing = []
    for p in REPO.rglob("section-*.html"):
        if should_skip(p):
            continue
        rel = p.relative_to(REPO).as_posix()
        if "front-matter" in rel:
            continue
        size = p.stat().st_size
        if size >= 30000 and rel not in bib_files:
            missing.append((rel, round(size / 1024, 1)))

    out.append(f"\n## Substantive section files (>30 KB) with no bibliography heading ({len(missing)})\n")
    if missing:
        out.append("| File | Size (KB) |\n|---|---|")
        for rel, sz in sorted(missing, key=lambda x: -x[1])[:50]:
            out.append(f"| `{rel}` | {sz} |")
        if len(missing) > 50:
            out.append(f"\n_...and {len(missing)-50} more._")

    # Canonical pattern recommendation
    out.append("\n## Recommended canonical pattern\n")
    out.append(
        "Based on the dominant usage:\n\n"
        "```html\n"
        '<section class="bibliography">\n'
        '  <h3>Further Reading</h3>\n'
        '  <div class="bib-category">Optional Group Label</div>\n'
        '  <div class="bib-entry-card">\n'
        '    <p class="bib-ref"><a href="..." rel="noopener" target="_blank">Author, A. (YEAR). \"Title.\" <em>Venue</em>.</a></p>\n'
        '    <p class="bib-annotation">One-sentence gloss of why this matters.</p>\n'
        '    <span class="bib-meta">\U0001F4C4 Paper</span>\n'
        '  </div>\n'
        '  <!-- additional cards... -->\n'
        '</section>\n'
        "```\n\n"
        "Fix list, in priority order:\n"
        f"1. Standardize heading on `<h3>Further Reading</h3>` (already used by {h3} of {len(bibs)} sections).\n"
        f"2. Convert the {sum(1 for b in odd if b['variant']=='ul-bibliography-list')} `ul.bibliography-list` sections and the "
        f"{sum(1 for b in odd if b['variant']=='comparison-table')} `comparison-table` section to `bib-entry-card` cards.\n"
        f"3. Populate or remove the {len(empty)} empty bibliographies.\n"
        f"4. Decide whether `bib-meta` icon-tags are required or removed, and apply uniformly across all cards.\n"
        f"5. Decide whether to keep `bib-category` grouping; if yes, mandate it; if no, drop the {with_cat} that have it.\n"
    )

    return "\n".join(out) + "\n"


if __name__ == "__main__":
    bibs = main()
    out = render(bibs)
    (REPO / "KDP" / "build" / "AUDIT_bibliography.md").write_text(out, encoding="utf-8")
    (REPO / "KDP" / "build" / "AUDIT_bibliography.json").write_text(
        json.dumps({"total": len(bibs), "bibs": bibs}, indent=2),
        encoding="utf-8",
    )
    print("wrote audit")
    print(f"total bibs: {len(bibs)}")
