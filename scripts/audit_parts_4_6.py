#!/usr/bin/env python3
"""Audit Parts 4, 5, 6 of LLMBook for five quality dimensions.

Read-only - emits a structured Markdown report.
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

# Canonical chapter titles from book_structure.yaml
PARTS = [
    ("part-4-training-adapting", "Part IV: Training and Adapting", {
        17: "Synthetic Data Generation & LLM Simulation",
        18: "Fine-Tuning Fundamentals",
        19: "Parameter-Efficient Fine-Tuning (PEFT)",
        20: "Alignment: RLHF, DPO & Preference Tuning",
        21: "Tools of the Trade: Training & Adaptation Stack",
    }),
    ("part-5-retrieval-conversation", "Part V: Retrieval and Conversation", {
        22: "Embeddings, Vector Databases & Semantic Search",
        23: "Retrieval-Augmented Generation (RAG)",
        24: "Building Conversational AI Systems",
        25: "Tools of the Trade: Retrieval & Conversation Stack",
    }),
    ("part-6-agentic-ai", "Part VI: Agentic AI", {
        26: "AI Agent Foundations",
        27: "Tool Use, Function Calling & Protocols",
        28: "Multi-Agent Systems",
        29: "Specialized Agents",
        30: "Tools of the Trade: Agent Stack",
    }),
]

# Standard callout palette
STANDARD_CALLOUTS = {
    "algorithm", "big-picture", "bibliography", "cross-ref", "exercise",
    "fun-note", "key-insight", "key-takeaway", "lab", "library-shortcut",
    "looking-back", "note", "numeric-example", "pathway", "postmortem",
    "practical-example", "production-pattern", "research-frontier", "self-check",
    "thesis-thread", "tip", "warning",
}

# Track issues by category and pattern
issues = {
    "format": defaultdict(list),
    "links": defaultdict(list),
    "naming": defaultdict(list),
    "captions": defaultdict(list),
    "styles": defaultdict(list),
}

# Overall stats
stats = {
    "total_files": 0,
    "files_clean_format": 0,
    "files_with_link_issues": 0,
    "files_with_naming_issues": 0,
    "files_with_caption_issues": 0,
    "files_with_style_issues": 0,
    "total_broken_links": 0,
    "total_naming_issues": 0,
    "total_caption_issues": 0,
    "total_style_issues": 0,
    "total_format_issues": 0,
}


class TagStackChecker(HTMLParser):
    """Simple HTML well-formedness checker (tracks tag stack).

    SVG tags like <stop>, <rect>, <circle>, <line>, <path>, <polygon>, etc.
    can be written either self-closing (<stop .../>) or with explicit
    closing tag (<stop ...></stop>). We do NOT treat them as void;
    we let them be balanced when explicitly closed.
    """
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                 "link", "meta", "param", "source", "track", "wbr"}
    # SVG tags we silently skip from stack tracking (they may appear self-closing
    # OR with explicit close; we don't care which).
    SVG_FLEXIBLE_TAGS = {"path", "circle", "rect", "line", "ellipse", "polygon",
                          "polyline", "use", "stop", "feDropShadow", "fedropshadow",
                          "feFlood", "feGaussianBlur", "feOffset", "feComposite",
                          "feMerge", "feMergeNode", "image", "text", "tspan",
                          "marker", "filter", "linearGradient", "lineargradient",
                          "radialGradient", "radialgradient", "defs", "g",
                          "clipPath", "clippath", "mask", "pattern", "symbol",
                          "foreignObject", "foreignobject", "switch", "title",
                          "desc"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []  # list of (tag, line)
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID_TAGS:
            return
        if tag in self.SVG_FLEXIBLE_TAGS:
            return  # tracked elsewhere if needed; ignore for balance
        line, col = self.getpos()
        self.stack.append((tag, line))

    def handle_endtag(self, tag):
        if tag in self.SVG_FLEXIBLE_TAGS:
            return
        line, col = self.getpos()
        if not self.stack:
            self.errors.append(f"L{line}: closing </{tag}> with no open tag")
            return
        # Look for matching tag in stack
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                # Anything above i is unclosed
                if i != len(self.stack) - 1:
                    for j in range(len(self.stack) - 1, i, -1):
                        unclosed_tag, unclosed_line = self.stack[j]
                        self.errors.append(
                            f"L{unclosed_line}: <{unclosed_tag}> never closed "
                            f"(before </{tag}> at L{line})")
                self.stack = self.stack[:i]
                return
        # No matching open tag
        self.errors.append(f"L{line}: closing </{tag}> with no matching open tag")

    def handle_startendtag(self, tag, attrs):
        # self-closing
        return

    def close(self):
        super().close()
        for tag, line in self.stack:
            self.errors.append(f"L{line}: <{tag}> never closed (EOF)")


def parse_section_id(filename: str) -> tuple[int, int] | None:
    m = re.match(r"section-(\d+)\.(\d+)\.html$", filename)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def normalize_path(base: Path, href: str) -> Path:
    """Resolve href relative to base file's parent."""
    href = href.split("#")[0].split("?")[0]
    if not href:
        return base
    return (base.parent / href).resolve()


def check_format(text: str, fpath: Path) -> list[str]:
    errs = []
    # Check well-formedness
    parser = TagStackChecker()
    try:
        parser.feed(text)
        parser.close()
    except Exception as e:
        errs.append(f"parse error: {e}")
    # Limit reported tag errors to most impactful
    for e in parser.errors[:5]:
        errs.append(f"unclosed-or-mismatched: {e}")
    # TODO / XXX markers
    for m in re.finditer(r"<!--\s*(TODO|XXX|FIXME)[^>]*-->", text, re.IGNORECASE):
        line = text[:m.start()].count("\n") + 1
        errs.append(f"L{line}: leftover marker {m.group(0)[:60]!r}")
    for m in re.finditer(r"\bXXX\b", text):
        # Limit false positives: skip if inside SVG fill colors etc. by context check
        line = text[:m.start()].count("\n") + 1
        # show context for visibility
        ctx_start = max(0, m.start() - 30)
        ctx_end = min(len(text), m.end() + 30)
        ctx = text[ctx_start:ctx_end].replace("\n", " ")
        # Skip if it's a placeholder in svg fill or font marker like "XXX-XX-XXXX"
        if re.search(r"[#a-fA-F0-9]{3,6}", ctx[max(0, m.start() - ctx_start - 1):m.start() - ctx_start + 1]):
            continue
        if "monospace" in ctx.lower() or "regex" in ctx.lower():
            continue
        errs.append(f"L{line}: 'XXX' marker found: ...{ctx[:80]}...")
    # Inline style overrides (heuristic - check non-trivial ones)
    inline_styles = list(re.finditer(r'\sstyle="([^"]+)"', text))
    if len(inline_styles) > 0:
        # Filter genuine offenders: those that override CSS classes
        # Common acceptable: style on agent-avatar-inline (background-color),
        # style on SVG elements is fine since they don't have CSS classes.
        suspicious_count = 0
        for m in inline_styles:
            line = text[:m.start()].count("\n") + 1
            content = m.group(1)
            # Get parent tag
            tag_start = text.rfind("<", 0, m.start())
            tag_text = text[tag_start:m.start()]
            tag_match = re.match(r"<(\w+)", tag_text)
            tag = tag_match.group(1).lower() if tag_match else "?"
            # Skip SVG content - SVG elements legitimately use style
            if tag in {"svg", "g", "rect", "circle", "line", "path", "text",
                       "polygon", "polyline", "ellipse", "use", "tspan",
                       "stop", "lineargradient", "radialgradient", "defs",
                       "fedropshadow", "filter", "marker"}:
                continue
            # Skip explicitly-allowed: agent-avatar-inline with background-color
            tag_attrs_end = text.find(">", tag_start)
            tag_attrs = text[tag_start:tag_attrs_end] if tag_attrs_end > tag_start else ""
            if "agent-avatar-inline" in tag_attrs and "background-color" in content:
                continue
            # Skip image width/max-width: these are often necessary for sizing single-instance images
            if re.fullmatch(r"\s*(max-)?width\s*:\s*[\d.]+(px|%|em|rem)?\s*;?\s*", content):
                continue
            # Skip simple alignment
            if "display:none" in content.replace(" ", "") and tag == "span":
                continue
            suspicious_count += 1
        if suspicious_count > 0:
            errs.append(f"inline-style: {suspicious_count} suspicious style= overrides "
                        f"(total inline styles: {len(inline_styles)})")
    return errs


def check_links(text: str, fpath: Path) -> list[str]:
    errs = []
    # All hrefs
    for m in re.finditer(r'<a\s[^>]*href="([^"]+)"', text):
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        if href.startswith("#"):
            continue
        # Strip fragment and query
        target = href.split("#")[0].split("?")[0]
        if not target:
            continue
        # Resolve
        try:
            resolved = (fpath.parent / target).resolve()
        except Exception as e:
            line = text[:m.start()].count("\n") + 1
            errs.append(f"L{line}: '{href}' -> resolve error: {e}")
            continue
        if not resolved.exists():
            line = text[:m.start()].count("\n") + 1
            errs.append(f"L{line}: '{href}' -> NOT FOUND")
    return errs


def check_naming(text: str, fpath: Path, part_name: str,
                 module_id: int, module_title: str, section_id: tuple[int, int]) -> list[str]:
    errs = []
    sec_num = f"{section_id[0]}.{section_id[1]}"
    # Title tag
    title_match = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        # Expected pattern: "Section N.M: <Title> | Building Conversational AI..."
        # But many books may use just "Section N.M: <Title>"
        if not title.startswith(f"Section {sec_num}:"):
            errs.append(f"<title> doesn't start with 'Section {sec_num}:': '{title[:80]}'")
    else:
        errs.append("missing <title> tag")
    # h1
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    if h1_match:
        h1 = re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()
        # h1 should match the title's section title portion
        if title_match:
            title_inner = title_match.group(1).strip()
            # Try to extract title body after "Section N.M:"
            tm = re.match(rf"Section {re.escape(sec_num)}:\s*(.+?)(\s*\|.*)?$", title_inner)
            if tm:
                expected_h1 = tm.group(1).strip()
                if expected_h1 != h1:
                    errs.append(f"<h1> '{h1[:60]}' != title body '{expected_h1[:60]}'")
    else:
        errs.append("missing <h1> tag")
    # Breadcrumb / page-current
    pc_match = re.search(r'<div class="page-current">(.*?)</div>', text)
    if pc_match:
        pc = pc_match.group(1).strip()
        if pc != f"Section {sec_num}":
            errs.append(f"page-current '{pc}' != 'Section {sec_num}'")
    else:
        errs.append("missing page-current breadcrumb")
    # pagefind chapter meta
    pf_match = re.search(
        r'data-pagefind-meta="chapter:Chapter (\d+):\s*([^"]+?)"', text)
    if pf_match:
        chap_num = int(pf_match.group(1))
        chap_title = pf_match.group(2)
        # Normalize entities for comparison
        chap_title_decoded = chap_title.replace("&amp;", "&")
        module_title_decoded = module_title.replace("&amp;", "&")
        if chap_num != module_id:
            errs.append(f"pagefind chapter number {chap_num} != {module_id}")
        if chap_title_decoded != module_title_decoded:
            errs.append(
                f"pagefind chapter title '{chap_title_decoded[:60]}' != "
                f"expected '{module_title_decoded[:60]}'")
    else:
        # Some sections may use breadcrumb-style pagefind meta
        # Also accept entity-encoded variants
        if not re.search(r'data-pagefind-meta="chapter:', text):
            errs.append("missing pagefind chapter meta")
    # Heading IDs - check h2/h3/h4 use correct section number prefix
    # Aggregate by stale prefix used (e.g. all using '14.1.x' instead of '17.1.x')
    bad_prefixes = defaultdict(list)  # stale_prefix -> [(line, heading), ...]
    total_bad = 0
    for m in re.finditer(r"<h([234])[^>]*>(.*?)</h\1>", text, re.DOTALL):
        heading = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        hm = re.match(r"^(\d+(?:\.\d+)+)\s", heading)
        if hm:
            heading_num = hm.group(1)
            if not heading_num.startswith(sec_num + "."):
                # extract just the "N.M" prefix (first two components)
                parts = heading_num.split(".")
                stale_prefix = ".".join(parts[:2])
                line = text[:m.start()].count("\n") + 1
                bad_prefixes[stale_prefix].append((line, heading[:50]))
                total_bad += 1
    for stale, entries in bad_prefixes.items():
        first_line = entries[0][0]
        example = entries[0][1]
        errs.append(
            f"heading-numbers use stale prefix '{stale}.x' (expected '{sec_num}.x') "
            f"x{len(entries)}, first at L{first_line}: '{example}'")
    return errs


def check_captions(text: str, fpath: Path, section_id: tuple[int, int]) -> list[str]:
    errs = []
    sec_num = f"{section_id[0]}.{section_id[1]}"
    # figures
    fig_count = 0
    fig_no_caption = 0
    fig_wrong_num = 0
    for m in re.finditer(r"<figure[^>]*>(.*?)</figure>", text, re.DOTALL):
        fig_count += 1
        inner = m.group(1)
        cap_match = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", inner, re.DOTALL)
        if not cap_match:
            fig_no_caption += 1
            line = text[:m.start()].count("\n") + 1
            errs.append(f"L{line}: <figure> without <figcaption>")
            continue
        cap_text = re.sub(r"<[^>]+>", "", cap_match.group(1)).strip()
        # Expected "Figure N.M.K"
        fm = re.match(r"Figure\s+(\d+\.\d+\.\d+)", cap_text)
        if not fm:
            line = text[:m.start()].count("\n") + 1
            errs.append(
                f"L{line}: figcaption doesn't start with 'Figure N.M.K': "
                f"'{cap_text[:60]}'")
            continue
        cap_num = fm.group(1)
        if not cap_num.startswith(sec_num + "."):
            fig_wrong_num += 1
            line = text[:m.start()].count("\n") + 1
            errs.append(
                f"L{line}: Figure {cap_num} doesn't match section {sec_num}")
    # comparison-tables
    table_count = 0
    table_no_title = 0
    table_wrong_num = 0
    # Look for comparison-table-title divs
    for m in re.finditer(
            r'<div class="comparison-table-title">(.*?)</div>', text, re.DOTALL):
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        tm = re.match(r"^(\d+\.\d+\.\d+)\s", title)
        if not tm:
            # Title without numbering
            line = text[:m.start()].count("\n") + 1
            errs.append(
                f"L{line}: comparison-table-title without 'N.M.K' numbering: "
                f"'{title[:60]}'")
        else:
            if not tm.group(1).startswith(sec_num + "."):
                line = text[:m.start()].count("\n") + 1
                errs.append(
                    f"L{line}: comparison-table-title number '{tm.group(1)}' "
                    f"doesn't match section {sec_num}")
    # Look for tables with comparison-table class that have NO title div before
    for m in re.finditer(
            r'<table[^>]*class="[^"]*comparison-table[^"]*"[^>]*>', text):
        # Look back ~200 chars for the title div
        prev = text[max(0, m.start() - 400):m.start()]
        if "comparison-table-title" not in prev:
            line = text[:m.start()].count("\n") + 1
            errs.append(
                f"L{line}: comparison-table without preceding "
                f"<div class='comparison-table-title'>")
    return errs


def check_styles(text: str, fpath: Path) -> list[str]:
    errs = []
    # Callouts
    callout_count_total = 0
    nonstandard = defaultdict(list)
    no_title = []
    # match <div class="callout ..."> ... </div> - but ".callout" may have multiple classes
    for m in re.finditer(r'<div\s+class="callout\s+([^"]+)"[^>]*>', text):
        callout_count_total += 1
        classes_str = m.group(1).strip()
        classes = classes_str.split()
        # Find any standard class
        std = [c for c in classes if c in STANDARD_CALLOUTS]
        non = [c for c in classes if c not in STANDARD_CALLOUTS]
        if not std:
            line = text[:m.start()].count("\n") + 1
            nonstandard[",".join(classes)].append(line)
        # Also flag stray non-standard classes alongside a standard one
        # Only complain if there's no standard at all - some classes like "compact" may be fine
        # Check for callout-title div following this opening tag (within ~300 chars)
        opening_end = m.end()
        # find matching closing </div> ? Hard - just check next ~400 chars for callout-title
        nearby = text[opening_end:opening_end + 600]
        if 'class="callout-title"' not in nearby and 'callout-title' not in nearby:
            line = text[:m.start()].count("\n") + 1
            no_title.append((line, classes_str))
    for cls_combo, lines in nonstandard.items():
        line_str = ",".join(f"L{l}" for l in lines[:3])
        more = f" (+{len(lines) - 3} more)" if len(lines) > 3 else ""
        errs.append(
            f"non-standard callout class '{cls_combo}' at {line_str}{more}")
    if no_title:
        examples = "; ".join(
            f"L{l} ({c})" for l, c in no_title[:3])
        more = f" (+{len(no_title) - 3} more)" if len(no_title) > 3 else ""
        errs.append(f"callout(s) missing <div class='callout-title'>: {examples}{more}")
    return errs


def main():
    report_lines = []
    report_lines.append("# Section Audit: Parts 4, 5, 6")
    report_lines.append("")
    report_lines.append(
        f"Audit of {sum(1 for _ in ROOT.rglob('section-*.html') if any(p in str(_) for p in ['part-4', 'part-5', 'part-6']))} section files "
        "across `part-4-training-adapting/`, `part-5-retrieval-conversation/`, "
        "`part-6-agentic-ai/` for five dimensions: HTML well-formedness/cleanliness, "
        "link integrity, naming consistency, figure/code captions, and callout style "
        "palette adherence.")
    report_lines.append("")
    report_lines.append("Generated by `scripts/audit_parts_4_6.py`. Read-only.")
    report_lines.append("")

    all_findings = []  # list of (part, module, section_file, findings_dict)
    for part_dir, part_label, modules in PARTS:
        part_path = ROOT / part_dir
        for module_dir in sorted(part_path.iterdir()):
            if not module_dir.is_dir() or not module_dir.name.startswith("module-"):
                continue
            mm = re.match(r"module-(\d+)-", module_dir.name)
            if not mm:
                continue
            module_id = int(mm.group(1))
            if module_id not in modules:
                continue
            module_title = modules[module_id]
            for section_file in sorted(module_dir.glob("section-*.html")):
                section_id = parse_section_id(section_file.name)
                if not section_id:
                    continue
                stats["total_files"] += 1
                try:
                    text = section_file.read_text(encoding="utf-8")
                except Exception as e:
                    all_findings.append({
                        "part": part_label, "module": module_id,
                        "module_title": module_title,
                        "section_id": section_id, "file": section_file,
                        "error": f"Could not read file: {e}",
                    })
                    continue
                findings = {
                    "format": check_format(text, section_file),
                    "links": check_links(text, section_file),
                    "naming": check_naming(
                        text, section_file, part_label, module_id, module_title, section_id),
                    "captions": check_captions(text, section_file, section_id),
                    "styles": check_styles(text, section_file),
                }
                # Update stats
                if not findings["format"]:
                    stats["files_clean_format"] += 1
                stats["total_format_issues"] += len(findings["format"])
                if findings["links"]:
                    stats["files_with_link_issues"] += 1
                stats["total_broken_links"] += len(findings["links"])
                if findings["naming"]:
                    stats["files_with_naming_issues"] += 1
                stats["total_naming_issues"] += len(findings["naming"])
                if findings["captions"]:
                    stats["files_with_caption_issues"] += 1
                stats["total_caption_issues"] += len(findings["captions"])
                if findings["styles"]:
                    stats["files_with_style_issues"] += 1
                stats["total_style_issues"] += len(findings["styles"])
                all_findings.append({
                    "part": part_label, "module": module_id,
                    "module_title": module_title,
                    "section_id": section_id, "file": section_file,
                    "findings": findings,
                })

    # ---- Summary ----
    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"- **Total files audited**: {stats['total_files']}")
    report_lines.append(
        f"- **Files with clean format (no HTML/marker issues)**: "
        f"{stats['files_clean_format']} ({stats['files_clean_format']*100//stats['total_files']}%)")
    report_lines.append(f"- **Total HTML format issues**: {stats['total_format_issues']}")
    report_lines.append(
        f"- **Files with broken links**: {stats['files_with_link_issues']} "
        f"(total broken hrefs: {stats['total_broken_links']})")
    report_lines.append(
        f"- **Files with naming inconsistencies**: {stats['files_with_naming_issues']} "
        f"(total issues: {stats['total_naming_issues']})")
    report_lines.append(
        f"- **Files with caption issues**: {stats['files_with_caption_issues']} "
        f"(total issues: {stats['total_caption_issues']})")
    report_lines.append(
        f"- **Files with style/callout issues**: {stats['files_with_style_issues']} "
        f"(total issues: {stats['total_style_issues']})")
    report_lines.append("")

    # ---- Aggregated patterns ----
    # Group repeating naming/caption/style issues across the corpus
    naming_patterns = defaultdict(list)  # pattern -> list of (sec, msg)
    caption_patterns = defaultdict(list)
    style_patterns = defaultdict(list)
    link_patterns = defaultdict(list)
    format_patterns = defaultdict(list)
    # Specialised aggregation: "Chapter N's headings use stale prefix from Chapter M"
    stale_chapter_map = defaultdict(list)  # (stale_chap, real_chap) -> [(sec, total)]

    for entry in all_findings:
        if "error" in entry:
            continue
        sec_label = f"{entry['section_id'][0]}.{entry['section_id'][1]}"
        for msg in entry["findings"]["naming"]:
            # Specialised: heading stale prefix
            sm = re.match(
                r"heading-numbers use stale prefix '(\d+)\.\d+\.x' "
                r"\(expected '(\d+)\.\d+\.x'\) x(\d+)", msg)
            if sm:
                stale_chap = int(sm.group(1))
                real_chap = int(sm.group(2))
                count = int(sm.group(3))
                stale_chapter_map[(real_chap, stale_chap)].append(
                    (sec_label, count))
                continue
            key = re.sub(r"L\d+", "L#", msg)
            key = re.sub(r"'[^']{30,}'", "'...'", key)
            naming_patterns[key].append((sec_label, msg))
        for msg in entry["findings"]["captions"]:
            key = re.sub(r"L\d+", "L#", msg)
            key = re.sub(r"'[^']{30,}'", "'...'", key)
            caption_patterns[key].append((sec_label, msg))
        for msg in entry["findings"]["styles"]:
            key = re.sub(r"L\d+|L#,?", "L#", msg)
            style_patterns[key].append((sec_label, msg))
        for msg in entry["findings"]["links"]:
            # Group by target file pattern
            tm = re.match(r"L(\d+): '([^']+)'", msg)
            if tm:
                target = tm.group(2)
                key = re.sub(r"section-\d+\.\d+\.html", "section-N.M.html", target)
                key = re.sub(r"module-\d+", "module-N", key)
                link_patterns[key].append((sec_label, msg))
            else:
                link_patterns[msg].append((sec_label, msg))
        for msg in entry["findings"]["format"]:
            key = re.sub(r"L\d+", "L#", msg)
            key = re.sub(r"'[^']{20,}'", "'...'", key)
            format_patterns[key].append((sec_label, msg))

    # ---- Recurring patterns section ----
    report_lines.append("## Recurring Patterns")
    report_lines.append("")
    report_lines.append(
        "Issues that show up across many sections, grouped to avoid duplication. "
        "Per-section detail follows below.")
    report_lines.append("")

    def add_pattern_table(title: str, patterns: dict, limit: int = 15):
        if not patterns:
            return
        report_lines.append(f"### {title}")
        report_lines.append("")
        sorted_patterns = sorted(patterns.items(), key=lambda x: -len(x[1]))
        for pat, occurrences in sorted_patterns[:limit]:
            cnt = len(occurrences)
            secs = sorted(set(o[0] for o in occurrences))
            sec_list = ", ".join(secs[:8])
            if len(secs) > 8:
                sec_list += f", ... (+{len(secs) - 8} more)"
            report_lines.append(f"- **[{cnt}x]** {pat}")
            report_lines.append(f"  - Sections: {sec_list}")
        if len(sorted_patterns) > limit:
            report_lines.append(
                f"- _(+ {len(sorted_patterns) - limit} more pattern variations)_")
        report_lines.append("")

    # Specialised: heading prefix stale-numbering table
    if stale_chapter_map:
        report_lines.append("### Heading numbering: stale chapter prefixes")
        report_lines.append("")
        report_lines.append(
            "Many sections were renumbered (chapter promotion) but their h2/h3/h4 "
            "headings still use the OLD chapter prefix. Each row aggregates all "
            "sections in `Real Chapter N` whose headings start with `M.x.y`.")
        report_lines.append("")
        sorted_keys = sorted(stale_chapter_map.keys())
        for (real, stale), entries in sorted_keys and [(k, stale_chapter_map[k]) for k in sorted_keys] or []:
            total = sum(c for _, c in entries)
            secs = sorted(set(s for s, _ in entries))
            sec_list = ", ".join(secs[:8])
            if len(secs) > 8:
                sec_list += f", ... (+{len(secs) - 8} more)"
            report_lines.append(
                f"- **Chapter {real}** headings still use **`{stale}.x.y`** "
                f"(should be `{real}.x.y`); "
                f"{total} stale headings across {len(secs)} section(s).")
            report_lines.append(f"  - Sections: {sec_list}")
        report_lines.append("")
    add_pattern_table("Naming inconsistencies (other)", naming_patterns)
    add_pattern_table("Caption / figure-number issues", caption_patterns)
    add_pattern_table("Style / callout palette issues", style_patterns)
    add_pattern_table("Broken-link patterns", link_patterns)
    add_pattern_table("HTML format issues", format_patterns)

    # ---- Per-section detail (only flagged sections) ----
    report_lines.append("## Per-Section Detail")
    report_lines.append("")
    report_lines.append(
        "Only sections with at least one finding are listed. Clean sections are omitted.")
    report_lines.append("")

    current_part = None
    current_module = None
    for entry in all_findings:
        if "error" in entry:
            report_lines.append(f"### {entry['file'].relative_to(ROOT).as_posix()}")
            report_lines.append(f"- FILE READ ERROR: {entry['error']}")
            report_lines.append("")
            continue
        f = entry["findings"]
        total = sum(len(v) for v in f.values())
        if total == 0:
            continue
        if entry["part"] != current_part:
            current_part = entry["part"]
            report_lines.append(f"### {current_part}")
            report_lines.append("")
        if entry["module"] != current_module:
            current_module = entry["module"]
            report_lines.append(
                f"#### Chapter {current_module}: {entry['module_title']}")
            report_lines.append("")
        sec_id = f"{entry['section_id'][0]}.{entry['section_id'][1]}"
        rel = entry["file"].relative_to(ROOT).as_posix()
        report_lines.append(f"##### Section {sec_id} — `{rel}`")
        report_lines.append("")
        for category, label in [
                ("format", "Format"), ("links", "Links"),
                ("naming", "Naming"), ("captions", "Captions"),
                ("styles", "Styles")]:
            msgs = f[category]
            if not msgs:
                continue
            # For captions, if more than 2, collapse to one summary line
            if category == "captions" and len(msgs) >= 2:
                first_line_match = re.search(r"L(\d+)", msgs[0])
                first_line = f"L{first_line_match.group(1)}" if first_line_match else "L?"
                report_lines.append(
                    f"- **{label}**: {len(msgs)} unnumbered comparison-table-title(s); "
                    f"first at {first_line}")
                continue
            report_lines.append(f"- **{label}**:")
            shown = msgs[:5]
            for msg in shown:
                report_lines.append(f"  - {msg}")
            if len(msgs) > 5:
                report_lines.append(f"  - _(+ {len(msgs) - 5} more)_")
        report_lines.append("")

    out_path = ROOT / "section-audit-parts-4-6.md"
    out_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"Total files: {stats['total_files']}, "
          f"format issues: {stats['total_format_issues']}, "
          f"link issues: {stats['total_broken_links']}, "
          f"naming issues: {stats['total_naming_issues']}, "
          f"caption issues: {stats['total_caption_issues']}, "
          f"style issues: {stats['total_style_issues']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
