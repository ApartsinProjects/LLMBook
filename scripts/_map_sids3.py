"""Print sid -> path for more SIDs."""
import sys
sys.path.insert(0, 'E:/Projects/BookBlogsHome/LLMBook/scripts')
from dedup_detector import gather_sections, section_id, ROOT

paths = gather_sections()
mapping = {}
for p in paths:
    sid = section_id(p)
    mapping[sid] = str(p.relative_to(ROOT)).replace('\\', '/')

targets = ['S20.1', 'S32.1a', 'S32.1b', 'S78.8', 'S78.9', 'S31.4', 'S31.4b', 'S15.3', 'S15.7',
           'S21.2', 'S21.4', 'S26.1', 'S32.3', 'S9.5', 'S31.1b', 'S31.3', 'S33.1', 'S35.4', 'S35.5a', 'S35.5b']
for t in targets:
    print(f'{t}: {mapping.get(t, "NOT FOUND")}')
