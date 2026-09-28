from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Vehicle, VehicleStatus
from app.core.security import get_current_user_payload

router = APIRouter(prefix="/api/stats", tags=["Dashboard Stats"])

@router.get("/summary")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user_payload),
):
    total = db.query(Vehicle).count()
    expired = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.EXPIRED).count()
    warning = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.WARNING).count()
    safe = db.query(Vehicle).filter(Vehicle.status == VehicleStatus.SAFE).count()

    return {
        "total": total,
        "expired": expired,
        "warning": warning,
        "safe": safe,
        "safe_ratio": round((safe / total * 100), 2) if total > 0 else 0.0
    }