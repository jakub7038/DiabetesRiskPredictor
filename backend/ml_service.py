import joblib
import pandas as pd
import os
import json
import numpy as np
from sklearn.linear_model import LinearRegression

_model = None
_model_columns = None

def load_model():
    """Loads the model files from the backend folder."""
    global _model, _model_columns
    
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, 'diabetes_model.pkl')
    columns_path = os.path.join(base_path, 'model_columns.pkl')

    if os.path.exists(model_path) and os.path.exists(columns_path):
        _model = joblib.load(model_path)
        _model_columns = joblib.load(columns_path)
        print("✅ ML Model loaded successfully.")
    else:
        print(f"❌ Error: Model files not found. Expected at: {model_path}")

def calculate_age_category(age):
    age = int(age)

    category = ((age - 25) // 5) + 2

    return max(1, min(13, category))


def predict_diabetes_risk(data):
    if _model is None:
        load_model()
        if _model is None:
            return None, "Model failed to load"

    try:
        input_df = pd.DataFrame(columns=_model_columns, dtype=float)
        input_df.loc[0] = 0.0


        mapper = {
            'HighBP': int(data.get('HighBP', 0)),
            'HighChol': int(data.get('HighChol', 0)),
            'Stroke': int(data.get('Stroke', 0)),
            'DiffWalk': int(data.get('DiffWalk', 0)),
            'PhysActivity': int(data.get('PhysActivity', 0)),
            'Sex': int(data.get('Sex', 0)),
            'HeartDiseaseorAttack': int(data.get('HeartDiseaseorAttack', 0)),
            'Smoker': int(data.get('Smoker', 0)),
            'Fruits': int(data.get('Fruits', 0)),
            'Veggies': int(data.get('Veggies', 0)),
            'HvyAlcoholConsump': int(data.get('HvyAlcoholConsump', 0)),

            'GenHlth': int(data.get('GenHlth', 3)),
            'PhysHlth': int(data.get('PhysHlth', 0)),
            'MentHlth': int(data.get('MentHlth', 0)),

            'BMI': float(data.get('BMI', 25.0)),

            'Age': int(data.get('Age', 1))
        }

        for col, val in mapper.items():
            if col in input_df.columns:
                input_df.at[0, col] = val

        prediction = _model.predict(input_df)[0]
        probabilities = _model.predict_proba(input_df)[0]

        confidence = float(round(max(probabilities) * 100, 2))

        return int(prediction), confidence

    except Exception as e:
        print(f"Prediction Error: {e}")
        return None, str(e)


def analyze_risk_trend(history_records):

    if not history_records or len(history_records) < 2:
        return None

    records = sorted(history_records, key=lambda x: x.created_at)

    first_date = records[0].created_at

    X = []
    y = []

    for record in records:
        # upływ czasu od pierwszego pomiaru
        delta = record.created_at - first_date
        days_diff = delta.total_seconds() / (3600 * 24)

        X.append([days_diff])
        y.append(record.probability)

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]

    trend_line_values = model.predict(X)

    last_day = X[-1][0]
    future_day = last_day + 30
    predicted_future_risk = model.predict([[future_day]])[0]
    predicted_future_risk = max(0, min(100, predicted_future_risk))

    return {
        "slope": round(slope, 4),
        "trend_direction": "increasing" if slope > 0 else "decreasing",
        "trend_description": "Ryzyko rośnie" if slope > 0 else "Ryzyko maleje",
        "current_risk": y[-1],
        "predicted_risk_30d": round(predicted_future_risk, 2),
        "history_points": [
            {
                "day": day[0],
                "risk": risk,
                "trend_value": round(trend_val, 2)
            }
            for day, risk, trend_val in zip(X, y, trend_line_values)
        ]
    }