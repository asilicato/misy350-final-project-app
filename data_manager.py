import json
from pathlib import Path


class DataManager:
    def __init__(self, file_path, default_data):
        self.file_path = Path(file_path)
        self.default_data = default_data

    def load_data(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as file:
                    return json.load(file)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self.default_data, file, indent=4)

            return self.default_data

        except Exception:
            return self.default_data

    def save_data(self, data):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            return True

        except Exception:
            return False