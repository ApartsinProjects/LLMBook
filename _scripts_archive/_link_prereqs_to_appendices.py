"""
Sweep all chapter index.html files and add hyperlinks in <div class="prereqs">
blocks to relevant appendix sections where appropriate.

Idempotent: skips items where the keyword is already inside an <a> tag.
"""
import re
import os
import glob

BASE = r"E:\Projects\LLMCourse"

# All module index files
index_files = sorted(glob.glob(os.path.join(BASE, "part-*", "module-*", "index.html")))

def rel_to_root(filepath):
    rel = os.path.relpath(filepath, BASE)
    depth = rel.count(os.sep)
    return "../" * depth

# Appendix targets (relative to project root)
APPENDIX_A1 = "appendices/appendix-a-mathematical-foundations/section-a.1.html"
APPENDIX_A2 = "appendices/appendix-a-mathematical-foundations/section-a.2.html"
APPENDIX_A3 = "appendices/appendix-a-mathematical-foundations/section-a.3.html"
APPENDIX_A4 = "appendices/appendix-a-mathematical-foundations/section-a.4.html"
APPENDIX_A5 = "appendices/appendix-a-mathematical-foundations/section-a.5.html"
APPENDIX_B1 = "appendices/appendix-b-ml-essentials/section-b.1.html"
APPENDIX_B2 = "appendices/appendix-b-ml-essentials/section-b.2.html"
APPENDIX_B3 = "appendices/appendix-b-ml-essentials/section-b.3.html"
APPENDIX_B4 = "appendices/appendix-b-ml-essentials/section-b.4.html"
APPENDIX_C  = "appendices/appendix-c-python-for-llm/index.html"
APPENDIX_D  = "appendices/appendix-d-environment-setup/index.html"
APPENDIX_G  = "appendices/appendix-g-hardware-compute/index.html"
APPENDIX_J  = "appendices/appendix-j-datasets-benchmarks/index.html"

def make_link(prefix, target, text):
    return f'<a href="{prefix}{target}">{text}</a>'

def strip_tags(html):
    """Return text with all HTML tags removed."""
    return re.sub(r'<[^>]+>', '', html)

def text_in_a_tag(li_html, keyword):
    """Check if keyword appears inside an <a>...</a> in this li."""
    for m in re.finditer(r'<a\b[^>]*>(.*?)</a>', li_html, re.DOTALL):
        if keyword.lower() in m.group(1).lower():
            return True
    return False

def text_outside_tags(li_html):
    """Get the text that is NOT inside any tag attribute or <a>...</a> content.
    This is a simplified check: we strip <a>...</a> completely, then strip remaining tags."""
    # Remove <a>...</a> blocks entirely
    stripped = re.sub(r'<a\b[^>]*>.*?</a>', '', li_html, flags=re.DOTALL)
    # Remove remaining tags
    stripped = re.sub(r'<[^>]+>', '', stripped)
    return stripped

def apply_sub_outside_links(li_html, pattern, replacement_fn):
    """Apply a regex substitution only on text outside <a> tags.
    Split the li into segments: (outside-a, inside-a, outside-a, ...).
    Only apply the pattern to outside-a segments."""

    # Split by <a ...>...</a>
    parts = re.split(r'(<a\b[^>]*>.*?</a>)', li_html, flags=re.DOTALL)
    changed = False
    result_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            # This is an <a>...</a> block, leave it alone
            result_parts.append(part)
        else:
            new_part, n = re.subn(pattern, replacement_fn, part, count=1)
            if n > 0:
                changed = True
            result_parts.append(new_part)
    return ''.join(result_parts), changed


# Each rule: (check_keyword_in_plain_text, regex_pattern, replacement_fn_factory)
# check_keyword: if this keyword already appears in an <a> tag, skip the rule
# regex_pattern: applied only to text outside <a> tags
# replacement_fn_factory: takes prefix, returns a lambda for re.sub

def build_rules(prefix):
    """Build rules with the given prefix baked in."""
    rules = []

    # Linear algebra
    rules.append({
        "skip_if_linked": "linear algebra",
        "pattern": r'\b([Bb]asic\s+)?[Ll]inear [Aa]lgebra\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A1, m.group(0)),
    })

    # "Basic probability and information theory" (combined, must be before individual rules)
    rules.append({
        "skip_if_linked": "probability",
        "pattern": r'\b[Bb]asic\s+[Pp]robability\s+and\s+[Ii]nformation\s+[Tt]heory\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A2, "basic probability") + " and " + make_link(prefix, APPENDIX_A5, "information theory"),
    })

    # "probability and information theory" (combined)
    rules.append({
        "skip_if_linked": "probability",
        "pattern": r'\b[Pp]robability\s+and\s+[Ii]nformation\s+[Tt]heory\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A2, "probability") + " and " + make_link(prefix, APPENDIX_A5, "information theory"),
    })

    # "basic probability and statistics"
    rules.append({
        "skip_if_linked": "probability",
        "pattern": r'\b[Bb]asic\s+[Pp]robability\s+and\s+[Ss]tatistics\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A2, m.group(0)),
    })

    # "Basic probability" (standalone)
    rules.append({
        "skip_if_linked": "probability",
        "pattern": r'\b[Bb]asic\s+[Pp]robability\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A2, m.group(0)),
    })

    # Probability (standalone, only if clearly a prereq)
    rules.append({
        "skip_if_linked": "probability",
        "pattern": r'\b[Pp]robability\s+[Tt]heory\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A2, m.group(0)),
    })

    # Cross-entropy, perplexity => information theory
    rules.append({
        "skip_if_linked": "cross-entropy",
        "pattern": r'\bcross-entropy,?\s*perplexity\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A5, m.group(0)),
    })

    # Information theory (standalone)
    rules.append({
        "skip_if_linked": "information theory",
        "pattern": r'\b[Ii]nformation\s+[Tt]heory\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A5, m.group(0)),
    })

    # Basic calculus
    rules.append({
        "skip_if_linked": "calculus",
        "pattern": r'\b[Bb]asic\s+[Cc]alculus\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A3, m.group(0)),
    })

    # Optimization fundamentals
    rules.append({
        "skip_if_linked": "optimization",
        "pattern": r'\b[Oo]ptimization\s+[Ff]undamentals\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A4, m.group(0)),
    })

    # Gradient descent
    rules.append({
        "skip_if_linked": "gradient descent",
        "pattern": r'\b[Gg]radient\s+[Dd]escent\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A4, m.group(0)),
    })

    # Loss functions
    rules.append({
        "skip_if_linked": "loss function",
        "pattern": r'\b[Ll]oss\s+[Ff]unctions?\b',
        "replace": lambda m: make_link(prefix, APPENDIX_B3, m.group(0)),
    })

    # Python proficiency / programming / experience
    rules.append({
        "skip_if_linked": "python",
        "pattern": r'\bPython\s+proficiency\b',
        "replace": lambda m: make_link(prefix, APPENDIX_C, m.group(0)),
    })
    rules.append({
        "skip_if_linked": "python",
        "pattern": r'\bPython\s+programming\b',
        "replace": lambda m: make_link(prefix, APPENDIX_C, m.group(0)),
    })
    rules.append({
        "skip_if_linked": "python",
        "pattern": r'\bPython\s+experience\b',
        "replace": lambda m: make_link(prefix, APPENDIX_C, m.group(0)),
    })
    # "Comfort with Python" / "Familiarity with Python" (standalone, not followed by "libraries" etc)
    rules.append({
        "skip_if_linked": "python",
        "pattern": r'\b(Comfort|Familiarity)\s+with\s+Python\b(?!\s+(?:libraries|APIs|tools|code))',
        "replace": lambda m: m.group(1) + " with " + make_link(prefix, APPENDIX_C, "Python"),
    })
    # "Basic familiarity with Python"
    rules.append({
        "skip_if_linked": "python",
        "pattern": r'\b[Bb]asic\s+familiarity\s+with\s+Python\b',
        "replace": lambda m: "basic familiarity with " + make_link(prefix, APPENDIX_C, "Python"),
    })
    # "Comfortable with Python"
    rules.append({
        "skip_if_linked": "python",
        "pattern": r'\b[Cc]omfortable\s+with\s+Python\b',
        "replace": lambda m: "comfortable with " + make_link(prefix, APPENDIX_C, "Python"),
    })

    # GPU access / GPU hardware
    rules.append({
        "skip_if_linked": "gpu",
        "pattern": r'\bGPU\s+[Aa]ccess\b',
        "replace": lambda m: make_link(prefix, APPENDIX_G, m.group(0)),
    })
    rules.append({
        "skip_if_linked": "gpu",
        "pattern": r'\bGPU\s+[Hh]ardware\b',
        "replace": lambda m: make_link(prefix, APPENDIX_G, m.group(0)),
    })
    rules.append({
        "skip_if_linked": "gpu",
        "pattern": r'\bGPU\s+[Mm]emory\s+[Cc]oncepts\b',
        "replace": lambda m: make_link(prefix, APPENDIX_G, m.group(0)),
    })
    rules.append({
        "skip_if_linked": "gpu",
        "pattern": r'\bGPU\s+[Mm]emory\s+[Hh]ierarchy\b',
        "replace": lambda m: make_link(prefix, APPENDIX_G, m.group(0)),
    })
    # "probability distributions" (standalone in prereqs)
    rules.append({
        "skip_if_linked": "probability",
        "pattern": r'\bprobability\s+distributions\b',
        "replace": lambda m: make_link(prefix, APPENDIX_A2, m.group(0)),
    })

    # Understanding of neural networks
    rules.append({
        "skip_if_linked": "neural network",
        "pattern": r'\b[Uu]nderstanding\s+of\s+[Nn]eural\s+[Nn]etworks\b',
        "replace": lambda m: "understanding of " + make_link(prefix, APPENDIX_B2, "neural networks"),
    })
    rules.append({
        "skip_if_linked": "neural network",
        "pattern": r'\b[Bb]asic\s+[Nn]eural\s+[Nn]etwork\s+[Cc]oncepts?\b',
        "replace": lambda m: "basic " + make_link(prefix, APPENDIX_B2, "neural network concepts"),
    })

    # Basic machine learning concepts / ML fundamentals
    rules.append({
        "skip_if_linked": "machine learning",
        "pattern": r'\b[Bb]asic\s+[Mm]achine\s+[Ll]earning\s+[Cc]oncepts?\b',
        "replace": lambda m: "basic " + make_link(prefix, APPENDIX_B1, "machine learning concepts"),
    })
    rules.append({
        "skip_if_linked": "ml fundamentals",
        "pattern": r'\bML\s+[Ff]undamentals\b',
        "replace": lambda m: make_link(prefix, APPENDIX_B1, m.group(0)),
    })

    # Evaluation metrics
    rules.append({
        "skip_if_linked": "evaluation metric",
        "pattern": r'\b[Ee]valuation\s+[Mm]etrics\b',
        "replace": lambda m: make_link(prefix, APPENDIX_B4, m.group(0)),
    })

    # Training loops (link to appendix B3 training)
    rules.append({
        "skip_if_linked": "training loop",
        "pattern": r'\b[Bb]asic\s+[Tt]raining\s+[Ll]oops?\b',
        "replace": lambda m: make_link(prefix, APPENDIX_B3, m.group(0)),
    })

    return rules


def process_prereqs_block(prereqs_html, prefix):
    """Process the prereqs HTML block and add links."""
    changed = False
    rules = build_rules(prefix)

    # Process each <li> separately
    def process_li(li_match):
        nonlocal changed
        li_html = li_match.group(0)

        for rule in rules:
            skip_kw = rule["skip_if_linked"]

            # Skip if keyword is already inside an <a> tag in this <li>
            if text_in_a_tag(li_html, skip_kw):
                continue

            # Check if pattern exists in text outside <a> tags
            outside = text_outside_tags(li_html)
            if not re.search(rule["pattern"], outside):
                continue

            # Apply substitution only outside <a> tags
            new_li, did_change = apply_sub_outside_links(li_html, rule["pattern"], rule["replace"])
            if did_change:
                li_html = new_li
                changed = True

        return li_html

    result = re.sub(r'<li>.*?</li>', process_li, prereqs_html, flags=re.DOTALL)
    return result, changed


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    prereqs_match = re.search(r'(<div class="prereqs">.*?</div>)', content, re.DOTALL)
    if not prereqs_match:
        return False, []

    prereqs_html = prereqs_match.group(1)
    prefix = rel_to_root(filepath)

    new_prereqs, changed = process_prereqs_block(prereqs_html, prefix)

    if changed:
        new_content = content[:prereqs_match.start(1)] + new_prereqs + content[prereqs_match.end(1):]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # Report what links were added
        old_links = set(re.findall(r'href="([^"]*appendix[^"]*)"', prereqs_html))
        new_links = set(re.findall(r'href="([^"]*appendix[^"]*)"', new_prereqs))
        added = new_links - old_links
        return True, sorted(added)
    return False, []


total_changed = 0
all_links_added = []

for filepath in index_files:
    filepath_display = os.path.relpath(filepath, BASE)
    was_changed, links_added = process_file(filepath)
    if was_changed:
        total_changed += 1
        print(f"  UPDATED: {filepath_display}")
        for link in links_added:
            print(f"    + {link}")
        all_links_added.extend(links_added)
    else:
        print(f"  (no change): {filepath_display}")

print(f"\nTotal files updated: {total_changed}")
print(f"Total new appendix links added: {len(all_links_added)}")
