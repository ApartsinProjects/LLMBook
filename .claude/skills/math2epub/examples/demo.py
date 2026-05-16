"""End-to-end smoke test for math2epub.

Runs both pipelines on the same input set and confirms each returns
plausible output. Writes a small EPUB to ./demo-output/math2epub-demo.epub
that can be dragged into Kindle Previewer 3 to visually verify rendering.

Run from anywhere:
    python .claude/skills/math2epub/examples/demo.py
"""
from __future__ import annotations

import base64
import sys
import uuid
import zipfile
from pathlib import Path

# Make scripts/ importable
HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from math2epub import render_batch  # noqa: E402

OUT_DIR = HERE / "demo-output"
OUT_DIR.mkdir(exist_ok=True)

TESTS = [
    {"id": "0", "tex": r"y_i", "display": False,
     "label": "y subscript i",
     "before": "The output for the i-th example is denoted",
     "after": ", where i runs from 1 to N."},
    {"id": "1", "tex": r"x^2", "display": False,
     "label": "x squared",
     "before": "We square the residual as",
     "after": "before summing across examples."},
    {"id": "2", "tex": r"\frac{1}{n}", "display": False,
     "label": "one over n",
     "before": "Averaging the loss gives the factor",
     "after": "in front of the sum."},
    {"id": "3",
     "tex": r"MSE = \frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2",
     "display": True,
     "label": "MSE block equation",
     "before": "For regression, the most common loss is Mean Squared Error:",
     "after": "Squaring the residual penalizes large errors more heavily."},
]


def build_chapter_xhtml(svgs: dict[str, str], png_refs: dict[str, str]) -> str:
    """Two prose sections per expression: one SVG, one PNG (file ref).

    Compares pipelines side by side in prose context (no table cells, see
    LESSONS L6).
    """
    sections = []
    for t in TESTS:
        idx, display = t["id"], t["display"]
        label, pre, post = t["label"], t["before"], t["after"]
        tex_esc = (t["tex"].replace("&", "&amp;")
                   .replace("<", "&lt;").replace(">", "&gt;"))

        def block(rendered: str, png_ref: bool = False) -> str:
            if display:
                if png_ref:
                    inner = (f'<p>{pre}</p>'
                             f'<div class="math-block">'
                             f'<img class="math-display" src="{rendered}" alt="{tex_esc}"/>'
                             f'</div>'
                             f'<p>{post}</p>')
                else:
                    inner = (f'<p>{pre}</p>'
                             f'<div class="math-block">{rendered}</div>'
                             f'<p>{post}</p>')
            else:
                if png_ref:
                    inner = (f'<p>{pre} '
                             f'<img class="math-inline" src="{rendered}" alt="{tex_esc}"/>'
                             f' {post}</p>')
                else:
                    inner = f'<p>{pre} {rendered} {post}</p>'
            return inner

        sections.append(
            f'<h2>Expression <code>{tex_esc}</code> (&#8220;{label}&#8221;)</h2>\n'
            f'<div class="section-card"><h3>SVG</h3>\n{block(svgs[idx])}\n</div>\n'
            f'<div class="section-card"><h3>PNG</h3>\n{block(png_refs[idx], png_ref=True)}\n</div>'
        )

    body = "\n".join(sections)
    css = (
        "body{font-family:Georgia,serif;line-height:1.7;margin:1em auto;"
        "max-width:38em;padding:0 1em;color:#222;background:#fff}"
        "h1{font-size:1.4em;border-bottom:2px solid #1a4078;padding-bottom:0.3em;margin-top:0}"
        "h2{font-size:1.15em;color:#1a4078;margin:1.8em 0 0.2em;"
        "border-bottom:1px solid #ddd;padding-bottom:0.15em}"
        "h3{font-size:0.95em;color:#555;margin:0.6em 0 0.1em;"
        "text-transform:uppercase;letter-spacing:0.05em;font-weight:700}"
        "p{margin:0.3em 0 0.7em}"
        "code{background:#f4f4f4;padding:0.1em 0.3em;border-radius:3px;"
        "font-size:0.85em;font-family:Consolas,monospace}"
        ".section-card{background:#fafafa;border-left:3px solid #1a4078;"
        "padding:0.5em 0.9em;margin:0.4em 0 1.2em}"
        ".math-block{text-align:center;margin:0.6em 0}"
        ".math-block img.math-display{max-width:100%;height:auto}"
        "img.math-inline{vertical-align:middle;max-height:1.5em}"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" lang="en">\n'
        '<head><meta charset="utf-8"/><title>math2epub demo</title>'
        f'<style>{css}</style></head>\n'
        f'<body><h1>math2epub demo: SVG and PNG side by side</h1>\n{body}\n</body></html>\n'
    )


def write_epub(svgs: dict[str, str], pngs: dict[str, bytes], path: Path) -> None:
    """Bundle the chapter and PNG files into a valid EPUB 3."""
    png_refs = {k: f"img/eq{int(k):02d}.png" for k in pngs}
    chapter = build_chapter_xhtml(svgs, png_refs)

    bookid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_OID, "math2epub-demo"))
    png_manifest = "\n    ".join(
        f'<item id="img{int(k):02d}" href="img/eq{int(k):02d}.png" '
        f'media-type="image/png"/>'
        for k in pngs
    )
    opf = (
        '<?xml version="1.0"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="id" '
        'version="3.0" prefix="rendition: http://www.idpf.org/vocab/rendition/#">\n'
        '  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f'    <dc:identifier id="id">{bookid}</dc:identifier>\n'
        '    <dc:title>math2epub demo</dc:title>\n'
        '    <dc:language>en</dc:language>\n'
        '    <meta property="dcterms:modified">2026-05-15T23:30:00Z</meta>\n'
        '    <meta property="rendition:layout">reflowable</meta>\n'
        '  </metadata>\n'
        '  <manifest>\n'
        '    <item id="page" href="page.xhtml" media-type="application/xhtml+xml" properties="svg"/>\n'
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n'
        f'    {png_manifest}\n'
        '  </manifest>\n'
        '  <spine><itemref idref="page"/></spine>\n'
        '</package>'
    )
    nav = (
        '<?xml version="1.0"?>\n<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" lang="en">\n'
        '<head><meta charset="utf-8"/><title>Nav</title></head>\n'
        '<body><nav epub:type="toc"><h1>Contents</h1>'
        '<ol><li><a href="page.xhtml">math2epub demo</a></li></ol></nav></body></html>'
    )
    with zipfile.ZipFile(path, "w") as z:
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        z.writestr(zi, "application/epub+zip")
        z.writestr(
            "META-INF/container.xml",
            '<?xml version="1.0"?>\n'
            '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">\n'
            '<rootfiles><rootfile media-type="application/oebps-package+xml" '
            'full-path="EPUB/content.opf"/></rootfiles></container>',
        )
        z.writestr("EPUB/content.opf", opf)
        z.writestr("EPUB/nav.xhtml", nav)
        z.writestr("EPUB/page.xhtml", chapter)
        for k, b in pngs.items():
            z.writestr(f"EPUB/img/eq{int(k):02d}.png", b)


def main() -> None:
    print("Rendering SVG pipeline...")
    svgs = render_batch(TESTS, pipeline="svg")
    for k, v in svgs.items():
        assert v.startswith("<svg"), f"SVG[{k}] does not start with <svg"
        print(f"  [{k}] {len(v):,} chars")

    print("Rendering PNG pipeline...")
    pngs = render_batch(TESTS, pipeline="png")
    for k, v in pngs.items():
        assert v.startswith(b"\x89PNG"), f"PNG[{k}] not a PNG"
        print(f"  [{k}] {len(v):,} bytes")

    epub_path = OUT_DIR / "math2epub-demo.epub"
    write_epub(svgs, pngs, epub_path)
    print(f"Wrote {epub_path} ({epub_path.stat().st_size:,} bytes)")
    print()
    print("Next: validate with")
    print(f"  python {SCRIPTS / 'validate.py'} {epub_path}")
    print("Then drag the EPUB into Kindle Previewer 3.")


if __name__ == "__main__":
    main()
