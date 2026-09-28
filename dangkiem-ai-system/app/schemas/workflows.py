from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.db.models import AppointmentStatus, CheckStatus, DocumentStatus, InspectionResult


class OwnerCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(default="", max_length=30)
    address: Optional[str] = Field(default=None, max_length=300)


class OwnerUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    phone: Optional[str] = Field(default=None, max_length=30)
    address: Optional[str] = Field(default=None, max_length=300)


class OwnerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    phone: str
    address: Optional[str]
    user_id: Optional[int]


class AppointmentCreate(BaseModel):
    vehicle_id: int
    scheduled_at: datetime
    notes: Optional[str] = Field(default=None, max_length=2000)


class AppointmentUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = Field(default=None, max_length=2000)


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    owner_id: int
    created_by_id: int
    scheduled_at: datetime
    status: AppointmentStatus
    notes: Optional[str]
    created_at: datetime


class ProfileCreate(BaseModel):
    vehicle_id: int
    appointment_id: Optional[int] = None
    notes: Optional[str] = Field(default=None, max_length=4000)
    check_items: list[str] = Field(
        default_factory=lambda: ["Phanh", "Khí thải", "Đèn", "Lốp"],
        min_length=1,
        max_length=50,
    )
    documents: list[str] = Field(default_factory=list, max_length=50)


class InspectionDocumentCreate(BaseModel):
    document_name: str = Field(min_length=2, max_length=160)
    status: DocumentStatus = DocumentStatus.MISSING
    notes: Optional[str] = Field(default=None, max_length=2000)


class InspectionDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_name: str
    status: DocumentStatus
    notes: Optional[str]
    updated_by_id: int
    updated_at: datetime


class InspectionCheckUpdate(BaseModel):
    status: CheckStatus
    notes: Optional[str] = Field(default=None, max_length=2000)


class InspectionCheckResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_name: str
    status: Optional[CheckStatus]
    notes: Optional[str]
    inspected_by_id: Optional[int]
    inspected_at: Optional[datetime]


class CertificateBriefResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    certificate_number: str
    expiration_date: datetime


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vehicle_id: int
    appointment_id: Optional[int]
    received_by_id: int
    notes: Optional[str]
    final_result: Optional[InspectionResult]
    completed_by_id: Optional[int]
    completed_at: Optional[datetime]
    created_at: datetime
    checks: list[InspectionCheckResponse] = Field(default_factory=list)
    documents: list[InspectionDocumentResponse] = Field(default_factory=list)
    certificate: Optional[CertificateBriefResponse] = None


class CompleteProfileRequest(BaseModel):
    result: InspectionResult
    notes: Optional[str] = Field(default=None, max_length=4000)


class CertificateCreate(BaseModel):
    expiration_date: datetime
    notes: Optional[str] = Field(default=None, max_length=2000)


class CertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile_id: int
    certificate_number: str
    issued_by_id: int
    issued_at: datetime
    expiration_date: datetime
    notes: Optional[str]


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=6, max_length=128)
    role: str


class UserRoleUpdate(BaseModel):
    role: str


class ProcessDocumentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    content: str = Field(min_length=20, max_length=20000)


class ProcessDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    updated_by_id: int
    updated_at: datetime


class AIConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class AITextRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    conversation: list[AIConversationMessage] = Field(default_factory=list, max_length=10)


class AITextResponse(BaseModel):
    response: str
    mode: str
