import os

def load_prompt(prompt_name: str, prompts_dir: str = "prompts") -> str:
    """
    Tải nội dung prompt từ file .txt trong thư mục prompts/

    Args:
        prompt_name (str): tên file (không kèm .txt)
        prompts_dir (str): đường dẫn thư mục prompt

    Returns:
        str: nội dung prompt
    """
    filename = os.path.join(prompts_dir, f"{prompt_name}.txt")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Không tìm thấy file prompt: {filename}")

    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
