# Wave 1: RWS Titles, Lab Coverage, Duplicate Prose Cleanup

Generated: 2026-05-20 (branch v2.0)

Three content-quality cleanup tasks executed autonomously. Final audit status:
**0 P0/P1 issues, 0 P2 issues** (1 pre-existing P3 IMAGE_OPPORTUNITY in
`part-1.../section-3.4.html`, unrelated to this wave).

---

## Task A: Real-World Scenario callout title prefix

Normalized every `practical-example` callout title to the canonical
`Real-World Scenario: <Specific Title>` form.

- **44 titles fixed total** (the brief estimated ~52; the true count of
  non-compliant `practical-example` titles was 44).
  - **30 prefix rewrites** (automated, deterministic): titles that began with
    `Practical example:`, `Practical Example:`, or `Case study:` had the prefix
    replaced with `Real-World Scenario:`, preserving the specific title text and
    any trailing `exercise-type` span. First letter of the kept text was
    capitalized where it had been lowercase.
  - **14 bare-title rewrites** (manual, context-derived): callouts whose title
    was just `Practical Example` or `Real-World Scenario` (no specific title).
    Each was given a concrete title read from the callout's own content:

    | File | New title |
    |------|-----------|
    | module-65 section-65.1 | Sharing the Hugging Face Cache Across Containers |
    | module-65 section-65.2 | Keeping API Keys Out of Docker Images |
    | module-65 section-65.3 | Separate Env Files for Dev, Staging, and Prod |
    | module-65 section-65.4 | Fitting a 70B Model on One GPU with Quantization |
    | module-06 section-6.8 (x3) | Llama-3.1 405B Training Configuration / FP8 Training Throughput Gains / Checkpoint Strategy for a 70B Pretraining Run |
    | module-09 section-9.7 | Pruning Plus Quantization for 7B Customer Support |
    | module-10 section-10.10 | Maintaining AWQ and GGUF Copies of One Model |
    | module-10 section-10.8 (x2) | Streaming Tokens from a Local vLLM Server / RadixAttention Shares a System Prompt Across Users |
    | module-19 section-19.5 | Auto-Syncing a Product-Docs Vector Index |
    | module-45 section-45.1 | Mixing On-Demand and Spot Replicas to Cut Cost |
    | module-16 section-16.5 | When Generic Embeddings Failed a Legal Search Engine (folded a redundant `<h4>` into the title) |

- Only `practical-example` callouts were touched; `exercise-type` spans were
  preserved; no other callout types modified.
- Verified: a re-scan finds **0** non-compliant `practical-example` titles, and
  the `CALLOUT_TITLE_PREFIX` audit check passes with 0 issues.

---

## Task B: Lab coverage

`LAB_COVERAGE` flagged exactly one module without a hands-on lab:
`part-3-working-with-llms/module-12-prompt-engineering` (FM.4 promises >= 1 lab
per chapter).

- Added one hands-on lab to **section-12.5** (Automatic Prompt & Context
  Engineering), the last content section before the exercises/bibliography:
  **"Hands-On Lab: Beat Your Hand-Written Prompt with DSPy."** The reader builds
  a small text classifier by hand and again with DSPy `BootstrapFewShot`, then
  compares accuracy on a fixed held-out test set; deliverable is a
  hand-vs-optimized accuracy table plus the auto-selected few-shot exemplars.
- Structured to the canonical lab pattern (`<div class="callout lab">` with
  Objective / Setup / Steps / Expected Output `<h3>` sub-headings and a
  `Solution Walkthrough` `<details>`), placed BEFORE the key-takeaway callout to
  satisfy `CALLOUT_ORDER`, with a `12.5.9 Lab:` heading.
- Verified: `LAB_COVERAGE`, `NON_CALLOUT_LAB`, `CALLOUT_ORDER`, and
  `CALLOUT_INTERNAL` all pass with 0 issues.

---

## Task C: Duplicate prose / code-caption clusters

Methodology note: the audit's `_content_pairs.jsonl` stores section names in the
pre-renumber `section-N.Ma`/`section-N.Mb` form. After stripping the `a`/`b`
suffix, **16 of the 30 flagged pairs are split-siblings** (consecutive sections
that intentionally share a Big-Picture/recap paragraph from the v2.0 length
split) and were skipped per the brief. The remaining **14 pairs are genuine
(non-sibling)**; of those, 7 had actual verbatim/near-verbatim shared prose and
7 are pure-thematic (cosine-only, `KEEP-BOTH`, different subtopics in the same
chapter). A whole-book verbatim-paragraph scan confirmed that after these fixes
there are **0** remaining non-adjacent verbatim prose duplications.

### Prose / callout clusters differentiated (7 clusters, 11 edits)

1. **Deep-dive "Optional - for depth" boilerplate** (`module-03` sections 3.5,
   3.6, 3.7, 3.8): the identical "This section dives deeper..." note appeared in
   four non-adjacent sections. Rewrote each to describe what that specific
   optional section covers (variants & efficiency / GPU systems / expressiveness
   theory / beyond-attention architectures) and why it is skippable.
2. **Workflow-orchestration "where the state lives" Key Insight** (`module-64`
   64.2 vs 64.4): kept the full five-framework comparison in 64.4 (the
   choose-a-framework section); rewrote 64.2's Key Insight around the
   workflow-engine-vs-task-queue axis it actually introduces, pointing to 64.4.
3. **"Your eval set has a half-life" Key Insight** (`module-44` 44.4 vs 44.5):
   kept 44.4 (Post-Launch Monitoring) as canonical; reframed 44.5's version
   through the drift-detection lens that is 44.5's actual topic.
4. **Triton intro** (cross-part: `module-03` 3.6 vs `module-09` 9.9): 3.6 keeps
   the foundational Triton teaching; rewrote 9.9's intro to cross-reference 3.6
   and frame Triton specifically for the inference/decode hot path (vLLM/SGLang).
5. **Suno/Udio music-gen paragraph** (`module-73` 73.6 vs 73.7): 73.6 keeps the
   capability survey; rewrote 73.7's opener to assume the reader knows Suno and
   lead with the rights/litigation angle (73.7's topic).
6. **Siemens Industrial Copilot paragraph** (`module-73` 73.1 vs 73.5): 73.5
   (Named-Vendor Cases) keeps the detailed OEM-pattern write-up; rewrote 73.1's
   overview mention into a concise OEM-vs-internal framing that forward-refs 73.5.
7. **Multi-query expansion Tip + library-shortcut pointer**
   (`module-35` 35.1 vs 35.2; and `module-31` 31.6 vs `module-32` 32.1): 35.2
   owns query transformation, so 35.1's duplicated Tip was reframed for hybrid
   retrieval with a pointer to 35.2; the verbatim "production library shortcut"
   See-Also pointer in 31.6 and 32.1 was rewritten to describe each section's own
   chunking snippet.

### Code-caption boilerplate differentiated ("Minimal working example using X", 9 edits)

The templated caption `Minimal working example using <library>` recurs ~29 times
book-wide. Rewrote the verbatim same-library duplicate pairs to describe what
each specific snippet does:

- **FAISS** (35.2.2 reusable `search()` helper returning triples; 37.6.8 swaps a
  memory store's NumPy scan for `IndexFlatIP`).
- **sklearn cosine_similarity** (31.2.10 ranks a precomputed matrix; 31.7.4
  re-encodes chunks on the fly for index-free retrieval).
- **sentence-transformers** (1.3.8 scores paraphrase pairs via `util.cos_sim`;
  1.4.8 shows the "bank" polysemy across three 384-dim embeddings).
- **PydanticAI** (26.2.3 multi-step research agent; 27.1.3 tool schema inferred
  from type hints with the tool-call output; 27.1.4 same tool, provider-agnostic
  model swap to Claude).

No code-caption is duplicated across 3+ files; no `<pre><code>` contents, URLs,
or normalized terminology forms were modified.

---

## Verification

- `python -m agents.book-skills.scripts.audit.run --priority P0+P1 --root .`
  -> **0 issues**.
- Full audit (all priorities) -> only 1 pre-existing P3 (`IMAGE_OPPORTUNITY`,
  section-3.4, not touched by this wave).
- Structural sanity check on all 32 edited files: balanced `<div>`/`</div>` and
  `<details>`/`</details>`, no empty callout titles.
- No em dashes introduced; commas/colons/semicolons used throughout.
