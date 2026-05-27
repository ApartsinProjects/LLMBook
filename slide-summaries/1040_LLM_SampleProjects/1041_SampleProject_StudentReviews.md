# 1041_SampleProject_StudentReviews — Per-Slide Summary

**Source file:** `1041_SampleProject_StudentReviews.pptx`
**Source folder:** `SlidesPool/1040_LLM_SampleProjects/`
**Drive link:** https://drive.google.com/file/d/1E2yOpduNn2NZ51OlDQVmUcF9lR6nKLgp/view
**Slide count (exact, via python-pptx):** 36
**Extraction:** Local parse + slide PNG render. The deck is dominated by code-screenshot slides; representative slides (4, 6, 10, 14, 26) were inspected visually to confirm code intent and table content, and several other image-only slides were scanned to confirm they continue the same code thread.

---

## Slide 1 — Project Example
Title slide announcing the worked end-to-end project example.

## Slide 2 — Motivation
The project frames departmental course-quality evaluation as an ML task: collect student reviews of CS courses, classify each review as positive or negative, and use the positive ratio as the course score. The challenge is that no public labeled dataset of student reviews exists for CS courses, so the project scope is to generate a synthetic dataset and evaluate several classification approaches on it.

## Slide 3 — Part 1: Data Preparation
Section divider introducing the data-generation half of the project.

## Slide 4 — Step 1: Generate fictitious courses
Visual inspection shows a Python code screenshot that builds a prompt asking GPT to return a list of fictitious CS courses as JSON with course_id, title, description, and lecturer_name. It calls the OpenAI client.chat.completions.create endpoint, parses the JSON response, and saves to course_data with json.dump.

## Slide 5 — Courses
A screenshot of the generated course catalog as a Python dict, listing fictitious entries like CS101, CS499, etc., each with title, description, and lecturer name.

## Slide 6 — Step 2: Generate a review batch
Visual inspection shows a Python function generate_review(course_info, sentiment, num_variants=8, temperature=0.7, prompt=prompt) that prompts GPT to produce short student reviews for a given course title, lecturer, and target sentiment. Returns list comprehension over response.choices.

## Slide 7 — Review Batch
Shows the output of the generation: a list of synthetic reviews. The captioned problems are that the reviews are too unnatural and lack diversity.

## Slide 8 — Debugging the generation function
Two screenshots illustrate the first debugging attempt: fine-tune the prompt and raise temperature. The annotation notes the reviews are still not very diverse.

## Slide 9 — Generate one-by-one
Two screenshots show generating reviews one at a time rather than in a batch. Still not diverse enough.

## Slide 10 — Generate review styles and attributes
Visual inspection shows a Python function generate_attributes(course_info, prompt) that asks GPT for five possible style and tone attributes (excluding sentiment polarity), returned as a JSON object of attribute name to value list. The output is a structured set of stylistic axes that downstream prompts will sample from.

## Slide 11 — Results
Screenshot of the diversified review batch produced after introducing style attributes; visibly more varied wording than earlier batches.

## Slide 12 — Generate Attribute Prompt
Screenshot of the prompt template used to generate per-course attribute sets, with the caption that students can edit or validate the attributes manually when the number of courses is small.

## Slide 13 — Generate with attributes
Code screenshot that combines a course, a sentiment, a random attribute combination, and the style prompt to generate one variant review.

## Slide 14 — Dataset Generation
Visual inspection shows the orchestration function generate_dataset(course_data, num_per_course=10) that loops over courses, samples sentiment, calls generate_attributes and generate_review per item, and assembles a pandas DataFrame with columns review, course_id, sentiment. The bottom of the slide previews five rows of the resulting frame.

## Slide 15 — Train-Test Split
Screenshot of a train_test_split call separating the generated DataFrame into training and test splits, stratified by sentiment.

## Slide 16 — Benchmarking Models
Section divider for the modeling half of the project.

## Slide 17 — BERT Classifier
Subsection divider announcing the fine-tuned BERT baseline.

## Slide 18 — Prepare Data
Screenshot of dataset construction code wrapping the DataFrame in a HuggingFace Dataset (or similar) and mapping sentiment strings to integer labels.

## Slide 19 — Load Models
Screenshot of HuggingFace transformers loading code: AutoTokenizer.from_pretrained and AutoModelForSequenceClassification.from_pretrained with a checkpoint such as bert-base-uncased and num_labels=2.

## Slide 20 — Tokenize Data
Two screenshots show batched tokenization via dataset.map applied to train and test splits, with padding and truncation arguments.

## Slide 21 — Prepare Trainers
Two screenshots show TrainingArguments and Trainer construction from transformers: output directory, learning rate, batch size, num_train_epochs, evaluation strategy, plus the Trainer assembled with model, args, train_dataset, eval_dataset, and compute_metrics.

## Slide 22 — Train Model
Two screenshots show trainer.train() being called, with the loss curve and evaluation metrics printed to the cell output.

## Slide 23 — Zero-Shot Classifier
Screenshot of a HuggingFace pipeline("zero-shot-classification") call applied to a review with the candidate labels ["positive", "negative"], serving as a no-fine-tuning baseline.

## Slide 24 — Discussion
Notes the next steps for a real project: more data (hundreds to thousands of examples with EDA on length and distribution by type and course, and how much was filtered out); more models with different training strategies and longer training; richer evaluation with multiple models, tables, and graphs; and insight work characterizing what kinds of reviews get misclassified (by course, type, attribute).

## Slide 25 — What about novelty?
Two screenshots that pivot the project toward a novel framing: rather than binary sentiment, the project will move to fine-grained aspect extraction.

## Slide 26 — Aspect-Oriented Sentiment Analysis
Visual inspection shows a ChatGPT response listing ten course-quality aspects with definitions: instructor effectiveness, course content quality, organization and structure, assessment and grading, learning resources and materials, workload and difficulty, student engagement and interaction, plus three more (recommendation, prerequisite alignment, overall satisfaction). These become the K labels for the multilabel problem.

## Slide 27 — Reframing Project
The new framing: fine-grained extraction of K aspects (content, organization, difficulty, quality, time, etc.) per review, framed as multilabel classification predicting a vector of K scores in [-1, 1] where zero means neutral or not mentioned. An alternative two-output framing (presence + score) is mentioned. Project scope becomes conditional synthetic data generation.

## Slide 28 — Extract into JSON
Screenshot of a prompt asking GPT to extract aspect scores into a JSON object keyed by aspect name with numeric values.

## Slide 29 — Generate prompt
Screenshot of a generation prompt that, given a course and a target aspect-score vector, produces a synthetic review consistent with those scores.

## Slide 30 — Generate Training Data
Screenshot of a loop that samples aspect-score vectors, calls the generation prompt, and assembles a labeled dataset suitable for multilabel regression.

## Slide 31 — More Ideas
Lists extension ideas: use the LLM to filter out bad examples (offensive, unhelpful, unnatural); use the LLM to augment, including translation into Hebrew; solve adjacent tasks like text generation, question answering, recommendation, token classification, and named-entity recognition. Many creative directions remain open.

## Slide 32 — Evaluation is critical!
Argues that best-effort projects are hobby projects; professional projects come with quality estimation. Recommends measuring intermediate-step metrics and end-to-end quality metrics, drawn from the broader world of metrics for different tasks and aspects of performance.

## Slide 33 — Language Interfaces
Section divider announcing the survey of LLM-serving interfaces the project can call.

## Slide 34 — OpenAI
Screenshot of OpenAI client setup: import openai, client = OpenAI(api_key=...), client.chat.completions.create with a model name.

## Slide 35 — Ollama local server
Screenshot showing how to point the same OpenAI-style client at a local Ollama server (base_url set to localhost), allowing local LLM inference with the familiar API.

## Slide 36 — HuggingFace
Screenshot of HuggingFace text-generation code: AutoModelForCausalLM.from_pretrained plus pipeline("text-generation") or model.generate, as the third inference route.

---

## Deck-level takeaway
This deck walks the reader through a full end-to-end LLM-for-NLP project in two arcs. The first arc generates a synthetic labeled dataset of student course reviews, starting from a naive batch prompt that produces unnatural and repetitive text, and iterating through three diversification fixes (prompt tuning and higher temperature, one-by-one generation, and finally per-course style and tone attributes) until the data is usable. The second arc benchmarks two classifiers (fine-tuned BERT and a zero-shot pipeline) on the synthetic data and then reframes the project from binary sentiment to fine-grained aspect-based scoring of about ten course-quality aspects, with conditional synthetic data generation now driven by target aspect-score vectors. The closing slides recap the importance of disciplined evaluation and survey three interchangeable LLM-serving interfaces (OpenAI, Ollama, HuggingFace) the team can use to power both data generation and inference.
