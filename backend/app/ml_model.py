import math
from pathlib import Path
from typing import TypedDict

import joblib
import pandas as pd
import shap

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "model.pkl"

_artifact = joblib.load(MODEL_PATH)
_clf = _artifact["model"]
_feature_columns: list[str] = _artifact["feature_columns"]
_label_classes: list[str] = _artifact["label_classes"]
THRESHOLD: float = _artifact["threshold"]

_nofailure_idx = _label_classes.index("NoFailure")
_explainer = shap.TreeExplainer(_clf)


class SensorInput(TypedDict):
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float
    tip: str  # 'L' | 'M' | 'H'


class Reason(TypedDict):
    feature: str
    value: float
    shap_contribution: float


class PredictionResult(TypedDict):
    risk_orani: float
    ariza_tipi: str
    risk_uyarisi: bool
    gerekce: list[Reason]


def _build_feature_row(sensor: SensorInput) -> pd.DataFrame:
    temp_diff = sensor["process_temperature"] - sensor["air_temperature"]
    power_w = sensor["torque"] * (sensor["rotational_speed"] * 2 * math.pi / 60)
    tool_wear_critical = 1 if sensor["tool_wear"] >= 200 else 0

    row = {
        "Air temperature [K]": sensor["air_temperature"],
        "Process temperature [K]": sensor["process_temperature"],
        "temp_diff": temp_diff,
        "Rotational speed [rpm]": sensor["rotational_speed"],
        "Torque [Nm]": sensor["torque"],
        "power_w": power_w,
        "Tool wear [min]": sensor["tool_wear"],
        "tool_wear_critical": tool_wear_critical,
        "Type_H": 1 if sensor["tip"] == "H" else 0,
        "Type_L": 1 if sensor["tip"] == "L" else 0,
        "Type_M": 1 if sensor["tip"] == "M" else 0,
    }
    return pd.DataFrame([row])[_feature_columns]


def predict(sensor: SensorInput, top_n: int = 3) -> PredictionResult:
    X = _build_feature_row(sensor)

    proba = _clf.predict_proba(X)[0]
    risk_orani = 1 - proba[_nofailure_idx]

    failure_probs = {cls: p for cls, p in zip(_label_classes, proba) if cls != "NoFailure"}
    ariza_tipi = max(failure_probs, key=failure_probs.get)

    shap_exp = _explainer(X)
    shap_nofailure = shap_exp[:, :, _nofailure_idx].values[0]
    order = shap_nofailure.argsort()[:top_n]

    gerekce: list[Reason] = [
        {
            "feature": _feature_columns[i],
            "value": float(X.iloc[0, i]),
            "shap_contribution": float(shap_nofailure[i]),
        }
        for i in order
    ]

    return {
        "risk_orani": float(risk_orani),
        "ariza_tipi": ariza_tipi,
        "risk_uyarisi": bool(risk_orani >= THRESHOLD),
        "gerekce": gerekce,
    }
