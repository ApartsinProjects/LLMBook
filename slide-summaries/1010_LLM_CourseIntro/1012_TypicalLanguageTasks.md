# 1012_TypicalLanguageTasks — Per-Slide Summary

**Source file:** `1012_TypicalLanguageTasks.pptx`
**Drive folder:** `SlidesPool/1010_LLM_CourseIntro/`
**Drive link:** https://drive.google.com/file/d/1g1vQGvjfENXq4EaNeOVlMdPcUaaBEE-n/view
**Slide count (exact, via python-pptx):** 24
**Extraction:** Local parse from downloaded .pptx (title placeholders, body text, image/table/chart counts, speaker notes). Image-bearing slides additionally rendered as PNGs via PowerPoint COM and visually analyzed (see slides 22, 23, 24).

---

## Slide 1 — Natural Language Processing

The opening title slide of the deck. The main title reads "Natural Language Processing" with the subtitle "Typical Tasks", framing the deck as a catalogue rather than a deep dive into any single method. It sets up the central question of the deck: what are the recurring problems that the NLP and LLM toolbox is repeatedly asked to solve?

## Slide 2 — Typical NLP Tasks (motivation)

Before listing the tasks, this slide explains *why* recognizing standard NLP tasks matters. The argument has two prongs. First, identifying known tasks inside a real application's requirements allows the developer to *reuse* ideas, components, libraries, and code that have already been built and tuned for that task family; you don't reinvent named-entity recognition every time. Second, the same task vocabulary is useful as *inspiration for course projects*: the reader is encouraged to frame their project as a sequence of customized, composed standard NLP tasks. The slide thus positions the rest of the deck as a vocabulary the reader will use to decompose later work.

## Slide 3 — 1. Text Classification

Defines text classification as assigning predefined categories or labels to text based on its content, typically using supervised learning to predict among a discrete set of classes. The slide grounds the abstraction with five canonical applications: sentiment analysis of product reviews (positive / negative / neutral), spam detection in email (spam vs. not spam), topic categorization of news articles (politics / sports / technology), intent detection in chatbots (booking / inquiry / complaint), and toxic-comment filtering on social media (toxic vs. non-toxic). The unifying signature is "text in, single label out", which the reader should learn to recognize anywhere in an application spec.

## Slide 4 — 2. Named Entity Recognition (NER)

Defines NER as identifying and classifying named entities in text, such as persons, organizations, and locations, into a predefined category set. The applications span domains: extracting company names from financial reports, identifying locations in travel blogs for geotagging, recognizing people's names in legal documents for anonymization, tagging medical entities (drug names) in clinical notes, and extracting product names from e-commerce reviews. NER differs from classification because the output is a set of *spans* (positions plus labels) rather than a single label on the whole document.

## Slide 5 — 3. Machine Translation

Defines machine translation as automatically translating text from one language to another while preserving meaning and context. The five enumerated applications cover the major commercial drivers: translating websites for global accessibility, real-time translation in messaging apps, localizing software interfaces for different markets, translating legal contracts for international firms, and converting academic papers for cross-country collaboration. The implicit subtlety, hinted at by "preserving meaning and context", is that translation is not word-for-word substitution; it depends on the model's representation of the source.

## Slide 6 — 4. Text Summarization

Defines summarization as generating a concise and coherent summary of a longer text, and introduces the standard split between *extractive* summarization (selecting key sentences verbatim from the source) and *abstractive* summarization (paraphrasing the content in new wording). Applications cited include summarizing news articles for quick reading, condensing research papers for literature reviews, creating executive summaries of business reports, generating previews of blog posts for social media, and summarizing customer-support tickets for faster resolution. The extractive-vs-abstractive distinction quietly previews the difference between selection-based and generation-based models that the course will revisit.

## Slide 7 — 5. Question-Answering

Defines QA as providing precise answers to user questions by extracting relevant information from a text corpus or knowledge base. The applications run from consumer to professional contexts: powering virtual assistants like Siri or Alexa, supporting customer-service chatbots for FAQs, enabling search engines to return direct answers rather than result lists, assisting students with study tools for textbooks, and helping doctors retrieve answers quickly from medical databases. The phrase "from a text corpus or knowledge base" foreshadows the later distinction between closed-book QA (the model answers from its weights) and retrieval-augmented QA (the model answers from a passed-in document).

## Slide 8 — 6. Text Generation

Defines text generation as creating coherent and contextually relevant text, often using models like GPT, for creative or assistive purposes. The applications span writing marketing copy for advertisements, generating fictional stories or poetry, autocompleting emails in productivity tools, creating chatbot responses for engaging conversations, and producing synthetic data for NLP model training. The last application is a quietly important one: text generation is not only an output but also an *input* to other NLP pipelines, used to manufacture training data when human labels are scarce.

## Slide 9 — 7. Topic Modeling

Defines topic modeling as identifying latent topics within a collection of documents by clustering words and phrases that frequently co-occur. Applications include analyzing customer feedback to identify common themes, organizing large archives of academic papers by topic, detecting trending topics in social media posts, categorizing support tickets for issue prioritization, and summarizing public opinion in survey responses. Unlike text classification, topic modeling is *unsupervised*: there is no predefined label set; the topics are discovered from the data itself.

## Slide 10 — 8. Text Similarity Scoring

Defines text similarity scoring as measuring how similar two pieces of text are in meaning, often using cosine similarity or vector embeddings. The applications hinge on duplicate or near-duplicate detection: detecting plagiarism in academic papers, recommending similar articles in news apps, clustering customer queries for support automation, matching resumes to job descriptions, and identifying duplicate user reviews on e-commerce platforms. The mention of "cosine similarity or embeddings" is the first explicit reference in this deck to the vector-space view of language that underpins both retrieval and modern dense retrieval / RAG systems.

## Slide 11 — 9. Dialog Systems

Defines dialog systems as building conversational agents (chatbots or virtual assistants) that engage in human-like dialogue. Example applications include customer-support chatbots for e-commerce, virtual tutors for educational platforms, mental-health chatbots for emotional support, booking assistants for travel agencies, and interactive NPCs in video games. The defining property, implicit here, is *statefulness across turns*: a dialog system has to track context, which differentiates it from one-shot QA or generation.

## Slide 12 — 10. Text Normalization

Defines normalization as standardizing text by correcting inconsistencies such as spelling errors, abbreviations, informal terms, or formatting. The applications are largely preprocessing chores: preprocessing social-media posts for analysis, standardizing medical records for data integration, correcting user input in search engines, normalizing transcripts for speech-to-text systems, and cleaning datasets for NLP model training. The slide sits inside a list of headline tasks but functions as a reminder that much of the engineering work in any NLP system happens *before* the model is invoked.

## Slide 13 — 11. Relation Extraction

Defines relation extraction as identifying and classifying semantic relationships between entities in text, formalized as triples like "X works for Y". Applications include building knowledge graphs from Wikipedia articles, extracting employee-organization links from resumes, identifying drug-disease relationships in medical texts, mapping family relationships in genealogical records, and detecting business partnerships in news. Conceptually this is the natural successor to NER: NER finds the entities, relation extraction finds how they are connected, and the two together populate a knowledge graph.

## Slide 14 — 12. Code Generation

Defines code generation as producing executable code from natural-language descriptions of desired functionality, with the explicit note that LLMs are central to translating intent into syntactically correct code. Applications include generating Python scripts for data analysis from user descriptions, creating HTML/CSS layouts from website design requests, producing SQL queries from natural-language database questions, generating unit tests for software functions described in text, and writing JavaScript front-end functions from user stories. From this slide onward the framing tilts noticeably toward *LLM-era* tasks ("LLMs are key for...") rather than classical NLP.

## Slide 15 — 13. Text Style Transfer

Defines style transfer as modifying the style or tone of text (e.g., formal to casual) while preserving the core meaning, again noting that LLMs are critical for maintaining coherence and style consistency. Applications include converting technical reports into conversational blog posts, transforming casual customer reviews into formal testimonials, adapting academic writing to journalistic styles for press releases, rewriting corporate emails in a friendly tone, and converting legal texts into plain language for accessibility. The hard part, hinted at implicitly, is the meaning-preservation constraint: a style-transferred text must change *how* it says something without changing *what* it says.

## Slide 16 — 14. Text Entailment Detection

Defines entailment detection (natural language inference) as determining whether one text (the hypothesis) logically follows from another (the premise), and frames it as a reasoning task where LLMs capture semantic relationships. Applications include verifying claims in fact-checking platforms against source texts, validating consistency in legal arguments within case documents, checking alignment between product descriptions and user reviews, assessing coherence in automated news summaries, and evaluating student-essay arguments against reference materials. This is the deck's first explicit "reasoning" task and is the closest classical-NLP cousin of LLM evaluation benchmarks like MNLI or RTE.

## Slide 17 — 15. Knowledge-Augmented Text Generation

Defines this task as generating text by combining external knowledge (databases, documents) with LLM capabilities to ensure accuracy and relevance, with LLMs framed as essential for integrating and synthesizing that knowledge. Applications include generating fact-checked news summaries from verified sources, creating detailed medical reports by integrating patient data and the literature, producing technical documentation by synthesizing API references, generating personalized learning content from educational databases, and creating financial reports by combining market data and analysis. This is effectively the deck's RAG (retrieval-augmented generation) slide under another name, though it does not yet use that term.

## Slide 18 — 16. Text Simplification

Defines simplification as rewriting complex text into simpler, more accessible language while preserving meaning, with LLMs critical for balancing readability and semantic fidelity. Applications include simplifying medical consent forms for patient understanding, rewriting academic articles for high-school resources, adapting technical manuals for non-expert users in DIY apps, simplifying financial reports for retail-investor newsletters, and rewriting legal terms of service for consumer clarity. It is structurally similar to style transfer but with a specific direction ("complex → simple") and an explicit accessibility motivation.

## Slide 19 — 17. Multimodal Text Generation

Defines multimodal text generation as generating text based on inputs from multiple modalities (text, images, or data), with LLMs essential when text generation requires integrating non-textual context. Applications include generating captions for product images in e-commerce listings, creating descriptions for infographics in data journalism, producing narratives for photo slideshows in travel blogs, generating explanations for charts in financial reports, and creating audio narration scripts for video game cutscenes. This is the deck's bridge into vision-language and audio-language models.

## Slide 20 — 18. Emotion Recognition

Defines emotion recognition as identifying specific emotions (joy, anger, sadness) expressed in text beyond a coarse positive/negative sentiment label, with LLMs key for detecting nuanced emotional cues. Applications include detecting frustration in customer-support chats for escalation, identifying joy in social-media posts for brand engagement analysis, recognizing sadness in mental-health-app journals for intervention, detecting anger in employee feedback for HR mediation, and identifying excitement in event reviews for marketing insights. The distinction from text classification is one of granularity: classification often outputs three labels, emotion recognition aims at a richer affective taxonomy.

## Slide 21 — 19. Text-Based Role Playing

Defines text-based role playing as generating interactive, context-aware dialogue or actions as a specific character or persona based on text prompts, with LLMs essential for maintaining character consistency across long conversations. Applications include playing fictional characters in interactive storytelling games, acting as virtual mentors in career coaching apps, simulating customer personas in sales training platforms, role-playing as therapists in mental-health practice tools, and simulating patient scenarios in medical training chatbots. This is the most uniquely LLM-era task in the list: maintaining a stable persona over an open-ended conversation is hard to imagine being solved by any of the earlier non-LLM approaches.

## Slide 22 — Healthcare Applications (image, visually analyzed)

A two-column infographic that pivots from the per-task catalogue to a *per-domain* view. The image is split into two card grids on a dark blue background. The **left column ("For medical professionals")** contains a grid of icon-labeled cards covering provider-facing use cases: clinical documentation, radiology interpretation, creating discharge summaries, suggesting treatment options, generating clinical notes, second-opinion support, insurance pre-authorization, diagnostic interpretation, summarizing research papers, and medical triage. The **right column ("For patients")** mirrors the same layout with patient-facing use cases: analyzing laboratory results, symptom assessment, disease descriptions, analyzing personal health data, interpreting physician notes, mental-health support, personalized health recommendations, medication adherence, health-risk prediction, and rehabilitation guidance. The slide's pedagogical purpose is to show that the abstract tasks enumerated earlier (NER on clinical notes, knowledge-augmented generation, simplification of consent forms, emotion recognition for mental-health support) collapse onto two very different user populations within a single industry, and the design choices follow from *who is reading the output*.

## Slide 23 — Cybersecurity Applications (image, visually analyzed)

A two-part visual. The **top band** shows nine numbered icon cards, each labeled with a cybersecurity application family enabled by LLMs: (1) Threat Detection and Analysis, (2) Phishing Detection and Response, (3) Incident Response, (4) Security Automation, (5) Cyber Forensics, (6) Chatbots, (7) Penetration Testing, (8) Security Protocols Verification, (9) Security Training and Awareness. The **bottom band** is a tree diagram titled *"Opportunities due to LLMs"* with five branches and three leaves per branch, breaking down concrete techniques inside each opportunity: **Vulnerability Detection & Management** (Code Fuzzing, Protocol Fuzzing, Code Explainability and Analysis); **Content Classification & Enforcement** (Safety Classifiers, Content Moderation, Phishing Detection); **Explainability & Prioritization** (Log Analysis, Policy Violations, Augment / Automate Manual Reviews); **Tackling Data Challenges** (Security Data Augmentation, Foundational Security LLMs, Network Traffic Modeling); and **Mitigating LLM Risks** (LLM Guardrails, Deepfake Detection, Adversarial Example Generation). The last branch is the noteworthy one — it acknowledges that LLMs themselves are part of the attack surface, not only part of the defense.

## Slide 24 — LLM in Software Engineering (image, visually analyzed)

The closing slide. It shows a stylized blue "petal" diagram centered on an "AI" chip, with five labeled petals fanning out to name the five places LLMs land in a software-engineering workflow: **Automated Documentation with GenAI**, **AI Code Generation & Automation**, **AI-Based Testing & Debugging**, **AI-Powered Code Review & Optimization**, and **Synthetic Data Generation for Testing**. The diagram is the visual restatement of slide 14 ("Code Generation") expanded to the full developer lifecycle: not just generating code, but documenting it, testing it, reviewing it, and synthesizing the data needed to evaluate it. This is the natural bookend to the catalogue, returning to the same audience (developers) that the course as a whole is addressed to.

---

## Deck-level takeaway

This is a *catalogue deck*: 2 framing slides, 19 numbered task slides (each with a one-line definition plus five concrete applications), and 3 image-only domain slides at the end. The pedagogical contract is the same on every task slide and is the deck's main rhythm — first define the task, then ground it in five real-world examples that span industries. The progression is also meaningful: it moves from classical NLP tasks that predate LLMs (classification, NER, translation, summarization) through tasks that LLMs simply do better (QA, generation, dialog) to tasks that are essentially LLM-native (code generation, knowledge-augmented generation, multimodal generation, role playing). The closing domain slides re-bundle the catalogue under three vertical lenses — healthcare, cybersecurity, software engineering — and signal that the rest of the course will treat these as recurring vocabularies, not isolated definitions.
