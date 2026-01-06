import requests

BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "pred_test_user@example.com"
TEST_PASSWORD = "password123"
"""
PAYLOAD = {
    "Age": 4,               # ~30-34 lata
    "BMI": 21.5,            # Norma
    "DiffWalk": 0,          # Brak problemów z chodzeniem
    "Fruits": 1,            # Je owoce
    "GenHlth": 2,           # Bardzo dobre zdrowie
    "HighBP": 0,            # Brak nadciśnienia
    "HighChol": 0,          # Brak cholesterolu
    "HvyAlcoholConsump": 0,
    "MentHlth": 0,          # Dobre zdrowie psychiczne
    "PhysActivity": 1,      # Aktywny
    "PhysHlth": 0,          # Dobre zdrowie fizyczne
    "Sex": 0,
    "Smoker": 0,
    "Stroke": 0,
    "Veggies": 1,
    "HeartDiseaseorAttack": 0
}
"""

PAYLOAD = {
    "Age": 10,
    "BMI": 38.5,
    "DiffWalk": 1,
    "Fruits": 0,
    "GenHlth": 5,
    "HighBP": 1,
    "HighChol": 1,
    "HvyAlcoholConsump": 0,
    "MentHlth": 5,
    "PhysActivity": 0,
    "PhysHlth": 25,
    "Sex": 1,
    "Smoker": 1,
    "Stroke": 0,
    "Veggies": 0,
    "HeartDiseaseorAttack": 1
}


def get_token():
    auth = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    requests.post(f"{BASE_URL}/register", json=auth)
    res = requests.post(f"{BASE_URL}/login", json=auth)
    return res.json()['data']['access_token'] if res.status_code == 200 else None

def test_guest():
    res = requests.post(f"{BASE_URL}/predict", json=PAYLOAD)
    print(f"Status: {res.status_code}")
    print(res.json())

def test_user(token):
    res = requests.post(
        f"{BASE_URL}/predict",
        json=PAYLOAD,
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status: {res.status_code}")
    print(res.json())

if __name__ == "__main__":
    test_guest()

    token = get_token()
    if token:
        test_user(token)
    else:
        print("Błąd logowania")
