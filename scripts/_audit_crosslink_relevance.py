"""Read-only audit of cross-link RELEVANCE in LLMBook HTML pages.

Differs from html_integrity_audit.py: that one catches 404/broken hrefs.
This one catches link-text-vs-destination MISMATCH:

  - Text: "Chapter 27 LLM Applications", href: ../module-42-strategy-prioritization/...
    -> P0 mismatched topic.
  - Text: "Section 25.4 on agent safety", href: ../module-38-agent-safety-security/section-38.4.html
    -> P1 number drift (target is about agent safety, but the cited section
       number is stale).
  - Text: "Master Reference Tables" / "Freshness Index" / dropped resources.
    -> P2 stale label.
  - Text: "GitHub Actions recipe", destination talks only about MLflow Projects.
    -> P3 over-promise (not a primary focus of this audit, but flag obvious cases).

Skip: self-links, anchor-only links, external links, and structural nav
(header-nav, chapter-nav). Those have their own audits.

Output: cross-link-integrity-audit.md at project root.

Read-only. Cap output around 700 lines, group by pattern.
"""
from __future__ import annotations

import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, unquote

from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
OUT_PATH = ROOT / "cross-link-integrity-audit.md"

EXCLUDE_DIR_NAMES = {
    "KDP", ".claude", "node_modules", "build",
    "pagefind", "templates", "vendor", "scripts", "agents",
    "downloads", "images", "_concept-figs", "__pycache__",
    "styles", ".git", ".github", ".html2pub_cache",
    ".book-update",
}
EXCLUDE_PREFIXES = ("temp_", "source_fix_backups")


def is_excluded_dir(name: str) -> bool:
    if name in EXCLUDE_DIR_NAMES:
        return True
    if any(name.startswith(p) for p in EXCLUDE_PREFIXES):
        return True
    if "backup" in name.lower():
        return True
    return False


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(Path(dirpath) / fn)
    return sorted(out)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


# -------------------------------------------------------------
# Patterns
# -------------------------------------------------------------

# Match "Chapter N" inside link text
PAT_CHAPTER = re.compile(r"\bChapter\s+(\d{1,2})\b", re.IGNORECASE)
# Match "Section N.M(.K)"
PAT_SECTION = re.compile(r"\bSection\s+(\d+(?:\.[\dA-Za-z]+){1,3})\b", re.IGNORECASE)
# Match "Appendix X" letter
PAT_APPENDIX = re.compile(r"\bAppendix\s+([A-Z])(?:[\.:\s]|$)")
# Match "Appendix X.Y"
PAT_APPENDIX_SEC = re.compile(r"\bAppendix\s+([A-Z]\.[\dA-Za-z]+)\b")
# Match "Part N" Roman
PAT_PART = re.compile(r"\bPart\s+(I{1,3}|IV|V|VI{0,3}|IX|XI{0,3}|XII)\b")

# Patterns within link text that signal a dropped resource
DROPPED_RESOURCES = [
    re.compile(r"\bMaster\s+Reference\s+Tables\b", re.IGNORECASE),
    re.compile(r"\b2026\s+Freshness\s+Index\b", re.IGNORECASE),
    re.compile(r"\bFreshness\s+Index\b", re.IGNORECASE),
    re.compile(r"\bAppendix\s+(AD|AE|AI)\b"),
]

# Stop words for noun-phrase matching
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "for", "to", "with",
    "from", "this", "that", "these", "those", "see", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "do", "does",
    "did", "by", "as", "at", "into", "out", "up", "down", "over", "after",
    "before", "between", "through", "during", "via", "vs", "but", "if",
    "when", "where", "why", "how", "what", "which", "who", "whom",
    "chapter", "section", "appendix", "part", "module", "lab",
    "table", "figure", "code", "fragment", "algorithm", "pseudocode",
    "you", "your", "we", "our", "they", "their",
    "more", "most", "less", "many", "few", "all", "each", "every",
    "no", "not", "yes", "can", "will", "may", "might", "must", "should",
    "would", "could", "shall", "llm", "llms", "ai", "model", "models",
    "system", "systems", "page", "pages",
    "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi",
    "xii",
    "on", "covers", "covering", "about", "for", "discusses", "discussed",
    "discussing",
    "&amp;", "&", "&#x2014;", "amp",
}


# -------------------------------------------------------------
# Build directory inventory (chapter num -> dir, appendix letter -> dir,
# section file -> {filename: chapter_num})
# -------------------------------------------------------------

CHAPTER_TO_DIR: dict[int, Path] = {}
PART_NUM_TO_ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V",
    6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
    11: "XI", 12: "XII",
}
ROMAN_TO_PART_NUM = {v: k for k, v in PART_NUM_TO_ROMAN.items()}
APPENDIX_LETTER_TO_DIR: dict[str, Path] = {}


def build_inventory() -> None:
    for part_dir in ROOT.glob("part-*"):
        if not part_dir.is_dir():
            continue
        for mod_dir in part_dir.glob("module-*"):
            if not mod_dir.is_dir():
                continue
            m = re.match(r"module-(\d+)-", mod_dir.name)
            if not m:
                continue
            ch = int(m.group(1))
            has_index = (mod_dir / "index.html").exists()
            has_sections = any(mod_dir.glob("section-*.html"))
            prev = CHAPTER_TO_DIR.get(ch)
            if prev is None:
                CHAPTER_TO_DIR[ch] = mod_dir
            else:
                prev_has_index = (prev / "index.html").exists()
                prev_has_sections = any(prev.glob("section-*.html"))
                if (has_index or has_sections) and not (prev_has_index or prev_has_sections):
                    CHAPTER_TO_DIR[ch] = mod_dir

    apx_root = ROOT / "appendices"
    if apx_root.is_dir():
        for apx_dir in apx_root.glob("appendix-*"):
            if not apx_dir.is_dir():
                continue
            m = re.match(r"appendix-([a-z]+)-", apx_dir.name, re.IGNORECASE)
            if not m:
                continue
            letter = m.group(1).upper()
            APPENDIX_LETTER_TO_DIR[letter] = apx_dir


# Cache: resolved page identity (h1_text, chapter_num, appendix_letter, section_label, part_num)
DEST_IDENTITY_CACHE: dict[Path, dict] = {}


def destination_identity(target: Path) -> dict:
    """Return {h1, chapter_num, appendix_letter, section_label, part_num, title_words}.
    chapter_num / section_label derived from the file path & filename, not from
    title text (because titles can lie too)."""
    if target in DEST_IDENTITY_CACHE:
        return DEST_IDENTITY_CACHE[target]
    out = {
        "h1": "",
        "chapter_num": None,
        "appendix_letter": None,
        "section_label": None,
        "part_num": None,
        "is_appendix": False,
        "title_words": set(),
        "topic_words": set(),  # h1 + h2s + first paragraph
    }
    # Path-based
    parts = target.parts
    for p in parts:
        m = re.match(r"part-(\d+)-", p)
        if m:
            out["part_num"] = int(m.group(1))
        m = re.match(r"module-(\d+)-", p)
        if m:
            out["chapter_num"] = int(m.group(1))
        m = re.match(r"appendix-([a-z]+)-", p, re.IGNORECASE)
        if m:
            out["appendix_letter"] = m.group(1).upper()
            out["is_appendix"] = True
    # Filename
    fn = target.name
    m = re.match(r"section-([\d]+(?:\.[\dA-Za-z]+)+)\.html$", fn)
    if m:
        out["section_label"] = m.group(1)
    m = re.match(r"section-([a-z]+\.[\dA-Za-z]+)\.html$", fn, re.IGNORECASE)
    if m and out["is_appendix"]:
        out["section_label"] = m.group(1).upper()

    try:
        html = target.read_text(encoding="utf-8", errors="replace")
    except OSError:
        DEST_IDENTITY_CACHE[target] = out
        return out
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if h1:
        out["h1"] = h1.get_text(" ", strip=True)
        out["title_words"] = noun_words(out["h1"])
    # Wider topic context: h1, h2, h3, meta description, first 2 paragraphs.
    topic_parts: list[str] = []
    if h1:
        topic_parts.append(h1.get_text(" ", strip=True))
    for h in soup.find_all(["h2", "h3"]):
        topic_parts.append(h.get_text(" ", strip=True))
    # Meta description
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        topic_parts.append(meta.get("content"))
    # Breadcrumb / pagefind chapter (e.g., "Chapter 27: Tool Use")
    bc = soup.find("div", class_="page-breadcrumb")
    if bc:
        topic_parts.append(bc.get_text(" ", strip=True))
    # First 2 paragraphs of main body content
    main = soup.find("main") or soup.body
    if main:
        pcount = 0
        for p in main.find_all("p"):
            # Skip nav
            if any(isinstance(x, Tag) and x.name in ("nav", "footer") for x in p.parents):
                continue
            txt = p.get_text(" ", strip=True)
            if len(txt) > 40:
                topic_parts.append(txt[:500])
                pcount += 1
                if pcount >= 2:
                    break
    out["topic_words"] = noun_words(" ".join(topic_parts))
    DEST_IDENTITY_CACHE[target] = out
    return out


# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------

def noun_words(text: str) -> set[str]:
    """Extract content words (lowercase, no stopwords, no digits-only).
    Hyphenated compounds are kept whole AND split into sub-words so that
    'evaluation-first' overlaps with 'evaluation'."""
    text = text.replace("&amp;", " ").replace("&#x2014;", " ").replace("&mdash;", " ")
    # Remove parenthetical chapter numbers
    text = re.sub(r"\([^)]*\)", " ", text)
    # Drop punctuation except hyphen
    text = re.sub(r"[^\w\s\-]", " ", text)
    raw = re.findall(r"[A-Za-z][A-Za-z0-9\-]+", text)
    out = set()
    for w in raw:
        wl = w.lower().rstrip("s")  # crude singularize
        if wl not in STOPWORDS and len(wl) >= 3:
            out.add(wl)
        # Also split compound words on hyphen
        if "-" in wl:
            for part in wl.split("-"):
                part = part.strip().rstrip("s")
                if part and len(part) >= 3 and part not in STOPWORDS:
                    out.add(part)
    return out


def classify_href(href: str) -> str:
    h = href.strip()
    sp = urlsplit(h)
    if sp.scheme in ("http", "https", "mailto", "tel", "javascript", "data", "ftp", "ftps", "ws", "wss"):
        return "external"
    if h.startswith("//"):
        return "external"
    if h.startswith("#"):
        return "anchor"
    return "internal"


def resolve_target(page: Path, href: str) -> Path | None:
    if not href:
        return None
    sp = urlsplit(href)
    path_part = unquote(sp.path)
    if not path_part:
        return None
    base = page.parent
    try:
        if path_part.startswith("/"):
            target = (ROOT / path_part.lstrip("/")).resolve()
        else:
            target = (base / path_part).resolve()
    except Exception:
        return None
    if path_part.endswith("/"):
        return target / "index.html"
    if target.exists() and target.is_dir():
        return target / "index.html"
    if not target.suffix and not target.exists():
        as_dir = target / "index.html"
        if as_dir.exists():
            return as_dir
    return target


def is_in_structural_nav(a: Tag) -> bool:
    for anc in a.parents:
        if not isinstance(anc, Tag):
            continue
        if anc.name == "nav":
            classes = anc.get("class") or []
            if any(c in ("chapter-nav", "header-nav") for c in classes):
                return True
        if anc.name == "header" and any(c in ("chapter-header",) for c in (anc.get("class") or [])):
            # Only header-nav links inside the header are structural; ToC links to chapters are still in body
            # We treat the breadcrumb-style links inside chapter-header as structural too,
            # since they're not body prose.
            return True
        if anc.name == "footer":
            return True
    return False


def get_surrounding_text(a: Tag, anchor_text: str) -> str:
    """Try to capture a sentence or two of surrounding context."""
    parent = a.find_parent(["p", "li", "td", "div", "figcaption"])
    if not parent:
        return anchor_text
    raw = parent.get_text(" ", strip=True)
    if len(raw) > 350:
        # Try to find the anchor within and grab a window
        idx = raw.find(anchor_text)
        if idx >= 0:
            start = max(0, idx - 150)
            end = min(len(raw), idx + len(anchor_text) + 200)
            return ("..." if start > 0 else "") + raw[start:end] + ("..." if end < len(raw) else "")
        return raw[:350] + "..."
    return raw


# -------------------------------------------------------------
# Main audit
# -------------------------------------------------------------

def main() -> None:
    print("Building inventory ...")
    build_inventory()
    print(f"  disk chapters: {len(CHAPTER_TO_DIR)}")
    print(f"  disk appendices: {len(APPENDIX_LETTER_TO_DIR)}")

    pages = iter_html_files()
    print(f"Scanning {len(pages)} HTML files for cross-link relevance ...")

    # Buckets
    p0_topic_mismatch = []   # (file, line, text, href, dest_h1, surrounding)
    p1_number_drift = []     # (file, line, text, href, cited_num, dest_num, kind)
    p2_stale_label = []      # (file, line, text, href, label)
    p3_over_promise = []     # (file, line, text, href, dest_h1, surrounding)
    relevant_count = 0
    total_checked = 0
    skipped_external = 0
    skipped_anchor = 0
    skipped_self = 0
    skipped_nav = 0
    broken_skipped = 0

    # Dropped reference labels seen
    dropped_label_counter: Counter[str] = Counter()
    p0_pattern_counter: Counter[str] = Counter()
    p1_pattern_counter: Counter[str] = Counter()

    for i, page in enumerate(pages):
        if i % 100 == 0:
            print(f"  {i}/{len(pages)} ...")
        try:
            html_text = page.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        try:
            soup = BeautifulSoup(html_text, "html.parser")
        except Exception:
            continue
        body = soup.body
        if body is None:
            continue

        for a in body.find_all("a"):
            href = a.get("href")
            if href is None:
                continue
            href = href.strip()
            if not href:
                continue
            if is_in_structural_nav(a):
                skipped_nav += 1
                continue
            kind = classify_href(href)
            if kind == "external":
                skipped_external += 1
                continue
            if kind == "anchor":
                skipped_anchor += 1
                continue

            anchor_text = a.get_text(" ", strip=True)
            if not anchor_text:
                continue

            # Self-link?
            target = resolve_target(page, href)
            if target is None:
                broken_skipped += 1
                continue
            try:
                if target.resolve() == page.resolve():
                    skipped_self += 1
                    continue
            except Exception:
                pass

            line = getattr(a, "sourceline", None) or 0

            # Stale-label check (P2) is independent of broken/working href
            stale_matched = False
            for pat in DROPPED_RESOURCES:
                if pat.search(anchor_text):
                    label = pat.search(anchor_text).group(0)
                    p2_stale_label.append((rel(page), line, anchor_text, href, label))
                    dropped_label_counter[label] += 1
                    stale_matched = True
                    break

            if not target.exists():
                broken_skipped += 1
                continue

            total_checked += 1

            # Get destination identity
            ident = destination_identity(target)
            dest_h1 = ident["h1"]
            dest_chapter = ident["chapter_num"]
            dest_appendix = ident["appendix_letter"]
            dest_section = ident["section_label"]

            # Cited-number checks (P1)
            # Important: if the anchor text STARTS with a section number ("0.1 ML Basics..."),
            # an embedded "Chapter N" mention inside is descriptive prose, not the link's claim.
            # Only treat the anchor as making a chapter/section claim if the anchor's leading
            # tokens contain that claim.
            m_chapter = PAT_CHAPTER.search(anchor_text)
            m_section = PAT_SECTION.search(anchor_text)
            m_apx = PAT_APPENDIX.search(anchor_text)
            m_apx_sec = PAT_APPENDIX_SEC.search(anchor_text)
            m_part = PAT_PART.search(anchor_text)

            # Heuristic: if anchor text starts with "N.M " or "N.M:" (section number),
            # ignore any embedded "Chapter X" mention.
            starts_with_section = re.match(r"^\s*\d+\.\d+\b", anchor_text) is not None
            # Heuristic: if anchor text starts with "X.M " (appendix letter section), ignore embedded
            starts_with_apx_section = re.match(r"^\s*[A-Z]\.\d+\b", anchor_text) is not None

            # An anchor might say "Chapter 27 (LLM Applications)" and point to chapter 42.
            cited_chapter = None
            cited_section = None
            cited_appendix = None
            cited_apx_sec = None
            cited_part = None
            if m_chapter and not starts_with_section:
                try:
                    cited_chapter = int(m_chapter.group(1))
                except ValueError:
                    pass
            if m_section and not starts_with_section:
                cited_section = m_section.group(1)
            # If anchor starts with a section number, that IS the cited section.
            if starts_with_section:
                m = re.match(r"^\s*(\d+\.\d+(?:\.[\dA-Za-z]+)?)\b", anchor_text)
                if m:
                    cited_section = m.group(1)
            if m_apx_sec and not starts_with_apx_section:
                cited_apx_sec = m_apx_sec.group(1).upper()
            elif m_apx and not starts_with_apx_section:
                cited_appendix = m_apx.group(1).upper()
            if starts_with_apx_section:
                m = re.match(r"^\s*([A-Z]\.\d+(?:\.[\dA-Za-z]+)?)\b", anchor_text)
                if m:
                    cited_apx_sec = m.group(1).upper()
            if m_part:
                cited_part = m_part.group(1)

            # ---- Number drift ----
            # If cited a chapter number AND destination is a chapter page (or section thereof)
            number_drift_logged = False
            # Use wider topic_words for overlap checks; falls back to title_words.
            d_topic = ident["topic_words"] or ident["title_words"]
            if cited_chapter is not None and dest_chapter is not None:
                if cited_chapter != dest_chapter:
                    # Need to decide: is this drift (topic right) or mismatch (topic wrong)?
                    # Compare topical word overlap of anchor_text vs dest topic_words.
                    a_words = noun_words(anchor_text)
                    overlap = len(a_words & d_topic)
                    surrounding = get_surrounding_text(a, anchor_text)
                    if overlap >= 1 or len(a_words) == 0:
                        # P1: number drift (topic still matches)
                        p1_number_drift.append((
                            rel(page), line, anchor_text, href,
                            f"Chapter {cited_chapter}",
                            f"Chapter {dest_chapter}: {dest_h1}",
                            "Chapter",
                        ))
                        p1_pattern_counter[f"Chapter {cited_chapter} -> Chapter {dest_chapter}"] += 1
                    else:
                        # P0: mismatched topic
                        p0_topic_mismatch.append((
                            rel(page), line, anchor_text, href,
                            f"Chapter {dest_chapter}: {dest_h1}",
                            surrounding,
                        ))
                        p0_pattern_counter[f"Chapter {cited_chapter} -> Chapter {dest_chapter}"] += 1
                    number_drift_logged = True

            if cited_section is not None and dest_section is not None and not number_drift_logged:
                if cited_section.lower() != dest_section.lower():
                    # Strip trailing nested if dest is parent
                    cited_top2 = ".".join(cited_section.split(".")[:2])
                    dest_top2 = ".".join(dest_section.split(".")[:2])
                    if cited_top2.lower() != dest_top2.lower():
                        a_words = noun_words(anchor_text)
                        overlap = len(a_words & d_topic)
                        surrounding = get_surrounding_text(a, anchor_text)
                        if overlap >= 1 or len(a_words) == 0:
                            p1_number_drift.append((
                                rel(page), line, anchor_text, href,
                                f"Section {cited_section}",
                                f"Section {dest_section}: {dest_h1}",
                                "Section",
                            ))
                            p1_pattern_counter[f"Section {cited_top2} -> Section {dest_top2}"] += 1
                        else:
                            p0_topic_mismatch.append((
                                rel(page), line, anchor_text, href,
                                f"Section {dest_section}: {dest_h1}",
                                surrounding,
                            ))
                            p0_pattern_counter[f"Section {cited_top2} -> Section {dest_top2}"] += 1
                        number_drift_logged = True

            if cited_appendix is not None and dest_appendix is not None and not number_drift_logged:
                if cited_appendix != dest_appendix:
                    a_words = noun_words(anchor_text)
                    overlap = len(a_words & d_topic)
                    surrounding = get_surrounding_text(a, anchor_text)
                    if overlap >= 1 or len(a_words) == 0:
                        p1_number_drift.append((
                            rel(page), line, anchor_text, href,
                            f"Appendix {cited_appendix}",
                            f"Appendix {dest_appendix}: {dest_h1}",
                            "Appendix",
                        ))
                        p1_pattern_counter[f"Appendix {cited_appendix} -> Appendix {dest_appendix}"] += 1
                    else:
                        p0_topic_mismatch.append((
                            rel(page), line, anchor_text, href,
                            f"Appendix {dest_appendix}: {dest_h1}",
                            surrounding,
                        ))
                        p0_pattern_counter[f"Appendix {cited_appendix} -> Appendix {dest_appendix}"] += 1
                    number_drift_logged = True

            if cited_apx_sec is not None and dest_section is not None and dest_appendix is not None and not number_drift_logged:
                # Compare "K.4" vs section_label
                if cited_apx_sec.upper() != dest_section.upper():
                    a_words = noun_words(anchor_text)
                    overlap = len(a_words & d_topic)
                    surrounding = get_surrounding_text(a, anchor_text)
                    if overlap >= 1 or len(a_words) == 0:
                        p1_number_drift.append((
                            rel(page), line, anchor_text, href,
                            f"Appendix {cited_apx_sec}",
                            f"Appendix {dest_section}: {dest_h1}",
                            "AppendixSection",
                        ))
                        p1_pattern_counter[f"Appendix {cited_apx_sec} -> Appendix {dest_section}"] += 1
                    else:
                        p0_topic_mismatch.append((
                            rel(page), line, anchor_text, href,
                            f"Appendix {dest_section}: {dest_h1}",
                            surrounding,
                        ))
                        p0_pattern_counter[f"Appendix {cited_apx_sec} -> Appendix {dest_section}"] += 1
                    number_drift_logged = True

            if cited_part is not None and ident["part_num"] is not None and not number_drift_logged:
                cited_part_num = ROMAN_TO_PART_NUM.get(cited_part)
                if cited_part_num is not None and cited_part_num != ident["part_num"]:
                    a_words = noun_words(anchor_text)
                    overlap = len(a_words & d_topic)
                    surrounding = get_surrounding_text(a, anchor_text)
                    if overlap >= 1 or len(a_words) == 0:
                        p1_number_drift.append((
                            rel(page), line, anchor_text, href,
                            f"Part {cited_part}",
                            f"Part {PART_NUM_TO_ROMAN.get(ident['part_num'], '?')}",
                            "Part",
                        ))
                        p1_pattern_counter[f"Part {cited_part} -> Part {PART_NUM_TO_ROMAN.get(ident['part_num'], '?')}"] += 1
                    else:
                        p0_topic_mismatch.append((
                            rel(page), line, anchor_text, href,
                            f"Part {PART_NUM_TO_ROMAN.get(ident['part_num'], '?')}",
                            surrounding,
                        ))
                        p0_pattern_counter[f"Part {cited_part} -> Part {PART_NUM_TO_ROMAN.get(ident['part_num'], '?')}"] += 1
                    number_drift_logged = True

            if number_drift_logged or stale_matched:
                continue

            # ---- General topic match (when no number is cited) ----
            # If anchor text is short ("here", "this", "above"), skip topical compare.
            stop_anchors = {
                "here", "this", "this section", "this chapter", "this appendix",
                "above", "below", "previous", "next", "back", "back to top",
                "top", "see", "see here", "read more", "more", "details",
                "click here", "link", "go", "section", "chapter", "appendix",
                "introduction", "summary", "conclusion", "overview",
                "previous section", "next section",
                # UI / CTA buttons
                "read free online", "read on web", "start here", "start here →",
                "buy on amazon", "buy on amazon ➝", "download pdf",
                "download pdf (free)", "free chapter (pdf)", "table of contents",
                "contents", "toc", "skip to content", "skip to main content",
                "search", "home", "back to home", "view source", "github",
                "buy", "get the book", "preview", "sample", "free pdf",
            }
            atxt_norm = anchor_text.strip().lower().rstrip(".:,")
            if atxt_norm in stop_anchors or len(atxt_norm) <= 3:
                relevant_count += 1
                continue

            a_words = noun_words(anchor_text)
            d_words = ident["topic_words"] or ident["title_words"]
            if not a_words or not d_words:
                relevant_count += 1
                continue
            # If anchor mentions Chapter/Section/Appendix but no number,
            # still rely on topic words.
            overlap = len(a_words & d_words)
            if overlap == 0:
                # Possibly a topic mismatch. But be lenient: many anchors
                # use friendly phrasing. Only flag P0 if at least 2 strong
                # content words in the anchor and zero overlap.
                strong_anchor_words = a_words - {"build", "use", "using", "build", "using",
                                                  "guide", "patterns", "pattern", "make",
                                                  "design", "way", "ways", "tip", "tips",
                                                  "best", "important", "key", "core",
                                                  "introduction", "overview", "summary",
                                                  "engineer", "engineering", "research",
                                                  "production", "applications", "application"}
                if len(strong_anchor_words) >= 2:
                    surrounding = get_surrounding_text(a, anchor_text)
                    p0_topic_mismatch.append((
                        rel(page), line, anchor_text, href,
                        dest_h1 or rel(target),
                        surrounding,
                    ))
                else:
                    relevant_count += 1
            else:
                relevant_count += 1

    # -------------------------------------------------------------
    # Compose the report
    # -------------------------------------------------------------

    p0_topic_mismatch.sort(key=lambda r: (r[0], r[1]))
    p1_number_drift.sort(key=lambda r: (r[0], r[1]))
    p2_stale_label.sort(key=lambda r: (r[0], r[1]))
    p3_over_promise.sort(key=lambda r: (r[0], r[1]))

    n_p0 = len(p0_topic_mismatch)
    n_p1 = len(p1_number_drift)
    n_p2 = len(p2_stale_label)
    n_p3 = len(p3_over_promise)

    lines: list[str] = []
    lines.append("# Cross-Link Integrity Audit")
    lines.append("")
    lines.append("Read-only audit of cross-link RELEVANCE, complementing `html-integrity-audit.md`")
    lines.append("(which catches broken hrefs). This audit catches links where the destination is")
    lines.append("reachable but the link text or surrounding claim no longer matches what is at")
    lines.append("the destination (the v6-v9 reshuffles moved targets while leaving prose untouched).")
    lines.append("")
    lines.append(f"Root: `{ROOT.as_posix()}` | HTML pages scanned: {len(pages)}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Cross-links checked (excluding nav / external / anchor / self / broken): {total_checked}")
    lines.append(f"- Resolvable + relevant: {relevant_count}")
    lines.append(f"- P0 (mismatched topic): {n_p0}")
    lines.append(f"- P1 (number drift, topic right): {n_p1}")
    lines.append(f"- P2 (stale label, dropped resource): {n_p2}")
    lines.append(f"- P3 (over-promise): {n_p3}")
    lines.append("")
    lines.append(f"_Skipped: {skipped_external} external, {skipped_anchor} anchor-only, "
                 f"{skipped_self} self, {skipped_nav} structural-nav, {broken_skipped} broken hrefs._")
    lines.append("")

    # ---- P0: mismatched topic ----
    lines.append("## P0: Mismatched topic")
    lines.append("")
    lines.append("Anchor text describes one topic; destination page is about something else.")
    lines.append("These are the lies-by-omission: the reader clicks expecting X and lands on Y.")
    lines.append("")
    if not p0_topic_mismatch:
        lines.append("_None detected._")
        lines.append("")
    else:
        # Group entries by (anchor_text, dest_h1) to dedupe.
        grouped: dict[tuple[str, str], list[tuple[str, int, str]]] = defaultdict(list)
        for f, ln, atxt, href, dest, surrounding in p0_topic_mismatch:
            grouped[(atxt[:140], dest[:140])].append((f, ln, href))
        # Sort groups by frequency desc, then alphabetical
        sorted_groups = sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        BUDGET_GROUPS = 50
        for (atxt, dest), occs in sorted_groups[:BUDGET_GROUPS]:
            if len(occs) > 1:
                lines.append(f"- ({len(occs)} occurrences) Text: `{atxt}`")
            else:
                lines.append(f"- Text: `{atxt}`")
            lines.append(f"  Destination: {dest}")
            # First occurrence + maybe a sample href
            f0, l0, h0 = occs[0]
            lines.append(f"  Example: `{f0}:{l0}` href=`{h0}`")
            if len(occs) > 1:
                more = ", ".join(f"`{f}:{l}`" for f, l, _ in occs[1:6])
                lines.append(f"  Other: {more}{' (...)' if len(occs) > 7 else ''}")
            lines.append("")
        if len(sorted_groups) > BUDGET_GROUPS:
            lines.append(f"_(... and {len(sorted_groups) - BUDGET_GROUPS} more unique mismatch patterns, capped.)_")
            lines.append("")

    # ---- P1: number drift ----
    lines.append("## P1: Number drift (topic right, citation stale)")
    lines.append("")
    lines.append("Anchor cites a chapter / section / appendix number that no longer matches the")
    lines.append("destination, but the destination IS still about the same topic. Rewrite the prose")
    lines.append("to cite the new number; the href is already correct.")
    lines.append("")
    if not p1_number_drift:
        lines.append("_None detected._")
        lines.append("")
    else:
        # Group by (cited, dest_number)
        p1_grouped: dict[tuple[str, str], list[tuple[str, int, str, str]]] = defaultdict(list)
        for f, ln, atxt, href, cited, dest, kind in p1_number_drift:
            p1_grouped[(cited[:80], dest[:140])].append((f, ln, atxt, href))
        sorted_p1 = sorted(p1_grouped.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        BUDGET_GROUPS = 50
        for (cited, dest), occs in sorted_p1[:BUDGET_GROUPS]:
            n = len(occs)
            header = f"- {cited} -> {dest}"
            if n > 1:
                header += f" ({n} occurrences)"
            lines.append(header)
            f0, l0, atxt0, h0 = occs[0]
            lines.append(f"  Example: `{f0}:{l0}` text=`{atxt0[:120]}`")
            if n > 1:
                more = ", ".join(f"`{f}:{l}`" for f, l, _, _ in occs[1:6])
                lines.append(f"  Other: {more}{' (...)' if n > 7 else ''}")
            lines.append("")
        if len(sorted_p1) > BUDGET_GROUPS:
            lines.append(f"_(... and {len(sorted_p1) - BUDGET_GROUPS} more unique drift patterns, capped.)_")
            lines.append("")

    # ---- P2: stale label ----
    lines.append("## P2: Stale label (dropped resource)")
    lines.append("")
    lines.append("Anchor text refers to a resource that was dropped in v9 (Master Reference Tables,")
    lines.append("2026 Freshness Index, Appendix AD/AE/AI). The href may resolve to a different")
    lines.append("appendix now, but the prose still names the old one. Rephrase to drop the")
    lines.append("reference or re-point to the actual current resource.")
    lines.append("")
    if not p2_stale_label:
        lines.append("_None detected._")
        lines.append("")
    else:
        # Group by file
        BUDGET = 60
        for f, ln, atxt, href, label in p2_stale_label[:BUDGET]:
            lines.append(f"- `{f}:{ln}`")
            lines.append(f"  Text: `{atxt[:200]}`")
            lines.append(f"  href: `{href}`")
            lines.append(f"  Stale label: `{label}`")
            lines.append("")
        if n_p2 > BUDGET:
            lines.append(f"_(... and {n_p2 - BUDGET} more, capped for report size.)_")
            lines.append("")

    # ---- P3: over-promise ----
    lines.append("## P3: Over-promise")
    lines.append("")
    lines.append("Claim makes a specific promise (\"for the GitHub Actions recipe\",")
    lines.append("\"see the YAML example\") that the destination section may not fulfill.")
    lines.append("Detection is heuristic; we do not actively flag P3 yet (manual spot-check needed).")
    lines.append("")
    if not p3_over_promise:
        lines.append("_None auto-detected. Consider a manual sweep for prose like \"for the X recipe\","
                     " \"see the example below\"._")
        lines.append("")

    # ---- Top patterns ----
    lines.append("## Top patterns")
    lines.append("")
    lines.append("### P0 mismatch frequency")
    lines.append("")
    if p0_pattern_counter:
        lines.append("| Occurrences | Citation -> Destination |")
        lines.append("|---:|---|")
        for pat, c in p0_pattern_counter.most_common(15):
            lines.append(f"| {c} | `{pat}` |")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("### P1 number-drift frequency")
    lines.append("")
    if p1_pattern_counter:
        lines.append("| Occurrences | Citation -> Destination |")
        lines.append("|---:|---|")
        for pat, c in p1_pattern_counter.most_common(20):
            lines.append(f"| {c} | `{pat}` |")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("### P2 dropped-resource labels")
    lines.append("")
    if dropped_label_counter:
        lines.append("| Occurrences | Stale label |")
        lines.append("|---:|---|")
        for lbl, c in dropped_label_counter.most_common(15):
            lines.append(f"| {c} | `{lbl}` |")
    else:
        lines.append("_None._")
    lines.append("")

    # ---- Per-file rollup (top 20 dirtiest files) ----
    file_counter: Counter[str] = Counter()
    for f, *_ in p0_topic_mismatch:
        file_counter[f] += 1
    for f, *_ in p1_number_drift:
        file_counter[f] += 1
    for f, *_ in p2_stale_label:
        file_counter[f] += 1
    for f, *_ in p3_over_promise:
        file_counter[f] += 1
    if file_counter:
        lines.append("### Files with most relevance issues (top 20)")
        lines.append("")
        lines.append("| Issues | File |")
        lines.append("|---:|---|")
        for f, c in file_counter.most_common(20):
            lines.append(f"| {c} | `{f}` |")
        lines.append("")

    # ---- Method notes ----
    lines.append("## Method notes")
    lines.append("")
    lines.append("Audit logic (`scripts/_audit_crosslink_relevance.py`):")
    lines.append("")
    lines.append("1. Walk every `<a href>` in `<body>` (skipping `nav.chapter-nav`, `nav.header-nav`, ")
    lines.append("   `header.chapter-header`, `footer`).")
    lines.append("2. Skip external, anchor-only, self, and broken-target links.")
    lines.append("3. For each link, read the destination file's `<h1>` and path-derived identity ")
    lines.append("   (chapter number from `module-NN-*`, section from `section-N.M.html`, etc.).")
    lines.append("4. P1 = anchor mentions a chapter/section/appendix/part number that does not match ")
    lines.append("   the destination's actual number, but the topic noun-phrase still overlaps the ")
    lines.append("   destination `<h1>` (>=1 content word in common).")
    lines.append("5. P0 = number cited and destination differ AND the topic noun-phrase has zero ")
    lines.append("   overlap with the destination `<h1>` (or anchor text has >=2 strong content words ")
    lines.append("   and zero overlap with the destination, even without a number).")
    lines.append("6. P2 = anchor text contains a dropped-resource label ('Master Reference Tables', ")
    lines.append("   'Freshness Index', 'Appendix AD/AE/AI'), independent of href resolution.")
    lines.append("7. Word overlap is computed over lowercased content words (>=3 chars, not stopwords), ")
    lines.append("   crudely singularized. Some false negatives are inevitable on synonyms.")
    lines.append("")
    lines.append("Limitations:")
    lines.append("")
    lines.append("- Single-word anchor text (\"here\", \"see\", \"this section\") is not checked for topic match.")
    lines.append("- Synonym mismatch ('RAG' vs 'Retrieval-Augmented Generation') may slip through if both ")
    lines.append("  forms appear in the destination's `<h1>` we'll match.")
    lines.append("- P3 (over-promise like \"GitHub Actions recipe\" pointing to a page that does not ")
    lines.append("  contain that recipe) is not auto-detected; the section is reserved for manual notes.")
    lines.append("- Some agents are actively editing files (C/D/E/F/G, H/I/J/K, Tools-of-the-Trade, ")
    lines.append("  whats-next blocks); their changes may not be reflected here.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Audit generated by `scripts/_audit_crosslink_relevance.py` (read-only).")
    lines.append("")

    # Cap at 700 lines
    if len(lines) > 700:
        # Trim each large detail block in reverse priority: P0 stays, P1 trimmed, P2 trimmed.
        # We do a hard cap: keep first 700 lines + a footer marker.
        kept = lines[:699]
        kept.append("_[Report truncated to 700 lines. See per-pattern frequency tables above for full counts.]_")
        lines = kept

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written: {OUT_PATH}  (P0={n_p0}, P1={n_p1}, P2={n_p2}, P3={n_p3})")


if __name__ == "__main__":
    main()
