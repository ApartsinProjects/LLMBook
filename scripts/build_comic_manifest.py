"""Extract COMIC / MENTAL-MAP imagegen prompts from comic_illustration_audit.md
into a structured manifest the generator can consume.

Each audit item looks like:
  N. COMIC <placement sentence>. ... Imagegen prompt: `"<prompt>"`
under a header:
  ### Section 34.1: The Information Extraction Landscape

Output rows: {section_path, chap_sec, kind, num, placement, prompt, alt,
caption, figure_label, filename}. Section paths are reconciled to the
current on-disk location (post-renumber) by chapter.section basename.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / 'docs' / 'content-audit' / 'comic_illustration_audit.md'
OUT = ROOT / '.book-update' / 'comic-manifest.jsonl'

# Map chapter.section -> current path by scanning section files.
def build_secmap():
    m = {}
    for p in ROOT.glob('part-*/module-*/section-*.html'):
        mm = re.match(r'^section-(\d+\.\d+)\.html$', p.name)
        if mm:
            m[mm.group(1)] = p
    return m

SECMAP = build_secmap()

HEADER_RE = re.compile(r'^###\s+Section\s+(\d+\.\d+)\s*:\s*(.+)$')
ITEM_RE = re.compile(
    r'^\s*(\d+)\.\s+(COMIC|MENTAL-MAP)\b(.*?)Imagegen prompt:\s*`"(.+?)"`\s*$'
)


def main():
    cur_sec = None
    cur_title = None
    rows = []
    text = AUDIT.read_text(encoding='utf-8')
    for line in text.splitlines():
        h = HEADER_RE.match(line)
        if h:
            cur_sec = h.group(1)
            cur_title = h.group(2).strip()
            continue
        it = ITEM_RE.match(line)
        if it and cur_sec:
            num, kind, placement, prompt = it.groups()
            sec_path = SECMAP.get(cur_sec)
            chap, sec = cur_sec.split('.')
            # next figure number is assigned at insert time; use a stable
            # filename derived from section + item number.
            slug = re.sub(r'[^a-z0-9]+', '-',
                          (cur_title or 'comic').lower()).strip('-')[:48]
            fname = f"images/comic-{cur_sec}-{num}-{slug}.jpg"
            rows.append({
                'chap_sec': cur_sec,
                'section': str(sec_path).replace('\\', '/') if sec_path else None,
                'section_exists': sec_path is not None,
                'kind': kind,
                'num': int(num),
                'placement': placement.strip().rstrip('.'),
                'prompt': prompt.strip(),
                'filename': fname,
            })
    with OUT.open('w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r) + '\n')
    present = sum(1 for r in rows if r['section_exists'])
    comic = sum(1 for r in rows if r['kind'] == 'COMIC')
    mm = sum(1 for r in rows if r['kind'] == 'MENTAL-MAP')
    print(f"Extracted {len(rows)} prompts ({comic} COMIC, {mm} MENTAL-MAP)")
    print(f"  sections resolvable on disk: {present}/{len(rows)}")
    print(f"  unresolved chap.sec: "
          + ", ".join(sorted({r['chap_sec'] for r in rows if not r['section_exists']})))
    print(f"  wrote {OUT}")


if __name__ == '__main__':
    main()
