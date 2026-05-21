"""
Custom split for section 30.2 because it has the unusual 'tot-subsection' wrapper layout
(no epigraph, no prerequisites, no top-level big-picture; three <section class="tot-subsection">
blocks each with their own big-picture).

Layout of original section-30.2.html (1004 lines):
  Lines 1-37:    head, body, header (NOT inside main)
  Line 38:       <main ...> opening
  Lines 39-110:  preamble (intro paragraph + h2 30.2.1..30.2.4 + comparison table + key-insight callout)
  Lines 112-418: first tot-subsection: LangChain Agents (Legacy) and Callbacks
  Lines 420-868: second tot-subsection: Agent Frameworks Deep Dive
  Lines 870-967: third tot-subsection body: Multi-Agent Patterns and Topologies
  Lines 967-992: bibliography (inside third tot-subsection)
  Line 994:      </section>  (extraneous close - probably a stray close from one of the tots)

Wait, examining again: opens=4 (3 tot-subsection + 1 bibliography), closes=4. So:
  112 -> 418   tot1
  420 -> 868   tot2
  870 ->       tot3 opens
  969 -> 991   bibliography (inside tot3)
  994:         tot3 closes? actually... details closes at 992, then </section> at 994 closes tot3.
              And there's no outer wrapper.

So:
  30.2a:  preamble + tot1 + tot2 (lines 39..868 from original)
  30.2b:  tot3 (lines 870..994 from original), which already contains the bibliography + closing </section>

But the bibliography is inside the third tot-subsection. For 30.2a we add our own whats-next pointing to 30.2b.
For 30.2b we use the existing whats-next that points to 30.3 (already there at line 962).

The bibliography in 30.2b stays as-is.
For 30.2a we need a small bibliography (or none). Looking at the original, the bibliography is exclusively
about multi-agent topology references; it does not duplicate the LangChain or framework references which
are inline. So we let 30.2a skip the bibliography entirely.

Approach:
  - Copy the head + body + header section (lines 1-37) for both.
  - For 30.2a: lines 1-37 + <main ...> + preamble (39-110) + tot1 (112-418) + tot2 (420-868) +
               our whats-next pointing to 30.2b + chapter-nav (a) + footer + closing tags.
  - For 30.2b: lines 1-37 + <main ...> + intro paragraph (one paragraph linking back to 30.2a) +
               tot3 (870-992) + closing </section> (994) + chapter-nav (b) + footer + closing tags.

For 30.2b we modify the existing whats-next inside tot3 if needed.
"""
import re
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
SRC = BOOK / "part-6-agentic-ai" / "module-30-tools-of-the-trade" / "section-30.2.html"

lines = SRC.read_text(encoding="utf-8").splitlines(keepends=False)
n = len(lines)
print(f"Source has {n} lines.")

# Header block (lines 1..37 -> indices 0..36 inclusive)
# The </header> tag is at line 37 (index 36); main opens at line 38 (index 37).
# We need to mutate lines 16,17,35 for new title/desc/h1.
def make_pre_main(new_title_str, new_desc, new_h1, page_current):
    out = []
    for i, ln in enumerate(lines[:37]):
        if i == 15:  # meta description
            out.append(re.sub(r'<meta content="[^"]*"', f'<meta content="{new_desc}"', ln))
        elif i == 16:  # title
            out.append(re.sub(r'<title>[^<]*</title>', f'<title>{new_title_str}</title>', ln))
        elif i == 34:  # h1
            out.append(f'<h1>{new_h1}</h1><div class="page-current">{page_current}</div>')
        else:
            out.append(ln)
    return out

# Open main
MAIN_OPEN = lines[37]  # the <main class="content"> line

# 30.2a body: preamble + tot1 + tot2 (lines 38..867 -> indices 38..867)
# Lines are 1-indexed; index = line - 1.
preamble_start = 38  # line 39 idx (line 39 = "Agent libraries cluster...")
preamble_end_exclusive = 110  # line 111 idx (line 111 is blank line between <key-insight> and tot1)
tot1_start = 111  # line 112 idx (open tot1)
tot1_end_exclusive = 419  # line 419 idx (line 419 is blank line)
tot2_start = 419  # line 420 idx (open tot2)
tot2_end_exclusive = 869  # line 869 idx (line 869 is blank between tot2 close 868 and tot3 open 870)
tot3_start = 869  # line 870 idx (open tot3)
tot3_end_exclusive = 994  # tot3's closing </section> at line 994 (idx 993)
# Verify
print(f"tot3 start line is: {lines[tot3_start][:80]}")
print(f"tot3 end-1 line is: {lines[tot3_end_exclusive-1][:80]}")

# Sanity: line 994 (idx 993) should be </section>
assert lines[993].strip() == "</section>", f"Expected </section> at line 994, got: {lines[993]}"

# Build pre_main for 30.2a
a_title = "Agent Libraries: LangChain Legacy & Framework Deep Dive"
a_desc = "Agent library landscape, LangChain Agents (Legacy) and callbacks, and a deep dive into modern agent frameworks (LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, Semantic Kernel, smolagents, PydanticAI)."
a_h1 = "Agent Libraries: LangChain &amp; Framework Deep Dive"
a_page = "Section 30.2a"

b_title = "Multi-Agent Patterns &amp; Topologies"
b_desc = "Multi-agent topology catalog: hierarchical (manager plus workers), peer / debate, pipeline, and competitive (best-of-N), with failure modes and canonical frameworks for each."
b_h1 = "Multi-Agent Patterns &amp; Topologies"
b_page = "Section 30.2b"

a_pre = make_pre_main(f"Section 30.2a: {a_title}", f"Section 30.2a: {a_title}. {a_desc}", a_h1, a_page)
b_pre = make_pre_main(f"Section 30.2b: Multi-Agent Patterns & Topologies", f"Section 30.2b: Multi-Agent Patterns and Topologies. {b_desc}", b_h1, b_page)

# 30.2a body
a_body = (
    [MAIN_OPEN]
    + lines[preamble_start:preamble_end_exclusive]
    + lines[tot1_start:tot1_end_exclusive]
    + lines[tot2_start:tot2_end_exclusive]
)

# 30.2a whats-next pointing to 30.2b
a_whatsnext = (
    '<div class="whats-next">\n'
    '<h3 id="what-s-next">What\'s Next?</h3>\n'
    '<p>In the next part of this section, <a href="section-30.2b.html">Section 30.2b: Multi-Agent Patterns &amp; Topologies</a>, we move from single-agent libraries to the topologies that combine multiple agents into one system.</p>\n'
    '</div>'
)

# 30.2a chapter-nav: prev=30.1, next=30.2b
a_nav = (
    '<nav class="chapter-nav">\n'
    '<a class="prev" href="section-30.1.html"><span class="nav-label">Previous</span><span class="nav-num">Section 30.1</span><span class="nav-title">Platforms</span></a>\n'
    '<a class="up" href="index.html"><span class="nav-label">In Chapter</span><span class="nav-num">Chapter 30</span><span class="nav-title">Tools of the Trade: Agent Stack</span></a>\n'
    '<a class="next" href="section-30.2b.html"><span class="nav-label">Next</span><span class="nav-num">Section 30.2b</span><span class="nav-title">Multi-Agent Patterns &amp; Topologies</span></a>\n'
    '</nav>'
)

# Footer + closing main/body/html (preserved from end of original)
# Original closing: <nav>...</nav> at 996-1000, then <footer> at 1001, then </main> 1002, </body> 1003, </html> 1004
# We need only the post-nav tail.
footer_and_close = '<footer><p>Fifteenth Edition, 2026 · <a href="../../toc.html">Contents</a></p></footer>\n</main>\n</body>\n</html>'

a_lines = (
    a_pre
    + a_body
    + [a_whatsnext]
    + [a_nav]
    + [footer_and_close]
)

# 30.2b body: an intro paragraph + tot3 (which already has a whats-next and bibliography)
b_intro = '<p>This continuation of <a href="section-30.2a.html">Section 30.2a</a> picks up after the single-agent libraries and moves to the topologies that combine multiple agents into one system. It catalogues the four multi-agent topologies in production (hierarchical, peer / debate, pipeline, competitive), names the canonical frameworks for each, and tabulates the failure modes you should expect.</p>'

# tot3 lines: from idx 869 (line 870, the <section> open) through idx 993 (line 994, the </section> close)
# But we need to modify the existing whats-next which points to section-30.3. That stays.
# We also need to update self-references in the tot3 body that point to section-30.2.html#anchor.
# Skip those for now -- the global xref rewrite handles them.

b_tot3 = lines[tot3_start:tot3_end_exclusive]  # idx 869..993, includes the closing </section> at 994 (idx 993)

b_nav = (
    '<nav class="chapter-nav">\n'
    '<a class="prev" href="section-30.2a.html"><span class="nav-label">Previous</span><span class="nav-num">Section 30.2a</span><span class="nav-title">Agent Libraries: LangChain &amp; Framework Deep Dive</span></a>\n'
    '<a class="up" href="index.html"><span class="nav-label">In Chapter</span><span class="nav-num">Chapter 30</span><span class="nav-title">Tools of the Trade: Agent Stack</span></a>\n'
    '<a class="next" href="section-30.3.html"><span class="nav-label">Next</span><span class="nav-num">Section 30.3</span><span class="nav-title">Datasets &amp; Benchmarks</span></a>\n'
    '</nav>'
)

b_lines = (
    b_pre
    + [MAIN_OPEN]
    + [b_intro]
    + b_tot3
    + [b_nav]
    + [footer_and_close]
)

a_path = SRC.with_name("section-30.2a.html")
b_path = SRC.with_name("section-30.2b.html")

a_path.write_text("\n".join(a_lines) + "\n", encoding="utf-8")
b_path.write_text("\n".join(b_lines) + "\n", encoding="utf-8")

print(f"Wrote: {a_path} ({len(a_lines)} chunks)")
print(f"Wrote: {b_path} ({len(b_lines)} chunks)")
