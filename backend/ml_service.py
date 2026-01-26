import joblib
import pandas as pd
import os
import json
import numpy as np
import shap
from sklearn.linear_model import LinearRegression

try:
    import google.generativeai as genai

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        _gemini_available = True
    else:
        _gemini_available = False
        print("Nie ma API key w .env!")

except ImportError:
    _gemini_available = False
    print("Nie ma biblioteki do LLM!")

# --- ZMIENNE GLOBALNE ---
_models = {
    'logistic': None,
    'random_forest': None,
    'gradient_boost': None
}
_model_columns = None
_scaler = None # Miejsce na wczytany StandardScaler
_shap_explainer = None


def load_model():
    """Wczytuje modele, kolumny oraz skaler z plików pkl."""
    global _models, _model_columns, _scaler

    base_path = os.path.dirname(__file__)

    # Ścieżki do plików
    model_files = {
        'logistic': 'diabetes_model_logistic.pkl',
        'random_forest': 'diabetes_model_rf.pkl',
        'gradient_boost': 'diabetes_model_gb.pkl'
    }

    columns_path = os.path.join(base_path, 'model_columns.pkl')
    scaler_path = os.path.join(base_path, 'scaler.pkl') # Ścieżka do skalera

    loaded_count = 0
    for key, filename in model_files.items():
        model_path = os.path.join(base_path, filename)
        if os.path.exists(model_path):
            _models[key] = joblib.load(model_path)
            loaded_count += 1
            print(f"Loaded {key} model")
        else:
            print(f"Warning: {filename} not found")

    # Wczytywanie skalera
    if os.path.exists(scaler_path):
        _scaler = joblib.load(scaler_path)
        print("StandardScaler loaded successfully.")
    else:
        print(f"Warning: scaler.pkl not found at: {scaler_path}")

    if os.path.exists(columns_path):
        _model_columns = joblib.load(columns_path)
        print("Model columns loaded successfully.")
    else:
        print(f"Error: model_columns.pkl not found at: {columns_path}")

    if loaded_count == 0:
        print("Error: No model files loaded!")


def get_shap_explanation(model, input_scaled_df):
    """Oblicza wpływ cech na wynik przy użyciu SHAP na przeskalowanych danych."""
    global _shap_explainer

    try:
        if _shap_explainer is None:
            _shap_explainer = shap.TreeExplainer(model)

        # Używamy przeskalowanych danych do analizy
        shap_values = _shap_explainer.shap_values(input_scaled_df, check_additivity=False)

        vals = shap_values[1] if isinstance(shap_values, list) and len(shap_values) > 1 else shap_values

        if isinstance(vals, list):
            vals = vals[-1]

        values_array = vals[0] if len(vals.shape) > 1 else vals
        feature_names = input_scaled_df.columns.tolist()

        importance_dict = {name: float(val) for name, val in zip(feature_names, values_array)}
        sorted_features = sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)

        risk_factors = [f"{k}" for k, v in sorted_features[:3] if v > 0]
        protective_factors = [f"{k}" for k, v in sorted_features[-3:] if v < 0]

        return risk_factors, protective_factors

    except Exception as e:
        print(f"SHAP Error: {e}")
        return [], []


def generate_llm_advice(user_data, prediction_class, diabetes_risk, risk_factors):
    """Generuje poradę tekstową przy użyciu Google Gemini."""
    if not _gemini_available:
        return None

    class_labels = {
        0: "brak cukrzycy (zdrowy)",
        1: "stan przedcukrzycowy",
        2: "cukrzyca"
    }

    predicted_label = class_labels.get(prediction_class, "nieznany")

    prompt = f"""
    Jesteś asystentem medycznym. Użytkownik przesłał dane zdrowotne i otrzymał wynik testu AI.

    DANE PACJENTA:
    - BMI: {user_data.get('BMI')}
    - Aktywność fizyczna: {'Tak' if user_data.get('PhysActivity') else 'Nie'}
    - Palenie: {'Tak' if user_data.get('Smoker') else 'Nie'}
    - Wiek (kategoria 1-13): {user_data.get('Age')}
    - Wysokie ciśnienie: {'Tak' if user_data.get('HighBP') else 'Nie'}
    - Wysoki cholesterol: {'Tak' if user_data.get('HighChol') else 'Nie'}

    WYNIKI AI (Random Forest):
    - Predykcja modelu: {predicted_label}
    - Ryzyko zachorowania na cukrzycę (przedcukrzycowy + cukrzyca): {diabetes_risk}%
    - Główne czynniki wpływające na ten wynik (wg SHAP): {', '.join(risk_factors) if risk_factors else 'brak danych'}

    ZADANIE:
    Napisz 3 krótkie, konkretne zalecenia dla tej osoby. 
    Bądź empatyczny, ale rzeczowy. Nie używaj wstępów, wypunktuj zalecenia.
    """

    try:
        model = genai.GenerativeModel('models/gemini-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None


def predict_diabetes_risk(data, is_authenticated=False):
    """Główna funkcja predykcji (Skalowanie -> ML -> SHAP -> Gemini)."""

    if all(model is None for model in _models.values()) or _scaler is None:
        load_model()
        if all(model is None for model in _models.values()):
            return None, "All models failed to load"

    try:
        # 1. Przygotowanie surowego DataFrame
        input_df = pd.DataFrame(columns=_model_columns, dtype=float)
        input_df.loc[0] = 0.0

        mapper = {
            'HighBP': int(data.get('HighBP', 0)),
            'HighChol': int(data.get('HighChol', 0)),
            'CholCheck': int(data.get('CholCheck', 1)),
            'BMI': float(data.get('BMI', 25.0)),
            'Smoker': int(data.get('Smoker', 0)),
            'Stroke': int(data.get('Stroke', 0)),
            'HeartDiseaseorAttack': int(data.get('HeartDiseaseorAttack', 0)),
            'PhysActivity': int(data.get('PhysActivity', 0)),
            'Fruits': int(data.get('Fruits', 0)),
            'Veggies': int(data.get('Veggies', 0)),
            'HvyAlcoholConsump': int(data.get('HvyAlcoholConsump', 0)),
            'AnyHealthcare': int(data.get('AnyHealthcare', 1)),
            'NoDocbcCost': int(data.get('NoDocbcCost', 0)),
            'GenHlth': int(data.get('GenHlth', 3)),
            'MentHlth': int(data.get('MentHlth', 0)),
            'PhysHlth': int(data.get('PhysHlth', 0)),
            'DiffWalk': int(data.get('DiffWalk', 0)),
            'Sex': int(data.get('Sex', 0)),
            'Age': int(data.get('Age', 1))
        }

        for col, val in mapper.items():
            if col in input_df.columns:
                input_df.at[0, col] = val

        # 2. SKALOWANIE DANYCH - Kluczowy krok dla poprawnych wyników
        if _scaler:
            input_scaled_values = _scaler.transform(input_df)
            input_scaled_df = pd.DataFrame(input_scaled_values, columns=_model_columns)
        else:
            input_scaled_df = input_df

        predictions = {}
        rf_prediction_class = 0
        rf_diabetes_risk = 0

        # 3. Predykcja na przeskalowanych danych
        for model_name, model in _models.items():
            if model is not None:
                try:
                    prediction = model.predict(input_scaled_df)[0]
                    probabilities = model.predict_proba(input_scaled_df)[0]
                    confidence = float(round(max(probabilities) * 100, 2))

                    # Ryzyko (klasa 1 + 2)
                    diabetes_risk = float(round((probabilities[1] + probabilities[2]) * 100, 2))

                    if model_name == 'random_forest':
                        rf_prediction_class = int(prediction)
                        rf_diabetes_risk = diabetes_risk

                    predictions[model_name] = {
                        'prediction': int(prediction),
                        'probabilities': {
                            f'class_{i}': float(round(p * 100, 2)) for i, p in enumerate(probabilities)
                        },
                        'confidence': confidence,
                        'diabetes_risk': diabetes_risk
                    }
                except Exception as e:
                    print(f"Error in {model_name}: {e}")
                    predictions[model_name] = None

        # 4. SHAP & LLM (wykorzystują przeskalowane dane)
        if is_authenticated and _models['random_forest']:
            risk_factors, _ = get_shap_explanation(_models['random_forest'], input_scaled_df)

            llm_text = generate_llm_advice(
                data,
                rf_prediction_class,
                rf_diabetes_risk,
                risk_factors
            )

            if llm_text:
                predictions['llm_analysis'] = llm_text

            predictions['shap_factors'] = risk_factors

        return predictions, None

    except Exception as e:
        print(f"Prediction logic error: {e}")
        return None, str(e)


def analyze_risk_trend(history_records):
    """Analiza trendów na podstawie historycznych wyników."""
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
    predicted_future_risk = max(0, min(100, model.predict([[last_day + 30]])[0]))

    return {
        "slope": round(slope, 4),
        "trend_direction": "increasing" if slope > 0.01 else ("decreasing" if slope < -0.01 else "stable"),
        "trend_description": "Ryzyko rośnie" if slope > 0.01 else ("Ryzyko maleje" if slope < -0.01 else "Ryzyko stabilne"),
        "current_risk": y[-1],
        "predicted_risk_30d": round(predicted_future_risk, 2),
        "history_points": [
            {"day": day[0], "risk": risk, "trend_value": round(trend_val, 2)}
            for day, risk, trend_val in zip(X, y, trend_line_values)
        ]
    }