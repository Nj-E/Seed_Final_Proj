import os
import json
import random

# === PATH CONFIGURATION ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEARCH_INDEX_PATH = os.path.join(SCRIPT_DIR, "..", "..", "data", "search_index.json")

def load_signals(future_type, sentiment):
    with open(SEARCH_INDEX_PATH, "r", encoding="utf-8") as f:
        all_signals = json.load(f)
    return [
        s for s in all_signals
        if s.get("future_type") == future_type and s.get("sentiment") == sentiment
    ]

def sample_signals(signals, n=4):
    return random.sample(signals, min(len(signals), n))

def build_narrative(signals, future_type, sentiment):
    if not signals:
        return "No signals available to generate a scenario."
    # Use the titles and a summary of the signals, skipping empty values
    titles = [sig.get('title', '').strip() for sig in signals if sig.get('title', '').strip()]
    main_points = [sig.get('description', '').strip() for sig in signals if sig.get('description', '').strip()]
    polarity_word = "optimistic" if sentiment == "positive" else "cautious"
    likelihood_word = {
        "probable": "very likely",
        "plausible": "plausible",
        "possible": "possible"
    }.get(future_type, future_type)
    theme = signals[0].get('theme', 'this theme')
    if titles:
        title_part = f"key developments include: {', '.join(titles)}. "
    else:
        title_part = "key developments are emerging. "
    if main_points:
        highlight_part = f"These signals suggest that the future may unfold with the following highlights: {main_points[0]}"
    else:
        highlight_part = "However, more details are needed to describe this scenario."
    summary = (
        f"In this {likelihood_word} and {polarity_word} scenario for {theme}, {title_part}{highlight_part}"
    )
    return summary

def generate(future_type="plausible", sentiment="positive"):
    signals = load_signals(future_type, sentiment)
    if not signals:
        return "No matching signals found.", []
    
    selected = sample_signals(signals)
    story = build_narrative(selected, future_type, sentiment)
    citations = [s["id"] for s in selected]
    return story, citations

if __name__ == "__main__":
    story, sources = generate(future_type="probable", sentiment="positive")
    print("Generated Scenario:")
    print(story)
    print("\nCitations:")
    for src in sources:
        print(f"- {src}")