import os
import json
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic

STRUCTURED_UNITS_DIR = "../data/structured_units_truncated"
THEME_MAPPING_PATH = "themes.json"
MODEL_DIR = "pipeline/bertopic_model"

all_paragraphs = []
unit_keys = []

print("Loading all paragraphs...")
for filename in sorted(os.listdir(STRUCTURED_UNITS_DIR)):
    if filename.endswith(".json"):
        with open(os.path.join(STRUCTURED_UNITS_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
            for unit in data:
                if unit.get("text") and len(unit["text"].split()) > 5:
                    all_paragraphs.append(unit["text"])
                    unit_keys.append((filename, unit["id"]))

print(f"Total paragraphs to cluster: {len(all_paragraphs)}")

print("Generating embeddings and fitting BERTopic model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
topic_model = BERTopic(embedding_model=embedder)
topics, _ = topic_model.fit_transform(all_paragraphs)

print("Saving BERTopic model...")
topic_model.save(MODEL_DIR)

print("Saving theme mapping...")
theme_map = list(zip(unit_keys, topics))
with open(THEME_MAPPING_PATH, "w", encoding="utf-8") as f:
    json.dump(theme_map, f)

print("Done.")