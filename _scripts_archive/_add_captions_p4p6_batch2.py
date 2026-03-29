"""Add captions to remaining uncaptioned <pre> code blocks in Parts 4-6 (batch 2)."""
import re
import os

CAPTIONS = {
    "part-4-training-adapting/module-13-synthetic-data/section-13.2.html": [
        # Block 5: pip install
        "This command installs openai, rouge-score, pandas, and tqdm, which provide the LLM API client, text similarity scoring, tabular data handling, and progress bars needed for the Self-Instruct lab.",
        # Block 6: Step 1 seed instructions
        "This lab step defines seed instruction examples containing instruction, input, and output fields for tasks like sentiment classification and summarization. The seed pool bootstraps the Self-Instruct pipeline by providing diverse exemplars the LLM uses to generate new instructions.",
        # Block 7: Step 2 generate_new_instruction
        "This lab step implements generate_new_instruction, which samples n_examples from the seed pool, constructs a few-shot prompt, and calls gpt-4o-mini with temperature=0.9 to produce a novel instruction/input/output triple. The high temperature encourages diverse task generation beyond the seed distribution.",
        # Block 8: Step 3 ROUGE dedup
        "This lab step implements ROUGE-L based deduplication using rouge_scorer.RougeScorer. The is_duplicate function compares each new instruction against all existing ones, returning True if any pairwise ROUGE-L fmeasure exceeds the 0.7 threshold.",
        # Block 9: Step 4 generation loop
        "This lab step runs the Self-Instruct generation loop using run_self_instruct, which calls generate_new_instruction repeatedly, filters duplicates via is_duplicate, and grows the pool until target_count is reached or max_attempts is exhausted. The tqdm progress bar tracks successful additions versus total attempts.",
        # Block 10: Step 5 quality filter and export
        "This lab step applies a quality_filter that rejects examples with short instructions or outputs beginning with refusal phrases, then converts passing examples to ChatML format via to_chatml and writes them as JSONL. The output file contains one JSON object per line with system/user/assistant message arrays.",
        # Block 11: complete solution
        "This complete solution combines seed instructions, the generate_new_instruction function, ROUGE deduplication, the generation loop, quality filtering, and JSONL export into a single script. It reproduces the full Self-Instruct pipeline from seed definitions through synthetic dataset creation.",
    ],
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.3.html": [
        # Block 5: pip install
        "This command installs transformers, trl, datasets, accelerate, torch, and matplotlib for the SFT training lab. The matplotlib package enables loss curve visualization in Step 4.",
        # Block 6: Step 1 load model
        "This lab step loads SmolLM2-135M-Instruct with AutoModelForCausalLM in float16 precision and captures a baseline response using apply_chat_template. Saving the base model output before training enables a side-by-side comparison after fine-tuning.",
        # Block 7: Step 2 prepare dataset
        "This lab step loads 500 shuffled examples from the HuggingFaceH4/no_robots instruction dataset and defines a format_chat function that applies the tokenizer's chat template. The formatted text column is used as input to SFTTrainer in the next step.",
        # Block 8: Step 3 SFT training
        "This lab step configures SFTConfig with per_device_train_batch_size=4, gradient_accumulation_steps=2, and num_train_epochs=3, then launches training with SFTTrainer. The TODO comments prompt students to fill in learning_rate, logging_steps, and max_seq_length before running.",
        # Block 9: Step 4 plot loss
        "This lab step extracts per-step loss values from trainer.state.log_history, filters entries containing a 'loss' key, and plots the training curve with matplotlib. The saved sft_loss_curve.png file and final loss printout confirm whether training converged.",
        # Block 10: Step 5 compare outputs
        "This lab step generates responses from the fine-tuned model on three test prompts using model.generate with temperature=0.7 and max_new_tokens=200. Comparing these outputs with the baseline captured in Step 1 reveals improvements in instruction following and response structure.",
        # Block 11: complete solution
        "This complete solution combines model loading, baseline capture, dataset preparation, SFT training with SFTConfig, loss curve plotting, and post-training generation into a single script. It reproduces the full supervised fine-tuning workflow on SmolLM2-135M-Instruct.",
    ],
    "part-4-training-adapting/module-16-distillation-merging/section-16.1.html": [
        # Block 5: pip install
        "This command installs transformers, torch, datasets, and tqdm for the knowledge distillation lab. These packages provide model loading, tensor operations, training data, and progress tracking.",
        # Block 6: Step 1 load teacher and student
        "This lab step loads gpt2-medium as the frozen teacher and distilgpt2 as the trainable student, sharing the same GPT-2 tokenizer. The parameter count comparison shows the teacher-to-student compression ratio (approximately 4x), establishing the efficiency target for distillation.",
        # Block 7: Step 2 distillation loss
        "This lab step implements distillation_loss, which combines KL divergence on temperature-scaled soft targets with cross-entropy on hard labels. The alpha parameter balances the two terms, and the T-squared factor on the KL term keeps gradient magnitudes stable across temperature settings.",
        # Block 8: Step 3 training loop
        "This lab step runs the distillation training loop over 2 epochs on 2000 wikitext-2 examples. Each batch passes through both teacher (with torch.no_grad) and student, computes the combined distillation_loss, and updates only the student's parameters via AdamW at lr=5e-5.",
        # Block 9: Step 4 evaluate perplexity
        "This lab step defines compute_perplexity using cross-entropy loss over the validation set, then compares perplexity for the teacher, original student, and distilled student. The expected result is a 10-20% perplexity improvement in the distilled student while maintaining 4x fewer parameters than the teacher.",
        # Block 10: complete solution
        "This complete solution combines teacher/student loading, the distillation_loss function, the training loop, and perplexity evaluation into a single script. It reproduces the full knowledge distillation pipeline from model setup through quantitative evaluation on wikitext-2.",
    ],
    "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.2.html": [
        # Block 6: pip install
        "This command installs transformers, trl, datasets, peft, accelerate, and torch for the DPO alignment lab. The trl library provides DPOTrainer and DPOConfig, while peft enables LoRA-based parameter-efficient training.",
        # Block 7: Step 1 load preference dataset
        "This lab step loads 500 examples from the trl-lib/ultrafeedback_binarized preference dataset, which contains prompt/chosen/rejected triples. The printout shows the column structure and previews the first example's prompt, preferred response, and rejected response.",
        # Block 8: Step 2 DPO loss from scratch
        "This lab step implements compute_log_probs (sum of per-token log probabilities using F.log_softmax and gather) and the core dpo_loss function. The DPO loss is -log_sigmoid(beta * (log_ratio_chosen - log_ratio_rejected)), rewarding the policy for preferring chosen over rejected responses more than the reference does.",
        # Block 9: Step 3 DPO training with TRL
        "This lab step trains SmolLM2-135M-Instruct with DPOTrainer using LoRA (r=16, alpha=32) and DPOConfig set to beta=0.1, learning_rate=5e-5, and max_length=512. The trainer automatically creates an internal reference model copy for computing the KL-constrained policy gradient.",
        # Block 10: Step 4 evaluate alignment
        "This lab step evaluates preference accuracy on 20 test examples by computing log probabilities for both chosen and rejected responses under the trained policy. The metric reports the fraction where the model assigns higher probability to the chosen response, with 60-70% expected versus the 50% random baseline.",
        # Block 11: complete solution
        "This complete solution combines dataset loading, the from-scratch DPO loss, DPOTrainer with LoRA configuration, and preference accuracy evaluation into a single script. It reproduces the full DPO alignment pipeline from data preparation through quantitative evaluation on ultrafeedback_binarized.",
    ],
    "part-5-retrieval-conversation/module-20-rag/section-20.2.html": [
        # Block 5: pip install
        "This command installs sentence-transformers, openai, and numpy for the advanced retrieval lab. These packages provide bi-encoder and cross-encoder models, the LLM API for query expansion, and numerical operations for similarity computation.",
        # Block 6: Step 1 baseline retrieval
        "This lab step builds a baseline bi-encoder retrieval system using all-MiniLM-L6-v2 on a 12-document Python knowledge corpus. The baseline_search function computes cosine similarity with pre-computed norms and returns the top_k most similar documents, establishing the performance floor that expansion and reranking aim to beat.",
        # Block 7: Step 2 query expansion
        "This lab step implements LLM-powered query expansion via expand_query, which prompts gpt-4o-mini to generate n alternative phrasings. The expanded_search function runs baseline_search with each variant and merges results by keeping the highest score per document index, broadening recall beyond single-query limitations.",
        # Block 8: Step 3 cross-encoder reranking
        "This lab step adds a cross-encoder reranking stage using ms-marco-MiniLM-L-6-v2 from CrossEncoder. The rerank function creates (query, document) pairs, scores them jointly (more accurate than bi-encoder cosine similarity), and returns the top_k by cross-encoder score.",
        # Block 9: Step 4 measure improvement
        "This lab step evaluates all three approaches (baseline, expanded, reranked) on four queries with known relevant document indices using recall_at_k. The comparison shows progressive improvement from approximately 0.5 baseline recall to 0.7 with expansion and 0.8 with reranking added.",
        # Block 10: complete solution
        "This complete solution combines the bi-encoder baseline, LLM query expansion, cross-encoder reranking, and the recall@5 benchmark into a single script. It reproduces the full advanced retrieval pipeline on the Python knowledge corpus.",
    ],
    "part-5-retrieval-conversation/module-21-conversational-ai/section-21.3.html": [
        # Block 7: pip install
        "This command installs openai, sentence-transformers, and numpy for the multi-layer memory chatbot lab. These packages provide the LLM API for summarization and chat, embedding models for long-term memory search, and numerical similarity computation.",
        # Block 8: Step 1 short-term memory
        "This lab step implements a ShortTermMemory class with a sliding window of max_turns messages. When the buffer overflows, evicted messages are collected in an overflow list for downstream summarization, and get_overflow returns and clears them.",
        # Block 9: Step 2 conversation summarizer
        "This lab step builds a Summarizer class that maintains a running_summary string and progressively incorporates new evicted messages via an LLM call. The prompt includes the current summary and new turns, asking gpt-4o-mini to produce an updated 2-4 sentence summary at temperature=0.3.",
        # Block 10: Step 3 long-term vector memory
        "This lab step implements a LongTermMemory class that uses an LLM to extract factual statements from conversation turns, encodes them with SentenceTransformer all-MiniLM-L6-v2, and stores them for cosine-similarity retrieval. The search method returns facts above a 0.3 similarity threshold.",
        # Block 11: Step 4 memory-augmented chatbot
        "This lab step wires all three memory layers into a MemoryChat class. The chat method searches LongTermMemory for relevant facts, builds a system prompt with the running summary and facts, generates a response, updates ShortTermMemory, and processes any overflow through the Summarizer and LongTermMemory extraction pipeline.",
        # Block 12: complete solution
        "This complete solution combines ShortTermMemory, Summarizer, LongTermMemory, and MemoryChat into a single script that runs a 7-turn conversation with user Bob. It demonstrates memory overflow handling, progressive summarization, fact extraction, and recall of previously mentioned details like employer and project.",
    ],
    "part-6-agentic-ai/module-22-ai-agents/section-22.5.html": [
        # Block 2: pip install
        "This command installs swebench, openai, tiktoken, and pandas for the SWE-bench evaluation lab. The swebench package provides the evaluation harness for running agents on real GitHub issue tasks.",
        # Block 3: Step 1 load tasks
        "This placeholder marks Step 1, where students configure the SWE-bench Lite harness by calling get_tasks to load 10 benchmark tasks from different repositories and setting up the agent with file read/write and test execution tools.",
        # Block 4: Step 2 run agent
        "This placeholder marks Step 2, where students loop over loaded tasks, run the agent on each, and record pass/fail outcomes, token usage, API cost, and tool call counts in a pandas DataFrame.",
        # Block 5: Step 3 categorize failures
        "This placeholder marks Step 3, where students analyze agent logs from failed tasks and classify each failure as misunderstanding the issue, producing incorrect code, or failing to navigate the repository structure.",
        # Block 6: Step 4 compare models
        "This placeholder marks Step 4, where students re-run the same tasks with a reasoning model and create a comparison table showing pass rates, cost, and efficiency differences between standard and reasoning variants.",
        # Block 7: complete solution
        "This solution outline describes the SWE-bench evaluation lab deliverables: a metrics table with per-task results, a failure categorization breakdown, and a model comparison. The lab focuses on measurement methodology rather than a single implementation script.",
    ],
    "part-6-agentic-ai/module-25-specialized-agents/section-25.1.html": [
        # Block 2: pip install
        "This command installs openai and subprocess32 for the self-debugging code agent lab. The openai package provides the LLM API, and subprocess32 offers an enhanced subprocess interface with timeout support.",
        # Block 3: Step 1 create agent with tools
        "This placeholder marks Step 1, where students define tool schemas for read_file, write_file, and run_command, then implement the agent loop that calls the LLM with tool definitions and executes tool results.",
        # Block 4: Step 2 self-debugging loop
        "This placeholder marks Step 2, where students implement retry logic with max_attempts=3 that feeds error tracebacks from failed test runs back into the next LLM prompt for self-correction.",
        # Block 5: Step 3 coding challenges
        "This placeholder marks Step 3, where students define 5 coding challenges (string manipulation, data structures, file parsing, API client, math) with test cases and run the agent on each.",
        # Block 6: Step 4 metrics and graceful failure
        "This placeholder marks Step 4, where students track success rate, attempts per task, and token cost in a DataFrame, and implement a give-up path that produces an explanation when the agent cannot solve a problem after 3 attempts.",
        # Block 7: complete solution
        "This solution outline lists the key components of the self-debugging code agent: tool definitions (read_file, write_file, run_command), the agent loop with LLM tool calling, retry logic with error context, and metrics collection in a pandas DataFrame.",
    ],
    "part-6-agentic-ai/module-25-specialized-agents/section-25.2.html": [
        # Block 2: pip install
        "This command installs playwright and openai, then runs playwright install chromium to download the browser binary. These provide headless browser automation and the LLM API for the browser agent lab.",
        # Block 3: Step 1 Playwright MCP setup
        "This placeholder marks Step 1, where students initialize a Playwright browser instance and define MCP tool schemas for navigate(url), click(selector), type(selector, text), and screenshot() actions.",
        # Block 4: Step 2 navigation and extraction
        "This placeholder marks Step 2, where students implement a multi-step web navigation task that searches for a product, clicks through results, and extracts structured data (name, price, rating) from the page.",
        # Block 5: Step 3 error handling
        "This placeholder marks Step 3, where students add try/except blocks around tool calls with wait-and-retry logic to handle cookie banners, modal dialogs, and timeout errors during browser interactions.",
        # Block 6: Step 4 screenshot verification
        "This placeholder marks Step 4, where students capture screenshots after each agent action and send them to a vision model to verify the action succeeded before proceeding to the next step.",
        # Block 7: complete solution
        "This solution outline lists the key components of the browser agent: Playwright browser setup, MCP tool definitions, the agent loop with tool calling and result parsing, error handling with retry and fallback, and screenshot-based verification using a vision model.",
    ],
}


def add_captions_to_file(filepath, captions):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pre_end_pattern = re.compile(r'</pre>')
    matches = list(pre_end_pattern.finditer(content))

    uncaptioned_positions = []
    for m in matches:
        end_pos = m.end()
        after = content[end_pos:end_pos + 200].strip()
        if not after.startswith('<div class="code-caption">'):
            uncaptioned_positions.append(end_pos)

    if len(uncaptioned_positions) != len(captions):
        print(f"  WARNING: {filepath} has {len(uncaptioned_positions)} uncaptioned blocks but {len(captions)} captions provided!")
        return False

    # Assign fragment numbers based on position among ALL pre blocks
    all_pre_matches = list(pre_end_pattern.finditer(content))
    fragment_num = 0
    assignments = {}
    for m in all_pre_matches:
        end_pos = m.end()
        after = content[end_pos:end_pos + 200].strip()
        fragment_num += 1
        if not after.startswith('<div class="code-caption">'):
            assignments[end_pos] = fragment_num

    # Insert captions in reverse order
    caption_idx = len(captions) - 1
    for pos in reversed(uncaptioned_positions):
        frag_num = assignments[pos]
        caption_html = f'\n<div class="code-caption"><strong>Code Fragment {frag_num}:</strong> {captions[caption_idx]}</div>'
        content = content[:pos] + caption_html + content[pos:]
        caption_idx -= 1

    # Renumber ALL captions sequentially
    counter = [0]
    def replacer(match):
        counter[0] += 1
        return f'<div class="code-caption"><strong>Code Fragment {counter[0]}:'
    content = re.sub(
        r'<div class="code-caption"><strong>Code Fragment \d+:',
        replacer,
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


base = "E:/Projects/LLMCourse"
total_added = 0
total_files = 0

for rel_path, captions in CAPTIONS.items():
    filepath = os.path.join(base, rel_path)
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        continue

    print(f"Processing {rel_path} ({len(captions)} captions)...")
    success = add_captions_to_file(filepath, captions)
    if success:
        total_added += len(captions)
        total_files += 1
        print(f"  Added {len(captions)} captions")
    else:
        print(f"  SKIPPED due to mismatch")

print(f"\nDone: {total_added} captions added across {total_files} files")
