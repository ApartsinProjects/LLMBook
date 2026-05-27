# 1025_ProjectTips — Per-Slide Summary

**Source file:** `1025_ProjectTips.pptx`
**Source folder:** `SlidesPool/1020_LLM_CoursePolicies/`
**Drive link:** https://drive.google.com/file/d/1ImmV46K0PbNM3I35DU7CQCW65MTiU21O/view
**Slide count (exact, via python-pptx):** 8
**Extraction:** Local parse + slide PNG render. Title-only divider slides (1 and 3) were inspected visually to confirm there is no body content beyond the section header.

---

## Slide 1 — Useful Tip for Succeeding in Course Project
Title slide for the deck of project-success tips.

## Slide 2 — Attributes of good technical presentation
A six-attribute table defines criteria for slides. Unambiguous statements admit only one interpretation (positive: "evaluate a two-step process for LLM-based response generation"; negative: "optimize customer service with chatbots"). Complete includes all necessary non-trivial information. Correct uses precise terminology (e.g., distinguish detection from classification). Coherent connects points logically and consistently. Accessible lets a reader understand effortlessly, preferring a few targeted graphs over many unfocused ones. Concise uses short informative bullets and avoids trivial filler. The table is positioned as a checklist for slide preparation.

## Slide 3 — Tips for project presentations
Section divider announcing the five tips that follow.

## Slide 4 — 1. Scope-definition
Argues that defining the proper scope is half the success and lists common pitfalls: too broad, unclear, too complex, or too simple. Recommends separating the applicative motivation from the project scope and problem statement, including data-generation strategies and a research questionnaire. The worked example separates motivation ("automate patient diagnosis") from scope ("compare approaches on data X using metrics Y"). Aligns goals to available data, compute, and pretrained models, and suggests core plus extended scope (evaluate two models, two more if time permits).

## Slide 5 — 2. Review Prior Art
Advocates searching Google Scholar and consulting ChatGPT, surfing references jump-by-jump, refining queries with "survey" or "review", and prioritizing recent and well-cited papers from known institutions. For each paper note the task and how it relates to your task, the models used (and whether you can borrow ideas or code), the datasets (and whether you can reuse them), and how performance is measured (with typical baseline accuracy magnitudes).

## Slide 6 — 3. Choosing the Right Models
Tells students to understand each candidate model's capabilities and limitations across three dimensions: generation, input representation, probability estimation. Other selection criteria are the availability of a foundation or specialized pretrained model, model size (practical to run?), model code availability, and whether the model has a cloud API for inference or fine-tuning.

## Slide 7 — 4. Experiment Planning
Calls for stating the experimental objective (compare and evaluate models), handling data with a strict train/validation/test split with the same test set across models and no leakage (especially when data is synthetic), and sanity-checking everywhere by inspecting samples, intermediate results, and both correct and wrong predictions. Metrics should be end-to-end for the final task and intrinsic for intermediate steps. Hyperparameters and prompts are flagged as a common weakest link that can silently break everything.

## Slide 8 — 5. Final Presentation
Focuses on visual storytelling and warns against breaking the logical chain from motivation through models, experiments, and results. Reminds students to respect the schedule (not too short, not too long) and to keep slides free of long texts and overloaded information in favor of informative visuals.

---

## Deck-level takeaway
The deck is a compact playbook for the course project, structured around a six-criteria slide-quality checklist followed by five sequential tips: get the scope right, do real prior-art review, pick the right model with practical constraints in mind, plan experiments with disciplined data handling and sanity checks, and tell a coherent visual story at the end. The recurring theme is that novelty, methodology, and clean presentation matter at least as much as raw accuracy, and that disciplined preparation at each stage compounds into a successful final delivery.
