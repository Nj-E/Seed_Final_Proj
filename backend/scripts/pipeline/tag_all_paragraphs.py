import os
import json
import numpy as np
import warnings

from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from transformers import pipeline
from bertopic import BERTopic
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

# ==== CONFIG ====
STRUCTURED_UNITS_DIR = "../data/structured_units_truncated"
TAGGED_SIGNALS_DIR = "../data/tagged_signals"
THEME_MAPPING_PATH = "themes.json"
os.makedirs(TAGGED_SIGNALS_DIR, exist_ok=True)

# ==== WARNINGS ====
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ==== LOAD THEME MAPPING ====
print("Loading theme mapping...")
with open(THEME_MAPPING_PATH, "r", encoding="utf-8") as f:
    raw_map = json.load(f)
theme_map = {tuple(k): v for k, v in raw_map}

# ==== LOAD MODELS ====
print("Loading models...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(embedder)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0 if embedder.device.type == "cuda" else -1)

# Define a safe vectorizer for KeyBERT
safe_vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words="english", max_features=1000)

# ==== TAGGING ====
skipped_units = []

for filename in sorted(os.listdir(STRUCTURED_UNITS_DIR)):
    if not filename.endswith(".json"):
        continue

    print(f"Tagging {filename}:")
    in_path = os.path.join(STRUCTURED_UNITS_DIR, filename)
    out_path = os.path.join(TAGGED_SIGNALS_DIR, filename)

    with open(in_path, "r", encoding="utf-8") as f:
        units = json.load(f)

    tagged = []
    for unit in tqdm(units, desc=filename, ncols=80):
        if not unit.get("text") or len(unit["text"].strip().split()) <= 5:
            skipped_units.append(unit)
            continue

        # Add theme from mapping
        key = (filename, unit["id"])
        unit["theme"] = theme_map.get(key, "unknown")

        # Keyword extraction with fallback
        try:
            keywords = kw_model.extract_keywords(
                unit["text"],
                keyphrase_ngram_range=(1, 2),
                stop_words="english",
                use_maxsum=True,
                vectorizer=safe_vectorizer,
                top_n=5
            )
            subthemes = [kw[0] for kw in keywords if len(kw[0].split()) >= 1 and kw[0].isalpha()]
        except Exception as e:
            print(f"Keyword extraction failed for unit {unit['id']} in {filename}. Skipping. Error: {e}")
            skipped_units.append(unit)
            continue

        unit["subThemes"] = subthemes

        # Sentiment classification
        try:
            result = classifier(unit["text"], candidate_labels=["positive", "neutral", "negative"])
            unit["sentiment"] = result["labels"][0]
        except Exception as e:
            print(f"Sentiment analysis failed for unit {unit['id']} in {filename}. Skipping. Error: {e}")
            skipped_units.append(unit)
            continue

        tagged.append(unit)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tagged, f, indent=2, ensure_ascii=False)

    print(f"Saved: {out_path} ({len(tagged)} tagged, {len(units) - len(tagged)} skipped)")

# Save skipped units
if skipped_units:
    with open("skipped_signals.json", "w", encoding="utf-8") as f:
        json.dump(skipped_units, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(skipped_units)} skipped units to skipped_signals.json")

print("All done.")