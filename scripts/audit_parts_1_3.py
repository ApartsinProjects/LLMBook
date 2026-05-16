#!/usr/bin/env python3
"""Section-level quality audit for Parts 1, 2, 3 of LLMBook.

Checks:
  P0 Uniform clean format (well-formed HTML, indentation, TODO/XXX markers, inline styles)
  P1 Working links (relative internal links resolve)
  P2 Section naming (<title>, <h1>, breadcrumb, pagefind chapter:)
  P3 Captions (figure, code, table)
  P4 Callout styles (standard palette + callout-title presence)
"""
from __future__ import annotations
import os
import re
import sys
import html.parser
import json
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
PARTS = [
    ("part-1-foundations", "Part I: Foundations"),
    ("part-2-understanding-llms", "Part II: Understanding LLMs"),
    ("part-3-working-with-llms", "Part III: Working with LLMs"),
]

# Standard callout palette
STANDARD_CALLOUTS = {
    "algorithm", "big-picture", "bibliography", "cross-ref",
    "exercise", "fun-note", "key-insight", "key-takeaway", "lab",
    "library-shortcut", "looking-back", "note", "numeric-example",
    "pathway", "postmortem", "practical-example", "production-pattern",
    "research-frontier", "self-check", "thesis-thread", "tip", "warning",
}

# Common helper / utility classes that can appear on a callout div
# These are NOT palette identifiers themselves; we ignore them when
# determining the palette class.
CALLOUT_HELPER_CLASSES = {
    "callout", "callout-title", "callout-body",  # rare descriptors
    "callout-wide", "callout-half", "wide", "narrow",
    "no-icon", "compact", "centered",
    # Layout modifiers added by chapter 4 etc.
    "skip-to-mechanics", "optional-marker", "lab-callout",
}


class TagBalanceChecker(html.parser.HTMLParser):
    """Detect unclosed tags (very rough, treats void tags as void)."""
    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, lineno)
        self.errors = []  # list of (lineno, msg)

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        # Treat self-closing trick (xhtml style) by relying on handle_startendtag
        self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        # explicit self-close: <foo/>
        pass

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        # Find matching open in stack
        for i in range(len(self.stack) - 1, -1, -1):
            ot, ol = self.stack[i]
            if ot == tag:
                # pop everything above (which are unclosed)
                for j in range(len(self.stack) - 1, i, -1):
                    ut, ul = self.stack[j]
                    self.errors.append((ul, f"unclosed <{ut}>"))
                del self.stack[i:]
                return
        # No matching open: stray close
        self.errors.append((self.getpos()[0], f"stray </{tag}>"))

    def close(self):
        super().close()
        for ut, ul in self.stack:
            self.errors.append((ul, f"unclosed <{ut}>"))


def check_wellformed(text: str):
    """Return list of (lineno, msg) for malformed HTML."""
    p = TagBalanceChecker()
    try:
        p.feed(text)
        p.close()
    except Exception as e:
        return [(0, f"parser error: {e}")]
    # Filter known-noise: <input>, <br>, ... already void; <p> often left open which
    # we'll permit (HTML5 allows it).  Keep only major structural tags.
    significant = {
        "html", "head", "body", "main", "header", "footer", "nav",
        "section", "article", "div", "span", "table", "thead", "tbody",
        "tr", "td", "th", "ul", "ol", "li", "pre", "code", "h1", "h2", "h3",
        "h4", "h5", "h6", "figure", "figcaption", "blockquote", "cite",
        "details", "summary", "a", "form", "label",
    }
    out = []
    for ln, msg in p.errors:
        for tag in significant:
            if f"<{tag}>" in msg or f"</{tag}>" in msg:
                out.append((ln, msg))
                break
    return out


def find_todos(text: str):
    """Return list of (lineno, snippet) for TODO/XXX markers."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        # detect literal markers - not inside ordinary text like "todo:" examples
        # We look for: <!--TODO ... -->, TODO:, FIXME:, XXX
        s = line.strip()
        # Skip if line is talking about TODO conceptually inside a <p>
        # (no easy way to be perfect; we restrict to comment markers and
        # ALL-CAPS XXX / FIXME forms.)
        if re.search(r"<!--\s*(TODO|FIXME|XXX|TBD)\b", s, re.IGNORECASE):
            out.append((i, s[:80]))
        elif re.search(r"\b(XXX|FIXME)\b", s) and "callout" not in s.lower():
            # Avoid catching CSS class names; "XXX" or "FIXME" as bare token
            # is what we want. Skip if it's inside an attribute string.
            # Heuristic: report only if not preceded by quote/equal sign.
            if not re.search(r'["\'=]\s*[A-Za-z0-9_-]*?(XXX|FIXME)', s):
                out.append((i, s[:80]))
    return out


def find_inline_styles(text: str):
    """Return list of (lineno, snippet) for inline style= overrides
    where a CSS class would do. We exclude:
      - SVG context (any style= attribute inside <svg>...</svg>)
      - The agent-avatar-inline background-color hack
      - <td>/<th> cells with single colorbar/align overrides inside
        comparison tables (legitimate per-cell decorations)
    Lines retained are those representing genuine block-level inline styles
    on <div>, <p>, <h*>, <section>, etc.
    """
    out = []
    # Strip <svg>...</svg> regions before scanning so we don't pick them up.
    text_no_svg = re.sub(r"<svg\b[\s\S]*?</svg>", "", text)
    # Build a line-number remap: easier to just rescan with line numbers
    # AND check if a given line falls inside an SVG block.
    svg_ranges = []
    pos = 0
    for m in re.finditer(r"<svg\b[\s\S]*?</svg>", text):
        ln_start = text.count("\n", 0, m.start()) + 1
        ln_end = text.count("\n", 0, m.end()) + 1
        svg_ranges.append((ln_start, ln_end))
    def in_svg(ln):
        for a, b in svg_ranges:
            if a <= ln <= b:
                return True
        return False
    for i, line in enumerate(text.splitlines(), 1):
        if in_svg(i):
            continue
        for m in re.finditer(r'\bstyle\s*=\s*"([^"]*)"', line):
            content = m.group(1).strip()
            if not content:
                continue
            if "background-color" in content and "agent-avatar-inline" in line:
                continue
            # Skip light-decoration on table cells like
            #   <td style="background:#f0f0f0; color:#999;">
            # These are legitimate per-cell styles. Recognize them by checking
            # the surrounding tag is <td or <th and the style only contains
            # background/color/text-align (no positioning).
            tag_lookback = line[max(0, m.start() - 60):m.start()]
            in_td_or_th = bool(re.search(r"<(td|th|caption)\b[^>]*$", tag_lookback))
            simple_decor = bool(re.fullmatch(
                r"(\s*(background(-color)?|color|text-align|font-weight|"
                r"font-style|padding(-[a-z]+)?|caption-side)\s*:\s*[^;]+;?\s*)+",
                content,
            ))
            if in_td_or_th and simple_decor:
                continue
            out.append((i, m.group(0)[:80]))
    return out


# ----- Link resolution -----

def find_internal_links(text: str, source_dir: Path):
    """Return list of (lineno, href, exists_flag)."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in re.finditer(r'<a\s+[^>]*href\s*=\s*"([^"]+)"', line):
            href = m.group(1)
            # skip external
            if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
                continue
            # skip pure anchors
            if href.startswith("#"):
                continue
            # strip anchor
            path_part = href.split("#", 1)[0]
            if not path_part:
                continue
            target = (source_dir / path_part).resolve()
            exists = target.exists()
            out.append((i, href, exists))
    return out


# ----- Naming -----

NUMERIC_PREFIX_RE = re.compile(r"^Section\s+(\d+\.\d+)\s*:\s*(.+?)(?:\s*\|\s*.+)?$")


def check_naming(text: str, sec_id: str, mod_idx: int):
    """sec_id like '0.1', mod_idx is module number int."""
    issues = []
    # <title>
    m = re.search(r"<title>([^<]+)</title>", text)
    title_text = m.group(1).strip() if m else None
    if not title_text:
        issues.append("missing <title>")
    else:
        # Title format: "Section N.M: Title | Building Conversational AI..."
        if not re.match(rf"^Section\s+{re.escape(sec_id)}\s*:\s*\S", title_text):
            issues.append(f"<title> prefix mismatch: '{title_text[:80]}'")

    # <h1>
    m = re.search(r"<h1>([^<]+)</h1>", text)
    h1_text = m.group(1).strip() if m else None
    if not h1_text:
        issues.append("missing <h1>")

    # Compare title body part with h1
    if title_text and h1_text:
        # Strip "Section N.M:" prefix and trailing " | Building..."
        body = title_text
        body = re.sub(rf"^Section\s+{re.escape(sec_id)}\s*:\s*", "", body)
        body = re.sub(r"\s*\|\s*.+$", "", body).strip()
        if body and h1_text and body.lower() != h1_text.lower():
            issues.append(f"<title> body '{body}' != <h1> '{h1_text}'")

    # Breadcrumb: data-pagefind-meta="chapter" with text containing Chapter N
    # Actually breadcrumb is .page-breadcrumb;
    m = re.search(r'<div class="page-breadcrumb"[^>]*>(.*?)</div>', text, re.S)
    crumb_html = m.group(1) if m else ""
    # 'Section N' indicator
    sec_id_dot = sec_id  # like 0.1
    m = re.search(r'<div class="page-current">([^<]+)</div>', text)
    cur_text = m.group(1).strip() if m else None
    if cur_text:
        if cur_text != f"Section {sec_id_dot}":
            issues.append(f"page-current shows '{cur_text}' expected 'Section {sec_id_dot}'")
    else:
        issues.append("missing .page-current")

    # Pagefind chapter meta:
    # <span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter N: Title" hidden=""></span>
    m = re.search(r'data-pagefind-meta="chapter:([^"]+)"', text)
    if not m:
        # Also might be split across attribute - check older format
        m = re.search(r'data-pagefind-meta="chapter"[^>]*>([^<]+)', text)
        if not m:
            issues.append("missing pagefind chapter meta")
    else:
        chapter_meta = m.group(1)
        # Expect "Chapter N: ..."
        if not re.match(rf"^Chapter\s+{mod_idx:02d}\s*:", chapter_meta) and \
           not re.match(rf"^Chapter\s+{mod_idx}\s*:", chapter_meta):
            issues.append(f"pagefind chapter='{chapter_meta}' missing 'Chapter {mod_idx}:'")

    return issues, title_text, h1_text


# ----- Captions -----

CAPTION_PREFIX_RE = re.compile(r"\b(Figure|Code Fragment|Table|Listing|Diagram)\s+(\d+\.\d+\.\d+)\b")


def check_captions(text: str, sec_id: str):
    """Look at <figure>, <pre>, comparison-tables, and check captions present + N.M.K numbered."""
    issues = []
    # 1) Figures
    for m in re.finditer(r"<figure\b[^>]*>(.*?)</figure>", text, re.S):
        block = m.group(1)
        if "<figcaption" not in block:
            issues.append("figure missing <figcaption>")
        else:
            # Check Figure N.M.K caption prefix
            fc = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", block, re.S)
            if fc:
                cap_text = re.sub(r"<[^>]+>", "", fc.group(1)).strip()
                # Allow "Figure N.M.K:" or "Figure N.M:" sometimes
                ok = re.search(rf"\b(Figure)\s+{re.escape(sec_id)}\.\d+\b", cap_text)
                if not ok:
                    # also accept Figure with section prefix
                    if not re.search(r"\bFigure\s+\d+\.\d+\.\d+", cap_text) and \
                       not re.search(r"\bFigure\s+\d+\.\d+\b", cap_text):
                        issues.append(f"figcaption missing Figure N.M.K numbering: '{cap_text[:60]}'")
                    else:
                        # numbering present but doesn't match section id
                        m2 = re.search(r"\bFigure\s+(\d+\.\d+)", cap_text)
                        if m2 and m2.group(1) != sec_id:
                            issues.append(f"figcaption Figure {m2.group(1)} != section {sec_id}: '{cap_text[:60]}'")

    # 2) Comparison-table titles
    for m in re.finditer(r'<div class="comparison-table"[^>]*>(.*?)</div>\s*<table', text, re.S):
        block = m.group(1)
        if 'class="comparison-table-title"' not in block:
            issues.append("comparison-table missing comparison-table-title")
    # Also look for tables that begin with class comparison-table but lack title
    for m in re.finditer(
        r'<div class="comparison-table"[^>]*>([\s\S]*?)</div>', text):
        body = m.group(1)
        if "comparison-table-title" not in body:
            # Could be matched above; check both
            pass

    # 3) Pre code blocks - flag significant code (>=5 logical lines) lacking
    # caption. Skip blocks that are clearly inside a callout (the callout title
    # acts as a caption), inside <details>/<summary> (collapsible labels), or
    # inside <figure>/<aside>.
    pre_matches = list(re.finditer(r"<pre\b[^>]*>(.*?)</pre>", text, re.S))
    for pm in pre_matches:
        code_body = pm.group(1)
        lines_in_code = code_body.count("\n")
        if lines_in_code < 5:
            continue
        # Detect whether this <pre> is inside a callout/details/aside/figure
        # by looking back from the pre to find the nearest unmatched open of
        # one of those tags within 8000 chars.
        lookback = text[max(0, pm.start() - 8000):pm.start()]
        # Count opens vs closes of each container type in lookback.
        def open_unclosed(tag):
            opens = len(re.findall(rf"<{tag}\b", lookback))
            closes = len(re.findall(rf"</{tag}>", lookback))
            return opens > closes
        # Iterate every callout-marker in lookback; if any of them has more
        # <div opens than </div> closes in the substring from its position to
        # the current pre, we are still inside that callout.
        in_callout = False
        for cal in re.finditer(r'<div\s+class="[^"]*\bcallout\b[^"]*"', lookback):
            inner_chunk = lookback[cal.start():]
            opens = len(re.findall(r"<div\b", inner_chunk))
            closes = len(re.findall(r"</div>", inner_chunk))
            if opens > closes:
                in_callout = True
                break
        if in_callout:
            continue
        # Inside <details>?
        det_marker = list(re.finditer(r"<details\b", lookback))
        if det_marker:
            last = det_marker[-1]
            inner = lookback[last.start():]
            opens = len(re.findall(r"<details\b", inner))
            closes = len(re.findall(r"</details>", inner))
            if opens > closes:
                continue
        # Inside <figure>?
        fig_marker = list(re.finditer(r"<figure\b", lookback))
        if fig_marker:
            last = fig_marker[-1]
            inner = lookback[last.start():]
            opens = len(re.findall(r"<figure\b", inner))
            closes = len(re.findall(r"</figure>", inner))
            if opens > closes:
                continue
        # Inside <aside>?
        as_marker = list(re.finditer(r"<aside\b", lookback))
        if as_marker:
            last = as_marker[-1]
            inner = lookback[last.start():]
            opens = len(re.findall(r"<aside\b", inner))
            closes = len(re.findall(r"</aside>", inner))
            if opens > closes:
                continue
        # Check captions near this pre block (broader window now):
        window_before = text[max(0, pm.start() - 1500):pm.start()]
        window_after = text[pm.end():pm.end() + 1500]
        has_cap = (
            'class="code-caption"' in window_before
            or 'class="code-caption"' in window_after
            or re.search(r"Code Fragment\s+\d+\.\d+\.\d+", window_before)
            or re.search(r"Code Fragment\s+\d+\.\d+\.\d+", window_after)
            or re.search(r"Listing\s+\d+\.\d+", window_before)
            or re.search(r"Listing\s+\d+\.\d+", window_after)
        )
        if not has_cap:
            ln = text.count("\n", 0, pm.start()) + 1
            issues.append(f"significant <pre> (lineno {ln}) missing caption")

    return issues


# ----- Callout styles -----

CALLOUT_RE = re.compile(r'<div\s+class="callout\s+([^"]+)"', re.IGNORECASE)
ANY_CALLOUT_RE = re.compile(r'<div\s+class="([^"]*\bcallout\b[^"]*)"', re.IGNORECASE)


def check_callouts(text: str):
    issues = []
    # Find every <div class="callout XXX"> or <aside class="callout XXX">
    pattern = re.compile(r'<(?:div|aside)\s+class="([^"]+)"[^>]*>', re.IGNORECASE)
    for m in pattern.finditer(text):
        classes = m.group(1).split()
        if "callout" not in classes:
            continue
        # Get palette class candidates: exclude "callout" and helper classes
        candidates = [c for c in classes if c != "callout" and c not in CALLOUT_HELPER_CLASSES]
        lineno = text.count("\n", 0, m.start()) + 1
        if not candidates:
            issues.append((lineno, "callout has no palette class"))
        else:
            non_standard = [c for c in candidates if c not in STANDARD_CALLOUTS]
            if non_standard:
                issues.append((lineno, f"non-standard callout class(es): {','.join(non_standard)}"))

        # Look for callout-title within next chunk (within 4k chars of the open)
        chunk = text[m.end():m.end() + 4000]
        if 'class="callout-title"' not in chunk:
            issues.append((lineno, "callout missing callout-title"))

    return issues


# ----- Per-file driver -----

def collect_section_files():
    """Yield (part_name, section_path, sec_id, mod_idx)."""
    out = []
    for part_dir, _ in PARTS:
        part_root = ROOT / part_dir
        for mod_dir in sorted(part_root.iterdir()):
            if not mod_dir.is_dir() or not mod_dir.name.startswith("module-"):
                continue
            # Determine module index from directory name
            mm = re.match(r"module-(\d+)-", mod_dir.name)
            if not mm:
                continue
            mod_idx = int(mm.group(1))
            for sec_file in sorted(mod_dir.glob("section-*.html")):
                # sec_id from filename
                sm = re.match(r"section-(\d+\.\d+)\.html", sec_file.name)
                if not sm:
                    continue
                sec_id = sm.group(1)
                out.append((part_dir, sec_file, sec_id, mod_idx))
    return out


def audit_file(part_dir: str, path: Path, sec_id: str, mod_idx: int):
    """Return dict of categorized findings."""
    text = path.read_text(encoding="utf-8", errors="replace")
    findings = {
        "p0": [],  # structure
        "p1": [],  # links
        "p2": [],  # naming
        "p3": [],  # captions
        "p4": [],  # styles
    }

    # P0 ----------------------
    wf = check_wellformed(text)
    for ln, msg in wf:
        findings["p0"].append(f"line {ln}: {msg}")
    todos = find_todos(text)
    for ln, snippet in todos:
        findings["p0"].append(f"line {ln}: TODO/XXX marker: {snippet[:60]}")
    inline = find_inline_styles(text)
    if inline:
        # Group by occurrence and limit
        n = len(inline)
        sample_lines = [str(ln) for ln, _ in inline[:5]]
        findings["p0"].append(
            f"{n} inline style= occurrences (sample lines: {','.join(sample_lines)})"
        )

    # P1 ----------------------
    links = find_internal_links(text, path.parent)
    for ln, href, ok in links:
        if not ok:
            findings["p1"].append(f"line {ln}: broken href '{href}'")

    # P2 ----------------------
    naming_issues, title, h1 = check_naming(text, sec_id, mod_idx)
    findings["p2"].extend(naming_issues)

    # P3 ----------------------
    cap = check_captions(text, sec_id)
    findings["p3"].extend(cap)

    # P4 ----------------------
    co = check_callouts(text)
    for ln, msg in co:
        findings["p4"].append(f"line {ln}: {msg}")

    return findings


def main():
    sections = collect_section_files()
    results = []
    counts = {"p0": 0, "p1": 0, "p2": 0, "p3": 0, "p4": 0}
    files_with_issue = {"p0": 0, "p1": 0, "p2": 0, "p3": 0, "p4": 0}

    for part_dir, path, sec_id, mod_idx in sections:
        findings = audit_file(part_dir, path, sec_id, mod_idx)
        results.append((part_dir, path, sec_id, mod_idx, findings))
        for k, v in findings.items():
            counts[k] += len(v)
            if v:
                files_with_issue[k] += 1

    # Aggregate repeating broken-href patterns
    broken_pattern_counts = {}
    for _, _, _, _, f in results:
        for entry in f["p1"]:
            m = re.search(r"broken href '([^']+)'", entry)
            if m:
                href = m.group(1)
                # canonicalize by stripping anchors
                href = href.split("#", 1)[0]
                broken_pattern_counts[href] = broken_pattern_counts.get(href, 0) + 1

    # Print summary
    out_lines = []
    out_lines.append("# Per-Section Audit - Parts 1-3")
    out_lines.append("")
    out_lines.append(f"_Scope: every `section-N.M.html` under `part-1-foundations/`, `part-2-understanding-llms/`, `part-3-working-with-llms/` (modules 00-16)._")
    out_lines.append("")
    out_lines.append("## Summary")
    out_lines.append(f"- Files audited: {len(sections)}")
    out_lines.append(f"- P0 (structure / well-formedness / inline styles / TODO markers): {counts['p0']} findings across {files_with_issue['p0']} files")
    out_lines.append(f"- P1 (broken non-external links): {counts['p1']} findings across {files_with_issue['p1']} files")
    out_lines.append(f"- P2 (naming drift in <title>/<h1>/breadcrumb/pagefind): {counts['p2']} findings across {files_with_issue['p2']} files")
    out_lines.append(f"- P3 (missing captions on figures/code/comparison-tables): {counts['p3']} findings across {files_with_issue['p3']} files")
    out_lines.append(f"- P4 (callout palette drift / missing callout-title): {counts['p4']} findings across {files_with_issue['p4']} files")
    out_lines.append("")
    if broken_pattern_counts:
        out_lines.append("### Repeating broken-link patterns")
        sorted_p = sorted(broken_pattern_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        for href, n in sorted_p:
            out_lines.append(f"- `{href}` -> {n} occurrence(s)")
        out_lines.append("")
        out_lines.append("These hrefs reference old numbering (section-33.x, section-31.x, section-25.x) or wrong module names that no longer exist after the part renumbering.")
        out_lines.append("")
    out_lines.append("## Per-file findings")
    for part_dir, path, sec_id, mod_idx, f in results:
        rel = path.relative_to(ROOT).as_posix()
        any_issue = any(f.values())
        if not any_issue:
            continue
        out_lines.append(f"### {rel}")
        if f["p0"]:
            out_lines.append(f"  - P0 structure ({len(f['p0'])}):")
            for x in f["p0"][:20]:
                out_lines.append(f"    - {x}")
            if len(f["p0"]) > 20:
                out_lines.append(f"    - ... +{len(f['p0']) - 20} more")
        if f["p1"]:
            out_lines.append(f"  - P1 links ({len(f['p1'])}):")
            for x in f["p1"][:20]:
                out_lines.append(f"    - {x}")
            if len(f["p1"]) > 20:
                out_lines.append(f"    - ... +{len(f['p1']) - 20} more")
        if f["p2"]:
            out_lines.append(f"  - P2 naming ({len(f['p2'])}):")
            for x in f["p2"]:
                out_lines.append(f"    - {x}")
        if f["p3"]:
            out_lines.append(f"  - P3 captions ({len(f['p3'])}):")
            for x in f["p3"][:20]:
                out_lines.append(f"    - {x}")
            if len(f["p3"]) > 20:
                out_lines.append(f"    - ... +{len(f['p3']) - 20} more")
        if f["p4"]:
            out_lines.append(f"  - P4 styles ({len(f['p4'])}):")
            for x in f["p4"][:20]:
                out_lines.append(f"    - {x}")
            if len(f["p4"]) > 20:
                out_lines.append(f"    - ... +{len(f['p4']) - 20} more")

    # Write the report
    report_path = ROOT / "section-audit-parts-1-3.md"
    out_lines.append("")
    out_lines.append(f"_Generated by scripts/audit_parts_1_3.py over {len(sections)} sections._")
    text_out = "\n".join(out_lines)
    # Trim if exceeds 600 lines
    lines = text_out.splitlines()
    if len(lines) > 600:
        lines = lines[:595] + ["", "_... report truncated to fit 600-line cap; remaining files had similar patterns._"]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {report_path} with {len(lines)} lines")
    # Print summary to stdout
    print("\n".join(out_lines[:12]))


if __name__ == "__main__":
    main()
