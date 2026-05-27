"""Organize the pedagogy audit punch list into per-chapter enrichment briefs."""
import json
from pathlib import Path
from collections import defaultdict

data = json.load(open('slide-summaries/_pedagogy_audit_v3.json', encoding='utf-8'))
found = [r for r in data['techniques'] if r['status'] == 'FOUND']

# Filter punch list
# Tier 1+2: weight=1.0 AND agg_score <= 2  -> ~37 items
# Tier 3:   weight=0.6 AND agg_score <= 1  -> ~59 items
# Combined: 96 items
punch = [r for r in found
         if (r['weight'] >= 1.0 and r['agg_score'] <= 2)
         or (r['weight'] >= 0.5 and r['weight'] < 1.0 and r['agg_score'] <= 1)]
print(f"Total enrichment punch-list items: {len(punch)}")

# Organize by part (extract from canonical_file path)
by_part = defaultdict(list)
for r in punch:
    parts = r['canonical_file'].split('/')
    part = parts[0]
    by_part[part].append(r)

print()
print("Distribution by part:")
for part, items in sorted(by_part.items()):
    print(f"  {part:60s} {len(items):3d} items")

# Save per-part briefs
out_dir = Path('slide-summaries/_enrichment_briefs')
out_dir.mkdir(exist_ok=True)
for part, items in by_part.items():
    short = part.replace('part-', '').replace('-', '_')
    f = out_dir / f"brief_{short}.json"
    f.write_text(json.dumps({
        'part': part,
        'count': len(items),
        'techniques': items,
    }, indent=2), encoding='utf-8')
    print(f"  Wrote: {f}")
