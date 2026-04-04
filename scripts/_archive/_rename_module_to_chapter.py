#!/usr/bin/env python3
"""
Rename "Module" to "Chapter" terminology across the entire book.

Idempotent: safe to run multiple times. Already-renamed text is not touched.
Skips content inside <pre>...</pre> and <code>...</code> tags.
Does NOT rename directory paths (module-XX-name folders stay as-is).
"""

import os
import re
import glob
from collections import defaultdict

ROOT = r"E:\Projects\LLMCourse"

# ── Counters ──────────────────────────────────────────────────────────
counts = defaultdict(int)
files_changed = 0


def protect_code_blocks(html):
    """Extract <pre>...</pre> and <code>...</code> blocks, replace with placeholders."""
    placeholders = []

    def save(m):
        placeholders.append(m.group(0))
        return f"\x00CODEBLOCK{len(placeholders) - 1}\x00"

    # pre blocks first (they may contain code tags)
    html = re.sub(r'<pre\b[^>]*>.*?</pre>', save, html, flags=re.DOTALL)
    # then inline code
    html = re.sub(r'<code\b[^>]*>.*?</code>', save, html, flags=re.DOTALL)
    return html, placeholders


def restore_code_blocks(html, placeholders):
    """Put code blocks back."""
    for i, block in enumerate(placeholders):
        html = html.replace(f"\x00CODEBLOCK{i}\x00", block)
    return html


def counted(category):
    """Return a replacement function that increments a counter."""
    def replacer(repl_str):
        def fn(m):
            counts[category] += 1
            # If repl_str contains group references like \1, expand them
            return m.expand(repl_str)
        return fn
    return replacer


# ── Replacement passes ────────────────────────────────────────────────

def apply_replacements(text):
    """Apply all module-to-chapter replacements on non-code text."""

    c = counted

    # ── 1. CSS class names in HTML attributes ──
    # Order matters: longer/more-specific patterns first

    # class="module-header" -> class="chapter-header-item"
    text = re.sub(
        r'(?<=class=")module-header(?=")',
        lambda m: (counts.__setitem__('css_class', counts['css_class'] + 1), 'chapter-header-item')[1],
        text
    )
    # .module-header in CSS selectors
    text = re.sub(
        r'\.module-header\b(?!-)',
        lambda m: (counts.__setitem__('css_selector', counts['css_selector'] + 1), '.chapter-header-item')[1],
        text
    )

    # class="module-index" -> class="chapter-index"
    text = re.sub(
        r'(?<=class=")module-index(?=")',
        lambda m: (counts.__setitem__('css_class', counts['css_class'] + 1), 'chapter-index')[1],
        text
    )
    text = re.sub(
        r'\.module-index\b',
        lambda m: (counts.__setitem__('css_selector', counts['css_selector'] + 1), '.chapter-index')[1],
        text
    )

    # class="module-label" -> class="chapter-label"
    text = re.sub(
        r'(?<=class=")module-label(?=")',
        lambda m: (counts.__setitem__('css_class', counts['css_class'] + 1), 'chapter-label')[1],
        text
    )
    text = re.sub(
        r'\.module-label\b',
        lambda m: (counts.__setitem__('css_selector', counts['css_selector'] + 1), '.chapter-label')[1],
        text
    )

    # class="module-num" -> class="chapter-num"
    text = re.sub(
        r'(?<=class=")module-num(?=")',
        lambda m: (counts.__setitem__('css_class', counts['css_class'] + 1), 'chapter-num')[1],
        text
    )
    text = re.sub(
        r'\.module-num\b',
        lambda m: (counts.__setitem__('css_selector', counts['css_selector'] + 1), '.chapter-num')[1],
        text
    )

    # class="module-desc" -> class="chapter-desc"
    text = re.sub(
        r'(?<=class=")module-desc(?=")',
        lambda m: (counts.__setitem__('css_class', counts['css_class'] + 1), 'chapter-desc')[1],
        text
    )
    text = re.sub(
        r'\.module-desc\b',
        lambda m: (counts.__setitem__('css_selector', counts['css_selector'] + 1), '.chapter-desc')[1],
        text
    )

    # class="module-body" -> class="chapter-body"
    text = re.sub(
        r'(?<=class=")module-body(?=")',
        lambda m: (counts.__setitem__('css_class', counts['css_class'] + 1), 'chapter-body')[1],
        text
    )
    text = re.sub(
        r'\.module-body\b',
        lambda m: (counts.__setitem__('css_selector', counts['css_selector'] + 1), '.chapter-body')[1],
        text
    )

    # class="module" (standalone) -> class="book-chapter"
    # Match class="module" exactly (not module-something)
    text = re.sub(
        r'class="module"',
        lambda m: (counts.__setitem__('css_class', counts['css_class'] + 1), 'class="book-chapter"')[1],
        text
    )
    # CSS selector .module followed by space, brace, colon, dot, or line end (not .module-)
    # But be careful not to match already-renamed .book-chapter
    text = re.sub(
        r'(?<!\w)\.module(?=\s*[\{:.>\s,]|$)(?!-)',
        lambda m: (counts.__setitem__('css_selector', counts['css_selector'] + 1), '.book-chapter')[1],
        text
    )

    # ── 2. ID attributes: id="modNN" -> id="chNN" ──
    text = re.sub(
        r'id="mod(\d+)"',
        lambda m: (counts.__setitem__('id_attr', counts['id_attr'] + 1), f'id="ch{m.group(1)}"')[1],
        text
    )

    # ── 3. Href anchors: #modNN -> #chNN ──
    text = re.sub(
        r'href="#mod(\d+)"',
        lambda m: (counts.__setitem__('href_anchor', counts['href_anchor'] + 1), f'href="#ch{m.group(1)}"')[1],
        text
    )

    # ── 4. Title tags: "Module NN:" -> "Chapter NN:" ──
    text = re.sub(
        r'(<title>)Module (\d+)',
        lambda m: (counts.__setitem__('title_tag', counts['title_tag'] + 1), f'{m.group(1)}Chapter {m.group(2)}')[1],
        text
    )

    # ── 5. Prose text replacements (case-sensitive) ──
    # Compound words first
    text = re.sub(
        r'Cross-module',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), 'Cross-chapter')[1],
        text
    )
    text = re.sub(
        r'cross-module',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), 'cross-chapter')[1],
        text
    )
    text = re.sub(
        r'per-module',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), 'per-chapter')[1],
        text
    )
    text = re.sub(
        r'multi-module',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), 'multi-chapter')[1],
        text
    )

    # "Modules" -> "Chapters" (when referring to book structure)
    # Avoid "Python modules", "nn.Modules" etc.
    # Match "Modules" when NOT preceded by Python/software/nn./torch. context
    text = re.sub(
        r'(?<!nn\.)(?<!torch\.)(?<!Python )(?<!python )(?<!software )Modules\b',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), 'Chapters')[1],
        text
    )
    text = re.sub(
        r'(?<!nn\.)(?<!torch\.)(?<!Python )(?<!python )(?<!software )(?<!\/)modules\b(?!\/)',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), 'chapters')[1],
        text
    )

    # "Module NN" -> "Chapter NN" (where NN is a digit)
    # Protect: href="...module-NN..." paths (directory names)
    # Protect: nn.Module, Python module, software module
    # Strategy: only replace "Module" followed by a space and digit
    text = re.sub(
        r'(?<!\.)Module (\d)',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), f'Chapter {m.group(1)}')[1],
        text
    )
    text = re.sub(
        r'(?<!\.)module (\d)',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), f'chapter {m.group(1)}')[1],
        text
    )

    # HTML comment references: MODULE 0, MODULE 1, etc.
    text = re.sub(
        r'MODULE (\d)',
        lambda m: (counts.__setitem__('prose', counts['prose'] + 1), f'CHAPTER {m.group(1)}')[1],
        text
    )

    return text


def process_file(filepath):
    """Process a single file. Return True if changed."""
    global files_changed

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original = f.read()

    # Protect code blocks
    text, placeholders = protect_code_blocks(original)

    # Apply replacements
    text = apply_replacements(text)

    # Restore code blocks
    text = restore_code_blocks(text, placeholders)

    if text != original:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        files_changed += 1
        return True
    return False


def main():
    global files_changed

    # Collect all HTML files
    html_files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)

    # Collect CSS files
    css_files = [os.path.join(ROOT, 'styles', 'book.css')]
    css_files += glob.glob(os.path.join(ROOT, '**', 'shared-*.css'), recursive=True)

    all_files = sorted(set(html_files + css_files))

    print(f"Found {len(html_files)} HTML files and {len(css_files)} CSS files")
    print(f"Total files to process: {len(all_files)}")
    print()

    changed_files = []
    for filepath in all_files:
        if process_file(filepath):
            rel = os.path.relpath(filepath, ROOT)
            changed_files.append(rel)

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files processed:  {len(all_files)}")
    print(f"Files changed:    {files_changed}")
    print()
    print("Replacements by category:")
    for cat in sorted(counts.keys()):
        print(f"  {cat:20s} {counts[cat]:>6d}")
    print(f"  {'TOTAL':20s} {sum(counts.values()):>6d}")
    print()

    if changed_files:
        print(f"Changed files ({len(changed_files)}):")
        for f in changed_files:
            print(f"  {f}")


if __name__ == '__main__':
    main()
