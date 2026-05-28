"""Detect Kindle-hostile patterns that EPUBCheck tolerates but Kindle's
converter (KPV / KDP) silently rejects.

Kindle uses a STRICT XHTML parser. EPUBCheck uses an HTML5-tolerant parser.
Any file that survives EPUBCheck can still die in KFX conversion. Today's
KPV+KDP failures (after the 19 section splits) traced to exactly this gap:

  - Undefined HTML entities (e.g. &rsaquo;, &middot;) -- HTML5 OK, XHTML fails
  - Unescaped & < > in text content
  - HTML entity inside alt= or aria-label= attribute values
  - <img> with inline style attribute (Kindle E21018)
  - Self-closing non-void tags (<span class="x"/>)
  - SVG with lowercase viewbox (Kindle drops the attribute silently)
  - SVG duplicate attribute names (xmlns appearing twice, etc.)
  - Whole-document XHTML well-formedness failure (mismatched/unclosed tags)

This is a P0 because each failure mode CAN result in a silently-rejected
KDP upload with no useful error message.
"""
import re
from collections import namedtuple
from xml.etree import ElementTree as ET

PRIORITY = "P0"
CHECK_ID = "KINDLE_STRICT_XHTML"
DESCRIPTION = "Kindle-hostile pattern: XHTML well-formedness, illegal entity, lowercase viewBox, img style, etc."

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# XHTML 1.0 strict only defines: amp, lt, gt, quot, apos
XHTML_BUILTIN = {'amp', 'lt', 'gt', 'quot', 'apos'}

NON_VOID = ('span', 'div', 'p', 'a', 'td', 'th', 'li', 'strong', 'em', 'b', 'i',
            'sub', 'sup', 'small', 'code', 'pre', 'section', 'article', 'header',
            'footer', 'main', 'nav', 'aside', 'figure', 'figcaption', 'blockquote',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'dl', 'dd', 'dt',
            'tbody', 'thead', 'tfoot', 'tr', 'table', 'details', 'summary',
            'script', 'style', 'label', 'button')

SC_NON_VOID_RE = re.compile(r'<(' + '|'.join(NON_VOID) + r')\b[^>]*/>', re.IGNORECASE)
IMG_STYLE_RE = re.compile(r'<img\b[^>]*\bstyle="[^"]*"', re.IGNORECASE)
ENT_NAMED_RE = re.compile(r'&([a-zA-Z][a-zA-Z0-9]*);')
# Only flag &lt; / &gt; / &quot; inside alt/aria-label/title attributes —
# Kindle interprets these as their literal characters when parsing the
# attribute, causing the attribute value to be misread (E21018). The
# &amp; entity is the CORRECT escape for & and must not be flagged.
ENT_IN_ATTR_RE = re.compile(
    r'(?:alt|aria-label|title)="[^"]*&(?:lt|gt|quot);[^"]*"',
    re.IGNORECASE,
)
# Case-SENSITIVE: flag ONLY lowercase 'viewbox=' (Kindle drops it).
# The canonical 'viewBox=' must NOT be flagged.
SVG_LOWER_VB_RE = re.compile(r'<svg\b[^>]*\bviewbox=')
SVG_OPEN_RE = re.compile(r'<svg\b[^>]*>', re.IGNORECASE)
ATTR_RE = re.compile(r'(\w[\w:-]*)=("[^"]*"|\'[^\']*\')')


def _line_at(html: str, pos: int) -> int:
    return html.count('\n', 0, pos) + 1


def _check_bare_ampersand(html: str) -> list[tuple[int, str]]:
    """Find & that is NOT part of a valid character / entity reference."""
    out = []
    pat = re.compile(r'&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)')
    for m in pat.finditer(html):
        # skip ampersands inside <script>...</script> or <style>...</style>
        # by checking the surrounding context
        before = html[:m.start()]
        last_script = max(before.rfind('<script'), before.rfind('<style'))
        if last_script >= 0:
            last_close = max(before.rfind('</script>'), before.rfind('</style>'))
            if last_script > last_close:
                continue
        out.append((_line_at(html, m.start()), html[max(0, m.start() - 20):m.start() + 30]))
    return out


def run(filepath, html, context):
    issues = []

    # 1. Illegal named entities (HTML5 OK, XHTML 1.0 strict rejects)
    illegal_ents = {}
    for m in ENT_NAMED_RE.finditer(html):
        name = m.group(1)
        if name in XHTML_BUILTIN:
            continue
        # Also accept common Latin1 entity names that XHTML 1.0 transitional defines
        # (we still flag them so authors normalize to numeric refs for safety)
        line = _line_at(html, m.start())
        illegal_ents.setdefault(name, []).append(line)
    for name, lines in illegal_ents.items():
        first_line = lines[0]
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, first_line,
                            f'illegal-in-XHTML named entity &{name}; '
                            f'(use numeric ref e.g. &#NNNN;) at line(s) {lines[:5]}'))

    # 2. HTML entity inside alt= or aria-label= attribute value
    for m in ENT_IN_ATTR_RE.finditer(html):
        line = _line_at(html, m.start())
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                            f'entity inside alt/aria-label attribute (Kindle E21018): '
                            f'{m.group(0)[:80]}'))

    # 3. <img> with inline style (Kindle E21018 trigger)
    for m in IMG_STYLE_RE.finditer(html):
        line = _line_at(html, m.start())
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                            f'<img> with inline style attribute (Kindle E21018)'))

    # 4. Self-closing non-void tags
    for m in SC_NON_VOID_RE.finditer(html):
        line = _line_at(html, m.start())
        tag = m.group(1)
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                            f'self-closing non-void <{tag}/> (Kindle E21018, must be <{tag}></{tag}>)'))

    # 5. SVG with lowercase viewbox (Kindle drops the attribute silently)
    for m in SVG_LOWER_VB_RE.finditer(html):
        line = _line_at(html, m.start())
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                            'SVG with lowercase viewbox= (use viewBox=, Kindle drops the lowercase form)'))

    # 6. SVG duplicate attribute names in the open tag
    for m in SVG_OPEN_RE.finditer(html):
        attrs_str = m.group(0)
        seen = set()
        for am in ATTR_RE.finditer(attrs_str):
            name = am.group(1).lower()
            if name in seen:
                line = _line_at(html, m.start())
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                                    f'SVG duplicate attribute "{name}" (XML rejects)'))
                break
            seen.add(name)

    # 7. Bare ampersand in text (not part of valid char/entity ref)
    bare = _check_bare_ampersand(html)
    if bare:
        first_line, ctx = bare[0]
        issues.append(Issue(PRIORITY, CHECK_ID, filepath, first_line,
                            f'bare & in text ({len(bare)} occurrences; first at line '
                            f'{first_line}: ...{ctx}...). Escape as &amp; or use entity.'))

    # 8. Whole-body XHTML well-formedness check (catches mismatched tags).
    # Strip <script>...</script> and <style>...</style> before parsing,
    # because raw JS operators (||, &&, <) are not XHTML-valid markup and
    # would produce false positives. In a real XHTML 1.0 doc these blocks
    # would be wrapped in CDATA, but Kindle's parser tolerates either form
    # as long as the surrounding HTML is well-formed.
    body_m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    if body_m:
        body_content = body_m.group(1)
        body_content = re.sub(
            r'<(script|style)\b[^>]*>.*?</\1>',
            r'<\1/>',
            body_content,
            flags=re.DOTALL | re.IGNORECASE,
        )
        body_xml = ('<root xmlns="http://www.w3.org/1999/xhtml">'
                    + body_content + '</root>')
        try:
            ET.fromstring(body_xml)
        except ET.ParseError as e:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                                f'XHTML body well-formedness fail: {e}'))

    return issues
