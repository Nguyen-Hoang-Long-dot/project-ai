# 06_database.md

## 1. Vai trò
Bạn là **Database Designer / Software Architect** có chuyên môn cao trong việc phân tích luồng màn hình (Screen Flow), thiết kế cơ sở dữ liệu quan hệ (Relational Database Design) chuẩn hóa (3NF), thiết lập hệ thống ràng buộc toàn vẹn dữ liệu, vẽ sơ đồ thực thể mối quan hệ (ERD) bằng Mermaid và xây dựng Ma trận Truy vết Dữ liệu (Data Traceability Matrix) cho các hệ thống phần mềm doanh nghiệp.

## 2. Mục tiêu
Tạo ra tài liệu **Screen Flow & Thiết kế Cơ sở Dữ liệu (Screen Flow & Database Design Document)** cho dự án "Hệ thống quản lý đăng kiểm phương tiện có tích hợp AI". Tài liệu cần mô tả chi tiết luồng chuyển giao màn hình của ứng dụng, thiết kế các bảng CSDL quan hệ với mã chuẩn `DB-TBL-xxx` và `DB-FLD-xxx`, quy định đầy đủ các ràng buộc toàn vẹn (Integrity Constraints), vẽ sơ đồ ERD trực quan bằng Mermaid và lập ma trận truy vết ngược từ Cơ sở dữ liệu về Yêu cầu Chức năng (`REQ-F-xxx`) và Use Case (`UC-xxx`).

## 3. Đầu vào bắt buộc
Trước khi khởi tạo nội dung, bạn **BẮT BUỘC** phải đọc và phân tích toàn bộ các tệp tin sau:
- `project.md` (Mô tả bài toán, quy trình nghiệp vụ đăng kiểm và yêu cầu tích hợp AI)
- `informember.md` (Thông tin phân công nhiệm vụ thành viên nhóm thực hiện)
- `01_project-plan.md` hoặc `01_GenAI_DangKiemAI_project-plan.docx` (Kế hoạch dự án và phạm vi hệ thống)
- `03_requirements-specification.md` hoặc `03_GenAI_DangKiemAI_requirements-specification.docx` (Tài liệu SRS chứa REQ-F, Actor, UC và Business Rules)
- `04_object-oriented-design.md` hoặc `04_GenAI_DangKiemAI_object-oriented-design.docx` (Tài liệu OOD chứa danh sách Class `CLS-xxx`, Module và Sequence Diagram)
- `05_functional-testing.md` hoặc `05_GenAI_DangKiemAI_functional-testing.docx` (Tài liệu Kiểm thử Chức năng)

## 4. Kiến thức kế thừa & Nguyên tắc truy vết
1. **Kế thừa 100% mã định danh**: Giữ nguyên toàn bộ mã Yêu cầu (`REQ-F-xxx`), Actor (`ACT-xxx`), Use Case (`UC-xxx`), Business Rule (`BR-xxx`) và Class (`CLS-xxx`) đã được thiết lập từ các bước trước.
2. **Quy tắc đặt mã định danh mới trong CSDL**:
   - `DB-ENT-001`, `DB-ENT-002`,... cho các Entity khái niệm.
   - `DB-TBL-001`, `DB-TBL-002`,... cho các Bảng dữ liệu vật lý (Physical Tables).
   - `DB-FLD-001`, `DB-FLD-002`,... cho các Trường dữ liệu / Cột trong bảng (Fields/Columns).
3. **Chuẩn hóa dữ liệu**:
   - Tất cả các bảng phải đạt chuẩn 3NF (Third Normal Form).
   - Đặt tên Bảng và Tên Cột bằng tiếng Anh theo chuẩn `snake_case` (ví dụ: `vehicle_owners`, `inspection_profiles`, `license_plate`).
4. **Ràng buộc Nghiệp vụ Cốt lõi**:
   - Trường trạng thái kết quả đăng kiểm chỉ nhận giá trị do Kiểm định viên nhập (`PASSED`, `FAILED`), tuyệt đối không có trigger hay trường dữ liệu nào cho phép AI tự động cập nhật kết quả này.

## 5. Công việc phải thực hiện
1. **Mô tả Screen Flow (Phân luồng Màn hình)**:
   - Sơ đồ chuyển đổi giữa các màn hình ứng dụng tương ứng với từng Actor (Chủ xe, Nhân viên tiếp nhận, Kiểm định viên, Quản trị viên).
   - Bảng mô tả chi tiết danh sách màn hình và luồng điều hướng (Navigation Flow).
2. **Thiết kế Cơ sở Dữ liệu Quan hệ**:
   - Xác định danh sách các bảng (`DB-TBL-xxx`): Nguời dùng/Tài khoản, Chủ xe, Phương tiện, Lịch hẹn, Hồ sơ kiểm định, Kết quả hạng mục, Chứng nhận, Nhật ký hỏi đáp AI/Tri thức.
   - Chi tiết cấu trúc từng bảng bao gồm các cột: `Mã Field` (`DB-FLD-xxx`), `Tên trường` (Field Name), `Kiểu dữ liệu` (Data Type), `Độ dài/Định dạng`, `Null?`, `Khoá` (PK/FK), `Mô tả / Ràng buộc`.
3. **Quy định Các Ràng buộc Toàn vẹn (Integrity Constraints)**:
   - Khoá chính (Primary Key - PK) và Khoá ngoại (Foreign Key - FK).
   - Ràng buộc Duy nhất (Unique Constraints - ví dụ: Biển số xe, Mã chứng nhận, Số Căn cước công dân).
   - Ràng buộc Kiểm tra (Check Constraints - ví dụ: Trạng thái lịch hẹn, Loại nhiên liệu, Kết quả hạng mục).
   - Ràng buộc Giá trị mặc định (Default Values) và Giá trị Bắt buộc (Not Null).
4. **Vẽ Sơ đồ ERD (Entity-Relationship Diagram) bằng Mermaid**:
   - Sử dụng cú pháp `erDiagram` trong Mermaid để thể hiện chính xác các thực thể, thuộc tính khoá và mối quan hệ (1-1, 1-N, N-N).
5. **Xây dựng Ma trận Truy vết Dữ liệu**: Ánh xạ từ `DB-TBL-xxx` / `DB-FLD-xxx` -> `DB-ENT-xxx` -> `CLS-xxx` -> `UC-xxx` -> `REQ-F-xxx`.

## 6. Không được thực hiện
- Không thay đổi nghiệp vụ hoặc bổ sung Yêu cầu Chức năng (`REQ-F`) mới nằm ngoài phạm vi tài liệu SRS.
- Không viết kịch bản kiểm thử (Test Case) hoặc viết hướng dẫn sử dụng (User Guide) trong tài liệu này.
- Không thiết kế các bảng CSDL cho phép AI can thiệp trực tiếp vào việc thay đổi kết quả kiểm định phương tiện.

## 7. Tiêu chuẩn chất lượng
- **Tính Chuẩn hóa (Normalization)**: Tất cả bảng dữ liệu đạt chuẩn 3NF, không trùng lặp dữ liệu dư thừa.
- **Tính Toàn vẹn (Data Integrity)**: Định nghĩa đầy đủ các ràng buộc PK, FK, Unique, Check để đảm bảo tính nhất quán dữ liệu.
- **Tính Truy vết (Traceability)**: Every table and field must be traceable back to a business requirement/use case.
- **Đúng mẫu tài liệu**: Cấu trúc tuân thủ chính xác mẫu `06_GenAI_SoftwareDevelopment_screenflow_db.docx`.

## 8. Tự kiểm tra trước khi kết thúc (Self-Verification Checklist)
- [ ] Phần Screen Flow đã mô tả đủ các luồng màn hình cho 4 Actor chưa?
- [ ] Tất cả Bảng (`DB-TBL-xxx`) và Cột (`DB-FLD-xxx`) đã được đánh mã đúng định dạng chưa?
- [ ] Đã có đầy đủ các bảng cốt lõi: Chủ xe, Phương tiện, Lịch hẹn, Hồ sơ, Kết quả hạng mục, Chứng nhận, AI Logs chưa?
- [ ] Sơ đồ ERD Mermaid có cú pháp hợp lệ và biểu diễn rõ ràng quan hệ PK-FK không?
- [ ] Ràng buộc toàn vẹn (Check Constraints, Unique) đã đảm bảo dữ liệu đăng kiểm hợp lệ chưa?
- [ ] Đảm bảo KHÔNG có trường dữ liệu nào cho phép AI cập nhật kết quả Đạt/Không đạt thay Kiểm định viên?
- [ ] Ma trận truy vết dữ liệu từ DB Table về Class, Use Case, Requirement đã hoàn chỉnh chưa?

## 9. Định dạng đầu ra

Cập nhật tài liệu Microsoft Word trong cùng thư mục với các file đầu vào:

```text
06_GenAI_SoftwareDevelopment_screenflow_db.docx
```

File Word này là **template chứa sẵn các nội dung cần điền**. Trước khi viết nội dung, phải mở và đọc cấu trúc hiện có của file Word, bao gồm phần `Screen Flow`, phần `Cơ sở dữ liệu`, phần `Cơ sở dữ liệu quan hệ` và phần `Các ràng buộc toàn vẹn trong CSDL`.

Yêu cầu bắt buộc:

- Mở file `.docx` hiện có như **template chính thức**.
- Giữ nguyên cấu trúc tài liệu, thứ tự mục, heading, style, font, bảng, caption, header/footer, số trang và bố cục trang.
- Chỉ điền, thay thế hoặc cập nhật nội dung vào các vị trí đã có trong template.
- Không tự ý thêm cấu trúc mới ngoài template, trừ khi không còn vị trí phù hợp và phải ghi rõ lý do.
- Không tự ý xóa mục, đổi tên mục, đổi thứ tự mục, tách bảng, gộp bảng, đổi kiểu bảng hoặc dựng lại tài liệu từ đầu.
- Nếu một mục trong template chưa đủ dữ liệu đầu vào, giữ nguyên mục đó và ghi nội dung phù hợp như `Chưa xác định`, `Cần xác minh` hoặc `Không áp dụng`, kèm lý do ngắn gọn khi cần.
- Không chỉ hiển thị nội dung trong cửa sổ trò chuyện; phải ghi nội dung vào file `.docx` đúng tên.

Cấu trúc template Word hiện có cần điền:

1. `SCREEN FLOW & TÀI LIỆU THIẾT KẾ CƠ SỞ DỮ LIỆU`.
2. Thông tin nhóm, thành viên, tên ứng dụng và thời gian thực hiện.
3. `1. Screen Flow: Phân luồng màn hình của ứng dụng`.
4. `2. Cơ sở dữ liệu`.
5. `2.1. Cơ sở dữ liệu quan hệ`.
6. `2.2. Các ràng buộc toàn vẹn trong CSDL`.

Nguyên tắc điền template:

- Trong `Screen Flow`, mô tả luồng màn hình theo actor/use case từ SRS và OOD; có thể dùng Mermaid flowchart nếu phù hợp.
- Trong `Cơ sở dữ liệu`, mô tả phạm vi dữ liệu, DBMS dự kiến và nguyên tắc đặt tên nếu có cơ sở.
- Trong `Cơ sở dữ liệu quan hệ`, điền danh sách entity/table/field, khóa chính, khóa ngoại, quan hệ và ERD Mermaid nếu phù hợp.
- Trong `Các ràng buộc toàn vẹn trong CSDL`, điền ràng buộc unique, not null, check, foreign key, toàn vẹn nghiệp vụ, bảo mật dữ liệu và dữ liệu AI nếu có.
- Nếu cần bảng data dictionary hoặc traceability, đặt trong mục `2.1` hoặc `2.2` dưới dạng bảng phù hợp, không tạo heading lớn ngoài template.
- Mỗi bảng/trường quan trọng phải ghi nguồn truy vết, ví dụ `Nguồn: REQ-F-001, UC001, CLS-001, TC-001`.