"""Remove literal backslash-hyphens in part-index files (artifact of re.escape in replacement strings)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

n_files = 0
for p in sorted(ROOT.glob('part-*/index.html')):
    text = p.read_text(encoding='utf-8')
    orig = text
    # Remove literal backslashes inside module-NN-name patterns (caused by re.escape in replacement)
    text = re.sub(r'module-(\d+)-([a-z][a-z\\-]*?)/', lambda m: f'module-{m.group(1)}-{m.group(2).replace(chr(92), "")}/', text)
    if text != orig:
        p.write_text(text, encoding='utf-8')
        n_files += 1
        print(f'  Fixed: {p.relative_to(ROOT)}')

print(f'Fixed backslash artifacts in {n_files} files')
