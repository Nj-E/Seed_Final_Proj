import json
from collections import Counter

with open('public/data/scenarios.json') as f:
    scenarios = json.load(f)

combo_counts = Counter((s['polarity'], s['likelihood']) for s in scenarios)
print("Scenario counts by (polarity, likelihood):")
for combo, count in sorted(combo_counts.items()):
    print(f"{combo}: {count}") 