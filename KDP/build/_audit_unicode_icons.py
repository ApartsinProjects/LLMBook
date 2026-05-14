"""Audit unicode-icon ::before rules in book.css that may cause tofu boxes."""
import zipfile, re
with zipfile.ZipFile(r'KDP/output/building-conversational-ai-llms-agents.epub') as z:
    book = z.read('EPUB/styles/book.css').decode('utf-8')

found = []
for m in re.finditer(r"([^{}]{1,150}::before)\s*\{[^}]*content\s*:\s*['\"]([^'\"]+)['\"]", book):
    sel = m.group(1).strip()
    content_val = m.group(2)
    has_unicode = any(ord(c) > 127 for c in content_val) or '\\' in content_val
    if has_unicode:
        found.append((sel, content_val))

print(f'Found {len(found)} ::before rules with unicode/escape content:')
for sel, content_val in found:
    print(f'  {sel[:90]} -> {content_val!r}')
