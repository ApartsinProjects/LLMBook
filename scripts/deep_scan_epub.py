"""Deep structural scan of the BUILT EPUB for reader-facing issues that
EPUBCheck and Kindle Previewer qualitychecks pass clean but still look wrong
on a Kindle:

  CODE-WS     <pre> whose text starts/ends with a blank line (visible gap)
  CODE-LONG   code line > 88 chars (horizontal overflow on 6" Kindle)
  TABLE-WIDE  table with >= 5 columns (overflows narrow column)
  IMG-NODIM   <img> without width AND height (reflow jank / oversize)
  EMPTY-EL    empty <p>/<li>/<td>/<h*> (stray blank line / bullet)
  INLINE-STY  style="" on a block element other than <img>/<svg> (Kindle
              strips many props -> layout shift)
  NEST-TABLE  <table> inside a .callout (KF8 nested-table breakage)

Pass --part <prefix> to focus the per-finding listing on one part (e.g.
"part-13"); book-wide COUNTS are always printed so a local pattern can be
generalized.

Usage: py -3 scripts/deep_scan_epub.py [epub] [--part part-13]
"""
from __future__ import annotations
import sys, zipfile, re
from collections import Counter, defaultdict
from pathlib import Path
from bs4 import BeautifulSoup

part = None
if "--part" in sys.argv:
    pi = sys.argv.index("--part")
    part = sys.argv[pi + 1]
epub_args = [a for a in sys.argv[1:] if a.endswith(".epub")]
EPUB = Path(epub_args[0]) if epub_args else Path("KDP/output/building-conversational-ai-llms-agents.epub")

z = zipfile.ZipFile(EPUB)
xh = [n for n in z.namelist() if n.endswith((".xhtml", ".html"))]

counts = Counter()
part_hits = defaultdict(list)

def note(code, chap, detail=""):
    counts[code] += 1
    if part and part in chap:
        part_hits[code].append(f"{chap.split('/')[-1]}: {detail}")

for n in xh:
    raw = z.read(n).decode("utf-8", "replace")
    soup = BeautifulSoup(raw, "html.parser")

    for pre in soup.find_all("pre"):
        txt = pre.get_text()
        # leading/trailing blank line (newline then whitespace-only then content)
        if txt.startswith("\n") and txt.lstrip("\n") != txt.lstrip():
            note("CODE-WS", n, "leading blank")
        elif re.match(r"[ \t]*\n", txt) and txt.strip() and txt[:txt.index(chr(10))].strip() == "" if "\n" in txt else False:
            note("CODE-WS", n, "leading blank")
        if txt.rstrip(" \t").endswith("\n\n") or (txt.endswith("\n") and txt.rstrip("\n") != txt.rstrip()):
            note("CODE-WS", n, "trailing blank")
        for line in txt.split("\n"):
            if len(line) > 88:
                note("CODE-LONG", n, f"{len(line)} chars")
                break

    for t in soup.find_all("table"):
        # max columns = max cells in any row
        maxc = 0
        for tr in t.find_all("tr"):
            c = len(tr.find_all(["td", "th"]))
            maxc = max(maxc, c)
        # Only a problem if NOT already wrapped for narrow viewports. wrap_wide_tables
        # puts >=4-col tables in .table-wide-wrap / .complex-table (font-shrunk +
        # horizontally scrollable), which is the intended handling.
        wrapped = bool(t.find_parent(class_=["table-wide-wrap", "complex-table", "table-wrapper"])) \
            or "complex-table" in (t.get("class") or [])
        if maxc >= 5 and not wrapped:
            note("TABLE-WIDE", n, f"{maxc} cols, unwrapped")
        # nested in callout?
        if t.find_parent(class_="callout"):
            note("NEST-TABLE", n)

    for img in soup.find_all("img"):
        if "cover" in n.lower():
            continue  # the auto-generated cover is full-page; no dims is correct
        if not (img.get("width") and img.get("height")):
            note("IMG-NODIM", n, img.get("src", "")[:40])

    for tag in soup.find_all(["p", "li", "td", "h1", "h2", "h3", "h4"]):
        if not tag.get_text(strip=True) and not tag.find(["img", "svg", "br", "input"]):
            # empty <td> is a legitimate blank table cell; don't flag
            if tag.name == "td":
                continue
            note("EMPTY-EL", n, f"<{tag.name}>")

    # Inline style: only STRUCTURAL/layout props that Kindle's KF8 strips or
    # mishandles are a real risk (position, float, flex/grid, transform, z-index,
    # columns). Cosmetic inline styles (text-align, color, margin, font-*, border,
    # background) render fine OR fall back to the stylesheet. Skip SVG internals.
    PROBLEM_STYLE = re.compile(
        r"\b(position|float|display\s*:\s*(flex|grid|inline-flex|inline-grid)|"
        r"transform|z-index|column-count|columns|clip-path|backdrop-filter)\b",
        re.IGNORECASE)
    for tag in soup.find_all(style=True):
        if tag.name in ("img", "svg", "span", "td", "th", "col", "colgroup"):
            continue
        if tag.find_parent("svg") is not None or tag.name in (
                "stop", "rect", "circle", "path", "g", "text", "line", "polygon",
                "polyline", "ellipse", "tspan", "defs", "marker", "use"):
            continue
        if PROBLEM_STYLE.search(tag.get("style", "")):
            note("INLINE-STY", n, f"<{tag.name}> {tag.get('style','')[:40]}")

# INFO codes are benign-by-design (handled by CSS/hooks); reported separately
# so the WARNING list stays meaningful.
#   CODE-LONG  -> pre{white-space:pre-wrap} wraps it
#   NEST-TABLE -> simple tables in callouts convert + render fine (KPV 0 errors)
INFO_CODES = {"CODE-LONG", "NEST-TABLE"}

print(f"=== deep scan: {EPUB.name} ({len(xh)} chapters) ===\n")
warn_total = sum(c for code, c in counts.items() if code not in INFO_CODES)
print(f"WARNINGS ({warn_total}):")
for code, c in counts.most_common():
    if code not in INFO_CODES:
        print(f"  {code:12} {c}")
print("\nINFO (benign by design):")
for code, c in counts.most_common():
    if code in INFO_CODES:
        print(f"  {code:12} {c}")
print("\nBOOK-WIDE COUNTS:")
for code, c in counts.most_common():
    print(f"  {code:12} {c}")
if part:
    print(f"\n--- {part} findings ---")
    for code in counts:
        hits = part_hits.get(code, [])
        if hits:
            print(f"\n{code} ({len(hits)} in {part}):")
            for h in hits[:15]:
                print("   ", h)
            if len(hits) > 15:
                print(f"    ... +{len(hits)-15} more")
