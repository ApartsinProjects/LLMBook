"""v6.47: Triage remaining 70 over-nest detections.

For each block flagged in python_structure_audit.csv as 'bug_pattern' but
not yet fixed by v6.44, extract the actual code and classify:

  - LEGITIMATE-CLOSURE: hook/wrapper/factory inside another function
    (signature with no `self`, takes `grad` or `*args` or specific callback args)
  - LEGITIMATE-DECORATOR: inner function defined inside outer decorator
    (preceded by `@functools.wraps` etc.)
  - LIKELY-BUG: method signature (`def name(self, ...)`) over-nested
  - AMBIGUOUS: needs manual review

Output: print classification + relevant snippet so we can decide what to fix.
"""
import csv
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CSV = ROOT / 'KDP' / 'validation' / 'python_structure_audit.csv'


def classify_block(code: str, line_in_block: int) -> tuple[str, str]:
    """Return (classification, evidence_snippet)."""
    lines = code.split('\n')
    if line_in_block - 1 >= len(lines):
        return 'UNKNOWN', ''
    target = lines[line_in_block - 1]
    target_stripped = target.lstrip()
    # Look at surrounding context: 5 lines before, 3 lines after
    ctx_start = max(0, line_in_block - 6)
    ctx_end = min(len(lines), line_in_block + 3)
    ctx = '\n'.join(lines[ctx_start:ctx_end])

    # Classification logic
    # 1. Decorator pattern: @decorator on the line just before, then `def`
    sig_match = re.match(r'(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)', target_stripped)
    if sig_match:
        name = sig_match.group(1)
        params = sig_match.group(2)
        # Check for decorator line
        prev_line = lines[line_in_block - 2] if line_in_block >= 2 else ''
        if re.search(r'@\w+', prev_line):
            return 'LEGITIMATE-DECORATOR', ctx
        # Check if it's a hook signature (grad, module, input, output)
        if re.match(r'^\s*(grad|module,\s*input|module,\s*grad)', params):
            return 'LEGITIMATE-HOOK', ctx
        # *args/**kwargs => probably wrapper
        if re.search(r'\*args|\*\*kwargs', params):
            return 'LEGITIMATE-WRAPPER', ctx
        # method with self => suspicious (could be real bug or factory method)
        if re.match(r'^\s*(self|cls)\b', params):
            return 'LIKELY-BUG (method sig)', ctx
        # def with no self, no *args, no callback signature
        # If the parent function returns this def (factory), legitimate
        # Look ahead a few lines for `return <name>` pattern
        for j in range(line_in_block, min(line_in_block + 20, len(lines))):
            if re.search(rf'return\s+{re.escape(name)}\b', lines[j]):
                return 'LEGITIMATE-FACTORY', ctx
        return 'AMBIGUOUS', ctx
    elif target_stripped.startswith('class '):
        # Inner class: could be legitimate (factory) or bug
        # Check if parent function returns the class
        cm = re.match(r'class\s+(\w+)', target_stripped)
        name = cm.group(1) if cm else ''
        if name:
            for j in range(line_in_block, min(line_in_block + 30, len(lines))):
                if re.search(rf'return\s+{re.escape(name)}\b', lines[j]):
                    return 'LEGITIMATE-FACTORY-CLASS', ctx
        return 'LIKELY-BUG (nested class)', ctx
    return 'UNKNOWN', ctx


def main():
    with CSV.open(encoding='utf-8') as f:
        rows = [r for r in csv.DictReader(f) if r['bug_pattern']]

    classes = {}
    detailed = []
    for r in rows:
        file_p = ROOT / r['file']
        offset = int(r['block_offset'])
        text = file_p.read_text(encoding='utf-8', errors='replace')
        # Extract block at offset
        m = re.search(
            r'<pre>\s*<code[^>]*lang-python[^>]*>(.+?)</code>\s*</pre>',
            text[offset:offset + 30000], re.DOTALL,
        )
        if not m:
            continue
        code = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
        line_match = re.search(r'at line (\d+)', r['bug_pattern'])
        if not line_match:
            continue
        line_in_block = int(line_match.group(1))
        cls, evidence = classify_block(code, line_in_block)
        classes[cls] = classes.get(cls, 0) + 1
        detailed.append({
            'file': r['file'],
            'bug_pattern': r['bug_pattern'],
            'classification': cls,
            'evidence': evidence,
            'block_offset': offset,
            'line_in_block': line_in_block,
        })

    print('Classification summary:')
    for cls, n in sorted(classes.items(), key=lambda x: -x[1]):
        print(f'  {n:3d}  {cls}')

    # Write detailed CSV
    out = ROOT / 'KDP' / 'validation' / 'overnest_triage.csv'
    with out.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['file', 'bug_pattern', 'classification',
                                          'block_offset', 'line_in_block', 'evidence'])
        w.writeheader()
        for d in detailed:
            d['evidence'] = d['evidence'][:300]
            w.writerow(d)
    print(f'\nTriage CSV: {out}')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
