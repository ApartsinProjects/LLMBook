"""Post-build EPUB patch: neutralize KFX-hostile <style> inside <svg>.

Why:
  Kindle's KFX renderer does not implement a full SVG CSS engine. SVGs
  that rely on an internal <style> block with class/id selectors render
  unstyled (best case) or fail entirely (worst case). The pattern
  `<style>@keyframes ... animation: ...` is documented to crash some
  pipelines.

What we do:
  1. Find every <svg>...</svg> block (standalone .svg files + inline in xhtml).
  2. Extract any internal <style>...</style> block.
  3. Parse simple CSS rules: `.cls{prop:val;...}`, `#id{prop:val;...}`,
     `tag{prop:val;...}`, `*{prop:val;...}`.
  4. For each matched element inside the SVG, append the rule's props
     as a direct `style="..."` attribute (presentation attributes that
     KFX's SVG parser handles natively).
  5. Discard `@keyframes`, `@import`, `animation:` / `transition:`
     properties (KFX cannot animate; dropping is safe).
  6. Remove the <style> block.

Run AFTER fix_cover_image_kdp.py.
"""
from __future__ import annotations
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

STYLE_BLOCK_RE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.DOTALL | re.IGNORECASE)
SVG_BLOCK_RE = re.compile(r'(<svg\b[^>]*>)(.*?)(</svg>)', re.DOTALL | re.IGNORECASE)
# CSS rule: selector { props } ; tolerate nested @rules by skipping them
RULE_RE = re.compile(r'([^{}@]+)\{([^{}]*)\}', re.DOTALL)
ATKEY_RE = re.compile(r'@(?:keyframes|media|import|font-face|supports)\b[^{]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', re.IGNORECASE)
ANIM_PROP_RE = re.compile(r'\b(?:animation|transition|will-change)[^;]*;?', re.IGNORECASE)


def parse_rules(css: str):
    """Return list of (selector_list, properties_dict) tuples."""
    # Strip @keyframes/@media/etc blocks entirely
    css_clean = ATKEY_RE.sub('', css)
    rules = []
    for m in RULE_RE.finditer(css_clean):
        sel_raw = m.group(1).strip()
        props_raw = m.group(2).strip()
        if not sel_raw or not props_raw:
            continue
        # Drop animation/transition/will-change properties
        props_raw = ANIM_PROP_RE.sub('', props_raw)
        props = {}
        for decl in props_raw.split(';'):
            decl = decl.strip().rstrip('!important').strip()
            if ':' in decl:
                k, v = decl.split(':', 1)
                k = k.strip().lower()
                v = v.strip().rstrip('!important').strip()
                if k and v:
                    props[k] = v
        if not props:
            continue
        selectors = [s.strip() for s in sel_raw.split(',') if s.strip()]
        for s in selectors:
            rules.append((s, props))
    return rules


def apply_rules_to_svg(svg_inner: str, rules: list[tuple[str, dict]]) -> str:
    """For each element in svg_inner matching a rule selector, append a style= attr."""
    for sel, props in rules:
        if not props:
            continue
        prop_str = ';'.join(f'{k}:{v}' for k, v in props.items())
        if sel == '*':
            # Apply to every direct element tag (best effort: every open tag with non-/)
            def add_universal(m):
                tag = m.group(0)
                if tag.endswith('/>') or m.group(1).lower() in ('style', 'defs', 'metadata', 'title'):
                    return tag
                return _merge_style(tag, prop_str)
            svg_inner = re.sub(r'<(\w+)\b[^>]*?>', add_universal, svg_inner)
        elif sel.startswith('.'):
            cls = sel[1:].strip()
            # find elements with class="... cls ..."
            pat = re.compile(r'(<\w+\b[^>]*\bclass="[^"]*\b' + re.escape(cls) + r'\b[^"]*"[^>]*?)(/?>)')
            svg_inner = pat.sub(lambda m: _merge_style(m.group(1), prop_str) + m.group(2), svg_inner)
        elif sel.startswith('#'):
            ident = sel[1:].strip()
            pat = re.compile(r'(<\w+\b[^>]*\bid="' + re.escape(ident) + r'"[^>]*?)(/?>)')
            svg_inner = pat.sub(lambda m: _merge_style(m.group(1), prop_str) + m.group(2), svg_inner)
        elif re.match(r'^[a-zA-Z][\w-]*$', sel):
            # plain tag selector like `rect`, `text`
            pat = re.compile(r'(<' + re.escape(sel) + r'\b[^>]*?)(/?>)', re.IGNORECASE)
            svg_inner = pat.sub(lambda m: _merge_style(m.group(1), prop_str) + m.group(2), svg_inner)
        # Skip complex selectors (descendant, pseudo, etc.) - rare in our SVGs
    return svg_inner


def _merge_style(open_tag_prefix: str, new_props: str) -> str:
    """Insert or extend a style="..." attribute on an open tag prefix (no closing >)."""
    m = re.search(r'\bstyle="([^"]*)"', open_tag_prefix)
    if m:
        existing = m.group(1).rstrip(';')
        merged = f'{existing};{new_props}'
        return open_tag_prefix[:m.start()] + f'style="{merged}"' + open_tag_prefix[m.end():]
    else:
        return open_tag_prefix + f' style="{new_props}"'


def process_svg_block(svg_open: str, svg_inner: str, svg_close: str) -> tuple[str, bool, int]:
    """Returns (new_block, changed, n_styles_removed)."""
    styles = list(STYLE_BLOCK_RE.finditer(svg_inner))
    if not styles:
        return svg_open + svg_inner + svg_close, False, 0
    # Collect all rules from every <style> block
    all_rules = []
    for sm in styles:
        all_rules.extend(parse_rules(sm.group(1)))
    # Remove the <style> blocks
    svg_inner_no_style = STYLE_BLOCK_RE.sub('', svg_inner)
    # Apply rules
    svg_inner_styled = apply_rules_to_svg(svg_inner_no_style, all_rules)
    return svg_open + svg_inner_styled + svg_close, True, len(styles)


def process_file(content: bytes) -> tuple[bytes, dict]:
    stats = {'svgs_scanned': 0, 'svgs_modified': 0, 'style_blocks_removed': 0}
    text = content.decode('utf-8', errors='ignore')

    def repl(m):
        stats['svgs_scanned'] += 1
        new_block, changed, n_styles = process_svg_block(m.group(1), m.group(2), m.group(3))
        if changed:
            stats['svgs_modified'] += 1
            stats['style_blocks_removed'] += n_styles
        return new_block

    new_text = SVG_BLOCK_RE.sub(repl, text)
    if stats['svgs_modified'] == 0:
        return content, stats
    return new_text.encode('utf-8'), stats


def patch(epub_path: Path) -> dict:
    totals = {'files_scanned': 0, 'files_modified': 0,
              'svgs_scanned': 0, 'svgs_modified': 0, 'style_blocks_removed': 0}
    tmp_out = epub_path.with_suffix(epub_path.suffix + '.tmp')
    with zipfile.ZipFile(epub_path, 'r') as zin, \
         zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        # mimetype FIRST
        for info in zin.infolist():
            if info.filename == 'mimetype':
                zout.writestr(info, zin.read(info.filename),
                              compress_type=zipfile.ZIP_STORED)
                break
        for info in zin.infolist():
            if info.filename == 'mimetype':
                continue
            data = zin.read(info.filename)
            lower = info.filename.lower()
            if lower.endswith(('.svg', '.xhtml', '.html')):
                totals['files_scanned'] += 1
                new_data, s = process_file(data)
                totals['svgs_scanned'] += s['svgs_scanned']
                if s['svgs_modified']:
                    totals['files_modified'] += 1
                    totals['svgs_modified'] += s['svgs_modified']
                    totals['style_blocks_removed'] += s['style_blocks_removed']
                    data = new_data
            zout.writestr(info.filename, data, compress_type=zipfile.ZIP_DEFLATED)
    os.replace(tmp_out, epub_path)
    return totals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('epub', type=Path)
    args = ap.parse_args()
    if not args.epub.exists():
        sys.exit(f'EPUB not found: {args.epub}')
    print(f'Patching {args.epub}')
    t = patch(args.epub)
    print(f'  files scanned:        {t["files_scanned"]}')
    print(f'  files modified:       {t["files_modified"]}')
    print(f'  SVGs scanned:         {t["svgs_scanned"]}')
    print(f'  SVGs modified:        {t["svgs_modified"]}')
    print(f'  <style> blocks removed: {t["style_blocks_removed"]}')
    print('DONE.')


if __name__ == '__main__':
    main()
