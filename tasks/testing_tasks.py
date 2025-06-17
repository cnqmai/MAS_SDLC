"""
testing_tasks.py
===============================
Tổng hợp tất cả Tasks cho Testing Agent - Phase 5 Testing
Bao gồm: Test Planning, Test Cases, Security/Performance, QA Checklist, Audit, Test Execution, Test Management

Phase: Phase 5 – Testing

Inputs (shared_memory):
- functional_requirements (F.R.D)
- use_case_diagrams
- project_plan
- security_architecture
- non_functional_requirements (NFR)
- source_code_documentation
- code_review_checklist
- cobit_checklist
- qa_checklist

Outputs:
- Test_Plan.docx
- Regression_Testing_Plan.md
- User_Acceptance_Test_Plan.docx
- Test_Case_Specification.xlsx
- Testing_Bug_Report_Template.xlsx
- Testing_Bug_List.xlsx
- Penetration_Testing_Report.md
- Performance_Testing_Report.md
- Documentation_Quality_Assurance_Checklist.md
- System_Quality_Assurance_Checklist.md
- COBIT_Checklist_and_Review.md
- COBIT_Objectives_And_Audit_Activity_Report.md
- Test_Summary_Report.docx
- Interoperability_Test_Logs.md
- Connectivity_Testing_Report.md
- Risk_Management_Register.xlsx
- Issues_Management_Log.xlsx
- Project_Status_Report.md
- Meeting_Summary_Template.docx
- Project_Milestone_Status_Form_Template.docx
"""

from crewai import Task
from utils.file_writer import write_output
from memory.shared_memory import shared_memory


# ========================================
# TEST PLANNING TASKS
# ========================================

def create_test_plan_tasks(testing_agent):
    """Tạo các nhiệm vụ lập kế hoạch kiểm thử"""
    print("🧪 Khởi tạo các nhiệm vụ lập kế hoạch kiểm thử...")
    print("📥 Lấy dữ liệu từ shared_memory...")

    frd = shared_memory.get("phase_3_design", "functional_requirements") or "Chưa có Functional Requirements Document."
    use_cases = shared_memory.get("phase_3_design", "use_case_diagrams") or "Chưa có Use Case Diagram."
    project_plan = shared_memory.get("phase_1_planning", "project_plan") or "Chưa có Project Plan."

    print("✅ Đã tải xong dữ liệu đầu vào.")

    # Task 1: Master Test Plan
    master_test_plan = Task(
        description=f"""
            Tạo tài liệu chính Test_Plan.docx định hướng toàn bộ hoạt động kiểm thử.

            ### Inputs:
            - Functional Requirements: {frd[:300]}...
            - Use Case Diagrams: {use_cases[:300]}...
            - Project Plan: {project_plan[:300]}...

            ### Nội dung bắt buộc:
            1. Mục tiêu & phạm vi kiểm thử
            2. Mô hình kiểm thử (Agile, Waterfall...)
            3. Loại kiểm thử áp dụng: Unit, Integration, System, Regression, UAT
            4. Chiến lược kiểm thử: manual vs automation
            5. Môi trường, dữ liệu kiểm thử
            6. Test schedule mapping với project timeline
            7. Vai trò và trách nhiệm (Dev, QA, PO)
            8. Công cụ kiểm thử: quản lý testcase, defect, CI/CD
            9. Tiêu chí đầu vào/đầu ra & traceability matrix
            10. Sign-off policy và versioning

            ### Output:
            Test_Plan.docx
        """,
        expected_output="Test_Plan.docx – Tài liệu kế hoạch kiểm thử tổng thể toàn dự án.",
        agent=testing_agent,
        callback=lambda output: (
            write_output("output/5_testing/Test_Plan.docx", output),
            shared_memory.set("phase_5_testing", "test_plan", output)
        )
    )

    # Task 2: Regression Testing Plan
    regression_test_plan = Task(
        description=f"""
            Tạo tài liệu Regression_Testing_Plan.md mô tả chiến lược kiểm thử hồi quy.

            ### Inputs:
            - Functional Requirements: {frd[:300]}...
            - Project Plan: {project_plan[:300]}...

            ### Nội dung cần có:
            1. Trigger points (khi nào chạy regression)
            2. Danh sách test case quan trọng
            3. Kịch bản kiểm thử hồi quy
            4. Chiến lược tự động hóa regression test
            5. Lịch chạy regression (per sprint / pre-release)
            6. Theo dõi coverage và lỗi tái diễn
            7. Cấu hình môi trường đặc biệt (nếu có)

            ### Output:
            Regression_Testing_Plan.md
        """,
        expected_output="Regression_Testing_Plan.md – Tài liệu chiến lược kiểm thử hồi quy.",
        agent=testing_agent,
        callback=lambda output: (
            write_output("output/5_testing/Regression_Testing_Plan.md", output),
            shared_memory.set("phase_5_testing", "regression_plan", output)
        )
    )

    # Task 3: User Acceptance Testing (UAT) Plan
    uat_test_plan = Task(
        description=f"""
            Lập kế hoạch kiểm thử UAT để người dùng xác nhận hệ thống đúng như yêu cầu nghiệp vụ.

            ### Inputs:
            - Functional Requirements: {frd[:300]}...
            - Use Case Diagrams: {use_cases[:300]}...
            - Project Plan: {project_plan[:300]}...

            ### Nội dung yêu cầu:
            1. Mục tiêu và phạm vi UAT
            2. Đối tượng tham gia (Users, PO, QA, BA)
            3. Use case cần xác thực và kịch bản test
            4. Timeline UAT & môi trường thử nghiệm
            5. Cách thu thập phản hồi người dùng
            6. Tiêu chí pass/fail và sign-off
            7. Checklist chuẩn bị & trách nhiệm từng bên

            ### Output:
            User_Acceptance_Test_Plan.docx
        """,
        expected_output="User_Acceptance_Test_Plan.docx – Tài liệu kế hoạch kiểm thử UAT từ người dùng.",
        agent=testing_agent,
        callback=lambda output: (
            write_output("output/5_testing/User_Acceptance_Test_Plan.docx", output),
            shared_memory.set("phase_5_testing", "uat_plan", output)
        )
    )

    print("✅ Hoàn tất tạo các Test Plan Tasks.")
    return [master_test_plan, regression_test_plan, uat_test_plan]


# ========================================
# TEST CASE TASKS
# ========================================

def create_test_case_tasks(testing_agent):
    """Tạo các nhiệm vụ viết test case và bug tracking"""
    print("🧪 Bắt đầu khởi tạo Test Case & Bug Tracking Tasks...")
    print("📥 Đang truy xuất dữ liệu đầu vào từ shared_memory...")

    test_plan = shared_memory.get("phase_5_testing", "test_plan") or "Test Plan chưa có."
    frd = shared_memory.get("phase_2_requirement", "frd") or "F.R.D chưa sẵn sàng."
    use_cases = shared_memory.get("phase_2_requirement", "use_case_diagrams") or "Use Case Diagram chưa có."

    print("✅ Dữ liệu đã sẵn sàng.")

    # Task 1: Test Case Specification
    test_case_task = Task(
        description=f"""
            Viết tài liệu Test Case Specification chi tiết dựa trên Test Plan, F.R.D và Use Case Diagrams.

            ### Yêu cầu nội dung:
            - Test Case ID
            - Chức năng kiểm thử
            - Điều kiện tiền đề
            - Bước kiểm thử
            - Kết quả mong đợi
            - Kết quả thực tế (runtime)
            - Mức ưu tiên
            - Loại kiểm thử (functional, regression, UAT)
            - Traceability tới requirement
            - Trạng thái thực thi

            ### Inputs:
            - Test Plan: {test_plan[:400]}...
            - F.R.D: {frd[:400]}...
            - Use Case Diagrams: {use_cases[:400]}...

            ### Output:
            - File: Test_Case_Specification.xlsx
        """,
        expected_output="Test_Case_Specification.xlsx – Danh sách test case có traceability rõ ràng.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Hoàn thành đặc tả test case."),
            write_output("output/5_testing/Test_Case_Specification.xlsx", output),
            shared_memory.set("phase_5_testing", "test_case_specification", output)
        )
    )

    # Task 2: Bug Report Template
    bug_template_task = Task(
        description="""
            Tạo template chuẩn để tester log bug dễ dàng và thống nhất.

            ### Yêu cầu các trường:
            - Bug ID
            - Tên module/chức năng
            - Các bước tái hiện lỗi
            - Kết quả mong đợi vs thực tế
            - Mức độ nghiêm trọng (Severity)
            - Ưu tiên (Priority)
            - Môi trường kiểm thử
            - Người báo lỗi & thời gian
            - Trạng thái (Open, Fixed, Closed...)
            - Liên kết Test Case ID

            ### Output:
            - File: Testing_Bug_Report_Template.xlsx
        """,
        expected_output="Testing_Bug_Report_Template.xlsx – Mẫu chuẩn báo cáo bug cho tester.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Tạo xong Bug Report Template."),
            write_output("output/5_testing/Testing_Bug_Report_Template.xlsx", output),
            shared_memory.set("phase_5_testing", "bug_report_template", output)
        )
    )

    # Task 3: Bug List
    bug_list_task = Task(
        description="""
            Tổng hợp danh sách bug được ghi nhận trong quá trình kiểm thử.

            ### Required Columns:
            - Bug ID
            - Mô tả tóm tắt
            - Trạng thái hiện tại
            - Developer được giao xử lý
            - Severity & Priority
            - Test Case liên kết
            - Sprint hoặc bản phát hành
            - Version đã fix
            - Kết quả xác minh lại

            ### Output:
            - File: Testing_Bug_List.xlsx
        """,
        expected_output="Testing_Bug_List.xlsx – Danh sách bug đang được theo dõi & xác minh.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Tạo xong danh sách bug."),
            write_output("output/5_testing/Testing_Bug_List.xlsx", output),
            shared_memory.set("phase_5_testing", "bug_list", output)
        )
    )

    print("🎯 Đã định nghĩa xong 3 nhiệm vụ: test case, bug template, bug list.")
    return [test_case_task, bug_template_task, bug_list_task]


# ========================================
# SECURITY & PERFORMANCE TESTING TASKS
# ========================================

def create_security_perf_test_tasks(testing_agent):
    """Tạo các nhiệm vụ kiểm thử bảo mật và hiệu năng"""
    print("🚀 Bắt đầu khởi tạo Security & Performance Testing Tasks...")
    print("🔍 Truy xuất dữ liệu từ shared_memory...")

    security_doc = shared_memory.get("phase_5_testing", "security_architecture") or "Chưa có tài liệu Security Architecture."
    nfr_doc = shared_memory.get("phase_3_design", "non_functional_requirements") or "Chưa có NFR."

    print("✅ Dữ liệu đầu vào đã được tải thành công.")

    # Task 1: Penetration Testing Report
    penetration_task = Task(
        description=f"""
            Thực hiện kiểm thử thâm nhập hệ thống theo tiêu chuẩn OWASP, dựa trên tài liệu kiến trúc bảo mật và yêu cầu phi chức năng.

            ### Nội dung bắt buộc:
            1. Scope và mục tiêu kiểm thử bảo mật
            2. Các kiểu tấn công giả lập: SQLi, XSS, CSRF, IDOR, Auth bypass...
            3. Công cụ sử dụng: Burp Suite, OWASP ZAP, Metasploit, Kali Linux...
            4. Môi trường và kịch bản kiểm thử (whitebox/blackbox)
            5. Mức độ rủi ro (CVSS Score) và ảnh hưởng
            6. Log, PoC hoặc ảnh minh họa
            7. Đề xuất biện pháp khắc phục
            8. Tổng kết độ an toàn tổng thể

            ### Input:
            - Security Architecture Document: {security_doc[:800]}...
            - NFR: {nfr_doc[:500]}...

            ### Output:
            - File: Penetration_Testing_Report.md
        """,
        expected_output="Penetration_Testing_Report.md – Báo cáo đầy đủ về kết quả kiểm thử bảo mật hệ thống.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Đã tạo Penetration_Testing_Report.md"),
            write_output("output/5_testing/Penetration_Testing_Report.md", str(output)),
            shared_memory.set("phase_5_testing", "penetration_test_report", str(output))
        )
    )

    # Task 2: Performance Testing Report
    performance_task = Task(
        description=f"""
            Thực hiện kiểm thử hiệu năng hệ thống dựa trên các mục tiêu phi chức năng: tốc độ phản hồi, khả năng chịu tải và tính ổn định.

            ### Nội dung bắt buộc:
            1. Loại kiểm thử: Load, Stress, Spike, Soak
            2. Cấu hình hệ thống: OS, CPU, RAM, DB, Users
            3. Kịch bản kiểm thử và dữ liệu test
            4. Công cụ sử dụng: JMeter, k6, Locust, Artillery...
            5. Kết quả đo lường:
            - Avg/Max Response Time
            - Throughput (req/sec)
            - CPU/RAM/Network sử dụng
            - Tỷ lệ lỗi
            6. Bottleneck analysis & root cause
            7. Đề xuất cải tiến
            8. Đánh giá khả năng mở rộng

            ### Input:
            - NFR: {nfr_doc[:800]}...

            ### Output:
            - File: Performance_Testing_Report.md
        """,
        expected_output="Performance_Testing_Report.md – Báo cáo hiệu năng chi tiết theo NFR.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Đã tạo Performance_Testing_Report.md"),
            write_output("output/5_testing/Performance_Testing_Report.md", str(output)),
            shared_memory.set("phase_5_testing", "performance_test_report", str(output))
        )
    )

    print("📊 Hoàn thành khởi tạo task kiểm thử bảo mật & hiệu năng.")
    return [penetration_task, performance_task]


# ========================================
# QA CHECKLIST TASKS
# ========================================

def create_qa_checklist_tasks(testing_agent):
    """Tạo các nhiệm vụ QA checklist"""
    print("🚀 Bắt đầu khởi tạo QA Checklist Tasks...")
    print("🔍 Lấy dữ liệu từ bộ nhớ chia sẻ...")

    doc_data = shared_memory.get("phase_5_testing", "source_code_documentation") or "Source Code Documentation chưa có."
    code_review = shared_memory.get("phase_5_testing", "code_review_checklist") or "Code Review Checklist chưa có."

    print("✅ Dữ liệu đã sẵn sàng!")

    # Task 1: Documentation QA Checklist
    doc_checklist_task = Task(
        description=f"""
            Tạo checklist QA đánh giá chất lượng tài liệu mã nguồn để đảm bảo tính đầy đủ, dễ bảo trì, và hỗ trợ tốt việc onboarding.

            ### Nội dung checklist:
            1. Có kiến trúc hệ thống, API, module logic
            2. Hướng dẫn cài đặt và chạy (local/staging)
            3. Có ví dụ mã nguồn minh họa
            4. Cập nhật version gần nhất
            5. Liên kết giữa tài liệu và module tương ứng
            6. Tuân thủ chuẩn format và naming
            7. Không có lỗi ngữ pháp hoặc đánh máy
            8. Ghi rõ người viết / thời gian cập nhật
            9. Sử dụng tốt trong onboarding
            10. Được kiểm soát version (Git/docs tool)

            ### Inputs:
            - Source Code Documentation: {doc_data[:800]}...
            - Code Review Checklist: {code_review[:400]}...

            ### Output:
            - Documentation_Quality_Assurance_Checklist.md
        """,
        expected_output="Checklist Markdown: Documentation_Quality_Assurance_Checklist.md",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Hoàn tất checklist tài liệu."),
            write_output("output/5_testing/Documentation_Quality_Assurance_Checklist.md", str(output)),
            shared_memory.set("phase_5_testing", "qa_doc_checklist", str(output))
        )
    )

    # Task 2: System QA Checklist
    sys_checklist_task = Task(
        description=f"""
            Tạo checklist QA để đánh giá chất lượng hệ thống tổng thể dựa trên source code và kết quả review.

            ### Nội dung checklist:
            1. Tuân thủ coding standard (naming, structure)
            2. Unit test coverage ≥ 80%
            3. Không còn bug blocker hoặc critical defect
            4. CI/CD pipeline hoạt động ổn định
            5. Không chứa hardcoded secrets/token
            6. Không còn warning từ static analysis
            7. Code tối ưu: loại bỏ dead code, loop inefficiency
            8. Có logging và error handling rõ ràng
            9. Phân tách tốt giữa logic / config / I/O
            10. Hệ thống có khả năng mở rộng và bảo trì tốt

            ### Inputs:
            - Source Code Documentation: {doc_data[:500]}...
            - Code Review Checklist: {code_review[:500]}...

            ### Output:
            - System_Quality_Assurance_Checklist.md
        """,
        expected_output="Checklist Markdown: System_Quality_Assurance_Checklist.md",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Hoàn tất checklist hệ thống."),
            write_output("output/5_testing/System_Quality_Assurance_Checklist.md", str(output)),
            shared_memory.set("phase_5_testing", "qa_system_checklist", str(output))
        )
    )

    print("📋 QA Checklist Tasks đã được tạo thành công.")
    return [doc_checklist_task, sys_checklist_task]


# ========================================
# AUDIT TASKS
# ========================================

def create_audit_tasks(testing_agent):
    """Tạo các nhiệm vụ audit theo COBIT"""
    print("🚀 Bắt đầu tạo các nhiệm vụ Audit theo COBIT...")
    print("🔍 Truy xuất dữ liệu đầu vào từ shared memory...")

    cobit_checklist = shared_memory.get("phase_5_testing", "cobit_checklist") or "Không tìm thấy COBIT Checklist."
    qa_checklist = shared_memory.get("phase_5_testing", "qa_checklist") or "Không tìm thấy QA Checklist."

    print("✅ Dữ liệu đầu vào đã sẵn sàng.")

    # Task 1: COBIT Checklist Review
    review_task = Task(
        description=f"""
            Đánh giá hệ thống theo COBIT 2019 bằng cách đối chiếu các tiêu chí kiểm thử từ QA Checklist.

            ### Nội dung chính:
            1. Mapping COBIT domain (BAI, DSS, EDM) với QA checklist
            2. Phân tích độ phủ, điểm mạnh/yếu của hệ thống
            3. Liệt kê các gaps, rủi ro & đề xuất điều chỉnh
            4. Đánh giá tổng thể mức độ tuân thủ chuẩn COBIT

            ### Inputs:
            - COBIT Checklist: {cobit_checklist[:800]}...
            - QA Checklist: {qa_checklist[:800]}...

            ### Output:
            - Markdown: COBIT_Checklist_and_Review.md
        """,
        expected_output="COBIT_Checklist_and_Review.md – Đánh giá compliance theo domain COBIT.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Đã tạo COBIT_Checklist_and_Review.md"),
            write_output("output/5_testing/COBIT_Checklist_and_Review.md", str(output)),
            shared_memory.set("phase_5_testing", "cobit_review", str(output))
        )
    )

    # Task 2: COBIT Audit Report
    audit_report_task = Task(
        description=f"""
            Tổng hợp báo cáo các hoạt động audit, đối chiếu với mục tiêu COBIT và đưa ra đề xuất cải tiến.

            ### Nội dung bắt buộc:
            1. COBIT Objectives được kiểm tra (vd: BAI03, DSS05)
            2. Phân tích bằng chứng kiểm thử & kỹ thuật giám sát
            3. Phát hiện non-conformities và mức độ rủi ro
            4. Đề xuất hoạt động kiểm soát hoặc cải tiến
            5. Kế hoạch xác minh lại
            6. Nhận xét tổng kết của auditor

            ### Inputs:
            - COBIT Checklist: {cobit_checklist[:800]}...
            - QA Checklist: {qa_checklist[:800]}...

            ### Output:
            - Markdown: COBIT_Objectives_And_Audit_Activity_Report.md
        """,
        expected_output="COBIT_Objectives_And_Audit_Activity_Report.md – Báo cáo giám sát & đề xuất cải tiến theo COBIT.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Đã tạo COBIT_Objectives_And_Audit_Activity_Report.md"),
            write_output("output/5_testing/COBIT_Objectives_And_Audit_Activity_Report.md", str(output)),
            shared_memory.set("phase_5_testing", "cobit_audit", str(output))
        )
    )

    print("✅ Hoàn tất tạo các Audit Tasks.")
    return [review_task, audit_report_task]


# ========================================
# TEST EXECUTION TASKS
# ========================================

def create_test_execution_tasks(testing_agent):
    """Tạo các nhiệm vụ thực thi kiểm thử"""
    print("🚦 Bắt đầu khởi tạo Test Execution Tasks...")
    print("📥 Truy xuất dữ liệu kiểm thử từ shared memory...")

    test_cases = shared_memory.get("phase_5_testing", "test_case_specification") or "Test Case Specification chưa có."
    bug_list = shared_memory.get("phase_5_testing", "bug_list") or "Bug List chưa có."

    print("✅ Dữ liệu đã sẵn sàng.")

    # Task 1: Test Summary Report
    summary_task = Task(
        description=f"""
            Tạo tài liệu tổng hợp kết quả thực thi kiểm thử toàn hệ thống, bao gồm tỷ lệ thành công, lỗi, coverage và đánh giá sẵn sàng triển khai.

            ### Inputs:
            - Test Case Specification: {test_cases[:400]}...
            - Bug List: {bug_list[:400]}...

            ### Nội dung cần có:
            1. Tổng số test case đã thực thi
            2. Tỷ lệ pass/fail & biểu đồ thống kê
            3. Danh sách & phân tích defect (theo severity)
            4. Mức độ coverage & traceability
            5. Module có lỗi nổi bật
            6. Kết luận chất lượng hệ thống
            7. Đề xuất cải tiến trước khi release
            8. Xác nhận QA lead

            ### Output:
            Test_Summary_Report.docx
        """,
        expected_output="Test_Summary_Report.docx – Tổng hợp kết quả thực thi kiểm thử hệ thống.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Báo cáo Test Summary đã hoàn thành."),
            write_output("output/5_testing/Test_Summary_Report.docx", output),
            shared_memory.set("phase_5_testing", "test_summary_report", output)
        )
    )

    # Task 2: Interoperability Logs
    interoperability_task = Task(
        description="""
            Ghi log kiểm thử tính tương thích (interoperability) giữa các module, dịch vụ, hệ thống hoặc phiên bản.

            ### Nội dung:
            - Môi trường kiểm thử (OS, DB, microservices, API gateway...)
            - Scenarios: cross-version, backward compatibility
            - Ghi nhận lỗi tương thích & xử lý
            - Kết luận mức độ tương thích và rủi ro tồn đọng

            ### Output:
            - Interoperability_Test_Logs.md
        """,
        expected_output="Interoperability_Test_Logs.md – Log kiểm thử tương thích chi tiết.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Log kiểm thử tương thích đã được ghi."),
            write_output("output/5_testing/Interoperability_Test_Logs.md", output),
            shared_memory.set("phase_5_testing", "interoperability_logs", output)
        )
    )

    # Task 3: Connectivity Testing Report
    connectivity_task = Task(
        description="""
            Tạo báo cáo kiểm thử kết nối hệ thống giữa các thành phần chính (frontend, backend, database, APIs).

            ### Nội dung bắt buộc:
            - Scope kiểm thử kết nối
            - Kết quả kiểm thử mạng (timeout, DNS, SSL handshake, retry logic)
            - Báo cáo status các endpoint/API
            - Phân tích bottleneck kết nối
            - Đề xuất cải thiện reliability hoặc config

            ### Output:
            - Connectivity_Testing_Report.md
        """,
        expected_output="Connectivity_Testing_Report.md – Báo cáo kiểm thử kết nối chi tiết và cải tiến đề xuất.",
        agent=testing_agent,
        callback=lambda output: (
            print("✅ Báo cáo kiểm thử kết nối hoàn tất."),
            write_output("output/5_testing/Connectivity_Testing_Report.md", output),
            shared_memory.set("phase_5_testing", "connectivity_test_report", output)
        )
    )

    print("🎯 Hoàn tất định nghĩa các nhiệm vụ thực thi kiểm thử.")
    return [summary_task, interoperability_task, connectivity_task]

def create_test_management_tasks(testing_agent):
    print("🛠️ Bắt đầu tạo các Test Management Tasks...")
    print("📥 Truy xuất dữ liệu từ shared_memory...")

    bug_report = shared_memory.get("phase_5_testing", "bug_list") or "Bug list chưa có."
    test_summary = shared_memory.get("phase_5_testing", "test_summary_report") or "Test summary chưa có."

    print("✅ Dữ liệu đã được load.")

    # Task 1: Risk Management Register
    risk_task = Task(
        description=f"""
            Tạo file Risk Register dựa trên các lỗi nghiêm trọng trong kiểm thử và phân tích từ báo cáo tổng hợp.

            ### Inputs:
            - Bug List: {bug_report[:300]}...
            - Test Summary Report: {test_summary[:300]}...

            ### Output:
            - File: Risk_Management_Register.xlsx

            ### Cột cần có:
            - Risk ID, Description, Root Cause
            - Impact, Probability, Severity, Owner
            - Mitigation Action, Status, Review Date
        """,
        expected_output="Risk_Management_Register.xlsx – Danh sách rủi ro được phát hiện qua kiểm thử.",
        agent=testing_agent,
        callback=lambda output: write_output("output/5_testing/Risk_Management_Register.xlsx", output)
    )

    # Task 2: Issues Management Log
    issues_task = Task(
        description="""
            Tạo bảng log quản lý các sự cố (issues) phát sinh trong quá trình kiểm thử.

            ### Output:
            - File: Issues_Management_Log.xlsx

            ### Trường yêu cầu:
            - Issue ID, Description, Priority, Status
            - Date Reported, Owner, Root Cause
            - Action Taken, Resolution Date, Comments
        """,
        expected_output="Issues_Management_Log.xlsx – Bảng theo dõi và xử lý sự cố QA.",
        agent=testing_agent,
        callback=lambda output: write_output("output/5_testing/Issues_Management_Log.xlsx", output)
    )

    # Task 3: Project Status Report
    status_report_task = Task(
        description=f"""
            Tạo báo cáo tiến độ dự án kiểm thử để cập nhật cho PM hoặc Stakeholder.

            ### Input:
            - Test Summary Report: {test_summary[:300]}...

            ### Output:
            - File: Project_Status_Report.md

            ### Nội dung:
            1. % hoàn thành kiểm thử
            2. Tình trạng bug blocker & tổng defect
            3. Mức độ coverage & chất lượng
            4. UAT readiness & các milestone quan trọng
            5. Go / No-Go Recommendation
        """,
        expected_output="Project_Status_Report.md – Báo cáo tiến độ dự án dưới góc nhìn QA.",
        agent=testing_agent,
        callback=lambda output: write_output("output/5_testing/Project_Status_Report.md", output)
    )

    # Task 4: Meeting Summary Template
    meeting_summary_task = Task(
        description="""
            Tạo mẫu biên bản họp cho các phiên review QA/UAT/Defect.

            ### Output:
            - File: Meeting_Summary_Template.docx

            ### Nội dung:
            - Meeting Title, Date, Time, Facilitator
            - Participants, Agenda, Discussion Summary
            - Decisions Taken, Action Items, Next Steps
        """,
        expected_output="Meeting_Summary_Template.docx – Mẫu chuẩn biên bản họp QA.",
        agent=testing_agent,
        callback=lambda output: write_output("output/5_testing/Meeting_Summary_Template.docx", output)
    )

    # Task 5: Project Milestone Status Form Template
    milestone_status_task = Task(
        description="""
            Tạo form theo dõi tiến độ milestone testing và chấp nhận (QA, UAT, Regression...).

            ### Output:
            - File: Project_Milestone_Status_Form_Template.docx

            ### Nội dung:
            - Milestone Name, Description, Due Date
            - Completion %, Status, Risk/Issues
            - Owner, Dependency, Notes
        """,
        expected_output="Project_Milestone_Status_Form_Template.docx – Form theo dõi tiến độ milestone QA/UAT.",
        agent=testing_agent,
        callback=lambda output: write_output("output/5_testing/Project_Milestone_Status_Form_Template.docx", output)
    )

    print("✅ Đã định nghĩa đầy đủ các nhiệm vụ quản lý kiểm thử.")
    return [
        risk_task,
        issues_task,
        status_report_task,
        meeting_summary_task,
        milestone_status_task
    ]