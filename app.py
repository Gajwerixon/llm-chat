import gradio as gr
import json

from ollama import chat
from pathlib import Path

SYSTEM_PROMPT = {
    "role": "system", 
    "content": "You are helpful assistant."
}

CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)
CHAT_FILE = CHATS_DIR / "chat_1.json"
print(CHAT_FILE)

initial_conversation = ""
if CHAT_FILE.exists():
    with open(CHAT_FILE, "r", encoding="utf-8") as file:
        initial_conversation = json.load(file)
else:
    initial_conversation = [SYSTEM_PROMPT]

with gr.Blocks() as demo:

    # Data save in Ollama form {"role": ..., "content": ...}
    conversation = gr.State(initial_conversation)

    # Output of current model answer
    chat_output_state = gr.State("")

    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about anything",
            show_label=False,
            elem_id="user-input"
        )

    chat_bot = gr.Chatbot()


    def user(user_input, conversation):
        conversation.append({"role": "user","content": user_input})
        return "", conversation

    def bot(conversation):
        response = chat(
            model="gemma3:4b", 
            messages=conversation, 
            stream=True
        )

        chat_output = ""
        for chunk in response:
            chat_output += chunk.message.content
            conversation_temp = conversation + [{"role": "assistant", "content": chat_output}]
            yield conversation_temp, chat_output


    def update_conversation(conversation, output_state):
        conversation.append({
            "role": "assistant", 
            "content": output_state
        })

        # Save data
        with open(CHAT_FILE, "w", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False, indent=4)

        return conversation


    user_input.submit(
        user, 
        [user_input, conversation],
        [user_input, conversation],
        queue=False
    ).then(
        bot,
        conversation,
        [chat_bot, chat_output_state]
    ).then(
        update_conversation,
        [conversation, chat_output_state],
        conversation
    )

demo.launch()