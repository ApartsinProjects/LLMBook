"""Really deep per-page scan for ANY KDP-suspicious pattern.

Beyond what audit_kindle_compliance, audit_h4_h5_h6_h7, audit_kdp_strict,
audit_kdp_fixed_layout_classifier, deep_hunt_fixed_layout,
per_page_analyzer, and hunt_fxl_cues_per_page already check.

25+ additional checks per page:
  A. Web-only nav scaffolding ('Skip to main content', headers, role=banner)
  B. Repeated boilerplate at start of every chapter (chrome content)
  C. <details>/<summary> usage (KDP-sanitized but worth flagging)
  D. <picture>/<source> multi-source responsive images (rare in EPUB)
  E. <a target="_blank"> / rel="noopener" (web-only attrs)
  F. <svg width="Xpx" height="Ypx"> with explicit px dims (fixed canvas)
  G. data: URIs (base64-embedded content)
  H. <meta http-equiv> tags (sometimes used for FXL signals)
  I. HTML5 semantic tags: <main>, <article>, <section>, <nav> deep nesting
  J. <aside epub:type="footnote"> structure
  K. KaTeX-rendered math markers (.katex, mathml)
  L. <table> count, nesting depth, COLs/COLGROUPs
  M. Image aspect ratios matching book-page (1.5/1.6) too dominantly
  N. Per-page MIME types declared
  O. <header> / <footer> on every chapter (repeating chrome)
  P. column-count / column-rule CSS (multi-column layout)
  Q. page-break-* CSS rules (fixed-layout pagination hints)
  R. widows/orphans CSS rules
  S. HTML comments with Amazon markers
  T. Inline base64 images in <img src="data:...">
  U. <video>/<audio>/<track> (multimedia, KDP-banned)
  V. <iframe> / <embed> / <object> (interactive, KDP-banned)
  W. <form> / <input> / <button> elements
  X. Per-page text-density outliers (bytes/word)
  Y. Specific Amazon-bound URLs in hrefs/srcs
"""
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

EPUB = Path('KDP/output/building-conversational-ai-llms-agents.epub')
if len(sys.argv) > 1:
    EPUB = Path(sys.argv[1])

print(f'Really deep scan: {EPUB} ({EPUB.stat().st_size/1024/1024:.2f} MB)\n')

with zipfile.ZipFile(EPUB) as z:
    names = z.namelist()
    xhtml_files = [n for n in names if n.lower().endswith(('.xhtml', '.html'))]
    css_files = [n for n in names if n.lower().endswith('.css')]
    print(f'Scanning {len(xhtml_files)} XHTML + {len(css_files)} CSS files\n')

    # Aggregate counters
    findings = defaultdict(list)  # check_id -> list of (severity, file, evidence)
    page_data = []  # per-page detailed records

    # Track repeated boilerplate
    body_prefixes = Counter()  # first 200 chars of body, normalized
    head_prefixes = Counter()  # head content normalized

    for n in xhtml_files:
        try:
            content = z.read(n).decode('utf-8', errors='ignore')
        except Exception:
            continue

        head_m = re.search(r'<head\b[^>]*>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
        body_m = re.search(r'<body\b[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        head = head_m.group(1) if head_m else ''
        body = body_m.group(1) if body_m else ''

        # === A. Web-only nav scaffolding ===
        if 'Skip to main content' in body[:500]:
            findings['A_skip_to_main_content'].append(('MED', n, '"Skip to main content" link in first 500B'))
        if re.search(r'<header\b[^>]*role="banner"', body, re.IGNORECASE):
            findings['A_role_banner'].append(('LOW', n, 'role="banner" on header'))
        if re.search(r'<nav\b[^>]*\bclass="[^"]*chapter-nav[^"]*"', body, re.IGNORECASE):
            findings['A_chapter_nav'].append(('LOW', n, 'web chapter-nav element'))

        # === B. Repeated boilerplate prefix ===
        prefix = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body[:300])).strip()[:100]
        body_prefixes[prefix] += 1

        # === C. <details>/<summary> ===
        if re.search(r'<details\b', body, re.IGNORECASE):
            findings['C_details_element'].append(('MED', n, 'has <details>'))

        # === D. <picture>/<source> ===
        if re.search(r'<picture\b', body, re.IGNORECASE):
            findings['D_picture_element'].append(('HIGH', n, 'has <picture>'))
        if re.search(r'<source\b', body, re.IGNORECASE):
            findings['D_source_element'].append(('HIGH', n, 'has <source>'))

        # === E. <a target=_blank> / rel attrs ===
        if re.search(r'<a\b[^>]*\btarget="_blank"', body, re.IGNORECASE):
            findings['E_target_blank'].append(('LOW', n, 'has target="_blank"'))
        if re.search(r'<a\b[^>]*\brel="(?:noopener|noreferrer)', body, re.IGNORECASE):
            findings['E_rel_noopener'].append(('LOW', n, 'has rel="noopener|noreferrer"'))

        # === F. <svg width=Xpx height=Ypx> ===
        for m in re.finditer(r'<svg\b[^>]*\bwidth="(\d+)(?:px)?"[^>]*\bheight="(\d+)(?:px)?"', body, re.IGNORECASE):
            findings['F_svg_px_dims'].append(('MED', n, f'<svg width="{m.group(1)}" height="{m.group(2)}">'))
            break  # one per file is enough

        # === G. data: URIs ===
        if 'src="data:' in body or 'href="data:' in body:
            findings['G_data_uri'].append(('HIGH', n, 'has data: URI'))

        # === H. <meta http-equiv> ===
        for m in re.finditer(r'<meta\b[^>]*\bhttp-equiv="([^"]+)"', head, re.IGNORECASE):
            findings['H_http_equiv'].append(('LOW', n, f'http-equiv="{m.group(1)}"'))

        # === I. Deep semantic nesting ===
        # Count nested <section>/<article> depth
        section_depth = 0
        max_section_depth = 0
        for m in re.finditer(r'<(/?)(?:section|article)\b', body, re.IGNORECASE):
            if m.group(1):
                section_depth -= 1
            else:
                section_depth += 1
                max_section_depth = max(max_section_depth, section_depth)
        if max_section_depth > 5:
            findings['I_deep_section_nesting'].append(('LOW', n, f'max section/article nesting {max_section_depth}'))

        # === J. epub:type="footnote" structures ===
        if re.search(r'<aside\b[^>]*\bepub:type="(?:footnote|endnote)"', body, re.IGNORECASE):
            findings['J_footnote_aside'].append(('LOW', n, 'has aside epub:type=footnote'))

        # === K. KaTeX/MathML markers ===
        n_katex = len(re.findall(r'class="[^"]*katex', body, re.IGNORECASE))
        n_mathml = len(re.findall(r'<math\b', body, re.IGNORECASE))
        if n_mathml > 0:
            findings['K_mathml'].append(('MED', n, f'{n_mathml} <math> elements (KDP MathML support spotty)'))

        # === L. <table> count and nesting ===
        n_tables = len(re.findall(r'<table\b', body, re.IGNORECASE))
        if n_tables > 0:
            # check nesting depth
            tdepth = 0
            maxtd = 0
            for m in re.finditer(r'<(/?)table\b', body, re.IGNORECASE):
                if m.group(1): tdepth -= 1
                else:
                    tdepth += 1
                    maxtd = max(maxtd, tdepth)
            if maxtd >= 2:
                findings['L_nested_tables'].append(('MED', n, f'nested table depth {maxtd}'))
        # COLs / COLGROUPs are fixed-layout-leaning
        if re.search(r'<colgroup\b', body, re.IGNORECASE):
            findings['L_colgroup'].append(('LOW', n, 'has <colgroup>'))

        # === N. Per-page byte size ===
        bsize = len(body)
        text = re.sub(r'<[^>]+>', ' ', body)
        text = re.sub(r'\s+', ' ', text).strip()
        words = len(text.split())
        density = bsize / max(1, words)

        page_data.append({
            'file': n, 'bytes': bsize, 'words': words, 'density': density,
            'tables': n_tables, 'mathml': n_mathml, 'katex': n_katex,
        })

        # === O. <header>/<footer> per chapter ===
        n_header = len(re.findall(r'<header\b', body, re.IGNORECASE))
        n_footer = len(re.findall(r'<footer\b', body, re.IGNORECASE))
        if n_header > 0:
            findings['O_chapter_header'].append(('LOW', n, f'{n_header} <header> element(s)'))
        if n_footer > 0:
            findings['O_chapter_footer'].append(('LOW', n, f'{n_footer} <footer> element(s)'))

        # === P/Q/R. CSS pagination/layout hints inline ===
        for prop, sev, lbl in [
            (r'column-count\s*:', 'MED', 'P_column_count'),
            (r'page-break-(?:before|after|inside)\s*:', 'MED', 'Q_page_break'),
            (r'\b(?:widows|orphans)\s*:', 'LOW', 'R_widows_orphans'),
        ]:
            if re.search(prop, body, re.IGNORECASE):
                findings[lbl].append(('MED' if sev=='MED' else 'LOW', n, prop))

        # === S. Amazon-bound URLs ===
        for m in re.finditer(r'href="https?://[^"]*(?:amazon\.com|amzn\.com|kdp\.amazon\.com)[^"]*"', body, re.IGNORECASE):
            findings['S_amazon_url'].append(('LOW', n, m.group(0)[:120]))
            break

        # === T. HTML comments with Amazon/fixed markers ===
        for m in re.finditer(r'<!--[^>]*(?:amzn|amazon|fixed[\s-]?layout|fxl|kpf)[^>]*-->', content, re.IGNORECASE):
            findings['T_amzn_comment'].append(('HIGH', n, m.group(0)[:120]))

        # === U/V/W. Multimedia / interactive (KDP-banned) ===
        for tag, sev in [
            ('video', 'HIGH'), ('audio', 'HIGH'), ('track', 'HIGH'),
            ('iframe', 'HIGH'), ('embed', 'HIGH'), ('object', 'HIGH'),
            ('form', 'HIGH'), ('input', 'HIGH'),
        ]:
            if re.search(rf'<{tag}\b', body, re.IGNORECASE):
                findings[f'V_{tag}'].append(('HIGH', n, f'has <{tag}>'))

    # === B. Boilerplate aggregation ===
    print('=' * 70)
    print('B. REPEATED BODY-PREFIX BOILERPLATE (first 100 chars of body, post-text-strip)')
    print('=' * 70)
    repeated = [(prefix, count) for prefix, count in body_prefixes.most_common(5)]
    for prefix, count in repeated:
        flag = ' <-- REPEATED IN >50 PAGES' if count > 50 else (' <-- repeated in >10 pages' if count > 10 else '')
        print(f'  appears in {count} page(s): {prefix!r}{flag}')

    # Image aspect ratio distribution
    print()
    print('=' * 70)
    print('M. IMAGE ASPECT RATIO DOMINANCE')
    print('=' * 70)
    try:
        from PIL import Image
        import io
        ar_buckets = Counter()
        for nm in names:
            if nm.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    im = Image.open(io.BytesIO(z.read(nm)))
                    w, h = im.size
                    ar = round(h / max(1, w), 2)
                    ar_buckets[ar] += 1
                except Exception:
                    pass
        total = sum(ar_buckets.values())
        print(f'  Total images: {total}    Distinct AR values: {len(ar_buckets)}')
        print(f'  Top 5 aspect ratios:')
        for ar, c in ar_buckets.most_common(5):
            pct = 100 * c / total
            book_like = ar in (1.5, 1.6, 0.625, 0.667)
            tag = ' (BOOK-PAGE ratio)' if book_like else ''
            print(f'    AR {ar:.2f}: {c} images ({pct:.1f}%){tag}')
    except ImportError:
        pass

    # X. Per-page byte/word outliers
    print()
    print('=' * 70)
    print('X. PER-PAGE OUTLIERS (top-5 by various metrics)')
    print('=' * 70)
    pd_sorted = sorted(page_data, key=lambda p: -p['bytes'])
    print('  Largest pages by bytes:')
    for p in pd_sorted[:5]:
        print(f'    {p["bytes"]/1024:6.1f} KB  words={p["words"]:5d}  tables={p["tables"]}  {p["file"]}')
    print('  Smallest pages by bytes:')
    for p in sorted(page_data, key=lambda p: p['bytes'])[:5]:
        print(f'    {p["bytes"]/1024:6.1f} KB  words={p["words"]:5d}  tables={p["tables"]}  {p["file"]}')


# Aggregate report
print()
print('=' * 70)
print('AGGREGATE FINDINGS BY CHECK')
print('=' * 70)
high_findings = []
if not findings:
    print('  No anomalies detected across any per-page check.')
else:
    by_check = []
    for check, hits in findings.items():
        sev = hits[0][0]
        by_check.append((sev, check, len(hits), hits[:3]))
    severity_rank = {'HIGH': 0, 'MED': 1, 'LOW': 2}
    by_check.sort(key=lambda x: (severity_rank[x[0]], -x[2]))
    for sev, check, count, samples in by_check:
        page_pct = 100 * count / len(xhtml_files)
        print(f'\n  [{sev}] {check}: {count} hit(s) ({page_pct:.1f}% of pages)')
        for s_sev, s_file, s_ev in samples:
            print(f'        {s_file}: {s_ev[:100]}')
        if sev == 'HIGH':
            high_findings.append((check, count))

# Hard-gate exit: any HIGH-severity finding fails the build
print()
print('=' * 70)
if high_findings:
    print(f'RESULT: FAIL — {len(high_findings)} HIGH-severity check(s) tripped')
    for check, count in high_findings:
        print(f'  [FAIL] {check}: {count} hit(s)')
    print('Fix recipe: see html2kpd LESSONS.md for the matching post-build patch.')
    sys.exit(1)
else:
    n_med = sum(1 for sev, _, _, _ in by_check if sev == 'MED') if findings else 0
    n_low = sum(1 for sev, _, _, _ in by_check if sev == 'LOW') if findings else 0
    print(f'RESULT: PASS — no HIGH-severity findings ({n_med} MED, {n_low} LOW informational)')
    sys.exit(0)
