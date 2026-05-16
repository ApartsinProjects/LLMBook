#!/usr/bin/env python3
"""Audit LLMBook for placeholder content (TODO stubs, empty callouts, etc.)."""
import os
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {"KDP", ".claude", "build", "source_fix_backups", "node_modules",
             "pagefind", "vendor", "temp_epub", "downloads", "_concept-figs",
             "images", "agents", "scripts", "styles", "templates"}

def skip_path(p: Path) -> bool:
    parts = p.parts
    for sd in SKIP_DIRS:
        if sd in parts:
            return True
    name = p.name
    if name.startswith("temp_"):
        return True
    return False

# Findings buckets
findings = {
    "p0_empty_callouts": [],
    "p0_placeholder_h1": [],
    "p0_dropped_appendix": [],
    "p1_todo_author": [],
    "p1_stub_index": [],
    "p1_empty_section": [],
    "p1_figure_replaced": [],
    "p2_caption_drift": [],
    "p2_todo_audit": [],
}

# Collect all HTML files
all_html = []
for p in ROOT.rglob("*.html"):
    if skip_path(p):
        continue
    all_html.append(p)

print(f"Scanning {len(all_html)} HTML files...", file=sys.stderr)

# Pre-build chapter prefix map: for files in part-N-.../module-XX-... the expected
# chapter number is XX. Module names like module-00 -> chapter 0 (or w/e numbering).
# We will check actual h1 number vs caption numbers.

def find_line(content: str, snippet: str) -> int:
    """Return 1-based line number where snippet first appears."""
    idx = content.find(snippet)
    if idx < 0:
        return 1
    return content[:idx].count("\n") + 1

def get_chapter_num_from_path(fp: Path) -> str | None:
    """Extract chapter number from parent dir like 'module-32-...' -> '32'."""
    for part in fp.parts:
        m = re.match(r"module-(\d+)", part)
        if m:
            return m.group(1).lstrip("0") or "0"
    return None

def get_chapter_num_from_h1(soup) -> str | None:
    """Extract chapter number from h1 like 'Chapter 3:' or 'Module 03'."""
    h1 = soup.find("h1")
    if not h1:
        return None
    txt = h1.get_text(" ", strip=True)
    m = re.search(r"(?:Chapter|Module|Appendix|Capstone)\s+([A-Z]?\d+)", txt, re.I)
    if m:
        return m.group(1).lstrip("0") or "0"
    return None

caption_pat = re.compile(r"\b(?:Code Fragment|Figure|Table|Equation|Listing)\s+([A-Z]?\d+)\.(\d+)(?:\.(\d+))?", re.I)
todo_author_pat = re.compile(r"TODO\s+author\s+(?:this|the|a)\b[^<\n]{0,80}", re.I)
todo_audit_pat = re.compile(r"<!--\s*TODO\(audit\)", re.I)
dropped_app_pat = re.compile(r"appendix-(?:n-production-patterns|i-hardware-compute)", re.I)
jinja_pat = re.compile(r"\{\{[^}]*\}\}")

for fp in all_html:
    try:
        content = fp.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        continue

    rel = fp.relative_to(ROOT).as_posix()

    # 1. TODO author this/the/a ... markers
    for m in todo_author_pat.finditer(content):
        line = content[:m.start()].count("\n") + 1
        snippet = m.group(0).strip()[:100]
        findings["p1_todo_author"].append((rel, line, snippet))

    # 2. TODO(audit) HTML comments
    for m in todo_audit_pat.finditer(content):
        line = content[:m.start()].count("\n") + 1
        # capture up to 80 chars of surrounding comment
        end = content.find("-->", m.start())
        snippet = content[m.start(): end+3 if end > 0 else m.start()+80][:120]
        findings["p2_todo_audit"].append((rel, line, snippet.replace("\n", " ")))

    # 3. <p class="figure-replaced"> -- match the opening tag (placeholder may contain <em>, etc.)
    for m in re.finditer(r'<p[^>]*class="[^"]*\bfigure-replaced\b[^"]*"[^>]*>', content):
        line = content[:m.start()].count("\n") + 1
        # capture up to 200 chars of inner content for context
        snippet = content[m.start(): m.start()+220].replace("\n", " ")[:200]
        findings["p1_figure_replaced"].append((rel, line, snippet))

    # 7. dropped appendix refs
    for m in dropped_app_pat.finditer(content):
        line = content[:m.start()].count("\n") + 1
        findings["p0_dropped_appendix"].append((rel, line, m.group(0)))

    # Now use BeautifulSoup
    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception:
        continue

    # 9. h1 with placeholder character
    for h1 in soup.find_all("h1"):
        txt = h1.get_text(" ", strip=True)
        if not txt:
            continue
        # Suspicious: starts with ^., _., or ?, or has {{...}}
        if (re.match(r"^[\^_]\s*\.", txt) or
            txt.strip() in {"?", "%", "."} or
            jinja_pat.search(txt) or
            txt.startswith("?.") or
            txt.startswith("%.")):
            line = find_line(content, str(h1)[:80])
            findings["p0_placeholder_h1"].append((rel, line, txt[:120]))

    # 5. Empty callouts: <div class="callout ...">  with title but no body <p>
    for cal in soup.find_all("div", class_=lambda c: c and "callout" in c.split()):
        # Skip nested title divs
        if "callout-title" in (cal.get("class") or []):
            continue
        # Has a title?
        title = cal.find("div", class_=lambda c: c and "callout-title" in (c.split() if c else []))
        if not title:
            continue
        # Find body content other than title
        body_elements = [child for child in cal.find_all(recursive=False)
                         if child is not title]
        # Check if any of those elements have non-empty text
        has_body = False
        for be in body_elements:
            t = be.get_text(" ", strip=True)
            if t:
                has_body = True
                break
        # Also check direct text content (NavigableString)
        if not has_body:
            for child in cal.children:
                if isinstance(child, str) and child.strip():
                    has_body = True
                    break
        if not has_body:
            line = find_line(content, str(cal)[:100])
            title_txt = title.get_text(" ", strip=True)[:60]
            findings["p0_empty_callouts"].append((rel, line, f"callout title='{title_txt}' has no body"))

    # 8. Caption drift: chapter num in caption mismatches the dir-based chapter number.
    # Use the parent module-XX dir, because section h1s often don't repeat "Chapter".
    ch_num = get_chapter_num_from_path(fp)
    if ch_num and ch_num.isdigit():
        # Find captions in many places: figcaption, caption, and elements with caption-ish class
        # We restrict the LEADING context to avoid catching cross-references like
        # "see Figure 5.2 in Chapter 5" mid-paragraph. We look at elements designed
        # to be the caption's own container.
        caption_tags = []
        for el in soup.find_all(["figcaption", "caption"]):
            caption_tags.append(el)
        for el in soup.find_all(class_=re.compile(r"\b(?:figure-caption|code-caption|diagram-caption|listing-caption|figure-label|caption)\b", re.I)):
            caption_tags.append(el)
        # Dedup
        seen_ids = set()
        for el in caption_tags:
            i = id(el)
            if i in seen_ids:
                continue
            seen_ids.add(i)
            # Only the LEADING text of the caption (e.g., 'Figure 5.2: ...')
            cap_txt = el.get_text(" ", strip=True)
            if not cap_txt:
                continue
            # Only consider the start of the caption (first ~40 chars) so a caption
            # whose body says 'see Figure 5.2' is not flagged.
            head = cap_txt[:60]
            m = caption_pat.match(head)
            if not m:
                # also accept leading 'Caption: Figure X.Y' patterns
                m = caption_pat.search(head)
                if not m or m.start() > 12:
                    continue
            cap_ch = m.group(1).lstrip("0") or "0"
            if cap_ch.isdigit() and cap_ch != ch_num:
                # Try to find a more precise line by searching for the literal caption marker
                marker = m.group(0)
                line = find_line(content, marker)
                findings["p2_caption_drift"].append(
                    (rel, line, f"caption '{marker}' but parent is module-{ch_num}: {cap_txt[:120]}"))

# 4. Stub-shape index.html (chapter index.html < 1500 bytes)
# A chapter index is one inside module-XX-... directories
for fp in all_html:
    if fp.name != "index.html":
        continue
    rel_parts = fp.relative_to(ROOT).parts
    # Must be a chapter index: parent dir starts with module- or appendix-
    parent = fp.parent.name
    if not (parent.startswith("module-") or parent.startswith("appendix-") or parent.startswith("capstone")):
        continue
    size = fp.stat().st_size
    if size < 1500:
        findings["p1_stub_index"].append((fp.relative_to(ROOT).as_posix(), 1, f"size={size}B (stub-shape)"))

# 6. Empty section files: section-X.Y.html < 2000 bytes
for fp in all_html:
    if not re.match(r"section-\d+\.\d+(?:\.\d+)?\.html$", fp.name):
        continue
    size = fp.stat().st_size
    if size < 2000:
        findings["p1_empty_section"].append((fp.relative_to(ROOT).as_posix(), 1, f"size={size}B (stub)"))

# Dedupe and sort
for k, v in findings.items():
    # dedupe by (file, line, snippet)
    seen = set()
    out = []
    for item in v:
        key = (item[0], item[1], item[2][:80])
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    out.sort(key=lambda x: (x[0], x[1]))
    findings[k] = out

# Counts
counts = {
    "P0": len(findings["p0_empty_callouts"]) + len(findings["p0_placeholder_h1"]) + len(findings["p0_dropped_appendix"]),
    "P1": len(findings["p1_todo_author"]) + len(findings["p1_stub_index"]) + len(findings["p1_empty_section"]) + len(findings["p1_figure_replaced"]),
    "P2": len(findings["p2_caption_drift"]) + len(findings["p2_todo_audit"]),
}

# Write the markdown
out_lines = []
out_lines.append(f"# LLMBook Placeholder Audit")
out_lines.append("")
out_lines.append(f"**Summary: P0: {counts['P0']}, P1: {counts['P1']}, P2: {counts['P2']}**")
out_lines.append("")
out_lines.append(f"Scanned {len(all_html)} HTML files under `E:/Projects/BookBlogsHome/LLMBook/`. Skipped: KDP, .claude, build, node_modules, temp_*, source_fix_backups, vendor, pagefind.")
out_lines.append("")

def section(title, items, rec):
    out_lines.append(f"## {title} ({len(items)})")
    out_lines.append("")
    if not items:
        out_lines.append("_None found._")
        out_lines.append("")
        return
    out_lines.append(f"_Recommendation: {rec}_")
    out_lines.append("")
    for fp, line, snip in items[:200]:  # cap per category for readability
        s = snip.replace("`", "'")
        out_lines.append(f"- `{fp}:{line}` -- {s}")
    if len(items) > 200:
        out_lines.append(f"- ... and {len(items) - 200} more")
    out_lines.append("")

out_lines.append("---")
out_lines.append("")
out_lines.append("## P0: Broken-looking")
out_lines.append("")
section("Empty callouts (title but no body)",
        findings["p0_empty_callouts"],
        "Either add body paragraphs or remove the callout shell.")
section("Placeholder h1 (Jinja-style or punctuation-only)",
        findings["p0_placeholder_h1"],
        "Replace with the proper chapter/section title.")
section("References to dropped appendices (production-patterns / hardware-compute)",
        findings["p0_dropped_appendix"],
        "Remove or redirect to the surviving appendix; these targets no longer exist.")

out_lines.append("---")
out_lines.append("")
out_lines.append("## P1: Missing content")
out_lines.append("")
section("TODO author this section markers",
        findings["p1_todo_author"],
        "Write the section or drop it from the TOC.")
section("Stub-shape chapter index.html files (< 1500 bytes)",
        findings["p1_stub_index"],
        "Author the chapter intro/big-picture/section-cards.")
section("Empty section files (< 2000 bytes)",
        findings["p1_empty_section"],
        "Either author the section or remove it from the build.")
section("<p class='figure-replaced'> placeholders",
        findings["p1_figure_replaced"],
        "Replace with actual figure (image, diagram, or remove caption).")

out_lines.append("---")
out_lines.append("")
out_lines.append("## P2: Drift")
out_lines.append("")
section("Mismatched caption chapter prefixes (post-renumber drift)",
        findings["p2_caption_drift"],
        "Rewrite caption numbers to match the current chapter index.")
section("TODO(audit) HTML comments",
        findings["p2_todo_audit"],
        "Resolve the audit note and remove the comment.")

# TODO list for follow-up agent
out_lines.append("---")
out_lines.append("")
out_lines.append("## Follow-up TODO list (for authoring agent)")
out_lines.append("")
out_lines.append("Organized by priority. Each item is self-contained; an agent can pick one and run it.")
out_lines.append("")

todo_idx = 1

# P0 first - empty callouts and h1 placeholders
if findings["p0_empty_callouts"]:
    out_lines.append(f"### Empty callouts (P0)")
    out_lines.append("")
    # group by file
    by_file = {}
    for fp, line, snip in findings["p0_empty_callouts"]:
        by_file.setdefault(fp, []).append((line, snip))
    for fp in sorted(by_file):
        sites = by_file[fp]
        out_lines.append(f"- [ ] **{todo_idx}.** Fill or remove {len(sites)} empty callout(s) in `{fp}`: lines {', '.join(str(s[0]) for s in sites[:10])}{'...' if len(sites)>10 else ''}")
        todo_idx += 1
    out_lines.append("")

if findings["p0_placeholder_h1"]:
    out_lines.append(f"### Placeholder titles (P0)")
    out_lines.append("")
    for fp, line, snip in findings["p0_placeholder_h1"]:
        out_lines.append(f"- [ ] **{todo_idx}.** Replace placeholder h1 '{snip}' in `{fp}:{line}` with proper chapter/section title.")
        todo_idx += 1
    out_lines.append("")

if findings["p0_dropped_appendix"]:
    out_lines.append(f"### Stale appendix references (P0)")
    out_lines.append("")
    by_file = {}
    for fp, line, snip in findings["p0_dropped_appendix"]:
        by_file.setdefault(fp, []).append(line)
    for fp in sorted(by_file):
        out_lines.append(f"- [ ] **{todo_idx}.** Remove/redirect dropped-appendix link(s) in `{fp}` (lines {', '.join(str(l) for l in by_file[fp][:10])}).")
        todo_idx += 1
    out_lines.append("")

# P1 - author markers, stub indices, empty sections
if findings["p1_todo_author"]:
    out_lines.append(f"### TODO author markers (P1)")
    out_lines.append("")
    by_file = {}
    for fp, line, snip in findings["p1_todo_author"]:
        by_file.setdefault(fp, []).append(line)
    for fp in sorted(by_file):
        out_lines.append(f"- [ ] **{todo_idx}.** Author the section(s) marked 'TODO author this section' in `{fp}` ({len(by_file[fp])} marker(s)).")
        todo_idx += 1
    out_lines.append("")

if findings["p1_stub_index"]:
    out_lines.append(f"### Stub chapter index.html (P1)")
    out_lines.append("")
    for fp, line, snip in findings["p1_stub_index"]:
        out_lines.append(f"- [ ] **{todo_idx}.** Author the chapter intro/big-picture/section-cards for `{fp}` ({snip}).")
        todo_idx += 1
    out_lines.append("")

if findings["p1_empty_section"]:
    out_lines.append(f"### Empty section files (P1)")
    out_lines.append("")
    for fp, line, snip in findings["p1_empty_section"][:80]:
        out_lines.append(f"- [ ] **{todo_idx}.** Author or drop `{fp}` ({snip}).")
        todo_idx += 1
    if len(findings["p1_empty_section"]) > 80:
        out_lines.append(f"- [ ] **{todo_idx}.** ... plus {len(findings['p1_empty_section']) - 80} additional stub section files (see list above).")
        todo_idx += 1
    out_lines.append("")

if findings["p1_figure_replaced"]:
    out_lines.append(f"### Replaced figure placeholders (P1)")
    out_lines.append("")
    by_file = {}
    for fp, line, snip in findings["p1_figure_replaced"]:
        by_file.setdefault(fp, []).append(line)
    for fp in sorted(by_file):
        out_lines.append(f"- [ ] **{todo_idx}.** Replace `<p class=\"figure-replaced\">` placeholder(s) in `{fp}` with actual figure ({len(by_file[fp])} site(s)).")
        todo_idx += 1
    out_lines.append("")

out_text = "\n".join(out_lines) + "\n"

out_path = ROOT / "placeholders-audit.md"
out_path.write_text(out_text, encoding="utf-8")

print(f"Wrote {out_path}", file=sys.stderr)
print(f"P0: {counts['P0']}, P1: {counts['P1']}, P2: {counts['P2']}", file=sys.stderr)
print(f"  empty callouts: {len(findings['p0_empty_callouts'])}", file=sys.stderr)
print(f"  placeholder h1: {len(findings['p0_placeholder_h1'])}", file=sys.stderr)
print(f"  dropped appendix: {len(findings['p0_dropped_appendix'])}", file=sys.stderr)
print(f"  TODO author: {len(findings['p1_todo_author'])}", file=sys.stderr)
print(f"  stub index: {len(findings['p1_stub_index'])}", file=sys.stderr)
print(f"  empty section: {len(findings['p1_empty_section'])}", file=sys.stderr)
print(f"  figure-replaced: {len(findings['p1_figure_replaced'])}", file=sys.stderr)
print(f"  caption drift: {len(findings['p2_caption_drift'])}", file=sys.stderr)
print(f"  TODO(audit): {len(findings['p2_todo_audit'])}", file=sys.stderr)
