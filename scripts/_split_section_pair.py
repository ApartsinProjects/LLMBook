"""
Split a single section HTML file at a chosen line index into two siblings:
section-X.Ya.html and section-X.Yb.html, sharing the original head/header/footer scaffolding.

Usage (programmatic):
  python _split_section_pair.py <abs path to section> <break_line_1_indexed> <a_title> <a_short_desc> <b_title> <b_short_desc> <a_suffix_label> <b_suffix_label>

Where:
- break_line_1_indexed is the line where the SECOND half begins (the line that has the first h2 of part B).
- All content from <main ...> opening up to (but not including) that line goes into A's body.
- All content from that line forward, up to (but not including) the closing </main>, goes into B's body.
- The shared head and footer scaffolding is duplicated.

This script does NOT do cross-file nav updates - it only writes the two new section files.
The caller is responsible for updating the chapter index, neighboring section prev/next
pointers, cross-references in the rest of the book, and deleting the original file.

By convention:
- A keeps the prereqs block.
- B does NOT include the prereqs block; instead it gets a one-paragraph "from <a>" intro after the big-picture callout.
- A's whats-next points to B.
- B's whats-next points to the next-section-after-the-original (caller passes b_next_href and b_next_label).
- A and B's title <h1> get the new title strings.
"""
import re
import sys
from pathlib import Path


def split_html(path: str, break_line: int,
               a_title: str, a_desc: str,
               b_title: str, b_desc: str,
               a_suffix: str, b_suffix: str,
               b_intro_html: str,
               a_next_href: str, a_next_label: str, a_next_title: str,
               b_prev_href: str, b_prev_label: str, b_prev_title: str,
               b_next_href: str, b_next_label: str, b_next_title: str,
               a_prev_href: str = None, a_prev_label: str = None, a_prev_title: str = None,
               whatsnext_a: str = None, whatsnext_b: str = None):
    p = Path(path)
    lines = p.read_text(encoding="utf-8").splitlines(keepends=False)

    # Locate key landmarks (1-indexed)
    main_open = None
    main_close = None
    title_line = None
    desc_line = None
    h1_block_line = None
    whatsnext_open = None
    biblio_open = None
    prereqs_open = None
    prereqs_close = None
    nav_open = None
    nav_close = None

    for i, ln in enumerate(lines):
        if '<title>' in ln and title_line is None:
            title_line = i
        if '<meta content=' in ln and 'name="description"' in ln and desc_line is None:
            desc_line = i
        if ln.startswith('<main class="content"') and main_open is None:
            main_open = i
        if ln.startswith('<h1>') and h1_block_line is None:
            h1_block_line = i
        if '<div class="prerequisites">' in ln and prereqs_open is None:
            prereqs_open = i
        if '<div class="whats-next">' in ln and whatsnext_open is None:
            whatsnext_open = i
        if '<details class="bibliography-collapsible">' in ln and biblio_open is None:
            biblio_open = i
        if '<nav class="chapter-nav">' in ln and nav_open is None:
            nav_open = i
        if ln.startswith('</main>') and main_close is None:
            main_close = i
        if '</nav>' in ln and nav_open is not None and nav_close is None and i > nav_open:
            nav_close = i

    # Locate prereqs close (next </div> after open at same indentation)
    if prereqs_open is not None:
        depth = 0
        for j in range(prereqs_open, len(lines)):
            if '<div' in lines[j]:
                depth += lines[j].count('<div')
            if '</div>' in lines[j]:
                depth -= lines[j].count('</div>')
                if depth == 0:
                    prereqs_close = j
                    break

    if main_open is None or main_close is None or h1_block_line is None:
        raise RuntimeError(f"Couldn't locate critical landmarks in {path}: main_open={main_open}, main_close={main_close}, h1_block_line={h1_block_line}")

    # The break_line is the FIRST line of B's content (0-indexed = break_line-1)
    bidx = break_line - 1

    # Split content: A = lines[main_open+1 .. bidx-1], B = lines[bidx .. whatsnext_open-1]
    # Note A's body excludes the whats-next, biblio, nav-chapter, footer that we re-attach.
    # B's body excludes the same and goes up to whats-next.

    # End of A body (exclusive): bidx
    # Start of B body: bidx
    # End of B body (exclusive): whatsnext_open (if present) else biblio_open else nav_open else main_close
    body_tail_start = whatsnext_open
    if body_tail_start is None:
        body_tail_start = biblio_open
    if body_tail_start is None:
        body_tail_start = nav_open
    if body_tail_start is None:
        body_tail_start = main_close

    # Pre-body (head + body open through h1 line)
    pre_main_a = lines[:main_open + 1]  # includes the <main ...> opening tag line
    pre_main_b = list(pre_main_a)  # we'll mutate per-file (title/desc/h1)

    # Identify the front-matter region (between main_open+1 and first <h2>)
    # We need: epigraph + big-picture + prereqs (in A only) + opening image/figure if any.
    # Front-matter A = lines[main_open+1 .. (first_h2_in_a or bidx) -1]
    # The cleanest approach: keep the entire front-matter for both, then for B remove the prereqs block.

    # Find first <h2 line index (after main_open)
    first_h2 = None
    for j in range(main_open + 1, len(lines)):
        if re.match(r'^<h2[\s>]', lines[j]):
            first_h2 = j
            break
    if first_h2 is None:
        raise RuntimeError(f"No <h2 found in {path}")

    front_matter = lines[main_open + 1: first_h2]  # epigraph, big-picture, prereqs, maybe an opening figure

    # A body = front_matter + content_a_h2_block, B body = front_matter (sans prereqs) + content_b_h2_block
    a_body_h2 = lines[first_h2: bidx]
    b_body_h2 = lines[bidx: body_tail_start]

    # Build B's front matter: front_matter with prereqs block removed
    if prereqs_open is not None and prereqs_close is not None:
        # prereqs_open and prereqs_close are absolute indices into `lines`
        rel_open = prereqs_open - (main_open + 1)
        rel_close = prereqs_close - (main_open + 1)
        b_front_matter = front_matter[:rel_open] + front_matter[rel_close + 1:]
    else:
        b_front_matter = list(front_matter)

    # Optionally insert b_intro_html after the big-picture callout in b_front_matter.
    if b_intro_html:
        # Find end of big-picture callout in b_front_matter
        depth = 0
        in_bp = False
        bp_end = None
        for k, ln in enumerate(b_front_matter):
            if '<div class="callout big-picture">' in ln:
                in_bp = True
                depth = ln.count('<div')
                depth -= ln.count('</div>')
                if depth == 0:
                    bp_end = k
                    break
                continue
            if in_bp:
                depth += ln.count('<div')
                depth -= ln.count('</div>')
                if depth == 0:
                    bp_end = k
                    break
        if bp_end is not None:
            b_front_matter = b_front_matter[:bp_end + 1] + [b_intro_html] + b_front_matter[bp_end + 1:]

    # Build whats-next blocks (per A and per B)
    if whatsnext_a is None:
        whatsnext_a = (
            f'<div class="whats-next">\n'
            f'<h3 id="what-s-next">What\'s Next?</h3>\n'
            f'<p>In the next part of this section, <a href="{a_next_href}">{a_next_label}: {a_next_title}</a>, {a_desc.lower()}</p>\n'
            f'</div>'
        )
    if whatsnext_b is None:
        whatsnext_b = (
            f'<div class="whats-next">\n'
            f'<h3 id="what-s-next">What\'s Next?</h3>\n'
            f'<p>In the next section, <a href="{b_next_href}">{b_next_label}: {b_next_title}</a>, we continue building on the topics covered here.</p>\n'
            f'</div>'
        )

    # Tail (biblio + chapter-nav + footer + closing main + script + body/html)
    # Use original biblio
    biblio_block = []
    if biblio_open is not None:
        # End of biblio: matching </details>
        bib_end = None
        for j in range(biblio_open + 1, len(lines)):
            if '</details>' in lines[j]:
                bib_end = j
                break
        if bib_end is not None:
            biblio_block = lines[biblio_open:bib_end + 1]

    # Closing main and script and body/html
    post_nav = lines[nav_close + 1: ] if nav_close is not None else lines[main_close:]
    # Actually we want: from </main> onward, original lines
    post_main = lines[main_close:]

    # Build A's chapter-nav
    if a_prev_href is None:
        # Use original prev
        # Find original prev a tag in chapter-nav
        # We'll just preserve the original prev from the file.
        if nav_open is not None and nav_close is not None:
            orig_nav = lines[nav_open:nav_close + 1]
            m = re.search(r'<a class="prev" href="([^"]+)"><span class="nav-label">[^<]*</span><span class="nav-num">([^<]+)</span><span class="nav-title">([^<]+)</span></a>', "\n".join(orig_nav))
            if m:
                a_prev_href = m.group(1)
                a_prev_label = m.group(2)
                a_prev_title = m.group(3)
        if a_prev_href is None:
            a_prev_href = "#"
            a_prev_label = "Previous"
            a_prev_title = "Previous Section"

    # Up link (in chapter) -- preserve from original
    up_match = None
    if nav_open is not None and nav_close is not None:
        orig_nav = "\n".join(lines[nav_open:nav_close + 1])
        m = re.search(r'<a class="up" href="([^"]+)"><span class="nav-label">[^<]*</span><span class="nav-num">([^<]+)</span><span class="nav-title">([^<]+)</span></a>', orig_nav)
        if m:
            up_match = (m.group(1), m.group(2), m.group(3))
    if up_match is None:
        up_match = ("index.html", "Chapter", "Chapter")

    def chapter_nav(prev_href, prev_label, prev_title, up_href, up_label, up_title, next_href, next_label, next_title):
        return (
            '<nav class="chapter-nav">\n'
            f'<a class="prev" href="{prev_href}"><span class="nav-label">Previous</span><span class="nav-num">{prev_label}</span><span class="nav-title">{prev_title}</span></a>\n'
            f'<a class="up" href="{up_href}"><span class="nav-label">In Chapter</span><span class="nav-num">{up_label}</span><span class="nav-title">{up_title}</span></a>\n'
            f'<a class="next" href="{next_href}"><span class="nav-label">Next</span><span class="nav-num">{next_label}</span><span class="nav-title">{next_title}</span></a>\n'
            '</nav>'
        )

    nav_a = chapter_nav(a_prev_href, a_prev_label, a_prev_title, up_match[0], up_match[1], up_match[2],
                        a_next_href, a_next_label, a_next_title)
    nav_b = chapter_nav(b_prev_href, b_prev_label, b_prev_title, up_match[0], up_match[1], up_match[2],
                        b_next_href, b_next_label, b_next_title)

    # Get the footer line and post-nav scripts (from after the chapter-nav to end of file)
    # post_nav (everything after the closing </nav>): includes <footer>, </main>, <script>, etc.
    if nav_close is not None:
        tail_after_nav = lines[nav_close + 1:]
    else:
        # No chapter-nav block? unlikely.
        tail_after_nav = lines[main_close:]

    # Now mutate <title> and <meta description> for A and B
    def make_pre_main(orig_pre_main, new_title, new_desc, new_h1_title, suffix_label):
        out = list(orig_pre_main)
        for k, ln in enumerate(out):
            if '<title>' in ln:
                # Replace the entire <title>...</title>
                out[k] = re.sub(r'<title>[^<]*</title>', f'<title>{new_title}</title>', ln)
            if '<meta content=' in ln and 'name="description"' in ln:
                # Replace the content="..." string
                out[k] = re.sub(r'<meta content="[^"]*"', f'<meta content="{new_desc}"', ln)
            if ln.startswith('<h1>'):
                # Replace <h1>OLD</h1><div class="page-current">Section X.Y</div>
                out[k] = re.sub(
                    r'<h1>[^<]*</h1><div class="page-current">Section ([^<]+)</div>',
                    lambda m: f'<h1>{new_h1_title}</h1><div class="page-current">Section {m.group(1).strip()}{suffix_label}</div>',
                    ln
                )
        return out

    # Build full A and B documents
    a_lines = (
        make_pre_main(pre_main_a, f"Section {extract_section_num(path, a_suffix)}: {a_title}", f"Section {extract_section_num(path, a_suffix)}: {a_title}. {a_desc}", a_title, a_suffix)
        + front_matter
        + a_body_h2
        + [whatsnext_a]
        + biblio_block
        + [nav_a]
        + tail_after_nav
    )

    b_lines = (
        make_pre_main(pre_main_b, f"Section {extract_section_num(path, b_suffix)}: {b_title}", f"Section {extract_section_num(path, b_suffix)}: {b_title}. {b_desc}", b_title, b_suffix)
        + b_front_matter
        + b_body_h2
        + [whatsnext_b]
        + biblio_block
        + [nav_b]
        + tail_after_nav
    )

    a_out = p.with_name(p.stem + 'a.html')
    b_out = p.with_name(p.stem + 'b.html')

    a_out.write_text("\n".join(a_lines) + "\n", encoding="utf-8")
    b_out.write_text("\n".join(b_lines) + "\n", encoding="utf-8")

    return str(a_out), str(b_out)


def extract_section_num(path: str, suffix: str) -> str:
    # path like /.../section-0.3.html -> "0.3" + suffix
    name = Path(path).stem  # "section-0.3"
    m = re.match(r'section-(.+)$', name)
    if m:
        return m.group(1) + suffix
    return name + suffix


if __name__ == "__main__":
    print("This module is intended to be imported / called from a driver script.")
