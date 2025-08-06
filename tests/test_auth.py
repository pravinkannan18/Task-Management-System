from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_and_login():
    response = client.post("/users/", json={"email": "test@example.com", "password": "test123"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

    response = client.post("/token", data={"username": "test@example.com", "password": "test123"})
    assert response.status_code == 200
    assert "access_token" in response.json()