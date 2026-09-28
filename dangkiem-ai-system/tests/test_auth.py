from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failed():
    response = client.post("/api/auth/login", json={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401


def test_protected_endpoints_require_login():
    assert client.get("/api/vehicles/").status_code == 401
    assert client.get("/api/stats/summary").status_code == 401
    assert client.post("/api/ai/chat", json={"prompt": "Phí đăng kiểm"}).status_code == 401