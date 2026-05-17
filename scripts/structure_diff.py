"""Diff book_structure.yaml (current) vs book_structure.target.yaml (target).

Outputs a migration plan: deletions, merges, splits, moves, new chapters.
This is the FIRST thing a restructure operator runs.
"""
from pathlib import Path
import yaml
import sys

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(p):
    return yaml.safe_load(p.read_text(encoding='utf-8'))


def chapter_slug_set(yam):
    """Return set of module-NN-slug strings for all chapters in a yaml."""
    out = set()
    for part in yam.get('parts', []):
        psl = part.get('slug', '?')
        for ch in part.get('chapters', []):
            out.add(f"part-{part['num']}-{psl}/module-{ch['num']:02d}-{ch['slug']}")
    return out


def chapter_index(yam):
    """Return dict slug -> (part_num, part_title, ch_num, ch_title, action)."""
    out = {}
    for part in yam.get('parts', []):
        for ch in part.get('chapters', []):
            out[ch.get('slug', '?')] = {
                'part': part['num'],
                'part_title': part['title'],
                'ch_num': ch['num'],
                'title': ch['title'],
                'action': ch.get('_action', '?'),
                'source': ch.get('_source'),
                'sources': ch.get('_sources'),
            }
    return out


def main():
    current = load_yaml(ROOT / 'book_structure.yaml')
    target = load_yaml(ROOT / 'book_structure.target.yaml')

    print('=== STRUCTURE DIFF ===\n')
    print(f'  Current: {len(current["parts"])} parts, '
          f'{sum(len(p["chapters"]) for p in current["parts"])} chapters')
    print(f'  Target:  {len(target["parts"])} parts, '
          f'{sum(len(p["chapters"]) for p in target["parts"])} chapters')
    print()

    # Show part-level mapping
    print('=== PART-LEVEL CHANGES ===')
    for p in target['parts']:
        action = p.get('_action', '?')
        n_ch = len(p.get('chapters', []))
        marker = {'unchanged': '   ', 'rename': '-->', 'new_part': '+++', 'move_and_restructure': '<->', 'renumber': '-->'}.get(action, '???')
        print(f'  {marker} Part {p["roman"]:>5s} ({n_ch} ch) {p["title"]}  [{action}]')

    # Show chapter-level actions grouped by action
    print('\n=== CHAPTER-LEVEL ACTIONS ===')
    actions = {}
    for p in target['parts']:
        for ch in p.get('chapters', []):
            a = ch.get('_action', '?')
            actions.setdefault(a, []).append((p['num'], ch))

    for action, items in sorted(actions.items()):
        print(f'\n  [{action}] {len(items)} chapter(s):')
        for part_num, ch in items:
            src_info = ''
            if ch.get('_source'):
                src_info = f'  <-- {ch["_source"]}'
            elif ch.get('_sources'):
                src_info = f'  <-- merge of: {", ".join(ch["_sources"])}'
            elif ch.get('_source_section'):
                src_info = f'  <-- promote from: {ch["_source_section"]}'
            elif ch.get('_source_sections'):
                src_info = f'  <-- sections: {", ".join(ch["_source_sections"])}'
            print(f'    Part {part_num} Ch {ch["num"]:>3d}: {ch["title"]}{src_info}')

    # Summary counts
    print('\n=== SUMMARY ===')
    for action in sorted(actions.keys()):
        print(f'  {action:>30s}: {len(actions[action])} chapter(s)')


if __name__ == '__main__':
    sys.exit(main() or 0)
