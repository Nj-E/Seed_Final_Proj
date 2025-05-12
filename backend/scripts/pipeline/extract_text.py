import os
import fitz
import json

# Define folder paths
RAW_PDF_DIR = "../../data/raw_data"
EXTRACTED_TEXT_DIR = "../../data/extracted_text"

# Debug statements
print("Looking for PDFs in:", os.path.abspath(RAW_PDF_DIR))
if not os.path.exists(RAW_PDF_DIR):
    print("Folder not found")
else:
    files = os.listdir(RAW_PDF_DIR)
    print("Folder found. Files inside:", files)

# Check output folder exists
os.makedirs(EXTRACTED_TEXT_DIR, exist_ok=True)

# Loop through all PDFs
for filename in os.listdir(RAW_PDF_DIR):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(RAW_PDF_DIR, filename)
        output_path = os.path.join(EXTRACTED_TEXT_DIR, filename.replace(".pdf", ".json"))

        print(f"Extracting: {filename}")
        doc = fitz.open(pdf_path)
        pages = []

        for i, page in enumerate(doc):
            text = page.get_text()
            pages.append({
                "page": i + 1,
                "text": text.strip()
            })

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)

        print(f"Saved to: {output_path}")