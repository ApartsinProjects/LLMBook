"""
Reformat single-paragraph research-frontier callouts into the standard format:
multiple <p> elements, each starting with a <strong>bold topic sentence.</strong>

The target format (from section 10.1):
  <div class="callout research-frontier">
    <div class="callout-title">Research Frontier</div>
    <p><strong>Topic sentence one.</strong> Supporting detail...</p>
    <p><strong>Topic sentence two.</strong> More detail...</p>
  </div>

Strategy: split the single paragraph at sentence boundaries where a new topic
begins (capital letter after period, keywords like "Second", "Another", etc.)

Usage:
  python fix_research_frontiers.py          # Dry run
  python fix_research_frontiers.py --fix    # Apply
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

FRONTIER_RE = re.compile(
    r'(<div class="callout research-frontier">\s*'
    r'<div class="callout-title">.*?</div>\s*)'
    r'(<p>)(.*?)(</p>)'
    r'(\s*</div>)',
    re.DOTALL
)

# Patterns that indicate a new topic sentence
TOPIC_STARTERS = re.compile(
    r'(?<=[.!?])\s+'  # After end of sentence
    r'(?='
    r'(?:Second|Third|Another|Meanwhile|Beyond|Recent|Current|Open|'
    r'Finally|Additionally|Furthermore|Moreover|Importantly|'
    r'A (?:key|major|related|separate|different|promising|notable)|'
    r'The (?:key|main|most|biggest|latest|emerging)|'
    r'One (?:promising|important|key|active|emerging)|'
    r'Early|Preliminary|Initial|Scaling|Several|Multiple|Perhaps|'
    r'In (?:parallel|practice|contrast|addition)|'
    r'On the (?:other|flip)|'
    r'More (?:recently|broadly|ambitiously)|'
    r'For (?:example|instance)|'
    r'At the (?:same|other)|'
    r'Looking (?:ahead|forward)|'
    r'This (?:matters|is|has|opens|connects|suggests|means|enables|raises))'
    r')'
)

TAG_RE = re.compile(r'<[^>]+>')


def split_into_topics(text):
    """Split a single paragraph into topic-sentence paragraphs."""
    # First try splitting at topic starters
    parts = TOPIC_STARTERS.split(text)

    if len(parts) <= 1:
        # Fallback: split at sentence boundaries where next sentence starts
        # with a capital letter and the current sentence was reasonably long
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        if len(sentences) >= 3:
            # Group into 2-3 sentence paragraphs
            parts = []
            current = []
            for i, s in enumerate(sentences):
                current.append(s)
                # Start a new paragraph every 2-3 sentences
                if len(current) >= 2 and i < len(sentences) - 1:
                    parts.append(' '.join(current))
                    current = []
            if current:
                parts.append(' '.join(current))
        else:
            return None  # Can't meaningfully split

    if len(parts) <= 1:
        return None

    return parts


def make_bold_lead(text):
    """Add <strong> to the first sentence of a paragraph."""
    # Find the first sentence boundary
    m = re.match(r'^(.*?[.!?])(\s+.+)?$', text, re.DOTALL)
    if m and m.group(2):
        first_sentence = m.group(1).strip()
        rest = m.group(2).strip()
        return f'<strong>{first_sentence}</strong> {rest}'
    else:
        # Single sentence paragraph, bold the whole thing
        return f'<strong>{text}</strong>'


def process_file(filepath, fix=False):
    content = filepath.read_text(encoding="utf-8")
    original = content

    matches = list(FRONTIER_RE.finditer(content))
    reformatted = 0

    for m in reversed(matches):
        prefix = m.group(1)  # Opening tags
        body = m.group(3)    # Content between <p>...</p>
        suffix = m.group(5)  # Closing </div>

        # Skip if already multi-paragraph
        if '<p>' in body:
            continue

        # Check if already has bold leads
        if '<strong>' in body:
            # Already formatted but in single <p>. Try to split at </strong>...<strong>
            pass

        # Get plain text to check length
        plain = TAG_RE.sub('', body)
        if len(plain) < 150:
            continue  # Too short to split meaningfully

        # Try to split
        parts = split_into_topics(body)
        if not parts or len(parts) <= 1:
            continue

        # Format each part with bold lead
        new_paras = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Don't re-bold if already has <strong>
            if not part.startswith('<strong>'):
                part = make_bold_lead(part)
            new_paras.append(f'<p>{part}</p>')

        new_body = '\n'.join(new_paras)

        # Replace in content
        start = m.start()
        end = m.end()
        replacement = f'{prefix}{new_body}{suffix}'
        content = content[:start] + replacement + content[end:]
        reformatted += 1

    if not fix:
        return reformatted

    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return reformatted


def main():
    fix = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total = 0
    files_affected = 0

    for f in all_files:
        count = process_file(f, fix=fix)
        if count > 0:
            files_affected += 1
            total += count
            rel = f.relative_to(BOOK_ROOT)
            action = "REFORMATTED" if fix else "needs reformatting"
            print(f"  {action}: {rel} ({count} callouts)")

    print(f"\n{'='*60}")
    print(f"Research frontiers to reformat: {total} across {files_affected} files")
    print(f"Scanned: {len(all_files)} files")
    if not fix and total > 0:
        print(f"\nRun with --fix to reformat.")


if __name__ == "__main__":
    main()
