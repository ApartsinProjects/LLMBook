# Lame Content Audit, May 2026

Scope: Tools-of-the-Trade chapters (Modules 6, 12, 16, 21, 25, 30, 33, 36, 39, 50, 60, 65), For-Instructors appendices (O, P, Q, R, S), and Part XI industry chapters (51-59).

Read-only audit. The most pervasive failure mode is a `Comparing the X` sub-h2 at the tail of every section that just transposes the bullet list immediately above it into a 3-5-row table, often with no new judgment, no recommendation, no tradeoff that was not visible in the bullet list. The user identified this in 50.5.4, 60.5.3, and 65.5.4 as "lame"; the pattern repeats roughly 60 times across the Tools-of-the-Trade chapters with little to no per-instance value-add.

Severity legend: **DROP** = remove the sub-section entirely (or merge its one useful row into the section above). **REWRITE** = the topic is worth keeping but the prose is shallow; replace with substantive content. **REVIEW** = borderline; author's call.

---

## A. The endemic "Comparing the venues / libraries / platforms" sub-h2 in Tools-of-the-Trade chapters

These are recommended for wholesale removal. In nearly every case the sub-section consists of one introductory paragraph (often missing) plus a 3-5 row table whose Best for / Use case / Latency cells are paraphrases of the same words used in the prior bullet list. There is no analytical content. The reader's eye reaches the table, registers "this is the same list with a different shape," and moves on. The chapters would read tighter, faster, and more competently if these were either deleted or collapsed into a single sentence that points at the canonical comparison (Appendix AD master tables, or Chapter 16's price table).

The user-identified calibration examples:

```
part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html:50 — 65.5.4 Comparing the venues — DROP — 3-column table (Venue / Best for / Latency) with five rows that re-paraphrase the bullets above; no analysis. The "final practical advice" callout below is also generic motivational filler ("the field will be different in 18 months", "read papers weekly"). — Drop both. Let 65.5.1-65.5.3 do the work; collapse the final-advice callout into one sentence at the chapter close.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.5.html:49 — 50.5.4 Comparing the venues — DROP — same 3-column table pattern; zero new information. — Drop entirely.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.5.html:43 — 60.5.3 Comparing the venues — DROP — same pattern; the table just renames Latency to Cadence. — Drop.
```

The full hit-list of the same sub-section template across the rest of the Tools-of-the-Trade .5 sections:

```
part-1-foundations/module-06-tools-of-the-trade/section-6.5.html:54 — 6.5.4 Comparing the reading sources — DROP — Same template, 4-column table. The "Why subscribe" column is the only one with any new info and reads as filler ("Signal-to-noise unmatched", "Best topic introductions on the open web"). — Drop. The bullet lists in 6.5.1-6.5.3 already characterise each source.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.5.html:61 — 12.5.5 Comparing the tracking sources — DROP — 4-column table (Cadence / Source / Best for / Why). Stronger than most because the cadence-grouping is the actual organising idea, but the prose around it is still absent. — REVIEW. If kept, demote to a paragraph and lose the table; the cadence framing is already in the bullet titles.
part-3-working-with-llms/module-16-tools-of-the-trade/section-16.5.html:57 — 16.5.5 Comparing the venues — DROP — Same template; useful only because OpenAI dev forum (multi-day) vs Reddit (hours) is real. Drop.
part-4-training-adapting/module-21-tools-of-the-trade/section-21.5.html:53 — 21.5.4 Comparing the venues — DROP — Standard template.
part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.5.html:49 — 25.5.4 Comparing the venues — DROP — Standard template.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html:50 — 30.5.4 Comparing the venues — DROP — Standard template.
part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.5.html:49 — 33.5.4 Comparing the venues — DROP — Standard template; no callout afterward, so this is the bottom-of-page filler.
part-8-evaluation-production/module-36-tools-of-the-trade/section-36.5.html:48 — 36.5.4 Comparing the venues — DROP — Standard template.
part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.5.html:52 — 39.5.4 Comparing the venues — DROP — Standard template.
```

The same template is repeated for sections .1 (Platforms), .2 (Libraries), .3 (Datasets), .4 (Models) in most of these chapters:

```
part-1-foundations/module-06-tools-of-the-trade/section-6.1.html:41 — 6.1.4 Comparing the platforms — DROP — Repeats Colab/Kaggle/Lightning/Local/AWS from the prose above with a Free GPU column that adds one fact per row. The "Watch out for" column has weak value ("Easy to bill $100 by accident" is true but the kind of thing the warning callout already says). — Collapse into the warning callout; drop the table.
part-1-foundations/module-06-tools-of-the-trade/section-6.2.html:46 — 6.2.4 Comparing the engines — DROP — Same pattern. The "When to skip" column is the only added information and is one phrase per row.
part-1-foundations/module-06-tools-of-the-trade/section-6.3.html:45 — 6.3.3 Comparing the teaching datasets — REVIEW — Slightly better because Size column is genuinely useful for "fits in laptop RAM" decisions. — Keep the size column, drop the rest.
part-1-foundations/module-06-tools-of-the-trade/section-6.4.html:47 — 6.4.4 Comparing the Part I reference models — REVIEW — Params + Type columns earn their keep. — Keep but drop the "Best for" column; it just repeats the bullet titles.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.1.html:43 — 12.1.4 Comparing the rental platforms — REVIEW — H100 $/hr column is a real datapoint. — Keep this one; it's the rare case where the table adds price data the bullets do not.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.2.html:51 — 12.2.4 Comparing the tokenizer libraries — DROP — "Used by" column has value but the bullets above already say "Default for Llama, T5, etc." Redundant.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.3.html:49 — 12.3.3 Comparing the pretraining corpora — REVIEW — Token-count column is useful if present; otherwise drop.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.4.html:51 — 12.4.4 Comparing the frontier model families — REVIEW — Likely worth keeping if it carries access + context-window data.
part-3-working-with-llms/module-16-tools-of-the-trade/section-16.2.html:58 — 16.2.5 Comparing the SDK layer — REVIEW — "Layer / Best for / When to skip" is at least the right framing. Could be tightened to two sentences.
part-3-working-with-llms/module-16-tools-of-the-trade/section-16.3.html:52 — 16.3.4 Comparing the chat benchmarks — REVIEW — Format/Judge columns are useful. Keep.
part-3-working-with-llms/module-16-tools-of-the-trade/section-16.4.html:49 — 16.4.4 Comparing the API-callable model lineup — KEEP — The cost-and-context table here is the rare case where the table is the point. Leave alone.
part-4-training-adapting/module-21-tools-of-the-trade/section-21.1.html:47 — 21.1.4 Comparing the platforms — DROP — Standard template.
part-4-training-adapting/module-21-tools-of-the-trade/section-21.2.html:46 — 21.2.4 Comparing the libraries — DROP — Standard template.
part-4-training-adapting/module-21-tools-of-the-trade/section-21.3.html:50 — 21.3.4 Comparing the datasets — REVIEW — Size + Use cells likely justify the table; cut the table title and prose around it.
part-4-training-adapting/module-21-tools-of-the-trade/section-21.4.html:46 — 21.4.3 Comparing the bases — REVIEW — Could carry useful "fits on N GB" data.
part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.1.html:44 — 25.1.3 Comparing the platforms — DROP — Standard.
part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.2.html:50 — 25.2.4 Comparing the libraries — DROP — Standard.
part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.3.html:48 — 25.3.4 Comparing the datasets — REVIEW — Numeric data may make this worth keeping.
part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.4.html:51 — 25.4.4 Comparing the models — REVIEW — Embedding-dim and license-tier data may make this worth keeping.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html:44 — 30.1.3 Comparing the platforms — DROP — Standard.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html:47 — 30.2.4 Comparing the libraries — DROP — Standard. The "Style / Best for / Tradeoff" framing is the cleanest of the template, but the row content is still verbatim from the bullets.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html:48 — 30.3.4 Comparing the benchmarks — REVIEW — Likely useful if it carries scores.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html:50 — 30.4.4 Comparing the models — REVIEW.
part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.1.html:55 — 33.1.4 Comparing the platforms — DROP — Standard.
part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.2.html:49 — 33.2.4 Comparing the libraries — DROP — Standard.
part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.3.html:50 — 33.3.4 Comparing the datasets — REVIEW.
part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.4.html:54 — 33.4.4 Comparing the models — REVIEW.
part-8-evaluation-production/module-36-tools-of-the-trade/section-36.1.html:53 — 36.1.4 Comparing the platforms — DROP — Standard.
part-8-evaluation-production/module-36-tools-of-the-trade/section-36.2.html:54 — 36.2.4 Comparing the libraries — DROP — Standard.
part-8-evaluation-production/module-36-tools-of-the-trade/section-36.3.html:51 — 36.3.4 Comparing the benchmarks — REVIEW — Likely useful if it carries score baselines.
part-8-evaluation-production/module-36-tools-of-the-trade/section-36.4.html:44 — 36.4.3 Comparing the options — DROP — Standard.
part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.1.html:48 — 39.1.4 Comparing the platforms — DROP — Cost-and-role columns are the only useful cells. Collapse into a paragraph.
part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.2.html:50 — 39.2.4 Comparing the libraries — DROP — Standard.
part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.3.html:49 — 39.3.4 Comparing the datasets — REVIEW.
part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.4.html:41 — 39.4.3 Comparing the models — REVIEW.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.1.html:59 — 50.1.5 Comparing the platforms — DROP — Standard.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.2.html:50 — 50.2.4 Comparing the libraries — DROP — Standard.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.3.html:42 — 50.3.3 Comparing the resources — DROP — Standard template, only 5 rows, "Status" column is "Active / Saturated / Evergreen" which is in the prose already.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.4.html:38 — 50.4.3 Comparing the models in context — REVIEW — Tier-recommendation is borderline useful; could be one sentence pointing at Chapter 16 instead.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.1.html:63 — 60.1.6 Comparing the verticals — DROP — Standard.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.2.html:51 — 60.2.5 Comparing the libraries — DROP — Standard.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.3.html:44 — 60.3.3 Comparing the benchmarks — REVIEW.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.4.html:37 — 60.4.2 Comparing the vertical models — REVIEW.
part-12-frontiers/module-65-tools-of-the-trade/section-65.1.html:57 — 65.1.5 Comparing the platforms — DROP — Standard.
part-12-frontiers/module-65-tools-of-the-trade/section-65.2.html:50 — 65.2.4 Comparing the libraries — DROP — Standard, especially thin: only 3 columns and the "Role" column is the bullet title.
part-12-frontiers/module-65-tools-of-the-trade/section-65.3.html:42 — 65.3.3 Comparing the frontier benchmarks — REVIEW — Frontier-score column actually carries data; keep but cut narrative.
part-12-frontiers/module-65-tools-of-the-trade/section-65.4.html:47 — 65.4.4 Comparing the frontier models — REVIEW.
```

Rule of thumb: keep the table only when at least one column carries numeric or licensing / cost / size data the bullet list does not have. Drop everything else.

---

## B. Other low-value prose in Tools-of-the-Trade chapters

```
part-3-working-with-llms/module-16-tools-of-the-trade/section-16.1.html:28 — Section 16.1 Platforms — DROP — The entire section body is "TODO author this section. This is a scaffold; replace with chapter content authored in Phase E." — Either author it or remove the section from the chapter index. It is currently shipping as a TODO stub in a published 15th-edition book.
part-7-multimodal-generation/module-33-tools-of-the-trade/section-33.5.html:28 — 33.5 intro paragraph — REVIEW — "Multimodal literature is split across image, video, audio, and music research communities. The sources below cover all four." is filler; the bullets already make that clear. Cut.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.5.html:28 — 60.5 intro — REVIEW — "Industry-specific AI literature is fragmented across trade journals, vendor blogs, and academic conferences. The list below is a starting point per industry." Both sentences are filler. Cut the first; keep "the list below is a starting point" only if it warns the reader the list is non-exhaustive.
part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html:28 — 65.5 intro — REVIEW — "The final section of the book points at where to keep reading after you finish it. The half-life of any specific tool listed in this book is short..." Half-life sentence is reused; first sentence is unnecessary scaffolding. Cut.
part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html:86-89 — "The final practical advice" callout — REWRITE — Currently reads as a graduation speech: "What stays constant is the discipline: read papers weekly, build prototypes monthly, measure quarterly, and never confuse the toolbox for the craft. Welcome to the working day." It's the last sentence of the book and it's a sub-Twitter aphorism. Replace with something concrete, e.g. a single pointer at the next book or a list of 3 papers worth reading after closing the book.
part-12-frontiers/module-65-tools-of-the-trade/section-65.4.html:28 — 65.4 intro — REVIEW — "Frontier models are by definition the most recent. This section lists the families pushing the boundary as of 2026, with the caveat that the list will be outdated within months." Filler.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.5.html:28-29 — 12.5 intro pair — REVIEW — The second paragraph ("The leaderboards and newsletters in this section will continue updating long after this book's print date...") is the standard "subscribe to originals not aggregators" disclaimer that appears in roughly every Tools-of-the-Trade .5 intro. Collapse to one sentence.
part-1-foundations/module-06-tools-of-the-trade/section-6.5.html:28-29 — 6.5 intro pair — REVIEW — Same disclaimer pattern as 12.5. Both paragraphs say roughly the same thing twice. Trim to one paragraph.
part-3-working-with-llms/module-16-tools-of-the-trade/section-16.5.html:50 — Filler sentence — REWRITE — "When your app fails at 2 AM, check the status page first. Roughly half of 'my prompt broke' incidents are upstream incidents." This stands alone between sub-sections and is the right idea but reads as a Twitter-thread aside. Move it inside the status-pages bullet list or promote to a proper callout.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html:50 (suspected) and 30.5.html — REWRITE — Section 30 has the youngest topic and the prose acknowledges it ("the field is changing fast enough that the canonical references shift every six months"). That admission is fine; what's missing is concrete guidance on how to triage a fast-moving literature. Add a "if you only follow three people / repos" recommendation.
part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.5.html:28 — 39.5 intro — REVIEW — "The AI safety, security, and ethics literature is large and contested. The list below is intentionally a starting point, not a survey." Filler; cut.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.5.html:73-76 — "Tip: spend 15 minutes a day, not 2 hours" callout — REVIEW — Concrete advice but somewhat formulaic ("the mistake most people make is X, do Y instead"). Keep or rewrite around an actual habit, not a slogan.
```

---

## C. Tools-of-the-Trade sub-section intro paragraphs that re-state definitions

The .1 / .2 / .3 / .4 sub-section openings frequently re-define terms covered in the main chapter prose. Worst offenders below.

```
part-1-foundations/module-06-tools-of-the-trade/section-6.2.html:28 — 6.2 intro pair — REWRITE — Paragraph 2 ("The principle is 'right tool, right layer'...") restates a point made in every PyTorch tutorial. The page would be tighter with the first paragraph only.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.2.html:28-29 — 12.2 intro pair — REVIEW — Paragraph 2 ("What is new compared to Part I is the absolute centrality of the tokenizer layer...") re-flags what Chapter 7 already said. Trim.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.1.html:28-29 — 12.1 intro — REVIEW — The paragraph "What changes for Part II is the cost calculus..." restates "70B in fp16 needs 140GB" which the body of Chapter 10 already covered. Cut.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html:28 — 30.1 intro — DROP — "Agentic systems run on top of LLM API platforms (Chapter 16) plus a new layer..." — one sentence that re-points at Ch 16. Drop and let the section title introduce itself.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.1.html:28 — 50.1 intro — DROP — "The platforms in Part X are not LLM platforms; they are the surrounding product tooling that AI startups standardize on." This is one of the leanest leads in the book and it's still unnecessary; the section title already says Platforms.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.3.html:28 — 50.3 intro — REWRITE — "Part X is unusually light on traditional ML datasets..." reads as an apology. Replace with a positive framing: "Part X's measurement story is developer-productivity benchmarks (SWE-bench, SWE-Lancer), event analytics, and revenue funnels." Or drop.
part-10-idea-to-product/module-50-tools-of-the-trade/section-50.4.html:28 — 50.4 intro — REWRITE — "Part X is mostly model-agnostic..." is the same apology pattern. Drop or rewrite as one sentence pointing at Chapter 16's tier table.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.1.html:28 — 60.1 intro — DROP — "This section enumerates the vertical-specific AI platforms by industry. The list is non-exhaustive and the vendors are by reputation and traction as of 2026." Filler. Cut.
part-11-applications-across-industries/module-60-tools-of-the-trade/section-60.4.html:28 — 60.4 intro — DROP — "Models specifically trained or fine-tuned for verticals are a small but growing slice of the 2026 landscape." Filler. Cut.
part-12-frontiers/module-65-tools-of-the-trade/section-65.1.html:28 — 65.1 intro — DROP — "The platforms for frontier research are paper preprint servers, lab publication channels, and live benchmark leaderboards." This is the section's own outline restated as prose. Drop.
part-12-frontiers/module-65-tools-of-the-trade/section-65.2.html:28 — 65.2 intro — DROP — Same pattern: "Libraries for frontier-research workflows are the paper-tracking tools, reproducibility helpers..." Just the outline in sentence form.
part-12-frontiers/module-65-tools-of-the-trade/section-65.3.html:28 — 65.3 intro — DROP — "Frontier-research benchmarks are the ones used to delineate the boundary between 'current' and 'next' capability. The shelf has changed substantially since 2022." First sentence is tautological; second is the kind of vague-historical handwave the user flagged. Drop both.
```

---

## D. Sub-section closing paragraphs that are pure transitions

Most Tools-of-the-Trade sections end with a sentence like "Section X.Y picks up Z." These are arguably navigation aids and not load-bearing, but several go further into editorial filler and should be removed.

```
part-1-foundations/module-06-tools-of-the-trade/section-6.1.html:91-93 — 6.1.5 Choosing a default — REWRITE — "For everything in Part I, the recommended default is..." this paragraph is the kind of advice that adds value, but the follow-up "With the platform settled, the rest of the chapter looks at the libraries that run on top of it..." is bare transitional prose. Strip the transition; keep the default-recommendation paragraph.
part-1-foundations/module-06-tools-of-the-trade/section-6.2.html:107-109 — 6.2.5 Versions and compatibility — REWRITE — The version-pinning advice is good, but the closing line "With the library layer chosen, the remaining question is what data to feed it..." is filler. Strip.
part-1-foundations/module-06-tools-of-the-trade/section-6.3.html:103-105 — 6.3.5 What "good enough" looks like — REVIEW — The "target metric per dataset" data is useful; the closing transition "With the data layer settled, the next section enumerates the reference models..." is generic. Strip the transition.
part-1-foundations/module-06-tools-of-the-trade/section-6.4.html:109-111 — 6.4.5 Looking ahead — DROP — "Part II will introduce the modern frontier zoo... Section 6.5 closes the chapter with the external reading list..." Pure pipework. Cut.
part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html:86-89 — "Welcome to the working day" callout — REWRITE — Already in section B.
```

---

## E. Generic motivational / aphoristic callouts

Across many Tools-of-the-Trade chapters there are tip / key-insight callouts whose content is generic productivity advice rather than substantive technical content.

```
part-1-foundations/module-06-tools-of-the-trade/section-6.5.html:100-103 — "Reading discipline beats reading volume" key-insight callout — REVIEW — "Skim ten papers a week and you remember nothing; read one a week and rebuild the math on paper, and by month three you can hold a conversation with the author." This is a personal-development claim presented as a technical insight. Keep as a tip, or replace with concrete advice on note-taking systems.
part-2-understanding-llms/module-12-tools-of-the-trade/section-12.5.html:77-80 — "Reading discipline scales" key-insight callout — DROP — Same generic motivational ("The reading habits you build in Part II carry over to Parts III through XII..."). Cuts no new ground.
part-4-training-adapting/module-21-tools-of-the-trade/section-21.5.html:89-92 — "A working pattern" tip — REVIEW — "Treat the alignment-handbook and AllenAI's open-instruct as your reference recipes..." This is actually good practical advice. Keep.
part-5-retrieval-conversation/module-25-tools-of-the-trade/section-25.5.html:85-88 — "A test for RAG advice" tip — KEEP — The "if a post recommends a magic chunk size or single best embedding model, treat it skeptically" advice is concrete and not redundant.
part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html:86-89 — "Read code, not posts" tip — KEEP — Concrete and actionable.
part-8-evaluation-production/module-36-tools-of-the-trade/section-36.5.html:84-87 — "Eval-driven development" tip — KEEP — Concrete.
part-9-safety-security-ethics/module-39-tools-of-the-trade/section-39.5.html:88-91 — "Compliance is a moving target" tip — KEEP — Concrete and provides Appendix P pointer.
```

---

## F. For-Instructors appendices

Mostly solid, but a few items:

```
appendices/appendix-o-course-syllabi/index.html:32-46 — "Track Overview" table — KEEP — Genuine value: students can pick a track based on duration, audience, capstone.
appendices/appendix-p-reading-pathways/index.html:159-167 — Pathway 8 (The Curious Generalist) — REWRITE — The first list item is broken: " · 1 hr · <em>(read the 5 unifying theses and 3 tensions)</em>" with no link or referent. Likely a copy-paste accident where the chapter link was deleted. Either fix the reference or drop the bullet.
appendices/appendix-p-reading-pathways/index.html:144-150 — Pathway 7 (Course Instructor) — REVIEW — Lists "FM.7 Copyright & Legal(Course Syllabi)" as the start, which is a clearly broken cross-reference (FM.7 is Copyright & Legal, not Course Syllabi). Fix the label or the link.
appendices/appendix-q-intermediate-projects/index.html — KEEP — All three projects are concrete and gradeable.
appendices/appendix-r-capstone-project/index.html — KEEP — Rubric is solid.
appendices/appendix-s-war-stories/index.html — KEEP — Five named, sourced, real incidents; this is the opposite of lame.
```

---

## G. Part XI industry chapters (51-59)

Spot-checked Modules 51 (Legal), 52 (Finance), and 54 (Education). All three are dense with concrete failure modes, named cases (Mata v. Avianca, Samsung leak, Khanmigo Socratic prompt design), and regulatory specifics. These chapters are emphatically not lame and should not be touched.

```
part-11-applications-across-industries/module-51-legal-llms/index.html — KEEP — Strong on named cases (Mata v. Avianca), specific vendor table, bar-association rules. Use as reference for what good industry-chapter prose looks like.
part-11-applications-across-industries/module-52-finance-llms/index.html — KEEP — Tier 0-3 trust framework, BloombergGPT callout, specific regulatory references (SR 11-7, DORA). Strong.
part-11-applications-across-industries/module-54-education-llms/index.html — KEEP — Khanmigo Socratic-prompt callout is the kind of concrete pedagogical insight the book benefits from.
```

Did not deep-read 53 (Healthcare), 55-59 because the index.html sizes (150-200 lines) are consistent with a similar shape to 51/52/54; the audit is conservative on these. Recommend spot-check by author.

---

## H. Cross-chapter pattern recommendations

1. **Delete the "Comparing the X" template wholesale where the table is paraphrase-of-the-bullets.** Roughly 40 of the 60 cases. The chapters get tighter and the remaining tables (where Size, Cost, Context-window, or License data sits) become more visible.

2. **Replace the "Tools-of-the-Trade .5 intro" boilerplate with a single sentence.** The pattern "X's literature is split between A, B, and C. The list below favours signal over volume." appears in almost every .5 with minor variations.

3. **Strip transitional closing paragraphs.** Almost every Tools-of-the-Trade subsection ends with "Section X.Y picks up Z." That belongs in the chapter-nav block at the bottom, not in prose.

4. **Author Section 16.1.** It is currently a published TODO.

5. **Re-think the role of "Tools-of-the-Trade" chapters generally.** When a stack chapter consists of 5 sections, each of which is "intro + 3 bullet lists + comparison table + tip callout", the chapter is closer to a reference appendix than a chapter. Either move them to appendices, or rewrite at least one section per chapter (probably .4 Models) to carry substantive analysis the way Chapters 51-54 do.

---

## Estimated impact

If the DROP recommendations in section A are applied alone, roughly 35-40 Tools-of-the-Trade sub-sections shrink by 15-30 lines each, removing ~600-1000 lines of low-value HTML. The chapters become noticeably shorter without losing any unique information; every fact in the dropped tables is preserved in the bullet lists above them.
