import requests
import json

BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = "test_user_01@example.com"
TEST_PASSWORD = "password123"


def test_register():
    print("Testing Registration...")
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)
    print(f"Status: {response.status_code}, Response: {response.text}")


def test_login():
    print("\nTesting Login...")
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)

    if response.status_code == 200:
        data = response.json()
        print(f"Status: {response.status_code}, Token received.")
        return data['data']['access_token']
    else:
        print(f"Status: {response.status_code}, Response: {response.text}")
        return None


def test_create_log(token):
    print("\nTesting Create Log...")
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "date": "2023-12-05",
        "ate_fruit": True,
        "ate_veggie": True,
        "physical_activity": True,
        "alcohol_drinks": 1,
        "bad_mental_day": False,
        "bad_physical_day": False,
        "weight": 75.5,
        "height": 180.0
    }

    response = requests.post(f"{BASE_URL}/logs", json=payload, headers=headers)
    print(f"Status: {response.status_code}, Response: {response.text}")


def test_get_logs(token):
    print("\nTesting Get Logs...")
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BASE_URL}/logs", headers=headers)
    print(f"Status: {response.status_code}, Count: {len(response.json())}")
    if response.status_code == 200:
        print(json.dumps(response.json()[0], indent=2))


if __name__ == "__main__":
    test_register()
    token = test_login()

    if token:
        test_create_log(token)
        test_get_logs(token)