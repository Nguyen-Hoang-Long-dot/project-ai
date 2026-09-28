from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user_payload, get_password_hash, require_roles
from app.db.database import get_db
from app.db.models import (
    AIInteraction,
    Appointment,
    AppointmentStatus,
    Certificate,
    CheckStatus,
    DocumentStatus,
    InspectionDocument,
    ProcessDocument,
    Inspection,
    InspectionCheck,
    InspectionProfile,
    InspectionResult,
    Owner,
    User,
    UserRole,
    Vehicle,
    VehicleStatus,
)
from app.schemas.workflows import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
    CertificateCreate,
    CertificateResponse,
    CompleteProfileRequest,
    InspectionCheckResponse,
    InspectionCheckUpdate,
    InspectionDocumentCreate,
    InspectionDocumentResponse,
    OwnerCreate,
    OwnerResponse,
    OwnerUpdate,
    ProfileCreate,
    ProfileResponse,
    ProcessDocumentCreate,
    ProcessDocumentResponse,
    UserCreate,
    UserRoleUpdate,
)

router = APIRouter(tags=["Inspection Workflows"])


def as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def current_user(db: Session, payload: dict) -> User:
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản không còn tồn tại.")
    return user


def owner_for_user(db: Session, user: User) -> Owner:
    owner = db.query(Owner).filter(Owner.user_id == user.id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Chưa có hồ sơ chủ xe gắn với tài khoản.")
    return owner


def vehicle_for_user(db: Session, vehicle_id: int, user: User) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện.")
    if user.role == UserRole.OWNER and vehicle.owner.user_id != user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền truy cập phương tiện này.")
    return vehicle


@router.get("/api/owners", response_model=list[OwnerResponse])
def list_owners(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    user = current_user(db, payload)
    if user.role == UserRole.OWNER:
        return [owner_for_user(db, user)]
    if user.role not in (UserRole.ADMIN, UserRole.STAFF):
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem danh sách chủ xe.")
    return db.query(Owner).order_by(Owner.full_name).all()


@router.post("/api/owners", response_model=OwnerResponse, status_code=status.HTTP_201_CREATED)
def create_owner(
    payload: OwnerCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN, UserRole.STAFF])),
):
    owner = Owner(**payload.model_dump())
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


@router.patch("/api/owners/{owner_id}", response_model=OwnerResponse)
def update_owner(
    owner_id: int,
    payload: OwnerUpdate,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = current_user(db, auth)
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Không tìm thấy chủ xe.")
    if user.role == UserRole.OWNER and owner.user_id != user.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật hồ sơ này.")
    if user.role not in (UserRole.OWNER, UserRole.ADMIN, UserRole.STAFF):
        raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật chủ xe.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(owner, field, value)
    db.commit()
    db.refresh(owner)
    return owner


@router.delete("/api/owners/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(
    owner_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN])),
):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Không tìm thấy chủ xe.")
    if owner.vehicles:
        raise HTTPException(status_code=409, detail="Không thể xóa chủ xe còn phương tiện trong hệ thống.")
    db.delete(owner)
    db.commit()
    return None


@router.get("/api/appointments", response_model=list[AppointmentResponse])
def list_appointments(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    user = current_user(db, payload)
    query = db.query(Appointment)
    if user.role == UserRole.OWNER:
        query = query.filter(Appointment.owner_id == owner_for_user(db, user).id)
    return query.order_by(Appointment.scheduled_at.desc()).all()


@router.post("/api/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = current_user(db, auth)
    if user.role not in (UserRole.OWNER, UserRole.ADMIN, UserRole.STAFF):
        raise HTTPException(status_code=403, detail="Vai trò này không thể đặt lịch.")
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện.")
    if user.role == UserRole.OWNER and vehicle.owner.user_id != user.id:
        raise HTTPException(status_code=403, detail="Chỉ có thể đặt lịch cho phương tiện của bạn.")
    scheduled_at = as_utc(payload.scheduled_at)
    if scheduled_at <= datetime.now(UTC):
        raise HTTPException(status_code=422, detail="Thời gian hẹn phải ở tương lai.")
    duplicate = db.query(Appointment).filter(
        Appointment.vehicle_id == vehicle.id,
        Appointment.scheduled_at == scheduled_at,
    ).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="Phương tiện đã có lịch hẹn được lưu tại thời điểm này.")
    appointment = Appointment(
        vehicle_id=vehicle.id,
        owner_id=vehicle.owner_id,
        created_by_id=user.id,
        scheduled_at=scheduled_at,
        notes=payload.notes,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.patch("/api/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = current_user(db, auth)
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")
    if user.role == UserRole.OWNER:
        owner = owner_for_user(db, user)
        if appointment.owner_id != owner.id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật lịch hẹn này.")
        owner_changes = payload.model_dump(exclude_unset=True)
        if set(owner_changes) != {"status"} or payload.status != AppointmentStatus.CANCELLED or appointment.status != AppointmentStatus.PENDING:
            raise HTTPException(status_code=403, detail="Chủ xe chỉ có thể hủy lịch đang chờ xác nhận.")
    elif user.role not in (UserRole.ADMIN, UserRole.STAFF):
        raise HTTPException(status_code=403, detail="Bạn không có quyền cập nhật lịch hẹn.")
    if appointment.status in (AppointmentStatus.CANCELLED, AppointmentStatus.ARRIVED):
        raise HTTPException(status_code=409, detail="Lịch hẹn đã kết thúc hoặc bị hủy.")
    changes = payload.model_dump(exclude_unset=True)
    new_time = changes.get("scheduled_at")
    if new_time is not None:
        new_time = as_utc(new_time)
        if new_time <= datetime.now(UTC):
            raise HTTPException(status_code=422, detail="Thời gian hẹn phải ở tương lai.")
        duplicate = db.query(Appointment).filter(
            Appointment.vehicle_id == appointment.vehicle_id,
            Appointment.scheduled_at == new_time,
            Appointment.id != appointment.id,
        ).first()
        if duplicate:
            raise HTTPException(status_code=409, detail="Phương tiện đã có lịch hẹn được lưu tại thời điểm này.")
        changes["scheduled_at"] = new_time
    new_status = changes.get("status")
    if new_status == AppointmentStatus.ARRIVED:
        raise HTTPException(status_code=409, detail="Hãy tiếp nhận phương tiện để ghi nhận trạng thái Đã đến.")
    allowed_transitions = {
        AppointmentStatus.PENDING: {AppointmentStatus.CONFIRMED, AppointmentStatus.CANCELLED},
        AppointmentStatus.CONFIRMED: {AppointmentStatus.CANCELLED},
    }
    if new_status is not None and new_status != appointment.status and new_status not in allowed_transitions.get(appointment.status, set()):
        raise HTTPException(status_code=409, detail="Trạng thái lịch hẹn không thể chuyển theo yêu cầu.")
    for field, value in changes.items():
        setattr(appointment, field, value)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/api/inspection-profiles", response_model=list[ProfileResponse])
def list_profiles(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    user = current_user(db, payload)
    query = db.query(InspectionProfile)
    if user.role == UserRole.OWNER:
        owner_id = owner_for_user(db, user).id
        query = query.join(Vehicle).filter(Vehicle.owner_id == owner_id)
    return query.order_by(InspectionProfile.created_at.desc()).all()


@router.post(
    "/api/inspection-profiles",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.ADMIN, UserRole.STAFF])),
):
    user = current_user(db, auth)
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện.")
    appointment = None
    if payload.appointment_id is not None:
        appointment = db.query(Appointment).filter(Appointment.id == payload.appointment_id).first()
        if not appointment:
            raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")
        if appointment.vehicle_id != vehicle.id:
            raise HTTPException(status_code=422, detail="Lịch hẹn không thuộc phương tiện đã chọn.")
        if appointment.status == AppointmentStatus.CANCELLED:
            raise HTTPException(status_code=409, detail="Không thể tạo hồ sơ từ lịch đã hủy.")
        if appointment.status != AppointmentStatus.CONFIRMED:
            raise HTTPException(status_code=409, detail="Nhân viên cần xác nhận lịch trước khi tiếp nhận phương tiện.")
        if appointment.inspection_profile:
            raise HTTPException(status_code=409, detail="Lịch hẹn đã có hồ sơ kiểm định.")
        appointment.status = AppointmentStatus.ARRIVED
    items = [name.strip() for name in payload.check_items]
    if any(not name for name in items) or len({name.casefold() for name in items}) != len(items):
        raise HTTPException(status_code=422, detail="Danh sách hạng mục phải có tên và không trùng lặp.")
    documents = [name.strip() for name in payload.documents]
    if any(not name for name in documents) or len({name.casefold() for name in documents}) != len(documents):
        raise HTTPException(status_code=422, detail="Danh sách giấy tờ phải có tên và không trùng lặp.")
    profile = InspectionProfile(
        vehicle_id=vehicle.id,
        appointment=appointment,
        received_by_id=user.id,
        notes=payload.notes,
        checks=[InspectionCheck(item_name=name) for name in items],
        documents=[
            InspectionDocument(document_name=name, status=DocumentStatus.MISSING, updated_by_id=user.id)
            for name in documents
        ],
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.put(
    "/api/inspection-profiles/{profile_id}/checks/{check_id}",
    response_model=InspectionCheckResponse,
)
def update_inspection_check(
    profile_id: int,
    check_id: int,
    payload: InspectionCheckUpdate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.INSPECTOR])),
):
    user = current_user(db, auth)
    profile = db.query(InspectionProfile).filter(InspectionProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ kiểm định.")
    if profile.final_result is not None:
        raise HTTPException(status_code=409, detail="Hồ sơ đã được kết luận, không thể sửa hạng mục.")
    check = db.query(InspectionCheck).filter(
        InspectionCheck.id == check_id,
        InspectionCheck.profile_id == profile_id,
    ).first()
    if not check:
        raise HTTPException(status_code=404, detail="Không tìm thấy hạng mục trong hồ sơ.")
    check.status = payload.status
    check.notes = payload.notes
    check.inspected_by_id = user.id
    check.inspected_at = datetime.now(UTC)
    db.commit()
    db.refresh(check)
    return check


@router.post(
    "/api/inspection-profiles/{profile_id}/documents",
    response_model=InspectionDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_inspection_document(
    profile_id: int,
    payload: InspectionDocumentCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.ADMIN, UserRole.STAFF])),
):
    user = current_user(db, auth)
    profile = db.query(InspectionProfile).filter(InspectionProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ kiểm định.")
    if profile.final_result is not None:
        raise HTTPException(status_code=409, detail="Hồ sơ đã kết luận, không thể thêm giấy tờ.")
    if any(document.document_name.casefold() == payload.document_name.casefold() for document in profile.documents):
        raise HTTPException(status_code=409, detail="Giấy tờ này đã có trong hồ sơ.")
    document = InspectionDocument(**payload.model_dump(), profile_id=profile.id, updated_by_id=user.id)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.put(
    "/api/inspection-profiles/{profile_id}/documents/{document_id}",
    response_model=InspectionDocumentResponse,
)
def update_inspection_document(
    profile_id: int,
    document_id: int,
    payload: InspectionDocumentCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.ADMIN, UserRole.STAFF])),
):
    user = current_user(db, auth)
    profile = db.query(InspectionProfile).filter(InspectionProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ kiểm định.")
    if profile.final_result is not None:
        raise HTTPException(status_code=409, detail="Hồ sơ đã kết luận, không thể sửa giấy tờ.")
    document = db.query(InspectionDocument).filter(
        InspectionDocument.id == document_id,
        InspectionDocument.profile_id == profile_id,
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy giấy tờ trong hồ sơ.")
    duplicate = any(
        existing.id != document_id
        and existing.document_name.casefold() == payload.document_name.casefold()
        for existing in profile.documents
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="Tên giấy tờ đã tồn tại trong hồ sơ.")
    document.document_name = payload.document_name
    document.status = payload.status
    document.notes = payload.notes
    document.updated_by_id = user.id
    db.commit()
    db.refresh(document)
    return document


@router.post("/api/inspection-profiles/{profile_id}/complete", response_model=ProfileResponse)
def complete_profile(
    profile_id: int,
    payload: CompleteProfileRequest,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.INSPECTOR])),
):
    user = current_user(db, auth)
    profile = db.query(InspectionProfile).filter(InspectionProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ kiểm định.")
    if profile.final_result is not None:
        raise HTTPException(status_code=409, detail="Hồ sơ đã có kết luận cuối cùng.")
    if not profile.checks or any(check.status is None for check in profile.checks):
        raise HTTPException(status_code=409, detail="Cần nhập kết quả cho toàn bộ hạng mục trước khi kết luận.")
    if payload.result == InspectionResult.PASSED and any(
        check.status == CheckStatus.FAILED for check in profile.checks
    ):
        raise HTTPException(status_code=422, detail="Không thể kết luận Đạt khi còn hạng mục Không đạt.")
    profile.final_result = payload.result
    profile.completed_by_id = user.id
    profile.completed_at = datetime.now(UTC)
    if payload.notes:
        profile.notes = payload.notes
    db.commit()
    db.refresh(profile)
    return profile


@router.post(
    "/api/inspection-profiles/{profile_id}/certificate",
    response_model=CertificateResponse,
    status_code=status.HTTP_201_CREATED,
)
def issue_certificate(
    profile_id: int,
    payload: CertificateCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.INSPECTOR])),
):
    user = current_user(db, auth)
    profile = db.query(InspectionProfile).filter(InspectionProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ kiểm định.")
    if profile.final_result != InspectionResult.PASSED:
        raise HTTPException(status_code=409, detail="Chỉ cấp chứng nhận sau khi kiểm định viên kết luận Đạt.")
    if profile.certificate:
        raise HTTPException(status_code=409, detail="Hồ sơ đã được cấp chứng nhận.")
    expiration_date = as_utc(payload.expiration_date)
    if expiration_date <= datetime.now(UTC):
        raise HTTPException(status_code=422, detail="Ngày hết hạn phải ở tương lai.")
    now = datetime.now(UTC)
    certificate = Certificate(
        profile_id=profile.id,
        certificate_number=f"DK-{now:%Y%m%d}-{uuid4().hex[:8].upper()}",
        issued_by_id=user.id,
        expiration_date=expiration_date,
        notes=payload.notes,
    )
    vehicle = profile.vehicle
    vehicle.expiration_date = expiration_date
    days_left = (expiration_date.date() - now.date()).days
    vehicle.status = (
        VehicleStatus.EXPIRED if days_left < 0
        else VehicleStatus.WARNING if days_left <= 15
        else VehicleStatus.SAFE
    )
    db.add(certificate)
    db.add(Inspection(
        vehicle_id=vehicle.id,
        inspection_date=profile.completed_at or now,
        next_inspection_date=expiration_date,
        result=InspectionResult.PASSED,
        notes=profile.notes,
    ))
    db.commit()
    db.refresh(certificate)
    return certificate


@router.get("/api/certificates", response_model=list[CertificateResponse])
def list_certificates(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    user = current_user(db, payload)
    query = db.query(Certificate).join(InspectionProfile)
    if user.role == UserRole.OWNER:
        owner_id = owner_for_user(db, user).id
        query = query.join(Vehicle).filter(Vehicle.owner_id == owner_id)
    return query.order_by(Certificate.issued_at.desc()).all()


@router.get("/api/admin/users")
def list_users(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN])),
):
    users = db.query(User).order_by(User.id).all()
    return [
        {"id": user.id, "username": user.username, "full_name": user.full_name, "role": user.role}
        for user in users
    ]


@router.post("/api/admin/users", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN])),
):
    try:
        role = UserRole(payload.role)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Vai trò không hợp lệ.") from exc
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=409, detail="Tên đăng nhập đã tồn tại.")
    user = User(
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        role=role,
    )
    if role == UserRole.OWNER:
        user.owner = Owner(full_name=payload.full_name, phone="")
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "full_name": user.full_name, "role": user.role}


@router.patch("/api/admin/users/{user_id}/role")
def update_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.ADMIN])),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")
    if user.id == db.query(User.id).filter(User.username == auth["sub"]).scalar():
        raise HTTPException(status_code=409, detail="Không thể tự thay đổi vai trò của tài khoản đang đăng nhập.")
    try:
        user.role = UserRole(payload.role)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Vai trò không hợp lệ.") from exc
    if user.role == UserRole.OWNER and not user.owner:
        user.owner = Owner(full_name=user.full_name, phone="")
    db.commit()
    return {"id": user.id, "username": user.username, "full_name": user.full_name, "role": user.role}


@router.get("/api/ai/process-documents", response_model=list[ProcessDocumentResponse])
def list_process_documents(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN])),
):
    return db.query(ProcessDocument).order_by(ProcessDocument.title).all()


@router.post("/api/ai/process-documents", status_code=status.HTTP_201_CREATED)
def create_process_document(
    payload: ProcessDocumentCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.ADMIN])),
):
    document = ProcessDocument(**payload.model_dump(), updated_by_id=current_user(db, auth).id)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.put("/api/ai/process-documents/{document_id}", response_model=ProcessDocumentResponse)
def update_process_document(
    document_id: int,
    payload: ProcessDocumentCreate,
    db: Session = Depends(get_db),
    auth: dict = Depends(require_roles([UserRole.ADMIN])),
):
    document = db.query(ProcessDocument).filter(ProcessDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu quy trình.")
    document.title = payload.title
    document.content = payload.content
    document.updated_by_id = current_user(db, auth).id
    db.commit()
    db.refresh(document)
    return document


@router.delete("/api/ai/process-documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process_document(
    document_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles([UserRole.ADMIN])),
):
    document = db.query(ProcessDocument).filter(ProcessDocument.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu quy trình.")
    db.delete(document)
    db.commit()
    return None


@router.get("/api/vehicles/{vehicle_id}/history")
def get_vehicle_history(
    vehicle_id: int,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = current_user(db, auth)
    vehicle = vehicle_for_user(db, vehicle_id, user)
    profiles = db.query(InspectionProfile).filter(
        InspectionProfile.vehicle_id == vehicle.id,
    ).order_by(InspectionProfile.created_at.desc()).all()
    legacy = db.query(Inspection).filter(Inspection.vehicle_id == vehicle.id).all()
    return {
        "vehicle": vehicle,
        "inspection_profiles": profiles,
        "legacy_inspections": legacy,
        "certificates": db.query(Certificate)
        .join(InspectionProfile)
        .filter(InspectionProfile.vehicle_id == vehicle.id)
        .order_by(Certificate.issued_at.desc())
        .all(),
    }
