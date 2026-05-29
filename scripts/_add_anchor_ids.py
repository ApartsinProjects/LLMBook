"""Audit A: Ensure every sub-h2 and h3 in section files has an id="..." for deep linking.

For every <h2> and <h3> in body content, generate a slug-based id from the heading
text and inject id="..." if missing. The section-title <h2> (the page heading) is
skipped because it is already covered by the page URL + page-current div.

Rules:
- Idempotent: headings that already have id="..." are left untouched.
- Slug format: numeric prefix is preserved as part of the id (so deep links survive
  later title rewrites). Lowercase, alphanumeric + hyphens only.
  Example: <h2>9.5.4 Subsection Title</h2> -> id="9-5-4-subsection-title".
  Example: <h3>9.5.4.2 Sub-sub-section</h3> -> id="9-5-4-2-sub-sub-section".
- We treat the FIRST <h1> in a section file as the section title. Any subsequent
  <h2>/<h3> are subsections and get ids.

Run dry-run (default) to count what would change, --apply to write.

Usage:
    python scripts/_add_anchor_ids.py              # dry-run, prints counts
    python scripts/_add_anchor_ids.py --apply      # write changes
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

# Directories to skip wholesale anywhere in the tree.
EXCLUDE_DIR_NAMES = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "vendor", "scripts", "docs", "styles", ".html2epub_cache", "agents",
    "images", "_concept-figs", "downloads", ".github",
}


def is_excluded(name: str) -> bool:
    if name in EXCLUDE_DIR_NAMES:
        return True
    if name.startswith("temp_"):
        return True
    if "backups" in name:
        return True
    return False


def iter_html_files() -> list[Path]:
    """Return only section files (section-*.html). Index/landing pages keep
    their headings unanchored because deep-linking inside a landing page is
    not the use case; readers deep-link to specific subsections inside a
    content section file like section-9.5.html."""
    out: list[Path] = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if not is_excluded(d)]
        for fn in fns:
            if fn.startswith("section-") and fn.endswith(".html"):
                out.append(Path(dp) / fn)
    return sorted(out)


def slugify(text: str) -> str:
    """Lowercase, alphanumeric + hyphens. Periods in numeric prefixes become hyphens."""
    # Strip HTML entities for the common ones first.
    text = text.replace("&amp;", "and").replace("&nbsp;", " ")
    text = text.replace("&lt;", "lt").replace("&gt;", "gt")
    # Remove anything else that looks like an entity.
    text = re.sub(r"&[a-zA-Z#0-9]+;", "", text)
    text = text.lower()
    # Replace any run of non-alphanumeric with a single hyphen.
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


_TAG_RE = re.compile(r"<[^>]+>")


def heading_text(inner_html: str) -> str:
    """Strip inner tags to recover the plain text of a heading."""
    return _TAG_RE.sub("", inner_html).strip()


# Match <h2 ...>...</h2> and <h3 ...>...</h3>. Captures attrs and inner.
_HEADING_RE = re.compile(
    r"<(?P<tag>h[23])(?P<attrs>[^>]*)>(?P<inner>.*?)</(?P=tag)>",
    re.DOTALL | re.IGNORECASE,
)


def has_id(attrs: str) -> bool:
    return bool(re.search(r"\bid\s*=", attrs, re.IGNORECASE))


def has_class(attrs: str, cls: str) -> bool:
    m = re.search(r'\bclass\s*=\s*"([^"]*)"', attrs, re.IGNORECASE)
    if not m:
        return False
    return cls in m.group(1).split()


def add_id(attrs: str, new_id: str) -> str:
    """Inject id="new_id" into attrs string (assume no existing id)."""
    # Place the id right at the start of attrs for consistency.
    if attrs.startswith(" ") or attrs == "":
        return f' id="{new_id}"' + attrs
    return f' id="{new_id}" ' + attrs


def process_file(path: Path, dry_run: bool) -> tuple[int, list[str]]:
    """Returns (count_added, list_of_collisions_warned)."""
    text = path.read_text(encoding="utf-8")
    # Operate only on content after the closing </header> if present, otherwise on whole body.
    # We pick a conservative boundary: anything inside <main> ... </main> or after </header>.
    # For simplicity, scan all h2/h3 in the file but exclude any nested inside <head> by
    # finding the body start.
    body_idx = text.lower().find("<body")
    if body_idx == -1:
        return 0, []
    head = text[:body_idx]
    body = text[body_idx:]

    # We do NOT want to add ids to navigation headings (those are in <header>) or to the
    # main page <h1>. Only headings inside <main> need ids.
    # The book uses <main class="content"> ... </main> as the content area, so restrict to that.
    main_match = re.search(r"<main\b[^>]*>", body, re.IGNORECASE)
    if not main_match:
        return 0, []
    main_start = main_match.start()
    main_end_match = re.search(r"</main\s*>", body[main_start:], re.IGNORECASE)
    if main_end_match:
        content_start = main_start
        content_end = main_start + main_end_match.end()
    else:
        content_start = main_start
        content_end = len(body)

    head_and_pre = text[:body_idx] + body[:content_start]
    content = body[content_start:content_end]
    after = body[content_end:]

    added = 0
    seen_ids: set[str] = set()
    # Track ids already in content so we don't collide.
    for m in re.finditer(r'\bid\s*=\s*"([^"]+)"', content):
        seen_ids.add(m.group(1))

    collisions: list[str] = []

    def replace(match: re.Match) -> str:
        nonlocal added
        attrs = match.group("attrs")
        inner = match.group("inner")
        tag = match.group("tag")
        # Skip headings that already have an id.
        if has_id(attrs):
            return match.group(0)
        # Skip headings that are inside specific structural classes we don't want to anchor
        # (e.g., callout titles are <div> not <h2>, so this rarely matters, but skip
        # "Show answer" etc.). Quiz answers use <summary>, so they won't match h2/h3.
        plain = heading_text(inner)
        if not plain:
            return match.group(0)
        slug = slugify(plain)
        if not slug:
            return match.group(0)
        # If collision, append a numeric suffix.
        candidate = slug
        i = 2
        while candidate in seen_ids:
            candidate = f"{slug}-{i}"
            i += 1
            if i > 50:
                collisions.append(plain)
                return match.group(0)
        seen_ids.add(candidate)
        added += 1
        new_attrs = add_id(attrs, candidate)
        return f"<{tag}{new_attrs}>{inner}</{tag}>"

    new_content = _HEADING_RE.sub(replace, content)

    if added > 0 and not dry_run:
        new_text = head_and_pre + new_content + after
        path.write_text(new_text, encoding="utf-8")

    return added, collisions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    args = parser.parse_args()

    files = iter_html_files()
    total_added = 0
    files_changed = 0
    collisions: list[tuple[str, str]] = []
    per_file_counts: Counter[str] = Counter()

    for f in files:
        added, coll = process_file(f, dry_run=not args.apply)
        if added > 0:
            files_changed += 1
            total_added += added
            per_file_counts[f.relative_to(ROOT).as_posix()] = added
        for c in coll:
            collisions.append((f.relative_to(ROOT).as_posix(), c))

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"[{mode}] Audit A: anchor ids on h2/h3")
    print(f"  Files scanned:  {len(files)}")
    print(f"  Files changed:  {files_changed}")
    print(f"  IDs added:      {total_added}")
    if collisions:
        print(f"  Collisions:     {len(collisions)} (see below)")
        for path, h in collisions[:20]:
            print(f"    {path}: {h!r}")
    # Top files for visibility.
    if per_file_counts:
        print("  Top files:")
        for path, n in per_file_counts.most_common(10):
            print(f"    {n:4d}  {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
