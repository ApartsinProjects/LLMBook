"""HTML hygiene sweep: small drift fixes book-wide.

Passes (each idempotent, each prints its own count):
  1. Smart-quote -> straight-quote. Book is overwhelmingly straight ASCII
     (~250k straight vs 12 smart book-wide), so smart quotes are the outlier
     and we normalize them away. Prose only; never inside <code>/<pre>/
     <script>/<style>.
  2. Truly-empty <p></p>, <p>&nbsp;</p>, <div></div> removal. Preserves
     <div id="search"></div> (Pagefind mount point) and any div with id=
     (intentional anchor/mount). Operates on raw text.
  3. Double <br><br> -> </p><p> paragraph break (outside <pre>/<code>).
  4. Double-encoded entities: &amp;quot; &amp;lt; &amp;gt; &amp;#39; &amp;nbsp;
     decoded in prose. Skipped inside <pre>/<code> where literal escaped
     output may be intentional.
  5. External-link safety: every <a> with http(s):// href gets
     target="_blank" rel="noopener" added if missing. Idempotent.
  6. (Report only) <img> with empty alt="" or missing alt attribute -
     decorative empty-alts are intentional, missing-alts flagged for review.
  7. Trailing whitespace inside <pre> blocks trimmed line-by-line.
  8. Nested <pre><code><code> flattened (inner <code> removed).
  9. Nested <strong><strong>/<em><em> flattened.

Safe zones: passes 1, 3, 4 operate only on text outside <script>, <style>,
<pre>, <code>. Pass 5 (links) is also safe-zone-aware. Passes 2, 7, 8, 9 work
on the full document text with targeted regex that won't damage inner pre/
code content.

Usage:
    python scripts/_html_hygiene_sweep.py            # dry-run report
    python scripts/_html_hygiene_sweep.py --apply    # write changes
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "vendor", "scripts", "docs", "styles", "tmp_whats_next",
}

# Regex matching script/style/pre/code blocks (with nested-safe non-greedy).
SAFE_ZONE_RE = re.compile(
    r"<(script|style|pre|code)\b[^>]*>.*?</\1>",
    re.DOTALL | re.IGNORECASE,
)


def split_safe(text: str):
    """Split text into list of (kind, segment); kind in {'safe','open'}."""
    parts = []
    pos = 0
    for m in SAFE_ZONE_RE.finditer(text):
        if m.start() > pos:
            parts.append(("open", text[pos:m.start()]))
        parts.append(("safe", m.group(0)))
        pos = m.end()
    if pos < len(text):
        parts.append(("open", text[pos:]))
    return parts


def join_safe(parts):
    return "".join(seg for _, seg in parts)


def iter_html_files(only=None):
    """Yield .html files under ROOT, skipping known-irrelevant trees.

    If `only` is provided, it must be a set of *relative* posix paths;
    only files in that set are yielded.
    """
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        if only is not None and p.relative_to(ROOT).as_posix() not in only:
            continue
        yield p


def _attr_value(attrs, name):
    m = re.search(
        rf"""\b{name}\s*=\s*(?:"([^"]*)"|'([^']*)')""",
        attrs,
        re.IGNORECASE,
    )
    if not m:
        return None
    return m.group(1) if m.group(1) is not None else m.group(2)


# -- Pass 1: smart -> straight quotes -----------------------------------------

SMART_QUOTE_MAP = {
    "“": '"',  # left double "
    "”": '"',  # right double "
    "‘": "'",  # left single '
    "’": "'",  # right single '
}


def pass_smart_quotes(text):
    parts = split_safe(text)
    total = 0
    for i, (kind, seg) in enumerate(parts):
        if kind != "open":
            continue
        n = 0
        new_seg = seg
        for smart, straight in SMART_QUOTE_MAP.items():
            c = new_seg.count(smart)
            if c:
                new_seg = new_seg.replace(smart, straight)
                n += c
        if n:
            parts[i] = ("open", new_seg)
            total += n
    return join_safe(parts), total


# -- Pass 2: empty <p>/<div> --------------------------------------------------
# Operates on raw text (no safe-zone strip), so it only matches *truly* empty
# elements. Preserves <div id="..."> (intentional anchor/mount).

EMPTY_P_RE = re.compile(
    r"<p\b[^>]*>\s*(?:&nbsp;| )?\s*</p>\s*\n?",
    re.IGNORECASE,
)
EMPTY_DIV_RE = re.compile(
    r"<div\b([^>]*)>\s*</div>\s*\n?",
    re.IGNORECASE,
)


def pass_empty_blocks(text):
    n_p = 0
    new_text, n_p = EMPTY_P_RE.subn("", text)

    def div_repl(m):
        attrs = m.group(1)
        # Skip if div carries an id (anchor / mount point like #search)
        if re.search(r"\bid\s*=", attrs, re.IGNORECASE):
            return m.group(0)
        return ""

    # Track count
    n_div = 0
    out = []
    last = 0
    for m in EMPTY_DIV_RE.finditer(new_text):
        replacement = div_repl(m)
        out.append(new_text[last:m.start()])
        out.append(replacement)
        if replacement == "":
            n_div += 1
        last = m.end()
    out.append(new_text[last:])
    new_text = "".join(out)
    return new_text, n_p, n_div


# -- Pass 3: double <br> -> paragraph break -----------------------------------

DOUBLE_BR_RE = re.compile(
    r"<br\s*/?>\s*<br\s*/?>",
    re.IGNORECASE,
)


def pass_double_br(text):
    parts = split_safe(text)
    total = 0
    for i, (kind, seg) in enumerate(parts):
        if kind != "open":
            continue
        new_seg, cnt = DOUBLE_BR_RE.subn("</p>\n<p>", seg)
        if cnt:
            parts[i] = ("open", new_seg)
            total += cnt
    return join_safe(parts), total


# -- Pass 4: double-encoded entities ------------------------------------------

DOUBLE_ENC_MAP = [
    ("&amp;quot;", "&quot;"),
    ("&amp;lt;", "&lt;"),
    ("&amp;gt;", "&gt;"),
    ("&amp;#39;", "&#39;"),
    ("&amp;nbsp;", "&nbsp;"),
]


def pass_double_encoded(text):
    parts = split_safe(text)
    counts = Counter()
    for i, (kind, seg) in enumerate(parts):
        if kind != "open":
            continue
        new_seg = seg
        local = Counter()
        for old, new in DOUBLE_ENC_MAP:
            c = new_seg.count(old)
            if c:
                new_seg = new_seg.replace(old, new)
                local[old] += c
        if local:
            parts[i] = ("open", new_seg)
            counts.update(local)
    return join_safe(parts), counts


# -- Pass 5: external link safety ---------------------------------------------

A_TAG_RE = re.compile(r"<a\b([^>]*)>", re.IGNORECASE)


def pass_external_links(text):
    parts = split_safe(text)
    n_added_target = 0
    n_added_rel = 0
    for i, (kind, seg) in enumerate(parts):
        if kind != "open":
            continue
        out = []
        last = 0
        seg_changed = False
        for m in A_TAG_RE.finditer(seg):
            attrs = m.group(1)
            href = _attr_value(attrs, "href")
            if not href or not (
                href.startswith("http://") or href.startswith("https://")
            ):
                continue
            target = _attr_value(attrs, "target")
            rel = _attr_value(attrs, "rel")
            target_ok = target is not None and "_blank" in target
            rel_ok = rel is not None and "noopener" in rel
            if target_ok and rel_ok:
                continue
            new_attrs = attrs
            if not target_ok:
                if target is None:
                    new_attrs = new_attrs.rstrip() + ' target="_blank"'
                else:
                    new_attrs = re.sub(
                        r"""\btarget\s*=\s*(?:"[^"]*"|'[^']*')""",
                        'target="_blank"',
                        new_attrs,
                        flags=re.IGNORECASE,
                    )
                n_added_target += 1
            if not rel_ok:
                if rel is None:
                    new_attrs = new_attrs.rstrip() + ' rel="noopener"'
                else:
                    new_rel_val = (rel + " noopener").strip()
                    new_attrs = re.sub(
                        r"""\brel\s*=\s*(?:"[^"]*"|'[^']*')""",
                        f'rel="{new_rel_val}"',
                        new_attrs,
                        flags=re.IGNORECASE,
                    )
                n_added_rel += 1
            new_tag = f"<a{new_attrs}>"
            out.append(seg[last:m.start()])
            out.append(new_tag)
            last = m.end()
            seg_changed = True
        if seg_changed:
            out.append(seg[last:])
            parts[i] = ("open", "".join(out))
    return join_safe(parts), n_added_target, n_added_rel


# -- Pass 6: img alt reporting (no fix) ---------------------------------------

IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)


def report_imgs(text):
    no_alt = empty_alt = 0
    for m in IMG_RE.finditer(text):
        tag = m.group(0)
        if not re.search(r"\balt\s*=", tag, re.IGNORECASE):
            no_alt += 1
            continue
        v = _attr_value(tag, "alt")
        if v == "":
            empty_alt += 1
    return no_alt, empty_alt


# -- Pass 7: trailing whitespace in <pre> -------------------------------------

PRE_BLOCK_RE = re.compile(
    r"(<pre\b[^>]*>)(.*?)(</pre>)",
    re.DOTALL | re.IGNORECASE,
)
TRAIL_WS_RE = re.compile(r"[ \t]+$", re.MULTILINE)


def pass_trim_pre(text):
    total_lines = 0

    def repl(m):
        nonlocal total_lines
        open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
        new_body, n = TRAIL_WS_RE.subn("", body)
        total_lines += n
        return open_tag + new_body + close_tag

    new_text = PRE_BLOCK_RE.sub(repl, text)
    return new_text, total_lines


# -- Pass 8: nested <pre><code><code> -----------------------------------------

NESTED_CODE_RE = re.compile(
    r"(<pre\b[^>]*>\s*<code\b[^>]*>)\s*<code\b[^>]*>(.*?)</code>\s*(</code>\s*</pre>)",
    re.DOTALL | re.IGNORECASE,
)


def pass_nested_code(text):
    n = 0

    def repl(m):
        nonlocal n
        n += 1
        return m.group(1) + m.group(2) + m.group(3)

    new_text = NESTED_CODE_RE.sub(repl, text)
    return new_text, n


# -- Pass 9: nested <strong><strong> / <em><em> -------------------------------

NESTED_STRONG_RE = re.compile(
    r"<strong\b([^>]*)>\s*<strong\b([^>]*)>(.*?)</strong>\s*</strong>",
    re.DOTALL | re.IGNORECASE,
)
NESTED_EM_RE = re.compile(
    r"<em\b([^>]*)>\s*<em\b([^>]*)>(.*?)</em>\s*</em>",
    re.DOTALL | re.IGNORECASE,
)


def pass_nested_emphasis(text):
    n_strong = 0
    n_em = 0

    def s_repl(m):
        nonlocal n_strong
        n_strong += 1
        return f"<strong{m.group(1)}>{m.group(3)}</strong>"

    def e_repl(m):
        nonlocal n_em
        n_em += 1
        return f"<em{m.group(1)}>{m.group(3)}</em>"

    new_text = NESTED_STRONG_RE.sub(s_repl, text)
    new_text = NESTED_EM_RE.sub(e_repl, new_text)
    return new_text, n_strong, n_em


# -- main ---------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Write changes (default: dry-run)")
    ap.add_argument("--manifest", metavar="PATH",
                    help="Write list of changed files to PATH (one per line)")
    ap.add_argument("--only", metavar="PATH",
                    help="Restrict to files listed in PATH (one per line, "
                         "posix-relative paths)")
    args = ap.parse_args()
    dry_run = not args.apply
    only = None
    if args.only:
        only = {
            line.strip()
            for line in Path(args.only).read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    totals = Counter()
    files_per_cat: dict[str, set[Path]] = defaultdict(set)
    files_changed = set()
    file_smart_counts = Counter()
    file_pre_ws_counts = Counter()
    file_link_counts = Counter()
    img_files_no_alt = Counter()
    img_files_empty_alt = Counter()

    for p in iter_html_files(only=only):
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text

        text, n_quotes = pass_smart_quotes(text)
        if n_quotes:
            totals["smart_quotes"] += n_quotes
            files_per_cat["smart_quotes"].add(p)
            file_smart_counts[p] = n_quotes

        text, n_p, n_div = pass_empty_blocks(text)
        if n_p:
            totals["empty_p"] += n_p
            files_per_cat["empty_p"].add(p)
        if n_div:
            totals["empty_div"] += n_div
            files_per_cat["empty_div"].add(p)

        text, n_brbr = pass_double_br(text)
        if n_brbr:
            totals["double_br"] += n_brbr
            files_per_cat["double_br"].add(p)

        text, enc_counts = pass_double_encoded(text)
        if enc_counts:
            for k, v in enc_counts.items():
                totals[f"enc_{k}"] += v
            files_per_cat["double_encoded"].add(p)

        text, n_target, n_rel = pass_external_links(text)
        if n_target:
            totals["link_target"] += n_target
        if n_rel:
            totals["link_rel"] += n_rel
        if n_target or n_rel:
            files_per_cat["link_safety"].add(p)
            file_link_counts[p] = max(n_target, n_rel)

        text, n_pre_ws = pass_trim_pre(text)
        if n_pre_ws:
            totals["pre_trailing_ws"] += n_pre_ws
            files_per_cat["pre_trailing_ws"].add(p)
            file_pre_ws_counts[p] = n_pre_ws

        text, n_nested_code = pass_nested_code(text)
        if n_nested_code:
            totals["nested_code"] += n_nested_code
            files_per_cat["nested_code"].add(p)

        text, n_strong, n_em = pass_nested_emphasis(text)
        if n_strong:
            totals["nested_strong"] += n_strong
            files_per_cat["nested_strong"].add(p)
        if n_em:
            totals["nested_em"] += n_em
            files_per_cat["nested_em"].add(p)

        # Report-only: img alt
        n_no_alt, n_empty_alt = report_imgs(text)
        if n_no_alt:
            totals["img_no_alt"] += n_no_alt
            img_files_no_alt[p] = n_no_alt
        if n_empty_alt:
            totals["img_alt_empty"] += n_empty_alt
            img_files_empty_alt[p] = n_empty_alt

        if text != original:
            files_changed.add(p)
            if not dry_run:
                p.write_text(text, encoding="utf-8")

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== HTML hygiene sweep ({mode}) ===\n")
    print("Counts per category (FIX = applied; [REPORT] = no fix):")
    label_map = [
        ("smart_quotes",    "FIX  Smart quotes -> straight"),
        ("empty_p",         "FIX  Empty <p> removed"),
        ("empty_div",       "FIX  Empty <div> removed (id-bearing preserved)"),
        ("double_br",       "FIX  <br><br> -> </p><p>"),
        ("enc_&amp;quot;",  "FIX  &amp;quot; -> &quot;"),
        ("enc_&amp;lt;",    "FIX  &amp;lt; -> &lt;"),
        ("enc_&amp;gt;",    "FIX  &amp;gt; -> &gt;"),
        ("enc_&amp;#39;",   "FIX  &amp;#39; -> &#39;"),
        ("enc_&amp;nbsp;",  "FIX  &amp;nbsp; -> &nbsp;"),
        ("link_target",     'FIX  Added target="_blank" to ext <a>'),
        ("link_rel",        'FIX  Added rel="noopener" to ext <a>'),
        ("pre_trailing_ws", "FIX  <pre> lines: trailing whitespace trimmed"),
        ("nested_code",     "FIX  <pre><code><code> -> <pre><code>"),
        ("nested_strong",   "FIX  Nested <strong><strong> flattened"),
        ("nested_em",       "FIX  Nested <em><em> flattened"),
        ("img_no_alt",      "[REPORT] <img> with no alt attr"),
        ("img_alt_empty",   '[REPORT] <img> with alt="" (decorative)'),
    ]
    for k, lbl in label_map:
        v = totals.get(k, 0)
        if v:
            print(f"  {lbl:55s} {v:>6d}")
    print(f"\nFiles changed: {len(files_changed)}\n")
    print("Files touched per category:")
    for cat in sorted(files_per_cat):
        print(f"  {cat:25s} {len(files_per_cat[cat]):>4d}")
    print()
    # Outlier reports
    if file_smart_counts:
        print("Smart-quote outliers (top 5):")
        for p, n in file_smart_counts.most_common(5):
            print(f"  {n:>3d}  {p.relative_to(ROOT)}")
        print()
    if file_pre_ws_counts:
        print("Trailing-ws <pre> outliers (top 10):")
        for p, n in file_pre_ws_counts.most_common(10):
            print(f"  {n:>4d}  {p.relative_to(ROOT)}")
        print()
    if file_link_counts:
        print("Link-safety outliers (top 10):")
        for p, n in file_link_counts.most_common(10):
            print(f"  {n:>4d}  {p.relative_to(ROOT)}")
        print()
    if img_files_no_alt:
        print(f"[REPORT] <img> missing alt entirely: "
              f"{sum(img_files_no_alt.values())} across "
              f"{len(img_files_no_alt)} files. Top 10:")
        for p, n in img_files_no_alt.most_common(10):
            print(f"  {n:>3d}  {p.relative_to(ROOT)}")
        print()
    if img_files_empty_alt:
        print(f'[REPORT] <img alt=""> (decorative, intentionally left alone): '
              f"{sum(img_files_empty_alt.values())} across "
              f"{len(img_files_empty_alt)} files")
    if args.manifest and files_changed:
        Path(args.manifest).write_text(
            "\n".join(str(p.relative_to(ROOT)) for p in sorted(files_changed)),
            encoding="utf-8",
        )
        print(f"\nManifest written: {args.manifest} ({len(files_changed)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
