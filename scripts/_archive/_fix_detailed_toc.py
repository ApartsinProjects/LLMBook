"""Fix the detailed TOC section to reflect the new chapter structure."""

import re

toc_path = r"E:/Projects/LLMCourse/toc.html"

with open(toc_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Ch 26 title in detailed TOC
content = content.replace(
    '<h2><a href="part-8-evaluation-production/module-26-evaluation-observability/index.html">Evaluation, Experiment Design &amp; Observability</a></h2>',
    '<h2><a href="part-8-evaluation-production/module-26-evaluation-observability/index.html">Evaluation &amp; Experiment Design</a></h2>'
)

# 2. In detailed TOC, the Ch 26 section currently includes lessons 26.1-26.8.
# We need to split: 26.1-26.4 stay in Ch 26, 26.5-26.8 move to new Ch 27 section.
# Find the section for lesson 26.5 and replace it with a Ch 27 header.

# Remove lessons 26.5-26.8 from Ch 26 and close Ch 26 body/div
# Then insert Ch 27 (Observability) with lessons 27.1-27.4

old_26_5_to_end = '''            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">26.5</span> <a href="part-8-evaluation-production/module-26-evaluation-observability/section-26.5.html">Observability &amp; Tracing</a>'''

# Find where 26.5 starts
idx_26_5 = content.find(old_26_5_to_end)
if idx_26_5 > 0:
    # Find the closing </div></div> for ch26 after 26.8
    # Look for the closing of ch26's chapter-body and book-chapter divs
    idx_ch26_end_marker = content.find('<!-- PART VII: PRODUCTION', idx_26_5)
    if idx_ch26_end_marker < 0:
        idx_ch26_end_marker = content.find('<!-- CHAPTER 26: Production', idx_26_5)
    if idx_ch26_end_marker < 0:
        # Find the closing divs after 26.8
        idx_ch26_end_marker = content.find('</div>\n    </div>\n\n    <!-- ===', idx_26_5)

    if idx_ch26_end_marker > 0:
        # Replace everything from 26.5 to the end of Ch 26 block with closing divs
        # Then insert Ch 27 Observability
        ch26_close_and_ch27 = """        </div>
    </div>

    <!-- ============================================================ -->
    <!-- CHAPTER 27: Observability, Monitoring & MLOps -->
    <!-- ============================================================ -->
    <div class="book-chapter" id="ch27">
        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle('collapsed')">
            <div><span class="chapter-num">Chapter 27</span>
                <h2><a href="part-8-evaluation-production/module-27-observability-monitoring/index.html">Observability, Monitoring &amp; MLOps</a></h2>
            </div>
            <span class="chevron">&#9660;</span>
        </div>
        <div class="chapter-body">
            <p class="chapter-desc">Make LLM applications observable, monitorable, and reproducible in production with tracing, drift detection, experiment tracking, and arena-style evaluation.</p>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">27.1</span> <a href="part-8-evaluation-production/module-27-observability-monitoring/section-27.1.html">Observability &amp; Tracing</a> <span class="badge-group"><span class="badge" title="Intermediate">&#x1F7E1;</span><span class="badge" title="Engineering">&#x2699;&#xFE0F;</span><span class="badge" title="Lab">&#x1F527;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>LLM tracing: capturing the full chain of calls</li>
                    <li>LangSmith, Langfuse, Phoenix, LangWatch, TruLens</li>
                    <li>Structured logging patterns and production alerting</li>
                    <li><strong>Lab:</strong> Instrument the project agent with Langfuse tracing</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">27.2</span> <a href="part-8-evaluation-production/module-27-observability-monitoring/section-27.2.html">LLM-Specific Monitoring &amp; Drift Detection</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Engineering">&#x2699;&#xFE0F;</span><span class="badge" title="Lab">&#x1F527;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Prompt drift, provider version drift, embedding drift</li>
                    <li>Output quality monitoring and statistical process control</li>
                    <li>Data quality monitoring for LLM pipelines</li>
                    <li><strong>Lab:</strong> Build a drift detection pipeline with automated alerts</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">27.3</span> <a href="part-8-evaluation-production/module-27-observability-monitoring/section-27.3.html">LLM Experiment Reproducibility</a> <span class="badge-group"><span class="badge" title="Intermediate">&#x1F7E1;</span><span class="badge" title="Engineering">&#x2699;&#xFE0F;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Versioning: prompt + retrieval config + model + system as reproducible artifact</li>
                    <li>Config management: Hydra, OmegaConf</li>
                    <li>Experiment tracking: DVC, MLflow, W&amp;B</li>
                    <li>Containerized reproducibility with Docker</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">27.4</span> <a href="part-8-evaluation-production/module-27-observability-monitoring/section-27.4.html">Arena-Style &amp; Crowdsourced Evaluation</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Chatbot Arena and Elo-based model ranking</li>
                    <li>Crowdsourced human evaluation at scale</li>
                    <li>Pairwise comparison methodologies</li>
                    <li>Community-driven benchmarking for LLM quality</li>
                </ul></div>
            </div>
        </div>
    </div>

"""
        content = content[:idx_26_5] + ch26_close_and_ch27 + content[idx_ch26_end_marker:]

# 3. Update old Ch 27 (Production) to Ch 28
content = content.replace(
    '<div class="book-chapter" id="ch27">\n        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle(\'collapsed\')">\n            <div><span class="chapter-num">Chapter 27</span>\n                <h2><a href="part-8-evaluation-production/module-27-production-engineering/index.html">Production Engineering &amp; Operations</a></h2>',
    '<div class="book-chapter" id="ch28">\n        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle(\'collapsed\')">\n            <div><span class="chapter-num">Chapter 28</span>\n                <h2><a href="part-8-evaluation-production/module-28-production-engineering/index.html">Production Engineering &amp; Operations</a></h2>'
)

# Update all section 27.x references within the old production chapter to 28.x
# These are in the detailed TOC section only
for i in range(1, 5):
    content = content.replace(
        f'<span class="lesson-num">27.{i}</span> <a href="part-8-evaluation-production/module-27-production-engineering/section-27.{i}.html">',
        f'<span class="lesson-num">28.{i}</span> <a href="part-8-evaluation-production/module-28-production-engineering/section-28.{i}.html">'
    )

# 4. Update Ch 28 (Safety) to Ch 29
content = content.replace(
    '<div class="book-chapter" id="ch28">\n        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle(\'collapsed\')">\n            <div><span class="chapter-num">Chapter 28</span>\n                <h2><a href="part-9-safety-strategy/module-28-safety-ethics-regulation/index.html">Safety, Ethics &amp; Regulation</a></h2>',
    '<div class="book-chapter" id="ch29">\n        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle(\'collapsed\')">\n            <div><span class="chapter-num">Chapter 29</span>\n                <h2><a href="part-9-safety-strategy/module-29-safety-ethics-regulation/index.html">Safety, Ethics &amp; Regulation</a></h2>'
)

# Update section references 28.x -> 29.x for safety chapter
for i in range(1, 8):
    content = content.replace(
        f'<span class="lesson-num">28.{i}</span> <a href="part-9-safety-strategy/module-28-safety-ethics-regulation/section-28.{i}.html">',
        f'<span class="lesson-num">29.{i}</span> <a href="part-9-safety-strategy/module-29-safety-ethics-regulation/section-29.{i}.html">'
    )

# 5. Update Ch 29 (Strategy) to Ch 30
content = content.replace(
    '<div class="book-chapter" id="ch29">\n        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle(\'collapsed\')">\n            <div><span class="chapter-num">Chapter 29</span>\n                <h2><a href="part-9-safety-strategy/module-29-strategy-product-roi/index.html">',
    '<div class="book-chapter" id="ch30">\n        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle(\'collapsed\')">\n            <div><span class="chapter-num">Chapter 30</span>\n                <h2><a href="part-9-safety-strategy/module-30-strategy-product-roi/index.html">'
)

# Update section references 29.x -> 30.x for strategy chapter
for i in range(1, 6):
    content = content.replace(
        f'<span class="lesson-num">29.{i}</span> <a href="part-9-safety-strategy/module-29-strategy-product-roi/section-29.{i}.html">',
        f'<span class="lesson-num">30.{i}</span> <a href="part-9-safety-strategy/module-30-strategy-product-roi/section-30.{i}.html">'
    )

# 6. Update Ch 30 (Frontiers) to split into Ch 31 + Ch 32
# Find the Ch 30 frontiers section
old_ch30_start = '<div class="book-chapter" id="ch30">'
idx_ch30 = content.find(old_ch30_start)
if idx_ch30 > 0:
    # Find the end of Ch 30 (closing </div></div>)
    # Look for the closing pair after the chapter-body
    idx_end = content.find('</div>\n    </div>\n\n    </div>', idx_ch30)
    if idx_end < 0:
        # Try finding the end differently
        idx_end = content.find('\n    </div>\n\n<', idx_ch30)

    if idx_end > 0:
        # Find the actual end of the ch30 div block
        # We need to find </div> (chapter-body) </div> (book-chapter)
        remaining = content[idx_ch30:]
        # Count divs to find closing
        depth = 0
        end_pos = 0
        for i, c in enumerate(remaining):
            if remaining[i:i+4] == '<div':
                depth += 1
            elif remaining[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end_pos = idx_ch30 + i + 6
                    break

        if end_pos > 0:
            new_ch31_32 = """<div class="book-chapter" id="ch31">
        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle('collapsed')">
            <div><span class="chapter-num">Chapter 31</span>
                <h2><a href="part-10-frontiers/module-31-emerging-architectures/index.html">Emerging Architectures &amp; Scaling Frontiers</a></h2>
            </div>
            <span class="chevron">&#9660;</span>
        </div>
        <div class="chapter-body">
            <p class="chapter-desc">Emergent abilities, scaling limits, alternative architectures, and the future of model development.</p>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">31.1</span> <a href="part-10-frontiers/module-31-emerging-architectures/section-31.1.html">Emergent Abilities: Real or Mirage?</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>The emergent abilities debate: sudden capability jumps or measurement artifact?</li>
                    <li>Evidence from both sides: phase transitions vs. metric choice effects</li>
                    <li>Implications for practitioners: predicting model capabilities</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">31.2</span> <a href="part-10-frontiers/module-31-emerging-architectures/section-31.2.html">Scaling Frontiers: What Comes Next</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Data walls and synthetic data strategies</li>
                    <li>Test-time compute scaling</li>
                    <li>The three axes of scaling: data, compute, inference</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">31.3</span> <a href="part-10-frontiers/module-31-emerging-architectures/section-31.3.html">Alternative Architectures Beyond Transformers</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>State space models: S4, Mamba, Mamba-2</li>
                    <li>Linear attention: RWKV, RetNet, Griffin</li>
                    <li>Hybrid architectures: Jamba (Mamba + Transformer)</li>
                    <li>When to consider non-transformer architectures in production</li>
                </ul></div>
            </div>
        </div>
    </div>

    <div class="book-chapter" id="ch32">
        <div class="chapter-header-item" onclick="this.parentElement.classList.toggle('collapsed')">
            <div><span class="chapter-num">Chapter 32</span>
                <h2><a href="part-10-frontiers/module-32-ai-society/index.html">AI, Society &amp; Open Problems</a></h2>
            </div>
            <span class="chevron">&#9660;</span>
        </div>
        <div class="chapter-body">
            <p class="chapter-desc">Alignment research, governance challenges, societal impact, and the open problems shaping the next decade of AI development.</p>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">32.1</span> <a href="part-10-frontiers/module-32-ai-society/section-32.1.html">Alignment Research Frontiers</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Scalable oversight and weak-to-strong generalization</li>
                    <li>Interpretability-based alignment</li>
                    <li>The superalignment problem</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">32.2</span> <a href="part-10-frontiers/module-32-ai-society/section-32.2.html">AI Governance and Open Problems</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Compute governance and international frameworks</li>
                    <li>The open-weight debate</li>
                    <li>Frontier model evaluations and liability</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">32.3</span> <a href="part-10-frontiers/module-32-ai-society/section-32.3.html">Societal Impact and the Road Ahead</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Labor market effects and education</li>
                    <li>Creative industries and scientific discovery</li>
                    <li>What skills will matter in an AI-integrated world</li>
                </ul></div>
            </div>

            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">32.4</span> <a href="part-10-frontiers/module-32-ai-society/section-32.4.html">Open Research Problems &amp; Future Directions</a> <span class="badge-group"><span class="badge" title="Advanced">&#x1F534;</span><span class="badge" title="Research">&#x1F52C;</span></span></div>
                <div class="lesson-topics"><ul>
                    <li>Fundamental understanding: mechanistic interpretability, in-context learning</li>
                    <li>Safety frontiers: scalable oversight, corrigibility</li>
                    <li>Efficiency: model compression limits, edge deployment</li>
                    <li>Building a personal research agenda</li>
                </ul></div>
            </div>
        </div>
    </div>"""
            content = content[:idx_ch30] + new_ch31_32 + content[end_pos:]

with open(toc_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Detailed TOC updated successfully")
