import joblib
import pandas as pd
import os
import json
import numpy as np
from sklearn.linear_model import LinearRegression

# Zmiana: przechowujemy 3 modele zamiast jednego
_models = {
    'logistic': None,
    'random_forest': None,
    'gradient_boost': None
}
_model_columns = None


def load_model():
    """Loads all three model files from the backend folder."""
    global _models, _model_columns

    base_path = os.path.dirname(__file__)

    # Ładujemy 3 różne modele
    model_files = {
        'logistic': 'diabetes_model_logistic.pkl',
        'random_forest': 'diabetes_model_rf.pkl',
        'gradient_boost': 'diabetes_model_gb.pkl'
    }

    columns_path = os.path.join(base_path, 'model_columns.pkl')

    loaded_count = 0
    for key, filename in model_files.items():
        model_path = os.path.join(base_path, filename)
        if os.path.exists(model_path):
            _models[key] = joblib.load(model_path)
            loaded_count += 1
            print(f"✅ Loaded {key} model")
        else:
            print(f"⚠️ Warning: {filename} not found")

    if os.path.exists(columns_path):
        _model_columns = joblib.load(columns_path)
        print("✅ Model columns loaded successfully.")
    else:
        print(f"❌ Error: model_columns.pkl not found at: {columns_path}")

    if loaded_count == 0:
        print("❌ Error: No model files loaded!")
    else:
        print(f"✅ {loaded_count}/3 ML Models loaded successfully.")


def calculate_age_category(age):
    age = int(age)
    category = ((age - 25) // 5) + 2
    return max(1, min(13, category))


def predict_diabetes_risk(data):
    """Wykonuje predykcję używając wszystkich 3 modeli i zwraca wszystkie wyniki."""

    # Sprawdzamy czy modele są załadowane
    if all(model is None for model in _models.values()):
        load_model()
        if all(model is None for model in _models.values()):
            return None, "All models failed to load"

    try:
        # Przygotowanie danych wejściowych
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

        # Predykcja dla każdego modelu
        predictions = {}

        for model_name, model in _models.items():
            if model is not None:
                try:
                    prediction = model.predict(input_df)[0]
                    probabilities = model.predict_proba(input_df)[0]

                    predictions[model_name] = {
                        'prediction': int(prediction),
                        'probabilities': {
                            'class_0': float(round(probabilities[0] * 100, 2)),
                            'class_1': float(round(probabilities[1] * 100, 2)),
                            'class_2': float(round(probabilities[2] * 100, 2))
                        },
                        'confidence': float(round(max(probabilities) * 100, 2))
                    }
                except Exception as e:
                    print(f"Error predicting with {model_name}: {e}")
                    predictions[model_name] = None

        if not predictions or all(v is None for v in predictions.values()):
            return None, "All predictions failed"

        return predictions, None

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