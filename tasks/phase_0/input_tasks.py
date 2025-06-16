import os
from memory.shared_memory import shared_memory # Tạm thời comment lại nếu chưa có file này

def run_input_collection():
    """
    Chạy một cuộc hội thoại để thu thập yêu cầu cho một dự án,
    với các câu hỏi được cấu trúc theo quy trình SDLC.
    """

    # --- BỘ CÂU HỎI MỚI CHO DỰ ÁN  THEO SDLC ---

    # Giai đoạn 1: Lập kế hoạch & Phân tích Yêu cầu (Planning & Requirement Analysis)
    planning_questions = {
        "title": "1. Lập Kế Hoạch & Yêu Cầu Chung",
        "questions": [
            "Tên hệ thống/dự án là gì?",
            "Mục tiêu chính của hệ thống là gì? (Ví dụ: giám sát nông nghiệp, nhà thông minh, theo dõi tài sản)",
            "Hệ thống này giải quyết vấn đề cụ thể nào cho người dùng hoặc doanh nghiệp?",
            "Ai là người dùng cuối của hệ thống? (Ví dụ: kỹ sư vận hành, người quản lý, người dân)",
            "Phạm vi của dự án là gì? (Chỉ giám sát, hay có cả điều khiển thiết bị từ xa?)",
            "Dự án có những ràng buộc nào về thời gian hoặc ngân sách không?"
        ]
    }

    # Giai đoạn 2: Thiết kế Hệ thống (System Design) - Chia nhỏ theo các lớp của 
    design_hardware_questions = {
        "title": "2.1. Thiết Kế - Phần Cứng (The 'Things')",
        "questions": [
            "Hệ thống sẽ sử dụng những loại cảm biến (sensor) hoặc cơ cấu chấp hành (actuator) nào? (Ví dụ: nhiệt độ, độ ẩm, GPS, relay...)",
            "Thiết bị sẽ hoạt động bằng nguồn điện nào? (Pin, điện lưới, năng lượng mặt trời?)",
            "Môi trường hoạt động của các thiết bị là gì? (Trong nhà, ngoài trời, nhà máy công nghiệp?)",
            "Có yêu cầu cụ thể nào về vỏ hộp hay độ bền của thiết bị không (ví dụ: chống nước, chống bụi IP67)?"
        ]
    }

    design_connectivity_questions = {
        "title": "2.2. Thiết Kế - Kết Nối (Connectivity)",
        "questions": [
            "Dữ liệu từ thiết bị sẽ được gửi đi bằng phương thức kết nối nào? (WiFi, Bluetooth/BLE, 4G/5G, LoRaWAN?)",
            "Tần suất gửi dữ liệu dự kiến là bao lâu một lần? (Mỗi giây, mỗi phút, mỗi giờ?)",
            "Giao thức truyền tin dự kiến là gì? (MQTT, HTTP, CoAP, hay giao thức khác?)"
        ]
    }
    
    design_platform_questions = {
        "title": "2.3. Thiết Kế - Nền tảng & Dữ liệu (Platform & Data)",
        "questions": [
            "Dữ liệu thu thập sẽ được xử lý và lưu trữ ở đâu? (Trên cloud, tại một server cục bộ, hay xử lý tại biên - edge computing?)",
            "Có yêu cầu tích hợp với nền tảng cloud cụ thể nào không? (AWS, Azure Hub, Google Cloud?)",
            "Hệ thống cần lưu trữ dữ liệu trong bao lâu? Có yêu cầu gì về truy xuất dữ liệu lịch sử không?"
        ]
    }

    design_application_questions = {
        "title": "2.4. Thiết Kế - Ứng dụng & Giao diện (Application & UI/UX)",
        "questions": [
            "Người dùng sẽ tương tác với hệ thống qua đâu? (Web dashboard, ứng dụng di động, email/SMS cảnh báo?)",
            "Hệ thống cần cung cấp những loại báo cáo, thống kê hay biểu đồ trực quan hóa dữ liệu nào?",
            "Giao diện người dùng cần có những đặc điểm gì? (Đơn giản, hiện đại, hiển thị real-time?)"
        ]
    }

    # Giai đoạn 3: Vận hành & Bảo trì (Operation & Maintenance)
    operation_questions = {
        "title": "3. Vận Hành & Bảo Mật",
        "questions": [
            "Hệ thống có yêu cầu đặc biệt nào về bảo mật không? (Mã hóa dữ liệu, xác thực thiết bị an toàn?)",
            "Có cần hỗ trợ cập nhật phần mềm cho thiết bị từ xa (OTA - Over-the-Air) không?",
            "Làm thế nào để quản lý và giám sát trạng thái của hàng loạt thiết bị? (Ví dụ: trạng thái pin, kết nối)"
        ]
    }
    
    # Tập hợp tất cả các nhóm câu hỏi
    all_question_groups = [
        planning_questions,
        design_hardware_questions,
        design_connectivity_questions,
        design_platform_questions,
        design_application_questions,
        operation_questions
    ]
    
    system_info = {}
    system_request = ""

    # Vòng lặp thu thập thông tin theo từng nhóm
    for group in all_question_groups:
        title = group["title"]
        questions = group["questions"]
        
        print(f"\n--- Bắt đầu nhóm câu hỏi: {title} ---")
        system_request += f"## {title}\n"
        
        for question in questions:
            print(f"\n🤖 Agent: {question}")
            answer = input("👤 Bạn: ")
            system_info[question] = answer # Lưu trữ Q&A
            system_request += f"**Câu hỏi:** {question}\n**Trả lời:** {answer}\n\n"

    # Lưu vào shared_memory (nếu bạn có module này)
    shared_memory.set("phase_0", "system_request", system_request)

    # Ghi vào file output/system_request.txt
    os.makedirs("output", exist_ok=True)
    with open("output/system_request.txt", "w", encoding="utf-8") as f:
        f.write(system_request)

    print("\n✅ Đã tạo file system_request.txt với thông tin yêu cầu hệ thống.\n")

# Chạy hàm chính
if __name__ == "__main__":
    run_input_collection()