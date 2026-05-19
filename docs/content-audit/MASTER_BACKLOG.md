# Master Audit Backlog (consolidated)

Consolidated from 4 audit-extract agents reading 14 audit reports. Items filtered to remove those already resolved by Waves 33-37.

**Legend:** `[P0]` critical / `[P1]` must-fix / `[P2]` polish / `[P3]` nice-to-have
**Type:** SWEEP (regex/Python script) / AUTHORING (per-chapter content) / AGENT (delegate) / DECISION (user input)

---

## P0 SWEEPABLE (immediate batch — Wave 38a)

| # | Finding | Source | Type |
|---|---|---|---|
| 1 | section-5.1 has 7 mid-content chapter-nav blocks with broken `#6-X-` anchors | cycle-3 G1 | SWEEP |
| 2 | section-5.2 has 8 inflated chapter-nav blocks with broken anchors | cycle-3 G1 | SWEEP |
| 3 | section-10.6 has 5 mid-content chapter-nav blocks labelled "Chapter 12"; section-10.8 has 2 | cycle-3 G1 | SWEEP |
| 4 | section-14.2 has 3 chapter-nav blocks with stale `#16-2-` anchors | cycle-3 G1 | SWEEP |
| 5 | section-19.2 has 10 chapter-nav blocks with `#21-2-`/`#21-3-` anchors; section-19.3 has 5 | cycle-3 G1 | SWEEP |
| 6 | Orphan content after `</main>`: 5 pages concatenate tot-subsection blocks each with own chapter-nav+footer (section-19.3.html has 5 pairs) | random_detector | SWEEP |
| 7 | U+FFFD replacement-character corruption in duplicated footers | random_detector | SWEEP |
| 8 | Placeholder text in production: `# implement <function_name>` Python comments; `Code Fragment h.7.N` appendix-letter placeholders; `<em>(Diagram to commission for final styling.)</em>` | random_detector | SWEEP |
| 9 | Section 34.1 stray extra `</strong>` after colon + "1.1 Classical IE" artifact prefix in `<em>` | anomalous_styling | SWEEP |

## P1 SWEEPABLE (Wave 38b)

| # | Finding | Source | Type |
|---|---|---|---|
| 10 | Sec 47.1: 12 H3s carry id=`30-1-N` + visible `49.1.N` + hrefs `#47-1-N` — three-way mismatch | cycle-3 G3 | SWEEP |
| 11 | Sec 57.4: breadcrumb + pagefind say "Chapter 44"; 3 code fragments say "44.14.X" | cycle-3 G3 | SWEEP |
| 12 | Ch 44 chapter-index breadcrumb says "Part VIII" | cycle-3 G3 | SWEEP |
| 13 | Ch 47 chapter-index title/meta say "Safety, Ethics & Regulation" (wrong) | cycle-3 G3 | SWEEP |
| 14 | 43 section files with stale breadcrumb chapter titles vs canonical H1 (Ch 43/44/47/52/54/55/42/57/60) | cycle-3 G3 | SWEEP |
| 15 | 8 module-index titles/meta still zero-padded "Chapter 00/01/02..."; module-02/03/04 also off-by-one | cycle-3 G1 | SWEEP |
| 16 | 4 part-index part-overview prose cite stale chapter ranges (Part I "0-6", II "7-12"...) | cycle-3 G1 | SWEEP |
| 17 | 14 chapter-opener figcaption figures off-by-1/2 (module-02 "Figure 3.0.1", module-15 "Figure 17.0.1") | cycle-3 G1 | SWEEP |
| 18 | 7 section-17.X.html files still link to "Chapter 17: PEFT" — Wave 16 rename never propagated | cycle-3 G1 | SWEEP |
| 19 | section-6.9 duplicated in part-2/index lines 56-57 + module-06/index lines 122-126 & 128-133 | cycle-3 G1 | SWEEP |
| 20 | 28+ Part-1 section files have zero-padded `<span class="nav-num">Chapter 00/01/02</span>` | cycle-3 G1 | SWEEP |
| 21 | module-09 concept-link tooltips: `title="Section Q.4"` etc | cycle-3 G1 | SWEEP |
| 22 | section-3.1 Code Fragment captions stale a/b/c suffix variants | cycle-3 G1 | SWEEP |
| 23 | 256 H2 headings in Chs 20/21/22(1st half)/24 use bare `1, 2, 3` instead of `N.M.K` (32 files) | cycle-3 G2 | SWEEP |
| 24 | Cross-part anchor breakage: section-5.1 → 14.1, module-19/index → Part 7 with `#21-3-` | cycle-3 G1 | SWEEP |
| 25 | Code-comment stale section refs: section-32.2:192 `# Section 32.5` (now 32.3); section-22.9 `# Section 38.2` | cycle-3 G2 | SWEEP |
| 26 | 256 H2 headings in Chs 20/21/22(1st)/24 use bare numbering | cycle-3 G2 | SWEEP |
| 27 | Module-67 breadcrumb labels: secs 67.4-67.6 say "Chapter 64"; 67.7-67.8 "Chapter 65"; 67.9-67.15 "Chapter 68" — should be Chapter 67 | cycle-3 G4 | SWEEP |
| 28 | Module-78 breadcrumb labels: 78.1-78.5 say "Chapter 73"; 78.6-78.7 "Chapter 74"; 78.8-78.10 "Chapter 75" | cycle-3 G4 | SWEEP |
| 29 | Sec 49.3/49.4 `<title>` say "Section 49.6"/"49.7" (off-by-3) | cycle-3 G3 | SWEEP |
| 30 | Ch 41 sections: `</main>` positioned AFTER `<footer>` (inversion) | anomalous_styling | SWEEP |
| 31 | Empty `<nav class="section-nav"></nav>` in 36.1/36.2/36.3/36.4 | anomalous_styling | SWEEP |
| 32 | Stale `<em>` numeric prefix inside `comparison-table-title` (`Table 51.3.1: 39.3.1 ...`) — 7 pages | random_detector | SWEEP |
| 33 | Bare prose section/chapter references not hyperlinked: "Section 22.1", "Chapter 29" — 7+ pages | random_detector | SWEEP |
| 34 | `<figure>` wrapping `<table>` labeled "Figure N.M.K" instead of "Table" — 7 pages | random_detector | SWEEP |
| 35 | Heading-text drift vs anchor IDs (e.g., `<h2 id="41-2-5-message-history-...">Message format and protocol libraries</h2>`) | random_detector | SWEEP |
| 36 | Trailing whitespace inside `<strong>` (9 pages) | random_detector | SWEEP |
| 37 | `<h2>` inside `<div class="whats-next">` instead of `<h3>` — 3 pages | random_detector | SWEEP |
| 38 | Lowercase acronym anchor text ("llm apis" → "LLM APIs") | random_detector | SWEEP |

## P0/P1 AUTHORING (focused agent dispatches — Wave 38c)

| # | Finding | Source | Type |
|---|---|---|---|
| 39 | Wave 14 deferred: Ch 41 sections 41.1-41.5 still contain RETRIEVAL/RAG content instead of Conversational AI tooling | REMEDIATION-PLAN | AUTHORING |
| 40 | §19.2 Libraries & Frameworks: 317KB/14k words/13 H2 — needs split | wave28 + GIANT_SECTION | AUTHORING |
| 41 | §37.3 Memory & Context (203KB/8k words/32 H2) — needs split | wave28 | AUTHORING |
| 42 | §47.1 LLM Security Threats (188KB/12k words/36 H2) + 12 broken H3 IDs — needs split + ID fix | wave28 + cycle-3 G3 | AUTHORING |
| 43 | §45.2 Libraries & Frameworks (171KB) — needs split | wave28 | AUTHORING |
| 44 | §31.4 Document Processing & Chunking (170KB) — needs split | wave28 | AUTHORING |
| 45 | §10.4 Explaining Transformers (160KB) — needs split | wave28 | AUTHORING |
| 46 | §0.3 PyTorch in 90 Minutes (152KB/8k words/38 H2) — needs split | wave28 | AUTHORING |
| 47 | §13.5 Dataset Engineering for LLMs (152KB/6k words) — needs split | wave28 | AUTHORING |
| 48 | Ch 71 (product tools) §71.3-71.5 severely under-content (154-311 words, no big_picture) | wave28 | AUTHORING |
| 49 | Ch 79 (apps tools) §79.1-79.5 severely under-content, 0% bib, 0% images | wave28 | AUTHORING |
| 50 | Ch 51 (security tools) §51.1-51.5 under-content (797-887 words, no big_picture, 0% bib) | wave28 | AUTHORING |
| 51 | 13 chapters with 0% bibliography: Ch 24, 25, 34, 36, 41, 46, 51, 56, 61, 69, 71, 79 | wave28 | AUTHORING |
| 52 | Industry chapters Ch 72-77 uniformly thin (~10KB each, 0% images) — accept as briefs or expand | wave28 | DECISION+AUTHORING |
| 53 | Math-foundations Appendix A: §A.1-A.5 missing big_picture | wave28 | AUTHORING |
| 54 | §25.3 ↔ §25.4 substantive duplication (Jaccard 0.50) | wave28 | AUTHORING |
| 55 | Ch 41 §41.1: no "why does this category exist" historical arc | wave31_32 | AUTHORING |
| 56 | Ch 56 §56.1 needs COMPAS/NYC LL 144 opener; §56.4 needs "prove safety mathematically" counterfactual | wave31_32 | AUTHORING |
| 57 | Ch 61: Colossus 122-day fun-note; four-tier platform stack mental-map; InfiniBand counterfactual | wave31_32 | AUTHORING |
| 58 | Ch 59: "straggler GPU" illustration; parallelism-cube mental-map figure | wave31_32 | AUTHORING |
| 59 | Ch 34: hybrid-as-cascaded-control framing for 34.3; spaCy counterfactual for 34.2 | wave31_32 | AUTHORING |
| 60 | Ch 46: short chapter (126 lines for §46.1); needs density review beyond engagement | wave31_32 | AUTHORING |
| 61 | 59 library-shortcut opportunities still open across Ch 34/35/36/41/46/56/59/61 | library_shortcut | AUTHORING |
| 62 | Ch 34 sections 34.3 placeholder description + 34.5 truncated description | cycle-3 G2 | AUTHORING |
| 63 | Ch 67 ideation sections + Ch 68 vibe-coding sections + Ch 65 containers/k8s sections need RWS template normalization | rws_template | AUTHORING |
| 64 | Hundreds of section descriptions still need rewrite from agent-proposed text (Wave 16) | REMEDIATION-PLAN | AUTHORING |
| 65 | Python code indent-rot in dataclass/function bodies — 10+ pages non-executable | random_detector | AGENT |
| 66 | Code-output disconnected from preceding code (4 iters: 3, 9, 13, 21) | random_detector | AUTHORING |
| 67 | 40 remaining comic / analogy / mental-map opportunities from comic_illustration_audit.md | comic_illustration | AGENT |

## DECISIONS NEEDED (block sweeps/authoring)

| # | Decision | Source |
|---|---|---|
| D1 | Part 2 Tools content in module-10/sections-10.5-10.9: move folder or rebrand breadcrumbs? | cycle-3 G1 |
| D2 | Tokenization (Ch 2) still in module-01: keep as 1.5-1.7 with breadcrumb fix, or extract to module-02? | cycle-3 G1 |
| D3 | Tier 1 section splits: 40.1, 50.1, 52.1 (changes URLs, breaks bookmarks) | split_candidates |
| D4 | Tier 2 section splits: 19.2, 37.3, 3.1, 3.3 (large, may be legitimately deep) | split_candidates |
| D5 | Real-World Scenario: confirm extended 8-field as canonical, sweep 312 callouts | rws_template |
| D6 | Tools-of-the-Trade template policy: consolidate-into-one-page vs standardize-5-section template? | wave28 |
| D7 | Industry chapters Ch 72-77: accept as "industry briefs" or expand to depth-bar? | wave28 |
| D8 | Ch 54 split: Watermarking + Transparency (54.6-54.10) into separate chapter? | REMEDIATION-PLAN |
| D9 | Chapter-nav placement: inside-main (Ch 36/41/56/59/61) vs outside-main (Ch 34/46) | anomalous_styling |
| D10 | H2 case-style: Title-Case (Ch 34/46/59) vs sentence-case (Ch 36/41/56/61) | anomalous_styling |
| D11 | Orphan section 52.2 (Hallucinations) move out of bias chapter; orphan 55.2 (AI Governance) move out of env chapter | REMEDIATION-PLAN |
| D12 | Ch 19 (PEFT) scope rename to "Parameter-Efficient Fine-Tuning, Distillation & Merging" | REMEDIATION-PLAN |

## P2/P3 BACKLOG (deferred polish)

- 116 mild under-content sections (1 flag each)
- 14 chapter-section-size imbalance cases
- 13 sections without sibling image (48.4, 54.6, 57.2, 57.3, 65.4, etc.)
- 7 Big Picture verbatim copy of meta description
- Pygments mis-tokenization of f-string format spec
- Empty `<li>` for worked-through fixes in appendix-b
- Hero alt-text fragmentation (truncated mid-word in 7 modules)
- 5 capstone nav corruption ("Next Next Next Next Next")
- Stale "Part XI" prose residue in 5 module index files
- 190 RWS callouts have valid 6/8 fields but title doesn't start with "Real-World Scenario:"

---

## Status mapping to Waves

- ✅ Waves 33-37: callout consolidation (101), legacy bib (20), pagefind metadata (35), double-strong (245+), GA install (544), hero images (37), callout title prefix (4626), 80 new callouts via 5 agents, 13 comic illustrations.
- 📋 Wave 38 (planned): sweep items 1-38 above (mechanical fixes)
- 📋 Wave 39+ (planned): dispatch authoring agents for items 39-67

Total open items: ~120 (38 sweepable + 29 authoring + 12 decisions + ~40 polish)
