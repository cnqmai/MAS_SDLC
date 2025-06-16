# tasks/maintenance_tasks.py (MODIFIED)

from crewai import Task
from utils.file_writer import write_output
from memory.shared_memory import shared_memory
from tasks.quality_gate_tasks import create_quality_gate_task # Import task mới

def create_maintenance_tasks(maintenance_agent, project_manager_agent): # THÊM project_manager_agent
    """
    Tạo các task liên quan đến bảo trì hệ thống, sử dụng agent đã được cung cấp.
    """
    sla_document = shared_memory.get("phase_2_requirements", "service_level_agreement_template") # Giả định SLA được lưu từ phase 2
    deployment_plan_for_maintenance = shared_memory.get("phase_6_deployment", "deployment_plan_and_impl_plan") # Lấy từ phase 6

    maintenance_plan_task = Task(
        description=(
            f"Dựa trên tài liệu SLA và kế hoạch triển khai, phát triển một kế hoạch bảo trì và hỗ trợ toàn diện. "
            f"Kế hoạch này phải bao gồm lịch trình bảo trì định kỳ, chính sách SLA và bảo hành, "
            f"và hướng dẫn quản lý bản vá.\n"
            f"--- SLA Document: {sla_document if sla_document else 'Không có'}\n"
            f"--- Deployment Plan (từ Phase 6): {deployment_plan_for_maintenance if deployment_plan_for_maintenance else 'Không có'}"
        ),
        expected_output="Tài liệu tiếng Việt 'Maintenance_and_Support_Plan.docx', 'Maintenance_Checklist.md', 'SLA_and_Warranty_Policies.docx', 'Patch_Management_Guide.md' đầy đủ.",
        agent=maintenance_agent,
        callback=lambda output: (
            print(f"--- Hoàn thành Maintenance Plan Task ---"),
            write_output("output/7_maintenance/Maintenance_and_Support_Plan.docx", str(output)),
            shared_memory.set("phase_7_maintenance", "maintenance_plan", str(output))
        )
    )

    feedback_review_task = Task(
        description=(
            f"Tiến hành xem xét và tổng hợp phản hồi sau dự án. "
            f"Tạo các tài liệu về bài học kinh nghiệm và báo cáo đánh giá sau dự án."
        ),
        expected_output="Tài liệu tiếng Việt 'Post_Project_Survey_Questionnaire.docx', 'Lessons_Learned.md', 'Post_Project_Review.docx' ghi nhận phản hồi và bài học.",
        agent=maintenance_agent,
        callback=lambda output: (
            print(f"--- Hoàn thành Feedback Review Task ---"),
            write_output("output/7_maintenance/Lessons_Learned.md", str(output)),
            shared_memory.set("phase_7_maintenance", "lessons_learned", str(output))
        )
    )

    transition_task = Task(
        description=(
            f"Phát triển các tài liệu liên quan đến yêu cầu thay đổi, kế hoạch chuyển giao (nếu có) "
            f"và kế hoạch ngừng sản phẩm."
        ),
        expected_output="Tài liệu tiếng Việt 'Change_Request_Document_(CCR)_Template.docx', 'Transition_Out_Plan.docx', 'Product_Retirement_Plan.docx' đầy đủ.",
        agent=maintenance_agent,
        callback=lambda output: (
            print(f"--- Hoàn thành Transition Task ---"),
            write_output("output/7_maintenance/Change_Request_Document_CCR_Template.docx", str(output)),
            shared_memory.set("phase_7_maintenance", "transition_plan", str(output))
        )
    )

    support_knowledge_task = Task(
        description=(
            f"Tạo các tài liệu chuyển giao kiến thức cho nhà phát triển và tổng hợp hỗ trợ ứng dụng toàn cầu. "
            f"Dựa trên tài liệu mã nguồn và tài liệu thiết kế API."
        ),
        expected_output="Tài liệu tiếng Việt 'Developer_Knowledge_Transfer_Report.md', 'Global_Application_Support_Summary.md' phục vụ chuyển giao kiến thức và hỗ trợ.",
        agent=maintenance_agent,
        callback=lambda output: (
            print(f"--- Hoàn thành Support Knowledge Task ---"),
            write_output("output/7_maintenance/Developer_Knowledge_Transfer_Report.md", str(output)),
            shared_memory.set("phase_7_maintenance", "knowledge_transfer", str(output))
        )
    )

    # Task Quality Gate cho Maintenance Phase
    quality_gate_maintenance_task = create_quality_gate_task(
        project_manager_agent,
        "Phase 7: Maintenance",
        "maintenance_plan", # Hoặc kết hợp các key khác
        "Maintenance and Support Plan, Lessons Learned, Transition Plans, Knowledge Transfer Reports"
    )
    quality_gate_maintenance_task.context = [maintenance_plan_task, feedback_review_task, transition_task, support_knowledge_task]

    return [maintenance_plan_task, feedback_review_task, transition_task, support_knowledge_task, quality_gate_maintenance_task] # THÊM quality_gate_maintenance_task