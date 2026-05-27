# 1042_LLMProjectExamples — Per-Slide Summary

**Source file:** `1042_LLMProjectExamples.pptx`
**Source folder:** `SlidesPool/1040_LLM_SampleProjects/`
**Drive link:** https://drive.google.com/file/d/1ycwhSDxEyaeJASXkZMH-cjy86y6V3dgW/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render. Each numbered project slide carries one decorative image; structural content lives in the parsed text.

---

## Slide 1 — LLM Projects Examples
Title slide framing the deck as a tour of past-course LLM projects.

## Slide 2 — 1. Resume Classification
The project filters resumes by candidate seniority. Challenges: candidates self-misreport seniority, and the seniority signal depends on the job role and the technical stack. Framing is text classification supported by synthetic data generation via attributed generation (job role) and role-playing generation (pretend to be a senior or junior), supplemented by scraped real resumes with manual labels.

## Slide 3 — 2. Code Review Assistant
The project distinguishes simple, self-descriptive code changes from complex changes that require human review. The challenge is that a classifier can be trained where training data exists (established languages and frameworks) but cannot for a new project, language, or framework. The framing is to translate previous code changes into the target language with GPT-4.1 and train a fine-tuned CodeBERT classifier on the translated data, then compare against performance on real target-language data; the example uses Java to C++ translation.

## Slide 4 — 3. Course Review Analysis
The project analyzes student course reviews to drive improvements. The challenge is that one review may give different ratings to different aspects (interesting, helpful, challenging). The framing is aspect-based sentiment analysis (ABSA), with attributed synthetic data conditioned on course, selected aspects, and target scores, plus 100 manually labeled real reviews from Kaggle. Modeling is fine-tuned BERT.

## Slide 5 — 4. Lyrics Emotion
The project attributes song lyrics to basic emotions. Challenges include multiple emotions per song and inherent subjectivity. Framing is multiple regression scoring per emotion; labeling uses 497 Kaggle Spotify songs with multiple raters and a Mean Opinion Score aggregation per emotion.

## Slide 6 — 5. Click Bait Style Detector
The project detects and filters clickbait articles. The challenge is that clickbait is hard to detect from content alone and is mostly identifiable by style. The framing is clickbait style detection on a synthetic dataset generated explicitly using ten common clickbait tactics as the style controls.

## Slide 7 — 6. Detect Language Bias
The project detects and rewrites gender-biased generated text. The challenge is context dependence: "a teacher said, he..." may or may not be biased depending on prior mentions. The framing classifies sentence pairs into justified or unjustified bias assumption and rewrites sentences with random assumption; synthetic data is generated via prompt engineering to produce pairs with explicit or implicit gender assumptions.

## Slide 8 — 7. Medical Interrogation
The project evaluates medical professionals on asking the right questions to reach an accurate diagnosis. The challenge is that no quantitative benchmark or protocol exists. The framing creates both a dataset and an evaluation methodology by generating synthetic patient descriptions in partial-information and complete-information variants and role-playing patient and doctor with separate LLM instances. Evaluation is similarity between true and predicted diagnosis after each interrogation round.

## Slide 9 — 8. Diagnosis from noisy texts
The project classifies noisy patient self-descriptions. The challenge is that patients omit information, use fuzzy terms, or add irrelevant noise. The framing is classification on a synthetic dataset that adds noise to clean patient stories.

## Slide 10 — 9. Identify critical medical issues in pharma forums
The project flags forum questions about medications that indicate critical issues needing immediate attention. The challenge is that detection requires medication knowledge and probable side effects. The framing is RAG-based text classification using DrugBank and the WHO Essential Medicines List as the retrieval corpus, evaluated on the labeled MedInfo2018 dataset.

## Slide 11 — 10 Automated Radiology Impression
The project automates radiologist "impressions" (the summary of findings). The challenge is that the input is semi-structured (findings, indications, comparisons) and the same impression can be worded many ways. The framing is summarization with LLM judges defining clinical equivalence, evaluated on the IU-Xray corpus of 4K radiology reports.

## Slide 12 — 11. Triage from free text
The project identifies case urgency from the first verbal case description. Challenges are that no recorded first textual encounter exists (only structured post-triage data) and descriptions are noisy and incomplete. The framing is text classification, with synthetic data generation producing natural-language case descriptions.

## Slide 13 — Papers
Three images of paper screenshots, included as a reference list of the publications behind the example projects.

---

## Deck-level takeaway
The deck is a quick-reference catalog of eleven past LLM projects, each compressed into one slide with motivation, challenge, ML framing, data strategy (often synthetic with attribute or role-playing prompting), and model or evaluation choice. The collection spans HR (resume seniority), software engineering (code-review triage with cross-language transfer), education (course-review ABSA), creative-arts NLP (lyric emotion regression), media (clickbait style detection), fairness (gender-bias detection and rewriting), and a large medical block (interrogation evaluation, noisy-text diagnosis classification, pharma-forum critical-issue RAG, radiology-impression summarization, free-text triage). The unifying patterns across the catalog are heavy use of synthetic data, attribute or style-conditioned generation, and benchmarking fine-tuned encoders against off-the-shelf or zero-shot LLM baselines.
