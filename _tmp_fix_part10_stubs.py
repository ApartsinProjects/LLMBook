"""
Rewrite the 8 Part-10 chapter-index stubs that still say "TODO author this".
For each, replace:
- Big-Picture callout body
- section-card-list to point at the real section titles
- whats-next prose (we are allowed to fix what comes next in chapter pages
  since the task only forbids editing the div content; we still leave it intact
  but with corrected target links)
- chapter-nav prev/up/next links
"""
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook/part-10-idea-to-product")

# Module-by-module config
# Each tuple: (module-dir, chapter_num, big_picture_body, sections_list_html, prev, next)
# prev/next: (href, num, title)

P10_PREV = ("../../part-9-safety-security-ethics/index.html", "Part IX", "Safety, Security &amp; Ethics")

def section_cards(num, sections):
    out = []
    for s_num, s_title in sections:
        out.append(f'<a class="section-card" href="section-{s_num}.html"><span class="section-num">Section {s_num}</span><span class="section-title">{s_title}</span></a>')
    return "\n".join(out)


CONFIG = [
    # (slug, chapter_num, big_picture, sections, prev_module_slug, prev_chapter_num, prev_title, next_module_slug, next_chapter_num, next_title)
    (
        "module-40-ideation", 40,
        "Every shipped LLM product starts as an answer to a question: is this a problem the model actually solves? Ideation is the disciplined search for problems whose underlying shape matches what an LLM is good at, where the user already pays for a worse solution, and where the data feedback loop will close. This chapter teaches the filters that separate a real opportunity from a thin wrapper.",
        [("40.1", "Ideation: Finding LLM-Worthy Problems")],
        None, None, None,
        "module-41-product-management", 41, "LLM Product Management",
    ),
    (
        "module-41-product-management", 41,
        "Once a real problem is in your hands, the work shifts from \"is there a there there?\" to \"how do we ship the smallest thing that proves it?\". This chapter is the AI product manager's playbook: turning a hypothesis into a spec, designing evals as a first-class artifact, and running the iteration loop on a probabilistic system.",
        [("41.1", "From Hypothesis to Product Spec"),
         ("41.2", "LLM Product Management")],
        "module-40-ideation", 40, "Ideation: Finding LLM-Worthy Problems",
        "module-42-strategy-prioritization", 42, "LLM Strategy &amp; Use Case Prioritization",
    ),
    (
        "module-42-strategy-prioritization", 42,
        "Even after you have a good problem and a working spec, you still have to pick which version to build first, which vendor to bet on, and whether to roll your own model. This chapter covers strategy and use-case prioritization: build vs. buy, vendor evaluation, and the value-frontier framework that orders a portfolio of LLM bets.",
        [("42.1", "LLM Strategy &amp; Use Case Prioritization"),
         ("42.2", "LLM Vendor Evaluation &amp; Build vs. Buy"),
         ("42.3", "LLM Strategy &amp; Use Case Prioritization"),
         ("42.4", "LLM Vendor Evaluation &amp; Build vs. Buy")],
        "module-41-product-management", 41, "LLM Product Management",
        "module-43-vibe-coding", 43, "Prototyping via Vibe-Coding",
    ),
    (
        "module-43-vibe-coding", 43,
        "Strategy meets keyboard here. Vibe-coding is the practice of building real working software with an LLM as your pair, riding the rapid prototyping cycle without losing engineering discipline. This chapter covers the workflow, the tools (Cursor, Claude Code, Cline), and the failure modes you have to keep eyes on.",
        [("43.1", "Prototyping via Vibe-Coding"),
         ("43.2", "Vibe-Coding &amp; AI-Assisted Software Engineering")],
        "module-42-strategy-prioritization", 42, "LLM Strategy &amp; Use Case Prioritization",
        "module-44-mvp", 44, "Building the MVP",
    ),
    (
        "module-44-mvp", 44,
        "An MVP for an AI product is not the same as for deterministic software. The smallest thing that proves your hypothesis has to include a minimum viable eval, a clear quality bar, and an honest answer for what happens when the model is wrong. This chapter shows you how to scope and ship that smallest thing.",
        [("44.1", "Building the MVP")],
        "module-43-vibe-coding", 43, "Prototyping via Vibe-Coding",
        "module-45-prototype-to-production", 45, "From Idea to Product Hypothesis",
    ),
    (
        "module-46-compute-planning", 46,
        "Once the MVP works, you need to know what it costs to serve at the volume you actually expect. This chapter covers compute planning and infrastructure: sizing GPUs, picking an inference stack, integrating with enterprise systems, and avoiding the two failure modes (over-provision and starve).",
        [("46.1", "LLM Compute Planning &amp; Infrastructure"),
         ("46.2", "Enterprise Integration Patterns for LLM Systems"),
         ("46.3", "LLM Compute Planning &amp; Infrastructure"),
         ("46.4", "Enterprise Integration Patterns for LLM Systems")],
        "module-45-prototype-to-production", 45, "From Idea to Product Hypothesis",
        "module-47-scaling-economics", 47, "Scaling Economics: Unit Costs &amp; ROI",
    ),
    (
        "module-47-scaling-economics", 47,
        "Every LLM dollar buys something specific, and at some volume the unit economics either work or they don't. This chapter covers scaling economics: ROI measurement, value attribution, and the economic design of LLM systems so that growth doesn't kill the margin.",
        [("47.1", "ROI Measurement &amp; Value Attribution"),
         ("47.2", "Economic Design of LLM Systems"),
         ("47.3", "ROI Measurement &amp; Value Attribution"),
         ("47.4", "Economic Design of LLM Systems")],
        "module-46-compute-planning", 46, "Compute Planning &amp; Infrastructure",
        "module-48-shipping-deploying", 48, "Shipping and Scaling AI Products",
    ),
    (
        "module-49-post-launch-monitoring", 49,
        "Shipping is not the finish line for an AI product, it's the start of the second loop. This chapter covers post-launch monitoring and iteration: eval-in-prod, drift detection, and the retraining cadence that keeps a model honest as the world it answers questions about keeps moving.",
        [("49.1", "Post-Launch Monitoring and Iteration")],
        "module-48-shipping-deploying", 48, "Shipping and Scaling AI Products",
        "module-50-tools-of-the-trade", 50, "Tools of the Trade: Idea-to-Product Toolkit",
    ),
]


for cfg in CONFIG:
    (slug, ch_num, big_picture, sections,
     prev_slug, prev_num, prev_title,
     next_slug, next_num, next_title) = cfg
    path = ROOT / slug / "index.html"
    if not path.exists():
        print(f"MISSING: {path}")
        continue
    text = path.read_text(encoding="utf-8")

    # Replace big-picture
    new_bp = (
        '<div class="callout big-picture">\n'
        '<div class="callout-title">Big Picture</div>\n'
        f'<p>{big_picture}</p>\n'
        '</div>'
    )
    text = re.sub(
        r'<div class="callout big-picture">\s*<div class="callout-title">Big Picture</div>\s*<p>TODO author this big-picture callout[^<]*</p>\s*</div>',
        new_bp,
        text,
        count=1,
    )

    # Replace section-card-list block
    cards_html = section_cards(ch_num, sections)
    new_sec = f'<h2>Sections in This Chapter</h2>\n<div class="section-card-list">\n{cards_html}\n</div>'
    text = re.sub(
        r'<h2>Sections in This Chapter</h2>\s*<div class="section-card-list">.*?</div>',
        new_sec,
        text,
        count=1,
        flags=re.DOTALL,
    )

    # Replace whats-next prose (the *content* paragraph that says TODO)
    next_section_label = f"Section {sections[0][0]}: {sections[0][1]}"
    next_section_href = f"section-{sections[0][0]}.html"
    new_whats = (
        f'<p>In the next section, <a href="{next_section_href}">{next_section_label}</a>, '
        f"we get to work on the chapter's first concrete topic. After this chapter you continue to "
        f'<a href="../{next_slug}/index.html">Chapter {next_num}: {next_title}</a>.</p>'
    )
    text = re.sub(
        r'<p>TODO author this\. Outline where this chapter sits[^<]+</p>',
        new_whats,
        text,
        count=1,
    )

    # Replace chapter-nav
    if prev_slug:
        prev_href = f"../{prev_slug}/index.html"
        prev_nav_num = f"Chapter {prev_num}"
        prev_nav_title = prev_title
    else:
        prev_href = "../index.html"
        prev_nav_num = "Part X"
        prev_nav_title = "Idea to Product"
    next_href = f"../{next_slug}/index.html"
    new_nav = (
        '<nav class="chapter-nav">\n'
        f'<a class="prev" href="{prev_href}"><span class="nav-label">Previous</span><span class="nav-num">{prev_nav_num}</span><span class="nav-title">{prev_nav_title}</span></a>\n'
        '<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">Part X</span><span class="nav-title">Idea to Product</span></a>\n'
        f'<a class="next" href="{next_href}"><span class="nav-label">Next</span><span class="nav-num">Chapter {next_num}</span><span class="nav-title">{next_title}</span></a>\n'
        '</nav>'
    )
    text = re.sub(
        r'<nav class="chapter-nav">.*?</nav>',
        new_nav,
        text,
        count=1,
        flags=re.DOTALL,
    )

    path.write_text(text, encoding="utf-8")
    print(f"Updated: {slug}")
