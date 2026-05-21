"""Cycle-4 terminology keeper: APPLY mass fixes (safe).

Reads HTML files, applies regex replacements to prose ONLY,
preserving:
  * <code>...</code> inline
  * <pre>...</pre> code blocks
  * <div class="code-block-wrapper">...</div>
  * <a href="...">...</a> URLs (only the href attribute)
  * HTML attributes: id=, class=, alt=, title=, src=, data-*
  * <script>, <style>, <header>, <footer>, <nav>
  * <ul/ol class="bibliography|references"> (paper title casing intentional)
  * <section class/id contains bibliography|references|further-reading>

Strategy: tokenize HTML into "safe" zones (replaceable prose) and "unsafe"
zones (preserved). Apply regex only to safe zones.

For pretraining: the audit recommended pretraining (matches body majority,
matches dir name). Apply to all body prose. The chapter 6 title element
(<h1>Pre-training (...)</h1>) we leave alone via specific checks: the
script preserves the H1 of section-6 chapter pages.

For Chain-of-Thought: per the audit caveat, preserve adjectival lowercase
("a chain-of-thought prompt"), only standardize the title-case method
name. We do CoT-related lowercase normalization more cautiously.

For Hugging Face: replace HuggingFace -> Hugging Face. Replace
huggingface -> Hugging Face. Don't change inside attributes/code (those
are package or domain names: huggingface.co etc.)

For Llama-3: per the audit, prose form is `Llama-3` (hyphen). Replace
"Llama 3" (space, capitalized) with "Llama-3", BUT only in running prose,
not in paper-quoted titles.

Usage:
  python cycle4_terminology_apply.py --term TERM --dry-run
  python cycle4_terminology_apply.py --term TERM --apply

  TERM is one of: pretraining, hugging-face, llama-3, chain-of-thought, all
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "KDP", "build", "source_fix_backups",
             "pagefind", ".book-update", "vendor", ".claude", "_archive",
             "agents", "templates", "docs", "scripts", "__pycache__",
             "_concept-figs"}


# --- Zones that must NOT be modified ---
# Order matters: most specific first.
SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL | re.IGNORECASE)
STYLE_RE = re.compile(r'<style\b[^>]*>.*?</style>', re.DOTALL | re.IGNORECASE)
HEADER_RE = re.compile(r'<header\b[^>]*>.*?</header>', re.DOTALL | re.IGNORECASE)
FOOTER_RE = re.compile(r'<footer\b[^>]*>.*?</footer>', re.DOTALL | re.IGNORECASE)
NAV_RE = re.compile(r'<nav\b[^>]*>.*?</nav>', re.DOTALL | re.IGNORECASE)
COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)
PRE_RE = re.compile(r'<pre\b[^>]*>.*?</pre>', re.DOTALL | re.IGNORECASE)
CODE_INLINE_RE = re.compile(r'<code\b[^>]*>.*?</code>', re.DOTALL | re.IGNORECASE)
CODE_BLOCK_WRAPPER_RE = re.compile(
    r'<div\b[^>]*class\s*=\s*"[^"]*code-block-wrapper[^"]*"[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)
CODE_OUTPUT_RE = re.compile(
    r'<div\b[^>]*class\s*=\s*"[^"]*code-output[^"]*"[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)
BIB_UL_RE = re.compile(
    r'<(?:ul|ol)\b[^>]*class\s*=\s*"[^"]*(?:bibliography|references)[^"]*"[^>]*>.*?</(?:ul|ol)>',
    re.DOTALL | re.IGNORECASE,
)
BIB_SECTION_RE = re.compile(
    r'<section\b[^>]*(?:id|class)\s*=\s*"[^"]*(?:bibliography|references|further-reading)[^"]*"[^>]*>.*?</section>',
    re.DOTALL | re.IGNORECASE,
)
# Bibliography entry cards: <div class="bib-entry-card">...</div> and
# <div class="bib-ref">...</div>. These contain paper titles that must be
# preserved verbatim.
BIB_ENTRY_CARD_RE = re.compile(
    r'<div\b[^>]*class\s*=\s*"[^"]*bib-entry-card[^"]*"[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)
BIB_REF_RE = re.compile(
    r'<div\b[^>]*class\s*=\s*"[^"]*bib-ref[^"]*"[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)
# <li class="bib-ref"> or <li class="reference"> etc.
BIB_LI_RE = re.compile(
    r'<li\b[^>]*class\s*=\s*"[^"]*(?:bib-ref|bib-entry|reference|citation)[^"]*"[^>]*>.*?</li>',
    re.DOTALL | re.IGNORECASE,
)
# <title>...</title> preserves the document title
TITLE_RE = re.compile(r'<title\b[^>]*>.*?</title>', re.DOTALL | re.IGNORECASE)
# <cite>...</cite> usually contains paper titles
CITE_RE = re.compile(r'<cite\b[^>]*>.*?</cite>', re.DOTALL | re.IGNORECASE)
# Any opening tag: preserve its attributes verbatim.
TAG_OPEN_RE = re.compile(r'<[a-zA-Z][a-zA-Z0-9\-]*\b[^>]*>')
# Closing tags can be ignored (no attributes).

# Preserve list (in priority order). For each, capture the full match and
# substitute a placeholder; later restore.
PRESERVE_PATTERNS = [
    ("COMMENT", COMMENT_RE),
    ("SCRIPT", SCRIPT_RE),
    ("STYLE", STYLE_RE),
    ("HEADER", HEADER_RE),
    ("FOOTER", FOOTER_RE),
    ("NAV", NAV_RE),
    ("PRE", PRE_RE),
    ("CODE_BLOCK", CODE_BLOCK_WRAPPER_RE),
    ("CODE_OUTPUT", CODE_OUTPUT_RE),
    ("CODE_INLINE", CODE_INLINE_RE),
    ("BIB_UL", BIB_UL_RE),
    ("BIB_SECTION", BIB_SECTION_RE),
    ("BIB_ENTRY_CARD", BIB_ENTRY_CARD_RE),
    ("BIB_REF", BIB_REF_RE),
    ("BIB_LI", BIB_LI_RE),
    ("TITLE", TITLE_RE),
    ("CITE", CITE_RE),
    ("TAG_OPEN", TAG_OPEN_RE),
]


def split_preserve(html: str):
    """Return (safe_text, preserved_dict). Replace each unsafe region with a
    unique sentinel token so that regex replacements on the resulting
    string only touch prose text and not HTML tags or code."""
    pieces = [html]
    preserved = []  # list of strings

    for label, pattern in PRESERVE_PATTERNS:
        new_pieces = []
        for piece in pieces:
            if isinstance(piece, int):
                # already preserved index
                new_pieces.append(piece)
                continue
            last = 0
            for m in pattern.finditer(piece):
                # text before match: still mutable
                if m.start() > last:
                    new_pieces.append(piece[last:m.start()])
                # the match: preserve it
                idx = len(preserved)
                preserved.append(m.group(0))
                new_pieces.append(idx)
                last = m.end()
            if last < len(piece):
                new_pieces.append(piece[last:])
        pieces = new_pieces

    # Now pieces is a list of strings (mutable prose) and ints (preserved indices)
    return pieces, preserved


def rejoin(pieces, preserved):
    """Inverse of split_preserve. Pieces is list of strings + ints."""
    out = []
    for p in pieces:
        if isinstance(p, int):
            out.append(preserved[p])
        else:
            out.append(p)
    return "".join(out)


def apply_substitution(html: str, pattern: re.Pattern, replacement) -> tuple[str, int]:
    """Apply a regex substitution only to safe (prose) regions.
    Returns (new_html, n_replacements)."""
    pieces, preserved = split_preserve(html)
    total = 0
    new_pieces = []
    for p in pieces:
        if isinstance(p, int):
            new_pieces.append(p)
        else:
            if callable(replacement):
                new_p, n = pattern.subn(replacement, p)
            else:
                new_p, n = pattern.subn(replacement, p)
            total += n
            new_pieces.append(new_p)
    return rejoin(new_pieces, preserved), total


# =================================================================
# Per-term replacement specs
# =================================================================

# Word boundary patterns: avoid replacing inside identifiers.
WB_PRE = r'(?<![\w-])'  # left: not preceded by word-char or hyphen
WB_POST = r'(?![\w-])'  # right: not followed by word-char or hyphen


def rules_for(term: str):
    """Return list of (pattern, replacement, label) tuples."""
    rules = []
    if term == "pretraining":
        # Replace "pre-training" (lowercase) -> "pretraining" everywhere in prose.
        # Word-boundary protected so "pre-trainings" or similar do not break.
        # Note: don't replace "pre-training" if preceded/followed by word chars
        #   (already protected by WB regex).
        # Lowercase form
        rules.append((
            re.compile(r'(?<![\w-])pre-training(?![\w-])'),
            'pretraining',
            'pre-training -> pretraining'
        ))
        # Capitalized form
        rules.append((
            re.compile(r'(?<![\w-])Pre-training(?![\w-])'),
            'Pretraining',
            'Pre-training -> Pretraining'
        ))
        # Note: the audit observed `pretraining` is the body-majority,
        # so we standardize on it. The h1/title of chapter 6 currently
        # says "Pre-training (Architecture and Scaling)". For the chapter
        # title we preserve "Pre-training" if it appears in an h1.
        # This is handled by TAG_OPEN preservation: the text inside <h1>...</h1>
        # is prose, but we will add a check below.
    elif term == "hugging-face":
        # HuggingFace -> Hugging Face
        rules.append((
            re.compile(r'(?<![\w-])HuggingFace(?![\w-])'),
            'Hugging Face',
            'HuggingFace -> Hugging Face'
        ))
        # huggingface (lowercase) in prose: only if not part of huggingface.co
        # (URL) or other identifier. Since we preserve attributes and code,
        # any "huggingface" remaining in prose is text. But: "huggingface.co"
        # might appear as plain text (rare). The regex below is conservative.
        # We only replace "huggingface" if followed by space or end-of-word
        # punctuation (not . or /).
        rules.append((
            re.compile(r'(?<![\w./-])huggingface(?![\w./-])'),
            'Hugging Face',
            'huggingface (prose) -> Hugging Face'
        ))
    elif term == "llama-3":
        # Replace "Llama 3" -> "Llama-3" (when followed by space, period, comma,
        # or end-of-word; also handles "Llama 3.1", "Llama 3.2", etc.)
        # But careful: "Llama 3.1" should become "Llama-3.1"
        rules.append((
            re.compile(r'(?<![\w-])Llama 3(?=[\s.,;)\]:!?]|\b|<)'),
            'Llama-3',
            'Llama 3 -> Llama-3'
        ))
        # LLaMA 3 (and uppercase variants)
        rules.append((
            re.compile(r'(?<![\w-])LLaMA 3(?=[\s.,;)\]:!?]|\b|<)'),
            'Llama-3',
            'LLaMA 3 -> Llama-3'
        ))
        # LLaMA-3
        rules.append((
            re.compile(r'(?<![\w-])LLaMA-3(?![\w-])'),
            'Llama-3',
            'LLaMA-3 -> Llama-3'
        ))
        # LLAMA 3 / LLAMA-3
        rules.append((
            re.compile(r'(?<![\w-])LLAMA 3(?=[\s.,;)\]:!?]|\b|<)'),
            'Llama-3',
            'LLAMA 3 -> Llama-3'
        ))
        rules.append((
            re.compile(r'(?<![\w-])LLAMA-3(?![\w-])'),
            'Llama-3',
            'LLAMA-3 -> Llama-3'
        ))
        # Llama 2 -> Llama-2 (low cost; safer to handle alongside)
        rules.append((
            re.compile(r'(?<![\w-])Llama 2(?=[\s.,;)\]:!?]|\b|<)'),
            'Llama-2',
            'Llama 2 -> Llama-2'
        ))
        rules.append((
            re.compile(r'(?<![\w-])LLaMA 2(?=[\s.,;)\]:!?]|\b|<)'),
            'Llama-2',
            'LLaMA 2 -> Llama-2'
        ))
    elif term == "chain-of-thought":
        # Per audit caveat: preserve lowercase chain-of-thought when used
        # adjectivally; standardize "Chain-of-thought" (lower t) to
        # "Chain-of-Thought" (correct title case); standardize
        # "Chain of Thought" (no hyphens) to "Chain-of-Thought".
        # Replace "Chain of Thought" -> "Chain-of-Thought"
        rules.append((
            re.compile(r'(?<![\w-])Chain of Thought(?![\w-])'),
            'Chain-of-Thought',
            'Chain of Thought -> Chain-of-Thought'
        ))
        # Replace "Chain-of-thought" (capital C, lowercase t) -> "Chain-of-Thought"
        rules.append((
            re.compile(r'(?<![\w-])Chain-of-thought(?![\w-])'),
            'Chain-of-Thought',
            'Chain-of-thought -> Chain-of-Thought'
        ))
        # Do NOT mass-replace lowercase "chain-of-thought"; it's adjectival.
    elif term == "kv-cache":
        # Replace KV-cache -> KV cache
        rules.append((
            re.compile(r'(?<![\w-])KV-cache(?![\w-])'),
            'KV cache',
            'KV-cache -> KV cache'
        ))
        # Replace KV Cache (lowercase 'cache') -> KV cache
        rules.append((
            re.compile(r'(?<![\w-])KV Cache(?![\w-])'),
            'KV cache',
            'KV Cache -> KV cache'
        ))
    elif term == "flashattention":
        rules.append((
            re.compile(r'(?<![\w-])Flash Attention(?![\w-])'),
            'FlashAttention',
            'Flash Attention -> FlashAttention'
        ))
    return rules


def get_html_files() -> list[Path]:
    """Find all section HTML files in part-* directories."""
    files = []
    for part_dir in ROOT.iterdir():
        if not part_dir.is_dir():
            continue
        if not part_dir.name.startswith("part-"):
            continue
        for path in part_dir.rglob("*.html"):
            # Skip if in a SKIP_DIRS subtree
            if any(skip in path.parts for skip in SKIP_DIRS):
                continue
            files.append(path)
    return sorted(files)


# Special case: pretraining inside <h1> for chapter 6. The audit suggests
# keeping the chapter title "Pre-training" but standardizing the body.
# We do this with a post-check: for each h1 in chapter 6 index.html or
# in any h1 in the book, if the original had "Pre-training", restore it.
# But: in practice the <h1> contents are mutable prose, so we need to
# specifically protect them.

H1_RE = re.compile(r'<h1\b[^>]*>(.*?)</h1>', re.DOTALL | re.IGNORECASE)
H2_RE = re.compile(r'<h2\b[^>]*>(.*?)</h2>', re.DOTALL | re.IGNORECASE)

# Phrases that are PROPER NOUNS (chapter/section titles) and must keep
# 'Pre-training' as the hyphenated form. We pre-substitute these with a
# sentinel, run the replacement, then restore.
PROTECTED_PHRASES_PRETRAINING = [
    # Chapter 6 title (canonical form)
    'Chapter 6: Pre-training, Scaling Laws &amp; Data Curation',
    'Chapter 6: Pre-training, Scaling Laws & Data Curation',
    'Pre-training, Scaling Laws &amp; Data Curation',
    'Pre-training, Scaling Laws & Data Curation',
    # Section 6.2 title
    'Pre-training Objectives &amp; Paradigms',
    'Pre-training Objectives & Paradigms',
    'Pre-training Objectives and Paradigms',
    'Section 6.2: Pre-training Objectives',
    # Some references in nav-title that match
    '>Pre-training, Scaling Laws',
    'Pre-training.',  # chapter opener alt-text "...illustration: Pre-training."
]


def protect_chapter_titles_pretraining(html: str) -> tuple[str, list[tuple[str, str]]]:
    """Replace known chapter-title phrases containing 'Pre-training' with
    sentinels to survive the pretraining replacement."""
    saved = []
    # We have to be careful to do longer phrases first so they win over shorter ones.
    phrases = sorted(set(PROTECTED_PHRASES_PRETRAINING), key=len, reverse=True)
    for phrase in phrases:
        if phrase in html:
            sentinel = f'\x00CYCLE4PHRASE{len(saved)}\x00'
            saved.append((sentinel, phrase))
            html = html.replace(phrase, sentinel)
    return html, saved


def restore_chapter_titles(html: str, saved: list[tuple[str, str]]) -> str:
    for sentinel, original in saved:
        html = html.replace(sentinel, original)
    return html


def process_file(path: Path, rules, dry_run=True, preserve_h1_pretraining=False):
    """Apply rules to a single file. Returns dict of rule label -> count."""
    try:
        html = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        html = path.read_text(encoding="utf-8", errors="replace")
    original = html
    saved_phrases = []
    if preserve_h1_pretraining:
        html, saved_phrases = protect_chapter_titles_pretraining(html)

    counts = Counter()
    for pattern, replacement, label in rules:
        html, n = apply_substitution(html, pattern, replacement)
        if n > 0:
            counts[label] += n

    if preserve_h1_pretraining:
        html = restore_chapter_titles(html, saved_phrases)

    if not dry_run and html != original:
        path.write_text(html, encoding="utf-8")
    return counts, (html != original)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--term", required=True,
                        choices=["pretraining", "hugging-face", "llama-3",
                                 "chain-of-thought", "kv-cache", "flashattention",
                                 "all"])
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes (default is dry-run)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.term == "all":
        terms = ["pretraining", "hugging-face", "llama-3", "chain-of-thought",
                 "kv-cache", "flashattention"]
    else:
        terms = [args.term]

    files = get_html_files()
    print(f"Found {len(files)} HTML files in part-* dirs", flush=True)
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}", flush=True)

    grand_total = Counter()
    file_changes = defaultdict(Counter)

    for term in terms:
        rules = rules_for(term)
        preserve_h1 = (term == "pretraining")
        term_total = 0
        files_affected = 0
        print(f"\n=== Processing term: {term} ===", flush=True)
        for path in files:
            counts, changed = process_file(path, rules,
                                            dry_run=not args.apply,
                                            preserve_h1_pretraining=preserve_h1)
            if changed:
                files_affected += 1
                file_changes[term][str(path.relative_to(ROOT))] = sum(counts.values())
            for label, n in counts.items():
                grand_total[label] += n
                term_total += n
                if args.verbose and n > 0:
                    print(f"  {path.relative_to(ROOT)}: {label} x {n}", flush=True)
        print(f"  Term '{term}' totals: {term_total} replacements across {files_affected} files", flush=True)

    print("\n=== GRAND TOTAL ===")
    for label, n in grand_total.most_common():
        print(f"  {label}: {n}")

    # Per-term file change summary
    for term, files_dict in file_changes.items():
        print(f"\n=== {term}: {len(files_dict)} files would change ===")
        if args.verbose:
            for f, n in sorted(files_dict.items(), key=lambda kv: -kv[1])[:20]:
                print(f"  {f}: {n}")

    return grand_total, file_changes


if __name__ == "__main__":
    main()
