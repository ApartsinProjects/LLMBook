#!/usr/bin/env python3
"""Generate illustration prompts and mapping for all missing textbook images."""

import json
import os

base = "E:/Projects/LLMCourse"
with open(f"{base}/scripts/missing_illustrations.json") as f:
    missing = json.load(f)

# Style prefix for textbook illustrations
TEXTBOOK_STYLE = (
    "Clean, professional textbook illustration in a modern flat design style "
    "with soft gradients, warm color palette (blues, teals, oranges, purples), "
    "no text or labels, suitable for a university-level AI/ML textbook. "
    "16:9 aspect ratio."
)

# Style for agent avatars
AVATAR_STYLE = (
    "Professional circular avatar icon for an AI agent team member, modern flat design, "
    "clean geometric shapes, single character portrait, vibrant color, white background, "
    "suitable for a website team page."
)

prompts = []
mapping = []

# Detailed prompt descriptions for each illustration
prompt_map = {
    "quantization-diet": "A neural network model on a strict diet plan. The model (represented as a large figure) steps onto a scale while a nutritionist recommends cutting bits (binary bits flying off). Weight parameters shrink from large to small. Before: bloated 32-bit model. After: lean 4-bit model that still works. Visual metaphor for model quantization reducing precision to save memory.",
    "speculative-decoding": "A fast junior writer rapidly drafting text on paper while a senior editor reads over their shoulder, checking and approving tokens in batches. The junior produces multiple candidate words quickly; the senior either stamps approved or crosses them out. Visual metaphor for speculative decoding where a small fast model drafts and a large model verifies.",
    "serving-stack-restaurant": "A busy restaurant kitchen serving as a metaphor for ML serving infrastructure. The host (load balancer) seats customers, the kitchen (inference engine) prepares orders, the expeditor (batching system) groups orders efficiently, and servers (API endpoints) deliver responses. Visual metaphor for the LLM serving stack.",
    "api-ecosystem-market": "A colorful outdoor marketplace/bazaar with different vendor stalls, each representing an LLM API provider. Signs show different specialties, pricing models, and capabilities. Developers browse and compare offerings. Visual metaphor for the diverse LLM API marketplace.",
    "api-hotel-receptionist": "A friendly hotel receptionist robot behind a desk helping a guest. The guest describes their request, the receptionist processes it behind the scenes (hidden complexity), and returns a polished response. Keys (API keys) and tokens are exchanged. Visual metaphor for LLM API interaction.",
    "circuit-breaker-pattern": "An electrical circuit breaker panel where some switches have tripped to protect the system. When too many API errors flow through, the breaker trips and diverts traffic. A dashboard shows green/yellow/red states. Visual metaphor for the circuit breaker pattern in API reliability.",
    "multimodal-senses-robot": "A robot being upgraded with new sensory modules: camera eyes for vision, microphone ears for audio, and reading glasses for document understanding. Each sense connects to the central LLM brain via cables. Visual metaphor for multimodal API capabilities.",
    "rate-limit-bouncer": "A nightclub bouncer standing at a velvet rope, checking API request tickets. A long queue of requests waits. The bouncer only lets a certain number through per minute, turning away excess requests. Visual metaphor for API rate limiting.",
    "reasoning-model-thinker": "A robot in Rodin's Thinker pose, sitting on a pedestal made of chain-of-thought reasoning steps. Thought bubbles show intermediate reasoning. A clock indicates the extra time needed for deliberation. Visual metaphor for reasoning models that take time to think through problems.",
    "retry-backoff-trampoline": "A person bouncing on a trampoline, each bounce going higher and waiting longer between bounces. The first bounce is quick and low, the second higher and longer, the third even more so. Numbers (1s, 2s, 4s, 8s) mark the wait times. Visual metaphor for exponential backoff retry strategy.",
    "semantic-caching": "A library with a smart filing system. When a new question arrives, a librarian checks if a nearly identical question was already answered (shown as similar books on a shelf). If found, the cached answer is returned instantly from the shelf instead of generating a new one. Visual metaphor for semantic caching of API responses.",
    "streaming-sse-conveyor": "A factory conveyor belt delivering tokens one by one to a waiting customer. Each token arrives as a small package on the belt. The customer can start reading/using early tokens while later ones are still being produced upstream. Visual metaphor for streaming Server-Sent Events.",
    "structured-output-mold": "Liquid, free-form model output being poured into a precise JSON-shaped mold or cookie cutter. The liquid takes the exact shape of the schema: proper fields, types, and structure. Visual metaphor for structured output formatting.",
    "tool-use-swiss-army": "A Swiss army knife where each fold-out tool is a different capability: calculator, web browser, database query, code executor, calendar. The LLM is the handle that coordinates which tool to deploy. Visual metaphor for LLM tool use.",
    "chain-of-thought-math-test": "A student working through a math problem step by step on a whiteboard, showing their work at each stage rather than jumping to the answer. Each step builds on the previous one with arrows connecting them. Visual metaphor for chain-of-thought prompting.",
    "meta-prompt-inception": "An Inception-style nested scene: a prompt writing another prompt, which writes another prompt. Russian nesting dolls or recursive mirrors show the meta-prompting concept. Each layer generates instructions for the next layer. Visual metaphor for meta-prompting.",
    "prompt-chaining-relay": "A relay race where runners (prompts) pass batons (intermediate outputs) to the next runner. Each leg of the race processes one step of a complex task. The final runner crosses the finish line with the complete result. Visual metaphor for prompt chaining.",
    "prompt-injection-defense": "A medieval castle with multiple layers of defense: outer walls (input validation), moat (content filtering), inner walls (output checking), and a guarded throne room (the system prompt). Attackers try various approaches but are repelled. Visual metaphor for defending against prompt injection.",
    "prompt-injection-trojan": "A wooden Trojan horse being wheeled toward a castle gate, but instead of soldiers inside, it contains malicious prompt instructions hidden within innocent-looking user input. Guards inspect the horse suspiciously. Visual metaphor for prompt injection attacks.",
    "prompt-template-madlibs": "A Mad Libs game card with blanks to fill in, but instead of nouns and verbs, the blanks are labeled context, task, format, examples. A pencil fills in the blanks to create a complete prompt. Visual metaphor for prompt templates.",
    "prompting-strategies-students": "A classroom with different students using different study strategies: one wings it (zero-shot), one looks at example problems (few-shot), one writes detailed notes step-by-step (chain-of-thought). Each approach has a different effectiveness meter. Visual metaphor for prompting strategies.",
    "reflection-loop": "A circular workflow diagram: Generate (pen writing), Critique (magnifying glass examining), Refine (polishing cloth), Repeat (circular arrow). A piece of text gets better with each loop iteration. Visual metaphor for the reflection/self-critique loop.",
    "self-consistency-jury": "A jury box in a courtroom with multiple identical jurors (model instances), each independently deliberating on the same question. They vote, and the majority verdict is selected. Visual metaphor for self-consistency through majority voting across model outputs.",
    "system-prompt-director": "A film director in a director's chair, holding a megaphone and giving instructions to actors (model responses) on a movie set. The director's script (system prompt) sets the tone, character, and boundaries for the entire performance. Visual metaphor for system prompts.",
    "tree-of-thought": "A large tree where each branch represents a different reasoning path. Some branches lead to dead ends (marked with X), while others reach fruit (correct answers). The model explores multiple paths simultaneously before choosing the best one. Visual metaphor for tree-of-thought reasoning.",
    "zero-vs-few-shot-chef": "Two chefs side by side: one cooking without any recipe (zero-shot, improvising), the other cooking with a few example recipes pinned up on the wall (few-shot, following examples). The few-shot chef produces more consistent dishes. Visual metaphor for zero-shot vs. few-shot learning.",
    "hybrid-pipeline-assembly": "An assembly line with two zones: a fast, precise robotics section (classical ML) handling structured tasks, and a creative artisan section (LLM) handling nuanced language tasks. Products pass between zones seamlessly. Visual metaphor for hybrid ML/LLM pipelines.",
    "latency-cost-race": "A three-way tug-of-war between characters labeled Latency (a sprinter), Cost (a banker), and Quality (an artist). Each pulls in a different direction, and you can only fully satisfy two at once. A trilemma triangle floats above them. Visual metaphor for the latency-cost-quality tradeoff.",
    "ml-vs-llm-toolbox": "An open toolbox with two compartments: one side has precision instruments (classical ML tools like random forests, calipers), the other has creative tools (LLM tools like paint, conversation bubbles, flexible materials). A craftsperson considers which to use. Visual metaphor for choosing between ML and LLM approaches.",
    "active-learning-fishing": "A fisher in a boat on a data lake, strategically choosing which fish (data points) to catch rather than netting everything. A sonar screen shows which areas have the most informative samples. Visual metaphor for active learning: selectively labeling the most valuable data.",
    "data-diversity-spectrum": "A garden with diverse flowers of many colors, shapes, and sizes representing a healthy, diverse dataset. Contrast with a monoculture field of identical flowers (homogeneous data). Visual metaphor for dataset diversity being essential for model robustness.",
    "data-quality-inspector": "A factory quality inspector examining synthetic data samples on a conveyor belt with a magnifying glass. Some pass inspection (green checkmarks), others are rejected (red X marks). Metrics dashboards show quality scores. Visual metaphor for synthetic data quality control.",
    "deduplication-twins": "A lineup of data samples where some are identical twins. A detective with a magnifying glass identifies the duplicates and removes them. The remaining unique samples stand confidently. Visual metaphor for deduplication in dataset cleaning.",
    "evol-instruct-evolution": "An evolution sequence (like the famous ape-to-human march) but with prompts: a simple instruction on the left gradually evolves through stages into a complex, sophisticated instruction on the right. Each stage adds complexity. Visual metaphor for Evol-Instruct.",
    "labeling-sorting-hat": "A magical sorting hat placed on data samples, assigning each one a label/category. Samples sorted into different labeled bins. The hat represents the LLM doing automated labeling. Visual metaphor for LLM-assisted data labeling.",
    "llm-actor-stage": "A theater stage where one LLM actor plays multiple roles: wearing a user hat, then switching to an assistant hat, then an evaluator hat. Costumes and masks hang on a rack. Visual metaphor for LLMs playing multiple roles in synthetic data generation.",
    "llm-assembly-line": "A factory assembly line where raw prompt templates enter one end, pass through LLM processing stations, and polished training examples emerge from the other end. Each station adds quality. Visual metaphor for the LLM generation pipeline.",
    "model-collapse-spiral": "A downward spiral where a model feeds on its own outputs, each generation becoming more distorted and less diverse. Like a photocopy of a photocopy degrading in quality. The spiral gets tighter and more homogeneous. Visual metaphor for model collapse from training on synthetic data.",
    "noisy-labels-orchestra": "An orchestra playing, but a few musicians are clearly playing wrong notes (shown with off-key symbols). Despite the noise, the overall melody remains recognizable because most players are correct. Visual metaphor for noisy labels in training data.",
    "prompt-template-cookie-cutter": "Cookie cutters in various shapes (question, instruction, dialogue) stamping out uniform synthetic data cookies from a sheet of dough. Each cutter produces consistent, shaped outputs. Visual metaphor for prompt templates in synthetic data generation.",
    "quality-filtering-pipeline": "A water treatment pipeline: raw synthetic data flows in (murky water), passes through multiple filter stages (grammar check, factual accuracy, diversity filter, deduplication), and clean, high-quality data flows out. Visual metaphor for quality filtering.",
    "reasoning-chain-dominos": "A line of dominos where each piece has a reasoning step. Pushing the first one triggers a chain reaction through the entire sequence, with each step logically leading to the next. Visual metaphor for reasoning chains in synthetic data.",
    "red-team-boxing-ring": "A boxing ring where two LLM robots spar: one (red corner) tries to generate adversarial, tricky inputs, while the other (blue corner) tries to handle them safely. A referee observes. Visual metaphor for red-teaming with synthetic data.",
    "rejection-sampling-panning": "A gold prospector panning for gold in a stream. Many pebbles (bad samples) wash away while gold nuggets (high-quality samples) remain in the pan. Visual metaphor for rejection sampling: generating many candidates and keeping only the best.",
    "seed-data-garden": "A gardener planting seed examples in fertile soil. Small sprouts grow into diverse plants representing the expanded synthetic dataset. The original seeds are clearly visible at the base. Visual metaphor for seed data as the starting point for synthetic generation.",
    "synthetic-data-factory": "A bustling factory interior where LLM-powered machines produce synthetic training data. Raw materials (seed prompts) enter, robotic arms assemble training examples, quality scanners check outputs. Visual metaphor for industrial-scale synthetic data production.",
    "weak-supervision-jury": "A jury of imperfect labeling functions (shown as jurors with different specialties and biases) voting on data labels. No single juror is always right, but their collective vote is usually correct. Visual metaphor for weak supervision.",
    "catastrophic-forgetting": "A student brain being filled with new knowledge (pouring in through one ear) while old knowledge leaks out (draining from the other ear). The old skills literally crumble as new ones take their place. Visual metaphor for catastrophic forgetting during fine-tuning.",
    "fine-tune-decision-tree": "A forking road/decision tree: at each junction, signs ask Enough data?, Task complexity?, Budget?. One path leads to Just Prompt Better, another to Fine-tune, another to Use RAG. A hiker considers the options. Visual metaphor for the decision of whether to fine-tune.",
    "fine-tuning-old-dog": "A lovable old dog (representing a pre-trained model) sitting in a training class, successfully learning a new trick. Training treats (labeled data) motivate the learning. The dog looks proud of its new ability. Visual metaphor for fine-tuning.",
    "sequence-packing-tetris": "A Tetris game screen where sequences of different lengths are packed tightly together like Tetris blocks, filling the available space efficiently with no gaps. Some blocks are color-coded by sample. Visual metaphor for sequence packing in training.",
    "lora-sticky-note": "A massive reference textbook (the base model) with small colorful sticky notes (LoRA adapters) attached to key pages. The sticky notes add new information without changing the original text. Visual metaphor for LoRA lightweight adaptation.",
    "peft-adapter-accessories": "A mannequin (base model) wearing mix-and-match accessories: adapter bracelets, prompt-tuning necklaces, LoRA earrings. Each accessory adds a new capability without changing the core outfit. Visual metaphor for various PEFT methods as accessories.",
    "qlora-truck-decals": "A compact delivery truck (quantized model) decorated with custom decals and modifications (LoRA adapters). The truck is smaller than a semi but still performs well, and the decals add personality. Visual metaphor for QLoRA: quantization plus adapters.",
    "distillation-chef": "A master chef at a cooking school, carefully demonstrating a complex recipe to an apprentice. The master dish is elaborate (teacher model), but the apprentice learns to capture the essential flavors in a simpler version (student model). Visual metaphor for knowledge distillation.",
    "model-merging-cocktail": "A bartender mixing multiple model cocktails together: different colored liquids (model weights) from different bottles are combined in a shaker. The resulting cocktail has properties of all ingredients. Visual metaphor for model merging techniques.",
    "constitutional-ai-angel": "An AI model with an angel on its shoulder (its constitutional principles). The angel holds a scroll of rules/values. The model consults its moral compass before responding. Visual metaphor for Constitutional AI self-governance approach.",
    "dpo-vs-rlhf-comparison": "A split scene comparing two training approaches. Left: a complex Rube Goldberg machine (RLHF) with reward models, value functions, and PPO. Right: a simple, direct path (DPO) going straight from preference data to the model. Visual metaphor for DPO being simpler than RLHF.",
    "rlhf-talent-show": "A talent show stage with AI model contestants performing. Human judges in the audience rate performances with number cards. The feedback loop: perform, get rated, improve, perform again. Visual metaphor for RLHF human feedback loop.",
    "interpretability-xray": "A doctor examining a neural network brain under an X-ray machine. The X-ray reveals internal structures: attention patterns glowing, feature neurons lighting up, circuit pathways visible. Visual metaphor for interpretability as medical imaging for models.",
    "logit-lens-building": "A cross-section of a tall building (transformer layers) where you can peek through each floor window to see how text representations change. Ground floor shows raw tokens; top floor shows refined predictions. Visual metaphor for the logit lens technique.",
    "superposition-coat-rack": "An overloaded coat rack with far more coats than hooks. Coats overlap and share hooks creatively. Some hooks hold multiple coats. Visual metaphor for superposition: neurons encoding more features than dimensions available.",
    "chunking-baguette": "A baker slicing a long baguette (document) into pieces. Too-thin slices crumble (lose context); too-thick slices are hard to eat (too much for retrieval). The ideal slice is just right. Visual metaphor for document chunking strategies.",
    "chunking-sushi-chef": "A sushi chef making precise cuts at natural boundaries of a fish/roll, each piece perfectly sized. The cuts follow the natural structure rather than arbitrary fixed lengths. Visual metaphor for semantic chunking.",
    "colpali-xray-vision": "A retrieval system wearing X-ray goggles that can see through document layouts: tables, figures, headers, and formatting all become visible as searchable features. Visual metaphor for ColPali vision-based document retrieval.",
    "contrastive-learning-magnets": "A set of magnets on a board: similar pairs (same-colored magnets) attract and cluster together, while dissimilar pairs (different-colored magnets) repel each other. Visual metaphor for contrastive learning pulling similar embeddings together.",
    "embedding-space-party": "A cocktail party in a large room where guests (words/concepts) naturally cluster by topic: science words gather near the bar, art words near the stage, sports words near the dance floor. Similar concepts stand close together. Visual metaphor for embedding space organization.",
    "hnsw-city-navigation": "A city map viewed from above, showing a navigation path: start on the highway (top HNSW layers), exit to local roads (middle layers), then navigate neighborhood streets (bottom layers) to reach the exact destination. Visual metaphor for HNSW graph traversal.",
    "hnsw-express-lanes": "A multi-level highway system where top levels are express lanes with few exits (sparse connections), and lower levels are local streets with many turns (dense connections). A car descends through levels to reach its destination. Visual metaphor for HNSW layer structure.",
    "late-interaction-judges": "A panel of judges (query tokens) each independently scoring different aspects of contestants (document tokens). Each judge focuses on their specialty rather than giving one holistic score. Visual metaphor for late interaction in retrieval models.",
    "matryoshka-embeddings-nesting": "Russian nesting dolls (matryoshka) where the largest doll contains the full embedding, and each smaller doll inside contains a truncated but still useful version. Peeling layers reveals progressively simpler representations. Visual metaphor for Matryoshka embeddings.",
    "metadata-filtering-bouncer": "A bouncer at a venue door checking metadata tickets before letting search results through the velvet rope. Date range? Check. Category? Check. Only matching results pass through to the similarity search stage. Visual metaphor for metadata pre-filtering.",
    "parent-child-retrieval-telescope": "A telescope zooming from a wide view (parent document) to a specific detail (child chunk). The search finds the precise detail, then pulls back to show the surrounding context. Visual metaphor for parent-child retrieval strategy.",
    "product-quantization-paint": "An artist painting with a limited palette of colors. Instead of millions of exact colors, they approximate using combinations from a small set of base colors. The result looks nearly as good but uses far fewer resources. Visual metaphor for product quantization.",
    "vector-db-librarian": "A librarian organizing books not alphabetically but by topic similarity. Books about similar subjects sit on neighboring shelves. When asked a question, the librarian points to the nearest cluster of relevant books. Visual metaphor for vector database search.",
    "advanced-rag-treasure-hunt": "A multi-step treasure hunt where each clue (retrieval step) leads closer to the treasure (answer). The hunter follows a chain of progressively more specific clues. Visual metaphor for advanced/iterative RAG strategies.",
    "graphrag-detective-board": "A detective investigation board with photos, documents, and clues connected by red string. The detective traces connections between entities to solve the case. Visual metaphor for GraphRAG connecting knowledge entities.",
    "hyde-crystal-ball": "A fortune teller peering into a crystal ball to envision a hypothetical answer, then using that vision to search for real evidence. The crystal ball shows a ghostly draft answer that guides the actual retrieval. Visual metaphor for Hypothetical Document Embeddings (HyDE).",
    "knowledge-graph-islands": "An archipelago of knowledge islands connected by bridges. Each island represents an entity (person, place, concept), and bridges represent relationships between them. Ships (queries) navigate the waterways. Visual metaphor for knowledge graphs.",
    "knowledge-graph-subway-map": "A subway/metro map where stations are entities and colored lines are relationships. Travelers hop between stations following routes. The map shows how to navigate from one concept to another through connections. Visual metaphor for navigating knowledge graphs.",
    "lost-in-middle-sandwich": "A sandwich where the bread slices (beginning and end of context) are well-toasted and attended to, but the filling in the middle is neglected and drooping. Eyes focus on the top and bottom but miss the middle. Visual metaphor for the lost-in-the-middle attention problem.",
    "rag-open-book-exam": "A student at an exam desk with an open textbook beside their paper. Before writing each answer, they flip to a relevant page, read the passage, then write a well-informed response. Visual metaphor for RAG as an open-book exam.",
    "rag-open-book-student": "A student in the process of the RAG workflow: (1) receiving a question, (2) searching through books/database for relevant pages, (3) reading the retrieved passages, (4) writing the final answer. A clear sequential flow. Visual metaphor for the RAG retrieval-then-generate workflow.",
    "reranking-judges-panel": "A talent show callback round: initial auditions (first retrieval) produce many candidates, then a panel of expert judges (reranker model) carefully evaluates the finalists and reorders them by quality. Visual metaphor for reranking in RAG.",
    "dialogue-system-receptionist": "A busy hotel receptionist juggling multiple tasks: answering phones, greeting guests, checking reservations, handling complaints, all while maintaining a friendly demeanor. Multiple conversation threads shown as parallel speech bubbles. Visual metaphor for dialogue systems.",
    "memory-management-containers": "A desk with different-sized containers: a small notepad (short-term/buffer memory), a filing cabinet (episodic memory), a reference shelf (semantic memory). The AI assistant accesses each as needed during conversation. Visual metaphor for conversation memory management.",
    "agent-control-room": "A mission control room with screens showing environmental data, a central planning console, and tool activation buttons. An AI operator monitors screens, plans actions, and presses tool buttons in a continuous loop. Visual metaphor for the AI agent control loop.",
    "agent-loop-detective": "A detective at a crime scene following the perceive-reason-act loop: examining clues (perceive), pondering connections at a desk (reason), then taking action (act). Arrows show the continuous cycle. Visual metaphor for the agent loop.",
    "code-sandbox-playground": "A child playground enclosed by a protective bubble/dome. Inside, an AI agent writes and runs code safely. Even if something goes wrong inside the bubble, the outside world remains unaffected. Visual metaphor for sandboxed code execution.",
    "four-patterns-toolbelt": "A utility belt with four distinct tool pouches, each representing an agentic design pattern: prompt chaining (chain links), routing (compass), orchestration (conductor baton), and autonomous (robot arm). Visual metaphor for the four agentic patterns.",
    "function-calling-waiter": "A restaurant scene: the LLM customer reads the menu and describes their order to a waiter (function caller). The waiter takes the structured order to the kitchen (external API), which prepares the dish (result). Visual metaphor for function calling.",
    "hybrid-agent-relay": "A relay race where a lightweight sprinter (small model) handles easy legs quickly, then passes the baton to a heavyweight runner (large model) for the difficult stretches. Both contribute their strengths. Visual metaphor for hybrid agent patterns.",
    "mcp-universal-adapter": "A universal power adapter that converts any plug type to any socket type. Multiple different tools/services connect through one standardized adapter. Visual metaphor for the Model Context Protocol as a universal tool interface.",
    "plan-execute-general": "A military command center split in two: the strategic room (planner) with maps and strategy boards, and the field operations room (executor) carrying out orders. The general plans while soldiers execute. Visual metaphor for plan-and-execute agent architecture.",
    "sandboxed-execution": "An AI agent working behind safety glass in a laboratory. The agent can manipulate code and tools inside the enclosure, but a thick glass barrier protects the outside environment. Visual metaphor for sandboxed agent execution.",
    "self-debugging-loop": "A programmer robot that writes code, runs it, spots a bug (red error), examines the error, fixes the code, and runs it again (now green/success). A circular workflow with clear stages. Visual metaphor for self-debugging agents.",
    "thinking-budget-dial": "A large dial/knob labeled from Quick and Cheap to Deep and Thorough. At the low setting, simple tasks get fast answers. At the high setting, complex tasks get careful, expensive deliberation. Visual metaphor for the thinking budget/compute tradeoff.",
    "tool-use-vending-machine": "A vending machine where an AI agent inserts a structured request (like coins) and selects a tool (like pressing a button). The machine dispenses the result. Different slots offer different tools. Visual metaphor for tool use in agents.",
    "tree-search-forest": "A forest with multiple branching paths. An agent explores several paths simultaneously (shown as ghost trails). Some paths hit dead ends; the best path is highlighted in gold. Visual metaphor for tree search in agent planning.",
    "tree-search-maze": "A bird's-eye view of a maze with multiple paths being explored simultaneously. Some paths are abandoned (red), others continue being explored (yellow), and the best path is highlighted (green). Visual metaphor for Language Agent Tree Search (LATS).",
    "debate-courtroom": "A courtroom with two AI agents on opposing sides arguing their cases before a judge agent. Evidence and arguments are presented. The judge weighs both sides. Visual metaphor for the debate pattern in multi-agent systems.",
    "debate-pattern": "Two AI agents facing each other in a structured debate format, each with speech bubbles containing opposing arguments. A mediator/judge sits between them evaluating. Visual metaphor for multi-agent debate pattern.",
    "framework-toolbox": "A hardware store display of different agent/ML framework toolkits, each in its own branded box. A developer compares the feature lists and documentation. Visual metaphor for choosing a framework.",
    "groupthink-conformity": "A group of identical-looking AI agents sitting in a circle, all nodding in agreement and producing the same output. One agent tries to disagree but is pressured to conform. Visual metaphor for multi-agent groupthink.",
    "langgraph-subway": "A subway system map where stations are graph nodes (agent states) and colored train lines are edges (transitions). Trains carry state through the graph. Visual metaphor for LangGraph state machine approach.",
    "orchestra-supervisor": "An orchestra conductor on a podium directing multiple musicians (specialized agents). The conductor points to different sections when their expertise is needed. Sheet music (shared state) flows between players. Visual metaphor for the supervisor pattern.",
    "pipeline-assembly-line": "A factory assembly line where each station is a different agent adding its specialized contribution. Raw input enters one end; each agent processes and passes it forward until a polished output emerges. Visual metaphor for pipeline agent architecture.",
    "supervisor-orchestra": "A conductor agent standing at a central podium, directing specialized agent musicians. The conductor decides which agent plays next based on the score (task requirements). Visual metaphor for the supervisor multi-agent pattern.",
    "diffusion-restoration": "A sequence showing pure TV static/noise on the left, gradually becoming clearer through intermediate stages, until a sharp, beautiful image appears on the right. Each step removes noise and adds detail. Visual metaphor for how diffusion models generate images.",
    "document-ai-reader": "A robot with reading glasses examining messy documents: PDFs with tables, handwritten notes, and complex layouts. The robot extracts clean, structured data from the chaos. Visual metaphor for Document AI processing.",
    "pipeline-vs-native-multimodal": "Split scene: Left shows separate models duct-taped together with pipes (pipeline approach). Right shows a single unified model that natively processes all modalities through one brain. The native approach is cleaner. Visual metaphor for pipeline vs. native multimodal.",
    "pair-programming-robot": "A human developer and a robot sitting side by side at a desk, both looking at the same code on screen. The robot suggests code while the human reviews and decides. Visual metaphor for AI pair programming.",
    "drift-monitoring-dashboard": "A monitoring dashboard with gauges and time-series charts. Some metrics drift from their baseline (green zone) into warning (yellow) and danger (red) zones. An alert bell rings. Visual metaphor for model drift detection in production.",
    "llm-judge-courtroom": "A courtroom where one LLM sits as the judge, evaluating another LLM output presented as evidence. The judge scores the response on a rubric. Visual metaphor for LLM-as-judge evaluation.",
    "quality-inspector": "A quality inspector at a conveyor belt of AI outputs, examining each response with tools: accuracy scales, relevance meters, and coherence gauges. Some responses pass; others are flagged. Visual metaphor for LLM output quality inspection.",
    "testing-pyramid": "A pyramid diagram with three levels: broad base of unit tests (many small tests), middle layer of integration tests, and narrow top of end-to-end tests. Each layer is a different color. Visual metaphor for the LLM testing pyramid.",
    "autoscaling-accordion": "An accordion instrument that expands and contracts. When demand is high, the accordion stretches wide (more servers). When demand drops, it compresses (fewer servers). Visual metaphor for auto-scaling infrastructure.",
    "deployment-rocket-launch": "A rocket on a launch pad going through final checks before launch. Engineers at control stations run through checklists. The journey from prototype (Jupyter notebook on the ground) to production (rocket in the sky). Visual metaphor for deploying LLM applications.",
    "missing-steering-wheel": "A powerful sports car (the LLM) with no steering wheel or controls. Beautiful engine, great performance, but impossible to direct. A guardrails kit sits nearby, ready to be installed. Visual metaphor for needing proper controls around powerful LLMs.",
    "restaurant-kitchen-architecture": "A restaurant kitchen blueprint/floor plan showing the flow from order intake (API gateway) to cooking stations (inference) to plating (post-processing) to serving (response delivery). Visual metaphor for production LLM architecture.",
}

# Chapter opener prompts by module
chapter_opener_map = {
    "module-08": "A futuristic server room where giant neural network models are being compressed and optimized. Conveyor belts carry large model blocks through quantization machines that shrink them. Speed gauges and efficiency meters on the walls. Visual metaphor for inference optimization, model compression, and efficient serving.",
    "module-09": "A grand hotel concierge desk where a friendly robot concierge assists various customers (developers). Behind the desk, switchboards and cables connect to multiple API provider doors. Keys, tokens, and request tickets are organized neatly. Visual metaphor for LLM API access, authentication, and provider ecosystems.",
    "module-10": "A film director chair with a megaphone, surrounded by script pages written in natural language. A clapperboard reads Prompt Engineering. Stage lights illuminate different prompt strategies laid out like storyboards. Visual metaphor for prompt engineering as directing AI behavior through language.",
    "module-11": "A modern workshop bench with two distinct toolsets side by side: traditional ML tools (rulers, calipers, precision instruments) and LLM tools (paintbrushes, creative instruments, conversation bubbles). A skilled craftsperson combines both into a hybrid pipeline. Visual metaphor for combining classical ML with LLMs.",
    "module-12": "A bustling data factory with conveyor belts. LLM robots stamp out training examples from templates. Quality inspectors check outputs. Raw seed data goes in one end, polished synthetic datasets emerge from the other. Pipes, gears, and steam suggest industrial scale. Visual metaphor for synthetic data generation.",
    "module-13": "An old, wise dog (representing a pre-trained model) sitting in a classroom, wearing reading glasses, learning new tricks from a chalkboard. The chalkboard shows domain-specific knowledge. Training treats and a leash represent learning rate and constraints. Visual metaphor for fine-tuning pre-trained models.",
    "module-14": "A massive frozen glacier (representing a frozen base model) with small, colorful sticky notes and adapters attached to its surface. The adapters glow with energy while the glacier remains unchanged. Toolbelts with lightweight attachments hang nearby. Visual metaphor for parameter-efficient fine-tuning (PEFT/LoRA).",
    "module-15": "A master chef in a grand kitchen distilling complex multi-course recipes into simple, elegant dishes for an apprentice. A large cauldron (teacher model) pours refined knowledge into smaller vessels (student models). Cocktail shakers nearby represent model merging. Visual metaphor for knowledge distillation and model merging.",
    "module-16": "A talent show stage where language model contestants perform. Human judges in the audience hold up score cards. A compass and moral scales sit beside the stage. A before/after split shows a raw model vs. an aligned, helpful model. Visual metaphor for RLHF, DPO, and alignment techniques.",
    "module-17": "An X-ray machine scanning a neural network brain, revealing the internal circuits, attention patterns, and feature representations glowing inside. A scientist examines the transparent layers. Magnifying glasses and probes surround the setup. Visual metaphor for interpretability and mechanistic understanding of neural networks.",
    "module-18": "A vast cosmic map where words and documents float as glowing stars, clustered by meaning. Similar concepts orbit close together while different ones are far apart. A librarian with a telescope searches this embedding universe. Vector arrows connect related items. Visual metaphor for embeddings and vector databases.",
    "module-19": "A student sitting at an exam desk with an open textbook (retrieval) beside their exam paper. The student looks up relevant pages before writing answers. Bookshelves and a search engine interface float in the background. Visual metaphor for Retrieval-Augmented Generation (RAG) as an open-book exam.",
    "module-20": "A friendly AI receptionist at a busy help desk, juggling multiple conversation threads represented as speech bubbles and ticket queues. Memory shelves store past conversation context. A calendar and tools suggest long-running dialogue management. Visual metaphor for conversational AI systems.",
    "module-21": "An AI agent in a control room with screens showing the environment, a planning whiteboard, and tool drawers. The agent follows a perceive-think-act loop shown as a circular diagram. Robotic arms reach toward various tools (calculator, browser, code terminal). Visual metaphor for autonomous AI agents.",
    "module-22": "An orchestra pit with multiple AI agents, each playing a different instrument (representing different skills). A conductor agent coordinates them from a podium. Music sheets flow between players representing shared state. Visual metaphor for multi-agent systems and collaboration.",
    "module-23": "A futuristic AI entity with multiple sensory organs: camera eyes for vision, microphone ears for audio, keyboard hands for text, and a paintbrush tail for generation. Images, text, and audio streams flow through and merge at the center. Visual metaphor for multimodal AI systems.",
    "module-24": "A diverse panorama of LLM applications: a robot coding partner, a financial analyst reading charts, a medical assistant reviewing scans, a legal researcher examining documents, and a creative writer crafting stories. All connected by a central LLM brain. Visual metaphor for real-world LLM applications.",
    "module-25": "A quality control laboratory with inspection stations. AI outputs pass through checkpoints: accuracy meters, bias detectors, hallucination scanners, and performance dashboards. Inspectors with clipboards evaluate model responses. Visual metaphor for LLM evaluation and observability.",
    "module-26": "A rocket launch pad where a Jupyter notebook transforms into a production rocket ship. Engineers check systems, monitoring dashboards light up, and scaling infrastructure extends into the clouds. The journey from prototype to production. Visual metaphor for production engineering of LLM applications.",
    "module-27": "A medieval castle with layered defenses protecting an LLM at the center. Shields (prompt injection defense, content filtering, bias detection) form concentric walls. Watchtowers monitor for threats. Visual metaphor for AI safety, ethics, and regulation.",
    "module-28": "A boardroom where technical charts meet business strategy. One side shows model architectures and metrics, the other shows ROI graphs, product roadmaps, and user journey maps. A bridge connects the two halves. Visual metaphor for AI strategy, product thinking, and return on investment.",
}

for m in missing:
    fn = m["filename"]
    target = m["target_path"]
    caption = m["caption"]

    # Skip author photo and templates
    if fn == "yehudit-aperstein":
        continue
    if "/templates/" in target or "{{" in m["src"]:
        continue

    # Agent avatars
    if "/agents/avatars/" in target:
        role = fn.split("-", 1)[1].replace("-", " ") if "-" in fn else fn
        prompt = (
            f"{AVATAR_STYLE} Role: {role}. The avatar should visually suggest "
            f"the role through symbolic elements (e.g., a magnifying glass for "
            f"fact-checker, code brackets for code agent, drafting tools for "
            f"designer, a metronome for pacing editor)."
        )
        prompts.append(prompt)
        mapping.append({"prompt_index": len(prompts), "prompt": prompt, "target_path": target})
        continue

    # Chapter openers
    if fn == "chapter-opener":
        module_key = None
        for key in chapter_opener_map:
            if key in target:
                module_key = key
                break
        if module_key:
            prompt = f"{TEXTBOOK_STYLE} {chapter_opener_map[module_key]}"
        else:
            prompt = f"{TEXTBOOK_STYLE} A chapter opening illustration for an AI/ML textbook. {caption}"
        prompts.append(prompt)
        mapping.append({"prompt_index": len(prompts), "prompt": prompt, "target_path": target})
        continue

    # Section illustrations
    if fn in prompt_map:
        prompt = f"{TEXTBOOK_STYLE} {prompt_map[fn]}"
    elif caption:
        clean_cap = caption.split(":")[1].strip() if ":" in caption else caption
        prompt = f"{TEXTBOOK_STYLE} {clean_cap}"
    else:
        desc = fn.replace("-", " ").replace("_", " ")
        prompt = f"{TEXTBOOK_STYLE} Conceptual illustration of {desc} for an AI/ML textbook."

    prompts.append(prompt)
    mapping.append({"prompt_index": len(prompts), "prompt": prompt, "target_path": target})

# Write prompts file
prompts_path = f"{base}/scripts/illustration_prompts.txt"
with open(prompts_path, "w", encoding="utf-8") as f:
    f.write("# Illustration prompts for LLMCourse textbook\n")
    f.write(f"# Total: {len(prompts)} prompts\n")
    f.write("# Generated by TASK-002\n\n")
    for p in prompts:
        f.write(p + "\n")

# Write mapping file
mapping_path = f"{base}/scripts/illustration_mapping.json"
with open(mapping_path, "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2)

print(f"Wrote {len(prompts)} prompts to {prompts_path}")
print(f"Wrote {len(mapping)} mappings to {mapping_path}")
