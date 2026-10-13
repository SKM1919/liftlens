"""LiftLens scoring service: returns uplift scores and targeting decisions."""
import json
from pathlib import Path

import pandas as pd
import xgboost as xgb
from fastapi import FastAPI
from pydantic import BaseModel

# ---------- Load the model and its config once, at startup ----------
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
config = json.loads((MODEL_DIR / "model_config.json").read_text())

FEATURES = config["features"]
CUTOFF = config["score_cutoff"]

model = xgb.XGBClassifier()
model.load_model(str(MODEL_DIR / "liftlens_s_learner.json"))

app = FastAPI(
    title="LiftLens Scoring API",
    description="Predicts how much an ad changes each user's chance of visiting, "
                "and whether they're worth targeting.",
    version="1.0.0",
)

# ---------- What a request must look like ----------
class User(BaseModel):
    f0: float
    f1: float
    f2: float
    f3: float
    f4: float
    f5: float
    f6: float
    f7: float
    f8: float
    f9: float
    f10: float
    f11: float

class ScoreRequest(BaseModel):
    users: list[User]

# ---------- Scoring logic: the same S-learner trick as the notebook ----------
def score(df: pd.DataFrame):
    with_ad = df[FEATURES].assign(treatment=1)
    without_ad = df[FEATURES].assign(treatment=0)
    return (model.predict_proba(with_ad)[:, 1]
            - model.predict_proba(without_ad)[:, 1])

# ---------- Endpoints ----------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": config["model"],
        "score_cutoff": CUTOFF,
        "target_share": config["target_share"],
        "xgboost_version": xgb.__version__,
    }

@app.post("/score")
def score_users(request: ScoreRequest):
    df = pd.DataFrame([u.model_dump() for u in request.users])
    uplift = score(df)
    results = [
        {
            "uplift_score": round(float(s), 6),
            "decision": "target" if s >= CUTOFF else "skip",
        }
        for s in uplift
    ]
    return {
        "results": results,
        "users_scored": len(results),
        "users_targeted": sum(r["decision"] == "target" for r in results),
        "note": config["calibration_note"],
    }

