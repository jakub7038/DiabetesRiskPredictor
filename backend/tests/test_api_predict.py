import requests

BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "pred_test_user@example.com"
TEST_PASSWORD = "password123"

PAYLOAD = {
    "Age": 8,
    "BMI": 22.22222222222222,
    "DiffWalk": 0,
    "Fruits": 0,
    "GenHlth": 3,
    "HighBP": 0,
    "HighChol": 0,
    "HvyAlcoholConsump": 0,
    "MentHlth": 20,
    "PhysActivity": 1,
    "PhysHlth": 15,
    "Sex": 0,
    "Smoker": 1,
    "Stroke": 0,
    "Veggies": 0,
    "HeartDiseaseorAttack": 0
}

def get_token():
    auth = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    requests.post(f"{BASE_URL}/register", json=auth)
    res = requests.post(f"{BASE_URL}/login", json=auth)
    return res.json()['data']['access_token'] if res.status_code == 200 else None

def test_guest():
    res = requests.post(f"{BASE_URL}/predict", json=PAYLOAD)
    if res.status_code == 200 and res.json().get('is_saved') is False:
        print(res.json())
    else:
        print(f"{res.status_code}, {res.json().get('is_saved')})")

def test_user(token):
    res = requests.post(f"{BASE_URL}/predict", json=PAYLOAD, headers={"Authorization": f"Bearer {token}"})
    if res.status_code == 200 and res.json().get('is_saved') is True:
        print(res.json())
    else:
        print(f" {res.status_code}, {res.json().get('is_saved')})")

if __name__ == "__main__":
    test_guest()
    token = get_token()
    if token:
        test_user(token)
    else:
        print("Login Failed")