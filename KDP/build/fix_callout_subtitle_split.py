"""Split long callout titles of the form `LABEL: rest-of-title` into
`<div class="callout-title">LABEL</div>` plus a separate
`<div class="callout-subtitle">rest-of-title</div>`.

ROOT CAUSE
  Many callouts (e.g. "Real-World Scenario: Token-Aware Prompt Engineering
  Cuts API Costs by 40%") put the whole sentence inside a single
  `<div class="callout-title">`. Because the CSS makes the entire title
  element bold + uppercase, the eBook reader sees a wall of bold text
  where only the short label should be emphasized.

DETECTION
  <div class="callout-title">LABEL: rest-of-title</div>
  where:
    - total title text > 60 chars
    - the colon is in the first 60 chars of the text
    - LABEL is a short word or 2-5 word phrase that matches
      [A-Za-z][A-Za-z0-9 \\-]+?  before the colon
    - the block does NOT already have a sibling <div class="callout-subtitle">

FIX
  Replace with:
    <div class="callout-title">LABEL</div>
    <div class="callout-subtitle">rest-of-title</div>

  Also append a matching `.callout-subtitle` rule to
  `KDP/build/epub_overrides.css` (right after the existing `.callout-title`
  rule) if not already present.

This complements `fix_long_callout_titles.py` which targets only the
formal Algorithm / Theorem / Definition / etc. callouts.

Idempotent: skip blocks already followed by a `.callout-subtitle` div.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CSS_PATH = Path(__file__).resolve().parent / "epub_overrides.css"

SKIP_DIRS = {"KDP", "node_modules", ".git", "source_fix_backups", "_archive"}

# Labels whose colon-splits we should NOT touch because the dedicated
# fix_long_callout_titles.py handles them with renumbering logic.
DEDICATED_LABELS = {
    "algorithm", "theorem", "definition", "proposition",
    "lemma", "proof", "example", "claim",
}

# The pattern: opening div, label group, colon (with optional whitespace),
# rest of title, closing div. The label allows multiple words.
# Note: we deliberately keep the regex permissive on inner HTML inside
# the title, but stop at `:` (the first colon) for splitting.
TITLE_RE = re.compile(
    r'(<div class="callout-title">)(.+?)(</div>)',
    re.DOTALL,
)

# Match the first colon NOT inside an HTML tag.
def _find_first_colon(title_inner: str) -> int:
    in_tag = False
    for i, c in enumerate(title_inner):
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif c == ":" and not in_tag:
            return i
    return -1


def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def _is_valid_label(label_text: str) -> bool:
    """A label is something like 'Tip', 'Real-World Scenario', 'Numeric Example',
    'Key Insight', 'Warning' --- a short prefix that classifies the callout.
    """
    label_text = label_text.strip()
    if not label_text:
        return False
    if len(label_text) > 60:
        return False
    # Reject if the label looks like a sentence already (ends with .!?)
    if label_text[-1] in ".!?":
        return False
    # Must start with an ASCII letter
    if not re.match(r"^[A-Za-z]", label_text):
        return False
    # All characters allowed in a label: letters, digits, spaces, hyphens,
    # single quotes ("What's Next"), slashes ("HOW/WHY"), parens.
    if not re.match(r"^[A-Za-z][A-Za-z0-9 \-/'()]*$", label_text):
        return False
    # Label is at most 6 words to avoid eating real sentences
    if len(label_text.split()) > 6:
        return False
    return True


def patch_file(path: Path) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    changes: list[str] = []

    def repl(m: re.Match) -> str:
        open_tag = m.group(1)
        inner = m.group(2)
        close_tag = m.group(3)
        full = m.group(0)

        # Idempotence: if a sibling callout-subtitle already exists right
        # after this title, skip. Cheap heuristic: look at the next 120
        # chars in `text` after the match end for the subtitle marker.
        end = m.end()
        tail = text[end:end + 200]
        if tail.lstrip().startswith('<div class="callout-subtitle">'):
            return full

        # Compute text length of title (without HTML tags)
        title_text = _strip_tags(inner).strip()
        if len(title_text) <= 60:
            return full

        # Find first colon outside of any tag
        colon_pos = _find_first_colon(inner)
        if colon_pos < 0:
            return full

        label_raw = inner[:colon_pos]
        rest_raw = inner[colon_pos + 1:].lstrip()
        if not rest_raw:
            return full

        # The label portion's plain text must look like a label
        label_text = _strip_tags(label_raw).strip()
        if not _is_valid_label(label_text):
            return full

        # Skip labels already handled by fix_long_callout_titles.py
        if label_text.split()[0].lower() in DEDICATED_LABELS:
            return full

        # The colon must occur within the first 60 chars of text
        if len(label_text) > 60:
            return full

        # Subtitle text must have meaningful length
        rest_text = _strip_tags(rest_raw).strip()
        if len(rest_text) < 4:
            return full

        changes.append(
            f"split: {label_text!r} + subtitle ({len(rest_text)} chars)"
        )
        return (
            f'{open_tag}{label_raw}{close_tag}\n'
            f'<div class="callout-subtitle">{rest_raw}</div>'
        )

    new_text = TITLE_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return len(changes), changes
    return 0, []


CSS_RULE = """
/* v17: callout subtitle (auto-split from long callout-title).
 * The label stays bold / uppercase via .callout-title; the descriptive
 * sentence becomes a quieter italic subtitle so the reader is not hit
 * with a wall of bold text. */
.callout-subtitle {
    font-weight: normal !important;
    font-style: italic !important;
    font-size: 0.95em !important;
    margin: 0.2em 0 0.4em !important;
    color: #444 !important;
}
"""


def ensure_css_rule() -> bool:
    """Add the .callout-subtitle rule to epub_overrides.css if not present."""
    css = CSS_PATH.read_text(encoding="utf-8")
    if ".callout-subtitle {" in css:
        return False
    # Insert right after the first .callout-title { ... } block at line ~247
    pattern = re.compile(
        r"(\.callout-title\s*\{[^}]*\})",
        re.DOTALL,
    )
    m = pattern.search(css)
    if not m:
        # Fallback: append at end
        CSS_PATH.write_text(css.rstrip() + "\n" + CSS_RULE, encoding="utf-8")
        return True
    insertion_point = m.end()
    new_css = css[:insertion_point] + "\n" + CSS_RULE + css[insertion_point:]
    CSS_PATH.write_text(new_css, encoding="utf-8")
    return True


def main() -> int:
    total_files = 0
    total_mod = 0
    total_fixes = 0
    for path in ROOT.rglob("section-*.html"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        total_files += 1
        try:
            n, changes = patch_file(path)
        except Exception as e:
            print(f"ERR {rel}: {e}", file=sys.stderr)
            continue
        if n:
            total_mod += 1
            total_fixes += n
            print(f"  {n:3d}  {rel}")
            for c in changes[:5]:
                print(f"          {c}")
            if len(changes) > 5:
                print(f"          ... and {len(changes) - 5} more")

    css_added = ensure_css_rule()
    print()
    print(f"Files scanned:    {total_files}")
    print(f"Files modified:   {total_mod}")
    print(f"Subtitles created:{total_fixes}")
    print(f"CSS rule added:   {css_added}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
