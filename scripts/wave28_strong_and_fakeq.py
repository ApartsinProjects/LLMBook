"""Wave 28: fix unmatched <strong><strong>X</strong> bleeding bold formatting
+ convert known fake callouts to canonical form.

ROOT CAUSE (bold-bleed): Wave 17c wrapped figure/table/code-fragment captions
with double <strong>...</strong>. Earlier Wave 17L collapsed
<strong><strong>X</strong></strong> → <strong>X</strong> but only when BOTH
sides were doubled. In cases where only the opening <strong> was doubled
and the closing was single, the collapse didn't fire, leaving 1,509 unmatched
<strong><strong>X</strong> patterns. Browsers leave the second <strong>
"open" until the next block close, making the rest of the caption / paragraph
bold (the "23.2.232.5 text is bold" complaint).

Fix: pattern '<strong><strong>X</strong>' (where there's no matching closing
<strong>) → '<strong>X</strong>'. We detect by looking for double-open without
double-close in the same line/caption window.

Plus: convert the 2 fake callouts identified by Wave 24 in Ch 34.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}


def fix_unmatched_strong(text: str) -> tuple[str, int]:
    n = 0

    # Case 1: <strong><strong>X</strong></strong> (already handled but recheck)
    while True:
        new = re.sub(
            r'<strong><strong>([\s\S]*?)</strong></strong>',
            r'<strong>\1</strong>',
            text,
        )
        if new == text:
            break
        text = new

    # Case 2: <strong><strong>X</strong> without a matching second </strong>
    # Heuristic: if we see <strong><strong>...</strong> on a line, and the
    # next </strong> (if any) comes after a block-closing tag, then strip
    # one <strong>.
    # Practically simpler: when the inner text after the first </strong>
    # contains no further <strong>...</strong> pair before the next block
    # close (</figcaption>, </p>, </li>, </div>, </td>, </h1>...</h6>),
    # the opening was unmatched.
    def replace_unmatched(m):
        nonlocal n
        whole = m.group(0)
        x = m.group(1)
        after = m.group(2)
        # If 'after' has a </strong> before any block-close, leave as-is.
        # Find the first occurrence of </strong> or </figcaption>/</p>/etc.
        block_close = re.search(
            r'(</strong>|</figcaption>|</p>|</li>|</div>|</td>|</th>|</h[1-6]>|</caption>)',
            after,
        )
        if not block_close:
            return whole
        if block_close.group(1) == '</strong>':
            # Properly matched, leave alone
            return whole
        # Unmatched — drop the outer <strong>
        n += 1
        return f'<strong>{x}</strong>{after}'

    text = re.sub(
        r'<strong><strong>([\s\S]*?)</strong>([\s\S]{0,800})',
        replace_unmatched,
        text,
    )
    return text, n


def fix_fake_callouts_ch34(text: str, path: str) -> tuple[str, int]:
    """Two fake callouts from Wave 24 audit."""
    n = 0
    if 'module-34-structured-information-extraction-ner/section-34.1.html' in path:
        # Line 29: "<p><strong>Why hybrid information extraction </strong>is the
        # production standard. ...</p>" — wrap as key-insight callout
        old = (
            '<p><strong>Why hybrid information extraction </strong>is the production standard. '
            'Pure classical IE (spaCy, CRF models) is fast and precise but rigid: it can only '
            'extract entity types it was trained on. Pure LLM-based IE is flexible but '
            'expensive, slow, and prone to hallucinating entities that do not exist in the '
            'source text. The hybrid approach uses classical NLP for well-defined, '
            'high-volume entity types (dates, names, addresses) and reserves the LLM for '
            'novel or complex extraction tasks (sentiment-bearing phrases, implicit '
            'relationships, domain-specific entities). This mirrors the general hybrid '
            'philosophy from <a href="../../part-3-working-with-llms/module-13-hybrid-ml-llm/'
            'section-13.3.html">Section 13.3</a>: use the cheapest tool that can do the job '
            'correctly, and escalate to the expensive tool only when needed.</p>'
        )
        new = (
            '<div class="callout key-insight">\n'
            '<div class="callout-title">Why Hybrid IE Is the Production Standard</div>\n'
            '<p>Pure classical IE (spaCy, CRF models) is fast and precise but rigid: it can '
            'only extract entity types it was trained on. Pure LLM-based IE is flexible but '
            'expensive, slow, and prone to hallucinating entities that do not exist in the '
            'source text. The hybrid approach uses classical NLP for well-defined, '
            'high-volume entity types (dates, names, addresses) and reserves the LLM for '
            'novel or complex extraction tasks (sentiment-bearing phrases, implicit '
            'relationships, domain-specific entities). This mirrors the general hybrid '
            'philosophy from <a href="../../part-3-working-with-llms/module-13-hybrid-ml-llm/'
            'section-13.3.html">Section 13.3</a>: use the cheapest tool that can do the job '
            'correctly, and escalate to the expensive tool only when needed.</p>\n'
            '</div>'
        )
        if old in text:
            text = text.replace(old, new)
            n += 1

    if 'module-34-structured-information-extraction-ner/section-34.3.html' in path:
        # Convert "<strong>Why this matters for production pipelines.</strong>" prose
        # into big-picture or key-insight callout (whichever first paragraph after).
        # The agent's report identified line 28; let me look for the pattern with strong-led
        # start. Use a conservative regex: convert leading paragraph if it starts with
        # <strong>Why this matters</strong>
        m = re.search(
            r'<p><strong>Why this matters([^<]*)</strong>([\s\S]*?)</p>',
            text,
            count=0 if False else 1,
        ) if False else re.search(
            r'<p><strong>Why this matters([^<]*)</strong>([\s\S]*?)</p>',
            text,
        )
        if m:
            after = m.group(2).strip()
            new_block = (
                '<div class="callout big-picture">\n'
                '<div class="callout-title">Why This Matters for Production Pipelines</div>\n'
                f'<p>{after}</p>\n'
                '</div>'
            )
            text = text[:m.start()] + new_block + text[m.end():]
            n += 1
    return text, n


def main():
    n_strong_files = 0
    n_strong_total = 0
    n_fake_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text

        text, n_strong = fix_unmatched_strong(text)
        if n_strong > 0:
            n_strong_files += 1
            n_strong_total += n_strong

        text, n_fake = fix_fake_callouts_ch34(text, str(p))
        if n_fake > 0:
            n_fake_files += 1

        if text != orig:
            p.write_text(text, encoding='utf-8')

    print(f'Unmatched <strong> openings collapsed: {n_strong_total} in {n_strong_files} files')
    print(f'Fake callouts converted (Ch 34): {n_fake_files} files')


if __name__ == '__main__':
    main()
