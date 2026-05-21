# Heading hierarchy & alt-text accessibility audit

Total HTML files scanned: 546

## Summary

| Issue | Total | Pages affected |
|---|---:|---:|
| Heading: skipped level (h1->h3 etc) | 230 | 227 |
| Heading: multiple <h1> on page | 0 | 0 |
| Heading: <h1> after non-h1 (demoted) | 0 | 0 |
| Heading: empty heading | 0 | 0 |
| Heading: block element inside heading | 299 | 16 |
| Alt: missing alt attribute | 0 | 0 |
| Alt: empty alt inside <figure> | 0 | 0 |
| Alt: boilerplate text | 25 | 25 |
| Alt: too short (<8 chars in figure) | 2 | 2 |
| Alt: too long (>250 chars) | 13 | 13 |

## Heading hierarchy issues

Files with heading issues: **242**

### Bulk pattern: single h1 -> h3 skip (223 pages)

These pages share the same templating pattern: a single `<h1>` section title followed directly by `<h3>` subsections, with no intermediate `<h2>`. This is consistent across the section template and should be fixed at the template level by either re-leveling subsections to `<h2>` or by inserting an `<h2>` chapter banner.

| Directory | Pages affected |
|---|---:|
| `.book-update/v9-preserved-content/` | 1 |
| `appendices/appendix-a-mathematical-foundations/` | 4 |
| `front-matter/` | 1 |
| `part-1-llm-building-blocks/module-00-ml-pytorch-foundations/` | 4 |
| `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/` | 7 |
| `part-1-llm-building-blocks/module-02-sequence-models-attention/` | 3 |
| `part-1-llm-building-blocks/module-03-transformer-architecture/` | 5 |
| `part-1-llm-building-blocks/module-04-decoding-text-generation/` | 4 |
| `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/` | 2 |
| `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/` | 4 |
| `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/` | 2 |
| `part-11-llm-ethics-trust-governance/module-52-bias-fairness/` | 2 |
| `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/` | 4 |
| `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/` | 2 |
| `part-12-llm-systems-at-scale/module-57-compute-planning/` | 1 |
| `part-12-llm-systems-at-scale/module-60-edge-on-device-llms/` | 1 |
| `part-13-llmops-lifecycle/module-62-production-engineering-core/` | 2 |
| `part-13-llmops-lifecycle/module-63-ai-gateways-routing/` | 1 |
| `part-13-llmops-lifecycle/module-64-workflow-orchestration/` | 1 |
| `part-13-llmops-lifecycle/module-65-containers-kubernetes/` | 1 |
| `part-13-llmops-lifecycle/module-66-reliability-slos-registry/` | 1 |
| `part-14-designing-llm-agent-products/module-67-ideation/` | 10 |
| `part-14-designing-llm-agent-products/module-68-vibe-coding/` | 3 |
| `part-14-designing-llm-agent-products/module-70-shipping-products/` | 6 |
| `part-15-applications-of-llms-across-industries/module-72-legal-llms/` | 2 |
| `part-15-applications-of-llms-across-industries/module-73-finance-llms/` | 1 |
| `part-15-applications-of-llms-across-industries/module-74-healthcare-llms/` | 1 |
| `part-15-applications-of-llms-across-industries/module-75-education-llms/` | 1 |
| `part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/` | 1 |
| `part-15-applications-of-llms-across-industries/module-77-government-llms/` | 1 |
| `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/` | 6 |
| `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/` | 3 |
| `part-16-llm-agentic-ai-research-frontiers/module-81-frontier-theory/` | 4 |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws/` | 9 |
| `part-2-understanding-llms/module-07-modern-llm-landscape/` | 3 |
| `part-2-understanding-llms/module-08-reasoning-test-time-compute/` | 6 |
| `part-2-understanding-llms/module-09-inference-optimization/` | 7 |
| `part-2-understanding-llms/module-10-interpretability/` | 4 |
| `part-3-working-with-llms/module-11-llm-apis/` | 4 |
| `part-3-working-with-llms/module-12-prompt-engineering/` | 5 |
| `part-3-working-with-llms/module-13-hybrid-ml-llm/` | 4 |
| `part-4-training-adaptation/module-15-synthetic-data/` | 7 |
| `part-4-training-adaptation/module-16-fine-tuning-fundamentals/` | 7 |
| `part-4-training-adaptation/module-17-peft/` | 7 |
| `part-4-training-adaptation/module-18-alignment-rlhf-dpo/` | 5 |
| `part-5-multimodal-llms/module-22-vision-language-models/` | 1 |
| `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/` | 2 |
| `part-6-agentic-ai/module-26-ai-agents/` | 6 |
| `part-6-agentic-ai/module-27-tool-use-protocols/` | 6 |
| `part-6-agentic-ai/module-28-multi-agent-systems/` | 4 |
| `part-6-agentic-ai/module-29-specialized-agents/` | 4 |
| `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/` | 5 |
| `part-7-retrieval-information-extraction-with-llms/module-32-rag/` | 4 |
| `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/` | 1 |
| `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/` | 5 |
| `part-8-conversational-ai-with-llms/module-37-conversational-ai/` | 4 |
| `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/` | 2 |
| `part-9-llm-evaluation-observability/module-42-evaluation-foundations/` | 12 |
| `part-9-llm-evaluation-observability/module-43-specialized-evaluation/` | 5 |
| `part-9-llm-evaluation-observability/module-44-online-eval-observability/` | 2 |

### Non-template heading issues (19 pages)

#### `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html`
- L67: <h3> contains block element <p>
- L87: <h3> contains block element <p>
- L113: <h3> contains block element <p>
- L142: <h3> contains block element <p>
- L153: <h3> contains block element <ul>
- L177: <h3> contains block element <p>
- L223: <h3> contains block element <p>
- L225: <h3> contains block element <p>
- L243: <h3> contains block element <p>
- L257: <h3> contains block element <p>
- L343: <h3> contains block element <p>
- L373: <h3> contains block element <p>
- L399: <h3> contains block element <p>
- L402: <h3> contains block element <p>
- L405: <h3> contains block element <p>
- L407: <h3> contains block element <div>
- L422: <h3> contains block element <p>
- L436: <h3> contains block element <p>
- L458: <h3> contains block element <p>

#### `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html`
- L87: <h3> contains block element <p>
- L127: <h3> contains block element <p>
- L163: <h3> contains block element <p>
- L210: <h3> contains block element <p>
- L248: <h3> contains block element <p>
- L272: <h3> contains block element <p>
- L439: <h3> contains block element <p>
- L501: <h3> contains block element <p>
- L507: <h3> contains block element <p>
- L526: <h3> contains block element <div>
- L674: <h3> contains block element <p>
- L689: <h3> contains block element <p>
- L713: <h3> contains block element <p>
- L734: <h3> contains block element <p>
- L774: <h3> contains block element <p>
- L800: <h3> contains block element <ul>
- L810: <h3> contains block element <p>
- L829: <h3> contains block element <p>
- L835: <h3> contains block element <p>
- L846: <h3> contains block element <p>
- L915: <h3> contains block element <p>
- L1055: <h3> contains block element <ul>
- L1068: <h3> contains block element <p>
- L1083: <h3> contains block element <p>
- L1145: <h3> contains block element <p>
- L1170: <h3> contains block element <p>

#### `part-14-designing-llm-agent-products/module-67-ideation/section-67.12.html`
- L41: skipped level (h1 -> h3)
- L57: skipped level (h2 -> h4)

#### `part-14-designing-llm-agent-products/module-67-ideation/section-67.15.html`
- L41: skipped level (h1 -> h3)
- L54: skipped level (h2 -> h4)

#### `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html`
- L79: <h3> contains block element <p>
- L89: <h3> contains block element <p>
- L110: <h3> contains block element <p>
- L140: <h3> contains block element <table>
- L157: <h3> contains block element <p>
- L195: <h3> contains block element <p>
- L205: <h3> contains block element <p>
- L231: <h3> contains block element <p>
- L233: <h3> contains block element <p>
- L235: <h3> contains block element <table>

#### `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html`
- L95: <h3> contains block element <ol>
- L131: <h3> contains block element <p>
- L202: <h3> contains block element <ul>
- L213: <h3> contains block element <p>

#### `part-16-llm-agentic-ai-research-frontiers/module-80-frontier-architectures/section-80.4.html`
- L50: skipped level (h1 -> h3)
- L54: <h2> contains block element <p>

#### `part-2-understanding-llms/module-10-interpretability/section-10.6.html`
- L91: <h3> contains block element <p>
- L124: <h3> contains block element <p>
- L169: <h3> contains block element <p>
- L207: <h3> contains block element <p>
- L233: <h3> contains block element <p>
- L277: <h3> contains block element <p>
- L340: <h3> contains block element <p>
- L362: <h3> contains block element <p>
- L407: <h3> contains block element <p>
- L434: <h3> contains block element <p>
- L502: <h3> contains block element <p>
- L543: <h3> contains block element <p>
- L564: <h3> contains block element <p>
- L591: <h3> contains block element <p>
- L609: <h3> contains block element <p>
- L629: <h3> contains block element <p>
- L669: <h3> contains block element <p>
- L701: <h3> contains block element <p>
- L721: <h3> contains block element <p>
- L788: <h3> contains block element <p>
- L810: <h3> contains block element <p>
- L837: <h3> contains block element <p>
- L860: <h3> contains block element <p>
- L881: <h3> contains block element <p>
- L893: <h3> contains block element <p>
- L938: <h3> contains block element <p>
- L957: <h3> contains block element <p>
- L994: <h3> contains block element <div>
- L1008: <h3> contains block element <p>
- L1048: <h3> contains block element <p>
- L1083: <h3> contains block element <p>

#### `part-2-understanding-llms/module-10-interpretability/section-10.8.html`
- L126: <h3> contains block element <p>
- L147: <h3> contains block element <p>
- L199: <h3> contains block element <p>
- L217: <h3> contains block element <div>
- L228: <h3> contains block element <p>
- L261: <h3> contains block element <p>

#### `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html`
- L41: skipped level (h1 -> h3)
- L56: skipped level (h2 -> h4)

#### `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html`
- L89: <h3> contains block element <p>
- L127: <h3> contains block element <p>
- L143: <h3> contains block element <p>
- L161: <h3> contains block element <p>
- L184: <h3> contains block element <p>
- L203: <h3> contains block element <p>
- L205: <h3> contains block element <p>
- L247: <h3> contains block element <p>

#### `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html`
- L136: <h3> contains block element <p>
- L205: <h3> contains block element <p>
- L238: <h3> contains block element <p>
- L266: <h3> contains block element <p>
- L307: <h3> contains block element <p>
- L398: <h3> contains block element <p>
- L448: <h3> contains block element <p>
- L452: <h3> contains block element <p>
- L504: <h3> contains block element <p>
- L537: <h3> contains block element <p>
- L541: <h3> contains block element <p>
- L572: <h3> contains block element <p>
- L596: <h3> contains block element <p>
- L616: <h3> contains block element <p>
- L642: <h3> contains block element <p>

#### `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.1.html`
- L70: <h3> contains block element <p>
- L114: <h3> contains block element <p>
- L168: <h3> contains block element <p>
- L211: <h3> contains block element <p>
- L258: <h3> contains block element <p>
- L309: <h3> contains block element <p>

#### `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.2.html`
- L85: <h3> contains block element <p>
- L133: <h3> contains block element <p>
- L173: <h3> contains block element <p>
- L215: <h3> contains block element <p>
- L264: <h3> contains block element <p>
- L266: <h3> contains block element <p>
- L281: <h3> contains block element <p>
- L314: <h3> contains block element <p>
- L392: <h3> contains block element <p>
- L450: <h3> contains block element <p>
- L521: <h3> contains block element <p>
- L558: <h3> contains block element <p>
- L632: <h3> contains block element <p>
- L686: <h3> contains block element <p>
- L738: <h3> contains block element <p>
- L774: <h3> contains block element <p>
- L825: <h3> contains block element <p>
- L885: <h3> contains block element <p>
- L940: <h3> contains block element <p>
- L1021: <h3> contains block element <p>
- L1064: <h3> contains block element <p>
- L1089: <h3> contains block element <p>
- L1111: <h3> contains block element <p>
- L1128: <h3> contains block element <p>
- L1153: <h3> contains block element <p>
- L1166: <h3> contains block element <p>
- L1195: <h3> contains block element <p>
- L1223: <h3> contains block element <p>
- L1249: <h3> contains block element <p>
- L1277: <h3> contains block element <p>
- L1315: <h3> contains block element <p>
- L1346: <h3> contains block element <p>
- L1362: <h3> contains block element <p>
- L1400: <h3> contains block element <p>
- L1420: <h3> contains block element <p>
- L1453: <h3> contains block element <p>
- L1478: <h3> contains block element <p>
- L1507: <h3> contains block element <p>
- L1553: <h3> contains block element <p>
- L1580: <h3> contains block element <p>
- L1615: <h3> contains block element <p>
- L1662: <h3> contains block element <p>
- L1706: <h3> contains block element <p>
- L1729: <h3> contains block element <p>
- L1773: <h3> contains block element <p>
- L1819: <h3> contains block element <p>
- L1825: <h3> contains block element <p>
- L1853: <h3> contains block element <p>
- L1883: <h3> contains block element <p>
- L1885: <h3> contains block element <p>
- L1888: <h3> contains block element <p>
- L1907: <h3> contains block element <p>
- L1943: <h3> contains block element <p>
- L1994: <h3> contains block element <p>
- L2069: <h3> contains block element <p>
- L2121: <h3> contains block element <p>
- L2167: <h3> contains block element <p>
- L2218: <h3> contains block element <p>

#### `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3.html`
- L194: <h3> contains block element <p>
- L341: <h3> contains block element <p>
- L347: <h3> contains block element <p>
- L382: <h3> contains block element <pre>
- L449: <h3> contains block element <p>
- L532: <h3> contains block element <p>
- L542: <h3> contains block element <p>
- L550: <h3> contains block element <pre>
- L593: <h3> contains block element <p>
- L599: <h3> contains block element <p>
- L616: <h3> contains block element <pre>
- L661: <h3> contains block element <pre>
- L697: <h3> contains block element <p>
- L732: <h3> contains block element <p>
- L809: <h3> contains block element <p>
- L842: <h3> contains block element <p>
- L871: <h3> contains block element <p>
- L903: <h3> contains block element <p>
- L939: <h3> contains block element <p>
- L972: <h3> contains block element <p>
- L998: <h3> contains block element <p>
- L1057: <h3> contains block element <p>
- L1114: <h3> contains block element <p>
- L1157: <h3> contains block element <p>
- L1205: <h3> contains block element <p>
- L1257: <h3> contains block element <p>
- L1287: <h3> contains block element <p>

#### `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.4.html`
- L115: <h3> contains block element <p>
- L244: <h3> contains block element <p>
- L287: <h3> contains block element <p>
- L394: <h3> contains block element <p>
- L446: <h3> contains block element <p>
- L583: <h3> contains block element <p>
- L663: <h3> contains block element <p>

#### `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html`
- L111: <h3> contains block element <p>
- L152: <h3> contains block element <p>
- L176: <h3> contains block element <p>
- L227: <h3> contains block element <p>
- L267: <h3> contains block element <p>
- L293: <h3> contains block element <p>
- L353: <h3> contains block element <p>
- L413: <h3> contains block element <p>
- L417: <h3> contains block element <p>
- L459: <h3> contains block element <p>
- L499: <h3> contains block element <p>
- L526: <h3> contains block element <p>
- L670: <h3> contains block element <p>
- L678: <h3> contains block element <p>
- L748: <h3> contains block element <p>
- L830: <h3> contains block element <p>
- L843: <h3> contains block element <p>
- L871: <h3> contains block element <p>
- L898: <h3> contains block element <p>
- L905: <h3> contains block element <p>
- L908: <h3> contains block element <p>
- L911: <h3> contains block element <div>
- L926: <h3> contains block element <p>
- L933: <h3> contains block element <p>

#### `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.1.html`
- L66: <h3> contains block element <p>
- L122: <h3> contains block element <p>
- L152: <h3> contains block element <p>
- L158: <h3> contains block element <p>
- L195: <h3> contains block element <p>
- L222: <h3> contains block element <p>
- L292: <h3> contains block element <p>
- L371: <h3> contains block element <p>
- L376: <h3> contains block element <p>
- L382: <h3> contains block element <p>
- L421: <h3> contains block element <p>
- L432: <h3> contains block element <p>
- L449: <h3> contains block element <p>
- L474: <h3> contains block element <p>
- L549: <h3> contains block element <p>
- L624: <h3> contains block element <p>
- L668: <h3> contains block element <p>
- L726: <h3> contains block element <p>
- L786: <h3> contains block element <p>
- L851: <h3> contains block element <p>

#### `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html`
- L70: <h3> contains block element <p>
- L93: <h3> contains block element <p>
- L122: <h3> contains block element <p>
- L162: <h3> contains block element <p>
- L164: <h3> contains block element <p>
- L170: <h3> contains block element <p>
- L238: <h3> contains block element <p>
- L241: <h3> contains block element <p>
- L271: <h3> contains block element <p>
- L306: <h3> contains block element <p>
- L346: <h3> contains block element <p>
- L392: <h3> contains block element <div>
- L402: <h3> contains block element <p>
- L436: <h3> contains block element <p>
- L487: <h3> contains block element <p>
- L552: <h3> contains block element <p>
- L597: <h3> contains block element <p>
- L649: <h3> contains block element <p>
- L691: <h3> contains block element <p>
- L754: <h3> contains block element <p>
- L805: <h3> contains block element <p>
- L813: <h3> contains block element <p>
- L831: <h3> contains block element <p>
- L838: <h3> contains block element <p>
- L864: <h3> contains block element <p>
- L887: <h3> contains block element <p>
- L924: <h3> contains block element <p>
- L933: <h3> contains block element <p>
- L935: <h3> contains block element <p>
- L937: <h3> contains block element <p>
- L969: <h3> contains block element <table>
- L986: <h3> contains block element <p>
- L1023: <h3> contains block element <p>
- L1026: <h3> contains block element <p>
- L1068: <h3> contains block element <p>
- L1082: <h3> contains block element <p>
- L1088: <h3> contains block element <p>

## Alt-text issues

### Missing `alt` attribute (0 total)

_None._

### Empty `alt=""` inside `<figure>` (0 total)

_None._

### Boilerplate alt text (25 total)

- `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.3.html` L169 [contains 'diagram of']: alt="Diagram of the Word2Vec Skip-gram architecture showing a center word as input, a hidden embedding layer, and output con..."
- `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.4.html` L67 [contains 'illustration of']: alt="Illustration of the polysemy problem showing the word bank with multiple meanings (financial institution, river bank, t..."
- `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html` L407 [contains 'image']: alt="Multimodal models convert images to token sequences via patch embedding"
- `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.1.html` L60 [contains 'diagram of']: alt="Diagram of three-layer LLM safety stack. Bottom layer labeled 'Alignment Training (RLHF, DPO, Constitutional AI)' shape..."
- `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.5.html` L120 [contains 'image']: alt="Diagram of a multimodal guardrail stack. User input branches into three lanes: text (Prompt Guard 2 + Presidio), image ..."
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html` L67 [contains 'diagram of']: alt="Diagram of the provenance ecosystem. Left side shows content sources: 'AI generator (closed)', 'AI generator (open weig..."
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.3.html` L156 [contains 'image']: alt="Two-panel comparison. Left panel: 'C2PA manifest' shown as a metadata block attached externally to an image file with a..."
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.4.html` L90 [contains 'image']: alt="Diagram of a video deepfake detection ensemble. Input video is decomposed into three parallel streams: (1) per-frame im..."
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.5.html` L60 [contains 'image']: alt="Diagram showing a watermarked image being attacked. The original image with embedded SynthID watermark passes through t..."
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.7.html` L115 [contains 'diagram of']: alt="Diagram of a typical dataset auditing pipeline. A dataset enters from the left. Three parallel analysis tools run: (1) ..."
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.9.html` L123 [contains 'diagram of']: alt="Diagram of a hash-chained audit log architecture. A sequence of audit log entries is shown horizontally. Each entry con..."
- `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html` L66 [contains 'diagram of']: alt="Sequence diagram of one DeMo optimizer step across a heterogeneous worker fleet"
- `part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/section-83.5.html` L46 [contains 'graphic']: alt="Concentric-ring infographic of the LLM field"
- `part-3-working-with-llms/module-11-llm-apis/section-11.4.html` L231 [contains 'image']: alt="A robot with multiple sensory inputs (eyes for images, ears for audio, hands for text) representing multimodal APIs"
- `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.1.html` L127 [contains 'image']: alt="Diagram comparing classical OCR pipeline (image to text to JSON) with end-to-end OCR-free model (image to JSON directly)"
- `part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html` L60 [contains 'image']: alt="ViT architecture diagram: image to patches to flattened patches to linear projection plus position embeddings to transf..."
- `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html` L61 [contains 'image']: alt="LLaVA-NeXT dynamic resolution diagram: 672x672 image partitioned into 4 tiles plus a downsampled overview, each tile en..."
- `part-5-multimodal-llms/module-22-vision-language-models/section-22.6.html` L43 [contains 'image']: alt="Two architecture diagrams side by side: a pipeline with ASR, LLM, TTS as discrete boxes, versus a native multimodal mod..."
- `part-5-multimodal-llms/module-22-vision-language-models/section-22.8.html` L39 [contains 'diagram of']: alt="Block diagram of an any-to-any architecture: modality encoders feed an LLM core, the LLM emits semantic embeddings that..."
- `part-5-multimodal-llms/module-22-vision-language-models/section-22.9.html` L39 [contains 'image']: alt="Comparison radar chart across four frontier omni models on six axes: text quality, image understanding, audio understan..."
- `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.1.html` L171 [contains 'diagram of']: alt="A timeline diagram of dynamic Gaussian splat evolution: 3DGS (2023), 4DGS (2024), Dynamic 3D Gaussians (2024), 4D-Rotor..."
- `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.3.html` L52 [contains 'image']: alt="Two-tier image-to-3D pipeline: input image, multi-view diffusion produces 4 to 16 novel views, then 3DGS or NeRF optimi..."
- `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.1.html` L52 [contains 'image']: alt="Diagram of a joint embedding space: a text encoder and an image encoder both project into a shared d-dimensional sphere..."
- `part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.2.html` L39 [contains 'image']: alt="Multimodal RAG architecture: user query, retrieval over text/image/audio/video index, top-k results spliced into VLM pr..."
- `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.2.html` L43 [contains 'diagram of']: alt="Block diagram of a streaming audio loop showing microphone, VAD, chunker, ASR or audio encoder, LLM, TTS or audio decod..."

### Alt text too short (<8 chars, inside `<figure>`) (2 total)

- `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html` L303: alt="Diagram" src=`images/section-l.1-svg1.png`
- `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html` L223: alt="Diagram" src=`images/section-l.5-svg1.png`

### Alt text too long (>250 chars) (13 total)

- `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.1.html` L60: alt length = 510 chars, src=`images/three-layer-safety.svg`
- `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.2.html` L167: alt length = 290 chars, src=`images/input-pipeline.svg`
- `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.3.html` L118: alt length = 481 chars, src=`images/output-guardrail-comparison.svg`
- `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/section-48.5.html` L120: alt length = 589 chars, src=`images/multimodal-guardrail-stack.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html` L67: alt length = 698 chars, src=`images/provenance-ecosystem.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.10.html` L91: alt length = 695 chars, src=`images/explainability-three-views.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.2.html` L127: alt length = 523 chars, src=`images/watermark-robustness.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.3.html` L156: alt length = 614 chars, src=`images/c2pa-vs-synthid-image.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.4.html` L90: alt length = 612 chars, src=`images/video-detection-ensemble.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.5.html` L60: alt length = 629 chars, src=`images/watermark-attack-tree.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.7.html` L115: alt length = 664 chars, src=`images/datasheet-pipeline.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.8.html` L80: alt length = 825 chars, src=`images/frontier-disclosure-comparison.svg`
- `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.9.html` L123: alt length = 610 chars, src=`images/audit-log-chain.svg`

## Worst-offender pages (3+ combined issues)

| Page | Heading issues | Alt issues | Total |
|---|---:|---:|---:|
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.2.html` | 58 | 0 | 58 |
| `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.2.html` | 37 | 0 | 37 |
| `part-2-understanding-llms/module-10-interpretability/section-10.6.html` | 31 | 0 | 31 |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3.html` | 27 | 0 | 27 |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html` | 26 | 0 | 26 |
| `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html` | 24 | 1 | 25 |
| `part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.1.html` | 20 | 0 | 20 |
| `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html` | 19 | 0 | 19 |
| `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html` | 15 | 1 | 16 |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html` | 10 | 0 | 10 |
| `part-3-working-with-llms/module-14-tools-of-the-trade/section-14.1.html` | 8 | 0 | 8 |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.4.html` | 7 | 0 | 7 |
| `part-2-understanding-llms/module-10-interpretability/section-10.8.html` | 6 | 0 | 6 |
| `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.1.html` | 6 | 0 | 6 |
| `part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html` | 4 | 0 | 4 |

## Recommended fix priority

1. **Repair 0 empty headings and 299 headings containing block elements.** These usually indicate broken templating and should be reviewed by hand.
2. **Re-level 230 skipped-heading instances** (e.g. h1 -> h3). Fix at the section template by either inserting an `<h2>` chapter banner or demoting the section subheads from `<h3>` to `<h2>`.
3. **Rewrite 25 boilerplate and 2 ultra-short alts** with concrete descriptions. 'Image of X' and 'Diagram' add no information.
4. **Trim 13 overlong alts (>250 chars)** by moving detail to the figure caption.
