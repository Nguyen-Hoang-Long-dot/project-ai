from datetime import UTC, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.db.database import get_db
from app.db.models import Inspection, UserRole, Vehicle, VehicleStatus
from app.schemas.vehicle import InspectionCreate, InspectionResponse

router = APIRouter(prefix="/api/inspections", tags=["Inspections"])

@router.post("/", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(
    payload: InspectionCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN, UserRole.INSPECTOR]))
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Phương tiện không tồn tại.")

    inspection = Inspection(**payload.model_dump())
    db.add(inspection)
    
    # Cập nhật hạn lưu hành mới cho xe
    vehicle.expiration_date = payload.next_inspection_date
    days_left = (payload.next_inspection_date - datetime.now(UTC)).days

    if days_left < 0:
        vehicle.status = VehicleStatus.EXPIRED
    elif days_left <= 15:
        vehicle.status = VehicleStatus.WARNING
    else:
        vehicle.status = VehicleStatus.SAFE
        
    db.commit()
    db.refresh(inspection)
    return inspection

@router.get("/vehicle/{vehicle_id}", response_model=List[InspectionResponse])
def get_inspection_history(vehicle_id: int, db: Session = Depends(get_db)):
    return db.query(Inspection).filter(Inspection.vehicle_id == vehicle_id).all()