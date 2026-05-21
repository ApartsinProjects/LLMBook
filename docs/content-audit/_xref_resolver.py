"""Helper to resolve cross-references for the XREF cycle-4 agent."""
import json
import os

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'

idx = json.load(open(os.path.join(ROOT, 'docs', 'content-audit', '_section_file_index.json')))
sections = idx['sections']
modules = idx['modules']


def resolve_section(source_file_rel, target_section):
    """Given source file (relative to ROOT) and target_section (e.g. '7.5'),
    return (href, verified, actual_target)."""
    actual = target_section
    if actual not in sections:
        for v in ['a', 'b', 'c']:
            if actual + v in sections:
                actual = actual + v
                break
        else:
            return None, False, target_section

    tgt_part, tgt_module, tgt_file = sections[actual]
    src_norm = source_file_rel.replace('\\', '/')
    src_parts = src_norm.split('/')
    if len(src_parts) < 3:
        return None, False, actual
    src_part = src_parts[0]
    src_module = src_parts[1]

    if src_part == tgt_part and src_module == tgt_module:
        href = tgt_file
    elif src_part == tgt_part:
        href = f'../{tgt_module}/{tgt_file}'
    else:
        href = f'../../{tgt_part}/{tgt_module}/{tgt_file}'

    return href, True, actual


def resolve_chapter(source_file_rel, chapter_num):
    """Given source file and chapter number (e.g. '11'), return relative href to index.html."""
    raw = chapter_num
    bare = raw.lstrip('0') or '0'
    zp_key = bare.zfill(2)
    if raw in modules:
        tgt_part, tgt_module = modules[raw]
    elif zp_key in modules:
        tgt_part, tgt_module = modules[zp_key]
    elif bare in modules:
        tgt_part, tgt_module = modules[bare]
    else:
        return None, False

    src_norm = source_file_rel.replace('\\', '/')
    src_parts = src_norm.split('/')
    src_part = src_parts[0]
    src_module = src_parts[1] if len(src_parts) > 1 else None

    if src_part == tgt_part and src_module == tgt_module:
        href = 'index.html'
    elif src_part == tgt_part:
        href = f'../{tgt_module}/index.html'
    else:
        href = f'../../{tgt_part}/{tgt_module}/index.html'
    return href, True


def verify_path_exists(source_file_rel, href):
    """Verify that the href resolves to an existing file."""
    src_dir = os.path.dirname(os.path.join(ROOT, source_file_rel))
    target = os.path.normpath(os.path.join(src_dir, href))
    return os.path.isfile(target)


if __name__ == '__main__':
    test_cases = [
        ('part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html', '7.1'),
        ('part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html', '0.3'),
        ('part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html', '7.5'),
    ]
    for src, tgt in test_cases:
        h, v, a = resolve_section(src, tgt)
        ok = verify_path_exists(src, h) if h else False
        print(f'{src}: Section {tgt} -> href={h}, verified={v}, actual={a}, exists={ok}')

    ch_tests = [
        ('part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3b.html', '06'),
        ('part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.4.html', '20'),
        ('part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html', '11'),
    ]
    for src, ch in ch_tests:
        h, v = resolve_chapter(src, ch)
        ok = verify_path_exists(src, h) if h else False
        print(f'{src}: Chapter {ch} -> href={h}, verified={v}, exists={ok}')
