# Diagram Inclusion Policy

A diagram earns its place by adding something the prose cannot. If the
diagram is just the prose drawn as boxes-with-arrows, the reader gains
nothing and the page becomes longer for nothing.

## The "what would I lose" test

Cover the diagram with your hand. Can you still understand the section?
- **Yes, completely** → diagram is decorative. **Drop it.**
- **Mostly, but I'd miss the spatial relationship / quantitative scale /
  named components** → diagram pulls weight. **Keep it.**

## When linear "sequence of steps" diagrams ARE useful

1. **Quantitative funnel** — show how a quantity changes across steps
   (e.g. "100 TB → 20 TB → 12 TB → 5 TB → 3 TB" for data curation).
   The drop ratios are the message; prose buries them in paragraphs.

2. **Named architecture stack** — concrete components stacked, each with
   a real name (e.g. "HTTP Server → API Layer → Scheduler → KV Cache →
   Executor → GPU"). The diagram makes the stack memorable. The reader
   wants this as a quick reference.

3. **Concrete worked example** — actual values flowing through the
   pipeline (e.g. logit lens showing "Layer 0: 'the' → Layer 4: 'France'
   → Layer 8: 'Paris'"). The diagram IS the example.

4. **Branching / decision points** — when the path isn't actually linear.
   A real flowchart with diamonds and forks.

5. **Multi-modal** — visual + textual labels that reinforce each other
   (e.g. a chess-like tree of beam search with log-prob scores at each
   node).

## When linear "sequence of steps" diagrams are NOT useful

1. **Generic labels only**: "Input → Process → Output", "Step 1 → Step 2
   → Step 3", "Tokenize → Embed → Generate". The labels carry no
   information the prose doesn't already give.

2. **Action-replay**: "Step 0: do X. Step 1: do Y. Step 2: do Z." drawn
   as a vertical chain of boxes. The reader reads the steps in the prose
   first, then sees the same steps boxed below. Pure redundancy.

3. **Faithful copy of prose pipeline**: when the figure caption can be
   inferred entirely from the visible labels and the reader is told
   nothing new by looking at it.

## Action policy

- **DROP** the figure if (1), (2), or (3) above.
- **CONVERT** to a richer visualization (matplotlib chart, Gemini
  infographic with quantitative axis, multi-panel composition) if the
  underlying message has structure that LINEAR boxes don't capture.
- **KEEP** if any of "When linear is useful" criteria are met.

## Audited and applied (v6.48)

| Diagram | Action | Rationale |
|---|---|---|
| `fig-2.2.6-bpe-merges` (Tokenization) | DROP | Step 0-4 action replay; prose lists same merges |
| `fig-1.2.1-nlp-pipeline` (NLP foundations) | DROP | Raw text → ... → Features; pure label sequence |
| `fig-7.1.3-reasoning-token-flow` (Reasoning models) | DROP | Prompt → Thinking → Answer → API; trivial chain |
| `fig-6.4.3-data-pipeline` (Pretraining) | DROP | Redundant with `fig-6.4.3-curation-funnel.png` (richer matplotlib version) |

## Audited and kept (v6.48)

The remaining 19 linear-step Mermaid diagrams all hit at least one of the
"useful" criteria:

- Quantitative: `section-10.5-svg1` (sparsity-quantize-distill GB sizes),
  `section-11.2-svg2` (ToT scores), `fig-7.3.4-mcts`,
  `fig-10.1.3-logit-lens`, `fig-5.1.3-beam-search` (log-prob examples).
- Named-architecture stacks: `fig-9.4.2-serving-stack`,
  `fig-3.3.2-scaled-dot-product`, `fig-11.1.2-llm-api-ecosystem`,
  `fig-25.1.3-prompt-injection-defense`, `fig-26.5.1-vla-pipeline`,
  `fig-0.3.3-comp-graph`, `fig-1.4.3-elmo`.
- Worked-example demonstrations: `fig-27.1.2-fim` (actual code shown),
  `section-11.2-svg1` (CoT vs direct prompting numeric example),
  `section-11.3-svg3` (prompt optimization with scores),
  `section-11.3-svg1` (generate-critique-revise loop),
  `section-11.1-svg2` (5-part prompt anatomy),
  `section-10.3-svg1` (fallback levels with UX implications),
  `fig-35.1.1-token-to-dollar` (cost-attribution flow with formulas).
