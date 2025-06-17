from crewai import Task
from textwrap import dedent
from utils.file_writer import write_output
from memory.shared_memory import shared_memory
from tasks.quality_gate_tasks import create_quality_gate_task

class RequirementTasksFactory:
    """
    Nhà máy chứa các phương thức để tạo ra các task chuyên môn chi tiết
    cho Giai đoạn 2: Phân tích Yêu cầu.
    """

    def create_scope_task(self, agent) -> Task:
        wbs_data = shared_memory.get("phase_2", "wbs_data_as_text") or "Dữ liệu WBS không có sẵn."
        project_plan_data = shared_memory.get("phase_2", "project_plan_data_as_xml") or "Dữ liệu Kế hoạch Dự án không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO BẢNG SCOPE REQUIREMENTS CHECKLIST

                ## Mục tiêu:
                Dựa trên WBS và Project Plan, hãy phân tích và tạo bảng Scope Requirements Checklist để xác định phạm vi yêu cầu phần mềm ban đầu.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Chuyên viên Phân tích Yêu cầu, bạn cần thực hiện các bước sau:
                1.  **Phân tích WBS**: Đọc kỹ dữ liệu WBS để xác định tất cả các sản phẩm bàn giao (deliverables) và các gói công việc (work packages) chính. Đây là nguồn chính để xác định "cái gì" cần được xây dựng.
                2.  **Phân tích Project Plan**: Xem xét kế hoạch dự án để hiểu các mốc thời gian, các giả định, và ràng buộc có thể ảnh hưởng đến phạm vi.
                3.  **Tạo Checklist**: Tổng hợp thông tin từ hai nguồn trên và xây dựng một bảng checklist chi tiết.

                ## Yêu cầu về Định dạng Đầu ra:
                Kết quả cuối cùng PHẢI là một **Bảng Markdown (Markdown Table)**. Việc này để một công cụ khác có thể dễ dàng chuyển đổi nó thành file .xlsx.
                Bảng phải có các cột sau:
                - `ID`: Mã định danh duy nhất cho mỗi hạng mục (ví dụ: SC-001).
                - `Hạng mục Phạm vi (Scope Item)`: Tên của sản phẩm bàn giao hoặc gói công việc.
                - `Mô tả (Description)`: Mô tả ngắn gọn, rõ ràng về hạng mục.
                - `Nguồn (Source)`: Nguồn gốc của hạng mục (ví dụ: "WBS 1.3.2", "Project Plan Section 4.1").
                - `Trạng thái (Status)`: Đặt giá trị mặc định là **"Cần làm rõ"**.

                ## Tài liệu tham khảo:
                - Dữ liệu WBS:\n{wbs_data[:1000]}...
                - Dữ liệu Kế hoạch Dự án:\n{project_plan_data[:1000]}...
            """),
            expected_output="""Một file văn bản chứa duy nhất một Bảng Markdown (Markdown Table).
            Bảng này liệt kê tất cả các hạng mục trong phạm vi dự án, tuân thủ chính xác 5 cột đã yêu cầu: ID, Hạng mục Phạm vi (Scope Item), Mô tả (Description), Nguồn (Source), và Trạng thái (Status).
            Ví dụ mẫu:
            | ID      | Hạng mục Phạm vi (Scope Item) | Mô tả (Description)                                 | Nguồn (Source)          | Trạng thái (Status) |
            |---------|-------------------------------|-----------------------------------------------------|--------------------------|---------------------|
            | SC-001  | Module Quản lý Sản phẩm       | Cho phép admin thêm, sửa, xóa sản phẩm.              | WBS 1.1                  | Cần làm rõ          |
            | SC-002  | Tích hợp Cổng thanh toán MoMo | Tích hợp API của MoMo để xử lý giao dịch điện tử.    | WBS 1.2.1                | Cần làm rõ          |
            | SC-003  | Báo cáo Doanh thu Tháng       | Hệ thống tự động tạo báo cáo doanh thu hàng tháng.  | Project Plan Section 3.5 | Cần làm rõ          |
            """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/Scope_Checklist.md", str(o)), 
                shared_memory.set("phase_2", "scope_checklist", str(o)))
        )

    def create_brd_task(self, agent) -> Task:
        scope_checklist = shared_memory.get("phase_2", "scope_checklist") or "Checklist Yêu cầu Phạm vi không có sẵn."
        vision_document = shared_memory.get("phase_1", "vision_document") or "Tài liệu Tầm nhìn không có sẵn."
        project_charter = shared_memory.get("phase_1", "project_charter") or "Hiến chương Dự án không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO BUSINESS REQUIREMENTS DOCUMENT (BRD)

                ## Mục tiêu:
                Từ danh sách yêu cầu phạm vi, hãy tạo Business Requirements Document (BRD) mô tả chi tiết yêu cầu nghiệp vụ từ góc độ khách hàng.

                ## Hướng dẫn chi tiết:
                Với vai trò là một Chuyên viên Phân tích Yêu cầu, bạn hãy chuyển đổi các hạng mục phạm vi thành một tài liệu nghiệp vụ hoàn chỉnh.
                Tài liệu này phải rõ ràng, logic và phục vụ làm cơ sở cho toàn bộ quá trình phát triển.

                ## Yêu cầu về Cấu trúc Tài liệu BRD:
                Bạn PHẢI tạo ra một tài liệu có cấu trúc chuyên nghiệp, bao gồm các phần chính sau:
                1.  **Tóm tắt (Executive Summary)**: Dựa vào Tầm nhìn dự án, viết một đoạn tóm tắt ngắn gọn về mục đích và giá trị của dự án.
                2.  **Mục tiêu Kinh doanh (Business Objectives)**: Tham khảo Hiến chương Dự án để liệt kê các mục tiêu kinh doanh (SMART).
                3.  **Phạm vi (Scope)**: Dựa vào 'Scope Requirements Checklist' để liệt kê các hạng mục Trong phạm vi (In-Scope) và Ngoài phạm vi (Out-of-Scope).
                4.  **Các Bên liên quan (Stakeholders)**: Liệt kê các bên liên quan chính được đề cập trong Hiến chương Dự án.
                5.  **Yêu cầu Chức năng (Functional Requirements)**: Đây là phần quan trọng nhất. Diễn giải từng hạng mục trong 'Scope Requirements Checklist' thành các yêu cầu chức năng cấp cao. Mô tả "hệ thống phải làm gì" từ góc độ người dùng.
                6.  **Yêu cầu Phi chức năng (Non-Functional Requirements)**: Phác thảo các yêu cầu ban đầu về hiệu suất, bảo mật, tính khả dụng, v.v.
                7.  **Giả định và Ràng buộc (Assumptions and Constraints)**: Ghi lại các giả định và ràng buộc đã biết.

                ## Tài liệu tham khảo đầu vào:
                - **Checklist Yêu cầu Phạm vi**:
                ```markdown
                {scope_checklist[:1500]}...
                ```
                - **Tài liệu Tầm nhìn (để lấy ngữ cảnh)**:
                ```
                {vision_document[:500]}...
                ```
                - **Hiến chương Dự án (để lấy mục tiêu và các bên liên quan)**:
                ```
                {project_charter[:500]}...
                ```
            """),
            expected_output="""Một tài liệu Business Requirements Document (BRD) hoàn chỉnh và chuyên nghiệp, được định dạng bằng Markdown.
            Tài liệu phải có đầy đủ 7 phần đã được yêu cầu, với nội dung chi tiết, logic và nhất quán.
            Phần Yêu cầu Chức năng phải được liên kết rõ ràng với các hạng mục trong Checklist Yêu cầu Phạm vi đầu vào.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/BRD.md", str(o)), 
                shared_memory.set("phase_2", "brd_document", str(o)))
        )

    def create_presentation_task(self, agent) -> Task:
        brd_document = shared_memory.get("phase_2", "brd_document") or "Tài liệu Yêu cầu Nghiệp vụ (BRD) không có sẵn."
        return Task(
             description=dedent(f"""
                # NHIỆM VỤ: TẠO DÀN Ý BÀI THUYẾT TRÌNH POWERPOINT TỪ BRD

                ## Mục tiêu:
                Chuyển nội dung BRD thành một dàn ý bài thuyết trình PowerPoint dễ hiểu để trình bày cho stakeholders, bao gồm cả những người không có nền tảng kỹ thuật.

                ## Hướng dẫn chi tiết:
                Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy tóm tắt nội dung chính của tài liệu BRD và cấu trúc nó thành một dàn ý logic cho bài thuyết trình.
                Tập trung vào việc truyền đạt "Tại sao?", "Cái gì?", và "Lợi ích là gì?" thay vì các chi tiết kỹ thuật sâu.

                ## Yêu cầu về Cấu trúc Dàn ý:
                Bạn PHẢI tạo ra một dàn ý dưới dạng văn bản Markdown. Mỗi slide được phân cách bởi dấu `---`.
                Mỗi slide phải có các phần sau:
                - **Tiêu đề Slide**: Bắt đầu bằng `#`. Ví dụ: `# Slide 1: Tên Dự án & Mục tiêu`
                - **Nội dung Slide**: Sử dụng các gạch đầu dòng `-` để liệt kê các ý chính.
                - **Ghi chú cho người thuyết trình (Speaker Notes)**: Bắt đầu bằng `**Speaker Notes:**`. Phần này chứa gợi ý về những gì cần nói hoặc nhấn mạnh khi trình bày slide đó.

                ## Đề xuất cấu trúc các slide:
                - **Slide 1: Trang bìa** (Tên dự án, Ngày trình bày, Người trình bày).
                - **Slide 2: Chương trình nghị sự (Agenda)**.
                - **Slide 3: Bối cảnh & Vấn đề** (Tóm tắt vấn đề kinh doanh mà dự án giải quyết).
                - **Slide 4: Tầm nhìn & Mục tiêu Dự án** (Dự án này sẽ đạt được điều gì?).
                - **Slide 5: Phạm vi Dự án** (Các hạng mục chính Trong và Ngoài phạm vi).
                - **Slide 6-7: Các Yêu cầu Chức năng Chính** (Chỉ nêu bật 3-5 yêu cầu quan trọng nhất, đừng liệt kê tất cả).
                - **Slide 8: Lợi ích Kinh doanh** (Dự án sẽ mang lại giá trị gì?).
                - **Slide 9: Các bước tiếp theo (Next Steps)**.
                - **Slide 10: Hỏi & Đáp (Q&A)**.

                ## Tài liệu tham khảo đầu vào (BRD):
                ```markdown
                {brd_document[:2000]}...
                ```
            """),
            expected_output="""Một file văn bản duy nhất chứa dàn ý chi tiết cho bài thuyết trình, được định dạng bằng Markdown.
            Mỗi slide được phân cách bởi '---'. Mỗi slide phải có Tiêu đề (dùng '#'), Nội dung (dùng '-'), và Ghi chú cho người thuyết trình (dùng '**Speaker Notes:**').
            Ví dụ mẫu:
            # Slide 1: Dự án E-commerce "SuperCart"
            - Giới thiệu tổng quan dự án và đội ngũ.
            **Speaker Notes:** Chào mừng các bên liên quan. Nhấn mạnh tầm quan trọng của dự án đối với chiến lược công ty.
            ---
            # Slide 2: Chương trình nghị sự
            - Bối cảnh & Vấn đề
            - Mục tiêu & Phạm vi
            - Yêu cầu chính
            - Các bước tiếp theo
            **Speaker Notes:** Giới thiệu nhanh các phần sẽ trình bày để mọi người nắm được luồng thông tin.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/BRD_Presentation_Outline.md", str(o)), 
                shared_memory.set("phase_2", "brd_presentation_outline", str(o)))
        )

    def create_srs_task(self, agent) -> Task:
        brd_document = shared_memory.get("phase_2", "brd_document") or "Tài liệu Yêu cầu Nghiệp vụ (BRD) không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO TÀI LIỆU ĐẶC TẢ YÊU CẦU HỆ THỐNG (SRS)

                ## Mục tiêu:
                Phân tích tài liệu BRD để tạo ra một tài liệu SRS (System Requirements Specification) mô tả các yêu cầu hệ thống một cách chi tiết, rõ ràng và không mơ hồ cho đội ngũ phát triển.

                ## Hướng dẫn chi tiết:
                Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy dịch các yêu cầu nghiệp vụ cấp cao trong BRD thành các yêu cầu hệ thống cụ thể.
                Tài liệu SRS là bản thiết kế chi tiết về "cái gì" hệ thống sẽ làm, không phải "làm như thế nào".
                Hãy tuân thủ cấu trúc dựa trên tiêu chuẩn IEEE 830. Nếu không chắc chắn, hãy ủy quyền cho Knowledge Assistant (researcher_agent) để tìm kiếm mẫu.

                ## Yêu cầu về Cấu trúc Tài liệu SRS:
                Tài liệu PHẢI bao gồm các phần chính sau:
                1.  **Giới thiệu (Introduction)**
                    1.1. Mục đích (Purpose): Mô tả mục đích của tài liệu SRS này.
                    1.2. Phạm vi sản phẩm (Product Scope): Mô tả ngắn gọn về sản phẩm phần mềm và mục tiêu của nó.
                    1.3. Định nghĩa, Từ viết tắt (Definitions, Acronyms): Liệt kê các thuật ngữ chuyên ngành.
                2.  **Mô tả Tổng quan (Overall Description)**
                    2.1. Bối cảnh sản phẩm (Product Perspective): Mối quan hệ của sản phẩm với các hệ thống khác.
                    2.2. Chức năng sản phẩm (Product Functions): Tóm tắt các chức năng chính mà hệ thống sẽ thực hiện.
                    2.3. Đặc điểm người dùng (User Characteristics): Mô tả các loại người dùng sẽ tương tác với hệ thống.
                3.  **Yêu cầu Cụ thể (Specific Requirements)**: Đây là phần cốt lõi.
                    3.1. **Yêu cầu Chức năng (Functional Requirements)**: Phân rã từng yêu cầu chức năng trong BRD thành các yêu cầu hệ thống chi tiết hơn. Mỗi yêu cầu phải có một mã định danh duy nhất (ví dụ: FR-001), có thể kiểm chứng, và không mơ hồ.
                        - Ví dụ: FR-001: "Hệ thống phải cho phép người dùng đăng ký bằng email và mật khẩu."
                        - Ví dụ: FR-002: "Hệ thống phải mã hóa mật khẩu người dùng bằng thuật toán bcrypt."
                    3.2. **Yêu cầu Phi chức năng (Non-Functional Requirements)**: Chi tiết hóa các yêu cầu về hiệu suất, bảo mật, tính khả dụng, khả năng bảo trì...
                        - Ví dụ: NFR-PERF-01: "Thời gian phản hồi của trang chủ phải dưới 2 giây với 1000 người dùng đồng thời."
                    3.3. **Yêu cầu về Giao diện Ngoài (External Interface Requirements)**: Mô tả cách hệ thống tương tác với các hệ thống bên ngoài khác (ví dụ: API của bên thứ ba, phần cứng).

                ## Tài liệu tham khảo đầu vào (BRD):
                ```markdown
                {brd_document[:3000]}...
                ```
            """),
            expected_output="""Một tài liệu System Requirements Specification (SRS) hoàn chỉnh, được định dạng chuyên nghiệp bằng Markdown.
            Tài liệu phải tuân thủ nghiêm ngặt cấu trúc 3 phần chính đã nêu. Phần 'Yêu cầu Cụ thể' phải chứa danh sách các yêu cầu chức năng và phi chức năng được đánh mã định danh duy nhất, rõ ràng và có thể kiểm chứng.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/SRS.md", str(o)), 
                shared_memory.set("phase_2", "srs_document", str(o)))
        )

#sửa lại yêu cầu 
    def create_usecase_tasks(self, agent) -> list[Task]:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."
        conops_document = shared_memory.get("phase_1", "conops_document") or "Tài liệu CONOPS không có sẵn."
        task1 = Task(
            description=dedent(f"""
                # NHIỆM VỤ (BƯỚC 1/2): TRÍCH XUẤT ACTORS VÀ USE CASES

                ## Mục tiêu:
                Phân tích kỹ lưỡng tài liệu SRS và CONOPS để xác định và liệt kê TẤT CẢ các tác nhân (Actors) và các kịch bản sử dụng (Use Cases) tương ứng của họ.

                ## Hướng dẫn chi tiết:
                - **Actor**: Là một người, một vai trò, hoặc một hệ thống khác tương tác với hệ thống của chúng ta.
                - **Use Case**: Là một hành động hoặc một mục tiêu mà Actor muốn đạt được khi sử dụng hệ thống.

                ## Yêu cầu về Định dạng Đầu ra:
                Bạn PHẢI trả về một danh sách có cấu trúc rõ ràng dưới dạng **Bảng Markdown**.
                Bảng này sẽ là đầu vào cho bước tiếp theo.
                Các cột cần có: `Actor` và `Use Case Description`.

                ## Tài liệu tham khảo đầu vào:
                - **Tài liệu SRS (Trích đoạn)**:
                  ```markdown
                  {srs_document[:1500]}...
                  ```
                - **Tài liệu CONOPS (Trích đoạn)**:
                  ```markdown
                  {conops_document[:1000]}...
                  ```.
            """),
            expected_output="""Một Bảng Markdown đơn giản liệt kê tất cả các cặp Actor và Use Case đã xác định.
                    Ví dụ:
                    | Actor             | Use Case Description          |
                    |-------------------|-------------------------------|
                    | Registered User   | Login to the system           |
                    | Registered User   | Manage personal profile       |
                    | Administrator     | Manage user accounts          |
                    | Administrator     | View system-wide reports      |
                    | Payment Gateway   | Process transaction           |
            """,
            agent=agent
        )
        task2 = Task(
            description=dedent(f"""# NHIỆM VỤ (BƯỚC 2/2): TẠO SƠ ĐỒ VÀ VIẾT USER STORIES

                ## Mục tiêu:
                Dựa trên danh sách Actors và Use Cases đã được cung cấp từ bước trước, hãy tạo ra một sơ đồ Use Case minh họa và viết các User Stories chi tiết.

                ## Hướng dẫn chi tiết:
                Bạn đã nhận được một danh sách rõ ràng. Bây giờ hãy thực hiện:
                1.  **Vẽ Sơ đồ**: Dùng danh sách đó để tạo mã code cho một sơ đồ Use Case tổng thể bằng cú pháp **Mermaid.js**.
                2.  **Viết User Stories**: Chọn ra các Use Case quan trọng nhất từ danh sách và viết User Stories chi tiết cho chúng.

                ## Yêu cầu về Định dạng Đầu ra:
                Đầu ra của bạn PHẢI là một tài liệu Markdown duy nhất, có 2 phần RÕ RÀNG:
                
                **Phần 1: Sơ đồ Use Case (Mã Mermaid.js):**
                Bắt đầu bằng tiêu đề `### Sơ đồ Use Case (Mermaid.js)`.
                
                **Phần 2: User Stories:**
                Bắt đầu bằng tiêu đề `### User Stories`. Mỗi story phải có:
                - **Story:** "As a [Actor], I want to [Use Case] so that [benefit]."
                - **Acceptance Criteria (AC):** Liệt kê các điều kiện để story được coi là hoàn thành.

                ## Ngữ cảnh đầu vào (Danh sách Actors và Use Cases):
                Dữ liệu này được cung cấp từ kết quả của task trước. Hãy sử dụng nó làm nguồn thông tin chính.
            """),
            expected_output="""Một file văn bản duy nhất được định dạng bằng Markdown, chứa hai phần rõ ràng:
                1.  Một khối code Mermaid.js để vẽ sơ đồ Use Case.
                2.  Một danh sách các User Stories chi tiết, mỗi story đều có Acceptance Criteria rõ ràng.
            """,
            agent=agent, context=[task1],
            callback=lambda o: (
                write_output("2_requirements/Use_Cases_and_User_Stories.md", str(o)), 
                shared_memory.set("phase_2", "use_cases_and_user_stories", str(o)))
        )
        return [task1, task2]
    
    def create_rtm_tasks(self, agent) -> Task:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."

        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO MA TRẬN TRUY VẾT YÊU CẦU (RTM)

                ## Mục tiêu:
                Tạo RTM từ tài liệu SRS để theo dõi các yêu cầu từ giai đoạn phân tích sang các giai đoạn thiết kế, phát triển, và kiểm thử trong tương lai.

                ## Hướng dẫn chi tiết:
                Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy đọc kỹ tài liệu SRS đã cung cấp.
                Nhiệm vụ của bạn là trích xuất từng yêu cầu cụ thể (cả chức năng và phi chức năng) và liệt kê chúng vào một ma trận.
                Ma trận này sẽ đóng vai trò là công cụ theo dõi, đảm bảo mọi yêu cầu đều được thiết kế, xây dựng và kiểm thử.

                ## Yêu cầu về Định dạng Đầu ra:
                Kết quả cuối cùng PHẢI là một chuỗi văn bản theo định dạng **CSV (Comma-Separated Values)**.
                - Dòng đầu tiên phải là header.
                - Các cột cần có:
                1. `Requirement_ID`: Mã định danh duy nhất của yêu cầu (ví dụ: FR-001, NFR-PERF-01).
                2. `Requirement_Description`: Mô tả ngắn gọn của yêu cầu.
                3. `Design_Artifact_ID`: ID của tài liệu thiết kế liên quan. Để trống hoặc điền "TBD" (To Be Determined).
                4. `Code_Module`: Module code thực thi yêu cầu. Để trống hoặc điền "TBD".
                5. `Test_Case_ID`: ID của các ca kiểm thử liên quan. Để trống hoặc điền "TBD".
                6. `Status`: Trạng thái ban đầu của yêu cầu. Đặt là "Chưa thực hiện".

                ## Tài liệu tham khảo đầu vào (SRS):
                ```markdown
                {srs_document[:3000]}...
                ```
            """),
            expected_output="""Một file văn bản duy nhất tuân thủ định dạng CSV.
            Dòng đầu tiên là header với 6 cột đã chỉ định. Mỗi dòng tiếp theo tương ứng với một yêu cầu từ SRS.
            Ví dụ mẫu:
            "Requirement_ID","Requirement_Description","Design_Artifact_ID","Code_Module","Test_Case_ID","Status"
            "FR-001","Hệ thống phải cho phép người dùng đăng ký bằng email và mật khẩu.","TBD","Auth_Module","TC-FR-001","Chưa thực hiện"
            "FR-002","Hệ thống phải mã hóa mật khẩu người dùng bằng thuật toán bcrypt.","TBD","Auth_Module","TC-FR-002","Chưa thực hiện"
            "NFR-PERF-01","Thời gian phản hồi của trang chủ phải dưới 2 giây.","TBD","WebApp","TC-NFR-01","Chưa thực hiện"
            """,
            agent=agent,
            callback=lambda output: (
                write_output("2_requirements/Requirements_Traceability_Matrix.csv", str(output)),
                shared_memory.set("phase_2", "rtm_document", str(output))
            )
        )

    def create_impact_analysis_task(self, agent, change_request) -> Task:
            rtm_document = shared_memory.get("phase_2", "rtm_document") or "Ma trận RTM không có sẵn."
            return Task(
                description=dedent(f"""
                    # NHIỆM VỤ: LẬP BÁO CÁO ĐÁNH GIÁ TÁC ĐỘNG THAY ĐỔI YÊU CẦU

                    ## Mục tiêu:
                    Dựa trên Ma trận Truy vết Yêu cầu (RTM), hãy phân tích và lập một báo cáo chi tiết đánh giá tác động của một yêu cầu thay đổi phần mềm cụ thể.

                    ## Yêu cầu Thay đổi cần Phân tích:
                    "{change_request}"

                    ## Hướng dẫn chi tiết:
                    Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy thực hiện các bước sau:
                    1.  **Hiểu rõ Yêu cầu Thay đổi**: Đọc kỹ mô tả yêu cầu thay đổi ở trên.
                    2.  **Xác định Yêu cầu Bị ảnh hưởng**: Rà soát RTM để tìm tất cả các yêu cầu hiện có (Requirement_ID) bị ảnh hưởng trực tiếp hoặc gián tiếp bởi thay đổi này.
                    3.  **Truy vết Tác động**: Đối với mỗi yêu cầu bị ảnh hưởng, hãy xem xét các cột tiếp theo trong RTM (`Design_Artifact_ID`, `Code_Module`, `Test_Case_ID`) để suy luận về các tác động tiềm tàng.
                    4.  **Tổng hợp Báo cáo**: Viết một báo cáo có cấu trúc rõ ràng, tổng hợp tất cả các phân tích của bạn.

                    ## Yêu cầu về Cấu trúc Báo cáo:
                    Báo cáo PHẢI bao gồm các phần sau:
                    - **1. Tóm tắt Yêu cầu Thay đổi**: Mô tả lại yêu cầu thay đổi bằng lời của bạn.
                    - **2. Danh sách Yêu cầu Bị ảnh hưởng**: Liệt kê các `Requirement_ID` từ RTM bị tác động.
                    - **3. Phân tích Tác động Chi tiết**:
                        - **Tác động đến Thiết kế (Design)**: Những tài liệu thiết kế nào cần được cập nhật?
                        - **Tác động đến Phát triển (Development)**: Những module code nào cần được sửa đổi hoặc tạo mới? Ước tính mức độ phức tạp (Thấp/Trung bình/Cao).
                        - **Tác động đến Kiểm thử (Testing)**: Những test case nào cần được cập nhật hoặc tạo mới?
                        - **Tác động đến các Yêu cầu khác**: Thay đổi này có gây mâu thuẫn với các yêu cầu khác không?
                    - **4. Đánh giá Rủi ro**: Liệt kê các rủi ro tiềm tàng (ví dụ: rủi ro kỹ thuật, rủi ro về thời gian).
                    - **5. Đề xuất**: Đưa ra đề xuất nên "Chấp thuận", "Chấp thuận có điều kiện", hay "Từ chối" yêu cầu thay đổi này, cùng với lý do.

                    ## Tài liệu tham khảo đầu vào (RTM dạng CSV):
                    ```csv
                    {rtm_document[:2000]}...
                    ```
                """),
                expected_output="""Một báo cáo Đánh giá Tác động Thay đổi hoàn chỉnh, được định dạng chuyên nghiệp bằng Markdown.
                Báo cáo phải có đầy đủ 5 phần đã yêu cầu, với các phân tích logic và có căn cứ dựa trên RTM được cung cấp.
                """,
                agent=agent,
                callback=lambda o: (
                    write_output("2_requirements/Change_Impact_Analysis_Report.md", str(o)),
                    shared_memory.set("phase_2", "change_impact_report", str(o)))
            )

    def create_sla_task(self, agent) -> Task:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."
        return Task(
            description=dedent(f"""
            # NHIỆM VỤ: TẠO MẪU THỎA THUẬN MỨC ĐỘ DỊCH VỤ (SLA)

            ## Mục tiêu:
            Tạo một bản mẫu Thỏa thuận Mức độ Dịch vụ (Service Level Agreement - SLA) chi tiết dựa trên các yêu cầu hệ thống, đặc biệt là các yêu cầu phi chức năng đã được nêu trong tài liệu SRS.

            ## Hướng dẫn chi tiết:
            Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy đọc kỹ tài liệu SRS và trích xuất các thông tin liên quan đến chất lượng dịch vụ để xây dựng một bản mẫu SLA.
            Tài liệu này phải định lượng các cam kết và xác định rõ các biện pháp xử lý khi không đạt được cam kết.

            ## Yêu cầu về Cấu trúc Tài liệu SLA:
            Bản mẫu SLA PHẢI bao gồm các phần chính sau:
            1.  **Giới thiệu và Định nghĩa**:
                - Mục đích của tài liệu SLA.
                - Định nghĩa các thuật ngữ chính (ví dụ: Uptime, Downtime, Thời gian phản hồi).
            2.  **Phạm vi Dịch vụ**: Mô tả ngắn gọn về các dịch vụ được cung cấp mà SLA này áp dụng.
            3.  **Các Cam kết về Mức độ Dịch vụ (Service Level Objectives - SLOs)**: Đây là phần quan trọng nhất.
                - **Tính khả dụng (Availability/Uptime)**: Đề xuất một con số cụ thể (ví dụ: 99.5%, 99.9%). Tính toán thời gian downtime cho phép mỗi tháng/năm.
                - **Hiệu suất (Performance)**: Dựa vào các NFR trong SRS, đề xuất các chỉ số như "Thời gian phản hồi trung bình của API chính < 500ms".
                - **Thời gian Phản hồi Hỗ trợ (Support Response Time)**: Đề xuất thời gian phản hồi cho các loại sự cố khác nhau (ví dụ: Sự cố nghiêm trọng - phản hồi trong 1 giờ; Yêu cầu thông thường - phản hồi trong 24 giờ).
                - **Thời gian Giải quyết Sự cố (Issue Resolution Time)**: Đề xuất thời gian mục tiêu để giải quyết các loại sự cố.
            4.  **Trách nhiệm của các bên**:
                - Trách nhiệm của nhà cung cấp dịch vụ.
                - Trách nhiệm của khách hàng/người dùng.
            5.  **Đo lường và Báo cáo**: Mô tả cách các chỉ số SLO sẽ được đo lường và tần suất báo cáo (ví dụ: báo cáo hàng tháng).
            6.  **Chế tài khi vi phạm SLA**: Đề xuất các biện pháp xử lý nếu không đáp ứng được SLOs (ví dụ: giảm giá dịch vụ, tín dụng dịch vụ).

            ## Tài liệu tham khảo đầu vào (SRS):
            ```markdown
            {srs_document[:3000]}...
            ```
            """),
            expected_output="""Một bản mẫu Thỏa thuận Mức độ Dịch vụ (SLA) hoàn chỉnh, được định dạng chuyên nghiệp bằng Markdown.
            Tài liệu phải có đầy đủ 6 phần đã yêu cầu. Phần Cam kết (SLOs) phải chứa các con số và chỉ số cụ thể, có thể đo lường được, được suy luận từ các yêu cầu phi chức năng trong SRS.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/SLA_Template.md", str(o)),
                shared_memory.set("phase_2", "sla_template", str(o))
            )
        )

    def create_nfr_task(self, agent) -> Task:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TRÍCH XUẤT VÀ TỔNG HỢP YÊU CẦU PHI CHỨC NĂNG (NFRs)

                ## Mục tiêu:
                Phân tích kỹ lưỡng tài liệu SRS để tạo ra một danh sách đầy đủ và có cấu trúc về các Yêu cầu Phi Chức năng (NFRs) như bảo mật, hiệu năng, và tính khả dụng.

                ## Hướng dẫn chi tiết:
                Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy đọc toàn bộ tài liệu SRS và xác định tất cả các câu lệnh mô tả về "chất lượng" hoặc "cách thức hoạt động" của hệ thống, thay vì "chức năng" của nó.
                Tài liệu này sẽ là nguồn tham khảo chính cho kiến trúc sư, đội ngũ an ninh và đội kiểm thử hiệu năng.

                ## Yêu cầu về Cấu trúc Tài liệu:
                Bạn PHẢI tạo ra một tài liệu Markdown, trong đó các NFRs được phân loại rõ ràng theo các danh mục sau:
                - **Hiệu suất (Performance)**: Thời gian phản hồi, thông lượng, khả năng xử lý tải.
                - **Bảo mật (Security)**: Mã hóa, xác thực, ủy quyền, phòng chống tấn công.
                - **Tính khả dụng (Availability)**: Uptime, thời gian phục hồi sau lỗi (failover), khả năng chịu lỗi.
                - **Khả năng sử dụng (Usability)**: Dễ học, dễ sử dụng, giao diện thân thiện.
                - **Khả năng mở rộng (Scalability)**: Khả năng xử lý khi lượng người dùng hoặc dữ liệu tăng lên.
                - **Khả năng bảo trì (Maintainability)**: Dễ dàng sửa lỗi, cập nhật, nâng cấp.
                
                Mỗi yêu cầu phải có một mã định danh duy nhất (ví dụ: NFR-PERF-01) và một mô tả rõ ràng, có thể đo lường được.

                ## Tài liệu tham khảo đầu vào (SRS):
                ```markdown
                {srs_document[:3000]}...
                ```
            """),
           expected_output="""Một file văn bản Markdown chứa danh sách các Yêu cầu Phi Chức năng được phân loại chi tiết.
                Ví dụ mẫu:
                # Danh sách Yêu cầu Phi Chức năng (NFRs)

                ### 1. Hiệu suất (Performance)
                - **NFR-PERF-01**: Thời gian phản hồi của API đăng nhập phải dưới 300ms với 500 người dùng đồng thời.
                - **NFR-PERF-02**: Trang chi tiết sản phẩm phải tải đầy đủ trong vòng 1.5 giây trên kết nối 4G.

                ### 2. Bảo mật (Security)
                - **NFR-SEC-01**: Tất cả mật khẩu người dùng phải được băm (hashed) bằng thuật toán Argon2.
                - **NFR-SEC-02**: Hệ thống phải có cơ chế chống tấn công CSRF trên tất cả các form.

                ### 3. Tính khả dụng (Availability)
                - **NFR-AVAIL-01**: Hệ thống phải đạt uptime 99.9% hàng tháng, ngoại trừ thời gian bảo trì đã được thông báo trước.
                """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/NFRs.md", str(o)), 
                shared_memory.set("phase_2", "nfr_document", str(o))
                )
        )

    def create_security_task(self, agent) -> Task:
        nfr_document = shared_memory.get("phase_2", "nfr_document") or "Tài liệu NFRs không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: VIẾT CHI TIẾT CÁC YÊU CẦU VỀ BẢO MẬT VÀ QUYỀN RIÊNG TƯ

                ## Mục tiêu:
                Dựa trên danh sách Yêu cầu Phi chức năng (NFRs) đã có, hãy xác định và viết chi tiết các yêu cầu cụ thể về bảo mật và quyền riêng tư của hệ thống.

                ## Hướng dẫn chi tiết:
                Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy lấy các yêu cầu bảo mật cấp cao từ NFRs và diễn giải chúng thành các quy tắc và hành vi cụ thể mà hệ thống phải tuân thủ. Tài liệu này sẽ là kim chỉ nam cho các nhà phát triển và kỹ sư bảo mật.

                ## Yêu cầu về Cấu trúc Tài liệu:
                Bạn PHẢI tạo ra một tài liệu Markdown, trong đó các yêu cầu được phân loại rõ ràng theo các danh mục sau. Với mỗi yêu cầu, hãy cung cấp một mã định danh duy nhất (ví dụ: SEC-AUTH-01).

                1.  **Xác thực & Quản lý Phiên (Authentication & Session Management)**:
                    - Chính sách mật khẩu (độ dài, độ phức tạp).
                    - Cơ chế chống đoán mật khẩu (rate limiting, CAPTCHA).
                    - Quản lý phiên đăng nhập (thời gian hết hạn, đăng xuất an toàn).
                    - Xác thực đa yếu tố (MFA/2FA) nếu có.

                2.  **Kiểm soát Truy cập (Authorization/Access Control)**:
                    - Nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
                    - Phân quyền dựa trên vai trò (Role-Based Access Control - RBAC).
                    - Cách hệ thống ngăn chặn người dùng truy cập vào dữ liệu không thuộc về họ.

                3.  **Bảo vệ Dữ liệu (Data Protection)**:
                    - Mã hóa dữ liệu khi lưu trữ (at-rest), ví dụ: mã hóa thông tin nhạy cảm của người dùng trong CSDL.
                    - Mã hóa dữ liệu khi truyền (in-transit), ví dụ: yêu cầu sử dụng HTTPS/TLS.

                4.  **Ghi nhật ký và Giám sát (Logging and Monitoring)**:
                    - Các sự kiện bảo mật cần được ghi log (đăng nhập thành công/thất bại, thay đổi quyền, ...).
                    - Nội dung của mỗi log entry.

                5.  **Tuân thủ Quyền riêng tư (Privacy Compliance)**:
                    - Các yêu cầu liên quan đến việc thu thập và xử lý dữ liệu cá nhân (ví dụ: tuân thủ Nghị định 13/2023/NĐ-CP của Việt Nam).
                    - Quyền của người dùng đối với dữ liệu của họ (quyền được xem, sửa, xóa).

                ## Tài liệu tham khảo đầu vào (NFRs):
                ```markdown
                {nfr_document[:2000]}...
                ```
            """),
            expected_output="""Một tài liệu chi tiết về các Yêu cầu Bảo mật và Quyền riêng tư, được định dạng bằng Markdown.
                Tài liệu phải được phân loại theo 5 mục đã nêu, và mỗi yêu cầu riêng lẻ phải có mã định danh duy nhất và mô tả rõ ràng.
                Ví dụ mẫu:
                # Yêu cầu Bảo mật và Quyền riêng tư

                ### 1. Xác thực & Quản lý Phiên
                - **SEC-AUTH-01**: Mật khẩu người dùng phải có độ dài tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt.
                - **SEC-AUTH-02**: Hệ thống phải khóa tài khoản trong 15 phút sau 5 lần đăng nhập thất bại liên tiếp.

                ### 2. Kiểm soát Truy cập
                - **SEC-AC-01**: Người dùng thông thường chỉ có thể xem và sửa thông tin cá nhân của chính họ, không thể xem của người dùng khác.
                """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/Security_Requirements.md", str(o)),
                shared_memory.set("phase_2", "privacy_and_security_requirements", str(o))
            )
        )

    def create_checklist_task(self, agent) -> Task:
        srs_document = shared_memory.get("phase_2", "srs_document") or "Tài liệu SRS không có sẵn."
        rtm_document = shared_memory.get("phase_2", "rtm_document") or "Ma trận RTM không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: TẠO BẢNG CHECKLIST KIỂM TRA YÊU CẦU

                ## Mục tiêu:
                Tạo một bảng checklist kiểm tra yêu cầu dựa trên tài liệu SRS và RTM nhằm đánh giá tính đầy đủ, nhất quán, và khả thi của các yêu cầu đã được đặc tả.

                ## Hướng dẫn chi tiết:
                Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy đóng vai một người đánh giá chất lượng (Quality Assurance). Nhiệm vụ của bạn không phải là viết thêm yêu cầu, mà là tạo ra một danh sách CÁC CÂU HỎI để kiểm tra các yêu cầu đã có.
                
                Hãy tạo các câu hỏi kiểm tra dựa trên các tiêu chí chất lượng sau:
                - **Tính Đầy đủ (Completeness)**: Yêu cầu có đủ thông tin để đội phát triển hiểu và thực hiện không?
                - **Tính Nhất quán (Consistency)**: Yêu cầu này có mâu thuẫn với các yêu cầu khác không?
                - **Tính Rõ ràng (Clarity/Unambiguous)**: Yêu cầu có thể được hiểu theo nhiều cách khác nhau không?
                - **Tính Khả thi (Feasibility)**: Yêu cầu có thể được thực hiện với công nghệ và nguồn lực hiện tại không?
                - **Tính Có thể Kiểm thử (Testability)**: Chúng ta có thể viết một test case để xác minh yêu cầu này đã được hoàn thành hay chưa?
                - **Tính Truy vết (Traceability)**: Yêu cầu này có được liên kết trong RTM không?

                ## Yêu cầu về Định dạng Đầu ra:
                Bạn PHẢI tạo ra một checklist dưới dạng **Bảng Markdown (Markdown Table)**.
                Bảng phải có các cột sau:
                - `Checklist_ID`: Mã định danh duy nhất cho mỗi câu hỏi (ví dụ: Q-01).
                - `Loại (Category)`: Loại tiêu chí chất lượng (ví dụ: "Tính Đầy đủ", "Tính Nhất quán").
                - `Câu hỏi Kiểm tra (Inspection Question)`: Câu hỏi cụ thể cần trả lời.
                - `Kết quả (Pass/Fail)`: Để trống cột này hoặc điền "Chưa kiểm tra".
                - `Ghi chú (Comments)`: Để trống cột này.

                ## Tài liệu tham khảo đầu vào:
                - **Tài liệu SRS (Trích đoạn)**:
                ```markdown
                {srs_document[:1500]}...
                ```
                - **Tài liệu RTM (Trích đoạn)**:
                ```csv
                {rtm_document[:1000]}...
                ```
            """),
            expected_output="""Một file văn bản chứa Bảng Markdown (Markdown Table) chi tiết.
                Bảng này là một checklist các câu hỏi để đánh giá chất lượng của các yêu cầu, tuân thủ chính xác 5 cột đã yêu cầu.
                Ví dụ mẫu:
                | Checklist_ID | Loại (Category)       | Câu hỏi Kiểm tra (Inspection Question)                                                      | Kết quả (Pass/Fail) | Ghi chú (Comments) |
                |--------------|-----------------------|---------------------------------------------------------------------------------------------|---------------------|--------------------|
                | Q-01         | Tính Rõ ràng          | Yêu cầu FR-001 ("Hệ thống phải nhanh") có định nghĩa rõ ràng về "nhanh" không (ví dụ: <2s)?      | Chưa kiểm tra       |                    |
                | Q-02         | Tính Nhất quán       | Yêu cầu FR-005 và FR-012 có mâu thuẫn với nhau về luồng xử lý đơn hàng không?               | Chưa kiểm tra       |                    |
                | Q-03         | Tính Có thể Kiểm thử  | Chúng ta có thể viết một test case cụ thể để kiểm tra yêu cầu NFR-SEC-01 không?              | Chưa kiểm tra       |                    |
                | Q-04         | Tính Truy vết        | Tất cả các yêu cầu chức năng trong SRS đã được liệt kê trong RTM chưa?                      | Chưa kiểm tra       |                    |
            """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/Requirements_Inspection_Checklist.md", str(o)),
                shared_memory.set("phase_2", "requirements_inspection_checklist", str(o))
            )
        )

    def create_training_task(self, agent) -> Task:
        conops_document = shared_memory.get("phase_1", "conops_document") or "Tài liệu CONOPS không có sẵn."
        use_case_data = shared_memory.get("phase_2", "use_cases_and_user_stories") or "Dữ liệu Use Case không có sẵn."
        return Task(
            description=dedent(f"""
                # NHIỆM VỤ: XÂY DỰNG KẾ HOẠCH ĐÀO TẠO (TRAINING PLAN)

                ## Mục tiêu:
                Tạo một bản Kế hoạch Đào tạo chi tiết để hướng dẫn người dùng cuối sử dụng hệ thống một cách hiệu quả, dựa trên các kịch bản sử dụng trong CONOPS và các chức năng đã được mô tả trong Use Case/User Stories.

                ## Hướng dẫn chi tiết:
                Với vai trò là Chuyên viên Phân tích Yêu cầu, bạn hãy thiết kế một chương trình đào tạo logic và dễ tiếp cận.
                Kế hoạch này phải xác định rõ "ai" cần được đào tạo, "cái gì" họ cần học, và "làm thế nào" để đào tạo họ.

                ## Yêu cầu về Cấu trúc Kế hoạch Đào tạo:
                Tài liệu PHẢI bao gồm các phần chính sau:
                1.  **Mục tiêu Đào tạo (Training Objectives)**: Sau khóa đào tạo, học viên sẽ có thể làm được những gì? (Ví dụ: "Học viên có thể tự đăng ký tài khoản và quản lý đơn hàng.").
                2.  **Đối tượng Đào tạo (Target Audience)**: Xác định các nhóm người dùng khác nhau cần được đào tạo (ví dụ: Khách hàng, Nhân viên bán hàng, Quản trị viên).
                3.  **Nội dung & Lịch trình Đào tạo (Training Content & Schedule)**:
                    - Chia nội dung thành các học phần (modules) logic, thường dựa trên các nhóm chức năng hoặc vai trò người dùng.
                    - Với mỗi học phần, liệt kê các chủ đề chính sẽ được đề cập.
                    - Đề xuất thời lượng cho mỗi học phần.
                4.  **Phương pháp & Tài liệu Đào tạo (Training Method & Materials)**:
                    - Đề xuất phương pháp đào tạo (ví dụ: Workshop trực tiếp, Khóa học video trực tuyến, Tự học qua tài liệu).
                    - Liệt kê các tài liệu cần chuẩn bị (ví dụ: Bài giảng PowerPoint, Video hướng dẫn, Sổ tay người dùng).
                5.  **Đánh giá & Hỗ trợ sau Đào tạo (Evaluation & Post-Training Support)**:
                    - Làm thế nào để đánh giá hiệu quả đào tạo (ví dụ: Bài kiểm tra ngắn, bài tập thực hành)?
                    - Các kênh hỗ trợ sau đào tạo (ví dụ: Diễn đàn hỏi đáp, Email hỗ trợ).

                ## Tài liệu tham khảo đầu vào:
                - **Tài liệu CONOPS (Trích đoạn)**:
                ```markdown
                {conops_document[:1000]}...
                ```
                - **Dữ liệu Use Case & User Story (Trích đoạn)**:
                ```markdown
                {use_case_data[:2000]}...
                ```
            """),
            expected_output="""Một bản Kế hoạch Đào tạo hoàn chỉnh, được định dạng chuyên nghiệp bằng Markdown.
                Tài liệu phải có đầy đủ 5 phần đã yêu cầu, với nội dung thực tế và có thể áp dụng được.
                Ví dụ mẫu:
                # Kế hoạch Đào tạo cho Hệ thống SuperCart

                ### 1. Mục tiêu Đào tạo
                - Học viên có thể tự quản lý tài khoản, tìm kiếm sản phẩm, và hoàn thành một đơn hàng.
                - Học viên hiểu rõ các chính sách của hệ thống.

                ### 2. Đối tượng Đào tạo
                - Nhóm 1: Khách hàng mới.
                - Nhóm 2: Nhân viên hỗ trợ khách hàng.

                ### 3. Nội dung & Lịch trình Đào tạo
                - **Học phần 1: Bắt đầu (30 phút)**
                - Chủ đề: Đăng ký, Đăng nhập, Tổng quan giao diện.
                - **Học phần 2: Mua sắm (60 phút)**
                - Chủ đề: Tìm kiếm, Lọc sản phẩm, Thêm vào giỏ hàng, Thanh toán.
            """,
            agent=agent,
            callback=lambda o: (
                write_output("2_requirements/Training_Plan.md", str(o)),
                shared_memory.set("phase_2", "training_plan", str(o))
                )
        )
    
    def create_requirement_tasks(requirement_agent, project_manager_agent):
        """
        Hàm điều phối chính: tạo, phân công và sắp xếp tất cả các task cho Giai đoạn Yêu cầu.
        """
        tasks_factory = RequirementTasksFactory()
        
        # Tạo các task chuyên môn và gán cho agent
        scope_task = tasks_factory.create_scope_task(agent=requirement_agent)
        brd_task = tasks_factory.create_brd_task(agent=requirement_agent)
        presentation_task = tasks_factory.create_presentation_task(agent=requirement_agent)
        srs_task = tasks_factory.create_srs_task(agent=requirement_agent)
        usecase_tasks_list = tasks_factory.create_usecase_tasks(agent=requirement_agent)
        rtm_task = tasks_factory.create_rtm_tasks(agent=requirement_agent)
        
        example_change_request = "Khách hàng yêu cầu thay đổi cơ chế xác thực, thêm lựa chọn đăng nhập bằng Zalo."
        impact_task = tasks_factory.create_impact_analysis_task(agent=requirement_agent, change_request=example_change_request)
        
        sla_task = tasks_factory.create_sla_task(agent=requirement_agent)
        nfr_task = tasks_factory.create_nfr_task(agent=requirement_agent)
        security_task = tasks_factory.create_security_task(agent=requirement_agent)
        checklist_task = tasks_factory.create_checklist_task(agent=requirement_agent)
        training_task = tasks_factory.create_training_task(agent=requirement_agent)

        # Thiết lập context để đảm bảo thứ tự thực thi tuần tự và logic
        brd_task.context = [scope_task]
        presentation_task.context = [brd_task]
        srs_task.context = [brd_task]
        nfr_task.context = [srs_task]
        security_task.context = [nfr_task]
        usecase_tasks_list[0].context = [srs_task]
        rtm_task.context = [srs_task]
        impact_task.context = [rtm_task]
        sla_task.context = [srs_task]
        training_task.context = [usecase_tasks_list[1]]
        checklist_task.context = [srs_task, rtm_task]

        # Danh sách các task cốt lõi cần được kiểm tra chất lượng
        core_tasks = [
            scope_task, brd_task, presentation_task, srs_task,
            usecase_tasks_list[0], usecase_tasks_list[1], rtm_task, impact_task, sla_task,
            nfr_task, security_task, checklist_task, training_task
        ]

        # Tạo task Quality Gate và giao cho Project Manager
        quality_gate_req_task = create_quality_gate_task(
            agent=project_manager_agent,
            phase_name="Phase 2: Requirements",
            keys_to_check="scope_checklist, brd_document, srs_document, rtm_document, nfr_document",
            document_names="Scope Checklist, BRD, SRS, RTM, NFRs, and all related documents."
        )
        quality_gate_req_task.context = core_tasks

        return core_tasks + [quality_gate_req_task]