import gradio as gr
import random
import time

SYSTEM_PROMPT = {
    "role": "system", 
    "content": "You are helpful assistant."
}

with gr.Blocks() as demo:

    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about anything",
            show_label=False,
            elem_id="user-input"
        )

    chat_bot = gr.Chatbot()


    def user(user_input, history):
        return "", history +  [
            {"role": "user", "content": user_input}
        ]

    def bot(history):
        messages = [SYSTEM_PROMPT] + history

        bot_message = random.choice([
            "Hello, I am not working...",
            "Hi, I am not working...",
            "Good morning, I am not working..."
        ])

        time.sleep(2)

        history.append({"role": "assistant", "content": bot_message})
        return history

    user_input.submit(
        user, 
        [user_input, chat_bot],
        [user_input, chat_bot],
        queue=False
    ).then(
        bot, chat_bot, chat_bot
    )

demo.launch()