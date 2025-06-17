# planning_phase_tasks.py
# This file contains all task creation functions for the Planning Phase of the project.

from crewai import Task
from crewai.tasks.task_output import TaskOutput
from utils.file_writer import write_output
from memory.shared_memory import shared_memory

# --- Helper function for callbacks ---
def _save_task_output(task_output: TaskOutput, phase: str, key: str, folder: str, filename: str):
    """A standardized callback function to save task output."""
    output_content = str(task_output.raw_output)
    task_title = key.replace('_', ' ').title()
    print(f"--- Nhiệm Vụ {task_title} Hoàn Thành ---")
    write_output(f"{folder}/{filename}", output_content)
    shared_memory.set(phase, key, output_content)

# --- Task Creation Functions ---

def create_costing_tasks(planning_agent):
    """Tạo các nhiệm vụ liên quan đến ước tính chi phí chi tiết."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    cost_estimation_task = Task(
        description=f"""Tạo một Bảng tính Excel chi tiết để Ước lượng Chi phí Dự án (Cost Estimation Worksheet).
    Tệp Excel này phải là một công cụ thực tế giúp Quản lý Dự án và các bên liên quan ước tính toàn diện
    các chi phí liên quan đến việc thực hiện một dự án.

    Bảng tính cần có cấu trúc rõ ràng, sử dụng các trang tính (sheets) riêng biệt để phân loại chi phí:

    **1. Trang 'Tổng quan' (Summary):**
       - Hiển thị tổng hợp các chi phí chính từ các trang tính khác.
       - Các mục chính: Tổng Chi phí Nhân sự, Tổng Chi phí Phần cứng/Phần mềm, Tổng Chi phí Bên thứ ba, Chi phí Quản lý/Gián tiếp.
       - Tính toán Chi phí Dự phòng (Contingency), thường là một tỷ lệ phần trăm (ví dụ: 15%) của tổng chi phí.
       - Hiển thị TỔNG CHI PHÍ DỰ ÁN (bao gồm dự phòng).
       - Nên có một biểu đồ hình tròn (pie chart) để trực quan hóa tỷ trọng của các loại chi phí.

    **2. Trang 'Chi phí Nhân sự' (Labor Costs):**
       - Liệt kê các vai trò trong dự án (ví dụ: Quản lý Dự án, Kỹ sư Phần mềm, Chuyên viên QA, Nhà thiết kế UI/UX).
       - Các cột: Vai trò, Số lượng, Đơn giá (theo giờ/ngày/tháng), Số giờ/ngày/tháng dự kiến, Thành tiền.
       - Tự động tính tổng chi phí cho mỗi vai trò và tổng chi phí nhân sự.

    **3. Trang 'Chi phí Cứng & Mềm' (Hardware & Software Costs):**
       - Liệt kê các chi phí liên quan đến phần cứng (máy chủ, máy tính) và phần mềm (bản quyền, license, dịch vụ đám mây).
       - Các cột: Hạng mục, Mô tả, Chi phí một lần (One-time), Chi phí định kỳ (Recurring - theo tháng/năm), Tổng chi phí.

    **4. Trang 'Chi phí Khác' (Other Costs):**
       - Dùng cho các chi phí không thuộc các loại trên.
       - Ví dụ: Chi phí đi lại, chi phí thuê văn phòng, chi phí cho nhà cung cấp/tư vấn bên ngoài.
       - Cấu trúc tương tự các trang chi phí khác.

    **5. Trang 'Hướng dẫn' (Instructions):**
       - Một trang tính đơn giản giải thích cách sử dụng bảng tính, ý nghĩa của các thuật ngữ và các ô cần nhập liệu.
    """,
    expected_output="""Một tệp Excel (.xlsx) hoàn chỉnh có tên 'Cost_Estimation_Worksheet.xlsx'.
    Tệp phải được định dạng chuyên nghiệp, với các công thức được thiết lập sẵn để tự động tính toán tổng số.
    Tất cả các trang tính phải chứa dữ liệu mẫu thực tế cho một dự án giả định (ví dụ: "Dự án Phát triển Ứng dụng Di động")
    để người dùng có thể dễ dàng hiểu và tùy chỉnh. Ngôn ngữ sử dụng trong tệp là Tiếng Việt.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "cost_estimation_worksheet", "1_costing", "cost_estimation_worksheet.md")
    )

    development_estimation_task = Task(
        description=f"""Xây dựng một Bảng tính Excel để Ước lượng Nỗ lực Phát triển Phần mềm (Development Effort Estimation).
    Công cụ này tập trung vào việc chia nhỏ các yêu cầu của dự án thành các hạng mục công việc (tasks) và
    ước tính nỗ lực (thường là person-hours hoặc story points) cho từng hạng mục.

    Bảng tính cần bao gồm các yếu tố sau:

    **1. Phân rã Công việc (Work Breakdown Structure):**
       - Cấu trúc phân cấp để liệt kê công việc: Epic > User Story > Task.
       - Sử dụng tính năng nhóm (grouping) của Excel để có thể thu gọn/mở rộng các cấp.

    **2. Kỹ thuật Ước tính 3 điểm (Three-point Estimation):**
       - Đối với mỗi hạng mục công việc (task), cần có các cột để nhập ước tính:
         - **Ước tính Lạc quan (Optimistic - O):** Thời gian hoàn thành trong điều kiện tốt nhất.
         - **Ước tính Thực tế (Most Likely - M):** Thời gian hoàn thành trong điều kiện bình thường.
         - **Ước tính Bi quan (Pessimistic - P):** Thời gian hoàn thành trong điều kiện xấu nhất.

    **3. Tính toán Trọng số (Weighted Average - PERT):**
       - Tự động tính toán nỗ lực ước tính cuối cùng bằng công thức PERT: **(O + 4M + P) / 6**.
       - Cung cấp một cột cho 'Độ lệch chuẩn' (Standard Deviation): **(P - O) / 6** để đo lường mức độ không chắc chắn.

    **4. Các Cột Thông tin Bổ sung:**
       - **Người thực hiện (Assignee):** Để gán công việc cho thành viên nhóm.
       - **Mức độ Ưu tiên (Priority):** Cao, Trung bình, Thấp.
       - **Trạng thái (Status):** Chưa bắt đầu, Đang thực hiện, Hoàn thành.
       - **Ghi chú/Giả định (Notes/Assumptions):** Một cột quan trọng để ghi lại các giả định đằng sau mỗi ước tính.

    **5. Trang 'Tổng hợp' (Summary):**
       - Tổng hợp tổng nỗ lực ước tính (tính bằng giờ hoặc ngày) cho toàn bộ dự án.
       - Biểu đồ Gantt đơn giản (sử dụng biểu đồ thanh của Excel) để trực quan hóa tiến trình các Epic lớn.
    """,
    expected_output="""Một tệp Excel (.xlsx) có tên 'Development_Estimation.xlsx'.
    Tệp phải được cấu trúc logic với các công thức PERT và Độ lệch chuẩn đã được cài đặt sẵn.
    Nó phải bao gồm dữ liệu mẫu cho một dự án phát triển web giả định (ví dụ: "Xây dựng Trang thương mại điện tử")
    với các Epic như 'Quản lý Người dùng', 'Danh mục Sản phẩm', 'Giỏ hàng & Thanh toán'.
    Ngôn ngữ sử dụng trong tệp là Tiếng Việt.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "development_estimation", "1_costing", "development_estimation.md")
    )

    capex_opex_comparison_task = Task(
        ddescription=f"""Tạo một Bảng tính Excel để phân tích và so sánh giữa Chi phí Đầu tư (CapEx) và
    Chi phí Vận hành (OpEx). Công cụ này rất quan trọng để đưa ra quyết định tài chính,
    ví dụ như lựa chọn giữa việc mua máy chủ vật lý (CapEx-heavy) và sử dụng dịch vụ đám mây (OpEx-heavy).

    Bảng tính cần có cấu trúc như sau:

    **1. Trang 'Đầu vào & Giả định' (Inputs & Assumptions):**
       - Một khu vực tập trung để người dùng nhập các biến số chính:
         - **Thời gian phân tích (Năm):** Ví dụ: 3, 5, hoặc 7 năm.
         - **Tỷ lệ chiết khấu (Discount Rate):** Dùng để tính Giá trị Hiện tại Ròng (NPV).
         - **Tỷ lệ lạm phát (Inflation Rate):** Để điều chỉnh chi phí vận hành hàng năm.
         - **Thuế suất (Tax Rate):** Để tính toán lợi ích từ khấu hao (nếu có).

    **2. Trang 'Phân tích Kịch bản' (Scenario Analysis):**
       - Chia thành hai phần rõ ràng để so sánh song song: **Kịch bản 1 (Ví dụ: On-Premise/CapEx)** và **Kịch bản 2 (Ví dụ: Cloud/OpEx)**.
       - **Đối với Kịch bản CapEx:**
         - Chi phí đầu tư ban đầu (Năm 0): Mua sắm phần cứng, phần mềm, chi phí cài đặt.
         - Chi phí vận hành hàng năm (Năm 1, 2, 3...): Điện, làm mát, bảo trì, nhân sự IT.
         - Tính toán khấu hao tài sản hàng năm (Depreciation).
       - **Đối với Kịch bản OpEx:**
         - Chi phí thiết lập ban đầu (nếu có).
         - Chi phí thuê bao/sử dụng hàng năm (Năm 1, 2, 3...): Phí dịch vụ đám mây, phí license.

    **3. Trang 'Bảng so sánh & Kết quả' (Comparison & Results):**
       - Trình bày kết quả phân tích một cách rõ ràng:
         - **Tổng Chi phí Sở hữu (Total Cost of Ownership - TCO):** Tính tổng chi phí cho mỗi kịch bản qua các năm.
         - **Giá trị Hiện tại Ròng của Chi phí (Net Present Value - NPV of Costs):** Tính toán NPV cho dòng tiền chi phí của mỗi kịch bản, sử dụng tỷ lệ chiết khấu đã nhập. Đây là thước đo so sánh chính xác nhất.
         - **Phân tích hòa vốn (Breakeven Analysis - nếu có thể):** Điểm thời gian mà tổng chi phí của hai kịch bản bằng nhau.
       - **Kết luận:** Một ô văn bản tóm tắt kết quả ("Kịch bản nào hiệu quả hơn về mặt tài chính và tại sao").
       - **Biểu đồ:** Biểu đồ đường (line chart) so sánh chi phí tích lũy của hai kịch bản qua từng năm.
    """,
    expected_output="""Một tệp Excel (.xlsx) chuyên nghiệp có tên 'Capex_Opex_Comparison.xlsx'.
    Tệp phải chứa các công thức tài chính phức tạp như NPV và TCO được cài đặt sẵn.
    Dữ liệu mẫu phải so sánh một trường hợp sử dụng cụ thể, ví dụ: "Triển khai hệ thống CRM: Mua license vĩnh viễn (CapEx)
    so với Thuê bao hàng tháng trên nền tảng đám mây (OpEx)" trong vòng 5 năm.
    Các thuật ngữ tài chính (CapEx, OpEx, TCO, NPV) nên được giữ nguyên bằng tiếng Anh để đảm bảo tính chính xác và phổ quát.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "capex_opex_comparison", "1_costing", "capex_opex_comparison.md")
    )

    return [cost_estimation_task, development_estimation_task, capex_opex_comparison_task]


def create_approval_tasks(planning_agent):
    """Tạo nhiệm vụ soạn thảo tài liệu phê duyệt dự án."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    project_approval_document = Task(
        description=f"""Soạn thảo một "Tài liệu Phê duyệt Dự án" (Project Approval Document) chính thức và toàn diện.
    Đây là tài liệu tổng hợp cuối cùng được trình lên Ban Lãnh đạo hoặc Hội đồng Quản trị Dự án (Steering Committee)
    để xin phê duyệt chính thức cho việc triển khai dự án. Tài liệu này chắt lọc những thông tin cốt lõi nhất
    từ Hiến chương, Phân tích Chi phí-Lợi ích, và các kế hoạch cấp cao.

    Mục tiêu là cung cấp một cái nhìn tổng quan, thuyết phục và đầy đủ để người phê duyệt có thể ra quyết định "Go/No-Go" cuối cùng.

    **1. Tóm tắt cho Lãnh đạo (Executive Summary):**
       - Tên dự án, Quản lý dự án, Nhà tài trợ.
       - Tuyên bố vấn đề/cơ hội một cách ngắn gọn.
       - Mô tả giải pháp (dự án) và kết quả chính mong đợi.
       - Yêu cầu chính: Phê duyệt dự án với tổng ngân sách là X và thời gian thực hiện là Y.

    **2. Luận điểm Kinh doanh và Sự phù hợp Chiến lược (Business Case & Strategic Alignment):**
       - Tóm tắt lại lý do tại sao dự án này cần thiết.
       - Giải thích rõ dự án này đóng góp như thế nào vào các mục tiêu chiến lược của tổ chức.
       - Trích dẫn các chỉ số tài chính quan trọng nhất từ Phân tích Chi phí-Lợi ích (ví dụ: ROI, Thời gian hoàn vốn, NPV).

    **3. Tóm tắt Phạm vi và Sản phẩm Bàn giao (Scope and Deliverables Summary):**
       - Mô tả ngắn gọn những gì nằm trong phạm vi (In-Scope).
       - Liệt kê các sản phẩm bàn giao chính (Key Deliverables) mà dự án sẽ tạo ra.

    **4. Tóm tắt Lịch trình và Ngân sách (Schedule and Budget Summary):**
       - **Lịch trình:** Trình bày các cột mốc quan trọng nhất và ngày dự kiến hoàn thành.
       - **Ngân sách:** Nêu rõ tổng ngân sách yêu cầu, bao gồm chi phí trực tiếp và các khoản dự phòng (contingency/management reserves).

    **5. Tóm tắt Rủi ro Chính (Key Risks Summary):**
       - Liệt kê 3-5 rủi ro hàng đầu có khả năng ảnh hưởng lớn nhất đến dự án.
       - Đối với mỗi rủi ro, mô tả ngắn gọn kế hoạch ứng phó cấp cao.

    **6. Quản trị Dự án và Các Bên liên quan Chính (Governance and Key Stakeholders):**
       - Xác định cấu trúc quản trị (ai báo cáo cho ai, vai trò của Hội đồng Quản trị Dự án).
       - Liệt kê các bên liên quan có ảnh hưởng cao nhất và vai trò của họ trong việc hỗ trợ dự án.

    **7. Yêu cầu Phê duyệt (Approval Request):**
       - Một tuyên bố chính thức yêu cầu sự phê duyệt để tiến hành dự án.
       - "Chúng tôi trân trọng đề nghị Ban Lãnh đạo phê duyệt dự án [Tên dự án] với phạm vi, lịch trình và ngân sách như đã nêu trên."

    **8. Phần Ký duyệt (Signatures):**
       - Chừa không gian cho chữ ký của tất cả các bên có thẩm quyền cần thiết để phê duyệt dự án.
       - Ví dụ: Nhà tài trợ Dự án (Project Sponsor), Giám đốc Tài chính (CFO), Giám đốc Điều hành (CEO), Trưởng PMO.
    """,
    expected_output="""Một "Tài liệu Phê duyệt Dự án" trang trọng, súc tích và thuyết phục dưới dạng Markdown.
    Tài liệu phải tổng hợp được tất cả các thông tin quan trọng nhất vào một định dạng dễ hiểu cho lãnh đạo cấp cao.
    Kết quả phải là một văn bản chính thức, đóng vai trò là bằng chứng cho việc dự án đã được phê duyệt để triển khai.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "project_approval_document", "1_approval", "project_approval_document.md")
    )
    return [project_approval_document]


def create_org_chart_tasks(planning_agent):
    """Tạo các nhiệm vụ liên quan đến sơ đồ tổ chức và ma trận trách nhiệm."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    org_chart = Task(
        description=f"""Thiết kế và xây dựng một "Sơ đồ Tổ chức" (Organizational Chart - Org Chart) chính thức và chi tiết.
    Tài liệu này là một công cụ quản lý và tham chiếu quan trọng, được sử dụng để trực quan hóa cấu trúc nội bộ,
    các tuyến báo cáo và mối quan hệ giữa các vị trí và phòng ban trong một tổ chức.
    Mục tiêu là tạo ra một sơ đồ rõ ràng, chính xác và cập nhật, giúp mọi người hiểu rõ vai trò và cấu trúc của công ty.

    Sơ đồ Tổ chức cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu ngắn gọn về lý do cần xây dựng hoặc cập nhật sơ đồ tổ chức (ví dụ: tái cấu trúc, tăng trưởng nhanh, dự án mới).
       - Mô tả các vấn đề mà sơ đồ này sẽ giải quyết (ví dụ: sự mơ hồ về vai trò, khó khăn trong giao tiếp).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: làm rõ tuyến báo cáo, hỗ trợ giới thiệu nhân viên mới, lập kế hoạch nhân sự).

    **2. Phạm vi và Cấp độ Chi tiết (Scope and Level of Detail):**
       - Đây là phần xác định mức độ bao quát của sơ đồ.
       - **Các Đơn vị trong Phạm vi (In-Scope Units):** Liệt kê rõ các phòng ban, đội nhóm, hoặc dự án sẽ được bao gồm trong sơ đồ.
       - **Các Đơn vị ngoài Phạm vi (Out-of-Scope Units):** Nêu rõ những gì sẽ KHÔNG được hiển thị (ví dụ: không bao gồm các vị trí thực tập sinh, nhà thầu bên ngoài, hoặc các công ty con chưa tích hợp).

    **3. Các Thành phần và Thông tin Hiển thị (Chart Components and Information):**
       - Liệt kê tất cả các thông tin sẽ được hiển thị cho mỗi vị trí trên sơ đồ.
       - Ví dụ: Họ và tên, Chức danh, Phòng ban, ID nhân viên, Ảnh chân dung, Tuyến báo cáo trực tiếp (cấp trên).
       - Xác định các sản phẩm bàn giao cuối cùng (ví dụ: file PDF, file ảnh PNG, file gốc có thể chỉnh sửa, liên kết đến phiên bản tương tác trực tuyến).

    **4. Định dạng và Công cụ (Format and Tools):**
       - Quy định rõ định dạng của sơ đồ (ví dụ: sơ đồ phân cấp từ trên xuống, sơ đồ ma trận).
       - Xác định công cụ sẽ được sử dụng để tạo và duy trì sơ đồ (ví dụ: Microsoft Visio, Lucidchart, PowerPoint, một phần mềm HRIS cụ thể).

    **5. Quy trình Thu thập Dữ liệu và Phê duyệt (Data Collection and Approval Process):**
       - Mô tả nguồn dữ liệu để xây dựng sơ đồ (ví dụ: hệ thống HRIS, xác nhận từ Trưởng phòng Nhân sự, thông tin từ các trưởng bộ phận).
       - Định nghĩa các tiêu chí để xác định sơ đồ là "chính xác" và "hoàn chỉnh".
       - Mô tả quy trình rà soát và phê duyệt (ví dụ: bản nháp được gửi cho các trưởng bộ phận để xác minh, bản cuối cùng được CEO/Giám đốc Nhân sự phê duyệt).

    **6. Các Giả định và Ràng buộc (Assumptions and Constraints):**
       - Liệt kê các giả định (ví dụ: "Dữ liệu từ phòng Nhân sự cung cấp là phiên bản mới nhất và chính xác").
       - Nêu các ràng buộc (ví dụ: "Phải tuân thủ mẫu branding của công ty", "Chỉ sử dụng phần mềm đã được cấp phép").

    **7. Vai trò và Trách nhiệm (Roles and Responsibilities):**
       - Xác định rõ trách nhiệm của các bên liên quan:
         - **Người cung cấp dữ liệu:** (ví dụ: Phòng Nhân sự).
         - **Người thiết kế sơ đồ:** (ví dụ: Nhà cung cấp, phòng ban nội bộ).
         - **Người rà soát và phê duyệt:** (ví dụ: Các trưởng bộ phận, Ban lãnh đạo).

    **8. Bảo mật và Phân phối (Confidentiality and Distribution):**
       - Nêu rõ các quy định về bảo mật thông tin trên sơ đồ.
       - Mô tả kế hoạch phân phối sơ đồ sau khi được phê duyệt (ví dụ: đăng trên mạng nội bộ, gửi email cho toàn công ty, chỉ chia sẻ với cấp quản lý).

    **9. Quy trình Cập nhật và Bảo trì (Update and Maintenance Process):**
       - Mô tả quy trình xử lý khi có thay đổi về nhân sự (nhân viên mới, thăng chức, nghỉ việc).
       - Định nghĩa tần suất rà soát và cập nhật định kỳ (ví dụ: hàng quý, hàng năm).
       - Chỉ định người hoặc bộ phận chịu trách nhiệm bảo trì sơ đồ.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của đại diện có thẩm quyền (ví dụ: Giám đốc Nhân sự, Giám đốc Điều hành) để xác nhận phiên bản chính thức của sơ đồ tổ chức.
    """,
    expected_output="""Một tài liệu "Đặc tả Sơ đồ Tổ chức" (Org Chart Specification) hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu này phải được viết với ngôn ngữ rõ ràng, chính xác, nhằm mục đích tạo ra một bản kế hoạch không mơ hồ cho việc xây dựng và duy trì sơ đồ.
    Kết quả phải là một tài liệu tham chiếu tin cậy cho tất cả các bên liên quan về cấu trúc, nội dung, và quy trình quản lý sơ đồ tổ chức.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "org_chart_specification", "1_org_chart", "org_chart_specification.md")
    )

    roles_responsibilities_matrix = Task(
        description=f"""Soạn thảo một tài liệu "Đặc tả Ma trận Phân công Vai trò và Trách nhiệm" (Roles and Responsibilities Matrix Specification).
    Tài liệu này đóng vai trò là bản kế hoạch chi tiết để xây dựng một Ma trận RACI (Responsible, Accountable, Consulted, Informed).
    Mục tiêu là tạo ra một công cụ quản lý rõ ràng, giúp loại bỏ sự mơ hồ về vai trò, cải thiện giao tiếp và tăng cường trách nhiệm giải trình trong một dự án hoặc đội nhóm.

    Tài liệu đặc tả này cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu ngắn gọn về dự án, quy trình hoặc phòng ban mà ma trận này sẽ áp dụng.
       - Mô tả các vấn đề cần giải quyết (ví dụ: sự nhầm lẫn về người ra quyết định cuối cùng, các tác vụ bị bỏ sót, nhiều người cùng làm một việc).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: xác định rõ một người duy nhất chịu trách nhiệm giải trình (Accountable) cho mỗi tác vụ, đảm bảo các bên liên quan được tham vấn (Consulted) và thông báo (Informed) kịp thời).

    **2. Phạm vi Áp dụng (Scope of Application):**
       - Đây là phần xác định ranh giới của ma trận.
       - **Các Tác vụ/Quy trình trong Phạm vi (In-Scope Tasks/Processes):** Liệt kê các hoạt động, sản phẩm bàn giao, hoặc các quyết định chính sẽ được đưa vào ma trận.
       - **Các Vai trò trong Phạm vi (In-Scope Roles):** Liệt kê tất cả các chức danh, vai trò hoặc cá nhân sẽ được đưa vào các cột của ma trận.
       - **Ngoài Phạm vi (Out-of-Scope):** Nêu rõ những gì sẽ KHÔNG được ma trận này bao quát để giữ cho nó tập trung và dễ quản lý (ví dụ: các công việc hành chính hàng ngày, các quy trình của phòng ban khác).

    **3. Các Thành phần của Ma trận (Matrix Components):**
       - **Danh sách Tác vụ (Task List):** Mô tả chi tiết các dòng của ma trận. Mỗi tác vụ cần được định nghĩa một cách rõ ràng và không chồng chéo.
       - **Danh sách Vai trò (Role List):** Mô tả chi tiết các cột của ma trận.
       - **Định nghĩa RACI (RACI Definitions):** Cung cấp định nghĩa chính xác và được thống nhất cho từng ký tự:
         - **R (Responsible):** Người thực hiện công việc.
         - **A (Accountable):** Người chịu trách nhiệm giải trình cuối cùng. Phải có và chỉ có một "A" cho mỗi tác vụ.
         - **C (Consulted):** Người cần được hỏi ý kiến, giao tiếp hai chiều.
         - **I (Informed):** Người cần được thông báo về tiến độ hoặc kết quả, giao tiếp một chiều.

    **4. Lịch trình Xây dựng và Các Cột mốc (Development Schedule and Milestones):**
       - Trình bày một lịch trình chi tiết cho việc xây dựng và hoàn thiện ma trận.
       - Xác định các cột mốc quan trọng, ví dụ:
         - "Hoàn thành danh sách Tác vụ và Vai trò nháp - [Ngày]"
         - "Tổ chức phiên làm việc (workshop) để gán RACI - [Ngày]"
         - "Hoàn thành bản nháp Ma trận RACI - [Ngày]"
         - "Ma trận RACI được phê duyệt cuối cùng - [Ngày]"

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định ma trận đã hoàn chỉnh và hợp lệ (ví dụ: "Mọi tác vụ đều có một và chỉ một 'A'", "Không có vai trò nào bị quá tải với các 'R'", "Tất cả những người tham gia đã đồng ý với vai trò được gán của họ").
       - Mô tả quy trình rà soát và phê duyệt (ví dụ: bản nháp được gửi cho trưởng dự án và các trưởng nhóm để xem xét, bản cuối cùng được người bảo trợ dự án (project sponsor) phê duyệt).

    **6. Các Giả định và Phụ thuộc (Assumptions and Dependencies):**
       - Liệt kê các giả định (ví dụ: "Các trưởng nhóm sẽ cung cấp danh sách đầy đủ các tác vụ chính", "Các thành viên tham gia hội thảo sẽ đại diện chính xác cho chức năng của họ").
       - Xác định các phụ thuộc (ví dụ: "Việc xây dựng ma trận phụ thuộc vào việc hoàn thành bản kế hoạch dự án chi tiết").

    **7. Vai trò và Trách nhiệm (trong việc xây dựng Ma trận):**
       - Xác định rõ trách nhiệm của các bên trong việc *tạo ra* chính ma trận RACI này.
       - Ví dụ: Người điều phối (Facilitator), Người cung cấp thông tin (từ các nhóm chuyên môn), Người phê duyệt cuối cùng.

    **8. Nguồn lực và Công cụ (Resources and Tools):**
       - Nêu rõ các nguồn lực cần thiết (ví dụ: thời gian của các bên liên quan để tham dự các buổi làm việc).
       - Xác định công cụ sẽ được sử dụng để tạo và lưu trữ ma trận (ví dụ: Microsoft Excel, Google Sheets, Confluence).

    **9. Quy trình Cập nhật và Bảo trì (Update and Maintenance Process):**
       - Mô tả quy trình xử lý khi có sự thay đổi về phạm vi dự án hoặc nhân sự.
       - Định nghĩa tần suất rà soát ma trận để đảm bảo tính phù hợp (ví dụ: "Rà soát lại vào đầu mỗi giai đoạn của dự án").
       - Chỉ định người hoặc vai trò chịu trách nhiệm duy trì và cập nhật ma trận.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của đại diện có thẩm quyền (ví dụ: Người bảo trợ dự án, Trưởng phòng) để chính thức hóa việc áp dụng ma trận.
    """,
    expected_output="""Một tài liệu "Đặc tả Ma trận Phân công Vai trò và Trách nhiệm" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu này phải được viết với ngôn ngữ rõ ràng, chính xác, tạo ra một kế hoạch không thể diễn giải sai cho việc xây dựng và duy trì ma trận RACI.
    Kết quả phải là một tài liệu tham chiếu duy nhất cho tất cả các bên liên quan về cách ma trận sẽ được tạo ra và quản lý.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "raci_matrix_specification", "1_org_chart", "raci_matrix_specification.md")
    )

    approvals_matrix = Task(
        description=f"""Soạn thảo một tài liệu "Đặc tả Ma trận Phê duyệt" (Approvals Matrix Specification).
    Tài liệu này là bản thiết kế chi tiết để xây dựng một ma trận quy định rõ ràng ai có thẩm quyền phê duyệt
    cho các loại yêu cầu và giao dịch khác nhau, thường dựa trên các ngưỡng giá trị hoặc mức độ rủi ro.
    Mục tiêu là tạo ra một khung kiểm soát nội bộ vững chắc, minh bạch, giúp tăng tốc độ ra quyết định,
    đảm bảo tuân thủ chính sách và ngăn chặn các giao dịch không được phép.

    Tài liệu đặc tả này cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu lý do cần xây dựng ma trận phê duyệt (ví dụ: yêu cầu từ bộ phận kiểm toán, sự thiếu nhất quán trong việc phê duyệt chi tiêu, quy trình hiện tại quá chậm).
       - Mô tả các vấn đề kinh doanh cần giải quyết (ví dụ: rủi ro tài chính do thiếu kiểm soát, sự chậm trễ trong hoạt động mua sắm, nhân viên không rõ giới hạn thẩm quyền của mình).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: chuẩn hóa quy trình phê duyệt trên toàn công ty, thiết lập một chuỗi phê duyệt rõ ràng, tạo ra một bản ghi có thể kiểm toán được cho tất cả các quyết định quan trọng).

    **2. Phạm vi Áp dụng (Scope of Application):**
       - Đây là phần xác định các loại giao dịch và phòng ban mà ma trận sẽ chi phối.
       - **Các Loại Phê duyệt trong Phạm vi (In-Scope Approval Types):** Liệt kê rõ tất cả các loại yêu cầu cần phê duyệt sẽ được đưa vào ma trận (ví dụ: Yêu cầu mua hàng (PR), Đơn đặt hàng (PO), Báo cáo chi phí công tác, Yêu cầu tuyển dụng, Yêu cầu thay đổi dự án, Hợp đồng nhà cung cấp).
       - **Các Đơn vị trong Phạm vi (In-Scope Departments):** Nêu rõ các phòng ban hoặc đơn vị kinh doanh sẽ phải tuân theo ma trận này.
       - **Ngoài Phạm vi (Out-of-Scope):** Liệt kê những gì sẽ KHÔNG được ma trận này điều chỉnh (ví dụ: các quyết định vận hành không liên quan đến tài chính, phê duyệt nghỉ phép).

    **3. Các Thành phần và Cấu trúc của Ma trận (Matrix Components and Structure):**
       - Mô tả chi tiết các cột và hàng của ma trận.
       - **Loại Giao dịch (Transaction Type):** Hạng mục của yêu cầu (ví dụ: "Chi tiêu Vốn", "Chi phí Vận hành").
       - **Ngưỡng Giá trị (Value Thresholds):** Các mức giá trị bằng tiền tệ (ví dụ: "< $1,000", "$1,001 - $10,000", "> $10,000").
       - **Cấp Phê duyệt (Approval Levels):** Xác định các cấp phê duyệt cần thiết (ví dụ: Cấp 1, Cấp 2).
       - **Vai trò Phê duyệt (Approver Role):** Chức danh của người có thẩm quyền phê duyệt ở mỗi cấp (ví dụ: "Quản lý trực tiếp", "Trưởng phòng", "Giám đốc Tài chính (CFO)").
       - **Các Điều kiện hoặc Ghi chú (Conditions or Notes):** Các quy tắc hoặc thông tin bổ sung (ví dụ: "Yêu cầu phải có 2 báo giá đính kèm").

    **4. Lịch trình Xây dựng và Các Cột mốc (Development Schedule and Milestones):**
       - Trình bày kế hoạch chi tiết để thu thập thông tin, thiết kế và triển khai ma trận.
       - Xác định các cột mốc quan trọng:
         - "Hoàn thành thu thập các ngưỡng phê duyệt hiện tại từ các phòng ban - [Ngày]"
         - "Tổ chức phiên làm việc với Tài chính và Lãnh đạo để thống nhất cấu trúc - [Ngày]"
         - "Hoàn thành bản nháp Ma trận Phê duyệt - [Ngày]"
         - "Ma trận được phê duyệt và sẵn sàng ban hành - [Ngày]"

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định ma trận là hoàn chỉnh (ví dụ: "Không có sự chồng chéo hoặc khoảng trống về thẩm quyền", "Tất cả các loại giao dịch phổ biến đều được bao quát", "Phù hợp với Sơ đồ Tổ chức hiện tại").
       - Mô tả quy trình rà soát và phê duyệt chính ma trận này (ví dụ: bản nháp được rà soát bởi phòng Tài chính và Pháp chế, bản cuối cùng được phê duyệt bởi Giám đốc Điều hành (CEO) và Giám đốc Tài chính (CFO)).

    **6. Các Giả định và Ràng buộc (Assumptions and Constraints):**
       - Liệt kê các giả định (ví dụ: "Các chức danh trong Sơ đồ Tổ chức là chính xác và cập nhật", "Ngưỡng ngân sách của các phòng ban đã được phê duyệt").
       - Nêu các ràng buộc (ví dụ: "Ma trận phải tuân thủ các quy định của pháp luật về quản trị doanh nghiệp", "Phải có khả năng tích hợp vào hệ thống ERP hiện tại").

    **7. Vai trò và Trách nhiệm (trong việc xây dựng Ma trận):**
       - Xác định rõ trách nhiệm của các bên trong việc *tạo ra* ma trận phê duyệt.
       - Ví dụ: Người chủ trì (thường từ phòng Tài chính hoặc Kiểm soát Nội bộ), Người cung cấp thông tin (Trưởng các phòng ban), Người phê duyệt cuối cùng của ma trận (Ban Lãnh đạo).

    **8. Công cụ và Hệ thống Tích hợp (Tools and System Integration):**
       - Xác định công cụ sẽ được sử dụng để tạo và lưu hành ma trận (ví dụ: SharePoint, Confluence, Excel).
       - Mô tả kế hoạch tích hợp ma trận vào các hệ thống công việc hàng ngày (ví dụ: cấu hình luồng phê duyệt tự động trong phần mềm kế toán hoặc hệ thống mua hàng).

    **9. Quy trình Cập nhật, Bảo trì và Truyền thông (Update, Maintenance, and Communication Plan):**
       - Mô tả quy trình chính thức để yêu cầu thay đổi ma trận khi có sự thay đổi về cơ cấu tổ chức hoặc chính sách.
       - Định nghĩa tần suất rà soát định kỳ (ví dụ: "Rà soát hàng năm cùng với chu kỳ lập ngân sách").
       - Lập kế hoạch truyền thông để đảm bảo toàn bộ nhân viên liên quan hiểu và tuân thủ ma trận mới.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền cao nhất (ví dụ: Giám đốc Điều hành, Giám đốc Tài chính) để ban hành chính sách này trên toàn công ty.
    """,
    expected_output="""Một tài liệu "Đặc tả Ma trận Phê duyệt" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu này phải được viết với ngôn ngữ rõ ràng, chính xác, tạo ra một kế hoạch không thể diễn giải sai cho việc xây dựng và thực thi các quy tắc phê duyệt.
    Kết quả phải là một tài liệu tham chiếu mang tính chính sách, làm cơ sở cho việc kiểm soát nội bộ và quản trị rủi ro.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "approvals_matrix_specification", "1_org_chart", "approvals_matrix_specification.md")
    )
    return [org_chart, roles_responsibilities_matrix, approvals_matrix]


def create_pmo_tasks(planning_agent):
    """Tạo các nhiệm vụ liên quan đến quản trị dự án (PMO) và tuân thủ."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    pmo_checklist = Task(
        description=f"""Xây dựng một "Danh mục Kiểm tra của PMO cho Giai đoạn Khởi tạo" (PMO Initiation Phase-Gate Checklist).
    Đây là một công cụ quản trị chính thức, được PMO sử dụng để tiến hành một buổi rà soát (gate review)
    nhằm xác nhận rằng dự án đã hoàn thành tất cả các yêu cầu cần thiết của giai đoạn Khởi tạo
    và đủ điều kiện để được phê duyệt chuyển sang giai đoạn Lập kế hoạch.

    Danh mục này đảm bảo dự án tuân thủ các tiêu chuẩn, quy trình của tổ chức và có nền tảng vững chắc.

    **1. Thông tin Chung về Buổi Rà soát (Review Session Details):**
       - Tên dự án:
       - Quản lý Dự án:
       - Nhà tài trợ Dự án:
       - Ngày Rà soát:
       - Người Rà soát (PMO):

    **2. Nhóm A: Sự Phù hợp Chiến lược & Luận điểm Kinh doanh (Strategic Alignment & Business Case)**
       - [ ] Luận điểm kinh doanh (Business Case) đã được trình bày và được coi là hợp lý.
       - [ ] "Phân tích Chi phí - Lợi ích" (Cost-Benefit Analysis) hoàn chỉnh và chứng minh được giá trị đầu tư.
       - [ ] Các mục tiêu dự án được xác định rõ ràng và phù hợp với mục tiêu chiến lược của tổ chức.

    **3. Nhóm B: Quản trị & Phê duyệt (Governance & Authorization)**
       - [ ] "Hiến chương Dự án" (Project Charter) đã hoàn thành, được ký duyệt và ban hành chính thức.
       - [ ] Nhà tài trợ dự án đã được xác nhận và cam kết với vai trò của mình.
       - [ ] Quản lý Dự án đã được bổ nhiệm và quyền hạn được xác định rõ ràng.

    **4. Nhóm C: Xác định Phạm vi & Kế hoạch Cấp cao (Scope Definition & High-Level Planning)**
       - [ ] Phạm vi cấp cao (In/Out Scope) được định nghĩa rõ ràng, không có sự mơ hồ lớn.
       - [ ] "Lịch trình Sơ bộ" (Preliminary Schedule) với các cột mốc chính đã được thiết lập và có tính khả thi.
       - [ ] "Ước tính Ngân sách" (Budget Estimate) đã được xây dựng dựa trên các cơ sở và giả định rõ ràng.
       - [ ] Các sản phẩm bàn giao chính (Key Deliverables) đã được liệt kê.

    **5. Nhóm D: Rủi ro & Các Bên liên quan (Risks & Stakeholders)**
       - [ ] Đánh giá rủi ro ban đầu đã được thực hiện và các rủi ro hàng đầu đã được xác định.
       - [ ] Các bên liên quan chính đã được nhận diện và phân tích (Stakeholder Register).
       - [ ] Kế hoạch tương tác với các bên liên quan cấp cao đã được phác thảo.

    **6. Nhóm E: Tuân thủ & Sẵn sàng (Compliance & Readiness)**
       - [ ] Dự án tuân thủ các chính sách nội bộ quan trọng (ví dụ: an ninh thông tin, pháp lý, mua sắm).
       - [ ] Đội ngũ dự án đã được thông báo và sẵn sàng cho buổi họp Khởi động (Kick-off).
       - [ ] Các tài liệu chính của giai đoạn Khởi tạo đã được lưu trữ tại kho lưu trữ chung của dự án.

    **7. Quyết định của PMO (PMO Gate Decision):**
       - Phần này dành cho PMO đưa ra quyết định cuối cùng sau buổi rà soát.
       - **Trạng thái:**
         - [ ] **Phê duyệt (Go):** Dự án được phép chuyển sang giai đoạn tiếp theo.
         - [ ] **Phê duyệt có Điều kiện (Go with Conditions):** Dự án được phép đi tiếp nhưng phải hoàn thành một số hành động khắc phục.
         - [ ] **Tạm dừng (Hold):** Cần thêm thông tin hoặc giải quyết các vấn đề lớn trước khi rà soát lại.
         - [ ] **Hủy bỏ (No-Go):** Dự án không được tiếp tục.
       - **Các Điều kiện / Ghi chú:** (Liệt kê các hành động cần thiết nếu là "Phê duyệt có Điều kiện").
       - **Chữ ký của Người đại diện PMO:**
    """,
    expected_output="""Một "Danh mục Kiểm tra của PMO" chuyên nghiệp và chính thức dưới dạng Markdown.
    Tài liệu phải được trình bày như một biểu mẫu rà soát (review form) mà PMO có thể sử dụng trực tiếp.
    Nó phải bao gồm các hạng mục kiểm tra tuân thủ, thông tin về buổi rà soát, và một phần quyết định rõ ràng (Go/No-Go).
    Kết quả phải là một công cụ quản trị hiệu quả để đảm bảo chất lượng và giảm thiểu rủi ro cho danh mục dự án của tổ chức.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "pmo_checklist", "1_pmo", "pmo_checklist.md")
    )

    cobit_checklist = Task(
        description=f"""Xây dựng một "Danh mục Kiểm tra Tuân thủ COBIT cho Giai đoạn Khởi tạo/Lập kế hoạch".
    Đây là một công cụ quản trị CNTT (IT Governance) được sử dụng để đánh giá sự phù hợp của dự án
    với các mục tiêu kiểm soát và quy trình quản trị CNTT của tổ chức, dựa trên khuôn khổ COBIT.
    Mục đích là đảm bảo dự án không chỉ thành công về mặt quản lý mà còn mang lại giá trị,
    tối ưu hóa rủi ro và nguồn lực từ góc độ CNTT doanh nghiệp.

    Danh mục này sẽ được sử dụng bởi bộ phận Quản trị CNTT, Kiến trúc sư Doanh nghiệp, hoặc PMO chuyên trách về quản trị.

    **1. Thông tin Chung về Buổi Rà soát (Review Session Details):**
       - Tên dự án:
       - Quản lý Dự án:
       - Người Rà soát (IT Governance/Architecture Team):
       - Ngày Rà soát:

    **2. Nhóm A: Đảm bảo Sự phù hợp và Giá trị (Ensure Alignment & Value Delivery - Dựa trên các domain EDM, APO của COBIT)**
       - [ ] Luận điểm kinh doanh (Business Case) có xác định rõ ràng các lợi ích và giá trị liên quan đến CNTT không?
       - [ ] Dự án có phù hợp với Chiến lược CNTT và Lộ trình Kiến trúc Doanh nghiệp (Enterprise Architecture) không?
       - [ ] Các bên liên quan về CNTT (ví dụ: Vận hành, An ninh, Kiến trúc) đã được xác định và tham gia vào giai đoạn đầu chưa?
       - [ ] Các chỉ số đo lường thành công (KPIs) có bao gồm các chỉ số về hiệu suất và giá trị CNTT (ví dụ: mức độ sẵn sàng, thời gian phản hồi) không?

    **3. Nhóm B: Tối ưu hóa Rủi ro (Optimize Risk - Dựa trên domain EDM, APO)**
       - [ ] Các rủi ro đặc thù về CNTT (ví dụ: an ninh mạng, tích hợp hệ thống, quyền riêng tư dữ liệu, lỗi thời công nghệ) đã được nhận diện và đánh giá chưa?
       - [ ] Dự án có tuân thủ các chính sách An ninh Thông tin của tổ chức không?
       - [ ] Các yêu cầu về sao lưu, phục hồi sau thảm họa (Backup & Disaster Recovery) đã được xem xét sơ bộ chưa?
       - [ ] Dự án có tuân thủ các quy định pháp lý liên quan đến CNTT (ví dụ: Luật An ninh mạng, Nghị định bảo vệ dữ liệu cá nhân) không?

    **4. Nhóm C: Tối ưu hóa Nguồn lực (Optimize Resources - Dựa trên domain APO, BAI)**
       - [ ] Kế hoạch nguồn lực có xem xét đầy đủ năng lực và tài nguyên CNTT hiện có (con người, hạ tầng, ứng dụng) không?
       - [ ] Yêu cầu về hạ tầng CNTT mới (máy chủ, mạng, lưu trữ) đã được xác định và ước tính sơ bộ chưa?
       - [ ] Nhu cầu về mua sắm giấy phép phần mềm và dịch vụ bên thứ ba đã được làm rõ chưa?
       - [ ] Kế hoạch dự án có bao gồm các hoạt động chuyển giao kiến thức và bàn giao cho đội ngũ vận hành CNTT (IT Operations) không?

    **5. Nhóm D: Đảm bảo Tính minh bạch và Quản lý Nhà cung cấp (Ensure Transparency & Manage Vendors - Dựa trên domain APO)**
       - [ ] Các tiêu chí lựa chọn nhà cung cấp CNTT (nếu có) có rõ ràng và tuân thủ chính sách mua sắm không?
       - [ ] Các thỏa thuận mức độ dịch vụ (SLA) với các bên liên quan và nhà cung cấp đã được phác thảo chưa?
       - [ ] Kế hoạch truyền thông có bao gồm việc báo cáo cho các cấp quản lý CNTT không?

    **6. Quyết định của Ban Quản trị CNTT (IT Governance Decision):**
       - Phần này dành cho người có thẩm quyền về quản trị CNTT đưa ra quyết định.
       - **Trạng thái:**
         - [ ] **Phê duyệt (Compliant):** Dự án tuân thủ các yêu cầu quản trị CNTT và được phép tiếp tục.
         - [ ] **Phê duyệt có Điều kiện (Compliant with Conditions):** Dự án được đi tiếp nhưng phải giải quyết các điểm chưa tuân thủ.
         - [ ] **Yêu cầu làm rõ (More Information Required):** Cần bổ sung thông tin trước khi đánh giá lại.
         - [ ] **Không Tuân thủ (Non-Compliant):** Dự án cần được thiết kế lại để đáp ứng các yêu cầu quản trị.
       - **Các Hành động Yêu cầu / Ghi chú:**
       - **Chữ ký của Người đại diện Quản trị CNTT:**
    """,
    expected_output="""Một "Danh mục Kiểm tra Tuân thủ COBIT" chuyên nghiệp và chính thức dưới dạng Markdown.
    Tài liệu phải phản ánh góc nhìn quản trị CNTT, tập trung vào giá trị, rủi ro, nguồn lực và sự tuân thủ theo các nguyên tắc của COBIT.
    Nó phải là một công cụ đánh giá (assessment tool) hiệu quả cho các bộ phận quản trị, giúp đảm bảo các dự án CNTT được triển khai một cách có kiểm soát và phù hợp với chiến lược chung.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "cobit_checklist", "1_pmo", "cobit_checklist.md")
    )
    return [pmo_checklist, cobit_checklist]


def create_procurement_tasks(planning_agent):
    """Tạo nhiệm vụ xây dựng kế hoạch quản lý mua sắm."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    procurement_plan = Task(
        description=f"""Soạn thảo một "Kế hoạch Quản lý Mua sắm" (Procurement Management Plan) toàn diện, chính thức và chi tiết.
    Tài liệu này là một thành phần của Kế hoạch Quản lý Dự án tổng thể, mô tả cách thức nhóm dự án sẽ mua sắm hoặc
    thuê ngoài các hàng hóa và dịch vụ cần thiết từ bên ngoài tổ chức.
    Mục tiêu là tạo ra một quy trình có cấu trúc và nhất quán để quản lý toàn bộ vòng đời mua sắm,
    từ việc quyết định mua gì cho đến khi kết thúc hợp đồng, nhằm đảm bảo giá trị tốt nhất và giảm thiểu rủi ro.

    Kế hoạch Quản lý Mua sắm cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu các nhu cầu của dự án đòi hỏi phải có sự tham gia của các nhà cung cấp bên ngoài.
       - Mô tả vấn đề cần giải quyết (ví dụ: thiếu quy trình chuẩn để lựa chọn nhà thầu, rủi ro pháp lý từ các hợp đồng không chặt chẽ, chi phí vượt dự toán do quản lý nhà cung cấp kém).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: đảm bảo quy trình lựa chọn nhà thầu công bằng và minh bạch, xác định các loại hợp đồng phù hợp để quản lý rủi ro, tích hợp lịch trình của nhà cung cấp vào lịch trình tổng thể của dự án).

    **2. Quyết định Mua hay Tự làm (Make-or-Buy Decisions):**
       - Đây là phần cốt lõi, ghi lại kết quả của các phân tích "Mua hay Tự làm".
       - **Danh sách Hạng mục Mua sắm (Items to Procure):** Liệt kê một cách rõ ràng tất cả các hàng hóa, dịch vụ hoặc kết quả sẽ được mua sắm. Mỗi hạng mục cần có một lý do biện minh.
       - **Danh sách Hạng mục Tự làm (Items to Make):** Liệt kê các công việc mà dự án đã quyết định sẽ tự thực hiện trong nội bộ để tránh nhầm lẫn.

    **3. Các Loại Hợp đồng và Tài liệu Mua sắm (Contract Types and Procurement Documents):**
       - **Loại Hợp đồng (Contract Types):** Xác định loại hợp đồng sẽ được sử dụng cho mỗi hạng mục mua sắm, dựa trên mức độ rõ ràng của phạm vi công việc. Ví dụ:
         - Hợp đồng Giá Cố định (Fixed-Price): Khi phạm vi được định nghĩa rõ.
         - Hợp đồng Hoàn trả Chi phí (Cost-Reimbursable): Khi phạm vi không chắc chắn.
         - Hợp đồng theo Thời gian và Nguyên vật liệu (Time & Materials - T&M): Thường dùng cho việc tăng cường nhân sự.
       - **Tài liệu Mua sắm (Procurement Documents):** Xác định loại tài liệu sẽ được sử dụng để mời thầu (ví dụ: Yêu cầu Thông tin - RFI, Yêu cầu Báo giá - RFQ, Yêu cầu Đề xuất - RFP).

    **4. Lịch trình và Các Cột mốc Mua sắm (Procurement Schedule and Milestones):**
       - Tích hợp các hoạt động mua sắm vào lịch trình tổng thể của dự án.
       - Xác định các cột mốc quan trọng cho từng gói mua sắm, ví dụ:
         - "Hoàn thành Bảng Mô tả Công việc (SoW) cho gói thầu - [Ngày]"
         - "Phát hành Yêu cầu Đề xuất (RFP) - [Ngày]"
         - "Nhận hồ sơ dự thầu từ nhà cung cấp - [Ngày]"
         - "Hoàn thành lựa chọn nhà cung cấp - [Ngày]"
         - "Ký kết hợp đồng - [Ngày]"
         - "Ngày giao hàng/hoàn thành dịch vụ - [Ngày]"

    **5. Tiêu chí Lựa chọn Nhà cung cấp (Seller Selection Criteria):**
       - Định nghĩa các tiêu chí khách quan sẽ được sử dụng để đánh giá và lựa chọn nhà cung cấp.
       - Ví dụ: Năng lực kỹ thuật, kinh nghiệm và hiệu suất trong quá khứ, năng lực tài chính, chi phí, sự hiểu biết về yêu cầu.
       - Có thể bao gồm một hệ thống tính điểm có trọng số để đảm bảo tính công bằng.

    **6. Các Giả định và Ràng buộc (Assumptions and Constraints):**
       - Liệt kê các giả định liên quan đến mua sắm (ví dụ: "Có sẵn một danh sách các nhà cung cấp đã được phê duyệt", "Thị trường có đủ các nhà cung cấp đủ năng lực").
       - Nêu các ràng buộc (ví dụ: "Phải tuân thủ chính sách mua hàng của công ty", "Ngân sách cho gói thầu X không được vượt quá Y", "Nhà cung cấp phải có chứng chỉ Z").

    **7. Vai trò và Trách nhiệm Quản lý Mua sắm (Procurement Roles and Responsibilities):**
       - Xác định rõ vai trò của các bên trong quy trình mua sắm.
       - **Quản lý Dự án:** Chịu trách nhiệm tổng thể, đảm bảo nhu cầu mua sắm phù hợp với dự án.
       - **Chuyên viên/Phòng Mua sắm:** Dẫn dắt quá trình mời thầu, đàm phán và soạn thảo hợp đồng.
       - **Nhóm Kỹ thuật:** Cung cấp yêu cầu kỹ thuật, viết SoW và tham gia đánh giá đề xuất kỹ thuật.
       - **Phòng Pháp chế:** Rà soát và phê duyệt các điều khoản hợp đồng.

    **8. Quản lý Hợp đồng và Hiệu suất (Contract and Performance Administration):**
       - Mô tả cách thức các hợp đồng sẽ được quản lý sau khi ký kết.
       - Bao gồm quy trình theo dõi hiệu suất của nhà cung cấp, kiểm tra chất lượng sản phẩm/dịch vụ, xử lý các thay đổi đối với hợp đồng, quy trình thanh toán và giải quyết tranh chấp.

    **9. Quản lý Rủi ro trong Mua sắm (Procurement Risk Management):**
       - Xác định các rủi ro tiềm ẩn liên quan đến quá trình mua sắm (ví dụ: nhà cung cấp không giao hàng đúng hẹn, chất lượng kém, chi phí tăng đột biến) và các chiến lược giảm thiểu tương ứng.
       - Có thể yêu cầu các nhà cung cấp cung cấp bảo lãnh thực hiện hợp đồng hoặc các hình thức bảo hiểm khác.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền (ví dụ: Quản lý Dự án, Trưởng phòng Mua sắm, Nhà tài trợ Dự án) để chính thức phê duyệt Kế hoạch Quản lý Mua sắm.
    """,
    expected_output="""Một tài liệu "Kế hoạch Quản lý Mua sắm" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu này phải cung cấp một lộ trình rõ ràng và có kiểm soát cho tất cả các hoạt động mua sắm của dự án.
    Kết quả phải là một tài liệu tham chiếu chiến lược, đảm bảo rằng việc mua sắm được tiến hành một cách công bằng,
    minh bạch và phù hợp với các mục tiêu chung của dự án.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "procurement_plan", "1_procurement", "procurement_plan.md")
    )
    return [procurement_plan]


def create_sow_tasks(planning_agent):
    """Tạo nhiệm vụ xây dựng Bảng Mô tả Công việc (SoW)."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    statement_of_work = Task(
        description=f"""Soạn thảo một "Bảng Mô tả Công việc" (Statement of Work - SoW) chính thức và chi tiết.
    Tài liệu này là một thỏa thuận ràng buộc, thường được sử dụng giữa khách hàng và nhà cung cấp (hoặc giữa các phòng ban),
    để định nghĩa chính xác phạm vi công việc, sản phẩm bàn giao, lịch trình, và chi phí.
    Mục tiêu là tạo ra một văn bản rõ ràng, không mơ hồ để làm cơ sở cho việc thực hiện và nghiệm thu công việc.

    Bảng Mô tả Công việc cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu ngắn gọn về dự án.
       - Mô tả vấn đề kinh doanh hoặc cơ hội mà công việc này sẽ giải quyết.
       - Nêu rõ các mục tiêu cụ thể mà SoW này hướng tới.

    **2. Phạm vi Công việc Chi tiết (Detailed Scope of Work):**
       - Đây là phần quan trọng nhất, mô tả chi tiết công việc sẽ được thực hiện.
       - **Các Tác vụ trong Phạm vi (In-Scope Tasks):** Liệt kê một cách tường minh tất cả các hoạt động, công việc mà nhà cung cấp sẽ thực hiện.
       - **Các Tác vụ ngoài Phạm vi (Out-of-Scope Tasks):** Liệt kê rõ những gì sẽ KHÔNG được thực hiện để tránh hiểu lầm và "scope creep".

    **3. Các Sản phẩm Bàn giao (Deliverables):**
       - Liệt kê tất cả các sản phẩm hữu hình hoặc vô hình sẽ được bàn giao cho khách hàng.
       - Ví dụ: Báo cáo phân tích, tài liệu thiết kế, mã nguồn phần mềm, tài liệu hướng dẫn sử dụng.

    **4. Lịch trình và Các Cột mốc (Schedule and Milestones):**
       - Trình bày một lịch trình chi tiết cho việc bàn giao các sản phẩm.
       - Xác định các cột mốc quan trọng (milestones) với ngày hoàn thành cụ thể.
       - Ví dụ: "Bàn giao Thiết kế UI/UX - 31/10/2023", "Hoàn thành Giai đoạn 1 - 15/12/2023".

    **5. Tiêu chí Chấp nhận và Quy trình Phê duyệt (Acceptance Criteria and Approval Process):**
       - Đối với mỗi sản phẩm bàn giao, định nghĩa các tiêu chí khách quan để xác định rằng nó đã hoàn thành và đạt yêu cầu.
       - Mô tả quy trình khách hàng sẽ rà soát và phê duyệt sản phẩm bàn giao (ví dụ: thời gian phản hồi, người phê duyệt).

    **6. Các Giả định, Ràng buộc, và Phụ thuộc (Assumptions, Constraints, and Dependencies):**
       - Liệt kê các giả định mà SoW này dựa trên.
       - Nêu các ràng buộc (ví dụ: ngân sách, công nghệ, nhân sự).
       - Xác định các phụ thuộc từ phía khách hàng (ví dụ: cung cấp dữ liệu, truy cập hệ thống).

    **7. Vai trò và Trách nhiệm (Roles and Responsibilities):**
       - Xác định rõ trách nhiệm của cả bên nhà cung cấp và bên khách hàng để đảm bảo sự hợp tác thành công.

    **8. Chi phí và Lịch trình Thanh toán (Pricing and Payment Schedule):**
       - Nêu rõ tổng chi phí của công việc.
       - Chi tiết hóa lịch trình thanh toán, thường gắn liền với việc hoàn thành các cột mốc (ví dụ: 30% khi ký SoW, 40% khi hoàn thành Giai đoạn 1, 30% khi nghiệm thu cuối cùng).

    **9. Quản lý Thay đổi và Báo cáo (Change Management and Reporting):**
       - Mô tả quy trình xử lý khi có yêu cầu thay đổi phạm vi công việc (Change Request Process).
       - Định nghĩa tần suất và định dạng của các báo cáo tiến độ.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của đại diện có thẩm quyền từ cả bên khách hàng và bên nhà cung cấp để chính thức hóa thỏa thuận.
    """,
    expected_output="""Một "Bảng Mô tả Công việc" (SoW) hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu phải được viết với ngôn ngữ rõ ràng, chính xác, có tính pháp lý, nhằm mục đích tạo ra một thỏa thuận không thể diễn giải sai.
    Kết quả phải là một tài liệu tham chiếu duy nhất cho tất cả các bên liên quan về những gì đã được thỏa thuận.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "statement_of_work", "1_sow", "statement_of_work.md")
    )
    return [statement_of_work]


def create_riskplan_tasks(planning_agent):
    """Tạo các nhiệm vụ liên quan đến kế hoạch quản lý rủi ro chi tiết."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    risk_information_form = Task(
        description=f"""Soạn thảo một tài liệu "Đặc tả Biểu mẫu Thông tin Rủi ro" (Risk Information Form Specification).
    Tài liệu này là một bản thiết kế chi tiết để xây dựng một biểu mẫu (form/template) chuẩn hóa,
    được sử dụng để ghi lại tất cả các thông tin cần thiết về một rủi ro cụ thể (mối đe dọa hoặc cơ hội) ngay khi nó được nhận diện.
    Mục tiêu là tạo ra một công cụ thu thập dữ liệu nhất quán, đảm bảo không bỏ sót thông tin quan trọng,
    và cung cấp đầu vào có cấu trúc cho Sổ đăng ký Rủi ro (Risk Register).

    Tài liệu đặc tả này cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu rằng biểu mẫu này là một công cụ thiết yếu trong quy trình Quản lý Rủi ro của dự án.
       - Mô tả vấn đề cần giải quyết (ví dụ: rủi ro được báo cáo một cách không nhất quán, thiếu thông tin để phân tích, khó tổng hợp và theo dõi).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: chuẩn hóa việc thu thập thông tin rủi ro, đảm bảo mọi rủi ro được ghi lại với đầy đủ các thuộc tính cần thiết, tạo điều kiện cho việc phân tích và ưu tiên hóa một cách hiệu quả).

    **2. Cấu trúc và Các Trường Dữ liệu của Biểu mẫu (Form Structure and Data Fields):**
       - Đây là phần quan trọng nhất, định nghĩa chi tiết tất cả các trường sẽ có trên biểu mẫu.
       - **Phần 1: Nhận dạng Rủi ro (Risk Identification)**
         - Mã Rủi ro (Risk ID - có thể được gán tự động)
         - Tên Rủi ro (Risk Title - tóm tắt ngắn gọn)
         - Người nhận diện (Identified By)
         - Ngày nhận diện (Date Identified)
       - **Phần 2: Mô tả Rủi ro (Risk Description)**
         - Mô tả Chi tiết (Detailed Description - theo cấu trúc Nguyên nhân -> Rủi ro -> Ảnh hưởng)
         - Hạng mục Rủi ro (Risk Category - ví dụ: Kỹ thuật, Lịch trình, Chi phí, Nguồn lực)
       - **Phần 3: Phân tích Rủi ro (Risk Analysis)**
         - Xác suất (Probability - ví dụ: thang điểm 1-5 hoặc Thấp/Trung bình/Cao)
         - Mức độ Ảnh hưởng (Impact - trên các mặt: Chi phí, Lịch trình, Phạm vi, Chất lượng; cũng theo thang điểm)
         - Điểm số Rủi ro (Risk Score - thường là Xác suất x Ảnh hưởng)
         - Các Yếu tố Kích hoạt (Triggers - các dấu hiệu cho thấy rủi ro sắp xảy ra)
       - **Phần 4: Kế hoạch Ứng phó (Response Planning)**
         - Chiến lược Ứng phó (Response Strategy - ví dụ: Né tránh, Giảm thiểu, Chuyển giao, Chấp nhận)
         - Các Hành động Ứng phó (Response Actions - các bước cụ thể cần làm)
         - Người chịu trách nhiệm (Risk Owner - người theo dõi và thực hiện kế hoạch ứng phó)
         - Hạn chót Thực hiện (Due Date)
       - **Phần 5: Theo dõi và Kiểm soát (Monitoring and Control)**
         - Trạng thái (Status - ví dụ: Mới, Đang xử lý, Đã đóng, Không còn phù hợp)
         - Ghi chú/Cập nhật (Notes/Updates)

    **3. Sản phẩm Bàn giao (Deliverable):**
       - Sản phẩm bàn giao chính là một file biểu mẫu (template) có thể sử dụng ngay.
       - Định dạng bàn giao: File Microsoft Word/Excel, file PDF có thể điền thông tin (fillable PDF), hoặc một biểu mẫu được tạo trên SharePoint/Jira/Confluence.
       - Có thể kèm theo một tài liệu hướng dẫn ngắn gọn cách điền biểu mẫu.

    **4. Lịch trình Thiết kế Biểu mẫu (Form Design Schedule):**
       - Trình bày kế hoạch chi tiết để thiết kế, lấy ý kiến và hoàn thiện biểu mẫu.
       - Xác định các cột mốc quan trọng:
         - "Hoàn thành bản nháp các trường dữ liệu của biểu mẫu - [Ngày]"
         - "Tổ chức lấy ý kiến từ các Quản lý Dự án và Trưởng nhóm - [Ngày]"
         - "Hoàn thiện thiết kế và chức năng của biểu mẫu - [Ngày]"
         - "Biểu mẫu được phê duyệt và sẵn sàng để ban hành - [Ngày]"

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định biểu mẫu đã hoàn chỉnh (ví dụ: "Bao gồm tất cả các trường dữ liệu bắt buộc theo Kế hoạch Quản lý Rủi ro", "Dễ hiểu và dễ sử dụng", "Tương thích với công cụ Sổ đăng ký Rủi ro").
       - Mô tả quy trình phê duyệt chính cái biểu mẫu này (ví dụ: Quản lý Dự án soạn thảo, Trưởng phòng PMO rà soát và phê duyệt để trở thành mẫu chuẩn của công ty/dự án).

    **6. Các Giả định và Phụ thuộc (Assumptions and Dependencies):**
       - Liệt kê các giả định (ví dụ: "Người dùng đã được đào tạo cơ bản về quản lý rủi ro", "Hệ thống đánh giá Xác suất và Ảnh hưởng đã được định nghĩa trong Kế hoạch Quản lý Rủi ro").
       - Xác định các phụ thuộc (ví dụ: "Thiết kế của biểu mẫu này phải phù hợp với cấu trúc của Sổ đăng ký Rủi ro", "Việc sử dụng biểu mẫu này là bắt buộc theo quy trình quản lý rủi ro").

    **7. Vai trò và Trách nhiệm (trong việc tạo và sử dụng Biểu mẫu):**
       - **Người tạo Biểu mẫu:** PMO hoặc Quản lý Dự án.
       - **Người sử dụng Biểu mẫu:** Bất kỳ thành viên nào trong nhóm dự án đều có thể nhận diện và điền thông tin rủi ro ban đầu.
       - **Người rà soát và phê duyệt thông tin:** Quản lý Dự án hoặc Người chịu trách nhiệm Rủi ro (Risk Owner).

    **8. Công cụ và Lưu trữ (Tool and Storage):**
       - Xác định công cụ chính để tạo và phân phối biểu mẫu (ví dụ: Microsoft Forms, Word).
       - Mô tả quy trình nộp và lưu trữ các biểu mẫu đã được điền (ví dụ: "Nộp qua email cho Quản lý Dự án", "Tải lên một thư mục SharePoint cụ thể").

    **9. Truyền thông và Hướng dẫn (Communication and Guidance):**
       - Lập kế hoạch truyền thông để thông báo cho toàn bộ nhóm dự án về việc ra mắt và sử dụng biểu mẫu mới.
       - Cung cấp tài liệu hướng dẫn hoặc tổ chức một buổi giới thiệu ngắn để đảm bảo mọi người hiểu cách điền thông tin một cách chính xác và nhất quán.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của đại diện có thẩm quyền (ví dụ: Trưởng phòng PMO, Nhà tài trợ Dự án) để chính thức ban hành biểu mẫu này như một công cụ chuẩn trong quy trình quản lý của dự án/tổ chức.
    """,
    expected_output="""Một tài liệu "Đặc tả Biểu mẫu Thông tin Rủi ro" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown,
    cùng với một sản phẩm bàn giao là một file biểu mẫu (template) sẵn sàng để sử dụng.
    Tài liệu đặc tả phải tạo ra một kế hoạch không thể diễn giải sai cho việc xây dựng biểu mẫu,
    và biểu mẫu kết quả phải là công cụ chuẩn hóa, giúp mọi rủi ro được ghi lại một cách đầy đủ và nhất quán.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "risk_information_form_specification", "1_riskplan", "risk_information_form_specification.md")
    )

    risk_analysis_plan = Task(
        description=f"""Soạn thảo một tài liệu "Kế hoạch Phân tích Rủi ro" (Risk Analysis Plan) chính thức và chi tiết.
    Tài liệu này thường là một phần của Kế hoạch Quản lý Rủi ro tổng thể, tập trung cụ thể vào việc
    định nghĩa phương pháp, công cụ và dữ liệu sẽ được sử dụng để đánh giá và ưu tiên hóa các rủi ro đã được nhận diện.
    Mục tiêu là thiết lập một quy trình khách quan và nhất quán để phân tích rủi ro, đảm bảo rằng
    nhóm dự án có một sự hiểu biết chung về mức độ nghiêm trọng của từng rủi ro và có thể tập trung nguồn lực vào những rủi ro quan trọng nhất.

    Kế hoạch Phân tích Rủi ro cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu rằng kế hoạch này định nghĩa quy trình phân tích cho các rủi ro được thu thập thông qua "Biểu mẫu Thông tin Rủi ro" và được ghi nhận trong "Sổ đăng ký Rủi ro".
       - Mô tả vấn đề cần giải quyết (ví dụ: sự đánh giá chủ quan và không nhất quán về rủi ro, thiếu cơ sở để so sánh và ưu tiên hóa các rủi ro khác nhau).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: định nghĩa các thang đo chuẩn cho xác suất và mức độ ảnh hưởng, thiết lập Ma trận Xác suất và Ảnh hưởng, xác định các ngưỡng rủi ro cần hành động ngay lập tức).

    **2. Phạm vi và Phương pháp Luận (Scope and Methodology):**
       - **Phạm vi (Scope):** Nêu rõ rằng kế hoạch này áp dụng cho tất cả các rủi ro đã được nhận diện trong dự án.
       - **Phương pháp Phân tích Định tính (Qualitative Analysis Methodology):** Mô tả cách thức xếp hạng rủi ro một cách tương đối.
       - **Phương pháp Phân tích Định lượng (Quantitative Analysis Methodology):** Mô tả (nếu có) cách thức phân tích rủi ro bằng các con số cụ thể (ví dụ: Phân tích Monte Carlo, Phân tích Độ nhạy). Nêu rõ khi nào phương pháp này sẽ được áp dụng (ví dụ: chỉ cho các rủi ro có điểm số cao nhất).
       - **Ngoài Phạm vi (Out-of-Scope):** Nêu rõ kế hoạch này không bao gồm việc nhận diện rủi ro ban đầu hoặc lập kế hoạch ứng phó chi tiết (đây là các quy trình trước và sau).

    **3. Các Thành phần và Công cụ Phân tích (Analysis Components and Tools):**
       - Đây là phần cốt lõi, định nghĩa các công cụ và thang đo.
       - **Thang đo Xác suất (Probability Scales):** Định nghĩa một thang đo cụ thể (ví dụ: 1-5) và mô tả ý nghĩa của từng cấp độ (ví dụ: 1 = Rất thấp <10%, 5 = Rất cao >80%).
       - **Thang đo Mức độ Ảnh hưởng (Impact Scales):** Định nghĩa các thang đo tác động đối với các mục tiêu dự án (ví dụ: Chi phí, Lịch trình, Phạm vi, Chất lượng). Mỗi mục tiêu cần có định nghĩa rõ ràng cho từng cấp độ (ví dụ: Ảnh hưởng "Cao" về Chi phí = >15% vượt ngân sách).
       - **Ma trận Xác suất và Ảnh hưởng (Probability and Impact Matrix):** Trình bày một ma trận trực quan cho thấy cách kết hợp xác suất và ảnh hưởng để tạo ra một Điểm số hoặc Mức độ Rủi ro tổng thể (ví dụ: Thấp/Vàng, Trung bình/Cam, Cao/Đỏ).
       - **Các Ngưỡng Rủi ro (Risk Thresholds):** Xác định rõ các ngưỡng. Ví dụ: "Bất kỳ rủi ro nào rơi vào vùng Đỏ đều phải được báo cáo lên Nhà tài trợ Dự án và cần có kế hoạch ứng phó chi tiết trong vòng 5 ngày làm việc".

    **4. Lịch trình và Tần suất Phân tích (Analysis Schedule and Frequency):**
       - Mô tả lịch trình cho các hoạt động phân tích rủi ro.
       - Xác định tần suất rà soát và phân tích lại Sổ đăng ký Rủi ro (ví dụ: "Các buổi họp rà soát rủi ro sẽ được tổ chức hai tuần một lần", "Một cuộc phân tích sâu sẽ được thực hiện tại mỗi cổng giai đoạn của dự án").

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định Kế hoạch Phân tích Rủi ro đã hoàn chỉnh (ví dụ: "Tất cả các thang đo đều có định nghĩa rõ ràng", "Ma trận P&I được tất cả các bên liên quan chính thống nhất").
       - Mô tả quy trình phê duyệt chính cái kế hoạch này (ví dụ: Quản lý Dự án soạn thảo, được rà soát bởi các trưởng nhóm và phê duyệt bởi Nhà tài trợ Dự án).

    **6. Các Giả định và Phụ thuộc (Assumptions and Dependencies):**
       - Liệt kê các giả định (ví dụ: "Các chuyên gia sẽ có mặt để cung cấp đánh giá khách quan", "Dữ liệu từ các dự án trước đó có sẵn để tham khảo").
       - Xác định các phụ thuộc (ví dụ: "Việc phân tích chỉ có thể thực hiện khi các rủi ro đã được nhận diện và ghi lại đầy đủ").

    **7. Vai trò và Trách nhiệm (trong Quy trình Phân tích):**
       - Xác định rõ vai trò của các bên trong việc *thực hiện* phân tích.
       - **Quản lý Dự án:** Điều phối các buổi họp phân tích, đảm bảo quy trình được tuân thủ.
       - **Người chịu trách nhiệm Rủi ro (Risk Owner):** Chịu trách nhiệm chính trong việc dẫn dắt phân tích cho rủi ro được giao.
       - **Nhóm Dự án & Chuyên gia (Team & SMEs):** Cung cấp dữ liệu và ý kiến chuyên môn để đánh giá xác suất và ảnh hưởng.

    **8. Định dạng Báo cáo và Lưu trữ (Reporting Format and Storage):**
       - Mô tả cách thức kết quả phân tích sẽ được ghi lại trong Sổ đăng ký Rủi ro.
       - Xác định định dạng của các báo cáo tóm tắt rủi ro sẽ được gửi cho ban lãnh đạo.
       - Quy định nơi lưu trữ các tài liệu phân tích (ví dụ: thư mục SharePoint của dự án).

    **9. Quản lý Thay đổi (Change Management):**
       - Mô tả quy trình để cập nhật chính Kế hoạch Phân tích Rủi ro này nếu phương pháp luận cần được điều chỉnh trong quá trình thực hiện dự án.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền (ví dụ: Quản lý Dự án, Nhà tài trợ Dự án) để chính thức phê duyệt phương pháp luận phân tích rủi ro sẽ được áp dụng cho toàn dự án.
    """,
    expected_output="""Một tài liệu "Kế hoạch Phân tích Rủi ro" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu này phải xác định một cách không mơ hồ về phương pháp luận, thang đo, và quy trình sẽ được sử dụng để đánh giá rủi ro.
    Kết quả phải là một tài liệu tham chiếu chuẩn, đảm bảo tính nhất quán và khách quan trong toàn bộ hoạt động phân tích rủi ro của dự án.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "risk_analysis_plan", "1_riskplan", "risk_analysis_plan.md")
    )

    risk_management_plan = Task(
        description=f"""Soạn thảo một "Kế hoạch Quản lý Rủi ro" (Risk Management Plan) toàn diện, chính thức và mang tính chiến lược.
    Tài liệu này là một thành phần cốt lõi của Kế hoạch Quản lý Dự án tổng thể, mô tả cách thức các hoạt động quản lý rủi ro
    sẽ được cấu trúc và thực hiện trong suốt vòng đời của dự án.
    Mục tiêu là tạo ra một khuôn khổ nhất quán để chủ động nhận diện, phân tích, lập kế hoạch ứng phó và giám sát rủi ro,
    nhằm tối đa hóa cơ hội và giảm thiểu các mối đe dọa đối với mục tiêu của dự án.

    Kế hoạch Quản lý Rủi ro cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu ngắn gọn về dự án và tầm quan trọng của việc quản lý rủi ro một cách có hệ thống.
       - Mô tả vấn đề cần giải quyết (ví dụ: các dự án trước đây thường bị động trước các vấn đề phát sinh, thiếu một quy trình chuẩn để xử lý sự không chắc chắn).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: thiết lập một quy trình quản lý rủi ro từ đầu đến cuối, xác định vai trò và trách nhiệm rõ ràng, đảm bảo các quyết định về rủi ro được đưa ra một cách sáng suốt và nhất quán).

    **2. Phương pháp Luận Quản lý Rủi ro (Risk Management Methodology):**
       - Mô tả cách tiếp cận tổng thể sẽ được sử dụng để quản lý rủi ro trong dự án này.
       - Xác định các quy trình chính sẽ được tuân thủ:
         1. Lập kế hoạch Quản lý Rủi ro (Plan Risk Management)
         2. Nhận diện Rủi ro (Identify Risks)
         3. Phân tích Rủi ro Định tính (Perform Qualitative Risk Analysis)
         4. Phân tích Rủi ro Định lượng (Perform Quantitative Risk Analysis - nếu có)
         5. Lập kế hoạch Ứng phó Rủi ro (Plan Risk Responses)
         6. Thực hiện Kế hoạch Ứng phó (Implement Risk Responses)
         7. Giám sát Rủi ro (Monitor Risks)

    **3. Vai trò và Trách nhiệm (Roles and Responsibilities):**
       - Đây là phần cốt lõi, xác định rõ ai chịu trách nhiệm cho các hoạt động quản lý rủi ro.
       - **Quản lý Dự án:** Chịu trách nhiệm tổng thể về việc thực thi Kế hoạch Quản lý Rủi ro.
       - **Người chịu trách nhiệm Rủi ro (Risk Owner):** Cá nhân chịu trách nhiệm giám sát một rủi ro cụ thể và kế hoạch ứng phó của nó.
       - **Nhóm Dự án:** Có trách nhiệm chủ động nhận diện và báo cáo rủi ro trong lĩnh vực của họ.
       - **Nhà tài trợ Dự án:** Cung cấp nguồn lực và là cấp phê duyệt cuối cùng cho các kế hoạch ứng phó với rủi ro lớn.
       - **Ban Quản lý Rủi ro (nếu có):** Nhóm chuyên trách rà soát và tư vấn về rủi ro.

    **4. Ngân sách và Nguồn lực Rủi ro (Risk Budgeting and Resources):**
       - Xác định cách thức dự phòng ngân sách cho các hoạt động quản lý rủi ro.
       - **Quỹ Dự phòng Ngẫu nhiên (Contingency Reserves):** Ngân sách dành cho các rủi ro đã được nhận diện và phân tích ("known-unknowns"), được Quản lý Dự án kiểm soát.
       - **Quỹ Dự phòng Quản lý (Management Reserves):** Ngân sách dành cho các rủi ro không thể lường trước ("unknown-unknowns"), được Ban Lãnh đạo cấp cao kiểm soát.
       - Phân bổ thời gian và nhân lực cho các hoạt động quản lý rủi ro (ví dụ: các buổi họp rà soát).

    **5. Lịch trình và Tần suất (Timing and Frequency):**
       - Xác định khi nào và tần suất các hoạt động quản lý rủi ro sẽ được thực hiện.
       - Ví dụ: "Các buổi họp nhận diện rủi ro sẽ được tổ chức vào đầu mỗi giai đoạn dự án", "Các cuộc họp rà soát Sổ đăng ký Rủi ro sẽ diễn ra hai tuần một lần", "Báo cáo rủi ro sẽ được đưa vào báo cáo tiến độ hàng tuần".

    **6. Các Hạng mục Rủi ro (Risk Categories):**
       - Cung cấp một cấu trúc phân loại rủi ro (Risk Breakdown Structure - RBS).
       - Các hạng mục có thể bao gồm: Kỹ thuật, Bên ngoài, Tổ chức, Quản lý Dự án, Thương mại, Pháp lý, v.v. Điều này giúp đảm bảo việc nhận diện rủi ro được toàn diện.

    **7. Phân tích Rủi ro và Ma trận (Risk Analysis and Matrix):**
       - Tham chiếu đến "Kế hoạch Phân tích Rủi ro" chi tiết.
       - Tóm tắt lại các định nghĩa về Thang đo Xác suất và Mức độ Ảnh hưởng.
       - Trình bày Ma trận Xác suất và Ảnh hưởng (P&I Matrix) sẽ được sử dụng để ưu tiên hóa rủi ro.

    **8. Các Ngưỡng Rủi ro và Mức độ Chấp nhận (Risk Thresholds and Appetite):**
       - Định nghĩa "mức độ chấp nhận rủi ro" của tổ chức hoặc dự án.
       - Thiết lập các ngưỡng rõ ràng (ví dụ: "Bất kỳ rủi ro nào có điểm số > 15 đều được coi là 'Cao' và yêu cầu báo cáo ngay lập tức cho Nhà tài trợ Dự án").

    **9. Báo cáo và Theo dõi (Reporting and Tracking):**
       - Mô tả định dạng và nội dung của các báo cáo rủi ro.
       - Xác định cách thức thông tin rủi ro sẽ được truyền đạt đến các bên liên quan khác nhau.
       - Quy định về Sổ đăng ký Rủi ro (Risk Register): ai chịu trách nhiệm cập nhật, nó được lưu trữ ở đâu, và những trường thông tin nào là bắt buộc.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền (Quản lý Dự án, Nhà tài trợ Dự án) để chính thức phê duyệt và ban hành Kế hoạch Quản lý Rủi ro này, biến nó thành một phần không thể thiếu của Kế hoạch Quản lý Dự án tổng thể.
    """,
    expected_output="""Một tài liệu "Kế hoạch Quản lý Rủi ro" hoàn chỉnh, mang tính chiến lược và chính thức dưới dạng Markdown.
    Tài liệu này không phải là một danh sách rủi ro, mà là một bản kế hoạch tổng thể định nghĩa 'cách thức, khi nào, ai, và như thế nào'
    trong việc quản lý rủi ro của dự án. Kết quả phải là một tài liệu tham chiếu cốt lõi, hướng dẫn mọi hoạt động liên quan đến rủi ro
    và thể hiện sự trưởng thành trong quản lý dự án.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "risk_management_plan", "1_riskplan", "risk_management_plan.md")
    )
    return [risk_information_form, risk_analysis_plan, risk_management_plan]


def create_wbs_tasks(planning_agent):
    """Tạo các nhiệm vụ liên quan đến Cấu trúc Phân rã Công việc (WBS)."""
    system_request = shared_memory.get("phase_1", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    wbs = Task(
        ddescription=f"""Soạn thảo một tài liệu "Đặc tả Cấu trúc Phân rã Công việc" (Work Breakdown Structure - WBS Specification).
    Tài liệu này là một bản kế hoạch chi tiết để xây dựng WBS, một công cụ nền tảng trong quản lý dự án,
    được sử dụng để phân rã một cách có hệ thống toàn bộ phạm vi công việc của dự án thành các thành phần nhỏ hơn, dễ quản lý hơn.
    Mục tiêu là tạo ra một tài liệu định hướng rõ ràng để xây dựng một WBS hoàn chỉnh, làm cơ sở cho việc lập kế hoạch chi tiết,
    ước tính chi phí, phân bổ nguồn lực và kiểm soát phạm vi dự án.

    Tài liệu đặc tả WBS cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu ngắn gọn về dự án mà WBS này sẽ phục vụ.
       - Mô tả vấn đề mà việc xây dựng WBS sẽ giải quyết (ví dụ: phạm vi dự án quá lớn và phức tạp, khó ước tính thời gian và chi phí, thiếu cơ sở để theo dõi tiến độ).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: tạo ra một danh sách đầy đủ 100% công việc của dự án, xác định các gói công việc (Work Packages) cụ thể, tạo cơ sở cho việc lập lịch trình và ngân sách).

    **2. Phạm vi và Cấp độ Phân rã (Scope and Level of Decomposition):**
       - **Phạm vi Dự án (Project Scope):** Tóm tắt phạm vi tổng thể của dự án sẽ được phân rã, tham chiếu đến tài liệu "Bảng Mô tả Công việc" (SoW) đã được phê duyệt.
       - **Nguyên tắc "100% Rule":** Nhấn mạnh rằng WBS sẽ bao gồm TOÀN BỘ công việc được xác định trong phạm vi dự án và không bao gồm bất kỳ công việc nào nằm ngoài phạm vi đó.
       - **Cấp độ Phân rã (Level of Decomposition):** Xác định mức độ chi tiết sẽ phân rã công việc. Nêu rõ tiêu chí để xác định một "Gói công việc" (Work Package), ví dụ như quy tắc 8/80 (công việc cần từ 8 đến 80 giờ để hoàn thành) hoặc có thể được giao cho một cá nhân/nhóm duy nhất.

    **3. Các Thành phần và Sản phẩm Bàn giao (Components and Deliverables):**
       - Liệt kê các sản phẩm bàn giao của chính nhiệm vụ tạo WBS này.
       - **Cấu trúc WBS (WBS Structure):** Một sơ đồ phân cấp trực quan hoặc danh sách có cấu trúc, hiển thị sự phân rã từ cấp cao nhất của dự án xuống các Gói công việc. Mỗi mục cần có một mã định danh duy nhất (WBS code).
       - **Từ điển WBS (WBS Dictionary):** Một tài liệu đi kèm mô tả chi tiết cho từng Gói công việc, bao gồm: mã WBS, mô tả công việc, sản phẩm bàn giao của gói công việc, tiêu chí chấp nhận, người/bộ phận chịu trách nhiệm, và các giả định.
       - **Định dạng bàn giao:** File PDF, file ảnh PNG, file gốc (ví dụ: Microsoft Project, Excel, Visio).

    **4. Lịch trình Xây dựng (Development Schedule):**
       - Trình bày một lịch trình chi tiết cho việc xây dựng và hoàn thiện WBS và từ điển đi kèm.
       - Xác định các cột mốc quan trọng:
         - "Hoàn thành phân rã Cấp 1 và 2 (các sản phẩm bàn giao chính) - [Ngày]"
         - "Tổ chức phiên làm việc với các nhóm chuyên môn để phân rã thành Gói công việc - [Ngày]"
         - "Hoàn thành bản nháp WBS và Từ điển WBS - [Ngày]"
         - "WBS được phê duyệt và trở thành đường cơ sở (baseline) - [Ngày]"

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định WBS đã hoàn chỉnh (ví dụ: "Tuân thủ nguyên tắc 100%", "Mỗi Gói công việc là duy nhất và không chồng chéo", "Tất cả các mục trong WBS đều có trong Từ điển WBS").
       - Mô tả quy trình rà soát và phê duyệt (ví dụ: bản nháp được rà soát bởi các trưởng nhóm, bản cuối cùng được phê duyệt bởi Quản lý Dự án và Nhà tài trợ Dự án để thiết lập đường cơ sở phạm vi (scope baseline)).

    **6. Các Giả định và Phụ thuộc (Assumptions and Dependencies):**
       - Liệt kê các giả định (ví dụ: "Tài liệu SoW là phiên bản cuối cùng và sẽ không thay đổi trong quá trình xây dựng WBS", "Các chuyên gia từ các bộ phận sẽ có mặt để đóng góp ý kiến").
       - Xác định các phụ thuộc (ví dụ: "Việc xây dựng WBS phụ thuộc vào việc SoW đã được ký duyệt", "Việc lập lịch trình và ngân sách chi tiết phụ thuộc vào việc WBS đã được phê duyệt").

    **7. Vai trò và Trách nhiệm (trong việc xây dựng WBS):**
       - Xác định rõ trách nhiệm của các bên trong quá trình *tạo ra* WBS.
       - **Quản lý Dự án (Project Manager):** Chịu trách nhiệm chính và điều phối quá trình.
       - **Các Trưởng nhóm/Chuyên gia (Team Leads/SMEs):** Chịu trách nhiệm phân rã các phần công việc thuộc lĩnh vực của họ.
       - **Nhà tài trợ Dự án (Project Sponsor):** Rà soát và phê duyệt WBS cuối cùng.

    **8. Công cụ và Kỹ thuật (Tools and Techniques):**
       - Nêu rõ các công cụ sẽ được sử dụng để tạo và trực quan hóa WBS (ví dụ: Microsoft Project, WBS Chart Pro, Excel, MindManager).
       - Mô tả kỹ thuật sẽ được áp dụng (ví dụ: "Phân rã từ trên xuống", "Sử dụng các mẫu WBS từ các dự án tương tự").

    **9. Quản lý Thay đổi (Change Management):**
       - Mô tả quy trình kiểm soát thay đổi sẽ được áp dụng sau khi WBS đã được phê duyệt và trở thành đường cơ sở.
       - Nhấn mạnh rằng bất kỳ thay đổi nào đối với WBS đều cấu thành một thay đổi phạm vi và phải tuân theo quy trình quản lý thay đổi chính thức của dự án.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền (ví dụ: Quản lý Dự án, Nhà tài trợ Dự án) để chính thức hóa "đường cơ sở phạm vi" (scope baseline).
    """,
    expected_output="""Một tài liệu "Đặc tả Cấu trúc Phân rã Công việc" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu này phải được viết với ngôn ngữ rõ ràng, chính xác, tạo ra một kế hoạch không thể diễn giải sai cho việc phân rã toàn bộ phạm vi công việc của dự án.
    Kết quả phải là một tài liệu tham chiếu cốt lõi, làm nền tảng cho tất cả các hoạt động lập kế hoạch và kiểm soát dự án sau này.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "wbs_specification", "1_wbs", "wbs_specification.md")
    )

    wbs_dictionary = Task(
        description=f"""Soạn thảo một tài liệu "Đặc tả Từ điển WBS" (WBS Dictionary Specification).
    Tài liệu này là một bản kế hoạch chi tiết để xây dựng Từ điển WBS, một tài liệu hỗ trợ quan trọng
    cung cấp mô tả chi tiết cho từng thành phần trong Cấu trúc Phân rã Công việc (WBS).
    Nếu WBS trả lời câu hỏi "Cần làm GÌ?", thì Từ điển WBS trả lời câu hỏi "Nó có nghĩa là GÌ?".
    Mục tiêu là tạo ra một tài liệu tham chiếu duy nhất, loại bỏ mọi sự mơ hồ về phạm vi của từng gói công việc (Work Package).

    Tài liệu đặc tả Từ điển WBS cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu rằng Từ điển WBS này là tài liệu đi kèm và bổ trợ cho tài liệu WBS đã được phê duyệt của dự án [Tên Dự án].
       - Mô tả vấn đề cần giải quyết (ví dụ: các tên gói công việc trong WBS có thể bị diễn giải sai, thiếu tiêu chí rõ ràng để nghiệm thu, khó khăn trong việc bàn giao công việc).
       - Nêu rõ mục tiêu cụ thể (ví dụ: cung cấp mô tả chi tiết và không mơ hồ cho mỗi gói công việc, định nghĩa sản phẩm bàn giao và tiêu chí chấp nhận cụ thể, tạo cơ sở vững chắc cho việc ước tính và kiểm soát).

    **2. Phạm vi và Cấu trúc (Scope and Structure):**
       - **Phạm vi (Scope):** Nêu rõ rằng từ điển này sẽ bao gồm một mục nhập chi tiết cho MỌI Gói công việc (Work Package) – tức là cấp độ thấp nhất – trong WBS đã được phê duyệt.
       - **Cấu trúc Mục nhập (Entry Structure):** Đây là phần cốt lõi, định nghĩa mẫu (template) cho mỗi mục trong từ điển. Mẫu này phải bao gồm các trường sau:
         - **Mã WBS (WBS Code):** Mã định danh duy nhất từ WBS (ví dụ: 1.4.2).
         - **Tên Gói công việc (Work Package Name):** Tên tương ứng trong WBS.
         - **Mô tả Công việc (Description of Work):** Mô tả chi tiết các hoạt động cần thực hiện.
         - **Sản phẩm Bàn giao (Deliverable(s)):** Danh sách các kết quả hữu hình hoặc vô hình sẽ được tạo ra từ gói công việc này.
         - **Tiêu chí Chấp nhận (Acceptance Criteria):** Các tiêu chí khách quan, có thể đo lường được để xác minh rằng sản phẩm bàn giao đã hoàn thành và đạt yêu cầu.
         - **Người/Bộ phận Chịu trách nhiệm (Responsible Person/Team):** Cá nhân hoặc nhóm được giao thực hiện.
         - **Các Giả định và Ràng buộc (Assumptions and Constraints):** Các giả định và ràng buộc cụ thể áp dụng cho riêng gói công việc này.
         - **Ước tính Chi phí/Ngân sách (Cost/Budget Estimate):** Chi phí dự kiến cho gói công việc.
         - **Cột mốc Lịch trình (Schedule Milestones):** Ngày bắt đầu, ngày kết thúc dự kiến hoặc các cột mốc quan trọng.
         - **Tài nguyên Yêu cầu (Resources Required):** Nhân sự, thiết bị, phần mềm cần thiết.

    **3. Sản phẩm Bàn giao (Deliverable):**
       - Sản phẩm bàn giao chính của nhiệm vụ này là tài liệu "Từ điển WBS" hoàn chỉnh, được điền đầy đủ thông tin cho tất cả các gói công việc.
       - Định dạng bàn giao: File Word/PDF, trang Confluence/SharePoint, hoặc một tab trong file MS Project/Excel.

    **4. Lịch trình Soạn thảo (Compilation Schedule):**
       - Trình bày kế hoạch chi tiết để điền thông tin và hoàn thiện từ điển.
       - Xác định các cột mốc quan trọng:
         - "Phân phối mẫu Từ điển WBS cho các Trưởng nhóm - [Ngày]"
         - "Thu thập bản nháp các mục từ điển từ các nhóm - [Ngày]"
         - "Rà soát, tổng hợp và chuẩn hóa tất cả các mục - [Ngày]"
         - "Từ điển WBS được phê duyệt cuối cùng - [Ngày]"

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định Từ điển WBS đã hoàn chỉnh (ví dụ: "Mỗi Gói công việc trong WBS đều có một mục tương ứng", "Tất cả các trường bắt buộc trong mẫu đều được điền", "Tiêu chí chấp nhận rõ ràng và có thể kiểm chứng").
       - Mô tả quy trình rà soát và phê duyệt (ví dụ: mỗi mục được rà soát bởi Quản lý Dự án và Trưởng nhóm liên quan, toàn bộ tài liệu được phê duyệt bởi Quản lý Dự án và Nhà tài trợ Dự án).

    **6. Các Giả định và Phụ thuộc (Assumptions and Dependencies):**
       - Liệt kê các giả định (ví dụ: "Tài liệu WBS đã được chốt và sẽ không thay đổi trong quá trình này", "Các Trưởng nhóm có đủ thông tin để mô tả chi tiết công việc").
       - Xác định các phụ thuộc (ví dụ: "Việc soạn thảo Từ điển WBS chỉ có thể bắt đầu sau khi WBS được phê duyệt").

    **7. Vai trò và Trách nhiệm (trong việc soạn thảo Từ điển):**
       - Xác định rõ trách nhiệm của các bên trong việc *tạo ra* Từ điển WBS.
       - **Quản lý Dự án:** Cung cấp mẫu, điều phối, rà soát tính nhất quán và phê duyệt.
       - **Trưởng nhóm/Chủ sở hữu Gói công việc:** Chịu trách nhiệm chính trong việc điền thông tin chi tiết cho các gói công việc thuộc phạm vi của họ.

    **8. Công cụ và Định dạng (Tool and Format):**
       - Xác định công cụ sẽ được sử dụng để tạo và duy trì Từ điển WBS (ví dụ: Microsoft Word, Excel, Confluence).
       - Nhấn mạnh sự cần thiết của việc sử dụng một mẫu (template) nhất quán cho tất cả các mục.

    **9. Quản lý Thay đổi (Change Management):**
       - Mô tả quy trình kiểm soát thay đổi sẽ được áp dụng cho Từ điển WBS.
       - Nhấn mạnh rằng Từ điển WBS là một phần của đường cơ sở phạm vi (scope baseline). Bất kỳ thay đổi nào đối với nó (ví dụ: thay đổi mô tả, tiêu chí chấp nhận) đều phải tuân theo quy trình quản lý thay đổi chính thức.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền (ví dụ: Quản lý Dự án, Nhà tài trợ Dự án) để chính thức hóa Từ điển WBS như một phần không thể thiếu của đường cơ sở phạm vi.
    """,
    expected_output="""Một tài liệu "Đặc tả Từ điển WBS" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown.
    Tài liệu này phải xác định rõ ràng cấu trúc, nội dung và quy trình xây dựng Từ điển WBS.
    Kết quả cuối cùng là một mẫu và kế hoạch hành động để tạo ra một Từ điển WBS chi tiết, đảm bảo sự hiểu biết chung về phạm vi công việc trong toàn bộ nhóm dự án.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "wbs_dictionary_specification", "1_wbs", "wbs_dictionary_specification.md")
    )

    wbs_resource_template = Task(
        description=f"""Soạn thảo một tài liệu "Đặc tả Mẫu Phân bổ Nguồn lực theo WBS" (WBS Resource Template Specification).
    Tài liệu này là một bản thiết kế chi tiết để xây dựng một mẫu chuẩn (template) dùng để xác định,
    ước tính và phân bổ tất cả các loại nguồn lực (nhân sự, thiết bị, vật liệu) cần thiết cho mỗi Gói công việc (Work Package) trong WBS.
    Mục tiêu là tạo ra một công cụ nhất quán và toàn diện, giúp đảm bảo rằng việc lập kế hoạch nguồn lực được thực hiện một cách đồng bộ
    trên toàn dự án, tạo điều kiện thuận lợi cho việc tổng hợp, phân tích và quản lý ngân sách.

    Tài liệu đặc tả này cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu rằng mẫu này sẽ được sử dụng cùng với WBS và Từ điển WBS để hoàn thiện kế hoạch dự án.
       - Mô tả vấn đề cần giải quyết (ví dụ: các nhóm ước tính nguồn lực theo các cách khác nhau, thiếu thông tin để tổng hợp kế hoạch nguồn lực toàn dự án, khó theo dõi chi phí nhân sự và thiết bị).
       - Nêu rõ các mục tiêu cụ thể (ví dụ: chuẩn hóa quy trình ước tính nguồn lực, tạo ra một nguồn dữ liệu duy nhất cho nhu cầu nguồn lực của dự án, cung cấp đầu vào chính xác cho kế hoạch chi phí và lịch trình).

    **2. Phạm vi và Cấu trúc Mẫu (Template Scope and Structure):**
       - **Phạm vi (Scope):** Nêu rõ rằng mẫu này sẽ được áp dụng cho mọi Gói công việc trong WBS và phải bao gồm tất cả các loại nguồn lực cần thiết.
       - **Cấu trúc Mẫu (Template Structure):** Đây là phần cốt lõi, định nghĩa các cột (trường dữ liệu) của mẫu. Mẫu này thường ở dạng bảng tính và phải bao gồm:
         - **Thông tin nhận dạng (Identifier Information):**
           - Mã WBS (WBS Code)
           - Tên Gói công việc (Work Package Name)
         - **Thông tin Nguồn lực (Resource Information):**
           - Loại Nguồn lực (Resource Type - ví dụ: Nhân sự, Thiết bị, Vật liệu, Cơ sở vật chất)
           - Tên/Vai trò Nguồn lực (Resource Name/Role - ví dụ: Lập trình viên Senior, Máy chủ Test, Giấy phép phần mềm X)
           - Đơn vị tính (Unit - ví dụ: Giờ, Ngày, Cái, Gói)
         - **Thông tin Ước tính (Estimation Information):**
           - Số lượng (Quantity)
           - Đơn giá (Unit Cost/Rate)
           - Tổng chi phí (Total Cost = Quantity * Unit Cost)
         - **Thông tin Lịch trình (Scheduling Information):**
           - Thời gian Bắt đầu Phân bổ (Planned Start Date)
           - Thời gian Kết thúc Phân bổ (Planned End Date)
         - **Ghi chú (Notes):** Các giả định hoặc thông tin bổ sung về nguồn lực này.

    **3. Sản phẩm Bàn giao (Deliverable):**
       - Sản phẩm bàn giao chính của nhiệm vụ này là một file mẫu (template) có thể sử dụng ngay, với cấu trúc đã được định nghĩa ở trên.
       - Định dạng bàn giao: File Microsoft Excel hoặc Google Sheets trống, có các tiêu đề cột, định dạng và các công thức tính toán cơ bản (ví dụ: cột Tổng chi phí).

    **4. Lịch trình Soạn thảo Mẫu (Template Development Schedule):**
       - Trình bày kế hoạch chi tiết để thiết kế và hoàn thiện mẫu phân bổ nguồn lực.
       - Xác định các cột mốc quan trọng:
         - "Hoàn thành bản nháp cấu trúc các cột của mẫu - [Ngày]"
         - "Lấy ý kiến từ các Trưởng nhóm và phòng Tài chính - [Ngày]"
         - "Hoàn thiện và khóa cấu trúc mẫu cuối cùng - [Ngày]"

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định mẫu đã hoàn chỉnh (ví dụ: "Bao gồm tất cả các trường dữ liệu cần thiết", "Công thức tính toán chính xác", "Có hướng dẫn sử dụng đi kèm nếu cần thiết").
       - Mô tả quy trình rà soát và phê duyệt chính cái mẫu này (ví dụ: Quản lý Dự án soạn thảo, Trưởng phòng Quản lý Dự án (PMO) hoặc Giám đốc Tài chính rà soát, Nhà tài trợ Dự án phê duyệt mẫu để đưa vào sử dụng chính thức).

    **6. Các Giả định và Phụ thuộc (Assumptions and Dependencies):**
       - Liệt kê các giả định (ví dụ: "Công ty có một danh sách đơn giá chuẩn cho các vai trò nhân sự và thiết bị", "Các Trưởng nhóm hiểu cách sử dụng Excel/Google Sheets").
       - Xác định các phụ thuộc (ví dụ: "Việc sử dụng mẫu này phụ thuộc vào việc WBS và Từ điển WBS đã được phê duyệt", "Đơn giá nguồn lực cần được cung cấp bởi phòng Nhân sự và Mua hàng").

    **7. Vai trò và Trách nhiệm (trong việc tạo Mẫu):**
       - Xác định rõ trách nhiệm của các bên trong việc *tạo ra* mẫu.
       - **Quản lý Dự án:** Chịu trách nhiệm chính trong việc thiết kế và điều phối.
       - **Trưởng nhóm:** Cung cấp ý kiến phản hồi về tính thực tiễn của mẫu.
       - **Phòng Tài chính/Kế toán:** Cung cấp yêu cầu về các trường dữ liệu liên quan đến chi phí để đảm bảo tính tương thích với hệ thống tài chính.

    **8. Công cụ và Hướng dẫn (Tool and Guidance):**
       - Xác định công cụ chính để tạo mẫu (ví dụ: Microsoft Excel).
       - Cân nhắc việc tạo một tab "Hướng dẫn sử dụng" (Instructions) ngắn gọn ngay trong file mẫu để giải thích ý nghĩa của từng cột và cách điền thông tin.

    **9. Quản lý Thay đổi (Change Management):**
       - Mô tả quy trình quản lý thay đổi cho chính cái mẫu này.
       - Sau khi mẫu được phê duyệt và đưa vào sử dụng, bất kỳ yêu cầu thay đổi cấu trúc mẫu (ví dụ: thêm/bớt cột) đều phải thông qua quy trình kiểm soát thay đổi để đảm bảo tính nhất quán.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền (ví dụ: Quản lý Dự án, Trưởng phòng PMO) để chính thức ban hành mẫu này như một công cụ bắt buộc cho việc lập kế hoạch dự án.
    """,
    expected_output="""Một tài liệu "Đặc tả Mẫu Phân bổ Nguồn lực theo WBS" hoàn chỉnh, chi tiết và chính thức dưới dạng Markdown,
    cùng với một sản phẩm bàn giao là một file mẫu (template) Excel/Google Sheets có cấu trúc rõ ràng.
    Tài liệu đặc tả phải tạo ra một kế hoạch không thể diễn giải sai cho việc xây dựng mẫu,
    và mẫu kết quả phải sẵn sàng để các nhóm dự án sử dụng ngay lập tức cho việc lập kế hoạch nguồn lực.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "wbs_resource_template_specification", "1_wbs", "wbs_resource_template_specification.md")
    )

    project_plan = Task(
        description=f"""Soạn thảo một tài liệu "Kế hoạch Quản lý Dự án" (Project Management Plan) toàn diện, chính thức và được tích hợp.
    Tài liệu này là một tài liệu tổng hợp, kết hợp tất cả các kế hoạch quản lý phụ và các đường cơ sở (baselines)
    để tạo thành một bản chỉ dẫn duy nhất cho việc thực hiện và kiểm soát dự án.
    Mục tiêu là tạo ra một "nguồn sự thật duy nhất" (single source of truth) cho tất cả các bên liên quan,
    định nghĩa rõ ràng CÁCH THỨC dự án sẽ được quản lý từ đầu đến cuối.

    Kế hoạch Quản lý Dự án cần bao gồm các phần chính sau:

    **1. Bối cảnh và Mục tiêu (Background and Objectives):**
       - Giới thiệu tổng quan về dự án, tham chiếu đến Hiến chương Dự án (Project Charter) và Bảng Mô tả Công việc (SoW).
       - Mô tả mục đích của tài liệu này: để định hướng việc thực thi, giám sát và kiểm soát dự án.
       - Nêu rõ các mục tiêu chính của kế hoạch: thiết lập các đường cơ sở (scope, schedule, cost), xác định các quy trình quản lý, và hướng dẫn việc ra quyết định trong suốt vòng đời dự án.

    **2. Cấu trúc và Các Kế hoạch thành phần (Structure and Subsidiary Plans):**
       - Đây là phần mô tả cấu trúc của Kế hoạch tổng thể này.
       - **Các Kế hoạch Quản lý Phụ (Subsidiary Management Plans):** Liệt kê tất cả các kế hoạch con sẽ được tích hợp hoặc tham chiếu, bao gồm:
         - Kế hoạch Quản lý Phạm vi (Scope Management Plan)
         - Kế hoạch Quản lý Yêu cầu (Requirements Management Plan)
         - Kế hoạch Quản lý Lịch trình (Schedule Management Plan)
         - Kế hoạch Quản lý Chi phí (Cost Management Plan)
         - Kế hoạch Quản lý Chất lượng (Quality Management Plan)
         - Kế hoạch Quản lý Nguồn lực (Resource Management Plan)
         - Kế hoạch Quản lý Truyền thông (Communications Management Plan)
         - Kế hoạch Quản lý Rủi ro (Risk Management Plan)
         - Kế hoạch Quản lý Mua sắm (Procurement Management Plan)
         - Kế hoạch Quản lý Các bên liên quan (Stakeholder Engagement Plan)
       - **Ngoài Phạm vi (Out-of-Scope):** Nêu rõ rằng tài liệu này là một kế hoạch quản lý, không phải là nơi lưu trữ các tài liệu thực thi hàng ngày (ví dụ: nhật ký công việc, báo cáo chi tiết).

    **3. Các Đường cơ sở của Dự án (Project Baselines):**
       - Đây là phần cốt lõi, xác định các thước đo hiệu suất của dự án.
       - **Đường cơ sở Phạm vi (Scope Baseline):** Bao gồm Bảng Mô tả Công việc (SoW) đã duyệt, Cấu trúc Phân rã Công việc (WBS), và Từ điển WBS (WBS Dictionary).
       - **Đường cơ sở Lịch trình (Schedule Baseline):** Phiên bản đã được phê duyệt của lịch trình dự án.
       - **Đường cơ sở Chi phí (Cost Baseline):** Ngân sách dự án đã được phê duyệt và phân bổ theo thời gian.
       - **Đường cơ sở Đo lường Hiệu suất (Performance Measurement Baseline - PMB):** Sự tích hợp của cả ba đường cơ sở trên, làm nền tảng cho việc phân tích giá trị thu được (Earned Value Analysis).

    **4. Lịch trình Soạn thảo và Phê duyệt Kế hoạch (Plan Development and Approval Schedule):**
       - Trình bày kế hoạch chi tiết để xây dựng, rà soát và phê duyệt Kế hoạch Quản lý Dự án tổng thể.
       - Xác định các cột mốc quan trọng:
         - "Hoàn thành các đường cơ sở (Scope, Schedule, Cost) - [Ngày]"
         - "Hoàn thành bản nháp tất cả các kế hoạch quản lý phụ - [Ngày]"
         - "Tích hợp và hoàn thiện bản nháp Kế hoạch Quản lý Dự án - [Ngày]"
         - "Kế hoạch Quản lý Dự án được phê duyệt cuối cùng - [Ngày]"

    **5. Tiêu chí Hoàn thành và Quy trình Phê duyệt (Completion Criteria and Approval Process):**
       - Định nghĩa các tiêu chí để xác định Kế hoạch đã hoàn chỉnh (ví dụ: "Tất cả các kế hoạch phụ đã được tích hợp", "Các đường cơ sở đã được thiết lập và phê duyệt", "Các kế hoạch nhất quán và không mâu thuẫn với nhau").
       - Mô tả quy trình phê duyệt chính thức: Quản lý Dự án trình kế hoạch, Ban kiểm soát thay đổi (CCB) hoặc PMO rà soát, và Nhà tài trợ Dự án là người phê duyệt cuối cùng để chính thức khởi động giai đoạn thực thi.

    **6. Các Giả định và Ràng buộc Tổng thể (Overall Assumptions and Constraints):**
       - Tổng hợp các giả định và ràng buộc chính từ tất cả các kế hoạch phụ, cung cấp một cái nhìn toàn cảnh về các yếu tố ảnh hưởng đến dự án.

    **7. Vai trò và Trách nhiệm Quản lý Dự án (Project Management Roles and Responsibilities):**
       - Tham chiếu đến Ma trận RACI và Sơ đồ Tổ chức dự án.
       - Tóm tắt các vai trò và trách nhiệm chính trong việc quản lý và thực thi dự án theo kế hoạch này.

    **8. Vòng đời Dự án và Các Giai đoạn (Project Life Cycle and Phases):**
       - Mô tả vòng đời dự án đã được chọn (ví dụ: Waterfall, Agile, Hybrid).
       - Xác định các giai đoạn chính của dự án và các cổng chất lượng (gate reviews) hoặc điểm quyết định giữa các giai đoạn.

    **9. Quy trình Quản lý Thay đổi Tích hợp (Integrated Change Control Process):**
       - Đây là một phần cực kỳ quan trọng. Mô tả quy trình chính thức để quản lý các thay đổi đối với BẤT KỲ phần nào của Kế hoạch Quản lý Dự án sau khi nó đã được phê duyệt.
       - Quy trình này bao gồm cách một yêu cầu thay đổi (Change Request) được đề xuất, phân tích, phê duyệt/từ chối, và cách các đường cơ sở sẽ được cập nhật.

    **10. Phần Ký duyệt (Sign-off):**
        - Chừa không gian cho chữ ký của các đại diện có thẩm quyền cao nhất, chính thức phê duyệt Kế hoạch Quản lý Dự án và cho phép dự án chuyển sang giai đoạn thực thi. Các bên ký duyệt thường bao gồm Quản lý Dự án và Nhà tài trợ Dự án.
    """,
    expected_output="""Một tài liệu "Kế hoạch Quản lý Dự án" hoàn chỉnh, được tích hợp, và mang tính chính thức dưới dạng Markdown.
    Tài liệu này không chỉ là một tập hợp các tài liệu rời rạc mà là một thể thống nhất, logic, và là kim chỉ nam cho mọi hoạt động của dự án.
    Kết quả phải là tài liệu tham chiếu cốt lõi mà Quản lý Dự án và nhóm dự án sử dụng để định hướng công việc của họ và đo lường sự thành công.
    """,
        agent=planning_agent,
        callback=lambda output: _save_task_output(output, "phase_1", "project_management_plan", "1_wbs", "project_management_plan.md")
    )
    return [wbs, wbs_dictionary, wbs_resource_template, project_plan]