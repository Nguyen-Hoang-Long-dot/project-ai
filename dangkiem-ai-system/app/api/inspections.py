from datetime import UTC, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user_payload, require_roles
from app.db.database import get_db
from app.db.models import Inspection, Owner, User, UserRole, Vehicle, VehicleStatus
from app.schemas.vehicle import InspectionCreate, InspectionResponse

router = APIRouter(prefix="/api/inspections", tags=["Inspections"])

@router.post("/", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(
    payload: InspectionCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.INSPECTOR]))
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
def get_inspection_history(
    vehicle_id: int,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = db.query(User).filter(User.username == auth["sub"]).first()
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện.")
    if user and user.role == UserRole.OWNER:
        owner = db.query(Owner).filter(Owner.user_id == user.id).first()
        if not owner or vehicle.owner_id != owner.id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền xem lịch sử phương tiện này.")
    return db.query(Inspection).filter(Inspection.vehicle_id == vehicle_id).order_by(Inspection.inspection_date.desc()).all()