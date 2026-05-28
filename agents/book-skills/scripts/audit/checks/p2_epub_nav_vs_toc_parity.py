"""Compare EPUB nav.xhtml against source toc.html for parity.

The built EPUB's nav.xhtml and the source toc.html should reference the
same set of chapters and sections. Drift causes:
  - Pages that ship in the EPUB but readers can't reach from the source
    web ToC (or vice versa)
  - Different ordering between web and Kindle navigation

Triggered: once, when the plugin sees toc.html. Reads the built EPUB
(KDP/output/<name>.epub) and extracts its nav.xhtml. If the EPUB does
not exist yet (pre-build), the plugin silently passes.
"""
import re
import zipfile
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "EPUB_TOC_PARITY"
DESCRIPTION = "EPUB nav.xhtml and source toc.html reference different sets of pages"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])


def _normalize_targets(text: str) -> set:
    """Extract href targets (sans fragment) from any HTML/XHTML."""
    raw = re.findall(r'href="([^"#]+)', text)
    out = set()
    for r in raw:
        if r.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
            continue
        # Normalize Windows paths; strip leading ../ chain; keep basename + parent dir for matching
        r = r.replace("\\", "/")
        out.add(r)
    return out


def _key(target: str) -> str | None:
    """Produce a stable key from a target href so toc.html refs and
    nav.xhtml refs (which live at different depths) can be compared.

    Strategy: collapse "../../" chains, normalize html2pub's spine-flattened
    form (EPUB/chapters/ch_NNNN_<slug>.xhtml) back to the canonical source
    pattern. Returns None for non-content refs (css, js, images).
    """
    if not target.endswith((".html", ".xhtml")):
        return None
    while target.startswith("../"):
        target = target[3:]
    while target.startswith("./"):
        target = target[2:]

    # Match canonical patterns
    patterns = [
        r"(part-\d+-[^/]+/module-\d+-[^/]+/(?:section-[\d.]+|index)\.html)",
        r"(part-\d+-[^/]+/index\.html)",
        r"(appendices/appendix-[a-z]-[^/]+/(?:section-[a-z]\.[\d.]+|index)\.html)",
        r"(capstone/index\.html)",
        r"(front-matter/[^/]+\.html)",
    ]
    for pat in patterns:
        m = re.search(pat, target, re.IGNORECASE)
        if m:
            return m.group(1).lower()
    return None


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]

    if not (filepath.name == "toc.html" and filepath.parent == book_root):
        return issues

    # Find the built EPUB
    epub_candidates = sorted((book_root / "KDP" / "output").glob("*.epub"))
    # Prefer the file without ".raw" / "-light" / "-reflowable" suffix
    epub_path = None
    for p in epub_candidates:
        if any(s in p.name for s in (".raw.", "-light", "-reflowable", "math-")):
            continue
        epub_path = p
        break
    if epub_path is None:
        return issues  # no built EPUB yet; skip silently

    # Extract nav.xhtml from the EPUB
    try:
        with zipfile.ZipFile(epub_path) as z:
            nav_name = None
            for n in z.namelist():
                if n.endswith("nav.xhtml") or n.endswith("toc.xhtml"):
                    nav_name = n
                    break
            if nav_name is None:
                return issues
            nav_html = z.read(nav_name).decode("utf-8", errors="replace")
    except Exception as e:
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                            f"Failed to read nav.xhtml from {epub_path.name}: {e}"))
        return issues

    # html2pub builds nav.xhtml from spine (section files) only; the source
    # toc.html also links to chapter/part LANDING pages. That's by design,
    # not a defect. Compare only the OVERLAP-eligible pages:
    #   - section-X.Y.html (chapter sections)
    #   - appendices/appendix-K/section-K.N.html
    #   - capstone/index.html
    #   - front-matter/*.html
    # Skip chapter/part index pages on both sides.
    def _is_eligible(key: str) -> bool:
        if key is None:
            return False
        if key.endswith("/index.html"):
            # only capstone/index.html is eligible; everything else is a landing page
            return key == "capstone/index.html"
        return True

    toc_targets = {_key(t) for t in _normalize_targets(html)}
    nav_targets = {_key(t) for t in _normalize_targets(nav_html)}
    toc_targets = {t for t in toc_targets if _is_eligible(t)}
    nav_targets = {t for t in nav_targets if _is_eligible(t)}

    only_in_toc = toc_targets - nav_targets
    only_in_nav = nav_targets - toc_targets

    for t in sorted(only_in_toc):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                            f"In source toc.html but missing from EPUB nav.xhtml: {t}"))
    for t in sorted(only_in_nav):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                            f"In EPUB nav.xhtml but missing from source toc.html: {t}"))
    return issues
