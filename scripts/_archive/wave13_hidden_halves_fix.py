"""Wave 13: fix the 3 chapters in Part 5 that are silently two chapters glued together.

  Ch 20 "Audio and Music Generation" → rename "Audio, Music, and Video Generation"
        Index lists 20.1-20.5 only; sections 20.6-20.10 (video) exist on disk
        with breadcrumbs still saying "Chapter 33: Video Generation".
  Ch 22 "Vision-Language Models" → rename "Vision-Language and Omni Models"
        Index lists 22.1-22.5 only; sections 22.6-22.9 (omni) exist on disk
        with breadcrumbs still saying "Chapter 37: Unified Multimodal and Omni Models".
  Ch 24 "Vision-Language-Action Models" → rename "VLA Models and LLM-Powered Robotics"
        Index lists 24.1-24.6 only; sections 24.7-24.13 (robotics) exist on disk
        with breadcrumbs still saying "Chapter 40: LLM-Powered Robotics".

For each chapter:
  1. Update index.html: rename h1 + page-title + meta description, expand sections-list
  2. For each second-half section file: fix breadcrumb to current chapter, fix
     pagefind-meta chapter, fix h2 visible numbering to match current section number
  3. Update part-5/index.html chapter-card title and section listing

Section content stays in place (sections 20.6 etc. still cover their topic).
The chapter is just acknowledged to span both topics.
"""
from pathlib import Path
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

CHAPTERS = [
    {
        'module': 'module-20-audio-music-generation',
        'ch_num': 20,
        'new_title': 'Audio, Music, and Video Generation',
        'old_title': 'Audio and Music Generation',
        'big_picture': 'Generative models for time-series media. The first half covers audio (text-to-speech with VITS/Bark/F5-TTS, voice cloning, music generation with MusicLM/MusicGen/Suno/Udio, audio editing, and ASR). The second half covers video (Diffusion Transformers, frontier video models Sora/Veo/Runway/Kling/Pika, camera and motion control, video editing, and long-form cinematic synthesis).',
        'second_half_old_chapter': 'Chapter 33',
        'second_half_old_topic': 'Video Generation',
        'section_titles': [
            (1, 'Text-to-Speech: VITS, Bark, and F5-TTS'),
            (2, 'Voice Cloning, Zero-Shot TTS, and Voice Conversion'),
            (3, 'Music Generation: MusicLM, MusicGen, Suno, and Udio'),
            (4, 'Audio Editing: Stems, Style Transfer, and Remixing'),
            (5, 'Speech Recognition for the Multimodal Stack'),
            (6, 'Video Diffusion Transformers (DiTs)'),
            (7, 'Leading Video Models: Sora, Veo, Runway, Kling, and Pika'),
            (8, 'Camera Control, Motion Control, and ControlNet for Video'),
            (9, 'Video Editing and Remixing'),
            (10, 'Long-Form and Cinematic Video Generation'),
        ],
        'second_half_start': 6,
    },
    {
        'module': 'module-22-vision-language-models',
        'ch_num': 22,
        'new_title': 'Vision-Language and Omni Models',
        'old_title': 'Vision-Language Models',
        'big_picture': 'How LLMs see. The first half covers vision-language models (ViT, CLIP/SigLIP contrastive learning, generative VLMs like LLaVA and Qwen-VL, frontier VLMs GPT-4V/Gemini/Claude Vision, multimodal benchmarks). The second half covers omni models (pipeline vs native multimodal, early vs late fusion, any-to-any generation, GPT-4o/Gemini/Llama-4-Omni/Chameleon).',
        'second_half_old_chapter': 'Chapter 37',
        'second_half_old_topic': 'Unified Multimodal and Omni Models',
        'section_titles': [
            (1, 'ViT and Visual Tokenization'),
            (2, 'Contrastive Vision-Language: CLIP and SigLIP'),
            (3, 'Generative VLMs: LLaVA, BLIP-3, Qwen-VL'),
            (4, 'Frontier VLMs: GPT-4V, Gemini, Claude Vision'),
            (5, 'Evaluating Multimodal Reasoning: MMMU and Saturation'),
            (6, 'Pipeline vs Native Multimodal'),
            (7, 'Early Fusion vs Late Fusion'),
            (8, 'Any-to-Any Generation'),
            (9, 'Frontier Omni Models: GPT-4o, Gemini, Llama-4-Omni, Chameleon'),
        ],
        'second_half_start': 6,
    },
    {
        'module': 'module-24-vla-models',
        'ch_num': 24,
        'new_title': 'VLA Models and LLM-Powered Robotics',
        'old_title': 'Vision-Language-Action Models',
        'big_picture': 'How LLMs act in the physical world. The first half covers Vision-Language-Action models (OpenVLA, Physical Intelligence pi-0, RT-2-X, and the VLA design space, comparisons, and limitations). The second half covers LLM-powered robotics: SayCan-style planning, Code-as-Policies, VoxPoser spatial reasoning, multi-robot dispatch, ROS 2 integration, planner comparison, and the sim-to-real gap.',
        'second_half_old_chapter': 'Chapter 40',
        'second_half_old_topic': 'LLM-Powered Robotics',
        'section_titles': [
            (1, 'VLA Architecture in One Equation'),
            (2, 'OpenVLA-7B Reference Implementation'),
            (3, 'Physical Intelligence pi-0 / pi-0.5'),
            (4, 'RT-2-X & the Data-Scaling Story'),
            (5, 'Comparing VLA Models'),
            (6, 'VLA Limitations'),
            (7, 'SayCan: Grounding LLM Plans'),
            (8, 'Code-as-Policies'),
            (9, 'VoxPoser: Language as Spatial Cost Field'),
            (10, 'Multi-Robot Dispatch via Shared LLM'),
            (11, 'ROS 2 Integration'),
            (12, 'Comparing the Planners'),
            (13, 'Sim-to-Real Gap'),
        ],
        'second_half_start': 7,
    },
]


def fix_chapter_index(module_dir, ch_num, new_title, big_picture, section_titles):
    """Rewrite the chapter index.html with the new title and full section list."""
    idx = module_dir / 'index.html'
    text = idx.read_text(encoding='utf-8')

    # Update title tag
    text = re.sub(
        rf'<title>Chapter {ch_num}:[^<]+</title>',
        f'<title>Chapter {ch_num}: {new_title} | Building Conversational AI with LLMs and Agents</title>',
        text
    )
    # Update meta description
    text = re.sub(
        rf'(<meta content=")Chapter {ch_num}:[^"]+(" name="description")',
        rf'\1Chapter {ch_num}: {new_title}. {big_picture[:100]}\2',
        text
    )
    # Update h1
    text = re.sub(
        r'<h1>[^<]+</h1>',
        f'<h1>{new_title}</h1>',
        text,
        count=1
    )
    # Update pagefind chapter meta
    text = re.sub(
        r'(<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter \d+:)[^"]+(")',
        rf'\1 {new_title}\2',
        text
    )
    # Update big-picture text
    text = re.sub(
        r'(<div class="callout big-picture">\s*<div class="callout-title">Big Picture</div>\s*<p>)[^<]+(</p>)',
        rf'\1{big_picture}\2',
        text,
        count=1
    )
    # Rebuild sections-list with all sections
    cards = []
    for sec_n, sec_title in section_titles:
        cards.append(
            f'<li><a class="section-card" href="section-{ch_num}.{sec_n}.html">\n'
            f'<span class="section-num">{ch_num}.{sec_n}</span>\n'
            f'<span class="section-title">{sec_title}</span>\n'
            f'<span class="section-desc">Section {ch_num}.{sec_n}.</span>\n'
            f'</a></li>'
        )
    text = re.sub(
        r'<ul class="sections-list">[\s\S]*?</ul>',
        '<ul class="sections-list">\n' + '\n'.join(cards) + '\n</ul>',
        text,
        count=1
    )
    idx.write_text(text, encoding='utf-8')


def fix_second_half_section(section_file, ch_num, sec_num, sec_title, new_chapter_title, old_chapter, old_topic):
    """Fix breadcrumb + pagefind-meta + h1 + visible h2 numbering in a second-half section."""
    text = section_file.read_text(encoding='utf-8')
    o = text

    # Fix breadcrumb: chapter link text says "Chapter 33: Video Generation" → "Chapter 20"
    text = re.sub(
        r'<a href="index\.html">Chapter \d+:[^<]+</a>',
        f'<a href="index.html">Chapter {ch_num}</a>',
        text
    )
    # Fix pagefind chapter meta
    text = re.sub(
        r'(<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter )\d+:[^"]+(")',
        rf'\1{ch_num}: {new_chapter_title}\2',
        text
    )
    # Fix chapter-nav up label
    text = re.sub(
        r'(<span class="nav-num">)Chapter \d+(</span><span class="nav-title">)[^<]+(</span>)',
        rf'\1Chapter {ch_num}\2{new_chapter_title}\3',
        text
    )
    # The agent noted: H2 visible numbering uses old chapter ("37.2.1", "33.X.Y").
    # Replace these with the current ch_num.sec_num.X.
    # Heuristic: extract old chapter number from h2 visible text matching `OLD_NUM.X.Y`
    # Replace OLD_NUM.X.Y with ch_num.sec_num where Y is preserved as the sub-section.
    # Specifically: h2 text like "37.2.1 ..." should become "22.7.1 ..." (if ch is 22, sec is 7).
    # We'll match heading text pattern: <h2 id="X-Y-Z-...">A.B.C ...</h2>
    # Use the section number we're processing as the canonical.
    # Match <h2 id="X-Y-Z-slug">N.M.K ...</h2> and rewrite the visible numbering to match ID
    def rewrite_h2(m):
        id_val = m.group(1)
        visible_num = m.group(2)
        rest = m.group(3)
        # ID is like "22-7-1-slug" → convert to "22.7.1"
        id_parts = re.match(r'(\d+)-(\d+)-(\d+)', id_val)
        if id_parts:
            new_num = f'{id_parts.group(1)}.{id_parts.group(2)}.{id_parts.group(3)}'
            return f'<h2 id="{id_val}">{new_num}{rest}</h2>'
        return m.group(0)

    text = re.sub(
        r'<h2 id="([^"]+)">([\d.]+)([^<]*)</h2>',
        rewrite_h2,
        text
    )

    # Same for h3
    def rewrite_h3(m):
        id_val = m.group(1)
        visible_num = m.group(2)
        rest = m.group(3)
        id_parts = re.match(r'(\d+)-(\d+)-(\d+)-(\d+)', id_val)
        if id_parts:
            new_num = f'{id_parts.group(1)}.{id_parts.group(2)}.{id_parts.group(3)}.{id_parts.group(4)}'
            return f'<h3 id="{id_val}">{new_num}{rest}</h3>'
        return m.group(0)

    text = re.sub(
        r'<h3 id="([^"]+)">([\d.]+)([^<]*)</h3>',
        rewrite_h3,
        text
    )

    # Fix figure captions: <strong>Figure N.M.K</strong> where N might be old chapter
    # Use the section file's actual section number as basis
    def rewrite_figcap(m):
        cap_num = m.group(1)
        # Figure caption like "Figure 37.2.1" — replace the chapter part with current ch
        parts = cap_num.split('.')
        if len(parts) >= 2:
            parts[0] = str(ch_num)
            return f'<strong>Figure {".".join(parts)}</strong>'
        return m.group(0)

    text = re.sub(
        r'<strong>Figure ([\d.]+)</strong>',
        rewrite_figcap,
        text
    )

    if text != o:
        section_file.write_text(text, encoding='utf-8')
        return True
    return False


def fix_part5_card(part5_idx_text, ch_num, new_title, section_titles, module_dir_name):
    """Update the Chapter N card in Part 5 index to use new title + full section list."""
    new_card = f'<div class="chapter-card">\n'
    new_card += f'<div class="chapter-card-header"><span class="mod-num">Chapter {ch_num}</span> {new_title}</div>\n'
    new_card += '<div class="chapter-card-body">\n<ul class="section-list">\n'
    for sec_n, sec_title in section_titles:
        new_card += f'<li><a href="{module_dir_name}/section-{ch_num}.{sec_n}.html"><span class="sec-num">{ch_num}.{sec_n}</span> {sec_title}</a></li>\n'
    new_card += '</ul>\n</div>\n</div>'

    # Find existing card for this chapter and replace
    pattern = rf'<div class="chapter-card">\s*<div class="chapter-card-header"><span class="mod-num">Chapter {ch_num}</span>[\s\S]*?</div>\s*</div>'
    new_text = re.sub(pattern, new_card, part5_idx_text, count=1)
    return new_text


def main():
    part5_idx = ROOT / 'part-5-multimodal-llms' / 'index.html'
    part5_text = part5_idx.read_text(encoding='utf-8')

    for ch in CHAPTERS:
        module_dir = ROOT / 'part-5-multimodal-llms' / ch['module']
        if not module_dir.exists():
            print(f"  Missing module: {ch['module']}")
            continue

        # 1. Fix chapter index.html
        fix_chapter_index(module_dir, ch['ch_num'], ch['new_title'],
                          ch['big_picture'], ch['section_titles'])
        print(f"  Updated Ch {ch['ch_num']} index ({ch['new_title']})")

        # 2. Fix second-half section files
        n_fixed = 0
        for sec_n, sec_title in ch['section_titles']:
            if sec_n < ch['second_half_start']:
                continue
            sf = module_dir / f"section-{ch['ch_num']}.{sec_n}.html"
            if sf.exists():
                if fix_second_half_section(sf, ch['ch_num'], sec_n, sec_title,
                                            ch['new_title'],
                                            ch['second_half_old_chapter'],
                                            ch['second_half_old_topic']):
                    n_fixed += 1
        print(f"    Fixed {n_fixed} second-half section files")

        # 3. Update Part 5 index card
        part5_text = fix_part5_card(part5_text, ch['ch_num'], ch['new_title'],
                                     ch['section_titles'], ch['module'])

    part5_idx.write_text(part5_text, encoding='utf-8')
    print("  Updated Part 5 index with renamed chapter cards + full section lists")


if __name__ == '__main__':
    main()
