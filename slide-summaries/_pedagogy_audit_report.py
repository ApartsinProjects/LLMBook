import json
import sys

data = json.load(open('slide-summaries/_pedagogy_audit.json', encoding='utf-8'))

print("=" * 70)
print("PEDAGOGY AUDIT SUMMARY")
print("=" * 70)
print(f"Total technique sub-sections detected: {data['total_techniques_detected']}")
print(f"Score distribution (0 = pure prose; 4 = figure + math + code + worked example):")
for s in sorted(data['score_distribution'].keys()):
    pct = 100 * data['score_distribution'][s] / data['total_techniques_detected']
    print(f"  {s}/4: {data['score_distribution'][s]:5d}  ({pct:5.1f}%)")
print()

# Score 0 means: prose only, no figure, no math, no code, no example callout
score0 = [r for r in data['deficient'] if r['score'] == 0]
score1 = [r for r in data['deficient'] if r['score'] == 1]

print("--- Top 25 score-0 (PURE PROSE) with substantial body (>= 500 chars) ---")
big_score0 = [r for r in score0 if r['body_chars'] >= 500]
for r in big_score0[:25]:
    parts = r['file'].split(chr(92))  # backslash on Windows
    loc = '/'.join(parts[-2:])
    title = r['title'][:55]
    print(f"  [{r['body_chars']:5d}c] {title:55s}  ({loc})")

print()
print(f"  (Total score-0 with body >= 500c: {len(big_score0)} of {len(score0)})")
print()

# Per chapter median
print("--- Per-chapter pedagogy health (15 worst) ---")
chs = sorted(data['chapter_summary'].items(), key=lambda x: x[1]['mean'])
for ch, stats in chs[:15]:
    bar = '#' * int(stats['mean'] * 10)
    print(f"  mean {stats['mean']:.2f}  ({stats['count']:3d} sub-sec, {stats['score_0_or_1']:3d} need work)  {bar:<25s} {ch}")
print()
print("--- Best-scoring chapters (top 5) ---")
for ch, stats in chs[-5:]:
    bar = '#' * int(stats['mean'] * 10)
    print(f"  mean {stats['mean']:.2f}  ({stats['count']:3d} sub-sec, {stats['score_0_or_1']:3d} need work)  {bar:<25s} {ch}")
