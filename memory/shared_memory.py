# memory/shared_memory.py

class SharedMemory:
    """
    Quản lý bộ nhớ chia sẻ giữa các agent và các phase của dự án.
    """
    _instance = None
    _data = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedMemory, cls).__new__(cls)
        return cls._instance

    def set(self, phase: str, key: str, value: any):
        """
        Lưu trữ một giá trị vào bộ nhớ chia sẻ dưới một phase và key cụ thể.
        """
        if phase not in self._data:
            self._data[phase] = {}
        self._data[phase][key] = value
        print(f"SharedMemory: Đã lưu '{key}' vào phase '{phase}'.")

    def get(self, phase: str, key: str):
        """
        Lấy một giá trị từ bộ nhớ chia sẻ dựa trên phase và key.
        """
        return self._data.get(phase, {}).get(key)

    def get_phase_data(self, phase: str):
        """
        Lấy tất cả dữ liệu của một phase cụ thể.
        """
        return self._data.get(phase, {})

    def clear(self):
        """
        Xóa toàn bộ bộ nhớ chia sẻ.
        """
        self._data = {}
        print("SharedMemory: Đã xóa toàn bộ bộ nhớ.")

# Khởi tạo instance duy nhất
shared_memory = SharedMemory()