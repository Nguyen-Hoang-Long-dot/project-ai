from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.database import get_db
from app.db.models import Vehicle, VehicleStatus, UserRole
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.core.security import get_current_user_payload, require_roles

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])

@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(
    q: Optional[str] = Query(None, description="Tìm theo biển số xe"),
    status: Optional[VehicleStatus] = Query(None, description="Lọc theo trạng thái"),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user_payload),
):
    query = db.query(Vehicle)
    if q:
        query = query.filter(Vehicle.plate_number.ilike(f"%{q}%"))
    if status:
        query = query.filter(Vehicle.status == status)
    return query.all()

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN, UserRole.STAFF]))
):
    if db.query(Vehicle).filter(Vehicle.plate_number == payload.plate_number).first():
        raise HTTPException(status_code=400, detail="Biển số xe đã tồn tại trong hệ thống.")
    
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN, UserRole.STAFF]))
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện.")
    
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(vehicle, key, value)
    
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
    db.delete(vehicle)
    db.commit()
    return None