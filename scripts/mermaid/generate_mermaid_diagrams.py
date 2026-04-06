#!/usr/bin/env python3
"""Generate Mermaid diagrams as PNGs to replace inline SVGs in the LLMCourse textbook.

Each function produces one .mmd file and renders it to PNG via mmdc (Mermaid CLI).
Run with: /c/Python314/python scripts/mermaid/generate_mermaid_diagrams.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "mermaid-config.json"
ARCHIVE_DIR = BASE_DIR / "_archive" / "replaced-svgs"


def render_mermaid(mmd_content: str, output_path: Path, width: int = 1200) -> Path:
    """Write .mmd content to a temp file and render it to PNG via mmdc."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write .mmd file alongside the output for reference
    mmd_path = output_path.with_suffix(".mmd")
    mmd_path.write_text(mmd_content, encoding="utf-8")

    cmd = [
        "mmdc",
        "-i", str(mmd_path),
        "-o", str(output_path),
        "-c", str(CONFIG_PATH),
        "-w", str(width),
        "-s", "3",  # scale factor for high DPI
        "--backgroundColor", "white",
    ]
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"  ERROR: mmdc failed for {output_path.name}")
        print(f"  stderr: {result.stderr}")
        print(f"  stdout: {result.stdout}")
        return None
    print(f"  Created: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# Diagram 1: LCEL Chain Data Flow (section-l.1.html, svg_index 1)
# ---------------------------------------------------------------------------
def diagram_l1_lcel_chain() -> Path:
    """LCEL chain data flow: PromptTemplate | ChatModel | OutputParser -> Result."""
    print("\n[1/9] LCEL Chain Data Flow (section-l.1.html)")
    mmd = """\
flowchart LR
    A["<b>PromptTemplate</b><br/><i>fills variables</i>"]
    B["<b>ChatModel</b><br/><i>generates response</i>"]
    C["<b>OutputParser</b><br/><i>extracts content</i>"]
    D["<b>Result</b><br/><i>clean string</i>"]

    A -->|"&nbsp;pipe&nbsp;"| B -->|"&nbsp;pipe&nbsp;"| C -->|"&nbsp;pipe&nbsp;"| D

    style A fill:#e8daef,stroke:#8e44ad,stroke-width:2px,color:#4a235a
    style B fill:#d5f5e3,stroke:#27ae60,stroke-width:2px,color:#1e8449
    style C fill:#fdebd0,stroke:#e67e22,stroke-width:2px,color:#935116
    style D fill:#d6eaf8,stroke:#2980b9,stroke-width:2px,color:#1a5276
"""
    out = BASE_DIR / "appendices" / "appendix-l-langchain" / "images" / "lcel-chain-data-flow.png"
    return render_mermaid(mmd, out, width=1000)


# ---------------------------------------------------------------------------
# Diagram 2: RunnableWithMessageHistory (section-l.2.html, svg_index 1)
# ---------------------------------------------------------------------------
def diagram_l2_message_history() -> Path:
    """RunnableWithMessageHistory wrapper flow."""
    print("\n[2/9] RunnableWithMessageHistory (section-l.2.html)")
    mmd = """\
flowchart LR
    UI["<b>User Input</b>"]
    RWM["<b>RunnableWith<br/>MessageHistory</b>"]
    HS["<b>History Store</b><br/><i>get_session_history</i>"]
    CH["<b>LCEL Chain</b>"]
    RS["<b>Response</b>"]

    UI --> RWM
    HS -.->|"load history"| RWM
    RWM --> CH --> RS
    CH -.->|"save exchange"| HS

    style UI fill:#d6eaf8,stroke:#2980b9,stroke-width:2px,color:#1a5276
    style RWM fill:#e8daef,stroke:#8e44ad,stroke-width:2px,color:#4a235a
    style HS fill:#fdebd0,stroke:#e67e22,stroke-width:2px,color:#935116
    style CH fill:#d5f5e3,stroke:#27ae60,stroke-width:2px,color:#1e8449
    style RS fill:#d6eaf8,stroke:#2980b9,stroke-width:2px,color:#1a5276
"""
    out = BASE_DIR / "appendices" / "appendix-l-langchain" / "images" / "runnable-message-history.png"
    return render_mermaid(mmd, out, width=1000)


# ---------------------------------------------------------------------------
# Diagram 3: Agent Execution Loop (section-l.5.html, svg_index 1)
# ---------------------------------------------------------------------------
def diagram_l5_agent_loop() -> Path:
    """Agent execution loop with tool calls and final answer."""
    print("\n[3/9] Agent Execution Loop (section-l.5.html)")
    mmd = """\
flowchart LR
    UI["<b>User Input</b>"]
    LLM["<b>LLM</b><br/><i>decides action</i>"]
    TOOL["<b>Tool</b><br/><i>execute</i>"]
    FA["<b>Final Answer</b><br/><i>no more tools</i>"]

    UI --> LLM
    LLM -->|"tool call"| TOOL
    TOOL -.->|"observation"| LLM
    LLM -->|"done"| FA

    style UI fill:#d6eaf8,stroke:#2980b9,stroke-width:2px,color:#1a5276
    style LLM fill:#d5f5e3,stroke:#27ae60,stroke-width:2px,color:#1e8449
    style TOOL fill:#fdebd0,stroke:#e67e22,stroke-width:2px,color:#935116
    style FA fill:#e8daef,stroke:#8e44ad,stroke-width:2px,color:#4a235a
"""
    out = BASE_DIR / "appendices" / "appendix-l-langchain" / "images" / "agent-execution-loop.png"
    return render_mermaid(mmd, out, width=900)


# ---------------------------------------------------------------------------
# Diagram 4: LlamaIndex Ingestion Pipeline (section-o.1.html, svg_index 1)
# ---------------------------------------------------------------------------
def diagram_o1_ingestion() -> Path:
    """LlamaIndex ingestion pipeline: Data Sources -> Connectors -> Documents -> TextNodes."""
    print("\n[4/9] LlamaIndex Ingestion Pipeline (section-o.1.html)")
    mmd = """\
flowchart LR
    DS["<b>Data Sources</b><br/><i>files, APIs, DBs</i>"]
    CN["<b>Connectors</b><br/><i>Readers / Loaders</i>"]
    DC["<b>Documents</b><br/><i>+ Transformations</i>"]
    TN["<b>TextNodes</b><br/><i>in an Index</i>"]

    DS --> CN --> DC --> TN

    style DS fill:#eaf2f8,stroke:#2980b9,stroke-width:2px,color:#2c3e50
    style CN fill:#fef9e7,stroke:#f39c12,stroke-width:2px,color:#7d6608
    style DC fill:#eafaf1,stroke:#27ae60,stroke-width:2px,color:#1e8449
    style TN fill:#f5eef8,stroke:#8e44ad,stroke-width:2px,color:#6c3483
"""
    out = BASE_DIR / "appendices" / "appendix-o-llamaindex" / "images" / "ingestion-pipeline.png"
    return render_mermaid(mmd, out, width=1000)


# ---------------------------------------------------------------------------
# Diagram 5: Production LLM Training Architecture (section-6.8.html, svg_index 1)
# ---------------------------------------------------------------------------
def diagram_6_8_training_arch() -> Path:
    """Production LLM training architecture with data, training, fault tolerance, checkpointing."""
    print("\n[5/9] Production Training Architecture (section-6.8.html)")
    mmd = """\
flowchart TB
    subgraph DP["Data Pipeline"]
        direction TB
        DP1["Object Storage<br/>S3/GCS"]
        DP2["Mosaic Streaming"]
        DP3["Deterministic<br/>Sharding"]
        DP4["Data Mixing /<br/>Curriculum"]
        DP5["Integrity Checks"]
    end

    subgraph TF["Training Framework"]
        direction TB
        TF1["Megatron-Core"]
        TF2["TP + PP + DP + CP"]
        TF3["torch.compile +<br/>Inductor"]
        TF4["FlashAttention-3"]
        TF5["FP8 Transformer<br/>Engine"]
    end

    subgraph FT["Fault Tolerance"]
        direction TB
        FT1["TorchElastic"]
        FT2["Health Monitoring"]
        FT3["Auto-Recovery"]
        FT4["Node Drain /<br/>Replace"]
        FT5["NaN Detection"]
    end

    subgraph CK["Checkpointing"]
        direction TB
        CK1["PyTorch DCP"]
        CK2["Async Staging"]
        CK3["Reshardable"]
        CK4["Parallel I/O"]
        CK5["Milestone Saves"]
    end

    DP --> TF --> FT --> CK

    subgraph MO["Monitoring and Observability"]
        direction LR
        MO1["Loss Curves<br/>W&B"]
        MO2["MFU Tracking"]
        MO3["GPU Health<br/>DCGM"]
        MO4["Network Metrics"]
    end

    subgraph HW["GPU Cluster"]
        direction LR
        HW1["H100/H200 Nodes<br/>8 GPUs each, NVLink"]
        HW2["InfiniBand/RoCE<br/>inter-node fabric"]
    end

    TF ~~~ MO
    MO ~~~ HW

    style DP fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#1565c0
    style TF fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#2e7d32
    style FT fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#e65100
    style CK fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#6a1b9a
    style MO fill:#fce4ec,stroke:#c62828,stroke-width:2px,color:#c62828
    style HW fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#283593
"""
    out = BASE_DIR / "part-2-understanding-llms" / "module-06-pretraining-scaling-laws" / "images" / "production-training-architecture.png"
    return render_mermaid(mmd, out, width=1200)


# ---------------------------------------------------------------------------
# Diagram 6: Reasoning Token Flow (section-7.1.html, svg_index 2)
# ---------------------------------------------------------------------------
def diagram_7_1_reasoning_flow() -> Path:
    """Reasoning token flow: Prompt -> Thinking Tokens -> Answer Tokens -> API Response."""
    print("\n[6/9] Reasoning Token Flow (section-7.1.html)")
    mmd = """\
flowchart LR
    P["<b>Prompt</b><br/><i>user input</i>"]
    TH["<b>Thinking Tokens</b><br/><i>5,000+ tokens</i><br/><i>internal reasoning</i>"]
    AN["<b>Answer Tokens</b><br/><i>visible to user</i>"]
    API["<b>API</b><br/><i>Response</i>"]
    KV["<b>KV Cache Impact</b><br/>5,000 thinking tokens = 5,000<br/>KV cache entries before first<br/>answer token"]
    VIS["Hidden: o-series (billed)<br/>Visible: DeepSeek R1"]

    P --> TH --> AN --> API
    TH -.-> VIS
    TH -.-> KV

    style P fill:#1a1a2e,stroke:#0f3460,stroke-width:2px,color:#fff
    style TH fill:#fff3cd,stroke:#e6a817,stroke-width:2px,color:#856404
    style AN fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724
    style API fill:#1a1a2e,stroke:#0f3460,stroke-width:2px,color:#fff
    style KV fill:#e8f4f8,stroke:#17a2b8,stroke-width:2px,color:#0c5460
    style VIS fill:#f8d7da,stroke:#f5c6cb,stroke-width:2px,color:#721c24
"""
    out = BASE_DIR / "part-2-understanding-llms" / "module-07-modern-llm-landscape" / "images" / "reasoning-token-flow.png"
    return render_mermaid(mmd, out, width=1200)


# ---------------------------------------------------------------------------
# Diagram 7: Bolt-on vs Native Multimodal Architecture (section-7.1.html, svg_index 3)
# ---------------------------------------------------------------------------
def diagram_7_1_multimodal_arch() -> Path:
    """Bolt-on vs native multimodal architecture comparison."""
    print("\n[7/9] Multimodal Architecture Comparison (section-7.1.html)")
    mmd = """\
flowchart TB
    subgraph BOLT["Bolt-On Multimodal (GPT-4V style)"]
        direction TB
        VE["<b>Vision Encoder</b><br/><i>ViT</i>"]
        TT["<b>Text Tokenizer</b>"]
        LA["<b>Linear Adapter</b>"]
        TE["<b>Text Embeddings</b>"]
        LLM1["<b>LLM Backbone</b><br/><i>pre-trained, often frozen</i>"]
        GAP["Representational gap<br/>bridged by adapter"]

        VE --> LA
        TT --> TE
        LA --> LLM1
        TE --> LLM1
        LLM1 -.-> GAP
    end

    subgraph NATIVE["Native Multimodal (Gemini / GPT-4o style)"]
        direction TB
        IMG["<b>Image</b><br/><i>patches</i>"]
        AUD["<b>Audio</b><br/><i>spectrograms</i>"]
        TXT["<b>Text</b><br/><i>tokens</i>"]
        UNI["<b>Unified Token / Embedding Space</b><br/><i>jointly optimized across all modalities</i>"]
        STK["<b>Single Transformer Stack</b><br/><i>cross-modal attention</i><br/><i>tokens attend to each other freely</i>"]
        BEN["No adapter gap.<br/>Joint training objective."]

        IMG --> UNI
        AUD --> UNI
        TXT --> UNI
        UNI --> STK
        STK -.-> BEN
    end

    style BOLT fill:#fef2f2,stroke:#c0392b,stroke-width:2px,color:#c0392b
    style NATIVE fill:#f0faf0,stroke:#28a745,stroke-width:2px,color:#28a745
    style VE fill:#fff,stroke:#c0392b,stroke-width:2px,color:#c0392b
    style TT fill:#fff,stroke:#1a1a2e,stroke-width:2px,color:#1a1a2e
    style LA fill:#fde8e8,stroke:#c0392b,stroke-width:2px,color:#c0392b
    style TE fill:#e8f4f8,stroke:#1a1a2e,stroke-width:2px,color:#1a1a2e
    style LLM1 fill:#1a1a2e,stroke:#0f3460,stroke-width:2px,color:#fff
    style GAP fill:#fef2f2,stroke:#c0392b,stroke-width:1px,color:#c0392b
    style IMG fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724
    style AUD fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724
    style TXT fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724
    style UNI fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724
    style STK fill:#1a1a2e,stroke:#28a745,stroke-width:2px,color:#fff
    style BEN fill:#f0faf0,stroke:#28a745,stroke-width:1px,color:#155724
"""
    out = BASE_DIR / "part-2-understanding-llms" / "module-07-modern-llm-landscape" / "images" / "bolt-on-vs-native-multimodal.png"
    return render_mermaid(mmd, out, width=1200)


# ---------------------------------------------------------------------------
# Diagram 8: Soft Prompt Method Decision Flowchart (section-15.4.html, svg_index 2)
# ---------------------------------------------------------------------------
def diagram_15_4_peft_decision() -> Path:
    """Decision flowchart for choosing soft prompt method vs LoRA."""
    print("\n[8/9] PEFT Decision Flowchart (section-15.4.html)")
    mmd = """\
flowchart TD
    START(["<b>Start: Choose PEFT Method</b>"])
    Q1{"Is your base model<br/>10B+ parameters?"}
    PT["<b>Prompt Tuning</b>"]
    Q2{"Is it a generation task?<br/><i>summarization, text-gen</i>"}
    PFX["<b>Prefix Tuning</b>"]
    Q3{"NLU task,<br/>small-to-medium model?<br/><i>NER, classification, etc.</i>"}
    PT2["<b>P-Tuning v2</b>"]
    LORA["<b>LoRA / QLoRA</b><br/><i>dominant default choice</i>"]

    START --> Q1
    Q1 -->|"Yes"| PT
    Q1 -->|"No"| Q2
    Q2 -->|"Yes"| PFX
    Q2 -->|"No"| Q3
    Q3 -->|"Yes"| PT2
    Q3 -->|"No"| LORA

    style START fill:#37474f,stroke:#263238,stroke-width:2px,color:#fff
    style Q1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#1565c0
    style PT fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#1565c0
    style Q2 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#6a1b9a
    style PFX fill:#e1bee7,stroke:#6a1b9a,stroke-width:2px,color:#6a1b9a
    style Q3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#2e7d32
    style PT2 fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#2e7d32
    style LORA fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#f57f17
"""
    out = BASE_DIR / "part-4-training-adapting" / "module-15-peft" / "images" / "peft-decision-flowchart.png"
    return render_mermaid(mmd, out, width=800)


# ---------------------------------------------------------------------------
# Diagram 9: Five-Layer Memory Taxonomy (section-22.7.html, svg_index 1)
# ---------------------------------------------------------------------------
def diagram_22_7_memory_taxonomy() -> Path:
    """Five-layer agent memory taxonomy with working memory at center."""
    print("\n[9/9] Memory Taxonomy (section-22.7.html)")
    mmd = """\
flowchart TB
    WM["<b>Working Memory</b><br/><i>Fast, bounded context window</i>"]

    EM["<b>Episodic Memory</b><br/><i>Conversation history, events</i>"]
    SM["<b>Semantic Memory</b><br/><i>Facts, knowledge, summaries</i>"]
    PM["<b>Profile Memory</b><br/><i>User prefs, persona, config</i>"]
    RM["<b>Retrieval Memory</b><br/><i>Vector store, external docs</i>"]

    EM -->|"load into context"| WM
    SM -->|"load into context"| WM
    PM -->|"load into context"| WM
    RM -->|"load into context"| WM

    WM -.->|"write back"| EM
    WM -.->|"write back"| SM
    WM -.->|"write back"| PM
    WM -.->|"write back"| RM

    style WM fill:#fce4ec,stroke:#e94560,stroke-width:3px,color:#c62828
    style EM fill:#e3f2fd,stroke:#3498db,stroke-width:2px,color:#1565c0
    style SM fill:#e8f5e9,stroke:#27ae60,stroke-width:2px,color:#2e7d32
    style PM fill:#fff3e0,stroke:#f39c12,stroke-width:2px,color:#e65100
    style RM fill:#f3e5f5,stroke:#8e44ad,stroke-width:2px,color:#6a1b9a
"""
    out = BASE_DIR / "part-6-agentic-ai" / "module-22-ai-agents" / "images" / "memory-taxonomy-five-layers.png"
    return render_mermaid(mmd, out, width=900)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Generating 9 Mermaid diagrams as PNGs")
    print("=" * 60)

    # Ensure images directories exist
    for d in [
        "appendices/appendix-l-langchain/images",
        "appendices/appendix-o-llamaindex/images",
        "part-2-understanding-llms/module-06-pretraining-scaling-laws/images",
        "part-2-understanding-llms/module-07-modern-llm-landscape/images",
        "part-4-training-adapting/module-15-peft/images",
        "part-6-agentic-ai/module-22-ai-agents/images",
    ]:
        (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

    results = []
    funcs = [
        diagram_l1_lcel_chain,
        diagram_l2_message_history,
        diagram_l5_agent_loop,
        diagram_o1_ingestion,
        diagram_6_8_training_arch,
        diagram_7_1_reasoning_flow,
        diagram_7_1_multimodal_arch,
        diagram_15_4_peft_decision,
        diagram_22_7_memory_taxonomy,
    ]

    for fn in funcs:
        path = fn()
        results.append((fn.__name__, path))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    success = 0
    for name, path in results:
        status = "OK" if path and path.exists() else "FAILED"
        if status == "OK":
            success += 1
        print(f"  {status}: {name} -> {path}")

    print(f"\n{success}/{len(results)} diagrams generated successfully.")
    return 0 if success == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
