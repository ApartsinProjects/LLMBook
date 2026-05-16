# Visual Assets Sweep Report

Date: 2026-05-16. Sweep covers broken-images-catalog.md (31 manual queue items) plus
five For-Instructors appendix hero gaps from new-sections-enrichment-audit.md.

## Broken-image queue (31)

### REGENERATED (20)

All saved to the exact path the broken `src` attribute references; the existing
`<figure>` block now resolves on disk.

- `part-9-safety-security-ethics/module-38-agent-safety-security/section-38.1.html` -> `part-9-safety-security-ethics/module-38-agent-safety-security/images/ch24-castle-defense-v3.png`
- `part-9-safety-security-ethics/module-38-agent-safety-security/section-38.2.html` -> `part-9-safety-security-ethics/module-38-agent-safety-security/images/ch26-sandbox-fishbowl.png`
- `part-9-safety-security-ethics/module-38-agent-safety-security/section-38.3.html` -> `part-9-safety-security-ethics/module-38-agent-safety-security/images/ch26-supply-chain-security.png`
- `part-10-idea-to-product/module-41-product-management/section-41.2.html` -> `part-10-idea-to-product/module-41-product-management/images/product-management-juggling.png`
- `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html` -> `part-10-idea-to-product/module-42-strategy-prioritization/images/strategy-use-case-funnel.png`
- `part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html` -> `part-10-idea-to-product/module-42-strategy-prioritization/images/vendor-evaluation-market.png`
- `part-10-idea-to-product/module-43-vibe-coding/section-43.2.html` -> `part-10-idea-to-product/module-43-vibe-coding/images/pair-programming-robot.png`
- `part-10-idea-to-product/module-46-compute-planning/section-46.3.html` -> `part-10-idea-to-product/module-46-compute-planning/images/compute-planning-blueprint.png`
- `part-10-idea-to-product/module-46-compute-planning/section-46.4.html` -> `part-10-idea-to-product/module-46-compute-planning/images/enterprise-integration-plumbing.png`
- `part-10-idea-to-product/module-47-scaling-economics/section-47.3.html` -> `part-10-idea-to-product/module-47-scaling-economics/images/roi-measurement-balance.png`
- `part-10-idea-to-product/module-47-scaling-economics/section-47.4.html` -> `part-10-idea-to-product/module-47-scaling-economics/images/economic-design-token-kitchen.png`
- `part-10-idea-to-product/module-48-shipping-deploying/section-48.5.html` -> `part-10-idea-to-product/module-48-shipping-deploying/images/ch26-observability-dashboard.png`
- `part-10-idea-to-product/module-48-shipping-deploying/section-48.6.html` -> `part-10-idea-to-product/module-48-shipping-deploying/images/ch26-error-recovery-safety-net.png`
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html` -> `part-12-frontiers/module-61-frontier-architectures/images/ch34-world-model-snowglobe.png`
- `part-12-frontiers/module-61-frontier-architectures/section-61.1.html` -> `part-12-frontiers/module-61-frontier-architectures/images/ch34-opener-frontier-telescope.png`
- `part-12-frontiers/module-61-frontier-architectures/section-61.1.html` -> `part-12-frontiers/module-61-frontier-architectures/images/ch34-emergence-mirage.png`
- `part-12-frontiers/module-61-frontier-architectures/section-61.3.html` -> `part-12-frontiers/module-61-frontier-architectures/images/ch34-alternative-architectures-zoo.png`
- `part-12-frontiers/module-62-frontier-theory/section-62.1.html` -> `part-12-frontiers/module-62-frontier-theory/images/ch34-system1-system2-thinking.png`
- `part-12-frontiers/module-62-frontier-theory/section-62.2.html` -> `part-12-frontiers/module-62-frontier-theory/images/ch34-memory-filing-cabinet.png`
- `appendices/appendix-e-orchestration-frameworks/index.html` -> `appendices/appendix-e-orchestration-frameworks/images/chapter-opener.png`

### REMOVED (11)

All entries below had `fig-NN.M.K-...` style filenames whose alt-text described a
structured technical diagram (flow chart, taxonomy tree, decision tree, side-by-side
architecture diagram) that gemini-imagegen cannot faithfully reproduce (text labels
and structured layouts always break). The `<figure>` or `<div class="diagram-container">`
block was replaced with prose that preserves the original caption's information so
the section still works for the reader and remains searchable. These are queued for
technical-diagram-designer at a later sweep.

- `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html` line 200 (`fig-31.1.1-ai-readiness-bars.png`) - reason: structured radar/bar chart, not cartoon
- `part-10-idea-to-product/module-43-vibe-coding/section-43.2.html` line 66 (`fig-27.1.2-fill-in-the-middle-fim-...png`) - reason: code-FIM technical diagram with text labels
- `part-10-idea-to-product/module-46-compute-planning/section-46.3.html` line 287 (`figure-30.5.1.png`) - reason: cost-curve plot with axes
- `part-10-idea-to-product/module-46-compute-planning/section-46.4.html` line 54 (`fig-31.7.1-enterprise-auth-flow.png`) - reason: OIDC/SAML flow diagram
- `part-10-idea-to-product/module-48-shipping-deploying/section-48.5.html` line 66 (`fig-25.3.2-agent-observability-stack.png`) - reason: stack architecture diagram with component labels
- `part-10-idea-to-product/module-48-shipping-deploying/section-48.6.html` line 62 (`fig-25.4.2-error-recovery-decision.png`) - reason: decision tree
- `part-12-frontiers/module-61-frontier-architectures/section-33.4.html` line 67 (`fig-33.4.2-world-model-architecture.png`) - reason: encoder/dynamics/policy architecture diagram
- `part-12-frontiers/module-61-frontier-architectures/section-61.3.html` line 100 (`fig-33.3.2-mamba-vs-transformer.png`) - reason: side-by-side block diagram
- `part-12-frontiers/module-61-frontier-architectures/section-61.3.html` line 301 (`fig-33.3.3-attention-variants-taxonomy.png`) - reason: taxonomy tree
- `part-12-frontiers/module-61-frontier-architectures/section-61.4.html` line 70 (`fig-34.10-domain-tokenization.png`) - reason: pipeline flow diagram
- `part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html` line 57 (`fig-33.9.1-tool-orchestration-economy.png`) - reason: orchestration architecture flow

### DEFERRED (0)

All 31 catalog entries resolved.

## For-Instructors hero gaps (5)

For each appendix, generated `images/chapter-opener.png` (16:9, 1K) and inserted a
`<figure class="illustration chapter-opener">` block immediately after the
`<main class="content">` meta-injected spans, before the first content block.

- Appendix O: `appendices/appendix-o-course-syllabi/images/chapter-opener.png` - prompt: classroom with 5 robot students in different graduation caps, instructor at chalkboard pointing at a branching tree of five tracks growing out of a foundations trunk.
- Appendix P: `appendices/appendix-p-reading-pathways/images/chapter-opener.png` - prompt: robot hiker at a forest trailhead with 8 wooden signposts pointing different directions; trails branch across a colorful hillside.
- Appendix Q: `appendices/appendix-q-intermediate-projects/images/chapter-opener.png` - prompt: three robot apprentices on graduated step-stools at a workshop bench between a small lab and a tall capstone tower.
- Appendix R: `appendices/appendix-r-capstone-project/images/chapter-opener.png` - prompt: three robot students on differently-shaped podiums (full-stack, API-only, research replication), each holding a differently-shaped trophy.
- Appendix S: `appendices/appendix-s-war-stories/images/chapter-opener.png` - prompt: robot detective at a corkboard pinned with five newspaper clippings, red string connecting them to chapter-number tags.

## Coordination notes

- Ch 32 / 16.1 / 64.5 hero illustrations: deliberately skipped for this sweep. Section
  authoring agent (a9b53b0692771f5fa) is mid-flight on those sections; a later sweep
  should add hero illustrations once authoring completes.
- For-Instructors index pages were edited only with a hero `<figure>` insertion at the
  top of `<main>`; no other edits to the existing content. No conflict observed with
  the index staleness fix agent (a2251a4de72513129) at the time of writing.

## Cost summary

- gemini-imagegen invocations: 25 (one batch run via `gemini-3.1-flash-image-preview`)
- Total images generated: 25 (20 broken-queue regenerates + 5 appendix hero gaps)
- Total `<figure>` / `<div class="diagram-container">` blocks removed: 11
- Generation script: `scripts/_visual_assets_sweep.py`
