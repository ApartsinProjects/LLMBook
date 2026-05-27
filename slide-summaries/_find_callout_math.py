"""Find math inside callout boxes in a single file."""
import re, sys
from pathlib import Path

p = Path(sys.argv[1])
text = p.read_text(encoding='utf-8')

# Find each top-level callout block and its inner math
# Use a non-greedy scan from <div class="callout *> up to the next callout or </main>
for m in re.finditer(
    r'<div class="callout [^"]+"[^>]*>(.*?)(?=<div class="callout |</main>)',
    text, re.DOTALL
):
    inner = m.group(1)
    # math signs
    has_display = '$$' in inner
    inline_iter = list(re.finditer(r'(?<!\\)\$([^\n$]{1,200}?)(?<!\\)\$', inner))
    # filter out probable HTML-entity dollar
    real_inline = [im for im in inline_iter if re.search(r'[_^{}=\\]', im.group(1))]
    if not has_display and not real_inline:
        continue
    line = text.count('\n', 0, m.start()) + 1
    title_m = re.search(r'<div class="callout-title">([^<]+)', inner)
    title = title_m.group(1) if title_m else '?'
    print(f'Line {line}: {title!r}')
    if has_display:
        for dm in re.finditer(r'\$\$([^$]+)\$\$', inner, re.DOTALL):
            print(f'  DISPLAY: {dm.group(0)[:160]}')
    for im in real_inline[:6]:
        print(f'  INLINE:  {im.group(0)[:140]}')
    print()
