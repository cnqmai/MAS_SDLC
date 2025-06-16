from crewai import Agent
def create_input_agent():
    model_string = "gemini/gemini-1.5-flash-latest"

    input_agent = Agent(
        role="Chuyên Gia Phân Tích Nghiệp Vụ (Business Analyst)",
        goal="Thực hiện một cuộc phỏng vấn chi tiết với khách hàng để thu thập đầy đủ yêu cầu "
             "cho một dự án Hệ thống Vạn vật Kết nối.",
        backstory=(
            "Bạn là một chuyên gia phân tích nghiệp vụ hàng đầu, chuyên về các dự án phần mềm. "
            "Bạn có kiến thức sâu rộng về phần cứng, kết nối, nền tảng cloud và ứng dụng. "
            "Khả năng của bạn là đặt những câu hỏi sâu sắc, đúng trọng tâm để khám phá mọi khía cạnh "
            "của dự án, từ mục tiêu kinh doanh đến các chi tiết kỹ thuật phức tạp."
        ),
        llm=model_string,
        allow_delegation=False,
        verbose=True
    )
    return input_agent
 