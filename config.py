import json
import os

_BASE_DIR = os.path.dirname(__file__)

"""short - 0.5..2 min
   medium - 1..5 min
   long - 1..15 min
   very long - 1..30 min"""


class Config:
    def __init__(self):
        self.chat_settings = self.load_chat_settings()

    @staticmethod
    def load_chat_settings():
        with open(f"{_BASE_DIR}/chat_settings.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def upload_chat_settings(self, chat_settings):
        with open(f"{_BASE_DIR}/chat_settings.json", "w", encoding="utf-8") as f:
            json.dump(chat_settings, f, ensure_ascii=False, indent=4)
        self.chat_settings = chat_settings
