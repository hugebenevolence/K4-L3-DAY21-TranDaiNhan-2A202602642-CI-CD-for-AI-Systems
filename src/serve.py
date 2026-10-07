"""FastAPI service that fetches the approved model from S3 at startup."""

import os
from pathlib import Path

import boto3
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = Path.home() / "models" / "model.joblib"
app = FastAPI()


def download_model() -> None:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    boto3.client("s3").download_file(os.environ["ARTIFACT_BUCKET"], MODEL_KEY, str(MODEL_PATH))


download_model()
model = joblib.load(MODEL_PATH)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    if len(req.features) != 10:
        raise HTTPException(status_code=400, detail="Expected 10 features (adult income)")
    features = pd.DataFrame([req.features], columns=model.feature_names_in_)
    prediction = int(model.predict(features)[0])
    return {
        "prediction": prediction,
        "label": "thu_nhap_cao" if prediction else "thu_nhap_thap",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
