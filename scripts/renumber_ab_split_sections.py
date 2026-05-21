"""Eliminate every section-N.Ma.html / section-N.Mb.html split file in the book.

After this script runs:
  - section-N.Ma.html  -> section-N.M.html      (no shift)
  - section-N.Mb.html  -> section-N.(M+1).html  (and all higher sections in the
                          same module shift up by 1)

Inside each renamed file the H2 ids and visible subsection numbers ("X.Y.Z")
are rewritten to match the new section, and the "Section X.Ya" page-current
label loses its a/b suffix.

Book-wide we then do a global text pass to update:
  - href="section-N.Ma.html"     -> href="section-N.M.html"
  - href="section-N.Mb.html"     -> href="section-N.(M+1).html"
  - "Section N.Ma" / "Section N.Mb" prose refs -> bare new section labels
  - "Section N.M.K" / "Figure N.M.K" prose refs targeting subsections that
    moved between halves (e.g., 9.1.5 was in 9.1b, becomes 9.2.2)
  - id="N-M-K..." / id="N.M.K..." inside the renamed files

The full operation uses a SINGLE placeholder pass per file so the new value of
one rule cannot match the old-value side of another rule. This is the same
two-pass pattern that fixed the Part 14 renumber cascade bug.

Edge cases handled:
  Module 10  : 10.4.html keeps name, 10.4b.html -> 10.5.html (no 10.4a exists)
  Module 31  : 31.4.html keeps name, 31.4b.html -> 31.5.html (no 31.4a exists)

Run:
  py -3 scripts/renumber_ab_split_sections.py            # dry-run, print map
  py -3 scripts/renumber_ab_split_sections.py --apply    # actually rename + edit
  py -3 scripts/renumber_ab_split_sections.py --module 5 # restrict to one module
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Directories to NOT rewrite (text-replacement skip-list)
SKIP_DIRS = {
    '_archive', 'node_modules', '.git', 'pagefind', 'KDP',
    'build', 'vendor', '.claude', '__pycache__', '.book-update',
}

LETTER_RE = re.compile(r'^section-(\d+)\.(\d+)([ab])\.html$')
PLAIN_RE = re.compile(r'^section-(\d+)\.(\d+)\.html$')


def list_module_sections(mod_dir: Path):
    items = []
    for f in mod_dir.glob('section-*.html'):
        name = f.name
        m = LETTER_RE.match(name)
        if m:
            chap = int(m.group(1))
            sec = int(m.group(2))
            letter = m.group(3)
            items.append(('ab', chap, sec, letter, name))
            continue
        m = PLAIN_RE.match(name)
        if m:
            chap = int(m.group(1))
            sec = int(m.group(2))
            items.append(('plain', chap, sec, None, name))
            continue
    def key(t):
        kind, chap, sec, letter, name = t
        letter_key = 0 if letter is None else (ord(letter) - ord('a') + 1)
        return (sec, letter_key)
    items.sort(key=key)
    return items


def compute_module_plan(items):
    groups = defaultdict(list)
    for item in items:
        groups[item[2]].append(item)
    cursor = None
    plan = []
    for sec_num in sorted(groups.keys()):
        bucket = groups[sec_num]
        kinds_letters = [(it[0], it[3]) for it in bucket]
        if cursor is None:
            base = sec_num
        else:
            base = max(cursor + 1, sec_num)
        has_plain = any(k == 'plain' for k, _ in kinds_letters)
        has_a = any(k == 'ab' and let == 'a' for k, let in kinds_letters)
        has_b = any(k == 'ab' and let == 'b' for k, let in kinds_letters)
        for it in bucket:
            kind, chap, sec, letter, name = it
            if kind == 'plain':
                plan.append((name, base, None))
            elif kind == 'ab' and letter == 'a':
                offset = 1 if has_plain else 0
                plan.append((name, base + offset, 'a'))
            elif kind == 'ab' and letter == 'b':
                offset = 0
                if has_plain:
                    offset += 1
                if has_a:
                    offset += 1
                plan.append((name, base + offset, 'b'))
        slots_used = (1 if has_plain else 0) + (1 if has_a else 0) + (1 if has_b else 0)
        cursor = base + slots_used - 1
    return plan


def all_modules():
    out = []
    for part_dir in ROOT.iterdir():
        if not part_dir.is_dir():
            continue
        if not part_dir.name.startswith('part-'):
            continue
        if part_dir.name.startswith('_'):
            continue
        for mod_dir in part_dir.iterdir():
            if not mod_dir.is_dir():
                continue
            if not mod_dir.name.startswith('module-'):
                continue
            out.append(mod_dir)
    return out


def needs_renumber(mod_dir: Path) -> bool:
    return any(LETTER_RE.match(f.name) for f in mod_dir.glob('section-*.html'))


def build_global_plan(module_filter=None):
    plan = {}
    for mod_dir in all_modules():
        if not needs_renumber(mod_dir):
            continue
        if module_filter is not None:
            m = re.match(r'^module-(\d+)-', mod_dir.name)
            if not m or int(m.group(1)) != module_filter:
                continue
        items = list_module_sections(mod_dir)
        plan[mod_dir] = compute_module_plan(items)
    return plan


def collect_h2_subsection_numbers(text, chap, old_sec):
    h2_re = re.compile(
        rf'<h2[^>]*id="{chap}-{old_sec}-(\d+)(?:-[\w-]+)?"',
    )
    seen = []
    for m in h2_re.finditer(text):
        k = int(m.group(1))
        if k not in seen:
            seen.append(k)
    return seen


def build_global_maps(global_plan):
    """Build the cross-book substitution maps.
    Returns (label_map, file_map, shift_map, sub_remap).
    """
    label_map = {}   # (chap, old_sec, letter) -> new_sec  (for ab files)
    file_map = {}    # (chap, old_sec, letter) -> new_sec  (same data, for file refs)
    shift_map = {}   # (chap, old_sec) -> new_sec          (for plain shifts)
    sub_remap = {}   # (chap, old_sec, letter) -> {k_old: k_new}  (b-half subsections)

    for mod_dir, entries in global_plan.items():
        for old_name, new_sec, letter in entries:
            m = LETTER_RE.match(old_name) or PLAIN_RE.match(old_name)
            if not m:
                continue
            chap = int(m.group(1))
            old_sec = int(m.group(2))
            if letter is None:
                if old_sec != new_sec:
                    shift_map[(chap, old_sec)] = new_sec
            else:
                label_map[(chap, old_sec, letter)] = new_sec
                file_map[(chap, old_sec, letter)] = new_sec
                if letter == 'b':
                    fpath = mod_dir / old_name
                    try:
                        body = fpath.read_text(encoding='utf-8')
                    except Exception:
                        body = ''
                    order = collect_h2_subsection_numbers(body, chap, old_sec)
                    sub_remap[(chap, old_sec, 'b')] = {
                        k_old: k_new for k_new, k_old in enumerate(order, start=1)
                    }
    return label_map, file_map, shift_map, sub_remap


# ===========================================================================
# Single combined substitution pass (file-specific + global) with shared
# placeholders so no rule cascades onto another rule's output.
# ===========================================================================

PLACEHOLDER_PFX = '\x00RN\x01'
PLACEHOLDER_SFX = '\x02'


def process_file(text, file_info, label_map, file_map, shift_map, sub_remap,
                 has_a_for_b=None):
    """Apply both in-file (if file_info given) and global rules to `text`.

    file_info: None for files not being renamed, otherwise a dict:
       {chap, old_sec, letter, new_sec}
    """
    placeholders = {}
    counter = [0]

    def stash(repl: str) -> str:
        idx = counter[0]
        counter[0] += 1
        ph = f'{PLACEHOLDER_PFX}{idx}{PLACEHOLDER_SFX}'
        placeholders[ph] = repl
        return ph

    # ---- File-specific rules (only for renamed files) ----
    if file_info is not None:
        chap = file_info['chap']
        old_sec = file_info['old_sec']
        letter = file_info['letter']  # 'a', 'b', or None for plain-shift
        new_sec = file_info['new_sec']

        # A) page-current label "Section X.Ya/b" or "Section X.Y"
        if letter in ('a', 'b'):
            text = re.sub(
                rf'(<div class="page-current">Section\s+){chap}\.{old_sec}({letter})(</div>)',
                lambda m: stash(f'{m.group(1)}{chap}.{new_sec}{m.group(3)}'),
                text,
            )
        else:
            # plain shift: rewrite the page-current "Section X.OLD"
            text = re.sub(
                rf'(<div class="page-current">Section\s+){chap}\.{old_sec}(</div>)',
                lambda m: stash(f'{m.group(1)}{chap}.{new_sec}{m.group(2)}'),
                text,
            )

        # B) H2/H3 id="C-S-K..." attributes
        if letter == 'b':
            sub_map_local = sub_remap.get((chap, old_sec, 'b'), {})
        else:
            sub_map_local = None  # identity within the same K

        def id_hyphen_sub(m):
            c, s, rest = int(m.group(1)), int(m.group(2)), m.group(3)
            if c != chap or s != old_sec:
                return m.group(0)
            rm = re.match(r'^(\d+)(.*)$', rest)
            if not rm:
                return m.group(0)
            k_old = int(rm.group(1))
            tail = rm.group(2)
            if sub_map_local is not None:
                if k_old not in sub_map_local:
                    return m.group(0)
                k_new = sub_map_local[k_old]
            else:
                k_new = k_old
            return stash(f'id="{chap}-{new_sec}-{k_new}{tail}"')
        text = re.sub(r'\bid="(\d+)-(\d+)-([\w-]+)"', id_hyphen_sub, text)

        def id_dot_sub(m):
            c, s, rest = int(m.group(1)), int(m.group(2)), m.group(3)
            if c != chap or s != old_sec:
                return m.group(0)
            rm = re.match(r'^(\d+)(.*)$', rest)
            if not rm:
                return m.group(0)
            k_old = int(rm.group(1))
            tail = rm.group(2)
            if sub_map_local is not None:
                if k_old not in sub_map_local:
                    return m.group(0)
                k_new = sub_map_local[k_old]
            else:
                k_new = k_old
            return stash(f'id="{chap}.{new_sec}.{k_new}{tail}"')
        text = re.sub(r'\bid="(\d+)\.(\d+)\.([\w.]+)"', id_dot_sub, text)

        # C) Display number "C.S.K" (h2/h3 visible numbering)
        def display_sub(m):
            c, s, rest = int(m.group(1)), int(m.group(2)), m.group(3)
            if c != chap or s != old_sec:
                return m.group(0)
            parts = rest.split('.')
            k_old = int(parts[0])
            if sub_map_local is not None:
                if k_old not in sub_map_local:
                    return m.group(0)
                k_new = sub_map_local[k_old]
            else:
                k_new = k_old
            new_rest = str(k_new)
            if len(parts) > 1:
                new_rest += '.' + '.'.join(parts[1:])
            return stash(f'{chap}.{new_sec}.{new_rest}')
        text = re.sub(
            r'(?<![\d.\-/])(\d+)\.(\d+)\.(\d+(?:\.\d+)*)\b',
            display_sub,
            text,
        )

        # D) "Section X.Ya/b" or "Section X.OLD" labels (file-local only).
        if letter in ('a', 'b'):
            text = re.sub(
                rf'\bSection\s+{chap}\.{old_sec}{letter}\b',
                lambda m: stash(f'Section {chap}.{new_sec}'),
                text,
            )
        else:
            text = re.sub(
                rf'\bSection\s+{chap}\.{old_sec}\b(?![\d.])',
                lambda m: stash(f'Section {chap}.{new_sec}'),
                text,
            )

        # E) Own filename in chapter-nav (self-link, e.g., section-5.2a.html)
        if letter in ('a', 'b'):
            text = re.sub(
                rf'\bsection-{chap}\.{old_sec}{letter}\.html\b',
                lambda m: stash(f'section-{chap}.{new_sec}.html'),
                text,
            )

    # ---- Global rules (applied to ALL files, including renamed ones) ----

    # 1) Cross-file ab filename references
    def file_ab_sub(m):
        c = int(m.group(1))
        s = int(m.group(2))
        let = m.group(3)
        ns = file_map.get((c, s, let))
        if ns is None:
            return m.group(0)
        return stash(f'section-{c}.{ns}.html')
    text = re.sub(r'\bsection-(\d+)\.(\d+)([ab])\.html\b', file_ab_sub, text)

    # 2) "Section X.Ya" / "Section X.Yb" prose labels (cross-file)
    def label_ab_sub(m):
        prefix = m.group(1)
        c = int(m.group(2))
        s = int(m.group(3))
        let = m.group(4)
        ns = label_map.get((c, s, let))
        if ns is None:
            return m.group(0)
        return stash(f'{prefix}{c}.{ns}')
    text = re.sub(
        r'\b(Section\s+|section\s+|Sections\s+|sections\s+|see\s+|See\s+|in\s+)(\d+)\.(\d+)([ab])\b',
        label_ab_sub,
        text,
    )

    # 2b) Bare "X.Ya" / "X.Yb" without any prefix (chapter index cards, etc.)
    def bare_ab_sub(m):
        c = int(m.group(1))
        s = int(m.group(2))
        let = m.group(3)
        ns = label_map.get((c, s, let))
        if ns is None:
            return m.group(0)
        return stash(f'{c}.{ns}')
    text = re.sub(r'\b(\d+)\.(\d+)([ab])\b', bare_ab_sub, text)

    # 3) Subsection refs "X.Y.Z" / "X.Y.Z.W" — b-half remap + plain-shift remap.
    def subref_sub(m):
        c = int(m.group(1))
        s = int(m.group(2))
        rest = m.group(3)
        parts = rest.split('.')
        k_old = int(parts[0])
        # If this is the file being renamed, skip — the file-specific pass
        # already handled it via display_sub (or chose not to).
        if file_info is not None and c == file_info['chap'] and s == file_info['old_sec']:
            return m.group(0)
        # Was this a b-half subsection that got remapped?
        b_map = sub_remap.get((c, s, 'b'))
        if b_map and k_old in b_map:
            ns = label_map[(c, s, 'b')]
            new_k = b_map[k_old]
            new_rest = '.'.join([str(new_k)] + parts[1:])
            return stash(f'{c}.{ns}.{new_rest}')
        # Plain-shifted section
        if (c, s) in shift_map:
            ns = shift_map[(c, s)]
            return stash(f'{c}.{ns}.{rest}')
        # a-half section whose number changed (a may shift if there was a
        # plain at same sec, but that's an unusual case we don't currently hit)
        if (c, s, 'a') in label_map:
            ns = label_map[(c, s, 'a')]
            if ns != s:
                return stash(f'{c}.{ns}.{rest}')
        return m.group(0)

    text = re.sub(
        r'(?<![\d.\-/])(\d+)\.(\d+)\.(\d+(?:\.\d+)*)\b',
        subref_sub,
        text,
    )

    # 4) Plain-shifted "Section X.OLD" labels (cross-file).
    def plain_label_sub(m):
        prefix = m.group(1)
        c = int(m.group(2))
        s = int(m.group(3))
        trailing = m.group(4)
        # Skip if this references the file's own old_sec (handled file-locally)
        if file_info is not None and c == file_info['chap'] and s == file_info['old_sec']:
            return m.group(0)
        ns = shift_map.get((c, s))
        if ns is None:
            return m.group(0)
        return stash(f'{prefix}{c}.{ns}') + trailing

    text = re.sub(
        r'\b(Section\s+|section\s+|Sections\s+|sections\s+|Figure\s+|figure\s+|Figures\s+|Table\s+|Tables\s+|Algorithm\s+|Lab\s+|see\s+|See\s+|in\s+)(\d+)\.(\d+)([^a-zA-Z0-9.]|$)',
        plain_label_sub,
        text,
    )

    # 4b) Bare "X.Y" inside `<span class="section-num">X.Y</span>` (chapter index
    #     cards). Plain-shifted version (no letter).
    def span_secnum_sub(m):
        prefix = m.group(1)
        c = int(m.group(2))
        s = int(m.group(3))
        suffix = m.group(4)
        if file_info is not None and c == file_info['chap'] and s == file_info['old_sec']:
            return m.group(0)
        ns = shift_map.get((c, s))
        if ns is None:
            return m.group(0)
        return stash(f'{prefix}{c}.{ns}{suffix}')
    text = re.sub(
        r'(<span class="section-num">)(\d+)\.(\d+)(</span>)',
        span_secnum_sub,
        text,
    )

    # 5) Plain-shifted filename refs: section-X.OLD.html -> section-X.NEW.html
    def plain_file_sub(m):
        c = int(m.group(1))
        s = int(m.group(2))
        if file_info is not None and c == file_info['chap'] and s == file_info['old_sec']:
            return m.group(0)
        ns = shift_map.get((c, s))
        if ns is None:
            return m.group(0)
        return stash(f'section-{c}.{ns}.html')
    text = re.sub(r'\bsection-(\d+)\.(\d+)\.html\b', plain_file_sub, text)

    # ---- Resolve placeholders (single pass at the end) ----
    for ph, repl in placeholders.items():
        text = text.replace(ph, repl)
    return text


# ===========================================================================

def walk_text_files():
    for path in ROOT.rglob('*.html'):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        yield path
    for path in (ROOT / 'docs').rglob('*'):
        if not path.is_file():
            continue
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        if path.suffix not in ('.md', '.json'):
            continue
        yield path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--module', type=int, default=None)
    ap.add_argument('--show-files', action='store_true')
    args = ap.parse_args()

    print(f"{'APPLY MODE' if args.apply else 'DRY RUN'}")
    if args.module is not None:
        print(f"  (restricted to module/chapter {args.module})")
    print()

    plan = build_global_plan(module_filter=args.module)
    print("=== Step 1: per-module rename plan ===")
    total_renames = 0
    for mod_dir, entries in plan.items():
        rel = mod_dir.relative_to(ROOT)
        print(f"\n[{rel}]")
        for old_name, new_sec, letter in entries:
            m = LETTER_RE.match(old_name) or PLAIN_RE.match(old_name)
            chap = int(m.group(1))
            new_name = f'section-{chap}.{new_sec}.html'
            tag = ''
            if old_name == new_name:
                tag = '  (no change)'
            else:
                total_renames += 1
            print(f"  {old_name}  ->  {new_name}{tag}")
    print(f"\nTotal file renames: {total_renames}")

    label_map, file_map, shift_map, sub_remap = build_global_maps(plan)
    print(f"\n=== Step 2: substitution maps ===")
    print(f"  ab-label entries: {len(label_map)}")
    print(f"  plain-shift entries: {len(shift_map)}")
    print(f"  b-half subsection remaps: {sum(len(v) for v in sub_remap.values())}")
    if args.show_files:
        print('\n  Plain shifts:')
        for key, val in sorted(shift_map.items()):
            print(f'    section-{key[0]}.{key[1]}.html -> section-{key[0]}.{val}.html')
        print('\n  b-half subsection remaps:')
        for key, val in sorted(sub_remap.items()):
            print(f'    {key}: {val}')

    # Build pending_writes for renamed files
    print(f"\n=== Step 3: rewriting renamed files (in-file + global pass) ===")
    pending_writes = []
    for mod_dir, entries in plan.items():
        for old_name, new_sec, letter in entries:
            m = LETTER_RE.match(old_name) or PLAIN_RE.match(old_name)
            chap = int(m.group(1))
            old_sec = int(m.group(2))
            old_path = mod_dir / old_name
            new_name = f'section-{chap}.{new_sec}.html'
            new_path = mod_dir / new_name
            if old_path == new_path:
                continue
            try:
                body = old_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"  ! cannot read {old_path}: {e}")
                continue
            file_info = {
                'chap': chap,
                'old_sec': old_sec,
                'letter': letter,
                'new_sec': new_sec,
            }
            new_body = process_file(
                body, file_info, label_map, file_map, shift_map, sub_remap
            )
            pending_writes.append((old_path, new_path, new_body))
    print(f"  files staged: {len(pending_writes)}")

    # Global pass for other files
    print(f"\n=== Step 4: global text rewrites on remaining files ===")
    renamed_olds = {p[0] for p in pending_writes}
    global_pending = []
    for path in walk_text_files():
        if path in renamed_olds:
            continue
        try:
            body = path.read_text(encoding='utf-8')
        except Exception:
            continue
        new_body = process_file(
            body, None, label_map, file_map, shift_map, sub_remap
        )
        if new_body != body:
            global_pending.append((path, new_body))
    print(f"  files changed: {len(global_pending)}")
    if args.show_files:
        for p, _ in global_pending[:40]:
            print(f"    {p.relative_to(ROOT)}")
        if len(global_pending) > 40:
            print(f"    ... and {len(global_pending) - 40} more")

    if args.apply:
        print(f"\n=== Step 5: applying changes ===")
        # 1) Write new files (under their NEW name)
        for old_path, new_path, new_body in pending_writes:
            new_path.write_text(new_body, encoding='utf-8')
        # 2) Delete originals — BUT only if no other rename targets that path
        # as its new_path. Otherwise we'd delete a file we just wrote.
        new_paths_set = {p[1] for p in pending_writes}
        for old_path, new_path, _ in pending_writes:
            if old_path == new_path:
                continue
            if old_path in new_paths_set:
                continue  # another rename wrote here, do NOT delete
            if old_path.exists():
                old_path.unlink()
        # 3) Write the other affected files
        for path, new_body in global_pending:
            path.write_text(new_body, encoding='utf-8')
        print(f"  Wrote {len(pending_writes)} renamed files")
        print(f"  Updated {len(global_pending)} other files")
        print(f"\nDone. Re-run audit + rebuild pagefind next.")
    else:
        print(f"\n(dry-run; pass --apply to commit)")


if __name__ == '__main__':
    main()
