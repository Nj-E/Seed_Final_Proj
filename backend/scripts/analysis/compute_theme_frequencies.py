import json
import numpy as np
from collections import defaultdict
import os

# === CONFIGURATION ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(SCRIPT_DIR, "..", "themes.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "future_types.json")

# === LOAD THEMES FILE ===
try:
    with open(THEME_PATH, "r", encoding="utf-8") as f:
        theme_map = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading themes.json: {e}")
    exit(1)

# === COUNT THEME FREQUENCIES (EXCLUDING -1) ===
theme_counts = defaultdict(int)
all_themes = set()

for entry in theme_map:
    _, theme_id = entry
    if theme_id != -1:
        theme_counts[theme_id] += 1
        all_themes.add(theme_id)
    elif theme_id == -1:
        all_themes.add(theme_id)

if not theme_counts:
    print("Warning: No valid themes found (all were -1). Exiting.")
    exit(1)

# === CALCULATE PERCENTILE THRESHOLDS ===
all_counts = np.array(list(theme_counts.values()))
p50, p85 = np.percentile(all_counts, [50, 85])

# === ASSIGN FUTURE TYPES ===
future_types = {}
for theme_id in all_themes:
    if theme_id == -1:
        future_types[str(theme_id)] = "possible"  # Treat unknowns as edge cases
    else:
        count = theme_counts[theme_id]
        if count >= p85:
            future_types[str(theme_id)] = "probable"
        elif count >= p50:
            future_types[str(theme_id)] = "plausible"
        else:
            future_types[str(theme_id)] = "possible"

# === SAVE OUTPUT ===
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(future_types, f, indent=2)

# === LOG SUMMARY ===
print(f"Processed {len(theme_counts)} valid themes (+ unknowns).")
print(f"Theme count thresholds - Possible: < {p50:.2f}, Plausible: ≥ {p50:.2f}, Probable: ≥ {p85:.2f}")
print(f"Saved theme classifications to {OUTPUT_PATH}")