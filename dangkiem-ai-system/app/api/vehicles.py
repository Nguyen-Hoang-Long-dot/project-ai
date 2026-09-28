from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.database import get_db
from app.db.models import Appointment, Inspection, InspectionProfile, Owner, User, Vehicle, VehicleStatus, UserRole
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.core.security import get_current_user_payload, require_roles

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])


def status_for_expiration(expiration_date: datetime) -> VehicleStatus:
    days_left = (expiration_date.date() - datetime.now().date()).days
    if days_left < 0:
        return VehicleStatus.EXPIRED
    if days_left <= 15:
        return VehicleStatus.WARNING
    return VehicleStatus.SAFE


@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(
    q: Optional[str] = Query(None, description="Tìm theo biển số xe"),
    status: Optional[VehicleStatus] = Query(None, description="Lọc theo trạng thái"),
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    query = db.query(Vehicle)
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if user and user.role == UserRole.OWNER:
        owner = db.query(Owner).filter(Owner.user_id == user.id).first()
        if owner:
            query = query.filter(Vehicle.owner_id == owner.id)
        else:
            query = query.filter(False)
    elif user and user.role not in (UserRole.ADMIN, UserRole.STAFF, UserRole.INSPECTOR):
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem phương tiện.")
    if q:
        query = query.filter(Vehicle.plate_number.ilike(f"%{q}%"))
    if status:
        query = query.filter(Vehicle.status == status)
    return query.all()

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = db.query(User).filter(User.username == auth["sub"]).first()
    if not user or user.role not in (UserRole.ADMIN, UserRole.STAFF, UserRole.OWNER):
        raise HTTPException(status_code=403, detail="Bạn không có quyền thêm phương tiện.")
    if user.role == UserRole.OWNER:
        owner = db.query(Owner).filter(Owner.user_id == user.id).first()
        if not owner:
            raise HTTPException(status_code=409, detail="Tài khoản chưa có hồ sơ chủ xe.")
        payload = payload.model_copy(update={"owner_id": owner.id})
    elif not db.query(Owner).filter(Owner.id == payload.owner_id).first():
        raise HTTPException(status_code=404, detail="Không tìm thấy chủ xe.")
    if db.query(Vehicle).filter(Vehicle.plate_number == payload.plate_number).first():
        raise HTTPException(status_code=400, detail="Biển số xe đã tồn tại trong hệ thống.")
    
    data = payload.model_dump()
    data["expiration_date"] = (
        data["expiration_date"].astimezone(datetime.now().astimezone().tzinfo).replace(tzinfo=None)
        if data["expiration_date"].tzinfo
        else data["expiration_date"]
    )
    data["status"] = status_for_expiration(data["expiration_date"])
    vehicle = Vehicle(**data)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện.")
    user = db.query(User).filter(User.username == auth["sub"]).first()
    if user and user.role == UserRole.OWNER:
        if vehicle.owner.user_id != user.id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật phương tiện này.")
        changes = payload.model_dump(exclude_unset=True)
        if set(changes) - {"brand", "manufacture_year"}:
            raise HTTPException(status_code=403, detail="Chủ xe không thể tự thay đổi hạn đăng kiểm hoặc trạng thái.")
    elif not user or user.role not in (UserRole.ADMIN, UserRole.STAFF):
        raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật phương tiện.")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        if key == "expiration_date" and value is not None:
            value = (
                value.astimezone(datetime.now().astimezone().tzinfo).replace(tzinfo=None)
                if value.tzinfo
                else value
            )
            vehicle.status = status_for_expiration(value)
        setattr(vehicle, key, value)
    if changes.get("expiration_date") is not None:
        vehicle.status = status_for_expiration(vehicle.expiration_date)
    
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN]))
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện.")
    if db.query(InspectionProfile).filter(InspectionProfile.vehicle_id == vehicle.id).first():
        raise HTTPException(status_code=409, detail="Không thể xóa phương tiện đã có hồ sơ kiểm định.")
    if db.query(Appointment).filter(Appointment.vehicle_id == vehicle.id).first():
        raise HTTPException(status_code=409, detail="Không thể xóa phương tiện đã có lịch hẹn.")
    if db.query(Inspection).filter(Inspection.vehicle_id == vehicle.id).first():
        raise HTTPException(status_code=409, detail="Không thể xóa phương tiện đã có lịch sử kiểm định.")
    db.delete(vehicle)
    db.commit()
    return None