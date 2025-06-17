"""
development_tasks.py
====================
Tổng hợp tất cả các nhiệm vụ giai đoạn Development Phase 4 cho Development Agent.
"""

from crewai import Task
from utils.file_writer import write_output
from memory.shared_memory import shared_memory

# ============================ CODE REVIEW TASKS ============================

def create_code_review_tasks(agent):
    coding_guidelines = shared_memory.get("phase_4_development", "coding_guidelines") or "Coding Guidelines chưa có."
    dev_standards = shared_memory.get("phase_4_development", "dev_standards") or "Development Standards chưa có."

    checklist_task = Task(
        description=f"""
            Tạo checklist kiểm tra mã nguồn chi tiết nhằm đảm bảo code tuân thủ chuẩn dự án.
            [10 mục checklist...]
            - Coding Guidelines: {coding_guidelines[:600]}...
            - Development Standards: {dev_standards[:600]}...
        """,
        expected_output="Checklist kiểm tra mã nguồn lưu tại file: Code_Review_Checklist.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Code_Review_Checklist.md", str(output)),
            shared_memory.set("phase_4_development", "code_review_checklist", str(output))
        )
    )
    return [checklist_task]

# ============================ DEV DOCS TASKS ============================

def create_dev_docs_tasks(agent):
    lld = shared_memory.get("phase_3_design", "low_level_design") or "Tài liệu LLD chưa sẵn sàng."

    source_doc_task = Task(
        description=f"""
            Tạo file Markdown template cho tài liệu mã nguồn.
            - LLD: {lld[:800]}...
        """,
        expected_output="Source_Code_Documentation_Template.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Source_Code_Documentation_Template.md", output),
            shared_memory.set("phase_4_development", "source_code_doc_template", output)
        )
    )

    progress_report_task = Task(
        description="Tạo mẫu báo cáo tiến độ phát triển.",
        expected_output="Development_Progress_Report_Template.docx",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Development_Progress_Report_Template.docx", output),
            shared_memory.set("phase_4_development", "dev_progress_template", output)
        )
    )

    middleware_task = Task(
        description=f"""
            Viết tài liệu middleware chi tiết.
            - LLD: {lld[:1000]}...
        """,
        expected_output="Middleware_Documentation.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Middleware_Documentation.md", output),
            shared_memory.set("phase_4_development", "middleware_docs", output)
        )
    )

    return [source_doc_task, progress_report_task, middleware_task]

# ============================ DEV STANDARDS TASKS ============================

def create_dev_standards_tasks(agent):
    config_plan = shared_memory.get("phase_1_planning", "config_plan") or "Không có Configuration Management Plan."
    project_plan = shared_memory.get("phase_1_planning", "project_plan") or "Không có Project Plan."

    standards_task = Task(
        description=f"""
            Tạo Development Standards và Coding Guidelines.
            - Config Plan: {config_plan[:500]}...
            - Project Plan: {project_plan[:500]}...
        """,
        expected_output="Development_Standards_Document.md và Coding_Guidelines.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Development_Standards_Document.md", output),
            write_output("output/4_development/Coding_Guidelines.md", output),
            shared_memory.set("phase_4_development", "dev_standards", output),
            shared_memory.set("phase_4_development", "coding_guidelines", output)
        )
    )

    review_task = Task(
        description="Đánh giá và xác minh các tiêu chuẩn phát triển.",
        expected_output="dev_standards_validation_report.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/dev_standards_validation_report.md", output),
            shared_memory.set("phase_4_development", "dev_standards_review", output)
        )
    )

    return [standards_task, review_task]

# ============================ INTEGRATION TASKS ============================

def create_integration_tasks(agent):
    hld = shared_memory.get("phase_3_design", "hld") or "Không có High-Level Design."
    api_doc = shared_memory.get("phase_4_development", "api_design") or "Không có API Design."

    integration_plan_task = Task(
        description=f"Tạo tài liệu tích hợp hệ thống.\n- HLD: {hld[:500]}...\n- API: {api_doc[:500]}...",
        expected_output="Integration_Plan.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Integration_Plan.md", str(output)),
            shared_memory.set("phase_4_development", "integration_plan", str(output))
        )
    )

    unit_test_template_task = Task(
        description="Tạo template Unit Test.",
        expected_output="Unit_Test_Scripts_Template.txt",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Unit_Test_Scripts_Template.txt", str(output)),
            shared_memory.set("phase_4_development", "unit_test_template", str(output))
        )
    )

    return [integration_plan_task, unit_test_template_task]

# ============================ SOURCE CONTROL TASKS ============================

def create_source_control_tasks(agent):
    dev_standards = shared_memory.get("phase_4_development", "dev_standards") or "Không có Development Standards."
    coding_guidelines = shared_memory.get("phase_4_development", "coding_guidelines") or "Không có Coding Guidelines."

    version_control_task = Task(
        description=f"Tạo Version Control Plan.\n- Standards: {dev_standards[:500]}...",
        expected_output="Version_Control_Plan.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Version_Control_Plan.md", str(output)),
            shared_memory.set("phase_4_development", "version_control_plan", str(output))
        )
    )

    repo_checklist_task = Task(
        description=f"Tạo Source Code Repository Checklist.\n- Guidelines: {coding_guidelines[:500]}...",
        expected_output="Source_Code_Repository_Checklist.md",
        agent=agent,
        callback=lambda output: (
            write_output("output/4_development/Source_Code_Repository_Checklist.md", str(output)),
            shared_memory.set("phase_4_development", "repo_checklist", str(output))
        )
    )

    return [version_control_task, repo_checklist_task]

# ============================ TỔNG HỢP ============================

def create_all_development_tasks(agent):
    return (
        create_code_review_tasks(agent) +
        create_dev_docs_tasks(agent) +
        create_dev_standards_tasks(agent) +
        create_integration_tasks(agent) +
        create_source_control_tasks(agent)
    )
