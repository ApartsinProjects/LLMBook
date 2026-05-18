"""Print sid -> path for additional SIDs."""
import sys
sys.path.insert(0, 'E:/Projects/BookBlogsHome/LLMBook/scripts')
from dedup_detector import gather_sections, section_id, ROOT

paths = gather_sections()
mapping = {}
for p in paths:
    sid = section_id(p)
    mapping[sid] = str(p.relative_to(ROOT)).replace('\\', '/')

targets = ['S30.2', 'S19.13', 'S61.4', 'S58.5', 'S59.2', 'S6.3', 'S48.5', 'S56.4', 'S45.2', 'S12.2',
           'S49.4', 'S30.3', 'S30.5', 'S29.2', 'S29.4', 'S30.1', 'S30.4', 'S15.6']
for t in targets:
    print(f'{t}: {mapping.get(t, "NOT FOUND")}')
