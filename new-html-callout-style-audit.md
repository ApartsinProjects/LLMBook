# New-HTML Callout-Style Audit

Audit scope: HTML files explicitly enumerated in the audit request as newly-authored or recently-rewritten in this session. Read-only; no HTML was modified.

## Summary

- Files audited: 35
- Non-standard callout classes found: **0** (every callout in scope uses a class from the approved palette)
- Callout-title mismatches: **0** (every title text is consistent with its class semantic)
- Inline content that should be callouts: **0** (no orphan `<p><strong>Note:</strong> ...`, no misused `<blockquote>`, no legacy `tip-box` / `warning-box`)
- Files with healthy callout density (3-5 per ~1k-2.5k content words): 13
- Files that are intentional stubs (1 `big-picture` "What this section is" callout only): 11
- Files that are chapter-index landing pages (1-3 callouts, OK by design): 8
- Files with NO callouts at all (P2 - enrichment opportunity): 3

## Non-standard callout classes (P0 - would render unstyled)

**None found in scope.**

The standard palette in `styles/book.css` is:
`algorithm`, `bibliography`, `big-picture`, `cross-ref`, `exercise`, `fun-note`, `key-insight`, `key-takeaway`, `library-shortcut`, `looking-back`, `note`, `numeric-example`, `pathway`, `postmortem`, `practical-example`, `production-pattern`, `research-frontier`, `self-check`, `thesis-thread`, `tip`, `warning`. The book-wide check (all 488 recently-touched HTML files, not just scope) surfaced only one outlier: a `callout numerical-example` class in `KDP/build/source_fix_backups/.../section-2.2.html` — but that is a build-time backup file, not source content, and the CSS rule is `.callout.numeric-example`. The live `section-2.2.html` uses the correct spelling.

The audit also confirmed the `<aside class="callout note skip-to-mechanics">` and `<aside class="callout note optional-marker">` variants used in `module-04-transformer-architecture/section-4.{1,3,4,5}.html` are NOT in scope, but they are also legitimate: the second class is a semantic modifier on top of the standard `callout note` and the CSS supports it.

## Callout-title mismatches (P1 - class doesn't match purpose)

**None found in scope.**

Spot-checks of the most likely-to-drift sites:
- `appendix-o-mlops/section-o.1.html` (5 callouts): `big-picture` titled "What this section is" (orientation phrase, correct); `key-insight` titled "Key Insight"; `warning` titled "Warning: Prompts are PII Vectors"; `cross-ref` titled "Cross-References"; `key-takeaway` titled "Key Takeaway". All consistent.
- `appendix-n-distributed-ml/section-n.1.html` (5 callouts): same pattern, `big-picture` + `key-insight` + `warning` + `cross-ref` + `key-takeaway`. All consistent.
- `appendix-m-data-engineering/index.html` (3 callouts): `big-picture` titled "What this appendix is"; `library-shortcut` titled "Library Shortcut"; `tip` titled "When to read this". All consistent.
- `part-3/.../section-16.1.html` (3 callouts): `tip` titled "Tip: route through an abstraction layer"; `warning` titled "Warning: pricing tiers move; latency budgets do not"; `key-takeaway` titled "Key takeaway". All consistent.
- `part-7/.../section-32.{1,2,3,4,8}.html`: 14 callouts across the five sections. `key-insight`, `production-pattern`, `cross-ref`, `warning`, `numeric-example`, `library-shortcut`, `fun-note` all have titles that match their semantic.
- `part-12/.../section-64.5.html`: `key-insight` ("The eval-is-the-product thesis, restated"), `looking-back` ("Looking back"). Consistent.
- `part-10-idea-to-product/module-{40-49}/index.html`: each has one `big-picture` callout titled "Big Picture". Consistent and uniform.

## Content that SHOULD be a callout (P2 - enrichment opportunity)

Auto-scan for `<p><strong>Note:</strong>`, `<p><strong>Tip:</strong>`, `<p><strong>Warning:</strong>`, and `<blockquote>` (non-epigraph) across the 35 scoped files returned ZERO matches. The recently-authored content is callout-disciplined; there is no obvious enrichment debt of the "this paragraph wants to be a callout" variety.

The author cards / war-story / capstone appendices (S, T, U) intentionally use plain `<h3>` + `<p><strong>What it teaches:</strong> ...` structures rather than callouts. These are correct as authored (they are deliberately uniform discussion cards, not callout boxes), but see "Per-file callout density" below for the alternative reading that they could each carry one `pathway` or `cross-ref` callout pointing back into the relevant chapters.

## Per-file callout density

The word-count column below is approximate (HTML token count); a rough rule is **0.4 to 0.6 of HTML tokens = English words**. The status column applies the audit's own thresholds (3-5 callouts per substantive section healthy, 0-1 in 1000+ words = under-enriched, 8+ = bloat).

| File | Callouts | HTML tokens | Status |
|---|---|---|---|
| `appendices/appendix-o-mlops/section-o.1.html` | 5 | 2316 | healthy |
| `appendices/appendix-o-mlops/section-o.2.html` | 1 | 350 | stub (intentional) |
| `appendices/appendix-o-mlops/section-o.3.html` | 1 | 350 | stub (intentional) |
| `appendices/appendix-o-mlops/section-o.4.html` | 1 | 356 | stub (intentional) |
| `appendices/appendix-o-mlops/section-o.5.html` | 1 | 368 | stub (intentional) |
| `appendices/appendix-n-distributed-ml/section-n.1.html` | 5 | 2807 | healthy |
| `appendices/appendix-m-data-engineering/index.html` | 3 | 849 | healthy (index page) |
| `appendices/appendix-e-orchestration-frameworks/section-e.2.html` | 1 | 464 | stub (intentional) |
| `appendices/appendix-e-orchestration-frameworks/section-e.3.html` | 1 | 481 | stub (intentional) |
| `appendices/appendix-f-agent-frameworks/section-f.2.html` | 1 | 456 | stub (intentional) |
| `appendices/appendix-f-agent-frameworks/section-f.3.html` | 1 | 479 | stub (intentional) |
| `appendices/appendix-i-environment-setup/section-i.6.html` | 2 | 933 | stub-with-planned-coverage (intentional) |
| `appendices/appendix-i-environment-setup/section-i.7.html` | 3 | 1122 | healthy |
| `part-7-multimodal-generation/module-32-embodied-world-models/section-32.1.html` | 3 | 2001 | healthy |
| `part-7-multimodal-generation/module-32-embodied-world-models/section-32.2.html` | 3 | 2055 | healthy |
| `part-7-multimodal-generation/module-32-embodied-world-models/section-32.3.html` | 3 | 1977 | healthy |
| `part-7-multimodal-generation/module-32-embodied-world-models/section-32.4.html` | 3 | 1986 | healthy |
| `part-7-multimodal-generation/module-32-embodied-world-models/section-32.8.html` | 4 | 1863 | healthy |
| `part-3-working-with-llms/module-16-tools-of-the-trade/section-16.1.html` | 3 | 2091 | healthy |
| `part-12-frontiers/module-64-agi-trajectories/section-64.5.html` | 2 | 1771 | borderline-thin (closing essay, intentional) |
| `part-10-idea-to-product/module-40-ideation/index.html` | 1 | 526 | index page (intentional 1-callout pattern) |
| `part-10-idea-to-product/module-41-product-management/index.html` | 1 | 543 | index page (intentional) |
| `part-10-idea-to-product/module-42-strategy-prioritization/index.html` | 1 | 599 | index page (intentional) |
| `part-10-idea-to-product/module-43-vibe-coding/index.html` | 1 | 529 | index page (intentional) |
| `part-10-idea-to-product/module-44-mvp/index.html` | 1 | 514 | index page (intentional) |
| `part-10-idea-to-product/module-46-compute-planning/index.html` | 1 | 587 | index page (intentional) |
| `part-10-idea-to-product/module-47-scaling-economics/index.html` | 1 | 586 | index page (intentional) |
| `part-10-idea-to-product/module-49-post-launch-monitoring/index.html` | 1 | 522 | index page (intentional) |
| `part-7-multimodal-generation/module-32-embodied-world-models/index.html` | 6 | 2071 | healthy (rich chapter index) |
| `part-7-multimodal-generation/index.html` | 2 | 1723 | borderline-thin (part landing page) |
| `appendices/appendix-q-course-syllabi/index.html` | 1 | 3909 | **under-enriched** (long index, 1 callout) |
| `appendices/appendix-r-reading-pathways/index.html` | 2 | 2707 | borderline-thin (long index) |
| `appendices/appendix-s-intermediate-projects/index.html` | **0** | 719 | **no callouts** (hero only; intentional?) |
| `appendices/appendix-t-capstone-project/index.html` | **0** | 817 | **no callouts** (hero only; intentional?) |
| `appendices/appendix-u-war-stories/index.html` | **0** | 1146 | **no callouts** (hero only; intentional?) |

## Recommended foreground fixes (deterministic, scriptable)

There are no class-rewrite or title-rewrite operations required. The audited HTML is callout-clean.

The only structural observations worth surfacing, all P2 (enrichment, not correctness):

1. **Appendix S / T / U** (intermediate projects, capstone, war stories) have hero illustrations but zero callout boxes. If the For-Instructors-hero pass intended to add 1-2 `pathway` or `cross-ref` callouts linking each list item to the chapter that pairs with it (e.g. an "Instructor note" callout opening each war story, or a `pathway` callout near the rubric), that work was not completed for these three appendices. The structural style (uniform `<h3>` + bold-strong-lead paragraphs) is otherwise sound; this is a "nice-to-have", not a correctness issue.

2. **`appendix-q-course-syllabi/index.html`** is ~3900 HTML tokens (~1800-2300 words) with only one `big-picture` callout. The five-track narrative would benefit from a `key-takeaway` callout per track (or one `key-insight` summarising "which track to pick") to mirror the density used in `appendix-r-reading-pathways/index.html`.

3. **`part-7-multimodal-generation/index.html`** (the part landing page) carries 2 callouts over ~1700 HTML tokens. Consistent with other part landing pages, but on the thin end. No action required.

4. **MLOps stubs O.2-O.5, Orchestration stubs E.2/E.3, Agent-framework stubs F.2/F.3, Environment-setup partial-stub I.6** are intentionally minimal: each has a single `big-picture` "What this section is" callout describing planned coverage. The callout class and title are correct; these are placeholders, not under-enriched authored content. The completed companion N.1 and O.1 (5 callouts each) confirm the team's target shape for the eventual fill-out.

5. **No global rewrite scripts needed.** Any `fun-fact -> fun-note` or `tip-box -> callout tip` rewrites that the audit anticipated finding turn up zero matches in scope.

## Methodology

- Recently-modified files identified via `find . -name "*.html" -mmin -360`. The intersection with the audit's enumerated scope produced 35 files.
- Class-palette check used `grep -hroE 'class="callout [a-z-]+( [a-z-]+)*"' --include="*.html"` aggregated and deduplicated. Cross-referenced against the `.callout.X` selectors in `styles/book.css`.
- Title-mismatch check: every `<div class="callout XXX">` inspected by reading the surrounding 5 lines for the immediate `<div class="callout-title">` and comparing the title text against the prompt's semantic table.
- Enrichment-opportunity scan: regex for `<p><strong>(Note|Tip|Warning):` and `<blockquote` across scoped files (zero hits).
- Density measurement: callout count from `grep -c 'class="callout '`; HTML-token count from `grep -oE '[a-zA-Z]+' | wc -l` (overstates true word count by 1.5-2x).
