"""v6.18: Replace HTML-span breadcrumb with plain-text breadcrumb.

PROBLEM
v6.17 prepended a styled span to result.meta.title:
   "<span class=\"pf-crumb\">Part 2 › Ch 6</span> Title"
But Pagefind UI 1.5.x HTML-escapes the title before rendering, so users
see the literal markup: "<span class==>...</span> Title".

FIX
Use a plain-text breadcrumb prefix. No HTML. The breadcrumb shows as text
inside the result link itself, distinguished by surrounding brackets and
a unicode chevron:
   "[Part 2 › Ch 6] Title"

Pagefind UI prints meta.title via textContent (effectively) so plain text
renders correctly. To keep the prefix visually muted, add a CSS rule that
matches the bracket-prefixed text using a `::before`-style trick is NOT
possible because we can't target a text node. So we accept default styling
for the prefix; brackets make it visually scannable enough.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

OLD_PROCESS = re.compile(
    r'processResult: function \(result\) \{\s*'
    r'try \{\s*'
    r'var part = \(result && result\.meta && result\.meta\.part\) \? result\.meta\.part : "";\s*'
    r'var chap = \(result && result\.meta && result\.meta\.chapter\) \? result\.meta\.chapter : "";\s*'
    r'// Strip[^\n]*\n\s*'
    r'var partShort = part\.split\(":"\)\[0\]\.trim\(\);\s*'
    r'var chapShort = chap\.split\(":"\)\[0\]\.trim\(\);\s*'
    r'var crumb = \[partShort, chapShort\]\.filter\(Boolean\)\.join\(" \\u203a "\);\s*'
    r'if \(crumb && result\.meta && result\.meta\.title\s*'
    r'&& result\.meta\.title\.indexOf\("pf-crumb"\) === -1\) \{\s*'
    r'result\.meta\.title = "<span class=\\"pf-crumb\\">" \+ crumb \+ "</span> "\s*'
    r'\+ result\.meta\.title;\s*'
    r'\}\s*'
    r'\} catch \(e\) \{ /\* fall through \*/ \}\s*'
    r'return result;\s*'
    r'\},?',
    re.DOTALL,
)

NEW_PROCESS = '''processResult: function (result) {
        try {
          var part = (result && result.meta && result.meta.part) ? result.meta.part : "";
          var chap = (result && result.meta && result.meta.chapter) ? result.meta.chapter : "";
          var partShort = part.split(":")[0].trim();
          var chapShort = chap.split(":")[0].trim();
          var crumb = [partShort, chapShort].filter(Boolean).join(" \\u203a ");
          if (crumb && result.meta && result.meta.title
              && result.meta.title.indexOf("[" + partShort) !== 0) {
            result.meta.title = "[" + crumb + "]  " + result.meta.title;
          }
        } catch (e) { /* fall through */ }
        return result;
      },'''


def fix_file(p: Path) -> bool:
    text = p.read_text(encoding='utf-8')
    if 'pf-crumb' not in text:
        return False  # already on new version
    new_text, n = OLD_PROCESS.subn(lambda m: NEW_PROCESS, text, count=1)
    if n == 0:
        # Fallback: simpler text-based replacement for the inner HTML line
        new_text = re.sub(
            r'result\.meta\.title = "<span class=\\"pf-crumb\\">" \+ crumb \+ "</span> "\s*\+ result\.meta\.title;',
            'result.meta.title = "[" + crumb + "]  " + result.meta.title;',
            text,
        )
        # Also relax the "already prefixed" guard
        new_text = re.sub(
            r'result\.meta\.title\.indexOf\("pf-crumb"\) === -1',
            'result.meta.title.indexOf("[" + partShort) !== 0',
            new_text,
        )
        if new_text == text:
            return False
    p.write_text(new_text, encoding='utf-8')
    return True


def main() -> int:
    files = sorted({
        *ROOT.glob('part-*/module-*/section-*.html'),
        *ROOT.glob('part-*/module-*/index.html'),
        *ROOT.glob('appendices/appendix-*/section-*.html'),
        *ROOT.glob('appendices/appendix-*/index.html'),
        *ROOT.glob('front-matter/**/*.html'),
        ROOT / 'toc.html',
        ROOT / 'index.html',
    })
    fixed = 0
    for p in files:
        if not p.exists():
            continue
        if fix_file(p):
            fixed += 1
    print(f'Fixed breadcrumb in {fixed} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
