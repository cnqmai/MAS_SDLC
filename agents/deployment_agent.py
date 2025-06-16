# agents/deployment_agents.py

from crewai import Agent
import logging

def create_deployment_agents():
    """Tạo agent cho giai đoạn Deployment."""

    model_string = "gemini/gemini-1.5-flash-latest"
    logging.info(f"Configuring Deployment Agents with LLM: {model_string}")

    # Agent cho Deployment (dựa trên bảng trong Structure_MAS.docx)
    # Tên agent: deployment_agent, Role: DevOps Engineer
    deployment_agent = Agent(
        role='DevOps Engineer',
        goal='Tạo kế hoạch triển khai, tài liệu bàn giao sản phẩm và thiết lập giám sát hệ thống.',
        backstory='Bạn là một kỹ sư DevOps giàu kinh nghiệm với hơn 10 năm trong việc tự động hóa và quản lý các quy trình triển khai phần mềm, đảm bảo hệ thống vận hành ổn định và hiệu quả sau khi Go-Live.',
        llm=model_string,
        allow_delegation=False,
        verbose=True
    )

    return deployment_agent