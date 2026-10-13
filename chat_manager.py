import json
from pathlib import Path


class ChatManager:
    """Manage chat conversations and persist them as JSON files."""

    def __init__(self):
        """Initialize storage paths and default conversation data."""
        self.chats_dir = Path("chats")
        self.chats_dir.mkdir(exist_ok=True)

        self.state_file = Path("state.json")

        self.system_prompt = [{
            "role": "system", 
            "content": "You are a helpful assistant."
        }]

        self.current_chat_id = None
        self.current_conversation = []


    def initialize_current_chat(self):
        """Load the previously active chat or create the first one."""
        chat_id = self._read_current_chat_id()

        if self.current_chat_id is not None:
            self.current_chat_id = chat_id
            self.current_conversation = self.load_chat()
        else:
            self.current_conversation = self.create_new_chat()


    def create_new_chat(self):
        """Create a new chat and make it the active conversation."""
        chat_ids = self.get_chat_ids()
        self.current_chat_id = max(chat_ids, default=0) + 1

        self.current_conversation = self.system_prompt.copy()

        self.save_chat(self.current_conversation)
        self._save_current_chat_id()

        return self.current_conversation


    def load_chat(self):
        """Load the active conversation from its JSON file."""
        with open(self.chat_file, "r", encoding="utf-8") as file:
            return json.load(file)


    def save_chat(self, conversation):
        """Save a conversation to the active chat's JSON file."""
        with open(self.chat_file, "w", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False, indent=4)


    def get_chat_ids(self):
        """Return existing chat IDs in ascending numerical order."""
        chat_ids = []

        for path in self.chats_dir.glob("chat_*.json"):
            try:
                chat_id = int(path.stem.removeprefix("chat_"))
            except ValueError:
                continue

            chat_ids.append(chat_id)

        return sorted(chat_ids)


    def switch_chat(self, chat_id):
        """Switch to an existing chat and return its conversation."""
        self.current_chat_id = chat_id

        self.current_conversation = self.load_chat()
        self._save_current_chat_id()

        return self.current_conversation


    def get_chat_history(self): 
        """Return the active conversation without the system prompt."""
        chat_history = []

        for message in self.current_conversation:
            if message["role"] != "system":
                chat_history.append(message)

        return chat_history


    def _save_current_chat_id(self):
        """Persist the ID of the active chat."""
        with self.state_file.open("w", encoding="utf-8") as file:
            json.dump(
                {"current_chat": self.current_chat_id},
                file,
                indent=4,
            )


    def _read_current_chat_id(self):
        """Read the active chat ID from the state file."""
        if not self.state_file.exists():
            return None

        with self.state_file.open("r", encoding="utf-8") as file:
            return json.load(file).get("current_chat")
    

    @property
    def chat_file(self):
        """Return the file path for the active conversation."""
        return self.chats_dir / f"chat_{self.current_chat_id}.json"