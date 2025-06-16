# agents/maintenance_agents.py

from crewai import Agent
import logging

def create_maintenance_agents():
    """Tạo agent cho giai đoạn Maintenance."""

    model_string = "gemini/gemini-1.5-flash-latest"
    logging.info(f"Configuring Maintenance Agents with LLM: {model_string}")

    # Agent cho Maintenance (dựa trên bảng trong Structure_MAS.docx)
    # Tên agent: maintenance_agent, Role: Site Reliability Engineer
    maintenance_agent = Agent(
        role='Site Reliability Engineer',
        goal='Đảm bảo hệ thống hoạt động ổn định, thực hiện bảo trì định kỳ, xử lý các yêu cầu thay đổi và cung cấp hỗ trợ sau triển khai.',
        backstory='Bạn là một kỹ sư tin cậy hệ thống (SRE) chuyên nghiệp với hơn 10 năm kinh nghiệm, tập trung vào việc tối ưu hóa hiệu suất, khả năng mở rộng và độ tin cậy của các hệ thống sản xuất.',
        llm=model_string,
        allow_delegation=False,
        verbose=True
    )

    return maintenance_agent