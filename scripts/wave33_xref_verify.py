"""Wave 33 cross-reference verification.

Categorizes findings:
  1. Bad anchor text: <a href="...section-31.1a.html">Section 31.1</a>
     (text says "Section 31.1" but target is 31.1a or different)
  2. Stale section labels: links whose number text refers to a moved/wrong section
  3. Unlinked references: "Section X.Y" / "Chapter N" in prose without an <a>
  4. Mismatched concept-link: class="concept-link" pointing to non-canonical home

Outputs a structured JSON sidecar and a markdown report.
"""

import os
import re
import glob
import json
from collections import defaultdict

ROOT = r"E:\Projects\BookBlogsHome\LLMBook"
os.chdir(ROOT)


# -----------------------------------------------------------------------------
# 1. Build target index
# -----------------------------------------------------------------------------
def index_sections():
    """Map section number -> (path, real chapter/section number).

    Section files live at part-N/module-MM-name/section-X.Y[a|b].html
    The section NUMBER is what appears after "section-" in the filename.
    """
    by_number = {}          # "31.1a" -> path
    chapter_to_module = {}  # chapter number (int) -> module folder name
    section_titles = {}     # path -> H1 title (or H2)

    for f in glob.glob("part-*/module-*/section-*.html"):
        norm = f.replace("\\", "/")
        bn = os.path.basename(f)
        m = re.match(r"section-([\d]+\.[\d]+[a-z]?)\.html$", bn)
        if not m:
            continue
        num = m.group(1)
        by_number[num] = norm

        # parse chapter number
        chap_m = re.match(r"(\d+)\.", num)
        if chap_m:
            ch = int(chap_m.group(1))
            mod_dir = norm.split("/")[1]
            chapter_to_module[ch] = mod_dir

    # also index module index pages
    for f in glob.glob("part-*/module-*/index.html"):
        norm = f.replace("\\", "/")
        m = re.search(r"module-(\d+)", norm)
        if m:
            ch = int(m.group(1))
            chapter_to_module.setdefault(ch, norm.split("/")[1])

    return by_number, chapter_to_module


SECTION_INDEX, CHAPTER_INDEX = index_sections()


# -----------------------------------------------------------------------------
# 2. Helper to resolve hrefs
# -----------------------------------------------------------------------------
def resolve_href(href, src_file):
    """Resolve a relative href into a normalized absolute file path."""
    if "#" in href:
        head, anchor = href.split("#", 1)
    else:
        head, anchor = href, None
    if not head:
        return None, anchor
    src_dir = os.path.dirname(os.path.abspath(src_file))
    abs_target = os.path.normpath(os.path.join(src_dir, head))
    return abs_target.replace("\\", "/"), anchor


def get_section_number_from_path(path):
    """Extract section number from a target path, or None."""
    bn = os.path.basename(path)
    m = re.match(r"section-([\d]+\.[\d]+[a-z]?)\.html$", bn)
    return m.group(1) if m else None


def get_chapter_from_path(path):
    """Extract chapter number from a module-NN path."""
    m = re.search(r"module-(\d+)", path)
    return int(m.group(1)) if m else None


# -----------------------------------------------------------------------------
# 3. Scan files
# -----------------------------------------------------------------------------

# Patterns
RE_A = re.compile(
    r'<a\b([^>]*?)>(.*?)</a>',
    re.DOTALL | re.IGNORECASE,
)
RE_HREF = re.compile(r'href\s*=\s*"([^"]*)"', re.IGNORECASE)
RE_CLASS = re.compile(r'class\s*=\s*"([^"]*)"', re.IGNORECASE)

# Strip tags inside anchor text
RE_INNER_TAG = re.compile(r"<[^>]+>")

# Section label patterns to detect "Section X.Y" or "Section X.Y[a]"
RE_SECTION_LABEL = re.compile(
    r"(?:section\s+)(\d+(?:\.\d+)?[a-z]?)",
    re.IGNORECASE,
)

# Chapter label
RE_CHAPTER_LABEL = re.compile(r"(?:chapter\s+)(\d+)", re.IGNORECASE)

# Tag detection for "in prose" unlinked refs: we look for naked "Section X.Y" / "Chapter N"
# in <p> tags that are NOT inside <a> tags.
RE_PARA = re.compile(r"<p\b[^>]*>(.*?)</p>", re.DOTALL | re.IGNORECASE)
RE_HEADING = re.compile(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]>", re.DOTALL | re.IGNORECASE)

# Excluded directories (skip the parts/modules per constraints)
SKIP_FILES = set()
for f in glob.glob("part-7-retrieval-information-extraction-with-llms/module-42-*/section-*.html"):
    SKIP_FILES.add(f.replace("\\", "/"))
for f in glob.glob("part-9-llm-evaluation-observability/module-44-*/section-*.html"):
    SKIP_FILES.add(f.replace("\\", "/"))


def strip_anchors(text):
    """Remove <a>...</a> tags entirely (keep text-only by replacing with placeholder).

    Returns prose-with-anchors-removed so we can find naked Section/Chapter refs.
    """
    return re.sub(r"<a\b[^>]*>.*?</a>", " ", text, flags=re.DOTALL | re.IGNORECASE)


# Output collectors
findings = {
    "bad_anchor_text": [],         # link text mismatches target section number
    "stale_section_labels": [],    # label like "Section 44.1" pointing somewhere else
    "unlinked_section_refs": [],   # "Section X.Y" in prose, not linked
    "unlinked_chapter_refs": [],   # "Chapter N" in prose, not linked
    "mismatched_concept_link": [], # concept-link target doesn't match concept name
    "broken_xrefs": [],            # target file missing
}


# Get all candidate files
ALL_FILES = []
for pattern in [
    "part-*/module-*/section-*.html",
    "part-*/module-*/index.html",
    "part-*/index.html",
    "appendices/**/*.html",
    "front-matter/*.html",
    "capstone/**/*.html",
]:
    for f in glob.glob(pattern, recursive=True):
        norm = f.replace("\\", "/")
        if norm in SKIP_FILES:
            continue
        # Don't touch module-42 or module-44
        if "module-42" in norm or "module-44" in norm:
            continue
        ALL_FILES.append(norm)

print(f"Scanning {len(ALL_FILES)} HTML files")
print(f"Section index has {len(SECTION_INDEX)} entries")


for fpath in ALL_FILES:
    try:
        with open(fpath, "r", encoding="utf-8") as fh:
            content = fh.read()
    except Exception:
        continue

    # Skip nav links - they always wrap link text in specific patterns
    # We process <a> tags but skip if inside <nav>
    # Quick approximation: find all <nav>...</nav> ranges and skip anchors within
    nav_ranges = []
    for m in re.finditer(r"<nav\b[^>]*>", content, re.IGNORECASE):
        start = m.start()
        # find matching </nav>
        depth = 1
        idx = m.end()
        while depth and idx < len(content):
            n_open = content.find("<nav", idx)
            n_close = content.find("</nav>", idx)
            if n_close == -1:
                break
            if n_open != -1 and n_open < n_close:
                depth += 1
                idx = n_open + 4
            else:
                depth -= 1
                idx = n_close + 6
        nav_ranges.append((start, idx))

    def in_nav(pos):
        for a, b in nav_ranges:
            if a <= pos < b:
                return True
        return False

    # 1. Iterate all <a> tags
    for m in RE_A.finditer(content):
        if in_nav(m.start()):
            continue
        attrs = m.group(1)
        inner = m.group(2)
        href_m = RE_HREF.search(attrs)
        class_m = RE_CLASS.search(attrs)
        cls = class_m.group(1) if class_m else ""
        if not href_m:
            continue
        href = href_m.group(1)
        # skip external/anchor-only/self
        if not href or href.startswith("#") or href.startswith("http") or href.startswith("mailto:"):
            continue

        plain_inner = RE_INNER_TAG.sub("", inner).strip()
        if not plain_inner:
            continue

        # Find target file
        tgt_abs, anchor = resolve_href(href, fpath)
        if not tgt_abs:
            continue
        tgt_exists = os.path.isfile(tgt_abs)
        if not tgt_exists:
            findings["broken_xrefs"].append({
                "file": fpath,
                "href": href,
                "text": plain_inner[:80],
            })
            continue

        tgt_norm = tgt_abs.replace("\\", "/")
        # Make it relative to repo root for storage
        try:
            tgt_rel = os.path.relpath(tgt_abs, ROOT).replace("\\", "/")
        except Exception:
            tgt_rel = tgt_norm

        # Check anchor text vs target section number
        # Only if target is a section-X.Y[a|b].html
        target_section = get_section_number_from_path(tgt_rel)

        # Skip section-card wrappers (the entire section card is wrapped in an <a>).
        # These are detected by class="section-card".
        is_section_card = "section-card" in cls

        if target_section and not is_section_card:
            # Only consider INLINE links where the entire anchor text is a section ref
            # (not section-card or other large block links).
            # Heuristic: text length under 80 chars AND starts with or matches Section X.Y label.
            short_inner = plain_inner.strip()
            if len(short_inner) <= 120:
                # If anchor text contains "Section X.Y" pattern
                sec_m = RE_SECTION_LABEL.search(short_inner)
                if sec_m:
                    cited_num = sec_m.group(1)
                    # Normalize: "31.1" cited vs "31.1a" target = bad anchor text
                    if cited_num != target_section:
                        findings["bad_anchor_text"].append({
                            "file": fpath,
                            "href": href,
                            "text": short_inner[:120],
                            "cited_section": cited_num,
                            "target_section": target_section,
                            "target": tgt_rel,
                        })

        # Stale section labels: linked text "Section 44.X" where target is in a different chapter
        # e.g. "Section 44.1" but target is at module-66/section-66.2
        if not is_section_card:
            short_inner = plain_inner.strip()
            if len(short_inner) <= 120:
                sec_m = RE_SECTION_LABEL.search(short_inner)
                if sec_m and target_section:
                    cited_chapter = int(sec_m.group(1).split(".")[0])
                    target_chapter = int(target_section.split(".")[0])
                    if cited_chapter != target_chapter:
                        findings["stale_section_labels"].append({
                            "file": fpath,
                            "href": href,
                            "text": short_inner[:120],
                            "cited_section": sec_m.group(1),
                            "target_section": target_section,
                            "target": tgt_rel,
                        })

        # Mismatched concept-link: concept-link class but the text is a name and target is a
        # chapter or module index, not its canonical home.
        # We'll only flag if the target file's <h1>/<h2> doesn't contain the concept name.
        if "concept-link" in cls:
            # Read target H1/H2 lazily (cache could be added later)
            try:
                with open(tgt_abs, "r", encoding="utf-8") as gh:
                    gc = gh.read(20000)
                h_m = re.search(r"<h[12]\b[^>]*>(.*?)</h[12]>", gc, re.DOTALL | re.IGNORECASE)
                heading_text = RE_INNER_TAG.sub("", h_m.group(1)) if h_m else ""
                heading_text = heading_text.lower()
                concept = plain_inner.lower()
                if heading_text and concept and concept not in heading_text:
                    # Loosely check if any concept word is in heading
                    words = [w for w in re.findall(r"[A-Za-z]+", concept) if len(w) > 3]
                    if words and not any(w in heading_text for w in words):
                        findings["mismatched_concept_link"].append({
                            "file": fpath,
                            "href": href,
                            "text": plain_inner[:80],
                            "target_heading": heading_text[:100],
                            "target": tgt_rel,
                        })
            except Exception:
                pass

    # 2. Find unlinked "Section X.Y" / "Chapter N" references in <p> bodies (NOT in <h>)
    for pm in RE_PARA.finditer(content):
        if in_nav(pm.start()):
            continue
        body = pm.group(1)
        # Strip anchors entirely
        body_stripped = strip_anchors(body)
        for sm in RE_SECTION_LABEL.finditer(body_stripped):
            cited = sm.group(1)
            # Only flag if numeric.numeric (don't flag stuff like "Section 4")
            if "." in cited:
                findings["unlinked_section_refs"].append({
                    "file": fpath,
                    "section": cited,
                    "context": body_stripped[max(0, sm.start()-40):sm.end()+40].strip()[:160],
                })
        for cm in RE_CHAPTER_LABEL.finditer(body_stripped):
            ch = cm.group(1)
            findings["unlinked_chapter_refs"].append({
                "file": fpath,
                "chapter": ch,
                "context": body_stripped[max(0, cm.start()-40):cm.end()+40].strip()[:160],
            })


# -----------------------------------------------------------------------------
# 4. Write outputs
# -----------------------------------------------------------------------------
out_json = os.path.join(ROOT, "docs", "content-audit", "_xref_findings.json")
with open(out_json, "w", encoding="utf-8") as fh:
    json.dump(findings, fh, indent=2)

print()
print("Summary:")
for k, v in findings.items():
    print(f"  {k}: {len(v)}")
print(f"JSON written to {out_json}")
