# TÁI CẤU TRÚC BỘ PROMPT PHÁT TRIỂN PHẦN MỀM — DỰ ÁN "HỆ THỐNG QUẢN LÝ ĐĂNG KIỂM PHƯƠNG TIỆN CÓ TÍCH HỢP AI"

Bạn là **Chuyên gia Prompt Engineering**, **Business Analyst**, **Software Architect**, **Database Designer**, **QA Engineer**, **Technical Writer** và **Software Development Consultant**.

Bạn có kinh nghiệm xây dựng quy trình sinh tài liệu phát triển phần mềm bằng Generative AI theo SDLC, có khả năng chuẩn hóa prompt, kiểm soát phạm vi tài liệu, bảo đảm tính nhất quán và truy vết giữa các giai đoạn.

---

## 1. Bối cảnh

### 1.1. Thông tin nhóm thực hiện

```text
Nhóm 28
1. Nguyễn Hoàng Long
2. Hoàng Trọng Tấn

Lớp: CNTT K23H
Trường: Đại học Công nghệ thông tin và Truyền thông
Khoa: Công nghệ thông tin
```

### 1.2. Thông tin dự án

Dự án: **Hệ thống quản lý đăng kiểm phương tiện có tích hợp AI**.

Trung tâm đăng kiểm cần quản lý phương tiện, chủ xe, lịch hẹn, hồ sơ kiểm định, kết quả hạng mục và chứng nhận. Chủ xe thường cần biết quy trình, giấy tờ và trạng thái hồ sơ. Hệ thống quản lý đăng kiểm ở mức mô phỏng nghiệp vụ, đồng thời tích hợp AI hỏi đáp quy trình, tóm tắt hồ sơ và sinh thông báo lịch hẹn. AI **không** được phép thay thế kết luận chuyên môn của kiểm định viên.

Tôi đã xây dựng một quy trình sử dụng AI để sinh bộ tài liệu phát triển phần mềm cho dự án này.

Hiện tại quy trình gồm các prompt Markdown:

```text
01. project-plan.md
02 requirements-qa.md
03 requirements-specification.md
04. object-oriented-design.md
05. functional-testing.md
06. đatabase.md
```

Khi tái cấu trúc, cần chuẩn hóa tên các prompt đầu ra theo quy ước thống nhất:

```text
01_project-plan.md
02_requirements-qa.md
03_requirements-specification.md
04_object-oriented-design.md
05_functional-testing.md
06_database.md
07_user-guide.md
```

Các tài liệu Word đã hoặc sẽ được sinh từ các prompt này (đặt tên theo mã dự án `GenAI_DangKiemAI`):

```text
01_GenAI_DangKiemAI_project-plan.docx
02_GenAI_DangKiemAI_requirements-qa.docx
03_GenAI_DangKiemAI_requirements-specification.docx
04_GenAI_DangKiemAI_object-oriented-design.docx
05_GenAI_DangKiemAI_functional-testing.docx
06_GenAI_DangKiemAI_screenflow_db.docx
07_GenAI_DangKiemAI_user-guide.docx
```

Ngoài ra có hai tài liệu đầu vào bắt buộc cho toàn bộ pipeline:

```text
project.md
informember.md
```

---

## 2. Mục tiêu

Hãy viết lại toàn bộ các prompt Markdown để tạo thành một **Pipeline Prompt hoàn chỉnh**, áp dụng riêng cho dự án Hệ thống quản lý đăng kiểm phương tiện có tích hợp AI, nhưng vẫn giữ khả năng tái sử dụng cho các dự án phát triển phần mềm khác nếu thay tài liệu đầu vào.

Các prompt mới phải:

- Có cấu trúc thống nhất.
- Phân chia nhiệm vụ rõ ràng theo từng giai đoạn SDLC.
- Không tạo nội dung trùng lặp giữa các tài liệu.
- Không sinh nội dung nằm ngoài phạm vi của từng giai đoạn.
- Kế thừa chính xác kết quả từ các prompt trước.
- Bảo đảm khả năng truy vết từ yêu cầu ban đầu đến thiết kế, cơ sở dữ liệu, kiểm thử và hướng dẫn sử dụng.
- Luôn giữ đúng ràng buộc nghiệp vụ cốt lõi của dự án: **AI hỗ trợ hỏi đáp quy trình, tóm tắt hồ sơ, nhắc lịch — không được kết luận đạt/không đạt thay kiểm định viên.**

---

## 3. Phạm vi thực hiện

### Được thực hiện

- Đọc và phân tích `project.md` và `informember.md`.
- Đọc và phân tích các tài liệu Word đã sinh (nếu có).
- Đọc và phân tích các prompt Markdown hiện tại.
- Thiết kế lại toàn bộ prompt Markdown theo cùng một chuẩn, áp dụng cho phạm vi nghiệp vụ đăng kiểm phương tiện.
- Bổ sung prompt còn thiếu cho tài liệu hướng dẫn sử dụng:

```text
07_user-guide.md
```

### Không được thực hiện

- Không chỉnh sửa các file Word.
- Không viết lại nội dung dự án cụ thể vượt ra ngoài những gì `project.md` và `informember.md` đã cung cấp.
- Không tạo tài liệu đầu ra thay cho các prompt.
- Không tự ý giả định thông tin không có trong tài liệu đầu vào (ví dụ: quy định pháp lý đăng kiểm cụ thể, biểu phí, thời hạn chứng nhận theo loại xe... nếu chưa được nêu).
- Nếu thiếu thông tin, phải ghi nhận vào mục `Vấn đề cần xác minh` hoặc `Câu hỏi cần làm rõ`, không dùng thông tin thiếu đó như một sự thật đã xác nhận.
- Không gộp nhiều giai đoạn SDLC vào cùng một prompt.
- Không để AI đưa ra kết luận đạt/không đạt đăng kiểm ở bất kỳ giai đoạn tài liệu nào.

---

## 4. Pipeline mong muốn

Thiết kế lại bộ prompt theo pipeline sau:

```text
project.md
informember.md
      |
      v
01_project-plan.md
      |
      v
02_requirements-qa.md
      |
      v
03_requirements-specification.md
      |
      v
04_object-oriented-design.md
      |
      v
05_functional-testing.md
      |
      v
06_database.md
      |
      v
07_user-guide.md
```

Mỗi prompt chỉ được thực hiện nhiệm vụ của đúng một giai đoạn.

Prompt sau bắt buộc phải đọc kết quả của prompt liền trước và các tài liệu nền liên quan (`project.md`, `informember.md`) đã được quy định trong phần đầu vào bắt buộc. Prompt chỉ được mở rộng, chuyển hóa hoặc chi tiết hóa thông tin đã có cơ sở (ví dụ: quản lý chủ xe, phương tiện, lịch hẹn, hồ sơ kiểm định, kết quả hạng mục, chứng nhận, chatbot quy trình, tóm tắt hồ sơ, nhắc lịch), không được tạo lại toàn bộ nội dung đã xuất hiện ở tài liệu trước.

---

## 5. Quan hệ truy vết bắt buộc

Toàn bộ pipeline phải bảo đảm truy vết hai chiều giữa các tầng thông tin:

```text
Project
  -> Requirement
  -> Use Case
  -> Design
  -> Database
  -> Test Case
  -> User Guide
```

Yêu cầu truy vết tối thiểu:

- Mỗi requirement (ví dụ: quản lý chủ xe/phương tiện, đặt lịch, quản lý hồ sơ, nhập kết quả hạng mục, quản lý chứng nhận, chatbot quy trình, tóm tắt hồ sơ, nhắc lịch) phải có mã định danh rõ ràng.
- Mỗi use case (ví dụ: Đặt lịch đăng kiểm, Nhập kết quả kiểm tra, Tra cứu lịch sử, Hỏi đáp quy trình qua AI) phải liên kết với requirement tương ứng.
- Mỗi thành phần thiết kế phải chỉ ra requirement hoặc use case liên quan.
- Mỗi bảng, entity hoặc trường dữ liệu (chủ xe, phương tiện, lịch hẹn, hồ sơ, kết quả hạng mục, chứng nhận) phải có nguồn gốc từ requirement, use case hoặc thiết kế.
- Mỗi test case phải chỉ ra requirement, use case hoặc rule được kiểm thử (bao gồm rule "AI không kết luận đạt/không đạt").
- Mỗi phần trong user guide phải liên kết với chức năng hoặc use case tương ứng.

Quy tắc mã định danh bắt buộc:

```text
REQ-F-001   Functional requirement
REQ-NF-001  Non-functional requirement
UC-001      Use case
ACT-001     Actor
BR-001      Business rule
MOD-001     Module hoặc component
CLS-001     Class
IF-001      Interface
DB-ENT-001  Entity
DB-TBL-001  Table
DB-FLD-001  Field
TC-001      Test case
UG-001      User guide section
```

Không đổi mã định danh đã được tạo ở giai đoạn trước. Nếu cần điều chỉnh, phải ghi rõ lý do và cập nhật ma trận truy vết tương ứng.

---

## 6. Công việc cần thực hiện

### Bước 1: Phân tích tài liệu hiện có

Đọc và phân tích toàn bộ các file sau:

```text
project.md
informember.md
01_GenAI_DangKiemAI_project-plan.docx
02_GenAI_DangKiemAI_requirements-qa.docx
03_GenAI_DangKiemAI_requirements-specification.docx
04_GenAI_DangKiemAI_object-oriented-design.docx
05_GenAI_DangKiemAI_functional-testing.docx
06_GenAI_DangKiemAI_screenflow_db.docx
07_GenAI_DangKiemAI_user-guide.docx
```

Mục đích phân tích:

- Hiểu quy trình phát triển phần mềm đang được áp dụng cho hệ thống đăng kiểm.
- Nhận diện cấu trúc của từng loại tài liệu.
- Đánh giá mức độ chi tiết cần có ở từng giai đoạn (dự án ở mức độ khó **Trung bình**).
- Xác định cách trình bày, bảng biểu, sơ đồ và định dạng đang dùng.
- Xác định mối liên hệ giữa các tài liệu.
- Xác định những điểm cần chuẩn hóa để pipeline có thể tái sử dụng.

### Bước 2: Phân tích prompt hiện tại

Đọc toàn bộ các prompt Markdown hiện có:

```text
01. project-plan.md
02 requirements-qa.md
03 requirements-specification.md
04. object-oriented-design.md
05. functional-testing.md
06. đatabase.md
```

Với từng prompt, hãy đánh giá:

- Prompt có thiếu vai trò, bối cảnh hoặc đầu vào không.
- Prompt có yêu cầu nào mơ hồ hoặc dễ gây hiểu sai không.
- Prompt có tạo nội dung dư thừa hoặc trùng với giai đoạn khác không.
- Prompt có kế thừa đúng kết quả từ bước trước không.
- Prompt có đủ ràng buộc để tạo tài liệu chất lượng cao không.
- Prompt có bảo đảm truy vết với các tài liệu trước và sau không.
- Prompt có cần chuẩn hóa tên file, heading, bảng, checklist hoặc sơ đồ không.
- Prompt có nhắc lại đúng giới hạn "AI không quyết định kết quả đăng kiểm" ở những giai đoạn liên quan không.

### Bước 3: Thiết kế lại bộ prompt

Viết lại các prompt sau:

```text
01_project-plan.md
02_requirements-qa.md
03_requirements-specification.md
04_object-oriented-design.md
05_functional-testing.md
06_database.md
07_user-guide.md
```

Mỗi prompt mới phải:

- Có thể chạy độc lập nếu người dùng cung cấp đủ file đầu vào bắt buộc.
- Có thể chạy tuần tự trong pipeline để kế thừa kết quả từ các bước trước.
- Chỉ sinh tài liệu đúng phạm vi của giai đoạn hiện tại.
- Chỉ sử dụng thông tin có cơ sở từ `project.md`, `informember.md` và các tài liệu trước đó trong pipeline.
- Nêu rõ các file cần đọc trước khi sinh kết quả.
- Nêu rõ file đầu ra cần tạo.
- Có phần tự kiểm tra trước khi kết thúc.

---

## 7. Template bắt buộc cho mỗi prompt

Tất cả prompt phải dùng cùng một cấu trúc dưới đây.

### 7.1. Vai trò

Xác định rõ AI cần đóng vai trò gì trong giai đoạn đó.

Ví dụ:

- Project Manager
- Business Analyst
- Software Architect
- Database Designer
- QA Engineer
- Technical Writer

### 7.2. Mục tiêu

Nêu rõ tài liệu cần sinh, mục đích sử dụng và giới hạn phạm vi trong bối cảnh hệ thống quản lý đăng kiểm phương tiện có tích hợp AI.

### 7.3. Đầu vào bắt buộc

Liệt kê các file phải đọc trước khi thực hiện.

Ví dụ:

```text
project.md
informember.md
01_GenAI_DangKiemAI_project-plan.docx
```

### 7.4. Kiến thức kế thừa

Nêu rõ tài liệu nào cần được kế thừa và kế thừa phần nào.

Prompt phải yêu cầu AI:

- Không tự suy diễn ngoài tài liệu đầu vào (ví dụ: không tự đặt ra quy định pháp lý đăng kiểm chưa được nêu trong `project.md`).
- Không tạo lại nội dung đã có.
- Chỉ chi tiết hóa hoặc chuyển hóa thông tin khi có cơ sở.
- Nếu bắt buộc phải nêu giả định để tiếp tục cấu trúc tài liệu, phải đặt trong mục `Giả định cần xác nhận`, không được xem giả định là yêu cầu đã được phê duyệt.

### 7.5. Công việc phải thực hiện

Liệt kê chi tiết các nhiệm vụ của giai đoạn hiện tại theo đúng SDLC.

### 7.6. Không được thực hiện

Nêu rõ các việc nằm ngoài phạm vi.

Ví dụ:

- Không thiết kế database nếu prompt không thuộc giai đoạn database.
- Không viết test case nếu prompt không thuộc giai đoạn kiểm thử.
- Không mô tả class diagram nếu prompt không thuộc giai đoạn thiết kế.
- Không sinh API nếu tài liệu đầu vào chưa có cơ sở.
- Không để AI (trong tài liệu hoặc trong hệ thống được mô tả) tự kết luận đạt/không đạt đăng kiểm thay kiểm định viên.

### 7.7. Tiêu chuẩn chất lượng

Mỗi prompt phải yêu cầu tài liệu đầu ra đạt các tiêu chuẩn:

- Không trùng lặp.
- Không mâu thuẫn.
- Không bỏ sót thông tin quan trọng.
- Có mã định danh rõ ràng.
- Có khả năng truy vết.
- Đúng chuẩn SDLC.
- Dùng thuật ngữ nhất quán (chủ xe, phương tiện, lịch hẹn, hồ sơ kiểm định, hạng mục, chứng nhận...).
- Bảng biểu và sơ đồ có cấu trúc rõ ràng.

Nếu giai đoạn có sử dụng chuẩn chuyên môn, hãy nêu rõ chuẩn phù hợp, ví dụ:

- IEEE cho tài liệu yêu cầu.
- UML cho thiết kế hướng đối tượng.
- Chuẩn kiểm thử phần mềm cho test case.
- Chuẩn thiết kế dữ liệu quan hệ cho database.

### 7.8. Tự kiểm tra trước khi kết thúc

Mỗi prompt phải có checklist tự kiểm tra.

Tùy giai đoạn, checklist cần kiểm tra các vấn đề như:

- Có thiếu requirement không (bao gồm cả requirement AI: chatbot, tóm tắt hồ sơ, nhắc lịch).
- Có requirement nào chưa được truy vết không.
- Có thiếu use case không.
- Có actor nào chưa được mô tả không (chủ xe, nhân viên tiếp nhận, kiểm định viên, quản trị viên).
- Có entity hoặc bảng nào chưa có nguồn gốc không.
- Có test case nào chưa liên kết với requirement không.
- Có chức năng nào chưa có hướng dẫn sử dụng không.
- Có thuật ngữ, mã định danh hoặc tên chức năng nào chưa nhất quán không.
- Có chỗ nào để AI ngầm kết luận đạt/không đạt đăng kiểm không.

Nếu phát hiện thiếu sót, AI phải tự hiệu chỉnh trước khi trả kết quả.

### 7.9. Định dạng đầu ra

Nêu rõ:

- Tên file đầu ra.
- Định dạng Markdown.
- Cấu trúc heading.
- Bảng bắt buộc.
- Checklist bắt buộc.
- Sơ đồ Mermaid nếu phù hợp.
- Quy tắc đặt mã định danh.
- Ma trận truy vết phù hợp với giai đoạn hiện tại.

---

## 8. Nguyên tắc Prompt Engineering bắt buộc

Các prompt mới phải áp dụng các nguyên tắc sau:

- Role Prompting.
- Context Prompting.
- Constraint Prompting.
- Structured Output.
- Step-by-step Planning.
- Self-Consistency.
- Self-Verification.
- Traceability.
- Output Validation.

Mỗi prompt phải yêu cầu AI:

- Phân tích đầu vào trước khi sinh tài liệu.
- Lập dàn ý nội bộ trước khi viết kết quả cuối cùng, nhưng không xuất dàn ý nội bộ trừ khi người dùng yêu cầu.
- Chỉ sử dụng thông tin có cơ sở từ tài liệu đầu vào.
- Đánh dấu rõ các điểm thiếu thông tin, câu hỏi cần làm rõ và giả định cần xác nhận nếu bắt buộc phải nêu giả định.
- Giữ nhất quán thuật ngữ, actor, chức năng, requirement, use case, entity, API và database.
- Tự kiểm tra và hiệu chỉnh kết quả trước khi kết thúc.
- Luôn tuân thủ ràng buộc: AI trong hệ thống đăng kiểm chỉ hỗ trợ hỏi đáp/tóm tắt/nhắc lịch, không kết luận đạt/không đạt.

---

## 9. Yêu cầu riêng cho từng prompt

### 9.1. `01_project-plan.md`

Tạo kế hoạch dự án từ `project.md` và `informember.md`.

Tập trung vào:

- Mục tiêu dự án: quản lý nghiệp vụ đăng kiểm phương tiện và tích hợp AI hỏi đáp/tóm tắt/nhắc lịch.
- Phạm vi: quản lý chủ xe, phương tiện, lịch hẹn, hồ sơ kiểm định, kết quả hạng mục, chứng nhận; chatbot quy trình; tóm tắt hồ sơ; sinh nhắc lịch.
- Stakeholder: quản trị viên, nhân viên tiếp nhận, kiểm định viên, chủ xe.
- Deliverable: các tài liệu 01–07 và ứng dụng backend/frontend theo yêu cầu kỹ thuật trong `project.md`.
- Mốc thời gian (theo các giai đoạn SDLC KT1, KT2, KT3, cuối kỳ nêu trong `project.md`).
- Rủi ro (ví dụ: AI trả lời sai phạm vi, dữ liệu hồ sơ nhạy cảm, phụ thuộc AI Engine bên ngoài).
- Giả định.
- Tiêu chí hoàn thành.

Không viết đặc tả yêu cầu chi tiết, thiết kế, database hoặc test case.

### 9.2. `02_requirements-qa.md`

Tạo bộ câu hỏi làm rõ yêu cầu dựa trên `project.md`, `informember.md` và kế hoạch dự án.

Tập trung vào:

- Câu hỏi nghiệp vụ (quy trình đăng kiểm, hạng mục kiểm tra, điều kiện cấp chứng nhận).
- Câu hỏi về actor và vai trò (quản trị, nhân viên tiếp nhận, kiểm định viên, chủ xe).
- Câu hỏi về chức năng (quản lý, đặt lịch, hồ sơ, kết quả, chứng nhận, thống kê, AI).
- Câu hỏi về dữ liệu (chủ xe, phương tiện, lịch hẹn, hồ sơ, kết quả hạng mục, chứng nhận, tài liệu quy trình cho AI).
- Câu hỏi về ràng buộc, ngoại lệ và quy tắc nghiệp vụ (đặc biệt: giới hạn AI không kết luận đạt/không đạt).
- Câu hỏi về phi chức năng (bảo mật dữ liệu hồ sơ, độ chính xác câu trả lời AI, hiệu năng).
- Câu hỏi về phạm vi chưa rõ (ví dụ: loại phương tiện áp dụng, quy định pháp lý cụ thể, AI Engine sử dụng: OpenAI/Gemini/Claude/Hugging Face/Ollama).

Không tự trả lời nếu tài liệu đầu vào chưa có cơ sở.

Đầu ra của prompt này phải có bảng quản lý câu hỏi với các cột tối thiểu:

| Mã câu hỏi | Nhóm câu hỏi | Nội dung câu hỏi | Nguồn phát sinh | Trạng thái | Câu trả lời/Phản hồi | Ảnh hưởng nếu chưa trả lời |
|---|---|---|---|---|---|---|

Nếu câu hỏi chưa có câu trả lời, đặt trạng thái là `Chưa trả lời`. Prompt `03_requirements-specification.md` chỉ được sử dụng các câu trả lời có trạng thái `Đã trả lời` hoặc thông tin đã có cơ sở trong tài liệu đầu vào.

### 9.3. `03_requirements-specification.md`

Tạo tài liệu đặc tả yêu cầu từ `project.md`, kế hoạch dự án và phần hỏi đáp yêu cầu.

Tập trung vào:

- Functional requirement (đăng nhập/phân quyền, quản lý chủ xe/phương tiện, đặt lịch, quản lý hồ sơ, nhập kết quả hạng mục, quản lý chứng nhận, tra cứu lịch sử, thống kê, chatbot, tóm tắt hồ sơ, nhắc lịch).
- Non-functional requirement (bảo mật, độ tin cậy câu trả lời AI, khả năng mở rộng AI Engine).
- Actor (quản trị viên, nhân viên tiếp nhận, kiểm định viên, chủ xe).
- Use case tương ứng từng chức năng quản lý và chức năng AI.
- Business rule (đặc biệt BR về việc AI không quyết định kết quả đăng kiểm).
- Dữ liệu nghiệp vụ ở mức khái niệm (chủ xe, phương tiện, lịch hẹn, hồ sơ, kết quả hạng mục, chứng nhận, tài liệu quy trình).
- Ma trận truy vết requirement.

Không thiết kế class, database vật lý, API chi tiết hoặc test case.

### 9.4. `04_object-oriented-design.md`

Tạo tài liệu thiết kế hướng đối tượng từ đặc tả yêu cầu.

Tập trung vào:

- Kiến trúc tổng quan (backend FastAPI/Flask/Django, frontend React/Vue/HTML, AI Engine).
- Module hoặc component (quản lý chủ xe/phương tiện, lịch hẹn, hồ sơ, kết quả, chứng nhận, module AI hỏi đáp/tóm tắt/nhắc lịch).
- Class.
- Interface (bao gồm interface gọi AI Engine với prompt hệ thống giới hạn phạm vi trả lời).
- Quan hệ giữa các class.
- Sequence diagram (ví dụ: luồng đặt lịch, luồng chatbot hỏi đáp quy trình).
- Luồng xử lý chính.
- Mapping từ requirement/use case sang thiết kế.

Không tạo test case hoặc thiết kế database vật lý nếu chưa cần thiết.

### 9.5. `05_functional-testing.md`

Tạo tài liệu kiểm thử chức năng từ đặc tả yêu cầu và thiết kế.

Tập trung vào:

- Test scenario (bao gồm lịch hẹn, hồ sơ, kết quả, chứng nhận và các chức năng AI).
- Test case, kể cả test case kiểm tra AI **không** đưa ra kết luận đạt/không đạt và test câu hỏi vượt phạm vi tài liệu quy trình (theo hướng dẫn KT3 trong `project.md`).
- Test data.
- Expected result.
- Điều kiện tiền đề.
- Ma trận truy vết test case với requirement/use case.

Không thay đổi yêu cầu, thiết kế hoặc database.

Vì prompt database được thực hiện sau prompt kiểm thử trong pipeline này, test data ở giai đoạn này chỉ được mô tả ở mức nghiệp vụ hoặc logic. Không ràng buộc test data vào tên bảng, tên cột hoặc kiểu dữ liệu vật lý nếu tài liệu database chưa được tạo.

### 9.6. `06_database.md`

Tạo tài liệu thiết kế cơ sở dữ liệu từ yêu cầu và thiết kế.

Tập trung vào:

- Entity (chủ xe, phương tiện, lịch hẹn, hồ sơ kiểm định, kết quả hạng mục, chứng nhận, tài khoản người dùng).
- Table, Field, Data type.
- Primary key, Foreign key, Constraint, Relationship.
- ERD bằng Mermaid nếu phù hợp.
- Mapping từ requirement/use case/entity sang bảng dữ liệu.

Không viết lại test case hoặc user guide.

### 9.7. `07_user-guide.md`

Tạo tài liệu hướng dẫn sử dụng từ yêu cầu, thiết kế, kiểm thử và database.

Tập trung vào:

- Đối tượng người dùng (quản trị viên, nhân viên tiếp nhận, kiểm định viên, chủ xe).
- Chức năng người dùng có thể thao tác (đặt lịch, quản lý hồ sơ, nhập kết quả, tra cứu, thống kê, hỏi đáp AI, xem tóm tắt hồ sơ AI, nhận nhắc lịch AI).
- Quy trình sử dụng theo từng use case.
- Hướng dẫn nhập liệu.
- Thông báo, lỗi thường gặp và cách xử lý.
- Giới hạn sử dụng (đặc biệt lưu ý AI chỉ hỗ trợ thông tin, không thay thế kết luận của kiểm định viên).
- Mapping từ hướng dẫn sang chức năng/use case.

Không mô tả nội bộ kỹ thuật quá sâu, không viết lại thiết kế hoặc database.

---

## 10. Kết quả đầu ra mong muốn

Sau khi hoàn thành, phải tạo hoặc cập nhật các file prompt sau:

```text
01_project-plan.md
02_requirements-qa.md
03_requirements-specification.md
04_object-oriented-design.md
05_functional-testing.md
06_database.md
07_user-guide.md
```

Đồng thời cung cấp phần tóm tắt ngắn gồm:

- Những vấn đề chính của bộ prompt cũ.
- Nguyên tắc đã dùng để thiết kế lại.
- Cách các prompt mới liên kết với nhau trong pipeline.
- Các điểm cần lưu ý khi sử dụng lại pipeline cho dự án khác (ví dụ: thay `project.md`/`informember.md` bằng dự án mới, đổi mã dự án trong tên file docx).

---

## 11. Tiêu chí nghiệm thu

Bộ prompt mới được xem là đạt yêu cầu khi:

- Mỗi prompt có cùng template chuẩn.
- Mỗi prompt có phạm vi rõ ràng và không chồng chéo.
- Pipeline có đủ 7 giai đoạn.
- Prompt sau kế thừa đúng prompt trước.
- Có cơ chế truy vết xuyên suốt.
- Có tiêu chuẩn chất lượng và checklist tự kiểm tra.
- Có định dạng đầu ra rõ ràng.
- Ràng buộc "AI không kết luận đạt/không đạt đăng kiểm" được thể hiện nhất quán ở mọi giai đoạn liên quan.
- Có thể tái sử dụng cho dự án phần mềm khác mà không phụ thuộc vào nội dung cụ thể của dự án hiện tại.
