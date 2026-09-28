from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def auth_headers():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_vehicles_list():
    response = client.get("/api/vehicles/", headers=auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_vehicle():
    response = client.get("/api/vehicles/?q=29A", headers=auth_headers())
    assert response.status_code == 200