# Công cụ định dạng văn bản

def generate_heading(title: str, level: int = 1) -> str:
    """Tạo heading Markdown với cấp độ nhất định. Ví dụ: level=2 → ## Title"""
    return f"{'#' * level} {title}\n"

def format_section(title: str, body: str, level: int = 2) -> str:
    """Định dạng một section với heading và nội dung."""
    heading = generate_heading(title, level)
    return f"{heading}\n{body.strip()}\n"

def create_table(headers: list[str], rows: list[list[str]]) -> str:
    """Tạo bảng Markdown từ danh sách tiêu đề và dòng."""
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, separator] + row_lines)

def wrap_code_block(code: str, lang: str = "python") -> str:
    """Đóng gói đoạn mã trong block Markdown."""
    return f"```{lang}\n{code.strip()}\n```"

def clean_output(text: str) -> str:
    """Dọn sạch văn bản đầu ra: loại bỏ dòng trắng thừa, strip dòng."""
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()
