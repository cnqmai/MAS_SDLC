# initiation_phase_tasks.py
# This file contains all task creation functions for the Initiation Phase of the project.

from crewai import Task
from crewai.tasks.task_output import TaskOutput
from utils.file_writer import write_output
from memory.shared_memory import shared_memory

# --- Helper function for callbacks ---
def _save_task_output(task_output: TaskOutput, phase: str, key: str, folder: str, filename: str):
    """A standardized callback function to save task output."""
    output_content = str(task_output.raw_output)
    print(f"--- Nhiệm Vụ {key.replace('_', ' ').title()} Hoàn Thành ---")
    write_output(f"{folder}/{filename}", output_content)
    shared_memory.set(phase, key, output_content)

# --- Task Creation Functions ---

def create_initiation_tasks(initiation_agent):
    """
    Tạo các nhiệm vụ khởi tạo dự án cốt lõi: Project Charter, Business Case, và Feasibility Report.
    """
    system_request = shared_memory.get("phase_0", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    Project_Charter = Task(
        description=f"""Dựa trên Yêu Cầu Hệ Thống ({system_request}), 
        hãy soạn thảo một Hiến Chương Dự Án (Project Charter) chính thức.
        Tài liệu này là văn bản phê duyệt sự tồn tại của dự án và cung cấp cho Quản lý Dự án quyền hạn để sử dụng các nguồn lực của tổ chức cho các hoạt động của dự án.
        
        Hiến Chương Dự Án cần bao gồm các phần cốt lõi sau:
        1. Tên dự án và mục đích (Project Purpose)
        2. Mục tiêu có thể đo lường và tiêu chí thành công (Measurable Objectives and Success Criteria)
        3. Các yêu cầu cấp cao (High-Level Requirements)
        4. Các giả định và ràng buộc chính (Key Assumptions and Constraints)
        5. Rủi ro cấp cao (High-Level Risks)
        6. Lịch trình cột mốc tóm tắt (Summary Milestone Schedule)
        7. Ngân sách tóm tắt (Summary Budget)
        8. Danh sách các bên liên quan (Stakeholder List)
        9. Phân công Quản lý dự án và quyền hạn (Project Manager Assignment and Authority Level)
        10. Sự chấp thuận của nhà tài trợ (Sponsor Authorization)
        """,
        expected_output="Một tài liệu Hiến Chương Dự Án (Project Charter) hoàn chỉnh dưới dạng Markdown. Tài liệu phải mang tính chính thức, rõ ràng, súc tích, đóng vai trò là văn bản phê duyệt và định hình khung cho dự án.",
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "project_charter", "0_initiation", "project_charter.md")
    )

    Business_Case = Task(
        description=f"""Từ Yêu Cầu Hệ Thống ({system_request}),
        hãy phát triển một Luận Chứng Kinh Doanh (Business Case) chi tiết để biện minh cho việc đầu tư vào dự án.
        Tài liệu này phải phân tích các lợi ích về tài chính, hoạt động và chiến lược, so sánh chúng với chi phí dự kiến để thuyết phục ban lãnh đạo phê duyệt dự án.

        Luận Chứng Kinh Doanh cần bao gồm các phần sau:
        1. Tóm tắt cho lãnh đạo (Executive Summary)
        2. Vấn đề và Cơ hội kinh doanh (Business Problem and Opportunity)
        3. Phân tích các phương án (Analysis of Options)
        4. Phương án đề xuất (Recommended Solution)
        5. Phân tích Chi phí - Lợi ích (Cost-Benefit Analysis)
        6. Rủi ro và Kế hoạch giảm thiểu (Risks and Mitigation)
        7. Sự phù hợp với chiến lược (Strategic Alignment)
        """,
        expected_output="Một tài liệu Luận Chứng Kinh Doanh (Business Case) hoàn chỉnh dưới dạng Markdown, có tính thuyết phục, dựa trên phân tích tài chính và chiến lược.",
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "business_case", "0_initiation", "business_case.md")
    )

    Feasibility_Report = Task(
        description=f"""Dựa trên Yêu Cầu Hệ Thống ({system_request}), hãy tiến hành một nghiên cứu và soạn thảo Báo cáo Khả thi (Feasibility Report) toàn diện.
        Báo cáo này cần đánh giá tính thực tiễn và khả thi của dự án được đề xuất trên nhiều phương diện khác nhau (Kỹ thuật, Kinh tế, Vận hành, Pháp lý, Thời gian) để xác định liệu dự án có nên được tiếp tục hay không.

        Báo cáo Khả thi cần phân tích và trình bày các khía cạnh sau:
        1.  Tổng quan và Mục đích Báo cáo
        2.  Phân tích Tính Khả thi Kỹ thuật
        3.  Phân tích Tính Khả thi Kinh tế
        4.  Phân tích Tính Khả thi Vận hành
        5.  Phân tích Tính Khả thi Pháp lý và Tuân thủ
        6.  Phân tích Tính Khả thi về Thời gian
        7.  Kết luận và Đề xuất (Tiếp tục, Tiếp tục có điều kiện, Hủy bỏ)
        """,
        expected_output="Một Báo cáo Khả thi (Feasibility Report) hoàn chỉnh dưới dạng Markdown, cung cấp một cơ sở vững chắc để quyết định có nên tiếp tục đầu tư vào giai đoạn lập kế hoạch hay không.",
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "feasibility_report", "0_initiation", "feasibility_report.md")
    )

    return [Project_Charter, Business_Case, Feasibility_Report]


def create_estimation_tasks(initiation_agent):
    """
    Tạo các nhiệm vụ ước tính ban đầu về tiến độ, ngân sách, và lợi ích.
    """
    system_request = shared_memory.get("phase_0", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    Preliminary_Schedule = Task(
    description=f"""Xây dựng một "Lịch trình Sơ bộ" (Preliminary Schedule) cho dự án.
    Tài liệu này cung cấp một cái nhìn tổng quan, cấp cao về dòng thời gian của dự án,
    xác định các giai đoạn chính và các cột mốc quan trọng (milestones).
    Mục đích của lịch trình này là để thiết lập kỳ vọng ban đầu về thời lượng dự án
    và cung cấp một khung sườn cho việc lập kế hoạch chi tiết ở giai đoạn sau.

    Lịch trình Sơ bộ cần bao gồm các phần chính sau:

    **1. Các Giả định Chính (Key Assumptions):**
       - Liệt kê các giả định nền tảng đã được sử dụng để xây dựng lịch trình này.
       - Ví dụ: "Giả định đội ngũ dự án sẽ đầy đủ vào ngày X", "Giả định thời gian phê duyệt các yêu cầu không quá 3 ngày làm việc", "Giả định không có sự chậm trễ từ nhà cung cấp bên thứ ba".

    **2. Tổng quan các Giai đoạn Dự án (Project Phases Overview):**
       - Chia dự án thành các giai đoạn chính và ước tính thời gian bắt đầu/kết thúc cho mỗi giai đoạn.
       - Trình bày dưới dạng bảng đơn giản:
         - **Giai đoạn (Phase):** (ví dụ: Khởi tạo, Lập kế hoạch, Thực thi & Phát triển, Kiểm thử, Triển khai, Đóng dự án).
         - **Ngày Bắt đầu Ước tính:**
         - **Ngày Kết thúc Ước tính:**
         - **Thời lượng (Tuần/Tháng):**

    **3. Bảng các Cột mốc Quan trọng (Key Milestones Table):**
       - Đây là phần cốt lõi, liệt kê các cột mốc chính (không phải các tác vụ nhỏ lẻ) dưới dạng bảng.
       - Một cột mốc đánh dấu sự hoàn thành của một nhóm công việc hoặc một sản phẩm bàn giao quan trọng.
       - Các cột bao gồm:
         - **ID Cột mốc:**
         - **Tên Cột mốc:** (ví dụ: "Hiến chương Dự án được ký duyệt", "Thiết kế UI/UX hoàn thành", "Bản thử nghiệm Alpha được phát hành", "Hệ thống đi vào hoạt động (Go-live)").
         - **Giai đoạn liên quan:**
         - **Ngày Hoàn thành Mục tiêu:**
         - **Tiêu chí Hoàn thành:** (Mô tả ngắn gọn làm thế nào để biết cột mốc này đã đạt được).

    **4. Các Phụ thuộc Cấp cao (High-Level Dependencies):**
       - Nêu bật các mối quan hệ phụ thuộc quan trọng nhất giữa các cột mốc hoặc các giai đoạn.
       - Ví dụ: "Giai đoạn Thực thi không thể bắt đầu cho đến khi Giai đoạn Lập kế hoạch được phê duyệt", "Việc Kiểm thử chỉ có thể bắt đầu sau khi bản thử nghiệm Alpha được phát hành".

    **5. Đường Găng (Critical Path) Sơ bộ:**
       - Dựa trên các cột mốc và phụ thuộc, xác định chuỗi các hoạt động dài nhất quyết định thời gian hoàn thành sớm nhất của dự án (nếu có thể xác định ở giai đoạn này).
       - Hoặc, chỉ cần nêu bật các cột mốc được cho là nằm trên đường găng.
    """,
    expected_output="""Một tài liệu "Lịch trình Sơ bộ" hoàn chỉnh dưới dạng Markdown.
    Tài liệu phải cung cấp một dòng thời gian cấp cao, rõ ràng, xác định các giai đoạn, cột mốc quan trọng, và các giả định cơ bản.
    Kết quả phải là một công cụ trực quan giúp tất cả các bên liên quan thống nhất về kỳ vọng thời gian và trình tự thực hiện dự án.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "preliminary_schedule", "0_estimation", "preliminary_schedule.md")
    )

    Budget_Estimate = Task(
        description=f"""Xây dựng tài liệu "Ước tính Ngân sách Sơ bộ" (Preliminary Budget Estimate) chi tiết.
    Tài liệu này cung cấp một phân tích ban đầu về tổng chi phí dự kiến để hoàn thành dự án.
    Mục đích là để trình bày cho nhà tài trợ và các bên liên quan một bức tranh tài chính tổng quan,
    làm cơ sở cho việc phê duyệt ngân sách và ra quyết định đầu tư.

    Ước tính Ngân sách cần bao gồm các phần chính sau:

    **1. Tóm tắt Ngân sách (Budget Summary):**
       - Trình bày con số tổng chi phí ước tính.
       - Nêu rõ độ chính xác của ước tính này (ví dụ: Ước tính Sơ bộ Cấp cao - Rough Order of Magnitude (ROM), với độ chính xác khoảng -25% đến +75%).
       - Thời gian hiệu lực của bản ước tính này.

    **2. Các Giả định và Cơ sở Ước tính (Assumptions and Basis of Estimate):**
       - Liệt kê các giả định tài chính quan trọng đã được sử dụng.
       - Ví dụ: "Đơn giá nhân công được lấy từ bảng lương chuẩn của công ty", "Chi phí phần mềm được dựa trên báo giá sơ bộ từ nhà cung cấp X", "Tỷ giá hối đoái được giả định là...".
       - Mô tả phương pháp ước tính đã sử dụng (ví dụ: Ước tính tương tự từ dự án cũ, ước tính tham số).

    **3. Phân rã Chi phí Chi tiết (Cost Breakdown):**
       - Đây là phần cốt lõi, phân rã tổng chi phí thành các hạng mục chính để tăng tính minh bạch. Trình bày dưới dạng bảng:
         - **Hạng mục Chi phí (Cost Category):** (ví dụ: Nhân sự, Phần cứng, Phần mềm, Đào tạo, Đi lại, Nhà thầu phụ).
         - **Mô tả Chi tiết:** (ví dụ: Lương cho 2 Lập trình viên trong 6 tháng, Mua 1 server staging, Giấy phép phần mềm Jira, Chi phí đào tạo người dùng cuối).
         - **Ước tính Chi phí (Estimated Cost):**
         - **Ghi chú:**
       - Cung cấp một dòng tổng cộng (Subtotal) cho các chi phí trực tiếp này.

    **4. Dự phòng Rủi ro (Contingency Reserve):**
       - Một khoản ngân sách được thêm vào để đối phó với các rủi ro đã xác định ("known-unknowns").
       - Thường được tính bằng một tỷ lệ phần trăm của tổng chi phí trực tiếp (ví dụ: 10% - 15%).
       - Nêu rõ: "Dự phòng Rủi ro (10%): [Số tiền]".

    **5. Dự phòng Quản lý (Management Reserve):**
       - Một khoản ngân sách riêng để đối phó với các rủi ro chưa xác định ("unknown-unknowns") hoặc các thay đổi phạm vi không lường trước.
       - Khoản này do ban lãnh đạo hoặc nhà tài trợ kiểm soát.
       - Thường được tính bằng một tỷ lệ phần trăm (ví dụ: 5% - 10%).
       - Nêu rõ: "Dự phòng Quản lý (5%): [Số tiền]".

    **6. Tổng Ngân sách Dự án (Total Project Budget):**
       - Tổng cộng của tất cả các khoản trên.
       - **Tổng chi phí trực tiếp + Dự phòng Rủi ro + Dự phòng Quản lý = Tổng Ngân sách Dự án.**
       - Trình bày rõ ràng con số cuối cùng này.

    **7. Lịch trình Giải ngân (Funding Schedule - Optional):**
       - Nếu có thể, phác thảo kế hoạch khi nào các khoản tiền cần được giải ngân theo các giai đoạn của dự án (ví dụ: Theo quý hoặc theo cột mốc).
    """,
    expected_output="""Một tài liệu "Ước tính Ngân sách Sơ bộ" hoàn chỉnh và chuyên nghiệp dưới dạng Markdown.
    Tài liệu phải trình bày một cách minh bạch và logic về cách con số ngân sách tổng được tính toán,
    bao gồm phân rã chi phí chi tiết, các khoản dự phòng, và các giả định quan trọng.
    Kết quả phải là một tài liệu thuyết phục, đáng tin cậy để hỗ trợ việc ra quyết định tài chính cho dự án.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "budget_estimate", "0_estimation", "budget_estimate.md")
    )

    Cost_Benefit_Analysis = Task(
        description=f"""Thực hiện và soạn thảo một tài liệu "Phân tích Chi phí - Lợi ích" (Cost-Benefit Analysis - CBA) thuyết phục.
    Tài liệu này đánh giá một cách có hệ thống cả chi phí đầu tư và lợi ích thu được từ dự án,
    nhằm cung cấp một cơ sở lý luận tài chính vững chắc cho việc phê duyệt dự án.
    Mục tiêu là chứng minh rằng lợi ích của dự án vượt trội so với chi phí bỏ ra.

    Tài liệu Phân tích Chi phí - Lợi ích cần bao gồm các phần chính sau:

    **1. Tóm tắt Phân tích (Executive Summary):**
       - Trình bày kết luận chính của bản phân tích: Dự án có đáng để đầu tư không?
       - Nêu bật các chỉ số tài chính quan trọng nhất (ví dụ: Tổng lợi ích, Tổng chi phí, Tỷ lệ Lợi ích/Chi phí, Thời gian hoàn vốn).

    **2. Mô tả Dự án và các Phương án (Project Description and Alternatives):**
       - Mô tả ngắn gọn về dự án đang được xem xét.
       - Liệt kê các phương án khác đã được cân nhắc, bao gồm cả phương án "Không làm gì" (Status Quo), để so sánh.

    **3. Phân tích Chi phí (Cost Analysis):**
       - Tổng hợp lại các chi phí dự kiến. Có thể tham chiếu từ tài liệu "Ước tính Ngân sách".
       - Phân loại chi phí:
         - **Chi phí một lần (One-Time Costs):** Chi phí phát triển, mua sắm thiết bị, phần mềm, đào tạo ban đầu.
         - **Chi phí định kỳ/vận hành (Recurring/Operational Costs):** Chi phí bảo trì, giấy phép hàng năm, lương nhân viên vận hành.
       - Trình bày chi phí dự kiến theo từng năm trong một khoảng thời gian phân tích (ví dụ: 3-5 năm).

    **4. Phân tích Lợi ích (Benefit Analysis):**
       - Xác định và định lượng (nếu có thể) các lợi ích mà dự án sẽ mang lại.
       - Phân loại lợi ích:
         - **Lợi ích hữu hình (Tangible Benefits):** Có thể đo lường trực tiếp bằng tiền. Ví dụ: Tăng doanh thu, giảm chi phí vận hành, tiết kiệm thời gian nhân viên (quy ra tiền lương).
         - **Lợi ích vô hình (Intangible Benefits):** Khó đo lường bằng tiền nhưng có giá trị quan trọng. Ví dụ: Tăng sự hài lòng của khách hàng, cải thiện hình ảnh thương hiệu, nâng cao tinh thần nhân viên, giảm rủi ro tuân thủ.
       - Trình bày lợi ích dự kiến theo từng năm trong cùng khoảng thời gian phân tích.

    **5. Phân tích Dòng tiền và các Chỉ số Tài chính (Cash Flow and Financial Metrics):**
       - Lập một bảng dòng tiền qua các năm, cho thấy sự chênh lệch giữa Lợi ích và Chi phí hàng năm.
       - Tính toán và trình bày các chỉ số tài chính quan trọng:
         - **Tỷ lệ Lợi ích/Chi phí (Benefit-Cost Ratio - BCR):** Tổng lợi ích / Tổng chi phí. (BCR > 1 là tốt).
         - **Thời gian Hoàn vốn (Payback Period - PBP):** Mất bao lâu để lợi ích tích lũy bằng với chi phí đầu tư ban đầu?
         - **Tỷ suất Hoàn vốn Đầu tư (Return on Investment - ROI):** ((Tổng lợi ích - Tổng chi phí) / Tổng chi phí) * 100%.
         - **Giá trị Hiện tại Ròng (Net Present Value - NPV):** (Tùy chọn nâng cao) - Giá trị của dòng tiền tương lai được chiết khấu về hiện tại. (NPV > 0 là tốt).

    **6. Phân tích Độ nhạy và Rủi ro (Sensitivity and Risk Analysis):**
       - Thảo luận về các yếu tố không chắc chắn có thể ảnh hưởng đến kết quả phân tích.
       - Ví dụ: "Điều gì sẽ xảy ra nếu chi phí tăng 10%?", "Điều gì sẽ xảy ra nếu lợi ích chỉ đạt 80% so với dự kiến?".

    **7. Kết luận và Khuyến nghị (Conclusion and Recommendation):**
       - Dựa trên toàn bộ phân tích, đưa ra một kết luận rõ ràng.
       - Đề xuất một khuyến nghị cụ thể: "Dựa trên phân tích, chúng tôi khuyến nghị phê duyệt dự án do ROI dự kiến là X% và thời gian hoàn vốn là Y năm, cho thấy đây là một khoản đầu tư hợp lý."
    """,
    expected_output="""Một tài liệu "Phân tích Chi phí - Lợi ích" hoàn chỉnh, có cấu trúc và thuyết phục dưới dạng Markdown.
    Tài liệu phải cung cấp một luận điểm kinh doanh rõ ràng cho dự án, được hỗ trợ bởi các phân tích chi phí, lợi ích (cả hữu hình và vô hình), và các chỉ số tài chính cụ thể.
    Kết quả phải là một công cụ ra quyết định mạnh mẽ cho các nhà tài trợ và ban lãnh đạo.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "cost_benefit_analysis", "0_estimation", "cost_benefit_analysis.md")
    )
    
    return [Preliminary_Schedule, Budget_Estimate, Cost_Benefit_Analysis]


def create_conops_tasks(initiation_agent):
    """
    Tạo nhiệm vụ xây dựng tài liệu Khái niệm Vận hành (ConOps).
    """
    system_request = shared_memory.get("phase_0", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    Concept_of_Operations = Task(
        description=f"""Soạn thảo tài liệu "Khái niệm Vận hành" (Concept of Operations - ConOps) toàn diện.
    Tài liệu này phải mô tả một cách rõ ràng và trực quan về cách thức hệ thống sẽ được sử dụng trong thực tế từ góc nhìn của người dùng cuối.
    ConOps không đi sâu vào chi tiết kỹ thuật "làm thế nào", mà tập trung vào "ai", "làm gì", "ở đâu", "khi nào" và "tại sao"
    để tạo ra một tầm nhìn chung cho tất cả các bên liên quan.

    Tài liệu ConOps cần bao gồm các phần chính sau:

    **1. Giới thiệu và Mục đích (Introduction and Purpose):**
       - Tóm tắt mục tiêu của tài liệu ConOps.
       - Mô tả phạm vi của hệ thống sẽ được đề cập.
       - Xác định đối tượng đọc chính của tài liệu (ví dụ: Ban lãnh đạo, đội phát triển, người dùng cuối).

    **2. Mô tả Bối cảnh Hiện tại (As-Is Scenario / Current State):**
       - Mô tả ngắn gọn quy trình hoặc hệ thống hiện tại mà người dùng đang sử dụng.
       - Nêu bật những khó khăn, hạn chế, hoặc các điểm yếu chính của tình trạng hiện tại mà dự án này nhằm giải quyết.

    **3. Mô tả Hệ thống Đề xuất (To-Be Scenario / Proposed System):**
       - Trình bày một tầm nhìn tổng quan về cách hệ thống mới sẽ hoạt động.
       - Mô tả cách hệ thống mới sẽ cải thiện hoặc thay thế quy trình hiện tại, giải quyết các vấn đề đã nêu ở phần "As-Is".
       - Nhấn mạnh những lợi ích chính mà người dùng và tổ chức sẽ nhận được.

    **4. Các Lớp Người dùng và Đặc điểm (User Classes and Characteristics):**
       - Xác định các nhóm người dùng khác nhau sẽ tương tác với hệ thống (ví dụ: Quản trị viên, Nhân viên Nhập liệu, Người duyệt, Khách hàng).
       - Đối với mỗi nhóm, mô tả ngắn gọn về trình độ, trách nhiệm và cách họ sẽ sử dụng hệ thống.

    **5. Các Kịch bản Vận hành Chính (Key Operational Scenarios):**
       - Đây là phần quan trọng nhất, mô tả các luồng công việc chính dưới dạng các câu chuyện (stories) hoặc kịch bản từng bước.
       - Với mỗi kịch bản, cần nêu rõ:
         - **Tên kịch bản:** (ví dụ: "Tạo một Đơn hàng Mới").
         - **Người thực hiện (Actor):** (ví dụ: "Nhân viên Bán hàng").
         - **Điều kiện tiên quyết:** (ví dụ: "Người dùng đã đăng nhập vào hệ thống").
         - **Luồng các bước chính:** Mô tả từng bước tương tác của người dùng với hệ thống để hoàn thành mục tiêu.
         - **Kết quả mong đợi:** (ví dụ: "Đơn hàng được tạo thành công và gửi thông báo xác nhận").
       - Cần bao gồm nhiều kịch bản để bao quát các chức năng cốt lõi của hệ thống.

    **6. Môi trường Vận hành (Operational Environment):**
       - Mô tả môi trường vật lý và kỹ thuật mà hệ thống sẽ hoạt động.
       - Ví dụ: Hệ thống sẽ được truy cập qua trình duyệt web trên máy tính để bàn, hay qua ứng dụng di động ngoài hiện trường? Yêu cầu về mạng, phần cứng là gì?

    **7. Các Ràng buộc và Giới hạn Vận hành (Operational Constraints and Limitations):**
       - Liệt kê các yếu tố có thể giới hạn cách thức vận hành của hệ thống.
       - Ví dụ: Các chính sách bảo mật phải tuân thủ, yêu cầu về hiệu năng (thời gian phản hồi), hoặc các hệ thống khác mà nó phải tích hợp.
    """,
    expected_output="""Một tài liệu "Khái niệm Vận hành" (ConOps) hoàn chỉnh và chi tiết dưới dạng Markdown.
    Tài liệu phải được viết rõ ràng, mạch lạc, tập trung vào góc nhìn người dùng và các kịch bản sử dụng thực tế.
    Nó phải vẽ nên một bức tranh sống động về cách hệ thống sẽ hoạt động, giúp thống nhất sự hiểu biết giữa các bên liên quan và định hướng cho việc phát triển các yêu cầu chi tiết.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "concept_of_operations", "0_conops", "concept_of_operations.md")
    )

    return [Concept_of_Operations]


def create_resourcing_tasks(initiation_agent):
    """
    Tạo các nhiệm vụ liên quan đến kế hoạch nguồn lực và định nghĩa đội ngũ.
    """
    system_request = shared_memory.get("phase_0", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    Project_Team_Definition = Task(
        Project_Team_Definition = Task(
    description=f"""Dựa trên phạm vi và các yêu cầu ban đầu của dự án,
    hãy xây dựng một tài liệu "Định nghĩa Đội ngũ Dự án" (Project Team Definition) chi tiết.
    Tài liệu này xác định rõ ràng cấu trúc nhóm, vai trò, trách nhiệm của từng thành viên,
    và cách thức họ sẽ phối hợp với nhau để đảm bảo dự án vận hành trơn tru.

    Tài liệu cần bao gồm các phần chính sau:

    **1. Sơ đồ Tổ chức Dự án (Project Organizational Chart):**
       - Trình bày một sơ đồ (hoặc mô tả bằng văn bản) cấu trúc phân cấp của đội ngũ dự án.
       - Sơ đồ cần chỉ rõ mối quan hệ báo cáo giữa các thành viên (ví dụ: Ai báo cáo cho Quản lý Dự án, Lập trình viên báo cáo cho Trưởng nhóm Kỹ thuật).

    **2. Bảng Phân công Vai trò và Trách nhiệm (Roles and Responsibilities Matrix):**
       - Lập một bảng chi tiết với các cột sau:
         - **Vai trò (Role):** Ví dụ: Quản lý Dự án, Chuyên viên Phân tích Nghiệp vụ, Trưởng nhóm Kỹ thuật, Lập trình viên, Chuyên viên QA.
         - **Tên Thành viên (Team Member Name):** (Có thể để trống nếu chưa xác định).
         - **Trách nhiệm chính (Key Responsibilities):** Liệt kê các nhiệm vụ và kết quả chính mà vai trò này chịu trách nhiệm.
         - **Quyền hạn (Authority Level):** Mô tả quyền ra quyết định (ví dụ: Phê duyệt yêu cầu thay đổi, quyết định về kỹ thuật).

    **3. Mô tả Chi tiết các Vai trò Chính (Key Role Descriptions):**
       - Đối với các vai trò cốt lõi (Quản lý Dự án, Trưởng nhóm Kỹ thuật, Chủ sản phẩm), cung cấp một mô tả ngắn gọn về:
         - Mục tiêu của vai trò.
         - Các kỹ năng và kinh nghiệm cần thiết.
         - Các đối tượng tương tác chính.

    **4. Thông tin Liên hệ của Nhóm (Team Contact List):**
       - Tạo một danh sách liên lạc đơn giản để các thành viên dễ dàng kết nối.
       - Các cột: Tên, Vai trò, Email, Số điện thoại / Kênh liên lạc chính (VD: Slack, Teams).

    **5. Quy tắc Làm việc của Nhóm (Team Working Agreements / Ground Rules):**
       - Đề xuất một số quy tắc nền tảng để thúc đẩy sự hợp tác hiệu quả, ví dụ:
         - **Kênh giao tiếp:** Giao tiếp khẩn cấp qua đâu? Giao tiếp hàng ngày qua đâu?
         - **Lịch họp:** Tần suất và thời gian các cuộc họp định kỳ (daily stand-up, họp tuần).
         - **Quy trình ra quyết định:** Ai là người ra quyết định cuối cùng cho các vấn đề kỹ thuật/nghiệp vụ?
         - **Quản lý công việc:** Công cụ sử dụng (Jira, Trello, etc.) và quy trình cập nhật trạng thái.
    """,
    expected_output="""Một tài liệu "Định nghĩa Đội ngũ Dự án" hoàn chỉnh dưới dạng Markdown.
    Tài liệu phải có cấu trúc chuyên nghiệp, xác định rõ ràng từng vai trò, trách nhiệm, sơ đồ tổ chức và các quy tắc làm việc của nhóm.
    Kết quả phải là một tài liệu tham chiếu hữu ích cho tất cả các thành viên trong suốt vòng đời dự án.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "project_team_definition", "0_resourcing", "project_team_definition.md")
    )

    Project_Resource_Plan = Task(
        description=f"""Xây dựng một "Kế hoạch Nguồn lực Dự án" (Project Resource Plan) chi tiết.
    Tài liệu này là công cụ thiết yếu để xác định, thu thập, và quản lý tất cả các nguồn lực
    cần thiết để hoàn thành dự án thành công. Kế hoạch này bao gồm không chỉ nguồn nhân lực
    mà còn cả thiết bị, vật tư, và cơ sở vật chất.

    Kế hoạch Nguồn lực Dự án cần bao gồm các phần chính sau:

    **1. Tóm tắt Nhu cầu Nguồn lực:**
       - Một đoạn giới thiệu ngắn gọn về mục đích của tài liệu và tổng quan về các loại nguồn lực chính mà dự án yêu cầu (nhân lực, thiết bị, phần mềm, v.v.).

    **2. Kế hoạch Quản lý Nguồn Nhân lực:**
       - **Danh sách Vai trò & Số lượng:** Liệt kê tất cả các vai trò cần thiết (ví dụ: Quản lý dự án, Lập trình viên, Chuyên viên QA) và số lượng yêu cầu cho mỗi vai trò.
       - **Yêu cầu về Kỹ năng & Kinh nghiệm:** Mô tả các kỹ năng cụ thể cần có cho từng vai trò chính.
       - **Lịch biểu Phân bổ (Resource Calendar/Histogram):** Phác thảo một lịch trình cho thấy khi nào và trong bao lâu mỗi nguồn lực (vai trò) sẽ cần thiết cho dự án (ví dụ: Lập trình viên Backend cần từ tháng 1-4, Chuyên viên QA cần từ tháng 3-5). Có thể trình bày dưới dạng bảng.

    **3. Kế hoạch Nguồn lực Vật chất & Thiết bị:**
       - Lập một bảng danh sách các nguồn lực không phải con người, bao gồm các cột:
         - **Loại Nguồn lực:** (ví dụ: Máy chủ, Phần mềm, Phòng họp).
         - **Tên/Mô tả cụ thể:** (ví dụ: Server Staging, Giấy phép Jira, Phòng họp A).
         - **Số lượng:**
         - **Thời gian cần thiết:** (ví dụ: Trong suốt dự án, Giai đoạn 2).
         - **Thông số kỹ thuật (nếu có):**

    **4. Chiến lược Thu thập Nguồn lực (Resource Acquisition Strategy):**
       - Mô tả cách thức dự án sẽ có được các nguồn lực đã xác định.
       - **Đối với Nhân lực:** Tuyển mới, sử dụng nhân sự nội bộ, hay thuê ngoài (outsource/freelancer)?
       - **Đối với Thiết bị/Phần mềm:** Mua mới, thuê, hay sử dụng tài sản sẵn có của công ty?

    **5. Ước tính Chi phí Nguồn lực (Resource Cost Estimation):**
       - Lập một bảng tổng hợp ước tính chi phí cho các loại nguồn lực chính. Đây là dữ liệu đầu vào quan trọng cho ngân sách tổng thể của dự án.
       - **Hạng mục:** (ví dụ: Chi phí Nhân sự, Chi phí Phần cứng, Chi phí Phần mềm).
       - **Ước tính Chi phí:**

    **6. Quản lý và Kiểm soát Nguồn lực:**
       - Mô tả ngắn gọn quy trình theo dõi việc sử dụng nguồn lực.
       - Ai chịu trách nhiệm quản lý và phân bổ nguồn lực? (Thường là Quản lý Dự án).
       - Cách giải quyết khi có xung đột hoặc thiếu hụt nguồn lực.
    """,
    expected_output="""Một tài liệu "Kế hoạch Nguồn lực Dự án" hoàn chỉnh và chi tiết dưới dạng Markdown.
    Tài liệu phải cung cấp một cái nhìn toàn diện về tất cả các nguồn lực cần thiết (con người, vật chất),
    bao gồm số lượng, thời gian, chi phí ước tính, và chiến lược để có được chúng.
    Đây phải là một kế hoạch có tính thực thi, làm cơ sở cho việc quản lý ngân sách và tiến độ dự án.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "project_resource_plan", "0_resourcing", "project_resource_plan.md")
    )

    return [Project_Team_Definition, Project_Resource_Plan]


def create_risk_tasks(initiation_agent):
    """
    Tạo các nhiệm vụ liên quan đến quản lý rủi ro và checklist khởi tạo.
    """
    system_request = shared_memory.get("phase_0", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    Risk_Assessment_Document = Task(
    description=f"""Thực hiện một quy trình Đánh giá Rủi ro bài bản và soạn thảo "Tài liệu Đánh giá Rủi ro" (Risk Assessment Document) chi tiết.
    Tài liệu này sẽ xác định, phân tích, và ưu tiên hóa các rủi ro tiềm ẩn có thể ảnh hưởng tiêu cực đến mục tiêu dự án (về phạm vi, tiến độ, ngân sách, và chất lượng).
    Mục tiêu là tạo ra một kế hoạch hành động để quản lý các rủi ro này một cách chủ động.

    Tài liệu Đánh giá Rủi ro cần bao gồm các phần chính sau:

    **1. Giới thiệu và Mục đích:**
       - Tóm tắt mục tiêu của tài liệu.
       - Mô tả ngắn gọn về phạm vi của việc đánh giá rủi ro (toàn bộ dự án, hay một giai đoạn cụ thể).

    **2. Phương pháp luận Đánh giá Rủi ro (Risk Assessment Methodology):**
       - **Cách nhận diện rủi ro:** (ví dụ: Brainstorming với đội ngũ, phỏng vấn chuyên gia, phân tích tài liệu, checklist).
       - **Thang đo Xác suất (Probability Scale):** Định nghĩa các mức độ xác suất xảy ra rủi ro (ví dụ: 1-Thấp, 2-Trung bình, 3-Cao).
       - **Thang đo Mức độ Ảnh hưởng (Impact Scale):** Định nghĩa các mức độ ảnh hưởng nếu rủi ro xảy ra, xét trên các khía cạnh như Chi phí, Tiến độ, Chất lượng (ví dụ: 1-Thấp, 2-Trung bình, 3-Cao).
       - **Ma trận Rủi ro (Risk Matrix):** Mô tả ma trận kết hợp giữa Xác suất và Ảnh hưởng để tính ra Mức độ Rủi ro tổng thể (ví dụ: Thấp, Trung bình, Cao, Nghiêm trọng).

    **3. Sổ Đăng ký Rủi ro (Risk Register):**
       - Đây là phần cốt lõi, trình bày dưới dạng một bảng chi tiết với các cột:
         - **ID Rủi ro:** Mã định danh duy nhất.
         - **Mô tả Rủi ro:** Mô tả rõ ràng về rủi ro theo cấu trúc "Nguyên nhân -> Sự kiện -> Hậu quả".
         - **Loại Rủi ro:** (ví dụ: Kỹ thuật, Nhân sự, Tài chính, Bên ngoài).
         - **Xác suất (P):** (Cao / Trung bình / Thấp).
         - **Ảnh hưởng (I):** (Cao / Trung bình / Thấp).
         - **Mức độ Rủi ro (P x I):** Mức độ ưu tiên (Nghiêm trọng / Cao / Trung bình / Thấp).
         - **Người chịu trách nhiệm (Risk Owner):** Ai là người theo dõi và quản lý rủi ro này?
         - **Kế hoạch Ứng phó (Response Plan):** Hành động cụ thể để (Né tránh, Giảm thiểu, Chuyển giao, hoặc Chấp nhận) rủi ro.
         - **Trạng thái:** (ví dụ: Mới, Đang xử lý, Đã đóng).

    **4. Phân tích các Rủi ro Hàng đầu (Top Risks Analysis):**
       - Liệt kê và phân tích sâu hơn về 5-10 rủi ro có Mức độ Rủi ro cao nhất (Nghiêm trọng/Cao).
       - Mô tả chi tiết hơn về kế hoạch ứng phó và các hành động cụ thể cần thực hiện ngay lập tức cho những rủi ro này.

    **5. Kế hoạch Giám sát và Báo cáo Rủi ro:**
       - Mô tả tần suất và cách thức đội ngũ sẽ rà soát lại sổ đăng ký rủi ro (ví dụ: Trong các cuộc họp dự án hàng tuần).
       - Quy trình để bất kỳ ai cũng có thể báo cáo một rủi ro mới.
    """,
    expected_output="""Một "Tài liệu Đánh giá Rủi ro" hoàn chỉnh và có cấu trúc dưới dạng Markdown.
    Tài liệu phải bao gồm cả phương pháp luận được sử dụng và một Sổ Đăng ký Rủi ro (Risk Register) chi tiết.
    Kết quả phải là một công cụ quản lý hữu ích, giúp Quản lý Dự án và đội ngũ có thể ra quyết định một cách chủ động để giảm thiểu các tác động tiêu cực đến dự án.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "risk_assessment_document", "0_risk", "risk_assessment_document.md")
    )

    Initiate_Project_Checklist = Task(
    description=f"""Thiết kế một "Danh mục Kiểm tra Khởi tạo Dự án" (Project Initiation Checklist) toàn diện và mang tính thực tiễn.
    Danh mục này hoạt động như một công cụ đảm bảo chất lượng, giúp Quản lý Dự án và Nhà tài trợ xác nhận rằng tất cả các bước cần thiết đã được hoàn thành
    và dự án có một nền tảng vững chắc trước khi chính thức bắt đầu giai đoạn Lập kế hoạch.

    Danh mục kiểm tra cần được tổ chức theo các nhóm logic, với các hạng mục có thể đánh dấu đã hoàn thành.

    **1. Nhóm A: Nền tảng & Phê duyệt (Foundation & Authorization)**
       - [ ] Xác định và thống nhất Vấn đề/Cơ hội kinh doanh.
       - [ ] Soạn thảo và được phê duyệt "Biểu mẫu Đề xuất Dự án" (Project Submission Form).
       - [ ] Soạn thảo và được ký duyệt "Hiến chương Dự án" (Project Charter).
       - [ ] Xác nhận chính thức Nhà tài trợ Dự án (Project Sponsor).
       - [ ] Bổ nhiệm chính thức Quản lý Dự án (Project Manager).

    **2. Nhóm B: Phạm vi & Yêu cầu Cấp cao (Scope & High-Level Requirements)**
       - [ ] Tổ chức buổi họp để xác định các mục tiêu SMART.
       - [ ] Định nghĩa phạm vi cấp cao (High-level In-Scope / Out-of-Scope).
       - [ ] Liệt kê các sản phẩm bàn giao chính (Key Deliverables).
       - [ ] Xây dựng tài liệu "Khái niệm Vận hành" (Concept of Operations - ConOps).

    **3. Nhóm C: Các Bên liên quan & Đội ngũ (Stakeholders & Team)**
       - [ ] Thực hiện "Phân tích các Bên liên quan" và tạo "Sổ Đăng ký các Bên liên quan".
       - [ ] Xây dựng tài liệu "Định nghĩa Đội ngũ Dự án" (Project Team Definition) sơ bộ.
       - [ ] Xác định các vai trò và trách nhiệm chính trong đội ngũ.

    **4. Nhóm D: Kế hoạch Sơ bộ & Rủi ro (Initial Planning & Risks)**
       - [ ] Xây dựng "Kế hoạch Nguồn lực Dự án" (Project Resource Plan) cấp cao.
       - [ ] Lập tiến độ các cột mốc chính (Summary Milestone Schedule).
       - [ ] Ước tính ngân sách sơ bộ (Summary Budget).
       - [ ] Thực hiện đánh giá ban đầu và tạo "Tài liệu Đánh giá Rủi ro" (Risk Assessment Document).

    **5. Nhóm E: Thiết lập & Truyền thông (Setup & Communication)**
       - [ ] Lên kế hoạch và lịch cho buổi họp Khởi động Dự án (Project Kick-off Meeting).
       - [ ] Thiết lập không gian làm việc chung (ví dụ: thư mục trên Google Drive/SharePoint, kênh Slack/Teams).
       - [ ] Thiết lập công cụ quản lý dự án (ví dụ: tạo project trên Jira/Trello).
       - [ ] Soạn thảo kế hoạch truyền thông ban đầu (ai cần biết gì, khi nào, bằng cách nào).

    **6. Phần Phê duyệt Chuyển giai đoạn (Phase Gate Approval)**
       - Mục này dành cho chữ ký xác nhận của các bên chủ chốt để chính thức kết thúc giai đoạn Khởi tạo và chuyển sang giai đoạn Lập kế hoạch.
       - Quản lý Dự án: [Chữ ký / Ngày]
       - Nhà tài trợ Dự án: [Chữ ký / Ngày]
    """,
    expected_output="""Một "Danh mục Kiểm tra Khởi tạo Dự án" hoàn chỉnh dưới dạng Markdown.
    Tài liệu phải là một checklist có thể sử dụng ngay lập tức, được phân chia thành các nhóm logic rõ ràng.
    Mỗi mục trong checklist phải là một hành động hoặc một tài liệu cần hoàn thành, có ô đánh dấu [ ] để theo dõi trạng thái.
    Kết quả phải là một công cụ thực tiễn giúp đảm bảo không bỏ sót bất kỳ hoạt động quan trọng nào trong giai đoạn khởi tạo.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "initiate_project_checklist", "0_risk", "initiate_project_checklist.md")
    )

    return [Risk_Assessment_Document, Initiate_Project_Checklist]


def create_stakeholder_tasks(initiation_agent):
    """
    Tạo các nhiệm vụ liên quan đến quản lý các bên liên quan.
    """
    system_request = shared_memory.get("phase_0", "system_request") or "Thông tin yêu cầu hệ thống bị thiếu."

    description=f"""Dựa trên Yêu Cầu Hệ Thống ({system_request}) và mục tiêu chung của dự án, 
    hãy xác định và lập một Danh sách các Bên liên quan (Stakeholder Register) chi tiết.
    Tài liệu này là cơ sở quan trọng để xây dựng kế hoạch quản lý và giao tiếp hiệu quả 
    với các bên liên quan trong suốt vòng đời dự án.

    Danh sách các bên liên quan cần được trình bày dưới dạng bảng Markdown với các cột thông tin chi tiết sau:
    1.  **Tên / Nhóm Bên Liên Quan:** Tên cá nhân hoặc phòng ban, tổ chức.
    2.  **Vai trò trong Dự án:** Chức vụ hoặc vai trò cụ thể của họ liên quan đến dự án (ví dụ: Nhà tài trợ, Người dùng cuối, Quản lý Kỹ thuật).
    3.  **Mối Quan Tâm & Kỳ Vọng Chính:** Những gì họ mong đợi từ dự án, những mối quan tâm chính của họ là gì?
    4.  **Mức độ Ảnh hưởng (Influence):** Khả năng tác động đến các quyết định và kết quả của dự án (Cao / Trung bình / Thấp).
    5.  **Mức độ Quan tâm (Interest):** Mức độ họ bị ảnh hưởng bởi hoặc quan tâm đến kết quả của dự án (Cao / Trung bình / Thấp).
    6.  **Phân loại:** Phân loại bên liên quan (ví dụ: Nội bộ, Bên ngoài, Nhà tài trợ, Cơ quan quản lý, Đội dự án).
    7.  **Chiến lược Tương tác Sơ bộ:** Cách tiếp cận ban đầu để quản lý mối quan hệ (ví dụ: Quản lý chặt chẽ, Giữ hài lòng, Cung cấp thông tin, Giám sát).
    """,
    expected_output="Một tài liệu Danh sách các Bên liên quan (Stakeholder Register) hoàn chỉnh dưới dạng Markdown, được trình bày dưới dạng bảng. Tài liệu phải xác định rõ ràng các bên liên quan, phân tích sơ bộ mức độ ảnh hưởng/quan tâm của họ và đề xuất chiến lược tương tác ban đầu.",
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "stakeholder_list", "0_stakeholder", "stakeholder_list.md")
    )
   
    Stakeholder_Analysis = Task(
        description=f"""Dựa trên Yêu Cầu Hệ Thống ({system_request}) và mục tiêu chung của dự án,
    hãy thực hiện một Phân tích các Bên liên quan (Stakeholder Analysis) toàn diện.
    Tài liệu này sẽ là kim chỉ nam chiến lược cho việc quản lý giao tiếp và sự tham gia của các bên liên quan.

    Tài liệu phân tích cần bao gồm các phần chính sau:

    **1. Bảng Đăng ký các Bên liên quan (Stakeholder Register):**
    Lập một bảng chi tiết xác định tất cả các bên liên quan với các cột:
    - Tên / Nhóm Bên Liên Quan
    - Vai trò trong Dự án
    - Mối Quan Tâm & Kỳ Vọng Chính
    - Mức độ Ảnh hưởng (Influence): (Cao / Trung bình / Thấp)
    - Mức độ Quan tâm (Interest): (Cao / Trung bình / Thấp)

    **2. Ma trận Ảnh hưởng/Quan tâm (Power/Interest Grid):**
    - Dựa trên bảng ở trên, hãy vẽ hoặc mô tả một ma trận phân loại các bên liên quan vào 4 nhóm chiến lược:
        - **Quản lý chặt chẽ (Manage Closely):** Ảnh hưởng cao, Quan tâm cao.
        - **Giữ hài lòng (Keep Satisfied):** Ảnh hưởng cao, Quan tâm thấp.
        - **Cung cấp thông tin (Keep Informed):** Ảnh hưởng thấp, Quan tâm cao.
        - **Giám sát (Monitor):** Ảnh hưởng thấp, Quan tâm thấp.
    - Liệt kê các bên liên quan thuộc mỗi nhóm.

    **3. Chiến lược Tương tác Chi tiết (Detailed Engagement Strategies):**
    - Từ kết quả phân tích trên ma trận, hãy đề xuất các chiến lược tương tác cụ thể cho từng nhóm:
        - Mô tả cách thức và tần suất giao tiếp cho nhóm "Quản lý chặt chẽ".
        - Mô tả cách giữ cho nhóm "Giữ hài lòng" không cản trở dự án.
        - Mô tả các kênh thông tin sẽ sử dụng cho nhóm "Cung cấp thông tin".
        - Mô tả cách giám sát nhóm "Giám sát" với nỗ lực tối thiểu.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "stakeholder_analysis", "0_stakeholder", "stakeholder_analysis.md")
    )

    Project_Submission_Form = Task(
        description=f"""Xây dựng một Biểu mẫu Đề xuất Dự án (Project Submission Form) toàn diện và chuyên nghiệp.
    Biểu mẫu này là tài liệu khởi đầu chính thức, được sử dụng để trình bày ý tưởng dự án,
    phác thảo các thông tin cốt lõi và tìm kiếm sự phê duyệt từ ban lãnh đạo hoặc nhà tài trợ.

    Biểu mẫu cần được cấu trúc một cách logic để người đề xuất có thể điền thông tin dễ dàng
    và người duyệt có thể nhanh chóng nắm bắt được bản chất của dự án.

    Biểu mẫu Đề xuất Dự án cần bao gồm các mục sau:

    **1. Thông tin chung về Dự án:**
       - Tên dự án:
       - Người đề xuất / Chủ dự án:
       - Phòng ban:
       - Ngày đề xuất:

    **2. Tóm tắt (Executive Summary):**
       - Một đoạn văn ngắn gọn (3-5 câu) mô tả tổng quan về dự án, vấn đề cần giải quyết, giải pháp đề xuất và kết quả mong đợi.

    **3. Vấn đề & Cơ hội Kinh doanh (Problem & Business Opportunity):**
       - Mô tả chi tiết vấn đề hiện tại mà dự án nhắm tới để giải quyết.
       - Hoặc, mô tả cơ hội kinh doanh mà dự án sẽ tận dụng.
       - Cung cấp dữ liệu hoặc bằng chứng (nếu có) để chứng minh sự cần thiết của dự án.

    **4. Mục tiêu Dự án (Project Goals):**
       - Liệt kê các mục tiêu cụ thể, đo lường được, khả thi, liên quan và có thời hạn (SMART).
       - Ví dụ: "Giảm 15% chi phí vận hành kho trong vòng 6 tháng."

    **5. Phạm vi Dự án (Project Scope):**
       - **Trong phạm vi (In-Scope):** Liệt kê rõ ràng các công việc, chức năng, sản phẩm chính sẽ được thực hiện.
       - **Ngoài phạm vi (Out-of-Scope):** Liệt kê những gì dự án sẽ KHÔNG thực hiện để tránh hiểu lầm và "scope creep".

    **6. Sản phẩm Bàn giao chính (Key Deliverables):**
       - Danh sách các kết quả, sản phẩm hữu hình hoặc vô hình sẽ được tạo ra khi dự án hoàn thành (ví dụ: phần mềm, báo cáo, quy trình mới).

    **7. Các Bên liên quan chính (Key Stakeholders):**
       - Liệt kê các cá nhân hoặc nhóm chính sẽ bị ảnh hưởng hoặc có ảnh hưởng đến dự án (ví dụ: Ban giám đốc, Trưởng phòng Marketing, Đội ngũ IT, Khách hàng).

    **8. Dự toán Ngân sách & Nguồn lực (Estimated Budget & Resources):**
       - Ước tính chi phí chính (nhân sự, thiết bị, phần mềm...).
       - Nguồn lực cần thiết (số lượng nhân sự, kỹ năng yêu cầu...).

    **9. Tiến độ Dự kiến & Các Cột mốc quan trọng (Proposed Timeline & Milestones):**
       - Phác thảo một dòng thời gian cấp cao cho dự án.
       - Xác định các cột mốc quan trọng (milestones) và ngày dự kiến hoàn thành.

    **10. Rủi ro, Giả định và Phụ thuộc (Risks, Assumptions, and Dependencies):**
        - **Rủi ro:** Liệt kê các rủi ro tiềm ẩn có thể ảnh hưởng đến dự án.
        - **Giả định:** Những điều được cho là đúng để kế hoạch dự án có thể thực hiện.
        - **Phụ thuộc:** Các yếu tố bên ngoài hoặc dự án khác mà dự án này phụ thuộc vào.

    **11. Thước đo Thành công (Success Metrics/KPIs):**
        - Làm thế nào để biết dự án thành công? Liệt kê các chỉ số hiệu suất chính (KPIs) sẽ được sử dụng để đo lường.

    **12. Phần Phê duyệt (Approval Section):**
        - Chừa không gian cho chữ ký của Nhà tài trợ dự án (Project Sponsor), Chủ dự án, và các bên phê duyệt liên quan.
    """,
    expected_output="""Một tài liệu mẫu (template) 'Biểu mẫu Đề xuất Dự án' hoàn chỉnh dưới dạng Markdown.
    Tài liệu phải có cấu trúc rõ ràng, chuyên nghiệp, bao gồm đầy đủ 12 mục đã nêu trong phần mô tả.
    Mỗi mục cần có tiêu đề, một mô tả ngắn gọn về nội dung cần điền, và các trường thông tin trống để người dùng có thể sử dụng ngay lập tức.
    """,
        agent=initiation_agent,
        callback=lambda output: _save_task_output(output, "phase_0", "project_submission_form", "0_stakeholder", "project_submission_form.md")
    )
    
    return [Project_Submission_Form, Stakeholder_List, Stakeholder_Analysis]