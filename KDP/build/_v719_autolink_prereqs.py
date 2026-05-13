"""9th edition Wave A5 follow-up: auto-link bare chapter/section
mentions inside prerequisite boxes.

Many chapter-index pages have prereq blocks like:
   <li>Chapter 03: Solid grasp of attention mechanisms ...</li>
Where "Chapter 03" is plain text. This script wraps the leading
"Chapter NN" or "Section X.Y" or "Appendix L" or "Module NN" in an
<a href="..."> link to the right index/section page.

Idempotent: only wraps tokens that are NOT already inside an <a>.
Sentinel: the wrapped <a> gets class="prereq-link" so we can spot
auto-linked vs. hand-linked refs.

Scope:
- Acts only inside <div class="prereqs"> or <div class="prerequisites">.
- Only wraps the FIRST occurrence per token per block (to avoid noise).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

PREREQ_BLOCK = re.compile(
    r'(<div\s+class="prereq(?:s|uisites)"[^>]*>)([\s\S]*?)(</div>)',
    re.IGNORECASE)


def build_chapter_map() -> dict[str, str]:
    """Discover Chapter NN -> path/index.html for every module dir."""
    out: dict[str, str] = {}
    # module-NN-foo: NN is the chapter number
    for module_idx in ROOT.glob('part-*/module-*/index.html'):
        m = re.search(r'module-(\d+)-', module_idx.parent.name)
        if not m:
            continue
        n = int(m.group(1))
        # Both "Chapter NN" and "Module NN" map to this path.
        # Use a relative path from any other page; we'll compute it later.
        key = f'{n:02d}'
        out[key] = str(module_idx.relative_to(ROOT)).replace('\\', '/')
    return out


def build_appendix_map() -> dict[str, str]:
    """Appendix A..AA -> path/index.html"""
    out: dict[str, str] = {}
    for app_idx in ROOT.glob('appendices/appendix-*/index.html'):
        # appendix-X-name / appendix-aa-name
        m = re.search(r'appendix-([a-z]+)-', app_idx.parent.name)
        if not m:
            continue
        letter = m.group(1).upper()
        out[letter] = str(app_idx.relative_to(ROOT)).replace('\\', '/')
    return out


def rel_path(from_file: Path, to_path_str: str) -> str:
    """Relative href from from_file to ROOT/to_path_str."""
    depth = len(from_file.parent.relative_to(ROOT).parts)
    return '../' * depth + to_path_str


def main() -> int:
    fix = '--fix' in sys.argv
    chap_map = build_chapter_map()
    app_map = build_appendix_map()

    # Token pattern: "Chapter NN" or "Module NN" or "Appendix L" or
    # "Section X.Y"
    chap_tok = re.compile(
        r'\b(Chapter|Module)\s+(\d{1,2})\b')
    app_tok = re.compile(
        r'\bAppendix\s+([A-Z]{1,3})\b')
    sec_tok = re.compile(
        r'\bSection\s+(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\b')

    n_files = 0
    n_links = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'prereq' not in text:
            continue
        original = text
        local = 0

        def rewrite_block(m: re.Match) -> str:
            nonlocal local
            head, inner, tail = m.group(1), m.group(2), m.group(3)
            # We split the inner into "outside <a>" and "inside <a>" runs
            # so we only touch outside text. Use a token-replacing pass.
            # For each token type, replace ONLY the first occurrence that's
            # outside an <a>.

            def split_by_anchor(s: str) -> list[tuple[str, bool]]:
                # Returns list of (chunk, is_inside_anchor)
                parts: list[tuple[str, bool]] = []
                cur = 0
                for am in re.finditer(r'<a\s[^>]*>[^<]*</a>', s,
                                      flags=re.IGNORECASE):
                    if am.start() > cur:
                        parts.append((s[cur:am.start()], False))
                    parts.append((s[am.start():am.end()], True))
                    cur = am.end()
                if cur < len(s):
                    parts.append((s[cur:], False))
                return parts

            seen_tokens: set[str] = set()

            def replace_tok(text_outside: str, pat: re.Pattern,
                            mk_href) -> str:
                def sub_fn(tm: re.Match) -> str:
                    nonlocal local
                    full = tm.group(0)
                    if full in seen_tokens:
                        return full
                    href = mk_href(tm)
                    if not href:
                        return full
                    seen_tokens.add(full)
                    local += 1
                    return f'<a class="prereq-link" href="{href}">{full}</a>'
                return pat.sub(sub_fn, text_outside)

            def chap_href(tm: re.Match) -> str | None:
                key = tm.group(2).zfill(2)
                tgt = chap_map.get(key)
                if not tgt:
                    return None
                return rel_path(p, tgt)

            def app_href(tm: re.Match) -> str | None:
                letter = tm.group(1).upper()
                tgt = app_map.get(letter)
                if not tgt:
                    return None
                return rel_path(p, tgt)

            def sec_href(tm: re.Match) -> str | None:
                key = tm.group(1)
                # "X.Y" -> chapter X, section file = section-X.Y.html
                # in the module-XX-* directory.
                parts = key.split('.')
                chap_key = parts[0].zfill(2)
                chap_path = chap_map.get(chap_key)
                if not chap_path:
                    return None
                # Replace /index.html with /section-X.Y.html
                # Section labels in this book sometimes use the un-padded
                # form (3.2) in the URL.
                un = '.'.join(p_.lstrip('0') or '0' for p_ in parts)
                section_url = chap_path.rsplit('/', 1)[0] + f'/section-{un}.html'
                # Only emit if the file actually exists.
                if not (ROOT / section_url).exists():
                    return None
                return rel_path(p, section_url)

            new_parts: list[str] = []
            for chunk, inside in split_by_anchor(inner):
                if inside:
                    new_parts.append(chunk)
                else:
                    chunk = replace_tok(chunk, sec_tok, sec_href)
                    chunk = replace_tok(chunk, chap_tok, chap_href)
                    chunk = replace_tok(chunk, app_tok, app_href)
                    new_parts.append(chunk)
            return head + ''.join(new_parts) + tail

        new_text = PREREQ_BLOCK.sub(rewrite_block, text)
        if local:
            n_files += 1
            n_links += local
            if fix and new_text != original:
                p.write_text(new_text, encoding='utf-8')

    print(f'Files touched: {n_files}; prereq autolinks added: {n_links}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
