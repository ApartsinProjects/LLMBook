"""
Fix all code blocks in Parts 1-2:
1. Add/fix Code Fragment N captions (preserve existing text)
2. Add opening comments where missing
3. Add prose references in preceding paragraphs
"""

import re
import os
import glob

files = sorted(
    glob.glob("E:/Projects/LLMCourse/part-1-foundations/module-*/section-*.html") +
    glob.glob("E:/Projects/LLMCourse/part-2-understanding-llms/module-*/section-*.html")
)


def detect_language(code_text):
    """Detect language from code content."""
    clean = re.sub(r'<[^>]+>', '', code_text).strip().lower()
    if any(kw in clean for kw in ['import ', 'from ', 'def ', 'class ', 'print(', 'np.', 'torch.']):
        return 'python'
    if any(kw in clean for kw in ['const ', 'let ', 'var ', 'function ', '=>', 'console.log']):
        return 'javascript'
    if 'select ' in clean and 'from ' in clean:
        return 'sql'
    if clean.startswith('$') or clean.startswith('pip ') or clean.startswith('curl '):
        return 'bash'
    return 'python'


def get_comment_prefix(lang):
    prefixes = {'python': '#', 'javascript': '//', 'sql': '--', 'bash': '#'}
    return prefixes.get(lang, '#')


def get_code_plain_text(code_html):
    return re.sub(r'<[^>]+>', '', code_html).strip()


def has_opening_comments(code_text, lang):
    """Check if code already starts with comment lines."""
    stripped = code_text.strip()
    if stripped.startswith('<code>'):
        stripped = stripped[6:]
    stripped = stripped.strip()
    prefix = get_comment_prefix(lang)

    lines = stripped.split('\n')
    for line in lines[:3]:
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if not clean_line:
            continue
        if clean_line.startswith(prefix) or clean_line.startswith('"""') or clean_line.startswith("'''"):
            return True
        return False
    return False


def generate_comments(code_text, lang):
    """Generate 2-line opening comments."""
    plain = get_code_plain_text(code_text)
    prefix = get_comment_prefix(lang)

    classes = re.findall(r'class\s+(\w+)', plain)
    funcs = [f for f in re.findall(r'def\s+(\w+)', plain) if f not in ('__init__', 'forward', '__repr__')]

    # Build line 1: what
    parts = []
    if classes:
        parts.append(f"Define {', '.join(classes[:2])}")
    if funcs:
        parts.append(f"implement {', '.join(funcs[:3])}")

    if not parts:
        if 'torch' in plain:
            parts.append("PyTorch implementation")
        elif 'numpy' in plain or 'np.' in plain:
            parts.append("NumPy computation")
        else:
            parts.append("Implementation example")

    line1 = f"{prefix} {'; '.join(parts)}"

    # Build line 2: key operations
    ops = []
    if 'forward' in plain: ops.append("forward pass computation")
    if 'loss' in plain.lower(): ops.append("loss calculation")
    if 'train' in plain.lower(): ops.append("training loop")
    if 'softmax' in plain.lower(): ops.append("softmax normalization")
    if 'attention' in plain.lower(): ops.append("attention mechanism")
    if 'embedding' in plain.lower() or 'embed' in plain.lower(): ops.append("embedding lookup")
    if 'gradient' in plain.lower() or 'backward' in plain.lower(): ops.append("gradient computation")
    if 'plt.' in plain or 'plot' in plain.lower(): ops.append("visualization")
    if 'print' in plain: ops.append("results display")

    if ops:
        line2 = f"{prefix} Key operations: {', '.join(ops[:3])}"
    else:
        line2 = f"{prefix} See inline comments for step-by-step details."

    return f"{line1}\n{line2}\n"


def generate_caption_text(code_text):
    """Generate a descriptive caption for a code block without Code Fragment label."""
    plain = get_code_plain_text(code_text)

    class_match = re.findall(r'class\s+(\w+)', plain)
    func_match = [f for f in re.findall(r'def\s+(\w+)', plain)
                  if f not in ('__init__', 'forward', '__repr__', '__str__')]

    parts = []
    if class_match:
        parts.append(f"the {class_match[0]} class")
    if func_match:
        parts.append(f"the {', '.join(func_match[:2])} function{'s' if len(func_match) > 1 else ''}")

    topic = ' and '.join(parts) if parts else 'this approach'

    tech = []
    if 'torch' in plain: tech.append('PyTorch')
    if 'numpy' in plain or 'np.' in plain: tech.append('NumPy')
    if 'attention' in plain.lower(): tech.append('attention computation')
    if 'embed' in plain.lower(): tech.append('embedding operations')
    if 'loss' in plain.lower(): tech.append('loss computation')

    tech_str = f" using {', '.join(tech[:2])}" if tech else ""

    sentence1 = f"This snippet demonstrates {topic}{tech_str}."

    # Sentence 2: notice
    if 'dropout' in plain.lower():
        sentence2 = "Notice how dropout is applied for regularization during training."
    elif 'attention' in plain.lower():
        sentence2 = "Notice how the attention weights are computed and applied to the value vectors."
    elif 'mask' in plain.lower():
        sentence2 = "Notice how masking prevents information leakage from future positions."
    elif 'embed' in plain.lower():
        sentence2 = "Notice how the embedding dimensions are scaled to maintain stable gradient flow."
    elif 'loss' in plain.lower():
        sentence2 = "Notice how the loss function drives the optimization toward better predictions."
    elif 'train' in plain.lower():
        sentence2 = "Notice how each training step updates the parameters based on the computed gradients."
    elif 'plt.' in plain or 'plot' in plain.lower():
        sentence2 = "The resulting visualization highlights the key trends and patterns in the data."
    else:
        sentence2 = "Study the implementation details to understand how each component contributes to the overall computation."

    # Sentence 3: why
    if 'torch' in plain:
        sentence3 = "This pattern is common in production PyTorch code and forms a building block for larger architectures."
    elif 'numpy' in plain or 'np.' in plain:
        sentence3 = "Understanding the underlying numerical operations builds intuition for how the model processes data."
    elif class_match:
        sentence3 = "This modular design makes it straightforward to compose larger systems from smaller, well-tested components."
    else:
        sentence3 = "Tracing through each step builds the intuition needed when debugging or extending similar systems."

    return f"{sentence1} {sentence2} {sentence3}"


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Find all <pre>...</pre> blocks
    pre_pattern = re.compile(r'<pre[^>]*>(.*?)</pre>', re.DOTALL)
    matches = list(pre_pattern.finditer(content))

    if not matches:
        return 0, 0, 0, 0

    num_blocks = len(matches)
    captions_fixed = 0
    comments_added = 0
    refs_added = 0

    # We need to process forward (for numbering) but track edits carefully
    # Strategy: collect all edits, then apply them in reverse order

    edits = []  # list of (position, delete_length, insert_text, edit_type)

    for idx, match in enumerate(matches):
        fragment_num = idx + 1
        pre_start = match.start()
        pre_end = match.end()
        code_content = match.group(1)

        # === CAPTION ===
        # Check for existing caption BEFORE <pre>
        before_zone = content[max(0, pre_start - 600):pre_start]
        # Look for a code-caption div as the last element before <pre>
        cap_before_match = re.search(
            r'(<div class="code-caption">)(.*?)(</div>)\s*$',
            before_zone, re.DOTALL
        )

        # Check for existing caption AFTER </pre>
        after_zone = content[pre_end:pre_end + 600]
        cap_after_match = re.match(
            r'\s*(<div class="code-caption">)(.*?)(</div>)',
            after_zone, re.DOTALL
        )

        if cap_before_match:
            # Caption exists before: add Code Fragment label if missing
            existing_text = cap_before_match.group(2).strip()
            has_label = bool(re.search(r'Code Fragment \d+:', re.sub(r'<[^>]+>', '', existing_text)))

            if not has_label:
                # Preserve existing text, just prepend label
                # Remove any existing <strong> wrapper at the start
                cleaned = re.sub(r'^<strong>[^<]*</strong>\s*', '', existing_text)
                new_inner = f'<strong>Code Fragment {fragment_num}:</strong> {cleaned}'
                abs_start = max(0, pre_start - 600) + cap_before_match.start(2)
                abs_end = max(0, pre_start - 600) + cap_before_match.end(2)
                edits.append((abs_start, abs_end - abs_start, new_inner, 'caption'))
                captions_fixed += 1

        elif cap_after_match:
            # Caption exists after: add Code Fragment label if missing
            existing_text = cap_after_match.group(2).strip()
            has_label = bool(re.search(r'Code Fragment \d+:', re.sub(r'<[^>]+>', '', existing_text)))

            if not has_label:
                cleaned = re.sub(r'^<strong>[^<]*</strong>\s*', '', existing_text)
                new_inner = f'<strong>Code Fragment {fragment_num}:</strong> {cleaned}'
                abs_start = pre_end + cap_after_match.start(2)
                abs_end = pre_end + cap_after_match.end(2)
                edits.append((abs_start, abs_end - abs_start, new_inner, 'caption'))
                captions_fixed += 1

        else:
            # No caption at all: add one after </pre>
            caption_text = generate_caption_text(code_content)
            new_caption = f'\n<div class="code-caption"><strong>Code Fragment {fragment_num}:</strong> {caption_text}</div>'
            edits.append((pre_end, 0, new_caption, 'caption'))
            captions_fixed += 1

        # === OPENING COMMENTS ===
        lang = detect_language(code_content)
        if not has_opening_comments(code_content, lang):
            comment_text = generate_comments(code_content, lang)
            # Find insertion point: right after <pre> or <pre><code>
            pre_tag_match = re.match(r'(<pre[^>]*>)(\s*<code>)?', content[pre_start:pre_start + 60])
            if pre_tag_match:
                insert_pos = pre_start + pre_tag_match.end()
                prefix = '\n' if content[insert_pos] != '\n' else ''
                edits.append((insert_pos, 0, prefix + comment_text, 'comment'))
                comments_added += 1

        # === PROSE REFERENCE ===
        # Find the nearest preceding <p>...</p> that is NOT inside a callout
        # Search backward from the caption position or pre_start
        search_before = pre_start
        if cap_before_match:
            search_before = max(0, pre_start - 600) + cap_before_match.start()

        # Find last </p> before search_before
        zone = content[:search_before]
        last_p_end = zone.rfind('</p>')
        if last_p_end != -1:
            p_start = zone.rfind('<p>', 0, last_p_end)
            if p_start == -1:
                p_start = zone.rfind('<p ', 0, last_p_end)
            if p_start != -1:
                p_end = last_p_end + 4
                p_text = content[p_start:p_end]

                # Check this paragraph is not inside a callout
                # Look for unclosed .callout div before this <p>
                preceding = content[max(0, p_start - 300):p_start]
                in_callout = False
                # Simple heuristic: check if there's a callout div open without close
                callout_opens = len(re.findall(r'<div class="callout', preceding))
                callout_closes = len(re.findall(r'</div>', preceding))
                if callout_opens > callout_closes:
                    in_callout = True

                if not in_callout:
                    # Check if paragraph already references code
                    plain_p = re.sub(r'<[^>]+>', '', p_text).lower()
                    reference_keywords = [
                        'following', 'below', 'code fragment', 'snippet',
                        'code block', 'listing', 'example shows', 'example demonstrates',
                        'illustrated by', 'shown in', 'see the code', 'we implement',
                        'consider the following', 'here we', 'next code',
                        'code example', 'demonstrates how', 'the code', 'this code',
                        'implementation below', 'implemented below', 'puts this into practice'
                    ]
                    has_ref = any(kw in plain_p for kw in reference_keywords)

                    if not has_ref:
                        # Insert reference before </p>
                        insert_text = f" Code Fragment {fragment_num} below puts this into practice."
                        edits.append((p_end - 4, 0, insert_text, 'ref'))
                        refs_added += 1

    # Apply edits in reverse order of position to preserve earlier positions
    edits.sort(key=lambda e: e[0], reverse=True)

    for pos, delete_len, insert_text, edit_type in edits:
        content = content[:pos] + insert_text + content[pos + delete_len:]

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return num_blocks, captions_fixed, comments_added, refs_added


# Process all files
print(f"Processing {len(files)} files...\n")
total_blocks = 0
total_captions = 0
total_comments = 0
total_refs = 0

for filepath in files:
    short = os.path.relpath(filepath, "E:/Projects/LLMCourse")
    blocks, captions, comments, refs = process_file(filepath)
    total_blocks += blocks
    total_captions += captions
    total_comments += comments
    total_refs += refs
    if blocks > 0:
        print(f"{short}: {blocks} blocks, {captions} captions, {comments} comments, {refs} refs")
    else:
        print(f"{short}: no code blocks")

print(f"\n=== TOTALS ===")
print(f"Files: {len(files)}")
print(f"Code blocks: {total_blocks}")
print(f"Captions fixed/added: {total_captions}")
print(f"Comments added: {total_comments}")
print(f"Prose references added: {total_refs}")
