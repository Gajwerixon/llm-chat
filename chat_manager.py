import json
from pathlib import Path

CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)


class ChatManager:
    def __init__(self):
        self.chats_dir = Path("chats")
        self.state_file = Path("state.json")
        self.system_prompt = {
            "role": "system", 
            "content": "You are a helpful assistant."
        }

        self.current_chat_id = None
        self.current_conversation = None
        self.chat_history = []


    def initialize_current_chat(self):
        self.current_chat_id = self.get_current_chat_id()

        if self.current_chat_id is None:
            self.current_conversation = self.create_chat()
        else:
            self.current_conversation = self.load_chat()
            self.chat_history = self.get_chat_history()


    def add_assistant_message(self, conversation):
        with open(self.get_formated_chat_file, "w", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False, indent=4)


    def clear_current_chat(self, conversation):
        with open(self.get_formated_chat_file, "w", encoding="utf-8") as file:
            json.dump(self.system_prompt, file, ensure_ascii=False, indent=4)
            return self.system_prompt


    def get_current_chat_id(self):
        """Get current chat id"""
        if self.state_file.exists():
            with open(self.state_file, "r", encoding="utf-8") as file:
                return json.load(file)["current_chat"]
        else:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump({"current_chat": None}, file)
                return None

    def get_chat_history(self):    
        return [
            message
            for message in self.current_conversation
            if message["role"] != "system"
        ]


    def create_chat(self):
        self.chats_dir.mkdir(exist_ok=True)
        self.current_chat_id = 1

        with open(self.get_formated_chat_file, "w", encoding="utf-8") as file:
            json.dump(self.system_prompt, file)
            return [self.system_prompt]


    def load_chat(self):
        with open(self.get_formated_chat_file, "r", encoding="utf-8") as file:
            return json.load(file)


    @property
    def get_formated_chat_file(self):
        return self.chats_dir / f"chat_{self.current_chat_id}.json"