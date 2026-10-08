"""ResQ prototype API. In-memory only. Triage is a deterministic rule engine (PROTOTYPE SIMULATION, not real AI)."""
from datetime import datetime, timezone
from threading import Lock
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="ResQ API (prototype)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
lock = Lock()
DEFAULT = {"phase": "idle", "offline": False, "eta": 4, "dist": 0.8, "respStatus": "AVAILABLE", "profile": None, "incId": "RQ-2026-10482", "started": False, "msgs": []}
STATE = {"version": 1, "data": dict(DEFAULT)}
VULN = {"General": 0, "Child": 14, "Senior": 12, "Mobility assistance": 12, "Speech assistance": 10,
        "Hearing assistance": 10, "Vision assistance": 10, "Cognitive assistance": 12}
SEED = [  # fictional demo incidents around Chennai
    ("RQ-10483", "Medical", "CRITICAL", "Priya", "2 min", "Responding"),
    ("RQ-10484", "Lost Person", "MEDIUM", "Unassigned", "--", "Searching"),
    ("RQ-10485", "Fire", "HIGH", "Karthik", "6 min", "Responding"),
]

class StateIn(BaseModel):
    data: dict

class TriageIn(BaseModel):
    assist: str = "General"
    trig: str = "Big SOS button"
    offline: bool = False

@app.get("/api/health")
def health():
    return {"ok": True, "time": datetime.now(timezone.utc).isoformat(), "mode": "prototype"}

@app.get("/api/state")
def get_state():
    return STATE

@app.put("/api/state")
def put_state(body: StateIn):
    bad = set(body.data) - set(DEFAULT)
    if bad:
        raise HTTPException(422, f"unknown keys: {sorted(bad)}")
    with lock:
        STATE["data"].update(body.data)
        STATE["version"] += 1
        return {"version": STATE["version"]}

@app.post("/api/reset")
def reset():
    with lock:
        saved_profile = STATE["data"].get("profile")
        STATE["data"] = dict(DEFAULT)
        if saved_profile:
            STATE["data"]["profile"] = saved_profile
        STATE["version"] += 1
    return STATE

@app.post("/api/triage")
def triage(t: TriageIn):
    score = 74 + VULN.get(t.assist, 0) + (8 if t.trig == "Automatic detection" else 3 if t.trig == "Wearable" else 0) + (5 if t.offline else 0)
    score = min(score, 99)
    sev = "CRITICAL" if score >= 90 else "HIGH" if score >= 80 else "MEDIUM" if score >= 65 else "LOW"
    why = [f"Base priority 74 for a confirmed SOS in a potentially high-risk area (demo).",
           f"Ability profile '{t.assist}': +{VULN.get(t.assist, 0)}.",
           f"Trigger '{t.trig}'.", "User was offline, SOS arrived via relay: +5." if t.offline else "User was online."]
    return {"type": "Accident", "label": "Possible road accident", "severity": sev, "priority": score,
            "confidence": round(0.88 + score / 1000, 2), "explanation": why,
            "disclaimer": "AI recommendation — responder rules override AI.", "simulated": True}

@app.get("/api/incidents")
def incidents():
    d = STATE["data"]
    live = []
    if d["phase"] != "idle":
        status = "Closed" if d["phase"] == "arrived" else "Searching" if d["phase"] == "waiting" else "Responding"
        eta = "--" if d["phase"] in ("arrived", "waiting") else f'{d["eta"]} min'
        resp = "Arun" if d["phase"] in ("accepted", "travelling", "arrived") else "Unassigned"
        live.append((d["incId"], "Accident", "HIGH", resp, eta, status))
    return [dict(zip(("id", "type", "severity", "responder", "eta", "status"), r)) for r in live + SEED]

