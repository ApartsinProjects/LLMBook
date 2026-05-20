# Comic Wiring Report: Chapters 41 and 46

Scope: the 12 manifest rows in `.book-update/comic-manifest.jsonl` whose `chap_sec`
starts with `41.` or `46.`. All 12 JPEGs were already generated on disk; each was
wired into its section as a `<figure class="illustration">`.

## Result summary

- Wired: 12 / 12
- Skipped (missing image): 0
- Audit (P0+P1+P2, edited files): 0 issues. No FIGURE_SEQUENCE, DUP_FIGURE_NUM,
  BROKEN_FIGURE_REF, or MISSING_IMG_DIMS.

## Important note: 6 figures already existed with placeholder filenames

Sections 41.2, 41.3, 41.4, and 46.1 already contained correctly-placed figures from
an earlier illustration pass, but their `<img src>` pointed at older draft filenames
(e.g. `comic-goldfish-memory.jpg`, `comic-arena-wrestling.jpg`). The canonical
manifest images are the final generated versions. For those six, the correct action
was to repoint `src` to the manifest filename rather than create a duplicate figure
(placement, alt, caption, and figure number were already correct). The other six
sections (41.1, 41.5, 46.2, 46.3, 46.4, 46.5) received brand-new figures with a prose
reference sentence added immediately before each.

## Per-comic detail

| chap_sec | manifest file | section | figure # | action | placement anchor |
|----------|---------------|---------|----------|--------|------------------|
| 41.1 | comic-41.1-35-platforms.jpg | section-41.1.html | 41.1.2 | NEW | after "Vendor lock-in is real but not always bad" warning |
| 41.2 | comic-41.2-38-libraries-and-frameworks.jpg | section-41.2.html | 41.2.1 | repoint (was comic-goldfish-memory.jpg) | memory primitives heading, near "Memory is the most under-engineered" callout |
| 41.2 | comic-41.2-39-libraries-and-frameworks.jpg | section-41.2.html | 41.2.2 | repoint (was comic-framework-graveyard.jpg) | orchestration-frameworks heading, framework half-life theme |
| 41.3 | comic-41.3-41-datasets-and-benchmarks.jpg | section-41.3.html | 41.3.1 | repoint (was comic-arena-wrestling.jpg) | LMSYS Arena / preference-benchmarks heading |
| 41.4 | comic-41.4-43-models.jpg | section-41.4.html | 41.4.1 | repoint (was comic-cascaded-vs-realtime.jpg) | 41.4.2 Voice-aware models |
| 41.5 | comic-41.5-45-external-reading-and-communities.jpg | section-41.5.html | 41.5.1 | NEW | end of main content (before bibliography), communities theme |
| 46.1 | comic-46.1-48-why-llm-as-judge-matters.jpg | section-46.1.html | 46.1.2 | repoint (was comic-gpt4-mirror.jpg) | after GPT-4 narcissism / self-preference, GPT-4 mirror |
| 46.1 | comic-46.1-49-why-llm-as-judge-matters.jpg | section-46.1.html | 46.1.1 | repoint (was comic-judge-five-biases.jpg) | Judge Bias Taxonomy, five-biases scale |
| 46.2 | comic-46.2-51-judge-reliability-and-common-biases.jpg | section-46.2.html | 46.2.2 | NEW | after the Tip "G-Eval requires logprobs access" |
| 46.3 | comic-46.3-53-debiasing-techniques-position-length-and-verbosi.jpg | section-46.3.html | 46.3.2 | NEW | after the "rubric-trained 7B beats GPT-4" Key Insight |
| 46.4 | comic-46.4-55-training-judge-models.jpg | section-46.4.html | 46.4.2 | NEW | after the Warning "distilled judges inherit the biases of their teacher" |
| 46.5 | comic-46.5-57-multi-judge-ensembles-and-production-patterns.jpg | section-46.5.html | 46.5.2 | NEW | end of section, after Key Takeaways (juror-panel ensemble) |

Note on manifest comic numbers for 46.1: comic 48 is the GPT-4-mirror (self-preference,
maps to existing Figure 46.1.2), comic 49 is the five-biases balance scale (maps to
existing Figure 46.1.1). They were repointed to match concept, not list order.

## Caption-order pass

`scripts/fix_caption_order_only.py --apply` was run on all 10 edited files: 3 caption
renumbers applied (1 in section-41.2.html, 2 in section-46.3.html), all Code Fragment
caption renumbers into document order. Prose references were re-checked afterward:

- 41.2: 1 Code Fragment caption renumber; no prose refs to those fragments, none stale.
- 46.3: 2 Code Fragment caption renumbers; the single prose ref (Code Fragment 46.3.1)
  and my Figure 46.3.2 prose ref both still match their captions.

## Editorial choices

- alt text describes the cartoon for a screen reader (characters, labels, action),
  distinct from the caption.
- captions connect each joke to the technical point of its section.
- Figure 46.3 caption deliberately frames the Prometheus 2 image around the
  rubric-specialist-beats-generalist result the section actually argues, and does not
  assert distillation (Prometheus 2 is rubric-fine-tuned, not GPT-4-distilled like
  JudgeLM in 46.4), keeping the caption technically accurate.
- No em dashes or double dashes were introduced.
- Existing humorous illustrations in the dry eval/tool sections were preserved.
- No images were modified or regenerated.
