import re, os, glob, sys

roots = ['part-1-foundations','part-2-understanding-llms','part-3-working-with-llms','part-4-training-adapting','part-5-retrieval-conversation','part-6-agentic-ai','part-7-multimodal-applications','part-8-evaluation-production','part-9-safety-strategy','part-10-frontiers','part-11-idea-to-product','appendices','front-matter']
base = r'E:/Projects/BookBlogsHome/LLMBook'
files = []
for r in roots:
    files += glob.glob(os.path.join(base, r, '**', '*.html'), recursive=True)

skip_subs = ['KDP\\build\\source_fix_backups', 'KDP\\html2pub\\tests', '\\temp_epub\\', '\\node_modules\\', '\\pagefind\\']

def relpath(f):
    p = f.replace(base, '').replace('\\','/').lstrip('/')
    return p

mode = sys.argv[1] if len(sys.argv)>1 else 'bare_inline'

if mode == 'bare_inline':
    out = []
    for f in files:
        if any(s in f for s in skip_subs): continue
        try:
            with open(f, encoding='utf-8') as fh:
                in_pre = False
                for ln, line in enumerate(fh, 1):
                    if '<pre' in line: in_pre = True
                    if '</pre>' in line:
                        in_pre = False
                        continue
                    if in_pre: continue
                    if 'delimiters' in line or 'KaTeX' in line: continue
                    if 'left:' in line and 'right:' in line: continue
                    if 'displayMode' in line: continue
                    stripped = re.sub(r'<span class="math">\$[^$]*\$</span>', '', line)
                    stripped = re.sub(r'\$\$[^$]+?\$\$', '', stripped)
                    stripped = re.sub(r'<code[^>]*>.*?</code>', '', stripped)
                    matches = re.findall(r'(?<![\\\w$])\$([^$\n]{1,150}?)\$(?!\w)', stripped)
                    for m in matches:
                        if any(c in m for c in '\\^_{}') or (re.search(r'[a-zA-Z]', m) and len(m) > 1):
                            out.append((relpath(f), ln, m[:80]))
                            break
        except Exception:
            pass
    print(f'COUNT={len(out)}')
    for x in out[:60]:
        print(f"{x[0]}:{x[1]} :: ${x[2]}$")

elif mode == 'plainwords':
    # plain English inside $...$ display or inline (not in \text{}, \operatorname, \mathrm)
    suspect_words = ['Performance','Data','Quality','Accuracy','Cost','Memory','Latency','Throughput','Bandwidth','Compute','Energy','Area','Power','Speed','Time','Cache','Hit','Rate','Loss','Error','Score','Reward','Value','Policy','Action','State','Reward','samples','tokens','params','where','if','then','else','for','and','or','not','is','count','sum','avg','min','max','mean','std','var','dim','batch','seq','len','vocab']
    # only flag bare word patterns (CamelCase or 2+ consecutive lowercase words) inside math
    out = []
    for f in files:
        if any(s in f for s in skip_subs): continue
        try:
            with open(f, encoding='utf-8') as fh:
                content = fh.read()
            # Find math blocks
            for m in re.finditer(r'\$\$([^$]+?)\$\$', content):
                body = m.group(1)
                clean = re.sub(r'\\(text|operatorname|mathrm|mathit|mathbf|mathcal|mathbb|mathfrak)\s*\{[^{}]*\}', '', body)
                # Look for ALL CAPS or CamelCase words OR bare lowercase >=4 chars not preceded by backslash
                bad = re.findall(r'(?<!\\)(?<!\w)([A-Z][a-z]{3,}|[a-z]{4,})(?!\w)', clean)
                bad = [b for b in bad if b in suspect_words]
                if bad:
                    line = content[:m.start()].count('\n')+1
                    out.append((relpath(f), line, bad, body[:90]))
            for m in re.finditer(r'<span class="math">\$([^$]+?)\$</span>', content):
                body = m.group(1)
                clean = re.sub(r'\\(text|operatorname|mathrm|mathit|mathbf|mathcal|mathbb|mathfrak)\s*\{[^{}]*\}', '', body)
                bad = re.findall(r'(?<!\\)(?<!\w)([A-Z][a-z]{3,}|[a-z]{4,})(?!\w)', clean)
                bad = [b for b in bad if b in suspect_words]
                if bad:
                    line = content[:m.start()].count('\n')+1
                    out.append((relpath(f), line, bad, body[:90]))
        except Exception:
            pass
    print(f'COUNT={len(out)}')
    seen = set()
    for x in out:
        key = (x[0], x[1])
        if key in seen: continue
        seen.add(key)
        print(f"{x[0]}:{x[1]} :: words={x[2]} :: {x[3]}")
        if len(seen)>=40: break

elif mode == 'sigma_pi':
    # find \Sigma or \Pi misuse (should be \sum / \prod)
    out = []
    for f in files:
        if any(s in f for s in skip_subs): continue
        try:
            with open(f, encoding='utf-8') as fh:
                for ln, line in enumerate(fh,1):
                    # look for bare \Sigma or \Pi inside math
                    if re.search(r'\$[^$]*\\(Sigma|Pi)[^a-zA-Z][^$]*\$', line):
                        out.append((relpath(f), ln, line.strip()[:140]))
        except: pass
    print(f'COUNT={len(out)}')
    for x in out[:30]:
        print(f"{x[0]}:{x[1]} :: {x[2]}")

elif mode == 'bare_funcs':
    # find bare softmax/argmax/argmin/std/var/mean inside $...$ that are NOT \operatorname or \text
    out = []
    funcs = ['softmax','argmax','argmin','sigmoid','relu','tanh','LayerNorm','RMSNorm','MultiHead','Attention','Concat']
    for f in files:
        if any(s in f for s in skip_subs): continue
        try:
            with open(f, encoding='utf-8') as fh:
                content = fh.read()
            for m in re.finditer(r'\$\$?([^$]+?)\$\$?', content):
                body = m.group(1)
                # remove text/operatorname wrappers
                clean = re.sub(r'\\(text|operatorname|mathrm)\s*\{[^{}]*\}', '', body)
                for fn in funcs:
                    if re.search(r'(?<!\\)(?<!\w)' + fn + r'(?!\w)', clean):
                        line = content[:m.start()].count('\n')+1
                        out.append((relpath(f), line, fn, body[:80]))
                        break
        except: pass
    print(f'COUNT={len(out)}')
    seen=set()
    for x in out:
        key=(x[0],x[1],x[2])
        if key in seen: continue
        seen.add(key)
        print(f"{x[0]}:{x[1]} :: bare={x[2]} :: {x[3]}")
        if len(seen)>=40: break

elif mode == 'wrappers':
    # wrapper drift detection
    counts = {'div.math-block': 0, 'p.math-display': 0, 'p_dd': 0, 'bare_dd': 0}
    examples = {'p.math-display':[], 'p_dd':[], 'bare_dd':[]}
    for f in files:
        if any(s in f for s in skip_subs): continue
        try:
            with open(f, encoding='utf-8') as fh:
                lines = fh.readlines()
            for i, line in enumerate(lines, 1):
                if 'class="math-block"' in line:
                    counts['div.math-block'] += line.count('class="math-block"')
                if 'class="math-display"' in line:
                    counts['p.math-display'] += line.count('class="math-display"')
                    examples['p.math-display'].append((relpath(f), i, line.strip()[:120]))
                # <p>$$ wrapper
                if re.search(r'<p>\s*\$\$', line):
                    counts['p_dd'] += 1
                    examples['p_dd'].append((relpath(f), i, line.strip()[:120]))
                # bare $$ on its own line (line starts with $$)
                if re.match(r'^\s*\$\$', line):
                    prev = lines[i-2] if i>1 else ''
                    # Check if this $$ is opener (not closer of a 2-line block)
                    # Look at preceding line for context
                    if 'math-block' not in prev and 'class="math' not in prev and '<p>' not in prev and '<li>' not in prev and '<td>' not in prev and '<div' not in prev:
                        counts['bare_dd'] += 1
                        examples['bare_dd'].append((relpath(f), i, line.strip()[:120]))
        except: pass
    print('COUNTS:', counts)
    for k, exs in examples.items():
        print(f'\n--- {k} (n={len(exs)}) ---')
        for ex in exs[:15]:
            print(f"{ex[0]}:{ex[1]} :: {ex[2]}")

elif mode == 'esc_dollar':
    # \$X$ broken escapes
    out = []
    for f in files:
        if any(s in f for s in skip_subs): continue
        try:
            with open(f, encoding='utf-8') as fh:
                for ln, line in enumerate(fh,1):
                    if re.search(r'\\\$[^$]+\$', line):
                        out.append((relpath(f), ln, line.strip()[:140]))
        except: pass
    print(f'COUNT={len(out)}')
    for x in out[:30]:
        print(f"{x[0]}:{x[1]} :: {x[2]}")

elif mode == 'html_in_math':
    # detect <br>, <span>, <em>, <strong>, <code>, &lt;, &gt; inside math
    out = []
    for f in files:
        if any(s in f for s in skip_subs): continue
        try:
            with open(f, encoding='utf-8') as fh:
                content = fh.read()
            # check $$..$$ blocks
            for m in re.finditer(r'\$\$([\s\S]+?)\$\$', content):
                body = m.group(1)
                if re.search(r'<(br|span|em|strong|code|p|div)\b', body):
                    line = content[:m.start()].count('\n')+1
                    out.append((relpath(f), line, body[:120]))
            for m in re.finditer(r'(?<!\$)\$([^$\n]+)\$(?!\$)', content):
                body = m.group(1)
                if re.search(r'<(br|span|em|strong|code|p|div)\b', body):
                    line = content[:m.start()].count('\n')+1
                    out.append((relpath(f), line, body[:120]))
        except: pass
    print(f'COUNT={len(out)}')
    for x in out[:30]:
        print(f"{x[0]}:{x[1]} :: {x[2]}")
