"""Find $$...$$ display math blocks containing English words not wrapped in \text{} or \operatorname{}."""
import os, re
base = r'E:\Projects\BookBlogsHome\LLMBook'
SKIP_DIRS = {'KDP', 'node_modules', 'pagefind', 'temp_epub', 'vendor', 'agents'}
DD_RE = re.compile(r'\$\$([\s\S]+?)\$\$')
WORD_RE = re.compile(r'(?<![\\a-zA-Z_])(input|output|where|loss|gradient|softmax|tokens?|weights?|inputs?|outputs?|context|target|source|prompt|reward|policy|reference|baseline|sample|mean|variance|labels?|positives?|negatives?|epochs?|batch|hidden|encoder|decoder|attention|model|prediction|reference|truth)(?![a-zA-Z_{])', re.I)
ALLOW_PREFIX = re.compile(r'\\(?:text|operatorname|mathrm|mathit|mathbf|textsf|textbf|mathsf|hbox|mbox)\s*\{[^{}]*\b')

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
        for m in DD_RE.finditer(content):
            block = m.group(1)
            # strip text-wrapped content
            cleaned = re.sub(r'\\(?:text|operatorname|mathrm|mathbf|mathit|mathsf|textsf|textbf|hbox|mbox)\s*\{[^{}]*\}', '', block)
            for w in WORD_RE.finditer(cleaned):
                # find line in original
                line_no = content[:m.start()].count('\n') + 1
                snippet = block.strip().replace('\n', ' ')[:90]
                found.append((os.path.relpath(path, base), line_no, w.group(0), snippet))
                break  # one per block

# dedup
seen = set()
uniq = []
for it in found:
    key = (it[0], it[1])
    if key in seen: continue
    seen.add(key)
    uniq.append(it)

print(f"DISPLAY MATH WITH BARE WORDS: {len(uniq)}")
for p, ln, w, s in uniq[:30]:
    print(f"  {p}:{ln} bare='{w}' :: {s}")
