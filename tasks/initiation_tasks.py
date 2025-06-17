# Bên trong tasks/initiation_tasks.py (MODIFIED)

from crewai import Task
from utils.file_writer import write_output
from memory.shared_memory import shared_memory
from tasks.quality_gate_tasks import create_quality_gate_task # Import task mới

def create_initiation_tasks(vision_agent, conops_agent, charter_agent, project_manager_agent): # THÊM project_manager_agent
    """
    Tạo các task liên quan đến khởi tạo dự án, sử dụng các agent đã được cung cấp.
    """
    system_request = shared_memory.get("phase_0", "system_request")
    if not system_request:
        print("Lỗi: Không tìm thấy 'system_request' trong shared_memory['phase_0']")
        system_request = "Thông tin yêu cầu hệ thống bị thiếu."

    vision_task = Task(
        description=f"Phân tích System Request sau và tạo Vision Document chi tiết:\n---\n{system_request}\n---",
        expected_output="Tài liệu tiếng Việt Vision Document đầy đủ, bao gồm scope, objectives, và strategic alignment.",
        agent=vision_agent,
        callback=lambda output: (
            print(f"--- Hoàn thành Vision Task ---"),
            write_output("output/1_initiation/vision_document.txt", str(output)),
            shared_memory.set("phase_0", "vision_document", str(output)) # Lưu vào phase_0
        )
    )

    conops_task = Task(
        description=f"Nghiên cứu System Request và Vision Document (nếu có trong context) để tạo Concept of Operations đầy đủ:\n---\n{system_request}\n---",
        expected_output="Tài liệu tiếng Việt Concept of Operations đầy đủ, mô tả cách thức vận hành của hệ thống.",
        agent=conops_agent,
        context=[vision_task],
        callback=lambda output: (
            print(f"--- Hoàn thành ConOps Task ---"),
            write_output("output/1_initiation/conops.txt", str(output)),
            shared_memory.set("phase_0", "conops", str(output)) # Lưu vào phase_0
        )
    )

    charter_task = Task(
        description=f"Dựa trên System Request, Vision Document và ConOps (nếu có trong context), xây dựng Project Charter đầy đủ:\n---\n{system_request}\n---",
        expected_output="Tài liệu tiếng Việt Project Charter đầy đủ, xác định rõ mục tiêu dự án, phạm vi, các bên liên quan và quyền hạn.",
        agent=charter_agent,
        context=[vision_task, conops_task],
        callback=lambda output: (
            print(f"--- Hoàn thành Charter Task ---"),
            write_output("output/1_initiation/project_charter.txt", str(output)),
            shared_memory.set("phase_0", "project_charter", str(output)) # Lưu vào phase_0
        )
    )

    # Task Quality Gate cho Initiation Phase
    quality_gate_initiation_task = create_quality_gate_task(
        project_manager_agent,
        "Phase 0: Initiation",
        "project_charter", # Giả định project_charter là output quan trọng nhất để kiểm tra
        "Project Charter, Vision Document và Concept of Operations"
    )
    quality_gate_initiation_task.context = [vision_task, conops_task, charter_task] # Đảm bảo agent có context của các task đã tạo ra

    return [vision_task, conops_task, charter_task, quality_gate_initiation_task] # THÊM quality_gate_initiation_task