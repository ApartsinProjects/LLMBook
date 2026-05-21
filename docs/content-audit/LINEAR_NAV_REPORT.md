# Linear next/prev navigation chain audit

Audited **536 pages** across the main book reading order: 15 part starters,
78 chapter starters, and 443 sections. Built a single Python script
(`scripts/audit_linear_nav_chain.py`) that discovers the structure on disk,
computes the expected `<a class="prev">` and `<a class="next">` for every
page per the documented convention (section -> next section, or next
chapter's starter at chapter boundaries, or next part's starter at part
boundaries), and compares against the live HTML. The audit initially flagged
**331 mismatches** (84 section nexts, 81 section prevs, 73 chapter nexts,
78 chapter prevs, 14 part prevs, 2 part nexts) covering wrong destinations
(e.g. section-28.4 -> section-29.1 instead of module-29 starter), wrong
labels (e.g. nav-num "Chapter 1" pointing at a section), and stale titles
(e.g. nav-title "Models" for what is now h1 "Platforms"). After applying the
fix in-place, **286 files were modified** (some pages had two fixable links)
and a re-audit produced **0 mismatches**. End-to-end traversal confirms the
chain is now intact: starting at `part-1/index.html` and following `next`
visits exactly 536 pages and terminates at `section-78.5 -> appendices/`;
starting at `section-78.5` and following `prev` walks the same 536 pages and
exits at `front-matter/copyright.html`. Edge cases handled manually:
section-78.5's "next" was kept pointing at `appendices/index.html` (the
existing convention) rather than re-routing to `capstone/` to avoid
disturbing the appendix chain; front-matter and appendices retain their
own internal navigation per the user's instruction.
