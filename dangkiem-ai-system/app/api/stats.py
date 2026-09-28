from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Appointment, InspectionProfile, InspectionResult, Owner, User, UserRole, Vehicle, VehicleStatus
from app.core.security import get_current_user_payload

router = APIRouter(prefix="/api/stats", tags=["Dashboard Stats"])

@router.get("/summary")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    user = db.query(User).filter(User.username == payload["sub"]).first()
    vehicles = db.query(Vehicle)
    profiles = db.query(InspectionProfile)
    appointments = db.query(Appointment)
    if user and user.role == UserRole.OWNER:
        owner = db.query(Owner).filter(Owner.user_id == user.id).first()
        owner_id = owner.id if owner else -1
        vehicles = vehicles.filter(Vehicle.owner_id == owner_id)
        profiles = profiles.join(Vehicle).filter(Vehicle.owner_id == owner_id)
        appointments = appointments.filter(Appointment.owner_id == owner_id)

    total = vehicles.count()
    expired = vehicles.filter(Vehicle.status == VehicleStatus.EXPIRED).count()
    warning = vehicles.filter(Vehicle.status == VehicleStatus.WARNING).count()
    safe = vehicles.filter(Vehicle.status == VehicleStatus.SAFE).count()

    return {
        "total": total,
        "expired": expired,
        "warning": warning,
        "safe": safe,
        "safe_ratio": round((safe / total * 100), 2) if total > 0 else 0.0,
        "appointments": appointments.count(),
        "completed_inspections": profiles.filter(InspectionProfile.final_result.isnot(None)).count(),
        "passed_inspections": profiles.filter(InspectionProfile.final_result == InspectionResult.PASSED).count(),
        "failed_inspections": profiles.filter(InspectionProfile.final_result == InspectionResult.FAILED).count(),
    }