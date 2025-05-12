# SEED Backend & Data Pipeline: Phases

A step-by-step guide to building the SEED speculative futures backend, from raw data to API integration.

---

## **Phase 1: Data Extraction**
**Goal:** Extract text from raw PDFs.
- **Input:** `backend/data/raw_data/*.pdf`
- **Output:** `backend/data/extracted_text/*.json`
- **Script:** `extract_text.py`
- **Action:**
  - Run extraction script to convert PDFs to JSON text files.

---

## **Phase 2: Structuring Units**
**Goal:** Split extracted text into structured paragraphs/units.
- **Input:** `backend/data/extracted_text/*.json`
- **Output:** `backend/data/structured_units/*.json`
- **Script:** `segment_text.py`
- **Action:**
  - Run segmentation script to create paragraph/unit JSON files.

---

## **Phase 3: Truncation & Filtering**
**Goal:** Clean and truncate units for quality and length.
- **Input:** `backend/data/structured_units/*.json`
- **Output:** `backend/data/structured_units_truncated/*.json`
- **Script:** `truncate_paragraphs.py`
- **Action:**
  - Run truncation script to filter and clean units.

---

## **Phase 4: Tagging Signals**
**Goal:** Tag each unit with theme, subThemes, sentiment, etc.
- **Input:** `backend/data/structured_units_truncated/*.json`
- **Output:** `backend/data/tagged_signals/*.json`
- **Script:** `tag_all_paragraphs.py`
- **Action:**
  - Run tagging script to produce tagged signal files.

---

## **Phase 5: Merging Signals**
**Goal:** Merge all tagged signals into a single file for the API.
- **Input:** `backend/data/tagged_signals/*.json`
- **Output:** `backend/data/signals.json`
- **Script:** `merge_signals.py`
- **Action:**
  - Run merge script to create `signals.json`.
  - Validate with `validate_signals.py`.

---

## **Phase 6: Assigning Likelihood (Optional)**
**Goal:** Assign a `future_type` (probable, plausible, possible) to each signal.
- **Input:** `signals.json`
- **Output:** `signals.json` (updated)
- **Script:** `compute_theme_frequencies.py` + patch script
- **Action:**
  - Compute theme frequencies and assign likelihoods.
  - Patch signals with `future_type` field.

---

## **Phase 7: Scenario Generation**
**Goal:** Generate scenarios by sampling/grouping signals by likelihood and polarity.
- **Input:** `signals.json`
- **Output:** `scenarios.json`
- **Script:** `generate_scenarios.py`
- **Action:**
  - Run scenario generation script to create scenario objects referencing signal IDs.

---

## **Phase 8: API Integration**
**Goal:** Serve scenarios and signals via FastAPI endpoints.
- **Input:** `signals.json`, `scenarios.json`
- **Output:** API endpoints (e.g., `/api/generate-scenario`)
- **Script:** `main.py` (FastAPI app)
- **Action:**
  - Implement and test API endpoints for frontend integration.

---

## **Phase 9: Frontend Integration**
**Goal:** Connect frontend to backend API for dynamic scenario generation.
- **Input:** API endpoints
- **Output:** Interactive frontend experience
- **Action:**
  - Update frontend to POST to `/api/generate-scenario` and display results.

---

## **Phase 10: Automation & Validation**
**Goal:** Automate the pipeline and ensure data integrity.
- **Input:** All scripts and data
- **Output:** Reproducible, validated data pipeline
- **Action:**
  - Create a Makefile or shell script to run all phases.
  - Add validation and logging at each step.

---

**Tip:** After each phase, validate outputs before moving to the next phase. 