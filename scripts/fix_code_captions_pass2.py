#!/usr/bin/env python3
"""
fix_code_captions_pass2.py

Second pass: handles the remaining manual review cases from pass 1.
Each fix is hand-crafted based on inspecting the actual file content.
"""

import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_file(rel_path):
    full = os.path.join(BASE_DIR, rel_path.replace("\\", "/"))
    with open(full, "r", encoding="utf-8") as f:
        return f.readlines()


def write_file(rel_path, lines):
    full = os.path.join(BASE_DIR, rel_path.replace("\\", "/"))
    with open(full, "w", encoding="utf-8") as f:
        f.writelines(lines)


def find_line_containing(lines, text, start=0):
    """Find 0-indexed line containing text, starting from start."""
    for i in range(start, len(lines)):
        if text in lines[i]:
            return i
    return -1


def find_closing_pre(lines, start_idx):
    """Find 0-indexed line containing </code></pre> from start_idx."""
    for i in range(start_idx, len(lines)):
        if "</code></pre>" in lines[i]:
            return i
    return -1


def insert_caption_after_pre(lines, pre_close_idx, caption_html):
    """Insert a caption line after the </code></pre> line."""
    lines.insert(pre_close_idx + 1, caption_html + "\n")


def extract_first_comment(lines, pre_start_idx):
    """Extract first comment from a code block."""
    for i in range(pre_start_idx, min(len(lines), pre_start_idx + 20)):
        stripped = lines[i].strip()
        if stripped.startswith("#") and not stripped.startswith("#!"):
            return stripped.lstrip("#").strip()
    return None


fixes_applied = []
fixes_skipped = []


def apply_fix(filepath, description, func):
    try:
        lines = read_file(filepath)
        result = func(lines)
        if result is not None:
            write_file(filepath, result)
            fixes_applied.append((filepath, description))
        else:
            fixes_skipped.append((filepath, description, "No change needed or could not apply"))
    except Exception as e:
        fixes_skipped.append((filepath, description, str(e)))


# ============================================================
# TYPE 1 FIXES: "Block2 needs a new caption after X"
# These files already had block1's caption moved by pass 1.
# Block2 just needs a new caption inserted after its </pre>.
# ============================================================

def fix_block2_caption(filepath, block2_comment_prefix, new_caption_label, new_caption_text):
    """
    Find block2 by its first comment line, find its closing </pre>,
    and insert a new caption after it.
    """
    def do_fix(lines):
        # Find the block2 start by its comment
        idx = find_line_containing(lines, block2_comment_prefix)
        if idx == -1:
            return None
        close = find_closing_pre(lines, idx)
        if close == -1:
            return None
        # Check if there's already a caption right after
        next_line = lines[close + 1].strip() if close + 1 < len(lines) else ""
        if "code-caption" in next_line:
            return None  # already has caption
        caption = f'<div class="code-caption"><strong>{new_caption_label}:</strong> {new_caption_text}</div>'
        insert_caption_after_pre(lines, close, caption)
        return lines
    apply_fix(filepath, f"Add caption '{new_caption_label}' for block2", do_fix)


# section-6.6: block2 is FSDP training
fix_block2_caption(
    r"part-2-understanding-llms\module-06-pretraining-scaling-laws\section-6.6.html",
    "# FSDP training with PyTorch",
    "Code Fragment 6.6.2",
    "FSDP training with PyTorch. FSDP shards model parameters, gradients, and optimizer states across GPUs, so each device stores only a fraction of the full model."
)

# section-6.7: block2 is task vector extraction
fix_block2_caption(
    r"part-2-understanding-llms\module-06-pretraining-scaling-laws\section-6.7.html",
    "# Conceptual demonstration of task vector extraction",
    "Code Fragment 6.7.2",
    "Conceptual demonstration of task vector extraction. The function computes the difference in model activations between a few-shot prompt and a zero-shot prompt to isolate the task-specific signal."
)

# section-4.4: block2 is FlashAttention pseudocode (algo-line-keyword)
def fix_4_4(lines):
    # Find the second block (the algorithm block with algo-line-keyword after the Code Fragment 4.4.1 caption)
    cap_idx = find_line_containing(lines, "Code Fragment 4.4.1")
    if cap_idx == -1:
        return None
    # Find the next <pre><code after this caption
    next_pre = find_line_containing(lines, "<pre><code", cap_idx + 1)
    if next_pre == -1:
        return None
    close = find_closing_pre(lines, next_pre)
    if close == -1:
        return None
    # Check if already has caption
    next_line = lines[close + 1].strip() if close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None
    caption = '<div class="code-caption"><strong>Pseudocode 4.4.2:</strong> FlashAttention tiling algorithm. Q, K, and V blocks are loaded from HBM into SRAM, attention is computed per tile, and running statistics track the online softmax normalization.</div>'
    insert_caption_after_pre(lines, close, caption)
    return lines

apply_fix(
    r"part-1-foundations\module-04-transformer-architecture\section-4.4.html",
    "Add Pseudocode 4.4.2 caption for FlashAttention tiling block",
    fix_4_4
)

# section-a.1: block2 is matrix multiplication in NumPy
fix_block2_caption(
    r"appendices\appendix-a-mathematical-foundations\section-a.1.html",
    "# Matrix multiplication in NumPy",
    "Code Fragment A.1.2",
    "Matrix multiplication in NumPy. The <code>@</code> operator computes the dot product of a batch of token vectors with a weight matrix, the core operation inside every feedforward layer."
)

# section-c.1: block2 is NumPy computation
fix_block2_caption(
    r"appendices\appendix-c-python-for-llm\section-c.1.html",
    "# NumPy computation",
    "Code Fragment C.1.2",
    "NumPy computation basics. Array operations on numeric data demonstrate the vectorized style used throughout scientific Python and ML preprocessing."
)

# section-c.2: block2 is uv install
fix_block2_caption(
    r"appendices\appendix-c-python-for-llm\section-c.2.html",
    "# Install uv",
    "Code Fragment C.2.2",
    "Using <code>uv</code> as a faster alternative to pip and venv. The <code>uv</code> tool handles virtual environment creation and package installation in a single step with significantly faster dependency resolution."
)

# section-d.2: block2 is verify CUDA installation
fix_block2_caption(
    r"appendices\appendix-d-environment-setup\section-d.2.html",
    "# Verify CUDA installation",
    "Code Fragment D.2.2",
    "Verifying the CUDA installation. The <code>nvcc</code> compiler reports the toolkit version while PyTorch's <code>cuda.is_available()</code> confirms the driver and runtime are correctly linked."
)

# section-d.3: block2 is venv alternative
fix_block2_caption(
    r"appendices\appendix-d-environment-setup\section-d.3.html",
    "# Requires system Python 3.10+",
    "Code Fragment D.3.2",
    "Creating a virtual environment with Python's built-in <code>venv</code> module. This approach requires a system-level CUDA toolkit installation and is lighter weight than Conda but less portable."
)

# section-e.1: block2 is Git LFS
fix_block2_caption(
    r"appendices\appendix-e-git-collaboration\section-e.1.html",
    "# Install Git LFS",
    "Code Fragment E.1.2",
    "Setting up Git LFS (Large File Storage) for model weights and datasets. LFS stores large binary files on a separate server while Git tracks lightweight pointer files."
)

# section-e.2: block2 is DVC pipeline yaml
fix_block2_caption(
    r"appendices\appendix-e-git-collaboration\section-e.2.html",
    "# Example dvc.yaml pipeline",
    "Code Fragment E.2.2",
    "A DVC pipeline definition in <code>dvc.yaml</code>. Each stage declares its dependencies, command, and outputs, enabling reproducible, cached execution of multi-step ML workflows."
)

# section-i.8: block2 is Reasoning Analysis template
fix_block2_caption(
    r"appendices\appendix-i-prompt-templates\section-i.8.html",
    "// Reasoning Analysis user template",
    "Code Fragment I.8.2",
    "An analysis prompt for reasoning models. Instead of a direct question, it asks the model to examine a subject from multiple angles, producing structured output with key findings, implications, and confidence levels."
)


# ============================================================
# TYPE 1 FIXES: "Could not determine fix automatically"
# ============================================================

# section-4.2: Two parts of a single multi-part code file.
# Block1 is imports/config, Block2 is training loop. They share caption "Code Fragment 4.2.2".
# These are logically one code file split for explanation. Keep together with single caption.
# But each section needs its own caption. Block1 = model definition, block2 = training loop.
def fix_4_2(lines):
    # Find "mini_transformer.py" in block1
    b1_idx = find_line_containing(lines, "mini_transformer.py")
    if b1_idx == -1:
        return None
    # Find the first </code></pre> after it
    b1_close = find_closing_pre(lines, b1_idx)
    if b1_close == -1:
        return None
    # Check if already has a caption
    next_line = lines[b1_close + 1].strip() if b1_close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None
    caption = '<div class="code-caption"><strong>Code Fragment 4.2.1:</strong> Model definition: imports, configuration dataclass, and the decoder-only Transformer architecture including multi-head causal self-attention, feedforward layers, and positional embeddings.</div>'
    insert_caption_after_pre(lines, b1_close, caption)
    return lines

apply_fix(
    r"part-1-foundations\module-04-transformer-architecture\section-4.2.html",
    "Add Code Fragment 4.2.1 for block1 (model definition)",
    fix_4_2
)

# section-8.3: Two pseudocode blocks in an algorithm callout (RLVR + GRPO).
# Block1 is the RLVR loop, Block2 is GRPO. They share "Pseudocode 8.3.4".
# The caption text matches block1 (RLVR). Block2 needs its own caption.
def fix_8_3(lines):
    # Find the second pseudocode block (GRPO) by its Input line
    idx = find_line_containing(lines, "problem p, policy pi, reference policy pi_ref, group size G")
    if idx == -1:
        return None
    # Go backward to find the <pre><code
    pre_idx = idx
    for i in range(idx, max(0, idx - 5), -1):
        if "<pre><code" in lines[i]:
            pre_idx = i
            break
    close = find_closing_pre(lines, pre_idx)
    if close == -1:
        return None
    next_line = lines[close + 1].strip() if close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None
    caption = '<div class="code-caption"><strong>Pseudocode 8.3.5:</strong> Group Relative Policy Optimization (GRPO). Instead of a separate critic, GRPO normalizes rewards within a group of G sampled solutions. The clipped ratio and KL penalty stabilize training without the memory cost of a value network.</div>'
    insert_caption_after_pre(lines, close, caption)
    return lines

apply_fix(
    r"part-2-understanding-llms\module-08-reasoning-test-time-compute\section-8.3.html",
    "Add Pseudocode 8.3.5 for GRPO block",
    fix_8_3
)

# section-d.4: Two install blocks (core + vllm). Move caption after block1, add caption for block2.
def fix_d_4(lines):
    # Find block1 (Core Hugging Face)
    b1_idx = find_line_containing(lines, "# Core Hugging Face ecosystem")
    if b1_idx == -1:
        return None
    b1_close = find_closing_pre(lines, b1_idx)
    if b1_close == -1:
        return None

    # Check if block1 already has a caption
    next_after_b1 = lines[b1_close + 1].strip() if b1_close + 1 < len(lines) else ""
    if "code-caption" in next_after_b1:
        return None  # already fixed

    # Find block2 (Install vLLM)
    b2_idx = find_line_containing(lines, "# Install vLLM")
    if b2_idx == -1:
        return None
    b2_close = find_closing_pre(lines, b2_idx)
    if b2_close == -1:
        return None

    # Find the shared caption
    cap_idx = find_line_containing(lines, "Code Fragment D.4.1")
    if cap_idx == -1:
        return None

    # Remove shared caption
    removed = lines.pop(cap_idx)

    # Recalculate indices after removal
    if b1_close >= cap_idx:
        b1_close -= 1
    if b2_close >= cap_idx:
        b2_close -= 1

    # Insert caption after block1
    cap1 = '<div class="code-caption"><strong>Code Fragment D.4.1:</strong> Installing the core library stack for LLM development: Hugging Face Transformers, fine-tuning tools (peft, trl), experiment tracking (wandb, mlflow), and data processing utilities.</div>'
    lines.insert(b1_close + 1, cap1 + "\n")

    # Recalculate b2_close
    b2_close += 1  # shifted by insertion

    # Insert caption after block2
    cap2 = '<div class="code-caption"><strong>Code Fragment D.4.2:</strong> Installing and launching vLLM as a local OpenAI-compatible inference server. The server exposes the same API as OpenAI, allowing existing client code to work with local models.</div>'
    b2_close_new = find_closing_pre(lines, find_line_containing(lines, "# Install vLLM"))
    lines.insert(b2_close_new + 1, cap2 + "\n")

    return lines

apply_fix(
    r"appendices\appendix-d-environment-setup\section-d.4.html",
    "Split caption D.4.1, add D.4.2 for vLLM block",
    fix_d_4
)

# section-i.5: Four blocks (code-gen system, code-gen user, code-review system, code-review user).
# Currently one caption for all four. Split: blocks 1+2 get I.5.1, blocks 3+4 get I.5.2.
def fix_i_5(lines):
    # Find code-gen user block closing </pre>
    user_idx = find_line_containing(lines, "// Code Generation user template")
    if user_idx == -1:
        return None
    user_close = find_closing_pre(lines, user_idx)
    if user_close == -1:
        return None
    # Check if already has caption
    next_line = lines[user_close + 1].strip() if user_close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None

    # Find the shared caption and change it to I.5.2 for code review
    cap_idx = find_line_containing(lines, "Code Fragment I.5.1")
    if cap_idx == -1:
        return None

    # Replace I.5.1 with I.5.2 in the existing caption and update text
    lines[cap_idx] = '<div class="code-caption"><strong>Code Fragment I.5.2:</strong> A code review system prompt that structures feedback into categories (bugs, performance, style, security) with a corrected version. The user message wraps the code in fenced blocks for clear delimitation.</div>\n'

    # Insert I.5.1 caption after the code-gen user block
    cap1 = '<div class="code-caption"><strong>Code Fragment I.5.1:</strong> Instructs the model to generate code from a specification, including type hints, docstrings, and edge case handling for production quality. The user message supplies the function signature and requirements, giving the model a clear contract to implement.</div>'
    lines.insert(user_close + 1, cap1 + "\n")

    return lines

apply_fix(
    r"appendices\appendix-i-prompt-templates\section-i.5.html",
    "Split into I.5.1 (code gen) and I.5.2 (code review)",
    fix_i_5
)

# section-i.7: Three blocks (general assistant, domain expert, guardrailed bot).
# Caption I.7.1 only covers general assistant. Add I.7.2 for domain expert, I.7.3 for guardrailed.
def fix_i_7(lines):
    # Find domain expert block
    domain_idx = find_line_containing(lines, "// Domain Expert system template")
    if domain_idx == -1:
        return None

    # Go back to find its <pre><code
    pre_idx = domain_idx
    for i in range(domain_idx, max(0, domain_idx - 3), -1):
        if "<pre><code" in lines[i]:
            pre_idx = i
            break

    domain_close = find_closing_pre(lines, pre_idx)
    if domain_close == -1:
        return None

    # Check if already has caption
    next_line = lines[domain_close + 1].strip() if domain_close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None

    # Find guardrailed bot block
    guard_idx = find_line_containing(lines, "// Guardrailed Bot system template")
    if guard_idx == -1:
        return None
    guard_close = find_closing_pre(lines, guard_idx)
    if guard_close == -1:
        return None

    # First: insert caption after guardrailed bot (do bottom-up to preserve indices)
    cap3 = '<div class="code-caption"><strong>Code Fragment I.7.3:</strong> A guardrailed bot system prompt that restricts the model to approved topics and defines strict behavioral rules. The fallback contact ensures users can reach a human when the bot cannot help.</div>'

    # Find the existing shared caption
    cap_idx = find_line_containing(lines, "Code Fragment I.7.1")
    if cap_idx == -1:
        return None

    # Remove the old shared caption (which was after the last block)
    old_cap = lines.pop(cap_idx)

    # Recalculate indices after removal
    domain_close_new = find_closing_pre(lines, find_line_containing(lines, "// Domain Expert system template"))
    guard_close_new = find_closing_pre(lines, find_line_containing(lines, "// Guardrailed Bot system template"))

    # Find general assistant block close
    gen_idx = find_line_containing(lines, "// General Assistant system template")
    gen_close = find_closing_pre(lines, gen_idx)

    # Insert captions bottom-up
    lines.insert(guard_close_new + 1, cap3 + "\n")
    # Recalculate domain_close after insert
    domain_close_new2 = find_closing_pre(lines, find_line_containing(lines, "// Domain Expert system template"))
    cap2 = '<div class="code-caption"><strong>Code Fragment I.7.2:</strong> Configures the model as a domain expert with field-specific terminology, trade-off analysis, and clear expertise boundaries. Replace the placeholders with your domain details.</div>'
    lines.insert(domain_close_new2 + 1, cap2 + "\n")

    # Re-insert I.7.1 after general assistant block
    gen_close_new = find_closing_pre(lines, find_line_containing(lines, "// General Assistant system template"))
    cap1 = '<div class="code-caption"><strong>Code Fragment I.7.1:</strong> Sets behavioral guidelines for a general-purpose assistant, including tone, formatting preferences, and knowledge boundaries.</div>'
    lines.insert(gen_close_new + 1, cap1 + "\n")

    return lines

apply_fix(
    r"appendices\appendix-i-prompt-templates\section-i.7.html",
    "Split into I.7.1 (general), I.7.2 (domain expert), I.7.3 (guardrailed)",
    fix_i_7
)

# section-m.1: Three blocks (pip install, AgentState, WindowedState). Caption covers all.
# Block1 is pip install (no caption needed). Block2+3 share the caption.
# Fix: add caption after AgentState block (M.1.1), rename existing to M.1.2.
def fix_m_1(lines):
    # Find AgentState block
    agent_idx = find_line_containing(lines, "class AgentState(TypedDict):")
    if agent_idx == -1:
        return None
    agent_close = find_closing_pre(lines, agent_idx)
    if agent_close == -1:
        return None
    next_line = lines[agent_close + 1].strip() if agent_close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None

    # Insert caption after AgentState block
    cap1 = '<div class="code-caption"><strong>Code Fragment M.1.1:</strong> Installing LangGraph and defining agent state with <code>TypedDict</code>. The <code>add_messages</code> reducer appends new messages to the list rather than overwriting it.</div>'
    lines.insert(agent_close + 1, cap1 + "\n")

    # Find and update existing caption to M.1.2
    cap_idx = find_line_containing(lines, "Code Fragment M.1.1:", agent_close + 2)
    if cap_idx != -1:
        lines[cap_idx] = '<div class="code-caption"><strong>Code Fragment M.1.2:</strong> A custom reducer that implements a sliding window over events. Unlike <code>add_messages</code>, this reducer trims the list to the last <em>n</em> entries after each append.</div>\n'

    return lines

apply_fix(
    r"appendices\appendix-m-langgraph\section-m.1.html",
    "Split M.1.1 into M.1.1 (AgentState) and M.1.2 (WindowedState)",
    fix_m_1
)

# section-m.2: Three blocks (routing graph, conditional edges snippet, tool agent).
# Block1 is a routing graph, block2 is conditional_edges snippet, block3 is tool agent.
# The caption is for M.2.1. Fix: caption after block2 (the conditional edges is a small snippet),
# then M.2.2 for the tool agent.
def fix_m_2(lines):
    # Find the tool agent block
    tool_idx = find_line_containing(lines, "from langgraph.prebuilt import ToolNode")
    if tool_idx == -1:
        return None
    # Go back to its <pre><code
    pre_idx = tool_idx
    for i in range(tool_idx, max(0, tool_idx - 3), -1):
        if "<pre><code" in lines[i]:
            pre_idx = i
            break
    # Check if there's a caption before this block (after the conditional_edges snippet)
    prev_close = -1
    for i in range(pre_idx - 1, max(0, pre_idx - 5), -1):
        if "</code></pre>" in lines[i]:
            prev_close = i
            break
    if prev_close >= 0:
        next_line = lines[prev_close + 1].strip()
        if "code-caption" not in next_line and "<pre><code" not in next_line:
            # No caption between the conditional_edges snippet and the tool agent block
            pass
    # Find tool agent close
    tool_close = find_closing_pre(lines, pre_idx)
    if tool_close == -1:
        return None

    # Find existing caption
    cap_idx = find_line_containing(lines, "Code Fragment M.2.1")
    if cap_idx == -1:
        return None

    # The existing caption text already talks about conditional routing (matches blocks 1+2).
    # Add M.2.2 after the tool agent block for the ReAct agent pattern.
    next_after_tool = lines[tool_close + 1].strip() if tool_close + 1 < len(lines) else ""
    if "code-caption" in next_after_tool:
        return None  # already has caption

    cap2 = '<div class="code-caption"><strong>Code Fragment M.2.2:</strong> A ReAct-style tool-calling agent. The cyclic graph alternates between the LLM node (which may emit tool calls) and the <code>ToolNode</code> (which executes them), looping until the LLM produces a final response.</div>'
    lines.insert(tool_close + 1, cap2 + "\n")
    return lines

apply_fix(
    r"appendices\appendix-m-langgraph\section-m.2.html",
    "Add M.2.2 caption for ReAct tool agent block",
    fix_m_2
)

# section-m.3: Three blocks (graph definition, invocation, interrupt_after snippet).
# Caption M.3.1 covers all. Fix: add caption after block1 (M.3.1), rename existing for block2+3.
def fix_m_3(lines):
    # The graph definition block ends before the invocation block
    invoke_idx = find_line_containing(lines, 'thread_config = {"configurable"')
    if invoke_idx == -1:
        return None
    # Find the <pre><code before invoke_idx
    for i in range(invoke_idx, max(0, invoke_idx - 3), -1):
        if "<pre><code" in lines[i]:
            invoke_pre = i
            break
    else:
        return None
    invoke_close = find_closing_pre(lines, invoke_pre)

    # Find interrupt_after block
    after_idx = find_line_containing(lines, "interrupt_after=")
    if after_idx == -1:
        return None
    after_close = find_closing_pre(lines, after_idx)

    # Find existing caption
    cap_idx = find_line_containing(lines, "Code Fragment M.3.1")
    if cap_idx == -1:
        return None

    # Check if invocation block already has caption
    next_after_invoke = lines[invoke_close + 1].strip() if invoke_close + 1 < len(lines) else ""
    if "code-caption" in next_after_invoke:
        return None

    # Update existing caption to cover the interrupt_after snippet
    lines[cap_idx] = '<div class="code-caption"><strong>Code Fragment M.3.3:</strong> Using <code>interrupt_after</code> instead. Execution completes the <code>draft</code> node and then pauses, giving you the draft output to inspect before the next node runs.</div>\n'

    # Insert caption after invocation block (M.3.2)
    cap2 = '<div class="code-caption"><strong>Code Fragment M.3.2:</strong> Invoking a graph with an interrupt. The first call pauses before the <code>send</code> node. After inspecting the draft, calling <code>invoke(None)</code> resumes execution from the checkpoint.</div>'
    lines.insert(invoke_close + 1, cap2 + "\n")

    # Recalculate: find the graph definition closing pre (before invoke block)
    # The graph definition is the first <pre><code in section 2
    h2_idx = find_line_containing(lines, "interrupt_before</code></h2>")
    if h2_idx == -1:
        h2_idx = find_line_containing(lines, "Using <code>interrupt_before")
    if h2_idx == -1:
        return lines  # partial fix
    first_pre = find_line_containing(lines, "<pre><code", h2_idx)
    if first_pre == -1:
        return lines
    first_close = find_closing_pre(lines, first_pre)
    next_after_first = lines[first_close + 1].strip() if first_close + 1 < len(lines) else ""
    if "code-caption" not in next_after_first:
        cap1 = '<div class="code-caption"><strong>Code Fragment M.3.1:</strong> Compiling a graph with <code>interrupt_before=["send"]</code>. The graph pauses after the <code>draft</code> node completes and before <code>send</code> begins, giving a human the chance to review the draft.</div>'
        lines.insert(first_close + 1, cap1 + "\n")

    return lines

apply_fix(
    r"appendices\appendix-m-langgraph\section-m.3.html",
    "Split M.3.1 into M.3.1/M.3.2/M.3.3 for graph def, invocation, and interrupt_after",
    fix_m_3
)

# section-m.4: Three blocks (MemorySaver, SqliteSaver, AsyncSqliteSaver).
# Caption M.4.1 covers all. Fix: add captions after each.
def fix_m_4(lines):
    # Find SqliteSaver block
    sqlite_idx = find_line_containing(lines, "from langgraph.checkpoint.sqlite import SqliteSaver")
    if sqlite_idx == -1:
        return None
    sqlite_close = find_closing_pre(lines, sqlite_idx)
    if sqlite_close == -1:
        return None

    # Find AsyncSqliteSaver block
    async_idx = find_line_containing(lines, "from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver")
    if async_idx == -1:
        return None
    async_close = find_closing_pre(lines, async_idx)

    # Find existing caption
    cap_idx = find_line_containing(lines, "Code Fragment M.4.1")
    if cap_idx == -1:
        return None

    # Update existing caption to M.4.3 for async
    lines[cap_idx] = '<div class="code-caption"><strong>Code Fragment M.4.3:</strong> Async checkpointing with <code>AsyncSqliteSaver</code>. The async context manager and <code>ainvoke</code> call allow non-blocking I/O in async applications.</div>\n'

    # Insert M.4.2 after SqliteSaver block
    cap2 = '<div class="code-caption"><strong>Code Fragment M.4.2:</strong> Persistent checkpointing with <code>SqliteSaver</code>. State survives process restarts because checkpoints are written to a local database file. Reopen the same file to resume any thread.</div>'
    lines.insert(sqlite_close + 1, cap2 + "\n")

    # Recalculate MemorySaver block close (first block)
    mem_idx = find_line_containing(lines, "from langgraph.checkpoint.memory import MemorySaver")
    if mem_idx == -1:
        return lines
    mem_close = find_closing_pre(lines, mem_idx)
    next_after_mem = lines[mem_close + 1].strip() if mem_close + 1 < len(lines) else ""
    if "code-caption" not in next_after_mem and "code-output" not in next_after_mem:
        cap1 = '<div class="code-caption"><strong>Code Fragment M.4.1:</strong> Using <code>MemorySaver</code> for in-memory checkpointing. Each <code>thread_id</code> maintains an independent state history. This backend is fast but loses all data when the process exits.</div>'
        lines.insert(mem_close + 1, cap1 + "\n")

    return lines

apply_fix(
    r"appendices\appendix-m-langgraph\section-m.4.html",
    "Split M.4.1 into M.4.1/M.4.2/M.4.3",
    fix_m_4
)

# section-m.5: Three blocks (subgraphs def, parent graph, prebuilt agents).
# Caption M.5.2 covers all. Fix: add captions per block.
def fix_m_5(lines):
    # Find parent graph block
    parent_idx = find_line_containing(lines, "# --- Parent graph ---")
    if parent_idx == -1:
        return None
    parent_close = find_closing_pre(lines, parent_idx)

    # Find prebuilt agents block
    prebuilt_idx = find_line_containing(lines, "from langgraph.prebuilt import create_react_agent")
    if prebuilt_idx == -1:
        return None
    prebuilt_close = find_closing_pre(lines, prebuilt_idx)

    # Find existing caption
    cap_idx = find_line_containing(lines, "Code Fragment M.5.2")
    if cap_idx == -1:
        return None

    # Update existing to M.5.3 for prebuilt agents
    lines[cap_idx] = '<div class="code-caption"><strong>Code Fragment M.5.3:</strong> Using <code>create_react_agent</code> to build specialized agents with one line each, then composing them as subgraph nodes in a parent graph.</div>\n'

    # Insert M.5.2 after parent graph block
    cap2 = '<div class="code-caption"><strong>Code Fragment M.5.2:</strong> Composing the research and writing subgraphs into a parent graph. The <code>research_notes</code> channel flows from the research subgraph to the writing subgraph through the shared parent state.</div>'
    lines.insert(parent_close + 1, cap2 + "\n")

    # Insert M.5.1 after subgraphs def block (first block)
    sub_idx = find_line_containing(lines, "# Shared state type")
    if sub_idx == -1:
        sub_idx = find_line_containing(lines, "class TeamState(TypedDict)")
    if sub_idx == -1:
        return lines
    # Go back to <pre><code
    for i in range(sub_idx, max(0, sub_idx - 5), -1):
        if "<pre><code" in lines[i]:
            sub_pre = i
            break
    else:
        return lines
    sub_close = find_closing_pre(lines, sub_pre)
    next_line = lines[sub_close + 1].strip() if sub_close + 1 < len(lines) else ""
    if "code-caption" not in next_line:
        cap1 = '<div class="code-caption"><strong>Code Fragment M.5.1:</strong> Defining two independent subgraphs: a research agent that gathers sources and a writing agent that drafts an article. Each subgraph is compiled separately for independent testing.</div>'
        lines.insert(sub_close + 1, cap1 + "\n")

    return lines

apply_fix(
    r"appendices\appendix-m-langgraph\section-m.5.html",
    "Split into M.5.1/M.5.2/M.5.3",
    fix_m_5
)

# section-t.1: Issue [32] and [33] from the report.
# Three code blocks share T.1.1: SparkSession config, reading formats, filtering.
# Two code blocks share T.1.2: exact dedup, near-dedup.
# Fix: add caption after SparkSession config (T.1.1), reading formats gets none (part of pipeline),
# and keep filtering + T.1.1 caption together. Actually: split T.1.1.
def fix_t_1(lines):
    # Block1: SparkSession config (ends with spark.sparkContext.setLogLevel)
    spark_idx = find_line_containing(lines, "spark.sparkContext.setLogLevel")
    if spark_idx == -1:
        return None
    spark_close = find_closing_pre(lines, spark_idx)
    next_after_spark = lines[spark_close + 1].strip() if spark_close + 1 < len(lines) else ""
    if "code-caption" in next_after_spark:
        return None  # already has caption

    # Insert caption after SparkSession config block
    cap_spark = '<div class="code-caption"><strong>Code Fragment T.1.1a:</strong> Configuring a SparkSession for LLM data workloads. Increased shuffle partitions, Kryo serialization, and Adaptive Query Execution are tuned for the wide rows and large shuffles typical of text corpora.</div>'
    lines.insert(spark_close + 1, cap_spark + "\n")

    # Find the reading formats block close (ends with print(f"Row count: ..."))
    row_count_idx = find_line_containing(lines, 'f"Row count:')
    if row_count_idx == -1:
        return lines
    read_close = find_closing_pre(lines, row_count_idx)
    next_after_read = lines[read_close + 1].strip() if read_close + 1 < len(lines) else ""
    if "code-caption" not in next_after_read:
        cap_read = '<div class="code-caption"><strong>Code Fragment T.1.1b:</strong> Reading corpora from multiple formats: Delta Lake, Parquet, newline-delimited JSON, and CSV. Delta Lake is preferred for its ACID guarantees; raw formats are common for externally sourced datasets.</div>'
        lines.insert(read_close + 1, cap_read + "\n")

    # Now handle the dedup pair: find exact dedup block
    exact_idx = find_line_containing(lines, "# --- Exact deduplication via SHA-256 ---")
    if exact_idx == -1:
        return lines
    exact_close = find_closing_pre(lines, exact_idx)
    next_after_exact = lines[exact_close + 1].strip() if exact_close + 1 < len(lines) else ""
    if "code-caption" not in next_after_exact:
        cap_exact = '<div class="code-caption"><strong>Code Fragment T.1.2a:</strong> Exact deduplication via SHA-256 hashing. A window function keeps only the first occurrence of each hash, removing byte-identical documents without shuffling the entire dataset.</div>'
        lines.insert(exact_close + 1, cap_exact + "\n")

    return lines

apply_fix(
    r"appendices\appendix-t-distributed-ml\section-t.1.html",
    "Add sub-captions for SparkSession, reading, and exact dedup blocks",
    fix_t_1
)

# section-t.4: Three blocks (REST API, Composer training, OpenAI client). Caption T.4.1 covers first.
def fix_t_4(lines):
    # Find Composer block
    composer_idx = find_line_containing(lines, "from composer import Trainer")
    if composer_idx == -1:
        return None
    composer_close = find_closing_pre(lines, composer_idx)
    next_after = lines[composer_close + 1].strip() if composer_close + 1 < len(lines) else ""
    if "code-caption" in next_after:
        return None

    # Find OpenAI client block
    openai_idx = find_line_containing(lines, "from openai import OpenAI", composer_close)
    if openai_idx == -1:
        return None
    openai_close = find_closing_pre(lines, openai_idx)

    # Find existing caption
    cap_idx = find_line_containing(lines, "Code Fragment T.4.1")
    if cap_idx == -1:
        return None

    # Insert captions bottom-up
    next_after_openai = lines[openai_close + 1].strip() if openai_close + 1 < len(lines) else ""
    if "code-caption" not in next_after_openai:
        cap3 = '<div class="code-caption"><strong>Code Fragment T.4.3:</strong> Querying a Databricks-hosted model through the OpenAI-compatible API. The same <code>openai</code> client library works by overriding <code>base_url</code> to point at the Databricks serving endpoint.</div>'
        lines.insert(openai_close + 1, cap3 + "\n")

    # Recalculate composer close
    composer_close = find_closing_pre(lines, find_line_containing(lines, "from composer import Trainer"))
    cap2 = '<div class="code-caption"><strong>Code Fragment T.4.2:</strong> Custom fine-tuning with MosaicML Composer on a Databricks cluster. <code>StreamingDataset</code> reads sharded MDS-format data from cloud storage with shuffle buffers that keep GPU utilization high.</div>'
    lines.insert(composer_close + 1, cap2 + "\n")

    return lines

apply_fix(
    r"appendices\appendix-t-distributed-ml\section-t.4.html",
    "Add T.4.2 (Composer) and T.4.3 (OpenAI client) captions",
    fix_t_4
)

# section-2.2 Type 1 remaining: block2 (production BPE code) needs caption
fix_block2_caption(
    r"part-1-foundations\module-02-tokenization-subword-models\section-2.2.html",
    "# Production equivalent using HuggingFace tokenizers",
    "Code Fragment 2.2.13",
    "Production equivalent using HuggingFace tokenizers (Rust-backed). The <code>tokenizers</code> library trains a BPE model in seconds on large corpora, handling the same algorithm as the pseudocode above."
)

# section-c.1 second issue: block2 (peft LoRA) needs caption after C.1.1
# This is the second Type 1 entry for this file. After pass 1 moved C.1.1, the peft block needs caption.
fix_block2_caption(
    r"appendices\appendix-c-python-for-llm\section-c.1.html",
    "# pip install peft",
    "Code Fragment C.1.3",
    "Adding LoRA adapters with the PEFT library. The <code>LoraConfig</code> targets specific attention projection matrices, training only a small fraction of the model's parameters."
)


# ============================================================
# TYPE 2 FIXES: remaining missing caption cases
# ============================================================

# section-2.2 Type 2: Between caption at line 161 and caption at line 275.
# After pass 1, these line numbers shifted. The issue was two pre blocks in the lab section.
# These are the lab implementation blocks that already have proper context.
# Let me check if this was actually resolved by the earlier fix.

# section-4.1 Type 2: Two pre blocks between lines 789 and 924.
# Block1 at 885, block2 at 917.
def fix_4_1_type2(lines):
    # Find the first block in question (around line 885)
    # This is in the labs section; look for the code blocks
    # Check if there's already a proper caption
    # Look for blocks without captions in the lab section
    # Find "Step" headers to identify lab steps
    idx = find_line_containing(lines, "Code Fragment 4.1.10:")
    if idx == -1:
        return None
    # The caption at what was line 924 covers block at 917.
    # Block at 885 might be a setup or missing caption block.
    # Read the area
    # Since line numbers shifted, search by content
    rmsnorm_idx = find_line_containing(lines, "# Manual implementation of RMSNorm")
    if rmsnorm_idx == -1:
        # Try alternate
        rmsnorm_idx = find_line_containing(lines, "class RMSNorm")
    if rmsnorm_idx == -1:
        return None
    # Check if it already has a caption
    rmsnorm_close = find_closing_pre(lines, rmsnorm_idx)
    if rmsnorm_close == -1:
        return None
    next_line = lines[rmsnorm_close + 1].strip() if rmsnorm_close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None

    # Check what's before this block (is it a setup pip install?)
    # Look a few lines before
    for i in range(max(0, rmsnorm_idx - 10), rmsnorm_idx):
        if "pip install" in lines[i]:
            # There's a pip install block before; that's the first pre block.
            # The RMSNorm block is the second. It already has a caption (Code Fragment 4.1.10 below it).
            # The pip install doesn't need a caption. This was correctly skipped.
            return None
    return None

apply_fix(
    r"part-1-foundations\module-04-transformer-architecture\section-4.1.html",
    "Check Type 2 for section 4.1",
    fix_4_1_type2
)

# section-6.3 Type 2: Two pre blocks between captions at 314 and 518.
def fix_6_3_type2(lines):
    # Find the first of the two blocks (around original line 430)
    # This should be a code block missing its caption
    # Look for Code Fragment 6.3.1 and 6.3.2 to identify the area
    cap1_idx = find_line_containing(lines, "Code Fragment 6.3.1")
    if cap1_idx == -1:
        return None
    cap2_idx = find_line_containing(lines, "Code Fragment 6.3.2")
    if cap2_idx == -1:
        return None

    # Find code blocks between these two captions
    pre_blocks = []
    for i in range(cap1_idx, cap2_idx):
        if "<pre><code" in lines[i]:
            pre_blocks.append(i)

    if len(pre_blocks) < 2:
        return None  # expected 2

    # First block needs a caption. Find its close.
    first_close = find_closing_pre(lines, pre_blocks[0])
    next_line = lines[first_close + 1].strip() if first_close + 1 < len(lines) else ""
    if "code-caption" in next_line:
        return None

    # Extract first comment for description
    comment = extract_first_comment(lines, pre_blocks[0])
    if not comment:
        comment = "Code example."

    # Determine caption number: between 6.3.1 and 6.3.2, so this might be a missing intermediate
    # Look at prose before the block for a reference
    for i in range(max(0, pre_blocks[0] - 15), pre_blocks[0]):
        match = re.search(r'(Code Fragment\s+[\w\.]+)', lines[i])
        if match:
            label = match.group(1)
            cap_text = f'<div class="code-caption"><strong>{label}:</strong> {comment}</div>'
            lines.insert(first_close + 1, cap_text + "\n")
            return lines

    # No prose reference found; use incremented number
    cap_text = f'<div class="code-caption"><strong>Code Fragment 6.3.1b:</strong> {comment}</div>'
    lines.insert(first_close + 1, cap_text + "\n")
    return lines

apply_fix(
    r"part-2-understanding-llms\module-06-pretraining-scaling-laws\section-6.3.html",
    "Add missing caption between 6.3.1 and 6.3.2",
    fix_6_3_type2
)

# section-18.2: block2 needs caption after 18.2.1 (TransformerLens circuit tracing)
fix_block2_caption(
    r"part-2-understanding-llms\module-18-interpretability\section-18.2.html",
    "# Using TransformerLens to trace a simple circuit",
    "Code Fragment 18.2.2",
    "Using TransformerLens to trace a simple circuit. This demonstrates the conceptual approach behind attribution graphs, hooking into model activations to track information flow."
)

# section-18.3: block2 needs caption (ROME model editing)
fix_block2_caption(
    r"part-2-understanding-llms\module-18-interpretability\section-18.3.html",
    "# Model Editing with ROME",
    "Code Fragment 18.3.2",
    "Model editing with ROME (Rank-One Model Editing). ROME updates a single feedforward layer's weights to change a specific factual association while preserving the model's other knowledge."
)

# section-c.4: block2 needs caption (save model)
fix_block2_caption(
    r"appendices\appendix-c-python-for-llm\section-c.4.html",
    "# Save a fine-tuned model",
    "Code Fragment C.4.2",
    "Saving and loading a fine-tuned model. The <code>save_pretrained</code> method stores both model weights and tokenizer files in a directory that can be reloaded with <code>from_pretrained</code>."
)

# ============================================================
# Print results
# ============================================================

print("=" * 70)
print("PASS 2 RESULTS")
print("=" * 70)
print()
print(f"Applied: {len(fixes_applied)}")
for f, d in fixes_applied:
    print(f"  {f}: {d}")
print()
print(f"Skipped: {len(fixes_skipped)}")
for f, d, reason in fixes_skipped:
    print(f"  {f}: {d} -- {reason}")
print()
print(f"Total: {len(fixes_applied)} applied, {len(fixes_skipped)} skipped.")


if __name__ == "__main__":
    pass  # All fixes are applied at module level during import
