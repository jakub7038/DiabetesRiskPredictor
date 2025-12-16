import requests

BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "pred_test_user@example.com"
TEST_PASSWORD = "password123"

PAYLOAD = {
    "sex": 1, "age": 30, "weight": 85.5, "height": 180.0, "alcohol_drinks": 2,
    "high_bp": 0, "high_chol": 0, "stroke": 0, "diff_walk": 0, "physical_activity": 1,
    "heart_disease": 0, "smoker": 0, "ate_fruit": 1, "ate_veggie": 1,
    "gen_hlth": 2, "bad_physical_day": 1, "bad_mental_day": 2
}

def get_token():
    auth = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    requests.post(f"{BASE_URL}/register", json=auth)
    res = requests.post(f"{BASE_URL}/login", json=auth)
    return res.json()['data']['access_token'] if res.status_code == 200 else None

def test_guest():
    res = requests.post(f"{BASE_URL}/predict", json=PAYLOAD)
    if res.status_code == 200 and res.json().get('is_saved') is False:
        print("gość działa")
    else:
        print(f"{res.status_code}, {res.json().get('is_saved')})")

def test_user(token):
    res = requests.post(f"{BASE_URL}/predict", json=PAYLOAD, headers={"Authorization": f"Bearer {token}"})
    if res.status_code == 200 and res.json().get('is_saved') is True:
        print("User działa")
    else:
        print(f" {res.status_code}, {res.json().get('is_saved')})")

if __name__ == "__main__":
    test_guest()
    token = get_token()
    if token:
        test_user(token)
    else:
        print("Login Failed")