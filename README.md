# SEED
### Seed is a speculative‑design platform that bridges imagination and reality. By ingesting signals from climate research, Seed generates possibilities of the future—probable, plausible, and possible—and empowers policymakers, designers, and innovators to prototype and simulate technology‑driven future narratives.

URL: https://github.com/Nj-E/Seed_proj

## What SEED does
- Parses and segments IPCC reports into discrete paragraph-level units
- Clusters them into topics using BERTopic
- Tags them with subthemes and sentiment
- Classifies them by how frequently they appear across documents (possible, plausible, probable)
- Indexes all structured signals into a single JSON file
- Generates 3–5 sentence speculative narratives using the identified signals
- Feeds the generated narrative into a explorative,React-based front-end

## Set-up Instructions
- To run the full pipeline, install: 
python scripts/pipeline/extract_text.py
python scripts/pipeline/segment_text.py
python scripts/pipeline/truncate_paragraphs.py
python scripts/pipeline/run_clustering_all.py
python scripts/pipeline/tag_all_paragraphs.py
python scripts/pipeline/compute_theme_frequencies.py
python scripts/pipeline/build_search_index.py
- Install the Bertopic model - it was excluded from this repository due to large file size whcih prevented upload to Github
- Run each.py script to transform the data step-by-step from raw PDFs to structured, tagged climate signals.
- (optional) Adjust the source metadata used during processing by running python scripts/setup/generate_metadata_template.py
- Once the search index is created, you can run the narrative generator using python scripts/core/generate_narrative.py


## Required Packages
- sentence-transformers
- bertopic
- keybert
- transformers
- sklearn
- numpy
- tqdm
- PyMuPDF

## Folder Structure
SeedProject/
├── config/                             # Metadata template per document
├── data/
│   ├── extracted_text/                 # Text extracted from PDFs
│   ├── structured_units/               # Segmented paragraphs
│   ├── structured_units_truncated/     # Truncated for model input
│   ├── tagged_signals/                 # Paragraphs tagged with themes, subthemes, sentiment
│   └── search_index.json               # Flattened, filterable index of all signals
├── scripts/                            # All processing and generation scripts
└── README.md
└── DESIGN.md

## Process that was followed for SEED 
1. Extract text from PDFs: python3 extract_text.py
2. Segment into paragraphs: python3 segment_text.py
3. Truncate paragraphs longer than 512 words: python3 truncate_paragraphs.py
4. Cluster topics with BERTopic: python3 run_clustering_all.py
5. Tag all paragraphs with themes, subthemes, and sentiment: python3 tag_all_paragraphs.py
6. Classify probability of signals, based on occurence: python3 compute_theme_frequencies.py
7. Build a searchable index: python3 build_search_index.py
8. Generate speculative narrative: python3 generate_narrative.py
9. Feed narrative output to React-based UI 


## Disclaimer on AI Use
This project was developed with support from AI-assisted tools, in accordance with the CS50 final project policy, which allows some use of AI tools provided the essence of the project remains the student’s. 

Throughout this project, I used ChatGPT as a technical assistant to accelerate my learning and development. ChatGPT helped clarify programming concepts and read through previously unfamiliar programming techniques and frameworks. For example - Bertopic was new to me and to understand it conceptually I used ChatGPT as a personal tutor. And, although I had some prior knowledge of React and building data extraction tools for pdf files, this project was more complex and larger in scope than any previous experience. This is by design - I wanted to really challenge myself with my final project to get constructive feedback on how I might grow my programming skills in the future.

I also used ChatGPT to signpost frameworks and documentation I should explore - this was especially useful for building the signal generator, as I was new to working with data at such volumes. However the logic, selection and processing of the data, the choice is scope and overall solution design, including the UI, is my own and was designed, tested and implemented by me. 
