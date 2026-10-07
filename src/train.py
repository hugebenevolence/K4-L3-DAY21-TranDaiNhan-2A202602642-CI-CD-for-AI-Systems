"""Train the Adult income classifier and record a reproducible MLflow run."""

import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score

F1_THRESHOLD = 0.65


def train(
    params: dict,
    data_path: str = "data/train_batch1.csv",
    eval_path: str = "data/holdout.csv",
) -> float:
    """Train on ``data_path`` and return positive-class F1 on the holdout set."""
    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)
    X_train, y_train = df_train.drop(columns="target"), df_train["target"]
    X_eval, y_eval = df_eval.drop(columns="target"), df_eval["target"]

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    with mlflow.start_run():
        mlflow.log_params(params)
        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_eval)
        f1 = float(f1_score(y_eval, predictions))
        accuracy = float(accuracy_score(y_eval, predictions))
        mlflow.log_metrics({"f1_score": f1, "accuracy": accuracy})
        mlflow.sklearn.log_model(model, "model")

        Path("outputs").mkdir(exist_ok=True)
        Path("models").mkdir(exist_ok=True)
        Path("outputs/report.json").write_text(
            json.dumps({"f1_score": f1, "accuracy": accuracy}, indent=2) + "\n",
            encoding="utf-8",
        )
        joblib.dump(model, "models/model.joblib")
        print(f"F1: {f1:.4f} | Accuracy: {accuracy:.4f}")
    return f1


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as file:
        train(yaml.safe_load(file))
