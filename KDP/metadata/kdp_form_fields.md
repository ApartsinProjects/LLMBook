# KDP Web Form: Field-by-Field Mapping

This file maps each field on the KDP "Create a new Kindle eBook" web form to the value to enter. Open https://kdp.amazon.com → "Create" → "Kindle eBook" and follow the three-step wizard.

---

## Step 1: Kindle eBook Details

### Language
> **English**

### Book Title
> **Building Conversational AI with LLMs and Agents**

### Subtitle (optional)
> **From the mathematics of attention to production agent systems**

### Series (optional)
Leave blank, or fill if you plan a series of related books.

### Edition Number (optional)
> **5**

### Author
- Primary author: **Alexander Apartsin**
- (KDP allows one primary author; co-author goes in Contributors)

### Contributors (optional, up to 9)
| Role | Name |
|------|------|
| Author | Yehudit Aperstein |

(Use role "Author" for both, since both contributed equally. KDP supports: Author, Editor, Foreword by, Illustrator, Introduction by, Narrator, Photographer, Preface by, Translator, Other.)

### Description (max 4000 characters, basic HTML allowed)
> Paste the contents of [description.html](description.html). Already under 4000 characters.

### Publishing Rights
> **I own the copyright and I hold the necessary publishing rights.**

### Keywords (up to 7)
> See [keywords.txt](keywords.txt) — paste each one into a separate keyword box:
> 1. large language models textbook
> 2. build AI agents production
> 3. RAG retrieval augmented generation guide
> 4. transformer architecture from scratch
> 5. LLM fine tuning LoRA RLHF
> 6. prompt engineering practitioners guide
> 7. machine learning deep learning NLP

### Categories (up to 3)
> See [categories.txt](categories.txt) for category paths. Click "Choose categories" and pick:
> 1. Computers > Computer Science > Artificial Intelligence (= COM004000)
> 2. Computers > Computer Science > Neural Networks (= COM044000)
> 3. Computers > Programming > General (= COM051300)

### Age and Grade Range (optional)
> Leave blank — adult/general technical audience.

### Pre-order
> Choose "I am ready to release my book now" unless you want to schedule a launch.

---

## Step 2: Kindle eBook Content

### Manuscript
> Upload **`KDP/output/building-conversational-ai-llms-agents.epub`**

### Kindle eBook Cover
> Upload **`KDP/cover/cover_kdp.jpg`**
> (KDP recommends 1600 x 2560 px JPEG, sRGB, < 50 MB. The cover_kdp.jpg meets these requirements; see `KDP/cover/cover_notes.md` for source/processing details.)

### Kindle eBook ISBN (optional)
> Leave blank unless you have purchased an ISBN. Amazon assigns an ASIN automatically.

### Publisher (optional)
> Either leave blank, enter "Independently published", or use your own imprint name.

### Reading Age (optional)
> Leave blank.

### Digital Rights Management (DRM)
> **No** (recommended for a technical book — DRM can prevent legitimate buyers from reading on third-party Kindle apps and rarely deters piracy).

### Kindle eBook Preview
> Use Kindle Previewer (free download from KDP) or the in-browser previewer to spot-check 5-10 pages. See [validation/kdp_checklist.md](../validation/kdp_checklist.md).

---

## Step 3: Kindle eBook Pricing

### KDP Select Enrollment
> **No** (recommended initially) — KDP Select gives you Kindle Unlimited royalties and 5 promo days per 90-day period, but requires 90-day Amazon exclusivity. For a textbook with potential institutional sales, exclusivity is restrictive.

### Territories
> **All territories (worldwide rights)**.

### Primary Marketplace
> **Amazon.com** (US).

### Royalty and Pricing
KDP offers two royalty plans:

| Plan | Royalty | Price range | Notes |
|------|---------|-------------|-------|
| **35%** | 35% of list price | USD 0.99 to 200.00 | All territories. No delivery fee. Pick this if you want to price > USD 9.99. |
| **70%** | 70% of (list price minus delivery fee) | USD 2.99 to 9.99 | Only some territories at 70%; falls back to 35% elsewhere. Delivery fee ~ USD 0.15/MB; a 30 MB EPUB costs ~ USD 4.50/sale in delivery, so net royalty drops sharply for large files. |

**Recommendation for this textbook (typical EPUB ~25-50 MB given images):**
- Set list price to **USD 9.99** and pick **70% royalty** (~USD 5.50 net per sale after typical delivery fee).
- Or set list price to **USD 14.99-19.99** with **35% royalty** (~USD 5.25-7.00 net per sale; preserves higher list price perception for a technical text).
- Either is reasonable; the 35% plan often wins for textbooks because the list price is more flexible.

### Matchbook
> Optional. Lets buyers of your print book buy the Kindle for USD 0.99-2.99. Ignore if you have no print edition.

### Book Lending
> **Enabled** for 70% royalty (mandatory). Optional for 35%.

---

## After You Click "Publish"

- Amazon validates the EPUB and cover (typically 24-72 hours).
- You will receive an email when the book is live with an ASIN and a Kindle store URL.
- Sales reports appear in the KDP dashboard within ~24 hours of first sale.
- You can update metadata, cover, and manuscript at any time after publication; updates trigger re-review.
- For first-time publishers, KDP may require tax interview (W-8BEN for non-US authors, W-9 for US) before publishing — complete this in Account → Tax Information.
