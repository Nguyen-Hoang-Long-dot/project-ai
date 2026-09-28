from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.db.models import InspectionResult, VehicleStatus


class VehicleBase(BaseModel):
    plate_number: str
    brand: str
    manufacture_year: int
    owner_id: int


class VehicleCreate(VehicleBase):
    expiration_date: datetime


class VehicleUpdate(BaseModel):
    brand: Optional[str] = None
    manufacture_year: Optional[int] = None
    expiration_date: Optional[datetime] = None
    status: Optional[VehicleStatus] = None


class VehicleResponse(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    expiration_date: datetime
    status: VehicleStatus


class InspectionCreate(BaseModel):
    vehicle_id: int
    next_inspection_date: datetime
    result: InspectionResult
    notes: Optional[str] = None


class InspectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    inspection_date: datetime
    next_inspection_date: datetime
    result: InspectionResult
    notes: Optional[str]