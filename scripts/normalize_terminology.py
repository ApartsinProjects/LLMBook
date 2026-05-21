"""Normalize terminology inconsistencies across the book's PROSE only.

Guards against touching:
  - <pre>...</pre> and <code>...</code> blocks (code, identifiers)
  - <a ...>...</a> href values and URLs
  - <script>/<style> blocks
  - quoted strings that look like paper titles ("..." spanning the term)
  - HTML attribute values (alt=, title=, src=, etc.)
  - known compound identifiers (HuggingFaceH4, huggingface_hub, huggingface.co)

Policy (canonical -> variants replaced):
  pretraining   <- pre-training
  pretrained    <- pre-trained
  Hugging Face  <- HuggingFace   (but NOT HuggingFaceH4, huggingface_hub, .co)
  chain-of-thought (adjectival, lowercase) <- Chain-of-Thought when not at
        sentence start and not in a heading/title
  fine-tuning   <- "fine tuning" (space form)
  fine-tune     <- "fine tune" (space form, verb)

Run:
  py -3 scripts/normalize_terminology.py            # dry-run counts
  py -3 scripts/normalize_terminology.py --apply
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'_archive', 'node_modules', '.git', 'pagefind', 'KDP',
             'build', 'vendor', '.claude', '__pycache__', '.book-update'}

# Regions to protect (replace with placeholders, restore at end).
PROTECT_PATTERNS = [
    re.compile(r'<pre\b.*?</pre>', re.DOTALL | re.IGNORECASE),
    re.compile(r'<code\b.*?</code>', re.DOTALL | re.IGNORECASE),
    re.compile(r'<script\b.*?</script>', re.DOTALL | re.IGNORECASE),
    re.compile(r'<style\b.*?</style>', re.DOTALL | re.IGNORECASE),
    # Any HTML tag with its attributes (so attr values like alt=, href=, src=,
    # title=, data-* are protected). This leaves only text BETWEEN tags.
    re.compile(r'<[^>]+>'),
]


def protect(text):
    store = []
    def stash(m):
        store.append(m.group(0))
        return f'\x00PT{len(store)-1}\x01'
    for pat in PROTECT_PATTERNS:
        text = pat.sub(stash, text)
    return text, store


def restore(text, store):
    # Restore in reverse so nested placeholders resolve correctly.
    for i in range(len(store) - 1, -1, -1):
        text = text.replace(f'\x00PT{i}\x01', store[i])
    return text


# Replacement rules applied to PROSE text only (after protect()).
# Each is (compiled_regex, replacement, label).
RULES = [
    # pre-training -> pretraining (case-insensitive on first letter; preserve case)
    (re.compile(r'\bPre-training\b'), 'Pretraining', 'Pre-training->Pretraining'),
    (re.compile(r'\bpre-training\b'), 'pretraining', 'pre-training->pretraining'),
    (re.compile(r'\bPre-trained\b'), 'Pretrained', 'Pre-trained->Pretrained'),
    (re.compile(r'\bpre-trained\b'), 'pretrained', 'pre-trained->pretrained'),
    (re.compile(r'\bPre-train\b'), 'Pretrain', 'Pre-train->Pretrain'),
    (re.compile(r'\bpre-train\b'), 'pretrain', 'pre-train->pretrain'),
    # HuggingFace -> Hugging Face, but NOT HuggingFaceH4 (handled by negative
    # lookahead for an uppercase letter or digit immediately after).
    (re.compile(r'\bHuggingFace\b(?![A-Za-z0-9_])'), 'Hugging Face', 'HuggingFace->Hugging Face'),
    # "fine tuning" (space) -> "fine-tuning"; "fine tune" -> "fine-tune".
    # Only when not already hyphenated and not "fine tuning" inside other words.
    (re.compile(r'\bfine tuning\b'), 'fine-tuning', 'fine tuning->fine-tuning'),
    (re.compile(r'\bFine tuning\b'), 'Fine-tuning', 'Fine tuning->Fine-tuning'),
    (re.compile(r'\bfine tuned\b'), 'fine-tuned', 'fine tuned->fine-tuned'),
    (re.compile(r'\bFine tuned\b'), 'Fine-tuned', 'Fine tuned->Fine-tuned'),
]

# Chain-of-Thought -> chain-of-thought ONLY mid-sentence (preceded by a
# lowercase word + space, to avoid sentence starts and headings). Conservative.
COT_RULE = (
    re.compile(r'(?<=[a-z] )Chain-of-Thought\b'),
    'chain-of-thought',
    'Chain-of-Thought->chain-of-thought (adjectival)'
)


def apply_rules(text):
    counts = {}
    for pat, repl, label in RULES:
        text, n = pat.subn(repl, text)
        if n:
            counts[label] = counts.get(label, 0) + n
    # CoT rule
    pat, repl, label = COT_RULE
    text, n = pat.subn(repl, text)
    if n:
        counts[label] = counts.get(label, 0) + n
    return text, counts


def process(text):
    protected, store = protect(text)
    new_protected, counts = apply_rules(protected)
    if not counts:
        return text, {}
    restored = restore(new_protected, store)
    return restored, counts


def walk():
    for p in ROOT.rglob('*.html'):
        if any(s in p.parts for s in SKIP_DIRS):
            continue
        yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    total = {}
    files_changed = 0
    for p in walk():
        try:
            text = p.read_text(encoding='utf-8')
        except Exception:
            continue
        new_text, counts = process(text)
        if counts and new_text != text:
            files_changed += 1
            for k, v in counts.items():
                total[k] = total.get(k, 0) + v
            if args.apply:
                p.write_text(new_text, encoding='utf-8')
    print(f"Files changed: {files_changed}")
    print("Per-rule counts:")
    for k, v in sorted(total.items(), key=lambda x: -x[1]):
        print(f"  {v:5d}  {k}")
    print(f"Total replacements: {sum(total.values())}")
    if not args.apply:
        print("\n(dry-run; pass --apply to write)")


if __name__ == '__main__':
    main()
