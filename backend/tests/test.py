import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:5000"
TEST_EMAIL = f"test_{int(time.time())}@example.com"
TEST_PASSWORD = "TestPassword123"


def print_json(data, label="Response"):
    """Pomocnicza funkcja do ładnego wypisywania JSON"""
    print(f"\n   🔍 {label}:")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print("   " + "-" * 40)


def seed_predictions(access_token, days=5):
    print(f"Seeding {days} predictions for trends...")
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    base_data = {
        "Sex": 1, "Age": 8, "HighBP": 0, "HighChol": 1, "Stroke": 0, "DiffWalk": 0,
        "PhysActivity": 1, "GenHlth": 3, "PhysHlth": 5, "MentHlth": 3,
        "HeartDiseaseorAttack": 0, "Smoker": 0, "Fruits": 1, "Veggies": 1,
        "HvyAlcoholConsump": 0, "BMI": 25.0
    }

    for i in range(days):
        test_data = base_data.copy()
        test_data["BMI"] = 25.0 + (i * 0.5)
        test_data["PhysActivity"] = 1 if i < 5 else 0
        requests.post(f"{BASE_URL}/predict", headers=headers, json=test_data)
        time.sleep(0.05)


def test_register():
    print("Test: Register")
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = requests.post(f"{BASE_URL}/register", json=payload)

    # WYPISYWANIE ODPOWIEDZI
    print_json(response.json(), "Rejestracja")

    return response.status_code == 201


def test_register_duplicate():
    print("Test: Register Duplicate")
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = requests.post(f"{BASE_URL}/register", json=payload)

    # WYPISYWANIE ODPOWIEDZI
    if response.status_code != 400:
        print_json(response.json(), "Błąd duplikatu (oczekiwano 400)")

    return response.status_code == 400


def test_login():
    print("Test: Login")
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = requests.post(f"{BASE_URL}/login", json=payload)

    if response.status_code == 200:
        print_json(response.json(), "Logowanie Sukces")
        return response.json()['data']['access_token']

    print_json(response.json(), "Logowanie Błąd")
    return None


def test_predict_anonymous():
    print("Test: Predict Anonymous (Should NOT have LLM)")
    test_data = {
        "Sex": 1, "Age": 8, "HighBP": 1, "HighChol": 1, "Stroke": 0, "DiffWalk": 0,
        "PhysActivity": 1, "GenHlth": 3, "PhysHlth": 10, "MentHlth": 5,
        "HeartDiseaseorAttack": 0, "Smoker": 1, "Fruits": 1, "Veggies": 1,
        "HvyAlcoholConsump": 0, "BMI": 28.5
    }
    response = requests.post(f"{BASE_URL}/predict", json=test_data)

    if response.status_code == 200:
        predictions = response.json().get('predictions', {})
        # Wypisujemy skróconą wersję (bez zagnieżdżeń), żeby nie zaśmiecać
        print(f"   📊 Wynik modeli: {list(predictions.keys())}")

        if 'llm_analysis' not in predictions:
            return True
        print("  ⚠️ Anonymous user got LLM analysis (Waste of resources!)")
        print_json(predictions, "Pełna odpowiedź")
        return False

    print_json(response.json(), "Błąd Predykcji Anonimowej")
    return False


def test_explainable_ai(access_token):
    print("Test: Explainable AI (SHAP + Gemini)")
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    # Dane wskazujące na ryzyko
    test_data = {
        "Sex": 1, "Age": 10, "HighBP": 1, "HighChol": 1, "Stroke": 0, "DiffWalk": 1,
        "PhysActivity": 0, "GenHlth": 4, "PhysHlth": 20, "MentHlth": 5,
        "HeartDiseaseorAttack": 1, "Smoker": 1, "Fruits": 0, "Veggies": 0,
        "HvyAlcoholConsump": 1, "BMI": 32.0
    }

    start_time = time.time()
    response = requests.post(f"{BASE_URL}/predict", headers=headers, json=test_data)
    duration = time.time() - start_time

    if response.status_code == 200:
        data = response.json()
        preds = data.get('predictions', {})

        # Pobieramy dane
        llm_feedback = preds.get('llm_analysis')
        shap_factors = preds.get('shap_factors', [])  # Teraz API to zwraca!

        if llm_feedback:
            print(f"  ✅ Otrzymano analizę w {round(duration, 2)}s")

            print("\n" + "=" * 60)
            print("🧠  CZYNNIKI WPŁYWU (SHAP) - To zostało wysłane do Gemini:")
            print("=" * 60)
            if shap_factors:
                for i, factor in enumerate(shap_factors, 1):
                    print(f"  {i}. {factor}")
            else:
                print("  (Brak danych SHAP)")

            print("\n" + "=" * 60)
            print("🤖  PEŁNA PORADA GEMINI:")
            print("=" * 60)
            print(llm_feedback)
            print("=" * 60 + "\n")

            return True
        else:
            print("  ⚠️ Brak pola 'llm_analysis'.")
            return True

    print(f"  ❌ Request failed: {response.status_code}")
    print(response.text)
    return False


def test_trends(access_token):
    print("Test: Get Trends")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/trends", headers=headers)

    if response.status_code == 200:
        print_json(response.json(), "Trendy")
        return True

    print_json(response.json(), "Błąd Trendów")
    return False


def run_all_tests():
    passed = 0
    total = 0

    # AUTH
    print("\n--- AUTH ---")
    if test_register():
        passed += 1;
        total += 1
    else:
        print("  FAIL Register");
        total += 1

    if test_register_duplicate():
        passed += 1;
        total += 1
    else:
        print("  FAIL Duplicate");
        total += 1

    token = test_login()
    total += 1
    if token:
        passed += 1
    else:
        print("  FAIL Login - ABORTING");
        return

    # FEATURES
    print("\n--- FEATURES ---")

    total += 1
    if test_predict_anonymous():
        passed += 1
    else:
        print("  FAIL Anon Predict")

    total += 1
    if test_explainable_ai(token):
        passed += 1
    else:
        print("  FAIL Explainable AI")

    print("\n--- SEEDING ---")
    seed_predictions(token)

    total += 1
    if test_trends(token):
        passed += 1
    else:
        print("  FAIL Trends")

    print(f"\n🎉 Result: {passed}/{total} passed.")


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        print(f"Error: {e}")