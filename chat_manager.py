import json
from pathlib import Path


class ChatManager:
    def __init__(self):
        self.chats_dir = Path("chats")
        self.chats_dir.mkdir(exist_ok=True)

        self.state_file = Path("state.json")

        self.system_prompt = {
            "role": "system", 
            "content": "You are a helpful assistant."
        }

        self.current_chat_id = None
        self.current_conversation = []


    def initialize_current_chat(self):
        """Load the active chat or create the first chat"""
        self.current_chat_id = self.get_current_chat_id()

        if self.current_chat_id is None:
            self.current_conversation = self.create_chat()
        else:
            self.current_conversation = self.load_chat()


    def create_chat(self):
        self.current_chat_id = 1

        with open(self.chat_file, "w", encoding="utf-8") as file:
            json.dump(self.system_prompt, file)
            return [self.system_prompt]


    def load_chat(self):
        with open(self.chat_file, "r", encoding="utf-8") as file:
            return json.load(file)


    def save_chat(self, conversation):
        """Save the current conversation to its JSON file"""
        with open(self.chat_file, "w", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False, indent=4)


    def clear_current_chat(self):
        """Remove all messages except the system prompt"""
        with open(self.chat_file, "w", encoding="utf-8") as file:
            json.dump([self.system_prompt], file, ensure_ascii=False, indent=4)
            return self.system_prompt


    def get_current_chat_id(self):
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


    @property
    def chat_file(self):
        return self.chats_dir / f"chat_{self.current_chat_id}.json"