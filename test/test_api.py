from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_generate_password():
    response = client.post("/generate-password", json={
        "length": 10,
        "include_uppercase": True,
        "include_lowercase": True,
        "include_numbers": True,
        "include_symbols": True,
        "exclude_chars": "!@#$"
    })
    assert response.status_code == 200
    password = response.json()["password"]
    assert len(password) == 10
    assert all(c not in "!@#$" for c in password)