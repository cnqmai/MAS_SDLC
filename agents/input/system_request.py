def load_system_request(file_path="input/system_request.txt") -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        print(f"⚠️ File {file_path} không tồn tại.")
        return ""
    except Exception as e:
        print(f"⚠️ Lỗi khi đọc system request: {e}")
        return ""
