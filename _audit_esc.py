import re, os, glob
roots = ['part-1-foundations','part-2-understanding-llms','part-3-working-with-llms','part-4-training-adapting','part-5-retrieval-conversation','part-6-agentic-ai','part-7-multimodal-applications','part-8-evaluation-production','part-9-safety-strategy','part-10-frontiers','part-11-idea-to-product','appendices','front-matter']
base = r'E:/Projects/BookBlogsHome/LLMBook'
files = []
for r in roots:
    files += glob.glob(os.path.join(base, r, '**', '*.html'), recursive=True)
skip = ['source_fix_backups','html2pub\\tests','temp_epub','node_modules','pagefind']

def rel(p):
    return p.replace(base,'').replace(chr(92),'/').lstrip('/')

out = []
for f in files:
    if any(s in f for s in skip): continue
    try:
        with open(f, encoding='utf-8') as fh:
            for ln, line in enumerate(fh,1):
                # \$<contains backslash-letter>$
                if re.search(r'\\\$[^$\n]*\\[a-zA-Z]+[^$\n]*\$', line):
                    out.append((rel(f), ln, line.strip()[:180]))
                elif re.search(r'\\\$1[+\-]\\?[a-zA-Z]+\$', line):
                    out.append((rel(f), ln, line.strip()[:180]))
    except: pass
print('count', len(out))
for x in out:
    print(f"{x[0]}:{x[1]} :: {x[2]}")
