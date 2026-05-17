"""Drop the 12 redirect-only appendix stubs (C-N) and rewrite all external refs to their canonical homes.

The stubs have content like:
  This content has moved -> see <a href="../../part-X/module-Y/section-Z.html">...

We:
  1. Parse each stub's <table class="content-moved-table"> to build a mapping
  2. Rewrite every <a href="...appendix-X-.../section-X.Y.html"> to the consolidated target
  3. Rewrite bare ../appendices/appendix-X-... index links to the first consolidated target in that appendix
  4. git rm the stub directories
  5. Remove the stubs from appendices/index.html and toc.html
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REDIRECT_DIRS = [
    'appendix-c-huggingface-ecosystem',
    'appendix-d-langchain',
    'appendix-e-orchestration-frameworks',
    'appendix-f-agent-frameworks',
    'appendix-g-python-for-llm',
    'appendix-h-environment-setup',
    'appendix-i-git-collaboration',
    'appendix-j-experiment-tracking',
    'appendix-k-inference-serving',
    'appendix-l-data-engineering',
    'appendix-m-distributed-ml',
    'appendix-n-mlops',
]

SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
             "temp_epub", "source_fix_backups", "pagefind", "templates",
             ".claude", ".book-update", "vendor", "docs"}


def parse_stub_mappings(stub_dir):
    """Return list of (letter, num, target_path) tuples from the content-moved-table."""
    idx = stub_dir / 'index.html'
    if not idx.exists(): return []
    text = idx.read_text(encoding='utf-8')
    rows = re.findall(
        r'<tr><td><code>section-([a-z])\.(\d+)\.html</code></td>\s*'
        r'<td><a href="\.\./\.\./([^"]+)"[^>]*>([^<]+)</a></td></tr>',
        text
    )
    return rows


def build_mapping():
    """Build dict: old_href (as appears anywhere in book) -> new_href.
    Both index and section-level refs.
    """
    mapping = {}
    for ad_name in REDIRECT_DIRS:
        ad_dir = ROOT / 'appendices' / ad_name
        rows = parse_stub_mappings(ad_dir)
        if not rows:
            print(f'  WARN: no mappings in {ad_name}')
            continue
        # First-target serves as the "appendix landing" replacement
        first_target = rows[0][2]
        # Index-level refs from ANY depth
        mapping[f'appendices/{ad_name}/index.html'] = first_target
        # Section-level refs
        for letter, num, target, _label in rows:
            mapping[f'appendices/{ad_name}/section-{letter}.{num}.html'] = target
    return mapping


def rewrite_external_refs(mapping, dry_run):
    """Walk every HTML file, rewrite any href containing a key to the corresponding value.

    Paths in refs may have various ../ depths. We anchor on the suffix:
      href="<any prefix>appendices/appendix-X-.../section-X.Y.html"
    becomes
      href="<any prefix WITHOUT 'appendices'>/part-X/module-Y/section-Z.html"

    For this to work, we compute relative paths per source file.
    """
    n_files = 0
    n_subs_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP_DIRS: continue
        # skip the stubs themselves
        if p.parts[-2] in REDIRECT_DIRS: continue
        text = p.read_text(encoding='utf-8')
        orig = text

        def replace_href(m):
            full_href = m.group(1)
            for old_suffix, new_target in mapping.items():
                if full_href.endswith(old_suffix):
                    # compute prefix portion (../ or empty)
                    prefix = full_href[:-len(old_suffix)]
                    return f'href="{prefix}{new_target}"'
            return m.group(0)

        text = re.sub(r'href="([^"]+)"', replace_href, text)
        if text != orig:
            n_subs_here = sum(
                1 for old in mapping if old in orig and old not in text
            )
            n_subs_total += n_subs_here
            if not dry_run:
                p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Rewrote refs in {n_files} files (replacements: {n_subs_total})')


def remove_stubs(dry_run):
    """git rm the stub directories."""
    n = 0
    for ad_name in REDIRECT_DIRS:
        ad_dir = ROOT / 'appendices' / ad_name
        if not ad_dir.exists(): continue
        if not dry_run:
            r = subprocess.run(['git', 'rm', '-rf', str(ad_dir)], cwd=ROOT,
                              capture_output=True, text=True)
            if r.returncode != 0:
                print(f'  ERR removing {ad_name}: {r.stderr}')
                continue
        n += 1
    print(f'  Removed {n} redirect-stub directories')


def update_appendix_index(dry_run):
    """Remove the redirect-stub entries from appendices/index.html."""
    idx = ROOT / 'appendices' / 'index.html'
    if not idx.exists(): return
    text = idx.read_text(encoding='utf-8')
    orig = text
    for ad_name in REDIRECT_DIRS:
        # Match list items / blocks referencing the stub
        # Pattern: <li>...<a href="appendix-X-name/...">...</a>...</li>
        text = re.sub(
            rf'<li[^>]*>[\s\S]*?{re.escape(ad_name)}[\s\S]*?</li>\s*',
            '', text
        )
        # Match grid-card / appendix-card divs referencing the stub
        text = re.sub(
            rf'<(?:div|a)[^>]*?{re.escape(ad_name)}[\s\S]*?</(?:div|a)>\s*',
            '', text
        )
    if text != orig and not dry_run:
        idx.write_text(text, encoding='utf-8')
    print(f'  appendices/index.html updated: {orig != text}')


def update_toc(dry_run):
    """Remove redirect-stub entries from toc.html."""
    toc = ROOT / 'toc.html'
    if not toc.exists(): return
    text = toc.read_text(encoding='utf-8')
    orig = text
    for ad_name in REDIRECT_DIRS:
        # toc has <li class="toc-chapter toc-appendix"> (or just toc-chapter)
        text = re.sub(
            rf'<li class="toc-chapter(?:\s+toc-appendix)?">\s*<a href="appendices/{re.escape(ad_name)}/[^"]*">[\s\S]*?</a>\s*</li>\s*',
            '', text
        )
    if text != orig and not dry_run:
        toc.write_text(text, encoding='utf-8')
    print(f'  toc.html updated: {orig != text}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dry_run = not args.apply
    print('=== Drop redirect-only appendix stubs ===')
    if dry_run:
        print('(DRY-RUN; pass --apply)\n')

    print('--- Build mapping ---')
    mapping = build_mapping()
    print(f'  {len(mapping)} old->new path mappings')

    print('\n--- Rewrite external refs ---')
    rewrite_external_refs(mapping, dry_run)

    print('\n--- Update appendix index ---')
    update_appendix_index(dry_run)

    print('\n--- Update toc.html ---')
    update_toc(dry_run)

    print('\n--- Remove stub directories ---')
    remove_stubs(dry_run)

    return 0


if __name__ == '__main__':
    sys.exit(main())
