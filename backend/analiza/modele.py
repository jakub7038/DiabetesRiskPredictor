import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, StratifiedKFold
import joblib
import time

try:
    df = pd.read_csv('diabetes.csv')
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    print("❌ Error: 'diabetes.csv' not found. Please make sure the file is in the same folder.")
    exit()

required_columns = [
    'Diabetes_012', # Target (0=Healthy, 1=Pre, 2=Diabetes)
    'HighBP', 
    'HighChol', 
    'Stroke', 
    'DiffWalk', 
    'PhysActivity', 
    'GenHlth', 
    'PhysHlth', 
    'MentHlth', 
    'Sex', 
    'HeartDiseaseorAttack', 
    'Smoker', 
    'Fruits', 
    'Veggies', 
    'HvyAlcoholConsump', 
    'BMI', 
    'Age'
]

missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(f"❌ Error: The following columns are missing from diabetes.csv: {missing_cols}")
    exit()

df = df[required_columns]

X = df.drop(columns=['Diabetes_012'])
y = df['Diabetes_012']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training on {X_train.shape[0]} records using {X_train.shape[1]} features.")

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost (Gradient Boosting)": GradientBoostingClassifier(random_state=42)
}

results = {}
best_model_name = ""
best_accuracy = 0
best_model_object = None

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    print(f"\nTraining {name}...")
    start_time = time.time()

    cv_scores = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy', n_jobs=-1)
    print(f"  Cross-val: {round(cv_scores.mean() * 100, 2)}% (+/- {round(cv_scores.std() * 100, 2)}%)")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    results[name] = acc

    end_time = time.time()
    print(f"  Time: {round(end_time - start_time, 2)}s")
    print(f"  Accuracy: {round(acc * 100, 2)}%")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model_name = name
        best_model_object = model

print("\n=== FINAL RESULTS ===")
for name, acc in results.items():
    print(f"{name}: {round(acc * 100, 2)}%")

print(f"\n🏆 Best Model: {best_model_name} ({round(best_accuracy * 100, 2)}%)")

import joblib

print(f"Saving {best_model_name}...")
joblib.dump(best_model_object, 'diabetes_model.pkl')
joblib.dump(X.columns.tolist(), 'model_columns.pkl')

print("✅ SUCCESS! 'diabetes_model.pkl' and 'model_columns.pkl' created.")