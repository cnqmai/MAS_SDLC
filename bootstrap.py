# bootstrap.py (MODIFIED)

import os
from crewai import Crew, Process
from dotenv import load_dotenv
import logging

# Import các hàm tạo agent và task cho TẤT CẢ các giai đoạn
from agents.initiation_agent import create_initiation_agents
from tasks.initiation_tasks import create_initiation_tasks

# --- Thêm import cho Project Manager Agent ---
from agents.project_manager_agent import create_project_manager_agent

# --- Import Researcher Agent nếu bạn muốn sử dụng ---
# from agents.researcher_agent import create_researcher_agent # Cần tạo file này nếu muốn dùng

# --- Phase 1: Planning ---
# from agents.planning_agents import create_planning_agents
# from tasks.planning_tasks import create_planning_tasks

# --- Phase 2: Requirements ---
# from agents.requirement_agents import create_requirement_agents
# from tasks.requirement_tasks import create_requirement_tasks

# --- Phase 3: Design ---
# from agents.design_agents import create_design_agents
# from tasks.design_tasks import create_design_tasks

# --- Phase 4: Development ---
# from agents.development_agents import create_development_agents
# from tasks.development_tasks import create_development_tasks

# --- Phase 5: Testing ---
# from agents.testing_agents import create_testing_agents
# from tasks.testing_tasks import create_testing_tasks

# --- Phase 6: Deployment ---
from agents.deployment_agent import create_deployment_agents
from tasks.deployment_tasks import create_deployment_tasks

# --- Phase 7: Maintenance ---
from agents.maintenance_agent import create_maintenance_agents
from tasks.maintenance_tasks import create_maintenance_tasks

from memory.shared_memory import shared_memory
from utils.file_writer import write_output

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_project_crew(system_request: str):
    """
    Chạy toàn bộ quy trình dự án qua các phase.
    """
    load_dotenv()

    # Đảm bảo thư mục output tồn tại
    output_base_dir = "output"
    # Tạo các thư mục cho từng phase
    for i in range(8): # Từ phase 0 đến phase 7
        os.makedirs(os.path.join(output_base_dir, f"{i}_" + ("initiation" if i==0 else "planning" if i==1 else "requirements" if i==2 else "design" if i==3 else "development" if i==4 else "testing" if i==5 else "deployment" if i==6 else "maintenance")), exist_ok=True)


    # --- KHỞI TẠO CÁC AGENT CHUNG (RESEARCHER VÀ PROJECT MANAGER) MỘT LẦN ---
    project_manager_agent = create_project_manager_agent()
    # researcher_agent = create_researcher_agent() # Nếu bạn đã tạo researcher_agent

    # 0. Giai đoạn Khởi tạo (Initiation)
    logging.info("Bắt đầu Giai đoạn 0: Khởi tạo dự án (Initiation Phase)")
    shared_memory.set("phase_0", "system_request", system_request)

    vision_agent, conops_agent, charter_agent = create_initiation_agents()
    # Truyền project_manager_agent vào hàm tạo tasks
    initiation_tasks = create_initiation_tasks(vision_agent, conops_agent, charter_agent, project_manager_agent) [cite: 78, 94]

    initiation_crew = Crew(
        agents=[vision_agent, conops_agent, charter_agent, project_manager_agent], # Thêm project_manager_agent 
        tasks=initiation_tasks,
        process=Process.sequential,
        verbose=True
    )
    initiation_result = initiation_crew.kickoff()
    logging.info("Hoàn thành Giai đoạn 0: Khởi tạo dự án.")
    logging.info(f"Kết quả Initiation Phase:\n{initiation_result}")

    # 1. Giai đoạn Lập kế hoạch (Planning)
    logging.info("Bắt đầu Giai đoạn 1: Lập kế hoạch (Planning Phase)")
    try:
        # planning_agents = create_planning_agents()
        # planning_tasks = create_planning_tasks(planning_agents, project_manager_agent) # THÊM project_manager_agent

        # planning_crew = Crew(
        #     agents=[planning_agents, project_manager_agent], # THÊM project_manager_agent 
        #     tasks=planning_tasks,
        #     process=Process.sequential,
        #     verbose=True
        # )
        # planning_result = planning_crew.kickoff()
        # logging.info("Hoàn thành Giai đoạn 1: Lập kế hoạch.")
        # logging.info(f"Kết quả Planning Phase:\n{planning_result}")
        logging.info("Giai đoạn 1 (Planning) chưa được triển khai đầy đủ. Bỏ qua.")
    except Exception as e:
        logging.error(f"Lỗi khi chạy Giai đoạn 1 (Planning): {e}")

    # 2. Giai đoạn Yêu cầu (Requirements)
    logging.info("Bắt đầu Giai đoạn 2: Yêu cầu (Requirements Phase)")
    try:
        # requirement_agents = create_requirement_agents()
        # requirement_tasks = create_requirement_tasks(requirement_agents, project_manager_agent)

        # requirement_crew = Crew(
        #     agents=[requirement_agents, project_manager_agent], 
        #     tasks=requirement_tasks,
        #     process=Process.sequential,
        #     verbose=True
        # )
        # requirement_result = requirement_crew.kickoff()
        # logging.info("Hoàn thành Giai đoạn 2: Yêu cầu.")
        # logging.info(f"Kết quả Requirements Phase:\n{requirement_result}")
        logging.info("Giai đoạn 2 (Requirements) chưa được triển khai đầy đủ. Bỏ qua.")
    except Exception as e:
        logging.error(f"Lỗi khi chạy Giai đoạn 2 (Requirements): {e}")

    # 3. Giai đoạn Thiết kế (Design)
    logging.info("Bắt đầu Giai đoạn 3: Thiết kế (Design Phase)")
    try:
        # design_agents = create_design_agents()
        # design_tasks = create_design_tasks(design_agents, project_manager_agent)

        # design_crew = Crew(
        #     agents=[design_agents, project_manager_agent], 
        #     tasks=design_tasks,
        #     process=Process.sequential,
        #     verbose=True
        # )
        # design_result = design_crew.kickoff()
        # logging.info("Hoàn thành Giai đoạn 3: Thiết kế.")
        # logging.info(f"Kết quả Design Phase:\n{design_result}")
        logging.info("Giai đoạn 3 (Design) chưa được triển khai đầy đủ. Bỏ qua.")
    except Exception as e:
        logging.error(f"Lỗi khi chạy Giai đoạn 3 (Design): {e}")

    # 4. Giai đoạn Phát triển (Development)
    logging.info("Bắt đầu Giai đoạn 4: Phát triển (Development Phase)")
    try:
        # development_agent = create_development_agents()
        # development_tasks = create_development_tasks(development_agent, project_manager_agent)

        # development_crew = Crew(
        #     agents=[development_agent, project_manager_agent], 
        #     tasks=development_tasks,
        #     process=Process.sequential,
        #     verbose=True
        # )
        # development_result = development_crew.kickoff()
        # logging.info("Hoàn thành Giai đoạn 4: Phát triển.")
        # logging.info(f"Kết quả Development Phase:\n{development_result}")
        logging.info("Giai đoạn 4 (Development) chưa được triển khai đầy đủ. Bỏ qua.")
    except Exception as e:
        logging.error(f"Lỗi khi chạy Giai đoạn 4 (Development): {e}")

    # 5. Giai đoạn Kiểm thử (Testing)
    logging.info("Bắt đầu Giai đoạn 5: Kiểm thử (Testing Phase)")
    try:
        # testing_agent = create_testing_agents()
        # testing_tasks = create_testing_tasks(testing_agent, project_manager_agent)

        # testing_crew = Crew(
        #     agents=[testing_agent, project_manager_agent], 
        #     tasks=testing_tasks,
        #     process=Process.sequential,
        #     verbose=True
        # )
        # testing_result = testing_crew.kickoff()
        # logging.info("Hoàn thành Giai đoạn 5: Kiểm thử.")
        # logging.info(f"Kết quả Testing Phase:\n{testing_result}")
        logging.info("Giai đoạn 5 (Testing) chưa được triển khai đầy đủ. Bỏ qua.")
    except Exception as e:
        logging.error(f"Lỗi khi chạy Giai đoạn 5 (Testing): {e}")

    # 6. Giai đoạn Triển khai (Deployment)
    logging.info("Bắt đầu Giai đoạn 6: Triển khai (Deployment Phase)")
    try:
        deployment_agent = create_deployment_agents()
        # Truyền project_manager_agent vào hàm tạo tasks
        deployment_tasks = create_deployment_tasks(deployment_agent, project_manager_agent) [cite: 90, 106]

        deployment_crew = Crew(
            agents=[deployment_agent, project_manager_agent], # Thêm project_manager_agent 
            tasks=deployment_tasks,
            process=Process.sequential,
            verbose=True
        )
        deployment_result = deployment_crew.kickoff()
        logging.info("Hoàn thành Giai đoạn 6: Triển khai.")
        logging.info(f"Kết quả Deployment Phase:\n{deployment_result}")
    except Exception as e:
        logging.error(f"Lỗi khi chạy Giai đoạn 6 (Deployment): {e}")

    # 7. Giai đoạn Bảo trì (Maintenance)
    logging.info("Bắt đầu Giai đoạn 7: Bảo trì (Maintenance Phase)")
    try:
        maintenance_agent = create_maintenance_agents()
        # Truyền project_manager_agent vào hàm tạo tasks
        maintenance_tasks = create_maintenance_tasks(maintenance_agent, project_manager_agent) [cite: 92, 108]

        maintenance_crew = Crew(
            agents=[maintenance_agent, project_manager_agent], # Thêm project_manager_agent 
            tasks=maintenance_tasks,
            process=Process.sequential,
            verbose=True
        )
        maintenance_result = maintenance_crew.kickoff()
        logging.info("Hoàn thành Giai đoạn 7: Bảo trì.")
        logging.info(f"Kết quả Maintenance Phase:\n{maintenance_result}")
    except Exception as e:
        logging.error(f"Lỗi khi chạy Giai đoạn 7 (Maintenance): {e}")

    logging.info("Toàn bộ quy trình dự án đã hoàn tất.")

if __name__ == "__main__":
    initial_request = "Tạo một hệ thống quản lý thư viện trực tuyến đơn giản bao gồm quản lý sách, thành viên và cho phép mượn/trả sách."
    run_project_crew(initial_request)