import os
from memory.shared_memory import shared_memory  # ✅ chỉnh đường dẫn đúng

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(BASE_DIR, "shared_memory")
MEMORY_FILE = os.path.join(MEMORY_DIR, "shared_state.json")

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"📁 Created: {path}")
    else:
        print(f"✔ Exists: {path}")

def bootstrap_project():
    print("🚀 Bootstrapping SDLC_MAS Project...")

    # 1. Tạo thư mục lưu shared state (dữ liệu runtime nếu cần)
    create_dir(MEMORY_DIR)

    # 2. Load lại bộ nhớ nếu đã tồn tại
    if os.path.exists(MEMORY_FILE):
        shared_memory.load_from_file(MEMORY_FILE)
        print("🔁 Loaded existing shared state.")
    else:
        # 3. Nếu chưa có, khởi tạo bộ nhớ mẫu cho phase_0
        shared_memory.set("phase_0", "status", "pending", verbose=True)
        shared_memory.set("phase_0", "crew", [
            "initiation_agent",
            "researcher_agent",
            "project_manager_agent"
        ])
        shared_memory.set("global", "current_phase", "phase_0", verbose=True)
        shared_memory.save_to_file(MEMORY_FILE)

    print("🧠 Current Shared State:")
    print(shared_memory.to_dict())
    print("✅ Bootstrap completed!")

if __name__ == "__main__":
    bootstrap_project()
