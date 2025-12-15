import requests
import json

BASE_URL = "http://127.0.0.1:5000"
SEED_EMAIL = "useruser@example.com"
SEED_PASSWORD = "password"


def test_seeder():
    response = requests.post(f"{BASE_URL}/login", json={"email": SEED_EMAIL, "password": SEED_PASSWORD})

    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return

    token = response.json()['data']['access_token']

    response = requests.get(f"{BASE_URL}/logs", headers={"Authorization": f"Bearer {token}"})

    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    test_seeder()