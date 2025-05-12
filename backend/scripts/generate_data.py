import os
import json
import random
from collections import defaultdict, Counter
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'generation'))
from generate_narrative import build_narrative

# --- CONFIG ---
TAGGED_SIGNALS_DIR = os.path.join(os.path.dirname(__file__), '../data/tagged_signals')
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
SIGNALS_PATH = os.path.join(DATA_DIR, 'signals.json')
SCENARIOS_PATH = os.path.join(DATA_DIR, 'scenarios.json')
METADATA_PATH = os.path.join(os.path.dirname(__file__), '../../config/source_metadata.json')
MAX_SCENARIOS = 50
MAX_PER_COMBO = 3
SIGNALS_PER_SCENARIO = 5

# --- LOAD METADATA TEMPLATE (if exists) ---
metadata_template = {}
if os.path.exists(METADATA_PATH):
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata_template = json.load(f)

# --- MERGE SIGNALS ---
signals = []
for fname in os.listdir(TAGGED_SIGNALS_DIR):
    if fname.endswith('.json'):
        with open(os.path.join(TAGGED_SIGNALS_DIR, fname), 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Enrich with metadata if available
                for sig in data:
                    source_pdf = sig.get('source_pdf') or sig.get('source') or fname
                    meta = metadata_template.get(source_pdf.replace('.json', '') + '.json', {})
                    sig['metadata'] = meta
                signals.extend(data)
            except Exception as e:
                print(f"Error reading {fname}: {e}")

# Optionally: deduplicate signals by id
unique_signals = {}
for sig in signals:
    if 'id' in sig:
        unique_signals[sig['id']] = sig
signals = list(unique_signals.values())

with open(SIGNALS_PATH, 'w', encoding='utf-8') as f:
    json.dump(signals, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(signals)} signals to {SIGNALS_PATH}")

# --- GENERATE SCENARIOS ---
signals_by_theme_and_sentiment = defaultdict(lambda: defaultdict(list))
for sig in signals:
    theme = sig.get('theme')
    sentiment = sig.get('sentiment', 'neutral')
    if theme is not None:
        signals_by_theme_and_sentiment[theme][sentiment].append(sig)

likelihood_thresholds = [
    ('probable', 10),
    ('plausible', 5),
    ('possible', 1),
]

signals_by_id = {sig['id']: sig for sig in signals}

scenarios = []
for theme, sentiment_dict in signals_by_theme_and_sentiment.items():
    for sentiment, sigs in sentiment_dict.items():
        if sentiment == 'neutral':
            continue  # Skip neutral sentiment
        count = len(sigs)
        for likelihood, threshold in likelihood_thresholds:
            if count >= threshold:
                num_scenarios = min(MAX_PER_COMBO, count // threshold)
                for i in range(num_scenarios):
                    title_counts = Counter([sig.get('title', f"Theme {theme}") for sig in sigs])
                    scenario_title = title_counts.most_common(1)[0][0]
                    sample = random.sample(sigs, min(SIGNALS_PER_SCENARIO, len(sigs)))
                    contributing_signals = [sig['id'] for sig in sample]
                    # Generate narrative description
                    signals_for_narrative = [sig for sig in sigs if sig['id'] in contributing_signals]
                    narrative = build_narrative(signals_for_narrative, likelihood, sentiment)
                    # Build sources list
                    sources = []
                    for sig_id in contributing_signals:
                        sig = signals_by_id.get(sig_id)
                        if sig:
                            src = sig.get('source') or sig.get('source_pdf') or sig.get('id')
                            title = sig.get('title', '')
                            sources.append(f"{sig_id}: {title} ({src})")
                    scenario = {
                        'id': f'theme-{theme}-{sentiment}-{likelihood}-{i+1}',
                        'title': scenario_title,
                        'description': narrative,
                        'polarity': sentiment,
                        'likelihood': likelihood,
                        'contributingSignals': contributing_signals,
                        'sources': sources
                    }
                    scenarios.append(scenario)

# Cap the total number of scenarios
if len(scenarios) > MAX_SCENARIOS:
    scenarios = random.sample(scenarios, MAX_SCENARIOS)

with open(SCENARIOS_PATH, 'w', encoding='utf-8') as f:
    json.dump(scenarios, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(scenarios)} scenarios to {SCENARIOS_PATH}") 