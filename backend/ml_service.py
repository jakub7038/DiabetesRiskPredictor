import joblib
import pandas as pd
import os
import json
import numpy as np

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
    """
    Maps raw age (e.g., 62) to the 1-13 scale required by the model.
    18-24 -> 1, 60-64 -> 9, >80 -> 13
    """
    age = int(age)
    if age < 18: return 1
    if 18 <= age <= 24: return 1
    if 25 <= age <= 29: return 2
    if 30 <= age <= 34: return 3
    if 35 <= age <= 39: return 4
    if 40 <= age <= 44: return 5
    if 45 <= age <= 49: return 6
    if 50 <= age <= 54: return 7
    if 55 <= age <= 59: return 8
    if 60 <= age <= 64: return 9
    if 65 <= age <= 69: return 10
    if 70 <= age <= 74: return 11
    if 75 <= age <= 79: return 12
    return 13 # 80+

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
        input_df = pd.DataFrame(columns=_model_columns)
        input_df.loc[0] = 0

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