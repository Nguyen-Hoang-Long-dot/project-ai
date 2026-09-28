from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import (
    AIInteraction,
    Appointment,
    Certificate,
    Inspection,
    InspectionProfile,
    Owner,
    ProcessDocument,
    User,
    Vehicle,
)
from main import app


def token(client: TestClient, username: str, password: str) -> dict[str, str]:
    response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def remove_test_data(db: Session, username: str, plate: str, document_title: str) -> None:
    owner_user = db.query(User).filter(User.username == username).first()
    vehicle = db.query(Vehicle).filter(Vehicle.plate_number == plate).first()
    if vehicle:
        profiles = db.query(InspectionProfile).filter(InspectionProfile.vehicle_id == vehicle.id).all()
        for profile in profiles:
            db.query(Certificate).filter(Certificate.profile_id == profile.id).delete()
            db.delete(profile)
        db.query(Inspection).filter(Inspection.vehicle_id == vehicle.id).delete()
        db.query(Appointment).filter(Appointment.vehicle_id == vehicle.id).delete()
        db.delete(vehicle)
    if owner_user and owner_user.owner:
        db.delete(owner_user.owner)
    if owner_user:
        db.query(AIInteraction).filter(AIInteraction.user_id == owner_user.id).delete()
        db.delete(owner_user)
    db.query(ProcessDocument).filter(ProcessDocument.title == document_title).delete()
    db.commit()


def test_owner_to_certificate_workflow_and_safe_ai(monkeypatch):
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")
    suffix = uuid4().hex[:10]
    username = f"owner_{suffix}"
    plate = f"TEST-{suffix.upper()}"
    document_title = f"Test procedure {suffix}"
    with TestClient(app) as client:
        admin = token(client, "admin", "admin123")
        staff = token(client, "staff1", "staff123")
        inspector = token(client, "inspector1", "123456")
        try:
            response = client.post(
                "/api/auth/register",
                json={"username": username, "full_name": "Test Owner", "password": "pass123"},
            )
            assert response.status_code == 201
            owner = token(client, username, "pass123")

            expiration = (datetime.now(UTC) + timedelta(days=365)).isoformat()
            response = client.post(
                "/api/vehicles/",
                headers=owner,
                json={
                    "plate_number": plate,
                    "brand": "Demo",
                    "manufacture_year": 2020,
                    "expiration_date": expiration,
                },
            )
            assert response.status_code == 201, response.text
            vehicle_id = response.json()["id"]
            assert [item["id"] for item in client.get("/api/vehicles/", headers=owner).json()] == [vehicle_id]

            scheduled = (datetime.now(UTC) + timedelta(days=2)).replace(tzinfo=None).isoformat()
            response = client.post(
                "/api/appointments",
                headers=owner,
                json={"vehicle_id": vehicle_id, "scheduled_at": scheduled},
            )
            assert response.status_code == 201, response.text
            appointment_id = response.json()["id"]
            assert client.patch(
                f"/api/appointments/{appointment_id}",
                headers=owner,
                json={"status": "CANCELLED", "notes": "Unexpected update"},
            ).status_code == 403
            assert client.post(
                "/api/appointments",
                headers=owner,
                json={"vehicle_id": vehicle_id, "scheduled_at": scheduled},
            ).status_code == 409
            assert client.post(
                "/api/inspection-profiles",
                headers=staff,
                json={"vehicle_id": vehicle_id, "appointment_id": appointment_id},
            ).status_code == 409
            assert client.patch(
                f"/api/appointments/{appointment_id}",
                headers=staff,
                json={"status": "CONFIRMED"},
            ).status_code == 200
            conflicting_time = (datetime.now(UTC) + timedelta(days=3)).replace(tzinfo=None).isoformat()
            assert client.post(
                "/api/appointments",
                headers=owner,
                json={"vehicle_id": vehicle_id, "scheduled_at": conflicting_time},
            ).status_code == 201
            assert client.patch(
                f"/api/appointments/{appointment_id}",
                headers=staff,
                json={"scheduled_at": conflicting_time},
            ).status_code == 409

            response = client.post(
                "/api/inspection-profiles",
                headers=staff,
                json={
                    "vehicle_id": vehicle_id,
                    "appointment_id": appointment_id,
                    "check_items": ["Brakes", "Lights"],
                    "documents": ["Registration paper"],
                },
            )
            assert response.status_code == 201, response.text
            profile = response.json()
            profile_id = profile["id"]
            document = profile["documents"][0]
            assert document["status"] == "MISSING"
            response = client.put(
                f"/api/inspection-profiles/{profile_id}/documents/{document['id']}",
                headers=staff,
                json={"document_name": "Registration paper", "status": "REVIEWED"},
            )
            assert response.status_code == 200, response.text
            assert client.post(
                f"/api/inspection-profiles/{profile_id}/complete",
                headers=staff,
                json={"result": "PASSED"},
            ).status_code == 403
            assert client.post(
                f"/api/inspection-profiles/{profile_id}/complete",
                headers=inspector,
                json={"result": "PASSED"},
            ).status_code == 409

            for check in profile["checks"]:
                assert client.put(
                    f"/api/inspection-profiles/{profile_id}/checks/{check['id']}",
                    headers=inspector,
                    json={"status": "PASSED"},
                ).status_code == 200
            response = client.post(
                f"/api/inspection-profiles/{profile_id}/complete",
                headers=inspector,
                json={"result": "PASSED"},
            )
            assert response.status_code == 200, response.text
            certificate_expiration = (datetime.now(UTC) + timedelta(days=300)).isoformat()
            response = client.post(
                f"/api/inspection-profiles/{profile_id}/certificate",
                headers=inspector,
                json={"expiration_date": certificate_expiration},
            )
            assert response.status_code == 201, response.text
            assert response.json()["certificate_number"].startswith("DK-")

            response = client.post(f"/api/ai/inspection-profiles/{profile_id}/summary", headers=owner)
            assert response.status_code == 200
            assert "PASSED" in response.json()["response"]
            response = client.post(f"/api/ai/appointments/{appointment_id}/reminder", headers=owner)
            assert response.status_code == 200
            assert plate in response.json()["response"]

            response = client.post(
                "/api/ai/chat",
                headers=owner,
                json={"prompt": "Xe tôi có đạt đăng kiểm không?"},
            )
            assert response.status_code == 200
            assert response.json()["mode"] == "safety_refusal"
            assert client.get("/api/admin/users", headers=owner).status_code == 403

            response = client.post(
                "/api/ai/process-documents",
                headers=admin,
                json={
                    "title": document_title,
                    "content": "Prepare vehicle paperwork and inspection documents before the appointment.",
                },
            )
            assert response.status_code == 201, response.text
            response = client.post(
                "/api/ai/chat",
                headers=owner,
                json={"prompt": "What paperwork should I prepare for the vehicle inspection?"},
            )
            assert response.status_code == 200
            assert document_title in response.json()["response"]
        finally:
            db = SessionLocal()
            try:
                remove_test_data(db, username, plate, document_title)
            finally:
                db.close()
