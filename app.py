import gradio as gr
from ollama import chat

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
        return "", history +  [{"role": "user","content": user_input}]

    def bot(history):
        messages = [SYSTEM_PROMPT]

        for items in history:
            messages.append({
                "role": items["role"], 
                "content": items["content"][0]["text"]
            })

        response = chat(
            model="gemma3:4b", 
            messages=messages, 
            stream=True
        )

        chat_output = ""
        for chunk in response:
            chat_output += chunk.message.content

        history.append({
            "role": "assistant", 
            "content": chat_output
        })
        return history

    user_input.submit(
        user, 
        [user_input, chat_bot],
        [user_input, chat_bot],
        queue=False
    ).then(
        bot, 
        chat_bot, 
        chat_bot
    )

demo.launch()