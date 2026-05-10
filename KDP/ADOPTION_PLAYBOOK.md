# Adoption Playbook

Concrete steps for the manual work the publishing pipeline can't do for you. Items here correspond to the original [`REVIEW_AND_OPPORTUNITIES.md`](REVIEW_AND_OPPORTUNITIES.md) recommendations that require human action (Amazon login, outreach emails, etc.).

---

## A1. Amazon Author Central setup (~1 hour, both authors needed)

**Why this matters:** Without Author Central, your book page on Amazon shows "by Alexander Apartsin" as plain text — no clickthrough, no photo, no bio, no follow button. With Author Central, every visitor sees a thumbnail of you, your bio, and a "Follow" button that notifies them when you publish next. This is the single highest-leverage trust signal you can add for free.

### Steps for Alexander Apartsin

1. Go to <https://authorcentral.amazon.com> and sign in with the same Amazon account you use for KDP.
2. Click **"Add another book"** → search for the ASIN once the book is live.
3. Confirm authorship (Amazon may ask for verification — usually instant if the KDP and Author Central accounts match).
4. Fill in:
   - **Profile photo** — high-res headshot, square. Suggested source: from `front-matter/images/Sasha Apartsin.jpg` (already in the book).
   - **Biography** — paste from `front-matter/about-authors.html`, or write a fresh 2-paragraph version focused on AI/LLM credibility.
   - **Other books authored** — link to any earlier publications.
   - **Website** — `https://www.apartsin.com` and `https://llmbook.apartsin.com`
   - **Twitter/X handle** — if you have one
   - **Blog/feed URL** — if you publish on Medium or substack
5. Save. The Amazon book page updates within ~24 hours.

### Steps for Yehudit Aperstein

Same process. Use:
- Photo: `front-matter/images/yehudit-aperstein.png`
- Bio: from `about-authors.html`, focus on academic credentials + ICSGen.AI
- Website: <https://www.afeka.ac.il/en/faculty-en/yehudit-aperstein/>
- LinkedIn: <https://www.linkedin.com/in/yehudit-aperstein-ph-d-22bb4615/>

### Verification

Within 24 hours of setup, search the book on Amazon and confirm:
- [ ] Author photo appears under "About the author"
- [ ] Bio is shown
- [ ] "Follow" button is present
- [ ] Both authors are listed (Yehudit shows after clicking "+ More")

---

## A10. Foreword / endorsement outreach (~1 week, long-shot but high-impact)

**Why this matters:** A 1-paragraph endorsement from a recognized industry figure becomes a quotable blurb you can use everywhere — book cover, Amazon description, social posts, instructor outreach emails. Even a non-endorsement reply ("Looks great, congrats on shipping!") provides a relationship for future outreach.

### Target list (in priority order)

Tier 1 — most impactful, hardest to reach:
- **Andrej Karpathy** (formerly OpenAI/Tesla) — `karpathy@gmail.com` reportedly works; or DM on X (@karpathy)
- **Sebastian Raschka** (Lightning AI, author of "Build a Large Language Model From Scratch") — <https://sebastianraschka.com/contact/>
- **Chip Huyen** (formerly NVIDIA, author of "AI Engineering") — via her personal site contact
- **Jeremy Howard** (fast.ai, author of fastai book) — <https://www.fast.ai>

Tier 2 — moderately reachable, very impactful:
- Hugging Face engineering team (Lewis Tunstall, Leandro von Werra, Omar Sanseviero — visible on Twitter, often reply)
- Anthropic research/engineering folks who post publicly (Amanda Askell, Saurav Kadavath)
- OpenAI cookbook contributors
- LangChain core team (Harrison Chase)

Tier 3 — academic peers, very reachable:
- Faculty in NLP/ML at Israeli universities (Hebrew U, Tel Aviv U, Technion, Weizmann) — direct via co-author Aperstein's network
- Authors of any book or paper you cite extensively in the book — find their email at their university page
- AI newsletter writers ("The Batch", "Import AI", "AI Tidbits", "TLDR AI", "Latent Space") — they reply to short, specific outreach

### Email template

Subject: **`<Their first name>, would you read a chapter of our LLM textbook?`**

```
Hi <Name>,

I'm Alexander Apartsin, faculty at Holon Institute of Technology. My
co-author Yehudit Aperstein (Afeka) and I just finished a 39-chapter
textbook on building LLMs and agents — from PyTorch foundations through
production agent systems.

I noticed your work on <SPECIFIC THING THEY DID — paper, library, talk>
and thought of you because <SPECIFIC CONNECTION — your chapter X
references their work / your style is similar / you're in the audience
they target>.

If you have 10 minutes to read a sample chapter, I'd love your honest
take. If you'd consider writing a 1-paragraph endorsement we could use
on the book's back cover and Amazon page, I'd be deeply grateful.

Sample chapter (PDF, ~30 pages):
https://llmbook.apartsin.com/downloads/sample-chapter-prompt-engineering.pdf

Full ToC: https://llmbook.apartsin.com

No pressure either way. Thanks for considering.

— Alexander
   www.apartsin.com
```

**Tips:**
- Personalize the SPECIFIC THING per recipient — generic outreach gets ignored.
- 1-2 sentences max for the personalization.
- Don't ask for "a foreword" upfront — ask for a read. The endorsement comes naturally if they like it.
- Send 3-5 per week, not 30 in one batch. Quality > quantity.
- Conversion estimate: ~10% reply rate, ~25% of replies become endorsements. So 20 emails → 2 reads → 0.5 endorsements. Aim for 30-50 emails total.

### Where to use endorsements once received

- **Amazon description** — top of "Editorial Reviews" section (Author Central → Books → Edit)
- **Book back cover** — for print edition (revise cover artwork if needed)
- **Foreword section** — if a Tier 1 person writes a real foreword, add to `front-matter/foreword-by-X.html`
- **Landing page hero** — single-line quote with portrait
- **LinkedIn launch post** — endorsements drive social shares
- **Book launch email to Apartsin Medium followers**

---

## A11. Multi-distribution beyond Amazon (~3 hours, +15-30% revenue)

KDP exclusivity is only required if you enroll in KDP Select. If you're not in Select (the default per your `metadata.yaml`), you can sell the same EPUB on:

- **Apple Books** — direct via <https://itunesconnect.apple.com> (free, takes 30%; requires Mac for some upload steps)
- **Kobo Writing Life** — <https://www.kobo.com/writinglife> (free, 70% royalty up to $12.99)
- **Google Play Books** — <https://play.google.com/books/publish> (free, 52% royalty)
- **Barnes & Noble Press** — <https://press.barnesandnoble.com> (free, 65% royalty)

Easiest single-upload path: **Draft2Digital** (<https://draft2digital.com>) — they distribute to all of the above plus Scribd, Tolino, and library systems. Take 10% off the top but save you 4× the upload work.

Recommended sequence:
1. Launch on KDP first (shortest review time, biggest market)
2. After 2 weeks (once KDP version is stable), upload to Draft2Digital
3. Apple Books direct only if you have a Mac and want the extra 5% royalty

---

## A12. Pre-launch ARC (Advance Reader Copy) outreach (~10 hours over 2 weeks)

**Goal**: 8-15 honest reviews live on Amazon within 1 week of launch. Without ARC, books typically take 3-6 months to accumulate first 10 reviews.

### Where to find reviewers

| Source | Cost | Realistic conversion | Notes |
|--------|------|---------------------|-------|
| **BookSirens** | $30 one-time + $0.50/download | ~20-40% review rate | Best for niche tech books |
| **BookSprout** | Free for first 50 reviews | ~15-25% | Mass-market focused, less tech audience |
| **NetGalley** | $399/six-month listing | ~30-50% | Heavy academic/library reviewer base; worth it for textbooks |
| **Direct outreach** (newsletters, Reddit, Twitter) | Free | ~5-15% | Highest quality reviewers but most labor-intensive |
| **University faculty network** | Free | ~30-50% | Best for course adoption + endorsement combined |

### Direct outreach targets

Email these newsletter writers / community moderators with a short pitch + free EPUB:

- **AI Tidbits** (Sahar Mor)
- **The Batch** (DeepLearning.AI / Andrew Ng)
- **Import AI** (Jack Clark)
- **TLDR AI** (Dan Ni)
- **Latent Space** (swyx)
- **Last Week in AI** (Andrey Kurenkov, Sharon Zhou)
- /r/MachineLearning moderators
- /r/LocalLLaMA moderators
- /r/learnmachinelearning moderators
- HackerNews submitters with high karma in AI tags
- Twitter/X "AI educator" accounts (>10k followers, post tutorials regularly)

Email template (very short):

```
Subject: Free EPUB review copy: 800-page LLM textbook (5th edition)

Hi <Name>,

I just shipped a 5th-edition technical textbook on building LLMs and agents
(39 chapters, PyTorch through production agents). I'd love to send you a
free EPUB review copy if you'd consider reading and posting an honest
review when it goes live next month.

ToC + sample: https://llmbook.apartsin.com

Reply with the email address to send the EPUB to and I'll forward today.

— Alex Apartsin
```

### ARC operations

1. **Generate ARC EPUB**: same as the KDP EPUB, except add "ADVANCE REVIEW COPY — NOT FOR DISTRIBUTION" watermark to the cover. Build flag idea: `python KDP/build/publish.py --arc` (you would add this flag to publish.py if you want it scripted).
2. **Tracking sheet**: Google Sheet with one row per reviewer (name, contact, sent date, replied, review posted, review URL).
3. **Launch coordination**: 2 days before KDP go-live, send all ARC recipients an email with the launch date and a one-line "Honest review when convenient — no pressure on length or rating."
4. **Post-launch follow-up**: 1 week after launch, polite reminder to those who haven't reviewed yet (1 reminder only, then drop).

### Realistic outcomes

| Send | Read | Review |
|-----:|-----:|-------:|
| 50 | 20 | 8-12 |
| 100 | 35 | 15-22 |
| 200 (NetGalley + direct combined) | 70 | 30-50 |

Most academic textbooks launch with 0-2 reviews. Anything above 5 puts you ahead of 90% of self-published competitors. 15+ reviews puts you in the "trusted" tier.

---

## Summary checklist (do these before clicking "Publish" on KDP)

- [ ] Author Central account created for Alexander
- [ ] Author Central account created for Yehudit
- [ ] Author photos uploaded
- [ ] Bios written
- [ ] llmbook.apartsin.com deployed (DNS propagated, SSL green padlock)
- [ ] Sample chapter PDF generated and uploaded to landing page
- [ ] 3-5 endorsement requests sent (Tier 2 or 3 — Tier 1 are 5%-reply long-shots)
- [ ] 50 ARC outreach emails sent (or BookSirens + NetGalley listings live)
- [ ] Tracking sheet for reviewers set up
- [ ] Pricing decision made (recommended: 35% royalty at $14.99-19.99)
- [ ] Tax interview completed in KDP (W-8BEN for non-US authors)
- [ ] DRM decision: leave OFF (per `metadata.yaml`)
- [ ] KDP Select decision: NOT enrolled (so you can multi-distribute)
