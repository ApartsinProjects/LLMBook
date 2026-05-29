#!/usr/bin/env python3
"""Audit orphan figure captions and unresolved figure references.

Categories:
  A. Orphan <figcaption>: <figcaption> inside a <figure> whose body lacks
     <img>, <svg>, <pre>, <table>, <iframe>, <canvas>, .diagram-container.
  B. Unresolved Figure-X.Y mentions in prose: "see Figure X.Y" but no
     matching figure label exists in the page (or any page, for global refs).
  C. Orphan .diagram-caption divs: <div class="diagram-caption">...</div>
     whose preceding sibling has no <img>, <svg>, <pre>, <table>, <canvas>.
  D. Empty <figure> wrappers: <figure> with only whitespace + figcaption.
  E. Sibling-orphan figcaption: <figcaption> not inside a <figure>.

Repository root is auto-detected (parents of this file).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

try:
    from bs4 import BeautifulSoup, Tag, NavigableString  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit("This script requires beautifulsoup4. Install with `pip install beautifulsoup4`.") from exc


REPO_ROOT = Path(__file__).resolve().parents[2]

SKIP_DIRS = {
    "node_modules",
    ".git",
    ".github",
    "pagefind",
    "temp_epub",
    ".html2epub_cache",
    "vendor",
    "source_fix_backups",
}

# Inside KDP/, skip build artifacts only — still scan KDP/index.html etc.
KDP_SKIP_SUBDIRS = {"build", "output", "html2epub"}

CONTENT_TAGS = {"img", "svg", "pre", "table", "iframe", "canvas", "video", "audio", "object"}
CONTENT_CLASS_HINTS = {"diagram-container", "mermaid", "katex-display", "math-block"}

FIG_LABEL_RE = re.compile(r"\bFigure\s+([A-Z0-9]+(?:\.\d+){0,3})\b", re.IGNORECASE)
# Require a digit/dot/letter pattern that looks like an actual numbered label,
# not the English noun "figure" (e.g., "figure out", "figure this", "stick-figure").
# We also require the leading word "Figure" to be capitalised, which is the
# convention used throughout the book for genuine references.
FIG_REF_PHRASE_RE = re.compile(
    r"(?<![\w-])Figure\s+([A-Z]?\d+(?:\.\d+){1,3}[a-z]?)\b",
)
FIG_CAPTION_LABEL_RE = re.compile(r"Figure\s+([A-Z0-9]+(?:\.\d+){0,3})", re.IGNORECASE)


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return True
    # KDP build / output / html2epub subtrees
    try:
        idx = path.parts.index("KDP")
    except ValueError:
        return False
    after = path.parts[idx + 1:]
    if after and after[0] in KDP_SKIP_SUBDIRS:
        return True
    return False


def iter_html_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.html"):
        if should_skip(p.relative_to(root)):
            continue
        yield p


def has_content_child(figure: Tag) -> tuple[bool, str]:
    """Return (has_content, reason). Recurses through descendants."""
    for desc in figure.descendants:
        if not isinstance(desc, Tag):
            continue
        if desc.name == "figcaption":
            continue
        if desc.name in CONTENT_TAGS:
            return True, f"<{desc.name}>"
        classes = set(desc.get("class") or [])
        if classes & CONTENT_CLASS_HINTS:
            return True, f"<{desc.name} class={'.'.join(classes)}>"
        # ASCII art often lives in <code> blocks too
        if desc.name == "code" and len((desc.get_text() or "").splitlines()) >= 3:
            return True, "<code multiline>"
    # Plain text body? Anything substantial that isn't inside the caption?
    body_text_parts = []
    for child in figure.children:
        if isinstance(child, Tag) and child.name == "figcaption":
            continue
        if isinstance(child, NavigableString):
            body_text_parts.append(str(child))
        elif isinstance(child, Tag):
            body_text_parts.append(child.get_text(" ", strip=True))
    body_text = " ".join(body_text_parts).strip()
    if len(body_text) >= 40:
        return True, f"text body ({len(body_text)} chars)"
    return False, ""


def caption_label(text: str) -> str | None:
    if not text:
        return None
    m = FIG_CAPTION_LABEL_RE.search(text)
    return m.group(1) if m else None


def find_figure_labels(soup: BeautifulSoup) -> set[str]:
    """All figure labels declared in this document, normalized lowercased."""
    labels: set[str] = set()
    # <figure> -> <figcaption>
    for fc in soup.find_all("figcaption"):
        lbl = caption_label(fc.get_text(" ", strip=True))
        if lbl:
            labels.add(lbl.lower())
    # <div class="diagram-caption">
    for dc in soup.find_all("div", class_="diagram-caption"):
        lbl = caption_label(dc.get_text(" ", strip=True))
        if lbl:
            labels.add(lbl.lower())
    # <table><caption>...Figure N.N.N (Table): ...</caption>
    for tc in soup.find_all("caption"):
        lbl = caption_label(tc.get_text(" ", strip=True))
        if lbl:
            labels.add(lbl.lower())
    # Also bare figure ids like id="fig-x-y-z"
    for tag in soup.find_all(id=re.compile(r"^fig[-_].+", re.IGNORECASE)):
        fid = tag.get("id", "")
        # e.g. fig-2-3-1 -> 2.3.1 ; fig-c-1 -> c.1
        bits = re.sub(r"^fig[-_]", "", fid, flags=re.IGNORECASE).replace("-", ".").replace("_", ".")
        if bits:
            labels.add(bits.lower())
    return labels


def collect_diagram_caption_orphans(soup: BeautifulSoup, file_rel: Path) -> list[dict]:
    out = []
    for dc in soup.find_all("div", class_="diagram-caption"):
        # First check siblings within the diagram-caption's parent (typical
        # pattern: figure/div containing diagram element + caption).
        prev = dc
        has_diagram = False
        steps = 0
        while True:
            prev = prev.previous_sibling
            if prev is None:
                break
            if isinstance(prev, NavigableString):
                if prev.strip() == "":
                    continue
                break
            if not isinstance(prev, Tag):
                break
            steps += 1
            if prev.name in CONTENT_TAGS:
                has_diagram = True
                break
            classes = set(prev.get("class") or [])
            if classes & CONTENT_CLASS_HINTS:
                has_diagram = True
                break
            if prev.find(lambda t: isinstance(t, Tag) and t.name in CONTENT_TAGS):
                has_diagram = True
                break
            if steps > 3:
                break

        # Also scan the immediate parent ONLY if it's a known diagram wrapper
        # (figure, .diagram-container, .figure-container) -- not an arbitrary div.
        if not has_diagram:
            parent = dc.parent
            if isinstance(parent, Tag):
                parent_classes = set(parent.get("class") or [])
                is_diagram_wrapper = (
                    parent.name == "figure"
                    or "diagram-container" in parent_classes
                    or "figure-container" in parent_classes
                    or "illustration" in parent_classes
                )
                if is_diagram_wrapper:
                    for desc in parent.descendants:
                        if not isinstance(desc, Tag):
                            continue
                        if desc is dc:
                            continue
                        if desc.find_parent(
                            lambda t: isinstance(t, Tag)
                            and t.name == "div"
                            and "diagram-caption" in (t.get("class") or [])
                        ):
                            continue
                        if desc.name in CONTENT_TAGS:
                            has_diagram = True
                            break

        if not has_diagram:
            out.append({
                "file": str(file_rel).replace("\\", "/"),
                "category": "C",
                "label": caption_label(dc.get_text(" ", strip=True)),
                "snippet": dc.get_text(" ", strip=True)[:200],
            })
    return out


def collect_orphan_figcaptions(soup: BeautifulSoup, file_rel: Path) -> list[dict]:
    out = []
    for fc in soup.find_all("figcaption"):
        figure = fc.find_parent("figure")
        if figure is None:
            # Category E: sibling-orphan
            out.append({
                "file": str(file_rel).replace("\\", "/"),
                "category": "E",
                "label": caption_label(fc.get_text(" ", strip=True)),
                "snippet": fc.get_text(" ", strip=True)[:200],
            })
            continue
        has_content, _why = has_content_child(figure)
        text = fc.get_text(" ", strip=True)
        label = caption_label(text)
        if not has_content:
            # Distinguish category A (caption + empty body) from D (truly empty figure)
            other_children = [c for c in figure.children
                              if isinstance(c, Tag) and c.name != "figcaption"]
            empty_body = len(other_children) == 0
            out.append({
                "file": str(file_rel).replace("\\", "/"),
                "category": "D" if empty_body else "A",
                "label": label,
                "snippet": text[:200],
            })
    return out


def collect_figure_refs(soup: BeautifulSoup, file_rel: Path) -> list[dict]:
    """Find 'see Figure X.Y' style references in prose."""
    refs = []
    # Look at every text node not inside <figcaption> or .diagram-caption
    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        if parent is None:
            continue
        # Skip inside captions and code
        if parent.find_parent("figcaption") is not None:
            continue
        if parent.find_parent(lambda t: isinstance(t, Tag)
                              and t.name == "div"
                              and "diagram-caption" in (t.get("class") or [])):
            continue
        if parent.find_parent(["pre", "code", "script", "style"]) is not None:
            continue
        raw = str(text_node)
        for m in FIG_REF_PHRASE_RE.finditer(raw):
            refs.append({
                "file": str(file_rel).replace("\\", "/"),
                "label": m.group(1),
                "phrase": raw[max(0, m.start() - 40): m.end() + 40].strip(),
            })
    return refs


def main():
    figcaption_issues: list[dict] = []
    diagram_caption_issues: list[dict] = []
    figure_refs: list[dict] = []
    all_labels: dict[str, set[str]] = {}   # file_rel -> set of labels
    global_labels: set[str] = set()
    total_figures = 0

    for f in iter_html_files(REPO_ROOT):
        try:
            html = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        soup = BeautifulSoup(html, "html.parser")
        rel = f.relative_to(REPO_ROOT)

        # Total figures with captions
        for fc in soup.find_all("figcaption"):
            total_figures += 1
        for dc in soup.find_all("div", class_="diagram-caption"):
            total_figures += 1
        for tc in soup.find_all("caption"):
            txt = tc.get_text(" ", strip=True)
            if caption_label(txt):
                total_figures += 1

        figcaption_issues.extend(collect_orphan_figcaptions(soup, rel))
        diagram_caption_issues.extend(collect_diagram_caption_orphans(soup, rel))
        labels = find_figure_labels(soup)
        all_labels[str(rel).replace("\\", "/")] = labels
        global_labels |= labels
        figure_refs.extend(collect_figure_refs(soup, rel))

    # Resolve refs: unresolved if label not present in same file AND not in global set.
    unresolved = []
    for ref in figure_refs:
        lbl = ref["label"].lower()
        file_labels = all_labels.get(ref["file"], set())
        if lbl in file_labels:
            continue  # local match
        if lbl in global_labels:
            # Global ref — cross-section reference is fine
            continue
        unresolved.append(ref)

    cat_A = [x for x in figcaption_issues if x["category"] == "A"]
    cat_B = unresolved
    cat_C = diagram_caption_issues
    cat_D = [x for x in figcaption_issues if x["category"] == "D"]
    cat_E = [x for x in figcaption_issues if x["category"] == "E"]

    summary = {
        "total_figures_with_captions": total_figures,
        "category_A_orphan_figcaptions": len(cat_A),
        "category_B_unresolved_refs": len(cat_B),
        "category_C_orphan_diagram_captions": len(cat_C),
        "category_D_empty_figure_wrappers": len(cat_D),
        "category_E_sibling_orphan_figcaptions": len(cat_E),
    }

    output = {
        "summary": summary,
        "category_A": cat_A,
        "category_B": cat_B,
        "category_C": cat_C,
        "category_D": cat_D,
        "category_E": cat_E,
    }

    out_path = REPO_ROOT / "KDP" / "build" / "AUDIT_orphan_figures.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return output


if __name__ == "__main__":
    main()
