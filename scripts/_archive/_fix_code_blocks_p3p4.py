#!/usr/bin/env python3
"""Fix ALL code blocks in Parts 3-4: captions, comments, prose references."""
import re, glob, os

os.chdir("E:/Projects/LLMCourse")
files = sorted(
    glob.glob("part-3-working-with-llms/module-*/section-*.html") +
    glob.glob("part-4-training-adapting/module-*/section-*.html")
)

def detect_language(code):
    if re.search(r'\b(import |from |def |class |print\()', code): return 'python'
    if re.search(r'\b(const |let |var |function |=>)', code): return 'javascript'
    return 'python'

def cp(lang):
    return '//' if lang == 'javascript' else '#'

def has_comments(code_text, lang='python'):
    lines = code_text.strip().split('\n')
    ne = [l.strip() for l in lines if l.strip()]
    if not ne: return True
    for l in ne[:3]:
        if l.startswith(cp(lang)) or '# ' in l or '// ' in l: return True
    return False

def plain(pre_content):
    return re.sub(r'<[^>]+>', '', pre_content).strip()

def gen_caption(ct):
    cl = ct.lower()
    tests = [
        ('openai' in cl and 'stream' in cl, "Streaming API call using the OpenAI client. Each chunk is processed incrementally, enabling real-time token display. This pattern is essential for interactive applications where perceived latency matters."),
        ('openai' in cl and 'batch' in cl, "Batch API workflow for asynchronous request processing. The JSONL format bundles multiple requests into a single submission. This approach trades latency for significant cost savings."),
        ('openai' in cl and ('chat.completions' in cl or 'completions.create' in cl) and 'function' not in cl and 'tool' not in cl, "Chat completion call using the OpenAI client library. The message array separates system instructions from user input, giving fine-grained control over model behavior. Token usage metadata helps track costs."),
        ('anthropic' in cl and 'cache' in cl, "Prompt caching with the Anthropic API to reduce repeated prefix costs. The cache control markers tell the API which portions to store across requests. Monitor the cache hit metrics to verify savings."),
        ('anthropic' in cl and 'tool' in cl, "Tool use with the Anthropic API, enabling the model to invoke external functions. The tool schema defines parameters the model can extract from the conversation. Your code executes the actual function and returns results."),
        ('anthropic' in cl, "Anthropic Messages API call showing the distinct parameter layout. The system prompt is a top-level parameter rather than a message role, and max_tokens is required. Content blocks provide structured access to generated text."),
        ('genai' in cl or ('google' in cl and 'generative' in cl), "Google Gemini API integration using the genai client. The configuration object bundles generation parameters, and usage metadata provides token counts for cost tracking."),
        ('boto3' in cl or 'bedrock' in cl, "AWS Bedrock API call using boto3. Authentication flows through IAM credentials rather than API keys, integrating naturally with existing AWS infrastructure."),
        (('vllm' in cl or 'localhost' in cl) and 'openai' in cl, "Self-hosted inference using vLLM with OpenAI-compatible endpoints. By pointing the standard OpenAI client at a local server, you can swap between cloud and self-hosted backends without changing application code."),
        ('retry' in cl or 'tenacity' in cl or 'backoff' in cl, "Retry logic with exponential backoff for handling transient API failures. The decorator wraps the API call transparently, so calling code does not need to manage retries. Jitter prevents thundering herd problems."),
        ('rate_limit' in cl or 'semaphore' in cl or 'throttl' in cl, "Rate limiting implementation to stay within API provider quotas. The concurrency control pattern prevents 429 errors. Adjust the limit based on your API tier."),
        ('async' in cl and ('gather' in cl or 'asyncio' in cl), "Asynchronous API calls using asyncio for concurrent request processing. Gathering multiple coroutines lets you overlap network latency across requests. This pattern is critical for throughput-sensitive workloads."),
        ('cache' in cl and ('redis' in cl or 'lru_cache' in cl or 'hash' in cl) and 'anthropic' not in cl, "Response caching layer to avoid redundant API calls for identical inputs. The cache key is derived from the request parameters. This reduces both latency and cost."),
        ('circuit' in cl or 'breaker' in cl, "Circuit breaker pattern for graceful degradation when API endpoints fail. After consecutive failures the circuit opens and returns a fallback response. This prevents cascading failures in production pipelines."),
        ('cost' in cl and ('track' in cl or 'estimat' in cl or 'pric' in cl), "Cost tracking utility that estimates API spend from token usage. Mapping model names to per-token prices lets you monitor expenses programmatically."),
        (('function' in cl and 'tool' in cl) or 'function_call' in cl or 'tools=' in cl, "Function calling (tool use) pattern that lets the model invoke external tools. The function schema tells the model what parameters to extract, and your code executes the actual logic."),
        (('structured' in cl and 'output' in cl) or 'json_schema' in cl or 'response_format' in cl, "Structured output extraction using schema-guided generation. The response format constraint forces the model to produce valid JSON matching your schema. This eliminates brittle regex parsing."),
        ('embed' in cl and ('embedding' in cl or 'encode' in cl), "Embedding generation for converting text into dense vector representations. These vectors capture semantic meaning, enabling similarity search and clustering."),
        ('tiktoken' in cl, "Token counting for pre-flight cost estimation. Knowing the exact token count before sending a request lets you enforce budgets and avoid truncation surprises."),
        ('prompt' in cl and 'template' in cl, "Prompt template with parameterized slots for dynamic content injection. Separating the template from the data makes prompts reusable and testable."),
        ('few_shot' in cl or 'few-shot' in cl or ('examples' in cl and 'shot' in cl), "Few-shot prompting pattern providing labeled examples before the actual query. The examples establish the expected input-output format. Ordering and diversity of examples significantly affect output quality."),
        ('chain_of_thought' in cl or 'chain-of-thought' in cl or ('step by step' in cl and 'think' in cl), "Chain-of-thought prompting that instructs the model to reason step by step. Explicit reasoning steps improve accuracy on multi-step problems."),
        ('tree' in cl and 'thought' in cl, "Tree-of-thought prompting that explores multiple reasoning branches in parallel. Each candidate path is evaluated and the most promising branches expanded further."),
        ('reflection' in cl or 'self_refine' in cl, "Self-reflection pattern where the model critiques and refines its own output. The feedback loop catches errors that a single-pass generation would miss."),
        ('injection' in cl or 'jailbreak' in cl or 'guardrail' in cl, "Prompt injection defense mechanism that sanitizes inputs before they reach the model. Layered defenses combine input validation, output filtering, and structural separation of instructions from data."),
        ('qlora' in cl or ('quantiz' in cl and 'lora' in cl), "QLoRA setup combining quantization with LoRA adapters. The base model loads in 4-bit precision while adapters train in full precision. This enables fine-tuning large models on consumer GPUs."),
        ('lora' in cl, "LoRA (Low-Rank Adaptation) configuration for parameter-efficient fine-tuning. Only the low-rank adapter matrices are trained, keeping the base model frozen. This reduces memory requirements by orders of magnitude."),
        ('peft' in cl, "PEFT adapter configuration for parameter-efficient fine-tuning. Only adapter weights are trained while the base model stays frozen. This reduces memory by orders of magnitude compared to full fine-tuning."),
        ('quantiz' in cl or 'bitsandbytes' in cl, "Quantization configuration for reducing model memory footprint. Lower precision (4-bit or 8-bit) trades minimal accuracy loss for substantial memory savings."),
        ('sftrainer' in cl or 'sft_trainer' in cl, "Supervised fine-tuning trainer setup with dataset and hyperparameters. The SFTTrainer handles tokenization, batching, and gradient accumulation automatically."),
        ('trainingarguments' in cl or 'training_args' in cl, "Training arguments configuration controlling the optimization process. Key parameters include learning rate schedule, batch size, and evaluation frequency."),
        ('trainer' in cl and ('train()' in cl or '.train(' in cl), "Training execution with the Hugging Face Trainer API. The trainer handles the loop, evaluation, checkpointing, and logging."),
        ('fine_tun' in cl or 'fine-tun' in cl or 'finetun' in cl, "Fine-tuning pipeline configuration with training hyperparameters. The learning rate, batch size, and epochs control the optimization trajectory."),
        ('dataset' in cl and ('load' in cl or 'from_' in cl), "Dataset loading and preparation for model training or evaluation. The preprocessing step formats raw data into the structure expected by the trainer."),
        ('tokeniz' in cl and ('encode' in cl or 'decode' in cl or 'tokenizer(' in cl), "Tokenization pipeline converting raw text into model-ready input IDs. The tokenizer handles special tokens, padding, and truncation automatically."),
        ('eval' in cl and ('metric' in cl or 'accuracy' in cl or 'f1' in cl or 'rouge' in cl), "Evaluation pipeline computing metrics on model predictions. Automated metrics provide a quick signal; supplement them with qualitative review."),
        ('wandb' in cl or 'mlflow' in cl or 'tensorboard' in cl, "Experiment tracking for monitoring training runs. Logging metrics and artifacts makes runs reproducible and comparable."),
        ('reward' in cl and 'model' in cl, "Reward model setup for scoring candidate outputs against human preferences. The reward signal guides the policy model during reinforcement learning."),
        ('dpo' in cl or 'direct preference' in cl, "DPO training loop that skips the reward model entirely. By optimizing directly on preference pairs, DPO simplifies the RLHF pipeline."),
        ('rlhf' in cl or 'ppo' in cl, "RLHF training loop using PPO to optimize the language model against a reward signal. The KL divergence penalty prevents drift from the reference model."),
        ('constitutional' in cl, "Constitutional AI pipeline where the model self-critiques using a set of principles. Each principle acts as a filter, and the model revises its output to comply."),
        ('preference' in cl and ('pair' in cl or 'chosen' in cl), "Preference data preparation formatting human comparisons into training pairs. Each pair contains a chosen and rejected response for the same prompt."),
        ('distill' in cl or ('teacher' in cl and 'student' in cl), "Knowledge distillation transferring capabilities from a larger teacher to a smaller student. The student learns from soft probability distributions rather than hard labels."),
        ('merg' in cl and ('model' in cl or 'weight' in cl), "Model merging combining weights from multiple fine-tuned checkpoints. No additional training is required, making this approach extremely efficient."),
        ('attention' in cl and ('weight' in cl or 'score' in cl or 'visualiz' in cl), "Attention weight visualization showing which input tokens the model focuses on. High scores indicate strong contextual dependency between token pairs."),
        ('probe' in cl or 'probing' in cl, "Probing classifier testing what information is encoded in hidden representations. A linear probe on frozen embeddings reveals whether the model has learned a particular feature."),
        ('logit' in cl and 'lens' in cl, "Logit lens technique projecting intermediate hidden states to the vocabulary space. By unembedding at each layer, you watch predictions evolve through the network."),
        ('activation' in cl and ('patch' in cl or 'steer' in cl), "Activation patching to test causal hypotheses about internal representations. Injecting activations from one forward pass into another isolates which components drive a behavior."),
        ('sae' in cl or 'sparse_autoencoder' in cl or 'sparse autoencoder' in cl, "Sparse autoencoder for decomposing dense activations into interpretable features. The sparsity penalty encourages each feature to activate for a narrow, coherent concept."),
        ('grad' in cl and ('salienc' in cl or 'attribut' in cl), "Gradient-based saliency analysis attributing model predictions to input features. Gradient magnitudes indicate feature importance."),
        ('neuron' in cl and ('ablat' in cl or 'zero' in cl), "Neuron ablation study zeroing out specific neurons to measure their causal effect. If ablating a neuron changes the prediction, that neuron is causally involved."),
        ('synthetic' in cl and ('generat' in cl or 'creat' in cl), "Synthetic data generation using an LLM to produce training examples. The prompt template controls style, difficulty, and format. Always validate a subset before training."),
        ('evol' in cl and 'instruct' in cl, "Evol-Instruct pipeline that progressively increases instruction complexity. Each round rewrites simple instructions into more challenging variants."),
        ('decontamin' in cl or 'ngram' in cl or 'n_gram' in cl, "Decontamination check ensuring training data does not leak benchmark answers. N-gram overlap detection flags suspicious matches."),
        ('quality' in cl and 'filter' in cl, "Quality filtering pipeline scoring and removing low-quality training examples. Combine heuristics with LLM-as-judge for higher precision."),
        ('persona' in cl and ('generat' in cl or 'sampl' in cl), "Persona-driven data generation varying style and perspective of synthetic examples. Diversity improves model robustness across user populations."),
        ('self_instruct' in cl or 'self-instruct' in cl, "Self-Instruct pipeline where the model generates its own training instructions. Seed tasks bootstrap the process; deduplication maintains quality."),
        ('sklearn' in cl or 'xgboost' in cl or 'lightgbm' in cl or 'logistic' in cl, "Traditional ML model serving as a fast, interpretable baseline. Classical models excel at structured tabular data where LLMs are overkill."),
        ('router' in cl or 'routing' in cl, "Request router directing queries to the appropriate model based on complexity. Simple queries use cheaper models; complex ones escalate to larger LLMs."),
        ('pipeline' in cl and ('step' in cl or 'stage' in cl), "Multi-stage pipeline combining components in sequence. Each stage handles the subtask it is best suited for. This modular design enables independent testing."),
        ('fallback' in cl or 'cascade' in cl, "Cascading fallback strategy trying progressively more capable models. If the lightweight model is confident, the expensive model is never called."),
        ('ensemble' in cl or 'voting' in cl, "Ensemble combining predictions from multiple models for improved robustness. Agreement increases confidence; disagreement flags uncertain cases."),
        ('confidence' in cl and ('score' in cl or 'threshold' in cl), "Confidence scoring mechanism gating downstream decisions on model certainty. Predictions below the threshold route to a fallback or human review."),
        ('class ' in cl and ('__init__' in cl or 'self.' in cl), "Class-based abstraction encapsulating the core logic into a reusable component. The constructor accepts configuration, and public methods expose primary operations."),
        ('test' in cl and ('assert' in cl or 'pytest' in cl), "Test suite verifying expected behavior across representative inputs. Assertions check both happy-path outputs and edge cases."),
        ('logging' in cl or 'logger' in cl, "Logging configuration for production observability. Structured entries capture request metadata, latency, and token counts."),
        ('fastapi' in cl or 'flask' in cl, "Web API endpoint wrapping the LLM call in an HTTP service. Add authentication and rate limiting before exposing to external clients."),
        ('langchain' in cl, "LangChain integration composing LLM calls into multi-step chains. The framework abstracts provider differences behind a common interface."),
        ('transformers' in cl and ('from_pretrained' in cl or 'pipeline' in cl), "Hugging Face Transformers setup for local model inference. Loading locally avoids API dependencies and per-token costs."),
        ('torch' in cl and ('nn' in cl or 'forward' in cl), "PyTorch module implementing the core neural network computation. The forward method defines data flow through layers."),
        ('matplotlib' in cl or 'plt.' in cl, "Visualization of results for qualitative inspection. Plotting metrics reveals patterns that summary statistics may hide."),
        ('json' in cl and ('dump' in cl or 'load' in cl), "JSON serialization for data interchange between pipeline stages. Validate the schema after serialization to catch structural errors."),
        ('pandas' in cl or 'dataframe' in cl, "DataFrame operations for structured data manipulation. Inspect shape and sample rows after each transformation to verify correctness."),
    ]
    for cond, cap in tests:
        if cond: return cap
    if 'import' in cl:
        return "Implementation showing key operations in context. Study the imports and function calls to understand the dependency chain. Modify parameters to adapt this to your use case."
    return "Implementation illustrating the technique discussed above. Walk through the code to understand the control flow. Adjust parameters for your production requirements."

def gen_comments(ct, lang='python'):
    cl = ct.lower()
    p = cp(lang)
    pairs = [
        (('openai', 'stream'), (f"{p} Stream tokens incrementally as they are generated", f"{p} Collect and display each chunk for real-time feedback")),
        (('openai', 'batch'), (f"{p} Batch API: submit requests for async processing", f"{p} Create JSONL input, upload, and launch the batch job")),
        (('anthropic', 'cache'), (f"{p} Anthropic prompt caching: reuse prefixes across calls", f"{p} Monitor cache_read_input_tokens to verify savings")),
        (('anthropic', 'tool'), (f"{p} Anthropic tool use: model invokes external functions", f"{p} Define tool schemas and handle tool_use blocks")),
        (('boto3',), (f"{p} AWS Bedrock API using IAM authentication", f"{p} Model ID uses provider/model-name format")),
        (('bedrock',), (f"{p} AWS Bedrock API using IAM authentication", f"{p} Model ID uses provider/model-name format")),
        (('genai',), (f"{p} Google Gemini API: configure and send request", f"{p} Usage metadata provides token counts for billing")),
        (('vllm',), (f"{p} Self-hosted vLLM with OpenAI-compatible endpoints", f"{p} Same client code works for cloud and local")),
        (('tenacity',), (f"{p} Retry with exponential backoff for transient errors", f"{p} Jitter prevents synchronized retries")),
        (('backoff',), (f"{p} Retry with exponential backoff for transient errors", f"{p} Jitter prevents synchronized retries")),
        (('rate_limit',), (f"{p} Rate limiter to stay within API quotas", f"{p} Cap concurrent requests to avoid 429 errors")),
        (('semaphore',), (f"{p} Semaphore-based rate limiting for API calls", f"{p} Throttle outbound requests to stay within quotas")),
        (('circuit',), (f"{p} Circuit breaker for graceful API failure handling", f"{p} Opens after consecutive failures, returns fallback")),
        (('breaker',), (f"{p} Circuit breaker for graceful API failure handling", f"{p} Opens after consecutive failures, returns fallback")),
        (('lora', 'peft'), (f"{p} LoRA adapters: train low-rank matrices, freeze base", f"{p} Reduces memory dramatically vs full fine-tuning")),
        (('lora',), (f"{p} LoRA: train low-rank adapter matrices only", f"{p} Base model weights stay frozen during training")),
        (('peft',), (f"{p} PEFT adapters for parameter-efficient fine-tuning", f"{p} Only adapter weights update; base model frozen")),
        (('qlora',), (f"{p} QLoRA: 4-bit quantization plus LoRA adapters", f"{p} Fine-tune large models on consumer GPUs")),
        (('quantiz',), (f"{p} Quantization for reduced-precision model loading", f"{p} Lower precision saves memory with minimal accuracy loss")),
        (('bitsandbytes',), (f"{p} BitsAndBytes quantization for memory efficiency", f"{p} NF4 data type provides optimal 4-bit quality")),
        (('sftrainer',), (f"{p} SFTTrainer: supervised fine-tuning with auto batching", f"{p} Handles tokenization and gradient accumulation")),
        (('trainingarguments',), (f"{p} Training hyperparameters for optimization", f"{p} Learning rate, batch size, schedule control convergence")),
        (('dpo',), (f"{p} DPO: optimize on preference pairs, no reward model", f"{p} Implicit reward from policy log-probabilities")),
        (('ppo',), (f"{p} PPO-based RLHF against a learned reward signal", f"{p} KL penalty prevents drift from reference model")),
        (('reward',), (f"{p} Reward model scoring outputs against preferences", f"{p} Higher scores correlate with preferred responses")),
        (('distill',), (f"{p} Distillation: transfer teacher to student", f"{p} Soft labels preserve richer information")),
        (('teacher', 'student'), (f"{p} Teacher-student distillation pipeline", f"{p} Student learns from soft distributions")),
        (('merg',), (f"{p} Merge weights from fine-tuned checkpoints", f"{p} No additional training required")),
        (('logit', 'lens'), (f"{p} Logit lens: project hidden states to vocabulary", f"{p} Watch predictions evolve layer by layer")),
        (('probe',), (f"{p} Probing classifier on frozen embeddings", f"{p} Test what features the model has learned")),
        (('probing',), (f"{p} Probing classifier on frozen embeddings", f"{p} Test what features the model has learned")),
        (('attention', 'weight'), (f"{p} Visualize attention weights across tokens", f"{p} High scores show contextual dependency")),
        (('attention', 'score'), (f"{p} Extract attention scores across heads", f"{p} Patterns reveal model focus")),
        (('activation', 'patch'), (f"{p} Activation patching to isolate causal components", f"{p} Inject activations between forward passes")),
        (('activation', 'steer'), (f"{p} Activation steering to modify model behavior", f"{p} Add vectors to shift outputs")),
        (('sae',), (f"{p} Sparse autoencoder for interpretable features", f"{p} Sparsity encourages coherent activation")),
        (('sparse_autoencoder',), (f"{p} Sparse autoencoder for interpretable features", f"{p} Sparsity encourages coherent activation")),
        (('synthetic', 'generat'), (f"{p} Generate synthetic training data via LLM", f"{p} Validate a subset before training")),
        (('synthetic', 'creat'), (f"{p} Create synthetic examples with controlled properties", f"{p} Template controls style and format")),
        (('evol', 'instruct'), (f"{p} Evol-Instruct: increase instruction complexity", f"{p} Each round rewrites into harder variants")),
        (('quality', 'filter'), (f"{p} Filter low-quality examples from dataset", f"{p} Combine heuristics with LLM-as-judge")),
        (('decontamin',), (f"{p} Check for benchmark leakage in training data", f"{p} N-gram overlap flags suspicious matches")),
        (('persona',), (f"{p} Persona-driven generation for diversity", f"{p} Each persona adds different style")),
        (('sklearn',), (f"{p} Traditional ML baseline for comparison", f"{p} Classical models excel on tabular data")),
        (('xgboost',), (f"{p} Gradient boosting baseline", f"{p} Compare against LLM-based alternatives")),
        (('router',), (f"{p} Route queries to models by complexity", f"{p} Simple queries use fast models")),
        (('confidence', 'threshold'), (f"{p} Confidence gating for uncertain predictions", f"{p} Below threshold, route to fallback")),
        (('langchain',), (f"{p} LangChain: compose LLM calls into chains", f"{p} Abstracts provider differences")),
        (('transformers',), (f"{p} Hugging Face Transformers model loading", f"{p} GPU acceleration recommended")),
        (('torch', 'nn'), (f"{p} PyTorch module for computation", f"{p} Forward method defines data flow")),
        (('pandas',), (f"{p} DataFrame operations for data analysis", f"{p} Check shape after transforms")),
        (('matplotlib',), (f"{p} Visualization for result inspection", f"{p} Plots reveal hidden patterns")),
        (('plt.',), (f"{p} Plot results for visual inspection", f"{p} Adjust labels for clarity")),
        (('json',), (f"{p} JSON data interchange", f"{p} Validate schema after serialization")),
        (('fastapi',), (f"{p} HTTP endpoint for LLM service", f"{p} Add auth for production")),
        (('flask',), (f"{p} Flask endpoint for predictions", f"{p} Add auth before deploying")),
        (('logging',), (f"{p} Logging for observability", f"{p} Capture latency and errors")),
        (('test', 'assert'), (f"{p} Tests for behavior verification", f"{p} Run after changes")),
        (('class ', '__init__'), (f"{p} Reusable class for pipeline logic", f"{p} Config via constructor")),
        (('constitutional',), (f"{p} Constitutional AI: self-critique", f"{p} Revise to comply with principles")),
        (('preference', 'pair'), (f"{p} Format preference pairs", f"{p} Quality determines alignment")),
        (('preference', 'chosen'), (f"{p} Preference data: chosen vs rejected", f"{p} Consistent labeling is critical")),
    ]
    for keys, (c1, c2) in pairs:
        if all(k in cl for k in keys): return [c1, c2]
    if 'anthropic' in cl: return [f"{p} Anthropic Messages API call", f"{p} System prompt is a top-level parameter"]
    if 'openai' in cl: return [f"{p} OpenAI chat completion call", f"{p} Messages separate system from user"]
    if 'async' in cl and 'await' in cl: return [f"{p} Async implementation for concurrent I/O", f"{p} Overlap network latency"]
    if 'import' in cl: return [f"{p} Set up dependencies and configure", f"{p} Adjust parameters for your setup"]
    return [f"{p} Implementation of the technique above", f"{p} Modify parameters for your needs"]

def gen_prose(ct, n):
    cl = ct.lower()
    tests = [
        ('stream' in cl and ('openai' in cl or 'anthropic' in cl), f"Code Fragment {n} shows how to stream tokens as they are generated."),
        ('batch' in cl and 'openai' in cl, f"Code Fragment {n} demonstrates the Batch API workflow."),
        ('openai' in cl and 'chat.completions' in cl, f"Code Fragment {n} illustrates a chat completion call."),
        ('anthropic' in cl and 'cache' in cl, f"Code Fragment {n} demonstrates prompt caching."),
        ('anthropic' in cl, f"Code Fragment {n} shows the Anthropic Messages API."),
        ('genai' in cl, f"Code Fragment {n} demonstrates the Google Gemini API."),
        ('boto3' in cl or 'bedrock' in cl, f"Code Fragment {n} shows the AWS Bedrock integration."),
        ('retry' in cl or 'tenacity' in cl, f"Code Fragment {n} implements retry with exponential backoff."),
        ('rate_limit' in cl or 'semaphore' in cl, f"Code Fragment {n} shows rate limiting."),
        ('async' in cl and ('gather' in cl or 'asyncio' in cl), f"Code Fragment {n} implements concurrent API calls."),
        ('cache' in cl and 'hash' in cl, f"Code Fragment {n} adds a caching layer."),
        ('circuit' in cl or 'breaker' in cl, f"Code Fragment {n} implements the circuit breaker pattern."),
        ('cost' in cl and 'track' in cl, f"Code Fragment {n} tracks API costs."),
        ('tool' in cl and ('function' in cl or 'tools=' in cl), f"Code Fragment {n} demonstrates function calling."),
        ('structured' in cl and 'output' in cl, f"Code Fragment {n} extracts structured output."),
        ('tiktoken' in cl, f"Code Fragment {n} counts tokens for cost estimation."),
        ('prompt' in cl and 'template' in cl, f"Code Fragment {n} defines a prompt template."),
        ('chain_of_thought' in cl or 'step by step' in cl, f"Code Fragment {n} uses chain-of-thought prompting."),
        ('tree' in cl and 'thought' in cl, f"Code Fragment {n} applies tree-of-thought reasoning."),
        ('reflection' in cl or 'self_refine' in cl, f"Code Fragment {n} implements self-reflection."),
        ('injection' in cl or 'guardrail' in cl, f"Code Fragment {n} demonstrates injection defenses."),
        ('lora' in cl or 'peft' in cl, f"Code Fragment {n} configures LoRA adapters."),
        ('quantiz' in cl or 'bitsandbytes' in cl, f"Code Fragment {n} sets up quantization."),
        ('sftrainer' in cl or 'sft' in cl, f"Code Fragment {n} sets up supervised fine-tuning."),
        ('trainingarguments' in cl, f"Code Fragment {n} defines training hyperparameters."),
        ('trainer' in cl and 'train' in cl, f"Code Fragment {n} runs the training loop."),
        ('dpo' in cl, f"Code Fragment {n} implements DPO training."),
        ('ppo' in cl or 'rlhf' in cl, f"Code Fragment {n} shows the RLHF loop."),
        ('reward' in cl and 'model' in cl, f"Code Fragment {n} sets up the reward model."),
        ('constitutional' in cl, f"Code Fragment {n} implements constitutional AI."),
        ('preference' in cl and ('pair' in cl or 'chosen' in cl), f"Code Fragment {n} prepares preference data."),
        ('distill' in cl or 'teacher' in cl, f"Code Fragment {n} implements distillation."),
        ('merg' in cl and ('model' in cl or 'weight' in cl), f"Code Fragment {n} demonstrates model merging."),
        ('attention' in cl and 'weight' in cl, f"Code Fragment {n} visualizes attention patterns."),
        ('logit' in cl and 'lens' in cl, f"Code Fragment {n} applies the logit lens."),
        ('probe' in cl or 'probing' in cl, f"Code Fragment {n} trains a probing classifier."),
        ('activation' in cl and ('patch' in cl or 'steer' in cl), f"Code Fragment {n} performs activation patching."),
        ('sae' in cl or 'sparse_autoencoder' in cl, f"Code Fragment {n} trains a sparse autoencoder."),
        ('synthetic' in cl and 'generat' in cl, f"Code Fragment {n} generates synthetic training data."),
        ('evol' in cl and 'instruct' in cl, f"Code Fragment {n} applies Evol-Instruct evolution."),
        ('quality' in cl and 'filter' in cl, f"Code Fragment {n} implements quality filtering."),
        ('decontamin' in cl, f"Code Fragment {n} performs decontamination."),
        ('dataset' in cl and ('load' in cl or 'from_' in cl), f"Code Fragment {n} loads the dataset."),
        ('tokeniz' in cl, f"Code Fragment {n} tokenizes text into model inputs."),
        ('sklearn' in cl or 'xgboost' in cl, f"Code Fragment {n} establishes a ML baseline."),
        ('router' in cl, f"Code Fragment {n} implements request routing."),
        ('ensemble' in cl, f"Code Fragment {n} combines model predictions."),
        ('confidence' in cl, f"Code Fragment {n} implements confidence gating."),
        ('class ' in cl and '__init__' in cl, f"Code Fragment {n} defines a reusable class."),
        ('vllm' in cl or 'localhost' in cl, f"Code Fragment {n} connects to a local server."),
        ('langchain' in cl, f"Code Fragment {n} uses LangChain composition."),
        ('transformers' in cl, f"Code Fragment {n} loads the model via Transformers."),
    ]
    for cond, intro in tests:
        if cond: return intro
    return f"The following snippet in Code Fragment {n} demonstrates the implementation."

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Remove code-caption before <pre>
    content = re.sub(r'(\s*<div class="code-caption">[^<]*</div>\s*)\n(\s*<pre>)', r'\n\2', content)

    pp = re.compile(r'<pre>.*?</pre>', re.DOTALL)
    matches = list(pp.finditer(content))
    if not matches: return 0, "no code blocks"
    nb = len(matches)

    for idx in range(nb-1, -1, -1):
        m = matches[idx]
        fn = idx + 1
        ps, pe = m.start(), m.end()
        pb = m.group()
        ct = plain(pb)
        lang = detect_language(ct)

        if not has_comments(ct, lang):
            coms = gen_comments(ct, lang)
            tag = '<pre><code>' if '<pre><code>' in pb else '<pre>'
            tp = pb.find(tag) + len(tag)
            at = pb[tp:]
            cl = '\n'.join(f'<span style="color:#6c7086">{c}</span>' for c in coms)
            if at.startswith('\n'):
                npb = pb[:tp] + cl + '\n' + at.lstrip('\n')
            else:
                npb = pb[:tp] + '\n' + cl + '\n' + at
            content = content[:ps] + npb + content[pe:]
            pe = ps + len(npb)

        ap = content[pe:]
        ro = 0
        s = ap.lstrip('\n\r\t ')
        wl = len(ap) - len(s)
        if s.startswith('<div class="code-output">'):
            ed = s.find('</div>')
            if ed != -1:
                ro = wl + ed + len('</div>')
        rest = ap[ro:]
        s2 = rest.lstrip('\n\r\t ')
        wl2 = len(rest) - len(s2)
        ecs = ece = None
        if s2.startswith('<div class="code-caption">'):
            ce = s2.find('</div>')
            if ce != -1:
                ecs = pe + ro + wl2
                ece = ecs + ce + len('</div>')

        ctn = plain(content[ps:pe])
        cap = gen_caption(ctn)
        nc = f'\n<div class="code-caption"><strong>Code Fragment {fn}:</strong> {cap}</div>'

        if ecs is not None and ece is not None:
            content = content[:ecs] + nc + content[ece:]
        else:
            ip = pe + ro
            content = content[:ip] + nc + content[ip:]

    matches = list(pp.finditer(content))
    for idx in range(len(matches)-1, -1, -1):
        m = matches[idx]
        fn = idx + 1
        ps = m.start()
        ct = plain(m.group())
        before = content[:ps]
        cr = before[-400:].lower() if len(before) > 400 else before.lower()
        refs = [f'code fragment {fn}', 'the following snippet', 'below, we',
                'the following code', 'the code below', 'shown below',
                'following example', 'snippet below', 'this snippet',
                'implementation below', 'consider the following',
                'illustrated below', 'we implement', 'the next snippet',
                'code shows', 'shown in code', 'here is the', 'here is a']
        if not any(r in cr for r in refs):
            prose = gen_prose(ct, fn)
            content = content[:ps] + f'\n    <p>{prose}</p>\n\n' + content[ps:]

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return nb, "updated"
    return nb, "no changes needed"

total = 0
for fp in files:
    nb, st = process_file(fp)
    total += nb
    print(f"  {fp}: {nb} blocks, {st}")
print(f"\nTotal: {total} code blocks across {len(files)} files")
