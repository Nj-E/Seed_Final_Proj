import os
import json

# ==== RESOLVE PATHS RELATIVELY ====
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

TAGGED_SIGNALS_DIR = os.path.join(PROJECT_ROOT, "data", "tagged_signals")
FUTURE_TYPE_PATH = os.path.join(SCRIPT_DIR, "..", "future_types.json")
OUTPUT_INDEX_PATH = os.path.join(PROJECT_ROOT, "data", "search_index.json")

# ==== LOAD FUTURE TYPES ====
try:
    with open(FUTURE_TYPE_PATH, "r", encoding="utf-8") as f:
        future_type_lookup = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"{FUTURE_TYPE_PATH} not found. Please run compute_theme_frequencies.py first.")

# ==== INDEX BUILDING ====
print("Building search index...")
search_index = []

for filename in sorted(os.listdir(TAGGED_SIGNALS_DIR)):
    if filename.endswith(".json"):
        file_path = os.path.join(TAGGED_SIGNALS_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                units = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Skipping {filename} due to JSON decode error.")
                continue

            for unit in units:
                theme = str(unit.get("theme", -1))
                future_type = future_type_lookup.get(theme, "possible")  # Treat unknowns as "possible"

                signal = {
                    "id": unit.get("id"),
                    "text": unit.get("text"),
                    "theme": unit.get("theme"),
                    "subThemes": unit.get("subThemes", []),
                    "sentiment": unit.get("sentiment"),
                    "source_pdf": unit.get("source_pdf"),
                    "future_type": future_type
                }
                search_index.append(signal)

print(f"Total signals added to index: {len(search_index)}")

# ==== SAVE INDEX ====
with open(OUTPUT_INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(search_index, f, indent=2, ensure_ascii=False)

print(f"Search index saved to: {OUTPUT_INDEX_PATH}")