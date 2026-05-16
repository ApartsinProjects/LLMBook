"""Read-only audit of three navigation-document problems flagged by the author.

1) appendices/index.html vs actual appendix directories on disk
2) toc.html (long-form, #toc-detailed) vs actual section files on disk
3) Glossary placement (appendices/index.html lists it; toc.html lists it
   under appendices; glossary's internal nav treats it as an appendix)

Writes nothing. Prints findings to stdout for parent agent to relay.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from collections import OrderedDict

from bs4 import BeautifulSoup

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
APPENDICES_DIR = ROOT / "appendices"
APPENDICES_INDEX = APPENDICES_DIR / "index.html"
TOC = ROOT / "toc.html"
GLOSSARY_DIR = APPENDICES_DIR / "glossary"

EXCLUDE = {"KDP", ".claude", "node_modules", "build"}


def line_of(html: str, needle: str) -> int:
    """Return 1-indexed line where needle first appears, or 0."""
    idx = html.find(needle)
    if idx < 0:
        return 0
    return html.count("\n", 0, idx) + 1


# -----------------------------------------------------------------------------
# 1) Appendices index.html vs actual directory layout
# -----------------------------------------------------------------------------
def audit_appendices_index():
    print("=" * 78)
    print("PART 1: appendices/index.html vs actual appendices/ directory layout")
    print("=" * 78)

    # On disk
    disk_dirs = sorted(
        d.name for d in APPENDICES_DIR.iterdir()
        if d.is_dir() and d.name not in EXCLUDE
    )
    print(f"\nDisk: {len(disk_dirs)} appendix directories under appendices/")
    for d in disk_dirs:
        print(f"  {d}")

    # Parse appendices/index.html
    html = APPENDICES_INDEX.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Each appendix appears as <div class="chapter-card"> with a header span
    # "<span class="mod-num">Appendix X</span> Title" and an <a> link.
    cards = soup.find_all("div", class_="chapter-card")
    print(f"\nappendices/index.html: {len(cards)} chapter-card entries")

    listed = []  # (letter_label, title, link, line)
    for card in cards:
        hdr = card.find("div", class_="chapter-card-header")
        if not hdr:
            continue
        mod = hdr.find("span", class_="mod-num")
        if not mod:
            continue
        label = mod.get_text(strip=True)
        # title = remainder of header after the span
        hdr_text = hdr.get_text(" ", strip=True)
        # strip the mod-num label off the front
        title = hdr_text[len(label):].strip() if hdr_text.startswith(label) else hdr_text
        # Use the "Read Appendix ..." link (the navigation link), not inline
        # glossary cross-references. It is the LAST <a> inside the card and
        # its text starts with "Read".
        href = ""
        a_read = None
        for a in card.find_all("a"):
            if a.get_text(strip=True).startswith("Read "):
                a_read = a
                href = a.get("href", "")
                break
        if href == "" and a_read is None:
            # fallback: last anchor
            anchors = card.find_all("a")
            if anchors:
                href = anchors[-1].get("href", "")
        # line of the header span in source
        snippet = f'<span class="mod-num">{label}</span>'
        ln = line_of(html, snippet)
        listed.append((label, title, href, ln))

    print("\nListed entries (label, title, href, line):")
    for label, title, href, ln in listed:
        print(f"  L{ln:>3}  {label!r:<22}  {title!r:<60}  href={href!r}")

    # Compare to disk
    print("\n--- Mismatches ---")
    found = 0

    # Map of letter -> disk directory based on slug pattern appendix-<letter>-...
    disk_letter_to_dir = {}
    for d in disk_dirs:
        m = re.match(r"appendix-([a-z])-", d)
        if m:
            disk_letter_to_dir[m.group(1)] = d
    # Glossary is special-cased (no appendix-<letter>-... pattern)
    has_glossary = "glossary" in disk_dirs

    # Listed letters: parse from label "Appendix X" / "Appendix AD" / "Appendix AI" / etc.
    # Also collect each link letter (derived from href like appendix-X-... or glossary/)
    listed_link_letters = []
    for label, title, href, ln in listed:
        m_lbl = re.match(r"Appendix\s+([A-Z]+)$", label)
        lbl_letter = m_lbl.group(1) if m_lbl else None

        m_href = re.match(r"appendix-([a-z])-", href)
        if m_href:
            href_letter = m_href.group(1).upper()
        elif href.startswith("glossary/"):
            href_letter = "GLOSSARY"
        else:
            href_letter = None

        listed_link_letters.append((label, title, href, ln, lbl_letter, href_letter))

        # Mismatch: label letter does not match the href dir letter
        if lbl_letter and href_letter and href_letter != "GLOSSARY":
            if lbl_letter != href_letter:
                print(f"  WRONG-LETTER: line {ln}  label says {label!r} but href points to appendix-{href_letter.lower()}-... ({href!r}); title={title!r}")
                found += 1

        # Mismatch: target dir does not exist
        if href and "/" in href:
            target_dir = href.split("/")[0]
            if not (APPENDICES_DIR / target_dir).exists():
                print(f"  BROKEN-LINK: line {ln}  href={href!r} dir {target_dir!r} does not exist")
                found += 1

    # Missing entries: on-disk dirs that are not represented by any href in the listing
    href_target_dirs = set()
    for _, _, href, _ in listed:
        if href and "/" in href:
            href_target_dirs.add(href.split("/")[0])
    for d in disk_dirs:
        if d not in href_target_dirs:
            print(f"  MISSING-FROM-INDEX: directory {d!r} on disk has no card in appendices/index.html")
            found += 1

    # Extra entries: hrefs in listing that point to non-existent dirs (already
    # caught as BROKEN-LINK above)

    # Letter-coverage gap: directories on disk use letters a..u (21 dirs + glossary).
    # Listing uses A..V + AD..AI (and may skip M..Q letters). Print the
    # mapping for context so author can confirm.
    print("\n--- Letter mapping audit (label vs href dir) ---")
    for label, title, href, ln, lbl_letter, href_letter in listed_link_letters:
        if lbl_letter and href_letter:
            tag = "OK   " if (lbl_letter == href_letter or href_letter == "GLOSSARY") else "DRIFT"
            print(f"  {tag}  line {ln:>3}  label={label!r:<18}  href_letter={href_letter}  ({title!r})")

    print(f"\nTotal mismatches in PART 1: {found}")
    return found


# -----------------------------------------------------------------------------
# 2) toc.html long-form vs actual section files on disk
# -----------------------------------------------------------------------------
def collect_section_files() -> dict:
    """Return {dir_relative_to_root: sorted list of section-*.html filenames}."""
    result = {}
    for part_dir in sorted(ROOT.iterdir()):
        if not part_dir.is_dir():
            continue
        if part_dir.name in EXCLUDE:
            continue
        if part_dir.name == "appendices":
            for sub in sorted(part_dir.iterdir()):
                if sub.is_dir():
                    sections = sorted(
                        f.name for f in sub.iterdir()
                        if f.is_file() and re.match(r"section-.+\.html$", f.name)
                    )
                    if sections:
                        result[f"appendices/{sub.name}"] = sections
        elif part_dir.name.startswith("part-"):
            for module in sorted(part_dir.iterdir()):
                if module.is_dir() and module.name.startswith("module-"):
                    sections = sorted(
                        f.name for f in module.iterdir()
                        if f.is_file() and re.match(r"section-\d+\.\d+\.html$", f.name)
                    )
                    if sections:
                        result[f"{part_dir.name}/{module.name}"] = sections
    return result


def audit_toc_detailed():
    print("\n" + "=" * 78)
    print("PART 2: toc.html #toc-detailed vs actual section files on disk")
    print("=" * 78)

    html = TOC.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    detailed = soup.find("div", id="toc-detailed")
    if detailed is None:
        print("  ERROR: <div id='toc-detailed'> not found in toc.html")
        return 1

    # Parse: walk each <div class="dense-sections"> which sits under the
    # preceding <div class="dense-chapter"> link.
    # We will compare each (chapter dir, list of section hrefs + titles) pair
    # against disk.
    found = 0

    # All <a> tags in dense-sections, paired with their preceding chapter link
    nodes = list(detailed.children)
    pairs = []  # list of (chapter_href, chapter_title, [(section_href, section_title)], dense_chapter_line)
    current_chapter_href = None
    current_chapter_title = None
    current_chapter_line = 0
    for child in nodes:
        if getattr(child, "name", None) != "div":
            continue
        classes = child.get("class") or []
        if "dense-chapter" in classes:
            a = child.find("a")
            if a:
                current_chapter_href = a.get("href", "")
                current_chapter_title = a.get_text(strip=True)
                snippet_marker = f'href="{current_chapter_href}"'
                current_chapter_line = line_of(html, snippet_marker)
        elif "dense-sections" in classes:
            secs = []
            for a in child.find_all("a"):
                secs.append((a.get("href", ""), a.get_text(strip=True)))
            pairs.append((current_chapter_href, current_chapter_title, secs, current_chapter_line))

    print(f"Parsed {len(pairs)} chapter -> sections pairs from #toc-detailed.")

    # Map disk section files for quick membership tests
    disk_sections = collect_section_files()

    # For each chapter pair, the section hrefs should resolve relative to ROOT.
    toc_section_pages = set()
    for chap_href, chap_title, secs, chap_line in pairs:
        # Derive chapter directory from chap_href (e.g. "part-1-foundations/module-00-.../index.html")
        chap_dir = "/".join(chap_href.split("/")[:-1]) if "/" in chap_href else ""
        # Validate chapter link
        chap_target = ROOT / chap_href.replace("/", "\\")
        if not chap_target.exists():
            print(f"  BROKEN-CHAPTER-LINK: line {chap_line}  href={chap_href!r}  target does not exist on disk")
            found += 1

        for sec_href, sec_title in secs:
            sec_line = line_of(html, f'href="{sec_href}"')
            toc_section_pages.add(sec_href)
            sec_target = ROOT / sec_href.replace("/", "\\")
            if not sec_target.exists():
                print(f"  BROKEN-SECTION-LINK: line {sec_line}  href={sec_href!r}  title={sec_title!r}  (chapter: {chap_title!r})")
                found += 1
                continue

            # Compare TOC section title vs actual <h1>/<title> of section
            try:
                sec_html = sec_target.read_text(encoding="utf-8", errors="replace")
                sec_soup = BeautifulSoup(sec_html, "html.parser")
                actual_h1 = sec_soup.find("h1")
                actual_h1_text = actual_h1.get_text(" ", strip=True) if actual_h1 else ""

                # Extract prefix from TOC title and H1.
                # Two shapes: numeric "6.5 Foo" OR alpha "G.1 Foo".
                def extract_prefix(text):
                    text = text.strip()
                    text = re.sub(r"^Section\s+", "", text)
                    m = re.match(r"^([A-Za-z])\.(\d+)\b", text)
                    if m:
                        return f"{m.group(1).upper()}.{m.group(2)}"
                    m = re.match(r"^(\d+)\.(\d+)\b", text)
                    if m:
                        return f"{m.group(1)}.{m.group(2)}"
                    return None

                toc_prefix = extract_prefix(sec_title)
                h1_prefix = extract_prefix(actual_h1_text)

                # Normalize bodies (strip prefix and "Glossary N" preludes)
                toc_title_clean = re.sub(r"^[A-Za-z]?\d*\.\d+\s+", "", sec_title).strip()
                h1_clean = re.sub(r"^(Section\s+)?[A-Za-z]?\d*\.\d+\s*[:\-]?\s*", "", actual_h1_text).strip()
                h1_clean = re.sub(r"^Glossary\s+\d+\s*[:\-]?\s*", "", h1_clean).strip()

                def norm(s):
                    return re.sub(r"[^a-z0-9]", "", s.lower())

                body_drift = (toc_title_clean and h1_clean and norm(toc_title_clean) != norm(h1_clean))
                prefix_drift = bool(toc_prefix and h1_prefix and toc_prefix != h1_prefix)

                if body_drift or prefix_drift:
                    print(f"  TITLE-DRIFT: line {sec_line}  href={sec_href}")
                    print(f"      toc says : {sec_title!r}")
                    print(f"      h1 says  : {actual_h1_text!r}")
                    if prefix_drift and not body_drift:
                        print(f"      (prefix-only drift: TOC={toc_prefix!r} vs H1={h1_prefix!r})")
                    found += 1
            except Exception as e:
                print(f"  READ-ERROR: {sec_href} ({e})")

    # Missing sections: section files on disk that don't appear in toc-detailed
    for dir_rel, fnames in disk_sections.items():
        for fname in fnames:
            sec_path = f"{dir_rel}/{fname}"
            if sec_path not in toc_section_pages:
                print(f"  MISSING-FROM-TOC: section file exists on disk but not in toc-detailed -> {sec_path}")
                found += 1

    # Also: order. Within each chapter the TOC sections should be in the
    # numeric order of the file names (section-X.1, X.2, X.3, ...).
    for chap_href, chap_title, secs, chap_line in pairs:
        ordered_hrefs = [s[0] for s in secs]
        # extract trailing "section-<key>.html" sortable key
        def key(href):
            m = re.search(r"section-([^/]+)\.html$", href)
            if not m:
                return (999, 0)
            tok = m.group(1)  # e.g. "1.2", "a.3", "f.5"
            parts = tok.split(".")
            if len(parts) == 2:
                a, b = parts
                # letter prefix sort separately
                if a.isalpha():
                    return (ord(a.lower()), int(b) if b.isdigit() else 0)
                else:
                    try:
                        return (int(a), int(b))
                    except ValueError:
                        return (999, 0)
            return (999, 0)

        sorted_hrefs = sorted(ordered_hrefs, key=key)
        if ordered_hrefs != sorted_hrefs:
            print(f"  ORDER-DRIFT: line {chap_line}  chapter {chap_title!r}")
            print(f"      toc order   : {ordered_hrefs}")
            print(f"      sorted order: {sorted_hrefs}")
            found += 1

    print(f"\nTotal issues in PART 2: {found}")
    return found


# -----------------------------------------------------------------------------
# 3) Glossary placement
# -----------------------------------------------------------------------------
def audit_glossary_placement():
    print("\n" + "=" * 78)
    print("PART 3: Glossary placement")
    print("=" * 78)
    found = 0

    # 3a) appendices/index.html should list glossary
    app_html = APPENDICES_INDEX.read_text(encoding="utf-8")
    app_soup = BeautifulSoup(app_html, "html.parser")
    glossary_card = False
    for card in app_soup.find_all("div", class_="chapter-card"):
        # The "Read X" link is the nav link we care about
        nav_a = None
        for a in card.find_all("a"):
            if a.get_text(strip=True).startswith("Read "):
                nav_a = a
                break
        if nav_a and nav_a.get("href", "").startswith("glossary/"):
            glossary_card = True
            mod = card.find("span", class_="mod-num")
            label = mod.get_text(strip=True) if mod else "(no label)"
            ln = line_of(app_html, 'href="glossary/index.html"')
            print(f"  3a OK: appendices/index.html lists glossary at line {ln} with label {label!r}")
            break
    if not glossary_card:
        print("  3a FAIL: appendices/index.html does NOT list glossary as a chapter-card")
        found += 1

    # 3b) toc.html: glossary should appear under appendices (in the appendices
    # block, not as a top-level entry)
    toc_html = TOC.read_text(encoding="utf-8")
    toc_soup = BeautifulSoup(toc_html, "html.parser")

    # Short toc
    short = toc_soup.find("div", id="toc-short")
    detailed = toc_soup.find("div", id="toc-detailed")

    for view_name, view_root in [("toc-short", short), ("toc-detailed", detailed)]:
        if view_root is None:
            continue
        # find any link with href containing "glossary/"
        glossary_links = [a for a in view_root.find_all("a") if "glossary/" in a.get("href", "")]
        # find the appendices part-header div, then the appendices block
        all_part_headers = view_root.find_all("div", class_="dense-part-header")
        appendices_header = None
        for ph in all_part_headers:
            a = ph.find("a")
            if a and "appendices/" in a.get("href", ""):
                appendices_header = ph
                break
        if not appendices_header:
            print(f"  3b WARN: {view_name} has no appendices part-header (cannot verify placement)")
            continue

        # All <a> in glossary should be after the appendices header
        # and before any other part-header that follows.
        # Find the start index of the appendices header in source.
        app_start_str = str(appendices_header)
        app_start_pos = toc_html.find(app_start_str)
        # find the next part-header after appendices header
        for gl in glossary_links:
            gl_href = gl.get("href", "")
            gl_str_pos = toc_html.find(f'href="{gl_href}"', app_start_pos)
            ln = line_of(toc_html, f'href="{gl_href}"')
            # find next part-header after appendices_header_pos
            next_ph_pos = -1
            for ph in all_part_headers:
                if ph is appendices_header:
                    continue
                ph_pos = toc_html.find(str(ph), app_start_pos + 1)
                if ph_pos > app_start_pos:
                    if next_ph_pos == -1 or ph_pos < next_ph_pos:
                        next_ph_pos = ph_pos
            in_block = (gl_str_pos > app_start_pos)
            if next_ph_pos != -1:
                in_block = in_block and (gl_str_pos < next_ph_pos)

            if in_block:
                print(f"  3b OK: {view_name} glossary link {gl_href!r} at line {ln} is inside appendices block")
            else:
                print(f"  3b FAIL: {view_name} glossary link {gl_href!r} at line {ln} is NOT inside appendices block")
                found += 1

    # 3c) Glossary's own internal nav treats it as an appendix.
    # Check appendices/glossary/index.html: header should have 'Appendices' as parent breadcrumb (toc link) and chapter-nav .up should point to appendices/index.html.
    gloss_index = GLOSSARY_DIR / "index.html"
    gloss_html = gloss_index.read_text(encoding="utf-8")
    gloss_soup = BeautifulSoup(gloss_html, "html.parser")

    # 3c-i: chapter-nav .up
    nav = gloss_soup.find("nav", class_="chapter-nav")
    up = nav.find("a", class_="up") if nav else None
    if up:
        up_href = up.get("href", "")
        up_text = up.get_text(strip=True)
        ln = line_of(gloss_html, '<a class="up"')
        if up_href == "../index.html" and "Appendices" in up_text:
            print(f"  3c-i OK : glossary/index.html chapter-nav .up at line {ln} -> {up_href!r} {up_text!r}")
        else:
            print(f"  3c-i FAIL: glossary/index.html chapter-nav .up at line {ln} -> {up_href!r} text {up_text!r}; should point to ../index.html (Appendices)")
            found += 1
    else:
        print("  3c-i FAIL: glossary/index.html has no chapter-nav .up link")
        found += 1

    # 3c-ii: chapter-nav .prev should chain from the previous appendix
    # (appendix-e last section). Make sure the previous link uses a path that
    # exists (and points to an appendix).
    if nav:
        prev = nav.find("a", class_="prev")
        if prev:
            prev_href = prev.get("href", "")
            ln = line_of(gloss_html, '<a class="prev"')
            target = (gloss_index.parent / prev_href).resolve()
            if not target.exists():
                print(f"  3c-ii FAIL: glossary/index.html .prev at line {ln} href={prev_href!r} -> file does not exist")
                found += 1
            else:
                # Check that it points to something inside ../appendix-* (i.e. an appendix dir)
                rel_target = target.relative_to(ROOT).as_posix() if ROOT in target.parents or target == ROOT else str(target)
                if "/appendix-" in rel_target or rel_target.startswith("appendices/appendix-"):
                    print(f"  3c-ii OK : glossary/index.html .prev at line {ln} -> {prev_href!r} (resolves to {rel_target})")
                else:
                    print(f"  3c-ii WARN: glossary/index.html .prev at line {ln} -> {prev_href!r} resolves to {rel_target}; expected an appendix dir")

    # 3c-iii: part-label / chapter-label  -- author asks "internal navigation
    # treats it as an appendix". The glossary/index.html part-label is
    # "Building Conversational AI..." (book title), not "Appendices". Flag
    # that drift.
    part_label = gloss_soup.find("div", class_="part-label")
    if part_label:
        pl_text = part_label.get_text(" ", strip=True)
        ln = line_of(gloss_html, '<div class="part-label"')
        if "Appendices" in pl_text or "Appendix" in pl_text:
            print(f"  3c-iii OK : glossary/index.html part-label at line {ln} = {pl_text!r}")
        else:
            print(f"  3c-iii FAIL: glossary/index.html part-label at line {ln} = {pl_text!r}; should reflect appendix context (e.g. 'Appendices' or 'Appendix F')")
            found += 1

    # 3c-iv: section files inside glossary use section-f.N pattern -- check
    # that their internal navigation also treats them as appendix sections.
    for sec_file in sorted(GLOSSARY_DIR.glob("section-f.*.html")):
        sec_html = sec_file.read_text(encoding="utf-8")
        sec_soup = BeautifulSoup(sec_html, "html.parser")
        chap_label = sec_soup.find("div", class_="chapter-label")
        if chap_label:
            a = chap_label.find("a")
            txt = chap_label.get_text(" ", strip=True)
            href = a.get("href", "") if a else ""
            ln = line_of(sec_html, '<div class="chapter-label"')
            # The chapter-label should link to ../index.html (glossary index)
            # or be labeled "Glossary"/"Appendix F"
            problems = []
            if href and href != "index.html":
                problems.append(f"chapter-label href={href!r} (expected 'index.html')")
            if "Glossary" not in txt and "Appendix" not in txt:
                problems.append(f"chapter-label text={txt!r} should contain 'Glossary' or 'Appendix F'")
            if problems:
                print(f"  3c-iv FAIL: {sec_file.relative_to(ROOT).as_posix()} line {ln}: {'; '.join(problems)}")
                found += 1

    # 3c-v: Compare glossary's section-f.* file naming against label "Appendix F"
    # in appendices/index.html. The appendices/index.html lists Glossary at the
    # "Appendix F" slot (line ~93). On disk, the directory is named "glossary"
    # (not "appendix-f-glossary"). Flag this as an additional inconsistency.
    expected_dir = "appendix-f-glossary"
    if not (APPENDICES_DIR / expected_dir).exists():
        # And the section files inside use a 'section-f.N' pattern, which only
        # makes sense if it IS Appendix F. So the section naming agrees with
        # "Appendix F". This is informational, not a bug, but worth noting.
        print(f"  3c-v NOTE: glossary directory is named 'glossary/' on disk (not 'appendix-f-glossary/'). Section files use 'section-f.N' pattern, consistent with Appendix F. This is OK as long as appendices/index.html and toc.html both link to glossary/ explicitly.")

    print(f"\nTotal issues in PART 3: {found}")
    return found


def main():
    p1 = audit_appendices_index()
    p2 = audit_toc_detailed()
    p3 = audit_glossary_placement()
    print("\n" + "=" * 78)
    print(f"GRAND TOTAL: {p1 + p2 + p3} issues  ({p1} P1, {p2} P2, {p3} P3)")
    print("=" * 78)


if __name__ == "__main__":
    main()
