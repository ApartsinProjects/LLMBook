"""Fill in the 29 remaining placeholder self-check answers (8 sections) with
real editorial content. Each (file, question_match_snippet) maps to the
new answer HTML that replaces the placeholder.

Idempotent: re-runnable; only touches placeholders.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLACEHOLDER = (
    "[Answer pending editorial revision. Refer to the section text "
    "for guidance on this question.]"
)

# Per-file: list of (question_substring_marker, answer_html).
# The question_substring_marker is a unique snippet from the <p class="quiz-question">
# text used to locate the corresponding <details>...</details> block right after it.
ANSWERS: dict[str, list[tuple[str, str]]] = {
    "part-8-evaluation-production/module-28-evaluation-observability/section-28.8.html": [
        ("Name three systematic biases that affect LLM-as-judge",
         "Three common biases and mitigations: (1) <strong>Position bias</strong>: judges tend to prefer the first response in a pairwise comparison. Mitigate by randomizing the order on each call and averaging across positions. (2) <strong>Length bias</strong>: judges tend to prefer longer responses even when they are not more correct. Mitigate with length-controlled prompts or with the AlpacaEval length-residualization trick described later in the chapter. (3) <strong>Self-enhancement bias</strong>: a judge prefers responses written by its own model family. Mitigate by using a different model family for judging, or by ensembling judgments from multiple model families."),
        ("How does G-Eval use chain-of-thought reasoning to improve scoring",
         "Direct &quot;rate this on 1-5&quot; prompts give the model no scaffolding; it returns a single integer with whatever it anchors on. G-Eval first asks the judge to <em>enumerate</em> the evaluation criteria (relevance, fluency, factuality, &hellip;), then <em>score each criterion</em> individually with brief justification, then <em>combine</em> them into a final score. The decomposition forces the judge to attend to multiple sub-criteria rather than collapsing them into one number, which produces finer gradations, more reproducibility across runs, and an interpretable trail you can spot-check."),
        ("What is the advantage of using an open-source judge model like Prometheus",
         "<strong>Advantages</strong>: reproducible (frozen weights, no API drift), cost-stable (no per-token pricing), runs on your own GPUs (no rate limits, no data leaving your premises), Apache-2.0 licensed for commercial use. <strong>Trade-offs</strong>: less general-purpose than a frontier model, slightly weaker on open-ended creative judgment, and you take on the GPU-infrastructure burden. Aggregate benchmark scores tend to be a few points lower than GPT-4 but competitive on the criteria Prometheus was fine-tuned to evaluate."),
        ("AlpacaEval introduced length-controlled debiasing",
         "Long responses tend to win head-to-head comparisons even when they are not more correct, because they read as more thorough. Without correction, models can climb a leaderboard simply by being more verbose. The length-controlled correction fits a regression of preference scores against response length, computes a length-residualized score that subtracts the predicted-from-length component, and ranks models by the residual. Models can no longer game the leaderboard with verbosity alone; the metric measures quality above and beyond what length predicts."),
    ],
    "part-8-evaluation-production/module-29-production-engineering/section-29.7.html": [
        ("What is the key architectural advantage of llama.cpp",
         "<code>llama.cpp</code> is pure C++ with no Python runtime or CUDA dependency in its core path. Optional GPU backends (CUDA, Metal, Vulkan, ROCm) are compile-time choices, so the same source tree builds for Mac, Linux x86, ARM mobile, and Windows. Quantization is baked into the GGUF model-file format (Q4_K_M, Q8_0, &hellip;), so the runtime does not have to compute quantization tables dynamically. The result is a single self-contained binary plus a GGUF file: drops onto almost any device with a C++17 compiler and runs."),
        ("Ollama exposes an OpenAI-compatible API",
         "API compatibility means existing client tooling works unchanged when you swap a hosted endpoint for a local one. An application written against the OpenAI Python SDK can switch its <code>base_url</code> from <code>api.openai.com</code> to <code>localhost:11434</code> and get back the same response shape. No code change beyond environment variables, no rewriting prompts, no retraining client libraries. The cloud-to-edge transition becomes a configuration change rather than an engineering project, which is the practical reason Ollama spread so quickly."),
        ("MLX exploits Apple Silicon's unified memory architecture",
         "On Apple Silicon, the CPU and GPU share the same physical memory pool. MLX exploits this by skipping the explicit host-to-device copies that CUDA-style discrete-GPU runtimes have to perform for every input and output. For large models the savings compound: bandwidth is not spent shuffling weights between host and device, and you can run models that exceed an equivalent discrete-GPU's VRAM because you have access to the whole machine's memory. <code>llama.cpp</code> on Mac still operates as if the GPU were discrete and pays the copy cost."),
        ("In the quantization benchmark lab, you compared Q4_K_M and Q8_0",
         "Q4_K_M packs weights at ~4 bits each (about 2&times; smaller and 1.5-2&times; faster than Q8_0 at inference) but loses some accuracy; Q8_0 keeps 8-bit precision with much better fidelity at higher memory and latency cost. Decide based on your task's error tolerance: for chat and summarization on a 7B-13B model, Q4_K_M is usually indistinguishable from FP16 to a human reader; for code generation, math, or anything where small errors compound (citations, formulas), the precision gap matters and Q8_0 is worth the cost. Measure perplexity AND downstream task accuracy on a representative eval set before deciding, because perplexity alone underestimates real-world impact."),
    ],
    "part-8-evaluation-production/module-29-production-engineering/section-29.8.html": [
        ("How do LLM failures differ from traditional software failures",
         "Traditional failures tend to be deterministic and observable at the protocol layer: a function throws, a TCP connection drops, a database returns an error code. LLM failures are often probabilistic and silent: the same prompt may succeed nine times in a row and produce a confidently wrong answer on the tenth, with a 200 OK response and well-formed JSON throughout. Two failure modes unique to LLM applications: (a) <strong>hallucination</strong>, where the output is fluent and plausible but factually wrong; nothing in the response shape signals the failure. (b) <strong>Prompt-injection cascade</strong>, where one request's user content alters the model's behavior on a later request via shared memory or chained context, breaking the request-independence assumption that traditional retries depend on."),
        ("Explain the circuit breaker pattern for LLM systems",
         "The breaker is a state machine sitting in front of the LLM. It opens when one of three thresholds is crossed: (i) <strong>error rate</strong> exceeds a percentage over a rolling window (e.g. 50&percnt; failures in the last 30 seconds); (ii) <strong>latency</strong> P99 climbs above your SLO; or (iii) <strong>cost</strong> per minute exceeds the budget guardrail. While the breaker is open, requests skip the LLM entirely and fall through to a fallback: a cached response, a smaller model, or a polite degraded-service message. After a cool-down period a single probe request is allowed through; success closes the breaker, failure resets the timer. The pattern keeps a misbehaving upstream from taking the whole application down."),
        ("Why are cascading failures especially dangerous in multi-agent",
         "Agents in a pipeline call other agents, usually with retries. When one agent slows or fails, its callers retry, multiplying load on the failing component. If multiple callers share a model endpoint, the latency spreads laterally. Example scenario: a <em>research agent</em> calls a <em>browser agent</em> to fetch sources. The browser agent gets rate-limited by an upstream site. The research agent retries 5 times, burning through its token budget. The orchestrator marks the research agent unhealthy and spawns a fresh one, which calls the still-rate-limited browser. The cycle continues until the global request budget is exhausted and the entire pipeline times out. The lesson: circuit-break at every boundary, not just at the outermost one."),
        ("What makes defining SLOs (Service Level Objectives) for LLM systems",
         "Traditional APIs have a clean success/failure axis at the HTTP layer. LLM responses are <em>usually</em> successful at the protocol layer but may be wrong at the application layer, so an HTTP-200-based SLO measures the wrong thing. Quality metrics need explicit definition (groundedness, instruction-following, hallucination rate) and most of them are expensive to compute, so you cannot evaluate every request. Useful LLM-specific SLOs: <strong>groundedness rate &gt;= X&percnt;</strong> on a sampled 1-5&percnt; subset; <strong>refusal rate</strong> bounded above and below; <strong>P99 time-to-first-token</strong> for streaming UX; <strong>cost per conversation</strong> against a budget; <strong>human escalation rate</strong> as a leading indicator of model regression."),
    ],
    "part-7-multimodal-applications/module-26-multimodal/section-26.5.html": [
        ("What distinguishes a Vision-Language-Action (VLA) model from a standard",
         "A standard vision-language model (VLM) takes vision + text and produces text (caption, answer, classification). A Vision-Language-Action model additionally produces <strong>robot actions</strong>: joint angles, gripper commands, end-effector poses, or navigation primitives. The output is an executable control sequence, which means the model has to reason about physical feasibility (kinematics, contact, dynamics) in addition to describing what it sees. The action modality is what turns a perception system into a policy."),
        ("RT-2 demonstrated a key finding about web-scale pretraining for robotics",
         "RT-2 showed that vision-language pretraining on internet-scale data gives a robot policy <strong>semantic generalization</strong> it could never have learned from robot demonstrations alone. The model could correctly pick up an object (e.g. an apple) even though no apple had appeared in its robot training set, because &quot;apple&quot; existed in the web-scale VLM pretraining corpus. Previous robot-learning systems required every concept to appear in robot demonstrations; RT-2 transferred concepts from internet pretraining into robot actions. This collapsed the cost of teaching a robot a new noun from hours of demonstration to zero."),
        ("Why is sim-to-real transfer so challenging for embodied agents",
         "Simulators differ from reality in physics fidelity (friction coefficients, contact dynamics, mass distributions), sensor noise (idealized cameras vs real lens distortion), and visual appearance (uniform textures vs cluttered photographic detail). A policy that exploits simulator quirks (e.g. a slightly-too-slippery floor) fails the moment it touches a real surface. <strong>Domain randomization</strong> randomizes the differences during training (lighting, textures, masses, friction) so the policy must learn invariant features. <strong>System identification</strong> fits simulator parameters to real-world measurements, narrowing the gap from the simulator side. The two are complementary: randomize what you don't know, identify what you can measure."),
        ("OpenVLA supports LoRA fine-tuning on a single GPU",
         "Full fine-tuning of a 7B+ parameter VLA needs tens of GB of VRAM for weights plus optimizer states; LoRA adapters require under 1&percnt; of that. For robotics this matters even more than for text-only LLMs because: (a) every robot setup needs its own adapter (different actuators, sensors, gripper geometries, payload constraints), so the same base model has to be specialized many times; (b) robotics labs operate on smaller compute budgets than text-only LLM labs; (c) on-robot deployment is memory-constrained, so a frozen base model plus swappable adapters per task is far more practical than swapping whole 7B-parameter models."),
    ],
    "part-7-multimodal-applications/module-26-multimodal/section-26.6.html": [
        ("SayCan uses affordance scoring to ground LLM task plans",
         "LLMs generate plans that are <em>linguistically</em> plausible but may be <em>physically</em> impossible: telling a robot to &quot;pick up the cup&quot; when no cup is in view, or proposing actions the robot's body can't perform. SayCan grounds plans by scoring each candidate LLM-proposed action against an <strong>affordance function</strong> that estimates whether the action is currently feasible from the robot's current state. Without it, a robot could try to execute &quot;wash the dishes&quot; when the user asked for &quot;tidy up the room&quot; — the LLM produced a plausible interpretation, but the affordance check correctly vetoes actions for which the precondition (dirty dishes in reach, working sink) is not satisfied."),
        ("What is the key difference between Code-as-Policies",
         "<strong>Code-as-Policies</strong> generates Python at planning time that composes primitive APIs in arbitrary ways: the LLM has full Turing-complete flexibility but can produce unsafe combinations. <strong>Skill-library</strong> approaches expose a fixed set of pre-validated, hand-engineered skills; the LLM picks one skill per step, and safety is easier to certify because the surface area is bounded. Code-as-Policies is more capable (can solve unanticipated tasks) but harder to make safe (every line of generated code is a new attack surface for prompt injection or hallucinated APIs). Skill libraries trade some capability for tractable safety guarantees, which most production deployments need."),
        ("In multi-robot coordination, why is language a useful communication medium",
         "Humans designed natural language to convey intent flexibly: language lets agents negotiate, request clarification, share partial plans, and disagree productively. Ad-hoc message protocols force every new capability to be added to the protocol schema. <strong>Limitations</strong>: parsing ambiguity (the same sentence interpreted differently by different agents); bandwidth (a 50-byte JSON beats a 200-token natural-language description by 4&times;); latency (tokenization plus LLM-as-parser adds milliseconds per message); and uncertainty (no compile-time check that two agents mean the same thing). For real-time coordination, structured protocols win; for open-ended or exploratory coordination, language wins. Production systems typically pick one of the two as primary and use the other as the fallback."),
        ("Edge deployment for robots introduces hard latency constraints",
         "Strategies that help meet hard latency budgets: (a) <strong>two-tier planning</strong>: an on-robot small model runs the fast control loop while a cloud LLM plans slower high-level goals; (b) <strong>plan caching</strong> for recurring patterns so common situations don't re-invoke the LLM; (c) <strong>speculative execution</strong>: the robot acts on the most-likely plan while the LLM generates alternatives in parallel; (d) <strong>hierarchical control</strong>: slow LLM at the goal level, fast learned policy at the motor-control level; (e) <strong>quantization and distillation</strong> of the planning model down to a size that fits on-board hardware. Most production robot stacks combine 2-3 of these."),
    ],
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html": [
        ("You have 64 GPUs with 80 GB each and a 30B parameter model",
         "Memory budget in FP32: weights = 30B &times; 4 bytes = 120 GB. Gradients = another 120 GB. AdamW optimizer states (m, v) = 240 GB. Total per-replica: ~480 GB. With 64 GPUs &times; 80 GB = 5,120 GB total, storing the model once needs 480 / 80 &approx; 6 GPUs. <strong>FSDP</strong> (Fully Sharded Data Parallel) shards weights, gradients, and optimizer states across all 64 GPUs, giving ~7.5 GB per GPU for state. <strong>TP</strong> (Tensor Parallelism) shards each layer's matrices across GPUs, reducing activation memory and compute. <strong>PP</strong> (Pipeline Parallelism) puts different layers on different GPUs. <strong>DP</strong> (Data Parallel) replicates the model and shards the batch. A practical 64-GPU configuration: FSDP + 4-way TP + 2-way PP + 8-way DP (a 3D mesh, Megatron-style)."),
        ("Explain why pipeline parallelism introduces \"bubble\" time",
         "When you split a model into N pipeline stages, the first stage must finish its forward pass and send activations downstream before the second stage can start. The <em>bubble</em> is the wall-clock time during which not all stages are working. With a single batch the bubble is (N-1) forward times + (N-1) backward times; pipeline efficiency is approximately N / (N + N - 1), i.e. ~57&percnt; for N=4. <strong>Micro-batching</strong>: split the batch into K micro-batches and feed them through the pipeline like an assembly line, so stage 2 processes micro-batch 1 while stage 1 processes micro-batch 2. Efficiency improves to K / (K + N - 1); with K=8 and N=4 it climbs from 57&percnt; to ~73&percnt;, and interleaving the forward and backward passes pushes it higher still."),
        ("A training run on 512 GPUs loses one node every 8 hours",
         "TorchElastic detects when a node disappears, kills the existing rendezvous, restarts with the new world size, and reloads from the most recent checkpoint. <strong>Asynchronous distributed checkpointing</strong> writes the model and optimizer state to local RAM-disk in the background, then drains to remote storage out of the critical path, so checkpoint frequency does not dominate training wall-clock. Concretely: take a checkpoint every 30 minutes (cost: 5-15 seconds of synchronous stall via async). When a node fails, TorchElastic restarts the surviving GPUs within 1-2 minutes from the last checkpoint. Worst-case loss: ~30 minutes of work per failure. At one failure per 8 hours, the expected progress reduction is ~6&percnt; — viable for multi-week pretraining."),
    ],
    "part-2-understanding-llms/module-09-inference-optimization/section-9.7.html": [
        ("A standard softmax attention kernel makes three passes",
         "Standard attention computes Q @ K<sup>T</sup> (write the N&times;N attention matrix to HBM), softmax (read+write that matrix), then @ V (read it again and write the output) — three round-trips to HBM, which is the bottleneck on modern GPUs. <strong>FlashAttention</strong> <em>tiles</em> the attention matrix and never materializes it fully in HBM. Each output block is computed by streaming small tiles of Q, K, V through SRAM, keeping the running max and exp-sum in registers, and only HBM-writing the final output. Per block this is one HBM round-trip instead of three. Even though FlashAttention performs slightly <em>more</em> arithmetic (it recomputes some softmax pieces during the backward), HBM bandwidth dominates wall-clock time and the savings translate to 2-4&times; speedup with much lower memory."),
        ("You write a Triton kernel that fuses LayerNorm, Linear, and GELU",
         "Three CUDA kernels means three kernel launch overheads (~5&micro;s each), three HBM writes of intermediate tensors, three HBM reads of those intermediates by the next kernel, and three separate cuBLAS or cuDNN call paths with their own warmup overhead. <strong>Fusing</strong> LayerNorm + Linear + GELU into one Triton kernel collapses all of that: one launch, one HBM read of input, intermediates stay in registers and SRAM, one HBM write of output. For small batch and sequence sizes (where launch overhead and HBM bandwidth dominate compute time), fusion typically wins 2-3&times;. For large batches where compute dominates, the win shrinks but is still positive."),
        ("After running torch.compile(model), the first forward pass",
         "The 30-second first call is the JIT trace + compile. <code>torch.compile</code> dynamically captures the model's execution into an FX graph, lowers it through TorchInductor to a fused Triton/CUDA kernel set, and JIT-compiles to a binary. The cost is one-time per shape and dtype. After warmup, subsequent calls execute the optimized kernels directly. <code>fullgraph=True</code> forces the model to be a <em>single</em> captured graph and fails if there is any data-dependent control flow that <code>torch.compile</code> cannot trace. Use it when (a) you have eliminated data-dependent branches, (b) you want to AOT-export the graph for deployment, or (c) you need a guarantee of no Python-roundtrip during inference. Default mode (graph breaks allowed) is more permissive but slightly slower because it has to bounce back to Python at each break."),
    ],
    "part-10-frontiers/module-33-emerging-architectures/section-33.10.html": [
        ("You are working with satellite imagery time series",
         "Three tokenization strategies and their trade-offs: <strong>spatial patching</strong> (each 16&times;16 pixel patch = one token) preserves local visual structure and matches Vision Transformer pretraining, but sees no motion. <strong>Temporal patching</strong> (a sequence of full frames sampled at intervals, one token per frame) captures seasonal and motion patterns but loses spatial detail. <strong>3D tubelets</strong> (spatial patches &times; temporal stride) capture both at the cost of token count exploding quadratically with image size. For multi-year forecasting at coarse spatial resolution, 3D tubelets with aggressive downsampling typically win. For high-resolution change detection within a season, spatial patching with a separate temporal embedding wins."),
        ("A pharmaceutical company asks you to build a model that generates novel drug",
         "Both encode molecules as strings, but they make different validity guarantees. <strong>SMILES</strong> is the chemistry standard (<code>CCO</code> for ethanol). Generative models often produce invalid SMILES (mismatched parentheses, unfilled valences) that must be filtered out at decoding time, which wastes compute and biases RL fine-tuning. <strong>SELFIES</strong> is designed so that <em>every</em> string in the alphabet encodes a valid molecule; valence constraints are baked into the grammar. <strong>SMILES pros</strong>: more pretraining data exists, the format is human-readable to medicinal chemists, tokenizer tooling is mature. <strong>SELFIES pros</strong>: 100&percnt; validity rate at generation time (which is decisive for RL-based drug optimization), shorter chains on average for the same molecule. Most modern generative drug-design papers use SELFIES specifically because the validity-by-construction property eliminates the validation rejection step."),
        ("Why might BPE tokenization work better than single-nucleotide tokenization",
         "<strong>Single-nucleotide tokenization</strong> treats each A/C/G/T as a token. Maximum granularity, never collapses information, ideal for variant calling and any task where a single base change matters clinically. <strong>BPE tokenization</strong> merges frequently co-occurring nucleotides into shared tokens (common k-mers in coding regions become single tokens). BPE works <em>better</em> when the task involves recognizing motifs, regulatory elements, or codon-level patterns — fewer tokens means longer effective context, so the model can attend across longer genomic regions. BPE works <em>worse</em> when the task involves rare variants or single-nucleotide effects, because a BPE merge could mask a single-base difference that matters. The choice mirrors the language-vs-character debate in NLP: granularity vs context length is a real trade-off, and the right answer is task-dependent."),
    ],
}


def main() -> int:
    total = 0
    files_touched = 0
    for rel_path, answer_list in ANSWERS.items():
        p = ROOT / rel_path
        if not p.exists():
            print(f"  MISSING {rel_path}")
            continue
        text = p.read_text(encoding="utf-8")
        original = text
        applied_here = 0
        for marker, answer in answer_list:
            # Find the question's text in the file
            qpos = text.find(marker)
            if qpos == -1:
                print(f"  WARN {rel_path}: marker {marker!r} not found")
                continue
            # Find the placeholder that follows (within the next ~1000 chars)
            ph_pos = text.find(PLACEHOLDER, qpos)
            if ph_pos == -1 or ph_pos - qpos > 2000:
                print(f"  WARN {rel_path}: placeholder not found after marker")
                continue
            text = text[:ph_pos] + answer + text[ph_pos + len(PLACEHOLDER):]
            applied_here += 1
        if text != original:
            p.write_text(text, encoding="utf-8")
            print(f"  {rel_path}: {applied_here}/{len(answer_list)} answers filled")
            files_touched += 1
            total += applied_here
    print()
    print(f"TOTAL: {total} answers filled across {files_touched} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
