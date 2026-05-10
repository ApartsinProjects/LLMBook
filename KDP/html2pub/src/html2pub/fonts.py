"""Font discovery and bundling."""
from __future__ import annotations

import re
from pathlib import Path

from html2pub.config import FontsSpec

FONT_MIME = {
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
}


def discover(spec: FontsSpec) -> list[Path]:
    """Resolve glob patterns to a list of font files (absolute paths)."""
    out: list[Path] = []
    for pat in spec.include:
        # Pat may be absolute, with wildcards
        p = Path(pat)
        if p.is_absolute():
            base = p.parent
            glob = p.name
        else:
            base = Path(".")
            glob = pat
        if any(c in glob for c in "*?["):
            for f in sorted(base.glob(glob)):
                if f.is_file() and f.suffix.lower() in FONT_MIME:
                    out.append(f.resolve())
        else:
            if p.exists() and p.is_file() and p.suffix.lower() in FONT_MIME:
                out.append(p.resolve())
    # de-dupe preserving order
    seen = set()
    deduped = []
    for f in out:
        if f not in seen:
            seen.add(f)
            deduped.append(f)
    return deduped


def rewrite_katex_css_to_woff2(css_text: str) -> str:
    """Drop woff and ttf entries from KaTeX @font-face src lists."""
    css_text = re.sub(r',\s*url\([^)]+\.woff\)\s*format\("woff"\)', "", css_text)
    css_text = re.sub(r',\s*url\([^)]+\.ttf\)\s*format\("truetype"\)', "", css_text)
    return css_text
