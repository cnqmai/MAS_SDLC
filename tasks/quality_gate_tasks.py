# tasks/quality_gate_tasks.py

from crewai import Task
from utils.file_writer import write_output
from memory.shared_memory import shared_memory

def create_quality_gate_task(project_manager_agent, phase_name: str, previous_tasks_output_key: str, description_suffix: str = ""):
    """
    Tạo một task cổng chất lượng (quality gate) cho một giai đoạn cụ thể.
    Task này sẽ yêu cầu Project Manager agent đánh giá đầu ra của giai đoạn trước đó.

    Args:
        project_manager_agent: Instance của Project Manager Agent.
        phase_name (str): Tên của giai đoạn hiện tại (ví dụ: "Phase 0: Initiation").
        previous_tasks_output_key (str): Key trong shared_memory chứa tổng hợp output của các tasks trước.
        description_suffix (str): Một chuỗi mô tả thêm cho task (ví dụ: các tài liệu cần kiểm tra).
    """
    # Lấy output từ các task trước của phase hiện tại
    outputs_to_validate = shared_memory.get(phase_name.replace(" ", "_").lower(), previous_tasks_output_key)
    if not outputs_to_validate:
        outputs_to_validate = "Không có tài liệu nào để kiểm tra từ các task trước trong giai đoạn này."

    return Task(
        description=(
            f"Với vai trò Project Manager, hãy xem xét kỹ lưỡng tất cả các đầu ra chính "
            f"của {phase_name}. Đảm bảo rằng chúng tuân thủ các tiêu chuẩn chất lượng, "
            f"phạm vi dự án, và các yêu cầu đã định. Cụ thể, kiểm tra:\n"
            f"- Tính đầy đủ và rõ ràng của tài liệu.\n"
            f"- Tính nhất quán với mục tiêu và yêu cầu dự án.\n"
            f"- Đảm bảo không có sai sót hoặc thiếu sót lớn.\n\n"
            f"Dựa trên các tài liệu sau:\n---\n{outputs_to_validate}\n---\n\n"
            f"Nếu có, hãy đặc biệt chú ý đến: {description_suffix}\n\n"
            f"Viết một báo cáo phê duyệt (validation report) chi tiết."
        ),
        expected_output=f"Báo cáo phê duyệt 'validation_report_{phase_name.replace(' ', '_').lower()}.md' bằng tiếng Việt, "
                        f"phân tích chất lượng, nêu rõ các điểm cần cải thiện (nếu có) và xác nhận sự phê duyệt.",
        agent=project_manager_agent,
        callback=lambda output: (
            print(f"--- Hoàn thành Quality Gate Task cho {phase_name} ---"),
            write_output(f"output/{phase_name.split(':')[0].strip().replace('Phase ', '').replace(' ', '_').lower()}/validation_report_{phase_name.replace(' ', '_').lower().replace('phase_', '')}.md", str(output)),
            shared_memory.set(phase_name.replace(" ", "_").lower(), f"validation_report", str(output))
        )
    )