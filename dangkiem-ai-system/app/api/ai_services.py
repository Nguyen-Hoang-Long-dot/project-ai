from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.core.security import get_current_user_payload

router = APIRouter(prefix="/api/ai", tags=["AI Integration"])

class ChatRequest(BaseModel):
    prompt: str

@router.post("/chat")
def ai_assistant_chat(payload: ChatRequest, _: dict = Depends(get_current_user_payload)):
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Nội dung câu hỏi không được để trống.")
    
    # Giả lập phản hồi thông minh nếu chưa cấu hình OPENAI_API_KEY
    if not settings.OPENAI_API_KEY or "sk-proj" not in settings.OPENAI_API_KEY:
        q = payload.prompt.lower()
        if "chu kỳ" in q or "thời hạn" in q:
            reply = "Theo Quy định Đăng kiểm: Xe ô tô chở người đến 9 chỗ không kinh doanh vận tải sản xuất dưới 7 năm có chu kỳ đầu là 36 tháng, chu kỳ định kỳ là 24 tháng."
        elif "phí" in q or "tiền" in q:
            reply = "Chi phí kiểm định ô tô con hiện tại là 250.000 VNĐ + Phí cấp giấy chứng nhận 90.000 VNĐ (Tổng: 340.000 VNĐ)."
        else:
            reply = f"Hệ thống Đăng kiểm AI hỗ trợ: Câu hỏi '{payload.prompt}' đã được ghi nhận. Quy trình kiểm định gồm 5 công đoạn: Nhận hồ sơ -> Kiểm tra tổng quát -> Kiểm tra an toàn/khí thải -> Nộp phí -> Cấp tem."
        return {"response": reply, "mode": "simulated"}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI chuyên tư vấn quy định đăng kiểm xe cơ giới tại Việt Nam. Trả lời ngắn gọn, chính xác."},
                {"role": "user", "content": payload.prompt}
            ]
        )
        return {"response": response.choices[0].message.content, "mode": "live"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi kết nối dịch vụ AI: {str(e)}")