"""Wave 9 step E: Voice & Realtime merge into new Ch 40.

Per v9 plan, merge:
  - sec 37.5 (Voice Agents and Speech Interfaces, ~178 KB) — currently in Ch 37 Conv AI
  - Ch 39 (Streaming Realtime Multimodal, 4 sections, ~117 KB total)

Into a single new Ch 40 (Voice & Realtime Multimodal Assistants):
  40.1  Voice Agents and Speech Interfaces  (was 37.5)
  40.2  Streaming Audio Architectures        (was 39.1)
  40.3  Gemini Live & GPT-4o Realtime API    (was 39.2)
  40.4  Audio Token Budget & Latency Eng.    (was 39.3)
  40.5  Open-Source Realtime: Moshi, Pipecat, LiveKit  (was 39.4)

Then renumber Ch 38 (Tools of the Trade) -> Ch 41 (Conv AI Tools).

Resulting Part 8 structure:
  Ch 37 Conversational AI (4 sec, no voice)
  Ch 40 Voice & Realtime (5 sec)
  Ch 41 Conv AI Tools (5 sec)

No content loss: 9 sections preserved.
"""
from pathlib import Path
import re
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PART = 'part-8-conversational-ai-with-llms'
CH37_DIR = ROOT / PART / 'module-37-conversational-ai'
CH38_DIR = ROOT / PART / 'module-38-tools-of-the-trade'
CH39_DIR = ROOT / PART / 'module-39-streaming-realtime-multimodal'
CH40_DIR = ROOT / PART / 'module-40-voice-realtime-multimodal'
CH41_DIR = ROOT / PART / 'module-41-conv-ai-tools'

# (src_chapter, src_y, target_y, title)
MERGE_INTO_40 = [
    ('37', 5, 1, 'Voice Agents and Speech Interfaces'),
    ('39', 1, 2, 'Streaming Audio Architectures'),
    ('39', 2, 3, 'Gemini Live and GPT-4o Realtime API'),
    ('39', 3, 4, 'Audio Token Budget and Latency Engineering'),
    ('39', 4, 5, 'Open-Source Realtime: Moshi, Pipecat, LiveKit Agents'),
]

# Renumber: Ch 38 -> Ch 41 (keep section count 1-5)
RENUMBER_38_TO_41 = [
    (1, 'Platforms'),
    (2, 'Libraries and Frameworks'),
    (3, 'Datasets and Benchmarks'),
    (4, 'Models'),
    (5, 'External Reading and Communities'),
]


def rewrite_section_metadata(file_path, old_ch, old_y, new_ch, new_y, new_title):
    text = file_path.read_text(encoding='utf-8')
    new_label = f'{new_ch}.{new_y}'
    text = re.sub(
        rf'<title>Section {old_ch}\.{old_y}:[^<]*</title>',
        f'<title>Section {new_label}: {new_title} | Building Conversational AI with LLMs and Agents</title>',
        text
    )
    text = re.sub(
        rf'(<meta content=")Section {old_ch}\.{old_y}:[^"]*(")',
        rf'\1Section {new_label}: {new_title}\2',
        text
    )
    text = re.sub(r'<div class="page-current">Section [^<]+</div>',
                  f'<div class="page-current">Section {new_label}</div>', text)
    text = re.sub(r'<span class="bc-current">Section [^<]+</span>',
                  f'<span class="bc-current">Section {new_label}</span>', text)
    text = re.sub(r'<h1>[^<]+</h1>',
                  f'<h1>{new_title}</h1>', text, count=1)

    if old_ch != new_ch:
        text = re.sub(
            r'<a href="index\.html">Chapter \d+[^<]*</a>',
            f'<a href="index.html">Chapter {new_ch}</a>',
            text
        )
        text = re.sub(
            r'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:[^"]+"',
            f'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {new_ch}"',
            text
        )
        text = re.sub(
            r'<span class="nav-num">Chapter \d+</span><span class="nav-title">[^<]+</span>',
            f'<span class="nav-num">Chapter {new_ch}</span><span class="nav-title">{new_title}</span>',
            text
        )

    text = re.sub(rf'\bid="{old_ch}-{old_y}-', f'id="{new_ch}-{new_y}-', text)
    text = re.sub(rf'\bhref="#{old_ch}-{old_y}-', f'href="#{new_ch}-{new_y}-', text)
    text = re.sub(rf'\bSection {old_ch}\.{old_y}\b', f'Section {new_label}', text)
    text = re.sub(rf'\b{old_ch}\.{old_y}\.(\d+)\b', rf'{new_ch}.{new_y}.\1', text)
    file_path.write_text(text, encoding='utf-8')


def main():
    CH40_DIR.mkdir(parents=True, exist_ok=True)
    (CH40_DIR / 'images').mkdir(exist_ok=True)

    # Step 1: stage all moves with .__tmp__ to avoid collisions
    print('Step 1: stage moves')
    for src_ch, src_y, tgt_y, _title in MERGE_INTO_40:
        src_dir = CH37_DIR if src_ch == '37' else CH39_DIR
        src = src_dir / f'section-{src_ch}.{src_y}.html'
        tmp = CH40_DIR / f'section-40.{tgt_y}.html.__tmp__'
        if src.exists() and not tmp.exists():
            subprocess.run(['git', 'mv', str(src), str(tmp)], cwd=ROOT, capture_output=True)
            print(f'  Staged {src_ch}.{src_y} -> 40.{tgt_y}.__tmp__')

    # Stage Ch 38 -> 41 with __tmp__
    CH41_DIR.mkdir(parents=True, exist_ok=True)
    (CH41_DIR / 'images').mkdir(exist_ok=True)
    for old_y, _title in RENUMBER_38_TO_41:
        src = CH38_DIR / f'section-38.{old_y}.html'
        tmp = CH41_DIR / f'section-41.{old_y}.html.__tmp__'
        if src.exists() and not tmp.exists():
            subprocess.run(['git', 'mv', str(src), str(tmp)], cwd=ROOT, capture_output=True)
            print(f'  Staged 38.{old_y} -> 41.{old_y}.__tmp__')

    # Step 2: finalize moves + metadata
    print('Step 2: finalize')
    for src_ch, src_y, tgt_y, title in MERGE_INTO_40:
        tmp = CH40_DIR / f'section-40.{tgt_y}.html.__tmp__'
        dst = CH40_DIR / f'section-40.{tgt_y}.html'
        if tmp.exists() and not dst.exists():
            subprocess.run(['git', 'mv', str(tmp), str(dst)], cwd=ROOT, capture_output=True)
            rewrite_section_metadata(dst, int(src_ch), src_y, 40, tgt_y, title)
            print(f'  Finalized {src_ch}.{src_y} -> 40.{tgt_y}: {title}')

    for old_y, title in RENUMBER_38_TO_41:
        tmp = CH41_DIR / f'section-41.{old_y}.html.__tmp__'
        dst = CH41_DIR / f'section-41.{old_y}.html'
        if tmp.exists() and not dst.exists():
            subprocess.run(['git', 'mv', str(tmp), str(dst)], cwd=ROOT, capture_output=True)
            rewrite_section_metadata(dst, 38, old_y, 41, old_y, title)
            print(f'  Renumbered 38.{old_y} -> 41.{old_y}')

    # Step 3: write Ch 40 index
    cards_40 = []
    for src_ch, src_y, tgt_y, title in MERGE_INTO_40:
        cards_40.append(
            f'<li><a class="section-card" href="section-40.{tgt_y}.html">\n'
            f'<span class="section-num">40.{tgt_y}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">Voice and realtime multimodal AI.</span>\n'
            f'</a></li>'
        )
    ch40_idx = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter 40: Voice and Realtime Multimodal Assistants. Speech interfaces, streaming audio, realtime APIs." name="description"/>
<title>Chapter 40: Voice and Realtime Multimodal Assistants | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page chapter-index">
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part VIII: Conversational AI with LLMs</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Chapter 40</span></div>
<h1>Voice and Realtime Multimodal Assistants</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 40: Voice and Realtime Multimodal Assistants" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>Text chat is one mode; conversational AI also lives in voice, video, and screen-sharing assistants. This chapter covers voice agents (ASR, TTS, turn-taking), streaming audio architectures, the realtime API surface from major vendors (Gemini Live, GPT-4o Realtime, Anthropic), audio token budgets, and the open-source realtime stack (Moshi, Pipecat, LiveKit). It merges material from the Conv AI Voice section and the Streaming/Realtime Multimodal chapter into one focused home.</p>
</div>
<h2>Sections in This Chapter</h2>
<ul class="sections-list">
__CARDS__
</ul>
<nav class="chapter-nav">
<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">Part VIII</span><span class="nav-title">Conversational AI with LLMs</span></a>
</nav>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''.replace('__CARDS__', '\n'.join(cards_40))
    (CH40_DIR / 'index.html').write_text(ch40_idx, encoding='utf-8')
    print('Wrote Ch 40 index')

    # Step 4: write Ch 41 index (Conv AI Tools)
    cards_41 = []
    for old_y, title in RENUMBER_38_TO_41:
        cards_41.append(
            f'<li><a class="section-card" href="section-41.{old_y}.html">\n'
            f'<span class="section-num">41.{old_y}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">Conv AI tooling.</span>\n'
            f'</a></li>'
        )
    ch41_idx = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter 41: Conversational AI Tools of the Trade." name="description"/>
<title>Chapter 41: Conversational AI Tools of the Trade | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page chapter-index">
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part VIII: Conversational AI with LLMs</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Chapter 41</span></div>
<h1>Conversational AI Tools of the Trade</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 41: Conversational AI Tools of the Trade" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>The conversational AI ecosystem has its own stack of platforms (Botpress, Rasa, Dialogflow), libraries (LangChain conversation memory, OpenAI Assistants, Anthropic prompts), datasets (PersonaChat, MultiWOZ), models, and communities. This chapter is the practical reference.</p>
</div>
<h2>Sections in This Chapter</h2>
<ul class="sections-list">
__CARDS__
</ul>
<nav class="chapter-nav">
<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">Part VIII</span><span class="nav-title">Conversational AI with LLMs</span></a>
</nav>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''.replace('__CARDS__', '\n'.join(cards_41))
    (CH41_DIR / 'index.html').write_text(ch41_idx, encoding='utf-8')
    print('Wrote Ch 41 index')

    # Step 5: remove old Ch 38 and Ch 39 dirs (they should be empty of sections now)
    # Check if any files remain
    for old in [CH38_DIR, CH39_DIR]:
        if old.exists():
            remaining = list(old.glob('section-*.html'))
            if not remaining:
                # Remove the index.html and the dir
                idx = old / 'index.html'
                if idx.exists():
                    subprocess.run(['git', 'rm', str(idx)], cwd=ROOT, capture_output=True)
                # Move any remaining images to canonical location if they're referenced from new sections
                img_dir = old / 'images'
                if img_dir.exists():
                    # we will migrate images in a separate step based on actual references
                    pass
                print(f'  {old.name}: section files gone, kept images dir for migration')

    # Step 6: rewrite Ch 37 index (now 4 sections only)
    print('Step 6: update Ch 37 index')
    ch37_idx = CH37_DIR / 'index.html'
    text = ch37_idx.read_text(encoding='utf-8')
    cards = []
    for y, title in [(1, 'Dialogue System Architecture'),
                     (2, 'Personas, Companionship and Creative Writing'),
                     (3, 'Memory and Context Management'),
                     (4, 'Multi-Turn Dialogue and Conversation Flows')]:
        cards.append(
            f'<li><a class="section-card" href="section-37.{y}.html">\n'
            f'<span class="section-num">37.{y}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">Conversational AI.</span>\n'
            f'</a></li>'
        )
    text = re.sub(
        r'<ul class="sections-list">[\s\S]*?</ul>',
        '<ul class="sections-list">\n' + '\n'.join(cards) + '\n</ul>',
        text,
        count=1
    )
    # Strip any leftover orphan section-card for section-37.5
    text = re.sub(
        r'<li>\s*<a class="section-card" href="section-37\.5\.html">[\s\S]*?</a>\s*</li>\s*',
        '',
        text
    )
    text = re.sub(
        r'<ul class="sections-list">\s*</ul>\s*',
        '',
        text
    )
    ch37_idx.write_text(text, encoding='utf-8')

    # Step 7: update Part 8 index — remove Ch 38, Ch 39 cards; add Ch 40, Ch 41 cards
    print('Step 7: update Part 8 index')
    part8_idx = ROOT / PART / 'index.html'
    text = part8_idx.read_text(encoding='utf-8')
    # Remove cards for Ch 38, Ch 39
    text = re.sub(
        r'<div class="chapter-card">\s*<div class="chapter-card-header"><span class="mod-num">Chapter (38|39)</span>[\s\S]*?</div>\s*</div>\s*',
        '',
        text
    )
    # Strip old module-38 and module-39 hrefs
    text = re.sub(r'<li>\s*<a href="module-38-[^"]*">[\s\S]*?</a>\s*</li>\s*', '', text)
    text = re.sub(r'<li>\s*<a href="module-39-[^"]*">[\s\S]*?</a>\s*</li>\s*', '', text)

    if 'module-40-voice-realtime-multimodal/' not in text:
        new_card = '<div class="chapter-card">\n'
        new_card += '<div class="chapter-card-header"><span class="mod-num">Chapter 40</span> Voice and Realtime Multimodal Assistants</div>\n'
        new_card += '<div class="chapter-card-body">\n<ul class="section-list">\n'
        for src_ch, src_y, tgt_y, title in MERGE_INTO_40:
            new_card += f'<li><a href="module-40-voice-realtime-multimodal/section-40.{tgt_y}.html"><span class="sec-num">40.{tgt_y}</span> {title}</a></li>\n'
        new_card += '</ul>\n</div>\n</div>\n'
        text = text.replace('</main>', new_card + '</main>', 1)

    if 'module-41-conv-ai-tools/' not in text:
        new_card = '<div class="chapter-card">\n'
        new_card += '<div class="chapter-card-header"><span class="mod-num">Chapter 41</span> Conversational AI Tools of the Trade</div>\n'
        new_card += '<div class="chapter-card-body">\n<ul class="section-list">\n'
        for old_y, title in RENUMBER_38_TO_41:
            new_card += f'<li><a href="module-41-conv-ai-tools/section-41.{old_y}.html"><span class="sec-num">41.{old_y}</span> {title}</a></li>\n'
        new_card += '</ul>\n</div>\n</div>\n'
        text = text.replace('</main>', new_card + '</main>', 1)

    part8_idx.write_text(text, encoding='utf-8')
    print('  Part 8 index updated')

    # Step 8: global cross-ref rewrite
    print('Step 8: global cross-ref rewrite')
    # Build move mapping
    moves = []
    # 37.5 -> 40.1
    moves.append(('module-37-conversational-ai', 37, 5, 'module-40-voice-realtime-multimodal', 40, 1))
    # 39.x -> 40.y
    for src_ch, src_y, tgt_y, _ in MERGE_INTO_40:
        if src_ch == '39':
            moves.append(('module-39-streaming-realtime-multimodal', 39, src_y, 'module-40-voice-realtime-multimodal', 40, tgt_y))
    # 38.x -> 41.x
    for old_y, _ in RENUMBER_38_TO_41:
        moves.append(('module-38-tools-of-the-trade', 38, old_y, 'module-41-conv-ai-tools', 41, old_y))

    SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
            'source_fix_backups', 'pagefind', 'templates', '.claude',
            '.book-update', 'vendor', 'docs'}
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Sentinel pattern
        for old_module, old_ch, old_y, new_module, new_ch, new_y in moves:
            text = re.sub(
                rf'(href="[^"]*?){re.escape(old_module)}/section-{old_ch}\.{old_y}\.html',
                rf'\1__MOVE_{old_ch}_{old_y}__',
                text
            )
        for old_module, old_ch, old_y, new_module, new_ch, new_y in moves:
            text = text.replace(
                f'__MOVE_{old_ch}_{old_y}__',
                f'{new_module}/section-{new_ch}.{new_y}.html'
            )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Cross-refs updated in {n_files} files')


if __name__ == '__main__':
    main()
