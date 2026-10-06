import json
from pathlib import Path

import gradio as gr
from ollama import chat


CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)
CHAT_FILE = CHATS_DIR / "chat_1.json"

SYSTEM_PROMPT = {
    "role": "system", 
    "content": "You are a helpful assistant."
}

chat_history = []

if CHAT_FILE.exists():
    with open(CHAT_FILE, "r", encoding="utf-8") as file:
        initial_conversation = json.load(file)

        for message in initial_conversation:
            if message["role"] == "system":
                continue
            chat_history.append(message)

else:
    initial_conversation = [SYSTEM_PROMPT]


with gr.Blocks() as demo:

    # Conversation history in Ollama message format
    conversation = gr.State(initial_conversation)

    # Current model response.
    chat_output_state = gr.State("")

    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about anything",
            show_label=False,
            elem_id="user-input"
        )

    chat_bot = gr.Chatbot(value=chat_history)

    with gr.Row():
        clear_btn = gr.Button(value="Clear chat")


    def user(user_input, conversation):
        conversation.append({"role": "user", "content": user_input})
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
            conversation_temp = conversation + [
                {"role": "assistant", "content": chat_output}
            ]
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


    def clear_chat(conversation, chat_output_state):

        conversation = [conversation[0]]

        chat_output_state = ""

        with open(CHAT_FILE, "w", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False, indent=4)

        return conversation, chat_output_state, []
        
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

    clear_btn.click(
        clear_chat,
        [conversation, chat_output_state],
        [conversation, chat_output_state, chat_bot]
    )

demo.launch()