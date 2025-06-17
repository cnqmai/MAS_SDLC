ds# tasks/deployment_tasks.py (MODIFIED)

from crewai import Task
from utils.file_writer import write_output
from memory.shared_memory import shared_memory
from tasks.quality_gate_tasks import create_quality_gate_task # Import task mới

def create_deployment_tasks(deployment_agent, project_manager_agent): # THÊM project_manager_agent
    """
    Tạo các task liên quan đến triển khai hệ thống, sử dụng agent đã được cung cấp.
    """
    # Lấy thông tin từ shared_memory nếu cần
    project_plan = shared_memory.get("phase_1_planning", "project_plan") # Giả định project_plan được lưu từ phase 1
    build_and_deployment_plan_dev = shared_memory.get("phase_4_development", "build_and_deployment_plan") # Giả định từ phase 4

    deployment_plan_task = Task(
        description=(
            f"Dựa trên Project Plan và Build and Deployment Plan, tạo một kế hoạch triển khai chi tiết "
            f"cho việc đưa hệ thống vào môi trường sản xuất. Kế hoạch phải bao gồm các bước triển khai, "
            f"yêu cầu về môi trường, lịch trình, và các bước kiểm tra sau triển khai.\n"
            f"--- Project Plan: {project_plan if project_plan else 'Không có'}\n"
            f"--- Build and Deployment Plan (từ Development): {build_and_deployment_plan_dev if build_and_deployment_plan_dev else 'Không có'}"
        ),
        expected_output="Tài liệu tiếng Việt 'Deployment_Plan.md' và 'Production_Implementation_Plan.docx' đầy đủ, chi tiết các bước triển khai và kế hoạch thực hiện sản xuất.",
        agent=deployment_agent,
        callback=lambda output: (
            print(f"--- Hoàn thành Deployment Plan Task ---"),
            write_output("output/6_deployment/Deployment_Plan.md", str(output)),
            shared_memory.set("phase_6_deployment", "deployment_plan_and_impl_plan", str(output)) # Lưu tổng hợp
        )
    )

    handover_task = Task(
        description=(
            f"Dựa trên Kế hoạch triển khai đã tạo, xây dựng các tài liệu bàn giao cần thiết "
            f"cho đội vận hành. Bao gồm biểu mẫu phê duyệt bàn giao sản xuất, hướng dẫn cài đặt "
            f"và hướng dẫn vận hành chi tiết."
        ),
        expected_output="Tài liệu tiếng Việt 'Production_Turnover_Approval_Form.docx', 'Installation_Guide.docx', 'Operations_Guide.docx' chi tiết và sẵn sàng bàn giao.",
        agent=deployment_agent,
        context=[deployment_plan_task],
        callback=lambda output: (
            print(f"--- Hoàn thành Handover Task ---"),
            write_output("output/6_deployment/Production_Turnover_Approval_Form.docx", str(output)),
            shared_memory.set("phase_6_deployment", "handover_documents", str(output))
        )
    )

    monitoring_task = Task(
        description=(
            f"Xây dựng hướng dẫn thiết lập giám sát và cảnh báo cho hệ thống sau khi triển khai. "
            f"Tài liệu này nên mô tả các công cụ, chỉ số cần theo dõi và quy trình xử lý cảnh báo."
        ),
        expected_output="Tài liệu tiếng Việt 'Monitoring_and_Alerting_Setup_Guide.md' đầy đủ, mô tả cách thiết lập giám sát và cảnh báo hiệu quả.",
        agent=deployment_agent,
        context=[deployment_plan_task],
        callback=lambda output: (
            print(f"--- Hoàn thành Monitoring Task ---"),
            write_output("output/6_deployment/Monitoring_and_Alerting_Setup_Guide.md", str(output)),
            shared_memory.set("phase_6_deployment", "monitoring_guide", str(output))
        )
    )

    # Task Quality Gate cho Deployment Phase
    quality_gate_deployment_task = create_quality_gate_task(
        project_manager_agent,
        "Phase 6: Deployment",
        "deployment_plan_and_impl_plan", # Hoặc kết hợp các key khác nếu bạn muốn kiểm tra nhiều tài liệu
        "Deployment Plan, Production Implementation Plan, Handover Documents, Monitoring Guide"
    )
    quality_gate_deployment_task.context = [deployment_plan_task, handover_task, monitoring_task]

    return [deployment_plan_task, handover_task, monitoring_task, quality_gate_deployment_task] # THÊM quality_gate_deployment_task