# 1141_FM_Intro — Per-Slide Summary

**Source file:** `1141_FM_Intro.pptx`
**Source folder:** `SlidesPool/1140_LLM_HuggingFace/`
**Drive link:** https://drive.google.com/file/d/1xy8FI0Kn5TjLPA-bg5lvkcmufVrvawyA/view
**Slide count (exact, via python-pptx):** 7
**Extraction:** Local parse + slide PNG render. The deck is short and each slide has clear body text plus a single supporting diagram.

---

## Slide 1 — Foundation Models
Title slide framing the introduction to foundation models.

## Slide 2 — Foundation Model
Contrasts traditional ML (one model per task, e.g., M1 for face recognition and M2 for car recognition) with foundation models (a single model serving many downstream tasks after being trained on a massive amount of data). Two types are called out: representation models and generative models.

## Slide 3 — Adapting FM for downstream tasks
Method 1, Composition: keep the FM frozen as a representation extractor and train a task-specific head (for example, a classification head) on top. Other adapter placements are also possible: preprocessor, head, or intermediate layers.

## Slide 4 — Adapting FM for downstream tasks (image)
Method 2, Fine-Tuning: change the FM weights to match the specific task through partial and incremental training of the large model. There are many ways to fine-tune efficiently given limited data; this slide illustrates the image case.

## Slide 5 — Adapting FM for downstream tasks (LLM)
The same Method 2, Fine-Tuning, illustrated for an LLM. The figure shows the layered LLM with selected weights being updated rather than the full stack.

## Slide 6 — Adapting FM for downstream data (LLM)
Method 3, Prompting / In-context Learning: no training or fine-tuning at all; the practitioner prepares a task-specific input for the generative FM (text prompt, augmented input, in-context examples) and reads the output.

## Slide 7 — Adapting FM for downstream data (Image)
Method 3 in the image setting, In-Context / Zero-Shot Learning: represent inputs and class prototypes (or class labels) using a pretrained model, then classify by similarity. No additional training is required.

---

## Deck-level takeaway
A compact seven-slide primer on foundation models that defines them as task-agnostic models trained at massive scale and contrasts them with the older one-model-per-task setup. The three downstream-adaptation strategies are laid out side-by-side: compose a frozen FM with a task-specific head, fine-tune (partial or full) the FM weights for the new task, or use prompting and in-context learning with no training. The latter two are shown in both the language and the image setting to underscore that the recipe is modality-agnostic.
