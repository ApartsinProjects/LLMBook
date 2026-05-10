# Publishing Guide: KDP Submission Walkthrough

This is the end-to-end walkthrough for submitting **Building Conversational AI with LLMs and Agents** to Amazon KDP. Allow ~30 minutes to complete the form, plus 24-72 hours for Amazon review.

## Prerequisites (one-time)

1. **Amazon account**: Use your existing Amazon shopper account.
2. **KDP account**: Sign up at https://kdp.amazon.com (free).
3. **Tax interview**: Account → Tax Information.
   - Non-US authors: W-8BEN
   - US authors: W-9
   - Without this, KDP will not let you publish.
4. **Bank account**: For royalty payments. KDP wires monthly when balance > USD 100 (or smaller via direct deposit in some regions).
5. **Author profile** (optional): Create at Author Central (https://authorcentral.amazon.com) to add your bio, photo, and sync books to a single author page.

## Pre-submission checklist

Before you click "Create eBook", verify:

- [ ] EPUB built successfully: `KDP/output/building-conversational-ai-llms-agents.epub` exists
- [ ] Validation passed: re-run `python KDP/validation/structural_check.py` and confirm "RESULT: PASS"
- [ ] Cover meets KDP specs: `KDP/cover/cover_kdp.jpg` is 1600 × 2560 sRGB JPEG
- [ ] You've reviewed `KDP/metadata/description.html` for accuracy
- [ ] You've reviewed `KDP/metadata/keywords.txt` and `categories.txt`
- [ ] (Recommended) You've previewed the EPUB in Kindle Previewer
- [ ] (Recommended) You've run the official epubcheck (see [validation/epubcheck_instructions.md](validation/epubcheck_instructions.md))

## Step 1 of 3: Kindle eBook Details

Open https://kdp.amazon.com → **Create** → **Kindle eBook**.

### Language
Select: **English**

### Book Title and Subtitle

| Field | Value |
|-------|-------|
| Book Title | Building Conversational AI with LLMs and Agents |
| Subtitle | From the mathematics of attention to production agent systems |

### Series
Skip unless you plan a multi-book series.

### Edition Number
Enter: **5**

### Author

KDP allows one primary author. Enter:
- First name: **Alexander**
- Last name: **Apartsin**

### Contributors

Click "Add Another" and enter the second author with role "Author":
- First name: **Yehudit**
- Last name: **Aperstein**

### Description

Open `KDP/metadata/description.html` in any text editor, copy the entire contents, and paste into the Description box. KDP accepts basic HTML (`<b>`, `<i>`, `<ul>`, `<li>`, `<p>`, `<h2>`, `<h3>`). The provided file uses only allowed tags and is 3,359 characters (under the 4,000 limit).

### Publishing Rights

Select: **I own the copyright and I hold the necessary publishing rights.**

### Keywords

Open `KDP/metadata/keywords.txt` and paste each line into a separate keyword box (KDP gives you 7 boxes):

1. large language models textbook
2. build AI agents production
3. RAG retrieval augmented generation guide
4. transformer architecture from scratch
5. LLM fine tuning LoRA RLHF
6. prompt engineering practitioners guide
7. machine learning deep learning NLP

### Categories

Click "Choose categories" and pick three from the browser. The three to pick (per `KDP/metadata/categories.txt`):

1. **Computers > Computer Science > Artificial Intelligence** (BISAC: COM004000)
2. **Computers > Computer Science > Neural Networks** (BISAC: COM044000)
3. **Computers > Programming > General** (BISAC: COM051300)

If KDP's tree has changed and these exact paths don't exist, see `KDP/metadata/bisac_reference.md` for fallback options.

### Age and Grade Range
Leave blank (general adult / professional audience).

### Pre-order
Select: **I am ready to release my book now.**

Click **Save and Continue**.

## Step 2 of 3: Kindle eBook Content

### Manuscript

Click "Upload eBook manuscript" and select:

`KDP/output/building-conversational-ai-llms-agents.epub`

KDP will run server-side validation. Possible issues at this stage:

| KDP message | Likely cause | Fix |
|-------------|--------------|-----|
| "Spelling errors" | False positives in code blocks / technical terms | Review and dismiss; can ignore |
| "Image quality" | Cover or interior images < 300 DPI equivalent | Re-render images at higher resolution |
| "Hyperlinks point to internal pages" | Wrong; these are correct after build | Should not occur with this EPUB |
| "Manuscript exceeds size" | EPUB > 650 MB | Reduce image quality with `--jpeg-quality 70 --max-image-side 1200` and rebuild |

If validation fails with a real error, the KDP web UI shows where in the EPUB the problem is. Fix in the source HTML, rebuild, re-upload.

### Kindle eBook Cover

Choose "Upload a cover you already have" → upload:

`KDP/cover/cover_kdp.jpg`

Skip "Use Cover Creator" (it's a basic Amazon tool aimed at novelists, not technical books).

### ISBN
Leave blank unless you have one. Amazon assigns an ASIN.

### Publisher (optional)
Either leave blank, enter your imprint name, or enter "Independently published".

### Reading Age (optional)
Leave blank.

### Digital Rights Management (DRM)

Select: **No, do not enable DRM.**

(DRM cannot be removed after publication. For technical books, DRM mostly inconveniences legitimate buyers; the audience is sophisticated enough to find unprotected copies regardless.)

### Preview

Click "Launch Previewer" or download Kindle Previewer (free, recommended for thorough check). Browse 5-10 pages to confirm:

- Cover displays correctly
- Table of Contents navigates properly
- Code blocks aren't truncated
- Images render
- Headings have proper hierarchy

Click **Save and Continue**.

## Step 3 of 3: Kindle eBook Pricing

### KDP Select

Select: **No** (recommended initially).

KDP Select gives you 5 promo days per 90-day period and inclusion in Kindle Unlimited. The cost is **90-day Amazon exclusivity** for the eBook (you cannot sell it on Kobo, Apple Books, Google Play, or your own site for that period). You can re-enroll every 90 days.

For a textbook with potential institutional, university bookstore, or international sales, exclusivity is restrictive. Defer this decision; you can enroll later.

### Territories

Select: **All territories (worldwide rights).**

### Primary Marketplace

Select: **Amazon.com** (US store).

### Royalty and Pricing

KDP offers two royalty plans. **Pick one.**

#### Option A: 70% royalty

- List price range: USD 2.99 to 9.99
- Royalty rate: 70% of (list price minus delivery fee)
- Delivery fee: ~ USD 0.15 / MB
- For this 70 MB EPUB, delivery fee = **~ USD 10.61 / sale**, so the 70% plan is **not viable** unless the book is dramatically smaller.

#### Option B: 35% royalty (recommended for this book)

- List price range: USD 0.99 to 200.00
- Royalty rate: 35% of list price
- No delivery fee
- All territories at this rate

**Recommended price: USD 14.99 - 19.99**

| List price | Royalty per sale (35%) |
|------------|------------------------|
| USD 9.99   | USD 3.50 |
| USD 14.99  | USD 5.25 |
| USD 19.99  | USD 7.00 |
| USD 29.99  | USD 10.50 |

For comparable LLM/AI textbooks on Amazon (Sebastian Raschka's "Build a Large Language Model From Scratch", Chip Huyen's "AI Engineering"), USD 19.99 - 39.99 is the going rate for the Kindle edition.

### International Pricing

KDP offers automatic conversion ("convert from US price") or manual entry per marketplace. Automatic is fine for a first launch.

### Matchbook
Skip (only relevant if you have a print edition).

### Book Lending

For 70% royalty, lending is mandatory. For 35%, optional. **Recommend: leave enabled** (allows 14-day Kindle lending; minor revenue impact, mild promo).

Click **Publish Your Kindle eBook**.

## After submission

- KDP shows a confirmation screen with a status of "In Review".
- Within 24-72 hours, you receive an email when the book is live.
- The book gets:
  - An ASIN (B0xxxxxxxx)
  - A Kindle store URL (https://www.amazon.com/dp/B0xxxxxxxx)
  - Eligibility for Look Inside, Kindle preview, Wishlist
- Sales reports appear in the KDP dashboard within ~24 hours of first sale.
- You can update metadata, cover, or manuscript at any time. Updates trigger re-review (typically faster than initial review).
- If KDP rejects your submission, the email lists specific issues; fix and resubmit through the same dashboard.

## Updating after publication

- Bug fix or content update? Bump the metadata revision in `metadata.yaml`, rebuild the EPUB, and use the KDP dashboard to upload the new file. Existing customers are notified via the Manage Your Content page; they can opt-in to the update.
- Cover update? Same flow. KDP recommends NOT changing the cover within the first 30 days unless absolutely necessary (it can confuse early reviewers).
- Price update? Takes effect within 6-24 hours; no re-review.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Your book contains spelling errors" | Often false positives in code/technical text. Click "Ignore" in the report. |
| Cover thumbnail looks blurry on Amazon | Wait 24h after publication; cover thumbnails take time to regenerate. If still blurry, re-upload at native 1600 × 2560. |
| Book is live but wrong category | Email KDP support requesting category re-assignment; they accept up to 10 categories total post-launch. |
| Book is live but no reviews | Normal. Run a friends/colleagues launch to seed reviews. Avoid review-buying services - Amazon's algorithms detect and remove. |
| KDP rejects EPUB with "validation errors" | Run epubcheck (see `validation/epubcheck_instructions.md`); fix the specific files it flags. |

## Resources

- KDP Help: https://kdp.amazon.com/en_US/help
- KDP Community Forums: https://kdp.amazon.com/community
- Kindle Previewer: https://kdp.amazon.com/en_US/help/topic/G202131170
- BISAC Subject Headings: https://bisg.org/page/BISACSubjectCodes
- Amazon Author Central: https://authorcentral.amazon.com
