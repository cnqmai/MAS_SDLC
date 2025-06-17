# main.py
import sys
import os
import logging
from dotenv import load_dotenv

# Cấu hình logging và tải biến môi trường
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

# Kiểm tra API key trước khi chạy
if not os.getenv("GEMINI_API_KEY"):
    logging.error("Lỗi: Biến môi trường GEMINI_API_KEY chưa được thiết lập trong file .env")
    sys.exit("Vui lòng cung cấp khóa API Gemini trong file .env")
else:
    logging.info("Đã tải API Key của Gemini thành công.")

# Import các thành phần của CrewAI và các hàm tạo của chúng ta
from crewai import Crew, Process
from agents.input_agent import create_input_agent
from tasks.phase_0.input_tasks import run_input_collection

def main():
    """Hàm chính để khởi tạo và chạy Crew."""
    print("\n--- Bắt đầu chương trình thu thập yêu cầu dự án phần mềm ---")

    # 1. Tạo Agent
    input_agent = create_input_agent()

    # 2. Tạo Task
    input_task = run_input_collection()

    # 3. Tạo và cấu hình Crew
    crew = Crew(
        agents=[input_agent],
        tasks=[input_task],
        process=Process.sequential,
        verbose=2  # Bật chế độ verbose để xem chi tiết quá trình làm việc của agent
    )

    # 4. Bắt đầu thực thi!
    # CrewAI sẽ bắt đầu task, và vì có `human_input=True`, nó sẽ dừng lại để chờ bạn trả lời
    print("\n🚀 Crew đang bắt đầu... Hãy chuẩn bị trả lời các câu hỏi từ Agent.")
    print("------------------------------------------------------------------")
    
    result = crew.kickoff()

    # 5. In và lưu kết quả cuối cùng
    print("\n------------------------------------------------------------------")
    print("🏆 Cuộc phỏng vấn đã kết thúc. Dưới đây là báo cáo tổng hợp:")
    print(result)
    
    # Lưu báo cáo ra file
    save_output("requirement_report.md", result)

if __name__ == "__main__":
    main()