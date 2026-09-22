Hệ thống quản lý đăng kiểm phương tiện có tích hợp AI
1. Mô tả bài toán

Trung tâm đăng kiểm cần quản lý phương tiện, chủ xe, lịch hẹn, hồ sơ kiểm định, kết quả hạng mục và chứng nhận. Chủ xe thường cần biết quy trình, giấy tờ và trạng thái hồ sơ. Hệ thống đang được triển khai dưới dạng backend FastAPI mô phỏng nghiệp vụ thực tế, với tích hợp AI để hỏi đáp quy trình, tóm tắt hồ sơ và sinh nhắc lịch.

2. Mục tiêu hiện tại

- Quản lý chủ xe, phương tiện, lịch hẹn, hồ sơ kiểm định, kết quả và chứng nhận.
- Tích hợp AI hỏi đáp quy trình, tóm tắt hồ sơ, sinh nhắc lịch.
- Bảo đảm AI không thay thế kết luận chuyên môn của kiểm định viên.
- Cung cấp nền tảng demo và test automation cho học tập và đánh giá.

3. Yêu cầu chức năng
3.1. Chức năng quản lý
1. Đăng nhập và phân quyền quản trị, nhân viên tiếp nhận, kiểm định viên.
2. Quản lý chủ xe và phương tiện.
3. Đặt lịch đăng kiểm.
4. Quản lý hồ sơ kiểm định và giấy tờ.
5. Nhập kết quả kiểm tra từng hạng mục.
6. Quản lý chứng nhận và ngày hết hạn.
7. Tra cứu lịch sử đăng kiểm.
8. Thống kê lượt kiểm định, hồ sơ đạt/không đạt.
3.2. Chức năng AI
1. Chatbot hỏi đáp quy trình và giấy tờ đăng kiểm.
2. AI tóm tắt hồ sơ phương tiện.
3. AI sinh tin nhắn nhắc lịch hoặc thông báo hồ sơ.
4. Yêu cầu kỹ thuật

- Backend: FastAPI
- ORM: SQLAlchemy
- CSDL: SQLite trong môi trường demo/phát triển
- Bảo mật: JWT + bcrypt
- AI Engine: mô phỏng / tích hợp tùy cấu hình OpenAI
- Có cảnh báo AI không quyết định kết quả đăng kiểm
- Có test tự động cho auth, vehicles, AI, health check

5. Dữ liệu đầu vào, đầu ra và dữ liệu hệ thống

- Dữ liệu chính: chủ xe, phương tiện, lịch hẹn, hồ sơ, kết quả hạng mục, chứng nhận.
- Đầu vào AI: tài liệu quy trình, hồ sơ phương tiện, lịch hẹn.
- Đầu ra AI: câu trả lời quy trình, tóm tắt hồ sơ, tin nhắn nhắc lịch.
- Dữ liệu môi trường: biến SECRET_KEY, DATABASE_URL, ENV, OPENAI_API_KEY.

Prompt mẫu:

System: Bạn là trợ lý trung tâm đăng kiểm. Chỉ trả lời theo quy trình được cung cấp, không kết luận đạt/không đạt thay kiểm định viên.
User: Câu hỏi: {{question}}. Tài liệu quy trình: {{process_docs}}. Hãy trả lời ngắn gọn.

6. Trạng thái triển khai hiện tại

- Hệ thống đã đáp ứng được kiến trúc API cơ bản và test suite cơ bản.
- Môi trường đã có health check và startup lifecycle rõ ràng.
- Cấu hình phụ thuộc đã được chuẩn hóa theo Pydantic v2.
- Seed dữ liệu mẫu được chạy đúng thời điểm lifecycle của app thay vì import-time side effects.

7. Hướng dẫn sử dụng AI trong từng giai đoạn SDLC

- KT1: Dùng AI phân tích lịch hẹn, hồ sơ, kết quả; thiết kế CSDL và giới hạn AI.
- KT2: Dùng AI sinh CRUD phương tiện, lịch, hồ sơ, kết quả; debug trạng thái.
- KT3: Dùng AI thiết kế prompt hỏi đáp quy trình; test câu hỏi vượt phạm vi.
- Cuối kỳ: Dùng AI viết tài liệu, báo cáo, slide và review bảo mật.

8. Mức độ khó

Trung bình: Có quy trình nghiệp vụ rõ và nhiều hồ sơ; AI cần giới hạn không thay quyết định chuyên môn.

9. Xu hướng nâng cấp production-ready

- Chuyển từ SQLite sang PostgreSQL/MySQL cho môi trường thực tế
- Tách config thành env với secret management
- Thêm monitoring, logging và health check mạnh hơn
- Bảo vệ API bằng rate limit, input validation và audit log
- Tạo CI/CD và environment separation cho dev/staging/prod

