#!/usr/bin/env /c/Python314/python
"""Read-only audit: identify high-leverage templating / unification opportunities.

Scans every HTML file under part-*/, appendices/, plus toc.html and
appendices/index.html, looking for:

  1. Repeated HTML skeletons (head, header, footer, navs, bibliography,
     whats-next, chapter-card structures, common callouts).
  2. Inline `style="..."` attributes that duplicate or could become a CSS class.
  3. Repeated text snippets (epigraphs, disclaimers, prerequisite paragraphs).
  4. Inline `<script>` blocks duplicated across pages (PagefindUI init, etc).
  5. Asset duplication (same image referenced through different relative paths).
  6. Single-source-of-truth violations (same numeric fact stated differently).
  7. Magic numbers / repeated CSS values that should be CSS variables (inline).

The script is READ-ONLY. It prints a ranked list of unification opportunities
ordered roughly by (impact = duplicate_count) and (effort = type of fix).

Usage:
  /c/Python314/python scripts/_audit_templating_opportunities.py
"""

from __future__ import annotations

import collections
import hashlib
import os
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: BeautifulSoup4 not available. Install with: pip install beautifulsoup4")
    sys.exit(2)

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {"KDP", ".claude", "node_modules", "build", "pagefind", "vendor",
             "_concept-figs"}
SKIP_PREFIXES = ("temp_",)


def in_scope(p: Path) -> bool:
    if p.suffix.lower() != ".html":
        return False
    rel = p.relative_to(ROOT)
    for part in rel.parts:
        if part in SKIP_DIRS:
            return False
        if any(part.startswith(pref) for pref in SKIP_PREFIXES):
            return False
    return True


def collect_html_files() -> list[Path]:
    files: list[Path] = []
    # Top-level files of interest
    for name in ("toc.html", "index.html"):
        p = ROOT / name
        if p.exists():
            files.append(p)
    # Appendices index
    aidx = ROOT / "appendices" / "index.html"
    if aidx.exists():
        files.append(aidx)
    # All HTML under part-*/, appendices/
    for top in sorted(ROOT.glob("part-*")):
        if top.is_dir():
            for p in top.rglob("*.html"):
                if in_scope(p):
                    files.append(p)
    aroot = ROOT / "appendices"
    if aroot.exists():
        for p in aroot.rglob("*.html"):
            if in_scope(p) and p not in files:
                files.append(p)
    return sorted(set(files))


def short_path(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def normalize_block(s: str) -> str:
    """Collapse whitespace so near-identical blocks compare equal."""
    s = re.sub(r"\s+", " ", s).strip()
    return s


def hash_block(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()[:12]


def main() -> None:
    files = collect_html_files()
    print(f"# Templating / Unification Audit")
    print(f"Scanned {len(files)} HTML files under {short_path(ROOT)}/\n")

    # Per-file source cache (raw text + soup)
    raw: dict[Path, str] = {}
    soups: dict[Path, BeautifulSoup] = {}
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"SKIP {short_path(p)}: {e}")
            continue
        raw[p] = text
        soups[p] = BeautifulSoup(text, "html.parser")

    # ---------- 1. HEAD blocks ----------------------------------------------
    head_sigs: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        head = soup.find("head")
        if not head:
            continue
        # Signature: ordered list of (tag, key attrs without text)
        parts = []
        for child in head.find_all(recursive=False):
            attrs = {}
            for k in ("rel", "href", "src", "name", "charset"):
                v = child.get(k)
                if v is None:
                    continue
                # bs4 may return list-like for multi-value attrs
                if isinstance(v, (list, tuple)):
                    v = " ".join(str(x) for x in v)
                v = str(v)
                # Strip the relative-up-prefix so files at different depths
                # still match (e.g. ../../ vs ../).
                v = re.sub(r"^(\.\./)+", "", v)
                attrs[k] = v
            parts.append((child.name, tuple(sorted(attrs.items()))))
        sig = hash_block(str(parts))
        head_sigs[sig].append(p)

    # ---------- 2. PagefindUI init script ------------------------------------
    pagefind_sigs: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for s in soup.find_all("script"):
            if s.string and "PagefindUI" in s.string:
                sig = hash_block(normalize_block(s.string))
                pagefind_sigs[sig].append(p)
                break  # one per file

    # ---------- 3. Footer blocks --------------------------------------------
    footer_sigs: dict[str, list[Path]] = collections.defaultdict(list)
    footer_texts: dict[str, str] = {}
    for p, soup in soups.items():
        for f in soup.find_all("footer"):
            txt = normalize_block(f.get_text(" "))
            sig = hash_block(txt)
            footer_sigs[sig].append(p)
            footer_texts[sig] = txt[:200]

    # ---------- 4. chapter-nav <nav class="chapter-nav"> --------------------
    # Look at structural template (drop hrefs / labels)
    chapter_nav_struct_sigs: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for n in soup.find_all("nav", class_="chapter-nav"):
            structure = []
            for a in n.find_all("a"):
                spans = [sp.get("class", [None])[0] for sp in a.find_all("span")]
                structure.append((a.get("class", [None])[0], tuple(spans)))
            sig = hash_block(str(structure))
            chapter_nav_struct_sigs[sig].append(p)

    # ---------- 5. header / chapter-header ----------------------------------
    chapter_header_sigs: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        h = soup.find("header", class_="chapter-header")
        if not h:
            continue
        # Structural signature: classes of nav/div/h1 children
        struct = []
        for child in h.find_all(recursive=False):
            classes = tuple(child.get("class", []) or [])
            struct.append((child.name, classes))
        sig = hash_block(str(struct))
        chapter_header_sigs[sig].append(p)

    # ---------- 6. epigraph repetition --------------------------------------
    epigraph_texts: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for bq in soup.find_all("blockquote", class_="epigraph"):
            quote = bq.find("p")
            if not quote:
                continue
            t = normalize_block(quote.get_text(" "))
            if len(t) < 12:
                continue
            epigraph_texts[t].append(p)

    # ---------- 7. callout repetition ---------------------------------------
    callout_text_to_files: dict[tuple[str, str], list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for c in soup.find_all("div", class_="callout"):
            classes = c.get("class", [])
            kind = next((cls for cls in classes if cls != "callout"), "")
            body = normalize_block(c.get_text(" "))
            if len(body) < 40:
                continue
            callout_text_to_files[(kind, body)].append(p)

    # ---------- 8. inline style attributes ----------------------------------
    style_attr_freq: collections.Counter = collections.Counter()
    style_attr_examples: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for el in soup.find_all(style=True):
            sty = normalize_block(el.get("style", ""))
            sty = sty.rstrip(";").strip()
            if not sty:
                continue
            style_attr_freq[sty] += 1
            if len(style_attr_examples[sty]) < 5:
                style_attr_examples[sty].append(p)

    # ---------- 9. bibliography section / whats-next ------------------------
    whats_next_count = 0
    bib_count = 0
    for p, soup in soups.items():
        if soup.find("div", class_="whats-next"):
            whats_next_count += 1
        if soup.find("section", class_="bibliography"):
            bib_count += 1

    # ---------- 10. section-card structures ---------------------------------
    section_card_files: list[Path] = []
    for p, soup in soups.items():
        if soup.find("a", class_="section-card"):
            section_card_files.append(p)

    # ---------- 11. image references / duplicate filenames ------------------
    img_name_to_files: dict[str, set[Path]] = collections.defaultdict(set)
    img_paths_per_file: dict[Path, list[str]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if not src or src.startswith("data:"):
                continue
            fname = os.path.basename(src)
            img_name_to_files[fname].add(p)
            img_paths_per_file[p].append(src)

    # ---------- 12. CSS magic numbers (inline + raw scan of book.css) -------
    inline_css_color_freq: collections.Counter = collections.Counter()
    color_re = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    for el_style, count in style_attr_freq.items():
        for m in color_re.findall(el_style):
            inline_css_color_freq[m.lower()] += count

    # Scan book.css for color counts too (to surface candidates for vars)
    book_css_path = ROOT / "styles" / "book.css"
    book_css_color_freq: collections.Counter = collections.Counter()
    book_css_size_freq: collections.Counter = collections.Counter()
    if book_css_path.exists():
        css = book_css_path.read_text(encoding="utf-8", errors="ignore")
        for m in color_re.findall(css):
            book_css_color_freq[m.lower()] += 1
        for m in re.findall(r"\b\d+px\b", css):
            book_css_size_freq[m] += 1

    # ---------- 13. KaTeX / Prism / Pygments script duplication -------------
    # Count how many files load KaTeX inline + the auto-render onload block
    katex_onload_sigs: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for s in soup.find_all("script"):
            ol = s.get("onload", "") or ""
            if "renderMathInElement" in ol:
                sig = hash_block(normalize_block(ol))
                katex_onload_sigs[sig].append(p)

    # ---------- 14. footer one-liner inside section files -------------------
    short_footer_re = re.compile(r"<footer><p>([^<]+)</p></footer>")
    short_footer_freq: collections.Counter = collections.Counter()
    short_footer_examples: dict[str, list[Path]] = collections.defaultdict(list)
    for p, text in raw.items():
        for m in short_footer_re.findall(text):
            t = normalize_block(m)
            short_footer_freq[t] += 1
            if len(short_footer_examples[t]) < 4:
                short_footer_examples[t].append(p)

    # ---------- 15. edition / copyright lines in raw text -------------------
    edition_re = re.compile(r"(Fourteenth|Fifteenth|Sixteenth|14th|15th|16th)\s+Edition", re.I)
    edition_freq: collections.Counter = collections.Counter()
    edition_examples: dict[str, list[Path]] = collections.defaultdict(list)
    for p, text in raw.items():
        for m in edition_re.findall(text):
            t = m.lower()
            edition_freq[t] += 1
            if len(edition_examples[t]) < 4:
                edition_examples[t].append(p)

    # ---------- 16. prerequisites blocks - same wording? --------------------
    prereq_text_freq: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for d in soup.find_all("div", class_="prerequisites"):
            t = normalize_block(d.get_text(" "))
            if 30 < len(t) < 800:
                prereq_text_freq[t].append(p)

    # ---------- 17. bib-entry-card structure ---------------------------------
    bib_card_count = 0
    bib_card_files: set[Path] = set()
    for p, soup in soups.items():
        cards = soup.find_all("div", class_="bib-entry-card")
        if cards:
            bib_card_count += len(cards)
            bib_card_files.add(p)

    # ---------- 18. data-pagefind-meta injected spans ------------------------
    pagefind_meta_freq: collections.Counter = collections.Counter()
    for p, soup in soups.items():
        for sp in soup.find_all("span", attrs={"data-pagefind-meta": True}):
            pagefind_meta_freq[sp.get("data-pagefind-meta", "")] += 1

    # ---------- 19. agent-avatar-inline ------------------------------------
    agent_avatar_styles: collections.Counter = collections.Counter()
    agent_avatar_examples: dict[str, list[Path]] = collections.defaultdict(list)
    for p, soup in soups.items():
        for sp in soup.find_all("span", class_="agent-avatar-inline"):
            sty = normalize_block(sp.get("style", ""))
            if sty:
                agent_avatar_styles[sty] += 1
                if len(agent_avatar_examples[sty]) < 4:
                    agent_avatar_examples[sty].append(p)

    # ---------- 20. shared part2 CSS - is it duplicated in book.css? --------
    shared_part2_present = (ROOT / "part-2-understanding-llms" / "shared-part2.css").exists()

    # =========================================================================
    # REPORT
    # =========================================================================
    def banner(title: str) -> None:
        print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")

    banner("SUMMARY METRICS")
    print(f"Files scanned:                       {len(files)}")
    print(f"Files with chapter-header skeleton:  {sum(len(v) for v in chapter_header_sigs.values())}")
    print(f"Distinct chapter-header signatures:  {len(chapter_header_sigs)}")
    print(f"Files with PagefindUI init script:   {sum(len(v) for v in pagefind_sigs.values())}")
    print(f"Distinct PagefindUI init signatures: {len(pagefind_sigs)}")
    print(f"Files with chapter-nav block:        {sum(len(v) for v in chapter_nav_struct_sigs.values())}")
    print(f"Files with whats-next block:         {whats_next_count}")
    print(f"Files with bibliography section:     {bib_count}")
    print(f"Files with section-card blocks:      {len(section_card_files)}")
    print(f"Total bib-entry-card blocks:         {bib_card_count} across {len(bib_card_files)} files")
    print(f"Files with KaTeX auto-render onload: {sum(len(v) for v in katex_onload_sigs.values())}")
    print(f"Files with short <footer><p>...</p></footer>: {sum(short_footer_freq.values())}")
    print(f"Distinct inline style='..' values:    {len(style_attr_freq)}")
    print(f"Total inline style='..' occurrences:  {sum(style_attr_freq.values())}")
    print(f"shared-part2.css present:            {shared_part2_present}")

    banner("TOP UNIFICATION OPPORTUNITIES (ordered by impact)")

    # Opportunity 1: <head> blocks
    print("\n[01] HEAD blocks (head includes for CSS/JS) are repeated in every section file.")
    print(f"     Distinct <head> shapes: {len(head_sigs)} across {sum(len(v) for v in head_sigs.values())} files.")
    sorted_heads = sorted(head_sigs.items(), key=lambda x: -len(x[1]))
    for sig, paths in sorted_heads[:3]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        print(f"     - signature {sig}: {len(paths)} files (e.g. {sample})")
    print("     Fix: extract head into _includes/head.html partial OR generate at build via html2epub.")

    # Opportunity 2: PagefindUI init
    print("\n[02] PagefindUI initialization <script> block at bottom of every section file.")
    print(f"     Distinct PagefindUI script signatures: {len(pagefind_sigs)}")
    for sig, paths in sorted(pagefind_sigs.items(), key=lambda x: -len(x[1]))[:3]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        print(f"     - signature {sig}: {len(paths)} files (e.g. {sample})")
    print("     Fix: move the entire window.addEventListener('DOMContentLoaded'... block to scripts/book.js")
    print("          (already loaded everywhere). Remove ~30 lines from every section file.")

    # Opportunity 3: short footer
    print("\n[03] Repeated short footer text (<footer><p>Fifteenth Edition, 2026 ...</p></footer>).")
    for t, n in short_footer_freq.most_common(5):
        sample = ", ".join(short_path(p) for p in short_footer_examples[t][:3])
        print(f"     - x{n}: {t[:80]!r} (e.g. {sample})")
    print("     Fix: replace each occurrence with a single <footer data-include='_includes/footer.html'>")
    print("          OR have html2epub stamp from a Jinja template; remove edition string from every file.")

    # Opportunity 4: edition strings duplicated
    print("\n[04] Edition strings ('Fifteenth Edition' / 'Fourteenth Edition') hard-coded across files.")
    for s, n in edition_freq.most_common():
        sample = ", ".join(short_path(p) for p in edition_examples[s][:3])
        print(f"     - {s!r:30s}: {n} occurrences (e.g. {sample})")
    print("     Fix: replace literal string with a Jinja variable {{ edition }} (or build-time templater),")
    print("          driven by BOOK_CONFIG. Right now 'Fourteenth' and 'Fifteenth' co-exist => stale.")

    # Opportunity 5: KaTeX onload init
    print("\n[05] KaTeX renderMathInElement onload script duplicated in every math-bearing file.")
    print(f"     Distinct onload payloads: {len(katex_onload_sigs)}")
    for sig, paths in sorted(katex_onload_sigs.items(), key=lambda x: -len(x[1]))[:3]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        print(f"     - signature {sig}: {len(paths)} files (e.g. {sample})")
    print("     Fix: move onload payload to a tiny katex-init.js loaded once via the partial head.html.")

    # Opportunity 6: chapter-header skeleton
    print("\n[06] <header class='chapter-header'> repeated near-identically across all sections.")
    print(f"     Distinct structural signatures: {len(chapter_header_sigs)}")
    for sig, paths in sorted(chapter_header_sigs.items(), key=lambda x: -len(x[1]))[:3]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        print(f"     - signature {sig}: {len(paths)} files (e.g. {sample})")
    print("     Fix: extract to _includes/chapter-header.html partial; pass {part, chapter, title}.")
    print("     Sub-issue: some files use plain text 'Building Conversational AI with LLMs and Agents'")
    print("     in <nav class='header-nav'> while others use <a class='book-title-link'>...</a>; unify.")

    # Opportunity 7: chapter-nav structural template
    print("\n[07] <nav class='chapter-nav'> with prev/up/next spans repeated everywhere.")
    print(f"     Distinct structural signatures: {len(chapter_nav_struct_sigs)}")
    for sig, paths in sorted(chapter_nav_struct_sigs.items(), key=lambda x: -len(x[1]))[:3]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        print(f"     - signature {sig}: {len(paths)} files (e.g. {sample})")
    print("     Fix: drive from a build-time nav table (TOC -> linkages); render via shared partial.")

    # Opportunity 8: epigraph repetition
    print("\n[08] Epigraph (blockquote.epigraph) quotes that appear in MULTIPLE files (potential copy/paste).")
    dup_epigraphs = [(t, ps) for t, ps in epigraph_texts.items() if len(ps) > 1]
    dup_epigraphs.sort(key=lambda x: -len(x[1]))
    print(f"     Found {len(dup_epigraphs)} epigraph quotes shared across >1 file.")
    for t, paths in dup_epigraphs[:5]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        snip = t[:90] + ("..." if len(t) > 90 else "")
        print(f"     - x{len(paths)}: {snip!r} (e.g. {sample})")
    print("     Fix: epigraphs should be single-source per section; flag any shared across sections.")

    # Opportunity 9: identical callout bodies
    print("\n[09] Callouts with IDENTICAL body text appearing in multiple files.")
    dup_callouts = [(k, ps) for k, ps in callout_text_to_files.items() if len(ps) > 1]
    dup_callouts.sort(key=lambda x: -len(x[1]))
    print(f"     Found {len(dup_callouts)} (kind, body) callout duplicates.")
    for (kind, body), paths in dup_callouts[:5]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        snip = body[:90] + ("..." if len(body) > 90 else "")
        print(f"     - x{len(paths)} [{kind}]: {snip!r} (e.g. {sample})")
    print("     Fix: extract repeated callouts to a shared partial (e.g. _includes/callout/big-picture-ml.html).")

    # Opportunity 10: inline style="..." attributes -> CSS classes
    print("\n[10] Inline style='...' attributes that recur many times (should become a CSS class).")
    top_styles = style_attr_freq.most_common(10)
    for sty, n in top_styles:
        snip = sty[:80] + ("..." if len(sty) > 80 else "")
        sample = ", ".join(short_path(p) for p in style_attr_examples[sty][:3])
        print(f"     - x{n}: style={snip!r} (e.g. {sample})")
    print("     Fix: define semantic classes in styles/book.css; drop the style= attributes.")

    # Opportunity 11: agent-avatar inline styles (background-color per agent)
    print("\n[11] <span class='agent-avatar-inline' style='background-color: #...'> repeated per agent.")
    print(f"     Distinct inline avatar styles: {len(agent_avatar_styles)}")
    for sty, n in agent_avatar_styles.most_common(8):
        sample = ", ".join(short_path(p) for p in agent_avatar_examples[sty][:3])
        print(f"     - x{n}: {sty!r} (e.g. {sample})")
    print("     Fix: add per-agent classes (.avatar-tensor, .avatar-eval, ...) with the background-color")
    print("          rule in book.css. Already a partial 'agent registry' would unify name/color/avatar.")

    # Opportunity 12: prerequisite text duplicated
    print("\n[12] <div class='prerequisites'> blocks with identical wording across files.")
    dup_prereqs = [(t, ps) for t, ps in prereq_text_freq.items() if len(ps) > 1]
    dup_prereqs.sort(key=lambda x: -len(x[1]))
    print(f"     Found {len(dup_prereqs)} prereq blocks duplicated verbatim.")
    for t, paths in dup_prereqs[:5]:
        sample = ", ".join(short_path(p) for p in paths[:3])
        snip = t[:90] + ("..." if len(t) > 90 else "")
        print(f"     - x{len(paths)}: {snip!r} (e.g. {sample})")
    print("     Fix: keep prereqs unique per section; if a block is generic, move to chapter index instead.")

    # Opportunity 13: bibliography card structure
    print(f"\n[13] <div class='bib-entry-card'> structure repeated {bib_card_count} times across {len(bib_card_files)} files.")
    print("     Each card has: <p class='bib-ref'>...</p>, <p class='bib-annotation'>...</p>, <span class='bib-meta'>...</span>.")
    print("     Fix: drive bibliography from a structured data file (refs.json / .bib) and render via a")
    print("          single template at build time. Easier to maintain consistency in citation format.")

    # Opportunity 14: short_path duplicate images
    multi_img = [(name, fps) for name, fps in img_name_to_files.items() if len(fps) >= 5]
    multi_img.sort(key=lambda x: -len(x[1]))
    print(f"\n[14] Image filenames referenced from >=5 files (possible copy of the same asset).")
    for name, fps in multi_img[:10]:
        # Also count the distinct paths used to reach it
        distinct_paths: set[str] = set()
        for p in fps:
            for src in img_paths_per_file.get(p, []):
                if os.path.basename(src) == name:
                    distinct_paths.add(src)
        print(f"     - {name}: referenced from {len(fps)} files via {len(distinct_paths)} distinct relative paths")
    print("     Fix: if same logical image, host once at /images/<name>.png and reference via root-relative.")
    print("          The build (html2epub) can rewrite to relative paths for EPUB.")

    # Opportunity 15: CSS magic colors in book.css that should be vars
    print("\n[15] Hex colors in styles/book.css used many times (should be CSS variables).")
    for color, n in book_css_color_freq.most_common(10):
        print(f"     - {color}: {n} uses in book.css")
    print("     Fix: define :root { --accent: #...; --callout-border: #...; ... } and replace hex literals.")
    print("     Top 'magic' pixel sizes in book.css (candidates for vars / spacing scale):")
    for sz, n in book_css_size_freq.most_common(8):
        print(f"     - {sz}: {n} uses")

    # Opportunity 16: section-card structure
    print(f"\n[16] <a class='section-card'> structure: {len(section_card_files)} chapter-index files repeat the same")
    print("     skeleton (section-num + section-title + 1-2 badges + section-desc).")
    print("     Fix: drive from TOC data; render via single 'section-card.html' partial.")

    # Opportunity 17: shared-part2.css side-effect
    print("\n[17] Only Part 2 has its own 'shared-part2.css' (348 lines).")
    print(f"     File: {short_path(ROOT / 'part-2-understanding-llms' / 'shared-part2.css')}")
    print("     Fix: audit it; if rules are genuinely book-wide, move into styles/book.css.")
    print("          If part-specific, rename to per-part CSS files for ALL parts (consistency), or fold in.")

    # Opportunity 18: whats-next block + bibliography section consistency
    print(f"\n[18] <div class='whats-next'> appears in {whats_next_count} files and <section class='bibliography'> in {bib_count}.")
    print("     Fix: extract whats-next to a shared partial that takes next_section_title / href as inputs;")
    print("          link the bibliography header text to a constant.")

    # Opportunity 19: pagefind meta span injection
    print(f"\n[19] data-pagefind-meta injected span tags repeat per file.")
    for meta, n in pagefind_meta_freq.most_common(6):
        print(f"     - meta={meta!r}: {n} occurrences")
    print("     Fix: emit these from the build template at the same time the breadcrumb is rendered;")
    print("          today they are hand-rolled per file and easy to forget on new pages.")

    # Opportunity 20: edition / fact drift hint
    print("\n[20] Single-source-of-truth: edition mismatch is one example (Opportunity 4).")
    print("     Recommend automated checks for other facts (model parameter counts, dates).")
    print("     Quick run: grep'ed strings that match patterns like '1.76T params' vs '1.8T parameters'")
    print("     would surface SoT violations; add a follow-up audit script (out of scope here).")

    banner("END OF REPORT")


if __name__ == "__main__":
    main()
