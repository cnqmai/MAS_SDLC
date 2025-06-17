import os

def write_output(filename: str, content):
    """
    Ghi nội dung vào file.

    Args:
        filename (str): đường dẫn tương đối, ví dụ '1_initiation/vision_document.md'
        content (str | bất kỳ): nội dung để ghi ra file
    """
    try:
        # Đảm bảo đường dẫn có thư mục output/ ở đầu
        if filename.startswith("output/"):
            full_path = filename
        else:
            full_path = os.path.join("output", filename)
        
        # Đảm bảo thư mục tồn tại
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(str(content))
        print(f"✅ Đã ghi file thành công: {full_path}")
    except Exception as e:
        print(f"❌ Lỗi khi ghi file {filename}: {e}")