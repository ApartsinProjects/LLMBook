"""
Fix all code blocks in Part 7 and Appendices to have:
1. Code Fragment N captions
2. Opening comments
3. Prose references in preceding paragraphs
"""

import re
import os
import glob

# Collect all target files
files = sorted(
    glob.glob("E:/Projects/LLMCourse/part-7-production-strategy/module-*/section-*.html") +
    glob.glob("E:/Projects/LLMCourse/appendices/*/index.html")
)

# === CLEANUP PASS: Remove duplicate <p class="code-caption"> from appendices ===
for filepath in glob.glob("E:/Projects/LLMCourse/appendices/*/index.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    # Remove <p class="code-caption">Code Fragment X.N: ...</p> lines (the old format)
    content = re.sub(r'\n*<p class="code-caption">Code Fragment [A-Z]+\.\d+:.*?</p>', '', content)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        removed = original.count('<p class="code-caption">Code Fragment') - content.count('<p class="code-caption">Code Fragment')
        print(f"CLEANUP: {os.path.basename(filepath)}: removed {removed} duplicate <p> captions")

# Stats tracking
stats = {}

def detect_language(code_text):
    """Detect language from code content."""
    stripped = code_text.strip()
    # Remove HTML tags for detection
    clean = re.sub(r'<[^>]+>', '', stripped)
    clean_lower = clean.lower().strip()

    # YAML detection (docker-compose, config files)
    if clean_lower.startswith('version:') or clean_lower.startswith('services:') or clean_lower.startswith('name:') or clean_lower.startswith('models:'):
        return 'python'  # YAML uses # comments same as python
    if clean_lower.startswith('import ') or clean_lower.startswith('from ') or 'def ' in clean or 'class ' in clean or 'print(' in clean or 'np.' in clean or 'torch.' in clean or 'python' in clean_lower:
        return 'python'
    if clean_lower.startswith('const ') or clean_lower.startswith('let ') or clean_lower.startswith('var ') or 'function ' in clean or '=>' in clean or 'console.log' in clean or 'route.ts' in clean_lower or 'interface ' in clean:
        return 'javascript'
    if 'select ' in clean_lower and 'from ' in clean_lower:
        return 'sql'
    if clean_lower.startswith('{') or clean_lower.startswith('['):
        return 'json'
    if clean_lower.startswith('$') or clean_lower.startswith('pip ') or clean_lower.startswith('curl ') or clean_lower.startswith('git ') or clean_lower.startswith('conda ') or clean_lower.startswith('docker '):
        return 'bash'
    return 'python'  # default

def get_comment_prefix(lang):
    if lang == 'python':
        return '#'
    if lang in ('javascript', 'java', 'go', 'rust', 'c', 'cpp'):
        return '//'
    if lang == 'sql':
        return '--'
    if lang == 'bash':
        return '#'
    return '#'

def has_opening_comments(code_text, lang):
    """Check if code already starts with comment lines."""
    # Remove leading HTML tags like <code>, <span ...>
    stripped = code_text.strip()
    # Remove wrapping <code> tag
    if stripped.startswith('<code>'):
        stripped = stripped[6:]
    stripped = stripped.strip()

    prefix = get_comment_prefix(lang)

    # Check if first non-empty, non-tag line is a comment
    lines = stripped.split('\n')
    for line in lines[:3]:
        # Strip HTML tags
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if not clean_line:
            continue
        if clean_line.startswith(prefix) or clean_line.startswith('"""') or clean_line.startswith("'''"):
            return True
        return False
    return False

def get_code_plain_text(code_html):
    """Strip all HTML tags to get plain text of code."""
    text = re.sub(r'<[^>]+>', '', code_html)
    return text.strip()

def generate_comment_for_code(code_text, lang):
    """Generate a brief 2-line comment describing the code."""
    plain = get_code_plain_text(code_text)
    prefix = get_comment_prefix(lang)

    # Try to figure out what the code does from its content
    lines = plain.split('\n')

    # Look for class or function definitions
    classes = [l.strip() for l in lines if l.strip().startswith('class ')]
    funcs = [l.strip() for l in lines if l.strip().startswith('def ')]
    imports = [l.strip() for l in lines if l.strip().startswith('import ') or l.strip().startswith('from ')]

    # Build description
    desc_parts = []
    if classes:
        class_names = [re.search(r'class\s+(\w+)', c).group(1) for c in classes if re.search(r'class\s+(\w+)', c)]
        if class_names:
            desc_parts.append(f"Define {', '.join(class_names)}")
    if funcs:
        func_names = [re.search(r'def\s+(\w+)', f).group(1) for f in funcs if re.search(r'def\s+(\w+)', f)]
        if func_names:
            desc_parts.append(f"implement {', '.join(func_names[:3])}")

    if not desc_parts:
        # Generic description from imports/content
        if 'fastapi' in plain.lower():
            desc_parts.append("FastAPI endpoint implementation")
        elif 'docker' in plain.lower() or 'services:' in plain:
            desc_parts.append("Container orchestration configuration")
        elif 'guardrail' in plain.lower() or 'safety' in plain.lower():
            desc_parts.append("Safety guardrail setup")
        elif 'mlflow' in plain.lower() or 'wandb' in plain.lower():
            desc_parts.append("Experiment tracking setup")
        elif 'modal' in plain.lower():
            desc_parts.append("Serverless deployment configuration")
        elif 'boto3' in plain.lower() or 'bedrock' in plain.lower():
            desc_parts.append("AWS cloud integration")
        elif 'gradio' in plain.lower():
            desc_parts.append("Gradio interface setup")
        elif 'streamlit' in plain.lower():
            desc_parts.append("Streamlit dashboard setup")
        elif 'torch' in plain:
            desc_parts.append("PyTorch implementation")
        elif 'numpy' in plain or 'np.' in plain:
            desc_parts.append("NumPy computation")
        elif 'sklearn' in plain:
            desc_parts.append("Scikit-learn example")
        elif 'pip ' in plain or 'conda ' in plain:
            desc_parts.append("Environment setup commands")
        elif 'git ' in plain:
            desc_parts.append("Version control workflow")
        else:
            desc_parts.append("Implementation example")

    line1 = f"{prefix} {'; '.join(desc_parts)}"

    # Try to identify key operations
    key_ops = []
    if 'forward' in plain:
        key_ops.append("forward pass computation")
    if 'loss' in plain.lower():
        key_ops.append("loss calculation")
    if 'train' in plain.lower():
        key_ops.append("training loop")
    if 'softmax' in plain.lower():
        key_ops.append("softmax normalization")
    if 'attention' in plain.lower():
        key_ops.append("attention mechanism")
    if 'embedding' in plain.lower():
        key_ops.append("embedding lookup")
    if 'gradient' in plain.lower() or 'backward' in plain.lower():
        key_ops.append("gradient computation")
    if 'plot' in plain.lower() or 'plt.' in plain:
        key_ops.append("visualization")
    if 'print' in plain:
        key_ops.append("results display")

    # Production / safety / strategy domain-specific operations
    if 'docker' in plain.lower() or 'container' in plain.lower():
        key_ops.append("containerized deployment")
    if 'fastapi' in plain.lower() or 'flask' in plain.lower():
        key_ops.append("API endpoint setup")
    if 'health' in plain.lower():
        key_ops.append("health checking")
    if 'redis' in plain.lower() or 'cache' in plain.lower():
        key_ops.append("caching layer")
    if 'guardrail' in plain.lower() or 'safety' in plain.lower():
        key_ops.append("safety guardrails")
    if 'monitor' in plain.lower() or 'metric' in plain.lower():
        key_ops.append("monitoring and metrics")
    if 'log' in plain.lower() and ('import' in plain.lower() or 'logging' in plain.lower()):
        key_ops.append("structured logging")
    if 'rate_limit' in plain.lower() or 'ratelimit' in plain.lower() or 'throttl' in plain.lower():
        key_ops.append("rate limiting")
    if 'deploy' in plain.lower() or 'modal' in plain.lower() or 'serverless' in plain.lower():
        key_ops.append("deployment configuration")
    if 'cost' in plain.lower() or 'budget' in plain.lower() or 'roi' in plain.lower():
        key_ops.append("cost tracking")
    if 'a/b' in plain.lower() or 'experiment' in plain.lower() or 'canary' in plain.lower():
        key_ops.append("experiment framework")
    if 'encrypt' in plain.lower() or 'hash' in plain.lower() or 'pii' in plain.lower():
        key_ops.append("data protection")
    if 'bias' in plain.lower() or 'fairness' in plain.lower():
        key_ops.append("fairness evaluation")
    if 'mlflow' in plain.lower() or 'wandb' in plain.lower():
        key_ops.append("experiment tracking")
    if 'prompt' in plain.lower():
        key_ops.append("prompt construction")
    if 'openai' in plain.lower() or 'client' in plain.lower():
        key_ops.append("API interaction")
    if 'eval' in plain.lower():
        key_ops.append("evaluation logic")
    if 'git' in plain.lower() and 'import' not in plain.lower():
        key_ops.append("version control workflow")
    if 'pip ' in plain.lower() or 'conda ' in plain.lower() or 'install' in plain.lower():
        key_ops.append("dependency installation")

    if key_ops:
        line2 = f"{prefix} Key operations: {', '.join(key_ops[:3])}"
    else:
        line2 = f"{prefix} See inline comments for step-by-step details."

    # Return HTML-styled comment spans matching existing syntax highlighting
    color = '#6c7086'
    html_line1 = f'<span style="color:{color};">{line1}</span>'
    html_line2 = f'<span style="color:{color};">{line2}</span>'
    return f"{html_line1}\n{html_line2}\n"

def has_caption_after_pre(content, pre_end_pos):
    """Check if there's a code-caption div right after the </pre> tag."""
    after = content[pre_end_pos:pre_end_pos + 300].strip()
    return after.startswith('<div class="code-caption">')

def has_caption_before_pre(content, pre_start_pos):
    """Check if there's a code-caption div right before the <pre> tag."""
    before = content[max(0, pre_start_pos - 300):pre_start_pos].strip()
    return before.endswith('</div>') and '<div class="code-caption">' in content[max(0, pre_start_pos - 300):pre_start_pos]

def get_caption_before_pre(content, pre_start_pos):
    """Get the code-caption div text before the <pre> tag."""
    search_zone = content[max(0, pre_start_pos - 500):pre_start_pos]
    match = re.search(r'<div class="code-caption">(.*?)</div>', search_zone, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def caption_has_fragment_label(caption_text):
    """Check if caption already has 'Code Fragment N:' label."""
    if caption_text is None:
        return False
    return bool(re.search(r'Code Fragment \d+:', re.sub(r'<[^>]+>', '', caption_text)))

def is_caption_too_short(caption_text):
    """Check if caption is too short (less than ~50 chars of actual text)."""
    if caption_text is None:
        return True
    plain = re.sub(r'<[^>]+>', '', caption_text).strip()
    return len(plain) < 80

def generate_caption_text(code_text, fragment_num):
    """Generate a descriptive caption for a code block."""
    plain = get_code_plain_text(code_text)

    # Analyze code content
    has_class = 'class ' in plain
    has_func = 'def ' in plain or 'function ' in plain
    has_torch = 'torch' in plain
    has_numpy = 'numpy' in plain or 'np.' in plain
    has_plot = 'plt.' in plain or 'plot' in plain.lower()
    has_train = 'train' in plain.lower()
    has_attention = 'attention' in plain.lower()
    has_loss = 'loss' in plain.lower()
    has_embed = 'embed' in plain.lower()

    # Build description sentence
    parts = []

    # Class/func names
    class_match = re.findall(r'class\s+(\w+)', plain)
    func_match = re.findall(r'def\s+(\w+)', plain)

    if class_match:
        parts.append(f"the {class_match[0]} class")
    if func_match:
        funcs = [f for f in func_match if f not in ('__init__', 'forward', '__repr__', '__str__')]
        if funcs:
            parts.append(f"the {', '.join(funcs[:2])} function{'s' if len(funcs) > 1 else ''}")

    topic = ' and '.join(parts) if parts else 'this approach'

    has_docker = 'docker' in plain.lower() or 'container' in plain.lower()
    has_fastapi = 'fastapi' in plain.lower()
    has_guardrail = 'guardrail' in plain.lower() or 'safety' in plain.lower()
    has_monitor = 'monitor' in plain.lower() or 'metric' in plain.lower()
    has_deploy = 'deploy' in plain.lower() or 'modal' in plain.lower() or 'serverless' in plain.lower()
    has_cost = 'cost' in plain.lower() or 'budget' in plain.lower() or 'roi' in plain.lower()
    has_cache = 'redis' in plain.lower() or 'cache' in plain.lower()
    has_hash = 'hash' in plain.lower() or 'encrypt' in plain.lower()
    has_api = 'openai' in plain.lower() or 'client' in plain.lower() or 'boto3' in plain.lower()
    has_mlops = 'mlflow' in plain.lower() or 'wandb' in plain.lower()
    has_git_ops = 'git ' in plain.lower() and 'import' not in plain.lower()
    has_install = 'pip ' in plain.lower() or 'conda ' in plain.lower()

    tech = []
    if has_torch:
        tech.append('PyTorch')
    if has_numpy:
        tech.append('NumPy')
    if has_fastapi:
        tech.append('FastAPI')
    if has_docker:
        tech.append('containerization')
    if has_guardrail:
        tech.append('safety guardrails')
    if has_monitor:
        tech.append('monitoring')
    if has_deploy:
        tech.append('deployment automation')
    if has_cost:
        tech.append('cost analysis')
    if has_cache:
        tech.append('caching')
    if has_hash:
        tech.append('data protection')
    if has_api:
        tech.append('API calls')
    if has_mlops:
        tech.append('experiment tracking')
    if has_attention:
        tech.append('attention computation')
    if has_embed:
        tech.append('embedding operations')
    if has_loss:
        tech.append('loss computation')
    if has_train:
        tech.append('training')
    if has_plot:
        tech.append('visualization')
    if has_git_ops:
        tech.append('version control')
    if has_install:
        tech.append('environment setup')

    tech_str = f" using {', '.join(tech[:2])}" if tech else ""

    desc = f"This snippet demonstrates {topic}{tech_str}."

    # Add a "notice" sentence
    notices = []
    if has_docker:
        notices.append("Notice the health checks and resource reservations that keep the stack resilient under load.")
    elif has_guardrail:
        notices.append("Notice how the safety checks run both before and after model inference to catch policy violations early.")
    elif has_monitor:
        notices.append("Notice how the metrics are tagged with request metadata so you can slice dashboards by model, user, or endpoint.")
    elif has_cost:
        notices.append("Notice how cost is tracked per request so you can attribute spend to individual features or customers.")
    elif has_cache:
        notices.append("Notice how the cache key is constructed to balance hit rate against staleness risk.")
    elif has_hash:
        notices.append("Notice how sensitive fields are handled before any data leaves the trusted boundary.")
    elif has_mlops:
        notices.append("Notice how experiment parameters and artifacts are logged together for full reproducibility.")
    elif has_fastapi:
        notices.append("Notice how async handlers prevent a single slow request from blocking the entire server.")
    elif has_deploy:
        notices.append("Notice how the deployment configuration separates environment-specific values from application code.")
    elif 'retriev' in plain.lower():
        notices.append("Notice how the retrieval step filters candidates before passing them to downstream processing.")
    elif 'agent' in plain.lower():
        notices.append("Notice how the agent loop decides which tool to invoke based on the current reasoning state.")
    elif 'eval' in plain.lower():
        notices.append("Notice how the evaluation criteria are defined to measure quality along multiple dimensions.")
    elif 'dropout' in plain.lower():
        notices.append("Notice how dropout is applied for regularization during training.")
    elif has_attention:
        notices.append("Notice how the attention weights are computed and applied to the value vectors.")
    elif 'mask' in plain.lower():
        notices.append("Notice how masking prevents information leakage from future positions.")
    elif has_embed:
        notices.append("Notice how the embedding dimensions capture semantic similarity across inputs.")
    elif has_loss:
        notices.append("Notice how the loss function drives the optimization process toward better predictions.")
    elif has_train:
        notices.append("Notice how each training step updates the model parameters based on the computed gradients.")
    elif has_plot:
        notices.append("The resulting visualization highlights the key trends and patterns in the data.")
    elif has_func:
        notices.append("The function encapsulates reusable logic that can be applied across different inputs.")
    else:
        notices.append("Study the implementation details to understand how each component contributes to the overall computation.")

    # Add a "why it matters" sentence
    matters = []
    if has_docker:
        matters.append("Containerized deployments provide consistent behavior from local development through production.")
    elif has_guardrail:
        matters.append("Layered safety checks are essential for responsible deployment and regulatory compliance.")
    elif has_monitor:
        matters.append("Proactive monitoring catches regressions before they reach users and simplifies root-cause analysis.")
    elif has_cost:
        matters.append("Granular cost tracking turns LLM spend from an opaque line item into an optimizable variable.")
    elif has_mlops:
        matters.append("Reproducible experiments are the foundation of reliable iteration in production ML systems.")
    elif has_torch:
        matters.append("This pattern is common in production PyTorch code and forms a building block for larger architectures.")
    elif has_numpy:
        matters.append("Understanding the underlying numerical operations helps build intuition for how the model processes data.")
    elif has_class:
        matters.append("This modular design makes it straightforward to compose larger systems from smaller, well-tested components.")
    else:
        matters.append("Tracing through each step builds the intuition needed when debugging or extending similar systems.")

    return f"{desc} {notices[0]} {matters[0]}"

def find_preceding_paragraph(content, pos):
    """Find the <p>...</p> block that precedes the given position."""
    before = content[:pos]
    # Look for the last </p> before this position
    last_p_end = before.rfind('</p>')
    if last_p_end == -1:
        return None, None, None

    # Find the start of this <p>
    p_start = before.rfind('<p>', 0, last_p_end)
    if p_start == -1:
        p_start = before.rfind('<p ', 0, last_p_end)
    if p_start == -1:
        return None, None, None

    p_text = content[p_start:last_p_end + 4]
    return p_start, last_p_end + 4, p_text

def paragraph_references_code(p_text, fragment_num):
    """Check if the paragraph references the upcoming code block."""
    if p_text is None:
        return True  # Can't add reference if there's no paragraph

    plain = re.sub(r'<[^>]+>', '', p_text).lower()
    reference_keywords = [
        'following', 'below', 'code fragment', 'snippet', 'implementation',
        'code block', 'listing', 'example shows', 'example demonstrates',
        'illustrated by', 'shown in', 'see the code', 'the code', 'we implement',
        'consider the following', 'here we', 'this code', 'next code',
        'code example', 'demonstrates how'
    ]
    return any(kw in plain for kw in reference_keywords)

def add_prose_reference(p_text, fragment_num):
    """Add a prose reference sentence at the end of the paragraph."""
    # Insert before the closing </p>
    insertion = f" Code Fragment {fragment_num} below puts this into practice."
    return p_text[:-4] + insertion + "</p>"

def process_file(filepath):
    """Process a single HTML file using multi-pass approach for safety."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    pre_pattern = re.compile(r'<pre[^>]*>(.*?)</pre>', re.DOTALL)

    # === PRE-PASS: Remove duplicate <p class="code-caption"> tags ===
    # Some appendix files have both <div class="code-caption"> and <p class="code-caption">
    # Remove the <p> versions when a <div> already exists nearby
    content = re.sub(r'\n*<p class="code-caption">Code Fragment [A-Z]\.\d+:.*?</p>', '', content)

    # Count blocks
    matches = list(pre_pattern.finditer(content))
    if not matches:
        return 0, 0, 0, 0

    num_blocks = len(matches)
    captions_fixed = 0
    comments_added = 0
    refs_added = 0

    # === PASS 1: Fix/add captions (update existing in-place, or add after </pre>) ===
    # Re-parse after each edit to avoid stale positions
    for frag_idx in range(num_blocks):
        fragment_num = frag_idx + 1
        matches = list(pre_pattern.finditer(content))
        if frag_idx >= len(matches):
            break
        match = matches[frag_idx]
        pre_start = match.start()
        pre_end = match.end()
        code_content = match.group(1)

        # Check for existing caption BEFORE the <pre>
        caption_before = has_caption_before_pre(content, pre_start)
        caption_after = has_caption_after_pre(content, pre_end)

        if caption_before:
            search_start = max(0, pre_start - 500)
            search_zone = content[search_start:pre_start]
            cap_match = re.search(r'(<div class="code-caption">)(.*?)(</div>)', search_zone, re.DOTALL)
            if cap_match:
                cap_full_start = search_start + cap_match.start()
                cap_full_end = search_start + cap_match.end()
                existing_caption = cap_match.group(2).strip()

                if not caption_has_fragment_label(existing_caption):
                    if is_caption_too_short(existing_caption):
                        new_caption_text = generate_caption_text(code_content, fragment_num)
                        new_caption = f'<div class="code-caption"><strong>Code Fragment {fragment_num}:</strong> {new_caption_text}</div>'
                    else:
                        cleaned = re.sub(r'^<strong>[^<]*</strong>\s*', '', existing_caption)
                        new_caption = f'<div class="code-caption"><strong>Code Fragment {fragment_num}:</strong> {cleaned}</div>'
                    content = content[:cap_full_start] + new_caption + content[cap_full_end:]
                    captions_fixed += 1

        elif caption_after:
            after_zone = content[pre_end:pre_end + 500]
            cap_match = re.search(r'(<div class="code-caption">)(.*?)(</div>)', after_zone, re.DOTALL)
            if cap_match:
                cap_full_start = pre_end + cap_match.start()
                cap_full_end = pre_end + cap_match.end()
                existing_caption = cap_match.group(2).strip()

                if not caption_has_fragment_label(existing_caption):
                    if is_caption_too_short(existing_caption):
                        new_caption_text = generate_caption_text(code_content, fragment_num)
                        new_caption = f'<div class="code-caption"><strong>Code Fragment {fragment_num}:</strong> {new_caption_text}</div>'
                    else:
                        cleaned = re.sub(r'^<strong>[^<]*</strong>\s*', '', existing_caption)
                        new_caption = f'<div class="code-caption"><strong>Code Fragment {fragment_num}:</strong> {cleaned}</div>'
                    content = content[:cap_full_start] + new_caption + content[cap_full_end:]
                    captions_fixed += 1
        else:
            # No caption, add after </pre>
            new_caption_text = generate_caption_text(code_content, fragment_num)
            new_caption = f'\n<div class="code-caption"><strong>Code Fragment {fragment_num}:</strong> {new_caption_text}</div>'
            content = content[:pre_end] + new_caption + content[pre_end:]
            captions_fixed += 1

    # === PASS 2: Add opening comments inside <pre> blocks ===
    # Process in reverse order to preserve positions
    matches = list(pre_pattern.finditer(content))
    for i in range(len(matches) - 1, -1, -1):
        match = matches[i]
        pre_start = match.start()
        code_content = match.group(1)
        lang = detect_language(code_content)

        if not has_opening_comments(code_content, lang):
            comment_text = generate_comment_for_code(code_content, lang)

            # Find insert position right after <pre> or <pre><code>
            pre_tag_match = re.match(r'(<pre[^>]*>)(\s*<code>)?', content[pre_start:pre_start + 50])
            if pre_tag_match:
                insert_pos = pre_start + pre_tag_match.end()
                # Ensure newline before comment
                if insert_pos < len(content) and content[insert_pos] != '\n':
                    comment_text = '\n' + comment_text
                content = content[:insert_pos] + comment_text + content[insert_pos:]
                comments_added += 1

    # === PASS 3: Add prose references before code blocks ===
    matches = list(pre_pattern.finditer(content))
    # Process in reverse to preserve positions
    for i in range(len(matches) - 1, -1, -1):
        fragment_num = i + 1
        match = matches[i]
        pre_start = match.start()

        # Find where to look: before caption if it exists, else before <pre>
        look_before = pre_start
        search_zone_before = content[max(0, pre_start - 600):pre_start]
        cap_in_before = re.search(r'<div class="code-caption">.*?</div>', search_zone_before, re.DOTALL)
        if cap_in_before:
            look_before = max(0, pre_start - 600) + cap_in_before.start()

        p_start, p_end, p_text = find_preceding_paragraph(content, look_before)

        if p_text and not paragraph_references_code(p_text, fragment_num):
            new_p = add_prose_reference(p_text, fragment_num)
            content = content[:p_start] + new_p + content[p_end:]
            refs_added += 1

    # Only write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return num_blocks, captions_fixed, comments_added, refs_added


# Process all files
print(f"Processing {len(files)} files...\n")
total_blocks = 0
total_captions = 0
total_comments = 0
total_refs = 0

for filepath in files:
    short_name = os.path.relpath(filepath, "E:/Projects/LLMCourse")
    blocks, captions, comments, refs = process_file(filepath)
    total_blocks += blocks
    total_captions += captions
    total_comments += comments
    total_refs += refs
    if blocks > 0:
        print(f"{short_name}: {blocks} code blocks, {captions} captions fixed, {comments} comments added, {refs} refs added")
    else:
        print(f"{short_name}: no code blocks")

print(f"\n=== TOTALS ===")
print(f"Files processed: {len(files)}")
print(f"Code blocks found: {total_blocks}")
print(f"Captions fixed/added: {total_captions}")
print(f"Comments added: {total_comments}")
print(f"Prose references added: {total_refs}")
