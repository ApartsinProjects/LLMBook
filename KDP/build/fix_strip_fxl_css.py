"""Post-build EPUB patch: strip KDP-disallowed CSS rules from stylesheets.

DEEP-HUNT finding: KDP's official "Creating Reflowable Books" help page
explicitly disallows `position:` in reflowable EPUBs. Our book.css has
ONE `position:fixed` rule (on the web-only .header-search #search element)
plus several `display:grid` rules and `vh/vw` units pointing at other
web-only elements we've already removed from the DOM via the chrome-strip
patch. These CSS rules are now DEAD CODE, but KDP's classifier doesn't
know that — it scans the CSS and likely flips fixed-format on the
presence of any disallowed property.

What this patch does:
  Removes (replaces with a no-op default) CSS declarations that KDP
  explicitly disallows or strongly associates with fixed-layout:

  - position: fixed | absolute | sticky          -> remove
  - display: grid | inline-grid                  -> change to block
  - display: flex | inline-flex                  -> change to block
  - any value containing vh/vw/vmin/vmax units   -> remove the declaration

Done at the DECLARATION level (one `prop:value;`) not the rule level,
so we keep the rest of each selector's styling intact.

Run AFTER fix_strip_web_chrome.py (chrome already removed from DOM,
making these CSS rules safe to delete entirely).
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path


# These match a single declaration: prop: value [!important] ;
# We strip the entire declaration (including trailing semicolon and spaces).
STRIP_PATTERNS = [
    # position: fixed / absolute / sticky
    re.compile(r'\bposition\s*:\s*(?:fixed|absolute|sticky)\s*(?:!important)?\s*;?', re.IGNORECASE),
    # display: grid (inline-grid)
    re.compile(r'\bdisplay\s*:\s*(?:inline-)?grid\s*(?:!important)?\s*;?', re.IGNORECASE),
    # display: flex (inline-flex)
    re.compile(r'\bdisplay\s*:\s*(?:inline-)?flex\s*(?:!important)?\s*;?', re.IGNORECASE),
    # any declaration whose value includes vh/vw/vmin/vmax
    re.compile(r'\b[a-zA-Z-]+\s*:\s*[^;}]*\b\d+(?:\.\d+)?v(?:h|w|min|max)\b[^;}]*(?:!important)?\s*;?', re.IGNORECASE),
    # grid-template-* (orphan after display:grid removal)
    re.compile(r'\bgrid-(?:template|gap|column|row|auto|area|areas)[a-z-]*\s*:[^;}]*(?:!important)?\s*;?', re.IGNORECASE),
    # gap (flex/grid only)
    re.compile(r'\bgap\s*:\s*[\d.]+(?:em|px|rem)\s*(?:!important)?\s*;?', re.IGNORECASE),
]


def strip_css(css: str) -> tuple[str, dict]:
    stats = {'position_removed': 0, 'display_grid_removed': 0,
             'display_flex_removed': 0, 'vh_vw_removed': 0,
             'grid_props_removed': 0, 'gap_removed': 0}
    counters = ['position_removed', 'display_grid_removed', 'display_flex_removed',
                'vh_vw_removed', 'grid_props_removed', 'gap_removed']
    for i, pat in enumerate(STRIP_PATTERNS):
        css, n = pat.subn('', css)
        stats[counters[i]] = n
    return css, stats


def patch(epub_path: Path) -> dict:
    totals = {'files_scanned': 0, 'files_modified': 0,
              'position_removed': 0, 'display_grid_removed': 0,
              'display_flex_removed': 0, 'vh_vw_removed': 0,
              'grid_props_removed': 0, 'gap_removed': 0}

    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED)
                break
        for info in zin.infolist():
            if info.filename == 'mimetype':
                continue
            data = zin.read(info.filename)
            if info.filename.lower().endswith('.css'):
                totals['files_scanned'] += 1
                css = data.decode('utf-8', errors='ignore')
                new_css, s = strip_css(css)
                if any(s[k] for k in s):
                    totals['files_modified'] += 1
                    for k in s:
                        totals[k] += s[k]
                    data = new_css.encode('utf-8')
            elif info.filename.lower().endswith(('.xhtml', '.html')):
                # Also strip from inline <style> blocks
                html = data.decode('utf-8', errors='ignore')
                STYLE_RE = re.compile(r'(<style\b[^>]*>)(.*?)(</style>)', re.DOTALL | re.IGNORECASE)
                def style_repl(m):
                    inner, s = strip_css(m.group(2))
                    for k in s:
                        totals[k] += s[k]
                    return m.group(1) + inner + m.group(3)
                new_html = STYLE_RE.sub(style_repl, html)
                if new_html != html:
                    totals['files_modified'] += 1
                    data = new_html.encode('utf-8')
            zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
    os.replace(tmp_out, epub_path)
    return totals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Stripping FXL-flagged CSS from {args.epub}')
    t = patch(args.epub)
    print(f'  Files scanned:           {t["files_scanned"]}')
    print(f'  Files modified:          {t["files_modified"]}')
    print(f'  position:fixed/abs/sticky removed: {t["position_removed"]}')
    print(f'  display:grid removed:    {t["display_grid_removed"]}')
    print(f'  display:flex removed:    {t["display_flex_removed"]}')
    print(f'  vh/vw value-decls removed: {t["vh_vw_removed"]}')
    print(f'  grid-* props removed:    {t["grid_props_removed"]}')
    print(f'  gap props removed:       {t["gap_removed"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
