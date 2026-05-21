"""Build a tiny EPUB that reproduces the two Kindle-only layout bugs using the
REAL book.css + epub_overrides.css, for fast KPV iterate-and-render loops.

Page 1: a .chapter-header h1 (heading-justify bug) + the 3-col comparison
table (cascade bug). Bundles the actual stylesheets so KPV sees the same CSS
as the full book.

Usage: py -3 scripts/build_min_epub.py [out.epub]
"""
import sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/Users/apart/AppData/Local/Temp/min-kpv.epub")

BOOK_CSS = (ROOT / "styles/book.css").read_text(encoding="utf-8", errors="replace")
OVR_CSS = (ROOT / "KDP/build/epub_overrides.css").read_text(encoding="utf-8", errors="replace")

CHAP = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Min KPV Test</title>
<link rel="stylesheet" type="text/css" href="styles/book.css"/>
<link rel="stylesheet" type="text/css" href="styles/epub_overrides.css"/>
</head>
<body>
<header class="chapter-header">
<div class="part-label">Part I: LLM Building Blocks</div>
<h1>Chapter 1: Foundations of NLP and Text Representation</h1>
</header>
<main class="content">
<p>The cross-entropy loss penalises confident wrong answers. The table below compares predicted probabilities and their loss.</p>
<div class="comparison-table-title"><strong>Table 0.1.1:</strong> <em>Predicted Probability Comparison.</em></div>
<table>
<thead>
<tr><th scope="col">Predicted Probability</th><th scope="col">Cross-Entropy Loss</th><th scope="col">Interpretation</th></tr>
</thead>
<tbody>
<tr><td>0.9</td><td>0.105</td><td>Confidently correct</td></tr>
<tr><td>0.5</td><td>0.693</td><td>Coin flip</td></tr>
<tr><td>0.1</td><td>2.303</td><td>Mostly wrong</td></tr>
<tr><td>0.01</td><td>4.605</td><td>Catastrophically wrong</td></tr>
</tbody>
</table>
</main>
</body></html>
"""

NAV = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><meta charset="utf-8"/><title>Contents</title></head>
<body><nav epub:type="toc" id="toc"><h1>Contents</h1>
<ol><li><a href="chap.xhtml">Chapter 1: Foundations of NLP and Text Representation</a></li></ol>
</nav></body></html>
"""

OPF = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:uuid:min-kpv-test-0001</dc:identifier>
<dc:title>Min KPV Test</dc:title><dc:language>en</dc:language>
<meta property="dcterms:modified">2026-05-21T00:00:00Z</meta>
</metadata>
<manifest>
<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="chap" href="chap.xhtml" media-type="application/xhtml+xml"/>
<item id="bookcss" href="styles/book.css" media-type="text/css"/>
<item id="ovrcss" href="styles/epub_overrides.css" media-type="text/css"/>
</manifest>
<spine><itemref idref="chap"/></spine>
</package>
"""

CONTAINER = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="EPUB/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
if OUT.exists():
    OUT.unlink()
with zipfile.ZipFile(OUT, "w") as z:
    z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
    z.writestr("META-INF/container.xml", CONTAINER, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("EPUB/content.opf", OPF, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("EPUB/nav.xhtml", NAV, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("EPUB/chap.xhtml", CHAP, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("EPUB/styles/book.css", BOOK_CSS, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("EPUB/styles/epub_overrides.css", OVR_CSS, compress_type=zipfile.ZIP_DEFLATED)
print("wrote", OUT, OUT.stat().st_size, "bytes")
