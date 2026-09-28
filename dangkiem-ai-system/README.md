# Hệ thống Quản lý Đăng kiểm Xe cơ giới tích hợp AI (Nhóm 28)

Dự án là một backend FastAPI mô phỏng hệ thống quản lý đăng kiểm phương tiện có tích hợp AI, phục vụ học tập, demo nghiệp vụ và kiểm thử API. Hệ thống quản lý chủ xe, phương tiện, lịch hẹn, hồ sơ kiểm định và trạng thái lưu hành; AI chỉ hỗ trợ tìm hiểu quy trình, tóm tắt hồ sơ và nhắc lịch, không thay thế quyết định chuyên môn của kiểm định viên.

## Tính năng chính

- Quản lý tài khoản và phân quyền: ADMIN, STAFF, INSPECTOR, OWNER
- Quản lý hồ sơ chủ xe và phương tiện; chủ xe chỉ truy cập dữ liệu của mình
- Đặt lịch, xác nhận/hủy lịch và tiếp nhận phương tiện
- Tạo hồ sơ kiểm định, ghi nhận từng hạng mục và lưu kết luận do kiểm định viên nhập
- Cấp chứng nhận sau khi hồ sơ được kết luận Đạt; ngày hết hạn do người có thẩm quyền nhập
- Tra cứu lịch sử kiểm định, chứng nhận và thống kê kết quả
- Theo dõi trạng thái phương tiện: SAFE, WARNING, EXPIRED
- API thống kê dashboard
- Chatbot chỉ trả lời từ tài liệu quy trình do quản trị viên cấu hình; từ chối dự đoán kết quả
- Chatbot giữ mạch trao đổi bằng tối đa 10 tin nhắn gần nhất khi dùng OpenAI
- AI hỗ trợ tóm tắt hồ sơ và tạo nội dung nhắc lịch (không gửi tin nhắn)
- Quản trị viên quản lý tài khoản, vai trò và tài liệu quy trình cho chatbot
- Health check cho môi trường deployment
- Seed dữ liệu mẫu để demo nhanh

## Kiến trúc hiện tại

- Backend: FastAPI
- ORM: SQLAlchemy
- CSDL: SQLite cho môi trường phát triển/demo
- Bảo mật: JWT + password hashing bằng bcrypt
- Frontend demo: Jinja template + HTML tĩnh, điều hướng dọc theo phân hệ và chatbot AI luôn hiển thị cạnh nội dung
- Test: Pytest

## Cài đặt môi trường

### 1. Tạo môi trường ảo

```bash
python -m venv venv
```

### 2. Kích hoạt môi trường

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### 3. Cài đặt phụ thuộc

```bash
pip install -r requirements.txt
```

### 4. Tạo file môi trường

```bash
copy .env.example .env
```

Hoặc tạo file `.env` theo cấu trúc:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./dangkiem.db
ENV=development
OPENAI_API_KEY=
```

## Chạy ứng dụng

```bash
python -m uvicorn main:app --reload
```

Truy cập:

- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Dashboard demo: http://127.0.0.1:8000/

## Tài khoản demo

Sau khi chạy ứng dụng, dữ liệu mẫu sẽ được seed tự động:

- admin / admin123
- staff1 / staff123
- inspector1 / 123456

Chủ xe có thể đăng ký tài khoản từ màn hình đăng nhập/đăng ký.

## API quan trọng

- POST /api/auth/login
- GET /api/vehicles/
- POST /api/vehicles/
- PUT /api/vehicles/{vehicle_id}
- DELETE /api/vehicles/{vehicle_id}
- POST /api/inspections/
- GET /api/inspections/vehicle/{vehicle_id}
- GET/POST /api/appointments
- GET/POST /api/inspection-profiles
- PUT /api/inspection-profiles/{profile_id}/checks/{check_id}
- POST /api/inspection-profiles/{profile_id}/complete
- POST /api/inspection-profiles/{profile_id}/certificate
- GET /api/certificates
- POST /api/ai/inspection-profiles/{profile_id}/summary
- POST /api/ai/appointments/{appointment_id}/reminder
- GET /api/stats/summary
- POST /api/ai/chat
- GET /health
- GET /api/health

## Quy tắc AI và nghiệp vụ

Rất quan trọng:

- AI chỉ hỗ trợ tra cứu quy trình, tóm tắt hồ sơ và nhắc lịch
- Chatbot chỉ sử dụng nguồn tài liệu được quản trị viên thêm vào; nếu không có nguồn phù hợp, hệ thống thông báo chưa có thông tin thay vì tự tạo quy định
- AI không có quyền quyết định Đạt / Không đạt đăng kiểm
- Kết luận chuyên môn phải thuộc về kiểm định viên hoặc người có thẩm quyền
- Hệ thống không tự suy ra chu kỳ pháp lý hoặc ngày hết hạn chứng nhận; người có thẩm quyền cung cấp ngày này
- Khi cấu hình OpenAI, câu hỏi, tối đa 10 tin nhắn hội thoại gần nhất và tài liệu quy trình được chọn sẽ được gửi đến dịch vụ OpenAI

## Kiểm thử

```bash
pytest -q
```

Hoặc với Python cụ thể:

```bash
py -3 -m pytest -q
```

## Triển khai production-ready

Các bước cần lưu ý khi đưa lên môi trường production:

- chuyển database từ SQLite sang PostgreSQL/MySQL
- quản lý SECRET_KEY qua biến môi trường
- tách cấu hình dev/prod
- bật logging và monitoring
- thêm rate limiting và bảo mật cho API
- không để OpenAI key trong source code
- chỉ nên seed dữ liệu demo trong môi trường dev/test

## Cấu trúc thư mục

```text
app/
  api/
  core/
  db/
  schemas/
  templates/
static/
tests/
README.md
requirements.txt
main.py
```

## Ghi chú

Dự án này phù hợp cho mục đích học tập, mô phỏng nghiệp vụ và demo kỹ thuật. Nếu cần mở rộng lên môi trường sản xuất thực tế, cần bổ sung nhiều lớp bảo mật và kiểm tra dữ liệu.