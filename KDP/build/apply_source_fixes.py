"""
Apply source-HTML fixes for issues that surface in the EPUB.

CRITICAL: Uses targeted regex-based substitution (NOT BeautifulSoup
round-trip) to preserve source HTML formatting. BeautifulSoup
re-serialization changes capitalization, attribute order, indentation,
and self-closing style across the entire file - even where logic intends
to touch only a few elements. The regex approach only modifies the
matched substrings, leaving everything else untouched byte-for-byte.

Per the policy "when finding a problem in the EPUB, if it also exists in
the source HTML, fix it in source", this script applies four fixes that
improve both EPUB rendering AND static (no-JS) viewing of source HTML:

  1. PYGMENTS-PRETOKENIZE
     Pre-tokenize <pre><code class="language-X">...</code></pre> blocks
     with Pygments. Replaces 'language-X' class with 'lang-X
     pygments-highlighted' so Prism.js (loaded in source) won't try to
     re-tokenize at runtime. Preserves any HTML-like text inside string
     literals (e.g. f"<pre>{x}</pre>" survives as &lt;pre&gt; in output).

  2. AVATAR-DIMENSIONS
     Add width/height attributes to <img> tags inside .agent-avatar-inline,
     .agent-avatar-large, .agent-avatar, .agent-card-avatar wrappers.

  3. URL-BRACES
     Replace illegal { and } chars in id attributes and url(...) refs.
     Surgical regex - only the bad characters in attribute values change.

  4. DUPLICATE-SVG-IDS
     Within each file, dedupe element ids that collide. Uses BS for the
     6 affected files since the rename logic needs to walk SVG ancestor
     scope and rewrite local references (regex too fragile here).

Usage:
    python KDP/build/apply_source_fixes.py            # apply all
    python KDP/build/apply_source_fixes.py --dry-run
    python KDP/build/apply_source_fixes.py --only avatar-dimensions
    python KDP/build/apply_source_fixes.py --skip pygments-pretokenize

Each fix is idempotent.

Backups: per-fix backups go to
KDP/build/source_fix_backups/<run-timestamp>/<original-path>.bak
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import time
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKUP_ROOT = PROJECT_ROOT / "KDP" / "build" / "source_fix_backups"

_LANG_ALIASES = {
    "language-python": "python", "language-py": "python",
    "language-bash": "bash", "language-sh": "bash", "language-shell": "bash",
    "language-js": "javascript", "language-javascript": "javascript",
    "language-ts": "typescript", "language-typescript": "typescript",
    "language-json": "json",
    "language-yaml": "yaml", "language-yml": "yaml",
    "language-toml": "toml",
    "language-html": "html", "language-xml": "xml",
    "language-css": "css",
    "language-c": "c", "language-cpp": "cpp", "language-c++": "cpp",
    "language-rust": "rust", "language-go": "go",
    "language-sql": "sql",
    "language-dockerfile": "dockerfile", "language-makefile": "makefile",
    "language-text": "text", "language-plain": "text",
    "language-diff": "diff",
    "language-md": "markdown", "language-markdown": "markdown",
    "language-r": "r", "language-julia": "julia",
}

AVATAR_SIZES = {
    "agent-avatar-inline": 28,
    "agent-avatar-large":  80,
    "agent-avatar":        80,
    "agent-card-avatar":   52,
}

INVALID_URL_CHARS = re.compile(r"[{}^\\\[\]`]")


# --------------------------------------------------------------------- helpers

def all_html_files() -> list[Path]:
    files: list[Path] = []
    for p in PROJECT_ROOT.rglob("*.html"):
        rel = p.relative_to(PROJECT_ROOT)
        if rel.parts and rel.parts[0] in {"KDP", "scripts", "vendor", "templates", "md", "node_modules"}:
            continue
        files.append(p)
    return files


def make_backup(file: Path, run_dir: Path) -> Path:
    rel = file.relative_to(PROJECT_ROOT)
    target = run_dir / rel.with_suffix(rel.suffix + ".bak")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, target)
    return target


# --------------------------------------------------------------------- Fix 1: Pygments (regex-based)

# Match a complete <pre><code ...class="...language-X..."...>BODY</code></pre> block.
# Uses non-greedy DOTALL match for BODY.
_PYGMENTS_BLOCK_RE = re.compile(
    r'(<pre[^>]*>)(<code\b([^>]*?))class="([^"]*)"([^>]*?>)(.*?)(</code></pre>)',
    re.DOTALL,
)


def fix_pygments_pretokenize(files: list[Path], run_dir: Path, dry_run: bool) -> dict:
    try:
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers import get_lexer_by_name
        from pygments.util import ClassNotFound
    except ImportError:
        print("  ERROR: pygments not installed. pip install pygments")
        return {"changed_files": 0, "blocks_tokenized": 0}

    formatter = HtmlFormatter(nowrap=True, classprefix="")

    n_changed_files = 0
    n_blocks = 0
    n_skipped_already = 0
    file_block_counts: dict[str, int] = {}

    for file in files:
        text = file.read_text(encoding="utf-8")
        if "<pre" not in text or "language-" not in text:
            continue

        local_count = 0

        def replace(m):
            nonlocal n_blocks, n_skipped_already, local_count
            pre_open = m.group(1)
            code_pre_class = m.group(2)
            code_pre_attrs = m.group(3)
            classes = m.group(4)
            code_post_attrs = m.group(5)
            body = m.group(6)
            code_close = m.group(7)

            # Skip if already pygments-highlighted
            if "pygments-highlighted" in classes:
                n_skipped_already += 1
                return m.group(0)

            # Find a recognized language-X class
            class_tokens = classes.split()
            lang_class = None
            lang = None
            for tok in class_tokens:
                if tok in _LANG_ALIASES:
                    lang_class = tok
                    lang = _LANG_ALIASES[tok]
                    break
                elif tok.startswith("language-"):
                    trial = tok[len("language-"):]
                    try:
                        get_lexer_by_name(trial)
                        lang_class = tok
                        lang = trial
                        break
                    except ClassNotFound:
                        continue
            if not lang:
                return m.group(0)

            # Decode HTML entities in body to recover original code text.
            # Pygments will re-escape HTML chars in its output.
            decoded = unescape(body).strip("\n")
            try:
                lexer = get_lexer_by_name(lang)
                highlighted = highlight(decoded, lexer, formatter).rstrip("\n")
            except Exception:
                return m.group(0)

            # Replace the language-X token in classes with "lang-X pygments-highlighted"
            new_classes_tokens = []
            replaced = False
            for tok in class_tokens:
                if tok == lang_class:
                    if not replaced:
                        new_classes_tokens.append(f"lang-{lang}")
                        new_classes_tokens.append("pygments-highlighted")
                        replaced = True
                else:
                    new_classes_tokens.append(tok)
            new_classes = " ".join(new_classes_tokens)

            local_count += 1
            n_blocks += 1
            return (
                f'{pre_open}{code_pre_class}{code_pre_attrs}'
                f'class="{new_classes}"{code_post_attrs}'
                f'{highlighted}{code_close}'
            )

        new_text = _PYGMENTS_BLOCK_RE.sub(replace, text)

        if local_count > 0 and new_text != text:
            n_changed_files += 1
            file_block_counts[str(file.relative_to(PROJECT_ROOT))] = local_count
            if not dry_run:
                make_backup(file, run_dir)
                file.write_text(new_text, encoding="utf-8")

    # Print summary lines for the most-changed files
    if file_block_counts:
        top = sorted(file_block_counts.items(), key=lambda kv: -kv[1])[:8]
        for path, n in top:
            print(f"  [pygments] {path}: {n} blocks")
        print(f"  [pygments] ... and {max(0, len(file_block_counts) - 8)} more files")

    return {
        "changed_files": n_changed_files,
        "blocks_tokenized": n_blocks,
        "skipped_already_highlighted": n_skipped_already,
    }


# --------------------------------------------------------------------- Fix 2: Avatar dimensions (regex-based)

def fix_avatar_dimensions(files: list[Path], run_dir: Path, dry_run: bool) -> dict:
    n_changed_files = 0
    n_imgs = 0

    # Build one regex per wrapper class. Match: opening wrapper tag,
    # optional whitespace, <img>, then optional whitespace, close.
    # Captures the img's existing attributes so we can extend them.
    patterns = {}
    for cls, size in AVATAR_SIZES.items():
        pat = re.compile(
            r'(<(?:span|div)\s+(?:[^>]*\s+)?class="[^"]*\b'
            + re.escape(cls)
            + r'\b[^"]*"[^>]*>)(\s*)(<img\b)([^>]*?)(/?\s*>)',
            re.IGNORECASE,
        )
        patterns[cls] = (pat, size)

    for file in files:
        text = file.read_text(encoding="utf-8")
        if not any(cls in text for cls in AVATAR_SIZES):
            continue

        original = text
        local_imgs = 0

        for cls, (pat, size) in patterns.items():
            def replace(m):
                nonlocal local_imgs, n_imgs
                wrap_open = m.group(1)
                gap = m.group(2)
                img_open = m.group(3)
                img_attrs = m.group(4)
                img_close = m.group(5)
                # Skip if already has both width and height
                has_w = re.search(r"\bwidth\s*=", img_attrs, re.IGNORECASE)
                has_h = re.search(r"\bheight\s*=", img_attrs, re.IGNORECASE)
                if has_w and has_h:
                    return m.group(0)
                inject = ""
                if not has_w:
                    inject += f' width="{size}"'
                if not has_h:
                    inject += f' height="{size}"'
                local_imgs += 1
                n_imgs += 1
                return f"{wrap_open}{gap}{img_open}{img_attrs}{inject}{img_close}"

            text = pat.sub(replace, text)

        if local_imgs > 0 and text != original:
            n_changed_files += 1
            if not dry_run:
                make_backup(file, run_dir)
                file.write_text(text, encoding="utf-8")

    print(f"  [avatar-dimensions] modified {n_changed_files} files, {n_imgs} <img> tags")

    return {"changed_files": n_changed_files, "imgs_updated": n_imgs}


# --------------------------------------------------------------------- Fix 3: URL braces (regex-based)

def fix_url_braces(files: list[Path], run_dir: Path, dry_run: bool) -> dict:
    n_changed_files = 0
    n_replacements = 0

    # Replace { and } only inside id="..." attributes and url(#...) values.
    id_attr_re = re.compile(r'\bid="([^"]*[{}^\\\[\]`][^"]*)"')
    url_re = re.compile(r'url\(#([^)]*[{}^\\\[\]`][^)]*)\)')
    href_frag_re = re.compile(r'(\bhref="#)([^"]*[{}^\\\[\]`][^"]*)(")')

    for file in files:
        text = file.read_text(encoding="utf-8")
        if not INVALID_URL_CHARS.search(text):
            continue

        original = text
        local = 0

        def clean_id(m):
            nonlocal local
            local += 1
            return f'id="{INVALID_URL_CHARS.sub("_", m.group(1))}"'
        text = id_attr_re.sub(clean_id, text)

        def clean_url(m):
            nonlocal local
            local += 1
            return f'url(#{INVALID_URL_CHARS.sub("_", m.group(1))})'
        text = url_re.sub(clean_url, text)

        def clean_href(m):
            nonlocal local
            local += 1
            return f'{m.group(1)}{INVALID_URL_CHARS.sub("_", m.group(2))}{m.group(3)}'
        text = href_frag_re.sub(clean_href, text)

        if local > 0 and text != original:
            n_changed_files += 1
            n_replacements += local
            if not dry_run:
                make_backup(file, run_dir)
                file.write_text(text, encoding="utf-8")
            print(f"  [url-braces] {file.relative_to(PROJECT_ROOT)}: {local} fixed")

    return {"changed_files": n_changed_files, "replacements": n_replacements}


# --------------------------------------------------------------------- Fix 4: Duplicate SVG IDs (BS-based, surgical)

def fix_duplicate_svg_ids(files: list[Path], run_dir: Path, dry_run: bool) -> dict:
    """Use BeautifulSoup ONLY for the few files with duplicate IDs.
    Document-wide ID rewriting is too tricky for regex.
    """
    from bs4 import BeautifulSoup

    n_changed_files = 0
    n_renames = 0

    for file in files:
        text = file.read_text(encoding="utf-8")
        # Quick pre-check: only run BS if the file has multiple id="" attributes
        ids = re.findall(r'\bid="([^"]+)"', text)
        if len(ids) == len(set(ids)):
            continue  # no duplicates

        soup = BeautifulSoup(text, "lxml")
        seen: dict[str, int] = {}
        renames: list[tuple] = []
        for el in soup.find_all(attrs={"id": True}):
            old_id = el["id"]
            if not old_id:
                continue
            if old_id not in seen:
                seen[old_id] = 1
                continue
            n = seen[old_id]
            new_id = f"{old_id}_d{n}"
            while new_id in seen:
                n += 1
                new_id = f"{old_id}_d{n}"
            seen[old_id] = n + 1
            seen[new_id] = 1
            renames.append((el, old_id, new_id))

        if not renames:
            continue

        for el, old_id, new_id in renames:
            scope = el
            while scope.parent is not None and scope.name != "svg":
                scope = scope.parent
            if scope.name != "svg":
                scope = soup
            el["id"] = new_id
            for ref_el in scope.find_all(True):
                for attr_name in list(ref_el.attrs):
                    val = ref_el.attrs[attr_name]
                    if not isinstance(val, str):
                        continue
                    if f"url(#{old_id})" in val:
                        ref_el.attrs[attr_name] = val.replace(
                            f"url(#{old_id})", f"url(#{new_id})"
                        )
                    elif val == f"#{old_id}":
                        ref_el.attrs[attr_name] = f"#{new_id}"
            n_renames += 1

        n_changed_files += 1
        if not dry_run:
            make_backup(file, run_dir)
            file.write_text(str(soup), encoding="utf-8")
        print(f"  [duplicate-ids] {file.relative_to(PROJECT_ROOT)}: {len(renames)} renamed (BS reformat applied)")

    return {"changed_files": n_changed_files, "ids_renamed": n_renames}


# --------------------------------------------------------------------- main

FIXES = {
    "pygments-pretokenize": fix_pygments_pretokenize,
    "avatar-dimensions": fix_avatar_dimensions,
    "url-braces": fix_url_braces,
    "duplicate-svg-ids": fix_duplicate_svg_ids,
}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--only", action="append", choices=list(FIXES))
    p.add_argument("--skip", action="append", choices=list(FIXES), default=[])
    args = p.parse_args(argv)

    files = all_html_files()
    print(f"Source HTML files in scope: {len(files)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'APPLY'}")

    run_dir = BACKUP_ROOT / datetime.now().strftime("%Y%m%d-%H%M%S")
    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)
        print(f"Backup root: {run_dir.relative_to(PROJECT_ROOT)}")

    only = set(args.only or FIXES.keys())
    skip = set(args.skip)
    selected = [name for name in FIXES if name in only and name not in skip]
    print(f"Fixes to run: {selected}\n")

    summary: dict[str, dict] = {}
    for name in selected:
        print(f"=== {name} ===")
        t0 = time.time()
        result = FIXES[name](files, run_dir, args.dry_run)
        elapsed = time.time() - t0
        summary[name] = {**result, "elapsed_s": round(elapsed, 1)}
        print(f"  done in {elapsed:.1f}s: {result}\n")

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, result in summary.items():
        print(f"{name:30s} {result}")
    if not args.dry_run and any(r.get("changed_files", 0) for r in summary.values()):
        print(f"\nBackups in: {run_dir.relative_to(PROJECT_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
