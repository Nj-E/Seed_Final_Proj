from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os
import random

app = FastAPI()

# Allow CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
SIGNALS_PATH = os.path.join(DATA_DIR, "signals.json")
SCENARIOS_PATH = os.path.join(DATA_DIR, "scenarios.json")

with open(SIGNALS_PATH, "r", encoding="utf-8") as f:
    SIGNALS = json.load(f)
with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
    SCENARIOS = json.load(f)

@app.get("/api/signals")
def get_signals():
    return SIGNALS

@app.get("/api/scenarios")
def get_scenarios():
    return SCENARIOS

@app.get("/api/scenarios/filter")
def filter_scenarios(
    polarity: Optional[str] = Query(None),
    likelihood: Optional[str] = Query(None)
):
    filtered = SCENARIOS
    if polarity:
        filtered = [s for s in filtered if s.get("polarity") == polarity]
    if likelihood:
        filtered = [s for s in filtered if s.get("likelihood") == likelihood]
    return filtered

@app.get("/api/signals/filter")
def filter_signals(ids: Optional[str] = Query(None)):
    if ids:
        id_list = [i.strip() for i in ids.split(",") if i.strip()]
        return [s for s in SIGNALS if s["id"] in id_list]
    return SIGNALS

@app.get("/api/signals")
def get_signals():
    with open(os.path.join(DATA_DIR, "signals.json")) as f:
        signals = json.load(f)
    return random.sample(signals, min(5, len(signals)))

@app.get("/api/scenarios")
def get_scenarios():
    with open(os.path.join(DATA_DIR, "scenarios.json")) as f:
        return json.load(f) 