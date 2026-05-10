#!/usr/bin/env python3
"""
Generate illustration prompts for all 73 sections without illustrations.
Creates a prompts file and a mapping file for embedding after generation.
"""

import json
from pathlib import Path

BOOK_ROOT = Path("E:/Projects/LLMCourse")

# Each entry: (section_path, image_filename, prompt, alt_text, caption, placement_after_h2_number)
# placement_after_h2_number: which h2 section to place after (1-based), 0 = preamble

sections = [
    # ── Part 2: Understanding LLMs ──
    (
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html",
        "production-training-fault-tolerance.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A massive industrial kitchen with multiple chefs (representing GPU workers) cooking at connected stations. One chef has dropped a pot (representing a node failure), but the other chefs seamlessly continue cooking, passing dishes along the assembly line. A clipboard on the wall shows a checkpoint recipe. The style should be friendly and approachable, like a comic strip or an XKCD-inspired infographic, with expressive characters and minimal visual clutter. No text or lettering in the image.",
        "A large industrial kitchen with multiple chefs at connected cooking stations, one chef dropping a pot while others seamlessly continue the assembly line, representing fault-tolerant distributed training where node failures do not halt the entire pipeline",
        "In production LLM training, fault tolerance is not optional: when one node drops out, the rest of the system must keep cooking without missing a beat.",
        3  # After "Elastic and Fault-Tolerant Training"
    ),
    (
        "part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html",
        "open-source-vs-open-weight.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: Two glass display cases side by side in a museum. The left case shows a fully transparent machine with all gears and blueprints visible, labeled nothing (representing open-source). The right case shows a similar machine but with a locked compartment hiding the internal blueprints, only the exterior is visible (representing open-weight). Visitors peer into both cases curiously. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Two glass museum display cases side by side, one showing a fully transparent machine with all gears and blueprints visible, the other showing a machine with a locked compartment hiding internal blueprints, illustrating the distinction between open-source and open-weight models",
        "Open-weight gives you the finished product; open-source gives you the recipe, the kitchen, and permission to remodel.",
        1  # After first h2
    ),
    (
        "part-2-understanding-llms/module-09-inference-optimization/section-9.5.html",
        "pruning-bonsai-tree.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A friendly robot gardener carefully trimming branches off a large bonsai tree shaped like a neural network. Some branches being cut are thin and wispy (unstructured pruning), while the robot also removes entire thick branches (structured pruning). The trimmed tree looks more elegant and compact. Small clippings fall into a recycling bin. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A friendly robot gardener trimming a bonsai tree shaped like a neural network, removing both thin wispy branches and entire thick branches, representing unstructured and structured model pruning approaches",
        "Model pruning is the art of making neural networks smaller without making them dumber: trim the right branches and the tree grows stronger.",
        1  # After "Why Pruning Matters"
    ),
    (
        "part-2-understanding-llms/module-09-inference-optimization/section-9.6.html",
        "test-time-compute-thinking-harder.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A cartoon robot sitting at a desk with a difficult math problem. Above its head, multiple thought bubbles branch out like a tree, each bubble showing a different approach to the problem. Some branches have checkmarks, others have X marks. The robot is sweating slightly but looks determined. A meter on the side shows 'thinking budget' being spent. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A cartoon robot at a desk working on a difficult problem with multiple branching thought bubbles above its head, some marked correct and others incorrect, with a thinking budget meter on the side, representing test-time compute and reasoning search strategies",
        "Sometimes the best way to get a smarter answer is not a bigger model, but a model that thinks longer and explores more paths before committing.",
        1  # After "The Test-Time Compute Paradigm"
    ),
    (
        "part-2-understanding-llms/module-09-inference-optimization/section-9.7.html",
        "gpu-kernel-programming.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A cross-section view of a GPU chip reimagined as a tiny city. Thousands of tiny worker robots (threads) march in perfect lockstep through narrow streets (warps). A few special buildings glow brightly (SRAM/shared memory) while a distant warehouse district represents global memory. A robot foreman directs traffic between the fast local streets and the slow highway to the warehouse. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A GPU chip reimagined as a tiny city with thousands of tiny worker robots marching in lockstep through narrow streets, glowing SRAM buildings nearby, and a distant warehouse representing slow global memory, illustrating GPU kernel programming concepts",
        "Writing GPU kernels means choreographing thousands of threads to move data through a memory hierarchy where the fastest storage is also the smallest.",
        1  # After "Why Custom Kernels Matter"
    ),
    (
        "part-2-understanding-llms/module-18-interpretability/section-18.3.html",
        "model-editing-surgery.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A team of tiny robot surgeons performing an operation on a giant brain (representing the model). One surgeon carefully replaces a single glowing neuron (representing a factual association) using tweezers, while monitors display before-and-after knowledge states. Other neurons nearby remain undisturbed. The operating room is clean and organized. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Tiny robot surgeons performing precise surgery on a giant brain, carefully replacing a single glowing neuron with tweezers while monitors show before and after knowledge states, representing model editing techniques like ROME and MEMIT",
        "Model editing lets you fix individual facts in a neural network without retraining the whole thing: brain surgery, not brain replacement.",
        3  # After "Model Editing: ROME and MEMIT"
    ),
    (
        "part-2-understanding-llms/module-18-interpretability/section-18.4.html",
        "explaining-transformers-xray.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A doctor robot holding up a giant X-ray of a transformer model. The X-ray reveals internal layers with different colors showing attention patterns, gradient flows lit up like veins, and highlighted pathways between input and output. The doctor looks thoughtful, pointing at specific bright spots. A patient (a confused-looking transformer block) sits on the examination table. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A doctor robot examining a giant X-ray of a transformer model revealing internal layers with colorful attention patterns and gradient flows, while a confused transformer block sits on the examination table, representing methods for explaining transformer decisions",
        "Explaining transformers is like reading an X-ray of thought: you can trace which inputs lit up which pathways, but the full picture remains tantalizingly incomplete.",
        1  # After "The Explanation Problem"
    ),

    # ── Part 3: Working with LLMs ──
    (
        "part-3-working-with-llms/module-10-llm-apis/section-10.5.html",
        "sparse-model-inference.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A highway system where most roads are empty (zeroed-out weights) and only a few key routes have bustling traffic (active parameters). A traffic controller robot watches a dashboard showing the sparse traffic pattern. Cars on the active routes zoom by quickly. Closed roads have barriers and cobwebs. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A highway system where most roads are empty with barriers and cobwebs representing zeroed-out weights, while a few key routes have bustling traffic representing active parameters, with a traffic controller robot monitoring the sparse pattern",
        "Sparse models skip the empty highways entirely: when most weights are zero, inference can focus compute only on the connections that matter.",
        4  # After "The Wanda Method"
    ),
    (
        "part-3-working-with-llms/module-11-prompt-engineering/section-11.5.html",
        "multimodal-prompting.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A friendly robot DJ at a mixing console with multiple input channels. One channel receives images (photos sliding in), another receives audio waves, another receives text documents. The robot combines all inputs through the mixing board, and the output speaker produces a single coherent response. The DJ wears headphones and looks focused. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A friendly robot DJ at a mixing console combining multiple input channels of images, audio waves, and text documents into a single coherent response through the output speaker, representing multimodal prompting patterns",
        "Multimodal prompting is the art of mixing signals: images, audio, and text each bring unique information, and the prompt engineer orchestrates them into harmony.",
        2  # After "Multimodal Prompting Patterns"
    ),
    (
        "part-3-working-with-llms/module-11-prompt-engineering/section-11.6.html",
        "automatic-prompt-optimization.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot scientist in a laboratory running experiments on prompts. Glass beakers contain different colored prompt variations. The robot feeds prompts into a machine that scores them, and an evolutionary selection process is shown: weaker prompts dissolve while stronger prompts multiply and mutate. A chart on the wall shows prompt quality improving over generations. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot scientist in a laboratory running experiments on prompt variations in glass beakers, feeding them into a scoring machine where weaker prompts dissolve and stronger ones multiply, with a chart showing quality improving over generations",
        "Why write prompts by hand when you can breed them? Automatic prompt optimization treats prompt engineering as a search problem and lets algorithms find what humans might miss.",
        1  # After first h2
    ),
    (
        "part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.2.html",
        "llm-feature-extractor.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A large friendly robot (the LLM) reading documents and producing colorful geometric crystals (embeddings) from each one. A smaller robot (the ML classifier) catches the crystals and sorts them into labeled bins. The large robot does not make the final decision; it just creates the features. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A large robot reading documents and producing colorful geometric crystals representing embeddings, while a smaller robot classifier catches them and sorts them into labeled bins, illustrating how LLMs serve as feature extractors for downstream ML models",
        "The LLM does not need to make every decision: sometimes its best role is turning messy text into clean features that a simpler model can reason about efficiently.",
        1  # After "Embeddings as Features"
    ),
    (
        "part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.5.html",
        "information-extraction-mining.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A team of robots mining in a cave made of text documents. Some robots use precise pickaxes (rule-based NER), others use metal detectors that glow (LLM extraction), and a coordinator robot combines their findings into structured crates of gems (structured data). Raw unstructured rock represents raw text, and the mined gems represent extracted entities and relations. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A team of robots mining in a cave of text documents using different tools: pickaxes for rule-based extraction, glowing metal detectors for LLM extraction, with a coordinator combining findings into structured crates of gems",
        "Information extraction turns unstructured text into structured gold: the best pipelines combine precise rules with flexible LLM understanding.",
        1  # After "The Information Extraction Landscape"
    ),
    (
        "part-3-working-with-llms/module-12-hybrid-ml-llm/section-12.8.html",
        "dataset-engineering-assembly.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A factory assembly line where raw logs (scrolls of paper with chat bubbles) enter one end and get processed through stations: cleaning, formatting, quality filtering, and labeling. Robot workers at each station perform their task. At the end, neat, organized training datasets emerge on golden platters. A quality inspector robot checks samples at the final station. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A factory assembly line processing raw chat logs through cleaning, formatting, filtering, and labeling stations operated by robot workers, with organized training datasets emerging on golden platters at the end",
        "The best LLM applications are only as good as their training data, and dataset engineering is the assembly line that transforms raw logs into learning fuel.",
        1  # After "Log-to-Dataset Pipelines"
    ),

    # ── Part 4: Training & Adapting ──
    (
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.5.html",
        "embedding-finetuning-clustering.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A room full of floating dots (embeddings) that start scattered randomly. A friendly robot teacher gently pushes similar dots together and pulls dissimilar dots apart (contrastive learning). After the robot's work, clusters of same-colored dots form neat groups with clear boundaries between them. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot teacher in a room of floating dots pushing similar ones together and pulling dissimilar ones apart through contrastive learning, resulting in neat clusters with clear boundaries between groups",
        "Fine-tuning for representations teaches the model that similar things should live close together and different things should keep their distance.",
        3  # After "Contrastive Learning for Embeddings"
    ),
    (
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.6.html",
        "classification-head-hat.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A large friendly robot (the pretrained model body) wearing interchangeable hats. Each hat represents a different classification head: a detective hat for sentiment, a medical hat for diagnosis, a legal wig for contract analysis. The robot's body stays the same, only the hat changes for each task. A rack of unused hats sits nearby. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A large robot wearing interchangeable hats representing different classification heads: a detective hat for sentiment, medical hat for diagnosis, and legal wig for contract analysis, with the robot body staying the same across tasks",
        "Classification fine-tuning adds a specialized head to a general body: same powerful foundation, different hat for each job.",
        1  # After "Classification Head Architecture"
    ),
    (
        "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.7.html",
        "long-context-telescope.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot trying to read an enormously long scroll that stretches far beyond the horizon. The robot holds a special telescope (context extension) that compresses the distant parts of the scroll into view, while keeping the nearby parts crisp. Some parts of the scroll are folded (chunking) and others are highlighted with magnifying glass markers (retrieval). The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot reading an enormously long scroll stretching to the horizon, using a special telescope to compress distant parts while keeping nearby text crisp, with some sections folded and others highlighted, representing context extension techniques",
        "Long documents push past the context window, and context extension techniques let models see further without losing the details up close.",
        1  # After "The Long Context Challenge"
    ),
    (
        "part-4-training-adapting/module-15-peft/section-15.3.html",
        "training-platform-toolbox.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A well-organized workshop with different workbenches, each with a distinct personality. One bench has a racing stripe and speed gauges (Unsloth, fast), another has a tidy configuration panel with dials (Axolotl, config-driven), another has a friendly touchscreen (LLaMA-Factory, web UI), and one has clean Pythonicgears (torchtune). A robot mechanic walks between them, choosing the right bench for the job. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A workshop with distinct workbenches representing different training platforms: one with racing stripes for speed, one with configuration dials, one with a touchscreen UI, and one with clean Pythonic gears, with a robot choosing the right bench",
        "Choosing a training platform is like choosing a workbench: some optimize for speed, others for configurability, and the best choice depends on your workflow.",
        0  # Preamble
    ),
    (
        "part-4-training-adapting/module-15-peft/section-15.4.html",
        "soft-prompts-invisible-steering.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A puppet theater stage where the LLM puppet performs on stage. Behind the curtain, a small puppeteer (the soft prompt) pulls invisible strings, subtly guiding the puppet's movements without the audience seeing the control mechanism. The strings are soft and glowing, representing learned continuous vectors rather than hard discrete tokens. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A puppet theater where an LLM puppet performs on stage while a small puppeteer behind the curtain pulls invisible glowing strings, representing soft prompts as learned continuous vectors that guide model behavior without being visible in the output",
        "Soft prompts are invisible steering wheels: a handful of learned vectors that guide the entire model without changing a single original weight.",
        1  # After "The Soft Prompt Family: A Taxonomy"
    ),
    (
        "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.4.html",
        "rlvr-math-judge.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot student solving math problems on a chalkboard. Instead of a human teacher grading the work, an automated judge robot uses a simple calculator to verify answers with a checkmark or X mark. No subjective judgment needed. The robot student improves its approach based on the binary correct/incorrect signal. A stack of solved problems grows taller over time. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot student solving math on a chalkboard while an automated judge robot verifies answers with a calculator giving simple checkmarks or X marks, with a growing stack of correctly solved problems, representing reinforcement learning with verifiable rewards",
        "When the answer is verifiable, you do not need expensive human judges: a simple calculator can tell the model whether it got it right.",
        1  # After "The Verifiable Reward Paradigm"
    ),

    # ── Part 5: Retrieval & Conversation ──
    (
        "part-5-retrieval-conversation/module-20-rag/section-20.5.html",
        "text-to-sql-translator.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A friendly robot translator sitting between two characters who speak different languages. On one side, a business person speaks in natural language questions (speech bubbles with question marks). On the other side, a database shaped like a filing cabinet speaks in structured query language (speech bubbles with table grids). The robot translates between them, occasionally checking a schema reference book. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot translator sitting between a business person speaking natural language questions and a database filing cabinet speaking structured queries, translating between them while checking a schema reference book",
        "Text-to-SQL lets users query databases in plain language, with the LLM serving as a translator between human intent and structured queries.",
        2  # After "Text-to-SQL: Architecture"
    ),
    (
        "part-5-retrieval-conversation/module-20-rag/section-20.6.html",
        "rag-framework-orchestra.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: An orchestra pit where different conductor robots each lead a small ensemble. Each conductor has a different style: one is methodical and chain-like (LangChain), one has an index of sheet music (LlamaIndex), one works with haystacks of documents (Haystack). They all produce the same type of music (RAG output) but with different conducting approaches. A composer robot watches from above, deciding which conductor to hire. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "An orchestra pit with different conductor robots each leading ensembles in distinct styles representing RAG frameworks: one chain-like, one index-focused, one working with document haystacks, all producing the same output",
        "RAG frameworks each solve the same fundamental problem with different philosophies: the best choice depends on your orchestration style, not just features.",
        1  # After "Why Use a RAG Framework?"
    ),
    (
        "part-5-retrieval-conversation/module-20-rag/section-20.7.html",
        "graphrag-knowledge-web.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A spider robot sitting at the center of a glowing knowledge web. The web's nodes are entities (people, places, concepts) connected by labeled relationship strands. Nearby, a traditional search robot flips through flat filing cards (vector search). The spider robot can traverse relationships that the flat search misses, following multi-hop connections. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A spider robot at the center of a glowing knowledge web with entity nodes connected by relationship strands, while a traditional search robot flips through flat filing cards nearby, showing how GraphRAG traverses multi-hop connections that vector search misses",
        "When questions require connecting dots across multiple relationships, knowledge graphs provide the web of connections that flat vector search cannot navigate.",
        1  # After "Why Vector-Only Retrieval Falls Short"
    ),
    (
        "part-5-retrieval-conversation/module-20-rag/section-20.8.html",
        "rag-ingestion-pipeline.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A water treatment plant where dirty, murky water (raw documents in various formats: PDFs, emails, web pages) enters from multiple pipes. The water passes through filtration stages: parsing (removes debris), chunking (divides into manageable portions), embedding (transforms into crystal-clear droplets), and indexing (stores in organized tanks). Clean, indexed water flows out ready for retrieval. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A water treatment plant where murky raw documents enter from multiple pipes and pass through parsing, chunking, embedding, and indexing stages, emerging as clean indexed droplets ready for retrieval",
        "RAG ingestion is water treatment for knowledge: garbage in, garbage out, so the quality of your parsing and chunking determines the quality of every answer downstream.",
        1  # After "Why Ingestion Quality Dominates"
    ),
    (
        "part-5-retrieval-conversation/module-20-rag/section-20.9.html",
        "source-attribution-receipts.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot librarian at a reference desk handing a research paper to a student. Every claim in the paper has a tiny receipt attached to it, linking back to the original source book on the shelf. Some claims have verified receipts (green), others have suspicious receipts that do not match any book (red). The librarian inspects each receipt with a magnifying glass. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot librarian inspecting research papers where each claim has a receipt linking back to source books on shelves, with verified receipts in green and unverifiable ones in red, representing source attribution in RAG systems",
        "Every RAG answer should come with receipts: if you cannot trace a claim back to its source, you cannot trust the answer.",
        1  # After "Why Attribution Matters"
    ),
    (
        "part-5-retrieval-conversation/module-21-conversational-ai/section-21.4.html",
        "conversation-repair-mechanic.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot mechanic in a conversation repair shop. A broken conversation (represented as a tangled, kinked pipe with speech bubbles leaking out) is on the workbench. The mechanic uses tools to straighten the pipe (clarification), plug leaks (disambiguation), and reroute around blockages (fallback strategies). A healthy, smooth conversation pipe hangs on the wall as the goal. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot mechanic in a conversation repair shop fixing a tangled kinked pipe with leaking speech bubbles, using tools to straighten, plug, and reroute, with a healthy smooth conversation pipe displayed as the goal",
        "Conversations break in predictable ways, and the best chatbots are built with repair strategies for every type of conversational pothole.",
        1  # After "Conversation Repair Patterns"
    ),
    (
        "part-5-retrieval-conversation/module-21-conversational-ai/section-21.5.html",
        "voice-multimodal-senses.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot with multiple sensory organs: large ears (speech-to-text), a mouth speaker (text-to-speech), camera eyes (vision), and typing fingers (text input). All senses feed into a central brain that processes everything together. Sound waves, light beams, and text streams all converge into the robot's head. The robot juggles these different modalities with a slightly overwhelmed but cheerful expression. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot with multiple sensory organs including large ears, speaker mouth, camera eyes, and typing fingers, all feeding into a central brain, juggling different modalities with a cheerful expression, representing voice and multimodal interfaces",
        "A truly conversational AI needs more than just text: ears, eyes, and a voice turn a chatbot into something that can interact with the physical world.",
        0  # Preamble
    ),
    (
        "part-5-retrieval-conversation/module-21-conversational-ai/section-21.6.html",
        "voice-agent-latency-race.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A relay race between robots on a track. The first robot (STT) catches a sound wave and converts it into a baton (text). The second robot (LLM) thinks quickly and passes a response baton. The third robot (TTS) converts it back into a sound wave at the finish line. A stopwatch overhead shows milliseconds ticking. The track has markers showing latency budgets for each leg. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A relay race between three robots on a track: one catching sound waves and converting to text, one thinking and responding, one converting back to sound, with a stopwatch showing milliseconds and latency budget markers",
        "Voice AI is a latency relay race: every millisecond saved in speech-to-text, thinking, and text-to-speech adds up to the difference between natural conversation and awkward silence.",
        4  # After "Latency Optimization"
    ),
    (
        "part-5-retrieval-conversation/module-21-conversational-ai/section-21.7.html",
        "human-ai-interaction-study.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A scientist robot observing through a two-way mirror as a human and an AI assistant collaborate on a task. The scientist takes notes on a clipboard, measuring things like trust (a gauge), satisfaction (a smiley meter), and productivity (a speedometer). The human and AI work at a shared desk, with the AI occasionally making helpful suggestions and the human sometimes correcting the AI. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A scientist robot observing through a two-way mirror as a human and AI assistant collaborate, measuring trust, satisfaction, and productivity on gauges, representing human-computer interaction evaluation methods for AI systems",
        "Building good AI assistants requires studying how humans actually use them: measuring trust, productivity, and the subtle dance between human and machine.",
        1  # After "HCI Methods"
    ),

    # ── Part 6: Agentic AI ──
    (
        "part-6-agentic-ai/module-22-ai-agents/section-22.2.html",
        "agent-memory-filing-system.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot office worker at a desk with three distinct memory systems. A sticky note board (working/episodic memory) with recent conversations. A filing cabinet with organized folders (semantic memory) for long-term facts. A muscle memory diagram on the wall (procedural memory) showing practiced routines. The robot consults all three to answer a question. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot office worker with three memory systems: a sticky note board for recent conversations, a filing cabinet for long-term facts, and a muscle memory diagram for practiced routines, representing episodic, semantic, and procedural agent memory",
        "Agents need three kinds of memory: what just happened, what they know, and what they know how to do.",
        2  # After "Episodic, Semantic, and Procedural Memory"
    ),
    (
        "part-6-agentic-ai/module-22-ai-agents/section-22.3.html",
        "agent-planning-chess.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot playing chess against a complex problem. Instead of just making the next move (reactive), the robot visualizes a tree of possible future moves hovering above the board (planning). Some branches glow green (promising), others fade to red (dead ends). The robot also has a mirror showing its last failed attempt (reflection/self-correction). The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot playing chess while visualizing a tree of possible future moves above the board with green promising branches and red dead ends, alongside a mirror showing a last failed attempt for self-correction, representing agent planning strategies",
        "Smart agents do not just react to the next move; they look ahead, explore branching possibilities, and learn from their mistakes.",
        2  # After "Tree of Thoughts and LATS"
    ),
    (
        "part-6-agentic-ai/module-22-ai-agents/section-22.4.html",
        "reasoning-model-agent-thinker.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: Two robot agents side by side. One robot (standard LLM) immediately blurts out an answer with a quick speech bubble. The other robot (reasoning model) has a visible 'thinking cloud' above its head showing step-by-step logical chains, taking longer but arriving at a more carefully considered answer. A cost meter shows the thinking robot using more tokens. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Two robot agents side by side: one immediately blurting an answer, the other with a visible thinking cloud showing step-by-step logic chains, with a cost meter showing the thinker using more tokens, comparing standard and reasoning models as agent backbones",
        "Reasoning models trade speed for depth: they think longer, spend more tokens, but crack problems that quick responses cannot.",
        1  # After "The Reasoning Model Revolution"
    ),
    (
        "part-6-agentic-ai/module-22-ai-agents/section-22.5.html",
        "agent-evaluation-obstacle-course.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: An obstacle course where different robot agents attempt various challenges. Some obstacles test tool use (a locked door requiring a key), others test planning (a maze), others test memory (recalling a previous clue). Judges with clipboards score from the sidelines. Some robots pass easily, others get stuck. A scoreboard shows different benchmark names. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "An obstacle course where robot agents attempt challenges testing tool use, planning, and memory, with judges scoring from the sidelines and a scoreboard showing benchmark names, representing agent evaluation and benchmarks",
        "Evaluating agents is harder than evaluating models: you need obstacle courses that test not just answers, but decisions, tool use, and recovery from failure.",
        1  # After "Why Agent Evaluation Is Hard"
    ),
    (
        "part-6-agentic-ai/module-22-ai-agents/section-22.6.html",
        "agent-architecture-blueprint.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: An architectural blueprint of a robot factory (production agent system) viewed from above. Eight distinct rooms are connected by corridors: an entrance hall (API gateway), a brain room (LLM), a tool workshop, a memory vault, a safety checkpoint, a cost accounting office, a monitoring tower, and an output dock. Data flows along the corridors like pneumatic tubes. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "An architectural blueprint of a robot factory viewed from above showing eight connected rooms: API gateway, LLM brain, tool workshop, memory vault, safety checkpoint, cost office, monitoring tower, and output dock, representing production agent architecture",
        "A production agent is not just an LLM with tools; it is an eight-room factory where every component must be designed for reliability, cost, and safety.",
        1  # After "The Eight Components"
    ),
    (
        "part-6-agentic-ai/module-22-ai-agents/section-22.7.html",
        "agent-memory-layers.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A cross-section of a robot's head showing five nested memory layers like geological strata. The outermost layer (scratchpad) is a thin, quickly-erasable whiteboard. Below it, working memory is a desk with active notes. Deeper, episodic memory stores snapshots of past experiences. Semantic memory holds organized knowledge books. At the core, procedural memory contains hardwired routines. Each layer has a different color and texture. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A cross-section of a robot head showing five nested memory layers like geological strata: a thin scratchpad whiteboard, a working memory desk, episodic snapshot storage, semantic knowledge books, and procedural routines at the core",
        "Agent memory is not one thing; it is five layers deep, from the scratchpad you erase every turn to the procedural habits that persist forever.",
        1  # After "Memory Taxonomy: Five Layers"
    ),
    (
        "part-6-agentic-ai/module-22-ai-agents/section-22.8.html",
        "research-replication-benchmark.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot scientist attempting to rebuild an elaborate Rube Goldberg machine from a research paper's instructions. The original machine is shown in a framed picture on the wall. The robot has some pieces assembled correctly but struggles with ambiguous steps, missing parts, and unexpected failures. A scoring clipboard nearby tracks completion percentage. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot scientist attempting to rebuild a Rube Goldberg machine from a research paper's framed instructions, with some pieces assembled but struggling with ambiguous steps and missing parts, with a scoring clipboard tracking completion",
        "Reproducing research is a benchmark in itself: the gap between a paper's description and a working implementation reveals what we still cannot automate.",
        1  # After "PaperBench"
    ),
    (
        "part-6-agentic-ai/module-25-specialized-agents/section-25.5.html",
        "domain-agent-specialists.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: Three robot specialists in their respective domains. A healthcare robot in a white coat with a stethoscope consulting patient records carefully, a legal robot in a judge's robe reviewing documents with extreme caution, and a finance robot with a calculator analyzing market charts. Each robot has unique safety guardrails visible (barriers, verification steps). The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Three domain specialist robots: a healthcare robot with stethoscope consulting patient records, a legal robot in judge's robe reviewing documents, and a finance robot analyzing charts, each with visible safety guardrails",
        "Domain-specific agents need domain-specific guardrails: what works in finance could be dangerous in healthcare, and the design patterns differ accordingly.",
        0  # Preamble
    ),
    (
        "part-6-agentic-ai/module-25-specialized-agents/section-25.7.html",
        "agentic-coding-workshop.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A modern workshop where a human developer and a robot coder work side by side at a shared terminal. The robot writes code on one half of the screen while the human reviews and guides on the other half. Behind them, autonomous robots work independently at their own stations (fully autonomous agents). A spectrum from 'copilot' to 'autonomous' is suggested by the arrangement. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A workshop where a human developer and robot coder share a terminal, with the robot writing code and the human reviewing, while autonomous robots work independently at background stations, showing the spectrum from copilot to autonomous coding agents",
        "Agentic coding spans a spectrum from helpful copilot to fully autonomous developer, and the right level of autonomy depends on the stakes.",
        1  # After "The Rise of Agentic Coding"
    ),
    (
        "part-6-agentic-ai/module-25-specialized-agents/section-25.8.html",
        "ai-code-quality-inspector.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A quality control conveyor belt where code blocks (represented as colorful building blocks) pass through inspection stations. One station has a security scanner that flags blocks with cracks (vulnerabilities). Another has a correctness tester that drops blocks into test tubes. A third station has a detective looking for hallucinated API calls (blocks that look real but are hollow inside). Some blocks pass, others are rejected. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A quality control conveyor belt where code blocks pass through inspection stations for security scanning, correctness testing, and hallucination detection, with some blocks passing and others being rejected",
        "AI-generated code looks confident, but confidence is not correctness: every block needs scanning for security holes, logic bugs, and hallucinated APIs.",
        1  # After "Security Vulnerabilities"
    ),
    (
        "part-6-agentic-ai/module-26-agent-safety-production/section-26.5.html",
        "multi-agent-testing-chaos.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A fire drill in a robot office. Multiple agent robots that normally collaborate smoothly are now being tested: one robot's message tube is intentionally blocked (network partition), another robot receives contradictory instructions (conflicting messages), and a chaos monkey robot introduces random failures. A test engineer observes from a control room, taking notes on how the system recovers. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A fire drill in a robot office where agent robots face intentional disruptions: blocked message tubes, contradictory instructions, and a chaos monkey introducing failures, while a test engineer observes recovery from a control room",
        "You do not know if your multi-agent system is robust until you try to break it: chaos engineering reveals the failure modes that happy-path testing misses.",
        2  # After "Contract Testing"
    ),
    (
        "part-6-agentic-ai/module-26-agent-safety-production/section-26.7.html",
        "supply-chain-security-fortress.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A medieval fortress (the agent sandbox) with multiple layers of defense. At the gate, a guard checks inventory lists (SBOM). On the walls, watchtower robots scan for vulnerabilities (Trivy). Inside, official seals are stamped on approved packages (Cosign signing). A provenance trail of footprints leads from the forge (build system) to the armory (deployment). The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A medieval fortress representing an agent sandbox with layered defenses: gate guards checking inventory lists, watchtower robots scanning for vulnerabilities, official seals on approved packages, and provenance trails from forge to armory",
        "Agent sandboxes are only as secure as their supply chain: if you do not verify what goes in, you cannot trust what comes out.",
        1  # After first h2
    ),

    # ── Part 7: Multimodal Applications ──
    (
        "part-7-multimodal-applications/module-27-multimodal/section-27.2.html",
        "audio-video-generation-studio.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot film studio with three production departments. In one room, a robot voice actor speaks into a microphone generating sound waves (TTS). In another, a robot musician plays instruments while music notes flow out (music generation). In the third, a robot director operates a camera that projects scenes from imagination onto a screen (video generation). All three rooms connect to a central editing bay. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot film studio with three departments: a voice actor generating sound waves, a musician creating music, and a director projecting imagined scenes, all connected to a central editing bay, representing audio, music, and video generation",
        "Generative AI has learned to speak, compose, and direct: text is just the beginning of what these models can create.",
        0  # Preamble
    ),
    (
        "part-7-multimodal-applications/module-27-multimodal/section-27.4.html",
        "unified-multimodal-fusion.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: Two robots building a bridge. On the left, a 'pipeline' robot connects separate specialized boxes (vision, audio, text) with external pipes and adapters. On the right, a 'native' multimodal robot has all modalities integrated inside a single body, with eyes, ears, and mouth all sharing the same internal wiring. The native robot looks more graceful while the pipeline robot looks functional but clunky. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Two robots: a pipeline robot connecting separate specialized vision, audio, and text boxes with external pipes, and a native multimodal robot with all modalities integrated in one body sharing internal wiring, comparing architectural approaches",
        "Pipeline multimodal systems bolt separate models together; native multimodal models weave all senses into one brain from the start.",
        1  # After "Pipeline vs. Native"
    ),
    (
        "part-7-multimodal-applications/module-27-multimodal/section-27.5.html",
        "robot-vla-model.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot arm in a kitchen attempting to follow a recipe. Its eyes (vision) see the ingredients, its brain (language model) understands the recipe instructions, and its hands (action model) execute the movements. Three colored streams (vision in blue, language in green, action in red) converge into the robot's central processor. The robot carefully picks up an egg. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot arm in a kitchen with vision eyes seeing ingredients, a language brain understanding recipes, and action hands executing movements, with three colored streams converging in a central processor, representing vision-language-action models",
        "Vision-Language-Action models give robots the trifecta: they can see the world, understand instructions, and physically act on them.",
        1  # After "Vision-Language-Action Models"
    ),
    (
        "part-7-multimodal-applications/module-27-multimodal/section-27.6.html",
        "robot-navigation-llm.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot explorer in a forest (representing a warehouse or building). It holds a map in one hand (spatial understanding) and talks to a walkie-talkie (LLM planner giving high-level directions). The robot's feet follow a dotted path on the ground (low-level navigation), while overhead, a drone robot (another agent) provides aerial reconnaissance. Trees have landmark tags. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot explorer in a forest holding a map and talking to a walkie-talkie LLM planner for high-level directions, with feet following a dotted path and a drone providing aerial reconnaissance, representing LLM-powered robot navigation",
        "LLMs give robots the ability to understand high-level navigation commands, but the physical world still requires low-level controllers to handle the messy details.",
        1  # After "LLM Task Planning for Robots"
    ),
    (
        "part-7-multimodal-applications/module-27-multimodal/section-27.7.html",
        "gaussian-splatting-snowglobe.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot artist painting a 3D scene by placing thousands of tiny, colorful, semi-transparent blobs (Gaussian splats) in 3D space. When viewed from the front, the blobs merge into a beautiful coherent scene. A rotating camera orbits the scene, and from each angle, the splats rearrange to show a consistent 3D view. The robot holds a palette of different-sized blobs. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot artist placing thousands of tiny semi-transparent colorful blobs in 3D space that merge into a coherent scene when viewed from the front, with a rotating camera showing consistent 3D views from multiple angles",
        "3D Gaussian splatting reconstructs scenes from a cloud of fuzzy blobs: simple primitives, but their collective effect is photorealistic 3D.",
        2  # After "How 3D Gaussian Splatting Works"
    ),
    (
        "part-7-multimodal-applications/module-28-llm-applications/section-28.2.html",
        "finance-llm-trading-floor.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot analyst on a trading floor. One screen shows news articles being converted into sentiment scores (happy/sad face meters). Another screen shows financial reports being auto-generated. A third screen shows fraud detection with a magnifying glass over suspicious transactions highlighted in red. The robot juggles multiple financial tasks simultaneously. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot analyst on a trading floor with screens showing news sentiment scoring, auto-generated financial reports, and fraud detection with a magnifying glass over suspicious transactions, representing LLM applications in finance",
        "LLMs on the trading floor read the news, write the reports, and flag the fraud: financial AI is becoming a multi-skilled analyst.",
        0  # Preamble
    ),
    (
        "part-7-multimodal-applications/module-28-llm-applications/section-28.3.html",
        "healthcare-ai-assistant.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot doctor in a medical setting with multiple specialties visible. In one area, it reads clinical notes and extracts key information. In another, it answers patient questions from a medical textbook. In a third area, it helps design molecular structures (drug discovery) by assembling building blocks. A prominent caution sign reminds that a human doctor always reviews the robot's work. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot doctor with multiple specialties: reading clinical notes, answering patient questions from a medical textbook, and assembling molecular structures for drug discovery, with a caution sign requiring human review",
        "Medical AI reads notes, answers questions, and even designs molecules, but the most important feature is always the human doctor who checks its work.",
        0  # Preamble
    ),
    (
        "part-7-multimodal-applications/module-28-llm-applications/section-28.4.html",
        "recommendation-search-concierge.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot concierge at a hotel desk helping a guest. Behind the robot, a wall of shelves shows personalized recommendations (items glowing based on user preferences). The robot also has a search lens that can find specific items. A conversation bubble shows the guest describing what they want in natural language, and the robot translates this into a curated selection. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot concierge at a hotel desk with a wall of personalized recommendations and a search lens, translating a guest's natural language request into a curated selection, representing LLM-powered recommendation and search",
        "LLMs transform search and recommendation from keyword matching into conversation: tell the system what you want, and it finds what you mean.",
        1  # After "LLMs as Recommendation Engines"
    ),
    (
        "part-7-multimodal-applications/module-28-llm-applications/section-28.5.html",
        "cybersecurity-llm-shield.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot security guard in a cyber-castle. The robot monitors multiple screens: one shows threat intelligence reports being analyzed, another shows log files with anomalies highlighted in red, and a third shows code being scanned for vulnerabilities. A shield protects the castle from incoming threats. However, a sneaky shadow figure on one screen represents adversarial uses. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot security guard in a cyber-castle monitoring screens for threat intelligence, log anomalies in red, and code vulnerabilities, with a protective shield and a sneaky shadow figure representing adversarial uses",
        "LLMs are both sword and shield in cybersecurity: they analyze threats and detect vulnerabilities, but adversaries wield the same technology.",
        0  # Preamble
    ),
    (
        "part-7-multimodal-applications/module-28-llm-applications/section-28.6.html",
        "education-legal-creative.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot wearing three hats simultaneously, switching between roles. As a teacher, it guides a student through personalized lessons with adaptive difficulty. As a lawyer, it reviews stacks of legal documents with a magnifying glass. As a writer, it collaborates with a human author, each contributing to a shared manuscript. The three roles overlap in the center where the robot stands. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot wearing three hats switching between roles: as teacher guiding personalized lessons, as lawyer reviewing documents, and as writer collaborating with a human on a manuscript, representing education, legal, and creative industry applications",
        "From classroom tutor to legal reviewer to creative collaborator, LLMs wear many professional hats, and each domain brings its own trust requirements.",
        0  # Preamble
    ),
    (
        "part-7-multimodal-applications/module-28-llm-applications/section-28.7.html",
        "robotics-scientific-discovery.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot standing at the intersection of the physical and digital worlds. One arm reaches into a laboratory, manipulating physical equipment (robotics). The other arm reaches into a digital space with swirling equations and molecular structures (scientific discovery). The robot's brain bridges both worlds, translating between language instructions and physical actions. A simulation environment surrounds the robot like a training ground. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot at the intersection of physical and digital worlds, one arm in a laboratory manipulating equipment and the other in a digital space with equations and molecules, bridging language instructions and physical actions",
        "When LLMs meet robotics and science, language becomes the interface between understanding the world and physically changing it.",
        0  # Preamble
    ),

    # ── Part 8: Evaluation & Production ──
    (
        "part-8-evaluation-production/module-29-evaluation-observability/section-29.11.html",
        "long-context-needle-haystack.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot searching for glowing needles hidden in an enormous haystack that stretches to the horizon. The robot uses different search strategies: one hand holds a magnet (attention mechanism), the other holds a systematic grid overlay (benchmark methodology). Some needles near the top are easy to find, but needles deep in the middle and bottom of the haystack are increasingly hard to detect. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot searching for glowing needles in an enormous haystack stretching to the horizon, using a magnet and systematic grid overlay, with needles near the top easy to find but those deep in the middle increasingly hard to detect",
        "Long-context benchmarks reveal an uncomfortable truth: models claim to handle 128K tokens, but their ability to find information drops sharply with depth.",
        2  # After "Needle-in-a-Haystack"
    ),
    (
        "part-8-evaluation-production/module-29-evaluation-observability/section-29.13.html",
        "research-methodology-lab.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A methodical robot scientist in a pristine laboratory, carefully running a controlled experiment. On one side, the variable being tested (a glowing prompt) is isolated under a glass dome. On the other side, a control group remains unchanged. The robot meticulously records results in a notebook, while a reproducibility seal stamp waits nearby. Error bars and confidence intervals float above the experiment like halos. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A methodical robot scientist running a controlled experiment with a test variable under a glass dome and an unchanged control group, recording results while error bars and confidence intervals float above like halos",
        "Rigorous research methodology is what separates publishable findings from expensive anecdotes: control your variables, report your uncertainties, and make your work reproducible.",
        1  # After "Experiment Design"
    ),
    (
        "part-8-evaluation-production/module-29-evaluation-observability/section-29.14.html",
        "hardware-benchmarking-racetrack.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A racetrack where different GPU robots compete in an LLM inference race. Each GPU robot has different specs and sizes. They race through checkpoints labeled with performance metrics (tokens per second, latency, throughput). Some GPUs are fast on straightaways but slow on turns (good at throughput, bad at latency). A cross-platform portability bridge connects different hardware lanes. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "GPU robots racing on a track through checkpoints labeled with performance metrics, with some fast on straightaways but slow on turns, and a portability bridge connecting different hardware lanes, representing LLM inference benchmarking",
        "Benchmarking LLM inference across hardware is a multi-dimensional race: the winner changes depending on whether you measure latency, throughput, or cost per token.",
        1  # After "MLPerf Training and Inference Suites"
    ),
    (
        "part-8-evaluation-production/module-31-production-engineering/section-31.4.html",
        "llmops-continuous-improvement.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A continuous improvement wheel (like a waterwheel) powered by user feedback flowing in as water. The wheel turns through stages: prompt versioning (filing cabinet with version numbers), A/B testing (two doors side by side with different results), monitoring (a dashboard with gauges), and model registry (a trophy case of model versions). The wheel keeps spinning, getting better each rotation. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A continuous improvement waterwheel powered by user feedback flowing through stages of prompt versioning, A/B testing, monitoring dashboards, and model registry, with each rotation improving quality",
        "LLMOps is a flywheel, not a one-time deployment: each cycle of feedback, testing, and iteration makes the system incrementally smarter.",
        0  # Preamble
    ),
    (
        "part-8-evaluation-production/module-31-production-engineering/section-31.6.html",
        "durable-execution-safety-net.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A tightrope walker robot performing a complex multi-step task on a high wire. Below the wire, a large safety net (durable execution framework) catches any fallen steps. Checkpoints along the wire are marked with save flags. When the robot slips (a failure occurs), it bounces on the net and resumes from the last checkpoint rather than starting over. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A tightrope walker robot performing multi-step tasks on a high wire with a safety net below for durable execution, save flag checkpoints along the wire, and the robot bouncing back from the last checkpoint after slipping",
        "Durable execution means never losing progress: when a long-running agent workflow crashes, it picks up from the last checkpoint instead of starting from scratch.",
        1  # After "Why LLM Agents Need Durable Execution"
    ),
    (
        "part-8-evaluation-production/module-31-production-engineering/section-31.9.html",
        "kubernetes-gpu-scheduling.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A busy train station where GPU train cars (each with a glowing GPU chip logo) are assigned to different platforms by a dispatcher robot (Kubernetes scheduler). Some trains are large (full GPU allocation), others share tracks (GPU sharing). A scaling control tower monitors traffic and adds more trains during peak hours. Waiting passengers (LLM inference requests) queue orderly at each platform. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A train station where GPU train cars are assigned to platforms by a Kubernetes dispatcher robot, with some trains large and others sharing tracks, a scaling control tower monitoring traffic, and inference requests queuing at platforms",
        "Kubernetes GPU scheduling is like running a train station: the dispatcher must balance full-size trains, shared tracks, and rush-hour demand without stranding any passengers.",
        1  # After "GPU Scheduling for LLM Training"
    ),

    # ── Part 9: Safety & Strategy ──
    (
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.10.html",
        "cross-cultural-alignment.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A round table with robots from different cultures (wearing different cultural hats and accessories) trying to agree on a single response. Each robot points to different values on a shared whiteboard, and the values partially overlap but also conflict. A mediator robot in the center tries to find common ground. The diversity of perspectives is visually represented by different colored lenses each robot wears. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Robots from different cultures at a round table with different cultural accessories trying to agree on values shown on a whiteboard, with partially overlapping and conflicting preferences, and a mediator robot seeking common ground",
        "Alignment is not universal: what counts as helpful, harmless, and honest depends on cultural context, and a single set of values cannot represent everyone.",
        3  # After "Pluralistic Alignment"
    ),
    (
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.12.html",
        "privacy-attacks-vault.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A bank vault (the trained model) with layers of security. A sneaky detective robot tries different attack methods: listening at the vault door (extraction attacks), checking if a specific document was stored inside (membership inference), and picking the lock (prompt injection for PII). Inside the vault, training data is visible through cracks. A privacy shield robot applies differential privacy noise like a fog machine, obscuring the contents. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A sneaky detective robot trying various attacks on a bank vault representing a trained model, with extraction listening, membership inference checking, and lock picking, while a privacy shield robot applies differential privacy noise like fog",
        "Trained models are leaky vaults: attackers can extract training data, infer membership, and probe for PII unless differential privacy adds enough noise to the lock.",
        1  # After "Training Data Extraction Attacks"
    ),
    (
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.5.html",
        "risk-governance-audit.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot auditor with a clipboard walking through a model warehouse. Models on shelves are tagged with risk levels: green (low), yellow (medium), red (high). The auditor checks each model against a governance framework checklist. Some models have approval stamps, others have warning flags. A governance board of robot executives reviews audit reports in a boardroom visible through a window. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot auditor with a clipboard in a model warehouse where models on shelves are tagged with green, yellow, and red risk levels, checking against a governance framework while a governance board reviews reports in a boardroom",
        "Governance without auditing is wishful thinking: every model needs a risk tag, a compliance check, and a paper trail.",
        1  # After "Governance Frameworks Comparison"
    ),
    (
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.6.html",
        "llm-licensing-spectrum.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A spectrum of doors representing different model licenses. On one end, a wide-open door with a welcome mat (fully open source, Apache/MIT). In the middle, a door with a bouncer checking IDs and a list of restrictions (restricted licenses like Llama). On the far end, a locked door with a keycard reader and a corporate logo (proprietary API-only access). A robot walks along the spectrum, choosing which door matches its needs. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A spectrum of doors from wide open with welcome mat (open source) to a door with a bouncer and restrictions (restricted license) to a locked corporate door (proprietary API), with a robot choosing which door fits its needs",
        "Model licenses are not all created equal: from fully open to API-only, the door you walk through determines what you can build and where you can deploy it.",
        1  # After "Model License Taxonomy"
    ),
    (
        "part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.9.html",
        "eu-ai-act-compliance.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A pyramid of AI applications sorted by risk level, EU-style. At the base, minimal-risk applications (a chatbot) play freely. In the middle, high-risk applications (a medical robot, a hiring robot) go through security checkpoints and documentation requirements. At the top, unacceptable-risk applications (a surveillance robot) are behind a red barrier with a stop sign. An EU flag flies above the pyramid. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A pyramid of AI applications sorted by EU risk levels: minimal-risk chatbots playing freely at the base, high-risk medical and hiring robots going through checkpoints in the middle, and unacceptable-risk surveillance behind a red barrier at the top",
        "The EU AI Act sorts every AI application into a risk pyramid: the higher the stakes, the more documentation, testing, and oversight you need to deploy.",
        1  # After "Risk Classification"
    ),

    # ── Part 10: Frontiers ──
    (
        "part-10-frontiers/module-34-emerging-architectures/section-34.10.html",
        "universal-sequence-machine.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A universal translator machine with multiple input ports. DNA strands enter one port, protein sequences enter another, molecular formulas enter a third, and time series data enters a fourth. Inside the machine, all inputs are converted to the same token format and processed by the same transformer core. Outputs emerge as predictions specific to each domain. The machine wears a crown suggesting its versatility. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A universal translator machine with input ports for DNA strands, protein sequences, molecular formulas, and time series, all converted to tokens and processed by the same transformer core, producing domain-specific predictions",
        "The transformer does not care what language you speak: DNA, proteins, molecules, and time series are all just sequences waiting to be modeled.",
        2  # After "Tokenization Strategies Across Domains"
    ),
    (
        "part-10-frontiers/module-34-emerging-architectures/section-34.2.html",
        "scaling-frontiers-three-axes.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot mountaineer at a three-way fork in a mountain trail. One path leads up 'Data Mountain' (but a wall blocks the way, representing the data wall). Another path leads up 'Compute Peak' (steep and expensive). The third path leads up 'Algorithm Ridge' (creative but uncertain). The robot studies a map trying to decide which path to climb. Synthetic data clouds float near the data path. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot mountaineer at a three-way fork with paths leading to Data Mountain blocked by a wall, steep expensive Compute Peak, and uncertain Algorithm Ridge, studying a map, with synthetic data clouds near the data path",
        "Scaling has three axes, and each one has its own ceiling: more data hits a wall, more compute hits a budget, and better algorithms hit the unknown.",
        3  # After "The Three Axes of Scaling"
    ),
    (
        "part-10-frontiers/module-34-emerging-architectures/section-34.7.html",
        "mechanistic-interpretability-microscope.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A scientist robot peering through an enormous microscope into the hidden layers of a neural network. Through the lens, tiny features are visible as distinct colored organisms (sparse autoencoder features). Some features cluster into circuits (connected by visible wires). The scientist carefully catalogs each discovered feature in a field journal. The scale contrast between the scientist and the vast network landscape is dramatic. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A scientist robot peering through an enormous microscope into neural network hidden layers, seeing tiny colored feature organisms clustering into circuits connected by wires, cataloging discoveries in a field journal",
        "Mechanistic interpretability is neuroscience for neural networks: peer deep enough and you find individual features, circuits, and the logic that connects them.",
        1  # After "The Superposition Hypothesis"
    ),
    (
        "part-10-frontiers/module-34-emerging-architectures/section-34.8.html",
        "agency-spectrum.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A spectrum showing robots at different levels of agency. On the left, a simple chatbot robot only responds when asked (reactive). In the middle, a robot with tools and a to-do list makes plans and takes actions (agentic). On the far right, a robot that sets its own goals, modifies its own code, and creates sub-agents (autonomous). Each robot is progressively more independent, with the rightmost one slightly unsettling. Warning signs increase toward the right. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A spectrum of robots at different agency levels: a simple chatbot only responding when asked on the left, a planning robot with tools in the middle, and an autonomous goal-setting robot creating sub-agents on the right, with increasing warning signs",
        "The spectrum from chatbot to autonomous agent is not just a technical distinction; it is a safety gradient where each level of independence demands stronger guardrails.",
        2  # After "A Spectrum of Agency"
    ),
    (
        "part-10-frontiers/module-34-emerging-architectures/section-34.9.html",
        "tool-economy-marketplace.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A marketplace where agent robots browse tool stalls. Each tool has a price tag showing its token cost and latency. A savvy shopper robot compares tools, using a calculator to figure out the best value. Some tools are cached (pre-made items on a shelf), while others are made-to-order (fresh API calls). A parallel execution lane shows multiple tools being used simultaneously. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Agent robots browsing a tool marketplace where each tool has token cost and latency price tags, with a shopper robot comparing value, cached items on shelves, and a parallel execution lane for simultaneous tool use",
        "Every tool call has a price in tokens and latency, and smart agents shop for the best value: caching, parallelizing, and skipping calls that are not worth the cost.",
        1  # After "The Cost Anatomy of a Tool Call"
    ),
    (
        "part-10-frontiers/module-35-ai-society/section-35.2.html",
        "ai-governance-puzzle.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A giant jigsaw puzzle representing AI governance, with different nations' robots each holding puzzle pieces. Some pieces fit together (international cooperation), but others have incompatible edges (regulatory fragmentation). A compute governance piece glows in the center as the keystone. Open-weight model pieces debate whether to lock or unlock. Some puzzle areas are complete, others have gaping holes (open problems). The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A giant jigsaw puzzle of AI governance with national robots holding pieces, some fitting together and others incompatible, a glowing compute governance keystone in the center, and open-weight pieces debating locks, with gaping holes for open problems",
        "AI governance is a global puzzle with no box lid: every nation holds pieces, but nobody has seen the finished picture.",
        0  # Preamble
    ),
    (
        "part-10-frontiers/module-35-ai-society/section-35.3.html",
        "societal-impact-ripples.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A stone (representing AI) dropped into a pond, creating concentric ripple circles. Each ripple ring represents a different sector being affected: the innermost ring shows tech workers and programmers, the next ring shows educators and students, then creative artists, then scientists, and the outermost ring shows society at large. Some figures ride the waves (benefiting), others struggle to stay afloat (disrupted). The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A stone representing AI dropped into a pond creating concentric ripple circles, each ring showing a different sector: tech workers, educators, artists, scientists, and society, with some riding the waves and others struggling",
        "AI's impact ripples outward from tech into every sector of society, and the farther it spreads, the harder it becomes to predict who rides the wave and who gets swept under.",
        0  # Preamble
    ),
    (
        "part-10-frontiers/module-35-ai-society/section-35.4.html",
        "open-research-questions.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot explorer standing at the edge of a vast, partly mapped territory. Behind the robot, well-charted lands represent solved problems. Ahead, uncharted territory stretches to the horizon with question marks floating above it. Signposts point in different research directions: 'What do models learn?', 'How to align safely?', 'How to make AI accessible?', 'How to evaluate properly?', and 'Data rights?' (but shown as icons, not text). The robot holds binoculars and a compass. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot explorer at the edge of mapped territory with solved problems behind and vast uncharted land ahead with floating question marks, directional signposts as icons, holding binoculars and a compass, representing open research frontiers",
        "The most exciting problems in AI are the ones we have not solved yet: the frontier is vast, partly charted, and full of questions that will define the next decade.",
        0  # Preamble
    ),
    (
        "part-10-frontiers/module-35-ai-society/section-35.6.html",
        "agent-cicd-pipeline.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A factory assembly line for agent software. Code enters on one end, passes through testing stations (unit tests, integration tests, golden trace comparison), then through a deployment gate (canary deployment shown as a small bird testing the path), and finally arrives in production. Monitoring cameras watch the production end. A rollback conveyor belt runs underneath in case of failures. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A factory assembly line for agent software with code passing through testing stations, a canary deployment bird at the gate, production monitoring cameras, and a rollback conveyor belt running underneath for failures",
        "Agent CI/CD is not just about shipping code; it is about shipping confidence through testing, canary deployment, and always having a rollback lane.",
        5  # After "Putting It Together"
    ),
    (
        "part-10-frontiers/module-35-ai-society/section-35.7.html",
        "agent-memory-architecture.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A robot librarian managing a complex library system. Short-term memory is a small desk with a few open books. Working memory is a larger table with active projects spread out. Long-term memory is floor-to-ceiling bookshelves with an index card catalog. The librarian uses a retrieval system (a mechanical arm) to fetch relevant books when needed. A garbage collection robot sweeps old, unused books into a recycling bin. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "A robot librarian managing a library with short-term memory as a small desk, working memory as a project table, long-term memory as floor-to-ceiling shelves, a mechanical retrieval arm, and a garbage collection robot sweeping old books",
        "Agent memory architectures mirror how libraries work: different storage tiers for different purposes, smart retrieval for what matters, and garbage collection for what does not.",
        1  # After "A Taxonomy of Agent Memory"
    ),

    # ── Part 11: Idea to Product ──
    (
        "part-11-idea-to-product/module-38-shipping-scaling/section-38.5.html",
        "capstone-assessment-finish-line.png",
        "Simple, cartoon-like educational illustration with clean lines and a warm color palette: A graduation ceremony for robots. Robot students cross a finish line wearing mortarboard caps, each carrying a completed project (a glowing prototype). Judges with rubric clipboards evaluate the projects. Behind the finish line, the road ahead stretches into the distance with new challenges and opportunities. Confetti falls as the robots celebrate completing the course. The style should be friendly and approachable, like an XKCD-inspired infographic. No text or lettering in the image.",
        "Robot students crossing a graduation finish line wearing mortarboard caps carrying glowing prototypes, with judges evaluating from rubric clipboards and the road ahead stretching into the distance with confetti falling",
        "Finishing a capstone project is not the end; it is the starting line for building real products that solve real problems.",
        0  # Preamble
    ),
]

# Write prompts file
prompts_path = BOOK_ROOT / "scripts" / "illustration_batch_prompts.txt"
prompts = [s[2] for s in sections]
prompts_path.write_text("\n".join(prompts), encoding="utf-8")

# Write mapping file for post-generation embedding
mapping_path = BOOK_ROOT / "scripts" / "illustration_mapping.json"
mapping = []
for s in sections:
    mapping.append({
        "section_path": s[0],
        "image_filename": s[1],
        "alt_text": s[3],
        "caption": s[4],
        "placement_h2": s[5],
    })
mapping_json = json.dumps(mapping, indent=2, ensure_ascii=False)
mapping_path.write_text(mapping_json, encoding="utf-8")

print(f"Generated {len(prompts)} prompts to {prompts_path}")
print(f"Generated mapping to {mapping_path}")
print(f"Sections covered: {len(sections)}")
