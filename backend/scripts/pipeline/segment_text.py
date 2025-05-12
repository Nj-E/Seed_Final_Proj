import os
import json
import re

# Folder paths
EXTRACTED_TEXT_DIR = "../data/extracted_text"
STRUCTURED_UNITS_DIR = "../data/structured_units"
METADATA_FILE = "../config/source_metadata.json"

# Load source metadata
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    SOURCE_METADATA = json.load(f)

# Ensure output folder exists
os.makedirs(STRUCTURED_UNITS_DIR, exist_ok=True)

# Helper: split page text into paragraphs
def split_into_paragraphs(text):
    return [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

# Loop through extracted text files
for filename in os.listdir(EXTRACTED_TEXT_DIR):
    if filename.endswith(".json"):
        input_path = os.path.join(EXTRACTED_TEXT_DIR, filename)
        output_path = os.path.join(STRUCTURED_UNITS_DIR, filename.replace(".json", "_paragraphs.json"))

        print(f"📄 Segmenting: {filename}")
        with open(input_path, "r", encoding="utf-8") as f:
            pages = json.load(f)

        metadata = SOURCE_METADATA.get(filename, {})
        paragraph_units = []

        for page in pages:
            paragraphs = split_into_paragraphs(page["text"])
            for i, para in enumerate(paragraphs):
                unit = {
                    "id": f"{filename.replace('.json', '')}_p{page['page']}_{i+1}",
                    "source_pdf": filename,
                    "page": page["page"],
                    "text": para,
                    "metadata": metadata
                }
                paragraph_units.append(unit)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(paragraph_units, f, indent=2, ensure_ascii=False)

        print(f"Saved: {output_path}")