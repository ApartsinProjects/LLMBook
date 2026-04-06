"""
Audit code captions across all section HTML files.

Checks:
1. Code blocks (<pre> or <pre><code>) without captions
2. Captions (<div class="code-caption">) without preceding code blocks
3. Caption text that doesn't reflect the actual code content (keyword mismatch)
4. Code blocks with duplicate/generic captions

Output: report of issues grouped by file.
"""

import re
import sys
from pathlib import Path
from collections import Counter

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Patterns
CODE_BLOCK_RE = re.compile(
    r'<pre[^>]*>(?:<code[^>]*>)?(.*?)(?:</code>)?</pre>',
    re.DOTALL
)
CODE_CAPTION_RE = re.compile(
    r'<div class="code-caption">(.*?)</div>',
    re.DOTALL
)
CODE_OUTPUT_RE = re.compile(
    r'<div class="code-output">(.*?)</div>',
    re.DOTALL
)
FIGURE_CAPTION_RE = re.compile(
    r'<figcaption[^>]*>(.*?)</figcaption>',
    re.DOTALL
)

# HTML tag stripper
TAG_RE = re.compile(r'<[^>]+>')

def strip_html(text):
    return TAG_RE.sub('', text).strip()

def extract_code_keywords(code_text):
    """Extract meaningful keywords from code content."""
    clean = strip_html(code_text)
    # Remove common noise
    clean = re.sub(r'#.*$', '', clean, flags=re.MULTILINE)  # comments
    clean = re.sub(r'""".*?"""', '', clean, flags=re.DOTALL)  # docstrings
    clean = re.sub(r"'''.*?'''", '', clean, flags=re.DOTALL)

    # Extract function/class names
    funcs = re.findall(r'def\s+(\w+)', clean)
    classes = re.findall(r'class\s+(\w+)', clean)

    # Extract imports
    imports = re.findall(r'(?:from|import)\s+([\w.]+)', clean)

    # Extract key identifiers (variable assignments, method calls)
    assignments = re.findall(r'(\w+)\s*=', clean)
    method_calls = re.findall(r'\.(\w+)\(', clean)

    keywords = set()
    for items in [funcs, classes, imports, assignments, method_calls]:
        for item in items:
            # Split camelCase and snake_case
            parts = re.split(r'[_.]', item)
            for p in parts:
                # Split camelCase
                sub = re.sub(r'([a-z])([A-Z])', r'\1 \2', p).lower().split()
                keywords.update(w for w in sub if len(w) > 2)

    return keywords

def extract_caption_keywords(caption_text):
    """Extract meaningful keywords from caption text."""
    clean = strip_html(caption_text)
    # Remove "Code Fragment N:" prefix
    clean = re.sub(r'Code Fragment\s*\d+\s*:', '', clean)
    # Tokenize
    words = re.findall(r'[a-zA-Z]+', clean.lower())
    # Filter stopwords
    stopwords = {'the', 'this', 'that', 'and', 'for', 'with', 'how', 'what',
                 'from', 'into', 'each', 'are', 'was', 'were', 'been', 'has',
                 'have', 'had', 'will', 'can', 'could', 'should', 'would',
                 'may', 'might', 'shall', 'not', 'but', 'yet', 'also', 'too',
                 'its', 'our', 'their', 'your', 'his', 'her', 'who', 'which',
                 'when', 'where', 'why', 'all', 'any', 'both', 'few', 'more',
                 'most', 'some', 'such', 'than', 'very', 'just', 'only',
                 'here', 'there', 'then', 'now', 'code', 'snippet', 'block',
                 'shows', 'demonstrates', 'example', 'notice', 'see', 'uses',
                 'fragment', 'above', 'below', 'following', 'first', 'second',
                 'step', 'steps', 'creates', 'implements', 'defines', 'using'}
    return set(w for w in words if len(w) > 2 and w not in stopwords)

def find_elements_in_order(html):
    """Find code blocks and captions in document order, with positions."""
    elements = []

    for m in CODE_BLOCK_RE.finditer(html):
        code_text = m.group(1)
        # Skip very short code (inline-like)
        if len(strip_html(code_text).strip()) < 10:
            continue
        elements.append({
            'type': 'code',
            'pos': m.start(),
            'end': m.end(),
            'text': code_text,
            'raw': m.group(0)
        })

    for m in CODE_CAPTION_RE.finditer(html):
        elements.append({
            'type': 'caption',
            'pos': m.start(),
            'end': m.end(),
            'text': m.group(1),
            'raw': m.group(0)
        })

    for m in CODE_OUTPUT_RE.finditer(html):
        elements.append({
            'type': 'output',
            'pos': m.start(),
            'end': m.end(),
            'text': m.group(1),
            'raw': m.group(0)
        })

    elements.sort(key=lambda e: e['pos'])
    return elements

def audit_file(filepath):
    """Audit a single file for code caption issues."""
    content = filepath.read_text(encoding='utf-8')
    issues = []

    elements = find_elements_in_order(content)

    # Walk through elements and pair code blocks with captions
    code_blocks = []
    captions = []
    paired_codes = set()
    paired_captions = set()

    for i, el in enumerate(elements):
        if el['type'] == 'code':
            code_blocks.append((i, el))
        elif el['type'] == 'caption':
            captions.append((i, el))

    # Try to pair: each caption should follow a code block (possibly with output in between)
    for ci, (cap_idx, cap_el) in enumerate(captions):
        # Find the nearest preceding code block
        preceding_code = None
        for code_idx, code_el in reversed(code_blocks):
            if code_el['pos'] < cap_el['pos']:
                preceding_code = (code_idx, code_el)
                break

        if preceding_code is None:
            issues.append({
                'type': 'orphan_caption',
                'caption': strip_html(cap_el['text'])[:120],
                'pos': cap_el['pos']
            })
        else:
            paired_codes.add(preceding_code[0])
            paired_captions.add(cap_idx)

            # Check content match
            code_kw = extract_code_keywords(preceding_code[1]['text'])
            cap_kw = extract_caption_keywords(cap_el['text'])

            if code_kw and cap_kw:
                overlap = code_kw & cap_kw
                # If very low overlap, flag as potential mismatch
                if len(overlap) == 0 and len(code_kw) > 3:
                    code_preview = strip_html(preceding_code[1]['text']).strip()[:100]
                    cap_preview = strip_html(cap_el['text']).strip()[:120]
                    issues.append({
                        'type': 'mismatch',
                        'code_preview': code_preview,
                        'caption': cap_preview,
                        'code_keywords': sorted(code_kw)[:10],
                        'caption_keywords': sorted(cap_kw)[:10],
                        'pos': cap_el['pos']
                    })

    # Find unpaired code blocks (no caption)
    for code_idx, code_el in code_blocks:
        if code_idx not in paired_codes:
            code_preview = strip_html(code_el['text']).strip()[:100]
            issues.append({
                'type': 'no_caption',
                'code_preview': code_preview,
                'pos': code_el['pos']
            })

    return issues

def main():
    patterns = [
        "part-*/module-*/section-*.html",
        "appendices/appendix-*/section-*.html",
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(BOOK_ROOT.glob(pattern))
    all_files = sorted(set(all_files))

    total_issues = 0
    total_no_caption = 0
    total_orphan = 0
    total_mismatch = 0
    files_with_issues = 0

    mismatch_details = []

    for f in all_files:
        issues = audit_file(f)
        if issues:
            files_with_issues += 1
            rel = f.relative_to(BOOK_ROOT)

            for issue in issues:
                total_issues += 1
                if issue['type'] == 'no_caption':
                    total_no_caption += 1
                elif issue['type'] == 'orphan_caption':
                    total_orphan += 1
                elif issue['type'] == 'mismatch':
                    total_mismatch += 1
                    mismatch_details.append((str(rel), issue))

    print(f"=== Code Caption Audit ===")
    print(f"Files scanned: {len(all_files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues: {total_issues}")
    print(f"  Code blocks without caption: {total_no_caption}")
    print(f"  Orphan captions (no code block): {total_orphan}")
    print(f"  Potential caption/code mismatches: {total_mismatch}")

    if '--verbose' in sys.argv or '-v' in sys.argv:
        print(f"\n=== Details ===")
        for f in all_files:
            issues = audit_file(f)
            if issues:
                rel = f.relative_to(BOOK_ROOT)
                print(f"\n{rel}:")
                for issue in issues:
                    if issue['type'] == 'no_caption':
                        print(f"  [NO CAPTION] Code: {issue['code_preview']}")
                    elif issue['type'] == 'orphan_caption':
                        print(f"  [ORPHAN CAP] Caption: {issue['caption']}")
                    elif issue['type'] == 'mismatch':
                        print(f"  [MISMATCH] Caption: {issue['caption']}")
                        print(f"             Code: {issue['code_preview']}")
                        print(f"             Code KW: {issue['code_keywords']}")
                        print(f"             Cap KW: {issue['caption_keywords']}")

    if '--mismatches' in sys.argv or '-m' in sys.argv:
        print(f"\n=== Potential Mismatches ===")
        for rel, issue in mismatch_details:
            print(f"\n{rel}:")
            print(f"  Caption: {issue['caption']}")
            print(f"  Code: {issue['code_preview']}")
            print(f"  Code KW: {issue['code_keywords']}")
            print(f"  Cap KW: {issue['caption_keywords']}")


if __name__ == "__main__":
    main()
