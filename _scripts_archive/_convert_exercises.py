#!/usr/bin/env python3
"""Convert exercise markup to standardized .callout.exercise format.

Pattern A: <div class="exercise"> with <h3> -> <div class="callout exercise"> with <div class="callout-title">
Pattern B: <section class="exercises"> with <ol>/<li> -> individual <div class="callout exercise"> boxes
"""

import re
import os
import glob

REPO = r"E:\Projects\LLMCourse"

# ---------- Pattern A conversion ----------

def convert_pattern_a(filepath):
    """Convert <div class="exercise"><h3>...</h3> to <div class="callout exercise"><div class="callout-title">...</div>"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    count = 0

    # Replace <div class="exercise"> with <div class="callout exercise">
    # and <h3> inside with <div class="callout-title">&#9998; ...
    def replace_exercise_block(m):
        nonlocal count
        count += 1
        block = m.group(0)
        # Replace opening div
        block = block.replace('<div class="exercise">', '<div class="callout exercise">', 1)
        # Replace <h3>...</h3> with <div class="callout-title">&#9998; ...</div>
        block = re.sub(
            r'<h3>(.*?)</h3>',
            lambda h: '<div class="callout-title">&#9998; ' + h.group(1) + '</div>',
            block,
            count=1
        )
        return block

    # Match each <div class="exercise">...</div> block (non-greedy, matching up to closing </div>)
    # We need to be careful with nested divs - but exercise blocks don't contain nested divs typically
    # Use a simple approach: find <div class="exercise"> and match until the next </div>\n\n or </div>\n\n

    # Actually, let's do line-by-line replacement which is safer
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if '<div class="exercise">' in line and 'callout' not in line:
            new_lines.append(line.replace('<div class="exercise">', '<div class="callout exercise">'))
            count += 1
            i += 1
            continue
        # Convert <h3>Exercise... to <div class="callout-title">&#9998; Exercise...
        if re.search(r'<h3>(Exercise\s+\d)', line):
            line = re.sub(
                r'<h3>(.*?)</h3>',
                lambda m: '<div class="callout-title">&#9998; ' + m.group(1) + '</div>',
                line
            )
            new_lines.append(line)
            i += 1
            continue
        new_lines.append(line)
        i += 1

    content = '\n'.join(new_lines)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    return count


# ---------- Pattern B conversion ----------

def parse_exercises_from_ol(ol_html, section_num, start_idx):
    """Parse <ol> containing <li> exercises into a list of exercise dicts."""
    exercises = []
    # Find all <li> items
    li_pattern = re.compile(r'<li>(.*?)</li>', re.DOTALL)
    for m in li_pattern.finditer(ol_html):
        li_content = m.group(1).strip()
        exercises.append({
            'content': li_content,
            'idx': start_idx + len(exercises)
        })
    return exercises


def extract_level_badge(text):
    """Extract level badge from text, return (badge_html, remaining_text)."""
    badge_match = re.search(r'<span class="level-badge\s+(\w+)">(.*?)</span>', text)
    if badge_match:
        level = badge_match.group(1).lower()
        label = badge_match.group(2)
        badge_html = f'<span class="level-badge {level}">{label}</span>'
        remaining = text[:badge_match.start()] + text[badge_match.end():]
        return badge_html, remaining.strip()
    return '', text


def extract_title_and_content(li_text):
    """Extract title (from <strong>) and question content from an <li>."""
    # Pattern: <span badge> <strong>Title:</strong> Question text
    # or: <strong>Title:</strong> Question text
    badge_html, text = extract_level_badge(li_text)

    # Extract <strong>Title:</strong> or <strong>Title</strong>
    title_match = re.match(r'\s*<strong>(.*?):?</strong>\s*(.*)', text, re.DOTALL)
    if title_match:
        title = title_match.group(1).rstrip(':')
        question = title_match.group(2).strip()
        return title, question, badge_html

    # No strong title, use first sentence as title
    return None, text, badge_html


def convert_pattern_b(filepath):
    """Convert <section class="exercises"> with <ol>/<li> to individual callout exercise boxes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Find the exercises section
    section_match = re.search(
        r'<section class="exercises">(.*?)</section>',
        content, re.DOTALL
    )
    if not section_match:
        return 0

    section_html = section_match.group(1)

    # Get section number from filename
    fname = os.path.basename(filepath)
    sec_match = re.search(r'section-(\d+\.\d+)', fname)
    if not sec_match:
        return 0
    section_num = sec_match.group(1)

    # Remove the styled instruction div
    instruction_match = re.search(
        r'<div style="[^"]*">\s*<p style="[^"]*"><strong>How to use these exercises:</strong>\s*(.*?)</p>\s*</div>',
        section_html, re.DOTALL
    )
    instruction_text = ''
    if instruction_match:
        instruction_text = instruction_match.group(1).strip()

    # Find all <ol> blocks and their preceding <h3> headers
    # Split by <h3> to get category groups
    # Find all exercises across all <ol> blocks
    all_exercises = []

    # Find all <h3> headers and their following <ol> blocks
    # Pattern: <h3>Category</h3> ... <ol>...</ol>
    category_pattern = re.compile(
        r'<h3>(.*?)</h3>\s*<ol>(.*?)</ol>',
        re.DOTALL
    )

    for cat_match in category_pattern.finditer(section_html):
        category = cat_match.group(1).strip()
        ol_html = cat_match.group(2)

        li_pattern = re.compile(r'<li>(.*?)</li>', re.DOTALL)
        for li_match in li_pattern.finditer(ol_html):
            li_content = li_match.group(1).strip()
            all_exercises.append({
                'category': category,
                'content': li_content,
            })

    if not all_exercises:
        return 0

    # Find answers section
    answers = []
    answers_match = re.search(
        r'<details>\s*<summary>Answers</summary>\s*<ol>(.*?)</ol>\s*</details>',
        section_html, re.DOTALL
    )
    if answers_match:
        answer_li_pattern = re.compile(r'<li>(.*?)</li>', re.DOTALL)
        for am in answer_li_pattern.finditer(answers_match.group(1)):
            answers.append(am.group(1).strip())

    # Build new exercises HTML
    exercise_parts = []
    exercise_parts.append('<section class="exercises">')
    exercise_parts.append('    <h2>Exercises</h2>')

    if instruction_text:
        exercise_parts.append(f'    <p><strong>How to use these exercises:</strong> {instruction_text}</p>')

    exercise_idx = 0
    for ex in all_exercises:
        exercise_idx += 1
        ex_num = f"{section_num}.{exercise_idx}"

        title, question, badge_html = extract_title_and_content(ex['content'])

        if title:
            title_line = f'&#9998; Exercise {ex_num}: {title}'
        else:
            title_line = f'&#9998; Exercise {ex_num}'

        if badge_html:
            title_line += f' {badge_html}'

        exercise_parts.append('')
        exercise_parts.append('    <div class="callout exercise">')
        exercise_parts.append(f'        <div class="callout-title">{title_line}</div>')
        exercise_parts.append(f'        <p>{question}</p>')

        # Add answer if available
        if exercise_idx - 1 < len(answers):
            answer = answers[exercise_idx - 1]
            exercise_parts.append(f'        <details><summary>Show Answer</summary>')
            exercise_parts.append(f'            <p>{answer}</p>')
            exercise_parts.append(f'        </details>')

        exercise_parts.append('    </div>')

    exercise_parts.append('</section>')

    new_section = '\n'.join(exercise_parts)

    # Replace old section with new
    content = content[:section_match.start()] + new_section + content[section_match.end():]

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return exercise_idx


# ---------- Main ----------

def main():
    total_exercises = 0
    files_converted = 0

    # Pattern A files
    pattern_a_files = []

    # Part 3 files
    for f in ['part-3-working-with-llms/module-10-llm-apis/section-10.4.html',
              'part-3-working-with-llms/module-11-prompt-engineering/section-11.5.html']:
        pattern_a_files.append(os.path.join(REPO, f))

    # Part 7 module-30 files
    for f in glob.glob(os.path.join(REPO, 'part-7-production-strategy/module-30-frontiers/section-30.*.html')):
        pattern_a_files.append(f)

    print("=== Pattern A Conversions ===")
    for filepath in pattern_a_files:
        if os.path.exists(filepath):
            count = convert_pattern_a(filepath)
            if count > 0:
                print(f"  {os.path.relpath(filepath, REPO)}: {count} exercises")
                total_exercises += count
                files_converted += 1
        else:
            print(f"  MISSING: {filepath}")

    # Pattern B files - all section files in part-5 that have exercises
    print("\n=== Pattern B Conversions ===")
    pattern_b_files = glob.glob(os.path.join(REPO, 'part-5-retrieval-conversation/*/section-*.html'))

    for filepath in sorted(pattern_b_files):
        with open(filepath, 'r', encoding='utf-8') as f:
            if '<section class="exercises">' not in f.read():
                continue
        count = convert_pattern_b(filepath)
        if count > 0:
            print(f"  {os.path.relpath(filepath, REPO)}: {count} exercises")
            total_exercises += count
            files_converted += 1

    print(f"\n=== Summary ===")
    print(f"Files converted: {files_converted}")
    print(f"Total exercises converted: {total_exercises}")


if __name__ == '__main__':
    main()
