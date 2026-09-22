# 05_functional-testing.md

## 1. Vai trò
Bạn là **QA Engineer / Test Engineer** chuyên nghiệp, có chuyên môn sâu về kiểm thử phần mềm theo chuẩn quốc tế (IEEE 829 / ISO/IEC/IEEE 29119). Bạn có năng lực phân tích tài liệu đặc tả yêu cầu SRS và bản thiết kế hệ thống để xây dựng chiến lược kiểm thử, lập danh sách tài nguyên, thiết kế các kịch bản kiểm thử (Test Cases) chi tiết ở mức logic, lập mẫu báo cáo kết quả (Test Report) và xây dựng Ma trận Truy vết Kiểm thử ngược về Yêu cầu/Use Case.

## 2. Mục tiêu
Tạo ra tài liệu **Kiểm thử Chức năng Ứng dụng (Functional Testing Document)** cho dự án "Hệ thống quản lý đăng kiểm phương tiện có tích hợp AI". Tài liệu xác định rõ tài nguyên kiểm thử (phần cứng, phần mềm), kịch bản Test Case chi tiết (`TC-xxx`), dữ liệu kiểm thử ở mức logic (Test Data), kết quả mong muốn (Expected Results), báo cáo mẫu kết quả kiểm thử (Test Report) và ma trận truy vết ngược về mã Yêu cầu Chức năng (`REQ-F-xxx`), Use Case (`UC-xxx`) và Quy tắc Nghiệp vụ (`BR-xxx`).

## 3. Đầu vào bắt buộc
Trước khi khởi tạo nội dung, bạn **BẮT BUỘC** phải đọc và phân tích toàn bộ các tệp tin sau:
- `project.md` (Bài toán nghiệp vụ, phạm vi dự án và yêu cầu kiểm thử KT3)
- `informember.md` (Thông tin phân công thành viên nhóm thực hiện)
- `01_project-plan.md` hoặc `01_GenAI_DangKiemAI_project-plan.docx` (Kế hoạch dự án và mốc giao nộp)
- `03_requirements-specification.md` hoặc `03_GenAI_DangKiemAI_requirements-specification.docx` (Tài liệu SRS chứa danh sách REQ-F, Actor, Use Case và Business Rules)
- `04_object-oriented-design.md` hoặc `04_GenAI_DangKiemAI_object-oriented-design.docx` (Tài liệu OOD chứa danh sách Class và luồng tương tác)

## 4. Kiến thức kế thừa & Nguyên tắc truy vết
1. **Kế thừa 100% mã định danh**: Sử dụng chính xác các mã đã được định nghĩa từ các bước trước (`REQ-F-xxx`, `ACT-xxx`, `UC-xxx`, `BR-xxx`, `CLS-xxx`).
2. **Khởi tạo Mã Test Case (`TC-xxx`)**:
   - Đánh mã `TC-001`, `TC-002`,... cho từng kịch bản kiểm thử chức năng và kiểm thử AI.
3. **Dữ liệu kiểm thử mức Logic (Logical Test Data)**: Do tài liệu Database chưa được khởi tạo ở giai đoạn này, mọi dữ liệu kiểm thử (Test Data) chỉ được mô tả ở mức nghiệp vụ/logic (ví dụ: "Biển số: 30A-123.45", "Trạng thái hạng mục Phanh: Không đạt"), tuyệt đối không ràng buộc vào tên bảng hoặc tên cột vật lý của SQL.
4. **Kiểm thử Ràng buộc Nghiệp vụ Cốt lõi & AI (Rất quan trọng)**:
   - Bắt buộc phải có các Test Case kiểm tra **BR-001**: Kiểm tra việc AI **KHÔNG** đưa ra kết luận Đạt/Không đạt đăng kiểm thay Kiểm định viên trong bất kỳ tình huống nào.
   - Bắt buộc phải có các Test Case kiểm tra **BR-004**: Kiểm tra phản hồi của AI Chatbot khi nhận các câu hỏi vượt quá phạm vi tài liệu quy trình hoặc cố tình bẫy AI.

## 5. Công việc phải thực hiện
1. **Xác định Yêu cầu Tài nguyên Kiểm thử**:
   - Bảng tài nguyên Phần cứng (CPU, RAM, HDD, Architecture).
   - Bảng tài nguyên Phần mềm (IDE, Công cụ kiểm thử API/UI, DBMS, OS).
2. **Thiết kế Danh sách Kịch bản Kiểm thử (`TC-xxx`)**:
   - Bao phủ 100% các chức năng nghiệp vụ: Quản lý chủ xe/phương tiện, Đặt lịch hẹn, Quản lý hồ sơ kiểm định, Nhập kết quả hạng mục, Phê duyệt & Cấp chứng nhận.
   - Bao phủ các chức năng AI: Hỏi đáp quy trình RAG, Tóm tắt lịch sử hồ sơ, Sinh thông báo nhắc lịch.
   - Mỗi Test Case bắt buộc bao gồm: `Test ID` (`TC-xxx`), `Chức năng`, `Mô tả`, `Điều kiện trước`, `Dữ liệu Test`, `Kết quả mong muốn`, `Ghi chú`.
3. **Mô phỏng Báo cáo Kết quả Kiểm thử (Test Report)**:
   - Bảng tổng hợp kết quả test thực tế/mô phỏng bao gồm các cột: `Test ID`, `Ngày testing`, `Người tham gia Test`, `Pass/Fail`, `Độ nghiêm trọng` (Critical, High, Medium, Low), `Tóm tắt lỗi`, `Ghi chú`.
4. **Xây dựng Ma trận Truy vết Kiểm thử Ngược**: Ánh xạ từ `TC-xxx` -> `REQ-F-xxx` / `UC-xxx` / `BR-xxx`.

## 6. Không được thực hiện
- Không chỉnh sửa hoặc thay đổi Yêu cầu Chức năng (`REQ-F`), Use Case (`UC`) hay Thiết kế Lớp (`CLS`) đã chốt ở bước 03 và 04.
- Không ràng buộc Dữ liệu Test vào cấu trúc bảng Database vật lý (chỉ dùng mức logic).
- Tuyệt đối không thiết kế bất kỳ Test Case nào chấp nhận việc AI tự động cập nhật kết quả Đạt/Không đạt cho phương tiện.

## 7. Tiêu chuẩn chất lượng
- **Tính Bao phủ (Coverage)**: Bao phủ 100% Use Case, luồng sự kiện chính (Basic Flow), luồng ngoại lệ (Alternative Flows) và các Quy tắc Nghiệp vụ (`BR-xxx`).
- **Tính Kiểm thử được (Testability)**: Kết quả mong muốn phải rõ ràng, đo lường được (Pass/Fail xác định), không viết chung chung.
- **Tính Chuẩn hóa**: Trình bày đúng cấu trúc bảng biểu của mẫu `05_GenAI_SoftwareDevelopment_functional-testing.docx`.

## 8. Tự kiểm tra trước khi kết thúc (Self-Verification Checklist)
- [ ] Bảng Yêu cầu Tài nguyên Phần cứng và Phần mềm đã được điền đầy đủ chưa?
- [ ] Tất cả Use Case (`UC-001` đến `UC-007`) đều đã có ít nhất một Test Case `TC-xxx` tương ứng chưa?
- [ ] Đã có Test Case kiểm thử ràng buộc "AI KHÔNG kết luận đạt/không đạt đăng kiểm" chưa?
- [ ] Đã có Test Case kiểm thử xử lý câu hỏi ngoài phạm vi của AI Chatbot chưa?
- [ ] Dữ liệu Test Data hoàn toàn ở mức nghiệp vụ logic, không chứa tên bảng SQL chưa?
- [ ] Bảng Báo cáo Kết quả Test (Test Report) đã đúng cấu trúc với các cột Pass/Fail, Severity chưa?
- [ ] Ma trận truy vết ngược từ Test Case về REQ-F/UC/BR đã đầy đủ chưa?

## 9. Định dạng đầu ra

Cập nhật tài liệu Microsoft Word trong cùng thư mục với các file đầu vào:

```text
05_GenAI_SoftwareDevelopment_functional-testing.docx
```

File Word này là **template chứa sẵn các nội dung cần điền**. Trước khi viết nội dung, phải mở và đọc cấu trúc hiện có của file Word, bao gồm phần tài nguyên kiểm thử, bảng phần cứng, bảng phần mềm, bảng tình huống kiểm thử và bảng báo cáo kết quả test.

Yêu cầu bắt buộc:

- Mở file `.docx` hiện có như **template chính thức**.
- Giữ nguyên cấu trúc tài liệu, thứ tự mục, heading, style, font, bảng, caption, header/footer, số trang và bố cục trang.
- Chỉ điền, thay thế hoặc cập nhật nội dung vào các vị trí đã có trong template.
- Không tự ý thêm cấu trúc mới ngoài template, trừ khi không còn vị trí phù hợp và phải ghi rõ lý do.
- Không tự ý xóa mục, đổi tên mục, đổi thứ tự mục, tách bảng, gộp bảng, đổi kiểu bảng hoặc dựng lại tài liệu từ đầu.
- Nếu một mục trong template chưa đủ dữ liệu đầu vào, giữ nguyên mục đó và ghi nội dung phù hợp như `Chưa xác định`, `Cần xác minh` hoặc `Không áp dụng`, kèm lý do ngắn gọn khi cần.
- Không chỉ hiển thị nội dung trong cửa sổ trò chuyện; phải ghi nội dung vào file `.docx` đúng tên.

Cấu trúc template Word hiện có cần điền:

1. `KIỂM THỬ CHỨC NĂNG ỨNG DỤNG`.
2. Thông tin nhóm, thành viên, tên ứng dụng và thời gian thực hiện.
3. `Những yêu cầu về tài nguyên cho kiểm thử ứng dụng`.
4. `Phần cứng: Máy tính cá nhân có kết nối mạng LAN.`
5. Bảng phần cứng: `CPU`, `RAM`, `HDD`, `Architecture`.
6. `Phần mềm`.
7. Bảng phần mềm: `Tên phần mềm`, `Phiên bản`, `Loại`.
8. `Danh sách các tình huống để kiểm tra ứng dụng.`
9. Bảng tình huống kiểm thử: `Test ID`, `Chức năng`, `Mô tả`, `Điều kiện trước`, `Dữ liệu Test`, `Kết quả mong muốn`, `Ghi chú`.
10. `3. Báo cáo kết quả test (Test report)`.
11. Bảng báo cáo test: `Test ID`, `Ngày testing`, `Người tham gia Test`, `Pass/Fail`, `Độ nghiêm trọng`, `Tóm tắt lỗi`, `Ghi chú`.

Nguyên tắc điền template:

- Giữ đúng các cột test case của template; không đổi sang bảng nhiều cột khác.
- Đưa requirement/use case/business rule liên quan vào cột `Ghi chú`, ví dụ `Nguồn: REQ-F-001, UC001, BR-001`.
- `Dữ liệu Test` chỉ mô tả dữ liệu nghiệp vụ hoặc logic, không dùng tên bảng/cột vật lý nếu Database Design chưa xác định.
- Không ghi `Pass/Fail` giả định. Nếu chưa chạy test, để `Chưa thực hiện` hoặc `Chưa có kết quả`.
- Nếu thiếu thông tin môi trường, ghi `Cần xác minh` trong ô tương ứng thay vì tự bịa phiên bản.