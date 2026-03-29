#!/usr/bin/env python3
"""
Comprehensive cross-reference hyperlink sweep across all section HTML files.
Adds <a class="cross-ref"> links for concepts mentioned in text that are taught
in other sections of the book.

Rules:
- Only link first occurrence of each concept per section file
- Don't link concepts in the section that defines them
- Don't add links inside existing <a> tags, <pre> blocks, <code> blocks,
  <figcaption>, <title>, or HTML attributes
- Use relative paths with class="cross-ref"
- Never remove existing hyperlinks
"""

import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

BASE = r"E:\Projects\LLMCourse"

# ============================================================
# Module directory mapping (chapter number -> relative path from BASE)
# ============================================================
MODULE_DIRS = {
    0:  "part-1-foundations/module-00-ml-pytorch-foundations",
    1:  "part-1-foundations/module-01-foundations-nlp-text-representation",
    2:  "part-1-foundations/module-02-tokenization-subword-models",
    3:  "part-1-foundations/module-03-sequence-models-attention",
    4:  "part-1-foundations/module-04-transformer-architecture",
    5:  "part-1-foundations/module-05-decoding-text-generation",
    6:  "part-2-understanding-llms/module-06-pretraining-scaling-laws",
    7:  "part-2-understanding-llms/module-07-modern-llm-landscape",
    8:  "part-2-understanding-llms/module-08-reasoning-test-time-compute",
    9:  "part-2-understanding-llms/module-09-inference-optimization",
    10: "part-3-working-with-llms/module-10-llm-apis",
    11: "part-3-working-with-llms/module-11-prompt-engineering",
    12: "part-3-working-with-llms/module-12-hybrid-ml-llm",
    13: "part-4-training-adapting/module-13-synthetic-data",
    14: "part-4-training-adapting/module-14-fine-tuning-fundamentals",
    15: "part-4-training-adapting/module-15-peft",
    16: "part-4-training-adapting/module-16-distillation-merging",
    17: "part-4-training-adapting/module-17-alignment-rlhf-dpo",
    18: "part-2-understanding-llms/module-18-interpretability",
    19: "part-5-retrieval-conversation/module-19-embeddings-vector-db",
    20: "part-5-retrieval-conversation/module-20-rag",
    21: "part-5-retrieval-conversation/module-21-conversational-ai",
    22: "part-6-agentic-ai/module-22-ai-agents",
    23: "part-6-agentic-ai/module-23-tool-use-protocols",
    24: "part-6-agentic-ai/module-24-multi-agent-systems",
    25: "part-6-agentic-ai/module-25-specialized-agents",
    26: "part-6-agentic-ai/module-26-agent-safety-production",
    27: "part-7-multimodal-applications/module-27-multimodal",
    28: "part-7-multimodal-applications/module-28-llm-applications",
    29: "part-8-evaluation-production/module-29-evaluation-observability",
    30: "part-8-evaluation-production/module-30-observability-monitoring",
    31: "part-8-evaluation-production/module-31-production-engineering",
    32: "part-9-safety-strategy/module-32-safety-ethics-regulation",
    33: "part-9-safety-strategy/module-33-strategy-product-roi",
    34: "part-10-frontiers/module-34-emerging-architectures",
    35: "part-10-frontiers/module-35-ai-society",
}

def section_path(chapter, section_num):
    """Return relative path from BASE for a section file."""
    mod = MODULE_DIRS.get(chapter)
    if mod is None:
        return None
    return f"{mod}/section-{chapter}.{section_num}.html"

def index_path(chapter):
    mod = MODULE_DIRS.get(chapter)
    if mod is None:
        return None
    return f"{mod}/index.html"

# ============================================================
# Concept -> target mapping
# Each entry: (regex_pattern, target_path_from_BASE, defining_modules)
# defining_modules = set of chapter numbers where the concept is DEFINED
# (we won't link from those sections)
# ============================================================

CONCEPT_RULES = []

def add_rule(pattern, target, defining_chapters, flags=re.IGNORECASE):
    """Helper to register a concept rule."""
    CONCEPT_RULES.append((re.compile(pattern, flags), target, set(defining_chapters)))

# --- Part 1: Foundations ---

# Chapter 0: ML/PyTorch
add_rule(r'\bPyTorch\b', section_path(0, 3), {0})
add_rule(r'\bgradient descent\b', section_path(0, 2), {0})
add_rule(r'\bbackpropagation\b', section_path(0, 2), {0})
add_rule(r'\bloss function(?:s)?\b', section_path(0, 2), {0})

# Chapter 1: NLP foundations
add_rule(r'\bbag[- ]of[- ]words\b', section_path(1, 1), {1})
add_rule(r'\bTF-IDF\b', section_path(1, 2), {1})
add_rule(r'\b[Ww]ord2[Vv]ec\b', section_path(1, 3), {1})
add_rule(r'\bGlo[Vv]e\b', section_path(1, 3), {1})
add_rule(r'\bword embeddings?\b', section_path(1, 3), {1})
add_rule(r'\bword vectors?\b', section_path(1, 3), {1})
add_rule(r'\btext representation\b', section_path(1, 1), {1})

# Chapter 2: Tokenization
add_rule(r'\btokeniz(?:ation|er|ers)\b', section_path(2, 1), {2})
add_rule(r'\b(?:byte[- ]pair encoding|BPE)\b', section_path(2, 1), {2})
add_rule(r'\bWordPiece\b', section_path(2, 2), {2})
add_rule(r'\bSentencePiece\b', section_path(2, 2), {2})
add_rule(r'\bsubword(?:\s+(?:tokenization|models?|units?))?\b', section_path(2, 1), {2})
add_rule(r'\bvocabulary size\b', section_path(2, 3), {2})

# Chapter 3: Sequence models and attention
add_rule(r'\battention mechanism(?:s)?\b', section_path(3, 3), {3})
add_rule(r'\bself[- ]attention\b', section_path(3, 3), {3, 4})
add_rule(r'\bseq2seq\b', section_path(3, 2), {3})
add_rule(r'\bsequence[- ]to[- ]sequence\b', section_path(3, 2), {3})
add_rule(r'\bRNN(?:s)?\b', section_path(3, 1), {3})
add_rule(r'\brecurrent neural network(?:s)?\b', section_path(3, 1), {3})
add_rule(r'\bLSTM(?:s)?\b', section_path(3, 1), {3})
add_rule(r'\bvanishing gradient(?:s)?\b', section_path(3, 1), {3})

# Chapter 4: Transformer architecture
add_rule(r'\b[Tt]ransformer architecture\b', section_path(4, 1), {4})
add_rule(r'\bmulti[- ]head(?:ed)? attention\b', section_path(4, 1), {4})
add_rule(r'\bpositional encoding(?:s)?\b', section_path(4, 2), {4})
add_rule(r'\brotary positional embedding(?:s)?\b', section_path(4, 2), {4})
add_rule(r'\bRoPE\b', section_path(4, 2), {4})
add_rule(r'\bfeed[- ]?forward (?:network|layer)(?:s)?\b', section_path(4, 1), {4})
add_rule(r'\blayer normalization\b', section_path(4, 1), {4})
add_rule(r'\bFlash ?Attention\b', section_path(4, 3), {4, 9})
add_rule(r'\bgrouped[- ]query attention\b', section_path(4, 3), {4, 7, 9})
add_rule(r'\bGQA\b', section_path(4, 3), {4, 7, 9})
add_rule(r'\bmulti[- ]query attention\b', section_path(4, 3), {4})
add_rule(r'\bMQA\b', section_path(4, 3), {4})
add_rule(r'\bencoder[- ]decoder\b', section_path(4, 4), {4})
add_rule(r'\bdecoder[- ]only\b', section_path(4, 4), {4})
add_rule(r'\bKV cache\b', section_path(4, 5), {4, 9})

# Chapter 5: Decoding / text generation
add_rule(r'\bbeam search\b', section_path(5, 1), {5})
add_rule(r'\bgreedy decoding\b', section_path(5, 1), {5})
add_rule(r'\bnucleus sampling\b', section_path(5, 2), {5})
add_rule(r'\btop[- ]p sampling\b', section_path(5, 2), {5})
add_rule(r'\btop[- ]k sampling\b', section_path(5, 2), {5})
add_rule(r'\btemperature\s+(?:parameter|scaling|setting)\b', section_path(5, 2), {5})
add_rule(r'\brepetition penalty\b', section_path(5, 3), {5})
add_rule(r'\bspeculative decoding\b', section_path(5, 4), {5, 9})

# --- Part 2: Understanding LLMs ---

# Chapter 6: Pretraining and scaling
add_rule(r'\bscaling law(?:s)?\b', section_path(6, 3), {6})
add_rule(r'\bChinchilla\b', section_path(6, 3), {6})
add_rule(r'\bpre[- ]?training\b', section_path(6, 1), {6})
add_rule(r'\bmasked language model(?:ing)?\b', section_path(6, 1), {6})
add_rule(r'\bnext[- ]token prediction\b', section_path(6, 2), {6})
add_rule(r'\bdata curation\b', section_path(6, 4), {6})
add_rule(r'\bemergent (?:abilities|capabilities|behavior)\b', section_path(6, 6), {6})

# Chapter 7: Modern LLM landscape
add_rule(r'\b[Mm]ixture[- ]of[- ][Ee]xperts?\b', section_path(7, 2), {7})
add_rule(r'\bMoE\b', section_path(7, 2), {7})
add_rule(r'\bopen[- ](?:source|weight) (?:models?|LLMs?)\b', section_path(7, 1), {7})

# Chapter 8: Reasoning and test-time compute
add_rule(r'\bchain[- ]of[- ]thought\b', section_path(8, 1), {8})
add_rule(r'\bCoT\b', section_path(8, 1), {8})
add_rule(r'\btest[- ]time compute\b', section_path(8, 2), {8})
add_rule(r'\breasoning model(?:s)?\b', section_path(8, 3), {8})

# Chapter 9: Inference optimization
add_rule(r'\bquantization\b', section_path(9, 1), {9})
add_rule(r'\b(?:GPTQ|AWQ|GGUF)\b', section_path(9, 1), {9})
add_rule(r'\bpruning\b', section_path(9, 2), {9})
add_rule(r'\bbatching\b', section_path(9, 3), {9})
add_rule(r'\bcontinuous batching\b', section_path(9, 3), {9})
add_rule(r'\bvLLM\b', section_path(9, 4), {9})
add_rule(r'\bPagedAttention\b', section_path(9, 4), {9})
add_rule(r'\bTensorRT[- ]LLM\b', section_path(9, 4), {9})

# --- Part 3: Working with LLMs ---

# Chapter 10: LLM APIs
add_rule(r'\bLLM API(?:s)?\b', section_path(10, 1), {10})
add_rule(r'\bOpenAI API\b', section_path(10, 1), {10})
add_rule(r'\bstreaming\b(?=.*(?:response|token|API|output))', section_path(10, 2), {10})
add_rule(r'\bfunction calling\b', section_path(10, 3), {10, 22, 23})
add_rule(r'\bstructured output(?:s)?\b', section_path(10, 3), {10})

# Chapter 11: Prompt engineering
add_rule(r'\bprompt engineering\b', section_path(11, 1), {11})
add_rule(r'\bfew[- ]shot\b(?!\s+learning)', section_path(11, 2), {11})
add_rule(r'\bzero[- ]shot\b', section_path(11, 2), {11})
add_rule(r'\bsystem prompt(?:s)?\b', section_path(11, 1), {11})
add_rule(r'\bprompt injection\b', section_path(11, 4), {11, 32})
add_rule(r'\bprompt template(?:s)?\b', section_path(11, 3), {11})
add_rule(r'\b[Tt]ree[- ]of[- ][Tt]hought(?:s)?\b', section_path(11, 3), {11})

# Chapter 12: Hybrid ML+LLM
add_rule(r'\bhybrid (?:ML|pipeline|architecture|system)(?:s)?\b', section_path(12, 1), {12})
add_rule(r'\bclassifier\b', section_path(12, 2), {12})

# --- Part 4: Training & Adapting ---

# Chapter 13: Synthetic data
add_rule(r'\bsynthetic data\b', section_path(13, 1), {13})
add_rule(r'\bEvol[- ]Instruct\b', section_path(13, 3), {13})
add_rule(r'\bself[- ]instruct\b', section_path(13, 2), {13})
add_rule(r'\bmodel collapse\b', section_path(13, 5), {13})

# Chapter 14: Fine-tuning fundamentals
add_rule(r'\bfine[- ]tun(?:e|ed|ing)\b', section_path(14, 1), {14})
add_rule(r'\bfull fine[- ]tuning\b', section_path(14, 2), {14})
add_rule(r'\bcatastrophic forgetting\b', section_path(14, 3), {14})
add_rule(r'\blearning rate\b(?!.*schedule)', section_path(14, 3), {14, 0})
add_rule(r'\binstruction tuning\b', section_path(14, 4), {14})
add_rule(r'\bSFT\b', section_path(14, 4), {14})
add_rule(r'\bsupervised fine[- ]tuning\b', section_path(14, 4), {14})

# Chapter 15: PEFT
add_rule(r'\bLoRA\b', section_path(15, 1), {15})
add_rule(r'\bQLoRA\b', section_path(15, 2), {15})
add_rule(r'\bPEFT\b', section_path(15, 1), {15})
add_rule(r'\bparameter[- ]efficient\b', section_path(15, 1), {15})
add_rule(r'\badapter(?:s)?\b(?=.*(?:tun|train|layer|modul|weight|fine|insert|freez))', section_path(15, 1), {15})
add_rule(r'\blow[- ]rank adaptation\b', section_path(15, 1), {15})
add_rule(r'\bprefix tuning\b', section_path(15, 3), {15})
add_rule(r'\bprompt tuning\b', section_path(15, 3), {15})

# Chapter 16: Distillation and merging
add_rule(r'\b(?:knowledge )?distillation\b', section_path(16, 1), {16})
add_rule(r'\bmodel merging\b', section_path(16, 2), {16})
add_rule(r'\bmodel compression\b', section_path(16, 1), {16, 9})
add_rule(r'\bteacher[- ]student\b', section_path(16, 1), {16})

# Chapter 17: Alignment, RLHF, DPO
add_rule(r'\bRLHF\b', section_path(17, 1), {17})
add_rule(r'\breinforcement learning from human feedback\b', section_path(17, 1), {17})
add_rule(r'\bDPO\b', section_path(17, 2), {17})
add_rule(r'\b[Dd]irect [Pp]reference [Oo]ptimization\b', section_path(17, 2), {17})
add_rule(r'\breward model(?:s|ing)?\b', section_path(17, 1), {17})
add_rule(r'\balignment\b(?=.*(?:model|LLM|AI|human|value|safety|technique))', section_path(17, 1), {17})
add_rule(r'\bconstitutional AI\b', section_path(17, 3), {17})
add_rule(r'\bRLVR\b', section_path(17, 4), {17})
add_rule(r'\bPPO\b', section_path(17, 1), {17})

# Chapter 18: Interpretability
add_rule(r'\binterpretability\b', section_path(18, 1), {18})
add_rule(r'\bmechanistic interpretability\b', section_path(18, 2), {18})
add_rule(r'\blogit lens\b', section_path(18, 2), {18})
add_rule(r'\bsparse autoencoder(?:s)?\b', section_path(18, 3), {18})
add_rule(r'\bSAE(?:s)?\b', section_path(18, 3), {18})
add_rule(r'\bsuperposition\b', section_path(18, 3), {18})
add_rule(r'\bprobing\b', section_path(18, 1), {18})
add_rule(r'\battention (?:pattern|visualization|head)(?:s)?\b', section_path(18, 1), {18})

# --- Part 5: Retrieval & Conversation ---

# Chapter 19: Embeddings and vector DB
add_rule(r'\bembedding(?:s)? (?:model|space|vector|dimension)\b', section_path(19, 1), {19, 1})
add_rule(r'\bvector (?:database|DB|store|index)(?:s|es)?\b', section_path(19, 2), {19})
add_rule(r'\bFAISS\b', section_path(19, 2), {19})
add_rule(r'\bPinecone\b', section_path(19, 2), {19})
add_rule(r'\bChroma(?:DB)?\b', section_path(19, 2), {19})
add_rule(r'\bWeaviate\b', section_path(19, 2), {19})
add_rule(r'\bHNSW\b', section_path(19, 3), {19})
add_rule(r'\bcosine similarity\b', section_path(19, 1), {19})
add_rule(r'\bsemantic search\b', section_path(19, 1), {19})
add_rule(r'\bchunking\b(?=.*(?:strateg|document|text|split|overlap|token))', section_path(19, 4), {19})

# Chapter 20: RAG
add_rule(r'\bretrieval[- ]augmented generation\b', section_path(20, 1), {20})
add_rule(r'\bRAG\b', section_path(20, 1), {20})
add_rule(r'\bhybrid (?:search|retrieval)\b', section_path(20, 2), {20})
add_rule(r'\breranking\b', section_path(20, 2), {20})
add_rule(r'\bre[- ]?rank(?:er|ing)\b', section_path(20, 2), {20})
add_rule(r'\bknowledge graph(?:s)?\b', section_path(20, 4), {20})
add_rule(r'\bGraphRAG\b', section_path(20, 4), {20})

# Chapter 21: Conversational AI
add_rule(r'\bconversational AI\b', section_path(21, 1), {21})
add_rule(r'\bdialogue (?:system|management|state)(?:s)?\b', section_path(21, 1), {21})
add_rule(r'\bmemory management\b', section_path(21, 3), {21})
add_rule(r'\bchat(?:bot)? memory\b', section_path(21, 3), {21})

# --- Part 6: Agentic AI ---

# Chapter 22: AI Agents
add_rule(r'\bAI agent(?:s)?\b', section_path(22, 1), {22})
add_rule(r'\bReAct\b', section_path(22, 2), {22})
add_rule(r'\btool use\b', section_path(22, 3), {22, 23})
add_rule(r'\btool calling\b', section_path(22, 3), {22, 23})
add_rule(r'\bagent(?:ic)? (?:loop|framework|architecture|system)(?:s)?\b', section_path(22, 1), {22})
add_rule(r'\bplan(?:ning)? (?:and |& )?(?:act|execution|execute)\b', section_path(22, 2), {22})

# Chapter 23: Tool use and protocols
add_rule(r'\bMCP\b(?=.*(?:protocol|tool|server|client|Model Context))', section_path(23, 2), {23})
add_rule(r'\bModel Context Protocol\b', section_path(23, 2), {23})
add_rule(r'\bA2A\b', section_path(23, 3), {23})
add_rule(r'\bAgent2Agent\b', section_path(23, 3), {23})

# Chapter 24: Multi-agent systems
add_rule(r'\bmulti[- ]agent\b', section_path(24, 1), {24})
add_rule(r'\bsupervisor pattern\b', section_path(24, 2), {24})
add_rule(r'\borchestrat(?:or|ion)\b(?=.*agent)', section_path(24, 2), {24})
add_rule(r'\bdebate pattern\b', section_path(24, 3), {24})

# Chapter 25: Specialized agents
add_rule(r'\bcoding agent(?:s)?\b', section_path(25, 1), {25})
add_rule(r'\bresearch agent(?:s)?\b', section_path(25, 2), {25})
add_rule(r'\bdata (?:analysis )?agent(?:s)?\b', section_path(25, 3), {25})

# Chapter 26: Agent safety and production
add_rule(r'\bagent safety\b', section_path(26, 1), {26})
add_rule(r'\bsandbox(?:ed|ing)?\b(?=.*(?:agent|execution|tool|code))', section_path(26, 2), {26})
add_rule(r'\bhuman[- ]in[- ]the[- ]loop\b', section_path(26, 3), {26})

# --- Part 7: Multimodal & Applications ---

# Chapter 27: Multimodal
add_rule(r'\bmultimodal\b(?=.*(?:model|LLM|AI|system|input|understanding))', section_path(27, 1), {27})
add_rule(r'\bvision[- ]language model(?:s)?\b', section_path(27, 1), {27})
add_rule(r'\bVLM(?:s)?\b', section_path(27, 1), {27})
add_rule(r'\bimage generation\b', section_path(27, 3), {27})
add_rule(r'\bdiffusion model(?:s)?\b', section_path(27, 3), {27})
add_rule(r'\bspeech[- ]to[- ]text\b', section_path(27, 2), {27})
add_rule(r'\bWhisper\b', section_path(27, 2), {27})
add_rule(r'\btext[- ]to[- ]speech\b', section_path(27, 2), {27})
add_rule(r'\bCLIP\b', section_path(27, 1), {27})

# Chapter 28: LLM Applications
add_rule(r'\bcode generation\b', section_path(28, 1), {28})
add_rule(r'\bpair programming\b', section_path(28, 1), {28})

# --- Part 8: Evaluation & Production ---

# Chapter 29: Evaluation
add_rule(r'\bLLM evaluation\b', section_path(29, 1), {29})
add_rule(r'\bLLM[- ]as[- ](?:a[- ])?judge\b', section_path(29, 3), {29})
add_rule(r'\bbenchmark(?:s|ing)?\b(?=.*(?:LLM|model|evaluat|leaderboard))', section_path(29, 2), {29})
add_rule(r'\bhuman evaluation\b', section_path(29, 4), {29})
add_rule(r'\bBLEU\b', section_path(29, 1), {29})
add_rule(r'\bROUGE\b', section_path(29, 1), {29})

# Chapter 30: Observability
add_rule(r'\bobservability\b', section_path(30, 1), {30})
add_rule(r'\btracing\b(?=.*(?:LLM|agent|request|span|observ))', section_path(30, 2), {30})
add_rule(r'\bdrift\b(?=.*(?:monitor|detect|model|concept|data))', section_path(30, 3), {30})

# Chapter 31: Production engineering
add_rule(r'\bLLMOps\b', section_path(31, 1), {31})
add_rule(r'\bmodel serving\b', section_path(31, 2), {31})
add_rule(r'\bA/B testing\b', section_path(31, 3), {31})
add_rule(r'\brate limit(?:ing)?\b', section_path(31, 2), {31, 10})
add_rule(r'\bguardrail(?:s)?\b', section_path(31, 4), {31, 32})

# --- Part 9: Safety & Strategy ---

# Chapter 32: Safety, Ethics
add_rule(r'\bred teaming\b', section_path(32, 3), {32})
add_rule(r'\bhallucination(?:s)?\b', section_path(32, 2), {32})
add_rule(r'\bbias\b(?=.*(?:model|AI|LLM|fairness|gender|racial|mitigat))', section_path(32, 4), {32})
add_rule(r'\bAI safety\b', section_path(32, 1), {32})
add_rule(r'\bEU AI Act\b', section_path(32, 6), {32})
add_rule(r'\bAI regulation(?:s)?\b', section_path(32, 6), {32})
add_rule(r'\bjailbreak(?:ing|s)?\b', section_path(32, 3), {32})

# Chapter 33: Strategy and ROI
add_rule(r'\bROI\b(?=.*(?:LLM|AI|model|invest|cost|return))', section_path(33, 2), {33})
add_rule(r'\bbuild vs\.? buy\b', section_path(33, 3), {33})
add_rule(r'\btotal cost of ownership\b', section_path(33, 2), {33})

# --- Part 10: Frontiers ---
add_rule(r'\bstate[- ]space model(?:s)?\b', section_path(34, 1), {34})
add_rule(r'\bMamba\b', section_path(34, 1), {34})
add_rule(r'\bAGI\b', section_path(35, 2), {35})

# --- Frameworks/Libraries (link to book sections, not external) ---
add_rule(r'\bHugging Face\b', section_path(14, 5), {14})
add_rule(r'\bLangChain\b', section_path(20, 3), {20})
add_rule(r'\bLlamaIndex\b', section_path(20, 3), {20})


# ============================================================
# Section/Chapter reference patterns
# e.g., "Section 4.1", "Chapter 14", "Part 3"
# ============================================================

SECTION_REF_RE = re.compile(r'\bSection\s+(\d+)\.(\d+)\b')
CHAPTER_REF_RE = re.compile(r'\bChapter\s+(\d+)\b')
PART_REF_RE    = re.compile(r'\bPart\s+(\d+)\b')

PART_DIRS = {
    1: "part-1-foundations",
    2: "part-2-understanding-llms",
    3: "part-3-working-with-llms",
    4: "part-4-training-adapting",
    5: "part-5-retrieval-conversation",
    6: "part-6-agentic-ai",
    7: "part-7-multimodal-applications",
    8: "part-8-evaluation-production",
    9: "part-9-safety-strategy",
    10: "part-10-frontiers",
}


# ============================================================
# HTML-aware replacement engine
# ============================================================

def get_chapter_from_filepath(filepath):
    """Extract the chapter number from a file path."""
    m = re.search(r'section-(\d+)\.', os.path.basename(filepath))
    if m:
        return int(m.group(1))
    m = re.search(r'module-(\d+)', filepath)
    if m:
        return int(m.group(1))
    return None

def compute_relative_path(from_file, to_path_from_base):
    """Compute relative path from from_file to to_path_from_base."""
    from_dir = os.path.dirname(os.path.relpath(from_file, BASE))
    rel = os.path.relpath(os.path.join(BASE, to_path_from_base),
                          os.path.join(BASE, from_dir))
    return rel.replace('\\', '/')


# Tags where we should NOT insert links
SKIP_TAGS = {'a', 'pre', 'code', 'script', 'style', 'title', 'figcaption', 'svg', 'math'}

def split_html_segments(html_content):
    """
    Split HTML into segments: (text, is_protected)
    Protected = inside tags, attributes, <a>...</a>, <pre>...</pre>, <code>...</code>, etc.
    """
    # Pattern to match: HTML tags, or content inside protected elements
    # We need to track nested protected regions

    segments = []
    # Regex to find HTML tags and protected blocks
    # Protected blocks: <a ...>...</a>, <pre>...</pre>, <code>...</code>, <script>...</script>,
    #                   <style>...</style>, <title>...</title>, <figcaption>...</figcaption>, <svg>...</svg>

    protected_pattern = re.compile(
        r'(<(?:a|pre|code|script|style|title|figcaption|svg|math)\b[^>]*>.*?</(?:a|pre|code|script|style|title|figcaption|svg|math)>)|'
        r'(<[^>]+>)',
        re.DOTALL | re.IGNORECASE
    )

    last_end = 0
    for m in protected_pattern.finditer(html_content):
        # Text before this match is unprotected
        if m.start() > last_end:
            segments.append((html_content[last_end:m.start()], False))
        # The match itself is protected
        segments.append((m.group(0), True))
        last_end = m.end()

    # Remaining text after last match
    if last_end < len(html_content):
        segments.append((html_content[last_end:], False))

    return segments


def process_file(filepath):
    """Process a single HTML file, adding cross-reference links."""
    chapter = get_chapter_from_filepath(filepath)
    if chapter is None:
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Split into protected and unprotected segments
    segments = split_html_segments(content)

    # Track which concepts have been linked (first occurrence only)
    linked_concepts = set()
    linked_sections = set()
    linked_chapters = set()
    linked_parts = set()

    new_segments = []
    link_count = 0

    for text, is_protected in segments:
        if is_protected:
            new_segments.append(text)
            continue

        # Process unprotected text
        replacements = []  # (start, end, replacement_html)

        # 1. Concept rules
        for regex, target_path, defining_chapters in CONCEPT_RULES:
            if target_path is None:
                continue
            rule_key = target_path  # use target path as dedup key
            if rule_key in linked_concepts:
                continue
            if chapter in defining_chapters:
                continue

            m = regex.search(text)
            if m:
                # Check this doesn't overlap with existing replacements
                overlaps = False
                for (rs, re_, _) in replacements:
                    if m.start() < re_ and m.end() > rs:
                        overlaps = True
                        break
                if overlaps:
                    continue

                rel_path = compute_relative_path(filepath, target_path)
                replacement = f'<a class="cross-ref" href="{rel_path}">{m.group(0)}</a>'
                replacements.append((m.start(), m.end(), replacement))
                linked_concepts.add(rule_key)

        # 2. Section references (e.g., "Section 4.1")
        for m in SECTION_REF_RE.finditer(text):
            ch = int(m.group(1))
            sec = int(m.group(2))
            ref_key = (ch, sec)
            if ref_key in linked_sections:
                continue
            if ch == chapter:
                continue

            target = section_path(ch, sec)
            if target is None:
                continue
            target_full = os.path.join(BASE, target)
            if not os.path.exists(target_full):
                continue

            # Check overlap
            overlaps = False
            for (rs, re_, _) in replacements:
                if m.start() < re_ and m.end() > rs:
                    overlaps = True
                    break
            if overlaps:
                continue

            rel_path = compute_relative_path(filepath, target)
            replacement = f'<a class="cross-ref" href="{rel_path}">{m.group(0)}</a>'
            replacements.append((m.start(), m.end(), replacement))
            linked_sections.add(ref_key)

        # 3. Chapter references (e.g., "Chapter 14")
        for m in CHAPTER_REF_RE.finditer(text):
            ch = int(m.group(1))
            if ch in linked_chapters:
                continue
            if ch == chapter:
                continue

            target = index_path(ch)
            if target is None:
                continue
            target_full = os.path.join(BASE, target)
            if not os.path.exists(target_full):
                continue

            overlaps = False
            for (rs, re_, _) in replacements:
                if m.start() < re_ and m.end() > rs:
                    overlaps = True
                    break
            if overlaps:
                continue

            rel_path = compute_relative_path(filepath, target)
            replacement = f'<a class="cross-ref" href="{rel_path}">{m.group(0)}</a>'
            replacements.append((m.start(), m.end(), replacement))
            linked_chapters.add(ch)

        # 4. Part references (e.g., "Part 3")
        for m in PART_REF_RE.finditer(text):
            part_num = int(m.group(1))
            if part_num in linked_parts:
                continue

            part_dir = PART_DIRS.get(part_num)
            if part_dir is None:
                continue
            target = f"{part_dir}/index.html"
            target_full = os.path.join(BASE, target)
            if not os.path.exists(target_full):
                continue

            overlaps = False
            for (rs, re_, _) in replacements:
                if m.start() < re_ and m.end() > rs:
                    overlaps = True
                    break
            if overlaps:
                continue

            rel_path = compute_relative_path(filepath, target)
            replacement = f'<a class="cross-ref" href="{rel_path}">{m.group(0)}</a>'
            replacements.append((m.start(), m.end(), replacement))
            linked_parts.add(part_num)

        # Apply replacements in reverse order to preserve positions
        replacements.sort(key=lambda x: x[0], reverse=True)
        for start, end, repl in replacements:
            text = text[:start] + repl + text[end:]
            link_count += 1

        new_segments.append(text)

    new_content = ''.join(new_segments)

    if new_content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return link_count


def main():
    # Collect all section HTML files from part-* directories
    all_files = []
    for part_dir in sorted(Path(BASE).glob("part-*")):
        for section_file in sorted(part_dir.rglob("section-*.html")):
            all_files.append(str(section_file))

    print(f"Found {len(all_files)} section files to process")

    total_links = 0
    files_modified = 0

    for filepath in all_files:
        links = process_file(filepath)
        if links > 0:
            rel = os.path.relpath(filepath, BASE)
            print(f"  +{links:3d} links: {rel}")
            total_links += links
            files_modified += 1

    print(f"\nDone: {total_links} links added across {files_modified} files")


if __name__ == '__main__':
    main()
