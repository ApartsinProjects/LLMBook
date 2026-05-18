"""Wave 36a: Prefix callout titles with the canonical type word.

User policy: keep descriptive titles (more useful), BUT enforce that every
callout-title starts with the canonical type word so readers can scan callouts
at a glance.

Examples:
  <div class="callout-title">Why sort-and-blend beats ray marching</div>
  -> <div class="callout-title">Key Insight: Why sort-and-blend beats ray marching</div>

  <div class="callout-title">A/B Testing a Prompt Rewrite</div>  (inside callout practical-example)
  -> <div class="callout-title">Real-World Scenario: A/B Testing a Prompt Rewrite</div>

Idempotent: if title already starts with a canonical prefix (case-insensitive),
skip it.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups', 'pagefind',
        '.book-update', 'vendor', '.claude', '_archive', 'agents', 'templates',
        'docs', 'scripts'}

# Type -> (canonical prefix to add, list of acceptable existing prefixes)
TITLE_RULES = {
    "big-picture":        ("Big Picture",         ["big picture", "the big picture"]),
    "key-insight":        ("Key Insight",         ["key insight", "key insights"]),
    "note":               ("Note",                ["note"]),
    "warning":            ("Warning",             ["warning", "caution"]),
    "tip":                ("Tip",                 ["tip", "pro tip", "production tip"]),
    "fun-note":           ("Fun Fact",            ["fun fact", "fun note", "did you know"]),
    "exercise":           ("Exercise",            ["exercise", "challenge", "hands-on lab"]),
    "self-check":         ("Self-Check",          ["self-check", "self check", "check yourself", "quick check"]),
    "lab":                ("Lab",                 ["lab", "hands-on", "hands on"]),
    "algorithm":          ("Algorithm",           ["algorithm"]),
    "numeric-example":    ("Numeric Example",     ["numeric example", "worked example", "example"]),
    "practical-example":  ("Real-World Scenario", ["real-world scenario", "real world scenario", "practical example", "case study"]),
    "production-pattern": ("Production Pattern",  ["production pattern", "production-pattern"]),
    "research-frontier":  ("Research Frontier",   ["research frontier", "open question", "open questions", "frontier"]),
    "library-shortcut":   ("Library Shortcut",    ["library shortcut", "shortcut", "library:"]),
    "cross-ref":          ("Cross-Reference",     ["cross-reference", "cross reference", "see also", "canonical reference", "related"]),
    "looking-back":       ("Looking Back",        ["looking back", "recap", "review"]),
    "postmortem":         ("Postmortem",          ["postmortem", "post-mortem", "incident", "lessons learned"]),
    "pathway":            ("Learning Objectives", ["learning objective", "pathway", "objectives"]),
    "thesis-thread":      ("Thesis Thread",       ["thesis thread", "thesis"]),
    "whats-next":         ("What's Next",         ["what's next", "what comes next", "whats next", "next:"]),
}

CALLOUT_BLOCK = re.compile(
    r'(<div\s+class="callout\s+([a-z-]+)"[^>]*>\s*'
    r'<div\s+class="callout-title"[^>]*>)(.*?)(</div>)',
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r'<[^>]+>')


def fix(text: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        prefix_tag = m.group(1)
        ctype = m.group(2).lower()
        title_inner = m.group(3)
        close_tag = m.group(4)
        rule = TITLE_RULES.get(ctype)
        if not rule:
            return m.group(0)
        canonical, accepted = rule
        plain_title = TAG_RE.sub('', title_inner).strip()
        if not plain_title:
            return m.group(0)  # empty title - skip
        lower = plain_title.lower()
        if any(lower.startswith(a) for a in accepted):
            return m.group(0)  # already canonical
        # Prepend
        new_title_inner = f'{canonical}: {title_inner.strip()}'
        return prefix_tag + new_title_inner + close_tag
    return CALLOUT_BLOCK.subn(repl, text)


def main():
    n_files = 0
    n_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        new, n = fix(text)
        if n > 0 and new != text:
            p.write_text(new, encoding='utf-8')
            n_files += 1
            n_total += n
    print(f'Prefixed {n_total} callout titles in {n_files} files')


if __name__ == '__main__':
    main()
