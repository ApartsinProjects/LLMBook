"""KDP fixed-format classifier audit.

KDP's web ingestion runs a classifier that decides reflowable vs
fixed-layout. The classifier IGNORES OPF rendition:layout declarations
when the cover.xhtml shows strong fixed-layout signals. If KDP misclas-
sifies a reflowable book as fixed-format, the user sees:

  "This content is a fixed format eBook. Updating a reflowable eBook
   with a fixed format eBook is not supported."

This check pins down all known classifier triggers BEFORE upload.

Triggers checked (any one HIT is enough to flag):
  T1. cover.xhtml body has `margin: 0` or `padding: 0` (ebooklib default
      template AND old fix_cover_kdp_heuristic.py both ship this)
  T2. cover.xhtml body is image-only when rendered (post-CSS):
      - <body> contains only <img> + display:none nodes
      - <body> has no visible text node
  T3. cover spine itemref has linear="no"
  T4. cover.xhtml has <meta name="viewport"> in head (paginated signal)
  T5. cover.xhtml has any <meta property="rendition:layout"> override
  T6. cover.xhtml has CSS using position:absolute or position:fixed in
      the cover content (typical fixed-layout positioning)

Run AFTER the build and AFTER all post-build patches, BEFORE upload.
"""
import re
import sys
import zipfile
from pathlib import Path


EPUB = Path('KDP/output/building-conversational-ai-llms-agents.epub')


def check_cover_for_classifier_triggers(epub_path: Path) -> dict:
    findings = {
        'T1_body_margin_zero': False,
        'T2_image_only_body': False,
        'T3_spine_linear_no': False,
        'T4_viewport_meta': False,
        'T5_rendition_override': False,
        'T6_absolute_positioning': False,
        'evidence': [],
        'cover_xhtml': '',
        'cover_id': '',
    }

    with zipfile.ZipFile(epub_path) as z:
        container = z.read('META-INF/container.xml').decode()
        opf_path = re.search(r'full-path="([^"]+)"', container).group(1)
        opf_dir = '/'.join(opf_path.split('/')[:-1])
        opf = z.read(opf_path).decode()

        cov_item = re.search(
            r'<item[^>]+href="([^"]*cover[^"]*\.xhtml)"[^>]*id="(cover[^"]*)"', opf)
        if not cov_item:
            findings['evidence'].append('No cover.xhtml manifest entry found')
            return findings
        cover_href = cov_item.group(1)
        cover_id = cov_item.group(2)
        findings['cover_id'] = cover_id
        cover_path = f'{opf_dir}/{cover_href}' if opf_dir else cover_href
        cover_xhtml = z.read(cover_path).decode()
        findings['cover_xhtml'] = cover_xhtml

        # T3. Spine linear="no" on cover
        sp = re.search(
            rf'<itemref[^>]+idref="{re.escape(cover_id)}"[^>]*linear="no"',
            opf)
        if sp:
            findings['T3_spine_linear_no'] = True
            findings['evidence'].append(
                f'T3: spine itemref idref="{cover_id}" linear="no"')

    # T1. body{margin:0|padding:0} CSS in cover.xhtml
    style_blocks = re.findall(
        r'<style\b[^>]*>(.*?)</style>', cover_xhtml, re.DOTALL | re.IGNORECASE)
    body_style_attr = re.findall(
        r'<body\b[^>]*\bstyle="([^"]+)"', cover_xhtml, re.IGNORECASE)
    all_css_for_body = []
    for sb in style_blocks:
        for m in re.finditer(
                r'\bbody\b[^{]*\{([^}]+)\}', sb, re.IGNORECASE):
            all_css_for_body.append(m.group(1))
    all_css_for_body.extend(body_style_attr)
    for css in all_css_for_body:
        if re.search(r'\bmargin\s*:\s*0(?:em|px|%)?\b', css, re.IGNORECASE) or \
           re.search(r'\bpadding\s*:\s*0(?:em|px|%)?\b', css, re.IGNORECASE):
            findings['T1_body_margin_zero'] = True
            findings['evidence'].append(
                f'T1: body CSS uses margin/padding:0 -> "{css.strip()[:80]}"')
            break

    # T2. Image-only body (post-render): strip <script>/<style>/display:none
    body_m = re.search(
        r'<body\b[^>]*>(.*?)</body>', cover_xhtml, re.DOTALL | re.IGNORECASE)
    if body_m:
        body = body_m.group(1)
        # Remove script/style blocks
        body = re.sub(r'<script\b.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
        body = re.sub(r'<style\b.*?</style>', '', body, flags=re.DOTALL | re.IGNORECASE)
        # Remove display:none nodes (cheap: any element with style="...display:none...")
        body = re.sub(
            r'<(\w+)\b[^>]*\bstyle="[^"]*display\s*:\s*none[^"]*"[^>]*>.*?</\1>',
            '', body, flags=re.DOTALL | re.IGNORECASE)
        # Also remove class="...cover-caption..." (legacy hidden caption)
        body = re.sub(
            r'<(\w+)\b[^>]*\bclass="[^"]*cover-caption[^"]*"[^>]*>.*?</\1>',
            '', body, flags=re.DOTALL | re.IGNORECASE)
        # Strip all tags
        text_only = re.sub(r'<[^>]+>', '', body).strip()
        has_img = bool(re.search(r'<img\b', body, re.IGNORECASE))
        if has_img and not text_only:
            findings['T2_image_only_body'] = True
            findings['evidence'].append(
                f'T2: cover.xhtml body contains <img> only (no visible text after stripping display:none)')

    # T4. <meta name="viewport"> in cover.xhtml head
    head_m = re.search(
        r'<head\b[^>]*>(.*?)</head>', cover_xhtml, re.DOTALL | re.IGNORECASE)
    if head_m:
        if re.search(r'<meta\b[^>]*\bname="viewport"', head_m.group(1),
                     re.IGNORECASE):
            findings['T4_viewport_meta'] = True
            findings['evidence'].append('T4: cover.xhtml has <meta name="viewport">')

    # T5. <meta property="rendition:layout"> in cover.xhtml
    if re.search(r'<meta\b[^>]*\bproperty="rendition:layout"', cover_xhtml,
                 re.IGNORECASE):
        findings['T5_rendition_override'] = True
        findings['evidence'].append(
            'T5: cover.xhtml has <meta property="rendition:layout"> override')

    # T6. position:absolute or position:fixed in cover.xhtml
    if re.search(r'position\s*:\s*(absolute|fixed)', cover_xhtml, re.IGNORECASE):
        findings['T6_absolute_positioning'] = True
        findings['evidence'].append('T6: cover.xhtml uses position:absolute/fixed')

    return findings


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', nargs='?', type=Path,
                    default=Path('KDP/output/building-conversational-ai-llms-agents.epub'))
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'EPUB: {args.epub}')
    findings = check_cover_for_classifier_triggers(args.epub)

    hits = sum(1 for k, v in findings.items()
               if k.startswith('T') and v is True)
    print()
    print('Cover fixed-layout classifier signal scan:')
    for key in ('T1_body_margin_zero', 'T2_image_only_body',
                'T3_spine_linear_no', 'T4_viewport_meta',
                'T5_rendition_override', 'T6_absolute_positioning'):
        status = 'HIT  ' if findings[key] else 'clean'
        print(f'  [{status}]  {key}')

    print()
    if findings['evidence']:
        print('Evidence:')
        for e in findings['evidence']:
            print(f'  - {e}')
    else:
        print('No fixed-layout classifier signals detected.')

    print()
    print('=' * 60)
    if hits == 0:
        print('RESULT: PASS (cover.xhtml looks unambiguously reflowable)')
        sys.exit(0)
    else:
        print(f'RESULT: FAIL ({hits} signal[s] hit; KDP may reject as fixed-format)')
        print('Fix recipe:')
        print('  - Run: python KDP/build/fix_cover_kdp_heuristic.py KDP/output/<book>.epub')
        print('  - Verify: no body{margin:0;padding:0}; visible <h1>/<p> body text;')
        print('    spine itemref linear="yes"; no viewport meta')
        sys.exit(1)


if __name__ == '__main__':
    main()
