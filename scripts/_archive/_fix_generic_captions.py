"""
Fix generic/template code captions and opening comments across HTML files.
Replaces boilerplate text with specific descriptions based on actual code content.
"""

import re
import os

# ============================================================
# PHASE 1: Fix "Import X and supporting dependencies" +
#           "These libraries provide the core functionality for this example"
# These always appear as a two-line pair at the start of code blocks.
# We need to replace them with specific comments about what the code does.
# ============================================================

def fix_import_comments(content, filepath):
    """Replace generic import comments with specific ones based on code context."""

    # Pattern: matches the two-line generic comment block
    # Line 1: # Import X and supporting dependencies
    # Line 2: # These libraries provide the core functionality for this example
    pattern = r'(# Import \w+ and supporting dependencies)\n(# These libraries provide the core functionality for this example)'

    matches = list(re.finditer(pattern, content))
    if not matches:
        return content

    # Process matches in reverse order to preserve positions
    for match in reversed(matches):
        start = match.start()
        end = match.end()

        # Get surrounding context (code after the comment) to determine replacement
        after_context = content[end:end+800]
        before_context = content[max(0,start-400):start]

        replacement = get_specific_import_comment(before_context, after_context, filepath)
        content = content[:start] + replacement + content[end:]

    return content


def get_specific_import_comment(before, after, filepath):
    """Generate a specific comment based on the code that follows."""
    after_lower = after.lower()
    fname = os.path.basename(filepath)

    # --- section-9.1.html ---
    if 'section-9.1' in filepath:
        if 'stream=True' in after or 'stream=true' in after or 'for chunk in stream' in after:
            return "# Stream a chat completion using Server-Sent Events\n# Each chunk delivers incremental tokens as they are generated"
        if 'bedrock' in after_lower or 'boto3' in after:
            return "# Call Claude on AWS Bedrock using boto3 with IAM authentication\n# The request body follows the Anthropic Messages API format"
        if 'azure' in after_lower or 'AzureOpenAI' in after:
            return "# Call OpenAI models via Azure OpenAI with regional deployment\n# Uses the same SDK but with Azure-specific endpoint and API version"
        if 'genai' in after or 'google' in after_lower or 'gemini' in after_lower:
            return "# Call Google Gemini using the genai SDK\n# Configuration uses GenerateContentConfig for temperature and token limits"
        if 'anthropic' in after_lower and 'Anthropic()' in after:
            return "# Call Claude using the Anthropic Messages API\n# The response includes input/output token counts for cost tracking"
        if 'chat.completions.create' in after and 'system' in after:
            return "# Send a chat completion request with system and user messages\n# Temperature and max_tokens control randomness and response length"
        if 'chat.completions.create' in after:
            return "# Send a chat completion request to the OpenAI API\n# The messages list follows the multi-turn conversation format"
        # generic fallback for 9.1
        return "# Set up the OpenAI client and send a chat completion request\n# The response object contains generated text and usage metadata"

    # --- section-9.2.html ---
    if 'section-9.2' in filepath:
        if 'instructor' in after_lower:
            return "# Use Instructor to extract structured Pydantic objects from LLM responses\n# Instructor patches the OpenAI client to return validated models"
        if 'tool_calls' in after or 'tools=' in after or 'function_call' in after:
            return "# Define tools for function calling and handle tool_calls in the response\n# The model decides which function to invoke based on the user query"
        if 'anthropic' in after_lower and 'tool_use' in after:
            return "# Use Anthropic tool_use for structured extraction with Claude\n# The response contains tool_use content blocks with extracted data"
        if 'google' in after_lower or 'genai' in after:
            return "# Use Google Gemini function calling for structured output\n# Gemini uses FunctionDeclaration for tool definitions"
        if 'asyncio' in after or 'async ' in after:
            return "# Run multiple LLM calls concurrently using asyncio\n# Async batching reduces wall-clock time for parallel requests"
        if 'json_schema' in after or 'response_format' in after:
            return "# Use OpenAI structured outputs with a JSON schema constraint\n# The model is forced to return valid JSON matching the schema"
        return "# Set up structured output extraction from the LLM\n# Parse the response into a typed data structure"

    # --- section-9.3.html ---
    if 'section-9.3' in filepath:
        if 'litellm' in after_lower:
            return "# Use LiteLLM as a unified interface across multiple LLM providers\n# A single completion() call works with OpenAI, Anthropic, and others"
        if 'retry' in after_lower or 'backoff' in after_lower or 'tenacity' in after_lower:
            return "# Implement exponential backoff retry logic for transient API failures\n# Retries handle rate limits (429) and server errors (5xx) gracefully"
        if 'hashlib' in after or 'cache' in after_lower:
            return "# Build a semantic cache that hashes prompts to avoid redundant API calls\n# Cache hits skip the network round-trip entirely, saving cost and latency"
        if 'embedding' in after_lower or 'cosine' in after_lower or 'numpy' in after_lower:
            return "# Compute cosine similarity between prompt embeddings for semantic caching\n# Similar prompts reuse cached responses within a configurable threshold"
        if 'portkey' in after_lower or 'PORTKEY' in after:
            return "# Route requests through the Portkey AI gateway for fallback and caching\n# Portkey handles provider failover and semantic response caching"
        if 'helicone' in after_lower or 'Helicone' in after:
            return "# Route requests through Helicone for observability and cost tracking\n# Custom headers tag requests for filtering in the analytics dashboard"
        if 'TokenBudget' in after or 'budget' in after_lower:
            return "# Enforce per-user token budgets to prevent runaway API costs\n# Track usage across configurable time windows (hourly, daily, monthly)"
        if 'CircuitBreaker' in after or 'circuit' in after_lower:
            return "# Implement a circuit breaker pattern for resilient LLM calls\n# Combines budget checks, caching, model fallback, and static responses"
        if 'ResilientResponse' in after or 'FallbackLevel' in after:
            return "# Build a multi-layer resilience pipeline for production LLM calls\n# Fallback chain: primary model, cache, simpler model, static response"
        return "# Configure the API client with production error handling\n# Wrap calls with retry logic and timeout management"

    # --- section-9.4.html ---
    if 'section-9.4' in filepath:
        if 'vision' in after_lower or 'image_url' in after or 'base64' in after_lower:
            if 'anthropic' in after_lower:
                return "# Send an image to Claude for visual analysis using base64 encoding\n# The content array mixes image and text blocks in a single message"
            if 'google' in after_lower or 'genai' in after:
                return "# Analyze an image with Google Gemini using inline_data\n# Gemini accepts raw image bytes with a MIME type"
            return "# Send an image to the OpenAI Vision API for analysis\n# The content array includes both an image_url and a text prompt"
        if 'audio' in after_lower or 'whisper' in after_lower or 'speech' in after_lower:
            return "# Transcribe or generate audio using the OpenAI audio endpoints\n# Whisper handles speech-to-text; TTS handles text-to-speech"
        if 'tool_calls' in after or 'tools=' in after:
            return "# Use the Anthropic tool_use API for multi-turn tool calling\n# The model selects tools and the client executes them in a loop"
        if 'dataclass' in after_lower or 'ModalityRouter' in after:
            return "# Build a modality router that dispatches inputs to the correct API\n# Supports text, image, audio, and document inputs with provider selection"
        return "# Set up a multimodal API call with image or audio input\n# The request packages different content types for the model"

    # --- section-10.2.html ---
    if 'section-10.2' in filepath:
        return "# Implement a ReAct agent loop with tool calling\n# The agent iterates through Think, Act, Observe steps until it has a final answer"

    # --- section-10.3.html ---
    if 'section-10.3' in filepath:
        return "# Configure DSPy with a language model and define a fact-checking signature\n# ChainOfThought adds step-by-step reasoning before producing the verdict"

    # --- section-10.4.html ---
    if 'section-10.4' in filepath:
        return "# Define a Promptfoo test suite in YAML for regression testing prompts\n# Test cases cover classification accuracy and prompt injection resistance"

    # --- section-11.1.html ---
    if 'section-11.1' in filepath:
        if 'sklearn' in after_lower or 'TfidfVectorizer' in after:
            return "# Train a TF-IDF + Logistic Regression baseline classifier\n# This lightweight pipeline runs in milliseconds and costs nothing per prediction"
        if 'regex' in after_lower or 're.' in after:
            return "# Build a regex-based extractor for structured patterns like dates and emails\n# Pattern matching handles deterministic extraction with zero inference cost"
        return "# Set up a traditional ML or rule-based component for the hybrid pipeline\n# Classical methods handle high-volume, well-defined tasks efficiently"

    # --- section-11.2.html ---
    if 'section-11.2' in filepath:
        if 'sentence_transformers' in after or 'SentenceTransformer' in after:
            return "# Generate sentence embeddings for semantic similarity comparison\n# The bi-encoder produces fixed-size vectors for fast nearest-neighbor search"
        return "# Build a feature extraction pipeline using pre-trained embeddings\n# These vectors serve as input features for downstream classifiers"

    # --- section-11.3.html ---
    if 'section-11.3' in filepath:
        if 'numpy' in after_lower and ('complexity' in after_lower or 'score' in after_lower):
            return "# Compute a complexity score to route queries to the right model tier\n# Simple heuristics (length, vocabulary, entity count) avoid LLM router overhead"
        if 'CascadeRouter' in after or 'cascade' in after_lower:
            return "# Implement a cascade router that tries cheap models first\n# Each tier has a confidence threshold; low-confidence results escalate to the next tier"
        if 'route_request' in after or 'router' in after_lower:
            return "# Use a small LLM to classify request difficulty and select a model tier\n# The router returns a JSON decision with tier, reasoning, and difficulty score"
        if 'dataclass' in after_lower and 'RoutingDecision' in after:
            return "# Define data classes for routing decisions and model tier configuration\n# Each tier specifies its cost, latency, and capability thresholds"
        if 'dataclass' in after_lower:
            return "# Define the routing tier configuration with cost and latency parameters\n# The cascade evaluates tiers in order of increasing cost"
        return "# Build a model routing component for the hybrid ML/LLM pipeline\n# Route requests to the most cost-effective model that meets quality requirements"

    # --- section-11.4.html ---
    if 'section-11.4' in filepath:
        if 'ModelConfig' in after or 'pareto' in after_lower:
            return "# Find the Pareto frontier of model configurations by cost and accuracy\n# Pareto-optimal configs cannot be improved on one axis without regressing the other"
        if 'tiktoken' in after_lower or 'token' in after_lower:
            return "# Estimate token usage and API cost for different model configurations\n# Token counting enables accurate cost projections before running at scale"
        if 'dataclass' in after_lower and 'benchmark' in after_lower:
            return "# Define benchmark result data structures for systematic model comparison\n# Track accuracy, cost per query, and latency across all configurations"
        if 'dataclass' in after_lower:
            return "# Structure the cost-performance analysis with typed data classes\n# Each configuration captures model name, accuracy, cost, and latency"
        if 'json' in after_lower:
            return "# Load benchmark results from JSON for cost-performance analysis\n# Compare models across accuracy, cost per query, and p50/p95 latency"
        return "# Analyze cost-performance tradeoffs across model configurations\n# Identify the Pareto-optimal set that balances accuracy against cost"

    # --- section-11.5.html ---
    if 'section-11.5' in filepath:
        if 'spacy' in after_lower and 'ner' in after_lower:
            return "# Run spaCy NER as the first extraction layer (classical, near-zero cost)\n# Standard entity types (PERSON, ORG, DATE) are handled without an LLM call"
        if 'spacy' in after_lower and ('instructor' in after_lower or 'hybrid' in after_lower or 'extract_with_llm' in after):
            return "# Combine spaCy NER with LLM extraction in a two-layer pipeline\n# The LLM handles domain-specific entities that spaCy cannot recognize"
        if 'spacy' in after_lower:
            return "# Use spaCy for classical named entity recognition\n# Extracts persons, organizations, dates, and locations at minimal cost"
        return "# Build a hybrid extraction pipeline combining classical NER with LLM\n# Route complex documents to the LLM layer only when needed"

    # --- section-12.1.html ---
    if 'section-12.1' in filepath:
        if 'pandas' in after_lower:
            return "# Load and inspect training data distributions using pandas\n# Understanding class balance and text length helps guide generation strategy"
        if 'dataclass' in after_lower:
            return "# Define data structures for synthetic data generation configuration\n# Specify target distributions, quality thresholds, and domain constraints"
        if 'hashlib' in after_lower or 'dedup' in after_lower:
            return "# Deduplicate synthetic examples using content hashing\n# Remove near-duplicates to ensure diversity in the generated dataset"
        return "# Set up the synthetic data generation pipeline\n# Configure generation parameters, quality filters, and output format"

    # --- section-12.2.html ---
    if 'section-12.2' in filepath:
        if 'json' in after_lower and ('seed' in after_lower or 'instruct' in after_lower):
            return "# Generate diverse instructions using the Self-Instruct pipeline\n# Seed tasks bootstrap generation; the LLM expands the instruction set"
        if 'itertools' in after_lower or 'evol' in after_lower:
            return "# Implement Evol-Instruct to evolve simple instructions into complex ones\n# Successive transformations add constraints, reasoning steps, and edge cases"
        return "# Build an instruction generation pipeline for synthetic data\n# Use seed examples and evolutionary strategies to create diverse training pairs"

    # --- section-12.3.html ---
    if 'section-12.3' in filepath:
        if 'openai' in after_lower and ('persona' in after_lower or 'style' in after_lower or 'diverse' in after_lower):
            return "# Generate synthetic responses with controlled persona and style variation\n# Different system prompts produce diverse writing styles for the same instruction"
        if 'dataclass' in after_lower:
            return "# Define quality scoring criteria for generated synthetic examples\n# Multi-dimensional scores track helpfulness, accuracy, and coherence"
        return "# Generate synthetic training data using LLM-based response synthesis\n# Control temperature, persona, and format to maximize diversity"

    # --- section-12.4.html ---
    if 'section-12.4' in filepath:
        if 'json' in after_lower and ('filter' in after_lower or 'quality' in after_lower):
            return "# Load synthetic data and apply multi-stage quality filtering\n# Combine rule-based checks with LLM-based quality scoring"
        if 'hashlib' in after_lower or 'dedup' in after_lower or 'contamination' in after_lower:
            return "# Check for train/test contamination using n-gram overlap detection\n# Prevent data leakage that would inflate benchmark scores"
        if 'FilterPipeline' in after or 'dataclass' in after_lower:
            return "# Build a composable filter pipeline for synthetic data quality control\n# Chain length, quality score, and repetition filters in sequence"
        if 'argilla' in after_lower:
            return "# Push synthetic data to Argilla for human review and annotation\n# Borderline examples are flagged for manual inspection"
        if 'distilabel' in after_lower:
            return "# Build a Distilabel pipeline for automated generation and scoring\n# TextGeneration creates candidates; UltraFeedback scores them"
        return "# Apply quality filters to the synthetic dataset\n# Remove low-quality, repetitive, or contaminated examples"

    # --- section-12.5.html ---
    if 'section-12.5' in filepath:
        if 'json' in after_lower and ('label' in after_lower or 'annot' in after_lower):
            return "# Structure annotation tasks as JSON with labeling guidelines\n# Consistent formatting enables both human and LLM annotators"
        if 'numpy' in after_lower and ('cohen' in after_lower or 'kappa' in after_lower or 'agreement' in after_lower):
            return "# Compute inter-annotator agreement using Cohen's kappa\n# Kappa measures agreement beyond chance between two raters"
        if 'numpy' in after_lower:
            return "# Calculate annotation quality metrics using numpy\n# Track agreement rates, label distributions, and annotator reliability"
        if 'label_studio' in after_lower:
            return "# Set up a Label Studio ML backend for LLM-powered pre-labeling\n# The backend generates draft labels that human annotators review"
        return "# Configure the annotation pipeline for synthetic data validation\n# Combine LLM pre-labeling with human review for quality assurance"

    # --- section-12.6.html ---
    if 'section-12.6' in filepath:
        if 're.' in after or 'regex' in after_lower:
            return "# Detect and filter personally identifiable information using regex\n# Pattern matching catches emails, phone numbers, and SSN-like strings"
        if 'numpy' in after_lower:
            return "# Measure dataset diversity using embedding-based metrics\n# Higher diversity in the training set improves model generalization"
        if 'dataclass' in after_lower:
            return "# Define a data governance record for tracking synthetic data provenance\n# Each record logs the generation model, filters applied, and license terms"
        return "# Apply privacy and governance checks to the synthetic dataset\n# Remove PII, check for bias, and document provenance"

    # --- section-12.7.html ---
    if 'section-12.7' in filepath:
        if 'openai' in after_lower and ('reason' in after_lower or 'step' in after_lower or 'chain' in after_lower or 'rejection' in after_lower):
            return "# Generate reasoning traces with rejection sampling\n# Only traces that produce the correct final answer are kept for training"
        if 'json' in after_lower:
            return "# Structure reasoning traces as JSON with step-level annotations\n# Each trace includes the problem, reasoning chain, and verified answer"
        return "# Build a reasoning data synthesis pipeline\n# Generate step-by-step solutions and filter by correctness"

    # --- section-13.1.html ---
    if 'section-13.1' in filepath:
        return "# Configure forgetting mitigation with data mixing ratios\n# Blend 70% task-specific data with 30% general data to preserve capabilities"

    # --- section-13.2.html ---
    if 'section-13.2' in filepath:
        if 'transformers' in after_lower and ('tokenizer' in after_lower or 'AutoTokenizer' in after):
            return "# Load a pre-trained tokenizer and configure padding/truncation\n# Consistent tokenization is critical for reproducible fine-tuning"
        if 'datasets' in after_lower or 'load_dataset' in after:
            return "# Load and preprocess a dataset from Hugging Face Hub\n# Map the tokenization function across all splits for training"
        if 'typing' in after_lower or 'dataclass' in after_lower:
            return "# Define typed configuration for the fine-tuning data pipeline\n# Centralize hyperparameters for dataset preparation and formatting"
        return "# Set up the training data pipeline for fine-tuning\n# Load, tokenize, and format examples for the model"

    # --- section-13.3.html ---
    if 'section-13.3' in filepath:
        if 'torch' in after_lower:
            return "# Configure PyTorch training with gradient accumulation and mixed precision\n# These settings control memory usage and effective batch size"
        return "# Set up the training loop configuration\n# Specify learning rate, batch size, and optimization parameters"

    # --- section-13.4.html ---
    if 'section-13.4' in filepath:
        if 'json' in after_lower and ('jsonl' in after_lower or 'format' in after_lower):
            return "# Format training data as JSONL for the OpenAI fine-tuning API\n# Each line contains a messages array with system, user, and assistant turns"
        if 'openai' in after_lower and ('fine_tun' in after_lower or 'FineTuning' in after):
            return "# Submit a fine-tuning job to the OpenAI API and monitor its progress\n# The job trains on your uploaded JSONL file and produces a custom model ID"
        if 'vertexai' in after_lower and 'tune' in after_lower:
            return "# Launch a Vertex AI fine-tuning job for a Gemini model\n# The training data is loaded from a GCS bucket or BigQuery table"
        if 'vertexai' in after_lower:
            return "# Evaluate the fine-tuned Gemini model on Vertex AI\n# Compare outputs against the base model to measure improvement"
        if 'anthropic' in after_lower:
            return "# Submit a fine-tuning job using the Anthropic API\n# Training data follows the Messages format with system/user/assistant turns"
        if 'together' in after_lower:
            return "# Launch a fine-tuning job on the Together AI platform\n# Together supports open-weight models like Llama and Mistral"
        if 'fireworks' in after_lower:
            return "# Fine-tune a model on the Fireworks AI platform\n# Fireworks provides fast inference for fine-tuned open-weight models"
        if 'dataclass' in after_lower:
            return "# Define a provider comparison framework for API-based fine-tuning\n# Track cost, supported models, and turnaround time across providers"
        return "# Configure API-based fine-tuning with the provider SDK\n# Upload training data and submit the fine-tuning job"

    # --- section-13.6.html ---
    if 'section-13.6' in filepath:
        if 'transformers' in after_lower and ('Trainer' in after or 'TrainingArguments' in after):
            return "# Configure Hugging Face Trainer with training arguments\n# Set learning rate schedule, batch size, and evaluation strategy"
        if 'transformers' in after_lower:
            return "# Load a pre-trained model for sequence classification fine-tuning\n# The classification head is initialized randomly on top of the base model"
        if 'torch' in after_lower and ('weight' in after_lower or 'CrossEntropy' in after):
            return "# Implement class-weighted loss for imbalanced dataset fine-tuning\n# Minority classes receive higher loss weights to counteract skew"
        return "# Set up the fine-tuning training configuration\n# Control learning rate, regularization, and checkpoint strategy"

    # --- section-13.7.html ---
    if 'section-13.7' in filepath:
        if 'transformers' in after_lower:
            return "# Load the fine-tuned model and run inference on test examples\n# Compare outputs against the base model to quantify improvement"
        if 'typing' in after_lower or 'dataclass' in after_lower:
            return "# Define evaluation metrics and comparison structures\n# Track per-task accuracy, latency, and cost across model versions"
        return "# Evaluate the fine-tuned model against the base model\n# Measure task-specific performance and check for regression on general tasks"

    # --- section-14.1.html ---
    if 'section-14.1' in filepath:
        if 'LoraConfig' in after or 'lora_config' in after_lower:
            return "# Configure LoRA adapter parameters: rank, alpha, target modules\n# Lower rank reduces trainable parameters; alpha scales the adapter contribution"
        if 'get_peft_model' in after:
            return "# Wrap the base model with a LoRA adapter using get_peft_model\n# Only the low-rank adapter matrices are trainable; base weights are frozen"
        if 'merge_and_unload' in after or 'save_pretrained' in after:
            return "# Merge the trained LoRA adapter back into the base model weights\n# The merged model runs at full speed with no adapter overhead"
        return "# Set up parameter-efficient fine-tuning with LoRA adapters\n# Freeze the base model and train only the low-rank decomposition matrices"

    # --- section-14.2.html ---
    if 'section-14.2' in filepath:
        if 'BitsAndBytes' in after or 'bnb' in after_lower or 'quantiz' in after_lower or '4bit' in after_lower or 'load_in_4bit' in after:
            return "# Load the base model in 4-bit precision using BitsAndBytes\n# QLoRA combines 4-bit quantization with LoRA for memory-efficient fine-tuning"
        if 'LoraConfig' in after:
            return "# Configure QLoRA adapter parameters on top of the quantized base\n# The adapter trains in float16 while the base stays in 4-bit NormalFloat"
        if 'prepare_model' in after:
            return "# Prepare the quantized model for LoRA training\n# Enable gradient checkpointing and cast layer norms to float32 for stability"
        return "# Set up QLoRA: 4-bit quantized base model with LoRA adapters\n# This reduces GPU memory by 4x compared to full-precision fine-tuning"

    # --- section-14.3.html ---
    if 'section-14.3' in filepath:
        if 'unsloth' in after_lower or 'FastLanguageModel' in after:
            return "# Load a model with Unsloth for 2x faster LoRA fine-tuning\n# Unsloth fuses kernels and optimizes memory layout automatically"
        if 'trl' in after_lower or 'SFTTrainer' in after:
            return "# Fine-tune with TRL's SFTTrainer for supervised instruction tuning\n# SFTTrainer handles chat template formatting and packing automatically"
        return "# Configure a PEFT training framework for efficient fine-tuning\n# Select the appropriate tool based on model size and hardware constraints"

    # --- section-15.1.html ---
    if 'section-15.1' in filepath:
        if 'torch' in after_lower and ('kl_div' in after_lower or 'KL' in after or 'soft_loss' in after_lower or 'distill' in after_lower):
            return "# Compute the KL-divergence distillation loss between teacher and student\n# Soft targets from the teacher transfer more information than hard labels"
        if 'torch' in after_lower and ('student' in after_lower or 'DistilledModel' in after):
            return "# Define the student model architecture for knowledge distillation\n# The student is smaller but trained to mimic the teacher's output distribution"
        if 'asyncio' in after_lower or 'async ' in after:
            return "# Generate teacher labels asynchronously for large-scale distillation\n# Async batching maximizes throughput when labeling with an API-based teacher"
        if 'datasets' in after_lower or 'load_dataset' in after:
            return "# Load and prepare the distillation dataset with teacher-generated labels\n# Each example pairs an input with the teacher model's soft predictions"
        return "# Set up the knowledge distillation training pipeline\n# Train a smaller student model to approximate the teacher's behavior"

    # --- section-15.2.html ---
    if 'section-15.2' in filepath:
        if 'torch' in after_lower:
            return "# Implement model merging by interpolating weight tensors\n# Linear interpolation (LERP/SLERP) blends capabilities from multiple models"
        return "# Configure model merging parameters and weight interpolation\n# Combine strengths of multiple fine-tuned models without additional training"

    # --- section-15.3.html ---
    if 'section-15.3' in filepath:
        if 'datasets' in after_lower or 'load_dataset' in after:
            return "# Load evaluation datasets for comparing distilled vs. base models\n# Use held-out test sets that neither model saw during training"
        if 'transformers' in after_lower:
            return "# Load both the teacher and student models for side-by-side evaluation\n# Measure accuracy, latency, and memory footprint for each"
        if 'torch' in after_lower and ('latency' in after_lower or 'benchmark' in after_lower or 'time' in after_lower):
            return "# Benchmark inference latency and throughput for the distilled model\n# Compare against the teacher to quantify the speed-quality tradeoff"
        if 'torch' in after_lower:
            return "# Evaluate the distilled model on downstream tasks using PyTorch\n# Compute accuracy, F1, and per-class metrics"
        return "# Set up the evaluation pipeline for distilled models\n# Compare student performance against the teacher on target tasks"

    # Generic fallback
    return "# Set up imports for this code example\n# The following libraries handle the core operations shown below"


def fix_captions(content, filepath):
    """Replace generic code captions with specific ones."""
    fname = os.path.basename(filepath)

    # Fix "Making an API call to the language model provider..." caption
    api_caption = "Making an API call to the language model provider. The response object contains both the generated text and metadata useful for monitoring token usage and latency."

    if api_caption in content:
        # Need to find each occurrence and determine what code precedes it
        parts = content.split(api_caption)
        new_parts = [parts[0]]

        for i in range(1, len(parts)):
            before = parts[i-1] if i > 0 else ""
            # Get the code block before this caption
            replacement = get_specific_api_caption(before, filepath, i)
            new_parts.append(replacement + parts[i])

        content = "".join(new_parts)

    # Fix "Configuration setup for the pipeline..." caption
    config_caption = "Configuration setup for the pipeline. These settings control resource allocation and behavior; adjust them based on your hardware and use case."

    if config_caption in content:
        parts = content.split(config_caption)
        new_parts = [parts[0]]

        for i in range(1, len(parts)):
            before = parts[i-1] if i > 0 else ""
            replacement = get_specific_config_caption(before, filepath, i)
            new_parts.append(replacement + parts[i])

        content = "".join(new_parts)

    return content


def get_specific_api_caption(before, filepath, occurrence):
    """Get a specific replacement for the generic API call caption."""
    before_lower = before[-1500:].lower() if len(before) > 1500 else before.lower()

    if 'section-9.1' in filepath:
        if 'stream' in before_lower and 'haiku' in before_lower:
            return "Streaming a chat completion with Server-Sent Events. Each chunk delivers an incremental delta of generated tokens, enabling real-time display in the UI."
        if 'system' in before_lower and 'multi-turn' in before_lower:
            return "Using the multi-turn message format with system, user, and assistant roles. The system message defines behavioral constraints while user and assistant messages establish conversation context."
        return "Sending a chat completion request and extracting the generated text along with token usage counts for cost tracking."

    if 'section-9.3' in filepath:
        if 'helicone' in before_lower:
            return "Routing an API call through Helicone for automatic logging of latency, token counts, cost, and custom metadata. The dashboard aggregates these metrics for monitoring."
        return "Sending a request through the AI gateway proxy. The gateway adds observability, caching, and routing without changing the application code."

    if 'section-10.2' in filepath:
        return "Implementing a ReAct (Reason + Act) agent loop. The model iterates through tool calls and observations until it gathers enough information to produce a final answer."

    if 'section-10.3' in filepath:
        return "A generate, critique, and revise loop using three sequential LLM calls per round. The critique step identifies specific weaknesses; the revision step addresses each one."

    if 'section-11.3' in filepath:
        return "Using a small LLM (gpt-4o-mini) as a complexity router. The router classifies each request into a model tier (regex, classifier, small_llm, or large_llm) based on estimated difficulty."

    if 'section-11.5' in filepath:
        return "A two-layer hybrid extraction pipeline combining spaCy NER with LLM-based extraction. Classical NER handles standard entities at near-zero cost; the LLM layer extracts domain-specific entities and relations."

    if 'section-12.7' in filepath:
        return "Rejection sampling for reasoning trace generation. The model generates 32 candidate solutions; only traces that produce the verified correct answer are retained for training data."

    return "Sending a request to the LLM API and processing the structured response."


def get_specific_config_caption(before, filepath, occurrence):
    """Get a specific replacement for the generic config caption."""
    before_lower = before[-1500:].lower() if len(before) > 1500 else before.lower()

    if 'section-9.1' in filepath:
        if 'genai' in before_lower or 'gemini' in before_lower or 'google' in before_lower:
            return "Calling Google Gemini with GenerateContentConfig. The genai SDK uses different terminology (contents instead of messages, model instead of assistant) but follows the same conversational pattern."
        if 'bedrock' in before_lower or 'boto3' in before_lower:
            return "Calling Claude on AWS Bedrock via boto3. IAM credentials replace API keys, and the invoke_model method wraps the Anthropic Messages format in an AWS-native interface."
        if 'cache_control' in before_lower or 'cache_creation' in before_lower:
            return "Using Anthropic prompt caching with cache_control markers. Cached prefixes receive a discount on subsequent requests that share the same system prompt."
        return "Configuring the API client and request parameters for the specific provider and use case."

    if 'section-9.3' in filepath:
        if 'portkey' in before_lower:
            return "Routing requests through the Portkey AI gateway with fallback strategy and semantic caching. The OpenAI client is repointed to Portkey's URL; application code remains unchanged."
        if 'resilient' in before_lower or 'fallback' in before_lower or 'circuit' in before_lower:
            return "A multi-layer resilience pipeline that chains budget enforcement, cache lookup, primary model, fallback model, and static responses. Each layer is tried in order until one succeeds."
        return "Configuring the production API pipeline with caching, routing, and cost controls."

    if 'section-10.3' in filepath:
        return "Using DSPy's ChainOfThought module with a FactCheck signature. DSPy generates the prompt automatically from the typed signature; the optimizer can later improve it without manual editing."

    if 'section-10.4' in filepath:
        return "A Promptfoo regression test suite comparing two prompt versions across two models. Test case 3 checks for prompt injection resistance; the v2.1 prompt fixes this vulnerability."

    if 'section-11.4' in filepath:
        if 'pareto' in before_lower:
            return "Pareto frontier analysis of ten model configurations. Six configs are Pareto-optimal, meaning no other config achieves both higher accuracy and lower cost. The hybrid router (BERT + GPT-4o) appears on the frontier."
        return "Benchmarking model configurations across accuracy, cost per query, and latency to identify the cost-performance tradeoff surface."

    if 'section-12.4' in filepath:
        if 'repetit' in before_lower or 'filter' in before_lower:
            return "A composable FilterPipeline that chains length, quality score, and repetition checks. Each filter returns a pass/fail result with a reason, enabling detailed rejection analytics."
        if 'distilabel' in before_lower:
            return "A Distilabel pipeline that generates three response candidates per seed instruction, then scores each using UltraFeedback criteria. High-scoring candidates form the training set."
        return "Applying multi-stage quality filters to synthetic data before use in training."

    if 'section-12.5' in filepath:
        return "A Label Studio ML backend that uses GPT-4o-mini for pre-labeling. The backend classifies sentiment, and human annotators review and correct the predictions in the Label Studio UI."

    if 'section-13.1' in filepath:
        return "Configuring catastrophic forgetting mitigation with a ForgettingMitigationConfig dataclass. The 70/30 data mix blends task-specific and general data; get_data_mix() calculates the exact sample counts."

    if 'section-13.6' in filepath:
        return "A WeightedTrainer subclass that applies class-weighted CrossEntropyLoss. The sqrt-inverse weighting strategy gives the rare class (2% frequency) a 2.46x loss multiplier to counteract class imbalance."

    if 'section-14.3' in filepath:
        return "A complete Axolotl YAML configuration for QLoRA fine-tuning of Llama 3.1 8B. Key settings include 4-bit quantization, LoRA rank 32, sample packing, and cosine learning rate scheduling."

    return "Configuring the pipeline parameters for the specific training or inference task."


def process_file(filepath):
    """Process a single HTML file to fix generic captions and comments."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Phase 1: Fix generic import comments
    content = fix_import_comments(content, filepath)

    # Phase 2: Fix generic captions
    content = fix_captions(content, filepath)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# List of all files to process
files = []
base = "E:/Projects/LLMCourse"

# Part 3
for sec in ['section-9.1', 'section-9.2', 'section-9.3', 'section-9.4']:
    files.append(f"{base}/part-3-working-with-llms/module-09-llm-apis/{sec}.html")

for sec in ['section-10.2', 'section-10.3', 'section-10.4']:
    files.append(f"{base}/part-3-working-with-llms/module-10-prompt-engineering/{sec}.html")

for sec in ['section-11.1', 'section-11.2', 'section-11.3', 'section-11.4', 'section-11.5']:
    files.append(f"{base}/part-3-working-with-llms/module-11-hybrid-ml-llm/{sec}.html")

# Part 4
for sec in ['section-12.1', 'section-12.2', 'section-12.3', 'section-12.4', 'section-12.5', 'section-12.6', 'section-12.7']:
    files.append(f"{base}/part-4-training-adapting/module-12-synthetic-data/{sec}.html")

for sec in ['section-13.1', 'section-13.2', 'section-13.3', 'section-13.4', 'section-13.6', 'section-13.7']:
    files.append(f"{base}/part-4-training-adapting/module-13-fine-tuning-fundamentals/{sec}.html")

for sec in ['section-14.1', 'section-14.2', 'section-14.3']:
    files.append(f"{base}/part-4-training-adapting/module-14-peft/{sec}.html")

for sec in ['section-15.1', 'section-15.2', 'section-15.3']:
    files.append(f"{base}/part-4-training-adapting/module-15-distillation-merging/{sec}.html")


changed = 0
for filepath in files:
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        continue
    if process_file(filepath):
        changed += 1
        print(f"FIXED: {os.path.basename(filepath)}")
    else:
        print(f"NO CHANGES: {os.path.basename(filepath)}")

print(f"\nTotal files changed: {changed}/{len(files)}")
