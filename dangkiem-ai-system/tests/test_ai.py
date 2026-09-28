from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api import ai_services
from app.core.config import settings
from main import app

client = TestClient(app)


def auth_headers():
    token = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_ai_chat_response():
    response = client.post("/api/ai/chat", json={"prompt": "Chu kỳ đăng kiểm xe con"}, headers=auth_headers())
    assert response.status_code == 200
    assert "response" in response.json()


def test_ai_chat_forwards_conversation_context(monkeypatch):
    captured = {}
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-key")
    lookup_queries = []

    def find_document(question, documents):
        lookup_queries.append(question)
        if len(lookup_queries) == 1:
            return None
        return SimpleNamespace(title="Quy trình", content="Thông tin quy trình.")

    monkeypatch.setattr(ai_services, "_find_process_document", find_document)

    def fake_request_openai(system, prompt, conversation=None):
        captured["conversation"] = conversation
        return "Câu trả lời"

    monkeypatch.setattr(ai_services, "_request_openai", fake_request_openai)
    response = client.post(
        "/api/ai/chat",
        json={
            "prompt": "Câu hỏi tiếp theo",
            "conversation": [
                {"role": "user", "content": "Câu hỏi trước"},
                {"role": "assistant", "content": "Câu trả lời trước"},
            ],
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert response.json()["response"] == "Câu trả lời"
    assert [message.content for message in captured["conversation"]] == [
        "Câu hỏi trước",
        "Câu trả lời trước",
    ]
    assert lookup_queries == ["Câu hỏi tiếp theo", "Câu hỏi trước Câu hỏi tiếp theo"]