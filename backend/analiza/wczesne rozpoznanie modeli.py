import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, StratifiedKFold
import joblib
import time

df = pd.read_csv('diabetes.csv')

# wybór cech
features_to_drop = ['Income', 'Education', 'AnyHealthcare', 'NoDocbcCost', 'CholCheck']
X = df.drop(columns=['Diabetes_012'] + features_to_drop)
y = df['Diabetes_012']

# podział na zbiór treningowy i testowy 80% uczenie, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"{X_train.shape[0]}rekordów")

# definicja modeli do porównania
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
    print(f"\n{name}")
    start_time = time.time()

    cv_scores = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy', n_jobs=-1)
    print(f"Cross-val: {round(cv_scores.mean() * 100, 2)}% (+/- {round(cv_scores.std() * 100, 2)}%)")

    # uczenie
    model.fit(X_train, y_train)

    # testowanie
    y_pred = model.predict(X_test)

    # ocena
    acc = accuracy_score(y_test, y_pred)
    results[name] = acc

    end_time = time.time()
    print(f"czas: {round(end_time - start_time, 2)}s")
    print(f"dokładność : {round(acc * 100, 2)}%")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model_name = name
        best_model_object = model


print("\nwyniki")
for name, acc in results.items():
    print(f"{name}: {round(acc * 100, 2)}%")

print(f"\bnajlepszy: {best_model_name}")