import re
import unicodedata
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user_payload
from app.db.database import get_db
from app.db.models import (
    AIInteraction,
    Appointment,
    InspectionProfile,
    Owner,
    ProcessDocument,
    User,
    UserRole,
    Vehicle,
)
from app.schemas.workflows import AIConversationMessage, AITextRequest, AITextResponse

router = APIRouter(prefix="/api/ai", tags=["AI Integration"])
SAFE_LIMIT_NOTICE = (
    "AI chỉ hỗ trợ tra cứu, tóm tắt và nhắc lịch; kết luận Đạt/Không đạt thuộc thẩm quyền "
    "của kiểm định viên."
)
OUT_OF_SCOPE_REPLY = (
    "Tôi không thể dự đoán hoặc kết luận phương tiện Đạt/Không đạt. "
    "Vui lòng trao đổi với kiểm định viên để được đánh giá chuyên môn."
)


def _plain(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.casefold())
    return "".join(
        "d" if char == "đ" else char
        for char in normalized
        if unicodedata.category(char) != "Mn"
    )


def _is_inspection_decision_request(question: str) -> bool:
    text = _plain(question)
    decision_terms = (
        "dat dang kiem",
        "khong dat",
        "dau hay rot",
        "do hay rot",
        "rot khong",
        "xe dat khong",
        "xe toi dat",
        "qua dang kiem",
        "cham diem",
    )
    vehicle_context = ("xe toi", "xe nay", "phuong tien nay", "bien so", "kiem dinh")
    return any(term in text for term in decision_terms) and any(term in text for term in vehicle_context)


def _find_process_document(question: str, documents: list[ProcessDocument]) -> ProcessDocument | None:
    words = {word for word in re.findall(r"\w+", _plain(question)) if len(word) > 2}
    scored = []
    for document in documents:
        corpus = _plain(f"{document.title} {document.content}")
        score = sum(1 for word in words if word in corpus)
        if score:
            scored.append((score, document))
    return max(scored, key=lambda item: item[0])[1] if scored else None


def _request_openai(
    system: str,
    prompt: str,
    conversation: list[AIConversationMessage] | None = None,
) -> str:
    try:
        from openai import OpenAI, OpenAIError
    except ImportError as exc:
        raise HTTPException(status_code=503, detail="Thư viện AI chưa được cài đặt.") from exc
    try:
        messages = [{"role": "system", "content": system}]
        messages.extend(
            {"role": message.role, "content": message.content}
            for message in conversation or []
        )
        messages.append({"role": "user", "content": prompt})
        response = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=8.0).chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
        )
    except OpenAIError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dịch vụ AI hiện không khả dụng. Vui lòng thử lại sau.",
        ) from exc
    content = response.choices[0].message.content
    if not content:
        raise HTTPException(status_code=502, detail="Dịch vụ AI không trả về nội dung.")
    return content.strip()


def _record(db: Session, user_id: int, kind: str, prompt: str, response: str) -> None:
    db.add(AIInteraction(
        user_id=user_id,
        interaction_type=kind,
        prompt=prompt,
        response=response,
    ))
    db.commit()


def _user(db: Session, payload: dict) -> User:
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Tài khoản không còn tồn tại.")
    return user


def _assert_profile_access(db: Session, user: User, profile: InspectionProfile) -> None:
    if user.role != UserRole.OWNER:
        return
    owner = db.query(Owner).filter(Owner.user_id == user.id).first()
    if not owner or profile.vehicle.owner_id != owner.id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem hồ sơ này.")


@router.post("/chat", response_model=AITextResponse)
def ai_assistant_chat(
    payload: AITextRequest,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    question = payload.prompt.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Nội dung câu hỏi không được để trống.")
    user = _user(db, auth)
    if _is_inspection_decision_request(question):
        _record(db, user.id, "process_question", question, OUT_OF_SCOPE_REPLY)
        return {"response": OUT_OF_SCOPE_REPLY, "mode": "safety_refusal"}

    documents = db.query(ProcessDocument).all()
    source = _find_process_document(question, documents)
    if not source:
        previous_question = next(
            (message.content for message in reversed(payload.conversation) if message.role == "user"),
            "",
        )
        if previous_question:
            source = _find_process_document(f"{previous_question} {question}", documents)
    if not source:
        answer = "Chưa có tài liệu quy trình phù hợp để trả lời câu hỏi này."
        _record(db, user.id, "process_question", question, answer)
        return {"response": answer, "mode": "knowledge_base"}

    if settings.OPENAI_API_KEY:
        answer = _request_openai(
            "Bạn là trợ lý trung tâm đăng kiểm. Chỉ trả lời dựa trên tài liệu quy trình được cung cấp. "
            "Nếu tài liệu không có câu trả lời, hãy nói rõ là chưa có thông tin. Không suy đoán luật, "
            "phí hoặc chu kỳ. Không bao giờ kết luận Đạt/Không đạt thay kiểm định viên. "
            f"{SAFE_LIMIT_NOTICE}",
            f"Câu hỏi: {question}\nTài liệu nguồn ({source.title}):\n{source.content}",
            payload.conversation,
        )
        mode = "openai"
    else:
        answer = f"Theo tài liệu “{source.title}”:\n{source.content}"
        mode = "knowledge_base"
    _record(db, user.id, "process_question", question, answer)
    return {"response": answer, "mode": mode}


@router.post("/inspection-profiles/{profile_id}/summary", response_model=AITextResponse)
def summarize_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = _user(db, auth)
    profile = db.query(InspectionProfile).filter(InspectionProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ kiểm định.")
    _assert_profile_access(db, user, profile)
    vehicle = profile.vehicle
    item_lines = [
        f"- {check.item_name}: {check.status.value if check.status else 'Chưa nhập'}"
        + (f" ({check.notes})" if check.notes else "")
        for check in profile.checks
    ]
    facts = (
        f"Biển số: {vehicle.plate_number}\n"
        f"Hãng xe: {vehicle.brand}\n"
        f"Năm sản xuất: {vehicle.manufacture_year}\n"
        f"Thời điểm tiếp nhận: {profile.created_at.isoformat()}\n"
        f"Kết luận do kiểm định viên ghi nhận: "
        f"{profile.final_result.value if profile.final_result else 'Chưa có'}\n"
        "Kết quả hạng mục:\n" + ("\n".join(item_lines) if item_lines else "- Chưa có")
    )
    if settings.OPENAI_API_KEY:
        summary = _request_openai(
            "Chỉ tóm tắt dữ kiện được cung cấp, không suy diễn, dự đoán, phê duyệt hoặc thay đổi kết quả "
            "kiểm định. Nếu nêu kết luận, phải ghi rõ đó là kết luận đã được kiểm định viên ghi nhận. "
            f"{SAFE_LIMIT_NOTICE}",
            facts,
        )
        mode = "openai"
    else:
        summary = facts
        mode = "local_summary"
    answer = f"{summary}\n\nLưu ý: {SAFE_LIMIT_NOTICE}"
    _record(db, user.id, "profile_summary", f"inspection_profile:{profile.id}", answer)
    return {"response": answer, "mode": mode}


@router.post("/appointments/{appointment_id}/reminder", response_model=AITextResponse)
def generate_appointment_reminder(
    appointment_id: int,
    db: Session = Depends(get_db),
    auth: dict = Depends(get_current_user_payload),
):
    user = _user(db, auth)
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")
    if user.role == UserRole.OWNER:
        owner = db.query(Owner).filter(Owner.user_id == user.id).first()
        if not owner or appointment.owner_id != owner.id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền xem lịch hẹn này.")
    scheduled = appointment.scheduled_at.strftime("%H:%M ngày %d/%m/%Y")
    answer = (
        f"Kính gửi {appointment.owner.full_name}, hệ thống nhắc lịch đăng kiểm cho xe "
        f"{appointment.vehicle.plate_number} vào lúc {scheduled}. "
        "Vui lòng chuẩn bị hồ sơ liên quan theo hướng dẫn của trung tâm. "
        "Đây là nội dung nhắc lịch được tạo tự động; hệ thống chưa gửi tin nhắn."
    )
    _record(db, user.id, "appointment_reminder", f"appointment:{appointment.id}", answer)
    return {"response": answer, "mode": "template"}
