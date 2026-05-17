# Random Detector Findings — Round 1 (2026-05-17)

Random-sampling audit of 40 HTML pages drawn from the in-scope book tree (parts 1-16, appendices, capstone, front-matter). Seed = 20260517. The first 10 iterations took files of any size; iterations 11-40 filtered to files >=5KB.

The executive summary is regenerated after all 40 iterations and appears at the bottom of this file (search for "## EXECUTIVE SUMMARY").

---

## Iteration 1 (part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.3.html)

### Issue: caption number mismatch inside `comparison-table-title`
- **Where**: line 60 — `<strong>Table 83.3.1:</strong> <em>65.3.1 Frontier benchmarks (2026).</em>`
- **What's wrong**: Caption has two table numbers; the `<em>` label starts with `65.3.1` while the chapter is 83. Stale number from a previous renumber pass.
- **Generalized pattern**: Inside `<div class="comparison-table-title">`, the `<strong>Table X.Y.Z:</strong>` number must match the chapter prefix of the enclosing file path (`section-<chap>.<sec>.html`). Detect when the bold label and the italic descriptor disagree on the leading numeric token. Regex sketch: `<div class="comparison-table-title">\s*<strong>Table (\d+\.\d+\.\d+):</strong>\s*<em>(\d+\.\d+\.\d+)\s` and assert the two captures are equal AND share the chapter prefix of the file.
- **Suggested fix**: Strip stale numeric prefix from `<em>` label; keep only descriptive caption. Cross-check chapter prefix matches file name.
- **TODO**: validator `check_table_caption_numbers.py`; fix `fix_stale_table_caption_numbers.py` (drop leading "N.M.K " from `<em>` content when it differs from the `<strong>Table N.M.K:</strong>`).

### Issue: external link points to unverifiable host
- **Where**: line 47 — `<a href="https://lukasberglund.github.io/MOC-bench/" ...>Mathematical Olympiad Programming benchmark (MOC)</a>`
- **What's wrong**: User-page on github.io for a benchmark; high risk of being either fabricated or transient. Benchmarks should link to a canonical source (arXiv, the maintaining lab, or a HuggingFace dataset card).
- **Generalized pattern**: External links matching `https://[a-z0-9-]+\.github\.io/[^/]+/?` that are presented as canonical benchmark/library references. Detect with `<a href="https://[^/]+\.github\.io/[^"]+"[^>]*>([^<]*\b(bench|benchmark|MOC|GPQA)\b[^<]*)</a>` and flag for verification.
- **Suggested fix**: Replace with the arXiv / HuggingFace / GitHub-repo canonical link.
- **TODO**: validator `check_github_io_benchmark_links.py`; suggest-list (no automated fix).

---
