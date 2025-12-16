import requests
import json

BASE_URL = "http://127.0.0.1:5000"
EMAIL = "useruser@example.com"
PASSWORD = "password"


def check_trends():
    resp = requests.post(f"{BASE_URL}/login", json={"email": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        print("Błąd logowania:", resp.text)
        return

    token = resp.json()['data']['access_token']

    resp = requests.get(f"{BASE_URL}/trends", headers={"Authorization": f"Bearer {token}"})

    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    check_trends()