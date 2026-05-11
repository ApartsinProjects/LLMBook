"""Strip CSS properties / HTML tags Kindle's converter doesn't support.

Targets the 4 noisiest patterns from KDP's conversion report:
  1. -webkit-box-shadow / box-shadow             (4538 notices)
  2. <summary display:list-item> in <details>    (1694 notices) -> convert to <div>
  3. width: min-content / max-content            (1398 notices)
  4. {padding|margin}-{side}: nullem | nanem     (4446 notices, suspected fatal cause)

Plus generic noise:
  - {caption-side: bottom}
  - any negative margin on tables

Usage:
  python _sanitize_kindle_css.py path/to/epub.epub [output.epub]
  -- or import sanitize() and pass an EPUB Path.
"""
from __future__ import annotations
import re, shutil, sys, zipfile
from pathlib import Path

# Strategy: REPLACE bad values with neutral safe values, don't delete declarations.
# This keeps the CSS syntactically valid even if my regex is imperfect.
#
# Each entry: (regex pattern, replacement) — applied left-to-right.
CSS_VALUE_REPLACEMENTS = [
    # nullem / nanem / undefinedem -> 0
    (re.compile(r':\s*(?:null|nan|undefined)em\b', re.IGNORECASE), ': 0'),
    # min-content / max-content / fit-content -> auto
    (re.compile(r':\s*(?:min|max|fit)-content\b', re.IGNORECASE), ': auto'),
    # negative margins -> 0
    (re.compile(r'(margin(?:-\w+)?\s*:\s*)-\d+(?:\.\d+)?(?:px|em|rem|%)?', re.IGNORECASE), r'\g<1>0'),
    # caption-side: ANY -> Kindle does not support caption positioning. Drop entirely.
    (re.compile(r'(?P<sep>^|;|\{)\s*caption-side\s*:[^;}]+(?=[;}])', re.IGNORECASE),
     lambda m: m.group('sep')),
    # box-shadow (any prefix): REMOVE the declaration entirely (don't even keep "none";
    # Kindle flags '-webkit-box-shadow=none' as unsupported even with our prior fix).
    # Use named group 'sep' to keep ONLY the leading separator (;{ or { or ;)
    # so we don't leave orphan property names like '-webkit-' behind.
    (re.compile(r'(?P<sep>^|;|\{)\s*(?:-webkit-|-moz-|-o-|-ms-)?box-shadow\s*:[^;}]+(?=[;}])', re.IGNORECASE),
     lambda m: m.group('sep')),
    # gap: Kindle CSS engine doesn't understand flex/grid gap; can produce
    # "nullem" reports. Drop the entire declaration (including any
    # row-/column- prefix). Keep only the leading separator (;{ or { or ;).
    (re.compile(r'(?P<sep>^|;|\{)\s*(?:row-|column-)?gap\s*:[^;}]+(?=[;}])', re.IGNORECASE),
     lambda m: m.group('sep')),
    # min() / max() / clamp() in length contexts: Kindle can't compute these
    # Replace the entire CSS function call with a sane fallback.
    # We pick the FIRST argument as a conservative replacement.
    (re.compile(r'\b(?:min|max|clamp)\(\s*([^,()]+?)\s*[,)][^)]*\)', re.IGNORECASE),
     r'\1'),
    # transition / transform / filter / animation: replace value with "none"
    (re.compile(r'(?:^|;|\{)\s*(transition|transform|filter|backdrop-filter|-webkit-backdrop-filter|animation)\s*:[^;}]+(?=[;}])', re.IGNORECASE),
     lambda m: m.group(0).split(':')[0].rstrip() + ': none'),
]

# HTML transforms: <details>/<summary> -> div with bold title (Kindle disclosure unsupported)
DETAILS_OPEN_RE = re.compile(r'<details(?:\s+[^>]*)?>', re.IGNORECASE)
DETAILS_CLOSE_RE = re.compile(r'</details>', re.IGNORECASE)
SUMMARY_RE = re.compile(r'<summary(?:\s+[^>]*)?>(.*?)</summary>', re.IGNORECASE | re.DOTALL)


def _sanitize_text(text: str, is_css: bool) -> tuple[str, int]:
    """Replace Kindle-unsupported CSS with safe neutral values."""
    n = 0
    for pat, repl in CSS_VALUE_REPLACEMENTS:
        new_text, count = pat.subn(repl, text)
        text = new_text
        n += count
    # Post-pass: collapse stray `;;` (left behind when we drop a whole
    # declaration that was preceded by `;`) and `{;` (declaration was
    # the first inside a rule). CSS-ONLY — running these on HTML mangles
    # entity references like `&quot;}` -> `&quot}` which produces fatal
    # XHTML parse errors (RSC-016).
    if is_css:
        text = re.sub(r';\s*;+', ';', text)
        text = re.sub(r'\{\s*;+', '{', text)
        text = re.sub(r';\s*\}', '}', text)
    if not is_css:
        text, n_sum = SUMMARY_RE.subn(r'<p class="details-title"><strong>\1</strong></p>', text)
        text, n_dop = DETAILS_OPEN_RE.subn('<div class="details-shim">', text)
        text, n_dcl = DETAILS_CLOSE_RE.subn('</div>', text)
        n += n_sum + n_dop + n_dcl
    return text, n


def sanitize(in_path: Path, out_path: Path | None = None) -> dict:
    if out_path is None:
        out_path = in_path
    work = in_path.parent / "_kindlecss_temp"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()

    with zipfile.ZipFile(in_path) as z:
        z.extractall(work)

    stats = {"css_files": 0, "html_files": 0, "removals": 0}
    for p in work.rglob("*"):
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        is_css = ext == ".css"
        is_html = ext in (".xhtml", ".html")
        if not (is_css or is_html):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        new_text, n = _sanitize_text(text, is_css)
        if n:
            p.write_text(new_text, encoding="utf-8")
            if is_css:
                stats["css_files"] += 1
            else:
                stats["html_files"] += 1
            stats["removals"] += n

    # Repack EPUB (mimetype first, stored)
    if out_path.exists():
        out_path.unlink()
    mimetype = work / "mimetype"
    with zipfile.ZipFile(out_path, "w") as zout:
        if mimetype.exists():
            zout.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
        for p in sorted(work.rglob("*")):
            if not p.is_file() or p == mimetype:
                continue
            arc = str(p.relative_to(work)).replace("\\", "/")
            zout.write(p, arc, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    shutil.rmtree(work)
    return stats


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    in_p = Path(sys.argv[1])
    out_p = Path(sys.argv[2]) if len(sys.argv) > 2 else in_p
    s = sanitize(in_p, out_p)
    print(f"  Sanitized: {s['removals']} CSS/HTML removals "
          f"({s['css_files']} CSS files, {s['html_files']} HTML chapters)")
    print(f"  Output: {out_p} ({out_p.stat().st_size/1024/1024:.2f} MB)")
