import os
import json

# Relative paths from this script
STRUCTURED_UNITS_DIR = "../data/structured_units"
TRUNCATED_UNITS_DIR = "../data/structured_units_truncated"
MAX_WORDS = 512  # Truncate paragraphs longer than this

os.makedirs(TRUNCATED_UNITS_DIR, exist_ok=True)

for filename in os.listdir(STRUCTURED_UNITS_DIR):
    if filename.endswith(".json"):
        input_path = os.path.join(STRUCTURED_UNITS_DIR, filename)
        output_path = os.path.join(TRUNCATED_UNITS_DIR, filename)
        with open(input_path, "r", encoding="utf-8") as f:
            units = json.load(f)
            for unit in units:
                words = unit["text"].split()
                if len(words) > MAX_WORDS:
                    unit["text"] = " ".join(words[:MAX_WORDS])
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(units, f, indent=2, ensure_ascii=False)

print("Truncation complete.")