"""Find doubled words in body text (the the, of of, etc.)."""
import os, re
base = r'E:\Projects\BookBlogsHome\LLMBook'
SKIP_DIRS = {'KDP', 'node_modules', 'pagefind', 'temp_epub', 'vendor', 'agents', 'images'}
TAG_RE = re.compile(r'<[^>]+>')
DOUBLE_RE = re.compile(r'\b(the|a|an|and|of|to|in|is|for|on|with|that|this|but|or|by|as|at|be|it|we|you)\s+\1\b', re.I)

found = []
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        try:
            content = open(path, 'r', encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        # remove style/script/code/pre blocks
        content = re.sub(r'<(style|script|pre|code)[^>]*>[\s\S]*?</\1>', '', content, flags=re.I)
        # remove math
        content = re.sub(r'\$\$[\s\S]*?\$\$', '', content)
        content = re.sub(r'\$[^$\n]+\$', '', content)
        text = TAG_RE.sub(' ', content)
        for m in DOUBLE_RE.finditer(text):
            line = content[:m.start()].count('\n') + 1
            ctx = text[max(0,m.start()-40):m.end()+40].replace('\n',' ').strip()
            found.append((os.path.relpath(path, base), line, m.group(0), ctx))

print(f"DOUBLED WORDS: {len(found)}")
for p, ln, w, c in found[:25]:
    print(f"  {p}: '{w}' :: ...{c}...")
