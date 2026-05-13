"""Wave 19: write 15 conceptual Mermaid diagrams from the architect review.

Each diagram is a small declarative Mermaid source. After this script
writes the .mmd files, render them with the existing pipeline:

    mmdc -i <X>.mmd -o <X>.png -c scripts/mermaid/mermaid-config.json -w 1200 -s 3 --backgroundColor white

The script just writes the .mmd files; rendering is a separate Bash
step so we can render in parallel and verify each visually.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# Each diagram: (target_dir, filename_stem, mmd_source)
DIAGRAMS = [
    # F1: Four-Tier Intervention Hierarchy
    ('part-3-working-with-llms', 'fig-W19-F01-four-tier-intervention',
     '''flowchart TB
    classDef cheap fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px,color:#1b5e20
    classDef medium fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#f57f17
    classDef expensive fill:#ffccbc,stroke:#e64a19,stroke-width:2px,color:#bf360c
    classDef research fill:#d1c4e9,stroke:#5e35b1,stroke-width:2px,color:#311b92

    T1["Tier 1: Prompting<br/><i>weights frozen</i><br/>cost: free | time: minutes"]:::cheap
    T2["Tier 2: RAG<br/><i>weights frozen</i><br/>cost: embedding+search | time: hours-days"]:::cheap
    T3["Tier 3: Fine-tuning / PEFT<br/><i>some weights change</i><br/>cost: $10-1000+ | time: days-weeks"]:::medium
    T4["Tier 4: Pretraining<br/><i>all weights</i><br/>cost: $1M+ | time: months"]:::expensive

    T1 -->|"insufficient on test set"| T2
    T2 -->|"need behavioral change, not facts"| T3
    T3 -->|"need fundamentally new model (rare)"| T4

    note["Heuristic: 80%% of 'I need to fine-tune'<br/>resolves to 'I need a better prompt or RAG'"]:::research
    T2 -.-> note
'''),

    # F2: Knowledge Storage Spectrum (2-D quadrant)
    ('part-5-retrieval-conversation', 'fig-W19-F02-knowledge-storage-spectrum',
     '''quadrantChart
    title Knowledge Storage Spectrum
    x-axis "Slow Access" --> "Fast Access"
    y-axis "Static (frozen)" --> "Dynamic (updatable)"
    quadrant-1 "Fast + Dynamic"
    quadrant-2 "Slow + Dynamic"
    quadrant-3 "Slow + Static"
    quadrant-4 "Fast + Static"
    "Parametric weights": [0.85, 0.10]
    "Long-context window": [0.80, 0.55]
    "RAG retrieval": [0.45, 0.85]
    "Agent memory": [0.20, 0.80]
    "Tool returns (API)": [0.15, 0.95]
'''),

    # F3: Two Scaling Axes
    ('part-2-understanding-llms', 'fig-W19-F03-two-scaling-axes',
     '''quadrantChart
    title Two Compute Axes (log-log; iso-performance curves)
    x-axis "Less train-time compute" --> "More train-time compute"
    y-axis "Less test-time compute" --> "More test-time compute"
    quadrant-1 "Train-heavy + Test-heavy<br/>(o3, Claude Opus 4 + extended thinking)"
    quadrant-2 "Train-light + Test-heavy<br/>(small model + best-of-N or PRM)"
    quadrant-3 "Train-light + Test-light<br/>(GPT-3.5-turbo, single sample)"
    quadrant-4 "Train-heavy + Test-light<br/>(GPT-4o single sample, Llama-3.1-405B)"
    "GPT-3 (2020)": [0.35, 0.10]
    "GPT-4o (2024)": [0.85, 0.20]
    "Llama 3.1 405B": [0.85, 0.20]
    "DeepSeek-V3 (2025)": [0.80, 0.25]
    "o3 (2024)": [0.85, 0.85]
    "DeepSeek-R1 (2025)": [0.60, 0.85]
    "Qwen3 hybrid +think": [0.55, 0.65]
'''),

    # F4: Goodhart's Law in LLMs
    ('part-8-evaluation-production', 'fig-W19-F04-goodhart-proxy-failures',
     '''flowchart TB
    classDef domain fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#bf360c

    GOODHART["Goodhart's Law<br/><i>'When a measure becomes a target,<br/>it ceases to be a good measure'</i>"]

    F1["1. Reward Hacking (Ch 16)<br/><b>Reward model</b> proxies human preference<br/>Policy learns to game the RM<br/>Mitigation: KL penalty, PRM, smaller RM"]:::domain
    F2["2. Benchmark Saturation (Ch 27)<br/><b>MMLU/GSM8K</b> proxy real capability<br/>Models hit ceiling and contamination<br/>Mitigation: LiveBench, private holdouts"]:::domain
    F3["3. Citation Hallucination (Ch 18)<br/><b>RAG faithfulness metric</b> proxies grounded answers<br/>Model cites real chunks but fabricates content<br/>Mitigation: source-quality gates, multi-source agreement"]:::domain
    F4["4. Attention as Explanation (Ch 31)<br/><b>Attention weights</b> proxy causal explanation<br/>Attention is correlation, not causation<br/>Mitigation: causal interventions, activation patching"]:::domain
    F5["5. Pass@1 Hides Variance (Ch 20)<br/><b>Single-run accuracy</b> proxies agent capability<br/>High run-to-run noise hidden<br/>Mitigation: pass@N, mean &plusmn; std reporting"]:::domain

    GOODHART --> F1
    GOODHART --> F2
    GOODHART --> F3
    GOODHART --> F4
    GOODHART --> F5
'''),

    # F5: Alignment Verification Gap
    ('part-10-frontiers', 'fig-W19-F05-alignment-verification-gap',
     '''xychart-beta
    title "The Alignment Verification Gap (capability vs. our ability to verify)"
    x-axis "Era" ["GPT-2", "GPT-3", "GPT-4", "Claude 3.5", "GPT-4o / o3", "Future"]
    y-axis "Relative level (log)" 0 --> 100
    line "Capability" [10, 25, 50, 65, 85, 95]
    line "Verifiability (humans+small models)" [10, 22, 38, 45, 50, 52]
'''),

    # F6: Generator-Verifier Asymmetry (spectrum)
    ('part-2-understanding-llms', 'fig-W19-F06-generator-verifier-asymmetry',
     '''flowchart LR
    classDef hard fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef medium fill:#fff9c4,stroke:#f9a825,color:#f57f17
    classDef easy fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20

    A["<b>Creative writing</b><br/><i>Generation: hard<br/>Verification: harder</i><br/>(test-time compute helps less)"]:::hard
    B["<b>Open-ended QA</b><br/><i>Generation: medium<br/>Verification: medium</i><br/>(RLHF reward models work)"]:::medium
    C["<b>Code generation</b><br/><i>Generation: hard<br/>Verification: easy (tests)</i><br/>(RLVR works well)"]:::easy
    D["<b>Math proofs</b><br/><i>Generation: very hard<br/>Verification: trivial (checkers)</i><br/>(strongest asymmetry)"]:::easy

    A -->|"verification asymmetry &rarr;"| B -->|""| C -->|""| D
'''),

    # F7: Transformer-as-Residual-Stream
    ('part-1-foundations', 'fig-W19-F07-residual-stream',
     '''flowchart LR
    classDef hl fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef block fill:#fff3e0,stroke:#e65100,color:#bf360c

    EMB["x_embed<br/>(token + position)"]:::hl

    subgraph L1[Layer 1]
      A1[Attention<br/>multi-head]:::block
      M1[MLP / FFN]:::block
    end
    subgraph L2[Layer 2]
      A2[Attention]:::block
      M2[MLP]:::block
    end
    subgraph LN[Layer N]
      AN[Attention]:::block
      MN[MLP]:::block
    end

    EMB -->|"residual stream"| L1
    L1 -->|"residual stream"| L2
    L2 -.->|"..."| LN
    LN -->|"residual stream"| OUT[LM head:<br/>logits over vocab]:::hl

    note["Each layer READS from + WRITES to a shared 'highway'.<br/>Mechanistic interpretability (Ch 31) finds modular circuits<br/>that operate on this stream: induction heads, name movers, ..."]
    L1 -.-> note
'''),

    # F8: MoE routing as learned modularity
    ('part-2-understanding-llms', 'fig-W19-F08-moe-routing-modularity',
     '''flowchart LR
    classDef tok fill:#e1f5fe,stroke:#01579b,color:#01579b
    classDef router fill:#fff9c4,stroke:#f57f17,color:#bf360c
    classDef expert fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20

    T1[Token: 'def']:::tok
    T2[Token: 'integral']:::tok
    T3[Token: 'Hello']:::tok

    R[Router<br/>top-2 selection]:::router

    E1[Expert 1<br/><i>code</i>]:::expert
    E2[Expert 2<br/><i>math</i>]:::expert
    E3[Expert 3<br/><i>conversation</i>]:::expert
    E4[Expert 4<br/><i>multilingual</i>]:::expert
    E5[Expert N<br/><i>...</i>]:::expert

    T1 --> R
    T2 --> R
    T3 --> R

    R -.->|"top-2"| E1
    R -.->|"top-2"| E2
    R -.->|"top-2"| E3
    R -.->|"top-2"| E4
    R -.->|"top-2"| E5

    out[Active params: ~10-15%<br/>Total params: 100%<br/>Specialization is EMERGENT]
    E1 --> out
    E2 --> out
'''),

    # F9: Agent decision tree (when to use an agent)
    ('part-6-agentic-ai', 'fig-W19-F09-agent-decision-tree',
     '''flowchart TB
    classDef q fill:#fff9c4,stroke:#f57f17,color:#bf360c
    classDef a fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef s fill:#ffebee,stroke:#c62828,color:#b71c1c

    Q1{"Does it fit in<br/>one model call?"}:::q
    A1[Use a single LLM call]:::a

    Q2{"Is the workflow<br/>fixed?"}:::q
    A2[Use a workflow / chain<br/>LangChain, prompt template]:::a

    Q3{"Does the model need<br/>to choose actions<br/>conditionally?"}:::q
    A3[Use an agent loop<br/>LangGraph, CrewAI, AutoGen]:::a

    Q4{"Multiple specialist<br/>roles needed?"}:::q
    A4[Use multi-agent<br/>CrewAI, AutoGen handoffs]:::a

    S[STOP. Escalate to research.<br/>Long-horizon autonomy is unsolved.]:::s

    Q1 -->|"Yes"| A1
    Q1 -->|"No"| Q2
    Q2 -->|"Yes"| A2
    Q2 -->|"No"| Q3
    Q3 -->|"Yes (and bounded)"| A3
    Q3 -->|"No"| S
    A3 --> Q4
    Q4 -->|"Yes"| A4
    Q4 -->|"No"| keep[Stay single-agent]:::a
'''),

    # F10: Scaling law resolution (Kaplan vs Chinchilla vs Inference-Optimal)
    ('part-2-understanding-llms', 'fig-W19-F10-scaling-laws-resolution',
     '''xychart-beta
    title "Compute-optimal model size: 3 generations of scaling laws"
    x-axis "log10(compute, FLOPs)" [20, 22, 24, 26, 28]
    y-axis "log10(optimal model size, params)" 0 --> 14
    line "Kaplan 2020 (alpha=0.73)" [4.5, 6.0, 7.5, 9.0, 10.5]
    line "Chinchilla 2022 (alpha=0.50)" [4.0, 5.0, 6.0, 7.0, 8.0]
    line "Inference-Optimal (Sardana 2023)" [3.0, 4.0, 5.0, 6.0, 7.0]
'''),

    # F11: Induction heads circuit
    ('part-10-frontiers', 'fig-W19-F11-induction-heads-circuit',
     '''flowchart LR
    classDef tok fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef head1 fill:#fff3e0,stroke:#e65100,color:#bf360c
    classDef head2 fill:#fce4ec,stroke:#c2185b,color:#880e4f
    classDef pred fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20

    T1[Earlier tokens:<br/>'<i>perro</i> -&gt; <i>dog</i>']:::tok
    T2[Earlier tokens:<br/>'<i>gato</i> -&gt; <i>cat</i>']:::tok
    Q[Current query:<br/>'<i>casa</i> -&gt;']:::tok

    L1["Layer N: Previous-token head<br/>finds prior occurrence of '<i>casa</i>'"]:::head1
    L2["Layer N+1: Induction head<br/>copies what FOLLOWED that occurrence"]:::head2

    P[Prediction: '<i>house</i>'<br/>(by analogy with prior pairs)]:::pred

    T1 --> L1
    T2 --> L1
    Q --> L1
    L1 --> L2
    L2 --> P

    note["Olsson et al. 2022:<br/>This is the mechanism behind few-shot prompting"]
    L2 -.-> note
'''),

    # F12: Chunking-Retrieval-Context Tradeoff (triangle)
    ('part-5-retrieval-conversation', 'fig-W19-F12-chunking-tradeoff',
     '''flowchart TB
    classDef vertex fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20

    A["Small chunks<br/>(50-200 tokens)<br/><i>+ precise retrieval<br/>+ low context cost<br/>- loses surrounding context</i>"]:::vertex
    B["Large chunks<br/>(500-2000 tokens)<br/><i>+ rich context<br/>+ better for narrative<br/>- noisier retrieval<br/>- higher context cost</i>"]:::vertex
    C["Many small + parent doc<br/>(parent-child)<br/><i>+ best of both<br/>+ retrieve precise, expand to parent<br/>- 2x storage<br/>- complex pipeline</i>"]:::vertex

    A <-->|tradeoff| B
    A -.->|hybrid| C
    B -.->|hybrid| C
'''),

    # F13: Alignment Method Decision Matrix (visual companion to T3)
    ('part-4-training-adapting', 'fig-W19-F13-alignment-method-matrix',
     '''quadrantChart
    title "Alignment method selection: data quality vs compute budget"
    x-axis "Less compute" --> "More compute"
    y-axis "Lower data quality" --> "Higher data quality"
    quadrant-1 "High data + high compute"
    quadrant-2 "High data + low compute"
    quadrant-3 "Low data + low compute"
    quadrant-4 "Low data + high compute"
    "SFT (demonstrations)": [0.20, 0.85]
    "DPO (pairs)": [0.35, 0.65]
    "RLHF/PPO (pairs+RM)": [0.85, 0.65]
    "Constitutional AI": [0.55, 0.35]
    "RLVR (verifier-based)": [0.65, 0.95]
    "KTO (binary feedback)": [0.30, 0.40]
'''),

    # F14: LLM Evaluation Taxonomy with Failure Mode
    ('part-8-evaluation-production', 'fig-W19-F14-eval-taxonomy-with-failures',
     '''flowchart TB
    classDef root fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef branch fill:#fff9c4,stroke:#f57f17,color:#bf360c
    classDef leaf fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef fail fill:#ffebee,stroke:#c62828,color:#b71c1c

    R[LLM Evaluation]:::root

    INTRINSIC[Intrinsic<br/>distribution metrics]:::branch
    REF[Reference-based<br/>vs ground truth]:::branch
    JUDGE[Judge-based<br/>model or human]:::branch
    BEH[Behavioral / safety<br/>red-team, adversarial]:::branch
    PROD[Production / online<br/>monitoring + drift]:::branch

    R --> INTRINSIC
    R --> REF
    R --> JUDGE
    R --> BEH
    R --> PROD

    P[Perplexity]:::leaf
    PF["<i>FAIL: tokenizer-dependent;<br/>weak correlation with quality</i>"]:::fail
    INTRINSIC --> P --> PF

    BL[BLEU / ROUGE]:::leaf
    BLF["<i>FAIL: paraphrase penalized;<br/>bad on creative tasks</i>"]:::fail
    REF --> BL --> BLF

    LJ[LLM-as-Judge]:::leaf
    LJF["<i>FAIL: position bias,<br/>verbosity bias, same-model bias</i>"]:::fail
    JUDGE --> LJ --> LJF

    HE[Human eval]:::leaf
    HEF["<i>FAIL: annotator drift,<br/>expensive, slow</i>"]:::fail
    JUDGE --> HE --> HEF

    RT[Red-team / adversarial]:::leaf
    RTF["<i>FAIL: incomplete coverage;<br/>cat-and-mouse with attackers</i>"]:::fail
    BEH --> RT --> RTF
'''),

    # F15: Capability-Interpretability Gap Over Time
    ('part-10-frontiers', 'fig-W19-F15-capability-interpretability-gap',
     '''xychart-beta
    title "Capability-Interpretability Gap (model power vs. what we can verify)"
    x-axis "Year" [2020, 2022, 2024, 2026, 2028]
    y-axis "Relative level" 0 --> 100
    line "Capability (benchmark frontier)" [15, 30, 55, 75, 90]
    line "Interpretability (% of behavior we can explain)" [5, 10, 18, 25, 32]
'''),
]


def main() -> int:
    written = 0
    for target_dir, stem, mmd in DIAGRAMS:
        # Place under part-X/_concept-figs/<stem>.mmd to keep them together
        out_dir = ROOT / target_dir / '_concept-figs'
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f'{stem}.mmd'
        path.write_text(mmd, encoding='utf-8')
        written += 1
    print(f'Wrote {written} Mermaid sources under part-*/_concept-figs/.')
    print('To render:')
    print('  for f in part-*/_concept-figs/fig-W19-*.mmd; do')
    print('    out="${f%.mmd}.png"')
    print('    mmdc -i "$f" -o "$out" -c scripts/mermaid/mermaid-config.json -w 1200 -s 3 --backgroundColor white')
    print('  done')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
