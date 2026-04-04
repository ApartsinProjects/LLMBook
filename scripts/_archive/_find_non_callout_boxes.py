#!/usr/bin/env python3
"""Find content that looks like it should be a callout but isn't using the
standard <div class="callout TYPE"> pattern.

Detects:
1. Standalone <div> with inline background/border styles (ad-hoc boxes)
2. <div class="..."> with class names that suggest callout-like content
   but don't use the callout system (e.g. "info-box", "note-box", "example")
3. <blockquote> that aren't epigraphs (could be callouts)
4. Bold-prefixed paragraphs like **Note:** or **Warning:** outside callouts
5. <div> with style containing background-color (inline styled boxes)
"""
import glob, re, os

files = sorted(
    glob.glob('part-*/module-*/**/*.html', recursive=True) +
    glob.glob('part-*/module-*/section-*.html') +
    glob.glob('appendices/**/*.html', recursive=True) +
    glob.glob('front-matter/**/*.html', recursive=True) +
    glob.glob('capstone/**/*.html', recursive=True)
)

# Deduplicate
files = sorted(set(files))

# Patterns for non-callout boxes
patterns = [
    # Inline styled divs with background (ad-hoc boxes)
    (re.compile(r'<div[^>]*style="[^"]*background[^"]*"[^>]*>(?!.*class="callout)', re.IGNORECASE),
     "inline-styled-box"),
    # Div classes that look callout-like but aren't
    (re.compile(r'<div[^>]*class="(?!callout\b)[^"]*(?:info-box|note-box|example-box|tip-box|alert|notice|highlight-box|important|caution)[^"]*"', re.IGNORECASE),
     "non-standard-box-class"),
    # Bold prefix patterns outside callouts: <p><strong>Note:</strong> or <p><b>Warning:</b>
    (re.compile(r'<p>\s*<(?:strong|b)>\s*(?:Note|Warning|Tip|Important|Caution|Remember|Example|Hint|Did you know|Key point|Key insight|Watch out|Pro tip)\s*(?::|!)\s*</(?:strong|b)>', re.IGNORECASE),
     "bold-prefix-paragraph"),
    # Blockquotes that aren't epigraphs and aren't inside callouts
    (re.compile(r'<blockquote(?![^>]*class="epigraph")[^>]*>(?!.*callout)', re.IGNORECASE),
     "non-epigraph-blockquote"),
]

results = {}

for f in files:
    content = open(f, 'r', encoding='utf-8').read()
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        for pat, label in patterns:
            if pat.search(line):
                # Skip if this line is inside a callout
                # Simple heuristic: check surrounding 10 lines for callout class
                context_start = max(0, line_num - 10)
                context_end = min(len(lines), line_num + 3)
                context = '\n'.join(lines[context_start:context_end])
                if 'class="callout' in context and label == "bold-prefix-paragraph":
                    continue
                if label == "non-epigraph-blockquote":
                    # Skip blockquotes that are clearly not callout material
                    if 'class="pull-quote"' in line or 'class="quote"' in line:
                        continue
                key = f
                if key not in results:
                    results[key] = []
                results[key].append((line_num, label, line.strip()[:120]))

# Print results
total = 0
for f, hits in sorted(results.items()):
    print(f'\n{f}:')
    for line_num, label, preview in hits:
        print(f'  L{line_num} [{label}] {preview}')
        total += 1

print(f'\n{"="*60}')
print(f'Total: {total} suspected non-callout boxes in {len(results)} files')
