# 1204_PromptEngineering — Per-Slide Summary

**Source file:** `1204_PromptEngineering.pptx`
**Source folder:** `SlidesPool/1200_LLM_LanguageFM/`
**Drive link:** https://drive.google.com/file/d/1BN1km8fsB37_EXHPLFQ3w9IuiB_YsQyu/view
**Slide count (exact, via python-pptx):** 35
**Extraction:** Local parse + slide PNG render. Most slides are code or example screenshots that operationalize a small number of well-defined prompt-engineering recipes captured in the titles and short bullets.

---

## Slide 1 — Prompt Engineering
Title slide for the deck on prompt engineering.

## Slide 2 — Prompt Engineering: meaning
Prompt format has a critical impact on model performance, and the right format depends on the model and its training data and method. The deck addresses how to give unambiguous, complete, and precise instructions, how to split tasks into subtasks via prompting strategies, and how to apply best practices, framing the LLM as a "universal function" inside a larger software system.

## Slide 3 — Prompt formats and content
Section divider for prompt formats and content.

## Slide 4 — Prompts for text classification: T5
Four screenshots of T5-style task-prefix prompts for text classification ("classify the sentiment of: ...").

## Slide 5 — Prompt for Text Classification: OpenAI
Five screenshots of OpenAI-style classification prompts, illustrating system-role plus user-role formatting.

## Slide 6 — Composition Prompts
Common prompt sections (role/persona, task description, context, format spec, examples, the actual input) composed into a single prompt.

## Slide 7 — Prompt templates for NLP tasks
Two screenshots showing prompt templates for canonical NLP tasks (classification, summarization, extraction, translation).

## Slide 8 — Mother prompt template
Two screenshots showing a "mother" template that consolidates the sections from slide 6 into a single reusable scaffold.

## Slide 9 — Iterative Prompt Refinement
Three screenshots illustrating the iterate-identify-improve loop: run the prompt, identify failure modes in outputs, and refine the prompt accordingly.

## Slide 10 — Modular prompt construction
A screenshot showing modular prompt construction where the prompt is assembled from independent named components.

## Slide 11 — In Context Learning
Provide examples directly in the prompt; no need to train or fine-tune the model.

## Slide 12 — Inject examples into chat history
Three screenshots showing how to inject prior examples into a chat history (as alternating user/assistant turns) instead of cramming them into a single message.

## Slide 13 — Checklist for Good Prompts
Section divider introducing a checklist of prompt-quality criteria.

## Slide 14 — Prompt self-critique and self-repair using ChatGPT
Three screenshots showing prompts that ask ChatGPT to critique and rewrite a previously suggested prompt.

## Slide 15 — Prompting isn't easy
A cautionary illustration that prompt engineering is non-trivial and benefits from systematic methods.

## Slide 16 — Prompt-based flows
Section divider for the next subsection on prompt-orchestrated flows.

## Slide 17 — Multistep Generation
Three screenshots illustrating multistep generation: the output of one prompt feeds the input of the next.

## Slide 18 — LangChain
LangChain is a popular library for building LLM-based applications by representing NLP pipelines as chains of calls to modules. It ships a rich library of modules (preprocessing, LLMs, etc.) where the output of the previous module is typically the input to the next.

## Slide 19 — LangChain
A second LangChain slide describes the core abstractions: PromptTemplate module (init with template, input variables, output prompt); LLM module (input prompt, output generated text). Modules are chained together; LLMChain is a common shorthand for prompt-then-LLM.

## Slide 20 — Reminder: Phi-3 Prompt Template
Screenshot showing the Phi-3 chat prompt template used by the LangChain example.

## Slide 21 — LangChain: Generate a story
Six screenshots walking through a LangChain story-generation chain expressed in LCEL (LangChain Expression Language).

## Slide 22 — Few-Shot Chain-Of-Thought Prompt
Asking the model to explain its reasoning often improves the final answer. Inject examples that contain the reasoning steps so the model imitates the explain-then-answer pattern.

## Slide 23 — Zero-Shot CoT Prompt
Just ask the model to think step-by-step; no examples needed.

## Slide 24 — Self-Consistency Prompting
Generate several versions (with higher temperature) and decide on the final answer by majority vote across the samples.

## Slide 25 — Tree-of-Thought
Break the problem into steps, explore different solutions for each step, and ask the LLM to decide on the best solution.

## Slide 26 — Constrained Text Generation Output
Section divider for the constrained-output subsection.

## Slide 27 — Constrained Output: Use Cases
Sometimes outputs must follow a specific format: specific JSON, Python code, CSV with specified columns, or XML-based formats. The two enforcement methods are prompt engineering (ask for the format) and constrained sampling (restrict allowed tokens during decoding).

## Slide 28 — Format specification in prompt
Four screenshots showing format-specification prompts that ask for output in a specific JSON or list format.

## Slide 29 — Constrained sampling
Constrained sampling restricts the set of allowed next tokens at each step according to a specified format. Examples include enumerated classification labels and Abstract Syntax Trees (AST) for code generation.

## Slide 30 — Prompt optimization with DSPy
Section divider for DSPy (pronounced "dee-es-pie").

## Slide 31 — DSPy: Declarative Prompting
DSPy motivates programming and fine-tuning prompts automatically rather than hand-crafting them. The core abstraction is a task signature, a declarative specification for a text-generation task (for example, "article -> type") expressed via a Signature class. A prompt compiler turns declarations into actual prompts; a Teleprompter finds the best prompt given examples and an evaluation, using an LLM for prompt modification and trial-and-error.

## Slide 32 — DSPy: Text-based task signatures
Three screenshots showing DSPy's Predict primitive, a basic input-to-output mapper, with the Signature class instantiated from a text string using the "->" syntax.

## Slide 33 — DSPy: Custom Task Signature Class
Two screenshots showing a custom Signature class where the class docstring describes the task and becomes part of the compiled prompt.

## Slide 34 — DSPy: Custom Generation Task with few-shot prompt
Screenshot of a DSPy generation task wired to use few-shot examples.

## Slide 35 — DSPy: Teleprompter for prompt optimization
Four screenshots showing the BootstrapFewShot Teleprompter selecting the best examples to include in a few-shot prompt to maximize evaluation score.

---

## Deck-level takeaway
The deck is a tour of prompt engineering at three depths: format and content (composition, templates, mother templates, modular construction), reasoning and orchestration (in-context learning, chain-of-thought in zero-shot and few-shot variants, self-consistency, tree-of-thought, multistep generation, LangChain chains), and quality-control engineering (constrained output via prompt or constrained sampling, and DSPy's declarative signatures with automatic prompt optimization via Teleprompter). The unifying message is that prompts are software artifacts that benefit from modular construction, iterative refinement, and tooling rather than ad hoc text editing, with LangChain and DSPy positioned as the two ecosystems supporting that engineering mindset.
