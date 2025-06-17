# --- START OF FILE run_phase_2.py ---

import sys
import os
import logging
from dotenv import load_dotenv
from crewai import Crew, Process

# 1. CẤU HÌNH BAN ĐẦU
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Đang tải biến môi trường từ file .env...")
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    logging.error("Lỗi: Biến môi trường GEMINI_API_KEY chưa được thiết lập.")
    sys.exit("Vui lòng cung cấp khóa API Gemini trong file .env")

# 2. IMPORT CÁC THÀNH PHẦN CỦA CREW
from agents.requirement_agent import get_requirement_agent
# from agents.common_agent import get_researcher_agent # Agent hỗ trợ
from memory.shared_memory import shared_memory

# Import tất cả các nhà máy tạo Task cho Giai đoạn 2
from tasks.requirement_tasks import (
    create_scope_tasks,
    create_brd_tasks,
    create_presentation_tasks,
    create_srs_tasks,   
    create_nfr_tasks,
    create_security_tasks,
    create_usecase_tasks,
    create_rtm_tasks,
    create_impact_analysis_tasks,
    create_sla_tasks,
    create_training_tasks,
    create_checklist_tasks
    )