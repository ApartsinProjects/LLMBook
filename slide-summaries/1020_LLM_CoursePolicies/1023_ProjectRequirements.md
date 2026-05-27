# 1023_ProjectRequirements — Per-Slide Summary

**Source file:** `1023_ProjectRequirements.pptx`
**Source folder:** `SlidesPool/1020_LLM_CoursePolicies/`
**Drive link:** https://drive.google.com/file/d/13h9I41Qtl9HpSZaqqWv0KT_UjVy0ucTc/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render. Slides 7, 8, 9, and 11 were inspected visually because their text bodies were empty in python-pptx output yet they carry the bulk of the lecture's structural content.

---

## Slide 1 — Course Project Requirements
Title slide announcing the topic of templates and requirements for the course project.

## Slide 2 — Course Project
The slide defines the project mandate: solve a task with an LLM or GenAI method that is both novel and relevant. It suggests targeting a task that has no available data, generating synthetic training and test data, and then comparing several methods (a mix of fine-tuned models and off-the-shelf models) once the data exists.

## Slide 3 — Project Example (LLM Course)
A worked example for aspect-based sentiment analysis of student course reviews along axes such as "interesting", "challenging", and "useful". The input is review text, the output is binary labels plus scores for non-zero aspects, evaluated with micro and macro precision. The proposed scope is to generate a large labeled dataset via attribute-based generation with GPT-4o and to compare pretrained GPT, a fine-tuned SBERT, and a fine-tuned Phi-3.

## Slide 4 — Project Example: GenAI course
A second worked example, this time for a veterinary clinic that needs to recognize dog breeds. The task takes a dog image and returns one of 150 breed labels, scored by accuracy. The scope is to design data-generation strategies based on Stable-Diffusion variants and compare three pretrained classifiers (CNN, ViT, VLM) after fine-tuning on the synthetic data.

## Slide 5 — In-class Project Presentation
Lists the three checkpoint deliverables: a Week 5 proposal (problem definition), a Week 9 interim report (data generation, EDA, baseline), and a Week 13 final report (self-contained presentation). End-of-semester plus two weeks the team submits the GitHub repo with code, slides, README, visuals, and data.

## Slide 6 — Presentation Templates
A short bridge slide indicating that the next slides give templates that students should adapt by adding their own information, specifics, and additional slides.

## Slide 7 — 1. Proposal slides
Visual inspection shows a six-card outline for the proposal deck. The cards are: motivating use case (background, why the problem matters, why it is hard, how it is solved today), project task description (problem statement, inputs and outputs, today's tools), models and methods (processing flow, model and technique types per step, adjustments per step, how each is applied), data specification and generation (training and evaluation requirements, the dataset, labeling, augmentation), and metrics and KPIs (how to measure results, quality measurements per step, measurement protocols, ground-truth data).

## Slide 8 — 2 Interim Presentation
Visual inspection reveals a five-card layout for the interim deck. The cards cover project review (motivation summary, what changed from the proposal, claimed novelty), previous work (review at least three recent and high-citation scientific papers, organized in a table with title and year, task, methods, data, results, and relation to the project), dataset (description of the dataset created or labeled, the data generation or labeling technique, EDA on labels and inputs including class distribution, length, and types), baseline solution and results (a pretrained model with minimal modifications, results shown as graphs and tables, error inspection), and plan (project steps, scope, due dates, expected outcomes, with the last step being preparation of the final presentation).

## Slide 9 — 3. Final Presentation
Visual inspection shows a five-card outline for the final deck. The cards request review and refinement of the project definition (short motivation, review of models, data, and metrics), project achievements and novelty, review methodology (what was done, prepared data, models trained, metrics, quality-assurance effort), results (tables and graphs with digestible labels, axes, colors, and visualization types), and a conclusion (whether the desired results were achieved, lessons learned, and future experiments).

## Slide 10 — GitHub repository: Requirements
The slide spells out the expected GitHub layout: a meaningful repository name, folders for slides (PPT and PDF), code (Python files and notebooks), data (images and texts, JSON and CSV metadata), results (CSV or JSON experiment outputs), and visuals (result figures and a visual abstract), plus a README file.

## Slide 11 — GitHub Repo ReadMe File: Sections
Visual inspection shows a twelve-tile grid of README sections: project motivation, problem statement, visual abstract, datasets used or collected, data augmentation and generation methods, input/output examples, models and pipelines used, training process and parameters, metrics, results, repository structure, and team members.

---

## Deck-level takeaway
This deck is the operational rubric for the LLM course capstone project. It defines what counts as an acceptable project (a novel and relevant LLM/GenAI task, often one with no existing data, attacked by generating synthetic data and comparing several models), walks through two concrete examples (aspect-based course-review sentiment, dog-breed recognition), and then pins down the three graded artifacts (proposal, interim, final) plus the deliverable GitHub repo. Slides 7 through 9 and 11 are essentially template specifications, listing the exact cards each presentation must contain and the exact README sections, so students can reuse the structure verbatim.
