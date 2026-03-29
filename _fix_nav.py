import re, glob, os

os.chdir("E:/Projects/LLMCourse")

# All front-matter files to fix nav classes on
files = (
    glob.glob('front-matter/pathways/*.html') +
    glob.glob('front-matter/syllabi/*.html') +
    ['front-matter/section-fm.1.html', 'front-matter/section-fm.4.html',
     'front-matter/section-fm.7.html', 'front-matter/index.html',
     'front-matter/wisdom-council.html']
)

# Skip files that already have correct classes
skip = {'front-matter/syllabi/index.html', 'front-matter/section-fm.5.html'}

for fpath in files:
    fpath = fpath.replace('\\', '/')
    if fpath in skip:
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the chapter-nav block with 2 <a> links (no classes)
    nav_pattern = re.compile(
        r'(<nav class="chapter-nav">)\s*\n'
        r'(\s*)<a (href="[^"]+">)(.*?</a>)\s*\n'
        r'(\s*)<a (href="[^"]+">)(.*?</a>)\s*\n'
        r'(\s*</nav>)',
        re.MULTILINE
    )

    match = nav_pattern.search(content)
    if match:
        # Check if classes already present
        if 'class="prev"' in match.group(0) or 'class="next"' in match.group(0):
            print(f'Already has classes: {fpath}')
            continue

        indent = match.group(2)
        replacement = (
            match.group(1) + '\n' +
            indent + '<a class="prev" ' + match.group(3) + match.group(4) + '\n' +
            indent + '<a class="next" ' + match.group(6) + match.group(7) + '\n' +
            match.group(8)
        )
        content = content[:match.start()] + replacement + content[match.end():]

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed nav classes: {fpath}')
    else:
        print(f'No 2-link nav match: {fpath}')
