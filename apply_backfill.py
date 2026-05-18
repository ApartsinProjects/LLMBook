"""Apply structural backfill to all flagged sections.

For each section in CONTENT, insert any missing epigraph, big-picture, prereqs
block, placed in the canonical order at the top of <main>.

Canonical order (top to bottom):
  pagefind-meta-injected spans
  <blockquote class="epigraph">
  <div class="callout big-picture">
  <div class="prerequisites">
  ... first h2 ...

Behavior:
- Skip blocks that already exist in the file.
- No em-dashes are introduced; CONTENT was authored without them.
- Anchor: insert immediately after the closing of the last pagefind-meta-injected span,
  or, if absent, immediately after <main class="content" id="main-content">.

Run from repo root.
"""
import re
import os
import sys
from backfill_content import CONTENT, AGENT_COLORS


def has_epigraph(html):
    return '<blockquote class="epigraph">' in html


def has_big_picture(html):
    return 'callout big-picture' in html


def has_prereq(html):
    return 'class="prerequisites"' in html or 'id="prerequisites"' in html


def epigraph_block(quote, agent, persona, avatar):
    color = AGENT_COLORS.get(avatar, '#3498db')
    return (
        '<blockquote class="epigraph">\n'
        f'<p>"{quote}"</p>\n'
        f'<span class="agent-avatar-inline" style="background-color: {color};">'
        f'<img alt="{agent}" height="28" src="../../front-matter/images/agents/{avatar}.png" width="28"/></span>'
        f'<cite>{agent}, <span class="agent-desc">{persona} AI Agent</span></cite>\n'
        '</blockquote>\n'
    )


def big_picture_block(html_text):
    return (
        '<div class="callout big-picture">\n'
        '<div class="callout-title">Big Picture</div>\n'
        f'<p>{html_text}</p>\n'
        '</div>\n'
    )


def prereq_block(html_text):
    return (
        '<div class="prerequisites">\n'
        '<h3 id="prerequisites">Prerequisites</h3>\n'
        f'<p>{html_text}</p>\n'
        '</div>\n'
    )


def find_after_pagefind(html):
    """End-of-pagefind-meta-injected, or end of <main> opening tag."""
    pf = list(re.finditer(r'<span class="pagefind-meta-injected"[^>]*></span>', html))
    if pf:
        return pf[-1].end()
    main_m = re.search(r'<main\b[^>]*>', html)
    if main_m:
        return main_m.end()
    raise ValueError("could not find <main> tag")


def find_after_epigraph(html):
    """End of an existing epigraph block, or after pagefind if none."""
    ep_match = re.search(r'</blockquote>', html)
    # only count epigraph blockquotes (need to verify it has class="epigraph")
    for m in re.finditer(r'<blockquote class="epigraph">.*?</blockquote>', html, re.DOTALL):
        return m.end()
    return find_after_pagefind(html)


def find_after_big_picture(html):
    """End of an existing big-picture callout, or wherever epigraph ends."""
    for m in re.finditer(r'<div class="callout big-picture">.*?</div>\s*</div>', html, re.DOTALL):
        # Greedy needed: the callout has a nested div, so match the second close
        pass
    bp = re.search(r'<div class="callout big-picture">', html)
    if bp:
        # Find matching closing </div> at depth 1
        i = bp.end()
        depth = 1
        while i < len(html) and depth > 0:
            next_open = html.find('<div', i)
            next_close = html.find('</div>', i)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                i = next_open + 4
            else:
                depth -= 1
                i = next_close + 6
        return i
    return find_after_epigraph(html)


def apply_to_file(filepath, sectiondata):
    """Apply backfill content to a single file.

    Each missing block is inserted at its canonical position (epigraph right after
    pagefind, big-picture right after the (possibly newly inserted) epigraph, and
    prereqs right after the (possibly newly inserted) big-picture). We insert in
    canonical-order (top-down), re-reading the html between inserts so that
    subsequent anchors find the most recent block.

    Returns (count_added_epigraph, count_added_big, count_added_pre).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    added_ep, added_bp, added_pr = 0, 0, 0

    # Step 1: insert epigraph after pagefind-meta-injected, if needed
    if 'epigraph' in sectiondata and not has_epigraph(html):
        e = sectiondata['epigraph']
        block = epigraph_block(e['quote'], e['agent'], e['persona'], e['avatar'])
        anchor = find_after_pagefind(html)
        html = html[:anchor] + '\n' + block + html[anchor:]
        added_ep = 1

    # Step 2: insert big-picture right after epigraph (or pagefind if no epigraph)
    if 'big_picture' in sectiondata and not has_big_picture(html):
        block = big_picture_block(sectiondata['big_picture'])
        anchor = find_after_epigraph(html)
        html = html[:anchor] + '\n' + block + html[anchor:]
        added_bp = 1

    # Step 3: insert prereqs right after big-picture (or epigraph or pagefind)
    if 'prereq' in sectiondata and not has_prereq(html):
        block = prereq_block(sectiondata['prereq'])
        anchor = find_after_big_picture(html)
        html = html[:anchor] + '\n' + block + html[anchor:]
        added_pr = 1

    if added_ep == 0 and added_bp == 0 and added_pr == 0:
        return 0, 0, 0

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(html)

    return added_ep, added_bp, added_pr


def main():
    cwd = os.getcwd()
    total_ep = total_bp = total_pr = 0
    file_count = 0
    skipped_files = 0
    missing = []

    for relpath, data in CONTENT.items():
        # CONTENT uses forward slashes; convert to OS path
        full = os.path.join(cwd, *relpath.split('/'))
        if not os.path.exists(full):
            missing.append(relpath)
            continue
        ep, bp, pr = apply_to_file(full, data)
        if ep or bp or pr:
            file_count += 1
            total_ep += ep
            total_bp += bp
            total_pr += pr
        else:
            skipped_files += 1

    print(f'Updated files: {file_count}')
    print(f'Skipped (already had all blocks): {skipped_files}')
    print(f'Inserted: epigraph={total_ep}, big_picture={total_bp}, prereq={total_pr}')
    if missing:
        print('MISSING FILES (path not found):')
        for m in missing:
            print(f'  {m}')


if __name__ == '__main__':
    main()
