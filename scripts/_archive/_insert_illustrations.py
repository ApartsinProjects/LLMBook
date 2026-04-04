#!/usr/bin/env python3
"""Insert illustration figures into section HTML files."""

import re
import os

CSS_BLOCK = """.illustration { margin: 2rem auto; text-align: center; }
.illustration img { max-width: 100%; border-radius: 8px; }
.illustration figcaption { font-size: 0.9rem; color: #666; margin-top: 0.5rem; font-style: italic; }"""

MODULE_12 = "E:/Projects/LLMCourse/part-4-training-adapting/module-12-synthetic-data"
MODULE_13 = "E:/Projects/LLMCourse/part-4-training-adapting/module-13-fine-tuning-fundamentals"
MODULE_14 = "E:/Projects/LLMCourse/part-4-training-adapting/module-14-peft"
MODULE_15 = "E:/Projects/LLMCourse/part-4-training-adapting/module-15-distillation-merging"
MODULE_16 = "E:/Projects/LLMCourse/part-4-training-adapting/module-16-alignment-rlhf-dpo"
MODULE_17 = "E:/Projects/LLMCourse/part-4-training-adapting/module-17-interpretability"
MODULE_18 = "E:/Projects/LLMCourse/part-5-retrieval-conversation/module-18-embeddings-vector-db"
MODULE_19 = "E:/Projects/LLMCourse/part-5-retrieval-conversation/module-19-rag"
MODULE_20 = "E:/Projects/LLMCourse/part-5-retrieval-conversation/module-20-conversational-ai"
MODULE_21 = "E:/Projects/LLMCourse/part-6-agents-applications/module-21-ai-agents"
MODULE_22 = "E:/Projects/LLMCourse/part-6-agents-applications/module-22-multi-agent-systems"
MODULE_23 = "E:/Projects/LLMCourse/part-6-agents-applications/module-23-multimodal"
MODULE_24 = "E:/Projects/LLMCourse/part-6-agents-applications/module-24-llm-applications"
MODULE_25 = "E:/Projects/LLMCourse/part-6-agents-applications/module-25-evaluation-observability"

# (module_dir, section_file, image_filename, alt_text, caption)
illustrations = [
    # Module 12: Synthetic Data
    (MODULE_12, "section-12.1.html", "synthetic-data-factory.png",
     "A whimsical factory assembly line producing synthetic training data from raw materials",
     "Welcome to the synthetic data factory, where LLMs work overtime turning prompts into training gold. No real users were harmed in the making of this dataset."),
    (MODULE_12, "section-12.1.html", "seed-data-garden.png",
     "A garden where seed examples grow into a full dataset, with small seedlings becoming large data trees",
     "Every great synthetic dataset starts with a handful of seed examples. Plant them well, and watch your training data bloom."),
    (MODULE_12, "section-12.2.html", "llm-assembly-line.png",
     "An assembly line where an LLM processes prompts on a conveyor belt, producing structured outputs",
     "The LLM generation pipeline: prompts go in one end, polished training examples come out the other. Quality control not included by default."),
    (MODULE_12, "section-12.2.html", "prompt-template-cookie-cutter.png",
     "Cookie cutters shaped like prompt templates stamping out uniform data examples from dough",
     "Prompt templates are the cookie cutters of synthetic data generation. Same shape, different fillings, consistently delicious results."),
    (MODULE_12, "section-12.2.html", "evol-instruct-evolution.png",
     "Instructions evolving from simple to complex forms, depicted as creatures on an evolutionary timeline",
     "Evol-Instruct in action: simple instructions evolve into increasingly complex ones, like Darwinian selection for prompt difficulty."),
    (MODULE_12, "section-12.3.html", "llm-actor-stage.png",
     "An LLM on a theater stage performing different roles with costume changes representing different personas",
     "The LLM takes center stage, playing user, assistant, and evaluator in a one-model show. Method acting has never been so computationally expensive."),
    (MODULE_12, "section-12.4.html", "quality-filtering-pipeline.png",
     "A pipeline with multiple filters catching bad data while letting high-quality examples pass through",
     "Quality filtering: because not everything an LLM generates deserves to make it into your training set. Think of it as a bouncer for your dataset."),
    (MODULE_12, "section-12.4.html", "data-quality-inspector.png",
     "An inspector with a magnifying glass examining data samples on a conveyor belt, rejecting flawed ones",
     "Every synthetic dataset needs a quality inspector. The good news is that the inspector can also be an LLM. The bad news? Inspectors make mistakes too."),
    (MODULE_12, "section-12.4.html", "deduplication-twins.png",
     "Identical twin data points being separated, with one being sent away while the other stays",
     "Deduplication catches those sneaky twin samples that inflate your dataset size without adding real diversity. Only one of you gets to stay."),
    (MODULE_12, "section-12.4.html", "data-diversity-spectrum.png",
     "A rainbow spectrum of diverse data samples spanning different topics, styles, and formats",
     "A healthy dataset is a diverse dataset. If all your examples look the same, your model will think the whole world looks that way too."),
    (MODULE_12, "section-12.4.html", "model-collapse-spiral.png",
     "A spiral descending into increasingly distorted and repetitive outputs, representing model collapse from training on synthetic data",
     "Model collapse: what happens when models train on their own outputs for too long. It is the AI equivalent of a photocopy of a photocopy of a photocopy."),
    (MODULE_12, "section-12.5.html", "labeling-sorting-hat.png",
     "A sorting hat from a magical school placing labels on data examples, categorizing them into different houses",
     "LLM-assisted labeling is like having a sorting hat for your data. It is not always right, but it is fast and surprisingly good at the job."),
    (MODULE_12, "section-12.5.html", "active-learning-fishing.png",
     "A fisherman carefully selecting which fish to catch from a sea of data points, choosing the most informative ones",
     "Active learning: why label everything when you can strategically fish for the samples that teach your model the most?"),
    (MODULE_12, "section-12.5.html", "noisy-labels-orchestra.png",
     "An orchestra where some musicians are playing the wrong notes, representing noisy labels in a dataset",
     "Noisy labels are like an orchestra where a few musicians are playing the wrong piece. The challenge is figuring out who is off-key."),
    (MODULE_12, "section-12.6.html", "weak-supervision-jury.png",
     "A jury of diverse labeling functions voting on the correct label for a data point",
     "Weak supervision lets multiple imperfect labeling functions vote on the answer. Democracy for data labels, where the majority usually wins."),
    (MODULE_12, "section-12.7.html", "reasoning-chain-dominos.png",
     "A chain of dominos falling in sequence, each representing a step in a reasoning chain",
     "Reasoning chains are like dominos: each step triggers the next, and if one falls wrong, the whole conclusion topples."),
    (MODULE_12, "section-12.7.html", "rejection-sampling-panning.png",
     "A prospector panning for gold nuggets in a stream of generated reasoning traces",
     "Rejection sampling for reasoning data is just gold panning with extra steps. Generate many traces, keep only the nuggets that actually reach the correct answer."),
    (MODULE_12, "section-12.7.html", "red-team-boxing-ring.png",
     "Two LLMs in a boxing ring, one generating adversarial examples while the other tries to defend against them",
     "Red-teaming with synthetic data: one LLM throws punches while the other learns to dodge. The best defense is a good sparring partner."),

    # Module 13: Fine-Tuning
    (MODULE_13, "section-13.1.html", "fine-tuning-old-dog.png",
     "An old dog happily learning a new trick, representing a pretrained model being fine-tuned for a new task",
     "They say you cannot teach an old dog new tricks, but fine-tuning proves them wrong. With the right data, even a pretrained model can learn your specific task."),
    (MODULE_13, "section-13.1.html", "fine-tune-decision-tree.png",
     "A decision tree flowchart helping practitioners decide whether to fine-tune or use prompting",
     "The eternal question: should you fine-tune or just prompt better? This decision tree saves you from weeks of unnecessary GPU bills."),
    (MODULE_13, "section-13.3.html", "catastrophic-forgetting.png",
     "A model losing old memories while absorbing new ones, depicted as books falling off a shelf as new ones are added",
     "Catastrophic forgetting: your model aced the new task but forgot everything else. It is like cramming for one exam and blanking on all the others."),
    (MODULE_13, "section-13.2.html", "sequence-packing-tetris.png",
     "Training sequences being packed together like Tetris blocks to minimize wasted padding tokens",
     "Sequence packing is Tetris for training data. Fit as many examples as possible into each batch, and watch your GPU utilization score soar."),

    # Module 14: PEFT
    (MODULE_14, "section-14.1.html", "lora-sticky-note.png",
     "A small sticky note attached to a large frozen neural network, representing LoRA's lightweight trainable parameters",
     "LoRA in a nutshell: instead of rewriting the whole textbook, just slap a sticky note on the relevant pages. Same knowledge, fraction of the effort."),
    (MODULE_14, "section-14.1.html", "qlora-truck-decals.png",
     "A delivery truck with custom decals representing QLoRA's quantized base model with low-rank adapters",
     "QLoRA: take your already-compact quantized model and add custom decals. You get personalization without needing a bigger garage."),
    (MODULE_14, "section-14.2.html", "peft-adapter-accessories.png",
     "A model wearing various adapter accessories like hats, scarves, and glasses representing different PEFT methods",
     "PEFT methods are like accessories for your base model. Mix and match adapters until you find the look that works for your task."),

    # Module 15: Distillation & Merging
    (MODULE_15, "section-15.1.html", "distillation-chef.png",
     "A master chef (teacher model) guiding a junior chef (student model) to recreate a complex dish in a simpler way",
     "Knowledge distillation: the master chef teaches the apprentice not just the recipe, but the subtle intuitions behind every step. The student's version might be smaller, but it captures the essence."),
    (MODULE_15, "section-15.2.html", "model-merging-cocktail.png",
     "A bartender mixing different model weights together like cocktail ingredients to create a blended model",
     "Model merging is mixology for neural networks. Combine the right weights in the right proportions, and you get something better than any single ingredient."),

    # Module 16: Alignment
    (MODULE_16, "section-16.1.html", "rlhf-talent-show.png",
     "A talent show where a model performs responses and human judges score them, representing RLHF's reward modeling",
     "RLHF is basically a talent show for language models. Humans judge the performances, and the model learns to play to the crowd."),
    (MODULE_16, "section-16.2.html", "dpo-vs-rlhf-comparison.png",
     "A side-by-side comparison showing RLHF's complex multi-stage pipeline versus DPO's streamlined single-stage approach",
     "DPO looks at RLHF's elaborate setup and says: why hire a separate critic when the model can learn directly from preferences? Fewer moving parts, similar results."),
    (MODULE_16, "section-16.3.html", "constitutional-ai-angel.png",
     "An angel on a model's shoulder representing constitutional principles guiding the model's self-critique",
     "Constitutional AI gives the model its own moral compass. Instead of relying solely on human feedback, the model critiques itself against a set of principles."),

    # Module 17: Interpretability
    (MODULE_17, "section-17.1.html", "interpretability-xray.png",
     "An X-ray machine scanning a neural network, revealing internal structures and activation patterns",
     "Interpretability is like giving your model an X-ray. You finally get to see what is going on inside all those billions of parameters."),
    (MODULE_17, "section-17.2.html", "superposition-coat-rack.png",
     "A coat rack with too many coats hanging on too few hooks, representing how neural networks store more features than they have dimensions",
     "Superposition: neurons store more concepts than they have dimensions, like hanging twenty coats on five hooks. It works until you try to grab just one."),
    (MODULE_17, "section-17.2.html", "logit-lens-building.png",
     "A cross-section view of a building showing different floors processing information differently, representing the logit lens view of transformer layers",
     "The logit lens lets you peek at each floor of the transformer to see how predictions evolve layer by layer. The ground floor has vague ideas; the penthouse has confident answers."),

    # Module 18: Embeddings & Vector DB
    (MODULE_18, "section-18.1.html", "embedding-space-party.png",
     "A party where similar concepts cluster together in groups while dissimilar ones stand far apart in a room",
     "Welcome to the embedding space party, where similar concepts hang out together and unrelated ones awkwardly avoid each other across the room."),
    (MODULE_18, "section-18.1.html", "contrastive-learning-magnets.png",
     "Magnets pulling similar text pairs together and pushing dissimilar pairs apart in embedding space",
     "Contrastive learning works like magnets: similar pairs get pulled together while dissimilar ones get pushed apart. Simple physics, powerful embeddings."),
    (MODULE_18, "section-18.1.html", "matryoshka-embeddings-nesting.png",
     "Russian nesting dolls where each layer represents a different embedding dimensionality, all containing useful information",
     "Matryoshka embeddings are like Russian nesting dolls: peel off outer dimensions and you still get a useful (if smaller) representation inside."),
    (MODULE_18, "section-18.2.html", "hnsw-city-navigation.png",
     "A city with express highways and local streets, representing HNSW's hierarchical graph structure for fast nearest-neighbor search",
     "HNSW navigates vector space like a city driver: start on the highway for big jumps, then switch to local streets to find the exact address."),
    (MODULE_18, "section-18.2.html", "hnsw-express-lanes.png",
     "Express lanes on a highway that skip stops, representing the skip connections in HNSW's upper layers",
     "The upper layers of HNSW are express lanes that skip most stops. The lower layers handle the last-mile navigation to your nearest neighbors."),
    (MODULE_18, "section-18.2.html", "product-quantization-paint.png",
     "An artist mixing a limited palette of base colors to approximate any color, representing product quantization's codebook approach",
     "Product quantization is like painting with a limited palette. You cannot represent every exact shade, but a clever mix of base colors gets surprisingly close."),
    (MODULE_18, "section-18.3.html", "vector-db-librarian.png",
     "A librarian organizing books not by title but by similarity of content, representing how vector databases organize data",
     "A vector database librarian does not care about alphabetical order. They shelve books by vibes, so everything about cooking ends up near everything about food."),
    (MODULE_18, "section-18.3.html", "metadata-filtering-bouncer.png",
     "A bouncer at a club checking IDs and metadata tags before allowing vectors into the search results",
     "Metadata filtering is the bouncer of vector search. Before any similarity matching happens, it checks the tags and kicks out vectors that do not belong."),
    (MODULE_18, "section-18.4.html", "chunking-baguette.png",
     "A baguette being sliced into chunks of different sizes, representing document chunking strategies",
     "Chunking a document is like slicing a baguette. Too thin and you lose context; too thick and it will not fit in the model's mouth."),
    (MODULE_18, "section-18.4.html", "chunking-sushi-chef.png",
     "A sushi chef carefully cutting fish into precise pieces, representing semantic chunking that respects natural boundaries",
     "Semantic chunking is sushi-grade precision. Cut at the natural boundaries, not at arbitrary character counts, and every piece is a complete thought."),
    (MODULE_18, "section-18.4.html", "parent-child-retrieval-telescope.png",
     "A telescope zooming from a wide view to a specific detail, representing parent-child chunk retrieval",
     "Parent-child retrieval: search finds the specific detail (child chunk), then hands back the full context (parent chunk). Zoom in to find it, zoom out to understand it."),
    (MODULE_18, "section-18.5.html", "colpali-xray-vision.png",
     "X-ray vision glasses looking at a document page and seeing both text and visual layout simultaneously",
     "ColPali gives retrieval systems X-ray vision for documents. Instead of just reading the text, it sees the whole page layout, tables, figures, and all."),
    (MODULE_18, "section-18.5.html", "late-interaction-judges.png",
     "A panel of judges each scoring different aspects of a document before combining their verdicts",
     "Late interaction models let each query token independently interrogate every document token. It is like having a panel of specialist judges instead of one generalist."),

    # Module 19: RAG
    (MODULE_19, "section-19.1.html", "rag-open-book-exam.png",
     "A student taking an exam with an open textbook, representing how RAG lets models look up information",
     "RAG turns every LLM query into an open-book exam. The model does not need to memorize everything when it can just look it up."),
    (MODULE_19, "section-19.1.html", "rag-open-book-student.png",
     "A student flipping through reference materials while writing an answer, representing the RAG retrieval-generation loop",
     "The RAG workflow: retrieve the relevant pages, read them quickly, then write a well-informed answer. Just like the best students in class."),
    (MODULE_19, "section-19.2.html", "advanced-rag-treasure-hunt.png",
     "An adventurer following a multi-step treasure map with clues leading to progressively better answers",
     "Advanced RAG is a treasure hunt where each retrieval step gets you closer to the answer. Query rewriting, re-ranking, and iterative refinement are your map and compass."),
    (MODULE_19, "section-19.2.html", "reranking-judges-panel.png",
     "A panel of judges re-scoring contestants after an initial screening round, representing cross-encoder reranking",
     "Reranking is the callback round: initial retrieval gives you candidates, then a cross-encoder judge takes a closer look at each one to pick the real winners."),
    (MODULE_19, "section-19.2.html", "hyde-crystal-ball.png",
     "A crystal ball generating a hypothetical answer that is then used to search for real documents",
     "HyDE peers into a crystal ball to generate a hypothetical answer first, then uses that answer to find real documents. Sometimes the best search query is a rough draft of the answer itself."),
    (MODULE_19, "section-19.2.html", "lost-in-middle-sandwich.png",
     "A sandwich where the middle filling is being ignored while the top and bottom bread get all the attention",
     "The lost-in-the-middle problem: LLMs pay attention to the first and last documents but forget what is sandwiched in between. Position matters more than it should."),
    (MODULE_19, "section-19.3.html", "knowledge-graph-islands.png",
     "Islands connected by bridges representing entities linked by relationships in a knowledge graph",
     "Knowledge graphs turn your documents into connected islands of facts. Each bridge is a relationship, and RAG can traverse them to find answers that span multiple hops."),
    (MODULE_19, "section-19.3.html", "knowledge-graph-subway-map.png",
     "A subway map where stations are entities and lines are relationships, representing knowledge graph traversal",
     "Navigating a knowledge graph is like riding the subway: hop between entity stations along relationship lines to reach your destination answer."),
    (MODULE_19, "section-19.3.html", "graphrag-detective-board.png",
     "A detective's evidence board with photos, strings, and pins connecting clues, representing GraphRAG's entity linking",
     "GraphRAG turns your retrieval system into a detective. Pin the entities to the board, connect them with strings, and follow the relationships to crack the case."),

    # Module 20: Conversational AI
    (MODULE_20, "section-20.1.html", "dialogue-system-receptionist.png",
     "A friendly receptionist managing multiple conversations, routing requests, and maintaining context",
     "A dialogue system is the ultimate receptionist: juggling multiple conversations, remembering preferences, and routing requests without dropping a single thread."),
    (MODULE_20, "section-20.3.html", "memory-management-containers.png",
     "Different-sized containers representing short-term, long-term, and working memory in a conversational AI system",
     "Memory management in conversational AI: short-term memory holds the current chat, long-term memory stores user preferences, and working memory juggles it all without spilling."),

    # Module 21: AI Agents
    (MODULE_21, "section-21.1.html", "agent-control-room.png",
     "A control room with monitors and switches where an AI agent observes, plans, and executes actions",
     "The agent control room: observe the environment, plan the next move, execute an action, and repeat. It is an endless loop of perceive, think, act."),
    (MODULE_21, "section-21.1.html", "agent-loop-detective.png",
     "A detective cycling through clues, hypotheses, and investigations, representing the agent's observe-think-act loop",
     "Every AI agent is a detective at heart: observe the clues, form a hypothesis, take action, and loop back when new evidence appears."),
    (MODULE_21, "section-21.1.html", "four-patterns-toolbelt.png",
     "A toolbelt with four distinct tools representing the four core agent patterns: ReAct, tool use, planning, and reflection",
     "The four fundamental agent patterns in one handy toolbelt. Pick the right pattern for the job, or combine them for maximum problem-solving power."),
    (MODULE_21, "section-21.2.html", "tool-use-vending-machine.png",
     "A vending machine where an agent inserts a function call and receives structured results",
     "Tool use is a vending machine for capabilities. The agent inserts a well-formatted function call and out pops a structured result. No reaching behind the glass allowed."),
    (MODULE_21, "section-21.2.html", "function-calling-waiter.png",
     "A waiter taking a structured order from an AI agent and delivering results from the kitchen (API)",
     "Function calling turns the LLM into a polite waiter: it takes your order in a structured format, sends it to the kitchen (API), and returns with exactly what you asked for."),
    (MODULE_21, "section-21.2.html", "mcp-universal-adapter.png",
     "A universal power adapter that lets any agent plug into any tool, representing the Model Context Protocol",
     "MCP is the universal power adapter of the agent world. One standard protocol, and suddenly every tool plugs in without custom wiring."),
    (MODULE_21, "section-21.3.html", "plan-execute-general.png",
     "A military general standing before a strategy board, planning the sequence of operations before executing them",
     "Plan-then-execute agents think before they act, like a general mapping out the campaign before sending troops. Upfront planning avoids costly mid-battle pivots."),
    (MODULE_21, "section-21.3.html", "tree-search-forest.png",
     "A hiker at a fork in a forest trail, with multiple branching paths representing tree search over possible action sequences",
     "Tree search explores multiple possible paths through the forest of actions. Some trails lead to treasure; others to dead ends. The trick is pruning early."),
    (MODULE_21, "section-21.3.html", "tree-search-maze.png",
     "A maze being explored from above, with highlighted paths showing different search strategies",
     "Navigating an action space is like solving a maze: breadth-first finds the shortest path, but depth-first discovers the interesting corners."),
    (MODULE_21, "section-21.4.html", "sandboxed-execution.png",
     "Code running inside a sealed glass box with safety barriers, representing sandboxed code execution",
     "Sandboxed execution keeps agent-generated code safely behind glass. It can compute, create, and transform, but it cannot escape to cause real-world damage."),
    (MODULE_21, "section-21.4.html", "code-sandbox-playground.png",
     "A children's playground enclosed by a fence, where code executes safely in a controlled environment",
     "The code sandbox is a fenced playground for LLM-generated scripts. Let them run wild inside, knowing the fence keeps everything contained."),
    (MODULE_21, "section-21.4.html", "self-debugging-loop.png",
     "A robot examining its own code with a magnifying glass, fixing bugs in a feedback loop",
     "Self-debugging agents read their own error messages and try again. It is like a programmer who actually reads the stack trace on the first attempt."),

    # Module 22: Multi-Agent Systems
    (MODULE_22, "section-22.2.html", "orchestra-supervisor.png",
     "A conductor leading an orchestra of specialized agents, each playing a different instrument",
     "The supervisor pattern is an orchestra conductor: one agent coordinates the specialists, ensuring everyone plays their part at the right time."),
    (MODULE_22, "section-22.2.html", "debate-pattern.png",
     "Two agents debating from podiums while a judge agent evaluates their arguments",
     "The debate pattern: agents argue opposing positions while a judge synthesizes the best answer. Adversarial collaboration at its finest."),
    (MODULE_22, "section-22.2.html", "groupthink-conformity.png",
     "A group of identical-looking agents all nodding in agreement, representing the danger of groupthink in multi-agent systems",
     "Beware of multi-agent groupthink: when all your agents come from the same model, they tend to agree with each other a little too enthusiastically."),
    (MODULE_22, "section-22.3.html", "pipeline-assembly-line.png",
     "An assembly line where each station is a different agent adding its contribution to the final product",
     "Pipeline agents work like an assembly line: each agent adds its piece, passes the work forward, and never looks back. Simple, predictable, and effective."),

    # Module 23: Multimodal
    (MODULE_23, "section-23.1.html", "pipeline-vs-native-multimodal.png",
     "A comparison showing a pipeline approach with separate vision and language models versus a unified native multimodal model",
     "Pipeline multimodal systems duct-tape separate models together; native multimodal models understand everything in one brain. The difference is like reading subtitles versus actually understanding the language."),
    (MODULE_23, "section-23.1.html", "diffusion-restoration.png",
     "A blurry, noisy image gradually becoming clear through the diffusion denoising process",
     "Diffusion models start with pure noise and gradually sculpt it into an image. It is like watching a Polaroid develop, except the camera is a neural network with billions of parameters."),
    (MODULE_23, "section-23.3.html", "document-ai-reader.png",
     "An AI reading a complex document with tables, figures, and text, extracting structured information",
     "Document AI reads your messy PDFs so you do not have to. Tables, headers, figures, footnotes: it parses the chaos and returns clean, structured data."),

    # Module 24: LLM Applications
    (MODULE_24, "section-24.1.html", "pair-programming-robot.png",
     "A robot sitting beside a human programmer, both looking at the same screen and collaborating on code",
     "AI pair programming: your tireless coding partner who never needs coffee breaks, never judges your variable names, and always has a suggestion ready."),

    # Module 25: Evaluation & Observability
    (MODULE_25, "section-25.1.html", "quality-inspector.png",
     "A quality inspector examining LLM outputs on a conveyor belt with a checklist and magnifying glass",
     "LLM evaluation is quality inspection for AI outputs. Every response gets checked against the rubric before it ships to production."),
    (MODULE_25, "section-25.2.html", "llm-judge-courtroom.png",
     "A judge LLM in a courtroom evaluating the quality of another LLM's response, with evidence exhibits on display",
     "LLM-as-judge: one model evaluates another's work in a courtroom of metrics. The verdict? It correlates surprisingly well with human judgment."),
    (MODULE_25, "section-25.4.html", "testing-pyramid.png",
     "A testing pyramid with unit tests at the base, integration tests in the middle, and end-to-end LLM evaluations at the top",
     "The LLM testing pyramid: unit tests form the solid base, integration tests fill the middle, and expensive end-to-end evaluations sit at the narrow top. Do not invert this pyramid."),
    (MODULE_25, "section-25.6.html", "drift-monitoring-dashboard.png",
     "A monitoring dashboard showing drift metrics, with some gauges in the green zone and others trending toward red",
     "Drift monitoring keeps watch so you do not wake up to a degraded model. When the gauges start trending red, it is time to investigate before users notice."),
]


def make_figure(img, alt, caption):
    return f'''<figure class="illustration">
    <img src="images/{img}" alt="{alt}" loading="lazy">
    <figcaption>{caption}</figcaption>
</figure>'''


def ensure_css(content):
    if '.illustration' in content:
        return content
    return content.replace('</style>', CSS_BLOCK + '\n</style>', 1)


def find_nth_p_end(content, start_pos, n=1):
    """Find the nth </p> after start_pos."""
    pos = start_pos
    for _ in range(n):
        pos = content.find('</p>', pos)
        if pos == -1:
            return -1
        pos += len('</p>')
    return pos


def insert_illustration(filepath, image_name, alt_text, caption, insert_after_p=1):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if image_name in content:
        print(f"  SKIP (already present): {image_name} in {os.path.basename(filepath)}")
        return False

    content = ensure_css(content)

    figure_html = make_figure(image_name, alt_text, caption)

    h1_match = re.search(r'<h1[^>]*>.*?</h1>', content)
    if not h1_match:
        print(f"  WARN: No <h1> in {os.path.basename(filepath)}")
        return False

    insert_pos = find_nth_p_end(content, h1_match.end(), insert_after_p)
    if insert_pos == -1:
        # Fall back to first </p>
        insert_pos = find_nth_p_end(content, h1_match.end(), 1)
        if insert_pos == -1:
            print(f"  WARN: Not enough </p> in {os.path.basename(filepath)} for {image_name}")
            return False

    content = content[:insert_pos] + '\n\n' + figure_html + '\n' + content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK: {image_name} -> {os.path.basename(filepath)}")
    return True


# Group images by file to handle multiple images per file
file_images = {}
for module_dir, section, img, alt, cap in illustrations:
    filepath = os.path.join(module_dir, section)
    if filepath not in file_images:
        file_images[filepath] = []
    file_images[filepath].append((img, alt, cap))

count = 0
for filepath, images in file_images.items():
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        continue

    for i, (img, alt, cap) in enumerate(images):
        # Insert after progressively later paragraphs to stagger images
        p_num = 1 + i * 2  # 1st, 3rd, 5th, 7th... paragraph
        if insert_illustration(filepath, img, alt, cap, insert_after_p=p_num):
            count += 1

print(f"\nTotal illustrations inserted: {count}")
