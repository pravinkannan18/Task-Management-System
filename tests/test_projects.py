from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_project():
    response = client.post("/users/", json={"email": "test@example.com", "password": "test123"})
    token = client.post("/token", data={"username": "test@example.com", "password": "test123"}).json()["access_token"]
    response = client.post("/projects/", json={"name": "Test Project", "description": "Test"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"

    response = client.get("/projects/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0