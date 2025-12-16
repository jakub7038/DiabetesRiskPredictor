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
    """
    data: Dictionary containing patient stats (from Frontend or DB).
    Returns: (Result Class [0,1,2], Probability %)
    """
    if _model is None:
        load_model()
        if _model is None:
            return None, "Model failed to load"

    try:
        input_df = pd.DataFrame(columns=_model_columns, dtype=float)
        input_df.loc[0] = 0.0

        # Logika danych
        
        bmi_val = 25.0
        if data.get('weight') and data.get('height'):
            w = float(data['weight'])
            h = float(data['height'])
            # Wysokość w metrach
            if h > 3: h = h / 100 
            if h > 0: bmi_val = w / (h ** 2)
        
        # Logika alkoholu (HvyAlcoholConsump)
        # 1 if Male > 14 drinks/week OR Female > 7 drinks/week, else 0
        drinks = int(data.get('alcohol_drinks', 0) or 0)
        sex = int(data.get('sex', 0) or 0) # 0 = Female, 1 = Male
        
        is_heavy_drinker = 0
        if sex == 1 and drinks > 14: is_heavy_drinker = 1 
        if sex == 0 and drinks > 7: is_heavy_drinker = 1
        
        raw_age = int(data.get('age', 30))
        age_category = calculate_age_category(raw_age)


        mapper = {
            'HighBP': int(data.get('high_bp', 0) or 0),
            'HighChol': int(data.get('high_chol', 0) or 0),
            'Stroke': int(data.get('stroke', 0) or 0),
            'DiffWalk': int(data.get('diff_walk', 0) or 0),
            'PhysActivity': int(data.get('physical_activity', 0) or 0),
            'Sex': sex,
            'HeartDiseaseorAttack': int(data.get('heart_disease', 0) or 0),
            'Smoker': int(data.get('smoker', 0) or 0),
            'Fruits': int(data.get('ate_fruit', 0) or 0),
            'Veggies': int(data.get('ate_veggie', 0) or 0),
            'HvyAlcoholConsump': is_heavy_drinker,
            
            'GenHlth': int(data.get('gen_hlth', 3)), # Scale 1-5
            'PhysHlth': int(data.get('bad_physical_day', 0) or 0), # Days 0-30
            'MentHlth': int(data.get('bad_mental_day', 0) or 0),   # Days 0-30
            'BMI': float(bmi_val),
            'Age': age_category
        }

        for col, val in mapper.items():
            if col in input_df.columns:
                input_df.at[0, col] = val

        prediction = _model.predict(input_df)[0]        # 0, 1, or 2
        probabilities = _model.predict_proba(input_df)[0] 
        
        # Konwersja numpy float na python float (inaczej błąd)
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