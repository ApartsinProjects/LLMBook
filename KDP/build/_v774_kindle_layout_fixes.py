"""v774: Kindle layout fixes per user feedback.

1. FM index page renders as a giant dark-navy hero in Kindle because
   <header class="chapter-header"> has background: navy in EPUB. Drop
   the navy background in epub_overrides.css so chapter headers render
   as plain text on Kindle (where decorative banners look broken).

2. about-authors photo overlaps text in Kindle because the inline
   <style> block with display:flex .author-card was stripped by html2epub
   when bundling the chapter (which strips inline styles for CSS
   isolation). Add equivalent rules to epub_overrides.css so they apply.

3. Streamline both author bios:
   - Drop duplicated full name from first sentence (already in <h3>).
   - Drop <div class="author-title"> affiliation (already in first sentence).

4. Rotate the OPF identifier so KDP treats this as a fresh submission
   (not an update of an existing reflowable book that KDP misclassified
   as fixed-format).
"""
from __future__ import annotations
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# ============================================================
# 1 + 2: epub_overrides.css additions
# ============================================================
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

# Replace .chapter-header rule to drop the dark navy background entirely
# in EPUB. Decorative hero banners do not work on Kindle (they either fill
# a whole page with empty color or break pagination unpredictably).
old_hero = (
    '.chapter-header {\n'
    '    -webkit-print-color-adjust: exact !important;\n'
    '    print-color-adjust: exact !important;\n'
    '    color-adjust: exact !important;\n'
    '    /* Fallback solid color in case the linear-gradient doesn\'t render\n'
    '     * (some older readers ignore CSS gradients) */\n'
    '    background-color: #1a1a2e !important;\n'
    '}'
)
new_hero = (
    '.chapter-header {\n'
    '    /* Strip the decorative dark-navy hero in EPUB. Kindle renders the\n'
    '     * banner as a near-blank colored page (the banner takes full page\n'
    '     * height with only header text on it), which made the FM index\n'
    '     * look broken. EPUB readers can still see the part-label/h1 with\n'
    '     * normal typography. */\n'
    '    background: transparent !important;\n'
    '    background-color: transparent !important;\n'
    '    color: inherit !important;\n'
    '    padding: 0.5em 0 !important;\n'
    '    margin: 0 0 1em 0 !important;\n'
    '}'
)
if old_hero in s:
    s = s.replace(old_hero, new_hero)
    print('  [override .chapter-header background -> transparent]')
else:
    print('  [skip .chapter-header old_hero pattern not found]')

# Force header text colors back to default (the next rule made them white,
# which on transparent background is invisible).
old_text = (
    '.chapter-header,\n'
    '.chapter-header h1,\n'
    '.chapter-header h2,\n'
    '.chapter-header h3,\n'
    '.chapter-header h4,\n'
    '.chapter-header h5,\n'
    '.chapter-header h6,\n'
    '.chapter-header a,\n'
    '.chapter-header .book-title-link {\n'
    '    color: #ffffff !important;\n'
    '}'
)
new_text = (
    '.chapter-header,\n'
    '.chapter-header h1,\n'
    '.chapter-header h2,\n'
    '.chapter-header h3,\n'
    '.chapter-header h4,\n'
    '.chapter-header h5,\n'
    '.chapter-header h6,\n'
    '.chapter-header a,\n'
    '.chapter-header .book-title-link {\n'
    '    color: inherit !important;\n'
    '}'
)
if old_text in s:
    s = s.replace(old_text, new_text)
    print('  [override .chapter-header text colors -> inherit]')

# Force part-label/chapter-label colors back to inherit (gold on white = invisible)
old_gold = (
    '.chapter-header .part-label,\n'
    '.chapter-header .chapter-label,\n'
    '.chapter-header .part-label a,\n'
    '.chapter-header .chapter-label a {\n'
    '    color: #d4b96a !important;  /* gold accent for breadcrumb labels */\n'
    '}'
)
new_gold = (
    '.chapter-header .part-label,\n'
    '.chapter-header .chapter-label,\n'
    '.chapter-header .part-label a,\n'
    '.chapter-header .chapter-label a {\n'
    '    color: #455a64 !important;  /* slate breadcrumb on light background */\n'
    '    text-decoration: none !important;\n'
    '    font-size: 0.85em !important;\n'
    '}'
)
if old_gold in s:
    s = s.replace(old_gold, new_gold)
    print('  [override .part-label gold -> slate]')

# Add .author-card / .author-photo rules so about-authors page renders
# correctly without the inline <style> block (which html2epub strips).
# Use simple side-by-side layout that works on Kindle.
author_css_block = '''
/* About the Authors layout (replaces inline <style> in about-authors.html
 * which html2epub strips). Kindle does not reliably support display:flex,
 * so use a simple float layout: photo floats left, bio text wraps around.
 */
.author-card {
    margin: 1.5em 0 2em;
    padding: 0;
    border: none;
    background: transparent;
    box-shadow: none;
    overflow: hidden;  /* contain the float */
}
.author-photo {
    float: left;
    width: 110px;
    height: 110px;
    margin: 0 1em 0.5em 0;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #455a64;
}
.author-info { display: block; }
.author-info h3 {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 1.15em;
    font-weight: 700;
    color: #1a4078;
    margin: 0 0 0.15em 0;
    border-bottom: none;
}
.author-info .author-title {
    font-size: 0.9em;
    color: #455a64;
    margin-bottom: 0.6em;
    font-style: italic;
}
.author-info p {
    font-size: 0.95em;
    line-height: 1.5;
    margin-bottom: 0.6em;
}
.author-links {
    margin-top: 0.6em;
    clear: both;  /* drop below the photo */
}
.author-links a {
    display: inline-block;
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-weight: 600;
    font-size: 0.85em;
    color: #1a4078;
    text-decoration: none;
    padding: 0.2em 0.6em;
    border: 1px solid #1a4078;
    border-radius: 6px;
}
.social-icon { display: none; }  /* SVG icons strip cleanly on Kindle */
'''
if '/* About the Authors layout' not in s:
    # Append at end of file
    s = s.rstrip() + '\n' + author_css_block + '\n'
    print('  [add .author-card layout block to epub_overrides.css]')
else:
    print('  [skip .author-card block: already present]')

overrides.write_text(s, encoding='utf-8')

# ============================================================
# 3. Streamline author bios
# ============================================================
about = ROOT / 'front-matter' / 'about-authors.html'
s = about.read_text(encoding='utf-8')

# Drop "Alexander (Sasha) Apartsin" + duplicated affiliation in opening sentence
old_a1 = ('<p><strong>Alexander (Sasha) Apartsin</strong> is a faculty '
          'member in the School of Computer Science at the Holon Institute '
          'of Technology. He holds a Ph.D.')
new_a1 = ('<p>He holds a Ph.D.')
if old_a1 in s:
    s = s.replace(old_a1, new_a1)
    print('  [streamline Alexander first sentence]')

# Drop the redundant <div class="author-title"> for Alexander
old_a_title = ('<div class="author-title">Faculty, School of Computer '
               'Science, Holon Institute of Technology</div>\n')
if old_a_title in s:
    s = s.replace(old_a_title, '')
    print('  [drop Alexander affiliation line]')

# Drop "Yehudit Aperstein" + duplicated affiliation in opening sentence
old_y1 = ('<p><strong>Yehudit Aperstein</strong> is a faculty member in '
          'the Department of Intelligent Systems at Afeka Academic College '
          'of Engineering. She holds a Ph.D.')
new_y1 = ('<p>She holds a Ph.D.')
if old_y1 in s:
    s = s.replace(old_y1, new_y1)
    print('  [streamline Yehudit first sentence]')

# Drop Yehudit affiliation line
old_y_title = ('<div class="author-title">Faculty, Department of '
               'Intelligent Systems, Afeka Academic College of '
               'Engineering</div>\n')
if old_y_title in s:
    s = s.replace(old_y_title, '')
    print('  [drop Yehudit affiliation line]')

# Add the author-title back as a brief affiliation line BELOW the h3
# (since user said names appear twice, but the affiliation is implicit
# in the first sentence after edit — actually drop it entirely; the
# bio paragraphs cover it).

about.write_text(s, encoding='utf-8')

# ============================================================
# 4. Rotate OPF identifier so KDP treats as fresh submission
# ============================================================
new_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID,
                          f'llmbook-thirteenth-edition-2026-rev{uuid.uuid4().hex[:6]}'))
new_uuid_full = f'urn:uuid:{new_uuid}'
print(f'  [new identifier] {new_uuid_full}')

# Update html2epub.toml
h2p = ROOT / 'html2epub.toml'
s = h2p.read_text(encoding='utf-8')
new_s = re.sub(r'identifier = "urn:uuid:[a-f0-9-]+"',
               f'identifier = "{new_uuid_full}"', s)
if new_s != s:
    h2p.write_text(new_s, encoding='utf-8')
    print(f'  [updated html2epub.toml identifier]')

# Update KDP/metadata/metadata.yaml
mp = ROOT / 'KDP' / 'metadata' / 'metadata.yaml'
s = mp.read_text(encoding='utf-8')
new_s = re.sub(r'uuid: "urn:uuid:[a-f0-9-]+"',
               f'uuid: "{new_uuid_full}"', s)
if new_s != s:
    mp.write_text(new_s, encoding='utf-8')
    print(f'  [updated metadata.yaml uuid]')

print('\nDone.')
