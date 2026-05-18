"""Print sid -> path mapping for the dedup work."""
import sys
sys.path.insert(0, 'E:/Projects/BookBlogsHome/LLMBook/scripts')
from dedup_detector import gather_sections, section_id, ROOT

paths = gather_sections()
mapping = {}
for p in paths:
    sid = section_id(p)
    mapping[sid] = str(p.relative_to(ROOT)).replace('\\', '/')

targets = ['S1.3', 'S1.4', 'S3.1a', 'S3.2', 'S13.2', 'S16.5', 'S31.1a', 'S31.1b',
           'S42.4', 'S44.3', 'S44.5', 'S66.1', 'S67.9', 'S70.3', 'S70.4',
           'S18.1', 'S18.2', 'S0.4', 'S8.3', 'S82.2',
           'S49.5', 'S32.4', 'S33.3', 'S33.4', 'S34.1', 'S34.2', 'S48.3', 'S72.5', 'S81.2',
           'S9.1', 'S9.2', 'S9.3', 'S9.4', 'S9.5', 'S31.2', 'S55.1', 'S80.4', 'S7.2', 'S10.8',
           'S1.5', 'S1.6', 'S1.7', 'S52.3', 'S7.3', 'S16.6', 'S41.4',
           'S47.1a', 'S47.1b', 'S12.4', 'S47.2', 'S47.3', 'S48.2', 'S48.5', 'S49.1',
           'S67.11', 'S70.1', 'S76.3', 'S76.5',
           'S4.1', 'S4.3', 'S6.2', 'S14.2',
           'S18.3', 'S54.6', 'S54.8', 'S75.5',
           'S33.1']
for t in targets:
    print(f'{t}: {mapping.get(t, "NOT FOUND")}')
