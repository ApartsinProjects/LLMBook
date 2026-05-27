"""Cycle 11: Deep technique discovery (target 400-500 named entities).

Strategy:
  1. Scan every section-*.html across the book root.
  2. Discover candidates from 4 sources:
       (a) every h2/h3/h4 title (extracted leading name token, NOT a generic phrase)
       (b) every <strong>NAME</strong> matching capitalized identifier pattern
       (c) every <dt>NAME</dt> term in glossary-like definition lists
       (d) every figure / table / code caption that names a technique
       (e) every bibliography entry's leading capitalized name (heuristic title parse)
  3. Track per-candidate: distinct files, count of h2/h3/h4/dt title hits, sources.
  4. Apply blocklist of generic English phrases (extends cycle-10 list).
  5. Apply alias normalization (case + hyphen/space stripped).
  6. Require at least 2 distinct files AND >=1 hit in an h2/h3/h4/dt/figure caption
     (i.e., something more structural than just a body <strong>).
  7. Merge with the 252-technique cycle-10 inventory.
  8. Save to _techniques_500.json (target 400-500 entries).
  9. If exceeds 600, tighten thresholds; if below 350, loosen.

Output schema per technique:
  {
    "name": "AttentionMechanism",
    "aliases": ["MHA", "Multi-Head Attention"],
    "regex": "...",
    "first_mention_file": "...",
    "n_sections_appearing": 47,
    "n_h2_h3_h4_titles": 8,
    "category": "attention",
    "discovered_via": "h3-title|strong|dt|caption|bibliography|inherited"
  }
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from _pedagogy_audit_v2 import parse_sections
from _discover_techniques import (
    EXPANSION_CANDIDATES,
    category_for,
    normalize,
    CURATED_TECHNIQUES,
)

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
EXCLUDE_DIRS = {'_downloads', 'node_modules', '.book-update',
                'source_fix_backups', '_archive', 'KDP', 'slide-summaries',
                'agents', '.git', 'kdp', 'temp_epub', 'vendor', 'templates',
                'pagefind', '_concept-figs', 'capstone',
                'generated-images', 'images', '__pycache__'}

OUT = ROOT / 'slide-summaries' / '_techniques_500.json'

# Extended blocklist for cycle 11
BLOCKLIST = {
    # generic doc/structure terms
    'figure', 'figures', 'table', 'tables', 'algorithm', 'algorithms',
    'example', 'examples', 'definition', 'definitions', 'theorem', 'lemma',
    'proof', 'proofs', 'note', 'notes', 'tip', 'tips', 'warning', 'warnings',
    'remark', 'remarks', 'exercise', 'exercises', 'lab', 'labs',
    'summary', 'summaries', 'overview', 'introduction', 'background', 'context',
    'references', 'reference', 'bibliography', 'appendix', 'chapter', 'section',
    'sections', 'part', 'parts', 'preface', 'foreword', 'conclusion', 'glossary',
    'index', 'recipe', 'recipes', 'cookbook', 'checklist', 'template', 'templates',
    'putting', 'key', 'what', 'why', 'how', 'when', 'where', 'who', 'which',
    'common', 'standard', 'basic', 'simple', 'classic', 'modern',
    'general', 'specific', 'practical', 'theoretical', 'core',
    'main', 'next', 'previous', 'first', 'second', 'third', 'fourth', 'fifth',
    'fundamental', 'fundamentals', 'advanced', 'beginner', 'expert', 'intermediate',
    'apparatus', 'further', 'official', 'recommended', 'optional', 'required',
    'a', 'an', 'the', 'in', 'on', 'with', 'and', 'or', 'is', 'are',
    'pre', 'post', 'mini', 'meta', 'multi', 'cross', 'inter', 'sub', 'super',
    'prerequisites', 'objective', 'objectives', 'step', 'steps', 'setup',
    'expected', 'stretch', 'extension', 'extensions', 'comparing',
    'foundational', 'building', 'tools', 'tooling', 'benchmarks',
    'cost', 'costs', 'surveys', 'observability', 'choosing', 'communities',
    'comparison', 'comparisons', 'audio', 'video',
    'evaluation', 'evaluations', 'task', 'tasks', 'problem', 'problems',
    'goal', 'goals', 'method', 'methods', 'approach', 'approaches',
    'pipeline', 'pipelines', 'training', 'inference', 'serving', 'deployment',
    'production', 'model', 'models', 'dataset', 'datasets',
    'application', 'applications', 'use', 'uses', 'using', 'choose', 'pick',
    'guide', 'guides', 'tutorial', 'tutorials', 'tier', 'tiers',
    'level', 'levels', 'walkthrough', 'demo', 'demos', 'reading', 'readings',
    'additional', 'related', 'similar', 'other', 'others',
    'notation', 'symbols', 'units', 'conventions',
    'history', 'origin', 'origins', 'motivation', 'motivations', 'rationale',
    'limitation', 'limitations', 'trade', 'tradeoff', 'tradeoffs',
    'pros', 'cons', 'advantages', 'disadvantages', 'benefits',
    'caveat', 'caveats', 'pitfall', 'pitfalls', 'gotcha', 'gotchas',
    'output', 'outputs', 'input', 'inputs',
    'concept', 'concepts', 'idea', 'ideas', 'principle', 'principles',
    'rule', 'rules', 'policy', 'policies', 'guideline', 'guidelines',
    'experiment', 'experiments', 'result', 'results', 'analysis', 'analyses',
    'discussion', 'discussions',
    'big', 'small', 'large', 'huge', 'tiny',
    'real', 'fake', 'true', 'false', 'good', 'bad', 'better', 'best', 'worse', 'worst',
    'this', 'these', 'those', 'each', 'every', 'all', 'some',
    'no', 'none', 'any', 'both', 'either', 'neither',
    'numerical', 'analytical', 'empirical', 'experimental',
    'visual', 'visualizing', 'visualization', 'visualizations',
    'understanding', 'learning', 'thinking', 'reasoning',
    'managing', 'controlling', 'measuring', 'monitoring', 'tracking',
    'optimizing', 'tuning', 'configuring', 'scaling',
    'data', 'code', 'text', 'image', 'images',
    'sample', 'samples', 'batch', 'batches', 'token', 'tokens',
    'layer', 'layers', 'block', 'blocks', 'module', 'modules',
    'class', 'classes', 'function', 'functions',
    'object', 'objects', 'instance', 'instances',
    'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'one', 'zero', 'half',
    # author/byline noise from bib entries
    'authors', 'author', 'editor', 'editors', 'volume', 'issue', 'pages',
    'proceedings', 'journal', 'paper', 'papers', 'preprint',
    # case-study labels
    'case', 'study', 'studies', 'scenario', 'scenarios',
    # vague verbs as titles
    'introducing', 'introduce', 'building', 'designing', 'creating',
    'measuring', 'evaluating', 'comparing', 'choosing', 'selecting',
    'deploying', 'monitoring', 'debugging', 'testing',
    'mathematical', 'statistical', 'computational',
    # numbers / dates only
    'q1', 'q2', 'q3', 'q4', 'h1', 'h2',
    # commonly-emphasized but generic
    'reader', 'readers', 'practitioner', 'practitioners', 'engineer', 'engineers',
    'developer', 'developers', 'scientist', 'scientists', 'user', 'users',
    # editorial scaffolding words
    'comes', 'takeaway', 'takeaways', 'self', 'check', 'practiced', 'practice',
    'canonical', 'external', 'internal', 'inside', 'outside',
    'frontier', 'frontiers', 'failure', 'failures', 'mitigation', 'mitigations',
    'considerations', 'documented', 'foundational', 'international',
    'official', 'documentation', 'research', 'recommendation', 'recommendations',
    'practices', 'modes', 'strategies', 'strategy', 'official',
    'production', 'consideration', 'governance', 'compliance',
    'safety', 'security', 'privacy', 'ethics', 'fairness',
    'architecture', 'architectures', 'implementation', 'implementations',
    'comparison', 'comparisons', 'tradeoff', 'tradeoffs',
    'integration', 'integrations', 'orchestration',
    'common', 'uncommon', 'rare',
    'inputs', 'outputs', 'parameter', 'parameters', 'hyperparameter', 'hyperparameters',
    'metric', 'metrics', 'measurement', 'measurements',
    'evaluation', 'evaluations', 'assessment', 'assessments',
    'workflow', 'workflows', 'pipeline', 'pipelines',
    'system', 'systems', 'service', 'services', 'platform', 'platforms',
    'framework', 'frameworks', 'library', 'libraries',
    'feature', 'features', 'capability', 'capabilities',
    'lifecycle', 'lifecycles',
    'roadmap', 'milestone', 'milestones',
    'review', 'reviews', 'audit', 'audits',
    'plan', 'plans', 'planning',
    'team', 'teams', 'organization', 'organizations',
    'budget', 'budgets',
    'lesson', 'lessons',
}

# Acronyms to NEVER promote
ACRONYM_BLOCKLIST = {
    'LLM', 'LLMS', 'RAG', 'PEFT', 'GPU', 'CPU', 'API', 'APIs', 'SDK', 'CLI', 'GUI', 'TPU',
    'MLM', 'NLP', 'ML', 'AI', 'NN', 'SQL', 'JSON', 'YAML', 'HTML', 'CSS',
    'FFT', 'STFT', 'DTW', 'FIR', 'IIR', 'DSP', 'PSU', 'RAM', 'SSD',
    'TOC', 'PDF', 'EPUB', 'KDP', 'OS', 'IO', 'IDE', 'VM', 'CI', 'CD',
    'HTTP', 'HTTPS', 'URL', 'URI', 'IP', 'TCP', 'UDP', 'DNS',
    'TODO', 'FAQ', 'AI/ML', 'ETL', 'ELT',
    'UI', 'UX', 'PM', 'CTO', 'CEO', 'CFO', 'KPI', 'OKR', 'ROI',
    'PR', 'PRs', 'QA',
}

# Names that need CASE-SENSITIVE matching
CASE_SENSITIVE = {
    'SuRe', 'Eagle', 'Falcon', 'Idefics', 'Pixtral', 'Molmo', 'Cambrian',
    'Tortoise', 'Voicebox', 'Llasa', 'Aider', 'Devin', 'OpenHands',
    'Marlin', 'Medusa', 'FLARE', 'CRAG', 'NPO', 'IPO', 'ORM', 'PRM',
    'PAL', 'PoT', 'KTO', 'ORPO', 'SimPO', 'BGE', 'GTE', 'E5',
    'MATH', 'GPQA', 'BBH', 'Bark', 'AGIEval', 'RA-DIT',
    'Best-of-N', 'Self-Refine', 'Self-RAG', 'OpenAI Swarm',
}


def is_in_skip_path(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & EXCLUDE_DIRS)


def looks_like_technique(name: str) -> bool:
    """Heuristic: must look like a model/algorithm name."""
    if not name or len(name) <= 2 or len(name) > 60:
        return False
    n_clean = name.strip().rstrip(':,.;')
    if n_clean.lower() in BLOCKLIST:
        return False
    if n_clean in ACRONYM_BLOCKLIST or n_clean.upper() in ACRONYM_BLOCKLIST:
        return False
    words = re.split(r'[-/\s]', n_clean)
    if not words:
        return False
    # Reject if EVERY word is in blocklist
    if all(w.lower() in BLOCKLIST for w in words if w):
        return False
    # Reject generic "X N" labels
    if re.fullmatch(r'(?:Pattern|Phase|Stage|Step|Tier|Level|Part|Chapter|Module|Section|Wave|Round|Cycle)\s+\d+', n_clean):
        return False
    # Strong signal: contains a digit (e.g., GPT-4, Llama-3.1, NF4)
    if re.search(r'\d', n_clean):
        return True
    # Strong signal: hyphen with at least one all-caps token
    if '-' in n_clean and any(re.fullmatch(r'[A-Z]{2,}', w) for w in words):
        return True
    # Strong signal: any token is an acronym (all-caps, 2-8 letters)
    for w in words:
        if re.fullmatch(r'[A-Z]{2,8}', w) and w not in ACRONYM_BLOCKLIST:
            return True
    # CamelCase pattern (e.g., LlamaIndex, BERTopic, FastText)
    if re.fullmatch(r'[A-Z][a-z]+(?:[A-Z][a-z]+){1,}', n_clean):
        return True
    # Multi-token Proper Nouns: only accept if contains a distinctive token
    # (a known org/model prefix, or all-caps word, or year-like number).
    # This rejects generic capitalized phrases like "Synthetic Data" or "Reward Hacking".
    KNOWN_PROPER_PREFIXES = {
        'openai', 'anthropic', 'google', 'meta', 'mistral', 'cohere',
        'nvidia', 'microsoft', 'amazon', 'apple', 'huggingface', 'hugging',
        'deepmind', 'stability', 'tencent', 'baidu', 'alibaba',
        'databricks', 'snowflake', 'pinecone', 'weaviate', 'chroma',
        'langchain', 'llamaindex', 'haystack',
    }
    if len(words) >= 2 and all(re.fullmatch(r'[A-Z][a-zA-Z]+', w) or w.lower() in ('of', 'the', 'and', 'for', 'in') for w in words):
        non_glue = [w for w in words if w.lower() not in ('of', 'the', 'and', 'for', 'in')]
        if len(non_glue) >= 2:
            # Require at least one token to be a known proper prefix OR all-caps
            distinctive = any(
                w.lower() in KNOWN_PROPER_PREFIXES or re.fullmatch(r'[A-Z]{2,}', w)
                for w in non_glue
            )
            if distinctive:
                return True
    # Reject everything else
    return False


def extract_title_name(title: str) -> str | None:
    """Extract the leading technique-like name from a section title."""
    # Strip numeric prefix like "27.1.3.2 "
    t = re.sub(r'^\d+(\.\d+)*\.?\s+', '', title).strip()
    if not t:
        return None
    # Pattern 1: starts with TechniqueName: ...
    m = re.match(r'^([A-Z][A-Za-z0-9][\w\-\./]*(?:\s+[A-Z][A-Za-z0-9][\w\-\./]*){0,4})\s*[:\(]', t)
    if m:
        return m.group(1).strip()
    # Pattern 2: title IS the technique name
    m = re.fullmatch(r'([A-Z][A-Za-z0-9][\w\-\./]*(?:\s+[A-Z][A-Za-z0-9][\w\-\./]*){0,4})\s*\??', t)
    if m:
        return m.group(1).strip()
    # Pattern 3: leading capitalized run
    m = re.match(r'^([A-Z][A-Za-z0-9][\w\-\./]*(?:\s+[A-Z][A-Za-z0-9][\w\-\./]*){0,3})', t)
    if m:
        return m.group(1).strip()
    return None


def main():
    # Collect all section files
    section_files = []
    for path in ROOT.rglob('section-*.html'):
        if is_in_skip_path(path):
            continue
        section_files.append(path)
    # Also include index pages (chapters/parts) that might have h2 titles
    print(f'Scanning {len(section_files)} section files.')

    # Regex helpers
    strong_re = re.compile(
        r'<strong>\s*([A-Z][A-Za-z0-9\-\.]+(?:[- /][A-Z0-9][A-Za-z0-9\-\.]*){0,3})\s*</strong>'
    )
    em_re = re.compile(
        r'<em>\s*([A-Z][A-Za-z0-9\-\.]+(?:[- /][A-Z0-9][A-Za-z0-9\-\.]*){0,3})\s*</em>'
    )
    dt_re = re.compile(r'<dt[^>]*>\s*([^<]+?)\s*</dt>', re.IGNORECASE)
    caption_re = re.compile(r'<(?:figcaption|caption)[^>]*>\s*([^<]+?)\s*</', re.IGNORECASE)
    bib_title_re = re.compile(r'class="bib-(?:entry-)?(?:title|card-title)"[^>]*>\s*([^<]+?)\s*<', re.IGNORECASE)

    # Aggregators: bucket-key (normalized) -> set of files, count of structural hits, spellings dict, categories
    bucket_files: dict[str, set[str]] = defaultdict(set)
    bucket_struct_hits: dict[str, int] = defaultdict(int)
    bucket_spellings: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    bucket_sources: dict[str, set[str]] = defaultdict(set)
    bucket_first_file: dict[str, str] = {}

    def record(candidate: str, file_path: str, source: str, is_structural: bool):
        if not looks_like_technique(candidate):
            return
        key = normalize(candidate)
        if not key or len(key) < 2:
            return
        bucket_files[key].add(file_path)
        if is_structural:
            bucket_struct_hits[key] += 1
        bucket_spellings[key][candidate] += 1
        bucket_sources[key].add(source)
        if key not in bucket_first_file:
            bucket_first_file[key] = file_path

    for path in section_files:
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        fp = str(path)

        # (a) h2/h3/h4 titles
        for m in re.finditer(r'<(h[234])\b[^>]*>(.*?)</\1>', html, re.DOTALL | re.IGNORECASE):
            tag = m.group(1).lower()
            title_raw = re.sub(r'<[^>]+>', '', m.group(2))
            title = re.sub(r'\s+', ' ', title_raw).strip()
            name = extract_title_name(title)
            if name:
                record(name, fp, f'{tag}-title', is_structural=True)

        # (b) <strong>
        for m in strong_re.finditer(html):
            record(m.group(1).strip(), fp, 'strong', is_structural=False)

        # (b2) <em>
        for m in em_re.finditer(html):
            record(m.group(1).strip(), fp, 'em', is_structural=False)

        # (c) <dt>
        for m in dt_re.finditer(html):
            term = m.group(1).strip()
            record(term, fp, 'dt', is_structural=True)

        # (d) figure / table captions
        for m in caption_re.finditer(html):
            txt = m.group(1).strip()
            # Try to extract leading capitalized name from caption
            name = extract_title_name(txt)
            if name:
                record(name, fp, 'caption', is_structural=True)

        # (e) bibliography titles - parse leading capitalized run
        for m in bib_title_re.finditer(html):
            txt = m.group(1).strip()
            name = extract_title_name(txt)
            if name:
                record(name, fp, 'bibliography', is_structural=True)

    print(f'Discovered raw candidates (normalized keys): {len(bucket_files)}')

    # Now filter
    discoveries = []
    for key, files in bucket_files.items():
        # Cycle 11 thresholds (looser to push toward 350-500):
        #   - Appears in 2+ files AND >=1 structural hit, OR
        #   - Appears in 1 file with >=1 structural hit (devoted h3/h4 section)
        # The structural-hit requirement ensures the candidate has a real section
        # somewhere; the 1-file allowance picks up techniques covered in a
        # single dedicated section (which is exactly what Tier C catalog
        # entries look like).
        if not ((len(files) >= 2 and bucket_struct_hits[key] >= 1) or
                (len(files) >= 1 and bucket_struct_hits[key] >= 1)):
            continue
        # Pick canonical spelling: most frequent
        spelling = max(bucket_spellings[key].items(), key=lambda kv: kv[1])[0]
        discoveries.append({
            'name': spelling,
            'aliases': sorted(set(bucket_spellings[key].keys()) - {spelling}),
            'regex': r'\b' + re.escape(spelling) + r'\b',
            'first_mention_file': '/'.join(bucket_first_file[key].replace('\\', '/').split('/')[-3:]),
            'n_sections_appearing': len(files),
            'n_h2_h3_h4_titles': bucket_struct_hits[key],
            'category': category_for(spelling),
            'discovered_via': '|'.join(sorted(bucket_sources[key])),
            'source': 'cycle11-deep-discovery',
        })

    # Merge with existing 252 inventory
    existing_inv = json.loads((ROOT / 'slide-summaries' / '_expanded_techniques.json').read_text(encoding='utf-8'))
    existing_norms = set()
    inherited = []
    for t in existing_inv['techniques']:
        nm = t['name']
        existing_norms.add(normalize(nm))
        # Also add curated regex hits to the alias set
        inherited.append({
            'name': nm,
            'aliases': [],
            'regex': t['regex'],
            'first_mention_file': '',
            'n_sections_appearing': 0,
            'n_h2_h3_h4_titles': 0,
            'category': t.get('category', 'tooling'),
            'discovered_via': 'inherited',
            'source': t.get('source', 'cycle10-inherited'),
            'weight': t.get('weight', 0.3),
        })

    # Also check inherited regex matches against discoveries to avoid alias duplication
    # by normalizing display name
    new_discoveries = []
    for d in discoveries:
        if normalize(d['name']) in existing_norms:
            # Already inherited; skip
            continue
        # Also check if any inherited regex matches this discovery's spelling
        matched = False
        for t in existing_inv['techniques']:
            try:
                if re.fullmatch(t['regex'], d['name']) or re.search(t['regex'], d['name'], re.IGNORECASE):
                    matched = True
                    break
            except re.error:
                continue
        if matched:
            continue
        new_discoveries.append(d)

    total_pool = inherited + new_discoveries

    # Auto-tune toward 400-500 target:
    if len(total_pool) > 500:
        # Sort new discoveries by quality, keep top ones to reach ~500
        new_discoveries.sort(key=lambda d: (
            -d['n_h2_h3_h4_titles'],
            -d['n_sections_appearing'],
            d['name'].lower(),
        ))
        target_new = 500 - len(inherited)
        if target_new < 0:
            target_new = 0
        if len(new_discoveries) > target_new:
            print(f'Total {len(total_pool)} exceeds 500; keeping top {target_new} of {len(new_discoveries)} new discoveries.')
            new_discoveries = new_discoveries[:target_new]
            total_pool = inherited + new_discoveries
    elif len(total_pool) < 350:
        print(f'Total {len(total_pool)} below 350; keeping all (this reflects the book\'s actual named-entity surface).')

    print(f'Inherited (cycle 10): {len(inherited)}')
    print(f'NEW deep discoveries kept: {len(new_discoveries)}')
    print(f'TOTAL: {len(total_pool)}')

    # Sort: inherited first, then new by n_sections desc
    new_discoveries.sort(key=lambda d: (-d['n_sections_appearing'], d['name'].lower()))
    final = inherited + new_discoveries

    OUT.write_text(
        json.dumps({
            'total': len(final),
            'inherited_count': len(inherited),
            'new_deep_count': len(new_discoveries),
            'techniques': final,
        }, indent=2),
        encoding='utf-8',
    )
    print(f'Saved {OUT}')
    print('\nTop 30 NEW deep discoveries:')
    for d in new_discoveries[:30]:
        print(f"  {d['name']:35s} n_files={d['n_sections_appearing']:3d}  n_struct={d['n_h2_h3_h4_titles']:2d}  via={d['discovered_via']:25s} cat={d['category']}")


if __name__ == '__main__':
    main()
