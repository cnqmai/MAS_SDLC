import json
import os


class SharedMemory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SharedMemory, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "memory"):  # Prevent re-initialization
            self.memory = {}

    def set(self, phase, key, value, *, verbose=False):
        if phase not in self.memory:
            self.memory[phase] = {}
        self.memory[phase][key] = value
        if verbose:
            print(f"[SharedMemory] SET {phase}.{key} = {value}")

    def get(self, phase, key, *, default=None):
        return self.memory.get(phase, {}).get(key, default)

    def has(self, phase, key):
        return key in self.memory.get(phase, {})

    def get_phase(self, phase):
        return self.memory.get(phase, {})

    def delete_phase(self, phase):
        if phase in self.memory:
            del self.memory[phase]

    def merge_phases(self, source_phase, target_phase):
        """Merge data from one phase into another."""
        if source_phase in self.memory:
            if target_phase not in self.memory:
                self.memory[target_phase] = {}
            self.memory[target_phase].update(self.memory[source_phase])

    def reset(self):
        """Clear all shared memory"""
        self.memory.clear()
        print("[SharedMemory] Memory reset.")

    def to_dict(self):
        return self.memory

    def load_from_dict(self, data: dict):
        self.memory = data.copy()

    def save_to_file(self, path="shared_memory_state.json"):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=4)
            print(f"[SharedMemory] Saved to {path}")
        except Exception as e:
            print(f"[SharedMemory] Error saving: {e}")

    def load_from_file(self, path="shared_memory_state.json"):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.load_from_dict(data)
                print(f"[SharedMemory] Loaded from {path}")
            except Exception as e:
                print(f"[SharedMemory] Error loading: {e}")


# Singleton instance
shared_memory = SharedMemory()
