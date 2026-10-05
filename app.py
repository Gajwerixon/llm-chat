import gradio as gr
from ollama import chat

SYSTEM_PROMPT = {
    "role": "system", 
    "content": "You are helpful assistant."
}

with gr.Blocks() as demo:

    # Data save in Ollama form {"role": ..., "content": ...}
    conversation = gr.State([SYSTEM_PROMPT])

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
            yield conversation_temp

        conversation.append({
            "role": "assistant", 
            "content": chat_output
        })


    user_input.submit(
        user, 
        [user_input, conversation],
        [user_input, conversation],
        queue=False
    ).then(
        bot, 
        conversation, 
        chat_bot
    )

demo.launch()