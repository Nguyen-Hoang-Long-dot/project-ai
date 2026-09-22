import enum
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    INSPECTOR = "INSPECTOR"

class VehicleStatus(str, enum.Enum):
    SAFE = "SAFE"           # An toàn (hạn lưu hành > 15 ngày)
    WARNING = "WARNING"     # Sắp hết hạn (<= 15 ngày)
    EXPIRED = "EXPIRED"     # Đã quá hạn

class InspectionResult(str, enum.Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STAFF, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)

    vehicles = relationship("Vehicle", back_populates="owner")

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True, nullable=False)
    brand = Column(String, nullable=False)
    manufacture_year = Column(Integer, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    status = Column(SQLEnum(VehicleStatus), default=VehicleStatus.SAFE, nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)

    owner = relationship("Owner", back_populates="vehicles")
    inspections = relationship("Inspection", back_populates="vehicle")

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    inspection_date = Column(DateTime, default=lambda: datetime.now(UTC))
    next_inspection_date = Column(DateTime, nullable=False)
    result = Column(SQLEnum(InspectionResult), nullable=False)
    notes = Column(String, nullable=True)

    vehicle = relationship("Vehicle", back_populates="inspections")