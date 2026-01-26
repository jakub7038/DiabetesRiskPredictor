import pandas as pd
import numpy as np
import joblib
import time
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report

# --- 1. ŁADOWANIE I PRZYGOTOWANIE DANYCH ---
try:
    df = pd.read_csv('diabetes.csv')
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    print("❌ Error: 'diabetes.csv' not found.")
    exit()

required_columns = [
    'Diabetes_012', 'HighBP', 'HighChol', 'Stroke', 'DiffWalk', 'PhysActivity',
    'GenHlth', 'PhysHlth', 'MentHlth', 'Sex', 'HeartDiseaseorAttack',
    'Smoker', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'BMI', 'Age'
]
df = df[required_columns]

X = df.drop(columns=['Diabetes_012'])
y = df['Diabetes_012']

# --- 2. SKALOWANIE (Standardization) ---
# Wyrównujemy skale wszystkich cech (np. BMI vs Age)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Podział z zachowaniem proporcji klas (stratify=y)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training on {X_train.shape[0]} records.")

# --- 3. DEFINICJA I OPTYMALIZACJA MODELI ---

# A. Regresja Logistyczna z wagami klas
lr = LogisticRegression(max_iter=2000, class_weight='balanced', random_state=42)

# B. Random Forest z automatycznym doborem parametrów
rf_base = RandomForestClassifier(class_weight='balanced', random_state=42)
rf_params = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_leaf': [2, 4]
}
rf_search = RandomizedSearchCV(rf_base, rf_params, n_iter=5, cv=3, random_state=42, n_jobs=-1)
print("Searching for best Random Forest parameters...")
rf_search.fit(X_train, y_train)
best_rf = rf_search.best_estimator_

# C. Gradient Boosting (klasyczny Boosting)
gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)

# --- 4. TRENOWANIE I EVALUACJA ---
models_to_train = {
    "Logistic Regression": lr,
    "Random Forest": best_rf,
    "Gradient Boosting": gb
}

results = {}

for name, model in models_to_train.items():
    print(f"\nTraining {name}...")
    start_time = time.time()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    results[name] = acc

    print(f"  Accuracy: {round(acc * 100, 2)}%")
    print(classification_report(y_test, y_pred))
    print(f"  Time: {round(time.time() - start_time, 2)}s")

# --- 5. ZAPISYWANIE ---
print("\nSaving models and scaler...")

joblib.dump(lr, '../diabetes_model_logistic.pkl')
joblib.dump(best_rf, '../diabetes_model_rf.pkl')
joblib.dump(gb, '../diabetes_model_gb.pkl')

joblib.dump(scaler, '../scaler.pkl')
joblib.dump(X.columns.tolist(), '../model_columns.pkl')

print("✅ SUCCESS! All 3 models and scaler saved.")