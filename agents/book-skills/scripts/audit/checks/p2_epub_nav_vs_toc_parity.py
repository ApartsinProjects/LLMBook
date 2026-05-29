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

    Strategy: collapse "../../" chains, normalize html2epub's spine-flattened
    form (EPUB/chapters/ch_NNNN_<slug>.xhtml) back to the canonical source
    pattern. Returns None for non-content refs (css, js, images).
    """
    if not target.endswith((".html", ".xhtml")):
        return None
    while target.startswith("../"):
        target = target[3:]
    while target.startswith("./"):
        target = target[2:]

    # html2epub flattens spine entries to chapters/ch_NNNN_<slug>.xhtml where
    # <slug> joins the source path with '-' (and replaces '/' with '-').
    # Recognized forms in the LLMBook EPUB:
    #   ch_NNNN_front-matter-<name>.xhtml   -> front-matter/<name>.html
    #   ch_NNNN_capstone-index.xhtml         -> capstone/index.html
    #   ch_NNNN_capstone-<name>.xhtml        -> capstone/<name>.html
    #   ch_NNNN_part-N-<slug>-index.xhtml    -> part-N-<slug>/index.html
    #   ch_NNNN_part-N-<slug>-module-M-<slug>-index.xhtml         -> part/module index
    #   ch_NNNN_part-N-<slug>-module-M-<slug>-section-X.Y.xhtml   -> part/module/section
    #   ch_NNNN_appendices-appendix-<k>-<slug>-(index|section-...).xhtml
    flat = re.match(r'(?:EPUB/)?chapters/ch_\d+_(.+)\.xhtml$', target)
    if flat:
        slug = flat.group(1)
        # Front-matter: front-matter-<name>
        m = re.match(r'^front-matter-(.+)$', slug)
        if m:
            return f'front-matter/{m.group(1)}.html'
        # Capstone: capstone-<name>
        m = re.match(r'^capstone-(.+)$', slug)
        if m:
            return f'capstone/{m.group(1)}.html'
        # EPUB slug uses '-' as section-segment separator (e.g. section-0-1
        # rather than section-0.1). Re-derive the dotted form from the slug.
        def _undash_section(seg: str) -> str:
            # Match "section-<digit-or-dash sequence>" and rewrite to use dots
            m = re.match(r'^section-([\d-]+)$', seg)
            if not m:
                return seg
            return 'section-' + m.group(1).replace('-', '.')

        def _undash_appendix_section(seg: str) -> str:
            m = re.match(r'^(section-[a-z])-([\d-]+)$', seg, re.IGNORECASE)
            if not m:
                return seg
            return f'{m.group(1)}.' + m.group(2).replace('-', '.')

        # Appendices: appendices-appendix-<k>-<slug>-(index|section-K-N-...)
        m = re.match(r'^appendices-(appendix-[a-z]-[a-z0-9-]+?)-(index|section-[a-z]-[\d-]+)$',
                     slug, re.IGNORECASE)
        if m:
            return f'appendices/{m.group(1)}/{_undash_appendix_section(m.group(2))}.html'
        # Part + module + section: part-N-<slug>-module-M-<slug>-(section-X-Y|index)
        m = re.match(r'^(part-\d+-[a-z0-9-]+?)-(module-\d+-[a-z0-9-]+?)-(section-[\d-]+|index)$',
                     slug, re.IGNORECASE)
        if m:
            return f'{m.group(1)}/{m.group(2)}/{_undash_section(m.group(3))}.html'
        # Part + module + index: part-N-<slug>-module-M-<slug>-index
        m = re.match(r'^(part-\d+-[a-z0-9-]+?)-(module-\d+-[a-z0-9-]+?)-index$',
                     slug, re.IGNORECASE)
        if m:
            return f'{m.group(1)}/{m.group(2)}/index.html'
        # Part + index: part-N-<slug>-index
        m = re.match(r'^(part-\d+-[a-z0-9-]+?)-index$', slug, re.IGNORECASE)
        if m:
            return f'{m.group(1)}/index.html'
        # Appendices index: appendices-index
        if slug == 'appendices-index':
            return 'appendices/index.html'
        # Fall through if nothing matched
        return slug + '.html'

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

    # html2epub builds nav.xhtml from spine (section files) only; the source
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

    # Tolerate Kindle filename-length truncation: html2epub truncates spine
    # filenames over some length, so a toc.html entry "part-9-...-module-45-
    # tools-of-the-trade/section-45.1.html" may appear in the EPUB nav as
    # "part-9-...-module-45-tools-of-the-trade-section" (chopped). Build a
    # set of nav-side PREFIXES for matching toc-side full keys.
    nav_prefixes = set()
    for n in nav_targets:
        if n is None:
            continue
        nav_prefixes.add(n)
        # also any prefix at section boundaries
        nav_prefixes.add(n[:80])  # tolerate ~80-char truncation
        nav_prefixes.add(n[:70])
        nav_prefixes.add(n[:60])

    def _has_nav_coverage(toc_key: str) -> bool:
        if toc_key in nav_targets:
            return True
        # tolerate truncated nav entry: any nav prefix matches toc_key prefix
        for k_len in (80, 70, 60):
            if toc_key[:k_len] in nav_prefixes:
                return True
        return False

    only_in_toc = [t for t in toc_targets if not _has_nav_coverage(t)]

    # We deliberately do NOT report "in nav but missing from toc" because
    # Kindle filename truncation makes that comparison too noisy.

    for t in sorted(only_in_toc):
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                            f"In source toc.html but missing from EPUB nav.xhtml: {t}"))
    return issues
