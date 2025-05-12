import os
import json

# === PATH CONFIG ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXTRACTED_TEXT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "data", "extracted_text")
CONFIG_DIR = os.path.join(SCRIPT_DIR, "..", "..", "config")
OUTPUT_PATH = os.path.join(CONFIG_DIR, "source_metadata.json")

# Ensure config folder exists
os.makedirs(CONFIG_DIR, exist_ok=True)

# === BUILD METADATA STRUCTURE ===
metadata_template = {}

for filename in os.listdir(EXTRACTED_TEXT_DIR):
    if filename.endswith(".json"):
        metadata_template[filename] = {
            "title": "INSERT TITLE HERE",
            "sourceType": "research",  # or fiction, news, policy, design
            "publication": "INSERT PUBLICATION NAME",
            "year": 2020,
            "geography": "global",
            "actorType": "institution",  # or individual, machine, collective
            "signalID_prefix": filename.replace(".json", "")
        }

# === WRITE TO OUTPUT ===
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata_template, f, indent=2, ensure_ascii=False)

print(f"Metadata template created at: {OUTPUT_PATH}")