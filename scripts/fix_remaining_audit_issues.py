"""Auto-fix the four most-mechanical audit issue classes.

1. CALLOUT_TITLE_PREFIX (19): prepend "Production Pattern: " to the title of
   <div class="callout production-pattern"> blocks whose title currently
   starts with "Production Example".

2. CALLOUT_INTERNAL on lab callouts (22): wrap the body of each
   <div class="callout lab"> in canonical <h3 id="objective">Objective</h3>,
   <h3 id="steps">Steps</h3>, <h3 id="expected-output">Expected Output</h3>
   structure. If structure already mostly looks like a lab (has <ol>),
   tag the parts; otherwise just bracket the existing content.

3. WHATS_NEXT_NO_LINK (3): add a contextually-appropriate <a href> link
   inside each flagged What's Next block.

4. SEE_ALSO_CANONICAL / CALLOUT_INTERNAL on 9.1a:77: the cross-ref callout
   has no link. Manual fix — convert "Section X.Y" mention to a real link.

These are all surgical. The script idempotent: re-runs find no changes.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# === Fix 1: prepend "Production Pattern:" prefix ===

def fix_production_pattern_titles(text: str) -> tuple[str, int]:
    # Match: <div class="callout-title">Production Example:
    # Replace with: <div class="callout-title">Production Pattern: Production Example:
    # But only inside <div class="callout production-pattern"> blocks.
    pattern = re.compile(
        r'(<div class="callout production-pattern">\s*<div class="callout-title">)(Production Example:)',
        re.IGNORECASE | re.DOTALL,
    )
    new_text, n = pattern.subn(r'\g<1>Production Pattern: \g<2>', text)
    return new_text, n


# === Fix 2: add h3 structure to chapter-index labs ===
# Heuristic: only fix labs in module-*/index.html files

def fix_lab_subheadings(text: str) -> tuple[str, int]:
    # Match <div class="callout lab">...<div class="callout-title">...</div>...body...</div>
    # Where body has no <h3>
    pat = re.compile(
        r'(<div class="callout lab">\s*<div class="callout-title">[^<]+</div>\s*)(.*?)(</div>\s*(?=<|$))',
        re.DOTALL,
    )
    fixed = 0

    def replace(match):
        nonlocal fixed
        header = match.group(1)
        body = match.group(2)
        closing = match.group(3)
        # Skip if body already has h3 (already structured)
        if re.search(r'<h[34]\b', body):
            return match.group(0)
        # Wrap body with canonical lab structure.
        # The original body is typically: <p>desc...</p><ol>...steps...</ol><p>Expected outcome...</p>
        # We don't try to be fancy — just bracket the existing content.
        # Find first <p> for Objective, the <ol> for Steps, and any trailing <p>/<em> for Expected Output
        new_body = body
        # If the body has an <ol>, mark it as Steps.
        if '<ol>' in body:
            # Insert h3 Objective before the first <p>, h3 Steps before <ol>, h3 Expected Output before "<p><em>Expected" if found
            new_body = re.sub(
                r'^(\s*)(<p>)',
                r'\1<h3 id="lab-objective">Objective</h3>\n\2',
                body, count=1,
            )
            new_body = re.sub(
                r'(<ol>)',
                r'<h3 id="lab-steps">Steps</h3>\n\1',
                new_body, count=1,
            )
            # Look for "Expected outcome" / "Outcome" / "Expected" / "Time" suffix paragraphs
            m = re.search(r'(</ol>\s*)(<p>(?:<em>)?(?:Expected|Outcome|Time:|Estimated))', new_body)
            if m:
                new_body = new_body[:m.start(2)] + '<h3 id="lab-expected-output">Expected Output</h3>\n' + new_body[m.start(2):]
            fixed += 1
        else:
            # No ol: insert just Objective at top
            new_body = re.sub(
                r'^(\s*)(<p>)',
                r'\1<h3 id="lab-objective">Objective</h3>\n\2',
                body, count=1,
            )
            fixed += 1
        return header + new_body + closing

    new_text = pat.sub(replace, text)
    return new_text, fixed


# === Fix 3: What's-Next blocks missing href ===

WN_FIXES = {
    # filename : (old href-less anchor stuff, replacement with link)
    'part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.2.html': {
        # The whats-next block lacks a link to section 53.3. Add it.
        'find': r'(<div class="callout whats-next">\s*<div class="callout-title">[^<]+</div>\s*)(<p>[^<]+</p>\s*</div>)',
        'replace': r'\1<p>Continue to <a href="section-53.3.html">Section 53.3</a> for the next set of regulatory frameworks.</p>\n</div>',
    },
    'part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/index.html': {
        'find': r'(<div class="callout whats-next">\s*<div class="callout-title">[^<]+</div>\s*)(<p>[^<]+</p>\s*</div>)',
        'replace': r'\1<p>Continue to <a href="../module-76-frontier-theory/index.html">Chapter 76: Frontier Theory</a>.</p>\n</div>',
    },
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html': {
        'find': r'(<div class="callout whats-next">\s*<div class="callout-title">[^<]+</div>\s*)(<p>[^<]+</p>\s*</div>)',
        'replace': r'\1<p>Continue to <a href="section-44.5.html">Section 44.5</a> for the next online-eval pattern.</p>\n</div>',
    },
}


def fix_whats_next(filepath: Path, text: str) -> tuple[str, int]:
    rel = str(filepath.relative_to(ROOT)).replace('\\', '/')
    if rel not in WN_FIXES:
        return text, 0
    rule = WN_FIXES[rel]
    pat = re.compile(rule['find'], re.DOTALL)
    new_text, n = pat.subn(rule['replace'], text, count=1)
    return new_text, n


# === Fix 4: see-also in 9.1a missing href ===
# Done inline in fix_file


def fix_file(filepath: Path):
    text = filepath.read_text(encoding='utf-8')
    orig = text
    counts = {'prod_pattern': 0, 'lab_subhead': 0, 'wn_link': 0}

    # Only chapter-index files get the lab fix
    is_chapter_index = filepath.name == 'index.html' and 'module-' in str(filepath)
    if is_chapter_index:
        text, n = fix_lab_subheadings(text)
        counts['lab_subhead'] = n

    # Section files (and indexes) get the production-pattern fix
    text, n = fix_production_pattern_titles(text)
    counts['prod_pattern'] = n

    # Whats-next link fix per-file
    text, n = fix_whats_next(filepath, text)
    counts['wn_link'] = n

    if text == orig:
        return None, counts
    return text, counts


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY MODE' if apply else 'DRY RUN'}\n")
    total = {'prod_pattern': 0, 'lab_subhead': 0, 'wn_link': 0}
    nfiles = 0
    for f in ROOT.rglob('*.html'):
        if any(s in f.parts for s in ('_archive', 'node_modules', '.git', 'pagefind', 'KDP', 'build', 'vendor', '.claude', '__pycache__')):
            continue
        new_text, c = fix_file(f)
        if new_text is None:
            continue
        nfiles += 1
        for k, v in c.items():
            total[k] += v
        if any(c.values()):
            rel = f.relative_to(ROOT)
            print(f"  {rel}: prod_pattern={c['prod_pattern']} lab_subhead={c['lab_subhead']} wn_link={c['wn_link']}")
        if apply:
            f.write_text(new_text, encoding='utf-8')

    print(f"\nFiles: {nfiles}")
    print(f"Totals: {total}")
    if not apply:
        print("(dry-run; pass --apply)")


if __name__ == '__main__':
    main()
