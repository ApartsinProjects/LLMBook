# Publishing Package Review + Size Reduction Opportunities

**Analysis only — no changes applied.** Recommendations are sequenced by impact-to-effort ratio so you can pick which to act on.

Current state of the package (as of last build):
- **EPUB**: 45.73 MB optimized (raw 72 MB), 0 epubcheck errors
- **Cover**: native Gemini i2i variant available; placeholder JPEG currently active
- **Description**: 3,359 chars (under 4,000 limit), HTML-formatted
- **Keywords**: 7 of 7 used
- **Categories**: AI/Semantics + Neural Networks + Programming/General
- **Distribution**: KDP only, no Author Central setup, no companion repo

---

## Part A — Adoption & review levers

Ranked by **expected impact** × **effort**.

### A1. Set up Amazon Author Central [HIGH impact, ~1 hour, FREE]

Currently both authors have **no Author Central profile**. This is the single biggest adoption blocker — without it the book page on Amazon shows "by Alexander Apartsin" as plain text with no clickthrough.

What Author Central adds:
- Author photo on the book page (massive trust signal)
- Author bio with links to other works
- "Follow this author" button (notifies readers of future books)
- Editorial reviews section
- Cross-linking to other Amazon-published works

Sign up at https://authorcentral.amazon.com (separate accounts per author). Both authors should claim the book.

### A2. Optimize "Look Inside" preview [HIGH impact, ~1 hour]

KDP shows the first ~10% of the book as a free preview ("Look Inside the Book"). Right now your preview opens with: cover → about-authors → about-book → fm-1 sections. By the time a browsing reader hits the actual content, they've already bounced.

**Recommendation**: Move a "compelling sample" early in the spine. Best candidates:
- A short, punchy excerpt from a popular chapter (Ch 11 Prompt Engineering with code highlighting, or Ch 22 AI Agents) **before** the about pages
- Or a "Why this book?" section that previews 2-3 lab examples upfront

Mechanically: edit `KDP/build/generate_spine.py` to inject the chosen chapter early. Doesn't change source HTML.

### A3. Companion GitHub repository [HIGH impact, ~4 hours, FREE]

Most modern technical books have a companion repo (Sebastian Raschka, Chip Huyen, all do). Readers expect:
- Runnable code for every chapter
- Errata
- Issue tracker for questions
- Stargazers act as social proof

Suggested repo structure:
```
LLMBook-companion/
├── README.md            ← Book description, errata, install
├── chapter-04/          ← Code for transformer chapter
├── chapter-11/          ← Prompt engineering examples
├── chapter-20/          ← RAG pipeline
├── ... (one folder per chapter)
├── requirements.txt
└── colab/               ← .ipynb for each lab
```

Once live, add `<repository>` reference to OPF metadata and mention in description.

### A4. Description optimization [HIGH impact, ~30 min]

Current description starts with the title and subtitle. The first 2-3 lines are what shows in search results — make them count.

**Current opener**:
> "Building Conversational AI with LLMs and Agents... From the mathematics of attention to production agent systems..."

**Better opener** (lead with reader benefit):
> "Build production AI agents from first principles. This 39-chapter textbook takes engineers, researchers, and ML practitioners from PyTorch fundamentals to shipping LLM-powered systems — covering RAG, fine-tuning, tool use, multi-agent orchestration, and safety in 800+ pages..."

Then the bullet list. Move "Twenty tailored reading pathways" to the very end as a feature highlight.

Add at the bottom (KDP allows up to 4000 chars, you have ~640 free):
- "**Companion code**: github.com/[username]/llmbook-companion"
- "**Errata and updates**: [your-website]/errata"
- "**Course adoption**: [your-website]/instructors (free instructor copies)"

### A5. Keywords refresh [MEDIUM impact, ~30 min]

Your 7 keywords mostly restate the title. Amazon already indexes the title — keywords are valuable for **adjacent searches** the title misses.

**Current** (analysis):
| Keyword | Issue |
|---------|-------|
| large language models textbook | Restates title |
| build AI agents production | Restates subtitle |
| RAG retrieval augmented generation guide | OK — adds RAG searches |
| transformer architecture from scratch | OK — pulls "Karpathy from scratch" demographic |
| LLM fine tuning LoRA RLHF | OK — captures fine-tuning searchers |
| prompt engineering practitioners guide | Decent — competes with Patel/Wolfe |
| machine learning deep learning NLP | Too generic — won't rank |

**Suggested refresh** (focus on co-purchase signals):
1. `RAG vector database semantic search` (RAG buyers also search for these terms)
2. `LangChain LangGraph CrewAI tutorial` (framework keyword, captures intent)
3. `transformer architecture from scratch attention` (better than yours; "from scratch" is a high-intent term)
4. `prompt engineering ChatGPT Claude Gemini` (model-name keywords boost discoverability)
5. `LLM fine tuning LoRA QLoRA RLHF DPO` (modern PEFT terms)
6. `AI agent multi-agent system LLM` (current hot topic)
7. `MLOps LLM production engineering observability` (production angle)

### A6. Categories — pick narrower for ranking [MEDIUM impact, ~15 min]

"Computers > Artificial Intelligence" has thousands of titles. To rank in Top 100 you need a narrower primary category.

**Current**: AI/Semantics + Neural Networks + Programming/General

**Better mix** (one broad for visibility + two narrow for ranking):
1. Primary: **Computers > Artificial Intelligence** (visibility — high traffic)
2. Secondary: **Computers > Programming Languages > Python** (Python is your lab language — narrower, easier to crack Top 100)
3. Tertiary: **Computers > Computer Science > Information Theory** (or "Software Development > Tools" — narrow, less competition)

KDP allows up to 10 categories on request — email KDP after publishing to add more. List I'd request:
- Computers > Software Development & Engineering > Tools
- Education > Teaching Methods & Materials > Computers & Technology
- Computers > Data Science > Machine Learning
- Mathematics > Probability & Statistics

### A7. Cover legibility check [MEDIUM impact]

Your Gemini i2i cover (`cover_gemini_with_text_i2i_v20260510-072934.jpg`) looks great at 1600×2560, but Amazon shows it at **250 px wide thumbnail** in search results. At that size:
- "BUILDING CONVERSATIONAL AI" is legible ✓
- "WITH LLMS AND AGENTS" is borderline (squint test fails)
- Subtitle "A practitioner's guide..." is illegible ✗
- Author names illegible ✗

**Recommendation**: Make 2-3 thumbnail-test variants:
- Drop subtitle from cover (move to description)
- Make title 30% larger
- Use higher contrast color for title (currently warm gold on navy — works, but lower contrast than e.g. white on navy)

The artwork-only Gemini variant + manual text overlay (Photoshop/Affinity/Figma) gives the most control.

### A8. Pre-launch ARC (Advance Reader Copies) [HIGH impact, ~10 hours over 2 weeks]

KDP authors with no reviews on launch day struggle to convert browsing readers (no social proof). Pre-launch ARCs solve this.

**Process**:
1. Generate 20-50 free ARC copies (DRM-free EPUBs sent via email)
2. Ask recipients to leave honest reviews when book launches
3. Target ML newsletter writers, Twitter/X AI personalities, university faculty in NLP

**Where to find reviewers**:
- BookSirens (paid, ~USD 30)
- BookSprout (free for first 50 reviews)
- Direct outreach to: PyData/PyTorch newsletters, "AI Tidbits" / "The Batch" / "Import AI" / "TLDR AI" newsletters
- Reddit /r/MachineLearning, /r/LocalLLaMA, /r/learnmachinelearning (recruit reviewers via post)
- Twitter/X @karpathy followers, @huggingface mentions

**Realistic conversion**: send 50 ARCs → get 8-15 reviews → 5-8 of those go live in launch week → puts you above the "0 reviews" trust gap.

### A9. Foreword by industry expert [HIGH impact if achievable, ~1 week]

A foreword from a known AI/ML figure (Karpathy, Huyen, Raschka, Patel, Bengio's lab, Hugging Face folks, Anthropic/OpenAI engineers) provides:
- Massive trust signal
- Quote you can use in marketing
- Their audience may share

Your authors have academic credentials → this is realistic. Reach out via email, LinkedIn, Twitter DM. Even a 1-paragraph endorsement is gold.

### A10. Distribution beyond Amazon [MEDIUM impact, ~3 hours]

Currently KDP-only. Multi-distribution typically adds 15-30% revenue (Apple Books readers don't shop Amazon, vice versa).

**Easy paths**:
- **Draft2Digital** (free aggregator): single upload distributes to Apple Books, Kobo, Barnes & Noble, Google Play, libraries
- **Direct upload to each platform** (more royalty per platform, more upload work)
- **Leanpub** (technical-book audience; supports updates, gets you to ML newsletter readers)

Caveat: don't enroll in **KDP Select** (Kindle Unlimited) until you've decided — Select requires 90-day Amazon exclusivity.

### A11. Companion website / landing page [MEDIUM impact, ~6 hours]

Single-page site at e.g. `building-llm-book.com`:
- Hero: cover image + "Buy on Amazon" CTA
- Sample: download Chapter 1 PDF (lead magnet — captures email)
- About: authors + book pitch
- Code: link to GitHub repo
- Errata page
- Newsletter signup ("Get notified when next edition drops")
- Course adoption form (if targeting universities)

Free hosting on GitHub Pages, Cloudflare Pages, or Netlify.

### A12. Review-generation in-book [LOW effort, MEDIUM impact]

Add a "Help others discover this book" page near the back (after capstone, before appendices):
- One paragraph: "If this book helped you, please consider leaving an honest review on Amazon — even a few sentences makes a real difference for independent authors."
- QR code to the Amazon review page
- Thanks!

This converts ~2-5% of finishers into reviewers (vs 0.1% who do it unprompted). Mechanically: add `front-matter/please-review.html` to the spine before appendices.

### A13. Academic/institutional adoption [HIGH leverage for textbook genre]

Textbooks live or die by **course adoption** (one professor adopting → 30 students buy). Optimize for this:
- "Course adoption" page on companion site (instructor request form)
- Free instructor copies on request
- Sample syllabus drafts (you already have these in front-matter — promote them)
- Solutions manual (separate, instructor-only)
- Slides for each chapter (ASF: bonus material for instructors)

Reach out to: AI/ML/NLP professors at universities you have personal connection to (Israel: Technion/Hebrew U/Weizmann/Tel Aviv U/Afeka — direct via co-author Aperstein), then expand.

---

## Part B — Size reduction opportunities (analysis only)

### Where the bytes go (current 45.73 MB EPUB)

| Bucket | Files | Compressed | % of EPUB |
|--------|-------|-----------:|----------:|
| **Images (chapter illustrations)** | **499** | **40.49 MB** | **88.6%** |
| Chapters (XHTML) | 441 | 4.61 MB | 10.1% |
| Callout icons | 22 | 0.19 MB | 0.4% |
| Fonts (woff2) | 4 | 0.09 MB | 0.2% |
| Cover | 2 | 0.07 MB | 0.2% |
| EPUB metadata (OPF/nav/NCX) | 4 | 0.05 MB | 0.1% |
| Stylesheets | 3 | 0.02 MB | 0.0% |

**Conclusion: 88.6% of the EPUB is images**. Everything else is rounding error. Focus image strategy first.

### B1. Image strategy (biggest lever)

Current image profile:

| Bucket | Count | Total |
|--------|------:|------:|
| <50 KB | 192 | 4.95 MB |
| 50-100 KB | 112 | 8.38 MB |
| 100-200 KB | **186** | **25.10 MB** ← target |
| 200KB+ | 9 | 2.07 MB |

The 100-200 KB bucket holds **half the EPUB by size**. These are full-bleed chapter illustrations (Gemini-generated 1600×x scenes) that look great at desktop but are oversized for any Kindle screen.

#### Strategies (no source-HTML changes needed; all in build script)

| Action | Mechanism | Estimated savings | Visual cost |
|--------|-----------|------------------:|-------------|
| `--max-image-side 1200` (was 1600) | Already supported flag | **8-10 MB** | None — Paperwhite is 1072×1448, Scribe 1200×1920; 1600 was overkill |
| `--jpeg-quality 75` (was 82) | Already supported flag | **4-6 MB** | Imperceptible at reading sizes; visible only at 100% pixel-peep |
| Both combined | | **~12-16 MB → 30-33 MB total EPUB** | Minimal |
| `--max-image-side 1000 --jpeg-quality 70` (aggressive) | | **~18-22 MB → 24-28 MB** | Slight softness on best illustrations; OK trade |
| Convert top-200 illustrations to AVIF | New code path | 10-15 MB | Risk: older Kindle e-ink can't render AVIF; KDP uses Kindle Format X (KFX) which converts so probably OK on most devices, but unverified |
| Convert to WebP | New code path | 8-12 MB | Same risk as AVIF (lower) |

**Recommendation**: change two flag defaults to **`--max-image-side 1280 --jpeg-quality 78`**. Sweet spot: ~10 MB savings, near-zero visible quality loss, no risk.

### B2. Image deduplication
**0 duplicate images detected** (MD5 hash comparison). No savings here.

### B3. Chapter HTML compression (10.1% of EPUB = 4.6 MB)

Largest chapters compress to 25-40 KB. Each contains:
- Site nav chrome (`<nav class="header-nav">`, breadcrumbs) — already hidden via CSS but not stripped from HTML
- `<footer>` with site link — same
- Per-chapter inline `<script>` references (already removed)
- Class attributes for never-rendered states (`book-title-link`, `:hover` styles' triggers)

**Estimate**: build-script could strip an additional ~10-15% of HTML by removing:
- `<header>` chrome (already hidden in CSS)
- `<footer>` (replace with simpler EPUB-only footer)
- Class attributes that no CSS rule references
- Minified attribute order (already done by epub-optimizer)

**Estimated savings: 0.5-1 MB**. Modest. Skip unless going for aggressive shrink.

### B4. CSS reduction (0.04 MB = 40 KB)

Analysis of book.css (post-minify, 64 KB) vs chapter usage:
- 257 unique class selectors in book.css
- 172 referenced in 50-chapter sample
- **141 selectors potentially unused in EPUB** (e.g., `book-chapter`, `bib-collapse`, `agent-card-meta`, `algo-line-keyword`, `analysis`, `badge-group`)

These are website-only classes (nav, lab interactivity, collapsible sections). Could be stripped via PurgeCSS or similar.

**Estimated savings: ~10-20 KB** — negligible (<0.05% of EPUB).

### B5. Fonts (88 KB)
Already subsetted from 775 KB. No additional savings without dropping a face. Only realistic option:
- Drop italic face (saves 24 KB; readers will use synthesized italic — looks slightly worse but acceptable)

Skip — 88 KB is rounding error.

### B6. Front-matter consolidation

Current front matter: 13 chapters, 48.5 KB total. Some are redundant:
- `section-fm-1.html` (no H1 — broken)
- `section-fm-1a.html` and `section-fm-1b.html` could merge
- Pathways and syllabi pages are heavy on links — useful but not for casual readers

**Estimated savings: ~10-15 KB** — negligible.

### B7. Wisdom council page

Currently 7.1 KB compressed with 42 agent images referenced (each is its own file in `img/`). Each agent image is 50-200 KB.

If you displayed only the 6-8 agents who actually contribute epigraphs (instead of all 42), you could drop ~30 unused agent images.

**Estimated savings: 3-5 MB** if you cut agent images aggressively.

### B8. Chapter index pages

77 index files (39 chapter + 22 appendix + 11 part + others), 218.7 KB compressed total. Currently each has: epigraph + illustration + Chapter Overview heading + Sections list (just links).

On Kindle, the "Sections list" is redundant (the ToC handles this). Could slim each by ~3 KB.

**Estimated savings: ~200 KB** — modest.

### Realistic size-reduction recommendation

If you change **only image flags** (highest leverage, lowest risk):

| Setting | Estimated EPUB | Delivery fee (70%) |
|---------|---------------:|-------------------:|
| Current (1600 px, Q82) | 45.73 MB | $6.86/sale |
| **Conservative: 1280 px, Q78** | **~36 MB** | **$5.40/sale** |
| Moderate: 1200 px, Q75 | ~30 MB | $4.50/sale |
| Aggressive: 1000 px, Q70 | ~24 MB | $3.60/sale |

Add wisdom-council pruning + HTML chrome stripping:
| | EPUB | Delivery fee |
|--|--:|--:|
| Conservative + wisdom prune + HTML strip | ~30 MB | $4.50/sale |
| Moderate + wisdom prune + HTML strip | ~24 MB | $3.60/sale |

At $9.99 list price (70% royalty plan: $6.99 base):
- Current: $6.99 - $6.86 = **$0.13/sale**
- Conservative: $6.99 - $5.40 = **$1.59/sale**
- Aggressive: $6.99 - $3.60 = **$3.39/sale**

At $14.99 list (35% royalty, no fee): $5.25/sale flat — beats anything except the aggressive 70% scenario.

**My read**: stick with **35% royalty at $14.99-19.99** unless you're willing to lose meaningful image quality. The size reduction game has diminishing returns once you're at 30 MB (not enough delivery-fee savings to overtake the 35% plan).

---

## Part C — Quick wins ranked

If you want to spend a few hours upgrading the package, in this order:

| # | Action | Time | Impact area |
|---|--------|------|-------------|
| 1 | Author Central setup (both authors) | 1 hr | Trust signal on every search result |
| 2 | Description rewrite (lead with reader benefit; add companion repo / errata links) | 30 min | Conversion of search-result viewers |
| 3 | Keywords refresh (drop redundant, add framework names + model names) | 30 min | Discoverability |
| 4 | Cover thumbnail test (verify legibility at 250 px; possibly resize title) | 1 hr | Click-through rate from search results |
| 5 | Companion GitHub repo (skeleton with chapter folders + README) | 4 hr | Adoption + reviews from devs who clone |
| 6 | Pre-launch ARC outreach (50 reviewers, 2 weeks before launch) | 10 hr | Launch-day reviews (cracks the 0-review barrier) |
| 7 | Image flags `--max-image-side 1280 --jpeg-quality 78` | 5 min | EPUB → 36 MB, delivery fee $6.86 → $5.40 |
| 8 | Add "Please review" page to back of book | 15 min | ~3-5x reviewer conversion rate |
| 9 | Companion landing page (cover + buy CTA + sample download) | 6 hr | Lead magnet + email list |
| 10 | Foreword outreach to 1-2 industry figures | varies | If achievable, biggest single trust signal |

Items **1, 2, 3, 4, 7, 8** are all under 4 hours combined. They're the realistic "before launch" punch list.

---

## What I'd do if I were shipping this next week

Day 1 (4 hours):
- Author Central setup (both)
- Description rewrite
- Keywords refresh
- Cover thumbnail check + recover if needed
- Image flags adjusted, rebuild

Day 2-3 (10 hours):
- Companion GitHub repo (skeleton, README, 2-3 chapters of code)
- Companion landing page (single page on existing site or GitHub Pages)
- Add "Please review" back-page

Day 4-14 (~10 hours total):
- ARC outreach (~50 emails to ML newsletter writers, university faculty, AI Twitter accounts)
- Foreword cold outreach to 3-5 industry figures (long-shot but worth trying)

Day 15: ship to KDP. Reviews start landing within 1 week.