import json

import numpy as np
import pandas as pd

from src.train import train

FEATURE_NAMES = [
    "age", "workclass", "education_num", "marital_status", "occupation",
    "relationship", "sex", "capital_gain", "capital_loss", "hours_per_week",
]


def test_train_writes_metrics_and_model(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rng = np.random.default_rng(0)
    frame = pd.DataFrame(rng.random((200, len(FEATURE_NAMES))), columns=FEATURE_NAMES)
    frame["target"] = rng.integers(0, 2, size=len(frame))
    frame.iloc[:160].to_csv("train.csv", index=False)
    frame.iloc[160:].to_csv("holdout.csv", index=False)

    f1 = train(
        {"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
        data_path="train.csv",
        eval_path="holdout.csv",
    )
    report = json.loads((tmp_path / "outputs" / "report.json").read_text())
    assert isinstance(f1, float) and 0.0 <= f1 <= 1.0
    assert report["f1_score"] == f1
    assert 0.0 <= report["accuracy"] <= 1.0
    assert (tmp_path / "models" / "model.joblib").is_file()
