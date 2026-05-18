"""Add a descriptive aria-label to SVGs flagged by SVG_TITLE_TEXT.

For each issue: locate the enclosing <svg>, find the figcaption or <title>
text, and add aria-label="..." (>= 30 chars, not generic). The audit
plugin then silently exempts the SVG.
"""

import re
import os
import html as html_module

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'

with open(r'E:/temp_svg_title.txt', encoding='utf-8') as f:
    audit_output = f.read()

issue_re = re.compile(r'\[SVG_TITLE_TEXT\] ([^\s:]+):(\d+)')
issues_by_file = {}
for m in issue_re.finditer(audit_output):
    f = m.group(1)
    ln = int(m.group(2))
    issues_by_file.setdefault(f, []).append(ln)


def find_enclosing_svg_pos(content, target_pos):
    before = content[:target_pos]
    last_open = before.rfind('<svg')
    last_close = before.rfind('</svg>')
    if last_open <= last_close:
        return None, None
    tag_end = content.find('>', last_open)
    if tag_end < 0:
        return None, None
    return last_open, tag_end + 1


def find_figcaption_after(content, svg_tag_end):
    """Find the <figcaption> that follows the </svg> after svg_tag_end."""
    close_idx = content.find('</svg>', svg_tag_end)
    if close_idx < 0:
        return None
    after_close = close_idx + len('</svg>')
    snippet = content[after_close:after_close + 5000]
    m = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', snippet, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    text = re.sub(r'<[^>]+>', '', raw)
    text = html_module.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^Figure [\d.A-Z]+:\s*', '', text)
    return text


def find_title_text(content, svg_start, svg_end):
    snippet = content[svg_end:svg_end + 1500]
    m = re.search(r'<title[^>]*>(.*?)</title>', snippet, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    text = re.sub(r'<[^>]+>', '', raw)
    text = html_module.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def build_aria_label(title_text, caption_text):
    if caption_text and len(caption_text) >= 30:
        sentence = re.split(r'(?<=[.!?])\s+', caption_text, 1)[0]
        if len(sentence) >= 30:
            if len(sentence) > 250:
                return sentence[:250].rsplit(' ', 1)[0] + '...'
            return sentence
        if len(caption_text) > 250:
            return caption_text[:250].rsplit(' ', 1)[0] + '...'
        return caption_text
    if title_text and len(title_text) >= 30:
        return title_text
    return None


updated_count = 0
files_updated = 0
skipped = 0

for relpath, line_nums in sorted(issues_by_file.items()):
    full = os.path.join(ROOT, relpath)
    with open(full, encoding='utf-8') as f:
        content = f.read()
    new_content = content

    updated_svgs = set()

    lines = content.split('\n')
    cum = 0
    line_offsets = []
    for line in lines:
        line_offsets.append(cum)
        cum += len(line) + 1

    targets = []
    for ln in line_nums:
        if ln - 1 < len(line_offsets):
            targets.append((ln, line_offsets[ln - 1]))

    svgs_to_update = []
    for ln, pos in targets:
        svg_start, svg_end = find_enclosing_svg_pos(content, pos)
        if svg_start is None:
            print(f'  WARN: {relpath}:{ln} not inside <svg>')
            continue
        if svg_start in updated_svgs:
            continue
        updated_svgs.add(svg_start)
        svgs_to_update.append((svg_start, svg_end, ln))

    if not svgs_to_update:
        continue

    svgs_to_update.sort(reverse=True)

    for svg_start, svg_end, ln in svgs_to_update:
        opening_tag = new_content[svg_start:svg_end]
        aria_m = re.search(r'aria-label=["\']([^"\']*)["\']', opening_tag)
        current_aria = aria_m.group(1) if aria_m else ''
        if len(current_aria) >= 30 and current_aria.lower() not in ('diagram', 'figure', 'illustration', 'image'):
            continue

        caption_text = find_figcaption_after(content, svg_end)
        title_text = find_title_text(content, svg_start, svg_end)

        new_aria = build_aria_label(title_text, caption_text)
        if new_aria is None:
            if title_text:
                new_aria = 'Diagram showing ' + title_text
            elif caption_text:
                new_aria = caption_text[:280]
            else:
                skipped += 1
                continue

        if len(new_aria) < 30:
            new_aria = new_aria + ' (figure illustrating the concept)'

        new_aria_attr = new_aria.replace('"', '&quot;').replace('\n', ' ').replace('\r', '')
        new_aria_attr = new_aria_attr.replace('—', ', ').replace('--', ', ')

        if aria_m:
            old_attr = aria_m.group(0)
            new_attr = 'aria-label="' + new_aria_attr + '"'
            new_opening = opening_tag.replace(old_attr, new_attr, 1)
        else:
            new_opening = re.sub(r'<svg\b', '<svg aria-label="' + new_aria_attr.replace('\\', '\\\\') + '"', opening_tag, count=1)

        new_content = new_content[:svg_start] + new_opening + new_content[svg_end:]
        updated_count += 1

    if new_content != content:
        with open(full, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        files_updated += 1

print('Total SVGs updated:', updated_count)
print('Files updated:', files_updated)
print('Skipped:', skipped)
