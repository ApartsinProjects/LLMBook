#!/usr/bin/env python3
"""Standardize bibliography blocks across the LLMBook.

Canonical format:
<div class="callout bibliography">
<div class="callout-title">Further Reading</div>
<ul class="bibliography-list">
<li><a href="..." rel="noopener" target="_blank">Author, F. et al. (Year). Title.</a> One-sentence context.</li>
...
</ul>
</div>
"""
import re
import sys
import time
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
             "source_fix_backups", "pagefind", "templates", ".claude",
             ".book-update", "_concept-figs", ".html2epub_cache"}
SKIP_FILE_SUFFIX = ("-audit.md", "-report.md")
FRONT_MATTER_DIR = "front-matter"

# Statistics
stats = {
    "files_scanned": 0,
    "files_edited": 0,
    "entries_preserved": 0,
    "rel_attrs_added": 0,
    "variants": defaultdict(int),
    "edited_paths": [],
}

def should_skip(path):
    parts = path.parts
    for skip in SKIP_DIRS:
        if skip in parts:
            return True
    if FRONT_MATTER_DIR in parts:
        return True
    name = path.name
    if name.endswith(SKIP_FILE_SUFFIX):
        return True
    if name.startswith("_tmp"):
        return True
    return False

def add_external_attrs(text):
    """Add rel='noopener' target='_blank' to external <a> tags missing them.

    Returns (new_text, count_added).
    """
    count_added = [0]
    def repl(m):
        full = m.group(0)
        href = m.group(1)
        if not href.startswith(("http://", "https://")):
            return full
        has_rel = "rel=" in full
        has_target = "target=" in full
        if has_rel and has_target:
            return full
        new = full
        if not has_target:
            new = new[:-1] + ' target="_blank">'
        if not has_rel:
            new = new[:-1] + ' rel="noopener">'
        count_added[0] += 1
        return new
    pat = re.compile(r'<a [^>]*?href="([^"]+)"[^>]*>')
    new_text = pat.sub(repl, text)
    return new_text, count_added[0]

def extract_card_entries(block_text):
    """Extract entries from a card-style bibliography block."""
    entries = []
    current_category = None
    pat = re.compile(
        r'<div class="bib-category">(.*?)</div>'
        r'|<div class="bib-entry-card">(.*?)</div>',
        re.DOTALL,
    )
    for m in pat.finditer(block_text):
        if m.group(1) is not None:
            current_category = m.group(1).strip()
        else:
            card = m.group(2)
            ref_m = re.search(r'<p class="bib-ref">(.*?)</p>', card, re.DOTALL)
            annot_m = re.search(r'<p class="bib-annotation">(.*?)</p>', card, re.DOTALL)
            ref_html = ref_m.group(1).strip() if ref_m else ""
            annot = annot_m.group(1).strip() if annot_m else ""
            if ref_html:
                entries.append({
                    "category": current_category,
                    "ref_html": ref_html,
                    "annotation": annot,
                })
    return entries

def extract_pref_pairs(block_text):
    """Extract entries from `<p class="bib-ref"> ... </p><p class="bib-annotation"> ... </p>`."""
    entries = []
    # Iterate over each bib-ref paragraph; the immediately-following bib-annotation
    # (if any) is its annotation.
    pat = re.compile(r'<p class="bib-ref">(.*?)</p>\s*(?:<p class="bib-annotation">(.*?)</p>)?', re.DOTALL)
    for m in pat.finditer(block_text):
        ref_html = m.group(1).strip() if m.group(1) else ""
        annot = m.group(2).strip() if m.group(2) else ""
        if ref_html:
            entries.append({
                "category": None,
                "ref_html": ref_html,
                "annotation": annot,
            })
    return entries

def extract_ul_entries(block_text):
    """Extract entries from a plain `<ul><li>...</li></ul>` pattern (top-level)."""
    entries = []
    # Find the first <ul> ... </ul> (greedy may overrun nested uls, so balance manually)
    # Quick approach: find first <ul ...> and matching </ul>.
    m = re.search(r'<ul(?:\s+class="[^"]*")?\s*>', block_text)
    if not m:
        return entries
    start = m.end()
    # Find the matching closing </ul> by depth counting
    depth = 1
    i = start
    open_pat = re.compile(r'<ul\b')
    close_pat = re.compile(r'</ul>')
    while i < len(block_text) and depth > 0:
        nopen = open_pat.search(block_text, i)
        nclose = close_pat.search(block_text, i)
        if nclose is None:
            return entries
        if nopen is not None and nopen.start() < nclose.start():
            depth += 1
            i = nopen.end()
        else:
            depth -= 1
            if depth == 0:
                ul_content = block_text[start:nclose.start()]
                # Top-level <li>...</li>
                li_pat = re.compile(r'<li>(.*?)</li>', re.DOTALL)
                for lm in li_pat.finditer(ul_content):
                    content = lm.group(1).strip()
                    entries.append({"raw_li": content})
                return entries
            i = nclose.end()
    return entries

def make_li_from_card_entry(entry):
    ref = entry["ref_html"].strip()
    annot = entry.get("annotation", "").strip()
    if ref and annot:
        sep = " " if ref.endswith((".", "?", "!", ")", ">", '"')) else ". "
        return "<li>" + ref + sep + annot + "</li>"
    return "<li>" + ref + "</li>"

def build_canonical_block(title, entries, group_by_category=True):
    if not entries:
        return ""
    parts = ['<div class="callout bibliography">']
    parts.append('<div class="callout-title">' + title + '</div>')
    has_categories = any(e.get("category") for e in entries if "raw_li" not in e)
    if has_categories and group_by_category:
        current_cat = "__sentinel__"
        for e in entries:
            cat = e.get("category")
            if cat != current_cat:
                if current_cat != "__sentinel__":
                    parts.append("</ul>")
                if cat:
                    parts.append("<h4>" + cat + "</h4>")
                parts.append('<ul class="bibliography-list">')
                current_cat = cat
            if "raw_li" in e:
                parts.append("<li>" + e["raw_li"] + "</li>")
            else:
                parts.append(make_li_from_card_entry(e))
        parts.append("</ul>")
    else:
        parts.append('<ul class="bibliography-list">')
        for e in entries:
            if "raw_li" in e:
                parts.append("<li>" + e["raw_li"] + "</li>")
            else:
                parts.append(make_li_from_card_entry(e))
        parts.append("</ul>")
    parts.append("</div>")
    return "\n".join(parts)

def determine_title(default, existing_title=""):
    if existing_title:
        et = existing_title.strip().lower()
        if "selected" in et:
            return "Further Reading"
        if "further" in et:
            return "Further Reading"
        if "reference" in et:
            return "References"
        if "bibliography" in et:
            return "Bibliography"
    return default

def find_balanced_section(text, start_marker, start_tag="<section", end_tag="</section>"):
    """Find a balanced section block starting at a marker.

    Returns (start, end) indices or None.
    """
    s = text.find(start_marker)
    if s < 0:
        return None
    depth = 0
    i = s
    open_pat = re.compile(re.escape(start_tag) + r'\b')
    close_pat = re.compile(re.escape(end_tag))
    while i < len(text):
        nopen = open_pat.search(text, i)
        nclose = close_pat.search(text, i)
        if nclose is None:
            return None
        if nopen is not None and nopen.start() < nclose.start():
            depth += 1
            i = nopen.end()
        else:
            depth -= 1
            i = nclose.end()
            if depth == 0:
                return (s, i)
    return None

def find_balanced_div(text, start_idx):
    """Starting at <div..., find the matching </div>."""
    if not text[start_idx:start_idx+4] == "<div":
        return None
    depth = 0
    i = start_idx
    open_pat = re.compile(r'<div\b')
    close_pat = re.compile(r'</div>')
    while i < len(text):
        nopen = open_pat.search(text, i)
        nclose = close_pat.search(text, i)
        if nclose is None:
            return None
        if nopen is not None and nopen.start() < nclose.start():
            depth += 1
            i = nopen.end()
        else:
            depth -= 1
            i = nclose.end()
            if depth == 0:
                return i
    return None

def process_file(path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False
    original = text
    new_text = text

    # Pass 1: Replace <section class="bibliography" ...>...</section> blocks
    # Handle optional attributes (e.g. id="bibliography")
    section_open_pat = re.compile(r'<section class="bibliography"(?:\s+[^>]*)?>')
    while True:
        m_open = section_open_pat.search(new_text)
        if not m_open:
            break
        s = m_open.start()
        # Find matching </section>
        end = new_text.find('</section>', s)
        if end < 0:
            break
        open_tag_end = m_open.end()
        end_inner = end
        end += len('</section>')
        full_block = new_text[s:end]
        section_inner = new_text[open_tag_end:end_inner]
        title_m = re.search(r'<h3[^>]*>(.*?)</h3>', section_inner, re.DOTALL)
        existing_title = title_m.group(1).strip() if title_m else ""
        title = determine_title("Further Reading", existing_title)
        entries = extract_card_entries(section_inner)
        if not entries:
            entries = extract_pref_pairs(section_inner)
        if not entries:
            entries = extract_ul_entries(section_inner)
        if not entries:
            # Can't process; replace with stub to avoid infinite loop
            new_text = new_text[:s] + "<!-- bibliography skipped: no entries -->" + new_text[end:]
            continue
        block = build_canonical_block(title, entries, group_by_category=True)
        new_text = new_text[:s] + block + new_text[end:]
        stats["variants"]["section_bibliography"] += 1
        stats["entries_preserved"] += len(entries)

    # Pass 2: Replace standalone <h3>Bibliography...</h3>...
    # (only if no section was here previously; previous pass already handled those)
    # Find each h3 not inside a callout bibliography
    h3_pat = re.compile(
        r'<h3[^>]*>\s*(?:Bibliography(?:\s+and\s+Further\s+Reading)?|Further\s+Reading|References)[^<]*</h3>',
        re.IGNORECASE,
    )
    for m in list(h3_pat.finditer(new_text)):
        s = m.start()
        # Skip if inside a callout-bibliography (we placed those during pass 1 wrapping)
        # Look backwards to find nearest enclosing div class="callout bibliography"
        prefix = new_text[max(0, s - 600):s]
        if 'class="callout bibliography"' in prefix and "</div>" not in prefix.split('class="callout bibliography"', 1)[-1]:
            continue
        # Find content end: next h2/h3 or nav/footer or section/div-callout/whats-next
        content_start = m.end()
        end_pat = re.compile(r'<h[123]\b|<nav\b|<footer\b|<section\b|<div class="(?:chapter-nav|whats-next|callout)|</main>')
        em = end_pat.search(new_text, content_start)
        if not em:
            continue
        h3_content = new_text[content_start:em.start()]
        existing_title_m = re.search(r'<h3[^>]*>([^<]+)</h3>', m.group(0))
        existing_title = existing_title_m.group(1).strip() if existing_title_m else ""
        title = determine_title("Further Reading", existing_title)
        entries = extract_card_entries(h3_content)
        if not entries:
            entries = extract_pref_pairs(h3_content)
        if not entries:
            entries = extract_ul_entries(h3_content)
        if not entries:
            continue
        block = build_canonical_block(title, entries, group_by_category=True)
        new_text = new_text[:s] + block + new_text[em.start():]
        stats["variants"]["h3_only_bibliography"] += 1
        stats["entries_preserved"] += len(entries)

    # Pass 3: Normalize existing <div class="callout bibliography"> blocks
    # Find each occurrence
    idx = 0
    while True:
        s = new_text.find('<div class="callout bibliography">', idx)
        if s < 0:
            break
        end = find_balanced_div(new_text, s)
        if end is None:
            idx = s + 1
            continue
        full = new_text[s:end]
        # Extract callout-title
        title_m = re.search(r'<div class="callout-title">([^<]+)</div>', full)
        existing_title = title_m.group(1).strip() if title_m else ""
        title = determine_title(existing_title or "Further Reading", existing_title)
        # Strip outer wrapper to get inner content for parsing
        inner_start = full.find('</div>', full.find('<div class="callout-title">'))
        if inner_start < 0:
            idx = end
            continue
        inner_start += len('</div>')
        inner = full[inner_start:-len('</div>')]
        # If already canonical: ul.bibliography-list and no bib-ref/bib-entry-card
        if 'class="bibliography-list"' in inner and '<p class="bib-ref"' not in inner and '<div class="bib-entry-card">' not in inner:
            idx = end
            continue
        entries = extract_card_entries(inner)
        if not entries:
            entries = extract_pref_pairs(inner)
        if not entries:
            entries = extract_ul_entries(inner)
        if not entries:
            idx = end
            continue
        block = build_canonical_block(title, entries, group_by_category=True)
        new_text = new_text[:s] + block + new_text[end:]
        stats["variants"]["callout_normalized"] += 1
        stats["entries_preserved"] += len(entries)
        # Advance index past the replacement
        idx = s + len(block)

    # Pass 4: Add rel/target attrs to external links inside each callout bibliography
    added_total = [0]
    idx = 0
    out_parts = []
    last = 0
    while True:
        s = new_text.find('<div class="callout bibliography">', idx)
        if s < 0:
            out_parts.append(new_text[last:])
            break
        end = find_balanced_div(new_text, s)
        if end is None:
            out_parts.append(new_text[last:])
            break
        out_parts.append(new_text[last:s])
        block = new_text[s:end]
        new_block, count = add_external_attrs(block)
        added_total[0] += count
        out_parts.append(new_block)
        last = end
        idx = end
    new_text = "".join(out_parts)
    stats["rel_attrs_added"] += added_total[0]

    if new_text != original:
        path.write_text(new_text, encoding="utf-8")
        stats["files_edited"] += 1
        stats["edited_paths"].append(str(path.relative_to(ROOT)))
        return True
    return False

def main():
    files = []
    for path in ROOT.rglob("*.html"):
        if should_skip(path):
            continue
        files.append(path)
    stats["files_scanned"] = len(files)
    for p in files:
        try:
            process_file(p)
        except Exception as e:
            print("ERROR on " + str(p) + ": " + str(e))

    print("Files scanned: " + str(stats["files_scanned"]))
    print("Files edited: " + str(stats["files_edited"]))
    print("Entries preserved: " + str(stats["entries_preserved"]))
    print("rel/target attrs added: " + str(stats["rel_attrs_added"]))
    print("Variant breakdown: " + str(dict(stats["variants"])))

    import json
    out = {
        "files_scanned": stats["files_scanned"],
        "files_edited": stats["files_edited"],
        "entries_preserved": stats["entries_preserved"],
        "rel_attrs_added": stats["rel_attrs_added"],
        "variants": dict(stats["variants"]),
        "edited_paths": stats["edited_paths"],
    }
    Path("E:/Projects/BookBlogsHome/LLMBook/.book-update/standardize_bib_stats.json").write_text(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
