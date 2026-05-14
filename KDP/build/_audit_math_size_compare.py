"""Compare file-size impact of KaTeX output modes."""
import os, subprocess, json, tempfile

env = os.environ.copy()
env['NODE_PATH'] = r'E:/Projects/BookBlogsHome/LLMBook/KDP/build/node_modules'

samples = {
    'display_complex': r'L_{aux} = \alpha N \sum_{i=1}^N f_i p_i',
    'inline_subscript': r'p_i',
    'fraction': r'\frac{a}{b}',
}

print(f'{"mode":>16}  {"complex":>10}  {"p_i":>5}  {"frac":>6}')
print('-' * 50)
for mode in ['html', 'mathml', 'htmlAndMathml']:
    sizes = []
    for name, tex in samples.items():
        js_content = (
            "const katex = require('katex');\n"
            f"const r = katex.renderToString({json.dumps(tex)}, "
            f"{{output: '{mode}', displayMode: true, throwOnError: false}});\n"
            "console.log(r.length);"
        )
        fd, tmp = tempfile.mkstemp(suffix='.js', dir=r'E:/temp')
        os.close(fd)
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                f.write(js_content)
            p = subprocess.run(['node', tmp], capture_output=True, text=True, env=env, timeout=10)
            sizes.append(int(p.stdout.strip()))
        finally:
            os.unlink(tmp)
    print(f'{mode:>16}  {sizes[0]:>10}  {sizes[1]:>5}  {sizes[2]:>6}')
