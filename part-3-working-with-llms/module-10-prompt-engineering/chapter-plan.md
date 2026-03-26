# Chapter Plan: Module 10 - Prompt Engineering & Advanced Techniques

## Scope

**What this chapter covers:** Prompt engineering as a systematic discipline, from foundational techniques through advanced reasoning strategies to automated optimization. Specifically: zero-shot, one-shot, and few-shot prompting; system prompt design and role assignment; prompt templates and variable injection; Chain-of-Thought (CoT) prompting and its variants; self-consistency with majority voting; Tree-of-Thought (ToT) for structured exploration; step-back prompting; the ReAct framework for interleaving reasoning with tool use; self-reflection and iterative refinement loops; meta-prompting; prompt chaining and decomposition; programmatic prompt optimization with DSPy and OPRO; prompt injection attacks and defense strategies; prompt compression; and prompt testing, versioning, and regression testing.

**What this chapter does NOT cover:** API mechanics (Module 09), RAG-specific prompting (Module 19), agent-specific prompt patterns (Module 21), fine-tuning as an alternative to prompting (Module 13), or model alignment (Module 16). Structured output via Instructor/Pydantic is briefly revisited in 10.4 for security context but is primarily covered in Module 09.2.

**Target audience:** Practitioners who have basic API fluency (Module 09) and want to systematically improve the quality, reliability, and security of their LLM interactions. Both beginners (Sections 10.1, 10.2) and intermediate users (10.3, 10.4) will find actionable material.

**Target length:** ~12,000 to 15,000 words across four sections.

---

## Learning Objectives

1. Design effective zero-shot, few-shot, and role-based prompts with measurable quality improvements.
2. Construct system prompts and prompt templates with variable injection for production applications.
3. Implement Chain-of-Thought, self-consistency, and Tree-of-Thought reasoning strategies.
4. Apply the ReAct framework to interleave reasoning with external tool use.
5. Build self-reflection and iterative refinement loops that improve output quality across multiple passes.
6. Use meta-prompting and prompt chaining to decompose complex tasks into manageable sub-tasks.
7. Identify and defend against prompt injection attacks (direct, indirect, and jailbreak variants).
8. Enforce structured output with JSON mode, Pydantic models, and the Instructor library.
9. Apply automated prompt optimization using DSPy and OPRO.
10. Design prompt testing suites with regression tests, A/B experiments, and version control.

---

## Prerequisites

- Module 05: Decoding Strategies (temperature, sampling, how generation works)
- Module 09: Working with LLM APIs (API calls, message formats, parameter tuning)
- Basic Python programming and familiarity with the OpenAI or Anthropic client libraries
- Conceptual understanding of how transformer models process and generate text

---

## Current Content Assessment

### Section 10.1: Foundational Prompt Design (~3,500 words)

**Strengths:**
- Clear anatomy-of-a-prompt diagram (Figure 10.1) mapping structural components to chat API message roles
- Excellent progression: prompt anatomy, zero-shot, few-shot, system prompts, templates, edge cases, iterative refinement
- The specificity principle is well demonstrated with before/after examples
- Few-shot entity extraction example with JSONL output is realistic and production-relevant
- System prompt architecture diagram (Figure 10.2) showing layered structure with attention weight guidance
- Prompt template system with variable injection code is practical and reusable
- Edge cases section addresses hallucinations, refusals, and verbosity with concrete mitigation strategies
- Iterative refinement workflow section provides a reproducible methodology
- Template injection warning is timely and connects to Section 10.4
- 5 quiz questions covering practical decisions

**Weaknesses / Improvement Opportunities:**
- The few-shot example selection criteria could be expanded. The text mentions choosing diverse examples but does not discuss strategies for selecting maximally informative examples (e.g., covering edge cases, choosing examples near decision boundaries).
- Missing: a quantitative comparison showing accuracy improvements from zero-shot to few-shot. The iterative refinement section mentions going from 72% to 93% but does not show the measurement methodology.
- The system prompt architecture section describes a layered approach but does not provide a complete system prompt example that combines all layers. Adding a full production system prompt (identity, context, rules, format, examples) would be a strong reference artifact.
- Missing: any mention of prompt length limits or the impact of long prompts on attention. A brief note connecting to the context window concept from Module 04 would help.
- The template system does not mention Jinja2 or any standard templating library, relying only on Python f-strings. A brief note about Jinja2 for complex templates would be practical.

**Structural Issues:**
- CSS and heading structure are consistent with other sections.
- Navigation links are correct.

---

### Section 10.2: Chain-of-Thought & Reasoning Techniques (~3,000 words)

**Strengths:**
- Big Picture callout clearly motivates why reasoning techniques matter
- CoT explanation is grounded in mechanism: generated text as a scratchpad that carries information forward
- Zero-shot CoT with GSM8K accuracy numbers (17.7% to 78.7%) provides compelling evidence
- Working code example for zero-shot CoT with a multi-step math problem and expected output
- Key Insight callout on when CoT helps vs. when it adds unnecessary tokens is excellent guidance
- Direct vs. CoT prompting comparison diagram (Figure 10.3) is clear
- Self-consistency implementation with majority voting and temperature > 0 is well explained
- Tree-of-Thought implementation with evaluation and pruning is a simplified but functional demonstration
- ReAct framework with a working search-tool loop shows the full Thought/Action/Observation pattern
- Comparison table of reasoning techniques (CoT, self-consistency, ToT, step-back, ReAct) covering complexity, cost, and best use cases
- Cost awareness callout for multi-call techniques
- 5 quiz questions testing understanding of mechanism, not just recall

**Weaknesses / Improvement Opportunities:**
- The few-shot CoT subsection (1.2) describes the concept but does not provide a complete code example with exemplars. Adding a concrete few-shot CoT example (2 to 3 exemplars followed by the test problem) would complete the picture.
- Step-back prompting (Section 4) is very brief (one paragraph). Either expand it with a code example or merge it into the CoT section as a variant.
- The ToT implementation is simplified but does not show backtracking. Adding a brief example where a branch is pruned and exploration resumes from a previous node would demonstrate the key advantage of ToT over self-consistency.
- Missing: any mention of when reasoning techniques fail or produce worse results. The Key Insight partially addresses this, but a concrete example (e.g., CoT on a simple classification task producing lower accuracy) would reinforce the point.
- The ReAct implementation hardcodes a Wikipedia search tool. A note about generalizing to other tools with a pointer to Module 21 would improve cross-module coherence.

**Structural Issues:**
- This is the shortest section in the module (621 lines). The density is appropriate, but some topics (step-back prompting) feel rushed.
- Navigation links are correct.

---

### Section 10.3: Advanced Prompt Patterns (~3,500 words)

**Strengths:**
- Big Picture callout positions this section as the transition from manual craft to automated optimization
- Reflection loop is thoroughly covered: basic loop, Reflexion with memory, and guidance on when reflection helps vs. wastes compute
- The generate-critique-revise code example is production-quality with configurable rounds and history tracking
- Reflection loop SVG diagram (Figure 10.5) is clear and well labeled
- Reflexion (memory-augmented) explanation differentiates it from basic reflection by adding persistent memory across attempts
- Meta-prompting section provides a working prompt-generator that creates task-specific prompts
- Prompt chaining diagram (Figure 10.6) with cost annotations showing cheaper models for simple stages is practical
- DSPy coverage includes both core concepts (signatures, modules) and optimization (BootstrapFewShot, MIPROv2)
- OPRO explanation with iteration diagram (Figure 10.7) showing prompt-score history is clear
- Comparison table of optimization approaches (manual, DSPy, APE, OPRO) covering effort, cost, and best use cases
- 5 quiz questions targeting practical decision-making

**Weaknesses / Improvement Opportunities:**
- The when-reflection-helps table is good, but a quantitative example would strengthen it. Showing a pass@1 metric improving from X% to Y% with reflection on a coding task would make the guidance concrete.
- DSPy code example uses v2 syntax but does not mention version requirements. A brief note on installation and version compatibility would prevent reader frustration.
- The APE section (5.1) is very brief (two sentences). Either expand with a code example or remove the standalone heading and merge it into the OPRO comparison.
- Missing: any discussion of how prompt chaining interacts with context windows. When the output of one stage is passed as input to the next, total token usage can grow rapidly. A note on managing context across chains would be practical.
- Constitutional AI-style self-checks are mentioned in the index description but receive only a brief mention in the reflection section. A more explicit treatment with a code snippet showing a constitutional check (evaluate against a set of principles) would fulfill the index promise.
- The meta-prompting example generates a prompt for sentiment analysis but does not show how to evaluate the generated prompt. Closing the loop with evaluation would demonstrate the full workflow.

**Structural Issues:**
- Well structured with clear H2/H3 hierarchy.
- Navigation links are correct.

---

### Section 10.4: Prompt Security & Optimization (~3,000 words)

**Strengths:**
- Big Picture callout correctly frames prompts as code that needs security and testing
- Injection attack taxonomy is comprehensive: direct, indirect, jailbreaks
- Attack taxonomy SVG diagram (Figure 10.8) is clear with examples and difficulty ratings for each category
- Warning callout on the fundamental difficulty of defending against injection (no syntactic boundary in natural language) is honest and important
- Three defense patterns (sandwich defense, delimiter hardening, output scanning) provide a layered approach
- Defense in depth diagram (Figure 10.9) showing four protection layers is excellent
- Promptfoo integration example with YAML configuration and assertions is practical
- Prompt versioning best practices section covers naming conventions, changelog, and rollback
- Prompt drift warning addresses a real production issue (model updates changing behavior without prompt changes)
- Production prompt pipeline section ties security, compression, testing, and versioning together
- 5 quiz questions on security and testing topics

**Weaknesses / Improvement Opportunities:**
- The sandwich defense implementation is clear, but the section does not mention that major providers have made progress on instruction hierarchy (e.g., OpenAI's system message privilege). A note on provider-level defenses would update the picture.
- LLMLingua prompt compression (Section 3.2) is described conceptually but has no code example. Since compression is becoming increasingly practical, a brief snippet showing LLMLingua usage would be valuable.
- Missing: any discussion of prompt injection detection as a separate classification task. Some production systems use a dedicated classifier to flag suspicious inputs before they reach the main LLM. A brief mention would broaden the defense toolkit.
- The structured output section in 10.4 overlaps with 9.2. A clearer cross-reference ("for implementation details, see Section 9.2") would reduce redundancy while maintaining the security framing.
- Missing: A/B testing implementation. The section mentions A/B experiments in the learning objectives and index description but does not provide a code example or framework recommendation.
- The output scanning guardrail uses string matching, which is brittle. A note about LLM-based output classification (and its cost tradeoff) would round out the approach.

**Structural Issues:**
- This section covers a lot of ground (security, compression, testing, versioning) and might benefit from being split if it grows. Currently the breadth is manageable at ~3,000 words.
- Navigation links are correct.

---

## Chapter Structure

### Section 10.1: Foundational Prompt Design (~3,500 words)
- Key concepts: prompt anatomy, zero-shot prompting, specificity principle, few-shot prompting, example selection, system prompts, role assignment, system prompt architecture (layered), prompt templates, variable injection, edge cases (hallucinations, refusals, verbosity), iterative refinement workflow
- **Diagrams:**
  - [EXISTS] Prompt anatomy mapped to chat API roles (Figure 10.1)
  - [EXISTS] System prompt architecture with attention weights (Figure 10.2)
- **Code examples:**
  - [EXISTS] Zero-shot classification
  - [EXISTS] Few-shot entity extraction with JSONL output
  - [EXISTS] System prompt with role assignment
  - [EXISTS] Prompt template system with variable injection
  - [EXISTS] Iterative refinement workflow
  - [ADD] Complete production system prompt combining all layers
- **Exercises:** [EXISTS] 5 quiz questions with detailed answers
- **Improvements:**
  - Add a complete multi-layer system prompt reference example
  - Expand few-shot example selection guidance
  - Add note on prompt length and context window limitations
  - Mention Jinja2 as an alternative to f-string templates

### Section 10.2: Chain-of-Thought & Reasoning Techniques (~3,000 words)
- Key concepts: Chain-of-Thought (zero-shot and few-shot), scratchpad mechanism, self-consistency (majority voting), Tree-of-Thought (branch, evaluate, prune, backtrack), step-back prompting, ReAct (Thought/Action/Observation loop), cost tradeoffs of multi-call techniques
- **Diagrams:**
  - [EXISTS] Direct vs. CoT prompting comparison (Figure 10.3)
  - [EXISTS] Tree-of-Thought branching and pruning (Figure 10.4)
- **Code examples:**
  - [EXISTS] Zero-shot CoT (math problem)
  - [EXISTS] Self-consistency with majority voting
  - [EXISTS] Simplified ToT implementation
  - [EXISTS] ReAct framework with search tool
  - [ADD] Few-shot CoT with explicit exemplars
- **Exercises:** [EXISTS] 5 quiz questions with detailed answers
- **Improvements:**
  - Add a few-shot CoT code example with 2 to 3 exemplars
  - Expand step-back prompting with a code example or merge into CoT
  - Show a ToT backtracking example
  - Add a concrete failure case for CoT on simple tasks

### Section 10.3: Advanced Prompt Patterns (~3,500 words)
- Key concepts: self-reflection (generate, critique, revise), Reflexion (memory-augmented self-improvement), when reflection helps vs. when it wastes compute, meta-prompting (prompts that generate prompts), prompt chaining and decomposition, Constitutional AI-style self-checks, DSPy (signatures, modules, optimizers), OPRO (optimization by prompting), comparison of optimization approaches
- **Diagrams:**
  - [EXISTS] Reflection loop (generate, critique, revise) (Figure 10.5)
  - [EXISTS] Prompt chaining with cost annotations (Figure 10.6)
  - [EXISTS] OPRO iteration with prompt-score history (Figure 10.7)
- **Code examples:**
  - [EXISTS] Basic reflection loop
  - [EXISTS] Reflexion with persistent memory
  - [EXISTS] Meta-prompting (prompt generator)
  - [EXISTS] DSPy signature and module
  - [EXISTS] DSPy optimization (BootstrapFewShot, MIPROv2)
  - [ADD] Constitutional self-check snippet
- **Exercises:** [EXISTS] 5 quiz questions with detailed answers
- **Improvements:**
  - Add a quantitative reflection improvement example (pass@1 before/after)
  - Add DSPy version compatibility note
  - Expand APE coverage or merge into OPRO comparison
  - Add context window management note for prompt chains
  - Add constitutional self-check code example

### Section 10.4: Prompt Security & Optimization (~3,000 words)
- Key concepts: prompt injection (direct, indirect, jailbreaks), sandwich defense, delimiter hardening, output scanning guardrails, defense in depth, LLMLingua prompt compression, manual compression techniques, Promptfoo regression testing, prompt versioning and changelogs, prompt drift, production prompt pipeline
- **Diagrams:**
  - [EXISTS] Injection attack taxonomy (Figure 10.8)
  - [EXISTS] Defense in depth layers (Figure 10.9)
- **Code examples:**
  - [EXISTS] Sandwich defense implementation
  - [EXISTS] Delimiter hardening
  - [EXISTS] Output scanning guardrail
  - [EXISTS] Promptfoo YAML configuration
  - [ADD] LLMLingua compression snippet
  - [ADD] A/B testing framework sketch
- **Exercises:** [EXISTS] 5 quiz questions with detailed answers
- **Improvements:**
  - Add LLMLingua code example
  - Mention provider-level instruction hierarchy defenses
  - Add injection detection as a separate classification step
  - Clarify cross-reference to 9.2 for structured output details
  - Add A/B testing code example or recommendation

---

## Terminology Standards

| Term | Usage | Notes |
|------|-------|-------|
| zero-shot | Hyphenated, lowercase | Prompting without examples |
| few-shot | Hyphenated, lowercase | Prompting with examples |
| Chain-of-Thought (CoT) | Capitalized, abbreviation in parentheses on first use | Research term from Wei et al. (2022) |
| self-consistency | Hyphenated, lowercase | Technique, not a proper noun |
| Tree-of-Thought (ToT) | Capitalized, abbreviation in parentheses on first use | Research term |
| ReAct | CamelCase | Framework name from Yao et al. (2022) |
| step-back prompting | Hyphenated, lowercase | Technique name |
| reflection / self-reflection | Lowercase | Generic agentic pattern |
| Reflexion | Capitalized | Specific framework from Shinn et al. (2023) |
| meta-prompting | Hyphenated, lowercase | Generic technique |
| prompt chaining | Lowercase | Generic technique |
| DSPy | Exact casing | Library name from Stanford |
| OPRO | All caps | Optimization by PRompting |
| prompt injection | Lowercase | Attack category |
| jailbreak | Lowercase | Attack variant |
| sandwich defense | Lowercase | Defense pattern |
| Promptfoo | Capitalized | Tool name |
| LLMLingua | CamelCase | Tool name from Microsoft |

---

## Cross-References

### Upstream Dependencies
- **Module 04 (Transformer Architecture):** Context window concept, attention mechanism (relevant to prompt length and system prompt architecture)
- **Module 05 (Decoding Strategies):** Temperature, top-p, and generation parameters used throughout all sections
- **Module 09 (LLM APIs):** API call mechanics, message formats, structured output (Instructor/Pydantic)

### Downstream Dependents
- **Module 11 (Hybrid ML+LLM):** Few-shot prompting and output formatting from 10.1; structured output from 10.4
- **Module 19 (RAG):** Prompt templates for retrieval-augmented contexts
- **Module 20 (Conversational AI):** System prompt design from 10.1; multi-turn conversation patterns
- **Module 21 (AI Agents):** ReAct framework from 10.2; reflection patterns from 10.3; tool use prompting
- **Module 22 (Multi-Agent Systems):** Meta-prompting and prompt chaining from 10.3
- **Module 25 (Evaluation):** Prompt testing and regression testing from 10.4
- **Module 26 (Production):** Prompt security and injection defense from 10.4

### Internal Cross-References
- Section 10.2 builds on the few-shot patterns from 10.1
- Section 10.3 extends 10.2's reasoning techniques with reflection and optimization
- Section 10.4 revisits structured output from 9.2 through a security lens
- The DSPy content in 10.3 complements the manual prompt refinement workflow in 10.1

---

## Estimated Word Count

| Section | Estimated Words |
|---------|----------------|
| 10.1 Foundational Prompt Design | ~3,500 |
| 10.2 Chain-of-Thought & Reasoning Techniques | ~3,000 |
| 10.3 Advanced Prompt Patterns | ~3,500 |
| 10.4 Prompt Security & Optimization | ~3,000 |
| **Total** | **~13,000** |

---

## Narrative Arc

The chapter follows a progression from **manual craft** to **systematic reasoning** to **automated optimization** to **hardening for production**:

1. **Section 10.1 (Foundation):** The reader starts with the building blocks of every prompt: how to structure instructions, provide examples, assign roles, and build reusable templates. The emphasis is on deliberate, measurable improvement through an iterative refinement workflow. The key message: good prompting is not guesswork; it is engineering with natural language.

2. **Section 10.2 (Reasoning):** The reader discovers that simple prompting hits a ceiling on complex tasks. Chain-of-Thought prompting breaks through that ceiling by teaching the model to show its work. Self-consistency and Tree-of-Thought extend this further by exploring multiple reasoning paths. ReAct bridges reasoning and action, introducing the concept that a model can reason about which tools to use. The key message: for hard problems, how you ask matters more than what you ask.

3. **Section 10.3 (Optimization):** The reader moves from hand-written prompts to prompts that improve themselves. Reflection loops let models critique and revise their own work. Meta-prompting and prompt chaining decompose complex workflows. DSPy and OPRO automate the optimization process entirely. The key message: the best prompt engineers build systems that engineer prompts for them.

4. **Section 10.4 (Hardening):** The reader confronts the reality that prompts in production face adversarial inputs and changing model behavior. Injection attacks, defense strategies, compression, and testing form the security and reliability layer. The key message: a prompt that works in a notebook is not ready for production until it is defended, compressed, tested, and versioned.

The overarching arc moves from "craft a single good prompt" to "build a prompt system that is reliable, self-improving, and secure at scale."
