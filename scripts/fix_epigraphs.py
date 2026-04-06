"""Replace TODO epigraphs in all appendix section files."""
import re
from pathlib import Path

# Map: (file_path_suffix, quote, attribution)
EPIGRAPHS = [
    # Appendix A: Mathematical Foundations
    ("appendix-a-mathematical-foundations/section-a.1.html",
     "The book of nature is written in the language of mathematics.",
     "Galileo Galilei"),
    ("appendix-a-mathematical-foundations/section-a.2.html",
     "Probability is the very guide of life.",
     "Cicero"),
    ("appendix-a-mathematical-foundations/section-a.3.html",
     "The gradient points uphill; wisdom is knowing when to walk the other way.",
     "Anonymous optimization researcher"),
    ("appendix-a-mathematical-foundations/section-a.4.html",
     "Information is the resolution of uncertainty.",
     "Claude Shannon"),
    ("appendix-a-mathematical-foundations/section-a.5.html",
     "Mathematics is not about numbers, equations, or algorithms: it is about understanding.",
     "William Paul Thurston"),

    # Appendix B: ML Essentials
    ("appendix-b-ml-essentials/section-b.1.html",
     "All models are wrong, but some are useful.",
     "George E. P. Box"),
    ("appendix-b-ml-essentials/section-b.2.html",
     "An approximate answer to the right problem is worth a good deal more than an exact answer to an approximate problem.",
     "John Tukey"),
    ("appendix-b-ml-essentials/section-b.3.html",
     "With four parameters I can fit an elephant, and with five I can make him wiggle his trunk.",
     "John von Neumann"),
    ("appendix-b-ml-essentials/section-b.4.html",
     "If you torture the data long enough, it will confess to anything.",
     "Ronald Coase"),

    # Appendix C: Python for LLM
    ("appendix-c-python-for-llm/section-c.1.html",
     "Life is short; use Python.",
     "Bruce Eckel"),
    ("appendix-c-python-for-llm/section-c.2.html",
     "The best code is the code that runs in the environment you actually set up.",
     "Every ML engineer who forgot to activate their venv"),
    ("appendix-c-python-for-llm/section-c.3.html",
     "A notebook is a thinking tool that happens to run code.",
     "Fernando Perez, creator of IPython"),
    ("appendix-c-python-for-llm/section-c.4.html",
     "Simplicity is prerequisite for reliability.",
     "Edsger W. Dijkstra"),

    # Appendix D: Environment Setup
    ("appendix-d-environment-setup/section-d.1.html",
     "Hardware eventually fails. Software eventually works.",
     "Michael Hartung"),
    ("appendix-d-environment-setup/section-d.2.html",
     "The driver is the soul of the GPU. Without it, you have a very expensive space heater.",
     "Frustrated CUDA developer proverb"),
    ("appendix-d-environment-setup/section-d.3.html",
     "In the beginning was the command line.",
     "Neal Stephenson"),
    ("appendix-d-environment-setup/section-d.4.html",
     "Dependency management is 90% of machine learning engineering. The other 90% is debugging shape mismatches.",
     "Folk wisdom of ML Twitter"),
    ("appendix-d-environment-setup/section-d.5.html",
     "The cloud is just someone else's computer, but at least it has GPUs.",
     "Every ML practitioner, eventually"),
    ("appendix-d-environment-setup/section-d.6.html",
     "Trust, but verify.",
     "Russian proverb, adopted by every DevOps engineer"),

    # Appendix E: Git Collaboration
    ("appendix-e-git-collaboration/section-e.1.html",
     "If it is not in version control, it does not exist.",
     "Ancient software engineering proverb"),
    ("appendix-e-git-collaboration/section-e.2.html",
     "Data is the new oil, but without version control, you are just spilling it everywhere.",
     "Dmitry Petrov, DVC creator"),
    ("appendix-e-git-collaboration/section-e.3.html",
     "An experiment not recorded is an experiment not performed.",
     "Adapted from a chemistry lab maxim"),
    ("appendix-e-git-collaboration/section-e.4.html",
     "Reproducibility: the ability to get the same wrong answer twice.",
     "Every honest scientist"),

    # Appendix F: Glossary
    ("appendix-f-glossary/section-f.1.html",
     "Give someone a library and they will build for a day. Teach them to read the docs and they will build forever.",
     "Adapted from a proverb"),
    ("appendix-f-glossary/section-f.2.html",
     "Naming things is one of the two hard problems in computer science.",
     "Phil Karlton"),
    ("appendix-f-glossary/section-f.3.html",
     "An algorithm must be seen to be believed.",
     "Donald Knuth"),
    ("appendix-f-glossary/section-f.4.html",
     "Natural language processing is the art of getting computers to do useful things with human language, which is itself an art.",
     "Adapted from Dan Jurafsky"),
    ("appendix-f-glossary/section-f.5.html",
     "In theory, there is no difference between theory and practice. In practice, there is.",
     "Jan L. A. van de Snepscheut"),

    # Appendix G: Hardware & Compute
    ("appendix-g-hardware-compute/section-g.1.html",
     "More compute has solved more problems than any clever algorithm.",
     "Rich Sutton, paraphrased from 'The Bitter Lesson'"),
    ("appendix-g-hardware-compute/section-g.2.html",
     "There is no cloud. It is just someone else's data center, and they charge by the hour.",
     "Overheard at an ML infrastructure meetup"),
    ("appendix-g-hardware-compute/section-g.3.html",
     "Choosing a GPU is like choosing a car: everyone has opinions, nobody reads the specs, and you will overspend.",
     "Anonymous ML engineer"),
    ("appendix-g-hardware-compute/section-g.4.html",
     "What gets measured gets managed, and what gets estimated gets budgeted.",
     "Adapted from Peter Drucker"),
    ("appendix-g-hardware-compute/section-g.5.html",
     "Configuration is the last mile of machine learning infrastructure, and the longest.",
     "Chip Huyen"),

    # Appendix H: Model Cards
    ("appendix-h-model-cards/section-h.1.html",
     "With great models come great API bills.",
     "Every startup CTO"),
    ("appendix-h-model-cards/section-h.2.html",
     "Open weights are the peer review of the AI era.",
     "Yann LeCun, paraphrased"),
    ("appendix-h-model-cards/section-h.3.html",
     "Benchmarks tell you what a model can do. Deployment tells you what it actually will do.",
     "Shreya Shankar"),

    # Appendix I: Prompt Templates
    ("appendix-i-prompt-templates/section-i.1.html",
     "To classify is human; to classify at scale is AI.",
     "Adapted from Alexander Pope"),
    ("appendix-i-prompt-templates/section-i.2.html",
     "Brevity is the soul of wit, and apparently the entire job description of a summarization model.",
     "Adapted from Shakespeare"),
    ("appendix-i-prompt-templates/section-i.3.html",
     "Information extraction is the art of finding needles in haystacks without catching the hay on fire.",
     "Anonymous NLP practitioner"),
    ("appendix-i-prompt-templates/section-i.4.html",
     "The important thing is not to stop questioning.",
     "Albert Einstein"),
    ("appendix-i-prompt-templates/section-i.5.html",
     "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
     "Martin Fowler"),
    ("appendix-i-prompt-templates/section-i.6.html",
     "Let us think step by step. No, seriously, that actually works.",
     "Kojima et al., 2022, paraphrased"),
    ("appendix-i-prompt-templates/section-i.7.html",
     "The persona you give an LLM matters more than most people realize.",
     "Ethan Mollick"),
    ("appendix-i-prompt-templates/section-i.8.html",
     "Reasoning models do not need you to hold their hand. They need you to clearly describe the destination.",
     "Adapted from OpenAI best practices"),

    # Appendix J: Datasets & Benchmarks
    ("appendix-j-datasets-benchmarks/section-j.1.html",
     "Data is the new oil, but most of it needs refining.",
     "Adapted from Clive Humby"),
    ("appendix-j-datasets-benchmarks/section-j.2.html",
     "The quality of your model is bounded by the quality of your instructions.",
     "Yizhong Wang et al., paraphrased"),
    ("appendix-j-datasets-benchmarks/section-j.3.html",
     "When a measure becomes a target, it ceases to be a good measure.",
     "Goodhart's Law"),
    ("appendix-j-datasets-benchmarks/section-j.4.html",
     "Not everything that counts can be counted, and not everything that can be counted counts.",
     "William Bruce Cameron"),
    ("appendix-j-datasets-benchmarks/section-j.5.html",
     "A license is a love letter from a lawyer. Read it carefully.",
     "Anonymous open-source advocate"),

    # Appendix K: HuggingFace Ecosystem
    ("appendix-k-huggingface-ecosystem/section-k.1.html",
     "Transformers made NLP accessible. The Transformers library made it a one-liner.",
     "Thomas Wolf, paraphrased"),
    ("appendix-k-huggingface-ecosystem/section-k.2.html",
     "A model is only as good as the data you feed it, and the tokenizer that chews it up first.",
     "Anonymous HuggingFace contributor"),
    ("appendix-k-huggingface-ecosystem/section-k.3.html",
     "Training a model is like baking: the recipe matters, but so does the oven.",
     "Sylvain Gugger, paraphrased"),
    ("appendix-k-huggingface-ecosystem/section-k.4.html",
     "Why fine-tune all the parameters when you can fine-tune just the ones that matter?",
     "Edward Hu et al., on LoRA"),
    ("appendix-k-huggingface-ecosystem/section-k.5.html",
     "The best model is the one other people can actually use.",
     "Clement Delangue, paraphrased"),

    # Appendix L: LangChain
    ("appendix-l-langchain/section-l.1.html",
     "The chain is only as strong as its weakest prompt.",
     "Adapted from Thomas Reid"),
    ("appendix-l-langchain/section-l.2.html",
     "Without memory, every conversation is a first date.",
     "Anonymous chatbot developer"),
    ("appendix-l-langchain/section-l.3.html",
     "The right chunk size is always the one you have not tried yet.",
     "Every RAG developer at 2 AM"),
    ("appendix-l-langchain/section-l.4.html",
     "Structured output is the difference between a demo and a product.",
     "Harrison Chase, paraphrased"),
    ("appendix-l-langchain/section-l.5.html",
     "An agent is just a for-loop with an LLM inside and a budget you will regret.",
     "Anonymous ML engineer"),

    # Appendix M: LangGraph
    ("appendix-m-langgraph/section-m.1.html",
     "A graph is worth a thousand if-else statements.",
     "Adapted from a software proverb"),
    ("appendix-m-langgraph/section-m.2.html",
     "Cycles in a graph are a feature. Infinite cycles in production are a bug.",
     "Nuno Campos, paraphrased"),
    ("appendix-m-langgraph/section-m.3.html",
     "The best AI systems know when to ask for help.",
     "Saleena Amershi, paraphrased"),
    ("appendix-m-langgraph/section-m.4.html",
     "Checkpointing is the art of making failure recoverable.",
     "Jim Gray"),
    ("appendix-m-langgraph/section-m.5.html",
     "One agent is a tool. A team of agents is either an orchestra or a food fight.",
     "Anonymous multi-agent developer"),

    # Appendix N: CrewAI
    ("appendix-n-crewai/section-n.1.html",
     "Every agent needs a role, a goal, and enough backstory to stay in character.",
     "Joao Moura, CrewAI creator, paraphrased"),
    ("appendix-n-crewai/section-n.2.html",
     "A well-defined task is half the solution.",
     "Charles Kettering, adapted"),
    ("appendix-n-crewai/section-n.3.html",
     "Give an agent the right tools and it will surprise you. Give it the wrong tools and it will surprise you more.",
     "Anonymous agent developer"),
    ("appendix-n-crewai/section-n.4.html",
     "Teamwork makes the dream work, even when the team is made of language models.",
     "Adapted from John C. Maxwell"),
    ("appendix-n-crewai/section-n.5.html",
     "Delegation is the art of getting agents to do work you are too expensive to do yourself.",
     "Adapted from a management proverb"),

    # Appendix O: LlamaIndex
    ("appendix-o-llamaindex/section-o.1.html",
     "Your data is trapped in files. A good connector sets it free.",
     "Jerry Liu, LlamaIndex creator, paraphrased"),
    ("appendix-o-llamaindex/section-o.2.html",
     "The index is the map. Without it, retrieval is just wandering.",
     "Anonymous information retrieval researcher"),
    ("appendix-o-llamaindex/section-o.3.html",
     "The best answer is the one assembled from the right pieces.",
     "Anonymous RAG practitioner"),
    ("appendix-o-llamaindex/section-o.4.html",
     "When one retriever is not enough, route, decompose, and fuse.",
     "LlamaIndex documentation, paraphrased"),
    ("appendix-o-llamaindex/section-o.5.html",
     "Agents are what happen when you give an LLM a to-do list and a set of tools.",
     "Anonymous AI engineer"),

    # Appendix P: Semantic Kernel
    ("appendix-p-semantic-kernel/section-p.1.html",
     "A kernel is the core of an operating system. A Semantic Kernel is the core of an AI application.",
     "Microsoft Semantic Kernel documentation, adapted"),
    ("appendix-p-semantic-kernel/section-p.2.html",
     "A good template is a conversation starter between developer and model.",
     "Matthew Bolanos, paraphrased"),
    ("appendix-p-semantic-kernel/section-p.3.html",
     "Planning is everything. Plans are nothing.",
     "Dwight D. Eisenhower, adapted for AI agents"),
    ("appendix-p-semantic-kernel/section-p.4.html",
     "Memory is the thread that weaves isolated responses into coherent dialogue.",
     "Anonymous conversational AI researcher"),
    ("appendix-p-semantic-kernel/section-p.5.html",
     "Enterprise readiness is not a feature. It is a thousand small decisions made correctly.",
     "Satya Nadella, paraphrased"),

    # Appendix Q: DSPy
    ("appendix-q-dspy/section-q.1.html",
     "Prompting is the assembly language of LLMs. DSPy is the compiler.",
     "Omar Khattab, paraphrased"),
    ("appendix-q-dspy/section-q.2.html",
     "Why write prompts by hand when you can declare what you want and let the optimizer figure it out?",
     "The DSPy philosophy, paraphrased"),
    ("appendix-q-dspy/section-q.3.html",
     "Optimization without good metrics is just expensive random search.",
     "Anonymous ML researcher"),
    ("appendix-q-dspy/section-q.4.html",
     "You cannot improve what you cannot measure.",
     "Lord Kelvin"),
    ("appendix-q-dspy/section-q.5.html",
     "Assertions turn silent failures into loud, fixable ones.",
     "Adapted from debugging folklore"),

    # Appendix R: Experiment Tracking
    ("appendix-r-experiment-tracking/section-r.1.html",
     "If you did not log it, it did not happen.",
     "Weights and Biases community saying"),
    ("appendix-r-experiment-tracking/section-r.2.html",
     "An ML pipeline without tracking is a kitchen without measuring cups.",
     "Matei Zaharia, paraphrased"),
    ("appendix-r-experiment-tracking/section-r.3.html",
     "Hyperparameter tuning is the fine art of spending compute to save compute.",
     "Anonymous ML engineer"),
    ("appendix-r-experiment-tracking/section-r.4.html",
     "A model without a registry is a ship without a port.",
     "Adapted from a DevOps proverb"),
    ("appendix-r-experiment-tracking/section-r.5.html",
     "Observability is not about watching dashboards. It is about knowing where to look when things go wrong.",
     "Charity Majors, paraphrased"),

    # Appendix S: Inference Serving
    ("appendix-s-inference-serving/section-s.1.html",
     "PagedAttention did for LLM memory what virtual memory did for operating systems.",
     "Woosuk Kwon et al., paraphrased"),
    ("appendix-s-inference-serving/section-s.2.html",
     "Deployment without configuration is hope. Configuration without deployment is procrastination.",
     "Anonymous MLOps engineer"),
    ("appendix-s-inference-serving/section-s.3.html",
     "Structure your generation, and the correctness will follow.",
     "Lianmin Zheng et al., paraphrased"),
    ("appendix-s-inference-serving/section-s.4.html",
     "Quantization is the art of forgetting just enough to still be useful.",
     "Tim Dettmers, paraphrased"),
    ("appendix-s-inference-serving/section-s.5.html",
     "Scaling is easy. Scaling reliably is engineering.",
     "Werner Vogels, adapted"),

    # Appendix T: Distributed ML
    ("appendix-t-distributed-ml/section-t.1.html",
     "When your data no longer fits on one machine, congratulations: you have a distributed systems problem.",
     "Matei Zaharia, paraphrased"),
    ("appendix-t-distributed-ml/section-t.2.html",
     "A lakehouse is a warehouse that learned to swim.",
     "Adapted from Databricks marketing, with affection"),
    ("appendix-t-distributed-ml/section-t.3.html",
     "The notebook is mightier than the deployment script, until production day.",
     "Anonymous Databricks user"),
    ("appendix-t-distributed-ml/section-t.4.html",
     "Foundation models are the new databases: everyone needs one, and nobody wants to maintain one.",
     "Anonymous infrastructure engineer"),
    ("appendix-t-distributed-ml/section-t.5.html",
     "Ray lets you scale from a laptop to a cluster without rewriting your code. Usually.",
     "Robert Nishihara, paraphrased"),
    ("appendix-t-distributed-ml/section-t.6.html",
     "A feature store is a team's shared memory of what the data actually means.",
     "Mike Del Balso, Tecton co-founder, paraphrased"),
    ("appendix-t-distributed-ml/section-t.7.html",
     "Building an ML pipeline is easy. Keeping it running at 3 AM on a Sunday is the real challenge.",
     "Chip Huyen, paraphrased"),

    # Appendix U: Docker & Containers
    ("appendix-u-docker-containers/section-u.1.html",
     "It works on my machine. Then we will ship your machine.",
     "The origin story of Docker"),
    ("appendix-u-docker-containers/section-u.2.html",
     "A Dockerfile is a recipe. A good Dockerfile is a recipe that does not download the entire internet.",
     "Anonymous DevOps engineer"),
    ("appendix-u-docker-containers/section-u.3.html",
     "One container is a service. Many containers are an architecture. Too many containers are a headache.",
     "Anonymous platform engineer"),
    ("appendix-u-docker-containers/section-u.4.html",
     "Containerizing an LLM server is straightforward. Fitting the model weights inside the container is the adventure.",
     "Anonymous MLOps practitioner"),

    # Appendix V: Tooling Ecosystem
    ("appendix-v-tooling-ecosystem/section-v.1.html",
     "The best tool is the one your team will actually use.",
     "Pragmatic engineering wisdom"),
    ("appendix-v-tooling-ecosystem/section-v.2.html",
     "Orchestration frameworks are the glue between your ideas and the LLM. Choose your glue carefully.",
     "Anonymous AI architect"),
    ("appendix-v-tooling-ecosystem/section-v.3.html",
     "An agent framework that does not let you debug is not a framework. It is a mystery.",
     "Anonymous frustrated developer"),
]

OLD_P = "    <p>TODO: Add section epigraph</p>"
OLD_CITE = "    <cite>A Thoughtful AI Agent</cite>"

base = Path("E:/Projects/LLMCourse/appendices")
replaced = 0
errors = []

for suffix, quote, attribution in EPIGRAPHS:
    fpath = base / suffix
    if not fpath.exists():
        errors.append(f"NOT FOUND: {fpath}")
        continue
    text = fpath.read_text(encoding="utf-8")
    if OLD_P not in text:
        errors.append(f"OLD_P not found: {fpath}")
        continue
    new_p = f"    <p>{quote}</p>"
    new_cite = f"    <cite>{attribution}</cite>"
    text = text.replace(OLD_P, new_p, 1)
    text = text.replace(OLD_CITE, new_cite, 1)
    fpath.write_text(text, encoding="utf-8")
    replaced += 1
    print(f"OK: {suffix}")

print(f"\nReplaced: {replaced}/{len(EPIGRAPHS)}")
if errors:
    print("ERRORS:")
    for e in errors:
        print(f"  {e}")
