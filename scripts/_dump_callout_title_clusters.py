"""Dump non-structural callout title clusters from the repeated-content audit."""
import sys, importlib.util

sys.path.insert(0, r'E:\Projects\BookBlogsHome\LLMBook\scripts')
spec = importlib.util.spec_from_file_location(
    'audit', r'E:\Projects\BookBlogsHome\LLMBook\scripts\_audit_repeated_content.py'
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

files = mod.collect_section_files()
print(f"Section files: {len(files)}")

all_callouts = []
all_captions = []
all_prose = []
for fp in files:
    callouts, captions, prose = mod.extract_section_data(fp)
    all_callouts.extend(callouts)
    all_captions.extend(captions)
    all_prose.extend(prose)

clusters, fuzzy_caption_clusters = mod.cluster_duplicates(all_callouts, all_captions, all_prose)
ctc = clusters['callout_title_non_structural']
print(f"Non-structural callout titles raw clusters: {len(ctc)}")

# Print clusters with 2+ sections
print("\n" + "=" * 70)
print("CLUSTERS WITH 2+ SECTIONS")
print("=" * 70)
n_shown = 0
for key, items in sorted(ctc.items()):
    sections_set = {it['section'] for it in items}
    if len(sections_set) < 2:
        continue
    n_shown += 1
    print(f"\n--- CLUSTER {n_shown}: TITLE: {key!r} ---")
    print(f"    sections: {len(sections_set)}, items: {len(items)}")
    for it in items:
        section = it.get('section', '?')
        line = it.get('line', '?')
        title = it.get('title', '')
        print(f"   {section}:{line}")
        print(f"     title: {title!r}")
        if 'preview' in it:
            preview = it['preview'][:140]
            print(f"     body: {preview}")
print(f"\nTotal clusters with 2+ sections: {n_shown}")
