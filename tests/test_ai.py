from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def auth_headers():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_ai_chat_response():
    response = client.post("/api/ai/chat", json={"prompt": "Chu kỳ đăng kiểm xe con"}, headers=auth_headers())
    assert response.status_code == 200
    assert "response" in response.json()