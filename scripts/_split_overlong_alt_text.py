"""Split <img alt="..."> over 250 chars into a short alt + figcaption description.

Rule:
- Short alt = first clause (up to first comma or first 80 chars, whichever
  comes first) of the long alt.
- Append the remaining alt text to the surrounding <figcaption> (creating
  one if missing), unless the figcaption already contains substantively
  similar content (>= 60% of the long-alt content tokens already present).
- Add aria-describedby pointing at the figcaption's id (assign one if
  missing).

Idempotent: skips images whose alt is already <= 250 chars.

Usage:
    python scripts/_split_overlong_alt_text.py audit
    python scripts/_split_overlong_alt_text.py apply
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "vendor", "scripts", "docs", "styles",
}

ALT_LIMIT = 250
SHORT_ALT_MAX = 80


def find_html_files() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        out.append(p)
    return out


# Match <figure>...</figure> blocks (non-greedy, multiline)
FIGURE_RE = re.compile(r"<figure\b[^>]*>(.*?)</figure>", re.I | re.S)
IMG_RE = re.compile(r"<img\b([^>]*)>", re.I)
ALT_ATTR_RE = re.compile(r"""\balt\s*=\s*(["'])(.*?)\1""", re.I | re.S)
ARIA_DESC_RE = re.compile(r"""\baria-describedby\s*=\s*["'][^"']*["']""", re.I)
FIGCAPTION_RE = re.compile(r"<figcaption\b([^>]*)>(.*?)</figcaption>", re.I | re.S)
ID_ATTR_RE = re.compile(r"""\bid\s*=\s*["']([^"']*)["']""", re.I)


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def split_short(long_alt: str) -> tuple[str, str]:
    """Return (short, rest). Short = up to first comma or SHORT_ALT_MAX."""
    s = normalize(long_alt)
    # Prefer first comma if it falls within SHORT_ALT_MAX
    comma = s.find(",")
    period = s.find(".")
    cut = SHORT_ALT_MAX
    for c in (comma, period):
        if 0 < c <= SHORT_ALT_MAX:
            cut = min(cut, c)
            break
    short = s[:cut].rstrip(", .;:")
    if len(short) < 10 and len(s) > 10:
        # Fall back: word-boundary split near SHORT_ALT_MAX
        m = re.match(r"^(.{1,%d}\S*)" % SHORT_ALT_MAX, s)
        if m:
            short = m.group(1).rstrip(", .;:")
    rest = s[len(short):].lstrip(", .;:").strip()
    return short, rest


def figcaption_covers(rest: str, caption_text: str) -> bool:
    """Heuristic: caption already covers the long-description content."""
    if not rest:
        return True
    rest_words = set(re.findall(r"\w{4,}", normalize(rest).lower()))
    cap_words = set(re.findall(r"\w{4,}", normalize(caption_text).lower()))
    if not rest_words:
        return True
    overlap = len(rest_words & cap_words) / len(rest_words)
    return overlap >= 0.60


def get_text_only(html: str) -> str:
    """Strip tags for content comparison."""
    return re.sub(r"<[^>]+>", " ", html)


def process_figure(figure_html: str, used_ids: set[str], counter: list[int]) -> tuple[str, bool, bool]:
    """Return (new_figure, changed, was_overlong).

    used_ids and counter are mutable accumulators across files for unique ids.
    """
    img_match = IMG_RE.search(figure_html)
    if not img_match:
        return figure_html, False, False
    img_attrs = img_match.group(1)
    alt_match = ALT_ATTR_RE.search(img_attrs)
    if not alt_match:
        return figure_html, False, False
    quote = alt_match.group(1)
    alt_raw = alt_match.group(2)
    alt_text = normalize(alt_raw)
    if len(alt_text) <= ALT_LIMIT:
        return figure_html, False, False

    short, rest = split_short(alt_text)
    cap_match = FIGCAPTION_RE.search(figure_html)
    cap_text_plain = ""
    cap_inner = ""
    cap_id = ""
    cap_attrs = ""
    if cap_match:
        cap_attrs = cap_match.group(1)
        cap_inner = cap_match.group(2)
        cap_text_plain = normalize(get_text_only(cap_inner))
        id_m = ID_ATTR_RE.search(cap_attrs)
        if id_m:
            cap_id = id_m.group(1)

    # Append long-desc to caption if not already covered.
    new_cap_inner = cap_inner
    appended = False
    if not figcaption_covers(rest, cap_text_plain) and rest:
        # Append as a separate sentence at the end of the caption.
        sep = "" if cap_inner.rstrip().endswith((".", "!", "?")) or not cap_inner.strip() else "."
        new_cap_inner = cap_inner.rstrip() + (sep + " " if cap_inner.strip() else "") + rest
        appended = True

    # Assign id to caption if missing.
    if cap_match:
        if not cap_id:
            counter[0] += 1
            new_id = f"long-desc-{counter[0]}"
            while new_id in used_ids:
                counter[0] += 1
                new_id = f"long-desc-{counter[0]}"
            used_ids.add(new_id)
            new_cap_attrs = cap_attrs + f' id="{new_id}"'
            cap_id = new_id
        else:
            new_cap_attrs = cap_attrs
            used_ids.add(cap_id)
        new_cap = f"<figcaption{new_cap_attrs}>{new_cap_inner}</figcaption>"
    else:
        # No figcaption: create one with rest text and a new id.
        counter[0] += 1
        new_id = f"long-desc-{counter[0]}"
        while new_id in used_ids:
            counter[0] += 1
            new_id = f"long-desc-{counter[0]}"
        used_ids.add(new_id)
        cap_id = new_id
        new_cap = f'<figcaption id="{new_id}">{rest}</figcaption>'

    # Replace alt with short and add aria-describedby. Handle self-closing
    # slash and trailing whitespace correctly.
    new_alt = f'alt={quote}{short}{quote}'
    new_img_attrs = ALT_ATTR_RE.sub(new_alt, img_attrs, count=1)
    # Separate any trailing self-closing slash (and whitespace) from the
    # attribute body before splicing in aria-describedby.
    body = new_img_attrs
    suffix = ""
    m_slash = re.search(r"\s*/\s*$", body)
    if m_slash:
        suffix = "/"
        body = body[: m_slash.start()]
    body = body.rstrip()
    if ARIA_DESC_RE.search(body):
        body = ARIA_DESC_RE.sub(f'aria-describedby="{cap_id}"', body, count=1)
    else:
        body = body + f' aria-describedby="{cap_id}"'

    new_img = f"<img{body}{suffix}>"
    new_figure = figure_html.replace(img_match.group(0), new_img, 1)
    if cap_match:
        new_figure = new_figure.replace(cap_match.group(0), new_cap, 1)
    else:
        # Insert <figcaption> just before </figure> in the original figure
        # placeholder. (figure_html itself is the inside; the caller wraps.)
        # Since process_figure receives the whole <figure>...</figure>, insert.
        new_figure = new_figure.replace("</figure>", new_cap + "</figure>", 1)

    return new_figure, True, True


def gather_overlong() -> list[tuple[Path, int, str]]:
    """Return list of (file, count_in_file, sample_alt)."""
    rows = []
    for p in find_html_files():
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if "<img" not in html or "alt=" not in html:
            continue
        count = 0
        sample = ""
        for fm in FIGURE_RE.finditer(html):
            block = fm.group(0)
            imm = IMG_RE.search(block)
            if not imm:
                continue
            am = ALT_ATTR_RE.search(imm.group(1))
            if not am:
                continue
            a = normalize(am.group(2))
            if len(a) > ALT_LIMIT:
                count += 1
                if not sample:
                    sample = a[:120] + "..."
        # Also check <img> not in <figure>
        img_outside_count = 0
        # remove figures, then scan
        html_no_figs = FIGURE_RE.sub("", html)
        for imm in IMG_RE.finditer(html_no_figs):
            am = ALT_ATTR_RE.search(imm.group(1))
            if not am:
                continue
            a = normalize(am.group(2))
            if len(a) > ALT_LIMIT:
                img_outside_count += 1
        if count or img_outside_count:
            rows.append((p, count + img_outside_count, sample))
    rows.sort(key=lambda r: (-r[1], r[0].as_posix()))
    return rows


def apply_to_file(p: Path, used_ids: set[str], counter: list[int]) -> int:
    """Return number of images split."""
    try:
        html = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return 0
    if "<img" not in html or "alt=" not in html:
        return 0

    # Seed used_ids with any existing ids in the file.
    for m in re.finditer(r"""\bid\s*=\s*["']([^"']*)["']""", html):
        used_ids.add(m.group(1))

    changed = 0

    def repl(match: re.Match) -> str:
        nonlocal changed
        new_fig, did_change, _ = process_figure(match.group(0), used_ids, counter)
        if did_change:
            changed += 1
        return new_fig

    new_html = FIGURE_RE.sub(repl, html)

    # For <img> outside <figure>, wrap in <figure>...<figcaption>...</figcaption></figure>
    # to provide a place for the long description.
    def wrap_repl(match: re.Match) -> str:
        nonlocal changed
        img_full = match.group(0)
        img_attrs = match.group(1)
        am = ALT_ATTR_RE.search(img_attrs)
        if not am:
            return img_full
        a = normalize(am.group(2))
        if len(a) <= ALT_LIMIT:
            return img_full
        short, rest = split_short(a)
        counter[0] += 1
        new_id = f"long-desc-{counter[0]}"
        while new_id in used_ids:
            counter[0] += 1
            new_id = f"long-desc-{counter[0]}"
        used_ids.add(new_id)
        new_attrs = ALT_ATTR_RE.sub(f'alt="{short}"', img_attrs, count=1)
        body = new_attrs
        suffix = ""
        m_slash = re.search(r"\s*/\s*$", body)
        if m_slash:
            suffix = "/"
            body = body[: m_slash.start()]
        body = body.rstrip()
        body = body + f' aria-describedby="{new_id}"'
        changed += 1
        return f'<figure><img{body}{suffix}><figcaption id="{new_id}">{rest}</figcaption></figure>'

    # Only run wrap_repl on images NOT inside a figure. We do this by
    # splitting on <figure>...</figure> blocks.
    # We do this after the figure_re pass, so any img inside figure is
    # already handled. Now operate on segments outside figures.
    parts: list[str] = []
    last = 0
    for m in FIGURE_RE.finditer(new_html):
        outside = new_html[last:m.start()]
        outside = IMG_RE.sub(wrap_repl, outside)
        parts.append(outside)
        parts.append(m.group(0))
        last = m.end()
    parts.append(IMG_RE.sub(wrap_repl, new_html[last:]))
    new_html = "".join(parts)

    if new_html != html:
        p.write_text(new_html, encoding="utf-8")
    return changed


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "audit"
    if cmd == "audit":
        rows = gather_overlong()
        total = sum(r[1] for r in rows)
        print(f"images with alt > {ALT_LIMIT} chars: {total} across {len(rows)} files")
        for p, n, sample in rows[:50]:
            rel = p.relative_to(ROOT).as_posix()
            print(f"  {n:>2}  {rel}")
            if sample:
                print(f"        e.g. {sample}")
    elif cmd == "apply":
        used_ids: set[str] = set()
        counter = [0]
        total_changed = 0
        files_touched = 0
        # Pre-scan to seed used_ids globally
        for p in find_html_files():
            try:
                html = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for m in re.finditer(r"""\bid\s*=\s*["']([^"']*)["']""", html):
                used_ids.add(m.group(1))
        for p in find_html_files():
            n = apply_to_file(p, used_ids, counter)
            if n:
                files_touched += 1
                total_changed += n
                rel = p.relative_to(ROOT).as_posix()
                print(f"  {n:>2}  {rel}")
        print(f"\nsplit {total_changed} images across {files_touched} files")
    else:
        print(f"unknown command {cmd!r}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
