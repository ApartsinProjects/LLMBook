"""Fix source HTML where Python code is tagged with lang-text (no highlighting).

Detects: <pre><code class="... lang-text"> blocks whose content looks like
Python (import/def/class/return + np./torch./pandas./numpy/...).
Replaces lang-text with lang-python so syntax highlighting kicks in.
"""
from __future__ import annotations
import re, shutil, time
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path('.')
EXCLUDE = {'_archive','KDP','vendor','scripts','templates','md','node_modules','temp_epub'}

PY_KEYWORDS = re.compile(r'\b(import|def|class|return|lambda|with|for|while|if|elif|else|try|except|yield|async|await)\b')
PY_LIBS = ('np.', 'torch.', 'pd.', 'numpy', 'pandas', 'sklearn', 'transformers', 'requests.', 'json.')


def looks_like_python(text: str) -> bool:
    if not PY_KEYWORDS.search(text):
        return False
    return any(lib in text for lib in PY_LIBS)


def main():
    backup = ROOT / f'KDP/build/source_fix_backups/mislabeled_code_{time.strftime("%Y%m%d_%H%M%S")}'
    n_files = 0
    n_blocks = 0
    for p in ROOT.rglob('*.html'):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if 'lang-text' not in text:
            continue
        soup = BeautifulSoup(text, 'lxml')
        changed = 0
        for code in soup.find_all('code', class_=lambda c: c and 'lang-text' in c):
            plain = code.get_text()
            if looks_like_python(plain):
                cls = [c for c in code.get('class') or [] if c != 'lang-text']
                cls.append('lang-python')
                code['class'] = cls
                changed += 1
        if changed:
            b = backup / p.relative_to(ROOT)
            b.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, b)
            # Re-serialize body content into source file
            body = soup.find('body')
            if body is None:
                continue
            body_inner = ''.join(str(c) for c in body.children)
            new_text = text[:text.find('<body')]
            head_close = text.find('>', text.find('<body')) + 1
            body_close = text.rfind('</body>')
            new_text = text[:head_close] + '\n' + body_inner + '\n' + text[body_close:]
            p.write_text(new_text, encoding='utf-8')
            n_files += 1
            n_blocks += changed
            print(f'  {changed:>2}x  {str(p).replace(chr(92), "/")}')
    print(f'\nFixed {n_blocks} mislabeled code blocks across {n_files} files')


if __name__ == '__main__':
    main()
