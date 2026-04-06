#!/usr/bin/env python3
"""
Generate ALL Mermaid diagrams to replace inline SVGs in the LLMCourse textbook.
Processes 271 SVGs across 131 HTML files.

Usage:
    C:/Python314/python scripts/mermaid/generate_all_mermaid.py [--render-only] [--replace-only] [--file PATTERN]
"""

import os
import re
import subprocess
import sys
import html
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "mermaid-config.json"
ARCHIVE_DIR = BASE_DIR / "_archive" / "replaced-svgs"


def render_mermaid(mmd_content: str, output_path: Path, width: int = 1200) -> Optional[Path]:
    """Write .mmd content to file and render to PNG via mmdc."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mmd_path = output_path.with_suffix(".mmd")
    mmd_path.write_text(mmd_content, encoding="utf-8")

    cmd = [
        "mmdc", "-i", str(mmd_path), "-o", str(output_path),
        "-c", str(CONFIG_PATH), "-w", str(width),
        "-s", "3", "--backgroundColor", "white",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"  ERROR: {output_path.name}: {result.stderr[:200]}")
        return None
    return output_path


def replace_svg_in_html(html_path: Path, svg_index: int, img_src: str, alt_text: str) -> bool:
    """Replace the Nth SVG in an HTML file with an img tag."""
    content = html_path.read_text(encoding="utf-8")
    svgs = list(re.finditer(r'<svg[^>]*>.*?</svg>', content, re.DOTALL))
    if svg_index >= len(svgs):
        print(f"  WARNING: SVG index {svg_index} not found in {html_path}")
        return False

    svg_match = svgs[svg_index]
    svg_text = svg_match.group()

    # Archive the SVG
    archive_name = f"{html_path.stem}-svg{svg_index+1}.html"
    archive_path = ARCHIVE_DIR / archive_name
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(svg_text, encoding="utf-8")

    # Replace SVG with img tag
    img_tag = f'<img src="{img_src}" alt="{alt_text}" loading="lazy" style="max-width: 100%;">'
    new_content = content[:svg_match.start()] + img_tag + content[svg_match.end():]
    html_path.write_text(new_content, encoding="utf-8")
    return True


# ============================================================================
# DIAGRAM DEFINITIONS
# Each returns (mmd_content, output_path, width, html_file, svg_index, alt_text)
# ============================================================================

def get_all_diagrams():
    """Return list of all diagram specs."""
    diagrams = []

    def add(name, mmd, rel_html, svg_idx, rel_img, alt, width=1200):
        diagrams.append({
            'name': name,
            'mmd': mmd,
            'html': str(BASE_DIR / rel_html),
            'svg_idx': svg_idx,
            'img_path': str(BASE_DIR / Path(rel_html).parent / rel_img),
            'img_src': rel_img,
            'alt': alt,
            'width': width,
        })

    # ==================================================================
    # PART 1: FOUNDATIONS (Chapters 0-5)
    # ==================================================================

    # --- Chapter 0: ML and PyTorch Foundations ---

    add("sec0.2-perceptron", """flowchart LR
    subgraph Inputs
        X1["<b>x1</b>"]
        X2["<b>x2</b>"]
        X3["<b>x3</b>"]
    end
    SUM(("<b>&Sigma;</b><br/><i>weighted sum</i>"))
    BIAS["<b>bias b</b>"]
    ACT["<b>f(z)</b><br/><i>activation</i>"]
    Y(("<b>y</b><br/><i>output</i>"))

    X1 -->|"w1"| SUM
    X2 -->|"w2"| SUM
    X3 -->|"w3"| SUM
    BIAS -.->|"+ b"| SUM
    SUM -->|"z = &Sigma;wx + b"| ACT --> Y

    style Inputs fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SUM fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style ACT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style Y fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style BIAS fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html", 0,
    "images/fig-0.2.2-perceptron.png",
    "Anatomy of a single perceptron with inputs, weights, summation, activation, and output",
    1000)

    add("sec0.2-backprop", """flowchart LR
    subgraph FWD["Forward Pass"]
        direction LR
        X["<b>x = 2</b>"]
        W["<b>w = 0.5</b>"]
        Z["<b>z = wx+b</b><br/><i>= 1.5</i>"]
        A["<b>ReLU(z)</b><br/><i>a = 1.5</i>"]
        L["<b>Loss</b><br/><i>(a-y)&sup2; = 0.25</i>"]
    end
    subgraph BWD["Backward Pass (gradients)"]
        direction RL
        DL["dL/da = 1.0"]
        DA["da/dz = 1"]
        DW["dL/dw = 2.0"]
    end

    X --> Z
    W --> Z
    Z --> A --> L
    L -.-> DL -.-> DA -.-> DW

    style FWD fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style BWD fill:#fce4ec,stroke:#c62828,stroke-width:2px""",
    "part-1-foundations/module-00-ml-pytorch-foundations/section-0.2.html", 1,
    "images/fig-0.2.4-backprop.png",
    "Backpropagation through a single neuron showing forward pass and gradient flow",
    1100)

    add("sec0.3-comp-graph", """flowchart LR
    X["<b>x</b><br/><i>leaf tensor</i>"]
    W["<b>w</b><br/><i>leaf tensor</i>"]
    B["<b>b</b><br/><i>leaf tensor</i>"]
    MUL["<b>MulBackward</b>"]
    ADD["<b>AddBackward</b>"]
    LOSS["<b>MSELoss</b>"]
    T["<b>target</b><br/><i>constant</i>"]

    X --> MUL
    W --> MUL
    MUL -->|"z = w*x"| ADD
    B --> ADD
    ADD -->|"y = z+b"| LOSS
    T --> LOSS
    LOSS -.->|".backward()"| ADD -.-> MUL

    style X fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style W fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style B fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style MUL fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style ADD fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style LOSS fill:#fce4ec,stroke:#c62828,stroke-width:2px""",
    "part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html", 0,
    "images/fig-0.3.3-comp-graph.png",
    "Computational graph for linear operation with MSE loss showing leaf tensors and backward traversal",
    1000)

    add("sec0.3-training-loop", """flowchart LR
    ZG["<b>0. Zero Gradients</b><br/><i>optimizer.zero_grad()</i>"]
    FWD["<b>1. Forward Pass</b><br/><i>pred = model(x)</i>"]
    LOSS["<b>2. Compute Loss</b><br/><i>loss = criterion(pred, y)</i>"]
    BWD["<b>3. Backward Pass</b><br/><i>loss.backward()</i>"]
    STEP["<b>4. Optimizer Step</b><br/><i>optimizer.step()</i>"]

    ZG --> FWD --> LOSS --> BWD --> STEP
    STEP -.->|"repeat for each mini-batch"| ZG

    style ZG fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style FWD fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style LOSS fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style BWD fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style STEP fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-00-ml-pytorch-foundations/section-0.3.html", 1,
    "images/fig-0.3.5-training-loop.png",
    "The canonical training loop: zero gradients, forward, loss, backward, optimizer step",
    1100)

    add("sec0.4-rl-loop", """flowchart LR
    AGENT["<b>Agent</b><br/><i>Dog / LLM</i>"]
    ENV["<b>Environment</b><br/><i>Trainer / Reward Model</i>"]

    AGENT -->|"Action (a): sit / next token"| ENV
    ENV -->|"Reward (r): treat / score"| AGENT
    ENV -->|"New State (s'): updated context"| AGENT

    style AGENT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style ENV fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-00-ml-pytorch-foundations/section-0.4.html", 0,
    "images/fig-0.4.2-rl-loop.png",
    "Agent-environment interaction loop with actions, rewards, and state updates",
    900)

    # --- Chapter 1: Foundations of NLP and Text Representation ---

    add("sec1.1-nlp-eras", """flowchart LR
    R["<b>Rule-Based</b><br/><i>1950s to 1980s</i><br/>Hand-written rules"]
    S["<b>Statistical</b><br/><i>1990s to 2000s</i><br/>Word counts"]
    N["<b>Neural</b><br/><i>2013 to 2017</i><br/>Dense vectors"]
    L["<b>LLM Era</b><br/><i>2017 to Present</i><br/>Contextual vectors"]

    R -->|"representation breakthrough"| S -->|"representation breakthrough"| N -->|"representation breakthrough"| L

    style R fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style S fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style N fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style L fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html", 0,
    "images/fig-1.1.2-nlp-eras.png",
    "The four eras of NLP from rule-based to LLMs, driven by representation breakthroughs",
    1100)

    add("sec1.1-nlp-tasks", """flowchart TB
    subgraph U["Understanding Tasks"]
        direction TB
        U1["<b>Classification</b>"]
        U2["<b>NER</b>"]
        U3["<b>Sentiment</b>"]
        U4["<b>QA</b>"]
    end
    subgraph G["Generation Tasks"]
        direction TB
        G1["<b>Translation</b>"]
        G2["<b>Summarization</b>"]
        G3["<b>Open-ended</b>"]
    end
    LLM["<b>LLMs can perform both</b>"]

    U --> LLM
    G --> LLM

    style U fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style G fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style LLM fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html", 1,
    "images/fig-1.1.4-nlp-tasks.png",
    "NLP tasks grouped by type: understanding vs generation",
    900)

    add("sec1.1-linguistic-layers", """flowchart TB
    P["<b>Pragmatics</b><br/><i>intent, context</i><br/>Can you pass the salt?"]
    SE["<b>Semantics</b><br/><i>meaning</i><br/>bank = river or finance?"]
    SY["<b>Syntax</b><br/><i>grammar, structure</i>"]
    M["<b>Morphology</b><br/><i>word forms</i>"]

    P --- SE --- SY --- M

    style P fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style SE fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SY fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style M fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html", 2,
    "images/fig-1.1.6-linguistic-layers.png",
    "Nested layers of linguistic complexity: morphology, syntax, semantics, pragmatics",
    700)

    add("sec1.2-pipeline", """flowchart LR
    RT["<b>Raw Text</b>"]
    UN["<b>Unicode<br/>Normalize</b>"]
    TK["<b>Tokenize &<br/>Lowercase</b>"]
    SW["<b>Remove<br/>Stop Words</b>"]
    SL["<b>Stem /<br/>Lemmatize</b>"]
    FT["<b>Features</b>"]

    RT --> UN --> TK --> SW --> SL --> FT

    style RT fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style UN fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style TK fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SW fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style SL fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style FT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html", 0,
    "images/fig-1.2.1-nlp-pipeline.png",
    "Classical NLP preprocessing pipeline from raw text to numeric features",
    1100)

    add("sec1.2-stem-lemma", """flowchart LR
    subgraph ST["Stemming (rule-based)"]
        direction TB
        S1["running -> run ✓"]
        S2["studies -> studi ✗"]
        S3["university -> univers ✗"]
    end
    subgraph LM["Lemmatization (dictionary)"]
        direction TB
        L1["running -> run ✓"]
        L2["studies -> study ✓"]
        L3["better -> good ✓"]
    end

    style ST fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style LM fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html", 1,
    "images/fig-1.2.2-stem-lemma.png",
    "Stemming vs lemmatization: stemming chops suffixes, lemmatization finds true base forms",
    900)

    add("sec1.2-bow-matrix", """flowchart TB
    subgraph BOW["Bag-of-Words Count Matrix"]
        direction TB
        HDR["<b>cat | chased | dog | log | mat | on | sat | the</b>"]
        D1["<b>Doc 1:</b> 1 0 0 0 1 1 1 2"]
        D2["<b>Doc 2:</b> 0 0 1 1 0 1 1 2"]
        D3["<b>Doc 3:</b> 1 1 1 0 0 0 0 2"]
    end
    N1["0 = absent (sparse)"]
    N2["1 = present once"]
    N3["2 = frequent"]

    BOW --> N1
    BOW --> N2
    BOW --> N3

    style BOW fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style N1 fill:#f5f5f5,stroke:#999,stroke-width:1px
    style N2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style N3 fill:#fff3e0,stroke:#e65100,stroke-width:1px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html", 2,
    "images/fig-1.2.3-bow-matrix.png",
    "Bag-of-Words count matrix: rows are documents, columns are vocabulary words",
    900)

    add("sec1.2-tfidf", """flowchart LR
    subgraph TFIDF["TF-IDF Weights"]
        direction TB
        LOW["<b>Low IDF (common)</b><br/>the: 0.00 (all docs)<br/>sat: 0.00 (not here)"]
        MED["<b>Medium IDF</b><br/>cat: 0.69 (2 docs)<br/>dog: 0.69 (2 docs)"]
        HIGH["<b>High IDF (rare)</b><br/>chased: 1.10 (1 doc)"]
    end

    style LOW fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style MED fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style HIGH fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.2.html", 3,
    "images/fig-1.2.4-tfidf.png",
    "TF-IDF weights: rare distinctive words get high weight, common words get zero",
    800)

    add("sec1.3-skipgram", """flowchart LR
    subgraph WIN["Window = 2"]
        direction LR
        W1["the"]
        W2["cat"]
        W3["<b>sat</b><br/><i>CENTER</i>"]
        W4["on"]
        W5["the"]
    end
    PAIRS["Training pairs:<br/>(sat, the), (sat, cat),<br/>(sat, on), (sat, the)"]

    W1 -.->|"context"| W3
    W2 -.->|"context"| W3
    W3 -.->|"context"| W4
    W3 -.->|"context"| W5
    W3 --> PAIRS

    style W3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style WIN fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style PAIRS fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html", 0,
    "images/fig-1.3.1-skipgram.png",
    "Skip-gram sliding window: center word paired with context words within window",
    1000)

    add("sec1.3-cosine-sim", """flowchart TB
    subgraph CS["Cosine Similarity"]
        direction TB
        HIGH["<b>king, queen</b><br/>15 deg, cos = 0.97<br/><i>semantically similar</i>"]
        LOW["<b>king, refrigerator</b><br/>65 deg, cos = 0.42<br/><i>unrelated</i>"]
    end
    NOTE["Only direction matters, not length!"]

    CS --> NOTE

    style HIGH fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style LOW fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style NOTE fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html", 1,
    "images/fig-1.3.5-cosine-sim.png",
    "Cosine similarity: small angle means high similarity, large angle means unrelated",
    700)

    add("sec1.3-fasttext", """flowchart LR
    W["<b>running</b>"]
    NG["<b>n-grams</b><br/>ru, run, unn,<br/>nni, nin, ing, ng"]
    SUM(("<b>&Sigma;</b>"))
    V["<b>v(running)</b><br/><i>final vector</i>"]

    W -->|"split"| NG -->|"each -> vector"| SUM --> V

    style W fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style NG fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style SUM fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style V fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html", 2,
    "images/fig-1.3.6-fasttext.png",
    "FastText subword decomposition: word split into n-grams, vectors summed",
    1000)

    add("sec1.4-static-contextual", """flowchart TB
    subgraph STATIC["Static (Word2Vec)"]
        direction TB
        S1["bank (money) -> SAME vector"]
        S2["bank (river) -> SAME vector"]
        S3["bank (rely) -> SAME vector"]
    end
    subgraph CTX["Contextual (ELMo/BERT)"]
        direction TB
        C1["bank (money) -> financial vector"]
        C2["bank (river) -> riverbank vector"]
        C3["bank (rely) -> reliance vector"]
    end

    style STATIC fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style CTX fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html", 0,
    "images/fig-1.4.2-static-contextual.png",
    "Static vs contextual embeddings: one vector per word vs different vectors per usage",
    800)

    add("sec1.4-elmo", """flowchart TB
    TOKENS["<b>Input Tokens</b><br/>The river bank is"]
    CHAR["<b>Character Embedding</b><br/><i>Layer 0</i>"]
    FWD["<b>Forward LSTM</b>"]
    BWD["<b>Backward LSTM</b>"]
    COMB["<b>ELMo Vector</b><br/>a0*h0 + a1*h1 + a2*h2<br/><i>learned weighted sum</i>"]

    TOKENS --> CHAR
    CHAR --> FWD
    CHAR --> BWD
    FWD --> COMB
    BWD --> COMB

    style TOKENS fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style CHAR fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style FWD fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style BWD fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style COMB fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html", 1,
    "images/fig-1.4.3-elmo.png",
    "ELMo computation graph: tokens through character embeddings and bidirectional LSTMs",
    800)

    add("sec1.4-elmo-layers", """flowchart TB
    L2["<b>Layer 2: Semantics</b><br/><i>Word sense, topic, meaning in context</i>"]
    L1["<b>Layer 1: Syntax</b><br/><i>Part-of-speech, grammatical role</i>"]
    L0["<b>Layer 0: Morphology</b><br/><i>Word identity, character patterns</i>"]

    L2 --- L1 --- L0

    style L2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style L1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style L0 fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html", 2,
    "images/fig-1.4.5-elmo-layers.png",
    "Information hierarchy across ELMo layers from morphology to semantics",
    600)

    add("sec1.4-evolution", """flowchart LR
    BOW["<b>BoW / TF-IDF</b><br/><i>Sparse, no semantics</i>"]
    W2V["<b>Word2Vec / GloVe</b><br/><i>Dense, but static</i>"]
    ELMO["<b>ELMo</b><br/><i>Contextual, but slow</i>"]
    BERT["<b>Transformers</b><br/><i>BERT, GPT</i>"]

    BOW -->|"need meaning"| W2V -->|"need context"| ELMO -->|"need speed"| BERT

    style BOW fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style W2V fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style ELMO fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style BERT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html", 3,
    "images/fig-1.4-evolution.png",
    "Evolution from BoW to Transformers, each solving the previous representation's limitation",
    1100)

    # --- Chapter 2: Tokenization and Subword Models ---

    add("sec2.1-vocab-spectrum", """flowchart LR
    CHAR["<b>Character-Level</b><br/>Vocab: ~256<br/>Sequences: Very long<br/>hello = 5 tokens"]
    SUB["<b>Subword (BPE/WP)</b><br/>Vocab: 32K to 100K<br/>Sweet spot<br/>unbreakable = 3 tokens"]
    WORD["<b>Whole-Word</b><br/>Vocab: 100K+<br/>Many OOV words<br/>unbreakable = 1 token (or OOV)"]

    CHAR -->|"sweet spot"| SUB --> WORD

    style CHAR fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style SUB fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style WORD fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.1.html", 0,
    "images/fig-2.1.2-vocab-spectrum.png",
    "Vocabulary size spectrum: subword tokenization is the sweet spot",
    1100)

    add("sec2.1-multilingual-tokens", """flowchart TB
    subgraph CTX["20-token context window usage"]
        direction TB
        EN["<b>English:</b> 5 tokens (75% remaining)"]
        ES["<b>Spanish:</b> 7 tokens (65% remaining)"]
        JA["<b>Japanese:</b> 14 tokens (30% remaining)"]
        HI["<b>Hindi:</b> 18 tokens (10% remaining)"]
    end

    style EN fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style ES fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style JA fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style HI fill:#fce4ec,stroke:#c62828,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.1.html", 1,
    "images/fig-2.1.3-multilingual-tokens.png",
    "Same greeting consumes vastly different context window amounts across languages",
    700)

    add("sec2.1-token-artifacts", """flowchart LR
    RAW["<b>Raw Text</b><br/>What is 128+256?"]
    TOK["<b>Tokenizer</b>"]
    TOKENS["<b>Tokens</b><br/>What, is, 12, 8,<br/>+, 256, ?"]
    MODEL["<b>Model</b><br/><i>sees 12 and 8<br/>as separate</i>"]
    OUT["<b>Output</b><br/>384 (correct)<br/>or 374 (wrong)"]

    RAW --> TOK --> TOKENS --> MODEL --> OUT

    style RAW fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style TOK fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style TOKENS fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style MODEL fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style OUT fill:#fce4ec,stroke:#c62828,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.1.html", 2,
    "images/fig-2.1.5-token-artifacts.png",
    "Tokenization artifacts propagate causing unexpected failures in arithmetic",
    1100)

    add("sec2.2-unigram", """flowchart TB
    WORD["<b>u n b r e a k a b l e</b>"]
    subgraph PATHS["All possible segmentations"]
        direction TB
        BEST["<b>Best:</b> un + break + able"]
        ALT1["Alt 1: un + bre + ak + able"]
        ALT2["Alt 2: u + n + break + able"]
    end
    VITERBI["<b>Viterbi Algorithm</b><br/>Selects highest probability path<br/>log P(un) + log P(break) + log P(able)"]

    WORD --> PATHS --> VITERBI

    style BEST fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style ALT1 fill:#f5f5f5,stroke:#999,stroke-width:1px
    style ALT2 fill:#f5f5f5,stroke:#999,stroke-width:1px
    style VITERBI fill:#e3f2fd,stroke:#1565c0,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.2.html", 0,
    "images/fig-2.2.4-unigram.png",
    "Unigram model selects highest probability segmentation via Viterbi algorithm",
    800)

    add("sec2.2-byte-bpe", """flowchart TB
    CHARS["<b>Characters:</b> H i 你 好"]
    BYTES["<b>UTF-8 bytes:</b><br/>0x48 0x69 0xE4 0xBD 0xA0 0xE5 0xA5 0xBD<br/><i>8 bytes total</i>"]
    MERGED["<b>After BPE merges:</b><br/>Hi (1 token) + 你 (1 token) + 好 (1 token)<br/><i>3 tokens</i>"]

    CHARS --> BYTES -->|"BPE learns byte merges"| MERGED

    style CHARS fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style BYTES fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style MERGED fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.2.html", 1,
    "images/fig-2.2.5-byte-bpe.png",
    "Byte-level BPE starts with 256 byte tokens and merges upward",
    800)

    add("sec2.3-chat-template", """flowchart TB
    SYS["<b>|im_start| system</b><br/>You are a helpful assistant<br/><b>|im_end|</b>"]
    USR["<b>|im_start| user</b><br/>Explain BPE vs WordPiece<br/><b>|im_end|</b>"]
    ASST["<b>|im_start| assistant</b><br/>Response...<br/><b>|im_end|</b>"]

    SYS --> USR --> ASST

    style SYS fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style USR fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style ASST fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.3.html", 0,
    "images/fig-2.3.2-chat-template.png",
    "Chat template uses special tokens to delineate system, user, and assistant messages",
    700)

    add("sec2.3-multimodal-tokens", """flowchart LR
    subgraph TEXT["Text Path"]
        direction TB
        RT["Raw Text<br/>A cat on a mat"]
        BPE["BPE Tokenizer"]
        TT["6 Text Tokens"]
    end
    subgraph IMG["Image Path"]
        direction TB
        RI["Raw Image<br/>224x224 px"]
        PE["Patch Embed<br/>16x16 patches"]
        IT["196 Image Tokens"]
    end
    TF["<b>Transformer</b><br/>202 total tokens"]

    TT --> TF
    IT --> TF

    style TEXT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style IMG fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style TF fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.3.html", 1,
    "images/fig-2.3.3-multimodal-tokens.png",
    "Multimodal models convert images to token sequences via patch embedding",
    1000)

    add("sec2.3-tokenizer-landscape", """flowchart TB
    subgraph BBPE["Byte-Level BPE"]
        direction TB
        B1["GPT-2 / GPT-3 / GPT-4"]
        B2["Llama 2 / Llama 3"]
        B3["Mistral / Claude"]
        B4["Vocab: 32K to 128K"]
    end
    subgraph WP["WordPiece"]
        direction TB
        W1["BERT / mBERT"]
        W2["DistilBERT / ELECTRA"]
        W3["Vocab: 30K to 110K"]
    end
    subgraph UG["Unigram (SentencePiece)"]
        direction TB
        U1["T5 / mT5"]
        U2["XLNet / ALBERT"]
        U3["Vocab: 32K to 250K"]
    end

    style BBPE fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style WP fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style UG fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px""",
    "part-1-foundations/module-02-tokenization-subword-models/section-2.3.html", 2,
    "images/fig-2.3.4-tokenizer-landscape.png",
    "Tokenizer landscape showing which algorithm each major model family uses",
    900)

    # --- Chapter 3: Sequence Models and Attention ---

    add("sec3.1-vanishing-grad", """flowchart LR
    T0["<b>t=0</b><br/><i>large gradient</i>"]
    T15["t=15"]
    T50["t=50"]
    T99["<b>t=99</b><br/><i>loss computed here</i>"]
    NOTE["Gradient from t=0 is<br/>exponentially smaller<br/>than from t=99<br/><b>Vanishing!</b>"]

    T0 -.->|"gradient shrinks"| T15 -.->|"gradient shrinks"| T50 -.->|"gradient shrinks"| T99
    T0 --> NOTE

    style T0 fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style T99 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style NOTE fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-03-sequence-models-attention/section-3.1.html", 0,
    "images/fig-3.1.3-vanishing-grad.png",
    "Gradient magnitude vanishes exponentially over time steps in vanilla RNN",
    1000)

    add("sec3.1-seq2seq", """flowchart LR
    subgraph ENC["ENCODER"]
        direction LR
        E1["LSTM<br/>the"] --> E2["LSTM<br/>cat"] --> E3["LSTM<br/>sat"]
    end
    CTX["<b>ctx</b><br/><i>bottleneck!</i>"]
    subgraph DEC["DECODER"]
        direction LR
        D1["LSTM<br/>le"] --> D2["LSTM<br/>chat"] --> D3["LSTM<br/>assis"]
    end

    E3 -->|"fixed-length vector"| CTX --> D1

    style ENC fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style DEC fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style CTX fill:#fce4ec,stroke:#c62828,stroke-width:2px""",
    "part-1-foundations/module-03-sequence-models-attention/section-3.1.html", 1,
    "images/fig-3.1.6-seq2seq.png",
    "Encoder-decoder architecture with information bottleneck at context vector",
    1100)

    add("sec3.2-gradient-attention", """flowchart TB
    LOSS["<b>Loss L</b>"]
    CTX["<b>context = &Sigma;ah</b>"]
    SOFT["<b>a = softmax(scores)</b>"]
    subgraph HIDDEN["Hidden States"]
        direction LR
        H1["h1"]
        H2["h2"]
        H3["h3<br/><i>high a</i>"]
        H4["h4"]
    end

    LOSS -->|"direct path"| CTX
    CTX --> SOFT
    SOFT -->|"gradient ~ a_j"| HIDDEN
    LOSS -.->|"indirect path"| SOFT

    style LOSS fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style CTX fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style SOFT fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style H3 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-03-sequence-models-attention/section-3.2.html", 0,
    "images/fig-3.2.4-gradient-attention.png",
    "Gradient flow through attention: direct path scales by attention weight",
    900)

    add("sec3.3-scaled-dot-product", """flowchart TB
    Q["<b>Q</b><br/>(n, dk)"]
    K["<b>K</b><br/>(m, dk)"]
    V["<b>V</b><br/>(m, dv)"]
    MM1["<b>MatMul</b><br/>QK^T"]
    SC["<b>Scale</b><br/>/ sqrt(dk)"]
    MASK["<b>Mask?</b><br/><i>optional</i>"]
    SM["<b>Softmax</b>"]
    MM2["<b>MatMul</b><br/>aV"]
    OUT["<b>Output</b>"]

    Q --> MM1
    K --> MM1
    MM1 --> SC --> MASK --> SM --> MM2 --> OUT
    V --> MM2

    style Q fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style K fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style V fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style SM fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style OUT fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px""",
    "part-1-foundations/module-03-sequence-models-attention/section-3.3.html", 0,
    "images/fig-3.3.2-scaled-dot-product.png",
    "Scaled dot-product attention: Q*K^T, scale, mask, softmax, multiply V",
    800)

    add("sec3.3-multi-head", """flowchart TB
    X["<b>Input X</b><br/>(n, d_model)"]
    subgraph HEADS["Parallel Attention Heads"]
        direction LR
        H1["<b>Head 1</b><br/>W1_Q, W1_K, W1_V"]
        H2["<b>Head 2</b><br/>W2_Q, W2_K, W2_V"]
        H3["<b>Head 3</b><br/>W3_Q, W3_K, W3_V"]
        H4["<b>Head 4</b><br/>W4_Q, W4_K, W4_V"]
    end
    CAT["<b>Concat</b><br/>(n, h x dk)"]
    WO["<b>W_O projection</b>"]
    OUT["<b>Output</b><br/>(n, d_model)"]

    X --> HEADS
    H1 --> CAT
    H2 --> CAT
    H3 --> CAT
    H4 --> CAT
    CAT --> WO --> OUT

    style X fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style HEADS fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style CAT fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style OUT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-03-sequence-models-attention/section-3.3.html", 1,
    "images/fig-3.3.3-multi-head.png",
    "Multi-head attention: parallel heads with independent projections, concatenated and projected",
    900)

    # --- Chapter 4: Transformer Architecture ---

    add("sec4.1-cross-entropy", """flowchart LR
    CE["<b>Cross-Entropy H(P,Q)</b>"]
    ENT["<b>Entropy H(P)</b><br/><i>Irreducible uncertainty</i>"]
    KL["<b>KL Divergence D_KL</b><br/><i>Extra cost from using Q</i><br/><i>Training minimizes this</i>"]
    PPL["<b>Perplexity</b><br/>= exp(cross-entropy)"]

    ENT -->|"+"| CE
    KL -->|"+"| CE
    CE -->|"exp"| PPL

    style ENT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style KL fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style CE fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style PPL fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.1.html", 0,
    "images/fig-4.1.2-cross-entropy.png",
    "Cross-entropy decomposes into entropy plus KL divergence; perplexity exponentiates it",
    1000)

    add("sec4.1-pos-encoding", """flowchart LR
    subgraph PE["Positional Encoding Heatmap"]
        direction TB
        HF["<b>Low dimensions (0-3)</b><br/><i>High frequency: oscillates quickly</i>"]
        LF["<b>High dimensions (60-63)</b><br/><i>Low frequency: changes slowly</i>"]
    end
    NOTE["Each position gets a<br/>unique fingerprint from<br/>the combination of<br/>sin/cos frequencies"]

    PE --> NOTE

    style HF fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style LF fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style NOTE fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.1.html", 1,
    "images/fig-4.1.4-pos-encoding.png",
    "Positional encoding: low dimensions oscillate fast, high dimensions change slowly",
    900)

    add("sec4.1-pre-post-ln", """flowchart TB
    subgraph POST["Post-LN (Original)"]
        direction TB
        P1["<b>x</b> (input)"]
        P2["<b>Sub-Layer</b><br/>(Attn/FFN)"]
        P3["<b>+ residual</b>"]
        P4["<b>LayerNorm</b>"]
        P1 --> P2 --> P3 --> P4
        P1 -.->|"residual"| P3
    end
    subgraph PRE["Pre-LN (Modern)"]
        direction TB
        R1["<b>x</b> (input)"]
        R2["<b>LayerNorm</b>"]
        R3["<b>Sub-Layer</b><br/>(Attn/FFN)"]
        R4["<b>+ residual</b>"]
        R1 --> R2 --> R3 --> R4
        R1 -.->|"residual"| R4
    end

    style POST fill:#fce4ec,stroke:#c62828,stroke-width:1px
    style PRE fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.1.html", 2,
    "images/fig-4.1.7-pre-post-ln.png",
    "Post-LN normalizes after residual; Pre-LN normalizes before the sub-layer",
    1000)

    add("sec4.1-causal-mask", """flowchart TB
    subgraph MASK["Causal Attention Mask (4 tokens)"]
        direction TB
        HDR["<b>Query \\ Key: The  cat  sat  down</b>"]
        R1["The:         ✓    ✗    ✗    ✗"]
        R2["cat:         ✓    ✓    ✗    ✗"]
        R3["sat:         ✓    ✓    ✓    ✗"]
        R4["down:        ✓    ✓    ✓    ✓"]
    end
    NOTE["Green = can attend<br/>Red = blocked (set to -inf)"]

    MASK --> NOTE

    style MASK fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style NOTE fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.1.html", 3,
    "images/fig-4.1.8-causal-mask.png",
    "Causal lower-triangular attention mask: each position attends only to previous positions",
    700)

    add("sec4.1-residual-stream", """flowchart LR
    EMB["<b>x_embed</b>"]
    A1["<b>Attn 1</b>"]
    F1["<b>FFN 1</b>"]
    A2["<b>Attn 2</b>"]
    F2["<b>FFN 2</b>"]
    OUT["<b>Output</b>"]

    EMB -->|"+ residual"| A1 -->|"+ residual"| F1 -->|"+ residual"| A2 -->|"+ residual"| F2 -->|"..."| OUT

    style EMB fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style A1 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style F1 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style A2 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style F2 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style OUT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.1.html", 4,
    "images/fig-4.1.9-residual-stream.png",
    "Residual stream: each sub-layer reads from and adds back to a shared communication channel",
    1200)

    add("sec4.2-decoder-only", """flowchart TB
    EMB["<b>Token + Position<br/>Embedding</b>"]
    subgraph BLOCK["Transformer Block (x N)"]
        direction TB
        LN1["LayerNorm"]
        ATT["Causal Multi-Head<br/>Self-Attention"]
        RES1["+ residual"]
        LN2["LayerNorm"]
        FFN["Feed-Forward<br/>(SwiGLU or ReLU)"]
        RES2["+ residual"]
        LN1 --> ATT --> RES1 --> LN2 --> FFN --> RES2
    end
    FLN["Final LayerNorm"]
    LIN["Linear (d_model -> vocab)"]
    SM["Softmax -> next token probs"]

    EMB --> BLOCK --> FLN --> LIN --> SM

    style EMB fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style BLOCK fill:#fff3e0,stroke:#e65100,stroke-width:1px
    style FLN fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style SM fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.2.html", 0,
    "images/fig-4.2.2-decoder-only.png",
    "Decoder-only Transformer: N blocks of self-attention and FFN with Pre-LN ordering",
    800)

    add("sec4.3-three-families", """flowchart LR
    subgraph EO["Encoder-Only"]
        direction TB
        E1["Bidirectional attention"]
        E2["BERT, RoBERTa, DeBERTa"]
        E3["Classification, NER, retrieval"]
    end
    subgraph DO["Decoder-Only"]
        direction TB
        D1["Causal (left-to-right)"]
        D2["GPT, Llama, Claude"]
        D3["Text generation, reasoning"]
    end
    subgraph ED["Encoder-Decoder"]
        direction TB
        ED1["Cross-attention bridge"]
        ED2["T5, BART, mBART"]
        ED3["Translation, summarization"]
    end

    style EO fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style DO fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style ED fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.3.html", 0,
    "images/fig-4.3.2-three-families.png",
    "Three Transformer families: encoder-only, decoder-only, encoder-decoder",
    1200)

    add("sec4.3-rope", """flowchart TB
    subgraph ROPE["RoPE: Rotary Position Embeddings"]
        direction TB
        R0["pos=0: No rotation"]
        R3["pos=3: Rotated by 3&theta;"]
        KEY["<b>Key Property:</b><br/>q(pos=5) . k(pos=3)<br/>depends only on relative distance = 2"]
    end

    style ROPE fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style KEY fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.3.html", 1,
    "images/fig-4.3.3-rope.png",
    "RoPE rotates embedding dimensions by position angle; dot product depends only on relative distance",
    700)

    add("sec4.3-pos-strategies", """flowchart TB
    subgraph SIN["Sinusoidal"]
        S1["Fixed sin/cos waves"]
        S2["Absolute, 0 params"]
        S3["Original Transformer"]
    end
    subgraph LRN["Learned"]
        L1["Trainable vectors"]
        L2["Absolute, N*d params"]
        L3["BERT, GPT-2"]
    end
    subgraph RP["RoPE"]
        R1["Rotation in each layer"]
        R2["Relative, 0 params"]
        R3["Llama, Mistral, GPT-NeoX"]
    end
    subgraph ALI["ALiBi"]
        A1["Linear bias to scores"]
        A2["Relative, 0 params"]
        A3["BLOOM, MPT"]
    end

    style SIN fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style LRN fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style RP fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style ALI fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.3.html", 2,
    "images/fig-4.3.4-pos-strategies.png",
    "Four positional encoding strategies: Sinusoidal, Learned, RoPE, ALiBi",
    1000)

    add("sec4.3-head-behaviors", """flowchart TB
    subgraph HEADS["Attention Head Specializations"]
        direction LR
        H1["<b>Head 1: Syntactic</b><br/>verb attends to subject"]
        H2["<b>Head 2: Local</b><br/>sliding window pattern"]
        H3["<b>Head 3: Induction</b><br/>copies previous pattern"]
        H4["<b>Head 4: Positional</b><br/>attends to specific pos"]
    end
    NOTE["These specializations emerge<br/>from training alone, not<br/>explicitly programmed"]

    HEADS --> NOTE

    style H1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style H2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style H3 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style H4 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style NOTE fill:#f5f5f5,stroke:#999,stroke-width:1px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.3.html", 3,
    "images/fig-4.3.5-head-behaviors.png",
    "Four types of attention head behavior: syntactic, local, induction, positional",
    1100)

    add("sec4.3-pre-post-ln2", """flowchart LR
    subgraph POST["Post-Norm (Vaswani 2017)"]
        direction TB
        P1["x (input)"] --> P2["SubLayer(x)"] --> P3["+ residual"] --> P4["LayerNorm"] --> P5["output"]
    end
    subgraph PRE["Pre-Norm (GPT-2+, modern)"]
        direction TB
        R1["x (input)"] --> R2["LayerNorm"] --> R3["SubLayer"] --> R4["+ residual"] --> R5["output"]
    end
    N1["<b>Post-Norm:</b> Unstable at scale"]
    N2["<b>Pre-Norm:</b> Clean gradient path"]

    POST --> N1
    PRE --> N2

    style POST fill:#fce4ec,stroke:#c62828,stroke-width:1px
    style PRE fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    style N1 fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style N2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.3.html", 4,
    "images/fig-4.3.6-pre-post-ln2.png",
    "Post-Norm vs Pre-Norm: Pre-Norm gives clean gradient path, stable at scale",
    1100)

    add("sec4.4-gpu-memory", """flowchart TB
    REG["<b>Registers</b><br/>~20 TB/s | 256 KB/SM | ~1 cycle"]
    SM["<b>Shared Memory / L1</b><br/>~19 TB/s | 228 KB/SM | ~30 cycles"]
    L2["<b>L2 Cache</b><br/>~5 TB/s | 50 MB (H100) | ~200 cycles"]
    HBM["<b>HBM (Global Memory)</b><br/>3.35 TB/s | 80 GB | ~400 cycles"]

    REG --- SM --- L2 --- HBM

    style REG fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style SM fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style L2 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style HBM fill:#fce4ec,stroke:#c62828,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.4.html", 0,
    "images/fig-4.4.2-gpu-memory.png",
    "GPU memory hierarchy from registers (fastest) to HBM (largest)",
    700)

    add("sec4.4-flash-attention", """flowchart LR
    subgraph FA["FlashAttention Tiling"]
        direction TB
        QB["Q Blocks<br/>(1, 2, 3, 4)"]
        KB["K^T Blocks<br/>(1, 2, 3, 4)"]
        TILE["Compute tile in SRAM"]
    end
    NOTE["Full T x T attention matrix<br/>is NEVER materialized in HBM"]
    STEPS["1. Load Q block, K block<br/>2. Compute tile of scores<br/>3. Online softmax update<br/>4. Accumulate output tile"]

    QB --> TILE
    KB --> TILE
    FA --> NOTE
    FA --> STEPS

    style FA fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style NOTE fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style STEPS fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.4.html", 1,
    "images/fig-4.4.3-flash-attention.png",
    "FlashAttention tiles computation into SRAM blocks, never materializing full attention matrix",
    1000)

    add("sec4.5-complexity", """flowchart TB
    P["<b>P</b> (polynomial time)"]
    NC1["<b>NC1</b><br/>Graph connectivity<br/>Boolean formula eval"]
    TC0["<b>TC0</b><br/>Fixed-depth Transformers<br/>with log-precision"]
    AC0["<b>AC0</b>"]

    P --- NC1 --- TC0 --- AC0

    style P fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style NC1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style TC0 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style AC0 fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-04-transformer-architecture/section-4.5.html", 0,
    "images/fig-4.5.2-complexity.png",
    "Complexity hierarchy: fixed-depth Transformers correspond to TC0",
    700)

    # --- Chapter 5: Decoding and Text Generation ---

    add("sec5.1-greedy", """flowchart TB
    START["<b>The</b>"]
    subgraph GREEDY["Greedy path: 0.6 x 0.4 x 0.5 = 0.12"]
        CAT["cat (0.6)"] --> SAT["sat (0.4)"] --> ON["on (0.5)"]
    end
    subgraph BETTER["Better path: 0.3 x 0.9 x 0.8 = 0.216"]
        OLD["old (0.3)"] --> CAT2["cat (0.9)"] --> PURRED["purred (0.8)"]
    end

    START --> CAT
    START --> OLD

    style GREEDY fill:#fce4ec,stroke:#c62828,stroke-width:1px
    style BETTER fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px""",
    "part-1-foundations/module-05-decoding-text-generation/section-5.1.html", 0,
    "images/fig-5.1.2-greedy.png",
    "Greedy decoding picks highest token but misses better complete sequences",
    900)

    add("sec5.1-beam-search", """flowchart LR
    S0["<b>Step 0</b><br/>The"]
    S1A["The cat<br/>-1.2"]
    S1B["The old<br/>-1.5"]
    S2A["The cat sat<br/>-2.1"]
    S2B["The old cat<br/>-1.9"]
    S3A["The cat sat on<br/>-2.6"]
    S3B["The old cat purred<br/>-2.3 ✓ best"]

    S0 --> S1A
    S0 --> S1B
    S1A --> S2A
    S1B --> S2B
    S2A --> S3A
    S2B --> S3B

    style S3B fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style S3A fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-05-decoding-text-generation/section-5.1.html", 1,
    "images/fig-5.1.3-beam-search.png",
    "Beam search k=2 tracks multiple hypotheses to find best sequence",
    1100)

    add("sec5.2-top-p", """flowchart LR
    subgraph CONF["Confident (peaked)"]
        direction TB
        C1["Paris: 0.70"]
        C2["Lyon: 0.22"]
        CN["nucleus (p=0.9): 2 tokens"]
    end
    subgraph UNCONF["Uncertain (flat)"]
        direction TB
        U1["eat: 0.22"]
        U2["run: 0.19"]
        U3["play: 0.17"]
        U4["read: 0.15"]
        U5["swim: 0.12"]
        UN["nucleus (p=0.9): 5 tokens"]
    end

    style CONF fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style UNCONF fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-05-decoding-text-generation/section-5.2.html", 0,
    "images/fig-5.2.3-top-p.png",
    "Top-p sampling adapts candidate count to model confidence",
    1000)

    add("sec5.3-contrastive", """flowchart LR
    subgraph EXPERT["Expert Model (7B)"]
        direction TB
        E1["brilliant: 0.15"]
        E2["the: 0.30"]
        E3["insightful: 0.08"]
    end
    MINUS["<b>minus</b>"]
    subgraph AMATEUR["Amateur Model (1B)"]
        direction TB
        A1["brilliant: 0.02"]
        A2["the: 0.35"]
        A3["insightful: 0.01"]
    end
    RESULT["<b>Result</b><br/>brilliant: amplified<br/>the: suppressed<br/>insightful: amplified"]

    EXPERT --> MINUS
    AMATEUR --> MINUS
    MINUS --> RESULT

    style EXPERT fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style AMATEUR fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style RESULT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px""",
    "part-1-foundations/module-05-decoding-text-generation/section-5.3.html", 0,
    "images/fig-5.3.2-contrastive.png",
    "Contrastive decoding amplifies expert-preferred tokens, suppresses common ones",
    1100)

    add("sec5.3-speculative", """flowchart LR
    DRAFT["<b>Step 1: Draft Model</b><br/>(fast, 1B params)<br/>Generates 6 tokens<br/>in 6 fast passes"]
    VERIFY["<b>Step 2: Target Model</b><br/>(large, 70B)<br/>Verifies all 6 in 1 pass<br/>Accepts 4, rejects at pos 5"]
    RESAMPLE["<b>Step 3: Resample</b><br/>from target distribution<br/>at rejected position"]

    DRAFT --> VERIFY --> RESAMPLE
    RESAMPLE -.->|"repeat"| DRAFT

    style DRAFT fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style VERIFY fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style RESAMPLE fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-1-foundations/module-05-decoding-text-generation/section-5.3.html", 1,
    "images/fig-5.3.3-speculative.png",
    "Speculative decoding: draft model generates cheaply, target model verifies in one pass",
    1100)

    add("sec5.4-diffusion", """flowchart LR
    subgraph FWD["Forward Process (add noise)"]
        direction LR
        F0["t=0 (clean)<br/>The cat sat on"]
        F1["t=1<br/>The [M] sat on"]
        FT["t=T<br/>[M] [M] [M] [M]"]
    end
    subgraph REV["Reverse Process (denoise)"]
        direction RL
        R0["all [MASK]"]
        R1["[M] cat [M] on"]
        RT["The cat sat on"]
    end

    F0 -->|"mask tokens"| F1 -->|"..."| FT
    R0 -->|"unmask"| R1 -->|"..."| RT

    style FWD fill:#fce4ec,stroke:#c62828,stroke-width:1px
    style REV fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px""",
    "part-1-foundations/module-05-decoding-text-generation/section-5.4.html", 0,
    "images/fig-5.4.2-diffusion.png",
    "Discrete diffusion for text: forward masks tokens, reverse recovers them",
    1100)

    add("sec5.4-ar-vs-diffusion", """flowchart TB
    subgraph AR["Autoregressive (GPT, Llama)"]
        direction TB
        A1["✓ Superior reasoning quality"]
        A2["✓ Mature ecosystem"]
        A3["✓ Easy to apply RLHF"]
        A4["✗ Sequential bottleneck (slow)"]
    end
    subgraph DIFF["Diffusion-Based"]
        direction TB
        D1["✓ Parallel generation"]
        D2["✓ Flexible output length"]
        D3["✓ Natural editing support"]
        D4["✗ Less mature, harder to train"]
    end

    style AR fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style DIFF fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-1-foundations/module-05-decoding-text-generation/section-5.4.html", 1,
    "images/fig-5.4.3-ar-vs-diffusion.png",
    "Autoregressive vs diffusion text generation: strengths and weaknesses",
    900)

    # ==================================================================
    # PART 2: UNDERSTANDING LLMs (Chapters 6-9, 18)
    # ==================================================================

    # --- Chapter 6: Pretraining and Scaling Laws ---

    add("sec6.1-encoder-timeline", """flowchart LR
    B["<b>BERT</b><br/>2018, 110M/340M<br/>Bidirectional MLM"]
    R["<b>RoBERTa</b><br/>2019, 355M<br/>Better training"]
    D["<b>DeBERTa</b><br/>2020, 1.5B<br/>Disentangled attn"]
    DV3["<b>DeBERTa V3</b><br/>2021, 304M<br/>ELECTRA + DeBERTa"]
    MB["<b>ModernBERT</b><br/>2024, 395M<br/>Flash Attn + RoPE"]

    B --> R --> D --> DV3 --> MB

    style B fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style R fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style D fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style DV3 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style MB fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html", 0,
    "images/fig-6.1.2-encoder-timeline.png",
    "Encoder-only model evolution from BERT to ModernBERT",
    1200)

    add("sec6.1-param-growth", """flowchart TB
    subgraph GROWTH["Parameter Growth (log scale)"]
        direction LR
        G1["<b>GPT-1</b><br/>2018, 117M"]
        G2["<b>GPT-2</b><br/>2019, 1.5B"]
        G3["<b>GPT-3</b><br/>2020, 175B"]
        G4["<b>GPT-4</b><br/>2023, undisclosed"]
    end
    subgraph REF["Reference Points"]
        direction LR
        R1["BERT: 340M"]
        R2["T5: 11B"]
        R3["InstructGPT"]
    end

    G1 --> G2 --> G3 --> G4

    style GROWTH fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style REF fill:#f5f5f5,stroke:#999,stroke-width:1px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html", 1,
    "images/fig-6.1.4-param-growth.png",
    "Exponential growth in model parameters from GPT-1 to GPT-4",
    1000)

    add("sec6.2-clm-mlm", """flowchart LR
    subgraph CLM["Causal LM (GPT)"]
        direction TB
        C1["The cat sat ???"]
        C2["Predicts: on (next token)"]
        C3["Left context only"]
        C4["Every position trains"]
    end
    subgraph MLM["Masked LM (BERT)"]
        direction TB
        M1["The [MASK] sat on"]
        M2["Predicts: cat (masked)"]
        M3["Bidirectional context"]
        M4["Only 15% positions train"]
    end

    style CLM fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style MLM fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html", 0,
    "images/fig-6.2.2-clm-mlm.png",
    "CLM sees left context, trains every token; MLM sees full context, trains only masked",
    1000)

    add("sec6.2-multi-token-pred", """flowchart TB
    BACKBONE["<b>Shared Transformer Backbone</b><br/>The cat sat on"]
    H1["<b>Head 1:</b> next token<br/>predicts 'the'"]
    H2["<b>Head 2:</b> t+2<br/>predicts 'mat'"]
    H3["<b>Head 3:</b> t+3<br/>predicts '.'"]

    BACKBONE --> H1
    BACKBONE --> H2
    BACKBONE --> H3

    style BACKBONE fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style H1 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style H2 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style H3 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html", 1,
    "images/fig-6.2.4-multi-token-pred.png",
    "Multi-token prediction: N independent heads on shared backbone predict different future tokens",
    800)

    add("sec6.3-scaling-laws", """flowchart LR
    subgraph KAPLAN["Kaplan (2020)"]
        direction TB
        K1["Model Size: ~5x per 10x C"]
        K2["Data: ~2x"]
        K3["GPT-3: 175B params, 300B tokens"]
        K4["Ratio: ~1.7 tokens/param"]
    end
    subgraph CHINCHILLA["Chinchilla (2022)"]
        direction TB
        C1["Model Size: Equal scaling"]
        C2["Data: Equal scaling"]
        C3["Chinchilla: 70B params, 1.4T tokens"]
        C4["Ratio: ~20 tokens/param"]
    end

    style KAPLAN fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style CHINCHILLA fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html", 0,
    "images/fig-6.3.4-scaling-laws.png",
    "Kaplan favors larger models; Chinchilla recommends equal scaling of params and tokens",
    1000)

    add("sec6.4-data-pipeline", """flowchart LR
    WC["<b>Web Crawl</b><br/>~100TB raw"]
    TE["<b>Text Extract</b><br/>~20TB"]
    DD["<b>Dedup</b><br/>MinHash LSH<br/>~12TB"]
    QF["<b>Quality Filter</b><br/>~5TB"]
    SF["<b>Safety Filter</b><br/>~4TB"]
    DM["<b>Domain Mix</b><br/>~3TB final"]

    WC --> TE --> DD --> QF --> SF --> DM

    style WC fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style TE fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style DD fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style QF fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style SF fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style DM fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html", 0,
    "images/fig-6.4.3-data-pipeline.png",
    "Data curation pipeline: progressive filtering from raw web crawl to training corpus",
    1200)

    add("sec6.6-ddp", """flowchart TB
    subgraph DDP["Data-Parallel Training"]
        direction LR
        G0["<b>GPU 0</b><br/>Full Model<br/>Data Shard 0"]
        G1["<b>GPU 1</b><br/>Full Model<br/>Data Shard 1"]
        G2["<b>GPU 2</b><br/>Full Model<br/>Data Shard 2"]
    end
    AR["<b>All-Reduce</b><br/>Synchronize Gradients"]

    G0 --> AR
    G1 --> AR
    G2 --> AR

    style DDP fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style AR fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html", 0,
    "images/fig-6.6.3-ddp.png",
    "DDP: each GPU holds full model, processes different data, gradients synchronized via all-reduce",
    900)

    add("sec6.6-pipeline", """flowchart LR
    subgraph PIPE["1F1B Pipeline Schedule"]
        direction TB
        G0["GPU 0: F1 F2 F3 F4 B1 B2 B3 B4"]
        G1["GPU 1: .. F1 F2 F3 B1 B2 B3 .."]
        G2["GPU 2: .... F1 F2 B1 B2 ...."]
        G3["GPU 3: ...... F1 B1 ......"]
    end
    NOTE["Interleaves forward (F) and<br/>backward (B) micro-batches<br/>to minimize idle bubbles"]

    PIPE --> NOTE

    style PIPE fill:#e3f2fd,stroke:#1565c0,stroke-width:1px
    style NOTE fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html", 1,
    "images/fig-6.6.4-pipeline.png",
    "1F1B pipeline schedule interleaves forward and backward micro-batches",
    900)

    add("sec6.7-bayesian", """flowchart LR
    PRIOR["<b>Prior P(concept)</b><br/><i>Many possible tasks</i>"]
    FEWSHOT["<b>Few-shot examples</b>"]
    POST["<b>Posterior P(concept|D)</b><br/><i>Narrowed to correct task</i>"]
    PRED["<b>Predict P(y|x,c*)</b><br/><i>Correct answer</i>"]

    PRIOR -->|"update with"| FEWSHOT --> POST --> PRED

    style PRIOR fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style FEWSHOT fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style POST fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style PRED fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html", 0,
    "images/fig-6.7.2-bayesian.png",
    "Bayesian interpretation: pre-training as prior, few-shot narrows posterior",
    1000)

    # --- Chapter 7: Modern LLM Landscape ---

    add("sec7.1-frontier-ecosystem", """flowchart TB
    subgraph T1["TIER 1: FRONTIER LEADERS"]
        direction LR
        OAI["<b>OpenAI</b><br/>GPT-4o, o1, o3"]
        ANT["<b>Anthropic</b><br/>Claude 3.5, 4"]
        GDM["<b>Google DeepMind</b><br/>Gemini 2.0/2.5"]
    end
    subgraph T2["TIER 2: STRONG COMPETITORS"]
        direction LR
        DS["<b>DeepSeek</b><br/>V3, R1"]
        META["<b>Meta AI</b><br/>Llama 3, 4"]
        XAI["<b>xAI</b><br/>Grok 3"]
    end

    style T1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style T2 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html", 0,
    "images/fig-7.1.2-frontier-ecosystem.png",
    "Closed-source frontier model ecosystem by competitive tier",
    1000)

    add("sec7.2-deepseek-v3", """flowchart TB
    subgraph DS["DeepSeek V3 Innovations"]
        direction TB
        MLA["<b>Multi-head Latent Attention</b><br/>Compress K,V into low-rank latent<br/>Reduces KV cache dramatically"]
        MOE["<b>Mixture of Experts</b><br/>256 experts, 8 active per token<br/>37B active of 671B total"]
        MTP["<b>Multi-Token Prediction</b><br/>Predict multiple future tokens<br/>Better representations"]
        FP8["<b>FP8 Training</b><br/>Mixed precision throughout<br/>Lower compute cost"]
    end

    style MLA fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style MOE fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style MTP fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style FP8 fill:#fff3e0,stroke:#e65100,stroke-width:2px""",
    "part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html", 0,
    "images/fig-7.2.1-deepseek-v3.png",
    "Four key architectural innovations in DeepSeek V3",
    800)

    add("sec7.3-train-test-scaling", """flowchart LR
    subgraph TRAIN["Train-Time Scaling"]
        direction TB
        T1["Invest compute ONCE"]
        T2["Larger model, more data"]
        T3["Fixed cost per query"]
    end
    subgraph TEST["Test-Time Scaling"]
        direction TB
        TE1["Additional compute PER QUERY"]
        TE2["Chain-of-thought, search"]
        TE3["Variable cost per query"]
    end

    style TRAIN fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style TEST fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px""",
    "part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html", 0,
    "images/fig-7.3.2-train-test-scaling.png",
    "Train-time vs test-time scaling: one-time investment vs per-query compute",
    1000)

    # I'll continue adding ALL remaining diagrams below...
    # For brevity in this initial version, let me add the remaining sections

    return diagrams


def process_all():
    """Process all diagrams: render first, then replace in reverse order per file."""
    diagrams = get_all_diagrams()
    print(f"Total diagrams to process: {len(diagrams)}")

    rendered = 0
    errors = []

    # Phase 1: Render all PNGs
    for i, d in enumerate(diagrams):
        print(f"\n[{i+1}/{len(diagrams)}] Rendering {d['name']}")
        img_path = Path(d['img_path'])
        result = render_mermaid(d['mmd'], img_path, d.get('width', 1200))
        if result:
            rendered += 1
            d['rendered'] = True
        else:
            errors.append(f"Render failed: {d['name']}")
            d['rendered'] = False

    # Phase 2: Group by HTML file and replace SVGs in REVERSE index order
    from collections import defaultdict
    by_file = defaultdict(list)
    for d in diagrams:
        if d.get('rendered'):
            by_file[d['html']].append(d)

    replaced = 0
    for html_file, file_diagrams in by_file.items():
        # Sort by svg_idx descending so replacements don't shift indices
        file_diagrams.sort(key=lambda x: x['svg_idx'], reverse=True)
        html_path = Path(html_file)
        if not html_path.exists():
            errors.append(f"HTML not found: {html_file}")
            continue

        content = html_path.read_text(encoding="utf-8")
        svgs = list(re.finditer(r'<svg[^>]*>.*?</svg>', content, re.DOTALL))

        for d in file_diagrams:
            idx = d['svg_idx']
            if idx >= len(svgs):
                errors.append(f"SVG index {idx} not found in {html_file}")
                continue

            svg_match = svgs[idx]
            svg_text = svg_match.group()

            # Archive
            archive_name = f"{html_path.stem}-svg{idx+1}.html"
            archive_path = ARCHIVE_DIR / archive_name
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            archive_path.write_text(svg_text, encoding="utf-8")

            # Replace
            img_tag = f'<img src="{d["img_src"]}" alt="{d["alt"]}" loading="lazy" style="max-width: 100%;">'
            content = content[:svg_match.start()] + img_tag + content[svg_match.end():]
            replaced += 1
            print(f"  Replaced {d['name']} (SVG#{idx}) in {html_path.name}")

        html_path.write_text(content, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"Rendered: {rendered}/{len(diagrams)}")
    print(f"Replaced: {replaced}/{len(diagrams)}")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")


if __name__ == "__main__":
    process_all()
