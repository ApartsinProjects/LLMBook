"""Verify toc.html against actual file structure on disk."""
import os
import re
from html.parser import HTMLParser

BASE = r"E:\Projects\LLMCourse"
TOC_PATH = os.path.join(BASE, "toc.html")

# ── Parse toc.html ──────────────────────────────────────────────────────────

with open(TOC_PATH, "r", encoding="utf-8") as f:
    toc_html = f.read()

class TocParser(HTMLParser):
    """Extract links from #toc-short and #toc-detailed divs."""
    def __init__(self):
        super().__init__()
        self.current_div = None  # 'toc-short' or 'toc-detailed'
        self.div_depth = 0
        self.links = {"toc-short": [], "toc-detailed": []}
        # For capturing link text
        self.in_a = False
        self.current_href = None
        self.current_text_parts = []

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "div" and ad.get("id") in ("toc-short", "toc-detailed"):
            self.current_div = ad["id"]
            self.div_depth = 1
            return
        if self.current_div and tag == "div":
            self.div_depth += 1
        if self.current_div and tag == "a":
            href = ad.get("href", "")
            if href and not href.startswith("#") and not href.startswith("http"):
                self.in_a = True
                self.current_href = href
                self.current_text_parts = []

    def handle_endtag(self, tag):
        if self.current_div and tag == "a" and self.in_a:
            text = "".join(self.current_text_parts).strip()
            # Remove leading section number like "0.1 " or "FM.1 "
            self.links[self.current_div].append((self.current_href, text))
            self.in_a = False
            self.current_href = None
        if self.current_div and tag == "div":
            self.div_depth -= 1
            if self.div_depth == 0:
                self.current_div = None

    def handle_data(self, data):
        if self.in_a:
            self.current_text_parts.append(data)

parser = TocParser()
parser.feed(toc_html)

short_links = parser.links["toc-short"]
detailed_links = parser.links["toc-detailed"]

print(f"=== ToC LINK COUNTS ===")
print(f"Short ToC links:    {len(short_links)}")
print(f"Detailed ToC links: {len(detailed_links)}")
print()

# ── 1. Verify each link exists on disk ──────────────────────────────────────

def check_links(links, label):
    missing = []
    for href, text in links:
        # Normalize path
        fpath = os.path.join(BASE, href.replace("/", os.sep))
        if not os.path.isfile(fpath):
            missing.append((href, text))
    if missing:
        print(f"=== MISSING FILES referenced in {label} ({len(missing)}) ===")
        for href, text in missing:
            print(f"  MISSING: {href}  ({text})")
    else:
        print(f"=== All {label} links resolve to existing files. ===")
    print()
    return missing

check_links(short_links, "#toc-short")
check_links(detailed_links, "#toc-detailed")

# ── 2. Find orphan section files not in detailed ToC ────────────────────────

detailed_hrefs = set(h for h, _ in detailed_links)
short_hrefs = set(h for h, _ in short_links)

# Walk disk for section-*.html files
disk_sections = []
for root, dirs, files in os.walk(BASE):
    # Skip hidden dirs and underscore dirs
    dirs[:] = [d for d in dirs if not d.startswith(".") and not d.startswith("_")]
    for fn in files:
        if fn.startswith("section-") and fn.endswith(".html"):
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, BASE).replace(os.sep, "/")
            disk_sections.append(rel)

disk_sections.sort()

orphans_detailed = [s for s in disk_sections if s not in detailed_hrefs]
orphans_short = [s for s in disk_sections if s not in short_hrefs]

if orphans_detailed:
    print(f"=== ORPHAN SECTIONS: on disk but NOT in #toc-detailed ({len(orphans_detailed)}) ===")
    for s in orphans_detailed:
        print(f"  {s}")
else:
    print("=== No orphan sections (all disk sections are in #toc-detailed). ===")
print()

if orphans_short:
    print(f"=== ORPHAN SECTIONS: on disk but NOT in #toc-short ({len(orphans_short)}) ===")
    for s in orphans_short:
        print(f"  {s}")
else:
    print("=== No orphan sections (all disk sections are in #toc-short). ===")
print()

# ── 3. Section count per chapter ────────────────────────────────────────────

# Also collect index.html files on disk
disk_indexes = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if not d.startswith(".") and not d.startswith("_")]
    for fn in files:
        if fn == "index.html" and root != BASE:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, BASE).replace(os.sep, "/")
            disk_indexes.append(rel)

# Group sections by parent directory
from collections import defaultdict

def group_by_dir(paths):
    g = defaultdict(list)
    for p in paths:
        d = "/".join(p.split("/")[:-1])
        g[d].append(p)
    return g

disk_by_dir = group_by_dir(disk_sections)

# Group detailed ToC section links by directory
toc_sections_only = [(h, t) for h, t in detailed_links if "/section-" in h]
toc_by_dir = defaultdict(list)
for h, t in toc_sections_only:
    d = "/".join(h.split("/")[:-1])
    toc_by_dir[d].append((h, t))

all_dirs = sorted(set(list(disk_by_dir.keys()) + list(toc_by_dir.keys())))

mismatched_counts = []
for d in all_dirs:
    disk_count = len(disk_by_dir.get(d, []))
    toc_count = len(toc_by_dir.get(d, []))
    if disk_count != toc_count:
        mismatched_counts.append((d, disk_count, toc_count))

if mismatched_counts:
    print(f"=== SECTION COUNT MISMATCHES (disk vs toc-detailed) ({len(mismatched_counts)}) ===")
    for d, dc, tc in mismatched_counts:
        print(f"  {d}: disk={dc}, toc={tc}")
        disk_files = set(os.path.basename(p) for p in disk_by_dir.get(d, []))
        toc_files = set(os.path.basename(h) for h, _ in toc_by_dir.get(d, []))
        only_disk = disk_files - toc_files
        only_toc = toc_files - disk_files
        if only_disk:
            print(f"    On disk only: {sorted(only_disk)}")
        if only_toc:
            print(f"    In ToC only:  {sorted(only_toc)}")
else:
    print("=== Section counts match for all chapters. ===")
print()

# ── 4. Verify section titles match ─────────────────────────────────────────

def extract_title_from_file(filepath):
    """Extract the <h1> or first heading text from an HTML file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(8000)  # First 8K should contain the title
    except Exception as e:
        return f"[ERROR reading: {e}]"

    # Try <h1 ...>...</h1>
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if m:
        # Strip inner tags
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        # Normalize whitespace
        title = re.sub(r'\s+', ' ', title)
        return title
    return "[NO H1 FOUND]"

def normalize_html_entities(s):
    """Decode common HTML entities for comparison."""
    s = s.replace("&amp;", "&")
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&#8211;", "\u2013")
    s = s.replace("&ndash;", "\u2013")
    s = s.replace("&#8212;", "\u2014")
    s = s.replace("&mdash;", "\u2014")
    s = s.replace("&nbsp;", " ")
    return s

def normalize_for_compare(s):
    """Normalize a title string for fuzzy comparison."""
    s = normalize_html_entities(s)
    # Remove leading section numbers like "0.1 ", "FM.1 ", "Section 0.1: "
    s = re.sub(r'^(Section\s+)?\d+\.\d+[:\s]+', '', s)
    s = re.sub(r'^(Section\s+)?FM\.\d+[:\s]+', '', s)
    s = re.sub(r'^(Chapter\s+)?\d+[:\s]+', '', s)
    # Normalize whitespace and case
    s = re.sub(r'\s+', ' ', s).strip()
    return s

title_mismatches = []
for href, toc_text in detailed_links:
    if "/section-" not in href:
        continue
    fpath = os.path.join(BASE, href.replace("/", os.sep))
    if not os.path.isfile(fpath):
        continue  # Already reported as missing
    file_title = extract_title_from_file(fpath)

    # Normalize both for comparison
    norm_toc = normalize_for_compare(toc_text)
    norm_file = normalize_for_compare(file_title)

    if norm_toc.lower() != norm_file.lower():
        title_mismatches.append((href, toc_text, file_title, norm_toc, norm_file))

if title_mismatches:
    print(f"=== TITLE MISMATCHES (toc-detailed vs file <h1>) ({len(title_mismatches)}) ===")
    for href, toc_t, file_t, nt, nf in title_mismatches:
        print(f"  {href}")
        print(f"    ToC:  {toc_t!r}")
        print(f"    File: {file_t!r}")
else:
    print("=== All section titles match between toc-detailed and files. ===")
print()

# ── 5. Check short ToC titles too ──────────────────────────────────────────

short_title_mismatches = []
for href, toc_text in short_links:
    fpath = os.path.join(BASE, href.replace("/", os.sep))
    if not os.path.isfile(fpath):
        continue
    file_title = extract_title_from_file(fpath)
    norm_toc = normalize_for_compare(toc_text)
    norm_file = normalize_for_compare(file_title)
    if norm_toc.lower() != norm_file.lower():
        short_title_mismatches.append((href, toc_text, file_title))

if short_title_mismatches:
    print(f"=== TITLE MISMATCHES (toc-short vs file <h1>) ({len(short_title_mismatches)}) ===")
    for href, toc_t, file_t in short_title_mismatches:
        print(f"  {href}")
        print(f"    ToC:  {toc_t!r}")
        print(f"    File: {file_t!r}")
else:
    print("=== All short ToC titles match files. ===")
print()

# ── 6. Check for index.html on disk not in any ToC ─────────────────────────

all_toc_hrefs = detailed_hrefs | short_hrefs
orphan_indexes = [p for p in disk_indexes if p not in all_toc_hrefs]
# Filter to only module/part indexes (not the root ones)
orphan_indexes = [p for p in orphan_indexes if "module-" in p or ("part-" in p and p.count("/") == 1)]

if orphan_indexes:
    print(f"=== INDEX FILES on disk not in either ToC ({len(orphan_indexes)}) ===")
    for p in sorted(orphan_indexes):
        print(f"  {p}")
else:
    print("=== All index files are referenced in at least one ToC. ===")
print()

print("=== VERIFICATION COMPLETE ===")
