# Cycle 3: Engagement, Terminology, Self-Containment

**Scope**: Parts 11-15 (modules 52-78).
**Branch**: v2.0
**Date**: 2026-05-20

This cycle ran three coordinated agents over parts 11-15:

- **Engagement designer (16)** to fix sections that opened with dry definitions or generic boilerplate
- **Terminology keeper (12)** to unify the top variants: `pre-trained` to `pretrained`, `HuggingFace` to `Hugging Face`, `Chain-of-Thought` to lowercase `chain-of-thought` in adjectival use
- **Self-containment verifier (21)** to patch obviously broken `Section X.Y` cross-references caused by chapter renumbering or stale paste-overs

## Engagement edits (opening hook replacements)

Each entry below shows the file, the old dry opener, and the rationale. Max 1 edit per section.

### 1. `part-13-llmops-lifecycle/module-66-reliability-slos-registry/section-66.1.html`

**Section 66.1.1 LLM Failure Taxonomy**

- **Old**: "Effective reliability engineering begins with a precise understanding of how systems fail. LLM application failures fall into two broad categories..."
- **New**: Opens with a concrete scenario: green dashboard, p99 fine, zero errors, yet the support inbox is full of complaints about wrong answers. Sets up the hard-vs-soft-failure distinction with a real-world hook.
- **Rationale**: The original opened with abstract boilerplate. The replacement makes the reader picture the exact failure mode that LLM reliability engineering is trying to solve.

### 2. `part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.9.html`

**Section 73.9.1 LLMs as Recommendation Engines**

- **Old**: "LLMs can serve as recommendation engines by leveraging their world knowledge and reasoning abilities."
- **New**: Opens with a tangible example: telling a friend "I just finished Dune and loved it, but I cannot stand romance subplots" and getting three recommendations in seconds, versus classical collaborative filtering needing thousands of interactions.
- **Rationale**: The original was a one-line generic claim. The replacement makes the cold-start advantage immediately concrete.

### 3. `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html`

**Section 57.4.1 MLPerf Training and Inference Suites**

- **Old**: "MLPerf, managed by MLCommons, is the industry-standard benchmark suite for comparing ML hardware and software performance. It provides reproducible, audited results..."
- **New**: Opens with the problem MLPerf solves: three vendor decks with three different precision modes and batch sizes; MLPerf exists to end the argument with audited rules.
- **Rationale**: The original led with a textbook definition. The replacement frames MLPerf as the resolution to a familiar pain point.

### 4. `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.4.html`

**Section 56.4.1 Safety classifiers**

- **Old**: "Safety classifiers score prompts and responses across harm categories (violent, sexual, hate, self-harm, criminal advice, prompt injection, jailbreak, child safety). They are the inline-policy layer between the LLM and the user."
- **New**: Opens with the stakes: "The fastest way to get fired in production AI is to ship a model that helps a teenager write a suicide note or guides a user through synthesizing fentanyl." Then introduces classifiers as the cheap inline chaperones.
- **Rationale**: Definitional opener replaced with a high-stakes hook that motivates why the topic matters.

### 5. `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.3.html`

**Section 56.3.1 LLM bias benchmarks**

- **Old**: "LLM bias benchmarks measure whether language models prefer stereotypical completions, demonstrate disparate behavior across protected attributes..."
- **New**: Opens with the WinoBias canonical probe: "the doctor told the nurse that she had to go home; who needed to leave?" and invites the reader to predict where the model lands.
- **Rationale**: Replaces dry abstract definition with a probe the reader can run mentally in three seconds.

### 6. `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.2.html`

**Section 56.2.1 Fairness metric and mitigation libraries**

- **Old**: "Fairness libraries compute group-disparity statistics..."
- **New**: Opens with "Run the same dataset through AIF360 and Fairlearn and you may get disparate-impact ratios that disagree at the third decimal. The third decimal is where the lawsuit lives."
- **Rationale**: Ties the dry definition to the surprising legal consequence; matches the section's existing epigraph theme.

## Terminology unifications

Canonical choices (per skill guidance): `pretraining` (one word), `pretrained` (no hyphen), `Hugging Face` (two words), `chain-of-thought` lowercase in adjectival use. Per-section dominant variants checked first.

### `pre-trained` to `pretrained`

| File | Context |
| --- | --- |
| `part-11/module-55/section-55.2.html` | `<h3>` heading "Reusing Pre-Trained Models..." and body "Using a pre-trained foundation model..." |
| `part-11/module-55/section-55.3.html` | Green-AI checklist bullet "an existing pre-trained model" |
| `part-15/module-76/section-76.3.html` | SAELens library shortcut "pre-trained SAEs" |
| `part-15/module-75/section-75.3.html` | "For pre-trained Mamba models, use Hugging Face Transformers" |
| `part-15/module-75/section-75.4.html` | Kronos description "pre-trained autoregressively" |

Skipped:
- Paper title in `part-12/module-61/section-61.5.html` bibliography (`"...LLM pre-training."`) — citation title, leave verbatim.

### `HuggingFace` to `Hugging Face`

| File | Context |
| --- | --- |
| `part-15/module-75/section-75.4.html` | Code-block comment "via HuggingFace" (line 315) and caption "via HuggingFace" (line 329) |
| `part-15/module-75/index.html` | Lab steps "from HuggingFace" |
| `part-15/module-78/index.html` | Bibliography note "The HuggingFace transformers paper" |
| `part-12/module-61/section-61.5.html` | Bibliography author "HuggingFace (2024)" for nanotron |

Skipped:
- Url path fragments like `HuggingFaceH4`, `HuggingFaceTB` (these are official org handles on the platform, not prose).
- A bibliography title `"HuggingFace Hub: Models, Adapters, and Datasets."` (quoted document title).
- A `title=""` tooltip on a concept link in `section-65.4.html` (deliberate kebab id reference).

### `Chain-of-Thought` to `chain-of-thought`

| File | Context |
| --- | --- |
| `part-15/module-76/section-76.1.html` | Key-takeaway bullet "Chain-of-Thought prompting" (adjectival, now lowercase) |

Skipped:
- Bibliography titles where the paper itself is titled with `Chain-of-Thought` (e.g., Wei et al. and Feng et al.) — title case in proper titles is correct.
- H2 heading "Chain-of-Thought as Emergent Computation" — heading title case is acceptable per guidance.

## Self-containment / cross-reference fixes

Patched obviously broken `Section X.Y` references caused by chapter renumbering (76.5-76.9 to 76.1-76.4) and stale paste-overs from earlier draft numbering (Section 32.X to actual Chapter 33).

| File | Fix |
| --- | --- |
| `part-15/module-76/section-76.2.html` | Removed duplicate "Section 76.7" stale paragraph; kept the linked 76.3 reference. |
| `part-15/module-76/section-76.3.html` | Removed duplicate "Section 76.8" stale paragraph; kept the linked 76.4 reference. Also linked "Section 76.5" in cross-ref bullet to the correct `section-76.1.html`. |
| `part-15/module-76/section-76.4.html` | Three fixes: (a) "memory systems from Section 76.6" to linked `section-76.2.html`; (b) "discussed in Section 76.5" to linked `section-76.1.html`; (c) "interpretability tools from Section 76.7" to linked `section-76.3.html`; (d) replaced stale "Section 76.9" paragraph with a clean handoff to Section 77.1. |
| `part-14/module-73/section-73.10.html` | "Section 32.7" to "Chapter 33" (link was already to module-33). |
| `part-14/module-73/section-73.7.html` | "Section 32.6" to "Chapter 33". |
| `part-14/module-73/section-73.5.html` | "Section 32.8 (Robotics...)" to "Chapter 24 (Robotics...)" — link was to module-24-vla-models. |
| `part-14/module-73/section-73.4.html` | "Section 32.7" inline to "Chapter 33 on cross-modal reasoning". |
| `part-14/module-73/section-73.6.html` | "Section 32.6" in prerequisites to "Chapter 33". |
| `part-14/module-73/section-73.8.html` | "Section 32.7" in prerequisites to "Chapter 33". |
| `part-14/module-73/section-73.9.html` | Removed stale "Section 75.5: Cybersecurity & LLMs" what-comes-next paragraph; clean handoff to Section 73.10. |
| `part-11/module-54b/section-54.9.html` | "Section 57.5 closes the chapter..." to linked `section-54.10.html` and corrected Part XIII to Part XV. |
| `part-15/module-76/section-76.2.html` | Prerequisites text "reasoning in Section 76.5" to linked `Section 76.1`. |
| `part-15/module-75/section-75.3.html` | Exercise text "implicit cross-entropy theory from Section 7.7" to linked `Section 6.7`. |
| `part-13/module-66/section-66.2.html` | "Section 44.1.3 above" now wraps the existing in-page anchor `#44-1-3-wandb-aliases-and-promotion`. |

Not addressed (out of scope for this conservative pass):
- Stale meta-description and `<title>` tags in `section-76.2.html`, `section-76.3.html`, `section-76.4.html`, `section-75.4.html` (still say e.g. "Section 76.8" in the `<head>`). These are not user-facing in the body. A renumbering pass should cover them.

## Summary

- **Sections touched**: 20 (6 engagement, 7 terminology, 14 cross-reference, with overlap when a section had multiple fixes)
- **Edits applied**: 28
- **Audit verification**: rebuilt the broken-`Section X.Y`-in-body scan after edits. Started at 22 unique broken body references across parts 11-15; ended at 0 navigation-breaking ones (the last remaining "Section 44.1.3" string is a self-reference now wrapping the existing in-page anchor).
- **Net effect**: cleaner openers in six sections, consistent pretraining / Hugging Face / chain-of-thought usage in seven sections, and 14 cross-references that previously resolved nowhere either correctly link to the renamed target or got their stale duplicate prose stripped.
- **Constraints honored**: no em dashes, no double dashes, no new content beyond opener replacements, conservative on terminology (skipped code identifiers, paper titles, and other proper nouns).
