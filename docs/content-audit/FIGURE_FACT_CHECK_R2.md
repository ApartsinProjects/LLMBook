# Figure Fact-Check Round 2

Agent: 39-figure-fact-checker
Branch: v2.0
Date: 2026-05-19
Scope: spot-check of ~35 figures across the book, focused on the highest-risk subset (number-rich captions, scaling-laws/benchmark figures, recent Wave 27+ illustrator output, fact-dense industry sections in Parts 11 to 16).

## Method
1. Grepped for `<figcaption>` containing numerical claims (percentages, dollars, B/M/T), then selected the densest captions.
2. For each pick, opened the surrounding SVG/image-alt and the body prose to triangulate the caption claim against what the visual really shows and what the prose says.
3. Fixed captions only when a load-bearing claim disagreed with the SVG or the prose; left metaphorical captions alone unless they made a verifiable factual claim.

## Fixes Applied

### 1. Section 75.4 - Figure 75.4.1 (Khanmigo five-layer architecture)
- BEFORE: caption said "Layers 1-3-5 (retrieval, Socratic prompt, output filter, throttle) sit in the request path".
- ISSUE: 4 named layers but only 3 layer numbers, and Socratic prompt is layer 2 in the SVG (not 3).
- AFTER: "Layers 1, 2, 3, and 5 (retrieval, Socratic prompt, output filter, throttle) sit in the request path".

### 2. Section 21.2 - Figure 21.2.2 (FUNSD error attribution)
- BEFORE: alt-text and caption claimed bars showed "30% checkbox handling, 24% multi-line, 18% OCR cascade, 14% header confusion, 14% other" summing to "72% of the remaining errors".
- ISSUE: the SVG actually plots OCR errors 38%, Reading order 22%, Long-tail keys 18%, Layout drift 14%, Other 8%. Completely different categories and percentages from the caption claim.
- AFTER: alt-text and caption updated to match the actual SVG categories and percentages; new claim is "Upstream OCR errors, reading-order confusion, and long-tail-key failures account for roughly 78% of the remaining errors at 92% F1, with OCR cascade dominating at 38%".

### 3. Section 59.4 - Figure 59.4.1 (GPipe vs 1F1B)
- BEFORE: caption claimed both panels used "P=4 stages and M=7 micro-batches" with bubble penalty ~ (P-1)/M.
- ISSUE: the SVG actually shows GPipe with M=4 (F1 to F4) and 1F1B with M=7 (F1 to F7). The GPipe panel literally labels itself "Bubble = 6/16 = 37.5%", which is the M=4 case.
- AFTER: caption now reads "GPipe (top, M=4 micro-batches) vs 1F1B (bottom, M=7), both for P=4 stages" and explicitly mentions the 37.5% bubble label.

### 4. Section 56.1 - Figure 56.1.2 (Responsible AI platform landscape)
- BEFORE: caption listed five categories: "governance suites, hyperscaler bundles, observability tools, fairness toolkits, and policy-aligned frameworks".
- ISSUE: the SVG actually shows six categories: Governance suites, Hyperscaler bundles, Observatories, LLM safety runtimes, Privacy-GRC hybrids, Open-source stacks. Neither "fairness toolkits" nor "policy-aligned frameworks" appears in the SVG.
- AFTER: caption now matches SVG categories exactly.

### 5. Section 65.2 - Figure 65.2.1 (Docker base images)
- BEFORE: caption claimed the table was "ordered by size".
- ISSUE: the rows go 150 MB, 3.5 GB, 5.5 GB, 15 GB, 8 GB. The 15 GB and 8 GB rows are out of size order.
- AFTER: rewrote caption to describe the range ("from ~150 MB to ~15 GB") without claiming ordering.

### 6. Section 74.3 - Figure 74.3.1 (Healthcare SaMD decision)
- BEFORE: caption said staying outside SaMD scope yields "$500K-$1.4M saved".
- ISSUE: the SVG shows SaMD initial cost of $500K-$2M and 50-70% savings from staying outside. 50-70% of $500K-$2M is roughly $250K-$1.4M, not $500K-$1.4M. The lower bound was wrong.
- AFTER: caption now reads "~50-70% compliance savings on a $500K-$2M baseline", matching the SVG.

### 7. Section 78.1 - Figure 78.1.1 (Manufacturing LLM patterns)
- BEFORE: caption described "maintenance copilot, inspection summarizer, work-order drafter, and supplier-risk briefer" pipeline.
- ISSUE: the image src is `comic-three-parallelism-kitchens.jpg` (borrowed from Chapter 59) and the alt-text describes "assembly-line workers in identical kitchens, then a serial pipeline of bakers, then a single big shared oven" representing data/pipeline/tensor parallelism. The image visual is unrelated to the four-station manufacturing pipeline the caption asserted.
- AFTER: caption rewritten to honestly describe what the image shows (parallel stations, serial pipelines, shared specialty equipment), still framed as factory-line analogy.

## Verified Without Changes

The following figures were spot-checked and the caption/SVG/prose triangulation passed:

- Figure 75.5.1 (Education two-market): Duolingo Max ~$540M ARR from 1.5M subscribers matches SVG.
- Figure 76.3.1 (Cybersecurity attack classes): four classes (prompt injection, training-data poisoning, membership inference, model extraction) match SVG; 0.001% Carlini threshold and Greshake 2023 attribution correct.
- Figure 69.3.1 (Token cost portfolio): four vendor buckets sum $234K + $176K + $30K + $40K = $480K vs $720K list, 33% reduction. Verified.
- Figure 69.2.1 (Input-price ladder): GPT-5.5 $3.00 / Gemini Flash 3 $0.15 = 20x gap. Verified.
- Figure 69.1.1 (ROI funnel): $10M -> -50% -> $5M -> -20% -> $4M; 4 / 1.2 = 3.33x. Verified.
- Figure 74.5.1 (Healthcare vendor map): all numbers (Hippocratic 1.5M interactions, 3M HIS + Optum at $4-5B, MS Dragon Copilot ex-Nuance DAX $19.7B) match SVG.
- Figure 75.3.1 (Education regulatory stack): COPPA $53,088 per violation matches SVG ($53K caption); ASU/UT/Wharton/Caltech ChatGPT Edu line matches prose.
- Figure 73.2.1 (Finance number-check): XBRL Hoffman 1998, SEC-mandated 2009 confirmed; LLM-narrative-only + regex-check flow matches SVG.
- Figure 59.4.1 caption corrections retained the (P-1)/M formula text since it is mathematically correct for both panels.
- Figure 6.3.2 (Chinchilla vs Kaplan): caption is generic, math elsewhere in section is correct (70B model at ~1.4T tokens = 20 tokens per parameter).
- Figure 22.1.2 (ViT variants): all token counts verified by formula (resolution / patch_size)^2 + 1.
- Figure 22.2.1 (Contrastive VLM lineage): 400M to 10B training-pair scaling and 85.8% SigLIP-2 ImageNet match table.
- Figure 22.4.1 (Three frontier VLMs): caption asserts 1-3 point benchmark gap claim is consistent with prose (MMMU 69.1 vs 72.0).
- Figure 27.4.2 (Atomic tools): "four atomic tools" matches alt-text and prose (create_record, get_record, update_record, delete_record).
- Figure 67.10.2 (Five role patterns): caption count matches table and prose.
- Figure 67.3.1 (Seven capabilities): caption count matches Table 67.3.1.
- Figure 67.15.1 (MVP gates): all per-role thresholds match Table 67.15.1.
- Figure 58.1.1 (Memory bandwidth ladder): all chip bandwidths (Cerebras 21 PB/s, B200 8 TB/s, H100 3.35 TB/s, MI355X 6 TB/s) match prose.
- Figure 58.5.2 (Sardana inference-aware): Llama 3.1 8B at 1800:1 verified (15T / 8B = 1875).
- Figure 80.4.1 (Universal recipe): "seven domain sources" count verified; Evo-2 4 nucleotides 1M-bp context, Chronos 4096 bins, EnCodec ~75 tokens/sec all verified.
- Figure 16.7.2 ("Lost in the middle"): 98% primacy / ~45% midpoint / 95% recency all match SVG labels.
- Figure C.1.2 (Precision formats for 7B): 28 GB / 14 GB / 7 GB / 4 GB at 32 / 16 / 8 / 4 bits all consistent (7 GB-params * bits / 8).
- Figure 23.1.1 + Table 23.1.2 (Gaussian splatting parameter budget): per-Gaussian byte counts (12 MB / 16 MB / 12 MB / 4 MB / 192 MB) all verified for 1M Gaussians.
- Figure 57.1.2 (Workload categories): 12x cost spread ($4800 / $400) verified.
- Figure 9.6.1 (Reasoning models): 5000 thinking tokens, 83% AIME, 13% GPT-4o baseline, 30-120 s latency, ~$0.50 all match SVG.

## Notes on Scope and Bias

- I focused on Parts 6, 9, 11, 12, 13, 14, 15, 16 (industry chapters and frontier/scale chapters with the most fact-dense captions), plus a smattering of Parts 1 to 5 to confirm older figures still hold.
- Style issues (em dashes, double-dashes) were intentionally left to the visual-identity agent, per task framing.
- Did not refresh references to external companies or products (bibliography agent's lane).
- Did not regenerate any SVGs; all fixes are caption / alt-text edits that bring the prose in line with what the image already shows.

## Suggested Follow-Up
- Figure 21.2.2's SVG was clearly drawn against a different (more generic) error-attribution scheme than the prose was originally written for. The prose still references checkbox / multi-line / OCR cascade categories; consider redrawing the SVG to match the FUNSD-specific error categories the prose discusses, or further softening the prose to talk about generic error attribution. Flagging for content authors.
- Figure 78.1.1 image (parallelism kitchens) is a generic stand-in. A dedicated factory-line illustration showing maintenance copilot / inspection summarizer / work-order drafter / supplier-risk briefer would land the caption claim better. Flagging for illustrator team.
