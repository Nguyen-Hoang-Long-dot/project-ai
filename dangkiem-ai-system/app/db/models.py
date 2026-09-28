import enum
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    INSPECTOR = "INSPECTOR"
    OWNER = "OWNER"

class VehicleStatus(str, enum.Enum):
    SAFE = "SAFE"           # An toàn (hạn lưu hành > 15 ngày)
    WARNING = "WARNING"     # Sắp hết hạn (<= 15 ngày)
    EXPIRED = "EXPIRED"     # Đã quá hạn

class InspectionResult(str, enum.Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"

class AppointmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    ARRIVED = "ARRIVED"

class CheckStatus(str, enum.Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"

class DocumentStatus(str, enum.Enum):
    MISSING = "MISSING"
    RECEIVED = "RECEIVED"
    REVIEWED = "REVIEWED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STAFF, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    owner = relationship("Owner", back_populates="user", uselist=False)

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)

    vehicles = relationship("Vehicle", back_populates="owner")
    user = relationship("User", back_populates="owner")

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
    appointments = relationship("Appointment", back_populates="vehicle")
    inspection_profiles = relationship("InspectionProfile", back_populates="vehicle")

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    inspection_date = Column(DateTime, default=lambda: datetime.now(UTC))
    next_inspection_date = Column(DateTime, nullable=False)
    result = Column(SQLEnum(InspectionResult), nullable=False)
    notes = Column(String, nullable=True)

    vehicle = relationship("Vehicle", back_populates="inspections")

class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        UniqueConstraint("vehicle_id", "scheduled_at", name="uq_appointment_vehicle_time"),
    )

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False, index=True)
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    vehicle = relationship("Vehicle", back_populates="appointments")
    owner = relationship("Owner")
    created_by = relationship("User")
    inspection_profile = relationship("InspectionProfile", back_populates="appointment", uselist=False)

class InspectionProfile(Base):
    __tablename__ = "inspection_profiles"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=True)
    received_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notes = Column(Text, nullable=True)
    final_result = Column(SQLEnum(InspectionResult), nullable=True)
    completed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    vehicle = relationship("Vehicle", back_populates="inspection_profiles")
    appointment = relationship("Appointment", back_populates="inspection_profile")
    received_by = relationship("User", foreign_keys=[received_by_id])
    completed_by = relationship("User", foreign_keys=[completed_by_id])
    checks = relationship("InspectionCheck", back_populates="profile", cascade="all, delete-orphan")
    documents = relationship("InspectionDocument", back_populates="profile", cascade="all, delete-orphan")
    certificate = relationship("Certificate", back_populates="profile", uselist=False)

class InspectionCheck(Base):
    __tablename__ = "inspection_checks"
    __table_args__ = (
        UniqueConstraint("profile_id", "item_name", name="uq_inspection_check_item"),
    )

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("inspection_profiles.id"), nullable=False)
    item_name = Column(String(120), nullable=False)
    status = Column(SQLEnum(CheckStatus), nullable=True)
    notes = Column(Text, nullable=True)
    inspected_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    inspected_at = Column(DateTime, nullable=True)

    profile = relationship("InspectionProfile", back_populates="checks")
    inspected_by = relationship("User")

class InspectionDocument(Base):
    __tablename__ = "inspection_documents"
    __table_args__ = (
        UniqueConstraint("profile_id", "document_name", name="uq_inspection_document_name"),
    )

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("inspection_profiles.id"), nullable=False)
    document_name = Column(String(160), nullable=False)
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.MISSING, nullable=False)
    notes = Column(Text, nullable=True)
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)

    profile = relationship("InspectionProfile", back_populates="documents")
    updated_by = relationship("User")

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("inspection_profiles.id"), unique=True, nullable=False)
    certificate_number = Column(String(40), unique=True, nullable=False, index=True)
    issued_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    issued_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)

    profile = relationship("InspectionProfile", back_populates="certificate")
    issued_by = relationship("User")

class ProcessDocument(Base):
    __tablename__ = "process_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    updated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)

    updated_by = relationship("User")

class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interaction_type = Column(String(30), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    user = relationship("User")