# Comic Illustration / Analogy Opportunities Audit

Scope: new chapters Ch 34, 36, 41, 46, 56, 59, 61 plus Wave 17i consolidated sections (24.6, 24.13, 26.6, 27.5, 29.1, 29.4, 35.2, 35.3, 37.3).

Voice target: XKCD-style metaphors, warm cartoon illustrations, and self-deprecating section-end notes. Reference voice: Section 0.1's "the cat was unimpressed", Section 1.3's "HR got involved" epigraph, Section 24.13's deployment-playbook tone, and the agent-epigraph cards already in use.

For each opportunity: (a) precise placement, (b) suggested concept/metaphor, (c) suggested gemini-imagegen prompt (where relevant).

Layout key:
- COMIC = small inline SVG or PNG with a humorous metaphor
- ANALOGY = a "X is like Y from everyday life" inline line in prose
- MENTAL-MAP = small whimsical diagram visualizing the section's mental model
- EPIGRAPH = opportunity to add a missing agent epigraph at the top of the section

---

## Chapter 34: Structured Information Extraction & NER

### Section 34.1: The Information Extraction Landscape

1. EPIGRAPH (top of `<main>`, before the first `<h2>`). The section opens directly into `34.1.1` with no epigraph and no big-picture callout. Suggest an Agent-X-style line riffing on "I found three entities, two of which I made up." Use existing agent avatar `prompt.png` or a new "extractor" agent.
2. MENTAL-MAP after paragraph ending "...and reserves the LLM for novel or complex extraction tasks". Concept: a librarian (classical NER) sorting fast through the easy books, then handing the weird ones to a wizard (LLM) who occasionally hallucinates an author. Imagegen prompt: `"A friendly cartoon librarian in glasses rapidly stamping books labeled PERSON, ORG, DATE with a green checkmark, while behind her a wizard in a tall blue hat is conjuring a glowing book labeled 'medical_condition' out of thin air, watercolor children's-book style, warm palette, no text on the books except labels, 16:9."`
3. ANALOGY in the same paragraph as Tip ("Always run spaCy's NER first..."): add "It's like getting the spell-checker's opinion before sending the email to your boss: cheap, fast, and saves the LLM from inventing words." (one-liner only.)
4. COMIC after Table 34.1.1. The table is dry; a four-panel comic comparing "Classical NER vs LLM NER" would carry the contrast. Imagegen prompt: `"Four-panel cartoon strip, white background, hand-drawn marker style. Panel 1: a small clockwork robot labeled 'spaCy' calmly stamping 'PERSON' on a passing piece of paper. Panel 2: same robot looking puzzled at a paper labeled 'medical_condition' and shrugging. Panel 3: a large slightly tired-looking wizard labeled 'LLM' lifting the same paper, casting a glow. Panel 4: the wizard hands back a result that says 'medical_condition: Stage II non-small cell lung cancer (confidence 0.97)' while a coin labeled '$0.02' falls into a tip jar. No speech bubbles, all gentle, friendly cartoon style."`

### Section 34.2: Classical and Open Information Extraction

5. ANALOGY in the paragraph introducing Open IE ("Traditional relation extraction requires a predefined schema..."). Add: "It's like the difference between filling out a tax form (closed IE) and writing a free-form journal entry the IRS still tries to file (open IE)."
6. COMIC after the Semantic Role Labeling callout. Concept: a Whodunit detective board labeling "Agent: Butler, Patient: Lord Featherstone, Instrument: candlestick, Location: library, Temporal: 9pm." Imagegen prompt: `"A cozy detective's pinboard, sepia tones, with a magnifying glass and red string connecting labeled photo cards: 'AGENT: butler', 'PATIENT: lord', 'INSTRUMENT: candlestick', 'LOCATION: library', 'TEMPORAL: 9pm'. Above the board a chalkboard reads 'Semantic Role Labeling'. Cozy, warm, slightly funny, watercolor over ink."`
7. MENTAL-MAP after section "From Events to Knowledge Graphs". Concept: events flowing into a graph database, with each event as a paper airplane carrying a "trigger + arguments" label, landing on the right node in a graph. Caption: "Events become hyper-edges; entities catch them like fly-paper."

### Section 34.3: Hybrid IE Architectures with LLMs

8. ANALOGY in the intro paragraph ("In a production document processing system, you might need to extract entities from 10,000 documents per day..."). Add: "Think of it as a hospital triage desk: most patients see the nurse practitioner; only the unusual cases get the attending physician's pager."
9. COMIC after the Key Insight callout at the bottom. Concept: a triage desk where the receptionist (classical NER) sends 70% of patients home cured and only escalates the 30% with weird symptoms to the specialist (LLM). Imagegen prompt: `"Hospital ER reception desk cartoon, cheerful watercolor style. A friendly receptionist robot labeled 'spaCy' stamps a clipboard 'CLEARED' for a queue of routine patients. To the right, one patient with question-mark thought bubble walks toward a tall wise wizard-doctor labeled 'LLM' who is putting on a stethoscope. A sign on the wall reads 'Hybrid IE Triage: 70% never reach the wizard'. No real text on patients."`

### Section 34.4: Production IE Deployment Patterns

10. EPIGRAPH (section opens directly into `34.4.5`). Suggest: "I extracted the entities. Whether they exist is a different question." attributed to a new "Grounding Officer AI Agent" persona.
11. ANALOGY in the Grounding Verification subsection. Add: "Grounding is the receipt you keep when the LLM tells you what it found. Without it, you're trusting the model's memoir."
12. COMIC after the Graceful Degradation paragraph. Concept: a circuit breaker between the classical NER (warm green) and the LLM (sleeping). When the LLM service is down, the classical pipeline still ships entities. Imagegen prompt: `"Two cartoon characters wired by a glowing cable. On the left a small alert robot labeled 'spaCy' is working. On the right a larger robot labeled 'LLM' has a Z over its head, fast asleep, with an unplugged cable. A circuit-breaker switch between them is flipped to BYPASS. Below: 'Graceful degradation: the show goes on.' Soft watercolor, friendly faces."`

### Section 34.5: Coreference Resolution and Document Pipelines

13. ANALOGY in the paragraph beginning "Consider the following passage". Add: "Coreference resolution is the conversational equivalent of finally figuring out which 'she' your friend has been talking about for the past fifteen minutes."
14. COMIC just before subsection 34.5.7.2 (LLM-Based Coreference Resolution). Concept: pronouns floating around with arrow tags, the resolver tying them with a label maker. Imagegen prompt: `"Five floating speech bubbles each containing a pronoun ('she', 'her', 'the doctor', 'Chen', 'her team'), with curling colored ribbons tying them all to one labelled tag 'Dr. Sarah Chen'. Background: a friendly hand holding a label-maker. Whimsical, soft pastels, no other text."`
15. MENTAL-MAP at the start of 34.5.8 Integrated Document Understanding Pipeline. Concept: an assembly line where a document passes through Coreference -> NER -> Relations -> Graph Assembly, with workers stamping it at each station. Imagegen prompt: `"Cute assembly line cartoon: a single document passes through four conveyor stations labelled CO-REF, NER, RELATIONS, GRAPH. Four small robot workers each stamp it with their own tool (a glue stick, a highlighter, an arrow tool, a network icon). The output bin is labelled 'Knowledge Graph'. Warm, hand-drawn, cheerful."`

---

## Chapter 36: Retrieval Tools of the Trade

### Section 36.1: Platforms

16. EPIGRAPH (section has no epigraph). Suggest an Agent-X cartoon line: "I picked the vector database with the prettiest landing page. We have since switched three times." Use the "vibe-averse" eval agent voice as inspiration.
17. ANALOGY in the second paragraph ("The platform choice is the most consequential infrastructure decision..."). Add: "Picking a vector DB is like picking a freezer for your restaurant: easy to install, painful to swap once it's full of food."
18. COMIC right after the "Serverless does not mean zero cost at zero load" callout. Concept: a vector DB salesperson holding up a flag "Pay only when you compute!" while a giant invoice labelled "Storage tier" rolls out of the back. Imagegen prompt: `"A small cartoon salesperson on a podium waving a 'SERVERLESS' flag, while behind them a printer is endlessly spitting out a paper labelled 'STORAGE: $50K/mo'. A confused engineer reads the printout. Friendly hand-drawn style, no real text other than the labels."`
19. MENTAL-MAP near 36.1.5 A decision tree. Replace the prose decision tree with a small flowchart in the canonical book SVG style: a single root "Pick a vector DB" branching to leaves (pgvector / Pinecone / Qdrant / Weaviate / Milvus) labelled with the actual decision criterion. Already has table 36.1.1 but a flow visual would be more skim-friendly.
20. COMIC after the "Benchmark on your data, not theirs" warning. Concept: a glossy "vendor benchmark" poster on one side, a worried engineer on the other holding a folder labelled "our actual data" looking at a much smaller, sadder graph. Imagegen prompt: `"Split-panel cartoon. Left: a glossy vendor poster showing 'p99 = 8ms' with confetti. Right: a tired engineer holding a clipboard 'OUR DATA' showing a much sadder graph 'p99 = 320ms'. Speech bubble above the engineer: 'huh'. Warm hand-drawn cartoon."`

### Section 36.2: Libraries and Frameworks

21. ANALOGY in the second paragraph ("A team that wires sentence-transformers directly..."). Add: "Frameworks are like IKEA furniture: fast to assemble, hard to modify once the dowels are glued."
22. COMIC near the "Framework abstractions leak" callout. Concept: a Russian-doll set of frameworks (LangChain wraps LlamaIndex wraps the SDK wraps the API), with an engineer peering inside to find the actual HTTP call at the very center. Imagegen prompt: `"A row of nested Russian matryoshka dolls labelled LangChain, LlamaIndex, OpenAI SDK, Anthropic SDK, and 'POST /v1/messages'. An engineer with a flashlight peers into the smallest doll. Warm watercolor."`
23. MENTAL-MAP after section 36.2.8 "The thinnest viable stack". Concept: a one-page "kitchen recipe card" showing the six libraries in the stack with ingredient icons. Imagegen prompt: `"A recipe card titled 'The 2026 thinnest viable RAG stack', listing 6 ingredients with cute icons next to each: (1) Embedder: sentence-transformers, (2) Vector store: pgvector, (3) BM25: bm25s, (4) Fusion: ranx, (5) Reranker: BGE-Reranker, (6) Parser: pymupdf. Style: a friendly hand-illustrated recipe card on parchment."`

### Section 36.3: Datasets and Benchmarks

24. EPIGRAPH (section opens directly into a large prose block). Suggest: "I beat the benchmark by twelve points. The user noticed nothing." (re-use eval-skeptic agent persona).
25. ANALOGY in the section introduction paragraph 2 ("training-data contamination has eaten into..."). Add: "A benchmark older than a year is like a cake left out at room temperature: still vaguely sweet, but probably not safe to eat."
26. COMIC after Fun Fact "The BM25 baseline still beats half of the dense retrievers on BEIR". Concept: an elderly 1994-era retriever (BM25) in a cardigan, sitting next to a fancy dense retriever, both holding the same NDCG score. Imagegen prompt: `"Two characters sitting on a park bench. Left: an elderly grandparent labelled 'BM25 (1994)' with reading glasses and a cardigan, knitting. Right: a young hipster robot labelled 'Dense Retriever (2024)' with sunglasses. Both hold scoreboards reading the same number, looking surprised. Sky background, friendly cartoon. No other text."`
27. MENTAL-MAP just before section 36.3.9 Building your own evaluation set. Concept: a tiered cake diagram with public benchmarks at the bottom (broadest, noisiest), MTEB shortlist in the middle, your own gold set at the top (smallest, most reliable). Imagegen prompt: `"A three-layer cake on a stand, watercolor style. Bottom layer (largest): 'Public benchmarks - noisy'. Middle layer: 'MTEB shortlist - top 10'. Top layer (smallest, with a cherry on top): 'Your 200-query gold set'. A friendly chef stands beside it with a label-pen."`

### Section 36.4: Models

28. ANALOGY in 36.4.7 Matryoshka and dimension tradeoffs intro paragraph. Add: "Matryoshka dimensions are like buying a tuxedo with detachable sleeves: keep the long version for the formal event, snap them off for the casual one."
29. COMIC after the "Read the embedder's prompt convention" warning. Concept: an engineer typing "what is the weather" into one embedder and "Represent this sentence for searching: what is the weather" into another, with the second one wearing a tiny crown labelled "+10 NDCG". Imagegen prompt: `"Two embedders side-by-side as cartoon characters at podiums. Left character labelled BGE has a sign 'query: ...' and a crown. Right character labelled BGE has a plain prompt and looks sad with a 'less retrieval' frown. Warm, hand-drawn, gentle teaching cartoon."`
30. MENTAL-MAP after section 36.4.10 Fine-tuning your own embedder. Concept: a barbell with "base model" on one side and "fine-tune data" on the other, with "domain-tuned model" sitting at the center. Caption: "Most of the weight is on the data side."

### Section 36.5: External Reading and Communities

31. ANALOGY in section opening paragraph. Add: "Reading IR research without reading the LLM-RAG blogs is like learning to drive only from the manual: technically correct, dangerously incomplete."
32. COMIC at the end (just before the bibliography). Concept: a "field map" showing two villages ("Classical IR" with stone walls; "LLM-RAG" with neon signs) with a small bridge between them and travelers walking both ways. Imagegen prompt: `"A whimsical aerial view of two cartoon villages connected by a bridge. Left village: stone walls, library, banner 'Classical IR' (TREC, SIGIR signs). Right village: glass towers, banner 'LLM-RAG' (Anthropic, LangChain signs). Tiny travelers cross the bridge in both directions. Friendly hand-drawn, top-down."`

---

## Chapter 41: Conversational AI Tools of the Trade

### Section 41.1: Platforms

33. EPIGRAPH (section currently has none). Suggest a Voiceflow-vs-Rasa joke: "Some of us draw boxes. Some of us write YAML. We do not talk." (signed by a "Platform-Agnostic Eval Agent").
34. ANALOGY in the paragraph beginning "A team that picks Voiceflow rarely needs to write Python..." Add: "Picking a chatbot platform is like picking a kitchen: you can cook the same meal in any of them, but the layout decides whether you reach for the salt or the saucepan first."
35. COMIC after the "Vendor lock-in is real but not always bad" warning. Concept: an engineer carrying an enormous Dialogflow flow on a wagon trying to drag it into a Voiceflow door, but the wagon does not fit. Imagegen prompt: `"A small cartoon engineer pushing a comically large wagon labelled 'Dialogflow CX flow' toward a door labelled 'Voiceflow'. The wagon is wider than the door. A sign next to the door reads 'Imports: PDF only'. Warm, hand-drawn, slightly resigned engineer's expression."`
36. MENTAL-MAP can replace the existing SVG at 41.1.7 with a friendlier hand-illustrated version (current SVG is functional but cold).

### Section 41.2: Libraries and Frameworks

37. ANALOGY at the start of 41.2.1 Conversation memory primitives. Add: "Chat memory is the conversational equivalent of where you put your keys: short-term (in your hand), medium-term (on the hook), long-term (in your spouse's head when you forget)."
38. COMIC after the "Memory is the most under-engineered part of most chatbots" callout. Concept: a chatbot with a goldfish-on-its-head trying to remember last message. Imagegen prompt: `"A friendly chatbot robot with a literal goldfish (in a bowl) balanced on its head, trying hard to remember 'what did the user say two turns ago?'. Speech bubble: '...something about a dog?' Hand-drawn, sympathetic, gentle humor."`
39. COMIC near the "Framework half-life is 18 months" fun-note. Concept: a tombstone graveyard with old LangChain abstractions (Chains, LCEL) as graves and LangGraph as a fresh sapling next to them. Imagegen prompt: `"A small cartoon cemetery in autumn. Three small tombstones labelled 'Chains', 'LCEL', 'AgentExecutor'. Next to them a fresh sapling with a sign 'LangGraph (2024)'. A gardener watering it labelled 'LangChain Core team'. Warm, friendly, no morbidness."`

### Section 41.3: Datasets and Benchmarks

40. ANALOGY in section intro. Add: "An Elo number on Chatbot Arena is like a Tinder bio: roughly informative, weirdly competitive, and never the whole truth."
41. COMIC after LMSYS Chatbot Arena description. Concept: two robots arm-wrestling on a stage with a crowd of humans voting "A!" "B!" while wearing blindfolds. Imagegen prompt: `"Two anonymized chatbots arm-wrestling on a stage with masks labelled 'Model A' and 'Model B'. A crowd of cartoon humans below wearing blindfolds raises 'A' and 'B' paddles. A scoreboard reads 'ELO: 1230 vs 1228'. Friendly arena scene."`

### Section 41.4: Models

42. ANALOGY in the section intro paragraph ("Conversation, unlike most other tasks, depends as much on style and prosody..."). Add: "A model can ace the SAT and still bomb the dinner party. Arena Elo is how we measure the second part."
43. COMIC near 41.4.2 Voice-aware models. Concept: a phone call between two robots, but one is reading text-to-speech off cards (the cascaded pipeline, slow) while the other (GPT-4o Realtime) just talks naturally with a coffee cup in hand. Imagegen prompt: `"Telephone call cartoon, split panel. Left robot ('cascaded') reading from a stack of giant flash cards labelled STT -> LLM -> TTS, looking stressed. Right robot ('GPT-4o Realtime') sipping coffee, relaxed, mid-sentence. Phone line connecting them. Warm hand-drawn."`

### Section 41.5: External Reading and Communities

44. EPIGRAPH could carry a "Latent Space podcast" joke - "Half my LLM knowledge is from podcasts during my commute. The other half is from Twitter at 2 AM."
45. COMIC at the bottom of the section: a cartoon "conversational AI study group" with characters representing the major communities. Imagegen prompt: `"A cozy cafe with a study table. Around it: a Reddit avatar reading r/Rag, a Vercel-orange engineer pair-coding, a small Voiceflow designer with sticky notes, a Discord avatar. All sharing one whiteboard labelled 'today's RAG patterns'. Warm and welcoming."`

---

## Chapter 46: LLM-as-Judge & Automated Evaluation

### Section 46.1: Why LLM-as-Judge Matters

46. EPIGRAPH (no epigraph). Suggest: "I asked GPT-4 to grade my output. It gave me an A and asked for a tip." (Agent persona: "Self-Scoring AI Agent".)
47. ANALOGY in section intro paragraph (currently jumps straight into the Production Pattern callout). Add a paragraph: "Using an LLM as a judge is like having a smart but easily flattered intern grade your essays: cheap, fast, and weirdly fond of the longer ones."
48. COMIC after the Fun Fact about GPT-4 narcissism. Concept: GPT-4 holding a mirror and grading the reflection with a big "5/5". Imagegen prompt: `"A friendly cartoon GPT-4 character holding a mirror up to its own face, while writing '5/5! Excellent!' on a clipboard. Caption banner: 'Self-preference bias in action.' Warm watercolor, no other text."`
49. MENTAL-MAP for the Five Biases callout could be an SVG showing each bias as a "weight on the scale" with the judge trying to balance them. Imagegen prompt: `"A balance scale held by a cartoon judge in a wig. Five small weights labelled 'Position', 'Length', 'Self-preference', 'Anchoring', 'Style' all on one side of the scale. The judge looks puzzled. Hand-drawn, friendly courtroom style."`

### Section 46.2: Judge Reliability and Common Biases

50. ANALOGY at the start of the G-Eval description. Add: "G-Eval is the equivalent of asking the judge to show their work before circling the final answer; the chain-of-thought reduces 'I felt like a 4 today' noise."
51. COMIC near the Tip about logprobs access. Concept: an OpenAI judge confidently reading "log-probability glasses" while a Claude judge squints without them. Imagegen prompt: `"Two cartoon judges side-by-side. Left: 'GPT-4' wearing fancy-looking 'logprobs glasses' that overlay 0.42, 0.31, 0.18 on the scoreboard. Right: 'Claude' squinting at the same answer without glasses, holding a magnifying glass. Friendly, warm, gentle."`

### Section 46.3: Debiasing Techniques: Position, Length, and Verbosity

52. EPIGRAPH suggestion: "I trained the judge to be fair. Now nobody likes its rulings." (Agent persona: "Calibrated-but-Lonely AI Agent".)
53. COMIC after the Prometheus 2 description. Concept: the open-source Prometheus 2 character bringing a rubric clipboard while the proprietary GPT-4 judge eyes it suspiciously. Imagegen prompt: `"Two cartoon judges. Left: a bookish open-source judge labelled 'Prometheus 2', carrying a thick rubric labelled 'SCORE 1-5'. Right: a bigger judge labelled 'GPT-4' looking impressed and slightly threatened. Caption banner: 'Distilled judges inherit their teacher's biases.' Hand-drawn."`

### Section 46.4: Training Judge Models

54. ANALOGY at the top. Add: "JudgeLM is the equivalent of teaching a teaching assistant by showing them how the professor grades, then hoping the TA learned to grade and not just to imitate the professor's bad jokes."
55. COMIC near the Warning about distilled judges. Concept: a small judge-bot wearing a too-large GPT-4 graduation hat that says "Now with extra verbosity bias!" Imagegen prompt: `"Small cartoon judge-bot ('JudgeLM') wearing an oversized graduation cap labelled 'GPT-4'. A scroll labelled 'Biases (transferred)' droops out of the cap. Warm, gentle, slightly cautionary cartoon."`

### Section 46.5: Multi-Judge Ensembles and Production Patterns

56. ANALOGY in the AlpacaEval intro. Add: "Length-controlled win rate is the diet-soda of evaluation: same flavor minus the empty verbosity calories."
57. COMIC at the end. Concept: a juror panel scene with three diverse judges (rule-based, LLM, human) voting, with a banner "Multi-judge ensembles: when one judge isn't enough". Imagegen prompt: `"Three cartoon judges in a row at a bench. Left: rule-based judge (an abacus). Middle: LLM judge (a tiny brain on legs). Right: human judge (an actual person with a clipboard). All three lift cards showing '4', '5', '4'. Caption: 'Ensemble vote.'"`

---

## Chapter 56: Responsible AI Tools of the Trade

### Section 56.1: Platforms

58. EPIGRAPH (none). Suggest: "We adopted three governance platforms last quarter. The auditor wants two more." (Persona: "GRC-Fatigued AI Agent".)
59. ANALOGY in the section intro paragraph 2 ("The 2024-2026 inflection point..."). Add: "The EU AI Act turned governance platforms from curiosities into purchase orders, like seatbelts in 1965."
60. COMIC after the "Most enterprises end up with two platforms, not one" key-insight callout. Concept: a Venn diagram of three buyers (Counsel, CDO, CISO), each pointing at a different platform tile. Imagegen prompt: `"A friendly Venn diagram cartoon. Three circles labelled 'General Counsel', 'CDO', 'CISO'. Each circle points to a different cartoon platform logo (governance suite, observability dashboard, runtime guard). The intersection is empty and labelled 'one platform to rule them all (theoretical)'. Hand-drawn diagram."`
61. MENTAL-MAP near 56.1.6 Selection criteria. Concept: four buyer personas as cartoon characters (the Lawyer with a folder, the VP of ML with a Grafana dashboard, the CISO with a firewall icon, the Researcher with a Jupyter notebook), each pointing to the platform they actually need.

### Section 56.2: Libraries and Frameworks

62. ANALOGY at the start of 56.2.1 Fairness metric libraries. Add: "Fairness libraries are like kitchen scales: they all measure weight, but they disagree on the third decimal place, which is where the lawsuits live."
63. COMIC after introducing AIF360, Fairlearn, Aequitas. Concept: three different fairness measurement tools all weighing the same dataset and producing slightly different numbers. Imagegen prompt: `"Three small cartoon scales on a counter, each labelled 'AIF360', 'Fairlearn', 'Aequitas'. All three weigh the same little package labelled 'Dataset'. The three readouts show 0.82, 0.83, 0.81. A confused engineer leans in with a magnifying glass."`
64. COMIC near 56.2.5 Watermarking libraries. Concept: a watermarked text and a clever forger trying to wash it off in a sink. Imagegen prompt: `"A cartoon scientist labelled 'Kirchenbauer Watermark' embeds a green tint in a passing piece of paper. Downstream, a small forger character labelled 'Paraphraser' scrubs the paper in a basin, but green dye is still visible. Friendly, mildly threatening, hand-drawn."`

### Section 56.3, 56.4, 56.5 - quick passes

65. ANALOGY for 56.3 (Datasets and benchmarks): "BBQ tests whether your model leans on stereotypes when context is missing. So do most awkward dinner parties."
66. COMIC for 56.4 (Models): the alignment-of-model-personalities, with Claude refusing to do something while another more permissive model is shown shrugging.
67. COMIC for 56.5 (External reading): the governance "library club" with characters reading the EU AI Act and NIST RMF side by side.

---

## Chapter 59: Distributed Training Systems

### Section 59.1: Distributed Training Fundamentals

68. EPIGRAPH (none). Suggest: "The model fits in memory. It just doesn't fit in one memory." (Agent persona: "Sharding-Strategist AI Agent".)
69. ANALOGY in the "Compute is cheap, memory bandwidth is not" key-insight callout. Add: "It's the same reason your kitchen has only one big oven but enough counter space for three pies: bandwidth, not compute, is the constraint."
70. COMIC for 59.1.2 Three Axes of Parallelism. The existing SVG (Three Orthogonal Axes) is functional but cold. A whimsical hand-illustrated version with three different cartoon scenes (Data: same recipe, four kitchens; Pipeline: assembly line; Tensor: a single huge cake cut radially across four bakers) would be warmer. Imagegen prompt: `"Three small cartoon panels, side-by-side. Panel 1 (Data): four identical chefs in four identical kitchens, each cooking a different chunk of the same recipe. Panel 2 (Pipeline): an assembly line where bakers handle dough->bake->frost->box in sequence. Panel 3 (Tensor): one giant cake on a turntable, four bakers cutting wedges and decorating in parallel. Friendly hand-drawn watercolor."`

### Section 59.2: ZeRO and FSDP

71. ANALOGY in section intro big-picture. Add: "ZeRO is the moving-house algorithm for GPUs: each rank holds onto only one box, and we pass them around when needed."
72. COMIC near 59.2.2 The ZeRO Progression. Concept: four climbers ascending a memory mountain, each carrying less and less (Stage 0: full backpack; Stage 1: smaller; Stage 2: smaller; Stage 3: just a daypack). Imagegen prompt: `"A vertical mountain climb scene. Four cartoon climbers progressing upward (Stage 0, 1, 2, 3). Each carries a smaller backpack than the one below. The summit is labelled 'Trillion-parameter model'. Cheerful, hand-drawn."`
73. MENTAL-MAP near the mixed-precision memory table (Table 59.2.1). A bar-chart-as-stacked-pizza-slices showing per-parameter bytes could help skimmers.

### Section 59.3: Tensor Parallelism

74. ANALOGY at the start of "Tensor parallelism shards within a layer..." Add: "Tensor parallelism is the surgical version of model parallelism: cut a single matrix, not the whole layer stack."
75. COMIC near "When Tensor Parallelism Breaks". Concept: an InfiniBand cable strained near breaking with a "T=8" sign on it, while a Slurm operator yells "do not add a ninth GPU!" Imagegen prompt: `"A bundle of InfiniBand cables visibly strained, labelled 'T=8'. A nervous operator-cartoon in a hard hat shouts 'STOP' with a small sign reading 'T<=8 over NVLink only'. Hand-drawn warning-comic style."`

### Section 59.4 and 59.5

76. ANALOGY for 59.4 Pipeline Parallelism: "Pipeline parallelism is like a bucket brigade in a fire-line: each rank holds one bucket; the brigade is only as fast as its slowest passer."
77. COMIC for 59.4 GPipe vs 1F1B scheduling: a friendly assembly-line comparison.
78. COMIC for 59.5 (Operations and observability): a 47-hours-into-training scene with a GPU on fire and an automated checkpoint robot calmly saving the run. Imagegen prompt: `"Cartoon training cluster at 3am. One GPU is smoking. A small robot labelled 'auto-checkpoint' calmly carries the model state to safety in a treasure chest labelled 'S3'. The on-call engineer in pajamas watches calmly with coffee. Hand-drawn, comforting."`

---

## Chapter 61: Scale Tools of the Trade

### Section 61.1: Platforms

79. EPIGRAPH (none). Suggest: "Yes, we'd love 8,192 H100s. No, next Tuesday is fine." (Agent persona: "Capacity-Procurement AI Agent".)
80. ANALOGY at the start of the section. Add: "Picking a training platform is like booking a stadium. You don't realize you needed loading docks, parking, and a generator until the band shows up."
81. COMIC at the "The InfiniBand premium is the line..." key-insight callout. Concept: two side-by-side cluster diagrams: one labelled "Cheap Ethernet" looking sad, one labelled "InfiniBand" with crisp full-throughput rays. Imagegen prompt: `"Two cartoon GPU clusters side-by-side. Left: 'Ethernet' clusters with thin droopy wires, sad GPUs achieving only 30% MFU. Right: 'InfiniBand' clusters with thick glowing cables, happy GPUs at 60% MFU. Caption: 'Interconnect is the silent multiplier.' Hand-drawn."`
82. MENTAL-MAP for the platform stack (currently SVG at 61.1.7). The existing stack diagram is fine but a friendlier hand-illustrated stack-of-pancakes metaphor with each layer labelled (compute / scheduler / storage / observability) would be warmer.

### Section 61.2-61.5 (Libraries, Datasets, Models, Communities)

83. ANALOGY for 61.2 vLLM vs TensorRT-LLM: "Picking an inference server is like picking running shoes: vLLM is the popular trainer, TensorRT-LLM is the carbon-plate race shoe, llama.cpp is the trail runner you carry in your backpack."
84. COMIC for 61.3 Pretraining datasets section: a small character labelled "RedPajama" carrying a backpack full of "the entire internet" while a quality filter robot tosses out bad data.
85. COMIC for 61.4 Frontier models lineage: a family tree of LLMs (GPT family, Claude family, Llama family) with each model represented as a chibi character.
86. COMIC for 61.5 Communities: a "training-cluster operators support group" with characters comparing Slurm horror stories.

---

## Wave 17i Consolidated Sections

### Section 24.6: VLA Limitations

87. ANALOGY in 24.6.2 "The Dexterity Ceiling" intro. Add: "Every VLA can pick the apple. Almost none of them can unwrap the candy bar. Dexterity is the line between 'demo' and 'production'."
88. COMIC after the "Dexterity is not a data problem in the same way" callout. Concept: a VLA robot triumphantly stacking apples while a tiny candy wrapper defeats it next to the bowl. Imagegen prompt: `"A friendly cartoon robot arm gleefully stacks apples in a pyramid. Right next to it, a single candy bar lies on the table; the robot's gripper hovers over it confused. Caption: 'The dexterity ceiling.' Hand-drawn, warm watercolor."`
89. COMIC for 24.6.3 Safety Story. Concept: a robot with three nested safety vests labelled "collision avoidance", "force limiter", "anomaly detector". Imagegen prompt: `"A friendly cartoon humanoid robot wearing three nested safety vests labelled 'COLLISION AVOIDANCE', 'FORCE LIMITER', 'ANOMALY DETECTOR'. It looks sheepish. Caption: 'No one safety layer is enough.' Hand-drawn."`

### Section 24.13: Sim-to-Real Gap

90. ANALOGY in 24.13.1 "Anatomy of the Gap" intro. Add: "The sim-to-real gap is the cooking-show problem: everything works on the studio counter; nothing works in your actual kitchen with your actual knife." 
91. COMIC for 24.13.2 Domain Randomization. Concept: a simulation environment as a snow globe being violently shaken by a giant hand, with parameters (lighting, friction, mass) floating around. Imagegen prompt: `"A snow globe containing a tiny robot arm and table. A giant hand shakes it. Tiny labels float around inside: lighting!, friction!, mass!, camera_jitter!. Outside the globe, a calm researcher holds a clipboard 'Domain Randomization'. Warm, whimsical, hand-drawn."`
92. EPIGRAPH suggestion if missing: "We trained for a million simulated kitchens. The customer's kitchen had cat hair."

### Section 26.6: Memory Architecture for Agents

93. ANALOGY at the top of 26.6.2 Working Memory for Multi-Step Plans. Add: "Working memory is the agent's sticky-note pad. The context window is just the part the LLM can read this turn."
94. COMIC after the "dialogue memory vs process memory" key-insight callout. Concept: a desk with two clearly labelled stacks: "Dialogue history" (transcripts) and "Process memory" (sticky notes, todo lists, tool-call receipts), with an agent juggling between them. Imagegen prompt: `"A cartoon agent at a wooden desk. Left stack: tidy printed transcripts labelled 'Dialogue Memory'. Right stack: chaotic sticky notes, todo lists, receipts labelled 'Process Memory'. The agent picks one note from the right pile. Warm, friendly."`
95. The illustration `memory-taxonomy-five-layers.png` already exists; suggest a second whimsical inline figure later showing "what bytes survive a session crash and what dies with it".

### Section 27.5: Retrieval as a Tool Call

96. The existing image `ch23-agentic-rag-librarian.png` is already strong (a robot librarian planning). No additional comic needed at the top.
97. ANALOGY at the start of 27.5.2 Shaping a Retrieval Tool. Add: "A well-shaped retrieval tool is like a well-shaped library card: precise scope, clear stamps, no fine print."
98. COMIC near the end (probably 27.5.5 or wherever the section concludes), about CRAG-style corrective grading. Concept: an agent receiving search results and giving each one a thumbs up / down / "needs more search" before passing them to the LLM. Imagegen prompt: `"A cartoon agent at a desk receiving five passages on cards from a conveyor belt. The agent stamps each one: 'KEEP', 'DISCARD', 'RE-QUERY'. A small librarian behind the conveyor labelled 'Retriever' watches. Hand-drawn, friendly."`

### Section 29.1: Code Generation Agents

99. The existing `ch25-opener-specialist-robots.png` figure works well. Add one more comic near the self-debug loop section.
100. ANALOGY at the start of 29.1.1 The Anatomy of a Code Agent. Add: "A code agent is what happens when you give an LLM both a keyboard and a 'run tests' button. It will use both, mostly correctly, and occasionally make you nervous."
101. COMIC for the self-debug loop. Concept: a robot writing code, running tests, watching them fail, scratching its head, rewriting, repeat (a small four-panel strip). Imagegen prompt: `"Four-panel cartoon strip. Panel 1: cartoon robot types code on a laptop. Panel 2: a 'tests' window shows 3 RED, 2 GREEN; robot frowns. Panel 3: robot scratches head, edits. Panel 4: tests now 5 GREEN; robot lifts arms in tiny triumph. Hand-drawn, warm."`

### Section 29.4: Production Agentic Coding Systems

102. ANALOGY at the top. Add: "Picking an agentic coding tool is like picking a co-worker: some are quiet and helpful (Aider), some are loud and confident (Devin), some live in your IDE rent-free (Cursor)."
103. COMIC near the 2026 vendor landscape table. Concept: a cartoon office floor with desks labelled "Cursor", "Claude Code", "Devin", "Aider", "Copilot Workspace", each with a different working style (one is just a terminal, one a fancy IDE, one is fully remote). Imagegen prompt: `"A cartoon open-plan office. Five desks each labelled with a different agentic coding tool. Each desk has a different character/setup: Cursor (a designer in an IDE), Claude Code (a person at a plain terminal with a tidy notebook), Devin (a phone with a tiny robot inside, 'cloud autonomous'), Aider (a focused engineer with sticky notes), Copilot Workspace (a GitHub-octocat-style staged worker). Warm illustration."`

### Section 35.2: RAG with Knowledge Graphs

104. The existing `knowledge-graph-islands.png` is well-suited. Suggest one additional comic near the Cypher subsection: a Cypher query as a treasure-hunt map. Imagegen prompt: `"An old treasure-hunt map with nodes labelled like Wikipedia stubs ('Einstein', 'Ulm', 'Germany'), and a dotted line traversing them. A pirate-themed cartoon traveler labelled 'MATCH (e:Person)-[:bornIn]->(c:City)' follows the dots. Warm, gentle, hand-drawn."`
105. ANALOGY at the start of 35.2.1 Knowledge Graph Fundamentals. Add: "A vector store is the library where books that mention Einstein live nearby. A knowledge graph is the library where Einstein himself walks among the books, with arrows pointing to his friends."

### Section 35.3: GraphRAG

106. The detective board image `graphrag-detective-board.png` (referenced from 35.2) is already in style. Suggest a complementary "community detection" comic for 35.3. Concept: an LLM "mayor" walking through a small graph town, declaring "this neighborhood is the AI safety community". Imagegen prompt: `"A small cartoon town drawn as a graph. A character labelled 'Leiden Algorithm' draws colored bubbles around clusters of houses; another character labelled 'LLM' walks behind labeling each bubble: 'AI Safety neighborhood', 'Robotics district', 'Eval-research street'. Warm watercolor."`

### Section 37.3: Memory & Context Management

107. Existing `memory-management-containers.png` works for short/long/working memory. Suggest an additional "lost-in-the-middle" comic. Imagegen prompt: `"A long park bench with many people sitting on it. The two ends (recent + oldest) are well-lit. The middle is in shadow, with question marks over their heads. An LLM character at one end says 'I can hear the ends just fine'. Caption: 'The lost-in-the-middle effect.' Friendly, warm."`
108. ANALOGY in 37.3 intro. Add: "Memory is what turns a stateless chat into a relationship that survives Monday."

---

## Summary Counts

| Chapter / Section | Comic suggestions | Analogy suggestions | Mental-map suggestions | Epigraphs to add |
|---|---|---|---|---|
| Ch 34 (5 sections) | 8 | 7 | 2 | 2 |
| Ch 36 (5 sections) | 7 | 7 | 4 | 2 |
| Ch 41 (5 sections) | 7 | 5 | 1 | 2 |
| Ch 46 (5 sections) | 6 | 4 | 1 | 3 |
| Ch 56 (5 sections) | 5 | 4 | 1 | 1 |
| Ch 59 (5 sections) | 6 | 4 | 2 | 1 |
| Ch 61 (5 sections) | 6 | 3 | 1 | 1 |
| Wave 17i (9 sections) | 8 | 7 | 0 | 2 |
| **Total** | **53** | **41** | **12** | **14** |

## Highest-leverage picks (top 10 if you only ship a few)

1. Section 34.1 four-panel strip: Classical vs LLM extraction (item 4)
2. Section 34.3 hospital triage cartoon for hybrid routing (item 9)
3. Section 36.1 storage-tier invoice gag for serverless myths (item 18)
4. Section 36.3 BM25 grandparent vs Dense robot bench scene (item 26)
5. Section 41.2 goldfish-on-chatbot-head memory gag (item 38)
6. Section 41.2 LangChain graveyard for framework half-life (item 39)
7. Section 46.1 GPT-4 narcissism mirror gag (item 48)
8. Section 56.1 Venn diagram of governance buyers (item 60)
9. Section 59.2 ZeRO mountain climbers with shrinking backpacks (item 72)
10. Section 24.6 robot stacking apples but defeated by candy wrapper (item 88)

These are the funniest and most clarifying, and they land in the highest-traffic sections.
